# Research Hub - Deep-Sea eDNA AI Pipeline

A comprehensive SwiftUI iOS application for managing and analyzing deep-sea environmental DNA (eDNA) data through an AI-powered pipeline.

## 🎯 Overview

Research Hub is a sophisticated mobile application designed for marine researchers and administrators to upload, analyze, and visualize eDNA sequence data. The app provides role-based access with distinct interfaces for researchers and administrators.

## ✨ Features

### 🔐 Authentication & Authorization
- **Secure Login/Signup** with email and password
- **Role-based Access Control**:
  - **Researcher**: Access to data upload, search, visualization, and reporting
  - **Admin**: Full system management, user administration, and dataset moderation
- **Persistent Authentication** with secure token storage

### 👨‍🔬 Researcher Features

#### 📊 Dashboard
- **Real-time Statistics**: Total sequences, active analyses, species found, novel taxa
- **Recent Activity Feed**: Latest uploads and analysis results
- **Quick Actions**: Direct access to key features
- **Progress Tracking**: Visual indicators for ongoing processes

#### 📤 Data Upload
- **Multi-format Support**: CSV, JSON, and FASTA files
- **Rich Metadata Collection**:
  - Sampling date and location coordinates
  - Environmental parameters (temperature, salinity, depth)
  - Custom notes and observations
- **Progress Tracking**: Real-time upload progress with notifications
- **File Validation**: Automatic format and size validation

#### 🔍 Advanced Search & Filtering
- **Comprehensive Search**: Species, taxa, and keyword-based queries
- **Advanced Filters**:
  - Date range selection
  - Geographic location filtering
  - Rarity and novelty classification
  - Confidence score ranges
- **Export Capabilities**: CSV, JSON, and PDF export formats
- **Saved Searches**: Store frequently used search criteria

#### 📈 Data Visualization
- **Taxonomic Tree**: Interactive hierarchical species classification
- **Phylogenetic Networks**: Evolutionary relationship visualization
- **Biodiversity Charts**: Species richness and diversity indices
- **Abundance Analysis**: Distribution and relative abundance charts
- **Interactive Charts**: Powered by Swift Charts framework

#### 🗺️ Map Integration
- **Interactive Sampling Sites**: MapKit-based location visualization
- **Environmental Overlays**: Temperature, depth, and species distribution
- **Site Details**: Comprehensive metadata for each sampling location
- **Biodiversity Hotspots**: Visual identification of high-diversity areas

#### 📋 Report Generation
- **Automated Reports**: PDF and HTML generation from analysis results
- **Custom Templates**: Branded report formatting
- **Export Options**: Multiple format support
- **Report History**: Access to previously generated reports

### 👨‍💼 Admin Features

#### 🏠 Admin Dashboard
- **System Overview**: User statistics, dataset counts, and system health
- **Real-time Monitoring**: Performance metrics and system status
- **Activity Tracking**: Recent user actions and system events
- **Health Indicators**: API, database, and storage status monitoring

#### 👥 User Management
- **User Directory**: Complete user listing with search and filtering
- **Role Assignment**: Assign researcher or admin roles
- **Account Management**: Activate, suspend, or delete user accounts
- **User Details**: Comprehensive user profile management

#### 📁 Dataset Moderation
- **Upload Review**: Approve or reject submitted datasets
- **File Validation**: Comprehensive data quality checks
- **Metadata Verification**: Ensure complete and accurate metadata
- **Bulk Operations**: Process multiple datasets efficiently

#### 📊 System Monitoring
- **Performance Metrics**: CPU, memory, disk, and network usage
- **Job Queue Management**: Monitor background processing tasks
- **Error Logging**: Comprehensive error tracking and analysis
- **Resource Optimization**: Identify and resolve performance bottlenecks

## 🛠 Technical Architecture

### 📱 iOS Framework
- **SwiftUI**: Modern declarative UI framework
- **iOS 17+**: Latest iOS features and capabilities
- **Combine**: Reactive programming for data flow
- **Async/Await**: Modern concurrency patterns

### 🎨 Design System
- **Brand Colors**: Professional color palette with primary, secondary, and accent colors
- **Typography**: Consistent font hierarchy and sizing
- **Components**: Reusable UI components with consistent styling
- **Accessibility**: Full VoiceOver and accessibility support

### 🌐 API Integration
- **RESTful API**: Complete integration with Deep-Sea eDNA AI Pipeline
- **Base URL**: `https://api.edna-pipeline.cmlre.gov.in`
- **Authentication**: Bearer token-based security
- **Rate Limiting**: Respects API limits (1000 requests/hour, 10 pipelines/user)

### 📊 Data Visualization
- **Swift Charts**: Native iOS charting framework
- **MapKit**: Interactive map integration
- **PDFKit**: Report generation and display
- **Custom Visualizations**: Specialized taxonomic and phylogenetic displays

### 💾 Data Management
- **Core Data**: Local data persistence
- **iCloud Sync**: Cross-device data synchronization
- **Offline Support**: Cached data for offline access
- **Data Export**: Multiple format support

## 🚀 Getting Started

