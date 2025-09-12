#!/bin/bash
# Deep-Sea eDNA Analysis Pipeline

# Step 1: Protist diversity
echo 'Running Step 1: Protist diversity'
blastn -db SSU_eukaryote_rRNA-nucl -query edna.fasta -out step1_results.xml -outfmt 5

# Step 2: Phylogenetic placement
echo 'Running Step 2: Phylogenetic placement'
blastn -db LSU_eukaryote_rRNA-nucl -query unassigned_step1.fasta -out step2_results.xml -outfmt 5

# Step 3: Species identification
echo 'Running Step 3: Species identification'
blastn -db ITS_eukaryote_sequences-nucl -query unassigned_step2.fasta -out step3_results.xml -outfmt 5

# Step 4: Comprehensive search
echo 'Running Step 4: Comprehensive search'
blastn -db nt_euk-nucl -query unassigned_step3.fasta -out step4_results.xml -outfmt 5

