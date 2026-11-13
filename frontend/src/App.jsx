import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import SkillManager from './pages/SkillManager';
import QuizSession from './pages/QuizSession';
import StudyTracker from './pages/StudyTracker';
import PerformanceAnalytics from './pages/PerformanceAnalytics';
import CenturySkillsAssessment from './pages/CenturySkillsAssessment';
import MLOpsInsights from './pages/MLOpsInsights';

function Navigation() {
  return (
    <nav className="navbar">
      <div className="nav-brand">
        <h2>AI Based Technical Skill Development Assistant</h2>
      </div>
      <div className="nav-links">
        <Link to="/" className="nav-link" style={{ fontWeight: 700, color: '#4f46e5' }}>
          🎯 21st Century Assessment
        </Link>
        <Link to="/tracker" className="nav-link">📊 Skill Tracker</Link>
        <Link to="/quiz" className="nav-link">🧠 Skill Quizzes</Link>
        <Link to="/skills" className="nav-link">🛠️ Skill Manager</Link>
        <Link to="/mlops-insights" className="nav-link">📈 MLOps Insights</Link>
        <Link to="/performance" className="nav-link">Performance</Link>
        <Link to="/dashboard" className="nav-link" style={{ opacity: 0.85 }}>Overview</Link>
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <div className="container">
        <Routes>
          {/* Default Landing Page: 21st-Century Technical Skill Confidence Assessment */}
          <Route path="/" element={<CenturySkillsAssessment />} />
          <Route path="/century-skills" element={<CenturySkillsAssessment />} />
          <Route path="/tracker" element={<StudyTracker />} />
          <Route path="/quiz" element={<QuizSession />} />
          <Route path="/skills" element={<SkillManager />} />
          <Route path="/syllabus" element={<Navigate to="/skills" replace />} />
          <Route path="/mlops-insights" element={<MLOpsInsights />} />
          <Route path="/performance" element={<PerformanceAnalytics />} />
          <Route path="/dashboard" element={<Dashboard />} />
          
          {/* Hidden/Redirected routes */}
          <Route path="/profile" element={<Navigate to="/" replace />} />
          <Route path="/login" element={<Navigate to="/" replace />} />
          <Route path="/admin" element={<Navigate to="/" replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