### Prerequisites
- Xcode 15.0 or later
- iOS 17.0 or later
- macOS 14.0 or later (for development)

### Installation
1. Clone the repository
2. Open `sih.xcodeproj` in Xcode
3. Select your target device or simulator
4. Build and run the project

### Configuration
1. Update API endpoints in `APIService.swift` if needed
2. Configure authentication settings
3. Set up Core Data model if using local storage
4. Customize brand colors in `Theme.swift`

## 📁 Project Structure

```
sih/
├── Models/
│   ├── User.swift                 # User and authentication models
│   ├── APIError.swift            # API error handling
│   ├── SequenceData.swift        # Sequence and upload models
│   └── SearchModels.swift        # Search and filter models
├── Services/
│   └── APIService.swift          # API integration service
├── DesignSystem/
│   └── Theme.swift               # Design system and theming
├── Views/
│   ├── Auth/
│   │   ├── AuthView.swift        # Login/signup interface
│   │   └── AuthManager.swift     # Authentication state management
│   ├── Common/
│   │   ├── SplashView.swift      # App launch screen
│   │   └── ProfileView.swift     # User profile management
│   ├── Main/
│   │   └── MainTabView.swift     # Main tab navigation
│   ├── Researcher/
│   │   ├── ResearcherDashboardView.swift  # Researcher dashboard
│   │   ├── UploadView.swift      # Data upload interface
│   │   ├── SearchView.swift      # Search and filtering
│   │   ├── VisualizationView.swift # Data visualization
│   │   └── MapView.swift         # Map integration
│   └── Admin/
│       ├── AdminDashboardView.swift      # Admin dashboard
│       ├── UserManagementView.swift     # User management
│       ├── DatasetModerationView.swift  # Dataset moderation
│       └── SystemMonitoringView.swift   # System monitoring
└── sihApp.swift                  # Main app entry point
```

## 🔧 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration

### Sequence Management
- `POST /api/v1/sequences/upload` - Upload sequence data
- `GET /api/v1/sequences` - Retrieve user sequences

### Search & Analysis
- `POST /api/v1/search/hierarchical` - Hierarchical search
- `GET /api/v1/search/{id}/results` - Get search results
- `POST /api/v1/ai/novel-taxa` - Novel taxa analysis
- `POST /api/v1/ai/classify` - Sequence classification

### Visualization
- `GET /api/v1/visualization/taxonomy` - Taxonomic tree data
- `GET /api/v1/visualization/phylogeny/{id}` - Phylogenetic tree data
- `GET /api/v1/biodiversity/community` - Community analysis
- `GET /api/v1/biodiversity/abundance` - Abundance analysis

### Export
- `GET /api/v1/export/{analysis_id}/report` - Generate reports

## 🎨 Design Guidelines

### Color Palette
- **Primary**: #3B82F6 (Blue)
- **Primary Light**: #60A5FA (Light Blue)
- **Primary Dark**: #2563EB (Dark Blue)
- **Secondary**: #8B5CF6 (Purple)
- **Accent**: #06B6D4 (Cyan)
- **Success**: #10B981 (Green)
- **Warning**: #F59E0B (Orange)
- **Danger**: #EF4444 (Red)

### Typography
- **Large Title**: Bold, 34pt
- **Title**: Semibold, 28pt
- **Headline**: Medium, 17pt
- **Body**: Regular, 17pt
- **Callout**: Regular, 16pt
- **Caption**: Regular, 12pt

## 🔒 Security Features

- **Token-based Authentication**: Secure API communication
- **Role-based Access Control**: Granular permission management
- **Data Encryption**: Secure local data storage
- **Input Validation**: Comprehensive data validation
- **Rate Limiting**: API abuse prevention

## 📱 Device Support

- **iPhone**: All iPhone models supporting iOS 17+
- **iPad**: Full iPad support with adaptive layouts
- **Accessibility**: Complete VoiceOver and accessibility support
- **Dark Mode**: Native dark mode support
- **Dynamic Type**: Support for user font size preferences

## 🚀 Performance Optimizations

- **Lazy Loading**: Efficient data loading and rendering
- **Image Caching**: Optimized image loading and caching
- **Background Processing**: Non-blocking data operations
- **Memory Management**: Efficient memory usage patterns
- **Network Optimization**: Minimized API calls and data transfer

## 🔮 Future Enhancements

- **Machine Learning Integration**: On-device ML capabilities
- **Real-time Collaboration**: Multi-user data sharing
- **Advanced Analytics**: Enhanced statistical analysis tools
- **Cloud Integration**: Seamless cloud data synchronization
- **AR Visualization**: Augmented reality data exploration

## 📄 License

This project is proprietary software developed for the Deep-Sea eDNA AI Pipeline research initiative.

## 👥 Contributing

This is a private research project. For questions or support, please contact the development team.

## 📞 Support

For technical support or feature requests, please contact:
- Email: support@edna-pipeline.cmlre.gov.in
- Documentation: [API Documentation](https://api.edna-pipeline.cmlre.gov.in/docs)

---

**Research Hub** - Empowering marine research through advanced eDNA analysis technology.
