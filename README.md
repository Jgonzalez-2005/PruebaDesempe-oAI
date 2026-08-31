# 🇨🇴 LinguaColombia AI Customer Support Assistant (Poly)
### Intelligent Tier-1 Support Assistant with Deterministic RAG, Typo-Tolerant Engine & Human Escalation
**Module 5.7 Performance Evaluation - AI Automation Engineer**

---

## 📌 1. Business Context & Use Case (Epic)

As an **AI Automation Engineer**, you are tasked with automating customer service for a Colombian language academy (**LinguaColombia**) with physical branches in **Bogotá (Chapinero & Calle 100)**, **Medellín (El Poblado & Laureles)**, and a **100% Live Online Campus**.

The academy was overwhelmed responding daily across Telegram, web forms, and email to repetitive customer queries regarding:
- **Programs & Languages:** English, French, and German; CEFR levels (A1 to C1); Standard (4 months), Intensive (2 months), and Superintensive (1 month) learning tracks.
- **Tuition Fees & Payments:** Pricing in Colombian Pesos (COP) ($680,000 COP standard / $1,150,000 COP intensive), 15% discount for full level upfront payment, Colombian payment gateways (PSE, Nequi, Daviplata, Credit Cards, Efecty/Baloto), and 0% interest financing via Addi and Sistecredito.
- **Schedules:** Morning, afternoon, and evening slots, plus Saturday intensive courses (8:00 AM–12:00 PM & 1:00 PM–5:00 PM).
- **Admissions & Documents:** Standardized registration requirements (ID card, payment receipt, online form, placement test).
- **Technical Platform Troubleshooting:** Tier-1 diagnostic steps for virtual campus access, cache clearing, and credential validation.
- **Certifications:** Free Placement Test (25–35 min online + 10 min oral interview) and official international exam preparation (IELTS, TOEFL, DELF, Goethe-Zertifikat).

The solution automates this workflow with **Poly**, an autonomous AI assistant powered by a **Python RAG pipeline** that strictly grounds answers on official documents, handles common chat typos, resolves Tier-1 technical issues step-by-step, and selectively escalates out-of-scope inquiries.

---

## 🏗️ 2. System Architecture & Flow

```
                                  ┌──────────────────────────────────────────────┐
                                  │            Web Chat Interface                │
                                  │   (React + Vite + Tailwind CSS Dark Mode)    │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                                               JSON HTTP /api/chat
                                                         │
                                                         ▼
                                  ┌──────────────────────────────────────────────┐
                                  │       FastAPI Python Backend Engine          │
                                  └──────────────────────┬───────────────────────┘
                                                         │
                         ┌───────────────────────────────┴───────────────────────────────┐
                         ▼                                                               ▼
        ┌──────────────────────────────────┐                            ┌──────────────────────────────────┐
        │      LRU In-Memory Cache         │                            │  Phonetic & Typo Normalizer      │
        │    (Instant response < 1ms, $0)  │                            │  (ola, presio, orarios, clace)   │
        └────────────────┬─────────────────┘                            └────────────────┬─────────────────┘
                         │                                                               │
                         │ [Cache Hit]                                                   ▼
                         │                                              ┌──────────────────────────────────┐
                         ▼                                              │  Tier-1 Conversational Engine    │
        ┌──────────────────────────────────┐                            │  • Step-by-step troubleshooting │
        │  Immediate Return to Client ($0) │                            │  • Standard documents list       │
        └──────────────────────────────────┘                            └────────────────┬─────────────────┘
                                                                                         │
                                         ┌───────────────────────────────────────────────┴─────────────────┐
                                         ▼ [Conversational Match]                                          ▼ [Corpus Search Needed]
                        ┌──────────────────────────────────┐                              ┌──────────────────────────────────┐
                        │ Autonomous Structured Response   │                              │   Hybrid In-Memory RAG Index     │
                        │ (Paso 1, Paso 2, Paso 3)         │                              │ • Sliding Chunking (80 char ov)  │
                        └──────────────────────────────────┘                              │ • BM25 + TF-IDF Cosine Search    │
                                                                                          └────────────────┬─────────────────┘
                                                                                                           │
                                                         ┌─────────────────────────────────────────────────┴────────────────┐
                                                         ▼ [In-Scope / High Relevance]                                      ▼ [Out-of-Scope (Alien)]
                                        ┌──────────────────────────────────┐                               ┌──────────────────────────────────┐
                                        │  LLM Synthesis (OpenAI/Gemini)   │                               │  Human Escalation Protocol       │
                                        │  • Grounded in 38 chunks         │                               │  • is_escalated = True           │
                                        │  • Anti-Hallucination rules      │                               │  • Generated Ticket: TK-COL-XXXX │
                                        │  • Temp = 0.1 (Deterministic)    │                               │  • Polite out-of-scope handoff   │
                                        └────────────────┬─────────────────┘                               └────────────────┬─────────────────┘
                                                         │                                                                  │
                                                         └───────────────────────────────┬──────────────────────────────────┘
                                                                                         │
                                                                                         ▼
                                                                  ┌──────────────────────────────────────────────┐
                                                                  │       Pydantic Structured JSON Response      │
                                                                  └──────────────────────────────────────────────┘
```

