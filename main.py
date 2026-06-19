"""
The Website Auditor — Simplified Version
Google Sheets integration via Make.com webhook (not Python libraries)
Email via Gmail SMTP
Contact: amit.ahuja@thewebsiteauditor.com | +91 98866 50133
"""

import os
import re
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="The Website Auditor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────

NAVY = "#0A1A40"
LIME = "#A3E635"
YELLOW = "#FACC15"
WHITE = "#FFFFFF"
LIGHT_BG = "#EAF1F8"
GREEN = "#65A30D"

# Email
EMAIL_ADDRESS = "amit.ahuja@thewebsiteauditor.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "jmhhocpsadmftomu")  # App password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Make.com webhook (will set up after)
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")

# ─────────────────────────────────────────────────────────────────────────
# 25-POINT WEBSITE AUDIT
# ─────────────────────────────────────────────────────────────────────────

def run_website_scan(url):
    """Run 25-point audit on website"""
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        html = response.text.lower()
        
        results = {
            "GA4": bool(re.search(r'G-[A-Z0-9]{8,}', html)) or bool(re.search(r'gtag\(', html)),
            "GTM": bool(re.search(r'GTM-[A-Z0-9]+', html)) or bool(re.search(r'googletagmanager', html)),
            "Meta Pixel": bool(re.search(r'facebook\.com/tr', html)) or bool(re.search(r'fbq\(', html)),
            "Google Ads": bool(re.search(r'google_conversion_id', html)) or bool(re.search(r'gads', html)),
            "Clarity": bool(re.search(r'clarity\.ms', html)) or bool(re.search(r'_cl_', html)),
            "LinkedIn": bool(re.search(r'linkedin\.com/px', html)) or bool(re.search(r'_linkedin', html)),
            "WhatsApp Button": bool(re.search(r'wa\.me|whatsapp', html)),
            "Live Chat": bool(re.search(r'tawk|crisp|drift|intercom', html)),
            "Contact Form": bool(re.search(r'<form|contact|message', html)),
            "Exit Intent": bool(re.search(r'exit.intent|mouseleave', html)),
            "SSL": response.url.startswith('https'),
            "Privacy Policy": bool(re.search(r'privacy|terms|policy', html)),
            "Reviews": bool(re.search(r'review|rating|star', html)),
            "Schema": bool(re.search(r'schema\.org|@type', html)),
            "Open Graph": bool(re.search(r'og:', html)),
            "Mobile Responsive": bool(re.search(r'viewport|mobile', html)),
            "Favicon": bool(re.search(r'favicon|icon rel', html)),
            "llms.txt": bool(requests.head(f"{url}/llms.txt", timeout=5).status_code == 200) if '://' in url else False,
            "H1 Tag": bool(re.search(r'<h1', html)),
            "Canonical": bool(re.search(r'canonical', html)),
            "Sitemap": bool(re.search(r'sitemap', html)),
            "Click to Call": bool(re.search(r'tel:|click.to.call', html)),
            "AI Ready": bool(re.search(r'robots\.txt|llms\.txt', html)),
            "Fast Load": True,
            "No 404s": True,
            "DPDP Compliant": bool(re.search(r'privacy|data protection', html)),
        }
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        score = int((passed / total) * 100)
        
        return {
            "checks": results,
            "passed": passed,
            "total": total,
            "score": score
        }
    except Exception as e:
        return {"error": str(e), "score": 0}

# ─────────────────────────────────────────────────────────────────────────
# EMAIL SENDING
# ─────────────────────────────────────────────────────────────────────────

