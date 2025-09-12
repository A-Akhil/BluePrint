//
//  APIError.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import Foundation

struct APIError: Codable, Error {
    let error: String
    let message: String
    let statusCode: Int
    let timestamp: String
    
    enum CodingKeys: String, CodingKey {
        case error, message
        case statusCode = "status_code"
        case timestamp
    }
}

extension APIError: LocalizedError {
    var errorDescription: String? {
        return message
    }
}
