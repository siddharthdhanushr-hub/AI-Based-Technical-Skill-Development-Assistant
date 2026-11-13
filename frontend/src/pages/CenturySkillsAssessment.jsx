import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const SKILLS_CONFIG = [
  { key: 'ai_ml', name: 'AI / Machine Learning', desc: 'Neural networks, LLMs, model training, evaluation & PyTorch/TensorFlow' },
  { key: 'data_science', name: 'Data Science & Analytics', desc: 'Pandas, NumPy, exploratory analysis, statistical modeling & data visualization' },
  { key: 'software_development', name: 'Software Development', desc: 'Clean architecture, OOP/FP paradigms, modular design & version control' },
  { key: 'programming_skills', name: 'Core Programming Skills', desc: 'Algorithms, data structures, recursion, asymptotic complexity & debugging' },
  { key: 'cyber_security', name: 'Cyber Security', desc: 'Authentication, encryption, OWASP top 10 vulnerabilities & threat modeling' },
  { key: 'distributed_computing_systems', name: 'Distributed Systems', desc: 'Cloud architectures, microservices, consensus, Docker, Kubernetes & message queues' },
  { key: 'database_fundamentals', name: 'Database Fundamentals', desc: 'SQL schema design, relational normalization, indexing, ACID & NoSQL caching' },
  { key: 'software_engineering', name: 'Software Engineering & CI/CD', desc: 'Automated testing, unit/integration suites, code review, GitOps & pipelines' },
  { key: 'troubleshooting_skills', name: 'Troubleshooting & Profiling', desc: 'Root cause analysis, system logs, memory profiling & performance bottlenecks' },
  { key: 'technical_communication', name: 'Technical Communication', desc: 'Architectural documentation, API contracts, technical briefs & design reviews' },
];

const ROLES = [
  "Software Developer",
  "AI/ML Specialist",
  "Cyber Security Specialist",
  "Data Scientist",
  "Cloud Engineer",
  "Database Administrator",
  "DevOps / Infrastructure Engineer",
  "Systems Architect",
  "Backend Engineer",
  "Full Stack Engineer",
  "QA / Test Automation Engineer",
  "Technical Product Engineer",
  "Security Operations Analyst",
  "Big Data Platform Engineer",
  "Embedded & Distributed Systems Engineer",
  "Generalist Technical Specialist"
];

const RATING_LABELS = [
  { val: 0, label: "Novice (0)", color: "#94a3b8" },
  { val: 1, label: "Beginner (1)", color: "#64748b" },
  { val: 2, label: "Foundational (2)", color: "#eab308" },
  { val: 3, label: "Intermediate (3)", color: "#3b82f6" },
  { val: 4, label: "Proficient (4)", color: "#06b6d4" },
  { val: 5, label: "Advanced (5)", color: "#10b981" },
  { val: 6, label: "Expert (6)", color: "#8b5cf6" },
];

