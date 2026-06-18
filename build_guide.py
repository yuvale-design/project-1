"""Generate the Street Hebrew Survival Guide PDF lead magnet — v3 elegant edition."""
from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from bidi import get_display

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
NAVY = HexColor("#0D1F3C")
NAVY_SOFT = HexColor("#1A2D52")
ELECTRIC = HexColor("#1A73E8")
ELECTRIC_DARK = HexColor("#0B5BC7")
GOLD = HexColor("#F4A724")
GOLD_DEEP = HexColor("#C98700")
LIGHT_GRAY = HexColor("#F7F8FA")
ROW_ALT = HexColor("#FAFBFD")
BORDER = HexColor("#E5E8F0")
INK = HexColor("#1A2138")
INK_SOFT = HexColor("#4B5572")
MUTED = HexColor("#8693B1")
CREAM = HexColor("#FFF6DE")
LIGHT_BLUE = HexColor("#E8F0FE")
RED_STRIKE = HexColor("#B71C1C")

CAT_NAVY = NAVY
CAT_BROWN = HexColor("#7B3F00")
CAT_GREEN = HexColor("#1E8B4C")
CAT_PURPLE = HexColor("#6A1B9A")
CAT_RED = HexColor("#B71C1C")

# ---------------------------------------------------------------------------
# Fonts — Heebo for Hebrew, Inter for Latin, Symbola for icons
# ---------------------------------------------------------------------------
FONT_DIR = Path(__file__).parent / "fonts"
SYMBOLA = "/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf"

_FONT_MAP = {
    "HebReg":    FONT_DIR / "Heebo-Regular.ttf",
    "HebMed":    FONT_DIR / "Heebo-Medium.ttf",
    "HebBold":   FONT_DIR / "Heebo-Bold.ttf",
    "HebXBold":  FONT_DIR / "Heebo-ExtraBold.ttf",
    "HebBlack":  FONT_DIR / "Heebo-Black.ttf",
    "Body":      FONT_DIR / "Inter-Regular.ttf",
    "BodyMed":   FONT_DIR / "Inter-Medium.ttf",
    "BodySemi":  FONT_DIR / "Inter-SemiBold.ttf",
    "BodyBold":  FONT_DIR / "Inter-Bold.ttf",
    "BodyXBold": FONT_DIR / "Inter-ExtraBold.ttf",
    "BodyIt":    FONT_DIR / "Inter-Italic.ttf",
    "BodyMedIt": FONT_DIR / "Inter-MediumItalic.ttf",
    "Symb":      Path(SYMBOLA),
}
for name, path in _FONT_MAP.items():
    pdfmetrics.registerFont(TTFont(name, str(path)))

PAGE_W, PAGE_H = A4


