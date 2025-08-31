import { useState, useMemo } from 'react';
import { 
  ChevronRightIcon, 
  ChevronDownIcon, 
  BeakerIcon,
  ChartBarIcon,
  MagnifyingGlassIcon,
  FunnelIcon
} from '@heroicons/react/24/outline';
import mockData from '../data/index.js';

const TaxonomyTreeBrowser = () => {
  const [expandedNodes, setExpandedNodes] = useState(new Set(['root']));
  const [selectedTaxon, setSelectedTaxon] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterMode, setFilterMode] = useState('all'); // all, novel, high_confidence

  // Build hierarchical taxonomy tree from sequences
  const taxonomyTree = useMemo(() => {
    const tree = { root: { name: 'All Taxa', children: {}, count: 0, level: 0 } };
    
    mockData.sequences.forEach(seq => {
      if (searchQuery && !seq.predicted_taxon.toLowerCase().includes(searchQuery.toLowerCase())) {
        return;
      }
      
      if (filterMode === 'novel' && !seq.novel) return;
      if (filterMode === 'high_confidence' && seq.confidence < 0.8) return;
      
      const parts = seq.predicted_taxon.split(' ');
      let current = tree.root;
      current.count++;
      
      // Build hierarchy: Kingdom > Phylum > Class > Order > Family > Genus > Species
      const taxonomyLevels = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'];
      
      for (let i = 0; i < Math.min(parts.length, taxonomyLevels.length); i++) {
        const part = parts[i];
        if (!current.children[part]) {
          current.children[part] = {
            name: part,
            level: taxonomyLevels[i],
            children: {},
            count: 0,
            sequences: [],
            avgConfidence: 0,
            novelCount: 0
          };
        }
        current.children[part].count++;
        current.children[part].sequences.push(seq);
        if (seq.novel) current.children[part].novelCount++;
        current = current.children[part];
      }
    });
    
    // Calculate average confidence for each node
    const calculateAvgConfidence = (node) => {
      if (node.sequences && node.sequences.length > 0) {
        node.avgConfidence = node.sequences.reduce((sum, seq) => sum + seq.confidence, 0) / node.sequences.length;
      }
      Object.values(node.children).forEach(calculateAvgConfidence);
    };
    
    calculateAvgConfidence(tree.root);
    return tree;
  }, [searchQuery, filterMode]);

  const toggleNode = (nodeId) => {
    const newExpanded = new Set(expandedNodes);
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId);
    } else {
      newExpanded.add(nodeId);
    }
    setExpandedNodes(newExpanded);
  };

  const renderTreeNode = (node, path = '', depth = 0) => {
    const nodeId = path || 'root';
    const isExpanded = expandedNodes.has(nodeId);
    const hasChildren = Object.keys(node.children).length > 0;
    const isSelected = selectedTaxon === nodeId;

    return (
      <div key={nodeId} className="select-none">
        <div 
          className={`flex items-center py-2 px-2 rounded cursor-pointer transition-colors ${
            isSelected 
              ? 'bg-ocean-100 dark:bg-ocean-900/50 border-l-4 border-ocean-600' 
              : 'hover:bg-deep-100 dark:hover:bg-deep-700'
          }`}
          style={{ paddingLeft: `${depth * 20 + 8}px` }}
          onClick={() => setSelectedTaxon(nodeId)}
        >
          <div className="flex items-center flex-1">
            {hasChildren && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  toggleNode(nodeId);
                }}
                className="mr-2 text-deep-500 dark:text-deep-400 hover:text-deep-700 dark:hover:text-deep-200"
              >
                {isExpanded ? (
                  <ChevronDownIcon className="w-4 h-4" />
                ) : (
                  <ChevronRightIcon className="w-4 h-4" />
                )}
              </button>
            )}
            {!hasChildren && <div className="w-6 mr-2" />}
            
            <div className="flex items-center flex-1">
              <span className="font-medium text-deep-900 dark:text-white mr-2">
                {node.name}
              </span>
              {node.level && depth > 0 && (
                <span className="text-xs px-2 py-1 bg-deep-200 dark:bg-deep-700 rounded text-deep-600 dark:text-deep-300 mr-2">
                  {node.level}
                </span>
              )}
              <span className="text-sm text-deep-600 dark:text-deep-300">
                ({node.count})
              </span>
              {node.novelCount > 0 && (
                <span className="ml-2 text-xs px-2 py-1 bg-amber-100 dark:bg-amber-900/50 text-amber-800 dark:text-amber-200 rounded">
                  {node.novelCount} novel
                </span>
              )}
            </div>
            
            {node.avgConfidence > 0 && (
              <div className="ml-auto flex items-center">
                <div className="w-16 bg-deep-200 dark:bg-deep-700 rounded-full h-2 mr-2">
                  <div 
                    className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-2 rounded-full"
                    style={{ width: `${node.avgConfidence * 100}%` }}
                  />
                </div>
                <span className="text-xs text-deep-600 dark:text-deep-300 w-8">
                  {(node.avgConfidence * 100).toFixed(0)}%
                </span>
              </div>
            )}
          </div>
        </div>
        
        {isExpanded && hasChildren && (
          <div>
            {Object.entries(node.children)
              .sort(([,a], [,b]) => b.count - a.count)
              .map(([key, child]) => 
                renderTreeNode(child, path ? `${path}.${key}` : key, depth + 1)
              )}
          </div>
        )}
      </div>
    );
  };

  const selectedNode = useMemo(() => {
    if (!selectedTaxon) return null;
    
    const findNode = (node, path, target) => {
      if (path === target) return node;
      for (const [key, child] of Object.entries(node.children)) {
        const childPath = path ? `${path}.${key}` : key;
        const result = findNode(child, childPath, target);
        if (result) return result;
      }
      return null;
    };
    
    return findNode(taxonomyTree.root, '', selectedTaxon);
  }, [selectedTaxon, taxonomyTree]);

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-deep-900 dark:text-white">
            Taxonomic Tree Browser
          </h3>
          <div className="flex items-center space-x-2">
            <select
              value={filterMode}
              onChange={(e) => setFilterMode(e.target.value)}
              className="px-3 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white"
            >
              <option value="all">All Taxa</option>
              <option value="novel">Novel Only</option>
              <option value="high_confidence">High Confidence</option>
            </select>
          </div>
        </div>
        
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-3 h-5 w-5 text-deep-400" />
          <input
            type="text"
            placeholder="Search taxonomy..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white placeholder-deep-500 dark:placeholder-deep-400"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tree View */}
        <div className="lg:col-span-2">
          <div className="card p-4 max-h-[600px] overflow-y-auto">
            <h4 className="font-medium text-deep-900 dark:text-white mb-4">
              Hierarchical Taxonomy
            </h4>
            {renderTreeNode(taxonomyTree.root)}
          </div>
        </div>

        {/* Details Panel */}
        <div className="space-y-6">
          {selectedNode && <TaxonDetailsPanel node={selectedNode} />}
          <TaxonomyStatsPanel tree={taxonomyTree} />
        </div>
      </div>
    </div>
  );
};

