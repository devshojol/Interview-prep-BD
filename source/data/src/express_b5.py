import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

EX_WRITING_MW = ("Express — Writing middleware", "https://expressjs.com/en/guide/writing-middleware.html")
NODE_HTTP = ("Node.js API — HTTP (response 'finish' / 'close')", "https://nodejs.org/api/http.html")
NODE_PROCESS = ("Node.js API — process.hrtime.bigint()", "https://nodejs.org/api/process.html")
PG_LIMIT = ("PostgreSQL — LIMIT and OFFSET", "https://www.postgresql.org/docs/current/queries-limit.html")
OWASP_SQLI = ("OWASP — SQL Injection Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html")
ZOD_API = ("Zod — Defining schemas", "https://zod.dev/api")
EX_ROUTING = ("Express — Routing (express.Router)", "https://expressjs.com/en/guide/routing.html")
RFC_8594 = ("RFC 8594 — The Sunset HTTP Header Field", "https://www.rfc-editor.org/rfc/rfc8594")
RFC_9745 = ("RFC 9745 — The Deprecation HTTP Response Header Field", "https://www.rfc-editor.org/rfc/rfc9745")
EX_MIGRATE5 = ("Express — Migrating to Express 5", "https://expressjs.com/en/guide/migrating-5.html")
EX_API5 = ("Express 5.x — API reference", "https://expressjs.com/en/5x/api.html")
NODE_RELEASES = ("Node.js — Releases", "https://nodejs.org/en/about/previous-releases")
IETF_IDEMPOTENCY = ("IETF HTTPAPI WG draft (expired) — The Idempotency-Key HTTP Header Field", "https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/")
MDN_IDEMPOTENT = ("MDN — Idempotent", "https://developer.mozilla.org/en-US/docs/Glossary/Idempotent")
PG_INSERT = ("PostgreSQL — INSERT (ON CONFLICT)", "https://www.postgresql.org/docs/current/sql-insert.html")

