"""package.py — build dist/: the 4-file app + README, a single-file standalone HTML, the source pipeline, and a zip."""
import glob, json, os, re, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
APP = os.path.join(DIST, 'interview-prep-bd')
shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(APP)
for f in ['index.html', 'styles.css', 'app.js', 'questions.js', 'README.md']:
    shutil.copy(os.path.join(ROOT, 'app', f), APP)
# Source pipeline
SRC = os.path.join(APP, 'source')
for d in ['data/src', 'data/json', 'tools', 'docs', 'app/src']:
    shutil.copytree(os.path.join(ROOT, d), os.path.join(SRC, d), ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.example.json'))
os.makedirs(os.path.join(SRC, 'tests'))
shutil.copy('/tmp/claude-0/e2e/e2e.mjs', os.path.join(SRC, 'tests', 'e2e.mjs'))
# Standalone single-file HTML
html = open(os.path.join(ROOT, 'app', 'index.html'), encoding='utf-8').read()
css = open(os.path.join(ROOT, 'app', 'styles.css'), encoding='utf-8').read()
app = open(os.path.join(ROOT, 'app', 'app.js'), encoding='utf-8').read()
assert '</script' not in app.lower() and '<!--' not in app
qjs = open(os.path.join(ROOT, 'app', 'questions.js'), encoding='utf-8').read()
start = qjs.index('window.QBANK = [') + len('window.QBANK = ')
data = json.loads(qjs[start:qjs.rindex(';')])
qinline = 'window.QBANK = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + ';'
assert '</script' not in qinline.lower()
html = html.replace('<link rel="stylesheet" href="styles.css">', '<style>\n' + css + '\n</style>')
html = html.replace('<script src="questions.js"></script>', '<script>\n' + qinline + '\n</script>')
html = html.replace('<script src="app.js"></script>', '<script>\n' + app + '\n</script>')
assert 'src="app.js"' not in html and 'href="styles.css"' not in html
open(os.path.join(DIST, 'interview-prep-bd-standalone.html'), 'w', encoding='utf-8').write(html)
# Zip
shutil.make_archive(os.path.join(DIST, 'interview-prep-bd'), 'zip', DIST, 'interview-prep-bd')
for f in sorted(os.listdir(DIST)):
    p = os.path.join(DIST, f)
    print(f, f'{os.path.getsize(p)/1024/1024:.2f} MB' if os.path.isfile(p) else '(dir)')
