import { useState, useEffect } from 'react';
import { 
  CogIcon, 
  MoonIcon, 
  SunIcon, 
  BeakerIcon,
  ChartBarIcon,
  CircleStackIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';

const SettingsConfiguration = () => {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true' || 
           (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });
  
  const [settings, setSettings] = useState({
    // Analysis Settings
    confidenceThreshold: 0.7,
    noveltyThreshold: 0.8,
    maxResults: 1000,
    enableZHNSW: true,
    parallelProcessing: true,
    
    // Display Settings
    resultsPerPage: 25,
    showConfidenceMeters: true,
    showNoveltyFlags: true,
    autoRefresh: false,
    
    // Export Settings
    defaultExportFormat: 'csv',
    includeMetadata: true,
    compressExports: false,
    
    // Performance Settings
    cacheResults: true,
    preloadZones: true,
    enableAnimations: true
  });

  useEffect(() => {
    // Apply dark mode
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('darkMode', darkMode.toString());
  }, [darkMode]);

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    // In a real app, this would save to backend or localStorage
    localStorage.setItem(`setting_${key}`, JSON.stringify(value));
  };

  const resetToDefaults = () => {
    const defaultSettings = {
      confidenceThreshold: 0.7,
      noveltyThreshold: 0.8,
      maxResults: 1000,
      enableZHNSW: true,
      parallelProcessing: true,
      resultsPerPage: 25,
      showConfidenceMeters: true,
      showNoveltyFlags: true,
      autoRefresh: false,
      defaultExportFormat: 'csv',
      includeMetadata: true,
      compressExports: false,
      cacheResults: true,
      preloadZones: true,
      enableAnimations: true
    };
    setSettings(defaultSettings);
    
    // Clear localStorage
    Object.keys(defaultSettings).forEach(key => {
      localStorage.removeItem(`setting_${key}`);
    });
  };

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-deep-900 dark:text-white flex items-center">
            <CogIcon className="w-6 h-6 mr-2" />
            Settings & Configuration
          </h3>
          <button
            onClick={resetToDefaults}
            className="btn-secondary text-sm"
          >
            Reset to Defaults
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Analysis Settings */}
          <div>
            <h4 className="font-medium text-deep-900 dark:text-white mb-4 flex items-center">
              <BeakerIcon className="w-5 h-5 mr-2" />
              Analysis Settings
            </h4>
            <div className="space-y-4">
              <SettingSlider
                label="Confidence Threshold"
                description="Minimum confidence score for sequence classification"
                value={settings.confidenceThreshold}
                min={0}
                max={1}
                step={0.1}
                onChange={(value) => updateSetting('confidenceThreshold', value)}
                suffix="%"
                displayValue={(v) => (v * 100).toFixed(0)}
              />
              
              <SettingSlider
                label="Novelty Detection Threshold"
                description="Sensitivity for detecting novel species"
                value={settings.noveltyThreshold}
                min={0}
                max={1}
                step={0.1}
                onChange={(value) => updateSetting('noveltyThreshold', value)}
                suffix="%"
                displayValue={(v) => (v * 100).toFixed(0)}
              />
              
              <SettingSlider
                label="Maximum Results"
                description="Maximum number of results to display"
                value={settings.maxResults}
                min={100}
                max={10000}
                step={100}
                onChange={(value) => updateSetting('maxResults', value)}
                displayValue={(v) => v.toLocaleString()}
              />
              
              <SettingToggle
                label="Enable ZHNSW Algorithm"
                description="Use zone-based hierarchical search for faster results"
                checked={settings.enableZHNSW}
                onChange={(checked) => updateSetting('enableZHNSW', checked)}
              />
              
              <SettingToggle
                label="Parallel Processing"
                description="Process multiple zones simultaneously"
                checked={settings.parallelProcessing}
                onChange={(checked) => updateSetting('parallelProcessing', checked)}
              />
            </div>
          </div>

          {/* Display Settings */}
          <div>
            <h4 className="font-medium text-deep-900 dark:text-white mb-4 flex items-center">
              <ChartBarIcon className="w-5 h-5 mr-2" />
              Display Settings
            </h4>
            <div className="space-y-4">
              <SettingSelect
                label="Results Per Page"
                description="Number of sequences to show per page"
                value={settings.resultsPerPage}
                options={[
                  { value: 10, label: '10 per page' },
                  { value: 25, label: '25 per page' },
                  { value: 50, label: '50 per page' },
                  { value: 100, label: '100 per page' }
                ]}
                onChange={(value) => updateSetting('resultsPerPage', parseInt(value))}
              />
              
              <SettingToggle
                label="Show Confidence Meters"
                description="Display visual confidence indicators"
                checked={settings.showConfidenceMeters}
                onChange={(checked) => updateSetting('showConfidenceMeters', checked)}
              />
              
              <SettingToggle
                label="Show Novelty Flags"
                description="Highlight novel species discoveries"
                checked={settings.showNoveltyFlags}
                onChange={(checked) => updateSetting('showNoveltyFlags', checked)}
              />
              
              <SettingToggle
                label="Auto Refresh"
                description="Automatically refresh results every 30 seconds"
                checked={settings.autoRefresh}
                onChange={(checked) => updateSetting('autoRefresh', checked)}
              />
              
              <div className="pt-2">
                <DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Advanced Settings */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Export Settings */}
        <div className="card p-6">
          <h4 className="font-medium text-deep-900 dark:text-white mb-4 flex items-center">
            <CircleStackIcon className="w-5 h-5 mr-2" />
            Export Settings
          </h4>
          <div className="space-y-4">
            <SettingSelect
              label="Default Export Format"
              description="Preferred format for data exports"
              value={settings.defaultExportFormat}
              options={[
                { value: 'csv', label: 'CSV (Spreadsheet)' },
                { value: 'json', label: 'JSON (Structured)' },
                { value: 'fasta', label: 'FASTA (Sequences)' },
                { value: 'report', label: 'PDF Report' }
              ]}
              onChange={(value) => updateSetting('defaultExportFormat', value)}
            />
            
            <SettingToggle
              label="Include Metadata"
              description="Add search parameters and algorithm info to exports"
              checked={settings.includeMetadata}
              onChange={(checked) => updateSetting('includeMetadata', checked)}
            />
            
            <SettingToggle
              label="Compress Large Exports"
              description="Automatically compress files larger than 10MB"
              checked={settings.compressExports}
              onChange={(checked) => updateSetting('compressExports', checked)}
            />
          </div>
        </div>

        {/* Performance Settings */}
        <div className="card p-6">
          <h4 className="font-medium text-deep-900 dark:text-white mb-4 flex items-center">
            <ShieldCheckIcon className="w-5 h-5 mr-2" />
            Performance Settings
          </h4>
          <div className="space-y-4">
            <SettingToggle
              label="Cache Results"
              description="Store search results for faster retrieval"
              checked={settings.cacheResults}
              onChange={(checked) => updateSetting('cacheResults', checked)}
            />
            
            <SettingToggle
              label="Preload Zone Data"
              description="Load zone information in background"
              checked={settings.preloadZones}
              onChange={(checked) => updateSetting('preloadZones', checked)}
            />
            
            <SettingToggle
              label="Enable Animations"
              description="Show smooth transitions and loading animations"
              checked={settings.enableAnimations}
              onChange={(checked) => updateSetting('enableAnimations', checked)}
            />
          </div>
        </div>
      </div>

      {/* System Information */}
      <SystemInformation settings={settings} />
    </div>
  );
};

