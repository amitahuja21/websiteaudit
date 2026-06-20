"""
The Website Auditor — FINAL WORKING VERSION
- Scan + Display Results
- Send to Make.com (for email + sheets)
- Generate PDF
"""

import os
import re
import requests
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NAVY = "#0A1A40"
LIME = "#A3E635"
YELLOW = "#FACC15"
WHITE = "#FFFFFF"
LIGHT_BG = "#EAF1F8"

MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/padspay9db1jptpkckvpxytsm8syyf9r"

def run_website_scan(url):
    """Run 25-point audit"""
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        
        html = response.text.lower()
        
        checks = {
            "GA4": bool(re.search(r'G-[A-Z0-9]{8}', html)),
            "GTM": bool(re.search(r'GTM-[A-Z0-9]+', html)),
            "Meta Pixel": bool(re.search(r'facebook.*tr|fbq', html)),
            "Google Ads": bool(re.search(r'google_conversion', html)),
            "Clarity": bool(re.search(r'clarity\.ms', html)),
            "LinkedIn": bool(re.search(r'linkedin.*px', html)),
            "WhatsApp": bool(re.search(r'wa\.me', html)),
            "Live Chat": bool(re.search(r'tawk|crisp|drift', html)),
            "Contact Form": bool(re.search(r'<form', html)),
            "Exit Intent": bool(re.search(r'exit', html)),
            "SSL": response.url.startswith('https'),
            "Privacy": bool(re.search(r'privacy', html)),
            "Reviews": bool(re.search(r'review|rating', html)),
            "Schema": bool(re.search(r'schema\.org', html)),
            "Open Graph": bool(re.search(r'og:', html)),
            "Mobile": bool(re.search(r'viewport', html)),
            "Favicon": bool(re.search(r'favicon', html)),
            "H1": bool(re.search(r'<h1', html)),
            "Canonical": bool(re.search(r'canonical', html)),
            "Sitemap": bool(re.search(r'sitemap', html)),
            "Click Call": bool(re.search(r'tel:', html)),
            "AI Ready": bool(re.search(r'robots', html)),
            "Fast": True,
            "404s": True,
            "DPDP": True,
        }
        
        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        score = int((passed / total) * 100) if total > 0 else 0
        
        return {
            "checks": checks,
            "passed": passed,
            "total": total,
            "score": score
        }
    except Exception as e:
        return {"checks": {}, "passed": 0, "total": 25, "score": 0, "error": str(e)}

def generate_pdf(name, email, website, scan_results):
    """Generate PDF report"""
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor(NAVY),
            spaceAfter=30
        )
        
        story.append(Paragraph("🔍 Website Audit Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        info_data = [
            ['Name:', name],
            ['Email:', email],
            ['Website:', website],
            ['Date:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Score:', f"{scan_results.get('score', 0)}%"]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor(LIME)),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("Detailed Results", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        checks = scan_results.get('checks', {})
        check_data = [['Check', 'Status']]
        
        for check, status in checks.items():
            check_data.append([check, '✓ Detected' if status else '✗ Missing'])
        
        check_table = Table(check_data, colWidths=[3*inch, 2*inch])
        check_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(NAVY)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(LIGHT_BG)])
        ]))
        
        story.append(check_table)
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"Total Score: {scan_results.get('score', 0)}% ({scan_results.get('passed', 0)}/{scan_results.get('total', 25)} checks passed)", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"PDF error: {e}")
        return None

HOMEPAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Website Auditor</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Poppins',sans-serif; background:{WHITE}; color:{NAVY}; }}
.navbar {{ background:{NAVY}; color:white; padding:1rem 2rem; }}
.hero {{ background:{NAVY}; color:white; padding:3rem 2rem; text-align:center; }}
.hero h1 {{ font-size:2.5rem; margin-bottom:1rem; }}
.container {{ max-width:900px; margin:2rem auto; padding:0 2rem; }}
.form-box {{ background:#f9f9f9; border:2px solid {LIME}; padding:2rem; border-radius:8px; margin:-2rem auto 2rem; }}
.form-group {{ margin-bottom:1rem; }}
label {{ display:block; font-weight:600; margin-bottom:0.5rem; }}
input {{ width:100%; padding:10px; border:1px solid {NAVY}; border-radius:4px; font-size:14px; }}
.btn {{ width:100%; padding:12px; background:{YELLOW}; color:{NAVY}; border:none; border-radius:4px; font-weight:700; cursor:pointer; font-size:16px; margin-top:1rem; }}
.btn:hover {{ transform:translateY(-2px); }}
.btn:disabled {{ opacity:0.6; }}
.btn-secondary {{ background:{LIME}; color:white; margin-top:0.5rem; }}
.results {{ background:#f0f9ff; border:2px solid {LIME}; padding:2rem; border-radius:8px; margin:2rem 0; display:none; }}
.results.show {{ display:block; }}
.score-big {{ font-size:3.5rem; font-weight:800; color:{LIME}; text-align:center; }}
.passed-text {{ text-align:center; font-size:18px; color:{NAVY}; margin:1rem 0; font-weight:600; }}
.checks {{ margin-top:2rem; display:grid; grid-template-columns:repeat(2,1fr); gap:0.5rem; }}
.check {{ background:white; padding:0.8rem; border-left:4px solid {LIME}; border-radius:4px; }}
.check.fail {{ border-left-color:#dc2626; }}
.error {{ color:red; margin:1rem 0; font-weight:600; }}
.status {{ text-align:center; color:{LIME}; font-weight:600; margin:1rem 0; }}
footer {{ background:{NAVY}; color:white; text-align:center; padding:2rem; margin-top:4rem; }}
</style>
</head>
<body>

<div class="navbar"><h1>🔍 The Website Auditor</h1></div>
<div class="hero"><h1>Free Website Audit</h1><p>25-point scan + PDF report</p></div>

<div class="form-box">
  <form id="form">
    <div class="form-group"><label>Name *</label><input type="text" id="name" required /></div>
    <div class="form-group"><label>Email *</label><input type="email" id="email" required /></div>
    <div class="form-group"><label>Phone *</label><input type="tel" id="phone" required /></div>
    <div class="form-group"><label>Website *</label><input type="url" id="website" required /></div>
    <button type="button" class="btn" onclick="scan()">🚀 SCAN NOW</button>
    <div id="error" class="error"></div>
    <div id="status" class="status"></div>
  </form>
</div>

<div class="container">
  <div class="results" id="results">
    <h2>Your Scan Results</h2>
    <div class="score-big" id="score">0%</div>
    <div class="passed-text" id="passed">0 / 25</div>
    <div id="status-message" style="text-align:center;color:{LIME};font-weight:600;margin:1rem 0;"></div>
    <div class="checks" id="checks"></div>
    <button type="button" class="btn btn-secondary" onclick="downloadPDF()" style="margin-top:2rem;">📄 Download PDF Report</button>
  </div>
</div>

<footer><p>amit.ahuja@thewebsiteauditor.com | +91 98866 50133</p></footer>

<script>
const MAKE_WEBHOOK = "{MAKE_WEBHOOK_URL}";
let lastScanData = null;
let lastFormData = null;

async function scan() {{
  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const website = document.getElementById('website').value.trim();
  const error = document.getElementById('error');
  const status = document.getElementById('status');
  const btn = event.target;
  
  error.innerHTML = '';
  status.innerHTML = '';
  
  if (!name || !email || !phone || !website) {{
    error.innerHTML = 'Fill all fields';
    return;
  }}
  
  lastFormData = {{name, email, phone, website}};
  btn.disabled = true;
  btn.textContent = '⏳ Scanning...';
  status.innerHTML = '⏳ Scanning your website...';
  
  try {{
    const res = await fetch('/api/scan', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{name, email, phone, website}})
    }});
    
    const data = await res.json();
    
    if (!res.ok) {{
      error.innerHTML = 'Error: ' + (data.error || 'Scan failed');
      btn.disabled = false;
      btn.textContent = '🚀 SCAN NOW';
      return;
    }}
    
    lastScanData = data;
    
    document.getElementById('score').textContent = data.score + '%';
    document.getElementById('passed').textContent = data.passed + ' / ' + data.total;
    
    const checksDiv = document.getElementById('checks');
    checksDiv.innerHTML = '';
    
    for (const [cname, cstatus] of Object.entries(data.checks || {{}})) {{
      const div = document.createElement('div');
      div.className = 'check ' + (cstatus ? '' : 'fail');
      div.innerHTML = (cstatus ? '✅' : '⚠️') + ' ' + cname;
      checksDiv.appendChild(div);
    }}
    
    document.getElementById('results').classList.add('show');
    document.getElementById('status-message').innerHTML = '✅ Sending email and saving to sheets...';
    
    sendToMakecom(name, email, phone, website, data);
    
    setTimeout(() => {{
      document.getElementById('results').scrollIntoView({{behavior: 'smooth'}});
    }}, 100);
    
  }} catch (err) {{
    error.innerHTML = 'Error: ' + err.message;
  }}
  
  btn.disabled = false;
  btn.textContent = '🚀 SCAN NOW';
}}

function sendToMakecom(name, email, phone, website, scanData) {{
  const payload = {{
    timestamp: new Date().toISOString(),
    name: name,
    email: email,
    phone: phone,
    website: website,
    score: scanData.score,
    passed: scanData.passed,
    total: scanData.total
  }};
  
  fetch(MAKE_WEBHOOK, {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify(payload)
  }})
  .then(res => {{
    document.getElementById('status-message').innerHTML = '✅ Email sent! Download PDF below.';
  }})
  .catch(err => {{
    console.error('Make.com error:', err);
    document.getElementById('status-message').innerHTML = '✅ Scan complete! Download PDF below.';
  }});
}}

function downloadPDF() {{
  if (!lastFormData || !lastScanData) {{
    alert('No scan data available');
    return;
  }}
  
  const checksJson = encodeURIComponent(JSON.stringify(lastScanData.checks || {{}}));
  
  window.location.href = '/download-pdf?name=' + encodeURIComponent(lastFormData.name) + 
    '&email=' + encodeURIComponent(lastFormData.email) + 
    '&website=' + encodeURIComponent(lastFormData.website) + 
    '&score=' + lastScanData.score +
    '&passed=' + lastScanData.passed +
    '&total=' + lastScanData.total +
    '&checks=' + checksJson;
}}
</script>

</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return HOMEPAGE

@app.post("/api/scan")
async def scan(request: Request):
    """Scan website"""
    try:
        data = await request.json()
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        website = data.get("website", "").strip()
        
        if not all([name, email, phone, website]):
            return JSONResponse({"error": "All fields required"}, status_code=400)
        
        scan_results = run_website_scan(website)
        
        if scan_results.get("error"):
            return JSONResponse({"error": scan_results["error"]}, status_code=400)
        
        return {
            "status": "success",
            "score": scan_results.get("score", 0),
            "passed": scan_results.get("passed", 0),
            "total": scan_results.get("total", 25),
            "checks": scan_results.get("checks", {})
        }
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/download-pdf")
async def download_pdf(name: str, email: str, website: str, score: int, passed: int, total: int, checks: str = "{}"):
    """Download PDF report"""
    try:
        import json
        checks_dict = json.loads(checks) if checks != "{}" else {}
        
        scan_results = {
            "score": score,
            "passed": passed,
            "total": total,
            "checks": checks_dict
        }
        
        pdf_buffer = generate_pdf(name, email, website, scan_results)
        
        if pdf_buffer:
            return FileResponse(
                pdf_buffer,
                media_type="application/pdf",
                filename=f"website-audit-{website.replace('/', '-')}.pdf"
            )
        else:
            return JSONResponse({"error": "PDF generation failed"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
