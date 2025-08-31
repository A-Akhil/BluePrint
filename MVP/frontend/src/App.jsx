import { useEffect } from 'react';
import Layout from './components/Layout.jsx';
import LandingPage from './pages/LandingPage.jsx';
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
        return <div className="p-8"><h1 className="text-2xl font-bold">Analysis Page Coming Soon...</h1></div>;
      case 'zones':
        return <div className="p-8"><h1 className="text-2xl font-bold">Zones Page Coming Soon...</h1></div>;
      case 'taxonomy':
        return <div className="p-8"><h1 className="text-2xl font-bold">Taxonomy Page Coming Soon...</h1></div>;
      case 'about':
        return <div className="p-8"><h1 className="text-2xl font-bold">About Page Coming Soon...</h1></div>;
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
