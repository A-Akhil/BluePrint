#!/usr/bin/env python3
"""
PROPER STATISTICAL EDA FOR NCBI BLAST DATABASES
Focus: Content analysis, patterns, distributions, statistical insights
NOT file sizes - actual data exploration
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict, Counter
import sqlite3
import subprocess
import warnings
warnings.filterwarnings('ignore')

# Set style for proper statistical visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

class ProperEDAAnalyzer:
    def __init__(self, data_dir="/home/srmist32/sihdna/ncbi_blast_db_files"):
        self.data_dir = Path(data_dir)
        self.results = {}
        self.database_stats = {}
        
    def analyze_taxonomy_distribution(self):
        """Analyze taxonomic distribution from taxonomy databases"""
        print("=== TAXONOMIC DISTRIBUTION ANALYSIS ===")
        
        # Find taxonomy database
        tax_db = self.data_dir / "taxonomy4blast.sqlite3"
        
        if not tax_db.exists():
            print("Warning: taxonomy4blast.sqlite3 not found")
            return None
            
        try:
            # Connect to taxonomy database
            conn = sqlite3.connect(str(tax_db))
            
            # Get table structure
            tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
            print(f"Available tables: {list(tables['name'])}")
            
            # Try to get taxonomic data
            if 'taxid_info' in tables['name'].values:
                tax_data = pd.read_sql_query("SELECT * FROM taxid_info LIMIT 1000;", conn)
                print(f"Taxonomy data shape: {tax_data.shape}")
                print(f"Columns: {list(tax_data.columns)}")
                
                # Analyze taxonomic ranks
                if 'rank' in tax_data.columns:
                    rank_dist = tax_data['rank'].value_counts()
                    print("\nTaxonomic rank distribution:")
                    print(rank_dist.head(10))
                    
                    # Visualize rank distribution
                    plt.figure(figsize=(12, 6))
                    rank_dist.head(15).plot(kind='bar')
                    plt.title('Distribution of Taxonomic Ranks')
                    plt.xlabel('Taxonomic Rank')
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.savefig('taxonomic_ranks_distribution.png', dpi=300)
                    plt.show()
                    
            conn.close()
            
        except Exception as e:
            print(f"Error analyzing taxonomy database: {e}")
            
        return tax_data if 'tax_data' in locals() else None
    
    def analyze_sequence_metadata(self):
        """Analyze sequence metadata from JSON files"""
        print("\n=== SEQUENCE METADATA ANALYSIS ===")
        
        json_files = list(self.data_dir.glob("*.json"))
        print(f"Found {len(json_files)} metadata files")
        
        all_metadata = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    metadata = json.load(f)
                    
                # Extract database info
                db_info = {
                    'database_name': json_file.stem.replace('-nucl-metadata', '').replace('-prot-metadata', ''),
                    'file_name': json_file.name
                }
                
                # Extract key statistics from JSON structure
                db_info.update({
                    'sequences': metadata.get('number-of-sequences', 0),
                    'letters': metadata.get('number-of-letters', 0),
                    'avg_length': metadata.get('number-of-letters', 0) / max(metadata.get('number-of-sequences', 1), 1),
                    'last_updated': metadata.get('last-updated', 'Unknown'),
                    'dbtype': metadata.get('dbtype', 'Unknown'),
                    'description': metadata.get('description', 'No description'),
                    'volumes': metadata.get('number-of-volumes', 1),
                    'total_bytes': metadata.get('bytes-total', 0)
                })
                
                all_metadata.append(db_info)
                
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
        
        if all_metadata:
            metadata_df = pd.DataFrame(all_metadata)
            
            # Clean data
            metadata_df = metadata_df[metadata_df['sequences'] > 0]
            
            print(f"\nMetadata analysis for {len(metadata_df)} databases:")
            print(f"Total sequences: {metadata_df['sequences'].sum():,}")
            print(f"Total nucleotides/amino acids: {metadata_df['letters'].sum():,}")
            
            # Statistical analysis
            print(f"\nSequence count statistics:")
            print(metadata_df['sequences'].describe())
            
            print(f"\nAverage sequence length statistics:")
            print(metadata_df['avg_length'].describe())
            
            # Visualizations
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # 1. Database sequence counts
            metadata_df.set_index('database_name')['sequences'].plot(kind='bar', ax=ax1)
            ax1.set_title('Number of Sequences per Database')
            ax1.set_ylabel('Sequence Count')
            ax1.tick_params(axis='x', rotation=45)
            
            # 2. Distribution of sequence counts
            ax2.hist(metadata_df['sequences'], bins=20, alpha=0.7)
            ax2.set_title('Distribution of Sequence Counts')
            ax2.set_xlabel('Number of Sequences')
            ax2.set_ylabel('Frequency')
            
            # 3. Average sequence length by database
            metadata_df.set_index('database_name')['avg_length'].plot(kind='bar', ax=ax3)
            ax3.set_title('Average Sequence Length per Database')
            ax3.set_ylabel('Average Length (bp/aa)')
            ax3.tick_params(axis='x', rotation=45)
            
            # 4. Sequence length distribution
            ax4.hist(metadata_df['avg_length'], bins=20, alpha=0.7)
            ax4.set_title('Distribution of Average Sequence Lengths')
            ax4.set_xlabel('Average Sequence Length')
            ax4.set_ylabel('Frequency')
            
            plt.tight_layout()
            plt.savefig('sequence_metadata_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # Correlation analysis
            if len(metadata_df) > 2:
                print("\nCorrelation analysis:")
                numeric_cols = ['sequences', 'letters', 'avg_length']
                correlation_matrix = metadata_df[numeric_cols].corr()
                print(correlation_matrix)
                
                # Correlation heatmap
                plt.figure(figsize=(8, 6))
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
                plt.title('Correlation Matrix: Database Characteristics')
                plt.tight_layout()
                plt.savefig('database_correlation_matrix.png', dpi=300)
                plt.show()
            
            return metadata_df
        
        return None
    
    def analyze_database_patterns(self):
        """Analyze database naming patterns and organizational structure"""
        print("\n=== DATABASE PATTERN ANALYSIS ===")
        
        # Get all database files
        all_files = [f.name for f in self.data_dir.glob("*") if f.is_file()]
        
        # Extract patterns
        patterns = {
            'nucleotide_types': [],
            'protein_types': [],
            'taxonomic_groups': [],
            'data_sources': [],
            'version_patterns': []
        }
        
        # Analyze naming conventions
        for filename in all_files:
            base_name = filename.split('.')[0]
            
            # Nucleotide databases
            if any(ext in filename for ext in ['.nhr', '.nin', '.nsq']):
                patterns['nucleotide_types'].append(base_name)
                
            # Protein databases  
            elif any(ext in filename for ext in ['.phr', '.pin', '.psq']):
                patterns['protein_types'].append(base_name)
                
            # Taxonomic indicators
            if any(tax in base_name.lower() for tax in ['euk', 'prok', 'virus', 'fungal', 'bacterial']):
                patterns['taxonomic_groups'].append(base_name)
                
            # Data sources
            if any(source in base_name.lower() for source in ['refseq', 'swissprot', 'pdb', 'tsa']):
                patterns['data_sources'].append(base_name)
        
        # Remove duplicates and analyze
        for pattern_type, items in patterns.items():
            patterns[pattern_type] = list(set(items))
        
        print("Database pattern analysis:")
        for pattern_type, items in patterns.items():
            print(f"  {pattern_type}: {len(items)} unique patterns")
            if items:
                print(f"    Examples: {items[:5]}")
        
        # Visualize patterns
        pattern_counts = {k: len(v) for k, v in patterns.items()}
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(pattern_counts.keys(), pattern_counts.values())
        plt.title('Database Organization Patterns')
        plt.xlabel('Pattern Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('database_patterns.png', dpi=300)
        plt.show()
        
        return patterns
    
    def analyze_eukaryotic_content(self):
        """Analyze eukaryotic content in the databases"""
        print("\n=== EUKARYOTIC CONTENT ANALYSIS ===")
        
        euk_metadata = []
        for f in self.metadata_files:
            if 'euk' in f.lower() or 'eukaryot' in f.lower():
                euk_metadata.append(f)
        
        print(f"Found {len(euk_metadata)} eukaryotic database files")
        
        if not euk_metadata:
            return {"message": "No eukaryotic databases found"}
        
        # Analyze eukaryotic databases
        euk_data = []
        for f in euk_metadata[:5]:  # Limit to first 5 for performance
            try:
                full_path = os.path.join(self.base_path, f)
                with open(full_path, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, dict):
                        euk_data.append(data)
            except Exception as e:
                continue
        
        if euk_data:
            euk_df = pd.DataFrame(euk_data)
            print("\nEukaryotic database statistics:")
            print(euk_df.head())
            
            # Create visualization
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Eukaryotic Database Analysis', fontsize=16)
            
            # Distribution plots if we have numeric data
            numeric_cols = euk_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                for i, col in enumerate(numeric_cols[:4]):
                    row, col_idx = i // 2, i % 2
                    if i < 4:
                        euk_df[col].hist(bins=20, ax=axes[row, col_idx])
                        axes[row, col_idx].set_title(f'{col} Distribution')
                        axes[row, col_idx].set_xlabel(col)
                        axes[row, col_idx].set_ylabel('Frequency')
            
            plt.tight_layout()
            plt.savefig('eukaryotic_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            return {"eukaryotic_databases": len(euk_metadata), "analysis_data": euk_df.to_dict()}
        
        return {"message": "No valid eukaryotic data found"}
                euk_metadata.append(f)
        
        print(f"Found {len(euk_metadata)} eukaryotic database files")
        
        if not euk_metadata:
            return {"message": "No eukaryotic databases found"}
        
        # Analyze eukaryotic databases
        euk_data = []
        for f in euk_metadata[:5]:  # Limit to first 5 for performance
            try:
                full_path = os.path.join(self.base_path, f)
                with open(full_path, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, dict):
                        euk_data.append(data)
            except Exception as e:
                continue
        
        if euk_data:
            euk_df = pd.DataFrame(euk_data)
            print("\nEukaryotic database statistics:")
            print(euk_df.head())
            
            # Create visualization
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Eukaryotic Database Analysis', fontsize=16)
            
            # Distribution plots if we have numeric data
            numeric_cols = euk_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                for i, col in enumerate(numeric_cols[:4]):
                    row, col_idx = i // 2, i % 2
                    if i < 4:
                        euk_df[col].hist(bins=20, ax=axes[row, col_idx])
                        axes[row, col_idx].set_title(f'{col} Distribution')
                        axes[row, col_idx].set_xlabel(col)
                        axes[row, col_idx].set_ylabel('Frequency')
            
            plt.tight_layout()
            plt.savefig('eukaryotic_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            return {"eukaryotic_databases": len(euk_metadata), "analysis_data": euk_df.to_dict()}
        
        return {"message": "No valid eukaryotic data found"}
        
        # Find eukaryotic databases
        euk_databases = []
        for f in self.data_dir.glob("*"):
            if 'euk' in f.name.lower() and f.is_file():
                euk_databases.append(f.name)
        
        print(f"Found {len(euk_databases)} eukaryotic database files")
        
        # Analyze metadata for eukaryotic databases
        euk_metadata = []
        for json_file in self.data_dir.glob("*euk*.json"):
            try:
                with open(json_file, 'r') as f:
                    metadata = json.load(f)
                    
                db_name = json_file.stem.replace('-nucl-metadata', '').replace('-prot-metadata', '')
                
                euk_info = {
                    'database': db_name,
                    'sequences': metadata.get('number-of-sequences', 0),
                    'total_length': metadata.get('number-of-letters', 0),
                    'avg_length': metadata.get('number-of-letters', 0) / max(metadata.get('number-of-sequences', 1), 1),
                    'dbtype': metadata.get('dbtype', 'Unknown'),
                    'description': metadata.get('description', 'No description')
                }
                euk_metadata.append(euk_info)
                    
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
        
        if euk_metadata:
            euk_df = pd.DataFrame(euk_metadata)
            
            print("\nEukaryotic database statistics:")
            print(euk_df)
            
            # Visualize eukaryotic content
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Sequence counts
            euk_df.set_index('database')['sequences'].plot(kind='bar', ax=ax1, color='darkgreen')
            ax1.set_title('Eukaryotic Database Sequence Counts')
            ax1.set_ylabel('Number of Sequences')
            ax1.tick_params(axis='x', rotation=45)
            
            # Average lengths
            euk_df.set_index('database')['avg_length'].plot(kind='bar', ax=ax2, color='darkblue')
            ax2.set_title('Average Sequence Lengths in Eukaryotic Databases')
            ax2.set_ylabel('Average Length (bp)')
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('eukaryotic_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            return euk_df
        
        return None
    
    def analyze_actual_sequences(self):
        """Analyze actual sequence content from BLAST databases"""
        print("\n=== ACTUAL SEQUENCE CONTENT ANALYSIS ===")
        
        # Try to extract sequence information using blastdbcmd
        sequence_analysis = {}
        
        # Look for key databases
        key_databases = ['16S_ribosomal_RNA', '18S_fungal_sequences', '28S_fungal_sequences']
        
        for db_name in key_databases:
            db_path = self.data_dir / db_name
            if any((self.data_dir / f"{db_name}.nhr").exists() for _ in [1]):
                try:
                    print(f"Analyzing sequences in {db_name}...")
                    
                    # Use blastdbcmd to get database info
                    cmd = f"blastdbcmd -db {self.data_dir}/{db_name} -info"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        info_lines = result.stdout.strip().split('\n')
                        
                        # Parse database info
                        db_info = {'name': db_name}
                        for line in info_lines:
                            if 'sequences' in line.lower():
                                try:
                                    seq_count = int(''.join(filter(str.isdigit, line)))
                                    db_info['sequence_count'] = seq_count
                                except:
                                    pass
                            elif 'total length' in line.lower():
                                try:
                                    total_len = int(''.join(filter(str.isdigit, line)))
                                    db_info['total_length'] = total_len
                                except:
                                    pass
                        
                        sequence_analysis[db_name] = db_info
                        print(f"  {db_name}: {db_info}")
                    
                    # Try to get sample sequences for length distribution
                    cmd_sample = f"blastdbcmd -db {self.data_dir}/{db_name} -entry all -outfmt '%l' | head -1000"
                    result_sample = subprocess.run(cmd_sample, shell=True, capture_output=True, text=True)
                    
                    if result_sample.returncode == 0:
                        lengths = []
                        for line in result_sample.stdout.strip().split('\n'):
                            try:
                                length = int(line.strip())
                                if length > 0:
                                    lengths.append(length)
                            except:
                                continue
                        
                        if lengths:
                            sequence_analysis[db_name]['sample_lengths'] = lengths
                            sequence_analysis[db_name]['avg_sample_length'] = np.mean(lengths)
                            sequence_analysis[db_name]['median_sample_length'] = np.median(lengths)
                            sequence_analysis[db_name]['std_sample_length'] = np.std(lengths)
                            
                            print(f"    Sample analysis: {len(lengths)} sequences")
                            print(f"    Avg length: {np.mean(lengths):.1f} bp")
                            print(f"    Median length: {np.median(lengths):.1f} bp")
                            print(f"    Std dev: {np.std(lengths):.1f} bp")
                
                except Exception as e:
                    print(f"  Error analyzing {db_name}: {e}")
        
        # Visualize sequence length distributions
        if any('sample_lengths' in info for info in sequence_analysis.values()):
            fig, axes = plt.subplots(1, len(sequence_analysis), figsize=(15, 5))
            if len(sequence_analysis) == 1:
                axes = [axes]
            
            for i, (db_name, info) in enumerate(sequence_analysis.items()):
                if 'sample_lengths' in info:
                    ax = axes[i] if len(sequence_analysis) > 1 else axes[0]
                    ax.hist(info['sample_lengths'], bins=30, alpha=0.7, color=f'C{i}')
                    ax.set_title(f'{db_name}\nSequence Length Distribution')
                    ax.set_xlabel('Sequence Length (bp)')
                    ax.set_ylabel('Frequency')
                    ax.axvline(info['avg_sample_length'], color='red', linestyle='--', 
                              label=f'Mean: {info["avg_sample_length"]:.0f}')
                    ax.legend()
            
            plt.tight_layout()
            plt.savefig('sequence_length_distributions.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        return sequence_analysis
        """Generate comprehensive statistical summary"""
        print("\n=== COMPREHENSIVE STATISTICAL SUMMARY ===")
        
        # Collect all analysis results
        summary_stats = {}
        
        # Database distribution analysis
        file_types = defaultdict(int)
        for f in self.data_dir.glob("*"):
            if f.is_file():
                ext = f.suffix.lower()
                file_types[ext] += 1
        
        # Most common file types
        common_types = dict(Counter(file_types).most_common(10))
        
        print("File extension distribution:")
        for ext, count in common_types.items():
            print(f"  {ext}: {count} files")
        
        # Statistical tests and insights
        print(f"\nKey statistical insights:")
        print(f"- File extension diversity: {len(file_types)} unique types")
        print(f"- Most common extension: {max(file_types, key=file_types.get)} ({max(file_types.values())} files)")
        
        # Generate summary visualization
        plt.figure(figsize=(12, 8))
        
        # File type distribution
        plt.subplot(2, 2, 1)
        extensions = list(common_types.keys())[:8]
        counts = list(common_types.values())[:8]
        plt.pie(counts, labels=extensions, autopct='%1.1f%%', startangle=90)
        plt.title('File Extension Distribution')
        
        # Database complexity analysis
        plt.subplot(2, 2, 2)
        complexity_scores = []
        db_names = []
        
        for f in self.data_dir.glob("*.json"):
            db_name = f.stem.replace('-nucl-metadata', '').replace('-prot-metadata', '')
            # Simple complexity score based on name length and components
            complexity = len(db_name.split('_')) + len(db_name) / 10
            complexity_scores.append(complexity)
            db_names.append(db_name[:10])  # Truncate for display
        
        if complexity_scores:
            plt.bar(range(len(complexity_scores)), complexity_scores)
            plt.title('Database Name Complexity Scores')
            plt.xlabel('Database Index')
            plt.ylabel('Complexity Score')
        
        plt.tight_layout()
        plt.savefig('statistical_summary.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return summary_stats

def main():
    """Execute proper statistical EDA"""
    print("=== PROPER STATISTICAL EDA FOR NCBI DATABASES ===")
    print("Focus: Content analysis, patterns, distributions")
    print("=" * 60)
    
    analyzer = ProperEDAAnalyzer()
    
    # Execute comprehensive statistical analysis
    results = {}
    
    # 1. Taxonomic distribution analysis
    tax_results = analyzer.analyze_taxonomy_distribution()
    results['taxonomy'] = tax_results
    
    # 2. Sequence metadata analysis
    metadata_results = analyzer.analyze_sequence_metadata()
    results['metadata'] = metadata_results
    
    # 3. Database pattern analysis
    pattern_results = analyzer.analyze_database_patterns()
    results['patterns'] = pattern_results
    
    # 4. Actual sequence content analysis
    sequence_results = analyzer.analyze_actual_sequences()
    results['sequences'] = sequence_results
    
    # 5. Eukaryotic content analysis
    euk_results = analyzer.analyze_eukaryotic_content()
    results['eukaryotic'] = euk_results
    
    # 6. Statistical summary
    summary_results = analyzer.statistical_summary()
    results['summary'] = summary_results
    
    print("\n" + "=" * 60)
    print("PROPER EDA ANALYSIS COMPLETE")
    print("Generated visualizations:")
    print("- taxonomic_ranks_distribution.png")
    print("- sequence_metadata_analysis.png") 
    print("- database_correlation_matrix.png")
    print("- database_patterns.png")
    print("- eukaryotic_analysis.png")
    print("- statistical_summary.png")
    
    return results

if __name__ == "__main__":
    main()
