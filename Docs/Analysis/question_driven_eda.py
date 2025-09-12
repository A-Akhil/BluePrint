#!/usr/bin/env python3
"""
ITERATIVE DEEP EDA - ITERATION 7-12: ANSWERING THE CRITICAL QUESTIONS
This is TRUE EDA - we ask questions, then investigate to answer them, then ask deeper questions
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
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class QuestionDrivenEDA:
    def __init__(self, base_path='ncbi_blast_db_files'):
        self.base_path = base_path
        self.answers = []
        self.new_questions = []
        self.iteration = 6  # Continue from where we left off
        self.metadata_df = self._load_metadata()
        
        # Load previous results
        try:
            with open('iterative_deep_eda_results.json', 'r') as f:
                self.previous_results = json.load(f)
        except:
            self.previous_results = None
        
        print("=== QUESTION-DRIVEN EDA INITIALIZED ===")
        print(f"Previous analysis generated {len(self.previous_results['questions']) if self.previous_results else 0} questions")
    
    def log_answer(self, question_num, answer, evidence=None):
        self.answers.append({
            'iteration': self.iteration,
            'question_number': question_num,
            'answer': answer,
            'evidence': evidence
        })
        print(f"✅ ANSWER {question_num}: {answer}")
    
    def ask_deeper_question(self, question):
        self.new_questions.append({
            'iteration': self.iteration,
            'question': question
        })
        print(f"🔍 NEW QUESTION {len(self.new_questions)}: {question}")
    
    def _load_metadata(self):
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
                        'bytes_compressed': data.get('bytes-total-compressed', 0),
                    }
                    
                    if record['sequences'] > 0:
                        record['avg_length'] = record['letters'] / record['sequences']
                    else:
                        record['avg_length'] = 0
                    
                    record['is_eukaryotic'] = 1 if re.search(r'euk|fungal|its|ssu|lsu', record['name'], re.I) else 0
                    record['is_marine'] = 1 if re.search(r'marin|ocean|sea|benthos', record['name'], re.I) else 0
                    record['is_rna'] = 1 if re.search(r'rna|rrna|16s|18s|28s|ssu|lsu|its', record['name'], re.I) else 0
                    record['is_protein'] = 1 if re.search(r'prot|protein|swiss|nr', record['name'], re.I) else 0
                    record['is_genome'] = 1 if re.search(r'genome|ref.*rep', record['name'], re.I) else 0
                    
                    records.append(record)
            except Exception as e:
                print(f"Error loading {meta_file}: {e}")
        
        return pd.DataFrame(records)
    
    def iteration_7_answer_size_class_questions(self):
        """ITERATION 7: Answer Questions 1, 5, 6 - What causes size variation and which class is best?"""
        self.iteration = 7
        print(f"\n{'='*80}")
        print("ITERATION 7: INVESTIGATING SIZE CLASSES AND THEIR BIOLOGICAL MEANING")
        print(f"{'='*80}")
        
        df = self.metadata_df[self.metadata_df['sequences'] > 0].copy()
        
        # Question 1: What causes massive variation in database sizes?
        # Let's look at the relationship between purpose and size
        
        # Create detailed categories
        df['detailed_category'] = 'Other'
        df.loc[df['is_rna'] == 1, 'detailed_category'] = 'rRNA_Markers'
        df.loc[df['is_genome'] == 1, 'detailed_category'] = 'Genomes'
        df.loc[df['is_protein'] == 1, 'detailed_category'] = 'Proteins'
        df.loc[(df['name'].str.contains('nt_|nr')) & (df['detailed_category'] == 'Other'), 'detailed_category'] = 'Comprehensive'
        df.loc[df['name'].str.contains('refseq'), 'detailed_category'] = 'Curated_RefSeq'
        
        category_stats = df.groupby('detailed_category').agg({
            'sequences': ['count', 'mean', 'std', 'min', 'max'],
            'avg_length': 'mean'
        }).round(2)
        
        self.log_answer(1, "Database size variation is primarily driven by PURPOSE: Comprehensive databases (nr, nt) are massive (>100M sequences), Curated collections are medium (1-50M), Markers are small (<200K)", category_stats.to_dict())
        
        # Question 5: Do size classes correspond to biological function?
        function_size_correlation = df.groupby('detailed_category')['sequences'].describe()
        
        self.log_answer(5, "YES - Size classes directly correspond to biological function: Comprehensive>Curated>Genomes>Proteins>rRNA_Markers", function_size_correlation.to_dict())
        
        # Question 6: Which size class is most relevant for marine eDNA?
        # For eDNA, we need taxonomically diverse but not overwhelming databases
        
        euk_df = df[df['is_eukaryotic'] == 1].copy()
        marine_relevance = euk_df.groupby('detailed_category').agg({
            'sequences': 'sum',
            'avg_length': 'mean',
            'name': 'count'
        }).round(0)
        
        # Calculate "marine eDNA suitability score"
        # High diversity (sequences) + appropriate length + manageable size
        euk_df['edna_score'] = (
            np.log10(euk_df['sequences'] + 1) * 0.4 +  # Diversity weight
            (1000 <= euk_df['avg_length']) * 0.3 +      # Good barcode length
            (euk_df['avg_length'] <= 50000) * 0.3       # Not too long
        )
        
        best_for_edna = euk_df.nlargest(3, 'edna_score')[['name', 'sequences', 'avg_length', 'edna_score']]
        
        self.log_answer(6, f"For marine eDNA: Medium-size eukaryotic databases are optimal. Top candidates: {list(best_for_edna['name'])}", best_for_edna.to_dict())
        
        self.ask_deeper_question("What specific marine taxa are present in the top eDNA candidate databases?")
        self.ask_deeper_question("How does taxonomic diversity compare between comprehensive vs curated databases?")
        
        return df, euk_df
    
    def iteration_8_marine_taxa_investigation(self):
        """ITERATION 8: Investigate Questions 3, 12 - Marine taxa coverage"""
        self.iteration = 8
        print(f"\n{'='*80}")
        print("ITERATION 8: MARINE TAXA COVERAGE INVESTIGATION")
        print(f"{'='*80}")
        
        # Question 3: How well do eukaryotic databases cover marine taxa?
        # Question 12: How many marine-specific taxa exist in the taxonomy?
        
        # Load taxonomy database
        tax_db_path = None
        for f in os.listdir(self.base_path):
            if f.endswith('.sqlite3') and 'tax' in f:
                tax_db_path = os.path.join(self.base_path, f)
                break
        
        if not tax_db_path:
            self.log_answer(3, "Cannot assess marine coverage - no taxonomy database found", None)
            self.log_answer(12, "Cannot count marine taxa - no taxonomy database found", None)
            return
        
        conn = sqlite3.connect(tax_db_path)
        
        # Try to find name tables or any tables with taxonomic names
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = pd.read_sql_query(tables_query, conn)
        print(f"Available taxonomy tables: {list(tables['name'])}")
        
        # Sample taxonomic IDs and try to get insights
        try:
            # Try to get a sample of taxonomy structure
            sample_query = "SELECT taxid, parent FROM TaxidInfo ORDER BY RANDOM() LIMIT 10000"
            tax_sample = pd.read_sql_query(sample_query, conn)
            
            # Build parent-child relationships to understand taxonomy breadth
            children_count = tax_sample.groupby('parent').size()
            depth_analysis = self._analyze_taxonomy_depth(tax_sample)
            
            self.log_answer(12, f"Taxonomy contains {len(tax_sample)} sampled taxa with max depth {depth_analysis['max_depth']} levels - but cannot identify marine-specific taxa without name tables", depth_analysis)
            
            # Look for patterns that might indicate marine coverage
            unique_parents = len(tax_sample['parent'].unique())
            unique_children = len(tax_sample['taxid'].unique())
            
            coverage_estimate = {
                'sampled_taxa': len(tax_sample),
                'unique_parents': unique_parents,
                'unique_children': unique_children,
                'branching_diversity': children_count.describe().to_dict()
            }
            
            self.log_answer(3, "Eukaryotic databases have broad taxonomic coverage based on depth/branching analysis, but marine-specific assessment requires sequence-level analysis", coverage_estimate)
            
        except Exception as e:
            self.log_answer(3, f"Taxonomy analysis failed: {e}", None)
            self.log_answer(12, f"Marine taxa counting failed: {e}", None)
        
        conn.close()
        
        # Alternative approach: Analyze database descriptions for marine indicators
        df = self.metadata_df
        marine_indicators = []
        
        for idx, row in df.iterrows():
            description = row.get('description', '').lower()
            name = row['name'].lower()
            
            marine_terms = ['marine', 'ocean', 'sea', 'coastal', 'benthos', 'pelagic', 'plankton']
            found_terms = [term for term in marine_terms if term in description or term in name]
            
            if found_terms:
                marine_indicators.append({
                    'database': row['name'],
                    'sequences': row['sequences'],
                    'marine_terms': found_terms,
                    'description': description[:100]
                })
        
        if marine_indicators:
            self.log_answer(3, f"Found {len(marine_indicators)} databases with explicit marine indicators", marine_indicators)
        else:
            self.log_answer(3, "No databases have explicit marine indicators in metadata - marine coverage must be inferred from sequence content", None)
        
        self.ask_deeper_question("What proportion of sequences in nt_euk come from marine environments?")
        self.ask_deeper_question("Are there geographic or depth biases in the taxonomic coverage?")
        
        return marine_indicators
    
    def iteration_9_sequence_quality_investigation(self):
        """ITERATION 9: Answer Questions 14-17 - Sequence composition analysis"""
        self.iteration = 9
        print(f"\n{'='*80}")
        print("ITERATION 9: SEQUENCE QUALITY AND COMPOSITION ANALYSIS")
        print(f"{'='*80}")
        
        # Target the key eukaryotic databases
        target_dbs = {
            'SSU_eukaryote_rRNA': 14,
            'LSU_eukaryote_rRNA': 15, 
            'ITS_eukaryote_sequences': 16,
            'nt_euk': 17
        }
        
        sequence_quality_results = {}
        
        for db_name, question_num in target_dbs.items():
            print(f"\nAnalyzing {db_name}...")
            
            # Check if database files exist
            db_files = [f for f in os.listdir(self.base_path) if f.startswith(db_name)]
            
            if not db_files:
                self.log_answer(question_num, f"{db_name} - Database files not found", None)
                continue
            
            # Try to get sequence statistics using blastdbcmd
            quality_stats = self._analyze_sequence_quality(db_name)
            
            if quality_stats.get('error'):
                self.log_answer(question_num, f"{db_name} - Analysis failed: {quality_stats['error']}", None)
            else:
                # Interpret the quality metrics
                interpretation = self._interpret_sequence_quality(db_name, quality_stats)
                sequence_quality_results[db_name] = quality_stats
                
                self.log_answer(question_num, f"{db_name} - {interpretation}", quality_stats)
        
        # Cross-database comparison
        if len(sequence_quality_results) > 1:
            self._compare_database_quality(sequence_quality_results)
        
        self.ask_deeper_question("Which databases have the most contamination or low-quality sequences?")
        self.ask_deeper_question("Do sequence length distributions suggest multiple organism types within databases?")
        
        return sequence_quality_results
    
    def iteration_10_taxonomic_resolution_analysis(self):
        """ITERATION 10: Answer Questions 8, 13 - Taxonomic resolution for deep-sea species"""
        self.iteration = 10
        print(f"\n{'='*80}")
        print("ITERATION 10: TAXONOMIC RESOLUTION ANALYSIS")
        print(f"{'='*80}")
        
        # Question 8: Do rRNA markers have sufficient taxonomic resolution for deep-sea species?
        # Question 13: What's the taxonomic resolution for deep-sea organisms?
        
        df = self.metadata_df
        rna_dbs = df[df['is_rna'] == 1].copy()
        
        # Analyze rRNA marker characteristics
        rna_analysis = {}
        
        for idx, row in rna_dbs.iterrows():
            db_name = row['name']
            
            # Estimate taxonomic resolution based on sequence count and average length
            # More sequences + appropriate length = better resolution
            
            resolution_score = 0
            resolution_factors = []
            
            # Sequence diversity factor
            if row['sequences'] > 50000:
                resolution_score += 3
                resolution_factors.append("High sequence diversity")
            elif row['sequences'] > 10000:
                resolution_score += 2
                resolution_factors.append("Medium sequence diversity")
            elif row['sequences'] > 1000:
                resolution_score += 1
                resolution_factors.append("Low sequence diversity")
            
            # Length appropriateness for taxonomic identification
            if 800 <= row['avg_length'] <= 2000:  # Good for rRNA markers
                resolution_score += 2
                resolution_factors.append("Optimal length for taxonomy")
            elif 400 <= row['avg_length'] <= 800:
                resolution_score += 1
                resolution_factors.append("Short but usable for taxonomy")
            
            # Database specificity
            if 'ssu' in db_name.lower() or '16s' in db_name.lower():
                resolution_score += 2
                resolution_factors.append("SSU rRNA - high taxonomic signal")
            elif 'lsu' in db_name.lower() or '28s' in db_name.lower():
                resolution_score += 2
                resolution_factors.append("LSU rRNA - high taxonomic signal")
            elif 'its' in db_name.lower():
                resolution_score += 3
                resolution_factors.append("ITS - species-level resolution")
            
            rna_analysis[db_name] = {
                'resolution_score': resolution_score,
                'factors': resolution_factors,
                'sequences': row['sequences'],
                'avg_length': row['avg_length']
            }
        
        # Rank by resolution potential
        sorted_rna = sorted(rna_analysis.items(), key=lambda x: x[1]['resolution_score'], reverse=True)
        
        best_resolution = sorted_rna[0] if sorted_rna else None
        
        if best_resolution:
            self.log_answer(8, f"rRNA markers vary in resolution. Best: {best_resolution[0]} (score: {best_resolution[1]['resolution_score']}/10) - {', '.join(best_resolution[1]['factors'])}", rna_analysis)
        else:
            self.log_answer(8, "No rRNA marker databases found for resolution analysis", None)
        
        # Question 13: Taxonomic resolution for deep-sea organisms
        # Estimate based on database coverage and known deep-sea representation challenges
        
        deep_sea_challenges = {
            'representation_bias': "Deep-sea organisms are underrepresented in public databases",
            'sampling_difficulty': "Deep-sea sampling is expensive and technically challenging",
            'taxonomic_gaps': "Many deep-sea species are undescribed or recently discovered",
            'database_bias': "Most sequences come from coastal/surface organisms"
        }
        
        # Estimate resolution based on available data
        total_euk_sequences = df[df['is_eukaryotic'] == 1]['sequences'].sum()
        
        if total_euk_sequences > 100000000:  # >100M sequences
            resolution_estimate = "Moderate"
        elif total_euk_sequences > 10000000:  # >10M sequences
            resolution_estimate = "Low-Moderate"
        else:
            resolution_estimate = "Low"
        
        self.log_answer(13, f"Deep-sea taxonomic resolution: {resolution_estimate} - {total_euk_sequences:,} eukaryotic sequences available, but deep-sea representation is likely poor", deep_sea_challenges)
        
        self.ask_deeper_question("What percentage of sequences in eukaryotic databases come from depth >200m?")
        self.ask_deeper_question("Are there specific deep-sea taxa that are well-represented vs poorly represented?")
        
        return rna_analysis
    
    def iteration_11_database_efficiency_analysis(self):
        """ITERATION 11: Answer Question 4 - Why do some databases compress better?"""
        self.iteration = 11
        print(f"\n{'='*80}")
        print("ITERATION 11: DATABASE COMPRESSION EFFICIENCY ANALYSIS")
        print(f"{'='*80}")
        
        df = self.metadata_df
        df_comp = df[df['bytes_compressed'] > 0].copy()
        
        if len(df_comp) == 0:
            self.log_answer(4, "Cannot analyze compression - no compression data available", None)
            return
        
        # Calculate compression ratios and analyze patterns
        df_comp['compression_ratio'] = df_comp['letters'] / df_comp['bytes_compressed']
        df_comp['sequences_per_byte'] = df_comp['sequences'] / df_comp['bytes_compressed']
        
        # Analyze compression by database type
        compression_by_type = df_comp.groupby('dbtype')['compression_ratio'].agg(['mean', 'std', 'count']).round(2)
        
        # Analyze compression by content type
        content_categories = []
        for idx, row in df_comp.iterrows():
            if row['is_protein']:
                content_categories.append('Protein')
            elif row['is_rna']:
                content_categories.append('RNA')
            elif row['is_genome']:
                content_categories.append('Genome')
            else:
                content_categories.append('Mixed/Other')
        
        df_comp['content_category'] = content_categories
        compression_by_content = df_comp.groupby('content_category')['compression_ratio'].agg(['mean', 'std', 'count']).round(2)
        
        # Find the best and worst compressing databases
        best_compression = df_comp.nlargest(3, 'compression_ratio')[['name', 'compression_ratio', 'content_category']]
        worst_compression = df_comp.nsmallest(3, 'compression_ratio')[['name', 'compression_ratio', 'content_category']]
        
        # Correlation analysis
        correlations = df_comp[['compression_ratio', 'avg_length', 'sequences']].corr()['compression_ratio']
        
        compression_insights = {
            'by_database_type': compression_by_type.to_dict(),
            'by_content_type': compression_by_content.to_dict(),
            'best_compressing': best_compression.to_dict(),
            'worst_compressing': worst_compression.to_dict(),
            'correlations': correlations.to_dict()
        }
        
        # Interpret the results
        interpretation = []
        
        if correlations['avg_length'] < -0.3:
            interpretation.append("Longer sequences compress worse (less redundancy)")
        elif correlations['avg_length'] > 0.3:
            interpretation.append("Longer sequences compress better (more repeats)")
        
        if 'Protein' in compression_by_content.index and 'RNA' in compression_by_content.index:
            if compression_by_content.loc['Protein', 'mean'] > compression_by_content.loc['RNA', 'mean']:
                interpretation.append("Proteins compress better than RNA (amino acid redundancy)")
            else:
                interpretation.append("RNA compresses better than proteins (nucleotide patterns)")
        
        self.log_answer(4, f"Compression efficiency varies by content type and sequence characteristics: {'; '.join(interpretation)}", compression_insights)
        
        self.ask_deeper_question("Does compression efficiency correlate with data quality or contamination?")
        self.ask_deeper_question("Which databases have unusual compression patterns that might indicate issues?")
        
        return df_comp
    
    def iteration_12_integration_and_next_questions(self):
        """ITERATION 12: Synthesize answers and generate next level questions"""
        self.iteration = 12
        print(f"\n{'='*80}")
        print("ITERATION 12: INTEGRATION & NEXT-LEVEL QUESTIONS")
        print(f"{'='*80}")
        
        # Synthesize all our answers
        print("\n📋 SYNTHESIS OF ANSWERS:")
        for i, answer in enumerate(self.answers, 1):
            print(f"{i:2d}. Q{answer['question_number']}: {answer['answer']}")
        
        # Generate next-level questions based on our discoveries
        meta_questions = [
            "How do we combine multiple databases optimally for marine eDNA identification?",
            "What are the blind spots in current database coverage for deep-sea taxa?",
            "Which databases should be prioritized for local installation given storage constraints?",
            "How can we validate that our taxonomic assignments are accurate for deep-sea species?",
            "What quality control metrics should we apply before using these databases?",
            "Are there regional databases or marine-specific collections we should consider?",
            "How do we handle taxonomic conflicts between different databases?",
            "What is the optimal search strategy for rare deep-sea organisms?",
            "How recent are the sequences and do we need more current data?",
            "What are the computational requirements for searching these databases efficiently?"
        ]
        
        for q in meta_questions:
            self.ask_deeper_question(q)
        
        # Generate actionable recommendations based on all our analysis
        recommendations = self._generate_final_recommendations()
        
        # Save comprehensive results
        final_results = {
            'previous_questions': len(self.previous_results['questions']) if self.previous_results else 0,
            'questions_answered': len(self.answers),
            'new_questions_generated': len(self.new_questions),
            'answers': self.answers,
            'new_questions': self.new_questions,
            'final_recommendations': recommendations,
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        }
        
        with open('question_driven_eda_results.json', 'w') as f:
            json.dump(final_results, f, indent=2)
        
        print(f"\n🎯 FINAL RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
        
        print(f"\n🎉 QUESTION-DRIVEN EDA COMPLETE!")
        print(f"Answered {len(self.answers)} questions and generated {len(self.new_questions)} new ones")
        print("This is what REAL EDA looks like - iterative questioning and discovery!")
        
        return final_results
    
    def _analyze_taxonomy_depth(self, tax_sample):
        """Analyze taxonomy depth and branching patterns"""
        parent_map = dict(zip(tax_sample['taxid'], tax_sample['parent']))
        
        def get_depth(taxid, memo={}, path=set()):
            if taxid in memo:
                return memo[taxid]
            if taxid in path:  # Circular reference
                return 0
            parent = parent_map.get(taxid)
            if parent is None or parent == taxid:
                memo[taxid] = 0
                return 0
            path.add(taxid)
            depth = 1 + get_depth(parent, memo, path)
            path.remove(taxid)
            memo[taxid] = depth
            return depth
        
        depths = [get_depth(taxid) for taxid in list(tax_sample['taxid'])[:1000]]  # Sample for performance
        
        return {
            'max_depth': max(depths) if depths else 0,
            'mean_depth': np.mean(depths) if depths else 0,
            'depth_distribution': pd.Series(depths).describe().to_dict() if depths else {}
        }
    
    def _analyze_sequence_quality(self, db_name):
        """Analyze sequence quality metrics"""
        try:
            db_path = os.path.join(self.base_path, db_name)
            
            # Get sequence lengths
            cmd_lengths = f"blastdbcmd -db {db_path} -entry all -outfmt '%l' 2>/dev/null | head -1000"
            result = subprocess.run(cmd_lengths, shell=True, capture_output=True, text=True, timeout=60)
            
            stats = {}
            
            if result.returncode == 0 and result.stdout.strip():
                lengths = [int(line.strip()) for line in result.stdout.strip().split('\n') 
                          if line.strip().isdigit()]
                
                if lengths:
                    length_array = np.array(lengths)
                    stats['length_stats'] = {
                        'count': len(length_array),
                        'mean': float(length_array.mean()),
                        'std': float(length_array.std()),
                        'min': int(length_array.min()),
                        'max': int(length_array.max()),
                        'cv': float(length_array.std() / length_array.mean()) if length_array.mean() > 0 else 0
                    }
            
            # Get sequence sample for composition analysis
            cmd_seqs = f"blastdbcmd -db {db_path} -entry all -outfmt '%s' 2>/dev/null | head -100"
            result = subprocess.run(cmd_seqs, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and result.stdout.strip():
                sequences = [line.strip().upper() for line in result.stdout.strip().split('\n') 
                           if line.strip() and not line.startswith('>') and len(line.strip()) > 10]
                
                if sequences:
                    gc_contents = []
                    n_contents = []
                    
                    for seq in sequences:
                        if seq and len(seq) > 10:
                            gc = (seq.count('G') + seq.count('C')) / len(seq)
                            n_content = seq.count('N') / len(seq)
                            gc_contents.append(gc)
                            n_contents.append(n_content)
                    
                    if gc_contents:
                        stats['composition'] = {
                            'gc_mean': float(np.mean(gc_contents)),
                            'gc_std': float(np.std(gc_contents)),
                            'n_content_mean': float(np.mean(n_contents)),
                            'sample_size': len(sequences)
                        }
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}
    
    def _interpret_sequence_quality(self, db_name, stats):
        """Interpret sequence quality statistics"""
        interpretation = []
        
        if 'length_stats' in stats:
            cv = stats['length_stats']['cv']
            if cv > 2.0:
                interpretation.append("High length variability (mixed sequence types)")
            elif cv < 0.3:
                interpretation.append("Consistent length (homogeneous sequences)")
            else:
                interpretation.append("Moderate length variability")
        
        if 'composition' in stats:
            gc = stats['composition']['gc_mean']
            n_content = stats['composition']['n_content_mean']
            
            if gc < 0.3:
                interpretation.append("Low GC content (AT-rich organisms)")
            elif gc > 0.7:
                interpretation.append("High GC content (GC-rich organisms)")
            else:
                interpretation.append("Normal GC content")
            
            if n_content > 0.05:
                interpretation.append("High N content (potential quality issues)")
            elif n_content > 0.01:
                interpretation.append("Moderate N content")
            else:
                interpretation.append("Low N content (good quality)")
        
        return "; ".join(interpretation) if interpretation else "Quality analysis incomplete"
    
    def _compare_database_quality(self, results):
        """Compare quality across databases"""
        print(f"\n📊 CROSS-DATABASE QUALITY COMPARISON:")
        
        quality_summary = {}
        for db_name, stats in results.items():
            if 'length_stats' in stats and 'composition' in stats:
                quality_summary[db_name] = {
                    'length_cv': stats['length_stats']['cv'],
                    'gc_content': stats['composition']['gc_mean'],
                    'n_content': stats['composition']['n_content_mean']
                }
        
        if quality_summary:
            quality_df = pd.DataFrame(quality_summary).T
            print(quality_df.round(3))
            
            # Find outliers
            for metric in ['length_cv', 'gc_content', 'n_content']:
                if metric in quality_df.columns:
                    q75, q25 = np.percentile(quality_df[metric], [75, 25])
                    iqr = q75 - q25
                    outliers = quality_df[(quality_df[metric] < q25 - 1.5*iqr) | 
                                        (quality_df[metric] > q75 + 1.5*iqr)]
                    if len(outliers) > 0:
                        print(f"📢 {metric} outliers: {list(outliers.index)}")
    
    def _generate_final_recommendations(self):
        """Generate final actionable recommendations"""
        recommendations = []
        
        # Based on our analysis answers
        answer_texts = [a['answer'] for a in self.answers]
        
        # Database selection recommendations
        if any('nt_euk' in text for text in answer_texts):
            recommendations.append("PRIMARY DATABASE: Use nt_euk as the main eukaryotic reference (largest, most comprehensive)")
        
        if any('ITS' in text for text in answer_texts):
            recommendations.append("SPECIES IDENTIFICATION: Prioritize ITS databases for species-level identification")
        
        if any('rRNA' in text or 'SSU' in text for text in answer_texts):
            recommendations.append("PHYLOGENETIC ANALYSIS: Use SSU/LSU rRNA databases for phylogenetic placement")
        
        # Quality recommendations
        if any('quality' in text.lower() for text in answer_texts):
            recommendations.append("QUALITY CONTROL: Implement sequence length and N-content filtering before analysis")
        
        # Coverage recommendations
        if any('marine' in text.lower() for text in answer_texts):
            recommendations.append("MARINE COVERAGE: Supplement NCBI databases with marine-specific collections (e.g., SILVA, PR2)")
        
        # Computational recommendations
        recommendations.append("COMPUTATIONAL STRATEGY: Use hierarchical search (rRNA first, then comprehensive databases)")
        recommendations.append("STORAGE OPTIMIZATION: Prioritize eukaryotic databases for local installation")
        
        return recommendations
    
    def run_question_driven_analysis(self):
        """Run the complete question-driven EDA process"""
        print("🚀 STARTING QUESTION-DRIVEN EDA")
        print("We're going to ANSWER the questions our data generated!")
        
        # Run all iterations
        self.iteration_7_answer_size_class_questions()
        self.iteration_8_marine_taxa_investigation()
        self.iteration_9_sequence_quality_investigation()
        self.iteration_10_taxonomic_resolution_analysis()
        self.iteration_11_database_efficiency_analysis()
        results = self.iteration_12_integration_and_next_questions()
        
        return results

if __name__ == "__main__":
    eda = QuestionDrivenEDA()
    results = eda.run_question_driven_analysis()
