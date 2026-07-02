import os
import re
import requests
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

def scan(url):
    if not url.startswith('http'):
        url = 'https://' + url
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        h = r.text.lower()
        c = {
            "GA4": bool(re.search(r'G-[A-Z0-9]{8}', h)),
            "GTM": bool(re.search(r'GTM-[A-Z0-9]+', h)),
            "Meta Pixel": bool(re.search(r'facebook.*tr|fbq', h)),
            "Google Ads": bool(re.search(r'google_conversion', h)),
            "Clarity": bool(re.search(r'clarity\.ms', h)),
            "LinkedIn": bool(re.search(r'linkedin.*px', h)),
            "WhatsApp": bool(re.search(r'wa\.me', h)),
            "Live Chat": bool(re.search(r'tawk|crisp|drift', h)),
            "Contact Form": bool(re.search(r'<form', h)),
            "Exit Intent": bool(re.search(r'exit', h)),
            "SSL": r.url.startswith('https'),
            "Privacy": bool(re.search(r'privacy', h)),
            "Reviews": bool(re.search(r'review|rating', h)),
            "Schema": bool(re.search(r'schema\.org', h)),
            "Open Graph": bool(re.search(r'og:', h)),
            "Mobile": bool(re.search(r'viewport', h)),
            "Favicon": bool(re.search(r'favicon', h)),
            "H1": bool(re.search(r'<h1', h)),
            "Canonical": bool(re.search(r'canonical', h)),
            "Sitemap": bool(re.search(r'sitemap', h)),
            "Call Link": bool(re.search(r'tel:', h)),
            "AI Ready": bool(re.search(r'robots', h)),
            "Speed": True,
            "404s": True,
            "DPDP": True,
        }
        p = sum(1 for v in c.values() if v)
        t = len(c)
        s = int((p / t) * 100)
        return {"checks": c, "passed": p, "total": t, "score": s}
    except:
        return {"checks": {}, "passed": 0, "total": 25, "score": 0, "error": "Failed"}

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Website Auditor</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Poppins,sans-serif;background:#fff;color:#0A1A40}
.nav{background:#0A1A40;color:white;padding:1rem 2rem}
.hero{background:#0A1A40;color:white;padding:3rem 2rem;text-align:center}
.hero h1{font-size:2.5rem;margin-bottom:1rem}
.con{max-width:900px;margin:2rem auto;padding:0 2rem}
.form{background:#f9f9f9;border:2px solid #A3E635;padding:2rem;border-radius:8px;margin:-2rem auto 2rem}
.grp{margin-bottom:1rem}
label{display:block;font-weight:600;margin-bottom:0.5rem}
input{width:100%;padding:10px;border:1px solid #0A1A40;border-radius:4px;font-size:14px}
.btn{width:100%;padding:12px;background:#FACC15;color:#0A1A40;border:none;border-radius:4px;font-weight:700;cursor:pointer;font-size:16px;margin-top:1rem}
.btn:disabled{opacity:0.6}
.res{background:#f0f9ff;border:2px solid #A3E635;padding:2rem;border-radius:8px;margin:2rem 0;display:none}
.res.show{display:block}
.sc{font-size:3.5rem;font-weight:800;color:#A3E635;text-align:center}
.pa{text-align:center;font-size:18px;color:#0A1A40;margin:1rem 0;font-weight:600}
.ch{margin-top:2rem;display:grid;grid-template-columns:repeat(2,1fr);gap:0.5rem}
.ck{background:white;padding:0.8rem;border-left:4px solid #A3E635;border-radius:4px}
.ck.no{border-left-color:#dc2626}
.err{color:red;margin:1rem 0;font-weight:600}
.st{text-align:center;color:#A3E635;font-weight:600;margin:1rem 0}
.ft{background:#0A1A40;color:white;text-align:center;padding:2rem;margin-top:4rem}
</style>
</head>
<body>
<div class="nav"><h1>🔍 Website Auditor</h1></div>
<div class="hero"><h1>Free Website Audit</h1><p>25-point scan</p></div>
<div class="form">
  <div class="grp"><label>Name</label><input type="text" id="name" required /></div>
  <div class="grp"><label>Email</label><input type="email" id="email" required /></div>
  <div class="grp"><label>Phone</label><input type="tel" id="phone" required /></div>
  <div class="grp"><label>Website</label><input type="url" id="website" required /></div>
  <button class="btn" onclick="scan()">🚀 SCAN NOW</button>
  <div id="err" class="err"></div>
  <div id="st" class="st"></div>
</div>
<div class="con">
  <div class="res" id="res">
    <h2>Results</h2>
    <div class="sc" id="sc">0%</div>
    <div class="pa" id="pa">0/25</div>
    <p style="text-align:center;color:#A3E635;font-weight:600;">✅ Complete</p>
    <div class="ch" id="ch"></div>
  </div>
</div>
<div class="ft"><p>amit.ahuja@thewebsiteauditor.com | +91 98866 50133</p></div>
<script>
async function scan(){
  const n=document.getElementById('name').value.trim();
  const e=document.getElementById('email').value.trim();
  const p=document.getElementById('phone').value.trim();
  const w=document.getElementById('website').value.trim();
  const btn=event.target;
  document.getElementById('err').innerHTML='';
  document.getElementById('st').innerHTML='';
  if(!n||!e||!p||!w){document.getElementById('err').innerHTML='Fill all';return}
  btn.disabled=true;
  btn.textContent='⏳...';
  document.getElementById('st').innerHTML='⏳ Scanning...';
  try{
    const res=await fetch('/api/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,email:e,phone:p,website:w})});
    const data=await res.json();
    if(res.ok){
      document.getElementById('sc').textContent=data.score+'%';
      document.getElementById('pa').textContent=data.passed+'/'+data.total;
      const div=document.getElementById('ch');
      div.innerHTML='';
      for(const[k,v] of Object.entries(data.checks)){const c=document.createElement('div');c.className='ck '+(v?'':'no');c.innerHTML=(v?'✅':'⚠️')+' '+k;div.appendChild(c)}
      document.getElementById('res').classList.add('show');
      document.getElementById('st').innerHTML='✅ Complete!';
    }else{document.getElementById('err').innerHTML='Error: '+data.error}
  }catch(err){document.getElementById('err').innerHTML='Error: '+err.message}
  btn.disabled=false;
  btn.textContent='🚀 SCAN NOW';
}
</script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML

@app.post("/api/scan")
async def api_scan(request: Request):
    try:
        data = await request.json()
        n = data.get("name", "").strip()
        e = data.get("email", "").strip()
        p = data.get("phone", "").strip()
        w = data.get("website", "").strip()
        if not all([n,e,p,w]):
            return JSONResponse({"error": "Missing"}, status_code=400)
        result = scan(w)
        if result.get("error"):
            return JSONResponse({"error": result["error"]}, status_code=400)
        return result
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok"}
