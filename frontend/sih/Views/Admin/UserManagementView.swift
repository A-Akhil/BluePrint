//
//  UserManagementView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

struct UserManagementView: View {
    @State private var users: [User] = []
    @State private var isLoading = false
    @State private var searchText = ""
    @State private var selectedRole: UserRole? = nil
    @State private var showAddUser = false
    @State private var showAlert = false
    @State private var alertMessage = ""
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Search and Filter Bar
                VStack(spacing: Theme.spacingM) {
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundColor(Theme.textSecondaryLight)
                        
                        TextField("Search users...", text: $searchText)
                            .textFieldStyle(PlainTextFieldStyle())
                    }
                    .padding(Theme.spacingM)
                    .background(Theme.surfaceLight)
                    .cornerRadius(Theme.radiusM)
                    
                    HStack {
                        Picker("Role", selection: $selectedRole) {
                            Text("All Roles").tag(nil as UserRole?)
                            ForEach(UserRole.allCases, id: \.self) { role in
                                Text(role.displayName).tag(role as UserRole?)
                            }
                        }
                        .pickerStyle(MenuPickerStyle())
                        
                        Spacer()
                        
                        Button(action: { showAddUser = true }) {
                            HStack {
                                Image(systemName: "plus")
                                Text("Add User")
                            }
                            .font(Theme.callout)
                            .foregroundColor(.white)
                            .padding(.horizontal, Theme.spacingM)
                            .padding(.vertical, Theme.spacingS)
                            .background(Theme.primary)
                            .cornerRadius(Theme.radiusM)
                        }
                    }
                }
                .padding(Theme.spacingL)
                .background(Theme.backgroundLight)
                
                // Users List
                if isLoading {
                    ProgressView("Loading users...")
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    ScrollView {
                        LazyVStack(spacing: Theme.spacingS) {
                            ForEach(filteredUsers) { user in
                                UserRow(user: user) {
                                    // Handle user action
                                }
                            }
                        }
                        .padding(.horizontal, Theme.spacingL)
                    }
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("User Management")
            .navigationBarTitleDisplayMode(.large)
        }
        .sheet(isPresented: $showAddUser) {
            AddUserView(isPresented: $showAddUser)
        }
        .alert("Error", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text(alertMessage)
        }
        .onAppear {
            loadUsers()
        }
    }
    
    private var filteredUsers: [User] {
        var filtered = users
        
        if !searchText.isEmpty {
            filtered = filtered.filter { user in
                user.name.localizedCaseInsensitiveContains(searchText) ||
                user.email.localizedCaseInsensitiveContains(searchText)
            }
        }
        
        if let role = selectedRole {
            filtered = filtered.filter { $0.role == role }
        }
        
        return filtered
    }
    
    private func loadUsers() {
        isLoading = true
        
        // Generate sample users
        users = [
            User(
                id: "1",
                email: "dr.smith@research.org",
                name: "Dr. Sarah Smith",
                role: .researcher,
                createdAt: Date().addingTimeInterval(-86400 * 30),
                isActive: true
            ),
            User(
                id: "2",
                email: "dr.johnson@research.org",
                name: "Dr. Michael Johnson",
                role: .researcher,
                createdAt: Date().addingTimeInterval(-86400 * 15),
                isActive: true
            ),
            User(
                id: "3",
                email: "admin@research.org",
                name: "Admin User",
                role: .admin,
                createdAt: Date().addingTimeInterval(-86400 * 60),
                isActive: true
            ),
            User(
                id: "4",
                email: "inactive@research.org",
                name: "Inactive User",
                role: .researcher,
                createdAt: Date().addingTimeInterval(-86400 * 90),
                isActive: false
            )
        ]
        
        isLoading = false
    }
}

struct UserRow: View {
    let user: User
    let onAction: () -> Void
    @State private var showUserDetails = false
    
    var body: some View {
        HStack(spacing: Theme.spacingM) {
            // Avatar
            Circle()
                .fill(user.role == .admin ? Theme.secondary : Theme.primary)
                .frame(width: 40, height: 40)
                .overlay(
                    Text(user.name.prefix(1).uppercased())
                        .font(.headline)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                )
            
            VStack(alignment: .leading, spacing: Theme.spacingXS) {
                Text(user.name)
                    .font(Theme.callout)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Text(user.email)
                    .font(Theme.caption)
                    .foregroundColor(Theme.textSecondaryLight)
                
                HStack {
                    Text(user.role.displayName)
                        .font(Theme.caption)
                        .fontWeight(.medium)
                        .padding(.horizontal, Theme.spacingS)
                        .padding(.vertical, Theme.spacingXS)
                        .background(user.role == .admin ? Theme.secondary.opacity(0.2) : Theme.primary.opacity(0.2))
                        .foregroundColor(user.role == .admin ? Theme.secondary : Theme.primary)
                        .cornerRadius(Theme.radiusS)
                    
                    if !user.isActive {
                        Text("Inactive")
                            .font(Theme.caption)
                            .fontWeight(.medium)
                            .padding(.horizontal, Theme.spacingS)
                            .padding(.vertical, Theme.spacingXS)
                            .background(Theme.danger.opacity(0.2))
                            .foregroundColor(Theme.danger)
                            .cornerRadius(Theme.radiusS)
                    }
                }
            }
            
            Spacer()
            
            Menu {
                Button("View Details") {
                    showUserDetails = true
                }
                
                Button("Edit User") {
                    // Edit user
                }
                
                if user.isActive {
                    Button("Suspend User", role: .destructive) {
                        // Suspend user
                    }
                } else {
                    Button("Activate User") {
                        // Activate user
                    }
                }
                
                Button("Delete User", role: .destructive) {
                    // Delete user
                }
            } label: {
                Image(systemName: "ellipsis.circle")
                    .foregroundColor(Theme.textSecondaryLight)
            }
        }
        .padding(Theme.spacingM)
        .cardStyle()
        .sheet(isPresented: $showUserDetails) {
            UserDetailView(user: user, isPresented: $showUserDetails)
        }
    }
}

