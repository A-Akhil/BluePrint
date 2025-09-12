//
//  SequenceData.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import Foundation

struct SequenceData: Codable, Identifiable {
    let id: String
    let filename: String
    let fileType: FileType
    let fileSize: Int
    let uploadDate: Date
    let status: UploadStatus
    let metadata: SequenceMetadata?
    let analysisId: String?
    
    enum CodingKeys: String, CodingKey {
        case id, filename
        case fileType = "file_type"
        case fileSize = "file_size"
        case uploadDate = "upload_date"
        case status, metadata
        case analysisId = "analysis_id"
    }
}

enum FileType: String, Codable, CaseIterable {
    case csv = "csv"
    case json = "json"
    case fasta = "fasta"
    
    var displayName: String {
        switch self {
        case .csv: return "CSV"
        case .json: return "JSON"
        case .fasta: return "FASTA"
        }
    }
    
    var fileExtension: String {
        return rawValue
    }
}

enum UploadStatus: String, Codable {
    case pending = "pending"
    case processing = "processing"
    case completed = "completed"
    case failed = "failed"
    
    var displayName: String {
        switch self {
        case .pending: return "Pending"
        case .processing: return "Processing"
        case .completed: return "Completed"
        case .failed: return "Failed"
        }
    }
}

struct SequenceMetadata: Codable {
    var samplingDate: Date?
    var temperature: Double?
    var salinity: Double?
    var depth: Double?
    var latitude: Double?
    var longitude: Double?
    var location: String?
    var notes: String?
    
    enum CodingKeys: String, CodingKey {
        case samplingDate = "sampling_date"
        case temperature, salinity, depth
        case latitude, longitude, location, notes
    }
}

struct UploadRequest: Codable {
    let metadata: SequenceMetadata
}

struct UploadResponse: Codable {
    let sequenceId: String
    let analysisId: String
    let status: UploadStatus
    
    enum CodingKeys: String, CodingKey {
        case sequenceId = "sequence_id"
        case analysisId = "analysis_id"
        case status
    }
}
