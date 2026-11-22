Write the cart, checkout, order-confirmation and cookie-consent copy for Asiajoly.

Return ONE JSON object: {"en": {...}, "zh": {...}} with exactly this structure:

{
  "cartPage": {
    "eyebrow": "Bag",
    "title": "headline, max 6 words",
    "sub": "one sentence",
    "empty": "one sentence",
    "emptyCta": "2-3 words",
    "item": "Item", "qty": "Qty", "price": "Price", "remove": "Remove",
    "summary": "Order summary",
    "subtotal": "Subtotal", "shipping": "Shipping", "free": "Free",
    "taxNote": "one line about taxes being calculated at checkout",
    "total": "Total",
    "checkout": "Checkout", "continue": "Continue shopping",
    "shipNote": "one line: free over $120, flat $8 below",
    "trust": ["3-5 words", "3-5 words", "3-5 words"]
  },
  "checkout": {
    "eyebrow": "Checkout",
    "title": "headline, max 6 words",
    "contact": "Contact", "shippingHead": "Shipping address", "paymentHead": "Payment",
    "email": "Email", "name": "Full name", "address": "Address", "city": "City",
    "zip": "Postal code", "country": "Country", "phone": "Phone (optional)",
    "method": "Shipping method", "standard": "Standard (3-5 days)", "express": "Express (1-2 days)",
    "payNote": "one sentence explaining this is a preview build and no card is charged",
    "placeOrder": "Place order", "back": "Back to bag",
    "summary": "In your bag", "demoBadge": "Preview build"
  },
  "success": {
    "eyebrow": "Order",
    "title": "headline, max 6 words",
    "sub": "one sentence",
    "orderLabel": "Order number", "emailNote": "one line about the confirmation email",
    "next": "What happens next", "steps": ["3-6 words", "3-6 words", "3-6 words"],
    "cta": "Continue shopping"
  },
  "consent": {
    "title": "one short line",
    "text": "2 sentences, plain language, no dark patterns: what is stored, why",
    "accept": "Accept", "reject": "Only essential", "settings": "Cookie settings",
    "note": "one short line linking to the privacy page"
  }
}

Rules:
- Never imply real payment is taken. The checkout is a preview build until Stripe is connected — say so plainly once, without scaring the visitor.
- No dark patterns in the consent text: rejecting must feel like a first-class choice.
- Keep both languages the same length within ±20%.
