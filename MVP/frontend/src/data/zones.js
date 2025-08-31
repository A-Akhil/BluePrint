// Mock data for 64 zones with representatives and performance metrics
export const zonesData = {
  zones: Array.from({ length: 64 }, (_, i) => ({
    id: `zone_${String(i + 1).padStart(3, '0')}`,
    representative: {
      id: `repr_${String(i + 1).padStart(3, '0')}`,
      embedding: Array.from({ length: 512 }, () => (Math.random() - 0.5) * 2)
    },
    sequences: Array.from({ length: Math.floor(Math.random() * 8000) + 2000 }, (_, j) => 
      `seq_${String(i + 1).padStart(3, '0')}_${String(j + 1).padStart(4, '0')}`
    ),
    taxa_distribution: {
      "Protista": Math.floor(Math.random() * 150) + 20,
      "Cnidaria": Math.floor(Math.random() * 80) + 5,
      "Foraminifera": Math.floor(Math.random() * 60) + 5,
      "Metazoa": Math.floor(Math.random() * 40) + 2,
      "Unknown": Math.floor(Math.random() * 30) + 1
    },
    performance_metrics: {
      avg_search_time_ms: Math.random() * 20 + 5,
      hit_rate: Math.random() * 0.3 + 0.7,
      sequence_density: Math.floor(Math.random() * 6000) + 2000,
      novelty_rate: Math.random() * 0.4 + 0.1
    },
    location_info: {
      latitude: (Math.random() - 0.5) * 180,
      longitude: (Math.random() - 0.5) * 360,
      depth_range: [Math.floor(Math.random() * 2000) + 1000, Math.floor(Math.random() * 2000) + 3000],
      temperature_range: [Math.random() * 3 + 1, Math.random() * 2 + 4]
    }
  })),
  
  zone_analytics: {
    total_zones: 64,
    avg_sequences_per_zone: 4167,
    zone_efficiency_ranking: Array.from({ length: 64 }, (_, i) => ({
      zone_id: `zone_${String(i + 1).padStart(3, '0')}`,
      efficiency_score: Math.random() * 0.3 + 0.7,
      search_frequency: Math.floor(Math.random() * 1000) + 100,
      last_accessed: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
    })).sort((a, b) => b.efficiency_score - a.efficiency_score),
    
    search_performance: {
      avg_zones_searched: 3.2,
      avg_search_time_ms: 23,
      performance_improvement: "94% faster than exhaustive search",
      memory_usage_gb: 2.8,
      traditional_search_time_ms: 1250
    }
  }
};

export default zonesData;
