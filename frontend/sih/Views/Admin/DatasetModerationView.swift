//
//  DatasetModerationView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

struct DatasetModerationView: View {
    @State private var datasets: [DatasetModeration] = []
    @State private var isLoading = false
    @State private var selectedStatus: ModerationStatus? = nil
    @State private var searchText = ""
    @State private var showAlert = false
    @State private var alertMessage = ""
    @State private var selectedDataset: DatasetModeration?
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Filter Bar
                VStack(spacing: Theme.spacingM) {
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundColor(Theme.textSecondaryLight)
                        
                        TextField("Search datasets...", text: $searchText)
                            .textFieldStyle(PlainTextFieldStyle())
                    }
                    .padding(Theme.spacingM)
                    .background(Theme.surfaceLight)
                    .cornerRadius(Theme.radiusM)
                    
                    HStack {
                        Picker("Status", selection: $selectedStatus) {
                            Text("All Status").tag(nil as ModerationStatus?)
                            ForEach([ModerationStatus.pending, .approved, .rejected], id: \.self) { status in
                                Text(status.displayName).tag(status as ModerationStatus?)
                            }
                        }
                        .pickerStyle(MenuPickerStyle())
                        
                        Spacer()
                        
                        Text("\(filteredDatasets.count) datasets")
                            .font(Theme.caption)
                            .foregroundColor(Theme.textSecondaryLight)
                    }
                }
                .padding(Theme.spacingL)
                .background(Theme.backgroundLight)
                
                // Datasets List
                if isLoading {
                    ProgressView("Loading datasets...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    ScrollView {
                        LazyVStack(spacing: Theme.spacingS) {
                            ForEach(filteredDatasets) { dataset in
                                DatasetRow(dataset: dataset) {
                                    selectedDataset = dataset
                                }
                            }
                        }
                        .padding(.horizontal, Theme.spacingL)
                    }
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Dataset Moderation")
            .navigationBarTitleDisplayMode(.large)
        }
        .sheet(item: $selectedDataset) { dataset in
            DatasetDetailView(dataset: dataset, isPresented: .constant(true))
        }
        .alert("Error", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text(alertMessage)
        }
        .onAppear {
            loadDatasets()
        }
    }
    
    private var filteredDatasets: [DatasetModeration] {
        var filtered = datasets
        
        if !searchText.isEmpty {
            filtered = filtered.filter { dataset in
                dataset.filename.localizedCaseInsensitiveContains(searchText) ||
                dataset.uploadedBy.localizedCaseInsensitiveContains(searchText)
            }
        }
        
        if let status = selectedStatus {
            filtered = filtered.filter { $0.status == status }
        }
        
        return filtered.sorted { $0.uploadedAt > $1.uploadedAt }
    }
    
    private func loadDatasets() {
        isLoading = true
        
        // Generate sample datasets
        datasets = [
            DatasetModeration(
                id: "1",
                filename: "marine_samples_2024.csv",
                uploadedBy: "Dr. Sarah Smith",
                uploadedAt: Date().addingTimeInterval(-3600),
                fileSize: 2.5,
                status: .pending
            ),
            DatasetModeration(
                id: "2",
                filename: "deep_sea_sequences.fasta",
                uploadedBy: "Dr. Michael Johnson",
                uploadedAt: Date().addingTimeInterval(-7200),
                fileSize: 15.8,
                status: .pending
            ),
            DatasetModeration(
                id: "3",
                filename: "benthic_community.json",
                uploadedBy: "Dr. Emily Davis",
                uploadedAt: Date().addingTimeInterval(-86400),
                fileSize: 8.2,
                status: .approved
            ),
            DatasetModeration(
                id: "4",
                filename: "invalid_data.csv",
                uploadedBy: "Dr. John Wilson",
                uploadedAt: Date().addingTimeInterval(-172800),
                fileSize: 1.1,
                status: .rejected
            ),
            DatasetModeration(
                id: "5",
                filename: "coral_reef_edna.fasta",
                uploadedBy: "Dr. Lisa Brown",
                uploadedAt: Date().addingTimeInterval(-259200),
                fileSize: 22.3,
                status: .approved
            )
        ]
        
        isLoading = false
    }
}

