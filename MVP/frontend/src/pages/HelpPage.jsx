import HelpDocumentation from '../components/HelpDocumentation.jsx';

const HelpPage = () => {
  return (
    <div className="min-h-screen bg-deep-50 dark:bg-deep-900">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-deep-900 dark:text-white">
            Help & Documentation
          </h1>
          <p className="mt-2 text-deep-600 dark:text-deep-300">
            Comprehensive guides, tutorials, and documentation for the Deep-Sea eDNA platform.
          </p>
        </div>
        
        <HelpDocumentation />
      </div>
    </div>
  );
};

export default HelpPage;
