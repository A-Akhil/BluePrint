import DownloadExport from '../components/DownloadExport.jsx';
import { useAppStore } from '../store/index.js';

const DownloadPage = () => {
  const { getPaginatedSequences, currentSearch } = useAppStore();
  const paginatedData = getPaginatedSequences();

  return (
    <div className="min-h-screen bg-deep-50 dark:bg-deep-900">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-deep-900 dark:text-white">
            Download & Export
          </h1>
          <p className="mt-2 text-deep-600 dark:text-deep-300">
            Export your analysis results in multiple formats for further research and publication.
          </p>
        </div>
        
        <DownloadExport 
          sequences={paginatedData.sequences} 
          currentSearch={currentSearch}
        />
      </div>
    </div>
  );
};

export default DownloadPage;
