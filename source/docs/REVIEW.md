# Independent accuracy review — instructions

You are reviewing questions written by someone else. Be adversarial about correctness, but do not rewrite
good content for style. The bank is used by job seekers; a wrong "reference answer" actively harms them.

Read first: docs/FACTS.md (verified versions, 2026-10-12), docs/AUTHORING.md (format & display semantics).
Sources are Python files `data/src/<tech>_b*.py` (raw triple-quoted strings). The JSON in `data/json/` is generated.

For EVERY question in your categories check:
1. Technical correctness of `a_*`, `ex_*`, `tip_*`, `mist_*`, follow-ups — for the current versions in FACTS.md.
   Version-sensitive claims must match FACTS.md / official docs; legacy/deprecated approaches must be labelled.
2. MCQs: exactly one defensible correct option at `correct`; distractors plausible but definitely wrong;
   the explanation's option letters/positions match the actual option order.
3. Code: syntactically valid and correct for the stated version. Run what you can (node 22 is installed;
   `node --check`, small scripts; python3 sqlite3; PostgreSQL 16 may be running locally — `psql -U postgres`
   or check `pg_lsclusters`). `output` must be EXACT. For `output`/`debugging`/MCQ-with-code the code is shown
   with the question, so it must not leak the answer in comments.
4. Bangla (`*_bn`) says the same thing as English, technically accurate, natural (not word-for-word), tech
   terms in Latin script. Fix clear mistranslations or missing content; don't polish style needlessly.
5. References: official, relevant, plausible URLs (you may spot-check a few with WebFetch; curl is blocked).

Fixing: edit the `.py` source directly (keep ids, difficulty, type and counts unchanged unless a question is
fundamentally broken), re-run `python3 data/src/<file>.py`, then `python3 tools/check.py <tech>` must say OK.
Use WebFetch on official docs for anything you are not sure about — never "fix" something into a guess.
Rendering supports paragraphs, `- ` bullets, `1. ` numbered lists (no nesting), `code`, **bold**, *emphasis*.

Known verified facts beyond FACTS.md (don't "correct" these):
- NGINX ≥ 1.29.7 (so 1.30 stable): upstream keepalive is on by default (`keepalive 32 local`), `proxy_http_version`
  defaults to 1.1 and `Connection` is not sent upstream; the old `proxy_http_version 1.1; proxy_set_header
  Connection "";` recipe is only needed on ≤ 1.28. WebSocket proxying still needs the Upgrade/Connection map.
- node-redis v6: `{ expiration: { type: 'EX', value: 300 } }` is the current SET option; `{ EX: 300 }` deprecated.
- Express 5: `res.send(404)` sends status 200 with body `404` (number bodies no longer set status).
- Drizzle: latest stable 0.45.4; v1 is a release candidate (npm `rc` tag 1.0.0-rc.4; rc.5 builds exist).
- Mongoose 9.2+: `new: true` deprecated in favour of `returnDocument: 'after'`.

Report back: number of questions reviewed per category; a list of every change (id — what was wrong — fix);
anything suspicious you could not resolve; confirmation that check.py is OK for each category.
