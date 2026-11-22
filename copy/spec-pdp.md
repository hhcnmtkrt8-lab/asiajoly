Write the RILL 01 product detail page copy. Return ONE JSON object:

{
  "en": {"pdp": {
    "breadcrumb":["Home","Shop","RILL 01"],
    "eyebrow":"Fountain · 2.8 L",
    "title":"RILL 01",
    "subtitle":"one line, max 12 words",
    "price":"$129",
    "compareAt":"",
    "rating":"4.8","ratingCount":"312 pre-orders",
    "desc":"2-3 sentences, 40-60 words",
    "variantLabel":"Finish","variants":[{"name":"Steel","note":"brushed 316","hex":"#C7CBD0"},{"name":"Graphite","note":"matte","hex":"#2E3134"},{"name":"Sand","note":"powder coat","hex":"#D8CBB8"}],
    "qtyLabel":"Quantity",
    "cta":"Add to bag",
    "ctaNote":"one short line under the button",
    "stock":"one short availability line",
    "shipping":"one line, shipping + returns",
    "features":[{"k":"01","title":"3-5 words","text":"20-30 words"},{"k":"02","title":"","text":""},{"k":"03","title":"","text":""},{"k":"04","title":"","text":""}],
    "specs":[{"k":"Capacity","v":"2.8 L"},{"k":"","v":""},{"k":"","v":""},{"k":"","v":""},{"k":"","v":""},{"k":"","v":""},{"k":"","v":""},{"k":"","v":""},{"k":"","v":""},{"k":"","v":""}],
    "box":["RILL 01 body","...","...","...","...","..."],
    "care":[{"k":"Daily","v":"one sentence"},{"k":"Weekly","v":"one sentence"},{"k":"Filter","v":"one sentence"}],
    "faq":[{"q":"question","a":"35-50 words"},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""}],
    "related":["RILL 01 PRO","RILL BOWL","Filter 3-pack"]
  }},
  "zh": { ... same keys, native Chinese ... }
}

Rules:
- specs must use only the brief's real numbers: 2.8 L, 24 dB, 30-second teardown, 316 stainless, 1.8 m braided cable, 5 parts, dishwasher-safe, 72 h battery (PRO only — do not put PRO specs on RILL 01), filter 30 days, pump 18 months.
- No medical claims, no invented certifications, no fake review counts beyond "312 pre-orders" which is already given.
- box: exactly 6 items. specs: exactly 10 rows. features: 4. faq: 4.
