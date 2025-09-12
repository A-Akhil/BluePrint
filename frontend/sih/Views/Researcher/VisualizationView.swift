//
//  VisualizationView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import Charts

struct VisualizationView: View {
    @StateObject private var apiService = APIService.shared
    @State private var selectedTab = 0
    @State private var analysisId = ""
    @State private var isLoading = false
    @State private var showAlert = false
    @State private var alertMessage = ""
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Analysis ID Input
                VStack(spacing: Theme.spacingM) {
                    Text("Enter Analysis ID")
                        .font(Theme.title3)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    HStack {
                        TextField("Analysis ID", text: $analysisId)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                        
                        Button("Load") {
                            loadVisualization()
                        }
                        .primaryButtonStyle()
                        .disabled(analysisId.isEmpty || isLoading)
                    }
                }
                .padding(Theme.spacingL)
                .background(Theme.surfaceLight)
                
                if !analysisId.isEmpty {
                    // Tab Selection
                    Picker("Visualization Type", selection: $selectedTab) {
                        Text("Taxonomy").tag(0)
                        Text("Phylogeny").tag(1)
                        Text("Biodiversity").tag(2)
                        Text("Abundance").tag(3)
                    }
                    .pickerStyle(SegmentedPickerStyle())
                    .padding(Theme.spacingL)
                    
                    // Content
                    TabView(selection: $selectedTab) {
                        TaxonomyTreeView(analysisId: analysisId)
                            .tag(0)
                        
                        PhylogenyView(analysisId: analysisId)
                            .tag(1)
                        
                        BiodiversityChartsView(analysisId: analysisId)
                            .tag(2)
                        
                        AbundanceChartsView(analysisId: analysisId)
                            .tag(3)
                    }
                    .tabViewStyle(PageTabViewStyle(indexDisplayMode: .never))
                } else {
                    VStack(spacing: Theme.spacingM) {
                        Image(systemName: "chart.bar.fill")
                            .font(.system(size: 60))
                            .foregroundColor(Theme.primary)
                        
                        Text("Enter an Analysis ID to view visualizations")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                            .multilineTextAlignment(.center)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Visualizations")
            .navigationBarTitleDisplayMode(.large)
        }
        .alert("Error", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text(alertMessage)
        }
    }
    
    private func loadVisualization() {
        isLoading = true
        // Visualization will be loaded by individual views
        isLoading = false
    }
}

struct TaxonomyTreeView: View {
    let analysisId: String
    @State private var taxonomyData: [String: Any] = [:]
    @State private var isLoading = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: Theme.spacingL) {
                Text("Taxonomic Tree")
                    .font(Theme.title2)
                    .foregroundColor(Theme.textPrimaryLight)
                
                if isLoading {
                    ProgressView("Loading taxonomy data...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    // Placeholder for taxonomic tree visualization
                    VStack(spacing: Theme.spacingM) {
                        Image(systemName: "tree.fill")
                            .font(.system(size: 80))
                            .foregroundColor(Theme.primary)
                        
                        Text("Taxonomic Tree Visualization")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Text("Interactive taxonomic tree will be displayed here")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                            .multilineTextAlignment(.center)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(Theme.spacingXL)
                    .cardStyle()
                }
            }
            .padding(Theme.spacingL)
        }
        .onAppear {
            loadTaxonomyData()
        }
    }
    
    private func loadTaxonomyData() {
        isLoading = true
        // Load taxonomy data from API
        isLoading = false
    }
}

struct PhylogenyView: View {
    let analysisId: String
    @State private var phylogenyData: [String: Any] = [:]
    @State private var isLoading = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: Theme.spacingL) {
                Text("Phylogenetic Tree")
                    .font(Theme.title2)
                    .foregroundColor(Theme.textPrimaryLight)
                
                if isLoading {
                    ProgressView("Loading phylogeny data...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    // Placeholder for phylogenetic tree visualization
                    VStack(spacing: Theme.spacingM) {
                        Image(systemName: "network")
                            .font(.system(size: 80))
                            .foregroundColor(Theme.accent)
                        
                        Text("Phylogenetic Tree Visualization")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Text("Interactive phylogenetic tree will be displayed here")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                            .multilineTextAlignment(.center)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(Theme.spacingXL)
                    .cardStyle()
                }
            }
            .padding(Theme.spacingL)
        }
        .onAppear {
            loadPhylogenyData()
        }
    }
    
    private func loadPhylogenyData() {
        isLoading = true
        // Load phylogeny data from API
        isLoading = false
    }
}