const TaxonDetailsPanel = ({ node }) => {
  const [activeTab, setActiveTab] = useState('overview');
  
  const tabs = [
    { id: 'overview', name: 'Overview' },
    { id: 'sequences', name: 'Sequences' },
    { id: 'distribution', name: 'Distribution' }
  ];

  return (
    <div className="card p-6">
      <h4 className="font-medium text-deep-900 dark:text-white mb-4">
        {node.name}
      </h4>
      
      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-4">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
              activeTab === tab.id
                ? 'bg-ocean-600 text-white'
                : 'text-deep-600 dark:text-deep-300 hover:bg-deep-100 dark:hover:bg-deep-700'
            }`}
          >
            {tab.name}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
              <div className="text-sm text-deep-600 dark:text-deep-300">Total Sequences</div>
              <div className="text-xl font-semibold text-deep-900 dark:text-white">
                {node.count}
              </div>
            </div>
            <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
              <div className="text-sm text-deep-600 dark:text-deep-300">Avg Confidence</div>
              <div className="text-xl font-semibold text-deep-900 dark:text-white">
                {(node.avgConfidence * 100).toFixed(1)}%
              </div>
            </div>
            {node.novelCount > 0 && (
              <div className="bg-amber-50 dark:bg-amber-900/20 p-3 rounded">
                <div className="text-sm text-amber-700 dark:text-amber-300">Novel Species</div>
                <div className="text-xl font-semibold text-amber-900 dark:text-amber-100">
                  {node.novelCount}
                </div>
              </div>
            )}
            <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
              <div className="text-sm text-deep-600 dark:text-deep-300">Taxonomic Level</div>
              <div className="text-xl font-semibold text-deep-900 dark:text-white">
                {node.level || 'Root'}
              </div>
            </div>
          </div>
          
          {Object.keys(node.children).length > 0 && (
            <div>
              <h5 className="font-medium text-deep-900 dark:text-white mb-2">
                Child Taxa ({Object.keys(node.children).length})
              </h5>
              <div className="space-y-1 max-h-32 overflow-y-auto">
                {Object.entries(node.children)
                  .sort(([,a], [,b]) => b.count - a.count)
                  .slice(0, 10)
                  .map(([name, child]) => (
                    <div key={name} className="flex justify-between text-sm">
                      <span className="text-deep-900 dark:text-white">{name}</span>
                      <span className="text-deep-600 dark:text-deep-300">{child.count}</span>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'sequences' && (
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {node.sequences?.slice(0, 20).map(seq => (
            <div key={seq.id} className="p-2 bg-deep-50 dark:bg-deep-800 rounded text-sm">
              <div className="flex justify-between items-center">
                <span className="font-mono text-deep-900 dark:text-white">{seq.id}</span>
                <div className="flex items-center space-x-2">
                  <span className="text-deep-600 dark:text-deep-300">
                    {(seq.confidence * 100).toFixed(1)}%
                  </span>
                  {seq.novel && (
                    <span className="px-2 py-1 bg-amber-100 dark:bg-amber-900/50 text-amber-800 dark:text-amber-200 rounded text-xs">
                      Novel
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'distribution' && (
        <div className="space-y-4">
          <div className="text-sm text-deep-600 dark:text-deep-300">
            Zone distribution analysis would be displayed here, showing which zones contain this taxon.
          </div>
        </div>
      )}
    </div>
  );
};

const TaxonomyStatsPanel = ({ tree }) => {
  const stats = useMemo(() => {
    const calculateStats = (node, depth = 0) => {
      let totalNodes = 1;
      let maxDepth = depth;
      let leafNodes = Object.keys(node.children).length === 0 ? 1 : 0;
      let totalSequences = node.count || 0;
      let novelSequences = node.novelCount || 0;
      
      Object.values(node.children).forEach(child => {
        const childStats = calculateStats(child, depth + 1);
        totalNodes += childStats.totalNodes;
        maxDepth = Math.max(maxDepth, childStats.maxDepth);
        leafNodes += childStats.leafNodes;
      });
      
      return { totalNodes, maxDepth, leafNodes, totalSequences, novelSequences };
    };
    
    return calculateStats(tree.root);
  }, [tree]);

  return (
    <div className="card p-6">
      <h4 className="font-medium text-deep-900 dark:text-white mb-4">
        Taxonomy Statistics
      </h4>
      
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Total Taxa:</span>
          <span className="font-semibold text-deep-900 dark:text-white">{stats.totalNodes}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Max Depth:</span>
          <span className="font-semibold text-deep-900 dark:text-white">{stats.maxDepth}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Leaf Taxa:</span>
          <span className="font-semibold text-deep-900 dark:text-white">{stats.leafNodes}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Total Sequences:</span>
          <span className="font-semibold text-deep-900 dark:text-white">{stats.totalSequences}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Novel Sequences:</span>
          <span className="font-semibold text-amber-600 dark:text-amber-400">{stats.novelSequences}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-deep-600 dark:text-deep-300">Novelty Rate:</span>
          <span className="font-semibold text-amber-600 dark:text-amber-400">
            {((stats.novelSequences / stats.totalSequences) * 100).toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default TaxonomyTreeBrowser;
