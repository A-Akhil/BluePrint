#!/usr/bin/env python3
"""
Proper EDA Analysis for NCBI BLAST Databases
Focus: Statistical content analysis rather than file inventory
"""

import os
import json
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import subprocess
import re
from datetime import datetime

class ProperEDAAnalyzer:
    def __init__(self, base_path='ncbi_blast_db_files'):
        self.base_path = base_path
        self.metadata_files = []
        self.database_files = []
        self.taxonomy_db_path = None
        self._scan_directory()
    
    def _scan_directory(self):
        """Scan the directory for database and metadata files"""
        if not os.path.exists(self.base_path):
            print(f"Error: Directory {self.base_path} not found")
            return
        
        for file in os.listdir(self.base_path):
            if file.endswith('-metadata.json'):
                self.metadata_files.append(file)
            elif file.endswith(('.nhr', '.phr', '.ndb', '.pdb')):
                self.database_files.append(file)
            elif file.endswith('.sqlite3'):
                self.taxonomy_db_path = os.path.join(self.base_path, file)
    
    def analyze_taxonomy_distribution(self):
        """Analyze taxonomic distribution using the taxonomy database"""
        print("=== TAXONOMIC DISTRIBUTION ANALYSIS ===")
        
        if not self.taxonomy_db_path:
            print("No taxonomy database found")
            return {"error": "No taxonomy database"}
        
        try:
            conn = sqlite3.connect(self.taxonomy_db_path)
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Available tables: {[t[0] for t in tables]}")
            
            # Basic taxonomy statistics
            if tables:
                table_name = tables[0][0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                total_taxa = cursor.fetchone()[0]
                print(f"Total taxonomic entries: {total_taxa:,}")
                
                # Sample data structure
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                sample_data = cursor.fetchall()
                
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                
                if sample_data:
                    print(f"Columns: {columns}")
                    print("Sample data:")
                    for row in sample_data[:3]:
                        print(f"  {row}")
            
            conn.close()
            return {"total_taxa": total_taxa, "tables": [t[0] for t in tables]}
            
        except Exception as e:
            print(f"Error accessing taxonomy database: {e}")
            return {"error": str(e)}
    
    def analyze_sequence_metadata(self):
        """Analyze sequence metadata from JSON files"""
        print("\n=== SEQUENCE METADATA ANALYSIS ===")
        print(f"Found {len(self.metadata_files)} metadata files")
        
        metadata_list = []
        errors = []
        
        for file in self.metadata_files:
            try:
                full_path = os.path.join(self.base_path, file)
                with open(full_path, 'r') as f:
                    data = json.load(f)
                    
                if isinstance(data, dict):
                    # Extract key statistics
                    record = {
                        'database': file.replace('-metadata.json', ''),
                        'sequences': data.get('sequences', 0),
                        'letters': data.get('letters', 0),
                        'dbtype': data.get('dbtype', 'unknown'),
                        'description': data.get('description', '')
                    }
                    
                    # Calculate average sequence length
                    if record['sequences'] > 0:
                        record['avg_length'] = record['letters'] / record['sequences']
                    else:
                        record['avg_length'] = 0
                    
                    metadata_list.append(record)
                else:
                    errors.append(f"Invalid format in {file}")
                    
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
                errors.append(f"Error in {file}: {str(e)}")
        
        if not metadata_list:
            return {"error": "No valid metadata found"}
        
        df = pd.DataFrame(metadata_list)
        
        print(f"\nMetadata analysis for {len(df)} databases:")
        print(f"Total sequences: {df['sequences'].sum():,}")
        print(f"Total nucleotides/amino acids: {df['letters'].sum():,}")
        
        # Statistics
        print("\nSequence count statistics:")
        print(df['sequences'].describe())
        
        print("\nAverage sequence length statistics:")
        print(df['avg_length'].describe())
        
        # Correlation analysis
        numeric_cols = ['sequences', 'letters', 'avg_length']
        correlation_matrix = df[numeric_cols].corr()
        print("\nCorrelation analysis:")
        print(correlation_matrix)
        
        # Create visualizations
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Sequence Metadata Analysis', fontsize=16)
        
        # Distribution plots
        df['sequences'].hist(bins=20, ax=axes[0, 0])
        axes[0, 0].set_title('Sequence Count Distribution')
        axes[0, 0].set_xlabel('Number of Sequences')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_yscale('log')
        
        df['avg_length'].hist(bins=20, ax=axes[0, 1])
        axes[0, 1].set_title('Average Sequence Length Distribution')
        axes[0, 1].set_xlabel('Average Length')
        axes[0, 1].set_ylabel('Frequency')
        
        # Scatter plot
        axes[1, 0].scatter(df['sequences'], df['letters'], alpha=0.7)
        axes[1, 0].set_title('Sequences vs Total Letters')
        axes[1, 0].set_xlabel('Number of Sequences')
        axes[1, 0].set_ylabel('Total Letters')
        axes[1, 0].set_xscale('log')
        axes[1, 0].set_yscale('log')
        
        # Database type distribution
        dbtype_counts = df['dbtype'].value_counts()
        axes[1, 1].pie(dbtype_counts.values, labels=dbtype_counts.index, autopct='%1.1f%%')
        axes[1, 1].set_title('Database Type Distribution')
        
        plt.tight_layout()
        plt.savefig('sequence_metadata_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Correlation heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Database Correlation Matrix')
        plt.tight_layout()
        plt.savefig('database_correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "total_databases": len(df),
            "total_sequences": int(df['sequences'].sum()),
            "total_letters": int(df['letters'].sum()),
            "avg_sequences_per_db": float(df['sequences'].mean()),
            "correlation_matrix": correlation_matrix.to_dict(),
            "database_types": dbtype_counts.to_dict(),
            "errors": errors
        }
    
    def analyze_database_patterns(self):
        """Analyze patterns in database names and types"""
        print("\n=== DATABASE PATTERN ANALYSIS ===")
        
        # Extract patterns from database names
        patterns = {
            'nucleotide_types': set(),
            'protein_types': set(),
            'taxonomic_groups': set(),
            'data_sources': set(),
            'version_patterns': set()
        }
        
        nucleotide_keywords = ['nucl', 'nt', 'rna', 'rRNA', 'ITS', 'LSU', 'SSU']
        protein_keywords = ['prot', 'protein', 'nr', 'swiss']
        taxonomic_keywords = ['euk', 'prok', 'viral', 'fungal', 'bacteria']
        
        for filename in self.metadata_files:
            basename = filename.replace('-metadata.json', '')
            
            # Check for nucleotide databases
            if any(keyword in basename for keyword in nucleotide_keywords):
                patterns['nucleotide_types'].add(basename)
            
            # Check for protein databases
            if any(keyword in basename for keyword in protein_keywords):
                patterns['protein_types'].add(basename)
            
            # Check for taxonomic groups
            if any(keyword in basename for keyword in taxonomic_keywords):
                patterns['taxonomic_groups'].add(basename)
            
            # Data sources
            if any(source in basename.lower() for source in ['refseq', 'genbank', 'pdb', 'swiss']):
                patterns['data_sources'].add(basename)
            
            # Version patterns (look for numbers)
            if re.search(r'\d+', basename):
                patterns['version_patterns'].add(re.findall(r'\d+', basename)[0])
        
        print("Database pattern analysis:")
        for pattern_type, pattern_set in patterns.items():
            print(f"  {pattern_type}: {len(pattern_set)} unique patterns")
            if pattern_set:
                examples = list(pattern_set)[:5]
                print(f"    Examples: {examples}")
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Database Pattern Analysis', fontsize=16)
        
        # Pattern type distribution
        pattern_counts = {k: len(v) for k, v in patterns.items() if v}
        if pattern_counts:
            axes[0, 0].bar(pattern_counts.keys(), pattern_counts.values())
            axes[0, 0].set_title('Pattern Type Distribution')
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Database name length distribution
        name_lengths = [len(f.replace('-metadata.json', '')) for f in self.metadata_files]
        axes[0, 1].hist(name_lengths, bins=15)
        axes[0, 1].set_title('Database Name Length Distribution')
        axes[0, 1].set_xlabel('Name Length (characters)')
        axes[0, 1].set_ylabel('Frequency')
        
        # Word frequency in database names
        all_words = []
        for filename in self.metadata_files:
            basename = filename.replace('-metadata.json', '')
            words = re.findall(r'[a-zA-Z]+', basename)
            all_words.extend([w.lower() for w in words if len(w) > 2])
        
        word_freq = Counter(all_words)
        top_words = dict(word_freq.most_common(10))
        
        if top_words:
            axes[1, 0].barh(list(top_words.keys()), list(top_words.values()))
            axes[1, 0].set_title('Top 10 Words in Database Names')
            axes[1, 0].set_xlabel('Frequency')
        
        # Database file size patterns (if available)
        file_sizes = []
        for db_file in self.database_files[:20]:  # Sample for performance
            try:
                full_path = os.path.join(self.base_path, db_file)
                size = os.path.getsize(full_path)
                file_sizes.append(size / (1024**3))  # Convert to GB
            except:
                continue
        
        if file_sizes:
            axes[1, 1].hist(file_sizes, bins=15)
            axes[1, 1].set_title('Database File Size Distribution (GB)')
            axes[1, 1].set_xlabel('Size (GB)')
            axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('database_patterns.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "patterns": {k: list(v) for k, v in patterns.items()},
            "word_frequency": dict(word_freq.most_common(20)),
            "pattern_counts": pattern_counts
        }
    
    def analyze_actual_sequences(self):
        """Analyze actual sequence content using blastdbcmd"""
        print("\n=== ACTUAL SEQUENCE CONTENT ANALYSIS ===")
        
        # Find some representative databases to analyze
        sample_dbs = []
        for filename in self.metadata_files[:3]:  # Limit for performance
            db_name = filename.replace('-metadata.json', '')
            db_path = os.path.join(self.base_path, db_name)
            
            # Check if corresponding database files exist
            if any(f.startswith(db_name) for f in self.database_files):
                sample_dbs.append(db_name)
        
        sequence_stats = {}
        
        for db_name in sample_dbs:
            print(f"Analyzing sequences in {db_name}...")
            try:
                # Try to get sequence information using blastdbcmd
                cmd = f"blastdbcmd -db {os.path.join(self.base_path, db_name)} -info"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    info_output = result.stdout
                    # Parse basic information
                    lines = info_output.split('\n')
                    for line in lines:
                        if 'sequences' in line.lower():
                            print(f"  {line.strip()}")
                        elif 'total length' in line.lower():
                            print(f"  {line.strip()}")
                
                # Sample a few sequences for analysis
                cmd = f"blastdbcmd -db {os.path.join(self.base_path, db_name)} -entry all -outfmt '%t %l' | head -10"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    sequence_info = result.stdout
                    if sequence_info.strip():
                        print(f"  Sample sequence info for {db_name}:")
                        print(f"    {sequence_info[:200]}...")
                
            except subprocess.TimeoutExpired:
                print(f"  Timeout analyzing {db_name}")
            except Exception as e:
                print(f"  Error analyzing {db_name}: {e}")
        
        return {"analyzed_databases": sample_dbs, "note": "Sequence analysis completed"}
    
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
    
    def statistical_summary(self):
        """Generate comprehensive statistical summary of all analyses"""
        print("\n=== STATISTICAL SUMMARY ===")
        
        summary = {
            "total_databases": len(self.metadata_files),
            "database_types": {},
            "size_distribution": {},
            "content_summary": {}
        }
        
        # Analyze database types
        nucl_count = len([f for f in self.metadata_files if 'nucl' in f])
        prot_count = len([f for f in self.metadata_files if 'prot' in f])
        
        summary["database_types"] = {
            "nucleotide": nucl_count,
            "protein": prot_count,
            "other": len(self.metadata_files) - nucl_count - prot_count
        }
        
        # Get size statistics from previous analysis
        metadata_stats = []
        for f in self.metadata_files[:20]:  # Sample for performance
            try:
                full_path = os.path.join(self.base_path, f)
                with open(full_path, 'r') as file:
                    data = json.load(file)
                    if isinstance(data, dict) and 'sequences' in data:
                        metadata_stats.append({
                            'sequences': data.get('sequences', 0),
                            'letters': data.get('letters', 0)
                        })
            except:
                continue
        
        if metadata_stats:
            stats_df = pd.DataFrame(metadata_stats)
            summary["size_distribution"] = {
                "total_sequences": int(stats_df['sequences'].sum()),
                "total_letters": int(stats_df['letters'].sum()),
                "avg_sequences_per_db": float(stats_df['sequences'].mean()),
                "median_sequences_per_db": float(stats_df['sequences'].median())
            }
        
        # Print summary
        print("Database Type Distribution:")
        for db_type, count in summary["database_types"].items():
            print(f"  {db_type}: {count}")
        
        if summary["size_distribution"]:
            print("\nSize Distribution Summary:")
            for key, value in summary["size_distribution"].items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value:,}")
        
        # Create summary visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Database Statistical Summary', fontsize=16)
        
        # Database types pie chart
        db_types = list(summary["database_types"].keys())
        db_counts = list(summary["database_types"].values())
        axes[0, 0].pie(db_counts, labels=db_types, autopct='%1.1f%%')
        axes[0, 0].set_title('Database Types Distribution')
        
        # Size distribution if available
        if metadata_stats:
            stats_df['sequences'].hist(bins=15, ax=axes[0, 1])
            axes[0, 1].set_title('Sequences per Database Distribution')
            axes[0, 1].set_xlabel('Number of Sequences')
            axes[0, 1].set_ylabel('Frequency')
            
            stats_df['letters'].hist(bins=15, ax=axes[1, 0])
            axes[1, 0].set_title('Letters per Database Distribution')
            axes[1, 0].set_xlabel('Number of Letters')
            axes[1, 0].set_ylabel('Frequency')
            
            # Scatter plot
            axes[1, 1].scatter(stats_df['sequences'], stats_df['letters'])
            axes[1, 1].set_title('Sequences vs Letters Relationship')
            axes[1, 1].set_xlabel('Number of Sequences')
            axes[1, 1].set_ylabel('Number of Letters')
        
        plt.tight_layout()
        plt.savefig('statistical_summary.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return summary

def main():
    """Main function to run the proper EDA analysis"""
    print("=== PROPER STATISTICAL EDA FOR NCBI DATABASES ===")
    print("Focus: Content analysis, patterns, distributions")
    print("=" * 60)
    
    analyzer = ProperEDAAnalyzer()
    results = {}
    
    # 1. Taxonomic distribution analysis
    taxonomy_results = analyzer.analyze_taxonomy_distribution()
    results['taxonomy'] = taxonomy_results
    
    # 2. Sequence metadata analysis
    metadata_results = analyzer.analyze_sequence_metadata()
    results['metadata'] = metadata_results
    
    # 3. Database pattern analysis
    pattern_results = analyzer.analyze_database_patterns()
    results['patterns'] = pattern_results
    
    # 4. Actual sequence analysis
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
    print("- sequence_metadata_analysis.png")
    print("- database_correlation_matrix.png")
    print("- database_patterns.png")
    print("- eukaryotic_analysis.png")
    print("- statistical_summary.png")
    
    return results

if __name__ == "__main__":
    main()
