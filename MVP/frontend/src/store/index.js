import { create } from 'zustand';
import mockData, { dataUtils } from '../data/index.js';

// Main application store
export const useAppStore = create((set, get) => ({
  // Data state
  sequences: mockData.sequences,
  zones: mockData.zones,
  currentSearch: null,
  selectedZones: [],
  uploadedFile: null,
  
  // UI state
  darkMode: false,
  currentPage: 'landing',
  isLoading: false,
  searchQuery: '',
  filters: {
    novel: null,
    minConfidence: 0,
    taxon: '',
    zoneId: '',
    dateRange: null
  },
  
  // Table state
  pagination: {
    page: 1,
    limit: 50,
    total: mockData.sequences.length
  },
  sortConfig: {
    key: 'confidence',
    direction: 'desc'
  },
  
  // Actions
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
  
  setCurrentPage: (page) => set({ currentPage: page }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setUploadedFile: (file) => set({ uploadedFile: file }),
  
  setSearchQuery: (query) => set({ searchQuery: query }),
  
  updateFilters: (newFilters) => set((state) => ({
    filters: { ...state.filters, ...newFilters }
  })),
  
  clearFilters: () => set({
    filters: {
      novel: null,
      minConfidence: 0,
      taxon: '',
      zoneId: '',
      dateRange: null
    },
    searchQuery: ''
  }),
  
  // Pagination
  setPage: (page) => set((state) => ({
    pagination: { ...state.pagination, page }
  })),
  
  setPageLimit: (limit) => set((state) => ({
    pagination: { ...state.pagination, limit, page: 1 }
  })),
  
  // Sorting
  setSortConfig: (key, direction) => set({
    sortConfig: { key, direction }
  }),
  
  // Search and filter sequences
  getFilteredSequences: () => {
    const { searchQuery, filters, sortConfig } = get();
    let results = dataUtils.searchSequences(searchQuery, filters);
    
    // Apply sorting
    if (sortConfig.key) {
      results.sort((a, b) => {
        const aVal = a[sortConfig.key];
        const bVal = b[sortConfig.key];
        
        if (typeof aVal === 'string') {
          return sortConfig.direction === 'asc' 
            ? aVal.localeCompare(bVal)
            : bVal.localeCompare(aVal);
        } else {
          return sortConfig.direction === 'asc'
            ? aVal - bVal
            : bVal - aVal;
        }
      });
    }
    
    return results;
  },
  
  // Get paginated sequences
  getPaginatedSequences: () => {
    const { pagination } = get();
    const filtered = get().getFilteredSequences();
    const startIndex = (pagination.page - 1) * pagination.limit;
    const endIndex = startIndex + pagination.limit;
    
    return {
      data: filtered.slice(startIndex, endIndex),
      total: filtered.length,
      hasNext: endIndex < filtered.length,
      hasPrev: pagination.page > 1
    };
  },
  
  // ZHNSW simulation
  simulateZHNSWSearch: (querySequence) => {
    set({ isLoading: true });
    
    // Simulate search delay
    setTimeout(() => {
      const searchResult = {
        ...mockData.search_simulation,
        query_sequence: querySequence,
        timestamp: new Date().toISOString()
      };
      
      set({ 
        currentSearch: searchResult,
        isLoading: false,
        currentPage: 'analysis'
      });
    }, 2000);
  },
  
  // Zone selection for visualization
  selectZones: (zoneIds) => set({ selectedZones: zoneIds }),
  
  // Get statistics
  getStatistics: () => {
    // Use direct sequences data instead of filtered results for initial stats
    const sequences = mockData.sequences;
    if (!sequences || sequences.length === 0) {
      return {
        total: 0,
        novel: 0,
        highConfidence: 0,
        avgConfidence: 0
      };
    }
    
    return {
      total: sequences.length,
      novel: sequences.filter(s => s.novel).length,
      highConfidence: sequences.filter(s => s.confidence > 0.8).length,
      avgConfidence: sequences.reduce((sum, s) => sum + s.confidence, 0) / sequences.length
    };
  }
}));

// Search store for advanced search functionality
export const useSearchStore = create((set, get) => ({
  searchHistory: [],
  savedSearches: [],
  quickFilters: [
    { name: 'Novel Sequences', filters: { novel: true } },
    { name: 'High Confidence', filters: { minConfidence: 0.8 } },
    { name: 'Protista', filters: { taxon: 'Protista' } },
    { name: 'Unknown', filters: { taxon: 'Unknown' } }
  ],
  
  addToHistory: (searchQuery, filters, resultCount) => {
    const historyItem = {
      id: Date.now(),
      query: searchQuery,
      filters,
      resultCount,
      timestamp: new Date().toISOString()
    };
    
    set((state) => ({
      searchHistory: [historyItem, ...state.searchHistory.slice(0, 9)] // Keep last 10
    }));
  },
  
  saveSearch: (name, query, filters) => {
    const savedSearch = {
      id: Date.now(),
      name,
      query,
      filters,
      created: new Date().toISOString()
    };
    
    set((state) => ({
      savedSearches: [...state.savedSearches, savedSearch]
    }));
  },
  
  removeSavedSearch: (id) => {
    set((state) => ({
      savedSearches: state.savedSearches.filter(s => s.id !== id)
    }));
  },
  
  applySavedSearch: (savedSearch) => {
    // This would typically update the main app store
    useAppStore.getState().setSearchQuery(savedSearch.query);
    useAppStore.getState().updateFilters(savedSearch.filters);
  }
}));

export default useAppStore;
