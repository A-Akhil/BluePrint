//
//  APIService.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import Foundation
import Combine

class APIService: ObservableObject {
    static let shared = APIService()
    
    private let baseURL = "http://localhost:3000" // Local mock server
    private let session = URLSession.shared
    private var cancellables = Set<AnyCancellable>()
    
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var accessToken: String?
    
    private init() {
        loadStoredCredentials()
    }
    
    // MARK: - Authentication
    
    func login(email: String, password: String) -> AnyPublisher<LoginResponse, APIError> {
        let request = LoginRequest(email: email, password: password)
        return performRequest(endpoint: "/auth/login", method: "POST", body: request)
    }
    
    func signup(email: String, password: String, name: String, role: UserRole) -> AnyPublisher<LoginResponse, APIError> {
        let request = SignupRequest(email: email, password: password, name: name, role: role)
        return performRequest(endpoint: "/auth/signup", method: "POST", body: request)
    }
    
    func logout() {
        accessToken = nil
        currentUser = nil
        isAuthenticated = false
        UserDefaults.standard.removeObject(forKey: "accessToken")
        UserDefaults.standard.removeObject(forKey: "userData")
    }
    
    // MARK: - Sequence Management
    
    func uploadSequence(fileData: Data, filename: String, fileType: FileType, metadata: SequenceMetadata) -> AnyPublisher<UploadResponse, APIError> {
        let boundary = UUID().uuidString
        var request = createRequest(endpoint: "/api/v1/sequences/upload", method: "POST")
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        
        // Add metadata
        if let metadataData = try? JSONEncoder().encode(metadata) {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"metadata\"\r\n".data(using: .utf8)!)
            body.append("Content-Type: application/json\r\n\r\n".data(using: .utf8)!)
            body.append(metadataData)
            body.append("\r\n".data(using: .utf8)!)
        }
        
