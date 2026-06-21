# The Hebrew Sprint — Project Files

Complete production-ready bundle for **thehebrewsprint.com**.

## What's in the box

```
.
├── index.html                                 ← Landing page (deployed)
├── Street_Hebrew_Survival_Guide_v5_Final.pdf  ← Free lead-magnet (50 phrases)
├── course-hsvr2024-x9k2m7.pdf                 ← Paid course (52 pages, 40 days)
├── words_clean.csv                            ← 400 source words for the course
├── build_guide.py                             ← Rebuilds the lead-magnet PDF
├── build_course.py                            ← Rebuilds the course PDF
├── add_pdf_link.py                            ← Re-stamps the CTA link on any PDF
├── fonts/                                     ← Heebo + Inter TTFs (used by PDFs)
├── CNAME                                      ← Custom domain config (GitHub Pages)
├── .github/workflows/pages.yml                ← Auto-deploy workflow
├── .gitignore
└── README.md (this file)
```

## Live URLs

| Asset | URL |
|---|---|
| Landing page | https://thehebrewsprint.com |
| Pricing anchor (CTA on the free PDF lands here) | https://thehebrewsprint.com/#pricing |
| Free lead-magnet PDF | https://thehebrewsprint.com/guide.pdf |
| Paid course PDF (post-payment download) | https://thehebrewsprint.com/course-hsvr2024-x9k2m7.pdf |

## How updates flow

1. Edit any file locally.
2. `git add -A && git commit -m "..." && git push origin main`
3. GitHub Actions runs the `.github/workflows/pages.yml` workflow.
4. About 30 seconds later, the changes are live on `thehebrewsprint.com`.

## To rebuild the PDFs (Python 3.11+)

```bash
pip install reportlab weasyprint pillow python-bidi pikepdf openpyxl
python3 build_guide.py        # → Street_Hebrew_Survival_Guide_v5_Final.pdf
python3 build_course.py       # → course-hsvr2024-x9k2m7.pdf
```

The build scripts cache Hebrew rasterized glyphs in `_heb_images/`
(gitignored). Delete that folder to force a clean rebuild.

## To change the CTA URL inside the lead-magnet PDF without rebuilding

```bash
python3 add_pdf_link.py \
  --pdf Street_Hebrew_Survival_Guide_v5_Final.pdf \
  --url 'https://thehebrewsprint.com/#pricing'
```

## PayPal

- Wired to live merchant Client ID in `index.html` line 11.
- `onApprove` renders a success screen with a real download button +
  the course URL + the PayPal email + the order ID, and stores the
  link in `localStorage` so the user can come back.

## Domain (Cloudflare DNS, GitHub Pages serving)

- A records on apex `thehebrewsprint.com` → `185.199.108.153 / .109 / .110 / .111` (DNS only, no proxy)
- CNAME `www` → `yuvale-design.github.io`
- Cloudflare SSL/TLS mode: **Full**
- GitHub Pages → Source: **GitHub Actions**
- Cache-busting `<meta http-equiv="Cache-Control">` tags in index.html so updates appear on first refresh.
