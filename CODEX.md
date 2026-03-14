# CODEX Project Memory - web-ai-agent

This file stores the current project state so future sessions can continue without re-discovery.

## 1) Project Goal and Current Product

The repository has been transformed from a Gradio chat demo into a business website for:

- Valerio Giuseppe Scaglione Fliesenlegerei (Wuppertal)

Current website structure:

- Startseite (`/`)
- Ueber uns (`/ueber-uns`)
- Anfrage stellen (`/anfrage-stellen`)
- Kontakt (`/kontakt`)
- Live Chat (`/live-chat`)
- Footer pages: Impressum (`/impressum`), Datenschutz (`/datenschutz`)

Primary language/content style is German.

## 2) Tech Stack and Runtime

- Backend: Flask (`app.py`)
- Templates: Jinja2 in `templates/`
- Static assets: `static/`
- AI chat backend: LangChain + Anthropic + DuckDuckGo search tool
- Deployment target: Render (existing service)
- Production URL: `https://web-ai-agent.onrender.com`

Runtime env vars expected:

- Required: `ANTHROPIC_API_KEY`
- Optional: `PORT` (default 7860)

## 3) Files and Responsibilities

### Core backend

- `app.py`
  - Defines all page routes
  - Defines `/api/chat` POST endpoint
  - Uses fixed model ID: `claude-haiku-4-5-20251001`
  - Handles API errors and always returns JSON from chat endpoint

### Chat prompt

- `prompt.txt`
  - Now tailored for Fliesenleger guidance
  - Instructs assistant to answer tiling questions and always guide user to contact Scaglione

### Dependencies

- `requirements.txt`
  - Flask + LangChain + Anthropic + search dependencies

### Templates

- `templates/base.html`: global layout/header/footer/nav
- `templates/startseite.html`: hero + service cards
- `templates/ueber_uns.html`: company/about content
- `templates/anfrage_stellen.html`: form UI only (no submit backend yet)
- `templates/kontakt.html`: contact details
- `templates/live_chat.html`: chat page UI shell
- `templates/impressum.html`
- `templates/datenschutz.html`

### Styling and behavior

- `static/css/style.css`
  - White/grey/blue visual system
  - Greyer background
  - Blue header
  - Responsive layout
- `static/js/chat.js`
  - Sends requests to `/api/chat`
  - Maintains local history array
  - Robust handling for non-JSON / server errors

### Logo

- Source uploaded by user: `assets/logo_fliesen.png`
- Active file used in header: `static/images/logo_fliesen.png`
- Displayed in header next to name via `templates/base.html`

## 4) Business Data in App

Hardcoded in `BUSINESS` dictionary in `app.py`:

- Name: Valerio Giuseppe Scaglione Fliesenlegerei
- Owner: Valerio Scaglione
- Phone: +49 202 478880
- Address: Varresbecker Str. 193, 42115 Wuppertal

Service list (used on Startseite):

- Fliesenverlegung
- Badsanierung
- Naturstein- und Mosaikarbeiten
- Reparatur- und Ausbesserungsarbeiten
- Beratung und Aufmass

## 5) Known Decisions Taken

- The old Gradio UI was replaced by normal multipage Flask website.
- Live Chat remains a real AI chat feature (not placeholder).
- Chat prompt was migrated from beauty-domain content to tiling-domain content.
- Model is fixed by user request to `claude-haiku-4-5-20251001`.
- Model is intentionally NOT environment-configured (user preference).
- Anfrage page currently has UI only and intentionally no submit handling.

## 6) Common Errors and Current Handling

### Error seen previously

- `Unexpected token '<' ... is not valid JSON`
  - Cause: frontend attempted JSON parse on HTML error response.
  - Fix: backend now returns JSON errors, frontend checks content-type and handles parse failures gracefully.

### Error seen previously

- Anthropic 404 not_found for some model IDs.
  - Current state: fixed model ID set to `claude-haiku-4-5-20251001` per user request.

## 7) Local Development Workflow

Conda example:

```bash
cd /Users/oliver-jan.jarosik/git/web-ai-agent
conda create -n web-ai-agent python=3.11 -y
conda activate web-ai-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY="..."
python app.py
```

Open:

- `http://localhost:7860/`
- `http://localhost:7860/live-chat`
- `https://web-ai-agent.onrender.com/`
- `https://web-ai-agent.onrender.com/live-chat`

## 8) Deploy Workflow (Render)

Current deployed site:

- `https://web-ai-agent.onrender.com`

Typical push flow:

```bash
git add .
git commit -m "..."
git push origin main
```

Render should auto-deploy from GitHub integration.

## 9) Suggested Next Improvements (Backlog)

- Implement actual submit backend for `Anfrage stellen` (email/CRM webhook).
- Replace placeholder hero image with real project photos.
- Expand legal texts for production-grade compliance.
- Add spam protection/rate limiting for `/api/chat`.
- Optional: add chat widget fixed bottom-right globally (user mentioned as possible future direction).

## 10) Important Note for Future Sessions

When continuing this project, treat `CODEX.md` as the source of truth for:

- current architecture,
- user preferences,
- model choice decision,
- and pending roadmap.

If any conflict appears between memory and code, code currently wins; then update this file.
