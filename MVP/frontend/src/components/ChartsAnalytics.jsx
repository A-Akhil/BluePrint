import { useState, useMemo } from 'react';
import { 
  ChartBarIcon, 
  ChartPieIcon, 
  PresentationChartLineIcon,
  ArrowTrendingUpIcon,
  BeakerIcon,
  MapIcon
} from '@heroicons/react/24/outline';
import mockData from '../data/index.js';

const ChartsAnalytics = () => {
  const [activeChart, setActiveChart] = useState('abundance');
  const [timeRange, setTimeRange] = useState('all');
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);

  const charts = [
    { id: 'abundance', name: 'Abundance Chart', icon: ChartBarIcon },
    { id: 'diversity', name: 'Diversity Metrics', icon: PresentationChartLineIcon },
    { id: 'novelty', name: 'Novelty Analysis', icon: ArrowTrendingUpIcon },
    { id: 'taxonomy', name: 'Taxonomy Distribution', icon: ChartPieIcon },
    { id: 'zones', name: 'Zone Performance', icon: MapIcon },
    { id: 'confidence', name: 'Confidence Analysis', icon: BeakerIcon }
  ];

  const filteredSequences = useMemo(() => {
    return mockData.sequences.filter(seq => seq.confidence >= confidenceThreshold);
  }, [confidenceThreshold]);

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-deep-900 dark:text-white">
            Charts & Analytics
          </h3>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <label className="text-sm text-deep-600 dark:text-deep-300">
                Confidence Threshold:
              </label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={confidenceThreshold}
                onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
                className="w-24"
              />
              <span className="text-sm font-medium text-deep-900 dark:text-white">
                {(confidenceThreshold * 100).toFixed(0)}%
              </span>
            </div>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-3 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white"
            >
              <option value="all">All Time</option>
              <option value="recent">Recent</option>
              <option value="month">This Month</option>
            </select>
          </div>
        </div>
        
        <div className="flex flex-wrap gap-2">
          {charts.map(chart => (
            <button
              key={chart.id}
              onClick={() => setActiveChart(chart.id)}
              className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeChart === chart.id
                  ? 'bg-ocean-600 text-white'
                  : 'bg-deep-100 dark:bg-deep-700 text-deep-700 dark:text-deep-300 hover:bg-deep-200 dark:hover:bg-deep-600'
              }`}
            >
              <chart.icon className="w-4 h-4 mr-2" />
              {chart.name}
            </button>
          ))}
        </div>
      </div>

      {/* Chart Content */}
      <div className="space-y-6">
        {activeChart === 'abundance' && <AbundanceChart sequences={filteredSequences} />}
        {activeChart === 'diversity' && <DiversityMetrics sequences={filteredSequences} />}
        {activeChart === 'novelty' && <NoveltyAnalysis sequences={filteredSequences} />}
        {activeChart === 'taxonomy' && <TaxonomyDistribution sequences={filteredSequences} />}
        {activeChart === 'zones' && <ZonePerformance />}
        {activeChart === 'confidence' && <ConfidenceAnalysis sequences={filteredSequences} />}
      </div>
    </div>
  );
};

const AbundanceChart = ({ sequences }) => {
  const abundanceData = useMemo(() => {
    const counts = {};
    sequences.forEach(seq => {
      const genus = seq.predicted_taxon?.split(' ')[0] || 'Unknown';
      counts[genus] = (counts[genus] || 0) + 1;
    });
    
    return Object.entries(counts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 15)
      .map(([genus, count]) => ({ genus, count }));
  }, [sequences]);

  const maxCount = Math.max(...abundanceData.map(d => d.count));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        <div className="card p-6">
          <h4 className="font-medium text-deep-900 dark:text-white mb-4">
            Top 15 Genera by Abundance
          </h4>
          <div className="space-y-3">
            {abundanceData.map((item, index) => (
              <div key={item.genus} className="flex items-center">
                <div className="w-24 text-sm text-deep-600 dark:text-deep-300 font-mono">
                  {item.genus}
                </div>
                <div className="flex-1 mx-4">
                  <div className="w-full bg-deep-200 dark:bg-deep-700 rounded-full h-6 relative">
                    <div 
                      className="bg-gradient-to-r from-ocean-500 to-ocean-600 h-6 rounded-full flex items-center justify-end pr-2"
                      style={{ width: `${(item.count / maxCount) * 100}%` }}
                    >
                      <span className="text-white text-xs font-medium">
                        {item.count}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="w-12 text-right">
                  <span className="text-xs text-deep-600 dark:text-deep-300">
                    #{index + 1}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="space-y-4">
        <AbundanceStats sequences={sequences} />
        <TopFindings abundanceData={abundanceData} />
      </div>
    </div>
  );
};

const AbundanceStats = ({ sequences }) => {
  const stats = useMemo(() => {
    const genera = new Set(sequences.map(seq => seq.taxon.split(' ')[0]));
    const species = new Set(sequences.map(seq => seq.taxon));
    const novelCount = sequences.filter(seq => seq.novelty_flag).length;
    
    return {
      totalSequences: sequences.length,
      uniqueGenera: genera.size,
      uniqueSpecies: species.size,
      novelSpecies: novelCount,
      noveltyRate: (novelCount / sequences.length) * 100
    };
  }, [sequences]);

  return (
    <div className="card p-6">
      <h4 className="font-medium text-deep-900 dark:text-white mb-4">
        Abundance Statistics
      </h4>
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Total Sequences:</span>
          <span className="font-semibold text-deep-900 dark:text-white">
            {stats.totalSequences.toLocaleString()}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Unique Genera:</span>
          <span className="font-semibold text-deep-900 dark:text-white">
            {stats.uniqueGenera}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Unique Species:</span>
          <span className="font-semibold text-deep-900 dark:text-white">
            {stats.uniqueSpecies}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Novel Species:</span>
          <span className="font-semibold text-amber-600 dark:text-amber-400">
            {stats.novelSpecies}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Novelty Rate:</span>
          <span className="font-semibold text-amber-600 dark:text-amber-400">
            {stats.noveltyRate.toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
};

const TopFindings = ({ abundanceData }) => {
  return (
    <div className="card p-6">
      <h4 className="font-medium text-deep-900 dark:text-white mb-4">
        Key Findings
      </h4>
      <div className="space-y-3 text-sm">
        <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded">
          <div className="font-medium text-green-800 dark:text-green-200 mb-1">
            Dominant Genus
          </div>
          <div className="text-green-700 dark:text-green-300">
            {abundanceData[0]?.genus} represents the highest abundance with {abundanceData[0]?.count} sequences
          </div>
        </div>
        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
          <div className="font-medium text-blue-800 dark:text-blue-200 mb-1">
            Diversity Insight
          </div>
          <div className="text-blue-700 dark:text-blue-300">
            Top 5 genera account for a significant portion of total abundance, indicating community structure
          </div>
        </div>
        <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded">
          <div className="font-medium text-purple-800 dark:text-purple-200 mb-1">
            Research Impact
          </div>
          <div className="text-purple-700 dark:text-purple-300">
            Abundance patterns reveal deep-sea ecosystem composition and potential indicator species
          </div>
        </div>
      </div>
    </div>
  );
};

const DiversityMetrics = ({ sequences }) => {
  const metrics = useMemo(() => {
    // Calculate Shannon Diversity Index
    const species = {};
    sequences.forEach(seq => {
      species[seq.taxon] = (species[seq.taxon] || 0) + 1;
    });
    
    const total = sequences.length;
    const shannon = -Object.values(species).reduce((sum, count) => {
      const p = count / total;
      return sum + p * Math.log(p);
    }, 0);
    
    // Calculate Simpson Index
    const simpson = Object.values(species).reduce((sum, count) => {
      const p = count / total;
      return sum + p * p;
    }, 0);
    
    // Calculate evenness
    const speciesCount = Object.keys(species).length;
    const maxShannon = Math.log(speciesCount);
    const evenness = shannon / maxShannon;
    
    return {
      shannon: shannon,
      simpson: 1 - simpson, // Simpson's Diversity Index
      evenness: evenness,
      richness: speciesCount,
      dominance: Math.max(...Object.values(species)) / total
    };
  }, [sequences]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-6">
          Biodiversity Indices
        </h4>
        <div className="space-y-6">
          <DiversityMeter 
            label="Shannon Index"
            value={metrics.shannon}
            max={5}
            color="green"
            description="Measures species diversity considering both richness and evenness"
          />
          <DiversityMeter 
            label="Simpson Index"
            value={metrics.simpson}
            max={1}
            color="blue"
            description="Probability that two randomly selected individuals are different species"
          />
          <DiversityMeter 
            label="Evenness"
            value={metrics.evenness}
            max={1}
            color="purple"
            description="How evenly species are distributed in the community"
          />
        </div>
      </div>
      
      <div className="space-y-6">
        <div className="card p-6">
          <h4 className="font-medium text-deep-900 dark:text-white mb-4">
            Community Structure
          </h4>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-deep-900 dark:text-white">
                {metrics.richness}
              </div>
              <div className="text-sm text-deep-600 dark:text-deep-300">
                Species Richness
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-deep-900 dark:text-white">
                {(metrics.dominance * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-deep-600 dark:text-deep-300">
                Dominance
              </div>
            </div>
          </div>
        </div>
        
        <DiversityInterpretation metrics={metrics} />
      </div>
    </div>
  );
};

const DiversityMeter = ({ label, value, max, color, description }) => {
  const percentage = (value / max) * 100;
  
  const colorClasses = {
    green: 'bg-green-500',
    blue: 'bg-blue-500',
    purple: 'bg-purple-500'
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        <span className="font-medium text-deep-900 dark:text-white">{label}</span>
        <span className="text-sm font-semibold text-deep-900 dark:text-white">
          {value.toFixed(3)}
        </span>
      </div>
      <div className="w-full bg-deep-200 dark:bg-deep-700 rounded-full h-3 mb-2">
        <div 
          className={`${colorClasses[color]} h-3 rounded-full transition-all duration-500`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
      <p className="text-xs text-deep-600 dark:text-deep-400">{description}</p>
    </div>
  );
};

const DiversityInterpretation = ({ metrics }) => {
  const getInterpretation = () => {
    if (metrics.shannon > 3) {
      return {
        level: 'Very High',
        color: 'green',
        description: 'Exceptional biodiversity indicating a highly diverse and healthy ecosystem'
      };
    } else if (metrics.shannon > 2) {
      return {
        level: 'High',
        color: 'blue',
        description: 'Good biodiversity with well-distributed species abundance'
      };
    } else if (metrics.shannon > 1) {
      return {
        level: 'Moderate',
        color: 'yellow',
        description: 'Moderate diversity with some species dominance patterns'
      };
    } else {
      return {
        level: 'Low',
        color: 'red',
        description: 'Lower diversity possibly indicating environmental stress or specialization'
      };
    }
  };

  const interpretation = getInterpretation();

  return (
    <div className="card p-6">
      <h4 className="font-medium text-deep-900 dark:text-white mb-4">
        Ecological Interpretation
      </h4>
      <div className={`p-4 rounded-lg bg-${interpretation.color}-50 dark:bg-${interpretation.color}-900/20`}>
        <div className={`font-semibold text-${interpretation.color}-800 dark:text-${interpretation.color}-200 mb-2`}>
          Diversity Level: {interpretation.level}
        </div>
        <div className={`text-${interpretation.color}-700 dark:text-${interpretation.color}-300 text-sm`}>
          {interpretation.description}
        </div>
      </div>
    </div>
  );
};

const NoveltyAnalysis = ({ sequences }) => {
  const noveltyData = useMemo(() => {
    const novel = sequences.filter(seq => seq.novelty_flag);
    const known = sequences.filter(seq => !seq.novelty_flag);
    
    const confidenceBins = {
      'Very High (>90%)': { novel: 0, known: 0 },
      'High (80-90%)': { novel: 0, known: 0 },
      'Medium (60-80%)': { novel: 0, known: 0 },
      'Low (<60%)': { novel: 0, known: 0 }
    };
    
    sequences.forEach(seq => {
      const conf = seq.confidence;
      const type = seq.novelty_flag ? 'novel' : 'known';
      
      if (conf > 0.9) confidenceBins['Very High (>90%)'][type]++;
      else if (conf > 0.8) confidenceBins['High (80-90%)'][type]++;
      else if (conf > 0.6) confidenceBins['Medium (60-80%)'][type]++;
      else confidenceBins['Low (<60%)'][type]++;
    });
    
    return {
      novel: novel.length,
      known: known.length,
      total: sequences.length,
      noveltyRate: (novel.length / sequences.length) * 100,
      confidenceBins
    };
  }, [sequences]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-6">
          Novelty Detection Results
        </h4>
        
        <div className="mb-6">
          <div className="flex items-center justify-center w-32 h-32 mx-auto mb-4 relative">
            <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="text-deep-200 dark:text-deep-700"
              />
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeDasharray={`${noveltyData.noveltyRate}, 100`}
                className="text-amber-500"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-xl font-bold text-deep-900 dark:text-white">
                  {noveltyData.noveltyRate.toFixed(1)}%
                </div>
                <div className="text-xs text-deep-600 dark:text-deep-300">
                  Novel
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 bg-amber-50 dark:bg-amber-900/20 rounded">
            <span className="text-amber-800 dark:text-amber-200">Novel Species</span>
            <span className="font-semibold text-amber-900 dark:text-amber-100">
              {noveltyData.novel.toLocaleString()}
            </span>
          </div>
          <div className="flex justify-between items-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
            <span className="text-blue-800 dark:text-blue-200">Known Species</span>
            <span className="font-semibold text-blue-900 dark:text-blue-100">
              {noveltyData.known.toLocaleString()}
            </span>
          </div>
        </div>
      </div>
      
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-4">
          Confidence Distribution
        </h4>
        <div className="space-y-3">
          {Object.entries(noveltyData.confidenceBins).map(([range, counts]) => (
            <div key={range}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-deep-600 dark:text-deep-300">{range}</span>
                <span className="text-deep-900 dark:text-white">
                  {counts.novel + counts.known} total
                </span>
              </div>
              <div className="flex h-6 bg-deep-200 dark:bg-deep-700 rounded overflow-hidden">
                <div 
                  className="bg-blue-500 flex items-center justify-center text-xs text-white"
                  style={{ width: `${(counts.known / (counts.novel + counts.known || 1)) * 100}%` }}
                >
                  {counts.known > 0 && counts.known}
                </div>
                <div 
                  className="bg-amber-500 flex items-center justify-center text-xs text-white"
                  style={{ width: `${(counts.novel / (counts.novel + counts.known || 1)) * 100}%` }}
                >
                  {counts.novel > 0 && counts.novel}
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="flex items-center justify-center space-x-4 mt-4 text-xs">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-blue-500 rounded mr-1"></div>
            <span className="text-deep-600 dark:text-deep-300">Known</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-amber-500 rounded mr-1"></div>
            <span className="text-deep-600 dark:text-deep-300">Novel</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const TaxonomyDistribution = ({ sequences }) => {
  const distributionData = useMemo(() => {
    const kingdoms = {};
    const phyla = {};
    const classes = {};
    
    sequences.forEach(seq => {
      const parts = seq.taxon.split(' ');
      if (parts.length > 0) {
        kingdoms[parts[0]] = (kingdoms[parts[0]] || 0) + 1;
      }
      if (parts.length > 1) {
        phyla[parts[1]] = (phyla[parts[1]] || 0) + 1;
      }
      if (parts.length > 2) {
        classes[parts[2]] = (classes[parts[2]] || 0) + 1;
      }
    });
    
    return { kingdoms, phyla, classes };
  }, [sequences]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <TaxonomyLevel title="Kingdoms" data={distributionData.kingdoms} color="blue" />
      <TaxonomyLevel title="Phyla" data={distributionData.phyla} color="green" />
      <TaxonomyLevel title="Classes" data={distributionData.classes} color="purple" />
    </div>
  );
};

const TaxonomyLevel = ({ title, data, color }) => {
  const sortedData = Object.entries(data)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 8);
  
  const total = Object.values(data).reduce((sum, count) => sum + count, 0);

  return (
    <div className="card p-6">
      <h4 className="font-medium text-deep-900 dark:text-white mb-4">
        {title} Distribution
      </h4>
      <div className="space-y-2">
        {sortedData.map(([name, count]) => (
          <div key={name}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-deep-900 dark:text-white truncate">{name}</span>
              <span className="text-deep-600 dark:text-deep-300">
                {((count / total) * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-deep-200 dark:bg-deep-700 rounded-full h-2">
              <div 
                className={`bg-${color}-500 h-2 rounded-full`}
                style={{ width: `${(count / total) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const ZonePerformance = () => {
  const performanceData = useMemo(() => {
    return mockData.zones.map(zone => ({
      ...zone,
      efficiency: 1000 / zone.avg_search_time_ms,
      throughput: zone.sequence_count / zone.avg_search_time_ms
    })).sort((a, b) => b.efficiency - a.efficiency);
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-4">
          Zone Performance Ranking
        </h4>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {performanceData.slice(0, 20).map((zone, index) => (
            <div key={zone.zone_id} className="flex items-center justify-between p-2 bg-deep-50 dark:bg-deep-800 rounded">
              <div className="flex items-center">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                  index < 3 ? 'bg-yellow-500 text-yellow-900' : 'bg-deep-200 dark:bg-deep-600 text-deep-700 dark:text-deep-300'
                }`}>
                  {index + 1}
                </div>
                <span className="ml-3 text-sm font-medium text-deep-900 dark:text-white">
                  {zone.zone_id}
                </span>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold text-deep-900 dark:text-white">
                  {zone.avg_search_time_ms}ms
                </div>
                <div className="text-xs text-deep-600 dark:text-deep-300">
                  {zone.throughput.toFixed(1)} seq/ms
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-4">
          Performance Distribution
        </h4>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-deep-600 dark:text-deep-300">Search Time (ms)</label>
            <div className="mt-2 space-y-1">
              {['< 200', '200-400', '400-600', '> 600'].map((range, index) => {
                const count = performanceData.filter(z => {
                  const time = z.avg_search_time_ms;
                  if (index === 0) return time < 200;
                  if (index === 1) return time >= 200 && time < 400;
                  if (index === 2) return time >= 400 && time < 600;
                  return time >= 600;
                }).length;
                
                return (
                  <div key={range} className="flex items-center justify-between">
                    <span className="text-sm text-deep-600 dark:text-deep-300">{range}</span>
                    <div className="flex items-center">
                      <div className="w-20 bg-deep-200 dark:bg-deep-700 rounded-full h-2 mr-2">
                        <div 
                          className="bg-ocean-500 h-2 rounded-full"
                          style={{ width: `${(count / performanceData.length) * 100}%` }}
                        />
                      </div>
                      <span className="text-sm text-deep-900 dark:text-white w-6">{count}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ConfidenceAnalysis = ({ sequences }) => {
  const confidenceData = useMemo(() => {
    const bins = {
      'Very High (>90%)': [],
      'High (80-90%)': [],
      'Medium (60-80%)': [],
      'Low (<60%)': []
    };
    
    sequences.forEach(seq => {
      const conf = seq.confidence;
      if (conf > 0.9) bins['Very High (>90%)'].push(seq);
      else if (conf > 0.8) bins['High (80-90%)'].push(seq);
      else if (conf > 0.6) bins['Medium (60-80%)'].push(seq);
      else bins['Low (<60%)'].push(seq);
    });
    
    return bins;
  }, [sequences]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-4">
          Confidence Level Distribution
        </h4>
        <div className="space-y-4">
          {Object.entries(confidenceData).map(([level, seqs]) => (
            <div key={level}>
              <div className="flex justify-between mb-2">
                <span className="text-deep-600 dark:text-deep-300">{level}</span>
                <span className="font-semibold text-deep-900 dark:text-white">
                  {seqs.length} ({((seqs.length / sequences.length) * 100).toFixed(1)}%)
                </span>
              </div>
              <div className="w-full bg-deep-200 dark:bg-deep-700 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-3 rounded-full"
                  style={{ width: `${(seqs.length / sequences.length) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-4">
          Confidence Insights
        </h4>
        <div className="space-y-3">
          <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded">
            <div className="font-medium text-green-800 dark:text-green-200 mb-1">
              High Confidence Rate
            </div>
            <div className="text-green-700 dark:text-green-300 text-sm">
              {((confidenceData['Very High (>90%)'].length + confidenceData['High (80-90%)'].length) / sequences.length * 100).toFixed(1)}% of sequences have high confidence (&gt;80%)
            </div>
          </div>
          <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
            <div className="font-medium text-blue-800 dark:text-blue-200 mb-1">
              Quality Assessment
            </div>
            <div className="text-blue-700 dark:text-blue-300 text-sm">
              Strong confidence distribution indicates reliable taxonomic assignments
            </div>
          </div>
          <div className="p-3 bg-amber-50 dark:bg-amber-900/20 rounded">
            <div className="font-medium text-amber-800 dark:text-amber-200 mb-1">
              Low Confidence Cases
            </div>
            <div className="text-amber-700 dark:text-amber-300 text-sm">
              {confidenceData['Low (<60%)'].length} sequences require manual review or additional analysis
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChartsAnalytics;
