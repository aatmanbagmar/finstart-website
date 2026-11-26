/* FinStart Advisory — "Which service do I need?" finder */
(function () {
  "use strict";
  var root = document.getElementById("finder");
  if (!root) return;

  var WA_NUMBER = "919049638800";
  var CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4.5 10.5l3.5 3.5 7.5-8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var CHEV = '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  var PAGES = { "vcfo": "virtual-cfo", "mis": "mis-reporting", "strategy": "strategic-consulting",
    "fundraise": "fundraise-support", "valuation": "business-valuation", "deal-structuring": "deal-structuring",
    "tax-compliance": "tax-compliance", "tax-advisory": "tax-advisory", "restructuring": "restructuring",
    "succession": "succession-planning" };
  var pageFor = function (k) { return PAGES[k] + ".html"; };

  var SERVICES = {
    "vcfo": {
      name: "Virtual CFO", model: "Ongoing retainer with no lock-in",
      pitch: "You need someone to own the numbers month after month: closing the books with your accountant, tracking cash, and helping you make decisions with data.",
      points: ["A monthly MIS and review meeting", "Cash flow, budget and forecast you can rely on", "Investor, board or lender reporting handled", "Compliance calendar kept on track"]
    },
    "mis": {
      name: "MIS & reporting", model: "Set-up project, then monthly",
      pitch: "Your first priority is a clear, reliable monthly view of profit, margins and cash, built around how you actually run the business.",
      points: ["KPIs chosen for your business model", "A monthly MIS pack and dashboard", "P&L by product, branch or channel", "A month-end routine that runs without chasing"]
    },
    "strategy": {
      name: "Strategic consulting", model: "Scoped to the decision",
      pitch: "You have a decision with real money attached. We'll model the options and give you a recommendation you can act on.",
      points: ["Business plan and projections", "Pricing, margin and cost review", "Feasibility for new markets or ventures", "Bank finance readiness"]
    },
    "fundraise": {
      name: "Fundraise support", model: "4-week or 6-week sprint",
      pitch: "You're preparing to raise. A focused sprint gets your story, numbers and documents investor-ready.",
      points: ["Pitch deck and investor-grade financial model", "Valuation and round sizing", "Data room and diligence preparation", "Support through investor conversations and term sheets"]
    },
    "valuation": {
      name: "Business valuation", model: "Scoped project",
      pitch: "You need to know what the business, or a stake in it, is worth, using methods investors and acquirers recognise.",
      points: ["DCF and market-based valuation", "Scenario and sensitivity analysis", "A clear explanation you can negotiate with", "Coordination of registered valuer reports where regulation requires one"]
    },
    "deal-structuring": {
      name: "Deal structuring", model: "Scoped to the deal",
      pitch: "A partner, investor or acquisition is on the table. The structure decides tax, control and what happens when things change.",
      points: ["Choice of instrument and structure", "Term sheet review and negotiation support", "Tax impact of each option", "Financial due diligence"]
    },
    "tax-compliance": {
      name: "Tax compliance (direct & indirect)", model: "Year-round compliance retainer",
      pitch: "You want income tax, TDS and GST handled correctly and on time, with no last-minute scramble.",
      points: ["Income tax, TDS and advance tax", "GST returns and reconciliations", "An annual compliance calendar with reminders", "Responses to notices"]
    },
    "tax-advisory": {
      name: "Tax advisory", model: "Scoped advice",
      pitch: "There's a tax question behind your plans. It's cheapest to get the answer before you act.",
      points: ["Tax-efficient business structures", "Startup tax benefits and DPIIT recognition", "ESOP and founder taxation", "Opinions on specific tax positions"]
    },
    "succession": {
      name: "Succession planning & business transition", model: "Scoped mandate, handled in confidence",
      pitch: "You're thinking about what happens to the business next. We'll plan the handover, value the business and find the right next owner, partner or operator, discreetly.",
      points: ["A readiness review and valuation", "The right route: sale, partner, operator, buyout or family handover", "Suitable parties approached confidentially, after your approval", "Negotiation, tax on the transfer and a handover plan"]
    },
    "restructuring": {
      name: "Restructuring", model: "Scoped project",
      pitch: "You're changing ownership, entity type or group structure. We'll plan the route and model the tax before anything moves.",
      points: ["Conversions to a company or LLP", "Mergers, demergers and holding structures", "Family business separation and succession", "Shareholder and partner exits"]
    }
  };

  // how strongly each answer points to each service
  var NEED_WEIGHTS = {
    raise:      { fundraise: 4, valuation: 1, "deal-structuring": 1 },
    numbers:    { mis: 4, vcfo: 2 },
    cash:       { vcfo: 4, mis: 1 },
    compliance: { "tax-compliance": 4 },
    taxplan:    { "tax-advisory": 4 },
    structure:  { restructuring: 4, "tax-advisory": 1 },
    deal:       { "deal-structuring": 4, valuation: 2 },
    value:      { valuation: 4 },
    growth:     { strategy: 4, vcfo: 1 },
    succession: { succession: 5, valuation: 1, restructuring: 1 }
  };
  var STAGE_WEIGHTS = {
    idea:        { "tax-advisory": 1, strategy: 1 },
    early:       { mis: 1, fundraise: 1 },
    scaling:     { vcfo: 2, fundraise: 1 },
    established: { mis: 1, "tax-compliance": 1 }
  };
  var TEAM_WEIGHTS = {
    founder:    { vcfo: 2, mis: 1 },
    accountant: { vcfo: 1, mis: 1 },
    team:       { vcfo: -1 },
    ca:         {}
  };
  var ROLE_FOR_STAGE = { idea: "Startup founder", early: "Startup founder", scaling: "Startup founder", established: "Business owner" };

  var steps = Array.prototype.slice.call(root.querySelectorAll(".finder-step"));
  var bars = Array.prototype.slice.call(root.querySelectorAll(".finder-progress span"));
  var msg = root.querySelector(".finder-msg");
  var backBtn = root.querySelector("[data-back]");
  var nextBtn = root.querySelector("[data-next]");
  var countEl = root.querySelector(".finder-nav .count");
  var nav = root.querySelector(".finder-nav");
  var result = document.getElementById("finder-result");
  var current = 0;

  function show(i) {
    current = i;
    steps.forEach(function (s, j) { s.classList.toggle("is-active", j === i); });
    bars.forEach(function (b, j) { b.classList.toggle("is-on", j <= i); });
    backBtn.hidden = i === 0;
    nextBtn.textContent = i === steps.length - 1 ? "See my recommendation" : "Next question";
    countEl.textContent = "Question " + (i + 1) + " of " + steps.length;
    msg.textContent = "";
    var legend = steps[i].querySelector("legend");
    if (legend) { legend.setAttribute("tabindex", "-1"); legend.focus({ preventScroll: true }); }
  }

  function answered(step) {
    return step.querySelectorAll("input:checked").length > 0;
  }

  function values(name) {
    return Array.prototype.slice.call(root.querySelectorAll("input[name='" + name + "']:checked")).map(function (i) { return i.value; });
  }
  function labelFor(name, value) {
    var input = root.querySelector("input[name='" + name + "'][value='" + value + "']");
    var l = input && root.querySelector("label[for='" + input.id + "']");
    return l ? l.querySelector("b").textContent : value;
  }

  function compute() {
    var stage = values("stage")[0], needs = values("needs"), team = values("team")[0], when = values("when")[0];
    var score = {};
    Object.keys(SERVICES).forEach(function (k) { score[k] = 0; });
    var add = function (w) { Object.keys(w || {}).forEach(function (k) { score[k] += w[k]; }); };
    needs.forEach(function (n) { add(NEED_WEIGHTS[n]); });
    add(STAGE_WEIGHTS[stage]); add(TEAM_WEIGHTS[team]);
    // several ongoing needs together are what a vCFO engagement is for
    var ongoing = ["numbers", "cash", "compliance", "growth", "raise"].filter(function (n) { return needs.indexOf(n) > -1; }).length;
    if (ongoing >= 3) score.vcfo += 3;
    var ranked = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; });
    return {
      stage: stage, needs: needs, team: team, when: when,
      primary: ranked[0],
      also: ranked.slice(1).filter(function (k) { return score[k] >= 3; }).slice(0, 3)
    };
  }

  function render(r) {
    var p = SERVICES[r.primary];
    var summary = "Stage: " + labelFor("stage", r.stage) + ". " +
      "Looking for help with: " + r.needs.map(function (n) { return labelFor("needs", n).toLowerCase(); }).join(", ") + ". " +
      "Finance today: " + labelFor("team", r.team).toLowerCase() + ". " +
      "Timing: " + labelFor("when", r.when).toLowerCase() + ". " +
      "Service finder suggested: " + p.name + ".";
    var waText = "Hello FinStart Advisory, I used the service finder on your website. " + summary + " I'd like to set up a discovery call.";

    try {
      sessionStorage.setItem("finstart-finder", JSON.stringify({ service: p.name.indexOf("Tax compliance") === 0 ? "Tax compliance" : p.name, role: ROLE_FOR_STAGE[r.stage], summary: summary }));
    } catch (e) { /* storage unavailable: contact form simply won't be prefilled */ }

    var html = '<div class="result-main"><div class="grid-paper" aria-hidden="true"></div>' +
      '<p class="label">Our recommendation</p>' +
      '<h2 tabindex="-1" id="result-title">' + p.name + '</h2>' +
      '<p>' + p.pitch + '</p>' +
      '<ul>' + p.points.map(function (t) { return '<li>' + CHECK + '<span>' + t + '</span></li>'; }).join("") + '</ul>' +
      '<p style="margin-bottom:1.5rem"><strong style="color:#fff">How it runs:</strong> ' + p.model + '</p>' +
      '<div class="result-actions">' +
        '<a class="btn btn--green" href="https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(waText) + '" target="_blank" rel="noopener">Send this to us on WhatsApp</a>' +
        '<a class="btn btn--ghost-light" href="contact.html">Send an enquiry instead</a>' +
      '</div></div>';
    if (r.also.length) {
      html += '<div class="result-also"><h3>Also worth a look</h3><ul class="ledger">' +
        r.also.map(function (k) {
          return '<li><a href="' + pageFor(k) + '"><span class="name">' + SERVICES[k].name + '</span><span class="desc">' + SERVICES[k].model + '</span>' + CHEV + '</a></li>';
        }).join("") + '</ul></div>';
    }
    html += '<p class="result-restart"><button type="button" class="linklike" data-restart>Start again</button> &nbsp;or&nbsp; <a class="text-link" href="' + pageFor(r.primary) + '">Read the full ' + p.name + ' details</a></p>';
    result.innerHTML = html;
    result.classList.add("is-active");
    root.hidden = true;
    var t = document.getElementById("result-title");
    if (t) t.focus();
    window.scrollTo({ top: result.getBoundingClientRect().top + window.pageYOffset - 120, behavior: "auto" });
    result.querySelector("[data-restart]").addEventListener("click", function () {
      root.querySelectorAll("input").forEach(function (i) { i.checked = false; });
      result.classList.remove("is-active"); result.innerHTML = "";
      root.hidden = false; show(0);
    });
  }

  nextBtn.addEventListener("click", function () {
    if (!answered(steps[current])) {
      msg.textContent = steps[current].querySelector("input[type='checkbox']") ? "Choose at least one option to continue." : "Choose an option to continue.";
      return;
    }
    if (current < steps.length - 1) show(current + 1);
    else render(compute());
  });
  backBtn.addEventListener("click", function () { if (current > 0) show(current - 1); });

  // single-choice questions advance on selection
  root.addEventListener("change", function (e) {
    if (e.target.type === "radio") {
      msg.textContent = "";
      if (current < steps.length - 1) setTimeout(function () { show(current + 1); }, 220);
    } else { msg.textContent = ""; }
  });

  nav.hidden = false;
  show(0);
  // don't steal focus on first load
  if (document.activeElement && document.activeElement.tagName === "LEGEND") document.activeElement.blur();
})();
