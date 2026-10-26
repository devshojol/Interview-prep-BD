# JavaScript content audit

Coverage: all 40 question IDs in dumps/javascript.md were reviewed: js-001, js-002, js-003, js-004, js-005, js-006, js-007, js-008, js-009, js-010, js-011, js-012, js-013, js-014, js-015, js-016, js-017, js-018, js-019, js-020, js-021, js-022, js-023, js-024, js-025, js-026, js-027, js-028, js-029, js-030, js-031, js-032, js-033, js-034, js-035, js-036, js-037, js-038, js-039 and js-040. **Count: 40/40.**

## Category summary
This is a very strong set. Every expected output I could execute matched exactly: 19 output, MCQ and debugging questions were run in Node 22.18, and js-035 was run with a polyfill. All coding solutions were run against their stated examples and extra edge cases (debounce `this`/cancel, throttle, promiseAll, memoize/curry, retry with abort, the promise pool with fail-fast/abort/empty input/limit<1, deepClone, the store, safeMerge, and the V8 `%HaveSameMap`/`%HasFastProperties` claims), and all of them behaved as described.

No MCQ has a wrong key, and no shown code leaks its answer in comments. The explanations consistently cover the "why", the traps, the trade-offs and production context such as cancellation, idempotency, cleanup and support status. Difficulty rises sensibly from typeof/hoisting up to V8 shapes.

Weaknesses are few, all P2/P3:
- One misleading mechanism: js-026 says the CommonJS "copy" happens when you destructure. It actually happens when `module.exports = { count }` runs.
- One wrong distractor rationale in js-027 (option C).
- A slightly stale Baseline label for `AbortSignal.timeout` in js-033.
- Minor oversimplifications (js-018, js-034).
- Illustrative code in js-032 that is a SyntaxError as an ES module.
- An "(Advanced…)" template prefix on the extreme answers.
- Some redundancy: there are three event-loop output-ordering questions.

The Bangla is natural, contemporary Bangladeshi developer register with tech terms in Latin script, and it is consistently complete relative to the English. I found only a couple of slightly literal phrases. Version claims mostly match FACTS.md and the MDN/BCD data I checked (Error.isError, Math.sumPrecise and the Map upsert Baseline date were all confirmed).

Coverage gaps: there is no dedicated var/let/const + TDZ question (FACTS research names this as the top BD topic), no `call`/`apply`/`bind` implementation question, and no easy/medium DOM-manipulation question.

