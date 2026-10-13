
  /* ======================================================================
     Bookmarks / Incorrect / Review
     ====================================================================== */
  function viewBookmarks() {
    const list = state.bookmarks.map((id) => QMAP.get(id)).filter(Boolean);
    const ids = list.map((q) => q.id);
    const node = frag(
      pageHead('nav_bookmarks', 'bookmarksLead', list.length ? [
        btn(t('practiceThese'), () => startQuickSession(shuffle(ids), 'practice', { label: t('nav_bookmarks') }), 'btn--primary', 'play'),
        btn(t('nav_flashcards'), () => { flash.source = 'bookmarked'; flash.tech = ''; flash.diff = ''; flash.ids = null; go('#/flashcards'); }, 'btn--ghost', 'cards'),
      ] : null),
      list.length ? frag(h('p', { class: 'results-count' }, h('strong', null, String(list.length)), ' ', t('bookmarkedQuestions')), questionList(list, t('nav_bookmarks')))
        : emptyState('bookmark', 'noBookmarks', 'noBookmarksText', [linkBtn('#/questions', t('browseQuestions'), 'btn--primary', 'list')]));
    return { title: tb('nav_bookmarks', null, { inline: true }), titleText: 'Bookmarks', node };
  }

  function viewIncorrect() {
    const tab = ui.incorrectTab;
    const incorrect = QUESTIONS.filter((q) => statusOf(q.id) === 'incorrect');
    const partial = QUESTIONS.filter((q) => statusOf(q.id) === 'partial');
    const list = tab === 'incorrect' ? incorrect : partial;
    const tabs = seg([
      { value: 'incorrect', label: t('res_incorrect') + ' (' + incorrect.length + ')' },
      { value: 'partial', label: t('res_partial') + ' (' + partial.length + ')' },
    ], tab, (v) => { ui.incorrectTab = v; rerender(); }, t('filter'));
    const all = incorrect.concat(partial).map((q) => q.id);
    const node = frag(
      pageHead('nav_incorrect', 'incorrectLead', all.length ? [btn(t('practiceMistakes'), () => startQuickSession(shuffle(all), 'practice', { label: t('nav_incorrect') }), 'btn--primary', 'rotate')] : null),
      h('div', { class: 'row row--between mb-2' }, tabs, h('span', { class: 'small muted' }, tb('latestResultNote'))),
      list.length ? questionList(list, t('nav_incorrect')) : emptyState('checkCircle', tab === 'incorrect' ? 'noIncorrect' : 'noPartial', 'noMistakesText', [linkBtn('#/practice', t('startPractice'), 'btn--primary', 'play')]));
    return { title: tb('nav_incorrect', null, { inline: true }), titleText: 'Incorrect Answers', node };
  }

  function viewReview() {
    const due = dueIds().map((id) => QMAP.get(id));
    const flagged = state.reviewQuestions.map((id) => QMAP.get(id)).filter(Boolean);
    const upcoming = upcomingIds(7).map((id) => QMAP.get(id));
    const recent = QUESTIONS.filter((q) => lastAt(q.id)).sort((a, b) => lastAt(b.id) - lastAt(a.id)).slice(0, 10);
    const reviewIds = Array.from(new Set(due.concat(flagged).map((q) => q.id)));
    const dueBadge = (q) => { const p = prog(q.id); return p && p.due ? h('span', { class: 'badge badge--warn' }, icon('calendar', 12), fmtDate(p.due)) : null; };
    const block = (titleKey, list, emptyKey, extraFn) => h('section', { class: 'mt-3' },
      h('div', { class: 'row row--between mb-1' }, h('h2', { class: 'mb-0' }, tb(titleKey)), h('span', { class: 'badge' }, String(list.length))),
      list.length ? h('div', { class: 'q-list' }, list.map((q) => questionItem(q, { navList: list.map((x) => x.id), navLabel: t(titleKey), extra: extraFn ? extraFn(q) : null })))
        : h('p', { class: 'muted small' }, tb(emptyKey)));
    const node = frag(
      pageHead('nav_review', 'reviewLead', reviewIds.length ? [btn(t('reviewNow'), () => startQuickSession(reviewIds, 'practice', { label: t('nav_review') }), 'btn--primary', 'rotate')] : null),
      h('div', { class: 'callout callout--info' }, h('div', { class: 'callout__title' }, icon('info', 16), tb('reviewScheduleTitle')), h('div', { class: 'small' }, tb('reviewScheduleText'))),
      block('dueForReview', due, 'nothingDue', dueBadge),
      block('flaggedForReview', flagged, 'nothingFlagged'),
      block('upcomingReviews', upcoming, 'nothingUpcoming', dueBadge),
      block('recentlyStudied', recent, 'nothingRecent', (q) => resultBadge(statusOf(q.id))));
    return { title: tb('nav_review', null, { inline: true }), titleText: 'Review Questions', node };
  }

  /* ======================================================================
     Study history
     ====================================================================== */
  function heatmap(weeks) {
    const end = new Date(); end.setHours(0, 0, 0, 0);
    const start = new Date(end); start.setDate(start.getDate() - (weeks * 7 - 1) - end.getDay());
    const cells = [];
    let activeDays = 0, totalActs = 0;
    for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
      const k = localDateKey(d);
      const n = state.activity[k] || 0;
      if (n) { activeDays++; totalActs += n; }
      const l = n === 0 ? 0 : n < 3 ? 1 : n < 8 ? 2 : n < 15 ? 3 : 4;
      cells.push(h('i', { 'data-l': String(l), title: k + ': ' + n }));
    }
    return { el: h('div', { class: 'heatmap', role: 'img', 'aria-label': t('heatmapLabel', { d: activeDays, n: totalActs, w: weeks }) }, cells), activeDays, totalActs };
  }
  function viewHistory() {
    const sessions = state.sessions.slice().reverse();
    const hm = heatmap(16);
    const streak = streakInfo();
    const totals = sessions.reduce((acc, s) => { const sm = s.summary || summarizeSession(s); acc.q += sm.total; acc.ms += sm.durationMs; return acc; }, { q: 0, ms: 0 });
    const table = sessions.length ? h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
      h('caption', { class: 'sr-only' }, t('nav_history')),
      h('thead', null, h('tr', null, h('th', null, t('date')), h('th', null, t('typeWord')), h('th', { class: 'num' }, t('questionsWord')), h('th', { class: 'num' }, t('weightedScore')), h('th', { class: 'num' }, t('accuracy')), h('th', { class: 'num' }, t('duration')), h('th', null, ''))),
      h('tbody', null, sessions.map((s) => {
        const sm = s.summary || summarizeSession(s);
        return h('tr', null,
          h('td', null, fmtDate(s.endedAt, true)),
          h('td', null, t('kind_' + s.kind), s.config && s.config.label ? h('span', { class: 'muted small' }, ' · ' + s.config.label) : null),
          h('td', { class: 'num' }, sm.total),
          h('td', { class: 'num' }, pct(sm.weighted)),
          h('td', { class: 'num' }, pct(sm.accuracy)),
          h('td', { class: 'num' }, fmtDuration(sm.durationMs)),
          h('td', null, h('a', { href: '#/results/' + encodeURIComponent(s.id) }, t('details'))));
      })))) : emptyState('clock', 'noHistory', 'noHistoryText', [linkBtn('#/practice', t('startPractice'), 'btn--primary', 'play')]);
    const node = frag(
      pageHead('nav_history', 'historyLead'),
      h('div', { class: 'grid grid--stats' },
        stat(t('sessionsWord'), String(sessions.length), null),
        stat(t('questionsPracticed'), String(totals.q), null),
        stat(t('timeSpent'), fmtDuration(totals.ms), null),
        stat(t('activeDays'), String(hm.activeDays), { hint: t('lastNWeeks', { n: 16 }) }),
        stat(t('studyStreak'), t('daysN', { n: streak.current }), { hint: t('bestStreak', { n: streak.best }) })),
      h('section', { class: 'card mt-3' },
        h('div', { class: 'card__head' }, h('h2', null, tb('activity')), h('span', { class: 'card__sub' }, t('heatmapLabel', { d: hm.activeDays, n: hm.totalActs, w: 16 }))),
        hm.el,
        h('div', { class: 'legend' }, h('span', null, t('less')), [0, 1, 2, 3, 4].map((l) => h('i', { style: { background: l ? null : 'var(--card-2)' }, class: 'hm-legend', 'data-l': String(l) })), h('span', null, t('more')))),
      h('section', { class: 'mt-3' }, h('h2', null, tb('pastSessions')), table));
    return { title: tb('nav_history', null, { inline: true }), titleText: 'Study History', node };
  }

  /* ======================================================================
     Study planner
     ====================================================================== */
  function viewPlanner() {
    const target = state.planner.dailyTarget;
    const days = [];
    for (let i = 6; i >= 0; i--) { const d = new Date(); d.setDate(d.getDate() - i); days.push(localDateKey(d)); }
    const maxV = Math.max(target, ...days.map((k) => state.activity[k] || 0), 1);
    const remaining = QUESTIONS.filter((q) => !isAnswered(q.id) && !isLearned(q.id)).length;
    let daysLeft = null;
    if (state.planner.interviewDate) {
      daysLeft = Math.round((startOfDay(new Date(state.planner.interviewDate + 'T00:00:00')) - startOfDay()) / DAY);
    }
    const suggested = daysLeft && daysLeft > 0 ? Math.ceil(remaining / daysLeft) : null;
    const today = state.activity[localDateKey()] || 0;
    const targetInput = h('input', { class: 'input', id: 'pl-target', type: 'number', min: '1', max: '200', value: String(target), style: { maxWidth: '140px' } });
    const dateInput = h('input', { class: 'input', id: 'pl-date', type: 'date', value: state.planner.interviewDate || '', style: { maxWidth: '200px' } });
    const save = () => {
      const v = parseInt(targetInput.value, 10);
      if (!Number.isFinite(v) || v < 1 || v > 200) { toast(t('invalidTarget'), 'bad'); targetInput.focus(); return; }
      state.planner.dailyTarget = v;
      state.planner.interviewDate = /^\d{4}-\d{2}-\d{2}$/.test(dateInput.value) ? dateInput.value : '';
      saveState();
      toast(t('plannerSaved'), 'ok');
      rerender();
    };
    const weak = weakAreas(6);
    const wd = weakDifficulties().filter((x) => x.attempts >= 3);
    const due = dueIds();
    const node = frag(
      pageHead('nav_planner', 'plannerLead'),
      h('div', { class: 'grid grid--2' },
        h('section', { class: 'card stack' },
          h('h2', null, tb('dailyTarget')),
          h('div', { class: 'row', style: { alignItems: 'flex-end' } },
            h('div', { class: 'field' }, h('label', { for: 'pl-target' }, t('questionsPerDay')), targetInput),
            h('div', { class: 'field' }, h('label', { for: 'pl-date' }, t('interviewDate')), dateInput),
            btn(t('save'), save, 'btn--primary', 'check')),
          h('div', null,
            h('div', { class: 'row row--between mb-1' }, h('strong', null, t('todayProgress', { n: today, t: target })), h('span', { class: 'small muted' }, pct(Math.min(1, today / target)))),
            progressBar(today / target, { lg: true, label: t('todaysGoal') })),
          h('p', { class: 'small muted mb-0' }, tb('activityDefinition'))),
        h('section', { class: 'card' },
          h('h2', null, tb('last7Days')),
          h('div', { class: 'vbars', role: 'img', 'aria-label': days.map((k) => k + ': ' + (state.activity[k] || 0)).join(', ') },
            days.map((k) => {
              const v = state.activity[k] || 0;
              return h('div', { class: 'vbar' }, h('span', { class: 'vbar__val' }, String(v)), h('div', { class: 'vbar__fill' + (v >= target ? ' is-goal' : ''), style: { height: Math.max(3, (v / maxV) * 90) + '%' } }), h('span', { class: 'vbar__label' }, fmtDay(k)));
            })),
          h('p', { class: 'small muted mt-1 mb-0' }, t('goalLine', { n: target })))),
      h('div', { class: 'grid grid--3 mt-3' },
        stat(t('remainingQuestions'), String(remaining), { hint: t('notAnsweredOrLearned') }),
        stat(t('daysUntilInterview'), daysLeft == null ? '—' : daysLeft < 0 ? t('passed') : String(daysLeft), { hint: state.planner.interviewDate || t('setDateHint') }),
        stat(t('suggestedPerDay'), suggested == null ? '—' : String(suggested), { hint: t('suggestedHint') })),
      h('div', { class: 'grid grid--2 mt-3' },
        h('section', { class: 'card' },
          h('h2', null, tb('weakTopics')),
          weak.length ? weakList(weak) : h('p', { class: 'muted small' }, tb('noWeakTopics')),
          wd.length ? h('div', { class: 'mt-2' }, h('h3', { class: 'section-title' }, t('missRateByDifficulty')),
            h('div', { class: 'bars' }, wd.map((x) => h('div', { class: 'bar-row' }, h('span', { class: 'bar-row__label' }, diffBadge(x.difficulty)), progressBar(x.missRate, { thin: true, label: t('missRate') }), h('span', { class: 'bar-row__value' }, pct(x.missRate)))))) : null,
          h('p', { class: 'tiny faint mt-2 mb-0' }, tb('weakHow'))),
        h('section', { class: 'card' },
          h('h2', null, tb('recommendedNext')),
          h('ul', { class: 'list-plain' },
            due.length ? h('li', null, icon('rotate', 16), h('div', null, tb('recDue', { n: due.length }), h('div', { class: 'mt-1' }, btn(t('reviewNow'), () => startQuickSession(due, 'practice', { label: t('nav_review') }), 'btn--sm btn--secondary', 'play')))) : null,
            h('li', null, icon('zap', 16), h('div', null, tb('recDaily'), h('div', { class: 'mt-1' }, linkBtn('#/daily', t('nav_daily'), 'btn--sm btn--ghost')))),
            h('li', null, icon('target', 16), h('div', null, tb('recPractice', { n: Math.min(target, 30) }), h('div', { class: 'mt-1' }, btn(t('startPractice'), () => { const cfg = practiceDefaults(); cfg.preset = 'custom'; cfg.count = Math.min(Math.max(target, 5), 30); cfg.order = 'priority'; cfg.pool = 'all'; go('#/practice'); }, 'btn--sm btn--ghost')))),
            h('li', null, icon('mic', 16), h('div', null, tb('recInterview'), h('div', { class: 'mt-1' }, linkBtn('#/interview', t('nav_interview'), 'btn--sm btn--ghost'))))))));
    return { title: tb('nav_planner', null, { inline: true }), titleText: 'Study Planner', node };
  }

  /* ======================================================================
     Settings: preferences, backup, reset, data health
     ====================================================================== */
  function downloadJSON(obj, filename) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = h('a', { href: url, download: filename, style: { display: 'none' } });
    document.body.append(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 500);
  }
  function viewSettings() {
    const p = state.preferences;
    const setPref = (k, v) => { p[k] = v; saveState(); applyPreferences(); rerender(); };
    const fileInput = h('input', { type: 'file', accept: 'application/json,.json', class: 'sr-only', id: 'importFile', onchange: (e) => handleImport(e.target) });
    const row = (labelKey, hintKey, control) => h('div', { class: 'row row--between', style: { padding: '12px 0', borderBottom: '1px solid var(--border)', gap: '16px' } },
      h('div', { style: { minWidth: '200px', flex: '1' } }, h('strong', null, tb(labelKey)), hintKey ? h('div', { class: 'small muted' }, tb(hintKey)) : null), control);
    const v = VALIDATION;
    const node = frag(
      pageHead('nav_settings', 'settingsLead'),
      h('div', { class: 'grid grid--2' },
        h('section', { class: 'card' },
          h('h2', null, tb('preferences')),
          row('language', 'languageHint', seg([{ value: 'en', label: 'English' }, { value: 'bn', label: 'বাংলা', lang: 'bn' }, { value: 'both', label: t('both') }], p.lang, setLang, t('language'))),
          row('theme', null, seg([{ value: 'dark', label: t('dark') }, { value: 'light', label: t('light') }], p.theme, (v2) => setPref('theme', v2), t('theme'))),
          row('defaultMode', 'defaultModeHint', seg([{ value: 'learning', label: t('learningMode') }, { value: 'interview', label: t('interviewMode') }], p.mode, (v2) => setPref('mode', v2), t('defaultMode'))),
          row('motion', 'motionHint', seg([{ value: 'system', label: t('motionSystem') }, { value: 'reduce', label: t('motionReduce') }, { value: 'full', label: t('motionFull') }], p.motion, (v2) => setPref('motion', v2), t('motion'))),
          row('textSize', null, seg([0.9, 1, 1.1, 1.2].map((x) => ({ value: x, label: Math.round(x * 100) + '%' })), p.fontScale, (v2) => setPref('fontScale', v2), t('textSize'))),
          row('sidebar', null, seg([{ value: false, label: t('expanded') }, { value: true, label: t('collapsed') }], p.sidebarCollapsed, (v2) => setPref('sidebarCollapsed', v2), t('sidebar')))),
        h('div', { class: 'stack' },
          h('section', { class: 'card stack stack--sm' },
            h('h2', null, tb('dataBackup')),
            h('p', { class: 'small muted' }, tb('localOnlyLong')),
            h('div', { class: 'btn-row' },
              btn(t('exportData'), () => { downloadJSON(exportData(), 'interview-prep-bd-backup-' + localDateKey() + '.json'); toast(t('exported'), 'ok'); }, 'btn--secondary', 'download'),
              h('label', { class: 'btn', for: 'importFile', tabindex: '0', role: 'button', onkeydown: (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); } } }, icon('upload', 16), t('importData')),
              fileInput),
            h('p', { class: 'tiny faint mb-0' }, tb('importHint'))),
          h('section', { class: 'card stack stack--sm', style: { borderColor: 'color-mix(in srgb, var(--bad) 35%, var(--border))' } },
            h('h2', null, tb('dangerZone')),
            h('p', { class: 'small muted' }, tb('resetHint')),
            h('div', null, btn(t('resetProgress'), async () => {
              const ok = await confirmModal({ title: t('resetTitle'), message: tb('resetText'), confirmLabel: t('resetProgress'), danger: true, requireText: 'RESET' });
              if (!ok) return;
              const prefs = Object.assign({}, state.preferences);
              state = defaultState();
              state.preferences = prefs;
              saveState();
              ui.revealed.clear(); ui.hidden.clear(); ui.mcq = {};
              toast(t('progressReset'), 'ok');
              rerender();
            }, 'btn--danger', 'trash'))),
          h('section', { class: 'card stack stack--sm' },
            h('h2', null, tb('dataHealth')),
            h('dl', { class: 'kv' },
              h('dt', null, t('records')), h('dd', null, String(v.total)),
              h('dt', null, t('usableQuestions')), h('dd', null, String(QUESTIONS.length)),
              h('dt', null, t('errors')), h('dd', null, h('span', { class: 'badge ' + (v.errors.length ? 'badge--bad' : 'badge--ok') }, String(v.errors.length))),
              h('dt', null, t('warnings')), h('dd', null, h('span', { class: 'badge ' + (v.warnings.length ? 'badge--warn' : 'badge--ok') }, String(v.warnings.length)))),
            h('div', null, btn(t('showDetails'), () => openModal({
              title: t('dataHealth'),
              body: v.errors.length || v.warnings.length
                ? h('div', { style: { maxHeight: '50vh', overflow: 'auto' } }, h('ul', { class: 'small mono' }, v.errors.map((e) => h('li', { style: { color: 'var(--bad)' } }, e)), v.warnings.map((w) => h('li', { style: { color: 'var(--partial)' } }, w))))
                : h('p', null, tb('noValidationIssues')),
            }), 'btn--ghost btn--sm', 'info')),
            h('p', { class: 'tiny faint mb-0' }, tb('validationConsole'))))));
    return { title: tb('nav_settings', null, { inline: true }), titleText: 'Settings', node };
  }
  function handleImport(input) {
    const file = input.files && input.files[0];
    input.value = '';
    if (!file) return;
    if (file.size > 15 * 1024 * 1024) { toast(t('import_tooLarge'), 'bad'); return; }
    const reader = new FileReader();
    reader.onerror = () => toast(t('import_readError'), 'bad');
    reader.onload = async () => {
      const res = parseImport(String(reader.result || ''));
      if (!res.ok) { toast(t('import_' + res.error), 'bad', 5000); return; }
      const s = res.summary;
      const ok = await confirmModal({
        title: t('importConfirmTitle'),
        message: h('div', null, h('p', null, tb('importConfirmText')), h('ul', null,
          h('li', null, t('nav_bookmarks') + ': ' + s.bookmarks),
          h('li', null, t('learned') + ': ' + s.learned),
          h('li', null, t('flaggedForReview') + ': ' + s.review),
          h('li', null, t('questionsWithProgress') + ': ' + s.progress),
          h('li', null, t('sessionsWord') + ': ' + s.sessions),
          s.exportedAt ? h('li', null, t('exportedAt') + ': ' + s.exportedAt) : null)),
        confirmLabel: t('replaceMyData'), danger: true,
      });
      if (!ok) return;
      state = res.data;
      saveState();
      applyPreferences();
      toast(t('imported'), 'ok');
      rerender();
    };
    reader.readAsText(file);
  }

  /* ======================================================================
     Versions & sources
     ====================================================================== */
  function viewSources() {
    const byTech = TECHS.map((tc) => [tc, countBy(BY_TECH.get(tc.id), 'difficulty'), BY_TECH.get(tc.id).length]);
    const typeCounts = countBy(QUESTIONS, 'type');
    const marketCounts = countBy(QUESTIONS, 'market');
    const group = (g, titleKey) => h('section', { class: 'card' },
      h('h2', null, tb(titleKey)),
      h('ul', { class: 'list-plain ref-list' }, SOURCES.filter((s) => s.group === g).map((s) => h('li', null, icon('link', 14), h('a', { href: s.url, target: '_blank', rel: 'noopener noreferrer' }, s.title)))));
    const node = frag(
      pageHead('nav_sources', 'sourcesLead', null, t('verifiedOn', { date: VERIFIED_AT })),
      h('section', { class: 'card' },
        h('h2', null, tb('verifiedVersions')),
        h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
          h('thead', null, h('tr', null, h('th', null, t('technology')), h('th', null, t('version')), h('th', null, t('notes')), h('th', null, t('source')))),
          h('tbody', null, VERSIONS.map((v) => h('tr', null, h('td', null, h('strong', null, v.tech)), h('td', { class: 'wrap' }, v.version), h('td', { class: 'wrap small muted' }, v.note), h('td', null, h('a', { href: v.url, target: '_blank', rel: 'noopener noreferrer' }, t('open'), ' ', icon('external', 12)))))))),
        h('p', { class: 'small muted mt-1 mb-0' }, tb('versionsNote'))),
      h('section', { class: 'card mt-3' },
        h('h2', null, tb('bankStats')),
        h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
          h('thead', null, h('tr', null, h('th', null, t('technology')), DIFFS.map((d) => h('th', { class: 'num' }, t('diff_' + d))), h('th', { class: 'num' }, t('totalWord')))),
          h('tbody', null, byTech.map(([tc, dc, n]) => h('tr', null, h('td', null, tc.name), DIFFS.map((d) => h('td', { class: 'num' }, dc[d] || 0)), h('td', { class: 'num' }, h('strong', null, n)))),
            h('tr', null, h('td', null, h('strong', null, t('totalWord'))), DIFFS.map((d) => h('td', { class: 'num' }, h('strong', null, countBy(QUESTIONS, 'difficulty')[d] || 0))), h('td', { class: 'num' }, h('strong', null, QUESTIONS.length)))))),
        h('div', { class: 'row mt-2' }, TYPES.map((ty) => h('span', { class: 'badge' }, t('type_' + ty) + ': ' + (typeCounts[ty] || 0)))),
        h('div', { class: 'row mt-1' }, MARKETS.map((m) => h('span', { class: 'badge badge--teal' }, t('market_' + m) + ': ' + (marketCounts[m] || 0))))),
      h('div', { class: 'callout callout--warn mt-3' }, h('div', { class: 'callout__title' }, icon('alert', 16), tb('honestyTitle')), h('div', { class: 'small' }, tb('honestyText'))),
      h('div', { class: 'grid grid--3 mt-3' }, group('versions', 'srcVersions'), group('market', 'srcMarket'), group('docs', 'srcDocs')));
    return { title: tb('nav_sources', null, { inline: true }), titleText: 'Versions & Sources', node };
  }
