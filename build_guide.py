"""Generate the Street Hebrew Survival Guide PDF lead magnet."""
from __future__ import annotations

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from bidi import get_display

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
NAVY = HexColor("#0D1F3C")
ELECTRIC = HexColor("#1A73E8")
GOLD = HexColor("#F4A724")
LIGHT_GRAY = HexColor("#F7F8FA")
ROW_GRAY = HexColor("#F1F3F8")
MUTED_BLUE = HexColor("#7A8CB0")
CREAM = HexColor("#FFF7E0")
LIGHT_BLUE = HexColor("#E8F0FE")
WHITE = white

CAT_NAVY = NAVY
CAT_BROWN = HexColor("#7B3F00")
CAT_GREEN = HexColor("#1E8B4C")
CAT_PURPLE = HexColor("#6A1B9A")
CAT_RED = HexColor("#B71C1C")

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
pdfmetrics.registerFont(TTFont("Heb", "/usr/share/fonts/truetype/culmus/HadasimCLM-Bold.ttf"))
pdfmetrics.registerFont(TTFont("HebReg", "/usr/share/fonts/truetype/culmus/HadasimCLM-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("BodyBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("BodyIt", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Symb", "/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf"))

PAGE_W, PAGE_H = A4


def heb(text: str) -> str:
    """Apply bidi reordering so RTL Hebrew renders correctly in reportlab."""
    return get_display(text)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
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
# Drawing helpers
# ---------------------------------------------------------------------------
def draw_israeli_flag(c: canvas.Canvas, cx: float, cy: float, w: float = 70, h: float = 48) -> None:
    """Draw a simple Israeli flag centered at (cx, cy)."""
    x, y = cx - w / 2, cy - h / 2
    c.setFillColor(white)
    c.setStrokeColor(HexColor("#DDDDDD"))
    c.setLineWidth(0.7)
    c.rect(x, y, w, h, fill=1, stroke=1)

    blue = HexColor("#0038B8")
    c.setFillColor(blue)
    c.setStrokeColor(blue)
    stripe_h = h * 0.13
    c.rect(x, y + h - stripe_h * 1.6, w, stripe_h, fill=1, stroke=0)
    c.rect(x, y + stripe_h * 0.6, w, stripe_h, fill=1, stroke=0)

    cx2, cy2 = x + w / 2, y + h / 2
    star_r = h * 0.22
    c.setStrokeColor(blue)
    c.setFillColor(blue)
    c.setLineWidth(1.6)
    import math
    pts_up = [(cx2 + star_r * math.cos(math.radians(a)),
               cy2 + star_r * math.sin(math.radians(a)))
              for a in (90, 210, 330)]
    pts_dn = [(cx2 + star_r * math.cos(math.radians(a)),
               cy2 + star_r * math.sin(math.radians(a)))
              for a in (270, 30, 150)]
    p = c.beginPath()
    p.moveTo(*pts_up[0]); p.lineTo(*pts_up[1]); p.lineTo(*pts_up[2]); p.close()
    c.drawPath(p, stroke=1, fill=0)
    p = c.beginPath()
    p.moveTo(*pts_dn[0]); p.lineTo(*pts_dn[1]); p.lineTo(*pts_dn[2]); p.close()
    c.drawPath(p, stroke=1, fill=0)


def diagonal_texture(c: canvas.Canvas) -> None:
    """Subtle diagonal lines on navy cover."""
    c.saveState()
    c.setStrokeColor(Color(1, 1, 1, alpha=0.04))
    c.setLineWidth(0.6)
    step = 14
    for i in range(-int(PAGE_H), int(PAGE_W) + int(PAGE_H), step):
        c.line(i, 0, i + PAGE_H, PAGE_H)
    c.restoreState()


def gold_bars(c: canvas.Canvas, color=GOLD, h: float = 8) -> None:
    c.setFillColor(color)
    c.rect(0, PAGE_H - h, PAGE_W, h, fill=1, stroke=0)
    c.rect(0, 0, PAGE_W, h, fill=1, stroke=0)


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, w: float,
                 font: str, size: float, color, leading: float | None = None,
                 align: str = "left") -> float:
    """Draw text wrapping inside width w using a Paragraph; returns height used."""
    style = ParagraphStyle(
        "s", fontName=font, fontSize=size, leading=leading or size * 1.25,
        textColor=color, alignment={"left": 0, "center": 1, "right": 2}[align],
    )
    p = Paragraph(text, style)
    pw, ph = p.wrap(w, 1000)
    p.drawOn(c, x, y - ph)
    return ph


def rounded_box(c: canvas.Canvas, x, y, w, h, r, fill=None, stroke=None,
                stroke_w: float = 1) -> None:
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(stroke_w)
    c.roundRect(x, y, w, h, r,
                fill=1 if fill is not None else 0,
                stroke=1 if stroke is not None else 0)


# ---------------------------------------------------------------------------
# Page 1 — Cover
# ---------------------------------------------------------------------------
def draw_cover(c: canvas.Canvas) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    diagonal_texture(c)
    gold_bars(c, h=8)

    draw_israeli_flag(c, PAGE_W / 2, PAGE_H - 150, w=86, h=58)

    c.setFillColor(white)
    c.setFont("BodyBold", 34)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 240, "THE STREET HEBREW")
    c.setFillColor(GOLD)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 280, "SURVIVAL GUIDE")

    c.setFillColor(white)
    style_sub = ParagraphStyle(
        "sub", fontName="Body", fontSize=12.5, leading=18,
        textColor=Color(1, 1, 1, alpha=0.85), alignment=1,
    )
    sub = Paragraph(
        "50 Essential Phrases to Navigate the Israeli Street with "
        "<b>100% Confidence</b> &mdash; <i>Zero Grammar Inside.</i>",
        style_sub,
    )
    sub_w = PAGE_W - 110
    pw, ph = sub.wrap(sub_w, 200)
    sub.drawOn(c, (PAGE_W - sub_w) / 2, PAGE_H - 320 - ph)

    divider_y = PAGE_H - 360 - ph
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.line(PAGE_W / 2 - 60, divider_y, PAGE_W / 2 + 60, divider_y)

    quote_w = PAGE_W - 110
    quote_x = (PAGE_W - quote_w) / 2
    quote_y_top = divider_y - 30
    quote_text = (
        '&ldquo;I spent weeks in Ulpan learning how to write essays, but froze when '
        'the Wolt delivery guy called. I created this guide so you don&rsquo;t have to '
        'experience that &lsquo;street paralysis&rsquo;. Here is the exact script you need '
        'to sound like a local.&rdquo;'
    )
    style_q = ParagraphStyle(
        "q", fontName="BodyIt", fontSize=11.5, leading=18,
        textColor=Color(1, 1, 1, alpha=0.78), alignment=1,
    )
    p_q = Paragraph(quote_text, style_q)
    qw, qh = p_q.wrap(quote_w - 50, 400)

    box_x, box_y = quote_x, quote_y_top - qh - 30
    box_w, box_h = quote_w, qh + 30
    c.saveState()
    c.setFillColor(Color(1, 1, 1, alpha=0.07))
    c.setStrokeColor(Color(1, 1, 1, alpha=0.18))
    c.setLineWidth(0.6)
    c.roundRect(box_x, box_y, box_w, box_h, 10, fill=1, stroke=1)
    c.setFillColor(GOLD)
    c.rect(box_x, box_y, 3, box_h, fill=1, stroke=0)
    c.restoreState()
    p_q.drawOn(c, box_x + 25, box_y + 15)

    c.setFillColor(MUTED_BLUE)
    c.setFont("Body", 9.5)
    c.drawCentredString(PAGE_W / 2, 28, "Hebrew in 40 Days  ·  Free Preview Edition")


