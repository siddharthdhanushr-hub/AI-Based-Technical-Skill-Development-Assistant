import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { FALLBACK_CURRICULUM, logLearningEvent } from '../api';

export default function QuizSession() {
  const { topicId } = useParams();
  const navigate = useNavigate();

  const questions = FALLBACK_CURRICULUM.quizzes[topicId] || [
    {
      question_id: 'q_gen_1',
      text: 'Which step is critical to prevent target leakage when preprocessing training data?',
      options: [
        'A. Fit transformations (e.g. scalers, encoders) strictly on the training partition only',
        'B. Impute missing values across the entire dataset before splitting',
        'C. Normalize test features using test set mean and standard deviation',
        'D. Compute target encoding on the combined train and test sets'
      ],
      correct_option: 'A',
      explanation: 'Fitting scalers, imputers, or encoders on data that includes the test partition leaks information about the validation distribution.'
    },
    {
      question_id: 'q_gen_2',
      text: 'Why is self-reported confidence alone inadequate for establishing topic mastery?',
      options: [
        'A. Uncalibrated self-assessment often diverges from demonstrated empirical problem-solving ability',
        'B. Students always under-report their true technical ability',
        'C. Confidence scores cannot be converted to numerical data',
        'D. Modern machine learning algorithms cannot consume continuous inputs'
      ],
      correct_option: 'A',
      explanation: 'Cognitive biases such as the Dunning-Kruger effect mean high confidence does not equal proven competence without empirical quiz verification.'
    }
  ];

  const [attemptId] = useState(`att_${Date.now()}`);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [scoreData, setScoreData] = useState(null);
  const [questionStartTime, setQuestionStartTime] = useState(Date.now());

  useEffect(() => {
    logLearningEvent({
      event_type: 'quiz_started',
      topic_id: topicId,
      attempt_id: attemptId,
      question_count: questions.length
    });
  }, [topicId, attemptId]);

  const currentQ = questions[currentIndex];

  const handleSelectOption = (optionKey) => {
    if (submitted) return;
    const responseTime = (Date.now() - questionStartTime) / 1000;

    setSelectedAnswers({
      ...selectedAnswers,
      [currentQ.question_id]: optionKey
    });

    logLearningEvent({
      event_type: 'question_answered',
      topic_id: topicId,
      attempt_id: attemptId,
      question_id: currentQ.question_id,
      selected_option: optionKey,
      response_time_seconds: responseTime
    });
  };

  const handleNextQuestion = () => {
    setQuestionStartTime(Date.now());
    setCurrentIndex((prev) => Math.min(prev + 1, questions.length - 1));
  };

  const handlePrevQuestion = () => {
    setQuestionStartTime(Date.now());
    setCurrentIndex((prev) => Math.max(prev - 1, 0));
  };

  const handleSubmitQuiz = async () => {
    let correctCount = 0;
    const feedback = questions.map((q) => {
      const selected = selectedAnswers[q.question_id];
      const isCorrect = selected === q.correct_option;
      if (isCorrect) correctCount++;
      return {
        question_id: q.question_id,
        selected,
        correct: q.correct_option,
        isCorrect,
        explanation: q.explanation
      };
    });

    const finalScore = Math.round((correctCount / questions.length) * 100);

    let readinessStatus = 'Developing';
    let recommendation = 'Review incorrect explanations and retest in 24 hours.';
    if (finalScore >= 80) {
      readinessStatus = 'Demonstrated Mastery';
      recommendation = 'Excellent work! You have proven strong technical command. Proceed to the next module.';
    } else if (finalScore < 60) {
      readinessStatus = 'Needs Revision';
      recommendation = 'Scores below 60% indicate foundational gaps. Review the flashcards and concept summaries.';
    }

    const calculatedData = {
      score: finalScore,
      correctCount,
      totalCount: questions.length,
      feedback,
      readinessStatus,
      recommendation
    };

    setScoreData(calculatedData);
    setSubmitted(true);

    // Save to local quiz history
    const quizHistory = JSON.parse(localStorage.getItem('quiz_history') || '[]');
    quizHistory.unshift({
      attempt_id: attemptId,
      topic_id: topicId,
      score: finalScore,
      readiness: readinessStatus,
      timestamp: new Date().toISOString()
    });
    localStorage.setItem('quiz_history', JSON.stringify(quizHistory));

    // Log telemetry events
    await logLearningEvent({
      event_type: 'quiz_submitted',
      topic_id: topicId,
      attempt_id: attemptId,
      quiz_score: finalScore
    });

    await logLearningEvent({
      event_type: 'quiz_result_calculated',
      topic_id: topicId,
      attempt_id: attemptId,
      quiz_score: finalScore,
      readiness_status: readinessStatus
    });
  };

  return (
    <div style={{ maxWidth: '840px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <Link to="/topics" style={{ color: 'var(--text-secondary)', textDecoration: 'none' }}>
          &larr; Back to Topics
        </Link>
        <span className="badge badge-info">Demonstrated Mastery Assessment</span>
      </div>

      {!submitted ? (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              Question {currentIndex + 1} of {questions.length}
            </span>
            <span style={{ fontSize: '0.85rem', color: 'var(--accent-light)' }}>
              Attempt ID: {attemptId.substring(0, 10)}
            </span>
          </div>

          <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '24px', lineHeight: 1.5 }}>
            {currentQ.text}
          </h3>

          <div style={{ marginBottom: '28px' }}>
            {currentQ.options.map((opt) => {
              const optKey = opt.charAt(0);
              const isSelected = selectedAnswers[currentQ.question_id] === optKey;
              return (
                <div
                  key={optKey}
                  onClick={() => handleSelectOption(optKey)}
                  className={`mcq-option ${isSelected ? 'selected' : ''}`}
                >
                  <div style={{
                    width: '28px',
                    height: '28px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: isSelected ? 'var(--accent-primary)' : 'rgba(255, 255, 255, 0.08)',
                    color: isSelected ? 'white' : 'var(--text-secondary)',
                    fontWeight: 700,
                    fontSize: '0.85rem'
                  }}>
                    {optKey}
                  </div>
                  <span style={{ fontSize: '0.95rem' }}>{opt.substring(3)}</span>
                </div>
              );
            })}
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button
              onClick={handlePrevQuestion}
              disabled={currentIndex === 0}
              className="btn btn-secondary"
              style={{ opacity: currentIndex === 0 ? 0.5 : 1 }}
            >
              &larr; Previous
            </button>

            {currentIndex < questions.length - 1 ? (
              <button onClick={handleNextQuestion} className="btn btn-primary">
                Next Question &rarr;
              </button>
            ) : (
              <button
                onClick={handleSubmitQuiz}
                disabled={Object.keys(selectedAnswers).length === 0}
                className="btn btn-primary"
                style={{ background: 'var(--success)' }}
              >
                Submit Quiz & Calculate Grip
              </button>
            )}
          </div>
        </div>
      ) : (
        /* Quiz Results View */
        <div>
          <div className="card" style={{ marginBottom: '24px', textAlign: 'center', padding: '36px 24px' }}>
            <span className="badge badge-info" style={{ marginBottom: '12px' }}>Evaluation Complete</span>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: scoreData.score >= 80 ? '#34d399' : scoreData.score >= 60 ? '#fbbf24' : '#f87171' }}>
              {scoreData.score}%
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', marginTop: '6px' }}>
              You answered {scoreData.correctCount} of {scoreData.totalCount} questions correctly.
            </p>

            <div style={{ marginTop: '20px', display: 'inline-flex', gap: '10px' }}>
              <span className={`badge ${
                scoreData.readinessStatus === 'Needs Revision' ? 'badge-low' :
                scoreData.readinessStatus === 'Developing' ? 'badge-mod' : 'badge-high'
              }`}>
                Readiness: {scoreData.readinessStatus}
              </span>
            </div>

            <div style={{ marginTop: '24px', padding: '16px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '12px', border: '1px solid var(--border-subtle)', maxWidth: '600px', margin: '24px auto 0' }}>
              <strong style={{ color: 'var(--accent-light)', display: 'block', marginBottom: '4px' }}>Recommended Next Action:</strong>
              <span style={{ fontSize: '0.95rem', color: 'var(--text-secondary)' }}>{scoreData.recommendation}</span>
            </div>
          </div>

          {/* Question Breakdown */}
          <div className="card" style={{ marginBottom: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: '20px' }}>Question Breakdown & Explanations</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {questions.map((q, idx) => {
                const fb = scoreData.feedback.find(f => f.question_id === q.question_id);
                return (
                  <div key={q.question_id} style={{
                    padding: '18px',
                    borderRadius: '12px',
                    background: fb?.isCorrect ? 'rgba(16, 185, 129, 0.04)' : 'rgba(239, 68, 68, 0.04)',
                    border: `1px solid ${fb?.isCorrect ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>Question {idx + 1}</span>
                      <span className={`badge ${fb?.isCorrect ? 'badge-high' : 'badge-low'}`}>
                        {fb?.isCorrect ? 'Correct' : 'Incorrect'}
                      </span>
                    </div>

                    <p style={{ fontWeight: 600, marginBottom: '12px' }}>{q.text}</p>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                      Your Answer: <strong>Option {fb?.selected || 'Skipped'}</strong> | Correct: <strong>Option {fb?.correct}</strong>
                    </p>
                    <div style={{ fontSize: '0.9rem', background: 'rgba(0, 0, 0, 0.2)', padding: '10px 14px', borderRadius: '8px', color: '#cbd5e1' }}>
                      💡 <strong>Explanation:</strong> {fb?.explanation}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: 'flex', gap: '14px', justifyContent: 'center' }}>
            <Link to="/dashboard" className="btn btn-secondary">
              View Dashboard Progress
            </Link>
            <Link to={`/revision/${topicId}`} className="btn btn-primary">
              Review Topic Flashcards
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
