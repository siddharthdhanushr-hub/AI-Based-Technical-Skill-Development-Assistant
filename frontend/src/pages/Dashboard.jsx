import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FALLBACK_CURRICULUM } from '../api';

export default function Dashboard() {
  const [stats, setStats] = useState({
    assessedCount: 0,
    weakTopicsCount: 0,
    quizzesCompleted: 0,
    averageScore: 0
  });

  const [recentAssessments, setRecentAssessments] = useState([]);

  useEffect(() => {
    // Load student state from localStorage
    const savedConfidence = JSON.parse(localStorage.getItem('topic_confidence') || '{}');
    const quizHistory = JSON.parse(localStorage.getItem('quiz_history') || '[]');

    const confidenceEntries = Object.entries(savedConfidence);
    const weakCount = confidenceEntries.filter(([_, conf]) => conf < 60).length;

    const avgScore = quizHistory.length > 0 
      ? Math.round(quizHistory.reduce((acc, q) => acc + q.score, 0) / quizHistory.length)
      : 0;

    setStats({
      assessedCount: confidenceEntries.length,
      weakTopicsCount: weakCount,
      quizzesCompleted: quizHistory.length,
      averageScore: avgScore
    });

    const recent = confidenceEntries.map(([topicId, conf]) => {
      const allTopics = Object.values(FALLBACK_CURRICULUM.topics).flat();
      const topicObj = allTopics.find(t => t.topic_id === topicId) || { topic_name: topicId };
      const latestQuiz = quizHistory.find(q => q.topic_id === topicId);

      let gripStatus = 'Provisional (Unassessed)';
      if (latestQuiz) {
        if (latestQuiz.score < 60) gripStatus = 'Needs Revision';
        else if (latestQuiz.score < 80) gripStatus = 'Developing';
        else gripStatus = 'Demonstrated Mastery';
      }

      return {
        topic_id: topicId,
        topic_name: topicObj.topic_name,
        confidence: conf,
        quizScore: latestQuiz ? `${latestQuiz.score}%` : 'Not Taken',
        grip: gripStatus,
        needsRevision: conf < 60
      };
    });

    setRecentAssessments(recent);
  }, []);

  return (
    <div className="dashboard-page">
      <header style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '8px' }}>
          Personalized Skill & Readiness Dashboard
        </h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Directly track your topic-wise self-confidence against demonstrated quiz performance.
        </p>
      </header>

      {/* Metric Cards */}
      <div className="grid-4" style={{ marginBottom: '32px' }}>
        <div className="card stat-box">
          <div className="stat-label">Assessed Topics</div>
          <div className="stat-value">{stats.assessedCount}</div>
        </div>

        <div className="card stat-box">
          <div className="stat-label">Weak Topics (&lt; 60%)</div>
          <div className="stat-value" style={{ color: stats.weakTopicsCount > 0 ? '#f87171' : 'var(--text-primary)' }}>
            {stats.weakTopicsCount}
          </div>
        </div>

        <div className="card stat-box">
          <div className="stat-label">Quizzes Completed</div>
          <div className="stat-value" style={{ color: '#818cf8' }}>
            {stats.quizzesCompleted}
          </div>
        </div>

        <div className="card stat-box">
          <div className="stat-label">Avg Quiz Score</div>
          <div className="stat-value" style={{ color: '#34d399' }}>
            {stats.averageScore}%
          </div>
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="grid-2">
        {/* Topic Readiness Summary */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Topic Grip & Readiness</h3>
            <Link to="/topics" className="btn btn-outline" style={{ fontSize: '0.85rem', padding: '6px 14px' }}>
              Explore Curriculum &rarr;
            </Link>
          </div>

          {recentAssessments.length === 0 ? (
            <div style={{ padding: '32px 0', textAlign: 'center', color: 'var(--text-muted)' }}>
              <p>No topics assessed yet.</p>
              <p style={{ fontSize: '0.9rem', marginTop: '6px' }}>
                Select a topic from the curriculum to rate your confidence and unlock targeted practice.
              </p>
              <Link to="/topics" className="btn btn-primary" style={{ marginTop: '16px' }}>
                Start Self-Assessment
              </Link>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {recentAssessments.map(item => (
                <div key={item.topic_id} style={{
                  padding: '16px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  borderRadius: '12px',
                  border: '1px solid var(--border-subtle)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <div>
                    <h4 style={{ fontWeight: 600, fontSize: '1rem', marginBottom: '4px' }}>{item.topic_name}</h4>
                    <div style={{ display: 'flex', gap: '12px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      <span>Confidence: <strong>{item.confidence}%</strong></span>
                      <span>Quiz: <strong>{item.quizScore}</strong></span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span className={`badge ${
                      item.grip === 'Needs Revision' ? 'badge-low' :
                      item.grip === 'Developing' ? 'badge-mod' :
                      item.grip === 'Demonstrated Mastery' ? 'badge-high' : 'badge-info'
                    }`}>
                      {item.grip}
                    </span>

                    {item.needsRevision ? (
                      <Link to={`/revision/${item.topic_id}`} className="btn btn-secondary" style={{ fontSize: '0.8rem', padding: '6px 12px' }}>
                        Revise
                      </Link>
                    ) : (
                      <Link to={`/quiz/${item.topic_id}`} className="btn btn-primary" style={{ fontSize: '0.8rem', padding: '6px 12px' }}>
                        Quiz
                      </Link>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Action Center & Recommendations */}
        <div className="card">
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '16px' }}>Recommended Next Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{
              padding: '16px',
              borderRadius: '12px',
              background: 'rgba(99, 102, 241, 0.08)',
              border: '1px solid rgba(99, 102, 241, 0.2)'
            }}>
              <span className="badge badge-info" style={{ marginBottom: '8px' }}>Action 1</span>
              <h4 style={{ fontWeight: 600, marginBottom: '4px' }}>Rate Topic Confidence</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                Assess your familiarity on technical skill topics using the 0-100 slider. Topics below 60% automatically unlock focused revision.
              </p>
            </div>

            <div style={{
              padding: '16px',
              borderRadius: '12px',
              background: 'rgba(245, 158, 11, 0.08)',
              border: '1px solid rgba(245, 158, 11, 0.2)'
            }}>
              <span className="badge badge-mod" style={{ marginBottom: '8px' }}>Action 2</span>
              <h4 style={{ fontWeight: 600, marginBottom: '4px' }}>Flip Revision Flashcards</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                Strengthen core concepts, definitions, and address common misconceptions before attempting the topic quiz.
              </p>
            </div>

            <div style={{
              padding: '16px',
              borderRadius: '12px',
              background: 'rgba(16, 185, 129, 0.08)',
              border: '1px solid rgba(16, 185, 129, 0.2)'
            }}>
              <span className="badge badge-high" style={{ marginBottom: '8px' }}>Action 3</span>
              <h4 style={{ fontWeight: 600, marginBottom: '4px' }}>Validate with Quiz Evidence</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                Demonstrate genuine knowledge through question-level performance to earn confirmed mastery status.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
