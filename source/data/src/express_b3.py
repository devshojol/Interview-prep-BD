import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_CORS = ("MDN — Cross-Origin Resource Sharing (CORS)", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS")
EX_CORS = ("Express — cors middleware", "https://expressjs.com/en/resources/middleware/cors.html")
MDN_COOKIES = ("MDN — Using HTTP cookies", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies")
MDN_SET_COOKIE = ("MDN — Set-Cookie", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie")
OWASP_SESSION = ("OWASP — Session Management Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html")
ERL_GITHUB = ("express-rate-limit (GitHub)", "https://github.com/express-rate-limit/express-rate-limit")
EX_PROXIES = ("Express — Express behind proxies", "https://expressjs.com/en/guide/behind-proxies.html")
OWASP_AUTH = ("OWASP — Authentication Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html")
OWASP_JWT = ("OWASP — JSON Web Token Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html")
JWT_LIB = ("jsonwebtoken (GitHub)", "https://github.com/auth0/node-jsonwebtoken")
OWASP_CSRF = ("OWASP — Cross-Site Request Forgery Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html")
OWASP_STUFFING = ("OWASP — Credential Stuffing Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ express-015
    Q(
        id="express-015", sub="CORS", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["cors", "browser", "fetch", "origin"],
        ver="Express 5.x; cors 2.x", vs=False, status="stable",
        q_en=r"""A React app on `http://localhost:5173` calls your Express API on `http://localhost:3000` with `fetch`. The browser console says the request was *blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present*. Which fix is correct?""",
        q_bn=r"""`http://localhost:5173`-এ চলা একটি React app `fetch` দিয়ে `http://localhost:3000`-এর Express API call করে। Browser console বলছে request-টি *blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present*। কোন সমাধানটি সঠিক?""",
        options=[
            ("In the React app, add `mode: 'no-cors'` to the `fetch` call", "React app-এ `fetch` call-এ `mode: 'no-cors'` যোগ করা"),
            ("In the Express API, return `Access-Control-Allow-Origin` for the frontend's origin (e.g. with the `cors` middleware)", "Express API-তে frontend-এর origin-এর জন্য `Access-Control-Allow-Origin` return করা (যেমন `cors` middleware দিয়ে)"),
            ("In the React app, send an `Access-Control-Allow-Origin: *` request header", "React app থেকে `Access-Control-Allow-Origin: *` request header পাঠানো"),
            ("Nothing — CORS errors only happen in development and disappear in production", "কিছুই না — CORS error শুধু development-এ হয়, production-এ চলে যায়"),
        ],
        correct=1,
        a_en=r"""
            Fix it on the server. The browser enforces CORS, but the *permission* has to come from the API's response headers. The two URLs are different origins (different ports), so the API must answer with `Access-Control-Allow-Origin: http://localhost:5173` (and handle preflight requests), which the `cors` middleware does for you.
        """,
        a_bn=r"""
            Server-এ ঠিক করতে হবে। CORS browser enforce করে, কিন্তু *অনুমতি* আসতে হয় API-র response header থেকে। দুটো URL আলাদা origin (port আলাদা), তাই API-কে `Access-Control-Allow-Origin: http://localhost:5173` দিয়ে উত্তর দিতে হবে (আর preflight request handle করতে হবে) — `cors` middleware এটা করে দেয়।
        """,
        ex_en=r"""
            - **Option A is the tempting trap:** `no-cors` doesn't bypass anything — it gives you an *opaque* response whose body and status you can't read, so your code still fails.
            - **Option C:** `Access-Control-Allow-*` are *response* headers; sending them from the client does nothing (and may trigger a preflight).
            - **Option D:** production often has the same issue (`app.example.com` calling `api.example.com` are different origins).
            - **Alternatives:** a dev-server proxy (e.g. Vite `server.proxy`) or serving the frontend and API from the same origin avoids CORS entirely.
            - **Remember:** CORS only controls whether *browser JavaScript* can read responses. It's not authentication — `curl` or a server can still call your API, so you still need auth and authorization.
        """,
        ex_bn=r"""
            - **Option A হলো প্রলোভনের ফাঁদ:** `no-cors` কিছুই bypass করে না — এটা একটি *opaque* response দেয়, যার body আর status পড়া যায় না, তাই code তবুও fail করে।
            - **Option C:** `Access-Control-Allow-*` হলো *response* header; client থেকে পাঠালে কিছুই হয় না (বরং preflight trigger হতে পারে)।
            - **Option D:** production-এও প্রায়ই একই সমস্যা হয় (`app.example.com` থেকে `api.example.com` call করা আলাদা origin)।
            - **বিকল্প:** dev-server proxy (যেমন Vite-এর `server.proxy`) বা frontend আর API একই origin থেকে serve করলে CORS-এর প্রশ্নই আসে না।
            - **মনে রাখো:** CORS শুধু নিয়ন্ত্রণ করে *browser-এর JavaScript* response পড়তে পারবে কি না। এটা authentication নয় — `curl` বা অন্য server তবুও API call করতে পারে, তাই auth আর authorization লাগবেই।
        """,
        tip_en=r"""Say "the browser enforces it, the server grants it" — that one line shows you understand who does what in CORS.""",
        tip_bn=r"""বলো "browser enforce করে, server অনুমতি দেয়" — এই এক লাইনেই বোঝা যায় CORS-এ কে কী করে তুমি জানো।""",
        refs=[MDN_CORS, EX_CORS],
    ),
    # ------------------------------------------------------------------ express-016
    Q(
        id="express-016", sub="Cookies & Sessions", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["cookies", "httponly", "samesite", "secure", "sessions"],
        ver="Express 5.x", vs=False, status="stable",
        q_en=r"""Your Express API sets a session cookie after login. Which cookie attributes would you set, and what does each one protect against?""",
        q_bn=r"""তোমার Express API login-এর পর একটি session cookie set করে। কোন কোন cookie attribute set করবে, আর প্রতিটি কীসের বিরুদ্ধে সুরক্ষা দেয়?""",
        a_en=r"""
            - **`httpOnly: true`** — JavaScript can't read the cookie (`document.cookie`), so an XSS bug can't simply steal the session.
            - **`secure: true`** — sent only over HTTPS, so it can't leak over plain HTTP.
            - **`sameSite: 'lax'`** (or `'strict'`) — the browser doesn't attach it to most cross-site requests, which is the main defence against CSRF. `'none'` is only for genuinely cross-site use and requires `secure`.
            - **`maxAge` / `expires`** — limits the lifetime; together with server-side expiry it reduces the damage of a stolen cookie.
            - **`path` and `domain`** — keep the scope narrow. Avoid setting `domain` unless subdomains really need the cookie.
            - **`__Host-` name prefix** — the browser only accepts it with `Secure`, `Path=/` and no `Domain`, so a subdomain can't overwrite it.

            The cookie should hold only an opaque session ID (or a signed value), never user data you trust without checking.
        """,
        a_bn=r"""
            - **`httpOnly: true`** — JavaScript cookie পড়তে পারে না (`document.cookie`), তাই কোনো XSS bug সহজে session চুরি করতে পারে না।
            - **`secure: true`** — শুধু HTTPS-এ পাঠানো হয়, তাই সাধারণ HTTP-তে ফাঁস হয় না।
            - **`sameSite: 'lax'`** (বা `'strict'`) — বেশিরভাগ cross-site request-এ browser এটা যুক্ত করে না, যা CSRF-এর বিরুদ্ধে প্রধান প্রতিরক্ষা। `'none'` শুধু সত্যিকারের cross-site ব্যবহারের জন্য, আর এর সাথে `secure` বাধ্যতামূলক।
            - **`maxAge` / `expires`** — আয়ু সীমিত করে; server-side expiry-র সাথে মিলে চুরি হওয়া cookie-র ক্ষতি কমায়।
            - **`path` ও `domain`** — scope সংকীর্ণ রাখো। Subdomain-এর সত্যিই দরকার না হলে `domain` set করো না।
            - **`__Host-` নামের prefix** — browser এটা শুধু `Secure`, `Path=/` আর `Domain` ছাড়া গ্রহণ করে, তাই কোনো subdomain এটা overwrite করতে পারে না।

            Cookie-তে শুধু একটি opaque session ID (বা signed value) থাকা উচিত, যাচাই ছাড়া বিশ্বাস করা কোনো user data কখনো নয়।
        """,
        ex_en=r"""
            - **Same-site vs same-origin:** `app.example.com` and `api.example.com` are different *origins* (CORS applies) but the same *site* (`example.com`), so `SameSite=Lax` cookies are still sent between them.
            - **Browsers default to `Lax`** when `SameSite` is missing in modern Chromium-based browsers, but set it explicitly — behaviour differs across browsers and versions.
            - **Reading cookies** in Express needs `cookie-parser` (`req.cookies`), or a session library like `express-session` that parses its own cookie.
            - **Behind a proxy**, set `app.set('trust proxy', 1)` — otherwise Express thinks the request is HTTP and `express-session` won't send a `secure` cookie.
            - **Express 5:** `res.clearCookie()` ignores `maxAge`/`expires`; pass the same `path`/`domain` used when setting the cookie, or it won't be cleared.
            - **Session fixation:** regenerate the session ID after login (`req.session.regenerate()` in express-session).
        """,
        ex_bn=r"""
            - **Same-site বনাম same-origin:** `app.example.com` আর `api.example.com` আলাদা *origin* (CORS প্রযোজ্য) কিন্তু একই *site* (`example.com`), তাই `SameSite=Lax` cookie এদের মধ্যে তবুও পাঠানো হয়।
            - আধুনিক Chromium-ভিত্তিক browser-এ `SameSite` না থাকলে default **`Lax`** ধরা হয়, তবুও স্পষ্ট করে set করো — browser আর version অনুযায়ী আচরণ আলাদা হতে পারে।
            - Express-এ **cookie পড়তে** `cookie-parser` (`req.cookies`) লাগে, অথবা `express-session`-এর মতো session library যা নিজের cookie নিজেই parse করে।
            - **Proxy-র পেছনে** `app.set('trust proxy', 1)` দাও — নইলে Express request-কে HTTP মনে করে এবং `express-session` `secure` cookie পাঠায় না।
            - **Express 5:** `res.clearCookie()` `maxAge`/`expires` ignore করে; set করার সময়ের একই `path`/`domain` দাও, নইলে cookie মুছবে না।
            - **Session fixation:** login-এর পর session ID নতুন করে তৈরি করো (express-session-এ `req.session.regenerate()`)।
        """,
        tip_en=r"""Pair each attribute with the attack it stops: httpOnly → XSS theft, secure → sniffing, SameSite → CSRF. That one-to-one mapping is exactly what interviewers want.""",
        tip_bn=r"""প্রতিটি attribute-কে সে যে attack থামায় তার সাথে জোড়া দাও: httpOnly → XSS চুরি, secure → sniffing, SameSite → CSRF। এই এক-এক mapping-টাই interviewer চায়।""",
        mist_en=r"""Thinking `httpOnly` prevents XSS (it only stops cookie theft — the attacker can still act as the user from the page), or storing user roles in an unsigned cookie.""",
        mist_bn=r"""`httpOnly` XSS আটকায় মনে করা (এটা শুধু cookie চুরি আটকায় — attacker তবুও page থেকে user হয়ে কাজ করতে পারে), অথবা unsigned cookie-তে user role রাখা।""",
        code=r"""
            app.post('/auth/login', async (req, res) => {
              const user = await verifyCredentials(req.body.email, req.body.password);
              const sessionId = await sessions.create(user.id); // opaque, random, stored server-side

              res.cookie('__Host-sid', sessionId, {
                httpOnly: true,
                secure: true,
                sameSite: 'lax',
                path: '/',
                maxAge: 8 * 60 * 60 * 1000, // 8 hours, in milliseconds
              });
              res.sendStatus(204);
            });

            app.post('/auth/logout', async (req, res) => {
              await sessions.destroy(req.cookies['__Host-sid']); // needs cookie-parser
              res.clearCookie('__Host-sid', { path: '/', secure: true, httpOnly: true, sameSite: 'lax' });
              res.sendStatus(204);
            });
        """,
        lang="javascript",
        follow=[
            ("Is `SameSite=Lax` enough CSRF protection on its own?", "শুধু `SameSite=Lax` কি যথেষ্ট CSRF সুরক্ষা?"),
            ("Why should you regenerate the session ID after login?", "Login-এর পর session ID নতুন করে কেন তৈরি করা উচিত?"),
        ],
        related=["express-017", "express-024"],
        refs=[MDN_SET_COOKIE, MDN_COOKIES, OWASP_SESSION],
    ),
    # ------------------------------------------------------------------ express-017
    Q(
        id="express-017", sub="CORS", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["cors", "credentials", "cookies", "preflight", "debugging"],
        ver="Express 5.x; cors 2.x", vs=True, status="stable",
        q_en=r"""The SPA on `https://app.example.com` calls the API on `https://api.example.com` with cookie-based sessions. First, `/me` always returned `401`. A developer added `credentials: 'include'` to `fetch`, and now the browser blocks the response with: *The value of the 'Access-Control-Allow-Origin' header must not be the wildcard '*' when the request's credentials mode is 'include'*. Fix the client and the server.""",
        q_bn=r"""`https://app.example.com`-এর SPA cookie-ভিত্তিক session দিয়ে `https://api.example.com`-এর API call করে। প্রথমে `/me` সবসময় `401` দিচ্ছিল। একজন developer `fetch`-এ `credentials: 'include'` যোগ করেছে, আর এখন browser response block করছে এই message দিয়ে: *The value of the 'Access-Control-Allow-Origin' header must not be the wildcard '*' when the request's credentials mode is 'include'*। Client আর server দুটোই ঠিক করো।""",
        a_en=r"""
            Two separate problems:

            1. **The `401`:** by default, a cross-origin `fetch` doesn't send cookies. Adding `credentials: 'include'` was the right client-side fix.
            2. **The CORS block:** for credentialed requests, the browser requires the API to name the exact origin — `Access-Control-Allow-Origin: *` is not allowed — and to send `Access-Control-Allow-Credentials: true`. The current `cors({ origin: '*', credentials: true })` produces exactly the forbidden combination (verified: it sends `*` together with `credentials: true`).

            Fix on the server: an explicit allow-list, `cors({ origin: ['https://app.example.com'], credentials: true })`. The middleware then echoes the matching origin, adds `Vary: Origin`, and omits `Access-Control-Allow-Origin` for any other origin, so the browser blocks those responses. Register it before the routes with `app.use()` so preflight `OPTIONS` requests are handled too.
        """,
        a_bn=r"""
            দুটো আলাদা সমস্যা:

            1. **`401`:** default-ভাবে cross-origin `fetch` cookie পাঠায় না। `credentials: 'include'` যোগ করাটা client-এর দিকে সঠিক fix ছিল।
            2. **CORS block:** credential সহ request-এর ক্ষেত্রে browser চায় API নির্দিষ্ট origin-এর নাম বলুক — `Access-Control-Allow-Origin: *` চলবে না — এবং `Access-Control-Allow-Credentials: true` পাঠাক। বর্তমান `cors({ origin: '*', credentials: true })` ঠিক এই নিষিদ্ধ সমন্বয়টাই তৈরি করে (যাচাই করা: এটা `credentials: true`-এর সাথে `*` পাঠায়)।

            Server-এ fix: একটি স্পষ্ট allow-list, `cors({ origin: ['https://app.example.com'], credentials: true })`। Middleware তখন মিলে যাওয়া origin echo করে, `Vary: Origin` যোগ করে, আর অন্য যেকোনো origin-এর জন্য `Access-Control-Allow-Origin` বাদ দেয়, ফলে browser সেই response block করে। Route-এর আগে `app.use()` দিয়ে register করো, যাতে preflight `OPTIONS` request-ও handle হয়।
        """,
        ex_en=r"""
            - **Why `*` is forbidden with credentials:** otherwise any website could make a logged-in user's browser call your API *with their cookies* and read the response.
            - **Never reflect any origin blindly** (`origin: true` or echoing `req.headers.origin`) together with `credentials: true` — that recreates the same hole. Use a fixed list or a strict function.
            - **Cookies across subdomains:** `app.example.com` → `api.example.com` is cross-origin but **same-site**, so a `SameSite=Lax` cookie is sent. Only a truly cross-site setup (e.g. `app.example.com` → `api.example.net`) needs `SameSite=None; Secure` — and third-party cookie restrictions may still block it, so prefer same-site domains.
            - **Express 5 gotcha:** the old `app.options('*', cors())` line throws at startup because `*` isn't valid path syntax anymore. `app.use(cors(...))` already answers preflights (204); if you need an explicit route, use `'/{*splat}'`.
            - **CSRF:** cookie auth + CORS still needs CSRF protection (SameSite plus a CSRF token or an Origin check) for state-changing requests.
        """,
        ex_bn=r"""
            - **Credential-এর সাথে `*` কেন নিষিদ্ধ:** না হলে যেকোনো website logged-in user-এর browser দিয়ে *তার cookie সহ* তোমার API call করে response পড়ে ফেলতে পারত।
            - **কখনো চোখ বন্ধ করে যেকোনো origin reflect করো না** (`origin: true` বা `req.headers.origin` echo করা) `credentials: true`-এর সাথে — এতে একই ফুটো আবার তৈরি হয়। নির্দিষ্ট list বা কড়া function ব্যবহার করো।
            - **Subdomain-জুড়ে cookie:** `app.example.com` → `api.example.com` cross-origin কিন্তু **same-site**, তাই `SameSite=Lax` cookie পাঠানো হয়। শুধু সত্যিকারের cross-site setup-এ (যেমন `app.example.com` → `api.example.net`) `SameSite=None; Secure` লাগে — আর third-party cookie restriction তখনও block করতে পারে, তাই same-site domain-ই ভালো।
            - **Express 5-এর gotcha:** পুরনো `app.options('*', cors())` line startup-এ throw করে, কারণ `*` আর valid path syntax নয়। `app.use(cors(...))` নিজেই preflight-এর উত্তর দেয় (204); আলাদা route লাগলে `'/{*splat}'` ব্যবহার করো।
            - **CSRF:** cookie auth + CORS থাকলেও state-changing request-এর জন্য CSRF সুরক্ষা লাগে (SameSite আর CSRF token বা Origin check)।
        """,
        tip_en=r"""Separate the two failures clearly (cookies not sent vs credentials + wildcard), then explain *why* the wildcard rule exists. Mentioning same-site vs same-origin for the cookie is a strong bonus.""",
        tip_bn=r"""দুটো failure স্পষ্টভাবে আলাদা করো (cookie না যাওয়া বনাম credential + wildcard), তারপর wildcard নিয়মটা *কেন* আছে ব্যাখ্যা করো। Cookie-র জন্য same-site বনাম same-origin-এর উল্লেখ বড় বোনাস।""",
        mist_en=r""""Fixing" it with `origin: true` (reflects every origin with credentials), or setting `SameSite=None` on all cookies without understanding same-site.""",
        mist_bn=r"""`origin: true` দিয়ে "ঠিক" করা (credential সহ সব origin reflect করে), অথবা same-site না বুঝেই সব cookie-তে `SameSite=None` দেওয়া।""",
        code=r"""
            // server (api.example.com)
            import cors from 'cors';
            import cookieParser from 'cookie-parser';

            app.use(cors({ origin: '*', credentials: true }));
            app.use(cookieParser());
            app.get('/me', requireSession, (req, res) => res.json(req.user));

            // client (app.example.com)
            const res = await fetch('https://api.example.com/me', { credentials: 'include' });
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                // server (api.example.com)
                const allowedOrigins = ['https://app.example.com'];

                app.use(cors({
                  origin: allowedOrigins,  // echoes the matching origin, adds Vary: Origin
                  credentials: true,       // Access-Control-Allow-Credentials: true
                }));                       // registered before routes: also answers preflight OPTIONS
                app.use(cookieParser());
                app.get('/me', requireSession, (req, res) => res.json(req.user));

                // client (app.example.com)
                const res = await fetch('https://api.example.com/me', { credentials: 'include' });
            """, label_en="Fixed version", label_bn="সংশোধিত version"),
        ],
        follow=[
            ("When does the browser send a preflight request, and what does the server have to answer?", "Browser কখন preflight request পাঠায়, আর server-কে কী উত্তর দিতে হয়?"),
            ("How would you allow every subdomain of example.com safely?", "example.com-এর সব subdomain নিরাপদে কীভাবে allow করবে?"),
        ],
        related=["express-015", "express-016"],
        refs=[MDN_CORS, EX_CORS, OWASP_CSRF],
    ),
    # ------------------------------------------------------------------ express-018
    Q(
        id="express-018", sub="Rate Limiting", diff="medium", type="scenario",
        prio="high", market="both", mins=7,
        tags=["rate-limiting", "express-rate-limit", "redis", "trust-proxy", "brute-force"],
        ver="Express 5.x; express-rate-limit 8.x; rate-limit-redis", vs=True, status="stable",
        q_en=r"""Your login endpoint is being hammered with password-guessing attempts. The API runs as 4 instances behind NGINX. How would you add rate limiting to this Express 5 app, and what pitfalls would you watch out for?""",
        q_bn=r"""তোমার login endpoint-এ password অনুমান করার চেষ্টায় ক্রমাগত আঘাত আসছে। API NGINX-এর পেছনে 4টি instance হিসেবে চলে। এই Express 5 app-এ কীভাবে rate limiting যোগ করবে, আর কোন কোন ফাঁদ সম্পর্কে সতর্ক থাকবে?""",
        a_en=r"""
            I'd clarify the goal first — stop brute force on login without locking out real users — then layer it:

            1. **Edge:** a coarse NGINX `limit_req` on `/auth/login` to absorb floods cheaply.
            2. **App:** `express-rate-limit` with a **strict limiter only on login** (and OTP/password-reset), plus a looser global API limiter.

            Pitfalls I'd handle explicitly:
            - **Shared store:** the default in-memory store counts per process. With 4 instances an attacker effectively gets 4× the limit, and counters reset on every deploy. Use a Redis store so all instances share counters.
            - **Real client IP:** set `app.set('trust proxy', 1)`. Without it every request appears to come from NGINX (one IP for everyone); with `true` the IP is spoofable via `X-Forwarded-For`.
            - **Right key:** for login, key by IP **and** account (`ip:email`), and count only failures (`skipSuccessfulRequests`). In v8, use `ipKeyGenerator(req.ip)` in custom keys so IPv6 users are grouped by subnet.
            - **Good responses:** `429` with `Retry-After` and standard `RateLimit` headers; the same generic message whether or not the account exists.
            - **Failure mode:** decide what happens if Redis is down — fail open (availability) or closed (security) — and set timeouts.
        """,
        a_bn=r"""
            প্রথমে লক্ষ্য পরিষ্কার করব — আসল user-কে lock out না করে login-এ brute force থামানো — তারপর স্তরে স্তরে সাজাব:

            1. **Edge:** `/auth/login`-এ মোটা দাগের NGINX `limit_req`, যাতে সস্তায় বন্যা আটকানো যায়।
            2. **App:** `express-rate-limit`, **শুধু login-এ কড়া limiter** (আর OTP/password-reset-এ), সাথে পুরো API-র জন্য একটু ঢিলা global limiter।

            যে ফাঁদগুলো স্পষ্টভাবে সামলাব:
            - **Shared store:** default in-memory store প্রতিটি process-এ আলাদা গোনে। 4টি instance থাকলে attacker কার্যত 4 গুণ limit পায়, আর প্রতি deploy-এ counter reset হয়। Redis store ব্যবহার করো, যাতে সব instance counter share করে।
            - **আসল client IP:** `app.set('trust proxy', 1)` দাও। না দিলে প্রতিটি request NGINX থেকে আসছে মনে হয় (সবার জন্য একটি IP); `true` দিলে `X-Forwarded-For` দিয়ে IP নকল করা যায়।
            - **সঠিক key:** login-এর জন্য IP **এবং** account দিয়ে key (`ip:email`), আর শুধু failure গোনা (`skipSuccessfulRequests`)। v8-এ custom key-তে `ipKeyGenerator(req.ip)` ব্যবহার করো, যাতে IPv6 user-রা subnet অনুযায়ী group হয়।
            - **ভালো response:** `Retry-After` আর standard `RateLimit` header সহ `429`; account থাকুক বা না থাকুক একই সাধারণ message।
            - **Failure mode:** Redis down হলে কী হবে ঠিক করো — fail open (availability) নাকি closed (security) — আর timeout set করো।
        """,
        ex_en=r"""
            - **Order matters:** `express.json()` must run before the limiter if the key uses `req.body.email`.
            - **Account-only keys cut both ways:** limiting per account across all IPs stops distributed guessing but lets an attacker lock a victim out. Combining `ip:account` with a separate, softer per-account limit (or CAPTCHA/progressive delay instead of a hard block) balances both.
            - **express-rate-limit 8 details:** the option is `limit` (formerly `max`); `standardHeaders: 'draft-8'` sends the combined `RateLimit` and `RateLimit-Policy` headers; the library logs validation errors for misconfigurations such as `X-Forwarded-For` without `trust proxy`, or a custom key generator that uses `req.ip` without `ipKeyGenerator`.
            - **Verified behaviour:** with `limit: 3` and `skipSuccessfulRequests`, the 4th failed attempt from the same IP+email got `429` with `Retry-After: 900`.
            - Rate limiting slows attackers; it doesn't replace MFA, breached-password checks or strong password hashing.
        """,
        ex_bn=r"""
            - **ক্রম গুরুত্বপূর্ণ:** key যদি `req.body.email` ব্যবহার করে, তাহলে limiter-এর আগে `express.json()` চলতে হবে।
            - **শুধু account-ভিত্তিক key-র দুই দিক:** সব IP মিলিয়ে account প্রতি limit দিলে distributed guessing থামে, কিন্তু attacker একজন নিরীহ user-কে lock out করে দিতে পারে। `ip:account`-এর সাথে আলাদা একটু নরম per-account limit (বা hard block-এর বদলে CAPTCHA/progressive delay) দুটোর ভারসাম্য রাখে।
            - **express-rate-limit 8-এর খুঁটিনাটি:** option-এর নাম `limit` (আগে ছিল `max`); `standardHeaders: 'draft-8'` একত্রিত `RateLimit` আর `RateLimit-Policy` header পাঠায়; ভুল configuration-এ library validation error log করে, যেমন `trust proxy` ছাড়া `X-Forwarded-For`, বা `ipKeyGenerator` ছাড়া `req.ip` ব্যবহার করা custom key generator।
            - **যাচাই করা আচরণ:** `limit: 3` আর `skipSuccessfulRequests` দিয়ে একই IP+email থেকে চতুর্থ ব্যর্থ চেষ্টায় `Retry-After: 900` সহ `429` এসেছে।
            - Rate limiting attacker-কে ধীর করে; এটা MFA, breached-password check বা শক্ত password hashing-এর বিকল্প নয়।
        """,
        tip_en=r"""Structure: goal → layers (edge + app) → the three classic pitfalls (shared store, trust proxy, key choice) → response format → failure mode. Naming the in-memory-store-with-multiple-instances bug is what interviewers listen for.""",
        tip_bn=r"""কাঠামো: লক্ষ্য → স্তর (edge + app) → তিনটি classic ফাঁদ (shared store, trust proxy, key বাছাই) → response format → failure mode। একাধিক instance-এ in-memory store-এর bug-এর নাম বলাটাই interviewer শুনতে চায়।""",
        mist_en=r"""Using the default memory store on multiple instances, forgetting `trust proxy` (everyone shares one IP), or applying the strict login limit to the whole API.""",
        mist_bn=r"""একাধিক instance-এ default memory store ব্যবহার করা, `trust proxy` ভুলে যাওয়া (সবাই একটি IP share করে), অথবা login-এর কড়া limit পুরো API-তে লাগিয়ে দেওয়া।""",
        code=r"""
            import express from 'express';
            import { rateLimit, ipKeyGenerator } from 'express-rate-limit';
            import { RedisStore } from 'rate-limit-redis';
            import { createClient } from 'redis';

            const redis = await createClient({ url: process.env.REDIS_URL })
              .on('error', (err) => console.error('redis error', err))
              .connect();

            const app = express();
            app.set('trust proxy', 1); // exactly one NGINX hop in front

            const loginLimiter = rateLimit({
              windowMs: 15 * 60 * 1000,
              limit: 5,                       // 5 failed attempts per IP+account per window
              skipSuccessfulRequests: true,   // successful logins don't count
              standardHeaders: 'draft-8',
              legacyHeaders: false,
              keyGenerator: (req) =>
                `${ipKeyGenerator(req.ip)}:${String(req.body?.email ?? '').trim().toLowerCase()}`,
              store: new RedisStore({
                prefix: 'rl:login:',
                sendCommand: (...args) => redis.sendCommand(args),
              }),
            });

            // Body must be parsed before the limiter reads req.body.email
            app.post('/auth/login', express.json({ limit: '2kb' }), loginLimiter, loginHandler);
        """,
        lang="javascript",
        follow=[
            ("How would you rate-limit per API key with different plans (free vs paid)?", "আলাদা plan (free বনাম paid) অনুযায়ী API key প্রতি কীভাবে rate-limit করবে?"),
            ("Fixed window vs sliding window: what's the difference and does it matter here?", "Fixed window বনাম sliding window: পার্থক্য কী, আর এখানে কি তা গুরুত্বপূর্ণ?"),
        ],
        related=["express-014", "express-020"],
        refs=[ERL_GITHUB, EX_PROXIES, OWASP_AUTH],
    ),
    # ------------------------------------------------------------------ express-019
    Q(
        id="express-019", sub="JWT", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["jwt", "refresh-token", "token-rotation", "reuse-detection", "authentication"],
        ver="Express 5.x; jsonwebtoken 9.x", vs=False, status="stable",
        q_en=r"""You're building authentication for a React SPA (`app.example.com`) and an Express API (`api.example.com`). Design the access/refresh token flow: where each token is stored, how long it lives, how refreshing works, and how you handle logout and a stolen refresh token.""",
        q_bn=r"""একটি React SPA (`app.example.com`) আর একটি Express API (`api.example.com`)-এর জন্য authentication বানাচ্ছ। Access/refresh token flow design করো: কোন token কোথায় রাখা হবে, কতক্ষণ বাঁচবে, refresh কীভাবে কাজ করবে, আর logout ও চুরি হওয়া refresh token কীভাবে সামলাবে।""",
        a_en=r"""
            - **Access token:** a short-lived JWT (about 5–15 minutes) with minimal claims (`sub`, role, `iss`, `aud`), signed with a strong secret (HS256) or a private key (RS256/EdDSA with a `kid` for rotation). The SPA keeps it **in memory** and sends it as `Authorization: Bearer …`. Not in `localStorage`, where any XSS can read it.
            - **Refresh token:** a long-lived (e.g. 30 days), **opaque random value**, stored **hashed** in the database with user, device, expiry and a *family ID*. It's delivered as an `httpOnly; Secure; SameSite=Strict` cookie scoped to `Path=/auth/refresh`, so JavaScript never sees it and it isn't sent to other endpoints.
            - **Refresh with rotation:** `POST /auth/refresh` looks up the token's hash, checks expiry/revocation, **marks it used and issues a new refresh token** plus a new access token — atomically.
            - **Reuse detection:** if a refresh token that was already rotated is presented again, someone has a copy. Revoke the whole family (every token from that login), force re-login, and alert.
            - **Logout:** delete the refresh token record and clear the cookie. The access token dies within minutes; for instant revocation (e.g. a banned user) keep a short-lived deny-list of `jti`s in Redis or check a user `tokenVersion`.
            - **Password change / "log out everywhere":** revoke all refresh tokens of the user.
        """,
        a_bn=r"""
            - **Access token:** অল্প আয়ুর JWT (প্রায় ৫–১৫ মিনিট), ন্যূনতম claim সহ (`sub`, role, `iss`, `aud`), শক্ত secret (HS256) বা private key (rotation-এর জন্য `kid` সহ RS256/EdDSA) দিয়ে signed। SPA এটা **memory-তে** রাখে এবং `Authorization: Bearer …` হিসেবে পাঠায়। `localStorage`-এ নয়, যেখানে যেকোনো XSS এটা পড়তে পারে।
            - **Refresh token:** দীর্ঘ আয়ুর (যেমন ৩০ দিন) **opaque random value**, database-এ **hash করে** রাখা, সাথে user, device, expiry আর একটি *family ID*। এটা `Path=/auth/refresh`-এ সীমিত `httpOnly; Secure; SameSite=Strict` cookie হিসেবে পাঠানো হয়, তাই JavaScript কখনো দেখে না এবং অন্য endpoint-এ যায় না।
            - **Rotation সহ refresh:** `POST /auth/refresh` token-এর hash খোঁজে, expiry/revocation check করে, **সেটাকে used চিহ্নিত করে নতুন refresh token** আর নতুন access token দেয় — atomically।
            - **Reuse detection:** আগেই rotate হওয়া refresh token আবার এলে বুঝতে হবে কারও কাছে কপি আছে। পুরো family (ওই login-এর সব token) revoke করো, আবার login করাও, আর alert দাও।
            - **Logout:** refresh token record মুছে cookie clear করো। Access token কয়েক মিনিটে মরে যায়; তাৎক্ষণিক revocation লাগলে (যেমন ban হওয়া user) Redis-এ `jti`-র স্বল্পমেয়াদি deny-list রাখো বা user-এর `tokenVersion` check করো।
            - **Password change / "সব জায়গা থেকে logout":** user-এর সব refresh token revoke করো।
        """,
        ex_en=r"""
            - **Why `SameSite=Strict` works here:** `app.example.com` and `api.example.com` are the same *site*, so the browser still sends the cookie on the SPA's `fetch` to `/auth/refresh` (with `credentials: 'include'`). Add an Origin check or CSRF token on the refresh endpoint as defence in depth.
            - **Why opaque refresh tokens:** they must be revocable and looked up anyway, so a JWT's self-contained nature buys nothing — and hashing them means a DB leak doesn't leak usable tokens.
            - **Concurrency:** two tabs refreshing at the same moment can look like reuse. Mitigate with a single-flight refresh in the client, or a short grace window where the just-rotated token returns the same new pair.
            - **JWT verification:** always pin `algorithms` (e.g. `['HS256']`), verify `iss`/`aud`/`exp`, and never accept `alg: none`.
            - **Simpler alternative:** for a single first-party web app, a classic server-side session cookie may be simpler and easier to revoke — JWTs shine when several services or mobile clients verify tokens independently.
        """,
        ex_bn=r"""
            - **এখানে `SameSite=Strict` কেন কাজ করে:** `app.example.com` আর `api.example.com` একই *site*, তাই SPA-র `/auth/refresh`-এ করা `fetch`-এ (`credentials: 'include'` সহ) browser cookie পাঠায়। বাড়তি সুরক্ষা হিসেবে refresh endpoint-এ Origin check বা CSRF token যোগ করো।
            - **Opaque refresh token কেন:** এগুলো revoke করতে হবে এবং খুঁজতেই হবে, তাই JWT-র self-contained হওয়ায় কোনো লাভ নেই — আর hash করে রাখলে DB leak হলেও ব্যবহারযোগ্য token ফাঁস হয় না।
            - **Concurrency:** দুটো tab একই মুহূর্তে refresh করলে reuse-এর মতো দেখাতে পারে। Client-এ single-flight refresh, বা অল্প grace window রাখা যেখানে সদ্য rotate হওয়া token একই নতুন জোড়া ফেরত দেয় — এভাবে সামলাও।
            - **JWT verification:** সবসময় `algorithms` pin করো (যেমন `['HS256']`), `iss`/`aud`/`exp` verify করো, আর কখনো `alg: none` গ্রহণ করো না।
            - **সহজ বিকল্প:** একটি মাত্র first-party web app-এর জন্য classic server-side session cookie হয়তো সহজ এবং revoke করাও সহজ — JWT তখনই উজ্জ্বল যখন একাধিক service বা mobile client নিজে নিজে token verify করে।
        """,
        tip_en=r"""Draw the two tokens side by side (lifetime, format, storage, transport), then walk through refresh → rotation → reuse detection. Ending with "or just use sessions if it's one web app" shows mature judgement.""",
        tip_bn=r"""দুটো token পাশাপাশি আঁকো (আয়ু, format, storage, পাঠানোর উপায়), তারপর refresh → rotation → reuse detection ধাপে ধাপে বলো। শেষে "একটি web app হলে সরাসরি session ব্যবহার করো" বলা পরিণত বিচারবুদ্ধি দেখায়।""",
        mist_en=r"""Storing tokens in `localStorage`, issuing long-lived (days) access tokens, using a JWT refresh token that can't be revoked, or never rotating refresh tokens.""",
        mist_bn=r"""`localStorage`-এ token রাখা, দীর্ঘ আয়ুর (কয়েক দিন) access token দেওয়া, revoke করা যায় না এমন JWT refresh token ব্যবহার করা, অথবা refresh token কখনো rotate না করা।""",
        code=r"""
            import { randomBytes, createHash } from 'node:crypto';
            import jwt from 'jsonwebtoken';

            const hash = (token) => createHash('sha256').update(token).digest('hex');
            const REFRESH_COOKIE = {
              httpOnly: true, secure: true, sameSite: 'strict',
              path: '/auth/refresh', maxAge: 30 * 24 * 60 * 60 * 1000,
            };

            function signAccessToken(user) {
              return jwt.sign({ sub: String(user.id), role: user.role }, process.env.JWT_SECRET, {
                algorithm: 'HS256', expiresIn: '10m',
                issuer: 'api.example.com', audience: 'app.example.com',
              });
            }

            app.post('/auth/refresh', async (req, res) => {
              const presented = req.cookies?.rt;                     // needs cookie-parser
              if (!presented) throw new AppError(401, 'NO_REFRESH_TOKEN', 'Not authenticated');

              const record = await refreshTokens.findByHash(hash(presented));
              if (!record || record.revokedAt || record.expiresAt < Date.now()) {
                throw new AppError(401, 'INVALID_REFRESH_TOKEN', 'Not authenticated');
              }

              if (record.usedAt) {                                   // already rotated => stolen copy
                await refreshTokens.revokeFamily(record.familyId);
                res.clearCookie('rt', { path: '/auth/refresh' });
                throw new AppError(401, 'REFRESH_TOKEN_REUSED', 'Please sign in again');
              }

              const newToken = randomBytes(32).toString('base64url');
              await refreshTokens.rotate(record, {                   // mark old used + insert new, in one transaction
                tokenHash: hash(newToken),
                expiresAt: Date.now() + REFRESH_COOKIE.maxAge,
              });

              const user = await users.findById(record.userId);
              res.cookie('rt', newToken, REFRESH_COOKIE);
              res.json({ accessToken: signAccessToken(user) });
            });
        """,
        lang="javascript",
        follow=[
            ("How would this design change for a native mobile app?", "Native mobile app-এর জন্য এই design কীভাবে বদলাবে?"),
            ("How do you rotate the JWT signing key without logging everyone out?", "সবাইকে logout না করিয়ে JWT signing key কীভাবে rotate করবে?"),
            ("How do you avoid false reuse alarms when two tabs refresh at once?", "দুটো tab একসাথে refresh করলে ভুল reuse alarm কীভাবে এড়াবে?"),
        ],
        related=["express-024", "express-023", "express-016"],
        refs=[OWASP_JWT, JWT_LIB, OWASP_SESSION],
    ),
    # ------------------------------------------------------------------ express-020
    Q(
        id="express-020", sub="Authentication", diff="extreme", type="scenario",
        prio="high", market="international", mins=20,
        tags=["credential-stuffing", "incident-response", "rate-limiting", "mfa", "bot-defense", "security"],
        ver="Express 5.x; express-rate-limit 8.x (example)", vs=False, status="stable",
        q_en=r"""Saturday night: your Express login endpoint suddenly receives about 40,000 attempts per minute from roughly 15,000 different IPs (residential proxies), using email/password pairs leaked from another website. Per-IP rate limiting isn't stopping it, several accounts have been taken over, and database CPU is at 95%. Walk through how you respond right now and what you build afterwards.""",
        q_bn=r"""শনিবার রাত: তোমার Express login endpoint-এ হঠাৎ প্রতি মিনিটে প্রায় 40,000টি চেষ্টা আসছে, প্রায় 15,000টি ভিন্ন IP থেকে (residential proxy), অন্য একটি website থেকে ফাঁস হওয়া email/password জোড়া ব্যবহার করে। Per-IP rate limiting এটা থামাতে পারছে না, কয়েকটি account ইতিমধ্যে দখল হয়ে গেছে, আর database CPU 95%-এ। এখনই কীভাবে সাড়া দেবে আর পরে কী তৈরি করবে — ধাপে ধাপে বলো।""",
        a_en=r"""
            *(Advanced, senior-level answer.)* This is **credential stuffing**: valid-looking credentials spread across many IPs, so each IP stays under a per-IP limit.

            **Right now — contain and protect availability:**
            1. **Push the fight to the edge:** enable the CDN/WAF bot-management rules or a managed challenge on `/auth/login`; add an NGINX/WAF rule for the attack's fingerprints (user agent, ASN, header order). Cheap rejections at the edge protect the database.
            2. **Require a challenge for logins** temporarily (CAPTCHA/managed challenge for all or for risky ones), and cap login concurrency in the app so authentication can't starve the rest of the API (return `429`/`503` when full).
            3. **Stop the takeovers:** identify accounts with successful logins from attack sources (logs: IP, ASN, user agent, request IDs), revoke their sessions and refresh tokens, force password resets, and notify users. Turn on step-up verification (email OTP) for new devices.
            4. **Communicate:** incident channel, status updates, and security/legal involvement if accounts were compromised.

            **Afterwards — build layered defences:**
            - **Multi-dimensional limits** in Redis: per account across *all* IPs (failures/hour → CAPTCHA or progressive delay rather than hard lockout), per IP and IPv6 subnet, per ASN, plus a global failed-login-rate alarm.
            - **MFA / passkeys (WebAuthn)** — the most effective control against reused passwords; offer and encourage it, require it for admins.
            - **Breached-password checks** (e.g. k-anonymity range queries) at signup, login and password change.
            - **Cheaper, safer login path:** identical responses and similar timing for unknown users vs wrong passwords; strong password hashing (argon2id/bcrypt) with capacity planned for attack load.
            - **Detection:** dashboards and alerts on login failure ratio, new-device logins, logins per account, impossible travel.
        """,
        a_bn=r"""
            *(Advanced, senior-level উত্তর।)* এটা **credential stuffing**: দেখতে বৈধ credential অনেক IP-তে ছড়িয়ে পাঠানো হয়, ফলে প্রতিটি IP per-IP limit-এর নিচে থাকে।

            **এখনই — নিয়ন্ত্রণ আর availability রক্ষা:**
            1. **লড়াইটা edge-এ নিয়ে যাও:** `/auth/login`-এ CDN/WAF-এর bot-management rule বা managed challenge চালু করো; attack-এর fingerprint-এর (user agent, ASN, header order) জন্য NGINX/WAF rule যোগ করো। Edge-এ সস্তায় reject করলে database রক্ষা পায়।
            2. **সাময়িকভাবে login-এ challenge বাধ্যতামূলক করো** (সবার জন্য বা ঝুঁকিপূর্ণগুলোর জন্য CAPTCHA/managed challenge), আর app-এ login concurrency সীমিত করো, যাতে authentication বাকি API-কে বঞ্চিত না করে (ভরে গেলে `429`/`503`)।
            3. **দখল থামাও:** attack source থেকে সফল login হওয়া account খুঁজে বের করো (log: IP, ASN, user agent, request ID), তাদের session ও refresh token revoke করো, password reset বাধ্যতামূলক করো, আর user-দের জানাও। নতুন device-এর জন্য step-up verification (email OTP) চালু করো।
            4. **যোগাযোগ:** incident channel, status update, আর account compromise হলে security/legal-কে যুক্ত করা।

            **পরে — স্তরভিত্তিক প্রতিরক্ষা তৈরি:**
            - Redis-এ **বহুমাত্রিক limit:** *সব* IP মিলিয়ে account প্রতি (ঘণ্টায় failure → hard lockout নয়, CAPTCHA বা progressive delay), IP ও IPv6 subnet প্রতি, ASN প্রতি, সাথে global failed-login-rate alarm।
            - **MFA / passkey (WebAuthn)** — পুনর্ব্যবহৃত password-এর বিরুদ্ধে সবচেয়ে কার্যকর; চালু করো ও উৎসাহ দাও, admin-দের জন্য বাধ্যতামূলক।
            - **Breached-password check** (যেমন k-anonymity range query) signup, login আর password change-এর সময়।
            - **সস্তা ও নিরাপদ login path:** অজানা user আর ভুল password-এর জন্য হুবহু একই response ও কাছাকাছি সময়; attack load মাথায় রেখে capacity-সহ শক্ত password hashing (argon2id/bcrypt)।
            - **Detection:** login failure ratio, নতুন device-এ login, account প্রতি login, impossible travel-এর উপর dashboard আর alert।
        """,
        ex_en=r"""
            - **Why per-IP limits fail:** 40,000 attempts / 15,000 IPs ≈ 3 attempts per IP per minute — below any sane per-IP threshold. The useful dimensions are per account, per ASN/subnet and global failure ratios.
            - **Why the DB is at 95%:** every attempt does a user lookup plus an expensive password hash. Rejecting at the edge, caching "unknown email" lookups briefly, and capping concurrency protect shared resources; password hashing should run off the main thread (bcrypt/argon2 native bindings use the thread pool) so the API stays responsive.
            - **Lockout trade-off:** hard account lockouts let attackers lock out real users at scale; prefer progressive delays and challenges.
            - **Don't leak signals:** different messages or timing for "user not found" vs "wrong password" help attackers validate their lists.
            - **Post-incident:** write a blameless postmortem, add the attack's indicators to detection, and run a game day to test the playbook.
        """,
        ex_bn=r"""
            - **Per-IP limit কেন ব্যর্থ:** 40,000 চেষ্টা / 15,000 IP ≈ প্রতি IP-তে মিনিটে ৩টি চেষ্টা — যেকোনো যুক্তিসঙ্গত per-IP সীমার নিচে। কাজের মাত্রাগুলো হলো account প্রতি, ASN/subnet প্রতি আর global failure ratio।
            - **DB কেন 95%-এ:** প্রতিটি চেষ্টায় একটি user lookup আর একটি ব্যয়বহুল password hash হয়। Edge-এ reject করা, "অজানা email" lookup অল্প সময়ের জন্য cache করা, আর concurrency সীমিত করা shared resource রক্ষা করে; password hashing main thread-এর বাইরে চলা উচিত (bcrypt/argon2-এর native binding thread pool ব্যবহার করে), যাতে API responsive থাকে।
            - **Lockout-এর trade-off:** hard account lockout attacker-কে বড় পরিসরে আসল user-দের lock out করার সুযোগ দেয়; progressive delay আর challenge ভালো।
            - **Signal ফাঁস কোরো না:** "user নেই" আর "ভুল password"-এর জন্য আলাদা message বা সময় attacker-কে তার list যাচাই করতে সাহায্য করে।
            - **Incident-এর পরে:** blameless postmortem লেখো, attack-এর indicator detection-এ যোগ করো, আর playbook পরীক্ষার জন্য একটি game day চালাও।
        """,
        tip_en=r"""Split the answer into "next 30 minutes" and "next 30 days". Interviewers for senior roles want to see that you protect availability and users first, then fix root causes — and that you know per-IP limits can't stop distributed attacks.""",
        tip_bn=r"""উত্তর দুই ভাগে ভাগ করো: "পরের ৩০ মিনিট" আর "পরের ৩০ দিন"। Senior role-এর interviewer দেখতে চায় তুমি আগে availability আর user-দের রক্ষা করো, তারপর মূল কারণ ঠিক করো — এবং জানো যে per-IP limit distributed attack থামাতে পারে না।""",
        mist_en=r"""Only tightening the per-IP limit, permanently locking accounts after N failures (enables mass lockouts), or forgetting to revoke sessions of already-compromised accounts.""",
        mist_bn=r"""শুধু per-IP limit আরও কড়া করা, N বার ব্যর্থ হলে account চিরতরে lock করা (গণ-lockout সম্ভব করে), অথবা ইতিমধ্যে compromise হওয়া account-এর session revoke করতে ভুলে যাওয়া।""",
        code=r"""
            // Per-account failures across ALL IPs (stuffing spreads over many IPs)
            const accountLimiter = rateLimit({
              windowMs: 60 * 60 * 1000,
              limit: 20,                         // failed attempts per account per hour
              skipSuccessfulRequests: true,
              keyGenerator: (req) => `acct:${String(req.body?.email ?? '').trim().toLowerCase()}`,
              handler: (req, res) => res.status(429).json({ error: 'TOO_MANY_ATTEMPTS', captchaRequired: true }),
              standardHeaders: 'draft-8', legacyHeaders: false,
              store: new RedisStore({ prefix: 'rl:acct:', sendCommand: (...a) => redis.sendCommand(a) }),
            });

            // Per IP (IPv6 grouped by subnet by default)
            const ipLimiter = rateLimit({
              windowMs: 15 * 60 * 1000,
              limit: 50,
              standardHeaders: 'draft-8', legacyHeaders: false,
              store: new RedisStore({ prefix: 'rl:ip:', sendCommand: (...a) => redis.sendCommand(a) }),
            });

            app.post(
              '/auth/login',
              express.json({ limit: '2kb' }),
              ipLimiter,
              accountLimiter,
              requireChallengeIfRisky,  // CAPTCHA / managed challenge based on risk signals
              loginHandler,             // same response + similar timing for unknown user vs wrong password
            );
        """,
        lang="javascript",
        follow=[
            ("How would you detect credential stuffing automatically before customers report takeovers?", "Customer-রা দখলের অভিযোগ করার আগেই credential stuffing স্বয়ংক্রিয়ভাবে কীভাবে ধরবে?"),
            ("Why are passkeys/WebAuthn resistant to this attack?", "Passkey/WebAuthn কেন এই attack-এর বিরুদ্ধে প্রতিরোধী?"),
            ("How do you keep password hashing from overloading the API during an attack?", "Attack চলাকালীন password hashing যেন API-কে overload না করে, কীভাবে নিশ্চিত করবে?"),
        ],
        related=["express-018", "express-019"],
        refs=[OWASP_STUFFING, OWASP_AUTH, ERL_GITHUB],
    ),
]

if __name__ == "__main__":
    save("express", "b3", QUESTIONS)
