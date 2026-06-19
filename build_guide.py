"""Generate the Street Hebrew Survival Guide PDF — v5 image-Hebrew edition.

Some PDF viewers (Microsoft Word's PDF preview, Office viewers, some
mobile readers) try to re-apply their own bidi shaping to the text in
the PDF, which double-reverses Hebrew and shows it scrambled. To make
the guide bullet-proof across every viewer, each Hebrew phrase is
rasterized to a PNG with PIL + Heebo + python-bidi, then embedded in
the HTML. Hebrew is no longer text in the PDF — it's pixels — so no
viewer can re-interpret it. Trade-off: Hebrew text isn't selectable,
which is fine for a marketing lead magnet.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from bidi import get_display
from weasyprint import HTML, CSS

ROOT = Path(__file__).parent
FONT_DIR = ROOT / "fonts"
IMG_DIR = ROOT / "_heb_images"
IMG_DIR.mkdir(exist_ok=True)
OUT = ROOT / "Street_Hebrew_Survival_Guide_v5_Final.pdf"

WHATSAPP_URL = "https://thehebrewsprint.com/#pricing"

# PIL Hebrew rendering — high DPI for crisp print + zoom
HEB_FONT = ImageFont.truetype(str(FONT_DIR / "Heebo-Bold.ttf"), 96)
HEB_COLOR = (13, 31, 60, 255)  # navy
RENDER_SCALE = 4  # 4x for retina sharpness

# ---------------------------------------------------------------------------
# Data — phrases in LOGICAL Hebrew order (no bidi preprocessing needed)
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "n": "01",
        "icon": "&#x1F3DB;",
        "title": "Public Spaces & Bureaucracy",
        "subtitle": "Survive any clerk, landlord, or government counter.",
        "key": "navy",
        "phrases": [
            ("סליחה, אפשר לעזור לי?", "Slee-cha, ef-shar la-a-ZOR li?",
             "Excuse me, can you help me? (polite opener — works everywhere)"),
            ("יש לי בעיה עם החשמל.", "Yesh li be-a-YA im ha-CHASH-mal.",
             "I have a problem with the electricity. (landlord&rsquo;s cue to panic)"),
            ("מתי אפשר לתקן?", "Ma-TAI ef-shar le-ta-KEN?",
             "When can it be fixed? (the follow-up that actually gets results)"),
            ("יש לי תור ב-9.", "Yesh li TOR be-TEI-sha.",
             "I have an appointment at 9. (skips the line, trust me)"),
            ("צריך לשלם ארנונה.", "Tzar-ICH li-sh-LEM ar-NO-na.",
             "Need to pay municipal tax. (say it confidently, they&rsquo;ll respect that)"),
            ("אפשר לקבל קבלה?", "Ef-SHAR le-ka-BEL ka-ba-LA?",
             "Can I get a receipt? (essential for any Israeli transaction)"),
            ("הלינק לא עובד.", "Ha-LINK lo o-VED.",
             "The link doesn&rsquo;t work. (universal Israeli tech complaint)"),
            ("יש טופס למלא?", "Yesh TOH-fes le-ma-LE?",
             "Is there a form to fill? (shows you know the drill)"),
            ("אני חדש פה.", "A-NI cha-DASH po.",
             "I&rsquo;m new here. (magic phrase &mdash; unlocks extra patience from any clerk)"),
            ("תודה רבה, עזרת לי מאוד.", "To-DA ra-BA, a-ZAR-ta li me-OD.",
             "Thank you so much, you helped me a lot. (ends any interaction on a high note)"),
        ],
    },
    {
        "n": "02",
        "icon": "&#x2615;",
        "title": "Cafes & Restaurants",
        "subtitle": "Order, sip, and pay like a Tel Aviv regular.",
        "key": "brown",
        "phrases": [
            ("קפה הפוך, בבקשה.", "Ka-FE ha-FUCH, be-va-ka-SHA.",
             "Upside-down coffee (Israeli latte). The national drink. Order this, belong."),
            ("בלי סוכר.", "Be-LI su-KAR.",
             "Without sugar. (they&rsquo;ll add it anyway &mdash; say this twice)"),
            ("עם חלב בצד.", "Im cha-LAV ba-TZAD.",
             "Milk on the side. (sounds very Israeli, very intentional)"),
            ("מה הסגנון?", "Ma ha-sig-NON?",
             "What&rsquo;s the vibe? (asked before choosing a cafe &mdash; instant local cred)"),
            ("אפשר מים?", "Ef-SHAR ma-YIM?",
             "Can I have water? (free, always &mdash; but you have to ask)"),
            ("זה טעים מאוד!", "Ze ta-IM me-OD!",
             "This is delicious! (say it loud &mdash; the owner is always nearby)"),
            ("יש ויתר בלי גלוטן?", "Ve-i-TER be-LI glu-TEN?",
             "Is there a gluten-free option? (Tel Aviv is very gluten-aware)"),
            ("חשבון, בבקשה.", "Chesh-BON, be-va-ka-SHA.",
             "Check, please. (wave your hand once &mdash; no need to chase the waiter)"),
            ("ביחד או נפרד?", "Be-ya-CHAD o nif-RAD?",
             "Together or separate? (they&rsquo;ll ask &mdash; now you know what it means)"),
            ("לקחת.", "La-KA-chat.",
             "To-go. (one word, zero confusion)"),
        ],
    },
    {
        "n": "03",
        "icon": "&#x1F6D2;",
        "title": "Markets & Money",
        "subtitle": "Bargain at the shuk and walk out with the win.",
        "key": "green",
        "phrases": [
            ("כמה זה עולה?", "Ka-MA ze O-le?",
             "How much does it cost? (ask before touching anything at Mahane Yehuda)"),
            ("זה יקר מדי.", "Ze ya-KAR mi-DAI.",
             "That&rsquo;s too expensive. (say it, pause, look away &mdash; watch the price drop)"),
            ("אפשר קצת יותר בזול?", "Ef-SHAR ktsat yo-TER be-ZOL?",
             "Can it be a bit cheaper? (the golden negotiation phrase)"),
            ("אקח שניים.", "E-KACH shna-YIM.",
             "I&rsquo;ll take two. (the magic number that always gets a discount)"),
            ("בכרטיס אשראי.", "Be-kar-TIS ash-RAI.",
             "By credit card. (they&rsquo;ll try to convince you cash is better &mdash; hold firm)"),
            ("קבלה, בבקשה.", "Ka-ba-LA, be-va-ka-SHA.",
             "Receipt, please. (non-negotiable, always ask)"),
            ("יש מבצע?", "Yesh miv-TZA?",
             "Is there a sale/deal? (the Israeli national question)"),
            ("אפשר לטעום?", "Ef-SHAR lit-OM?",
             "Can I taste? (at markets, always yes &mdash; just ask)"),
            ("זה טרי?", "Ze ta-RI?",
             "Is this fresh? (for anything at the market &mdash; they respect the question)"),
            ("סגרנו עסקה.", "Sa-GAR-nu is-KA.",
             "We&rsquo;ve got a deal. (seals the negotiation &mdash; very Israeli energy)"),
        ],
    },
    {
        "n": "04",
        "icon": "&#x1F91D;",
        "title": "Small Talk & Networking",
        "subtitle": "Slip into any conversation and sound like an insider.",
        "key": "purple",
        "phrases": [
            ("מה נשמע?", "Ma nish-MA?",
             "What&rsquo;s up? (the Israeli &lsquo;hello&rsquo; &mdash; use it constantly)"),
            ("הכל בסדר?", "Ha-KOL be-SE-der?",
             "Is everything okay? (warm check-in, very common)"),
            ("אח שלי!", "ACH she-LI!",
             "My brother! (term of endearment &mdash; used between strangers, means you&rsquo;re in)"),
            ("סבבה גמור.", "Sa-BA-ba ga-MUR.",
             "Totally cool / all good. (highest level of Israeli approval)"),
            ("תכלס, מה המצב?", "Tach-LES, ma ha-ma-TZAV?",
             "Real talk &mdash; what&rsquo;s the situation? (skips small talk, gets to business)"),
            ("מאיפה אתה?", "Me-EI-fo a-TA?",
             "Where are you from? (they WILL ask within 30 seconds)"),
            ("אני לומד עברית.", "A-NI lo-MED iv-RIT.",
             "I&rsquo;m learning Hebrew. (instant goodwill &mdash; they&rsquo;ll want to help you)"),
            ("יאללה, ביי!", "Ya-LA, bai!",
             "Yalla, bye! (the Israeli goodbye &mdash; iconic, use it)"),
            ("חבל על הזמן, זה מדהים.", "Cha-VAL al ha-ZMAN, ze mad-HIM.",
             "What a waste of time &mdash; it&rsquo;s amazing! (sounds negative, means amazing)"),
            ("נדבר.", "Ne-da-BER.",
             "We&rsquo;ll talk. (ends any conversation like a boss)"),
        ],
    },
    {
        "n": "05",
        "icon": "&#x1F6A8;",
        "title": "Emergency & Logistics",
        "subtitle": "The phrases that save the day &mdash; and the delivery.",
        "key": "red",
        "phrases": [
            ("עזרה!", "ez-RA!",
             "Help! (short, loud, universal)"),
            ("אני לא מבין/ה.", "A-NI lo me-VIN / me-VI-na.",
             "I don&rsquo;t understand. (say it early, before you nod and regret)"),
            ("אפשר לדבר לאט?", "Ef-SHAR le-da-BER le-AT?",
             "Can you speak slowly? (they&rsquo;ll slow down &mdash; Israelis are impatient but kind)"),
            ("אני מחכה למשלוח.", "A-NI me-cha-KE le-mish-LO-ach.",
             "I&rsquo;m waiting for a delivery. (Wolt driver on the phone &mdash; this is it)"),
            ("אני בכניסה.", "A-NI ba-kni-SA.",
             "I&rsquo;m at the entrance. (second call from the driver &mdash; use this)"),
            ("תתקשר אליי.", "Tit-ka-SHER e-LAI.",
             "Call me. (simple, direct, works)"),
            ("אני אבוד/ה.", "A-NI a-VUD / a-vu-DA.",
             "I&rsquo;m lost. (better to admit it than wander for 40 minutes)"),
            ("יש פה וויפי?", "Yesh po WI-FI?",
             "Is there WiFi here? (crosses all cultural barriers)"),
            ("דחוף.", "Da-CHUF.",
             "Urgent. (one word &mdash; opens doors and skips queues)"),
            ("תודה, הצלת אותי.", "To-DA, hi-TZAL-ta o-TI.",
             "Thank you, you saved me. (the best thing you can say to any Israeli who helped)"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Font + CSS
# ---------------------------------------------------------------------------
def font_face(family: str, file: str, weight: str = "normal",
              style: str = "normal") -> str:
    path = (FONT_DIR / file).resolve().as_uri()
    return (f"@font-face {{ font-family: '{family}'; src: url({path}); "
            f"font-weight: {weight}; font-style: {style}; }}")


def symbola_face() -> str:
    return ("@font-face { font-family: 'Symbola'; "
            "src: url(file:///usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf); }")


FONTS_CSS = "\n".join([
    font_face("Heebo", "Heebo-Regular.ttf", "400"),
    font_face("Heebo", "Heebo-Medium.ttf", "500"),
    font_face("Heebo", "Heebo-Bold.ttf", "700"),
    font_face("Heebo", "Heebo-ExtraBold.ttf", "800"),
    font_face("Heebo", "Heebo-Black.ttf", "900"),
    font_face("Inter", "Inter-Regular.ttf", "400"),
    font_face("Inter", "Inter-Italic.ttf", "400", "italic"),
    font_face("Inter", "Inter-Medium.ttf", "500"),
    font_face("Inter", "Inter-MediumItalic.ttf", "500", "italic"),
    font_face("Inter", "Inter-SemiBold.ttf", "600"),
    font_face("Inter", "Inter-Bold.ttf", "700"),
    font_face("Inter", "Inter-ExtraBold.ttf", "800"),
    symbola_face(),
])


CSS_BODY = r"""
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact; }

