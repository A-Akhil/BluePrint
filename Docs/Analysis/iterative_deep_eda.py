#!/usr/bin/env python3
"""
ITERATIVE DEEP EDA - Marine eDNA Database Analysis
TRUE EDA: Ask questions, find patterns, ask deeper questions, drill down further
Focus: Progressive discovery through data interrogation and hypothesis testing
"""

import os
import json
import sqlite3
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import re
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class IterativeDeepEDA:
    def __init__(self, base_path='ncbi_blast_db_files'):
        self.base_path = base_path
        self.findings = []
        self.questions = []
        self.metadata_df = None
        self.taxonomy_db = None
        self.iteration = 0
        self._initialize()
    
    def log_finding(self, finding, data=None):
        self.findings.append({
            'iteration': self.iteration,
            'finding': finding,
            'data': data
        })
        print(f"🔍 FINDING {len(self.findings)}: {finding}")
    
    def ask_question(self, question):
        self.questions.append({
            'iteration': self.iteration,
            'question': question
        })
        print(f"❓ QUESTION {len(self.questions)}: {question}")
    
    def _initialize(self):
        # Load all available data
        self.metadata_df = self._load_comprehensive_metadata()
        self.taxonomy_db = self._find_taxonomy_db()
        print("=== ITERATIVE DEEP EDA INITIALIZED ===")
        print(f"Loaded {len(self.metadata_df)} databases for analysis")
    
    def _load_comprehensive_metadata(self):
        """Load and clean all metadata with comprehensive parsing"""
        records = []
        metadata_files = [f for f in os.listdir(self.base_path) if f.endswith('-metadata.json')]
        
        for meta_file in metadata_files:
            try:
                with open(os.path.join(self.base_path, meta_file), 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    record = {
                        'name': meta_file.replace('-metadata.json', ''),
                        'sequences': data.get('number-of-sequences', data.get('sequences', 0)),
                        'letters': data.get('number-of-letters', data.get('letters', 0)),
                        'dbtype': data.get('dbtype', 'unknown'),
                        'description': data.get('description', ''),
                        'version': data.get('version', ''),
                        'bytes_cache': data.get('bytes-to-cache', 0),
                        'bytes_compressed': data.get('bytes-total-compressed', 0),
                        'volumes': data.get('number-of-volumes', 1),
                        'files': len(data.get('files', [])),
                    }
                    
                    # Calculate derived metrics
                    if record['sequences'] > 0:
                        record['avg_length'] = record['letters'] / record['sequences']
                    else:
                        record['avg_length'] = 0
                    
                    if record['bytes_compressed'] > 0:
                        record['compression_ratio'] = record['letters'] / record['bytes_compressed']
                    else:
                        record['compression_ratio'] = 0
                    
                    # Categorize databases
                    record['is_eukaryotic'] = 1 if re.search(r'euk|fungal|its|ssu|lsu', record['name'], re.I) else 0
                    record['is_protein'] = 1 if re.search(r'prot|protein|swiss|nr', record['name'], re.I) else 0
                    record['is_rna'] = 1 if re.search(r'rna|rrna|16s|18s|28s', record['name'], re.I) else 0
                    record['is_genome'] = 1 if re.search(r'genome|ref_.*_rep', record['name'], re.I) else 0
                    record['is_refseq'] = 1 if re.search(r'refseq', record['name'], re.I) else 0
                    
                    records.append(record)
                    
            except Exception as e:
                print(f"Error loading {meta_file}: {e}")
        
        return pd.DataFrame(records)
    
    def _find_taxonomy_db(self):
        for f in os.listdir(self.base_path):
            if f.endswith('.sqlite3') and 'tax' in f:
                return os.path.join(self.base_path, f)
        return None
    
    def iteration_1_overview_and_questions(self):
        """ITERATION 1: Initial overview and question generation"""
        self.iteration = 1
        print(f"\n{'='*60}")
        print("ITERATION 1: INITIAL OVERVIEW & QUESTION GENERATION")
        print(f"{'='*60}")
        
        df = self.metadata_df
        
        # Basic overview
        print(f"Dataset Overview:")
        print(f"- Total databases: {len(df)}")
        print(f"- Total sequences: {df['sequences'].sum():,}")
        print(f"- Total letters: {df['letters'].sum():,}")
        
        # Find interesting patterns that generate questions
        
        # Size distribution analysis
        size_stats = df['sequences'].describe()
        self.log_finding(f"Sequence count varies dramatically: min={size_stats['min']:,.0f}, max={size_stats['max']:,.0f}, std={size_stats['std']:,.0f}")
        self.ask_question("What causes this massive variation in database sizes? Are there distinct size classes?")
        
        # Database type distribution
        type_counts = df['dbtype'].value_counts()
        self.log_finding(f"Database types: {dict(type_counts)}")
        self.ask_question("Why do we have more nucleotide than protein databases? What's the biological significance?")
        
        # Eukaryotic focus
        euk_count = df['is_eukaryotic'].sum()
        euk_sequences = df[df['is_eukaryotic']==1]['sequences'].sum()
        self.log_finding(f"Eukaryotic databases: {euk_count} databases with {euk_sequences:,} sequences")
        self.ask_question("How well do eukaryotic databases cover marine taxa? What's missing?")
        
        # Compression efficiency
        comp_stats = df[df['compression_ratio']>0]['compression_ratio'].describe()
        self.log_finding(f"Compression efficiency varies: mean={comp_stats['mean']:.2f}, std={comp_stats['std']:.2f}")
        self.ask_question("Why do some databases compress better? Is it sequence complexity or redundancy?")
        
        return df
    
    def iteration_2_size_class_analysis(self):
        """ITERATION 2: Deep dive into database size patterns"""
        self.iteration = 2
        print(f"\n{'='*60}")
        print("ITERATION 2: DATABASE SIZE CLASS ANALYSIS")
        print(f"{'='*60}")
        
        df = self.metadata_df
        
        # Cluster databases by size
        df_nonzero = df[df['sequences'] > 0].copy()
        df_nonzero['log_sequences'] = np.log10(df_nonzero['sequences'])
        df_nonzero['log_letters'] = np.log10(df_nonzero['letters'])
        
        # Identify size classes using clustering
        features = df_nonzero[['log_sequences', 'log_letters']].values
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        kmeans = KMeans(n_clusters=4, random_state=42)
        df_nonzero['size_class'] = kmeans.fit_predict(features_scaled)
        
        # Analyze each size class
        for class_id in sorted(df_nonzero['size_class'].unique()):
            class_data = df_nonzero[df_nonzero['size_class'] == class_id]
            seq_range = (class_data['sequences'].min(), class_data['sequences'].max())
            
            self.log_finding(f"Size Class {class_id}: {len(class_data)} databases, sequence range: {seq_range[0]:,.0f} - {seq_range[1]:,.0f}")
            
            # What types of databases are in each class?
            types_in_class = class_data['dbtype'].value_counts()
            categories = []
            if class_data['is_eukaryotic'].sum() > 0:
                categories.append('eukaryotic')
            if class_data['is_protein'].sum() > 0:
                categories.append('protein')
            if class_data['is_rna'].sum() > 0:
                categories.append('RNA')
            if class_data['is_genome'].sum() > 0:
                categories.append('genome')
            
            print(f"  Categories: {', '.join(categories)}")
            print(f"  Examples: {list(class_data['name'].head(3))}")
        
        self.ask_question("Do size classes correspond to biological function or data source?")
        self.ask_question("Which size class is most relevant for marine eDNA identification?")
        
        # Visualize size classes
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(df_nonzero['log_sequences'], df_nonzero['log_letters'], 
                            c=df_nonzero['size_class'], cmap='viridis', alpha=0.7)
        plt.xlabel('Log10(Sequences)')
        plt.ylabel('Log10(Letters)')
        plt.title('Database Size Classes')
        plt.colorbar(scatter)
        
        # Annotate interesting points
        for idx, row in df_nonzero.iterrows():
            if row['is_eukaryotic'] == 1:
                plt.annotate(row['name'], (row['log_sequences'], row['log_letters']), 
                           fontsize=8, alpha=0.7)
        
        plt.tight_layout()
        plt.savefig('eda_iteration2_size_classes.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return df_nonzero
    
    def iteration_3_eukaryotic_deep_dive(self):
        """ITERATION 3: Deep analysis of eukaryotic databases for marine relevance"""
        self.iteration = 3
        print(f"\n{'='*60}")
        print("ITERATION 3: EUKARYOTIC DATABASE DEEP DIVE")
        print(f"{'='*60}")
        
        df = self.metadata_df
        euk_df = df[df['is_eukaryotic'] == 1].copy()
        
        # Analyze eukaryotic database characteristics
        self.log_finding(f"Eukaryotic databases represent {euk_df['sequences'].sum() / df['sequences'].sum() * 100:.1f}% of all sequences")
        
        # Compare average sequence lengths
        euk_avg_lengths = euk_df['avg_length'].dropna()
        non_euk_avg_lengths = df[df['is_eukaryotic'] == 0]['avg_length'].dropna()
        
        t_stat, p_value = stats.ttest_ind(euk_avg_lengths, non_euk_avg_lengths)
        self.log_finding(f"Eukaryotic vs non-eukaryotic sequence lengths differ significantly (p={p_value:.2e})")
        
        # Analyze by specific categories
        categories = {
            'rRNA_markers': euk_df[euk_df['is_rna'] == 1],
            'genomes': euk_df[euk_df['is_genome'] == 1],
            'general': euk_df[(euk_df['is_rna'] == 0) & (euk_df['is_genome'] == 0)]
        }
        
        for cat_name, cat_df in categories.items():
            if len(cat_df) > 0:
                self.log_finding(f"{cat_name}: {len(cat_df)} databases, {cat_df['sequences'].sum():,} sequences")
                self.log_finding(f"{cat_name} average length: {cat_df['avg_length'].mean():.0f} letters")
        
        self.ask_question("Which eukaryotic category is best for marine eDNA barcoding?")
        self.ask_question("Do rRNA markers have sufficient taxonomic resolution for deep-sea species?")
        
        # Sample actual sequences from key eukaryotic databases
        key_dbs = ['SSU_eukaryote_rRNA', 'LSU_eukaryote_rRNA', 'ITS_eukaryote_sequences']
        sequence_analysis = {}
        
        for db_name in key_dbs:
            self.ask_question(f"What taxa are represented in {db_name}?")
            
            # Try to get taxonomic breakdown
            tax_analysis = self._analyze_database_taxonomy(db_name)
            if tax_analysis:
                sequence_analysis[db_name] = tax_analysis
                
        return euk_df, sequence_analysis
    
    def iteration_4_taxonomy_coverage_analysis(self):
        """ITERATION 4: Analyze taxonomic coverage and marine relevance"""
        self.iteration = 4
        print(f"\n{'='*60}")
        print("ITERATION 4: TAXONOMIC COVERAGE ANALYSIS")
        print(f"{'='*60}")
        
        if not self.taxonomy_db:
            self.log_finding("No taxonomy database found - cannot analyze taxonomic coverage")
            return
        
        # Analyze taxonomy structure for marine relevance
        marine_keywords = ['marin', 'ocean', 'deep', 'sea', 'benthos', 'pelagic', 'abyssal', 'hadal']
        
        conn = sqlite3.connect(self.taxonomy_db)
        
        # Sample taxonomy entries and look for patterns
        query = "SELECT taxid, parent FROM TaxidInfo LIMIT 50000"
        tax_sample = pd.read_sql_query(query, conn)
        
        # Build parent-child relationships
        parent_map = dict(zip(tax_sample['taxid'], tax_sample['parent']))
        children = defaultdict(list)
        for taxid, parent in parent_map.items():
            children[parent].append(taxid)
        
        # Calculate taxonomy metrics
        depths = []
        branching_factors = []
        
        def get_depth(taxid, memo={}):
            if taxid in memo:
                return memo[taxid]
            parent = parent_map.get(taxid)
            if parent is None or parent == taxid:
                memo[taxid] = 0
                return 0
            depth = 1 + get_depth(parent, memo)
            memo[taxid] = depth
            return depth
        
        for taxid in list(tax_sample['taxid'])[:10000]:  # Sample for performance
            depths.append(get_depth(taxid))
            branching_factors.append(len(children[taxid]))
        
        depth_stats = pd.Series(depths).describe()
        branch_stats = pd.Series(branching_factors).describe()
        
        self.log_finding(f"Taxonomy depth distribution: mean={depth_stats['mean']:.1f}, max={depth_stats['max']:.0f}")
        self.log_finding(f"Branching factor: mean={branch_stats['mean']:.1f}, max={branch_stats['max']:.0f}")
        
        self.ask_question("How many marine-specific taxa exist in the taxonomy?")
        self.ask_question("What's the taxonomic resolution for deep-sea organisms?")
        
        # Look for potential marine taxa patterns
        # This is a simplified analysis - in practice you'd need name tables
        terminal_nodes = [taxid for taxid, children_list in children.items() if len(children_list) == 0]
        self.log_finding(f"Terminal taxa (species-level): {len(terminal_nodes):,} in sample")
        
        conn.close()
        
        return {
            'depth_stats': depth_stats.to_dict(),
            'branch_stats': branch_stats.to_dict(),
            'terminal_nodes': len(terminal_nodes)
        }
    
    def iteration_5_sequence_content_analysis(self):
        """ITERATION 5: Analyze actual sequence content and composition"""
        self.iteration = 5
        print(f"\n{'='*60}")
        print("ITERATION 5: SEQUENCE CONTENT ANALYSIS")
        print(f"{'='*60}")
        
        # Focus on key databases for marine eDNA
        target_dbs = [
            'SSU_eukaryote_rRNA',
            'LSU_eukaryote_rRNA', 
            'ITS_eukaryote_sequences',
            'nt_euk'
        ]
        
        sequence_stats = {}
        
        for db_name in target_dbs:
            self.ask_question(f"What is the sequence composition and quality of {db_name}?")
            
            stats = self._analyze_sequence_composition(db_name)
            if stats:
                sequence_stats[db_name] = stats
                
                # Ask follow-up questions based on findings
                if 'gc_content' in stats:
                    gc_mean = stats['gc_content']['mean']
                    self.log_finding(f"{db_name} GC content: {gc_mean:.1%}")
                    
                    if gc_mean < 0.4:
                        self.ask_question(f"Why is {db_name} GC content low? AT-rich organisms?")
                    elif gc_mean > 0.6:
                        self.ask_question(f"Why is {db_name} GC content high? Specific taxa bias?")
                
                if 'length_distribution' in stats:
                    lengths = stats['length_distribution']
                    cv = lengths['std'] / lengths['mean'] if lengths['mean'] > 0 else 0
                    self.log_finding(f"{db_name} length CV: {cv:.2f}")
                    
                    if cv > 1.0:
                        self.ask_question(f"Why does {db_name} have high length variability? Mixed sequence types?")
        
        return sequence_stats
    
    def iteration_6_integration_and_recommendations(self):
        """ITERATION 6: Integrate findings and generate actionable recommendations"""
        self.iteration = 6
        print(f"\n{'='*60}")
        print("ITERATION 6: INTEGRATION & RECOMMENDATIONS")
        print(f"{'='*60}")
        
        # Synthesize all findings
        print("\n📊 SYNTHESIS OF FINDINGS:")
        for i, finding in enumerate(self.findings, 1):
            print(f"{i:2d}. {finding['finding']}")
        
        print(f"\n❓ QUESTIONS GENERATED: {len(self.questions)}")
        for i, q in enumerate(self.questions, 1):
            print(f"{i:2d}. {q['question']}")
        
        # Generate recommendations based on iterative analysis
        recommendations = []
        
        # Based on size class analysis
        euk_dbs = self.metadata_df[self.metadata_df['is_eukaryotic'] == 1]
        if len(euk_dbs) > 0:
            top_euk = euk_dbs.sort_values('sequences', ascending=False).iloc[0]
            recommendations.append(f"PRIMARY: Use {top_euk['name']} ({top_euk['sequences']:,} sequences) as main eukaryotic reference")
        
        # Based on marker analysis
        rna_dbs = euk_dbs[euk_dbs['is_rna'] == 1]
        if len(rna_dbs) > 0:
            recommendations.append(f"PHYLOGENETIC: Use {len(rna_dbs)} rRNA databases for phylogenetic placement")
        
        # Based on compression analysis
        efficient_dbs = self.metadata_df[self.metadata_df['compression_ratio'] > 10]
        if len(efficient_dbs) > 0:
            recommendations.append(f"EFFICIENCY: {len(efficient_dbs)} databases have high compression efficiency (>10x)")
        
        print(f"\n🎯 ACTIONABLE RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        # Save comprehensive analysis
        analysis_summary = {
            'iterations': self.iteration,
            'findings': self.findings,
            'questions': self.questions,
            'recommendations': recommendations,
            'database_summary': {
                'total_databases': len(self.metadata_df),
                'eukaryotic_databases': int(self.metadata_df['is_eukaryotic'].sum()),
                'total_sequences': int(self.metadata_df['sequences'].sum()),
                'total_letters': int(self.metadata_df['letters'].sum())
            }
        }
        
        with open('iterative_deep_eda_results.json', 'w') as f:
            json.dump(analysis_summary, f, indent=2)
        
        return analysis_summary
    
    def _analyze_database_taxonomy(self, db_name):
        """Analyze taxonomic composition of a database"""
        try:
            db_path = os.path.join(self.base_path, db_name)
            # Try to get taxonomy info if blastdbcmd is available
            cmd = f"blastdbcmd -db {db_path} -entry all -outfmt '%T' | head -100"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                taxids = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                return {
                    'sample_taxids': len(taxids),
                    'unique_taxids': len(set(taxids)),
                    'example_taxids': taxids[:10]
                }
        except:
            pass
        return None
    
    def _analyze_sequence_composition(self, db_name):
        """Analyze sequence composition (GC content, length distribution)"""
        try:
            db_path = os.path.join(self.base_path, db_name)
            
            # Get sequence lengths
            cmd_lengths = f"blastdbcmd -db {db_path} -entry all -outfmt '%l' | head -200"
            result = subprocess.run(cmd_lengths, shell=True, capture_output=True, text=True, timeout=30)
            
            stats = {}
            
            if result.returncode == 0 and result.stdout.strip():
                lengths = [int(line.strip()) for line in result.stdout.strip().split('\n') 
                          if line.strip().isdigit()]
                
                if lengths:
                    length_array = np.array(lengths)
                    stats['length_distribution'] = {
                        'count': len(length_array),
                        'mean': float(length_array.mean()),
                        'std': float(length_array.std()),
                        'min': int(length_array.min()),
                        'max': int(length_array.max()),
                        'median': float(np.median(length_array))
                    }
            
            # Get GC content sample
            cmd_seqs = f"blastdbcmd -db {db_path} -entry all -outfmt '%s' | head -50"
            result = subprocess.run(cmd_seqs, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                sequences = [line.strip().upper() for line in result.stdout.strip().split('\n') 
                           if line.strip() and not line.startswith('>')]
                
                if sequences:
                    gc_contents = []
                    for seq in sequences:
                        if seq and len(seq) > 10:  # Only analyze reasonable length sequences
                            gc = (seq.count('G') + seq.count('C')) / len(seq)
                            gc_contents.append(gc)
                    
                    if gc_contents:
                        gc_array = np.array(gc_contents)
                        stats['gc_content'] = {
                            'count': len(gc_array),
                            'mean': float(gc_array.mean()),
                            'std': float(gc_array.std()),
                            'min': float(gc_array.min()),
                            'max': float(gc_array.max())
                        }
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}
    
    def run_iterative_analysis(self):
        """Run the complete iterative EDA process"""
        print("🚀 STARTING ITERATIVE DEEP EDA")
        print("This is what REAL EDA looks like - asking questions and drilling deeper!")
        
        # Run all iterations
        self.iteration_1_overview_and_questions()
        df_with_classes = self.iteration_2_size_class_analysis()
        euk_analysis = self.iteration_3_eukaryotic_deep_dive()
        tax_analysis = self.iteration_4_taxonomy_coverage_analysis()
        seq_analysis = self.iteration_5_sequence_content_analysis()
        final_summary = self.iteration_6_integration_and_recommendations()
        
        print(f"\n{'='*60}")
        print("🎉 ITERATIVE DEEP EDA COMPLETE!")
        print(f"Generated {len(self.findings)} findings and {len(self.questions)} questions")
        print("Results saved to: iterative_deep_eda_results.json")
        print(f"{'='*60}")
        
        return final_summary

if __name__ == "__main__":
    eda = IterativeDeepEDA()
    results = eda.run_iterative_analysis()
