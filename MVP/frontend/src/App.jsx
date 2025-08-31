import { useEffect } from 'react';
import Layout from './components/Layout.jsx';
import LandingPage from './pages/LandingPage.jsx';
import UnifiedAnalysisPage from './pages/UnifiedAnalysisPage.jsx';
import DownloadPage from './pages/DownloadPage.jsx';
import SettingsPage from './pages/SettingsPage.jsx';
import HelpPage from './pages/HelpPage.jsx';
import AboutPage from './pages/AboutPage.jsx';
import { useAppStore } from './store/index.js';

function App() {
  const { currentPage, darkMode } = useAppStore();

  // Apply dark mode to document root
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'landing':
        return <LandingPage />;
      case 'analysis':
        return <UnifiedAnalysisPage />;
      case 'download':
        return <DownloadPage />;
      case 'settings':
        return <SettingsPage />;
      case 'help':
        return <HelpPage />;
      case 'about':
        return <AboutPage />;
      default:
        return <LandingPage />;
    }
  };

  return (
    <Layout>
      {renderCurrentPage()}
    </Layout>
  );
}

export default App;
