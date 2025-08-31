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
          
          return (
            <div
              key={zoneId}
              className={`aspect-square rounded-md flex items-center justify-center text-xs font-bold transition-all duration-500 transform cursor-pointer ${
                isSelected && activeStep >= 2
                  ? 'bg-gradient-to-br from-ocean-500 to-ocean-700 text-white shadow-2xl scale-125 z-10 ring-4 ring-ocean-300 animate-pulse'
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
              {i + 1}
              {isSearching && isSelected && (
                <div className="absolute inset-0 bg-yellow-400 opacity-30 rounded-md animate-ping"></div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Enhanced Legend */}
      <div className="mt-4 space-y-2">
        <div className="flex items-center justify-center space-x-6 text-sm">
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
            <span className="text-deep-600 dark:text-deep-300">Active Search</span>
          </div>
        </div>
        {activeStep >= 2 && selectedZones.length > 0 && (
          <div className="text-center text-sm text-ocean-600 dark:text-ocean-400 font-medium">
            Searching {selectedZones.length} of 64 zones • {((selectedZones.length / 64) * 100).toFixed(0)}% efficiency
          </div>
        )}
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
