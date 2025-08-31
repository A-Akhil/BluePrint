// ZHNSW search simulation data
export const searchSimulationData = {
  // Example search scenarios
  search_scenarios: [
    {
      id: "search_001",
      query_sequence: {
        id: "uploaded_seq_001",
        sequence_data: "ATCGTGATCGTAATCGATCGATCGTAATCGATCGTAATCG",
        length: 298,
        type: "18S rRNA"
      },
      zhnsw_process: {
        step1_zone_comparison: {
          total_zones: 64,
          zones_compared: 64,
          time_ms: 2.3,
          top_zones: [
            { zone_id: "zone_012", similarity: 0.94, representative_distance: 0.087 },
            { zone_id: "zone_034", similarity: 0.91, representative_distance: 0.112 },
            { zone_id: "zone_007", similarity: 0.89, representative_distance: 0.134 },
            { zone_id: "zone_045", similarity: 0.86, representative_distance: 0.156 },
            { zone_id: "zone_023", similarity: 0.83, representative_distance: 0.178 }
          ]
        },
        step2_zone_selection: {
          strategy: "heuristic_based",
          zones_selected: ["zone_012", "zone_034", "zone_007"],
          selection_threshold: 0.85,
          zones_skipped: 61,
          time_ms: 0.8
        },
        step3_parallel_search: {
          searches: [
            {
              zone_id: "zone_012",
              sequences_searched: 4250,
              top_matches: [
                { seq_id: "seq_012_1847", similarity: 0.96, taxon: "Protista sp. nov." },
                { seq_id: "seq_012_0234", similarity: 0.94, taxon: "Protista sp." },
                { seq_id: "seq_012_3456", similarity: 0.92, taxon: "Protista sp." }
              ],
              time_ms: 12.4
            },
            {
              zone_id: "zone_034", 
              sequences_searched: 3890,
              top_matches: [
                { seq_id: "seq_034_0892", similarity: 0.93, taxon: "Dinoflagellata sp." },
                { seq_id: "seq_034_1234", similarity: 0.91, taxon: "Dinoflagellata sp." },
                { seq_id: "seq_034_2567", similarity: 0.89, taxon: "Stramenopiles sp." }
              ],
              time_ms: 11.2
            },
            {
              zone_id: "zone_007",
              sequences_searched: 4100,
              top_matches: [
                { seq_id: "seq_007_1567", similarity: 0.91, taxon: "Chrysophyceae sp." },
                { seq_id: "seq_007_0890", similarity: 0.88, taxon: "Stramenopiles sp." },
                { seq_id: "seq_007_2134", similarity: 0.86, taxon: "Chrysophyceae sp." }
              ],
              time_ms: 13.1
            }
          ],
          total_sequences_searched: 12240,
          parallel_time_ms: 13.1, // Max of parallel searches
          total_sequences_skipped: 307760 // ~320k total - 12k searched
        },
        step4_result_merging: {
          all_candidates: 9,
          final_top_k: 5,
          time_ms: 1.2,
          final_results: [
            { seq_id: "seq_012_1847", similarity: 0.96, taxon: "Protista sp. nov.", zone: "zone_012", confidence: 0.92 },
            { seq_id: "seq_012_0234", similarity: 0.94, taxon: "Protista sp.", zone: "zone_012", confidence: 0.89 },
            { seq_id: "seq_034_0892", similarity: 0.93, taxon: "Dinoflagellata sp.", zone: "zone_034", confidence: 0.87 },
            { seq_id: "seq_012_3456", similarity: 0.92, taxon: "Protista sp.", zone: "zone_012", confidence: 0.85 },
            { seq_id: "seq_034_1234", similarity: 0.91, taxon: "Dinoflagellata sp.", zone: "zone_034", confidence: 0.83 }
          ]
        }
      },
      performance_metrics: {
        total_zhnsw_time_ms: 17.6,
        traditional_exhaustive_time_ms: 1847,
        speedup_factor: 105,
        memory_usage_mb: 124,
        traditional_memory_mb: 2890,
        accuracy_maintained: 0.987,
        zones_searched_percentage: 4.7,
        sequences_searched_percentage: 3.8
      },
      classification_result: {
        predicted_taxon: "Protista sp. nov.",
        confidence: 0.92,
        novel_likelihood: 0.87,
        functional_annotation: "Photosynthetic protist",
        phylogenetic_position: "Eukaryota;SAR;Stramenopiles;Protista_novel",
        ecological_context: "Deep-sea planktonic organism, likely primary producer"
      }
    }
  ],

  // Performance comparison data
  performance_comparison: {
    traditional_approach: {
      name: "Exhaustive HNSW Search",
      avg_search_time_ms: 1650,
      memory_usage_gb: 12.4,
      accuracy: 1.0,
      scalability: "Poor for billion-scale",
      zones_searched: 64,
      sequences_searched: 320000
    },
    zhnsw_approach: {
      name: "Zonal HNSW (ZHNSW)",
      avg_search_time_ms: 18.7,
      memory_usage_gb: 2.8,
      accuracy: 0.987,
      scalability: "Excellent for billion-scale",
      avg_zones_searched: 3.2,
      avg_sequences_searched: 12500
    },
    improvements: {
      speed_improvement: "98.9% faster",
      memory_improvement: "77.4% less memory",
      accuracy_trade_off: "1.3% accuracy loss",
      zones_reduction: "95% fewer zones searched",
      sequences_reduction: "96.1% fewer sequences searched"
    }
  },

  // Real-time search statistics
  search_statistics: {
    total_searches_performed: 1247,
    avg_zones_selected: 3.2,
    avg_search_time_ms: 18.7,
    novel_sequences_discovered: 89,
    most_active_zones: [
      { zone_id: "zone_012", search_count: 234, hit_rate: 0.89 },
      { zone_id: "zone_034", search_count: 198, hit_rate: 0.84 },
      { zone_id: "zone_007", search_count: 167, hit_rate: 0.91 },
      { zone_id: "zone_045", search_count: 145, hit_rate: 0.77 },
      { zone_id: "zone_023", search_count: 134, hit_rate: 0.82 }
    ],
    zone_selection_strategies: {
      fixed_fraction: { usage: 0.23, avg_time: 15.4, accuracy: 0.981 },
      distance_threshold: { usage: 0.31, avg_time: 19.8, accuracy: 0.991 },
      heuristic_based: { usage: 0.46, avg_time: 18.2, accuracy: 0.987 }
    }
  }
};

export default searchSimulationData;