const SettingSlider = ({ label, description, value, min, max, step, onChange, suffix = '', displayValue }) => {
  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        <label className="text-sm font-medium text-deep-700 dark:text-deep-300">
          {label}
        </label>
        <span className="text-sm font-semibold text-deep-900 dark:text-white">
          {displayValue ? displayValue(value) : value}{suffix}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-2 bg-deep-200 dark:bg-deep-700 rounded-lg appearance-none cursor-pointer"
      />
      <p className="text-xs text-deep-600 dark:text-deep-400 mt-1">{description}</p>
    </div>
  );
};

const SettingToggle = ({ label, description, checked, onChange }) => {
  return (
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <label className="text-sm font-medium text-deep-700 dark:text-deep-300 block">
          {label}
        </label>
        <p className="text-xs text-deep-600 dark:text-deep-400">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          checked ? 'bg-ocean-600' : 'bg-deep-300 dark:bg-deep-600'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
            checked ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    </div>
  );
};

const SettingSelect = ({ label, description, value, options, onChange }) => {
  return (
    <div>
      <label className="text-sm font-medium text-deep-700 dark:text-deep-300 block mb-2">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 border border-deep-300 dark:border-deep-600 rounded-lg bg-white dark:bg-deep-800 text-deep-900 dark:text-white"
      >
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <p className="text-xs text-deep-600 dark:text-deep-400 mt-1">{description}</p>
    </div>
  );
};

