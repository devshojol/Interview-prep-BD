# Interview Prep BD: audit report

| | |
|---|---|
| **Audit date** | 2026-10-26 |
| **Scope** | Live site <https://devshojol.github.io/Interview-prep-BD/> and local repo (`main` @ `9f78943`, clean) |
| **Mode** | Audit only. No project files were modified. This `audit/` folder is the only addition. |
| **Content coverage** | 584 / 584 questions, English and Bangla, every field |
| **Per-technology detail** | [`audit/content/<tech>.md`](content/) has the full issue register, a one-line verdict per question, gaps, items needing verification, and what was executed. Mentions of `dumps/…` or `run/…` in those files point to the reviewers' temporary working files, which were not kept. |

---

## A. Executive summary

**Content quality is not the bottleneck.** The 584-question bank is technically strong, current and properly bilingual. Every question was reviewed by a technology specialist who ran the code where possible: all JS/Node output and coding questions on Node 22.18, every portable SQL query in sqlite3, vector maths in Python, and Redis/NGINX/Mongo outputs traced by hand. The review found:

- **0 wrong MCQ answer keys**
- **0 wrong expected outputs**
- **0 P0 issues**
- **2 P1 issues** (both are "the explanation points at the wrong thing", not wrong concepts)
- **33 P2 issues**
- **206 P3 issues** (polish)

Category accuracy scores are 8.5–9.5/10 across all 18 technologies. Answers explain mechanisms, trade-offs and real production failure modes, not just definitions. Bangla is natural, keeps technical terms in Latin script, and matches the English in meaning and caveats; Bangla scores are 8–9/10.

**The real weaknesses are elsewhere, in this order:**

1. **Discoverability and SEO (the biggest product risk).** On the live site, the 584 answers are effectively invisible to search engines:
   - They exist only behind hash routes (`#/q/js-001`) inside a 4.9 MB JavaScript file.
   - Every blog page is `noindex`, and there is no sitemap, robots.txt or canonical URL.
   - The 404 page is broken on the GitHub Pages sub-path.

   The README describes this as a deliberate "preview build", but the site at the README's own URL is the public one.
2. **Time-sensitive version drift.** 50 questions label or recommend "Node.js 24 LTS". Node 24 moved to Maintenance on 2026-10-20, and Node 26 becomes Active LTS on **2026-10-28 (two days after this audit)**. Several other FACTS.md entries have also drifted since 2026-10-12, for example NestJS 12.2.0 on npm (2026-10-19) and CSS anchor positioning's Baseline status.
3. **MCQ mechanics.** Specifically:
   - 114 of 140 MCQs have no follow-up questions.
   - The answer key is skewed: option B is correct in 64 of 140 (46%).
   - 8 MCQs say "Option 2" while the UI shows A–D.
   - 4 MCQs use A–E labels inside the content that collide with the A–D option labels. One of them (nginx-012) states the wrong letter.
4. **A handful of example-code defects in "fixed"/"recommended" solutions.** These matter because learners copy them:
   - mongoose-026's fix breaks its own search.
   - next-028 recommends unsanitised `dangerouslySetInnerHTML`.
   - node-028's shutdown can hang forever.
   - redis-008's sliding session isn't sliding.
   - express-019's token-reuse detection is racy.
   - docker-031's rollback points at a stopped container.
5. **App bugs and UX friction:**
   - A literal "null" is rendered on empty search results.
   - Hidden filter state persists across navigation.
   - Bangla-script search returns nothing, even for the term shown in the placeholder.
   - Long multi-line question texts are flattened into giant bold headings.
   - Question pages have no `<h1>`.
6. **Coverage gaps (real but modest).** Each category has 1–4 genuinely missing junior-relevant topics: for example var/let/const + TDZ, `call`/`apply`/`bind`, change streams, `arrayFilters`, `useReducer`, React security, Next.js `<Link>`/prefetching, TypeORM/Prisma in NestJS, PostgreSQL 18 AIO, and `UNION`/`INTERSECT`/`EXCEPT`. There is also deliberate-looking but excessive cross-category repetition: the bank-transfer `balance >= amount` guard is taught 4×, "proxy is not a security boundary" 3×, and the `$ne` login injection several times.

**Readiness:** the content is ready for learners today. Fixing the 2 P1s, the copyable-code P2s and the Node 24 relabel takes days, not weeks. The product is **not** ready to attract learners through search until the SEO architecture (section F) is addressed.

---

## B. Project and route inventory

### Stack

- Static site with no framework, no backend and no runtime build step. Vanilla JS app (`index.html` + `styles.css` + `app.js` + `questions.js`) that also works from `file://`. Progress lives in `localStorage` (`ipbd:state`, versioned).
- `app.js` (291,919 B) is a plain concatenation of `source/app/src/00…99-*.js`. I verified it is byte-identical to `cat source/app/src/*.js`.
- `questions.js` (4,885,068 B) is `window.QBANK = [...]`, built by `source/tools/build_bank.py` from `source/data/src/<tech>_bN.py` (77 batch files) via `source/data/json/*.json`. The built bank matches the JSON exactly, except for an added `documentationUrl`.
- Blog: Markdown in `source/content/blog/*.md`, rendered by `source/tools/build_blog.py` (stdlib Python) into `blog/`.
- Content tooling and docs: `source/tools/check.py` (validator: **OK for all 18 techs**), `qb.py`, `build_*.py`, `package.py` (documented as broken), `source/docs/{AUTHORING,FACTS,COVERAGE,REVIEW}.md`.
- Tests: `source/tests/e2e.mjs` (Playwright + axe, 102 `check()` calls). It is **not runnable as committed** (see F-TECH-01).
- **Live vs local:** `index.html`, `app.js`, `questions.js`, `styles.css`, `404.html` and the blog files fetched from the live site are byte-identical to local HEAD (`curl` + `cmp`). The live `Last-Modified` is 2026-10-13 06:57 GMT, matching commit `9f78943`. **There is no discrepancy.**

### Routes (hash router, `40-views-a.js` `render()`)

`#/dashboard` (default) · `#/technologies` · `#/questions?tech=…` · `#/q/<id>` · `#/practice` · `#/session` · `#/results/<id>` · `#/interview` · `#/bookmarks` · `#/incorrect` · `#/review` · `#/history` · `#/planner` · `#/settings` · `#/flashcards` · `#/daily` · `#/sources` · fallback "not found" view.

Static pages: `/blog/`, plus 5 articles at `/blog/<slug>/`, plus `/404.html`.

### Content collections

**Technologies:** 18, each with 32 questions except JavaScript (40), for 584 in total:

- html, css, javascript, react, nextjs, nodejs, express, nestjs
- mongodb, mongoose, postgresql, sql, drizzle, redis, vectordb
- docker, nginx, aws

**Difficulty:** 201 easy / 201 medium / 127 hard / 55 extreme.

**Type:**

| Type | Count |
|---|---:|
| MCQ | 140 |
| Conceptual | 115 |
| Scenario | 67 |
| Debugging | 57 |
| Coding | 46 |
| Comparison | 44 |
| Security-performance | 27 |
| Query | 25 |
| Architecture | 23 |
| Output | 23 |
| System design | 17 |

**Market label:** both 457, bangladesh 72, international 55.

**Fields per question:**

- Bilingual: question, answer, explanation, interview tip, common mistakes, follow-ups, and MCQ options.
- Code: code/setup/output and extra code.
- Metadata: complexity, related, references, `technologyVersion`, `verifiedAt` (2026-10-12), `versionSensitive`, `status`.

**Blog:** 5 English articles (event loop, SQL joins/NULL, useEffect, Express 5 errors, how to practise). No Bangla articles exist yet.

### Major features (as implemented)

- **Question explorer:** text search (EN/BN substring), filters by tech, difficulty, type and market, and status filters (bookmarked, incorrect, unanswered, learned, review).
- **Question detail:** Learning vs Interview modes, reveal, self-grade (correct/partial/incorrect/skip), bookmark, flag, related questions, docs links, version box.
- **Practice:** presets and custom sessions, priority ordering, timer, resume after reload.
- **Interview simulation:** timed, auto-submit.
- **MCQ auto-grading**, daily challenge, flashcards with decks.
- **Progress and planning:** spaced review (1/3/7/14/30 days), weak-topic detection, planner, 16-week heatmap, history.
- **Data management:** export/import JSON, reset.
- **Interface:** EN / বাংলা / Both language modes, dark/light theme, text size, reduced motion, keyboard shortcuts, collapsible sidebar, mobile drawer.

### Verification limitations

- **Databases and servers:** no PostgreSQL, MongoDB, Redis, Docker or NGINX was available. Those outputs were checked by careful tracing, plus sqlite3 for portable SQL. Confidence is marked per issue.
- **Express/NestJS/Mongoose/Drizzle:** not installed. Behaviour was checked against official docs and npm (≈5–6 targeted web checks per reviewer).
- **Post-cutoff versions:** many FACTS.md versions (React 19.3, Next.js 16.4, Node 26, MongoDB 9.0, Compose v5, TS 7, and others) postdate the reviewers' training data. They were not marked wrong for that reason. Where checked online they held up; the rest are listed under "Needs verification" in each content file.
- **Bundled e2e suite:** not run, because its paths are hard-coded to another machine and installing dependencies was out of scope. Interactive behaviour was tested by hand on the live site instead (section F).
- **Performance:** cold-load timings were not captured (only a cached reload was measured). Transfer sizes were measured with `curl`.
- **Native-speaker proofreading:** the Bangla was reviewed for fidelity and naturalness by bilingual reviewers. The README itself notes it has not had a native-speaker proofread, and that remains true.

