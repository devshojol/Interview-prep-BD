
  /* ======================================================================
     Voice: an English "interviewer" reads questions aloud with the
     browser's speech synthesis (Web Speech API). Voices come from the
     operating system or browser. Bangla is not read aloud: the built-in
     Bangla voices sound too robotic, so Bangla mode reads the English text.
     ====================================================================== */
  const VOICE_OK = typeof window !== 'undefined' && 'speechSynthesis' in window && typeof window.SpeechSynthesisUtterance === 'function';
  // Novelty and effect voices that ship with macOS; never offered or auto-picked.
  const NOVELTY_VOICES = /^(albert|bad news|bahh|bells|boing|bubbles|cellos|deranged|good news|hysterical|jester|organ|pipe organ|superstar|trinoids|whisper|wobble|zarvox|fred|junior|ralph|kathy)\b/i;
  const voice = { list: [], speaking: false, key: null, listeners: new Set(), blocked: false };

  function loadVoices() {
    if (!VOICE_OK) return [];
    voice.list = window.speechSynthesis.getVoices()
      .filter((v) => !NOVELTY_VOICES.test(v.name) && (v.lang || '').toLowerCase().replace('_', '-').startsWith('en'))
      .sort((a, b) => voiceScore(b) - voiceScore(a) || a.name.localeCompare(b.name));
    return voice.list;
  }
  if (VOICE_OK) {
    loadVoices();
    window.speechSynthesis.addEventListener('voiceschanged', () => {
      const before = voice.list.length;
      loadVoices();
      voiceNotify();
      // The settings card lists voices; redraw it once the browser has loaded them.
      if (before !== voice.list.length && currentRoute && currentRoute.name === 'settings') rerender();
    });
  }
  // Rank voices so the most natural-sounding one is the default.
  function voiceScore(v) {
    const n = v.name.toLowerCase();
    const l = (v.lang || '').toLowerCase();
    let s = 0;
    if (/natural|neural|online|premium|enhanced|siri/.test(n)) s += 50;
    if (/google/.test(n)) s += 30;
    if (/^(samantha|daniel|karen|moira|rishi|tessa|ava|zoe|evan|nathan|serena|aria|jenny|guy|sonia|ryan|libby|emma|andrew|brian)\b/.test(n)) s += 20;
    if (/^(eddy|flo|reed|rocko|sandy|shelley|grandma|grandpa)\b/.test(n)) s -= 15; // older formant voices sound robotic
    if (/en-(us|gb|in)/.test(l)) s += 5;
    if (l === 'en-us') s += 1;
    if (v.localService) s += 2;
    return s;
  }
  function chosenVoice() {
    const list = voice.list.length ? voice.list : loadVoices();
    return list.find((v) => v.name === state.preferences.voice.en) || list[0] || null;
  }

  /* Turn markdown-ish question text into something that sounds right when read aloud. */
  function cleanForSpeech(s) {
    return String(s || '')
      .replace(/```[\s\S]*?```/g, ' ')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/https?:\/\/\S+/g, ' ')
      .replace(/<\/?([a-z][a-z0-9-]*)[^<>]*>/gi, ' $1 ') // `<header>` -> header
      .replace(/\s*(→|->)\s*/g, ' to ').replace(/≥/g, ' at least ').replace(/≤/g, ' at most ')
      .replace(/!==/g, ' not strictly equal ').replace(/===/g, ' strictly equals ').replace(/!=/g, ' not equal ').replace(/==/g, ' equals ')
      .replace(/=>/g, ' arrow ').replace(/&&/g, ' and ').replace(/\|\|/g, ' or ')
      .replace(/\(\)/g, '')
      .replace(/[`*_#>]/g, '')
      .replace(/^\s*[-•]\s+/gm, '')
      .replace(/^\s*\d+\.\s+/gm, '')
      .replace(/\s*\n+\s*/g, '. ')
      .replace(/\.\s*\./g, '.')
      .replace(/\s{2,}/g, ' ')
      .replace(/\s+([,.;:!?])/g, '$1')
      .trim();
  }
  // Split long text into sentence-sized chunks: some browsers stop speaking long utterances.
  function speechChunks(text) {
    const parts = text.match(/[^.!?।]+[.!?।]*\s*/g) || [text];
    const out = [];
    let cur = '';
    parts.forEach((p) => {
      if ((cur + p).length > 220 && cur) { out.push(cur.trim()); cur = ''; }
      cur += p;
    });
    if (cur.trim()) out.push(cur.trim());
    return out;
  }

  /* What the "interviewer" says for a question (always the English text). */
  function questionSpeech(q, opts) {
    const o = opts || {};
    const parts = [];
    if (o.intro) parts.push(o.intro);
    parts.push(cleanForSpeech(q.question.en));
    if ((q.code && q.code.source && (q.type === 'output' || q.type === 'debugging' || q.type === 'mcq')) || (q.setup && q.setup.source)) {
      parts.push('Take a look at the code on your screen.');
    }
    if (q.isMCQ && o.options !== false) {
      parts.push('Your options are:');
      q.options.forEach((op, i) => parts.push('ABCD'[i] + '. ' + cleanForSpeech(op.en) + '.'));
    }
    return parts.join(' ');
  }
  function answerSpeech(q) {
    const src = q.quickAnswer || q.answer;
    let txt = cleanForSpeech(src.en);
    if (!q.quickAnswer && txt.length > 600) txt = txt.slice(0, 600).replace(/[^.!?]*$/, '');
    return txt;
  }

  /* Speak text with the chosen English voice. key identifies what is being read. */
  function speak(text, key) {
    if (!VOICE_OK || !text) return false;
    const v = chosenVoice();
    if (!v) return false;
    const synth = window.speechSynthesis;
    synth.cancel();
    const chunks = speechChunks(text);
    voice.key = key || null;
    voice.speaking = true;
    voice.blocked = false;
    voiceNotify();
    const rate = state.preferences.voice.rate;
    chunks.forEach((chunk, i) => {
      const u = new SpeechSynthesisUtterance(chunk);
      u.voice = v;
      u.lang = v.lang;
      u.rate = rate;
      u.pitch = 1;
      if (i === chunks.length - 1) u.onend = () => { if (voice.key === (key || null)) { voice.speaking = false; voice.key = null; voiceNotify(); } };
      u.onerror = (e) => {
        if (e && e.error === 'not-allowed') voice.blocked = true; // autoplay policy: needs a click first
        if (e && (e.error === 'interrupted' || e.error === 'canceled')) return;
        voice.speaking = false; voice.key = null; voiceNotify();
      };
      synth.speak(u);
    });
    // Chrome can leave the queue paused after a tab switch; resume defensively.
    if (synth.paused) synth.resume();
    return true;
  }
  function stopSpeaking() {
    if (!VOICE_OK) return;
    window.speechSynthesis.cancel();
    if (voice.speaking) { voice.speaking = false; voice.key = null; voiceNotify(); }
  }
  function speakQuestion(q, key, opts) { return speak(questionSpeech(q, opts), key); }
  function speakAnswer(q, key) { return speak(answerSpeech(q), key); }
  function toggleSpeak(key, start) {
    if (voice.speaking && voice.key === key) { stopSpeaking(); return; }
    start();
  }
  function voiceNotify() { voice.listeners.forEach((fn) => { try { fn(); } catch (e) { /* detached */ } }); }
  function autoReadOn(where) { return VOICE_OK && !!state.preferences.voice.auto[where]; }

  /* "Listen" pill: speaker icon, label, and animated bars while speaking. Updates itself. */
  function speakButton(key, start, opts) {
    const o = opts || {};
    if (!VOICE_OK) return null;
    const label = h('span', { class: 'speak-btn__label' });
    const b = h('button', { type: 'button', class: 'speak-btn' + (o.compact ? ' speak-btn--compact' : ''), 'aria-keyshortcuts': o.shortcut === false ? null : 'V',
      onclick: (e) => { e.stopPropagation(); toggleSpeak(key, start); } },
    h('span', { class: 'speak-btn__icon', 'aria-hidden': 'true' }, icon('speaker', 16), h('span', { class: 'eq' }, h('i'), h('i'), h('i'), h('i'))),
    label);
    const sync = () => {
      if (!b.isConnected && b._mounted) { voice.listeners.delete(sync); return; }
      b._mounted = b._mounted || b.isConnected;
      const on = voice.speaking && voice.key === key;
      b.classList.toggle('is-speaking', on);
      b.classList.toggle('is-blocked', voice.blocked && !on);
      b.setAttribute('aria-pressed', String(on));
      const txt = on ? t('voiceStop') : (o.label || t('voiceListen'));
      label.textContent = o.compact ? '' : txt;
      b.setAttribute('aria-label', txt + (o.shortcut === false ? '' : ' (V)'));
      b.title = txt + (o.shortcut === false ? '' : ' (V)');
    };
    voice.listeners.add(sync);
    sync();
    return b;
  }

  /* Interviewer bar used in interview simulation and the daily challenge. */
  function interviewerBar(key, start, autoKey) {
    if (!VOICE_OK) return null;
    const status = h('span', { class: 'interviewer__status' });
    const wave = h('span', { class: 'wave', 'aria-hidden': 'true' }, h('i'), h('i'), h('i'), h('i'), h('i'));
    const autoBtn = h('button', { type: 'button', class: 'interviewer__auto', 'aria-pressed': String(autoReadOn(autoKey)),
      onclick: () => {
        state.preferences.voice.auto[autoKey] = !state.preferences.voice.auto[autoKey];
        saveState();
        if (!state.preferences.voice.auto[autoKey]) stopSpeaking();
        sync();
      } });
    const replay = speakButton(key, start, { label: t('voiceReplay') });
    const bar = h('div', { class: 'interviewer', role: 'group', 'aria-label': t('voiceInterviewer') },
      h('span', { class: 'interviewer__avatar', 'aria-hidden': 'true' }, icon('mic', 18)),
      h('div', { class: 'interviewer__text' }, h('strong', null, t('voiceInterviewer')), h('span', { class: 'row', style: { gap: '8px' } }, wave, status)),
      h('div', { class: 'interviewer__actions' }, autoBtn, replay));
    const sync = () => {
      if (!bar.isConnected && bar._mounted) { voice.listeners.delete(sync); return; }
      bar._mounted = bar._mounted || bar.isConnected;
      const on = voice.speaking && voice.key === key;
      bar.classList.toggle('is-speaking', on);
      status.textContent = on ? t('voiceAsking') : voice.blocked ? t('voiceTapToHear') : t('voiceYourTurn');
      const auto = autoReadOn(autoKey);
      autoBtn.setAttribute('aria-pressed', String(auto));
      clear(autoBtn);
      autoBtn.append(icon(auto ? 'speaker' : 'speakerOff', 15), h('span', null, auto ? t('voiceAutoOn') : t('voiceAutoOff')));
      autoBtn.title = t('voiceAutoHint');
    };
    voice.listeners.add(sync);
    sync();
    return bar;
  }

  function speakTest() { return speak(tLang('voiceTestText', 'en'), 'voice:test'); }

  /* Settings card: English voice, speed and where questions are read automatically. */
  function voiceSettingsCard() {
    const v = state.preferences.voice;
    const set = (fn) => { fn(v); saveState(); rerender(); };
    const head = h('div', { class: 'row row--between' }, h('h2', { class: 'row', style: { margin: 0, gap: '8px' } }, icon('speaker', 20), tb('voiceSettings', null, { inline: true })),
      VOICE_OK && voice.list.length ? speakButton('voice:test', speakTest, { label: t('voiceTest'), shortcut: false }) : null);
    if (!VOICE_OK) return h('section', { class: 'card stack stack--sm voice-card' }, head, h('p', { class: 'small muted' }, tb('voiceUnsupported')));
    const list = voice.list.length ? voice.list : loadVoices();
    const places = [['interview', 'nav_interview'], ['daily', 'nav_daily'], ['practice', 'nav_practice'], ['flashcards', 'nav_flashcards']];
    return h('section', { class: 'card stack stack--sm voice-card' },
      head,
      h('p', { class: 'small muted mb-0' }, tb('voiceLead')),
      list.length ? h('div', { class: 'field' }, h('label', { for: 'voice-en' }, t('voiceEnglish')),
        h('select', { class: 'select', id: 'voice-en', onchange: (e) => set((p) => { p.en = e.target.value; }) },
          h('option', { value: '', selected: !v.en }, t('voiceBest') + ': ' + list[0].name),
          list.map((x) => h('option', { value: x.name, selected: v.en === x.name }, x.name + ' · ' + x.lang + (x.localService ? '' : ' · online')))))
        : h('p', { class: 'voice-note' }, icon('alert', 13), ' ', tb('voiceNone')),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('voiceSpeed')),
        seg([{ value: 0.85, label: t('voiceSlow') }, { value: 1, label: t('voiceNormal') }, { value: 1.15, label: t('voiceFast') }], v.rate, (x) => set((p) => { p.rate = x; }), t('voiceSpeed'))),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('voiceAutoRead')),
        h('div', { class: 'chip-group' }, places.map(([k, label]) => chip(t(label), v.auto[k], () => set((p) => { p.auto[k] = !p.auto[k]; })))),
        h('p', { class: 'voice-note' }, tb('voiceAutoReadHint'))),
      h('p', { class: 'voice-note' }, icon('info', 13), ' ', tb('voiceEnglishOnly')),
      h('p', { class: 'voice-note' }, icon('info', 13), ' ', tb('voicePrivacy')));
  }
