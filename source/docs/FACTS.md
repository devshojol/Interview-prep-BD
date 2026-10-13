# Verified Technology Facts — verified 2026-10-12

All versions below were checked on 2026-10-12 against the npm registry (`npm view <pkg> dist-tags`),
nodejs.org, official docs/blogs and release-note pages. Use `verifiedAt: "2026-10-12"` in question records.
If you write a version-sensitive claim that is NOT covered here, verify it yourself against the official
docs (WebFetch) before writing it, or phrase it in a version-independent way.

## Version table

| Technology | Current stable (2026-10-12) | Notes |
|---|---|---|
| HTML | HTML Living Standard (WHATWG) | No version numbers. Use Baseline status (web-features 3.42.0) for browser support. |
| CSS | CSS Snapshot / Baseline | See Baseline list below. |
| JavaScript | ECMAScript 2026 (17th edition, approved by Ecma GA on 2026-06-30) | ES2025 + ES2026 features listed below. |
| React | **19.3.0** (blog post 2026-09-09) | React Compiler v1.0 (2025-10-07). React Foundation (Linux Foundation) since Feb 2026. |
| Next.js | **16.4.0** (2026-10-06) | Uses React 19.3. Next 16.0 was 2025-10-21. Next 17 not released (Cache Components will be default in 17). Min Node 20.9. |
| Node.js | **v24 "Krypton" = Active LTS (24.21.0)**, moves to Maintenance 2026-10-20. **v26 = Current (26.11.1)**, becomes LTS on 2026-10-28. v22 "Jod" = Maintenance LTS until 2027-04-30. v20 EOL 2026-04-30. v25 EOL. | New release model from Node 27: one major per year (April), every release becomes LTS (October), alpha channel; 27.0.0-alpha starts 2026-10-28, 27.0.0 in April 2027. Recommend v24 LTS for production now (v26 after 2026-10-28). |
| Express | **5.3.0** (2026-10-09); `latest-4` = 4.22.3 | Express 5 is the npm default since 5.1.0 (2025-03-31). Express 5 `engines.node >= 18`. |
| NestJS | **12.1.3** (`@nestjs/core`, 2026-10-12); v11 = legacy line (11.2.7) | v12: core packages ship as ESM (CJS apps still work via `require(esm)`), Standard Schema validation (`StandardSchemaValidationPipe`, `schema` option on `@Body()`/`@Query()`/`@Param()`), `@nestjs/observe`, requires Node 20.19+ / 22.12+. `@nestjs/platform-express` 12 uses Express 5.2.x; `@nestjs/platform-fastify` uses Fastify 5.12.x. Rspack default for monorepos; oxlint in generated projects. |
| MongoDB server | **9.0** (9.0.0 released 2026-09-28; current stable series). Previous: 8.3, 8.0, 7.0 | 9.0: `$accumulator`/`$function`/`$where` un-deprecated (WebAssembly engine); per-operation memory limit; `maxConcurrentMultiDocumentTransactions` default 10000; `constraint` validation level; Queryable Encryption prefix/suffix/substring GA; `$queryStats` on by default. Minor releases (X.Y) from 9.0 only on Atlas; annual "Feature Update" X.5 release for self-managed. Majors supported 5 years. |
| MongoDB Node.js driver | **7.7.0** | |
| Mongoose | **9.11.1** (8.x line = 8.24.5) | Node >= 20.19. See Mongoose 9 breaking changes below. |
| PostgreSQL | **18** (latest minor 18.6, 2026-08-13). PostgreSQL 19 is in **beta (Beta 4, 2026-09-24)** — not GA. | PG 14 EOL 2026-11-12. |
| SQL | ISO/IEC 9075 (SQL:2023 is latest edition) | Teach portable SQL; label PostgreSQL-specific syntax. |
| Drizzle ORM | **0.45.4 stable** (`latest` tag, 2026-10-08); drizzle-kit **0.31.11**. **v1.0 is still a release candidate (npm `rc` tag 1.0.0-rc.4; rc.5 builds exist)** — NOT stable. | Teach 0.45 APIs as current stable; mention v1 RC changes (defineRelations, RQB v2) labelled as `preview`. |
| Redis | **Redis Open Source 8.10** (8.10.2, 2026-09-17). 8.2 = Extended support (EOL 2030-09-01); 8.0 EOL 2026-12-01. | Redis 8 = Redis Open Source with Query Engine, JSON, time series, probabilistic types and Vector Sets built in; AGPLv3 added as a license option (Redis 8.0, May 2025) alongside RSALv2/SSPLv1. Node clients: `redis` (node-redis) **6.3.0**, `ioredis` **6.0.0**. Valkey is the Linux Foundation BSD fork (from Redis 7.2.4). |
| pgvector | **0.8.7** (2026-10-01) | 0.8.0 added iterative index scans; halfvec/sparsevec since 0.7.0; HNSW and IVFFlat indexes. |
| Docker Engine | **29.9.0** (2026-10-08) | Docker Compose **v5.6.0** (2026-10-02). The top-level `version:` key in compose files is obsolete (ignored, warns). Use `docker compose` (plugin), not legacy `docker-compose` v1 (Python, EOL 2023). BuildKit is the default builder. |
| NGINX | Mainline **1.31.6**, Stable **1.30.5** (legacy 1.28.x) | Even minor = stable branch, odd = mainline. NGINX recommends mainline for most users. |
| AWS | Service-based (no single version) | Lambda Node.js runtimes: `nodejs24.x` (GA, deprecation 2028-04-30), `nodejs22.x` (deprecation 2027-04-30), `nodejs26.x` (public preview, not for production). Amazon Linux 2 reached end of support 2026-06-30 → use Amazon Linux 2023. AWS SDK for JavaScript v3 (modular `@aws-sdk/client-*`, e.g. client-s3 3.1149.0); SDK v2 is end-of-support (Sept 2025). |
| TypeScript | **7.0.2** (native Go compiler "tsgo", ~10x faster) | TS 6.0 was the last JS-based compiler release. |
| Other npm (for code examples) | zod 4.6.6, helmet 8.x, express-rate-limit 8.x, multer 2.x, jsonwebtoken 9.x, pg 8.23, Prisma 7.10, Vite 8.3, ESLint 10.x (flat config only) | |

