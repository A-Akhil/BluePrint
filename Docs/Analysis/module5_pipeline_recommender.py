#!/usr/bin/env python3
"""
Module 5: Pipeline Recommender
Recommend analysis pipeline for deep-sea eDNA
"""

import json

def recommend_pipeline():
    """Recommend hierarchical eDNA analysis pipeline"""
    print("🔬 eDNA Analysis Pipeline Recommendation")
    print("="*45)
    
    pipeline = {
        'Step_1_Primary_18S': {
            'database': 'SSU_eukaryote_rRNA-nucl',
            'command': 'blastn -db SSU_eukaryote_rRNA-nucl -query edna.fasta -out step1_results.xml -outfmt 5',
            'expected_coverage': '60-80%',
            'focus': 'Protist diversity',
            'priority': 'ESSENTIAL'
        },
        'Step_2_Secondary_28S': {
            'database': 'LSU_eukaryote_rRNA-nucl',
            'command': 'blastn -db LSU_eukaryote_rRNA-nucl -query unassigned_step1.fasta -out step2_results.xml -outfmt 5',
            'expected_coverage': '40-60% additional',
            'focus': 'Phylogenetic placement',
            'priority': 'IMPORTANT'
        },
        'Step_3_Species_Level': {
            'database': 'ITS_eukaryote_sequences-nucl',
            'command': 'blastn -db ITS_eukaryote_sequences-nucl -query unassigned_step2.fasta -out step3_results.xml -outfmt 5',
            'expected_coverage': '10-30% additional',
            'focus': 'Species identification',
            'priority': 'SUPPLEMENTARY'
        },
        'Step_4_Comprehensive': {
            'database': 'nt_euk-nucl',
            'command': 'blastn -db nt_euk-nucl -query unassigned_step3.fasta -out step4_results.xml -outfmt 5',
            'expected_coverage': '5-15% additional',
            'focus': 'Comprehensive search',
            'priority': 'BACKUP (expensive)'
        },
        'Step_5_Novel_Taxa': {
            'database': 'AI/ML approach',
            'command': 'python novel_taxa_classifier.py unassigned_final.fasta',
            'expected_coverage': '20-40% of total',
            'focus': 'Novel lineage discovery',
            'priority': 'CRITICAL for deep-sea'
        }
    }
    
    print("Recommended Pipeline Steps:")
    for step_name, details in pipeline.items():
        step_num = step_name.split('_')[1]
        print(f"\n🎯 STEP {step_num}: {' '.join(step_name.split('_')[2:]).title()}")
        print(f"   Database: {details['database']}")
        print(f"   Command: {details['command']}")
        print(f"   Coverage: {details['expected_coverage']}")
        print(f"   Focus: {details['focus']}")
        print(f"   Priority: {details['priority']}")
    
    # Generate bash script
    bash_script = "#!/bin/bash\n"
    bash_script += "# Deep-Sea eDNA Analysis Pipeline\n\n"
    
    for i, (step_name, details) in enumerate(pipeline.items(), 1):
        if 'blastn' in details['command']:
            bash_script += f"# Step {i}: {details['focus']}\n"
            bash_script += f"echo 'Running Step {i}: {details['focus']}'\n"
            bash_script += f"{details['command']}\n\n"
    
    with open('edna_pipeline.sh', 'w') as f:
        f.write(bash_script)
    
    # Save pipeline config
    with open('pipeline_config.json', 'w') as f:
        json.dump(pipeline, f, indent=2)
    
    print(f"\n✅ Pipeline configured with {len(pipeline)} steps")
    print("💾 Saved: pipeline_config.json")
    print("💾 Saved: edna_pipeline.sh")
    
    return pipeline

if __name__ == "__main__":
    pipeline = recommend_pipeline()