struct DatasetRow: View {
    let dataset: DatasetModeration
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: Theme.spacingM) {
                // File Icon
                Image(systemName: fileIcon(for: dataset.filename))
                    .font(.title2)
                    .foregroundColor(fileColor(for: dataset.filename))
                    .frame(width: 30)
                
                VStack(alignment: .leading, spacing: Theme.spacingXS) {
                    Text(dataset.filename)
                        .font(Theme.callout)
                        .foregroundColor(Theme.textPrimaryLight)
                        .lineLimit(1)
                    
                    Text("by \(dataset.uploadedBy)")
                        .font(Theme.caption)
                        .foregroundColor(Theme.textSecondaryLight)
                    
                    HStack {
                        Text(String(format: "%.1f MB", dataset.fileSize))
                            .font(Theme.caption)
                            .foregroundColor(Theme.textSecondaryLight)
                        
                        Text("•")
                            .font(Theme.caption)
                            .foregroundColor(Theme.textSecondaryLight)
                        
                        Text(dataset.uploadedAt, style: .relative)
                            .font(Theme.caption)
                            .foregroundColor(Theme.textSecondaryLight)
                    }
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
                    
                    Image(systemName: "chevron.right")
                        .font(.caption)
                        .foregroundColor(Theme.textSecondaryLight)
                }
            }
            .padding(Theme.spacingM)
            .cardStyle()
        }
        .buttonStyle(PlainButtonStyle())
    }
    
    private func fileIcon(for filename: String) -> String {
        let ext = filename.components(separatedBy: ".").last?.lowercased() ?? ""
        switch ext {
        case "csv": return "doc.text.fill"
        case "json": return "doc.text.fill"
        case "fasta": return "dna.helix"
        default: return "doc.fill"
        }
    }
    
    private func fileColor(for filename: String) -> Color {
        let ext = filename.components(separatedBy: ".").last?.lowercased() ?? ""
        switch ext {
        case "csv": return Theme.success
        case "json": return Theme.accent
        case "fasta": return Theme.primary
        default: return Theme.textSecondaryLight
        }
    }
}

struct DatasetDetailView: View {
    let dataset: DatasetModeration
    @Binding var isPresented: Bool
    @State private var showApprovalDialog = false
    @State private var showRejectionDialog = false
    @State private var rejectionReason = ""
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.spacingL) {
                    // File Header
                    VStack(spacing: Theme.spacingM) {
                        Image(systemName: fileIcon(for: dataset.filename))
                            .font(.system(size: 60))
                            .foregroundColor(fileColor(for: dataset.filename))
                        
                        Text(dataset.filename)
                            .font(Theme.title2)
                            .foregroundColor(Theme.textPrimaryLight)
                            .multilineTextAlignment(.center)
                        
                        Text("by \(dataset.uploadedBy)")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // File Details
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("File Details")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        VStack(spacing: Theme.spacingS) {
                            DetailRow(icon: "doc.fill", title: "File Size", value: String(format: "%.1f MB", dataset.fileSize))
                            DetailRow(icon: "calendar", title: "Uploaded", value: dataset.uploadedAt, style: .date)
                            DetailRow(icon: "person.fill", title: "Uploaded By", value: dataset.uploadedBy)
                            DetailRow(icon: "tag.fill", title: "Status", value: dataset.status.displayName)
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // File Preview (placeholder)
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("File Preview")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Text("File content preview would be displayed here")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                            .frame(maxWidth: .infinity)
                            .padding(Theme.spacingXL)
                            .background(Theme.surfaceLight)
                            .cornerRadius(Theme.radiusM)
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Action Buttons
                    if dataset.status == .pending {
                        VStack(spacing: Theme.spacingM) {
                            Button("Approve Dataset") {
                                showApprovalDialog = true
                            }
                            .primaryButtonStyle()
                            
                            Button("Reject Dataset") {
                                showRejectionDialog = true
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding(Theme.spacingM)
                            .background(Theme.danger)
                            .cornerRadius(Theme.radiusM)
                        }
                        .padding(.horizontal, Theme.spacingL)
                    }
                    
                    Spacer()
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Dataset Review")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Close") {
                        isPresented = false
                    }
                }
            }
        }
        .alert("Approve Dataset", isPresented: $showApprovalDialog) {
            Button("Cancel", role: .cancel) { }
            Button("Approve") {
                // Approve dataset
                isPresented = false
            }
        } message: {
            Text("Are you sure you want to approve this dataset?")
        }
        .alert("Reject Dataset", isPresented: $showRejectionDialog) {
            TextField("Reason for rejection", text: $rejectionReason)
            Button("Cancel", role: .cancel) { }
            Button("Reject", role: .destructive) {
                // Reject dataset
                isPresented = false
            }
        }
    }
    
    private func fileIcon(for filename: String) -> String {
        let ext = filename.components(separatedBy: ".").last?.lowercased() ?? ""
        switch ext {
        case "csv": return "doc.text.fill"
        case "json": return "doc.text.fill"
        case "fasta": return "dna.helix"
        default: return "doc.fill"
        }
    }
    
    private func fileColor(for filename: String) -> Color {
        let ext = filename.components(separatedBy: ".").last?.lowercased() ?? ""
        switch ext {
        case "csv": return Theme.success
        case "json": return Theme.accent
        case "fasta": return Theme.primary
        default: return Theme.textSecondaryLight
        }
    }
}

#Preview {
    DatasetModerationView()
}
