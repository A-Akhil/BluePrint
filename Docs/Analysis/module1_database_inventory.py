#!/usr/bin/env python3
"""
Module 1: Database Inventory for Deep-Sea eDNA
Simple inventory of available NCBI BLAST databases
"""

import os
import json
from pathlib import Path

def get_database_inventory(blast_db_path="/home/srmist32/sihdna/ncbi_blast_db_files"):
    """Get basic inventory of BLAST databases"""
    print("📋 NCBI BLAST Database Inventory")
    print("="*40)
    
    db_files = {}
    metadata_files = list(Path(blast_db_path).glob("*-metadata.json"))
    
    for metadata_file in metadata_files:
        db_name = metadata_file.stem.replace("-nucl-metadata", "").replace("-prot-metadata", "")
        
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            db_files[db_name] = {
                'sequences': metadata.get('number-of-sequences', 0),
                'bases': metadata.get('number-of-letters', 0),
                'description': metadata.get('description', ''),
                'type': 'nucleotide' if 'nucl' in metadata_file.name else 'protein'
            }
            
            print(f"📊 {db_name}")
            print(f"   Sequences: {db_files[db_name]['sequences']:,}")
            print(f"   Type: {db_files[db_name]['type']}")
            
        except Exception as e:
            print(f"❌ Error reading {metadata_file}: {e}")
    
    # Save inventory
    with open('database_inventory.json', 'w') as f:
        json.dump(db_files, f, indent=2)
    
    print(f"\n✅ Found {len(db_files)} databases")
    print("💾 Saved: database_inventory.json")
    return db_files

if __name__ == "__main__":
    inventory = get_database_inventory()
