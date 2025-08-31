import { useState } from 'react';
import { 
  CloudArrowDownIcon, 
  DocumentArrowDownIcon, 
  TableCellsIcon,
  DocumentTextIcon,
  PhotoIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';
import mockData from '../data/index.js';

const DownloadExport = ({ sequences, currentSearch }) => {
  const [downloadFormat, setDownloadFormat] = useState('csv');
  const [includeMetadata, setIncludeMetadata] = useState(true);
  const [includeNovelty, setIncludeNovelty] = useState(true);
  const [isDownloading, setIsDownloading] = useState(false);

  const downloadOptions = [
    {
      id: 'csv',
      name: 'CSV File',
      description: 'Spreadsheet format for Excel/Google Sheets',
      icon: TableCellsIcon,
      extension: '.csv'
    },
    {
      id: 'json',
      name: 'JSON File',
      description: 'Structured data for programming/analysis',
      icon: DocumentTextIcon,
      extension: '.json'
    },
    {
      id: 'fasta',
      name: 'FASTA File',
      description: 'Sequence data in FASTA format',
      icon: DocumentArrowDownIcon,
      extension: '.fasta'
    },
    {
      id: 'report',
      name: 'Analysis Report',
      description: 'Complete PDF report with visualizations',
      icon: PhotoIcon,
      extension: '.pdf'
    }
  ];

  const generateCSV = (data) => {
    const headers = [
      'Sequence_ID',
      'Predicted_Taxon',
      'Confidence',
      'Novelty_Flag',
      'Functional_Role',
      'Zone_ID',
      'Similarity_Score'
    ];

    if (includeMetadata) {
      headers.push('Search_Time_ms', 'Algorithm_Used', 'Reference_Database');
    }

    const csvContent = [
      headers.join(','),
      ...data.map(seq => [
        seq.id,
        `"${seq.taxon}"`,
        seq.confidence,
        seq.novelty_flag ? 'TRUE' : 'FALSE',
        seq.functional_role || 'Unknown',
        seq.zone_id || 'N/A',
        seq.similarity_score || 'N/A',
        ...(includeMetadata ? [
          seq.search_time_ms || 'N/A',
          'ZHNSW',
          'Marine_eDNA_DB_v2.1'
        ] : [])
      ].join(','))
    ].join('\n');

    return csvContent;
  };

  const generateJSON = (data) => {
    const exportData = {
      metadata: {
        export_date: new Date().toISOString(),
        total_sequences: data.length,
        novel_sequences: data.filter(seq => seq.novelty_flag).length,
        algorithm: 'ZHNSW',
        database_version: 'Marine_eDNA_DB_v2.1',
        confidence_threshold: 0.5
      },
      search_parameters: currentSearch ? {
        query_id: currentSearch.query_sequence.id,
        zones_searched: currentSearch.zhnsw_process.step2_zone_selection.zones_selected,
        total_search_time: currentSearch.performance_metrics.total_zhnsw_time_ms
      } : null,
      sequences: data.map(seq => ({
        id: seq.id,
        taxon: seq.taxon,
        confidence: seq.confidence,
        novelty_flag: seq.novelty_flag,
        functional_role: seq.functional_role,
        zone_id: seq.zone_id,
        similarity_score: seq.similarity_score,
        ...(includeMetadata && {
          metadata: {
            search_time_ms: seq.search_time_ms,
            algorithm: 'ZHNSW',
            reference_db: 'Marine_eDNA_DB_v2.1'
          }
        })
      }))
    };

    return JSON.stringify(exportData, null, 2);
  };

  const generateFASTA = (data) => {
    return data.map(seq => 
      `>${seq.id}|${seq.taxon}|confidence:${seq.confidence}|novel:${seq.novelty_flag}\n` +
      `${seq.sequence_fragment || 'ATCGATCGATCGATCGATCGATCG'}`
    ).join('\n\n');
  };

  const downloadFile = async (content, filename, type = 'text/plain') => {
    setIsDownloading(true);
    
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    setIsDownloading(false);
  };

  const handleDownload = async () => {
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const baseFilename = `edna_analysis_${timestamp}`;
    
    const data = sequences || mockData.sequences.slice(0, 1000);
    
    switch (downloadFormat) {
      case 'csv':
        await downloadFile(
          generateCSV(data),
          `${baseFilename}.csv`,
          'text/csv'
        );
        break;
      case 'json':
        await downloadFile(
          generateJSON(data),
          `${baseFilename}.json`,
          'application/json'
        );
        break;
      case 'fasta':
        await downloadFile(
          generateFASTA(data),
          `${baseFilename}.fasta`,
          'text/plain'
        );
        break;
      case 'report':
        // Simulate PDF generation
        await downloadFile(
          'PDF Report Generation - This would contain comprehensive analysis report with charts and visualizations',
          `${baseFilename}_report.pdf`,
          'application/pdf'
        );
        break;
    }
  };

  const dataStats = {
    totalSequences: sequences ? sequences.length : mockData.sequences.length,
    novelSequences: sequences 
      ? sequences.filter(seq => seq.novelty_flag).length 
      : mockData.sequences.filter(seq => seq.novelty_flag).length,
    avgConfidence: sequences
      ? sequences.reduce((sum, seq) => sum + seq.confidence, 0) / sequences.length
      : mockData.sequences.reduce((sum, seq) => sum + seq.confidence, 0) / mockData.sequences.length
  };

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-deep-900 dark:text-white">
            Download & Export Data
          </h3>
          <div className="flex items-center space-x-2">
            <CloudArrowDownIcon className="w-5 h-5 text-deep-600 dark:text-deep-300" />
            <span className="text-sm text-deep-600 dark:text-deep-300">
              Export Analysis Results
            </span>
          </div>
        </div>

        {/* Export Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-deep-50 dark:bg-deep-800 p-4 rounded-lg">
            <div className="text-sm text-deep-600 dark:text-deep-300">Total Sequences</div>
            <div className="text-2xl font-semibold text-deep-900 dark:text-white">
              {dataStats.totalSequences.toLocaleString()}
            </div>
          </div>
          <div className="bg-amber-50 dark:bg-amber-900/20 p-4 rounded-lg">
            <div className="text-sm text-amber-700 dark:text-amber-300">Novel Species</div>
            <div className="text-2xl font-semibold text-amber-900 dark:text-amber-100">
              {dataStats.novelSequences.toLocaleString()}
            </div>
          </div>
          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <div className="text-sm text-green-700 dark:text-green-300">Avg Confidence</div>
            <div className="text-2xl font-semibold text-green-900 dark:text-green-100">
              {(dataStats.avgConfidence * 100).toFixed(1)}%
            </div>
          </div>
        </div>

        {/* Format Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-deep-700 dark:text-deep-300 mb-3">
            Export Format
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {downloadOptions.map(option => (
              <label
                key={option.id}
                className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                  downloadFormat === option.id
                    ? 'border-ocean-500 bg-ocean-50 dark:bg-ocean-900/20'
                    : 'border-deep-200 dark:border-deep-600 hover:border-deep-300 dark:hover:border-deep-500'
                }`}
              >
                <input
                  type="radio"
                  name="downloadFormat"
                  value={option.id}
                  checked={downloadFormat === option.id}
                  onChange={(e) => setDownloadFormat(e.target.value)}
                  className="sr-only"
                />
                <option.icon className={`w-6 h-6 mr-3 ${
                  downloadFormat === option.id 
                    ? 'text-ocean-600 dark:text-ocean-400' 
                    : 'text-deep-600 dark:text-deep-300'
                }`} />
                <div>
                  <div className={`font-medium ${
                    downloadFormat === option.id 
                      ? 'text-ocean-900 dark:text-ocean-100' 
                      : 'text-deep-900 dark:text-white'
                  }`}>
                    {option.name}
                  </div>
                  <div className="text-sm text-deep-600 dark:text-deep-400">
                    {option.description}
                  </div>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Export Options */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-deep-700 dark:text-deep-300 mb-3">
            Export Options
          </label>
          <div className="space-y-3">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={includeMetadata}
                onChange={(e) => setIncludeMetadata(e.target.checked)}
                className="rounded border-deep-300 dark:border-deep-600 text-ocean-600 focus:ring-ocean-500 dark:bg-deep-800"
              />
              <span className="ml-2 text-deep-700 dark:text-deep-300">
                Include metadata (search times, algorithms, database versions)
              </span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={includeNovelty}
                onChange={(e) => setIncludeNovelty(e.target.checked)}
                className="rounded border-deep-300 dark:border-deep-600 text-ocean-600 focus:ring-ocean-500 dark:bg-deep-800"
              />
              <span className="ml-2 text-deep-700 dark:text-deep-300">
                Include novelty detection results and confidence scores
              </span>
            </label>
          </div>
        </div>

        {/* Download Button */}
        <div className="flex items-center justify-between">
          <div className="text-sm text-deep-600 dark:text-deep-300">
            File will be downloaded as: <span className="font-mono">
              edna_analysis_[timestamp]{downloadOptions.find(opt => opt.id === downloadFormat)?.extension}
            </span>
          </div>
          <button
            onClick={handleDownload}
            disabled={isDownloading}
            className={`btn-primary flex items-center ${
              isDownloading ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            {isDownloading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Processing...
              </>
            ) : (
              <>
                <CloudArrowDownIcon className="w-5 h-5 mr-2" />
                Download {downloadOptions.find(opt => opt.id === downloadFormat)?.name}
              </>
            )}
          </button>
        </div>
      </div>

      {/* Quick Export Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <QuickExportCard
          title="Research Publication"
          description="CSV format with metadata for research papers"
          icon={TableCellsIcon}
          onClick={() => {
            setDownloadFormat('csv');
            setIncludeMetadata(true);
            handleDownload();
          }}
          disabled={isDownloading}
        />
        <QuickExportCard
          title="Bioinformatics Pipeline"
          description="JSON format for computational analysis"
          icon={DocumentTextIcon}
          onClick={() => {
            setDownloadFormat('json');
            setIncludeMetadata(true);
            handleDownload();
          }}
          disabled={isDownloading}
        />
        <QuickExportCard
          title="Sequence Database"
          description="FASTA format for sequence alignment"
          icon={DocumentArrowDownIcon}
          onClick={() => {
            setDownloadFormat('fasta');
            handleDownload();
          }}
          disabled={isDownloading}
        />
      </div>
    </div>
  );
};

const QuickExportCard = ({ title, description, icon: Icon, onClick, disabled }) => {
  return (
    <div className="card p-4 hover:shadow-md transition-shadow">
      <button
        onClick={onClick}
        disabled={disabled}
        className={`w-full text-left ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <div className="flex items-center mb-3">
          <Icon className="w-6 h-6 text-ocean-600 dark:text-ocean-400 mr-3" />
          <h4 className="font-medium text-deep-900 dark:text-white">{title}</h4>
        </div>
        <p className="text-sm text-deep-600 dark:text-deep-300">{description}</p>
        <div className="mt-3 flex items-center text-sm text-ocean-600 dark:text-ocean-400">
          <CloudArrowDownIcon className="w-4 h-4 mr-1" />
          Quick Export
        </div>
      </button>
    </div>
  );
};

export default DownloadExport;
