/* FinStart Advisory — shared site behaviour */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var WA_NUMBER = "919049638800";

  /* ---------- Every page opens at the top ----------
     Unless the link points to a section on the page (#name), reset scroll on load,
     including inside embedded previews where the outer frame keeps its position. */
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  function openAtTop() {
    var id = location.hash.length > 1 ? decodeURIComponent(location.hash.slice(1)) : "";
    var target = id && document.getElementById(id);
    if (target) return;
    try { window.scrollTo({ top: 0, left: 0, behavior: "instant" }); } catch (e) { window.scrollTo(0, 0); }
    try { document.documentElement.scrollIntoView({ block: "start", behavior: "instant" }); } catch (e) { /* not supported */ }
  }
  openAtTop();
  window.addEventListener("load", openAtTop);
  window.addEventListener("pageshow", function (e) { if (e.persisted) openAtTop(); });

  /* ---------- Header: scrolled state ---------- */
  var header = document.querySelector(".site-header");
  var wa = document.querySelector(".wa-float");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    if (wa) wa.classList.toggle("is-visible", y > 480);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.querySelector(".label").textContent = open ? "Close" : "Menu";
      nav.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setOpen(false); toggle.focus(); }
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    window.addEventListener("resize", function () { if (window.innerWidth >= 1024) setOpen(false); });
  }

  /* ---------- Hero chart: draw actuals, reveal milestones, then forecast ---------- */
  var chart = document.querySelector(".hero-chart");
  if (chart) {
    var line = chart.querySelector(".chart-actual");
    var ms = Array.prototype.slice.call(chart.querySelectorAll(".chart-ms[data-x]"));
    var forecastMs = chart.querySelector(".chart-ms--forecast");
    var finish = function () {
      ms.forEach(function (m) { m.classList.add("is-on"); });
      chart.classList.add("is-done");
      if (forecastMs) setTimeout(function () { forecastMs.classList.add("is-on"); }, reduceMotion ? 0 : 500);
    };
    if (!line || !line.getTotalLength || reduceMotion) {
      if (line) line.style.strokeDasharray = "none";
      finish();
    } else {
      var len = line.getTotalLength();
      // length along the path at which each milestone sits
      var stops = ms.map(function (m) {
        var tx = parseFloat(m.getAttribute("data-x")), best = 0, bestD = Infinity;
        for (var s = 0; s <= len; s += 4) {
          var d = Math.abs(line.getPointAtLength(s).x - tx);
          if (d < bestD) { bestD = d; best = s; }
        }
        return best / len;
      });
      line.style.strokeDasharray = len + " " + len;
      line.style.strokeDashoffset = len;
      var DURATION = 2600, start = null;
      var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
      var step = function (ts) {
        if (start === null) start = ts;
        var t = Math.min(1, (ts - start) / DURATION), p = ease(t);
        line.style.strokeDashoffset = len * (1 - p);
        stops.forEach(function (st, i) { if (p >= st - 0.005) ms[i].classList.add("is-on"); });
        if (t < 1) requestAnimationFrame(step); else finish();
      };
      setTimeout(function () { requestAnimationFrame(step); }, 350);
    }
  }

  /* ---------- Services page: highlight current section in sub-nav ---------- */
  var svcNav = document.querySelector(".svc-nav");
  if (svcNav && "IntersectionObserver" in window) {
    var links = Array.prototype.slice.call(svcNav.querySelectorAll("a[href^='#']"));
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var a = map[en.target.id];
          if (a && a !== current) {
            if (current) current.classList.remove("is-active");
            a.classList.add("is-active"); current = a;
            var wrap = svcNav.querySelector(".wrap");
            var left = a.offsetLeft - wrap.clientWidth / 2 + a.clientWidth / 2;
            wrap.scrollTo({ left: left, behavior: reduceMotion ? "auto" : "smooth" });
          }
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  /* ---------- Contact form ---------- */
  var form = document.getElementById("enquiry-form");
  if (form) {
    var status = document.getElementById("form-status");
    var btn = form.querySelector("button[type='submit']");

    // Prefill from the service finder, if the visitor came from there.
    try {
      var pre = sessionStorage.getItem("finstart-finder");
      if (pre) {
        pre = JSON.parse(pre);
        if (pre.service && form.service) form.service.value = pre.service;
        if (pre.role && form.role) form.role.value = pre.role;
        if (pre.summary && form.message && !form.message.value) form.message.value = pre.summary;
      }
    } catch (e) { /* storage unavailable: nothing to prefill */ }

    var setErr = function (name, msg) {
      var input = form.elements[name];
      var err = document.getElementById("err-" + name);
      if (input) input.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg || "";
    };
    var waLink = function (data) {
      var text = "Hello FinStart Advisory, I'm " + data.name + (data.company ? " from " + data.company : "") +
        ". " + (data.service && data.service !== "Not sure yet" ? "I'm interested in " + data.service + ". " : "") + data.message;
      return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(text);
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form._honey && form._honey.value) return;
      var data = {
        name: form.name.value.trim(), company: form.company.value.trim(),
        email: form.email.value.trim(), phone: form.phone.value.trim(),
        role: form.role.value, service: form.service.value, message: form.message.value.trim()
      };
      var ok = true;
      setErr("name", ""); setErr("email", ""); setErr("message", "");
      if (!data.name) { setErr("name", "Enter your name."); ok = false; }
      if (!data.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) { setErr("email", "Enter an email address we can reply to, like name@company.com."); ok = false; }
      if (!data.message) { setErr("message", "Tell us briefly what you need help with."); ok = false; }
      if (!ok) { var first = form.querySelector("[aria-invalid='true']"); if (first) first.focus(); return; }

      btn.disabled = true; btn.textContent = "Sending…";
      status.className = "form-status"; status.textContent = "";

      fetch(form.getAttribute("action"), {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          _subject: "Website enquiry: " + data.name + (data.company ? " (" + data.company + ")" : ""),
          _template: "table", _captcha: "false",
          Name: data.name, Company: data.company || "-", Email: data.email, Phone: data.phone || "-",
          "I am a": data.role, "Interested in": data.service, Message: data.message
        })
      }).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .then(function () {
          status.className = "form-status is-ok";
          status.textContent = "Enquiry sent. Thank you, " + data.name.split(" ")[0] + ". We'll be in touch to set up a discovery call.";
          form.reset();
          try { sessionStorage.removeItem("finstart-finder"); } catch (e2) {}
        })
        .catch(function () {
          status.className = "form-status is-err";
          status.innerHTML = "Your enquiry couldn't be sent from this page. Please <a href=\"" + waLink(data) +
            "\" target=\"_blank\" rel=\"noopener\">send it on WhatsApp</a> or email <a href=\"mailto:finstartadvisory@gmail.com\">finstartadvisory@gmail.com</a>. Your details are still in the form.";
        })
        .then(function () { btn.disabled = false; btn.textContent = "Send enquiry"; status.focus(); });
    });
  }

  /* ---------- Buyer / partner interest form (services page) ---------- */
  var iform = document.getElementById("interest-form");
  if (iform) {
    var istatus = document.getElementById("interest-status");
    var ibtn = iform.querySelector("button[type='submit']");
    var ierr = function (id, input, msg) {
      var el = document.getElementById(id); if (el) el.textContent = msg || "";
      if (input) input.setAttribute("aria-invalid", msg ? "true" : "false");
    };
    // "Any of the above" and "Not sure yet" stand alone; picking one clears the specific options.
    iform.addEventListener("change", function (e) {
      if (e.target.name !== "open_to" || !e.target.checked) return;
      var general = ["Any of the above", "Not sure yet"];
      var boxes = iform.querySelectorAll("input[name='open_to']");
      for (var k = 0; k < boxes.length; k++) {
        var b = boxes[k]; if (b === e.target) continue;
        var bGeneral = general.indexOf(b.value) > -1, tGeneral = general.indexOf(e.target.value) > -1;
        if (tGeneral || bGeneral) b.checked = false;
      }
      ierr("err-i-open", null, "");
    });
    iform.addEventListener("submit", function (e) {
      e.preventDefault();
      if (iform._honey && iform._honey.value) return;
      var open = Array.prototype.slice.call(iform.querySelectorAll("input[name='open_to']:checked")).map(function (b) { return b.value; });
      var d = { name: iform.name.value.trim(), email: iform.email.value.trim(), phone: iform.phone.value.trim(),
        role: iform.role.value, sectors: iform.sectors.value.trim(), note: iform.note.value.trim() };
      var ok = true;
      ierr("err-i-name", iform.name, ""); ierr("err-i-email", iform.email, ""); ierr("err-i-open", null, "");
      if (!d.name) { ierr("err-i-name", iform.name, "Enter your name."); ok = false; }
      if (!d.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) { ierr("err-i-email", iform.email, "Enter an email address we can reply to, like name@company.com."); ok = false; }
      if (!open.length) { ierr("err-i-open", null, "Choose at least one option, or “Not sure yet”."); ok = false; }
      if (!ok) { var f = iform.querySelector("[aria-invalid='true']") || iform.querySelector("input[name='open_to']"); if (f) f.focus(); return; }
      ibtn.disabled = true; ibtn.textContent = "Registering…";
      istatus.className = "form-status"; istatus.textContent = "";
      fetch(iform.getAttribute("action"), {
        method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({ _subject: "Buyer interest: " + d.name, _template: "table", _captcha: "false",
          Name: d.name, "I am": d.role, Email: d.email, Phone: d.phone || "-", "Open to": open.join(", "),
          "Sectors and locations": d.sectors || "-", Note: d.note || "-" })
      }).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .then(function () {
          istatus.className = "form-status is-ok";
          istatus.textContent = "Interest registered. Thank you, " + d.name.split(" ")[0] + ". We'll contact you when a suitable opportunity comes up.";
          iform.reset();
        })
        .catch(function () {
          var text = "Hello FinStart Advisory, I'd like to register interest in taking over or partnering with a business. I'm " + d.name +
            " (" + d.role.toLowerCase() + "), open to: " + open.join(", ").toLowerCase() + (d.sectors ? ". Interests: " + d.sectors : "") + ".";
          istatus.className = "form-status is-err";
          istatus.innerHTML = "Your details couldn't be sent from this page. Please <a href=\"https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(text) +
            "\" target=\"_blank\" rel=\"noopener\">send them on WhatsApp</a> or email <a href=\"mailto:finstartadvisory@gmail.com\">finstartadvisory@gmail.com</a>.";
        })
        .then(function () { ibtn.disabled = false; ibtn.textContent = "Register interest"; istatus.focus(); });
    });
  }

  /* ---------- Footer year ---------- */
  var y = document.querySelectorAll("[data-year]");
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();
})();
