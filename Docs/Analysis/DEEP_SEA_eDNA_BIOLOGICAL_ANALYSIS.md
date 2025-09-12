# BIOLOGICAL ANALYSIS: NCBI DATABASES FOR DEEP-SEA eDNA

## Problem Focus
**Challenge**: Identifying eukaryotic taxa from deep-sea eDNA samples
**Location**: Abyssal plains, hydrothermal vents, seamounts
**Target**: Protists, cnidarians, metazoans from deep-sea environments

## ESSENTIAL DATABASES FOR YOUR PROBLEM

### 🎯 TIER 1 - PRIMARY (MUST HAVE)
1. **SSU_eukaryote_rRNA-nucl** - 18S rRNA universal marker
   - Expected success: 60-80% of deep-sea eDNA sequences
   - Target: All eukaryotes (protists dominant)

### 🎯 TIER 2 - SECONDARY (IMPORTANT)
2. **LSU_eukaryote_rRNA-nucl** - 28S rRNA phylogenetic placement
   - Expected success: 40-60% additional assignments
   - Target: Novel lineage placement

### 🎯 TIER 3 - SUPPLEMENTARY
3. **ITS_eukaryote_sequences-nucl** - Species-level identification
   - Expected success: 10-30% (high confidence)
   - Target: Fungi and some protists

### 🎯 TIER 4 - COMPREHENSIVE BACKUP
4. **nt_euk-nucl** - All eukaryotic sequences
   - Expected success: 5-15% additional
   - Warning: Computationally expensive

## CRITICAL GAPS
- **20-40% sequences will be unassigned** due to novel deep-sea taxa
- **AI/ML approaches required** for novel lineage discovery
- **Phylogenetic placement essential** for sequences <80% identity

## PYTHON + BLAST INTEGRATION
```python
# Primary analysis with BioPython
from Bio.Blast import NCBIXML
from Bio import SeqIO
import subprocess

# Step 1: 18S analysis
subprocess.run(['blastn', '-db', 'SSU_eukaryote_rRNA-nucl', 
               '-query', 'edna_sequences.fasta',
               '-out', 'primary_results.xml', '-outfmt', '5'])
```
