import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

EX_USING_MW = ("Express — Using middleware", "https://expressjs.com/en/guide/using-middleware.html")
EX_WRITING_MW = ("Express — Writing middleware", "https://expressjs.com/en/guide/writing-middleware.html")
EX_ROUTING = ("Express — Routing", "https://expressjs.com/en/guide/routing.html")
EX_MIGRATE5 = ("Express — Migrating to Express 5", "https://expressjs.com/en/guide/migrating-5.html")
EX_API5 = ("Express 5.x — API reference", "https://expressjs.com/en/5x/api.html")
EX_ERRORS = ("Express — Error handling", "https://expressjs.com/en/guide/error-handling.html")
RFC_9457 = ("RFC 9457 — Problem Details for HTTP APIs", "https://www.rfc-editor.org/rfc/rfc9457")
OWASP_ERRORS = ("OWASP — Error Handling Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html")
EX_PERF = ("Express — Production best practices: performance and reliability", "https://expressjs.com/en/advanced/best-practice-performance.html")
EX_SECURITY = ("Express — Production best practices: security", "https://expressjs.com/en/advanced/best-practice-security.html")
OWASP_REST = ("OWASP — REST Security Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ express-001
    Q(
        id="express-001", sub="Middleware", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["middleware", "next", "request-pipeline", "express-basics"],
        ver="Express 5.x", vs=False, status="stable",
        q_en=r"""What is middleware in Express, and how does a request flow through the middleware stack?""",
        q_bn=r"""Express-এ middleware কী, আর একটি request middleware stack-এর মধ্য দিয়ে কীভাবে যায়?""",
        a_en=r"""
            Middleware is a function with the signature `(req, res, next)` that runs as part of the request pipeline. Express keeps an ordered list of middleware and route handlers, and for each request it runs the matching ones **in the order they were registered**.

            Each middleware can do one of three things:
            - read or modify `req`/`res` (parse the body, attach `req.user`, set headers),
            - **end the response** (`res.json()`, `res.send()`, `res.sendStatus()`), or
            - call `next()` to hand control to the next matching middleware — or `next(err)` to jump straight to error-handling middleware.

            If a middleware neither responds nor calls `next()`, the request just hangs. Typical examples are built-ins like `express.json()` and `express.static()`, third-party ones like `helmet` and `cors`, and my own auth or logging middleware.
        """,
        a_bn=r"""
            Middleware হলো `(req, res, next)` signature-এর একটি function, যা request pipeline-এর অংশ হিসেবে চলে। Express middleware আর route handler-এর একটি ক্রমানুসারী তালিকা রাখে, আর প্রতিটি request-এর জন্য মিলে যাওয়া handler-গুলো **যে ক্রমে register করা হয়েছে সেই ক্রমে** চালায়।

            প্রতিটি middleware তিনটির একটি করতে পারে:
            - `req`/`res` পড়া বা বদলানো (body parse করা, `req.user` যোগ করা, header set করা),
            - **response শেষ করা** (`res.json()`, `res.send()`, `res.sendStatus()`), অথবা
            - `next()` call করে পরের মিলে যাওয়া middleware-কে নিয়ন্ত্রণ দেওয়া — বা `next(err)` দিয়ে সরাসরি error-handling middleware-এ চলে যাওয়া।

            কোনো middleware যদি response-ও না দেয়, `next()`-ও call না করে, তাহলে request ঝুলে থাকে। সাধারণ উদাহরণ: `express.json()` ও `express.static()`-এর মতো built-in, `helmet` ও `cors`-এর মতো third-party, আর আমার নিজের auth বা logging middleware।
        """,
        ex_en=r"""
            - **Mount paths:** `app.use('/api', mw)` runs `mw` for every path that *starts with* `/api`; `app.get('/x', mw)` matches only that method and path.
            - **Order is the whole game:** body parsers and security middleware go first, routes in the middle, the 404 handler and error handler last.
            - **Passing data:** attach request-scoped data to `req` (e.g. `req.user`) or `res.locals`, not to module-level variables.
            - **`next('route')`** skips the remaining handlers of the current route; `next('router')` leaves the current router.
            - **Express 5:** if an `async` middleware's promise rejects, Express calls `next(err)` for you. A resolved promise does *not* call `next()` automatically — you still call it yourself.
        """,
        ex_bn=r"""
            - **Mount path:** `app.use('/api', mw)` `/api` দিয়ে *শুরু হওয়া* প্রতিটি path-এ `mw` চালায়; `app.get('/x', mw)` শুধু ওই method আর path মেলায়।
            - **ক্রমই আসল খেলা:** body parser আর security middleware আগে, route মাঝখানে, 404 handler আর error handler সবার শেষে।
            - **Data পাঠানো:** request-নির্দিষ্ট data `req`-এ (যেমন `req.user`) বা `res.locals`-এ রাখো, module-level variable-এ নয়।
            - **`next('route')`** current route-এর বাকি handler বাদ দেয়; `next('router')` current router থেকে বেরিয়ে যায়।
            - **Express 5:** `async` middleware-এর promise reject হলে Express নিজেই `next(err)` call করে। কিন্তু promise resolve হলে `next()` স্বয়ংক্রিয়ভাবে call হয় না — সেটা তোমাকেই করতে হবে।
        """,
        tip_en=r"""Describe it as a pipeline and give the three possible outcomes (modify, respond, pass on). Mentioning "order of registration matters" up front is what interviewers listen for.""",
        tip_bn=r"""একে একটি pipeline হিসেবে বর্ণনা করো এবং তিনটি সম্ভাব্য ফলাফল বলো (বদলানো, response দেওয়া, পরের জনকে দেওয়া)। শুরুতেই "register করার ক্রম গুরুত্বপূর্ণ" বলাটাই interviewer শুনতে চায়।""",
        mist_en=r"""Calling `next()` after already sending a response, or thinking Express runs middleware in parallel.""",
        mist_bn=r"""Response পাঠানোর পরেও `next()` call করা, অথবা মনে করা যে Express middleware parallel-এ চালায়।""",
        code=r"""
            import express from 'express';

            const app = express();

            // 1) Runs for every request
            app.use((req, res, next) => {
              req.startedAt = Date.now();
              next(); // pass control on
            });

            // 2) Built-in body parser
            app.use(express.json());

            // 3) Route handler: ends the response
            app.get('/ping', (req, res) => {
              res.json({ pong: true, tookMs: Date.now() - req.startedAt });
            });

            app.listen(3000);
        """,
        lang="javascript",
        follow=[
            ("What happens if a middleware never calls `next()` and never responds?", "কোনো middleware যদি কখনো `next()` call না করে এবং response-ও না দেয়, তাহলে কী হয়?"),
            ("What's the difference between `app.use()` and `app.get()` for mounting middleware?", "Middleware mount করার জন্য `app.use()` আর `app.get()`-এর পার্থক্য কী?"),
        ],
        related=["express-004", "express-010"],
        refs=[EX_USING_MW, EX_WRITING_MW],
    ),
    # ------------------------------------------------------------------ express-002
    Q(
        id="express-002", sub="Routing (Express 5 Path Syntax)", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["routing", "path-to-regexp", "wildcard", "express-5"],
        ver="Express 5.x (path-to-regexp v8)", vs=True, status="stable",
        q_en=r"""In Express 5, you need a catch-all `GET` route that matches every path, **including `/` itself** (for example to serve a single-page app's `index.html`). Which definition is correct?""",
        q_bn=r"""Express 5-এ তোমার এমন একটি catch-all `GET` route দরকার যা প্রতিটি path মেলাবে, **`/` নিজেকেও সহ** (যেমন single-page app-এর `index.html` serve করতে)। কোন definition সঠিক?""",
        options=[
            ("`app.get('*', handler)`", "`app.get('*', handler)`"),
            ("`app.get('/*', handler)`", "`app.get('/*', handler)`"),
            ("`app.get('/*splat', handler)`", "`app.get('/*splat', handler)`"),
            ("`app.get('/{*splat}', handler)`", "`app.get('/{*splat}', handler)`"),
        ],
        correct=3,
        a_en=r"""
            `app.get('/{*splat}', handler)`. Express 5 uses path-to-regexp v8, where a wildcard must have a name (`*splat`), and wrapping it in braces makes it optional — so it matches `/` as well as any deeper path.
        """,
        a_bn=r"""
            `app.get('/{*splat}', handler)`। Express 5 path-to-regexp v8 ব্যবহার করে, যেখানে wildcard-এর একটি নাম থাকতে হয় (`*splat`), আর brace-এর ভেতরে রাখলে সেটা optional হয় — ফলে এটা `/` এবং যেকোনো গভীর path দুটোই মেলায়।
        """,
        ex_en=r"""
            - `'*'` and `'/*'` are Express 4 syntax. In Express 5 they **throw at startup** (`Missing parameter name`), so the app won't even boot — verified on Express 5.3.
            - `'/*splat'` is the tempting answer: it's valid, but it requires at least one character after `/`, so a request for `/` itself doesn't match.
            - `req.params.splat` is an **array of segments**: `GET /a/b` → `['a', 'b']`. For `/` the parameter is omitted entirely.
            - Related v8 rules: optional parts use braces (`/:file{.:ext}` instead of `/:ext?`), regex characters like `()[]?+!` are reserved in string paths (use an array of paths or a `RegExp` object instead), and the name `splat` is just a convention.
        """,
        ex_bn=r"""
            - `'*'` আর `'/*'` হলো Express 4-এর syntax। Express 5-এ এগুলো **startup-এর সময়ই throw করে** (`Missing parameter name`), তাই app boot-ই হয় না — Express 5.3-এ যাচাই করা।
            - `'/*splat'` হলো প্রলোভনের উত্তর: এটা valid, কিন্তু `/`-এর পরে অন্তত একটি character লাগে, তাই `/` নিজে মেলে না।
            - `req.params.splat` হলো **segment-এর array**: `GET /a/b` → `['a', 'b']`। `/`-এর ক্ষেত্রে parameter-টি পুরোপুরি বাদ যায়।
            - v8-এর আরও নিয়ম: optional অংশ brace দিয়ে (`/:ext?`-এর বদলে `/:file{.:ext}`), string path-এ `()[]?+!`-এর মতো regex character reserved (এর বদলে path-এর array বা `RegExp` object ব্যবহার করো), আর `splat` নামটা শুধু একটি প্রথা।
        """,
        tip_en=r"""Mention that the Express 4 syntax doesn't just "not match" — it crashes at startup. That's the practical migration gotcha interviewers like to hear.""",
        tip_bn=r"""উল্লেখ করো যে Express 4-এর syntax শুধু "মেলে না" তা নয় — startup-এই crash করে। এটাই migration-এর বাস্তব gotcha যা interviewer শুনতে পছন্দ করে।""",
        refs=[EX_MIGRATE5, EX_ROUTING],
    ),
    # ------------------------------------------------------------------ express-003
    Q(
        id="express-003", sub="Request & Response Lifecycle", diff="easy", type="conceptual",
        prio="high", market="bangladesh", mins=3,
        tags=["req-params", "req-query", "req-body", "express-5", "body-parser"],
        ver="Express 5.x", vs=True, status="stable",
        q_en=r"""What is the difference between `req.params`, `req.query` and `req.body` in Express, and what changed about them in Express 5?""",
        q_bn=r"""Express-এ `req.params`, `req.query` আর `req.body`-এর পার্থক্য কী, আর Express 5-এ এগুলোর ব্যাপারে কী বদলেছে?""",
        a_en=r"""
            - **`req.params`** — values from the route path: for `/users/:id`, a request to `/users/42` gives `req.params.id === '42'`. Always strings.
            - **`req.query`** — the parsed query string: `?page=2&tag=a&tag=b` → `{ page: '2', tag: ['a', 'b'] }`. Also strings (or arrays of strings).
            - **`req.body`** — the parsed request body, which exists only if a body-parsing middleware ran: `express.json()`, `express.urlencoded()`, or multer for multipart.

            Express 5 changes:
            - `req.body` is **`undefined`** when no parser ran (Express 4 gave `{}`), so destructuring it crashes instead of silently giving `undefined` fields.
            - `req.query` is now a **getter** — you can't reassign it, and the default parser is **`'simple'`**, so nested syntax like `?filter[price]=10` stays a flat key `'filter[price]'`.
            - `req.param(name)` was removed; use the specific object instead.
        """,
        a_bn=r"""
            - **`req.params`** — route path-এর value: `/users/:id`-এর জন্য `/users/42`-এ request এলে `req.params.id === '42'`। সবসময় string।
            - **`req.query`** — parse করা query string: `?page=2&tag=a&tag=b` → `{ page: '2', tag: ['a', 'b'] }`। এগুলোও string (বা string-এর array)।
            - **`req.body`** — parse করা request body, যা শুধু তখনই থাকে যখন কোনো body-parsing middleware চলেছে: `express.json()`, `express.urlencoded()`, বা multipart-এর জন্য multer।

            Express 5-এর পরিবর্তন:
            - কোনো parser না চললে `req.body` **`undefined`** (Express 4-এ ছিল `{}`), তাই destructure করলে চুপচাপ `undefined` field না দিয়ে crash করে।
            - `req.query` এখন একটি **getter** — এটা reassign করা যায় না, আর default parser **`'simple'`**, তাই `?filter[price]=10`-এর মতো nested syntax একটি flat key `'filter[price]'` হিসেবেই থাকে।
            - `req.param(name)` সরিয়ে দেওয়া হয়েছে; নির্দিষ্ট object-টাই ব্যবহার করো।
        """,
        ex_en=r"""
            - **Everything is a string:** `req.params.id` and `req.query.page` must be converted and validated (`Number(...)`, a zod schema) before use.
            - **`req.query` is recomputed on access**, so `req.query.page = 1` is silently lost and `req.query = {...}` throws a `TypeError` in strict-mode code (ES modules). Store parsed/validated values in `res.locals` or a custom property such as `req.validated`.
            - **Need nested query objects?** Opt in with `app.set('query parser', 'extended')` — but nested parsing increases attack surface (deep objects, prototype keys), so validate strictly.
            - **`req.params`** has a null prototype for string paths in Express 5, wildcard params are arrays, and unmatched optional params are omitted rather than `undefined`.
            - Content-type matters: `express.json()` only parses `application/json`; a form post to a JSON-only app leaves `req.body` `undefined`.
        """,
        ex_bn=r"""
            - **সবকিছুই string:** ব্যবহারের আগে `req.params.id` আর `req.query.page` convert ও validate করতে হবে (`Number(...)`, একটি zod schema)।
            - **`req.query` প্রতিবার access-এ নতুন করে তৈরি হয়**, তাই `req.query.page = 1` চুপচাপ হারিয়ে যায় আর strict-mode code-এ (ES module) `req.query = {...}` একটি `TypeError` throw করে। Parse/validate করা value `res.locals`-এ বা `req.validated`-এর মতো নিজস্ব property-তে রাখো।
            - **Nested query object দরকার?** `app.set('query parser', 'extended')` দিয়ে চালু করো — তবে nested parsing attack surface বাড়ায় (গভীর object, prototype key), তাই কড়াভাবে validate করো।
            - Express 5-এ string path-এর জন্য **`req.params`**-এর prototype null, wildcard param array হয়, আর মেলেনি এমন optional param `undefined` না হয়ে পুরোপুরি বাদ যায়।
            - Content-type গুরুত্বপূর্ণ: `express.json()` শুধু `application/json` parse করে; JSON-only app-এ form post করলে `req.body` `undefined` থাকে।
        """,
        tip_en=r"""Give a one-line example URL for each, then list the Express 5 changes. Knowing that `req.body` is now `undefined` without a parser instantly shows you've worked with v5, not just v4 tutorials.""",
        tip_bn=r"""প্রতিটির জন্য এক লাইনের উদাহরণ URL দাও, তারপর Express 5-এর পরিবর্তনগুলো বলো। Parser ছাড়া `req.body` এখন `undefined` — এটা জানলেই বোঝা যায় তুমি শুধু v4 tutorial নয়, v5 নিয়ে কাজ করেছ।""",
        mist_en=r"""Treating `req.query.page` as a number, or writing validated values back into `req.query` in Express 5.""",
        mist_bn=r"""`req.query.page`-কে number হিসেবে ব্যবহার করা, অথবা Express 5-এ validate করা value আবার `req.query`-তে লিখে দেওয়া।""",
        code=r"""
            import express from 'express';

            const app = express();
            app.use(express.json()); // without this, req.body is undefined in Express 5

            // PUT /users/42?notify=true&tag=a&tag=b   body: {"name":"Rahim"}
            app.put('/users/:id', (req, res) => {
              const id = Number(req.params.id);          // '42' -> 42
              const notify = req.query.notify === 'true'; // query values are strings
              const tags = [req.query.tag].flat().filter(Boolean); // 'a' or ['a','b'] -> array
              res.json({ id, notify, tags, name: req.body?.name });
            });
        """,
        lang="javascript",
        follow=[
            ("How would you safely parse `?page=` into a positive integer with a default?", "`?page=`-কে default সহ positive integer-এ নিরাপদে কীভাবে parse করবে?"),
            ("Why might enabling the 'extended' query parser be a security concern?", "'extended' query parser চালু করা কেন security-র দিক থেকে উদ্বেগের হতে পারে?"),
        ],
        related=["express-012", "express-028"],
        refs=[EX_MIGRATE5, EX_API5],
    ),
    # ------------------------------------------------------------------ express-004
    Q(
        id="express-004", sub="Middleware", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["middleware-order", "body-parser", "authentication", "express-5", "debugging"],
        ver="Express 5.x", vs=True, status="stable",
        q_en=r"""After upgrading to Express 5, `POST /api/users` returns 500 with `Cannot destructure property 'name' of 'req.body' as it is undefined`. A security review also found that the `/api` routes accept requests without any token. Find and fix the bugs.""",
        q_bn=r"""Express 5-এ upgrade করার পর `POST /api/users` 500 return করছে, error: `Cannot destructure property 'name' of 'req.body' as it is undefined`। একটি security review-তে আরও দেখা গেছে যে `/api` route-গুলো কোনো token ছাড়াই request নিচ্ছে। Bug-গুলো খুঁজে বের করে ঠিক করো।""",
        a_en=r"""
            Both bugs are **middleware order** problems — Express runs middleware strictly in the order it was registered.

            1. The router is mounted **before** `express.json()`. When `POST /api/users` arrives, the router's handler runs first and sends the response, so the JSON parser never runs for it. In Express 5 an unparsed body is `undefined`, so destructuring throws. (In Express 4 `req.body` was `{}`, so the same bug silently produced `undefined` name and email — arguably worse.)
            2. `authenticate` is registered **after** the router, so for any route the router handles, the response is already sent before authentication would run. The routes are effectively public.

            Fix: register in this order — security/global middleware → body parser → authentication → routes → 404 handler → error handler. Mounting `authenticate` together with the router (`app.use('/api', authenticate, apiRouter)`) also makes the dependency explicit.
        """,
        a_bn=r"""
            দুটো bug-ই **middleware order**-এর সমস্যা — Express ঠিক যে ক্রমে register করা হয়েছে সেই ক্রমেই middleware চালায়।

            1. Router mount করা হয়েছে `express.json()`-এর **আগে**। `POST /api/users` এলে router-এর handler আগে চলে এবং response পাঠিয়ে দেয়, তাই JSON parser এই request-এর জন্য কখনো চলে না। Express 5-এ parse না হওয়া body `undefined`, তাই destructure করলে throw হয়। (Express 4-এ `req.body` ছিল `{}`, ফলে একই bug চুপচাপ `undefined` name আর email দিত — যা আরও খারাপ বলা যায়।)
            2. `authenticate` register করা হয়েছে router-এর **পরে**, তাই router যে route handle করে, সেখানে authentication চলার আগেই response চলে যায়। Route-গুলো কার্যত public।

            Fix: এই ক্রমে register করো — security/global middleware → body parser → authentication → route → 404 handler → error handler। Router-এর সাথে একসাথে `authenticate` mount করলে (`app.use('/api', authenticate, apiRouter)`) dependency-টাও স্পষ্ট হয়।
        """,
        ex_en=r"""
            - **How to spot order bugs quickly:** read `app.use` calls top to bottom and ask "has X already happened when this runs?" Logging `req.body` at the start of the handler or setting `DEBUG=express:*,router` also shows which layers ran.
            - **Body parser scope:** you can apply `express.json()` only where needed (e.g. `apiRouter.use(express.json())`) — but it must still come before the handlers that read `req.body`.
            - **Auth placement:** public routes (login, health checks) should be mounted *before* the auth middleware or on a separate router; everything after it is protected.
            - **404 and error handlers must be last** — a 404 handler registered early would swallow every request.
            - The verified fixed version returns 401 without a token, 201 with a valid token, 400 for malformed JSON (from the body parser), and 404 for unknown routes.
        """,
        ex_bn=r"""
            - **Order bug দ্রুত ধরার উপায়:** `app.use` call-গুলো উপর থেকে নিচে পড়ো আর জিজ্ঞেস করো "এটা চলার সময় X কি ইতিমধ্যে ঘটেছে?" Handler-এর শুরুতে `req.body` log করলে বা `DEBUG=express:*,router` set করলেও কোন layer চলেছে বোঝা যায়।
            - **Body parser-এর scope:** `express.json()` শুধু যেখানে দরকার সেখানেও লাগানো যায় (যেমন `apiRouter.use(express.json())`) — কিন্তু `req.body` পড়া handler-এর আগেই থাকতে হবে।
            - **Auth-এর অবস্থান:** public route (login, health check) auth middleware-এর *আগে* বা আলাদা router-এ mount করো; এর পরের সবকিছু protected।
            - **404 আর error handler সবার শেষে** — আগে register করা 404 handler সব request গিলে ফেলবে।
            - যাচাই করা fixed version token ছাড়া 401, valid token-এ 201, malformed JSON-এ 400 (body parser থেকে), আর অজানা route-এ 404 দেয়।
        """,
        tip_en=r"""Point out that Express 5 made this bug *louder* (crash instead of silent `undefined`) — and that the auth bug is the more dangerous one. Prioritising the security issue shows judgement.""",
        tip_bn=r"""উল্লেখ করো যে Express 5 এই bug-কে *জোরালো* করেছে (চুপচাপ `undefined`-এর বদলে crash) — আর auth bug-টাই বেশি বিপজ্জনক। Security issue-কে অগ্রাধিকার দেওয়া তোমার বিচারবুদ্ধি দেখায়।""",
        mist_en=r""""Fixing" the crash with `req.body ?? {}` in the handler, which hides the ordering bug, or adding auth checks inside every handler instead of fixing the order.""",
        mist_bn=r"""Handler-এ `req.body ?? {}` দিয়ে crash "ঠিক" করা, যা ordering bug লুকিয়ে ফেলে, অথবা order ঠিক না করে প্রতিটি handler-এর ভেতরে auth check বসানো।""",
        code=r"""
            import express from 'express';
            import { authenticate } from './auth.js';
            import { apiRouter } from './routes/api.js'; // contains POST /users

            const app = express();

            app.use('/api', apiRouter);
            app.use(express.json());
            app.use('/api', authenticate);

            app.use((err, req, res, next) => {
              res.status(500).json({ error: err.message });
            });

            app.listen(3000);
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                const app = express();

                app.use(express.json({ limit: '100kb' }));        // 1. parse bodies first
                app.post('/auth/login', loginHandler);            // 2. public routes before auth
                app.use('/api', authenticate, apiRouter);         // 3. auth, then protected routes

                app.use((req, res) => {                           // 4. 404 for anything unmatched
                  res.status(404).json({ error: 'Not Found' });
                });

                app.use((err, req, res, next) => {                // 5. error handler last
                  res.status(err.status ?? 500).json({ error: err.expose ? err.message : 'Internal Server Error' });
                });
            """, label_en="Fixed version (correct order)", label_bn="সংশোধিত version (সঠিক ক্রম)"),
        ],
        follow=[
            ("Where would you put `helmet()` and `cors()` in this stack, and why?", "এই stack-এ `helmet()` আর `cors()` কোথায় রাখবে, এবং কেন?"),
            ("How would you write a test that catches this ordering bug?", "এই ordering bug ধরার জন্য কীভাবে test লিখবে?"),
        ],
        related=["express-001", "express-003", "express-010"],
        refs=[EX_USING_MW, EX_MIGRATE5],
    ),
    # ------------------------------------------------------------------ express-005
    Q(
        id="express-005", sub="Error-Handling Middleware", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["async-errors", "express-5", "error-handling", "promises"],
        ver="Express 5.x", vs=True, status="stable",
        q_en=r"""In Express 5, what happens when `db.users.findById()` rejects (e.g. the database refuses the connection)?""",
        q_bn=r"""Express 5-এ `db.users.findById()` reject করলে (যেমন database connection refuse করলে) কী হবে?""",
        code=r"""
            app.get('/users/:id', async (req, res) => {
              const user = await db.users.findById(req.params.id);
              res.json(user);
            });

            app.use((err, req, res, next) => {
              res.status(500).json({ error: 'Internal Server Error' });
            });
        """,
        lang="javascript",
        options=[
            ("The process crashes with an unhandled promise rejection", "Unhandled promise rejection-এ process crash করবে"),
            ("The request hangs until the client times out", "Client timeout না হওয়া পর্যন্ত request ঝুলে থাকবে"),
            ("Express forwards the rejection to the error-handling middleware, which responds with 500 JSON", "Express rejection-টি error-handling middleware-এ পাঠাবে, যা 500 JSON response দেবে"),
            ("Express retries the handler once and then responds with 502", "Express handler-টি একবার retry করবে, তারপর 502 response দেবে"),
        ],
        correct=2,
        a_en=r"""
            Express forwards it. In Express 5, when a route handler or middleware returns a rejected promise (an `async` function that throws or awaits a rejection), Express calls `next(err)` with the rejection value, so the error-handling middleware sends the 500 JSON response.
        """,
        a_bn=r"""
            Express এটা forward করবে। Express 5-এ কোনো route handler বা middleware rejected promise return করলে (যে `async` function throw করে বা rejection-এর জন্য await করে), Express rejection value দিয়ে `next(err)` call করে, ফলে error-handling middleware 500 JSON response পাঠায়।
        """,
        ex_en=r"""
            Options A and B describe **Express 4**: it ignored the returned promise, so the rejection was unhandled — which on Node 15+ crashes the process, and on older setups left the request hanging. That's why Express 4 code used `try/catch` + `next(err)` in every handler or wrappers like `express-async-handler`. In Express 5 those wrappers are unnecessary.

            What Express 5 still **cannot** catch:
            - errors thrown inside callbacks that run later (`setTimeout`, event listeners, old callback APIs),
            - promises you don't `await` or return (fire-and-forget calls),
            - stream `'error'` events you didn't wire up (use `pipeline`).

            Those still crash the process or hang, so keep everything on the awaited promise chain.
        """,
        ex_bn=r"""
            Option A আর B হলো **Express 4**-এর আচরণ: সে return করা promise ignore করত, ফলে rejection unhandled থাকত — Node 15+-এ এতে process crash করে, আর পুরনো setup-এ request ঝুলে থাকত। এজন্যই Express 4-এর code-এ প্রতিটি handler-এ `try/catch` + `next(err)` বা `express-async-handler`-এর মতো wrapper ব্যবহার হতো। Express 5-এ এসব wrapper অপ্রয়োজনীয়।

            Express 5 এখনও যা **ধরতে পারে না**:
            - পরে চলা callback-এর ভেতরে throw হওয়া error (`setTimeout`, event listener, পুরনো callback API),
            - যে promise তুমি `await` বা return করো না (fire-and-forget call),
            - যে stream `'error'` event তুমি সংযুক্ত করোনি (`pipeline` ব্যবহার করো)।

            এগুলো এখনও process crash করায় বা ঝুলিয়ে রাখে, তাই সবকিছু await করা promise chain-এর মধ্যে রাখো।
        """,
        tip_en=r"""Contrast v4 and v5 in one sentence, then list what v5 still doesn't catch. The "still doesn't catch" list is what separates a memorised answer from real understanding.""",
        tip_bn=r"""এক বাক্যে v4 আর v5-এর তুলনা করো, তারপর v5 এখনও যা ধরে না তার তালিকা দাও। এই "এখনও ধরে না" তালিকাটাই মুখস্থ উত্তর আর সত্যিকারের বোঝাপড়ার পার্থক্য গড়ে দেয়।""",
        refs=[EX_ERRORS, EX_MIGRATE5],
    ),
    # ------------------------------------------------------------------ express-006
    Q(
        id="express-006", sub="Centralized Error Handling", diff="hard", type="architecture",
        prio="high", market="both", mins=12,
        tags=["error-handling", "app-error", "problem-details", "express-5", "architecture"],
        ver="Express 5.x; zod 4.x", vs=True, status="stable",
        q_en=r"""Design centralized error handling for an Express 5 REST API. How do you represent expected errors, map library errors (validation, malformed JSON, duplicate keys) to proper HTTP responses, avoid leaking internals, and keep handlers clean?""",
        q_bn=r"""একটি Express 5 REST API-এর জন্য centralized error handling design করো। প্রত্যাশিত error কীভাবে represent করবে, library error (validation, malformed JSON, duplicate key) কীভাবে সঠিক HTTP response-এ map করবে, internal তথ্য ফাঁস হওয়া কীভাবে আটকাবে, আর handler-গুলো কীভাবে পরিষ্কার রাখবে?""",
        a_en=r"""
            I separate **operational errors** (expected: not found, validation failed, conflict, unauthorized) from **programmer/unknown errors** (bugs, outages), and handle both in one place.

            - **`AppError` class:** carries `status`, a stable machine-readable `code` (`NOT_FOUND`, `VALIDATION_FAILED`), a client-safe message, optional `details`, and an `expose` flag (true for 4xx). Handlers simply `throw AppError.notFound('User')`.
            - **No try/catch in handlers:** in Express 5, a thrown error or rejected promise in an `async` handler goes straight to the error middleware.
            - **One mapping function** converts known library errors: `ZodError` → 400 with field errors, body-parser `entity.parse.failed` → 400, `entity.too.large` → 413, PostgreSQL `23505` / MongoDB `11000` → 409, JWT errors → 401. Everything unknown becomes a generic 500.
            - **Consistent format:** RFC 9457 problem details (`application/problem+json` with `type`, `title`, `status`, plus my `code` and `errors`).
            - **No leaks:** for 5xx, the client sees only "Internal Server Error"; the real error, stack and request ID go to the logs.
            - **Order and edge cases:** a 404 handler (creates an `AppError`) then the 4-argument error handler, registered last; if `res.headersSent` is true, delegate to Express's default handler with `next(err)` so it closes the connection.
        """,
        a_bn=r"""
            আমি **operational error** (প্রত্যাশিত: not found, validation failed, conflict, unauthorized) আর **programmer/অজানা error** (bug, outage) আলাদা করি, আর দুটোই এক জায়গায় handle করি।

            - **`AppError` class:** এতে থাকে `status`, একটি স্থির machine-readable `code` (`NOT_FOUND`, `VALIDATION_FAILED`), client-কে দেখানো নিরাপদ message, optional `details`, আর একটি `expose` flag (4xx-এ true)। Handler শুধু `throw AppError.notFound('User')` করে।
            - **Handler-এ try/catch নেই:** Express 5-এ `async` handler-এ throw হওয়া error বা rejected promise সরাসরি error middleware-এ যায়।
            - **একটি mapping function** পরিচিত library error রূপান্তর করে: `ZodError` → field error সহ 400, body-parser-এর `entity.parse.failed` → 400, `entity.too.large` → 413, PostgreSQL `23505` / MongoDB `11000` → 409, JWT error → 401। অজানা সবকিছু একটি সাধারণ 500।
            - **একই format:** RFC 9457 problem details (`application/problem+json`, যাতে `type`, `title`, `status`, আর আমার `code` ও `errors`)।
            - **কোনো leak নয়:** 5xx-এ client শুধু "Internal Server Error" দেখে; আসল error, stack আর request ID যায় log-এ।
            - **ক্রম ও edge case:** একটি 404 handler (`AppError` তৈরি করে), তারপর 4-argument error handler, সবার শেষে register করা; `res.headersSent` true হলে `next(err)` দিয়ে Express-এর default handler-কে দাও, যাতে সে connection বন্ধ করে।
        """,
        ex_en=r"""
            - **Why stable `code`s:** clients (mobile apps, frontends) branch on `code`, not on message text — messages can be translated or reworded without breaking them.
            - **Logging policy:** 4xx are usually `warn` or not logged individually (they're client mistakes); 5xx are `error` with the full error object and `cause` chain.
            - **Unknown errors are bugs:** after an `uncaughtException` outside the request chain, log and restart the process — don't keep serving in an unknown state.
            - **`headersSent` case:** if a stream fails halfway through a response, you can't send a new status code; Express's default handler destroys the socket so the client sees a broken response instead of corrupted data.
            - **Testing:** each mapping is easy to unit-test with supertest (verified: 404, 400 validation, 409 duplicate, 400 malformed JSON, 413 large body, and a generic 500 that hides the message).
            - Express 4 note (legacy): the same design works, but every `async` handler needed a wrapper or `try/catch` + `next(err)`.
        """,
        ex_bn=r"""
            - **স্থির `code` কেন:** client (mobile app, frontend) message text নয়, `code` দেখে সিদ্ধান্ত নেয় — তাই message অনুবাদ বা পরিবর্তন করলেও কিছু ভাঙে না।
            - **Logging policy:** 4xx সাধারণত `warn` বা আলাদা করে log হয় না (এগুলো client-এর ভুল); 5xx হয় `error`, পুরো error object আর `cause` chain সহ।
            - **অজানা error মানে bug:** request chain-এর বাইরে `uncaughtException` হলে log করে process restart করো — অজানা অবস্থায় serve করতে থাকো না।
            - **`headersSent`-এর ক্ষেত্র:** response-এর মাঝপথে stream fail করলে নতুন status code পাঠানো যায় না; Express-এর default handler socket destroy করে দেয়, ফলে client নষ্ট data নয়, ভাঙা response দেখে।
            - **Testing:** প্রতিটি mapping supertest দিয়ে সহজে unit-test করা যায় (যাচাই করা: 404, 400 validation, 409 duplicate, 400 malformed JSON, 413 বড় body, আর message লুকানো সাধারণ 500)।
            - Express 4 নোট (legacy): একই design কাজ করে, কিন্তু প্রতিটি `async` handler-এ wrapper বা `try/catch` + `next(err)` লাগত।
        """,
        tip_en=r"""Structure it as: error types → where they're thrown → one mapping layer → response format → logging. Mentioning RFC 9457 and the `headersSent` edge case are strong senior signals.""",
        tip_bn=r"""এভাবে সাজাও: error-এর ধরন → কোথায় throw হয় → একটি mapping layer → response format → logging। RFC 9457 আর `headersSent` edge case-এর উল্লেখ senior হওয়ার শক্ত ইঙ্গিত।""",
        mist_en=r"""Sending `err.message` and `err.stack` to clients for 500s, writing `try/catch` in every Express 5 handler, or registering the error handler before the routes.""",
        mist_bn=r"""500-এর ক্ষেত্রে client-কে `err.message` আর `err.stack` পাঠানো, Express 5-এর প্রতিটি handler-এ `try/catch` লেখা, অথবা route-এর আগে error handler register করা।""",
        code=r"""
            import { z, ZodError } from 'zod';

            export class AppError extends Error {
              constructor(status, code, message, { details, cause } = {}) {
                super(message, { cause });
                this.name = 'AppError';
                this.status = status;
                this.code = code;
                this.details = details;
                this.expose = status < 500; // safe to show the message to clients
              }
              static notFound(what = 'Resource') {
                return new AppError(404, 'NOT_FOUND', `${what} not found`);
              }
              static conflict(message) {
                return new AppError(409, 'CONFLICT', message);
              }
            }

            function toAppError(err) {
              if (err instanceof AppError) return err;
              if (err instanceof ZodError) {
                return new AppError(400, 'VALIDATION_FAILED', 'Invalid request', {
                  details: z.flattenError(err).fieldErrors,
                });
              }
              if (err.type === 'entity.parse.failed') return new AppError(400, 'INVALID_JSON', 'Malformed JSON body');
              if (err.type === 'entity.too.large') return new AppError(413, 'PAYLOAD_TOO_LARGE', 'Request body too large');
              if (err.code === '23505') return AppError.conflict('Resource already exists'); // Postgres unique_violation
              return new AppError(500, 'INTERNAL', 'Internal Server Error', { cause: err });
            }

            export function notFoundHandler(req, res, next) {
              next(AppError.notFound(`Route ${req.method} ${req.path}`));
            }

            export function errorHandler(err, req, res, next) {
              if (res.headersSent) return next(err); // response already started: let Express abort it

              const appErr = toAppError(err);
              if (appErr.status >= 500) (req.log ?? console).error({ err }, 'unhandled error');

              res
                .status(appErr.status)
                .type('application/problem+json') // RFC 9457 problem details
                .json({
                  type: `https://api.example.com/problems/${appErr.code.toLowerCase()}`,
                  title: appErr.expose ? appErr.message : 'Internal Server Error',
                  status: appErr.status,
                  code: appErr.code,
                  ...(appErr.details && { errors: appErr.details }),
                  instance: req.originalUrl,
                });
            }

            // In a route (Express 5): no try/catch needed
            // app.get('/users/:id', async (req, res) => {
            //   const user = await users.findById(req.params.id);
            //   if (!user) throw AppError.notFound('User');
            //   res.json(user);
            // });
            // ...after all routes:
            // app.use(notFoundHandler);
            // app.use(errorHandler);
        """,
        lang="javascript",
        follow=[
            ("How would you add the request ID to every error response and log line?", "প্রতিটি error response আর log line-এ request ID কীভাবে যোগ করবে?"),
            ("What should happen on an `uncaughtException` that happens outside any request?", "কোনো request-এর বাইরে `uncaughtException` হলে কী হওয়া উচিত?"),
            ("How do you map JWT verification errors?", "JWT verification error কীভাবে map করবে?"),
        ],
        related=["express-005", "express-008", "express-012"],
        refs=[EX_ERRORS, RFC_9457, OWASP_ERRORS],
    ),
    # ------------------------------------------------------------------ express-007
    Q(
        id="express-007", sub="Deployment", diff="extreme", type="system-design",
        prio="high", market="international", mins=20,
        tags=["system-design", "architecture", "multi-tenant", "scalability", "observability", "express-5"],
        ver="Express 5.x; Node.js 24 LTS / 26", vs=False, status="stable",
        q_en=r"""Design the backend for a multi-tenant B2B SaaS REST API built with Express 5: about 3,000 requests per second at peak, strict tenant data isolation, 99.9% availability, and a small team that must ship features quickly. Describe the application structure, the middleware stack, how it scales, and how you'd operate it in production.""",
        q_bn=r"""Express 5 দিয়ে একটি multi-tenant B2B SaaS REST API-এর backend design করো: peak-এ প্রায় প্রতি সেকেন্ডে 3,000 request, কঠোর tenant data isolation, 99.9% availability, আর একটি ছোট team যাদের দ্রুত feature ship করতে হবে। Application structure, middleware stack, কীভাবে scale করবে, আর production-এ কীভাবে চালাবে — বর্ণনা করো।""",
        a_en=r"""
            *(Advanced, senior-level answer.)*

            **Application structure** — a modular monolith first (fastest for a small team): feature modules (`billing`, `users`, `projects`), each with routes → controllers (HTTP only) → services (business rules) → repositories (DB access). A `createApp(deps)` factory builds the Express app with injected dependencies, so tests and workers can reuse it without `listen()`.

            **Middleware stack (order matters):** request ID + `pino-http` logging → `helmet` → `cors` with an allow-list → `express.json({ limit })` → health routes (public) → rate limiting (Redis store, per tenant and per IP) → authentication (JWT verification) → **tenant resolution** (tenant from the token, never from a client-controlled header alone) → versioned routers (`/v1`) with per-route validation (zod) and authorization → 404 → centralized error handler.

            **Tenant isolation:** every table has `tenant_id`; repositories always scope queries by the tenant from the request context (AsyncLocalStorage), and PostgreSQL Row-Level Security acts as a second guard. Large tenants can later move to a dedicated database without changing the API.

            **Scaling:** stateless containers (one Node process each) behind an ALB/NGINX with `trust proxy` set correctly; autoscale on CPU and p95 latency. PostgreSQL primary + read replicas behind PgBouncer; Redis for cache, rate limits and sessions/token deny-lists. Slow or heavy work (emails, exports, webhooks) goes to a queue and separate workers.

            **Operations:** health/readiness endpoints and graceful shutdown; structured logs, metrics (RED: rate, errors, duration) and OpenTelemetry traces with request IDs; SLO-based alerts; zero-downtime rolling deploys with expand/contract migrations; feature flags; OpenAPI contract tests in CI; dependency and container scanning.
        """,
        a_bn=r"""
            *(Advanced, senior-level উত্তর।)*

            **Application structure** — শুরুতে একটি modular monolith (ছোট team-এর জন্য সবচেয়ে দ্রুত): feature module (`billing`, `users`, `projects`), প্রতিটিতে route → controller (শুধু HTTP) → service (business rule) → repository (DB access)। একটি `createApp(deps)` factory inject করা dependency দিয়ে Express app বানায়, ফলে test আর worker `listen()` ছাড়াই এটা পুনরায় ব্যবহার করতে পারে।

            **Middleware stack (ক্রম গুরুত্বপূর্ণ):** request ID + `pino-http` logging → `helmet` → allow-list সহ `cors` → `express.json({ limit })` → health route (public) → rate limiting (Redis store, tenant ও IP অনুযায়ী) → authentication (JWT verification) → **tenant resolution** (token থেকে tenant, কখনো শুধু client-নিয়ন্ত্রিত header থেকে নয়) → per-route validation (zod) আর authorization সহ versioned router (`/v1`) → 404 → centralized error handler।

            **Tenant isolation:** প্রতিটি table-এ `tenant_id`; repository সবসময় request context (AsyncLocalStorage) থেকে পাওয়া tenant দিয়ে query scope করে, আর দ্বিতীয় পাহারা হিসেবে PostgreSQL Row-Level Security। বড় tenant-কে পরে API না বদলেই আলাদা database-এ সরানো যায়।

            **Scaling:** stateless container (প্রতিটিতে একটি Node process), ALB/NGINX-এর পেছনে সঠিকভাবে `trust proxy` set করে; CPU আর p95 latency দেখে autoscale। PgBouncer-এর পেছনে PostgreSQL primary + read replica; cache, rate limit আর session/token deny-list-এর জন্য Redis। ধীর বা ভারী কাজ (email, export, webhook) queue আর আলাদা worker-এ যায়।

            **Operations:** health/readiness endpoint আর graceful shutdown; structured log, metric (RED: rate, errors, duration) আর request ID সহ OpenTelemetry trace; SLO-ভিত্তিক alert; expand/contract migration সহ zero-downtime rolling deploy; feature flag; CI-তে OpenAPI contract test; dependency আর container scanning।
        """,
        ex_en=r"""
            **Capacity sanity check:** 3,000 rps across, say, 6–10 instances is a few hundred rps per Node process — comfortable for I/O-bound handlers if nothing blocks the event loop. The database is usually the bottleneck, so caching hot reads and keeping queries indexed matters more than the framework.

            **Failure scenarios:**
            - Redis down → rate limiter and cache must fail in a defined way (fail-open for cache, a decision for rate limits) with timeouts, not hang requests.
            - One noisy tenant → per-tenant rate limits and quotas; move heavy tenants to dedicated workers or databases.
            - Bad deploy → canary + automatic rollback on error-rate SLO.
            - DB failover → connection retry with backoff; idempotency keys on unsafe POSTs so client retries are safe.

            **Trade-offs:** a modular monolith keeps deployment simple; split out a service only when a module needs independent scaling or ownership. RLS adds safety but complicates connection pooling (set the tenant per transaction).

            **Security:** OWASP API Top 10 — broken object-level authorization is the classic multi-tenant bug, so every repository call takes the tenant and checks ownership.
        """,
        ex_bn=r"""
            **Capacity-র মোটা হিসাব:** ধরো 6–10টি instance-এ 3,000 rps মানে প্রতি Node process-এ কয়েকশো rps — event loop block না হলে I/O-bound handler-এর জন্য এটা স্বচ্ছন্দ। সাধারণত database-ই bottleneck, তাই framework-এর চেয়ে hot read cache করা আর query indexed রাখা বেশি গুরুত্বপূর্ণ।

            **Failure scenario:**
            - Redis down → rate limiter আর cache-কে নির্ধারিত উপায়ে fail করতে হবে (cache-এর জন্য fail-open, rate limit-এর জন্য একটি সিদ্ধান্ত), timeout সহ — request ঝুলিয়ে নয়।
            - একটি noisy tenant → per-tenant rate limit আর quota; ভারী tenant-কে dedicated worker বা database-এ সরানো।
            - খারাপ deploy → canary + error-rate SLO দেখে স্বয়ংক্রিয় rollback।
            - DB failover → backoff সহ connection retry; unsafe POST-এ idempotency key, যাতে client retry নিরাপদ হয়।

            **Trade-off:** modular monolith deployment সহজ রাখে; কোনো module-এর আলাদা scaling বা ownership দরকার হলেই কেবল আলাদা service বানাও। RLS নিরাপত্তা বাড়ায় কিন্তু connection pooling জটিল করে (প্রতি transaction-এ tenant set করতে হয়)।

            **Security:** OWASP API Top 10 — broken object-level authorization হলো multi-tenant-এর classic bug, তাই প্রতিটি repository call tenant নেয় এবং ownership check করে।
        """,
        tip_en=r"""Start with requirements and a rough capacity estimate, then walk the request path through the middleware stack, then data isolation, then scaling and operations. Naming failure modes (Redis down, noisy tenant) is what makes it senior.""",
        tip_bn=r"""Requirement আর মোটা capacity হিসাব দিয়ে শুরু করো, তারপর middleware stack ধরে request-এর পথ দেখাও, তারপর data isolation, তারপর scaling আর operations। Failure mode-এর নাম বলা (Redis down, noisy tenant) উত্তরটাকে senior মানের করে।""",
        mist_en=r"""Starting with microservices for a small team, trusting an `X-Tenant-Id` header from the client, or keeping sessions/rate-limit counters in process memory while running many instances.""",
        mist_bn=r"""ছোট team নিয়ে microservices দিয়ে শুরু করা, client-এর পাঠানো `X-Tenant-Id` header বিশ্বাস করা, অথবা অনেক instance চালিয়েও session/rate-limit counter process memory-তে রাখা।""",
        code=r"""
            // app.js — composition root (no listen() here, so tests and workers can import it)
            import express from 'express';
            import helmet from 'helmet';
            import cors from 'cors';
            import { pinoHttp } from 'pino-http';
            import { rateLimit } from 'express-rate-limit';

            export function createApp({ config, logger, deps }) {
              const app = express();
              app.set('trust proxy', 1); // exactly one proxy (ALB/NGINX) in front

              app.use(pinoHttp({ logger, genReqId: deps.requestId }));
              app.use(helmet());
              app.use(cors({ origin: config.corsOrigins, credentials: true }));
              app.use(express.json({ limit: '1mb' }));

              app.use('/health', deps.healthRouter);                // public, cheap
              app.use('/v1', rateLimit({
                windowMs: 60_000, limit: 600, standardHeaders: 'draft-8', legacyHeaders: false,
                store: deps.rateLimitStore,                         // Redis-backed, shared by all instances
              }));
              app.use('/v1', deps.authenticate, deps.resolveTenant, deps.v1Router);

              app.use(deps.notFoundHandler);
              app.use(deps.errorHandler);
              return app;
            }
        """,
        lang="javascript",
        follow=[
            ("How would you enforce tenant isolation if a developer forgets the `tenant_id` filter?", "কোনো developer `tenant_id` filter দিতে ভুলে গেলে tenant isolation কীভাবে নিশ্চিত করবে?"),
            ("When would you split this modular monolith into services?", "কখন এই modular monolith-কে আলাদা service-এ ভাগ করবে?"),
            ("How do you decide whether the rate limiter fails open or closed when Redis is down?", "Redis down হলে rate limiter fail-open নাকি fail-closed হবে কীভাবে ঠিক করবে?"),
        ],
        related=["express-006", "express-014", "express-018"],
        refs=[EX_PERF, EX_SECURITY, OWASP_REST],
    ),
]

if __name__ == "__main__":
    save("express", "b1", QUESTIONS)