# ---------------------------------------------------------------------------
# Content page header / footer
# ---------------------------------------------------------------------------
def content_chrome(c: canvas.Canvas, page_num: int) -> None:
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 38, PAGE_W, 38, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 41, PAGE_W, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("BodyBold", 10.5)
    c.drawString(28, PAGE_H - 25, "STREET HEBREW SURVIVAL GUIDE")
    c.setFillColor(GOLD)
    c.setFont("BodyIt", 9.5)
    c.drawRightString(PAGE_W - 28, PAGE_H - 25, "Hebrew in 40 Days")

    c.setFillColor(LIGHT_GRAY)
    c.rect(0, 0, PAGE_W, 30, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 30, PAGE_W, 1.5, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Body", 9)
    c.drawString(28, 12, "hebrew-in-40-days.com")
    c.setFillColor(NAVY)
    c.setFont("BodyBold", 9)
    c.drawRightString(PAGE_W - 28, 12, f"Page {page_num} / 5")


# ---------------------------------------------------------------------------
# Category section
# ---------------------------------------------------------------------------
def draw_category(c: canvas.Canvas, cat: dict, y_top: float) -> float:
    margin = 28
    width = PAGE_W - margin * 2
    header_h = 54

    rounded_box(c, margin, y_top - header_h, width, header_h, 8, fill=cat["color"])
    c.setFillColor(GOLD)
    c.rect(margin, y_top - header_h, 4, header_h, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Symb", 22)
    icon_x = margin + 22
    icon_y = y_top - header_h / 2 - 4
    c.drawString(icon_x, icon_y - 4, cat["icon"])

    c.setFillColor(white)
    c.setFont("BodyBold", 14)
    c.drawString(icon_x + 38, y_top - 22, cat["title"])
    c.setFillColor(Color(1, 1, 1, alpha=0.85))
    c.setFont("BodyIt", 9.5)
    c.drawString(icon_x + 38, y_top - 38, cat["subtitle"])

    y = y_top - header_h - 4

    col_x = [margin, margin + 150, margin + 280]
    col_w = [150, 130, width - 280]
    row_h_min = 30

    for i, (hb, phon, meaning) in enumerate(cat["phrases"]):
        heb_style = ParagraphStyle(
            "h", fontName="Heb", fontSize=12.5, leading=15,
            textColor=NAVY, alignment=2,
        )
        phon_style = ParagraphStyle(
            "p", fontName="BodyIt", fontSize=8.8, leading=11.5,
            textColor=HexColor("#1A73E8"), alignment=0,
        )
        meaning_style = ParagraphStyle(
            "m", fontName="Body", fontSize=8.5, leading=11.5,
            textColor=HexColor("#222B45"), alignment=0,
        )
        p_h = Paragraph(heb(hb), heb_style)
        p_p = Paragraph(phon, phon_style)
        p_m = Paragraph(meaning, meaning_style)

        _, hh = p_h.wrap(col_w[0] - 14, 1000)
        _, ph2 = p_p.wrap(col_w[1] - 10, 1000)
        _, mh = p_m.wrap(col_w[2] - 14, 1000)
        row_h = max(row_h_min, hh + 8, ph2 + 8, mh + 8)

        bg = LIGHT_GRAY if i % 2 == 0 else white
        c.setFillColor(bg)
        c.rect(margin, y - row_h, width, row_h, fill=1, stroke=0)
        c.setFillColor(cat["color"])
        c.rect(margin, y - row_h, 3, row_h, fill=1, stroke=0)

        c.setStrokeColor(HexColor("#E3E6EE"))
        c.setLineWidth(0.4)
        c.line(col_x[1], y - row_h + 4, col_x[1], y - 4)
        c.line(col_x[2], y - row_h + 4, col_x[2], y - 4)

        p_h.drawOn(c, col_x[0] + 8, y - 6 - hh)
        p_p.drawOn(c, col_x[1] + 8, y - 6 - ph2)
        p_m.drawOn(c, col_x[2] + 8, y - 6 - mh)

        y -= row_h

    c.setStrokeColor(HexColor("#D5DAE6"))
    c.setLineWidth(0.5)
    c.rect(margin, y, width, y_top - header_h - y, fill=0, stroke=1)

    return y - 14


# ---------------------------------------------------------------------------
# Page 5 — Pitch
# ---------------------------------------------------------------------------
def draw_pitch(c: canvas.Canvas) -> None:
    c.setFillColor(LIGHT_GRAY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    content_chrome(c, 5)

    margin = 36
    width = PAGE_W - margin * 2

    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 50, PAGE_W, 5, fill=1, stroke=0)
    c.rect(0, 33, PAGE_W, 5, fill=1, stroke=0)

    y = PAGE_H - 90

    hook_h = 84
    rounded_box(c, margin, y - hook_h, width, hook_h, 10,
                fill=CREAM, stroke=GOLD, stroke_w=2)
    c.setFillColor(NAVY)
    c.setFont("BodyBold", 16)
    c.drawCentredString(PAGE_W / 2, y - 32, "Now you have the words.")
    c.setFillColor(HexColor("#B07B00"))
    c.setFont("BodyBold", 16)
    c.drawCentredString(PAGE_W / 2, y - 56, "But do you have the reflex?")
    y -= hook_h + 22

    body_style = ParagraphStyle(
        "body", fontName="Body", fontSize=11, leading=17,
        textColor=NAVY, alignment=1,
    )
    body = Paragraph(
        "Knowing 50 phrases on paper is great. But the Israeli street moves fast. "
        "When someone speaks back to you at lightning speed, you need more than a "
        "cheat sheet. <b>You need muscle memory.</b>",
        body_style,
    )
    bw, bh = body.wrap(width - 30, 400)
    body.drawOn(c, margin + 15, y - bh)
    y -= bh + 24

    c.setFillColor(NAVY)
    c.setFont("BodyBold", 22)
    c.drawCentredString(PAGE_W / 2, y - 24, "The 40-Day Hebrew Sprint")
    c.setFillColor(GOLD)
    c.rect(PAGE_W / 2 - 30, y - 34, 60, 2.5, fill=1, stroke=0)
    y -= 56

    features = [
        ("\U0001F3A7", "Daily 2-minute audio bites",
         "Straight to your phone. Listen on the bus, in line, while you stir coffee."),
        ("✕", "Zero grammar. 100% action.",
         "Built for the street, not the classroom. Memorize, repeat, deploy."),
        ("\U0001F4AC", "Real-world challenges",
         "Voice-message tasks that force you to speak and think in Hebrew."),
    ]
    feat_h = 50
    for icon, title, desc in features:
        rounded_box(c, margin, y - feat_h, width, feat_h, 8,
                    fill=white, stroke=HexColor("#E2E6F0"), stroke_w=0.8)
        c.setFillColor(ELECTRIC)
        c.roundRect(margin + 10, y - feat_h + 8, 34, 34, 6, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Symb", 18)
        c.drawCentredString(margin + 27, y - feat_h + 16, icon)
        c.setFillColor(NAVY)
        c.setFont("BodyBold", 11.5)
        c.drawString(margin + 56, y - 20, title)
        c.setFillColor(HexColor("#46506E"))
        c.setFont("Body", 9.5)
        c.drawString(margin + 56, y - 34, desc)
        y -= feat_h + 8

    y -= 4
    c.setFillColor(GOLD)
    c.rect(PAGE_W / 2 - 80, y, 160, 1.5, fill=1, stroke=0)
    y -= 16

    offer_h = 96
    rounded_box(c, margin, y - offer_h, width, offer_h, 10,
                fill=LIGHT_BLUE, stroke=ELECTRIC, stroke_w=1.5)
    c.setFillColor(NAVY)
    c.setFont("Body", 10.5)
    c.drawCentredString(PAGE_W / 2, y - 18,
                        "Since you downloaded this guide, you can join our upcoming")
    c.drawCentredString(PAGE_W / 2, y - 32,
                        "closed Beta cohort for just")

    price_y = y - 62
    big = "$39"
    small = "$149"
    big_w = c.stringWidth(big, "BodyBold", 26)
    small_w = c.stringWidth(small, "BodyBold", 13)
    gap = 12
    total_w = big_w + gap + small_w
    start_x = PAGE_W / 2 - total_w / 2

    c.setFillColor(ELECTRIC)
    c.setFont("BodyBold", 26)
    c.drawString(start_x, price_y, big)

    small_x = start_x + big_w + gap
    c.setFillColor(HexColor("#9099AD"))
    c.setFont("BodyBold", 13)
    c.drawString(small_x, price_y + 4, small)
    c.setStrokeColor(HexColor("#B71C1C"))
    c.setLineWidth(1.4)
    c.line(small_x - 1, price_y + 8, small_x + small_w + 1, price_y + 8)

    c.setFillColor(HexColor("#B71C1C"))
    c.setFont("BodyBold", 10)
    c.drawCentredString(PAGE_W / 2, y - 82, "Only 10 spots available.")
    y -= offer_h + 18

    btn_h = 48
    btn_x = margin
    btn_w = width
    btn_y = y - btn_h
    whatsapp_url = "https://wa.me/972XXXXXXXXX"
    c.saveState()
    c.setFillColor(ELECTRIC)
    c.roundRect(btn_x, btn_y, btn_w, btn_h, 10, fill=1, stroke=0)
    c.setFillColor(HexColor("#0B5BC7"))
    c.roundRect(btn_x, btn_y - 2, btn_w, 4, 2, fill=1, stroke=0)
    c.setFillColor(ELECTRIC)
    c.roundRect(btn_x, btn_y, btn_w, btn_h, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("BodyBold", 14)
    c.drawCentredString(PAGE_W / 2, btn_y + btn_h / 2 - 5,
                        "Secure My Beta Spot & Start Speaking Now →")
    c.restoreState()
    c.linkURL(whatsapp_url,
              (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
              relative=0, thickness=0)
    y = btn_y - 16

    c.setFillColor(HexColor("#5B6685"))
    c.setFont("BodyIt", 9.5)
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

    # Page 1 — Cover
    draw_cover(c)
    c.showPage()

    # Pages 2-4 — Categories (5 categories across 3 pages)
    layout = [
        [CATEGORIES[0], CATEGORIES[1]],   # Page 2
        [CATEGORIES[2], CATEGORIES[3]],   # Page 3
        [CATEGORIES[4]],                   # Page 4
    ]
    for page_idx, cats in enumerate(layout, start=2):
        content_chrome(c, page_idx)
        y = PAGE_H - 60
        for cat in cats:
            y = draw_category(c, cat, y)
        c.showPage()

    # Page 5 — Pitch
    draw_pitch(c)
    c.showPage()

    c.save()


if __name__ == "__main__":
    build("Street_Hebrew_Survival_Guide_v2.pdf")
    print("Wrote Street_Hebrew_Survival_Guide_v2.pdf")
