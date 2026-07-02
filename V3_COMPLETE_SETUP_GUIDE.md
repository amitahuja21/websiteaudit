# WEBSITE V3 — COMPLETE SETUP GUIDE
## Lead Capture + Email Bot + Anti-Junk Deliverability + WhatsApp

---

## PART 1: DEPLOY THE NEW WEBSITE (10 minutes)

Push these 7 files to the ROOT of your GitHub repo (Render auto-deploys):

| File | What it is |
|------|-----------|
| `index.html` | The complete v3 website (replaces old file) |
| `privacy.html` | Real privacy policy page |
| `terms.html` | Real terms of service page |
| `og-image.png` | Social/WhatsApp share preview image |
| `robots.txt` | AI crawler access (from earlier — keep it) |
| `llms.txt` | AI business summary (from earlier — keep it) |
| `sitemap.xml` | Updated — now includes privacy & terms |

**GitHub web upload:** repo → "Add file" → "Upload files" → drag all 7 → Commit.
Render deploys in ~30 seconds.

---

## PART 2: CONNECT YOUR GOOGLE DRIVE LEAD SHEET (10 minutes)

You said you already have a lead file shared in Google Drive — perfect, we plug straight into it:

1. Open your existing lead Google Sheet in Drive
2. Create/rename a tab to exactly: **Leads**
3. Menu: **Extensions → Apps Script**
4. Delete any existing code, paste the entire **Code.gs** file I gave you
5. In the SETTINGS block at top, confirm `NOTIFY_EMAIL` is correct
6. Run the function **setupSheetAndTrigger** once (Run ▶ button)
   - Grant permissions when Google asks (it's your own account)
   - This creates the header row + installs the daily 9 AM follow-up bot
7. Click **Deploy → New deployment → ⚙️ type: Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click Deploy → **copy the Web App URL**
8. Open `index.html`, find `CONFIG` near the bottom, and paste the URL:
   ```
   SCRIPT_URL: 'https://script.google.com/macros/s/AKfycb.../exec',
   ```
9. Push index.html to GitHub again → done.

**What now happens automatically on every form submission:**
- Lead saved to your sheet (Timestamp, Name, Email, Phone, Website, Message, Status="New")
- Lead instantly receives a branded confirmation email
- YOU instantly receive a "🔔 New Lead" alert email
- After 15 days, if you haven't marked them Replied/Won/Closed, the bot emails them:
  *"We'll fix the 2 most critical issues from your report — completely free"*
- Bot marks FollowUpSent so nobody is ever emailed twice

**Your only job:** when a lead replies or converts, change their Status column to
`Replied`, `Won`, or `Closed`. That's it.

---

## PART 3: TRACKING IDS (fill CONFIG in index.html)

| Setting | Where to get it | Format |
|---------|----------------|--------|
| `GA4_ID` | analytics.google.com → Admin → Data Streams | `G-XXXXXXXXXX` |
| `GTM_ID` | tagmanager.google.com → your container | `GTM-XXXXXXX` |
| `META_PIXEL_ID` | business.facebook.com → Events Manager | numbers only |

Smart safety built in: tracking scripts DON'T load until (a) you enter real IDs
AND (b) the visitor clicks **Accept** on the cookie banner. No more broken
placeholder calls, and you're GDPR/DPDP-clean for AU/NZ/UAE/EU prospects.

---

## PART 4: STOP EMAILS GOING TO JUNK (do this BEFORE first campaign)

Emails from Apps Script send through YOUR Gmail/Workspace account — good start,
because Google's servers have strong reputation. Now lock in authentication:

### A. The 3 DNS records (add in Squarespace DNS, 15 minutes)

**1. SPF** — TXT record on `@`:
```
v=spf1 include:_spf.google.com ~all
```
(If a TXT starting `v=spf1` already exists, MERGE into one record — never two SPF records.)

**2. DKIM** — In Google Admin (admin.google.com):
Apps → Google Workspace → Gmail → Authenticate email → Generate new record
→ copy the TXT record (host: `google._domainkey`) into Squarespace → back in
Admin click **Start authentication**.

**3. DMARC** — TXT record on host `_dmarc`:
```
v=DMARC1; p=none; rua=mailto:amit.ahuja@thewebsiteauditor.com; pct=100
```
After 2-3 weeks of clean reports, upgrade `p=none` → `p=quarantine`.

**Verify:** send an email to the address given at **mail-tester.com** — target score 9+/10.

### B. Sender behavior rules (equally important)

1. **Warm up:** week 1 send max 20-30 emails/day, increase gradually. Sudden 500/day = spam folder.
2. **Create the alias** `hello@thewebsiteauditor.com` in Google Admin (Users → your user
   → Add alternate email) — the website mentions it; without the alias those emails bounce.
3. **Ask for replies** — "Just reply YES" (our follow-up does this). Replies are the
   strongest inbox-reputation signal that exists.
4. **Avoid junk triggers:** ALL CAPS subjects, too many !!!, words like FREE MONEY,
   GUARANTEED, ACT NOW, 10+ links, image-only emails. (Our templates are already clean —
   one link, mostly text.)
5. **Always include** identity + unsubscribe line (already built into the follow-up template).
6. **Never buy email lists.** Cold lists = spam complaints = domain reputation destroyed
   = even your genuine audit reports land in junk.

---

## PART 5: WHATSAPP — BUSINESS NAME + BOT

### A. Display name "The Website Auditor" (your number stays hidden)

You're right — with the **WhatsApp Business Platform (API)**, your verified business
display name shows instead of the raw number when messaging customers who haven't
saved you. Setup:

1. **Meta Business Manager** (business.facebook.com) → verify your business
   (GST/company documents) — one-time
2. Add WhatsApp product → register a number (use a NEW/spare number; a number on the
   API cannot use the normal WhatsApp app — same two-number rule we confirmed for
   Bharat Riders)
3. Set **Display Name: "The Website Auditor"** → Meta approves in 1-3 days
   (name must relate to your business/domain — yours matches perfectly)
4. Easiest management layer: **WATI** (you already know it) or Meta Cloud API direct
   (free tier: 1,000 service conversations/month)

The simple `wa.me` floating button on the website works from day one with your
existing number; migrate the button to the API number once approved.

### B. The customer-query bot (WATI flow — no code)

Recommended flow to configure:

```
[Customer messages anything]
 └─ WELCOME: "👋 Welcome to The Website Auditor! I'm your assistant.
     Reply with a number:
     1️⃣ Get my FREE 25-point website audit
     2️⃣ Pricing & services
     3️⃣ What is AI Search Visibility?
     4️⃣ Talk to Amit"

 1 → "Great! Please send: your name, email & website URL.
      Your audit report arrives in 1-2 hours. 🚀"
      (WATI webhook → same Google Sheet → same email automation)
 2 → "🆓 Free: 25-point audit
      💼 Pro $499: full 55-point audit + video + fix plan
      🤖 AI Readiness $399: get recommended by ChatGPT & Gemini
      📈 Monthly $999: continuous optimization
      Reply 1 to start free!"
 3 → "Customers now ask ChatGPT, Gemini & Perplexity for recommendations
      instead of Google. If AI can't read your website, it recommends your
      COMPETITOR. We fix that. Reply 1 for a free AI-visibility check!"
 4 → "Connecting you to Amit — he typically replies within 30 minutes
      during business hours (IST). 🙏"  → assign chat to you
 [Keyword 'audit' anywhere] → route to option 1
 [After 24h silence on option 1 started but not completed] → gentle nudge template
```

### C. Connect WhatsApp bot leads to the same automation

In WATI: Automation → Webhook on flow completion → POST to your same Apps Script
Web App URL with name/email/phone/website parameters. One sheet, one email bot,
two capture channels (website + WhatsApp). 

---

## PART 6: LAUNCH TEST CHECKLIST (15 minutes, in order)

☐ All 7 files pushed, Render deployed, https://thewebsiteauditor.com loads
☐ Mobile: hamburger menu opens, all links work
☐ Cookie banner appears → Accept → (after IDs added) GA4 Realtime shows your visit
☐ Submit the form with YOUR details →
   ☐ Row appears in Google Sheet
   ☐ You receive confirmation email (check it's in INBOX, not spam)
   ☐ You receive the "🔔 New Lead" alert
☐ WhatsApp float button opens chat with pre-filled message
☐ privacy.html and terms.html open from footer
☐ Share the URL in a WhatsApp chat → og-image preview shows
☐ mail-tester.com score 9+/10 after SPF/DKIM/DMARC
☐ To test the 15-day bot immediately: temporarily change FOLLOWUP_DAYS to 0,
   run dailyFollowUp manually, check the email, change back to 15

---

## WHAT I STILL NEED FROM YOU

1. **GA4 Measurement ID** (G-…) — or say the word and I'll walk you through creating it
2. **GTM Container ID** (GTM-…) — optional if using GA4 direct
3. **Meta Pixel ID**
4. **Apps Script Web App URL** — after you complete Part 2, send it to me and I'll
   give you the final index.html with everything filled in, ready to push.
