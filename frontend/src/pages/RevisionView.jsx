import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { FALLBACK_CURRICULUM, logLearningEvent, fetchTopicRevision } from '../api';

export default function RevisionView() {
  const { topicId } = useParams();
  const navigate = useNavigate();

  const [revision, setRevision] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cardIndex, setCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    const loadContent = async () => {
      setLoading(true);
      const data = await fetchTopicRevision(topicId);
      setRevision(data || {
        topic_id: topicId,
        topic_name: 'Topic Targeted Revision',
        summary: 'Essential concept summary: Review key mathematical formulations and empirical principles before beginning the quiz.',
        key_definitions: [
          { term: 'Foundational Theory', definition: 'The core operational principles and statistical assumptions governing this domain.' },
          { term: 'Evaluation Standard', definition: 'Objective metrics used to distinguish mastery from random performance.' }
        ],
        flashcards: [
          { card_id: 'def_1', front: 'What is the goal of this topic assessment?', back: 'Demonstrating solid conceptual retention and empirical understanding.' },
          { card_id: 'def_2', front: 'How is student readiness established?', back: 'By answering validated multiple-choice questions with instant explanatory feedback.' }
        ]
      });
      setLoading(false);
    };

    loadContent();

    logLearningEvent({
      event_type: 'revision_opened',
      topic_id: topicId
    });
  }, [topicId]);

  // Flashcard controls
  const handleNextCard = useCallback(() => {
    if (!revision?.flashcards?.length) return;
    setIsFlipped(false);
    setCardIndex((prev) => (prev + 1) % revision.flashcards.length);
  }, [revision]);

  const handlePrevCard = useCallback(() => {
    if (!revision?.flashcards?.length) return;
    setIsFlipped(false);
    setCardIndex((prev) => (prev - 1 + revision.flashcards.length) % revision.flashcards.length);
  }, [revision]);

  const handleToggleFlip = useCallback(() => {
    setIsFlipped((prev) => !prev);
  }, []);

  // Keyboard accessibility: Space to flip, Arrow keys to navigate
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Space') {
        e.preventDefault();
        handleToggleFlip();
      } else if (e.code === 'ArrowRight') {
        handleNextCard();
      } else if (e.code === 'ArrowLeft') {
        handlePrevCard();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleToggleFlip, handleNextCard, handlePrevCard]);

  const handleCompleteRevision = async () => {
    const durationSeconds = Math.round((Date.now() - startTime) / 1000);

    // Save completion record in localStorage
    const revHistory = JSON.parse(localStorage.getItem('completed_revisions') || '[]');
    if (!revHistory.includes(topicId)) {
      revHistory.push(topicId);
      localStorage.setItem('completed_revisions', JSON.stringify(revHistory));
    }

    await logLearningEvent({
      event_type: 'revision_completed',
      topic_id: topicId,
      cards_reviewed_count: revision?.flashcards?.length || 0,
      duration_seconds: durationSeconds,
      revision_status: 'completed'
    });

    navigate(`/quiz/${topicId}`);
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 0' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Loading topic revision materials...</p>
      </div>
    );
  }

  const currentCard = revision?.flashcards?.[cardIndex] || { front: '', back: '' };

  return (
    <div style={{ maxWidth: '840px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <Link to="/topics" style={{ color: 'var(--text-secondary)', textDecoration: 'none' }}>
          &larr; Back to Topics
        </Link>
        <span className="badge badge-info">Focused Revision Section</span>
      </div>

      <header style={{ marginBottom: '28px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, marginBottom: '8px' }}>{revision.topic_name}</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Review key concepts and test recall with interactive flashcards before taking the topic quiz.
        </p>
      </header>

      {/* Concept Summary Card */}
      <div className="card" style={{ marginBottom: '28px' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>📖</span> Concept Summary
        </h3>
        <p style={{ color: 'var(--text-primary)', lineHeight: 1.7, marginBottom: '20px' }}>
          {revision.summary}
        </p>

        <h4 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--accent-light)', marginBottom: '12px' }}>
          Key Principles & Definitions:
        </h4>
        <div style={{ display: 'grid', gap: '10px' }}>
          {revision.key_definitions.map((item, idx) => (
            <div key={idx} style={{ padding: '12px 16px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px', borderLeft: '3px solid var(--accent-primary)' }}>
              <strong>{item.term}:</strong> <span style={{ color: 'var(--text-secondary)' }}>{item.definition}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Interactive Flashcard Component */}
      <div className="card" style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>
            Interactive Flashcards ({cardIndex + 1} of {revision.flashcards.length})
          </h3>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Keyboard: <strong>Space</strong> (Flip) | <strong>&larr; &rarr;</strong> (Navigate)
          </span>
        </div>

        <div
          className="flashcard-wrapper"
          onClick={handleToggleFlip}
          tabIndex={0}
          role="button"
          aria-label="Interactive flashcard. Press space or click to flip."
        >
          <div className={`flashcard-inner ${isFlipped ? 'flipped' : ''}`}>
            {/* Front */}
            <div className="flashcard-front">
              <span className="badge badge-info" style={{ marginBottom: '16px' }}>Question / Prompt</span>
              <p style={{ fontSize: '1.2rem', fontWeight: 600, maxWidth: '640px', lineHeight: 1.6 }}>
                {currentCard.front}
              </p>
              <span style={{ marginTop: '20px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                ↺ Click card or press Space to reveal answer
              </span>
            </div>

            {/* Back */}
            <div className="flashcard-back">
              <span className="badge badge-high" style={{ marginBottom: '16px' }}>Explanation / Answer</span>
              <p style={{ fontSize: '1.15rem', color: '#e0e7ff', maxWidth: '640px', lineHeight: 1.6 }}>
                {currentCard.back}
              </p>
              <span style={{ marginTop: '20px', fontSize: '0.85rem', color: 'rgba(255, 255, 255, 0.5)' }}>
                ↺ Click card or press Space to view question
              </span>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px' }}>
          <button onClick={handlePrevCard} className="btn btn-secondary" style={{ padding: '8px 16px' }}>
            &larr; Previous Card
          </button>
          <button onClick={handleToggleFlip} className="btn btn-outline" style={{ padding: '8px 16px' }}>
            Flip Card ↺
          </button>
          <button onClick={handleNextCard} className="btn btn-secondary" style={{ padding: '8px 16px' }}>
            Next Card &rarr;
          </button>
        </div>
      </div>

      {/* Completion Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 24px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.25)' }}>
        <div>
          <h4 style={{ fontWeight: 700, color: '#34d399', marginBottom: '4px' }}>Ready to demonstrate mastery?</h4>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Mark revision as completed to update your learning record and launch the topic quiz.
          </p>
        </div>
        <button onClick={handleCompleteRevision} className="btn btn-primary" style={{ background: 'var(--success)' }}>
          Start Topic Quiz &rarr;
        </button>
      </div>
    </div>
  );
}