---

## C. Content audit: scores per category

Scores are 1–10, from the specialist reviewer of each category. "Orig." means originality and information value; "Struct." means structural clarity.

| Technology | Qs | Accuracy | Depth | Interview use | Bangla | English | Examples/code | Orig. | Struct. | P1 | P2 | P3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HTML | 32 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 0 | 2 | 9 |
| CSS | 32 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 0 | 1 | 12 |
| JavaScript | 40 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 0 | 2 | 16 |
| React | 32 | 9 | 9 | 9 | 8 | 9 | 9 | 8 | 9 | 0 | 1 | 12 |
| Next.js | 32 | 9 | 9 | 9 | 8 | 9 | 8 | 7 | 9 | 0 | 3 | 15 |
| Node.js | 32 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 0 | 3 | 10 |
| Express | 32 | 9 | 9 | 10 | 8 | 9 | 9 | 9 | 9 | 0 | 2 | 11 |
| NestJS | 32 | 9 | 9 | 9 | 9 | 9 | 8 | 9 | 9 | 0 | 1 | 13 |
| MongoDB | 32 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 0 | 3 | 7 |
| Mongoose | 32 | 8.5 | 9 | 9 | 9 | 9 | 8 | 9 | 9 | 1 | 2 | 8 |
| PostgreSQL | 32 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 0 | 1 | 12 |
| SQL | 32 | 9 | 9 | 10 | 8 | 9 | 10 | 9 | 9 | 0 | 1 | 17 |
| Drizzle | 32 | 9 | 10 | 9 | 9 | 9 | 9 | 9 | 8 | 0 | 1 | 12 |
| Redis | 32 | 9 | 9 | 9 | 8.5 | 9 | 8 | 9 | 9 | 0 | 3 | 8 |
| Vector DBs | 32 | 9.5 | 9 | 9 | 8.5 | 9 | 9 | 9 | 9 | 0 | 1 | 9 |
| Docker | 32 | 9 | 9 | 9 | 8 | 9 | 9 | 8 | 9 | 0 | 2 | 10 |
| NGINX | 32 | 9 | 9 | 9 | 8 | 9 | 9 | 9 | 8 | 1 | 1 | 12 |
| AWS | 32 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 8 | 0 | 3 | 13 |
| **Total** | **584** | | | | | | | | | **2** | **33** | **206** |

Blog (5 articles, assessed separately by the lead auditor):

- **Accuracy and depth:** high, with one P2 contradiction (BLOG-01). All four event-loop article outputs reproduced on Node 22.18.
- **Bangla:** not applicable (no Bangla articles yet).

### What the content does well (evidence)

- **Code is correct and tested.**
  - Every expected output checked was exact: 17/17 JS outputs, all SQL query results in sqlite3, and all vector maths (cosine, L2, RRF, recall/MRR).
  - No shown code leaks its answer.
- **Production-grade depth.** Examples:
  - the ALB/Node keep-alive 502 (aws)
  - EvalPlanQual re-checks (pg)
  - `proxy_cache_lock` (nginx)
  - fencing tokens over Redlock (redis)
  - the `pg.Pool` BEGIN/COMMIT trap (pg)
  - the Express 5 `res.send(404)` semantics
- **Version-aware.** Legacy approaches are labelled (Pages Router, `middleware.ts`, Express 4 wildcards, Mongoose callbacks), and current APIs are taught as current.
- **Faithful Bangla.** It is natural and keeps the same caveats, for example `component-এর`, `cache করা`, and first-person interview phrasing.

### Systemic content patterns (cross-category root causes)

| ID | Pattern | Affected | Severity |
|---|---|---|---|
| SYS-C01 | "Node.js 24 LTS" used as the current/recommended LTS in labels and text. It is stale since 2026-10-20 (Maintenance) and wrong after 2026-10-28 (Node 26 becomes LTS). | 50 questions: js-026, js-035, next-019, node-001…032 (all 32), express-007/026/027/031, sql-021, redis-019, docker-005/012/014/015/017/022/024, nginx-022/026, aws-012 | P2 (time-bound) |
| SYS-C02 | MCQs have no follow-up questions, while every non-MCQ has at least one. | 114 / 140 MCQs | P3 |
| SYS-C03 | The answer key is position-skewed and options are never shuffled (`correctIndex` B = 64, A = 32, C = 23, D = 21), so a learner can guess "B". | 140 MCQs; app has no option shuffling | P2 |
| SYS-C04 | Options are referred to by number while the UI shows A–D. | nest-009, aws-002/004/007/011/018/019/029 | P2 |
| SYS-C05 | Letters inside the question content collide with the A–D option labels. | **nginx-012 (P1: "The answer is D" but the keyed option is B)**, drizzle-008 (P2), css-022 and mongoose-025 (P3: confusing but not wrong) | P1–P3 |
| SYS-C06 | Stiff Bangla calque for "tempting wrong answer" repeated in MCQ explanations: লোভনীয় (51×), প্রলোভনজনক (15×), আকর্ষণীয় ফাঁদ (3×). | ~69 questions | P3 |
| SYS-C07 | Authoring notes leak into learner text: "Verified on/with…" (node-028, express-012/014/021/023/027/028, nest-029), "(Advanced…)" template openers (js-037…040, pg-032, sql-032), and "interviewers love…" filler (8×). | 22 questions | P3 |
| SYS-C08 | Unjustified `market` labels. Universal fundamentals are tagged `bangladesh` (e.g. html/css fundamentals, redis-002/020, vec-011), and sql-028 makes an unsourced claim about Bangladeshi banking/ERP systems. Local flavour (Dhaka, BDT, `bn-BD`, 64 districts) is used appropriately as context and is **not** a problem. | see per-tech files | P3 |
| SYS-C09 | The same lesson is taught several times across categories: the transfer `AND balance >= amount` guard (sql-010, pg-019, pg-023, sql-032), "proxy isn't the security boundary" (next-020/023/025), `$ne` login injection and the conditional `$inc` stock guard (mongo/mongoose), and `min-width:auto`, `will-change` and LCP images (css, 3–4× each). | see per-tech files | P3 |
| SYS-C10 | FACTS.md (the declared source of truth) has drifted since 2026-10-12: `@nestjs/core` 12.2.0 is on npm (2026-10-19, content says 12.1), Drizzle `rc` is now 1.0.0-rc.5, CSS anchor positioning may now be Baseline (Firefox 147, Jan 2026; unresolved), and the Node LTS handover (SYS-C01). | FACTS.md, plus content referencing these | P2 |

---

## D. Question-level issue register

This section lists every **P1 and P2** content issue (35 rows). All **206 P3** items, with the same columns, are in each technology's file under [](content/). That folder also has a one-line verdict for every one of the 584 questions. The cross-category root causes (SYS-C01 to SYS-C10) are in section C, and product, SEO and blog findings are in section F.

Columns: ID · Question(s) · Language · Severity · Category · Issue · Evidence · Recommended correction · Confidence · Verification / acceptance test.


### HTML ([full register](content/html.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| HTML-C01 | html-027 | both | P2 | Technical correctness (code/config) | The CSP allowlists only `app-sanitizer`. DOMPurify tries to create its own Trusted Types policy named `dompurify`, and internally calls `DOMParser.parseFromString`, which is itself a Trusted Types sink. With `trusted-types app-sanitizer` and enforcement on, DOMPurify's policy creation is blocked. Its parse step then receives a plain string, so sanitizing can throw a TypeError. The "one reviewed place" design breaks exactly where it is meant to work. | Header: `require-trusted-types-for 'script'; trusted-types app-sanitizer;` with `createHTML: (dirty) => DOMPurify.sanitize(dirty)` | Allowlist both names (`trusted-types app-sanitizer dompurify`), or mention that DOMPurify needs its own policy name or `RETURN_TRUSTED_TYPE`. Add one sentence: "sanitizer libraries need their own policy name allowlisted". | Medium | In Chrome, serve the page with the header and call `renderComment` with HTML input. There should be no TypeError and no "policy dompurify could not be created" warning. |
| HTML-C02 | html-024 | both | P2 | Technical correctness (a11y) | The common-mistakes section lists "injecting a `role="alert"` element together with its text and expecting it to be announced" as a mistake. In practice `role="alert"` is the exception: most screen readers announce it even when it is inserted along with its content. Generic `aria-live`/`role="status"` regions are the ones that must already exist in the DOM. The explanation bullet about live regions is correct, but this mistake is overstated. | "or injecting a `role="alert"` element together with its text and expecting it to be announced." | Reword: "injecting an `aria-live`/`role="status"` region together with its text (it often isn't announced); `role="alert"` is more forgiving but still most reliable when the container already exists". | Medium | Test with NVDA+Chrome and VoiceOver+Safari: inject `<div role=alert>Error</div>`. It is announced. |

### CSS ([full register](content/css.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| CSS-C01 | css-028 (and FACTS.md Baseline list) | both | P2 | Version currency | Anchor positioning is taught as "limited availability, not Baseline". Caniuse and several sources report Firefox 147 (Jan 2026) shipping it unflagged; Chrome 125+ and Safari 26 already had it. The core feature may now be Baseline newly available, with the group status possibly still "limited" for newer sub-features (`position-visibility`, `anchor-size()`). The question presents itself as authoritative "It's October 2026" content, so a stale status here is costly. | "Enhancement: anchor positioning (limited availability, not Baseline)"; "**anchor positioning**, **scroll-driven animations** … not Baseline yet" | Check web-features/webstatus.dev for the current status. If it is newly available, move it to the "Newly available" bucket and keep the `@supports` fallback advice. If the group is still limited, say "core anchoring works in all engines since early 2026, but the feature group is still flagged limited". | Medium | webstatus.dev/features/anchor-positioning shows the status, and the text matches it. |

