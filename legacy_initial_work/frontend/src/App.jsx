import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import TopicSelection from './pages/TopicSelection';
import ConfidenceAssessment from './pages/ConfidenceAssessment';
import RevisionView from './pages/RevisionView';
import QuizSession from './pages/QuizSession';
import PerformanceAnalytics from './pages/PerformanceAnalytics';

function Navigation() {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <span className="brand-badge">AI Assistant</span>
        <h1 style={{ fontSize: '1.15rem' }}>Skill & Readiness Platform</h1>
      </div>
      <div className="nav-links">
        <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>Dashboard</Link>
        <Link to="/topics" className={`nav-link ${location.pathname.startsWith('/topics') ? 'active' : ''}`}>Curriculum</Link>
        <Link to="/analytics" className={`nav-link ${location.pathname === '/analytics' ? 'active' : ''}`}>Analytics</Link>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <main className="app-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/topics" element={<TopicSelection />} />
          <Route path="/confidence/:topicId" element={<ConfidenceAssessment />} />
          <Route path="/revision/:topicId" element={<RevisionView />} />
          <Route path="/quiz/:topicId" element={<QuizSession />} />
          <Route path="/analytics" element={<PerformanceAnalytics />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
