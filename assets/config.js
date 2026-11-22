/* Site configuration — fill these in when the integrations are ready.
   Nothing here is secret: it all ships to the browser. Never put API secrets in this file. */
window.AJ_CONFIG = {
  currency: "USD",
  freeShippingOver: 120,
  flatShipping: 8,

  /* Real payments (optional).
     Create a Stripe Payment Link per product (no server needed):
       Stripe Dashboard → Payment links → New → add the product → copy the https://buy.stripe.com/... URL
     Paste them here. Products with a link get a "Buy now" button that goes straight to Stripe.
     With no links, checkout stays in preview mode (no card is ever charged). */
  stripe: {
    links: {
      // "spring-01": "https://buy.stripe.com/xxxxxxxx",
    }
  },

  /* Analytics — only loaded after the visitor accepts cookies.
     Set either one, or neither (then nothing is loaded). */
  analytics: {
    ga4: "",              // "G-XXXXXXXXXX"
    plausibleDomain: "",  // "asiajoly.com"  (privacy-friendly, no cookie banner strictly needed)
  },
};