### JavaScript ([full register](content/javascript.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| JS-C01 | js-026 | both | P2 | Technical accuracy (misleading mechanism) | The text says the CJS value is copied at destructuring time. The copy actually happens when the exporter builds `module.exports = { count, … }`, so even `require('./counter.cjs').count` stays `0` without any destructuring. Learners will wrongly conclude that "don't destructure" fixes it. | "CommonJS copies whatever is on `module.exports` when you destructure it"; "CommonJS prints `0` because destructuring copied the number"; BN "CommonJS-এ destructure করলে সেই মুহূর্তে `module.exports`-এ যা আছে তার copy পাও" | Say: "`module.exports = { count }` stores the current value of `count` (0) in a property. Later `count++` changes the local variable, not the exported property, so every importer sees 0 whether or not it destructures. ESM imports are live bindings to the variable itself." Optionally mention exposing a getter (`get count() { return count; }`). | High | Ran counter.cjs/main.cjs: destructured → `0`, `m.count` without destructuring → `0`; ESM → `1`. |
| JS-C02 | js-027 | both | P2 | MCQ distractor rationale wrong | `[1, 4, 9]` is the result of ignoring `filter` (squares of 1, 2, 3). If `take(3)` ran before `filter`, the result would be `[4]`. | "**Option C** assumes `take` runs before `filter`; the chain order is respected." BN "Option C ধরে নেয় `take` `filter`-এর আগে চলে" | "Option C forgets the `filter` step (it squares 1, 2, 3). Note that even if `take` ran first you would get `[4]`; the chain runs in the written order, one value at a time." | High | Manual trace; ran the code → `[ 4, 16, 36 ]`. |

### React ([full register](content/react.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| REACT-C01 | react-029 (category-level) | both | P2 | Coverage gap | No React security question. COVERAGE lists accessibility and production debugging, and AUTHORING asks for a security-performance item. The only one (029) is about performance; security gets a single line ("never ship 10,000 rows… filter on the server"). XSS via `dangerouslySetInnerHTML`, `javascript:` URLs in `href`, sanitising CMS HTML, and keeping React/RSC patched after the Dec-2025 RSC CVEs (FACTS) are never taught. | 029 EXPLANATION: "Security/perf angle: never ship 10,000 rows of data the user isn't allowed to see" | Add one medium/hard security question: a `dangerouslySetInnerHTML` + `href={userUrl}` debugging task with a DOMPurify/URL-allowlist fix, plus a note on RSC patching (react-dom 19.x security releases). | High | The category contains a question whose answer covers sanitisation, `javascript:` URL blocking and dependency patching. |

### Next.js ([full register](content/nextjs.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| NEXT-C01 | next-028 | code | P2 | Security in example | The "AFTER" code (the recommended version) in a **security-performance** question parses CMS markdown with `marked` and injects it via `dangerouslySetInnerHTML` with only a comment saying to sanitise. `marked` does not sanitise. Learners will copy an XSS-prone pattern as "best practice". | `const html = await marked.parse(post.markdown);` … `<div dangerouslySetInnerHTML={{ __html: html }} /> {/* sanitise CMS HTML */}` | Actually sanitise on the server: `const html = sanitizeHtml(await marked.parse(post.markdown))` (sanitize-html or isomorphic-dompurify). Add one sentence to "Security angle": moving parsing to the server doesn't remove the XSS risk. | High | Recommended code contains a sanitisation call; explanation mentions it. |
| NEXT-C02 | next-020, next-023, next-025 | both | P2 | Redundancy | Three questions share the same core lesson and near-identical sentences: proxy is optimistic, Server Actions are POSTs to the page route so a matcher change can skip them, and a DAL must verify. 020 is effectively an MCQ version of 023. | 020: "a matcher change or moving the action to another route can silently remove proxy coverage"; 023: "a matcher change can silently skip them"; 025: "a matcher change can silently skip them" | Keep 023 (deep) and 025 (proxy coding). Repurpose 020 into a currently missing topic (e.g. an MCQ on `<Link>` prefetching, `revalidatePath` vs `revalidateTag`, or `next/font`). | High | No two questions share the same primary learning objective. |
| NEXT-C04 | next-001…032 (category) | both | P2 | Coverage gap | Missing or thin topics for the target audience: <br>- `<Link>`/client navigation and prefetching, including the 16.4 additions in FACTS (`partialPrefetching`, `export const ensureStatic`, `navigation()`/`prefetch()` from `next/cache`) — no question; <br>- `next/font` — only listed in 001; <br>- `revalidatePath` — mentioned only; <br>- testing a Next.js app (Playwright, testing Server Actions) — only a phrase in 031; <br>- `after()` — mention only; <br>- i18n routing — absent. | 014 code: `partialPrefetching: true` (never explained) | Add a medium question on navigation/prefetching (Link, `useRouter` from `next/navigation`, `prefetch`, Partial Prefetching/App Shell in 16.4). Fold `next/font` into 008 or 028. | High | COVERAGE + FACTS 16.4 items have at least one primary question. |

