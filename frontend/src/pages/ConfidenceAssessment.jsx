import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { FALLBACK_CURRICULUM, logLearningEvent } from '../api';

export default function ConfidenceAssessment() {
  const { topicId } = useParams();
  const navigate = useNavigate();

  const allTopics = Object.values(FALLBACK_CURRICULUM.topics).flat();
  const topic = allTopics.find(t => t.topic_id === topicId) || {
    topic_id: topicId,
    topic_name: 'Selected Topic',
    description: 'Technical topic overview'
  };

  const [confidence, setConfidence] = useState(50);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    const existing = JSON.parse(localStorage.getItem('topic_confidence') || '{}');
    if (existing[topicId] !== undefined) {
      setConfidence(existing[topicId]);
    }
  }, [topicId]);

  const getBand = (val) => {
    if (val < 60) return { label: 'Low Confidence (Needs Attention)', class: 'badge-low', color: '#f87171' };
    if (val < 80) return { label: 'Moderate Confidence (Developing)', class: 'badge-mod', color: '#fbbf24' };
    return { label: 'High Confidence (Comfortable)', class: 'badge-high', color: '#34d399' };
  };

  const currentBand = getBand(confidence);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Persist in localStorage
    const existing = JSON.parse(localStorage.getItem('topic_confidence') || '{}');
    existing[topicId] = confidence;
    localStorage.setItem('topic_confidence', JSON.stringify(existing));

    // Log telemetry event
    await logLearningEvent({
      event_type: 'confidence_assessment_submitted',
      topic_id: topicId,
      confidence_score: confidence,
      confidence_band: confidence < 60 ? 'Low' : confidence < 80 ? 'Moderate' : 'High',
      threshold_applied: 60.0
    });

    setSubmitted(true);
  };

  return (
    <div style={{ maxWidth: '720px', margin: '0 auto' }}>
      <Link to="/topics" style={{ color: 'var(--text-secondary)', textDecoration: 'none', display: 'inline-block', marginBottom: '20px' }}>
        &larr; Back to Topics
      </Link>

      <div className="card">
        <span className="badge badge-info" style={{ marginBottom: '12px' }}>Self-Assessment</span>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '8px' }}>{topic.topic_name}</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '28px' }}>
          Rate how confident you feel explaining, deriving, and applying the principles of this topic.
        </p>

        {!submitted ? (
          <form onSubmit={handleSubmit}>
            <div className="slider-container" style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '24px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <span style={{ fontSize: '0.95rem', fontWeight: 600 }}>Your Confidence Rating:</span>
                <span style={{ fontSize: '1.8rem', fontWeight: 800, color: currentBand.color }}>{confidence}%</span>
              </div>

              <input
                type="range"
                min="0"
                max="100"
                value={confidence}
                onChange={(e) => setConfidence(parseInt(e.target.value))}
                className="confidence-range"
              />

              <div className="slider-labels">
                <span>0% (Completely New)</span>
                <span>50% (Partial Grasp)</span>
                <span>100% (Fully Mastered)</span>
              </div>

              <div style={{ marginTop: '18px' }}>
                <span className={`badge ${currentBand.class}`}>
                  {currentBand.label}
                </span>
              </div>
            </div>

            <div style={{ marginTop: '24px', display: 'flex', gap: '14px', alignItems: 'center' }}>
              <button type="submit" className="btn btn-primary" style={{ flex: 1, padding: '12px' }}>
                Save Confidence Score
              </button>
            </div>
          </form>
        ) : (
          <div style={{ textAlign: 'center', padding: '24px 0' }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              background: 'var(--success-bg)',
              color: 'var(--success)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '2rem',
              margin: '0 auto 16px'
            }}>
              ✓
            </div>
            <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '8px' }}>Confidence Score Saved: {confidence}%</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '28px', maxWidth: '500px', margin: '0 auto 28px' }}>
              {confidence < 60
                ? 'Your rating is below our 60% threshold. We strongly recommend completing the targeted revision and flashcards before taking the quiz.'
                : 'Great! You have reported solid confidence. You may either review the concepts or jump straight to the topic quiz to demonstrate mastery.'}
            </p>

            <div style={{ display: 'flex', gap: '14px', justifyContent: 'center' }}>
              <Link to={`/revision/${topicId}`} className="btn btn-primary">
                {confidence < 60 ? 'Start Revision & Flashcards' : 'Quick Revision'}
              </Link>
              <Link to={`/quiz/${topicId}`} className="btn btn-secondary">
                Take Quiz Directly
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
