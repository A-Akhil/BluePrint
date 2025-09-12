//
//  Theme.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

struct Theme {
    // MARK: - Brand Colors
    static let primary = Color(hex: "#3B82F6")
    static let primaryLight = Color(hex: "#60A5FA")
    static let primaryDark = Color(hex: "#2563EB")
    static let secondary = Color(hex: "#8B5CF6")
    static let accent = Color(hex: "#06B6D4")
    
    // MARK: - Status Colors
    static let success = Color(hex: "#10B981")
    static let warning = Color(hex: "#F59E0B")
    static let danger = Color(hex: "#EF4444")
    static let info = Color(hex: "#0EA5E9")
    
    // MARK: - Neutral Colors
    static let backgroundLight = Color(hex: "#F8FAFC")
    static let backgroundDark = Color(hex: "#0F172A")
    static let surfaceLight = Color(hex: "#FFFFFF")
    static let surfaceDark = Color(hex: "#1E293B")
    static let textPrimaryLight = Color(hex: "#0F172A")
    static let textSecondaryLight = Color(hex: "#475569")
    static let textPrimaryDark = Color(hex: "#F1F5F9")
    static let textSecondaryDark = Color(hex: "#94A3B8")
    
    // MARK: - Typography
    static let largeTitle = Font.largeTitle.weight(.bold)
    static let title = Font.title.weight(.semibold)
    static let title2 = Font.title2.weight(.semibold)
    static let title3 = Font.title3.weight(.medium)
    static let headline = Font.headline.weight(.medium)
    static let body = Font.body
    static let callout = Font.callout
    static let subheadline = Font.subheadline
    static let footnote = Font.footnote
    static let caption = Font.caption
    
    // MARK: - Spacing
    static let spacingXS: CGFloat = 4
    static let spacingS: CGFloat = 8
    static let spacingM: CGFloat = 16
    static let spacingL: CGFloat = 24
    static let spacingXL: CGFloat = 32
    static let spacingXXL: CGFloat = 48
    
    // MARK: - Corner Radius
    static let radiusS: CGFloat = 4
    static let radiusM: CGFloat = 8
    static let radiusL: CGFloat = 12
    static let radiusXL: CGFloat = 16
    
    // MARK: - Shadows
    static let shadowSmall = Shadow(color: .black.opacity(0.1), radius: 2, x: 0, y: 1)
    static let shadowMedium = Shadow(color: .black.opacity(0.15), radius: 4, x: 0, y: 2)
    static let shadowLarge = Shadow(color: .black.opacity(0.2), radius: 8, x: 0, y: 4)
}

struct Shadow {
    let color: Color
    let radius: CGFloat
    let x: CGFloat
    let y: CGFloat
}

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }
        
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

// MARK: - View Modifiers
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .background(Theme.surfaceLight)
            .cornerRadius(Theme.radiusL)
            .shadow(color: Theme.shadowSmall.color, radius: Theme.shadowSmall.radius, x: Theme.shadowSmall.x, y: Theme.shadowSmall.y)
    }
}

struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .foregroundColor(.white)
            .padding(.horizontal, Theme.spacingL)
            .padding(.vertical, Theme.spacingM)
            .background(Theme.primary)
            .cornerRadius(Theme.radiusM)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}

struct SecondaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .foregroundColor(Theme.primary)
            .padding(.horizontal, Theme.spacingL)
            .padding(.vertical, Theme.spacingM)
            .background(Theme.primary.opacity(0.1))
            .cornerRadius(Theme.radiusM)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardStyle())
    }
    
    func primaryButtonStyle() -> some View {
        buttonStyle(PrimaryButtonStyle())
    }
    
    func secondaryButtonStyle() -> some View {
        buttonStyle(SecondaryButtonStyle())
    }
}
