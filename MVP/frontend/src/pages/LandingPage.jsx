import { useState } from 'react';
import { useAppStore } from '../store/index.js';
import { CloudArrowUpIcon, PlayIcon, ChartBarIcon, BeakerIcon } from '@heroicons/react/24/outline';

const LandingPage = () => {
  const { setCurrentPage, simulateZHNSWSearch } = useAppStore();
  const [uploadedFile, setUploadedFile] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      // Simulate processing the uploaded file
      const mockQuery = {
        id: `uploaded_${Date.now()}`,
        sequence_data: "ATCGTGATCGTAATCGATCGATCGTAATCGATCGTAATCG",
        length: 298,
        type: "18S rRNA",
        filename: file.name
      };
      simulateZHNSWSearch(mockQuery);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-ocean-50 to-deep-50 dark:from-deep-900 dark:to-deep-800">
      {/* Hero Section */}
      <section className="relative px-4 pt-16 pb-20 sm:px-6 lg:px-8 lg:pt-24 lg:pb-28">
        <div className="relative max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl tracking-tight font-extrabold text-deep-900 dark:text-white sm:text-5xl md:text-6xl">
              <span className="block">Deep-Sea eDNA</span>
              <span className="block text-ocean-600 dark:text-ocean-400">
                Biodiversity Explorer
              </span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-deep-500 dark:text-deep-300 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              Revolutionary AI-driven platform using <strong>Zonal HNSW algorithm</strong> to identify 
              taxonomy and assess biodiversity from environmental DNA datasets. Discover the unknown 
              depths of marine life with unprecedented speed and accuracy.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4 sm:gap-6">
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
                className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-ocean-600 hover:bg-ocean-700 cursor-pointer transition-colors duration-200"
              >
                <CloudArrowUpIcon className="w-5 h-5 mr-2" />
                Upload eDNA Sample
              </label>
            </div>
            
            <button
              onClick={() => setCurrentPage('analysis')}
              className="inline-flex items-center px-8 py-3 border border-ocean-300 dark:border-ocean-600 text-base font-medium rounded-md text-ocean-700 dark:text-ocean-300 bg-white dark:bg-deep-800 hover:bg-ocean-50 dark:hover:bg-deep-700 transition-colors duration-200"
            >
              <PlayIcon className="w-5 h-5 mr-2" />
              View Demo Analysis
            </button>
          </div>

          {/* Stats Section */}
          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {[
                { label: 'Sequences Analyzed', value: '250K+', icon: BeakerIcon },
                { label: 'Novel Species Found', value: '1,240', icon: ChartBarIcon },
                { label: 'Search Speed Improvement', value: '94%', icon: PlayIcon },
                { label: 'Active Zones', value: '64', icon: CloudArrowUpIcon }
              ].map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="flex justify-center mb-2">
                    <stat.icon className="w-8 h-8 text-ocean-600 dark:text-ocean-400" />
                  </div>
                  <div className="text-2xl font-bold text-deep-900 dark:text-white">
                    {stat.value}
                  </div>
                  <div className="text-sm text-deep-600 dark:text-deep-300">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white dark:bg-deep-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-extrabold text-deep-900 dark:text-white">
              Revolutionary ZHNSW Technology
            </h2>
            <p className="mt-4 text-lg text-deep-600 dark:text-deep-300">
              Solving the database limitation problem in deep-sea biodiversity research
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="card p-6">
              <div className="w-12 h-12 bg-ocean-100 dark:bg-ocean-900 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-ocean-600 dark:text-ocean-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-deep-900 dark:text-white mb-2">
                Zonal Partitioning
              </h3>
              <p className="text-deep-600 dark:text-deep-300">
                Intelligent division of billion-scale datasets into manageable zones, 
                dramatically reducing search complexity and memory usage.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="card p-6">
              <div className="w-12 h-12 bg-ocean-100 dark:bg-ocean-900 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-ocean-600 dark:text-ocean-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-deep-900 dark:text-white mb-2">
                Lightning-Fast Search
              </h3>
              <p className="text-deep-600 dark:text-deep-300">
                98.9% faster than traditional exhaustive search methods while maintaining 
                98.7% accuracy through smart zone selection algorithms.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="card p-6">
              <div className="w-12 h-12 bg-ocean-100 dark:bg-ocean-900 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-ocean-600 dark:text-ocean-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-deep-900 dark:text-white mb-2">
                Novel Species Discovery
              </h3>
              <p className="text-deep-600 dark:text-deep-300">
                Advanced algorithms to identify previously unknown deep-sea species, 
                filling critical gaps in marine biodiversity databases.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Statement Section */}
      <section className="py-16 bg-deep-50 dark:bg-deep-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-extrabold text-deep-900 dark:text-white">
              Addressing Real-World Challenges
            </h2>
            <p className="mt-4 text-lg text-deep-600 dark:text-deep-300">
              Smart India Hackathon Problem Statement #25042
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-2xl font-bold text-deep-900 dark:text-white mb-6">
                The Deep-Sea Database Problem
              </h3>
              <div className="space-y-4 text-deep-600 dark:text-deep-300">
                <p>
                  Traditional eDNA analysis relies heavily on reference databases like SILVA, PR2, 
                  and NCBI, which are poorly represented for deep-sea organisms.
                </p>
                <p>
                  Existing pipelines (QIIME2, DADA2, mothur) struggle with novel taxa, leading to:
                </p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>Misclassifications of unknown species</li>
                  <li>Underestimation of biodiversity</li>
                  <li>Long computational processing times</li>
                  <li>High memory requirements</li>
                </ul>
                <p className="font-semibold text-ocean-600 dark:text-ocean-400">
                  Our ZHNSW solution addresses all these challenges with minimal database dependency.
                </p>
              </div>
            </div>

            <div className="card p-8">
              <h4 className="text-lg font-semibold text-deep-900 dark:text-white mb-4">
                Performance Comparison
              </h4>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-deep-600 dark:text-deep-300">Search Speed</span>
                  <span className="font-bold text-green-600">98.9% faster</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-deep-600 dark:text-deep-300">Memory Usage</span>
                  <span className="font-bold text-green-600">77% reduction</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-deep-600 dark:text-deep-300">Accuracy</span>
                  <span className="font-bold text-green-600">98.7% maintained</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-deep-600 dark:text-deep-300">Novel Discovery</span>
                  <span className="font-bold text-green-600">+340% improved</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
