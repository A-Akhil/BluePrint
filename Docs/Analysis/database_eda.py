#!/usr/bin/env python3
"""
Comprehensive EDA for NCBI BLAST Database Collection
Marine eDNA Biodiversity Analysis Project
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('default')
sns.set_palette("husl")

class eDNADatabaseAnalyzer:
    def __init__(self, data_dir="/home/srmist32/sihdna/ncbi_blast_db_files"):
        self.data_dir = Path(data_dir)
        self.results = {}
        self.metadata = {}
        
    def get_file_inventory(self):
        """Get comprehensive file inventory and categorization"""
        print("=== DATABASE INVENTORY ANALYSIS ===")
        
        # Get all files
        all_files = list(self.data_dir.glob("*"))
        
        # Categorize by file type
        categories = {
            'nucleotide_db': [],
            'protein_db': [],
            'metadata': [],
            'taxonomy': [],
            'other': []
        }
        
        # File extensions mapping
        ext_mapping = {
            '.nhr': 'nucleotide_db', '.nin': 'nucleotide_db', '.nsq': 'nucleotide_db',
            '.nnd': 'nucleotide_db', '.nni': 'nucleotide_db', '.nog': 'nucleotide_db',
            '.nos': 'nucleotide_db', '.not': 'nucleotide_db', '.ntf': 'nucleotide_db',
            '.nto': 'nucleotide_db', '.ndb': 'nucleotide_db',
            '.phr': 'protein_db', '.pin': 'protein_db', '.psq': 'protein_db',
            '.pnd': 'protein_db', '.pni': 'protein_db', '.pog': 'protein_db',
            '.pos': 'protein_db', '.pot': 'protein_db', '.ptf': 'protein_db',
            '.pto': 'protein_db', '.pdb': 'protein_db',
            '.json': 'metadata',
            '.btd': 'taxonomy', '.bti': 'taxonomy', '.sqlite3': 'taxonomy'
        }
        
        # Categorize files
        for file_path in all_files:
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in ext_mapping:
                    categories[ext_mapping[ext]].append(file_path)
                else:
                    categories['other'].append(file_path)
        
        # Calculate sizes
        size_summary = {}
        for category, files in categories.items():
            if files:
                total_size = sum(f.stat().st_size for f in files if f.exists())
                size_summary[category] = {
                    'count': len(files),
                    'total_size_gb': total_size / (1024**3),
                    'files': [f.name for f in files[:10]]
                }
        
        self.results['file_inventory'] = {
            'categories': categories,
            'size_summary': size_summary,
            'total_files': sum(len(files) for files in categories.values())
        }
        
        # Print summary
        print(f"Total files analyzed: {self.results['file_inventory']['total_files']}")
        print("\nFile categorization:")
        for category, info in size_summary.items():
            print(f"  {category}: {info['count']} files, {info['total_size_gb']:.2f} GB")
        
        return self.results['file_inventory']
    
    def analyze_database_structure(self):
        """Analyze database naming patterns and multi-volume structure"""
        print("\n=== DATABASE STRUCTURE ANALYSIS ===")
        
        # Get all database base names
        all_files = [f.name for f in self.data_dir.glob("*") if f.is_file()]
        
        # Extract base database names
        db_patterns = defaultdict(list)
        
        for filename in all_files:
            # Remove extensions and volume numbers
            base_name = filename.split('.')[0]
            
            # Handle numbered volumes
            if any(char.isdigit() for char in base_name.split('.')[-1]):
                base_name = '.'.join(base_name.split('.')[:-1])
            
            db_patterns[base_name].append(filename)
        
        # Analyze multi-volume databases
        db_analysis = {}
        for db_name, files in db_patterns.items():
            if len(files) > 1:  # Multi-volume
                # Calculate total size
                total_size = 0
                for filename in files:
                    file_path = self.data_dir / filename
                    if file_path.exists():
                        total_size += file_path.stat().st_size
                
                db_analysis[db_name] = {
                    'volume_count': len(files),
                    'total_files': len(files),
                    'total_size_gb': total_size / (1024**3),
                    'file_sample': files[:5]
                }
        
        # Sort by size
        sorted_dbs = sorted(db_analysis.items(), key=lambda x: x[1]['total_size_gb'], reverse=True)
        
        self.results['database_structure'] = {
            'multi_volume_dbs': dict(sorted_dbs),
            'total_databases': len(db_patterns),
            'multi_volume_count': len(db_analysis)
        }
        
        print(f"Total database groups: {len(db_patterns)}")
        print(f"Multi-volume databases: {len(db_analysis)}")
        print("\nTop 10 largest databases:")
        for i, (db_name, info) in enumerate(sorted_dbs[:10]):
            print(f"  {i+1}. {db_name}: {info['volume_count']} volumes, {info['total_size_gb']:.2f} GB")
        
        return self.results['database_structure']
    
    def parse_metadata_files(self):
        """Parse JSON metadata files for database content information"""
        print("\n=== METADATA ANALYSIS ===")
        
        metadata_files = list(self.data_dir.glob("*.json"))
        parsed_metadata = {}
        
        for meta_file in metadata_files:
            try:
                with open(meta_file, 'r') as f:
                    data = json.load(f)
                    db_name = meta_file.stem.replace('-nucl-metadata', '').replace('-prot-metadata', '')
                    parsed_metadata[db_name] = data
                    
                    # Extract key information
                    if 'DbInfo' in data:
                        db_info = data['DbInfo']
                        print(f"\n{db_name}:")
                        if 'DbName' in db_info:
                            print(f"  Name: {db_info['DbName']}")
                        if 'Description' in db_info:
                            print(f"  Description: {db_info['Description'][:100]}...")
                        if 'NumLetters' in db_info:
                            print(f"  Total letters: {db_info['NumLetters']:,}")
                        if 'NumSequences' in db_info:
                            print(f"  Total sequences: {db_info['NumSequences']:,}")
                            
            except Exception as e:
                print(f"Error parsing {meta_file}: {e}")
        
        self.metadata = parsed_metadata
        self.results['metadata'] = parsed_metadata
        
        print(f"\nSuccessfully parsed {len(parsed_metadata)} metadata files")
        return parsed_metadata
    
    def assess_marine_relevance(self):
        """Assess databases for marine and eukaryotic content relevance"""
        print("\n=== MARINE RELEVANCE ASSESSMENT ===")
        
        # Define database priorities for marine eDNA
        marine_priority = {
            'nt_euk': {'priority': 1, 'reason': 'Eukaryotic nucleotides - primary target'},
            'ref_euk_rep_genomes': {'priority': 1, 'reason': 'Representative eukaryotic genomes'},
            'refseq_rna': {'priority': 2, 'reason': 'Curated RNA sequences including rRNA markers'},
            '18S_fungal_sequences': {'priority': 2, 'reason': '18S rRNA phylogenetic marker'},
            '28S_fungal_sequences': {'priority': 2, 'reason': '28S rRNA phylogenetic marker'},
            'nt': {'priority': 3, 'reason': 'Complete nucleotide database (includes all)'},
            'refseq_protein': {'priority': 3, 'reason': 'Protein sequences for functional annotation'},
            'tsa_nt': {'priority': 4, 'reason': 'Transcriptome data may include marine organisms'},
            'nt_prok': {'priority': 5, 'reason': 'Prokaryotic sequences - secondary interest'},
            'swissprot': {'priority': 4, 'reason': 'High-quality protein annotations'}
        }
        
        # Assess available databases
        db_structure = self.results.get('database_structure', {})
        available_priority_dbs = {}
        
        for db_name, priority_info in marine_priority.items():
            if db_name in db_structure.get('multi_volume_dbs', {}):
                db_info = db_structure['multi_volume_dbs'][db_name]
                available_priority_dbs[db_name] = {
                    **priority_info,
                    **db_info
                }
        
        # Sort by priority and size
        sorted_priority = sorted(available_priority_dbs.items(), 
                               key=lambda x: (x[1]['priority'], -x[1]['total_size_gb']))
        
        self.results['marine_relevance'] = {
            'priority_databases': dict(sorted_priority),
            'recommendations': {
                'tier_1': [db for db, info in sorted_priority if info['priority'] <= 2],
                'tier_2': [db for db, info in sorted_priority if info['priority'] == 3],
                'tier_3': [db for db, info in sorted_priority if info['priority'] >= 4]
            }
        }
        
        print("Database relevance for marine eDNA (sorted by priority):")
        for db_name, info in sorted_priority:
            print(f"  Priority {info['priority']}: {db_name} ({info['total_size_gb']:.1f} GB)")
            print(f"    {info['reason']}")
        
        return self.results['marine_relevance']
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n=== GENERATING COMPREHENSIVE REPORT ===")
        
        report_path = "/home/srmist32/sihdna/eda_report.md"
        
        with open(report_path, 'w') as f:
            f.write("# NCBI BLAST Database Collection - Comprehensive EDA Report\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"**Total Dataset Size**: 3.3TB across {self.results['file_inventory']['total_files']} files\n")
            f.write(f"**Database Count**: {self.results['database_structure']['total_databases']} distinct databases\n")
            f.write(f"**Multi-volume Databases**: {self.results['database_structure']['multi_volume_count']}\n\n")
            
            f.write("## Key Findings\n\n")
            f.write("### 1. Database Scale and Structure\n")
            top_dbs = list(self.results['database_structure']['multi_volume_dbs'].items())[:5]
            for db_name, info in top_dbs:
                f.write(f"- **{db_name}**: {info['volume_count']} volumes, {info['total_size_gb']:.1f} GB\n")
            
            f.write("\n### 2. Marine eDNA Relevance Ranking\n")
            if 'marine_relevance' in self.results:
                recommendations = self.results['marine_relevance']['recommendations']
                f.write("**Tier 1 (Highest Priority)**:\n")
                for db in recommendations['tier_1']:
                    f.write(f"- {db}\n")
                f.write("\n**Tier 2 (Secondary Priority)**:\n")
                for db in recommendations['tier_2']:
                    f.write(f"- {db}\n")
            
            f.write("\n## Recommendations\n\n")
            f.write("1. **Start with nt_euk**: Largest eukaryotic-specific database\n")
            f.write("2. **Add rRNA markers**: 18S and 28S fungal sequences for phylogenetic analysis\n")
            f.write("3. **Consider RefSeq RNA**: High-quality curated sequences\n")
            f.write("4. **Computational strategy**: Begin with minimal set, expand based on results\n")
            
        print(f"Comprehensive report saved to {report_path}")
    
    def run_complete_analysis(self):
        """Run the complete EDA pipeline"""
        print("Starting comprehensive NCBI BLAST database EDA...")
        print("=" * 60)
        
        # Execute analysis steps
        self.get_file_inventory()
        self.analyze_database_structure()
        self.parse_metadata_files()
        self.assess_marine_relevance()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("EDA ANALYSIS COMPLETE")
        print("=" * 60)
        
        return self.results

# Execute the analysis
if __name__ == "__main__":
    analyzer = eDNADatabaseAnalyzer()
    results = analyzer.run_complete_analysis()