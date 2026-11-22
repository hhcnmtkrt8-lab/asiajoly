Write the policy pages. Return ONE JSON object: {"en": {...}, "zh": {...}} shaped as:

{
  "shipping": {"title":"Shipping","updated":"2026-02-01","intro":"2 sentences","sections":[{"h":"3-6 words","p":["paragraph","paragraph"]},{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]}]},
  "returns": {"title":"Returns & 30-day trial","updated":"","intro":"","sections":[{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]}]},
  "warranty": {"title":"Warranty","updated":"","intro":"","sections":[{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]}]},
  "privacy": {"title":"Privacy","updated":"","intro":"","sections":[{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]}]},
  "terms": {"title":"Terms of service","updated":"","intro":"","sections":[{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]},{"h":"","p":[""]}]},
  "wholesale": {"title":"Wholesale","updated":"","intro":"2 sentences","sections":[{"h":"","p":[""]},{"h":"","p":[""]}],
    "form":{"company":"Company","name":"Contact name","email":"Email","country":"Country","volume":"Expected monthly units","message":"Tell us about your store","send":"Send application"}}
}

Facts you may use:
- Prices in USD. Free US shipping over $120; flat $8 below that. EU/UK shipping calculated at checkout,
  duties and taxes not included. Orders ship from a US warehouse in 2–4 business days.
- Returns: 30-day trial on fountains and feeders — use it, and if your pet will not switch, send it back
  for a refund; buyer pays return shipping unless the unit is faulty. Consumables (filters, pumps) are
  not returnable once opened, except if faulty.
- Warranty: 2 years on the pump and electronics, 1 year on the battery, lifetime on the stainless body
  against manufacturing defects. Wear parts (filters) excluded.
- EU/UK: 14-day withdrawal right, 2-year legal guarantee. GPSR Responsible Person details are on the
  packaging and listing.
- Privacy: collect only what is needed to fulfil an order; no selling data; app data (Spring 01 Pro,
  Feast 01 Pro) stored to provide intake/feeding history, deletable on request.
- Terms: prices may change; the site is a direct-to-consumer store; governing law Delaware, USA.

Rules: write like a careful small brand, not a law firm — short paragraphs, plain language, but
complete. Do not invent company registration numbers, VAT IDs or addresses; where an address is
needed, use "[registered address]" as a placeholder. Never claim certifications that are not yet held;
for compliance say "designed to" and "testing in progress".
