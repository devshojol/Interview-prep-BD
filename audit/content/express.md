# Express content audit

Coverage: all 32 IDs in dumps/express.md reviewed — express-001, express-002, express-003, express-004, express-005, express-006, express-007, express-008, express-009, express-010, express-011, express-012, express-013, express-014, express-015, express-016, express-017, express-018, express-019, express-020, express-021, express-022, express-023, express-024, express-025, express-026, express-027, express-028, express-029, express-030, express-031, express-032 (count: 32).

## Category summary
This is a high-quality, Express-5-first set. Every Express 5 behaviour I could check matches the official migration guide (fetched) and path-to-regexp 8.3 (run locally):
- the routing syntax: `*` and `/*` throw "Missing parameter name"; `/*splat` doesn't match `/`; `/{*splat}` does
- `req.body` is `undefined` without a parser
- `req.query` is a getter and uses the simple parser
- `res.send(number)` is gone
- `clearCookie` ignores `maxAge`
- dot-directories in `express.static`
- `app.listen` passes errors to its callback
- `req.host` keeps the port
- the codemod command

The MCQ keys are all defensible, and the distractors are realistic (often the Express 4 behaviour). The security content goes beyond typical interview prep: trust proxy, CORS with credentials, refresh-token rotation, credential stuffing, idempotency keys, IDOR. The debugging scenarios teach diagnostic reasoning.

The weaknesses are few:
- express-032's explanation contradicts its own code about transactional consistency.
- express-019's rotation code has a check-then-act race.
- express-007's text says "per tenant" rate limiting, but the limiter runs before the tenant is resolved.
- Some small imprecisions (helmet "cross-origin isolation"), a Java-specific OWASP reference, and empty MCQ follow-ups.

