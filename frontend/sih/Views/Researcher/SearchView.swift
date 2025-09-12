//
//  SearchView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import Combine

struct SearchView: View {
    @StateObject private var apiService = APIService.shared
    @State private var searchQuery = ""
    @State private var searchResults: [SearchResult] = []
    @State private var isLoading = false
    @State private var showFilters = false
    @State private var filters = SearchFilters()
    @State private var selectedExportFormat: ExportFormat = .csv
    @State private var showExportOptions = false
    @State private var currentPage = 1
    @State private var totalPages = 1
    @State private var showAlert = false
    @State private var alertMessage = ""
    @State private var cancellables = Set<AnyCancellable>()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Search Bar
                VStack(spacing: Theme.spacingM) {
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundColor(Theme.textSecondaryLight)
                        
                        TextField("Search species, taxa, or keywords...", text: $searchQuery)
                            .textFieldStyle(PlainTextFieldStyle())
                            .onSubmit {
                                performSearch()
                            }
                        
                        if !searchQuery.isEmpty {
                            Button(action: { searchQuery = "" }) {
                                Image(systemName: "xmark.circle.fill")
                                    .foregroundColor(Theme.textSecondaryLight)
                            }
                        }
                    }
                    .padding(Theme.spacingM)
                    .background(Theme.surfaceLight)
                    .cornerRadius(Theme.radiusM)
                    
                    HStack {
                        Button(action: { showFilters.toggle() }) {
                            HStack {
                                Image(systemName: "line.3.horizontal.decrease.circle")
                                Text("Filters")
                            }
                            .font(Theme.callout)
                            .foregroundColor(Theme.primary)
                        }
                        
                        Spacer()
                        
                        if !searchResults.isEmpty {
                            Button(action: { showExportOptions = true }) {
                                HStack {
                                    Image(systemName: "square.and.arrow.up")
                                    Text("Export")
                                }
                                .font(Theme.callout)
                                .foregroundColor(Theme.primary)
                            }
                        }
                    }
                }
                .padding(Theme.spacingL)
                .background(Theme.backgroundLight)
                
                // Filters Panel
                if showFilters {
                    FilterPanel(filters: $filters) {
                        performSearch()
                    }
                    .transition(.slide)
                }
                
                // Results
                if isLoading {
                    VStack(spacing: Theme.spacingM) {
                        ProgressView()
                            .scaleEffect(1.2)
                        Text("Searching...")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if searchResults.isEmpty && !searchQuery.isEmpty {
                    VStack(spacing: Theme.spacingM) {
                        Image(systemName: "magnifyingglass")
                            .font(.system(size: 50))
                            .foregroundColor(Theme.textSecondaryLight)
                        
                        Text("No results found")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        Text("Try adjusting your search terms or filters")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textSecondaryLight)
                            .multilineTextAlignment(.center)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    ScrollView {
                        LazyVStack(spacing: Theme.spacingM) {
                            ForEach(searchResults) { result in
                                SearchResultRow(result: result)
                            }
                            
                            // Pagination
                            if totalPages > 1 {
                                HStack {
                                    Button("Previous") {
                                        if currentPage > 1 {
                                            currentPage -= 1
                                            performSearch()
                                        }
                                    }
                                    .disabled(currentPage <= 1)
                                    
                                    Spacer()
                                    
                                    Text("Page \(currentPage) of \(totalPages)")
                                        .font(Theme.callout)
                                        .foregroundColor(Theme.textSecondaryLight)
                                    
                                    Spacer()
                                    
                                    Button("Next") {
                                        if currentPage < totalPages {
                                            currentPage += 1
                                            performSearch()
                                        }
                                    }
                                    .disabled(currentPage >= totalPages)
                                }
                                .padding(Theme.spacingL)
                            }
                        }
                        .padding(.horizontal, Theme.spacingL)
                    }
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Search")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Search") {
                        performSearch()
                    }
                    .disabled(searchQuery.isEmpty)
                }
            }
        }
        .sheet(isPresented: $showExportOptions) {
            ExportOptionsView(
                results: searchResults,
                format: $selectedExportFormat,
                isPresented: $showExportOptions
            )
        }
        .alert("Error", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text(alertMessage)
        }
    }
    
    private func performSearch() {
        isLoading = true
        
        let request = SearchRequest(
            query: searchQuery.isEmpty ? nil : searchQuery,
            species: filters.selectedSpecies.isEmpty ? nil : filters.selectedSpecies,
            taxa: filters.selectedTaxa.isEmpty ? nil : filters.selectedTaxa,
            dateRange: filters.dateRange,
            location: filters.locationFilter,
            rarity: filters.selectedRarity,
            novelty: filters.selectedNovelty,
            confidence: filters.confidenceRange,
            page: currentPage,
            limit: 20
        )
        
        apiService.searchSequences(request: request)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    isLoading = false
                    if case .failure(let error) = completion {
                        alertMessage = "Search failed: \(error.message)"
                        showAlert = true
                    }
                },
                receiveValue: { response in
                    searchResults = response.results
                    totalPages = response.totalPages
                }
            )
            .store(in: &cancellables)
    }
}

