//
//  ContentView.swift
//  Research Hub
//
//  Created by admin61 on 12/09/25.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "dna.helix")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Research Hub")
                .font(.title)
                .fontWeight(.bold)
            Text("Deep-Sea eDNA AI Pipeline")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
