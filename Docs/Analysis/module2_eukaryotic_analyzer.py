#!/usr/bin/env python3
"""
Module 2: Eukaryotic Database Analyzer
Identify databases relevant for eukaryotic eDNA analysis
"""

import json
import os

def analyze_eukaryotic_databases():
    """Analyze databases for eukaryotic relevance"""
    print("🔬 Eukaryotic Database Analysis")
    print("="*35)
    
    # Load inventory
    if not os.path.exists('database_inventory.json'):
        print("❌ Run module1_database_inventory.py first!")
        return
    
    with open('database_inventory.json', 'r') as f:
        inventory = json.load(f)
    
    # Define eukaryotic databases
    eukaryotic_dbs = {
        'SSU_eukaryote_rRNA': 'PRIMARY - 18S rRNA universal marker',
        'LSU_eukaryote_rRNA': 'SECONDARY - 28S rRNA phylogenetic',
        'ITS_eukaryote_sequences': 'TERTIARY - Species identification',
        'ITS_RefSeq_Fungi': 'SUPPLEMENTARY - Fungal diversity',
        '28S_fungal_sequences': 'SUPPLEMENTARY - Fungal phylogeny',
        'nt_euk': 'COMPREHENSIVE - All eukaryotic sequences'
    }
    
    results = {}
    
    for db_name, relevance in eukaryotic_dbs.items():
        if db_name in inventory:
            print(f"\n🎯 {db_name}")
            print(f"   Relevance: {relevance}")
            print(f"   Sequences: {inventory[db_name]['sequences']:,}")
            
            # Calculate average sequence length
            if inventory[db_name]['sequences'] > 0 and inventory[db_name]['bases'] > 0:
                avg_len = inventory[db_name]['bases'] / inventory[db_name]['sequences']
                print(f"   Avg Length: {avg_len:.1f} bp")
            
            results[db_name] = {
                'relevance': relevance,
                'sequences': inventory[db_name]['sequences'],
                'avg_length': avg_len if 'avg_len' in locals() else 0
            }
        else:
            print(f"❌ {db_name} not found in inventory")
    
    # Save results
    with open('eukaryotic_databases.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Analyzed {len(results)} eukaryotic databases")
    print("💾 Saved: eukaryotic_databases.json")
    
    return results

if __name__ == "__main__":
    results = analyze_eukaryotic_databases()
