Write the homepage copy. Return ONE JSON object shaped exactly like this (both languages, identical structure):

{
  "en": {
    "nav": {"shop":"Shop","technology":"Technology","manifesto":"Manifesto","ritual":"Ritual","faq":"FAQ","cart":"Cart (0)","menu":"Menu"},
    "hero": {"eyebrow":"short kicker, 2-4 words","title":["Line one","Line two","Line three"],"sub":"1-2 sentences, max 30 words","cta":"Shop RILL 01","cta2":"See the teardown","scroll":"Scroll","note":"one line of small print under the buttons, e.g. free shipping / 30-day"},
    "marquee": ["316 stainless","24 dB","2.8 L","30-second clean","Made to be kept"],
    "manifesto": {"eyebrow":"01 — Manifesto","title":"6-9 word headline","p1":"60-80 words","p2":"60-80 words","p3":"40-60 words","signature":"— name / role"},
    "collection": {"eyebrow":"02 — The collection","title":"headline","sub":"1 sentence","viewAll":"View all","items":[
      {"id":"rill01","name":"RILL 01","kind":"Fountain","price":"$129","desc":"20-28 words","points":["3-5 words","3-5 words","3-5 words"],"label":"Core object","cta":"View RILL 01"},
      {"id":"rill01pro","name":"RILL 01 PRO","kind":"Fountain · app","price":"$169","desc":"20-28 words","points":["3-5 words","3-5 words","3-5 words"],"label":"Connected","cta":"View RILL 01 PRO"},
      {"id":"rillbowl","name":"RILL BOWL","kind":"Bowl","price":"$49","desc":"20-28 words","points":["3-5 words","3-5 words","3-5 words"],"label":"The companion","cta":"View RILL BOWL"}]},
    "tech": {"eyebrow":"03 — Engineering","title":"headline","sub":"1-2 sentences","stats":[
      {"value":"24","unit":"dB","label":"3-6 words","note":"one short clause"},
      {"value":"2.8","unit":"L","label":"3-6 words","note":"one short clause"},
      {"value":"30","unit":"s","label":"3-6 words","note":"one short clause"},
      {"value":"316","unit":"steel","label":"3-6 words","note":"one short clause"}]},
    "anatomy": {"eyebrow":"04 — Anatomy","title":"headline","sub":"1 sentence","hotspots":[
      {"id":"a","label":"2-4 words","text":"18-30 words"},
      {"id":"b","label":"2-4 words","text":"18-30 words"},
      {"id":"c","label":"2-4 words","text":"18-30 words"},
      {"id":"d","label":"2-4 words","text":"18-30 words"},
      {"id":"e","label":"2-4 words","text":"18-30 words"}]},
    "ritual": {"eyebrow":"05 — The ritual","title":"headline","sub":"1 sentence","steps":[
      {"n":"01","title":"3-5 words","text":"20-30 words"},
      {"n":"02","title":"3-5 words","text":"20-30 words"},
      {"n":"03","title":"3-5 words","text":"20-30 words"}]},
    "compare": {"eyebrow":"06 — Honest comparison","title":"headline","sub":"1 sentence","head":["","RILL 01","A typical fountain"],"rows":[
      {"label":"2-4 words","rill":"2-6 words","other":"2-6 words"},
      {"label":"","rill":"","other":""},
      {"label":"","rill":"","other":""},
      {"label":"","rill":"","other":""},
      {"label":"","rill":"","other":""},
      {"label":"","rill":"","other":""}]},
    "proof": {"eyebrow":"07 — Field notes","title":"headline","sub":"1 sentence","quotes":[
      {"text":"25-40 words","author":"First name + initial","role":"City"},
      {"text":"25-40 words","author":"First name + initial","role":"City"},
      {"text":"25-40 words","author":"First name + initial","role":"City"}],
      "disclaimer":"one short line noting these are pre-launch field-test notes"},
    "subscribe": {"eyebrow":"08 — Kept, not replaced","title":"headline","sub":"1 sentence","price":"$19","period":"/ quarter","points":["4-7 words","4-7 words","4-7 words"],"cta":"Start a filter plan","note":"one short line"},
    "faq": {"eyebrow":"09 — Questions","title":"headline","items":[
      {"q":"question","a":"35-55 words"},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""},{"q":"","a":""}]},
    "newsletter": {"eyebrow":"Keep in touch","title":"headline","sub":"1 sentence","placeholder":"Email address","cta":"Join","note":"one short line"},
    "footer": {"tagline":"one sentence","cols":[
      {"h":"Shop","links":["RILL 01","RILL 01 PRO","RILL BOWL","Filters","Pump"]},
      {"h":"Company","links":["Manifesto","Engineering","Journal","Contact"]},
      {"h":"Support","links":["Shipping","Returns","Warranty","Care guide"]}],
      "legal":"© 2026 RILL Objects Inc.","disclaimer":"one line about specifications being pre-production"}
  },
  "zh": { ... exactly the same keys and structure, native Chinese ... }
}

Rules:
- RILL 01 is the core object. The hero headline must not mention "hydration" or "healthy" — lead with the object and its material/quietness.
- FAQ must answer: why $129 vs a $30 fountain; is it quiet enough for a bedroom; can the pump be replaced; how often to clean; will my cat use it; is it safe for a dog; what about EU/UK shipping.
- Comparison rows compare honestly (RILL wins on steel, teardown, quietness, replaceable parts; typical fountain wins on price). Do not make the competitor row cartoonishly bad — one row must concede a real advantage.
- Every array must have exactly the number of items shown.
