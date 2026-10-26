# Redis content audit

Coverage: 32/32 questions reviewed — redis-001, redis-002, redis-003, redis-004, redis-005, redis-006, redis-007, redis-008, redis-009, redis-010, redis-011, redis-012, redis-013, redis-014, redis-015, redis-016, redis-017, redis-018, redis-019, redis-020, redis-021, redis-022, redis-023, redis-024, redis-025, redis-026, redis-027, redis-028, redis-029, redis-030, redis-031, redis-032.

Distribution: easy 11 (001–011), medium 11 (012–022), hard 7 (023–029), extreme 3 (030–032). MCQs 8 (002, 004, 007, 009, 016, 017, 022, 029).

## Category summary
This is a strong category. Command semantics, outputs and MCQ keys are accurate. I traced every command output and MCQ by hand, and the claims I spot-checked online (Redis 8.6 LRM eviction, DELEX/IFEQ in 8.4, the Redis docs recommending fencing tokens, node-redis v6 RESP3 default plus 5 s command timeout) are correct. The answers are interview-ready: they define, explain the mechanism, give trade-offs and failure modes (lost update, TTL wiped by SET, KEYS blocking, PEL/XAUTOCLAIM, lease vs fencing, fork/THP stalls). The main weaknesses are in Node.js integration code, not in Redis theory:
- **Fail-open claims don't match the code.** Several snippets promise "fall back to the DB / fail open when Redis is down" but use node-redis defaults, where commands queue offline or wait up to the 5 s command timeout.
- **Session TTL bug.** The session example's "sliding expiration" can't work because the cookie maxAge is never refreshed.
- **Stream reply shape.** The Streams consumer reads the RESP2 reply shape, while redis-019 itself says v6 defaults to RESP3.

