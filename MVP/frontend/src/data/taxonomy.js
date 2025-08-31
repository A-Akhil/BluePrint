// Taxonomic hierarchy and biodiversity data
export const taxonomyData = {
  taxonomic_hierarchy: {
    "Eukaryota": {
      count: 4250,
      children: {
        "SAR": {
          count: 1680,
          children: {
            "Stramenopiles": {
              count: 890,
              children: {
                "Chrysophyceae": { count: 456 },
                "Bacillariophyta": { count: 234 },
                "Phaeophyceae": { count: 200 }
              }
            },
            "Alveolata": {
              count: 567,
              children: {
                "Dinoflagellata": { count: 345 },
                "Ciliophora": { count: 122 },
                "Apicomplexa": { count: 100 }
              }
            },
            "Rhizaria": {
              count: 223,
              children: {
                "Foraminifera": { count: 134 },
                "Radiolaria": { count: 89 }
              }
            }
          }
        },
        "Archaeplastida": {
          count: 892,
          children: {
            "Chlorophyta": {
              count: 567,
              children: {
                "Chlorophyceae": { count: 345 },
                "Trebouxiophyceae": { count: 222 }
              }
            },
            "Rhodophyta": {
              count: 325,
              children: {
                "Florideophyceae": { count: 200 },
                "Bangiophyceae": { count: 125 }
              }
            }
          }
        },
        "Opisthokonta": {
          count: 1134,
          children: {
            "Metazoa": {
              count: 678,
              children: {
                "Cnidaria": { count: 234 },
                "Arthropoda": { count: 189 },
                "Mollusca": { count: 156 },
                "Nematoda": { count: 99 }
              }
            },
            "Fungi": {
              count: 456,
              children: {
                "Ascomycota": { count: 278 },
                "Basidiomycota": { count: 178 }
              }
            }
          }
        },
        "Excavata": {
          count: 544,
          children: {
            "Euglenozoa": {
              count: 234,
              children: {
                "Euglenida": { count: 134 },
                "Kinetoplastida": { count: 100 }
              }
            },
            "Metamonada": {
              count: 310,
              children: {
                "Diplomonadida": { count: 189 },
                "Parabasalia": { count: 121 }
              }
            }
          }
        }
      }
    },
    "Unknown": {
      count: 750,
      children: {
        "Novel_Group_1": { count: 234 },
        "Novel_Group_2": { count: 189 },
        "Novel_Group_3": { count: 156 },
        "Unclassified": { count: 171 }
      }
    }
  },

  biodiversity_metrics: {
    shannon_index: 3.247,
    simpson_index: 0.891,
    chao1_estimate: 6890,
    ace_estimate: 7234,
    total_sequences: 5000,
    total_taxa: 147,
    novel_sequences: 750,
    novel_taxa: 23,
    
    confidence_distribution: {
      "high_confidence (>0.8)": 2156,
      "medium_confidence (0.5-0.8)": 1834,
      "low_confidence (<0.5)": 1010
    },
    
    functional_distribution: {
      "Photosynthetic protist": 1234,
      "Heterotrophic flagellate": 892,
      "Marine predator": 567,
      "Filter feeder": 445,
      "Primary producer": 389,
      "Detritus feeder": 334,
      "Symbiotic organism": 289,
      "Plankton": 456,
      "Benthic organism": 223,
      "Unknown function": 171
    },

    depth_distribution: {
      "1000-2000m": 1567,
      "2000-3000m": 1834,
      "3000-4000m": 1234,
      "4000m+": 365
    },

    temporal_trends: [
      { month: "Jan 2024", sequences: 412, novel: 67, shannon: 3.12 },
      { month: "Feb 2024", sequences: 445, novel: 72, shannon: 3.18 },
      { month: "Mar 2024", sequences: 434, novel: 69, shannon: 3.15 },
      { month: "Apr 2024", sequences: 467, novel: 78, shannon: 3.23 },
      { month: "May 2024", sequences: 489, novel: 82, shannon: 3.28 },
      { month: "Jun 2024", sequences: 501, novel: 85, shannon: 3.31 },
      { month: "Jul 2024", sequences: 523, novel: 89, shannon: 3.35 },
      { month: "Aug 2024", sequences: 556, novel: 94, shannon: 3.42 },
      { month: "Sep 2024", sequences: 578, novel: 98, shannon: 3.47 },
      { month: "Oct 2024", sequences: 591, novel: 102, shannon: 3.52 },
      { month: "Nov 2024", sequences: 602, novel: 106, shannon: 3.56 },
      { month: "Dec 2024", sequences: 618, novel: 112, shannon: 3.61 }
    ]
  },

  abundance_data: Array.from({ length: 50 }, (_, i) => ({
    taxon: `Species_${i + 1}`,
    count: Math.floor(Math.random() * 200) + 10,
    percentage: Math.random() * 15 + 1,
    novel: Math.random() < 0.2,
    confidence: Math.random() * 0.4 + 0.6
  })).sort((a, b) => b.count - a.count)
};

export default taxonomyData;
