# Node.js content audit

Coverage: all 32 IDs in dumps/nodejs.md reviewed — node-001, node-002, node-003, node-004, node-005, node-006, node-007, node-008, node-009, node-010, node-011, node-012, node-013, node-014, node-015, node-016, node-017, node-018, node-019, node-020, node-021, node-022, node-023, node-024, node-025, node-026, node-027, node-028, node-029, node-030, node-031, node-032 (count: 32).

## Category summary
This is a strong set. The answers are technically precise and current, and they explain mechanisms rather than giving dictionary definitions. They usually say why something happens, and most questions include a "what doesn't work" angle. I ran every output and event-loop question on Node 22.18 (node-002, -004, -013, -021, plus the ESM twist) and all printed exactly the expected output. The runnable coding answers (node-011, -028, -031) and the MCQs node-012, -016 and -019 also behaved as claimed.

I found no wrong MCQ keys, no wrong outputs and no answer leaks in the shown code. Most of the problems are small:
- One debugging premise names the wrong symptom (node-023).
- One coding solution can still hang, despite its "never hang" requirement (node-028).
- Some release-calendar text is going stale (node-022).
- A few minor inconsistencies and some Bangla literalisms.

The Bangla is natural, contemporary developer Bangla with tech terms in Latin script. It keeps the same caveats as the English almost everywhere. A few calques recur, such as "প্রলোভনের ভুল উত্তর" and "memory বিস্ফোরিত হয়".

On versions, the claims I could check against official docs are correct:
- require(esm) "no longer experimental" in v25.4
- `--env-file` stable in v24.10 / v22.21
- `--allow-net` added in v25
- type stripping stable in v25.2 / v24.12
- `--experimental-transform-types` removed in v26

