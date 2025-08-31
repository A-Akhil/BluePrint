// Main data index - combines all mock data sources
import zonesData from './zones.js';
import sequencesData from './sequences.js';
import taxonomyData from './taxonomy.js';
import searchSimulationData from './searchSimulation.js';

export const mockData = {
  zones: zonesData.zones,
  zone_analytics: zonesData.zone_analytics,
  sequences: sequencesData.detailed_sequences,
  sequence_summary: sequencesData.summary,
  taxonomy: taxonomyData.taxonomic_hierarchy,
  biodiversity: taxonomyData.biodiversity_metrics,
  abundance: taxonomyData.abundance_data,
  search_simulation: searchSimulationData.search_scenarios[0],
  performance_comparison: searchSimulationData.performance_comparison,
  search_stats: searchSimulationData.search_statistics
};

// Sample locations for mapping
export const sampleLocations = [
  {
    id: "site_001",
    name: "Abyssal Plain Alpha",
    latitude: -35.2156,
    longitude: 142.1234,
    depth_m: 4200,
    temperature_c: 2.1,
    samples_collected: 45,
    sequences_found: 1247,
    novel_sequences: 89,
    last_sampled: "2024-08-15"
  },
  {
    id: "site_002", 
    name: "Seamount Beta",
    latitude: -12.3456,
    longitude: 150.4567,
    depth_m: 3800,
    temperature_c: 3.4,
    samples_collected: 32,
    sequences_found: 892,
    novel_sequences: 67,
    last_sampled: "2024-07-22"
  },
  {
    id: "site_003",
    name: "Hydrothermal Vent Gamma", 
    latitude: -8.9876,
    longitude: 125.6789,
    depth_m: 2950,
    temperature_c: 8.7,
    samples_collected: 28,
    sequences_found: 1456,
    novel_sequences: 134,
    last_sampled: "2024-08-03"
  },
  {
    id: "site_004",
    name: "Deep Trench Delta",
    latitude: -25.4321,
    longitude: 160.9876,
    depth_m: 5400,
    temperature_c: 1.8,
    samples_collected: 18,
    sequences_found: 567,
    novel_sequences: 45,
    last_sampled: "2024-06-30"
  }
];

// Helper functions for data manipulation
export const dataUtils = {
  getZoneById: (zoneId) => mockData.zones.find(z => z.id === zoneId),
  
  getSequencesByZone: (zoneId) => 
    mockData.sequences.filter(seq => seq.zone_id === zoneId),
  
  getNovelSequences: () => 
    mockData.sequences.filter(seq => seq.novel),
  
  getHighConfidenceSequences: () =>
    mockData.sequences.filter(seq => seq.confidence > 0.8),
  
  getSequencesByTaxon: (taxon) =>
    mockData.sequences.filter(seq => seq.predicted_taxon.includes(taxon)),
  
  calculateDiversityMetrics: (sequences) => {
    const taxa = [...new Set(sequences.map(s => s.predicted_taxon))];
    const totalSeqs = sequences.length;
    
    // Shannon diversity index calculation
    const shannon = taxa.reduce((sum, taxon) => {
      const count = sequences.filter(s => s.predicted_taxon === taxon).length;
      const p = count / totalSeqs;
      return sum - (p * Math.log(p));
    }, 0);
    
    return {
      taxa_count: taxa.length,
      shannon_index: shannon,
      total_sequences: totalSeqs
    };
  },
  
  getTopTaxa: (limit = 10) =>
    mockData.abundance.slice(0, limit),
  
  searchSequences: (query, filters = {}) => {
    let results = mockData.sequences;
    
    if (query) {
      results = results.filter(seq => 
        seq.predicted_taxon.toLowerCase().includes(query.toLowerCase()) ||
        seq.id.toLowerCase().includes(query.toLowerCase()) ||
        seq.functional_annotation.toLowerCase().includes(query.toLowerCase())
      );
    }
    
    if (filters.novel !== undefined) {
      results = results.filter(seq => seq.novel === filters.novel);
    }
    
    if (filters.minConfidence) {
      results = results.filter(seq => seq.confidence >= filters.minConfidence);
    }
    
    if (filters.taxon) {
      results = results.filter(seq => seq.predicted_taxon.includes(filters.taxon));
    }
    
    if (filters.zoneId) {
      results = results.filter(seq => seq.zone_id === filters.zoneId);
    }
    
    return results;
  }
};

export default mockData;
