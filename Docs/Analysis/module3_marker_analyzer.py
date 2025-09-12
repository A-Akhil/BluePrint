#!/usr/bin/env python3
"""
Module 3: Marker Gene Analyzer
Analyze marker genes for deep-sea eDNA applications
"""

import json

def analyze_marker_genes():
    """Analyze marker genes for eDNA suitability"""
    print("🧬 Marker Gene Analysis")
    print("="*25)
    
    markers = {
        '18S_rRNA': {
            'databases': ['SSU_eukaryote_rRNA'],
            'optimal_length': '1200-2000bp (full) or 400-800bp (V4)',
            'resolution': 'Genus to phylum',
            'deep_sea_score': 5,  # 1-5 scale
            'expected_success': '60-80%'
        },
        '28S_rRNA': {
            'databases': ['LSU_eukaryote_rRNA', '28S_fungal_sequences'],
            'optimal_length': '1000-4000bp',
            'resolution': 'Higher taxonomy',
            'deep_sea_score': 4,
            'expected_success': '40-60%'
        },
        'ITS_region': {
            'databases': ['ITS_eukaryote_sequences', 'ITS_RefSeq_Fungi'],
            'optimal_length': '200-800bp',
            'resolution': 'Species level',
            'deep_sea_score': 2,
            'expected_success': '10-30%'
        },
        'COI': {
            'databases': ['nt_euk (limited)'],
            'optimal_length': '650bp',
            'resolution': 'Species level',
            'deep_sea_score': 1,
            'expected_success': '<5%'
        }
    }
    
    print("Marker Performance for Deep-Sea eDNA:")
    for marker, info in markers.items():
        print(f"\n🎯 {marker.replace('_', ' ').upper()}")
        print(f"   Databases: {', '.join(info['databases'])}")
        print(f"   Length: {info['optimal_length']}")
        print(f"   Resolution: {info['resolution']}")
        print(f"   Deep-sea Score: {info['deep_sea_score']}/5")
        print(f"   Expected Success: {info['expected_success']}")
    
    # Save results
    with open('marker_analysis.json', 'w') as f:
        json.dump(markers, f, indent=2)
    
    print(f"\n✅ Analyzed {len(markers)} marker genes")
    print("💾 Saved: marker_analysis.json")
    
    return markers

if __name__ == "__main__":
    results = analyze_marker_genes()