struct AddUserView: View {
    @Binding var isPresented: Bool
    @State private var name = ""
    @State private var email = ""
    @State private var password = ""
    @State private var selectedRole: UserRole = .researcher
    @State private var isLoading = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.spacingL) {
                VStack(alignment: .leading, spacing: Theme.spacingM) {
                    Text("Full Name")
                        .font(Theme.callout)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    TextField("Enter full name", text: $name)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                
                VStack(alignment: .leading, spacing: Theme.spacingM) {
                    Text("Email")
                        .font(Theme.callout)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    TextField("Enter email", text: $email)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                }
                
                VStack(alignment: .leading, spacing: Theme.spacingM) {
                    Text("Password")
                        .font(Theme.callout)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    SecureField("Enter password", text: $password)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                }
                
                VStack(alignment: .leading, spacing: Theme.spacingM) {
                    Text("Role")
                        .font(Theme.callout)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    Picker("Role", selection: $selectedRole) {
                        ForEach(UserRole.allCases, id: \.self) { role in
                            Text(role.displayName).tag(role)
                        }
                    }
                    .pickerStyle(SegmentedPickerStyle())
                }
                
                Spacer()
            }
            .padding(Theme.spacingL)
            .background(Theme.backgroundLight)
            .navigationTitle("Add User")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        isPresented = false
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        addUser()
                    }
                    .disabled(isLoading || name.isEmpty || email.isEmpty || password.isEmpty)
                }
            }
        }
    }
    
    private func addUser() {
        isLoading = true
        // Implement user creation
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            isLoading = false
            isPresented = false
        }
    }
}

struct UserDetailView: View {
    let user: User
    @Binding var isPresented: Bool
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: Theme.spacingL) {
                    // User Info
                    VStack(spacing: Theme.spacingM) {
                        Circle()
                            .fill(user.role == .admin ? Theme.secondary : Theme.primary)
                            .frame(width: 80, height: 80)
                            .overlay(
                                Text(user.name.prefix(1).uppercased())
                                    .font(.largeTitle)
                                    .fontWeight(.bold)
                                    .foregroundColor(.white)
                            )
                        
                        VStack(spacing: Theme.spacingS) {
                            Text(user.name)
                                .font(Theme.title2)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            Text(user.email)
                                .font(Theme.callout)
                                .foregroundColor(Theme.textSecondaryLight)
                            
                            Text(user.role.displayName)
                                .font(Theme.callout)
                                .fontWeight(.medium)
                                .padding(.horizontal, Theme.spacingM)
                                .padding(.vertical, Theme.spacingS)
                                .background(user.role == .admin ? Theme.secondary.opacity(0.2) : Theme.primary.opacity(0.2))
                                .foregroundColor(user.role == .admin ? Theme.secondary : Theme.primary)
                                .cornerRadius(Theme.radiusM)
                        }
                    }
                    .padding(Theme.spacingL)
                    .cardStyle()
                    
                    // User Stats
                    LazyVGrid(columns: [
                        GridItem(.flexible()),
                        GridItem(.flexible())
                    ], spacing: Theme.spacingM) {
                        UserStatCard(title: "Joined", value: user.createdAt, style: .date, icon: "calendar", color: Theme.accent)
                        UserStatCard(title: "Status", value: user.isActive ? "Active" : "Inactive", icon: "person.fill", color: user.isActive ? Theme.success : Theme.danger)
                    }
                    .padding(.horizontal, Theme.spacingL)
                    
                    Spacer()
                }
            }
            .background(Theme.backgroundLight)
            .navigationTitle("User Details")
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

struct UserStatCard: View {
    let title: String
    let value: Any
    let style: Text.DateStyle?
    let icon: String
    let color: Color
    
    init(title: String, value: String, icon: String, color: Color) {
        self.title = title
        self.value = value
        self.style = nil
        self.icon = icon
        self.color = color
    }
    
    init(title: String, value: Date, style: Text.DateStyle, icon: String, color: Color) {
        self.title = title
        self.value = value
        self.style = style
        self.icon = icon
        self.color = color
    }
    
    var body: some View {
        VStack(spacing: Theme.spacingS) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            
            if let date = value as? Date, let style = style {
                Text(date, style: style)
                    .font(Theme.title3)
                    .fontWeight(.bold)
                    .foregroundColor(Theme.textPrimaryLight)
            } else {
                Text("\(value)")
                    .font(Theme.title3)
                    .fontWeight(.bold)
                    .foregroundColor(Theme.textPrimaryLight)
            }
            
            Text(title)
                .font(Theme.caption)
                .foregroundColor(Theme.textSecondaryLight)
        }
        .frame(maxWidth: .infinity)
        .padding(Theme.spacingM)
        .cardStyle()
    }
}

#Preview {
    UserManagementView()
}
