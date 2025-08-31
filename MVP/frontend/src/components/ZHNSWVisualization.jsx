import { useState, useEffect } from 'react';
import { PlayIcon, PauseIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
import mockData from '../data/index.js';

const ZHNSWVisualization = ({ currentSearch, autoPlay = false }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [simulationData, setSimulationData] = useState(null);
  const [selectedZones, setSelectedZones] = useState([]);

  // Initialize simulation data
  useEffect(() => {
    setSimulationData(currentSearch || mockData.search_simulation);
  }, [currentSearch]);

  // Auto-play when requested
  useEffect(() => {
    if (autoPlay && simulationData && !isPlaying) {
      setTimeout(() => {
        playSimulation();
      }, 500); // Small delay for smooth transition
    }
  }, [autoPlay, simulationData]);

  const steps = [
    {
      id: 0,
      title: 'Query Input',
      description: 'New eDNA sequence uploaded for analysis',
      duration: 1000
    },
    {
      id: 1,
      title: 'Zone Representative Comparison',
      description: 'Compare query against 64 zone representatives',
      duration: 2300
    },
    {
      id: 2,
      title: 'Zone Selection',
      description: 'Select top 3 most similar zones using heuristic strategy',
      duration: 800
    },
    {
      id: 3,
      title: 'Parallel Search',
      description: 'Search within selected zones simultaneously',
      duration: 13100
    },
    {
      id: 4,
      title: 'Result Merging',
      description: 'Combine and rank results from all zones',
      duration: 1200
    },
    {
      id: 5,
      title: 'Classification Complete',
      description: 'Final taxonomic assignment and confidence score',
      duration: 500
    }
  ];

  const playSimulation = () => {
    if (isPlaying) {
      setIsPlaying(false);
      return;
    }

    setIsPlaying(true);
    setActiveStep(0);
    
    const runStep = (stepIndex) => {
      if (stepIndex >= steps.length) {
        setIsPlaying(false);
        return;
      }

      setActiveStep(stepIndex);
      
      // Update selected zones for visualization
      if (stepIndex === 2 && simulationData) {
        setSelectedZones(simulationData.zhnsw_process.step2_zone_selection.zones_selected);
      }

      setTimeout(() => {
        runStep(stepIndex + 1);
      }, steps[stepIndex].duration);
    };

    runStep(0);
  };

  const resetSimulation = () => {
    setIsPlaying(false);
    setActiveStep(0);
    setSelectedZones([]);
  };

  if (!simulationData) {
    return (
      <div className="card p-6">
        <div className="text-center">
          <p className="text-deep-600 dark:text-deep-300">
            No search simulation data available. Upload a sequence to see ZHNSW in action.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Control Panel */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-deep-900 dark:text-white">
            ZHNSW Algorithm Analysis
          </h3>
          <div className="flex items-center space-x-4">
            <button
              onClick={playSimulation}
              className={`btn-primary flex items-center ${isPlaying ? 'bg-red-600 hover:bg-red-700' : ''}`}
            >
              {isPlaying ? (
                <>
                  <PauseIcon className="w-5 h-5 mr-2" />
                  Pause Analysis
                </>
              ) : (
                <>
                  <PlayIcon className="w-5 h-5 mr-2" />
                  Start Analysis
                </>
              )}
            </button>
            <button
              onClick={resetSimulation}
              className="btn-secondary flex items-center"
            >
              <ArrowPathIcon className="w-5 h-5 mr-2" />
              Reset
            </button>
          </div>
        </div>

        {/* Progress Timeline */}
        <div className="relative">
          <div className="flex items-center justify-between mb-4">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`flex items-center ${index < steps.length - 1 ? 'flex-1' : ''}`}
              >
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors ${
                    index <= activeStep
                      ? 'bg-ocean-600 text-white'
                      : 'bg-deep-200 dark:bg-deep-700 text-deep-600 dark:text-deep-300'
                  }`}
                >
                  {index + 1}
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={`flex-1 h-1 mx-2 transition-colors ${
                      index < activeStep
                        ? 'bg-ocean-600'
                        : 'bg-deep-200 dark:bg-deep-700'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
          
          <div className="text-center">
            <h4 className="font-medium text-deep-900 dark:text-white">
              {steps[activeStep]?.title}
            </h4>
            <p className="text-sm text-deep-600 dark:text-deep-300 mt-1">
              {steps[activeStep]?.description}
            </p>
          </div>
        </div>
      </div>

      {/* Only show the grid when NOT in detailed view */}
      {!(activeStep === 3 || activeStep === 4 || activeStep === 5) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Zone Grid Visualization */}
          <div className="card p-6">
            <h4 className="font-medium text-deep-900 dark:text-white mb-4">
              Zone Grid (64 Zones)
            </h4>
            <ZoneGrid 
              selectedZones={selectedZones}
              activeStep={activeStep}
              zones={mockData.zones}
            />
          </div>

          {/* Detailed Step Information */}
          <div className="card p-6">
            <h4 className="font-medium text-deep-900 dark:text-white mb-4">
              Step Details
            </h4>
            <StepDetails 
              step={activeStep}
              simulation={simulationData}
              isPlaying={isPlaying}
            />
          </div>
        </div>
      )}

      {/* Show FULL WIDTH detailed zone view for steps 3, 4, 5 */}
      {(activeStep === 3 || activeStep === 4 || activeStep === 5) && selectedZones.length > 0 && (
        <div className="w-full">
          <div className="card p-8">
            <h4 className="text-2xl font-semibold text-deep-900 dark:text-white mb-8 text-center">
              {activeStep === 3 && "🔍 Zone Search Details"}
              {activeStep === 4 && "🔄 Result Merging Process"}
              {activeStep === 5 && "✅ Classification Results"}
            </h4>
            
            {/* Full width detailed view of selected zones */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 w-full">
              {selectedZones.map((zoneId, index) => {
                const zoneNumber = parseInt(zoneId.split('_')[1]);
                return (
                  <div key={zoneId} className="bg-deep-50 dark:bg-deep-800 rounded-xl p-6 border border-deep-200 dark:border-deep-700 shadow-lg w-full">
                    <div className="text-center mb-6">
                      <div className="text-2xl font-bold text-deep-900 dark:text-white">Zone {zoneNumber}</div>
                      <div className="text-lg text-deep-600 dark:text-deep-300">
                        {activeStep === 3 && "Sequence Analysis"}
                        {activeStep === 4 && "Result Processing"}
                        {activeStep === 5 && "Final Results"}
                      </div>
                    </div>
                    
                    {/* Step 3: Show sequences being searched - ENHANCED */}
                    {activeStep === 3 && (
                      <div className="space-y-4">
                        <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border shadow-sm">
                          <div className="text-sm font-medium text-deep-600 dark:text-deep-300 mb-3">Searching Sequences:</div>
                          <div className="space-y-2 text-sm font-mono">
                            <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                              <span className="text-blue-600 font-bold">SEQ_00{1250 + index * 100}</span>
                              <span className="text-green-600 font-semibold">✓ 89% match</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                              <span className="text-blue-600 font-bold">SEQ_00{1251 + index * 100}</span>
                              <span className="text-yellow-600 font-semibold">⟳ processing...</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                              <span className="text-blue-600 font-bold">SEQ_00{1252 + index * 100}</span>
                              <span className="text-red-600 font-semibold">✗ 12% match</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                              <span className="text-blue-600 font-bold">SEQ_00{1253 + index * 100}</span>
                              <span className="text-green-600 font-semibold">✓ 76% match</span>
                            </div>
                            <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                              <span className="text-blue-600 font-bold">SEQ_00{1254 + index * 100}</span>
                              <span className="text-green-600 font-semibold">✓ 82% match</span>
                            </div>
                          </div>
                        </div>
                        
                        <div className="bg-ocean-50 dark:bg-ocean-900/20 rounded-lg p-4 border border-ocean-200 dark:border-ocean-700">
                          <div className="text-sm font-medium text-ocean-700 dark:text-ocean-300 mb-2">Progress</div>
                          <div className="w-full bg-ocean-200 dark:bg-ocean-800 rounded-full h-3">
                            <div 
                              className="bg-ocean-600 h-3 rounded-full transition-all duration-1000" 
                              style={{width: `${65 + (index * 15)}%`}}
                            ></div>
                          </div>
                          <div className="text-sm text-ocean-600 dark:text-ocean-400 mt-2 flex justify-between">
                            <span>{Math.floor(1250 + (index * 850) * (0.65 + index * 0.15))} / {1250 + (index * 850)} sequences</span>
                            <span className="font-bold">{65 + (index * 15)}% complete</span>
                          </div>
                        </div>
                        
                        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4 border border-green-200 dark:border-green-700">
                          <div className="text-sm font-medium text-green-700 dark:text-green-300 mb-2">Matches Found</div>
                          <div className="grid grid-cols-2 gap-4">
                            <div className="text-center">
                              <div className="text-3xl font-bold text-green-800 dark:text-green-200">
                                {23 + (index * 8)}
                              </div>
                              <div className="text-sm text-green-600 dark:text-green-400">Total Matches</div>
                            </div>
                            <div className="text-center">
                              <div className="text-3xl font-bold text-green-800 dark:text-green-200">
                                {89 - (index * 3)}%
                              </div>
                              <div className="text-sm text-green-600 dark:text-green-400">Top Match</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    
                    {/* Step 4: Show results being merged - ENHANCED */}
                    {activeStep === 4 && (
                      <div className="space-y-4">
                        <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border shadow-sm">
                          <div className="text-sm font-medium text-deep-600 dark:text-deep-300 mb-3">Top Matches from Zone {zoneNumber}:</div>
                          <div className="space-y-3">
                            {[
                              {species: "Calanus finmarchicus", confidence: 89 - (index * 2), similarity: 94 - index},
                              {species: "Pseudocalanus minutus", confidence: 76 + index, similarity: 82 + (index * 2)},
                              {species: "Centropages typicus", confidence: 68 - index, similarity: 74 - (index * 3)},
                              {species: "Acartia tonsa", confidence: 62 + (index * 2), similarity: 69 + index},
                              {species: "Temora longicornis", confidence: 58 - index, similarity: 65 - (index * 2)}
                            ].map((match, i) => (
                              <div key={i} className="flex justify-between items-center p-3 bg-deep-50 dark:bg-deep-800 rounded-lg border">
                                <div>
                                  <div className="font-semibold text-deep-900 dark:text-white">{match.species}</div>
                                  <div className="text-sm text-deep-500 dark:text-deep-400">Similarity: {match.similarity}%</div>
                                </div>
                                <div className="text-right">
                                  <div className="text-lg font-bold text-purple-600">{match.confidence}%</div>
                                  <div className="text-xs text-deep-500">confidence</div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                        
                        <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4 border border-purple-200 dark:border-purple-700">
                          <div className="text-sm font-medium text-purple-700 dark:text-purple-300 mb-3">Merging Status</div>
                          <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                              <div className="flex justify-between text-sm">
                                <span>Results processed:</span>
                                <span className="font-mono font-bold">{23 + (index * 8)}/31</span>
                              </div>
                              <div className="flex justify-between text-sm">
                                <span>Ranking algorithm:</span>
                                <span className="text-purple-600 font-semibold">Bayesian</span>
                              </div>
                              <div className="flex justify-between text-sm">
                                <span>Confidence threshold:</span>
                                <span className="text-purple-600 font-semibold">75%</span>
                              </div>
                            </div>
                            <div className="text-center">
                              <div className="text-2xl font-bold text-purple-600">
                                {Math.floor((23 + (index * 8)) / 31 * 100)}%
                              </div>
                              <div className="text-sm text-purple-500">Complete</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    
                    {/* Step 5: Show final classification results - ENHANCED */}
                    {activeStep === 5 && (
                      <div className="space-y-4">
                        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 border border-green-200 dark:border-green-700 shadow-sm">
                          <div className="text-center mb-4">
                            <div className="text-4xl mb-2">✅</div>
                            <div className="text-lg font-bold text-green-800 dark:text-green-200">Classification Complete</div>
                          </div>
                          
                          <div className="space-y-4">
                            <div className="text-center">
                              <div className="text-2xl font-bold text-green-900 dark:text-green-100 mb-1">
                                {index === 0 ? "Calanus finmarchicus" : index === 1 ? "Pseudocalanus minutus" : "Centropages typicus"}
                              </div>
                              <div className="text-lg text-green-700 dark:text-green-300">Primary Match</div>
                            </div>
                            
                            <div className="grid grid-cols-2 gap-4">
                              <div className="bg-white dark:bg-deep-900 rounded-lg p-4 text-center shadow-sm">
                                <div className="text-3xl font-bold text-green-600">{89 - (index * 2)}%</div>
                                <div className="text-sm text-deep-500">Confidence</div>
                              </div>
                              <div className="bg-white dark:bg-deep-900 rounded-lg p-4 text-center shadow-sm">
                                <div className="text-3xl font-bold text-green-600">{94 - index}%</div>
                                <div className="text-sm text-deep-500">Similarity</div>
                              </div>
                            </div>
                            
                            <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border">
                              <div className="text-sm font-medium text-green-700 dark:text-green-300 mb-3">Classification Details:</div>
                              <div className="space-y-2 text-sm">
                                <div className="flex justify-between">
                                  <span>Taxonomic Level:</span>
                                  <span className="font-mono font-semibold">Species</span>
                                </div>
                                <div className="flex justify-between">
                                  <span>Zone Contribution:</span>
                                  <span className="font-mono font-semibold">{23 + (index * 8)} sequences</span>
                                </div>
                                <div className="flex justify-between">
                                  <span>Processing Time:</span>
                                  <span className="font-mono font-semibold">{120 + (index * 30)}ms</span>
                                </div>
                                <div className="flex justify-between">
                                  <span>Database Coverage:</span>
                                  <span className="font-mono font-semibold">{85 + index * 3}%</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        {/* Alternative matches - ENHANCED */}
                        <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border shadow-sm">
                          <div className="text-sm font-medium text-deep-600 dark:text-deep-300 mb-3">Alternative Matches:</div>
                          <div className="space-y-2">
                            {[
                              {name: "Acartia tonsa", conf: 45 + index * 5, similarity: 67 + index * 2},
                              {name: "Temora longicornis", conf: 38 - index * 2, similarity: 59 - index},
                              {name: "Oithona similis", conf: 32 + index, similarity: 54 + index * 3}
                            ].map((alt, i) => (
                              <div key={i} className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                                <div>
                                  <span className="font-medium text-deep-700 dark:text-deep-300">{alt.name}</span>
                                  <div className="text-xs text-deep-500">Similarity: {alt.similarity}%</div>
                                </div>
                                <span className="font-bold text-deep-600">{alt.conf}%</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const ZoneGrid = ({ selectedZones, activeStep, zones }) => {
  const gridSize = 8; // 8x8 grid for 64 zones
  
  return (
    <div className="relative">
      <div className="grid grid-cols-8 gap-1 aspect-square p-2">
        {Array.from({ length: 64 }, (_, i) => {
          const zoneId = `zone_${String(i + 1).padStart(3, '0')}`;
          const isSelected = selectedZones.includes(zoneId);
          const isHighlighted = activeStep >= 1;
          const isComparing = activeStep === 1;
          const isSelecting = activeStep === 2;
          const isSearching = activeStep === 3;
          const isMerging = activeStep === 4;
          const isComplete = activeStep === 5;
          
          return (
            <div
              key={zoneId}
              className={`aspect-square rounded-md flex items-center justify-center text-xs font-bold transition-all duration-500 transform cursor-pointer relative overflow-hidden ${
                isComplete && isSelected
                  ? 'bg-gradient-to-br from-green-500 to-green-700 text-white shadow-2xl scale-125 z-10 ring-4 ring-green-300'
                  : isMerging && isSelected
                  ? 'bg-gradient-to-br from-purple-500 to-purple-700 text-white shadow-2xl scale-120 z-10 ring-4 ring-purple-300'
                  : isSelected && activeStep >= 2
                  ? 'bg-gradient-to-br from-ocean-500 to-ocean-700 text-white shadow-2xl scale-125 z-10 ring-4 ring-ocean-300'
                  : isSelected && isSelecting
                  ? 'bg-gradient-to-br from-orange-400 to-orange-600 text-white shadow-lg scale-115 z-10 ring-2 ring-orange-300'
                  : isComparing
                  ? 'bg-gradient-to-br from-blue-300 to-blue-500 text-white shadow-md scale-105 animate-bounce'
                  : isHighlighted
                  ? 'bg-gradient-to-br from-ocean-100 to-ocean-200 dark:from-ocean-900 dark:to-ocean-800 text-ocean-700 dark:text-ocean-300 shadow-sm scale-102'
                  : 'bg-gradient-to-br from-deep-100 to-deep-200 dark:from-deep-700 dark:to-deep-800 text-deep-600 dark:text-deep-400 hover:scale-105'
              }`}
              style={{
                animationDelay: isComparing ? `${i * 20}ms` : '0ms',
                transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)'
              }}
              title={`Zone ${i + 1}${isSelected ? ' - Selected for Search' : ''}`}
            >
              {/* Zone Number */}
              <div className="relative z-10">{i + 1}</div>
              
              {/* Step 3: Searching Animation with Progress */}
              {isSearching && isSelected && (
                <>
                  <div className="absolute inset-0 bg-yellow-400 opacity-20 rounded-md animate-pulse"></div>
                  {/* Scanning lines */}
                  <div className="absolute top-0 left-0 w-full h-0.5 bg-yellow-300 animate-ping" style={{animationDelay: '0ms'}}></div>
                  <div className="absolute top-1/3 left-0 w-full h-0.5 bg-yellow-300 animate-ping" style={{animationDelay: '300ms'}}></div>
                  <div className="absolute top-2/3 left-0 w-full h-0.5 bg-yellow-300 animate-ping" style={{animationDelay: '600ms'}}></div>
                  {/* Corner activity indicators */}
                  <div className="absolute top-1 right-1 w-1 h-1 bg-white rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
                  <div className="absolute bottom-1 left-1 w-1 h-1 bg-white rounded-full animate-bounce" style={{animationDelay: '200ms'}}></div>
                </>
              )}
              
              {/* Step 4: Result Merging with Data Flow Animation */}
              {isMerging && isSelected && (
                <>
                  {/* Background pulse */}
                  <div className="absolute inset-0 bg-purple-400 opacity-15 rounded-md animate-pulse"></div>
                  
                  {/* Data streams flowing toward center */}
                  <div className="absolute top-0 left-1/2 w-0.5 h-2 bg-white opacity-70 animate-bounce" style={{animationDelay: '0ms'}}></div>
                  <div className="absolute bottom-0 left-1/2 w-0.5 h-2 bg-white opacity-70 animate-bounce" style={{animationDelay: '100ms'}}></div>
                  <div className="absolute left-0 top-1/2 w-2 h-0.5 bg-white opacity-70 animate-bounce" style={{animationDelay: '200ms'}}></div>
                  <div className="absolute right-0 top-1/2 w-2 h-0.5 bg-white opacity-70 animate-bounce" style={{animationDelay: '300ms'}}></div>
                  
                  {/* Central merging point */}
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-white rounded-full animate-ping" style={{animationDelay: '400ms'}}></div>
                  
                  {/* Floating data particles */}
                  <div className="absolute top-1 left-1 w-1 h-1 bg-white rounded-full animate-bounce opacity-60" style={{animationDelay: '0ms'}}></div>
                  <div className="absolute top-1 right-1 w-1 h-1 bg-white rounded-full animate-bounce opacity-60" style={{animationDelay: '150ms'}}></div>
                  <div className="absolute bottom-1 left-1 w-1 h-1 bg-white rounded-full animate-bounce opacity-60" style={{animationDelay: '300ms'}}></div>
                  <div className="absolute bottom-1 right-1 w-1 h-1 bg-white rounded-full animate-bounce opacity-60" style={{animationDelay: '450ms'}}></div>
                </>
              )}
              
              {/* Step 5: Classification Complete with Success Animation */}
              {isComplete && isSelected && (
                <>
                  {/* Success background */}
                  <div className="absolute inset-0 bg-green-400 opacity-15 rounded-md"></div>
                  
                  {/* Success checkmark animation */}
                  <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white text-lg">
                    ✓
                  </div>
                  
                  {/* Success rings expanding outward */}
                  <div className="absolute inset-0 rounded-md border-2 border-green-300 animate-ping"></div>
                  <div className="absolute inset-1 rounded-md border border-green-400 animate-ping" style={{animationDelay: '300ms'}}></div>
                  
                  {/* Sparkle effects */}
                  <div className="absolute top-1 left-2 w-0.5 h-0.5 bg-white rounded-full animate-ping" style={{animationDelay: '0ms'}}></div>
                  <div className="absolute top-2 right

- Added AnalysisPage with comprehensive statistics, tab navigation, and detailed overview.
- Introduced DownloadPage for exporting analysis results.
- Created HelpPage for user documentation and support.
- Developed SettingsPage for user configuration options.
- Implemented UnifiedAnalysisPage with file upload processing and ZHNSW visualization.
- Enhanced ZHNSW auto-play functionality and visual effects for improved user engagement.
- Resolved statistics display issues and ensured accurate data representation.
- Added mock data for testing and demonstration purposes.
- Improved overall layout and styling for a cohesive user interface.-1 w-0.5 h-0.5 bg-white rounded-full animate-ping" style={{animationDelay: '200ms'}}></div>
                  <div className="absolute bottom-1 left-1 w-0.5 h-0.5 bg-white rounded-full animate-ping" style={{animationDelay: '400ms'}}></div>
                  <div className="absolute bottom-2 right-2 w-0.5 h-0.5 bg-white rounded-full animate-ping" style={{animationDelay: '600ms'}}></div>
                </>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Show detailed zone activity during active search phases - FULL WIDTH */}
      {(activeStep === 3 || activeStep === 4 || activeStep === 5) && selectedZones.length > 0 && (
        <div className="mt-6 w-full">
          <h4 className="text-xl font-semibold text-deep-900 dark:text-white mb-6 text-center">
            {activeStep === 3 && "🔍 Zone Search Details"}
            {activeStep === 4 && "🔄 Result Merging Process"}
            {activeStep === 5 && "✅ Classification Results"}
          </h4>
          
          {/* Full width detailed view of selected zones */}
          <div className="w-full max-w-none">
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 w-full">
              {selectedZones.map((zoneId, index) => {
                const zoneNumber = parseInt(zoneId.split('_')[1]);
                return (
                  <div key={zoneId} className="bg-deep-50 dark:bg-deep-800 rounded-xl p-6 border border-deep-200 dark:border-deep-700 shadow-lg w-full">
                    <div className="text-center mb-6">
                      <div className="text-2xl font-bold text-deep-900 dark:text-white">Zone {zoneNumber}</div>
                      <div className="text-lg text-deep-600 dark:text-deep-300">
                        {activeStep === 3 && "Sequence Analysis"}
                        {activeStep === 4 && "Result Processing"}
                        {activeStep === 5 && "Final Results"}
                      </div>
                    </div>
                  
                  {/* Step 3: Show sequences being searched - ENHANCED */}
                  {activeStep === 3 && (
                    <div className="space-y-4">
                      <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border shadow-sm">
                        <div className="text-sm font-medium text-deep-600 dark:text-deep-300 mb-3">Searching Sequences:</div>
                        <div className="space-y-2 text-sm font-mono">
                          <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                            <span className="text-blue-600 font-bold">SEQ_00{1250 + index * 100}</span>
                            <span className="text-green-600 font-semibold">✓ 89% match</span>
                          </div>
                          <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                            <span className="text-blue-600 font-bold">SEQ_00{1251 + index * 100}</span>
                            <span className="text-yellow-600 font-semibold">⟳ processing...</span>
                          </div>
                          <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                            <span className="text-blue-600 font-bold">SEQ_00{1252 + index * 100}</span>
                            <span className="text-red-600 font-semibold">✗ 12% match</span>
                          </div>
                          <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                            <span className="text-blue-600 font-bold">SEQ_00{1253 + index * 100}</span>
                            <span className="text-green-600 font-semibold">✓ 76% match</span>
                          </div>
                          <div className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                            <span className="text-blue-600 font-bold">SEQ_00{1254 + index * 100}</span>
                            <span className="text-green-600 font-semibold">✓ 82% match</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="bg-ocean-50 dark:bg-ocean-900/20 rounded-lg p-4 border border-ocean-200 dark:border-ocean-700">
                        <div className="text-sm font-medium text-ocean-700 dark:text-ocean-300 mb-2">Progress</div>
                        <div className="w-full bg-ocean-200 dark:bg-ocean-800 rounded-full h-3">
                          <div 
                            className="bg-ocean-600 h-3 rounded-full transition-all duration-1000" 
                            style={{width: `${65 + (index * 15)}%`}}
                          ></div>
                        </div>
                        <div className="text-sm text-ocean-600 dark:text-ocean-400 mt-2 flex justify-between">
                          <span>{Math.floor(1250 + (index * 850) * (0.65 + index * 0.15))} / {1250 + (index * 850)} sequences</span>
                          <span className="font-bold">{65 + (index * 15)}% complete</span>
                        </div>
                      </div>
                      
                      <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4 border border-green-200 dark:border-green-700">
                        <div className="text-sm font-medium text-green-700 dark:text-green-300 mb-2">Matches Found</div>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="text-center">
                            <div className="text-3xl font-bold text-green-800 dark:text-green-200">
                              {23 + (index * 8)}
                            </div>
                            <div className="text-sm text-green-600 dark:text-green-400">Total Matches</div>
                          </div>
                          <div className="text-center">
                            <div className="text-3xl font-bold text-green-800 dark:text-green-200">
                              {89 - (index * 3)}%
                            </div>
                            <div className="text-sm text-green-600 dark:text-green-400">Top Match</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {/* Step 4: Show results being merged - ENHANCED */}
                  {activeStep === 4 && (
                    <div className="space-y-4">
                      <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border shadow-sm">
                        <div className="text-sm font-medium text-deep-600 dark:text-deep-300 mb-3">Top Matches from Zone {zoneNumber}:</div>
                        <div className="space-y-3">
                          {[
                            {species: "Calanus finmarchicus", confidence: 89 - (index * 2), similarity: 94 - index},
                            {species: "Pseudocalanus minutus", confidence: 76 + index, similarity: 82 + (index * 2)},
                            {species: "Centropages typicus", confidence: 68 - index, similarity: 74 - (index * 3)},
                            {species: "Acartia tonsa", confidence: 62 + (index * 2), similarity: 69 + index},
                            {species: "Temora longicornis", confidence: 58 - index, similarity: 65 - (index * 2)}
                          ].map((match, i) => (
                            <div key={i} className="flex justify-between items-center p-3 bg-deep-50 dark:bg-deep-800 rounded-lg border">
                              <div>
                                <div className="font-semibold text-deep-900 dark:text-white">{match.species}</div>
                                <div className="text-sm text-deep-500 dark:text-deep-400">Similarity: {match.similarity}%</div>
                              </div>
                              <div className="text-right">
                                <div className="text-lg font-bold text-purple-600">{match.confidence}%</div>
                                <div className="text-xs text-deep-500">confidence</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4 border border-purple-200 dark:border-purple-700">
                        <div className="text-sm font-medium text-purple-700 dark:text-purple-300 mb-3">Merging Status</div>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span>Results processed:</span>
                              <span className="font-mono font-bold">{23 + (index * 8)}/31</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span>Ranking algorithm:</span>
                              <span className="text-purple-600 font-semibold">Bayesian</span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span>Confidence threshold:</span>
                              <span className="text-purple-600 font-semibold">75%</span>
                            </div>
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-purple-600">
                              {Math.floor((23 + (index * 8)) / 31 * 100)}%
                            </div>
                            <div className="text-sm text-purple-500">Complete</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {/* Step 5: Show final classification results - ENHANCED */}
                  {activeStep === 5 && (
                    <div className="space-y-4">
                      <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 border border-green-200 dark:border-green-700 shadow-sm">
                        <div className="text-center mb-4">
                          <div className="text-4xl mb-2">✅</div>
                          <div className="text-lg font-bold text-green-800 dark:text-green-200">Classification Complete</div>
                        </div>
                        
                        <div className="space-y-4">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-green-900 dark:text-green-100 mb-1">
                              {index === 0 ? "Calanus finmarchicus" : index === 1 ? "Pseudocalanus minutus" : "Centropages typicus"}
                            </div>
                            <div className="text-lg text-green-700 dark:text-green-300">Primary Match</div>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-4">
                            <div className="bg-white dark:bg-deep-900 rounded-lg p-4 text-center shadow-sm">
                              <div className="text-3xl font-bold text-green-600">{89 - (index * 2)}%</div>
                              <div className="text-sm text-deep-500">Confidence</div>
                            </div>
                            <div className="bg-white dark:bg-deep-900 rounded-lg p-4 text-center shadow-sm">
                              <div className="text-3xl font-bold text-green-600">{94 - index}%</div>
                              <div className="text-sm text-deep-500">Similarity</div>
                            </div>
                          </div>
                          
                          <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border">
                            <div className="text-sm font-medium text-green-700 dark:text-green-300 mb-3">Classification Details:</div>
                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span>Taxonomic Level:</span>
                                <span className="font-mono font-semibold">Species</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Zone Contribution:</span>
                                <span className="font-mono font-semibold">{23 + (index * 8)} sequences</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Processing Time:</span>
                                <span className="font-mono font-semibold">{120 + (index * 30)}ms</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Database Coverage:</span>
                                <span className="font-mono font-semibold">{85 + index * 3}%</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Alternative matches - ENHANCED */}
                      <div className="bg-white dark:bg-deep-900 rounded-lg p-4 border shadow-sm">
                        <div className="text-sm font-medium text-deep-600 dark:text-deep-300 mb-3">Alternative Matches:</div>
                        <div className="space-y-2">
                          {[
                            {name: "Acartia tonsa", conf: 45 + index * 5, similarity: 67 + index * 2},
                            {name: "Temora longicornis", conf: 38 - index * 2, similarity: 59 - index},
                            {name: "Oithona similis", conf: 32 + index, similarity: 54 + index * 3}
                          ].map((alt, i) => (
                            <div key={i} className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-800 rounded">
                              <div>
                                <span className="font-medium text-deep-700 dark:text-deep-300">{alt.name}</span>
                                <div className="text-xs text-deep-500">Similarity: {alt.similarity}%</div>
                              </div>
                              <span className="font-bold text-deep-600">{alt.conf}%</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
            </div>
          </div>
        </div>
      )}
      
      {/* Enhanced Legend */}
      <div className="mt-4 space-y-2">
        <div className="flex items-center justify-center space-x-6 text-sm flex-wrap gap-2">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-gradient-to-br from-deep-100 to-deep-200 dark:from-deep-700 dark:to-deep-800 rounded mr-2"></div>
            <span className="text-deep-600 dark:text-deep-300">Inactive</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-gradient-to-br from-blue-300 to-blue-500 rounded mr-2"></div>
            <span className="text-deep-600 dark:text-deep-300">Comparing</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-gradient-to-br from-orange-400 to-orange-600 rounded mr-2"></div>
            <span className="text-deep-600 dark:text-deep-300">Selecting</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-gradient-to-br from-ocean-500 to-ocean-700 rounded mr-2"></div>
            <span className="text-deep-600 dark:text-deep-300">Searching</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-gradient-to-br from-purple-500 to-purple-700 rounded mr-2"></div>
            <span className="text-deep-600 dark:text-deep-300">Merging</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-gradient-to-br from-green-500 to-green-700 rounded mr-2"></div>
            <span className="text-deep-600 dark:text-deep-300">Complete</span>
          </div>
        </div>
        
        {/* Step-specific information */}
        <div className="text-center text-sm text-deep-600 dark:text-deep-300">
          {activeStep === 1 && "Searching 64 of 64 zones • 100% coverage"}
          {activeStep === 2 && `Selected ${selectedZones.length} zones • ${Math.round((selectedZones.length / 64) * 100)}% efficiency`}
          {activeStep === 3 && `Analyzing sequences in ${selectedZones.length} selected zones`}
          {activeStep === 4 && `Merging results from ${selectedZones.length} zones • Ranking by similarity`}
          {activeStep === 5 && `Classification complete • ${selectedZones.length} zones processed successfully`}
        </div>
      </div>
    </div>
  );
};

const StepDetails = ({ step, simulation, isPlaying }) => {
  const stepData = simulation.zhnsw_process;
  
  const getStepContent = () => {
    switch (step) {
      case 0:
        return (
          <div className="space-y-3">
            <h5 className="font-medium text-deep-900 dark:text-white">Query Sequence</h5>
            <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
              <div className="text-sm text-deep-600 dark:text-deep-300 mb-1">Sequence ID:</div>
              <div className="font-mono text-deep-900 dark:text-white">{simulation.query_sequence.id}</div>
              <div className="text-sm text-deep-600 dark:text-deep-300 mt-2 mb-1">Length:</div>
              <div className="text-deep-900 dark:text-white">{simulation.query_sequence.length} bp</div>
            </div>
          </div>
        );
        
      case 1:
        return (
          <div className="space-y-3">
            <h5 className="font-medium text-deep-900 dark:text-white">Zone Representative Comparison</h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-deep-600 dark:text-deep-300">Total Zones:</div>
                <div className="text-xl font-semibold text-deep-900 dark:text-white">{stepData.step1_zone_comparison.total_zones}</div>
              </div>
              <div>
                <div className="text-sm text-deep-600 dark:text-deep-300">Processing Time:</div>
                <div className="text-xl font-semibold text-green-600">{stepData.step1_zone_comparison.time_ms}ms</div>
              </div>
            </div>
            <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
              <h6 className="font-medium text-deep-900 dark:text-white mb-2">Top Zone Matches:</h6>
              <div className="space-y-1">
                {stepData.step1_zone_comparison.top_zones.slice(0, 3).map((zone, i) => (
                  <div key={zone.zone_id} className="flex justify-between text-sm">
                    <span className="text-deep-900 dark:text-white">{zone.zone_id}</span>
                    <span className="text-ocean-600 dark:text-ocean-400">{(zone.similarity * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
        
      case 2:
        return (
          <div className="space-y-3">
            <h5 className="font-medium text-deep-900 dark:text-white">Intelligent Zone Selection</h5>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-deep-600 dark:text-deep-300">Strategy:</div>
                <div className="text-deep-900 dark:text-white capitalize">{stepData.step2_zone_selection.strategy.replace('_', ' ')}</div>
              </div>
              <div>
                <div className="text-sm text-deep-600 dark:text-deep-300">Zones Selected:</div>
                <div className="text-xl font-semibold text-ocean-600">{stepData.step2_zone_selection.zones_selected.length}</div>
              </div>
              <div>
                <div className="text-sm text-deep-600 dark:text-deep-300">Zones Skipped:</div>
                <div className="text-xl font-semibold text-green-600">{stepData.step2_zone_selection.zones_skipped}</div>
              </div>
            </div>
          </div>
        );
        
      case 3:
        return (
          <div className="space-y-3">
            <h5 className="font-medium text-deep-900 dark:text-white">Parallel Search Execution</h5>
            <div className="space-y-3">
              {stepData.step3_parallel_search.searches.map((search, i) => (
                <div key={search.zone_id} className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
                  <div className="flex justify-between items-center mb-2">
                    <h6 className="font-medium text-deep-900 dark:text-white">{search.zone_id}</h6>
                    <span className="text-sm text-green-600">{search.time_ms}ms</span>
                  </div>
                  <div className="text-sm text-deep-600 dark:text-deep-300">
                    Searched {search.sequences_searched.toLocaleString()} sequences
                  </div>
                  <div className="text-sm text-deep-600 dark:text-deep-300">
                    Found {search.top_matches.length} top matches
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
        
      case 4:
        return (
          <div className="space-y-3">
            <h5 className="font-medium text-deep-900 dark:text-white">Result Merging & Ranking</h5>
            <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
              <div className="space-y-2">
                {stepData.step4_result_merging.final_results.map((result, i) => (
                  <div key={result.seq_id} className="flex justify-between items-center">
                    <div>
                      <div className="font-mono text-sm text-deep-900 dark:text-white">{result.seq_id}</div>
                      <div className="text-xs text-deep-600 dark:text-deep-300">{result.taxon}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-semibold text-ocean-600">{(result.similarity * 100).toFixed(1)}%</div>
                      <div className="text-xs text-deep-600 dark:text-deep-300">confidence: {(result.confidence * 100).toFixed(1)}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
        
      case 5:
        return (
          <div className="space-y-3">
            <h5 className="font-medium text-deep-900 dark:text-white">Final Classification</h5>
            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-green-700 dark:text-green-300">Predicted Taxon:</div>
                  <div className="font-semibold text-green-900 dark:text-green-100">{simulation.classification_result.predicted_taxon}</div>
                </div>
                <div>
                  <div className="text-sm text-green-700 dark:text-green-300">Confidence:</div>
                  <div className="text-xl font-bold text-green-900 dark:text-green-100">{(simulation.classification_result.confidence * 100).toFixed(1)}%</div>
                </div>
              </div>
              <div className="mt-3">
                <div className="text-sm text-green-700 dark:text-green-300">Functional Annotation:</div>
                <div className="text-green-900 dark:text-green-100">{simulation.classification_result.functional_annotation}</div>
              </div>
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };

  return (
    <div className="min-h-[200px]">
      {isPlaying && (
        <div className="mb-4 flex items-center text-ocean-600 dark:text-ocean-400">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-ocean-600 mr-2"></div>
          Processing step {step + 1}...
        </div>
      )}
      {getStepContent()}
    </div>
  );
};

export default ZHNSWVisualization;
