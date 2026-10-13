
  /* ======================================================================
     i18n helpers (dictionary lives in 35-i18n.js)
     ====================================================================== */
  const lang = () => state.preferences.lang;
  function fill(str, vars) {
    if (!vars) return str;
    // {s} → English plural suffix for {n}
    return String(str).replace(/\{(\w+)\}/g, (m, k) => (vars[k] != null ? vars[k] : k === 's' && vars.n != null ? (Number(vars.n) === 1 ? '' : 's') : m));
  }
  /** Single-language UI string (Both mode → English, used for buttons, aria labels, titles). */
  function t(key, vars) {
    const e = I18N[key];
    if (!e) { if (window.console) console.warn('[i18n] missing key', key); return key; }
    const s = lang() === 'bn' ? (e.bn || e.en) : e.en;
    return fill(s, vars);
  }
  function tLang(key, lg, vars) { const e = I18N[key]; if (!e) return key; return fill(lg === 'bn' ? (e.bn || e.en) : e.en, vars); }
  /** Bilingual-aware node: in Both mode shows English with Bangla underneath. */
  function tb(key, vars, opts) {
    const L = lang();
    if (L !== 'both') return h('span', { lang: L === 'bn' ? 'bn' : 'en', class: L === 'bn' ? 'bn' : null }, inline(t(key, vars)));
    const inlineMode = opts && opts.inline;
    return h('span', { class: 'tb' },
      h('span', { lang: 'en' }, inline(tLang(key, 'en', vars))),
      inlineMode ? ' · ' : h('br'),
      h('span', { lang: 'bn', class: 'bn muted', style: { fontSize: inlineMode ? 'inherit' : '.88em' } }, inline(tLang(key, 'bn', vars))));
  }
  /** Pick text from a {en,bn} object for single-line contexts. */
  function pick(obj) {
    if (!obj) return '';
    if (lang() === 'bn') return obj.bn || obj.en || '';
    return obj.en || obj.bn || '';
  }

  /* ======================================================================
     Formatting
     ====================================================================== */
  const pct = (x) => (x == null || !Number.isFinite(x) ? '—' : Math.round(x * 100) + '%');
  const fmtNum = (n) => (Number.isFinite(n) ? (Math.round(n * 10) / 10).toLocaleString('en-US') : '—');
  function fmtDuration(ms) {
    const s = Math.max(0, Math.round(ms / 1000));
    const hh = Math.floor(s / 3600), mm = Math.floor((s % 3600) / 60), ss = s % 60;
    if (hh) return hh + 'h ' + String(mm).padStart(2, '0') + 'm';
    return mm + 'm ' + String(ss).padStart(2, '0') + 's';
  }
  function fmtClock(ms) {
    const s = Math.max(0, Math.round(ms / 1000));
    const mm = Math.floor(s / 60), ss = s % 60;
    return String(mm).padStart(2, '0') + ':' + String(ss).padStart(2, '0');
  }
  function fmtDate(ts, withTime) {
    if (!ts) return '—';
    const loc = lang() === 'bn' ? 'bn-BD' : 'en-GB';
    const opts = withTime ? { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' } : { day: 'numeric', month: 'short', year: 'numeric' };
    try { return new Date(ts).toLocaleString(loc, opts); } catch (e) { return new Date(ts).toISOString().slice(0, 10); }
  }
  function fmtDay(key) {
    try { return new Date(key + 'T00:00:00').toLocaleDateString(lang() === 'bn' ? 'bn-BD' : 'en-GB', { weekday: 'short' }); } catch (e) { return key.slice(5); }
  }

  /* ======================================================================
     Rich text (safe subset: paragraphs, lists, `code`, **bold**, ``` fences)
     ====================================================================== */
  function inline(text) {
    const out = [];
    const s = String(text || '');
    // `code`, **bold**, *emphasis* (single asterisks must hug the text, so "a * b * c" stays literal)
    const re = /(`[^`\n]+`|\*\*[^*\n]+?\*\*|(?<![\w*])\*(?![\s*])[^*\n]+?(?<![\s*])\*(?![\w*]))/g;
    let last = 0, m;
    while ((m = re.exec(s))) {
      if (m.index > last) out.push(s.slice(last, m.index));
      const tok = m[0];
      if (tok[0] === '`') out.push(h('code', null, tok.slice(1, -1)));
      else if (tok.startsWith('**')) out.push(h('strong', null, inline(tok.slice(2, -2))));
      else out.push(h('em', null, inline(tok.slice(1, -1))));
      last = m.index + tok.length;
    }
    if (last < s.length) out.push(s.slice(last));
    return out;
  }
  function renderRich(text) {
    const root = document.createDocumentFragment();
    const lines = String(text || '').replace(/\r\n?/g, '\n').split('\n');
    let para = [];
    const flush = () => { if (para.length) { root.append(h('p', null, inline(para.join(' ')))); para = []; } };
    const BUL = /^\s*[-*•]\s+/;
    const NUM = /^\s*\d+[.)]\s+/;
    let i = 0;
    while (i < lines.length) {
      const line = lines[i];
      if (/^\s*```/.test(line)) {
        flush();
        const lg = line.replace(/^\s*```/, '').trim() || 'text';
        const buf = [];
        i++;
        while (i < lines.length && !/^\s*```/.test(lines[i])) { buf.push(lines[i]); i++; }
        i++;
        root.append(codeBlock({ language: lg, source: buf.join('\n') }));
        continue;
      }
      if (BUL.test(line) || NUM.test(line)) {
        flush();
        const ordered = NUM.test(line);
        const list = h(ordered ? 'ol' : 'ul');
        const MARK = ordered ? NUM : BUL;
        while (i < lines.length && MARK.test(lines[i])) {
          let item = lines[i].replace(MARK, '');
          i++;
          while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !BUL.test(lines[i]) && !NUM.test(lines[i])) { item += ' ' + lines[i].trim(); i++; }
          list.append(h('li', null, inline(item)));
        }
        root.append(list);
        continue;
      }
      if (!line.trim()) { flush(); i++; continue; }
      if (/^#{1,4}\s+/.test(line)) { flush(); root.append(h('p', null, h('strong', null, inline(line.replace(/^#{1,4}\s+/, ''))))); i++; continue; }
      para.push(line.trim());
      i++;
    }
    flush();
    return root;
  }

  /** Shows a {en,bn} text according to the language preference. */
  function biText(obj, opts) {
    const o = opts || {};
    const L = lang();
    const en = obj && obj.en, bn = obj && obj.bn;
    const make = (txt, lg) => {
      const el = h(o.tag || 'div', { class: (o.cls || 'prose') + (lg === 'bn' ? ' bn' : ''), lang: lg });
      if (o.plain) append(el, inline(txt)); else el.append(renderRich(txt));
      return el;
    };
    if (L === 'both' && en && bn) {
      return h('div', { class: 'bi-block' },
        h('div', { class: 'bi-pane' }, o.noLabels ? null : h('span', { class: 'bi-label', 'aria-hidden': 'true' }, 'English'), make(en, 'en')),
        h('div', { class: 'bi-pane' }, o.noLabels ? null : h('span', { class: 'bi-label', 'aria-hidden': 'true' }, 'বাংলা'), make(bn, 'bn')));
    }
    if (L === 'bn') {
      if (bn) return make(bn, 'bn');
      return h('div', null, make(en || '', 'en'), h('p', { class: 'tiny faint' }, t('noTranslation')));
    }
    return make(en || bn || '', en ? 'en' : 'bn');
  }
  /** Compact title text (inline only) for lists. */
  function biTitle(obj, cls) {
    const L = lang();
    if (L === 'both' && obj.en && obj.bn) {
      return h('span', { class: cls || null }, h('span', { lang: 'en' }, inline(obj.en)), h('span', { class: 'bn', lang: 'bn' }, inline(obj.bn)));
    }
    if (L === 'bn' && obj.bn) return h('span', { class: (cls ? cls + ' ' : '') + 'bn', lang: 'bn' }, inline(obj.bn));
    return h('span', { class: cls || null, lang: 'en' }, inline(obj.en || obj.bn || ''));
  }

  /* ======================================================================
     Code blocks with a tiny, safe syntax highlighter
     ====================================================================== */
  const KW = {
    js: new Set('abstract as async await break case catch class const continue debugger declare default delete do else enum export extends false finally for from function get if implements import in infer instanceof interface keyof let namespace new null of override private protected public readonly return satisfies set static super switch this throw true try type typeof undefined using var void while with yield'.split(' ')),
    sql: new Set('add all alter analyze and any as asc begin between by cascade case check coalesce column commit concurrently constraint create cross current_date current_timestamp database default delete desc distinct do drop else end except exists explain false fetch filter first following foreign from full function generated group having if ilike in index inner insert intersect into is join key last lateral left like limit materialized not null nulls offset on or order outer over partition preceding primary procedure range recursive references replace returning returns right rollback row rows savepoint select serializable set table then to transaction trigger true truncate unbounded union unique update using values view when where window with without'.split(' ')),
    sh: new Set('if then else elif fi for in do done while case esac function return export local echo sudo cd npm npx node docker git curl apt yarn pnpm kubectl aws psql redis-cli mongosh nginx systemctl set unset'.split(' ')),
    docker: new Set('FROM AS RUN CMD LABEL EXPOSE ENV ADD COPY ENTRYPOINT VOLUME USER WORKDIR ARG ONBUILD STOPSIGNAL HEALTHCHECK SHELL'.split(' ')),
    py: new Set('and as assert async await break class continue def del elif else except False finally for from global if import in is lambda None nonlocal not or pass raise return True try while with yield'.split(' ')),
    nginx: new Set('server location upstream http events listen server_name root index proxy_pass proxy_set_header proxy_http_version proxy_read_timeout proxy_connect_timeout proxy_send_timeout proxy_cache proxy_cache_path proxy_cache_valid proxy_buffering return rewrite try_files include worker_processes worker_connections ssl_certificate ssl_certificate_key ssl_protocols http2 http3 gzip gzip_types limit_req limit_req_zone limit_conn limit_conn_zone client_max_body_size keepalive_timeout access_log error_log map add_header expires least_conn ip_hash hash if set alias default_type sendfile'.split(' ')),
  };
  function langFamily(lg) {
    const l = String(lg || '').toLowerCase();
    if (['js', 'javascript', 'jsx', 'ts', 'typescript', 'tsx', 'mjs', 'cjs', 'json', 'node'].includes(l)) return 'js';
    if (['sql', 'psql', 'postgresql', 'pgsql', 'plpgsql'].includes(l)) return 'sql';
    if (['bash', 'sh', 'shell', 'zsh', 'console', 'terminal'].includes(l)) return 'sh';
    if (['dockerfile', 'docker'].includes(l)) return 'docker';
    if (['yaml', 'yml'].includes(l)) return 'yaml';
    if (['html', 'xml', 'svg', 'vue'].includes(l)) return 'html';
    if (['css', 'scss'].includes(l)) return 'css';
    if (['nginx', 'conf'].includes(l)) return 'nginx';
    if (['python', 'py'].includes(l)) return 'py';
    return 'plain';
  }
  const HL_RE = {
    js: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|('(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*"|`(?:\\[\s\S]|[^`\\])*`)|(\b(?:0x[\da-fA-F]+|\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?n?)\b)|([A-Za-z_$][\w$]*)(?=\s*\()|([A-Za-z_$][\w$]*)/g,
    sql: /(--[^\n]*|\/\*[\s\S]*?\*\/)|('(?:''|[^'])*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][\w]*)(?=\s*\()|([A-Za-z_][\w]*)/g,
    sh: /(#[^\n]*)|('[^'\n]*'|"(?:\\.|[^"\\\n])*")|(\b\d+\b)|(\$\{?[\w]+\}?)|([A-Za-z_][\w-]*)/g,
    docker: /(#[^\n]*)|('[^'\n]*'|"(?:\\.|[^"\\\n])*")|(\b\d+\b)|(\$\{?[\w]+\}?)|([A-Za-z_][\w-]*)/g,
    py: /(#[^\n]*)|('''[\s\S]*?'''|"""[\s\S]*?"""|'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*")|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)(?=\s*\()|([A-Za-z_]\w*)/g,
    nginx: /(#[^\n]*)|('[^'\n]*'|"[^"\n]*")|(\b\d+[kmsKMGhd]?\b)|(\$[\w]+)|([A-Za-z_][\w]*)/g,
    yaml: /(#[^\n]*)|('[^'\n]*'|"(?:\\.|[^"\\\n])*")|(\b\d+(?:\.\d+)?\b)|(^\s*-?\s*[\w.\-/]+(?=:))|(\b(?:true|false|null|yes|no)\b)/gm,
    html: /(<[!]--[\s\S]*?-->)|("[^"]*"|'[^']*')|(<\/?[A-Za-z][\w-]*|\/?>)|([A-Za-z_:@][\w\-:.]*)(?==)/g,
    css: /(\/\*[\s\S]*?\*\/)|("[^"]*"|'[^']*')|(#[\da-fA-F]{3,8}\b|-?\b\d+(?:\.\d+)?(?:px|rem|em|%|vh|vw|dvh|svh|lvh|s|ms|fr|deg|ch|lh|cqi|cqw)?\b)|([\w-]+)(?=\s*:[^;{}\n]*;)|(@[\w-]+|!important)/g,
  };
  function classify(fam, m) {
    switch (fam) {
      case 'js': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return KW.js.has(m[4]) ? 'kw' : 'fn'; if (m[5]) return KW.js.has(m[5]) ? 'kw' : null; return null;
      case 'sql': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return KW.sql.has(m[4].toLowerCase()) ? 'kw' : 'fn'; if (m[5]) return KW.sql.has(m[5].toLowerCase()) ? 'kw' : null; return null;
      case 'sh': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return KW.sh.has(m[5]) ? 'kw' : null; return null;
      case 'docker': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return KW.docker.has(m[5]) ? 'kw' : null; return null;
      case 'py': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return KW.py.has(m[4]) ? 'kw' : 'fn'; if (m[5]) return KW.py.has(m[5]) ? 'kw' : null; return null;
      case 'nginx': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return KW.nginx.has(m[5]) ? 'kw' : null; return null;
      case 'yaml': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return 'kw'; return null;
      case 'html': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'tag'; if (m[4]) return 'attr'; return null;
      case 'css': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return 'kw'; return null;
      default: return null;
    }
  }
  function highlight(src, lg) {
    const f = document.createDocumentFragment();
    const fam = langFamily(lg);
    const base = HL_RE[fam];
    const text = String(src || '');
    if (!base || text.length > 20000) { f.append(text); return f; }
    const re = new RegExp(base.source, base.flags);
    let last = 0, m;
    while ((m = re.exec(text))) {
      if (!m[0]) { re.lastIndex++; continue; }
      if (m.index > last) f.append(text.slice(last, m.index));
      const cls = classify(fam, m);
      f.append(cls ? h('span', { class: 'tok-' + cls }, m[0]) : m[0]);
      last = m.index + m[0].length;
    }
    if (last < text.length) f.append(text.slice(last));
    return f;
  }

  async function copyText(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return true; }
    } catch (e) { /* fall through */ }
    try {
      const ta = h('textarea', { style: { position: 'fixed', top: '-1000px', opacity: '0' }, 'aria-hidden': 'true' });
      ta.value = text;
      document.body.append(ta);
      ta.select();
      const ok = document.execCommand('copy');
      ta.remove();
      return ok;
    } catch (e) { return false; }
  }

  function codeBlock(code, opts) {
    const o = opts || {};
    const isOut = !!o.output;
    const text = isOut ? code.output : code.source;
    const copyBtn = h('button', {
      class: 'copy-btn', type: 'button', 'aria-label': t('copyCode'),
      onclick: async () => {
        const ok = await copyText(text);
        copyBtn.textContent = ok ? t('copied') : t('copyFailed');
        setTimeout(() => { copyBtn.textContent = t('copy'); }, 1500);
      },
    }, t('copy'));
    const label = o.label ? h('span', { class: 'code__label' }, o.label) : null;
    return h('figure', { class: 'code' + (isOut ? ' code--output' : '') },
      h('div', { class: 'code__bar' },
        h('span', { class: 'row', style: { gap: '8px' } }, label, h('span', { class: 'code__lang' }, isOut ? t('expectedOutput') : (code.language || 'text'))),
        copyBtn),
      h('pre', { tabindex: '0', 'aria-label': isOut ? t('expectedOutput') : t('codeExample') }, h('code', null, isOut ? text : highlight(text, code.language))));
  }

  /* ======================================================================
     Badges & small components
     ====================================================================== */
  function diffBadge(d) {
    const n = DIFFS.indexOf(d) + 1;
    return h('span', { class: 'badge badge--' + d, title: t('difficulty') + ': ' + t('diff_' + d) },
      h('span', { class: 'pips', 'aria-hidden': 'true' }, [1, 2, 3, 4].map((k) => h('i', { class: k <= n ? 'on' : null }))),
      t('diff_' + d));
  }
  const typeBadge = (ty) => h('span', { class: 'badge', title: t('questionType') }, t('type_' + ty));
  function marketBadge(m) {
    if (m === 'both') return h('span', { class: 'badge', title: t('market') }, icon('globe', 12), t('market_both'));
    return h('span', { class: 'badge badge--teal', title: t('market') }, icon('globe', 12), t('market_' + m));
  }
  const priorityBadge = (p) => h('span', { class: 'badge' + (p === 'high' ? ' badge--primary' : ''), title: t('priority') }, icon('star', 12), t('prio_' + p));
  function techBadge(id) {
    const tc = TECH_MAP.get(id);
    if (!tc) return null;
    return h('span', { class: 'badge' }, h('span', { 'aria-hidden': 'true', style: { width: '8px', height: '8px', borderRadius: '50%', background: tc.color, display: 'inline-block' } }), tc.name);
  }
  function resultBadge(r) {
    if (!r) return h('span', { class: 'badge' }, t('res_none'));
    const cls = { correct: 'ok', partial: 'partial', incorrect: 'bad', skipped: '' }[r];
    const ic = { correct: 'check', partial: 'half', incorrect: 'x', skipped: 'skip' }[r];
    return h('span', { class: 'badge' + (cls ? ' badge--' + cls : '') }, icon(ic, 12), t('res_' + r));
  }
  function featureStatusBadge(s) {
    if (!s || s === 'stable') return h('span', { class: 'badge badge--ok' }, t('st_stable'));
    return h('span', { class: 'badge badge--warn' }, icon('alert', 12), I18N['st_' + s] ? t('st_' + s) : s);
  }
  function techLogo(tc, size) {
    return h('span', { class: size === 'sm' ? 'tech-dot' : 'tech-card__logo', style: { background: tc.color }, 'aria-hidden': 'true' }, tc.short);
  }
  function progressBar(fraction, opts) {
    const o = opts || {};
    const v = clamp(fraction || 0, 0, 1);
    return h('div', { class: 'progress' + (o.thin ? ' progress--thin' : '') + (o.lg ? ' progress--lg' : ''), role: 'progressbar', 'aria-valuemin': '0', 'aria-valuemax': '100', 'aria-valuenow': String(Math.round(v * 100)), 'aria-label': o.label || t('progress') },
      h('span', { style: { width: (v * 100).toFixed(1) + '%' } }));
  }
  function stat(label, value, opts) {
    const o = opts || {};
    return h('div', { class: 'stat' + (o.tone ? ' stat--' + o.tone : '') },
      h('div', { class: 'stat__label' }, label),
      h('div', { class: 'stat__value' }, value),
      o.hint ? h('div', { class: 'stat__hint' }, o.hint) : null);
  }
  function emptyState(iconName, titleKey, textKey, actions) {
    return h('div', { class: 'empty' },
      h('div', { class: 'empty__icon' }, icon(iconName || 'info', 26)),
      h('h3', null, tb(titleKey)),
      textKey ? h('p', null, tb(textKey)) : null,
      actions ? h('div', { class: 'btn-row', style: { justifyContent: 'center' } }, actions) : null);
  }
  function linkBtn(href, label, cls, ic) {
    return h('a', { class: 'btn ' + (cls || ''), href }, ic ? icon(ic, 16) : null, label);
  }
  function btn(label, onClick, cls, ic, extra) {
    return h('button', Object.assign({ type: 'button', class: 'btn ' + (cls || ''), onclick: onClick }, extra || {}), ic ? icon(ic, 16) : null, label);
  }
  function seg(options, current, onChange, ariaLabel) {
    const wrap = h('div', { class: 'seg', role: 'group', 'aria-label': ariaLabel || '' });
    options.forEach((o) => {
      wrap.append(h('button', { type: 'button', 'aria-pressed': String(o.value === current), lang: o.lang || null, onclick: () => onChange(o.value) }, o.label));
    });
    return wrap;
  }
  function chip(label, pressed, onToggle, extra) {
    return h('button', Object.assign({ type: 'button', class: 'chip', 'aria-pressed': String(!!pressed), onclick: onToggle }, extra || {}), label);
  }

  /* ======================================================================
     Toasts & modal dialog
     ====================================================================== */
  function toast(msg, kind, ms) {
    const root = $('#toasts');
    if (!root) return;
    const el = h('div', { class: 'toast toast--' + (kind || 'info') }, icon(kind === 'ok' ? 'checkCircle' : kind === 'bad' ? 'alert' : 'info', 18), h('div', null, msg));
    root.append(el);
    setTimeout(() => { el.classList.add('is-leaving'); setTimeout(() => el.remove(), 260); }, ms || 3400);
  }

  let modalCloseHandler = null;
  function openModal(o) {
    const dlg = $('#modal');
    clear(dlg);
    const body = h('div', { class: 'modal__body' }, h('h2', { class: 'modal__title', id: 'modalTitle' }, o.title), o.body);
    const foot = h('div', { class: 'modal__foot' });
    const close = (result) => {
      if (dlg.open) dlg.close();
      const cb = modalCloseHandler; modalCloseHandler = null;
      if (cb) cb(result);
    };
    (o.actions || [{ label: t('close'), kind: 'btn--primary', value: true }]).forEach((a) => {
      const b = h('button', { type: 'button', class: 'btn ' + (a.kind || ''), onclick: () => {
        if (a.onClick && a.onClick() === false) return;
        close(a.value);
      } }, a.label);
      if (a.disabledUntil) { b.disabled = true; a.disabledUntil(b); }
      foot.append(b);
    });
    dlg.append(body, foot);
    modalCloseHandler = o.onClose || null;
    // Ignore stale close events that arrive after a new modal has already been opened.
    dlg.onclose = () => { if (dlg.open) return; const cb = modalCloseHandler; modalCloseHandler = null; if (cb) cb(undefined); };
    if (typeof dlg.showModal === 'function') {
      dlg.showModal();
      const auto = dlg.querySelector('[data-autofocus]') || foot.querySelector('.btn--primary, .btn--danger') || foot.querySelector('button');
      if (auto) auto.focus();
    } else {
      // Very old browsers: degrade to native confirm
      const ok = window.confirm(String(o.title));
      close(ok ? true : undefined);
    }
    return close;
  }
  function confirmModal(o) {
    return new Promise((resolve) => {
      let input = null;
      const parts = [h('div', { class: 'prose' }, o.message)];
      if (o.requireText) {
        input = h('input', { class: 'input', type: 'text', autocomplete: 'off', 'data-autofocus': 'true', 'aria-label': t('typeToConfirm', { word: o.requireText }) });
        parts.push(h('div', { class: 'field mt-2' }, h('label', null, t('typeToConfirm', { word: o.requireText })), input));
      }
      openModal({
        title: o.title,
        body: h('div', null, parts),
        actions: [
          { label: t('cancel'), kind: 'btn--ghost', value: false },
          {
            label: o.confirmLabel || t('confirm'), kind: o.danger ? 'btn--danger' : 'btn--primary', value: true,
            disabledUntil: input ? (b) => { input.addEventListener('input', () => { b.disabled = input.value.trim().toUpperCase() !== o.requireText; }); } : null,
          },
        ],
        onClose: (v) => resolve(v === true),
      });
    });
  }