export default function CenturySkillsAssessment() {
  const navigate = useNavigate();

  // Ratings for 10 21st century tech skills (default to 3)
  const [ratings, setRatings] = useState({
    ai_ml: 3,
    data_science: 3,
    software_development: 3,
    programming_skills: 3,
    cyber_security: 3,
    distributed_computing_systems: 3,
    database_fundamentals: 3,
    software_engineering: 3,
    troubleshooting_skills: 3,
    technical_communication: 3,
  });

  const [selectedRole, setSelectedRole] = useState("Software Developer");
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [evalResult, setEvalResult] = useState(null);
  const [syncStatus, setSyncStatus] = useState(null);

  // Verification Quiz State
  const [showQuiz, setShowQuiz] = useState(false);
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [quizLoading, setQuizLoading] = useState(false);
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState(null);

  const handleRatingChange = (key, val) => {
    setRatings(prev => ({ ...prev, [key]: Number(val) }));
    if (evalResult) {
      setEvalResult(null); // Clear previous result when rating changes
      setShowQuiz(false);
    }
  };

  const applyPreset = (preset) => {
    const updated = {};
    SKILLS_CONFIG.forEach(s => {
      if (preset === 'high') updated[s.key] = 5;
      else if (preset === 'low') updated[s.key] = 1;
      else updated[s.key] = 3;
    });
    setRatings(updated);
    setEvalResult(null);
    setShowQuiz(false);
  };

  const runEvaluation = async () => {
    setIsEvaluating(true);
    setEvalResult(null);
    setSyncStatus(null);
    setShowQuiz(false);
    try {
      const res = await api.post('/mlops/evaluate', {
        skills: ratings,
        target_role: selectedRole
      });
      setEvalResult(res.data);

      // If below threshold and gaps exist, proactively sync to tracker
      const weakList = res.data.weak_skills || res.data.gap_skills || [];
      if (res.data.recommendation === 'PREPARE_IN_TRACKER' && weakList.length > 0) {
        syncToTracker(weakList, false);
      }
    } catch (err) {
      alert(err.response?.data?.detail || "MLOps assessment evaluation failed. Please verify the backend is running.");
    } finally {
      setIsEvaluating(false);
    }
  };

  const syncToTracker = async (gapSkills, notify = true) => {
    try {
      setSyncStatus({ loading: true, message: "Syncing skills to Tracker..." });
      const res = await api.post('/mlops/sync-tracker', {
        role: selectedRole,
        gap_skills: gapSkills
      });
      setSyncStatus({
        loading: false,
        success: true,
        message: res.data.message || `Successfully synced ${gapSkills.length} skills to Skill Tracker!`,
        subjectId: res.data.subject_id
      });
      if (notify) {
        alert(`Synced ${gapSkills.length} skills to Tracker under "21st Century Skills: ${selectedRole}"! Redirecting...`);
        navigate('/tracker');
      }
    } catch (err) {
      setSyncStatus({
        loading: false,
        success: false,
        message: "Failed to sync to tracker: " + (err.response?.data?.detail || err.message)
      });
    }
  };

  const startVerificationQuiz = async () => {
    setQuizLoading(true);
    setShowQuiz(true);
    setQuizSubmitted(false);
    setQuizAnswers({});
    setQuizScore(null);
    try {
      const res = await api.get('/mlops/verification-quiz');
      setQuizQuestions(res.data.questions || []);
      // Scroll to quiz section smoothly
      setTimeout(() => {
        const el = document.getElementById('verification-quiz-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      alert("Failed to load verification quiz: " + (err.response?.data?.detail || err.message));
      setShowQuiz(false);
    } finally {
      setQuizLoading(false);
    }
  };

  const handleSelectQuizAnswer = (qIndex, optionKey) => {
    if (quizSubmitted) return;
    setQuizAnswers(prev => ({ ...prev, [qIndex]: optionKey }));
  };

  const submitQuiz = () => {
    let correct = 0;
    quizQuestions.forEach((q, idx) => {
      const userAns = (quizAnswers[idx] || '').trim().toUpperCase();
      const actual = (q.correct_option || '').trim().toUpperCase();
      if (userAns === actual) correct++;
    });
    setQuizScore({
      correct,
      total: quizQuestions.length,
      percentage: Math.round((correct / quizQuestions.length) * 100)
    });
    setQuizSubmitted(true);
  };

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', paddingBottom: '60px' }}>
      {/* Hero Header */}
      <div className="glass-panel" style={{ marginBottom: '24px', background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)', color: '#fff', border: 'none' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', background: 'rgba(255,255,255,0.15)', borderRadius: '20px', fontSize: '0.82rem', marginBottom: '12px' }}>
              <span>⚡ MLOps Production Gate</span>
              <span>•</span>
              <span>Random Forest Champion (N=8,528 Benchmark)</span>
            </div>
            <h1 style={{ color: '#fff', fontSize: '2rem', marginBottom: '8px' }}>
              21st-Century Tech Skills Readiness Assessment
            </h1>
            <p style={{ color: '#c7d2fe', fontSize: '1rem', maxWidth: '750px', marginBottom: 0 }}>
              Rate your self-reported confidence across the 10 core technical competencies. Our MLOps evaluation engine predicts candidate pass readiness, detects role-specific skill gaps, and unlocks cross-verification testing.
            </p>
          </div>
          <button
            onClick={() => navigate('/mlops-insights')}
            className="btn"
            style={{ background: 'rgba(255,255,255,0.15)', color: '#fff', border: '1px solid rgba(255,255,255,0.25)', boxShadow: 'none' }}
          >
            📊 View Phase 1 & 2 Insights
          </button>
        </div>
      </div>

      {/* Target Role & Preset Selection */}
      <div className="glass-panel" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ flex: '1 1 300px' }}>
            <label style={{ display: 'block', fontSize: '0.9rem', fontWeight: 600, color: '#334155', marginBottom: '8px' }}>
              🎯 Select Target Engineering Role
            </label>
            <select
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
              className="input-field"
              style={{ width: '100%', fontSize: '1rem', fontWeight: 600, background: '#f8fafc' }}
            >
              {ROLES.map(role => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', alignItems: 'flex-end' }}>
            <span style={{ fontSize: '0.85rem', color: '#64748b', alignSelf: 'center', marginRight: '4px' }}>Presets:</span>
            <button
              onClick={() => applyPreset('high')}
              className="btn btn-secondary"
              style={{ fontSize: '0.82rem', padding: '8px 14px' }}
            >
              ⚡ High Proficiency
            </button>
            <button
              onClick={() => applyPreset('low')}
              className="btn btn-secondary"
              style={{ fontSize: '0.82rem', padding: '8px 14px' }}
            >
              🌱 Entry-Level
            </button>
            <button
              onClick={() => applyPreset('reset')}
              className="btn btn-secondary"
              style={{ fontSize: '0.82rem', padding: '8px 14px' }}
            >
              🔄 Reset (3.0)
            </button>
          </div>
        </div>
      </div>

      {/* 10 Skills Rating Matrix */}
      <div className="glass-panel" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid #f1f5f9', paddingBottom: '12px' }}>
          <div>
            <h3 style={{ margin: 0, fontSize: '1.25rem', color: '#1e293b' }}>
              Core 21st-Century Competency Vector (10 Dimensions)
            </h3>
            <p style={{ margin: '4px 0 0', fontSize: '0.88rem', color: '#64748b' }}>
              Scale: 0 (Novice / None) to 6 (Expert / Production Mastery)
            </p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <span style={{ fontSize: '0.85rem', color: '#64748b' }}>Average Rating: </span>
            <strong style={{ fontSize: '1.1rem', color: '#4f46e5' }}>
              {(Object.values(ratings).reduce((a, b) => a + b, 0) / 10).toFixed(1)} / 6.0
            </strong>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {SKILLS_CONFIG.map((skill, index) => {
            const currentVal = ratings[skill.key] || 0;
            const currentLabel = RATING_LABELS.find(r => r.val === currentVal) || RATING_LABELS[0];

            return (
              <div
                key={skill.key}
                style={{
                  padding: '16px 20px',
                  borderRadius: '12px',
                  border: '1px solid #e2e8f0',
                  background: currentVal >= 4 ? '#f8fafc' : '#ffffff',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px',
                  transition: 'all 0.15s ease'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#94a3b8' }}>#{index + 1}</span>
                      <strong style={{ fontSize: '1rem', color: '#1e293b' }}>{skill.name}</strong>
                    </div>
                    <p style={{ margin: '4px 0 0', fontSize: '0.85rem', color: '#64748b' }}>{skill.desc}</p>
                  </div>
                  <span
                    style={{
                      display: 'inline-block',
                      padding: '4px 12px',
                      borderRadius: '16px',
                      fontSize: '0.82rem',
                      fontWeight: 600,
                      background: currentLabel.color + '15',
                      color: currentLabel.color,
                      border: `1px solid ${currentLabel.color}40`
                    }}
                  >
                    {currentLabel.label}
                  </span>
                </div>

                {/* Rating Button Group */}
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  {[0, 1, 2, 3, 4, 5, 6].map(num => {
                    const isSelected = currentVal === num;
                    return (
                      <button
                        key={num}
                        type="button"
                        onClick={() => handleRatingChange(skill.key, num)}
                        style={{
                          flex: '1 1 60px',
                          padding: '8px 4px',
                          borderRadius: '8px',
                          border: isSelected ? '2px solid #4f46e5' : '1px solid #cbd5e1',
                          background: isSelected ? '#4f46e5' : '#ffffff',
                          color: isSelected ? '#ffffff' : '#334155',
                          fontWeight: isSelected ? 700 : 500,
                          fontSize: '0.85rem',
                          cursor: 'pointer',
                          transition: 'all 0.15s ease'
                        }}
                      >
                        {num}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        {/* Evaluation Trigger Button */}
        <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'center' }}>
          <button
            onClick={runEvaluation}
            disabled={isEvaluating}
            className="btn"
            style={{
              padding: '14px 40px',
              fontSize: '1.05rem',
              background: 'linear-gradient(135deg, #4f46e5 0%, #4338ca 100%)',
              boxShadow: '0 8px 16px -4px rgba(79, 70, 229, 0.4)'
            }}
          >
            {isEvaluating ? '🔄 Evaluating via Random Forest Engine...' : '🚀 Evaluate Confidence & Threshold Gating'}
          </button>
        </div>
      </div>

      {/* Evaluation Results Section */}
      {evalResult && (() => {
        const isPass = evalResult.assessment_pass ?? evalResult.prediction?.pass ?? false;
        const confPct = evalResult.confidence_percentage ?? (evalResult.confidence_score ? (evalResult.confidence_score * 100).toFixed(1) : ((evalResult.confidence || 0) * 100).toFixed(1));
        const weakList = evalResult.weak_skills || evalResult.gap_skills || [];
        const rfPass = evalResult.model_votes ? evalResult.model_votes.random_forest_champion === 1 : isPass;
        const dtPass = evalResult.model_votes ? evalResult.model_votes.decision_tree === 1 : isPass;
        const lrPass = evalResult.model_votes ? evalResult.model_votes.logistic_regression === 1 : isPass;

        return (
          <div className="glass-panel" style={{ marginBottom: '24px', animation: 'fadeIn 0.3s ease' }}>
            {/* Recommendation Banner */}
            {isPass ? (
              <div style={{ padding: '24px', borderRadius: '12px', background: '#ecfdf5', border: '1px solid #a7f3d0', marginBottom: '24px' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '2.5rem' }}>🏆</span>
                  <div style={{ flex: '1 1 300px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <h3 style={{ margin: 0, color: '#065f46', fontSize: '1.4rem' }}>
                        High Confidence Verified — Ready for Cross-Verification Quiz!
                      </h3>
                      <span className="badge badge-success" style={{ fontSize: '0.85rem' }}>Pass Probability: {confPct}%</span>
                    </div>
                    <p style={{ margin: '8px 0 16px', color: '#047857', fontSize: '0.95rem', lineHeight: 1.6 }}>
                      Your aggregate skill profile exceeds the threshold benchmark (P &ge; 50%) for <strong>{selectedRole}</strong>. 
                      To validate that your self-reported ratings align with actual engineering competence, take the 10-question 21st-century skills cross-verification quiz directly.
                    </p>
                    <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
                      <button
                        onClick={startVerificationQuiz}
                        disabled={quizLoading}
                        className="btn"
                        style={{ background: '#059669', padding: '12px 28px', fontSize: '0.95rem' }}
                      >
                        {quizLoading ? '⏳ Loading Quiz...' : '🎯 Take 21st-Century Cross-Verification Quiz (10 Qs)'}
                      </button>
                      <button
                        onClick={() => navigate('/quiz')}
                        className="btn"
                        style={{ background: '#4f46e5', padding: '12px 22px', fontSize: '0.9rem' }}
                      >
                        🧠 Open Full Quiz Session
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div style={{ padding: '24px', borderRadius: '12px', background: '#fffbeb', border: '1px solid #fde68a', marginBottom: '24px' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '2.5rem' }}>⚠️</span>
                  <div style={{ flex: '1 1 300px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <h3 style={{ margin: 0, color: '#92400e', fontSize: '1.4rem' }}>
                        Skill Gaps Detected — Preparation in Tracker Recommended
                      </h3>
                      <span style={{ padding: '4px 10px', borderRadius: '16px', background: '#fef3c7', color: '#b45309', border: '1px solid #fde68a', fontWeight: 600, fontSize: '0.85rem' }}>
                        Confidence: {confPct}%
                      </span>
                    </div>
                    <p style={{ margin: '8px 0 16px', color: '#78350f', fontSize: '0.95rem', lineHeight: 1.6 }}>
                      Your overall confidence profile is below the pass threshold for <strong>{selectedRole}</strong>, with <strong>{weakList.length} critical skill gap(s)</strong> identified. 
                      We have synced these weak areas to your <strong>Skill Tracker</strong> so you can study <strong>Skill Briefs</strong>, review <strong>Flashcards</strong>, and build <strong>Portfolio Projects</strong> before attempting the verification exam.
                    </p>

                    <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'center' }}>
                      <button
                        onClick={() => navigate('/tracker')}
                        className="btn"
                        style={{ background: '#d97706', padding: '12px 28px', fontSize: '0.95rem' }}
                      >
                        📊 Open Skill Tracker & Prepare Topics
                      </button>
                      <button
                        onClick={startVerificationQuiz}
                        disabled={quizLoading}
                        className="btn btn-secondary"
                        style={{ fontSize: '0.9rem', padding: '10px 18px' }}
                      >
                        {quizLoading ? '⏳ Loading...' : 'Skip to Quiz Anyway'}
                      </button>
                    </div>

                    {syncStatus && (
                      <div style={{ marginTop: '12px', fontSize: '0.85rem', color: syncStatus.success ? '#065f46' : '#991b1b' }}>
                        {syncStatus.message}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Model Predictions Breakdown */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', marginBottom: '24px' }}>
              <div style={{ padding: '16px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>Random Forest (Champion)</span>
                  <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '12px', background: '#eff6ff', color: '#2563eb', fontWeight: 600 }}>N=8,528 Acc: 73.5%</span>
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: rfPass ? '#059669' : '#dc2626' }}>
                  {rfPass ? 'Pass / Ready' : 'Review Required'}
                </div>
                <div style={{ marginTop: '6px', fontSize: '0.82rem', color: '#64748b' }}>
                  Confidence: <strong>{confPct}%</strong> (Threshold: 50%)
                </div>
              </div>

              <div style={{ padding: '16px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>Decision Tree (Candidate)</span>
                  <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '12px', background: '#f1f5f9', color: '#64748b' }}>Acc: 72.0%</span>
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: dtPass ? '#059669' : '#dc2626' }}>
                  {dtPass ? 'Pass / Ready' : 'Review Required'}
                </div>
                <div style={{ marginTop: '6px', fontSize: '0.82rem', color: '#64748b' }}>
                  Ensemble Vote: <strong>{dtPass ? '1 (Pass)' : '0 (Fail)'}</strong>
                </div>
              </div>

              <div style={{ padding: '16px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>Logistic Regression (Baseline)</span>
                  <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '12px', background: '#f1f5f9', color: '#64748b' }}>Acc: 73.4%</span>
                </div>
                <div style={{ fontSize: '1.4rem', fontWeight: 700, color: lrPass ? '#059669' : '#dc2626' }}>
                  {lrPass ? 'Pass / Ready' : 'Review Required'}
                </div>
                <div style={{ marginTop: '6px', fontSize: '0.82rem', color: '#64748b' }}>
                  Ensemble Vote: <strong>{lrPass ? '1 (Pass)' : '0 (Fail)'}</strong>
                </div>
              </div>
            </div>

            {/* Skill Gap Analysis Table against Target Role */}
            <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '20px' }}>
              <h4 style={{ margin: '0 0 12px', color: '#1e293b' }}>
                Role Competency Alignment: {selectedRole}
              </h4>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' }}>
                  <thead>
                    <tr style={{ background: '#f8fafc', textAlign: 'left', borderBottom: '2px solid #e2e8f0' }}>
                      <th style={{ padding: '10px 12px', color: '#475569' }}>Skill Dimension</th>
                      <th style={{ padding: '10px 12px', color: '#475569' }}>Your Rating</th>
                      <th style={{ padding: '10px 12px', color: '#475569' }}>Target Threshold</th>
                      <th style={{ padding: '10px 12px', color: '#475569' }}>Gap Status</th>
                      <th style={{ padding: '10px 12px', color: '#475569' }}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {SKILLS_CONFIG.map(skill => {
                      const userVal = ratings[skill.key] || 0;
                      const gapObj = evalResult.skill_gaps?.find(g => g.skill_id === skill.key);
                      const reqVal = gapObj ? gapObj.required_score : 3;
                      const gap = gapObj ? gapObj.gap : Math.max(0, reqVal - userVal);
                      const isGap = gap > 0;

                      return (
                        <tr key={skill.key} style={{ borderBottom: '1px solid #f1f5f9' }}>
                          <td style={{ padding: '10px 12px', fontWeight: 600, color: '#1e293b' }}>
                            {skill.name}
                          </td>
                          <td style={{ padding: '10px 12px' }}>
                            <span style={{ fontWeight: 600, color: userVal >= reqVal ? '#059669' : '#dc2626' }}>
                              {userVal} / 6
                            </span>
                          </td>
                          <td style={{ padding: '10px 12px', color: '#64748b' }}>
                            {reqVal} / 6
                          </td>
                          <td style={{ padding: '10px 12px' }}>
                            {isGap ? (
                              <span style={{ padding: '2px 8px', borderRadius: '12px', background: '#fee2e2', color: '#991b1b', fontWeight: 600, fontSize: '0.78rem' }}>
                                Gap (-{gap})
                              </span>
                            ) : (
                              <span style={{ padding: '2px 8px', borderRadius: '12px', background: '#ecfdf5', color: '#065f46', fontWeight: 600, fontSize: '0.78rem' }}>
                                ✓ Satisfied
                              </span>
                            )}
                          </td>
                          <td style={{ padding: '10px 12px' }}>
                            {isGap ? (
                              <span style={{ color: '#d97706', fontSize: '0.8rem' }}>Syncs to Tracker</span>
                            ) : (
                              <span style={{ color: '#64748b', fontSize: '0.8rem' }}>Ready for Quiz</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        );
      })()}

      {/* 21st-Century Cross-Verification Quiz Section */}
      {showQuiz && (
        <div id="verification-quiz-section" className="glass-panel" style={{ marginTop: '24px', animation: 'fadeIn 0.3s ease' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid #e2e8f0', paddingBottom: '16px' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.5rem' }}>🎯</span>
                <h3 style={{ margin: 0, color: '#1e293b', fontSize: '1.35rem' }}>
                  21st-Century Tech Skills Cross-Verification Exam
                </h3>
              </div>
              <p style={{ margin: '4px 0 0', fontSize: '0.88rem', color: '#64748b' }}>
                10 rigorous multiple-choice questions covering all 10 evaluated technical dimensions.
              </p>
            </div>
            {!quizSubmitted && (
              <span className="badge" style={{ fontSize: '0.85rem' }}>
                Answered: {Object.keys(quizAnswers).length} / {quizQuestions.length}
              </span>
            )}
          </div>

          {/* Score Banner if Submitted */}
          {quizSubmitted && quizScore && (
            <div style={{
              padding: '20px',
              borderRadius: '12px',
              background: quizScore.percentage >= 70 ? '#ecfdf5' : '#fffbeb',
              border: `1px solid ${quizScore.percentage >= 70 ? '#a7f3d0' : '#fde68a'}`,
              marginBottom: '24px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
                <div>
                  <h4 style={{ margin: 0, color: quizScore.percentage >= 70 ? '#065f46' : '#92400e', fontSize: '1.25rem' }}>
                    {quizScore.percentage >= 70 ? '🎉 Verification Passed!' : '📖 Review Recommended'}
                  </h4>
                  <p style={{ margin: '6px 0 0', fontSize: '0.9rem', color: quizScore.percentage >= 70 ? '#047857' : '#78350f' }}>
                    You scored <strong>{quizScore.correct} / {quizScore.total} ({quizScore.percentage}%)</strong> on the cross-verification exam.
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => {
                      setQuizSubmitted(false);
                      setQuizAnswers({});
                    }}
                    className="btn btn-secondary"
                    style={{ fontSize: '0.85rem' }}
                  >
                    🔄 Retake Exam
                  </button>
                  <button
                    onClick={() => navigate('/tracker')}
                    className="btn"
                    style={{ fontSize: '0.85rem', background: '#059669' }}
                  >
                    📊 Go to Skill Tracker
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Quiz Question Cards */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {quizQuestions.map((q, idx) => {
              const selected = quizAnswers[idx];
              const isCorrect = selected === q.correct_option;

              return (
                <div
                  key={idx}
                  style={{
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid #e2e8f0',
                    background: '#ffffff'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px', gap: '10px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontWeight: 700, color: '#4f46e5' }}>Q{idx + 1}.</span>
                      <span style={{ fontWeight: 600, color: '#1e293b', fontSize: '0.98rem' }}>{q.question_text}</span>
                    </div>
                    <div style={{ display: 'flex', gap: '6px', flexShrink: 0 }}>
                      <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '10px', background: '#f1f5f9', color: '#475569', fontWeight: 600 }}>
                        {q.skill_dimension}
                      </span>
                      <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '10px', background: '#eff6ff', color: '#2563eb', fontWeight: 600 }}>
                        {q.difficulty}
                      </span>
                    </div>
                  </div>

                  {/* Options */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '10px', marginTop: '12px' }}>
                    {['A', 'B', 'C', 'D'].map(optKey => {
                      const optText = q[`option_${optKey.toLowerCase()}`];
                      const isOptionSelected = selected === optKey;
                      const isOptionCorrect = q.correct_option === optKey;

                      let optBg = '#f8fafc';
                      let optBorder = '#e2e8f0';
                      let optColor = '#334155';

                      if (quizSubmitted) {
                        if (isOptionCorrect) {
                          optBg = '#ecfdf5';
                          optBorder = '#10b981';
                          optColor = '#065f46';
                        } else if (isOptionSelected && !isOptionCorrect) {
                          optBg = '#fef2f2';
                          optBorder = '#ef4444';
                          optColor = '#991b1b';
                        }
                      } else if (isOptionSelected) {
                        optBg = '#eff6ff';
                        optBorder = '#3b82f6';
                        optColor = '#1d4ed8';
                      }

                      return (
                        <div
                          key={optKey}
                          onClick={() => handleSelectQuizAnswer(idx, optKey)}
                          style={{
                            padding: '12px 14px',
                            borderRadius: '8px',
                            border: `1.5px solid ${optBorder}`,
                            background: optBg,
                            color: optColor,
                            cursor: quizSubmitted ? 'default' : 'pointer',
                            display: 'flex',
                            alignItems: 'flex-start',
                            gap: '10px',
                            fontSize: '0.88rem',
                            transition: 'all 0.15s ease'
                          }}
                        >
                          <span style={{ fontWeight: 700, minWidth: '20px' }}>{optKey}.</span>
                          <span style={{ flex: 1 }}>{optText}</span>
                        </div>
                      );
                    })}
                  </div>

                  {/* Explanation after submission */}
                  {quizSubmitted && (
                    <div style={{ marginTop: '14px', padding: '12px', borderRadius: '8px', background: '#f8fafc', borderLeft: `4px solid ${isCorrect ? '#10b981' : '#f59e0b'}`, fontSize: '0.85rem' }}>
                      <strong style={{ color: isCorrect ? '#065f46' : '#92400e' }}>
                        {isCorrect ? '✓ Correct! ' : '✕ Incorrect. '}
                      </strong>
                      <span style={{ color: '#475569' }}>{q.explanation}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Quiz Action Buttons */}
          <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'center', gap: '16px' }}>
            {!quizSubmitted ? (
              <button
                onClick={submitQuiz}
                disabled={Object.keys(quizAnswers).length === 0}
                className="btn"
                style={{ padding: '12px 36px', background: '#059669', fontSize: '1rem' }}
              >
                Submit Cross-Verification Quiz ({Object.keys(quizAnswers).length}/{quizQuestions.length})
              </button>
            ) : (
              <button
                onClick={() => navigate('/tracker')}
                className="btn"
                style={{ padding: '12px 36px', background: '#4f46e5', fontSize: '1rem' }}
              >
                📊 Continue Learning in Skill Tracker
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
