//
//  MapView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import MapKit

struct MapView: View {
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 12.0, longitude: 77.0), // Default to Indian Ocean
        span: MKCoordinateSpan(latitudeDelta: 10.0, longitudeDelta: 10.0)
    )
    @State private var selectedAnnotation: SamplingSite?
    @State private var showFilters = false
    @State private var selectedOverlay: MapOverlay = .speciesDistribution
    @State private var samplingSites: [SamplingSite] = []
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            ZStack {
                // Map
                Map(coordinateRegion: $region, annotationItems: samplingSites) { site in
                    MapAnnotation(coordinate: site.coordinate) {
                        SamplingSiteAnnotation(
                            site: site,
                            isSelected: selectedAnnotation?.id == site.id
                        ) {
                            selectedAnnotation = site
                        }
                    }
                }
                .ignoresSafeArea()
                
                // Top Controls
                VStack {
                    HStack {
                        // Filter Button
                        Button(action: { showFilters.toggle() }) {
                            Image(systemName: "line.3.horizontal.decrease.circle.fill")
                                .font(.title2)
                                .foregroundColor(.white)
                                .padding(Theme.spacingM)
                                .background(Theme.primary)
                                .cornerRadius(Theme.radiusL)
                                .shadow(radius: 4)
                        }
                        
                        Spacer()
                        
                        // Overlay Selector
                        Menu {
                            ForEach(MapOverlay.allCases, id: \.self) { overlay in
                                Button(overlay.displayName) {
                                    selectedOverlay = overlay
                                }
                            }
                        } label: {
                            HStack {
                                Image(systemName: "layers.fill")
                                Text(selectedOverlay.displayName)
                            }
                            .font(Theme.callout)
                            .foregroundColor(.white)
                            .padding(Theme.spacingM)
                            .background(Theme.accent)
                            .cornerRadius(Theme.radiusL)
                            .shadow(radius: 4)
                        }
                    }
                    .padding(.horizontal, Theme.spacingL)
                    .padding(.top, Theme.spacingL)
                    
                    Spacer()
                }
                
                // Bottom Sheet
                VStack {
                    Spacer()
                    
                    VStack(spacing: 0) {
                        // Handle
                        RoundedRectangle(cornerRadius: 2)
                            .fill(Theme.textSecondaryLight)
                            .frame(width: 40, height: 4)
                            .padding(.top, Theme.spacingS)
                        
                        if let site = selectedAnnotation {
                            SamplingSiteDetailView(site: site) {
                                selectedAnnotation = nil
                            }
                        } else {
                            MapStatsView(sites: samplingSites)
                        }
                    }
                    .background(Theme.surfaceLight)
                    .cornerRadius(Theme.radiusXL, corners: [.topLeft, .topRight])
                    .shadow(radius: 8)
                }
            }
            .navigationTitle("Sampling Sites")
            .navigationBarTitleDisplayMode(.inline)
            .navigationBarHidden(true)
        }
        .sheet(isPresented: $showFilters) {
            MapFiltersView(
                selectedOverlay: $selectedOverlay,
                isPresented: $showFilters
            )
        }
        .onAppear {
            loadSamplingSites()
        }
    }
    
    private func loadSamplingSites() {
        isLoading = true
        
        // Generate sample data for demonstration
        samplingSites = [
            SamplingSite(
                id: "1",
                name: "Site Alpha",
                coordinate: CLLocationCoordinate2D(latitude: 12.0, longitude: 77.0),
                depth: 1200,
                temperature: 4.2,
                salinity: 34.8,
                speciesCount: 45,
                lastSampled: Date().addingTimeInterval(-86400 * 7)
            ),
            SamplingSite(
                id: "2",
                name: "Site Beta",
                coordinate: CLLocationCoordinate2D(latitude: 11.5, longitude: 77.5),
                depth: 1500,
                temperature: 3.8,
                salinity: 35.1,
                speciesCount: 38,
                lastSampled: Date().addingTimeInterval(-86400 * 14)
            ),
            SamplingSite(
                id: "3",
                name: "Site Gamma",
                coordinate: CLLocationCoordinate2D(latitude: 12.5, longitude: 76.5),
                depth: 800,
                temperature: 5.1,
                salinity: 34.5,
                speciesCount: 52,
                lastSampled: Date().addingTimeInterval(-86400 * 3)
            ),
            SamplingSite(
                id: "4",
                name: "Site Delta",
                coordinate: CLLocationCoordinate2D(latitude: 11.0, longitude: 78.0),
                depth: 2000,
                temperature: 2.9,
                salinity: 35.3,
                speciesCount: 29,
                lastSampled: Date().addingTimeInterval(-86400 * 21)
            )
        ]
        
        isLoading = false
    }
}

struct SamplingSite: Identifiable {
    let id: String
    let name: String
    let coordinate: CLLocationCoordinate2D
    let depth: Double
    let temperature: Double
    let salinity: Double
    let speciesCount: Int
    let lastSampled: Date
}

struct SamplingSiteAnnotation: View {
    let site: SamplingSite
    let isSelected: Bool
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            VStack(spacing: 0) {
                Image(systemName: "mappin.circle.fill")
                    .font(.title)
                    .foregroundColor(isSelected ? Theme.accent : Theme.primary)
                    .background(
                        Circle()
                            .fill(.white)
                            .frame(width: 20, height: 20)
                    )
                
                if isSelected {
                    Text(site.name)
                        .font(Theme.caption)
                        .fontWeight(.medium)
                        .foregroundColor(.white)
                        .padding(.horizontal, Theme.spacingS)
                        .padding(.vertical, Theme.spacingXS)
                        .background(Theme.accent)
                        .cornerRadius(Theme.radiusS)
                        .offset(y: -5)
                }
            }
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct SamplingSiteDetailView: View {
    let site: SamplingSite
    let onClose: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.spacingM) {
            HStack {
                Text(site.name)
                    .font(Theme.title3)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Spacer()
                
                Button(action: onClose) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(Theme.textSecondaryLight)
                }
            }
            
