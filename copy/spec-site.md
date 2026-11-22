Write the site-wide copy (home, shop, about, technology, faq, contact, 404, nav, footer).

Return ONE JSON object: {"en": {...}, "zh": {...}} with exactly this structure:

{
  "nav": {"shop":"Shop","fountains":"Fountains","feeders":"Feeders","bowls":"Bowls & Mats","play":"Play","about":"About","journal":"Journal","faq":"FAQ","cart":"Cart","menu":"Menu","search":"Search","all":"All products"},
  "common": {"addToBag":"Add to bag","view":"View","from":"From","new":"New","best":"Best seller","soldOut":"Sold out","freeShip":"Free shipping over $120","learnMore":"Learn more","shopAll":"Shop all","readMore":"Read","minutes":"min read","backHome":"Back to home","email":"Email address","subscribe":"Subscribe","close":"Close","loading":"Loading"},
  "home": {
    "hero": {"eyebrow":"4-6 words","title":["Line one","Line two"],"sub":"max 28 words","cta":"Shop the collection","cta2":"How it works","note":"short line about shipping/trial"},
    "ticker": ["4-6 words","4-6 words","4-6 words","4-6 words"],
    "intro": {"eyebrow":"01 — Why we exist","title":"6-9 words","p1":"50-70 words","p2":"50-70 words","link":"Read our story"},
    "lines": {"eyebrow":"02 — Four lines","title":"headline","sub":"1 sentence",
      "items":[{"name":"Spring","kind":"Fountains","text":"18-26 words","href":"shop.html?line=spring"},
               {"name":"Feast","kind":"Feeders","text":"18-26 words","href":"shop.html?line=feast"},
               {"name":"Still","kind":"Bowls & mats","text":"18-26 words","href":"shop.html?line=still"},
               {"name":"Play","kind":"Toys","text":"18-26 words","href":"shop.html?line=play"}]},
    "featured": {"eyebrow":"03 — Most loved","title":"headline","sub":"1 sentence"},
    "why": {"eyebrow":"04 — What we care about","title":"headline","sub":"1 sentence",
      "items":[{"k":"01","title":"3-5 words","text":"24-34 words"},{"k":"02","title":"","text":""},{"k":"03","title":"","text":""},{"k":"04","title":"","text":""}]},
    "journal": {"eyebrow":"05 — Journal","title":"headline","sub":"1 sentence"},
    "reviews": {"eyebrow":"06 — From the first homes","title":"headline","sub":"1 sentence",
      "items":[{"text":"24-36 words","author":"First name + initial","city":"City"},{"text":"","author":"","city":""},{"text":"","author":"","city":""}],
      "note":"one line saying these are pre-launch test-home notes"},
    "newsletter": {"eyebrow":"Letters","title":"headline","sub":"1 sentence","note":"one line"}
  },
  "shop": {"eyebrow":"Shop","title":"headline","sub":"1-2 sentences","count":"{n} products","filters":"Filter","sort":"Sort","sortOptions":["Featured","Price, low to high","Price, high to low","Newest"],"empty":"No products in this filter.","clear":"Clear filters"},
  "about": {"eyebrow":"About","title":"headline","sub":"1-2 sentences",
    "sections":[{"h":"3-6 words","p":"60-90 words"},{"h":"","p":""},{"h":"","p":""},{"h":"","p":""}],
    "values":{"title":"headline","items":[{"title":"3-5 words","text":"20-30 words"},{"title":"","text":""},{"title":"","text":""}]},
    "signature":"— Name, Founder"},
  "technology": {"eyebrow":"Technology","title":"headline","sub":"1-2 sentences",
    "sections":[{"h":"3-6 words","p":"55-85 words"},{"h":"","p":""},{"h":"","p":""}],
    "stats":[{"v":"24","u":"dB","l":"3-6 words"},{"v":"2.8","u":"L","l":""},{"v":"30","u":"s","l":""},{"v":"316","u":"steel","l":""}],
    "note":"one line about specs being design targets"},
  "faq": {"eyebrow":"FAQ","title":"headline","sub":"1 sentence","items":[
    {"q":"","a":"45-70 words"},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},
    {"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""}]},
  "contact": {"eyebrow":"Contact","title":"headline","sub":"1 sentence","form":{"name":"Name","email":"Email","topic":"Topic","message":"Message","send":"Send","note":"one line"},"channels":[{"k":"Support","v":"email address placeholder: hello@asiajoly.com"},{"k":"Wholesale","v":"trade@asiajoly.com"},{"k":"Returns","v":"returns@asiajoly.com"}],"address":"one line"},
  "notFound": {"title":"headline","sub":"1 sentence","cta":"Back to shop"},
  "footer": {"tagline":"one sentence","cols":[
    {"h":"Shop","links":["Spring fountains","Feast feeders","Still bowls","Play toys","Care"]},
    {"h":"Company","links":["About","Technology","Journal","Wholesale","Contact"]},
    {"h":"Help","links":["Shipping","Returns","Warranty","FAQ","Care guide"]}],
    "legal":"© 2026 Asiajoly.","disclaimer":"one line: preview build, specifications are design targets",
    "payNote":"one short line"}
}

Rules:
- FAQ items must answer: which fountain for two cats; is it quiet at night; how often to clean; can I
  replace the pump; are the parts dishwasher-safe; will my cat use it; is it safe for dogs; what is
  the difference between Spring 01 and 01 Pro; how does the filter subscription work; shipping to
  EU/UK; what is the warranty; what if my pet does not like it.
- `about.sections` tells the real story: a small team, factories in Shenzhen and Chaozhou (ceramics),
  why the objects are designed for small apartments, and why the brand exists. Do not invent
  funding, headcount or founding date beyond "2024".
- Arrays: fix lengths as shown (4 lines, 4 why items, 3 reviews, 4 about sections, 3 values,
  3 tech sections, 4 stats, 12 FAQs, 3 channels).