## ECMAScript features by year (for JS questions)
- ES2022: class fields/private `#x`, static blocks, top-level await (modules), `.at()`, `Object.hasOwn`, `Error.cause`.
- ES2023: `findLast`/`findLastIndex`, change-array-by-copy (`toSorted`, `toReversed`, `toSpliced`, `with`), hashbang.
- ES2024: `Object.groupBy`/`Map.groupBy`, `Promise.withResolvers`, `/v` flag, resizable ArrayBuffer, `Atomics.waitAsync`, well-formed Unicode strings.
- ES2025: Iterator helpers (`.map/.filter/.take/.drop/.flatMap/.reduce/.toArray` on iterators), Set methods (`union`, `intersection`, `difference`, `symmetricDifference`, `isSubsetOf`...), `Promise.try`, `RegExp.escape`, JSON modules + import attributes (`import data from './x.json' with { type: 'json' }`), regex modifiers, duplicate named capture groups, `Float16Array`.
- ES2026 (approved 2026-06-30): `Math.sumPrecise`, `Iterator.concat`, `Array.fromAsync`, `Error.isError`, Map/WeakMap upsert (`getOrInsert`, `getOrInsertComputed`), `Uint8Array` base64/hex (`toBase64`, `fromBase64`, `toHex`, `fromHex`), `JSON.parse` source text access + `JSON.rawJSON`.
- NOT in the standard yet / not Baseline: Temporal (shipped in Chrome 144 & Firefox 139, not Safari → not Baseline), explicit resource management `using` (Chrome 134, Firefox 141; not Safari). Label these `experimental`/limited support if mentioned. Decorators: TC39 stage 3 (TypeScript implements them) — not in ECMAScript yet.

