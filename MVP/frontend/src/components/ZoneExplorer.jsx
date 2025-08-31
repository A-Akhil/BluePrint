import { useState, useMemo } from 'react';
import { 
  MapIcon, 
  ClockIcon, 
  CpuChipIcon, 
  ChartBarIcon,
  MagnifyingGlassIcon,
  ArrowTopRightOnSquareIcon,
  BeakerIcon
} from '@heroicons/react/24/outline';
import mockData from '../data/index.js';

const ZoneExplorer = () => {
  const [selectedZone, setSelectedZone] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // grid, list, performance
  const [sortBy, setSortBy] = useState('zone_id'); // zone_id, sequences, performance, diversity
  const [searchQuery, setSearchQuery] = useState('');

  const filteredZones = useMemo(() => {
    let zones = mockData.zones.filter(zone => 
      searchQuery === '' || 
      zone.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      zone.location_info.toString().toLowerCase().includes(searchQuery.toLowerCase())
    );

    zones.sort((a, b) => {
      switch (sortBy) {
        case 'sequences':
          return b.sequences.length - a.sequences.length;
        case 'performance':
          return a.performance_metrics.avg_search_time_ms - b.performance_metrics.avg_search_time_ms;
        case 'diversity':
          return Object.keys(b.taxa_distribution).length - Object.keys(a.taxa_distribution).length;
        default:
          return a.id.localeCompare(b.id);
      }
    });

    return zones;
  }, [searchQuery, sortBy]);

  const performanceStats = useMemo(() => {
    const zones = mockData.zones;
    return {
      totalZones: zones.length,
      avgSearchTime: zones.reduce((sum, z) => sum + z.avg_search_time_ms, 0) / zones.length,
      totalSequences: zones.reduce((sum, z) => sum + z.sequence_count, 0),
      avgDiversity: zones.reduce((sum, z) => sum + z.diversity_index, 0) / zones.length,
      fastestZone: zones.reduce((min, z) => z.avg_search_time_ms < min.avg_search_time_ms ? z : min),
      slowestZone: zones.reduce((max, z) => z.avg_search_time_ms > max.avg_search_time_ms ? z : max),
      mostDiverse: zones.reduce((max, z) => z.diversity_index > max.diversity_index ? z : max),
      leastDiverse: zones.reduce((min, z) => z.diversity_index < min.diversity_index ? z : min)
    };
  }, []);

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-deep-900 dark:text-white">
            Zone Explorer
          </h3>
          <div className="flex items-center space-x-4">
            <select
              value={viewMode}
              onChange={(e) => setViewMode(e.target.value)}
              className="px-3 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white"
            >
              <option value="grid">Grid View</option>
              <option value="list">List View</option>
              <option value="performance">Performance View</option>
            </select>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white"
            >
              <option value="zone_id">Zone ID</option>
              <option value="sequences">Sequence Count</option>
              <option value="performance">Performance</option>
              <option value="diversity">Diversity</option>
            </select>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="relative flex-1">
            <MagnifyingGlassIcon className="absolute left-3 top-3 h-5 w-5 text-deep-400" />
            <input
              type="text"
              placeholder="Search zones..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white placeholder-deep-500 dark:placeholder-deep-400"
            />
          </div>
          <div className="text-sm text-deep-600 dark:text-deep-300">
            {filteredZones.length} of {mockData.zones.length} zones
          </div>
        </div>
      </div>

      {/* Performance Overview */}
      <PerformanceOverview stats={performanceStats} />

      {/* Zone Display */}
      {viewMode === 'grid' && (
        <ZoneGrid 
          zones={filteredZones} 
          selectedZone={selectedZone}
          onSelectZone={setSelectedZone}
        />
      )}
      
      {viewMode === 'list' && (
        <ZoneList 
          zones={filteredZones}
          selectedZone={selectedZone}
          onSelectZone={setSelectedZone}
        />
      )}
      
      {viewMode === 'performance' && (
        <PerformanceView zones={filteredZones} />
      )}

      {/* Zone Details Modal */}
      {selectedZone && (
        <ZoneDetailsModal 
          zone={selectedZone}
          onClose={() => setSelectedZone(null)}
        />
      )}
    </div>
  );
};

