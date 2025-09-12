//
//  APIResponses.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import Foundation

// MARK: - Authentication Responses
struct LoginResponse: Codable {
    let success: Bool
    let token: String
    let user: User
    
    enum CodingKeys: String, CodingKey {
        case success, token, user
    }
}

struct AuthResponse: Codable {
    let success: Bool
    let accessToken: String
    let user: User
    
    enum CodingKeys: String, CodingKey {
        case success
        case accessToken = "access_token"
        case user
    }
}

// MARK: - AI Analysis Responses
struct NovelTaxaResponse: Codable {
    let analysisId: String
    let novelTaxa: [NovelTaxaItem]
    let confidence: Double
    let timestamp: Date
    
    enum CodingKeys: String, CodingKey {
        case analysisId = "analysis_id"
        case novelTaxa = "novel_taxa"
        case confidence, timestamp
    }
}

struct NovelTaxaItem: Codable {
    let species: String
    let confidence: Double
    let sequence: String
    let position: Int
}

struct ClassificationResponse: Codable {
    let analysisId: String
    let classifications: [ClassificationItem]
    let totalSequences: Int
    let timestamp: Date
    
    enum CodingKeys: String, CodingKey {
        case analysisId = "analysis_id"
        case classifications, totalSequences = "total_sequences"
        case timestamp
    }
}

struct ClassificationItem: Codable {
    let sequenceId: String
    let species: String
    let confidence: Double
    let taxonomy: [String]
    
    enum CodingKeys: String, CodingKey {
        case sequenceId = "sequence_id"
        case species, confidence, taxonomy
    }
}

// MARK: - Visualization Responses
struct TaxonomyResponse: Codable {
    let analysisId: String
    let taxonomyTree: TaxonomyNode
    let totalSpecies: Int
    let timestamp: Date
    
    enum CodingKeys: String, CodingKey {
        case analysisId = "analysis_id"
        case taxonomyTree = "taxonomy_tree"
        case totalSpecies = "total_species"
        case timestamp
    }
}

struct TaxonomyNode: Codable {
    let name: String
    let level: String
    let count: Int
    let children: [TaxonomyNode]?
    let confidence: Double?
}

struct PhylogenyResponse: Codable {
    let analysisId: String
    let phylogenyTree: PhylogenyNode
    let totalSequences: Int
    let timestamp: Date
    
    enum CodingKeys: String, CodingKey {
        case analysisId = "analysis_id"
        case phylogenyTree = "phylogeny_tree"
        case totalSequences = "total_sequences"
        case timestamp
    }
}

struct PhylogenyNode: Codable {
    let name: String
    let branchLength: Double?
    let children: [PhylogenyNode]?
    let sequence: String?
    
    enum CodingKeys: String, CodingKey {
        case name
        case branchLength = "branch_length"
        case children, sequence
    }
}

// MARK: - Biodiversity Responses
struct CommunityResponse: Codable {
    let analysisId: String
    let diversityIndices: DiversityIndices
    let speciesRichness: Int
    let communityStructure: [CommunityItem]
    let timestamp: Date
    
    enum CodingKeys: String, CodingKey {
        case analysisId = "analysis_id"
        case diversityIndices = "diversity_indices"
        case speciesRichness = "species_richness"
        case communityStructure = "community_structure"
        case timestamp
    }
}

struct DiversityIndices: Codable {
    let shannon: Double
    let simpson: Double
    let evenness: Double
    let chao1: Double
}

struct CommunityItem: Codable {
    let species: String
    let abundance: Double
    let relativeAbundance: Double
    let frequency: Int
    
    enum CodingKeys: String, CodingKey {
        case species, abundance
        case relativeAbundance = "relative_abundance"
        case frequency
    }
}

struct AbundanceResponse: Codable {
    let analysisId: String
    let abundanceData: [AbundanceItem]
    let totalAbundance: Double
    let timestamp: Date
    
    enum CodingKeys: String, CodingKey {
        case analysisId = "analysis_id"
        case abundanceData = "abundance_data"
        case totalAbundance = "total_abundance"
        case timestamp
    }
}

struct AbundanceItem: Codable {
    let species: String
    let abundance: Double
    let relativeAbundance: Double
    let rank: Int
    
    enum CodingKeys: String, CodingKey {
        case species, abundance
        case relativeAbundance = "relative_abundance"
        case rank
    }
}