struct SearchFilters {
    var selectedSpecies: [String] = []
    var selectedTaxa: [String] = []
    var dateRange: DateRange?
    var locationFilter: LocationFilter?
    var selectedRarity: RarityFilter?
    var selectedNovelty: NoveltyFilter?
    var confidenceRange: ConfidenceFilter?
    
    mutating func updateDateRange(startDate: Date, endDate: Date) {
        dateRange = DateRange(startDate: startDate, endDate: endDate)
    }
    
    mutating func updateConfidenceRange(min: Double, max: Double) {
        confidenceRange = ConfidenceFilter(minConfidence: min, maxConfidence: max)
    }
}

struct FilterPanel: View {
    @Binding var filters: SearchFilters
    let onApply: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.spacingM) {
            Text("Filters")
                .font(Theme.title3)
                .foregroundColor(Theme.textPrimaryLight)
            
            // Date Range
            VStack(alignment: .leading, spacing: Theme.spacingS) {
                Text("Date Range")
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                HStack {
                    DatePicker("From", selection: Binding(
                        get: { filters.dateRange?.startDate ?? Date() },
                        set: { 
                            let endDate = filters.dateRange?.endDate ?? Date()
                            filters.updateDateRange(startDate: $0, endDate: endDate)
                        }
                    ), displayedComponents: .date)
                    .datePickerStyle(CompactDatePickerStyle())
                    
                    DatePicker("To", selection: Binding(
                        get: { filters.dateRange?.endDate ?? Date() },
                        set: { 
                            let startDate = filters.dateRange?.startDate ?? Date()
                            filters.updateDateRange(startDate: startDate, endDate: $0)
                        }
                    ), displayedComponents: .date)
                    .datePickerStyle(CompactDatePickerStyle())
                }
            }
            
            // Rarity Filter
            VStack(alignment: .leading, spacing: Theme.spacingS) {
                Text("Rarity")
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Picker("Rarity", selection: $filters.selectedRarity) {
                    Text("All").tag(nil as RarityFilter?)
                    ForEach(RarityFilter.allCases, id: \.self) { rarity in
                        Text(rarity.displayName).tag(rarity as RarityFilter?)
                    }
                }
                .pickerStyle(MenuPickerStyle())
            }
            
            // Novelty Filter
            VStack(alignment: .leading, spacing: Theme.spacingS) {
                Text("Novelty")
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Picker("Novelty", selection: $filters.selectedNovelty) {
                    Text("All").tag(nil as NoveltyFilter?)
                    ForEach(NoveltyFilter.allCases, id: \.self) { novelty in
                        Text(novelty.displayName).tag(novelty as NoveltyFilter?)
                    }
                }
                .pickerStyle(MenuPickerStyle())
            }
            
            // Confidence Range
            VStack(alignment: .leading, spacing: Theme.spacingS) {
                Text("Confidence Range")
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                HStack {
                    Text("Min: \(Int((filters.confidenceRange?.minConfidence ?? 0.0) * 100))%")
                        .font(Theme.caption)
                        .foregroundColor(Theme.textSecondaryLight)
                    
                    Slider(
                        value: Binding(
                            get: { filters.confidenceRange?.minConfidence ?? 0.0 },
                            set: { 
                                let maxConfidence = filters.confidenceRange?.maxConfidence ?? 1.0
                                filters.updateConfidenceRange(min: $0, max: maxConfidence)
                            }
                        ),
                        in: 0...1
                    )
                    
                    Text("Max: \(Int((filters.confidenceRange?.maxConfidence ?? 1.0) * 100))%")
                        .font(Theme.caption)
                        .foregroundColor(Theme.textSecondaryLight)
                }
            }
            
            Button("Apply Filters") {
                onApply()
            }
            .primaryButtonStyle()
        }
        .padding(Theme.spacingL)
        .background(Theme.surfaceLight)
        .cornerRadius(Theme.radiusL)
        .padding(.horizontal, Theme.spacingL)
    }
}

