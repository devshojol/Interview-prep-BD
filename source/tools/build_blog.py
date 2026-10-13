"""build_blog.py — pre-render the public Interview Prep BD blog to static HTML.

    python3 tools/build_blog.py                     # preview build (noindex, no canonical/sitemap)
    SITE_URL=https://example.org python3 tools/build_blog.py   # production build
    python3 tools/build_blog.py --check             # validate content only, write nothing
    python3 tools/build_blog.py --out DIR --content DIR        # alternate output / content (tests)

Standard library only. The practice app (index.html + app.js + questions.js) does not depend on
anything written here; the blog only links into it.

Source of truth
    content/site.json         site name, description, default author, production origin
    content/blog/*.md         one article per file: frontmatter + safe Markdown subset
                              (fields: title, description, publishedAt, category, [slug, seoTitle, updatedAt,
                              tags, practice, lang, translationKey, author, draft, featured, coverImage,
                              coverAlt, canonicalUrl]; see content/blog/README.md)
    data/tech-icons.json      technology marks (shared with the app)
    ../questions.js           question ids, so links to individual questions are checked

Output (relative to the repo root unless --out is given)
    blog/index.html, blog/page/N/, blog/<slug>/, blog/bn/<slug>/, blog/category/<category>/
    blog/blog.css, blog/blog.js, blog/feed.xml            (feed only with an origin)
    sitemap.xml, robots.txt                                 (only with an origin)
    404.html                                                (always noindex)
    index.html  <!-- seo:start --> … <!-- seo:end -->       (homepage social/canonical tags)

Without a production origin the build is a *preview*: every page is noindex, canonical URLs,
JSON-LD, the feed, the sitemap and robots.txt are omitted, so a preview deploy can never
compete with production. Never derive the origin from request headers — it comes only from
SITE_URL or content/site.json.
"""
import html, json, math, os, re, shutil, sys
from datetime import date
from urllib.parse import urlsplit, quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # source/
REPO = os.path.dirname(ROOT)                                          # deployable root
PAGE_SIZE = 10
MIN_CATEGORY_POSTS = 3   # categories with fewer published posts get no page (no thin pages)
TOC_MIN_H2 = 4
WPM = 200
LANGS = {'en': {'og': None, 'label': 'English'}, 'bn': {'og': 'bn_BD', 'label': 'বাংলা'}}
APP_ROUTES = {'technologies', 'questions', 'q', 'practice', 'interview', 'flashcards', 'daily', 'review', 'sources'}
SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


class ContentError(Exception):
    pass


def esc(s):
    return html.escape(str(s), quote=True)


def plain_heading(s):
    """Heading text without Markdown markers (keeps a literal * such as COUNT(*))."""
    return re.sub(r'`|\*\*', '', s)


def slugify(s):
    s = re.sub(r'[`*_]', '', s.lower())
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s or 'section'


# --------------------------------------------------------------------------- config

def load_site(content_dir):
    site = json.load(open(os.path.join(content_dir, 'site.json'), encoding='utf-8'))
    origin = (os.environ.get('SITE_URL') or site.get('origin') or '').strip()
    if origin:
        u = urlsplit(origin)
        if u.scheme != 'https' or not u.netloc or u.query or u.fragment or '@' in u.netloc:
            raise ContentError(f'SITE_URL / site.json origin must be an https URL without query or fragment, got {origin!r}')
        origin = f'https://{u.netloc.lower()}{u.path.rstrip("/")}'
    site['origin'] = origin
    site['base_path'] = (urlsplit(origin).path if origin else '') + '/'
    return site


def load_tech():
    icons = json.load(open(os.path.join(ROOT, 'data', 'tech-icons.json'), encoding='utf-8'))
    app_core = open(os.path.join(ROOT, 'app', 'src', '00-core.js'), encoding='utf-8').read()
    names = dict(re.findall(r"\{ id: '([a-z]+)', name: '([^']+)'", app_core))
    assert set(names) == set(icons), 'tech ids in 00-core.js and tech-icons.json differ'
    return {tid: dict(icons[tid], name=names[tid]) for tid in icons}


def load_question_ids():
    path = os.path.join(REPO, 'questions.js')
    if not os.path.exists(path):
        return None
    txt = open(path, encoding='utf-8').read()
    return set(re.findall(r'"id":\s*"([a-z0-9-]+)"', txt))


# --------------------------------------------------------------------------- frontmatter

def parse_frontmatter(text, where):
    if not text.startswith('---\n'):
        raise ContentError(f'{where}: missing frontmatter (file must start with ---)')
    end = text.find('\n---\n', 4)
    if end < 0:
        raise ContentError(f'{where}: unterminated frontmatter')
    meta = {}
    for n, line in enumerate(text[4:end].split('\n'), 2):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        m = re.match(r'^([A-Za-z][A-Za-z0-9]*):\s*(.*)$', line)
        if not m:
            raise ContentError(f'{where}:{n}: cannot parse frontmatter line {line!r}')
        k, v = m.group(1), m.group(2).strip()
        if v.startswith('[') and v.endswith(']'):
            v = [x.strip().strip('"\'') for x in v[1:-1].split(',') if x.strip()]
        elif v in ('true', 'false'):
            v = v == 'true'
        elif len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
            v = v[1:-1]
        meta[k] = v
    return meta, text[end + 5:]


def valid_date(s):
    if not isinstance(s, str) or not DATE_RE.match(s):
        return False
    try:
        date.fromisoformat(s)
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------------- highlighting