The Bangla is fluent and technically faithful, with a few calques ("প্রলোভনের উত্তর", "JWT তখনই উজ্জ্বল"). On versions, "Node 24 LTS" wording in express-031 is going stale. Coverage matches COVERAGE.md fully. Minor redundancy: Express 5 `req.query`/`req.body` changes are repeated across express-003, -012, -030 and -031, and the cookie/session material overlaps across express-016, -019 and -024.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 10 | Bangla quality 8 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| EXP-C01 | express-032 | both | P2 | Internal inconsistency | The explanation justifies PostgreSQL by "writing the payment row and marking the key completed in the same PostgreSQL transaction". The code does something different: it marks the key in a separate `UPDATE` inside a `res.json` override, outside any payment transaction. Also, responses sent with `res.send`/`res.sendStatus`/`res.end` bypass the override, which leaves the row stuck `in_progress`. | EXPL: "writing the payment row and marking the key `completed` in the same PostgreSQL transaction keeps them consistent"; CODE: "res.json = (body) => { const done = … db.query(`UPDATE idempotency_keys …`" | Either (a) say the middleware approach is "eventually consistent, with reconciliation covering the gap", or (b) show the handler completing the key inside the payment transaction (`client.query` in the same `BEGIN…COMMIT`). Note that only `res.json` responses are captured. | High | Text and code describe the same mechanism. |
| EXP-C02 | express-019 | both | P2 | Code correctness (race) | Reuse detection is check-then-act. `findByHash` and the `usedAt` check run before `rotate()`. Two concurrent requests with the same (stolen or duplicated) token both see `usedAt == null` and both receive valid new tokens, so reuse goes undetected. A transaction around the writes alone doesn't prevent this. The handler also never checks that `users.findById` returned an active user. | "if (record.usedAt) { … }" … "await refreshTokens.rotate(record, { // mark old used + insert new, in one transaction" | Make the claim atomic: `UPDATE refresh_tokens SET used_at = now() WHERE token_hash = $1 AND used_at IS NULL RETURNING …`. If 0 rows are updated, treat it as reuse (or as the grace-window case). Reject if the user is missing or disabled. | Medium-High | Two parallel `/auth/refresh` calls with the same cookie → exactly one 200; the other 401 (or the defined grace behaviour). |
| EXP-C03 | express-007 | both | P3 | Internal inconsistency | The answer says rate limiting is "per tenant and per IP", but the limiter is mounted before `authenticate`/`resolveTenant`, so there is no tenant to key on. | "rate limiting (Redis store, per tenant and per IP) → authentication (JWT verification) → **tenant resolution**"; code: `app.use('/v1', rateLimit({...}))` before `deps.authenticate, deps.resolveTenant` | Keep the pre-auth IP limiter, and add a per-tenant limiter after `resolveTenant` (keyGenerator: `req.tenant.id`). | High | The order in the text matches the code. |
| EXP-C04 | express-021 | both | P3 | Precision | "Cross-origin isolation headers" overstates the helmet 8 defaults. Helmet sets `Cross-Origin-Opener-Policy` and `Cross-Origin-Resource-Policy`, but `Cross-Origin-Embedder-Policy` is off by default. Without COEP, the page is not cross-origin isolated. | "cross-origin isolation headers" | Write "`Cross-Origin-Opener-Policy` and `Cross-Origin-Resource-Policy` (COEP is opt-in)". | Medium-High | Compare with the helmet README default list. |
| EXP-C05 | express-016 | both | P3 | Overstatement | SameSite is called "the main defence against CSRF". OWASP treats SameSite as defence in depth, with tokens or Origin checks as the primary control. The follow-up and express-017 say this correctly. | "which is the main defence against CSRF" | "a strong first layer against CSRF; combine with a CSRF token or Origin check for state-changing requests". | Medium | Consistent with express-017's "CSRF:" bullet. |
| EXP-C06 | express-019, express-023, express-024 | EN refs | P3 | References | The "OWASP — JSON Web Token Cheat Sheet" link points to the Java-specific sheet. | url ".../JSON_Web_Token_for_Java_Cheat_Sheet.html" | Retitle it "OWASP — JSON Web Token Cheat Sheet for Java (concepts apply generally)", or add RFC 8725 (JWT BCP). | High | — |
| EXP-C07 | express-023 | both | P3 | Robustness | The Bearer scheme compare is case-sensitive, and `split(' ')` breaks on repeated spaces. RFC 7235/9110 say auth schemes are case-insensitive. | "const [scheme, token] = (req.get('authorization') ?? '').split(' '); if (scheme !== 'Bearer' …" | `const m = /^Bearer\s+(\S+)$/i.exec(header)`. | High | `authorization: bearer <tok>` is accepted. |
| EXP-C08 | express-025 | both | P3 | Code robustness | In the fixed version, if `ROLLBACK` itself fails (broken connection), the error replaces the original one and the broken client still goes back to the pool. | "catch (err) { await client.query('ROLLBACK'); throw err; } finally { client.release(); }" | `catch (err) { await client.query('ROLLBACK').catch(() => {}); throw err; }` and `client.release(errIfBroken)`, or use a transaction helper. | Medium | — |
| EXP-C09 | express-031 (also express-007 ver header) | both | P3 | Version currency | The answer recommends "Node 24 LTS". After 2026-10-28, v26 is Active LTS and v24 is already in Maintenance (since 2026-10-20). | "move to Node 24 LTS in its own release" | "move to the current Active LTS (v24 → v26 from 28 Oct 2026)". | High | — |
| EXP-C10 | express-009 | both | P3 | Consistency | The code returns `Location: /v1/orders/:id`, but the answer says `Location: /orders/123`. | code `.location(`/v1/orders/${order.id}`)`; A: "`Location: /orders/123`" | Use the same path in both. | High | — |
| EXP-C11 | express-002, express-005, express-008, express-014, express-015, express-021, express-030 | both | P3 | Follow-ups | MCQs have empty FOLLOW-UPS and RELATED lists. | "FOLLOW-UPS: []  RELATED: []" | Add 1–2 follow-ups each (e.g. express-014: "How would you configure trust proxy behind Cloudflare + ALB?"). | High | — |
| EXP-C12 | express-002, express-014, express-015, express-030 (BN); express-019 (BN) | BN | P3 | Bangla naturalness | Calques: "প্রলোভনের উত্তর/ফাঁদ" and "JWT তখনই উজ্জ্বল" (literally "JWT shines"). | "`'/*splat'` হলো প্রলোভনের উত্তর"; "JWT তখনই উজ্জ্বল যখন একাধিক service…" | "সবচেয়ে বিভ্রান্তিকর option"; "JWT তখনই বেশি কাজে আসে যখন…". | High | Native-speaker read-through. |
| EXP-C13 | express-032 | both | P3 | Edge case | The fingerprint uses `JSON.stringify(req.body)`, which is sensitive to key order. The same logical request with keys reordered gets a 422. | "update(`${req.method} ${req.originalUrl} ${JSON.stringify(req.body)}`)" | Hash a canonical serialisation of the validated body (sorted keys), or hash only business fields (amount, currency, target). | Medium | — |

No P0 or P1 issues found.

## Per-question notes
- express-001 — OK
- express-002 — issues: EXP-C11, EXP-C12; scores acc 10 / depth 9 / BN 8 / EN 9 (route behaviour verified with path-to-regexp 8.3.0)
- express-003 — OK (claims verified against the migration guide)
- express-004 — OK
- express-005 — issues: EXP-C11; scores 10/9/9/9
- express-006 — OK
- express-007 — issues: EXP-C03, EXP-C09; scores 9/10/9/9
- express-008 — issues: EXP-C11; scores 10/9/9/9
- express-009 — issues: EXP-C10; scores 10/8/9/9
- express-010 — OK
- express-011 — OK
- express-012 — OK (zod v4 behaviours verified: coercion and defaults, limit=500 rejected, empty page rejected, strictObject unknown key in formErrors)
- express-013 — OK
- express-014 — issues: EXP-C11, EXP-C12; scores 10/9/8/9
- express-015 — issues: EXP-C11, EXP-C12; scores 10/8/8/9
- express-016 — issues: EXP-C05; scores 9/9/9/9
- express-017 — OK (cors 2.8.5 verified: `origin:'*', credentials:true` → `*` + `true`)
- express-018 — OK
- express-019 — issues: EXP-C02, EXP-C06, EXP-C12; scores 8/10/8/9
- express-020 — OK
- express-021 — issues: EXP-C04, EXP-C11; scores 9/8/9/9
- express-022 — OK
- express-023 — issues: EXP-C06, EXP-C07; scores 9/9/9/9
- express-024 — issues: EXP-C06; scores 10/9/9/9
- express-025 — issues: EXP-C08; scores 10/10/9/9
- express-026 — OK
- express-027 — OK
- express-028 — OK (z.enum(Object.keys(SORTS)) rejects injection string — verified)
- express-029 — OK (`@1790812800` = 2026-10-01T00:00:00Z verified)
- express-030 — issues: EXP-C11, EXP-C12; scores 10/9/8/9
- express-031 — issues: EXP-C09; scores 10/10/9/9
- express-032 — issues: EXP-C01, EXP-C13; scores 8/10/9/9

