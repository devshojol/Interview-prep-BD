
  /* ======================================================================
     Question bank: normalisation, validation, indexing, search
     ====================================================================== */
  function biObj(v) {
    if (isStr(v)) return { en: v, bn: '' };
    if (!isObj(v)) return { en: '', bn: '' };
    return { en: isStr(v.en) ? v.en : '', bn: isStr(v.bn) ? v.bn : '' };
  }
  function codeObj(v) {
    if (!isObj(v)) return null;
    const source = isStr(v.source) ? v.source : '';
    const output = isStr(v.output) ? v.output : '';
    if (!source && !output) return null;
    return { language: isStr(v.language) ? v.language : 'text', source, output };
  }

  function normalizeQuestion(raw) {
    if (!isObj(raw) || !isStr(raw.id) || !raw.id) return null;
    const q = {
      id: raw.id,
      technology: TECH_MAP.has(raw.technology) ? raw.technology : null,
      subtopic: isStr(raw.subtopic) ? raw.subtopic : 'General',
      difficulty: DIFFS.includes(raw.difficulty) ? raw.difficulty : 'medium',
      type: TYPES.includes(raw.type) ? raw.type : 'conceptual',
      market: MARKETS.includes(raw.market) ? raw.market : 'both',
      priority: PRIORITIES.includes(raw.priority) ? raw.priority : 'medium',
      estimatedMinutes: Number.isFinite(raw.estimatedMinutes) ? clamp(Math.round(raw.estimatedMinutes), 1, 60) : 3,
      tags: Array.isArray(raw.tags) ? raw.tags.filter(isStr) : [],
      technologyVersion: isStr(raw.technologyVersion) ? raw.technologyVersion : 'Version-independent concept',
      verifiedAt: isStr(raw.verifiedAt) ? raw.verifiedAt : '',
      versionSensitive: raw.versionSensitive === true,
      status: isStr(raw.status) ? raw.status : 'stable',
      question: biObj(raw.question),
      answer: biObj(raw.answer),
      explanation: biObj(raw.explanation),
      interviewTip: biObj(raw.interviewTip),
      commonMistakes: raw.commonMistakes ? biObj(raw.commonMistakes) : null,
      code: codeObj(raw.code),
      setup: codeObj(raw.setup),
      extraCode: Array.isArray(raw.extraCode)
        ? raw.extraCode.filter(isObj).map((x) => ({ language: isStr(x.language) ? x.language : 'text', source: isStr(x.source) ? x.source : '', label: biObj(x.label) })).filter((x) => x.source)
        : [],
      followUps: Array.isArray(raw.followUps) ? raw.followUps.map(biObj).filter((f) => f.en || f.bn) : [],
      related: Array.isArray(raw.related) ? raw.related.filter(isStr) : [],
      references: Array.isArray(raw.references)
        ? raw.references.filter((r) => isObj(r) && isStr(r.url) && /^https:\/\//.test(r.url)).map((r) => ({ title: isStr(r.title) && r.title ? r.title : r.url, url: r.url }))
        : [],
      options: Array.isArray(raw.options) ? raw.options.map(biObj) : null,
      correctIndex: Number.isInteger(raw.correctIndex) ? raw.correctIndex : null,
      complexity: isObj(raw.complexity) ? { time: String(raw.complexity.time || ''), space: String(raw.complexity.space || '') } : null,
    };
    q.documentationUrl = isStr(raw.documentationUrl) && raw.documentationUrl ? raw.documentationUrl : (q.references[0] ? q.references[0].url : (TECH_MAP.get(q.technology) || {}).docs || '');
    q.isMCQ = q.type === 'mcq' && Array.isArray(q.options) && q.options.length >= 2 && q.correctIndex != null && q.correctIndex >= 0 && q.correctIndex < q.options.length;
    if (q.type === 'mcq' && !q.isMCQ) q.type = 'conceptual'; // malformed MCQ degrades gracefully
    return q;
  }

  /* Development-time validator: reports problems in the console, never throws. */
  function validateBank(rawList) {
    const errors = [];
    const warnings = [];
    const ids = new Map();
    const list = Array.isArray(rawList) ? rawList : [];
    if (!Array.isArray(rawList)) errors.push('window.QBANK is missing or not an array.');
    const BN = /[ঀ-৿]/;
    list.forEach((q, i) => {
      const where = (q && q.id) ? q.id : ('#' + i);
      if (!isObj(q)) { errors.push(where + ': record is not an object'); return; }
      if (!isStr(q.id) || !q.id) errors.push(where + ': missing id');
      else ids.set(q.id, (ids.get(q.id) || 0) + 1);
      if (!TECH_MAP.has(q.technology)) errors.push(where + ': unknown technology "' + q.technology + '"');
      if (!DIFFS.includes(q.difficulty)) errors.push(where + ': invalid difficulty "' + q.difficulty + '"');
      if (!TYPES.includes(q.type)) errors.push(where + ': invalid type "' + q.type + '"');
      if (!MARKETS.includes(q.market)) errors.push(where + ': invalid market "' + q.market + '"');
      ['question', 'answer', 'explanation'].forEach((f) => {
        const o = q[f];
        if (!isObj(o) || !o.en) errors.push(where + ': missing English ' + f);
        if (!isObj(o) || !o.bn) errors.push(where + ': missing Bangla ' + f);
        else if (!BN.test(o.bn)) warnings.push(where + ': Bangla ' + f + ' contains no Bangla characters');
      });
      if (!isObj(q.interviewTip) || !q.interviewTip.en || !q.interviewTip.bn) warnings.push(where + ': interview tip missing a language');
      if (!isStr(q.technologyVersion) || !q.technologyVersion) errors.push(where + ': missing technologyVersion');
      if (q.versionSensitive && !/\d/.test(q.technologyVersion || '')) errors.push(where + ': versionSensitive but technologyVersion has no version number');
      if (!isStr(q.verifiedAt) || !/^\d{4}-\d{2}-\d{2}$/.test(q.verifiedAt)) warnings.push(where + ': missing/invalid verifiedAt');
      if (!Array.isArray(q.references) || !q.references.length) warnings.push(where + ': no documentation references');
      if (q.type === 'mcq') {
        if (!Array.isArray(q.options) || q.options.length !== 4) errors.push(where + ': MCQ must have 4 options');
        else q.options.forEach((o, k) => { if (!isObj(o) || !o.en || !o.bn) errors.push(where + ': MCQ option ' + k + ' missing a language'); });
        if (!Number.isInteger(q.correctIndex) || !q.options || q.correctIndex < 0 || q.correctIndex >= q.options.length) errors.push(where + ': MCQ correctIndex does not reference an option');
      }
      if (q.type === 'output' && !(isObj(q.code) && q.code.output)) errors.push(where + ': output question without expected output');
    });
    for (const [id, n] of ids) if (n > 1) errors.push(id + ': duplicate id (' + n + ' records)');
    list.forEach((q) => {
      if (isObj(q) && Array.isArray(q.related)) q.related.forEach((r) => { if (!ids.has(r)) errors.push(q.id + ': broken related reference "' + r + '"'); });
    });
    return { errors, warnings, total: list.length };
  }

  const RAW_BANK = Array.isArray(window.QBANK) ? window.QBANK : [];
  const VALIDATION = validateBank(window.QBANK);
  const QUESTIONS = [];
  const QMAP = new Map();
  for (const raw of RAW_BANK) {
    let q = null;
    try { q = normalizeQuestion(raw); } catch (e) { q = null; }
    if (!q || !q.technology || QMAP.has(q.id)) continue;
    QUESTIONS.push(q);
    QMAP.set(q.id, q);
  }
  // Stable display order: technology order, then difficulty, then id
  const TECH_ORDER = new Map(TECHS.map((t, i) => [t.id, i]));
  QUESTIONS.sort((a, b) => (TECH_ORDER.get(a.technology) - TECH_ORDER.get(b.technology)) || (DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty)) || a.id.localeCompare(b.id, 'en', { numeric: true }));
  QUESTIONS.forEach((q, i) => {
    q._order = i;
    const t = TECH_MAP.get(q.technology);
    q._sTitle = normalizeText(q.question.en + ' \n ' + q.question.bn);
    q._sMeta = normalizeText([q.subtopic, q.tags.join(' '), q.id, t ? t.name : '', q.type].join(' '));
    q._sBody = normalizeText([q.answer.en, q.answer.bn, q.explanation.en, q.explanation.bn].join(' '));
  });
  const BY_TECH = new Map(TECHS.map((t) => [t.id, []]));
  QUESTIONS.forEach((q) => BY_TECH.get(q.technology).push(q));

  function logValidation() {
    try {
      const v = VALIDATION;
      const label = '[Interview Prep BD] Question bank validation: ' + QUESTIONS.length + ' usable / ' + v.total + ' records, ' + v.errors.length + ' errors, ' + v.warnings.length + ' warnings';
      if (v.errors.length || v.warnings.length) {
        console.groupCollapsed(label);
        v.errors.forEach((e) => console.error(e));
        v.warnings.forEach((w) => console.warn(w));
        console.groupEnd();
      } else {
        console.info(label);
      }
    } catch (e) { /* console unavailable */ }
  }

  /* Search: every term must match somewhere; title matches rank higher. */
  function searchScore(q, terms) {
    let score = 0;
    for (const term of terms) {
      if (q._sTitle.includes(term)) score += 3;
      else if (q._sMeta.includes(term)) score += 2;
      else if (q._sBody.includes(term)) score += 1;
      else return 0;
    }
    return score;
  }
  function searchTerms(text) {
    return normalizeText(text).split(/\s+/).map((s) => s.trim()).filter(Boolean);
  }

  function countBy(list, key) {
    const out = {};
    for (const q of list) out[q[key]] = (out[q[key]] || 0) + 1;
    return out;
  }
