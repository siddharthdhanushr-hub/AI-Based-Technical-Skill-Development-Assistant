import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [progress, setProgress] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profRes, subRes] = await Promise.all([
          api.get('/user/profile'),
          api.get('/syllabus/subjects')
        ]);
        setProfile(profRes.data);
        setSubjects(subRes.data);

        // Fetch analytics & progress gracefully
        try {
          const [anaRes, progRes] = await Promise.all([
            api.get('/ml/analytics'),
            api.get('/user/progress')
          ]);
          setAnalytics(anaRes.data);
          setProgress(progRes.data);
        } catch (e) {
          console.debug("Analytics loading background:", e);
        }
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      }
    };
    fetchData();
  }, []);

  if (!profile) return <div className="flex-center" style={{ height: '50vh' }}>Loading Dashboard...</div>;

  const allTopics = subjects.flatMap(s => s.topics || []);
  const completedTopics = allTopics.filter(t => t.is_completed).length;
  const completionPct = allTopics.length > 0 ? Math.round((completedTopics / allTopics.length) * 100) : 0;

  return (
    <div>
      {/* Header Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ margin: '0 0 6px 0' }}>Welcome, {profile.name}! 👋</h1>
          <p style={{ fontSize: '1.05rem', margin: 0, color: 'var(--text-secondary)' }}>
            Your personalized AI technical skill development and competency command center.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button className="btn" onClick={() => navigate('/century-skills')} style={{ background: '#4f46e5' }}>
            🎯 21st Century Assessment
          </button>
          <button className="btn" onClick={() => navigate('/tracker')} style={{ background: '#0284c7' }}>
            📊 Skill Tracker
          </button>
          <button className="btn btn-secondary" onClick={() => navigate('/mlops-insights')}>
            📈 MLOps Insights
          </button>
        </div>
      </div>

      {/* Featured MLOps Gate Feature Banner */}
      <div
        className="glass-panel"
        style={{
          marginBottom: '28px',
          background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)',
          color: '#ffffff',
          border: 'none',
          padding: '24px'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
          <div style={{ maxWidth: '700px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', background: 'rgba(255,255,255,0.15)', borderRadius: '20px', fontSize: '0.8rem', marginBottom: '10px' }}>
              <span>🚀 MLOps Production Gate</span>
              <span>•</span>
              <span>Random Forest Champion Model (N=8,528 Students)</span>
            </div>
            <h2 style={{ color: '#fff', fontSize: '1.45rem', margin: '0 0 8px 0' }}>
              Assess Your 21st-Century Tech Skills & Unlock Cross-Verification
            </h2>
            <p style={{ color: '#c7d2fe', fontSize: '0.92rem', margin: 0, lineHeight: 1.5 }}>
              Input your self-reported confidence across 10 modern competencies (AI/ML, Data Science, Full-Stack, Cloud Systems, Security, etc.). Our trained MLOps champion evaluates your readiness threshold ($P \ge 50\%$). If qualified, take the cross-verification quiz directly; if skill gaps are detected, sync directly to the Skill Tracker for targeted preparation!
            </p>
          </div>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button
              onClick={() => navigate('/century-skills')}
              className="btn"
              style={{ background: '#10b981', color: '#fff', padding: '12px 24px', fontWeight: 700 }}
            >
              🎯 Start Assessment Now
            </button>
            <button
              onClick={() => navigate('/mlops-insights')}
              className="btn"
              style={{ background: 'rgba(255,255,255,0.15)', color: '#fff', border: '1px solid rgba(255,255,255,0.25)', padding: '12px 20px', boxShadow: 'none' }}
            >
              📊 Phase 1 & 2 Insights
            </button>
          </div>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '16px',
        marginBottom: '28px'
      }}>
        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #3b82f6' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>SKILL TRACKS</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#1e293b', marginTop: '4px' }}>{subjects.length}</div>
          <span style={{ fontSize: '0.8rem', color: '#64748b' }}>Active domains</span>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #10b981' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>COMPETENCY MASTERY</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#10b981', marginTop: '4px' }}>
            {completedTopics} / {allTopics.length}
          </div>
          <span style={{ fontSize: '0.8rem', color: '#64748b' }}>{completionPct}% competencies verified</span>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #8b5cf6' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>CAREER READINESS SCORE</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#8b5cf6', marginTop: '4px' }}>
            {analytics?.exam_readiness_prob ? `${Math.round(analytics.exam_readiness_prob * 100)}%` : 'Active'}
          </div>
          <span style={{ fontSize: '0.8rem', color: '#64748b' }}>Status: {analytics?.topic_mastery || 'In Progress'}</span>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid #f59e0b' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>ASSESSMENTS COMPLETED</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#d97706', marginTop: '4px' }}>
            {progress.length}
          </div>
          <span style={{ fontSize: '0.8rem', color: '#64748b' }}>Evaluated skill quizzes</span>
        </div>
      </div>

      {/* Main Content: 2 Columns */}
      <div className="grid grid-cols-2">
        {/* Left Column: Your Subjects & Topics Breakdown */}
        <div className="glass-panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2 style={{ margin: 0 }}>🛠️ Skill Tracks & Competencies</h2>
            <button className="btn" onClick={() => navigate('/skills')} style={{ fontSize: '0.8rem', padding: '5px 12px', background: '#e0e7ff', color: '#4338ca' }}>
              Manage Skills
            </button>
          </div>

          {subjects.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '30px', background: '#f8fafc', borderRadius: '12px' }}>
              <p>No skill tracks found. Start by setting up your skills in Skill Manager or running the 21st-Century Assessment!</p>
              <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', marginTop: '10px' }}>
                <button className="btn" onClick={() => navigate('/century-skills')}>
                  🎯 Run 21st Century Assessment
                </button>
                <button className="btn btn-secondary" onClick={() => navigate('/skills')}>
                  Setup Skills Manually
                </button>
              </div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {subjects.map(sub => {
                const sTopics = sub.topics || [];
                const sDone = sTopics.filter(t => t.is_completed).length;
                const sPct = sTopics.length > 0 ? Math.round((sDone / sTopics.length) * 100) : 0;

                return (
                  <div
                    key={sub.subject_id}
                    style={{
                      background: '#fff',
                      padding: '16px',
                      borderRadius: '12px',
                      border: '1px solid var(--border-color)',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.04)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <h3 style={{ margin: 0, fontSize: '1.05rem', color: '#1e293b' }}>{sub.subject_name}</h3>
                      <span style={{ fontSize: '0.8rem', fontWeight: 600, color: sPct === 100 ? '#10b981' : '#64748b' }}>
                        {sDone}/{sTopics.length} done ({sPct}%)
                      </span>
                    </div>

                    <div style={{ background: '#e2e8f0', borderRadius: '999px', height: '8px', overflow: 'hidden', marginBottom: '12px' }}>
                      <div style={{
                        background: sPct === 100 ? '#10b981' : 'var(--accent-color)',
                        height: '100%',
                        width: `${sPct}%`,
                        borderRadius: '999px',
                        transition: 'width 0.4s'
                      }} />
                    </div>

                    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                      <button
                        className="btn"
                        onClick={() => navigate('/tracker')}
                        style={{ padding: '4px 10px', fontSize: '0.75rem', background: '#0284c7' }}
                      >
                        Track Competencies
                      </button>
                      {sTopics.length > 0 && (
                        <button
                          className="btn"
                          onClick={() => navigate('/quiz', { state: { topicIds: sTopics.map(t => t.topic_id) } })}
                          style={{ padding: '4px 10px', fontSize: '0.75rem', background: '#6366f1' }}
                        >
                          Assess Track (10 Qs)
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right Column: AI Suite & Performance Insight */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Quick AI Learning Toolkit */}
          <div className="glass-panel">
            <h2 style={{ marginBottom: '14px' }}>⚡ AI Skill Development Suite</h2>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
              Instant AI tools available in Skill Tracker for every technical domain:
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div
                onClick={() => navigate('/tracker')}
                style={{
                  background: '#f8fafc',
                  padding: '14px',
                  borderRadius: '10px',
                  border: '1px solid var(--border-color)',
                  cursor: 'pointer'
                }}
              >
                <div style={{ fontSize: '1.2rem', marginBottom: '4px' }}>🚀</div>
                <strong style={{ fontSize: '0.9rem', color: '#1e293b' }}>Portfolio Projects</strong>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: '#64748b' }}>Real-world builds with tech stack & resume impact</p>
              </div>

              <div
                onClick={() => navigate('/century-skills')}
                style={{
                  background: '#f8fafc',
                  padding: '14px',
                  borderRadius: '10px',
                  border: '1px solid var(--border-color)',
                  cursor: 'pointer'
                }}
              >
                <div style={{ fontSize: '1.2rem', marginBottom: '4px' }}>🎯</div>
                <strong style={{ fontSize: '0.9rem', color: '#1e293b' }}>21st-Century Gating</strong>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: '#64748b' }}>10-skill self-evaluation with Random Forest champion</p>
              </div>

              <div
                onClick={() => navigate('/tracker')}
                style={{
                  background: '#f8fafc',
                  padding: '14px',
                  borderRadius: '10px',
                  border: '1px solid var(--border-color)',
                  cursor: 'pointer'
                }}
              >
                <div style={{ fontSize: '1.2rem', marginBottom: '4px' }}>🗺️</div>
                <strong style={{ fontSize: '0.9rem', color: '#1e293b' }}>Mastery Roadmaps</strong>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: '#64748b' }}>Structured progression & time allocation</p>
              </div>

              <div
                onClick={() => navigate('/tracker')}
                style={{
                  background: '#f8fafc',
                  padding: '14px',
                  borderRadius: '10px',
                  border: '1px solid var(--border-color)',
                  cursor: 'pointer'
                }}
              >
                <div style={{ fontSize: '1.2rem', marginBottom: '4px' }}>📚</div>
                <strong style={{ fontSize: '0.9rem', color: '#1e293b' }}>Skill Briefs & Cards</strong>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: '#64748b' }}>Interactive flashcards & core concepts</p>
              </div>
            </div>
          </div>

          {/* Weak Topics & Readiness Card */}
          <div className="glass-panel">
            <h2 style={{ marginBottom: '12px' }}>🎯 Skill Readiness Status</h2>
            {analytics?.weak_topics && analytics.weak_topics.length > 0 ? (
              <div style={{ background: '#fef2f2', padding: '14px', borderRadius: '10px', border: '1px solid #fecaca' }}>
                <strong style={{ color: '#991b1b', fontSize: '0.9rem' }}>⚠️ High Priority Competencies to Practice:</strong>
                <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px', color: '#7f1d1d', fontSize: '0.85rem' }}>
                  {analytics.weak_topics.map((wt, i) => (
                    <li key={i}>{wt}</li>
                  ))}
                </ul>
              </div>
            ) : (
              <div style={{ background: '#f0fdf4', padding: '14px', borderRadius: '10px', border: '1px solid #bbf7d0' }}>
                <strong style={{ color: '#166534', fontSize: '0.9rem' }}>✨ On Track:</strong>
                <p style={{ margin: '4px 0 0 0', color: '#14532d', fontSize: '0.85rem' }}>
                  All tested skills demonstrate solid competency. Keep building projects and taking quizzes to advance your profile!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
