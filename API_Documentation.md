# Deep-Sea eDNA AI Pipeline - API Documentation

## Overview

This document outlines the comprehensive API specifications for the AI-driven deep-sea environmental DNA (eDNA) analysis pipeline developed for the Centre for Marine Living Resources and Ecology (CMLRE). The pipeline addresses the critical challenge of identifying eukaryotic taxa from deep-sea samples where traditional database-dependent methods fail due to poor representation of deep-sea organisms in reference databases.

## Architecture

- **Base URL**: `https://api.edna-pipeline.cmlre.gov.in`
- **Authentication**: Bearer Token
- **Content-Type**: `application/json`
- **API Version**: `v1`

---

## 1. Sequence Processing APIs

### 1.1 Upload Raw Sequences

**Endpoint**: `POST /api/v1/sequences/upload`

**Description**: Upload raw eDNA sequencing data for processing

**Headers**:
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Request Body**:
```json
{
  "sample_id": "CMLRE_DeepSea_001",
  "expedition_id": "DSE_2025_01",
  "location": {
    "latitude": -23.4567,
    "longitude": 65.7890,
    "depth_meters": 3500,
    "habitat_type": "abyssal_plain"
  },
  "sample_metadata": {
    "collection_date": "2025-09-15T10:30:00Z",
    "sample_type": "sediment",
    "volume_ml": 250,
    "extraction_method": "DNeasy",
    "amplicon_region": "18S_V4"
  },
  "sequence_file": "file_upload",
  "quality_file": "file_upload"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "upload_id": "upload_12345",
    "sample_id": "CMLRE_DeepSea_001",
    "file_size_mb": 125.7,
    "sequence_count": 45678,
    "estimated_processing_time_minutes": 15,
    "status": "uploaded"
  },
  "message": "Sequences uploaded successfully and queued for processing"
}
```

### 1.2 Quality Control and Preprocessing

**Endpoint**: `POST /api/v1/sequences/preprocess`

**Description**: Perform quality control, filtering, and preprocessing of raw sequences

**Request Body**:
```json
{
  "upload_id": "upload_12345",
  "parameters": {
    "min_length": 400,
    "max_length": 800,
    "min_quality_score": 20,
    "max_n_percent": 5,
    "remove_chimeras": true,
    "trim_primers": true,
    "primer_sequences": {
      "forward": "CCAGCASCYGCGGTAATTCC",
      "reverse": "ACTTTCGTTCTTGATYRA"
    }
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "processing_id": "proc_67890",
    "input_sequences": 45678,
    "filtered_sequences": 42134,
    "quality_metrics": {
      "mean_length": 456,
      "mean_quality": 32.4,
      "gc_content": 0.52
    },
    "processing_time_seconds": 180,
    "status": "completed"
  }
}
```

---

## 2. Database Search APIs

### 2.1 Hierarchical Database Search

**Endpoint**: `POST /api/v1/search/hierarchical`

**Description**: Perform hierarchical search through eukaryotic databases (18S → 28S → ITS)

**Request Body**:
```json
{
  "processing_id": "proc_67890",
  "search_parameters": {
    "databases": ["SSU_eukaryote_rRNA", "LSU_eukaryote_rRNA", "ITS_eukaryote_sequences"],
    "blast_parameters": {
      "e_value": 1e-5,
      "min_identity": 80,
      "min_coverage": 70,
      "max_targets": 10
    },
    "taxonomic_filters": ["Eukaryota"],
    "exclude_terrestrial": true
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "search_id": "search_11111",
    "results_summary": {
      "total_sequences": 42134,
      "assigned_sequences": 29694,
      "assignment_rate": 0.704,
      "database_breakdown": {
        "SSU_eukaryote_rRNA": 26789,
        "LSU_eukaryote_rRNA": 2156,
        "ITS_eukaryote_sequences": 749
      }
    },
    "unassigned_sequences": 12440,
    "processing_time_minutes": 8.5
  }
}
```

### 2.2 Get Search Results

**Endpoint**: `GET /api/v1/search/{search_id}/results`

**Description**: Retrieve detailed results from database search

**Parameters**:
- `page`: Page number (default: 1)
- `limit`: Results per page (default: 100)
- `taxonomy_level`: Filter by taxonomic level
- `confidence_threshold`: Minimum confidence score

