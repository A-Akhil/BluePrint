//
//  SystemMonitoringView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import Charts

struct SystemMonitoringView: View {
    @State private var systemMetrics = SystemMetrics()
    @State private var recentJobs: [SystemJob] = []
    @State private var errorLogs: [ErrorLog] = []
    @State private var isLoading = false
    @State private var selectedTimeRange: TimeRange = .last24Hours
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.spacingL) {
                    // Time Range Selector
                    Picker("Time Range", selection: $selectedTimeRange) {
                        ForEach(TimeRange.allCases, id: \.self) { range in
                            Text(range.displayName).tag(range)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                    .padding(.horizontal, Theme.spacingL)
                    
                    // System Metrics
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("System Performance")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: Theme.spacingM) {
                            MetricCard(
                                title: "CPU Usage",
                                value: "\(Int(systemMetrics.cpuUsage * 100))%",
                                icon: "cpu.fill",
                                color: systemMetrics.cpuUsage > 0.8 ? Theme.danger : Theme.success
                            )
                            
                            MetricCard(
                                title: "Memory Usage",
                                value: "\(Int(systemMetrics.memoryUsage * 100))%",
                                icon: "memorychip.fill",
                                color: systemMetrics.memoryUsage > 0.8 ? Theme.danger : Theme.success
                            )
                            
                            MetricCard(
                                title: "Disk Usage",
                                value: "\(Int(systemMetrics.diskUsage * 100))%",
                                icon: "internaldrive.fill",
                                color: systemMetrics.diskUsage > 0.9 ? Theme.danger : Theme.warning
                            )
                            
                            MetricCard(
                                title: "Network I/O",
                                value: String(format: "%.1f MB/s", systemMetrics.networkIO),
                                icon: "network",
                                color: Theme.accent
                            )
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Performance Chart
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Performance Over Time")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Chart(systemMetrics.performanceData) { dataPoint in
                            LineMark(
                                x: .value("Time", dataPoint.timestamp),
                                y: .value("CPU", dataPoint.cpuUsage)
                            )
                            .foregroundStyle(Theme.primary.gradient)
                            .interpolationMethod(.catmullRom)
                            
                            LineMark(
                                x: .value("Time", dataPoint.timestamp),
                                y: .value("Memory", dataPoint.memoryUsage)
                            )
                            .foregroundStyle(Theme.accent.gradient)
                            .interpolationMethod(.catmullRom)
                        }
                        .frame(height: 200)
                        .padding(Theme.spacingM)
                        .cardStyle()
                    }
                    .padding(.horizontal, Theme.spacingL)
                    
                    // Recent Jobs
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Recent Jobs")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        LazyVStack(spacing: Theme.spacingS) {
                            ForEach(recentJobs.prefix(5)) { job in
                                JobRow(job: job)
                            }
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Error Logs
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Recent Errors")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        LazyVStack(spacing: Theme.spacingS) {
                            ForEach(errorLogs.prefix(5)) { error in
                                ErrorRow(error: error)
                            }
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    Spacer(minLength: Theme.spacingXL)
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("System Monitoring")
            .navigationBarTitleDisplayMode(.large)
        }
        .onAppear {
            loadSystemData()
        }
    }
    
    private func loadSystemData() {
        isLoading = true
        
        // Generate sample data
        systemMetrics = SystemMetrics(
            cpuUsage: 0.65,
            memoryUsage: 0.72,
            diskUsage: 0.45,
            networkIO: 12.5,
            performanceData: generatePerformanceData()
        )
        
        recentJobs = [
            SystemJob(
                id: "1",
                name: "Sequence Analysis",
                status: .running,
                progress: 0.75,
                startedAt: Date().addingTimeInterval(-1800)
            ),
            SystemJob(
                id: "2",
                name: "Data Backup",
                status: .completed,
                progress: 1.0,
                startedAt: Date().addingTimeInterval(-3600)
            ),
            SystemJob(
                id: "3",
                name: "Report Generation",
                status: .failed,
                progress: 0.3,
                startedAt: Date().addingTimeInterval(-7200)
            )
        ]
        
        errorLogs = [
            ErrorLog(
                id: "1",
                message: "Database connection timeout",
                level: .error,
                timestamp: Date().addingTimeInterval(-900)
            ),
            ErrorLog(
                id: "2",
                message: "API rate limit exceeded",
                level: .warning,
                timestamp: Date().addingTimeInterval(-1800)
            ),
            ErrorLog(
                id: "3",
                message: "File upload failed",
                level: .error,
                timestamp: Date().addingTimeInterval(-2700)
            )
        ]
        
        isLoading = false
    }
    
    private func generatePerformanceData() -> [PerformanceDataPoint] {
        let now = Date()
        return (0..<24).map { hour in
            PerformanceDataPoint(
                timestamp: now.addingTimeInterval(-Double(hour) * 3600),
                cpuUsage: Double.random(in: 0.3...0.8),
                memoryUsage: Double.random(in: 0.4...0.9)
            )
        }
    }
}

