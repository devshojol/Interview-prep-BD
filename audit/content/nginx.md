# NGINX content audit
Coverage: 32 of 32 questions reviewed. IDs: nginx-001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 025, 026, 027, 028, 029, 030, 031, 032.

## Category summary
This is a high-quality, current NGINX set. It covers the classic interview traps well (location matching order, `proxy_pass` trailing slash, `root` vs `alias` and off-by-slash traversal, `add_header` inheritance, `worker_connections` counting upstream connections, hop-by-hop WebSocket headers, 502 vs 504 vs 499). It also correctly reflects the 2025–2026 changes: upstream keepalive and HTTP/1.1 on by default in 1.29.7, `add_header_inherit` in 1.29.3, OSS `sticky` in 1.29.6, `least_time` and `ngx_http_tunnel_module` in 1.31.0, upstream `resolve` in 1.27.3, and HTTP/2 to backends in 1.29.4. I verified all of these against nginx.org CHANGES. Answers explain mechanisms, give scoped fixes, and include security and operational caveats (trust proxy spoofing, CGNAT, realip, Set-Cookie caching).

Main weaknesses:
- One MCQ (nginx-012) whose response labels A–E collide with the option letters A–D, so the answer text says "D" while the keyed option is B.
- A verification tip that gives a false negative (`curl -I` with gzip).
- A few missing caveats (rate-limit empty key, `proxy_cache_lock_timeout`, buffering vs `$upstream_response_time`).
- Repeated themes across items (add_header inheritance 3×, keepalive-timeout race 3×).
- Generic "interviewers love this" filler in the tips.