**Response**:
```json
{
  "status": "success",
  "data": {
    "search_id": "search_11111",
    "total_results": 29694,
    "page": 1,
    "limit": 100,
    "results": [
      {
        "sequence_id": "seq_001",
        "best_match": {
          "accession": "KX123456",
          "species": "Radiolaria sp. CMLRE_001",
          "identity_percent": 92.3,
          "coverage_percent": 85.7,
          "e_value": 2.4e-89,
          "database": "SSU_eukaryote_rRNA"
        },
        "taxonomy": {
          "kingdom": "Eukaryota",
          "phylum": "Retaria",
          "class": "Radiolaria",
          "order": "Spumellaria",
          "family": "Actinommidae",
          "genus": "Actinomma",
          "species": "Actinomma sp."
        },
        "confidence_score": 0.923
      }
    ]
  }
}
```

---

## 3. AI Classification APIs

### 3.1 Novel Taxa Detection

**Endpoint**: `POST /api/v1/ai/novel-taxa`

**Description**: Use unsupervised learning to identify potential novel taxa from unassigned sequences

**Request Body**:
```json
{
  "search_id": "search_11111",
  "parameters": {
    "clustering_method": "UMAP_HDBSCAN",
    "similarity_threshold": 0.85,
    "min_cluster_size": 5,
    "feature_extraction": {
      "kmer_size": 6,
      "include_reverse_complement": true,
      "normalize": true
    },
    "deep_learning_model": "eukaryotic_transformer_v2"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "analysis_id": "ai_22222",
    "novel_clusters": [
      {
        "cluster_id": "novel_001",
        "sequence_count": 127,
        "representative_sequence": "seq_5678",
        "confidence_score": 0.89,
        "predicted_taxonomy": {
          "kingdom": "Eukaryota",
          "phylum": "Unknown_Protist_Clade_A",
          "confidence": 0.76
        },
        "habitat_specificity": "deep_sea_sediment"
      }
    ],
    "total_novel_sequences": 8932,
    "processing_time_minutes": 25.3
  }
}
```

### 3.2 Deep Learning Classification

**Endpoint**: `POST /api/v1/ai/classify`

**Description**: Apply deep learning models for taxonomic classification

**Request Body**:
```json
{
  "processing_id": "proc_67890",
  "model_config": {
    "model_name": "DeepSea_Eukaryote_Classifier_v3",
    "confidence_threshold": 0.7,
    "ensemble_methods": ["CNN", "Transformer", "LSTM"],
    "feature_types": ["sequence", "kmer", "phylogenetic"]
  },
  "target_sequences": "unassigned_only"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "classification_id": "class_33333",
    "classified_sequences": 7834,
    "high_confidence_predictions": 6012,
    "taxonomic_distribution": {
      "Protista": 5234,
      "Metazoa": 1876,
      "Cnidaria": 567,
      "Fungi": 157
    },
    "novel_lineages_detected": 23,
    "processing_time_minutes": 42.1
  }
}
```

---

## 4. Phylogenetic Placement APIs

### 4.1 Phylogenetic Tree Placement

**Endpoint**: `POST /api/v1/phylogeny/placement`

**Description**: Place sequences on reference phylogenetic trees for evolutionary context

**Request Body**:
```json
{
  "sequence_ids": ["seq_5678", "seq_5679", "seq_5680"],
  "reference_tree": "eukaryotic_18S_tree_v4",
  "placement_method": "EPA-ng",
  "parameters": {
    "bootstrap_replicates": 100,
    "model": "GTR+GAMMA",
    "likelihood_threshold": 0.95
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "placement_id": "phylo_44444",
    "placements": [
      {
        "sequence_id": "seq_5678",
        "placement_node": "node_1234",
        "likelihood_weight": 0.89,
        "pendant_length": 0.0234,
        "closest_relatives": [
          "Radiolaria_sp_ABC123",
          "Spumellaria_sp_DEF456"
        ],
        "evolutionary_distance": 0.12
      }
    ],
    "tree_file_url": "/api/v1/files/phylo_44444_tree.newick"
  }
}
```

---

## 5. Biodiversity Assessment APIs

### 5.1 Community Analysis

**Endpoint**: `POST /api/v1/biodiversity/community`

**Description**: Calculate biodiversity metrics and community structure

