# CODEX Project Memory - web-ai-agent

This file stores the current project state so future sessions can continue without re-discovery.

## 1) Project Goal and Current Product

The repository is a Flask/Jinja business website for:

- Valerio Giuseppe Scaglione Fliesenlegerei (Wuppertal)

Primary language/content style is German.

Current routes still exist as separate Flask pages:

- Startseite (`/`)
- Ueber uns (`/ueber-uns`)
- Anfrage stellen (`/anfrage-stellen`)
- Kontakt (`/kontakt`)
- Live Chat (`/live-chat`)
- Footer pages: Impressum (`/impressum`), Datenschutz (`/datenschutz`)

Important current UX decision:

- The main navigation now behaves like a one-page website and links to anchored sections on the Startseite.
- Users can scroll from top to bottom through the main content flow on `/`.
- The standalone routes still exist and still render.

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
  - Stores business data including service area, hours, and Google Maps embed URL

### Chat prompt

- `prompt.txt`
  - Tailored for Fliesenleger guidance
  - Instructs assistant to answer tiling questions and guide users to direct contact

### Dependencies

- `requirements.txt`
  - Flask + LangChain + Anthropic + search dependencies

### Templates

- `templates/base.html`
  - Global layout/header/footer/nav
  - Nav now points to Startseite anchor sections instead of route-first navigation
- `templates/startseite.html`
  - Main one-page flow
  - Includes hero, services, why-us, process, ueber-uns section, anfrage section, live-chat section, kontakt section, final CTA
  - Includes chat JS because the live chat is embedded on the homepage
- `templates/ueber_uns.html`
  - Standalone about page
- `templates/anfrage_stellen.html`
  - Standalone inquiry page
- `templates/kontakt.html`
  - Standalone contact page
  - Uses a two-column layout with contact card + embedded Google Map iframe
- `templates/live_chat.html`
  - Standalone chat page UI shell
- `templates/impressum.html`
- `templates/datenschutz.html`

### Styling and behavior

- `static/css/style.css`
  - Current design direction is deep blue + white + light blue
  - Dark blue header
  - Full-width section blocks / tile-like strips
  - Less rounded, more squared visual language
  - Header is no longer sticky
  - Mobile topbar is hidden
  - Footer is full-width and visually integrated with the page
- `static/js/chat.js`
  - Sends requests to `/api/chat`
  - Maintains local history array
  - Robust handling for non-JSON / server errors
  - Used both on standalone Live Chat page and embedded homepage section

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
- Service area: Wuppertal und Umgebung
- Hours note: Termine nach Vereinbarung
- Maps embed URL: Google Maps embed based on business address

Service list (used on Startseite):

- Fliesenverlegung
- Badsanierung
- Naturstein- und Mosaikarbeiten
- Reparatur- und Ausbesserungsarbeiten
- Beratung und Aufmass

## 5) Current Design Decisions

- Main color direction: dark deep blue, white, light blue
- Homepage section flow:
  - dark hero
  - white block
  - dark blue block
  - pale blue block
  - additional anchored content sections below
- Large rounded cards were intentionally reduced in favor of more squared "tile" sections
- Header should not stick while scrolling
- Footer and hero should visually stretch full width
- Contact style was partially inspired by local repo `git/gelenkwerk-physio`
  - especially the contact card + embedded map composition

## 6) Known Decisions Taken

- The old Gradio UI was replaced by normal multipage Flask website.
- Live Chat remains a real AI chat feature, not a placeholder.
- Chat prompt was migrated from beauty-domain content to tiling-domain content.
- Model is fixed by user request to `claude-haiku-4-5-20251001`.
- Model is intentionally NOT environment-configured.
- Separate routes remain available even though the homepage now acts like a one-page scroll experience.

## 7) Open UX / Content Notes

This is important for the next session:

- User explicitly said the website currently feels a bit text-bloated.
- Next design/content pass should remove some explanatory copy and shorten sections.
- User liked the current direction overall, but wants less text density.
- User also asked for smaller typography, especially in the footer, and that work has already been started.

## 8) Common Errors and Current Handling

### Error seen previously

- `Unexpected token '<' ... is not valid JSON`
  - Cause: frontend attempted JSON parse on HTML error response.
  - Fix: backend now returns JSON errors, frontend checks content-type and handles parse failures gracefully.

### Error seen previously

- Anthropic 404 not_found for some model IDs.
  - Current state: fixed model ID set to `claude-haiku-4-5-20251001` per user request.

## 9) Local Development Workflow

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

## 10) Deploy Workflow (Render)

Current deployed site:

- `https://web-ai-agent.onrender.com`

Typical push flow:

```bash
git add .
git commit -m "..."
git push origin main
```

Render should auto-deploy from GitHub integration.

## 11) Suggested Next Improvements (Backlog)

- Reduce text density on homepage and subpages
- Tighten spacing and simplify copy in sections that feel too explanatory
- If needed, unify remaining typography sizing across all templates
- Implement actual submit backend for `Anfrage stellen` (email/CRM webhook)
- Replace placeholder hero image treatment with real project photos
- Expand legal texts for production-grade compliance
- Add spam protection/rate limiting for `/api/chat`

## 12) Important Note for Future Sessions

When continuing this project, treat `CODEX.md` as the source of truth for:

- current architecture,
- user preferences,
- model choice decision,
- design direction,
- and pending roadmap.

If any conflict appears between memory and code, code currently wins; then update this file.