KW = {
    'js': 'await async break case catch class const continue default delete do else export extends finally for from function if import in instanceof let new of return static super switch this throw try typeof var void while yield null undefined true false',
    'sql': 'select from where join left right inner outer full cross on group by having order asc desc limit offset as and or not null is in exists insert into values update set delete create table index primary key references distinct count sum avg min max case when then else end with union all coalesce between like',
    'bash': 'npm npx node cd export if then fi for do done echo curl',
}
LANG_ALIAS = {'js': 'js', 'javascript': 'js', 'ts': 'js', 'typescript': 'js', 'jsx': 'js', 'tsx': 'js', 'mjs': 'js', 'json': 'js',
              'sql': 'sql', 'postgresql': 'sql', 'sh': 'bash', 'bash': 'bash', 'shell': 'bash'}


def highlight(code, lang):
    kind = LANG_ALIAS.get(lang)
    if not kind:
        return esc(code)
    words = set(KW[kind].split())
    if kind == 'sql':
        com = r'--[^\n]*'
        strs = r"'(?:[^']|'')*'"
    elif kind == 'bash':
        com = r'#[^\n]*'
        strs = r'"(?:\\.|[^"\\])*"|\'[^\']*\''
    else:
        com = r'//[^\n]*|/\*[\s\S]*?\*/'
        strs = r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|`(?:\\.|[^`\\])*`'
    tok = re.compile(rf'(?P<com>{com})|(?P<str>{strs})|(?P<num>\b\d+(?:\.\d+)?\b)|(?P<id>[A-Za-z_$][\w$]*)(?P<call>\s*\()?')
    out, last = [], 0
    for m in tok.finditer(code):
        out.append(esc(code[last:m.start()]))
        last = m.end()
        if m.group('com'):
            out.append(f'<span class="tok-com">{esc(m.group(0))}</span>')
        elif m.group('str'):
            out.append(f'<span class="tok-str">{esc(m.group(0))}</span>')
        elif m.group('num'):
            out.append(f'<span class="tok-num">{esc(m.group(0))}</span>')
        else:
            w = m.group('id')
            key = w.lower() if kind == 'sql' else w
            if key in words:
                out.append(f'<span class="tok-kw">{esc(w)}</span>')
            elif m.group('call') and kind == 'js':
                out.append(f'<span class="tok-fn">{esc(w)}</span>')
            else:
                out.append(esc(w))
            if m.group('call'):
                out.append(esc(m.group('call')))
    out.append(esc(code[last:]))
    return ''.join(out)


# --------------------------------------------------------------------------- markdown (safe subset)

class Renderer:
    """Paragraphs, ##/###/#### headings, lists, blockquotes, pipe tables, fenced code, `code`,
    **bold**, *em* and links. Raw HTML is never passed through: everything is escaped."""

    def __init__(self, ctx, where):
        self.ctx, self.where = ctx, where
        self.headings, self.links, self.ids = [], [], set()
        self.prose_words = self.code_words = 0

    def link(self, label, target):
        c = self.ctx
        if target.startswith('post:'):
            slug = target[5:]
            self.links.append(('post', slug))
            href = c['post_href'](slug)
            return f'<a href="{esc(href)}">{label}</a>'
        if target.startswith('app:'):
            route = target[4:]
            m = re.match(r'^#/([a-z]+)(/[a-z0-9-]+)?(\?tech=([a-z]+))?$', route)
            if not m or m.group(1) not in APP_ROUTES:
                raise ContentError(f'{self.where}: app link {target!r} is not a public app route')
            if m.group(1) == 'q':
                qid = (m.group(2) or '')[1:]
                if c['question_ids'] is not None and qid not in c['question_ids']:
                    raise ContentError(f'{self.where}: app link to unknown question {qid!r}')
            if m.group(4) and m.group(4) not in c['tech']:
                raise ContentError(f'{self.where}: app link to unknown technology {m.group(4)!r}')
            return f'<a href="{esc(c["app_href"] + route)}">{label}</a>'
        u = urlsplit(target)
        if u.scheme != 'https' or not u.netloc:
            raise ContentError(f'{self.where}: link {target!r} must be https://, post:<slug> or app:#/<route>')
        return f'<a href="{esc(target)}" rel="noopener">{label}</a>'

    def inline(self, text):
        out, last = [], 0
        pat = re.compile(r'`([^`\n]+)`|\[([^\]\n]+)\]\(([^)\s]+)\)|\*\*([^*\n]+?)\*\*|(?<![\w*])\*(?![\s*])([^*\n]+?)(?<![\s*])\*(?![\w*])')
        for m in pat.finditer(text):
            out.append(esc(text[last:m.start()]))
            last = m.end()
            if m.group(1) is not None:
                out.append(f'<code>{esc(m.group(1))}</code>')
            elif m.group(2) is not None:
                out.append(self.link(self.inline(m.group(2)), m.group(3)))
            elif m.group(4) is not None:
                out.append(f'<strong>{self.inline(m.group(4))}</strong>')
            else:
                out.append(f'<em>{self.inline(m.group(5))}</em>')
        out.append(esc(text[last:]))
        return ''.join(out)

    def count(self, text):
        self.prose_words += len(re.findall(r'[\w\u0980-\u09FF]+', text))

    def heading(self, level, text):
        base = slugify(text)
        hid, n = base, 2
        while hid in self.ids:
            hid, n = f'{base}-{n}', n + 1
        self.ids.add(hid)
        self.headings.append((level, hid, text))
        self.count(text)
        return f'<h{level} id="{hid}">{self.inline(text)}</h{level}>'

    def code(self, lang, src):
        self.code_words += len(re.findall(r'\w+', src))
        label = esc(lang) if lang and lang != 'text' else 'text'
        return (f'<figure class="code"><figcaption class="code__bar"><span class="code__lang">{label}</span></figcaption>'
                f'<pre tabindex="0"><code>{highlight(src, lang)}</code></pre></figure>')

    def table(self, rows):
        def cells(r):
            return [c.strip() for c in r.strip().strip('|').split('|')]
        head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
        aligns = ['num' if c.strip().endswith(':') else '' for c in cells(rows[1])]
        th = ''.join(f'<th scope="col" class="{a}">{self.inline(c)}</th>' for c, a in zip(head, aligns))
        trs = ''.join('<tr>' + ''.join(f'<td class="{a}">{self.inline(c)}</td>' for c, a in zip(r, aligns)) + '</tr>' for r in body)
        for r in [head] + body:
            for c in r:
                self.count(c)
        return f'<div class="table-wrap" tabindex="0" role="region" aria-label="Table"><table class="table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'

    def render(self, md):
        lines = md.replace('\r\n', '\n').split('\n')
        out, para, i = [], [], 0

        def flush():
            if para:
                t = ' '.join(x.strip() for x in para)
                self.count(t)
                out.append(f'<p>{self.inline(t)}</p>')
                para.clear()

        while i < len(lines):
            line = lines[i]
            fence = re.match(r'^```([\w+-]*)\s*$', line)
            if fence:
                flush()
                buf, i = [], i + 1
                while i < len(lines) and not re.match(r'^```\s*$', lines[i]):
                    buf.append(lines[i])
                    i += 1
                if i >= len(lines):
                    raise ContentError(f'{self.where}: unterminated code fence')
                out.append(self.code(fence.group(1) or 'text', '\n'.join(buf)))
                i += 1
                continue
            hm = re.match(r'^(#{1,6})\s+(.+?)\s*#*$', line)
            if hm:
                flush()
                level = len(hm.group(1))
                if level == 1 or level > 4:
                    raise ContentError(f'{self.where}: use ## to #### in the body (the title is the only h1)')
                out.append(self.heading(level, hm.group(2)))
                i += 1
                continue
            if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|?\s*:?-{3,}', lines[i + 1]):
                flush()
                rows = []
                while i < len(lines) and lines[i].startswith('|'):
                    rows.append(lines[i])
                    i += 1
                out.append(self.table(rows))
                continue
            lm = re.match(r'^(\s*)([-*]|\d+[.)])\s+(.*)$', line)
            if lm and not lm.group(1):
                flush()
                ordered = lm.group(2)[0].isdigit()
                items = []
                while i < len(lines):
                    m2 = re.match(r'^([-*]|\d+[.)])\s+(.*)$', lines[i])
                    if m2 and (m2.group(1)[0].isdigit()) == ordered:
                        items.append([m2.group(2)])
                    elif lines[i].startswith('  ') and lines[i].strip() and items:
                        items[-1].append(lines[i].strip())
                    else:
                        break
                    i += 1
                lis = []
                for it in items:
                    t = ' '.join(it)
                    self.count(t)
                    lis.append(f'<li>{self.inline(t)}</li>')
                tag = 'ol' if ordered else 'ul'
                out.append(f'<{tag}>{"".join(lis)}</{tag}>')
                continue
            if line.startswith('> '):
                flush()
                buf = []
                while i < len(lines) and lines[i].startswith('>'):
                    buf.append(lines[i][1:].strip())
                    i += 1
                t = ' '.join(buf)
                self.count(t)
                out.append(f'<blockquote><p>{self.inline(t)}</p></blockquote>')
                continue
            if not line.strip():
                flush()
            else:
                if re.match(r'^\s*<[a-zA-Z/!]', line):
                    raise ContentError(f'{self.where}: raw HTML is not allowed in articles')
                para.append(line)
            i += 1
        flush()
        return '\n'.join(out)


