"""Generate The 40-Day Hebrew Sprint — full course PDF.

Reads words from words_clean.csv (400 words, 10 per day) and embeds the
50 street-Hebrew sentences inline. Builds a 55-page A4 PDF with Heebo
rendered as PNG images so it's bullet-proof across all PDF viewers.

Output: course-hsvr2024-x9k2m7.pdf  (intentionally hard-to-guess so the
URL only reaches the customer through the Pages download button or
the post-payment email).
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from weasyprint import HTML, CSS

ROOT = Path(__file__).parent
FONT_DIR = ROOT / "fonts"
IMG_DIR = ROOT / "_heb_images"
IMG_DIR.mkdir(exist_ok=True)
OUT = ROOT / "course-hsvr2024-x9k2m7.pdf"

LP_URL = "https://thehebrewsprint.com"

HEB_FONT_BIG = ImageFont.truetype(str(FONT_DIR / "Heebo-Bold.ttf"), 96)
HEB_FONT_MED = ImageFont.truetype(str(FONT_DIR / "Heebo-Bold.ttf"), 72)
HEB_COLOR = (13, 31, 60, 255)


# ---------------------------------------------------------------------------
# Hebrew rendering
# ---------------------------------------------------------------------------
def heb_png(text: str, font=HEB_FONT_BIG) -> str:
    """Render Hebrew text to PNG and return file:// URI (cached on disk)."""
    if not text:
        return ""
    key = hashlib.sha1((text + str(font.size)).encode("utf-8")).hexdigest()[:16]
    out = IMG_DIR / f"heb_{key}.png"
    if not out.exists():
        bbox = font.getbbox(text)
        left, top, right, bottom = bbox
        w = right - left
        h = bottom - top
        pad_x, pad_y = 12, 10
        img = Image.new("RGBA", (w + pad_x * 2, h + pad_y * 2), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        d.text((pad_x - left, pad_y - top), text, font=font, fill=HEB_COLOR)
        img.save(out, "PNG", optimize=True)
    return out.resolve().as_uri()


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def load_words() -> list[tuple[str, str, str]]:
    rows = []
    with open(ROOT / "words_clean.csv", encoding="utf-8") as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            rows.append((row[1], row[2], row[3]))  # hebrew, english, phonetic
    return rows


WORDS = load_words()
assert len(WORDS) == 400, f"expected 400 words, got {len(WORDS)}"

# 50 street sentences pulled from the lead-magnet PDF (logical-order Hebrew)
SENTENCES = [
    # Part 1 - Street & public space (days highlight: 3, 14)
    ("סליחה, איפה השירותים?", "Sli-cha, e-fo ha-shi-ru-tim?", "Excuse me, where is the restroom?"),
    ("איך מגיעים לים?", "Eich me-gi-im le-yam?", "How do I get to the beach?"),
    ("זה קרוב לתחנה?", "Ze ka-rov la-ta-cha-na?", "Is it close to the station?"),
    ("יש פה בנק באזור?", "Yesh po bank ba-e-zor?", "Is there a bank around here?"),
    ("אני צריך להגיע לרכבת.", "Ani tza-rich le-ha-gi-a la-ra-ke-vet.", "I need to get to the train."),
    ("מתי מגיע האוטובוס?", "Ma-tai me-gi-a ha-o-to-bus?", "When does the bus arrive?"),
    ("כמה זמן עד לתל אביב?", "Ka-ma zman ad le-tel a-viv?", "How long until Tel Aviv?"),
    ("זה הולך ברגל לרוטשילד?", "Ze ho-lech be-re-gel le-rot-shild?", "Is it walking distance to Rothschild?"),
    ("סליחה, אתה יודע אם פתוח שם?", "Sli-cha, a-ta yo-de-a im pa-tu-ach sham?", "Excuse me, do you know if it's open there?"),
    ("לקחת ימינה או שמאלה ברמזור?", "La-ka-chat ya-mi-na o smo-la ba-ram-zor?", "Take a right or left at the light?"),
    # Part 2 - Cafés & Restaurants (days 4, 6, 7, 29)
    ("אפשר לקבל תפריט, בבקשה?", "Ef-shar le-ka-bel taf-rit, be-va-ka-sha?", "Can I get a menu, please?"),
    ("בשבילי הפוך גדול חזק, תודה.", "Bish-vi-li a-fuch ga-dol cha-zak, to-da.", "For me a large strong cappuccino, thanks."),
    ("אפשר לקבל סלט בלי בצל?", "Ef-shar le-ka-bel sa-lat bli ba-tzal?", "Can I get a salad without onions?"),
    ("זה מגיע עם צ'יפס או סלט?", "Ze me-gi-a im chips o sa-lat?", "Does it come with fries or salad?"),
    ("אפשר לשבת או שזה רק לקחת?", "Ef-shar la-she-vet o she-ze rak la-ka-chat?", "Can we sit, or is it take-away only?"),
    ("מה אתה ממליץ מהמנות הראשונות?", "Ma a-ta mam-litz me-ha-ma-not ha-ri-sho-not?", "What do you recommend from the appetizers?"),
    ("אפשר לקבל חשבון, כשיוצא לך?", "Ef-shar le-ka-bel chesh-bon, kshe-yo-tze le-cha?", "Can I get the bill when you get a chance?"),
    ("אפשר לשלם באשראי?", "Ef-shar le-sha-lem be-ash-ra-i?", "Can I pay with credit card?"),
    ("אנחנו חולקים את הקינוח הזה.", "An-ach-nu chol-kim et ha-ki-nu-ach ha-ze.", "We are sharing this dessert."),
    ("תעשה לי אמריקנו קר גדול.", "Ta-a-se li a-me-ri-ka-no kar ga-dol.", "Make me a large iced Americano."),
    # Part 3 - Shopping & money (days 5, 18)
    ("כמה זה עולה בסך הכל?", "Ka-ma ze o-le be-sach ha-kol?", "How much does this cost in total?"),
    ("יש על זה מבצע היום?", "Yesh al ze miv-tza ha-yom?", "Is there a sale on this today?"),
    ("זה יקר מדי, אתה יכול לעשות הנחה?", "Ze ya-kar mi-day, a-ta ya-chol la-a-sot han-acha?", "It's too expensive, can you give a discount?"),
    ("יש לכם את זה במידה יותר גדולה?", "Yesh la-chem et ze be-mi-da yo-ter g-do-la?", "Do you have this in a larger size?"),
    ("אני רק מסתכל, תודה רבה.", "Ani rak mi-sta-kel, to-da ra-ba.", "I'm just looking, thank you very much."),
    ("אתה מקבל מזומן או רק אפליקציה?", "A-ta me-ka-bel me-zu-man o rak ap-li-katz-ya?", "Do you take cash or app only?"),
    ("צריך קוד בשביל כרטיס האשראי?", "Tza-rich kod bish-vil kar-tis ha-ash-ra-i?", "Is a code required for the credit card?"),
    ("איפה הקופה של המזומן?", "E-fo ha-ku-pa shel ha-me-zu-man?", "Where is the cash register?"),
    ("אפשר שקית ניילון, בבקשה?", "Ef-shar sa-kit nay-lon, be-va-ka-sha?", "Can I have a plastic bag, please?"),
    ("שמע, זה מחיר מוגזם לגמרי.", "Shma, ze me-chir mug-zam le-gam-rey.", "Listen, this is a completely exaggerated price."),
    # Part 4 - Small talk & social (days 11, 26, 30)
    ("מה קורה אח שלי? מה הלו\"ז?", "Ma ko-re ach she-li? Ma ha-luz?", "What's up bro? What's the plan?"),
    ("נעים מאוד, אני דניאל, ואתה?", "Na-im me-od, ani dan-yel, ve-a-ta?", "Nice to meet you, I'm Daniel, and you?"),
    ("מאיפה אתה בעולם במקור?", "Me-e-fo a-ta ba-o-lam ba-ma-kor?", "Where are you originally from in the world?"),
    ("בוא נצא בערב לבירה בפאב.", "Bo ne-tze ba-e-rev le-bi-ra ba-pab.", "Let's go out for a beer at the pub tonight."),
    ("נשמע טוב, שלח לי מיקום בוואטסאפ.", "Nish-ma tov, shlach li mi-kum ba-whatsapp.", "Sounds good, send me a location on WhatsApp."),
    ("מה התוכניות שלך לסוף השבוע?", "Ma ha-toch-ni-yot shel-cha le-sof ha-sha-vu-a?", "What are your plans for the weekend?"),
    ("וואלה? לא ידעתי שאתה גר פה.", "Wa-lla? Lo ya-da-ti she-a-ta gar po.", "Wow, really? I didn't know you live here."),
    ("חובה לעשות את המפגש הזה שוב.", "Cho-va la-a-sot et ha-mif-gash ha-ze shuv.", "We must do this meetup again."),
    ("בכיף, אני תמיד זורם על האש.", "Be-kef, ani ta-mid zo-rem al ha-esh.", "With pleasure, I'm always down for a BBQ."),
    ("תגיד, יש לך המלצה על בר טוב?", "Ta-gid, yesh le-cha ham-la-tza al bar tov?", "Tell me, do you have a recommendation for a good bar?"),
    # Part 5 - Bureaucracy & housing (days 20-25)
    ("יש לי בעיה דחופה עם המזגן בדירה.", "Yesh li ba-a-ya d'chu-fa im ha-maz-gan ba-di-ra.", "I have an urgent problem with the AC in the apartment."),
    ("מי המנהל פה? אני צריך לעשות בירור.", "Mi ha-me-na-hel po? Ani tza-rich la-a-sot bi-rur.", "Who is the manager here? I need to make an inquiry."),
    ("אפשר לדבר לאט? אני לא מבין הכל.", "Ef-shar le-da-ber le-at? Ani lo me-vin ha-kol.", "Can you speak slowly? I don't understand everything."),
    ("איפה חותמים על חוזה השכירות?", "E-fo chot-mim al cho-ze ha-schi-rut?", "Where do we sign the lease contract?"),
    ("מתי זה יהיה מוכן? זה ממש דחוף לי.", "Ma-tai ze yee-hye mu-chan? Ze ma-mash da-chuf li.", "When will it be ready? It's really urgent for me."),
    ("הייתה פה טעות, לא הבנתי את המחיר של הארנונה.", "Ha-y-ta po ta-ut, lo he-van-ti et ha-me-chir shel ha-ar-no-na.", "There was a mistake, I didn't understand the municipal tax price."),
    ("אתה יכול לבדוק לי את חשבון החשמל?", "A-ta ya-chol liv-dok li et chesh-bon ha-chash-mal?", "Can you check the electricity bill for me?"),
    ("סגרנו על מחיר כולל ועד בית, נכון?", "Sa-gar-nu al me-chir ko-lel va-ad ba-yit, na-chon?", "We agreed on a price including the building fee, right?"),
    ("מי מטפל בתיקון של הנזילה בקיר?", "Mi me-ta-pel ba-ti-kun shel ha-ne-zi-la ba-kir?", "Who handles the repair of the leak in the wall?"),
    ("תודה על העזרה, אני באמת מעריך את זה.", "To-da al ha-ez-ra, ani be-e-met ma-a-rich et ze.", "Thank you for the help, I truly appreciate it."),
]
assert len(SENTENCES) == 50


# ---------------------------------------------------------------------------
# Day-by-day curriculum: theme + sentence indexes (1-based) + challenge
# ---------------------------------------------------------------------------
PHASES = {
    "Foundation": (1, 7),
    "Daily Life": (8, 15),
    "Practical Life": (16, 22),
    "Social Integration": (23, 30),
    "Advanced": (31, 40),
}


DAYS = [
    # (theme, sentence_indexes, challenge)
    ("First Words — Greetings & Politeness",  [], "Say 'Shalom' and 'Toda' to three Israelis today. Watch them smile."),
    ("Who You Are — Identity & Introductions", [32], "Introduce yourself in Hebrew to one person today: 'Shalom, korim li ___, naim meod.'"),
    ("Getting Around — Locations & Directions", [1, 10], "Ask a stranger for directions in Hebrew, even if you already know the way."),
    ("Café Basics — Order Your First Drink",   [11, 12], "Walk into a café and order coffee using only Hebrew. Hold your ground."),
    ("Money Talk — Prices & Numbers",          [21, 28], "Ask 'kama ze ole?' at three different places today."),
    ("Coffee Specifics — Customizing Your Order", [13, 14], "Order a coffee 'bli sukar, im chalav batzad.' Sound like a regular."),
    ("Eating Out — Food & Preferences",        [15, 16, 19], "Recommend a restaurant in Hebrew: 'Yesh po makom ta-im?'"),
    ("Sentence Glue — Connectors & Time",      [], "Build one sentence today using 'aval' (but) and 'ki' (because)."),
    ("Necessities — Need, Must, Should",       [5, 41], "Express a need: 'ani tzarich ___' three times today."),
    ("Israeli Slang Decoded",                  [31, 39], "Drop 'sababa' and 'yalla' into one real conversation today."),
    # Phase 2 - Daily Life
    ("Relationships — Friends & Family",       [38], "Ask someone 'yesh lecha mishpacha po?' and listen to their story."),
    ("When & How Long — Time Expressions",     [6, 7], "Schedule something in Hebrew: 'machar ba-erev?' (tomorrow evening?)"),
    ("Describing the World — Adjectives & Feelings", [], "Use 3 feelings today: ta-im, ya-fe, ayef. Out loud."),
    ("Public Transport — Buses, Trains & Airports", [2, 3, 4], "Ride a bus today using only Hebrew when asking for the stop."),
    ("Speaking Hebrew — Meta Language",        [43], "When stuck, say 'ef-shar le-da-ber le-at? Ani lomed iv-rit.'"),
    # Phase 3 - Practical Life
    ("At the Bank — Money & Accounts",         [27], "Walk into a bank and ask any question in Hebrew. Tellers love olim trying."),
    ("Post Office & Deliveries",               [], "Receive a package and say 'cha-vi-la bish-vi-li?' to the courier."),
    ("Supermarket Survival",                   [22, 26, 29], "Buy 5 items at a shuk and ask for one discount: 'efshar yoter bezol?'"),
    ("Pharmacy & Health",                      [], "Walk into a pharmacy and ask: 'yesh lachem ___?' (Tylenol/Acamol)."),
    ("Bureaucracy Basics — Forms & Signatures", [42], "Say 'mi ha-menahel po?' next time you face a stuck process."),
    ("Finding an Apartment",                   [44], "Ask one landlord in Hebrew: 'ka-ma sh-chi-rut?' (how much rent?)."),
    ("Utility Bills & Maintenance",            [46, 47, 48], "Open a bill — name 3 things in Hebrew (chashmal, mayim, arnona)."),
    # Phase 4 - Social Integration
    ("Moving In — Furniture & Logistics",      [], "Tell someone 'avarti dira' (I moved). Watch them ask follow-ups."),
    ("Signing Contracts",                      [44], "Read one Hebrew word on any contract today. Even 'chatima' counts."),
    ("When Things Break — Plumbers & Repairs", [40, 49], "Call a plumber and try: 'yesh li ne-zi-la, da-chuf.'"),
    ("Going Out & Parties",                    [34, 35], "Invite someone out in Hebrew: 'bo ne-tze ba-erev.'"),
    ("Hobbies & The Beach",                    [], "Tell an Israeli your hobby: 'ha-tach-viv she-li ___.'"),
    ("Talking About the Weather",              [], "Open a conversation today with 'eize me-zeg a-vir!' (what weather!)."),
    ("At the Restaurant — Service",            [17, 18, 20], "End a meal with: 'chesh-bon, be-va-ka-sha.' Then tip."),
    ("The Art of Israeli Conversation",        [30, 37], "Say 'wa-lla?' to a friend today. It works for ANY surprise."),
    # Phase 5 - Advanced
    ("Job Hunting & Work",                     [], "Tell someone what you do in Hebrew: 'ani o-ved be ___.'"),
    ("Office Life — Meetings & Email",         [45], "Send one WhatsApp in Hebrew today, even if it's just 'sababa.'"),
    ("Business Travel",                        [], "Book a hotel/taxi in Hebrew today. Even one phrase counts."),
    ("Career Growth & Networking",             [], "Ask a colleague: 'efshar le-va-kesh tza-va?' (can I ask a favor?)"),
    ("Workplace Culture",                      [], "Say 'ka-vod!' to honor someone's good work today."),
    ("Problems & Apologies",                   [50], "Apologize in Hebrew once today: 'sli-cha, ta-ut she-li.'"),
    ("Planning the Future",                    [36], "Ask someone: 'ma ha-toch-ni-yot shel-cha?' (what are your plans?)"),
    ("Sharing Opinions",                       [], "Say 'le-da-a-ti' (in my opinion) and follow with anything."),
    ("The Tools of Learning",                  [], "Tell yourself: 'a-ni lo-med iv-rit, ya-chol la-a-sot et ze.'"),
    ("Graduation — Putting It All Together",   [50], "Have a 3-minute Hebrew-only conversation today. You're ready."),
]
assert len(DAYS) == 40


# ---------------------------------------------------------------------------
# Fonts (re-use the existing webfonts)
# ---------------------------------------------------------------------------
def font_face(family, file, weight="normal", style="normal"):
    path = (FONT_DIR / file).resolve().as_uri()
    return (f"@font-face {{ font-family: '{family}'; src: url({path}); "
            f"font-weight: {weight}; font-style: {style}; }}")


FONTS_CSS = "\n".join([
    font_face("Heebo", "Heebo-Regular.ttf", "400"),
    font_face("Heebo", "Heebo-Bold.ttf", "700"),
    font_face("Heebo", "Heebo-Black.ttf", "900"),
    font_face("Inter", "Inter-Regular.ttf", "400"),
    font_face("Inter", "Inter-Italic.ttf", "400", "italic"),
    font_face("Inter", "Inter-Medium.ttf", "500"),
    font_face("Inter", "Inter-MediumItalic.ttf", "500", "italic"),
    font_face("Inter", "Inter-SemiBold.ttf", "600"),
    font_face("Inter", "Inter-Bold.ttf", "700"),
    font_face("Inter", "Inter-ExtraBold.ttf", "800"),
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
}

@page { size: A4; margin: 0; }

html, body {
  font-family: 'Inter', sans-serif;
  color: var(--ink);
  background: white;
  font-size: 10.5pt;
  line-height: 1.5;
}

.page {
  width: 210mm;
  height: 297mm;
  position: relative;
  overflow: hidden;
  page-break-after: always;
}
.page:last-child { page-break-after: auto; }

/* ─────────────── COVER ─────────────── */
.cover {
  background: linear-gradient(155deg, #0D1F3C 0%, #15294F 55%, #0D1F3C 100%);
  color: white;
  padding: 0;
}
.cover::before {
  content: '';
  position: absolute; inset: 0;
  background-image: repeating-linear-gradient(135deg, rgba(255,255,255,0.04) 0 1px, transparent 1px 28px);
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
.cover .bar-top, .cover .bar-bot {
  position: absolute; left: 0; right: 0; height: 8px;
  background: var(--gold);
}
.cover .bar-top { top: 0; }
.cover .bar-bot { bottom: 0; }

.cover-inner {
  position: relative; z-index: 2;
  padding: 28mm 22mm 24mm;
  height: 100%;
  display: flex; flex-direction: column;
}
.cover .kicker {
  text-align: center;
  font-weight: 700;
  font-size: 9pt;
  letter-spacing: 0.3em;
  color: var(--gold);
  margin-bottom: 14mm;
}
.cover h1 {
  text-align: center;
  font-weight: 800;
  font-size: 40pt;
  line-height: 1.05;
  letter-spacing: -0.02em;
  color: white;
  margin-top: 6mm;
}
.cover h1 .gold { color: var(--gold); display: block; margin-top: 2mm; }
.cover .title-rule {
  width: 80px; height: 3px; background: var(--gold);
  margin: 8mm auto 6mm; border-radius: 2px;
}
.cover .subtitle {
  text-align: center;
  font-weight: 500;
  font-size: 14pt;
  line-height: 1.55;
  color: rgba(255,255,255,0.92);
  margin-top: 4mm;
}
.cover .subtitle .gold-it {
  display: block; margin-top: 4mm;
  color: var(--gold); font-style: italic; font-size: 12pt; font-weight: 500;
}
.cover .badges {
  display: flex; justify-content: center; gap: 12px;
  margin-top: 16mm;
}
.cover .badge {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.28);
  padding: 8px 14px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 9pt;
  letter-spacing: 0.06em;
  color: white;
}
.cover .quote-card {
  margin-top: auto;
  margin-bottom: 16mm;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.18);
  border-left: 4px solid var(--gold);
  border-radius: 14px;
  padding: 22px 26px;
  color: rgba(255,255,255,0.92);
}
.cover .quote-label {
  font-weight: 800;
  font-size: 9pt;
  letter-spacing: 0.2em;
  color: var(--gold);
  padding-bottom: 4px;
  border-bottom: 1.5px solid var(--gold);
  display: inline-block;
  margin-bottom: 12px;
}
.cover .quote-text {
  font-style: italic;
  font-weight: 500;
  font-size: 12pt;
  line-height: 1.6;
}
.cover .footer {
  position: absolute; left: 0; right: 0; bottom: 14mm;
  text-align: center;
  font-size: 9pt;
  color: rgba(255,255,255,0.55);
}

/* ─────────────── WELCOME PAGE ─────────────── */
.welcome-page {
  background: white;
  padding: 22mm 22mm;
}
.welcome-page h1 {
  font-weight: 800;
  font-size: 28pt;
  color: var(--navy);
  letter-spacing: -0.01em;
  margin-bottom: 4mm;
}
.welcome-page h1 .gold { color: var(--gold-deep); display: block; }
.welcome-page .lede {
  font-size: 12pt;
  color: var(--ink-soft);
  margin: 10mm 0 8mm;
  line-height: 1.6;
}
.welcome-page h2 {
  font-weight: 700;
  font-size: 13pt;
  color: var(--navy);
  margin-top: 10mm;
  margin-bottom: 4mm;
}
.welcome-page p { color: var(--ink-soft); font-size: 10.5pt; line-height: 1.7; margin-bottom: 4mm; }
.welcome-page ul { margin: 4mm 0 4mm 6mm; }
.welcome-page li { font-size: 10.5pt; color: var(--ink-soft); margin-bottom: 3mm; line-height: 1.6; }
.welcome-page li strong { color: var(--navy); }

/* ─────────────── PHASE DIVIDER ─────────────── */
.phase {
  background: linear-gradient(155deg, #0D1F3C 0%, #1A2D52 100%);
  color: white;
  padding: 0;
}
.phase-inner {
  height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 0 32mm;
}
.phase-kicker {
  font-weight: 800;
  font-size: 11pt;
  letter-spacing: 0.3em;
  color: var(--gold);
  margin-bottom: 6mm;
}
.phase-rule {
  width: 70px; height: 3px; background: var(--gold);
  margin: 0 auto 6mm; border-radius: 2px;
}
.phase h1 {
  font-weight: 800;
  font-size: 48pt;
  letter-spacing: -0.02em;
  color: white;
  text-align: center;
  line-height: 1.1;
}
.phase .days-range {
  margin-top: 12mm;
  font-weight: 700;
  font-size: 11pt;
  letter-spacing: 0.15em;
  color: rgba(255,255,255,0.65);
}
.phase .preview {
  margin-top: 14mm;
  font-style: italic;
  color: rgba(255,255,255,0.75);
  text-align: center;
  font-size: 11pt;
  line-height: 1.6;
  max-width: 110mm;
}

/* ─────────────── DAY PAGE ─────────────── */
.day {
  background: white;
  padding: 0;
}
.day .top {
  position: absolute; top: 0; left: 0; right: 0;
  height: 12mm;
  background: var(--navy);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 12mm;
  border-bottom: 3px solid var(--gold);
}
.day .top .brand {
  color: white;
  font-weight: 700;
  font-size: 9pt;
  letter-spacing: 0.08em;
}
.day .top .phase-tag {
  color: var(--gold);
  font-weight: 700;
  font-size: 8.5pt;
  letter-spacing: 0.15em;
  font-style: italic;
}

.day .body {
  position: absolute;
  top: 14mm; bottom: 12mm; left: 12mm; right: 12mm;
  display: flex; flex-direction: column;
}

.day-header {
  margin-bottom: 4mm;
}
.day-num {
  display: inline-block;
  font-weight: 800;
  font-size: 10pt;
  letter-spacing: 0.2em;
  color: var(--gold-deep);
  margin-bottom: 1mm;
}
.day-title {
  font-weight: 800;
  font-size: 20pt;
  color: var(--navy);
  line-height: 1.15;
  letter-spacing: -0.01em;
}
.day-rule {
  width: 50px; height: 3px; background: var(--gold);
  margin: 3mm 0 4mm; border-radius: 1.5px;
}
.day-context {
  font-size: 9.8pt;
  color: var(--ink-soft);
  line-height: 1.55;
  margin-bottom: 5mm;
}

.section-label {
  display: flex; align-items: center; gap: 8px;
  font-weight: 800;
  font-size: 8.5pt;
  letter-spacing: 0.18em;
  color: var(--navy);
  margin-bottom: 3mm;
}
.section-label::before {
  content: '';
  width: 18px; height: 2px;
  background: var(--gold);
}

.vocab-table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 5mm;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
}
.vocab-table td {
  padding: 5px 8px;
  vertical-align: middle;
  border-bottom: 0.5px solid var(--border);
  font-size: 9pt;
}
.vocab-table tr:last-child td { border-bottom: none; }
.vocab-table tr:nth-child(odd) td { background: var(--row-alt); }
.vocab-table td.idx {
  width: 22px;
  font-weight: 700;
  font-size: 8pt;
  color: var(--muted);
  text-align: center;
}
.vocab-table td.heb {
  width: 30%;
  text-align: right;
  padding-right: 12px;
  border-right: 3px solid var(--navy);
}
.vocab-table td.heb img {
  height: 19px; width: auto; max-width: 100%;
  vertical-align: middle;
}
.vocab-table td.phon {
  width: 30%;
  font-style: italic;
  font-weight: 500;
  color: var(--electric);
  font-size: 8.5pt;
  border-left: 0.5px solid var(--border);
  padding-left: 10px;
}
.vocab-table td.eng {
  font-size: 8.8pt;
  color: var(--ink-soft);
  padding-left: 10px;
  border-left: 0.5px solid var(--border);
}

.sentence-box {
  background: var(--light-blue);
  border: 1.2px solid var(--electric);
  border-radius: 12px;
  padding: 8px 14px;
  margin-bottom: 5mm;
}
.sentence-box .label {
  font-weight: 800;
  font-size: 7.5pt;
  letter-spacing: 0.18em;
  color: var(--electric-dark);
  margin-bottom: 3px;
}
.sentence-line {
  display: flex; align-items: center; gap: 14px;
  padding: 3px 0;
}
.sentence-line .h img {
  height: 22px; width: auto;
  vertical-align: middle;
}
.sentence-line .meta {
  flex: 1;
}
.sentence-line .meta .phon {
  font-style: italic; font-weight: 500;
  color: var(--navy);
  font-size: 9pt;
}
.sentence-line .meta .eng {
  font-size: 8.5pt;
  color: var(--ink-soft);
}

.challenge-box {
  background: var(--cream);
  border: 1.4px solid var(--gold);
  border-radius: 12px;
  padding: 10px 14px;
  margin-top: auto;
}
.challenge-box .label {
  font-weight: 800;
  font-size: 8.5pt;
  letter-spacing: 0.18em;
  color: var(--gold-deep);
  margin-bottom: 4px;
}
.challenge-box .text {
  font-size: 10pt;
  color: var(--navy);
  line-height: 1.5;
  font-weight: 500;
}

.day .bottom {
  position: absolute; left: 0; right: 0; bottom: 0;
  height: 10mm;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 12mm;
  border-top: 1px solid var(--border);
  background: white;
}
.day .bottom .site {
  color: var(--muted);
  font-weight: 500;
  font-size: 8pt;
}
.day .bottom .prog {
  color: var(--ink);
  font-weight: 700;
  font-size: 8pt;
  letter-spacing: 0.06em;
}

/* ─────────────── GRADUATION + APPENDIX ─────────────── */
.grad {
  background: linear-gradient(155deg, #0D1F3C 0%, #15294F 100%);
  color: white;
  padding: 30mm 22mm;
}
.grad .kicker {
  text-align: center;
  font-weight: 800;
  font-size: 10pt;
  letter-spacing: 0.3em;
  color: var(--gold);
  margin-bottom: 6mm;
}
.grad h1 {
  text-align: center;
  font-weight: 800;
  font-size: 34pt;
  letter-spacing: -0.01em;
  color: white;
  line-height: 1.1;
}
.grad h1 .gold { color: var(--gold); display: block; margin-top: 2mm; }
.grad .rule {
  width: 80px; height: 3px; background: var(--gold);
  margin: 10mm auto; border-radius: 2px;
}
.grad p {
  text-align: center;
  font-size: 12pt;
  line-height: 1.65;
  color: rgba(255,255,255,0.85);
  margin: 0 auto 6mm;
  max-width: 120mm;
}
.grad ul {
  list-style: none;
  margin: 8mm auto;
  max-width: 120mm;
}
.grad ul li {
  padding: 6px 0 6px 26px;
  color: rgba(255,255,255,0.9);
  font-size: 11pt;
  position: relative;
  line-height: 1.55;
}
.grad ul li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--gold);
  font-weight: 800;
  font-size: 14pt;
}
.grad .signature {
  margin-top: 12mm;
  text-align: center;
  font-style: italic;
  color: var(--gold);
  font-size: 10pt;
}

/* ─────────────── CHEAT SHEET ─────────────── */
.cheat {
  background: white;
  padding: 0;
}
.cheat .top {
  position: absolute; top: 0; left: 0; right: 0;
  height: 12mm;
  background: var(--navy);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 12mm;
  border-bottom: 3px solid var(--gold);
}
.cheat .top .brand { color: white; font-weight: 700; font-size: 9pt; letter-spacing: 0.08em; }
.cheat .top .pub { color: var(--gold); font-weight: 700; font-size: 9pt; font-style: italic; }
.cheat .body {
  position: absolute;
  top: 16mm; bottom: 12mm; left: 12mm; right: 12mm;
}
.cheat h2 {
  font-weight: 800;
  font-size: 18pt;
  color: var(--navy);
  letter-spacing: -0.01em;
  margin-bottom: 1mm;
}
.cheat .cheat-sub {
  color: var(--ink-soft);
  font-size: 9.5pt;
  margin-bottom: 5mm;
  font-style: italic;
}
.cheat .cheat-cat {
  font-weight: 800;
  font-size: 10pt;
  color: white;
  background: var(--navy);
  border-radius: 6px;
  padding: 4px 10px;
  display: inline-block;
  margin: 4mm 0 2mm;
}
.cheat-table {
  border-collapse: collapse;
  width: 100%;
  font-size: 8.5pt;
  margin-bottom: 3mm;
}
.cheat-table td {
  padding: 3px 8px;
  vertical-align: middle;
  border-bottom: 0.5px solid var(--border);
}
.cheat-table tr:nth-child(odd) td { background: var(--row-alt); }
.cheat-table td.heb { width: 38%; text-align: right; padding-right: 10px; border-right: 2.5px solid var(--gold-deep); }
.cheat-table td.heb img { height: 15px; width: auto; vertical-align: middle; }
.cheat-table td.phon { width: 28%; font-style: italic; color: var(--electric); font-size: 8pt; }
.cheat-table td.eng { font-size: 8.2pt; color: var(--ink-soft); }
.cheat .bottom {
  position: absolute; left: 0; right: 0; bottom: 0;
  height: 10mm;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 12mm;
  border-top: 1px solid var(--border);
  background: white;
}
.cheat .bottom .site { color: var(--muted); font-size: 8pt; font-weight: 500; }
.cheat .bottom .prog { color: var(--ink); font-size: 8pt; font-weight: 700; letter-spacing: 0.06em; }
"""


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------
def get_phase(day_num: int) -> str:
    for name, (start, end) in PHASES.items():
        if start <= day_num <= end:
            return name
    return ""


def get_phase_index(day_num: int) -> int:
    for i, (name, (start, end)) in enumerate(PHASES.items(), 1):
        if start <= day_num <= end:
            return i
    return 0


def cover_html() -> str:
    return f"""
    <div class="page cover">
      <div class="bar-top"></div>
      <div class="bar-bot"></div>
      <div class="cover-inner">
        <div class="kicker">HEBREW IN 40 DAYS &middot; COMPLETE EDITION</div>

        <h1>The 40-Day<span class="gold">Hebrew Sprint</span></h1>
        <div class="title-rule"></div>
        <p class="subtitle">
          400 essential words. 50 street-ready sentences.<br/>
          One page a day, fifteen minutes a sitting.
          <span class="gold-it">Designed to make you sound like a local in six weeks.</span>
        </p>

        <div class="badges">
          <span class="badge">40 DAYS</span>
          <span class="badge">400 WORDS</span>
          <span class="badge">50 SENTENCES</span>
          <span class="badge">5 PHASES</span>
        </div>

        <div class="quote-card">
          <div class="quote-label">FROM THE CREATOR</div>
          <div class="quote-text">
            This is the program I wish I had when I moved to Tel Aviv. No Nikkud,
            no Binyanim, no academic detours &mdash; just the exact words and
            sentences Israelis actually use, organized so each day builds on the
            last. Commit to 15 minutes a day for the next 40 days. By Day 40,
            you'll hold real conversations.
          </div>
        </div>

        <div class="footer">thehebrewsprint.com &middot; Lifetime Access &middot; Founding Cohort Edition</div>
      </div>
    </div>
    """


def welcome_html() -> str:
    return """
    <div class="page welcome-page">
      <h1>Welcome to<span class="gold">The Hebrew Sprint.</span></h1>
      <p class="lede">
        You've just unlocked the complete 40-day program. By the time you turn
        the last page, you'll have an arsenal of 400 essential words and 50
        ready-to-use sentences &mdash; everything you need to navigate Israel
        as a real participant, not a tourist.
      </p>

      <h2>How to use this course</h2>
      <ul>
        <li><strong>One day, one page, fifteen minutes.</strong> No skipping. The
          power comes from compounding daily reps, not from binge-reading.</li>
        <li><strong>Read the vocabulary out loud.</strong> Pronunciation builds
          faster through speaking than through silent reading.</li>
        <li><strong>Do today's challenge.</strong> Each page ends with a tiny
          real-world action. That's where Hebrew turns from text on a page into
          a tool in your mouth.</li>
        <li><strong>Don't worry about grammar.</strong> Israelis don't talk in
          grammar tables &mdash; they talk in patterns. You'll absorb patterns by
          using the sentences, not by analyzing them.</li>
        <li><strong>Listen for the words you learned today, in the wild.</strong>
          Once you know a word, you'll start hearing it everywhere &mdash; on
          buses, in cafes, in WhatsApp voice notes. That's the magic.</li>
      </ul>

      <h2>The 5 phases</h2>
      <p>
        The 40 days are organized in 5 phases of 7-10 days each. Each phase
        opens with a divider page so you know where you are. Don't rush ahead.
        Foundation phrases get used hundreds of times a day &mdash; the time
        you spend mastering them pays back forever.
      </p>

      <h2>If you miss a day</h2>
      <p>
        You will miss a day. That's fine. Pick up where you left off &mdash;
        not by skipping ahead. The whole point is consistency, not perfection.
      </p>

      <h2>One more thing</h2>
      <p>
        Israelis are <em>extraordinarily</em> patient with anyone trying. Don't
        wait until you're "ready" to speak. Bad Hebrew said out loud beats
        perfect Hebrew kept in your head &mdash; every time.
      </p>

      <h2 style="margin-top:14mm;color:var(--gold-deep);">Yalla. Let's go.</h2>
    </div>
    """


PHASE_INTROS = {
    "Foundation": "Greetings, identity, locations, café, money &mdash; the absolute essentials. Use these every day, everywhere.",
    "Daily Life": "Israeli slang, family talk, time, transport. The Hebrew that fills the gaps between formal phrases.",
    "Practical Life": "Bank, post office, supermarket, pharmacy, forms. The grown-up tasks that prove you really live here.",
    "Social Integration": "Apartments, contracts, plumbers, parties. You're not visiting anymore &mdash; you're settling in.",
    "Advanced": "Work, business travel, opinions, future plans. The Hebrew that turns you from oleh to insider.",
}


def phase_html(name: str, idx: int, day_range: tuple[int, int]) -> str:
    intro = PHASE_INTROS[name]
    return f"""
    <div class="page phase">
      <div class="phase-inner">
        <div class="phase-kicker">PHASE {idx} OF 5</div>
        <div class="phase-rule"></div>
        <h1>{name}</h1>
        <div class="days-range">DAYS {day_range[0]} &mdash; {day_range[1]}</div>
        <p class="preview">{intro}</p>
      </div>
    </div>
    """


def day_html(day_num: int) -> str:
    theme, sentence_idxs, challenge = DAYS[day_num - 1]
    phase = get_phase(day_num)
    words = WORDS[(day_num - 1) * 10:day_num * 10]

    vocab_rows = ""
    for i, (heb, eng, phon) in enumerate(words, 1):
        img = heb_png(heb, HEB_FONT_BIG)
        vocab_rows += (
            f"<tr>"
            f"<td class='idx'>{i}</td>"
            f"<td class='heb'><img src='{img}'/></td>"
            f"<td class='phon'>{phon}</td>"
            f"<td class='eng'>{eng}</td>"
            f"</tr>"
        )

    sentence_html = ""
    if sentence_idxs:
        sentence_html = '<div class="section-label">SENTENCE OF THE DAY</div><div class="sentence-box">'
        for si in sentence_idxs[:2]:
            heb, phon, eng = SENTENCES[si - 1]
            img = heb_png(heb, HEB_FONT_MED)
            sentence_html += (
                f"<div class='sentence-line'>"
                f"<div class='h'><img src='{img}'/></div>"
                f"<div class='meta'>"
                f"<div class='phon'>{phon}</div>"
                f"<div class='eng'>{eng}</div>"
                f"</div>"
                f"</div>"
            )
        sentence_html += "</div>"

    return f"""
    <div class="page day">
      <div class="top">
        <div class="brand">THE 40-DAY HEBREW SPRINT</div>
        <div class="phase-tag">Phase {get_phase_index(day_num)}: {phase}</div>
      </div>

      <div class="body">
        <div class="day-header">
          <div class="day-num">DAY {day_num} OF 40</div>
          <h1 class="day-title">{theme}</h1>
          <div class="day-rule"></div>
        </div>

        <div class="section-label">TODAY'S 10 WORDS</div>
        <table class="vocab-table">{vocab_rows}</table>

        {sentence_html}

        <div class="challenge-box">
          <div class="label">TODAY'S CHALLENGE &middot; 5 MINUTES</div>
          <div class="text">{challenge}</div>
        </div>
      </div>

      <div class="bottom">
        <div class="site">thehebrewsprint.com</div>
        <div class="prog">DAY {day_num} / 40</div>
      </div>
    </div>
    """


def graduation_html() -> str:
    return """
    <div class="page grad">
      <div class="kicker">DAY 40 &middot; YOU MADE IT</div>
      <h1>Mazel tov.<span class="gold">You're not a tourist anymore.</span></h1>
      <div class="rule"></div>
      <p>
        Forty days ago you couldn't order a coffee. Now you can rent an
        apartment, argue with the cable company, charm your way through a
        first date, and split a bill at a Tel Aviv restaurant &mdash; all
        in Hebrew.
      </p>

      <ul>
        <li>You memorized 400 essential words across 40 themed days.</li>
        <li>You internalized 50 ready-to-use sentence patterns.</li>
        <li>You completed 40 real-world speaking challenges.</li>
        <li>You proved &mdash; mostly to yourself &mdash; that you could.</li>
      </ul>

      <p>
        Hebrew rewards consistency, not talent. The fact that you finished
        this puts you ahead of 95% of olim who quit by week three. Keep
        speaking. Keep listening. Israelis will fill in everything you
        haven't learned yet.
      </p>

      <div class="signature">&mdash; The Hebrew Sprint team. Bekef, achi.</div>
    </div>
    """


def cheat_sheet_html() -> str:
    """All 50 sentences on 2-3 pages, organized by category."""
    cats = [
        ("Street & Public Space", range(0, 10)),
        ("Cafés & Restaurants", range(10, 20)),
        ("Shopping, Markets, Money", range(20, 30)),
        ("Small Talk & Social Life", range(30, 40)),
        ("Bureaucracy & Housing", range(40, 50)),
    ]
    page_html = ""
    sentences_per_page = 20
    current_page_count = 0
    sentence_chunks = ""
    page_num = 1

    def open_page():
        return f"""
    <div class="page cheat">
      <div class="top">
        <div class="brand">THE 40-DAY HEBREW SPRINT</div>
        <div class="pub">50-Sentence Cheat Sheet</div>
      </div>
      <div class="body">
        <h2>The 50-Sentence Cheat Sheet</h2>
        <div class="cheat-sub">Every street-ready phrase from the program, organized by situation.</div>
"""

    def close_page(pn):
        return f"""
      </div>
      <div class="bottom">
        <div class="site">thehebrewsprint.com</div>
        <div class="prog">CHEAT SHEET &middot; PAGE {pn}</div>
      </div>
    </div>
"""

    out = open_page()
    on_page = 0
    for cat_name, idxs in cats:
        # If adding this category would overflow, start a new page first
        if on_page > 0 and on_page + len(list(idxs)) > sentences_per_page:
            out += close_page(page_num)
            page_num += 1
            out += open_page()
            on_page = 0
        out += f'<div class="cheat-cat">{cat_name}</div><table class="cheat-table">'
        for i in idxs:
            heb, phon, eng = SENTENCES[i]
            img = heb_png(heb, HEB_FONT_MED)
            out += (
                f"<tr>"
                f"<td class='heb'><img src='{img}'/></td>"
                f"<td class='phon'>{phon}</td>"
                f"<td class='eng'>{eng}</td>"
                f"</tr>"
            )
            on_page += 1
        out += "</table>"
    out += close_page(page_num)
    return out


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build() -> None:
    pages = [cover_html(), welcome_html()]

    # Phase dividers + day pages
    for phase_idx, (phase_name, (start, end)) in enumerate(PHASES.items(), 1):
        pages.append(phase_html(phase_name, phase_idx, (start, end)))
        for d in range(start, end + 1):
            pages.append(day_html(d))

    pages.append(graduation_html())
    pages.append(cheat_sheet_html())

    html = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"/><title>The 40-Day Hebrew Sprint</title></head>
<body>{''.join(pages)}</body>
</html>"""

    css = CSS(string=FONTS_CSS + "\n" + CSS_BODY)
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(OUT), stylesheets=[css])
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