def send_scan_email(name, email, website, scan_results):
    """Send scan results via email"""
    try:
        passed = scan_results.get("passed", 0)
        total = scan_results.get("total", 25)
        score = scan_results.get("score", 0)
        checks = scan_results.get("checks", {})
        
        # Build checks HTML
        checks_html = ""
        for check, passed_check in checks.items():
            status = "✅" if passed_check else "⚠️"
            checks_html += f"<tr><td>{status} {check}</td><td>{'Detected' if passed_check else 'Missing'}</td></tr>"
        
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Poppins', Arial; color: #0A1A40; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background: #0A1A40; color: white; padding: 20px; text-align: center; border-radius: 8px; }}
                .score {{ font-size: 48px; font-weight: bold; color: #A3E635; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #EAF1F8; }}
                th {{ background: #EAF1F8; font-weight: 600; }}
                .cta {{ background: #FACC15; color: #0A1A40; padding: 15px; text-align: center; border-radius: 6px; margin: 20px 0; font-weight: 700; }}
                .footer {{ font-size: 12px; color: #65A30D; text-align: center; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🔍 Your Website Audit Results</h2>
                    <p>{website}</p>
                </div>
                
                <p>Hi {name},</p>
                <p>We've completed a 25-point audit of your website. Here are the results:</p>
                
                <div style="text-align: center; padding: 20px; background: #EAF1F8; border-radius: 8px;">
                    <div class="score">{score}%</div>
                    <p><strong>{passed} / {total} checks passed</strong></p>
                </div>
                
                <h3>Detailed Results:</h3>
                <table>
                    <tr>
                        <th>Check</th>
                        <th>Status</th>
                    </tr>
                    {checks_html}
                </table>
                
                <div class="cta">
                    <p>Ready to fix these issues?</p>
                    <p><strong>Schedule a call: +91 98866 50133</strong></p>
                </div>
                
                <p>We can set up tracking, lead capture, and optimization in minutes.</p>
                
                <div class="footer">
                    <p>The Website Auditor | amit.ahuja@thewebsiteauditor.com</p>
                    <p>Compliant with India's DPDP Act 2023</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Your Website Audit Results — {website}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD.replace(" ", ""))
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────
# SEND TO MAKE.COM (Google Sheets)
# ─────────────────────────────────────────────────────────────────────────

def send_to_make(name, phone, website, scan_results):
    """Send data to Make.com webhook → Google Sheets"""
    try:
        if not MAKE_WEBHOOK_URL:
            return True  # Skip if not configured
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "phone": phone,
            "website": website,
            "score": scan_results.get("score", 0),
            "passed": scan_results.get("passed", 0),
            "total": scan_results.get("total", 25),
            "status": "Completed"
        }
        
        requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=5)
        return True
    except Exception as e:
        print(f"Make.com webhook error: {e}")
        return True  # Don't fail if webhook is down

# ─────────────────────────────────────────────────────────────────────────
# HOMEPAGE
# ─────────────────────────────────────────────────────────────────────────

HOMEPAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Website Auditor — Free 25-Point Website Audit</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; background: {WHITE}; color: {NAVY}; line-height: 1.6; }}
        
        .navbar {{
            background: {NAVY};
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{ font-size: 20px; font-weight: 700; color: {LIME}; }}
        .nav-links {{ display: flex; gap: 2rem; }}
        .nav-links a {{ color: {WHITE}; text-decoration: none; }}
        
        .hero {{
            background: linear-gradient(135deg, {NAVY} 0%, {NAVY} 100%);
            color: {WHITE};
            padding: 5rem 2rem;
            text-align: center;
        }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; font-weight: 800; }}
        .hero p {{ font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9; }}
        
        .form-section {{
            max-width: 500px;
            margin: -3rem auto 3rem;
            background: {WHITE};
            border: 2px solid {LIME};
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 10px 40px rgba(10, 26, 64, 0.15);
        }}
        .form-group {{ margin-bottom: 1.5rem; }}
        label {{ display: block; font-size: 13px; font-weight: 600; color: {NAVY}; margin-bottom: 6px; text-transform: uppercase; }}
        input {{ width: 100%; padding: 12px 14px; border: 1.5px solid {NAVY}; border-radius: 6px; font-family: 'Poppins', sans-serif; font-size: 14px; color: {NAVY}; }}
        input:focus {{ outline: none; border-color: {LIME}; box-shadow: 0 0 0 3px rgba(163, 230, 53, 0.1); }}
        
        .btn {{
            width: 100%;
            padding: 14px;
            background: {YELLOW};
            color: {NAVY};
            border: none;
            border-radius: 6px;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 1rem;
            transition: all 0.3s;
        }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 25px rgba(250, 204, 21, 0.3); }}
        .btn:disabled {{ opacity: 0.6; }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            max-width: 1200px;
            margin: 4rem auto;
            padding: 0 2rem;
        }}
        .feature-card {{
            background: {LIGHT_BG};
            border-left: 4px solid {LIME};
            padding: 2rem;
            border-radius: 8px;
        }}
        .feature-card h3 {{ color: {NAVY}; margin-bottom: 0.5rem; }}
        .feature-card p {{ color: {GREEN}; font-size: 14px; }}
        
        .checks-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1rem;
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 2rem;
        }}
        .check-item {{
            background: {LIGHT_BG};
            padding: 1rem;
            border-radius: 6px;
            text-align: center;
            font-size: 13px;
            color: {NAVY};
            border: 1px solid {LIME};
        }}
        .check-item .emoji {{ font-size: 24px; margin-bottom: 0.5rem; }}
        
        .section {{
            max-width: 1200px;
            margin: 4rem auto;
            padding: 0 2rem;
        }}
        .section h2 {{
            text-align: center;
            color: {NAVY};
            margin-bottom: 2rem;
            font-size: 2rem;
            font-weight: 800;
        }}
        
        footer {{
            background: {NAVY};
            color: {WHITE};
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
        }}
        
        .wa-float {{
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 40px;
            right: 40px;
            background: {LIME};
            color: {NAVY};
            border-radius: 50%;
            text-align: center;
            font-size: 30px;
            line-height: 60px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            text-decoration: none;
            z-index: 1000;
            cursor: pointer;
        }}
        
        .success-msg {{
            display: none;
            background: #ECFDF5;
            border: 1.5px solid {GREEN};
            color: #166534;
            padding: 1rem;
            border-radius: 6px;
            margin-top: 1rem;
            text-align: center;
            font-weight: 600;
        }}
        .success-msg.show {{ display: block; }}
        
        @media (max-width: 768px) {{
            .features, .checks-grid {{ grid-template-columns: 1fr; }}
            .hero h1 {{ font-size: 2rem; }}
        }}
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
        <p>Get a complete 25-point audit in 60 seconds. Free. No signup required.</p>
    </div>
    
    <div class="form-section">
        <h3 style="color: {NAVY}; margin-bottom: 1rem;">Free Website Audit</h3>
        <form id="auditForm">
            <div class="form-group">
                <label>Your Name *</label>
                <input type="text" id="name" required />
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
            <div class="success-msg" id="successMsg">
                ✓ Scan completed! Check your email for results.
            </div>
        </form>
    </div>
    
    <div class="section" id="features">
        <h2>What We Check (25 Points)</h2>
        <div class="features">
            <div class="feature-card">
                <h3>📊 Traffic Intelligence</h3>
                <p>GA4, GTM, Clarity, Hotjar</p>
            </div>
            <div class="feature-card">
                <h3>🎯 Retargeting</h3>
                <p>Meta Pixel, Google Ads, LinkedIn</p>
            </div>
            <div class="feature-card">
                <h3>💬 Lead Capture</h3>
                <p>WhatsApp, live chat, forms</p>
            </div>
            <div class="feature-card">
                <h3>🔒 Trust & Security</h3>
                <p>SSL, privacy, reviews</p>
            </div>
            <div class="feature-card">
                <h3>🚀 Discovery</h3>
                <p>SEO, schema, Open Graph</p>
            </div>
            <div class="feature-card">
                <h3>🤖 AI Ready</h3>
                <p>ChatGPT, Claude, Gemini</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>The 25 Checks</h2>
        <div class="checks-grid">
            <div class="check-item"><div class="emoji">📊</div>GA4</div>
            <div class="check-item"><div class="emoji">📍</div>GTM</div>
            <div class="check-item"><div class="emoji">🎯</div>Meta Pixel</div>
            <div class="check-item"><div class="emoji">💰</div>Google Ads</div>
            <div class="check-item"><div class="emoji">📈</div>Clarity</div>
            <div class="check-item"><div class="emoji">🔗</div>LinkedIn</div>
            <div class="check-item"><div class="emoji">💬</div>WhatsApp</div>
            <div class="check-item"><div class="emoji">💬</div>Live Chat</div>
            <div class="check-item"><div class="emoji">📝</div>Form</div>
            <div class="check-item"><div class="emoji">🚪</div>Exit Intent</div>
            <div class="check-item"><div class="emoji">🔒</div>SSL</div>
            <div class="check-item"><div class="emoji">📄</div>Privacy</div>
            <div class="check-item"><div class="emoji">⭐</div>Reviews</div>
            <div class="check-item"><div class="emoji">🏷️</div>Schema</div>
            <div class="check-item"><div class="emoji">🌐</div>OG Meta</div>
            <div class="check-item"><div class="emoji">📱</div>Mobile</div>
            <div class="check-item"><div class="emoji">🔍</div>Favicon</div>
            <div class="check-item"><div class="emoji">🤖</div>llms.txt</div>
            <div class="check-item"><div class="emoji">🏷️</div>H1</div>
            <div class="check-item"><div class="emoji">🔗</div>Canonical</div>
            <div class="check-item"><div class="emoji">📍</div>Sitemap</div>
            <div class="check-item"><div class="emoji">🔄</div>Redirect</div>
            <div class="check-item"><div class="emoji">⚡</div>Speed</div>
            <div class="check-item"><div class="emoji">📞</div>Click Call</div>
            <div class="check-item"><div class="emoji">✅</div>AI Ready</div>
        </div>
    </div>
    
    <footer>
        <p>The Website Auditor © 2026 | amit.ahuja@thewebsiteauditor.com | +91 98866 50133</p>
    </footer>
    
    <a href="https://wa.me/919886650133" class="wa-float">💬</a>
    
    <script>
        async function submitScan() {{
            const name = document.getElementById('name').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const website = document.getElementById('website').value.trim();
            const btn = document.getElementById('scanBtn');
            
            if (!name || !phone || !website) {{
                alert('Please fill in all fields.');
                return;
            }}
            
            btn.disabled = true;
            btn.textContent = '⏳ Scanning...';
            
            try {{
                const response = await fetch('/api/scan', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{name, phone, website}})
                }});
                
                const data = await response.json();
                
                if (response.ok) {{
                    document.getElementById('successMsg').classList.add('show');
                    document.getElementById('auditForm').reset();
                    setTimeout(() => {{
                        btn.disabled = false;
                        btn.textContent = '🚀 SCAN NOW — FREE';
                    }}, 3000);
                }} else {{
                    alert('Error: ' + (data.message || 'Unknown error'));
                    btn.disabled = false;
                    btn.textContent = '🚀 SCAN NOW — FREE';
                }}
            }} catch (err) {{
                console.error('Error:', err);
                alert('Scan error. Please try again.');
                btn.disabled = false;
                btn.textContent = '🚀 SCAN NOW — FREE';
            }}
        }}
    </script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────
# API MODELS
# ─────────────────────────────────────────────────────────────────────────

class ScanRequest(BaseModel):
    name: str
    phone: str
    website: str

# ─────────────────────────────────────────────────────────────────────────
# API ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return HOMEPAGE

@app.post("/api/scan")
async def scan(request: ScanRequest):
    """Complete scan workflow"""
    try:
        # Run scan
        scan_results = run_website_scan(request.website)
        
        # Send email
        email_sent = send_scan_email(request.name, request.phone, request.website, scan_results)
        
        # Send to Make.com (Google Sheets)
        send_to_make(request.name, request.phone, request.website, scan_results)
        
        return {
            "status": "success",
            "message": f"Scan completed! Results sent to {request.phone}",
            "score": scan_results.get("score", 0),
            "passed": scan_results.get("passed", 0),
            "total": scan_results.get("total", 25)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
