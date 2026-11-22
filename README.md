# RILL — Water, considered.

A high-end, editorial DTC storefront for a pet-hydration brand, built as static HTML/CSS/JS with
no build step, no frameworks and no external requests. Bilingual (EN / 中文), with a working bag,
finish switcher, subscription entry point and a product page.

**Live:** https://hhcnmtkrt8-lab.github.io/rill-pet-site/

---

## What this is

A production-shaped front end for the brand strategy in
[`pet-ecommerce-research`](../pet-ecommerce-research): a narrow, premium hard-goods catalogue
(one fountain, one connected fountain, one bowl, consumables) sold direct-first, positioned against
the $30 plastic fountain rather than competing with it.

The design intent is "equipment, not gadget": near-black stages, ivory paper sections, one glacial
accent, tight display type, and product art drawn as SVG so it stays sharp at any size and costs
nothing to load.

| | |
|---|---|
| Pages | `index.html` (home), `product.html` (RILL 01 PDP) |
| Weight | ~25 KB HTML, ~22 KB CSS, ~18 KB JS, ~8 KB SVG art — no images, no fonts, no CDN |
| JavaScript | vanilla, ~380 lines, no dependencies |
| Language | EN / 中文 toggle, persisted in `localStorage` |
| Bag | drawer, quantity, subtotal, free-shipping threshold, `localStorage` persistence |
| Motion | scroll reveals, counters, marquee, parallax hero, canvas caustics; all disabled under `prefers-reduced-motion` |

## Run it

```bash
open index.html          # macOS
python3 -m http.server   # or serve the folder at http://localhost:8000
```

No installation step. Everything works from `file://` except that a local server is required if you
later add fetch-based features.

## Structure

```
rill-pet-site/
├── index.html              home
├── product.html            product detail page
├── assets/
│   ├── styles.css          design system + layout
│   ├── app.js              i18n, rendering, bag, motion
│   ├── copy.js             GENERATED — all site copy, EN + ZH
│   ├── fountain-steel.svg  product art (also graphite, sand, pro)
│   ├── bowl-sand.svg
│   └── filter.svg
├── copy/
│   ├── brief.md            brand + copy brief given to the model
│   ├── spec-home.md        JSON schema for the homepage copy
│   └── spec-pdp.md         JSON schema for the product page copy
├── build_art.py            regenerates the SVG product art
├── merge_copy.py           validates + merges generated copy into assets/copy.js
└── .build/                 raw model output (git-ignored)
```

## How the copy was produced

Every word of on-site copy was written by Claude (`claude-opus-4-5`, via the local Claude Code CLI)
against `copy/brief.md`, which locks the brand register, the product facts and a set of hard rules —
no invented certifications, no invented press, no health claims, no fake review counts.

The model returns strict JSON; `merge_copy.py` validates the structure (array lengths, required keys),
fills any gap from the other language, and writes `assets/copy.js`. The renderer never shows a blank
headline because a key was missing.

To regenerate:

```bash
python3 - <<'EOF'
# same pipeline used to build this repo
EOF
# or simply re-run after editing copy specs:
cat copy/brief.md copy/spec-home.md | claude -p --model claude-opus-4-5 > .build/home.raw
cat copy/brief.md copy/spec-pdp.md  | claude -p --model claude-opus-4-5 > .build/pdp.raw
# parse raw -> .build/*.json, then:
python3 merge_copy.py
python3 build_art.py
```

## Before this goes live

This is a **preview build**. It is honest about that in the footer, but these are the real gates:

1. **Brand clearance.** "RILL" is a working name. Search USPTO / EUIPO / UKIPO for conflicts in
   class 21 (household/containers) and 11 (water apparatus) before printing anything.
2. **Product claims.** 2.8 L, 24 dB, 30-second teardown, 316 stainless, 1.8 m cable, 30-day filter,
   18-month pump, $129/$169/$49/$19 are design targets. Every one must be re-measured on the
   production unit and backed by a test report before the copy ships.
3. **Certification language.** The site says "designed to UL/CE requirements, with testing in progress"
   and must keep saying that until the certificates exist. Do not add CE/UL marks to the footer.
4. **Reviews.** The three "field notes" are pre-launch test-reader quotes and are labelled as such.
   Replace with verified purchase reviews (Judge.me / Okendo) before launch; do not invent counts.
5. **Legal pages.** Shipping, returns, warranty, privacy, terms and EU/UK consumer-rights pages are
   linked but not written. The EU 14-day withdrawal right and the 2-year legal guarantee need
   jurisdiction-specific wording.
6. **Commerce.** The bag is client-side only. Wire it to Shopify Storefront / Stripe / Snipcart and
   add server-side price validation — never trust the price in `localStorage`.
7. **Compliance surface.** GPSR requires an EU Responsible Person named on the listing and the
   packaging; WEEE, battery and packaging EPR registrations are per-country. The footer disclaimer is
   not a substitute for those registrations.

## Notes on the code

- `assets/copy.js` is generated. Edit `copy/*.md` or the JSON in `.build/`, then re-run `merge_copy.py`.
- Product art is pure SVG with internal CSS animations, so it works inside `<img>` with no JS.
- `build_art.py` parameterises the finishes; changing a hex there regenerates every product view.
- The bag price lives in `PRODUCTS` in `app.js`. That is fine for a preview and unacceptable in
  production.
- Reduced-motion users get the final state immediately; no content depends on an animation completing.

## License

Design and code: MIT. Copy: © 2026 RILL (placeholder brand).
