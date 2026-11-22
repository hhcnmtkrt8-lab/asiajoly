/* =========================================================================
   Asiajoly — site behaviour
   Language switching, catalogue rendering, filtering, bag, PDP, motion.
   No dependencies. Runs on every page.
   ========================================================================= */
(function () {
  "use strict";

  const COPY = window.COPY || { en: {}, zh: {} };
  const CATALOGUE = (window.PRODUCTS || { items: [], order: [] });
  const ITEMS = CATALOGUE.items || [];
  const BY_ID = {};
  ITEMS.forEach(function (p) { BY_ID[p.id] = p; });

  const BAG_KEY = "aj-bag";
  const CONSENT_KEY = "aj-consent";
  const CONFIG = window.AJ_CONFIG || {};
  let lang = (document.documentElement.lang || "en").toLowerCase().indexOf("zh") === 0 ? "zh" : "en";
  const BASE = (document.querySelector('meta[name="aj-base"]') || {}).content || "";

  // Read the cache-busting version off our own <script src="...app.js?v=xxx"> tag,
  // so images injected at runtime stay in sync with the deployed build.
  const ASSET_V = (function () {
    const tag = Array.prototype.slice.call(document.scripts).filter(function (s) {
      return s.src && s.src.indexOf("app.js") >= 0;
    })[0];
    const m = tag && tag.src.match(/[?&]v=([\w-]+)/);
    return m ? m[1] : "";
  })();
  const asset = function (u) {
    if (!u) return u;
    let out = u;
    if (BASE && out.indexOf("assets/") === 0) out = BASE + out;
    return ASSET_V ? out + (out.indexOf("?") >= 0 ? "&" : "?") + "v=" + ASSET_V : out;
  };

  const $ = function (s, r) { return (r || document).querySelector(s); };
  const $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  const esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  };
  const money = function (n) { return "$" + Number(n).toFixed(0); };

  /* ---------------- i18n ---------------- */
  function t(path) {
    let node = COPY[lang];
    String(path).split(".").forEach(function (p) {
      if (node == null) return;
      node = Array.isArray(node) ? node[Number(p)] : node[p];
    });
    if (node == null && lang !== "en") {
      node = COPY.en;
      String(path).split(".").forEach(function (p) {
        if (node == null) return;
        node = Array.isArray(node) ? node[Number(p)] : node[p];
      });
    }
    return node == null ? "" : node;
  }
  function pt(p, key) { return (p && p[lang] && p[lang][key]) || (p && p.en && p.en[key]) || ""; }

  function applyStatic() {
    // Server-rendered text is already correct for this language; only fill gaps.
    $$("[data-i18n]").forEach(function (el) {
      if (el.textContent.trim()) return;
      const v = t(el.dataset.i18n);
      if (typeof v === "string" && v) el.textContent = v;
    });
    $$("[data-i18n-html]").forEach(function (el) {
      const v = t(el.dataset.i18nHtml);
      if (typeof v === "string") el.textContent = v;
    });
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
    const cl = $("#cartLabel");
    if (cl) cl.textContent = lang === "zh" ? "购物袋" : "Cart";
  }

  /* ---------------- catalogue ---------------- */
  function cardHtml(p, delay) {
    const colors = (p.colors || []).map(function (c) {
      return '<span class="dot" style="background:' + esc(c.hex) + '"></span>';
    }).join("");
    let badge = "";
    if (p.badge) {
      const cls = String(p.badge).toLowerCase() === "new" ? " card__badge--new" : "";
      badge = '<span class="card__badge' + cls + '">' + esc(p.badge) + "</span>";
    }
    return '<article class="card" data-reveal style="--d:' + (delay || 0) + 'ms" data-id="' + p.id + '">' +
      '<a class="card__media" href="p-' + p.id + '.html">' + badge +
      '<img src="' + asset(p.img) + '" alt="' + esc(pt(p, "name")) + '" loading="lazy" width="620" height="760">' +
      '<span class="card__swap"><span class="btn btn--sm btn--light">' + esc(t("common.view")) + "</span></span></a>" +
      '<div class="card__body"><div class="card__row">' +
      '<a class="card__name" href="p-' + p.id + '.html">' + esc(pt(p, "name")) + "</a>" +
      '<span class="card__price">' + money(p.price) + "</span></div>" +
      '<p class="card__meta">' + esc(pt(p, "tagline")) + "</p>" +
      '<div class="card__dots">' + colors + "</div></div></article>";
  }

  function renderGrids() {
    $$("[data-grid]").forEach(function (grid) {
      const ids = (grid.dataset.pids || "").split(",").filter(Boolean);
      const mode = grid.dataset.grid;
      let list = ids.map(function (id) { return BY_ID[id]; }).filter(Boolean);
      if (mode === "all") list = applyShopState(list);
      grid.innerHTML = list.map(function (p, i) { return cardHtml(p, i * 60); }).join("");
    });
    observeReveals();
  }

  /* ---------------- shop ---------------- */
  const shopState = { category: "All", sort: "Featured" };

  function applyShopState(list) {
    let out = list.slice();
    if (shopState.category !== "All") {
      const map = { Fountains: "spring", Feeders: "feast", Bowls: "still", Play: "play", Care: "care" };
      const slug = map[shopState.category];
      out = out.filter(function (p) { return p.category === shopState.category || p.lineSlug === slug; });
    }
    if (shopState.sort === "Price, low to high") out.sort(function (a, b) { return a.price - b.price; });
    else if (shopState.sort === "Price, high to low") out.sort(function (a, b) { return b.price - a.price; });
    else if (shopState.sort === "Newest") out.reverse();
    return out;
  }

  function initShop() {
    const grid = $("#shopGrid");
    if (!grid) return;
    const params = new URLSearchParams(location.search);
    const line = params.get("line");
    const cat = params.get("category");
    const lineToCat = { spring: "Fountains", feast: "Feeders", still: "Bowls", play: "Play", care: "Care" };
    if (cat) shopState.category = cat;
    else if (line && lineToCat[line]) shopState.category = lineToCat[line];

    $$(".chip").forEach(function (chip) {
      chip.classList.toggle("is-on", chip.dataset.filter === shopState.category);
      chip.addEventListener("click", function () {
        shopState.category = chip.dataset.filter;
        $$(".chip").forEach(function (c) { c.classList.toggle("is-on", c === chip); });
        renderGrids();
        updateCount();
      });
    });
    const sort = $("#sort");
    if (sort) sort.addEventListener("change", function () {
      shopState.sort = sort.value;
      renderGrids(); updateCount();
    });
    renderGrids(); updateCount();
  }

  function updateCount() {
    const el = $("#count");
    const grid = $("#shopGrid");
    const empty = $("#emptyNote");
    if (!el || !grid) return;
    const n = grid.querySelectorAll(".card").length;
    el.textContent = n + " " + (lang === "zh" ? "件产品" : "products");
    if (empty) empty.style.display = n ? "none" : "block";
  }

  /* ---------------- product page ---------------- */
  const pdpState = { qty: 1, color: 0 };

  function initPdp() {
    const wrap = $(".buy[data-pid]");
    if (!wrap) return;
    const p = BY_ID[wrap.dataset.pid];
    if (!p) return;

    const priceEl = $("#pdpPrice");
    const swatches = $$(".swatch");
    swatches.forEach(function (sw) {
      sw.addEventListener("click", function () {
        pdpState.color = Number(sw.dataset.color);
        swatches.forEach(function (s) { s.classList.toggle("is-on", s === sw); });
        const names = pt(p, "colorNames") || [];
        const cn = $("#colorName");
        if (cn) cn.textContent = names[pdpState.color] || "";
      });
    });
    const cn = $("#colorName");
    if (cn) {
      const names = pt(p, "colorNames") || [];
      cn.textContent = names[0] || "";
    }

    const qv = $("#qVal");
    $("#qMinus") && $("#qMinus").addEventListener("click", function () {
      pdpState.qty = Math.max(1, pdpState.qty - 1); qv.textContent = pdpState.qty;
    });
    $("#qPlus") && $("#qPlus").addEventListener("click", function () {
      pdpState.qty = Math.min(9, pdpState.qty + 1); qv.textContent = pdpState.qty;
    });
    $$("[data-add='" + p.id + "']").forEach(function (btn) {
      btn.addEventListener("click", function () { addToBag(p.id, pdpState.qty); });
    });

    $$("[data-thumb]").forEach(function (b) {
      b.addEventListener("click", function () {
        $$("[data-thumb]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
        const img = $("#galleryImg");
        const src = b.querySelector("img").getAttribute("src");
        if (img && src) { img.style.opacity = "0"; setTimeout(function () { img.src = src; img.style.opacity = "1"; }, 140); }
      });
    });

    const bar = $("#buybar");
    if (bar) window.addEventListener("scroll", function () {
      bar.classList.toggle("is-on", window.scrollY > 480);
    }, { passive: true });
  }

  function renderPdpText() {
    const wrap = $(".buy[data-pid]");
    if (!wrap) return;
    const p = BY_ID[wrap.dataset.pid];
    if (!p) return;
    const set = function (sel, val) { const el = $(sel); if (el) el.textContent = val; };
    set("#pdpName", pt(p, "name"));
    set("#pdpTag", pt(p, "tagline"));
    set("#pdpDesc", pt(p, "desc"));
    const ul = $("#pdpBullets");
    if (ul) ul.innerHTML = (pt(p, "bullets") || []).map(function (b) { return "<li>" + esc(b) + "</li>"; }).join("");
    const tbl = $("#pdpSpecs");
    if (tbl) tbl.innerHTML = (pt(p, "specs") || []).map(function (r) {
      return "<tr><td>" + esc(r.k) + "</td><td>" + esc(r.v) + "</td></tr>";
    }).join("");
    const names = pt(p, "colorNames") || [];
    const cn = $("#colorName");
    if (cn) cn.textContent = names[pdpState.color] || "";
    swatchesTitle(swatchesOf(p));
  }
  function swatchesOf(p) { return p.colors || []; }
  function swatchesTitle() { /* labels live in the title attribute; set at build time */ }

  /* ---------------- bag ---------------- */
  function readBag() {
    try { return JSON.parse(localStorage.getItem(BAG_KEY)) || []; } catch (e) { return []; }
  }
  function writeBag(items) {
    localStorage.setItem(BAG_KEY, JSON.stringify(items));
    renderBagCount(); renderBag(); renderCartPage(); renderCheckout();
  }
  function bagCount() { return readBag().reduce(function (s, i) { return s + i.qty; }, 0); }
  function bagTotal(items) {
    return items.reduce(function (s, i) { return s + (BY_ID[i.id] ? BY_ID[i.id].price : 0) * i.qty; }, 0);
  }
  function renderBagCount() {
    $$("#cartCount").forEach(function (el) { el.textContent = bagCount(); });
  }
  function renderBag() {
    const body = $("#cartBody"), foot = $("#cartFoot");
    if (!body || !foot) return;
    const items = readBag();
    if (!items.length) {
      body.innerHTML = '<p class="drawer__empty">' + esc(t("cart.empty")) + "</p>";
      foot.innerHTML = "";
      return;
    }
    body.innerHTML = items.map(function (i) {
      const p = BY_ID[i.id] || { name: i.id, price: 0, img: "" };
      return '<div class="line-item"><div class="line-item__img"><img src="' + p.img + '" alt=""></div>' +
        "<div><h4>" + esc(pt(p, "name")) + "</h4>" +
        '<div class="meta2">' + esc(t("pdp.inStock")) + "</div>" +
        '<div class="qty" style="height:32px;margin-top:7px"><button data-qty="-1" data-id="' + i.id + '">−</button>' +
        "<span>" + i.qty + "</span>" +
        '<button data-qty="1" data-id="' + i.id + '">+</button></div></div>' +
        '<div><div class="price">' + money(p.price * i.qty) + "</div>" +
        '<button class="rm" data-rm="' + i.id + '">' + esc(t("cart.remove")) + "</button></div></div>";
    }).join("");

    const total = bagTotal(items);
    const freeAt = 120;
    const pct = Math.min(100, (total / freeAt) * 100);
    foot.innerHTML =
      '<div class="shipbar"><i style="width:' + pct + '%"></i></div>' +
      '<div class="shipnote">' + (total >= freeAt
        ? esc(t("cart.unlocked"))
        : money(freeAt - total) + " " + esc(t("cart.away"))) + "</div>" +
      '<div class="drawer__row"><span>' + esc(t("cart.subtotal")) + "</span><span>" + money(total) + "</span></div>" +
      '<div class="drawer__row"><span>' + esc(t("cart.shipping")) + "</span><span>" +
        (total >= freeAt ? esc(t("cart.free")) : "$8") + "</span></div>" +
      '<div class="drawer__row total"><span>' + esc(t("cart.total")) + "</span><b>" +
        money(total + (total >= freeAt ? 0 : 8)) + "</b></div>" +
      '<a class="btn btn--full" href="' + BASE + 'cart.html"><span>' + esc(t("cart.checkout")) + "</span></a>" +
      '<a class="link-u" href="' + BASE + 'cart.html" style="display:block;text-align:center;margin-top:12px;font-size:11px">' +
        esc(lang === "zh" ? "查看购物袋" : "View bag") + "</a>" +
      '<p style="margin:10px 0 0;font-size:11px;color:var(--muted);text-align:center">' + esc(t("cart.note")) + "</p>";
  }

  function addToBag(id, qty) {
    const items = readBag();
    const found = items.filter(function (i) { return i.id === id; })[0];
    if (found) found.qty += qty || 1;
    else items.push({ id: id, qty: qty || 1 });
    writeBag(items);
    openBag();
    toast(lang === "zh" ? "已加入购物袋" : "Added to bag");
  }
  function openBag() {
    $("#drawer").classList.add("is-open");
    $("#drawer").setAttribute("aria-hidden", "false");
    $("#overlay").classList.add("is-open");
    document.body.classList.add("is-locked");
  }
  function closeBag() {
    const d = $("#drawer"); if (!d) return;
    d.classList.remove("is-open");
    d.setAttribute("aria-hidden", "true");
    $("#overlay").classList.remove("is-open");
    document.body.classList.remove("is-locked");
  }

  let toastTimer;
  function toast(msg) {
    const el = $("#toast"); if (!el) return;
    el.textContent = msg; el.classList.add("is-on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove("is-on"); }, 2300);
  }

  /* ---------------- motion ---------------- */
  let revealObs;
  // Anything already on screen is revealed immediately: the scroll animation is an
  // enhancement, never a precondition for reading the page (and some renderers and
  // preview services never fire IntersectionObserver).
  function revealInView() {
    const vh = window.innerHeight || 800;
    $$("[data-reveal]:not(.is-in)").forEach(function (el) {
      const r = el.getBoundingClientRect();
      if (r.top < vh * 0.96 && r.bottom > 0) { el.classList.add("is-in"); el.classList.add("is-instant"); }
    });
  }

  function observeReveals() {
    if (revealObs) revealObs.disconnect();
    if (!("IntersectionObserver" in window)) {
      $$("[data-reveal]").forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    revealObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); revealObs.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.05 });
    $$("[data-reveal]").forEach(function (el) { revealObs.observe(el); });
    requestAnimationFrame(revealInView);
    setTimeout(revealInView, 400);
    setTimeout(revealInView, 1500);
  }

  /* ---------------- misc ---------------- */
  function initAccordions() {
    $$(".acc__q").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const item = btn.parentElement;
        const open = item.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });
  }

  function initForms() {
    const nf = $("#newsForm");
    if (nf) nf.addEventListener("submit", function (e) {
      e.preventDefault();
      const v = ($("#newsEmail").value || "").trim();
      if (v.indexOf("@") < 1) { toast(lang === "zh" ? "请输入有效邮箱" : "Enter a valid email"); return; }
      $("#newsEmail").value = "";
      toast(lang === "zh" ? "已订阅。" : "Subscribed.");
    });
    const cf = $("#contactForm");
    if (cf) cf.addEventListener("submit", function (e) {
      e.preventDefault();
      cf.reset();
      toast(lang === "zh" ? "已发送，我们会在 1 个工作日内回复" : "Sent. We reply within one business day.");
    });
  }

  function initHeader() {
    const header = $("#header");
    if (header) {
      const onScroll = function () { header.classList.toggle("is-stuck", window.scrollY > 8); };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
    const mnav = $("#mnav");
    $("#menuBtn") && $("#menuBtn").addEventListener("click", function () { mnav.classList.add("is-open"); document.body.classList.add("is-locked"); });
    $("#mnavClose") && $("#mnavClose").addEventListener("click", function () { mnav.classList.remove("is-open"); document.body.classList.remove("is-locked"); });
  }


  /* ---------------- cart page ---------------- */
  function lineHtml(i) {
    const p = BY_ID[i.id] || { name: i.id, price: 0, img: "" };
    return '<div class="cart-line">' +
      '<div class="cart-line__prod">' +
        '<div class="cart-line__img"><img src="' + asset(p.img) + '" alt=""></div>' +
        '<div><h3>' + esc(pt(p, "name")) + "</h3>" +
        '<p class="small">' + esc(t("pdp.inStock")) + "</p></div>" +
      "</div>" +
      '<div><div class="qty"><button data-qty="-1" data-id="' + i.id + '">−</button>' +
        "<span>" + i.qty + "</span>" +
        '<button data-qty="1" data-id="' + i.id + '">+</button></div>' +
        '<button class="rm" data-rm="' + i.id + '">' + esc(t("cart.remove")) + "</button></div>" +
      '<div class="lineprice">' + money(p.price * i.qty) + "</div></div>";
  }

  function totals() {
    const items = readBag();
    const sub = bagTotal(items);
    const freeAt = CONFIG.freeShippingOver || 120;
    const flat = CONFIG.flatShipping || 8;
    const ship = sub === 0 ? 0 : (sub >= freeAt ? 0 : flat);
    return { items: items, sub: sub, ship: ship, total: sub + ship, freeAt: freeAt };
  }

  function renderCartPage() {
    const lines = $("#cartLines");
    if (!lines) return;
    const T = totals();
    const empty = $("#cartEmpty");
    if (!T.items.length) {
      lines.innerHTML = "";
      if (empty) empty.hidden = false;
    } else {
      if (empty) empty.hidden = true;
      lines.innerHTML = T.items.map(lineHtml).join("");
    }
    const check = document.querySelector('.cart-aside .btn');
    if (check) {
      const off = !T.items.length;
      check.style.opacity = off ? ".4" : "";
      check.style.pointerEvents = off ? "none" : "";
      check.setAttribute("aria-disabled", off ? "true" : "false");
    }
    if ($("#sumSubtotal")) $("#sumSubtotal").textContent = money(T.sub);
    if ($("#sumShipping")) $("#sumShipping").textContent = T.sub === 0 ? "—" : (T.ship ? money(T.ship) : t("cart.free"));
    if ($("#sumTotal")) $("#sumTotal").textContent = money(T.total);
  }

  /* ---------------- checkout ---------------- */
  function renderCheckout() {
    const box = $("#checkoutLines");
    if (!box) return;
    const T = totals();
    box.innerHTML = T.items.map(function (i) {
      const p = BY_ID[i.id] || { price: 0 };
      return '<div class="cart-row"><span>' + esc(pt(p, "name")) + " × " + i.qty +
             "</span><span>" + money(p.price * i.qty) + "</span></div>";
    }).join("");
    if ($("#coSubtotal")) $("#coSubtotal").textContent = money(T.sub);
    if ($("#coShipping")) $("#coShipping").textContent = T.ship ? money(T.ship) : t("cart.free");
    if ($("#coTotal")) $("#coTotal").textContent = money(T.total);
  }

  function orderNumber() {
    const d = new Date();
    const pad = function (n) { return String(n).padStart(2, "0"); };
    const rnd = Math.floor(1000 + Math.random() * 9000);
    return "AJ-" + String(d.getFullYear()).slice(2) + pad(d.getMonth() + 1) + pad(d.getDate()) + "-" + rnd;
  }

  function initCheckout() {
    const form = $("#checkoutForm");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const T = totals();
      if (!T.items.length) { toast(lang === "zh" ? "购物袋是空的" : "Your bag is empty"); return; }
      if (!form.checkValidity()) { form.reportValidity(); return; }
      const data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      const order = {
        no: orderNumber(), email: data.email || "", name: data.name || "",
        total: T.total, items: T.items.slice(), country: data.country || "",
        method: data.method || "", placed: new Date().toISOString(),
      };
      try { sessionStorage.setItem("aj-order", JSON.stringify(order)); } catch (err) {}
      writeBag([]);
      location.href = "success.html?order=" + encodeURIComponent(order.no);
    });
  }

  function initSuccess() {
    const el = $("#orderNo");
    if (!el) return;
    let order = null;
    try { order = JSON.parse(sessionStorage.getItem("aj-order") || "null"); } catch (e) {}
    const q = new URLSearchParams(location.search).get("order");
    el.textContent = (order && order.no) || q || "—";
    if (order && order.email && $("#orderEmail")) {
      $("#orderEmail").textContent = order.email + " · " + money(order.total);
    }
  }

  /* ---------------- consent + analytics ---------------- */
  function consentCopy() {
    const c = t("consent") || {};
    return {
      title: c.title || (lang === "zh" ? "关于 Cookie" : "A note on cookies"),
      text: c.text || (lang === "zh"
        ? "我们只用必要 Cookie 记住你的购物袋和语言。同意后我们才会加载访问统计。"
        : "We use essential cookies to remember your bag and language. Analytics only loads if you accept."),
      accept: c.accept || (lang === "zh" ? "同意" : "Accept"),
      reject: c.reject || (lang === "zh" ? "仅必要" : "Essential only"),
      note: c.note || "",
      settings: c.settings || "Cookie settings",
    };
  }

  function loadAnalytics() {
    const a = (CONFIG.analytics || {});
    if (a.ga4 && !window.__ajGa) {
      window.__ajGa = 1;
      const s = document.createElement("script");
      s.async = true;
      s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(a.ga4);
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", a.ga4, { anonymize_ip: true });
    }
    if (a.plausibleDomain && !window.__ajPl) {
      window.__ajPl = 1;
      const s = document.createElement("script");
      s.defer = true;
      s.setAttribute("data-domain", a.plausibleDomain);
      s.src = "https://plausible.io/js/script.js";
      document.head.appendChild(s);
    }
  }

  function renderConsent(force) {
    const c = consentCopy();
    let saved = null;
    try { saved = localStorage.getItem(CONSENT_KEY); } catch (e) {}
    if (saved === "accept") loadAnalytics();
    if (saved && !force) return;

    const el = document.createElement("div");
    el.className = "consent";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", c.title);
    el.innerHTML =
      "<div><strong>" + esc(c.title) + "</strong><p>" + esc(c.text) +
      (c.note ? ' <a href="privacy.html">' + esc(c.note) + "</a>" : "") + "</p></div>" +
      '<div class="consent__btns">' +
      '<button class="btn btn--ghost btn--sm" data-consent="reject"><span>' + esc(c.reject) + "</span></button>" +
      '<button class="btn btn--sm" data-consent="accept"><span>' + esc(c.accept) + "</span></button>" +
      "</div>";
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add("is-on"); });
    el.addEventListener("click", function (e) {
      const b = e.target.closest("[data-consent]");
      if (!b) return;
      try { localStorage.setItem(CONSENT_KEY, b.dataset.consent); } catch (err) {}
      if (b.dataset.consent === "accept") loadAnalytics();
      el.classList.remove("is-on");
      setTimeout(function () { el.remove(); }, 400);
    });
  }

  /* ---------------- boot ---------------- */
  function boot() {
    applyStatic();
    initHeader();
    initAccordions();
    initForms();
    initShop();
    initPdp();
    renderPdpText();
    renderBagCount();
    renderBag();
    renderCartPage();
    renderCheckout();
    initCheckout();
    initSuccess();
    renderConsent(false);
    observeReveals();

    $("#cartBtn") && $("#cartBtn").addEventListener("click", openBag);
    $("#closeCart") && $("#closeCart").addEventListener("click", closeBag);
    $("#overlay") && $("#overlay").addEventListener("click", closeBag);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeBag(); });

    document.addEventListener("click", function (e) {
      const add = e.target.closest("[data-add]");
      if (add) { e.preventDefault(); addToBag(add.dataset.add, pdpState.qty); return; }
      const q = e.target.closest("[data-qty]");
      if (q) {
        const items = readBag();
        const it = items.filter(function (i) { return i.id === q.dataset.id; })[0];
        if (it) {
          it.qty += Number(q.dataset.qty);
          if (it.qty <= 0) items.splice(items.indexOf(it), 1);
          writeBag(items);
        }
        return;
      }
      const rm = e.target.closest("[data-rm]");
      if (rm) {
        writeBag(readBag().filter(function (i) { return i.id !== rm.dataset.rm; }));
        return;
      }
      if (e.target.closest("#checkout")) {
        toast(lang === "zh" ? "演示站：结算未接入" : "Preview build: checkout not connected");
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
