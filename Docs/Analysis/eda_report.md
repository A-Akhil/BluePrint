# NCBI BLAST Database Collection - Comprehensive EDA Report

## Executive Summary

**Total Dataset Size**: 3.3TB across 7917 files
**Database Count**: 70 distinct databases
**Multi-volume Databases**: 35

## Key Findings

### 1. Database Scale and Structure
- **nt**: 2203 volumes, 715.0 GB
- **nr**: 1149 volumes, 707.5 GB
- **nt_euk**: 1164 volumes, 565.2 GB
- **ref_euk_rep_genomes**: 978 volumes, 452.3 GB
- **refseq_protein**: 324 volumes, 258.7 GB

### 2. Marine eDNA Relevance Ranking
**Tier 1 (Highest Priority)**:
- nt_euk
- ref_euk_rep_genomes
- refseq_rna

**Tier 2 (Secondary Priority)**:
- nt
- refseq_protein

## Recommendations

1. **Start with nt_euk**: Largest eukaryotic-specific database
2. **Add rRNA markers**: 18S and 28S fungal sequences for phylogenetic analysis
3. **Consider RefSeq RNA**: High-quality curated sequences
4. **Computational strategy**: Begin with minimal set, expand based on results
