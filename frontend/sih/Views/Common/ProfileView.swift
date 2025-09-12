//
//  ProfileView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

struct ProfileView: View {
    @EnvironmentObject var authManager: AuthManager
    @State private var showEditProfile = false
    @State private var showSettings = false
    @State private var savedSearches: [SavedSearch] = []
    @State private var savedReports: [SavedReport] = []
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.spacingL) {
                    // Profile Header
                    VStack(spacing: Theme.spacingM) {
                        // Avatar
                        Circle()
                            .fill(Theme.primary.gradient)
                            .frame(width: 100, height: 100)
                            .overlay(
                                Text(authManager.currentUser?.name.prefix(1).uppercased() ?? "U")
                                    .font(.largeTitle)
                                    .fontWeight(.bold)
                                    .foregroundColor(.white)
                            )
                        
                        VStack(spacing: Theme.spacingS) {
                            Text(authManager.currentUser?.name ?? "User")
                                .font(Theme.title2)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Text(authManager.currentUser?.email ?? "")
                                .font(Theme.callout)
                                .foregroundColor(Theme.textSecondaryLight)
                            
                            Text(authManager.currentUser?.role.displayName ?? "")
                                .font(Theme.caption)
                                .fontWeight(.medium)
                                .padding(.horizontal, Theme.spacingM)
                                .padding(.vertical, Theme.spacingS)
                                .background(Theme.primary.opacity(0.1))
                                .foregroundColor(Theme.primary)
                                .cornerRadius(Theme.radiusM)
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Quick Actions
                    VStack(alignment: .leading, spacing: Theme.spacingM) {
                        Text("Quick Actions")
                            .font(Theme.title3)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        VStack(spacing: Theme.spacingS) {
                            ProfileActionRow(
                                icon: "person.circle",
                                title: "Edit Profile",
                                color: Theme.primary
                            ) {
                                showEditProfile = true
                            }
                            
                            ProfileActionRow(
                                icon: "gearshape.fill",
                                title: "Settings",
                                color: Theme.accent
                            ) {
                                showSettings = true
                            }
                            
                            ProfileActionRow(
                                icon: "doc.text.fill",
                                title: "Saved Reports",
                                color: Theme.success
                            ) {
                                // Navigate to saved reports
                            }
                            
                            ProfileActionRow(
                                icon: "magnifyingglass",
                                title: "Saved Searches",
                                color: Theme.secondary
                            ) {
                                // Navigate to saved searches
                            }
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
                                ProfileActivityRow(activity: activity)
                            }
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // Logout Button
                    Button(action: {
                        authManager.logout()
                    }) {
                        HStack {
                            Image(systemName: "rectangle.portrait.and.arrow.right")
                            Text("Sign Out")
                        }
                        .frame(maxWidth: .infinity)
                    }
                    .foregroundColor(.white)
                    .padding(Theme.spacingM)
                    .background(Theme.danger)
                    .cornerRadius(Theme.radiusM)
                    .padding(.horizontal, Theme.spacingL)
                    
                    Spacer(minLength: Theme.spacingXL)
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("Profile")
            .navigationBarTitleDisplayMode(.large)
        }
        .sheet(isPresented: $showEditProfile) {
            EditProfileView(isPresented: $showEditProfile)
        }
        .sheet(isPresented: $showSettings) {
            SettingsView(isPresented: $showSettings)
        }
        .onAppear {
            loadUserData()
        }
    }
    
    private func loadUserData() {
        // Load saved searches and reports
        savedSearches = []
        savedReports = []
    }
    
    private var recentActivities: [Activity] {
        [
            Activity(id: "1", title: "Uploaded sequence data", timestamp: Date().addingTimeInterval(-3600)),
            Activity(id: "2", title: "Generated biodiversity report", timestamp: Date().addingTimeInterval(-7200)),
            Activity(id: "3", title: "Searched for novel taxa", timestamp: Date().addingTimeInterval(-86400)),
            Activity(id: "4", title: "Viewed phylogenetic tree", timestamp: Date().addingTimeInterval(-172800))
        ]
    }
}

struct ProfileActionRow: View {
    let icon: String
    let title: String
    let color: Color
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack(spacing: Theme.spacingM) {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundColor(color)
                    .frame(width: 24)
                
                Text(title)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(Theme.textSecondaryLight)
            }
            .padding(Theme.spacingM)
            .background(Theme.surfaceLight)
            .cornerRadius(Theme.radiusM)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct Activity: Identifiable {
    let id: String
    let title: String
    let timestamp: Date
}

struct ProfileActivityRow: View {
    let activity: Activity
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: "clock.fill")
                .foregroundColor(Theme.accent)
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

struct SavedSearch: Identifiable {
    let id: String
    let name: String
    let query: String
    let createdAt: Date
}

struct SavedReport: Identifiable {
    let id: String
    let name: String
    let analysisId: String
    let createdAt: Date
}

struct EditProfileView: View {
    @Binding var isPresented: Bool
    @EnvironmentObject var authManager: AuthManager
    @State private var name = ""
    @State private var email = ""
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.spacingL) {
                VStack(alignment: .leading, spacing: Theme.spacingM) {
                    Text("Full Name")
                        .font(Theme.callout)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    TextField("Enter your name", text: $name)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                
                VStack(alignment: .leading, spacing: Theme.spacingM) {
                    Text("Email")
                        .font(Theme.callout)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    TextField("Enter your email", text: $email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                }
                
                Spacer()
            }
            .padding(Theme.spacingL)
            .background(Theme.backgroundLight)
            .navigationTitle("Edit Profile")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        isPresented = false
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        saveProfile()
                    }
                    .disabled(isLoading)
                }
            }
        }
        .onAppear {
            name = authManager.currentUser?.name ?? ""
            email = authManager.currentUser?.email ?? ""
        }
    }
    
    private func saveProfile() {
        isLoading = true
        // Implement profile update
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            isLoading = false
            isPresented = false
        }
    }
}