Scores:
| Dimension | Score |
|---|---|
| Technical accuracy | 9 |
| Explanation depth | 9 |
| Interview usefulness | 9 |
| Bangla quality | 9 |
| English quality | 9 |
| Examples & code | 9 |
| Originality/information value | 9 |
| Structural clarity | 9 |

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| JS-C01 | js-026 | both | P2 | Technical accuracy (misleading mechanism) | The text says the CJS value is copied at destructuring time. The copy actually happens when the exporter builds `module.exports = { count, … }`, so even `require('./counter.cjs').count` stays `0` without any destructuring. Learners will wrongly conclude that "don't destructure" fixes it. | "CommonJS copies whatever is on `module.exports` when you destructure it"; "CommonJS prints `0` because destructuring copied the number"; BN "CommonJS-এ destructure করলে সেই মুহূর্তে `module.exports`-এ যা আছে তার copy পাও" | Say: "`module.exports = { count }` stores the current value of `count` (0) in a property. Later `count++` changes the local variable, not the exported property, so every importer sees 0 whether or not it destructures. ESM imports are live bindings to the variable itself." Optionally mention exposing a getter (`get count() { return count; }`). | High | Ran counter.cjs/main.cjs: destructured → `0`, `m.count` without destructuring → `0`; ESM → `1`. |
| JS-C02 | js-027 | both | P2 | MCQ distractor rationale wrong | `[1, 4, 9]` is the result of ignoring `filter` (squares of 1, 2, 3). If `take(3)` ran before `filter`, the result would be `[4]`. | "**Option C** assumes `take` runs before `filter`; the chain order is respected." BN "Option C ধরে নেয় `take` `filter`-এর আগে চলে" | "Option C forgets the `filter` step (it squares 1, 2, 3). Note that even if `take` ran first you would get `[4]`; the chain runs in the written order, one value at a time." | High | Manual trace; ran the code → `[ 4, 16, 36 ]`. |
| JS-C03 | js-033 | both | P3 | Version/status | `AbortSignal.timeout` is labelled "Baseline newly available". Per MDN it is **Widely available** (Chrome 124 completed support in April 2024; Firefox 100, Safari 16, Node 17.3). The header `ver` repeats the label. | "`AbortSignal.timeout` is Baseline newly available" (EN + BN, and ver line) | Change to "Baseline widely available". `AbortSignal.any` (Safari 17.4, March 2024) is also widely available now, as the text already says. | High | MDN timeout_static page ("Widely available"); BCD AbortSignal.json. |
| JS-C04 | js-032 | EN (code) | P3 | Code correctness (illustrative) | The single code block declares `function mountTicketPanel` twice ("Leaky" and "Fixed"). As an ES module (the app's default mental model elsewhere) this is a `SyntaxError: Identifier 'mountTicketPanel' has already been declared`. As a sloppy script, the second declaration silently wins. | `function mountTicketPanel(el, store) {` … `function mountTicketPanel(el, store) {` | Rename to `mountTicketPanelLeaky` / `mountTicketPanel`, or move the fixed version into an `extra` block. | High | `node --check js-032.mjs` → SyntaxError; `.cjs` → OK. |
| JS-C05 | js-018 | both | P3 | Oversimplification | "Writing a property always creates/updates an own property" is false when an inherited setter or a non-writable inherited property exists. This is relevant at medium level because classes use getters/setters. | "Writing a property always creates/updates an **own** property." BN "property লিখলে সবসময় **নিজস্ব** property তৈরি/update হয়" | "…usually creates/updates an own property (unless an inherited setter or a read-only inherited property intercepts the write)." | High | Spec [[Set]] / OrdinarySet. |
| JS-C06 | js-034 | both | P3 | Overstatement | For the finite list shown, the microtask queue does empty, but only after all the work is done. "Never empties" / "identical to `while (true)`" is only true for unbounded recursion. | "the queue never empties. The result is identical to a `while (true)` loop" | "…the queue doesn't empty until the whole job is finished, so the effect is the same as one long synchronous loop: no paint, no input, no timers until it's done (forever if the recursion is unbounded)." | High | Reasoning from the HTML event loop. |
| JS-C07 | js-023 | both | P3 | MCQ explanation clarity | The option C rationale is confusing: callbacks don't "return nothing" here. `resolved: undefined` would require `fetchUser` to fulfil with `undefined`. | "**Option C** would need the callback to return nothing; here the rejection propagates instead." | "Option C would need `fetchUser` to fulfil with `undefined`; it rejects, so the `.then` callback never runs." | High | Ran code → `rejected: User 7 not found`. |
| JS-C08 | js-009 | both | P3 | Terminology | `address: { city }` is **nested destructuring**, not renaming. Renaming is `id: userId`. The code comment also says "rename via nesting". | "renaming (`address: { city }`, `id: userId`)"; code "// Object destructuring: rename via nesting, default, rest" | "renaming (`id: userId`), nesting (`address: { city }`)…"; comment: "nested pattern, default, rest". | High | Language spec / MDN Destructuring. |
| JS-C09 | js-022 | both | P3 | Code accuracy in prose | The ES2026 one-liner drops the `this` forwarding that the question requires and has no LRU behaviour. It is presented as replacing the implementation without that caveat. | "`cache.getOrInsertComputed(key, () => fn(...args))` … replaces the `has`/`get`/`set` dance for simple caches" | Add: "(for an unbounded cache; use `fn.apply(this, args)` and keep the delete/re-insert step if you need LRU)". | High | Comparison with the solution code. |
| JS-C10 | js-016 | both | P3 | English/BN wording | "Not before the next task" is an awkward, almost inverted phrasing; the BN mirrors it. | "`setTimeout(fn, 0)` means "not before the next task", not "immediately""; BN "মানে "পরের task-এর আগে নয়", "এখনই" নয়" | "`setTimeout(fn, 0)` means "run in a later task, after the current script and all microtasks", not "immediately"." BN: "মানে "পরের কোনো task-এ, বর্তমান script আর সব microtask শেষ হওয়ার পরে", "এখনই" নয়।" | High | n/a |
| JS-C11 | js-020 | both | P3 | Question ambiguity | The example says `fn` runs "300 ms after the last call" but never states `wait = 300`. | "→ `fn` runs **once**, 300 ms after the last call" | "With `wait = 300`, a search box calls…" | High | n/a |
| JS-C12 | js-037, js-038, js-039, js-040 | both | P3 | Template filler | The answers start with a meta label that a candidate would never say aloud and that adds no information. | "(Advanced.) I use…", "(Advanced design question.)", "(Advanced scenario.)", "(Advanced — engine internals; profile before acting on any of this.)"; BN "(Advanced বিষয়।)" | Remove the parenthetical labels (difficulty is already in metadata). Keep "profile before acting" as a real sentence in js-040. | High | grep: 8 occurrences. |
| JS-C13 | js-016, js-017, js-029 | both | P3 | Redundancy | There are three output-ordering event-loop questions (sync → microtasks → `setTimeout`), plus js-034. js-016 and js-029 test largely the same rule (js-029 adds nested timers). | js-016 `A E G C D F B`; js-029 `S1 S2 M1 M3 A1 M2 T1…`; js-017 `script start … timeout` | Keep js-016 (medium) and js-029 (hard). Re-scope js-017 to `return` vs `return await` / thenable tick counts, or swap it for a `process.nextTick`/`setImmediate` Node ordering question. | Medium | n/a |
| JS-C14 | js-001, js-002, js-005, js-008 | meta | P3 | market label | These universal fundamentals are tagged `market=bangladesh`. They are equally asked internationally, and the label may hide them from an "international" filter. FACTS research supports their importance for BD, but not exclusivity. | `market=bangladesh` | Use `market=both`. | Medium | FACTS.md research notes. |
| JS-C15 | js-035 (also js-026 ver line) | both | P3 | Version currency (soon stale) | The text frames Node 24 as "the LTS" without the upsert feature. Node 24 moved to Maintenance on 2026-10-20, and Node 26 becomes LTS on 2026-10-28, so after that date upsert *is* available in the current LTS. | "It's in Node.js 26 but **not** Node.js 24 LTS"; ver "Node.js 24 LTS / 26" | "Available in Node.js 26 (LTS from 2026-10-28); not in Node.js 24 (Maintenance LTS) or 22." Update the `ver` strings. | High | FACTS.md Node row. |
| JS-C16 | js-022 | BN | P3 | Bangla phrasing | The LRU translation is literal and awkward. | "**সবচেয়ে কম সম্প্রতি ব্যবহৃত** (LRU) entry বাদ দেবে" | "যে entry সবচেয়ে বেশি সময় ধরে ব্যবহার হয়নি (least recently used, LRU), সেটা বাদ দেবে" | Medium | n/a |
| JS-C17 | js-026 | both | P3 | Missing current Node detail | The module-type rules omit Node's ESM syntax detection: since 22.7 a `.js` file with no `"type"` field that contains ESM syntax is run as ESM. That is relevant to "practical differences in Node.js today". | "a file is ESM if it's `.mjs` or the nearest `package.json` has `"type": "module"`" | Add: "…and since Node 22.7, an ambiguous `.js` file with ESM syntax is detected as ESM (with a warning/perf cost); set `"type"` explicitly." | Medium | Node docs (packages: syntax detection); not fetched. |
| JS-C18 | (category) | n/a | P3 | Coverage gap | (a) There is no dedicated var/let/const scope + TDZ question, although FACTS research lists it first for BD. (b) There is no `call`/`apply`/`bind` question; "implement `bind`" is a very common written test. (c) DOM manipulation appears only as an extreme scenario, with no easy/medium question (querySelector, createElement/DocumentFragment, textContent vs innerHTML, classList, dataset). | — | Add 1–3 questions, or re-scope a redundant event-loop question (JS-C13). | Medium | COVERAGE.md vs IDs. |

## Per-question notes
- js-001 — OK (output verified). acc 10 / depth 8 / BN 9 / EN 9. Label: JS-C14.
- js-002 — issues: JS-C14; scores acc/depth/BN/EN 10/9/9/9 (output verified).
- js-003 — OK (output + IIFE extra verified).
- js-004 — OK (counter outputs 7/undefined/0 verified).
- js-005 — issues: JS-C14; scores 10/9/9/9 (output verified).
- js-006 — OK (ran in ESM and CJS: regular callback → `undefined`, arrow → team; `typeof this` undefined in ESM, object in CJS, matching the comments).
- js-007 — OK (output verified; key correct).
- js-008 — issues: JS-C14; scores 10/9/9/9 (all examples incl. emoji and the anagram extra verified).
- js-009 — issues: JS-C08; scores 9/9/9/9 (outputs verified).
- js-010 — OK.
- js-011 — OK (key C correct).
- js-012 — OK (reduce + Object.groupBy/Map.groupBy verified; "Node 21+" correct).
- js-013 — OK (output `undefined` and fixed version 3800/0 verified; `'[object Object]800'` reasoning correct).
- js-014 — OK (output verified).
- js-015 — OK (ESM output verified).
- js-016 — issues: JS-C10, JS-C13; scores 10/9/9/8.
- js-017 — issues: JS-C13; scores 10/9/9/9 (output verified; the option C "Node 10, three ticks" history is correct by trace).
- js-018 — issues: JS-C05; scores 9/9/9/9 (output verified).
- js-019 — OK (output verified; the Error.isError support claims match BCD exactly).
- js-020 — issues: JS-C11; scores 10/9/9/9 (debounce latest-args, `this` forwarding, cancel and throttle leading+trailing verified by run).
- js-021 — OK (outputs `[]`, `boom`, `['a',42,'c']` verified).
- js-022 — issues: JS-C09, JS-C16; scores 9/9/8/9 (memoize `80 80 1`, fib(50), curry `6 6 6` verified).
- js-023 — issues: JS-C07; scores 10/9/9/9 (output verified; ESLint/typescript-eslint claims correct).
- js-024 — OK.
- js-025 — OK.
- js-026 — issues: JS-C01, JS-C15, JS-C17; scores 8/8/9/9.
- js-027 — issues: JS-C02; scores 9/8/9/9 (output verified).
- js-028 — OK (output verified).
- js-029 — issues: JS-C13 (kept as the hard variant); scores 10/10/9/9 (output verified).
- js-030 — OK (vulnerable output `dark true` and safeMerge `dark undefined` verified).
- js-031 — OK (Sanitizer/Trusted Types status in Needs verification).
- js-032 — issues: JS-C04; scores 9/9/9/9.
- js-033 — issues: JS-C03; scores 9/10/9/9 (retry/backoff, non-retryable stop and abort during sleep verified).
- js-034 — issues: JS-C06; scores 9/9/9/9.
- js-035 — issues: JS-C15; scores 10/9/9/9 (logic verified with a spec-shaped polyfill → `3 2 2`; Baseline Feb 2026 confirmed).
- js-036 — OK (`true 5 true` / `false` verified).
- js-037 — issues: JS-C12; scores 10/10/9/9 (max in-flight = limit, ordered results, fail-fast stops new starts, abort, empty input, RangeError verified).
- js-038 — issues: JS-C12; scores 10/10/9/9 (`cart: 0 -> 2` single batched log verified).
- js-039 — issues: JS-C12; scores 9/10/9/9.
- js-040 — issues: JS-C12; scores 10/9/9/9 (`%HaveSameMap` true and `%HasFastProperties` false after delete verified).

## Coverage & gaps
- Every COVERAGE.md subtopic is touched: variables/types, scope/hoisting, closures, `this`, arrows, prototypes, objects/arrays, copies, destructuring, array methods, promises, async/await, event loop, call stack/execution contexts/lexical environments, modules, errors, debounce/throttle, delegation, DOM manipulation (js-039), memory/GC, immutability, FP, ESM vs CJS, performance, XSS, prototype pollution, plenty of output and coding questions, and ES2025/26.
- Gaps (JS-C18): a dedicated var/let/const + TDZ question; a `call`/`apply`/`bind` (implement `bind`) question; an easy/medium DOM manipulation question. Optional: `null` vs `undefined` (currently only a follow-up) and generators basics.
- Redundancy (JS-C13): js-016 / js-017 / js-029 overlap. This is acceptable as a difficulty ladder, but js-017 could be re-scoped.
- Difficulty labels look right throughout. js-012 groupBy as "easy coding" is fine. js-038 is labelled extreme/architecture, which is appropriate.

## Needs verification
- js-031: "Trusted Types … Baseline newly available in February 2026" (consistent with the FACTS `ver` string; not fetched). "HTML Sanitizer API (`element.setHTML()`) ships in Chromium and Firefox but is not Baseline."
- js-034: "`scheduler.yield()` … Chromium 129+, Firefox 142+, no Safari"; "`requestIdleCallback` … isn't available in Safari".
- js-035: exact versions "Chrome 145, Firefox 144, Safari 26.2" for Map upsert (the Baseline Feb 2026 date itself is verified). "It's in Node.js 26". "`Uint8Array.fromBase64()`… Baseline since September 2025, Node.js 26". "`Iterator.concat()` (Baseline 2026-03)".
- js-022: "Map upsert, Baseline 2026 / Node 26" (same as js-035).
- js-027: "Chrome 122, Firefox 131, Safari 18.4" for iterator helpers (consistent with my knowledge; not fetched).
- js-039: "`content-visibility` Baseline newly available" (believed correct: Safari 18, Sept 2024).

## Verified
- Node v22.18.0. I extracted every `code.source` and `extra` from bank.json into SCRATCH/run/js/*.mjs.
- Expected output matched exactly for js-001, 002, 003, 005, 007, 013, 014, 015, 016, 017, 018, 019, 023, 027, 028, 029 and 030.
- Ran without expected output and confirmed the comments: js-004, 006 (ESM + CJS), 008 (+ anagram extra), 009, 012, 021, 022 (+ curry extra), 036 and 038.
- js-003 extra (IIFE) → 0 1 2. js-013 extra → 3800, 0. js-030 safeMerge extra → `dark undefined`.
- js-020: debounce fires once with the latest args, forwards `this` (`this.n= obj`), `cancel()` prevents firing; throttle gives a leading call then roughly one call per 100 ms with the latest args.
- js-026: multi-file test. ESM live binding → 1; CJS destructured → 0; CJS non-destructured `m.count` → 0 (basis for JS-C01); `require('./counter.mjs')` works in Node 22.18.
- js-032: `node --check` as .mjs → SyntaxError (duplicate declaration); as .cjs → OK.
- js-033: retry with mock task (2 retries then success); a 400 is not retried; aborting during a 1 s backoff rejects after about 50 ms with the abort reason.
- js-035: polyfilled `getOrInsert`/`getOrInsertComputed` → `3 2 2`. Node 22 lacks the upsert methods, `Math.sumPrecise`, `Error.isError`, `Uint8Array.fromBase64` and `Iterator.concat` (as expected).
- js-037: 20 mock tasks with limit 5 → max in flight 5 and ordered results. Failure at index 6 with limit 3 → rejects with "fail 6" and no new tasks start afterwards. Abort → AbortError. `[]` → `[]`. Limit 0 → RangeError.
- js-040: `node --allow-natives-syntax` → `%HaveSameMap(toOrder(a), toOrder(b))` true; `%HasFastProperties` after delete → false; toOrderSlow with and without coupon → different maps.
- Fetched (6):
  - MDN Error.isError → Limited availability.
  - BCD `javascript/builtins/Error.json` → isError Chrome 134, Firefox 138, Safari 18.4 partial (DOMException false), Node 24.3.0 full (24.0–24.3 partial). This matches js-019 exactly.
  - MDN AbortSignal.timeout → "Widely available" (basis for JS-C03).
  - BCD `api/AbortSignal.json` → any: Chrome 116, Firefox 124, Safari 17.4, Node 20.3; timeout: Chrome 124 (partial 103–123), Firefox 100, Safari 16, Node 17.3.
  - MDN Map.getOrInsert → "Baseline 2026 · Newly available since February 2026" (matches js-035).
  - BCD Math.json → sumPrecise Chrome 147, Firefox 137, Safari 26.2, Node false. This matches "Baseline since April 2026; not yet in Node.js 26".
