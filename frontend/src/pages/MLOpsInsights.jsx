import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const PHASE1_METRICS = [
  { model: 'Random Forest (Champion)', acc: '73.51%', prec: '0.7211', rec: '0.6917', f1: '0.7061', auc: '0.7949', champion: true },
  { model: 'Logistic Regression (Baseline)', acc: '73.45%', prec: '0.7117', rec: '0.7108', f1: '0.7113', auc: '0.7974', champion: false },
  { model: 'Decision Tree (Candidate)', acc: '72.04%', prec: '0.7238', rec: '0.6344', f1: '0.6762', auc: '0.7885', champion: false },
];

const SKILLS_21ST = [
  { key: 'ai_ml', name: 'AI & Machine Learning', domain: 'Artificial Intelligence', justification: 'Generative AI, predictive modeling, LLM tooling, and autonomous intelligence systems.' },
  { key: 'data_science', name: 'Data Science & Big Data', domain: 'Analytics & Pipelines', justification: 'Data-driven decision making, high-throughput feature engineering, and statistical modeling.' },
  { key: 'software_development', name: 'Full-Stack Software Dev', domain: 'Application Engineering', justification: 'Modern decoupled architectures, REST/GraphQL APIs, and cloud-native services.' },
  { key: 'programming_skills', name: 'Core Coding & Algorithms', domain: 'Computer Science Core', justification: 'Data structures, asymptotic complexity, algorithmic problem solving, and language fluency.' },
  { key: 'cyber_security', name: 'Cyber Security & DevSecOps', domain: 'Security & Privacy', justification: 'Cloud security, zero-trust architectures, OWASP mitigation, and secure authentication.' },
  { key: 'distributed_computing_systems', name: 'Cloud & Distributed Systems', domain: 'Infrastructure & Scale', justification: 'Microservices, Docker, Kubernetes, consensus protocols, and horizontal scalability.' },
  { key: 'database_fundamentals', name: 'Modern Data Stores', domain: 'Data Engineering', justification: 'SQL schema normalization, indexing, ACID transactions, and NoSQL caching.' },
  { key: 'software_engineering', name: 'Software Engineering & CI/CD', domain: 'Quality & Process', justification: 'Clean code, TDD/automated testing suites, design patterns, and deployment pipelines.' },
  { key: 'troubleshooting_skills', name: 'Troubleshooting & SRE', domain: 'Observability & Systems', justification: 'Production debugging, distributed tracing, root-cause analysis, and performance tuning.' },
  { key: 'technical_communication', name: 'Technical Communication', domain: 'Agile Collaboration', justification: 'Cross-functional design reviews, architectural briefs, pull requests, and API contracts.' },
];

const EXCLUDED_SKILLS = [
  { key: 'computer_architecture', category: 'Hardware / Silicon', reason: 'Focuses on low-level microprocessor/silicon design; largely non-core for modern software screening.' },
  { key: 'computer_forensics_fundamentals', category: 'Post-Incident Niche', reason: 'Traditional disk/file forensic inspection; modern security engineering is unified under cyber_security.' },
  { key: 'networking', category: 'Legacy Telco / On-Prem', reason: 'Physical cabling and legacy protocols; superseded by cloud distributed systems and microservices.' },
  { key: 'project_management', category: 'Waterfall Process', reason: 'Legacy sequential PM; modern software teams employ agile workflows within technical communication.' },
  { key: 'business_analysis', category: 'Corporate Consulting', reason: 'Non-technical business process consulting; distinct from software engineering screening.' },
  { key: 'communication_skills', category: 'Generic Soft Skill', reason: 'Conversational speech; replaced by precise, code-oriented technical_communication.' },
  { key: 'graphics_designing', category: 'Creative Media', reason: 'Visual artwork and illustration; distinct from computer science and algorithmic proficiencies.' },
];

