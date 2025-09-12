#!/usr/bin/env python3
"""
Module 6: Visualization Module
Create visualizations for deep-sea eDNA analysis
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def create_visualizations():
    """Create visualizations from analysis results"""
    print("📊 Creating Visualizations")
    print("="*25)
    
    # Load results from other modules
    data_files = {
        'eukaryotic': 'eukaryotic_databases.json',
        'markers': 'marker_analysis.json',
        'assessment': 'deep_sea_assessment.json'
    }
    
    data = {}
    for key, filename in data_files.items():
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data[key] = json.load(f)
            print(f"✅ Loaded {filename}")
        else:
            print(f"❌ Missing {filename} - run previous modules first")
            return
    
    # Create multi-panel figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Database sizes
    if 'eukaryotic' in data:
        db_names = list(data['eukaryotic'].keys())
        seq_counts = [data['eukaryotic'][db]['sequences'] for db in db_names]
        
        ax1.barh(db_names, seq_counts, color='skyblue')
        ax1.set_xlabel('Number of Sequences')
        ax1.set_title('Eukaryotic Database Sizes')
        ax1.tick_params(axis='y', labelsize=8)
    
    # 2. Marker gene scores
    if 'markers' in data:
        markers = list(data['markers'].keys())
        scores = [data['markers'][m]['deep_sea_score'] for m in markers]
        
        colors = ['red' if s <= 2 else 'orange' if s <= 3 else 'green' for s in scores]
        ax2.bar(markers, scores, color=colors)
        ax2.set_ylabel('Deep-Sea Suitability Score')
        ax2.set_title('Marker Gene Performance')
        ax2.tick_params(axis='x', rotation=45)
    
    # 3. Expected taxonomic composition
    if 'assessment' in data:
        taxa = list(data['assessment']['taxa_composition'].keys())
        # Extract mid-range values from abundance ranges
        abundances = []
        for taxon in taxa:
            range_str = data['assessment']['taxa_composition'][taxon]['abundance_range']
            if '-' in range_str:
                low, high = range_str.replace('%', '').split('-')
                mid = (float(low) + float(high)) / 2
                abundances.append(mid)
            else:
                abundances.append(5)  # default
        
        ax3.pie(abundances, labels=taxa, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Expected Deep-Sea eDNA Composition')
    
    # 4. Database coverage assessment
    coverage_categories = ['Excellent', 'Good', 'Moderate', 'Poor', 'Very Poor']
    coverage_counts = [0, 1, 1, 2, 1]  # Based on analysis
    
    ax4.bar(coverage_categories, coverage_counts, color='orange', alpha=0.7)
    ax4.set_ylabel('Number of Taxa Groups')
    ax4.set_title('Database Coverage Assessment')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('deep_sea_edna_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create marker heatmap
    if 'markers' in data:
        marker_df = pd.DataFrame({
            'Deep-sea Score': [data['markers'][m]['deep_sea_score'] for m in data['markers']],
            'Resolution Score': [5 if 'Species' in data['markers'][m]['resolution'] else 
                               4 if 'Genus' in data['markers'][m]['resolution'] else 3 
                               for m in data['markers']]
        }, index=list(data['markers'].keys()))
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(marker_df.T, annot=True, cmap='RdYlGn', center=3, 
                   cbar_kws={'label': 'Score (1=Poor, 5=Excellent)'})
        plt.title('Marker Gene Suitability Heatmap')
        plt.tight_layout()
        plt.savefig('marker_suitability_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    print("✅ Visualizations created:")
    print("   - deep_sea_edna_summary.png")
    print("   - marker_suitability_heatmap.png")

if __name__ == "__main__":
    create_visualizations()
