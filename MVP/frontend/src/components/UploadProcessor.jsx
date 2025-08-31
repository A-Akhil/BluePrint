import { useState, useEffect } from 'react';
import { 
  CheckCircleIcon, 
  BeakerIcon, 
  ChartBarIcon,
  MagnifyingGlassIcon,
  CpuChipIcon
} from '@heroicons/react/24/outline';

const UploadProcessor = ({ file, onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [detectedSequences, setDetectedSequences] = useState([]);
  const [processingResults, setProcessingResults] = useState(null);

  const steps = [
    { name: 'File Validation', duration: 800 },
    { name: 'Sequence Extraction', duration: 1200 },
    { name: 'Quality Assessment', duration: 1000 },
    { name: 'ZHNSW Index Search', duration: 2000 },
    { name: 'Taxonomic Classification', duration: 1500 },
    { name: 'Biogeographic Assignment', duration: 800 },
    { name: 'Analysis Complete', duration: 500 }
  ];

  const mockSequenceNames = [
    'Deep-sea Protista sp. ABYS-001',
    'Uncharacterized eukaryote HADAL-237',
    'Cnidaria sp. TRENCH-445',
    'Novel Foraminifera DEEP-089',
    'Metazoan candidate ABYSSAL-162',
    'Radiolaria sp. PACIFIC-334',
    'Unknown flagellate MARIANA-078',
    'Dinoflagellata DEPTHS-291'
  ];

  const mockTaxonomy = [
    { taxon: 'Eukaryota; Protista; Unclassified', confidence: 0.23, novel: true },
    { taxon: 'Eukaryota; Cnidaria; Anthozoa; Hexacorallia', confidence: 0.87, novel: false },
    { taxon: 'Eukaryota; Foraminifera; Globothalamea', confidence: 0.65, novel: true },
    { taxon: 'Eukaryota; Metazoa; Unclassified', confidence: 0.34, novel: true },
    { taxon: 'Eukaryota; Dinoflagellata; Gymnodiniales', confidence: 0.76, novel: false }
  ];

  useEffect(() => {
    const processFile = async () => {
      for (let i = 0; i < steps.length; i++) {
        setCurrentStep(i);
        
        // Simulate processing time
        await new Promise(resolve => {
          const duration = steps[i].duration;
          const interval = 50;
          let elapsed = 0;
          
          const progressInterval = setInterval(() => {
            elapsed += interval;
            const stepProgress = Math.min((elapsed / duration) * 100, 100);
            const totalProgress = ((i * 100) + stepProgress) / steps.length;
            setProgress(totalProgress);
            
            // Add sequences during extraction step
            if (i === 1 && stepProgress > 30) {
              const numSequences = Math.min(Math.floor(stepProgress / 20), mockSequenceNames.length);
              setDetectedSequences(mockSequenceNames.slice(0, numSequences));
            }
            
            if (elapsed >= duration) {
              clearInterval(progressInterval);
              resolve();
            }
          }, interval);
        });
      }
      
      // Generate final results
      const results = {
        totalSequences: Math.floor(Math.random() * 5) + 3,
        novelSpecies: Math.floor(Math.random() * 3) + 1,
        avgConfidence: (Math.random() * 0.4 + 0.6).toFixed(2),
        taxonomicAssignments: mockTaxonomy.slice(0, Math.floor(Math.random() * 3) + 2),
        processingTime: '1.8s',
        zhnsWQueries: Math.floor(Math.random() * 50) + 20
      };
      
      setProcessingResults(results);
      
      // Complete after showing results
      setTimeout(() => {
        onComplete(results);
      }, 2000);
    };
    
    processFile();
  }, [file]);

  if (processingResults) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white dark:bg-deep-800 rounded-lg max-w-2xl w-full p-8">
          <div className="text-center mb-6">
            <CheckCircleIcon className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-deep-900 dark:text-white mb-2">
              Analysis Complete
            </h3>
            <p className="text-deep-600 dark:text-deep-300">
              Your eDNA sequences have been successfully processed
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {processingResults.totalSequences}
              </div>
              <div className="text-sm text-blue-700 dark:text-blue-300">Sequences Detected</div>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                {processingResults.novelSpecies}
              </div>
              <div className="text-sm text-green-700 dark:text-green-300">Novel Species</div>
            </div>
            <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {processingResults.avgConfidence}
              </div>
              <div className="text-sm text-purple-700 dark:text-purple-300">Avg Confidence</div>
            </div>
            <div className="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg text-center">
              <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
                {processingResults.processingTime}
              </div>
              <div className="text-sm text-orange-700 dark:text-orange-300">Processing Time</div>
            </div>
          </div>
          
          <div className="border-t border-deep-200 dark:border-deep-600 pt-4">
            <h4 className="font-semibold text-deep-900 dark:text-white mb-3">Taxonomic Classifications:</h4>
            <div className="space-y-2">
              {processingResults.taxonomicAssignments.map((assignment, idx) => (
                <div key={idx} className="flex justify-between items-center p-2 bg-deep-50 dark:bg-deep-700 rounded">
                  <span className="text-sm text-deep-700 dark:text-deep-300">{assignment.taxon}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium">{(assignment.confidence * 100).toFixed(0)}%</span>
                    {assignment.novel && (
                      <span className="px-2 py-1 bg-amber-100 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 text-xs rounded">
                        Novel
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-deep-800 rounded-lg max-w-2xl w-full p-8">
        <div className="text-center mb-8">
          <BeakerIcon className="w-16 h-16 text-ocean-500 mx-auto mb-4 animate-pulse" />
          <h3 className="text-2xl font-bold text-deep-900 dark:text-white mb-2">
            Processing eDNA Sequences
          </h3>
          <p className="text-deep-600 dark:text-deep-300">
            Analyzing {file?.name} using ZHNSW algorithm
          </p>
        </div>
        
        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-deep-700 dark:text-deep-300">
              {steps[currentStep]?.name}
            </span>
            <span className="text-sm text-deep-600 dark:text-deep-400">
              {Math.round(progress)}%
            </span>
          </div>
          <div className="w-full bg-deep-200 dark:bg-deep-700 rounded-full h-2">
            <div 
              className="bg-ocean-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
        
        {/* Processing Steps */}
        <div className="space-y-3 mb-6">
          {steps.map((step, index) => (
            <div key={index} className="flex items-center">
              <div className={`w-4 h-4 rounded-full mr-3 ${
                index < currentStep ? 'bg-green-500' :
                index === currentStep ? 'bg-ocean-500 animate-pulse' :
                'bg-deep-300 dark:bg-deep-600'
              }`} />
              <span className={`text-sm ${
                index <= currentStep ? 'text-deep-900 dark:text-white' : 'text-deep-500 dark:text-deep-400'
              }`}>
                {step.name}
              </span>
              {index === currentStep && (
                <CpuChipIcon className="w-4 h-4 ml-2 text-ocean-500 animate-spin" />
              )}
            </div>
          ))}
        </div>
        
        {/* Detected Sequences */}
        {detectedSequences.length > 0 && (
          <div className="border-t border-deep-200 dark:border-deep-600 pt-4">
            <h4 className="text-sm font-semibold text-deep-900 dark:text-white mb-3 flex items-center">
              <MagnifyingGlassIcon className="w-4 h-4 mr-2" />
              Detected Sequences ({detectedSequences.length})
            </h4>
            <div className="space-y-1 max-h-32 overflow-y-auto">
              {detectedSequences.map((seq, idx) => (
                <div key={idx} className="text-xs text-deep-600 dark:text-deep-400 p-2 bg-deep-50 dark:bg-deep-700 rounded">
                  {seq}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadProcessor;