struct SystemMetrics {
    var cpuUsage: Double = 0.0
    var memoryUsage: Double = 0.0
    var diskUsage: Double = 0.0
    var networkIO: Double = 0.0
    var performanceData: [PerformanceDataPoint] = []
}

struct PerformanceDataPoint: Identifiable {
    let id = UUID()
    let timestamp: Date
    let cpuUsage: Double
    let memoryUsage: Double
}

enum TimeRange: String, CaseIterable {
    case lastHour = "1h"
    case last24Hours = "24h"
    case last7Days = "7d"
    case last30Days = "30d"
    
    var displayName: String {
        switch self {
        case .lastHour: return "1 Hour"
        case .last24Hours: return "24 Hours"
        case .last7Days: return "7 Days"
        case .last30Days: return "30 Days"
        }
    }
}

struct MetricCard: View {
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
                .font(Theme.title3)
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

struct SystemJob: Identifiable {
    let id: String
    let name: String
    let status: JobStatus
    let progress: Double
    let startedAt: Date
}

enum JobStatus {
    case pending
    case running
    case completed
    case failed
    
    var displayName: String {
        switch self {
        case .pending: return "Pending"
        case .running: return "Running"
        case .completed: return "Completed"
        case .failed: return "Failed"
        }
    }
    
    var color: Color {
        switch self {
        case .pending: return Theme.warning
        case .running: return Theme.info
        case .completed: return Theme.success
        case .failed: return Theme.danger
        }
    }
}

struct JobRow: View {
    let job: SystemJob
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: "gear")
                .foregroundColor(job.status.color)
                .frame(width: 20)
            
            VStack(alignment: .leading, spacing: Theme.spacingXS) {
                Text(job.name)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                HStack {
                    Text(job.status.displayName)
                        .font(Theme.caption)
                        .fontWeight(.medium)
                        .padding(.horizontal, Theme.spacingS)
                        .padding(.vertical, Theme.spacingXS)
                        .background(job.status.color.opacity(0.2))
                        .foregroundColor(job.status.color)
                        .cornerRadius(Theme.radiusS)
                    
                    Text(job.startedAt, style: .relative)
                        .font(Theme.caption)
                        .foregroundColor(Theme.textSecondaryLight)
                }
            }
            
            Spacer()
            
            if job.status == .running {
                ProgressView(value: job.progress)
                    .progressViewStyle(LinearProgressViewStyle(tint: job.status.color))
                    .frame(width: 60)
            }
        }
        .padding(Theme.spacingS)
    }
}

struct ErrorLog: Identifiable {
    let id: String
    let message: String
    let level: ErrorLevel
    let timestamp: Date
}

enum ErrorLevel {
    case info
    case warning
    case error
    case critical
    
    var displayName: String {
        switch self {
        case .info: return "Info"
        case .warning: return "Warning"
        case .error: return "Error"
        case .critical: return "Critical"
        }
    }
    
    var color: Color {
        switch self {
        case .info: return Theme.info
        case .warning: return Theme.warning
        case .error: return Theme.danger
        case .critical: return Theme.danger
        }
    }
    
    var icon: String {
        switch self {
        case .info: return "info.circle.fill"
        case .warning: return "exclamationmark.triangle.fill"
        case .error: return "xmark.circle.fill"
        case .critical: return "exclamationmark.octagon.fill"
        }
    }
}

struct ErrorRow: View {
    let error: ErrorLog
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: error.level.icon)
                .foregroundColor(error.level.color)
                .frame(width: 20)
            
            VStack(alignment: .leading, spacing: Theme.spacingXS) {
                Text(error.message)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                    .lineLimit(2)
                
                HStack {
                    Text(error.level.displayName)
                        .font(Theme.caption)
                        .fontWeight(.medium)
                        .padding(.horizontal, Theme.spacingS)
                        .padding(.vertical, Theme.spacingXS)
                        .background(error.level.color.opacity(0.2))
                        .foregroundColor(error.level.color)
                        .cornerRadius(Theme.radiusS)
                    
                    Text(error.timestamp, style: .relative)
                        .font(Theme.caption)
                        .foregroundColor(Theme.textSecondaryLight)
                }
            }
            
            Spacer()
        }
        .padding(Theme.spacingS)
    }
}

#Preview {
    SystemMonitoringView()
}