The framing "Node 24 LTS" is now dated: v24 entered Maintenance on 2026-10-20, and v26 becomes LTS on 2026-10-28. Coverage of COVERAGE.md is nearly complete. Gaps are a dedicated `uncaughtException`/process-lifecycle question and a hands-on `node:test` question. Redundancy is mild and intentional: node-020 and node-028 (shutdown), node-006 and node-018 (blocking), node-017 and node-026 (cluster).

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| NODE-C01 | node-022 | both | P2 | Version currency | The release-calendar answer is now stale. Per FACTS, v24 went to Maintenance on 2026-10-20 and v26 becomes Active LTS on 2026-10-28. Today (2026-10-26) v24 is no longer "Active LTS". The question says only "It is October 2026", so the key depends on which day. | "As of 12 October 2026, v24 is Active LTS, and v26 is still Current until it is promoted to LTS on 28 October 2026" / Option B "Node.js 24 — the Active LTS line" | Pin the question to a date ("On 12 October 2026…"). Or reword option B to "the newest LTS line (v24 now, v26 from 28 Oct 2026)". Add a review date, because status=version-specific. | High | The question carries an explicit date, and the key stays correct for the whole of October 2026. |
| NODE-C02 | node-003, node-010, node-015, node-025 (also ver headers of most Node items) | both | P3 | Version currency | "Node.js 24 LTS" is used as the current recommended line. It will be outdated after 2026-10-28. | node-003 "In a new Node.js 24 LTS project"; node-015 "in a Node.js 24 application"; node-010 "`node:24-…`"; node-025 "Seat belt for trusted code (Node 24 / 26)" | Use "current LTS (v24/v26)" or "Node 22.12+/24+" wording. The concepts are version-independent anyway. | High | No sentence implies v24 is the newest LTS after 28 Oct 2026. |
| NODE-C03 | node-023 | both | P2 | Technical correctness (debugging premise) | The scenario names "write after end" as a symptom. After a client disconnects, `res.write()` on the destroyed response fails with `ERR_STREAM_DESTROYED`, reported via the write callback, and no `'error'` event is emitted. `ERR_STREAM_WRITE_AFTER_END` only happens after `res.end()`, which this code never calls. | Q: "occasional "write after end" errors"; A: "writes to a closed response — the "write after end" errors" | Change the symptom to "`ERR_STREAM_DESTROYED` / writes to destroyed sockets (`write()` returns false)", or say "write-after-close errors". Keep the rest. | Medium-High (verified with node:http on Node 22; Express `res` is the same object) | Run the SSE repro: a client disconnects, then `res.write` callback receives `ERR_STREAM_DESTROYED`. |
| NODE-C04 | node-028 | both | P2 | Code correctness vs requirement | The solution clears the safety-net timer in `finally` and then relies on `process.exitCode`. If any handle stays open after `closeResources()` (a Redis client not quit, a non-unref'd interval, a keep-alive outbound socket), the process hangs forever. That breaks the stated requirement "never hang longer than 10 seconds". The force timer is already `unref()`'d, so clearing it gains nothing. node-020 uses `process.exit(0)` instead, so the two answers give conflicting advice. | "finally { clearTimeout(forceTimer); }" and Q: "never hang longer than 10 seconds in total" | Don't clear the unref'd force timer. Or call `process.exit(process.exitCode)` after cleanup and a log flush. Explain the choice and align node-020 with node-028. | High (logic) | Add `setInterval(()=>{},1000)` (not unref'd) as a "leaked handle". The process must still exit in 10 s or less. |
| NODE-C05 | node-019 | both | P3 | Internal inconsistency / ref | The question says the server is 8-core, but the explanation says "six hashes on four cores still contend". One reference title is irrelevant: `UV_THREADPOOL_SIZE` is linked as "Command-line options (--env-file)". | "six hashes on four cores still contend for CPU"; ref title "Node.js API — Command-line options (--env-file)" | Reword: "a pool larger than your free cores doesn't speed up CPU-bound work". Retitle the ref "Command-line options (UV_THREADPOOL_SIZE)". | High | The text matches the 8-core premise. |
| NODE-C06 | node-007 | both | P3 | Overstatement | The idempotency check (`alreadySent` → send → `markSent`) still sends a duplicate if the worker crashes between send and mark. The answer says "A retried job then becomes a no-op". | "A retried job then becomes a no-op." | Add: "the window between send and mark remains; pass an idempotency key to the email provider, or accept rare duplicates". | High | The answer mentions the send/mark crash window. |
| NODE-C07 | node-020 | both | P3 | Clarity | It says "four things" but then lists five numbered items. | "Zero downtime needs four things to line up" … items 1–5 | Say "five things" or merge item 5. | High | The count matches the list. |
| NODE-C08 | node-032 | both | P3 | Code robustness | If `upload.done()` rejects first, `Promise.all` rejects but the `pipeline(req, …, body)` is not torn down. The request stream stays paused and open until the error response or a timeout. | "await Promise.all([pipeline(req, limitBytes(MAX_BYTES), body), upload.done()]);" | Create an `AbortController`, pass `{ signal }` to `pipeline`, and abort it in `catch` (or `req.destroy()`). | Medium | Force an S3 failure; the request socket must close promptly. |
| NODE-C09 | node-003, node-009, node-012, node-016, node-019, node-022, node-024 | both | P3 | Follow-ups | MCQs have empty FOLLOW-UPS and RELATED lists. The other formats have strong follow-ups. | "FOLLOW-UPS: []  RELATED: []" | Add 1–2 follow-ups each (e.g. node-016: "How does `events.once` behave on 'error'?"; node-009: "What does `npm update` do with the lockfile?"). | High | Each MCQ has at least one follow-up. |
| NODE-C10 | node-009, node-012, node-016, node-019, node-022, node-024 (BN) | BN | P3 | Bangla naturalness | The calque "প্রলোভনের ভুল উত্তর" (tempting wrong answer) is unnatural and repeated. | "`6.0.0` হলো প্রলোভনের ভুল উত্তর"; "এজন্যই এটা সবচেয়ে প্রলোভনের ভুল উত্তর" | Use "সবচেয়ে বিভ্রান্তিকর ভুল option" or "এখানেই বেশিরভাগ মানুষ ভুল করে". | High | Native-speaker read-through. |
| NODE-C11 | node-005, node-030 (BN) | BN | P3 | Bangla naturalness | Literal idioms: "memory বিস্ফোরিত হয়" (memory explodes) and "Zalgo ছেড়ে দিও না". | "return value ignore করলেই memory বিস্ফোরিত হয়"; "**Zalgo ছেড়ে দিও না:**" | "memory অনিয়ন্ত্রিতভাবে বাড়তে থাকে"; "\"Releasing Zalgo\" এড়াও:" (keep the English term). | High | Native-speaker read-through. |
| NODE-C12 | node-001 (BN), node-006 (BN) | BN | P3 | Register consistency | The BN text mixes first-person "আমার JavaScript code" with second-person "তুমি". This is acceptable but inconsistent with "আমাদের code" a few lines later in the same answer. | "আমার JavaScript code একটি main thread-এ চলে" … "আমাদের code → core module" | Pick one voice per answer. | Medium | — |
| NODE-C13 | node-008 | both | P3 | Needs verification | Syntax detection is claimed to still be "release candidate". The modules page does not state this, so I could not confirm it. | "on by default since v22.7 / v20.19 but still "release candidate"" | Verify on nodejs.org/api/packages.html (syntax detection). If it is now stable, drop the phrase. | Low | Docs check. |

## Per-question notes
- node-001 — issues: NODE-C12; scores acc 10 / depth 9 / BN 8 / EN 9
- node-002 — OK (output verified CJS `A E D C B`, ESM `A E C D B`)
- node-003 — issues: NODE-C02, NODE-C09; scores 9/8/9/9
- node-004 — OK (verified 3 runs, deterministic)
- node-005 — issues: NODE-C11; scores 10/9/8/9 (64 KiB default verified)
- node-006 — issues: NODE-C12 (minor); scores 10/10/9/9
- node-007 — issues: NODE-C06; scores 9/10/9/9
- node-008 — issues: NODE-C13; scores 9/9/9/9 (require(esm) `.default` and ERR_REQUIRE_ASYNC_MODULE verified)
- node-009 — issues: NODE-C09, NODE-C10; scores 10/8/8/9
- node-010 — issues: NODE-C02; scores 10/9/9/9
- node-011 — OK (ran: byte count, ENOENT, ABORT_ERR, partial file removed)
- node-012 — issues: NODE-C09, NODE-C10; scores 10/8/8/9 (exit code 1 verified)
- node-013 — OK (exact output verified)
- node-014 — OK
- node-015 — issues: NODE-C02; scores 9/9/9/9
- node-016 — issues: NODE-C09, NODE-C10; scores 10/8/8/9 (throw verified)
- node-017 — OK
- node-018 — OK
- node-019 — issues: NODE-C05, NODE-C09, NODE-C10; scores 9/9/8/9 (4+2 timing pattern verified); difficulty "hard" arguably medium
- node-020 — issues: NODE-C04 (consistency with node-028), NODE-C07; scores 9/10/9/9
- node-021 — OK (output verified)
- node-022 — issues: NODE-C01, NODE-C09, NODE-C10; scores 7/8/8/9
- node-023 — issues: NODE-C03; scores 8/9/9/9
- node-024 — issues: NODE-C09, NODE-C10; scores 10/9/8/9 (ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX for enum and parameter property verified)
- node-025 — issues: NODE-C02; scores 10/10/9/9 (prototype-pollution snippet verified `true`)
- node-026 — OK
- node-027 — OK
- node-028 — issues: NODE-C04; scores 8/9/9/9 (happy path verified: in-flight request completes, exit 0)
- node-029 — OK
- node-030 — issues: NODE-C11; scores 10/9/8/9
- node-031 — OK (ran: `[300,100,200]` in ~300 ms, `[]` for empty input, no new items after rejection)
- node-032 — issues: NODE-C08; scores 9/10/9/9

## Coverage & gaps
- COVERAGE.md subtopics are all touched: runtime, V8/libuv, event loop, streams, buffers, fs/promises, EventEmitter, ESM/CJS/require(esm), npm/semver/lockfiles, env (--env-file), error handling, worker threads, cluster, memory, CPU-bound work, API design, security/permission model, logging, graceful shutdown, performance, LTS.
- Real gaps:
  - **`uncaughtException` handling semantics** (why not to resume; `process.on('exit')` vs `'beforeExit'`). It is only mentioned in passing in node-012 and express-006.
  - **A practical `node:test` / `--watch` question.** It is only mentioned in node-003 and used in express-026.
  - **An `AsyncLocalStorage` pitfall question** (context loss with some callback libraries). Optional.
- Redundancy (acceptable and intentional): node-020/node-028 (shutdown scenario vs code); node-006/node-018 (event-loop blocking); node-017/node-026 (cluster). Across techs: node-029 (request-ID logging) and express-027 (request timer) are complementary; node-012 and express-005 both teach unhandled rejection vs Express 5 forwarding, which is fine.
- Difficulty: the progression is good (10 easy, 11 medium, 8 hard, 3 extreme). node-019 is labelled hard but reads as medium.
- Market labels: `bangladesh` is used only on output-tracing and MCQ fundamentals (node-002, -009, -016, -021, -027), which matches the FACTS guidance. There are no unsupported frequency claims.

## Needs verification
- node-008: "Syntax detection … still 'release candidate'".
- node-007: "BullMQ rejects custom job IDs that are plain integers or contain `:`". I believe recent BullMQ restricts this, but check the current BullMQ docs.
- node-025: "`--allow-child-process`, `--allow-worker` and `--allow-net` … still marked 'active development'". `--allow-net` is confirmed at Stability 1.1; the other two are not checked.
- node-015: "the `.env` utilities are documented as stable in current docs". The `--env-file` flag is confirmed; `process.loadEnvFile` stability is not checked.
- node-029: "pino 10" in the version header.

## Verified
- `node v22.18.0` (local). Scripts are in SCRATCH/run/.
- node-002: `node order.js` → `A E D C B`; `node order.mjs` → `A E C D B` (matches the claimed ESM twist).
- node-004: 3 runs → `sync nextTick promise immediate timeout` each time.
- node-005: `new Writable().writableHighWaterMark` → 65536.
- node-008: `require('./utils.mjs')` from .cjs → named export works, default at `.default`; TLA module → `ERR_REQUIRE_ASYNC_MODULE`.
- node-011: compressFile → returns byte count; missing src → `ENOENT`, no partial file; aborted signal → `AbortError ABORT_ERR`, no partial file.
- node-012: process exits code 1 with the stack; `still running` is not printed.
- node-013: exact output `sync n1 p1 p2 n2 i1 n3 p3 i2 t1`. (ESM variant prints `sync p1 n1 n2 p2 …`, which is useful for the follow-up.)
- node-016: emit('error') with no listener throws; `after emit` is not printed.
- node-019: 10-core Mac: hashes 1–4 at ~183 ms, 5–6 at ~331 ms (4-thread pool pattern confirmed).
- node-021: `5 / 15 / <Buffer 48 69 21> / SGkh / 3`.
- node-023: plain http SSE repro: after client disconnect, `res.write` → returns false, callback `ERR_STREAM_DESTROYED`, `writableEnded=false` (basis for NODE-C03).
- node-024: enum and parameter-property .ts files → `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX`; interface/import type file runs.
- node-025: prototype-pollution merge snippet prints `true`.
- node-028: SIGTERM during an in-flight keep-alive request → client gets 200, "clean shutdown", exit 0 after ~1.05 s.
- node-031: ordered results in 301 ms; empty input → `[]`; after the rejection only items [1,2] were ever started.
- WebFetch https://nodejs.org/api/modules.html → require(esm): "v25.4.0: This feature is no longer experimental"; unflagged v23.0/v22.12/v20.19.
- WebFetch https://nodejs.org/api/cli.html → `--env-file` "v24.10.0, v22.21.0: no longer experimental"; `--allow-net` "Added in: v25.0.0", Stability 1.1; "v23.5.0, v22.13.0: Permission Model and --allow-fs flags are stable".
- WebFetch https://nodejs.org/api/typescript.html → type stripping enabled by default v23.6/v22.18, stable v25.2/v24.12; `--experimental-transform-types` removed in v26.0.0; `.tsx` unsupported; tsconfig ignored.