def heb(text: str) -> str:
    """Reorder Hebrew logical→visual so reportlab's LTR engine renders it correctly."""
    return get_display(text)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "n": "01",
        "icon": "\U0001F3DB",
        "title": "Public Spaces & Bureaucracy",
        "subtitle": "Survive any clerk, landlord, or government counter.",
        "color": CAT_NAVY,
        "phrases": [
            ("סליחה, אפשר לעזור לי?", "Slee-cha, ef-shar la-a-ZOR li?",
             "Excuse me, can you help me? (polite opener — works everywhere)"),
            ("יש לי בעיה עם החשמל.", "Yesh li be-a-YA im ha-CHASH-mal.",
             "I have a problem with the electricity. (landlord's cue to panic)"),
            ("מתי אפשר לתקן?", "Ma-TAI ef-shar le-ta-KEN?",
             "When can it be fixed? (the follow-up that actually gets results)"),
            ("יש לי תור ב-9.", "Yesh li TOR be-TEI-sha.",
             "I have an appointment at 9. (skips the line, trust me)"),
            ("צריך לשלם ארנונה.", "Tzar-ICH li-sh-LEM ar-NO-na.",
             "Need to pay municipal tax. (say it confidently, they'll respect that)"),
            ("אפשר לקבל קבלה?", "Ef-SHAR le-ka-BEL ka-ba-LA?",
             "Can I get a receipt? (essential for any Israeli transaction)"),
            ("הלינק לא עובד.", "Ha-LINK lo o-VED.",
             "The link doesn't work. (universal Israeli tech complaint)"),
            ("יש טופס למלא?", "Yesh TOH-fes le-ma-LE?",
             "Is there a form to fill? (shows you know the drill)"),
            ("אני חדש פה.", "A-NI cha-DASH po.",
             "I'm new here. (magic phrase — unlocks extra patience from any clerk)"),
            ("תודה רבה, עזרת לי מאוד.", "To-DA ra-BA, a-ZAR-ta li me-OD.",
             "Thank you so much, you helped me a lot. (ends any interaction on a high note)"),
        ],
    },
    {
        "n": "02",
        "icon": "☕",
        "title": "Cafes & Restaurants",
        "subtitle": "Order, sip, and pay like a Tel Aviv regular.",
        "color": CAT_BROWN,
        "phrases": [
            ("קפה הפוך, בבקשה.", "Ka-FE ha-FUCH, be-va-ka-SHA.",
             "Upside-down coffee (Israeli latte). The national drink. Order this, belong."),
            ("בלי סוכר.", "Be-LI su-KAR.",
             "Without sugar. (they'll add it anyway — say this twice)"),
            ("עם חלב בצד.", "Im cha-LAV ba-TZAD.",
             "Milk on the side. (sounds very Israeli, very intentional)"),
            ("מה הסגנון?", "Ma ha-sig-NON?",
             "What's the vibe? (asked before choosing a cafe — instant local cred)"),
            ("אפשר מים?", "Ef-SHAR ma-YIM?",
             "Can I have water? (free, always — but you have to ask)"),
            ("זה טעים מאוד!", "Ze ta-IM me-OD!",
             "This is delicious! (say it loud — the owner is always nearby)"),
            ("יש ויתר בלי גלוטן?", "Ve-i-TER be-LI glu-TEN?",
             "Is there a gluten-free option? (Tel Aviv is very gluten-aware)"),
            ("חשבון, בבקשה.", "Chesh-BON, be-va-ka-SHA.",
             "Check, please. (wave your hand once — no need to chase the waiter)"),
            ("ביחד או נפרד?", "Be-ya-CHAD o nif-RAD?",
             "Together or separate? (they'll ask — now you know what it means)"),
            ("לקחת.", "La-KA-chat.",
             "To-go. (one word, zero confusion)"),
        ],
    },
    {
        "n": "03",
        "icon": "\U0001F6D2",
        "title": "Markets & Money",
        "subtitle": "Bargain at the shuk and walk out with the win.",
        "color": CAT_GREEN,
        "phrases": [
            ("כמה זה עולה?", "Ka-MA ze O-le?",
             "How much does it cost? (ask before touching anything at Mahane Yehuda)"),
            ("זה יקר מדי.", "Ze ya-KAR mi-DAI.",
             "That's too expensive. (say it, pause, look away — watch the price drop)"),
            ("אפשר קצת יותר בזול?", "Ef-SHAR ktsat yo-TER be-ZOL?",
             "Can it be a bit cheaper? (the golden negotiation phrase)"),
            ("אקח שניים.", "E-KACH shna-YIM.",
             "I'll take two. (the magic number that always gets a discount)"),
            ("בכרטיס אשראי.", "Be-kar-TIS ash-RAI.",
             "By credit card. (they'll try to convince you cash is better — hold firm)"),
            ("קבלה, בבקשה.", "Ka-ba-LA, be-va-ka-SHA.",
             "Receipt, please. (non-negotiable, always ask)"),
            ("יש מבצע?", "Yesh miv-TZA?",
             "Is there a sale/deal? (the Israeli national question)"),
            ("אפשר לטעום?", "Ef-SHAR lit-OM?",
             "Can I taste? (at markets, always yes — just ask)"),
            ("זה טרי?", "Ze ta-RI?",
             "Is this fresh? (for anything at the market — they respect the question)"),
            ("סגרנו עסקה.", "Sa-GAR-nu is-KA.",
             "We've got a deal. (seals the negotiation — very Israeli energy)"),
        ],
    },
    {
        "n": "04",
        "icon": "\U0001F91D",
        "title": "Small Talk & Networking",
        "subtitle": "Slip into any conversation and sound like an insider.",
        "color": CAT_PURPLE,
        "phrases": [
            ("מה נשמע?", "Ma nish-MA?",
             "What's up? (the Israeli 'hello' — use it constantly)"),
            ("הכל בסדר?", "Ha-KOL be-SE-der?",
             "Is everything okay? (warm check-in, very common)"),
            ("אח שלי!", "ACH she-LI!",
             "My brother! (term of endearment — used between strangers, means you're in)"),
            ("סבבה גמור.", "Sa-BA-ba ga-MUR.",
             "Totally cool / all good. (highest level of Israeli approval)"),
            ("תכלס, מה המצב?", "Tach-LES, ma ha-ma-TZAV?",
             "Real talk — what's the situation? (skips small talk, gets to business)"),
            ("מאיפה אתה?", "Me-EI-fo a-TA?",
             "Where are you from? (they WILL ask within 30 seconds)"),
            ("אני לומד עברית.", "A-NI lo-MED iv-RIT.",
             "I'm learning Hebrew. (instant goodwill — they'll want to help you)"),
            ("יאללה, ביי!", "Ya-LA, bai!",
             "Yalla, bye! (the Israeli goodbye — iconic, use it)"),
            ("חבל על הזמן, זה מדהים.", "Cha-VAL al ha-ZMAN, ze mad-HIM.",
             "What a waste of time — it's amazing! (sounds negative, means amazing)"),
            ("נדבר.", "Ne-da-BER.",
             "We'll talk. (ends any conversation like a boss)"),
        ],
    },
    {
        "n": "05",
        "icon": "\U0001F6A8",
        "title": "Emergency & Logistics",
        "subtitle": "The phrases that save the day — and the delivery.",
        "color": CAT_RED,
        "phrases": [
            ("עזרה!", "ez-RA!",
             "Help! (short, loud, universal)"),
            ("אני לא מבין/ה.", "A-NI lo me-VIN / me-VI-na.",
             "I don't understand. (say it early, before you nod and regret)"),
            ("אפשר לדבר לאט?", "Ef-SHAR le-da-BER le-AT?",
             "Can you speak slowly? (they'll slow down — Israelis are impatient but kind)"),
            ("אני מחכה למשלוח.", "A-NI me-cha-KE le-mish-LO-ach.",
             "I'm waiting for a delivery. (Wolt driver on the phone — this is it)"),
            ("אני בכניסה.", "A-NI ba-kni-SA.",
             "I'm at the entrance. (second call from the driver — use this)"),
            ("תתקשר אליי.", "Tit-ka-SHER e-LAI.",
             "Call me. (simple, direct, works)"),
            ("אני אבוד/ה.", "A-NI a-VUD / a-vu-DA.",
             "I'm lost. (better to admit it than wander for 40 minutes)"),
            ("יש פה וויפי?", "Yesh po WI-FI?",
             "Is there WiFi here? (crosses all cultural barriers)"),
            ("דחוף.", "Da-CHUF.",
             "Urgent. (one word — opens doors and skips queues)"),
            ("תודה, הצלת אותי.", "To-DA, hi-TZAL-ta o-TI.",
             "Thank you, you saved me. (the best thing you can say to any Israeli who helped)"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------
def rrect(c, x, y, w, h, r, fill=None, stroke=None, sw=1.0):
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
    c.roundRect(x, y, w, h, r,
                fill=1 if fill is not None else 0,
                stroke=1 if stroke is not None else 0)


def draw_text_lines(c, lines, x, y, font, size, color, leading=None, align="left"):
    """Draw consecutive text lines; returns y after the last line."""
    leading = leading or size * 1.35
    c.setFillColor(color)
    c.setFont(font, size)
    for ln in lines:
        if align == "left":
            c.drawString(x, y, ln)
        elif align == "right":
            c.drawRightString(x, y, ln)
        else:
            c.drawCentredString(x, y, ln)
        y -= leading
    return y + leading


def wrap_text(c, text, font, size, max_w):
    """Greedy word-wrap; returns list of lines."""
    if not text:
        return []
    words = text.split()
    lines, cur = [], ""
    for w in words:
        candidate = (cur + " " + w).strip()
        if c.stringWidth(candidate, font, size) <= max_w:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# Page 1 — Cover
# ---------------------------------------------------------------------------
def draw_israeli_flag(c, cx, cy, w=92, h=62):
    x, y = cx - w / 2, cy - h / 2
    c.setFillColor(white)
    c.setStrokeColor(HexColor("#E2E6F0"))
    c.setLineWidth(0.6)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)

    flag_blue = HexColor("#0038B8")
    c.setFillColor(flag_blue)
    c.setStrokeColor(flag_blue)
    stripe_h = h * 0.12
    c.rect(x, y + h - stripe_h * 1.7, w, stripe_h, fill=1, stroke=0)
    c.rect(x, y + stripe_h * 0.7, w, stripe_h, fill=1, stroke=0)

    cx2, cy2 = x + w / 2, y + h / 2
    star_r = h * 0.22
    c.setStrokeColor(flag_blue)
    c.setLineWidth(2.0)
    pts_up = [(cx2 + star_r * math.cos(math.radians(a)),
               cy2 + star_r * math.sin(math.radians(a)))
              for a in (90, 210, 330)]
    pts_dn = [(cx2 + star_r * math.cos(math.radians(a)),
               cy2 + star_r * math.sin(math.radians(a)))
              for a in (270, 30, 150)]
    for pts in (pts_up, pts_dn):
        p = c.beginPath()
        p.moveTo(*pts[0])
        p.lineTo(*pts[1])
        p.lineTo(*pts[2])
        p.close()
        c.drawPath(p, stroke=1, fill=0)


def cover_texture(c):
    """Subtle diagonal grid + soft vignette glow at top."""
    c.saveState()
    c.setStrokeColor(Color(1, 1, 1, alpha=0.035))
    c.setLineWidth(0.5)
    step = 18
    for i in range(-int(PAGE_H), int(PAGE_W) + int(PAGE_H), step):
        c.line(i, 0, i + PAGE_H, PAGE_H)
    c.restoreState()
    c.saveState()
    for i, a in enumerate((0.06, 0.04, 0.025, 0.015)):
        c.setFillColor(Color(0.42, 0.58, 1.0, alpha=a))
        c.circle(PAGE_W / 2, PAGE_H - 30, 200 + i * 80, stroke=0, fill=1)
    c.restoreState()


def draw_cover(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    cover_texture(c)

    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 8, PAGE_W, 8, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, 8, fill=1, stroke=0)
    c.setFillColor(Color(1, 1, 1, alpha=0.3))
    c.rect(0, PAGE_H - 11, PAGE_W, 1, fill=1, stroke=0)
    c.rect(0, 11, PAGE_W, 1, fill=1, stroke=0)

    # Kicker label
    c.setFillColor(GOLD)
    c.setFont("BodyBold", 9)
    label = "HEBREW IN 40 DAYS  ·  FREE GUIDE"
    c.drawCentredString(PAGE_W / 2, PAGE_H - 70, label)
    # Underline
    lw = c.stringWidth(label, "BodyBold", 9)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(PAGE_W / 2 - lw / 2 - 14, PAGE_H - 76, PAGE_W / 2 - lw / 2 - 4, PAGE_H - 76)
    c.line(PAGE_W / 2 + lw / 2 + 4, PAGE_H - 76, PAGE_W / 2 + lw / 2 + 14, PAGE_H - 76)

    # Israeli flag
    draw_israeli_flag(c, PAGE_W / 2, PAGE_H - 140, w=88, h=60)

    # Main title
    c.setFillColor(white)
    c.setFont("BodyXBold", 40)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 230, "THE STREET HEBREW")
    c.setFillColor(GOLD)
    c.setFont("BodyXBold", 40)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 275, "SURVIVAL GUIDE")

    # Tiny gold rule under title
    c.setFillColor(GOLD)
    c.rect(PAGE_W / 2 - 32, PAGE_H - 295, 64, 2.5, fill=1, stroke=0)

    # Subtitle (two clean centred lines)
    c.setFillColor(Color(1, 1, 1, alpha=0.92))
    c.setFont("BodyMed", 13)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 322,
                        "50 essential phrases to navigate the Israeli street")
    c.drawCentredString(PAGE_W / 2, PAGE_H - 342,
                        "with 100% confidence.")
    c.setFillColor(GOLD)
    c.setFont("BodyMedIt", 11)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 365, "Zero grammar inside.")

    # "What's inside" mini preview strip
    pills = [
        ("PUBLIC SPACES", CAT_NAVY),
        ("CAFES", CAT_BROWN),
        ("MARKETS", CAT_GREEN),
        ("SMALL TALK", CAT_PURPLE),
        ("EMERGENCY", CAT_RED),
    ]
    c.setFont("BodyXBold", 8)
    pill_pad = 12
    pill_h = 20
    pill_widths = [c.stringWidth(p, "BodyXBold", 8) + pill_pad * 2 + 8 for p, _ in pills]
    gap = 7
    total = sum(pill_widths) + gap * (len(pills) - 1)
    px = (PAGE_W - total) / 2
    py = PAGE_H - 415
    for (label, col), pw in zip(pills, pill_widths):
        c.setFillColor(Color(1, 1, 1, alpha=0.08))
        c.setStrokeColor(Color(1, 1, 1, alpha=0.3))
        c.setLineWidth(0.6)
        c.roundRect(px, py, pw, pill_h, pill_h / 2, fill=1, stroke=1)
        # color dot on the left
        c.setFillColor(col if col != CAT_NAVY else GOLD)
        c.circle(px + 11, py + pill_h / 2, 2.6, stroke=0, fill=1)
        # label
        c.setFillColor(white)
        c.setFont("BodyXBold", 8)
        c.drawCentredString(px + pw / 2 + 4, py + 6.5, label)
        px += pw + gap

    # Quote card — elegant glass panel
    card_w = PAGE_W - 120
    card_x = (PAGE_W - card_w) / 2
    card_h = 170
    card_y = 200

    c.saveState()
    c.setFillColor(Color(1, 1, 1, alpha=0.06))
    c.setStrokeColor(Color(1, 1, 1, alpha=0.18))
    c.setLineWidth(0.8)
    c.roundRect(card_x, card_y, card_w, card_h, 14, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.roundRect(card_x, card_y, 4, card_h, 2, fill=1, stroke=0)
    c.restoreState()

    # Tiny "TESTIMONIAL" label above the quote
    c.setFillColor(GOLD)
    c.setFont("BodyXBold", 8.5)
    c.drawString(card_x + 28, card_y + card_h - 22, "FROM THE CREATOR")
    c.setFillColor(GOLD)
    c.rect(card_x + 28, card_y + card_h - 28, 24, 1.5, fill=1, stroke=0)

    # Quote text — wrapped manually so we control line breaks
    quote = ("I spent weeks in Ulpan learning how to write essays, but froze "
             "when the Wolt delivery guy called. I created this guide so you "
             "don't have to experience that 'street paralysis' — here is the "
             "exact script you need to sound like a local.")
    c.setFillColor(Color(1, 1, 1, alpha=0.94))
    lines = wrap_text(c, quote, "BodyMedIt", 11.5, card_w - 60)
    y = card_y + card_h - 50
    for ln in lines:
        c.setFont("BodyMedIt", 11.5)
        c.drawString(card_x + 28, y, ln)
        y -= 17

    # Attribution
    c.setFillColor(Color(1, 1, 1, alpha=0.65))
    c.setFont("BodyMedIt", 9.5)
    c.drawString(card_x + 28, card_y + 20, "— Built for new Israelis, by a frustrated Ulpan grad.")

    # Footer
    c.setFillColor(Color(1, 1, 1, alpha=0.55))
    c.setFont("BodyMed", 9)
    c.drawCentredString(PAGE_W / 2, 36, "hebrew-in-40-days.com  ·  Free Preview Edition")


# ---------------------------------------------------------------------------
# Content chrome
# ---------------------------------------------------------------------------
def content_chrome(c, page_num):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Top bar — slim, navy with gold accent
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 36, PAGE_W, 36, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 39, PAGE_W, 3, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("BodyBold", 9.5)
    c.drawString(36, PAGE_H - 24, "STREET HEBREW SURVIVAL GUIDE")
    c.setFillColor(GOLD)
    c.setFont("BodyMedIt", 9)
    c.drawRightString(PAGE_W - 36, PAGE_H - 24, "Hebrew in 40 Days")

    # Bottom — minimal
    c.setFillColor(BORDER)
    c.rect(36, 36, PAGE_W - 72, 0.6, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("BodyMed", 8.5)
    c.drawString(36, 22, "hebrew-in-40-days.com")
    c.setFillColor(INK)
    c.setFont("BodyBold", 8.5)
    c.drawRightString(PAGE_W - 36, 22, f"PAGE {page_num} OF 5")


# ---------------------------------------------------------------------------
# Category section
# ---------------------------------------------------------------------------
def draw_category(c, cat, y_top):
    margin = 36
    width = PAGE_W - margin * 2
    header_h = 60

    # Header card with rounded corners
    rrect(c, margin, y_top - header_h, width, header_h, 10, fill=cat["color"])

    # Subtle gold inner accent on header right edge
    c.saveState()
    c.setFillColor(GOLD)
    c.roundRect(margin + width - 5, y_top - header_h + 8, 3, header_h - 16, 1.5,
                fill=1, stroke=0)
    c.restoreState()

    # Number badge
    badge_x = margin + 20
    badge_cy = y_top - header_h / 2
    c.setFillColor(Color(1, 1, 1, alpha=0.14))
    c.circle(badge_x, badge_cy, 17, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("BodyXBold", 12)
    c.drawCentredString(badge_x, badge_cy - 4, cat["n"])

    # Icon
    c.setFillColor(Color(1, 1, 1, alpha=0.95))
    c.setFont("Symb", 18)
    c.drawString(badge_x + 28, badge_cy - 7, cat["icon"])

    # Title + subtitle
    c.setFillColor(white)
    c.setFont("BodyXBold", 14.5)
    c.drawString(badge_x + 55, y_top - 26, cat["title"].upper())
    c.setFillColor(Color(1, 1, 1, alpha=0.78))
    c.setFont("BodyMedIt", 9.5)
    c.drawString(badge_x + 55, y_top - 42, cat["subtitle"])

    # Table
    y = y_top - header_h - 8

    # Column geometry
    heb_x_right = margin + 168     # right edge for Hebrew (RTL anchor)
    phon_x = margin + 184
    phon_w = 130
    mean_x = phon_x + phon_w + 12
    mean_w = (margin + width) - mean_x - 14

    for i, (hb, phon, meaning) in enumerate(cat["phrases"]):
        # Wrap phonetic and meaning
        phon_lines = wrap_text(c, phon, "BodyMedIt", 9, phon_w)
        mean_lines = wrap_text(c, meaning, "Body", 8.8, mean_w)

        # Hebrew is single-line; we draw it as one chunk
        heb_lines = [heb(hb)]

        n_lines = max(len(phon_lines), len(mean_lines), 1)
        row_h = max(34, 11 + n_lines * 12 + 6)

        # Row background
        if i % 2 == 0:
            c.setFillColor(ROW_ALT)
            c.rect(margin, y - row_h, width, row_h, fill=1, stroke=0)

        # Left accent bar
        c.setFillColor(cat["color"])
        c.rect(margin, y - row_h, 2.5, row_h, fill=1, stroke=0)

        # Hebrew — right-aligned, larger, bold
        c.setFillColor(NAVY)
        c.setFont("HebBold", 16)
        text_y = y - row_h / 2 - 5
        c.drawRightString(heb_x_right, text_y, heb_lines[0])

        # Vertical micro-divider between Hebrew & phonetic
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.4)
        div_x = margin + 176
        c.line(div_x, y - row_h + 8, div_x, y - 8)

        # Phonetic
        c.setFillColor(ELECTRIC)
        c.setFont("BodyMedIt", 9)
        line_y = y - 14
        for ln in phon_lines:
            c.drawString(phon_x, line_y, ln)
            line_y -= 12

        # Meaning
        c.setFillColor(INK_SOFT)
        c.setFont("Body", 8.8)
        line_y = y - 14
        for ln in mean_lines:
            c.drawString(mean_x, line_y, ln)
            line_y -= 12

        # Bottom row hairline
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(margin + 6, y - row_h, margin + width - 6, y - row_h)

        y -= row_h

    return y - 10


# ---------------------------------------------------------------------------
# Page 5 — Pitch
# ---------------------------------------------------------------------------
def draw_pitch(c):
    c.setFillColor(LIGHT_GRAY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    content_chrome(c, 5)

    margin = 44
    width = PAGE_W - margin * 2

    # Top gold accent under header
    c.setFillColor(GOLD)
    c.rect(margin, PAGE_H - 60, 50, 3, fill=1, stroke=0)

    y = PAGE_H - 80

    # Hook
    c.setFillColor(MUTED)
    c.setFont("BodyBold", 9)
    c.drawString(margin, y, "STEP 02  ·  THE NEXT MOVE")
    y -= 26
    c.setFillColor(NAVY)
    c.setFont("BodyXBold", 26)
    c.drawString(margin, y, "Now you have the words.")
    y -= 32
    c.setFillColor(GOLD_DEEP)
    c.setFont("BodyXBold", 26)
    c.drawString(margin, y, "But do you have the reflex?")
    y -= 30

    # Body
    body = ("Knowing 50 phrases on paper is great. But the Israeli street moves fast. "
            "When someone speaks back to you at lightning speed, you need more than a "
            "cheat sheet. You need muscle memory.")
    c.setFillColor(INK_SOFT)
    body_lines = wrap_text(c, body, "Body", 11, width)
    for ln in body_lines:
        c.setFont("Body", 11)
        c.drawString(margin, y, ln)
        y -= 16
    y -= 14

    # Program name card
    prog_h = 70
    rrect(c, margin, y - prog_h, width, prog_h, 12,
          fill=NAVY)
    # Gold accent
    c.setFillColor(GOLD)
    c.rect(margin + 16, y - prog_h + 14, 3, prog_h - 28, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("BodyBold", 9)
    c.drawString(margin + 30, y - 22, "INTRODUCING")
    c.setFillColor(white)
    c.setFont("BodyXBold", 22)
    c.drawString(margin + 30, y - 48, "The 40-Day Hebrew Sprint")
    y -= prog_h + 18

    # Features grid — 3 cards side by side
    features = [
        ("\U0001F3A7", "Daily 2-min audio bites",
         "Straight to your phone. Listen on the bus, in line, while you stir coffee."),
        ("✕", "Zero grammar. 100% action.",
         "Built for the street, not the classroom. Memorize, repeat, deploy."),
        ("\U0001F4AC", "Real-world challenges",
         "Voice-message tasks that force you to think and speak in Hebrew."),
    ]
    feat_h = 96
    col_gap = 10
    col_w = (width - col_gap * 2) / 3
    for i, (icon, title, desc) in enumerate(features):
        cx = margin + i * (col_w + col_gap)
        rrect(c, cx, y - feat_h, col_w, feat_h, 10,
              fill=white, stroke=BORDER, sw=0.8)
        # Icon disc
        c.setFillColor(LIGHT_BLUE)
        c.circle(cx + 22, y - 22, 14, stroke=0, fill=1)
        c.setFillColor(ELECTRIC)
        c.setFont("Symb", 14)
        c.drawCentredString(cx + 22, y - 27, icon)
        # Title
        c.setFillColor(NAVY)
        c.setFont("BodyBold", 10.5)
        title_lines = wrap_text(c, title, "BodyBold", 10.5, col_w - 24)
        ty = y - 46
        for ln in title_lines:
            c.drawString(cx + 12, ty, ln)
            ty -= 13
        # Desc
        c.setFillColor(INK_SOFT)
        c.setFont("Body", 8.5)
        desc_lines = wrap_text(c, desc, "Body", 8.5, col_w - 24)
        dy = ty - 4
        for ln in desc_lines:
            c.drawString(cx + 12, dy, ln)
            dy -= 11

    y -= feat_h + 22

    # Gold divider
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(PAGE_W / 2 - 36, y, PAGE_W / 2 + 36, y)
    y -= 22

    # Beta offer card
    offer_h = 124
    rrect(c, margin, y - offer_h, width, offer_h, 12,
          fill=LIGHT_BLUE, stroke=ELECTRIC, sw=1.3)

    # Ribbon "BETA"
    rib_w = 90
    rib_x = margin + width - rib_w - 16
    rrect(c, rib_x, y - 22, rib_w, 18, 9, fill=ELECTRIC)
    c.setFillColor(white)
    c.setFont("BodyXBold", 9)
    c.drawCentredString(rib_x + rib_w / 2, y - 18, "BETA  ·  10 SPOTS")

    # Offer copy
    c.setFillColor(NAVY)
    c.setFont("BodyMed", 11)
    c.drawString(margin + 22, y - 30,
                 "Since you downloaded this guide, you can join our")
    c.drawString(margin + 22, y - 46,
                 "upcoming closed Beta cohort for just")

    # Price row
    big = "$39"
    small = "$149"
    c.setFillColor(ELECTRIC)
    c.setFont("BodyXBold", 38)
    c.drawString(margin + 22, y - 92, big)
    big_w = c.stringWidth(big, "BodyXBold", 38)

    sx = margin + 22 + big_w + 14
    c.setFillColor(MUTED)
    c.setFont("BodyBold", 16)
    c.drawString(sx, y - 80, small)
    sw_ = c.stringWidth(small, "BodyBold", 16)
    c.setStrokeColor(RED_STRIKE)
    c.setLineWidth(1.6)
    c.line(sx - 1, y - 74, sx + sw_ + 1, y - 74)

    # Savings pill
    pill_x = sx + sw_ + 14
    pill_w = 84
    rrect(c, pill_x, y - 86, pill_w, 18, 9, fill=GOLD)
    c.setFillColor(NAVY)
    c.setFont("BodyXBold", 9)
    c.drawCentredString(pill_x + pill_w / 2, y - 82, "SAVE $110")

    # Sub note
    c.setFillColor(RED_STRIKE)
    c.setFont("BodyMedIt", 9.5)
    c.drawString(margin + 22, y - 110, "Only 10 spots available — first come, first served.")

    y -= offer_h + 20

    # CTA button
    btn_h = 52
    btn_x = margin
    btn_w = width
    btn_y = y - btn_h
    whatsapp_url = "https://wa.me/972XXXXXXXXX"

    # Soft shadow
    c.saveState()
    c.setFillColor(Color(0.1, 0.45, 0.91, alpha=0.18))
    c.roundRect(btn_x + 2, btn_y - 4, btn_w, btn_h, 12, fill=1, stroke=0)
    c.restoreState()

    # Button gradient effect via two stacked rects
    rrect(c, btn_x, btn_y, btn_w, btn_h, 12, fill=ELECTRIC_DARK)
    rrect(c, btn_x, btn_y + 3, btn_w, btn_h - 3, 11, fill=ELECTRIC)

    c.setFillColor(white)
    c.setFont("BodyXBold", 15)
    c.drawCentredString(PAGE_W / 2, btn_y + btn_h / 2 - 5,
                        "Secure My Beta Spot & Start Speaking Now  →")

    c.linkURL(whatsapp_url,
              (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
              relative=0, thickness=0)

    y = btn_y - 22

    # Footer note
    c.setFillColor(MUTED)
    c.setFont("BodyMedIt", 9)
    c.drawCentredString(PAGE_W / 2, y,
                        "Questions? Reply directly — we respond within 24 hours.")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build(filename: str) -> None:
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle("The Street Hebrew Survival Guide")
    c.setAuthor("Hebrew in 40 Days")
    c.setSubject("50 essential street Hebrew phrases")

    draw_cover(c)
    c.showPage()

    layout = [
        [CATEGORIES[0], CATEGORIES[1]],
        [CATEGORIES[2], CATEGORIES[3]],
        [CATEGORIES[4]],
    ]
    for page_idx, cats in enumerate(layout, start=2):
        content_chrome(c, page_idx)
        y = PAGE_H - 60
        for cat in cats:
            y = draw_category(c, cat, y)
        c.showPage()

    draw_pitch(c)
    c.showPage()

    c.save()


if __name__ == "__main__":
    build("Street_Hebrew_Survival_Guide_v3_Elegant.pdf")
    print("Wrote Street_Hebrew_Survival_Guide_v3_Elegant.pdf")