QUESTIONS = [
    # ------------------------------------------------------------------ express-027
    Q(
        id="express-027", sub="Logging", diff="easy", type="coding",
        prio="high", market="bangladesh", mins=5,
        tags=["middleware", "logging", "response-time", "finish-event", "coding"],
        ver="Express 5.x; Node.js 24 LTS / 26", vs=False, status="stable",
        q_en=r"""
            Write an Express middleware `requestTimer` that logs one line per request **when the response has been sent**: method, original URL, status code and duration in milliseconds — for example `GET /api/products?page=2 200 16.5ms`. If the client disconnects before the response is finished, log an "aborted" line instead.
        """,
        q_bn=r"""
            একটি Express middleware `requestTimer` লেখো, যা **response পাঠানো হয়ে গেলে** প্রতি request-এ একটি লাইন log করবে: method, original URL, status code আর millisecond-এ সময় — যেমন `GET /api/products?page=2 200 16.5ms`। Response শেষ হওয়ার আগেই client disconnect করলে বদলে একটি "aborted" লাইন log করবে।
        """,
        a_en=r"""
            Record a start time with `process.hrtime.bigint()`, then listen to the response's events and call `next()` immediately:

            - `res.on('finish')` fires when the response has been fully handed to the OS — that's when status code and duration are final.
            - `res.on('close')` fires when the underlying connection closes; if `res.writableFinished` is still `false` at that point, the client went away before we finished, so I log it as aborted.

            I can't just measure after `next()` returns, because route handlers are usually asynchronous — `next()` returns long before the response is sent. I register the middleware first so it measures everything after it, and use `req.originalUrl` because routers rewrite `req.url` for mounted paths.
        """,
        a_bn=r"""
            `process.hrtime.bigint()` দিয়ে শুরুর সময় রেকর্ড করি, তারপর response-এর event-এ listen করি এবং সাথে সাথে `next()` call করি:

            - `res.on('finish')` fire হয় যখন response পুরোপুরি OS-এর হাতে তুলে দেওয়া হয়েছে — তখনই status code আর সময় চূড়ান্ত।
            - `res.on('close')` fire হয় যখন নিচের connection বন্ধ হয়; তখনও `res.writableFinished` `false` থাকলে বুঝি আমরা শেষ করার আগেই client চলে গেছে, তাই aborted হিসেবে log করি।

            শুধু `next()` return করার পর সময় মাপা যায় না, কারণ route handler সাধারণত asynchronous — response পাঠানোর অনেক আগেই `next()` return করে। Middleware-টা সবার আগে register করি যাতে এর পরের সবকিছু মাপা হয়, আর `req.originalUrl` ব্যবহার করি কারণ mount করা path-এ router `req.url` বদলে দেয়।
        """,
        ex_en=r"""
            - **Why `hrtime.bigint()` and not `Date.now()`:** it's monotonic and high-resolution, so clock adjustments (NTP) can't produce negative or wrong durations. `performance.now()` works too.
            - **`finish` then `close`:** for a normal response both events fire, in that order; checking `writableFinished` in `close` avoids double logging.
            - **Production:** use a structured logger such as `pino-http`, which logs method, URL, status and `responseTime` as JSON fields, adds request IDs, and logs aborted requests — but this exercise shows how it works underneath.
            - **Don't log sensitive data:** query strings can contain tokens or emails; redact or drop them if needed.
            - **Want the timing in a response header?** It has to be set *before* headers are sent (e.g. a `Server-Timing` header set by the handler), not in `finish`.
            - Verified on Express 5.3: a normal request logs `200 16.5ms`, an unknown route logs `404`, and a client timeout logs the aborted line.
        """,
        ex_bn=r"""
            - **`Date.now()` না হয়ে `hrtime.bigint()` কেন:** এটা monotonic আর high-resolution, তাই clock adjustment (NTP) negative বা ভুল সময় দেখাতে পারে না। `performance.now()`-ও চলে।
            - **আগে `finish`, তারপর `close`:** স্বাভাবিক response-এ দুটো event-ই এই ক্রমে fire হয়; `close`-এ `writableFinished` check করলে দুবার log হয় না।
            - **Production:** `pino-http`-এর মতো structured logger ব্যবহার করো, যা method, URL, status আর `responseTime` JSON field হিসেবে log করে, request ID যোগ করে, আর aborted request-ও log করে — তবে এই exercise দেখায় ভেতরে এটা কীভাবে কাজ করে।
            - **Sensitive data log কোরো না:** query string-এ token বা email থাকতে পারে; দরকার হলে redact করো বা বাদ দাও।
            - **সময়টা response header-এ চাও?** সেটা header পাঠানোর *আগেই* set করতে হবে (যেমন handler-এর set করা `Server-Timing` header), `finish`-এ নয়।
            - Express 5.3-এ যাচাই করা: স্বাভাবিক request log করে `200 16.5ms`, অজানা route log করে `404`, আর client timeout হলে aborted লাইন log হয়।
        """,
        tip_en=r"""Explain why you listen to `finish` instead of measuring after `next()` — that's the insight the question is really testing.""",
        tip_bn=r"""ব্যাখ্যা করো কেন `next()`-এর পরে না মেপে `finish`-এ listen করছ — প্রশ্নটা আসলে এই উপলব্ধিটাই পরীক্ষা করে।""",
        mist_en=r"""Logging right after `next()` (async handlers haven't responded yet), forgetting to call `next()` (every request hangs), or registering the timer after the routes.""",
        mist_bn=r"""`next()`-এর ঠিক পরে log করা (async handler তখনও response দেয়নি), `next()` call করতে ভুলে যাওয়া (সব request ঝুলে থাকে), অথবা route-এর পরে timer register করা।""",
        code=r"""
            export function requestTimer(req, res, next) {
              const start = process.hrtime.bigint();
              const elapsedMs = () => (Number(process.hrtime.bigint() - start) / 1e6).toFixed(1);

              res.on('finish', () => {
                console.log(`${req.method} ${req.originalUrl} ${res.statusCode} ${elapsedMs()}ms`);
              });

              res.on('close', () => {
                if (!res.writableFinished) {
                  console.warn(`${req.method} ${req.originalUrl} aborted by client after ${elapsedMs()}ms`);
                }
              });

              next(); // don't block the request while we wait for the response
            }

            // Register first so it measures everything that follows
            app.use(requestTimer);
        """,
        lang="javascript",
        time="O(1) per request", space="O(1) per request",
        follow=[
            ("How would you add a request ID to each log line?", "প্রতিটি log line-এ request ID কীভাবে যোগ করবে?"),
            ("How would you turn these logs into p95/p99 latency metrics?", "এই log থেকে কীভাবে p95/p99 latency metric বানাবে?"),
        ],
        related=["express-001", "express-025"],
        refs=[EX_WRITING_MW, NODE_HTTP, NODE_PROCESS],
    ),
    # ------------------------------------------------------------------ express-028
    Q(
        id="express-028", sub="Pagination, Filtering & Sorting", diff="medium", type="coding",
        prio="high", market="both", mins=10,
        tags=["pagination", "filtering", "sorting", "sql-injection", "postgresql", "zod"],
        ver="Express 5.x; zod 4.x; node-postgres 8.x", vs=False, status="stable",
        q_en=r"""
            Implement `GET /api/products` backed by PostgreSQL with:

            - pagination: `page` (default 1) and `limit` (default 20, max 100);
            - filters: `category`, `minPrice`, `maxPrice`;
            - sorting: `sort` = `price`, `-price`, `createdAt` or `-createdAt` (default `-createdAt`);
            - response: `{ data, page, limit, total, totalPages }`.

            Example: `GET /api/products?category=books&minPrice=100&sort=-price&page=2`. Invalid input must return `400`, and no user input may be concatenated into SQL unsafely.
        """,
        q_bn=r"""
            PostgreSQL-ভিত্তিক `GET /api/products` implement করো, যাতে থাকবে:

            - pagination: `page` (default 1) আর `limit` (default 20, max 100);
            - filter: `category`, `minPrice`, `maxPrice`;
            - sorting: `sort` = `price`, `-price`, `createdAt` বা `-createdAt` (default `-createdAt`);
            - response: `{ data, page, limit, total, totalPages }`।

            উদাহরণ: `GET /api/products?category=books&minPrice=100&sort=-price&page=2`। ভুল input-এ `400` দিতে হবে, আর কোনো user input অনিরাপদভাবে SQL-এ জোড়া লাগানো যাবে না।
        """,
        a_en=r"""
            Three rules make this safe:

            1. **Validate and coerce the query first** with a zod schema: numbers coerced, `limit` capped at 100, `sort` restricted to an enum, `minPrice <= maxPrice`. A `ZodError` goes to the error handler as `400`.
            2. **Values go into placeholders** (`$1`, `$2`…): filters are added to a `WHERE` list while pushing their values into a `params` array.
            3. **Identifiers come from a whitelist.** Column names and sort direction can't be parameterised, so the `sort` key maps to a fixed `ORDER BY` fragment — user text never reaches the SQL string. I add `id` as a tie-breaker so ordering is deterministic across pages.

            Then I run the page query (`LIMIT`/`OFFSET` as parameters) and a `count(*)` with the same filters in parallel, and compute `totalPages`.
        """,
        a_bn=r"""
            তিনটি নিয়ম এটাকে নিরাপদ করে:

            1. **আগে query validate ও coerce করা** zod schema দিয়ে: number coerce, `limit` সর্বোচ্চ 100, `sort` একটি enum-এ সীমিত, `minPrice <= maxPrice`। `ZodError` error handler-এ গিয়ে `400` হয়।
            2. **Value যায় placeholder-এ** (`$1`, `$2`…): filter-গুলো একটি `WHERE` list-এ যোগ হয়, আর তাদের value `params` array-তে push হয়।
            3. **Identifier আসে whitelist থেকে।** Column-এর নাম আর sort direction parameterise করা যায় না, তাই `sort` key একটি নির্দিষ্ট `ORDER BY` অংশে map হয় — user-এর লেখা কখনো SQL string-এ পৌঁছায় না। Page-জুড়ে ordering নির্ধারিত রাখতে tie-breaker হিসেবে `id` যোগ করি।

            তারপর page query (`LIMIT`/`OFFSET` parameter হিসেবে) আর একই filter সহ `count(*)` parallel-এ চালাই, এবং `totalPages` হিসাব করি।
        """,
        ex_en=r"""
            - **Offset vs cursor (keyset) pagination:** `OFFSET 100000` makes the database read and discard 100k rows, and rows can be duplicated or skipped when data changes between page loads. For infinite scroll or large tables, use a cursor: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT $3`, returning the last row's values as `nextCursor`. Offset is fine for small admin tables where users jump to page N.
            - **`count(*)` can be expensive** on big tables; consider caching it, using an estimate, or dropping `total` with cursor pagination.
            - **Indexes:** support the common filter + sort combination, e.g. `(category, price)` or `(created_at, id)`.
            - **Express 5 query parsing:** with the default `simple` parser, `?category=a&category=b` becomes an array and the string schema rejects it (`400`) — decide explicitly whether to support multi-value filters.
            - Verified with a recording fake pool: the example request produces `WHERE category = $1 AND price >= $2 ORDER BY price DESC, id DESC LIMIT $3 OFFSET $4` with params `['books', 100, 20, 20]`, and `sort=name;DROP TABLE products` returns `400`.
        """,
        ex_bn=r"""
            - **Offset বনাম cursor (keyset) pagination:** `OFFSET 100000` দিলে database 100k row পড়ে ফেলে দেয়, আর page load-এর মাঝে data বদলালে row duplicate বা বাদ পড়তে পারে। Infinite scroll বা বড় table-এর জন্য cursor ব্যবহার করো: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT $3`, আর শেষ row-এর value `nextCursor` হিসেবে ফেরত দাও। যেখানে user সরাসরি page N-এ যায় এমন ছোট admin table-এ offset ঠিক আছে।
            - **বড় table-এ `count(*)` ব্যয়বহুল** হতে পারে; cache করা, estimate ব্যবহার করা, বা cursor pagination-এ `total` বাদ দেওয়া বিবেচনা করো।
            - **Index:** প্রচলিত filter + sort সমন্বয়কে support করো, যেমন `(category, price)` বা `(created_at, id)`।
            - **Express 5-এর query parsing:** default `simple` parser-এ `?category=a&category=b` array হয়ে যায় আর string schema সেটা reject করে (`400`) — multi-value filter support করবে কি না স্পষ্টভাবে ঠিক করো।
            - Recording fake pool দিয়ে যাচাই করা: উদাহরণের request তৈরি করে `WHERE category = $1 AND price >= $2 ORDER BY price DESC, id DESC LIMIT $3 OFFSET $4`, params `['books', 100, 20, 20]`, আর `sort=name;DROP TABLE products` দিলে `400` আসে।
        """,
        tip_en=r"""Say the key sentence early: "values are parameterised, identifiers are whitelisted". Then mention cursor pagination as the scalable alternative — interviewers almost always ask about it next.""",
        tip_bn=r"""মূল বাক্যটা শুরুতেই বলো: "value parameterise করা, identifier whitelist করা"। তারপর scalable বিকল্প হিসেবে cursor pagination-এর কথা বলো — interviewer প্রায় সবসময় পরের প্রশ্ন এটাই করে।""",
        mist_en=r"""Interpolating `req.query.sort` into `ORDER BY`, not capping `limit` (`?limit=1000000`), or sorting without a unique tie-breaker so rows jump between pages.""",
        mist_bn=r"""`req.query.sort` সরাসরি `ORDER BY`-তে বসিয়ে দেওয়া, `limit`-এর সীমা না রাখা (`?limit=1000000`), অথবা unique tie-breaker ছাড়া sort করা, ফলে row এক page থেকে আরেক page-এ লাফায়।""",
        code=r"""
            import { z } from 'zod';
            import { pool } from './db.js';

            const SORTS = { // whitelist: user input never reaches the SQL text
              price: 'price ASC, id ASC',
              '-price': 'price DESC, id DESC',
              createdAt: 'created_at ASC, id ASC',
              '-createdAt': 'created_at DESC, id DESC',
            };

            const listQuery = z
              .object({
                page: z.coerce.number().int().min(1).default(1),
                limit: z.coerce.number().int().min(1).max(100).default(20),
                category: z.string().trim().min(1).max(50).optional(),
                minPrice: z.coerce.number().nonnegative().optional(),
                maxPrice: z.coerce.number().nonnegative().optional(),
                sort: z.enum(Object.keys(SORTS)).default('-createdAt'),
              })
              .refine((q) => q.minPrice === undefined || q.maxPrice === undefined || q.minPrice <= q.maxPrice, {
                message: 'minPrice must be <= maxPrice',
                path: ['minPrice'],
              });

            app.get('/api/products', async (req, res) => {
              const q = listQuery.parse(req.query); // ZodError -> 400 in the error handler

              const where = [];
              const params = [];
              const addFilter = (sql, value) => {
                params.push(value);
                where.push(`${sql} $${params.length}`);
              };
              if (q.category) addFilter('category =', q.category);
              if (q.minPrice !== undefined) addFilter('price >=', q.minPrice);
              if (q.maxPrice !== undefined) addFilter('price <=', q.maxPrice);
              const whereSql = where.length ? `WHERE ${where.join(' AND ')}` : '';

              const offset = (q.page - 1) * q.limit;
              const [page, count] = await Promise.all([
                pool.query(
                  `SELECT id, name, category, price, created_at
                     FROM products ${whereSql}
                    ORDER BY ${SORTS[q.sort]}
                    LIMIT $${params.length + 1} OFFSET $${params.length + 2}`,
                  [...params, q.limit, offset],
                ),
                pool.query(`SELECT count(*)::int AS total FROM products ${whereSql}`, params),
              ]);

              const total = count.rows[0].total;
              res.json({ data: page.rows, page: q.page, limit: q.limit, total, totalPages: Math.ceil(total / q.limit) });
            });
        """,
        lang="javascript",
        time="O(limit) rows returned; OFFSET makes the DB scan O(offset + limit)", space="O(limit)",
        follow=[
            ("Rewrite this endpoint with cursor-based pagination.", "এই endpoint-টি cursor-based pagination দিয়ে আবার লেখো।"),
            ("How would you support filtering by multiple categories safely?", "একাধিক category দিয়ে filter নিরাপদে কীভাবে support করবে?"),
        ],
        related=["express-012", "express-003"],
        refs=[OWASP_SQLI, PG_LIMIT, ZOD_API],
    ),
    # ------------------------------------------------------------------ express-029
    Q(
        id="express-029", sub="API Versioning", diff="medium", type="conceptual",
        prio="medium", market="both", mins=5,
        tags=["api-versioning", "deprecation", "sunset-header", "routers", "rest"],
        ver="Express 5.x; RFC 8594 / RFC 9745", vs=False, status="stable",
        q_en=r"""How would you version a public REST API built with Express, and how do you retire an old version without breaking clients?""",
        q_bn=r"""Express দিয়ে বানানো একটি public REST API-র versioning কীভাবে করবে, আর client-দের না ভেঙে পুরনো version কীভাবে বন্ধ করবে?""",
        a_en=r"""
            **Strategy:** I usually version in the **URL path** (`/v1/orders`, `/v2/orders`). It's explicit, easy to route, test, cache and document. Alternatives are a custom header (`Api-Version: 2`, or date-based versions) or media-type versioning (`Accept: application/vnd.example.v2+json`) — cleaner URLs, but harder to test in a browser and caches need `Vary` on that header.

            **When to bump:** only for **breaking** changes (removing or renaming fields, changing types or semantics). Adding optional fields or new endpoints is backward compatible and stays in the current version.

            **In Express:** each version is its own `express.Router()` mounted with `app.use('/v1', v1Router)` and `app.use('/v2', v2Router)`. Versions share services and repositories; v2 can reuse v1 handlers for unchanged endpoints, so only the HTTP layer differs.

            **Retiring v1:** announce a timeline; send `Deprecation` (RFC 9745) and `Sunset` (RFC 8594) headers plus a `Link` to the migration guide; measure v1 traffic per client/API key and contact heavy users; optionally run short "brownouts"; after the sunset date return `410 Gone` with a helpful message.
        """,
        a_bn=r"""
            **কৌশল:** আমি সাধারণত **URL path**-এ version রাখি (`/v1/orders`, `/v2/orders`)। এটা স্পষ্ট, এবং route, test, cache ও document করা সহজ। বিকল্প হলো custom header (`Api-Version: 2`, বা তারিখ-ভিত্তিক version) অথবা media-type versioning (`Accept: application/vnd.example.v2+json`) — URL পরিষ্কার থাকে, কিন্তু browser-এ test করা কঠিন আর cache-এ ওই header-এর জন্য `Vary` লাগে।

            **কখন version বাড়াব:** শুধু **breaking** change-এর জন্য (field সরানো বা নাম বদলানো, type বা অর্থ বদলানো)। Optional field বা নতুন endpoint যোগ করা backward compatible, তাই current version-এই থাকে।

            **Express-এ:** প্রতিটি version নিজস্ব `express.Router()`, যা `app.use('/v1', v1Router)` আর `app.use('/v2', v2Router)` দিয়ে mount করা। Version-গুলো service আর repository share করে; অপরিবর্তিত endpoint-এর জন্য v2 v1-এর handler পুনরায় ব্যবহার করতে পারে, তাই শুধু HTTP layer আলাদা হয়।

            **v1 বন্ধ করা:** একটি সময়সূচি ঘোষণা করা; `Deprecation` (RFC 9745) আর `Sunset` (RFC 8594) header, সাথে migration guide-এর `Link` পাঠানো; client/API key অনুযায়ী v1 traffic মাপা এবং বেশি ব্যবহারকারীদের সাথে যোগাযোগ করা; চাইলে অল্প সময়ের "brownout" চালানো; sunset তারিখের পর সহায়ক message সহ `410 Gone` return করা।
        """,
        ex_en=r"""
            - **Avoid versioning by default for internal APIs** consumed only by your own frontend that deploys together with the backend — evolve compatibly instead.
            - **Contract discipline:** an OpenAPI spec per version plus contract tests in CI catch accidental breaking changes before they ship.
            - **Don't fork the business logic:** two copies of the domain code per version doubles bugs. Keep translation (request/response mapping) at the edge.
            - **Header formats:** `Deprecation` is a structured-field date like `@1790812800` (Unix seconds); `Sunset` is an HTTP date. RFC 9745 also defines a `deprecation` link relation for documentation links.
            - **Mobile clients** can't be force-upgraded instantly, so sunset windows for public/mobile APIs are usually months, not weeks.
        """,
        ex_bn=r"""
            - **Internal API-তে default-ভাবে versioning এড়াও**, যা শুধু তোমার নিজের frontend ব্যবহার করে এবং backend-এর সাথে একসাথে deploy হয় — বরং compatible উপায়ে বদলাও।
            - **Contract শৃঙ্খলা:** প্রতিটি version-এর জন্য একটি OpenAPI spec আর CI-তে contract test অনিচ্ছাকৃত breaking change ship হওয়ার আগেই ধরে।
            - **Business logic fork কোরো না:** প্রতি version-এ domain code-এর দুটো কপি মানে দ্বিগুণ bug। Translation (request/response mapping) edge-এ রাখো।
            - **Header format:** `Deprecation` একটি structured-field তারিখ, যেমন `@1790812800` (Unix seconds); `Sunset` একটি HTTP date। RFC 9745 documentation link-এর জন্য একটি `deprecation` link relation-ও define করে।
            - **Mobile client** সাথে সাথে জোর করে upgrade করানো যায় না, তাই public/mobile API-র sunset window সাধারণত সপ্তাহ নয়, মাস।
        """,
        tip_en=r"""Pick one strategy and justify it, say when you *don't* bump the version, and describe a concrete deprecation process with headers and usage metrics. The retirement plan is what most candidates forget.""",
        tip_bn=r"""একটি কৌশল বেছে নিয়ে যুক্তি দাও, কখন version *বাড়াবে না* সেটা বলো, আর header ও usage metric সহ একটি বাস্তব deprecation প্রক্রিয়া বর্ণনা করো। বন্ধ করার পরিকল্পনাটাই বেশিরভাগ candidate ভুলে যায়।""",
        mist_en=r"""Creating a new version for every additive change, copying the whole codebase per version, or switching v1 off on a date without measuring who still uses it.""",
        mist_bn=r"""প্রতিটি additive change-এ নতুন version বানানো, প্রতি version-এ পুরো codebase কপি করা, অথবা কে এখনও ব্যবহার করছে না মেপেই নির্দিষ্ট তারিখে v1 বন্ধ করে দেওয়া।""",
        code=r"""
            import express from 'express';
            import { v1Router } from './routes/v1/index.js';
            import { v2Router } from './routes/v2/index.js';

            const app = express();

            // v1 still works, but every response announces its retirement
            app.use('/v1', (req, res, next) => {
              res.set({
                Deprecation: '@1790812800',               // RFC 9745: deprecated since 2026-10-01 (Unix seconds)
                Sunset: 'Wed, 30 Jun 2027 00:00:00 GMT',   // RFC 8594: stops working after this date
                Link: '<https://docs.example.com/api/migrate-to-v2>; rel="deprecation"',
              });
              next();
            }, v1Router);

            app.use('/v2', v2Router);

            // After the sunset date, replace the v1 mount with:
            // app.use('/v1', (req, res) => res.status(410).json({ error: 'API v1 has been retired; use /v2' }));
        """,
        lang="javascript",
        follow=[
            ("How would you handle a breaking change to a single field without a whole new version?", "পুরো নতুন version ছাড়া একটি মাত্র field-এর breaking change কীভাবে সামলাবে?"),
            ("How do you know which clients still call v1?", "কোন client এখনও v1 call করে কীভাবে জানবে?"),
        ],
        related=["express-009", "express-007"],
        refs=[EX_ROUTING, RFC_8594, RFC_9745],
    ),
    # ------------------------------------------------------------------ express-030
    Q(
        id="express-030", sub="Express 4 to 5 Migration", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["express-5", "migration", "removed-apis", "sendstatus"],
        ver="Express 5.x (vs 4.x)", vs=True, status="stable",
        q_en=r"""You're upgrading an app from Express 4 to Express 5. Which of these lines still does what the author intended, **unchanged**, in Express 5?""",
        q_bn=r"""একটি app Express 4 থেকে Express 5-এ upgrade করছ। নিচের কোন line Express 5-এ **কোনো পরিবর্তন ছাড়াই** লেখকের উদ্দেশ্যমতো কাজ করে?""",
        options=[
            ("`app.del('/users/:id', removeUser)`", "`app.del('/users/:id', removeUser)`"),
            ("`res.send(404)` to respond with status 404", "Status 404 দিয়ে response দিতে `res.send(404)`"),
            ("`req.param('id')` to read a route or query parameter", "Route বা query parameter পড়তে `req.param('id')`"),
            ("`res.sendStatus(404)`", "`res.sendStatus(404)`"),
        ],
        correct=3,
        a_en=r"""
            `res.sendStatus(404)` — it sets the status and sends the standard reason phrase ("Not Found") as the body, exactly as in Express 4. The other three rely on APIs that Express 5 removed or changed.
        """,
        a_bn=r"""
            `res.sendStatus(404)` — এটা status set করে এবং body হিসেবে standard reason phrase ("Not Found") পাঠায়, ঠিক Express 4-এর মতোই। বাকি তিনটি এমন API-র উপর নির্ভর করে যা Express 5 সরিয়ে দিয়েছে বা বদলেছে।
        """,
        ex_en=r"""
            - **`app.del()`** was removed — use `app.delete()`. Calling it throws `TypeError: app.del is not a function` at startup.
            - **`req.param()`** was removed — read `req.params`, `req.query` or `req.body` explicitly.
            - **`res.send(404)` is the tempting trap**: it doesn't crash. In Express 5 a number passed to `res.send()` is treated as the body, so the client gets **status `200`** with body `404` (verified on Express 5.3). A silent bug like this is worse than a crash — use `res.sendStatus(404)` or `res.status(404).send(...)`.

            Other removals to grep for: `res.sendfile` (→ `res.sendFile`), `res.json(obj, status)` (→ `res.status(status).json(obj)`), `res.redirect('back')` (→ `res.redirect(req.get('Referrer') || '/')`), and pluralised `req.acceptsCharsets()` etc. The official codemods (`npx codemod@latest @expressjs/v5-migration-recipe`) automate many of these.
        """,
        ex_bn=r"""
            - **`app.del()`** সরিয়ে দেওয়া হয়েছে — `app.delete()` ব্যবহার করো। Call করলে startup-এ `TypeError: app.del is not a function` throw করে।
            - **`req.param()`** সরিয়ে দেওয়া হয়েছে — স্পষ্টভাবে `req.params`, `req.query` বা `req.body` পড়ো।
            - **`res.send(404)` হলো প্রলোভনের ফাঁদ**: এটা crash করে না। Express 5-এ `res.send()`-এ দেওয়া number-কে body ধরা হয়, ফলে client পায় **status `200`** আর body `404` (Express 5.3-এ যাচাই করা)। এমন নীরব bug crash-এর চেয়েও খারাপ — `res.sendStatus(404)` বা `res.status(404).send(...)` ব্যবহার করো।

            আরও যেসব বাদ পড়েছে, grep করে খুঁজো: `res.sendfile` (→ `res.sendFile`), `res.json(obj, status)` (→ `res.status(status).json(obj)`), `res.redirect('back')` (→ `res.redirect(req.get('Referrer') || '/')`), আর বহুবচন `req.acceptsCharsets()` ইত্যাদি। অফিসিয়াল codemod (`npx codemod@latest @expressjs/v5-migration-recipe`) এর অনেকগুলো স্বয়ংক্রিয়ভাবে ঠিক করে।
        """,
        tip_en=r"""After answering, point out which failures are loud (removed functions throw) and which are silent (`res.send(404)`). Prioritising the silent ones in a migration plan shows real experience.""",
        tip_bn=r"""উত্তরের পর দেখাও কোন failure জোরালো (সরানো function throw করে) আর কোনটা নীরব (`res.send(404)`)। Migration plan-এ নীরবগুলোকে অগ্রাধিকার দেওয়া বাস্তব অভিজ্ঞতা দেখায়।""",
        refs=[EX_MIGRATE5, EX_API5],
    ),
    # ------------------------------------------------------------------ express-031
    Q(
        id="express-031", sub="Express 4 to 5 Migration", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["express-5", "migration", "path-to-regexp", "query-parser", "rollout"],
        ver="Express 4.x → 5.x; Node.js 24 LTS", vs=True, status="stable",
        q_en=r"""You own a large Express 4 codebase (about 150 routes, many third-party middlewares, still on Node 18). Plan the migration to Express 5 in production: what breaks, how do you find it, and how do you roll it out safely?""",
        q_bn=r"""তোমার দায়িত্বে একটি বড় Express 4 codebase (প্রায় 150টি route, অনেক third-party middleware, এখনও Node 18-এ)। Production-এ Express 5-এ migration-এর পরিকল্পনা করো: কী কী ভাঙবে, কীভাবে খুঁজে বের করবে, আর কীভাবে নিরাপদে rollout করবে?""",
        a_en=r"""
            **0. Upgrade Node first, separately.** Node 18 is end-of-life; move to Node 24 LTS in its own release so you don't debug two upgrades at once. (Express 5 needs Node 18+, but you want a supported runtime.)

            **1. Inventory what breaks — loud vs silent:**
            - *Loud (crash at startup or on first call):* route syntax — `'*'` → `'/*splat'` or `'/{*splat}'`, `'/users/:id?'` → `'/users{/:id}'`, regex characters in path strings; removed APIs such as `app.del`, `req.param`, `res.sendfile`.
            - *Silent (wrong behaviour):* `res.send(status)` now sends the number as a 200 body; `req.query` uses the **simple** parser (nested `?filter[price][gte]=10` no longer becomes an object) and is read-only; `req.body` is `undefined` without a parser; `express.urlencoded` defaults to `extended: false`; `express.static` ignores dot-directories (e.g. `/.well-known` → 404); `req.host` keeps the port; `res.status()` rejects non-integers; `res.redirect('back')` is gone.
            - *Improvement:* async errors are forwarded automatically — wrappers become unnecessary but are harmless, so remove them later.

            **2. Find it:** run the official codemods (`npx codemod@latest @expressjs/v5-migration-recipe`), grep for the risky patterns, update `@types/express`, check each third-party middleware for v5 support (especially anything that mutates `req.query`), and run the full test suite. Add tests for query parsing, wildcard routes and static files.

            **3. Roll out safely:** deploy to staging and **replay real traffic** (or shadow it), diffing status codes and bodies between v4 and v5. Then canary 5% of production instances and watch per-route 404/400/500 rates and latency, with a fast rollback. Expand gradually.
        """,
        a_bn=r"""
            **0. আগে Node upgrade, আলাদাভাবে।** Node 18 end-of-life; নিজস্ব একটি release-এ Node 24 LTS-এ যাও, যাতে একসাথে দুটো upgrade debug করতে না হয়। (Express 5-এর জন্য Node 18+ লাগে, কিন্তু তোমার দরকার supported runtime।)

            **1. কী ভাঙবে তার তালিকা — জোরালো বনাম নীরব:**
            - *জোরালো (startup-এ বা প্রথম call-এ crash):* route syntax — `'*'` → `'/*splat'` বা `'/{*splat}'`, `'/users/:id?'` → `'/users{/:id}'`, path string-এ regex character; সরানো API যেমন `app.del`, `req.param`, `res.sendfile`।
            - *নীরব (ভুল আচরণ):* `res.send(status)` এখন number-কে 200 body হিসেবে পাঠায়; `req.query` **simple** parser ব্যবহার করে (nested `?filter[price][gte]=10` আর object হয় না) এবং read-only; parser ছাড়া `req.body` `undefined`; `express.urlencoded`-এর default `extended: false`; `express.static` dot-directory ignore করে (যেমন `/.well-known` → 404); `req.host` port রেখে দেয়; `res.status()` non-integer reject করে; `res.redirect('back')` আর নেই।
            - *উন্নতি:* async error স্বয়ংক্রিয়ভাবে forward হয় — wrapper অপ্রয়োজনীয় কিন্তু ক্ষতিকর নয়, তাই পরে সরাও।

            **2. খুঁজে বের করা:** অফিসিয়াল codemod চালাও (`npx codemod@latest @expressjs/v5-migration-recipe`), ঝুঁকিপূর্ণ pattern grep করো, `@types/express` update করো, প্রতিটি third-party middleware-এর v5 support যাচাই করো (বিশেষ করে যেগুলো `req.query` বদলায়), আর পুরো test suite চালাও। Query parsing, wildcard route আর static file-এর জন্য test যোগ করো।

            **3. নিরাপদ rollout:** staging-এ deploy করে **আসল traffic replay** করো (বা shadow করো), v4 আর v5-এর মধ্যে status code ও body-র diff দেখো। তারপর production instance-এর 5%-এ canary, route অনুযায়ী 404/400/500 rate আর latency দেখো, দ্রুত rollback-এর ব্যবস্থা রাখো। ধীরে ধীরে বাড়াও।
        """,
        ex_en=r"""
            - **Why separate "loud" from "silent":** startup crashes are found by any test run; silent changes only show up as wrong responses, so they need targeted tests and traffic diffing.
            - **Query parser decision:** if clients send nested filters, either keep compatibility with `app.set('query parser', 'extended')` (and validate strictly) or migrate clients first. Decide before the rollout, not after a spike of 400s.
            - **Middleware that writes to `req.query`** (some sanitisers/validators) breaks because it's a getter now — move parsed values to `res.locals` or a custom property.
            - **`.well-known`** (ACME challenges, app links) silently 404s with the new `dotfiles` default — serve it explicitly with `dotfiles: 'allow'`.
            - **`app.listen` callback** now receives errors such as `EADDRINUSE` instead of them being thrown — check the argument.
            - **Ownership:** split the work per module/team, track it on a checklist, and keep the canary running long enough to see daily traffic patterns.
        """,
        ex_bn=r"""
            - **"জোরালো" আর "নীরব" আলাদা করা কেন:** startup crash যেকোনো test run-এই ধরা পড়ে; নীরব পরিবর্তন শুধু ভুল response হিসেবে দেখা দেয়, তাই এগুলোর জন্য নির্দিষ্ট test আর traffic diff লাগে।
            - **Query parser-এর সিদ্ধান্ত:** client যদি nested filter পাঠায়, তাহলে হয় `app.set('query parser', 'extended')` দিয়ে compatibility রাখো (আর কড়াভাবে validate করো), নয়তো আগে client migrate করো। Rollout-এর আগেই সিদ্ধান্ত নাও, 400-এর spike দেখার পরে নয়।
            - **যে middleware `req.query`-তে লেখে** (কিছু sanitiser/validator), সেটা ভাঙে কারণ এটা এখন getter — parse করা value `res.locals` বা নিজস্ব property-তে সরাও।
            - **`.well-known`** (ACME challenge, app link) নতুন `dotfiles` default-এ নীরবে 404 দেয় — `dotfiles: 'allow'` দিয়ে আলাদাভাবে serve করো।
            - **`app.listen` callback** এখন `EADDRINUSE`-এর মতো error throw না করে argument হিসেবে পায় — argument-টা check করো।
            - **দায়িত্ব:** module/team অনুযায়ী কাজ ভাগ করো, checklist-এ track করো, আর দৈনিক traffic pattern দেখার মতো লম্বা সময় canary চালু রাখো।
        """,
        tip_en=r"""Frame the answer as risk management: separate upgrades, classify breakages as loud or silent, verify with traffic diffs, and roll out with a canary. That structure matters more than listing every API change.""",
        tip_bn=r"""উত্তরকে risk management হিসেবে সাজাও: upgrade আলাদা করা, breakage-কে জোরালো বা নীরব হিসেবে ভাগ করা, traffic diff দিয়ে যাচাই, আর canary দিয়ে rollout। প্রতিটি API পরিবর্তনের তালিকা দেওয়ার চেয়ে এই কাঠামো বেশি গুরুত্বপূর্ণ।""",
        mist_en=r"""Upgrading Node and Express in one big-bang release, trusting "it boots" as proof of compatibility, or forgetting that the query parser change silently alters filters.""",
        mist_bn=r"""এক বড় release-এ একসাথে Node আর Express upgrade করা, "boot হচ্ছে" দেখেই compatibility-র প্রমাণ ধরে নেওয়া, অথবা ভুলে যাওয়া যে query parser-এর পরিবর্তন নীরবে filter বদলে দেয়।""",
        code=r"""
            // Express 5 version                              // Express 4 (legacy) form it replaces
            app.get('/{*splat}', spa);                       // app.get('*', spa)
            app.get('/files/:name{.:ext}', sendFileRoute);   // '/files/:name.:ext?'
            app.get('/users{/:id}', usersRoute);             // '/users/:id?'
            app.delete('/users/:id', removeUser);            // app.del(...)

            // inside handlers:
            res.sendStatus(404);                             // res.send(404)
            res.status(201).json(user);                      // res.json(user, 201)
            res.redirect(req.get('Referrer') || '/');        // res.redirect('back')
            res.locals.page = Number(req.query.page);        // req.query.page = Number(...)

            // Keep nested query objects only if clients depend on them (then validate strictly):
            app.set('query parser', 'extended');

            // Serve ACME / app-link files that the new dotfiles default would hide:
            app.use('/.well-known', express.static('public/.well-known', { dotfiles: 'allow' }));
        """,
        lang="javascript",
        follow=[
            ("How would you diff responses between the v4 and v5 builds using recorded traffic?", "Record করা traffic দিয়ে v4 আর v5 build-এর response-এর পার্থক্য কীভাবে দেখবে?"),
            ("Which Express 5 changes would you expect a test suite to miss?", "Express 5-এর কোন পরিবর্তনগুলো test suite মিস করবে বলে মনে করো?"),
        ],
        related=["express-030", "express-002", "express-003"],
        refs=[EX_MIGRATE5, NODE_RELEASES],
    ),
    # ------------------------------------------------------------------ express-032
    Q(
        id="express-032", sub="REST APIs", diff="extreme", type="architecture",
        prio="high", market="international", mins=20,
        tags=["idempotency", "payments", "retries", "concurrency", "postgresql", "distributed-systems"],
        ver="Express 5.x; PostgreSQL 18 (Idempotency-Key pattern)", vs=False, status="stable",
        q_en=r"""Mobile clients on flaky networks retry `POST /payments` when a request times out, and some customers have been charged twice. Design idempotency for this Express API running on many instances — including two identical requests arriving at the same time and a server crash in the middle of a payment.""",
        q_bn=r"""দুর্বল network-এর mobile client request timeout হলে `POST /payments` retry করে, আর কিছু customer-কে দুবার charge করা হয়েছে। অনেক instance-এ চলা এই Express API-র জন্য idempotency design করো — একই সময়ে দুটো হুবহু request আসা এবং payment-এর মাঝখানে server crash হওয়ার ক্ষেত্রসহ।""",
        a_en=r"""
            *(Advanced, senior-level answer.)* `POST` isn't idempotent, so retries need an explicit **idempotency key**.

            **Protocol:** the client generates an `Idempotency-Key` (a UUID) per *logical* payment and reuses it for every retry. The server requires it on `POST /payments`.

            **Storage:** a durable table (PostgreSQL) keyed by `(user_id, key)` with a request **fingerprint** (hash of method, path and body), `status` (`in_progress`/`completed`), the stored response (status + body), and an expiry (e.g. 24 h). A unique constraint makes the claim atomic across all instances.

            **Flow:**
            1. `INSERT … ON CONFLICT DO NOTHING` with status `in_progress`. Only one request can win this race.
            2. **Winner:** process the payment — passing the **same key to the payment provider** as its idempotency key — then store the response and return it.
            3. **Loser / retry:** read the row. Different fingerprint → `422` (key reused for a different request). `in_progress` → `409 Conflict` with `Retry-After`. `completed` → replay the stored status and body (plus an `Idempotent-Replayed: true` header).

            **Crash in the middle:** a row stuck in `in_progress` past a lease time is not blindly retried. A reconciliation step asks the payment provider (by the same key) whether the charge happened, then completes or releases the row. Because the provider deduplicates by key too, even a retry after an uncertain failure doesn't double-charge.

            **Scope rules:** keys are per user (no cross-user collisions); validate the request *before* claiming the key, so validation failures and concurrency conflicts never store a result; on a `5xx` release the key so the client can retry (safe because the provider deduplicates by the same key); expire old keys with a cleanup job.
        """,
        a_bn=r"""
            *(Advanced, senior-level উত্তর।)* `POST` idempotent নয়, তাই retry-এর জন্য একটি স্পষ্ট **idempotency key** লাগে।

            **Protocol:** client প্রতিটি *যৌক্তিক* payment-এর জন্য একটি `Idempotency-Key` (একটি UUID) তৈরি করে এবং প্রতিটি retry-তে সেটাই ব্যবহার করে। Server `POST /payments`-এ এটা বাধ্যতামূলক করে।

            **Storage:** `(user_id, key)` দিয়ে key করা একটি durable table (PostgreSQL), যাতে থাকে request-এর **fingerprint** (method, path আর body-র hash), `status` (`in_progress`/`completed`), রেখে দেওয়া response (status + body), আর একটি expiry (যেমন 24 ঘণ্টা)। Unique constraint সব instance-জুড়ে claim-কে atomic করে।

            **Flow:**
            1. `in_progress` status দিয়ে `INSERT … ON CONFLICT DO NOTHING`। এই প্রতিযোগিতায় কেবল একটি request জিততে পারে।
            2. **বিজয়ী:** payment process করে — payment provider-কেও তার idempotency key হিসেবে **একই key পাঠিয়ে** — তারপর response রেখে দিয়ে return করে।
            3. **পরাজিত / retry:** row পড়ে। Fingerprint আলাদা → `422` (ভিন্ন request-এ key পুনর্ব্যবহার)। `in_progress` → `Retry-After` সহ `409 Conflict`। `completed` → রাখা status আর body replay (সাথে `Idempotent-Replayed: true` header)।

            **মাঝপথে crash:** lease time পেরিয়েও `in_progress`-এ আটকে থাকা row অন্ধভাবে retry করা হয় না। একটি reconciliation ধাপ একই key দিয়ে payment provider-কে জিজ্ঞেস করে charge হয়েছিল কি না, তারপর row complete বা release করে। Provider-ও key দিয়ে deduplicate করে বলে অনিশ্চিত failure-এর পর retry হলেও দুবার charge হয় না।

            **Scope-এর নিয়ম:** key user প্রতি (ভিন্ন user-এর মধ্যে collision নেই); key claim করার *আগেই* request validate করা হয়, ফলে validation failure বা concurrency conflict-এর কোনো ফলাফল রাখা হয় না; `5xx` হলে key ছেড়ে দেওয়া হয় যাতে client retry করতে পারে (নিরাপদ, কারণ provider একই key দিয়ে deduplicate করে); একটি cleanup job দিয়ে পুরনো key expire করা হয়।
        """,
        ex_en=r"""
            - **Why a database and not just Redis `SET NX`:** Redis works for the lock, but the idempotency record should be as durable as the payment itself; writing the payment row and marking the key `completed` in the same PostgreSQL transaction keeps them consistent. Redis is fine as a fast front-check if you accept that trade-off.
            - **Exactly-once is an illusion across a network:** you get *effectively-once* by combining at-least-once retries with deduplication at every hop (your API and the payment provider).
            - **Fingerprint check** prevents a buggy client from reusing a key for a different amount and silently getting the old response.
            - **Client side:** generate the key before the first attempt, persist it with the pending operation (so an app restart reuses it), and retry with exponential backoff and jitter.
            - **Observability:** count replays, 409 conflicts and stuck `in_progress` rows; alert when reconciliation finds mismatches.
            - The `Idempotency-Key` header was proposed in an IETF HTTPAPI working-group draft (the draft has expired without becoming an RFC), but the header name and pattern are a de facto convention used by large payment APIs.
        """,
        ex_bn=r"""
            - **কেন শুধু Redis `SET NX` নয়, database:** lock-এর জন্য Redis কাজ করে, কিন্তু idempotency record payment-এর মতোই durable হওয়া উচিত; একই PostgreSQL transaction-এ payment row লেখা আর key-কে `completed` চিহ্নিত করা দুটোকে consistent রাখে। সেই trade-off মেনে নিলে দ্রুত প্রাথমিক check হিসেবে Redis চলে।
            - **Network-এর উপর exactly-once একটি মায়া:** at-least-once retry-এর সাথে প্রতিটি ধাপে deduplication (তোমার API আর payment provider) মিলিয়ে *effectively-once* পাওয়া যায়।
            - **Fingerprint check** ত্রুটিপূর্ণ client-কে ভিন্ন amount-এর জন্য একই key ব্যবহার করে নীরবে পুরনো response পাওয়া থেকে আটকায়।
            - **Client-এর দিক:** প্রথম চেষ্টার আগেই key তৈরি করো, pending operation-এর সাথে সংরক্ষণ করো (যাতে app restart হলেও সেটাই ব্যবহার হয়), আর exponential backoff ও jitter দিয়ে retry করো।
            - **Observability:** replay, 409 conflict আর আটকে থাকা `in_progress` row গোনো; reconciliation কোনো অমিল পেলে alert দাও।
            - `Idempotency-Key` header IETF HTTPAPI working group-এর একটি draft-এ প্রস্তাব করা হয়েছিল (draft-টি RFC না হয়েই expire হয়েছে), তবে এই header-এর নাম আর pattern বড় payment API-গুলোতে কার্যত প্রচলিত রীতি।
        """,
        tip_en=r"""Walk through three timelines: a normal retry after timeout, two concurrent identical requests, and a crash mid-payment. Showing what happens in each — and that the provider also needs the key — is what makes this a senior answer.""",
        tip_bn=r"""তিনটি timeline ধরে বলো: timeout-এর পর স্বাভাবিক retry, একই সময়ে দুটো হুবহু request, আর payment-এর মাঝখানে crash। প্রতিটিতে কী হয় — আর provider-কেও যে key দিতে হয় — সেটা দেখানোই উত্তরটাকে senior মানের করে।""",
        mist_en=r"""Checking "does a payment with these details already exist?" (legitimate identical payments exist), using an in-memory map (doesn't work across instances), or not forwarding the key to the payment provider.""",
        mist_bn=r""""এই details-এর payment কি আগে থেকেই আছে?" check করা (বৈধ হুবহু payment-ও থাকতে পারে), in-memory map ব্যবহার করা (instance-জুড়ে কাজ করে না), অথবা payment provider-কে key forward না করা।""",
        code=r"""
            import { createHash } from 'node:crypto';
            import { db } from './db.js';

            export function idempotent() {
              return async (req, res, next) => {
                const key = req.get('idempotency-key');
                if (!key || !/^[\w-]{8,100}$/.test(key)) {
                  return res.status(400).json({ error: 'IDEMPOTENCY_KEY_REQUIRED' });
                }
                const fingerprint = createHash('sha256')
                  .update(`${req.method} ${req.originalUrl} ${JSON.stringify(req.body)}`)
                  .digest('hex');

                // Atomic claim across all instances: only one request inserts the row
                const claim = await db.query(
                  `INSERT INTO idempotency_keys (user_id, key, fingerprint, status, expires_at)
                   VALUES ($1, $2, $3, 'in_progress', now() + interval '24 hours')
                   ON CONFLICT (user_id, key) DO NOTHING`,
                  [req.user.id, key, fingerprint],
                );

                if (claim.rowCount === 0) {
                  const { rows: [existing] } = await db.query(
                    `SELECT fingerprint, status, response_status, response_body
                       FROM idempotency_keys WHERE user_id = $1 AND key = $2`,
                    [req.user.id, key],
                  );
                  if (existing.fingerprint !== fingerprint) {
                    return res.status(422).json({ error: 'IDEMPOTENCY_KEY_REUSED' });
                  }
                  if (existing.status === 'in_progress') {
                    return res.set('Retry-After', '2').status(409).json({ error: 'REQUEST_IN_PROGRESS' });
                  }
                  return res.set('Idempotent-Replayed', 'true')
                    .status(existing.response_status)
                    .json(existing.response_body);
                }

                // First request: persist the outcome before it reaches the client
                res.locals.idempotencyKey = key; // handler forwards it to the payment provider
                const sendJson = res.json.bind(res);
                res.json = (body) => {
                  const done = res.statusCode < 500
                    ? db.query(
                        `UPDATE idempotency_keys
                            SET status = 'completed', response_status = $3, response_body = $4
                          WHERE user_id = $1 AND key = $2`,
                        [req.user.id, key, res.statusCode, body],
                      )
                    // 5xx: release the key so the client can retry; the provider dedupes by the same key
                    : db.query('DELETE FROM idempotency_keys WHERE user_id = $1 AND key = $2', [req.user.id, key]);
                  done
                    .catch((err) => req.log?.error({ err }, 'idempotency bookkeeping failed'))
                    .finally(() => sendJson(body));
                  return res;
                };
                next();
              };
            }

            // Validate BEFORE claiming the key, so invalid requests never store a result:
            // app.post('/payments', authenticate, express.json(), validate(paymentSchema), idempotent(), createPayment);
        """,
        lang="javascript",
        extra=[
            dict(lang="sql", src=r"""
                CREATE TABLE idempotency_keys (
                  user_id         bigint      NOT NULL,
                  key             text        NOT NULL,
                  fingerprint     text        NOT NULL,
                  status          text        NOT NULL CHECK (status IN ('in_progress', 'completed')),
                  response_status int,
                  response_body   jsonb,
                  created_at      timestamptz NOT NULL DEFAULT now(),
                  expires_at      timestamptz NOT NULL,
                  PRIMARY KEY (user_id, key)
                );
                -- A periodic job deletes expired rows and reconciles stale 'in_progress' ones.
            """, label_en="PostgreSQL table", label_bn="PostgreSQL table"),
        ],
        follow=[
            ("How would you reconcile a payment stuck in `in_progress` after a crash?", "Crash-এর পর `in_progress`-এ আটকে থাকা payment কীভাবে reconcile করবে?"),
            ("Should a `500` response be stored and replayed? Why or why not?", "একটি `500` response কি রেখে replay করা উচিত? কেন বা কেন নয়?"),
            ("How do idempotency keys relate to exactly-once message processing in queues?", "Queue-তে exactly-once message processing-এর সাথে idempotency key-র সম্পর্ক কী?"),
        ],
        related=["express-009", "express-007"],
        refs=[IETF_IDEMPOTENCY, MDN_IDEMPOTENT, PG_INSERT],
    ),
]

if __name__ == "__main__":
    save("express", "b5", QUESTIONS)