Bangla is natural and technically equivalent throughout, with only a few literal idioms. Versions match FACTS.md. The only stale item is the "Node.js 24 LTS" label in redis-019. Coverage of COVERAGE.md subtopics is complete. The token bucket appears only as prose and a follow-up, which is acceptable. Redundancy is low; 005/013/014 and 017/026 overlap but test different skills.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8.5 | English quality 9 | Examples & code 8 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| REDIS-C01 | redis-005, redis-012, redis-013 (fixed version), redis-023 | both | P2 | Technical accuracy / code | Claims of graceful fallback or fail-open when Redis is down, but clients use node-redis defaults: the offline queue is enabled, so commands are queued while reconnecting and only reject at the default 5 s `commandTimeout` (v6). Each request stalls instead of failing fast. redis-019 itself explains this ("requests hang instead of falling back"), so the bank is internally inconsistent. | 012: `console.error('Rate limiter unavailable, failing open:'...)` with a client created without options; 005: "if Redis goes down the app can still read from the database"; 013 fix: `console.warn('Cache read failed, falling back to DB'...)` | Create the shared client with `disableOfflineQueue: true` (and/or a short per-command timeout) in these snippets, or add a sentence: "this fallback only triggers promptly if the client fails fast (see redis-019)". | Medium-High | Stop Redis while the app runs: with the current snippet, a request hangs up to ~5 s; with `disableOfflineQueue: true` it hits the catch immediately. |
| REDIS-C02 | redis-008 | both | P2 | Technical accuracy / code | "Sliding expiration" is broken. `GETEX` refreshes the Redis TTL on every request, but the cookie is set once at login with `maxAge: SESSION_TTL * 1000` and never re-issued. The browser drops the cookie 24 h after login regardless of activity, so "log out after 24 h of inactivity" really means "log out 24 h after login". | `res.cookie('sid', sid, { ... maxAge: SESSION_TTL * 1000 })` only in `createSession`; answer: "refresh the TTL for **sliding expiration** if you want 'log out after 24 h of inactivity'" | In the middleware, re-set the cookie (same options) when the session is valid, or use a session cookie (no maxAge) and rely on the server TTL. Add an absolute maximum lifetime as a best practice. | High | Log in, stay active for 25 h: with the current code the cookie expires at 24 h and the user is logged out. |
| REDIS-C03 | redis-021 (vs redis-019) | both | P2 | Internal inconsistency / version | redis-019 says node-redis v6 defaults to RESP3 (confirmed by the v6 release notes). Under RESP3, node-redis returns XREAD/XREADGROUP as a map keyed by stream name, not an array of `{name, messages}`. The redis-021 loop would then silently process nothing. | `for (const m of res?.[0]?.messages ?? []) await handle(m);`; redis-019: "Both v6 lines default to **RESP3**" | Either show the RESP3 shape (`res?.[STREAM]` / `Object.values(res ?? {})`, per the v6 docs) or create the client with `RESP: 2` and say so. Also loop `XAUTOCLAIM` on `nextId` as the explanation says. | Medium (exact RESP3 transform shape not verified against v6 source) | Run the snippet against Redis 8 with node-redis 6.3 defaults and log `res`. Messages must be processed. |
| REDIS-C04 | redis-030 | both | P3 | Completeness | The conditional-update design has no recovery path: if the worker crashes after setting `status='charging'` (before or after charging), the order is stuck because only `status='pending'` rows can be claimed. The lock release is also not in `finally`. Fine for illustration, but an extreme-level answer should name it. | `WHERE id = ${orderId} AND status = 'pending' AND fence < ${fence}` ... `await redis.sendCommand(['DELEX', ...])` (not in finally) | Add one bullet: a reconciler retries `charging` rows older than N minutes using the same idempotency key (safe because the provider deduplicates); wrap the release in `finally`. | High | Reviewer reads the answer and can say what happens to an order whose worker died mid-charge. |
| REDIS-C05 | redis-012 | both | P3 | Misleading mistake text | The common mistake "resetting the TTL on every request (turning the window into '100 per minute of silence')" applies to un-windowed keys, not to the shown design. The key includes `windowId`, so plain `EXPIRE` every time would be harmless. `EXPIRE ... NX` is fine but not what prevents the bug here. | `const key = \`${prefix}:${id}:${windowId}\``; "resetting the TTL on every request" | Rephrase: "if the key is just `rl:<id>` (no window number), resetting the TTL on each request turns it into…". | High | Text matches the code's key design. |
| REDIS-C06 | redis-002, redis-020 (`bangladesh`); redis-031 (`international`); redis-026 tip | EN | P3 | Market labels / unsupported claims | `bangladesh` market labels on generic INCR/command-tracing fundamentals are only weakly supported (FACTS mentions BD MCQ/output-tracing tests, not Redis). redis-031 is set on a Bangladeshi 11.11 sale but labelled `international`. The redis-026 tip asserts an unsupported market claim. | 026 tip: "Interviewers for international roles especially look for that incident-response structure." | Use `market=both` for 002/020/031 (or justify), and drop "for international roles especially". | Medium | Labels are justified against the FACTS research notes. |
| REDIS-C07 | redis-007 | both | P3 | Mis-categorised subtopic / distractor | Subtopic "Memory Usage", but the question is about blocking/latency (KEYS O(N) on a single thread). Option A ("only searches database 0") is a partially true statement (KEYS scans only the selected DB). It isn't a "danger", but it's not purely false. | `redis-007 | Memory Usage`; Option A text | Re-tag as "Production Failure Scenarios" or "Single-threaded execution", and reword A to a clearly false claim (e.g. "`KEYS` returns at most 10 keys per call"). | High | Subtopic matches content; exactly one defensible option. |
| REDIS-C08 | redis-019 | EN | P3 | Version currency | `ver` says "Node.js 24 LTS". Per FACTS, Node 24 entered Maintenance on 2026-10-20 and Node 26 becomes LTS on 2026-10-28. The SIGTERM snippet also says "stop accepting work" but never closes the HTTP server. | `ver=node-redis 6.3; ioredis 6.0; Node.js 24 LTS`; `process.on('SIGTERM', async () => { await Promise.allSettled([...]); process.exit(0); })` | Change to "Node.js 24/26 LTS" and add `server.close()` before closing clients. | High | ver label current; snippet shows the HTTP server closing first. |
| REDIS-C09 | redis-012, redis-026, redis-021 | BN | P3 | Bangla phrasing | Literal idioms read awkwardly. | 012: "চুপ থাকার প্রতি মিনিটে 100"; 026: "রক্তক্ষরণ থামাও"; 021: "অনাথ message" | 012: "window তখন 'শেষ request-এর পর এক মিনিট' হয়ে যায়"; 026: "আগে আগুন নেভাও / আগে পরিস্থিতি সামলাও"; 021: "মালিকহীন (orphaned) message". | Medium | Native BN reviewer reads them as natural. |
| REDIS-C10 | redis-002, 004, 007, 009, 016, 017, 022, 029 | both | P3 | Weak follow-ups | All MCQs have `FOLLOW-UPS: []`, though AUTHORING asks for 1–3 per question. | `FOLLOW-UPS: []` | Add 1–2 follow-ups each (e.g. 004: "How would you keep the remaining TTL when overwriting?" → KEEPTTL). | High | check.py / manual: every question has ≥1 follow-up. |
| REDIS-C11 | redis-027 | both | P3 | Precision | "at most about one second of writes lost" with `everysec`. The Redis persistence docs describe the worst case as up to ~2 s when the background fsync is delayed. | "at most about one second of writes lost" | "typically about one second (worst case ~2 s if fsync stalls)". | Medium | Matches the persistence doc wording. |