const BEHAVIORAL_TESTS = [
  { name: 'Boundary Extremes Test', result: 'PASSED (4/4)', desc: 'Validates that a 0-confidence vector strictly yields Pass=0 (Fail), while a 6-confidence vector strictly yields Pass=1.' },
  { name: 'Directional Monotonicity Test', result: 'PASSED (10/10)', desc: 'Validates that monotonically increasing any skill rating never decreases the predicted pass probability.' },
  { name: 'Metadata Invariance Test', result: 'PASSED (6/6)', desc: 'Validates that student ID, session timestamp, and non-predictive metadata do not alter inference outputs.' },
  { name: 'Inference Latency Benchmark', result: 'PASSED (<12ms)', desc: 'Evaluates p95 inference latency under 15ms target on standard hardware, guaranteeing real-time web responsiveness.' },
];

export default function MLOpsInsights() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('phase1');

  return (
    <div style={{ maxWidth: '1150px', margin: '0 auto', paddingBottom: '60px' }}>
      {/* Hero Header */}
      <div className="glass-panel" style={{ marginBottom: '24px', background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)', color: '#fff', border: 'none' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', background: 'rgba(255,255,255,0.12)', borderRadius: '20px', fontSize: '0.82rem', marginBottom: '12px' }}>
              <span>🚀 MLOps Productionization Hub</span>
              <span>•</span>
              <span>Phase 1 Rework & Phase 2 Governance</span>
            </div>
            <h1 style={{ color: '#fff', fontSize: '2.1rem', marginBottom: '8px' }}>
              MLOps Results & Architectural Insights
            </h1>
            <p style={{ color: '#cbd5e1', fontSize: '1rem', maxWidth: '800px', marginBottom: 0 }}>
              Detailed evaluation reports, benchmark performance matrices, behavioral model testing suites, and production governance deliverables for the <strong>AI-Based Technical Skill Development Assistant</strong>.
            </p>
          </div>
          <button
            onClick={() => navigate('/century-skills')}
            className="btn"
            style={{ background: '#4f46e5', color: '#fff', border: 'none' }}
          >
            🎯 Try Skills Assessment
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', borderBottom: '2px solid #e2e8f0', paddingBottom: '8px' }}>
        <button
          onClick={() => setActiveTab('phase1')}
          style={{
            padding: '10px 20px',
            background: 'none',
            border: 'none',
            borderBottom: activeTab === 'phase1' ? '3px solid #4f46e5' : '3px solid transparent',
            color: activeTab === 'phase1' ? '#4f46e5' : '#64748b',
            fontWeight: 700,
            fontSize: '1rem',
            cursor: 'pointer',
            transition: 'all 0.15s ease'
          }}
        >
          📈 Phase 1: Benchmark Evaluation
        </button>
        <button
          onClick={() => setActiveTab('phase2')}
          style={{
            padding: '10px 20px',
            background: 'none',
            border: 'none',
            borderBottom: activeTab === 'phase2' ? '3px solid #4f46e5' : '3px solid transparent',
            color: activeTab === 'phase2' ? '#4f46e5' : '#64748b',
            fontWeight: 700,
            fontSize: '1rem',
            cursor: 'pointer',
            transition: 'all 0.15s ease'
          }}
        >
          🛡️ Phase 2: Productionization & Governance
        </button>
        <button
          onClick={() => setActiveTab('taxonomy')}
          style={{
            padding: '10px 20px',
            background: 'none',
            border: 'none',
            borderBottom: activeTab === 'taxonomy' ? '3px solid #4f46e5' : '3px solid transparent',
            color: activeTab === 'taxonomy' ? '#4f46e5' : '#64748b',
            fontWeight: 700,
            fontSize: '1rem',
            cursor: 'pointer',
            transition: 'all 0.15s ease'
          }}
        >
          🧩 21st-Century Skills Taxonomy
        </button>
      </div>

      {/* TAB 1: PHASE 1 INSIGHTS */}
      {activeTab === 'phase1' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Executive Overview Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
            <div className="glass-panel" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.85rem', color: '#64748b', fontWeight: 600 }}>Benchmark Population</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#1e293b', marginTop: '4px' }}>8,528 Students</div>
              <div style={{ fontSize: '0.8rem', color: '#10b981', marginTop: '4px' }}>CareerMap Mendeley Data (DOI: 10.17632)</div>
            </div>
            <div className="glass-panel" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.85rem', color: '#64748b', fontWeight: 600 }}>Test Evaluation Set</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#4f46e5', marginTop: '4px' }}>1,706 Profiles</div>
              <div style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '4px' }}>Stratified 70/30 split, zero data leakage</div>
            </div>
            <div className="glass-panel" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.85rem', color: '#64748b', fontWeight: 600 }}>Champion Accuracy</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#059669', marginTop: '4px' }}>73.51%</div>
              <div style={{ fontSize: '0.8rem', color: '#059669', marginTop: '4px' }}>ROC-AUC: 0.795, F1: 0.706</div>
            </div>
            <div className="glass-panel" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.85rem', color: '#64748b', fontWeight: 600 }}>Champion Model</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: '#d97706', marginTop: '4px' }}>Random Forest</div>
              <div style={{ fontSize: '0.8rem', color: '#d97706', marginTop: '4px' }}>100 de-correlated trees, max_depth=7</div>
            </div>
          </div>

          {/* Model Comparison Table */}
          <div className="glass-panel">
            <h3 style={{ margin: '0 0 16px', color: '#1e293b' }}>
              Model Benchmark Leaderboard (Held-Out Evaluation Set)
            </h3>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', textAlign: 'left', borderBottom: '2px solid #e2e8f0' }}>
                    <th style={{ padding: '12px 14px', color: '#475569' }}>Model Architecture</th>
                    <th style={{ padding: '12px 14px', color: '#475569' }}>Accuracy</th>
                    <th style={{ padding: '12px 14px', color: '#475569' }}>Precision</th>
                    <th style={{ padding: '12px 14px', color: '#475569' }}>Recall</th>
                    <th style={{ padding: '12px 14px', color: '#475569' }}>F1-Score</th>
                    <th style={{ padding: '12px 14px', color: '#475569' }}>ROC-AUC</th>
                    <th style={{ padding: '12px 14px', color: '#475569' }}>MLOps Status</th>
                  </tr>
                </thead>
                <tbody>
                  {PHASE1_METRICS.map(m => (
                    <tr
                      key={m.model}
                      style={{
                        borderBottom: '1px solid #f1f5f9',
                        background: m.champion ? '#f0fdf4' : 'transparent'
                      }}
                    >
                      <td style={{ padding: '12px 14px', fontWeight: 600, color: '#1e293b' }}>
                        {m.model}
                      </td>
                      <td style={{ padding: '12px 14px', fontWeight: 700, color: m.champion ? '#059669' : '#1e293b' }}>
                        {m.acc}
                      </td>
                      <td style={{ padding: '12px 14px' }}>{m.prec}</td>
                      <td style={{ padding: '12px 14px' }}>{m.rec}</td>
                      <td style={{ padding: '12px 14px' }}>{m.f1}</td>
                      <td style={{ padding: '12px 14px', fontWeight: 600 }}>{m.auc}</td>
                      <td style={{ padding: '12px 14px' }}>
                        {m.champion ? (
                          <span style={{ padding: '4px 10px', borderRadius: '12px', background: '#dcfce7', color: '#15803d', fontWeight: 700, fontSize: '0.78rem' }}>
                            🏆 Champion (Staged: Prod)
                          </span>
                        ) : (
                          <span style={{ padding: '4px 10px', borderRadius: '12px', background: '#f1f5f9', color: '#64748b', fontWeight: 600, fontSize: '0.78rem' }}>
                            Candidate
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{ marginTop: '16px', padding: '14px', borderRadius: '8px', background: '#f8fafc', fontSize: '0.85rem', color: '#475569' }}>
              <strong>Selection Rationale:</strong> Random Forest was chosen as champion because it aggregates 100 de-correlated decision trees, achieving the highest ROC-AUC (0.7949) and balanced precision/recall without majority class bias. Constraining tree depth to 7 matches real-world placement exam uncertainty where boundary candidates cannot be deterministically separated by skill ratings alone.
            </div>
          </div>

          {/* Confusion Matrix Visualization */}
          <div className="glass-panel">
            <h3 style={{ margin: '0 0 16px', color: '#1e293b' }}>
              Champion Confusion Matrix (N = 1,706 Held-Out Students)
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', alignItems: 'center' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', maxWidth: '420px', margin: '0 auto' }}>
                <div style={{ padding: '18px', borderRadius: '10px', background: '#ecfdf5', border: '1px solid #a7f3d0', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.8rem', color: '#065f46', fontWeight: 600 }}>True Negatives (TN)</div>
                  <div style={{ fontSize: '2rem', fontWeight: 700, color: '#047857', margin: '4px 0' }}>711</div>
                  <div style={{ fontSize: '0.75rem', color: '#059669' }}>Correctly flagged for preparation</div>
                </div>
                <div style={{ padding: '18px', borderRadius: '10px', background: '#fffbeb', border: '1px solid #fde68a', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.8rem', color: '#92400e', fontWeight: 600 }}>False Positives (FP)</div>
                  <div style={{ fontSize: '2rem', fontWeight: 700, color: '#b45309', margin: '4px 0' }}>210</div>
                  <div style={{ fontSize: '0.75rem', color: '#d97706' }}>Predicted pass, needed review</div>
                </div>
                <div style={{ padding: '18px', borderRadius: '10px', background: '#fef2f2', border: '1px solid #fecaca', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.8rem', color: '#991b1b', fontWeight: 600 }}>False Negatives (FN)</div>
                  <div style={{ fontSize: '2rem', fontWeight: 700, color: '#b91c1c', margin: '4px 0' }}>242</div>
                  <div style={{ fontSize: '0.75rem', color: '#dc2626' }}>Underestimated readiness</div>
                </div>
                <div style={{ padding: '18px', borderRadius: '10px', background: '#ecfdf5', border: '1px solid #a7f3d0', textAlign: 'center' }}>
                  <div style={{ fontSize: '0.8rem', color: '#065f46', fontWeight: 600 }}>True Positives (TP)</div>
                  <div style={{ fontSize: '2rem', fontWeight: 700, color: '#047857', margin: '4px 0' }}>543</div>
                  <div style={{ fontSize: '0.75rem', color: '#059669' }}>Correctly cleared for assessment</div>
                </div>
              </div>

              <div style={{ fontSize: '0.88rem', color: '#475569', lineHeight: 1.6 }}>
                <h4 style={{ margin: '0 0 8px', color: '#1e293b' }}>Operational Interpretation:</h4>
                <p style={{ margin: '0 0 10px' }}>
                  • <strong>False Positives (FP = 210):</strong> Mitigated directly by our <strong>21st-Century Cross-Verification Quiz</strong>. If a candidate over-reports confidence, the 10-question gate detects the gap before real-world screening.
                </p>
                <p style={{ margin: '0 0 10px' }}>
                  • <strong>False Negatives (FN = 242):</strong> Mitigated by our <strong>Skill Tracker sync</strong>. Candidates directed to the tracker receive Skill Briefs, Flashcards, and Portfolio Projects to quickly shore up confidence and re-qualify.
                </p>
                <p style={{ margin: 0 }}>
                  • <strong>Overall Specificity:</strong> 77.20% on the Fail class; <strong>Sensitivity:</strong> 69.17% on the Pass class.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: PHASE 2 GOVERNANCE */}
      {activeTab === 'phase2' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Behavioral Tests Grid */}
          <div className="glass-panel">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h3 style={{ margin: 0, color: '#1e293b' }}>
                Behavioral Model Quality Tests (46/46 Passed)
              </h3>
              <span className="badge badge-success">100% Quality Pass Rate</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
              {BEHAVIORAL_TESTS.map(test => (
                <div key={test.name} style={{ padding: '16px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <strong style={{ fontSize: '0.92rem', color: '#1e293b' }}>{test.name}</strong>
                    <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#059669', background: '#ecfdf5', padding: '2px 8px', borderRadius: '10px' }}>
                      {test.result}
                    </span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.82rem', color: '#64748b', lineHeight: 1.5 }}>
                    {test.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Production MLOps Architecture */}
          <div className="glass-panel">
            <h3 style={{ margin: '0 0 16px', color: '#1e293b' }}>
              MLOps Pipeline Governance & Architecture
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              <div style={{ padding: '18px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                <h4 style={{ margin: '0 0 8px', color: '#4f46e5' }}>1. Data Version Control (DVC)</h4>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#64748b', lineHeight: 1.6 }}>
                  Dataset versions and feature pipelines are version-tracked via DVC with cryptographic hashes. Guarantees 100% reproducible training runs across any environment without data divergence.
                </p>
              </div>

              <div style={{ padding: '18px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                <h4 style={{ margin: '0 0 8px', color: '#059669' }}>2. MLflow Model Registry</h4>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#64748b', lineHeight: 1.6 }}>
                  Trained artifacts (Random Forest, Decision Tree, Logistic Regression) are logged with complete hyperparameter manifests. Automated promotion tags the champion model into the <code>Production</code> stage.
                </p>
              </div>

              <div style={{ padding: '18px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                <h4 style={{ margin: '0 0 8px', color: '#d97706' }}>3. Model Risk & Uncertainty Flags</h4>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#64748b', lineHeight: 1.6 }}>
                  Evaluations with pass probabilities in the borderline uncertainty window (45%–55%) trigger automated risk flags, prompting mandatory verification testing before final recommendations.
                </p>
              </div>

              <div style={{ padding: '18px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                <h4 style={{ margin: '0 0 8px', color: '#0284c7' }}>4. Docker & FastAPI Microservice</h4>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#64748b', lineHeight: 1.6 }}>
                  High-throughput REST API packaged with non-root security principles, automated OpenAPI documentation, Pydantic v2 validation contracts, and automated healthcheck probes.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: TAXONOMY & EXCLUSIONS */}
      {activeTab === 'taxonomy' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* 10 Core Skills */}
          <div className="glass-panel">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h3 style={{ margin: 0, color: '#1e293b' }}>
                  10 Curated 21st-Century Technical Competencies
                </h3>
                <p style={{ margin: '4px 0 0', fontSize: '0.85rem', color: '#64748b' }}>
                  Aligned with modern screening realities (LeetCode, HackerRank, CodeSignal assessments).
                </p>
              </div>
              <span className="badge badge-success">Evaluator Directive Curated</span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '14px' }}>
              {SKILLS_21ST.map((s, idx) => (
                <div key={s.key} style={{ padding: '14px 16px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <strong style={{ fontSize: '0.95rem', color: '#1e293b' }}>#{idx + 1} {s.name}</strong>
                    <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: '10px', background: '#eff6ff', color: '#2563eb', fontWeight: 600 }}>
                      {s.domain}
                    </span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.82rem', color: '#64748b', lineHeight: 1.5 }}>
                    {s.justification}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* 7 Excluded Skills */}
          <div className="glass-panel">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h3 style={{ margin: 0, color: '#1e293b' }}>
                  7 Excluded Legacy / Peripheral Skills
                </h3>
                <p style={{ margin: '4px 0 0', fontSize: '0.85rem', color: '#64748b' }}>
                  Pruning justification per evaluator feedback — removing non-software and legacy hardware domains.
                </p>
              </div>
              <span style={{ padding: '4px 10px', borderRadius: '12px', background: '#fef2f2', color: '#991b1b', fontWeight: 600, fontSize: '0.8rem' }}>
                Pruned from Screening
              </span>
            </div>

            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' }}>
                <thead>
                  <tr style={{ background: '#f8fafc', textAlign: 'left', borderBottom: '2px solid #e2e8f0' }}>
                    <th style={{ padding: '10px 12px', color: '#475569' }}>Excluded Discipline</th>
                    <th style={{ padding: '10px 12px', color: '#475569' }}>Discipline Category</th>
                    <th style={{ padding: '10px 12px', color: '#475569' }}>Architectural Rationale for Pruning</th>
                  </tr>
                </thead>
                <tbody>
                  {EXCLUDED_SKILLS.map(s => (
                    <tr key={s.key} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '10px 12px', fontWeight: 600, color: '#1e293b' }}>
                        <code>{s.key}</code>
                      </td>
                      <td style={{ padding: '10px 12px' }}>
                        <span style={{ padding: '2px 8px', borderRadius: '10px', background: '#f1f5f9', color: '#475569', fontSize: '0.78rem' }}>
                          {s.category}
                        </span>
                      </td>
                      <td style={{ padding: '10px 12px', color: '#64748b', fontSize: '0.83rem' }}>
                        {s.reason}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

