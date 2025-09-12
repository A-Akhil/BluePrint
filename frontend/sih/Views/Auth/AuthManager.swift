//
//  AuthManager.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import Combine

class AuthManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var isLoading = true
    
    private let apiService = APIService.shared
    private var cancellables = Set<AnyCancellable>()
    
    init() {
        setupBindings()
    }
    
    private func setupBindings() {
        apiService.$isAuthenticated
            .assign(to: \.isAuthenticated, on: self)
            .store(in: &cancellables)
        
        apiService.$currentUser
            .assign(to: \.currentUser, on: self)
            .store(in: &cancellables)
        
        // Check initial auth state
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            self.isLoading = false
        }
    }
    
    func logout() {
        apiService.logout()
    }
}