## Baseline status of selected web features (web-features 3.42.0)
- Baseline **Widely available**: container size queries, `:has()`, CSS nesting, cascade layers (`@layer`), `<dialog>`, subgrid, `color-mix()`, oklab/oklch, `structuredClone`, `Array.fromAsync`, `Promise.withResolvers`, `Object.groupBy`.
- Baseline **Newly available**: popover (2025-01), View Transitions same-document (2025-10), invoker commands `command`/`commandfor` (2025-12), `@scope` (2026-03), container style queries (2026-05), `field-sizing` (2026-06), `@starting-style`, `light-dark()`, `text-wrap: balance`, `content-visibility`, `<details name>` exclusive accordions, `sibling-count()/sibling-index()` (2026-08), `shape()` (2026-02), Iterator helpers, Set methods, `Uint8Array` base64/hex, `Math.sumPrecise` (2026-04), `Iterator.concat` (2026-03).
- **Not Baseline yet (limited availability)**: CSS anchor positioning (missing in a major engine), scroll-driven animations, customizable `<select>` (`appearance: base-select`), cross-document view transitions, CSS `if()`, `interestfor` (interest invokers), `<dialog closedby>`, `calc-size()`/`interpolate-size`, Temporal, `using`.

## React 19.x facts
- React 19.0 (Dec 2024): Actions, `useActionState`, `useFormStatus`, `useOptimistic`, `use()`, `ref` as a prop (forwardRef no longer needed for function components), `<Context>` as provider, document metadata (`<title>`, `<meta>` hoisting), stylesheet/script support, Server Components & Server Actions stable for frameworks. Removed: `propTypes` checks & `defaultProps` for function components, string refs, legacy context, `ReactDOM.render` / `hydrate` (use `createRoot` / `hydrateRoot`), `react-test-renderer/shallow`.
- React 19.1 (Mar 2025): Owner stack, Suspense improvements.
- React 19.2 (2025-10-01): `<Activity mode="visible|hidden">`, `useEffectEvent`, `cacheSignal` (RSC), Partial Pre-rendering APIs, Performance Tracks in DevTools, batching of Suspense boundary reveals for SSR.
- React 19.3 (2026-09-09): `<ViewTransition>` + `addTransitionType` **stable**; Fragment Refs (`<Fragment ref>` → `FragmentInstance`) **stable**; `browser()` from `react-dom` (`use(browser())` to opt a subtree out of SSR); Trusted Types support; Server Components can render `<Context value>` directly. Transitions render independently.
- React Compiler 1.0 (2025-10-07): automatic memoization; reduces need for manual `useMemo`/`useCallback`/`React.memo` (still valid APIs). Next.js 16 `reactCompiler: true` stable option.
- Create React App is deprecated (Feb 2025) → use a framework (Next.js, React Router v7 framework mode) or Vite.
- Security: React blog posts on 2025-12-03 (critical RSC vulnerability) and 2025-12-11 (DoS & source-code exposure in RSC) → keep React/Next.js patched; Next.js announced another out-of-band security release for 2026-10-14.

