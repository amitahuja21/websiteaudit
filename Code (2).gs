/************************************************************************
 * THE WEBSITE AUDITOR — LEAD CAPTURE + EMAIL AUTOMATION BOT
 * ----------------------------------------------------------------------
 * WHAT THIS DOES:
 *  1. Receives form submissions from thewebsiteauditor.com
 *  2. Saves every lead into your Google Sheet (your existing Drive lead file)
 *  3. Instantly emails the lead a branded confirmation
 *  4. Instantly notifies YOU (email) about the new lead
 *  5. EVERY DAY at 9 AM: finds leads with no reply after 15 days and
 *     sends them a follow-up offering to FIX 2 ISSUES FREE
 *
 * SETUP (10 minutes, one time):
 *  1. Open your existing lead Google Sheet in Drive
 *  2. Rename (or create) a tab called exactly:  Leads
 *  3. Extensions → Apps Script → delete everything → paste this file
 *  4. Update the 3 SETTINGS below
 *  5. Run the function  setupSheetAndTrigger  once (grant permissions)
 *  6. Deploy → New deployment → type: Web app →
 *       Execute as: Me   |   Who has access: Anyone
 *  7. Copy the Web App URL → paste into CONFIG.SCRIPT_URL in index.html
 ************************************************************************/

// ======================= SETTINGS — EDIT THESE =======================
const NOTIFY_EMAIL   = 'amit.ahuja@thewebsiteauditor.com'; // you get new-lead alerts here
const FROM_NAME      = 'The Website Auditor';
const FOLLOWUP_DAYS  = 15;                                  // days before reminder
const WHATSAPP_LINK  = 'https://wa.me/919886650133';
// =====================================================================

const SHEET_NAME = 'Leads';
const COLS = ['Timestamp','Name','Email','Phone','Website','Message','Status','FollowUpSent','Notes'];
// Status values you set manually in the sheet: New / Audit Sent / Replied / Won / Closed
// The follow-up bot ONLY emails leads whose Status is "New" or "Audit Sent".