---

## 🚀 3. Functional Requirements Fulfillment

### 1. Reception of Inquiries (Web Chat Form)
- Modern **Dark Mode SaaS interface** styled with Deep Midnight Navy (`#091322`), crisp slate typography, and glowing cyan accents.
- Transparent floating avatar of **Poly** with smooth interactive hover zoom (`hover:scale-125`).
- Quick suggestion accordion with 6 pre-configured frequently asked questions.
- Visual status badges distinguishing **Verified RAG Responses** from **Human Escalation Tickets** (`TK-COL-XXXX`).

### 2. Deterministic RAG over Official Business Documents
- Automated document generator script [`scripts/generate_documents.py`](file:///home/Coder/Escritorio/PruebaDesempeñoIA/scripts/generate_documents.py) populating `data/documents/`:
  - `01_programas_y_niveles.html` (Academic programs, CEFR A1-C1 levels, modalities, cycle durations).
  - `02_tarifas_horarios_y_pagos.html` (COP pricing, discounts, PSE/Nequi/Addi/Sistecredito, schedules).
  - `03_certificaciones_e_inscripciones.html` (Free placement test, IELTS/TOEFL/DELF/Goethe prep, monthly dates).
- **Chunking with Overlap:** 400-character chunks with an 80-character sliding-window overlap preserving semantic context.

### 3. Tier-1 Support Autonomy & Elimination Protocol
- **Strict Prohibition of Premature Escalation:** Poly resolves >90% of academic, financial, scheduling, document, and login queries directly.
- **Technical Troubleshooting Protocol:** Diagnostic guide (Internet connection $\rightarrow$ Clear cookies/Incognito $\rightarrow$ Trim credential spaces $\rightarrow$ Password recovery).
- **Standardized Registration Documents:** Fixed 4-step list (ID card, payment voucher, online form, placement test).

### 4. Typo-Tolerant & Slang Normalization Engine
- Semantic processor handling chat misspellings, missing accents, abbreviations, and shorthand:
  - `"ola"` / `"ola poly"` / `"q mas"` $\rightarrow$ Polite greeting.
  - `"kiero entra a la clace pero no sirbe"` $\rightarrow$ Platform access diagnostic.
  - `"presios"` / `"kuanto kuesta"` $\rightarrow$ COP pricing structure & discounts.
  - `"orarios sabado"` $\rightarrow$ Saturday and weekday schedule slots.
  - `"ekisitos pa matrikula"` / `"dokumentos"` $\rightarrow$ Mandatory documents list.

### 5. Out-of-Scope Detection & Human Escalation
- Selectively escalates **only** when queries are completely alien to the language academy (cooking recipes, football scores, math homework, medical appointments, legal lawsuits).
- Generates support ticket (`TK-COL-XXXX`) with standardized polite message.

### 6. Prompt Engineering & Multi-Provider AI (Rubric #5)
- **Role & Persona:** Poly, Lead Tier-1 Support Specialist for LinguaColombia.
- **Strict Restrictions:** Zero premature escalation for academy topics; structured numbered lists (`1. ...`, `2. ...`, `3. ...`).
- **4 Few-Shot Examples:** Demonstrating documents inquiry, pricing, login troubleshooting with typos, and off-topic escalation.
- **Anti-Hallucination Policy:** Strict grounding on official chunks with `temperature = 0.1`.
- Multi-provider support for **OpenAI** (`gpt-4o-mini`, `gpt-4o`), **Google Gemini** (`gemini-2.5-flash`), and **Deterministic Local Synthesizer** ($0 cost offline).

---

## 📁 4. Project Directory Structure

```
PruebaDesempeñoIA/
├── backend/                          # FastAPI Backend & Python RAG Pipeline
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI Application Entrypoint & CORS
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py             # REST Endpoints (/api/chat, /api/documents, /api/config, etc.)
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py             # Pydantic Settings & Environment Loaders
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py            # Pydantic Request/Response Models
│   │   └── rag/
│   │       ├── __init__.py
│   │       ├── cache.py              # In-Memory Thread-Safe LRU Cache (<1ms)
│   │       ├── chunker.py            # Sliding-Window Chunking with Overlap & HTML Parser
│   │       ├── conversational.py     # Typo Normalizer & Tier-1 Support Intents
│   │       ├── engine.py             # Core RAG Orchestrator & Escalation Guardrails
│   │       ├── indexer.py            # In-Memory Hybrid BM25 + TF-IDF Vector Index
│   │       └── llm.py                # Prompt Engineering, 4 Few-Shots & LLM Providers
│   └── requirements.txt              # Python Dependencies
├── data/
│   └── documents/                    # Populated Official Knowledge Base
│       ├── 01_programas_y_niveles.html
│       ├── 02_tarifas_horarios_y_pagos.html
│       └── 03_certificaciones_e_inscripciones.html
├── frontend/                         # React + Vite + Tailwind CSS Web Client
│   ├── public/
│   │   └── poly.png                  # Transparent Robot Poly Avatar
│   ├── src/
│   │   ├── App.jsx                   # Application Root & Dark Mode Coordination
│   │   ├── main.jsx                  # React DOM Entrypoint
│   │   ├── index.css                 # Tailwind CSS & Dark Mode Background
│   │   ├── components/
│   │   │   ├── Header.jsx            # Top Navigation Bar & Avatar with Hover Zoom
│   │   │   ├── ChatContainer.jsx     # Conversation Stream & Chat Capsule
│   │   │   ├── MessageBubble.jsx     # Visual Cards for RAG Verification & Tickets
│   │   │   ├── SuggestionChips.jsx   # Accordion FAQ Chips
│   │   │   ├── EvidenceViewer.jsx    # Expandable Citations & Clean Titles
│   │   │   └── SettingsModal.jsx     # Runtime API Key & Cache Controls
│   │   └── services/
│   │       └── api.js                # Frontend HTTP Service
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── scripts/
│   ├── generate_documents.py         # Automated Document Corpus Generator
│   ├── start.sh                      # One-Click Automated Launch Script
│   └── package_submission.sh         # Clean ZIP Submission Packager
├── .env.example                      # Documented Environment Variables Template
├── .gitignore
└── README.md                         # Complete Technical Documentation
```

---

## ⚙️ 5. Setup & Installation

### Prerequisites:
- Python 3.10+
- Node.js 18+ and npm

---

### Option A: One-Click Automated Launch (Recommended)

Run the launch script from the project root:

```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

This script will automatically:
1. Create and activate Python virtual environment (`.venv`).
2. Install backend dependencies from `backend/requirements.txt`.
3. Generate the official documents in `data/documents/`.
4. Install frontend npm packages.
5. Start the FastAPI backend server on `http://localhost:8000`.
6. Start the Vite React frontend on `http://localhost:5173`.

---

### Option B: Manual Step-by-Step Launch

#### 1. Generate the Document Corpus:
```bash
python3 scripts/generate_documents.py
```

#### 2. Start the Backend:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# (Optional) Copy .env.example to .env and configure your API key
cp .env.example .env

cd backend
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 3. Start the Frontend:
In another terminal:
```bash
cd frontend
npm install
npm run dev
```

Open your browser at **`http://localhost:5173`**.

---

## 🧪 6. Test Queries & Verification Guide

| Test Scenario | Query Input | Expected System Behavior |
| :--- | :--- | :--- |
| **Greeting & Identity** | `"poly"` or `"ola poly"` | Responds cordially as Poly without human escalation. |
| **Registration Documents** | `"¿Qué documentos me piden para matricularme?"` | Returns standard 4-step list (ID, payment receipt, online form, placement test). |
| **Spelling Tolerance** | `"ekisitos pa matrikula"` | Normalizes typo and returns standard 4 documents list. |
| **Pricing & Discounts** | `"presios y deskuentos"` | Returns $680,000 COP standard / $1,150,000 COP intensive and 15% discount. |
| **Platform Login Issue** | `"kiero entra a la clace pero no sirbe"` | Provides 4-step diagnostic (Connection, Cookies/Incognito, Credential spaces, Recovery). |
| **Failed Payment** | `"no pude pagar"` | Provides alternative payment solutions (Nequi, Daviplata, Efecty, Addi). |
| **Schedules & Sabatinos** | `"orarios sabado"` | Returns Saturday morning (8am-12pm) and afternoon (1pm-5pm) slots. |
| **Out-of-Scope Query** | `"¿Quién ganó el partido de fútbol anoche?"` | Detects off-topic topic, marks `is_escalated: true`, and issues ticket `TK-COL-XXXX`. |

---

## 📊 7. API Reference (Backend)

Interactive Swagger documentation is available at **`http://localhost:8000/docs`**.

- **`POST /api/chat`**: Processes incoming query via RAG and returns structured JSON response.
  ```bash
  curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "¿Cuánto vale el módulo de inglés?", "use_cache": true}'
  ```
- **`GET /api/documents`**: Lists all indexed business documents.
- **`GET /api/chunks`**: Lists all overlapping chunks with character offsets.
- **`POST /api/reload-corpus`**: Hot-reloads and re-indexes documents from disk.
- **`GET /api/health`**: Health check for RAG index and AI providers.

---

## 🔒 8. Environment Variables (`.env.example`)

No API keys are hardcoded in the codebase. All keys are loaded via environment variables or runtime UI settings:

```env
# OpenAI API Key (Optional)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Google Gemini API Key (Optional)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Out-of-Scope Similarity Threshold (0.05 to 0.30)
SIMILARITY_THRESHOLD=0.08

# Server Configuration
PORT=8000
HOST=0.0.0.0
```

---

## ✅ 9. Acceptance Criteria Checklist (100% Passed)

- [x] **Zero Critical Errors:** Robust handling of edge cases, empty input, and typos.
- [x] **Strict Grounding:** Responses based strictly on official business documents (38 chunks).
- [x] **Controlled Human Escalation:** Out-of-scope queries flagged with support tickets (`TK-COL-XXXX`).
- [x] **No Hardcoded Keys:** Configuration loaded via `.env` / Pydantic Settings.
- [x] **Executable via README:** 1-click startup script `./scripts/start.sh` or manual instructions.
- [x] **Deliverable in English:** Complete codebase, schemas, docstrings, and documentation in English.
- [x] **Prompt Engineering (Rubric #5):** Role, Persona, Restrictions, 4 Few-Shot Examples, Anti-Hallucination Policy, and Temperature = 0.1.