The Bangla is fluent and technically faithful, with a few literal calques ("নিবেদিত tool", "ধারালো কোণ", "কড়ি") and one broken sentence (nginx-003). Coverage of COVERAGE.md subtopics is complete. Difficulty is 11 easy, 11 medium, 7 hard, 3 extreme.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 8

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| NGINX-C01 | nginx-012 | both | P1 | MCQ letter mismatch | The locations return the strings "A"–"E", and the options are also lettered A–D. The keyed option is **B** (whose text starts "D — …"), but the answer says "The answer is **D**". The explanation also calls response "B" (option A) "the tempting wrong answer" and response "C" (option C). Learners will read this as a wrong key. | ANSWER: "The answer is **D**." ; OPTION B (CORRECT): "D — the regex location wins…" ; "The tempting wrong answer is B" | Rename the returned bodies to non-letters (e.g. `return 200 "root"`, `"images"`, `"icons"`, `"regex"`, `"logo"`) and update options/explanation, or refer to options only by content. Same in BN. | High | Each letter mentioned in the answer/explanation is the same letter as the option it refers to. |
| NGINX-C02 | nginx-009 | both | P2 | Incorrect verification step | The tip's check uses `curl -I` (a HEAD request). NGINX's gzip header filter skips header-only responses, so `Content-Encoding: gzip` never appears and the learner concludes gzip is broken. (The extra code, which uses GET, is correct.) | TIP: "Verify with `curl -H 'Accept-Encoding: gzip' -I`." / BN "`curl -H 'Accept-Encoding: gzip' -I` দিয়ে যাচাই করো।" | Use `curl -s -o /dev/null -D - -H 'Accept-Encoding: gzip' URL` (as in the extra code) and note "HEAD responses aren't gzipped". | High (source verified) | Tip command is a GET. |
| NGINX-C03 | nginx-010 | both | P3 | Missing caveat | "Excluding slow-client time" holds only with `proxy_buffering on` (the default). With buffering off (as recommended for streaming in nginx-026), upstream time also includes time waiting on the client. | "Which variable tells you how long the Node.js backend took … excluding the time NGINX spent talking to a slow client?" | Add one line: "true with the default `proxy_buffering on`; with buffering off, a slow client also inflates `$upstream_response_time`." | Medium–High | Caveat present in EN and BN. |
| NGINX-C04 | nginx-030 | both | P3 | Missing caveat | `limit_req_zone $cookie_session …`: per the docs, requests with an empty key are not counted, so requests without a session cookie bypass the checkout limit. (Here they're still covered by `api_ip`, but this should be stated.) | `limit_req_zone $cookie_session zone=checkout_s:10m rate=2r/s;` | Note "empty keys aren't accounted, so keep the per-IP limit too (as here), or map a missing cookie to `$binary_remote_addr`." | High | Explanation mentions the empty-key behaviour. |
| NGINX-C05 | nginx-023 | both | P3 | Overstatement | `proxy_cache_lock` doesn't guarantee exactly one upstream request. After `proxy_cache_lock_timeout` (5 s default) the waiting requests go upstream, and their responses aren't cached. | "send only **one** request to Node…" ; "`proxy_cache_lock on` lets only one request populate a missing entry while the others wait." | Add `proxy_cache_lock_timeout` / `proxy_cache_lock_age` to the explanation. | High | Lock timeout mentioned. |
| NGINX-C06 | nginx-024 | both | P3 | Imprecise | Docker's embedded DNS does return a TTL. The reason for `valid=` is to override that TTL with a short re-resolve interval, not that the TTL is "not meaningful". | "Keep `valid=` short, because Docker's DNS answers don't carry a meaningful TTL for this purpose." | "Docker's DNS returns a long TTL; `valid=10s` makes NGINX re-resolve sooner after a container is recreated." | Low–Medium | Wording no longer claims no TTL. |
| NGINX-C07 | nginx-026 | both | P3 | Overconfident inference | The root cause is asserted as fact; silence for 60 s could also be a slow query before the first byte. | "so Node sent **nothing** for 60 s. It's building the entire CSV in memory before responding." | "…most likely because it builds the whole CSV (or waits on a slow query) before writing anything." | Medium | Hedged wording. |
| NGINX-C08 | nginx-031 | both | P3 | Missing pitfalls | (a) Anonymous users are bucketed by IP and then by `uid` after login, so they can flip versions mid-session. (b) Anyone can set the `canary=always` cookie, which exposes v2. (c) The `X-Release-Variant` header advertises internals publicly. | `map $cookie_uid $canary_key { "" $remote_addr; …}` ; `map $cookie_canary … always api_canary;` | Add these to the pitfalls (set a `uid` cookie on first visit; restrict the QA override, e.g. by IP allow-list or a signed value). | Medium | Pitfalls list includes them. |
| NGINX-C09 | nginx-008 | both | P3 | Version currency | "Let's Encrypt certificates are … 90 days" is still the default, but Let's Encrypt has announced a move to shorter lifetimes (45-day opt-in profile in 2026, default later), alongside the CA/B 47-day schedule already cited. | "Let's Encrypt certificates are short-lived (90 days)" | Add "(Let's Encrypt is moving to 45-day certificates)". Verify the exact dates first. | Medium | Statement current as of publish date. |
| NGINX-C10 | nginx-003, nginx-002, nginx-023, nginx-032 | BN | P3 | Bangla wording | One broken sentence and a few literal calques. | 003: "`server` block-এ `add_header` দিয়ে HSTS set করলে, তারপর একটা `location`-এ একটা `add_header Cache-Control …` যোগ করলে। ওই location-এর…" (fragment) ; 002: "নিবেদিত tool" ; 023: "ধারালো কোণগুলোও জানো" ; 032: "যেকোনো একটা কড়ি ভাঙলেই" | 003: "…যোগ করলে ওই location-এর response থেকে HSTS চুপচাপ হারিয়ে যায়।" 002: "আলাদা/বিশেষায়িত tool"; 023: "ঝুঁকিপূর্ণ দিকগুলোও জানো"; 032: "chain-এর যেকোনো একটা ধাপ ভাঙলেই" | High | A native reviewer reads the sentences as natural. |
| NGINX-C11 | nginx-008, 013, 015, 017, 021, 028 (pattern) | both | P3 | Filler | Tips end with generic claims about interviewer reactions. | "Interviewers love this question because the bug is one character." ; "a small detail that interviewers notice" ; "That's the depth interviewers look for." | Remove or replace with concrete phrasing to say aloud. | High | Tips are actionable only. |
| NGINX-C12 | 003/020/027; 019/025/032; 001/007/016; 005/015/022; 011/018; 006/020 | both | P3 | Redundancy | The same sub-points are re-explained several times (add_header inheritance + `add_header_inherit`; the Node keepAliveTimeout vs NGINX keepalive race; reload worker hand-off; the proxy header set). | e.g. inheritance trap in 003 EXPLANATION, 020 EXPLANATION and 027 ANSWER §3 | Keep the full treatment in one canonical item (027 for headers, 025 for keepalive) and reference it from the others. | Medium | Each repeated point is fully explained in one item and only referenced elsewhere. |
| NGINX-C13 | nginx-022, nginx-026 | EN | P3 | Version currency | ver labels say "Node.js 24 LTS". Node 24 has been in Maintenance since 2026-10-20 and Node 26 becomes LTS on 2026-10-28 (FACTS). | ver: "NGINX 1.30 stable, Node.js 24 LTS, PM2 / systemd" | Update to "Node.js 24/26 LTS" or the current Active LTS. | High (per FACTS) | No label implies 24 is Active LTS. |
| NGINX-C14 | FACTS (affects version notes generally) | — | P3 | Facts file currency | FACTS says mainline is 1.31.6. The nginx.org CHANGES fetch reported 1.31.8 (21 Oct 2026) as the latest entry. Content says "1.31 mainline" generically, so no question is wrong. | FACTS: "Mainline **1.31.6**" | Re-check and update FACTS. | Low (summarised fetch) | FACTS matches nginx.org. |

## Per-question notes
- nginx-001 — OK
- nginx-002 — issues: C10; acc 10 / depth 9 / BN 8 / EN 9 (tunnel module in 1.31.0 verified)
- nginx-003 — issues: C10, C12; acc 10 / depth 9 / BN 7 / EN 9
- nginx-004 — OK
- nginx-005 — OK
- nginx-006 — OK
- nginx-007 — issues: C12 (overlaps 001); acc 10 / depth 8 / BN 9 / EN 9
- nginx-008 — issues: C09, C11; acc 9 / depth 9 / BN 9 / EN 9
- nginx-009 — issues: C02; acc 8 / depth 9 / BN 9 / EN 9
- nginx-010 — issues: C03; acc 9 / depth 9 / BN 9 / EN 9
- nginx-011 — OK
- nginx-012 — issues: C01; acc 6 (keying presentation) / depth 9 / BN 8 / EN 8
- nginx-013 — issues: C11; acc 10 / depth 9 / BN 9 / EN 9
- nginx-014 — OK
- nginx-015 — issues: C11, C12; acc 10 / depth 9 / BN 9 / EN 9
- nginx-016 — OK
- nginx-017 — issues: C11; acc 10 / depth 10 / BN 9 / EN 9
- nginx-018 — OK (sticky 1.29.6, least_time 1.31.0 verified)
- nginx-019 — issues: C12; acc 10 / depth 9 / BN 9 / EN 9
- nginx-020 — issues: C12; acc 10 / depth 9 / BN 9 / EN 9
- nginx-021 — issues: C11; acc 10 / depth 8 / BN 9 / EN 9
- nginx-022 — issues: C12, C13; acc 9 / depth 9 / BN 9 / EN 9
- nginx-023 — issues: C05, C10; acc 9 / depth 9 / BN 8 / EN 9
- nginx-024 — issues: C06; acc 9 / depth 9 / BN 9 / EN 9 (upstream `resolve` 1.27.3 verified)
- nginx-025 — issues: C12; acc 10 / depth 9 / BN 9 / EN 9 (1.29.7 defaults verified)
- nginx-026 — issues: C07, C13; acc 9 / depth 10 / BN 9 / EN 9
- nginx-027 — OK (add_header_inherit 1.29.3 verified)
- nginx-028 — issues: C11; acc 10 / depth 9 / BN 9 / EN 9
- nginx-029 — OK
- nginx-030 — issues: C04; acc 9 / depth 10 / BN 9 / EN 9
- nginx-031 — issues: C08; acc 9 / depth 9 / BN 9 / EN 9 (`drain` parameter in 1.29.6 verified)
- nginx-032 — issues: C10, C12; acc 10 / depth 10 / BN 8 / EN 9

## Coverage & gaps
- Every COVERAGE.md subtopic is covered: master/worker, reverse vs forward proxy, LB algorithms and passive checks, HTTPS/TLS termination, static files, upstreams, proxy headers, WebSocket, proxy_cache, rate limiting, gzip, 413, timeouts, logging, config blocks and location order, 502/504, NGINX + Node, NGINX + Docker, deployment architecture, SPA fallback, `http2 on;`.
- Minor gaps (optional): `limit_conn` is only mentioned in passing; there's no item on redirects/rewrites (`return 301` vs `rewrite`, www→apex canonicalisation) or `server_name` selection rules beyond default_server (027); `stream {}` TCP/UDP proxying (e.g. a Postgres/Redis TCP proxy) appears only in one sentence; access control (`allow/deny`, `auth_basic`) is shown only in the stub_status snippet.
- Difficulty labels are appropriate. nginx-021 (`http2 on` MCQ) could be easy.
- Redundancy: see C12. Cross-tech overlap: nginx-024 ↔ docker-010/025 (localhost / Docker DNS), nginx-031 ↔ docker-031 (blue/green vs canary). These complement each other; cross-link them via RELATED.

## Needs verification
- nginx-008: Let's Encrypt shorter-lifetime rollout dates (45-day certificates) and the CA/B "47 days by 2029" schedule (the latter I believe is correct: ballot SC-081).
- nginx-021/025: the exact directive form `proxy_http_version 2` for HTTP/2 upstreams. CHANGES 1.29.4 says only "ngx_http_proxy_module supports HTTP/2" and doesn't name the value.
- nginx-029/031: OSS `sticky cookie` syntax `sticky cookie rt_srv expires=1h path=/ httponly secure;` matches the open-source docs (it's the Plus syntax; the 1.29.6 feature is confirmed, but the parameter set is not).
- nginx-027: "Let's Encrypt shut down its OCSP service in 2025" (I believe this is correct, August 2025).
- FACTS mainline version (C14).

## Verified
- WebFetch https://nginx.org/en/CHANGES confirmed:
  - 1.29.7 (24 Mar 2026): keepalive in upstream on by default; `proxy_http_version` default 1.1; `Connection` not sent.
  - 1.29.3 (28 Oct 2025): `add_header_inherit`.
  - 1.29.6 (10 Mar 2026): `sticky` plus `route`/`drain` server parameters.
  - 1.29.4 (09 Dec 2025): proxy module supports HTTP/2.
  - 1.31.0 (13 May 2026): `least_time` and `ngx_http_tunnel_module`.
  - 1.27.3 (26 Nov 2024): upstream `server … resolve`.
  - The latest entry reported was 1.31.8 (21 Oct 2026).
- WebFetch of `src/http/modules/ngx_http_gzip_filter_module.c` (nginx GitHub master): the skip condition in `ngx_http_gzip_header_filter` includes `|| r->header_only`, which confirms that HEAD responses are not gzipped (basis for C02).
- No nginx binary available locally (`which nginx` → not found), so no configs were executed.
