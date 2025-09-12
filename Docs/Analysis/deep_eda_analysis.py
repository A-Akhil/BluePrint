#!/usr/bin/env python3
"""
Deep Statistical EDA for NCBI BLAST Databases (Marine eDNA focus)
Adds: accurate metadata parsing, taxonomy structural metrics, sequence sampling (length + GC),
compression efficiency, branching factor, depth distribution, and eukaryotic database efficiency.
"""
import os
import json
import sqlite3
import subprocess
from collections import defaultdict, Counter
import re
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_PATH = 'ncbi_blast_db_files'

class DeepEDA:
    def __init__(self, base_path=BASE_PATH):
        self.base_path = base_path
        self.metadata_files = []
        self.taxonomy_db = None
        self._scan()

    def _scan(self):
        if not os.path.isdir(self.base_path):
            raise FileNotFoundError(self.base_path)
        for f in os.listdir(self.base_path):
            if f.endswith('-metadata.json'):
                self.metadata_files.append(f)
            elif f.endswith('.sqlite3') and 'tax' in f:
                self.taxonomy_db = os.path.join(self.base_path, f)

    def load_metadata(self) -> pd.DataFrame:
        records = []
        for meta in self.metadata_files:
            path = os.path.join(self.base_path, meta)
            try:
                with open(path,'r') as fh:
                    data = json.load(fh)
                if not isinstance(data, dict):
                    continue
                rec = {}
                rec['raw_name'] = meta.replace('-metadata.json','')
                # Normalize keys
                rec['dbname'] = data.get('dbname', rec['raw_name'])
                rec['version'] = data.get('version')
                rec['dbtype'] = data.get('dbtype')
                rec['description'] = data.get('description','')
                # Accept multiple possible key variants
                rec['sequences'] = data.get('number-of-sequences') or data.get('sequences') or 0
                rec['letters'] = data.get('number-of-letters') or data.get('letters') or 0
                rec['bytes_to_cache'] = data.get('bytes-to-cache') or data.get('bytes_to_cache')
                rec['bytes_total_compressed'] = data.get('bytes-total-compressed') or data.get('bytes_total_compressed')
                rec['num_volumes'] = data.get('number-of-volumes') or data.get('number_of_volumes')
                files = data.get('files') or []
                rec['file_count'] = len(files) if isinstance(files,list) else None
                rec['is_euk_focus'] = int(bool(re.search(r'euk|fung|its|ssu|lsu', rec['raw_name'], re.I)))
                rec['is_protein'] = int(bool(re.search(r'prot|protein|swiss|nr', rec['raw_name'], re.I)))
                rec['is_rRNA_marker'] = int(bool(re.search(r'ssu|lsu|16s|18s|28s|rrna', rec['raw_name'], re.I)))
                records.append(rec)
            except Exception as e:
                print(f"Metadata read fail {meta}: {e}")
        df = pd.DataFrame(records)
        if not df.empty:
            df['avg_len'] = df.apply(lambda r: (r.letters / r.sequences) if r.sequences else np.nan, axis=1)
            # Compression efficiency metrics
            if 'bytes_total_compressed' in df:
                df['letters_per_compressed_byte'] = df.apply(lambda r: (r.letters / r.bytes_total_compressed) if r.bytes_total_compressed and r.bytes_total_compressed>0 else np.nan, axis=1)
            df['letters_per_sequence_log10'] = np.log10(df['avg_len'].replace(0,np.nan))
        return df

    def visualize_metadata(self, df: pd.DataFrame):
        if df.empty:
            print('No metadata to visualize')
            return
        plt.figure(figsize=(10,6))
        sns.histplot(df['sequences'][df['sequences']>0], bins=30, log_scale=True)
        plt.title('Distribution of Sequence Counts (log-scale)')
        plt.xlabel('Sequences')
        plt.ylabel('Databases')
        plt.tight_layout(); plt.savefig('deep_seqcount_distribution.png', dpi=250); plt.close()

        plt.figure(figsize=(10,6))
        sns.histplot(df['avg_len'].dropna(), bins=30)
        plt.title('Average Sequence Length Distribution')
        plt.xlabel('Average length'); plt.ylabel('Databases')
        plt.tight_layout(); plt.savefig('deep_avglen_distribution.png', dpi=250); plt.close()

        if 'letters_per_compressed_byte' in df:
            plt.figure(figsize=(10,6))
            sns.histplot(df['letters_per_compressed_byte'].dropna(), bins=30)
            plt.title('Compression Efficiency (letters per compressed byte)')
            plt.xlabel('Letters / Compressed Byte')
            plt.tight_layout(); plt.savefig('deep_compression_efficiency.png', dpi=250); plt.close()

        # Correlation heatmap
        corr_cols = ['sequences','letters','avg_len','bytes_to_cache','bytes_total_compressed','file_count','num_volumes']
        corr_df = df[corr_cols].select_dtypes(include=[float,int])
        corr = corr_df.corr()
        plt.figure(figsize=(8,6))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='viridis', square=True)
        plt.title('Metadata Metric Correlations')
        plt.tight_layout(); plt.savefig('deep_metadata_correlation.png', dpi=250); plt.close()

    # Taxonomy structural analysis
    def taxonomy_structure(self, sample_limit=None):
        if not self.taxonomy_db:
            print('No taxonomy DB')
            return {}
        conn = sqlite3.connect(self.taxonomy_db)
        cur = conn.cursor()
        cur.execute('SELECT taxid,parent FROM TaxidInfo')
        rows = cur.fetchmany(sample_limit) if sample_limit else cur.fetchall()
        parent_map = {}
        children = defaultdict(list)
        for taxid,parent in rows:
            parent_map[taxid]=parent
            children[parent].append(taxid)
        conn.close()
        # Depth computation with memoization
        depth_cache = {}
        def depth(tid):
            if tid in depth_cache:
                return depth_cache[tid]
            p = parent_map.get(tid)
            if p is None or p==tid:
                depth_cache[tid]=0; return 0
            d = 1 + depth(p)
            depth_cache[tid]=d
            return d
        sample_taxids = list(parent_map.keys())[:200000]  # limit for performance
        depths = [depth(t) for t in sample_taxids]
        branching = [len(children[t]) for t in sample_taxids]
        depth_series = pd.Series(depths)
        branch_series = pd.Series(branching)
        plt.figure(figsize=(10,6))
        depth_series.hist(bins=40)
        plt.title('Taxonomy Depth Distribution (sample)')
        plt.xlabel('Depth'); plt.ylabel('Count')
        plt.tight_layout(); plt.savefig('deep_taxonomy_depth_distribution.png', dpi=250); plt.close()

        plt.figure(figsize=(10,6))
        branch_series[branch_series<50].hist(bins=50)
        plt.title('Branching Factor Distribution (capped <50)')
        plt.xlabel('Children per Node'); plt.ylabel('Count')
        plt.tight_layout(); plt.savefig('deep_taxonomy_branching_distribution.png', dpi=250); plt.close()

        return {
            'sample_taxids': len(sample_taxids),
            'max_depth': int(depth_series.max()),
            'median_depth': float(depth_series.median()),
            'mean_depth': float(depth_series.mean()),
            'nodes_with_no_children': int((branch_series==0).sum()),
            'mean_branching_factor': float(branch_series.mean()),
            'p95_branching_factor': float(branch_series.quantile(0.95))
        }

    def sample_sequence_lengths_and_gc(self, db_name, max_entries=80, seq_entries_for_gc=30):
        """Sample sequence lengths and GC content via blastdbcmd; fail gracefully if tool absent."""
        db_path = os.path.join(self.base_path, db_name)
        if not any(f.startswith(db_name) for f in os.listdir(self.base_path)):
            return {'error': 'db files not found'}
        base_cmd = f"blastdbcmd -db {db_path} -entry all -outfmt '%a %l' | head -{max_entries}"
        try:
            r = subprocess.run(base_cmd, shell=True, capture_output=True, text=True, timeout=45)
            if r.returncode!=0 or not r.stdout.strip():
                return {'error': 'blastdbcmd failed lengths'}
            lengths = []
            accs = []
            for line in r.stdout.strip().split('\n'):
                parts = line.strip().split()
                if len(parts)>=2 and parts[-1].isdigit():
                    acc = parts[0]
                    ln = int(parts[1])
                    accs.append(acc)
                    lengths.append(ln)
            stats = {}
            if lengths:
                arr = np.array(lengths)
                stats = {
                    'count': int(len(arr)),
                    'min': int(arr.min()),
                    'p25': float(np.percentile(arr,25)),
                    'median': float(np.median(arr)),
                    'p75': float(np.percentile(arr,75)),
                    'max': int(arr.max()),
                    'mean': float(arr.mean()),
                    'std': float(arr.std())
                }
                plt.figure(figsize=(8,5))
                sns.histplot(arr, bins=30)
                plt.title(f'Sequence Length Distribution (sample) - {db_name}')
                plt.xlabel('Length'); plt.ylabel('Frequency')
                plt.tight_layout(); plt.savefig(f'deep_lengths_{db_name}.png', dpi=220); plt.close()
            # GC sampling
            gc_stats = {}
            if accs:
                subset = accs[:seq_entries_for_gc]
                acc_list = ','.join(subset)
                gc_cmd = f"blastdbcmd -db {db_path} -entry {acc_list} -outfmt '%a %s'"
                r2 = subprocess.run(gc_cmd, shell=True, capture_output=True, text=True, timeout=60)
                if r2.returncode==0 and r2.stdout.strip():
                    gc_vals = []
                    for line in r2.stdout.strip().split('\n'):
                        parts = line.split()
                        if len(parts)>=2:
                            seq = parts[-1].upper()
                            if seq:
                                gc = (seq.count('G')+seq.count('C'))/len(seq)
                                n_frac = seq.count('N')/len(seq)
                                gc_vals.append((gc,n_frac))
                    if gc_vals:
                        gcs = np.array([g for g,_ in gc_vals])
                        nfs = np.array([n for _,n in gc_vals])
                        gc_stats = {
                            'gc_mean': float(gcs.mean()),
                            'gc_std': float(gcs.std()),
                            'gc_min': float(gcs.min()),
                            'gc_max': float(gcs.max()),
                            'n_content_mean': float(nfs.mean())
                        }
                        plt.figure(figsize=(6,4))
                        sns.histplot(gcs, bins=15)
                        plt.title(f'GC% Distribution (sample) - {db_name}')
                        plt.xlabel('GC fraction'); plt.tight_layout(); plt.savefig(f'deep_gc_{db_name}.png', dpi=220); plt.close()
            return {'length_stats': stats, 'gc_stats': gc_stats}
        except subprocess.TimeoutExpired:
            return {'error': 'timeout'}
        except FileNotFoundError:
            return {'error': 'blastdbcmd not installed'}
        except Exception as e:
            return {'error': str(e)}

    def euk_detail(self, df: pd.DataFrame):
        if df.empty: return {}
        euk_df = df[df.is_euk_focus==1].copy()
        if euk_df.empty: return {}
        # Efficiency metrics
        euk_df['letters_per_sequence'] = euk_df['avg_len']
        summary = {
            'euk_db_count': int(len(euk_df)),
            'total_euk_sequences': int(euk_df.sequences.sum()),
            'total_euk_letters': int(euk_df.letters.sum()),
            'median_letters_per_sequence': float(euk_df.letters_per_sequence.median()),
            'top_by_sequences': euk_df.sort_values('sequences', ascending=False)[['raw_name','sequences']].head(5).to_dict(orient='records')
        }
        plt.figure(figsize=(10,6))
        top = euk_df.sort_values('sequences', ascending=False).head(10)
        sns.barplot(x='sequences', y='raw_name', data=top)
        plt.title('Top Euk-Focused Databases by Sequence Count')
        plt.xlabel('Sequences'); plt.ylabel('Database')
        plt.tight_layout(); plt.savefig('deep_euk_top_sequences.png', dpi=250); plt.close()
        return summary

    def run(self):
        print('=== DEEP EDA START ===')
        meta_df = self.load_metadata()
        print(f'Metadata databases parsed: {len(meta_df)}')
        if not meta_df.empty:
            nonzero = (meta_df.sequences>0).sum()
            print(f'Databases with sequence counts >0: {nonzero}')
            print(meta_df[['raw_name','sequences','letters','avg_len']].head())
        self.visualize_metadata(meta_df)
        tax_struct = self.taxonomy_structure()
        if tax_struct:
            print('Taxonomy structural metrics:', tax_struct)
        # Sequence sampling for selected representative databases (prefer small marker sets)
        targets = ['SSU_eukaryote_rRNA','LSU_eukaryote_rRNA','ITS_eukaryote_sequences']
        seq_sampling_results = {}
        for t in targets:
            # some metadata names end with -nucl so test both
            for candidate in [t, f'{t}-nucl']:
                res = self.sample_sequence_lengths_and_gc(candidate)
                if 'error' not in res:
                    seq_sampling_results[candidate]=res
                    break
        if seq_sampling_results:
            print('Sequence sampling results (length + GC):')
            for db,res in seq_sampling_results.items():
                print(db, res)
        euk_summary = self.euk_detail(meta_df)
        print('Eukaryotic focus summary:', euk_summary)
        # Save combined JSON summary
        out = {
            'taxonomy_structure': tax_struct,
            'sequence_sampling': seq_sampling_results,
            'euk_summary': euk_summary,
            'global_totals': {
                'total_sequences_all': int(meta_df.sequences.sum()) if not meta_df.empty else 0,
                'total_letters_all': int(meta_df.letters.sum()) if not meta_df.empty else 0
            }
        }
        with open('deep_eda_summary.json','w') as fh:
            json.dump(out, fh, indent=2)
        print('=== DEEP EDA COMPLETE ===')
        return out

if __name__ == '__main__':
    DeepEDA().run()
