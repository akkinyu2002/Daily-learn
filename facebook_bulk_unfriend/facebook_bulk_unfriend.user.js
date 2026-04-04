// ==UserScript==
// @name         Facebook Bulk Unfriend Helper
// @namespace    local.fb.bulk.unfriend
// @version      1.3.0
// @description  Select friends in bulk, unselect keep list, then unfriend selected.
// @match        https://www.facebook.com/*
// @match        https://facebook.com/*
// @match        https://m.facebook.com/*
// @run-at       document-idle
// @grant        none
// ==/UserScript==

(function () {
  "use strict";

  if (window.__fbBulkUnfriendLoaded) return;
  window.__fbBulkUnfriendLoaded = true;

  const state = {
    running: false,
    analyzing: false,
    stopRequested: false,
    selectedLinks: new Set(),
    cardByLink: new Map(),
    profileMetaByLink: new Map(),
    autoSelectNew: false,
  };

  const LABELS = {
    friendsButton: ["friends", "friend", "following"],
    menuButton: ["actions for", "more options", "see options", "options"],
    unfriendAction: ["unfriend", "remove friend"],
    confirmAction: ["confirm", "unfriend", "remove"],
  };

  const css = `
#fbu-panel {
  position: fixed;
  top: 76px;
  right: 16px;
  width: 320px;
  z-index: 2147483647;
  background: #ffffff;
  border: 1px solid #d0d7de;
  border-radius: 12px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.2);
  font-family: Arial, sans-serif;
  color: #1f2328;
}
#fbu-panel * { box-sizing: border-box; }
#fbu-panel header {
  padding: 10px 12px;
  border-bottom: 1px solid #e6ebf1;
  font-weight: 700;
  font-size: 14px;
}
#fbu-panel .fbu-body { padding: 10px 12px; }
#fbu-panel .fbu-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}
#fbu-panel button {
  border: 1px solid #d0d7de;
  background: #f6f8fa;
  border-radius: 8px;
  padding: 7px 8px;
  font-size: 12px;
  cursor: pointer;
}
#fbu-panel button:hover { background: #eef2f6; }
#fbu-panel button:disabled { opacity: 0.5; cursor: not-allowed; }
#fbu-panel textarea {
  width: 100%;
  min-height: 90px;
  max-height: 150px;
  resize: vertical;
  border: 1px solid #d0d7de;
  border-radius: 8px;
  padding: 8px;
  font-size: 12px;
  margin-bottom: 8px;
}
#fbu-panel input[type="number"] {
  width: 66px;
  border: 1px solid #d0d7de;
  border-radius: 8px;
  padding: 6px 8px;
  font-size: 12px;
}
#fbu-panel .fbu-inline {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
}
#fbu-status {
  font-size: 12px;
  background: #f6f8fa;
  border: 1px solid #e6ebf1;
  border-radius: 8px;
  padding: 8px;
  white-space: pre-line;
}
.fbu-card-mark {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 20px;
  height: 20px;
  z-index: 20;
}
.fbu-soft-done {
  opacity: 0.45 !important;
}
`;

  injectStyle(css);
  const ui = createPanel();

  setStatus("Ready. Open your Facebook friends page, then scan.");
  periodicScan();

  function injectStyle(text) {
    const el = document.createElement("style");
    el.textContent = text;
    document.documentElement.appendChild(el);
  }

  function normalize(s) {
    return (s || "").replace(/\s+/g, " ").trim();
  }

  function lower(s) {
    return normalize(s).toLowerCase();
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function randomBetween(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function canonicalFriendHref(rawHref) {
    if (!rawHref) return "";

    try {
      const url = new URL(rawHref, window.location.origin);
      const path = (url.pathname || "").toLowerCase();

      if (path === "/profile.php") {
        const id = url.searchParams.get("id");
        if (!id) return "";
        return `${url.origin}/profile.php?id=${id}`;
      }

      const blocked = ["/groups/", "/events/", "/watch/", "/marketplace/", "/stories/", "/reel/"];
      if (blocked.some((p) => path.includes(p))) return "";

      const cleanPath = url.pathname.replace(/\/+$/, "") || "/";
      return `${url.origin}${cleanPath}`;
    } catch (_) {
      return "";
    }
  }

  function withSk(href, sk) {
    try {
      const url = new URL(href, window.location.origin);
      url.searchParams.set("sk", sk);
      return url.toString();
    } catch (_) {
      return href;
    }
  }

  function timelineUrl(href) {
    return withSk(href, "timeline");
  }

  function parseHumanDate(text) {
    const ms = Date.parse(text);
    if (!Number.isFinite(ms)) return null;
    if (ms < new Date("2005-01-01T00:00:00Z").getTime()) return null;
    if (ms > Date.now() + 24 * 60 * 60 * 1000) return null;
    return ms;
  }

  function extractRecentActivityMs(html) {
    if (!html) return null;
    const timestamps = [];
    const minMs = new Date("2005-01-01T00:00:00Z").getTime();
    const maxMs = Date.now() + 24 * 60 * 60 * 1000;

    const pushTime = (raw) => {
      let ms = Number(raw);
      if (!Number.isFinite(ms)) return;
      if (String(Math.trunc(ms)).length <= 10) ms *= 1000;
      if (ms < minMs || ms > maxMs) return;
      timestamps.push(ms);
    };

    // Common server-rendered timestamp marker.
    const dataUtime = /data-utime=["'](\d{10})["']/g;
    let m = null;
    while ((m = dataUtime.exec(html)) !== null) {
      pushTime(m[1]);
    }

    const keyedUnix = /"(?:publish_time|story_creation_time|creation_time|timestamp)"\s*:\s*(\d{10,13})/g;
    while ((m = keyedUnix.exec(html)) !== null) {
      pushTime(m[1]);
    }

    const isoDates = /\b(20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)\b/g;
    while ((m = isoDates.exec(html)) !== null) {
      const ms = parseHumanDate(m[1]);
      if (ms) timestamps.push(ms);
    }

    const longDates = /\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{1,2},\s+20\d{2}\b/gi;
    while ((m = longDates.exec(html)) !== null) {
      const ms = parseHumanDate(m[0]);
      if (ms) timestamps.push(ms);
    }

    const rel = /\b(\d{1,3})\s*(years?|yrs?|months?|mos?|mo|weeks?|days?|hours?|hrs?)\s+ago\b/gi;
    while ((m = rel.exec(html)) !== null) {
      const n = Number(m[1]);
      const unit = lower(m[2]);
      if (!Number.isFinite(n) || n <= 0) continue;

      let delta = 0;
      if (unit.startsWith("year") || unit.startsWith("yr")) delta = n * 365 * 24 * 60 * 60 * 1000;
      else if (unit.startsWith("month") || unit === "mo" || unit.startsWith("mos")) delta = n * 30 * 24 * 60 * 60 * 1000;
      else if (unit.startsWith("week")) delta = n * 7 * 24 * 60 * 60 * 1000;
      else if (unit.startsWith("day")) delta = n * 24 * 60 * 60 * 1000;
      else if (unit.startsWith("hour") || unit.startsWith("hr")) delta = n * 60 * 60 * 1000;
      if (!delta) continue;

      const ms = Date.now() - delta;
      if (ms >= minMs && ms <= maxMs) timestamps.push(ms);
    }

    if (!timestamps.length) return null;

    // If only one very fresh timestamp exists, it can be page metadata instead of activity.
    const sorted = timestamps.sort((a, b) => b - a);
    if (sorted.length <= 2 && sorted[0] > Date.now() - 3 * 24 * 60 * 60 * 1000) {
      return null;
    }

    return Math.max(...timestamps);
  }

  function looksDeactivated(html) {
    if (!html) return false;
    const text = lower(html);
    const flags = [
      "this content isn't available right now",
      "this profile isn't available",
      "the link you followed may be broken",
      "may have been removed",
      "account has been deactivated",
      "facebook user",
    ];
    return flags.some((x) => text.includes(x));
  }

  function looksUnavailableUrl(urlText) {
    const t = lower(urlText || "");
    return t.includes("/checkpoint/") || t.includes("/recover/") || t.includes("/login");
  }

  function isLikelyDeactivatedName(name) {
    const n = lower(name);
    return n === "facebook user" || n === "facebook user.";
  }

  async function fetchProfileMeta(friend) {
    const candidates = [timelineUrl(friend.href), withSk(friend.href, "all_activity"), withSk(friend.href, "posts")];

    let lastActivityMs = null;
    let deactivated = isLikelyDeactivatedName(friend.name);

    for (const url of candidates) {
      try {
        const res = await fetch(url, {
          method: "GET",
          credentials: "include",
          cache: "no-store",
          redirect: "follow",
        });

        const html = await res.text();
        if (looksDeactivated(html) || looksUnavailableUrl(res.url) || res.status >= 400) {
          deactivated = true;
        }

        const ts = extractRecentActivityMs(html);
        if (Number.isFinite(ts) && (!Number.isFinite(lastActivityMs) || ts > lastActivityMs)) {
          lastActivityMs = ts;
        }

        // No need to over-fetch if we already found activity newer than 6 months.
        if (Number.isFinite(lastActivityMs) && lastActivityMs > Date.now() - 180 * 24 * 60 * 60 * 1000) {
          break;
        }
      } catch (_) {
        // Ignore single endpoint failures and keep trying fallbacks.
      }
    }

    return {
      checkedAt: Date.now(),
      deactivated,
      lastActivityMs,
    };
  }

  function isVisible(el) {
    if (!el || !el.isConnected) return false;
    const style = window.getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden" || style.opacity === "0") return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }

  function textMatches(candidate, expectedList) {
    const t = lower(candidate);
    return expectedList.some((kw) => t.includes(lower(kw)));
  }

  function findFriendsButton(scope) {
    const candidates = Array.from(
      scope.querySelectorAll('[role="button"], [aria-label], div[tabindex="0"], a[role="button"]')
    );

    for (const c of candidates) {
      if (!isVisible(c)) continue;
      const combined = `${c.getAttribute("aria-label") || ""} ${c.textContent || ""}`;
      if (textMatches(combined, LABELS.friendsButton)) {
        return c;
      }
    }

    return null;
  }

  function findMenuButton(scope) {
    const candidates = Array.from(
      scope.querySelectorAll('[role="button"], [aria-label], div[tabindex="0"], a[role="button"]')
    );

    for (const c of candidates) {
      if (!isVisible(c)) continue;
      const combined = `${c.getAttribute("aria-label") || ""} ${c.textContent || ""}`;
      if (textMatches(combined, LABELS.menuButton)) {
        return c;
      }
    }

    return null;
  }

  function findFriendCard(link) {
    let node = link;
    for (let depth = 0; depth < 10 && node; depth += 1) {
      node = node.parentElement;
      if (!node || !node.isConnected || !isVisible(node)) continue;

      const rect = node.getBoundingClientRect();
      if (rect.width < 220 || rect.height < 80 || rect.height > 520) continue;

      if (findFriendsButton(node) || findMenuButton(node)) {
        return node;
      }
    }

    return link.closest('div[role="listitem"], div[data-pagelet], li, article') || link.parentElement;
  }

  function parseFriendCards() {
    const links = Array.from(document.querySelectorAll('a[href]'));
    const unique = new Map();

    for (const link of links) {
      if (!isVisible(link)) continue;

      const name = normalize(link.textContent);
      if (!name || name.length < 2) continue;
      if (name.length > 80) continue;

      const href = canonicalFriendHref(link.getAttribute("href") || link.href);
      if (!href) continue;

      const card = findFriendCard(link);
      if (!card || !card.isConnected) continue;

      const hasAction = !!(findFriendsButton(card) || findMenuButton(card));
      if (!hasAction) continue;

      if (!unique.has(href)) {
        unique.set(href, { name, href, card, likelyDeactivated: isLikelyDeactivatedName(name) });
      }
    }

    return Array.from(unique.values());
  }

  function ensureCheckbox(friend) {
    const { card, href } = friend;

    const existing = card.querySelector('input.fbu-card-mark[type="checkbox"]');
    if (existing) return;

    const marker = document.createElement("input");
    marker.type = "checkbox";
    marker.className = "fbu-card-mark";
    marker.title = "Select for unfriend";
    marker.dataset.href = href;

    if (state.selectedLinks.has(href) || state.autoSelectNew) {
      marker.checked = true;
      state.selectedLinks.add(href);
    }

    marker.addEventListener("change", () => {
      if (marker.checked) state.selectedLinks.add(href);
      else state.selectedLinks.delete(href);
      refreshStatus();
    });

    if (getComputedStyle(card).position === "static") {
      card.style.position = "relative";
    }

    card.appendChild(marker);
  }

  function scanVisible() {
    const cards = parseFriendCards();

    for (const friend of cards) {
      state.cardByLink.set(friend.href, friend);
      ensureCheckbox(friend);
    }

    refreshStatus();
    return cards.length;
  }

  async function autoScrollAndScan() {
    setStatus("Auto scrolling and scanning...");

    let stableRounds = 0;
    let lastHeight = -1;

    for (let i = 0; i < 80; i += 1) {
      if (state.stopRequested) break;

      scanVisible();
      window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
      await sleep(1100);

      const h = document.body.scrollHeight;
      if (h === lastHeight) {
        stableRounds += 1;
      } else {
        stableRounds = 0;
        lastHeight = h;
      }

      if (stableRounds >= 4) break;
    }

    scanVisible();
    setStatus("Auto scan complete.");
  }

  function setAllChecked(checked) {
    const boxes = Array.from(document.querySelectorAll('input.fbu-card-mark[type="checkbox"]'));
    for (const box of boxes) {
      box.checked = checked;
      const href = box.dataset.href || "";
      if (!href) continue;

      if (checked) state.selectedLinks.add(href);
      else state.selectedLinks.delete(href);
    }

    refreshStatus();
  }

  function getKeepSet() {
    const rows = ui.keepNames.value
      .split("\n")
      .map((x) => lower(x))
      .filter(Boolean);
    return new Set(rows);
  }

  function unselectKeepNames() {
    const keep = getKeepSet();
    if (!keep.size) {
      setStatus("Keep Names is empty.");
      return;
    }

    const cards = parseFriendCards();
    let changed = 0;

    for (const friend of cards) {
      if (!keep.has(lower(friend.name))) continue;

      const box = friend.card.querySelector('input.fbu-card-mark[type="checkbox"]');
      if (box && box.checked) {
        box.checked = false;
        state.selectedLinks.delete(friend.href);
        changed += 1;
      }
    }

    refreshStatus(`Unselected ${changed} keep-name matches.`);
  }

  function selectDuplicateNames() {
    if (state.running || state.analyzing) return;

    const cards = parseFriendCards();
    if (!cards.length) {
      setStatus("No loaded friend cards found. Scan first.");
      return;
    }

    const keep = getKeepSet();
    const byName = new Map();

    for (const friend of cards) {
      const key = lower(friend.name);
      if (!key) continue;
      if (!byName.has(key)) byName.set(key, []);
      byName.get(key).push(friend);
    }

    let groups = 0;
    let selectedDupes = 0;
    let skippedByKeep = 0;

    for (const [nameKey, group] of byName.entries()) {
      if (group.length < 2) continue;
      groups += 1;

      // If this name is in keep list, skip entire duplicate group.
      if (keep.has(nameKey)) {
        skippedByKeep += group.length;
        continue;
      }

      // Keep the first loaded account and select the rest as duplicates.
      for (let i = 1; i < group.length; i += 1) {
        applySelection(group[i], true);
        selectedDupes += 1;
      }
    }

    refreshStatus(
      `Duplicate scan done. Duplicate groups: ${groups}. Selected duplicates: ${selectedDupes}. Skipped by keep names: ${skippedByKeep}.`
    );
  }

  function monthsToMs(months) {
    return Math.max(1, months) * 30 * 24 * 60 * 60 * 1000;
  }

  function applySelection(friend, checked) {
    const box = friend.card.querySelector('input.fbu-card-mark[type="checkbox"]');
    if (box) box.checked = checked;
    if (checked) state.selectedLinks.add(friend.href);
    else state.selectedLinks.delete(friend.href);
  }

  async function analyzeAndSelectTargets() {
    if (state.running || state.analyzing) return;

    const cards = parseFriendCards();
    if (!cards.length) {
      setStatus("No loaded friend cards found. Scan first.");
      return;
    }

    const includeInactive = !!ui.includeInactive.checked;
    const includeDeactivated = !!ui.includeDeactivated.checked;
    const includeUnknown = !!ui.includeUnknown.checked;
    const unknownAsInactive = !!ui.unknownAsInactive.checked;
    const months = Math.max(1, Number(ui.monthsInput.value) || 6);
    ui.monthsInput.value = String(months);

    if (!includeInactive && !includeDeactivated && !includeUnknown) {
      setStatus("Enable at least one rule: inactive, deactivated, or unknown.");
      return;
    }

    state.analyzing = true;
    state.stopRequested = false;
    toggleButtons();

    const threshold = Date.now() - monthsToMs(months);
    let reviewed = 0;
    let matched = 0;
    let matchedInactive = 0;
    let matchedDeactivated = 0;
    let matchedUnknown = 0;
    let unknown = 0;

    for (const friend of cards) {
      if (state.stopRequested) break;

      setStatus(`Analyzing ${reviewed + 1}/${cards.length}\nNow: ${friend.name}`);

      let meta = state.profileMetaByLink.get(friend.href);
      const cacheAge = meta ? Date.now() - (meta.checkedAt || 0) : Number.POSITIVE_INFINITY;
      if (!meta || cacheAge > 2 * 60 * 60 * 1000) {
        try {
          meta = await fetchProfileMeta(friend);
          state.profileMetaByLink.set(friend.href, meta);
        } catch (_) {
          meta = { checkedAt: Date.now(), deactivated: false, lastActivityMs: null, failed: true };
          state.profileMetaByLink.set(friend.href, meta);
        }
      }

      const isDeactivated = !!meta.deactivated || !!friend.likelyDeactivated;
      const isInactive = Number.isFinite(meta.lastActivityMs) && meta.lastActivityMs < threshold;
      const isUnknown = !Number.isFinite(meta.lastActivityMs) && !isDeactivated;
      if (isUnknown) unknown += 1;

      const includeUnknownAsInactive = includeInactive && unknownAsInactive;
      const shouldSelect =
        (includeDeactivated && isDeactivated) ||
        (includeInactive && isInactive) ||
        (includeUnknown && isUnknown) ||
        (includeUnknownAsInactive && isUnknown);
      if (shouldSelect) {
        applySelection(friend, true);
        matched += 1;
      }

      if (isInactive || (includeUnknownAsInactive && isUnknown)) matchedInactive += 1;
      if (isDeactivated) matchedDeactivated += 1;
      if (isUnknown) matchedUnknown += 1;

      reviewed += 1;
      refreshStatus(
        `Reviewing... ${reviewed}/${cards.length}\nMatched: ${matched} (inactive ${matchedInactive}, deactivated ${matchedDeactivated}, unknown ${matchedUnknown})`
      );

      await sleep(randomBetween(700, 1300));
    }

    state.analyzing = false;
    toggleButtons();

    refreshStatus(
      `Analyze done. Matched ${matched}/${reviewed}. Inactive>${months}m: ${matchedInactive}, Deactivated: ${matchedDeactivated}, Unknown: ${unknown}.`
    );
  }

  function findActionByText(texts, rootSelector) {
    const roots = rootSelector ? Array.from(document.querySelectorAll(rootSelector)) : [document.body];

    for (const root of roots) {
      const candidates = Array.from(
        root.querySelectorAll('[role="menuitem"], [role="button"], div[tabindex="0"], span, a[role="button"]')
      );

      for (const c of candidates) {
        if (!isVisible(c)) continue;
        const combined = `${c.getAttribute("aria-label") || ""} ${c.textContent || ""}`;
        if (textMatches(combined, texts)) {
          return c;
        }
      }
    }

    return null;
  }

  async function clickAction(texts, rootSelector, waitMs) {
    for (let attempt = 0; attempt < 5; attempt += 1) {
      const target = findActionByText(texts, rootSelector);
      if (target) {
        target.click();
        await sleep(waitMs);
        return true;
      }
      await sleep(350);
    }

    return false;
  }

  async function unfriendOne(friend) {
    const actionBtn = findFriendsButton(friend.card) || findMenuButton(friend.card);
    if (!actionBtn) return { ok: false, reason: "friend action button not found" };

    friend.card.scrollIntoView({ behavior: "smooth", block: "center" });
    await sleep(450);

    actionBtn.click();
    await sleep(700);

    const menuClicked = await clickAction(LABELS.unfriendAction, '[role="menu"], [role="dialog"], div[aria-label] ', 700);
    if (!menuClicked) return { ok: false, reason: "unfriend menu item not found" };

    const confirmClicked = await clickAction(LABELS.confirmAction, '[role="dialog"], [aria-label*="Confirm"], [aria-label*="Unfriend"]', 900);
    if (!confirmClicked) {
      await sleep(800);
      // final fallback: click visible button with confirm labels anywhere
      const fallback = await clickAction(LABELS.confirmAction, null, 900);
      if (!fallback) return { ok: false, reason: "confirm action not found" };
    }

    await sleep(randomBetween(1200, 2200));

    const box = friend.card.querySelector('input.fbu-card-mark[type="checkbox"]');
    if (box) box.checked = false;
    state.selectedLinks.delete(friend.href);
    friend.card.classList.add("fbu-soft-done");

    return { ok: true };
  }

  async function runBulkUnfriend() {
    if (state.running || state.analyzing) return;

    const targets = parseFriendCards().filter((f) => state.selectedLinks.has(f.href));
    if (!targets.length) {
      setStatus("No selected friends found on currently loaded cards.");
      return;
    }

    const shouldRun = window.confirm(
      `Unfriend ${targets.length} selected friends? This cannot be undone automatically.`
    );
    if (!shouldRun) return;

    state.running = true;
    state.stopRequested = false;
    toggleButtons();

    let done = 0;
    let failed = 0;

    for (const friend of targets) {
      if (state.stopRequested) break;

      setStatus(`Working... ${done + failed + 1}/${targets.length}\nNow: ${friend.name}`);

      try {
        const result = await unfriendOne(friend);
        if (result.ok) done += 1;
        else failed += 1;
      } catch (err) {
        failed += 1;
      }

      refreshStatus(`Progress: ${done} success, ${failed} failed.`);
    }

    state.running = false;
    toggleButtons();
    refreshStatus(`Finished. ${done} success, ${failed} failed.`);
  }

  function stopRun() {
    state.stopRequested = true;
    setStatus("Stop requested. Finishing current action...");
  }

  function toggleButtons() {
    const busy = state.running || state.analyzing;
    ui.unfriendBtn.disabled = busy;
    ui.autoScanBtn.disabled = busy;
    ui.scanBtn.disabled = busy;
    ui.selectAllBtn.disabled = busy;
    ui.clearBtn.disabled = busy;
    ui.unselectKeepBtn.disabled = busy;
    ui.analyzeBtn.disabled = busy;
    ui.duplicateBtn.disabled = busy;
    ui.includeInactive.disabled = busy;
    ui.includeDeactivated.disabled = busy;
    ui.includeUnknown.disabled = busy;
    ui.unknownAsInactive.disabled = busy;
    ui.monthsInput.disabled = busy;
    ui.stopBtn.disabled = !busy;
  }

  function refreshStatus(extraLine) {
    const loaded = state.cardByLink.size;
    const selected = state.selectedLinks.size;
    const lines = [
      `Loaded cards: ${loaded}`,
      `Selected: ${selected}`,
      `Running: ${state.running ? "yes" : "no"}`,
      `Analyzing: ${state.analyzing ? "yes" : "no"}`,
    ];
    if (extraLine) lines.push(extraLine);
    ui.status.textContent = lines.join("\n");
  }

  function setStatus(text) {
    ui.status.textContent = text;
  }

  function periodicScan() {
    const tick = () => {
      if (!state.running && !state.analyzing) {
        scanVisible();
      }
      window.setTimeout(tick, 3500);
    };
    window.setTimeout(tick, 3500);
  }

  function createPanel() {
    const panel = document.createElement("section");
    panel.id = "fbu-panel";

    panel.innerHTML = `
<header>FB Bulk Unfriend</header>
<div class="fbu-body">
  <div class="fbu-row">
    <button id="fbu-scan">Scan Visible</button>
    <button id="fbu-auto-scan">Auto Scroll + Scan</button>
  </div>
  <div class="fbu-row">
    <label class="fbu-inline"><input id="fbu-rule-inactive" type="checkbox" checked>Inactive</label>
    <input id="fbu-months" type="number" min="1" max="36" value="6" title="Inactive for N months">
    <label class="fbu-inline"><input id="fbu-rule-deactivated" type="checkbox" checked>Deactivated</label>
  </div>
  <div class="fbu-row">
    <label class="fbu-inline"><input id="fbu-rule-unknown" type="checkbox">Unknown</label>
    <label class="fbu-inline"><input id="fbu-unknown-as-inactive" type="checkbox" checked>Hidden=>Inactive</label>
  </div>
  <div class="fbu-row">
    <button id="fbu-analyze">Find & Select Targets</button>
    <button id="fbu-select-duplicates">Select Duplicate Names</button>
  </div>
  <div class="fbu-row">
    <button id="fbu-select-all">Select All</button>
    <button id="fbu-clear">Clear</button>
  </div>
  <textarea id="fbu-keep-names" placeholder="Keep Names (one per line)"></textarea>
  <div class="fbu-row">
    <button id="fbu-unselect-keep">Unselect Keep Names</button>
  </div>
  <div class="fbu-row">
    <button id="fbu-unfriend" style="background:#c62828;color:white;border-color:#a32020;">Unfriend Selected</button>
    <button id="fbu-stop">Stop</button>
  </div>
  <div id="fbu-status"></div>
</div>`;

    document.body.appendChild(panel);

    const refs = {
      scanBtn: panel.querySelector("#fbu-scan"),
      autoScanBtn: panel.querySelector("#fbu-auto-scan"),
      includeInactive: panel.querySelector("#fbu-rule-inactive"),
      monthsInput: panel.querySelector("#fbu-months"),
      includeDeactivated: panel.querySelector("#fbu-rule-deactivated"),
      includeUnknown: panel.querySelector("#fbu-rule-unknown"),
      unknownAsInactive: panel.querySelector("#fbu-unknown-as-inactive"),
      analyzeBtn: panel.querySelector("#fbu-analyze"),
      duplicateBtn: panel.querySelector("#fbu-select-duplicates"),
      selectAllBtn: panel.querySelector("#fbu-select-all"),
      clearBtn: panel.querySelector("#fbu-clear"),
      keepNames: panel.querySelector("#fbu-keep-names"),
      unselectKeepBtn: panel.querySelector("#fbu-unselect-keep"),
      unfriendBtn: panel.querySelector("#fbu-unfriend"),
      stopBtn: panel.querySelector("#fbu-stop"),
      status: panel.querySelector("#fbu-status"),
    };

    refs.scanBtn.addEventListener("click", () => {
      const n = scanVisible();
      refreshStatus(`Scanned ${n} cards from current viewport.`);
    });

    refs.autoScanBtn.addEventListener("click", async () => {
      state.stopRequested = false;
      await autoScrollAndScan();
    });

    refs.analyzeBtn.addEventListener("click", analyzeAndSelectTargets);
    refs.duplicateBtn.addEventListener("click", selectDuplicateNames);

    refs.selectAllBtn.addEventListener("click", () => {
      state.autoSelectNew = true;
      setAllChecked(true);
    });

    refs.clearBtn.addEventListener("click", () => {
      state.autoSelectNew = false;
      setAllChecked(false);
    });

    refs.unselectKeepBtn.addEventListener("click", unselectKeepNames);
    refs.unfriendBtn.addEventListener("click", runBulkUnfriend);
    refs.stopBtn.addEventListener("click", stopRun);

    refs.stopBtn.disabled = true;

    return refs;
  }
})();