struct SettingsView: View {
    @Binding var isPresented: Bool
    @State private var notificationsEnabled = true
    @State private var darkModeEnabled = false
    @State private var autoSyncEnabled = true
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.spacingL) {
                VStack(alignment: .leading, spacing: Theme.spacingM) {
                    Text("Preferences")
                        .font(Theme.title3)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    VStack(spacing: Theme.spacingS) {
                        SettingsRow(
                            icon: "bell.fill",
                            title: "Notifications",
                            color: Theme.accent
                        ) {
                            AnyView(Toggle("", isOn: $notificationsEnabled))
                        }
                        
                        SettingsRow(
                            icon: "moon.fill",
                            title: "Dark Mode",
                            color: Theme.secondary
                        ) {
                            AnyView(Toggle("", isOn: $darkModeEnabled))
                        }
                        
                        SettingsRow(
                            icon: "arrow.clockwise",
                            title: "Auto Sync",
                            color: Theme.success
                        ) {
                            AnyView(Toggle("", isOn: $autoSyncEnabled))
                        }
                    }
                }
                .padding(Theme.spacingL)
                .cardStyle()
                
                Spacer()
            }
            .padding(Theme.spacingL)
            .background(Theme.backgroundLight)
            .navigationTitle("Settings")
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

struct SettingsRow: View {
    let icon: String
    let title: String
    let color: Color
    let content: () -> AnyView
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(color)
                .frame(width: 24)
            
            Text(title)
                .font(Theme.callout)
                .foregroundColor(Theme.textPrimaryLight)
            
            Spacer()
            
            content()
        }
        .padding(Theme.spacingM)
        .background(Theme.surfaceLight)
        .cornerRadius(Theme.radiusM)
    }
}

#Preview {
    ProfileView()
        .environmentObject(AuthManager())
}