# --------------------------------------------------------------------------- content loading

def load_posts(content_dir, site, tech, question_ids):
    blog_dir = os.path.join(content_dir, 'blog')
    raw, errors = [], []
    for name in sorted(os.listdir(blog_dir)):
        if not name.endswith('.md') or name.upper() == 'README.MD':  # README.md is the authoring guide
            continue
        where = os.path.join('content', 'blog', name)
        try:
            meta, body = parse_frontmatter(open(os.path.join(blog_dir, name), encoding='utf-8').read(), where)
            meta.setdefault('slug', name[:-3])
            meta.setdefault('lang', 'en')
            meta.setdefault('author', site['author'])
            meta.setdefault('tags', [])
            meta.setdefault('practice', [])
            meta.setdefault('draft', False)
            for f in ('title', 'description', 'publishedAt', 'category'):
                if not isinstance(meta.get(f), str) or not meta[f].strip():
                    raise ContentError(f'{where}: missing or empty "{f}"')
            if not SLUG_RE.match(meta['slug']):
                raise ContentError(f'{where}: slug {meta["slug"]!r} must be lowercase words joined by hyphens')
            if meta['lang'] not in LANGS:
                raise ContentError(f'{where}: lang must be one of {sorted(LANGS)}')
            if not valid_date(meta['publishedAt']):
                raise ContentError(f'{where}: publishedAt must be a real YYYY-MM-DD date')
            if meta.get('updatedAt') is not None:
                if not valid_date(meta['updatedAt']) or meta['updatedAt'] < meta['publishedAt']:
                    raise ContentError(f'{where}: updatedAt must be a YYYY-MM-DD date on or after publishedAt')
            for f in ('tags', 'practice'):
                if not isinstance(meta[f], list):
                    raise ContentError(f'{where}: {f} must be a [list]')
            bad = [t for t in meta['practice'] if t not in tech]
            if bad:
                raise ContentError(f'{where}: unknown technology in practice: {bad}')
            if not isinstance(meta['draft'], bool):
                raise ContentError(f'{where}: draft must be true or false')
            if len(meta['description']) > 200:
                raise ContentError(f'{where}: description is {len(meta["description"])} characters; keep it a concise summary')
            if meta.get('canonicalUrl'):
                cu = urlsplit(meta['canonicalUrl'])
                if cu.scheme != 'https' or (site['origin'] and cu.netloc != urlsplit(site['origin']).netloc):
                    raise ContentError(f'{where}: canonicalUrl must be an https URL on the production origin')
            if meta.get('coverImage'):
                img = os.path.join(REPO, meta['coverImage'].lstrip('/'))
                if not os.path.isfile(img) or not meta.get('coverAlt'):
                    raise ContentError(f'{where}: coverImage must exist and have coverAlt')
            meta['_body'], meta['_file'] = body, where
            raw.append(meta)
        except ContentError as e:
            errors.append(str(e))
    seen = {}
    for p in raw:
        key = (p['lang'], p['slug'])
        if key in seen:
            errors.append(f'{p["_file"]}: duplicate slug {p["slug"]!r} (also in {seen[key]})')
        seen[key] = p['_file']
    return raw, errors


