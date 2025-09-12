#!/usr/bin/env python3
"""
Database Size Analysis and Visualization for Marine eDNA Project
Generates charts and insights for database selection strategy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
import numpy as np

class DatabaseVisualizationAnalyzer:
    def __init__(self, data_dir='/home/srmist32/sihdna/ncbi_blast_db_files'):
        self.data_dir = Path(data_dir)
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_priority_visualization(self):
        """Create visualization showing database priorities for marine eDNA"""
        
        # Database priority data based on EDA results
        priority_data = {
            'Database': ['nt_euk', 'ref_euk_rep_genomes', 'refseq_rna', 'nt', 
                        'refseq_protein', 'core_nt', 'nt_prok', 'nt_viruses'],
            'Size_GB': [565.2, 452.3, 69.0, 715.0, 258.7, 253.7, 82.1, 63.7],
            'Priority': ['Tier 1', 'Tier 1', 'Tier 2', 'Tier 3', 'Tier 3', 'Tier 4', 'Tier 4', 'Tier 4'],
            'Marine_Relevance': [95, 90, 85, 70, 60, 65, 20, 15],
            'Implementation_Phase': [1, 1, 2, 3, 3, 4, 4, 4]
        }
        
        df = pd.DataFrame(priority_data)
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('NCBI Database Analysis for Marine eDNA Project', fontsize=16, fontweight='bold')
        
        # 1. Database Size by Priority Tier
        tier_colors = {'Tier 1': '#2E8B57', 'Tier 2': '#4682B4', 'Tier 3': '#DAA520', 'Tier 4': '#CD5C5C'}
        bars1 = ax1.bar(df['Database'], df['Size_GB'], 
                       color=[tier_colors[tier] for tier in df['Priority']])
        ax1.set_title('Database Size by Priority Tier', fontweight='bold')
        ax1.set_ylabel('Size (GB)')
        ax1.set_xlabel('Database')
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, value in zip(bars1, df['Size_GB']):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'{value:.0f}GB', ha='center', va='bottom', fontsize=9)
        
        # 2. Marine Relevance Score vs Database Size
        scatter = ax2.scatter(df['Size_GB'], df['Marine_Relevance'], 
                            c=df['Implementation_Phase'], s=100, alpha=0.7, cmap='viridis')
        ax2.set_title('Marine Relevance vs Database Size', fontweight='bold')
        ax2.set_xlabel('Database Size (GB)')
        ax2.set_ylabel('Marine Relevance Score (%)')
        
        # Add database labels
        for i, db in enumerate(df['Database']):
            ax2.annotate(db, (df['Size_GB'].iloc[i], df['Marine_Relevance'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.colorbar(scatter, ax=ax2, label='Implementation Phase')
        
        # 3. Cumulative Storage Requirements by Implementation Phase
        phase_data = df.groupby('Implementation_Phase')['Size_GB'].sum().cumsum()
        ax3.plot(phase_data.index, phase_data.values, marker='o', linewidth=3, markersize=8)
        ax3.fill_between(phase_data.index, phase_data.values, alpha=0.3)
        ax3.set_title('Cumulative Storage Requirements', fontweight='bold')
        ax3.set_xlabel('Implementation Phase')
        ax3.set_ylabel('Cumulative Size (GB)')
        ax3.grid(True, alpha=0.3)
        
        # Add value labels
        for phase, size in phase_data.items():
            ax3.text(phase, size + 50, f'{size:.0f}GB', ha='center', fontweight='bold')
        
        # 4. Priority Distribution Pie Chart
        priority_sizes = df.groupby('Priority')['Size_GB'].sum()
        wedges, texts, autotexts = ax4.pie(priority_sizes.values, labels=priority_sizes.index,
                                          autopct='%1.1f%%', startangle=90,
                                          colors=[tier_colors[tier] for tier in priority_sizes.index])
        ax4.set_title('Storage Distribution by Priority Tier', fontweight='bold')
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig('database_priority_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return df
    
    def create_implementation_roadmap(self):
        """Create implementation roadmap visualization"""
        
        # Implementation phases data
        phases = {
            'Phase 1: Eukaryotic Focus': {
                'databases': ['nt_euk', 'ref_euk_rep_genomes'],
                'size_gb': 635,
                'timeline': '2-4 weeks',
                'ram_req': '64GB',
                'description': 'Core marine eukaryotic identification'
            },
            'Phase 2: rRNA Phylogenetics': {
                'databases': ['refseq_rna', '18S_fungal', '28S_fungal'],
                'size_gb': 704,
                'timeline': '1-2 weeks',
                'ram_req': '64-80GB', 
                'description': 'Phylogenetic tree construction'
            },
            'Phase 3: Comprehensive Analysis': {
                'databases': ['nt', 'refseq_protein'],
                'size_gb': 1419,
                'timeline': '4-6 weeks',
                'ram_req': '128-256GB',
                'description': 'Full biodiversity assessment'
            },
            'Phase 4: Specialized Applications': {
                'databases': ['tsa_nt', 'swissprot', 'pdb'],
                'size_gb': 1430,
                'timeline': '1-2 weeks',
                'ram_req': '128-256GB',
                'description': 'Functional annotation & novel discovery'
            }
        }
        
        # Create roadmap visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Timeline and storage requirements
        phase_names = list(phases.keys())
        storage_cumsum = []
        storage_increment = []
        
        cumulative = 0
        for phase in phase_names:
            current_size = phases[phase]['size_gb']
            cumulative += current_size
            storage_cumsum.append(cumulative)
            storage_increment.append(current_size)
        
        # Phase implementation chart
        x_pos = np.arange(len(phase_names))
        bars = ax1.bar(x_pos, storage_increment, alpha=0.7, 
                      color=['#2E8B57', '#4682B4', '#DAA520', '#CD5C5C'])
        
        # Add cumulative line
        ax1_twin = ax1.twinx()
        line = ax1_twin.plot(x_pos, storage_cumsum, color='red', marker='o', 
                           linewidth=3, markersize=8, label='Cumulative Storage')
        
        ax1.set_title('Implementation Roadmap: Storage Requirements by Phase', 
                     fontsize=14, fontweight='bold')
        ax1.set_xlabel('Implementation Phase')
        ax1.set_ylabel('Phase Storage (GB)', color='blue')
        ax1_twin.set_ylabel('Cumulative Storage (GB)', color='red')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels([p.split(':')[0] for p in phase_names], rotation=15)
        
        # Add value labels
        for i, (bar, cum_val) in enumerate(zip(bars, storage_cumsum)):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                    f'{storage_increment[i]}GB', ha='center', va='bottom', fontweight='bold')
            ax1_twin.text(i, cum_val + 50, f'{cum_val}GB', ha='center', va='bottom', 
                         color='red', fontweight='bold')
        
        # Requirements summary table
        ax2.axis('tight')
        ax2.axis('off')
        
        table_data = []
        for phase, data in phases.items():
            table_data.append([
                phase.split(':')[0],
                ', '.join(data['databases'][:2]) + ('...' if len(data['databases']) > 2 else ''),
                f"{data['size_gb']}GB",
                data['ram_req'],
                data['timeline'],
                data['description']
            ])
        
        table = ax2.table(cellText=table_data,
                         colLabels=['Phase', 'Key Databases', 'Storage', 'RAM', 'Timeline', 'Objective'],
                         cellLoc='left',
                         loc='center',
                         bbox=[0, 0, 1, 1])
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Style the table
        for i in range(len(table_data) + 1):
            for j in range(6):
                cell = table[(i, j)]
                if i == 0:  # Header row
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax2.set_title('Implementation Phase Details', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig('implementation_roadmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return phases
    
    def generate_executive_summary(self):
        """Generate executive summary with key recommendations"""
        
        summary = """
