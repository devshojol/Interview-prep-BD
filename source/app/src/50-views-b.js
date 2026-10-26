
  /* ======================================================================
     Practice configuration & session engine
     ====================================================================== */
  const PRESETS = [
    { id: 'quick', count: 10, icon: 'zap' },
    { id: 'focus', count: 20, icon: 'target' },
    { id: 'deep', count: 30, icon: 'layers' },
    { id: 'custom', count: null, icon: 'settings' },
  ];
  let practiceCfg = null;
  function practiceDefaults() {
    if (!practiceCfg) practiceCfg = { preset: 'quick', count: 10, techs: [], diffs: [], types: [], market: 'all', order: 'random', pool: 'all', timer: 0 };
    return practiceCfg;
  }
  let interviewCfg = null;
  function interviewDefaults() {
    if (!interviewCfg) interviewCfg = { count: 8, techs: [], diffs: ['medium', 'hard'], timer: 30, includeMcq: false, market: 'all' };
    return interviewCfg;
  }

  function matchingPool(cfg) {
    let list = QUESTIONS;
    if (cfg.techs && cfg.techs.length) list = list.filter((q) => cfg.techs.includes(q.technology));
    if (cfg.diffs && cfg.diffs.length) list = list.filter((q) => cfg.diffs.includes(q.difficulty));
    if (cfg.types && cfg.types.length) list = list.filter((q) => cfg.types.includes(q.type));
    if (cfg.includeMcq === false) list = list.filter((q) => !q.isMCQ);
    if (cfg.market === 'bangladesh') list = list.filter((q) => q.market === 'bangladesh' || q.market === 'both');
    else if (cfg.market === 'international') list = list.filter((q) => q.market === 'international' || q.market === 'both');
    if (cfg.pool === 'unanswered') list = list.filter((q) => !isAnswered(q.id));
    else if (cfg.pool === 'answered') list = list.filter((q) => isAnswered(q.id));
    else if (cfg.pool === 'mistakes') list = list.filter((q) => { const s = statusOf(q.id); return s === 'incorrect' || s === 'partial'; });
    return list;
  }
  function orderQuestions(list, order) {
    if (order !== 'priority') return shuffle(list);
    const due = new Set(dueIds());
    const prioRank = { high: 0, medium: 1, low: 2 };
    return list.map((q) => ({ q, k: [due.has(q.id) ? 0 : 1, isAnswered(q.id) ? 1 : 0, prioRank[q.priority], Math.random()] }))
      .sort((a, b) => { for (let i = 0; i < 4; i++) if (a.k[i] !== b.k[i]) return a.k[i] - b.k[i]; return 0; })
      .map((x) => x.q);
  }

  function createSession(kind, ids, config) {
    const now = Date.now();
    const timer = Number(config.timer) || 0;
    const s = {
      id: uid('s'), kind, config: Object.assign({}, config), ids: ids.slice(), index: 0, answers: {},
      startedAt: now, endedAt: null, deadline: timer ? now + timer * 60000 : null,
      dateKey: kind === 'daily' ? localDateKey() : null, summary: null,
    };
    state.activeSession = s;
    saveState();
    return s;
  }
  async function startSession(kind, ids, config) {
    const clean = ids.filter((id) => QMAP.has(id));
    if (!clean.length) { toast(t('nothingToPractice'), 'bad'); return false; }
    if (state.activeSession) {
      const ok = await confirmModal({ title: t('replaceSessionTitle'), message: tb('replaceSessionText'), confirmLabel: t('startNew') });
      if (!ok) return false;
      finishSession(state.activeSession, { silent: true });
    }
    createSession(kind, clean, config || {});
    go('#/session');
    return true;
  }
  function startQuickSession(ids, kind, extra) {
    return startSession(kind || 'practice', ids.slice(0, 60), Object.assign({ mode: 'practice', timer: 0 }, extra || {}));
  }
  function finishSession(s, opts) {
    const o = opts || {};
    s.endedAt = Date.now();
    s.summary = summarizeSession(s);
    state.sessions.push(s);
    if (state.sessions.length > 200) state.sessions = state.sessions.slice(-200);
    if (state.activeSession && state.activeSession.id === s.id) state.activeSession = null;
    if (s.kind === 'daily') state.daily[s.dateKey || localDateKey()] = { sessionId: s.id, score: s.summary.weighted };
    saveState();
    if (!o.silent) {
      if (o.timeUp) toast(tb('timeUp', null, { inline: true }), 'info', 4000);
      go('#/results/' + encodeURIComponent(s.id));
    }
  }

  function viewPractice() {
    const cfg = practiceDefaults();
    const countEl = h('span', { class: 'results-count', 'aria-live': 'polite' });
    const warnEl = h('div');
    function refresh() {
      const n = matchingPool(cfg).length;
      clear(countEl);
      countEl.append(h('strong', null, String(n)), ' ', t('matchingQuestions'));
      clear(warnEl);
      if (n === 0) warnEl.append(h('div', { class: 'callout callout--warn mt-1', role: 'alert' }, tb('noneMatchConfig')));
      else if (n < cfg.count) warnEl.append(h('div', { class: 'callout callout--info mt-1' }, tb('fewerThanRequested', { n, c: cfg.count })));
    }
    const multi = (key, values, labelFn, extraCount) => h('div', { class: 'chip-group', role: 'group' },
      chip(t('all'), !cfg[key].length, () => { cfg[key] = []; rerender(); }),
      values.map((v) => chip(h('span', null, labelFn(v), extraCount ? h('span', { class: 'count' }, ' ' + extraCount(v)) : null), cfg[key].includes(v), () => {
        cfg[key] = cfg[key].includes(v) ? cfg[key].filter((x) => x !== v) : cfg[key].concat(v);
        rerender();
      })));
    const techCounts = countBy(QUESTIONS, 'technology');
    const resume = state.activeSession ? h('div', { class: 'callout callout--info mb-2' },
      h('div', { class: 'callout__title' }, icon('play', 16), tb('unfinishedSession')),
      h('p', { class: 'small mb-1' }, tb('unfinishedText', { n: Object.values(state.activeSession.answers).filter((a) => a.result).length, total: state.activeSession.ids.length })),
      h('div', { class: 'btn-row' },
        linkBtn('#/session', t('resumeSession'), 'btn--primary btn--sm', 'play'),
        btn(t('finishNow'), () => finishSession(state.activeSession), 'btn--ghost btn--sm', 'stop'))) : null;

    const presets = h('div', { class: 'grid grid--4' }, PRESETS.map((p) => {
      const active = cfg.preset === p.id;
      return h('button', { type: 'button', class: 'card card--interactive', 'aria-pressed': String(active), style: { textAlign: 'left', cursor: 'pointer', borderColor: active ? 'var(--primary)' : null, background: active ? 'var(--primary-soft)' : null },
        onclick: () => { cfg.preset = p.id; if (p.count) cfg.count = p.count; rerender(); } },
      h('div', { class: 'row', style: { gap: '10px' } }, h('span', { class: 'empty__icon', style: { width: '38px', height: '38px', margin: 0, borderRadius: '10px' } }, icon(p.icon, 18)),
        h('div', null, h('strong', null, t('preset_' + p.id)), h('div', { class: 'small muted' }, p.count ? t('nQuestions', { n: p.count }) : t('presetCustomHint')))));
    }));
    const countInput = cfg.preset === 'custom' ? h('div', { class: 'field', style: { maxWidth: '220px' } },
      h('label', { for: 'p-count' }, t('numberOfQuestions')),
      h('input', { class: 'input', id: 'p-count', type: 'number', min: '1', max: '100', value: String(cfg.count), oninput: (e) => { const v = parseInt(e.target.value, 10); cfg.count = Number.isFinite(v) ? clamp(v, 1, 100) : 10; refresh(); } })) : null;

    const form = h('section', { class: 'card card--pad-lg stack' },
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('technologies')), multi('techs', TECHS.map((x) => x.id), (id) => TECH_MAP.get(id).name, (id) => techCounts[id] || 0)),
      h('div', { class: 'grid grid--2' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('difficulty')), multi('diffs', DIFFS, (d) => t('diff_' + d))),
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('market')), seg([{ value: 'all', label: t('allMarkets') }, { value: 'bangladesh', label: t('market_bangladesh') }, { value: 'international', label: t('market_international') }], cfg.market, (v) => { cfg.market = v; rerender(); }, t('market')))),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('questionTypes')), multi('types', TYPES, (ty) => t('type_' + ty))),
      h('div', { class: 'grid grid--3' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('selection')), seg([{ value: 'random', label: t('randomized') }, { value: 'priority', label: t('priorityBased') }], cfg.order, (v) => { cfg.order = v; rerender(); }, t('selection'))),
        h('div', { class: 'field' }, h('label', { for: 'p-pool' }, t('questionPool')),
          h('select', { class: 'select', id: 'p-pool', onchange: (e) => { cfg.pool = e.target.value; refresh(); } },
            [['all', 'poolAll'], ['unanswered', 'poolUnanswered'], ['answered', 'poolAnswered'], ['mistakes', 'poolMistakes']].map(([v, k]) => h('option', { value: v, selected: cfg.pool === v }, t(k))))),
        h('div', { class: 'field' }, h('label', { for: 'p-timer' }, t('timer')),
          h('select', { class: 'select', id: 'p-timer', onchange: (e) => { cfg.timer = parseInt(e.target.value, 10) || 0; } },
            [0, 10, 20, 30, 45, 60].map((m) => h('option', { value: String(m), selected: cfg.timer === m }, m ? t('minutesN', { n: m }) : t('untimed')))))),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('language')), seg([{ value: 'en', label: 'English' }, { value: 'bn', label: 'বাংলা', lang: 'bn' }, { value: 'both', label: t('both') }], lang(), setLang, t('language'))),
      countInput,
      h('hr', { style: { margin: '4px 0' } }),
      h('div', { class: 'row row--between' }, countEl,
        btn(t('startSession'), async () => {
          const pool = matchingPool(cfg);
          if (!pool.length) { toast(t('noneMatchShort'), 'bad'); return; }
          let n = cfg.count;
          if (pool.length < n) {
            const ok = await confirmModal({ title: t('notEnoughTitle'), message: tb('fewerThanRequested', { n: pool.length, c: n }), confirmLabel: t('startWithN', { n: pool.length }) });
            if (!ok) return;
            n = pool.length;
          }
          startSession('practice', orderQuestions(pool, cfg.order).slice(0, n).map((q) => q.id), { mode: 'practice', timer: cfg.timer, preset: cfg.preset, filters: { techs: cfg.techs, diffs: cfg.diffs, types: cfg.types, market: cfg.market, pool: cfg.pool, order: cfg.order }, count: n });
        }, 'btn--primary btn--lg', 'play')),
      warnEl);
    refresh();
    const node = frag(
      pageHead('nav_practice', 'practiceLead'),
      resume,
      presets,
      countInput ? null : null,
      h('div', { class: 'mt-3' }, form),
      h('div', { class: 'callout callout--info mt-3' },
        h('div', { class: 'callout__title' }, icon('info', 16), tb('howScoringWorks')),
        h('div', { class: 'small' }, tb('scoringExplain'))));
    return { title: tb('nav_practice', null, { inline: true }), titleText: 'Practice', node };
  }

  function viewSession() {
    const s = state.activeSession;
    if (!s) {
      return { title: tb('nav_practice', null, { inline: true }), node: emptyState('play', 'noActiveSession', 'noActiveSessionText', [linkBtn('#/practice', t('nav_practice'), 'btn--primary', 'play'), linkBtn('#/interview', t('nav_interview'), 'btn--ghost', 'mic')]) };
    }
    if (s.deadline && Date.now() >= s.deadline) { finishSession(s, { timeUp: true }); return null; }
    s.index = clamp(s.index, 0, s.ids.length - 1);
    const id = s.ids[s.index];
    const q = QMAP.get(id);
    if (!q) {
      s.ids = s.ids.filter((x) => QMAP.has(x));
      if (!s.ids.length) { state.activeSession = null; saveState(); return viewSession(); }
      saveState();
      return viewSession();
    }
    const a = s.answers[id] || (s.answers[id] = { result: null, revealed: false, mcqChoice: null, at: null, firstSeenAt: Date.now() });
    if (!a.firstSeenAt) a.firstSeenAt = Date.now();
    saveState();
    const isInterview = s.kind === 'interview';
    const answeredCount = s.ids.filter((x) => s.answers[x] && s.answers[x].result).length;
    const total = s.ids.length;
    const isLast = s.index === total - 1;

    const goIndex = (i) => { s.index = clamp(i, 0, total - 1); saveState(); render({ focus: false }); window.scrollTo(0, 0); };
    const advance = () => {
      const nextUnanswered = s.ids.findIndex((x, i) => i > s.index && !(s.answers[x] && s.answers[x].result));
      if (nextUnanswered >= 0) goIndex(nextUnanswered);
      else if (!isLast) goIndex(s.index + 1);
      else rerender();
    };
    const assess = (r) => {
      a.result = r; a.at = Date.now();
      if (r !== 'skipped') a.revealed = true;
      recordResult(q.id, r, s.id);
      saveState();
      if (s.ids.every((x) => s.answers[x] && s.answers[x].result)) { rerender(); return; }
      setTimeout(advance, prefersReducedMotion() ? 0 : 220);
    };
    const endSession = async () => {
      const remaining = total - s.ids.filter((x) => s.answers[x] && s.answers[x].result).length;
      if (remaining > 0) {
        const ok = await confirmModal({ title: t('endSessionTitle'), message: tb('endSessionText', { n: remaining }), confirmLabel: t('finishNow') });
        if (!ok) return;
      }
      finishSession(s);
    };

    // Timer
    const timerEl = h('span', { class: 'timer', role: 'timer', 'aria-label': s.deadline ? t('timeRemaining') : t('timeElapsed') }, icon('clock', 15), h('span'));
    const thinkEl = h('span', { class: 'small muted' });
    const tick = () => {
      const now = Date.now();
      const span = timerEl.lastChild;
      if (s.deadline) {
        const left = s.deadline - now;
        span.textContent = fmtClock(left);
        timerEl.classList.toggle('is-low', left < 60000);
        if (left <= 0) { stopTimers(); finishSession(s, { timeUp: true }); }
      } else span.textContent = fmtClock(now - s.startedAt);
      if (isInterview && !a.result) thinkEl.textContent = t('thinkTime') + ': ' + fmtClock(now - a.firstSeenAt);
    };

    const top = h('div', { class: 'session-top' },
      h('strong', { class: 'nowrap' }, t('kind_' + s.kind)),
      h('span', { class: 'small muted nowrap' }, t('questionXofY', { x: s.index + 1, y: total })),
      progressBar(answeredCount / total, { label: t('sessionProgress') }),
      h('span', { class: 'small muted nowrap' }, answeredCount + '/' + total + ' ' + t('doneWord')),
      timerEl,
      btn(t('endSession'), endSession, 'btn--ghost btn--sm', 'stop'));

    const dots = h('nav', { class: 'dots mb-2', 'aria-label': t('questionNav') }, s.ids.map((x, i) => {
      const r = s.answers[x] && s.answers[x].result;
      return h('button', { type: 'button', class: 'dot-btn' + (r ? ' r-' + r : ''), 'aria-current': i === s.index ? 'step' : null, 'aria-label': t('questionN', { n: i + 1 }) + (r ? ' — ' + t('res_' + r) : ''), onclick: () => goIndex(i) }, String(i + 1));
    }));

    // Voice: the interviewer reads the question (auto-read per session kind, or on demand with V)
    const voiceKey = 'session:' + s.id + ':' + id;
    const autoKey = s.kind === 'interview' ? 'interview' : s.kind === 'daily' ? 'daily' : 'practice';
    const introFor = isInterview ? tLang(isLast && total > 1 ? 'voiceIntroLast' : 'voiceIntroN', 'en', { n: s.index + 1 }) : null;
    const speakThis = () => speakQuestion(q, voiceKey, { intro: introFor });
    const voiceBar = autoKey !== 'practice' ? interviewerBar(voiceKey, speakThis, autoKey) : null;

    const tools = h('div', { class: 'row' },
      autoKey === 'practice' ? speakButton(voiceKey, speakThis, { compact: true }) : null,
      h('button', { type: 'button', class: 'icon-btn', 'aria-pressed': String(isBookmarked(q.id)), 'aria-label': t('bookmark') + ' (B)', title: t('bookmark') + ' (B)', onclick: () => { toggleIn('bookmarks', q.id); rerender(); } }, icon('bookmark', 18)),
      h('button', { type: 'button', class: 'icon-btn', 'aria-pressed': String(isFlagged(q.id)), 'aria-label': t('flagReview') + ' (F)', title: t('flagReview') + ' (F)', onclick: () => { toggleIn('reviewQuestions', q.id); rerender(); } }, icon('flag', 18)));

    const qCard = h('section', { class: 'card card--pad-lg' },
      voiceBar,
      h('div', { class: 'row row--between mb-1' }, h('div', { class: 'row' }, techBadge(q.technology), h('span', { class: 'small muted' }, t('questionN', { n: s.index + 1 }))), tools),
      metaBadges(q, false),
      questionBody(q),
      isInterview ? h('p', { class: 'mt-2 mb-0' }, thinkEl) : null);

    let answerArea;
    let mcqRef = null;
    if (q.isMCQ) {
      const locked = a.mcqChoice != null;
      mcqRef = mcqBlock(q, a.mcqChoice, locked, (choice) => {
        if (a.mcqChoice != null) return; // never score twice
        a.mcqChoice = choice; a.revealed = true;
        a.result = choice === q.correctIndex ? 'correct' : 'incorrect';
        a.at = Date.now();
        recordResult(q.id, a.result, s.id);
        saveState();
        rerender();
      });
      answerArea = h('section', { class: 'card card--pad-lg stack' },
        h('h2', { class: 'section-title' }, icon('list', 15), tb('chooseAnswer', null, { inline: true })),
        mcqRef,
        !locked ? h('div', null, btn(t('skip') + ' (S)', () => assess('skipped'), 'btn--ghost btn--sm', 'skip')) : null,
        locked ? answerPanel(q) : null);
    } else if (!a.revealed) {
      answerArea = h('section', { class: 'card card--pad-lg' },
        h('div', { class: 'reveal' },
          h('h2', { style: { margin: 0 } }, tb(isInterview ? 'answerAloud' : 'thinkFirst')),
          h('p', { class: 'muted', style: { margin: 0, maxWidth: '54ch' } }, tb('thinkFirstText', { n: q.estimatedMinutes })),
          h('div', { class: 'btn-row', style: { justifyContent: 'center' } },
            btn(t('revealAnswer'), () => { a.revealed = true; saveState(); rerender(); }, 'btn--primary btn--lg', 'eye', { title: t('revealAnswer') + ' (Space)' }),
            btn(t('skip'), () => assess('skipped'), 'btn--ghost', 'skip', { title: t('skip') + ' (S)' })),
          h('p', { class: 'tiny faint', style: { margin: 0 } }, icon('keyboard', 12), ' ', t('shortcutsHint'))));
    } else {
      answerArea = frag(
        h('section', { class: 'card card--pad-lg' }, answerPanel(q)),
        h('section', { class: 'card' },
          h('h2', { class: 'section-title' }, icon('target', 15), tb('howDidYouDo', null, { inline: true })),
          h('p', { class: 'small muted' }, tb('selfAssessHelp')),
          assessBar(a.result, assess, { keys: true })));
    }

    const allDone = s.ids.every((x) => s.answers[x] && s.answers[x].result);
    const footer = h('nav', { class: 'row row--between mt-2', 'aria-label': t('questionNav') },
      btn(t('previous'), () => goIndex(s.index - 1), 'btn--ghost', 'arrowL', { disabled: s.index === 0 }),
      allDone ? btn(t('seeResults'), () => finishSession(s), 'btn--primary btn--lg', 'trophy')
        : (isLast ? btn(t('finishSession'), endSession, 'btn--secondary', 'stop') : null),
      h('button', { type: 'button', class: 'btn btn--ghost', disabled: isLast, onclick: () => goIndex(s.index + 1) }, t('next'), icon('arrowR', 16)));

    ui.keyHandler = (e) => {
      const k = e.key;
      if (k === 'ArrowLeft') { if (s.index > 0) goIndex(s.index - 1); return true; }
      if (k === 'ArrowRight') { if (!isLast) goIndex(s.index + 1); return true; }
      if (k === 'b' || k === 'B') { toggleIn('bookmarks', q.id); rerender(); return true; }
      if (k === 'f' || k === 'F') { toggleIn('reviewQuestions', q.id); rerender(); return true; }
      if (k === 'v' || k === 'V') { toggleSpeak(voiceKey, speakThis); return true; }
      if (q.isMCQ) {
        if (a.mcqChoice != null) { if (k === 'Enter' && !isLast) { advance(); return true; } return false; }
        if (['1', '2', '3', '4'].includes(k)) { mcqRef._select(parseInt(k, 10) - 1); return true; }
        if (['a', 'b', 'c', 'd'].includes(k.toLowerCase()) && k.toLowerCase() !== 'b') { mcqRef._select('abcd'.indexOf(k.toLowerCase())); return true; }
        if (k === 'Enter') { mcqRef._submit(); return true; }
        if (k === 's' || k === 'S') { assess('skipped'); return true; }
        return false;
      }
      if (!a.revealed) {
        if (k === ' ' || k === 'Enter') { a.revealed = true; saveState(); rerender(); return true; }
        if (k === 's' || k === 'S') { assess('skipped'); return true; }
        return false;
      }
      if (k === '1') { assess('correct'); return true; }
      if (k === '2') { assess('partial'); return true; }
      if (k === '3') { assess('incorrect'); return true; }
      if (k === '4' || k === 's' || k === 'S') { assess('skipped'); return true; }
      return false;
    };
    const node = h('div', null, top, dots, h('div', { class: 'stack' }, qCard, answerArea, footer));
    return {
      title: tb('kind_' + s.kind, null, { inline: true }), titleText: tLang('kind_' + s.kind, 'en'), node, narrow: true,
      after: () => {
        tick(); ui.timers.push(setInterval(tick, 1000));
        if (autoReadOn(autoKey) && !a.result && ui.voiceRead !== voiceKey) { ui.voiceRead = voiceKey; speakThis(); }
      },
    };
  }

  /* ======================================================================
     Results
     ====================================================================== */
  function scoreRing(fraction) {
    const v = clamp(fraction || 0, 0, 1);
    const r = 70, c = 2 * Math.PI * r;
    const svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 168 168');
    svg.setAttribute('aria-hidden', 'true');
    const track = document.createElementNS(SVG_NS, 'circle');
    track.setAttribute('class', 'track'); track.setAttribute('cx', '84'); track.setAttribute('cy', '84'); track.setAttribute('r', String(r));
    const bar = document.createElementNS(SVG_NS, 'circle');
    bar.setAttribute('class', 'bar'); bar.setAttribute('cx', '84'); bar.setAttribute('cy', '84'); bar.setAttribute('r', String(r));
    bar.setAttribute('stroke-dasharray', String(c));
    bar.setAttribute('stroke-dashoffset', String(c));
    svg.append(track, bar);
    requestAnimationFrame(() => requestAnimationFrame(() => bar.setAttribute('stroke-dashoffset', String(c * (1 - v)))));
    return svg;
  }
  function confetti() {
    if (prefersReducedMotion()) return null;
    const colors = ['var(--primary)', 'var(--easy)', 'var(--medium)', 'var(--partial)', 'var(--hard)'];
    const box = h('div', { class: 'confetti', 'aria-hidden': 'true' });
    for (let i = 0; i < 28; i++) box.append(h('i', { style: { left: (Math.random() * 100) + '%', background: colors[i % colors.length], animationDelay: (Math.random() * 0.5) + 's' } }));
    setTimeout(() => box.remove(), 2600);
    return box;
  }
  function breakdownTable(rows, firstColKey, labelFn) {
    return h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
      h('thead', null, h('tr', null, h('th', null, t(firstColKey)), h('th', { class: 'num' }, t('questionsWord')), h('th', { class: 'num' }, t('res_correct')), h('th', { class: 'num' }, t('res_partial')), h('th', { class: 'num' }, t('res_incorrect')), h('th', { class: 'num' }, t('skippedWord')), h('th', { class: 'num' }, t('points')), h('th', { class: 'num' }, t('weightedScore')))),
      h('tbody', null, rows.map(([key, b]) => h('tr', null, h('td', null, labelFn(key)), h('td', { class: 'num' }, b.total), h('td', { class: 'num' }, b.correct), h('td', { class: 'num' }, b.partial), h('td', { class: 'num' }, b.incorrect), h('td', { class: 'num' }, b.skipped), h('td', { class: 'num' }, fmtNum(b.earned) + ' / ' + b.possible), h('td', { class: 'num' }, pct(b.possible ? b.earned / b.possible : null)))))));
  }
  function viewResults(route) {
    const s = state.sessions.find((x) => x.id === route.params[0]);
    if (!s) return { title: t('notFound'), node: emptyState('alert', 'sessionNotFound', 'sessionNotFoundText', [linkBtn('#/history', t('nav_history'), 'btn--primary')]) };
    const sm = summarizeSession(s);
    const w = sm.weighted || 0;
    const band = w >= 0.85 ? 'fbExcellent' : w >= 0.65 ? 'fbGood' : w >= 0.4 ? 'fbProgress' : 'fbKeepGoing';
    const mistakes = s.ids.filter((id) => QMAP.has(id) && s.answers[id] && (s.answers[id].result === 'incorrect' || s.answers[id].result === 'partial'));
    const toReview = s.ids.filter((id) => QMAP.has(id) && (!s.answers[id] || s.answers[id].result !== 'correct'));
    const heroCard = h('section', { class: 'card card--pad-lg', style: { position: 'relative', overflow: 'hidden' } },
      w >= 0.8 ? confetti() : null,
      h('div', { class: 'results-hero' },
        h('div', { class: 'score-ring' }, scoreRing(w), h('div', { class: 'score-ring__label' }, h('div', null, h('b', null, pct(sm.weighted)), h('span', null, t('weightedScore'))))),
        h('div', { style: { flex: '1', minWidth: '240px' } },
          h('p', { class: 'meta-line' }, t('kind_' + s.kind) + ' · ' + fmtDate(s.endedAt, true)),
          h('h1', null, tb(band)),
          h('p', { class: 'muted' }, tb(band + 'Text')),
          h('div', { class: 'btn-row' },
            btn(t('reviewMistakes'), () => startQuickSession(mistakes, 'practice', { label: t('reviewMistakes') }), 'btn--primary', 'rotate', { disabled: !mistakes.length }),
            btn(t('practiceAgain'), () => practiceAgain(s), 'btn--secondary', 'shuffle'),
            linkBtn('#/dashboard', t('returnDashboard'), 'btn--ghost', 'dashboard')))));
    const statsGrid = h('section', { class: 'grid grid--stats mt-3', 'aria-label': t('sessionStats') },
      stat(t('finalScore'), fmtNum(sm.earned) + ' / ' + sm.possible, { hint: t('pointsWord') }),
      stat(t('weightedScore'), pct(sm.weighted), { hint: t('weightedHint') }),
      stat(t('accuracy'), pct(sm.accuracy), { hint: t('accuracyHint') }),
      stat(t('completionTime'), fmtDuration(sm.durationMs), null),
      stat(t('res_correct'), String(sm.correct), { tone: 'ok' }),
      stat(t('res_partial'), String(sm.partial), { tone: 'partial' }),
      stat(t('res_incorrect'), String(sm.incorrect), { tone: 'bad' }),
      stat(t('skippedWord'), String(sm.skipped), { hint: t('skippedHint') }));
    const techRows = Object.keys(sm.byTech).map((k) => [k, sm.byTech[k]]);
    const diffRows = DIFFS.filter((d) => sm.byDiff[d].total).map((d) => [d, sm.byDiff[d]]);
    const reviewList = toReview.length ? h('div', { class: 'q-list' }, toReview.map((id) => questionItem(QMAP.get(id), { navList: toReview, navLabel: t('questionsToReview'), extra: resultBadge(s.answers[id] && s.answers[id].result ? s.answers[id].result : 'skipped') })))
      : h('p', { class: 'muted' }, tb('nothingToReview'));
    const node = frag(
      heroCard,
      statsGrid,
      h('div', { class: 'callout callout--info mt-2 small' }, tb('scoringExplain')),
      h('div', { class: 'grid grid--2 mt-3' },
        h('section', { class: 'card' }, h('h2', null, tb('byTechnology')), breakdownTable(techRows, 'technology', (k) => techBadge(k))),
        h('section', { class: 'card' }, h('h2', null, tb('byDifficulty')), breakdownTable(diffRows, 'difficulty', (d) => diffBadge(d)))),
      h('section', { class: 'mt-3' }, h('h2', null, tb('questionsToReview')), reviewList));
    return { title: tb('results', null, { inline: true }), titleText: 'Results', node };
  }
  function practiceAgain(s) {
    const c = s.config || {};
    if (s.kind === 'daily') { startQuickSession(shuffle(s.ids), 'practice', { label: t('nav_daily') }); return; }
    if (c.filters) {
      const cfg = Object.assign({ techs: [], diffs: [], types: [], market: 'all', pool: 'all', order: 'random' }, c.filters);
      if (s.kind === 'interview') cfg.includeMcq = !!c.includeMcq;
      const pool = matchingPool(cfg);
      const ids = orderQuestions(pool.length ? pool : s.ids.map((id) => QMAP.get(id)).filter(Boolean), cfg.order).slice(0, c.count || s.ids.length).map((q) => q.id);
      startSession(s.kind, ids, c);
    } else startSession(s.kind, shuffle(s.ids), c);
  }

  /* ======================================================================
     Interview simulation
     ====================================================================== */
  function viewInterview() {
    const cfg = interviewDefaults();
    const countEl = h('span', { class: 'results-count', 'aria-live': 'polite' });
    const refresh = () => { clear(countEl); countEl.append(h('strong', null, String(matchingPool(cfg).length)), ' ', t('matchingQuestions')); };
    const multi = (key, values, labelFn) => h('div', { class: 'chip-group' },
      chip(t('all'), !cfg[key].length, () => { cfg[key] = []; rerender(); }),
      values.map((v) => chip(labelFn(v), cfg[key].includes(v), () => { cfg[key] = cfg[key].includes(v) ? cfg[key].filter((x) => x !== v) : cfg[key].concat(v); rerender(); })));
    const resume = state.activeSession && state.activeSession.kind === 'interview' ? h('div', { class: 'callout callout--info mb-2' },
      h('div', { class: 'callout__title' }, icon('mic', 16), tb('unfinishedInterview')),
      h('div', { class: 'btn-row' }, linkBtn('#/session', t('resumeSession'), 'btn--primary btn--sm', 'play'))) : null;
    const form = h('section', { class: 'card card--pad-lg stack' },
      h('div', { class: 'grid grid--2' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('numberOfQuestions')), seg([5, 8, 10, 15].map((n) => ({ value: n, label: String(n) })), cfg.count, (v) => { cfg.count = v; rerender(); }, t('numberOfQuestions'))),
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('timeLimit')), seg([0, 15, 30, 45, 60].map((m) => ({ value: m, label: m ? m + 'm' : t('none') })), cfg.timer, (v) => { cfg.timer = v; rerender(); }, t('timeLimit')))),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('technologies')), multi('techs', TECHS.map((x) => x.id), (id) => TECH_MAP.get(id).name)),
      h('div', { class: 'grid grid--2' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('difficulty')), multi('diffs', DIFFS, (d) => t('diff_' + d))),
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('market')), seg([{ value: 'all', label: t('allMarkets') }, { value: 'bangladesh', label: t('market_bangladesh') }, { value: 'international', label: t('market_international') }], cfg.market, (v) => { cfg.market = v; rerender(); }, t('market')))),
      h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: cfg.includeMcq, onchange: (e) => { cfg.includeMcq = e.target.checked; refresh(); } }), t('includeMcq')),
      VOICE_OK ? h('div', { class: 'row row--between', style: { gap: '12px' } },
        h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: autoReadOn('interview'), onchange: (e) => { state.preferences.voice.auto.interview = e.target.checked; saveState(); } }), icon('speaker', 15), t('voiceInterviewOpt')),
        speakButton('voice:test', () => speakTest(), { label: t('voiceTest'), shortcut: false })) : null,
      h('div', { class: 'row row--between' }, countEl,
        btn(t('startInterview'), async () => {
          const pool = matchingPool(cfg);
          if (!pool.length) { toast(t('noneMatchShort'), 'bad'); return; }
          let n = cfg.count;
          if (pool.length < n) {
            const ok = await confirmModal({ title: t('notEnoughTitle'), message: tb('fewerThanRequested', { n: pool.length, c: n }), confirmLabel: t('startWithN', { n: pool.length }) });
            if (!ok) return;
            n = pool.length;
          }
          // Interviews usually move from easier to harder questions
          const picked = shuffle(pool).slice(0, n).sort((a, b) => DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty));
          startSession('interview', picked.map((q) => q.id), { mode: 'interview', timer: cfg.timer, includeMcq: cfg.includeMcq, count: n, filters: { techs: cfg.techs, diffs: cfg.diffs, market: cfg.market, types: [], pool: 'all', order: 'random' } });
        }, 'btn--primary btn--lg', 'mic')));
    refresh();
    const how = h('section', { class: 'card' },
      h('h2', null, tb('howInterviewWorks')),
      h('ol', { class: 'prose' }, ['iw1', 'iw2', 'iw3', 'iw4'].map((k) => h('li', null, tb(k)))));
    const node = frag(pageHead('nav_interview', 'interviewLead'), resume, h('div', { class: 'grid grid--2-1' }, form, how));
    return { title: tb('nav_interview', null, { inline: true }), titleText: 'Interview Simulation', node };
  }

  /* ======================================================================
     Daily challenge (deterministic by local date, no server)
     ====================================================================== */
  function dailyIdsFor(key) {
    const rnd = mulberry32(hashString('daily:' + key));
    const chosen = [];
    const pickFrom = (filter) => {
      const pool = QUESTIONS.filter((q) => filter(q) && !chosen.includes(q));
      if (!pool.length) return null;
      const q = pool[Math.floor(rnd() * pool.length)];
      chosen.push(q);
      return q;
    };
    pickFrom((q) => q.isMCQ && (q.difficulty === 'easy' || q.difficulty === 'medium')) || pickFrom(() => true);
    pickFrom((q) => !q.isMCQ && q.difficulty === 'medium') || pickFrom(() => true);
    pickFrom((q) => q.difficulty === 'hard') || pickFrom(() => true);
    return chosen.map((q) => q.id);
  }
  function dailyInfo() {
    const key = localDateKey();
    const rec = state.daily[key];
    return { key, ids: dailyIdsFor(key), done: !!rec, sessionId: rec ? rec.sessionId : null, score: rec ? rec.score : null };
  }
  function dailyStreak() {
    let n = 0;
    const d = new Date();
    if (!state.daily[localDateKey(d)]) d.setDate(d.getDate() - 1);
    while (state.daily[localDateKey(d)]) { n++; d.setDate(d.getDate() - 1); }
    return n;
  }
  function viewDaily() {
    const info = dailyInfo();
    const active = state.activeSession && state.activeSession.kind === 'daily' && state.activeSession.dateKey === info.key;
    const items = info.ids.map((id, i) => {
      const q = QMAP.get(id);
      return h('li', { class: 'card', style: { padding: '14px 16px' } },
        h('div', { class: 'row row--between' },
          h('div', { class: 'row' }, h('strong', null, '#' + (i + 1)), techBadge(q.technology), diffBadge(q.difficulty), typeBadge(q.type)),
          info.done ? h('a', { href: '#/q/' + encodeURIComponent(id), class: 'small' }, t('open')) : h('span', { class: 'small muted' }, t('hiddenUntilStart'))),
        info.done ? h('div', { class: 'mt-1' }, biTitle(q.question, 'q-item__title')) : null);
    });
    const node = frag(
      pageHead('nav_daily', 'dailyLead', null, info.key),
      !QUESTIONS.length ? emptyState('database', 'bankEmpty', 'bankEmptyText') : h('div', { class: 'grid grid--2-1' },
        h('section', { class: 'stack' },
          h('ol', { class: 'list-plain' }, items),
          h('div', { class: 'btn-row' },
            info.done ? linkBtn('#/results/' + encodeURIComponent(info.sessionId), t('viewResults'), 'btn--primary', 'trophy')
              : active ? linkBtn('#/session', t('resumeSession'), 'btn--primary btn--lg', 'play')
                : btn(t('startChallenge'), () => startSession('daily', info.ids, { mode: 'practice', timer: 0 }), 'btn--primary btn--lg', 'zap'),
            info.done ? btn(t('practiceAgain'), () => startQuickSession(info.ids, 'practice', { label: t('nav_daily') }), 'btn--ghost', 'shuffle') : null)),
        h('section', { class: 'card stack stack--sm' },
          h('h2', null, tb('dailyStatus')),
          h('dl', { class: 'kv' },
            h('dt', null, t('today')), h('dd', null, info.done ? h('span', { class: 'badge badge--ok' }, icon('check', 12), t('completed')) : h('span', { class: 'badge' }, t('notYet'))),
            h('dt', null, t('weightedScore')), h('dd', null, pct(info.score)),
            h('dt', null, t('dailyStreak')), h('dd', null, t('daysN', { n: dailyStreak() }))),
          h('p', { class: 'small muted mb-0' }, tb('dailyHow')))));
    return { title: tb('nav_daily', null, { inline: true }), titleText: 'Daily Challenge', node };
  }

  /* ======================================================================
     Flashcards
     ====================================================================== */
  const flash = { tech: '', diff: '', source: 'all', ids: null, index: 0, flipped: false, sig: '' };
  function flashDeck() {
    const sig = [flash.tech, flash.diff, flash.source].join('|');
    if (flash.ids && flash.sig === sig) return flash.ids.filter((id) => QMAP.has(id));
    let list = QUESTIONS;
    if (flash.tech) list = list.filter((q) => q.technology === flash.tech);
    if (flash.diff) list = list.filter((q) => q.difficulty === flash.diff);
    if (flash.source === 'bookmarked') list = list.filter((q) => isBookmarked(q.id));
    else if (flash.source === 'due') { const due = new Set(dueIds()); list = list.filter((q) => due.has(q.id) || isFlagged(q.id)); }
    else if (flash.source === 'incorrect') list = list.filter((q) => { const s = statusOf(q.id); return s === 'incorrect' || s === 'partial'; });
    else if (flash.source === 'unlearned') list = list.filter((q) => !isLearned(q.id));
    else if (flash.source === 'quick') list = list.filter((q) => q.type === 'quick');
    flash.ids = list.map((q) => q.id);
    flash.sig = sig;
    flash.index = 0;
    flash.flipped = false;
    return flash.ids;
  }
  function plainCode(code) {
    return h('figure', { class: 'code' }, h('div', { class: 'code__bar' }, h('span', { class: 'code__lang' }, code.language || 'text')), h('pre', null, h('code', null, highlight(code.source, code.language))));
  }
  function viewFlashcards() {
    const deck = flashDeck();
    flash.index = clamp(flash.index, 0, Math.max(0, deck.length - 1));
    const setF = (k, v) => { flash[k] = v; flash.ids = null; rerender(); };
    const controls = h('section', { class: 'card card--flat' }, h('div', { class: 'filters filters--4' },
      h('div', { class: 'field' }, h('label', { for: 'fc-tech' }, t('technology')), h('select', { class: 'select', id: 'fc-tech', onchange: (e) => setF('tech', e.target.value) }, [['', t('allTechs')]].concat(TECHS.map((x) => [x.id, x.name])).map(([v, l]) => h('option', { value: v, selected: flash.tech === v }, l)))),
      h('div', { class: 'field' }, h('label', { for: 'fc-diff' }, t('difficulty')), h('select', { class: 'select', id: 'fc-diff', onchange: (e) => setF('diff', e.target.value) }, [['', t('allLevels')]].concat(DIFFS.map((d) => [d, t('diff_' + d)])).map(([v, l]) => h('option', { value: v, selected: flash.diff === v }, l)))),
      h('div', { class: 'field' }, h('label', { for: 'fc-src' }, t('deck')), h('select', { class: 'select', id: 'fc-src', onchange: (e) => setF('source', e.target.value) }, [['all', 'deckAll'], ['quick', 'deckQuick'], ['unlearned', 'deckUnlearned'], ['bookmarked', 'nav_bookmarks'], ['due', 'deckDue'], ['incorrect', 'deckMistakes']].map(([v, k]) => h('option', { value: v, selected: flash.source === v }, t(k))))),
      h('div', { class: 'field' }, h('span', { class: 'field-label', 'aria-hidden': 'true' }, ' '), btn(t('shuffle'), () => { flash.ids = shuffle(deck); flash.index = 0; flash.flipped = false; rerender(); }, '', 'shuffle', { disabled: deck.length < 2 }))));
    if (!deck.length) {
      return { title: tb('nav_flashcards', null, { inline: true }), node: frag(pageHead('nav_flashcards', 'flashLead'), controls, h('div', { class: 'mt-3' }, emptyState('cards', 'emptyDeck', 'emptyDeckText'))) };
    }
    const q = QMAP.get(deck[flash.index]);
    const faceKey = () => 'flash:' + q.id + (flash.flipped ? ':back' : ':front');
    const speakFace = () => (flash.flipped ? speakAnswer(q, faceKey()) : speakQuestion(q, faceKey(), { options: true }));
    const flip = () => {
      flash.flipped = !flash.flipped; card.classList.toggle('is-flipped', flash.flipped); card.setAttribute('aria-pressed', String(flash.flipped));
      if (autoReadOn('flashcards')) speakFace(); else stopSpeaking();
      listenSlot.replaceChildren(speakButton(faceKey(), speakFace) || '');
    };
    const listenSlot = h('span', { class: 'row' });
    const nav = (d) => { flash.index = clamp(flash.index + d, 0, deck.length - 1); flash.flipped = false; rerender(); };
    const front = h('div', { class: 'flashcard__face flashcard__face--front', 'aria-hidden': String(flash.flipped) },
      h('div', { class: 'row' }, techBadge(q.technology), diffBadge(q.difficulty), typeBadge(q.type)),
      biText(q.question, { cls: 'q-title', plain: true }),
      q.setup && q.setup.source ? plainCode(q.setup) : null,
      codeInQuestion(q) ? plainCode(q.code) : null,
      q.isMCQ ? h('ol', { type: 'A', class: 'prose' }, q.options.map((o) => h('li', null, pick(o)))) : null,
      h('p', { class: 'flash-hint' }, t('tapToFlip')));
    const back = h('div', { class: 'flashcard__face flashcard__face--back', 'aria-hidden': String(!flash.flipped) },
      h('div', { class: 'meta-line' }, t(q.quickAnswer ? 'quickAnswer' : 'referenceAnswer')),
      q.isMCQ ? h('p', null, h('strong', null, t('correctAnswer') + ': ' + 'ABCD'[q.correctIndex] + ' — '), pick(q.options[q.correctIndex])) : null,
      biText(q.quickAnswer || q.answer),
      q.code && q.code.output ? h('div', null, h('div', { class: 'small muted' }, t('expectedOutput')), h('pre', { class: 'mono small' }, q.code.output)) : null);
    const card = h('button', { type: 'button', class: 'flashcard' + (flash.flipped ? ' is-flipped' : ''), 'aria-pressed': String(flash.flipped), 'aria-label': t('flipCard'), onclick: flip }, front, back);
    ui.keyHandler = (e) => {
      if (e.key === ' ' || e.key === 'Enter') { if (document.activeElement === card) return false; flip(); return true; }
      if (e.key === 'ArrowRight') { nav(1); return true; }
      if (e.key === 'ArrowLeft') { nav(-1); return true; }
      if (e.key === 'v' || e.key === 'V') { toggleSpeak(faceKey(), speakFace); return true; }
      return false;
    };
    listenSlot.append(speakButton(faceKey(), speakFace) || '');
    const autoFlash = VOICE_OK ? h('button', { type: 'button', class: 'interviewer__auto', 'aria-pressed': String(autoReadOn('flashcards')),
      onclick: () => { state.preferences.voice.auto.flashcards = !state.preferences.voice.auto.flashcards; saveState(); if (state.preferences.voice.auto.flashcards) speakFace(); else stopSpeaking(); rerender(); } },
    icon(autoReadOn('flashcards') ? 'speaker' : 'speakerOff', 15), t('voiceAutoFlash')) : null;
    const node = frag(
      pageHead('nav_flashcards', 'flashLead'),
      controls,
      h('div', { class: 'row row--between mt-3 mb-1', style: { maxWidth: '760px', marginInline: 'auto' } },
        h('span', { class: 'small muted' }, t('cardXofY', { x: flash.index + 1, y: deck.length })),
        progressBar((flash.index + 1) / deck.length, { thin: true }),
        h('a', { href: '#/q/' + encodeURIComponent(q.id), class: 'small', onclick: () => { ui.navList = deck.slice(); ui.navLabel = t('nav_flashcards'); } }, t('openFull'))),
      h('div', { class: 'flash-wrap' }, card),
      h('div', { class: 'btn-row mt-2', style: { justifyContent: 'center' } },
        btn(t('previous'), () => nav(-1), 'btn--ghost', 'arrowL', { disabled: flash.index === 0 }),
        btn(t('flip'), flip, 'btn--secondary', 'rotate'),
        h('button', { type: 'button', class: 'btn btn--ghost', disabled: flash.index >= deck.length - 1, onclick: () => nav(1) }, t('next'), icon('arrowR', 16))),
      VOICE_OK ? h('div', { class: 'btn-row mt-1', style: { justifyContent: 'center' } }, listenSlot, autoFlash) : null,
      h('div', { class: 'btn-row mt-1', style: { justifyContent: 'center' } },
        toggleBtnInline(isLearned(q.id), 'grad', t('learned'), t('markLearned'), () => { toggleIn('learnedQuestions', q.id); rerender(); }),
        toggleBtnInline(isFlagged(q.id), 'flag', t('flagged'), t('needsReviewBtn'), () => { toggleIn('reviewQuestions', q.id); rerender(); }),
        toggleBtnInline(isBookmarked(q.id), 'bookmark', t('bookmarked'), t('bookmark'), () => { toggleIn('bookmarks', q.id); rerender(); })),
      h('p', { class: 'flash-hint' }, icon('keyboard', 12), ' ', t('flashKeys')));
    const readKey = 'flash:' + q.id + ':' + flash.index;
    return { title: tb('nav_flashcards', null, { inline: true }), titleText: 'Flashcards', node, narrow: false,
      after: () => { if (autoReadOn('flashcards') && ui.voiceRead !== readKey) { ui.voiceRead = readKey; speakFace(); } } };
  }
  function toggleBtnInline(pressed, ic, onLabel, offLabel, onClick) {
    return h('button', { type: 'button', class: 'btn btn--sm ' + (pressed ? 'btn--secondary' : 'btn--ghost'), 'aria-pressed': String(pressed), onclick: onClick }, icon(ic, 15), pressed ? onLabel : offLabel);
  }
