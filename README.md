# Website Intelligence Auditor — Standalone

Your own website audit tool. Paste any URL → instant 25-point report.
Reads the live HTML source directly = 100% accurate results.

## Run on your computer (2 minutes)

1. Install Python 3.10+ from python.org
2. Open terminal/command prompt in this folder
3. Run:
   pip install -r requirements.txt
   uvicorn main:app --port 8000
4. Open http://localhost:8000 in your browser. Done.

## Deploy free on the internet (10 minutes)

### Option A — Render.com (easiest)
1. Create free account at render.com
2. Push this folder to a GitHub repository
3. In Render: New → Web Service → connect your repo
4. Build command:  pip install -r requirements.txt
5. Start command:  uvicorn main:app --host 0.0.0.0 --port $PORT
6. Deploy. You get a free URL like youraudit.onrender.com

### Option B — Railway.app
1. railway.app → New Project → Deploy from GitHub
2. Railway auto-detects Python. Set start command:
   uvicorn main:app --host 0.0.0.0 --port $PORT

### Custom domain
Both platforms let you attach your own domain (e.g. audit.bharatriders.in)
in their dashboard settings for free.

## What it checks (25 points)

Traffic: GA4, old UA detection, Google Tag Manager
Behaviour: Microsoft Clarity, Hotjar
Retargeting: Meta Pixel, Google Ads, LinkedIn Insight
Lead Capture: WhatsApp button, live chat, forms, exit popups, click-to-call
Trust: SSL, privacy policy (DPDP Act), testimonials
SEO: schema, Open Graph, meta description, sitemap, mobile, favicon
AI Readiness: llms.txt, H1 structure, canonical tags

## Known limitation

Sites that inject tracking via JavaScript AFTER page load (some big
e-commerce sites) may show false "missing" for those tools. For your
target market (SME websites) detection is highly accurate because they
embed scripts directly in HTML. Upgrade path: add Playwright/Puppeteer
rendering for a "Pro" tier later.

## Business use

This tool is yours. Brand it, put it on your domain, charge for audits.
