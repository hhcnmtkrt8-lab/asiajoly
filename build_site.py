#!/usr/bin/env python3
"""Build the Asiajoly site.

Reads the generated copy + catalogue, renders every page to static HTML with English
content server-side (so the site works without JS and is crawlable), and leaves
data-i18n hooks that app.js uses to switch to Chinese at runtime.

Run: python3 build_site.py
"""
import hashlib
import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
BUILD, DATA, ASSETS = HERE / ".build", HERE / "data", HERE / "assets"

DOMAIN = "https://asiajoly.com"
BRAND = "Asiajoly"


# ----------------------------------------------------------------- data
def load(name, fallback=None):
    for base in (BUILD, DATA):
        p = base / f"{name}.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    if fallback is None:
        raise SystemExit(f"missing data: {name}.json")
    return fallback


_SITE = load("site")
_JOURNAL = load("journal")
_LEGAL = load("legal")
_PRODUCTS = load("products")
_COMMERCE = load("commerce") if (BUILD / "commerce.json").exists() else {"en": {}, "zh": {}}

LANG = "en"
SITE = JOURNAL = LEGAL = COMMERCE = None
PRODUCTS = BY_ID = None


def set_lang(lang):
    """Point every renderer at one language tree. Called once per build pass."""
    global LANG, SITE, JOURNAL, LEGAL, COMMERCE, PRODUCTS, BY_ID
    LANG = lang
    SITE = _SITE[lang]
    JOURNAL = _JOURNAL[lang]
    LEGAL = _LEGAL[lang]
    COMMERCE = _COMMERCE.get(lang, {})
    PRODUCTS = _PRODUCTS[lang]
    BY_ID = {p["id"]: p for p in PRODUCTS}


set_lang("en")
IS_ZH = False
BASE = ""          # href prefix for the current pass ("" for /, "../" for /zh/)
CURRENT = "index.html"

# Content hash of the static assets: appended to every asset URL so a new deploy
# always busts the CDN / browser cache (Hostinger's CDN caches CSS for 7 days).
_asset_files = [HERE / "assets" / "styles.css", HERE / "assets" / "app.js",
                HERE / "assets" / "copy.js", HERE / "assets" / "products.js"]
_asset_files += sorted((HERE / "assets" / "products").glob("*.svg"))
_h = hashlib.md5()
for _f in _asset_files:
    if _f.exists():
        _h.update(_f.name.encode())
        _h.update(_f.read_bytes())
BUILD_ID = _h.hexdigest()[:10]

PHOTOS = {p["id"]: f"assets/products/{p['id']}.svg?v={BUILD_ID}" for p in PRODUCTS}

CARE = {
    "Fountains": ("Rinse the five parts weekly, or put them in the dishwasher. Swap the filter every "
                  "30 days and the pump when the flow noticeably slows — usually around 18 months."),
    "Feeders": ("Wipe the bowl insert daily and wash it weekly. Empty and dry the hopper every few "
                "weeks; the desiccant sachet should be replaced when it stops being crunchy."),
    "Bowls": ("Dishwasher-safe on the top rack. The silicone foot lifts off so nothing gets trapped "
              "underneath — rinse it once a week."),
    "Play": ("Machine washable at 30°C on a gentle cycle. Not indestructible: retire it once the seams "
             "open or the fabric thins."),
    "Care": ("Filters last about 30 days in normal use, pumps about 18 months. Both click in without "
             "tools and are meant to be bought again, not thrown away with the object."),
}

BOX = {
    "Fountains": ("Fountain body", "Reservoir", "Pump", "Braided cable, 1.8 m", "First filter", "Quick-start card"),
    "Feeders": ("Feeder body", "Hopper lid", "Stainless bowl insert", "Desiccant sachet", "Power adapter", "Quick-start card"),
    "Bowls": ("Bowl", "Silicone non-slip foot", "Care card", "", "", ""),
    "Play": ("Toy", "Care card", "", "", "", ""),
    "Care": ("Filter or pump", "Fitment guide", "", "", "", ""),
}


