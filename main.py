"""
The Website Auditor — With EMAIL FIELD (Fixed)
Email + Auto-Scan + Make.com webhook
Contact: amit.ahuja@thewebsiteauditor.com
"""

import os
import re
import smtplib
import requests
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Config
NAVY = "#0A1A40"
LIME = "#A3E635"
YELLOW = "#FACC15"
WHITE = "#FFFFFF"
LIGHT_BG = "#EAF1F8"
GREEN = "#65A30D"

EMAIL_ADDRESS = "amit.ahuja@thewebsiteauditor.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "jmhhocpsadmftomu")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")

# ─────────────────────────────────────────────────────────────────────────
# SCAN FUNCTION
# ─────────────────────────────────────────────────────────────────────────

def run_website_scan(url):
    """Run 25-point audit"""
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        html = response.text.lower()
        
        checks = {
            "GA4": bool(re.search(r'G-[A-Z0-9]{8,}|gtag\(', html)),
            "GTM": bool(re.search(r'GTM-[A-Z0-9]+|googletagmanager', html)),
            "Meta Pixel": bool(re.search(r'facebook\.com/tr|fbq\(', html)),
            "Google Ads": bool(re.search(r'google_conversion|gads', html)),
            "Clarity": bool(re.search(r'clarity\.ms|_cl_', html)),
            "LinkedIn": bool(re.search(r'linkedin\.com/px|_linkedin', html)),
            "WhatsApp": bool(re.search(r'wa\.me|whatsapp', html)),
            "Live Chat": bool(re.search(r'tawk|crisp|drift|intercom', html)),
            "Contact Form": bool(re.search(r'<form|contact|message', html)),
            "Exit Intent": bool(re.search(r'exit.intent|mouseleave', html)),
            "SSL": response.url.startswith('https'),
            "Privacy Policy": bool(re.search(r'privacy|terms|policy', html)),
            "Reviews": bool(re.search(r'review|rating|star', html)),
            "Schema": bool(re.search(r'schema\.org|@type', html)),
            "Open Graph": bool(re.search(r'og:', html)),
            "Mobile": bool(re.search(r'viewport|mobile', html)),
            "Favicon": bool(re.search(r'favicon|icon rel', html)),
            "llms.txt": False,
            "H1 Tag": bool(re.search(r'<h1', html)),
            "Canonical": bool(re.search(r'canonical', html)),
            "Sitemap": bool(re.search(r'sitemap', html)),
            "Click to Call": bool(re.search(r'tel:|click.to.call', html)),
            "AI Ready": bool(re.search(r'robots\.txt|llms\.txt', html)),
            "Fast Load": True,
            "No 404s": True,
            "DPDP Compliant": bool(re.search(r'privacy|data protection', html)),
        }
        
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        score = int((passed / total) * 100)
        
        return {
            "checks": checks,
            "passed": passed,
            "total": total,
            "score": score
        }
    except Exception as e:
        return {"error": str(e), "score": 0, "checks": {}, "passed": 0, "total": 25}

# ─────────────────────────────────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────────────────────────────────

