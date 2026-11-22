/* =========================================================================
   RILL — site behaviour
   i18n, rendering, cart, motion. No dependencies.
   ========================================================================= */
(function () {
  "use strict";

  const COPY = window.COPY || { en: {}, zh: {} };
  const LANGS = ["en", "zh"];
  const STORE_KEY = "rill-lang";
  const CART_KEY = "rill-bag";

  const PRODUCTS = {
    rill01: { img: "assets/fountain-steel.svg", price: 129 },
    rill01pro: { img: "assets/fountain-pro.svg", price: 169 },
    rillbowl: { img: "assets/bowl-sand.svg", price: 49 },
    filter: { img: "assets/filter.svg", price: 19 }
  };

  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  let lang = localStorage.getItem(STORE_KEY) || "en";
  if (LANGS.indexOf(lang) < 0) lang = "en";

  /* ---------------- i18n ---------------- */
  function t(path) {
    const parts = String(path).split(".");
    let node = COPY[lang];
    for (const p of parts) {
      if (node == null) break;
      node = node[p];
    }
    if (node == null && lang !== "en") {
      node = COPY.en;
      for (const p of parts) { if (node == null) break; node = node[p]; }
    }
    return node == null ? "" : node;
  }

  function applyStatic() {
    $$("[data-i18n]").forEach((el) => {
      const v = t(el.dataset.i18n);
      if (typeof v === "string") el.textContent = v;
    });
    $$("[data-i18n-attr]").forEach((el) => {
      const [attr, key] = el.dataset.i18nAttr.split(":");
      const v = t(key);
      if (typeof v === "string") el.setAttribute(attr, v);
    });
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
    const label = $("#langLabel");
    if (label) label.textContent = lang === "zh" ? "EN" : "中";
    const cl = $("#cartLabel");
    if (cl) cl.textContent = lang === "zh" ? "购物袋" : "Cart";
  }

  /* ---------------- home renderers ---------------- */
  function renderMarquee() {
    const el = $("#marquee");
    if (!el) return;
    const items = t("marquee") || [];
    const one = items.map((s) => '<span>' + esc(s) + "</span>").join("");
    el.innerHTML = one + one + one + one;
  }

  function renderCards() {
    const el = $("#cards");
    if (!el) return;
    const items = t("collection.items") || [];
    el.innerHTML = items.map((it, i) => `
      <article class="card" data-reveal style="--d:${i * 90}ms">
        <a href="product.html#${esc(it.id)}" aria-label="${esc(it.name)}">
          <div class="card__stage">
            <span class="card__label">${esc(it.label)}</span>
            <img src="${PRODUCTS[it.id] ? PRODUCTS[it.id].img : "assets/fountain-steel.svg"}" alt="${esc(it.name)}" loading="lazy">
          </div>
        </a>
        <div class="card__body">
          <div class="card__row">
            <span class="card__kind">${esc(it.kind)}</span>
            <span class="card__price num">${esc(it.price)}</span>
          </div>
          <h3 class="h3">${esc(it.name)}</h3>
          <p class="card__desc">${esc(it.desc)}</p>
          <ul class="card__points">${(it.points || []).map((p) => "<li>" + esc(p) + "</li>").join("")}</ul>
          <a class="card__cta" href="product.html#${esc(it.id)}"><span>${esc(it.cta)}</span><i>→</i></a>
        </div>
      </article>`).join("");
  }

  function renderStats() {
    const el = $("#stats");
    if (!el) return;
    const items = t("tech.stats") || [];
    el.innerHTML = items.map((s, i) => `
      <div class="stat" data-reveal style="--d:${i * 80}ms">
        <div class="stat__v num" data-count="${esc(s.value)}">0<span class="stat__u">${esc(s.unit)}</span></div>
        <div class="stat__l">${esc(s.label)}</div>
        <div class="stat__n">${esc(s.note)}</div>
      </div>`).join("");
  }

  function renderHotspots() {
    const el = $("#hotList");
    if (!el) return;
    const items = t("anatomy.hotspots") || [];
    el.innerHTML = items.map((h, i) => `
      <li data-hot-item="${i}">
        <span class="k">${String(i + 1).padStart(2, "0")}</span>
        <div><h4>${esc(h.label)}</h4><p>${esc(h.text)}</p></div>
      </li>`).join("");
  }

  function renderRitual() {
    const el = $("#ritualGrid");
    if (!el) return;
    const items = t("ritual.steps") || [];
    el.innerHTML = items.map((s, i) => `
      <article data-reveal style="--d:${i * 90}ms">
        <div class="n">${esc(s.n)}</div>
        <h4>${esc(s.title)}</h4>
        <p>${esc(s.text)}</p>
      </article>`).join("");
  }

  function renderCompare() {
    const head = $("#cmpHead"), body = $("#cmpBody");
    if (!head || !body) return;
    const h = t("compare.head") || ["", "RILL", "Other"];
    head.innerHTML = h.map((c, i) => `<th${i === 0 ? ' scope="col"' : ""}>${esc(c)}</th>`).join("");
    const rows = t("compare.rows") || [];
    body.innerHTML = rows.map((r) => `<tr>
      <th scope="row">${esc(r.label)}</th>
      <td class="rill">${esc(r.rill)}</td>
      <td>${esc(r.other)}</td>
    </tr>`).join("");
  }

  function renderQuotes() {
    const el = $("#quotes");
    if (!el) return;
    const items = t("proof.quotes") || [];
    el.innerHTML = items.map((q, i) => `
      <figure class="quote" data-reveal style="--d:${i * 90}ms">
        <blockquote>${esc(q.text)}</blockquote>
        <figcaption><b>${esc(q.author)}</b>${esc(q.role)}</figcaption>
      </figure>`).join("");
  }

  function renderSubscribe() {
    const el = $("#subList");
    if (!el) return;
    const items = t("subscribe.points") || [];
    el.innerHTML = items.map((p) => "<li>" + esc(p) + "</li>").join("");
  }

  function renderFaq() {
    const el = $("#faqList");
    if (!el) return;
    const items = t("faq.items") || [];
    el.innerHTML = items.map((f) => `
      <div class="faq__item">
        <button class="faq__q" aria-expanded="false"><span>${esc(f.q)}</span><i>+</i></button>
        <div class="faq__a"><div><p>${esc(f.a)}</p></div></div>
      </div>`).join("");
    $$(".faq__q", el).forEach((btn) => {
      btn.addEventListener("click", () => {
        const item = btn.parentElement;
        const open = item.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });
  }

  function renderFooter() {
    const cols = t("footer.cols") || [];
    const el = $("#footCols");
    if (el) {
      el.innerHTML = cols.map((c) => `<div>
        <h5>${esc(c.h)}</h5>
        <ul>${c.links.map((l) => `<li><a href="#">${esc(l)}</a></li>`).join("")}</ul>
      </div>`).join("");
    }
    const badges = $("#badges");
    if (badges) badges.innerHTML = "";
  }


  /* ---------------- product page ---------------- */
  const FINISH_IMG = ["assets/fountain-steel.svg", "assets/fountain-graphite.svg", "assets/fountain-sand.svg"];
  const RELATED = ["rill01pro", "rillbowl", "filter"];
  const pdpState = { variant: 0, qty: 1 };

  function accItem(id, label, inner, open) {
    return `<div class="faq__item${open ? " is-open" : ""}">
      <button class="faq__q" aria-expanded="${open ? "true" : "false"}"><span>${esc(label)}</span><i>+</i></button>
      <div class="faq__a"><div>${inner}</div></div>
    </div>`;
  }

  function renderPdp() {
    const titleEl = $("#pdpTitle");
    if (!titleEl) return;
    const p = t("pdp");
    if (!p || !p.title) return;

    const crumbs = p.breadcrumb || [];
    const crumbEl = $("#crumb");
    if (crumbEl) {
      crumbEl.innerHTML = crumbs.map((c, i) => {
        if (i === crumbs.length - 1) return "<span>" + esc(c) + "</span>";
        return '<a href="index.html">' + esc(c) + '</a><span>—</span>';
      }).join("");
    }
    $("#pdpEyebrow").textContent = p.eyebrow || "";
    titleEl.textContent = p.title;
    $("#pdpSub").textContent = p.subtitle || "";
    $("#pdpPrice").textContent = p.price || "";
    $("#pdpRating").textContent = [p.rating ? "★ " + p.rating : "", p.ratingCount || ""].filter(Boolean).join(" · ");
    $("#pdpDesc").textContent = p.desc || "";
    $("#variantLabel").textContent = p.variantLabel || "Finish";
    $("#pdpStock").textContent = p.stock || "";
    $("#pdpShip").textContent = p.shipping || "";
    $("#pdpCtaNote").textContent = p.ctaNote || "";
    $("#addLabel").textContent = p.cta || "Add to bag";
    $("#bbName").textContent = p.title;
    $("#bbPrice").textContent = p.price || "";

    // swatches
    const sw = $("#swatches");
    const variants = p.variants || [];
    sw.innerHTML = variants.map((v, i) =>
      `<button class="swatch${i === 0 ? " is-on" : ""}" data-sw="${i}" title="${esc(v.name)} — ${esc(v.note || "")}"
        style="background:${esc(v.hex)}" aria-label="${esc(v.name)}"></button>`).join("");
    const setVariant = (i) => {
      pdpState.variant = i;
      $$(".swatch").forEach((b, k) => b.classList.toggle("is-on", k === i));
      const v = variants[i];
      if (v) $("#variantName").textContent = v.name + (v.note ? " · " + v.note : "");
      const img = $("#pdpImg");
      if (img && FINISH_IMG[i]) { img.style.opacity = "0"; setTimeout(() => { img.src = FINISH_IMG[i]; img.style.opacity = "1"; }, 160); }
    };
    $$(".swatch").forEach((b) => b.addEventListener("click", () => setVariant(parseInt(b.dataset.sw, 10))));
    setVariant(0);

    // thumbs
    const th = $("#pdpThumbs");
    if (th) {
      th.innerHTML = FINISH_IMG.map((src, i) =>
        `<button data-th="${i}" class="${i === 0 ? "is-on" : ""}" aria-label="View ${i + 1}"><img src="${src}" alt=""></button>`).join("");
      $$("[data-th]").forEach((b) => b.addEventListener("click", () => {
        $$("[data-th]").forEach((x) => x.classList.remove("is-on"));
        b.classList.add("is-on");
        setVariant(parseInt(b.dataset.th, 10));
      }));
    }

    // features
    $("#features").innerHTML = (p.features || []).map((f) =>
      `<article><div class="k">${esc(f.k || "")}</div><h4>${esc(f.title)}</h4><p>${esc(f.text)}</p></article>`).join("");

    // accordion
    const specs = (p.specs || []).map((s) => `<tr><td>${esc(s.k)}</td><td>${esc(s.v)}</td></tr>`).join("");
    const box = (p.box || []).map((b) => "<li>" + esc(b) + "</li>").join("");
    const care = (p.care || []).map((c) => `<div class="drawer__row"><span>${esc(c.k)}</span><span style="text-align:right;max-width:60%">${esc(c.v)}</span></div>`).join("");
    const faqs = (p.faq || []).map((f) => accItem("f", f.q, "<p>" + esc(f.a) + "</p>", false)).join("");
    $("#acc").innerHTML =
      accItem("specs", (p.acc && p.acc.specs) || "Specifications", '<table class="spec-table">' + specs + "</table>", true) +
      accItem("box", (p.acc && p.acc.box) || "In the box", "<ul class=\"sub-list\">" + box + "</ul>", false) +
      accItem("care", (p.acc && p.acc.care) || "Care", care, false) +
      accItem("faq", (p.acc && p.acc.faq) || "Questions", faqs, false);

    $$("#acc .faq__q").forEach((btn) => btn.addEventListener("click", () => {
      const item = btn.parentElement;
      const open = item.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }));

    // related
    const rel = $("#related");
    if (rel) {
      rel.innerHTML = RELATED.map((id, i) => `
        <article class="card" data-reveal style="--d:${i * 90}ms">
          <a href="product.html" aria-label="${esc(productName(id))}">
            <div class="card__stage"><img src="${PRODUCTS[id].img}" alt="${esc(productName(id))}" loading="lazy"></div>
          </a>
          <div class="card__body">
            <div class="card__row"><span class="card__kind">${esc(lang === "zh" ? "系列" : "Collection")}</span>
              <span class="card__price num">$${PRODUCTS[id].price}</span></div>
            <h3 class="h3">${esc(productName(id))}</h3>
            <a class="card__cta" href="product.html"><span>${esc(lang === "zh" ? "查看" : "View")}</span><i>→</i></a>
          </div>
        </article>`).join("");
    }

    observeReveals();
  }

  function bindPdp() {
    const qv = $("#qVal");
    if (!qv) return;
    const sync = () => { qv.textContent = pdpState.qty; };
    $("#qMinus").addEventListener("click", () => { pdpState.qty = Math.max(1, pdpState.qty - 1); sync(); });
    $("#qPlus").addEventListener("click", () => { pdpState.qty = Math.min(9, pdpState.qty + 1); sync(); });
    $("#addBtn").addEventListener("click", () => addToCart("rill01", pdpState.qty));
    const bb = $("#bbAdd");
    if (bb) bb.addEventListener("click", () => addToCart("rill01", pdpState.qty));

    const bar = $("#buybar");
    window.addEventListener("scroll", () => {
      if (bar) bar.classList.toggle("is-on", window.scrollY > 520);
    }, { passive: true });
  }

  function renderAll() {
    applyStatic();
    renderMarquee();
    renderCards();
    renderStats();
    renderHotspots();
    renderRitual();
    renderCompare();
    renderQuotes();
    renderSubscribe();
    renderFaq();
    renderFooter();
    renderPdp();
    observeReveals();
    observeCounters();
    bindHotspots();
  }

  /* ---------------- cart ---------------- */
  function readCart() {
    try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; } catch (e) { return []; }
  }
  function writeCart(items) {
    localStorage.setItem(CART_KEY, JSON.stringify(items));
    renderCartCount();
    renderCart();
  }
  function cartTotal(items) {
    return items.reduce((s, i) => s + (PRODUCTS[i.id] ? PRODUCTS[i.id].price : 0) * i.qty, 0);
  }
  function renderCartCount() {
    const n = readCart().reduce((s, i) => s + i.qty, 0);
    $$("#cartCount").forEach((el) => { el.textContent = n; });
  }
  function productName(id) {
    const items = t("collection.items") || [];
    const found = items.find((x) => x.id === id);
    if (found) return found.name;
    if (id === "filter") return lang === "zh" ? "滤芯 3 片装" : "Filter, 3-pack";
    return id;
  }
  function money(n) { return "$" + n.toFixed(0); }

  function renderCart() {
    const body = $("#cartBody"), foot = $("#cartFoot");
    if (!body || !foot) return;
    const items = readCart();
    if (!items.length) {
      body.innerHTML = '<p class="drawer__empty">' + esc(lang === "zh" ? "购物袋是空的。" : "Your bag is empty.") + "</p>";
      foot.innerHTML = "";
      return;
    }
    body.innerHTML = items.map((i) => `
      <div class="line-item">
        <img src="${PRODUCTS[i.id] ? PRODUCTS[i.id].img : ""}" alt="${esc(productName(i.id))}">
        <div>
          <h4>${esc(productName(i.id))}</h4>
          <div class="meta">${esc(lang === "zh" ? "现货 · 2–4 个工作日发出" : "In stock · ships in 2–4 days")}</div>
          <div class="qty">
            <button data-qty="-1" data-id="${esc(i.id)}" aria-label="Decrease">−</button>
            <span>${i.qty}</span>
            <button data-qty="1" data-id="${esc(i.id)}" aria-label="Increase">+</button>
          </div>
        </div>
        <div class="price num">${money((PRODUCTS[i.id] ? PRODUCTS[i.id].price : 0) * i.qty)}</div>
      </div>`).join("");

    const total = cartTotal(items);
    const freeAt = 120;
    const pct = Math.min(100, (total / freeAt) * 100);
    foot.innerHTML = `
      <div class="ship-bar"><i style="width:${pct}%"></i></div>
      <div class="ship-note">${total >= freeAt
        ? esc(lang === "zh" ? "已享免运费" : "Free shipping unlocked")
        : esc(lang === "zh" ? `再买 $${(freeAt - total).toFixed(0)} 免运费` : `$${(freeAt - total).toFixed(0)} away from free shipping`)}</div>
      <div class="drawer__row"><span>${esc(lang === "zh" ? "小计" : "Subtotal")}</span><span class="num">${money(total)}</span></div>
      <div class="drawer__row"><span>${esc(lang === "zh" ? "运费" : "Shipping")}</span><span>${total >= freeAt ? esc(lang === "zh" ? "免费" : "Free") : "$8"}</span></div>
      <div class="drawer__row total"><span>${esc(lang === "zh" ? "合计" : "Total")}</span><b class="num">${money(total + (total >= freeAt ? 0 : 8))}</b></div>
      <button class="btn btn--full" id="checkout"><span>${esc(lang === "zh" ? "去结算" : "Checkout")}</span></button>
      <p style="margin:12px 0 0;font-size:11px;color:var(--fg-dim);text-align:center">${esc(lang === "zh" ? "演示站 · 不产生实际交易" : "Preview build · no payment is taken")}</p>`;
  }

  function addToCart(id, qty) {
    const items = readCart();
    const found = items.find((i) => i.id === id);
    if (found) found.qty += qty || 1;
    else items.push({ id: id, qty: qty || 1 });
    writeCart(items);
    openCart();
    toast(lang === "zh" ? "已加入购物袋" : "Added to bag");
  }

  function openCart() {
    $("#drawer").classList.add("is-open");
    $("#drawer").setAttribute("aria-hidden", "false");
    $("#overlay").classList.add("is-open");
    document.body.classList.add("is-locked");
  }
  function closeCart() {
    $("#drawer").classList.remove("is-open");
    $("#drawer").setAttribute("aria-hidden", "true");
    $("#overlay").classList.remove("is-open");
    document.body.classList.remove("is-locked");
  }

  let toastTimer;
  function toast(msg) {
    const el = $("#toast");
    if (!el) return;
    el.textContent = msg;
    el.classList.add("is-on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove("is-on"), 2400);
  }

  /* ---------------- motion ---------------- */
  let revealObs, countObs;
  function observeReveals() {
    if (revealObs) revealObs.disconnect();
    revealObs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("is-in"); revealObs.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    $$("[data-reveal]").forEach((el) => revealObs.observe(el));
  }

  function observeCounters() {
    if (countObs) countObs.disconnect();
    countObs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        const el = e.target;
        countObs.unobserve(el);
        const raw = el.dataset.count;
        const target = parseFloat(raw);
        const decimals = (raw.split(".")[1] || "").length;
        const dur = 1400;
        const t0 = performance.now();
        const unit = el.querySelector(".stat__u");
        const unitHTML = unit ? unit.outerHTML : "";
        (function tick(now) {
          const p = Math.min(1, (now - t0) / dur);
          const eased = 1 - Math.pow(1 - p, 3);
          el.innerHTML = (target * eased).toFixed(decimals) + unitHTML;
          if (p < 1) requestAnimationFrame(tick);
        })(t0);
      });
    }, { threshold: 0.4 });
    $$("[data-count]").forEach((el) => countObs.observe(el));
  }

  function bindHotspots() {
    const dots = $$(".hot"), rows = $$("[data-hot-item]");
    if (!dots.length || !rows.length) return;
    const on = (i) => {
      dots.forEach((d, k) => d.classList.toggle("is-on", k === i));
      rows.forEach((r, k) => r.classList.toggle("is-on", k === i));
    };
    dots.forEach((d, i) => {
      d.addEventListener("mouseenter", () => on(i));
      d.addEventListener("click", () => on(i));
    });
    rows.forEach((r, i) => {
      r.addEventListener("mouseenter", () => on(i));
      r.addEventListener("click", () => on(i));
    });
    on(0);
  }

  /* ---------------- caustics ---------------- */
  function initCaustics() {
    const cv = $("#caustics");
    if (!cv) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ctx = cv.getContext("2d", { alpha: true });
    let w = 0, h = 0, dpr = Math.min(2, window.devicePixelRatio || 1);
    let raf = 0, t0 = performance.now();

    function resize() {
      w = cv.clientWidth; h = cv.clientHeight;
      cv.width = Math.floor(w * dpr); cv.height = Math.floor(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function draw(now) {
      const t = (now - t0) / 1000;
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = "lighter";
      const lines = 13;
      for (let i = 0; i < lines; i++) {
        const yBase = (i / lines) * h * 1.1 - h * 0.05;
        const amp = 12 + ((i * 7) % 26);
        const freq = 0.004 + ((i % 5) * 0.0016);
        const speed = 0.16 + ((i % 4) * 0.05);
        ctx.beginPath();
        for (let x = 0; x <= w; x += 14) {
          const y = yBase + Math.sin(x * freq + t * speed + i) * amp
                    + Math.sin(x * freq * 2.3 + t * speed * 1.6 + i * 2) * amp * 0.4;
          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        const alpha = 0.028 + (i % 3) * 0.012;
        const g = ctx.createLinearGradient(0, 0, w, 0);
        g.addColorStop(0, "rgba(169,203,217,0)");
        g.addColorStop(0.35, `rgba(169,203,217,${alpha})`);
        g.addColorStop(0.65, `rgba(169,203,217,${alpha * 0.8})`);
        g.addColorStop(1, "rgba(169,203,217,0)");
        ctx.strokeStyle = g;
        ctx.lineWidth = 1.15;
        ctx.stroke();
      }
      ctx.globalCompositeOperation = "source-over";
      raf = requestAnimationFrame(draw);
    }

    resize();
    window.addEventListener("resize", function () { resize(); }, { passive: true });
    raf = requestAnimationFrame(draw);
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) cancelAnimationFrame(raf);
      else raf = requestAnimationFrame(draw);
    });
  }

  /* ---------------- header / parallax ---------------- */
  function initHeader() {
    const header = $("#header");
    if (!header) return;
    let last = 0, ticking = false;
    function onScroll() {
      const y = window.scrollY;
      header.classList.toggle("is-solid", y > 40);
      const probe = document.elementFromPoint(Math.min(window.innerWidth - 8, 24), 34);
      const inLight = probe && probe.closest && probe.closest(".light");
      header.classList.toggle("is-light", !!inLight);
      const stage = $("#heroStage");
      if (stage && y < window.innerHeight * 1.2) {
        stage.style.transform = "translateY(" + (y * 0.12) + "px)";
      }
      last = y; ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
    }, { passive: true });
    onScroll();
  }

  /* ---------------- language ---------------- */
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l;
    localStorage.setItem(STORE_KEY, l);
    renderAll();
    renderCart();
  }

  /* ---------------- boot ---------------- */
  function boot() {
    renderAll();
    renderCartCount();
    renderCart();
    initCaustics();
    initHeader();
    bindPdp();

    $("#langBtn") && $("#langBtn").addEventListener("click", () => setLang(lang === "zh" ? "en" : "zh"));
    $("#cartBtn") && $("#cartBtn").addEventListener("click", openCart);
    $("#closeCart") && $("#closeCart").addEventListener("click", closeCart);
    $("#overlay") && $("#overlay").addEventListener("click", closeCart);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeCart(); });

    document.addEventListener("click", (e) => {
      const add = e.target.closest("[data-add]");
      if (add) { e.preventDefault(); addToCart(add.dataset.add, 1); return; }
      const q = e.target.closest("[data-qty]");
      if (q) {
        const id = q.dataset.id, d = parseInt(q.dataset.qty, 10);
        const items = readCart();
        const it = items.find((i) => i.id === id);
        if (it) { it.qty += d; if (it.qty <= 0) items.splice(items.indexOf(it), 1); writeCart(items); }
      }
      const co = e.target.closest("#checkout");
      if (co) toast(lang === "zh" ? "演示站：结算流程未接入" : "Preview build: checkout not connected");
    });

    const form = $("#newsForm");
    if (form) form.addEventListener("submit", (e) => {
      e.preventDefault();
      const v = $("#newsEmail").value.trim();
      if (!v || v.indexOf("@") < 0) { toast(lang === "zh" ? "请输入有效邮箱" : "Enter a valid email"); return; }
      $("#newsEmail").value = "";
      toast(lang === "zh" ? "已订阅。保持安静。" : "Subscribed. Stay quiet.");
    });

    const menuBtn = $("#menuBtn");
    if (menuBtn) menuBtn.addEventListener("click", () => {
      const n = $(".nav");
      if (!n) return;
      const open = n.dataset.open === "1";
      if (open) { n.removeAttribute("data-open"); n.removeAttribute("style"); }
      else {
        n.dataset.open = "1";
        n.setAttribute("style", "display:flex;position:fixed;inset:74px 0 auto;flex-direction:column;gap:6px;padding:24px var(--pad) 32px;background:rgba(8,9,11,.97);backdrop-filter:blur(18px);border-bottom:1px solid var(--line);z-index:59");
        $$("a", n).forEach((a) => { a.style.fontSize = "18px"; a.style.letterSpacing = ".08em"; a.style.padding = "10px 0"; });
        $$("a", n).forEach((a) => a.addEventListener("click", () => { n.removeAttribute("data-open"); n.removeAttribute("style"); }));
      }
    });
  }

  setTimeout(function () { document.documentElement.classList.add("anim-done"); }, 2600);

  document.addEventListener("DOMContentLoaded", boot);
})();
