//
//  User.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import Foundation

struct User: Codable, Identifiable {
    let id: String
    let email: String
    let name: String
    let role: UserRole
    let createdAt: Date
    let isActive: Bool
    
    enum CodingKeys: String, CodingKey {
        case id, email, name, role
        case createdAt = "created_at"
        case isActive = "is_active"
    }
}

enum UserRole: String, Codable, CaseIterable {
    case researcher = "researcher"
    case admin = "admin"
    
    var displayName: String {
        switch self {
        case .researcher:
            return "Researcher"
        case .admin:
            return "Administrator"
        }
    }
}

struct LoginRequest: Codable {
    let email: String
    let password: String
}


struct SignupRequest: Codable {
    let email: String
    let password: String
    let name: String
    let role: UserRole
}