const DarkModeToggle = ({ darkMode, setDarkMode }) => {
  return (
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <label className="text-sm font-medium text-deep-700 dark:text-deep-300 block">
          Dark Mode
        </label>
        <p className="text-xs text-deep-600 dark:text-deep-400">Toggle between light and dark themes</p>
      </div>
      <button
        onClick={() => setDarkMode(!darkMode)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          darkMode ? 'bg-deep-600' : 'bg-yellow-400'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform flex items-center justify-center ${
            darkMode ? 'translate-x-6' : 'translate-x-1'
          }`}
        >
          {darkMode ? (
            <MoonIcon className="w-3 h-3 text-deep-600" />
          ) : (
            <SunIcon className="w-3 h-3 text-yellow-600" />
          )}
        </span>
      </button>
    </div>
  );
};

const SystemInformation = ({ settings }) => {
  const systemStats = {
    version: '2.1.0-beta',
    database: 'Marine_eDNA_DB_v2.1',
    algorithm: 'ZHNSW-Enhanced',
    zones: 64,
    sequences: '256,847',
    lastUpdate: '2025-08-31',
    uptime: '99.7%'
  };

  return (
    <div className="card p-6">
      <h4 className="font-medium text-deep-900 dark:text-white mb-4">
        System Information
      </h4>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
          <div className="text-sm text-deep-600 dark:text-deep-300">Platform Version</div>
          <div className="font-semibold text-deep-900 dark:text-white">{systemStats.version}</div>
        </div>
        <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
          <div className="text-sm text-deep-600 dark:text-deep-300">Database</div>
          <div className="font-semibold text-deep-900 dark:text-white">{systemStats.database}</div>
        </div>
        <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
          <div className="text-sm text-deep-600 dark:text-deep-300">Algorithm</div>
          <div className="font-semibold text-deep-900 dark:text-white">{systemStats.algorithm}</div>
        </div>
        <div className="bg-deep-50 dark:bg-deep-800 p-3 rounded">
          <div className="text-sm text-deep-600 dark:text-deep-300">System Uptime</div>
          <div className="font-semibold text-green-600">{systemStats.uptime}</div>
        </div>
      </div>
      
      <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
        <div className="text-sm text-blue-800 dark:text-blue-200">
          <strong>Current Configuration:</strong> ZHNSW {settings.enableZHNSW ? 'Enabled' : 'Disabled'}, 
          Confidence Threshold: {(settings.confidenceThreshold * 100).toFixed(0)}%, 
          Max Results: {settings.maxResults.toLocaleString()}, 
          Parallel Processing: {settings.parallelProcessing ? 'On' : 'Off'}
        </div>
      </div>
    </div>
  );
};

export default SettingsConfiguration;
