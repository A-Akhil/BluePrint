#!/usr/bin/env python3
"""
Module 4: Deep-Sea Relevance Assessor
Assess database coverage for deep-sea organisms
"""

import json

def assess_deep_sea_relevance():
    """Assess deep-sea relevance and database gaps"""
    print("🌊 Deep-Sea Relevance Assessment")
    print("="*35)
    
    # Expected taxonomic composition in deep-sea eDNA
    taxa_composition = {
        'Protists': {
            'abundance_range': '60-80%',
            'examples': ['Radiolaria', 'Foraminifera', 'Ciliates'],
            'database_coverage': 'MODERATE',
            'relevance': 'HIGH'
        },
        'Cnidarians': {
            'abundance_range': '5-15%',
            'examples': ['Deep-sea corals', 'Hydrozoa'],
            'database_coverage': 'POOR',
            'relevance': 'MODERATE'
        },
        'Metazoans': {
            'abundance_range': '10-25%',
            'examples': ['Nematodes', 'Copepods', 'Polychaetes'],
            'database_coverage': 'VERY POOR',
            'relevance': 'HIGH'
        },
        'Fungi': {
            'abundance_range': '1-5%',
            'examples': ['Marine fungi', 'Yeasts'],
            'database_coverage': 'POOR',
            'relevance': 'LOW'
        }
    }
    
    print("Expected Taxa in Deep-Sea eDNA:")
    for taxa, info in taxa_composition.items():
        print(f"\n🦠 {taxa.upper()}")
        print(f"   Abundance: {info['abundance_range']}")
        print(f"   Examples: {', '.join(info['examples'])}")
        print(f"   DB Coverage: {info['database_coverage']}")
        print(f"   Relevance: {info['relevance']}")
    
    # Database gaps
    gaps = {
        'Depth_Bias': '20-40% unassigned sequences expected',
        'Geographic_Bias': 'Novel deep-sea lineages missed',
        'Taxonomic_Bias': 'High false positive risk',
        'Marker_Bias': 'Phylogenetic placement required'
    }
    
    print(f"\n❌ Critical Database Gaps:")
    for gap, consequence in gaps.items():
        print(f"   {gap.replace('_', ' ')}: {consequence}")
    
    # Save results
    results = {
        'taxa_composition': taxa_composition,
        'database_gaps': gaps
    }
    
    with open('deep_sea_assessment.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Assessment complete")
    print("💾 Saved: deep_sea_assessment.json")
    
    return results

if __name__ == "__main__":
    results = assess_deep_sea_relevance()
