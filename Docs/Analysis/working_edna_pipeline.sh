#!/bin/bash
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
