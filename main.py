"""
The Website Auditor — Complete FastAPI App
With WhatsApp Integration + Exit Popup + Live Chat + Lead Form
Brand Colors: Navy #0A1A40, Lime #A3E635, Yellow #FACC15
Contact: amit.ahuja@thewebsiteauditor.com | +91 98866 50133
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="The Website Auditor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Brand Colors
NAVY = "#0A1A40"
LIME = "#A3E635"
YELLOW = "#FACC15"
WHITE = "#FFFFFF"
LIGHT_BG = "#EAF1F8"
GREEN = "#65A30D"

HTML_CONTENT = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Website Auditor — Free 25-Point Website Audit in 60 Seconds</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; background: {WHITE}; color: {NAVY}; line-height: 1.6; }}
        
        /* NAVBAR */
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
        
        /* HERO */
        .hero {{
            background: linear-gradient(135deg, {NAVY} 0%, {NAVY} 100%);
            color: {WHITE};
            padding: 5rem 2rem;
            text-align: center;
        }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; font-weight: 800; }}
        .hero p {{ font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9; }}
        
        /* FORM SECTION */
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
        input, textarea {{ width: 100%; padding: 12px 14px; border: 1.5px solid {NAVY}; border-radius: 6px; font-family: 'Poppins', sans-serif; font-size: 14px; color: {NAVY}; }}
        input:focus, textarea:focus {{ outline: none; border-color: {LIME}; box-shadow: 0 0 0 3px rgba(163, 230, 53, 0.1); }}
        
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
        
        /* FEATURES */
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
        
        /* CHECKS GRID */
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
        
        /* FOOTER */
        footer {{
            background: {NAVY};
            color: {WHITE};
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
            font-size: 14px;
        }}
        
        /* FLOATING WHATSAPP BUTTON */
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
            transition: all 0.3s;
        }}
        .wa-float:hover {{ transform: scale(1.1); }}
        
        /* EXIT POPUP */
        .overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }}
        .overlay.show {{ display: flex; }}
        .popup {{
            background: {WHITE};
            padding: 2rem;
            border-radius: 12px;
            max-width: 400px;
            width: 90%;
            text-align: center;
            border: 2px solid {LIME};
            position: relative;
        }}
        .popup h3 {{ color: {NAVY}; margin-bottom: 1rem; font-size: 20px; }}
        .popup p {{ color: {GREEN}; margin-bottom: 1rem; }}
        .popup input {{ margin-bottom: 1rem; }}
        .popup .x {{
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 28px;
            cursor: pointer;
            color: {NAVY};
            border: none;
            background: none;
        }}
        
        /* LIVE CHAT WIDGET */
        .chat-widget {{
            position: fixed;
            bottom: 120px;
            right: 40px;
            width: 320px;
            background: {WHITE};
            border: 2px solid {LIME};
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            display: none;
            z-index: 999;
            flex-direction: column;
            max-height: 400px;
        }}
        .chat-widget.show {{ display: flex; }}
        .chat-header {{
            background: {NAVY};
            color: {WHITE};
            padding: 1rem;
            border-radius: 10px 10px 0 0;
            font-weight: 700;
        }}
        .chat-body {{
            flex: 1;
            padding: 1rem;
            overflow-y: auto;
            font-size: 13px;
        }}
        .chat-msg {{ margin-bottom: 0.5rem; }}
        .chat-msg.user {{ text-align: right; color: {LIME}; }}
        .chat-msg.bot {{ color: {NAVY}; }}
        .chat-footer {{
            padding: 1rem;
            border-top: 1px solid {LIME};
            display: flex;
            gap: 0.5rem;
        }}
        .chat-footer input {{
            flex: 1;
            border: 1px solid {LIME};
        }}
        .chat-footer button {{
            background: {YELLOW};
            color: {NAVY};
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .features, .checks-grid {{ grid-template-columns: 1fr; }}
            .hero h1 {{ font-size: 2rem; }}
            .wa-float, .chat-widget {{ right: 20px; bottom: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">🔍 The Website Auditor</div>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="#contact">Contact</a>
            <a href="https://wa.me/919886650133" target="_blank">WhatsApp</a>
        </div>
    </div>
    
    <div class="hero">
        <h1>Is Your Website Ready?</h1>
        <p>Get a complete 25-point audit in 60 seconds. Free. No signup required.</p>
    </div>
    
    <div class="form-section">
        <h3 style="color: {NAVY}; margin-bottom: 1rem;">Free Website Audit</h3>
        <form id="leadForm">
            <div class="form-group">
                <label>Your Name *</label>
                <input type="text" id="c_name" required />
            </div>
            <div class="form-group">
                <label>Phone (WhatsApp) *</label>
                <input type="tel" id="c_phone" required />
            </div>
            <div class="form-group">
                <label>Your Website *</label>
                <input type="url" id="c_site" placeholder="https://example.com" required />
            </div>
            <div class="form-group">
                <label>City</label>
                <input type="text" id="c_city" />
            </div>
            <div class="form-group">
                <label>Message</label>
                <textarea id="c_msg" rows="3"></textarea>
            </div>
            <button type="button" class="btn" onclick="submitLead()">🚀 GET FREE AUDIT</button>
        </form>
    </div>
    
    <div class="section" id="features">
        <h2>What We Check (25 Points)</h2>
        <div class="features">
            <div class="feature-card">
                <h3>📊 Traffic Intelligence</h3>
                <p>GA4, GTM, Clarity, Hotjar tracking</p>
            </div>
            <div class="feature-card">
                <h3>🎯 Retargeting</h3>
                <p>Meta Pixel, Google Ads, LinkedIn tags</p>
            </div>
            <div class="feature-card">
                <h3>💬 Lead Capture</h3>
                <p>WhatsApp, live chat, contact forms</p>
            </div>
            <div class="feature-card">
                <h3>🔒 Trust & Security</h3>
                <p>SSL, privacy policy, reviews</p>
            </div>
            <div class="feature-card">
                <h3>🚀 Discovery</h3>
                <p>SEO, schema, Open Graph, llms.txt</p>
            </div>
            <div class="feature-card">
                <h3>🤖 AI Ready</h3>
                <p>ChatGPT, Claude, Gemini visibility</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>The 25 Checks</h2>
        <div class="checks-grid">
            <div class="check-item"><div class="emoji">📊</div>GA4</div>
            <div class="check-item"><div class="emoji">📍</div>GTM</div>
            <div class="check-item"><div class="emoji">📈</div>Clarity</div>
            <div class="check-item"><div class="emoji">🎯</div>Meta Pixel</div>
            <div class="check-item"><div class="emoji">💰</div>Google Ads</div>
            <div class="check-item"><div class="emoji">🔗</div>LinkedIn</div>
            <div class="check-item"><div class="emoji">💬</div>WhatsApp</div>
            <div class="check-item"><div class="emoji">💬</div>Live Chat</div>
            <div class="check-item"><div class="emoji">📝</div>Lead Form</div>
            <div class="check-item"><div class="emoji">🚪</div>Exit Intent</div>
            <div class="check-item"><div class="emoji">🔒</div>SSL</div>
            <div class="check-item"><div class="emoji">📄</div>Privacy</div>
            <div class="check-item"><div class="emoji">⭐</div>Reviews</div>
            <div class="check-item"><div class="emoji">🏷️</div>Schema</div>
            <div class="check-item"><div class="emoji">🌐</div>Open Graph</div>
            <div class="check-item"><div class="emoji">📱</div>Mobile</div>
            <div class="check-item"><div class="emoji">🔍</div>Favicon</div>
            <div class="check-item"><div class="emoji">🤖</div>llms.txt</div>
            <div class="check-item"><div class="emoji">🏷️</div>H1 Tag</div>
            <div class="check-item"><div class="emoji">🔗</div>Canonical</div>
            <div class="check-item"><div class="emoji">📍</div>Sitemap</div>
            <div class="check-item"><div class="emoji">🔄</div>Redirect</div>
            <div class="check-item"><div class="emoji">⚡</div>Speed</div>
            <div class="check-item"><div class="emoji">📞</div>Click-to-Call</div>
            <div class="check-item"><div class="emoji">✅</div>AI Ready</div>
        </div>
    </div>
    
    <div class="section" id="contact">
        <h2>Ready to Get Your Free Audit?</h2>
        <p style="text-align: center; font-size: 16px; margin-bottom: 2rem;">
            WhatsApp me your website URL and get a detailed report in 60 seconds.
        </p>
        <div style="text-align: center;">
            <a href="https://wa.me/919886650133?text=Hi%20Amit%2C%20I%27d%20like%20a%20free%20website%20audit" class="btn" style="display: inline-block; padding: 15px 40px;">💬 Chat on WhatsApp</a>
        </div>
    </div>
    
    <footer>
        <p>The Website Auditor © 2026</p>
        <p>amit.ahuja@thewebsiteauditor.com | +91 98866 50133</p>
        <p style="font-size: 12px; margin-top: 1rem;">We never sell your data. Compliant with India's DPDP Act 2023.</p>
    </footer>
    
    <!-- FLOATING WHATSAPP BUTTON -->
    <a href="https://wa.me/919886650133?text=Hi%20Amit,%20I'd%20like%20a%20free%20website%20audit" class="wa-float" title="Chat on WhatsApp">💬</a>
    
    <!-- EXIT POPUP -->
    <div class="overlay" id="exitPopup">
        <div class="popup">
            <button class="x" onclick="closePopup()">×</button>
            <h3>Wait — Get Your Free Audit! 🎁</h3>
            <p>Drop your WhatsApp number and we'll send you a free 25-point website audit.</p>
            <input type="tel" id="exit_phone" placeholder="+91 your number">
            <button class="btn" onclick="submitExit()">Send Me The Audit</button>
        </div>
    </div>
    
    <!-- LIVE CHAT WIDGET -->
    <div class="chat-widget" id="chatWidget">
        <div class="chat-header">
            Website Auditor Support
            <span style="float: right; cursor: pointer; font-size: 20px;" onclick="toggleChat()">−</span>
        </div>
        <div class="chat-body" id="chatBody">
            <div class="chat-msg bot">Hi! 👋 How can I help you today?</div>
        </div>
        <div class="chat-footer">
            <input type="text" id="chatInput" placeholder="Type message..." />
            <button onclick="sendChat()">Send</button>
        </div>
    </div>
    
    <button class="chat-widget" id="chatToggle" style="position: fixed; bottom: 120px; right: 40px; width: 60px; height: 60px; background: {LIME}; color: {NAVY}; border: none; border-radius: 50%; font-size: 20px; cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 999;" onclick="toggleChat()">💬</button>
    
    <script>
        let popupShown = false;
        let chatOpen = false;
        
        // Lead form submit
        function submitLead() {{
            const name = document.getElementById('c_name').value.trim();
            const phone = document.getElementById('c_phone').value.trim();
            const site = document.getElementById('c_site').value.trim();
            const city = document.getElementById('c_city').value.trim();
            const msg = document.getElementById('c_msg').value.trim();
            
            if (!name || !phone || !site) {{
                alert('Please fill in your name, phone, and website.');
                return;
            }}
            
            const text = `New Audit Request:%0A%0AName: ${{name}}%0APhone: ${{phone}}%0AWebsite: ${{site}}%0ACity: ${{city}}%0AMessage: ${{msg}}`;
            window.open(`https://wa.me/919886650133?text=${{text}}`, '_blank');
            
            document.getElementById('leadForm').reset();
        }}
        
        // Exit popup
        function showPopup() {{
            if (!popupShown) {{
                document.getElementById('exitPopup').classList.add('show');
                popupShown = true;
            }}
        }}
        function closePopup() {{
            document.getElementById('exitPopup').classList.remove('show');
        }}
        function submitExit() {{
            const phone = document.getElementById('exit_phone').value.trim();
            if (!phone) {{
                alert('Please enter your WhatsApp number.');
                return;
            }}
            const text = `Hi Amit, I'd like a free website audit. My WhatsApp: ${{phone}}`;
            window.open(`https://wa.me/919886650133?text=${{encodeURIComponent(text)}}`, '_blank');
            closePopup();
        }}
        
        // Toggle chat
        function toggleChat() {{
            chatOpen = !chatOpen;
            document.getElementById('chatWidget').classList.toggle('show');
            document.getElementById('chatToggle').style.display = chatOpen ? 'none' : 'flex';
        }}
        
        function sendChat() {{
            const msg = document.getElementById('chatInput').value.trim();
            if (!msg) return;
            
            document.getElementById('chatBody').innerHTML += `<div class="chat-msg user">${{msg}}</div>`;
            document.getElementById('chatInput').value = '';
            
            setTimeout(() => {{
                document.getElementById('chatBody').innerHTML += `<div class="chat-msg bot">Thanks for your message! For immediate help, please WhatsApp +91 98866 50133</div>`;
            }}, 500);
        }}
        
        // Show exit popup when user tries to leave
        document.addEventListener('mouseout', (e) => {{
            if (e.clientY < 0) showPopup();
        }});
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def homepage():
    return HTML_CONTENT

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
