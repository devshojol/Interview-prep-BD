"""build_tech_icons.py — vendor technology brand marks into the app.

Usage:
    python3 tools/build_tech_icons.py <simple-icons package dir> <devicon package dir>

Get the packages without installing them (no install scripts run):
    npm pack simple-icons@16.33.0 && tar -xzf simple-icons-16.33.0.tgz   # -> package/
    npm pack devicon@2.17.0 && tar -xzf devicon-2.17.0.tgz               # -> package/

Writes:
    data/tech-icons.json        single source of truth (also read by tools/build_blog.py)
    app/src/05-tech-icons.js    TECH_ICONS for the app bundle (run tools/build_app.sh afterwards)

Sources and licences:
    Simple Icons (CC0-1.0) for 16 marks. Devicon (MIT) for the AWS wordmark, which Simple Icons
    no longer ships. SQL and vector databases have no official logo, so they get plain generic
    symbols drawn here, not invented brand marks. All trademarks belong to their owners and are
    used only to identify the technology.

Colour: each mark keeps its brand hue. When the brand colour fails 3:1 non-text contrast against
the theme surface, it is mixed toward white (dark theme) or black (light theme) until it passes;
near-neutral brands (Next.js, Express) fall back to the theme text colour.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SIMPLE = {  # app tech id -> simple-icons slug
    'html': 'html5', 'css': 'css', 'javascript': 'javascript', 'react': 'react',
    'nextjs': 'nextdotjs', 'nodejs': 'nodedotjs', 'express': 'express', 'nestjs': 'nestjs',
    'mongodb': 'mongodb', 'mongoose': 'mongoose', 'postgresql': 'postgresql', 'drizzle': 'drizzle',
    'redis': 'redis', 'docker': 'docker', 'nginx': 'nginx',
}
GENERIC = {
    # Database cylinder: SQL is a language with no official mark.
    'sql': {'viewBox': '0 0 24 24', 'stroke': True, 'title': 'SQL (generic database symbol)',
            'd': 'M12 8c4.97 0 9-1.34 9-3s-4.03-3-9-3-9 1.34-9 3 4.03 3 9 3z M21 12c0 1.66-4 3-9 3s-9-1.34-9-3 M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5'},
    # Three vectors from an origin: no single vector database owns a logo.
    'vectordb': {'viewBox': '0 0 24 24', 'stroke': True, 'title': 'Vector databases (generic vector symbol)',
                 'd': 'M4 20 19 5 M19 5h-5 M19 5v5 M4 20h16 M20 20l-3-3 M20 20l-3 3 M4 20 9 7 M9 7l-3.4 1.2 M9 7l1 3.4'},
}
SURFACE = {'dark': (0x15, 0x1E, 0x33), 'light': (0xFF, 0xFF, 0xFF)}


def lum(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def themed(hexc, theme):
    """Brand colour adjusted to >= 3:1 on the theme surface, or None for the text colour."""
    rgb = hex2rgb(hexc)
    if max(rgb) - min(rgb) < 24:  # neutral brand (black/white marks) -> follow the theme text colour
        return None
    target = (255, 255, 255) if theme == 'dark' else (0, 0, 0)
    for step in range(0, 101, 5):
        t = step / 100
        mix = tuple(round(c + (tc - c) * t) for c, tc in zip(rgb, target))
        if contrast(mix, SURFACE[theme]) >= 3:
            return '#%02X%02X%02X' % mix
    return None


def main(si_dir, dv_dir):
    meta = json.load(open(os.path.join(si_dir, 'data', 'simple-icons.json'), encoding='utf-8'))
    meta = meta if isinstance(meta, list) else meta['icons']
    by_slug = {}
    for m in meta:
        slug = m.get('slug') or re.sub(r'[^a-z0-9]', '', m['title'].lower())
        by_slug[slug] = m
    out = {}
    for tid, slug in SIMPLE.items():
        svg = open(os.path.join(si_dir, 'icons', slug + '.svg'), encoding='utf-8').read()
        d = re.search(r' d="([^"]+)"', svg).group(1)
        m = by_slug[slug]
        out[tid] = {'title': m['title'], 'viewBox': '0 0 24 24', 'd': d, 'brand': '#' + m['hex'],
                    'source': 'Simple Icons 16.33.0 (CC0-1.0)'}
    aws = open(os.path.join(dv_dir, 'icons', 'amazonwebservices', 'amazonwebservices-plain-wordmark.svg'), encoding='utf-8').read()
    paths = re.findall(r' d="([^"]+)"', aws)
    assert len(paths) == 1, 'AWS wordmark layout changed; re-check the bbox'
    # viewBox cropped to the measured bounding box of the wordmark (0.70 26.15 126.60 75.70)
    out['aws'] = {'title': 'Amazon Web Services', 'viewBox': '0.7 26.15 126.6 75.7', 'd': paths[0], 'brand': '#FF9900',
                  'source': 'Devicon 2.17.0 (MIT)'}
    for tid, g in GENERIC.items():
        out[tid] = dict(g, brand=None, source='Interview Prep BD (generic symbol)')
    for tid, ic in out.items():
        ic['dark'] = themed(ic['brand'], 'dark') if ic['brand'] else None
        ic['light'] = themed(ic['brand'], 'light') if ic['brand'] else None
    order = ['html', 'css', 'javascript', 'react', 'nextjs', 'nodejs', 'express', 'nestjs', 'mongodb', 'mongoose',
             'postgresql', 'sql', 'drizzle', 'redis', 'vectordb', 'docker', 'nginx', 'aws']
    assert sorted(order) == sorted(out), 'tech id mismatch'
    data = {tid: out[tid] for tid in order}
    with open(os.path.join(ROOT, 'data', 'tech-icons.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')
    js = ('\n  /* Technology marks — generated by tools/build_tech_icons.py from data/tech-icons.json.\n'
          '     Simple Icons (CC0-1.0); AWS wordmark from Devicon (MIT); SQL and vector databases use generic\n'
          '     symbols because neither has an official logo. Trademarks belong to their owners. */\n'
          '  const TECH_ICONS = ' + json.dumps({k: {f: v[f] for f in ('viewBox', 'd', 'dark', 'light') if v.get(f) is not None}
                                                | ({'stroke': True} if v.get('stroke') else {}) for k, v in data.items()},
                                               separators=(',', ':')) + ';\n')
    assert '</script' not in js.lower()
    with open(os.path.join(ROOT, 'app', 'src', '05-tech-icons.js'), 'w', encoding='utf-8') as f:
        f.write(js)
    for k, v in data.items():
        print(f'{k:11} {v["source"]:34} brand={v["brand"]} dark={v["dark"]} light={v["light"]}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