## Next.js 16.x facts
- `proxy.ts` (export `proxy` function) replaces `middleware.ts` (deprecated; middleware still available only for Edge runtime use cases). `proxy.ts` runs on the **Node.js runtime**.
- Request APIs are async only: `await params`, `await searchParams`, `await cookies()`, `await headers()`, `await draftMode()`.
- Cache Components (`cacheComponents: true` in next.config): `'use cache'` directive (file/component/function), `cacheLife('hours')`, `cacheTag('x')`; dynamic by default, caching is opt-in. 16.4 recommends Cache Components for every app; new `create-next-app` apps enable it by default; it becomes the default in Next 17. 16.4 adds `export const ensureStatic = 'navigation' | 'prefetch' | 'shell'`, `navigation()` / `prefetch()` from `next/cache`, and `partialPrefetching: true`.
- `revalidateTag(tag, profile)` — second arg (`'max'`, `'hours'`, `{ expire: n }`) required for SWR; single-arg form deprecated. `updateTag(tag)` (Server Actions only, read-your-writes). `refresh()` (Server Actions only, refreshes uncached data). `revalidatePath()` still exists.
- Turbopack is the default bundler for dev and build (`--webpack` to opt out). React Compiler support stable (`reactCompiler: true`, not default).
- Removed in 16: AMP, `next lint` (use ESLint/Biome directly), `serverRuntimeConfig`/`publicRuntimeConfig` (use env vars), `experimental.ppr` / `experimental.dynamicIO` (→ `cacheComponents`). Parallel route slots require `default.js`. `images.domains` deprecated → `images.remotePatterns`. `next/legacy/image` deprecated.
- Min Node.js 20.9; TypeScript 5.1+; browsers Chrome/Edge/Firefox 111+, Safari 16.4+.
- Legacy (pre-Cache-Components) App Router behaviour: `export const revalidate = 60`, `fetch(url, { next: { revalidate, tags } })`, `export const dynamic = 'force-dynamic'`, `unstable_cache` — still exists when Cache Components is off; label as "previous model" when discussing. In Next 15+ `fetch` is NOT cached by default (changed from Next 14).
- Pages Router still supported: `getServerSideProps`, `getStaticProps`, `getStaticPaths`, ISR via `revalidate` returned from getStaticProps, API routes in `pages/api`.

## Node.js facts
- Type stripping (run `.ts` directly; erasable syntax only — no enums, no runtime namespaces, no parameter properties) became **stable** in v25.2.0 / v24.12.0; enabled by default since v23.6 / v22.18.
- `require(esm)` works by default (v22.12+/v20.19+) for synchronous ES modules.
- Built-ins: `fetch`, `WebSocket` client (v22+ stable), `node:test` test runner, `--watch`, `--env-file=.env`, `node:sqlite` (stable? check docs; label experimental unless verified), permission model `--permission` (stable since v23.5/v22.13… verify before claiming), `AsyncLocalStorage`, `worker_threads`, `node:cluster`, `process.loadEnvFile()`, `util.parseArgs`, `util.styleText`, `URL.parse`.
- npm 11 ships with Node 24+.

## Express 5 facts (vs 4)
- Rejected promises / thrown errors in async handlers are automatically forwarded to `next(err)`.
- path-to-regexp v8 syntax: wildcard must be named `/*splat` (match root too: `/{*splat}`), optional segments use braces `/:file{.:ext}`, no `?` optional params, no regex chars in path strings; `app.all('*')` → `app.all('/*splat')`.
- Removed: `app.del` (use `app.delete`), `req.param()`, `res.sendfile` (→ `res.sendFile`), `res.send(status)` number-only bodies (→ `res.sendStatus`), `res.json(obj, status)` signature (→ `res.status(s).json(obj)`), `res.redirect('back')` magic string (→ `req.get('Referrer') || '/'`), `app.router` object, pluralized `req.acceptsCharset` etc.
- `req.body` is `undefined` (not `{}`) when no body parser ran; `req.query` is a getter and read-only; default query parser is `'simple'` (not `'extended'`).
- `express.urlencoded` `extended` defaults to `false`. Brotli supported. `res.status()` only accepts integers 100–999.
- Node.js 18+.
- Ecosystem: `helmet` for security headers, `cors`, `express-rate-limit`, `multer` 2.x for uploads (several 2025–2026 security releases → keep patched), `csurf` is deprecated (2025) — use SameSite cookies + CSRF tokens via maintained libs.

