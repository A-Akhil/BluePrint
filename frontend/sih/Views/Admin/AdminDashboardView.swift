//
//  AdminDashboardView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import Charts

struct AdminDashboardView: View {
    @EnvironmentObject var authManager: AuthManager
    @State private var systemStats = SystemStats()
    @State private var recentUsers: [User] = []
    @State private var pendingDatasets: [DatasetModeration] = []
    @State private var systemHealth = SystemHealth()
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.spacingL) {
                    // Welcome Header
                    VStack(alignment: .leading, spacing: Theme.spacingS) {
                        Text("Admin Dashboard")
                            .font(Theme.title2)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Text("System overview and management")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.horizontal, Theme.spacingL)
                    
                    // System Stats
                    LazyVGrid(columns: [
                        GridItem(.flexible()),
                        GridItem(.flexible())
                    ], spacing: Theme.spacingM) {
                        AdminStatCard(
                            title: "Total Users",
                            value: "\(systemStats.totalUsers)",
                            icon: "person.2.fill",
                            color: Theme.primary
                        )
                        
                        AdminStatCard(
                            title: "Active Datasets",
                            value: "\(systemStats.activeDatasets)",
                            icon: "doc.text.fill",
                            color: Theme.success
                        )
                        
                        AdminStatCard(
                            title: "Pending Reviews",
                            value: "\(systemStats.pendingReviews)",
                            icon: "clock.fill",
                            color: Theme.warning
                        )
                        
                        AdminStatCard(
                            title: "System Load",
                            value: "\(Int(systemStats.systemLoad * 100))%",
                            icon: "cpu.fill",
                            color: systemStats.systemLoad > 0.8 ? Theme.danger : Theme.accent
                        )
                    }
                    .padding(.horizontal, Theme.spacingL)
                    
                    // System Health
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("System Health")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        VStack(spacing: Theme.spacingS) {
                            HealthIndicator(
                                title: "API Status",
                                status: systemHealth.apiStatus,
                                value: systemHealth.apiResponseTime
                            )
                            
                            HealthIndicator(
                                title: "Database",
                                status: systemHealth.databaseStatus,
                                value: systemHealth.databaseConnections
                            )
                            
                            HealthIndicator(
                                title: "Storage",
                                status: systemHealth.storageStatus,
                                value: systemHealth.storageUsage
                            )
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Recent Activity
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Recent Activity")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        LazyVStack(spacing: Theme.spacingS) {
                            ForEach(recentActivities) { activity in
                                AdminActivityRow(activity: activity)
                            }
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Pending Datasets
                    if !pendingDatasets.isEmpty {
                        VStack(alignment: .leading, spacing: Theme.spacingM) {
                            HStack {
                                Text("Pending Dataset Reviews")
                                    .font(Theme.title3)
                                    .foregroundColor(Theme.textPrimaryLight)
                                
                                Spacer()
                                
                                Button("View All") {
                                    // Navigate to dataset moderation
                                }
                                .font(Theme.callout)
                                .foregroundColor(Theme.primary)
                            }
                            
                            LazyVStack(spacing: Theme.spacingS) {
                                ForEach(pendingDatasets.prefix(3)) { dataset in
                                    PendingDatasetRow(dataset: dataset)
                                }
                            }
                        }
                        .padding(Theme.spacingL)
                        .cardStyle()
                    }
                    
                    Spacer(minLength: Theme.spacingXL)
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Admin Dashboard")
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
            loadAdminData()
        }
    }
    
    private func loadAdminData() {
        isLoading = true
        
        // Generate sample data
        systemStats = SystemStats(
            totalUsers: 156,
            activeDatasets: 89,
            pendingReviews: 12,
            systemLoad: 0.65
        )
        
        systemHealth = SystemHealth(
            apiStatus: .healthy,
            apiResponseTime: "120ms",
            databaseStatus: .healthy,
            databaseConnections: "45/100",
            storageStatus: .warning,
            storageUsage: "78%"
        )
        
        pendingDatasets = [
            DatasetModeration(
                id: "1",
                filename: "marine_samples_2024.csv",
                uploadedBy: "Dr. Smith",
                uploadedAt: Date().addingTimeInterval(-3600),
                fileSize: 2.5,
                status: .pending
            ),
            DatasetModeration(
                id: "2",
                filename: "deep_sea_sequences.fasta",
                uploadedBy: "Dr. Johnson",
                uploadedAt: Date().addingTimeInterval(-7200),
                fileSize: 15.8,
                status: .pending
            )
        ]
        
        isLoading = false
    }
    
    private var recentActivities: [AdminActivity] {
        [
            AdminActivity(
                id: "1",
                title: "New user registered: Dr. Wilson",
                timestamp: Date().addingTimeInterval(-1800),
                type: .user
            ),
            AdminActivity(
                id: "2",
                title: "Dataset approved: ocean_data_2024.json",
                timestamp: Date().addingTimeInterval(-3600),
                type: .dataset
            ),
            AdminActivity(
                id: "3",
                title: "System backup completed",
                timestamp: Date().addingTimeInterval(-7200),
                type: .system
            )
        ]
    }
}

