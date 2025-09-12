//
//  ResearcherDashboardView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import Charts
import Combine

struct ResearcherDashboardView: View {
    @EnvironmentObject var authManager: AuthManager
    @StateObject private var apiService = APIService.shared
    @State private var recentSequences: [SequenceData] = []
    @State private var isLoading = false
    @State private var stats = DashboardStats()
    @State private var cancellables = Set<AnyCancellable>()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.spacingL) {
                    // Welcome Header
                    VStack(alignment: .leading, spacing: Theme.spacingS) {
                        Text("Welcome back, \(authManager.currentUser?.name ?? "Researcher")!")
                            .font(Theme.title2)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Text("Here's your research overview")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.horizontal, Theme.spacingL)
                    
                    // Quick Stats
                    LazyVGrid(columns: [
                        GridItem(.flexible()),
                        GridItem(.flexible())
                    ], spacing: Theme.spacingM) {
                        StatCard(
                            title: "Total Sequences",
                            value: "\(stats.totalSequences)",
                            icon: "dna.helix",
                            color: Theme.primary
                        )
                        
                        StatCard(
                            title: "Active Analyses",
                            value: "\(stats.activeAnalyses)",
                            icon: "chart.line.uptrend.xyaxis",
                            color: Theme.success
                        )
                        
                        StatCard(
                            title: "Species Found",
                            value: "\(stats.speciesFound)",
                            icon: "leaf.fill",
                            color: Theme.accent
                        )
                        
                        StatCard(
                            title: "Novel Taxa",
                            value: "\(stats.novelTaxa)",
                            icon: "sparkles",
                            color: Theme.secondary
                        )
                    }
                    .padding(.horizontal, Theme.spacingL)
                    
                    // Recent Activity
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        HStack {
                            Text("Recent Activity")
                                .font(Theme.title3)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Spacer()
                            
                            Button("View All") {
                                // Navigate to full activity view
                            }
                            .font(Theme.callout)
                            .foregroundColor(Theme.primary)
                        }
                        .padding(.horizontal, Theme.spacingL)
                        
                        if isLoading {
                            ProgressView()
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, Theme.spacingXL)
                        } else {
                        LazyVStack(spacing: Theme.spacingS) {
                            ForEach(recentSequences.prefix(5)) { sequence in
                                SequenceActivityRow(sequence: sequence)
                            }
                        }
                            .padding(.horizontal, Theme.spacingL)
                        }
                    }
                    
                    // Quick Actions
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Quick Actions")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                            .padding(.horizontal, Theme.spacingL)
                        
                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: Theme.spacingM) {
                            QuickActionCard(
                                title: "Upload Data",
                                icon: "square.and.arrow.up",
                                color: Theme.primary
                            ) {
                                // Navigate to upload
                            }
                            
                            QuickActionCard(
                                title: "Search Sequences",
                                icon: "magnifyingglass",
                                color: Theme.accent
                            ) {
                                // Navigate to search
                            }
                            
                            QuickActionCard(
                                title: "View Reports",
                                icon: "doc.text.fill",
                                color: Theme.success
                            ) {
                                // Navigate to reports
                            }
                            
                            QuickActionCard(
                                title: "Map View",
                                icon: "map.fill",
                                color: Theme.secondary
                            ) {
                                // Navigate to map
                            }
                        }
                        .padding(.horizontal, Theme.spacingL)
                    }
                    
                    Spacer(minLength: Theme.spacingXL)
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Dashboard")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        authManager.logout()
                    }) {
                        Image(systemName: "rectangle.portrait.and.arrow.right")
                            .foregroundColor(Theme.primary)
                    }
                }
            }
        }
        .onAppear {
            loadDashboardData()
        }
    }
    
    private func loadDashboardData() {
        isLoading = true
        
        // Load recent sequences
        apiService.getSequences()
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { _ in
                    isLoading = false
                },
                receiveValue: { sequences in
                    recentSequences = sequences.sorted { $0.uploadDate > $1.uploadDate }
                }
            )
            .store(in: &cancellables)
    }
}

struct DashboardStats {
    var totalSequences: Int = 0
    var activeAnalyses: Int = 0
    var speciesFound: Int = 0
    var novelTaxa: Int = 0
}

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(spacing: Theme.spacingS) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            
            Text(value)
                .font(Theme.title2)
                .fontWeight(.bold)
                .foregroundColor(Theme.textPrimaryLight)
            
            Text(title)
                .font(Theme.caption)
                .foregroundColor(Theme.textSecondaryLight)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(Theme.spacingM)
        .cardStyle()
    }
}

struct SequenceActivityRow: View {
    let sequence: SequenceData
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: "doc.text.fill")
                .foregroundColor(Theme.primary)
                .frame(width: 24)
            
            VStack(alignment: .leading, spacing: Theme.spacingXS) {
                Text(sequence.filename)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                    .lineLimit(1)
                
                Text(sequence.uploadDate, style: .relative)
                    .font(Theme.caption)
                    .foregroundColor(Theme.textSecondaryLight)
            }
            
            Spacer()
            
            StatusBadge(status: sequence.status)
        }
        .padding(Theme.spacingM)
        .cardStyle()
    }
}

struct StatusBadge: View {
    let status: UploadStatus
    
    var body: some View {
        Text(status.displayName)
            .font(Theme.caption)
            .fontWeight(.medium)
            .padding(.horizontal, Theme.spacingS)
            .padding(.vertical, Theme.spacingXS)
            .background(statusColor.opacity(0.2))
            .foregroundColor(statusColor)
            .cornerRadius(Theme.radiusS)
    }
    
    private var statusColor: Color {
        switch status {
        case .pending: return Theme.warning
        case .processing: return Theme.info
        case .completed: return Theme.success
        case .failed: return Theme.danger
        }
    }
}

struct QuickActionCard: View {
    let title: String
    let icon: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: Theme.spacingS) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                
                Text(title)
                    .font(Theme.callout)
                    .fontWeight(.medium)
                    .foregroundColor(Theme.textPrimaryLight)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity)
            .padding(Theme.spacingM)
            .cardStyle()
        }
        .buttonStyle(PlainButtonStyle())
    }
}

#Preview {
    ResearcherDashboardView()
        .environmentObject(AuthManager())
}