:root {
  --navy: #0D1F3C;
  --navy-soft: #1A2D52;
  --electric: #1A73E8;
  --electric-dark: #0B5BC7;
  --gold: #F4A724;
  --gold-deep: #C98700;
  --light-gray: #F7F8FA;
  --row-alt: #FAFBFD;
  --border: #E5E8F0;
  --ink: #1A2138;
  --ink-soft: #4B5572;
  --muted: #8693B1;
  --cream: #FFF6DE;
  --light-blue: #E8F0FE;
  --red: #B71C1C;

  --cat-navy: #0D1F3C;
  --cat-brown: #7B3F00;
  --cat-green: #1E8B4C;
  --cat-purple: #6A1B9A;
  --cat-red: #B71C1C;
}

@page {
  size: A4;
  margin: 0;
}
@page cover {
  margin: 0;
  background: var(--navy);
}
@page content {
  margin: 0;
  @top-left  { content: ''; }
  @bottom-left { content: ''; }
}

html, body {
  font-family: 'Inter', sans-serif;
  color: var(--ink);
  background: white;
  font-size: 11pt;
  line-height: 1.45;
}

.page {
  width: 210mm;
  height: 297mm;
  position: relative;
  overflow: hidden;
  page-break-after: always;
}
.page:last-child { page-break-after: auto; }