## Mongoose 9 breaking changes (vs 8)
- Pre middleware no longer receives `next()` — use `async function () {}` or return a promise. `isAsync` (`function(next, done)`) middleware removed.
- Callbacks removed everywhere (since v7 for most APIs; v9 removed remaining: `doValidate()` returns a promise, `Document.prototype.updateOne` no callback).
- Update pipelines disabled by default (`{ updatePipeline: true }` or `mongoose.set('updatePipeline', true)`).
- `findOneAndUpdate(filter, update, { new: true })` → prefer `{ returnDocument: 'after' }` (`new`/`returnOriginal` deprecated since 9.2).
- `isValidObjectId(6)` → false; `new ObjectId(6)` throws. UUIDs returned as `bson.UUID` instances.
- `background` index option removed. TypeScript: `FilterQuery` renamed `QueryFilter`.
- Node >= 20.19; uses MongoDB driver 7.x. `strictQuery` default false since Mongoose 7.
- Known: with MongoDB 9.0, `syncIndexes()` may rebuild unchanged indexes unless Mongoose ≥ 9.10.4 / 8.24.5.

## PostgreSQL 18 features (2025-09-25)
- Asynchronous I/O subsystem (`io_method`), B-tree **skip scan**, `uuidv7()`, **virtual generated columns are the default** (`STORED` optional), `OLD`/`NEW` in `RETURNING` for INSERT/UPDATE/DELETE/MERGE, temporal constraints (`WITHOUT OVERLAPS`, `PERIOD`), OAuth authentication, planner stats kept across `pg_upgrade`, data checksums on by default, **MD5 password auth deprecated** (use SCRAM-SHA-256), `EXPLAIN ANALYZE` includes BUFFERS automatically.
- PG 17 (2024): incremental backups (`pg_basebackup --incremental`), `JSON_TABLE`, SQL/JSON constructors, `MERGE ... RETURNING`, improved VACUUM memory.
- PG 16: logical replication from standbys, `pg_stat_io`. PG 15: `MERGE`, `UNIQUE NULLS NOT DISTINCT`.

## Docker facts
- Compose file: `compose.yaml` preferred; top-level `version` obsolete; `depends_on` with `condition: service_healthy`; `develop.watch` (Compose Watch); profiles; secrets.
- BuildKit default; `# syntax=docker/dockerfile:1`; cache mounts `RUN --mount=type=cache`; secret mounts `RUN --mount=type=secret`; multi-stage builds; `.dockerignore`; `HEALTHCHECK`; `USER node`; distroless/alpine/slim trade-offs; `docker init`; `docker scout` for CVEs; `docker buildx` multi-platform.

## Redis facts
- Data types: strings, hashes, lists, sets, sorted sets, streams, bitmaps, HyperLogLog, geospatial, JSON, Vector Sets (8.0+), time series, probabilistic (Bloom, Cuckoo, Count-min, Top-K, t-digest).
- Redis 7.4+/8: hash field expiration (`HEXPIRE`, `HPEXPIRE`, `HTTL`, `HGETEX`/`HSETEX` in 8.0).
- Eviction policies: `noeviction` (default), `allkeys-lru`, `allkeys-lfu`, `volatile-*`, `allkeys-random`, `volatile-ttl`.
- Persistence: RDB snapshots, AOF (`appendfsync everysec` default), hybrid; Redis 7+ multi-part AOF.
- Distributed locks: `SET key value NX PX 30000` + compare-and-delete via Lua; Redlock controversy (Kleppmann) — use fencing tokens for correctness.
- node-redis v5+/v6: `import { createClient } from 'redis'; const client = await createClient({ url }).on('error', ...).connect();` commands are promise-based camelCase (`client.hSet`, ...). In node-redis v6 the SET TTL option is `{ expiration: { type: 'EX', value: 60 } }`; the older `{ EX: 60 }` shorthand is deprecated.

