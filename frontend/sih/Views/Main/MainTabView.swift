//
//  MainTabView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

struct MainTabView: View {
    @EnvironmentObject var authManager: AuthManager
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            if authManager.currentUser?.role == .researcher {
                ResearcherDashboardView()
                    .tabItem {
                        Image(systemName: "house.fill")
                        Text("Dashboard")
                    }
                    .tag(0)
                
                UploadView()
                    .tabItem {
                        Image(systemName: "square.and.arrow.up")
                        Text("Upload")
                    }
                    .tag(1)
                
                SearchView()
                    .tabItem {
                        Image(systemName: "magnifyingglass")
                        Text("Search")
                    }
                    .tag(2)
                
                VisualizationView()
                    .tabItem {
                        Image(systemName: "chart.bar.fill")
                        Text("Visualize")
                    }
                    .tag(3)
                
                MapView()
                    .tabItem {
                        Image(systemName: "map.fill")
                        Text("Map")
                    }
                    .tag(4)
                
                ProfileView()
                    .tabItem {
                        Image(systemName: "person.fill")
                        Text("Profile")
                    }
                    .tag(5)
            } else {
                AdminDashboardView()
                    .tabItem {
                        Image(systemName: "house.fill")
                        Text("Dashboard")
                    }
                    .tag(0)
                
                UserManagementView()
                    .tabItem {
                        Image(systemName: "person.2.fill")
                        Text("Users")
                    }
                    .tag(1)
                
                DatasetModerationView()
                    .tabItem {
                        Image(systemName: "doc.text.fill")
                        Text("Datasets")
                    }
                    .tag(2)
                
                SystemMonitoringView()
                    .tabItem {
                        Image(systemName: "chart.line.uptrend.xyaxis")
                        Text("Monitoring")
                    }
                    .tag(3)
                
                ProfileView()
                    .tabItem {
                        Image(systemName: "person.fill")
                        Text("Profile")
                    }
                    .tag(4)
            }
        }
        .accentColor(Theme.primary)
    }
}

#Preview {
    MainTabView()
        .environmentObject(AuthManager())
}