            VStack(alignment: .leading, spacing: Theme.spacingS) {
                DetailRow(icon: "location.fill", title: "Location", value: String(format: "%.3f, %.3f", site.coordinate.latitude, site.coordinate.longitude))
                
                DetailRow(icon: "arrow.down", title: "Depth", value: "\(Int(site.depth)) m")
                
                DetailRow(icon: "thermometer", title: "Temperature", value: String(format: "%.1f°C", site.temperature))
                
                DetailRow(icon: "drop.fill", title: "Salinity", value: String(format: "%.1f PSU", site.salinity))
                
                DetailRow(icon: "leaf.fill", title: "Species Count", value: "\(site.speciesCount)")
                
                DetailRow(icon: "calendar", title: "Last Sampled", value: site.lastSampled, style: .date)
            }
            
            Button("View Details") {
                // Navigate to detailed site view
            }
            .primaryButtonStyle()
        }
        .padding(Theme.spacingL)
    }
}

struct DetailRow: View {
    let icon: String
    let title: String
    let value: Any
    let style: Text.DateStyle?
    
    init(icon: String, title: String, value: String) {
        self.icon = icon
        self.title = title
        self.value = value
        self.style = nil
    }
    
    init(icon: String, title: String, value: Date, style: Text.DateStyle) {
        self.icon = icon
        self.title = title
        self.value = value
        self.style = style
    }
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundColor(Theme.accent)
                .frame(width: 20)
            
            Text(title)
                .font(Theme.callout)
                .foregroundColor(Theme.textSecondaryLight)
            
            Spacer()
            
            if let date = value as? Date, let style = style {
                Text(date, style: style)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
            } else {
                Text("\(value)")
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
            }
        }
    }
}

struct MapStatsView: View {
    let sites: [SamplingSite]
    
    var body: some View {
        VStack(alignment: .leading, spacing: Theme.spacingM) {
            Text("Sampling Overview")
                .font(Theme.title3)
                .foregroundColor(Theme.textPrimaryLight)
            
            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: Theme.spacingM) {
                MapStatCard(
                    title: "Total Sites",
                    value: "\(sites.count)",
                    icon: "mappin.circle.fill",
                    color: Theme.primary
                )
                
                MapStatCard(
                    title: "Avg Depth",
                    value: "\(Int(sites.map(\.depth).reduce(0, +) / Double(sites.count)))m",
                    icon: "arrow.down",
                    color: Theme.accent
                )
                
                MapStatCard(
                    title: "Total Species",
                    value: "\(sites.map(\.speciesCount).reduce(0, +))",
                    icon: "leaf.fill",
                    color: Theme.success
                )
                
                MapStatCard(
                    title: "Avg Temp",
                    value: String(format: "%.1f°C", sites.map(\.temperature).reduce(0, +) / Double(sites.count)),
                    icon: "thermometer",
                    color: Theme.warning
                )
            }
        }
        .padding(Theme.spacingL)
    }
}

struct MapStatCard: View {
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
        }
        .frame(maxWidth: .infinity)
        .padding(Theme.spacingM)
        .cardStyle()
    }
}

enum MapOverlay: String, CaseIterable {
    case speciesDistribution = "species_distribution"
    case hotspots = "hotspots"
    case temperature = "temperature"
    case depth = "depth"
    
    var displayName: String {
        switch self {
        case .speciesDistribution: return "Species Distribution"
        case .hotspots: return "Biodiversity Hotspots"
        case .temperature: return "Temperature"
        case .depth: return "Depth"
        }
    }
}

struct MapFiltersView: View {
    @Binding var selectedOverlay: MapOverlay
    @Binding var isPresented: Bool
    
    var body: some View {
        NavigationView {
            VStack(alignment: .leading, spacing: Theme.spacingL) {
                Text("Map Overlays")
                    .font(Theme.title2)
                    .foregroundColor(Theme.textPrimaryLight)
                
                ForEach(MapOverlay.allCases, id: \.self) { overlay in
                    Button(action: {
                        selectedOverlay = overlay
                        isPresented = false
                    }) {
                        HStack {
                            Text(overlay.displayName)
                                .font(Theme.callout)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Spacer()
                            
                            if selectedOverlay == overlay {
                                Image(systemName: "checkmark")
                                    .foregroundColor(Theme.primary)
                            }
                        }
                        .padding(Theme.spacingM)
                        .background(Theme.surfaceLight)
                        .cornerRadius(Theme.radiusM)
                    }
                    .buttonStyle(PlainButtonStyle())
                }
                
                Spacer()
            }
            .padding(Theme.spacingL)
            .background(Theme.backgroundLight)
            .navigationTitle("Map Filters")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        isPresented = false
                    }
                }
            }
        }
    }
}

extension View {
    func cornerRadius(_ radius: CGFloat, corners: UIRectCorner) -> some View {
        clipShape(RoundedCorner(radius: radius, corners: corners))
    }
}

struct RoundedCorner: Shape {
    var radius: CGFloat = .infinity
    var corners: UIRectCorner = .allCorners

    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: radius, height: radius)
        )
        return Path(path.cgPath)
    }
}

#Preview {
    MapView()
}
