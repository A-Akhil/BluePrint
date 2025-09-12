//
//  sihApp.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

@main
struct ResearchHubApp: App {
    @StateObject private var authManager = AuthManager()
    
    var body: some Scene {
        WindowGroup {
            Group {
                if authManager.isLoading {
                    SplashView()
                } else if authManager.isAuthenticated {
                    MainTabView()
                } else {
                    AuthView()
                }
            }
            .environmentObject(authManager)
        }
    }
}
