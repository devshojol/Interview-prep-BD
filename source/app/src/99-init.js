
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

  function init() {
    applyPreferences();
    logValidation();

    window.addEventListener('hashchange', () => { closeMobileNav(); render({ focus: true }); });
    $('#menuBtn').addEventListener('click', () => ($('#app').classList.contains('is-nav-open') ? closeMobileNav() : openMobileNav()));
    $('#scrim').addEventListener('click', closeMobileNav);
    $('#collapseBtn').addEventListener('click', () => {
      state.preferences.sidebarCollapsed = !state.preferences.sidebarCollapsed;
      saveState();
      applyPreferences();
    });
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