def jsonld(obj):
    return ('<script type="application/ld+json">' +
            json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>")


def org_jsonld():
    return jsonld({
        "@context": "https://schema.org", "@type": "Organization",
        "name": BRAND, "url": DOMAIN + "/",
        "logo": DOMAIN + "/assets/favicon.svg",
        "description": SITE["footer"]["tagline"],
        "sameAs": [],
    })


def product_jsonld(p):
    return jsonld({
        "@context": "https://schema.org", "@type": "Product",
        "name": p["name"], "description": p["desc"],
        "image": DOMAIN + "/" + PHOTOS[p["id"]],
        "brand": {"@type": "Brand", "name": BRAND},
        "sku": p["id"], "category": p["category"],
        "offers": {
            "@type": "Offer", "price": p["price"], "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": f"{DOMAIN}/p-{p['id']}.html",
        },
    })


def esc(s):
    return html.escape(str(s), quote=True)


def money(n):
    return f"${n:,.0f}"


# ----------------------------------------------------------------- chrome
def slug_of(page):
    return "home" if page == "index.html" else page[:-5]


def head(title, desc, canonical, extra=""):
    en_url = DOMAIN + "/" + canonical
    zh_url = DOMAIN + "/zh/" + canonical
    url = zh_url if IS_ZH else en_url
    og = f"{DOMAIN}/assets/og/{slug_of(canonical)}.png"
    html_lang = "zh-CN" if IS_ZH else "en"
    return f"""<!doctype html>
<html lang="{html_lang}" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="zh-Hans" href="{zh_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="aj-base" content="{BASE}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'zh_CN' if IS_ZH else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#fdfbf7">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2314201f'/%3E%3Ctext x='16' y='22' font-family='Helvetica' font-size='13' fill='%23fdfbf7' text-anchor='middle' letter-spacing='1'%3EA%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/styles.css?v={BUILD_ID}">{extra}
</head>
<body>"""


NAV = [
    ("shop.html", "Shop", "shop"),
    ("about.html", "About", "about"),
    ("technology.html", "Technology", "technology"),
    ("journal.html", "Journal", "journal"),
    ("faq.html", "FAQ", "faq"),
]


NAV_ZH = {"shop": "商店", "about": "关于", "technology": "技术", "journal": "札记", "faq": "常见问题"}


def header(active):
    links = "".join(
        f'<a href="{href}" data-i18n="nav.{key}"{" aria-current=\"page\"" if active == key else ""}>'
        f'{esc(NAV_ZH.get(key) if IS_ZH else SITE["nav"].get(key, label).title() if key != "faq" else "FAQ")}</a>'
        for href, label, key in NAV
    )
    return f"""
<div class="announce" data-i18n="common.freeShip">{esc(SITE['common']['freeShip'])} · {'30 天试用' if IS_ZH else '30-day trial'}</div>
<header class="header" id="header">
  <div class="header__in">
    <a class="brand" href="index.html">ASIA<em>JOLY</em></a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <div class="spacer"></div>
    <div class="tools">
      <a class="icon-btn" id="langBtn" href="{(BASE if IS_ZH else 'zh/')}{CURRENT}" hreflang="{'en' if IS_ZH else 'zh-Hans'}" aria-label="Switch language"><span id="langLabel">{'EN' if IS_ZH else '中'}</span></a>
      <button class="icon-btn" id="cartBtn" aria-label="Open bag"><span id="cartLabel">Cart</span>
        <span class="cart-count" id="cartCount">0</span></button>
      <button class="icon-btn menu-btn" id="menuBtn" aria-label="Menu">☰</button>
    </div>
  </div>
</header>
<div class="mnav" id="mnav">
  <div class="mnav__top"><span class="brand">ASIA<em>JOLY</em></span>
    <button class="icon-btn" id="mnavClose" aria-label="Close">✕</button></div>
  <a href="shop.html" data-i18n="nav.shop">Shop</a>
  <a href="about.html" data-i18n="nav.about">About</a>
  <a href="technology.html" data-i18n="nav.technology">Technology</a>
  <a href="journal.html" data-i18n="nav.journal">Journal</a>
  <a href="faq.html" data-i18n="nav.faq">FAQ</a>
  <a href="contact.html" data-i18n="contact.eyebrow">Contact</a>
</div>"""


def footer():
    cols = SITE["footer"]["cols"]
    col_html = ""
    hrefs = {
        "Shop": ["shop.html?line=spring", "shop.html?line=feast", "shop.html?line=still",
                 "shop.html?line=play", "shop.html?category=Care"],
        "Company": ["about.html", "technology.html", "journal.html", "wholesale.html", "contact.html"],
        "Help": ["shipping.html", "returns.html", "warranty.html", "faq.html", "technology.html"],
    }
    for c in cols:
        links = "".join(
            f'<li><a href="{hrefs.get(c["h"], ["#"] * 5)[i] if i < len(hrefs.get(c["h"], [])) else "#"}">{esc(l)}</a></li>'
            for i, l in enumerate(c["links"]))
        col_html += f'<div><h5>{esc(c["h"])}</h5><ul>{links}</ul></div>'
    return f"""
<footer class="footer">
  <div class="wrap">
    <div class="footer__top">
      <div>
        <div class="brand">ASIA<em>JOLY</em></div>
        <p class="footer__tagline" data-i18n="footer.tagline">{esc(SITE['footer']['tagline'])}</p>
        <a class="link-u" href="shop.html" data-i18n="common.shopAll">Shop all</a>
      </div>
      {col_html}
    </div>
    <div class="footer__bottom">
      <span data-i18n="footer.legal">{esc(SITE['footer']['legal'])}</span>
      <span class="grow"></span>
      <button class="cookie-link" data-cookie-settings>Cookie settings</button>
      <div class="pay"><span>VISA</span><span>MC</span><span>AMEX</span><span>APPLE PAY</span></div>
      <span>{esc(SITE['footer']['disclaimer'])}</span>
    </div>
  </div>
</footer>

<div class="overlay" id="overlay"></div>
<aside class="drawer" id="drawer" aria-label="Shopping bag" aria-hidden="true">
  <div class="drawer__head"><h3 data-i18n="cart.title">Your bag</h3>
    <button class="icon-btn" id="closeCart" aria-label="Close">✕</button></div>
  <div class="drawer__body" id="cartBody"></div>
  <div class="drawer__foot" id="cartFoot"></div>
</aside>
<div class="toast" id="toast"></div>
<script src="assets/config.js?v={BUILD_ID}"></script>
<script src="assets/copy.js?v={BUILD_ID}"></script>
<script src="assets/products.js?v={BUILD_ID}"></script>
<script src="assets/app.js?v={BUILD_ID}"></script>
</body>
</html>"""


def page(title, desc, canonical, body, active=""):
    global CURRENT
    CURRENT = canonical
    return head(title, desc, canonical) + header(active) + "<main>" + body + "</main>" + footer()


# ----------------------------------------------------------------- blocks
def page_ld(title, desc, canonical, body, active="", ld=""):
    global CURRENT
    CURRENT = canonical
    return head(title, desc, canonical, ld) + header(active) + "<main>" + body + "</main>" + footer()


def section_head(eyebrow, title, sub="", href="", label=""):
    link = f'<a class="link-u" href="{href}">{esc(label)} →</a>' if href else ""
    sub_html = f'<p class="lede" data-i18n="{sub}">{esc(_lookup(sub))}</p>' if sub else ""
    return f"""<div class="head-row">
  <div><p class="eyebrow" data-i18n="{eyebrow}">{esc(_lookup(eyebrow))}</p>
    <h2 class="h2" data-i18n="{title}" data-reveal>{esc(_lookup(title))}</h2></div>
  {sub_html}{link}
</div>"""


def _lookup(path):
    """Resolve a dot path inside the English copy (for server-side rendering)."""
    node = {"home": SITE["home"], "shop": SITE["shop"], "about": SITE["about"],
            "technology": SITE["technology"], "faq": SITE["faq"], "contact": SITE["contact"],
            "footer": SITE["footer"], "journalPage": JOURNAL["index"]}
    for part in str(path).split("."):
        if isinstance(node, dict):
            node = node.get(part, "")
        elif isinstance(node, list):
            try:
                node = node[int(part)]
            except (ValueError, IndexError):
                return ""
        else:
            return ""
    return node if isinstance(node, (str, int, float)) else ""


def product_card(p, reveal=0):
    colors = "".join(f'<span class="dot" style="background:{esc(c["hex"])}"></span>' for c in p.get("colors", []))
    badge = ""
    if p.get("badge"):
        cls = "card__badge--new" if p["badge"].lower() == "new" else ""
        badge = f'<span class="card__badge {cls}">{esc(p["badge"])}</span>'
    return f"""<article class="card" data-reveal style="--d:{reveal}ms" data-id="{p['id']}">
  <a class="card__media" href="p-{p['id']}.html">{badge}
    <img src="{PHOTOS[p['id']]}" alt="{esc(p['name'])}" loading="lazy" width="620" height="760">
    <span class="card__swap"><span class="btn btn--sm btn--light" data-i18n="common.view">View</span></span>
  </a>
  <div class="card__body">
    <div class="card__row"><a class="card__name" href="p-{p['id']}.html">{esc(p['name'])}</a>
      <span class="card__price">{money(p['price'])}</span></div>
    <p class="card__meta">{esc(p['tagline'])}</p>
    <div class="card__dots">{colors}</div>
  </div>
</article>"""


def accordion(label, inner, open_=False):
    return f"""<div class="acc__item{' is-open' if open_ else ''}">
  <button class="acc__q" aria-expanded="{'true' if open_ else 'false'}"><span>{esc(label)}</span><i>+</i></button>
  <div class="acc__a"><div>{inner}</div></div>
</div>"""


# ----------------------------------------------------------------- pages
def build_home():
    h = SITE["home"]
    title = " ".join(h["hero"]["title"])
    ticker = "".join(
        f'<span data-i18n="home.ticker.{i}">{esc(x)}</span>'
        for _pass in range(2)
        for i, x in enumerate(h["ticker"]))
    lines = "".join(f"""<a class="line-card" href="{l['href']}" data-reveal style="--d:{i*70}ms">
      <img src="{PHOTOS[['spring-01','feast-01','still-bowl','play-snuffle'][i]]}" alt="">
      <span class="k">{esc(l['kind'])}</span>
      <h3>{esc(l['name'])}</h3><p>{esc(l['text'])}</p>
      <span class="link-u">{esc(SITE['common']['view'])} →</span></a>""" for i, l in enumerate(h["lines"]["items"]))
    featured = [BY_ID["spring-01"], BY_ID["feast-01"], BY_ID["spring-02"], BY_ID["play-snuffle"]]
    cards = "".join(product_card(p, i * 80) for i, p in enumerate(featured))
    feat_ids = ",".join(p["id"] for p in featured)
    why = "".join(f"""<article data-reveal style="--d:{i*70}ms"><div class="k">{esc(w['k'])}</div>
      <h4>{esc(w['title'])}</h4><p>{esc(w['text'])}</p></article>""" for i, w in enumerate(h["why"]["items"]))
    arts = JOURNAL["articles"]
    jcards = "".join(f"""<a class="jcard" href="journal-{i+1}.html" data-reveal style="--d:{i*80}ms">
      <div class="jcard__media"><span class="jcard__tag">{esc(a['tag'])}</span>
        <img class="orn" src="assets/products/{['filter-3','still-bowl','still-mat'][i]}.svg" alt=""></div>
      <time>{esc(a['date'])} · {esc(a['read'])} min</time>
      <h3>{esc(a['title'])}</h3><p>{esc(a['excerpt'])}</p></a>""" for i, a in enumerate(arts[:3]))
    revs = "".join(f"""<figure class="review" data-reveal style="--d:{i*80}ms">
      <blockquote>{esc(r['text'])}</blockquote>
      <figcaption><b>{esc(r['author'])}</b><br>{esc(r['city'])}</figcaption></figure>"""
                   for i, r in enumerate(h["reviews"]["items"]))

    body = f"""
<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <p class="eyebrow" data-i18n="home.hero.eyebrow">{esc(h['hero']['eyebrow'])}</p>
      <h1 class="display" data-reveal><span data-i18n="home.hero.title.0">{esc(h['hero']['title'][0])}</span><em data-i18n="home.hero.title.1">{esc(h['hero']['title'][1])}</em></h1>
      <p class="hero__sub" data-i18n="home.hero.sub">{esc(h['hero']['sub'])}</p>
      <div class="hero__cta">
        <a class="btn" href="shop.html"><span data-i18n="home.hero.cta">{esc(h['hero']['cta'])}</span></a>
        <a class="btn btn--ghost" href="technology.html"><span data-i18n="home.hero.cta2">{esc(h['hero']['cta2'])}</span></a>
      </div>
      <p class="hero__note" data-i18n="home.hero.note">{esc(h['hero']['note'])}</p>
    </div>
    <div class="hero__stage" data-reveal>
      <span class="hero__badge"><span data-i18n="common.best">{esc(SITE['common'].get('best') or ('畅销' if IS_ZH else 'Best seller'))}</span> · Spring 01</span>
      <img src="assets/products/hero.svg" alt="Asiajoly Spring 01 fountain" width="620" height="760">
      <div class="hero__stamp"><span>FROM</span><b>$129</b><span>FREE SHIP</span></div>
    </div>
  </div>
</section>

<div class="ticker"><div class="ticker__track">{ticker}{ticker}</div></div>

<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow" data-i18n="home.intro.eyebrow">{esc(h['intro']['eyebrow'])}</p>
      <h2 class="h2" data-i18n="home.intro.title" data-reveal>{esc(h['intro']['title'])}</h2>
    </div>
    <div>
      <p class="lede" style="margin-bottom:18px" data-i18n="home.intro.p1">{esc(h['intro']['p1'])}</p>
      <p class="lede" style="margin-bottom:22px" data-i18n="home.intro.p2">{esc(h['intro']['p2'])}</p>
      <a class="link-u" href="about.html" data-i18n="home.intro.link">{esc(h['intro']['link'])} →</a>
    </div>
  </div>
</section>

<section class="section tint section--tight">
  <div class="wrap">
    {section_head('home.lines.eyebrow', 'home.lines.title', 'home.lines.sub', 'shop.html', SITE['common']['shopAll'])}
    <div class="lines">{lines}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head('home.featured.eyebrow', 'home.featured.title', 'home.featured.sub', 'shop.html', SITE['common']['shopAll'])}
    <div class="grid grid--4" data-grid="featured" data-pids="{feat_ids}">{cards}</div>
  </div>
</section>

<section class="section tint-mint">
  <div class="wrap">
    {section_head('home.why.eyebrow', 'home.why.title', 'home.why.sub')}
    <div class="usp">{why}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {section_head('home.journal.eyebrow', 'home.journal.title', 'home.journal.sub', 'journal.html', SITE['common']['readMore'])}
    <div class="journal-grid">{jcards}</div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    {section_head('home.reviews.eyebrow', 'home.reviews.title', 'home.reviews.sub')}
    <div class="reviews">{revs}</div>
    <p class="small" style="margin-top:18px" data-i18n="home.reviews.note">{esc(h['reviews']['note'])}</p>
  </div>
</section>

<section class="section newsband">
  <div class="wrap news">
    <div>
      <p class="eyebrow" data-i18n="home.newsletter.eyebrow">{esc(h['newsletter']['eyebrow'])}</p>
      <h2 class="h2" data-i18n="home.newsletter.title" data-reveal>{esc(h['newsletter']['title'])}</h2>
      <p class="lede" style="margin-top:12px" data-i18n="home.newsletter.sub">{esc(h['newsletter']['sub'])}</p>
    </div>
    <div>
      <form id="newsForm" novalidate>
        <input type="email" id="newsEmail" required placeholder="Email address" aria-label="Email address">
        <button type="submit" data-i18n="common.subscribe">Subscribe</button>
      </form>
      <p class="news__note" data-i18n="home.newsletter.note">{esc(h['newsletter']['note'])}</p>
    </div>
  </div>
</section>"""
    return page_ld(f"{BRAND} — {title}", h["hero"]["sub"], "index.html", body, "", org_jsonld())


def build_shop():
    s = SITE["shop"]
    cats = ["All"] + sorted({p["category"] for p in PRODUCTS})
    chips = "".join(
        f'<button class="chip{" is-on" if c == "All" else ""}" data-filter="{esc(c)}" '
        f'data-i18n="{"shop.all" if c == "All" else "cat." + c.lower()}">'
        f'{esc(SITE["shop"].get("all", "All") if c == "All" else c)}</button>' for c in cats)
    cards = "".join(product_card(p, i * 50) for i, p in enumerate(PRODUCTS))
    all_ids = ",".join(p["id"] for p in PRODUCTS)
    opts = "".join(f"<option>{esc(o)}</option>" for o in s["sortOptions"])
    body = f"""
<section class="shop-head"><div class="wrap">
  <p class="eyebrow" data-i18n="shop.eyebrow">{esc(s['eyebrow'])}</p>
  <h1 class="h1" data-i18n="shop.title">{esc(s['title'])}</h1>
  <p class="lede" style="margin-top:14px" data-i18n="shop.sub">{esc(s['sub'])}</p>
</div></section>
<section class="section section--tight"><div class="wrap">
  <div class="chips" id="chips">{chips}</div>
  <div class="toolbar">
    <span class="toolbar__count" id="count">{len(PRODUCTS)} products</span>
    <select class="select" id="sort" aria-label="Sort">{opts}</select>
  </div>
  <div class="grid grid--4" id="shopGrid" data-grid="all" data-pids="{all_ids}">{cards}</div>
  <p class="small" id="emptyNote" style="display:none;padding:40px 0">No products in this filter.</p>
</div></section>"""
    return page(f"Shop — {BRAND}", s["sub"], "shop.html", body, "shop")


def build_product(p):
    pid = p["id"]
    specs = "".join(f"<tr><td>{esc(r['k'])}</td><td>{esc(r['v'])}</td></tr>" for r in p["specs"])
    bullets = "".join(f"<li>{esc(b)}</li>" for b in p["bullets"])
    swatches = "".join(
        f'<button class="swatch{" is-on" if i == 0 else ""}" data-color="{i}" '
        f'style="background:{esc(c["hex"])}" title="{esc(c.get("name",""))}" aria-label="{esc(c.get("name",""))}"></button>'
        for i, c in enumerate(p.get("colors", [])))
    box = [b for b in BOX.get(p["category"], ()) if b]
    box_html = "<ul class='bullets'>" + "".join(f"<li>{esc(b)}</li>" for b in box) + "</ul>"
    related_ids = [x for x in BY_ID if x != pid and BY_ID[x]["category"] == p["category"]][:3]
    if len(related_ids) < 3:
        related_ids += [x for x in ("filter-3", "still-bowl", "still-mat") if x != pid and x not in related_ids][:3 - len(related_ids)]
    related = "".join(product_card(BY_ID[x], i * 70) for i, x in enumerate(related_ids[:3]))
    rel_ids = ",".join(related_ids[:3])
    badge = f'<span class="card__badge">{esc(p["badge"])}</span>' if p.get("badge") else ""

    body = f"""
<div class="wrap">
  <nav class="crumbs"><a href="index.html">Home</a><span>—</span><a href="shop.html">Shop</a>
    <span>—</span><span>{esc(p['category'])}</span><span>—</span><span>{esc(p['name'])}</span></nav>
  <div class="pdp">
    <div class="gallery">
      <div class="gallery__main">{badge}<img id="galleryImg" src="{PHOTOS[pid]}" alt="{esc(p['name'])}" width="620" height="760"></div>
      <div class="thumbs" id="thumbs">
        <button class="is-on" data-thumb="0"><img src="{PHOTOS[pid]}" alt=""></button>
        <button data-thumb="1"><img src="assets/products/{pid}-a.svg" alt=""></button>
        <button data-thumb="2"><img src="assets/products/{pid}-b.svg" alt=""></button>
        <button data-thumb="3"><img src="assets/products/{pid}.svg" alt=""></button>
      </div>
    </div>
    <div class="buy" data-pid="{pid}">
      <p class="eyebrow" data-i18n="pdp.eyebrow" style="margin-bottom:10px">{esc(p['line'])} · {esc(p['category'])}</p>
      <h1 class="pdp__title" id="pdpName">{esc(p['name'])}</h1>
      <p class="pdp__tag" id="pdpTag">{esc(p['tagline'])}</p>
      <div class="price-row"><span class="price" id="pdpPrice">{money(p['price'])}</span>
        {f'<span class="price-was">{money(p["compareAt"])}</span>' if p.get('compareAt') else ''}</div>
      <div class="reviewline"><span class="stars">★★★★★</span>
        <span data-i18n="pdp.inStock">{esc(SITE and 'In stock · ships in 2–4 days')}</span></div>
      <p class="pdp__desc" id="pdpDesc">{esc(p['desc'])}</p>
      <ul class="bullets" id="pdpBullets">{bullets}</ul>
      <div class="opt">
        <div class="opt__label"><span data-i18n="pdp.color">Color</span><span id="colorName">{esc((p.get('colors') or [{'name':''}])[0].get('name',''))}</span></div>
        <div class="swatches" id="swatches">{swatches}</div>
      </div>
      <div class="buyrow">
        <div class="qty"><button id="qMinus" aria-label="Decrease">−</button><span id="qVal">1</span>
          <button id="qPlus" aria-label="Increase">+</button></div>
        <button class="btn" id="addBtn" data-add="{pid}"><span data-i18n="common.addToBag">Add to bag</span></button>
      </div>
      <div class="meta"><span data-i18n="common.freeShip">{esc(SITE['common']['freeShip'])}</span>
        <span>30-day trial</span><span>2-year warranty on the pump</span></div>
      <div class="acc">
        {accordion('Specifications', f'<table class="spec-table" id="pdpSpecs">{specs}</table>', True)}
        {accordion('In the box', box_html)}
        {accordion('Care', f'<p>{esc(CARE.get(p["category"], ""))}</p>')}
        {accordion('Shipping & returns', '<p>Free US shipping over $120, flat $8 below. Ships from our US warehouse in 2–4 business days. 30-day trial: if your pet will not switch, send it back.</p>')}
      </div>
    </div>
  </div>
</div>
<section class="section"><div class="wrap">
  <div class="head-row"><div><p class="eyebrow" data-i18n="pdp.related">Also in the collection</p>
    <h2 class="h2" data-i18n="pdp.relatedTitle" data-reveal>Good together</h2></div></div>
  <div class="grid grid--3" data-grid="related" data-pids="{rel_ids}">{related}</div>
</div></section>
<div class="buybar" id="buybar"><div class="p"><small>{esc(p['name'])}</small>
  <span id="bbPrice">{money(p['price'])}</span></div>
  <button class="btn btn--sm" data-add="{pid}"><span data-i18n="common.addToBag">Add to bag</span></button></div>"""
    return page_ld(f"{p['name']} — {BRAND}", p["desc"], f"p-{pid}.html", body, "shop", product_jsonld(p))


def build_about():
    a = SITE["about"]
    secs = "".join(f'<div style="margin-bottom:34px" data-reveal><h2 class="h3" style="margin-bottom:10px">{esc(s["h"])}</h2>'
                   f'<p class="lede">{esc(s["p"])}</p></div>' for s in a["sections"])
    vals = "".join(f'<article><div class="k">0{i+1}</div><h4>{esc(v["title"])}</h4><p>{esc(v["text"])}</p></article>'
                   for i, v in enumerate(a["values"]["items"]))
    body = f"""
<section class="section tint"><div class="wrap">
  <p class="eyebrow">{esc(a['eyebrow'])}</p>
  <h1 class="display" style="max-width:18ch">{esc(a['title'])}</h1>
  <p class="lede" style="margin-top:20px;max-width:52ch">{esc(a['sub'])}</p>
</div></section>
<section class="section"><div class="wrap split">
  <div><img src="assets/products/hero.svg" alt="" style="width:min(82%,420px);margin:0 auto;filter:drop-shadow(0 30px 30px rgba(20,32,31,.16))"></div>
  <div>{secs}<p class="small" style="font-family:var(--serif);font-style:italic;font-size:17px">{esc(a['signature'])}</p></div>
</div></section>
<section class="section tint-mint"><div class="wrap">
  <h2 class="h2" style="margin-bottom:26px">{esc(a['values']['title'])}</h2>
  <div class="usp">{vals}</div>
</div></section>"""
    return page(f"About — {BRAND}", a["sub"], "about.html", body, "about")


def build_technology():
    t = SITE["technology"]
    secs = "".join(f'<div style="margin-bottom:30px" data-reveal><h3 class="h3">{esc(s["h"])}</h3>'
                   f'<p class="lede" style="margin-top:8px">{esc(s["p"])}</p></div>' for s in t["sections"])
    stats = "".join(f'<div class="stat"><div class="stat__v">{esc(s["v"])}<span style="font-size:.4em;color:var(--muted)">'
                    f'{esc(s["u"])}</span></div><div class="stat__l">{esc(s["l"])}</div></div>' for s in t["stats"])
    body = f"""
<section class="section tint"><div class="wrap">
  <p class="eyebrow">{esc(t['eyebrow'])}</p>
  <h1 class="display" style="max-width:20ch">{esc(t['title'])}</h1>
  <p class="lede" style="margin-top:20px">{esc(t['sub'])}</p>
</div></section>
<section class="section"><div class="wrap split">
  <div><img src="assets/products/spring-01.svg" alt="" style="width:min(82%,420px);margin:0 auto"></div>
  <div>{secs}</div>
</div></section>
<section class="section tint-sky"><div class="wrap">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:18px">{stats}</div>
  <p class="small" style="margin-top:22px">{esc(t['note'])}</p>
</div></section>"""
    return page(f"Technology — {BRAND}", t["sub"], "technology.html", body, "technology")


def build_journal():
    j = JOURNAL["index"]
    arts = JOURNAL["articles"]
    cards = "".join(f"""<a class="jcard" href="journal-{i+1}.html" data-reveal style="--d:{i*80}ms">
      <div class="jcard__media"><span class="jcard__tag">{esc(a['tag'])}</span>
        <img class="orn" src="assets/products/{['filter-3','still-bowl','still-mat'][i]}.svg" alt=""></div>
      <time>{esc(a['date'])} · {esc(a['read'])} min</time>
      <h3>{esc(a['title'])}</h3><p>{esc(a['excerpt'])}</p></a>""" for i, a in enumerate(arts))
    body = f"""
<section class="section tint"><div class="wrap">
  <p class="eyebrow">{esc(j['eyebrow'])}</p>
  <h1 class="display" style="max-width:20ch">{esc(j['title'])}</h1>
  <p class="lede" style="margin-top:18px">{esc(j['sub'])}</p>
</div></section>
<section class="section"><div class="wrap"><div class="journal-grid">{cards}</div></div></section>"""
    return page(f"Journal — {BRAND}", j["sub"], "journal.html", body, "journal")


def build_article(i, a):
    paras = "".join(f"<p>{esc(x)}</p>" for x in a["body"])
    body = f"""
<div class="wrap">
  <div class="article-head">
    <div class="meta-line"><span>{esc(a['tag'])}</span><span>{esc(a['date'])}</span><span>{esc(a['read'])} min</span></div>
    <h1 class="h1" style="max-width:22ch">{esc(a['title'])}</h1>
    <p class="lede" style="margin-top:16px">{esc(a['excerpt'])}</p>
  </div>
  <div class="article-media" style="background:var(--{'mint' if i==0 else 'sand' if i==1 else 'sky'})">
    <figure style="max-width:820px;padding:0 24px;text-align:center">
      <div class="eyebrow" style="justify-content:center;margin-bottom:14px">Journal · {i+1:02d} · {esc(a['tag'])}</div>
      <blockquote style="font-family:var(--serif);font-size:clamp(19px,2.3vw,32px);line-height:1.35;letter-spacing:-.015em;margin:0;color:var(--ink)">
        {esc(a['takeaway'])}</blockquote>
    </figure>
  </div>
  <div class="split" style="align-items:start">
    <div class="prose">{paras}
      <div class="takeaway">{esc(a['takeaway'])}</div></div>
    <div class="jside" style="position:sticky;top:96px">
      <p class="eyebrow" style="margin-bottom:12px">Shop this</p>
      <div class="grid" style="gap:14px" data-grid="article" data-pids="spring-01,still-bowl">
        {product_card(BY_ID['spring-01'], 0)}{product_card(BY_ID['still-bowl'], 60)}</div>
    </div>
  </div>
</div>"""
    return page(f"{a['title']} — {BRAND}", a["excerpt"], f"journal-{i+1}.html", body, "journal")


def build_faq():
    f = SITE["faq"]
    items = "".join(accordion(x["q"], f"<p>{esc(x['a'])}</p>", i == 0) for i, x in enumerate(f["items"]))
    body = f"""
<section class="section tint"><div class="wrap">
  <p class="eyebrow">{esc(f['eyebrow'])}</p>
  <h1 class="display" style="max-width:16ch">{esc(f['title'])}</h1>
  <p class="lede" style="margin-top:16px">{esc(f['sub'])}</p>
</div></section>
<section class="section"><div class="wrap" style="max-width:860px">
  <div class="acc">{items}</div>
  <p style="margin-top:26px" class="small">Still stuck? <a class="link-u" href="contact.html">Write to us</a></p>
</div></section>"""
    return page(f"FAQ — {BRAND}", f["sub"], "faq.html", body, "faq")


def build_contact():
    c = SITE["contact"]
    chans = "".join(f'<div style="border-top:1px solid var(--line);padding-top:14px;margin-top:14px">'
                    f'<div class="eyebrow" style="margin-bottom:4px">{esc(x["k"])}</div>'
                    f'<div style="font-size:15px">{esc(x["v"])}</div></div>' for x in c["channels"])
    body = f"""
<section class="section"><div class="wrap split" style="align-items:start">
  <div>
    <p class="eyebrow">{esc(c['eyebrow'])}</p>
    <h1 class="h1">{esc(c['title'])}</h1>
    <p class="lede" style="margin-top:14px">{esc(c['sub'])}</p>
    {chans}
    <p class="small" style="margin-top:18px">{esc(c['address'])}</p>
  </div>
  <form class="form" id="contactForm">
    <div class="form__row">
      <div class="field"><label>{esc(c['form']['name'])}</label><input required></div>
      <div class="field"><label>{esc(c['form']['email'])}</label><input type="email" required></div>
    </div>
    <div class="field"><label>{esc(c['form']['topic'])}</label>
      <select><option>Order</option><option>Returns</option><option>Product question</option><option>Wholesale</option></select></div>
    <div class="field"><label>{esc(c['form']['message'])}</label><textarea required></textarea></div>
    <button class="btn" type="submit"><span>{esc(c['form']['send'])}</span></button>
    <p class="small">{esc(c['form']['note'])}</p>
  </form>
</div></section>"""
    return page(f"Contact — {BRAND}", c["sub"], "contact.html", body, "")


def build_legal(slug, data, active=""):
    secs = "".join(f'<h2>{esc(s["h"])}</h2>' + "".join(f"<p>{esc(x)}</p>" for x in s["p"])
                   for s in data["sections"])
    nav_items = [("shipping.html", "Shipping"), ("returns.html", "Returns"),
                 ("warranty.html", "Warranty"), ("privacy.html", "Privacy"),
                 ("terms.html", "Terms"), ("wholesale.html", "Wholesale")]
    nav = "".join(f'<a href="{h}" class="{"is-on" if h == slug else ""}">{esc(l)}</a>' for h, l in nav_items)
    body = f"""
<section class="section"><div class="wrap legal">
  <aside class="legal__nav">{nav}</aside>
  <div class="prose">
    <p class="eyebrow">{esc(data.get('updated', ''))}</p>
    <h1 class="h1" style="margin-bottom:18px">{esc(data['title'])}</h1>
    <p style="font-size:16px">{esc(data['intro'])}</p>
    {secs}
  </div>
</div></section>"""
    return page(f"{data['title']} — {BRAND}", data["intro"], slug, body, active)


def build_wholesale():
    w = LEGAL["wholesale"]
    secs = "".join(f'<h2>{esc(s["h"])}</h2>' + "".join(f"<p>{esc(x)}</p>" for x in s["p"]) for s in w["sections"])
    f = w["form"]
    body = f"""
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="prose"><h1 class="h1" style="margin-bottom:16px">{esc(w['title'])}</h1>
    <p>{esc(w['intro'])}</p>{secs}</div>
  <form class="form">
    <div class="form__row">
      <div class="field"><label>{esc(f['company'])}</label><input required></div>
      <div class="field"><label>{esc(f['name'])}</label><input required></div>
    </div>
    <div class="form__row">
      <div class="field"><label>{esc(f['email'])}</label><input type="email" required></div>
      <div class="field"><label>{esc(f['country'])}</label><input required></div>
    </div>
    <div class="field"><label>{esc(f['volume'])}</label><input></div>
    <div class="field"><label>{esc(f['message'])}</label><textarea></textarea></div>
    <button class="btn" type="submit"><span>{esc(f['send'])}</span></button>
  </form>
</div></section>"""
    return page(f"Wholesale — {BRAND}", w["intro"], "wholesale.html", body, "")


def build_404():
    n = SITE["notFound"]
    body = f"""
<section class="section"><div class="wrap center" style="padding-block:80px">
  <p class="eyebrow" style="justify-content:center">404</p>
  <h1 class="display">{esc(n['title'])}</h1>
  <p class="lede" style="margin:16px auto 26px">{esc(n['sub'])}</p>
  <a class="btn" href="shop.html"><span>{esc(n['cta'])}</span></a>
</div></section>"""
    return page(f"Not found — {BRAND}", n["sub"], "404.html", body)



# ----------------------------------------------------------------- commerce
def build_cart():
    c = COMMERCE["cartPage"]
    trust = "".join(f"<li>{esc(x)}</li>" for x in c["trust"])
    body = f"""
<section class="section"><div class="wrap">
  <p class="eyebrow">{esc(c['eyebrow'])}</p>
  <h1 class="h1">{esc(c['title'])}</h1>
  <p class="lede" style="margin:12px 0 34px">{esc(c['sub'])}</p>
  <div class="cart-grid">
    <div>
      <div class="cart-head"><span>{esc(c['item'])}</span><span>{esc(c['qty'])}</span><span>{esc(c['price'])}</span></div>
      <div id="cartLines"></div>
      <p class="cart-empty" id="cartEmpty" hidden>{esc(c['empty'])}
        <a class="link-u" href="shop.html">{esc(c['emptyCta'])} →</a></p>
    </div>
    <aside class="cart-aside">
      <h2 class="h3" style="margin-bottom:16px">{esc(c['summary'])}</h2>
      <div class="cart-row"><span>{esc(c['subtotal'])}</span><span id="sumSubtotal">$0</span></div>
      <div class="cart-row"><span>{esc(c['shipping'])}</span><span id="sumShipping">—</span></div>
      <div class="cart-row total"><span>{esc(c['total'])}</span><b id="sumTotal">$0</b></div>
      <p class="small" style="margin:10px 0 16px">{esc(c['taxNote'])}</p>
      <a class="btn btn--full" href="checkout.html"><span>{esc(c['checkout'])}</span></a>
      <p class="small" style="margin-top:12px">{esc(c['shipNote'])}</p>
      <ul class="cart-trust">{trust}</ul>
    </aside>
  </div>
  <p style="margin-top:34px"><a class="link-u" href="shop.html">← {esc(c['continue'])}</a></p>
</div></section>"""
    return page_ld(f"{c['title']} — {BRAND}", c['sub'], "cart.html", body, "",
                   '<meta name="robots" content="noindex">')


def build_checkout():
    c = COMMERCE["checkout"]
    body = f"""
<section class="section"><div class="wrap">
  <p class="eyebrow">{esc(c['eyebrow'])} <span class="badge-soft">{esc(c['demoBadge'])}</span></p>
  <h1 class="h1">{esc(c['title'])}</h1>
  <p class="lede" style="margin:12px 0 32px">{esc(c['payNote'])}</p>
  <form class="checkout-grid" id="checkoutForm" novalidate>
    <div>
      <h2 class="h3">{esc(c['contact'])}</h2>
      <div class="form" style="margin:14px 0 30px">
        <div class="field"><label>{esc(c['email'])}</label><input type="email" name="email" required></div>
      </div>
      <h2 class="h3">{esc(c['shippingHead'])}</h2>
      <div class="form" style="margin-top:14px">
        <div class="field"><label>{esc(c['name'])}</label><input name="name" required></div>
        <div class="field"><label>{esc(c['address'])}</label><input name="address" required></div>
        <div class="form__row">
          <div class="field"><label>{esc(c['city'])}</label><input name="city" required></div>
          <div class="field"><label>{esc(c['zip'])}</label><input name="zip" required></div>
        </div>
        <div class="form__row">
          <div class="field"><label>{esc(c['country'])}</label>
            <select name="country"><option>United States</option><option>Canada</option>
              <option>United Kingdom</option><option>Germany</option><option>France</option>
              <option>Netherlands</option><option>Australia</option><option>Japan</option></select></div>
          <div class="field"><label>{esc(c['phone'])}</label><input name="phone"></div>
        </div>
        <div class="field"><label>{esc(c['method'])}</label>
          <select name="method"><option>{esc(c['standard'])}</option><option>{esc(c['express'])}</option></select></div>
      </div>
      <h2 class="h3" style="margin-top:30px">{esc(c['paymentHead'])}</h2>
      <p class="small" style="margin-top:8px">{esc(c['payNote'])}</p>
      <p style="margin-top:22px"><a class="link-u" href="cart.html">← {esc(c['back'])}</a></p>
    </div>
    <aside class="cart-aside">
      <h2 class="h3" style="margin-bottom:16px">{esc(c['summary'])}</h2>
      <div id="checkoutLines"></div>
      <div class="cart-row"><span>{esc(COMMERCE['cartPage']['subtotal'])}</span><span id="coSubtotal">$0</span></div>
      <div class="cart-row"><span>{esc(COMMERCE['cartPage']['shipping'])}</span><span id="coShipping">—</span></div>
      <div class="cart-row total"><span>{esc(COMMERCE['cartPage']['total'])}</span><b id="coTotal">$0</b></div>
      <button class="btn btn--full" type="submit" style="margin-top:16px"><span>{esc(c['placeOrder'])}</span></button>
      <p class="small" style="margin-top:12px">{esc(c['payNote'])}</p>
    </aside>
  </form>
</div></section>"""
    return page_ld(f"{c['title']} — {BRAND}", c['payNote'], "checkout.html", body, "",
                   '<meta name="robots" content="noindex">')


def build_success():
    c = COMMERCE["success"]
    steps = "".join(f"<li>{esc(x)}</li>" for x in c["steps"])
    body = f"""
<section class="section"><div class="wrap" style="max-width:760px">
  <p class="eyebrow">{esc(c['eyebrow'])}</p>
  <h1 class="h1">{esc(c['title'])}</h1>
  <p class="lede" style="margin:14px 0 26px">{esc(c['sub'])}</p>
  <div class="order-box">
    <span class="small">{esc(c['orderLabel'])}</span>
    <strong id="orderNo">—</strong>
    <span class="small" id="orderEmail"></span>
  </div>
  <p class="small" style="margin:14px 0 30px">{esc(c['emailNote'])}</p>
  <h2 class="h3">{esc(c['next'])}</h2>
  <ol class="order-steps">{steps}</ol>
  <a class="btn" href="shop.html" style="margin-top:26px"><span>{esc(c['cta'])}</span></a>
</div></section>"""
    return page_ld(f"{c['title']} — {BRAND}", c['sub'], "success.html", body, "",
                   '<meta name="robots" content="noindex">')



def main():
    global IS_ZH, BASE, CURRENT
    out = HERE
    zh_dir = HERE / "zh"

    made = {}

    def render_all():
        pages = {
            "index.html": build_home(),
            "shop.html": build_shop(),
            "about.html": build_about(),
            "technology.html": build_technology(),
            "journal.html": build_journal(),
            "faq.html": build_faq(),
            "contact.html": build_contact(),
            "wholesale.html": build_wholesale(),
            "404.html": build_404(),
            "cart.html": build_cart(),
            "checkout.html": build_checkout(),
            "success.html": build_success(),
        }
        for i, a in enumerate(JOURNAL["articles"]):
            pages[f"journal-{i+1}.html"] = build_article(i, a)
        for slug in ("shipping", "returns", "warranty", "privacy", "terms"):
            pages[f"{slug}.html"] = build_legal(f"{slug}.html", LEGAL[slug])
        for pr in PRODUCTS:
            pages[f"p-{pr['id']}.html"] = build_product(pr)
        return pages

    # --- English pass ---
    set_lang("en"); IS_ZH = False; BASE = ""
    en_pages = render_all()
    for name, content in en_pages.items():
        (out / name).write_text(content, encoding="utf-8")

    # --- Chinese pass (same renderers, Chinese data, written under /zh/) ---
    set_lang("zh"); IS_ZH = True; BASE = "../"
    zh_dir.mkdir(exist_ok=True)
    zh_pages = render_all()
    for name, content in zh_pages.items():
        # only asset URLs need lifting one level; page links stay relative
        content = content.replace('src="assets/', 'src="../assets/')
        content = content.replace('href="assets/', 'href="../assets/')
        (zh_dir / name).write_text(content, encoding="utf-8")

    # --- sitemap with both languages ---
    today = "2026-11-22"
    tier = {"index.html": "1.0", "shop.html": "0.9"}
    urls = []
    for name in en_pages:
        if name in ("404.html", "cart.html", "checkout.html", "success.html"):
            continue
        pri = tier.get(name, "0.8" if name.startswith("p-") else "0.6")
        urls.append((name, pri))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for name, pri in urls:
        en_url = DOMAIN + "/" + ("" if name == "index.html" else name)
        zh_url = DOMAIN + "/zh/" + ("" if name == "index.html" else name)
        alt = (f'<xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>'
               f'<xhtml:link rel="alternate" hreflang="zh-Hans" href="{zh_url}"/>')
        lines.append(f"  <url><loc>{en_url}</loc>{alt}<lastmod>{today}</lastmod><priority>{pri}</priority></url>")
        lines.append(f"  <url><loc>{zh_url}</loc>{alt}<lastmod>{today}</lastmod><priority>{pri}</priority></url>")
    lines.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    (out / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + DOMAIN + "/sitemap.xml\n", encoding="utf-8")

    total = len(en_pages) + len(zh_pages)
    print(f"wrote {len(en_pages)} EN pages + {len(zh_pages)} ZH pages = {total}")
    print(f"wrote sitemap.xml ({len(urls) * 2} urls, hreflang) and robots.txt")
    for old in ("product.html", "products.html"):
        if (out / old).exists():
            (out / old).unlink()
            print("removed stale", old)


if __name__ == "__main__":
    main()