## Per-question notes
- redis-001 — OK
- redis-002 — issues: REDIS-C06, REDIS-C10; acc 10 / depth 8 / BN 9 / EN 9
- redis-003 — OK
- redis-004 — issues: REDIS-C10; acc 10 / depth 9 / BN 9 / EN 9
- redis-005 — issues: REDIS-C01; acc 8 / depth 9 / BN 9 / EN 9
- redis-006 — OK
- redis-007 — issues: REDIS-C07, REDIS-C10; acc 9 / depth 9 / BN 9 / EN 9
- redis-008 — issues: REDIS-C02; acc 7 / depth 9 / BN 9 / EN 9
- redis-009 — issues: REDIS-C10; acc 10 / depth 9 / BN 9 / EN 9
- redis-010 — OK (licensing timeline, Valkey 7.2.4 fork, VADD/VSIM syntax, Q8 default all consistent with FACTS)
- redis-011 — OK
- redis-012 — issues: REDIS-C01, REDIS-C05, REDIS-C09; acc 8 / depth 9 / BN 8 / EN 9
- redis-013 — issues: REDIS-C01 (fixed version); acc 9 / depth 9 / BN 9 / EN 9
- redis-014 — OK
- redis-015 — OK (BLMOVE RIGHT LEFT, XGROUP/MKSTREAM, MAXLEN ~ syntax correct)
- redis-016 — issues: REDIS-C10; acc 10 / depth 9 / BN 9 / EN 9 (D correctly empty; BYSCORE REV form correct)
- redis-017 — issues: REDIS-C10; acc 10 / depth 9 / BN 9 / EN 9 (8.6 LRM verified)
- redis-018 — OK (HEXPIRE/HTTL/HSETEX/HGETEX syntax and -1/900 replies correct)
- redis-019 — issues: REDIS-C08; acc 9 / depth 9 / BN 9 / EN 9
- redis-020 — issues: REDIS-C06; acc 10 / depth 9 / BN 9 / EN 9 (all 12 replies traced correct)
- redis-021 — issues: REDIS-C03, REDIS-C09; acc 7 / depth 9 / BN 8 / EN 9
- redis-022 — issues: REDIS-C10; acc 10 / depth 9 / BN 9 / EN 9
- redis-023 — issues: REDIS-C01; acc 9 / depth 10 / BN 9 / EN 9
- redis-024 — OK (Lua logic, TIME use, retryAfter math and expected output consistent)
- redis-025 — OK (DELEX IFEQ 8.4 verified; SETNX deprecated correct)
- redis-026 — issues: REDIS-C06, REDIS-C09; acc 10 / depth 9 / BN 8 / EN 9
- redis-027 — issues: REDIS-C11; acc 9 / depth 9 / BN 9 / EN 9
- redis-028 — OK
- redis-029 — issues: REDIS-C10; acc 10 / depth 9 / BN 9 / EN 9 (EXEC → 1, WRONGTYPE, 2; counter "2" correct)
- redis-030 — issues: REDIS-C04; acc 9 / depth 10 / BN 9 / EN 9 (Lua SET NX truthiness and same-slot hash tags correct; fencing recommendation matches Redis docs)
- redis-031 — issues: REDIS-C06; acc 9 / depth 10 / BN 9 / EN 9
- redis-032 — OK (sort pipeline on `INFO commandstats` verified to sort by usec_per_call)

