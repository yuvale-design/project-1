"""add_pdf_link.py — stamp / replace the CTA hyperlink on page 5.

Use this to point the "Secure My Beta Spot…" button at a new URL without
rebuilding the PDF from source. Detects an existing /Link annotation on
the bottom half of page 5 and updates its URI, or creates a new one over
the CTA button's measured rectangle if none is found.

Usage:
    pip install pikepdf
    python3 add_pdf_link.py \\
        --pdf Street_Hebrew_Survival_Guide_v5_Final.pdf \\
        --url https://thehebrewsprint.com/#pricing
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import pikepdf

# CTA button rectangle, in PDF user-space points (origin bottom-left).
# Matches the .cta block produced by build_guide.py on an A4 page
# (margin 44mm, height ~48pt, sitting just below the beta-offer card).
CTA_RECT_DEFAULT = (39.69, 225.55, 555.59, 272.85)  # x1, y1, x2, y2


def find_cta_annotation(page: pikepdf.Page) -> pikepdf.Object | None:
    """Return the existing /Link annotation that overlays the CTA button.

    The CTA sits in the bottom third of the page and spans almost the full
    width, so we pick the widest /Link annotation whose vertical centre is
    below 40% of the page height.
    """
    if "/Annots" not in page:
        return None

    page_height = float(page.MediaBox[3])
    best, best_width = None, 0.0
    for ann in page.Annots:
        if ann.get("/Subtype") != pikepdf.Name("/Link"):
            continue
        rect = ann.get("/Rect")
        if rect is None:
            continue
        x1, y1, x2, y2 = (float(v) for v in rect)
        width = abs(x2 - x1)
        cy = (y1 + y2) / 2
        if cy < page_height * 0.4 and width > best_width:
            best, best_width = ann, width
    return best


def make_uri_action(pdf: pikepdf.Pdf, url: str) -> pikepdf.Object:
    return pdf.make_indirect(pikepdf.Dictionary(
        S=pikepdf.Name("/URI"),
        URI=pikepdf.String(url),
        Type=pikepdf.Name("/Action"),
    ))


def make_link_annotation(pdf: pikepdf.Pdf, rect, url: str) -> pikepdf.Object:
    return pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name("/Annot"),
        Subtype=pikepdf.Name("/Link"),
        Rect=pikepdf.Array([pikepdf.Object.parse(str(v)) for v in rect]),
        Border=pikepdf.Array([0, 0, 0]),
        H=pikepdf.Name("/N"),
        A=make_uri_action(pdf, url),
    ))


def stamp_cta_link(in_pdf: Path, out_pdf: Path, url: str,
                   page_number: int = 5,
                   fallback_rect: tuple[float, float, float, float] = CTA_RECT_DEFAULT
                   ) -> tuple[bool, list[float]]:
    """Update or create the CTA link. Returns (updated_existing, rect)."""
    with pikepdf.open(in_pdf) as pdf:
        if page_number > len(pdf.pages):
            raise SystemExit(
                f"PDF has only {len(pdf.pages)} pages; cannot stamp page {page_number}."
            )
        page = pdf.pages[page_number - 1]
        existing = find_cta_annotation(page)
        if existing is not None:
            existing.A = make_uri_action(pdf, url)
            rect = [float(v) for v in existing.Rect]
            updated = True
        else:
            annot = make_link_annotation(pdf, fallback_rect, url)
            if "/Annots" in page:
                page.Annots.append(annot)
            else:
                page.Annots = pikepdf.Array([annot])
            rect = list(fallback_rect)
            updated = False
        pdf.save(out_pdf)
    return updated, rect


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pdf", required=True, type=Path,
                    help="path to the PDF file (will be updated in place by default)")
    ap.add_argument("--url", required=True,
                    help="target URL for the CTA button")
    ap.add_argument("--out", type=Path,
                    help="output path (default: overwrite --pdf via temp file)")
    ap.add_argument("--page", type=int, default=5,
                    help="page number that holds the CTA (1-indexed, default: 5)")
    args = ap.parse_args()

    src: Path = args.pdf
    if not src.exists():
        print(f"error: {src} not found", file=sys.stderr)
        return 1

    out: Path = args.out or src.with_suffix(".linked.pdf")
    updated, rect = stamp_cta_link(src, out, args.url, page_number=args.page)

    if args.out is None:
        shutil.move(out, src)
        out = src

    verb = "Updated existing link" if updated else "Added new link"
    print(f"{verb} on page {args.page} -> {args.url}")
    print(f"  rect: {[round(v, 2) for v in rect]}")
    print(f"  wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
