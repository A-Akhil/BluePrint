//
//  UploadView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import UniformTypeIdentifiers
import Combine

struct UploadView: View {
    @StateObject private var apiService = APIService.shared
    @State private var selectedFile: URL?
    @State private var selectedFileType: FileType = .csv
    @State private var metadata = SequenceMetadata(
        samplingDate: nil,
        temperature: nil,
        salinity: nil,
        depth: nil,
        latitude: nil,
        longitude: nil,
        location: nil,
        notes: nil
    )
    @State private var isUploading = false
    @State private var uploadProgress: Double = 0
    @State private var showFilePicker = false
    @State private var showAlert = false
    @State private var alertMessage = ""
    @State private var uploadSuccess = false
    @State private var cancellables = Set<AnyCancellable>()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.spacingL) {
                    // File Selection Section
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Select File")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Button(action: { showFilePicker = true }) {
                            VStack(spacing: Theme.spacingM) {
                                Image(systemName: selectedFile == nil ? "plus.circle" : "checkmark.circle.fill")
                                    .font(.system(size: 40))
                                    .foregroundColor(selectedFile == nil ? Theme.primary : Theme.success)
                                
                                if let file = selectedFile {
                                    Text(file.lastPathComponent)
                                        .font(Theme.callout)
                                        .foregroundColor(Theme.textPrimaryLight)
                                        .lineLimit(2)
                                    
                                    Text("Tap to change file")
                                        .font(Theme.caption)
                                        .foregroundColor(Theme.textSecondaryLight)
                                } else {
                                    Text("Tap to select file")
                                        .font(Theme.callout)
                                        .foregroundColor(Theme.textSecondaryLight)
                                }
                            }
                            .frame(maxWidth: .infinity)
                            .frame(height: 120)
                            .background(Theme.surfaceLight)
                            .cornerRadius(Theme.radiusL)
                            .overlay(
                                RoundedRectangle(cornerRadius: Theme.radiusL)
                                    .stroke(Theme.primary.opacity(0.3), lineWidth: 2)
                            )
                        }
                        .buttonStyle(PlainButtonStyle())
                        
                        // File Type Picker
                        Picker("File Type", selection: $selectedFileType) {
                            ForEach(FileType.allCases, id: \.self) { type in
                                Text(type.displayName).tag(type)
                            }
                        }
                        .pickerStyle(SegmentedPickerStyle())
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Metadata Section
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Metadata")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        VStack(spacing: Theme.spacingM) {
                            // Sampling Date
                            VStack(alignment: .leading, spacing: Theme.spacingS) {
                                Text("Sampling Date")
                                    .font(Theme.callout)
                                    .foregroundColor(Theme.textPrimaryLight)
                                
                                DatePicker("", selection: Binding(
                                    get: { metadata.samplingDate ?? Date() },
                                    set: { metadata.samplingDate = $0 }
                                ), displayedComponents: .date)
                                .datePickerStyle(CompactDatePickerStyle())
                            }
                            
                            // Location
                            VStack(alignment: .leading, spacing: Theme.spacingS) {
                                Text("Location")
                                    .font(Theme.callout)
                                    .foregroundColor(Theme.textPrimaryLight)
                                
                                TextField("Enter location name", text: Binding(
                                    get: { metadata.location ?? "" },
                                    set: { metadata.location = $0.isEmpty ? nil : $0 }
                                ))
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                            }
                            
                            // Coordinates
                            HStack(spacing: Theme.spacingM) {
                                VStack(alignment: .leading, spacing: Theme.spacingS) {
                                    Text("Latitude")
                                        .font(Theme.callout)
                                        .foregroundColor(Theme.textPrimaryLight)
                                    
                                    TextField("0.0", value: Binding(
                                        get: { metadata.latitude ?? 0.0 },
                                        set: { metadata.latitude = $0 }
                                    ), format: .number)
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .keyboardType(.decimalPad)
                                }
                                
                                VStack(alignment: .leading, spacing: Theme.spacingS) {
                                    Text("Longitude")
                                        .font(Theme.callout)
                                        .foregroundColor(Theme.textPrimaryLight)
                                    
                                    TextField("0.0", value: Binding(
                                        get: { metadata.longitude ?? 0.0 },
                                        set: { metadata.longitude = $0 }
                                    ), format: .number)
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .keyboardType(.decimalPad)
                                }
                            }
                            
                            // Environmental Data
                            HStack(spacing: Theme.spacingM) {
                                VStack(alignment: .leading, spacing: Theme.spacingS) {
                                    Text("Temperature (°C)")
                                        .font(Theme.callout)
                                        .foregroundColor(Theme.textPrimaryLight)
                                    
                                    TextField("0.0", value: Binding(
                                        get: { metadata.temperature ?? 0.0 },
                                        set: { metadata.temperature = $0 }
                                    ), format: .number)
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .keyboardType(.decimalPad)
                                }
                                
                                VStack(alignment: .leading, spacing: Theme.spacingS) {
                                    Text("Salinity (PSU)")
                                        .font(Theme.callout)
                                        .foregroundColor(Theme.textPrimaryLight)
                                    
                                    TextField("0.0", value: Binding(
                                        get: { metadata.salinity ?? 0.0 },
                                        set: { metadata.salinity = $0 }
                                    ), format: .number)
                                    .textFieldStyle(RoundedBorderTextFieldStyle())
                                    .keyboardType(.decimalPad)
                                }
                            }
                            
                            // Depth
                            VStack(alignment: .leading, spacing: Theme.spacingS) {
                                Text("Depth (m)")
                                    .font(Theme.callout)
                                    .foregroundColor(Theme.textPrimaryLight)
                                
                                TextField("0.0", value: Binding(
                                    get: { metadata.depth ?? 0.0 },
                                    set: { metadata.depth = $0 }
                                ), format: .number)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.decimalPad)
                            }
                            
                            // Notes
                            VStack(alignment: .leading, spacing: Theme.spacingS) {
                                Text("Notes")
                                    .font(Theme.callout)
                                    .foregroundColor(Theme.textPrimaryLight)
                                
                                TextField("Additional notes...", text: Binding(
                                    get: { metadata.notes ?? "" },
                                    set: { metadata.notes = $0.isEmpty ? nil : $0 }
                                ), axis: .vertical)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .lineLimit(3...6)
                            }
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Upload Button
                    Button(action: uploadFile) {
                        HStack {
                            if isUploading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                    .scaleEffect(0.8)
                            }
                            Text(isUploading ? "Uploading..." : "Upload Sequence")
                        }
                        .frame(maxWidth: .infinity)
                    }
                    .primaryButtonStyle()
                    .disabled(selectedFile == nil || isUploading)
                    .padding(.horizontal, Theme.spacingL)
                    
                    // Progress Bar
                    if isUploading {
                        VStack(spacing: Theme.spacingS) {
                            ProgressView(value: uploadProgress, total: 1.0)
                                .progressViewStyle(LinearProgressViewStyle(tint: Theme.primary))
                            
                            Text("\(Int(uploadProgress * 100))% Complete")
                                .font(Theme.caption)
                                .foregroundColor(Theme.textSecondaryLight)
                        }
                        .padding(.horizontal, Theme.spacingL)
                    }
                    
                    Spacer(minLength: Theme.spacingXL)
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Upload Data")
            .navigationBarTitleDisplayMode(.large)
        }
        .fileImporter(
            isPresented: $showFilePicker,
            allowedContentTypes: [UTType.data],
            allowsMultipleSelection: false
        ) { result in
            switch result {
            case .success(let urls):
                if let url = urls.first {
                    selectedFile = url
                }
            case .failure(let error):
                alertMessage = "Failed to select file: \(error.localizedDescription)"
                showAlert = true
            }
        }
        .alert(uploadSuccess ? "Success" : "Error", isPresented: $showAlert) {
            Button("OK") {
                if uploadSuccess {
                    resetForm()
                }
            }
        } message: {
            Text(alertMessage)
        }
    }
    
    private func uploadFile() {
        guard let fileURL = selectedFile else { return }
        
        isUploading = true
        uploadProgress = 0
        
        do {
            let fileData = try Data(contentsOf: fileURL)
            let filename = fileURL.lastPathComponent
            
            // Simulate progress
            Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
                uploadProgress += 0.1
                if uploadProgress >= 1.0 {
                    timer.invalidate()
                }
            }
            
            apiService.uploadSequence(
                fileData: fileData,
                filename: filename,
                fileType: selectedFileType,
                metadata: metadata
            )
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    isUploading = false
                    if case .failure(let error) = completion {
                        alertMessage = "Upload failed: \(error.message)"
                        showAlert = true
                    }
                },
                receiveValue: { response in
                    uploadSuccess = true
                    alertMessage = "File uploaded successfully! Analysis ID: \(response.analysisId)"
                    showAlert = true
                }
            )
            .store(in: &cancellables)
            
        } catch {
            isUploading = false
            alertMessage = "Failed to read file: \(error.localizedDescription)"
            showAlert = true
        }
    }
    
    private func resetForm() {
        selectedFile = nil
        metadata = SequenceMetadata(
            samplingDate: nil,
            temperature: nil,
            salinity: nil,
            depth: nil,
            latitude: nil,
            longitude: nil,
            location: nil,
            notes: nil
        )
        uploadProgress = 0
        uploadSuccess = false
    }
}

#Preview {
    UploadView()
}
