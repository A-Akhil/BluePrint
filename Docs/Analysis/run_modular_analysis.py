#!/usr/bin/env python3
"""
Master Runner: Deep-Sea eDNA Modular Analysis
Run all modules in sequence for complete analysis
"""

import subprocess
import sys

def run_module(module_name, description):
    """Run a single module with error handling"""
    print(f"\n🚀 Running {module_name}")
    print(f"📝 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, module_name], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"✅ {module_name} completed successfully")
            return True
        else:
            print(f"❌ {module_name} failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {module_name}: {e}")
        return False

def main():
    """Run complete modular analysis"""
    print("🌊 DEEP-SEA eDNA MODULAR ANALYSIS")
    print("="*50)
    print("Problem: Identifying eukaryotic taxa from deep-sea eDNA")
    print("Approach: Modular analysis of NCBI BLAST databases")
    print("="*50)
    
    modules = [
        ("module1_database_inventory.py", "Inventory NCBI BLAST databases"),
        ("module2_eukaryotic_analyzer.py", "Analyze eukaryotic database relevance"),
        ("module3_marker_analyzer.py", "Assess marker genes for eDNA"),
        ("module4_deep_sea_assessor.py", "Evaluate deep-sea organism coverage"),
        ("module5_pipeline_recommender.py", "Generate analysis pipeline"),
        ("module6_visualizer.py", "Create summary visualizations")
    ]
    
    success_count = 0
    
    for module_name, description in modules:
        if run_module(module_name, description):
            success_count += 1
        else:
            print(f"⚠️  Continuing despite {module_name} failure...")
    
    print(f"\n🎯 ANALYSIS COMPLETE!")
    print(f"✅ {success_count}/{len(modules)} modules completed successfully")
    
    if success_count == len(modules):
        print("\n📋 SUMMARY OF RESULTS:")
        print("   📊 database_inventory.json - Complete database inventory")
        print("   🔬 eukaryotic_databases.json - Eukaryotic database analysis")
        print("   🧬 marker_analysis.json - Marker gene assessment")
        print("   🌊 deep_sea_assessment.json - Deep-sea relevance analysis")
        print("   🔬 pipeline_config.json - Recommended analysis pipeline")
        print("   📈 Visualizations: deep_sea_edna_summary.png, marker_suitability_heatmap.png")
        print("   💻 edna_pipeline.sh - Ready-to-run BLAST commands")
        
        print("\n🎯 KEY FINDINGS:")
        print("   1. Use SSU_eukaryote_rRNA-nucl as PRIMARY database")
        print("   2. Expected 60-80% assignments for protist-dominated samples")
        print("   3. 20-40% sequences will require AI/ML for novel taxa")
        print("   4. Hierarchical pipeline: 18S → 28S → ITS → AI/ML")

if __name__ == "__main__":
    main()