/* ---------- 1. RECEIVE FORM SUBMISSIONS ---------- */
function doPost(e) {
  try {
    const p = e.parameter;
    const sheet = getSheet_();
    sheet.appendRow([
      new Date(),
      p.name || '', p.email || '', p.phone || '',
      p.website || '', p.message || '',
      'New', '', ''
    ]);

    if (p.email) sendConfirmationEmail_(p.name, p.email, p.website);
    notifyOwner_(p);

    return ContentService.createTextOutput(JSON.stringify({ok: true}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ok: false, error: String(err)}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/* ---------- 2. INSTANT CONFIRMATION EMAIL TO THE LEAD ---------- */
function sendConfirmationEmail_(name, email, website) {
  const subject = 'Your Free 25-Point Website Audit is Being Prepared ✅';
  const html = emailShell_(`
    <h2 style="color:#0A2540;margin-top:0;">Hi ${esc_(name)},</h2>
    <p>Thank you for requesting your <b>free 25-point audit</b> for
       <b>${esc_(website)}</b>.</p>
    <p>Our team is scanning your website right now across lead capture, tracking,
       security, SEO and <b>AI search visibility</b> (whether ChatGPT, Gemini &amp;
       Perplexity recommend your business).</p>
    <p><b>Your report arrives within 1–2 hours</b> — by email and WhatsApp.</p>
    <p>Have a question meanwhile? Just reply to this email or
       <a href="${WHATSAPP_LINK}" style="color:#65A30D;font-weight:bold;">message us on WhatsApp</a>.</p>
    <p style="margin-bottom:0;">Talk soon,<br>
       <b>Amit Ahuja</b><br>Founder, The Website Auditor<br>
       +91 98866 50133 | thewebsiteauditor.com</p>
  `);
  GmailApp.sendEmail(email, subject, stripHtml_(html), {htmlBody: html, name: FROM_NAME});
}

/* ---------- 3. NEW LEAD ALERT TO YOU ---------- */
function notifyOwner_(p) {
  const body = `🔔 NEW LEAD — thewebsiteauditor.com

Name:    ${p.name}
Email:   ${p.email}
Phone:   ${p.phone}
Website: ${p.website}
Message: ${p.message || '-'}

→ Open the sheet and start the audit. Status auto-set to "New".`;
  GmailApp.sendEmail(NOTIFY_EMAIL, `🔔 New Lead: ${p.name} (${p.website})`, body, {name: 'Lead Bot'});
}

/* ---------- 4. DAILY 15-DAY FOLLOW-UP BOT ---------- */
function dailyFollowUp() {
  const sheet = getSheet_();
  const rows = sheet.getDataRange().getValues();
  const now = new Date();
  let sent = 0;

  for (let i = 1; i < rows.length; i++) {
    const [ts, name, email, , website, , status, followUpSent] = rows[i];
    if (!email || followUpSent) continue;
    if (['Replied','Won','Closed'].indexOf(String(status).trim()) !== -1) continue;

    const ageDays = (now - new Date(ts)) / (1000 * 60 * 60 * 24);
    if (ageDays >= FOLLOWUP_DAYS) {
      sendFollowUpEmail_(name, email, website);
      sheet.getRange(i + 1, COLS.indexOf('FollowUpSent') + 1).setValue(new Date());
      sent++;
      Utilities.sleep(1500); // gentle sending pace protects sender reputation
    }
  }
  if (sent > 0) {
    GmailApp.sendEmail(NOTIFY_EMAIL, `📬 Follow-up bot sent ${sent} reminder(s) today`,
      `The 15-day follow-up bot emailed ${sent} lead(s). Check the sheet's FollowUpSent column.`,
      {name: 'Lead Bot'});
  }
}

function sendFollowUpEmail_(name, email, website) {
  const subject = `${esc_(name)}, we'll fix 2 website issues for you — FREE`;
  const html = emailShell_(`
    <h2 style="color:#0A2540;margin-top:0;">Hi ${esc_(name)},</h2>
    <p>Two weeks ago we audited <b>${esc_(website)}</b> and sent your free 25-point report.
       I wanted to check in personally.</p>
    <p>To make this easy, here's my offer this week:</p>
    <div style="background:#F0FDF4;border-left:4px solid #A3E635;padding:14px 18px;border-radius:6px;">
      <b>We will fix the 2 most critical issues from your report — completely free,
      no strings attached.</b> You see the result first, then decide if you want more.
    </div>
    <p>Just reply "<b>YES</b>" to this email or
       <a href="${WHATSAPP_LINK}" style="color:#65A30D;font-weight:bold;">tap here to WhatsApp me</a>
       and we'll get started this week.</p>
    <p style="margin-bottom:0;">Best regards,<br>
       <b>Amit Ahuja</b><br>Founder, The Website Auditor<br>
       +91 98866 50133 | thewebsiteauditor.com</p>
    <p style="font-size:11px;color:#999;">If you'd rather not hear from us again,
       just reply "unsubscribe" and we'll remove you immediately.</p>
  `);
  GmailApp.sendEmail(email, subject, stripHtml_(html), {htmlBody: html, name: FROM_NAME});
}

/* ---------- 5. ONE-TIME SETUP ---------- */
function setupSheetAndTrigger() {
  // Ensure sheet + header row exist
  const sheet = getSheet_();
  if (sheet.getLastRow() === 0) sheet.appendRow(COLS);
  sheet.getRange(1, 1, 1, COLS.length).setFontWeight('bold').setBackground('#0A2540').setFontColor('#FFFFFF');

  // Remove old triggers, install daily 9 AM follow-up
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('dailyFollowUp').timeBased().everyDays(1).atHour(9).create();

  Logger.log('✅ Setup complete: sheet ready, daily 9 AM follow-up trigger installed.');
}

/* ---------- helpers ---------- */
function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
}

function emailShell_(inner) {
  return `<div style="font-family:Arial,Helvetica,sans-serif;max-width:600px;margin:0 auto;color:#333;line-height:1.6;">
    <div style="background:#0A2540;padding:20px;text-align:center;border-radius:8px 8px 0 0;">
      <span style="color:#A3E635;font-size:20px;font-weight:bold;">🔍 The Website Auditor</span>
    </div>
    <div style="padding:24px;border:1px solid #E5E7EB;border-top:none;border-radius:0 0 8px 8px;">
      ${inner}
    </div>
    <p style="font-size:11px;color:#999;text-align:center;">The Website Auditor · Bangalore, India · thewebsiteauditor.com</p>
  </div>`;
}

function esc_(s) { return String(s || '').replace(/[<>&"]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c])); }
function stripHtml_(h) { return h.replace(/<[^>]+>/g, '').replace(/\s+\n/g, '\n').trim(); }
