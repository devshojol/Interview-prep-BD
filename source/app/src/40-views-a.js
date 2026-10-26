
  /* ======================================================================
     UI state (in-memory, not persisted)
     ====================================================================== */
  const ui = {
    nonce: 0,
    explorer: { q: '', tech: '', diff: '', type: '', market: '', bookmarked: false, incorrect: false, unanswered: false, learned: false, review: false, sort: 'default', page: 1 },
    navList: null,
    navLabel: '',
    revealed: new Set(),
    hidden: new Set(),
    mcq: {},
    techs: { q: '', sort: 'default', group: 'all' },
    incorrectTab: 'incorrect',
    timers: [],
    keyHandler: null,
    lastPath: null,
    voiceRead: null, // last thing auto-read, so re-renders don't repeat it
  };
  function stopTimers() { ui.timers.forEach((id) => clearInterval(id)); ui.timers = []; ui.keyHandler = null; }

  /* ======================================================================
     Layout: sidebar, topbar, theme, language
     ====================================================================== */
  const NAV = [
    { group: 'navLearn', items: [['dashboard', 'dashboard', 'nav_dashboard'], ['technologies', 'layers', 'nav_technologies'], ['questions', 'list', 'nav_questions'], ['flashcards', 'cards', 'nav_flashcards'], ['daily', 'zap', 'nav_daily']] },
    { group: 'navPractice', items: [['practice', 'play', 'nav_practice'], ['interview', 'mic', 'nav_interview']] },
    { group: 'navProgress', items: [['bookmarks', 'bookmark', 'nav_bookmarks'], ['incorrect', 'xcircle', 'nav_incorrect'], ['review', 'rotate', 'nav_review'], ['history', 'clock', 'nav_history'], ['planner', 'calendar', 'nav_planner']] },
    { group: 'navMore', items: [['blog', 'article', 'nav_blog'], ['sources', 'book', 'nav_sources'], ['settings', 'settings', 'nav_settings']] },
  ];
  function activeNav(route) {
    if (route.name === 'q') return 'questions';
    if (route.name === 'session') return state.activeSession && state.activeSession.kind === 'interview' ? 'interview' : state.activeSession && state.activeSession.kind === 'daily' ? 'daily' : 'practice';
    if (route.name === 'results') return 'history';
    return route.name;
  }
  function navBadge(key) {
    if (key === 'bookmarks') return state.bookmarks.filter((id) => QMAP.has(id)).length;
    if (key === 'incorrect') return QUESTIONS.filter((q) => statusOf(q.id) === 'incorrect').length;
    if (key === 'review') return new Set(dueIds().concat(state.reviewQuestions.filter((id) => QMAP.has(id)))).size;
    return 0;
  }
  function renderNav(route) {
    const nav = $('#nav');
    clear(nav);
    const cur = activeNav(route);
    const L = lang();
    for (const g of NAV) {
      nav.append(h('div', { class: 'nav-group-label' }, t(g.group)));
      for (const [key, ic, label] of g.items) {
        const n = navBadge(key);
        // The blog is static HTML beside the app, not a hash route; file:// has no directory index.
        const href = key === 'blog' ? (location.protocol === 'file:' ? 'blog/index.html' : 'blog/') : '#/' + key;
        nav.append(h('a', { class: 'nav-link', href, 'aria-current': cur === key ? 'page' : null, 'data-tip': t(label) + (n ? ' · ' + n : ''), 'data-tip-side': 'right', 'data-tip-collapsed': '' },
          icon(ic, 18),
          h('span', { class: 'nav-label' },
            h('span', { lang: L === 'bn' ? 'bn' : 'en', class: L === 'bn' ? 'bn' : null }, t(label)),
            L === 'both' ? h('small', { lang: 'bn' }, tLang(label, 'bn')) : null),
          n ? h('span', { class: 'nav-badge', 'aria-label': n + ' ' + t('items') }, n) : null));
      }
    }
    const techWrap = $('#sidebarTechs');
    clear(techWrap);
    techWrap.append(h('div', { class: 'nav-group-label' }, t('navTechs')));
    const curTech = route.name === 'questions' ? ui.explorer.tech : (route.name === 'q' && QMAP.get(route.params[0]) ? QMAP.get(route.params[0]).technology : '');
    for (const tc of TECHS) {
      const list = BY_TECH.get(tc.id);
      const st = statsFor(list);
      techWrap.append(h('a', { class: 'tech-link', href: '#/questions?tech=' + tc.id, 'aria-current': curTech === tc.id ? 'page' : null, 'data-tip': tc.name + ' · ' + list.length + ' ' + t('questionsWord') + ' · ' + Math.round(st.completion * 100) + '%', 'data-tip-side': 'right', 'data-tip-collapsed': '' },
        techLogo(tc, 'sm'),
        h('span', { class: 'tech-name' }, tc.name),
        h('span', { class: 'mini-progress', 'aria-hidden': 'true' }, h('i', { style: { width: Math.round(st.completion * 100) + '%' } }))));
    }
    const foot = $('#sidebarFoot');
    clear(foot);
    foot.append(h('div', null, t('localOnlyShort')), h('div', null, 'v' + APP_VERSION + ' · ' + t('verifiedOn', { date: VERIFIED_AT })));
  }

  function renderTopbar(title) {
    const tt = $('#pageTitle');
    clear(tt);
    if (title) append(tt, title);
    const act = $('#topbarActions');
    clear(act);
    act.append(
      h('a', { class: 'icon-btn hide-sm', href: '#/questions', 'aria-label': t('searchQuestions'), 'aria-keyshortcuts': '/', 'data-tip': t('searchQuestions'), 'data-tip-key': '/' }, icon('search', 18)),
      seg([
        { value: 'en', label: 'EN', lang: 'en' },
        { value: 'bn', label: 'বাংলা', lang: 'bn' },
        { value: 'both', label: lang() === 'bn' ? 'দুটোই' : 'Both' },
      ], lang(), setLang, t('language')),
      h('button', { class: 'icon-btn', type: 'button', 'aria-label': state.preferences.theme === 'dark' ? t('lightTheme') : t('darkTheme'), 'data-tip': state.preferences.theme === 'dark' ? t('lightTheme') : t('darkTheme'), onclick: () => setTheme(state.preferences.theme === 'dark' ? 'light' : 'dark') },
        icon(state.preferences.theme === 'dark' ? 'sun' : 'moon', 18)));
  }

  function applyPreferences() {
    const p = state.preferences;
    const root = document.documentElement;
    root.setAttribute('data-theme', p.theme);
    root.setAttribute('lang', p.lang === 'bn' ? 'bn' : 'en');
    if (p.motion === 'system') root.removeAttribute('data-motion'); else root.setAttribute('data-motion', p.motion);
    root.style.setProperty('--fs', (15 * p.fontScale) + 'px');
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', p.theme === 'dark' ? '#0B1020' : '#F5F6FB');
    $('#app').classList.toggle('is-collapsed', p.sidebarCollapsed && window.innerWidth > 860);
    const cb = $('#collapseBtn');
    if (cb) {
      const label = p.sidebarCollapsed ? t('expandSidebar') : t('collapseSidebar');
      cb.setAttribute('aria-expanded', String(!p.sidebarCollapsed));
      cb.setAttribute('aria-label', label);
      cb.setAttribute('data-tip', label);
    }
    const skip = $('.skip-link');
    if (skip) skip.textContent = t('skipToContent');
  }
  function setLang(l) {
    if (!['en', 'bn', 'both'].includes(l) || l === state.preferences.lang) return;
    state.preferences.lang = l;
    saveState();
    applyPreferences();
    rerender();
  }
  function setTheme(th) {
    state.preferences.theme = th;
    saveState();
    applyPreferences();
    renderTopbar($('#pageTitle').textContent);
  }
  function prefersReducedMotion() {
    if (state.preferences.motion === 'reduce') return true;
    if (state.preferences.motion === 'full') return false;
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /* ======================================================================
     Router
     ====================================================================== */
  function parseRoute() {
    const raw = location.hash.replace(/^#\/?/, '');
    const qi = raw.indexOf('?');
    const path = qi >= 0 ? raw.slice(0, qi) : raw;
    const qs = qi >= 0 ? raw.slice(qi + 1) : '';
    const parts = path.split('/').filter(Boolean).map((p) => { try { return decodeURIComponent(p); } catch (e) { return p; } });
    return { name: parts[0] || 'dashboard', params: parts.slice(1), query: new URLSearchParams(qs) };
  }
  function go(hash) {
    if (location.hash === hash) render({ focus: true });
    else location.hash = hash;
  }
  let currentRoute = null;
  function render(opts) {
    const o = opts || {};
    const route = parseRoute();
    currentRoute = route;
    if (o.focus) ui.nonce++;
    stopTimers();
    const pathKey = route.name + '/' + route.params.join('/');
    if (ui.lastPath && ui.lastPath !== pathKey) stopSpeaking();
    ui.lastPath = pathKey;
    const VIEWS = {
      dashboard: viewDashboard, technologies: viewTechnologies, questions: viewQuestions, q: viewQuestion,
      practice: viewPractice, session: viewSession, results: viewResults, interview: viewInterview,
      bookmarks: viewBookmarks, incorrect: viewIncorrect, review: viewReview, history: viewHistory,
      planner: viewPlanner, settings: viewSettings, flashcards: viewFlashcards, daily: viewDaily, sources: viewSources,
    };
    const view = VIEWS[route.name] || viewNotFound;
    let out;
    try { out = view(route); } catch (err) {
      console.error(err);
      out = { title: t('errorTitle'), node: emptyState('alert', 'errorTitle', 'errorText', [linkBtn('#/dashboard', t('nav_dashboard'), 'btn--primary')]) };
    }
    if (!out) return; // view redirected
    const main = $('#main');
    clear(main);
    main.className = 'view' + (out.narrow ? ' view--narrow' : '');
    main.append(out.node);
    document.title = (out.titleText || tLang('nav_' + route.name, 'en') || 'Interview Prep BD').toString().replace(/^nav_.*/, 'Interview Prep BD').replace(/[`*]/g, '') + ' · Interview Prep BD';
    renderNav(route);
    renderTopbar(out.title || null);
    if (o.focus) {
      window.scrollTo(0, 0);
      main.focus({ preventScroll: true });
    }
    if (out.after) out.after();
  }
  function rerender() {
    const y = window.scrollY;
    render();
    window.scrollTo(0, y);
  }
  function viewNotFound() {
    return { title: t('notFound'), node: emptyState('alert', 'notFound', 'notFoundText', [linkBtn('#/dashboard', t('nav_dashboard'), 'btn--primary')]) };
  }

  function pageHead(titleKey, leadKey, actions, meta) {
    return h('div', { class: 'page-head' },
      h('div', null,
        h('h1', null, tb(titleKey)),
        leadKey ? h('p', { class: 'lead' }, tb(leadKey)) : null,
        meta ? h('p', { class: 'meta-line mt-1' }, meta) : null),
      actions ? h('div', { class: 'btn-row' }, actions) : null);
  }

  /* ======================================================================
     Dashboard
     ====================================================================== */
  function continueTarget() {
    if (state.activeSession) return { href: '#/session', label: t('resumeSession') };
    let tech = null, latest = 0;
    for (const id of Object.keys(state.questionProgress)) {
      const q = QMAP.get(id);
      if (!q) continue;
      const at = lastAt(id);
      if (at > latest) { latest = at; tech = q.technology; }
    }
    const pool = tech ? BY_TECH.get(tech) : BY_TECH.get('javascript');
    const prioRank = { high: 0, medium: 1, low: 2 };
    const next = (pool || QUESTIONS).filter((q) => !isAnswered(q.id) && !isLearned(q.id))
      .sort((a, b) => (DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty)) || (prioRank[a.priority] - prioRank[b.priority]) || a._order - b._order)[0]
      || QUESTIONS.find((q) => !isAnswered(q.id) && !isLearned(q.id)) || QUESTIONS[0];
    if (!next) return { href: '#/questions', label: t('continueLearning') };
    ui.navList = (pool || QUESTIONS).map((q) => q.id);
    return { href: '#/q/' + encodeURIComponent(next.id), label: t('continueLearning') };
  }

  function viewDashboard() {
    const all = statsFor(QUESTIONS);
    const streak = streakInfo();
    const isNew = all.attempted === 0 && !state.sessions.length && !state.bookmarks.length && !state.learnedQuestions.length;
    const cont = continueTarget();
    const due = dueIds();
    const needsReview = new Set(due.concat(state.reviewQuestions.filter((id) => QMAP.has(id)))).size;
    const today = streak.today;
    const target = state.planner.dailyTarget;

    const hero = h('section', { class: 'hero' },
      h('h1', null, tb(isNew ? 'welcomeNew' : 'welcomeBack')),
      h('p', null, tb('welcomeText', { n: QUESTIONS.length, t: TECHS.filter((x) => x.group !== 'career').length })),
      h('div', { class: 'btn-row mt-2' },
        linkBtn(cont.href, cont.label, 'btn--primary', state.activeSession ? 'play' : 'book'),
        linkBtn('#/practice', t('startPractice'), 'btn--secondary', 'target'),
        linkBtn('#/daily', t('nav_daily'), 'btn--ghost', 'zap')));

    if (!QUESTIONS.length) {
      return { title: tb('nav_dashboard', null, { inline: true }), node: frag(hero, h('div', { class: 'mt-3' }, emptyState('database', 'bankEmpty', 'bankEmptyText'))) };
    }

    const gettingStarted = isNew ? h('section', { class: 'card card--pad-lg mt-3' },
      h('div', { class: 'card__head' }, h('h2', null, tb('gettingStarted'))),
      h('ol', { class: 'steps' }, ['gs1', 'gs2', 'gs3', 'gs4'].map((k) => h('li', null, h('div', null, tb(k))))),
      h('p', { class: 'small muted mt-2 mb-0' }, tb('localOnlyLong'))) : null;

    const stats = h('section', { class: 'grid grid--stats mt-3', 'aria-label': t('yourStats') },
      stat(t('statTotal'), String(QUESTIONS.length), { hint: TECHS.filter((x) => x.group !== 'career').length + ' ' + t('technologiesWord') }),
      stat(t('statAnswered'), String(all.answered), { hint: t('ofTotal', { n: QUESTIONS.length }) }),
      stat(t('res_correct'), String(all.correct), { tone: 'ok' }),
      stat(t('res_partial'), String(all.partial), { tone: 'partial' }),
      stat(t('res_incorrect'), String(all.incorrect), { tone: 'bad' }),
      stat(t('accuracy'), pct(all.accuracy), { hint: t('accuracyHint') }),
      stat(t('weightedScore'), pct(all.weighted), { hint: t('weightedHint') }),
      stat(t('completion'), pct(all.completion), { hint: all.completed + ' / ' + all.total }),
      stat(t('nav_bookmarks'), String(all.bookmarked), null),
      stat(t('needsReview'), String(needsReview), { hint: t('dueToday', { n: due.length }) }),
      stat(t('studyStreak'), t('daysN', { n: streak.current }), { hint: t('bestStreak', { n: streak.best }) }));

    // Today's goal + recent sessions
    const goal = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('todaysGoal')), linkBtn('#/planner', t('nav_planner'), 'btn--ghost btn--sm', 'calendar')),
      h('div', { class: 'row row--between mb-1' }, h('strong', { style: { fontSize: '1.4rem' } }, today + ' / ' + target), h('span', { class: 'muted small' }, t('activitiesToday'))),
      progressBar(today / target, { lg: true, label: t('todaysGoal') }),
      h('p', { class: 'small muted mt-1 mb-0' }, today >= target ? tb('goalDone') : tb('goalLeft', { n: target - today })));

    const recent = state.sessions.slice(-5).reverse();
    const recentCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('recentSessions')), linkBtn('#/history', t('viewAll'), 'btn--ghost btn--sm')),
      recent.length ? h('ul', { class: 'list-plain' }, recent.map((s) => {
        const sm = s.summary || summarizeSession(s);
        return h('li', null,
          h('a', { href: '#/results/' + encodeURIComponent(s.id), class: 'row row--between', style: { width: '100%', color: 'inherit' } },
            h('span', null, h('strong', null, t('kind_' + s.kind)), h('span', { class: 'muted small' }, ' · ' + fmtDate(s.endedAt, true))),
            h('span', { class: 'row' }, h('span', { class: 'badge badge--primary' }, pct(sm.weighted)), h('span', { class: 'small muted' }, sm.total + ' ' + t('qShort')))));
      })) : h('p', { class: 'muted small mb-0' }, tb('noSessionsYet')));

    // Technology progress
    const techBars = h('div', { class: 'bars' }, TECHS.map((tc) => {
      const st = statsFor(BY_TECH.get(tc.id));
      return h('div', { class: 'bar-row' },
        h('a', { class: 'bar-row__label', href: '#/questions?tech=' + tc.id }, techLogo(tc, 'sm'), tc.name),
        progressBar(st.completion, { thin: true, label: tc.name + ' ' + t('completion') }),
        h('span', { class: 'bar-row__value' }, st.completed + '/' + st.total));
    }));
    const techCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('techProgress')), h('span', { class: 'card__sub' }, t('completionLegend'))),
      techBars);

    // Difficulty distribution
    const bankDiff = countBy(QUESTIONS, 'difficulty');
    const diffCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('difficultyDist'))),
      h('div', { class: 'stacked-bar', role: 'img', 'aria-label': DIFFS.map((d) => t('diff_' + d) + ' ' + (bankDiff[d] || 0)).join(', ') },
        DIFFS.map((d) => h('span', { style: { width: ((bankDiff[d] || 0) / QUESTIONS.length * 100) + '%', background: 'var(--' + d + ')' }, title: t('diff_' + d) + ': ' + (bankDiff[d] || 0) }))),
      h('div', { class: 'legend' }, DIFFS.map((d) => h('span', null, h('i', { style: { background: 'var(--' + d + ')' } }), t('diff_' + d) + ' · ' + (bankDiff[d] || 0)))),
      h('div', { class: 'table-wrap mt-2', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
        h('caption', { class: 'sr-only' }, t('difficultyDist')),
        h('thead', null, h('tr', null, h('th', null, t('difficulty')), h('th', { class: 'num' }, t('questionsWord')), h('th', { class: 'num' }, t('statAnswered')), h('th', { class: 'num' }, t('accuracy')), h('th', { class: 'num' }, t('pointsEach')))),
        h('tbody', null, DIFFS.map((d) => {
          const bd = all.byDiff[d];
          return h('tr', null, h('td', null, diffBadge(d)), h('td', { class: 'num' }, bd.total), h('td', { class: 'num' }, bd.answered), h('td', { class: 'num' }, pct(bd.answered ? bd.correct / bd.answered : null)), h('td', { class: 'num' }, POINTS[d]));
        })))),
      h('p', { class: 'small muted mt-1 mb-0' }, tb('extremeNote')));

    const weak = weakAreas(5);
    const weakCard = weak.length ? h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('weakTopics')), linkBtn('#/planner', t('seePlan'), 'btn--ghost btn--sm')),
      weakList(weak)) : null;

    const daily = dailyInfo();
    const dailyCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('nav_daily')), h('span', { class: 'badge badge--teal' }, localDateKey())),
      h('p', { class: 'muted small' }, tb(daily.done ? 'dailyDoneShort' : 'dailyIntroShort', { score: pct(daily.score) })),
      h('div', { class: 'btn-row' }, linkBtn('#/daily', daily.done ? t('viewChallenge') : t('startChallenge'), daily.done ? 'btn--ghost' : 'btn--secondary', 'zap')));

    const node = frag(
      hero,
      storageBanner(),
      gettingStarted,
      stats,
      h('div', { class: 'grid grid--3 mt-3' }, goal, dailyCard, recentCard),
      h('div', { class: 'grid grid--2 dash-split mt-3' }, techCard, h('div', { class: 'stack' }, diffCard, weakCard)));
    return { title: tb('nav_dashboard', null, { inline: true }), titleText: 'Dashboard', node };
  }
  function storageBanner() {
    if (!storageNotice && storageOK) return null;
    const key = storageNotice === 'corrupt' ? 'storageCorrupt' : storageNotice === 'incompatible' ? 'storageIncompatible' : 'storageUnavailable';
    return h('div', { class: 'callout callout--warn mt-2', role: 'alert' }, h('div', { class: 'callout__title' }, icon('alert', 16), tb('storageNoticeTitle')), h('div', { class: 'small' }, tb(key)));
  }
  function weakList(weak) {
    return h('ul', { class: 'list-plain' }, weak.map((g) => {
      const tc = TECH_MAP.get(g.tech);
      return h('li', { class: 'row row--between', style: { width: '100%' } },
        h('span', { class: 'row', style: { minWidth: 0 } }, techLogo(tc, 'sm'), h('span', null, h('strong', null, g.subtopic), h('span', { class: 'muted small' }, ' · ' + tc.name))),
        h('span', { class: 'row' },
          h('span', { class: 'badge badge--bad', title: t('missRate') }, t('missRateShort', { n: Math.round(g.missRate * 100) })),
          btn(t('practice'), () => startQuickSession(Array.from(g.ids), 'practice', { label: g.subtopic }), 'btn--sm btn--secondary', 'play')));
    }));
  }

  /* ======================================================================
     Technology explorer
     ====================================================================== */
  function viewTechnologies() {
    const f = ui.techs;
    const grid = h('div', { class: 'grid grid--auto' });
    const countEl = h('p', { class: 'results-count', 'aria-live': 'polite' });
    function update() {
      clear(grid);
      const terms = searchTerms(f.q);
      let list = TECHS.map((tc) => ({ tc, list: BY_TECH.get(tc.id), st: statsFor(BY_TECH.get(tc.id)) }));
      if (terms.length) list = list.filter((x) => terms.every((term) => normalizeText(x.tc.name + ' ' + x.tc.desc.en + ' ' + x.tc.desc.bn + ' ' + x.tc.group).includes(term)));
      if (f.group !== 'all') list = list.filter((x) => x.tc.group === f.group);
      if (f.sort === 'name') list.sort((a, b) => a.tc.name.localeCompare(b.tc.name));
      else if (f.sort === 'count') list.sort((a, b) => b.list.length - a.list.length);
      else if (f.sort === 'progressDesc') list.sort((a, b) => b.st.completion - a.st.completion);
      else if (f.sort === 'progressAsc') list.sort((a, b) => a.st.completion - b.st.completion);
      clear(countEl);
      countEl.append(h('strong', null, String(list.length)), ' ', t('categoriesWord'));
      if (!list.length) { grid.append(emptyState('search', 'noTechMatch', 'tryDifferent')); return; }
      for (const { tc, list: qs, st } of list) {
        const dc = countBy(qs, 'difficulty');
        grid.append(h('article', { class: 'card card--interactive tech-card' },
          h('div', { class: 'tech-card__head' }, techLogo(tc),
            h('div', { style: { minWidth: 0 } }, h('h2', { class: 'tech-card__title' }, tc.name), h('div', { class: 'tech-card__ver' }, tc.version))),
          h('p', { class: 'tech-card__desc' + (lang() === 'bn' ? ' bn' : ''), lang: lang() === 'bn' ? 'bn' : 'en' }, lang() === 'bn' ? tc.desc.bn : tc.desc.en),
          lang() === 'both' ? h('p', { class: 'tech-card__desc bn small muted', lang: 'bn', style: { minHeight: 0 } }, tc.desc.bn) : null,
          h('div', { class: 'row row--between small' }, h('span', null, h('strong', null, qs.length), ' ', t('questionsWord')), h('span', { class: 'muted' }, pct(st.completion) + ' ' + t('completeWord'))),
          h('div', { class: 'diff-counts' }, DIFFS.map((d) => h('div', { class: 'diff-count diff-count--' + d }, h('b', null, dc[d] || 0), h('span', null, t('diff_' + d))))),
          progressBar(st.completion, { thin: true, label: tc.name + ' ' + t('completion') }),
          h('div', { class: 'btn-row' },
            linkBtn('#/questions?tech=' + tc.id, t('startLearning'), 'btn--secondary btn--sm', 'book'),
            btn(t('practice'), () => { practiceDefaults().techs = [tc.id]; go('#/practice'); }, 'btn--ghost btn--sm', 'play'))));
      }
    }
    const search = h('input', { class: 'input', type: 'search', placeholder: t('searchTechs'), value: f.q, 'aria-label': t('searchTechs'), oninput: debounce((e) => { f.q = e.target.value; update(); }, 120) });
    const sortSel = h('select', { class: 'select', 'aria-label': t('sortBy'), onchange: (e) => { f.sort = e.target.value; update(); } },
      [['default', 'sortDefault'], ['name', 'sortName'], ['count', 'sortCount'], ['progressDesc', 'sortProgressDesc'], ['progressAsc', 'sortProgressAsc']].map(([v, k]) => h('option', { value: v, selected: f.sort === v }, t(k))));
    const groups = seg(['all'].concat(TECH_GROUPS).map((g) => ({ value: g, label: t('group_' + g) })), f.group, (g) => { f.group = g; rerender(); }, t('filterGroup'));
    update();
    const node = frag(
      pageHead('nav_technologies', 'techLead'),
      h('div', { class: 'card card--flat' },
        h('div', { class: 'filters filters--2' },
          h('div', { class: 'field field--search' }, h('label', null, t('search')), h('div', { class: 'search-box' }, icon('search', 16), search)),
          h('div', { class: 'field' }, h('label', null, t('sortBy')), sortSel)),
        h('div', { class: 'filters__more' }, h('span', { class: 'field-label' }, t('filterGroup')), groups)),
      h('div', { class: 'results-bar' }, countEl),
      grid);
    return { title: tb('nav_technologies', null, { inline: true }), titleText: 'Technologies', node };
  }

  /* ======================================================================
     Question explorer
     ====================================================================== */
  function filterQuestions(f) {
    let list = QUESTIONS;
    if (f.tech) list = list.filter((q) => q.technology === f.tech);
    if (f.diff) list = list.filter((q) => q.difficulty === f.diff);
    if (f.type) list = list.filter((q) => q.type === f.type);
    if (f.market) list = list.filter((q) => q.market === f.market);
    if (f.bookmarked) list = list.filter((q) => isBookmarked(q.id));
    if (f.incorrect) list = list.filter((q) => statusOf(q.id) === 'incorrect');
    if (f.unanswered) list = list.filter((q) => !isAnswered(q.id));
    if (f.learned) list = list.filter((q) => isLearned(q.id));
    if (f.review) { const due = new Set(dueIds()); list = list.filter((q) => isFlagged(q.id) || due.has(q.id)); }
    const terms = searchTerms(f.q);
    let scored = null;
    if (terms.length) {
      scored = new Map();
      list = list.filter((q) => { const s = searchScore(q, terms); if (s) scored.set(q.id, s); return s > 0; });
    }
    const prioRank = { high: 0, medium: 1, low: 2 };
    list = list.slice();
    if (f.sort === 'diffAsc') list.sort((a, b) => DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty) || a._order - b._order);
    else if (f.sort === 'diffDesc') list.sort((a, b) => DIFFS.indexOf(b.difficulty) - DIFFS.indexOf(a.difficulty) || a._order - b._order);
    else if (f.sort === 'priority') list.sort((a, b) => prioRank[a.priority] - prioRank[b.priority] || a._order - b._order);
    else if (f.sort === 'recent') list.sort((a, b) => (lastAt(b.id) - lastAt(a.id)) || a._order - b._order);
    else if (scored) list.sort((a, b) => scored.get(b.id) - scored.get(a.id) || a._order - b._order);
    return list;
  }
  function syncExplorerHash() {
    const f = ui.explorer;
    const qs = f.tech ? '?tech=' + encodeURIComponent(f.tech) : '';
    const target = '#/questions' + qs;
    if (location.hash !== target) history.replaceState(null, '', target);
  }
  function questionItem(q, opts) {
    const st = statusOf(q.id);
    const o = opts || {};
    const dotCls = st ? 'status-dot--' + st : (isLearned(q.id) ? 'status-dot--learned' : '');
    const dotLabel = st ? t('res_' + st) : (isLearned(q.id) ? t('learned') : t('res_none'));
    return h('a', { class: 'q-item', href: '#/q/' + encodeURIComponent(q.id), onclick: () => { if (o.navList) { ui.navList = o.navList; ui.navLabel = o.navLabel || ''; } } },
      h('span', { class: 'status-dot ' + dotCls, role: 'img', 'aria-label': dotLabel, title: dotLabel }),
      h('div', { style: { minWidth: 0 } },
        h('div', { class: 'q-item__title' }, biTitle(q.question)),
        h('div', { class: 'q-item__meta' },
          techBadge(q.technology), diffBadge(q.difficulty), typeBadge(q.type),
          h('span', { class: 'badge' }, q.subtopic),
          q.market !== 'both' ? marketBadge(q.market) : null,
          q.status !== 'stable' ? featureStatusBadge(q.status) : null,
          o.extra || null)),
      h('div', { class: 'q-item__side' },
        isBookmarked(q.id) ? h('span', { class: 'badge badge--primary', title: t('bookmarked') }, icon('bookmark', 12), h('span', { class: 'sr-only' }, t('bookmarked'))) : null,
        isFlagged(q.id) ? h('span', { class: 'badge badge--warn', title: t('flagged') }, icon('flag', 12), h('span', { class: 'sr-only' }, t('flagged'))) : null,
        h('span', { class: 'small muted nowrap' }, icon('clock', 12), ' ', t('minN', { n: q.estimatedMinutes }))));
  }
  function questionList(list, navLabel, limit) {
    const ids = list.map((q) => q.id);
    const items = (limit ? list.slice(0, limit) : list).map((q) => questionItem(q, { navList: ids, navLabel }));
    return h('div', { class: 'q-list' }, items);
  }

  function viewQuestions(route) {
    const f = ui.explorer;
    const qTech = route.query.get('tech');
    if (qTech !== null && TECH_MAP.has(qTech) && qTech !== f.tech) { f.tech = qTech; f.page = 1; }
    if (qTech === null && route.query.toString() === '' && ui.lastExplorerHash && ui.lastExplorerHash !== location.hash) { /* keep state */ }

    const results = h('div');
    const countEl = h('p', { class: 'results-count', 'aria-live': 'polite' });
    const pagerTop = h('div', { class: 'row' });

    function update(resetPage) {
      if (resetPage) f.page = 1;
      const list = filterQuestions(f);
      ui.navList = list.map((q) => q.id);
      ui.navLabel = t('nav_questions');
      const pages = Math.max(1, Math.ceil(list.length / PAGE_SIZE));
      f.page = clamp(f.page, 1, pages);
      clear(countEl);
      append(countEl, [h('strong', null, String(list.length)), ' ', t('matchingQuestions'), list.length ? h('span', { class: 'muted small' }, ' · ' + t('showingRange', { a: (f.page - 1) * PAGE_SIZE + 1, b: Math.min(list.length, f.page * PAGE_SIZE) })) : null]);
      clear(results);
      if (!list.length) {
        results.append(emptyState('search', QUESTIONS.length ? 'noMatchTitle' : 'bankEmpty', QUESTIONS.length ? 'noMatchText' : 'bankEmptyText', QUESTIONS.length ? [btn(t('clearFilters'), clearAll, 'btn--primary', 'x')] : null));
        return;
      }
      const slice = list.slice((f.page - 1) * PAGE_SIZE, f.page * PAGE_SIZE);
      results.append(h('div', { class: 'q-list' }, slice.map((q) => questionItem(q, { navList: ui.navList, navLabel: ui.navLabel }))));
      if (pages > 1) {
        results.append(h('nav', { class: 'pager', 'aria-label': t('pagination') },
          btn(t('prev'), () => { f.page--; update(); scrollTo({ top: 0 }); }, 'btn--sm', 'chevL', { disabled: f.page <= 1 }),
          h('span', { class: 'small muted' }, t('pageXofY', { x: f.page, y: pages })),
          btn(t('next'), () => { f.page++; update(); scrollTo({ top: 0 }); }, 'btn--sm', 'chevR', { disabled: f.page >= pages })));
      }
      syncExplorerHash();
      renderNav(parseRoute());
    }
    function clearAll() {
      Object.assign(f, { q: '', tech: '', diff: '', type: '', market: '', bookmarked: false, incorrect: false, unanswered: false, learned: false, review: false, sort: 'default', page: 1 });
      history.replaceState(null, '', '#/questions');
      rerender();
    }
    const sel = (key, labelKey, options) => {
      const s = h('select', { class: 'select', id: 'f-' + key, onchange: (e) => { f[key] = e.target.value; update(true); } },
        options.map(([v, lbl]) => h('option', { value: v, selected: f[key] === v }, lbl)));
      return h('div', { class: 'field' }, h('label', { for: 'f-' + key }, t(labelKey)), s);
    };
    const search = h('input', { class: 'input', id: 'f-q', type: 'search', placeholder: t('searchPlaceholder'), value: f.q, autocomplete: 'off', oninput: debounce((e) => { f.q = e.target.value; update(true); }, 140) });
    const flag = (key, labelKey) => h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: f[key], onchange: (e) => { f[key] = e.target.checked; update(true); } }), t(labelKey));
    const counts = countBy(QUESTIONS, 'technology');
    const panel = h('section', { class: 'card card--flat', 'aria-label': t('filters') },
      h('div', { class: 'filters' },
        h('div', { class: 'field field--search' }, h('label', { for: 'f-q' }, t('searchLabel')), h('div', { class: 'search-box' }, icon('search', 16), search)),
        sel('tech', 'technology', [['', t('allTechs')]].concat(TECHS.map((tc) => [tc.id, tc.name + ' (' + (counts[tc.id] || 0) + ')']))),
        sel('diff', 'difficulty', [['', t('allLevels')]].concat(DIFFS.map((d) => [d, t('diff_' + d)]))),
        sel('type', 'questionType', [['', t('allTypes')]].concat(TYPES.map((ty) => [ty, t('type_' + ty)]))),
        sel('market', 'market', [['', t('allMarkets')]].concat(MARKETS.map((m) => [m, t('market_' + m)])))),
      h('div', { class: 'filters__more' },
        flag('bookmarked', 'onlyBookmarked'), flag('incorrect', 'onlyIncorrect'), flag('unanswered', 'onlyUnanswered'), flag('learned', 'onlyLearned'), flag('review', 'onlyReview'),
        h('span', { style: { flex: '1' } }),
        h('div', { class: 'row' },
          h('label', { class: 'field-label', for: 'f-sort' }, t('sortBy')),
          h('select', { class: 'select', id: 'f-sort', style: { width: 'auto' }, onchange: (e) => { f.sort = e.target.value; update(true); } },
            [['default', 'sortRelevance'], ['diffAsc', 'sortDiffAsc'], ['diffDesc', 'sortDiffDesc'], ['priority', 'sortPriority'], ['recent', 'sortRecent']].map(([v, k]) => h('option', { value: v, selected: f.sort === v }, t(k))))),
        h('div', { class: 'row' }, h('span', { class: 'field-label' }, t('language')), seg([{ value: 'en', label: 'EN' }, { value: 'bn', label: 'বাংলা', lang: 'bn' }, { value: 'both', label: t('both') }], lang(), setLang, t('language'))),
        btn(t('clearFilters'), clearAll, 'btn--ghost btn--sm', 'x')));
    update();
    const node = frag(
      pageHead('nav_questions', 'questionsLead', [
        btn(t('practiceThese'), () => { const ids = filterQuestions(f).map((q) => q.id); if (!ids.length) { toast(t('nothingToPractice'), 'bad'); return; } startQuickSession(shuffle(ids).slice(0, 20), 'practice', { label: t('nav_questions') }); }, 'btn--secondary', 'play'),
      ]),
      panel,
      h('div', { class: 'results-bar' }, countEl, pagerTop),
      results);
    return { title: tb('nav_questions', null, { inline: true }), titleText: 'All Questions', node, after: () => { if (route.query.get('focus') === 'search') search.focus(); } };
  }

  /* ======================================================================
     Question detail
     ====================================================================== */
  const codeInQuestion = (q) => !!(q.code && q.code.source && (q.type === 'output' || q.type === 'debugging' || q.type === 'mcq'));

  function questionBody(q) {
    const parts = [biText(q.question, { cls: 'q-title', plain: true })];
    if (q.setup && q.setup.source) parts.push(h('div', { class: 'mt-2' }, codeBlock(q.setup, { label: t('schemaAndData') })));
    if (codeInQuestion(q)) parts.push(h('div', { class: 'mt-2' }, codeBlock({ language: q.code.language, source: q.code.source }, { label: q.type === 'debugging' ? t('buggyCode') : null })));
    return h('div', { class: 'stack stack--sm' }, parts);
  }
  function metaBadges(q, withTech) {
    return h('div', { class: 'q-head' },
      withTech ? techBadge(q.technology) : null,
      diffBadge(q.difficulty), typeBadge(q.type),
      h('span', { class: 'badge' }, q.subtopic),
      marketBadge(q.market), priorityBadge(q.priority),
      h('span', { class: 'badge', title: t('estimatedTime') }, icon('clock', 12), t('minN', { n: q.estimatedMinutes })),
      q.versionSensitive ? h('span', { class: 'badge badge--teal', title: t('versionSensitive') }, icon('info', 12), q.technologyVersion) : null,
      q.status !== 'stable' ? featureStatusBadge(q.status) : null);
  }
  function section(iconName, titleKey, content) {
    return h('section', { class: 'stack stack--sm' }, h('h3', { class: 'section-title' }, icon(iconName, 15), tb(titleKey, null, { inline: true })), content);
  }
  function answerPanel(q) {
    const parts = [];
    if (q.quickAnswer && (q.quickAnswer.en || q.quickAnswer.bn)) {
      parts.push(h('div', { class: 'callout callout--quick' }, h('div', { class: 'callout__title' }, icon('zap', 16), tb('quickAnswer', null, { inline: true }),
        h('span', { style: { marginLeft: 'auto' } }, speakButton('answer:' + q.id, () => speakAnswer(q, 'answer:' + q.id), { label: t('voiceListenAnswer'), shortcut: false }))), biText(q.quickAnswer)));
      parts.push(section('checkCircle', 'fullAnswer', biText(q.answer)));
    } else parts.push(section('checkCircle', q.type === 'behavioral' ? 'howToAnswer' : 'referenceAnswer', biText(q.answer)));
    if (q.complexity && (q.complexity.time || q.complexity.space)) {
      parts.push(h('div', { class: 'row' },
        q.complexity.time ? h('span', { class: 'badge badge--primary' }, t('timeComplexity') + ': ' + q.complexity.time) : null,
        q.complexity.space ? h('span', { class: 'badge badge--primary' }, t('spaceComplexity') + ': ' + q.complexity.space) : null));
    }
    if (q.code && q.code.source && !codeInQuestion(q)) {
      const label = q.type === 'coding' ? t('referenceSolution') : q.type === 'query' ? t('query') : t('codeExample');
      parts.push(codeBlock({ language: q.code.language, source: q.code.source }, { label }));
    }
    if (q.code && q.code.output) parts.push(codeBlock(q.code, { output: true }));
    q.extraCode.forEach((x) => parts.push(codeBlock(x, { label: pick(x.label) || null })));
    if (q.explanation.en || q.explanation.bn) parts.push(section(q.type === 'behavioral' ? 'message' : 'bulb', q.type === 'behavioral' ? 'sampleAnswer' : 'explanation', biText(q.explanation)));
    if (q.commonMistakes) parts.push(h('div', { class: 'callout callout--warn' }, h('div', { class: 'callout__title' }, icon('alert', 16), tb('commonMistakes', null, { inline: true })), biText(q.commonMistakes)));
    if (q.interviewTip.en || q.interviewTip.bn) parts.push(h('div', { class: 'callout callout--tip' }, h('div', { class: 'callout__title' }, icon('mic', 16), tb('interviewTip', null, { inline: true })), biText(q.interviewTip)));
    if (q.followUps.length) parts.push(section('message', 'followUps', h('ul', { class: 'list-plain' }, q.followUps.map((fu) => h('li', null, icon('chevR', 14), h('div', { style: { minWidth: 0 } }, biText(fu, { plain: true, noLabels: true })))))));
    if (q.references.length) parts.push(section('link', 'references', h('ul', { class: 'list-plain ref-list' }, q.references.map((r) => h('li', null, h('a', { href: r.url, target: '_blank', rel: 'noopener noreferrer' }, r.title, icon('external', 13)))))));
    return h('div', { class: 'stack answer-panel' }, parts);
  }
  function assessBar(current, onPick, opts) {
    const o = opts || {};
    const defs = [['correct', 'checkCircle', '100%'], ['partial', 'half', '50%'], ['incorrect', 'xcircle', '0%']];
    if (o.skip !== false) defs.push(['skipped', 'skip', t('recorded')]);
    return h('div', { class: 'assess', role: 'group', 'aria-label': t('selfAssess') },
      defs.map(([r, ic, hint], i) => h('button', { type: 'button', class: 'assess-btn assess-btn--' + r, 'aria-pressed': String(current === r), onclick: () => onPick(r), title: t('res_' + r) + (o.keys ? ' (' + (r === 'skipped' ? 'S' : i + 1) + ')' : '') },
        icon(ic, 20), h('span', null, t(r === 'skipped' ? 'skip' : 'res_' + r)), h('small', null, hint))));
  }
  function mcqBlock(q, choice, locked, onSubmit, opts) {
    const o = opts || {};
    let selected = choice;
    const L = lang();
    const keys = ['A', 'B', 'C', 'D', 'E', 'F'];
    const submit = h('button', { type: 'button', class: 'btn btn--primary', disabled: selected == null || locked, onclick: () => { if (selected != null && !locked) onSubmit(selected); } }, icon('check', 16), t('submitAnswer'));
    const opts2 = q.options.map((op, i) => {
      const isCorrect = locked && i === q.correctIndex;
      const isWrong = locked && i === choice && choice !== q.correctIndex;
      const txt = L === 'both'
        ? h('span', null, h('span', { lang: 'en' }, inline(op.en)), h('span', { class: 'bn-line bn', lang: 'bn' }, inline(op.bn)))
        : L === 'bn' ? h('span', { class: 'bn', lang: 'bn' }, inline(op.bn || op.en)) : h('span', { lang: 'en' }, inline(op.en || op.bn));
      const stateLbl = isCorrect ? h('span', { class: 'mcq-option__state', style: { color: 'var(--ok)' } }, t('correctAnswer')) : isWrong ? h('span', { class: 'mcq-option__state', style: { color: 'var(--bad)' } }, t('yourAnswer')) : h('span');
      const b = h('button', { type: 'button', role: 'radio', class: 'mcq-option' + (isCorrect ? ' is-correct' : '') + (isWrong ? ' is-wrong' : ''), 'aria-checked': String(selected === i), disabled: locked, 'data-idx': String(i),
        onclick: () => { if (locked) return; selected = i; opts2.forEach((x, k) => x.setAttribute('aria-checked', String(k === i))); submit.disabled = false; if (o.onSelect) o.onSelect(i); } },
      h('span', { class: 'mcq-option__key', 'aria-hidden': 'true' }, keys[i]), txt, stateLbl);
      return b;
    });
    const group = h('div', { class: 'mcq', role: 'radiogroup', 'aria-label': t('chooseAnswer') }, opts2);
    const wrap = h('div', { class: 'stack' }, group);
    if (!locked) wrap.append(h('div', { class: 'btn-row' }, submit, h('span', { class: 'small muted' }, t('mcqOnce'))));
    else {
      const ok = choice === q.correctIndex;
      wrap.append(h('div', { class: 'callout ' + (ok ? 'callout--tip' : 'callout--warn'), role: 'status' },
        h('div', { class: 'callout__title' }, icon(ok ? 'checkCircle' : 'xcircle', 16), tb(ok ? 'mcqCorrect' : 'mcqWrong', { key: keys[q.correctIndex] }, { inline: true }))));
    }
    wrap._select = (i) => { if (!locked && opts2[i]) opts2[i].click(); };
    wrap._submit = () => submit.click();
    return wrap;
  }
  function versionCard(q) {
    return h('section', { class: 'card' },
      h('h3', { class: 'section-title' }, icon('info', 15), t('versionInfo')),
      h('dl', { class: 'ver-box' },
        h('dt', null, t('version')), h('dd', null, q.technologyVersion),
        h('dt', null, t('featureStatus')), h('dd', null, featureStatusBadge(q.status)),
        h('dt', null, t('versionSensitive')), h('dd', null, q.versionSensitive ? t('yes') : t('no')),
        h('dt', null, t('verified')), h('dd', null, q.verifiedAt || '—'),
        q.documentationUrl ? h('dt', null, t('officialDocs')) : null,
        q.documentationUrl ? h('dd', null, h('a', { href: q.documentationUrl, target: '_blank', rel: 'noopener noreferrer' }, t('openDocs'), ' ', icon('external', 12))) : null));
  }
  function toggleBtn(pressed, ic, onLabel, offLabel, onClick) {
    return h('button', { type: 'button', class: 'btn btn--block ' + (pressed ? 'btn--secondary' : ''), 'aria-pressed': String(pressed), onclick: onClick, style: { justifyContent: 'flex-start' } }, icon(ic, 16), pressed ? onLabel : offLabel);
  }

  function viewQuestion(route) {
    const q = QMAP.get(route.params[0]);
    if (!q) return viewNotFound();
    const tc = TECH_MAP.get(q.technology);
    const mode = state.preferences.mode;
    const navList = ui.navList && ui.navList.includes(q.id) ? ui.navList : BY_TECH.get(q.technology).map((x) => x.id);
    const pos = navList.indexOf(q.id);
    const prevId = pos > 0 ? navList[pos - 1] : null;
    const nextId = pos < navList.length - 1 ? navList[pos + 1] : null;
    const attemptId = 'detail:' + q.id + ':' + ui.nonce;
    const mcqState = ui.mcq[q.id] && ui.mcq[q.id].nonce === ui.nonce ? ui.mcq[q.id] : null;
    const revealed = q.isMCQ ? (!!mcqState || ui.revealed.has(q.id)) : (mode === 'learning' ? !ui.hidden.has(q.id) : ui.revealed.has(q.id));
    const st = statusOf(q.id);
    const p = prog(q.id);

    const modeSeg = seg([{ value: 'learning', label: t('learningMode') }, { value: 'interview', label: t('interviewMode') }], mode, (m) => {
      state.preferences.mode = m; saveState(); ui.revealed.delete(q.id); ui.hidden.delete(q.id); rerender();
    }, t('studyMode'));

    const voiceKey = 'q:' + q.id;
    const speakThis = () => speakQuestion(q, voiceKey);
    ui.keyHandler = (e) => { if (e.key === 'v' || e.key === 'V') { toggleSpeak(voiceKey, speakThis); return true; } return false; };
    const headCard = h('section', { class: 'card card--pad-lg' },
      h('div', { class: 'row row--between mb-2' },
        h('a', { href: '#/questions?tech=' + q.technology, class: 'row small', style: { gap: '8px' } }, techLogo(tc, 'sm'), tc.name),
        h('div', { class: 'row', style: { gap: '8px' } }, speakButton(voiceKey, speakThis), modeSeg)),
      metaBadges(q, false),
      questionBody(q));

    let answerArea;
    if (q.isMCQ) {
      const locked = !!mcqState;
      answerArea = h('section', { class: 'card card--pad-lg stack' },
        h('h2', { class: 'section-title' }, icon('list', 15), tb('chooseAnswer', null, { inline: true })),
        mcqBlock(q, mcqState ? mcqState.choice : null, locked, (choice) => {
          ui.mcq[q.id] = { nonce: ui.nonce, choice };
          recordResult(q.id, choice === q.correctIndex ? 'correct' : 'incorrect', attemptId);
          rerender();
        }),
        !locked && !revealed ? h('div', null, btn(t('revealWithoutAnswering'), () => { ui.revealed.add(q.id); rerender(); }, 'btn--ghost btn--sm', 'eye')) : null,
        revealed ? answerPanel(q) : null);
    } else if (!revealed) {
      answerArea = h('section', { class: 'card card--pad-lg' },
        h('div', { class: 'reveal' },
          h('h2', { style: { margin: 0 } }, tb('thinkFirst')),
          h('p', { class: 'muted', style: { margin: 0, maxWidth: '52ch' } }, tb('thinkFirstText', { n: q.estimatedMinutes })),
          btn(t('revealAnswer'), () => { ui.revealed.add(q.id); ui.hidden.delete(q.id); rerender(); }, 'btn--primary btn--lg', 'eye')));
    } else {
      answerArea = frag(
        h('section', { class: 'card card--pad-lg' },
          h('div', { class: 'row row--between mb-2' },
            h('h2', { style: { margin: 0, fontSize: '1.1rem' } }, tb('answerSection', null, { inline: true })),
            mode === 'learning' ? btn(t('hideAnswer'), () => { ui.hidden.add(q.id); ui.revealed.delete(q.id); rerender(); }, 'btn--ghost btn--sm', 'eye') : null),
          answerPanel(q)),
        h('section', { class: 'card' },
          h('h2', { class: 'section-title' }, icon('target', 15), tb('howDidYouDo', null, { inline: true })),
          h('p', { class: 'small muted' }, tb('selfAssessHelp')),
          assessBar(p && p.history.length && p.history[p.history.length - 1].s === attemptId ? p.history[p.history.length - 1].r : null, (r) => {
            recordResult(q.id, r, attemptId);
            toast(tb('savedResult', { r: t('res_' + r) }, { inline: true }), r === 'correct' ? 'ok' : 'info', 1800);
            rerender();
          })));
    }

    const navRow = h('nav', { class: 'row row--between mt-2', 'aria-label': t('questionNav') },
      prevId ? linkBtn('#/q/' + encodeURIComponent(prevId), t('previous'), 'btn--ghost', 'arrowL') : h('span'),
      h('span', { class: 'small muted' }, (ui.navLabel && ui.navList === navList ? ui.navLabel + ' · ' : tc.name + ' · ') + (pos + 1) + ' / ' + navList.length),
      nextId ? h('a', { class: 'btn btn--ghost', href: '#/q/' + encodeURIComponent(nextId) }, t('next'), icon('arrowR', 16)) : h('span'));

    const related = [];
    q.related.forEach((id) => { const r = QMAP.get(id); if (r && r !== q) related.push(r); });
    BY_TECH.get(q.technology).forEach((r) => { if (related.length < 5 && r !== q && r.subtopic === q.subtopic && !related.includes(r)) related.push(r); });

    const aside = h('aside', { class: 'q-detail__aside', 'aria-label': t('questionTools') },
      h('section', { class: 'card stack stack--sm' },
        h('h3', { class: 'section-title' }, icon('bookmark', 15), t('myStatus')),
        toggleBtn(isBookmarked(q.id), 'bookmark', t('bookmarked'), t('bookmark'), () => { const v = toggleIn('bookmarks', q.id); toast(v ? t('addedBookmark') : t('removedBookmark'), 'ok', 1600); rerender(); }),
        toggleBtn(isLearned(q.id), 'grad', t('learned'), t('markLearned'), () => { toggleIn('learnedQuestions', q.id); rerender(); }),
        toggleBtn(isFlagged(q.id), 'flag', t('flagged'), t('flagReview'), () => { toggleIn('reviewQuestions', q.id); rerender(); }),
        h('dl', { class: 'kv mt-1' },
          h('dt', null, t('lastResult')), h('dd', null, resultBadge(st)),
          h('dt', null, t('attempts')), h('dd', null, p ? p.history.filter((e) => e.r !== 'skipped').length : 0),
          h('dt', null, t('nextReview')), h('dd', null, p && p.due ? fmtDate(p.due) : '—'))),
      versionCard(q),
      related.length ? h('section', { class: 'card' },
        h('h3', { class: 'section-title' }, icon('link', 15), t('relatedQuestions')),
        h('ul', { class: 'list-plain' }, related.map((r) => h('li', null, h('a', { href: '#/q/' + encodeURIComponent(r.id), class: 'small' }, pick(r.question)), ' ', diffBadge(r.difficulty))))) : null);

    const node = h('div', null,
      h('div', { class: 'row row--between mb-2' },
        h('a', { href: '#/questions', class: 'row small muted' }, icon('arrowL', 14), t('backToQuestions')),
        h('span', { class: 'tag' }, q.id)),
      h('div', { class: 'q-detail' }, h('div', { class: 'stack' }, headCard, answerArea, navRow), aside));
    return { title: h('span', null, tc.name, h('small', null, t('diff_' + q.difficulty))), titleText: pick(q.question).slice(0, 60), node };
  }
