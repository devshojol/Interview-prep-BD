
  /* ======================================================================
     Persistent state (localStorage, versioned, corruption-safe)
     ====================================================================== */
  function defaultState() {
    return {
      version: STORAGE_VERSION,
      createdAt: Date.now(),
      preferences: { lang: 'en', theme: 'dark', mode: 'learning', motion: 'system', fontScale: 1, sidebarCollapsed: false, voice: defaultVoicePrefs() },
      bookmarks: [],
      learnedQuestions: [],
      reviewQuestions: [],
      questionProgress: {},
      sessions: [],
      activeSession: null,
      planner: { dailyTarget: 10, interviewDate: '' },
      activity: {},
      daily: {},
    };
  }

  let storageOK = true;
  let storageNotice = null; // 'corrupt' | 'incompatible' | 'unavailable' | null
  function storageGet(key) { try { return window.localStorage.getItem(key); } catch (e) { storageOK = false; return null; } }
  function storageSet(key, val) { window.localStorage.setItem(key, val); }

  const strArr = (v) => (Array.isArray(v) ? Array.from(new Set(v.filter((x) => isStr(x) && x.length < 120))) : []);

  function defaultVoicePrefs() {
    return { rate: 1, en: '', auto: { interview: true, daily: true, practice: false, flashcards: false } };
  }
  function sanitizeVoicePrefs(v) {
    const d = defaultVoicePrefs();
    if (!isObj(v)) return d;
    const a = isObj(v.auto) ? v.auto : {};
    return {
      rate: [0.85, 1, 1.15].includes(v.rate) ? v.rate : d.rate,
      en: isStr(v.en) && v.en.length < 200 ? v.en : '',
      auto: { interview: typeof a.interview === 'boolean' ? a.interview : d.auto.interview, daily: typeof a.daily === 'boolean' ? a.daily : d.auto.daily,
        practice: a.practice === true, flashcards: a.flashcards === true },
    };
  }
  function sanitizePreferences(p) {
    const d = defaultState().preferences;
    if (!isObj(p)) return d;
    return {
      lang: ['en', 'bn', 'both'].includes(p.lang) ? p.lang : d.lang,
      theme: ['dark', 'light'].includes(p.theme) ? p.theme : d.theme,
      mode: ['learning', 'interview'].includes(p.mode) ? p.mode : d.mode,
      motion: ['system', 'reduce', 'full'].includes(p.motion) ? p.motion : d.motion,
      fontScale: [0.9, 1, 1.1, 1.2].includes(p.fontScale) ? p.fontScale : d.fontScale,
      sidebarCollapsed: p.sidebarCollapsed === true,
      voice: sanitizeVoicePrefs(p.voice),
    };
  }
  function sanitizeProgressEntry(p) {
    if (!isObj(p)) return null;
    const history = Array.isArray(p.history)
      ? p.history.filter((e) => isObj(e) && RESULTS.includes(e.r) && Number.isFinite(e.at)).map((e) => ({ r: e.r, at: e.at, s: isStr(e.s) ? e.s : null })).slice(-20)
      : [];
    if (!history.length) return null;
    return {
      history,
      box: Number.isInteger(p.box) ? clamp(p.box, 0, REVIEW_INTERVALS.length) : null,
      due: Number.isFinite(p.due) ? p.due : null,
    };
  }
  function sanitizeSession(s) {
    if (!isObj(s) || !isStr(s.id) || !Array.isArray(s.ids)) return null;
    const ids = s.ids.filter(isStr).slice(0, 200);
    if (!ids.length) return null;
    const answers = {};
    if (isObj(s.answers)) {
      for (const id of ids) {
        const a = s.answers[id];
        if (!isObj(a)) continue;
        answers[id] = {
          result: RESULTS.includes(a.result) ? a.result : null,
          revealed: a.revealed === true,
          mcqChoice: Number.isInteger(a.mcqChoice) ? a.mcqChoice : null,
          at: Number.isFinite(a.at) ? a.at : null,
          firstSeenAt: Number.isFinite(a.firstSeenAt) ? a.firstSeenAt : null,
        };
      }
    }
    return {
      id: s.id,
      kind: ['practice', 'interview', 'daily'].includes(s.kind) ? s.kind : 'practice',
      config: isObj(s.config) ? s.config : {},
      ids,
      index: Number.isInteger(s.index) ? clamp(s.index, 0, ids.length - 1) : 0,
      answers,
      startedAt: Number.isFinite(s.startedAt) ? s.startedAt : Date.now(),
      endedAt: Number.isFinite(s.endedAt) ? s.endedAt : null,
      deadline: Number.isFinite(s.deadline) ? s.deadline : null,
      dateKey: isStr(s.dateKey) ? s.dateKey : null,
      summary: isObj(s.summary) ? s.summary : null,
    };
  }

  /* Migrations: each entry upgrades data FROM version n to n+1. */
  const MIGRATIONS = {
    // 0 = unversioned prototype format: { bookmarks, learned, review, progress, history }
    0: (d) => ({
      version: 1,
      preferences: d.preferences || d.prefs,
      bookmarks: d.bookmarks,
      learnedQuestions: d.learnedQuestions || d.learned,
      reviewQuestions: d.reviewQuestions || d.review,
      questionProgress: d.questionProgress || d.progress,
      sessions: d.sessions || d.history,
      planner: d.planner,
      activity: d.activity,
      daily: d.daily,
    }),
  };
  function migrate(data) {
    let d = data;
    let v = Number.isInteger(d.version) ? d.version : 0;
    if (v > STORAGE_VERSION) return { data: null, incompatible: true };
    while (v < STORAGE_VERSION) {
      const step = MIGRATIONS[v];
      if (!step) return { data: null, incompatible: true };
      d = step(d);
      v = d.version;
    }
    return { data: d, incompatible: false };
  }

  function sanitizeState(d) {
    const base = defaultState();
    if (!isObj(d)) return base;
    base.createdAt = Number.isFinite(d.createdAt) ? d.createdAt : base.createdAt;
    base.preferences = sanitizePreferences(d.preferences);
    base.bookmarks = strArr(d.bookmarks);
    base.learnedQuestions = strArr(d.learnedQuestions);
    base.reviewQuestions = strArr(d.reviewQuestions);
    if (isObj(d.questionProgress)) {
      for (const id of Object.keys(d.questionProgress)) {
        if (!isStr(id) || id.length > 120) continue;
        const e = sanitizeProgressEntry(d.questionProgress[id]);
        if (e) base.questionProgress[id] = e;
      }
    }
    base.sessions = Array.isArray(d.sessions) ? d.sessions.map(sanitizeSession).filter((s) => s && s.endedAt).slice(-200) : [];
    base.activeSession = d.activeSession ? sanitizeSession(d.activeSession) : null;
    if (base.activeSession && base.activeSession.endedAt) base.activeSession = null;
    if (isObj(d.planner)) {
      const t = parseInt(d.planner.dailyTarget, 10);
      base.planner.dailyTarget = Number.isFinite(t) ? clamp(t, 1, 200) : 10;
      base.planner.interviewDate = isStr(d.planner.interviewDate) && /^\d{4}-\d{2}-\d{2}$/.test(d.planner.interviewDate) ? d.planner.interviewDate : '';
    }
    if (isObj(d.activity)) {
      for (const k of Object.keys(d.activity)) {
        const n = d.activity[k];
        if (/^\d{4}-\d{2}-\d{2}$/.test(k) && Number.isFinite(n) && n > 0) base.activity[k] = Math.min(10000, Math.round(n));
      }
    }
    if (isObj(d.daily)) {
      for (const k of Object.keys(d.daily)) {
        const v = d.daily[k];
        if (/^\d{4}-\d{2}-\d{2}$/.test(k) && isObj(v) && isStr(v.sessionId)) base.daily[k] = { sessionId: v.sessionId, score: Number.isFinite(v.score) ? v.score : null };
      }
    }
    return base;
  }

  function loadState() {
    const raw = storageGet(STORAGE_KEY);
    if (!storageOK) { storageNotice = 'unavailable'; return defaultState(); }
    if (raw == null) return defaultState();
    let parsed;
    try { parsed = JSON.parse(raw); } catch (e) { parsed = undefined; }
    if (!isObj(parsed)) {
      try { storageSet(STORAGE_KEY + ':corrupt:' + Date.now(), raw); } catch (e) { /* ignore */ }
      storageNotice = 'corrupt';
      return defaultState();
    }
    const m = migrate(parsed);
    if (m.incompatible) {
      try { storageSet(STORAGE_KEY + ':backup:' + Date.now(), raw); } catch (e) { /* ignore */ }
      storageNotice = 'incompatible';
      return defaultState();
    }
    return sanitizeState(m.data);
  }

  let state = loadState();

  function saveState() {
    if (!storageOK) return false;
    try {
      storageSet(STORAGE_KEY, JSON.stringify(state));
      return true;
    } catch (e) {
      // Quota exceeded: trim history and retry once
      try {
        state.sessions = state.sessions.slice(-50);
        storageSet(STORAGE_KEY, JSON.stringify(state));
        return true;
      } catch (e2) {
        storageOK = false;
        toast(t('storageFull'), 'bad');
        return false;
      }
    }
  }

  /* ======================================================================
     Progress, scoring and review scheduling
     ====================================================================== */
  function prog(id) { return state.questionProgress[id] || null; }

  /** Latest non-skipped result (the question's "answer status"). */
  function statusOf(id) {
    const p = prog(id);
    if (!p) return null;
    for (let i = p.history.length - 1; i >= 0; i--) if (p.history[i].r !== 'skipped') return p.history[i].r;
    return 'skipped';
  }
  function lastAt(id) { const p = prog(id); return p && p.history.length ? p.history[p.history.length - 1].at : 0; }
  const isAnswered = (id) => { const s = statusOf(id); return s === 'correct' || s === 'partial' || s === 'incorrect'; };

  function bumpActivity(n) {
    const k = localDateKey();
    state.activity[k] = (state.activity[k] || 0) + (n || 1);
  }

  function scheduleReview(p, result, now) {
    if (result === 'incorrect') { p.box = 0; p.due = addDays(startOfDay(now), REVIEW_INTERVALS[0]); }
    else if (result === 'partial') { p.box = Math.min(p.box == null ? 1 : Math.max(1, p.box), REVIEW_INTERVALS.length - 1); p.due = addDays(startOfDay(now), REVIEW_INTERVALS[p.box]); }
    else if (result === 'correct') {
      if (p.due != null) {
        const next = (p.box == null ? 0 : p.box) + 1;
        if (next >= REVIEW_INTERVALS.length) { p.box = null; p.due = null; }
        else { p.box = next; p.due = addDays(startOfDay(now), REVIEW_INTERVALS[next]); }
      }
    }
  }

  /** Record a result. With a sessionId, a previous result from the same session is replaced (no double counting). */
  function recordResult(id, result, sessionId) {
    if (!QMAP.has(id) || !RESULTS.includes(result)) return;
    const now = Date.now();
    let p = state.questionProgress[id];
    if (!p) p = state.questionProgress[id] = { history: [], box: null, due: null };
    let replaced = false;
    if (sessionId) {
      const idx = p.history.findIndex((e) => e.s === sessionId);
      if (idx >= 0) { p.history.splice(idx, 1); replaced = true; }
    }
    p.history.push({ r: result, at: now, s: sessionId || null });
    if (p.history.length > 20) p.history = p.history.slice(-20);
    scheduleReview(p, result, now);
    if (!replaced && result !== 'skipped') bumpActivity(1);
    saveState();
  }

  function dueIds(now) {
    const end = addDays(startOfDay(now || Date.now()), 1) - 1;
    return QUESTIONS.filter((q) => { const p = prog(q.id); return p && p.due != null && p.due <= end; }).map((q) => q.id);
  }
  function upcomingIds(days) {
    const start = addDays(startOfDay(Date.now()), 1);
    const end = addDays(start, days);
    return QUESTIONS.filter((q) => { const p = prog(q.id); return p && p.due != null && p.due >= start && p.due < end; }).map((q) => q.id);
  }

  const setHas = (key, id) => state[key].includes(id);
  function toggleIn(key, id, force) {
    const has = state[key].includes(id);
    const want = force == null ? !has : !!force;
    if (want && !has) { state[key].push(id); if (key === 'learnedQuestions') bumpActivity(1); }
    if (!want && has) state[key] = state[key].filter((x) => x !== id);
    saveState();
    return want;
  }
  const isBookmarked = (id) => setHas('bookmarks', id);
  const isLearned = (id) => setHas('learnedQuestions', id);
  const isFlagged = (id) => setHas('reviewQuestions', id);

  /** Aggregate stats over a list of questions using each question's latest status. */
  function statsFor(list) {
    const s = { total: list.length, answered: 0, correct: 0, partial: 0, incorrect: 0, skippedOnly: 0, attempted: 0, learned: 0, bookmarked: 0, flagged: 0, earned: 0, possible: 0, completed: 0, byDiff: {} };
    DIFFS.forEach((d) => { s.byDiff[d] = { total: 0, answered: 0, correct: 0, partial: 0, incorrect: 0 }; });
    for (const q of list) {
      const st = statusOf(q.id);
      const bd = s.byDiff[q.difficulty];
      bd.total++;
      if (isLearned(q.id)) s.learned++;
      if (isBookmarked(q.id)) s.bookmarked++;
      if (isFlagged(q.id)) s.flagged++;
      if (st) {
        s.attempted++;
        s.possible += POINTS[q.difficulty];
        s.earned += POINTS[q.difficulty] * RESULT_FACTOR[st];
      }
      if (st === 'skipped') s.skippedOnly++;
      else if (st) { s.answered++; s[st]++; bd.answered++; bd[st]++; }
      if ((st && st !== 'skipped') || isLearned(q.id)) s.completed++;
    }
    s.accuracy = s.answered ? s.correct / s.answered : null;
    s.weighted = s.possible ? s.earned / s.possible : null;
    s.completion = s.total ? s.completed / s.total : 0;
    return s;
  }

  function streakInfo() {
    const today = localDateKey();
    let d = new Date();
    if (!state.activity[today]) d.setDate(d.getDate() - 1);
    let streak = 0;
    while (state.activity[localDateKey(d)]) { streak++; d.setDate(d.getDate() - 1); }
    let best = 0, run = 0;
    const keys = Object.keys(state.activity).sort();
    let prev = null;
    for (const k of keys) {
      if (prev && (startOfDay(new Date(k + 'T00:00:00')) - startOfDay(new Date(prev + 'T00:00:00'))) <= DAY * 1.5) run++;
      else run = 1;
      best = Math.max(best, run);
      prev = k;
    }
    return { current: streak, best: Math.max(best, streak), today: state.activity[today] || 0 };
  }

  /** Session summary with weighted score and accuracy. Unanswered questions count as skipped. */
  function summarizeSession(sess) {
    const sm = { total: 0, correct: 0, partial: 0, incorrect: 0, skipped: 0, earned: 0, possible: 0, byTech: {}, byDiff: {}, durationMs: 0 };
    DIFFS.forEach((d) => { sm.byDiff[d] = { total: 0, correct: 0, partial: 0, incorrect: 0, skipped: 0, earned: 0, possible: 0 }; });
    for (const id of sess.ids) {
      const q = QMAP.get(id);
      if (!q) continue;
      const a = sess.answers[id] || {};
      const r = RESULTS.includes(a.result) ? a.result : 'skipped';
      const pts = POINTS[q.difficulty];
      const earned = pts * RESULT_FACTOR[r];
      sm.total++; sm[r]++; sm.possible += pts; sm.earned += earned;
      const bt = sm.byTech[q.technology] || (sm.byTech[q.technology] = { total: 0, correct: 0, partial: 0, incorrect: 0, skipped: 0, earned: 0, possible: 0 });
      const bd = sm.byDiff[q.difficulty];
      for (const b of [bt, bd]) { b.total++; b[r]++; b.earned += earned; b.possible += pts; }
    }
    sm.answered = sm.correct + sm.partial + sm.incorrect;
    sm.accuracy = sm.answered ? sm.correct / sm.answered : null;
    sm.weighted = sm.possible ? sm.earned / sm.possible : null;
    sm.durationMs = Math.max(0, (sess.endedAt || Date.now()) - sess.startedAt);
    return sm;
  }

  /** Weak areas: subtopics/technologies with the most incorrect or partial answers (min 2 attempts). */
  function weakAreas(limit) {
    const groups = new Map();
    for (const q of QUESTIONS) {
      const p = prog(q.id);
      if (!p) continue;
      const answered = p.history.filter((e) => e.r !== 'skipped');
      if (!answered.length) continue;
      const key = q.technology + '::' + q.subtopic;
      const g = groups.get(key) || { tech: q.technology, subtopic: q.subtopic, attempts: 0, correct: 0, partial: 0, incorrect: 0, ids: new Set() };
      for (const e of answered) { g.attempts++; g[e.r]++; }
      g.ids.add(q.id);
      groups.set(key, g);
    }
    const arr = Array.from(groups.values()).filter((g) => g.attempts >= 2 && (g.incorrect + g.partial) > 0);
    arr.forEach((g) => { g.missRate = (g.incorrect + 0.5 * g.partial) / g.attempts; g.accuracy = g.correct / g.attempts; });
    arr.sort((a, b) => b.missRate - a.missRate || b.attempts - a.attempts);
    return arr.slice(0, limit || 6);
  }
  function weakDifficulties() {
    const out = [];
    for (const d of DIFFS) {
      let attempts = 0, miss = 0;
      for (const q of QUESTIONS) {
        if (q.difficulty !== d) continue;
        const p = prog(q.id);
        if (!p) continue;
        for (const e of p.history) { if (e.r === 'skipped') continue; attempts++; if (e.r === 'incorrect') miss += 1; else if (e.r === 'partial') miss += 0.5; }
      }
      out.push({ difficulty: d, attempts, missRate: attempts ? miss / attempts : null });
    }
    return out;
  }

  /* ======================================================================
     Export / import
     ====================================================================== */
  function exportData() {
    return {
      app: 'interview-prep-bd',
      appVersion: APP_VERSION,
      exportedAt: new Date().toISOString(),
      data: {
        version: STORAGE_VERSION,
        createdAt: state.createdAt,
        preferences: state.preferences,
        bookmarks: state.bookmarks,
        learnedQuestions: state.learnedQuestions,
        reviewQuestions: state.reviewQuestions,
        questionProgress: state.questionProgress,
        sessions: state.sessions,
        planner: state.planner,
        activity: state.activity,
        daily: state.daily,
      },
    };
  }
  /** Validates an imported backup. Returns { ok, data?, error?, summary? } and never mutates state. */
  function parseImport(text) {
    if (!isStr(text) || text.length > 15 * 1024 * 1024) return { ok: false, error: 'tooLarge' };
    let obj;
    try { obj = JSON.parse(text); } catch (e) { return { ok: false, error: 'invalidJson' }; }
    if (!isObj(obj) || obj.app !== 'interview-prep-bd' || !isObj(obj.data)) return { ok: false, error: 'notBackup' };
    const m = migrate(obj.data);
    if (m.incompatible) return { ok: false, error: 'incompatible' };
    const clean = sanitizeState(m.data);
    clean.activeSession = null;
    const known = (id) => QMAP.has(id);
    const summary = {
      bookmarks: clean.bookmarks.filter(known).length,
      learned: clean.learnedQuestions.filter(known).length,
      review: clean.reviewQuestions.filter(known).length,
      progress: Object.keys(clean.questionProgress).filter(known).length,
      sessions: clean.sessions.length,
      exportedAt: isStr(obj.exportedAt) ? obj.exportedAt : '',
    };
    return { ok: true, data: clean, summary };
  }