        // Add file
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: application/octet-stream\r\n\r\n".data(using: .utf8)!)
        body.append(fileData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        return session.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: UploadResponse.self, decoder: JSONDecoder())
            .mapError { error in
                if let apiError = try? JSONDecoder().decode(APIError.self, from: Data()) {
                    return apiError
                }
                return APIError(error: "Network Error", message: error.localizedDescription, statusCode: 0, timestamp: ISO8601DateFormatter().string(from: Date()))
            }
            .eraseToAnyPublisher()
    }
    
    func getSequences() -> AnyPublisher<[SequenceData], APIError> {
        return performGetRequest(endpoint: "/api/v1/sequences")
    }
    
    // MARK: - Search
    
    func searchSequences(request: SearchRequest) -> AnyPublisher<SearchResponse, APIError> {
        return performRequest(endpoint: "/api/v1/search/hierarchical", method: "POST", body: request)
    }
    
    func getSearchResults(searchId: String) -> AnyPublisher<SearchResponse, APIError> {
        return performGetRequest(endpoint: "/api/v1/search/\(searchId)/results")
    }
    
    // MARK: - AI Analysis
    
    func analyzeNovelTaxa(analysisId: String) -> AnyPublisher<NovelTaxaResponse, APIError> {
        let request = ["analysis_id": analysisId]
        return performRequest(endpoint: "/api/v1/ai/novel-taxa", method: "POST", body: request)
    }
    
    func classifySequences(analysisId: String) -> AnyPublisher<ClassificationResponse, APIError> {
        let request = ["analysis_id": analysisId]
        return performRequest(endpoint: "/api/v1/ai/classify", method: "POST", body: request)
    }
    
    // MARK: - Visualization
    
    func getTaxonomyVisualization(analysisId: String) -> AnyPublisher<TaxonomyResponse, APIError> {
        return performGetRequest(endpoint: "/api/v1/visualization/taxonomy", queryParams: ["analysis_id": analysisId])
    }
    
    func getPhylogenyVisualization(analysisId: String) -> AnyPublisher<PhylogenyResponse, APIError> {
        return performGetRequest(endpoint: "/api/v1/visualization/phylogeny/\(analysisId)")
    }
    
    // MARK: - Biodiversity
    
    func getCommunityAnalysis(analysisId: String) -> AnyPublisher<CommunityResponse, APIError> {
        return performGetRequest(endpoint: "/api/v1/biodiversity/community", queryParams: ["analysis_id": analysisId])
    }
    
    func getAbundanceAnalysis(analysisId: String) -> AnyPublisher<AbundanceResponse, APIError> {
        return performGetRequest(endpoint: "/api/v1/biodiversity/abundance", queryParams: ["analysis_id": analysisId])
    }
    
    // MARK: - Export
    
    func generateReport(analysisId: String, format: String) -> AnyPublisher<Data, APIError> {
        return session.dataTaskPublisher(for: createRequest(endpoint: "/api/v1/export/\(analysisId)/report", method: "GET", queryParams: ["format": format]))
            .map(\.data)
            .mapError { error in
                APIError(error: "Export Error", message: error.localizedDescription, statusCode: 0, timestamp: ISO8601DateFormatter().string(from: Date()))
            }
            .eraseToAnyPublisher()
    }
    
    // MARK: - Private Methods
    
    private func performGetRequest<R: Codable>(endpoint: String, queryParams: [String: String]? = nil) -> AnyPublisher<R, APIError> {
        let request = createRequest(endpoint: endpoint, method: "GET", queryParams: queryParams)
        
        return session.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: R.self, decoder: JSONDecoder())
            .mapError { error in
                if let apiError = try? JSONDecoder().decode(APIError.self, from: Data()) {
                    return apiError
                }
                return APIError(error: "Network Error", message: error.localizedDescription, statusCode: 0, timestamp: ISO8601DateFormatter().string(from: Date()))
            }
            .eraseToAnyPublisher()
    }
    
    private func performRequest<T: Codable, R: Codable>(endpoint: String, method: String, body: T? = nil, queryParams: [String: String]? = nil) -> AnyPublisher<R, APIError> {
        var request = createRequest(endpoint: endpoint, method: method, queryParams: queryParams)
        
        if let body = body {
            do {
                request.httpBody = try JSONEncoder().encode(body)
                request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            } catch {
                return Fail(error: APIError(error: "Encoding Error", message: error.localizedDescription, statusCode: 0, timestamp: ISO8601DateFormatter().string(from: Date())))
                    .eraseToAnyPublisher()
            }
        }
        
        return session.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: R.self, decoder: JSONDecoder())
            .mapError { error in
                if let apiError = try? JSONDecoder().decode(APIError.self, from: Data()) {
                    return apiError
                }
                return APIError(error: "Network Error", message: error.localizedDescription, statusCode: 0, timestamp: ISO8601DateFormatter().string(from: Date()))
            }
            .eraseToAnyPublisher()
    }
    
    private func createRequest(endpoint: String, method: String, queryParams: [String: String]? = nil) -> URLRequest {
        var components = URLComponents(string: baseURL + endpoint)!
        
        if let queryParams = queryParams {
            components.queryItems = queryParams.map { URLQueryItem(name: $0.key, value: $0.value) }
        }
        
        var request = URLRequest(url: components.url!)
        request.httpMethod = method
        
        if let token = accessToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        return request
    }
    
    private func loadStoredCredentials() {
        if let token = UserDefaults.standard.string(forKey: "accessToken") {
            accessToken = token
            isAuthenticated = true
            
            if let userData = UserDefaults.standard.data(forKey: "userData"),
               let user = try? JSONDecoder().decode(User.self, from: userData) {
                currentUser = user
            }
        }
    }
    
    func storeCredentials(token: String, user: User) {
        accessToken = token
        currentUser = user
        isAuthenticated = true
        
        UserDefaults.standard.set(token, forKey: "accessToken")
        if let userData = try? JSONEncoder().encode(user) {
            UserDefaults.standard.set(userData, forKey: "userData")
        }
    }
}