## Coverage & gaps
- All COVERAGE.md subtopics are present: fundamentals, data types, TTL including hash-field expiry, cache-aside/invalidation, sessions, rate limiting (fixed + sliding; token bucket only as prose/follow-up), Pub/Sub, Streams, RDB/AOF, eviction, memory, stampede, locks/Redlock/fencing, vs DB, vs Memcached, node-redis/ioredis, failure scenarios, Redis 8/Valkey, cluster/sentinel.
- Small gaps (optional):
  - Pipelining vs MULTI is only covered inside the redis-029 explanation; there is no question on HyperLogLog/bitmaps.
  - A token-bucket Lua question would cover the named COVERAGE item explicitly. Could replace one of the two Production Failure scenarios if space is tight.
- Overlap is acceptable: 005/013/014 (cache-aside read/debug/invalidation), 017/026 (eviction MCQ vs OOM incident), 025/030 (lock bugs vs fencing design).
- Difficulty labels are appropriate. redis-029 (MULTI runtime error) is arguably medium rather than hard.

## Needs verification
- redis-019 / redis-032: "Both v6 lines (node-redis, **ioredis 6.0**) default to RESP3 and require Node.js 20+". This is verified for node-redis 6.0 but not for ioredis 6.0.
- redis-021: "Redis 8.2 added options (e.g. `XACKDEL`)". Not checked.
- redis-021 / REDIS-C03: the exact node-redis v6 RESP3 reply shape for `xReadGroup`.
- redis-010: "8.10 is the current stable release; 8.2 extended-support". Matches FACTS; not re-checked.

## Verified
- WebFetch https://redis.io/docs/latest/develop/reference/eviction/ — `allkeys-lrm`/`volatile-lrm` exist "Starting with Redis 8.6" (confirms redis-017).
- WebFetch https://redis.io/docs/latest/commands/delex/ — DELEX since 8.4.0 with IFEQ/IFNE/IFDEQ/IFDNE; SET has IFDEQ/IFDNE options (confirms redis-025/030).
- WebFetch https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/ — "Disclaimer about consistency" says "You should implement fencing tokens" (confirms the redis-030 claim).
- WebSearch: node-redis 6.0.0 release notes (mirrored at releases.sh: https://releases.sh/release/rel_Pm49rG_HmsdLVzwfvMgUQ) — RESP3 default, Node 20 minimum, `commandTimeout` default 5 s (confirms redis-019/032).
- Shell: ran a sample `INFO commandstats` text through `sort -t= -k4 -n | tail` — it sorts by usec_per_call (redis-032 correct).
- Manual traces: redis-020 (12 replies), redis-029 (EXEC reply), redis-016 options, redis-024 Lua/expected output, redis-004 TTL semantics — all correct.
