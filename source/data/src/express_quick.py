import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

EX_HELLO = ("Express — Hello world example", "https://expressjs.com/en/starter/hello-world.html")
EX_USING_MW = ("Express — Using middleware", "https://expressjs.com/en/guide/using-middleware.html")
EX_ROUTING = ("Express — Routing (express.Router)", "https://expressjs.com/en/guide/routing.html")
EX_API5 = ("Express 5.x — API reference", "https://expressjs.com/en/5x/api.html")
EX_ERRORS = ("Express — Error handling", "https://expressjs.com/en/guide/error-handling.html")
EX_CORS = ("Express — cors middleware", "https://expressjs.com/en/resources/middleware/cors.html")
EX_FAQ = ("Express — FAQ (How should I structure my application?)", "https://expressjs.com/en/starter/faq.html")
MDN_STATUS = ("MDN — HTTP response status codes", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status")
EX_STATIC = ("Express — Serving static files", "https://expressjs.com/en/starter/static-files.html")

VER = "Express 5.x (5.3)"

QUESTIONS = [
    # ------------------------------------------------------------------ express-q01
    Q(
        id="express-q01", sub="Request & Response Lifecycle", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["express", "framework", "node-http"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is Express.js, and why use it instead of Node's built-in `http` module?""",
        q_bn=r"""Express.js কী, আর Node-এর built-in `http` module-এর বদলে কেন এটা ব্যবহার করো?""",
        a_en=r"""Express is a minimal web framework for Node.js that sits on top of the `http` module. It adds routing by method and path, a middleware pipeline, and helpers like `res.json()` and `req.params`, so you don't parse URLs and bodies or set headers by hand. Express 5 is the current version.""",
        a_bn=r"""Express হলো Node.js-এর একটা minimal web framework, যেটা `http` module-এর উপর চলে। এটা method আর path ধরে routing, middleware pipeline, আর `res.json()`, `req.params`-এর মতো helper দেয়, তাই URL বা body নিজে parse করতে বা header হাতে set করতে হয় না। বর্তমান version হলো Express 5।""",
        code=r"""
            import express from 'express';
            const app = express();
            app.use(express.json());
            app.get('/health', (req, res) => res.json({ ok: true })); // → {"ok":true}
            app.listen(3000);
        """, lang="javascript",
        ex_en=r"""It is unopinionated: no fixed folder structure, ORM or validation, so you choose the libraries. Frameworks like NestJS can run on top of Express.""",
        ex_bn=r"""Express unopinionated: নির্দিষ্ট folder structure, ORM বা validation নেই, library তুমি নিজে বেছে নাও। NestJS-এর মতো framework Express-এর উপরেও চলতে পারে।""",
        tip_en=r"""Name the three things it adds: routing, middleware and request/response helpers.""",
        tip_bn=r"""এটা যে তিনটা জিনিস যোগ করে সেগুলো বলো: routing, middleware আর request/response helper।""",
        follow=[("What does `express.json()` do?", "`express.json()` কী করে?")],
        related=["express-001"],
        refs=[EX_HELLO],
    ),
    # ------------------------------------------------------------------ express-q02
    Q(
        id="express-q02", sub="Middleware", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["app-use", "app-get", "routing", "middleware"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `app.use()` and `app.get()`?""",
        q_bn=r"""`app.use()` আর `app.get()`-এর পার্থক্য কী?""",
        a_en=r"""`app.use(path, fn)` mounts middleware for **every HTTP method** and every path that **starts with** `path` (default `/`), so it's used for parsers, auth, logging and routers. `app.get(path, fn)` is a route: it runs only for **GET** requests whose path matches exactly.""",
        a_bn=r"""`app.use(path, fn)` middleware mount করে **সব HTTP method**-এর জন্য, আর যেসব path `path` দিয়ে **শুরু হয়** সেগুলোর জন্য (default `/`), তাই parser, auth, logging আর router-এর জন্য এটা ব্যবহার হয়। `app.get(path, fn)` হলো route: এটা শুধু সেইসব **GET** request-এ চলে যাদের path হুবহু মেলে।""",
        code=r"""
            app.use('/api', logRequest);           // GET /api, POST /api, GET /api/users ...
            app.get('/api', (req, res) => res.send('get /api'));
            // GET  /api       → logRequest, then "get /api"
            // POST /api       → logRequest only (then 404)
            // GET  /api/users → logRequest only (then 404)
        """, lang="javascript",
        ex_en=r"""Inside `app.use('/api', fn)`, `req.url` has the mount path stripped; use `req.originalUrl` for the full URL.""",
        ex_bn=r"""`app.use('/api', fn)`-এর ভেতরে `req.url` থেকে mount path বাদ যায়; পুরো URL-এর জন্য `req.originalUrl` ব্যবহার করো।""",
        tip_en=r"""Say "use = prefix match, any method; get = exact path, GET only" and give one example of each.""",
        tip_bn=r"""বলো "use = prefix match, যেকোনো method; get = হুবহু path, শুধু GET", আর প্রতিটার একটা example দাও।""",
        follow=[("What does `app.all()` do?", "`app.all()` কী করে?")],
        related=["express-001", "express-004"],
        refs=[EX_USING_MW],
    ),
    # ------------------------------------------------------------------ express-q03
    Q(
        id="express-q03", sub="Routing (Express 5 Path Syntax)", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["router", "express-router", "mergeparams", "modular"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is `express.Router()`, and why use it?""",
        q_bn=r"""`express.Router()` কী, আর কেন ব্যবহার করো?""",
        a_en=r"""`express.Router()` creates a mini-app with its own routes and middleware that you mount on a path with `app.use('/users', usersRouter)`. It splits a big app into one file per feature and lets you apply middleware (like auth) to just that group. Use `{ mergeParams: true }` when a nested router needs the parent's params.""",
        a_bn=r"""`express.Router()` নিজস্ব route আর middleware-সহ একটা mini-app তৈরি করে, যেটা `app.use('/users', usersRouter)` দিয়ে একটা path-এ mount করা হয়। এতে বড় app feature অনুযায়ী আলাদা file-এ ভাগ হয়, আর শুধু ওই group-এ middleware (যেমন auth) লাগানো যায়। Nested router-এ parent-এর params লাগলে `{ mergeParams: true }` দাও।""",
        code=r"""
            const comments = express.Router({ mergeParams: true });
            comments.get('/', (req, res) => res.json({ postId: req.params.postId }));

            const posts = express.Router();
            posts.use('/:postId/comments', comments);
            app.use('/posts', posts);
            // GET /posts/7/comments → {"postId":"7"}
        """, lang="javascript",
        ex_en=r"""Without `mergeParams`, `req.params.postId` would be missing inside `comments`. Routers also use Express 5 path syntax.""",
        ex_bn=r"""`mergeParams` না দিলে `comments`-এর ভেতরে `req.params.postId` পাওয়া যেত না। Router-এও Express 5-এর path syntax চলে।""",
        tip_en=r"""Describe your usual layout: one router per resource, mounted in `app.js` under a version prefix like `/v1`.""",
        tip_bn=r"""তোমার সাধারণ layout বলো: প্রতি resource-এর জন্য একটা router, `app.js`-এ `/v1`-এর মতো version prefix-এর নিচে mount করা।""",
        follow=[("How would you protect every route in one router with an auth middleware?", "একটা router-এর সব route-এ কীভাবে auth middleware লাগাবে?")],
        related=["express-029", "express-007"],
        refs=[EX_ROUTING],
    ),
    # ------------------------------------------------------------------ express-q04
    Q(
        id="express-q04", sub="Request & Response Lifecycle", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["req-params", "req-query", "req-body"],
        ver=VER, vs=True, status="stable",
        q_en=r"""For the route `app.get('/users/:id', ...)` and the request `GET /users/42?sort=name`, what are `req.params`, `req.query` and `req.body`?""",
        q_bn=r"""`app.get('/users/:id', ...)` route আর `GET /users/42?sort=name` request-এর জন্য `req.params`, `req.query` আর `req.body` কী হবে?""",
        a_en=r"""`req.params` is `{ id: '42' }` (from the path), `req.query` is `{ sort: 'name' }` (from the query string) and `req.body` is `undefined`: a GET has no body here and no body parser ran. In Express 5 `req.body` stays `undefined` until a parser like `express.json()` runs, and all params and query values are strings.""",
        a_bn=r"""`req.params` হবে `{ id: '42' }` (path থেকে), `req.query` হবে `{ sort: 'name' }` (query string থেকে), আর `req.body` হবে `undefined`: এখানে GET-এর কোনো body নেই, body parser-ও চলেনি। Express 5-এ `express.json()`-এর মতো parser না চলা পর্যন্ত `req.body` `undefined` থাকে, আর params ও query-র সব value string।""",
        code=r"""
            app.get('/users/:id', (req, res) => {
              res.json({ params: req.params, query: req.query, body: req.body });
            });
            // GET /users/42?sort=name → {"params":{"id":"42"},"query":{"sort":"name"}}
            // (body is undefined, so JSON.stringify leaves it out)
        """, lang="javascript",
        ex_en=r"""`'42'` is a string, so convert it (`Number(req.params.id)`) or validate with a schema before using it.""",
        ex_bn=r"""`'42'` একটা string, তাই ব্যবহারের আগে convert করো (`Number(req.params.id)`) বা schema দিয়ে validate করো।""",
        tip_en=r"""Map each one to its source: path → params, `?query` → query, request body + parser → body.""",
        tip_bn=r"""প্রতিটাকে তার উৎসের সাথে মিলিয়ে বলো: path → params, `?query` → query, request body + parser → body।""",
        follow=[("What is `req.query` for `?tag=a&tag=b`?", "`?tag=a&tag=b` হলে `req.query` কী হবে?")],
        related=["express-003", "express-004"],
        refs=[EX_API5],
    ),
    # ------------------------------------------------------------------ express-q05
    Q(
        id="express-q05", sub="Request & Response Lifecycle", diff="easy", type="quick",
        prio="medium", market="both", mins=2,
        tags=["res-send", "res-json", "res-sendstatus", "response"],
        ver=VER, vs=True, status="stable",
        q_en=r"""What is the difference between `res.send()`, `res.json()` and `res.sendStatus()`?""",
        q_bn=r"""`res.send()`, `res.json()` আর `res.sendStatus()`-এর পার্থক্য কী?""",
        a_en=r"""`res.send(body)` sends a string, Buffer or object and guesses the `Content-Type` (a string becomes `text/html`). `res.json(data)` always sends JSON with `application/json`. `res.sendStatus(code)` sets the status and sends its standard text, like `204` with an empty body; to set a status with a body, chain `res.status(201).json(data)`.""",
        a_bn=r"""`res.send(body)` string, Buffer বা object পাঠায় আর `Content-Type` অনুমান করে নেয় (string হলে `text/html`)। `res.json(data)` সবসময় `application/json`-সহ JSON পাঠায়। `res.sendStatus(code)` status set করে তার standard text পাঠায়, যেমন `204` হলে খালি body; body-সহ status দিতে chain করো `res.status(201).json(data)`।""",
        code=r"""
            app.get('/a', (req, res) => res.send('<p>hi</p>'));       // 200 text/html
            app.get('/b', (req, res) => res.json({ ok: true }));      // 200 application/json
            app.delete('/c', (req, res) => res.sendStatus(204));      // 204, empty body
            app.post('/d', (req, res) => res.status(201).json({ id: 1 }));
        """, lang="javascript",
        ex_en=r"""Express 5 gotcha: `res.send(404)` no longer sets the status; it responds `200` with the body `404`. Use `res.sendStatus(404)`.""",
        ex_bn=r"""Express 5-এর ফাঁদ: `res.send(404)` এখন আর status set করে না; এটা `200` দেয় আর body-তে `404` পাঠায়। `res.sendStatus(404)` ব্যবহার করো।""",
        tip_en=r"""Say that for APIs you use `res.status(...).json(...)`, and mention the Express 5 `res.send(number)` change.""",
        tip_bn=r"""বলো API-তে তুমি `res.status(...).json(...)` ব্যবহার করো, আর Express 5-এর `res.send(number)` পরিবর্তনটা উল্লেখ করো।""",
        follow=[("What happens if you call `res.json()` twice in one handler?", "একটা handler-এ দুবার `res.json()` call করলে কী হয়?")],
        related=["express-030", "express-011"],
        refs=[EX_API5],
    ),
    # ------------------------------------------------------------------ express-q06
    Q(
        id="express-q06", sub="Error-Handling Middleware", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["error-handling", "async", "express5", "middleware"],
        ver=VER, vs=True, status="version-specific",
        q_en=r"""How do you handle errors in Express 5? Do async route handlers still need `try/catch` or an `asyncHandler` wrapper?""",
        q_bn=r"""Express 5-এ error কীভাবে handle করো? Async route handler-এ কি এখনো `try/catch` বা `asyncHandler` wrapper লাগে?""",
        a_en=r"""No: in Express 5, if an `async` handler throws or a promise rejects, Express passes the error to `next(err)` automatically. You write one error-handling middleware with four arguments, `(err, req, res, next)`, register it after all routes, and send the error response there. In Express 4 you needed `try/catch` + `next(err)` or a wrapper.""",
        a_bn=r"""না: Express 5-এ `async` handler throw করলে বা promise reject হলে Express নিজেই error-টা `next(err)`-এ পাঠায়। চার argument-এর একটা error-handling middleware লেখো, `(err, req, res, next)`, সব route-এর পরে register করো, আর সেখান থেকেই error response পাঠাও। Express 4-এ `try/catch` + `next(err)` বা wrapper লাগত।""",
        code=r"""
            app.get('/users/:id', async (req, res) => {
              const user = await db.findUser(req.params.id); // rejects: "DB down"
              res.json(user);
            });
            app.use((err, req, res, next) => {
              res.status(err.status ?? 500).json({ error: 'Internal Server Error' });
            }); // → 500 {"error":"Internal Server Error"}
        """, lang="javascript",
        ex_en=r"""The error handler must have exactly four parameters, or Express treats it as normal middleware. Log the real error, but don't send stack traces to clients.""",
        ex_bn=r"""Error handler-এ ঠিক চারটা parameter থাকতে হবে, নইলে Express এটাকে সাধারণ middleware ধরে। আসল error log করো, কিন্তু client-কে stack trace পাঠিও না।""",
        tip_en=r"""Say "Express 5 forwards rejected promises", then show the four-argument handler registered last.""",
        tip_bn=r"""বলো "Express 5 rejected promise নিজেই forward করে", তারপর শেষে register করা চার argument-এর handler-টা দেখাও।""",
        follow=[("Why must the error handler be registered after the routes?", "Error handler কেন route-গুলোর পরে register করতে হয়?")],
        related=["express-005", "express-008", "express-006"],
        refs=[EX_ERRORS],
    ),
    # ------------------------------------------------------------------ express-q07
    Q(
        id="express-q07", sub="CORS", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["cors", "same-origin", "browser", "middleware"],
        ver="Express 5.x (5.3), cors 2.x", vs=False, status="stable",
        q_en=r"""What is CORS, and how do you enable it in an Express API?""",
        q_bn=r"""CORS কী, আর Express API-তে কীভাবে চালু করো?""",
        a_en=r"""CORS (Cross-Origin Resource Sharing) is how a server tells the **browser** that JavaScript from another origin (a different scheme, host or port) may read its responses. Browsers block those reads by default. In Express, use the `cors` middleware with an allow-list of your frontend origins, registered before the routes.""",
        a_bn=r"""CORS (Cross-Origin Resource Sharing) হলো server-এর **browser**-কে জানানোর উপায় যে অন্য origin (আলাদা scheme, host বা port) থেকে আসা JavaScript তার response পড়তে পারবে। Browser default-এ এই পড়া block করে। Express-এ route-এর আগে `cors` middleware register করো, frontend origin-গুলোর একটা allow-list দিয়ে।""",
        code=r"""
            import cors from 'cors';
            app.use(cors({ origin: ['http://localhost:5173'] }));
            // request from that origin → Access-Control-Allow-Origin: http://localhost:5173
            // request from any other origin → no CORS header, so the browser blocks the read
        """, lang="javascript",
        ex_en=r"""CORS is not security for your API: `curl` and servers ignore it, so you still need authentication. With cookies, `origin: '*'` is not allowed; list exact origins and set `credentials: true`.""",
        ex_bn=r"""CORS তোমার API-র security নয়: `curl` বা server এটা মানে না, তাই authentication লাগবেই। Cookie থাকলে `origin: '*'` চলে না; নির্দিষ্ট origin দাও আর `credentials: true` set করো।""",
        tip_en=r"""Say the browser enforces it and the server grants it with response headers; a client-side fix can't solve it.""",
        tip_bn=r"""বলো browser এটা enforce করে আর server response header দিয়ে অনুমতি দেয়; client-এ কিছু করে এটা সমাধান হয় না।""",
        follow=[("What is a preflight request?", "Preflight request কী?")],
        related=["express-015", "express-017"],
        refs=[EX_CORS],
    ),
    # ------------------------------------------------------------------ express-q08
    Q(
        id="express-q08", sub="Project Structure", diff="easy", type="quick",
        prio="medium", market="both", mins=2,
        tags=["mvc", "architecture", "controllers", "services"],
        ver="Version-independent concept (Express 5.x)", vs=False, status="stable",
        q_en=r"""How do you structure an Express project? What is MVC in an Express API?""",
        q_bn=r"""Express project কীভাবে সাজাও? Express API-তে MVC কী?""",
        a_en=r"""MVC splits code into **Models** (data and database access), **Views** (the output: HTML templates, or JSON in an API) and **Controllers** (handle the request and call the model). In APIs I add a **service** layer for business logic: routes → controllers (HTTP only) → services → models/repositories, so each layer is easy to test and change.""",
        a_bn=r"""MVC code-কে ভাগ করে **Model** (data আর database access), **View** (output: HTML template, API-তে JSON) আর **Controller** (request সামলায়, model-কে call করে)-এ। API-তে আমি business logic-এর জন্য একটা **service** layer যোগ করি: route → controller (শুধু HTTP) → service → model/repository, যাতে প্রতিটা layer সহজে test আর পরিবর্তন করা যায়।""",
        code=r"""
            src/
              routes/users.routes.js        # URL + method → controller
              controllers/users.controller.js # read req, call service, send res
              services/users.service.js     # business rules
              models/user.model.js          # schema / DB access
              middlewares/  app.js  server.js
        """, lang="text",
        ex_en=r"""Express doesn't force any structure. Keep `req`/`res` out of services so the same logic works from tests, jobs and other routes.""",
        ex_bn=r"""Express কোনো structure চাপিয়ে দেয় না। Service-এ `req`/`res` রেখো না, যাতে একই logic test, job আর অন্য route থেকেও চলে।""",
        tip_en=r"""Draw the request path through the layers and say what each one is not allowed to do.""",
        tip_bn=r"""Layer-গুলোর মধ্য দিয়ে request-এর পথটা এঁকে দেখাও, আর বলো কোন layer কী করতে পারবে না।""",
        follow=[("Why split `app.js` (the app) from `server.js` (the `listen()` call)?", "`app.js` (app) আর `server.js` (`listen()` call) আলাদা রাখো কেন?")],
        related=["express-007", "express-026"],
        refs=[EX_FAQ],
    ),
    # ------------------------------------------------------------------ express-q09
    Q(
        id="express-q09", sub="REST APIs", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["status-codes", "http", "rest"],
        ver="Version-independent concept (HTTP, RFC 9110)", vs=False, status="stable",
        q_en=r"""Which HTTP status codes should a REST API commonly return?""",
        q_bn=r"""একটা REST API সাধারণত কোন কোন HTTP status code return করে?""",
        a_en=r"""Success: `200 OK` (read or update), `201 Created` (after POST), `204 No Content` (delete). Client errors: `400` (invalid input), `401` (not logged in), `403` (logged in but not allowed), `404` (not found), `409` (conflict, like a duplicate email), `429` (too many requests). Server errors: `500` for unexpected bugs.""",
        a_bn=r"""সফল হলে: `200 OK` (read বা update), `201 Created` (POST-এর পরে), `204 No Content` (delete)। Client-এর ভুল: `400` (ভুল input), `401` (login করা নেই), `403` (login আছে কিন্তু অনুমতি নেই), `404` (পাওয়া যায়নি), `409` (conflict, যেমন duplicate email), `429` (অনেক বেশি request)। Server-এর ভুল: অপ্রত্যাশিত bug-এ `500`।""",
        code=r"""
            res.status(201).json(newUser);              // created
            res.sendStatus(204);                        // deleted, no body
            res.status(404).json({ error: 'User not found' });
        """, lang="javascript",
        ex_en=r"""Remember the families: 2xx success, 3xx redirect, 4xx the client's fault, 5xx the server's fault. Don't return `200` with `{ error: ... }`.""",
        ex_bn=r"""Family-গুলো মনে রাখো: 2xx সফল, 3xx redirect, 4xx client-এর ভুল, 5xx server-এর ভুল। `{ error: ... }`-সহ `200` return কোরো না।""",
        tip_en=r"""Explain `401` vs `403` clearly; it's the most common follow-up.""",
        tip_bn=r"""`401` আর `403`-এর পার্থক্য পরিষ্কার করে বলো; এটাই সবচেয়ে সাধারণ follow-up।""",
        follow=[("What is the difference between `401` and `403`?", "`401` আর `403`-এর পার্থক্য কী?")],
        related=["express-009", "express-022"],
        refs=[MDN_STATUS],
    ),
    # ------------------------------------------------------------------ express-q10
    Q(
        id="express-q10", sub="Middleware", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["express-static", "static-files", "middleware"],
        ver=VER, vs=True, status="stable",
        q_en=r"""How do you serve static files (images, CSS, a built frontend) with Express?""",
        q_bn=r"""Express দিয়ে static file (image, CSS, build করা frontend) কীভাবে serve করো?""",
        a_en=r"""Use the built-in `express.static` middleware: `app.use(express.static('public'))` serves files from the `public` folder, so `public/logo.png` is available at `/logo.png`. Add a prefix with `app.use('/assets', express.static('public'))`. In Express 5 dotfiles and dot-folders (like `/.well-known`) are not served by default.""",
        a_bn=r"""Built-in `express.static` middleware ব্যবহার করো: `app.use(express.static('public'))` `public` folder থেকে file serve করে, তাই `public/logo.png` পাওয়া যায় `/logo.png`-এ। Prefix দিতে `app.use('/assets', express.static('public'))`। Express 5-এ dotfile আর dot-folder (যেমন `/.well-known`) default-এ serve হয় না।""",
        code=r"""
            import path from 'node:path';
            app.use(express.static(path.join(import.meta.dirname, 'public')));
            // public/hello.txt → GET /hello.txt → 200 "hello"
        """, lang="javascript",
        ex_en=r"""Use an absolute path so it works from any working directory. In production, NGINX or a CDN often serves static files instead.""",
        ex_bn=r"""Absolute path দাও যাতে যেকোনো working directory থেকে চলে। Production-এ প্রায়ই NGINX বা CDN static file serve করে।""",
        tip_en=r"""Show the one-liner, then mention absolute paths and serving through a CDN in production.""",
        tip_bn=r"""এক লাইনের code-টা দেখাও, তারপর absolute path আর production-এ CDN দিয়ে serve করার কথা বলো।""",
        follow=[("How would you serve a React SPA so that deep links like `/dashboard` work?", "React SPA এমনভাবে কীভাবে serve করবে যাতে `/dashboard`-এর মতো deep link কাজ করে?")],
        related=["express-002", "express-031"],
        refs=[EX_STATIC],
    ),
]

save("express", "quick", QUESTIONS)
