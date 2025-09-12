//
//  SplashView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

struct SplashView: View {
    @State private var isAnimating = false
    
    var body: some View {
        VStack(spacing: Theme.spacingXL) {
            Image(systemName: "dna.helix")
                .font(.system(size: 80))
                .foregroundColor(Theme.primary)
                .scaleEffect(isAnimating ? 1.2 : 1.0)
                .animation(.easeInOut(duration: 1.5).repeatForever(autoreverses: true), value: isAnimating)
            
            VStack(spacing: Theme.spacingM) {
                Text("Research Hub")
                    .font(Theme.largeTitle)
                    .foregroundColor(Theme.textPrimaryLight)
                
                Text("Deep-Sea eDNA AI Pipeline")
                    .font(Theme.title3)
                    .foregroundColor(Theme.textSecondaryLight)
            }
            
            ProgressView()
                .progressViewStyle(CircularProgressViewStyle(tint: Theme.primary))
                .scaleEffect(1.2)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Theme.backgroundLight)
        .onAppear {
            isAnimating = true
        }
    }
}

#Preview {
    SplashView()
}
