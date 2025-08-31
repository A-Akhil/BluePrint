import SettingsConfiguration from '../components/SettingsConfiguration.jsx';

const SettingsPage = () => {
  return (
    <div className="min-h-screen bg-deep-50 dark:bg-deep-900">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-deep-900 dark:text-white">
            Settings & Configuration
          </h1>
          <p className="mt-2 text-deep-600 dark:text-deep-300">
            Customize your analysis parameters, display preferences, and system settings.
          </p>
        </div>
        
        <SettingsConfiguration />
      </div>
    </div>
  );
};

export default SettingsPage;