## NGINX facts
- NGINX ≥ 1.29.7 (so 1.30 stable): upstream keepalive on by default (`keepalive 32 local`), `proxy_http_version` defaults to 1.1, `Connection` no longer sent upstream — the old `proxy_http_version 1.1; proxy_set_header Connection "";` recipe is only needed on ≤ 1.28. WebSocket proxying still needs the Upgrade/Connection map. (Verified in nginx.org CHANGES during content writing.)
- `proxy_pass`, `upstream` (round-robin default, `least_conn`, `ip_hash`, `hash ... consistent`), `proxy_set_header Host $host; X-Real-IP; X-Forwarded-For $proxy_add_x_forwarded_for; X-Forwarded-Proto $scheme`.
- WebSocket: `proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection $connection_upgrade;` (map block).
- `listen 443 ssl;` + `http2 on;` (the `http2` parameter on `listen` is deprecated since 1.25.1). HTTP/3 via `listen 443 quic reuseport;` + `http3 on;`.
- `limit_req_zone` / `limit_req`, `limit_conn`, `client_max_body_size` (default 1m → 413), `proxy_read_timeout` (default 60s → 504 on upstream timeout), 502 = bad gateway (upstream refused/crashed/closed), `proxy_cache_path`, `gzip on;`, `try_files $uri $uri/ /index.html;` for SPAs, `nginx -t`, `nginx -s reload`.

## AWS facts
- IAM: prefer roles + temporary credentials (STS), IAM Identity Center for humans, least privilege, no long-lived access keys on EC2 (use instance profiles), MFA; SCPs in Organizations; IMDSv2 required by default on new instances.
- S3: Block Public Access on and ACLs disabled by default for new buckets (since April 2023), SSE-S3 encryption by default (since Jan 2023), strong read-after-write consistency (since Dec 2020), presigned URLs, lifecycle rules, storage classes, versioning, CloudFront OAC (Origin Access Control; OAI is legacy).
- RDS/Aurora Multi-AZ, read replicas, automated backups + PITR; RDS Proxy for Lambda connection pooling.
- ECS (Fargate / EC2), ECR, ALB (L7) vs NLB (L4), Auto Scaling target tracking, Route 53 routing policies, CloudWatch Logs/Metrics/Alarms, X-Ray, Secrets Manager (rotation) vs SSM Parameter Store (SecureString, cheaper), Well-Architected Framework (6 pillars incl. Sustainability).
- Lambda: Node 24 GA runtime; SnapStart for Java/Python/.NET; response streaming; 15-min max timeout; 10 GB memory max; provisioned concurrency.

## Interview market research notes (for `market` and `priority`)
- Bangladesh: Public interview reviews (e.g., Glassdoor Brain Station 23, 2023–2024) describe aptitude/online MCQ tests (OOP, DBMS fundamentals, DSA, output tracing, SDLC), coding tests with easy/medium LeetCode-style problems, then a technical "viva". A dev.to article on "JavaScript interview questions for the Bangladesh job market" emphasises fundamentals: var/let/const, hoisting, closures, `this`, call/apply/bind, event loop, promises, Promise.all vs race, DOM events/bubbling, ES6 features and string/array coding problems. BD job posts (e.g., LinkedIn, 2026) for MERN/NestJS full-stack roles list Node/Express/NestJS, React/Next.js, MongoDB/PostgreSQL/MySQL, ORMs (Mongoose/Prisma/TypeORM), JWT/RBAC auth, Redis caching, Docker/AWS/CI-CD as nice-to-have.
- International: Stack Overflow Developer Survey 2025 (professional developers): Docker 73.8%, JavaScript 68.8%, PostgreSQL 58.2%, Node.js 49.1%, React 46.9%, AWS 45.9%, MySQL 39.6%, Redis 30.7%, MongoDB 24.3%, Next.js 21.5%, Express 20.3%, NestJS 7.4%. International/remote interviews more often include system design, scalability, production debugging, cloud architecture and trade-off discussions.
- Use `market: "both"` by default. Use `"bangladesh"` only for question styles specifically reported for BD hiring (written MCQ/output-tracing fundamentals, viva-style definitions, MERN/NestJS stack combos typical of BD job posts). Use `"international"` for deeper system-design / large-scale / cloud-architecture questions typical of international or remote senior roles. Never claim exact frequencies.