## Coverage & gaps
- All COVERAGE.md subtopics are covered:
  - routing (v5 syntax), middleware, lifecycle, error middleware, centralized errors (v5 async)
  - REST, validation, authN/authZ, JWT, cookies/sessions, CORS
  - rate limiting, helmet, multer, pagination/filter/sort, versioning
  - logging, testing (supertest + node:test), deployment/trust proxy, production debugging
  - v4→v5 migration
  - practical middleware implementations (010, 012, 023, 027, 032)
- Minor gaps:
  - **CSRF implementation**, now that `csurf` is deprecated (FACTS mentions this; it is only touched in bullets).
  - **`express.Router` composition** (`mergeParams`, router-level middleware).
  - **Response streaming/compression** (`compression`, Brotli in Express 5 per FACTS).
- Redundancy: the Express 5 `req.query`/`req.body` changes are taught in express-003, -012, -030 and -031. Consider trimming express-031's silent-change list to reference express-003. The cookie attributes in express-016 overlap express-024 and -019, which is acceptable.
- Cross-tech overlap with nodejs: node-012 and express-005 (unhandled rejections) and node-029 and express-027 (logging) are complementary, not duplicates.
- Difficulty: the progression is sensible (10 easy, 11 medium, 7 hard, 4 extreme). No mislabels.
- Market labels: `bangladesh` is used on MCQ/viva-style fundamentals and MERN-typical JWT middleware. No unsupported frequency claims.

## Needs verification
- "Verified on Express 5.3" claims (express-002, -008, -014, -021, -023, -026, -027, -030). I could not run Express 5 locally (no copy, offline). The route semantics were checked with path-to-regexp 8.3.0, and the API changes against the official migration guide.
- express-021: "helmet 8.3" and the HSTS default "one year, includeSubDomains" (I believe helmet 8 changed the default to 365 days, so this is likely correct).
- express-018/020: express-rate-limit 8 details. `ipKeyGenerator` and the IPv6 subnet grouping by default are consistent with what I know of v8. Not fetched: the `ERR_ERL_UNEXPECTED_X_FORWARDED_FOR` name, and `draft-8` sending combined `RateLimit` and `RateLimit-Policy`.
- express-013: "an outdated multer has had several DoS fixes in 2025–2026" (from FACTS).
- express-024: connect-redis named export `RedisStore` (true for v8+; version unspecified).

## Verified
- path-to-regexp 8.3.0 (local copy at ~/.npm/_npx/69f9afb961c37556/node_modules/path-to-regexp):
  - `*` and `/*` → throw "Missing parameter name"
  - `/*splat` → no match for `/`, `/a/b` → `['a','b']`
  - `/{*splat}` → matches `/` with params `{}`
  - `/:file{.:ext}` → `/x.png` → `{file:'x', ext:'png'}`
  - `/users/:id?` → throws "Unexpected ?"
- zod v4 (zod 3.25.76 `/v4` entry): listProducts schema → `{page:2,limit:20,sort:'-createdAt'}`; `limit=500` → fail; `page=''` → fail; strictObject → `formErrors:["Unrecognized key: \"isAdmin\""]`; `z.stringbool`, `z.url` exist; `z.enum(Object.keys(SORTS))` rejects `name;DROP`.
- cors 2.8.5: `cors({origin:'*',credentials:true})` → `Access-Control-Allow-Origin: *` and `Access-Control-Allow-Credentials: true` (confirms express-017).
- `new Date(1790812800*1000)` → 2026-10-01T00:00:00Z (express-029).
- WebFetch https://expressjs.com/en/guide/migrating-5.html confirms:
  - codemod `npx codemod@latest @expressjs/v5-migration-recipe`
  - dotfiles check applies to hidden directories (`/.well-known` → 404 unless `dotfiles:'allow'`)
  - `req.host` keeps the port; `app.listen` passes errors to its callback
  - `res.status` accepts only integers 100–999
  - `req.body` is `undefined` when unparsed
  - `req.query` is a getter, with the default parser changed to "simple"
  - `clearCookie` ignores `maxAge`/`expires`
  - `req.params` has a null prototype for string paths
  - `res.send(status)` is unsupported (quote numbers to send them as a body)