const PerformanceOverview = ({ stats }) => {
  const metrics = [
    {
      label: 'Total Zones',
      value: stats.totalZones,
      icon: MapIcon,
      color: 'blue'
    },
    {
      label: 'Avg Search Time',
      value: `${stats.avgSearchTime.toFixed(1)}ms`,
      icon: ClockIcon,
      color: 'green'
    },
    {
      label: 'Total Sequences',
      value: stats.totalSequences.toLocaleString(),
      icon: BeakerIcon,
      color: 'purple'
    },
    {
      label: 'Avg Diversity',
      value: stats.avgDiversity.toFixed(2),
      icon: ChartBarIcon,
      color: 'orange'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <div key={index} className="card p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-deep-600 dark:text-deep-300">{metric.label}</p>
              <p className="text-2xl font-semibold text-deep-900 dark:text-white">{metric.value}</p>
            </div>
            <div className={`p-3 rounded-lg bg-${metric.color}-100 dark:bg-${metric.color}-900/20`}>
              <metric.icon className={`w-6 h-6 text-${metric.color}-600 dark:text-${metric.color}-400`} />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

const ZoneGrid = ({ zones, selectedZone, onSelectZone }) => {
  const getZoneColor = (zone) => {
    const performance = zone.performance_metrics.avg_search_time_ms;
    if (performance < 15) return 'bg-green-100 dark:bg-green-900/20 border-green-200 dark:border-green-800';
    if (performance < 20) return 'bg-yellow-100 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800';
    return 'bg-red-100 dark:bg-red-900/20 border-red-200 dark:border-red-800';
  };

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-3">
      {zones.map(zone => (
        <div
          key={zone.id}
          onClick={() => onSelectZone(zone)}
          className={`
            p-3 rounded-lg border-2 cursor-pointer transition-all duration-200 hover:scale-105
            ${getZoneColor(zone)}
            ${selectedZone?.id === zone.id 
              ? 'ring-2 ring-ocean-500 border-ocean-500' 
              : 'hover:border-deep-400 dark:hover:border-deep-500'
            }
          `}
        >
          <div className="text-center">
            <div className="font-semibold text-deep-900 dark:text-white text-sm">
              {zone.id.replace('zone_', '')}
            </div>
            <div className="text-xs text-deep-600 dark:text-deep-300 mt-1">
              {zone.sequences.length.toLocaleString()}
            </div>
            <div className="text-xs text-deep-500 dark:text-deep-400">
              {zone.performance_metrics.avg_search_time_ms.toFixed(1)}ms
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

const ZoneList = ({ zones, selectedZone, onSelectZone }) => {
  return (
    <div className="card">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-deep-50 dark:bg-deep-800">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-deep-500 dark:text-deep-400 uppercase tracking-wider">
                Zone
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-deep-500 dark:text-deep-400 uppercase tracking-wider">
                Location
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-deep-500 dark:text-deep-400 uppercase tracking-wider">
                Sequences
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-deep-500 dark:text-deep-400 uppercase tracking-wider">
                Search Time
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-deep-500 dark:text-deep-400 uppercase tracking-wider">
                Diversity
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-deep-500 dark:text-deep-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-deep-200 dark:divide-deep-700">
            {zones.map(zone => (
              <tr 
                key={zone.id}
                className={`hover:bg-deep-50 dark:hover:bg-deep-800 cursor-pointer ${
                  selectedZone?.id === zone.id 
                    ? 'bg-ocean-50 dark:bg-ocean-900/20' 
                    : ''
                }`}
                onClick={() => onSelectZone(zone)}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-deep-900 dark:text-white">
                    {zone.id}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-deep-600 dark:text-deep-300">
                    {`${zone.location_info.latitude.toFixed(2)}, ${zone.location_info.longitude.toFixed(2)}`}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-deep-900 dark:text-white">
                    {zone.sequences.length.toLocaleString()}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="text-sm text-deep-900 dark:text-white mr-2">
                      {zone.avg_search_time_ms}ms
                    </div>
                    <div className={`w-2 h-2 rounded-full ${
                      zone.avg_search_time_ms < 200 ? 'bg-green-500' :
                      zone.avg_search_time_ms < 400 ? 'bg-yellow-500' : 'bg-red-500'
                    }`} />
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-deep-900 dark:text-white">
                    {zone.diversity_index.toFixed(2)}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectZone(zone);
                    }}
                    className="text-ocean-600 dark:text-ocean-400 hover:text-ocean-800 dark:hover:text-ocean-200"
                  >
                    <ArrowTopRightOnSquareIcon className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const PerformanceView = ({ zones }) => {
  const performanceData = useMemo(() => {
    return zones.map(zone => ({
      ...zone,
      efficiency: 1000 / zone.performance_metrics.avg_search_time_ms, // Higher is better
      sequences_per_ms: zone.sequences.length / zone.performance_metrics.avg_search_time_ms
    })).sort((a, b) => b.efficiency - a.efficiency);
  }, [zones]);

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <h4 className="font-medium text-deep-900 dark:text-white mb-4">
          Performance Ranking
        </h4>
        <div className="space-y-3">
          {performanceData.slice(0, 10).map((zone, index) => (
            <div key={zone.id} className="flex items-center justify-between p-3 bg-deep-50 dark:bg-deep-800 rounded">
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                  index === 0 ? 'bg-yellow-500 text-yellow-900' :
                  index === 1 ? 'bg-gray-400 text-gray-900' :
                  index === 2 ? 'bg-orange-500 text-orange-900' :
                  'bg-deep-200 dark:bg-deep-600 text-deep-700 dark:text-deep-300'
                }`}>
                  {index + 1}
                </div>
                <div className="ml-3">
                  <div className="font-medium text-deep-900 dark:text-white">{zone.id}</div>
                  <div className="text-sm text-deep-600 dark:text-deep-300">
                    {`${zone.location_info.latitude.toFixed(2)}, ${zone.location_info.longitude.toFixed(2)}`}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-semibold text-deep-900 dark:text-white">
                  {zone.performance_metrics.avg_search_time_ms.toFixed(1)}ms
                </div>
                <div className="text-sm text-deep-600 dark:text-deep-300">
                  {zone.sequences_per_ms.toFixed(1)} seq/ms
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-6">
          <h4 className="font-medium text-deep-900 dark:text-white mb-4">
            Search Time Distribution
          </h4>
          <div className="space-y-2">
            {['< 200ms', '200-400ms', '> 400ms'].map((range, index) => {
              const count = zones.filter(z => {
                if (index === 0) return z.avg_search_time_ms < 200;
                if (index === 1) return z.avg_search_time_ms >= 200 && z.avg_search_time_ms < 400;
                return z.avg_search_time_ms >= 400;
              }).length;
              const percentage = (count / zones.length) * 100;
              
              return (
                <div key={range} className="flex items-center justify-between">
                  <span className="text-sm text-deep-600 dark:text-deep-300">{range}</span>
                  <div className="flex items-center">
                    <div className="w-24 bg-deep-200 dark:bg-deep-700 rounded-full h-2 mr-2">
                      <div 
                        className={`h-2 rounded-full ${
                          index === 0 ? 'bg-green-500' : 
                          index === 1 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium text-deep-900 dark:text-white">
                      {count} ({percentage.toFixed(1)}%)
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="card p-6">
          <h4 className="font-medium text-deep-900 dark:text-white mb-4">
            Diversity vs Performance
          </h4>
          <div className="text-sm text-deep-600 dark:text-deep-300">
            Correlation analysis between zone diversity and search performance would be displayed here
            as an interactive scatter plot.
          </div>
        </div>
      </div>
    </div>
  );
};

const ZoneDetailsModal = ({ zone, onClose }) => {
  const [activeTab, setActiveTab] = useState('overview');
  
  const tabs = [
    { id: 'overview', name: 'Overview' },
    { id: 'performance', name: 'Performance' },
    { id: 'sequences', name: 'Sequences' },
    { id: 'location', name: 'Location' }
  ];

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-deep-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-deep-200 dark:border-deep-600">
          <h3 className="text-lg font-semibold text-deep-900 dark:text-white">
            {zone.id} - Details
          </h3>
          <button
            onClick={onClose}
            className="text-deep-400 hover:text-deep-600 dark:hover:text-deep-300"
          >
            <ArrowTopRightOnSquareIcon className="w-6 h-6 rotate-180" />
          </button>
        </div>

        <div className="flex border-b border-deep-200 dark:border-deep-600">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-ocean-50 dark:bg-ocean-900/20 text-ocean-600 dark:text-ocean-400 border-b-2 border-ocean-600'
                  : 'text-deep-600 dark:text-deep-300 hover:bg-deep-50 dark:hover:bg-deep-700'
              }`}
            >
              {tab.name}
            </button>
          ))}
        </div>

        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Zone ID</label>
                  <div className="text-deep-900 dark:text-white">{zone.id}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Location</label>
                  <div className="text-deep-900 dark:text-white">
                    {`${zone.location_info.latitude.toFixed(2)}, ${zone.location_info.longitude.toFixed(2)}`}
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Depth Range</label>
                  <div className="text-deep-900 dark:text-white">
                    {zone.location_info.depth_range[0]}-{zone.location_info.depth_range[1]}m
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Sequence Count</label>
                  <div className="text-2xl font-semibold text-deep-900 dark:text-white">
                    {zone.sequences?.length?.toLocaleString() || '0'}
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Taxa Count</label>
                  <div className="text-2xl font-semibold text-deep-900 dark:text-white">
                    {Object.keys(zone.taxa_distribution || {}).length}
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Average Search Time</label>
                  <div className="text-2xl font-semibold text-deep-900 dark:text-white">
                    {zone.performance_metrics?.avg_search_time_ms?.toFixed(1) || '0'}ms
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'performance' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded">
                  <div className="text-green-700 dark:text-green-300 text-sm">Search Time</div>
                  <div className="text-green-900 dark:text-green-100 text-xl font-semibold">
                    {zone.performance_metrics?.avg_search_time_ms?.toFixed(1) || '0'}ms
                  </div>
                </div>
                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded">
                  <div className="text-blue-700 dark:text-blue-300 text-sm">Hit Rate</div>
                  <div className="text-blue-900 dark:text-blue-100 text-xl font-semibold">
                    {((zone.performance_metrics?.hit_rate || 0) * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded">
                  <div className="text-purple-700 dark:text-purple-300 text-sm">Novelty Rate</div>
                  <div className="text-purple-900 dark:text-purple-100 text-xl font-semibold">
                    {((zone.performance_metrics?.novelty_rate || 0) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'sequences' && (
            <div className="space-y-4">
              <div className="text-deep-600 dark:text-deep-300">
                This zone contains {(zone.sequences?.length || 0).toLocaleString()} sequences with {Object.keys(zone.taxa_distribution || {}).length} distinct taxa.
              </div>
              <div className="bg-deep-50 dark:bg-deep-800 p-4 rounded">
                <div className="text-sm text-deep-600 dark:text-deep-300">
                  Detailed sequence listing and analysis would be displayed here, 
                  including taxonomic breakdown and novelty detection results.
                </div>
              </div>
            </div>
          )}

          {activeTab === 'location' && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Latitude</label>
                  <div className="text-deep-900 dark:text-white">{zone.representative_coords.lat.toFixed(6)}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-deep-700 dark:text-deep-300">Longitude</label>
                  <div className="text-deep-900 dark:text-white">{zone.representative_coords.lon.toFixed(6)}</div>
                </div>
              </div>
              <div className="bg-deep-50 dark:bg-deep-800 p-4 rounded h-64 flex items-center justify-center">
                <div className="text-deep-600 dark:text-deep-300">
                  Interactive map visualization would be displayed here showing the zone location,
                  sampling sites, and geographic context.
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ZoneExplorer;