def post_path(p):
    return f'blog/{p["slug"]}/' if p['lang'] == 'en' else f'blog/{p["lang"]}/{p["slug"]}/'


def rel(from_dir, to_path):
    """Relative href from an output directory (e.g. 'blog/x/') to a site path (e.g. 'blog/')."""
    depth = len([x for x in from_dir.split('/') if x])
    return '../' * depth + to_path if (depth or to_path) else './'


def fmt_date(s):
    d = date.fromisoformat(s)
    return f'{d.day} {d.strftime("%B %Y")}'


# --------------------------------------------------------------------------- page chrome

def jsonld(obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    return s.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')


def mark_svg(size=28):
    return (f'<svg viewBox="0 0 32 32" width="{size}" height="{size}" aria-hidden="true" focusable="false">'
            '<rect width="32" height="32" rx="8" class="mark-tile"/><g transform="translate(0 -.6)" class="mark-ink">'
            '<path d="M7.6 11.4a4.6 4.6 0 1 1 6.8 4c-1.4.8-2.2 1.6-2.2 3v.6" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            '<circle cx="12.2" cy="24.6" r="1.85"/><rect x="18" y="23.2" width="7.4" height="2.9" rx=".7"/></g></svg>')


def tech_svg(t, size=18):
    vb = [float(x) for x in t['viewBox'].split()]
    w = round(size * min(vb[2] / vb[3], 1.8), 1)
    style = ''.join(f'--mark-{k[0]}:{t[k]};' for k in ('dark', 'light') if t.get(k))
    paint = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"' if t.get('stroke') else 'fill="currentColor"'
    return (f'<svg class="tech-mark" viewBox="{t["viewBox"]}" width="{w}" height="{size}" aria-hidden="true" focusable="false"'
            f'{f" style={chr(34)}{style}{chr(34)}" if style else ""}><path d="{t["d"]}" {paint}/></svg>')


def page(site, *, out_dir, title, description, body, lang='en', canonical_path=None, og_type='website',
         og_image=None, og_image_alt=None, ld=None, alternates=None, noindex=False, prev_next=None, extra_head=''):
    origin = site['origin']
    up = rel(out_dir, '')
    robots = 'noindex, follow' if (noindex or not origin) else 'index, follow, max-image-preview:large'
    head = [
        f'<meta charset="utf-8">',
        f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f'<title>{esc(title)}</title>',
        f'<meta name="description" content="{esc(description)}">',
        f'<meta name="robots" content="{robots}">',
        '<meta name="color-scheme" content="dark light">',
        '<meta name="theme-color" content="#0B1020">',
        f'<link rel="icon" href="{up}assets/brand/favicon.svg" type="image/svg+xml">',
        f'<link rel="apple-touch-icon" href="{up}assets/brand/apple-touch-icon.png">',
    ]
    if origin and canonical_path is not None and not noindex:
        url = origin + '/' + canonical_path
        img = origin + '/' + (og_image or 'assets/brand/og-default.png')
        head += [
            f'<link rel="canonical" href="{esc(url)}">',
            f'<meta property="og:site_name" content="{esc(site["name"])}">',
            f'<meta property="og:type" content="{og_type}">',
            f'<meta property="og:title" content="{esc(title)}">',
            f'<meta property="og:description" content="{esc(description)}">',
            f'<meta property="og:url" content="{esc(url)}">',
            f'<meta property="og:image" content="{esc(img)}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            f'<meta property="og:image:alt" content="{esc(og_image_alt or site["name"])}">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
        if LANGS[lang]['og']:
            head.append(f'<meta property="og:locale" content="{LANGS[lang]["og"]}">')
        head.append(f'<link rel="alternate" type="application/atom+xml" title="{esc(site["name"])} blog" href="{esc(origin)}/blog/feed.xml">')
        for hl, path in (alternates or []):
            head.append(f'<link rel="alternate" hreflang="{hl}" href="{esc(origin + "/" + path)}">')
        for relname, path in (prev_next or []):
            head.append(f'<link rel="{relname}" href="{esc(origin + "/" + path)}">')
        for obj in (ld or []):
            head.append(f'<script type="application/ld+json">{jsonld(obj)}</script>')
    fonts = 'family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap'
    if lang == 'bn':
        fonts = 'family=Hind+Siliguri:wght@400;600&' + fonts
    head += [
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}">',
        f'<link rel="stylesheet" href="{up}styles.css">',
        f'<link rel="stylesheet" href="{up}blog/blog.css">',
        # Same theme preference as the app (localStorage key ipbd:state); defaults to dark like the app.
        "<script>try{var t=JSON.parse(localStorage.getItem('ipbd:state')).preferences.theme;if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>",
        f'<script src="{up}blog/blog.js" defer></script>',
        extra_head,
    ]
    header = (f'<header class="site-head"><div class="site-head__in">'
              f'<a class="site-brand" href="{up}">{mark_svg()}<span>{esc(site["name"])}</span></a>'
              f'<nav aria-label="Site"><ul class="site-nav">'
              f'<li><a href="{up}blog/"{" aria-current=" + chr(34) + "page" + chr(34) if out_dir == "blog/" else ""}>Blog</a></li>'
              f'<li><a href="{up}#/technologies">Technologies</a></li>'
              f'<li><a class="site-nav__cta" href="{up}#/practice">Start practising</a></li>'
              f'</ul></nav></div></header>')
    footer = (f'<footer class="site-foot"><div class="site-foot__in">'
              f'<a class="site-brand" href="{up}">{mark_svg(24)}<span>{esc(site["name"])}</span></a>'
              f'<p>{esc(site["tagline"])}</p>'
              f'<ul class="site-foot__links"><li><a href="{up}blog/">Blog</a></li><li><a href="{up}#/questions">All questions</a></li>'
              f'<li><a href="{up}#/sources">Versions &amp; sources</a></li>'
              + (f'<li><a href="{up}blog/feed.xml">Atom feed</a></li>' if origin else '') +
              '</ul></div></footer>')
    return (f'<!doctype html>\n<html lang="{lang}" data-theme="dark">\n<head>\n' + '\n'.join(h for h in head if h) +
            f'\n</head>\n<body class="blog">\n<a class="skip-link" href="#main">Skip to main content</a>\n{header}\n'
            f'<main id="main" tabindex="-1">\n{body}\n</main>\n{footer}\n</body>\n</html>\n')


# --------------------------------------------------------------------------- views

def post_meta_line(p):
    parts = [f'<time datetime="{p["publishedAt"]}">{fmt_date(p["publishedAt"])}</time>']
    if p.get('updatedAt') and p['updatedAt'] != p['publishedAt']:
        parts.append(f'Updated <time datetime="{p["updatedAt"]}">{fmt_date(p["updatedAt"])}</time>')
    parts.append(f'{p["_minutes"]} min read')
    return ' · '.join(parts)


def category_ref(p, cat_pages, out_dir):
    c = p['category']
    if c in cat_pages:
        return f'<a class="post-cat" href="{rel(out_dir, cat_pages[c])}">{esc(c)}</a>'
    return f'<span class="post-cat">{esc(c)}</span>'


def post_item(p, cat_pages, out_dir, heading='h2'):
    href = rel(out_dir, p['_path'])
    lang = f' lang="{p["lang"]}"' if p['lang'] != 'en' else ''
    return (f'<li class="post-item"{lang}><p class="post-meta">{category_ref(p, cat_pages, out_dir)} · {post_meta_line(p)}</p>'
            f'<{heading} class="post-item__title"><a href="{href}">{esc(p["title"])}</a></{heading}>'
            f'<p class="post-item__desc">{esc(p["description"])}</p></li>')


def practice_list(site, tech, out_dir, ids=None):
    up = rel(out_dir, '')
    items = ''.join(f'<li><a href="{up}#/questions?tech={tid}">{tech_svg(t)}<span>{esc(t["name"])}</span></a></li>'
                    for tid, t in tech.items() if ids is None or tid in ids)
    return f'<ul class="tech-links">{items}</ul>'


def org(site):
    o = {'@type': 'Organization', 'name': site['name'], 'url': site['origin'] + '/'}
    o['logo'] = {'@type': 'ImageObject', 'url': site['origin'] + '/assets/brand/apple-touch-icon.png', 'width': 180, 'height': 180}
    return o


def build(content_dir, out_root, check_only=False):
    site = load_site(content_dir)
    tech = load_tech()
    qids = load_question_ids()
    posts, errors = load_posts(content_dir, site, tech, qids)
    published = [p for p in posts if not p['draft']]
    slugs = {(p['lang'], p['slug']) for p in published}
    by_slug = {}
    for p in published:
        p['_path'] = post_path(p)
        by_slug.setdefault(p['slug'], p)
    ctx_base = {'tech': tech, 'question_ids': qids}
    # Render bodies (validates links against *published* posts only, so drafts can't be linked)
    for p in published:
        out_dir = p['_path']
        ctx = dict(ctx_base, app_href=rel(out_dir, ''),
                   post_href=lambda s, d=out_dir: rel(d, by_slug[s]['_path']) if s in by_slug else None)
        r = Renderer(ctx, p['_file'])
        try:
            p['_html'] = r.render(p['_body'])
            for kind, s in r.links:
                if kind == 'post' and s not in by_slug:
                    raise ContentError(f'{p["_file"]}: link to unknown or unpublished post {s!r}')
            if sum(1 for lv, _, _ in r.headings if lv == 2) == 0:
                raise ContentError(f'{p["_file"]}: an article needs at least one ## section')
        except ContentError as e:
            errors.append(str(e))
            continue
        p['_headings'] = r.headings
        p['_words'] = r.prose_words + r.code_words
        p['_minutes'] = max(1, math.ceil((r.prose_words + r.code_words / 2) / WPM))
    for p in published:
        tk = p.get('translationKey')
        p['_alts'] = [q for q in published if tk and q.get('translationKey') == tk]
    if errors:
        raise ContentError('Content errors:\n  ' + '\n  '.join(errors))
    published.sort(key=lambda p: (p['publishedAt'], p['slug']), reverse=True)
    print(f'{len(published)} published, {len(posts) - len(published)} draft(s); origin: {site["origin"] or "(none: preview build, noindex)"}')
    if check_only:
        return

    origin = site['origin']
    written = []

    def write(path, text):
        full = os.path.join(out_root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(text)
        written.append(path)

    # Clean previous generated blog pages (keep blog.css / blog.js, which live in source/blog-assets)
    blog_out = os.path.join(out_root, 'blog')
    if os.path.isdir(blog_out):
        shutil.rmtree(blog_out)
    for fname in ('blog.css', 'blog.js'):
        src = os.path.join(ROOT, 'blog-assets', fname)
        os.makedirs(blog_out, exist_ok=True)
        shutil.copy(src, os.path.join(blog_out, fname))
    cats = {}
    for p in published:
        cats.setdefault(p['category'], []).append(p)
    cat_pages = {c: f'blog/category/{slugify(c)}/' for c, ps in cats.items() if len(ps) >= MIN_CATEGORY_POSTS}
    publisher = org(site) if origin else None

    # ---- articles
    for p in published:
        out_dir = p['_path']
        up = rel(out_dir, '')
        toc = ''
        h2s = [h for h in p['_headings'] if h[0] == 2]
        if len(h2s) >= TOC_MIN_H2:
            items = ''.join(f'<li><a href="#{hid}">{esc(plain_heading(t))}</a></li>' for lv, hid, t in p['_headings'] if lv == 2)
            toc = f'<nav class="toc" aria-labelledby="toc-h"><h2 id="toc-h" class="toc__title">On this page</h2><ol>{items}</ol></nav>'
        practice = ''
        if p['practice']:
            practice = (f'<aside class="practice" aria-labelledby="practice-h"><h2 id="practice-h">Practise this topic</h2>'
                        f'<p>Answer real interview questions in English and Bangla, then check yourself against the reference answers. Progress stays in your browser.</p>'
                        f'{practice_list(site, tech, out_dir, p["practice"])}</aside>')
        def score(q):
            return 3 * (q['category'] == p['category']) + len(set(q['tags']) & set(p['tags'])) + len(set(q['practice']) & set(p['practice']))
        related = sorted((q for q in published if q is not p and q['lang'] == p['lang']), key=lambda q: (score(q), q['publishedAt']), reverse=True)
        related = [q for q in related if score(q) > 0][:3] or related[:2]
        rel_html = ''
        if related:
            rel_html = ('<section class="related" aria-labelledby="related-h"><h2 id="related-h">Related articles</h2><ul class="post-list">'
                        + ''.join(post_item(q, cat_pages, out_dir, 'h3') for q in related) + '</ul></section>')
        alts = [q for q in p['_alts'] if q is not p]
        alt_link = ''.join(f'<p class="post-alt"><a href="{rel(out_dir, q["_path"])}" hreflang="{q["lang"]}" lang="{q["lang"]}">'
                           f'{"এই লেখাটি বাংলায় পড়ুন" if q["lang"] == "bn" else "Read this article in English"}</a></p>' for q in alts)
        tags = ''.join(f'<li>{esc(t)}</li>' for t in p['tags'])
        crumbs = (f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{up}">Home</a></li><li><a href="{rel(out_dir, "blog/")}">Blog</a></li>'
                  f'<li><span aria-current="page">{esc(p["title"])}</span></li></ol></nav>')
        body = (f'<div class="article-wrap">{crumbs}<article class="post" lang="{p["lang"]}">'
                f'<header class="post-head"><p class="post-meta">{category_ref(p, cat_pages, out_dir)}</p>'
                f'<h1>{esc(p["title"])}</h1><p class="post-lead">{esc(p["description"])}</p>'
                f'<p class="post-meta">By {esc(p["author"])} · {post_meta_line(p)}</p>{alt_link}</header>'
                f'{toc}<div class="prose post-body">{p["_html"]}</div>'
                + (f'<footer class="post-foot"><h2 class="sr-only">Tags</h2><ul class="post-tags">{tags}</ul></footer>' if tags else '')
                + f'</article>{practice}{rel_html}<p class="back"><a href="{rel(out_dir, "blog/")}">← All articles</a></p></div>')
        ld = None
        if origin:
            url = f'{origin}/{out_dir}'
            img = origin + '/' + (p.get('coverImage', '').lstrip('/') or (f'assets/og/{p["slug"]}.png' if os.path.isfile(os.path.join(REPO, 'assets', 'og', p['slug'] + '.png')) else 'assets/brand/og-default.png'))
            ld = [{'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['description'],
                   'image': [img], 'datePublished': p['publishedAt'], 'dateModified': p.get('updatedAt') or p['publishedAt'],
                   'inLanguage': p['lang'], 'articleSection': p['category'], 'keywords': ', '.join(p['tags']), 'wordCount': p['_words'],
                   'author': {'@type': 'Organization', 'name': p['author'], 'url': origin + '/'}, 'publisher': publisher,
                   'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'url': url},
                  {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                      {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': origin + '/'},
                      {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': origin + '/blog/'},
                      {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': url}]}]
        og_img = p.get('coverImage', '').lstrip('/') or (f'assets/og/{p["slug"]}.png' if os.path.isfile(os.path.join(REPO, 'assets', 'og', p['slug'] + '.png')) else None)
        alternates = None
        if len(p['_alts']) > 1:  # genuine translations only; each version is canonical to itself
            alternates = [(q['lang'], q['_path']) for q in p['_alts']]
            en = next((q for q in p['_alts'] if q['lang'] == 'en'), None)
            if en:
                alternates.append(('x-default', en['_path']))
        extra = (f'<meta property="article:published_time" content="{p["publishedAt"]}">'
                 + (f'<meta property="article:modified_time" content="{p["updatedAt"]}">' if p.get('updatedAt') else '')
                 + f'<meta property="article:section" content="{esc(p["category"])}">'
                 + ''.join(f'<meta property="article:tag" content="{esc(t)}">' for t in p['tags'])) if origin else ''
        canon = p.get('canonicalUrl')
        canonical_path = urlsplit(canon).path.lstrip('/') if canon else out_dir
        head_title = p.get('seoTitle') or p['title']
        if len(head_title) <= 60:  # brand suffix only while the result title stays readable
            head_title += f' | {site["name"]}'
        write(out_dir + 'index.html', page(site, out_dir=out_dir, title=head_title, description=p['description'], body=body,
                                          lang=p['lang'], canonical_path=canonical_path, og_type='article', og_image=og_img,
                                          og_image_alt=p['title'], ld=ld, alternates=alternates, extra_head=extra))

    # ---- index + pagination
    en_posts = published
    pages = max(1, math.ceil(len(en_posts) / PAGE_SIZE))
    featured = next((p for p in en_posts if p.get('featured')), None)
    for n in range(1, pages + 1):
        out_dir = 'blog/' if n == 1 else f'blog/page/{n}/'
        chunk = en_posts[(n - 1) * PAGE_SIZE: n * PAGE_SIZE]
        if n == 1 and featured:
            chunk = [p for p in chunk if p is not featured]
        intro = (f'<header class="blog-head"><h1>{esc(site["blogTitle"])}</h1><p class="post-lead">{esc(site["blogIntro"])}</p></header>')
        feat = ''
        if n == 1 and featured:
            feat = (f'<section class="featured" aria-labelledby="featured-h"><h2 id="featured-h" class="label">Start here</h2>'
                    f'<p class="post-meta">{category_ref(featured, cat_pages, out_dir)} · {post_meta_line(featured)}</p>'
                    f'<h3 class="featured__title"><a href="{rel(out_dir, featured["_path"])}">{esc(featured["title"])}</a></h3>'
                    f'<p class="post-item__desc">{esc(featured["description"])}</p></section>')
        listing = (f'<section aria-labelledby="latest-h"><h2 id="latest-h" class="label">{"Latest articles" if n == 1 else f"Articles, page {n}"}</h2>'
                   f'<ul class="post-list">' + ''.join(post_item(p, cat_pages, out_dir) for p in chunk) + '</ul></section>')
        pager = ''
        if pages > 1:
            prev_dir = None if n == 1 else ('blog/' if n == 2 else f'blog/page/{n - 1}/')
            next_dir = None if n == pages else f'blog/page/{n + 1}/'
            pager = ('<nav class="pager" aria-label="Pagination">'
                     + (f'<a href="{rel(out_dir, prev_dir)}" rel="prev">← Newer</a>' if prev_dir else '<span></span>')
                     + f'<span>Page {n} of {pages}</span>'
                     + (f'<a href="{rel(out_dir, next_dir)}" rel="next">Older →</a>' if next_dir else '<span></span>') + '</nav>')
        cat_nav = ''
        if cat_pages:
            cat_nav = ('<nav class="cat-nav" aria-labelledby="cat-h"><h2 id="cat-h" class="label">Topics</h2><ul>'
                       + ''.join(f'<li><a href="{rel(out_dir, path)}">{esc(c)}</a> <span>{len(cats[c])}</span></li>' for c, path in sorted(cat_pages.items())) + '</ul></nav>')
        aside = (f'<aside class="blog-aside">{cat_nav}<section aria-labelledby="tech-h"><h2 id="tech-h" class="label">Practise by technology</h2>'
                 f'{practice_list(site, tech, out_dir)}</section></aside>')
        body = f'<div class="blog-wrap">{intro}<div class="blog-grid"><div>{feat}{listing}{pager}</div>{aside}</div></div>'
        ld = None
        if origin:
            ld = [{'@context': 'https://schema.org', '@type': 'Blog', 'name': site['blogTitle'], 'description': site['blogIntro'],
                   'url': f'{origin}/{out_dir}', 'inLanguage': 'en', 'publisher': publisher,
                   'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': f'{origin}/{p["_path"]}', 'datePublished': p['publishedAt']}
                                for p in en_posts[(n - 1) * PAGE_SIZE: n * PAGE_SIZE]]}]
        pn = []
        if pages > 1:
            if n > 1:
                pn.append(('prev', 'blog/' if n == 2 else f'blog/page/{n - 1}/'))
            if n < pages:
                pn.append(('next', f'blog/page/{n + 1}/'))
        title = site['blogTitle'] + (f' (page {n})' if n > 1 else '') + f' | {site["name"]}'
        write(out_dir + 'index.html', page(site, out_dir=out_dir, title=title, description=site['blogDescription'], body=body,
                                          canonical_path=out_dir, ld=ld, prev_next=pn))

    # ---- category pages (only substantial ones)
    for c, path in cat_pages.items():
        ps = cats[c]
        body = (f'<div class="blog-wrap"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{rel(path, "")}">Home</a></li>'
                f'<li><a href="{rel(path, "blog/")}">Blog</a></li><li><span aria-current="page">{esc(c)}</span></li></ol></nav>'
                f'<header class="blog-head"><h1>{esc(c)}</h1><p class="post-lead">{len(ps)} articles about {esc(c)}.</p></header>'
                f'<ul class="post-list">' + ''.join(post_item(p, cat_pages, path) for p in ps) + '</ul></div>')
        write(path + 'index.html', page(site, out_dir=path, title=f'{c} articles | {site["name"]}',
                                       description=f'{site["name"]} articles about {c}: ' + '; '.join(p['title'] for p in ps[:3])[:150],
                                       body=body, canonical_path=path))

    # ---- 404 (served by static hosts for unknown paths; assets via absolute paths)
    base = site['base_path']
    nf = page(site, out_dir='', title=f'Page not found | {site["name"]}', description='This page does not exist.', noindex=True,
              body=(f'<div class="article-wrap"><h1>Page not found</h1><p class="post-lead">There is no page at this address. '
                    f'It may have moved, or the link may be mistyped.</p><ul class="post-tags-inline"><li><a href="{base}blog/">Browse the blog</a></li>'
                    f'<li><a href="{base}">Open the practice app</a></li></ul></div>'))
    nf = nf.replace('href="./assets/', f'href="{base}assets/').replace('href="./styles.css"', f'href="{base}styles.css"') \
           .replace('href="./blog/', f'href="{base}blog/').replace('src="./blog/', f'src="{base}blog/').replace('href="./"', f'href="{base}"') \
           .replace('href="./#/', f'href="{base}#/')
    write('404.html', nf)

    # ---- sitemap, robots, feed (production only)
    for f in ('sitemap.xml', 'robots.txt'):
        if not origin and os.path.exists(os.path.join(out_root, f)):
            os.remove(os.path.join(out_root, f))
    if origin:
        newest = max(p.get('updatedAt') or p['publishedAt'] for p in published) if published else None
        urls = [(f'{origin}/', None), (f'{origin}/blog/', newest)]
        urls += [(f'{origin}/blog/page/{n}/', None) for n in range(2, pages + 1)]
        urls += [(f'{origin}/{p["_path"]}', p.get('updatedAt') or p['publishedAt']) for p in published if not p.get('canonicalUrl')]
        urls += [(f'{origin}/{path}', max(p.get('updatedAt') or p['publishedAt'] for p in cats[c])) for c, path in cat_pages.items()]
        xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u, lm in urls:
            xml.append(f'  <url><loc>{esc(u)}</loc>' + (f'<lastmod>{lm}</lastmod>' if lm else '') + '</url>')
        xml.append('</urlset>')
        write('sitemap.xml', '\n'.join(xml) + '\n')
        write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n')
        if urlsplit(origin).path:
            print('warning: origin has a path; robots.txt only takes effect at the host root, so submit the sitemap in Search Console instead')
        feed = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom">',
                f'  <title>{esc(site["blogTitle"])} | {esc(site["name"])}</title>', f'  <link href="{origin}/blog/"/>',
                f'  <link rel="self" href="{origin}/blog/feed.xml"/>', f'  <id>{origin}/blog/</id>',
                f'  <updated>{newest}T00:00:00Z</updated>', f'  <author><name>{esc(site["author"])}</name></author>']
        for p in published[:20]:
            feed += ['  <entry>', f'    <title>{esc(p["title"])}</title>', f'    <link href="{origin}/{p["_path"]}"/>',
                     f'    <id>{origin}/{p["_path"]}</id>', f'    <published>{p["publishedAt"]}T00:00:00Z</published>',
                     f'    <updated>{p.get("updatedAt") or p["publishedAt"]}T00:00:00Z</updated>',
                     f'    <summary>{esc(p["description"])}</summary>', '  </entry>']
        feed.append('</feed>')
        write('blog/feed.xml', '\n'.join(feed) + '\n')

    # ---- homepage social / canonical tags (between markers in index.html)
    idx_path = os.path.join(out_root, 'index.html')
    if os.path.exists(idx_path):
        idx = open(idx_path, encoding='utf-8').read()
        if '<!-- seo:start -->' in idx:
            tags = [f'<meta property="og:site_name" content="{esc(site["name"])}">', '<meta property="og:type" content="website">',
                    f'<meta property="og:title" content="{esc(site["homeTitle"])}">', f'<meta property="og:description" content="{esc(site["description"])}">']
            if origin:
                tags += [f'<link rel="canonical" href="{origin}/">', f'<meta property="og:url" content="{origin}/">',
                         f'<meta property="og:image" content="{origin}/assets/brand/og-default.png">',
                         '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
                         f'<meta property="og:image:alt" content="{esc(site["name"])}">', '<meta name="twitter:card" content="summary_large_image">',
                         f'<script type="application/ld+json">{jsonld([{"@context": "https://schema.org", "@type": "WebSite", "name": site["name"], "url": origin + "/", "inLanguage": ["en", "bn"], "publisher": org(site)}])}</script>']
            block = '<!-- seo:start -->\n  ' + '\n  '.join(tags) + '\n  <!-- seo:end -->'
            idx = re.sub(r'<!-- seo:start -->.*?<!-- seo:end -->', lambda m: block, idx, flags=re.S)
            with open(idx_path, 'w', encoding='utf-8') as f:
                f.write(idx)
            written.append('index.html (seo block)')
    print(f'wrote {len(written)} files' + ('' if origin else ' (preview: noindex, no canonical/sitemap/robots/feed)'))


if __name__ == '__main__':
    args = sys.argv[1:]
    out_root = REPO
    content_dir = os.path.join(ROOT, 'content')
    if '--out' in args:
        out_root = os.path.abspath(args[args.index('--out') + 1])
    if '--content' in args:
        content_dir = os.path.abspath(args[args.index('--content') + 1])
    try:
        build(content_dir, out_root, check_only='--check' in args)
    except ContentError as e:
        sys.exit(str(e))