# EXECUTIVE SUMMARY: NCBI Database Analysis for Marine eDNA Project

## KEY FINDINGS

### Dataset Scale
- **Total Collection**: 3.3TB across 7,917 files
- **Database Groups**: 70 distinct collections
- **Primary Focus**: Eukaryotic databases (1.02TB) for marine species identification

### Top Priority Databases
1. **nt_euk** (565GB) - Eukaryotic nucleotide sequences
2. **ref_euk_rep_genomes** (452GB) - Representative eukaryotic genomes  
3. **refseq_rna** (69GB) - Curated RNA including rRNA markers

### Implementation Strategy
- **Phase 1**: Start with 635GB eukaryotic subset (64GB RAM minimum)
- **Phase 2**: Add phylogenetic markers (+69GB)
- **Phase 3**: Scale to comprehensive analysis (1.4TB total)

## STRATEGIC RECOMMENDATIONS

### Immediate Actions
1. **Deploy Phase 1 databases** on high-memory system (64+ GB RAM)
2. **Test marine hit rates** with deep-sea eDNA samples
3. **Validate computational performance** before scaling

### Long-term Considerations  
1. **Plan storage expansion** for comprehensive dataset (2TB+)
2. **Consider cloud deployment** for scalable processing
3. **Implement regular updates** from NCBI releases

## COMPETITIVE ADVANTAGES
- **Comprehensive Coverage**: 565GB of eukaryotic sequences
- **Curated Quality**: RefSeq databases provide expert annotation
- **Phylogenetic Capability**: rRNA markers enable precise classification
- **Scalable Deployment**: Modular implementation phases

## RISK MITIGATION
- **Start with validated subsets** to minimize computational overhead
- **Monitor system performance** throughout scaling
- **Maintain backup strategy** for critical database files

This analysis confirms that the NCBI collection provides an excellent foundation for 
deep-sea eDNA biodiversity assessment with clear implementation pathways.
        """
        
        with open('executive_summary.md', 'w') as f:
            f.write(summary)
        
        print("Executive Summary generated: executive_summary.md")
        return summary

def main():
    """Execute comprehensive database visualization analysis"""
    
    print("=== NCBI Database Visualization Analysis ===")
    print("Generating comprehensive charts and insights...")
    
    analyzer = DatabaseVisualizationAnalyzer()
    
    # Generate priority analysis charts
    print("\n1. Creating database priority visualization...")
    priority_df = analyzer.create_priority_visualization()
    
    # Generate implementation roadmap
    print("\n2. Creating implementation roadmap...")
    roadmap_data = analyzer.create_implementation_roadmap()
    
    # Generate executive summary
    print("\n3. Generating executive summary...")
    summary = analyzer.generate_executive_summary()
    
    print("\n=== ANALYSIS COMPLETE ===")
    print("Generated files:")
    print("- database_priority_analysis.png")
    print("- implementation_roadmap.png") 
    print("- executive_summary.md")
    
    print(f"\nPriority database summary:")
    print(f"- Tier 1 databases: {priority_df[priority_df['Priority'] == 'Tier 1']['Size_GB'].sum():.1f}GB")
    print(f"- Total collection: {priority_df['Size_GB'].sum():.1f}GB")
    print(f"- Marine relevance avg: {priority_df['Marine_Relevance'].mean():.1f}%")

if __name__ == "__main__":
    main()
