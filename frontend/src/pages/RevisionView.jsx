import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { FALLBACK_CURRICULUM, logLearningEvent } from '../api';

export default function RevisionView() {
  const { topicId } = useParams();
  const navigate = useNavigate();

  const revision = FALLBACK_CURRICULUM.revisions[topicId] || {
    topic_id: topicId,
    topic_name: 'Topic Revision',
    summary: 'Essential concept summary: Review key mathematical definitions, objective formulations, and operational caveats before the assessment.',
    key_definitions: [
      { term: 'Core Concept', definition: 'The foundational theorem or empirical formula governing this topic.' },
      { term: 'Application Rule', definition: 'Guidelines for choosing appropriate hyperparameters and model architectures.' }
    ],
    flashcards: [
      { card_id: 'def_1', front: 'What is the primary objective of this module?', back: 'Establishing solid conceptual retention and empirical understanding.' },
      { card_id: 'def_2', front: 'How is performance evaluated?', back: 'Via objective multiple-choice questions with validated explanations.' }
    ]
  };

  const [cardIndex, setCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    logLearningEvent({
      event_type: 'revision_opened',
      topic_id: topicId
    });
  }, [topicId]);

  const currentCard = revision.flashcards[cardIndex] || revision.flashcards[0];

  const handleNextCard = () => {
    setIsFlipped(false);
    setCardIndex((prev) => (prev + 1) % revision.flashcards.length);
  };

  const handlePrevCard = () => {
    setIsFlipped(false);
    setCardIndex((prev) => (prev - 1 + revision.flashcards.length) % revision.flashcards.length);
  };

  const handleCompleteRevision = async () => {
    const durationSeconds = Math.round((Date.now() - startTime) / 1000);

    // Persist revision completion in localStorage
    const revHistory = JSON.parse(localStorage.getItem('completed_revisions') || '[]');
    if (!revHistory.includes(topicId)) {
      revHistory.push(topicId);
      localStorage.setItem('completed_revisions', JSON.stringify(revHistory));
    }

    await logLearningEvent({
      event_type: 'revision_completed',
      topic_id: topicId,
      cards_reviewed_count: revision.flashcards.length,
      duration_seconds: durationSeconds,
      revision_status: 'completed'
    });

    navigate(`/quiz/${topicId}`);
  };

  return (
    <div style={{ maxWidth: '840px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <Link to="/topics" style={{ color: 'var(--text-secondary)', textDecoration: 'none' }}>
          &larr; Back to Topics
        </Link>
        <span className="badge badge-info">Focused Revision</span>
      </div>

      <header style={{ marginBottom: '28px' }}>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, marginBottom: '8px' }}>{revision.topic_name}</h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Review the core principles and test your recall with interactive flashcards before starting the quiz.
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
          Key Terminology & Definitions:
        </h4>
        <div style={{ display: 'grid', gap: '10px' }}>
          {revision.key_definitions.map((item, idx) => (
            <div key={idx} style={{ padding: '12px 16px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '8px', borderLeft: '3px solid var(--accent-primary)' }}>
              <strong>{item.term}:</strong> <span style={{ color: 'var(--text-secondary)' }}>{item.definition}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Flashcard Component */}
      <div className="card" style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>
            Interactive Flashcards ({cardIndex + 1} of {revision.flashcards.length})
          </h3>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Click card to flip</span>
        </div>

        <div className="flashcard-wrapper" onClick={() => setIsFlipped(!isFlipped)}>
          <div className={`flashcard-inner ${isFlipped ? 'flipped' : ''}`}>
            {/* Front */}
            <div className="flashcard-front">
              <span className="badge badge-info" style={{ marginBottom: '16px' }}>Question / Prompt</span>
              <p style={{ fontSize: '1.15rem', fontWeight: 600, maxWidth: '600px' }}>
                {currentCard.front}
              </p>
              <span style={{ marginTop: '20px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                ↺ Click to reveal answer
              </span>
            </div>

            {/* Back */}
            <div className="flashcard-back">
              <span className="badge badge-high" style={{ marginBottom: '16px' }}>Explanation / Answer</span>
              <p style={{ fontSize: '1.1rem', color: '#e0e7ff', maxWidth: '600px' }}>
                {currentCard.back}
              </p>
              <span style={{ marginTop: '20px', fontSize: '0.85rem', color: 'rgba(255, 255, 255, 0.5)' }}>
                ↺ Click to return to question
              </span>
            </div>
          </div>
        </div>

        {/* Flashcard Controls */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px' }}>
          <button onClick={handlePrevCard} className="btn btn-secondary" style={{ padding: '8px 16px' }}>
            &larr; Previous Card
          </button>
          <button onClick={() => setIsFlipped(!isFlipped)} className="btn btn-outline" style={{ padding: '8px 16px' }}>
            Flip Card ↺
          </button>
          <button onClick={handleNextCard} className="btn btn-secondary" style={{ padding: '8px 16px' }}>
            Next Card &rarr;
          </button>
        </div>
      </div>

      {/* Completion CTA */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px', background: 'rgba(16, 185, 129, 0.08)', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
        <div>
          <h4 style={{ fontWeight: 700, color: '#34d399', marginBottom: '4px' }}>Ready to test your knowledge?</h4>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Mark revision as completed to update your learning record and start the topic quiz.
          </p>
        </div>
        <button onClick={handleCompleteRevision} className="btn btn-primary" style={{ background: 'var(--success)' }}>
          Start Topic Quiz &rarr;
        </button>
      </div>
    </div>
  );
}