### Node.js ([full register](content/nodejs.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| NODE-C01 | node-022 | both | P2 | Version currency | The release-calendar answer is now stale. Per FACTS, v24 went to Maintenance on 2026-10-20 and v26 becomes Active LTS on 2026-10-28. Today (2026-10-26) v24 is no longer "Active LTS". The question says only "It is October 2026", so the key depends on which day. | "As of 12 October 2026, v24 is Active LTS, and v26 is still Current until it is promoted to LTS on 28 October 2026" / Option B "Node.js 24 — the Active LTS line" | Pin the question to a date ("On 12 October 2026…"). Or reword option B to "the newest LTS line (v24 now, v26 from 28 Oct 2026)". Add a review date, because status=version-specific. | High | The question carries an explicit date, and the key stays correct for the whole of October 2026. |
| NODE-C03 | node-023 | both | P2 | Technical correctness (debugging premise) | The scenario names "write after end" as a symptom. After a client disconnects, `res.write()` on the destroyed response fails with `ERR_STREAM_DESTROYED`, reported via the write callback, and no `'error'` event is emitted. `ERR_STREAM_WRITE_AFTER_END` only happens after `res.end()`, which this code never calls. | Q: "occasional "write after end" errors"; A: "writes to a closed response — the "write after end" errors" | Change the symptom to "`ERR_STREAM_DESTROYED` / writes to destroyed sockets (`write()` returns false)", or say "write-after-close errors". Keep the rest. | Medium-High (verified with node:http on Node 22; Express `res` is the same object) | Run the SSE repro: a client disconnects, then `res.write` callback receives `ERR_STREAM_DESTROYED`. |
| NODE-C04 | node-028 | both | P2 | Code correctness vs requirement | The solution clears the safety-net timer in `finally` and then relies on `process.exitCode`. If any handle stays open after `closeResources()` (a Redis client not quit, a non-unref'd interval, a keep-alive outbound socket), the process hangs forever. That breaks the stated requirement "never hang longer than 10 seconds". The force timer is already `unref()`'d, so clearing it gains nothing. node-020 uses `process.exit(0)` instead, so the two answers give conflicting advice. | "finally { clearTimeout(forceTimer); }" and Q: "never hang longer than 10 seconds in total" | Don't clear the unref'd force timer. Or call `process.exit(process.exitCode)` after cleanup and a log flush. Explain the choice and align node-020 with node-028. | High (logic) | Add `setInterval(()=>{},1000)` (not unref'd) as a "leaked handle". The process must still exit in 10 s or less. |

### Express ([full register](content/express.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| EXP-C01 | express-032 | both | P2 | Internal inconsistency | The explanation justifies PostgreSQL by "writing the payment row and marking the key completed in the same PostgreSQL transaction". The code does something different: it marks the key in a separate `UPDATE` inside a `res.json` override, outside any payment transaction. Also, responses sent with `res.send`/`res.sendStatus`/`res.end` bypass the override, which leaves the row stuck `in_progress`. | EXPL: "writing the payment row and marking the key `completed` in the same PostgreSQL transaction keeps them consistent"; CODE: "res.json = (body) => { const done = … db.query(`UPDATE idempotency_keys …`" | Either (a) say the middleware approach is "eventually consistent, with reconciliation covering the gap", or (b) show the handler completing the key inside the payment transaction (`client.query` in the same `BEGIN…COMMIT`). Note that only `res.json` responses are captured. | High | Text and code describe the same mechanism. |
| EXP-C02 | express-019 | both | P2 | Code correctness (race) | Reuse detection is check-then-act. `findByHash` and the `usedAt` check run before `rotate()`. Two concurrent requests with the same (stolen or duplicated) token both see `usedAt == null` and both receive valid new tokens, so reuse goes undetected. A transaction around the writes alone doesn't prevent this. The handler also never checks that `users.findById` returned an active user. | "if (record.usedAt) { … }" … "await refreshTokens.rotate(record, { // mark old used + insert new, in one transaction" | Make the claim atomic: `UPDATE refresh_tokens SET used_at = now() WHERE token_hash = $1 AND used_at IS NULL RETURNING …`. If 0 rows are updated, treat it as reuse (or as the grace-window case). Reject if the user is missing or disabled. | Medium-High | Two parallel `/auth/refresh` calls with the same cookie → exactly one 200; the other 401 (or the defined grace behaviour). |

### NestJS ([full register](content/nestjs.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| NEST-C15 | (category) | both | P2 | Coverage gap | COVERAGE asks for "database integration (TypeORM/Prisma/Drizzle/Mongoose)". Only Drizzle has a worked question (nest-022). TypeORM, Prisma and `@nestjs/mongoose` get one sentence each, even though FACTS notes BD job posts list Mongoose/Prisma/TypeORM. | nest-022: "TypeORM has `@nestjs/typeorm` (`forRootAsync` + `forFeature` + `@InjectRepository`), Mongoose has `@nestjs/mongoose`, and Prisma is usually a `PrismaService` provider" | Add one medium question, e.g. "`@nestjs/mongoose` `MongooseModule.forFeature` + `@InjectModel` vs a `PrismaService` with `onModuleInit`/shutdown". Or extend nest-022 with a short example. | High | The bank has at least one question with a Mongoose or Prisma/TypeORM Nest code sample |

### MongoDB ([full register](content/mongodb.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| MONGO-C01 | mongo-022 | both | P2 | Technical accuracy | The definition of the `moderate` validation level leaves out inserts. In `moderate` mode, inserts are validated, and so are updates to documents that were already valid. | EN: "`moderate` only checks updates to documents that were already valid"; BN: "`moderate` শুধু আগে থেকে valid document-এর update check করে" | "`moderate` validates all inserts, and updates only to documents that were already valid (existing invalid documents can still be updated freely)." | High | Matches the MongoDB Schema Validation docs ("validationLevel: moderate"). |
| MONGO-C03 | mongo-014 | BN | P2 | BN meaning drift | "একটাই item" means "only one item". That suggests an order with exactly one item, not "one and the same element satisfies both conditions", which is what the question tests. | BN Q: "যেখানে **একটাই item**-এর SKU \"A\" এবং `qty ≥ 5`" | Use "যেখানে **একই item**-এর SKU \"A\" আর `qty ≥ 5`" (or "একটা item-ই দুইটা শর্ত পূরণ করে"). | High | A BN reader understands the question as "the same element matches both conditions". |
| MONGO-C10 | (category) | — | P2 | Coverage gap | Change streams appear in answers (mongo-020, mongo-029, mongo-030) but are never asked about. There is no question on array update operators (`$`, `$[]`, `$[<id>]` with `arrayFilters`) or on geospatial `2dsphere` / `$near`. These are common in MERN interviews (e.g. "update one item's qty inside an order"). | — | Add 1–2 medium questions: change streams (resume tokens, need for a replica set), and an `arrayFilters` update query. Optionally, a geo "nearby shops" query. | Medium | COVERAGE review. |

### Mongoose ([full register](content/mongoose.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| MGS-C01 | mongoose-026 | both (code) | P1 | Wrong code / misleading fix | The fixed version turns on `sanitizeFilter` globally and then builds a filter with its own `$regex` operator. `sanitizeFilter` wraps any nested object with a `$`-prefixed key in `$eq`. So `{ nameLower: { $regex: "^abc" } }` becomes `{ nameLower: { $eq: { $regex: "^abc" } } }` and the search returns nothing. The answer text mentions `mongoose.trusted()`, but the code doesn't apply it. | Code: `mongoose.set("sanitizeFilter", true);` … `Product.find({ nameLower: { $regex: \`^${safe}\` } })` | Use `Product.find({ nameLower: mongoose.trusted({ $regex: \`^${safe}\` }) })` (or a `RegExp` object: `{ nameLower: new RegExp(\`^${safe}\`) }`, which isn't a `$`-key object). Add a sentence saying operators you add yourself must be wrapped in `trusted()` once `sanitizeFilter` is on. | High | Mongoose API docs: sanitizeFilter "wrap[s] any nested objects that have a property whose name starts with `$` in a `$eq`"; `trusted()` opts out. Acceptance test: with `sanitizeFilter: true`, the fixed search returns the matching products. |
| MGS-C05 | mongoose-032 | both | P2 | Scenario/answer gap | The scenario says the app "calls `syncIndexes()` at startup" and "no error surfaced". An awaited `syncIndexes()` rejects when the unique build fails on duplicates. The answer explains the silence only through the `autoIndex` `'index'` event and never says why the `syncIndexes()` rejection went unnoticed. | Q: "the app calls `syncIndexes()` at startup … no error surfaced"; A: "Mongoose reports that only as an `'index'` error event / log line" | Add: "the startup `syncIndexes()` call was fire-and-forget / caught-and-logged (or ran in only one pod and failed there), so its rejection was swallowed", or change the scenario. | Medium | The explanation covers both index paths. |
| MGS-C11 | (category) | — | P2 | Coverage gap | No question on TypeScript with Mongoose (`InferSchemaType`, `HydratedDocument`, typing methods and statics). It's only a follow-up in 008 and a passing mention in 021. Nothing on subdocument arrays (`doc.items.id()`, positional `$` / `arrayFilters` via Mongoose), and nothing on `Model.watch()` change streams. TS + Mongoose is very common in NestJS/MERN roles. | mongoose-008 follow-up: "How would you type instance methods and statics in TypeScript?" | Add a medium TS-typing question and an easy/medium subdocument-array update question. | Medium | COVERAGE review. |

### PostgreSQL ([full register](content/postgresql.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| PG-C07 | (category) | — | P2 | Coverage gap | COVERAGE.md lists "PostgreSQL 18 features (… AIO)". No question or explanation mentions the asynchronous I/O subsystem (`io_method`); a grep for `io_method`/`AIO` finds nothing. | COVERAGE: "PostgreSQL 18 features (uuidv7, virtual generated columns, skip scan, OLD/NEW RETURNING, AIO)" | Add a short mention, e.g. in pg-029/pg-031 explanation or a "what's new in PG18" MCQ: `io_method` (`worker` default, `io_uring` on Linux, `sync`) speeds up seq scans, bitmap heap scans and vacuum reads | High | AIO mentioned with correct GUC name and status |

### SQL ([full register](content/sql.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| SQL-C01 | sql-002 | both | P2 | Technical accuracy | The claim is wrong for `USING`. `USING (col)` names its join columns explicitly, so adding a same-named column elsewhere does not change it. Only `NATURAL JOIN` (which joins on *all* common column names) silently changes. The real `USING` caveats are different: the merged output column, and needing to qualify it. | "Avoid `NATURAL JOIN` / `USING` on wide schemas: adding a column with the same name can silently change the join." / BN "`NATURAL JOIN` / `USING` এড়িয়ে চলো: একই নামের নতুন column যোগ হলে join নীরবে বদলে যেতে পারে।" | "Avoid `NATURAL JOIN`: it joins on every same-named column, so adding e.g. `created_at` to both tables silently changes the join. `USING (id)` is explicit and safe, but merges the join column into one." | High | Text distinguishes NATURAL from USING in EN and BN |

### Drizzle ORM ([full register](content/drizzle.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| DRZ-C01 | drizzle-008 | both | P2 | MCQ structure / ambiguity | The code lines are labelled A–D, and the four answer options are also lettered A–D. So the correct option is "A" while its text is "Only D", and the explanation switches between line letters and option letters. A learner can easily misread which "D" or "B/C" is meant. | Code: "// A … // D"; options: "OPTION A (CORRECT): Only D"; explanation: "The tempting wrong answer is B/C" (lines) … "Option D in the list ('Drizzle escapes everything')" (option) | Label the code lines 1–4 (or i–iv) and rewrite the options as "Only line 4", "Lines 2 and 3", and so on. Update the explanation to match. | High | Learner text never uses the same letter for both a line and an option |

### Redis ([full register](content/redis.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| REDIS-C01 | redis-005, redis-012, redis-013 (fixed version), redis-023 | both | P2 | Technical accuracy / code | Claims of graceful fallback or fail-open when Redis is down, but clients use node-redis defaults: the offline queue is enabled, so commands are queued while reconnecting and only reject at the default 5 s `commandTimeout` (v6). Each request stalls instead of failing fast. redis-019 itself explains this ("requests hang instead of falling back"), so the bank is internally inconsistent. | 012: `console.error('Rate limiter unavailable, failing open:'...)` with a client created without options; 005: "if Redis goes down the app can still read from the database"; 013 fix: `console.warn('Cache read failed, falling back to DB'...)` | Create the shared client with `disableOfflineQueue: true` (and/or a short per-command timeout) in these snippets, or add a sentence: "this fallback only triggers promptly if the client fails fast (see redis-019)". | Medium-High | Stop Redis while the app runs: with the current snippet, a request hangs up to ~5 s; with `disableOfflineQueue: true` it hits the catch immediately. |
| REDIS-C02 | redis-008 | both | P2 | Technical accuracy / code | "Sliding expiration" is broken. `GETEX` refreshes the Redis TTL on every request, but the cookie is set once at login with `maxAge: SESSION_TTL * 1000` and never re-issued. The browser drops the cookie 24 h after login regardless of activity, so "log out after 24 h of inactivity" really means "log out 24 h after login". | `res.cookie('sid', sid, { ... maxAge: SESSION_TTL * 1000 })` only in `createSession`; answer: "refresh the TTL for **sliding expiration** if you want 'log out after 24 h of inactivity'" | In the middleware, re-set the cookie (same options) when the session is valid, or use a session cookie (no maxAge) and rely on the server TTL. Add an absolute maximum lifetime as a best practice. | High | Log in, stay active for 25 h: with the current code the cookie expires at 24 h and the user is logged out. |
| REDIS-C03 | redis-021 (vs redis-019) | both | P2 | Internal inconsistency / version | redis-019 says node-redis v6 defaults to RESP3 (confirmed by the v6 release notes). Under RESP3, node-redis returns XREAD/XREADGROUP as a map keyed by stream name, not an array of `{name, messages}`. The redis-021 loop would then silently process nothing. | `for (const m of res?.[0]?.messages ?? []) await handle(m);`; redis-019: "Both v6 lines default to **RESP3**" | Either show the RESP3 shape (`res?.[STREAM]` / `Object.values(res ?? {})`, per the v6 docs) or create the client with `RESP: 2` and say so. Also loop `XAUTOCLAIM` on `nextId` as the explanation says. | Medium (exact RESP3 transform shape not verified against v6 source) | Run the snippet against Redis 8 with node-redis 6.3 defaults and log `res`. Messages must be processed. |

### Vector Databases ([full register](content/vectordb.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| VEC-C01 | vec-010 | both | P2 | Misleading simplification | The keyed answer and its extra SQL imply that putting `WHERE price < 2000` in the same pgvector query avoids the "too few results" problem of option C. With an HNSW index, pgvector applies the WHERE after the index scan (as vec-013/025 explain), so the query can still return fewer than 10 rows unless iterative scans are on or the planner picks a B-tree path. | Option B "applying both in the same query"; extra code `WHERE price < 2000 AND in_stock ... ORDER BY embedding <=> $1 LIMIT 10` with no `hnsw.iterative_scan` | Add one line under the extra code: "with an HNSW index, also `SET hnsw.iterative_scan = relaxed_order` (pgvector 0.8+) or raise `ef_search`; see vec-025". Optionally add that line to the SQL. | High | The extra code/explanation mentions iterative scan, consistent with vec-013/025. |

### Docker ([full register](content/docker.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| DOCKER-C01 | docker-031 | both | P2 | Technical correctness | The rollback step is inconsistent with the deploy flow. The script `docker stop`s the old slot, but rollback is described as only switching the NGINX include back. That would point NGINX at a stopped container and cause 502s. | "`docker stop -t 30` the old slot so it drains → keep its image for instant rollback" … "**Rollback:** switch the include back and reload. That takes seconds and needs no rebuild." | Either keep the old slot running (idle) for a soak period and then stop it, or say that rollback = `docker start api_<old>` → wait for healthy → switch include → reload. | High | The rollback text names a step that (re)starts and health-gates the old container, or the script delays `docker stop` of the old slot. |
| DOCKER-C03 | docker-019 | both | P2 | Misleading detail | The 10-second rule is misexplained. Containers that exit immediately are still restarted. The 10 s marks a "successful start" (it resets the back-off delay). Tight loops are prevented by the exponential back-off (100 ms doubling), not by the 10 s rule. | "A restart policy only takes effect after the container has stayed up for at least 10 seconds, which prevents tight restart loops on boot failures." | Rephrase: "Docker restarts with an increasing delay (starting at 100 ms, doubling); the delay resets once the container has run ~10 s. A container failing at boot shows `Restarting (1)` with growing gaps." Mirror in BN. | Medium | The text no longer implies that fast-failing containers aren't restarted. Check against the docs page "Start containers automatically". |

### NGINX ([full register](content/nginx.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| NGINX-C01 | nginx-012 | both | P1 | MCQ letter mismatch | The locations return the strings "A"–"E", and the options are also lettered A–D. The keyed option is **B** (whose text starts "D — …"), but the answer says "The answer is **D**". The explanation also calls response "B" (option A) "the tempting wrong answer" and response "C" (option C). Learners will read this as a wrong key. | ANSWER: "The answer is **D**." ; OPTION B (CORRECT): "D — the regex location wins…" ; "The tempting wrong answer is B" | Rename the returned bodies to non-letters (e.g. `return 200 "root"`, `"images"`, `"icons"`, `"regex"`, `"logo"`) and update options/explanation, or refer to options only by content. Same in BN. | High | Each letter mentioned in the answer/explanation is the same letter as the option it refers to. |
| NGINX-C02 | nginx-009 | both | P2 | Incorrect verification step | The tip's check uses `curl -I` (a HEAD request). NGINX's gzip header filter skips header-only responses, so `Content-Encoding: gzip` never appears and the learner concludes gzip is broken. (The extra code, which uses GET, is correct.) | TIP: "Verify with `curl -H 'Accept-Encoding: gzip' -I`." / BN "`curl -H 'Accept-Encoding: gzip' -I` দিয়ে যাচাই করো।" | Use `curl -s -o /dev/null -D - -H 'Accept-Encoding: gzip' URL` (as in the extra code) and note "HEAD responses aren't gzipped". | High (source verified) | Tip command is a GET. |

### AWS ([full register](content/aws.md))

| ID | Question(s) | Lang | Sev | Category | Issue | Evidence | Recommended correction | Confidence | Verification |
|---|---|---|---|---|---|---|---|---|---|
| AWS-C01 | aws-002, aws-004, aws-007, aws-011, aws-018, aws-019, aws-029 | both | P2 | MCQ structure | Answers and explanations name options by number, but the app renders options as an `<ol type="A">` and shows the key as "Correct answer: B — …". Learners see A–D, so "Option 4" has to be mentally translated, and aws-002 even says "The second option". | aws-002: "**Option 4 is the tempting trap.**", "Option 1 is wrong twice"; aws-029: "Option 2. Only **REST APIs**…"; BN "Option 4 হলো আকর্ষণীয় ফাঁদ" (app.js:3100 `h('ol', { type: 'A' …`, 3104 `'ABCD'[q.correctIndex]`) | Replace Option 1/2/3/4 with A/B/C/D in a_en/a_bn/ex_en/ex_bn for all 7 MCQs. | High | grep `Option [1-4]` in aws dump returns 0 hits; each explanation's letters match the rendered list. |
| AWS-C03 | aws-016 | both | P2 | Technical accuracy (code comment) | The code comment says an RDS-managed secret contains host/port. A secret created by RDS master-password management (`ManageMasterUserPassword`, `rds!db-…`) stores only `username` and `password`. Host/port only appear in secrets created through the Secrets Manager "credentials for RDS" flow. The destructuring `{ username, password, host, port }` would give `host`/`port` = undefined for an RDS-managed secret. | `// RDS-managed secret: JSON with username/password/host/port` … `const { username, password, host, port } = JSON.parse(db.SecretString);` | Change the comment to "Secrets Manager database secret (username/password/host/port)", or keep the RDS-managed secret and read host/port from config. Optionally note that RDS-managed secrets rotate every 7 days by default. | Medium (RDS doc fetched; it doesn't list the JSON fields, but from knowledge an `rds!` secret holds username/password only) | Run `aws secretsmanager get-secret-value` on an `rds!db-…` secret and check the keys. |
| AWS-C07 | aws-023 | both | P2 | Depth gap (security of design) | CloudFront + WAF fronts a *public* ALB, but nothing stops clients from hitting the ALB directly and bypassing WAF and caching. Restricting the origin is a standard senior-level point. | "`/api/*` behaviour forwards to the ALB with caching disabled"; "an **ALB** in public subnets" | Add: restrict the ALB SG to the CloudFront managed prefix list (`com.amazonaws.global.cloudfront.origin-facing`) plus a secret custom origin header checked by a listener rule, or use CloudFront VPC origins with an internal ALB. | Medium-High | Explanation mentions origin protection for the ALB. |

---

## E. Missing-content and coverage report

Every category covers every subtopic its `COVERAGE.md` entry requires, with one exception: PostgreSQL 18 AIO (`io_method`) is never mentioned (PG-C07). The difficulty mix is on target everywhere (11/11/7/3; JS 14/14/8/4). The gaps below are the ones that matter for **junior-to-mid candidates** or are explicitly promised by COVERAGE/FACTS. They are not padding.

| Tech | Genuinely missing (recommend adding) | Redundant / trim or cross-link | Difficulty notes |
|---|---|---|---|
| HTML | Accessible data tables (`caption`, `th scope`); `target="_blank"` + `rel`; iframe `sandbox` | — | — |
| CSS | `display` block/inline/inline-block; centering techniques; units (`rem`/`em`/`vh`/`dvh`) | `min-width:auto`, `will-change` and LCP image each taught 3–4× | — |
| JavaScript | var/let/const + TDZ (dedicated); `call`/`apply`/`bind` (implement `bind`); easy/medium DOM manipulation | js-016 / js-017 / js-029 (event-loop ordering ×3) | — |
| React | Security (XSS, `javascript:` URLs, patching after the Dec-2025 RSC CVEs); `useReducer`; `use(promise)`; Fragment refs and `browser()` as primary topics (COVERAGE lists them); `useLayoutEffect` | 004/021 (index keys), 012/027 (`useEffectEvent`); identical `<Context value>` paragraph in react-008 and next-021 | — |
| Next.js | `<Link>`/navigation/prefetching (incl. 16.4 `partialPrefetching`/`ensureStatic`/`navigation()`/`prefetch()` listed in FACTS); `next/font`; testing; `after()`; i18n | 020/023/025 (proxy ≠ security boundary ×3), 006/029 | next-010 is arguably medium |
| Node.js | `uncaughtException` semantics (`exit` vs `beforeExit`); practical `node:test`/`--watch` | acceptable progression pairs | node-019 reads as medium |
| Express | CSRF now that `csurf` is deprecated; `express.Router` composition (`mergeParams`); compression/streaming | Express 5 `req.query`/`req.body` changes taught in 003, 012, 030, 031 | — |
| NestJS | Worked TypeORM / Prisma / `@nestjs/mongoose` integration (the BD MERN/NestJS job posts cited in FACTS list these) | Drizzle overlaps (nest-022/025/032 vs drizzle-003/019/025) | — |
| MongoDB | Change streams (mentioned 3×, never asked); array updates with `$[]`/`arrayFilters`; geospatial `2dsphere`/`$near`; `$jsonSchema` validation | `$ne` injection and conditional `$inc` stock guard repeated with Mongoose | — |
| Mongoose | TypeScript (`InferSchemaType`, `HydratedDocument`); subdocument arrays/positional updates; `watch()` | see MongoDB | — |
| PostgreSQL | PG18 AIO (`io_method`) | pg-019 vs pg-023 (transfer guard) | — |
| SQL | `UNION`/`INTERSECT`/`EXCEPT` set operations | sql-012/013 and sql-014/025 (intentional); transfer guard (sql-010, sql-032 + pg) | sql-024 is medium, not hard |
| Drizzle | Optional: bulk insert, `drizzle-zod`, `jsonb` `$type<T>()`, `pgView`, testing with PGlite | overlaps with NestJS | — |
| Redis | Token bucket with Lua (named in COVERAGE, only prose); pipelining vs MULTI; HyperLogLog/bitmaps | acceptable | redis-029 arguably medium |
| Vector DBs | Optional: sparse vectors; HNSW delete/update bloat | 013/025 overlap on post-filtering | — |
| Docker | Basic container debugging toolkit (`exec`, `inspect`, `cp`, `compose logs`) as a direct easy question; Compose Watch; `docker init` | — | docker-019 could be easy |
| NGINX | Redirects/rewrites (`return 301` vs `rewrite`, www→apex); `server_name` selection; `stream {}` TCP proxy; `allow/deny`/`auth_basic` | — | nginx-021 could be easy |
| AWS | Dedicated Auto Scaling question (target tracking, health checks, warm-up) | intentional progressions (003→004, 015→024) | — |

**Bangladesh relevance.** The bank serves BD candidates well. It has viva-style fundamentals, MCQ and output tracing (the format FACTS cites from public BD interview reviews), MERN/NestJS stack combinations, and realistic local context: Dhaka time zone (UTC+6) bugs, BDT pricing, Bangla `lang="bn"`/UTF-8, bilingual district search, and mobile-first on mid-range Android. **No question claims a specific company asked it**, and there are no frequency, salary or outcome guarantees. The issues are limited to labelling (SYS-C08) and one unsourced sector claim (sql-028). Two points remain:

- The app has **no behavioural/HR questions** and **no DSA/aptitude section**, though FACTS itself says BD hiring includes aptitude MCQs and LeetCode-style easy/medium problems. That is a scope decision for the owner, not a defect. If added, it would be the highest-value expansion for BD juniors.
- **There is no Bangla blog content.** The build already supports `blog/bn/<slug>/` with `hreflang`.

---

## F. Product and technical audit

All observations below were made on the **live site** (identical to HEAD) in the in-app browser at 1024 px and 375 px, plus source reading.

### Functionality

| ID | Sev | Where | Observed problem (evidence) | Impact | Recommended fix | Acceptance test |
|---|---|---|---|---|---|---|
| F-FUNC-01 | P2 | `source/app/src/40-views-a.js:474` | Results count renders **"0 matching questionsnull"**. The ternary passes `null` to `Element.append()`, which stringifies it. Seen live after a search with 0 hits (screenshot taken). | A visible bug on the main browse page; looks broken. | Filter falsy children before `append` (or pass `''`). Audit other `append(..., cond ? x : null)` calls. | Search `zzzz`: text reads "0 matching questions" with no "null". |
| F-FUNC-02 | P2 | `viewQuestions` (`40-views-a.js` ~456–460), sidebar "All Questions" link | Explorer filters and search text persist invisibly. Opening `#/questions?tech=react` and then clicking **All Questions** (`#/questions`) still shows only React. The tech select stays "React", the page title says "All Questions", and the URL has no filter. An earlier search term (`প্যাজিনেশন`) also persisted, so a later `?tech=react` deep link showed **0 results**. | Learners land on empty or partial lists without understanding why. Blog deep links can show 0 results. | Either make the URL the single source of truth (serialise all filters into the hash), or reset filters when the nav link is clicked and show an obvious "Filters active · Clear" chip. | Set a search plus tech, click All Questions: the list shows all 584, or a visible active-filter banner. Open `?tech=react` from the blog: 32 results. |
| F-FUNC-03 | P2 | `35-i18n.js:127`, `10-data.js:141` | Bangla-script search finds nothing. The EN placeholder itself suggests **"ইনডেক্স"**, which returns 0. Also 0 for ক্লোজার, ক্যাশ, ইভেন্ট লুপ, হ্যাশ, জয়েন, প্যাজিনেশন, because content keeps terms in Latin script and search is plain substring. Latin terms work (closure 7, JWT 19, N+1 6). | Bangla-first users who type terms phonetically find nothing. The UI suggests a query that fails. | Add a small transliteration alias map (ইনডেক্স→index, ক্যাশ→cache, ক্লোজার→closure, …) applied to query terms, and change the placeholder to an example that works. | Each listed Bangla term returns the same results as its Latin form. Placeholder example returns more than 0 results. |
| F-FUNC-04 | P3 | not-found view | `#/nonsense` and `#/q/doesnotexist` give the title "Interview Prep BD · Interview Prep BD". The sidebar keeps "All Questions" as `aria-current`. There is no h1. | Minor confusion; poor a11y and SEO signals. | Title "Page not found · …", clear `aria-current`, h1 in the empty state. | — |
| F-FUNC-05 | P3 | `biText(q.question,{plain:true})` (`40-views-a.js:537`, `50-views-b.js:558`) | 49 question texts contain newlines and 39 contain bullet/numbered lists, but they are rendered as **one flattened bold heading**. Example: mongo-028 in a session renders "- The Express route runs … - mongod runs … - The app connects …" as a single 6-line bold block. 95 titles exceed 300 chars (max 646). | Scenario questions are hard to read; the requirement lists are lost. | Render a short title (first sentence) as the heading and the rest with the prose renderer. Or add a `title` field and keep `question` as the body. | mongo-028 shows a heading plus a bulleted list. |
| F-FUNC-06 | P3 | 8 questions | Generic titles become the page `<title>` and list rows: "What does this line print?" (js-001), html-006, css-002, css-023, js-005, js-017, node-016, sql-005. | Lists and tabs are indistinguishable; weak SEO. | Make titles specific ("`typeof` results for null, arrays, functions and NaN"). | No two list rows share a generic title. |
| F-FUNC-07 | P2 | MCQ rendering | Options are never shuffled, and the key is skewed to B (SYS-C03). | Answer-position bias inflates MCQ scores. | Rebalance `correctIndex` in content (≈35 per position) **and/or** shuffle per session, while keeping letters in explanations consistent. Shuffling requires rewriting explanations to refer to option text, not letters. | `correctIndex` distribution within 30–40 per position. |
| — | OK | Sessions | Start Quick Practice → reveal → grade "Partially correct" → **reload**: session resumed on the same question with grade and timer intact (`ipbd:state` v1). Direct reload of nested hash routes works. Language switch sets `<html lang="bn">` and per-block `lang`. No console errors on load (built-in validator: 584/584, 0 warnings). | — | — | — |

### Accessibility (WCAG 2.2 AA as target; compliance not claimed)

- **axe-core 4.10.2** (WCAG 2.0/2.1/2.2 A+AA rules), run on the live site in the dark theme, EN, 1024 px, found **0 violations** on 10 routes: dashboard, questions, q/js-017, q/sql-005, practice, technologies, flashcards, settings, planner and sources. Form controls have proper `<label>`s, icons are `aria-hidden`, and the toggles use `aria-pressed`.
- **F-A11Y-01 (P2):** question detail pages have **no `<h1>`**. The question text is a `<div class="q-title">`, and the first heading is h2 "Choose one answer" or "Reference answer". Screen-reader users navigating by heading cannot find the question. Fix: render the question title as `<h1>`. Test: every `#/q/<id>` has exactly one h1, which contains the question.
- **F-A11Y-02 (P3):** in Bangla mode the menu button's `aria-label` stays "Open navigation", while the theme button is translated.
- **F-A11Y-03 (P3):** the UI chrome transliterates technical words into Bangla script (ড্যাশবোর্ড, টেকনোলজি, ফ্ল্যাশকার্ড), while the content rule (AUTHORING §6) keeps them in Latin. Pick one convention. This also feeds F-FUNC-03.
- **Not tested by me:** the light theme, Bangla and Both modes, and 375 px under axe; screen-reader output; full keyboard-only flows. The README reports these as passing in its own (now unrunnable) suite.

### SEO

| ID | Sev | Observed | Impact | Fix |
|---|---|---|---|---|
| F-SEO-01 | **P1** | All 584 Q&As live only at hash routes (`#/q/js-001`) inside a 4.9 MB `questions.js`. Search engines index `/` once and never see individual questions. There are no per-question URLs, titles, descriptions or structured data. | The site's most valuable asset is invisible to organic search, which is the main way BD developers find prep material. | Pre-render a static page per question (e.g. `/q/js-001/`) or per subtopic with the same stdlib-Python approach `build_blog.py` already uses. Include the EN/BN text, a canonical, `hreflang`, `QAPage`/`Quiz`-appropriate JSON-LD that mirrors visible content, internal links and a sitemap. Keep the SPA for practice. |
| F-SEO-02 | **P1** | The live blog is fully de-indexed: all 6 pages have `<meta name="robots" content="noindex, follow">`, no canonical and no JSON-LD (0 found live). `sitemap.xml` and `robots.txt` return 404. `site.json` has `"origin": ""`. The README says this is a "preview build until a domain is configured", but `https://devshojol.github.io/Interview-prep-BD` **is** the production URL the README documents. | No page on the site can rank. | Build with `SITE_URL=https://devshojol.github.io/Interview-prep-BD` (or the chosen domain), deploy, and submit the sitemap in Search Console. |
| F-SEO-03 | P2 | `404.html` uses root-absolute paths (`/styles.css`, `/blog/blog.css`, `/blog/`, `/#/questions`, `/assets/...`). On the sub-path these resolve to `devshojol.github.io/...` and 404. The live page renders **unstyled** (screenshot taken), and every link leaves the project. | Broken first impression for any mistyped or old URL. | Generate 404 links with the configured base path (or `<base href>`), or use relative URLs. |
| F-SEO-04 | P2 | `index.html` has no canonical, `og:url`, `og:image` or Twitter card (`og-default.png` exists in `assets/brand/` but isn't referenced), and no `WebSite`/`Organization` JSON-LD. | Poor share previews on Facebook/Messenger/LinkedIn, the main discovery channels the content itself mentions (html-017). | Add them from `site.json` at build time. |
| F-SEO-05 | P3 | Generic question titles (F-FUNC-06) would become duplicate page titles once questions are pre-rendered. | — | Fix the titles before F-SEO-01. |

### Performance (measured)

- `questions.js` is 4,885,068 B raw / **1,425,534 B gzip transferred** (`curl`, `Content-Encoding: gzip`). It is loaded and parsed on **every** route, including the dashboard and the blog→app hand-off.
- `app.js` is 291,919 B raw / 84,605 B gzip. `styles.css` is 48.9 KB. Google Fonts load 3 families (4 woff2 files, ≈160 KB).
- GitHub Pages serves `cache-control: max-age=600`, so returning visitors revalidate after 10 minutes.
- Cold-load timings on slow mobile networks were **not measured**. I make no claim about specific load times. Given that the content itself argues BD users are on "mid-range Android phones with slow or unstable mobile data" (html-030), a ~1.4 MB parse-blocking script is worth measuring with WebPageTest or Lighthouse on a throttled profile.
- **Recommended direction:** split the bank per technology (18 files of about 80 KB gzip each) plus a small index (id, tech, difficulty, type, titles, tags) for search and the dashboard. Load full records on demand.
- Acceptance: the dashboard first load transfers less than 300 KB of JS, and Lighthouse mobile is measured before and after (no target number is claimed here).

### Maintainability and technical reliability

| ID | Sev | Observed | Recommendation |
|---|---|---|---|
| F-TECH-01 | P2 | `source/tests/e2e.mjs` hard-codes `file:///home/claude/interview-prep/app/index.html` and `/tmp/claude-0/e2e/node_modules/axe-core/axe.min.js`. There is no `package.json` and no CI workflow, so the claimed "103/103 passing" cannot be reproduced from the repo. | Read paths from env/relative paths, add a minimal `package.json` (playwright, axe-core), and add a GitHub Actions workflow that runs `check.py` for all techs, `node --check app.js`, `build_blog.py --check` and the e2e suite. |
| F-TECH-02 | P3 | Build requires manual copying ("then copy `app/app.js` to the repo root", "copy `app/questions.js`"). A forgotten copy deploys stale code or content. It is currently in sync (verified). | Have `build_app.sh` / `build_bank.py` write the root files directly, and add a CI check that the root files equal a fresh build. |
| F-TECH-03 | P3 | `source/tools/package.py` is documented as broken. | Fix or delete. |
| F-TECH-04 | P3 | The repo carries about 36 MB of design-agent tooling (`.agents/`, `.claude/skills/` including a `darwin-arm64` binary, `.codex/`, `.impeccable/`), committed `.DS_Store` files, and no `.gitignore`. `.claude/launch.json` contains absolute local paths, including a stale scratchpad path. (Dot-dirs are not served by Pages; I verified a 404.) | Add `.gitignore` (`.DS_Store`, local configs). Decide whether agent tooling belongs in the public repo. |
| F-TECH-05 | OK | No `innerHTML`, `insertAdjacentHTML`, `eval` or `new Function` in app or blog JS. The DOM is built through `h()`. Imports are validated (per the README; not re-tested). | — |
| F-TECH-06 | P2 | FACTS.md is the declared "source of truth" but has a single date and no re-verification process. Within 14 days it had drifted (SYS-C10). | Add a `lastVerified` per row and a monthly checklist (npm dist-tags, Node release schedule, Baseline). Show "verified on" per question in the UI (the field already exists). |

### Blog content

| ID | Sev | Item | Evidence | Fix |
|---|---|---|---|---|
| BLOG-01 | P2 | `source/content/blog/express-5-error-handling.md:25` | "The same route on Express 4 produces an `unhandledRejection` event, and the request never gets a response: the client waits until something times out." On Node ≥ 15 (`--unhandled-rejections=throw` default) with no listener, **the process crashes**. This contradicts the bank's own express-005 explanation ("on Node 15+ crashes the process"). | State that it crashes on Node 15+ and that it only hangs if an `unhandledRejection` listener swallows the error. |
| BLOG-02 | OK | `javascript-event-loop-output-questions.md` | All 4 outputs, including the CJS (`sync, nextTick, promise`) vs ESM (`sync, promise, nextTick`) order, reproduced on Node 22.18. | — |

---

## G. Prioritised remediation roadmap

Each phase lists its dependencies and measurable exit criteria. The IDs refer to sections D, F and the per-tech files.

### 1. Critical factual and functional corrections (do first; about 1–2 days)

- **NGINX-C01** (nginx-012) and **DRZ-C01** (drizzle-008): rename the content labels (responses `"A"…"E"` → `"root"`, `"images"`, `"icons"`, `"regex"`, `"exact"`; code lines A–D → ①–④ or L1–L4) and fix "The answer is D". *Exit:* no MCQ option text starts with or mentions a lone A–E letter that isn't an option reference (re-run the scan from section C).
- **MGS-C01** (mongoose-026): use `mongoose.trusted({ $regex: … })` or a `RegExp` in the fixed code.
- **NEXT-C01** (next-028): sanitise (`isomorphic-dompurify`, or render markdown on the server with a sanitiser) in the "AFTER" code.
- **SYS-C01** (50 questions): Node 24 → "Node 24 (Maintenance LTS) / Node 26 (Active LTS from 2026-10-28)". Update FACTS.md first. *Depends on:* FACTS refresh. *Exit:* `grep -c "24 LTS"` finds 0 in learner-facing text after 2026-10-28; node-022's answer matches the actual release schedule.
- **F-FUNC-01** "null", **F-SEO-03** broken 404 (small code fixes).

### 2. High-impact answer rewrites (copyable code that is wrong; about 3–4 days)

NODE-C04 (node-028 hang), REDIS-C02 (redis-008 sliding session), EXP-C02 (express-019 race), EXP-C01 (express-032 transaction claim vs code), DOCKER-C01 (docker-031 rollback), REDIS-C01 (fail-open claims vs node-redis offline queue), REDIS-C03 (RESP3 reply shape in redis-021; verify first), AWS-C03 (aws-016 secret fields), AWS-C07 (aws-023 origin restriction), HTML-C01 (html-027 Trusted Types policy names), VEC-C01 (vec-010 pgvector post-filtering), NODE-C03 (node-023 error code).

*Exit:* each fixed snippet is executed (or, for services not available locally, run in Docker in CI) and the run output is stored alongside the question's source batch.

### 3. Conceptual precision fixes (P2 text errors; about 1–2 days)

JS-C01 (js-026), JS-C02 (js-027), SQL-C01 (sql-002 `USING` vs `NATURAL`), MONGO-C01 (mongo-022 `moderate`), MGS-C05 (mongoose-032), DOCKER-C03 (docker-019 10-second rule), HTML-C02 (html-024 `role=alert`), NGINX-C02 (nginx-009 `curl -I`), CSS-C01 (css-028 anchor positioning; verify on webstatus.dev first), BLOG-01.

### 4. Bilingual consistency and language

- MONGO-C03 (mongo-014: "একটাই" → "একই"), plus the BN P3 items in each file: e.g. "অনাথ order" (sql-019), a Bangla word inside a code expression (sql-030), the broken sentence in nginx-003, and the dropped "Pages Router is legacy" caveat in one Next.js BN answer.
- SYS-C06: replace লোভনীয় / প্রলোভনজনক / আকর্ষণীয় ফাঁদ with natural phrasing, e.g. "সবচেয়ে বেশি মানুষ যে ভুল option-টা বেছে নেয়" or "ভুল হলেও সঠিক মনে হওয়া option".
- F-A11Y-02 and F-A11Y-03: one terminology convention for UI chrome vs content.
- *Exit:* a native Bangladeshi developer proofreads one full category end to end and signs off. The README's open "not proofread by a native-speaker editor" limitation is closed.

### 5. Examples, edge cases, MCQ mechanics

- SYS-C02: add 1–2 follow-ups to all 114 MCQs that lack them.
- SYS-C03 / F-FUNC-07: rebalance the key positions.
- SYS-C04: replace option numbers with letters.
- SYS-C07: remove authoring notes, "(Advanced…)" openers and "interviewers love" filler.
- *Exit:* 0 MCQs without follow-ups; `correctIndex` 30–40 per position; 0 matches for `Verified (on|with)`, `^\(Advanced`, `interviewers love`.

### 6. Coverage and learning structure

- Add the questions in section E (about 25–35 new items across categories), prioritising junior impact: JS TDZ / `call`-`apply`-`bind` / DOM; CSS display/centering/units; React security / `useReducer`; Next `<Link>`; Mongo change streams / `arrayFilters`; Nest TypeORM/Prisma; SQL set operations; AWS Auto Scaling; NGINX redirects; Docker debugging toolkit.
- Trim or merge the redundant sets (SYS-C09). Prefer cross-links (`related`) over re-explaining.
- Fix the difficulty labels flagged in section E.
- *Exit:* `check.py` OK; each new question passes the AUTHORING checklist and its code is executed; the redundancy pairs listed in section E are resolved or intentionally cross-linked.

### 7. Functional, accessibility and SEO

- **SEO architecture** (F-SEO-01/02/04/05): production blog build, pre-rendered question pages, sitemap. *Depends on:* the F-FUNC-06 title fixes.
- F-FUNC-02 (URL-driven filters), F-FUNC-03 (Bangla search aliases), F-FUNC-05 (question title/body split), F-A11Y-01 (h1).
- Performance split of `questions.js`.
- F-TECH-01/02 (runnable tests plus CI that guards root-file sync).

### 8. Lower-priority polish

The remaining ~190 P3 items in `audit/content/*.md`, F-FUNC-04, F-TECH-03/04, and market-label clean-up (SYS-C08).

---

## H. Content rewrite specifications

These are the patterns to apply when fixing. They are drawn from the bank's own best answers, so the target quality already exists in the repo.

**H1. MCQ explanation template** (applies to all 140 MCQs)

- **Answer:** name the correct option **by letter and by its content** ("**B**: the regex location wins"). Never refer to a letter used inside the question content.
- **Explanation:** the mechanism in 2–4 steps, then why the most tempting wrong option is wrong. Refer to it as "option A (`/images/` longest prefix)", never "Option 1".
- **Follow-ups:** 1–2 that test transfer ("What changes if `/images/` were `^~`?").
- **Research:** none beyond the existing explanation, except where the per-tech file says "needs verification".
- **Model example already in the bank:** js-001 (letter references are consistent, and the trap is explained).

**H2. "Fixed / recommended code" in debugging and security questions**

- The fixed code must be safe to copy as is. No "sanitise here" comments: actually call the sanitiser, close the handle, or use the atomic update.
- State the failure mode the fix prevents and one remaining limitation.
- Execute it. If the service isn't available locally, run it with Testcontainers or Docker in CI, and record "Verified on <version>" in the **source batch metadata**, not in learner text (SYS-C07).
- **Model examples:** pg-023 (conditional UPDATE re-check) and express-005 (forwarding plus what Express 5 still can't catch).

**H3. Version-sensitive statements**

- Phrase them as "As of <date>, Node 26 is Active LTS; Node 24 is in Maintenance until <date>" and put the date in `technologyVersion`.
- Prefer version-independent phrasing in answers ("use the current Active LTS") and keep the specific number in the metadata label.
- **Research:** nodejs.org release schedule; npm dist-tags for `@nestjs/core`, `drizzle-orm`, `mongoose`, `express`; webstatus.dev for Baseline. Do not invent dates: if a date can't be confirmed, say "planned".

**H4. Long scenario questions**

- Split into `title` (≤ 120 chars, specific) and `body` (the context bullets), so the UI can render a heading plus a list (F-FUNC-05).
- **Example:** mongo-028 becomes the title "Harden a login API and a MongoDB deployment that are open to the internet", with the body holding the three current bullet points.

**H5. Bangla phrasing**

- Keep the existing conventions (Latin-script terms with hyphenated suffixes, তুমি-form tips).
- Avoid literal calques of English idioms ("tempting answer", "cold cache" → "ঠান্ডা cache"). Write how a Dhaka developer would say it aloud: "cache তখনো খালি (cold cache)".
- Every caveat in EN must appear in BN. Check with a side-by-side pass for "only / except / unless / legacy / deprecated / not Baseline".

**H6. New questions** (for section E gaps)

- Follow AUTHORING.md exactly.
- One concept per question. Code executed. 1–3 official references. Market `both` unless there is evidence for another label.
- No claims about which companies ask it.

---

## I. Final acceptance checklist

**Content correctness**

- [ ] NGINX-C01 and MGS-C01 (P1) fixed and re-reviewed.
- [ ] All 33 P2 content items in section D fixed, or explicitly rejected with a reason recorded.
- [ ] Every "fixed/recommended" snippet in debugging/security questions executed, with output recorded in source metadata.
- [ ] FACTS.md refreshed (Node 24/26 LTS, NestJS 12.2, Drizzle rc tag, anchor positioning Baseline), with per-row `lastVerified`.
- [ ] 0 learner-facing occurrences of "Node.js 24 LTS" as the current recommendation after 2026-10-28.
- [ ] All "Needs verification" items in `audit/content/*.md` resolved (verified with a source URL, or rephrased version-independently).

**MCQs**

- [ ] 0 option references by number; 0 A–E label collisions (scan script re-run).
- [ ] `correctIndex` distribution 30–40 per position (or per-session shuffle, with explanations not relying on letters).
- [ ] Every MCQ has at least 1 follow-up.

**Bilingual parity**

- [ ] mongo-014 and the other BN P3 items fixed; 0 occurrences of লোভনীয় / প্রলোভনজনক / আকর্ষণীয় ফাঁদ.
- [ ] A native-speaker proofread of at least one category, signed off.
- [ ] UI chrome uses the same terminology convention as content; all `aria-label`s translated.

**Question quality and coverage**

- [ ] Gap questions from section E added (`check.py` OK; distribution still on target, or the target documented as changed).
- [ ] Redundant clusters (SYS-C09) merged or cross-linked; difficulty mislabels fixed.
- [ ] 0 generic titles; no title over 120 chars once title and body are split.
- [ ] 0 authoring notes or filler phrases (SYS-C07 grep).

**Functionality**

- [ ] The "null" bug is gone; Bangla-script searches for the listed terms return results; filters are reflected in the URL or visibly indicated.
- [ ] Multi-line questions render as a heading plus a list.
- [ ] Session resume, MCQ lock, export/import and reset still pass (e2e).

**Accessibility**

- [ ] Every `#/q/<id>` has exactly one h1.
- [ ] axe-core 0 serious/critical violations in both themes × EN/BN/Both × 375/1280 px.

**SEO**

- [ ] Production blog build: indexable pages, canonical, JSON-LD, `sitemap.xml`; robots/sitemap submitted.
- [ ] 404 page styled, with working links on the sub-path.
- [ ] Per-question (or per-subtopic) static pages with unique titles and descriptions, linked from the sitemap.
- [ ] `index.html` has canonical, `og:url`, `og:image` and a Twitter card.

**Build and CI**

- [ ] e2e runnable from the repo (`npm test` or equivalent) and passing in CI.
- [ ] CI fails if root `app.js`/`questions.js` differ from a fresh build, or if `check.py` fails for any tech.
- [ ] Performance: the bank is split; dashboard JS transfer is measured before and after (target agreed by the owner).

---

## J. Audit coverage statement

| Area | Inspected | How |
|---|---|---|
| Questions | **584 / 584** (all 18 techs), every field (question, answer, explanation, mistakes, tip, follow-ups, options, code, setup, output, extra code, references) in **EN and BN** | 10 specialist reviewers, one per tech group, each confirming every ID (verified programmatically: every ID appears in each file's per-question notes) |
| Code executed | All JS/Node output and coding questions (Node 22.18; ES2026 Map upsert polyfilled); all portable SQL query questions plus pg-017/pg-022 (sqlite3 3.51); vector maths (Python); RRF and chunker (Node); path-to-regexp 8.3 route syntax; zod 4; the next-009 number parsing; the node-023 stream error | per-tech "Verified" sections |
| Traced, not executed | PostgreSQL-specific behaviour, MongoDB/Mongoose, Redis, NGINX, Docker, AWS, NestJS, Drizzle, Express 5 runtime | reasoning plus about 50 targeted official-doc and npm checks (URLs in the per-tech files) |
| App source | All 10 files in `source/app/src/` (router, search, rendering and filters read in detail; the rest skimmed for unsafe DOM APIs); `index.html`; `404.html`; build scripts (read headers); docs (AUTHORING, FACTS, COVERAGE, REVIEW, README) | read |
| Routes tested live | All 17 hash routes plus the not-found fallback (render and title check); interactive tests: search (25 queries EN/BN), filters and nav persistence, question detail, MCQ view, practice session start/reveal/grade/reload-resume, language switch, theme labels, mobile 375 px question page, blog article and links, 404 | in-app browser on the production URL |
| Accessibility | axe-core on 10 routes (dark, EN, 1024 px); heading structure; label association; `aria-pressed` | live |
| SEO | All 7 HTML entry points' meta tags; robots/sitemap/canonical/JSON-LD presence | `curl` plus live DOM |
| Live vs repo | 9 files byte-compared | `curl` + `cmp` |
| Blog | 5 / 5 articles: event-loop article fully verified by execution; the other 4 read for structure and key claims (code not executed) | — |

**Not inspected, or only partly:**

- The bundled e2e suite was not run (environment-specific paths; no dependency installs during the audit).
- Light-theme, Bangla and 375 px axe runs were not done.
- No screen-reader testing.
- No cold-load performance or Lighthouse measurement.
- The planner, heatmap, export/import and reset flows were not exercised by hand.
- The flashcards and daily challenge were only render-checked.
- Not all 853 reference URLs were fetched: references were judged for officialness and relevance, with spot checks only.
- The `.agents/` and `.claude/skills/` tooling was not audited (not part of the product).
