#!/usr/bin/env python3
"""
BIOLOGICAL EDA FOR DEEP-SEA eDNA TAXONOMY IDENTIFICATION
Focus: Which databases contain eukaryotic sequences suitable for deep-sea biodiversity assessment
Problem: Poor representation of deep-sea organisms in reference databases
Goal: Identify optimal databases for 18S rRNA, COI, and other eDNA markers
"""

import os
import json
import sqlite3
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import re
import warnings
warnings.filterwarnings('ignore')

class BiologicalEDA:
    def __init__(self, base_path='ncbi_blast_db_files'):
        self.base_path = base_path
        self.problem_focus = "deep-sea eukaryotic eDNA taxonomy identification"
        self.target_markers = ['18S', 'COI', '28S', 'ITS', 'SSU', 'LSU']
        self.target_taxa = ['eukaryotes', 'protists', 'cnidarians', 'metazoans']
        self.biological_findings = []
        self.database_suitability = {}
        
        print("=== BIOLOGICAL EDA FOR DEEP-SEA eDNA ANALYSIS ===")
        print(f"Problem Focus: {self.problem_focus}")
        print(f"Target Markers: {', '.join(self.target_markers)}")
        print(f"Target Taxa: {', '.join(self.target_taxa)}")
    
    def log_biological_finding(self, finding, taxa_relevance="", marker_suitability="", deep_sea_coverage=""):
        self.biological_findings.append({
            'finding': finding,
            'taxa_relevance': taxa_relevance,
            'marker_suitability': marker_suitability,
            'deep_sea_coverage': deep_sea_coverage
        })
        print(f"🔬 BIOLOGICAL FINDING: {finding}")
        if taxa_relevance:
            print(f"   🦠 Taxa Relevance: {taxa_relevance}")
        if marker_suitability:
            print(f"   🧬 Marker Suitability: {marker_suitability}")
        if deep_sea_coverage:
            print(f"   🌊 Deep-sea Coverage: {deep_sea_coverage}")
    
    def analyze_edna_marker_databases(self):
        """Analyze databases specifically for eDNA marker genes"""
        print(f"\n{'='*80}")
        print("ANALYZING eDNA MARKER GENE DATABASES")
        print(f"{'='*80}")
        
        # Load metadata
        marker_databases = {}
        metadata_files = [f for f in os.listdir(self.base_path) if f.endswith('-metadata.json')]
        
        for meta_file in metadata_files:
            try:
                with open(os.path.join(self.base_path, meta_file), 'r') as f:
                    data = json.load(f)
                
                db_name = meta_file.replace('-metadata.json', '')
                
                # Check if this is an eDNA-relevant database
                edna_relevance = self._assess_edna_relevance(db_name, data.get('description', ''))
                
                if edna_relevance['is_relevant']:
                    marker_databases[db_name] = {
                        'sequences': data.get('number-of-sequences', 0),
                        'letters': data.get('number-of-letters', 0),
                        'description': data.get('description', ''),
                        'markers': edna_relevance['markers'],
                        'taxa_focus': edna_relevance['taxa_focus'],
                        'avg_length': data.get('number-of-letters', 0) / max(data.get('number-of-sequences', 1), 1)
                    }
                    
            except Exception as e:
                print(f"Error loading {meta_file}: {e}")
        
        # Analyze each marker database for eDNA suitability
        for db_name, db_info in marker_databases.items():
            self._analyze_marker_database_biology(db_name, db_info)
        
        return marker_databases
    
    def _assess_edna_relevance(self, db_name, description):
        """Assess if database is relevant for eDNA analysis"""
        name_lower = db_name.lower()
        desc_lower = description.lower()
        
        # eDNA marker genes
        marker_patterns = {
            '18S': ['18s', 'ssu.*eukaryote', 'small.*subunit.*eukaryote'],
            '28S': ['28s', 'lsu.*eukaryote', 'large.*subunit.*eukaryote'],
            'COI': ['coi', 'cox1', 'cytochrome.*oxidase'],
            'ITS': ['its', 'internal.*transcribed'],
            'SSU': ['ssu', 'small.*subunit'],
            'LSU': ['lsu', 'large.*subunit'],
            '16S': ['16s', 'ssu.*prokaryote']
        }
        
        found_markers = []
        for marker, patterns in marker_patterns.items():
            for pattern in patterns:
                if re.search(pattern, name_lower) or re.search(pattern, desc_lower):
                    found_markers.append(marker)
                    break
        
        # Taxa relevance for eDNA
        taxa_patterns = {
            'eukaryotes': ['eukaryot', 'protist', 'fungi', 'metazoa', 'plant'],
            'marine': ['marine', 'ocean', 'sea', 'coastal'],
            'microbes': ['microbial', 'prokaryot', 'bacteria', 'archaea']
        }
        
        taxa_focus = []
        for taxa, patterns in taxa_patterns.items():
            for pattern in patterns:
                if re.search(pattern, name_lower) or re.search(pattern, desc_lower):
                    taxa_focus.append(taxa)
                    break
        
        is_relevant = len(found_markers) > 0 or 'eukaryotes' in taxa_focus
        
        return {
            'is_relevant': is_relevant,
            'markers': found_markers,
            'taxa_focus': taxa_focus
        }
    
    def _analyze_marker_database_biology(self, db_name, db_info):
        """Analyze biological suitability of each marker database"""
        sequences = db_info['sequences']
        avg_length = db_info['avg_length']
        markers = db_info['markers']
        taxa_focus = db_info['taxa_focus']
        
        # Assess for 18S rRNA (primary eDNA eukaryotic marker)
        if any('18S' in marker or 'SSU' in marker for marker in markers) and 'eukaryotes' in taxa_focus:
            if 1400 <= avg_length <= 2000:
                suitability = "EXCELLENT - optimal length for 18S phylogeny"
            elif 800 <= avg_length <= 1400:
                suitability = "GOOD - suitable for 18S metabarcoding"
            else:
                suitability = "MODERATE - length may limit resolution"
            
            self.log_biological_finding(
                f"{db_name}: {sequences:,} 18S sequences for eukaryotic identification",
                "PRIMARY TARGET for protists, cnidarians, metazoans",
                suitability,
                "Critical for deep-sea eukaryotic diversity assessment"
            )
            
            self.database_suitability[db_name] = {
                'priority': 'HIGH',
                'use_case': '18S eukaryotic identification',
                'deep_sea_value': 'High - universal eukaryotic marker'
            }
        
        # Assess for 28S rRNA (complementary eukaryotic marker)
        elif any('28S' in marker or 'LSU' in marker for marker in markers) and 'eukaryotes' in taxa_focus:
            if 2000 <= avg_length <= 4000:
                suitability = "EXCELLENT - full-length 28S resolution"
            elif 600 <= avg_length <= 2000:
                suitability = "GOOD - partial 28S useful for identification"
            else:
                suitability = "MODERATE - length limitations"
            
            self.log_biological_finding(
                f"{db_name}: {sequences:,} 28S sequences for eukaryotic phylogeny",
                "SECONDARY TARGET for higher-level taxonomy",
                suitability,
                "Useful for deep-sea taxonomic placement"
            )
            
            self.database_suitability[db_name] = {
                'priority': 'MEDIUM',
                'use_case': '28S phylogenetic placement',
                'deep_sea_value': 'Medium - good for family/order level'
            }
        
        # Assess for ITS (species-level identification)
        elif 'ITS' in markers:
            if 200 <= avg_length <= 800:
                suitability = "EXCELLENT - optimal ITS length for species ID"
            else:
                suitability = "MODERATE - ITS length may be suboptimal"
            
            self.log_biological_finding(
                f"{db_name}: {sequences:,} ITS sequences for species identification",
                "SPECIES-LEVEL identification, especially fungi",
                suitability,
                "Limited deep-sea coverage but high resolution when available"
            )
            
            self.database_suitability[db_name] = {
                'priority': 'MEDIUM',
                'use_case': 'Species-level identification',
                'deep_sea_value': 'Variable - depends on deep-sea representation'
            }
        
        # Assess comprehensive eukaryotic databases
        elif 'eukaryotes' in taxa_focus and sequences > 10000000:  # Large eukaryotic database
            self.log_biological_finding(
                f"{db_name}: {sequences:,} eukaryotic sequences (comprehensive)",
                "BROAD COVERAGE - mixed markers and taxa",
                "Good backup for unassigned sequences",
                "May contain some deep-sea sequences but requires filtering"
            )
            
            self.database_suitability[db_name] = {
                'priority': 'MEDIUM',
                'use_case': 'Comprehensive eukaryotic search',
                'deep_sea_value': 'Low-Medium - broad but shallow coverage'
            }
        
        # Other databases
        else:
            priority = 'LOW'
            if sequences > 1000000:
                priority = 'LOW-MEDIUM'
            
            self.log_biological_finding(
                f"{db_name}: {sequences:,} sequences - {', '.join(markers) if markers else 'unclear markers'}",
                f"Taxa focus: {', '.join(taxa_focus) if taxa_focus else 'unclear'}",
                "Needs sequence-level analysis to assess suitability",
                "Unknown deep-sea representation"
            )
            
            self.database_suitability[db_name] = {
                'priority': priority,
                'use_case': 'Unclear - requires investigation',
                'deep_sea_value': 'Unknown'
            }
    
    def analyze_deep_sea_taxonomic_coverage(self):
        """Analyze what we know about deep-sea taxonomic coverage"""
        print(f"\n{'='*80}")
        print("DEEP-SEA TAXONOMIC COVERAGE ANALYSIS")
        print(f"{'='*80}")
        
        # Known challenges with deep-sea eDNA databases
        deep_sea_challenges = {
            'Depth bias': 'Most sequences from 0-200m; deep-sea (>200m) underrepresented',
            'Geographic bias': 'Atlantic/Pacific coastal regions overrepresented vs abyssal plains',
            'Taxonomic bias': 'Known taxa from accessible environments vs novel deep-sea lineages',
            'Marker bias': '18S available but COI limited for deep-sea metazoans',
            'Temporal bias': 'Recent collections may miss deep-sea seasonal patterns'
        }
        
        for challenge, description in deep_sea_challenges.items():
            self.log_biological_finding(
                f"Database limitation: {challenge}",
                description,
                "Impacts eDNA classification accuracy",
                "Requires phylogenetic placement for novel sequences"
            )
        
        # Expected taxonomic groups in deep-sea eDNA
        expected_deep_sea_taxa = {
            'Protists': {
                'groups': ['Radiolaria', 'Foraminifera', 'Ciliates', 'Flagellates'],
                'marker': '18S rRNA',
                'abundance': 'High in sediment and water column',
                'database_coverage': 'Moderate - coastal species well represented'
            },
            'Cnidarians': {
                'groups': ['Deep-sea corals', 'Hydrozoa', 'Scyphozoa'],
                'marker': '18S rRNA, COI',
                'abundance': 'Moderate around seamounts/hydrothermal vents',
                'database_coverage': 'Poor - most deep-sea species undescribed'
            },
            'Metazoans': {
                'groups': ['Nematodes', 'Copepods', 'Polychaetes', 'Bivalves'],
                'marker': '18S rRNA, COI, 28S',
                'abundance': 'High diversity in sediments',
                'database_coverage': 'Very poor - high endemism in deep-sea'
            },
            'Fungi': {
                'groups': ['Marine fungi', 'Yeasts'],
                'marker': 'ITS, 18S, 28S',
                'abundance': 'Present but low in deep-sea',
                'database_coverage': 'Poor - marine fungi understudied'
            }
        }
        
        for taxa, info in expected_deep_sea_taxa.items():
            self.log_biological_finding(
                f"Expected deep-sea taxa: {taxa}",
                f"Groups: {', '.join(info['groups'])}; Abundance: {info['abundance']}",
                f"Best markers: {info['marker']}",
                f"Database coverage: {info['database_coverage']}"
            )
        
        return expected_deep_sea_taxa
    
    def assess_database_combinations_for_edna(self):
        """Assess optimal database combinations for eDNA pipeline"""
        print(f"\n{'='*80}")
        print("OPTIMAL DATABASE COMBINATIONS FOR eDNA PIPELINE")
        print(f"{'='*80}")
        
        # Primary strategy: hierarchical approach
        strategies = {
            'Primary_18S_Strategy': {
                'databases': ['SSU_eukaryote_rRNA', '18S_fungal_sequences'],
                'rationale': '18S rRNA is universal eukaryotic marker',
                'sensitivity': 'High for protists, moderate for metazoans',
                'specificity': 'High phylogenetic signal',
                'computational_cost': 'Low',
                'deep_sea_suitability': 'Good - best available option'
            },
            'Secondary_28S_Strategy': {
                'databases': ['LSU_eukaryote_rRNA', '28S_fungal_sequences'],
                'rationale': '28S provides complementary phylogenetic information',
                'sensitivity': 'Moderate - fewer sequences available',
                'specificity': 'High for higher-level taxonomy',
                'computational_cost': 'Low',
                'deep_sea_suitability': 'Moderate - good for placement'
            },
            'Species_Level_Strategy': {
                'databases': ['ITS_eukaryote_sequences', 'ITS_RefSeq_Fungi'],
                'rationale': 'ITS provides species-level resolution',
                'sensitivity': 'Low - limited taxa with ITS',
                'specificity': 'Very high for fungi and some protists',
                'computational_cost': 'Low',
                'deep_sea_suitability': 'Poor - limited deep-sea representation'
            },
            'Comprehensive_Backup': {
                'databases': ['nt_euk', 'ref_euk_rep_genomes'],
                'rationale': 'Broad coverage for unassigned sequences',
                'sensitivity': 'Very high - all available sequences',
                'specificity': 'Variable - mixed markers',
                'computational_cost': 'Very high',
                'deep_sea_suitability': 'Low-Medium - needle in haystack'
            }
        }
        
        for strategy_name, strategy_info in strategies.items():
            self.log_biological_finding(
                f"Strategy: {strategy_name}",
                f"Rationale: {strategy_info['rationale']}",
                f"Sensitivity: {strategy_info['sensitivity']}; Specificity: {strategy_info['specificity']}",
                f"Deep-sea suitability: {strategy_info['deep_sea_suitability']}"
            )
        
        # Recommended pipeline
        recommended_pipeline = [
            "1. Primary: 18S rRNA databases (SSU_eukaryote_rRNA) - universal eukaryotic identification",
            "2. Secondary: 28S rRNA databases (LSU_eukaryote_rRNA) - phylogenetic placement", 
            "3. Species-level: ITS databases for high-confidence species ID",
            "4. Backup: Comprehensive eukaryotic databases for remaining sequences",
            "5. Phylogenetic placement: For sequences with low database similarity"
        ]
        
        self.log_biological_finding(
            "Recommended eDNA pipeline hierarchy",
            "Balances sensitivity, specificity, and computational efficiency",
            "Uses marker-specific databases in order of phylogenetic resolution",
            "Addresses deep-sea representation gaps with phylogenetic methods"
        )
        
        return strategies, recommended_pipeline
    
    def generate_biological_recommendations(self):
        """Generate specific biological recommendations for deep-sea eDNA"""
        print(f"\n{'='*80}")
        print("BIOLOGICAL RECOMMENDATIONS FOR DEEP-SEA eDNA ANALYSIS")
        print(f"{'='*80}")
        
        recommendations = {
            'Primary_Databases': [
                "SSU_eukaryote_rRNA-nucl: PRIMARY for 18S eukaryotic identification",
                "LSU_eukaryote_rRNA-nucl: SECONDARY for 28S phylogenetic placement",
                "ITS_eukaryote_sequences-nucl: TERTIARY for species-level identification"
            ],
            'Quality_Control': [
                "Filter 18S sequences: 1200-2000bp for full-length, 400-800bp for V4 region",
                "Filter 28S sequences: 1000-4000bp depending on target region",
                "Remove sequences with >5% N's or low complexity regions",
                "Apply minimum 70% query coverage for reliable assignments"
            ],
            'Deep_Sea_Adaptations': [
                "Use phylogenetic placement (EPA, pplacer) for sequences <80% identity",
                "Implement environmental clustering for potential novel taxa",
                "Cross-reference with depth/location metadata when available",
                "Flag sequences that cluster separately as potential new lineages"
            ],
            'Computational_Strategy': [
                "Start with 18S databases (fastest, most informative)",
                "Use 28S for sequences with poor 18S matches",
                "Reserve comprehensive databases for final unassigned sequences",
                "Implement parallel processing for large eDNA datasets"
            ],
            'Biological_Interpretation': [
                "Focus on protist diversity (highest abundance in deep-sea eDNA)",
                "Expect high proportion of unassigned metazoan sequences",
                "Validate cnidarian identifications (high deep-sea endemism)",
                "Consider geographic isolation effects on taxonomy"
            ]
        }
        
        for category, recs in recommendations.items():
            print(f"\n📋 {category.replace('_', ' ')}:")
            for i, rec in enumerate(recs, 1):
                print(f"   {i}. {rec}")
        
        return recommendations
    
    def save_biological_analysis(self):
        """Save biological analysis results"""
        results = {
            'problem_focus': self.problem_focus,
            'target_markers': self.target_markers,
            'target_taxa': self.target_taxa,
            'biological_findings': self.biological_findings,
            'database_suitability': self.database_suitability,
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        }
        
        with open('biological_eda_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 BIOLOGICAL ANALYSIS SAVED: biological_eda_results.json")
        return results
    
    def run_biological_eda(self):
        """Run complete biological EDA for deep-sea eDNA"""
        print("🧬 STARTING BIOLOGICAL EDA FOR DEEP-SEA eDNA ANALYSIS")
        
        # Analyze marker databases
        marker_dbs = self.analyze_edna_marker_databases()
        
        # Analyze deep-sea coverage
        taxa_coverage = self.analyze_deep_sea_taxonomic_coverage()
        
        # Assess database combinations
        strategies, pipeline = self.assess_database_combinations_for_edna()
        
        # Generate recommendations
        recommendations = self.generate_biological_recommendations()
        
        # Save results
        results = self.save_biological_analysis()
        
        print(f"\n{'='*80}")
        print("🎉 BIOLOGICAL EDA COMPLETE!")
        print(f"Found {len(self.biological_findings)} biological findings")
        print(f"Assessed {len(self.database_suitability)} databases for eDNA suitability")
        print("Results focused on DEEP-SEA EUKARYOTIC TAXONOMY IDENTIFICATION")
        print(f"{'='*80}")
        
        return results

if __name__ == "__main__":
    bio_eda = BiologicalEDA()
    results = bio_eda.run_biological_eda()