**Request Body**:
```json
{
  "sample_ids": ["CMLRE_DeepSea_001", "CMLRE_DeepSea_002"],
  "analysis_type": "comprehensive",
  "metrics": [
    "shannon_diversity",
    "simpson_diversity",
    "chao1_richness",
    "faith_pd",
    "beta_diversity"
  ],
  "rarefaction": {
    "enabled": true,
    "depth": 1000,
    "iterations": 100
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "analysis_id": "bio_55555",
    "diversity_metrics": {
      "CMLRE_DeepSea_001": {
        "shannon_h": 3.45,
        "simpson_d": 0.89,
        "chao1": 234.5,
        "observed_otus": 187,
        "faith_pd": 45.6
      }
    },
    "community_composition": {
      "dominant_taxa": [
        {"taxon": "Radiolaria", "relative_abundance": 0.34},
        {"taxon": "Foraminifera", "relative_abundance": 0.28},
        {"taxon": "Ciliophora", "relative_abundance": 0.15}
      ]
    },
    "beta_diversity_matrix": "matrix_data_url"
  }
}
```

### 5.2 Abundance Estimation

**Endpoint**: `POST /api/v1/biodiversity/abundance`

**Description**: Estimate species abundance with bias correction for database gaps

**Request Body**:
```json
{
  "search_id": "search_11111",
  "correction_method": "database_bias_adjustment",
  "parameters": {
    "depth_correction": true,
    "habitat_specificity": "deep_sea",
    "detection_probability_model": "hierarchical_bayesian"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "abundance_id": "abund_66666",
    "corrected_abundances": [
      {
        "taxon": "Radiolaria sp. nov. 1",
        "raw_count": 1234,
        "corrected_abundance": 0.156,
        "confidence_interval": [0.142, 0.171],
        "detection_probability": 0.78
      }
    ],
    "bias_correction_factors": {
      "database_completeness": 0.65,
      "depth_bias": 1.23,
      "habitat_specificity": 1.45
    }
  }
}
```

---

## 6. Visualization APIs

### 6.1 Generate Taxonomic Plots

**Endpoint**: `POST /api/v1/visualization/taxonomy`

**Description**: Generate taxonomic composition visualizations

**Request Body**:
```json
{
  "analysis_id": "bio_55555",
  "plot_type": "stacked_bar",
  "parameters": {
    "taxonomic_level": "phylum",
    "color_scheme": "marine_palette",
    "include_unknowns": true,
    "format": "png",
    "width": 1200,
    "height": 800
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "plot_id": "viz_77777",
    "plot_url": "/api/v1/files/viz_77777_taxonomy.png",
    "thumbnail_url": "/api/v1/files/viz_77777_thumb.png",
    "metadata": {
      "taxa_displayed": 15,
      "unknown_percentage": 23.4,
      "generated_at": "2025-09-15T14:30:00Z"
    }
  }
}
```

### 6.2 Phylogenetic Tree Visualization

**Endpoint**: `GET /api/v1/visualization/phylogeny/{placement_id}`

**Description**: Generate interactive phylogenetic tree visualizations

**Parameters**:
- `format`: Tree format (newick, nexus, json)
- `style`: Visualization style (circular, rectangular)
- `annotations`: Include annotations (bootstrap, species_names)

**Response**:
```json
{
  "status": "success",
  "data": {
    "tree_viz_id": "tree_88888",
    "interactive_url": "/api/v1/interactive/tree_88888",
    "static_image_url": "/api/v1/files/tree_88888.svg",
    "tree_statistics": {
      "total_nodes": 456,
      "placed_sequences": 127,
      "novel_clades": 8
    }
  }
}
```

---

## 7. Pipeline Management APIs

### 7.1 Create Analysis Pipeline

**Endpoint**: `POST /api/v1/pipeline/create`

**Description**: Create and configure a complete analysis pipeline

**Request Body**:
```json
{
  "pipeline_name": "Deep_Sea_Survey_2025",
  "description": "Comprehensive eDNA analysis for deep-sea biodiversity survey",
  "workflow_steps": [
    {
      "step": "preprocess",
      "parameters": {"min_length": 400, "max_length": 800}
    },
    {
      "step": "database_search",
      "parameters": {"databases": ["SSU_eukaryote_rRNA", "LSU_eukaryote_rRNA"]}
    },
    {
      "step": "ai_classification",
      "parameters": {"model": "DeepSea_Eukaryote_Classifier_v3"}
    },
    {
      "step": "phylogenetic_placement",
      "parameters": {"reference_tree": "eukaryotic_18S_tree_v4"}
    },
    {
      "step": "biodiversity_analysis",
      "parameters": {"metrics": ["shannon_diversity", "simpson_diversity"]}
    }
  ],
  "notification_settings": {
    "email": "researcher@cmlre.gov.in",
    "webhook": "https://cmlre.gov.in/webhook/pipeline"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "pipeline_id": "pipe_99999",
    "pipeline_name": "Deep_Sea_Survey_2025",
    "status": "created",
    "estimated_runtime_hours": 2.5,
    "webhook_token": "webhook_token_abc123"
  }
}
```