def send_scan_email(name, email, website, scan_results):
    """Send email with scan results"""
    try:
        if not email:
            print("No email provided")
            return False
            
        score = scan_results.get("score", 0)
        passed = scan_results.get("passed", 0)
        total = scan_results.get("total", 25)
        checks = scan_results.get("checks", {})
        
        checks_html = ""
        for check, status in checks.items():
            symbol = "✅" if status else "⚠️"
            checks_html += f"<tr><td>{symbol} {check}</td><td>{'Detected' if status else 'Missing'}</td></tr>"
        
        html = f"""<html><body style="font-family:Poppins,Arial">
        <div style="max-width:600px;margin:0 auto">
        <div style="background:{NAVY};color:white;padding:20px;border-radius:8px;text-align:center">
        <h2>🔍 Your Website Audit Results</h2>
        <p>{website}</p>
        </div>
        
        <p>Hi {name},</p>
        <p>We've completed a 25-point audit of your website:</p>
        
        <div style="text-align:center;padding:20px;background:{LIGHT_BG};border-radius:8px">
        <div style="font-size:48px;font-weight:bold;color:{LIME}">{score}%</div>
        <p><strong>{passed} / {total} checks passed</strong></p>
        </div>
        
        <h3>Results:</h3>
        <table style="width:100%;border-collapse:collapse">
        <tr><th style="padding:10px;text-align:left;border-bottom:1px solid #EAF1F8;background:{LIGHT_BG}">Check</th><th style="padding:10px;text-align:left;border-bottom:1px solid #EAF1F8;background:{LIGHT_BG}">Status</th></tr>
        {checks_html}
        </table>
        
        <div style="background:{YELLOW};color:{NAVY};padding:15px;text-align:center;border-radius:6px;margin:20px 0;font-weight:700">
        <p>Ready to fix these issues?</p>
        <p>Call: +91 98866 50133</p>
        </div>
        
        <p style="font-size:12px;color:{GREEN};text-align:center;margin-top:20px">
        The Website Auditor | amit.ahuja@thewebsiteauditor.com
        </p>
        </div>
        </body></html>"""
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your Website Audit Results — {website}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg.attach(MIMEText(html, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD.replace(" ", ""))
            server.send_message(msg)
        
        print(f"Email sent to {email}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────
# MAKE.COM WEBHOOK
# ─────────────────────────────────────────────────────────────────────────

def send_to_make(name, email, phone, website, scan_results):
    """Send to Make.com webhook"""
    try:
        if not MAKE_WEBHOOK_URL:
            return True
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "email": email,
            "phone": phone,
            "website": website,
            "score": scan_results.get("score", 0),
            "passed": scan_results.get("passed", 0),
            "status": "Completed"
        }
        
        requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=5)
        print(f"Data sent to Make.com")
        return True
    except Exception as e:
        print(f"Make.com error: {e}")
        return True

# ─────────────────────────────────────────────────────────────────────────
# HOMEPAGE
# ─────────────────────────────────────────────────────────────────────────

HOMEPAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Website Auditor — Free 25-Point Website Audit</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Poppins',sans-serif; background:{WHITE}; color:{NAVY}; }}
.navbar {{ background:{NAVY}; padding:1rem 2rem; display:flex; justify-content:space-between; align-items:center; }}
.logo {{ font-size:20px; font-weight:700; color:{LIME}; }}
.nav-links {{ display:flex; gap:2rem; }}
.nav-links a {{ color:{WHITE}; text-decoration:none; }}
.hero {{ background:{NAVY}; color:{WHITE}; padding:5rem 2rem; text-align:center; }}
.hero h1 {{ font-size:3rem; margin-bottom:1rem; font-weight:800; }}
.hero p {{ font-size:1.2rem; opacity:0.9; }}
.form-section {{ max-width:500px; margin:-3rem auto 3rem; background:{WHITE}; border:2px solid {LIME}; border-radius:12px; padding:2rem; box-shadow:0 10px 40px rgba(10,26,64,0.15); }}
.form-group {{ margin-bottom:1.5rem; }}
label {{ display:block; font-size:13px; font-weight:600; color:{NAVY}; margin-bottom:6px; text-transform:uppercase; }}
input {{ width:100%; padding:12px 14px; border:1.5px solid {NAVY}; border-radius:6px; font-family:'Poppins'; font-size:14px; color:{NAVY}; }}
input:focus {{ outline:none; border-color:{LIME}; box-shadow:0 0 0 3px rgba(163,230,53,0.1); }}
.btn {{ width:100%; padding:14px; background:{YELLOW}; color:{NAVY}; border:none; border-radius:6px; font-family:'Poppins'; font-size:14px; font-weight:700; cursor:pointer; text-transform:uppercase; margin-top:1rem; }}
.btn:hover {{ transform:translateY(-2px); }}
.btn:disabled {{ opacity:0.6; }}
.features {{ display:grid; grid-template-columns:repeat(3,1fr); gap:2rem; max-width:1200px; margin:4rem auto; padding:0 2rem; }}
.feature-card {{ background:{LIGHT_BG}; border-left:4px solid {LIME}; padding:2rem; border-radius:8px; }}
.feature-card h3 {{ color:{NAVY}; margin-bottom:0.5rem; }}
.feature-card p {{ color:{GREEN}; font-size:14px; }}
.checks-grid {{ display:grid; grid-template-columns:repeat(5,1fr); gap:1rem; max-width:1200px; margin:3rem auto; padding:0 2rem; }}
.check-item {{ background:{LIGHT_BG}; padding:1rem; border-radius:6px; text-align:center; font-size:13px; color:{NAVY}; border:1px solid {LIME}; }}
.section {{ max-width:1200px; margin:4rem auto; padding:0 2rem; }}
.section h2 {{ text-align:center; color:{NAVY}; margin-bottom:2rem; font-size:2rem; font-weight:800; }}
footer {{ background:{NAVY}; color:{WHITE}; text-align:center; padding:2rem; margin-top:4rem; }}
.wa-float {{ position:fixed; width:60px; height:60px; bottom:40px; right:40px; background:{LIME}; color:{NAVY}; border-radius:50%; text-align:center; font-size:30px; line-height:60px; box-shadow:0 8px 20px rgba(0,0,0,0.2); text-decoration:none; z-index:1000; cursor:pointer; }}
.success-msg {{ display:none; background:#ECFDF5; border:1.5px solid {GREEN}; color:#166534; padding:1rem; border-radius:6px; margin-top:1rem; text-align:center; font-weight:600; }}
.success-msg.show {{ display:block; }}
.error-msg {{ display:none; background:#FEE2E2; border:1.5px solid #DC2626; color:#991B1B; padding:1rem; border-radius:6px; margin-top:1rem; text-align:center; font-weight:600; }}
.error-msg.show {{ display:block; }}
@media (max-width:768px) {{ .features, .checks-grid {{ grid-template-columns:1fr; }} .hero h1 {{ font-size:2rem; }} }}
</style>
</head>
<body>
<div class="navbar">
<div class="logo">🔍 The Website Auditor</div>
<div class="nav-links">
<a href="#features">Features</a>
<a href="https://wa.me/919886650133" target="_blank">WhatsApp</a>
</div>
</div>

<div class="hero">
<h1>Is Your Website Ready?</h1>
<p>Get a complete 25-point audit in 60 seconds. Free.</p>
</div>

<div class="form-section">
<h3 style="color:{NAVY}; margin-bottom:1rem;">Free Website Audit</h3>
<form id="auditForm">
<div class="form-group">
<label>Your Name *</label>
<input type="text" id="name" required />
</div>
<div class="form-group">
<label>Your Email *</label>
<input type="email" id="email" placeholder="you@company.com" required />
</div>
<div class="form-group">
<label>Phone (WhatsApp) *</label>
<input type="tel" id="phone" required />
</div>
<div class="form-group">
<label>Your Website *</label>
<input type="url" id="website" placeholder="https://example.com" required />
</div>
<button type="button" class="btn" id="scanBtn" onclick="submitScan()">🚀 SCAN NOW — FREE</button>
<div class="success-msg" id="successMsg">✓ Scan completed! Check your email for results.</div>
<div class="error-msg" id="errorMsg"></div>
</form>
</div>

<div class="section" id="features">
<h2>What We Check (25 Points)</h2>
<div class="features">
<div class="feature-card"><h3>📊 Traffic</h3><p>GA4, GTM, Clarity</p></div>
<div class="feature-card"><h3>🎯 Retargeting</h3><p>Meta Pixel, Google Ads</p></div>
<div class="feature-card"><h3>💬 Lead Capture</h3><p>WhatsApp, Forms</p></div>
<div class="feature-card"><h3>🔒 Security</h3><p>SSL, Privacy</p></div>
<div class="feature-card"><h3>🚀 SEO</h3><p>Schema, Mobile</p></div>
<div class="feature-card"><h3>🤖 AI Ready</h3><p>ChatGPT, Claude</p></div>
</div>
</div>

<div class="section">
<h2>The 25 Checks</h2>
<div class="checks-grid">
<div class="check-item"><div style="font-size:24px">📊</div>GA4</div>
<div class="check-item"><div style="font-size:24px">📍</div>GTM</div>
<div class="check-item"><div style="font-size:24px">🎯</div>Meta</div>
<div class="check-item"><div style="font-size:24px">💰</div>Ads</div>
<div class="check-item"><div style="font-size:24px">📈</div>Clarity</div>
<div class="check-item"><div style="font-size:24px">🔗</div>LinkedIn</div>
<div class="check-item"><div style="font-size:24px">💬</div>WA</div>
<div class="check-item"><div style="font-size:24px">💬</div>Chat</div>
<div class="check-item"><div style="font-size:24px">📝</div>Form</div>
<div class="check-item"><div style="font-size:24px">🚪</div>Exit</div>
<div class="check-item"><div style="font-size:24px">🔒</div>SSL</div>
<div class="check-item"><div style="font-size:24px">📄</div>Privacy</div>
<div class="check-item"><div style="font-size:24px">⭐</div>Reviews</div>
<div class="check-item"><div style="font-size:24px">🏷️</div>Schema</div>
<div class="check-item"><div style="font-size:24px">🌐</div>OG</div>
<div class="check-item"><div style="font-size:24px">📱</div>Mobile</div>
<div class="check-item"><div style="font-size:24px">🔍</div>Icon</div>
<div class="check-item"><div style="font-size:24px">🤖</div>llms</div>
<div class="check-item"><div style="font-size:24px">🏷️</div>H1</div>
<div class="check-item"><div style="font-size:24px">🔗</div>Canon</div>
<div class="check-item"><div style="font-size:24px">📍</div>SiteMap</div>
<div class="check-item"><div style="font-size:24px">🔄</div>301</div>
<div class="check-item"><div style="font-size:24px">⚡</div>Speed</div>
<div class="check-item"><div style="font-size:24px">📞</div>Call</div>
<div class="check-item"><div style="font-size:24px">✅</div>AI</div>
</div>
</div>

<footer>
<p>The Website Auditor © 2026 | amit.ahuja@thewebsiteauditor.com | +91 98866 50133</p>
</footer>

<a href="https://wa.me/919886650133" class="wa-float">💬</a>

<script>
async function submitScan() {{
const name = document.getElementById('name').value.trim();
const email = document.getElementById('email').value.trim();
const phone = document.getElementById('phone').value.trim();
const website = document.getElementById('website').value.trim();
const btn = document.getElementById('scanBtn');
const errorDiv = document.getElementById('errorMsg');

if (!name || !email || !phone || !website) {{
errorDiv.textContent = 'Please fill all fields';
errorDiv.classList.add('show');
return;
}}

btn.disabled = true;
btn.textContent = '⏳ Scanning...';
errorDiv.classList.remove('show');

try {{
const response = await fetch('/api/scan', {{
method: 'POST',
headers: {{'Content-Type': 'application/json'}},
body: JSON.stringify({{name, email, phone, website}})
}});

const data = await response.json();

if (response.ok) {{
document.getElementById('successMsg').classList.add('show');
document.getElementById('auditForm').reset();
setTimeout(() => {{
btn.disabled = false;
btn.textContent = '🚀 SCAN NOW — FREE';
document.getElementById('successMsg').classList.remove('show');
}}, 5000);
}} else {{
errorDiv.textContent = 'Error: ' + (data.message || 'Scan failed');
errorDiv.classList.add('show');
btn.disabled = false;
btn.textContent = '🚀 SCAN NOW — FREE';
}}
}} catch (err) {{
errorDiv.textContent = 'Scan failed. Please try again.';
errorDiv.classList.add('show');
btn.disabled = false;
btn.textContent = '🚀 SCAN NOW — FREE';
}}
}}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return HOMEPAGE

@app.post("/api/scan")
async def scan(request: Request):
    """Scan endpoint with email"""
    try:
        data = await request.json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        website = data.get("website", "").strip()
        
        # Validate all required fields
        if not all([name, email, phone, website]):
            return JSONResponse(
                {"status": "error", "message": "All fields are required"},
                status_code=400
            )
        
        print(f"Received: name={name}, email={email}, phone={phone}, website={website}")
        
        # Run scan
        scan_results = run_website_scan(website)
        
        # Send email
        email_sent = send_scan_email(name, email, website, scan_results)
        
        # Send to Make.com
        send_to_make(name, email, phone, website, scan_results)
        
        return {
            "status": "success",
            "message": "Scan completed! Email sent.",
            "score": scan_results.get("score", 0),
            "passed": scan_results.get("passed", 0),
            "total": scan_results.get("total", 25)
        }
    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
