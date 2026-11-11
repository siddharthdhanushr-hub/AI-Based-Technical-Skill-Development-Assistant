import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function SkillManager() {
  const [subjects, setSubjects] = useState([]);
  const [newSubject, setNewSubject] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [resourceFiles, setResourceFiles] = useState([]);
  
  // Active skill track
  const [activeSubject, setActiveSubject] = useState(null);
  const [newSkillName, setNewSkillName] = useState('');
  const [editingTopicId, setEditingTopicId] = useState(null);
  const [editSkillName, setEditSkillName] = useState('');
  const [editingSubjectId, setEditingSubjectId] = useState(null);
  const [editSubjectName, setEditSubjectName] = useState('');
  const [extractedTopics, setExtractedTopics] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);
  const [isAddingTopics, setIsAddingTopics] = useState(false);
  const [isUploadingPanelFile, setIsUploadingPanelFile] = useState(false);

  const navigate = useNavigate();

  const fetchSubjects = async () => {
    try {
      const res = await api.get('/syllabus/subjects');
      setSubjects(res.data);
      if (res.data.length > 0 && !activeSubject) {
        setActiveSubject(res.data[0].subject_id);
      }
    } catch (err) {
      console.error("Error fetching skill tracks:", err);
    }
  };

  useEffect(() => {
    fetchSubjects();
  }, []);

  const handleAddSubject = async (e) => {
    e.preventDefault();
    if (!newSubject.trim()) return;
    try {
      // 1. Create Skill Track
      const res = await api.post('/syllabus/subjects', { subject_name: newSubject.trim() });
      const createdSubjectId = res.data.subject_id;

      // 2. Upload photo / roadmap file if selected
      if (selectedFile) {
        const formData = new FormData();
        formData.append('file', selectedFile);
        await api.post(`/syllabus/subjects/${createdSubjectId}/upload`, formData);
      }

      // 3. Upload additional resources if selected
      if (resourceFiles && resourceFiles.length > 0) {
        for (const file of resourceFiles) {
          const resFormData = new FormData();
          resFormData.append('file', file);
          await api.post(`/syllabus/subjects/${createdSubjectId}/resources`, resFormData);
        }
      }

      setNewSubject('');
      setSelectedFile(null);
      setResourceFiles([]);
      await fetchSubjects();
      setActiveSubject(createdSubjectId);
    } catch (err) {
      alert('Failed to add skill track or upload file');
    }
  };

  const handlePanelFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file || !activeSubject) return;
    setIsUploadingPanelFile(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      await api.post(`/syllabus/subjects/${activeSubject}/upload`, formData);
      await fetchSubjects();
    } catch (err) {
      alert('Failed to upload file for this skill track.');
    } finally {
      setIsUploadingPanelFile(false);
      e.target.value = null;
    }
  };

  const handleAddResource = async (e) => {
    if (!e.target.files || e.target.files.length === 0) return;
    if (!activeSubject) return;
    try {
      for (const file of Array.from(e.target.files)) {
        const formData = new FormData();
        formData.append('file', file);
        await api.post(`/syllabus/subjects/${activeSubject}/resources`, formData);
      }
      fetchSubjects();
    } catch (err) {
      alert('Failed to upload resource');
    }
    e.target.value = null;
  };

  const handleDeleteResource = async (resourceId) => {
    if (!window.confirm("Delete this reference material?")) return;
    try {
      await api.delete(`/syllabus/subjects/${activeSubject}/resources/${resourceId}`);
      fetchSubjects();
    } catch (err) {
      alert('Failed to delete resource');
    }
  };

  const handleDeleteSubject = async (e, subjectId) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this skill track and all its competencies?")) return;
    try {
      await api.delete(`/syllabus/subjects/${subjectId}`);
      if (activeSubject === subjectId) setActiveSubject(null);
      fetchSubjects();
    } catch (err) {
      alert('Failed to delete skill track');
    }
  };

  // Add Skill without difficulty, estimated hours, or preferred time
  const handleAddSkill = async (e) => {
    e.preventDefault();
    if (!activeSubject || !newSkillName.trim()) return;
    try {
      await api.post(`/syllabus/subjects/${activeSubject}/topics`, {
        topic_name: newSkillName.trim(),
        difficulty_weight: 3.0,
        estimated_hours: 3.0,
        preferred_time: null
      });
      setNewSkillName('');
      fetchSubjects();
    } catch (err) {
      alert('Failed to add skill');
    }
  };

  const handleDeleteSkill = async (topicId) => {
    try {
      await api.delete(`/syllabus/subjects/${activeSubject}/topics/${topicId}`);
      fetchSubjects();
    } catch (err) {
      alert('Failed to delete skill');
    }
  };

  const handleEditSkill = (topic) => {
    setEditingTopicId(topic.topic_id);
    setEditSkillName(topic.topic_name);
  };

  const handleSaveSkill = async (topicId) => {
    if (!editSkillName.trim()) return;
    try {
      await api.put(`/syllabus/subjects/${activeSubject}/topics/${topicId}`, {
        topic_name: editSkillName.trim(),
        difficulty_weight: 3.0,
        estimated_hours: 3.0,
        preferred_time: null
      });
      setEditingTopicId(null);
      fetchSubjects();
    } catch (err) {
      alert('Failed to update skill');
    }
  };

  const handleSaveSubjectName = async (subjectId) => {
    if (!editSubjectName.trim()) return;
    try {
      await api.put(`/syllabus/subjects/${subjectId}`, { subject_name: editSubjectName });
      setEditingSubjectId(null);
      fetchSubjects();
    } catch (err) {
      alert('Failed to update skill track name');
    }
  };

  const handleExtractSkills = async () => {
    if (!activeSubject) return;
    setIsExtracting(true);
    setExtractedTopics(null);
    try {
      const res = await api.post(`/ai/syllabus/extract/${activeSubject}`);
      const topics = (res.data.topics || []).map(t => ({ ...t, selected: true }));
      setExtractedTopics(topics);
      fetchSubjects();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to extract skills. Please try again.');
    } finally {
      setIsExtracting(false);
    }
  };

  const activeSubObj = subjects.find(s => s.subject_id === activeSubject);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ margin: 0 }}>🛠️ Skill Manager</h1>
          <p style={{ margin: '4px 0 0 0', color: 'var(--text-secondary)' }}>
            Curate technical domains, upload skill roadmaps/photos, and extract competencies using AI.
          </p>
        </div>
        <button
          className="btn"
          onClick={() => navigate('/tracker')}
          style={{ background: '#0284c7' }}
        >
          📊 Go to Skill Tracker
        </button>
      </div>

      <div className="grid grid-cols-2">
        {/* Left Column: Create Skill Track & List */}
        <div className="glass-panel" style={{ alignSelf: 'start' }}>
          <h2>Add New Skill Track</h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '16px' }}>
            Enter a domain (e.g. <em>MLOps & Model Deployment, Neural Networks & Deep Learning, Cloud Architecture</em>) and optionally upload a roadmap image.
          </p>

          <form onSubmit={handleAddSubject} style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '32px' }}>
            <input 
              type="text" 
              className="input-field" 
              placeholder="e.g. MLOps & Production Engineering" 
              value={newSubject} 
              onChange={e => setNewSubject(e.target.value)} 
              required 
            />

            <div style={{
              border: '2px dashed #cbd5e1', 
              borderRadius: '12px', 
              padding: '16px', 
              textAlign: 'center', 
              background: '#f8fafc',
              cursor: 'pointer'
            }}>
              <label htmlFor="skill-file-upload" style={{ cursor: 'pointer', display: 'block' }}>
                <div style={{ fontSize: '1.6rem', marginBottom: '6px' }}>📷 / 📄</div>
                <strong style={{ fontSize: '0.9rem', color: '#1e293b' }}>
                  {selectedFile ? `Selected: ${selectedFile.name}` : "Upload Roadmap Photo / Curriculum (PNG, JPG, PDF)"}
                </strong>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: '#64748b' }}>
                  Our AI reads photos and extracts clean technical competencies!
                </p>
              </label>
              <input 
                id="skill-file-upload" 
                type="file" 
                accept=".png,.jpg,.jpeg,.bmp,.webp,.pdf,.doc,.docx,.txt" 
                onChange={e => setSelectedFile(e.target.files[0])} 
                style={{ display: 'none' }} 
              />
            </div>

            <button type="submit" className="btn" style={{ padding: '12px', fontSize: '0.95rem', fontWeight: 600 }}>
              ➕ Create Skill Track
            </button>
          </form>

          {/* List of Skill Tracks */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ margin: 0, fontSize: '1.1rem' }}>Active Skill Tracks</h3>
            <span className="badge">{subjects.length} Tracks</span>
          </div>

          {subjects.length === 0 ? (
            <p style={{ textAlign: 'center', padding: '20px 0', color: 'var(--text-secondary)' }}>No skill tracks created yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {subjects.map(sub => {
                const isSelected = activeSubject === sub.subject_id;
                const isEditing = editingSubjectId === sub.subject_id;
                return (
                  <div 
                    key={sub.subject_id} 
                    className="glass-panel" 
                    onClick={() => setActiveSubject(sub.subject_id)}
                    style={{
                      border: isSelected ? '2px solid var(--accent-color)' : '1px solid var(--border-color)',
                      cursor: 'pointer',
                      padding: '14px 16px',
                      background: isSelected ? '#eff6ff' : '#fff',
                      transition: 'all 0.2s',
                      borderRadius: '12px',
                      boxShadow: isSelected ? '0 4px 6px -1px rgba(59, 130, 246, 0.1)' : 'none'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div style={{ flex: 1 }}>
                        {isEditing ? (
                          <div style={{ display: 'flex', gap: '6px' }} onClick={e => e.stopPropagation()}>
                            <input 
                              type="text" 
                              className="input-field" 
                              value={editSubjectName} 
                              onChange={e => setEditSubjectName(e.target.value)}
                              style={{ padding: '4px 8px', fontSize: '0.9rem' }}
                            />
                            <button className="btn" style={{ padding: '4px 8px', fontSize: '0.8rem' }} onClick={() => handleSaveSubjectName(sub.subject_id)}>Save</button>
                            <button className="btn btn-secondary" style={{ padding: '4px 8px', fontSize: '0.8rem' }} onClick={() => setEditingSubjectId(null)}>X</button>
                          </div>
                        ) : (
                          <h4 style={{ margin: 0, fontSize: '1rem', color: isSelected ? '#1d4ed8' : '#1e293b' }}>
                            {sub.subject_name}
                          </h4>
                        )}
                        <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '2px', display: 'block' }}>
                          {sub.topics?.length || 0} skills cataloged
                        </span>
                      </div>

                      <div style={{ display: 'flex', gap: '6px' }} onClick={e => e.stopPropagation()}>
                        {!isEditing && (
                          <button 
                            onClick={() => { setEditingSubjectId(sub.subject_id); setEditSubjectName(sub.subject_name); }} 
                            style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '0.9rem' }}
                            title="Edit Track Name"
                          >
                            ✏️
                          </button>
                        )}
                        <button 
                          onClick={(e) => handleDeleteSubject(e, sub.subject_id)} 
                          style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '0.9rem' }}
                          title="Delete Skill Track"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right Column: Managing Active Skill Track */}
        <div className="glass-panel" style={{ alignSelf: 'start' }}>
          {!activeSubObj ? (
            <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-secondary)' }}>
              <p>Select a skill track on the left to manage its competencies and materials.</p>
            </div>
          ) : (
            <>
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '16px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                <div>
                  <h2 style={{ margin: '0 0 2px 0' }}>
                    Managing: <span style={{ color: 'var(--accent-color)' }}>{activeSubObj.subject_name}</span>
                  </h2>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                    {activeSubObj.topics?.length || 0} competencies configured
                  </span>
                </div>
                
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button 
                    onClick={() => navigate('/tracker')} 
                    className="btn" 
                    style={{ fontSize: '0.85rem', padding: '6px 12px', background: '#0284c7' }}
                  >
                    📊 Skill Tracker
                  </button>
                  {activeSubObj.topics?.length > 0 && (
                    <button 
                      onClick={() => navigate('/quiz', { state: { topicIds: activeSubObj.topics.map(t => t.topic_id) } })} 
                      className="btn" 
                      style={{ fontSize: '0.85rem', padding: '6px 12px', background: '#4f46e5' }}
                    >
                      🧠 Test Skills
                    </button>
                  )}
                </div>
              </div>

              {/* AI Extraction & Photo/Roadmap Section */}
              <div style={{
                background: '#e0e7ff',
                padding: '16px',
                borderRadius: '12px',
                marginBottom: '24px',
                border: '1px solid #c7d2fe'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                  <h3 style={{ fontSize: '1.05rem', margin: 0, color: '#3730a3' }}>
                    📷 Skill Roadmap & AI Extraction
                  </h3>
                  {activeSubObj.file_path && (
                    <span style={{ fontSize: '0.75rem', background: '#c7d2fe', color: '#312e81', padding: '2px 8px', borderRadius: '4px' }}>
                      File Attached
                    </span>
                  )}
                </div>
                
                <p style={{ fontSize: '0.85rem', color: '#4338ca', marginBottom: '14px' }}>
                  {activeSubObj.file_path 
                    ? "Your roadmap image/document is uploaded. Click below to let the AI Engine extract all technical competencies automatically!" 
                    : "Upload a skills roadmap photo or document to extract technical competencies automatically."
                  }
                </p>

                <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
                  <button 
                    onClick={handleExtractSkills} 
                    disabled={isExtracting}
                    className="btn" 
                    style={{
                      background: isExtracting ? '#9ca3af' : '#4f46e5',
                      color: '#fff',
                      boxShadow: '0 4px 6px -1px rgba(79, 70, 229, 0.3)',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px'
                    }}
                  >
                    {isExtracting ? '⏳ Reading & Extracting Skills...' : '✨ Extract Skills with AI'}
                  </button>

                  <label 
                    className="btn btn-secondary" 
                    style={{ fontSize: '0.85rem', padding: '7px 12px', cursor: 'pointer', margin: 0 }}
                  >
                    {isUploadingPanelFile ? 'Uploading...' : '📁 Upload New Photo/File'}
                    <input 
                      type="file" 
                      accept=".png,.jpg,.jpeg,.bmp,.webp,.pdf,.doc,.docx,.txt" 
                      onChange={handlePanelFileUpload}
                      style={{ display: 'none' }}
                      disabled={isUploadingPanelFile}
                    />
                  </label>
                </div>
              </div>

              {/* Extracted Skills Review Card (NO difficulty or hours shown) */}
              {extractedTopics && (
                <div className="glass-panel" style={{ background: '#f8fafc', border: '2px solid var(--accent-color)', padding: '16px', borderRadius: '12px', marginBottom: '24px' }}>
                  <h3 style={{ fontSize: '1.1rem', marginBottom: '6px', color: 'var(--accent-color)' }}>
                    📋 Suggested Skills ({extractedTopics.length})
                  </h3>
                  <p style={{ fontSize: '0.85rem', marginBottom: '14px', color: '#64748b' }}>
                    Select the competencies you want to add to this skill track:
                  </p>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '260px', overflowY: 'auto', marginBottom: '16px', paddingRight: '4px' }}>
                    {extractedTopics.map((topic, idx) => (
                      <label 
                        key={idx}
                        style={{
                          display: 'flex', 
                          alignItems: 'center', 
                          gap: '10px', 
                          padding: '10px 14px', 
                          background: '#fff', 
                          border: '1px solid var(--border-color)', 
                          borderRadius: '8px',
                          cursor: 'pointer',
                          fontSize: '0.92rem'
                        }}
                      >
                        <input 
                          type="checkbox" 
                          checked={topic.selected}
                          onChange={() => {
                            const updated = [...extractedTopics];
                            updated[idx].selected = !updated[idx].selected;
                            setExtractedTopics(updated);
                          }}
                          style={{ accentColor: 'var(--accent-color)', width: '16px', height: '16px' }}
                        />
                        <span style={{ fontWeight: 600, color: '#1e293b' }}>{topic.topic_name}</span>
                      </label>
                    ))}
                  </div>
                  
                  <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                    <button 
                      type="button"
                      disabled={isAddingTopics}
                      onClick={async (e) => {
                        e.preventDefault();
                        const selected = extractedTopics.filter(t => t.selected);
                        if (selected.length === 0) {
                          alert("Please select at least one skill.");
                          return;
                        }
                        setIsAddingTopics(true);
                        try {
                          await api.post(`/syllabus/subjects/${activeSubject}/topics/bulk`, selected.map(s => ({
                            topic_name: s.topic_name,
                            difficulty_weight: 3.0,
                            estimated_hours: 3.0
                          })));
                          setExtractedTopics(null);
                          alert(`Successfully added ${selected.length} skills!`);
                          fetchSubjects();
                        } catch (err) {
                          alert(`Failed to add skills: ${err.response?.data?.detail || err.message}`);
                        } finally {
                          setIsAddingTopics(false);
                        }
                      }}
                      className="btn"
                      style={{ background: isAddingTopics ? '#9ca3af' : 'var(--success-color)', cursor: isAddingTopics ? 'not-allowed' : 'pointer' }}
                    >
                      {isAddingTopics ? 'Saving Skills...' : `Add Selected Skills (${extractedTopics.filter(t => t.selected).length})`}
                    </button>
                    <button 
                      onClick={() => setExtractedTopics(null)} 
                      className="btn btn-secondary"
                      disabled={isAddingTopics}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              {/* Reference Documentation Section */}
              <div style={{ background: '#f8fafc', padding: '16px', borderRadius: '12px', marginBottom: '24px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <h3 style={{ fontSize: '1.05rem', margin: 0 }}>Reference Documentation & Notes</h3>
                  <label 
                    htmlFor="panel-resource-upload" 
                    className="btn btn-secondary"
                    style={{ padding: '4px 12px', fontSize: '0.85rem', cursor: 'pointer', margin: 0 }}
                  >
                    + Add Reference Doc
                  </label>
                  <input 
                    id="panel-resource-upload"
                    type="file" 
                    multiple
                    accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.txt"
                    onChange={handleAddResource}
                    style={{ display: 'none' }}
                  />
                </div>
                
                {activeSubObj?.resources && activeSubObj.resources.length > 0 ? (
                  <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px', margin: 0, padding: 0 }}>
                    {activeSubObj.resources.map(res => (
                      <li key={res.resource_id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px', background: '#fff', border: '1px solid var(--border-color)', borderRadius: '6px' }}>
                        <span style={{ fontSize: '0.9rem', fontWeight: 500, color: 'var(--text-primary)' }}>
                          📎 {res.filename}
                        </span>
                        <button 
                          onClick={() => handleDeleteResource(res.resource_id)}
                          style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '0.95rem', color: '#ef4444' }}
                          title="Delete File"
                        >
                          🗑️
                        </button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: 0 }}>No supplementary documentation uploaded.</p>
                )}
              </div>

              {/* Add Single Skill Form (Clean single input without difficulty or hours) */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <h3 style={{ fontSize: '1.1rem', margin: 0 }}>Competencies & Skills List</h3>
                <span className="badge">{activeSubObj?.topics?.length || 0} Skills</span>
              </div>

              <form onSubmit={handleAddSkill} style={{ display: 'flex', gap: '10px', marginBottom: '24px', background: '#f9fafb', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                <input 
                  type="text" 
                  className="input-field" 
                  placeholder="Enter Technical Skill Name (e.g. Docker Containerization & Multi-Stage Builds)" 
                  value={newSkillName} 
                  onChange={e => setNewSkillName(e.target.value)} 
                  required 
                  style={{ flex: 1 }}
                />
                <button type="submit" className="btn" style={{ padding: '0 20px', whiteSpace: 'nowrap', fontWeight: 600 }}>
                  ➕ Add Skill
                </button>
              </form>

              {/* Skills List Items (Clean: No difficulty, hours, or pref time) */}
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '10px', padding: 0 }}>
                {activeSubObj?.topics?.map(topic => {
                  const isEditing = editingTopicId === topic.topic_id;
                  const isDone = Boolean(topic.is_completed);

                  return (
                    <li 
                      key={topic.topic_id} 
                      style={{ 
                        padding: '14px 16px', 
                        background: isDone ? '#f0fdf4' : '#fff', 
                        borderRadius: '10px', 
                        border: isDone ? '1px solid #86efac' : '1px solid var(--border-color)', 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        boxShadow: '0 1px 3px rgba(0,0,0,0.04)'
                      }}
                    >
                      {isEditing ? (
                        <div style={{ display: 'flex', gap: '8px', width: '100%' }}>
                          <input
                            type="text"
                            className="input-field"
                            value={editSkillName}
                            onChange={e => setEditSkillName(e.target.value)}
                            placeholder="Skill Name"
                            required
                            style={{ flex: 1 }}
                          />
                          <button onClick={() => handleSaveSkill(topic.topic_id)} className="btn" style={{ padding: '6px 14px', fontSize: '0.85rem', background: 'var(--success-color)' }}>Save</button>
                          <button onClick={() => setEditingTopicId(null)} className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '0.85rem' }}>Cancel</button>
                        </div>
                      ) : (
                        <>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{ fontSize: '1.1rem' }}>{isDone ? '✅' : '🔹'}</span>
                            <div>
                              <span style={{ fontWeight: 600, fontSize: '0.98rem', color: isDone ? '#166534' : '#1e293b' }}>
                                {topic.topic_name}
                              </span>
                              <span style={{ fontSize: '0.78rem', color: isDone ? '#16a34a' : '#d97706', fontWeight: 600, marginLeft: '10px' }}>
                                {isDone ? '● Mastered' : '○ In Progress'}
                              </span>
                            </div>
                          </div>
                          <div style={{ display: 'flex', gap: '6px' }}>
                            <button onClick={() => handleEditSkill(topic)} className="btn btn-secondary" style={{ padding: '5px 8px', fontSize: '0.85rem', border: 'none', background: 'transparent' }} title="Edit Skill">✏️</button>
                            <button onClick={() => handleDeleteSkill(topic.topic_id)} style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '1rem' }} title="Delete Skill">🗑️</button>
                          </div>
                        </>
                      )}
                    </li>
                  );
                })}
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default SkillManager;

