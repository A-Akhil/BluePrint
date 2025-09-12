const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// Mock data
const mockUsers = [
    {
        id: 1,
        email: "researcher@edna-pipeline.cmlre.gov.in",
        name: "Research User",
        role: "researcher",
        isActive: true,
        createdAt: new Date().toISOString()
    },
    {
        id: 2,
        email: "admin@edna-pipeline.cmlre.gov.in", 
        name: "Admin User",
        role: "admin",
        isActive: true,
        createdAt: new Date().toISOString()
    }
];

const mockSequences = [
    {
        id: 1,
        sequence: "ATCGATCGATCG",
        species: "Deep-sea fish",
        confidence: 0.95,
        uploadDate: new Date().toISOString(),
        metadata: {
            location: { latitude: 12.3456, longitude: 78.9012, depth: 1500 },
            environmentalData: { temperature: 4.2, salinity: 35.1, pH: 8.1 }
        }
    }
];

// Authentication endpoints
app.post('/api/v1/auth/login', (req, res) => {
    const { email, password } = req.body;
    const user = mockUsers.find(u => u.email === email);
    
    if (user && password === "ResearchHub2024!" || password === "AdminHub2024!") {
        res.json({
            success: true,
            token: "mock-jwt-token-" + user.id,
            user: user
        });
    } else {
        res.status(401).json({
            success: false,
            error: "Invalid credentials"
        });
    }
});

app.post('/api/v1/auth/signup', (req, res) => {
    const { email, password, name, role } = req.body;
    const newUser = {
        id: mockUsers.length + 1,
        email,
        name,
        role: role || "researcher",
        isActive: true,
        createdAt: new Date().toISOString()
    };
    mockUsers.push(newUser);
    
    res.json({
        success: true,
        token: "mock-jwt-token-" + newUser.id,
        user: newUser
    });
});

// Sequence endpoints
app.get('/api/v1/sequences', (req, res) => {
    res.json(mockSequences);
});

app.post('/api/v1/sequences/upload', (req, res) => {
    const { file, filename, metadata } = req.body;
    const newSequence = {
        id: mockSequences.length + 1,
        sequence: "UPLOADED_SEQUENCE_DATA",
        species: metadata?.species || "Unknown",
        confidence: 0.85,
        uploadDate: new Date().toISOString(),
        metadata: metadata || {}
    };
    mockSequences.push(newSequence);
    
    res.json({
        success: true,
        message: "Sequence uploaded successfully",
        sequenceId: newSequence.id
    });
});

// Search endpoints
app.post('/api/v1/search/hierarchical', (req, res) => {
    res.json({
        success: true,
        searchId: "mock-search-" + Date.now(),
        results: mockSequences
    });
});

// Visualization endpoints
app.get('/api/v1/visualization/taxonomy', (req, res) => {
    res.json({
        success: true,
        data: {
            nodes: [
                { id: "root", name: "Root", level: 0 },
                { id: "fish", name: "Fish", level: 1, parent: "root" },
                { id: "deep-sea", name: "Deep-sea Fish", level: 2, parent: "fish" }
            ],
            links: [
                { source: "root", target: "fish" },
                { source: "fish", target: "deep-sea" }
            ]
        }
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`Mock API server running on http://localhost:${PORT}`);
    console.log('Available endpoints:');
    console.log('- POST /api/v1/auth/login');
    console.log('- POST /api/v1/auth/signup');
    console.log('- GET /api/v1/sequences');
    console.log('- POST /api/v1/sequences/upload');
    console.log('- POST /api/v1/search/hierarchical');
    console.log('- GET /api/v1/visualization/taxonomy');
    console.log('- GET /health');
});
