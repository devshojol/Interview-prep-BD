import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

EX_ERRORS = ("Express — Error handling", "https://expressjs.com/en/guide/error-handling.html")
EX_WRITING_MW = ("Express — Writing middleware", "https://expressjs.com/en/guide/writing-middleware.html")
EX_API5 = ("Express 5.x — API reference", "https://expressjs.com/en/5x/api.html")
MDN_STATUS = ("MDN — HTTP response status codes", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status")
MDN_IDEMPOTENT = ("MDN — Idempotent", "https://developer.mozilla.org/en-US/docs/Glossary/Idempotent")
RFC_9110 = ("RFC 9110 — HTTP Semantics", "https://www.rfc-editor.org/rfc/rfc9110")
NODE_ERRORS = ("Node.js API — Errors (ERR_HTTP_HEADERS_SENT)", "https://nodejs.org/api/errors.html")
ZOD_API = ("Zod — Defining schemas", "https://zod.dev/api")
ZOD_ERRORS = ("Zod — Formatting errors", "https://zod.dev/error-formatting")
OWASP_INPUT = ("OWASP — Input Validation Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html")
EX_MULTER = ("Express — multer middleware", "https://expressjs.com/en/resources/middleware/multer.html")
OWASP_UPLOAD = ("OWASP — File Upload Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html")
EX_PROXIES = ("Express — Express behind proxies", "https://expressjs.com/en/guide/behind-proxies.html")

QUESTIONS = [
    # ------------------------------------------------------------------ express-008
    Q(
        id="express-008", sub="Error-Handling Middleware", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["error-middleware", "arity", "express-basics"],
        ver="Express 4.x and 5.x", vs=False, status="stable",
        q_en=r"""Which of these does Express treat as **error-handling middleware**?""",
        q_bn=r"""নিচের কোনটিকে Express **error-handling middleware** হিসেবে গণ্য করে?""",
        options=[
            ("`app.use((req, res, next) => { if (res.statusCode >= 400) res.json({ error: true }); })`", "`app.use((req, res, next) => { if (res.statusCode >= 400) res.json({ error: true }); })`"),
            ("`app.use((err, req, res, next) => { res.status(500).json({ error: 'Something broke' }); })`", "`app.use((err, req, res, next) => { res.status(500).json({ error: 'Something broke' }); })`"),
            ("`app.use((err, req, res) => { res.status(500).json({ error: 'Something broke' }); })`", "`app.use((err, req, res) => { res.status(500).json({ error: 'Something broke' }); })`"),
            ("`app.on('error', (err) => { console.error(err); })`", "`app.on('error', (err) => { console.error(err); })`"),
        ],
        correct=1,
        a_en=r"""
            The four-argument function `(err, req, res, next)`. Express identifies error-handling middleware by its **arity** — the function must declare exactly four parameters. It is skipped during normal processing and only runs when an error is passed with `next(err)` (or, in Express 5, when a handler throws or returns a rejected promise).
        """,
        a_bn=r"""
            চার argument-এর function `(err, req, res, next)`। Express error-handling middleware চেনে তার **arity** দেখে — function-টিতে ঠিক চারটি parameter declare করা থাকতে হবে। স্বাভাবিক processing-এ এটা বাদ পড়ে, শুধু `next(err)` দিয়ে error পাঠালে (বা Express 5-এ handler throw করলে বা rejected promise return করলে) চলে।
        """,
        ex_en=r"""
            Option C is the classic trap: with only three parameters Express treats it as **normal** middleware, and the names don't matter — `err` actually receives `req`, `req` receives `res`, and `res` receives `next`. When an error happens it's skipped, and Express's default handler responds with an HTML error page; for an unmatched route it runs with shifted arguments and throws `TypeError: res.status is not a function`, which Express then turns into its default 500 HTML page (verified on Express 5.3).

            So keep the fourth `next` parameter even if you don't use it (linters may complain — disable the rule for that line rather than removing the parameter).

            Other rules: register error handlers **after** all routes; you can chain several (e.g. one for logging that calls `next(err)`, one that responds); and if `res.headersSent` is true, delegate with `next(err)`.
        """,
        ex_bn=r"""
            Option C হলো classic ফাঁদ: মাত্র তিনটি parameter থাকলে Express একে **সাধারণ** middleware ধরে, আর নামের কোনো গুরুত্ব নেই — `err` আসলে পায় `req`, `req` পায় `res`, আর `res` পায় `next`। Error হলে এটা বাদ পড়ে এবং Express-এর default handler একটি HTML error page দিয়ে response দেয়; আর অমিল route-এ এটা সরে যাওয়া argument নিয়ে চলে এবং `TypeError: res.status is not a function` throw করে, যাকে Express তারপর তার default 500 HTML page-এ পরিণত করে (Express 5.3-এ যাচাই করা)।

            তাই চতুর্থ `next` parameter ব্যবহার না করলেও রেখে দাও (linter আপত্তি করলে parameter না সরিয়ে ওই line-এর জন্য rule বন্ধ করো)।

            অন্যান্য নিয়ম: error handler সব route-এর **পরে** register করো; একাধিক chain করা যায় (যেমন একটি logging-এর জন্য, যে `next(err)` call করে, আর একটি response দেয়); আর `res.headersSent` true হলে `next(err)` দিয়ে পরের জনকে দাও।
        """,
        tip_en=r"""Say the word "arity" — and explain why the three-parameter version silently fails. That shows you understand how Express dispatches, not just the syntax.""",
        tip_bn=r""""Arity" শব্দটা বলো — আর ব্যাখ্যা করো কেন তিন parameter-এর version চুপচাপ fail করে। এতে বোঝা যায় তুমি শুধু syntax নয়, Express কীভাবে dispatch করে সেটাও বোঝো।""",
        refs=[EX_ERRORS, EX_WRITING_MW],
    ),
    # ------------------------------------------------------------------ express-009
    Q(
        id="express-009", sub="REST APIs", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["rest", "http-methods", "status-codes", "idempotency", "api-design"],
        ver="Version-independent (HTTP semantics, RFC 9110); Express 5.x example", vs=False, status="stable",
        q_en=r"""You're designing a REST API for orders in Express. Which HTTP methods, URLs and status codes would you use for list, read, create, update and delete — and which of those operations are idempotent?""",
        q_bn=r"""Express-এ order-এর জন্য একটি REST API design করছ। List, read, create, update আর delete-এর জন্য কোন HTTP method, URL আর status code ব্যবহার করবে — আর এর মধ্যে কোন operation-গুলো idempotent?""",
        a_en=r"""
            Resources are nouns, actions are HTTP methods:

            - `GET /orders` → list, `200` (with pagination).
            - `GET /orders/:id` → read, `200`, or `404` if it doesn't exist.
            - `POST /orders` → create, `201 Created` with a `Location: /orders/123` header and the new resource.
            - `PUT /orders/:id` → full replace; `PATCH /orders/:id` → partial update; `200` with the updated resource (or `204`).
            - `DELETE /orders/:id` → `204 No Content`.
            - Errors: `400` invalid input, `401` not authenticated, `403` authenticated but not allowed, `404`, `409` conflict (duplicate or invalid state), `429` rate limited, `500` server error.

            **Idempotent** means repeating the same request leaves the server in the same state: `GET`, `HEAD`, `PUT` and `DELETE` are idempotent; `POST` is not (sending it twice creates two orders), and `PATCH` isn't guaranteed to be. That's why clients can safely retry a `PUT` after a timeout, but a retried `POST` needs an idempotency key.
        """,
        a_bn=r"""
            Resource হলো noun, action হলো HTTP method:

            - `GET /orders` → list, `200` (pagination সহ)।
            - `GET /orders/:id` → read, `200`, অথবা না থাকলে `404`।
            - `POST /orders` → create, `201 Created`, সাথে `Location: /orders/123` header আর নতুন resource।
            - `PUT /orders/:id` → পুরো replace; `PATCH /orders/:id` → আংশিক update; update হওয়া resource সহ `200` (বা `204`)।
            - `DELETE /orders/:id` → `204 No Content`।
            - Error: `400` ভুল input, `401` authenticated নয়, `403` authenticated কিন্তু অনুমতি নেই, `404`, `409` conflict (duplicate বা ভুল state), `429` rate limited, `500` server error।

            **Idempotent** মানে একই request বারবার পাঠালে server-এর state একই থাকে: `GET`, `HEAD`, `PUT` আর `DELETE` idempotent; `POST` নয় (দুবার পাঠালে দুটো order তৈরি হয়), আর `PATCH`-এর ক্ষেত্রে নিশ্চয়তা নেই। এজন্যই timeout-এর পর client নিরাপদে `PUT` retry করতে পারে, কিন্তু retry করা `POST`-এর জন্য idempotency key লাগে।
        """,
        ex_en=r"""
            - **Safe vs idempotent:** safe methods (`GET`, `HEAD`, `OPTIONS`) have no side effects at all; idempotent methods may change state, but repeating them doesn't change it further.
            - **`DELETE` twice** may return `204` then `404` — different responses, but the server state is the same, so it's still idempotent.
            - **State transitions** that aren't plain CRUD are often modelled as sub-resources or actions: `POST /orders/:id/cancel`. That's pragmatic and widely accepted.
            - **`400` vs `422`:** some teams use `422 Unprocessable Content` for well-formed but semantically invalid data; pick one convention and document it.
            - **Consistency beats perfection:** the same error format, pagination style and naming everywhere matter more than any single choice.
        """,
        ex_bn=r"""
            - **Safe বনাম idempotent:** safe method (`GET`, `HEAD`, `OPTIONS`)-এর কোনো side effect নেই; idempotent method state বদলাতে পারে, কিন্তু বারবার করলে আর বদলায় না।
            - **দুবার `DELETE`** করলে প্রথমে `204` তারপর `404` আসতে পারে — response আলাদা, কিন্তু server-এর state একই, তাই এটা তবুও idempotent।
            - **State transition**, যা সাধারণ CRUD নয়, প্রায়ই sub-resource বা action হিসেবে model করা হয়: `POST /orders/:id/cancel`। এটা বাস্তবসম্মত এবং ব্যাপকভাবে গৃহীত।
            - **`400` বনাম `422`:** কিছু team ঠিকঠাক format-এর কিন্তু অর্থগতভাবে ভুল data-র জন্য `422 Unprocessable Content` ব্যবহার করে; একটি নিয়ম বেছে নিয়ে document করো।
            - **নিখুঁত হওয়ার চেয়ে ধারাবাহিকতা জরুরি:** সব জায়গায় একই error format, pagination style আর naming — কোনো একক সিদ্ধান্তের চেয়ে এটা বেশি গুরুত্বপূর্ণ।
        """,
        tip_en=r"""Walk through the five operations quickly, then spend your time on idempotency and why it matters for retries. That's where an easy question turns into a strong answer.""",
        tip_bn=r"""পাঁচটি operation দ্রুত বলে যাও, তারপর বেশি সময় দাও idempotency আর retry-এর ক্ষেত্রে এর গুরুত্বে। এখানেই একটি সহজ প্রশ্ন শক্তিশালী উত্তরে পরিণত হয়।""",
        mist_en=r"""Verbs in URLs (`/getOrders`, `/createOrder`), returning `200` with `{ "error": ... }` for failures, or saying `POST` is idempotent.""",
        mist_bn=r"""URL-এ verb রাখা (`/getOrders`, `/createOrder`), failure-এ `{ "error": ... }` সহ `200` return করা, অথবা `POST`-কে idempotent বলা।""",
        code=r"""
            import express from 'express';

            export const ordersRouter = express.Router();

            ordersRouter.get('/', listOrders);          // 200 + pagination
            ordersRouter.get('/:id', getOrder);         // 200 | 404

            ordersRouter.post('/', async (req, res) => {
              const order = await orders.create(req.body);
              res.status(201).location(`/v1/orders/${order.id}`).json(order);
            });

            ordersRouter.patch('/:id', updateOrder);    // 200 with the updated order

            ordersRouter.delete('/:id', async (req, res) => {
              await orders.remove(req.params.id);
              res.sendStatus(204);
            });

            ordersRouter.post('/:id/cancel', cancelOrder); // state transition as an action
        """,
        lang="javascript",
        follow=[
            ("How would you make `POST /orders` safe to retry?", "`POST /orders`-কে retry করার জন্য কীভাবে নিরাপদ বানাবে?"),
            ("When would you return `409` instead of `400`?", "কখন `400`-এর বদলে `409` return করবে?"),
        ],
        related=["express-032", "express-022"],
        refs=[RFC_9110, MDN_STATUS, MDN_IDEMPOTENT],
    ),
    # ------------------------------------------------------------------ express-010
    Q(
        id="express-010", sub="Middleware", diff="easy", type="debugging",
        prio="high", market="bangladesh", mins=3,
        tags=["middleware", "next", "hanging-request", "api-key", "debugging"],
        ver="Express 4.x and 5.x", vs=False, status="stable",
        q_en=r"""Requests with an **invalid** API key correctly get `401`, but requests with a **valid** key never get a response — the browser spins until it times out (behind NGINX they end as `504`). What's wrong with this middleware?""",
        q_bn=r"""**ভুল** API key দিলে request ঠিকঠাক `401` পায়, কিন্তু **সঠিক** key দিলে কখনো response আসে না — browser timeout না হওয়া পর্যন্ত ঘুরতে থাকে (NGINX-এর পেছনে `504` দিয়ে শেষ হয়)। এই middleware-এ সমস্যা কী?""",
        a_en=r"""
            The middleware never calls `next()`. On the valid-key path it doesn't send a response either, so Express just waits — nothing else in the stack runs and the request hangs until a timeout.

            There's a second, hidden bug: after sending the `401` there's no `return`. If someone "fixes" the hang by adding `next()` at the end, invalid requests would send the 401 *and* continue to the route handler, causing `ERR_HTTP_HEADERS_SENT` errors — and executing protected code for unauthenticated users.

            Fix: `return` after responding, and call `next()` on the success path.
        """,
        a_bn=r"""
            Middleware কখনো `next()` call করে না। সঠিক key-র পথে এটা response-ও পাঠায় না, তাই Express শুধু অপেক্ষা করে — stack-এর আর কিছুই চলে না এবং timeout না হওয়া পর্যন্ত request ঝুলে থাকে।

            আরেকটি লুকানো bug আছে: `401` পাঠানোর পর কোনো `return` নেই। কেউ যদি শেষে `next()` যোগ করে ঝুলে থাকা "ঠিক" করে, তাহলে ভুল request `401` পাঠাবে *এবং* route handler-এও চলে যাবে — ফলে `ERR_HTTP_HEADERS_SENT` error হবে, আর unauthenticated user-এর জন্য protected code-ও চলবে।

            Fix: response দেওয়ার পর `return`, আর সফল পথে `next()` call করা।
        """,
        ex_en=r"""
            - **Rule of thumb:** every code path in a middleware must either send a response or call `next()` — exactly once.
            - **Debugging hangs:** log at the start and end of each middleware, or use `DEBUG=express:*,router` to see which layer was entered last. Request-level timeouts and access logs that record *unfinished* requests make this visible in production.
            - **Comparing secrets:** for API keys, compare with `crypto.timingSafeEqual` on equal-length buffers to avoid timing attacks, and keep keys hashed in storage when possible.
            - **Express 5 note:** an `async` middleware that resolves without calling `next()` still hangs — only rejections are auto-forwarded.
        """,
        ex_bn=r"""
            - **মূল নিয়ম:** middleware-এর প্রতিটি code path-কে হয় response পাঠাতে হবে, নয়তো `next()` call করতে হবে — ঠিক একবার।
            - **Hang debug করা:** প্রতিটি middleware-এর শুরু ও শেষে log করো, অথবা `DEBUG=express:*,router` দিয়ে দেখো সবশেষে কোন layer-এ ঢুকেছে। Request-level timeout আর *অসমাপ্ত* request রেকর্ড করা access log production-এ এটা দৃশ্যমান করে।
            - **Secret তুলনা:** API key-র জন্য timing attack এড়াতে সমান দৈর্ঘ্যের buffer-এ `crypto.timingSafeEqual` দিয়ে তুলনা করো, আর সম্ভব হলে storage-এ key hash করে রাখো।
            - **Express 5 নোট:** যে `async` middleware `next()` call না করেই resolve হয়, সেটাও ঝুলে থাকে — শুধু rejection স্বয়ংক্রিয়ভাবে forward হয়।
        """,
        tip_en=r"""Point out both bugs — the missing `next()` and the missing `return`. Spotting the second one before it bites shows the reviewer mindset interviewers look for.""",
        tip_bn=r"""দুটো bug-ই দেখাও — `next()` না থাকা আর `return` না থাকা। দ্বিতীয়টা সমস্যা তৈরির আগেই ধরতে পারা interviewer-রা যে reviewer মানসিকতা খোঁজে সেটাই দেখায়।""",
        mist_en=r"""Adding `next()` at the bottom without a `return` in the error branch, or "fixing" the hang with a global timeout instead of the missing `next()`.""",
        mist_bn=r"""Error branch-এ `return` না দিয়ে শুধু নিচে `next()` যোগ করা, অথবা `next()` ঠিক না করে global timeout দিয়ে ঝুলে থাকা "ঠিক" করা।""",
        code=r"""
            function requireApiKey(req, res, next) {
              const key = req.get('x-api-key');
              if (key !== process.env.API_KEY) {
                res.status(401).json({ error: 'Invalid API key' });
              }
              // valid key: continue to the route
            }

            app.use('/api', requireApiKey);

            app.get('/api/products', async (req, res) => {
              res.json(await products.list());
            });
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                function requireApiKey(req, res, next) {
                  const key = req.get('x-api-key');
                  if (key !== process.env.API_KEY) {
                    return res.status(401).json({ error: 'Invalid API key' }); // stop here
                  }
                  next(); // valid key: hand over to the next middleware/route
                }
            """, label_en="Fixed version", label_bn="সংশোধিত version"),
        ],
        follow=[
            ("How would you detect hanging requests in production before users complain?", "User অভিযোগ করার আগেই production-এ ঝুলে থাকা request কীভাবে ধরবে?"),
            ("Why should API keys be compared in constant time?", "API key কেন constant time-এ তুলনা করা উচিত?"),
        ],
        related=["express-001", "express-011"],
        refs=[EX_WRITING_MW],
    ),
    # ------------------------------------------------------------------ express-011
    Q(
        id="express-011", sub="Request & Response Lifecycle", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["headers-sent", "err-http-headers-sent", "return", "debugging", "side-effects"],
        ver="Express 5.x", vs=False, status="stable",
        q_en=r"""Logs are full of `Error [ERR_HTTP_HEADERS_SENT]: Cannot set headers after they are sent to the client`, and finance reports orders with `quantity: 0` in the database even though the API "rejects" them with `400`. Find the bug in this handler and fix it.""",
        q_bn=r"""Log ভরে আছে `Error [ERR_HTTP_HEADERS_SENT]: Cannot set headers after they are sent to the client` দিয়ে, আর finance জানাচ্ছে database-এ `quantity: 0` সহ order আছে, যদিও API সেগুলো `400` দিয়ে "reject" করে। এই handler-এর bug খুঁজে ঠিক করো।""",
        a_en=r"""
            `res.status(400).json(...)` sends the response but **does not stop the function**. Without a `return`, execution continues: the handler looks up the product, **creates the order anyway**, and then tries to send a second response with `res.status(201).json(...)`. Node refuses because the headers (and body) were already sent, so it throws `ERR_HTTP_HEADERS_SENT`.

            The same happens with the `404` branch: if the product doesn't exist, the code continues to `product.price` and crashes with a `TypeError`.

            The log error is just the symptom — the real damage is the side effect (an invalid order) that runs after the client was told the request failed. Fix: `return` after every response (or, in Express 5, `throw` an error and let the error middleware respond).
        """,
        a_bn=r"""
            `res.status(400).json(...)` response পাঠায় কিন্তু **function থামায় না**। `return` না থাকায় execution চলতে থাকে: handler product খোঁজে, **তবুও order তৈরি করে**, তারপর `res.status(201).json(...)` দিয়ে দ্বিতীয় response পাঠাতে চায়। Header (আর body) আগেই পাঠানো হয়ে গেছে বলে Node অস্বীকার করে এবং `ERR_HTTP_HEADERS_SENT` throw করে।

            `404` branch-এও একই ঘটনা: product না থাকলে code `product.price`-এ পৌঁছে `TypeError` দিয়ে crash করে।

            Log-এর error শুধু উপসর্গ — আসল ক্ষতি হলো side effect (একটি invalid order), যা client-কে request fail হয়েছে জানানোর পরেও চলে। Fix: প্রতিটি response-এর পর `return` (অথবা Express 5-এ error `throw` করে error middleware-কে response দিতে দেওয়া)।
        """,
        ex_en=r"""
            Other common causes of `ERR_HTTP_HEADERS_SENT`:
            - calling `next()` (or `next(err)`) after already responding;
            - responding inside a loop or in both a callback and the main flow;
            - a timeout middleware sends `503`, then the slow handler finishes and responds again;
            - an error handler that responds without checking `res.headersSent`.

            Why "throw instead of respond" is nice in Express 5: a thrown `AppError` immediately leaves the handler, so there's no way to forget the `return`, and all error responses get the same format from one place.

            Also validate input **before** any database work — a schema validation middleware catches `quantity: 0` before the handler even runs.
        """,
        ex_bn=r"""
            `ERR_HTTP_HEADERS_SENT`-এর অন্যান্য সাধারণ কারণ:
            - response দেওয়ার পরেও `next()` (বা `next(err)`) call করা;
            - loop-এর ভেতরে, বা callback আর মূল flow দুই জায়গাতেই response দেওয়া;
            - একটি timeout middleware `503` পাঠায়, তারপর ধীর handler শেষ হয়ে আবার response দেয়;
            - `res.headersSent` check না করে response দেওয়া error handler।

            Express 5-এ "response না দিয়ে throw করা" কেন ভালো: throw করা `AppError` সাথে সাথে handler থেকে বের হয়ে যায়, তাই `return` ভুলে যাওয়ার সুযোগ নেই, আর সব error response এক জায়গা থেকে একই format পায়।

            আর database-এর কাজের **আগেই** input validate করো — একটি schema validation middleware handler চলার আগেই `quantity: 0` ধরে ফেলে।
        """,
        tip_en=r"""Lead with the business impact ("we create orders after telling the client it failed"), then the mechanism (`res.json` doesn't return from the function). Interviewers value seeing the side-effect risk, not just the log message.""",
        tip_bn=r"""ব্যবসায়িক প্রভাব দিয়ে শুরু করো ("client-কে fail জানানোর পরেও আমরা order তৈরি করছি"), তারপর mechanism (`res.json` function থেকে return করে না)। Interviewer শুধু log message নয়, side-effect-এর ঝুঁকি দেখতে পারাটাকে মূল্য দেয়।""",
        mist_en=r"""Wrapping the second `res.json` in `if (!res.headersSent)` — it hides the error but the invalid order is still created.""",
        mist_bn=r"""দ্বিতীয় `res.json`-কে `if (!res.headersSent)` দিয়ে মুড়ে দেওয়া — এতে error লুকায়, কিন্তু invalid order তবুও তৈরি হয়।""",
        code=r"""
            app.post('/api/orders', async (req, res) => {
              const { productId, quantity } = req.body;

              if (!productId || !(quantity >= 1)) {
                res.status(400).json({ error: 'productId and quantity >= 1 are required' });
              }

              const product = await products.findById(productId);
              if (!product) {
                res.status(404).json({ error: 'Product not found' });
              }

              const order = await orders.create({ productId, quantity, price: product.price });
              res.status(201).json(order);
            });
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                app.post('/api/orders', async (req, res) => {
                  const { productId, quantity } = req.body;

                  if (!productId || !(quantity >= 1)) {
                    return res.status(400).json({ error: 'productId and quantity >= 1 are required' });
                  }

                  const product = await products.findById(productId);
                  if (!product) {
                    throw AppError.notFound('Product'); // Express 5: goes to the error middleware
                  }

                  const order = await orders.create({ productId, quantity, price: product.price });
                  res.status(201).json(order);
                });
            """, label_en="Fixed version (return / throw after responding)", label_bn="সংশোধিত version (response-এর পর return / throw)"),
        ],
        follow=[
            ("How would a timeout middleware cause this error, and how do you prevent it?", "একটি timeout middleware কীভাবে এই error ঘটাতে পারে, আর কীভাবে আটকাবে?"),
            ("What should an error handler do if `res.headersSent` is already true?", "`res.headersSent` আগে থেকেই true হলে error handler-এর কী করা উচিত?"),
        ],
        related=["express-010", "express-006", "express-012"],
        refs=[EX_API5, NODE_ERRORS],
    ),
    # ------------------------------------------------------------------ express-012
    Q(
        id="express-012", sub="Validation", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["validation", "zod", "middleware", "express-5", "coding"],
        ver="Express 5.x; zod 4.x", vs=True, status="stable",
        q_en=r"""
            Write a reusable Express 5 middleware `validate({ params, query, body })` that validates the request with zod 4 schemas.

            - On failure: respond `400` with errors grouped by request part.
            - On success: make the **parsed** values (coerced types, defaults applied, unknown keys removed or rejected) available to the handler.

            Example: `GET /products?page=2` → the handler gets `{ page: 2, limit: 20, sort: '-createdAt' }` with numbers and defaults; `GET /products?limit=500` → `400`.
        """,
        q_bn=r"""
            একটি reusable Express 5 middleware `validate({ params, query, body })` লেখো, যা zod 4 schema দিয়ে request validate করবে।

            - Fail হলে: request-এর অংশ অনুযায়ী ভাগ করা error সহ `400` response।
            - সফল হলে: **parse করা** value (coerce করা type, default বসানো, অজানা key বাদ বা reject করা) handler-এর কাছে পৌঁছে দেবে।

            উদাহরণ: `GET /products?page=2` → handler পাবে `{ page: 2, limit: 20, sort: '-createdAt' }`, number আর default সহ; `GET /products?limit=500` → `400`।
        """,
        a_en=r"""
            The middleware factory takes a schema per request part, runs `safeParse` on each, collects errors with `z.flattenError()`, and either responds `400` or stores the parsed data and calls `next()`.

            The Express 5 twist: `req.query` is a **read-only getter**, so I can't write the coerced values back into it. I store them in `res.locals.validated` (a custom `req.validated` property also works). Handlers then read typed values from one place and never touch raw input.

            For bodies I use `z.strictObject()` so unexpected keys like `isAdmin` are rejected — protection against mass assignment.
        """,
        a_bn=r"""
            Middleware factory request-এর প্রতিটি অংশের জন্য একটি schema নেয়, প্রত্যেকটিতে `safeParse` চালায়, `z.flattenError()` দিয়ে error জমায়, তারপর হয় `400` response দেয়, নয়তো parse করা data রেখে `next()` call করে।

            Express 5-এর twist: `req.query` একটি **read-only getter**, তাই coerce করা value আবার এতে লিখে দেওয়া যায় না। আমি সেগুলো `res.locals.validated`-এ রাখি (নিজস্ব `req.validated` property-ও চলে)। Handler এরপর এক জায়গা থেকে typed value পড়ে, কখনো raw input ছোঁয় না।

            Body-র জন্য `z.strictObject()` ব্যবহার করি, যাতে `isAdmin`-এর মতো অপ্রত্যাশিত key reject হয় — mass assignment-এর বিরুদ্ধে সুরক্ষা।
        """,
        ex_en=r"""
            - **Why `safeParse`:** it returns `{ success, data, error }` instead of throwing, so the middleware can collect errors from all parts in one response. (Alternatively, throw the `ZodError` and let the central error handler map it to 400.)
            - **Coercion:** query/params are strings; `z.coerce.number()` converts them. Note `?page=` (empty) coerces to `0` and then fails `.min(1)` — a correct 400.
            - **Zod 4 specifics:** `z.flattenError(err)` gives `{ formErrors, fieldErrors }` (the old `err.flatten()` is deprecated); unknown keys in a strict object appear in `formErrors`; `z.email()`, `z.url()` are top-level; `.default()` short-circuits on `undefined`.
            - **Edge cases:** a missing body (`undefined` in Express 5) is validated as `{}`, so required fields report clearly; arrays from repeated query keys (`?tag=a&tag=b`) need `z.array(...)` or a preprocess step.
            - **Validation ≠ authorization:** a valid `orderId` still needs an ownership check in the handler or service.
            - Verified with supertest: coerced numbers and defaults, `400` for `limit=500` and unknown sort, `201` with trimmed name, `400` for unknown key `isAdmin`.
        """,
        ex_bn=r"""
            - **কেন `safeParse`:** এটা throw না করে `{ success, data, error }` return করে, তাই middleware এক response-এ সব অংশের error জমাতে পারে। (বিকল্পভাবে `ZodError` throw করে central error handler-কে 400-এ map করতে দেওয়া যায়।)
            - **Coercion:** query/params string; `z.coerce.number()` এগুলো convert করে। খেয়াল করো `?page=` (খালি) `0`-তে coerce হয়, তারপর `.min(1)`-এ fail করে — সঠিক 400।
            - **Zod 4-এর বিশেষত্ব:** `z.flattenError(err)` দেয় `{ formErrors, fieldErrors }` (পুরনো `err.flatten()` deprecated); strict object-এ অজানা key `formErrors`-এ আসে; `z.email()`, `z.url()` top-level; `undefined` হলে `.default()` সরাসরি default দেয়।
            - **Edge case:** body না থাকলে (Express 5-এ `undefined`) সেটা `{}` হিসেবে validate হয়, তাই required field-এর error স্পষ্ট আসে; repeated query key (`?tag=a&tag=b`) থেকে আসা array-এর জন্য `z.array(...)` বা একটি preprocess ধাপ লাগে।
            - **Validation মানে authorization নয়:** valid `orderId` হলেও handler বা service-এ ownership check লাগবে।
            - Supertest দিয়ে যাচাই করা: coerce করা number ও default, `limit=500` আর অজানা sort-এ `400`, trim করা name সহ `201`, অজানা key `isAdmin`-এ `400`।
        """,
        tip_en=r"""Mention the Express 5 `req.query` getter right away — it's the detail that shows you've actually built this on v5. Then mention strict objects for mass-assignment protection.""",
        tip_bn=r"""শুরুতেই Express 5-এর `req.query` getter-এর কথা বলো — এই detail-টাই দেখায় তুমি সত্যিই v5-এ এটা বানিয়েছ। তারপর mass-assignment সুরক্ষার জন্য strict object-এর কথা বলো।""",
        mist_en=r"""Assigning `req.query = result.data` (throws in Express 5 ES modules), validating but then using the raw `req.body` in the handler, or passing the whole body straight into an ORM `create()` call.""",
        mist_bn=r"""`req.query = result.data` assign করা (Express 5-এর ES module-এ throw করে), validate করার পরেও handler-এ raw `req.body` ব্যবহার করা, অথবা পুরো body সরাসরি ORM-এর `create()`-এ পাঠিয়ে দেওয়া।""",
        code=r"""
            import { z } from 'zod';

            export function validate(schemas) {
              return (req, res, next) => {
                const parsed = {};
                const errors = {};

                for (const part of ['params', 'query', 'body']) {
                  const schema = schemas[part];
                  if (!schema) continue;
                  const result = schema.safeParse(req[part] ?? {});
                  if (result.success) parsed[part] = result.data;
                  else errors[part] = z.flattenError(result.error); // { formErrors, fieldErrors }
                }

                if (Object.keys(errors).length > 0) {
                  return res.status(400).json({ error: 'VALIDATION_FAILED', details: errors });
                }
                res.locals.validated = parsed; // req.query is a read-only getter in Express 5
                next();
              };
            }

            // --- usage ---
            const listProducts = {
              query: z.object({
                page: z.coerce.number().int().min(1).default(1),
                limit: z.coerce.number().int().min(1).max(100).default(20),
                sort: z.enum(['price', '-price', 'createdAt', '-createdAt']).default('-createdAt'),
              }),
            };

            const createProduct = {
              body: z.strictObject({            // unknown keys (e.g. isAdmin) -> 400
                name: z.string().trim().min(2).max(120),
                price: z.number().positive(),
                tags: z.array(z.string().max(30)).max(10).default([]),
              }),
            };

            app.get('/products', validate(listProducts), async (req, res) => {
              const { page, limit, sort } = res.locals.validated.query; // numbers + defaults
              res.json(await products.list({ page, limit, sort }));
            });

            app.post('/products', validate(createProduct), async (req, res) => {
              res.status(201).json(await products.create(res.locals.validated.body));
            });
        """,
        lang="javascript",
        time="O(size of the validated input)", space="O(size of the validated input)",
        follow=[
            ("How would you share these schemas with a TypeScript frontend?", "এই schema-গুলো TypeScript frontend-এর সাথে কীভাবে share করবে?"),
            ("Would you strip unknown keys or reject them? Why?", "অজানা key বাদ দেবে নাকি reject করবে? কেন?"),
        ],
        related=["express-003", "express-006", "express-028"],
        refs=[ZOD_API, ZOD_ERRORS, OWASP_INPUT],
    ),
    # ------------------------------------------------------------------ express-013
    Q(
        id="express-013", sub="File Uploads (multer)", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["file-upload", "multer", "security", "mime-sniffing", "dos", "express-5"],
        ver="Express 5.x; multer 2.x", vs=True, status="stable",
        q_en=r"""You need an endpoint that lets users upload a profile picture (JPEG, PNG or WebP, max 2 MB) with Express 5 and multer. What can go wrong — security- and performance-wise — and how do you implement it safely?""",
        q_bn=r"""Express 5 আর multer দিয়ে এমন একটি endpoint দরকার, যেখানে user profile picture upload করবে (JPEG, PNG বা WebP, সর্বোচ্চ 2 MB)। Security ও performance-এর দিক থেকে কী কী ভুল হতে পারে, আর কীভাবে নিরাপদে implement করবে?""",
        a_en=r"""
            **Risks:**
            - **DoS / resource exhaustion:** huge files, many files or fields, slow uploads; `memoryStorage` without limits can exhaust RAM, disk storage can fill the disk.
            - **Trusting client metadata:** `file.mimetype` comes from the client's `Content-Type`, and `originalname` is attacker-controlled (path traversal like `../../app.js`, overwriting files, weird characters).
            - **Malicious content:** an "image" that's really HTML/SVG with scripts → stored XSS if served from your domain; polyglot files; decompression bombs.
            - **Exposure:** multer mounted globally lets attackers upload to any route; an outdated multer has had several DoS fixes in 2025–2026, so keep it patched.

            **Safe implementation:**
            1. Authenticate (and rate-limit) **before** the upload middleware; attach multer only to this route with `upload.single('avatar')`.
            2. Set `limits`: `fileSize: 2 MB`, `files: 1`, small `fields`/`parts`. With a 2 MB cap, memory storage is acceptable; also set `client_max_body_size` in NGINX.
            3. `fileFilter` does a cheap first check on the declared MIME type, then **verify the magic bytes** (e.g. the `file-type` package) after upload.
            4. **Re-encode** the image (e.g. with `sharp`): strips metadata (GPS EXIF) and embedded payloads, normalises size and format.
            5. Generate the storage key server-side (`avatars/<userId>/<uuid>.webp`), never from `originalname`; store in a private bucket or outside the web root.
            6. Serve via a CDN/separate domain with the correct `Content-Type` and `X-Content-Type-Options: nosniff`.
            7. Map `MulterError` codes: `LIMIT_FILE_SIZE` → `413`, others → `400`.
        """,
        a_bn=r"""
            **ঝুঁকি:**
            - **DoS / resource শেষ হয়ে যাওয়া:** বিশাল file, অনেক file বা field, ধীর upload; limit ছাড়া `memoryStorage` RAM শেষ করে দিতে পারে, disk storage disk ভরে ফেলতে পারে।
            - **Client-এর metadata বিশ্বাস করা:** `file.mimetype` আসে client-এর `Content-Type` থেকে, আর `originalname` attacker-নিয়ন্ত্রিত (`../../app.js`-এর মতো path traversal, file overwrite, অদ্ভুত character)।
            - **ক্ষতিকর content:** যে "image" আসলে script সহ HTML/SVG → নিজের domain থেকে serve করলে stored XSS; polyglot file; decompression bomb।
            - **Exposure:** globally mount করা multer attacker-কে যেকোনো route-এ upload করতে দেয়; পুরনো multer-এ 2025–2026-এ কয়েকটি DoS fix এসেছে, তাই patched রাখো।

            **নিরাপদ implementation:**
            1. Upload middleware-এর **আগে** authenticate (আর rate-limit) করো; multer শুধু এই route-এ `upload.single('avatar')` দিয়ে লাগাও।
            2. `limits` set করো: `fileSize: 2 MB`, `files: 1`, ছোট `fields`/`parts`। 2 MB cap থাকলে memory storage চলে; NGINX-এ `client_max_body_size`-ও দাও।
            3. `fileFilter` declare করা MIME type-এর উপর সস্তা প্রথম check করে, তারপর upload-এর পর **magic bytes যাচাই** করো (যেমন `file-type` package)।
            4. Image **re-encode** করো (যেমন `sharp` দিয়ে): metadata (GPS EXIF) আর লুকানো payload মুছে যায়, size ও format normalise হয়।
            5. Storage key server-এ তৈরি করো (`avatars/<userId>/<uuid>.webp`), কখনো `originalname` থেকে নয়; private bucket-এ বা web root-এর বাইরে রাখো।
            6. সঠিক `Content-Type` আর `X-Content-Type-Options: nosniff` সহ CDN/আলাদা domain থেকে serve করো।
            7. `MulterError` code map করো: `LIMIT_FILE_SIZE` → `413`, বাকিগুলো → `400`।
        """,
        ex_en=r"""
            - **Why both checks:** the `fileFilter` check runs before bytes are stored and rejects obvious junk cheaply; the magic-byte check runs on the actual content. Neither alone is enough; re-encoding is the strongest guarantee that what you store is really an image.
            - **CPU cost:** image decoding/encoding is CPU-heavy; `sharp` does it in native threads, but you should still rate-limit uploads and cap pixel dimensions to avoid decompression bombs.
            - **Large files** (videos, documents) are a different design: stream to object storage or use presigned URLs instead of buffering in Node.
            - **Errors:** when `fileFilter` rejects with `cb(null, false)`, `req.file` is `undefined` — handle that explicitly. Multer passes its own errors (`MulterError`) to `next(err)`.
            - **Cleanup:** with disk storage, delete temp files on validation failure; with memory storage, buffers are freed after the request.
        """,
        ex_bn=r"""
            - **দুটো check কেন:** `fileFilter` check byte জমা হওয়ার আগেই চলে এবং সহজে স্পষ্ট আবর্জনা reject করে; magic-byte check আসল content-এর উপর চলে। একটা একা যথেষ্ট নয়; re-encoding-ই সবচেয়ে শক্ত নিশ্চয়তা যে যা রাখছ তা সত্যিই একটি image।
            - **CPU খরচ:** image decode/encode CPU-heavy; `sharp` native thread-এ করে, তবুও upload rate-limit করো এবং decompression bomb এড়াতে pixel dimension সীমিত করো।
            - **বড় file** (video, document) আলাদা design: Node-এ buffer না করে object storage-এ stream করো বা presigned URL ব্যবহার করো।
            - **Error:** `fileFilter` `cb(null, false)` দিয়ে reject করলে `req.file` `undefined` থাকে — এটা স্পষ্টভাবে handle করো। Multer নিজের error (`MulterError`) `next(err)`-এ পাঠায়।
            - **Cleanup:** disk storage-এ validation fail হলে temp file মুছে ফেলো; memory storage-এ request শেষে buffer মুক্ত হয়ে যায়।
        """,
        tip_en=r"""Organise the answer as "limits, verify, transform, store, serve". Saying explicitly that `file.mimetype` is client-controlled is the detail most candidates miss.""",
        tip_bn=r"""উত্তর সাজাও "limit, verify, transform, store, serve" ক্রমে। `file.mimetype` যে client-নিয়ন্ত্রিত — এটা স্পষ্ট করে বলাই সেই detail যা বেশিরভাগ candidate বাদ দেয়।""",
        mist_en=r"""Using `app.use(upload.any())` globally, saving files under `public/` with their original names, or validating only the file extension.""",
        mist_bn=r"""Globally `app.use(upload.any())` ব্যবহার করা, file-গুলো original নামে `public/`-এর নিচে save করা, অথবা শুধু file extension validate করা।""",
        code=r"""
            import express from 'express';
            import multer from 'multer';
            import sharp from 'sharp';
            import { fileTypeFromBuffer } from 'file-type';
            import { randomUUID } from 'node:crypto';

            const ALLOWED = new Set(['image/jpeg', 'image/png', 'image/webp']);

            const upload = multer({
              storage: multer.memoryStorage(), // acceptable only because size is capped
              limits: { fileSize: 2 * 1024 * 1024, files: 1, fields: 5, parts: 6 },
              fileFilter: (req, file, cb) => {
                cb(null, ALLOWED.has(file.mimetype)); // cheap first check; client-controlled!
              },
            });

            app.post('/me/avatar', authenticate, avatarRateLimit, upload.single('avatar'), async (req, res) => {
              if (!req.file) throw new AppError(400, 'NO_FILE', 'Upload a JPEG, PNG or WebP image');

              const detected = await fileTypeFromBuffer(req.file.buffer); // magic bytes
              if (!detected || !ALLOWED.has(detected.mime)) {
                throw new AppError(415, 'UNSUPPORTED_MEDIA_TYPE', 'Only JPEG, PNG or WebP images are allowed');
              }

              // Re-encode: strips metadata/embedded payloads, normalises size and format
              const image = await sharp(req.file.buffer, { limitInputPixels: 40_000_000 })
                .resize(512, 512, { fit: 'cover' })
                .webp()
                .toBuffer();

              const key = `avatars/${req.user.id}/${randomUUID()}.webp`; // never use originalname
              await storage.put(key, image, { contentType: 'image/webp' });
              res.status(201).json({ url: `${process.env.CDN_URL}/${key}` });
            });

            // In the central error handler:
            // if (err instanceof multer.MulterError) {
            //   return res.status(err.code === 'LIMIT_FILE_SIZE' ? 413 : 400).json({ error: err.code });
            // }
        """,
        lang="javascript",
        follow=[
            ("Why is serving user uploads from your main domain risky?", "নিজের main domain থেকে user upload serve করা কেন ঝুঁকিপূর্ণ?"),
            ("How would you change this design for 500 MB video uploads?", "500 MB video upload-এর জন্য এই design কীভাবে বদলাবে?"),
        ],
        related=["express-006", "express-018"],
        refs=[EX_MULTER, OWASP_UPLOAD],
    ),
    # ------------------------------------------------------------------ express-014
    Q(
        id="express-014", sub="Deployment", diff="hard", type="mcq",
        prio="high", market="both", mins=3,
        tags=["trust-proxy", "req-ip", "x-forwarded-for", "nginx", "rate-limiting"],
        ver="Express 4.x and 5.x", vs=False, status="stable",
        q_en=r"""Your Express app runs behind **exactly one** reverse proxy (NGINX), which appends the client's address to `X-Forwarded-For`. A client sends a forged header `X-Forwarded-For: 1.1.1.1`, so the app receives `X-Forwarded-For: 1.1.1.1, 203.0.113.7`. With `app.set('trust proxy', 1)`, what is `req.ip`?""",
        q_bn=r"""তোমার Express app **ঠিক একটি** reverse proxy (NGINX)-এর পেছনে চলে, যা `X-Forwarded-For`-এ client-এর address যোগ করে। একজন client নকল header `X-Forwarded-For: 1.1.1.1` পাঠায়, ফলে app পায় `X-Forwarded-For: 1.1.1.1, 203.0.113.7`। `app.set('trust proxy', 1)` থাকলে `req.ip` কী হবে?""",
        options=[
            ("`1.1.1.1` — the leftmost address is the original client", "`1.1.1.1` — বাম দিকের প্রথম address-ই আসল client"),
            ("`203.0.113.7` — the address NGINX actually saw", "`203.0.113.7` — যে address NGINX আসলে দেখেছে"),
            ("NGINX's own address, for example `127.0.0.1`", "NGINX-এর নিজের address, যেমন `127.0.0.1`"),
            ("`undefined`, because the header contains two addresses", "`undefined`, কারণ header-এ দুটি address আছে"),
        ],
        correct=1,
        a_en=r"""
            `203.0.113.7`. `trust proxy: 1` tells Express to trust exactly one hop: it takes the address that the single trusted proxy appended (the rightmost entry). Anything to the left of it was supplied by the client and can be forged.
        """,
        a_bn=r"""
            `203.0.113.7`। `trust proxy: 1` Express-কে ঠিক একটি hop বিশ্বাস করতে বলে: একমাত্র trusted proxy যে address যোগ করেছে (ডান দিকের শেষ entry) সেটাই নেয়। তার বাঁ দিকের যেকোনো কিছু client দিয়েছে এবং নকল হতে পারে।
        """,
        ex_en=r"""
            Verified with Express 5.3 + supertest:

            - **`trust proxy: 1`** → `203.0.113.7` (correct). `req.protocol` and `req.secure` also honour `X-Forwarded-Proto` from that proxy.
            - **`trust proxy: true`** → `1.1.1.1` (option A). It trusts *every* hop, so `req.ip` becomes the leftmost, client-controlled value — attackers can rotate fake IPs to bypass IP-based rate limits and poison audit logs. That's why A is the dangerous, tempting answer.
            - **Default (`false`)** → the proxy's own address (option C). Every user looks like the same IP, so a rate limiter blocks everyone at once; `req.protocol` is `http` even for HTTPS traffic, so `secure` session cookies aren't set.

            Set it to match your real topology: a hop count (`1`, or `2` for CDN + load balancer) or trusted subnets (`'loopback, 10.0.0.0/8'`). express-rate-limit 8 even logs a validation error (`ERR_ERL_UNEXPECTED_X_FORWARDED_FOR`) if it sees `X-Forwarded-For` while `trust proxy` is off.
        """,
        ex_bn=r"""
            Express 5.3 + supertest দিয়ে যাচাই করা:

            - **`trust proxy: 1`** → `203.0.113.7` (সঠিক)। ওই proxy-র `X-Forwarded-Proto` অনুযায়ী `req.protocol` আর `req.secure`-ও ঠিক হয়।
            - **`trust proxy: true`** → `1.1.1.1` (option A)। এটা *প্রতিটি* hop বিশ্বাস করে, ফলে `req.ip` হয় বাম দিকের, client-নিয়ন্ত্রিত value — attacker নকল IP বদলে বদলে IP-ভিত্তিক rate limit এড়াতে আর audit log দূষিত করতে পারে। এজন্যই A হলো বিপজ্জনক, প্রলোভনের উত্তর।
            - **Default (`false`)** → proxy-র নিজের address (option C)। সব user-কে একই IP মনে হয়, তাই rate limiter একসাথে সবাইকে block করে; HTTPS traffic-এও `req.protocol` হয় `http`, ফলে `secure` session cookie set হয় না।

            তোমার আসল topology অনুযায়ী set করো: hop সংখ্যা (`1`, বা CDN + load balancer হলে `2`) অথবা trusted subnet (`'loopback, 10.0.0.0/8'`)। express-rate-limit 8 এমনকি `trust proxy` বন্ধ থাকা অবস্থায় `X-Forwarded-For` দেখলে একটি validation error (`ERR_ERL_UNEXPECTED_X_FORWARDED_FOR`) log করে।
        """,
        tip_en=r"""Explain all three settings and their consequences (spoofable vs everyone-is-one-IP). Linking `trust proxy` to rate limiting and secure cookies shows production experience.""",
        tip_bn=r"""তিনটি setting আর তাদের পরিণাম ব্যাখ্যা করো (নকল করা যায় বনাম সবাই এক IP)। `trust proxy`-কে rate limiting আর secure cookie-র সাথে যুক্ত করা production অভিজ্ঞতা দেখায়।""",
        refs=[EX_PROXIES],
    ),
]

if __name__ == "__main__":
    save("express", "b2", QUESTIONS)
