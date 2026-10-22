import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FALLBACK_CURRICULUM } from '../api';

export default function PerformanceAnalytics() {
  const [data, setData] = useState([]);
  const [telemetryEvents, setTelemetryEvents] = useState([]);

  useEffect(() => {
    const confidenceMap = JSON.parse(localStorage.getItem('topic_confidence') || '{}');
    const quizHistory = JSON.parse(localStorage.getItem('quiz_history') || '[]');
    const buffered = JSON.parse(localStorage.getItem('buffered_events') || '[]');

    const allTopics = Object.values(FALLBACK_CURRICULUM.topics).flat();

    const rows = allTopics.map(t => {
      const conf = confidenceMap[t.topic_id] ?? null;
      const topicQuizzes = quizHistory.filter(q => q.topic_id === t.topic_id);
      const latestQuiz = topicQuizzes[0] ?? null;
      const avgQuiz = topicQuizzes.length > 0
        ? Math.round(topicQuizzes.reduce((acc, q) => acc + q.score, 0) / topicQuizzes.length)
        : null;

      let calibration = 'Unassessed';
      if (conf !== null && latestQuiz !== null) {
        const gap = conf - latestQuiz.score;
        if (gap > 20) calibration = 'Overconfident (Gap > +20%)';
        else if (gap < -20) calibration = 'Underconfident (Gap < -20%)';
        else calibration = 'Well-Calibrated';
      }

      return {
        topic_id: t.topic_id,
        topic_name: t.topic_name,
        confidence: conf,
        latestQuizScore: latestQuiz ? latestQuiz.score : null,
        avgQuizScore: avgQuiz,
        attemptsCount: topicQuizzes.length,
        calibration
      };
    });

    setData(rows);
    setTelemetryEvents(buffered);
  }, []);

  return (
    <div className="analytics-page">
      <header style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, marginBottom: '8px' }}>
          Performance Calibration & Telemetry Analytics
        </h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Detailed comparison between self-reported confidence and demonstrated quiz performance.
        </p>
      </header>

      {/* Comparison Table */}
      <div className="card" style={{ marginBottom: '32px' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '16px' }}>Topic Knowledge Calibration</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.95rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '12px 16px' }}>Topic</th>
                <th style={{ padding: '12px 16px' }}>Confidence Score</th>
                <th style={{ padding: '12px 16px' }}>Latest Quiz Score</th>
                <th style={{ padding: '12px 16px' }}>Attempts</th>
                <th style={{ padding: '12px 16px' }}>Calibration Assessment</th>
              </tr>
            </thead>
            <tbody>
              {data.map(row => (
                <tr key={row.topic_id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                  <td style={{ padding: '14px 16px', fontWeight: 600 }}>{row.topic_name}</td>
                  <td style={{ padding: '14px 16px' }}>
                    {row.confidence !== null ? `${row.confidence}%` : <span style={{ color: 'var(--text-muted)' }}>Unrated</span>}
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    {row.latestQuizScore !== null ? `${row.latestQuizScore}%` : <span style={{ color: 'var(--text-muted)' }}>No Attempt</span>}
                  </td>
                  <td style={{ padding: '14px 16px' }}>{row.attemptsCount}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <span className={`badge ${
                      row.calibration.startsWith('Overconfident') ? 'badge-low' :
                      row.calibration === 'Well-Calibrated' ? 'badge-high' :
                      row.calibration.startsWith('Underconfident') ? 'badge-mod' : 'badge-info'
                    }`}>
                      {row.calibration}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* First-Party Telemetry Log View */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>First-Party Telemetry Event Stream</h3>
          <span className="badge badge-info">{telemetryEvents.length} Buffered Events</span>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '16px' }}>
          Real-time learning telemetry collected directly by the frontend during student actions.
        </p>

        {telemetryEvents.length === 0 ? (
          <div style={{ padding: '24px 0', textAlign: 'center', color: 'var(--text-muted)' }}>
            No telemetry events buffered yet. Complete a confidence rating or quiz to see live event logging.
          </div>
        ) : (
          <div style={{ maxHeight: '320px', overflowY: 'auto', background: 'rgba(0, 0, 0, 0.25)', padding: '16px', borderRadius: '10px', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
            {telemetryEvents.slice(-10).reverse().map((ev, idx) => (
              <div key={idx} style={{ marginBottom: '8px', paddingBottom: '8px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <span style={{ color: '#38bdf8' }}>[{ev.timestamp?.substring(11, 19)}]</span>{' '}
                <strong style={{ color: '#a855f7' }}>{ev.event_type}</strong>{' '}
                <span style={{ color: 'var(--text-muted)' }}>topic:</span> <span style={{ color: '#34d399' }}>{ev.topic_id}</span>{' '}
                {ev.confidence_score !== undefined && <span>score: {ev.confidence_score}</span>}
                {ev.quiz_score !== undefined && <span>result: {ev.quiz_score}%</span>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