struct BiodiversityChartsView: View {
    let analysisId: String
    @State private var biodiversityData: [String: Any] = [:]
    @State private var isLoading = false
    @State private var chartData: [BiodiversityDataPoint] = []
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: Theme.spacingL) {
                Text("Biodiversity Analysis")
                    .font(Theme.title2)
                    .foregroundColor(Theme.textPrimaryLight)
                
                if isLoading {
                    ProgressView("Loading biodiversity data...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    VStack(spacing: Theme.spacingL) {
                        // Species Richness Chart
                        VStack(alignment: .leading, spacing: Theme.spacingM) {
                            Text("Species Richness")
                                .font(Theme.title3)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Chart(chartData) { dataPoint in
                                BarMark(
                                    x: .value("Category", dataPoint.category),
                                    y: .value("Count", dataPoint.value)
                                )
                                .foregroundStyle(Theme.primary.gradient)
                            }
                            .frame(height: 200)
                            .padding(Theme.spacingM)
                            .cardStyle()
                        }
                        
                        // Diversity Index Chart
                        VStack(alignment: .leading, spacing: Theme.spacingM) {
                            Text("Diversity Indices")
                                .font(Theme.title3)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Chart(chartData) { dataPoint in
                                LineMark(
                                    x: .value("Category", dataPoint.category),
                                    y: .value("Count", dataPoint.value)
                                )
                                .foregroundStyle(Theme.accent.gradient)
                                .interpolationMethod(.catmullRom)
                            }
                            .frame(height: 200)
                            .padding(Theme.spacingM)
                            .cardStyle()
                        }
                    }
                }
            }
            .padding(Theme.spacingL)
        }
        .onAppear {
            loadBiodiversityData()
        }
    }
    
    private func loadBiodiversityData() {
        isLoading = true
        
        // Generate sample data for demonstration
        chartData = [
            BiodiversityDataPoint(category: "Bacteria", value: 45),
            BiodiversityDataPoint(category: "Archaea", value: 12),
            BiodiversityDataPoint(category: "Eukarya", value: 78),
            BiodiversityDataPoint(category: "Viruses", value: 23),
            BiodiversityDataPoint(category: "Unknown", value: 8)
        ]
        
        isLoading = false
    }
}

struct AbundanceChartsView: View {
    let analysisId: String
    @State private var abundanceData: [String: Any] = [:]
    @State private var isLoading = false
    @State private var abundanceChartData: [AbundanceDataPoint] = []
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: Theme.spacingL) {
                Text("Species Abundance")
                    .font(Theme.title2)
                    .foregroundColor(Theme.textPrimaryLight)
                
                if isLoading {
                    ProgressView("Loading abundance data...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    VStack(spacing: Theme.spacingL) {
                        // Abundance Distribution
                        VStack(alignment: .leading, spacing: Theme.spacingM) {
                            Text("Abundance Distribution")
                                .font(Theme.title3)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Chart(abundanceChartData) { dataPoint in
                                BarMark(
                                    x: .value("Species", dataPoint.species),
                                    y: .value("Abundance", dataPoint.abundance)
                                )
                                .foregroundStyle(Theme.secondary.gradient)
                            }
                            .frame(height: 300)
                            .padding(Theme.spacingM)
                            .cardStyle()
                        }
                        
                        // Relative Abundance Pie Chart
                        VStack(alignment: .leading, spacing: Theme.spacingM) {
                            Text("Relative Abundance")
                                .font(Theme.title3)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Chart(abundanceChartData) { dataPoint in
                                SectorMark(
                                    angle: .value("Abundance", dataPoint.abundance),
                                    innerRadius: .ratio(0.5),
                                    angularInset: 2
                                )
                                .foregroundStyle(by: .value("Species", dataPoint.species))
                            }
                            .frame(height: 250)
                            .padding(Theme.spacingM)
                            .cardStyle()
                        }
                    }
                }
            }
            .padding(Theme.spacingL)
        }
        .onAppear {
            loadAbundanceData()
        }
    }
    
    private func loadAbundanceData() {
        isLoading = true
        
        // Generate sample data for demonstration
        abundanceChartData = [
            AbundanceDataPoint(species: "Species A", abundance: 150),
            AbundanceDataPoint(species: "Species B", abundance: 120),
            AbundanceDataPoint(species: "Species C", abundance: 95),
            AbundanceDataPoint(species: "Species D", abundance: 80),
            AbundanceDataPoint(species: "Species E", abundance: 60),
            AbundanceDataPoint(species: "Species F", abundance: 45),
            AbundanceDataPoint(species: "Species G", abundance: 30),
            AbundanceDataPoint(species: "Species H", abundance: 20)
        ]
        
        isLoading = false
    }
}

// MARK: - Data Models
struct BiodiversityDataPoint: Identifiable {
    let id = UUID()
    let category: String
    let value: Double
}

struct AbundanceDataPoint: Identifiable {
    let id = UUID()
    let species: String
    let abundance: Double
}

#Preview {
    VisualizationView()
}
