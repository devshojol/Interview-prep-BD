"""build_og_images.py — render social-sharing PNGs with headless Chrome.

    python3 tools/build_og_images.py            # default image, apple-touch-icon, one image per published article

Writes (repo root):
    assets/brand/og-default.png      1200x630, used by the homepage and blog index
    assets/brand/apple-touch-icon.png 180x180
    assets/og/<slug>.png             1200x630 per published article (title on the brand background)

Needs Google Chrome or Chromium. Optional: tools/build_blog.py falls back to og-default.png for any
article without its own image. Run this before build_blog.py when titles change.
"""
import html, os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_blog as bb  # noqa: E402  (reuses the content loader and validation)

CHROME_CANDIDATES = [
    os.environ.get('CHROME_BIN', ''),
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    shutil.which('google-chrome') or '', shutil.which('chromium') or '', shutil.which('chromium-browser') or '',
]
MARK = ('<svg viewBox="0 0 32 32" width="{s}" height="{s}"><rect width="32" height="32" rx="8" fill="#8B7CFF"/>'
        '<g transform="translate(0 -.6)" fill="#0B1020"><path d="M7.6 11.4a4.6 4.6 0 1 1 6.8 4c-1.4.8-2.2 1.6-2.2 3v.6" fill="none" '
        'stroke="#0B1020" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12.2" cy="24.6" r="1.85"/>'
        '<rect x="18" y="23.2" width="7.4" height="2.9" rx=".7"/></g></svg>')
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700&family=Hind+Siliguri:wght@500&display=block">'


def card(kicker, title, foot):
    size = 68 if len(title) < 60 else 58 if len(title) < 90 else 50
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
html,body{{margin:0;width:1200px;height:630px;background:#0B1020;color:#F1F5F9;font-family:Inter,system-ui,sans-serif}}
.c{{box-sizing:border-box;height:630px;padding:72px 80px;display:flex;flex-direction:column;border-bottom:10px solid #8B7CFF}}
.b{{display:flex;align-items:center;gap:18px;font-size:30px;font-weight:700;letter-spacing:-.01em}}
.k{{margin-top:auto;font-size:26px;font-weight:500;color:#A79BFF}}
h1{{margin:14px 0 0;font-size:{size}px;line-height:1.12;letter-spacing:-.025em;font-weight:700;max-width:1040px;text-wrap:balance}}
.f{{margin-top:36px;font-size:24px;color:#94A3B8}}
.f span{{font-family:"Hind Siliguri",sans-serif}}
</style></head><body><div class="c"><div class="b">{MARK.format(s=56)}Interview Prep BD</div>
<div class="k">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1><div class="f">{foot}</div></div></body></html>'''


def icon_page():
    return ('<!doctype html><html><head><style>html,body{margin:0;width:180px;height:180px;background:#8B7CFF}</style></head><body>'
            '<svg viewBox="0 0 32 32" width="180" height="180"><rect width="32" height="32" fill="#8B7CFF"/>'
            '<g transform="translate(16 15.4) scale(.78) translate(-16 -16)" fill="#0B1020"><path d="M7.6 11.4a4.6 4.6 0 1 1 6.8 4c-1.4.8-2.2 1.6-2.2 3v.6" fill="none" '
            'stroke="#0B1020" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12.2" cy="24.6" r="1.85"/>'
            '<rect x="18" y="23.2" width="7.4" height="2.9" rx=".7"/></g></svg></body></html>')


def shoot(chrome, page_html, out, w, h):
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, 'page.html')
        open(src, 'w', encoding='utf-8').write(page_html)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        f'--window-size={w},{h}', '--virtual-time-budget=4000', f'--screenshot={out}', 'file://' + src],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('wrote', os.path.relpath(out, bb.REPO))


def main():
    chrome = next((c for c in CHROME_CANDIDATES if c and os.path.exists(c)), None)
    if not chrome:
        sys.exit('Chrome/Chromium not found; set CHROME_BIN')
    content = os.path.join(bb.ROOT, 'content')
    site = bb.load_site(content)
    posts, errors = bb.load_posts(content, site, bb.load_tech(), bb.load_question_ids())
    if errors:
        sys.exit('\n'.join(errors))
    foot = 'Bilingual technical interview practice · English · <span>বাংলা</span>'
    shoot(chrome, card('Practice · Learn · Review', 'Technical interview preparation for developers in Bangladesh and beyond', foot),
          os.path.join(bb.REPO, 'assets', 'brand', 'og-default.png'), 1200, 630)
    shoot(chrome, icon_page(), os.path.join(bb.REPO, 'assets', 'brand', 'apple-touch-icon.png'), 180, 180)
    keep = set()
    for p in posts:
        if p['draft']:
            continue
        out = os.path.join(bb.REPO, 'assets', 'og', p['slug'] + '.png')
        keep.add(out)
        shoot(chrome, card(p['category'], p['title'], foot), out, 1200, 630)
    og_dir = os.path.join(bb.REPO, 'assets', 'og')
    for f in os.listdir(og_dir):
        if os.path.join(og_dir, f) not in keep:
            os.remove(os.path.join(og_dir, f))


if __name__ == '__main__':
    main()
