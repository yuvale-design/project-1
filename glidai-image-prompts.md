# Glidai Properties — JVC Investor Carousel — Photo Prompts

**Master style anchor** (paste at the end of every prompt):
*editorial luxury real estate photography, ultra-premium, cinematic, color palette of deep black, charcoal grey, dark emerald, luxury beige, metallic gold accents, shot on Hasselblad H6D 50mm, shallow depth of field, soft warm golden-hour light, no text, no logos, no watermark, --ar 4:5 --style raw --v 6*

---

## Slide 1 — Cover (aerial sunset)
Ultra-luxury aerial drone view of Jumeirah Village Circle (JVC) in Dubai at sunset, modern residential towers arranged around circular streets, lush green inner parks, distant Dubai Marina and Downtown skyline glowing in the warm haze, golden orange and amber sky, hint of deep emerald shadows, cinematic, museum-quality real estate cover, dramatic light, photorealistic.

## Slide 2 — Location
Luxury Dubai skyline at twilight from above, JVC area highlighted by a soft golden glow at center, faint metallic-gold road lines connecting JVC outward to Downtown, Marina, Palm Jumeirah, and the airports, deep charcoal grey sky with stars, ultra-clean cinematic composition, premium investment fund visual language.

## Slide 3 — Payment Plan
First-person view from a luxurious private apartment terrace in JVC at golden hour, polished travertine floor, slim brass railing, lounge chair softly out of focus, looking out at modern beige and white residential towers, warm sun flare, calm aspirational mood, palm trees swaying gently, premium editorial real estate photography, no people.

## Slide 4 — Leading Developers
Composition of three premium Dubai project lobbies and façades blended into one sophisticated key visual — cream marble floors, brass chandeliers, fluted wood paneling, geometric ceiling lights, dark emerald accents, sculptural modern furniture, warm golden light, no people, ultra high-end architectural photography.

## Slide 5 — Stable Demand
Lifestyle dusk scene of a JVC community plaza — stylish young professionals and a family at an outdoor café, modern villas and a low residential tower behind them, palm trees, soft string lights, warm amber tones with hints of dark emerald foliage, candid editorial photography, premium, aspirational, no logos.

## Slide 6 — Capital Growth
Cinematic dual-state composition: same luxury Dubai residential tower shown under construction on the left, then fully completed and illuminated at dusk on the right, smooth golden gradient connecting both, warm amber-gold sky, ultra realistic architectural visualization, no people, no text.

## Slide 7 — Income Paths
Interior of a luxurious modern penthouse in Dubai at twilight, floor-to-ceiling windows revealing illuminated Dubai skyline, low warm-beige sofa, gold accents, dark emerald velvet cushions, marble coffee table, soft ambient interior lighting blending with the city glow outside, editorial real estate photography, ultra premium, no people, no text.

## Slide 8 — CTA closer
Wide cinematic shot at sunset, silhouette of a confident investor on a private rooftop terrace looking out over the Dubai skyline, JVC luxury towers in the foreground, Marina and Downtown skyline glowing in warm orange and gold horizon, lens flare, aspirational, powerful, editorial photography.

---

## Logo / Brand Footer Spec

Position: centered, bottom of every slide, 100–120 px above the bottom edge.
Treatment:
- Small diamond crest containing the letter **G** in Cinzel, 1 px gold stroke.
- Wordmark **GLIDAI PROPERTIES** in Cinzel, all caps, 18 px, gold (#D4AF37), 0.55em letter spacing.
- Micro-sub **DUBAI · REAL ESTATE** in Heebo, 10 px, 60% warm white.
- Thin gold gradient rule (110 px, fading at both ends) above the crest.

These are already wired into the HTML — the `.glidai` block. Swap the crest letter `G` for an SVG of your real Glidai mark when ready.

---

## Export workflow

1. Open `glidai-carousel.html` in Chrome at 100% zoom.
2. Capture each `.slide` (1080 × 1350) — DevTools → Capture node screenshot or print-to-PDF.
3. Replace the SVG silhouette backgrounds inside each `.photo` block with the AI-generated photographs above (as `background-image`); keep the `.vignette` overlay for legibility.
4. Export each slide as JPG, sRGB, quality 90+.
5. Upload in order 01 → 08.
