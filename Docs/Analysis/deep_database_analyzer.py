#!/usr/bin/env python3
"""
Module 7: Database Content Deep Analyzer
Analyze actual sequence content using BLAST database commands
"""

import subprocess
import json
import os

def analyze_database_content():
    """Analyze actual sequence content of databases"""
    print("🔍 DATABASE CONTENT DEEP ANALYSIS")
    print("="*40)
    
    blast_db_path = "/home/srmist32/sihdna/ncbi_blast_db_files"
    target_databases = ['SSU_eukaryote_rRNA', 'LSU_eukaryote_rRNA', 'ITS_eukaryote_sequences']
    
    results = {}
    
    for db_name in target_databases:
        print(f"\n🎯 Analyzing {db_name}")
        
        db_path = os.path.join(blast_db_path, db_name)
        
        # Check if database exists
        if not os.path.exists(f"{db_path}.nhr"):
            print(f"   ❌ Database not found: {db_path}")
            continue
            
        try:
            # Get database statistics
            cmd = ['blastdbcmd', '-db', db_path, '-info']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=blast_db_path)
            
            if result.returncode == 0:
                print(f"   ✅ Database accessible")
                
                # Extract key statistics from output
                info_text = result.stdout
                
                # Parse database info
                db_stats = {
                    'database_name': db_name,
                    'accessible': True,
                    'info_output': info_text[:500] + "..." if len(info_text) > 500 else info_text
                }
                
                # Try to get sequence count from info
                for line in info_text.split('\n'):
                    if 'sequences' in line.lower() and any(char.isdigit() for char in line):
                        db_stats['info_line'] = line.strip()
                        break
                
                # Sample a few sequences for analysis
                print(f"   🧬 Sampling sequences...")
                
                # Get first sequence
                sample_cmd = ['blastdbcmd', '-db', db_path, '-entry', '1', '-outfmt', '%f']
                sample_result = subprocess.run(sample_cmd, capture_output=True, text=True, cwd=blast_db_path)
                
                if sample_result.returncode == 0:
                    sample_seq = sample_result.stdout.strip()
                    if sample_seq:
                        # Analyze sequence composition
                        lines = sample_seq.split('\n')
                        if len(lines) > 1:
                            header = lines[0]
                            sequence = ''.join(lines[1:]).upper()
                            
                            if sequence:
                                db_stats['sample_header'] = header[:100] + "..." if len(header) > 100 else header
                                db_stats['sample_length'] = len(sequence)
                                db_stats['sample_gc_content'] = ((sequence.count('G') + sequence.count('C')) / len(sequence) * 100) if sequence else 0
                                
                                print(f"   📏 Sample length: {db_stats['sample_length']} bp")
                                print(f"   🧪 Sample GC%: {db_stats['sample_gc_content']:.1f}%")
                
                results[db_name] = db_stats
                
            else:
                print(f"   ❌ Error accessing database: {result.stderr}")
                results[db_name] = {'accessible': False, 'error': result.stderr}
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results[db_name] = {'accessible': False, 'error': str(e)}
    
    # Save results
    with open('database_content_analysis.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Content analysis complete")
    print("💾 Saved: database_content_analysis.json")
    
    return results

def create_sample_edna_data():
    """Create sample eDNA sequences for testing pipeline"""
    print("\n🧬 CREATING SAMPLE eDNA DATA")
    print("="*35)
    
    # Create sample sequences based on known eukaryotic markers
    sample_sequences = {
        'deep_sea_protist_18S': {
            'sequence': 'ACCTGGTTGATCCTGCCAGTAGTCATATGCTTGTCTCAAAGATTAAGCCATGCATGTCTAAGTATAAACAGTATCAACTTGACTTGTAAAAGGAATTGACGGAAGGGCACCACCAGGCGGCCGCTAATAGCGACGTACGAAAGCGATGGATCAGGATACCGTCGTAGTCTTAACCATAAACGATGCCGACTAGGGATCGGACGATGTTACCTTGGCACCTTCAGCTCGGTTACCGAAACGGGGGGTTGGTGTGGCAAAGGATGGTGATGGAACATATCTGGGAGGGGTGAAATCCTTCTCGTTAAGGGATGGGGAATAACGAAGTGATGGAAGAAGCGAAGTAGGCGTTCGGAGG',
            'description': 'Simulated deep-sea protist 18S rRNA (partial)',
            'expected_hit': 'SSU_eukaryote_rRNA'
        },
        'deep_sea_foram_18S': {
            'sequence': 'ACCTGGTTGATCCTGCCAGTAGTCATATGCTTGTCTCAAAGATTAAGCCATGCATGTCTAAGTATAAACAGTATCAACTTGACTTGTAAAAGGAATTGACGGAAGGGCACCACCAGGCGGCCGCTAATAGCGACGTACGAAAGCGATGGATCAGGATACCGTCGTAGTCTTAACCATAAACGATGCCGACTAGGGATCGGACGATGTTACCTTGGCACCTTCAGCTCGGTTACCGAAACGGGGGGTTGGTGTGGCAAAGGATGGTGATGGAACATATCTGGGAGGGGTGAAATCCTTCTCGTTAAGGGATGGGGAATAACGAAGTGATGGAAGAAGCGAAGTAGGCGTTCGGAGG',
            'description': 'Simulated foraminifera 18S rRNA (partial)',
            'expected_hit': 'SSU_eukaryote_rRNA'
        },
        'marine_fungus_ITS': {
            'sequence': 'TCCGTAGGTGAACCTGCGGAAGGATCATTACCGAGTTTACAACTCCCAAACCCCTGTGAACATACCACTTGTTGCCTCGGCGGATCAGCCCGCTCCCGGTAAAACGGGACGGCCCGCCGCAGGACCCCCTAAACTCTGTTTTTAGTGGAACTTCTGAGTAAAACCAAACAAATAAATCAAAACTTTCAACAACGGATCTCTTGGTTCTGGCATCGATGAAGAACGCAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTCTTTGAACGCAAGTTGCGCCCGAACC',
            'description': 'Simulated marine fungus ITS region',
            'expected_hit': 'ITS_eukaryote_sequences'
        },
        'novel_deep_cnidarian': {
            'sequence': 'ACCTGGTTGATCCTGCCAGTAGTCATATGCTTGTCTCAAAGATTAAGCCATGCATGTCTAAGTATAAACAGTATCAACTTGACTTGTAAAAGGAATTGACGGAAGGGCACCACCAGGCGGCCGCTAATAGCGACGTACGAAAGCGATGGATCAGGATACCGTCGTAGTCTTAACCATAAACGATGCCGACTAGGGATCGGACGATGTTACCTTGGCACCTTCAGCTCGGTTACCGAAACGGGGGGTTGGTGTGGCAAAGGATGGTGATGGAACATATCTGGGAGGGGTGAAATCCTTCTCGTTAAGGGATGGGGAATAACGAAGTGATGGAAGAAGCGAAGTAGGCGTTCGGAGG',
            'description': 'Simulated novel deep-sea cnidarian (may have low similarity)',
            'expected_hit': 'Low similarity to known sequences'
        }
    }
    
    # Create FASTA file with sample sequences
    with open('sample_edna_sequences.fasta', 'w') as f:
        for seq_id, data in sample_sequences.items():
            f.write(f">{seq_id} | {data['description']}\n")
            f.write(f"{data['sequence']}\n")
    
    print("📋 Created sample eDNA sequences:")
    for seq_id, data in sample_sequences.items():
        print(f"   🧬 {seq_id}: {len(data['sequence'])} bp")
        print(f"      Expected: {data['expected_hit']}")
    
    print("\n💾 Saved: sample_edna_sequences.fasta")
    
    # Create updated pipeline script with real file
    pipeline_script = """#!/bin/bash
# Deep-Sea eDNA Analysis Pipeline with Sample Data

echo "🌊 Starting Deep-Sea eDNA Analysis Pipeline"
echo "Using sample_edna_sequences.fasta as input"

# Set database path
export BLASTDB="/home/srmist32/sihdna/ncbi_blast_db_files"

# Step 1: Primary 18S Analysis
echo "🎯 Step 1: Primary 18S rRNA Analysis"
blastn -db SSU_eukaryote_rRNA -query sample_edna_sequences.fasta -out step1_18S_results.xml -outfmt 5 -evalue 1e-5

# Step 2: Secondary 28S Analysis (for demonstration)
echo "🎯 Step 2: Secondary 28S rRNA Analysis"
blastn -db LSU_eukaryote_rRNA -query sample_edna_sequences.fasta -out step2_28S_results.xml -outfmt 5 -evalue 1e-5

# Step 3: Species-Level ITS Analysis
echo "🎯 Step 3: Species-Level ITS Analysis"
blastn -db ITS_eukaryote_sequences -query sample_edna_sequences.fasta -out step3_ITS_results.xml -outfmt 5 -evalue 1e-5

echo "✅ Pipeline complete! Check result files:"
echo "   - step1_18S_results.xml"
echo "   - step2_28S_results.xml"
echo "   - step3_ITS_results.xml"
"""
    
    with open('working_edna_pipeline.sh', 'w') as f:
        f.write(pipeline_script)
    
    print("💾 Saved: working_edna_pipeline.sh (with sample data)")
    
    return sample_sequences

if __name__ == "__main__":
    # Run content analysis
    content_results = analyze_database_content()
    
    # Create sample data
    sample_data = create_sample_edna_data()
    
    print("\n🎯 DEEP ANALYSIS COMPLETE!")
    print("✅ Database content analyzed")
    print("✅ Sample eDNA data created")
    print("✅ Working pipeline ready to test")
