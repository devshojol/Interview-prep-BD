
  /* ======================================================================
     Boot
     ====================================================================== */
  function closeMobileNav() {
    const app = $('#app');
    app.classList.remove('is-nav-open');
    const scrim = $('#scrim');
    scrim.classList.remove('is-visible');
    scrim.hidden = true;
    $('#menuBtn').setAttribute('aria-expanded', 'false');
  }
  function openMobileNav() {
    const app = $('#app');
    app.classList.add('is-nav-open');
    const scrim = $('#scrim');
    scrim.hidden = false;
    requestAnimationFrame(() => scrim.classList.add('is-visible'));
    $('#menuBtn').setAttribute('aria-expanded', 'true');
    const first = $('#nav a');
    if (first) first.focus();
  }

  /* Tooltips for [data-tip] elements: mouse hover (after a short delay, instant while "warm") and keyboard focus.
     data-tip-side="right|bottom"; data-tip-collapsed = only while the sidebar is collapsed; data-tip-key = shortcut.
     Purely visual (aria-hidden): every target already has its name as text or aria-label. */
  function initTooltips() {
    const tip = h('div', { class: 'tooltip', 'aria-hidden': 'true' });
    document.body.append(tip);
    let target = null, timer = 0, warmUntil = 0;
    const eligible = (el) => el && el.dataset.tip && (!('tipCollapsed' in el.dataset) || ($('#app').classList.contains('is-collapsed') && window.innerWidth > 860));
    function place(el) {
      const r = el.getBoundingClientRect(), tr = tip.getBoundingClientRect(), gap = 8;
      let x, y;
      if (el.dataset.tipSide === 'right') { x = r.right + gap + 2; y = r.top + r.height / 2 - tr.height / 2; }
      else { x = r.left + r.width / 2 - tr.width / 2; y = r.bottom + gap; }
      x = clamp(x, 6, window.innerWidth - tr.width - 6);
      y = clamp(y, 6, window.innerHeight - tr.height - 6);
      tip.style.transform = 'translate(' + Math.round(x) + 'px,' + Math.round(y) + 'px)';
    }
    function show(el) {
      target = el;
      clear(tip);
      tip.append(el.dataset.tip);
      if (el.dataset.tipKey) tip.append(h('kbd', null, el.dataset.tipKey));
      place(el);
      tip.classList.add('is-visible');
    }
    function hide() {
      clearTimeout(timer);
      if (target) warmUntil = Date.now() + 400;
      target = null;
      tip.classList.remove('is-visible');
    }
    function request(el, immediate) {
      clearTimeout(timer);
      if (!eligible(el)) { hide(); return; }
      if (immediate || Date.now() < warmUntil || target) show(el);
      else timer = setTimeout(() => show(el), 350);
    }
    document.addEventListener('pointerover', (e) => {
      if (e.pointerType !== 'mouse' && e.pointerType !== 'pen') return;
      const el = e.target.closest('[data-tip]');
      if (el && el !== target) request(el, false);
      else if (!el && target) hide();
    });
    document.addEventListener('pointerleave', hide);
    document.addEventListener('focusin', (e) => {
      const el = e.target.closest('[data-tip]');
      if (el && el.matches(':focus-visible')) request(el, true); else hide();
    });
    document.addEventListener('focusout', hide);
    document.addEventListener('pointerdown', hide);
    document.addEventListener('keydown', (e) => { if (e.key !== 'Tab' && e.key !== 'Shift') hide(); });
    window.addEventListener('scroll', hide, true);
    window.addEventListener('hashchange', hide);
  }

  function init() {
    applyPreferences();
    logValidation();

    window.addEventListener('hashchange', () => { closeMobileNav(); render({ focus: true }); });
    $('#menuBtn').addEventListener('click', () => ($('#app').classList.contains('is-nav-open') ? closeMobileNav() : openMobileNav()));
    $('#scrim').addEventListener('click', closeMobileNav);
    initTooltips();
    const toggleSidebar = () => {
      state.preferences.sidebarCollapsed = !state.preferences.sidebarCollapsed;
      saveState();
      applyPreferences();
    };
    $('#collapseBtn').addEventListener('click', toggleSidebar);
    window.addEventListener('resize', debounce(() => {
      $('#app').classList.toggle('is-collapsed', state.preferences.sidebarCollapsed && window.innerWidth > 860);
      if (window.innerWidth > 860) closeMobileNav();
    }, 150));

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && $('#app').classList.contains('is-nav-open')) { closeMobileNav(); $('#menuBtn').focus(); return; }
      if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
      const tg = e.target;
      const tag = tg && tg.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (tg && tg.isContentEditable)) return;
      if ($('#modal').open) return;
      if (e.key === '[' && window.innerWidth > 860) { e.preventDefault(); toggleSidebar(); return; }
      if (e.key === '/' ) {
        e.preventDefault();
        const s = $('#f-q');
        if (s) s.focus(); else go('#/questions?focus=search');
        return;
      }
      // Let focused buttons/links handle Space/Enter natively.
      if ((e.key === ' ' || e.key === 'Enter') && tg && (tag === 'BUTTON' || tag === 'A' || tg.getAttribute('role') === 'button')) return;
      if (ui.keyHandler && ui.keyHandler(e)) e.preventDefault();
    });

    // Keep multiple tabs in sync
    window.addEventListener('storage', (e) => {
      if (e.key !== STORAGE_KEY || e.newValue == null) return;
      try {
        const parsed = JSON.parse(e.newValue);
        const m = migrate(parsed);
        if (!m.incompatible) { state = sanitizeState(m.data); applyPreferences(); rerender(); }
      } catch (err) { /* ignore */ }
    });

    if (storageNotice === 'corrupt') setTimeout(() => toast(tb('storageCorrupt'), 'bad', 7000), 300);
    else if (storageNotice === 'incompatible') setTimeout(() => toast(tb('storageIncompatible'), 'bad', 7000), 300);
    else if (!storageOK) setTimeout(() => toast(tb('storageUnavailable'), 'bad', 7000), 300);

    render({ focus: false });
  }

  // Expose a tiny debug API (read-only helpers) for development and testing.
  window.InterviewPrep = Object.freeze({
    version: APP_VERSION,
    validate: () => validateBank(window.QBANK),
    counts: () => {
      const out = {};
      TECHS.forEach((tc) => { out[tc.id] = Object.assign({ total: BY_TECH.get(tc.id).length }, countBy(BY_TECH.get(tc.id), 'difficulty')); });
      return out;
    },
    getState: () => JSON.parse(JSON.stringify(state)),
    scoreSession: (sess) => summarizeSession(sess),
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
