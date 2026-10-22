# Frontend Architecture & Learner Usage Guide — Phase 1

**Author:** Member 3 (Siddharth Chandrashekar C)  
**Role:** Student Frontend, Revision, Flashcards and Quiz Experience  
**Date:** October 2026  
**Status:** Completed & Build Verified  

---

## 1. Overview & Technical Stack
The learner-facing application is built with **React 19**, **React Router v7**, and **Vite**, featuring a clean custom CSS design system using Google Fonts (*Outfit* & *JetBrains Mono*) with modern glassmorphism panels, responsive grid layouts, and keyboard-accessible micro-interactions.

### Key Capabilities:
- **Direct First-Party Data Capture**: Replaces detached forms and spreadsheets by capturing confidence assessments, revision completions, and question answers directly as structured telemetry events.
- **Distinction of Competence**: Visually and semantically isolates **Self-Reported Confidence** from **Demonstrated Quiz Mastery**.
- **Resilient Fallback Mode**: If the backend API or an optional LLM service is offline, the client seamlessly loads verified local curriculum datasets and buffers telemetry in `localStorage`.

---

## 2. Screen-by-Screen User Journey

### A. Curriculum Explorer (`/topics`)
- **Domain Tabs**: Switch between technical areas (*Machine Learning Core*, *MLOps & Reproducibility*).
- **Topic Cards**: Each card displays the topic title, difficulty badge (*Medium*, *Hard*), estimated completion time, and current confidence rating.
- **Direct Actions**: Links to **Rate Confidence** or **Start Revision**.

### B. Confidence Assessment (`/confidence/:topicId`)
- **0–100 Continuous Range Slider**: Allows students to calibrate their perceived understanding on a granular scale.
- **Dynamic Confidence Bands**:
  - `Low Confidence` ($< 60\%$): Displays a warning recommendation to complete revision before the quiz.
  - `Moderate Confidence` ($60–79\%$): Developing familiarity.
  - `High Confidence` ($\ge 80\%$): Comfortable grasp.
- **Telemetry Event**: Submitting dispatches `confidence_assessment_submitted`.

### C. Targeted Revision & Interactive Flashcards (`/revision/:topicId`)
- **Concept Summaries**: Formally written definitions, empirical formulations, and loss functions.
- **Interactive 3D Flipping Flashcards**:
  - Displays conceptual questions on the front and concise explanations on the back.
  - **Keyboard Accessibility**: Press **Space** or **Enter** to flip cards; press **Left/Right Arrow** keys to navigate.
- **Revision Completion**: Clicking **"Start Topic Quiz"** logs duration and dispatches `revision_completed`.

### D. Demonstrated Mastery Quiz (`/quiz/:topicId`)
- **Question Navigation**: Topic-mapped multiple choice items with options A, B, C, D.
- **Immediate Scoring**: Computes validated percentage score and determines grip status:
  - **Needs Revision** ($< 60\%$)
  - **Developing** ($60–79\%$)
  - **Demonstrated Mastery** ($\ge 80\%$)
- **Question Breakdown**: Displays student choice vs. correct answer with detailed explanations.
- **Multi-Attempt Tracking**: Supports retaking quizzes with unique attempt identifiers (`att_...`).

### E. Personalized Dashboard (`/`)
- **Metric Cards**: Real-time counts of assessed topics, weak topics ($< 60\%$), total quizzes completed, and average score.
- **Topic Readiness Summary**: Clear status tags distinguishing unassessed provisional topics from proven demonstrated mastery.
- **Next-Action Recommendations**: Transparent rule-based action suggestions.

### F. Calibration Analytics (`/analytics`)
- **Calibration Assessment Table**: Evaluates whether the student is **Overconfident** (Confidence $> 20\%$ above Quiz), **Well-Calibrated**, or **Underconfident** (Quiz $> 20\%$ above Confidence).
- **First-Party Telemetry Stream**: Live inspectable terminal of buffered telemetry events.

---

## 3. Local Development & Verification Commands

```bash
# Navigate to frontend
cd frontend

# Install dependencies (React 19, Axios, React Router)
npm install

# Start local development server (http://localhost:5173)
npm run dev

# Run production build validation
npm run build
```

Production build compiles in $< 3.5\text{s}$ into `frontend/dist/`.
Contract validation tests run via:
```bash
pytest tests/test_frontend_contracts.py -v
```
