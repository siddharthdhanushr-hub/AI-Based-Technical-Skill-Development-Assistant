import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const renderMarkdown = (text) => {
  if (!text) return { __html: "" };
  let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  formatted = formatted.replace(/^\s*\*\s+(.*)$/gm, '• $1');
  formatted = formatted.replace(/###\s+(.*)$/gm, '<h3 style="margin: 12px 0 6px 0; color: #1e293b;">$1</h3>');
  formatted = formatted.replace(/####\s+(.*)$/gm, '<h4 style="margin: 10px 0 4px 0; color: #334155;">$1</h4>');
  return { __html: formatted };
};

function StudyTracker() {
  const [subjects, setSubjects] = useState([]);
  const [activeSubject, setActiveSubject] = useState(null);
  const [aiContent, setAiContent] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const navigate = useNavigate();

  const fetchSubjects = async () => {
    try {
      const res = await api.get('/syllabus/subjects');
      setSubjects(res.data);
      if (res.data.length > 0 && activeSubject === null) {
        setActiveSubject(res.data[0].subject_id);
      }
    } catch (err) {
      console.error("Failed to load subjects:", err);
    }
  };

  useEffect(() => {
    fetchSubjects();
  }, []);

  // Toggle topic completion directly
  const handleToggleTopic = async (topicId) => {
    try {
      await api.put(`/syllabus/topics/${topicId}/toggle-complete`);
      // Update local state smoothly
      setSubjects(prevSubjects =>
        prevSubjects.map(sub => ({
          ...sub,
          topics: sub.topics.map(t =>
            t.topic_id === topicId ? { ...t, is_completed: !t.is_completed } : t
          )
        }))
      );
    } catch (err) {
      alert("Failed to update topic status");
    }
  };

  // Calculate per-subject stats
  const getSubjectStats = (subject) => {
    const topics = subject.topics || [];
    const total = topics.length;
    const completed = topics.filter(t => t.is_completed).length;
    const completionPct = total > 0 ? Math.round((completed / total) * 100) : 0;
    const totalMinutes = topics
      .filter(t => t.is_completed)
      .reduce((sum, t) => sum + Math.round((t.estimated_hours || 2.0) * 60), 0);
    return { total, completed, completionPct, totalMinutes };
  };

  const handleAIAction = async (type, topicId) => {
    setAiLoading(true);
    setAiContent(null);
    try {
      const res = await api.post(`/ai/${type}/${topicId}`);
      setAiContent({ type, data: res.data });
    } catch (err) {
      alert(err.response?.data?.detail || `Failed to generate ${type}.`);
    } finally {
      setAiLoading(false);
    }
  };

  const handleSubjectAI = async (type, payload) => {
    setAiLoading(true);
    setAiContent(null);
    try {
      let res;
      if (type === 'project-ideas') {
        res = await api.post(`/ai/project-ideas/${payload.subject_id}`);
      } else {
        res = await api.post(`/ai/${type}`, payload);
      }
      setAiContent({ type, data: res.data });
    } catch (err) {
      alert(err.response?.data?.detail || `Failed to generate ${type}.`);
    } finally {
      setAiLoading(false);
    }
  };

  const downloadPDF = async () => {
    if (!aiContent) return;
    
    try {
      const jspdfModule = await new Promise((resolve, reject) => {
        if (window.jspdf) {
          resolve(window.jspdf);
          return;
        }
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
        script.onload = () => resolve(window.jspdf);
        script.onerror = (e) => reject(e);
        document.body.appendChild(script);
      });

      const { jsPDF } = jspdfModule;
      const doc = new jsPDF();
      const title = `${aiContent.type.toUpperCase()} - ${aiContent.data.topic_name || activeSubObj?.subject_name || 'Study Resource'}`;
      const filename = `${(aiContent.data.topic_name || activeSubObj?.subject_name || 'Study_Resource').replace(/[^a-z0-9]/gi, '_')}_${aiContent.type}.pdf`;

      doc.setFont("helvetica", "bold");
      doc.setFontSize(16);
      doc.text(title, 15, 18);
      
      doc.setFont("helvetica", "normal");
      doc.setFontSize(11);
      
      let yOffset = 28;
      const pageHeight = doc.internal.pageSize.height;
      
      const writeLine = (text, style = "normal", isBold = false) => {
        doc.setFont("helvetica", isBold ? "bold" : "normal");
        const lines = doc.splitTextToSize(String(text || ''), 180);
        lines.forEach(line => {
          if (yOffset > pageHeight - 15) {
            doc.addPage();
            yOffset = 15;
          }
          doc.text(line, 15, yOffset);
          yOffset += 6;
        });
      };

      if (aiContent.type === 'summary') {
        writeLine(aiContent.data.summary);
      } else if (aiContent.type === 'explanation') {
        writeLine(aiContent.data.explanation);
      } else if (aiContent.type === 'hints') {
        aiContent.data.hints.forEach((hint, i) => {
          writeLine(`${i + 1}. ${hint}`);
          yOffset += 2;
        });
      } else if (aiContent.type === 'flashcards') {
        aiContent.data.flashcards.forEach((card, i) => {
          writeLine(`Card ${i + 1}:`, "normal", true);
          writeLine(`Front: ${card.front}`);
          writeLine(`Back: ${card.back}`);
          yOffset += 4;
        });
      } else if (aiContent.type === 'wellness') {
        writeLine(`Wellness Tip:`, "normal", true);
        writeLine(aiContent.data.wellness_tip);
        yOffset += 4;
        writeLine(`Motivation Quote:`, "normal", true);
        writeLine(`"${aiContent.data.motivation_quote}"`);
        yOffset += 4;
        writeLine(`Break Activity:`, "normal", true);
        writeLine(aiContent.data.break_activity);
        yOffset += 4;
        writeLine(`Health Reminder:`, "normal", true);
        writeLine(aiContent.data.health_reminder);
      } else if (aiContent.type === 'study-strategy') {
        writeLine(`Strategy Summary:`, "normal", true);
        writeLine(aiContent.data.strategy_summary);
        yOffset += 4;
        if (aiContent.data.topic_order) {
          writeLine(`Recommended Topic Order:`, "normal", true);
          aiContent.data.topic_order.forEach((t, i) => {
            writeLine(`${i + 1}. ${t}`);
          });
          yOffset += 4;
        }
        if (aiContent.data.time_allocation) {
          writeLine(`Time Allocation:`, "normal", true);
          aiContent.data.time_allocation.forEach(a => {
            writeLine(`• ${a.topic}: ${a.hours}h - Technique: ${a.technique || 'N/A'}`);
          });
          yOffset += 4;
        }
        if (aiContent.data.revision_tips) {
          writeLine(`Revision Tips:`, "normal", true);
          aiContent.data.revision_tips.forEach(tip => {
            writeLine(`• ${tip}`);
          });
          yOffset += 4;
        }
        if (aiContent.data.motivation) {
          writeLine(`Motivation Note:`, "normal", true);
          writeLine(aiContent.data.motivation);
        }
      } else if (aiContent.type === 'mocktest') {
        aiContent.data.questions.forEach((q, i) => {
          writeLine(`Q${i + 1}. ${q.question_text} (${q.difficulty || 'Medium'})`, "normal", true);
          writeLine(`A. ${q.option_a}`);
          writeLine(`B. ${q.option_b}`);
          writeLine(`C. ${q.option_c}`);
          writeLine(`D. ${q.option_d}`);
          writeLine(`Correct Option: ${q.correct_option}`, "normal", true);
          writeLine(`Explanation: ${q.explanation}`);
          yOffset += 4;
        });
      } else if (aiContent.type === 'project-ideas') {
        const projects = aiContent.data.projects || [];
        writeLine(`Portfolio Projects for ${aiContent.data.subject_name || 'Skill Track'}`, "normal", true);
        yOffset += 2;
        projects.forEach((proj, i) => {
          writeLine(`Project ${i + 1}: ${proj.title} (${proj.level})`, "normal", true);
          writeLine(`Tech Stack: ${proj.tech_stack}`);
          writeLine(`Description: ${proj.description}`);
          writeLine(`Key Deliverables:`, "normal", true);
          (proj.key_deliverables || []).forEach(d => writeLine(`  • ${d}`));
          writeLine(`Portfolio Impact: ${proj.portfolio_impact}`);
          yOffset += 4;
        });
      }

      doc.save(filename);
    } catch (err) {
      alert("Failed to download PDF: " + err.message);
    }
  };

  const activeSubObj = subjects.find(s => s.subject_id === activeSubject) || subjects[0];

  // Global calculations
  const allTopics = subjects.flatMap(s => s.topics || []);
  const allCompleted = allTopics.filter(t => t.is_completed).length;
  const overallPct = allTopics.length > 0 ? Math.round((allCompleted / allTopics.length) * 100) : 0;
  const totalMinsStudied = allTopics.filter(t => t.is_completed).reduce((sum, t) => sum + Math.round((t.estimated_hours || 2) * 60), 0);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ margin: 0 }}>📊 Technical Skill Tracker</h1>
          <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)' }}>
            Track competency mastery, verify hands-on skills, and generate AI portfolio projects & assessments.
          </p>
        </div>
        <button className="btn" onClick={() => navigate('/skills')} style={{ background: '#3b82f6' }}>
          🛠️ Skill Manager
        </button>
      </div>

      {/* Top Progress Banner */}
      <div style={{
        background: 'linear-gradient(135deg, #1e293b, #0f172a)',
        color: '#fff',
        padding: '20px 24px',
        borderRadius: '16px',
        marginBottom: '28px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px',
        boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'
      }}>
        <div style={{ minWidth: '220px' }}>
          <span style={{ fontSize: '0.85rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Overall Competency Mastery</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#38bdf8' }}>{overallPct}% Mastered</div>
          <div style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>{allCompleted} of {allTopics.length} competencies verified</div>
        </div>

        <div style={{ display: 'flex', gap: '32px', flexWrap: 'wrap' }}>
          <div>
            <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#34d399' }}>{subjects.length}</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Skill Tracks</div>
          </div>
          <div>
            <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#fbbf24' }}>{allTopics.length}</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Total Competencies</div>
          </div>
          <div>
            <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#a78bfa' }}>{Math.round(totalMinsStudied / 60)} hrs</div>
            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Hands-on Hours Logged</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2">
        {/* Left: Skill Tracks Overview */}
        <div className="glass-panel" style={{ alignSelf: 'start' }}>
          <h2 style={{ marginBottom: '16px' }}>🛠️ Skill Tracks</h2>

          {subjects.length === 0 ? (
            <div style={{ background: '#f9fafb', padding: '24px', borderRadius: '12px', border: '1px solid var(--border-color)', textAlign: 'center' }}>
              <p>No skill tracks found. Add your technical tracks to start tracking!</p>
              <button className="btn" onClick={() => navigate('/skills')} style={{ marginTop: '12px' }}>
                Go to Skill Manager
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {subjects.map(sub => {
                const stats = getSubjectStats(sub);
                const isActive = activeSubObj?.subject_id === sub.subject_id;
                return (
                  <div
                    key={sub.subject_id}
                    onClick={() => setActiveSubject(sub.subject_id)}
                    style={{
                      background: isActive ? '#eff6ff' : '#fff',
                      padding: '16px',
                      borderRadius: '12px',
                      border: isActive ? '2px solid var(--accent-color)' : '1px solid var(--border-color)',
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      boxShadow: isActive ? '0 4px 6px -1px rgba(59, 130, 246, 0.1)' : 'none'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <h3 style={{ margin: 0, fontSize: '1.05rem', color: isActive ? '#1d4ed8' : '#1e293b' }}>
                        {sub.subject_name}
                      </h3>
                      <span style={{ fontSize: '0.8rem', fontWeight: 600, color: stats.completionPct === 100 ? '#166534' : 'var(--text-secondary)' }}>
                        {stats.completed}/{stats.total} done ({stats.completionPct}%)
                      </span>
                    </div>

                    {/* Progress bar */}
                    <div style={{ background: '#e5e7eb', borderRadius: '999px', height: '8px', overflow: 'hidden', marginBottom: '8px' }}>
                      <div style={{
                        background: stats.completionPct === 100 ? '#10b981' : stats.completionPct >= 50 ? 'var(--accent-color)' : '#f59e0b',
                        height: '100%',
                        width: `${stats.completionPct}%`,
                        borderRadius: '999px',
                        transition: 'width 0.4s'
                      }} />
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                      <span>{stats.totalMinutes} mins practiced</span>
                      <span style={{ color: isActive ? '#2563eb' : '#64748b', fontWeight: isActive ? 600 : 400 }}>
                        {isActive ? '● Active Track' : 'Click to View →'}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right: Competencies & AI Tools */}
        <div className="glass-panel" style={{ alignSelf: 'start' }}>
          {!activeSubObj ? (
            <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-secondary)' }}>
              <p style={{ fontSize: '1.1rem' }}>Select a skill track to view competencies and tools.</p>
            </div>
          ) : (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid var(--border-color)', paddingBottom: '16px', marginBottom: '20px' }}>
                <div>
                  <h2 style={{ margin: '0 0 4px 0' }}>
                    <span style={{ color: 'var(--accent-color)' }}>{activeSubObj.subject_name}</span> Competencies
                  </h2>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    {activeSubObj.topics?.length || 0} technical skills in this domain
                  </span>
                </div>
                
                {activeSubObj.topics?.length > 0 && (
                  <button 
                    className="btn" 
                    onClick={() => navigate('/quiz', { state: { topicIds: activeSubObj.topics.map(t => t.topic_id) } })}
                    style={{ background: '#4f46e5', fontSize: '0.85rem', padding: '6px 12px' }}
                  >
                    🧠 Practice Quiz (10 Qs)
                  </button>
                )}
              </div>

              {/* Subject-Level AI Actions */}
              {activeSubObj.topics?.length > 0 && (
                <div style={{
                  background: '#f8fafc',
                  padding: '14px',
                  borderRadius: '12px',
                  border: '1px solid var(--border-color)',
                  marginBottom: '20px'
                }}>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569', marginBottom: '10px' }}>
                    ⚡ AI Technical Skill Suite:
                  </div>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    <button
                      className="btn"
                      style={{ fontSize: '0.85rem', background: '#2563eb', flex: '1 1 auto' }}
                      disabled={aiLoading}
                      onClick={() => handleSubjectAI('project-ideas', { subject_id: activeSubObj.subject_id })}
                    >
                      🚀 Real-world Projects
                    </button>
                    <button
                      className="btn"
                      style={{ fontSize: '0.85rem', background: '#059669', flex: '1 1 auto' }}
                      disabled={aiLoading}
                      onClick={() => handleSubjectAI('mocktest', { subject_id: activeSubObj.subject_id, num_questions: 10 })}
                    >
                      🎯 Skill Assessment (10 Qs)
                    </button>
                    <button
                      className="btn"
                      style={{ fontSize: '0.85rem', background: '#7c3aed', flex: '1 1 auto' }}
                      disabled={aiLoading}
                      onClick={() => handleSubjectAI('study-strategy', { subject_id: activeSubObj.subject_id, days_until_exam: 14, hours_per_day: 3 })}
                    >
                      🗺️ Mastery Roadmap
                    </button>
                    <button
                      className="btn"
                      style={{ fontSize: '0.85rem', background: '#ec4899', flex: '1 1 auto' }}
                      disabled={aiLoading}
                      onClick={() => handleSubjectAI('wellness', { study_hours_today: 2, days_until_exam: 14 })}
                    >
                      💡 Performance Coach
                    </button>
                  </div>
                </div>
              )}

              {/* Topics List */}
              {(!activeSubObj.topics || activeSubObj.topics.length === 0) ? (
                <div style={{ background: '#fefce8', padding: '16px', borderRadius: '12px', border: '1px solid #fde68a', textAlign: 'center' }}>
                  <p style={{ margin: 0 }}>No competencies added yet. Add skills in Skill Manager.</p>
                  <button className="btn" onClick={() => navigate('/skills')} style={{ marginTop: '10px', fontSize: '0.85rem' }}>
                    Add Skills Now
                  </button>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {activeSubObj.topics.map(topic => {
                    const isDone = Boolean(topic.is_completed);

                    return (
                      <div
                        key={topic.topic_id}
                        style={{
                          background: isDone ? '#f0fdf4' : '#fff',
                          padding: '16px',
                          borderRadius: '12px',
                          border: isDone ? '1px solid #86efac' : '1px solid var(--border-color)',
                          transition: 'all 0.2s',
                          boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                          <h4 style={{ margin: 0, fontSize: '1rem', color: isDone ? '#166534' : '#1e293b' }}>
                            {isDone && '✓ '}{topic.topic_name}
                          </h4>
                          
                          {/* Toggle Completion Button */}
                          <button
                            onClick={() => handleToggleTopic(topic.topic_id)}
                            style={{
                              background: isDone ? '#dcfce7' : '#f1f5f9',
                              color: isDone ? '#166534' : '#475569',
                              border: isDone ? '1px solid #86efac' : '1px solid #cbd5e1',
                              padding: '5px 12px',
                              borderRadius: '20px',
                              cursor: 'pointer',
                              fontSize: '0.8rem',
                              fontWeight: 600,
                              display: 'flex',
                              alignItems: 'center',
                              gap: '6px',
                              transition: 'all 0.2s'
                            }}
                          >
                            {isDone ? '✅ Completed' : '⬜ Mark Done'}
                          </button>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                          <span>Difficulty: {topic.difficulty_weight || 2}/5</span>
                          <span>Est. {topic.estimated_hours || 2}h</span>
                          <span style={{ color: isDone ? '#16a34a' : '#d97706', fontWeight: 600 }}>
                            {isDone ? 'Mastered' : 'In Progress'}
                          </span>
                        </div>

                        {/* AI Action Buttons for Topic */}
                        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                          <button
                            className="btn"
                            style={{ padding: '5px 12px', fontSize: '0.78rem', background: '#4f46e5' }}
                            disabled={aiLoading}
                            onClick={() => handleAIAction('summary', topic.topic_id)}
                          >
                            📚 Skill Brief
                          </button>
                          <button
                            className="btn"
                            style={{ padding: '5px 12px', fontSize: '0.78rem', background: '#0284c7' }}
                            disabled={aiLoading}
                            onClick={() => handleAIAction('flashcards', topic.topic_id)}
                          >
                            🎴 Flashcards
                          </button>
                          <button
                            className="btn"
                            style={{ padding: '5px 12px', fontSize: '0.78rem', background: '#d97706' }}
                            disabled={aiLoading}
                            onClick={() => handleAIAction('hints', topic.topic_id)}
                          >
                            💡 Key Patterns
                          </button>
                          <button
                            className="btn"
                            style={{ padding: '5px 12px', fontSize: '0.78rem', background: '#7c3aed' }}
                            disabled={aiLoading}
                            onClick={() => handleAIAction('explanation', topic.topic_id)}
                          >
                            🔬 Deep Dive
                          </button>
                          <button
                            className="btn"
                            style={{ padding: '5px 12px', fontSize: '0.78rem', background: '#10b981' }}
                            onClick={() => navigate('/quiz', { state: { topicId: topic.topic_id } })}
                          >
                            🎯 Quiz (10 Qs)
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {/* AI Content Modal Overlay */}
      {(aiLoading || aiContent) && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(15, 23, 42, 0.65)',
            backdropFilter: 'blur(4px)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000,
            padding: '20px'
          }}
          onClick={() => { if (!aiLoading) setAiContent(null); }}
        >
          <div
            style={{
              background: '#fff',
              borderRadius: '16px',
              width: '100%',
              maxWidth: '680px',
              maxHeight: '85vh',
              overflowY: 'auto',
              padding: '24px',
              boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04)',
              position: 'relative',
              display: 'flex',
              flexDirection: 'column'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {aiLoading ? (
              <div style={{ textAlign: 'center', padding: '40px 0' }}>
                <div style={{
                  border: '4px solid #f3f3f3',
                  borderTop: '4px solid var(--accent-color)',
                  borderRadius: '50%',
                  width: '40px',
                  height: '40px',
                  animation: 'spin 1s linear infinite',
                  margin: '0 auto 16px auto'
                }}></div>
                <h3 style={{ margin: 0, color: 'var(--accent-color)' }}>Generating with AI Engine...</h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '8px', marginBottom: 0 }}>
                  Crafting study materials and questions for you...
                </p>
              </div>
            ) : (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
                  <h3 style={{ margin: 0, fontSize: '1.2rem', color: '#1e293b' }}>
                    {aiContent.type === 'summary' && '📚 Skill Summary & Core Concepts'}
                    {aiContent.type === 'flashcards' && '🎴 Technical Flashcards'}
                    {aiContent.type === 'hints' && '💡 Key Engineering Patterns'}
                    {aiContent.type === 'explanation' && '🔬 Deep Dive & Real-World Concepts'}
                    {aiContent.type === 'study-strategy' && '🗺️ Skill Mastery Roadmap'}
                    {aiContent.type === 'wellness' && '💡 Performance & Energy Coach'}
                    {aiContent.type === 'mocktest' && '🎯 Skill Assessment Exam (10 Questions)'}
                    {aiContent.type === 'project-ideas' && `🚀 Portfolio Projects — ${aiContent.data.subject_name || ''}`}
                    {aiContent.data.topic_name ? ` — ${aiContent.data.topic_name}` : ''}
                  </h3>
                  <button onClick={() => setAiContent(null)} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.5rem', color: '#94a3b8', padding: 0 }}>&times;</button>
                </div>

                <div style={{ flex: 1, overflowY: 'auto', marginBottom: '20px', paddingRight: '4px' }}>
                  {/* Summary */}
                  {aiContent.type === 'summary' && (
                    <div>
                      <div style={{ lineHeight: 1.7, fontSize: '0.95rem', marginBottom: '20px' }} dangerouslySetInnerHTML={renderMarkdown(aiContent.data.summary)} />
                      <div style={{ background: '#f8fafc', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                        <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9rem', color: '#475569' }}>🌐 Verified References:</h4>
                        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                          <a href={`https://www.google.com/search?q=${encodeURIComponent(aiContent.data.topic_name || '')}`} target="_blank" rel="noreferrer" className="btn" style={{ padding: '4px 10px', fontSize: '0.75rem', background: '#3b82f6', textDecoration: 'none', color: '#fff' }}>Google Search</a>
                          <a href={`https://en.wikipedia.org/wiki/Special:Search?search=${encodeURIComponent(aiContent.data.topic_name || '')}`} target="_blank" rel="noreferrer" className="btn" style={{ padding: '4px 10px', fontSize: '0.75rem', background: '#10b981', textDecoration: 'none', color: '#fff' }}>Wikipedia</a>
                          <a href={`https://www.geeksforgeeks.org/search/${encodeURIComponent(aiContent.data.topic_name || '')}`} target="_blank" rel="noreferrer" className="btn" style={{ padding: '4px 10px', fontSize: '0.75rem', background: '#059669', textDecoration: 'none', color: '#fff' }}>GeeksforGeeks</a>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Flashcards */}
                  {aiContent.type === 'flashcards' && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      {aiContent.data.flashcards?.map((card, i) => (
                        <FlashcardWidget key={i} front={card.front} back={card.back} index={i} />
                      ))}
                    </div>
                  )}

                  {/* Hints */}
                  {aiContent.type === 'hints' && (
                    <ul style={{ paddingLeft: '20px', lineHeight: 1.8, margin: 0 }}>
                      {aiContent.data.hints?.map((hint, i) => (
                        <li key={i} style={{ fontSize: '0.95rem', marginBottom: '6px' }}>{hint}</li>
                      ))}
                    </ul>
                  )}

                  {/* Explanation */}
                  {aiContent.type === 'explanation' && (
                    <div style={{ lineHeight: 1.7, fontSize: '0.95rem' }} dangerouslySetInnerHTML={renderMarkdown(aiContent.data.explanation)} />
                  )}

                  {/* Study Strategy */}
                  {aiContent.type === 'study-strategy' && aiContent.data && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                      <p style={{ fontSize: '0.95rem', lineHeight: 1.6, fontStyle: 'italic', margin: 0, background: '#f0f9ff', padding: '12px', borderRadius: '8px', borderLeft: '4px solid #0284c7' }}>
                        {aiContent.data.strategy_summary}
                      </p>
                      
                      {aiContent.data.topic_order?.length > 0 && (
                        <div>
                          <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9rem', color: '#1e293b' }}>Recommended Priority Order:</h4>
                          <ol style={{ paddingLeft: '20px', margin: 0, lineHeight: 1.7 }}>
                            {aiContent.data.topic_order.map((t, i) => <li key={i} style={{ marginBottom: '4px' }}><strong>{t}</strong></li>)}
                          </ol>
                        </div>
                      )}

                      {aiContent.data.time_allocation?.length > 0 && (
                        <div>
                          <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9rem', color: '#1e293b' }}>Time & Technique Allocation:</h4>
                          {aiContent.data.time_allocation.map((a, i) => (
                            <div key={i} style={{ padding: '8px 12px', background: '#f8fafc', borderRadius: '8px', border: '1px solid var(--border-color)', marginBottom: '6px' }}>
                              <strong>{a.topic}</strong> — <span style={{ color: '#0284c7', fontWeight: 600 }}>{a.hours} hours</span> {a.technique && `(${a.technique})`}
                            </div>
                          ))}
                        </div>
                      )}

                      {aiContent.data.revision_tips?.length > 0 && (
                        <div>
                          <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9rem', color: '#1e293b' }}>Key Revision Tips:</h4>
                          <ul style={{ paddingLeft: '20px', margin: 0, lineHeight: 1.6 }}>
                            {aiContent.data.revision_tips.map((t, i) => <li key={i} style={{ marginBottom: '4px' }}>{t}</li>)}
                          </ul>
                        </div>
                      )}

                      {aiContent.data.motivation && (
                        <div style={{ padding: '12px', background: '#fef3c7', borderRadius: '8px', textAlign: 'center', fontStyle: 'italic', margin: 0, color: '#92400e' }}>
                          ✨ "{aiContent.data.motivation}"
                        </div>
                      )}
                    </div>
                  )}

                  {/* Wellness */}
                  {aiContent.type === 'wellness' && aiContent.data && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                      <div style={{ fontSize: '2.5rem', textAlign: 'center' }}>{aiContent.data.mood_emoji || '😊'}</div>
                      <div style={{ padding: '12px', background: '#ecfdf5', borderRadius: '8px', border: '1px solid #a7f3d0' }}>
                        <strong style={{ color: '#065f46' }}>Wellness Tip:</strong> {aiContent.data.wellness_tip}
                      </div>
                      <div style={{ padding: '12px', background: '#fef3c7', borderRadius: '8px', fontStyle: 'italic', textAlign: 'center', color: '#78350f' }}>
                        "{aiContent.data.motivation_quote}"
                      </div>
                      <div style={{ padding: '12px', background: '#eff6ff', borderRadius: '8px', border: '1px solid #bfdbfe' }}>
                        <strong style={{ color: '#1e40af' }}>Break Activity:</strong> {aiContent.data.break_activity}
                      </div>
                      <div style={{ padding: '12px', background: '#fef2f2', borderRadius: '8px', border: '1px solid #fecaca' }}>
                        <strong style={{ color: '#991b1b' }}>Physical Health:</strong> {aiContent.data.health_reminder}
                      </div>
                    </div>
                  )}

                  {/* Mock Test */}
                  {aiContent.type === 'mocktest' && (
                    <MockTestPanel questions={aiContent.data?.questions || []} />
                  )}

                  {/* Portfolio Projects */}
                  {aiContent.type === 'project-ideas' && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                      <p style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>
                        Build these real-world portfolio projects to prove hands-on technical competence to recruiters and engineering teams:
                      </p>
                      {(aiContent.data?.projects || []).map((proj, idx) => (
                        <div key={idx} style={{
                          background: '#f8fafc',
                          borderRadius: '12px',
                          padding: '16px',
                          border: '1px solid var(--border-color)',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '8px'
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '6px' }}>
                            <h4 style={{ margin: 0, color: '#1e293b', fontSize: '1.05rem' }}>
                              #{idx + 1} {proj.title}
                            </h4>
                            <span style={{
                              fontSize: '0.75rem',
                              padding: '3px 8px',
                              borderRadius: '999px',
                              background: idx === 0 ? '#dbeafe' : idx === 1 ? '#e0e7ff' : '#fef3c7',
                              color: idx === 0 ? '#1d4ed8' : idx === 1 ? '#4338ca' : '#b45309',
                              fontWeight: 600
                            }}>
                              {proj.level}
                            </span>
                          </div>
                          <div style={{ fontSize: '0.85rem', color: '#475569' }}>
                            <strong>🛠️ Tech Stack:</strong> {proj.tech_stack}
                          </div>
                          <p style={{ margin: 0, fontSize: '0.9rem', color: '#334155', lineHeight: 1.5 }}>
                            {proj.description}
                          </p>
                          <div>
                            <strong style={{ fontSize: '0.85rem', color: '#1e293b' }}>Key Deliverables:</strong>
                            <ul style={{ margin: '4px 0 0 0', paddingLeft: '20px', fontSize: '0.85rem', color: '#475569', lineHeight: 1.6 }}>
                              {(proj.key_deliverables || []).map((del, dIdx) => (
                                <li key={dIdx}>{del}</li>
                              ))}
                            </ul>
                          </div>
                          <div style={{
                            marginTop: '4px',
                            padding: '8px 12px',
                            background: '#f0fdf4',
                            borderRadius: '8px',
                            borderLeft: '3px solid #10b981',
                            fontSize: '0.82rem',
                            color: '#166534'
                          }}>
                            <strong>💼 Resume & Portfolio Impact:</strong> {proj.portfolio_impact}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', borderTop: '1px solid var(--border-color)', paddingTop: '14px' }}>
                  <button className="btn" onClick={downloadPDF} style={{ background: 'var(--success-color)' }}>
                    📥 Download PDF
                  </button>
                  <button className="btn btn-secondary" onClick={() => setAiContent(null)}>
                    Close
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// Interactive Flip-Card
function FlashcardWidget({ front, back, index }) {
  const [flipped, setFlipped] = useState(false);
  return (
    <div
      onClick={() => setFlipped(!flipped)}
      style={{
        background: flipped ? '#ecfdf5' : '#fff',
        padding: '14px 16px',
        borderRadius: '10px',
        border: '1px solid ' + (flipped ? '#86efac' : 'var(--border-color)'),
        cursor: 'pointer',
        transition: 'all 0.2s',
        boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
      }}
    >
      <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>
        Card {index + 1} — {flipped ? 'Answer (Click to flip back)' : 'Click to flip'}
      </div>
      <div style={{ fontSize: '0.95rem', fontWeight: flipped ? 500 : 600, color: flipped ? '#065f46' : '#1e293b' }}>
        {flipped ? back : front}
      </div>
    </div>
  );
}

// Mock Test Component
function MockTestPanel({ questions }) {
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  if (!questions || questions.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '30px', color: 'var(--text-secondary)' }}>
        <p>No questions generated for this mock test. Please try again.</p>
      </div>
    );
  }

  const handleSelect = (qIdx, option) => {
    if (submitted) return;
    setAnswers({ ...answers, [qIdx]: option });
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  const getCorrectCount = () => {
    let count = 0;
    questions.forEach((q, idx) => {
      const selected = (answers[idx] || '').trim().toUpperCase();
      const correct = (q.correct_option || '').trim().toUpperCase();
      if (selected === correct || correct.split(',').includes(selected)) {
        count++;
      }
    });
    return count;
  };

  return (
    <div style={{ marginTop: '8px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h4 style={{ margin: 0, color: '#1e293b' }}>Mock Test Questions ({questions.length} total)</h4>
        {!submitted && (
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Answered: {Object.keys(answers).length} / {questions.length}
          </span>
        )}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
        {questions.map((q, idx) => {
          const selected = answers[idx];
          const correctOpt = (q.correct_option || '').trim().toUpperCase();
          const isCorrect = (selected || '').trim().toUpperCase() === correctOpt;

          return (
            <div
              key={idx}
              style={{
                padding: '16px',
                background: '#fff',
                borderRadius: '10px',
                border: '1px solid var(--border-color)',
                boxShadow: '0 1px 3px rgba(0,0,0,0.04)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#64748b' }}>
                  Question {idx + 1} of {questions.length} ({q.difficulty || 'Medium'})
                </span>
                {q.topic && (
                  <span style={{ fontSize: '0.8rem', background: '#eff6ff', color: '#1d4ed8', padding: '2px 8px', borderRadius: '4px', fontWeight: 500 }}>
                    {q.topic}
                  </span>
                )}
              </div>

              <p style={{ fontWeight: 600, margin: '0 0 12px 0', fontSize: '0.95rem', color: '#1e293b' }}>
                {q.question_text}
              </p>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {['A', 'B', 'C', 'D'].map(opt => {
                  const label = opt === 'A' ? q.option_a : opt === 'B' ? q.option_b : opt === 'C' ? q.option_c : q.option_d;
                  const isOptSelected = selected === opt;
                  
                  let bg = '#fff';
                  let border = '1px solid #e2e8f0';
                  let textColor = '#334155';

                  if (submitted) {
                    if (opt === correctOpt || correctOpt.split(',').includes(opt)) {
                      bg = '#dcfce7';
                      border = '1px solid #86efac';
                      textColor = '#166534';
                    } else if (isOptSelected && !isCorrect) {
                      bg = '#fee2e2';
                      border = '1px solid #fca5a5';
                      textColor = '#991b1b';
                    }
                  } else if (isOptSelected) {
                    bg = '#eff6ff';
                    border = '2px solid var(--accent-color)';
                    textColor = '#1d4ed8';
                  }

                  return (
                    <button
                      key={opt}
                      onClick={() => handleSelect(idx, opt)}
                      disabled={submitted}
                      style={{
                        textAlign: 'left',
                        padding: '10px 14px',
                        background: bg,
                        border: border,
                        color: textColor,
                        borderRadius: '8px',
                        cursor: submitted ? 'default' : 'pointer',
                        fontSize: '0.9rem',
                        transition: 'all 0.15s'
                      }}
                    >
                      <strong>{opt}.</strong> {label}
                    </button>
                  );
                })}
              </div>

              {submitted && (
                <div style={{ marginTop: '12px', padding: '10px 14px', background: '#f8fafc', borderRadius: '8px', fontSize: '0.85rem', borderLeft: isCorrect ? '4px solid #10b981' : '4px solid #ef4444' }}>
                  <span style={{ fontWeight: 700, color: isCorrect ? 'var(--success-color)' : 'var(--danger-color)' }}>
                    {isCorrect ? '✓ Correct! ' : '✗ Incorrect. '}
                  </span>
                  <span>{q.explanation}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {!submitted ? (
        <button
          onClick={handleSubmit}
          className="btn"
          style={{ marginTop: '20px', width: '100%', background: 'var(--success-color)', padding: '12px', fontSize: '1rem', fontWeight: 600 }}
        >
          Submit Mock Test
        </button>
      ) : (
        <div style={{ marginTop: '20px', padding: '16px', background: '#eff6ff', borderRadius: '10px', textAlign: 'center', border: '1px solid #bfdbfe' }}>
          <h3 style={{ margin: '0 0 6px 0', color: '#1d4ed8' }}>Mock Test Results</h3>
          <p style={{ margin: 0, fontSize: '1.2rem', fontWeight: 700 }}>
            Score: {getCorrectCount()} / {questions.length} ({Math.round((getCorrectCount() / questions.length) * 100)}%)
          </p>
        </div>
      )}
    </div>
  );
}

export default StudyTracker;
