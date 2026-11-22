# Asiajoly — asiajoly.com

A bright, editorial storefront for a design-led pet brand: 30 static pages, 13 products across four
lines, bilingual (EN / 中文), no build step, no frameworks, no external requests.

**Live:** https://hhcnmtkrt8-lab.github.io/asiajoly/
**Repository:** https://github.com/hhcnmtkrt8-lab/asiajoly

---

## What's here

| | |
|---|---|
| Pages | **30** — home, shop, 13 product pages, about, technology, journal index + 3 articles, FAQ, contact, wholesale, 5 policy pages, 404 |
| Products | **13 SKUs** in four lines — Spring (fountains), Feast (feeders), Still (bowls & mats), Play (toys) — plus Care (filters, pumps) |
| Language | English server-rendered; Chinese switches instantly at runtime from `assets/copy.js` |
| Weight | ~70 KB HTML per page, 24 KB CSS, 26 KB JS, product art as SVG (no photography, no CDN, no web fonts) |
| Commerce | Client-side bag with localStorage, quantity, free-shipping threshold. No payment integration |
| Motion | Scroll reveals, marquee, hover states — all disabled under `prefers-reduced-motion` |

### Page map

```
index.html               home
shop.html                catalogue with category filter + sort
p-<id>.html              13 product pages (p-spring-01.html … p-pump.html)
about.html               brand story, values
technology.html          materials, noise, teardown, the four numbers
journal.html             article index
journal-1..3.html        "Why cats prefer running water", "The case against plastic bowls",
                         "A small-apartment setup"
faq.html                 12 questions
contact.html             support, wholesale, returns contacts
wholesale.html           trade application
shipping / returns / warranty / privacy / terms .html
404.html
```

## Deploying with Hostinger

The repository is the deployable artifact — every HTML file is committed and there is nothing to
build on the server.

1. Hostinger → **Website → Connect Git repository** (or upload the repo contents to `public_html`).
2. Branch: `main`. **Build command: none.** **Output directory: `/`** (the repo root is the site).
3. Point `asiajoly.com` at the Hostinger site and enable free SSL.
4. Canonical URLs in every page already point at `https://asiajoly.com/…`.

If you prefer GitHub Pages instead, it is already enabled on this repo.

## Local preview

```bash
python3 -m http.server 8000     # then open http://localhost:8000
```
Opening `index.html` directly from disk also works.

## Regenerating the site

All copy and art are generated. The pipeline is committed so the site can be rebuilt or extended.

```bash
python3 build_art.py        # 13 products × 3 views of SVG art → assets/products/
python3 build_products.py   # .build/products.json → assets/products.js
python3 merge_copy.py       # .build/{site,journal,legal}.json → assets/copy.js
python3 build_site.py       # renders all 30 pages into the repo root
```

Copy is written by Claude (`claude-opus-4-5`) against the briefs in `copy/`:

```bash
cat copy/brief.md copy/spec-site.md     | claude -p --model claude-opus-4-5 > .build/site.raw
cat copy/brief.md copy/spec-products.md | claude -p --model claude-opus-4-5 > .build/products.raw
cat copy/brief.md copy/spec-journal.md  | claude -p --model claude-opus-4-5 > .build/journal.raw
cat copy/brief.md copy/spec-legal.md    | claude -p --model claude-opus-4-5 > .build/legal.raw
# strip fences, save as .build/*.json, then run the three build steps above
```

`copy/brief.md` locks the brand register and — importantly — the hard rules: no invented
certifications, awards, press, review counts, no health claims, no fake urgency, honest toy
durability, real product facts only.

## Structure

```
asiajoly-site/
├── *.html                     30 generated pages (committed — this is the deployable site)
├── assets/
│   ├── styles.css             bright design system
│   ├── app.js                 i18n, catalogue rendering, filters, bag, PDP
│   ├── copy.js                GENERATED — all copy, EN + ZH
│   ├── products.js            GENERATED — the 13-product catalogue
│   └── products/*.svg         39 files: 13 products × 3 views
├── data/products.json         catalogue source
├── copy/                      brand brief + three copy specs
├── build_art.py               SVG product art
├── build_products.py          catalogue normaliser
├── merge_copy.py              copy validator + merger
├── build_site.py              page renderer
└── push_via_api.py            push helper for networks where git over 443 is blocked
```

## Design notes

- **Palette:** warm paper `#FDFBF7`, ink `#14201F`, teal `#12736B`, coral `#E8734A`; tinted panels
  (mint, sand, sky, blush) alternate to give the long page a rhythm without using photography.
- **Type:** system sans for UI, a serif for pull-quotes and review text, monospace for labels and
  prices. No webfonts, so first paint is immediate.
- **Product art** is drawn, not photographed: each line has its own silhouette (vessel, box, bowl,
  soft object) and every colour is derived from one hex per product, so adding a finish is a one-line
  change in `build_art.py`.
- **Chinese** is a parallel original, not a translation, with its own leading and letter-spacing.

## Before this goes live

This is a **preview build** and says so in the footer. Real gates:

1. **Trademark.** Search "Asiajoly" in USPTO / EUIPO / UKIPO (classes 21, 11) before printing.
2. **Specs.** 2.8 L, 24 dB, 30-second teardown, 316 stainless, 24 dB, 72-hour backup, capacities and
   prices are design targets. Re-measure on production units; each needs a test report behind it.
3. **Certification language.** The site says "designed to UL/CE requirements, testing in progress".
   Keep it that way until certificates exist; do not add CE/UL marks to the footer.
4. **Reviews.** The three "first homes" quotes are pre-launch test notes and are labelled as such.
5. **Policies.** Shipping / returns / warranty / privacy / terms are written in plain language and use
   `[registered address]` placeholders. Have a lawyer review before launch, especially EU/UK
   withdrawal rights and the 2-year guarantee.
6. **Commerce.** The bag is client-side only; prices live in `assets/products.js`. Wire to Shopify /
   Stripe / Snipcart and validate every price server-side.
7. **Compliance surface.** GPSR Responsible Person, WEEE, battery and packaging EPR registrations are
   per-country obligations — a footer disclaimer is not a substitute.

## License

Code and design: MIT. Copy and brand: © 2026 Asiajoly (placeholder brand).