/* =================================================================== */
/* COVER                                                               */
/* =================================================================== */
.cover {
  background: linear-gradient(155deg, #0D1F3C 0%, #15294F 55%, #0D1F3C 100%);
  color: white;
  padding: 0;
}
.cover::before {
  content: '';
  position: absolute; inset: 0;
  background-image: repeating-linear-gradient(
    135deg, rgba(255,255,255,0.04) 0 1px, transparent 1px 28px);
  pointer-events: none;
}
.cover::after {
  content: '';
  position: absolute;
  width: 520px; height: 520px;
  background: radial-gradient(circle, rgba(106,150,255,0.18) 0%, transparent 60%);
  top: -100px; left: 50%;
  transform: translateX(-50%);
  pointer-events: none;
}
.cover .gold-bar-top, .cover .gold-bar-bottom {
  position: absolute; left: 0; right: 0; height: 8px;
  background: var(--gold);
}
.cover .gold-bar-top { top: 0; }
.cover .gold-bar-bottom { bottom: 0; }
.cover .gold-bar-top::after, .cover .gold-bar-bottom::after {
  content: ''; position: absolute; left: 0; right: 0; height: 1px;
  background: rgba(255,255,255,0.3);
}
.cover .gold-bar-top::after { bottom: -3px; }
.cover .gold-bar-bottom::after { top: -3px; }

.cover-inner {
  position: relative;
  z-index: 2;
  padding: 28mm 22mm 24mm 22mm;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.kicker {
  text-align: center;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 9pt;
  letter-spacing: 0.18em;
  color: var(--gold);
  display: inline-block;
}
.kicker-wrap {
  text-align: center;
  display: flex; align-items: center; justify-content: center;
  gap: 12px;
  margin-bottom: 12mm;
}
.kicker-wrap::before, .kicker-wrap::after {
  content: ''; display: inline-block;
  width: 24px; height: 1px; background: var(--gold);
}

.flag {
  width: 92px; height: 62px; margin: 0 auto;
  background: white;
  border-radius: 5px;
  border: 1px solid rgba(255,255,255,0.4);
  position: relative;
}
.flag::before, .flag::after {
  content: ''; position: absolute; left: 0; right: 0; height: 7px;
  background: #0038B8;
}
.flag::before { top: 10px; }
.flag::after  { bottom: 10px; }
.flag-star {
  position: absolute; top: 50%; left: 50%;
  width: 28px; height: 28px;
  transform: translate(-50%, -50%);
  color: #0038B8;
}

.title {
  text-align: center;
  margin-top: 14mm;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 36pt;
  line-height: 1.05;
  letter-spacing: -0.01em;
  color: white;
}
.title .gold { color: var(--gold); display: block; margin-top: 2mm; }

.title-rule {
  width: 60px; height: 3px;
  background: var(--gold);
  margin: 6mm auto 5mm auto;
  border-radius: 2px;
}

.subtitle {
  text-align: center;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 13pt;
  line-height: 1.55;
  color: rgba(255,255,255,0.92);
}
.subtitle .gold-it {
  display: block; margin-top: 4mm;
  color: var(--gold); font-style: italic; font-weight: 500; font-size: 11pt;
}

.pills {
  display: flex; justify-content: center; gap: 7px;
  margin-top: 7mm; flex-wrap: nowrap;
}
.pill {
  display: inline-block;
  padding: 5px 12px 5px 22px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.32);
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 7.5pt;
  letter-spacing: 0.06em;
  color: white;
  white-space: nowrap;
  position: relative;
}
.pill .dot {
  position: absolute;
  left: 9px; top: 50%;
  width: 7px; height: 7px;
  margin-top: -3.5px;
  border-radius: 50%;
}
.pill.navy   .dot { background: #F4A724; }
.pill.brown  .dot { background: #C97A2A; }
.pill.green  .dot { background: #1E8B4C; }
.pill.purple .dot { background: #9D4ED1; }
.pill.red    .dot { background: #E33B3B; }

.quote-card {
  margin-top: auto;
  margin-bottom: 18mm;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 14px;
  border-left: 4px solid var(--gold);
  padding: 18px 22px 16px 22px;
  color: rgba(255,255,255,0.94);
  position: relative;
}
.quote-label {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 8.5pt;
  letter-spacing: 0.18em;
  color: var(--gold);
  padding-bottom: 4px;
  border-bottom: 1.5px solid var(--gold);
  display: inline-block;
  margin-bottom: 11px;
}
.quote-text {
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-weight: 500;
  font-size: 11.5pt;
  line-height: 1.6;
}
.quote-attr {
  margin-top: 14px;
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-size: 9.5pt;
  color: rgba(255,255,255,0.65);
}

.cover-footer {
  position: absolute;
  bottom: 14mm;
  left: 0; right: 0;
  text-align: center;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 9pt;
  color: rgba(255,255,255,0.55);
}

/* =================================================================== */
/* CONTENT PAGES                                                       */
/* =================================================================== */
.content {
  padding: 0;
  background: white;
}
.content-header {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 10mm;
  background: var(--navy);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 12mm;
  border-bottom: 3px solid var(--gold);
}
.content-header .brand {
  color: white;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 9.5pt;
  letter-spacing: 0.08em;
}
.content-header .pub {
  color: var(--gold);
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-weight: 500;
  font-size: 9pt;
}
.content-footer {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 10mm;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 12mm;
  border-top: 1px solid var(--border);
  background: white;
}
.content-footer .site {
  color: var(--muted);
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 8.5pt;
}
.content-footer .pgnum {
  color: var(--ink);
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 8.5pt;
  letter-spacing: 0.06em;
}

.content-body {
  position: absolute;
  top: 15mm; bottom: 15mm; left: 10mm; right: 10mm;
}
.pitch .content-body {
  top: 18mm; bottom: 15mm; left: 14mm; right: 14mm;
}

/* category header card */
.cat {
  border-radius: 10px;
  color: white;
  position: relative;
  display: flex; align-items: center;
  padding: 7px 14px 7px 12px;
  overflow: hidden;
}
.cat::after {
  content: ''; position: absolute; right: 8px; top: 12px; bottom: 12px;
  width: 3px; border-radius: 1.5px; background: var(--gold);
}
.cat.navy   { background: var(--cat-navy); }
.cat.brown  { background: var(--cat-brown); }
.cat.green  { background: var(--cat-green); }
.cat.purple { background: var(--cat-purple); }
.cat.red    { background: var(--cat-red); }

.cat-num {
  display: flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; border-radius: 50%;
  background: rgba(255,255,255,0.16);
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 9.5pt;
  margin-right: 12px;
}
.cat-icon {
  font-family: 'Symbola', sans-serif;
  font-size: 14pt;
  margin-right: 12px;
  line-height: 1;
}
.cat-meta { flex: 1; }
.cat-title {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 12.5pt;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  line-height: 1.1;
}
.cat-sub {
  margin-top: 1px;
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-weight: 500;
  font-size: 8.5pt;
  color: rgba(255,255,255,0.82);
}

/* phrases table */
.phrases {
  border-collapse: collapse;
  width: 100%;
  margin: 4px 0 8px 0;
  table-layout: fixed;
  border-radius: 8px;
  overflow: hidden;
}
.phrases td {
  vertical-align: middle;
  padding: 5.5px 10px;
  border-bottom: 0.5px solid var(--border);
  font-size: 8.5pt;
}
.phrases tr:last-child td { border-bottom: none; }
.phrases tr:nth-child(odd) td { background: var(--row-alt); }
.phrases td.heb {
  width: 38%;
  text-align: right;
  border-right: 3px solid transparent;
  padding-right: 14px;
  padding-top: 8px;
  padding-bottom: 8px;
  vertical-align: middle;
}
.phrases td.heb img {
  height: 26px;
  width: auto;
  max-width: 100%;
  display: inline-block;
  vertical-align: middle;
}
.cat-navy ~ .phrases td.heb,
.phrases.navy   td.heb { border-right-color: var(--cat-navy); }
.phrases.brown  td.heb { border-right-color: var(--cat-brown); }
.phrases.green  td.heb { border-right-color: var(--cat-green); }
.phrases.purple td.heb { border-right-color: var(--cat-purple); }
.phrases.red    td.heb { border-right-color: var(--cat-red); }

.phrases td.phon {
  width: 25%;
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-weight: 500;
  font-size: 8.4pt;
  line-height: 1.35;
  color: var(--electric);
  border-left: 0.5px solid var(--border);
  padding-left: 12px;
}
.phrases td.mean {
  width: 37%;
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 8.4pt;
  color: var(--ink-soft);
  line-height: 1.4;
  padding-left: 12px;
  border-left: 0.5px solid var(--border);
}

/* =================================================================== */
/* PITCH                                                               */
/* =================================================================== */
.pitch {
  background: var(--light-gray);
}
.pitch .content-body { padding: 0; }
.pitch-kicker {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 9pt;
  letter-spacing: 0.18em;
  color: var(--muted);
}
.pitch-kicker::before {
  content: ''; display: inline-block;
  width: 28px; height: 3px;
  background: var(--gold);
  margin-right: 10px;
  vertical-align: 4px;
}
.pitch h1 {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 26pt;
  line-height: 1.15;
  letter-spacing: -0.01em;
  color: var(--navy);
  margin-top: 10px;
}
.pitch h1 .gold { color: var(--gold-deep); display: block; }

.pitch-lede {
  font-family: 'Inter', sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  color: var(--ink-soft);
  margin-top: 12px;
}

.program-card {
  margin-top: 18px;
  background: var(--navy);
  color: white;
  border-radius: 12px;
  padding: 16px 22px;
  position: relative;
}
.program-card::before {
  content: ''; position: absolute;
  left: 12px; top: 14px; bottom: 14px;
  width: 3px; border-radius: 2px;
  background: var(--gold);
}
.program-card .intro {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 9pt;
  letter-spacing: 0.18em;
  color: var(--gold);
  padding-left: 14px;
}
.program-card .name {
  margin-top: 4px;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 21pt;
  letter-spacing: -0.005em;
  padding-left: 14px;
}

.features {
  display: flex; gap: 10px;
  margin-top: 16px;
}
.feature {
  flex: 1;
  background: white;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 14px 12px 14px;
  position: relative;
}
.feature .ico {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: var(--light-blue);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 9px;
}
.feature .ico svg { width: 20px; height: 20px; fill: none; stroke: var(--electric); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.feature h3 {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 10.5pt;
  color: var(--navy);
  line-height: 1.25;
}
.feature p {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 8.7pt;
  color: var(--ink-soft);
  line-height: 1.45;
  margin-top: 5px;
}

.divider-gold {
  margin: 18px auto 14px auto;
  width: 72px; height: 2px;
  background: var(--gold);
  border-radius: 1px;
}

.offer {
  background: var(--light-blue);
  border: 1.4px solid var(--electric);
  border-radius: 14px;
  padding: 16px 20px 18px 20px;
  position: relative;
}
.offer .ribbon {
  position: absolute; top: 14px; right: 18px;
  background: var(--electric);
  color: white;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 8.5pt;
  letter-spacing: 0.1em;
  padding: 4px 10px;
  border-radius: 999px;
}
.offer .lead {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 10.5pt;
  color: var(--navy);
  line-height: 1.4;
}
.offer .price-row {
  display: flex; align-items: baseline; gap: 14px;
  margin-top: 10px;
}
.offer .price-now {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 34pt;
  color: var(--electric);
  line-height: 1;
}
.offer .price-was {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 15pt;
  color: var(--muted);
  text-decoration: line-through;
  text-decoration-color: var(--red);
  text-decoration-thickness: 1.5px;
}
.offer .save {
  background: var(--gold);
  color: var(--navy);
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 9pt;
  letter-spacing: 0.08em;
  padding: 5px 10px;
  border-radius: 999px;
  align-self: center;
}
.offer .scarcity {
  margin-top: 10px;
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-weight: 500;
  font-size: 9.5pt;
  color: var(--red);
}

.cta {
  display: block;
  margin-top: 16px;
  background: linear-gradient(180deg, var(--electric) 0%, var(--electric-dark) 100%);
  color: white;
  text-align: center;
  text-decoration: none;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 14pt;
  padding: 18px 0;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(26,115,232,0.25);
}
.cta-note {
  margin-top: 10px;
  text-align: center;
  font-family: 'Inter', sans-serif;
  font-style: italic;
  font-size: 9pt;
  color: var(--muted);
}

.proof {
  margin-top: 12px;
  display: flex; gap: 14px; justify-content: center;
  font-family: 'Inter', sans-serif;
  font-size: 8.5pt;
  color: var(--muted);
}
.proof .star { color: var(--gold); margin-right: 3px; }
"""


# ---------------------------------------------------------------------------
# Hebrew → PNG rasterizer (one image per phrase, cached on disk)
# ---------------------------------------------------------------------------
def hebrew_image(text: str) -> str:
    """Render a Hebrew phrase to a PNG file and return its file:// URI.

    PIL/Pillow with a TrueType font calls HarfBuzz under the hood, which
    handles Hebrew bidi shaping natively. Pass the logical Unicode text
    directly — DO NOT pre-bidi with python-bidi, that double-reverses.
    """
    key = hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]
    out = IMG_DIR / f"heb_{key}.png"
    if not out.exists():
        bbox = HEB_FONT.getbbox(text)
        left, top, right, bottom = bbox
        w = right - left
        h = bottom - top
        pad_x, pad_y = 14, 12
        img = Image.new("RGBA", (w + pad_x * 2, h + pad_y * 2), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        d.text((pad_x - left, pad_y - top), text, font=HEB_FONT, fill=HEB_COLOR)
        img.save(out, "PNG", optimize=True)
    return out.resolve().as_uri()


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------
def cover_html() -> str:
    pills = "".join(
        f'<span class="pill {c["key"]}"><span class="dot"></span>'
        f'{c["title"].split(" &")[0].split(" and")[0].upper().split(" & ")[0]}</span>'
        for c in CATEGORIES
    )
    # Simpler explicit pills (override above for cleaner labels)
    pill_labels = [
        ("navy", "PUBLIC SPACES"),
        ("brown", "CAFES"),
        ("green", "MARKETS"),
        ("purple", "SMALL TALK"),
        ("red", "EMERGENCY"),
    ]
    pills = "".join(
        f'<span class="pill {k}"><span class="dot"></span>{label}</span>'
        for k, label in pill_labels
    )

    # Star of David — two interlocking triangles
    flag_svg = """
      <svg class="flag-star" viewBox="0 0 50 50">
        <polygon points="25,4 32,16 46,16 35,25 39,38 25,30 11,38 15,25 4,16 18,16"
                 fill="none" stroke="#0038B8" stroke-width="2.6"
                 stroke-linejoin="round"/>
        <polygon points="25,4 33,18 17,18" fill="none" stroke="#0038B8"
                 stroke-width="2.6" stroke-linejoin="round"/>
        <polygon points="25,46 33,32 17,32" fill="none" stroke="#0038B8"
                 stroke-width="2.6" stroke-linejoin="round"/>
      </svg>
    """
    return f"""
    <div class="page cover">
      <div class="gold-bar-top"></div>
      <div class="gold-bar-bottom"></div>
      <div class="cover-inner">
        <div class="kicker-wrap"><span class="kicker">HEBREW IN 40 DAYS &middot; FREE GUIDE</span></div>

        <div class="flag">{flag_svg}</div>

        <h1 class="title">THE STREET HEBREW<span class="gold">SURVIVAL GUIDE</span></h1>
        <div class="title-rule"></div>

        <p class="subtitle">
          50 essential phrases to navigate the Israeli street<br/>with 100% confidence.
          <span class="gold-it">Zero grammar inside.</span>
        </p>

        <div class="pills">{pills}</div>

        <div class="quote-card">
          <div class="quote-label">FROM THE CREATOR</div>
          <div class="quote-text">
            I spent weeks in Ulpan learning how to write essays, but froze when the
            Wolt delivery guy called. I created this guide so you don&rsquo;t have to
            experience that &lsquo;street paralysis&rsquo; &mdash; here is the exact
            script you need to sound like a local.
          </div>
          <div class="quote-attr">&mdash; Built for new Israelis, by a frustrated Ulpan grad.</div>
        </div>

        <div class="cover-footer">thehebrewsprint.com &middot; Free Preview Edition</div>
      </div>
    </div>
    """


def category_html(cat: dict) -> str:
    rows = ""
    for hb, phon, meaning in cat["phrases"]:
        img_uri = hebrew_image(hb)
        rows += (
            f"<tr>"
            f"<td class='heb'><img src='{img_uri}' alt='{hb}'/></td>"
            f"<td class='phon'>{phon}</td>"
            f"<td class='mean'>{meaning}</td>"
            f"</tr>"
        )
    return f"""
      <div class="cat {cat['key']}">
        <div class="cat-num">{cat['n']}</div>
        <div class="cat-icon">{cat['icon']}</div>
        <div class="cat-meta">
          <div class="cat-title">{cat['title']}</div>
          <div class="cat-sub">{cat['subtitle']}</div>
        </div>
      </div>
      <table class="phrases {cat['key']}">{rows}</table>
    """


def content_page_html(page_num: int, cats: list[dict]) -> str:
    body = "".join(category_html(c) for c in cats)
    return f"""
    <div class="page content">
      <div class="content-header">
        <div class="brand">STREET HEBREW SURVIVAL GUIDE</div>
        <div class="pub">Hebrew in 40 Days</div>
      </div>
      <div class="content-body">{body}</div>
      <div class="content-footer">
        <div class="site">thehebrewsprint.com</div>
        <div class="pgnum">PAGE {page_num} OF 5</div>
      </div>
    </div>
    """


def pitch_html() -> str:
    return f"""
    <div class="page content pitch">
      <div class="content-header">
        <div class="brand">STREET HEBREW SURVIVAL GUIDE</div>
        <div class="pub">Hebrew in 40 Days</div>
      </div>
      <div class="content-body">
        <div class="pitch-kicker">STEP 02 &middot; THE NEXT MOVE</div>
        <h1>Now you have the words.<span class="gold">But do you have the reflex?</span></h1>
        <p class="pitch-lede">
          Knowing 50 phrases on paper is great. But the Israeli street moves fast.
          When someone speaks back to you at lightning speed, you need more than a
          cheat sheet. <strong>You need muscle memory.</strong>
        </p>

        <div class="program-card">
          <div class="intro">INTRODUCING</div>
          <div class="name">The 40-Day Hebrew Sprint</div>
        </div>

        <div class="features">
          <div class="feature">
            <div class="ico">
              <svg viewBox="0 0 24 24" fill="none" stroke="#1A73E8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 14v-2a9 9 0 0 1 18 0v2"/>
                <path d="M21 14v4a2 2 0 0 1-2 2h-1v-7h3z"/>
                <path d="M3 14v4a2 2 0 0 0 2 2h1v-7H3z"/>
              </svg>
            </div>
            <h3>Daily 2-min audio bites</h3>
            <p>Straight to your phone. Listen on the bus, in line, while you stir coffee.</p>
          </div>
          <div class="feature">
            <div class="ico">
              <svg viewBox="0 0 24 24" fill="none" stroke="#1A73E8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="9"/>
                <path d="M9 9l6 6M15 9l-6 6"/>
              </svg>
            </div>
            <h3>Zero grammar. 100% action.</h3>
            <p>Built for the street, not the classroom. Memorize, repeat, deploy.</p>
          </div>
          <div class="feature">
            <div class="ico">
              <svg viewBox="0 0 24 24" fill="none" stroke="#1A73E8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 12a8 8 0 0 1-11.5 7.2L4 21l1.8-5.5A8 8 0 1 1 21 12z"/>
                <circle cx="9" cy="12" r="0.8" fill="#1A73E8"/>
                <circle cx="12.5" cy="12" r="0.8" fill="#1A73E8"/>
                <circle cx="16" cy="12" r="0.8" fill="#1A73E8"/>
              </svg>
            </div>
            <h3>Real-world challenges</h3>
            <p>Voice-message tasks that force you to think and speak in Hebrew.</p>
          </div>
        </div>

        <div class="divider-gold"></div>

        <div class="offer">
          <div class="ribbon">BETA &middot; 10 SPOTS</div>
          <div class="lead">
            Since you downloaded this guide, you can join our<br/>
            upcoming closed Beta cohort for just
          </div>
          <div class="price-row">
            <div class="price-now">$39</div>
            <div class="price-was">$149</div>
            <div class="save">SAVE $110</div>
          </div>
          <div class="scarcity">Only 10 spots available &mdash; first come, first served.</div>
        </div>

        <a class="cta" href="{WHATSAPP_URL}">Secure My Beta Spot &amp; Start Speaking Now  &rarr;</a>
        <div class="cta-note">Questions? Reply directly &mdash; we respond within 24 hours.</div>

        <div class="proof">
          <span><span class="star">&#x2605;&#x2605;&#x2605;&#x2605;&#x2605;</span> Loved by 1,200+ new Israelis</span>
          <span>&middot;</span>
          <span>Featured in 3 Tel Aviv expat groups</span>
          <span>&middot;</span>
          <span>Money-back guarantee</span>
        </div>
      </div>
      <div class="content-footer">
        <div class="site">thehebrewsprint.com</div>
        <div class="pgnum">PAGE 5 OF 5</div>
      </div>
    </div>
    """


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build() -> None:
    layout = [
        [CATEGORIES[0], CATEGORIES[1]],
        [CATEGORIES[2], CATEGORIES[3]],
        [CATEGORIES[4]],
    ]
    pages = [cover_html()]
    for i, cats in enumerate(layout, start=2):
        pages.append(content_page_html(i, cats))
    pages.append(pitch_html())

    html = f"""<!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8"/>
        <title>The Street Hebrew Survival Guide</title>
      </head>
      <body>{''.join(pages)}</body>
    </html>
    """

    css = CSS(string=FONTS_CSS + "\n" + CSS_BODY)
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(OUT), stylesheets=[css])
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
    print(f"Hebrew phrase images cached in {IMG_DIR}/")
