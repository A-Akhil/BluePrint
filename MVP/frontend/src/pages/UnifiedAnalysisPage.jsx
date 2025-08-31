import { useState, useEffect } from 'react';
import { useAppStore } from '../store/index.js';
import mockData from '../data/index.js';
import { 
  BeakerIcon, 
  ChartBarIcon, 
  MapIcon,
  DocumentTextIcon,
  CloudArrowUpIcon
} from '@heroicons/react/24/outline';
import UploadProcessor from '../components/UploadProcessor.jsx';
import ZHNSWVisualization from '../components/ZHNSWVisualization.jsx';

const UnifiedAnalysisPage = () => {
  const { 
    getStatistics,
    simulateZHNSWSearch,
    uploadedFile: storeUploadedFile,
    setUploadedFile
  } = useAppStore();
  
  const [localUploadedFile, setLocalUploadedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadResults, setUploadResults] = useState(null);
  const [shouldAutoPlayZHNSW, setShouldAutoPlayZHNSW] = useState(false);
  
  // Use direct sequences from mockData instead of filtered
  const sequences = mockData.sequences;
  const statistics = getStatistics();

  // Check if there's an uploaded file from the store (from LandingPage)
  useEffect(() => {
    if (storeUploadedFile && !isProcessing) {
      setLocalUploadedFile(storeUploadedFile);
      setIsProcessing(true);
      // Clear the file from store after we start processing
      setUploadedFile(null);
    }
  }, [storeUploadedFile, isProcessing, setUploadedFile]);

  // Reset auto-play flag after some time
  useEffect(() => {
    if (shouldAutoPlayZHNSW) {
      const timer = setTimeout(() => {
        setShouldAutoPlayZHNSW(false);
      }, 10000); // Reset after 10 seconds
      return () => clearTimeout(timer);
    }
  }, [shouldAutoPlayZHNSW]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setLocalUploadedFile(file);
      setIsProcessing(true);
    }
  };

  const handleProcessingComplete = (results) => {
    setUploadResults(results);
    setIsProcessing(false);
    setLocalUploadedFile(null);
    
    // Trigger ZHNSW auto-play after upload
    setShouldAutoPlayZHNSW(true);
    
    // Simulate adding new sequences to the system
    simulateZHNSWSearch(`uploaded_sequence_${Date.now()}`);
  };

  // Sample zones data for visualization
  const topZones = [
    { id: 'zone_001', name: 'Mariana Trench Deep', sequences: 1247, novelty: 23 },
    { id: 'zone_012', name: 'Abyssal Plain Alpha', sequences: 892, novelty: 18 },
    { id: 'zone_008', name: 'Hydrothermal Vent Beta', sequences: 1456, novelty: 34 },
    { id: 'zone_025', name: 'Hadal Zone Gamma', sequences: 567, novelty: 12 }
  ];

  // Sample species data
  const topSpecies = [
    { name: 'Deep-sea Protista sp.', count: 1247, confidence: 87, novel: false },
    { name: 'Unknown eukaryote ABYS-001', count: 892, confidence: 23, novel: true },
    { name: 'Cnidaria sp. TRENCH-445', count: 756, confidence: 91, novel: false },
    { name: 'Novel Foraminifera DEEP-089', count: 445, confidence: 34, novel: true },
    { name: 'Radiolaria sp. PACIFIC-334', count: 334, confidence: 78, novel: false }
  ];

  // Sample diversity metrics
  const diversityData = [
    { zone: 'Abyssal Plains', shannon: 3.2, simpson: 0.85, species: 45 },
    { zone: 'Hydrothermal Vents', shannon: 2.8, simpson: 0.78, species: 38 },
    { zone: 'Deep Trenches', shannon: 2.1, simpson: 0.65, species: 28 },
    { zone: 'Seamount Ridges', shannon: 3.7, simpson: 0.92, species: 52 }
  ];

  return (
    <div className="min-h-screen bg-deep-50 dark:bg-deep-900">
      {isProcessing && (
        <UploadProcessor 
          file={localUploadedFile} 
          onComplete={handleProcessingComplete} 
        />
      )}
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with Upload */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 className="text-3xl font-bold text-deep-900 dark:text-white">
                Deep-Sea eDNA Biodiversity Explorer
              </h1>
              <p className="mt-2 text-deep-600 dark:text-deep-300">
                Advanced taxonomic classification powered by ZHNSW algorithm
              </p>
            </div>
            
            <div className="relative">
              <input
                type="file"
                accept=".fasta,.fa,.fastq,.fq,.txt"
                onChange={handleFileUpload}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-ocean-600 hover:bg-ocean-700 cursor-pointer transition-colors duration-200"
              >
                <CloudArrowUpIcon className="w-5 h-5 mr-2" />
                Upload New Sample
              </label>
            </div>
          </div>
          
          {uploadResults && (
            <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
              <div className="flex items-center">
                <BeakerIcon className="w-5 h-5 text-green-600 dark:text-green-400 mr-2" />
                <span className="text-green-800 dark:text-green-200 font-medium">
                  Upload Complete: {uploadResults.totalSequences} sequences processed, 
                  {uploadResults.novelSpecies} novel species detected
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Overview Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DocumentTextIcon className="w-8 h-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-deep-600 dark:text-deep-300">Total Sequences</p>
                <p className="text-2xl font-semibold text-deep-900 dark:text-white">
                  {statistics.total.toLocaleString()}
                </p>
              </div>
            </div>
          </div>
          
          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BeakerIcon className="w-8 h-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-deep-600 dark:text-deep-300">Novel Species</p>
                <p className="text-2xl font-semibold text-deep-900 dark:text-white">
                  {statistics.novel.toLocaleString()}
                </p>
                <p className="text-xs text-green-600">
                  {statistics.total > 0 ? ((statistics.novel / statistics.total) * 100).toFixed(1) : '0'}% discovery rate
                </p>
              </div>
            </div>
          </div>
          
          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="w-8 h-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-deep-600 dark:text-deep-300">High Confidence</p>
                <p className="text-2xl font-semibold text-deep-900 dark:text-white">
                  {statistics.highConfidence.toLocaleString()}
                </p>
                <p className="text-xs text-purple-600">
                  {statistics.total > 0 ? ((statistics.highConfidence / statistics.total) * 100).toFixed(1) : '0'}% accuracy
                </p>
              </div>
            </div>
          </div>
          
          <div className="card p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <MapIcon className="w-8 h-8 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-deep-600 dark:text-deep-300">Avg Confidence</p>
                <p className="text-2xl font-semibold text-deep-900 dark:text-white">
                  {isNaN(statistics.avgConfidence) ? '0' : (statistics.avgConfidence * 100).toFixed(1)}%
                </p>
                <p className="text-xs text-orange-600">Classification certainty</p>
              </div>
            </div>
          </div>
        </div>

        {/* ZHNSW Algorithm Visualization */}
        <div className="mb-8">
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4 flex items-center">
              <ChartBarIcon className="w-5 h-5 mr-2 text-blue-600" />
              ZHNSW Algorithm Performance
            </h3>
            <ZHNSWVisualization autoPlay={shouldAutoPlayZHNSW} />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Species Discovery */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4 flex items-center">
              <BeakerIcon className="w-5 h-5 mr-2 text-green-600" />
              Top Species Discoveries
            </h3>
            <div className="space-y-3">
              {topSpecies.map((species, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-deep-50 dark:bg-deep-700 rounded">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-deep-900 dark:text-white text-sm">
                        {species.name}
                      </span>
                      {species.novel && (
                        <span className="px-2 py-1 bg-amber-100 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 text-xs rounded">
                          Novel
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-deep-600 dark:text-deep-400">
                      {species.count} sequences • {species.confidence}% confidence
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Zone Analysis */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4 flex items-center">
              <MapIcon className="w-5 h-5 mr-2 text-blue-600" />
              Biogeographic Zones
            </h3>
            <div className="space-y-3">
              {topZones.map((zone, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-deep-50 dark:bg-deep-700 rounded">
                  <div className="flex-1">
                    <div className="font-medium text-deep-900 dark:text-white text-sm">
                      {zone.name}
                    </div>
                    <div className="text-xs text-deep-600 dark:text-deep-400">
                      {zone.sequences} sequences • {zone.novelty}% novel species
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="w-16 bg-deep-200 dark:bg-deep-600 rounded-full h-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full"
                        style={{ width: `${(zone.novelty / 40) * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Diversity Analysis */}
        <div className="mt-8">
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4 flex items-center">
              <ChartBarIcon className="w-5 h-5 mr-2 text-purple-600" />
              Biodiversity Metrics by Habitat
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {diversityData.map((data, idx) => (
                <div key={idx} className="p-4 bg-deep-50 dark:bg-deep-700 rounded-lg">
                  <h4 className="font-medium text-deep-900 dark:text-white text-sm mb-3">
                    {data.zone}
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-deep-600 dark:text-deep-400">Shannon Index:</span>
                      <span className="font-medium text-deep-900 dark:text-white">{data.shannon}</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-deep-600 dark:text-deep-400">Simpson Index:</span>
                      <span className="font-medium text-deep-900 dark:text-white">{data.simpson}</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-deep-600 dark:text-deep-400">Species Count:</span>
                      <span className="font-medium text-deep-900 dark:text-white">{data.species}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-8">
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4">
              Recent Analysis Activity
            </h3>
            <div className="space-y-3">
              {sequences.slice(0, 8).map((seq, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 border-l-4 border-ocean-500 bg-deep-50 dark:bg-deep-700">
                  <div className="flex-1">
                    <div className="font-medium text-deep-900 dark:text-white text-sm">
                      {seq.predicted_taxon}
                    </div>
                    <div className="text-xs text-deep-600 dark:text-deep-400">
                      Zone: {seq.zone_id} • Confidence: {(seq.confidence * 100).toFixed(0)}%
                      {seq.novel && <span className="ml-2 text-amber-600">• Novel Species</span>}
                    </div>
                  </div>
                  <div className="text-xs text-deep-500 dark:text-deep-400">
                    {seq.id}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UnifiedAnalysisPage;
