import Navigation from './Navigation.jsx';
import { useAppStore } from '../store/index.js';

const Layout = ({ children }) => {
  const { darkMode } = useAppStore();

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      <div className="bg-white dark:bg-deep-900 transition-colors duration-200">
        <Navigation />
        <main className="relative">
          {children}
        </main>
        <Footer />
      </div>
    </div>
  );
};

const Footer = () => {
  return (
    <footer className="bg-deep-50 dark:bg-deep-800 border-t border-deep-200 dark:border-deep-700">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Project Info */}
          <div>
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4">
              DeepSea eDNA Explorer
            </h3>
            <p className="text-deep-600 dark:text-deep-300 text-sm mb-4">
              An AI-driven platform for identifying taxonomy and assessing biodiversity 
              from environmental DNA datasets using the revolutionary ZHNSW algorithm.
            </p>
            <div className="flex items-center space-x-2">
              <span className="inline-block w-2 h-2 bg-green-500 rounded-full"></span>
              <span className="text-sm text-deep-600 dark:text-deep-300">
                Smart India Hackathon 2025
              </span>
            </div>
          </div>

          {/* Organization */}
          <div>
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4">
              Organization
            </h3>
            <div className="space-y-2 text-sm text-deep-600 dark:text-deep-300">
              <p>Ministry of Earth Sciences (MoES)</p>
              <p>Centre for Marine Living Resources and Ecology (CMLRE)</p>
              <p>Problem Statement ID: 25042</p>
            </div>
          </div>

          {/* Technology */}
          <div>
            <h3 className="text-lg font-semibold text-deep-900 dark:text-white mb-4">
              Technology
            </h3>
            <div className="space-y-2 text-sm text-deep-600 dark:text-deep-300">
              <p>• Zonal HNSW Algorithm</p>
              <p>• Deep Learning Classification</p>
              <p>• Real-time Biodiversity Analysis</p>
              <p>• Interactive Data Visualization</p>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-deep-200 dark:border-deep-700">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-deep-500 dark:text-deep-400">
              © 2025 DeepSea eDNA Explorer. Built for Smart India Hackathon.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <span className="text-sm text-deep-500 dark:text-deep-400">
                Powered by React & TailwindCSS
              </span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Layout;
