//
//  SearchModels.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import Foundation

struct SearchRequest: Codable {
    let query: String?
    let species: [String]?
    let taxa: [String]?
    let dateRange: DateRange?
    let location: LocationFilter?
    let rarity: RarityFilter?
    let novelty: NoveltyFilter?
    let confidence: ConfidenceFilter?
    let page: Int
    let limit: Int
    
    enum CodingKeys: String, CodingKey {
        case query, species, taxa
        case dateRange = "date_range"
        case location, rarity, novelty, confidence
        case page, limit
    }
}

struct DateRange: Codable {
    let startDate: Date
    let endDate: Date
    
    enum CodingKeys: String, CodingKey {
        case startDate = "start_date"
        case endDate = "end_date"
    }
}

struct LocationFilter: Codable {
    let latitude: Double?
    let longitude: Double?
    let radius: Double? // in kilometers
}

enum RarityFilter: String, Codable, CaseIterable {
    case common = "common"
    case uncommon = "uncommon"
    case rare = "rare"
    case veryRare = "very_rare"
    
    var displayName: String {
        switch self {
        case .common: return "Common"
        case .uncommon: return "Uncommon"
        case .rare: return "Rare"
        case .veryRare: return "Very Rare"
        }
    }
}

enum NoveltyFilter: String, Codable, CaseIterable {
    case known = "known"
    case potentiallyNovel = "potentially_novel"
    case novel = "novel"
    
    var displayName: String {
        switch self {
        case .known: return "Known"
        case .potentiallyNovel: return "Potentially Novel"
        case .novel: return "Novel"
        }
    }
}

struct ConfidenceFilter: Codable {
    let minConfidence: Double
    let maxConfidence: Double
    
    enum CodingKeys: String, CodingKey {
        case minConfidence = "min_confidence"
        case maxConfidence = "max_confidence"
    }
}

struct SearchResult: Codable, Identifiable {
    let id: String
    let species: String
    let taxa: [String]
    let confidence: Double
    let rarity: RarityFilter
    let novelty: NoveltyFilter
    let samplingDate: Date
    let location: SearchLocation
    let sequenceId: String
    let analysisId: String
    
    enum CodingKeys: String, CodingKey {
        case id, species, taxa, confidence, rarity, novelty
        case samplingDate = "sampling_date"
        case location
        case sequenceId = "sequence_id"
        case analysisId = "analysis_id"
    }
}

struct SearchLocation: Codable {
    let latitude: Double
    let longitude: Double
    let name: String?
    let depth: Double?
}

struct SearchResponse: Codable {
    let results: [SearchResult]
    let totalCount: Int
    let page: Int
    let totalPages: Int
    
    enum CodingKeys: String, CodingKey {
        case results
        case totalCount = "total_count"
        case page
        case totalPages = "total_pages"
    }
}
