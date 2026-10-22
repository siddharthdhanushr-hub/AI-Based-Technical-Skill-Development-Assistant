import { useState } from 'react';
import { Link } from 'react-router-dom';
import { FALLBACK_CURRICULUM, logLearningEvent } from '../api';

export default function TopicSelection() {
  const [selectedSubject, setSelectedSubject] = useState(FALLBACK_CURRICULUM.subjects[0].subject_id);

  const currentTopics = FALLBACK_CURRICULUM.topics[selectedSubject] || [];
  const savedConfidence = JSON.parse(localStorage.getItem('topic_confidence') || '{}');

  const handleSelectTopic = (topicId) => {
    logLearningEvent({
      event_type: 'topic_selected',
      topic_id: topicId,
      subject_id: selectedSubject
    });
  };

  return (
    <div className="topic-selection-page">
      <header style={{ marginBottom: '32px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, marginBottom: '8px' }}>Course & Topic Curriculum</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Browse technical domains, review topic syllabi, and calibrate your self-confidence scores.
        </p>
      </header>

      {/* Subject Filter Tabs */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '28px' }}>
        {FALLBACK_CURRICULUM.subjects.map(sub => (
          <button
            key={sub.subject_id}
            onClick={() => setSelectedSubject(sub.subject_id)}
            className={`btn ${selectedSubject === sub.subject_id ? 'btn-primary' : 'btn-secondary'}`}
          >
            {sub.subject_name}
          </button>
        ))}
      </div>

      {/* Topics Grid */}
      <div className="grid-2">
        {currentTopics.map(topic => {
          const confidence = savedConfidence[topic.topic_id];
          return (
            <div key={topic.topic_id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <span className="badge badge-info">{topic.difficulty}</span>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>⏱ ~{topic.estimated_minutes} mins</span>
                </div>

                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '8px' }}>{topic.topic_name}</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', marginBottom: '20px' }}>
                  {topic.description}
                </p>
              </div>

              <div>
                <div style={{
                  padding: '12px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  borderRadius: '10px',
                  border: '1px solid var(--border-subtle)',
                  marginBottom: '16px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Current Confidence:</span>
                  <span style={{
                    fontWeight: 700,
                    color: confidence === undefined ? 'var(--text-muted)' : confidence < 60 ? '#f87171' : '#34d399'
                  }}>
                    {confidence !== undefined ? `${confidence}%` : 'Unrated'}
                  </span>
                </div>

                <div style={{ display: 'flex', gap: '10px' }}>
                  <Link
                    to={`/confidence/${topic.topic_id}`}
                    onClick={() => handleSelectTopic(topic.topic_id)}
                    className="btn btn-primary"
                    style={{ flex: 1, fontSize: '0.9rem' }}
                  >
                    Rate Confidence
                  </Link>

                  <Link
                    to={`/revision/${topic.topic_id}`}
                    onClick={() => handleSelectTopic(topic.topic_id)}
                    className="btn btn-secondary"
                    style={{ fontSize: '0.9rem' }}
                  >
                    Revision
                  </Link>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
