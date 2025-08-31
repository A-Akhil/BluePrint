// Mock detailed sequence data
const generateSequence = (id, zoneId, index) => {
  const taxa = [
    "Protista sp. nov.",
    "Cnidaria sp.",
    "Foraminifera sp.",
    "Unknown deep-sea eukaryote",
    "Radiolaria sp.",
    "Dinoflagellata sp.",
    "Chrysophyceae sp.",
    "Metazoa sp. nov.",
    "Amoebozoa sp.",
    "Stramenopiles sp."
  ];
  
  const functionalRoles = [
    "Photosynthetic protist",
    "Heterotrophic flagellate", 
    "Marine predator",
    "Symbiotic organism",
    "Detritus feeder",
    "Plankton",
    "Benthic organism",
    "Filter feeder",
    "Primary producer",
    "Unknown function"
  ];

  const randomTaxon = taxa[Math.floor(Math.random() * taxa.length)];
  const isNovel = Math.random() < 0.15; // 15% novel sequences
  
  return {
    id,
    sequence_data: `ATCGTGATCGT${'ATCG'.repeat(Math.floor(Math.random() * 100) + 50)}`,
    length: Math.floor(Math.random() * 500) + 200,
    quality_score: Math.random() * 10 + 30,
    predicted_taxon: isNovel ? "Unknown deep-sea eukaryote" : randomTaxon,
    confidence: isNovel ? Math.random() * 0.4 + 0.1 : Math.random() * 0.4 + 0.6,
    novel: isNovel,
    functional_annotation: functionalRoles[Math.floor(Math.random() * functionalRoles.length)],
    zone_id: zoneId,
    embedding: Array.from({ length: 512 }, () => (Math.random() - 0.5) * 2),
    similarity_scores: {
      closest_known: Math.random() * 0.3 + 0.7,
      second_closest: Math.random() * 0.3 + 0.5,
      third_closest: Math.random() * 0.3 + 0.3
    },
    phylogenetic_position: isNovel ? 
      "Eukaryota;Unknown;Unknown;Unknown" : 
      `Eukaryota;${randomTaxon.split(' ')[0]};${randomTaxon.split(' ')[0]}_class;${randomTaxon}`,
    metadata: {
      sample_location: `Sample Site ${Math.floor(Math.random() * 20) + 1}`,
      depth_m: Math.floor(Math.random() * 3000) + 1000,
      temperature_c: Math.random() * 3 + 1,
      collection_date: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      ph: Math.random() * 1 + 7,
      salinity: Math.random() * 5 + 34,
      oxygen_ml_l: Math.random() * 2 + 1
    },
    analysis_metadata: {
      sequencing_platform: ["Illumina HiSeq", "Illumina NovaSeq", "PacBio"][Math.floor(Math.random() * 3)],
      read_count: Math.floor(Math.random() * 10000) + 1000,
      gc_content: Math.random() * 20 + 40,
      n50: Math.floor(Math.random() * 500) + 200,
      coverage: Math.random() * 50 + 10
    }
  };
};

// Generate 5000 detailed sequences across all zones
export const sequencesData = {
  detailed_sequences: Array.from({ length: 5000 }, (_, i) => {
    const zoneId = `zone_${String(Math.floor(i / 78) + 1).padStart(3, '0')}`;
    const seqId = `seq_${String(i + 1).padStart(6, '0')}`;
    return generateSequence(seqId, zoneId, i);
  }),
  
  // Summary statistics
  summary: {
    total_sequences: 5000,
    novel_sequences: 750,
    high_confidence: 3200,
    medium_confidence: 1400,
    low_confidence: 400,
    avg_length: 342,
    avg_quality: 35.2,
    avg_gc_content: 52.3
  }
};

export default sequencesData;