### 7.2 Execute Pipeline

**Endpoint**: `POST /api/v1/pipeline/{pipeline_id}/execute`

**Description**: Execute a configured analysis pipeline

**Request Body**:
```json
{
  "sample_ids": ["CMLRE_DeepSea_001", "CMLRE_DeepSea_002"],
  "priority": "high",
  "resource_allocation": {
    "cpu_cores": 16,
    "memory_gb": 64,
    "gpu_enabled": true
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "execution_id": "exec_00000",
    "pipeline_id": "pipe_99999",
    "status": "running",
    "progress": {
      "current_step": "database_search",
      "completion_percentage": 35,
      "estimated_completion": "2025-09-15T16:45:00Z"
    },
    "resource_usage": {
      "cpu_usage": "75%",
      "memory_usage": "42GB",
      "processing_rate": "1250 sequences/minute"
    }
  }
}
```

### 7.3 Get Pipeline Status

**Endpoint**: `GET /api/v1/pipeline/{execution_id}/status`

**Description**: Get real-time status of pipeline execution

**Response**:
```json
{
  "status": "success",
  "data": {
    "execution_id": "exec_00000",
    "status": "completed",
    "start_time": "2025-09-15T14:00:00Z",
    "end_time": "2025-09-15T16:30:00Z",
    "total_runtime_minutes": 150,
    "step_results": {
      "preprocess": {"status": "completed", "sequences_processed": 42134},
      "database_search": {"status": "completed", "assignments": 29694},
      "ai_classification": {"status": "completed", "novel_taxa": 23},
      "phylogenetic_placement": {"status": "completed", "placements": 127},
      "biodiversity_analysis": {"status": "completed", "shannon_h": 3.45}
    },
    "output_files": [
      "/api/v1/files/exec_00000_results.json",
      "/api/v1/files/exec_00000_report.pdf"
    ]
  }
}
```

---

## 8. Error Handling

### Standard Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_SEQUENCE_FORMAT",
    "message": "Uploaded file is not in FASTQ format",
    "details": {
      "file_name": "sample_001.txt",
      "expected_format": "FASTQ",
      "detected_format": "plain_text"
    },
    "timestamp": "2025-09-15T14:30:00Z",
    "request_id": "req_12345"
  }
}
```

### Common Error Codes

- `INVALID_SEQUENCE_FORMAT`: Unsupported file format
- `INSUFFICIENT_SEQUENCE_QUALITY`: Sequences don't meet quality thresholds
- `DATABASE_UNAVAILABLE`: Reference database temporarily unavailable
- `PROCESSING_TIMEOUT`: Analysis exceeded time limits
- `INVALID_TAXONOMIC_FILTER`: Specified taxonomic group not supported
- `MODEL_NOT_FOUND`: Requested AI model not available
- `QUOTA_EXCEEDED`: User has exceeded processing limits

---

## 9. Rate Limits and Quotas

- **Uploads**: 100 files per hour
- **API Calls**: 1000 requests per hour
- **Processing**: 10 concurrent pipelines per user
- **Storage**: 100GB per user account
- **Data Retention**: 90 days for results, 30 days for raw data

---

## 10. Authentication

### Bearer Token Authentication

Include the token in the Authorization header:
```
Authorization: Bearer your_api_token_here
```

### Token Management

- **Get Token**: `POST /api/v1/auth/token`
- **Refresh Token**: `POST /api/v1/auth/refresh`
- **Revoke Token**: `DELETE /api/v1/auth/token`

---

## 11. Data Export

### Export Formats

- **JSON**: Structured data for programmatic access
- **CSV**: Spreadsheet-compatible format
- **FASTA**: Sequence data
- **Newick**: Phylogenetic trees
- **PDF**: Formatted reports

### Export Endpoints

- `GET /api/v1/export/{analysis_id}/json`
- `GET /api/v1/export/{analysis_id}/csv`
- `GET /api/v1/export/{analysis_id}/fasta`
- `GET /api/v1/export/{analysis_id}/report`

