//
//  AuthView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI
import Combine

struct AuthView: View {
    @StateObject private var apiService = APIService.shared
    @State private var isLoginMode = true
    @State private var email = ""
    @State private var password = ""
    @State private var name = ""
    @State private var selectedRole: UserRole = .researcher
    @State private var isLoading = false
    @State private var errorMessage = ""
    @State private var showAlert = false
    @State private var cancellables = Set<AnyCancellable>()
    
    var body: some View {
        NavigationView {
            VStack(spacing: Theme.spacingXL) {
                // Header
                VStack(spacing: Theme.spacingM) {
                    Image(systemName: "dna.helix")
                        .font(.system(size: 60))
                        .foregroundColor(Theme.primary)
                    
                    Text("Research Hub")
                        .font(Theme.largeTitle)
                        .foregroundColor(Theme.textPrimaryLight)
                    
                    Text("Deep-Sea eDNA AI Pipeline")
                        .font(Theme.title3)
                        .foregroundColor(Theme.textSecondaryLight)
                }
                .padding(.top, Theme.spacingXXL)
                
                // Form
                VStack(spacing: Theme.spacingL) {
                    if !isLoginMode {
                        // Name field for signup
                        VStack(alignment: .leading, spacing: Theme.spacingS) {
                            Text("Full Name")
                                .font(Theme.callout)
                                .foregroundColor(Theme.textPrimaryLight)
                            
                            TextField("Enter your full name", text: $name)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .autocapitalization(.words)
                        }
                        
                        // Role selection for signup
                        VStack(alignment: .leading, spacing: Theme.spacingS) {
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
                    }
                    
                    // Email field
                    VStack(alignment: .leading, spacing: Theme.spacingS) {
                        Text("Email")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        TextField("Enter your email", text: $email)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                            .keyboardType(.emailAddress)
                            .autocapitalization(.none)
                    }
                    
                    // Password field
                    VStack(alignment: .leading, spacing: Theme.spacingS) {
                        Text("Password")
                            .font(Theme.callout)
                            .foregroundColor(Theme.textPrimaryLight)
                        
                        SecureField("Enter your password", text: $password)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                    }
                }
                .padding(.horizontal, Theme.spacingL)
                
                // Action buttons
                VStack(spacing: Theme.spacingM) {
                    Button(action: handleAuth) {
                        HStack {
                            if isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                    .scaleEffect(0.8)
                            }
                            Text(isLoginMode ? "Sign In" : "Sign Up")
                        }
                        .frame(maxWidth: .infinity)
                    }
                    .primaryButtonStyle()
                    .disabled(isLoading || !isFormValid)
                    
                    Button(action: { isLoginMode.toggle() }) {
                        Text(isLoginMode ? "Don't have an account? Sign Up" : "Already have an account? Sign In")
                            .font(Theme.callout)
                            .foregroundColor(Theme.primary)
                    }
                }
                .padding(.horizontal, Theme.spacingL)
                
                Spacer()
            }
            .background(Theme.backgroundLight)
            .navigationBarHidden(true)
        }
        .alert("Error", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text(errorMessage)
        }
    }
    
    private var isFormValid: Bool {
        if isLoginMode {
            return !email.isEmpty && !password.isEmpty
        } else {
            return !email.isEmpty && !password.isEmpty && !name.isEmpty
        }
    }
    
    private func handleAuth() {
        isLoading = true
        errorMessage = ""
        
        let authPublisher: AnyPublisher<LoginResponse, APIError>
        
        if isLoginMode {
            authPublisher = apiService.login(email: email, password: password)
        } else {
            authPublisher = apiService.signup(email: email, password: password, name: name, role: selectedRole)
        }
        
        authPublisher
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    isLoading = false
                    if case .failure(let error) = completion {
                        errorMessage = error.message
                        showAlert = true
                    }
                },
                receiveValue: { response in
                    apiService.storeCredentials(token: response.token, user: response.user)
                }
            )
            .store(in: &cancellables)
    }
}

#Preview {
    AuthView()
}