struct SearchResultRow: View {
    let result: SearchResult
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.spacingS) {
            HStack {
                Text(result.species)
                    .font(Theme.headline)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Spacer()
                
                ConfidenceBadge(confidence: result.confidence)
            }
            
            if !result.taxa.isEmpty {
                Text(result.taxa.joined(separator: " • "))
                    .font(Theme.callout)
                    .foregroundColor(Theme.textSecondaryLight)
            }
            
            HStack {
                RarityBadge(rarity: result.rarity)
                NoveltyBadge(novelty: result.novelty)
                
                Spacer()
                
                Text(result.samplingDate, style: .date)
                    .font(Theme.caption)
                    .foregroundColor(Theme.textSecondaryLight)
            }
            
            if let location = result.location.name {
                HStack {
                    Image(systemName: "location.fill")
                        .foregroundColor(Theme.accent)
                    Text(location)
                        .font(Theme.caption)
                        .foregroundColor(Theme.textSecondaryLight)
                }
            }
        }
        .padding(Theme.spacingM)
        .cardStyle()
    }
}

struct ConfidenceBadge: View {
    let confidence: Double
    
    var body: some View {
        Text("\(Int(confidence * 100))%")
            .font(Theme.caption)
            .fontWeight(.medium)
            .padding(.horizontal, Theme.spacingS)
            .padding(.vertical, Theme.spacingXS)
            .background(confidenceColor.opacity(0.2))
            .foregroundColor(confidenceColor)
            .cornerRadius(Theme.radiusS)
    }
    
    private var confidenceColor: Color {
        if confidence >= 0.8 { return Theme.success }
        else if confidence >= 0.6 { return Theme.warning }
        else { return Theme.danger }
    }
}

struct RarityBadge: View {
    let rarity: RarityFilter
    
    var body: some View {
        Text(rarity.displayName)
            .font(Theme.caption)
            .fontWeight(.medium)
            .padding(.horizontal, Theme.spacingS)
            .padding(.vertical, Theme.spacingXS)
            .background(rarityColor.opacity(0.2))
            .foregroundColor(rarityColor)
            .cornerRadius(Theme.radiusS)
    }
    
    private var rarityColor: Color {
        switch rarity {
        case .common: return Theme.success
        case .uncommon: return Theme.info
        case .rare: return Theme.warning
        case .veryRare: return Theme.danger
        }
    }
}

struct NoveltyBadge: View {
    let novelty: NoveltyFilter
    
    var body: some View {
        Text(novelty.displayName)
            .font(Theme.caption)
            .fontWeight(.medium)
            .padding(.horizontal, Theme.spacingS)
            .padding(.vertical, Theme.spacingXS)
            .background(noveltyColor.opacity(0.2))
            .foregroundColor(noveltyColor)
            .cornerRadius(Theme.radiusS)
    }
    
    private var noveltyColor: Color {
        switch novelty {
        case .known: return Theme.success
        case .potentiallyNovel: return Theme.warning
        case .novel: return Theme.secondary
        }
    }
}

enum ExportFormat: String, CaseIterable {
    case csv = "csv"
    case json = "json"
    case pdf = "pdf"
    
    var displayName: String {
        switch self {
        case .csv: return "CSV"
        case .json: return "JSON"
        case .pdf: return "PDF"
        }
    }
}

struct ExportOptionsView: View {
    let results: [SearchResult]
    @Binding var format: ExportFormat
    @Binding var isPresented: Bool
    @State private var isExporting = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.spacingL) {
                Text("Export \(results.count) results")
                    .font(Theme.title3)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Picker("Format", selection: $format) {
                    ForEach(ExportFormat.allCases, id: \.self) { format in
                        Text(format.displayName).tag(format)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
                
                Button("Export") {
                    exportResults()
                }
                .primaryButtonStyle()
                .disabled(isExporting)
                
                if isExporting {
                    ProgressView("Exporting...")
                        .progressViewStyle(CircularProgressViewStyle())
                }
                
                Spacer()
            }
            .padding(Theme.spacingL)
            .navigationTitle("Export Options")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Cancel") {
                        isPresented = false
                    }
                }
            }
        }
    }
    
    private func exportResults() {
        isExporting = true
        // Implement export logic here
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            isExporting = false
            isPresented = false
        }
    }
}

#Preview {
    SearchView()
}
