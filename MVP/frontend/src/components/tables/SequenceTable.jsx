import { useState } from 'react';
import { 
  MagnifyingGlassIcon, 
  FunnelIcon, 
  ChevronUpIcon, 
  ChevronDownIcon,
  EyeIcon,
  CloudArrowDownIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

const SequenceTable = ({ 
  data, 
  searchQuery, 
  setSearchQuery, 
  filters, 
  updateFilters, 
  clearFilters,
  showFilters, 
  setShowFilters,
  sortConfig, 
  setSortConfig,
  pagination,
  setPage,
  setPageLimit 
}) => {
  const [selectedSequences, setSelectedSequences] = useState([]);
  const [showSequenceDetail, setShowSequenceDetail] = useState(null);

  const handleSort = (key) => {
    const direction = 
      sortConfig.key === key && sortConfig.direction === 'asc' ? 'desc' : 'asc';
    setSortConfig(key, direction);
  };

  const handleSelectAll = () => {
    if (selectedSequences.length === data.data.length) {
      setSelectedSequences([]);
    } else {
      setSelectedSequences(data.data.map(seq => seq.id));
    }
  };

  const handleSelectSequence = (seqId) => {
    setSelectedSequences(prev => 
      prev.includes(seqId) 
        ? prev.filter(id => id !== seqId)
        : [...prev, seqId]
    );
  };

  return (
    <div className="space-y-6">
      {/* Search and Filter Bar */}
      <div className="card p-4">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-deep-400" />
            <input
              type="text"
              placeholder="Search sequences, taxa, or annotations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white focus:ring-2 focus:ring-ocean-500 focus:border-transparent"
            />
          </div>

          {/* Filter Toggle */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`btn-secondary flex items-center ${showFilters ? 'bg-ocean-100 dark:bg-ocean-900' : ''}`}
          >
            <FunnelIcon className="w-5 h-5 mr-2" />
            Filters
            {Object.values(filters).some(v => v !== null && v !== '' && v !== 0) && (
              <span className="ml-2 bg-ocean-500 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center">
                !
              </span>
            )}
          </button>

          {/* Export */}
          <button className="btn-primary flex items-center">
            <CloudArrowDownIcon className="w-5 h-5 mr-2" />
            Export ({selectedSequences.length || data.total})
          </button>
        </div>

        {/* Advanced Filters */}
        {showFilters && (
          <div className="mt-4 p-4 bg-deep-50 dark:bg-deep-800 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-deep-700 dark:text-deep-300 mb-2">
                  Novel Status
                </label>
                <select
                  value={filters.novel === null ? '' : filters.novel.toString()}
                  onChange={(e) => updateFilters({ 
                    novel: e.target.value === '' ? null : e.target.value === 'true' 
                  })}
                  className="w-full p-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-700 text-deep-900 dark:text-white"
                >
                  <option value="">All sequences</option>
                  <option value="true">Novel only</option>
                  <option value="false">Known only</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-deep-700 dark:text-deep-300 mb-2">
                  Min Confidence
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={filters.minConfidence}
                  onChange={(e) => updateFilters({ minConfidence: parseFloat(e.target.value) })}
                  className="w-full"
                />
                <span className="text-sm text-deep-600 dark:text-deep-400">
                  {(filters.minConfidence * 100).toFixed(0)}%
                </span>
              </div>

              <div>
                <label className="block text-sm font-medium text-deep-700 dark:text-deep-300 mb-2">
                  Taxon
                </label>
                <input
                  type="text"
                  placeholder="e.g., Protista, Cnidaria..."
                  value={filters.taxon}
                  onChange={(e) => updateFilters({ taxon: e.target.value })}
                  className="w-full p-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-700 text-deep-900 dark:text-white"
                />
              </div>
            </div>

            <div className="mt-4 flex justify-end">
              <button
                onClick={clearFilters}
                className="btn-secondary flex items-center"
              >
                <XMarkIcon className="w-4 h-4 mr-2" />
                Clear Filters
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Results Summary */}
      <div className="flex justify-between items-center text-sm text-deep-600 dark:text-deep-300">
        <span>
          Showing {((pagination.page - 1) * pagination.limit) + 1} to {Math.min(pagination.page * pagination.limit, data.total)} of {data.total.toLocaleString()} sequences
        </span>
        <div className="flex items-center space-x-2">
          <label>Show:</label>
          <select
            value={pagination.limit}
            onChange={(e) => setPageLimit(parseInt(e.target.value))}
            className="border border-deep-300 dark:border-deep-600 rounded px-2 py-1 bg-white dark:bg-deep-800"
          >
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
        </div>
      </div>

      {/* Data Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-deep-200 dark:divide-deep-700">
            <thead className="table-header">
              <tr>
                <th className="px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    checked={selectedSequences.length === data.data.length && data.data.length > 0}
                    onChange={handleSelectAll}
                    className="rounded border-deep-300 text-ocean-600 focus:ring-ocean-500"
                  />
                </th>
                {[
                  { key: 'id', label: 'Sequence ID' },
                  { key: 'predicted_taxon', label: 'Predicted Taxon' },
                  { key: 'confidence', label: 'Confidence' },
                  { key: 'novel', label: 'Novel' },
                  { key: 'length', label: 'Length' },
                  { key: 'quality_score', label: 'Quality' },
                  { key: 'zone_id', label: 'Zone' },
                  { key: 'actions', label: 'Actions' }
                ].map((column) => (
                  <th
                    key={column.key}
                    className="px-6 py-3 text-left cursor-pointer hover:bg-deep-100 dark:hover:bg-deep-700"
                    onClick={() => column.key !== 'actions' && handleSort(column.key)}
                  >
                    <div className="flex items-center space-x-1">
                      <span>{column.label}</span>
                      {column.key !== 'actions' && sortConfig.key === column.key && (
                        sortConfig.direction === 'asc' 
                          ? <ChevronUpIcon className="w-4 h-4" />
                          : <ChevronDownIcon className="w-4 h-4" />
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-deep-800 divide-y divide-deep-200 dark:divide-deep-700">
              {data.data.map((sequence) => (
                <tr key={sequence.id} className="hover:bg-deep-50 dark:hover:bg-deep-700">
                  <td className="px-6 py-4">
                    <input
                      type="checkbox"
                      checked={selectedSequences.includes(sequence.id)}
                      onChange={() => handleSelectSequence(sequence.id)}
                      className="rounded border-deep-300 text-ocean-600 focus:ring-ocean-500"
                    />
                  </td>
                  <td className="px-6 py-4 text-sm font-mono text-deep-900 dark:text-white">
                    {sequence.id}
                  </td>
                  <td className="px-6 py-4 text-sm text-deep-900 dark:text-white">
                    <div className="flex items-center space-x-2">
                      <span className={sequence.novel ? 'font-semibold text-purple-600 dark:text-purple-400' : ''}>
                        {sequence.predicted_taxon}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 bg-deep-200 dark:bg-deep-600 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            sequence.confidence > 0.8 ? 'bg-green-500' :
                            sequence.confidence > 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${sequence.confidence * 100}%` }}
                        />
                      </div>
                      <span className="text-deep-900 dark:text-white font-medium">
                        {(sequence.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    {sequence.novel ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-300">
                        Novel
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300">
                        Known
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm text-deep-900 dark:text-white">
                    {sequence.length} bp
                  </td>
                  <td className="px-6 py-4 text-sm text-deep-900 dark:text-white">
                    {sequence.quality_score.toFixed(1)}
                  </td>
                  <td className="px-6 py-4 text-sm font-mono text-deep-600 dark:text-deep-400">
                    {sequence.zone_id}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <button
                      onClick={() => setShowSequenceDetail(sequence)}
                      className="text-ocean-600 hover:text-ocean-800 dark:text-ocean-400 dark:hover:text-ocean-300"
                    >
                      <EyeIcon className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="bg-white dark:bg-deep-800 px-4 py-3 border-t border-deep-200 dark:border-deep-700 sm:px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setPage(pagination.page - 1)}
                disabled={!data.hasPrev}
                className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span className="text-sm text-deep-700 dark:text-deep-300">
                Page {pagination.page}
              </span>
              <button
                onClick={() => setPage(pagination.page + 1)}
                disabled={!data.hasNext}
                className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
            <div className="text-sm text-deep-500 dark:text-deep-400">
              {selectedSequences.length} selected
            </div>
          </div>
        </div>
      </div>

      {/* Sequence Detail Modal */}
      {showSequenceDetail && (
        <SequenceDetailModal 
          sequence={showSequenceDetail}
          onClose={() => setShowSequenceDetail(null)}
        />
      )}
    </div>
  );
};

const SequenceDetailModal = ({ sequence, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-deep-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white">
              Sequence Details: {sequence.id}
            </h3>
            <button
              onClick={onClose}
              className="text-deep-400 hover:text-deep-600 dark:hover:text-deep-300"
            >
              <XMarkIcon className="w-6 h-6" />
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-deep-900 dark:text-white mb-3">Classification</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">Predicted Taxon:</span>
                  <span className="font-medium text-deep-900 dark:text-white">{sequence.predicted_taxon}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">Confidence:</span>
                  <span className="font-medium text-deep-900 dark:text-white">{(sequence.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">Novel Species:</span>
                  <span className={`font-medium ${sequence.novel ? 'text-purple-600' : 'text-green-600'}`}>
                    {sequence.novel ? 'Yes' : 'No'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">Functional Role:</span>
                  <span className="font-medium text-deep-900 dark:text-white">{sequence.functional_annotation}</span>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-deep-900 dark:text-white mb-3">Sequence Properties</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">Length:</span>
                  <span className="font-medium text-deep-900 dark:text-white">{sequence.length} bp</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">Quality Score:</span>
                  <span className="font-medium text-deep-900 dark:text-white">{sequence.quality_score.toFixed(1)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">Zone:</span>
                  <span className="font-medium text-deep-900 dark:text-white">{sequence.zone_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-deep-600 dark:text-deep-300">GC Content:</span>
                  <span className="font-medium text-deep-900 dark:text-white">{sequence.analysis_metadata.gc_content.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h4 className="font-medium text-deep-900 dark:text-white mb-3">Sample Metadata</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-deep-600 dark:text-deep-300">Location:</span>
                <p className="font-medium text-deep-900 dark:text-white">{sequence.metadata.sample_location}</p>
              </div>
              <div>
                <span className="text-deep-600 dark:text-deep-300">Depth:</span>
                <p className="font-medium text-deep-900 dark:text-white">{sequence.metadata.depth_m}m</p>
              </div>
              <div>
                <span className="text-deep-600 dark:text-deep-300">Temperature:</span>
                <p className="font-medium text-deep-900 dark:text-white">{sequence.metadata.temperature_c}°C</p>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h4 className="font-medium text-deep-900 dark:text-white mb-3">Sequence Data</h4>
            <div className="bg-deep-50 dark:bg-deep-900 p-4 rounded-lg">
              <code className="text-sm font-mono text-deep-900 dark:text-white break-all">
                {sequence.sequence_data}
              </code>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SequenceTable;