struct SystemStats {
    var totalUsers: Int = 0
    var activeDatasets: Int = 0
    var pendingReviews: Int = 0
    var systemLoad: Double = 0.0
}

struct SystemHealth {
    var apiStatus: HealthStatus = .healthy
    var apiResponseTime: String = ""
    var databaseStatus: HealthStatus = .healthy
    var databaseConnections: String = ""
    var storageStatus: HealthStatus = .healthy
    var storageUsage: String = ""
}

enum HealthStatus {
    case healthy
    case warning
    case critical
    
    var color: Color {
        switch self {
        case .healthy: return Theme.success
        case .warning: return Theme.warning
        case .critical: return Theme.danger
        }
    }
    
    var icon: String {
        switch self {
        case .healthy: return "checkmark.circle.fill"
        case .warning: return "exclamationmark.triangle.fill"
        case .critical: return "xmark.circle.fill"
        }
    }
}

struct AdminStatCard: View {
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

struct HealthIndicator: View {
    let title: String
    let status: HealthStatus
    let value: String
    
    var body: some View {
        HStack {
            Image(systemName: status.icon)
                .foregroundColor(status.color)
                .frame(width: 20)
            
            Text(title)
                .font(Theme.callout)
                .foregroundColor(Theme.textPrimaryLight)
            
            Spacer()
            
            Text(value)
                .font(Theme.callout)
                .foregroundColor(Theme.textSecondaryLight)
        }
        .padding(Theme.spacingS)
    }
}

struct AdminActivity: Identifiable {
    let id: String
    let title: String
    let timestamp: Date
    let type: ActivityType
}

enum ActivityType {
    case user
    case dataset
    case system
    
    var icon: String {
        switch self {
        case .user: return "person.fill"
        case .dataset: return "doc.text.fill"
        case .system: return "gear.fill"
        }
    }
    
    var color: Color {
        switch self {
        case .user: return Theme.primary
        case .dataset: return Theme.success
        case .system: return Theme.accent
        }
    }
}

struct AdminActivityRow: View {
    let activity: AdminActivity
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: activity.type.icon)
                .foregroundColor(activity.type.color)
                .frame(width: 20)
            
            VStack(alignment: .leading, spacing: Theme.spacingXS) {
                Text(activity.title)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Text(activity.timestamp, style: .relative)
                    .font(Theme.caption)
                    .foregroundColor(Theme.textSecondaryLight)
            }
            
            Spacer()
        }
        .padding(Theme.spacingS)
    }
}

struct DatasetModeration: Identifiable {
    let id: String
    let filename: String
    let uploadedBy: String
    let uploadedAt: Date
    let fileSize: Double // in MB
    let status: ModerationStatus
}

enum ModerationStatus {
    case pending
    case approved
    case rejected
    
    var displayName: String {
        switch self {
        case .pending: return "Pending"
        case .approved: return "Approved"
        case .rejected: return "Rejected"
        }
    }
    
    var color: Color {
        switch self {
        case .pending: return Theme.warning
        case .approved: return Theme.success
        case .rejected: return Theme.danger
        }
    }
}

struct PendingDatasetRow: View {
    let dataset: DatasetModeration
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: "doc.text.fill")
                .foregroundColor(Theme.primary)
                .frame(width: 24)
            
            VStack(alignment: .leading, spacing: Theme.spacingXS) {
                Text(dataset.filename)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                    .lineLimit(1)
                
                Text("by \(dataset.uploadedBy) • \(dataset.fileSize, specifier: "%.1f") MB")
                    .font(Theme.caption)
                    .foregroundColor(Theme.textSecondaryLight)
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: Theme.spacingXS) {
                Text(dataset.status.displayName)
                    .font(Theme.caption)
                    .fontWeight(.medium)
                    .padding(.horizontal, Theme.spacingS)
                    .padding(.vertical, Theme.spacingXS)
                    .background(dataset.status.color.opacity(0.2))
                    .foregroundColor(dataset.status.color)
                    .cornerRadius(Theme.radiusS)
                
                Text(dataset.uploadedAt, style: .relative)
                    .font(Theme.caption)
                    .foregroundColor(Theme.textSecondaryLight)
            }
        }
        .padding(Theme.spacingM)
        .cardStyle()
    }
}

#Preview {
    AdminDashboardView()
        .environmentObject(AuthManager())
}
