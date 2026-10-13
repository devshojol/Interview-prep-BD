import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

HELMET = ("helmet (GitHub)", "https://github.com/helmetjs/helmet")
EX_SECURITY = ("Express — Production best practices: security", "https://expressjs.com/en/advanced/best-practice-security.html")
OWASP_AUTHZ = ("OWASP — Authorization Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html")
MDN_401 = ("MDN — 401 Unauthorized", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401")
MDN_403 = ("MDN — 403 Forbidden", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/403")
JWT_LIB = ("jsonwebtoken (GitHub)", "https://github.com/auth0/node-jsonwebtoken")
OWASP_JWT = ("OWASP — JSON Web Token Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html")
RFC_6750 = ("RFC 6750 — OAuth 2.0 Bearer Token Usage", "https://www.rfc-editor.org/rfc/rfc6750")
EX_SESSION = ("Express — express-session middleware", "https://expressjs.com/en/resources/middleware/session.html")
OWASP_SESSION = ("OWASP — Session Management Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html")
EX_PERF = ("Express — Production best practices: performance and reliability", "https://expressjs.com/en/advanced/best-practice-performance.html")
PINO_HTTP = ("pino-http (GitHub)", "https://github.com/pinojs/pino-http")
NODE_PG_POOL = ("node-postgres (GitHub)", "https://github.com/brianc/node-postgres")
NODE_TEST = ("Node.js API — Test runner", "https://nodejs.org/api/test.html")
SUPERTEST = ("supertest (GitHub)", "https://github.com/forwardemail/supertest")

QUESTIONS = [
    # ------------------------------------------------------------------ express-021
    Q(
        id="express-021", sub="Security Headers (helmet)", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=2,
        tags=["helmet", "security-headers", "csp", "hsts"],
        ver="Express 5.x; helmet 8.x", vs=True, status="stable",
        q_en=r"""What does adding `app.use(helmet())` to an Express app actually do?""",
        q_bn=r"""Express app-এ `app.use(helmet())` যোগ করলে আসলে কী হয়?""",
        options=[
            ("It validates and sanitises request bodies to prevent SQL injection and XSS", "এটা request body validate ও sanitise করে SQL injection আর XSS আটকায়"),
            ("It sets a group of security-related response headers (e.g. `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`) and removes `X-Powered-By`", "এটা কিছু security-সংক্রান্ত response header set করে (যেমন `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`) এবং `X-Powered-By` সরিয়ে দেয়"),
            ("It encrypts cookies and turns on HTTPS automatically", "এটা cookie encrypt করে এবং স্বয়ংক্রিয়ভাবে HTTPS চালু করে"),
            ("It rate-limits requests per IP to block brute-force attacks", "এটা IP প্রতি request rate-limit করে brute-force attack আটকায়"),
        ],
        correct=1,
        a_en=r"""
            It sets security-related HTTP **response headers**. Helmet 8's defaults include a baseline `Content-Security-Policy`, `Strict-Transport-Security` (one year, `includeSubDomains`), `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: no-referrer`, cross-origin isolation headers, `X-XSS-Protection: 0`, and it removes `X-Powered-By`.
        """,
        a_bn=r"""
            এটা security-সংক্রান্ত HTTP **response header** set করে। Helmet 8-এর default-এ আছে একটি baseline `Content-Security-Policy`, `Strict-Transport-Security` (এক বছর, `includeSubDomains`), `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: no-referrer`, cross-origin isolation header, `X-XSS-Protection: 0`, আর এটা `X-Powered-By` সরিয়ে দেয়।
        """,
        ex_en=r"""
            Option A is the common misconception: helmet does **nothing** to your input. You still need schema validation, parameterised queries and output encoding. It also doesn't rate-limit (that's `express-rate-limit`) or enable HTTPS (TLS is terminated by NGINX/the load balancer; HSTS only tells browsers to keep using HTTPS).

            Practical notes:
            - The default CSP matters most for HTML pages; if you serve an SPA that loads scripts from a CDN, you must customise `contentSecurityPolicy.directives`.
            - `X-XSS-Protection: 0` is intentional — the old browser XSS filter caused vulnerabilities, so helmet disables it.
            - Headers are defence in depth: they reduce the impact of bugs (clickjacking, MIME sniffing, some XSS), they don't fix them.
            - Verified with helmet 8.3 on Express 5.3: the response had all the headers above and no `X-Powered-By`.
        """,
        ex_bn=r"""
            Option A হলো প্রচলিত ভুল ধারণা: helmet তোমার input-এর জন্য **কিছুই** করে না। Schema validation, parameterised query আর output encoding তবুও লাগবে। এটা rate-limit-ও করে না (সেটা `express-rate-limit`-এর কাজ), HTTPS-ও চালু করে না (TLS terminate করে NGINX/load balancer; HSTS শুধু browser-কে HTTPS ব্যবহার চালিয়ে যেতে বলে)।

            বাস্তব নোট:
            - Default CSP সবচেয়ে বেশি গুরুত্বপূর্ণ HTML page-এর জন্য; CDN থেকে script load করা SPA serve করলে `contentSecurityPolicy.directives` customise করতে হবে।
            - `X-XSS-Protection: 0` ইচ্ছাকৃত — পুরনো browser XSS filter নিজেই vulnerability তৈরি করত, তাই helmet এটা বন্ধ করে।
            - Header হলো defence in depth: এগুলো bug-এর প্রভাব কমায় (clickjacking, MIME sniffing, কিছু XSS), bug ঠিক করে না।
            - Express 5.3-এ helmet 8.3 দিয়ে যাচাই করা: response-এ উপরের সব header ছিল এবং `X-Powered-By` ছিল না।
        """,
        tip_en=r"""Name two or three concrete headers and what each prevents (CSP → XSS impact, HSTS → downgrade, nosniff → MIME sniffing). Then say clearly what helmet does *not* do.""",
        tip_bn=r"""দুই-তিনটি নির্দিষ্ট header-এর নাম বলো এবং প্রতিটি কী আটকায় (CSP → XSS-এর প্রভাব, HSTS → downgrade, nosniff → MIME sniffing)। তারপর স্পষ্ট বলো helmet কী *করে না*।""",
        refs=[HELMET, EX_SECURITY],
    ),
    # ------------------------------------------------------------------ express-022
    Q(
        id="express-022", sub="Authorization", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["authentication", "authorization", "401-vs-403", "idor", "bola"],
        ver="Version-independent; Express 5.x example", vs=False, status="stable",
        q_en=r"""What is the difference between authentication and authorization in an Express API? Where does each happen, and which status codes do you return when they fail?""",
        q_bn=r"""Express API-তে authentication আর authorization-এর পার্থক্য কী? প্রতিটি কোথায় ঘটে, আর fail করলে কোন status code return করো?""",
        a_en=r"""
            - **Authentication — "who are you?"** Verify a credential (session cookie, JWT, API key) and attach the identity to `req.user`. It runs as middleware early in the chain for protected routes. Failure → **`401 Unauthorized`** (despite the name, it means "not authenticated"), usually with a `WWW-Authenticate` header for bearer tokens.
            - **Authorization — "what are you allowed to do?"** Check the identity against the action and the specific resource. Failure → **`403 Forbidden`** (or `404` when you don't want to reveal that the resource exists).

            Authorization happens at two levels:
            - **Route level:** role or permission middleware, e.g. `requireRole('admin')` for admin endpoints.
            - **Object level:** in the handler or service — does *this* order belong to *this* user (and tenant)? Skipping this check is the classic IDOR / BOLA bug: a logged-in user changes `/orders/123` to `/orders/124` and sees someone else's data.
        """,
        a_bn=r"""
            - **Authentication — "তুমি কে?"** একটি credential (session cookie, JWT, API key) যাচাই করে identity `req.user`-এ যুক্ত করা। Protected route-এর জন্য chain-এর শুরুর দিকে middleware হিসেবে চলে। Fail হলে → **`401 Unauthorized`** (নামের বিপরীতে, এর মানে "authenticated নয়"), bearer token-এর ক্ষেত্রে সাধারণত `WWW-Authenticate` header সহ।
            - **Authorization — "তুমি কী করতে পারো?"** Identity-কে action আর নির্দিষ্ট resource-এর সাথে মিলিয়ে দেখা। Fail হলে → **`403 Forbidden`** (অথবা resource-টি আছে কি না জানাতে না চাইলে `404`)।

            Authorization দুই স্তরে হয়:
            - **Route level:** role বা permission middleware, যেমন admin endpoint-এর জন্য `requireRole('admin')`।
            - **Object level:** handler বা service-এ — *এই* order কি *এই* user-এর (আর tenant-এর)? এই check বাদ দেওয়াই classic IDOR / BOLA bug: একজন logged-in user `/orders/123` বদলে `/orders/124` করে অন্যের data দেখে ফেলে।
        """,
        ex_en=r"""
            - **Why object-level checks are easy to miss:** role middleware passes (the user *is* a customer), the route works in testing with your own IDs, and nothing fails visibly. It's #1 in the OWASP API Security Top 10 for a reason.
            - **Best practice:** scope the query itself — `orders.findOne({ id, userId: req.user.id })` — so you can't forget a separate `if`.
            - **401 vs 403 in practice:** an expired token is `401` (the client should refresh or log in again); a valid token without permission is `403` (logging in again won't help).
            - **Centralise policies** (e.g. a `can(user, action, resource)` helper) instead of scattering `if (user.role === 'admin')` across handlers.
            - **Never trust identity fields from the body** (`userId` in JSON) — take them from `req.user`.
        """,
        ex_bn=r"""
            - **Object-level check কেন সহজে বাদ পড়ে:** role middleware pass করে (user সত্যিই customer), নিজের ID দিয়ে test করলে route ঠিকঠাক কাজ করে, আর চোখে পড়ার মতো কিছু fail করে না। এজন্যই এটা OWASP API Security Top 10-এর #1।
            - **Best practice:** query-টাকেই scope করো — `orders.findOne({ id, userId: req.user.id })` — যাতে আলাদা `if` লিখতে ভুলে যাওয়ার সুযোগ না থাকে।
            - **বাস্তবে 401 বনাম 403:** expired token হলে `401` (client-এর refresh বা আবার login করা উচিত); valid token কিন্তু অনুমতি নেই হলে `403` (আবার login করে লাভ নেই)।
            - **Policy কেন্দ্রীভূত করো** (যেমন একটি `can(user, action, resource)` helper), handler-জুড়ে `if (user.role === 'admin')` ছড়িয়ে না দিয়ে।
            - **Body থেকে আসা identity field কখনো বিশ্বাস কোরো না** (JSON-এর `userId`) — সেগুলো `req.user` থেকে নাও।
        """,
        tip_en=r"""Give the one-line definitions, the status codes, and then immediately bring up object-level authorization (IDOR). That jump from textbook to real vulnerability is what makes the answer stand out.""",
        tip_bn=r"""এক লাইনের definition, status code, তারপর সাথে সাথে object-level authorization (IDOR)-এর প্রসঙ্গ তোলো। Textbook থেকে বাস্তব vulnerability-তে এই লাফটাই উত্তরকে আলাদা করে।""",
        mist_en=r"""Returning `403` for a missing token (should be `401`), or thinking role checks alone are enough authorization.""",
        mist_bn=r"""Token না থাকলে `403` return করা (হওয়া উচিত `401`), অথবা শুধু role check-কেই যথেষ্ট authorization মনে করা।""",
        code=r"""
            // Route-level authorization: role check
            app.delete('/admin/users/:id', authenticate, requireRole('admin'), deleteUser);

            // Object-level authorization: scope the query to the current user
            app.get('/orders/:id', authenticate, async (req, res) => {
              const order = await orders.findOne({ id: req.params.id, userId: req.user.id });
              if (!order) throw AppError.notFound('Order'); // 404: don't reveal other users' orders
              res.json(order);
            });
        """,
        lang="javascript",
        follow=[
            ("When would you return 404 instead of 403 for an unauthorized resource?", "অননুমোদিত resource-এর জন্য কখন 403-এর বদলে 404 return করবে?"),
            ("How would you test for IDOR vulnerabilities automatically?", "IDOR vulnerability স্বয়ংক্রিয়ভাবে কীভাবে test করবে?"),
        ],
        related=["express-023", "express-009"],
        refs=[OWASP_AUTHZ, MDN_401, MDN_403],
    ),
    # ------------------------------------------------------------------ express-023
    Q(
        id="express-023", sub="Authentication", diff="medium", type="coding",
        prio="high", market="bangladesh", mins=8,
        tags=["jwt", "auth-middleware", "rbac", "jsonwebtoken", "coding"],
        ver="Express 5.x; jsonwebtoken 9.x", vs=False, status="stable",
        q_en=r"""
            Write two Express 5 middlewares:

            - `authenticate` — reads a `Bearer` JWT from the `Authorization` header, verifies it (HS256, issuer `api.example.com`, audience `app.example.com`) and sets `req.user = { id, role }`. Respond `401` with a `WWW-Authenticate` header for missing, invalid or expired tokens (use error code `TOKEN_EXPIRED` for expired ones).
            - `requireRole(...roles)` — lets the request through only if `req.user.role` is one of `roles`, otherwise `403`.

            Usage: `app.delete('/admin/users/:id', authenticate, requireRole('admin'), handler)`.
        """,
        q_bn=r"""
            দুটি Express 5 middleware লেখো:

            - `authenticate` — `Authorization` header থেকে `Bearer` JWT পড়বে, verify করবে (HS256, issuer `api.example.com`, audience `app.example.com`) এবং `req.user = { id, role }` set করবে। Token না থাকলে, invalid বা expired হলে `WWW-Authenticate` header সহ `401` দেবে (expired-এর জন্য error code `TOKEN_EXPIRED`)।
            - `requireRole(...roles)` — `req.user.role` যদি `roles`-এর একটি হয় তবেই request যেতে দেবে, নইলে `403`।

            ব্যবহার: `app.delete('/admin/users/:id', authenticate, requireRole('admin'), handler)`।
        """,
        a_en=r"""
            `authenticate` parses the header, rejects anything that isn't `Bearer <token>`, and calls `jwt.verify` with **pinned options**: `algorithms: ['HS256']`, `issuer` and `audience`. If verification throws, it maps `TokenExpiredError` to `TOKEN_EXPIRED` and everything else to `INVALID_TOKEN`, sets `WWW-Authenticate`, and returns `401`. On success it copies only the claims it needs to `req.user` and calls `next()` — **outside** the `try` block, so an error in a later middleware is never misreported as an invalid token.

            `requireRole` is a factory: it captures the allowed roles in a `Set` and returns middleware that answers `401` if `req.user` is missing (a misconfigured route), `403` if the role isn't allowed, and otherwise calls `next()`.
        """,
        a_bn=r"""
            `authenticate` header parse করে, `Bearer <token>` ছাড়া অন্য কিছু হলে reject করে, এবং **pin করা option** দিয়ে `jwt.verify` call করে: `algorithms: ['HS256']`, `issuer` আর `audience`। Verification throw করলে `TokenExpiredError`-কে `TOKEN_EXPIRED` আর বাকি সবকিছুকে `INVALID_TOKEN`-এ map করে, `WWW-Authenticate` set করে এবং `401` return করে। সফল হলে শুধু দরকারি claim `req.user`-এ কপি করে `next()` call করে — `try` block-এর **বাইরে**, যাতে পরের কোনো middleware-এর error কখনো invalid token হিসেবে ভুলভাবে রিপোর্ট না হয়।

            `requireRole` একটি factory: এটা অনুমোদিত role-গুলো একটি `Set`-এ ধরে রাখে এবং এমন middleware return করে যা `req.user` না থাকলে (ভুলভাবে configure করা route) `401`, role অনুমোদিত না হলে `403`, আর অন্যথায় `next()` call করে।
        """,
        ex_en=r"""
            - **Pin the algorithm:** without `algorithms`, a library could accept tokens signed with an unexpected algorithm (the historic `alg: none` and RS/HS confusion attacks). Verified: an `alg: none` token is rejected with `401`.
            - **Check `iss`/`aud`:** a token minted for another service with the same secret shouldn't work here (verified: wrong audience → `401`).
            - **Secrets:** a long random `JWT_SECRET` from the environment/secrets manager; consider asymmetric keys (RS256/EdDSA) when other services must verify but not issue tokens.
            - **Keep claims small and non-sensitive** — JWT payloads are only base64url-encoded, not encrypted.
            - **Roles in tokens go stale** until the token expires; that's another reason for short access-token lifetimes.
            - Verified with supertest on Express 5.3 + jsonwebtoken 9: no token → 401, garbage → 401 `INVALID_TOKEN`, expired → 401 `TOKEN_EXPIRED`, customer → 403, admin → 204.
        """,
        ex_bn=r"""
            - **Algorithm pin করো:** `algorithms` না দিলে library অপ্রত্যাশিত algorithm-এ signed token গ্রহণ করতে পারে (ঐতিহাসিক `alg: none` আর RS/HS confusion attack)। যাচাই করা: `alg: none` token `401` দিয়ে reject হয়।
            - **`iss`/`aud` check করো:** একই secret দিয়ে অন্য service-এর জন্য বানানো token এখানে কাজ করা উচিত নয় (যাচাই করা: ভুল audience → `401`)।
            - **Secret:** environment/secrets manager থেকে আসা লম্বা random `JWT_SECRET`; অন্য service-কে শুধু verify করতে দিতে হলে (issue নয়) asymmetric key (RS256/EdDSA) বিবেচনা করো।
            - **Claim ছোট ও অ-সংবেদনশীল রাখো** — JWT payload শুধু base64url-encoded, encrypted নয়।
            - **Token-এর role পুরনো হয়ে যায়** token expire না হওয়া পর্যন্ত; access token-এর আয়ু ছোট রাখার এটাও একটা কারণ।
            - Express 5.3 + jsonwebtoken 9-এ supertest দিয়ে যাচাই করা: token নেই → 401, আবর্জনা → 401 `INVALID_TOKEN`, expired → 401 `TOKEN_EXPIRED`, customer → 403, admin → 204।
        """,
        tip_en=r"""While coding, say out loud *why* you pin `algorithms`, check `aud`, and call `next()` outside the `try`. Those three justifications are what turn a common exercise into a senior-sounding answer.""",
        tip_bn=r"""Code লেখার সময় মুখে বলো *কেন* `algorithms` pin করছ, `aud` check করছ, আর `try`-এর বাইরে `next()` call করছ। এই তিনটি যুক্তিই একটি সাধারণ exercise-কে senior-মানের উত্তরে পরিণত করে।""",
        mist_en=r"""Using `jwt.decode()` instead of `jwt.verify()` (no signature check), not pinning algorithms, or returning `403` for an expired token.""",
        mist_bn=r"""`jwt.verify()`-এর বদলে `jwt.decode()` ব্যবহার করা (signature check হয় না), algorithm pin না করা, অথবা expired token-এর জন্য `403` return করা।""",
        code=r"""
            import jwt from 'jsonwebtoken';

            const JWT_OPTIONS = { algorithms: ['HS256'], issuer: 'api.example.com', audience: 'app.example.com' };

            export function authenticate(req, res, next) {
              const [scheme, token] = (req.get('authorization') ?? '').split(' ');
              if (scheme !== 'Bearer' || !token) {
                res.set('WWW-Authenticate', 'Bearer');
                return res.status(401).json({ error: 'UNAUTHENTICATED' });
              }

              let payload;
              try {
                payload = jwt.verify(token, process.env.JWT_SECRET, JWT_OPTIONS); // pin the algorithm!
              } catch (err) {
                const code = err.name === 'TokenExpiredError' ? 'TOKEN_EXPIRED' : 'INVALID_TOKEN';
                res.set('WWW-Authenticate', 'Bearer error="invalid_token"');
                return res.status(401).json({ error: code });
              }

              req.user = { id: payload.sub, role: payload.role };
              next(); // outside the try: later errors aren't misreported as "invalid token"
            }

            export function requireRole(...roles) {
              const allowed = new Set(roles);
              return (req, res, next) => {
                if (!req.user) return res.status(401).json({ error: 'UNAUTHENTICATED' }); // authenticate missing
                if (!allowed.has(req.user.role)) return res.status(403).json({ error: 'FORBIDDEN' });
                next();
              };
            }

            // app.delete('/admin/users/:id', authenticate, requireRole('admin'), deleteUser);
        """,
        lang="javascript",
        time="O(1) per request (plus signature verification)", space="O(1)",
        follow=[
            ("How would you support permission-based checks (e.g. `orders:refund`) instead of roles?", "Role-এর বদলে permission-ভিত্তিক check (যেমন `orders:refund`) কীভাবে support করবে?"),
            ("How would you verify tokens issued by an external identity provider (OIDC)?", "External identity provider (OIDC)-এর issue করা token কীভাবে verify করবে?"),
        ],
        related=["express-022", "express-019", "express-024"],
        refs=[JWT_LIB, OWASP_JWT, RFC_6750],
    ),
    # ------------------------------------------------------------------ express-024
    Q(
        id="express-024", sub="Cookies & Sessions", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["sessions", "jwt", "express-session", "redis", "authentication"],
        ver="Express 5.x; express-session 1.x; connect-redis (example)", vs=False, status="stable",
        q_en=r"""Compare server-side sessions (cookie + session store) with stateless JWTs for authenticating users of an Express web app. Which would you choose for a typical web app, and when would you pick the other?""",
        q_bn=r"""Express web app-এর user authenticate করার জন্য server-side session (cookie + session store) আর stateless JWT-এর তুলনা করো। সাধারণ একটি web app-এর জন্য কোনটা বেছে নেবে, আর কখন অন্যটা?""",
        a_en=r"""
            **Server-side sessions:** the browser holds an opaque, random session ID in an `httpOnly` cookie; the server looks the session up in a store (Redis) on each request.
            - Pros: instant revocation (delete the session), small cookie, no sensitive data on the client, roles/permissions always fresh.
            - Cons: a lookup per request and a shared store for multiple instances; cookies are sent automatically, so you need CSRF protection (SameSite + token).

            **Stateless JWTs:** a signed token carries the claims; any service with the key verifies it without a lookup.
            - Pros: no shared session store, works well across many services, mobile clients and third-party APIs; easy to verify at a gateway.
            - Cons: hard to revoke before expiry (you add short lifetimes + refresh tokens or a deny-list — reintroducing state), claims go stale, bigger tokens, key management, and a storage dilemma in browsers (memory/`localStorage` vs cookies).

            **My default for a first-party web app with one backend: sessions** in Redis with secure cookies — simpler and safer. I choose JWTs when several services or native mobile apps must verify identity independently, or when tokens come from an identity provider (OAuth 2.0 / OpenID Connect).
        """,
        a_bn=r"""
            **Server-side session:** browser একটি `httpOnly` cookie-তে opaque, random session ID রাখে; server প্রতিটি request-এ store (Redis) থেকে session খোঁজে।
            - সুবিধা: তাৎক্ষণিক revocation (session মুছে দাও), ছোট cookie, client-এ কোনো sensitive data নেই, role/permission সবসময় হালনাগাদ।
            - অসুবিধা: প্রতি request-এ একটি lookup আর একাধিক instance-এর জন্য shared store; cookie স্বয়ংক্রিয়ভাবে যায়, তাই CSRF সুরক্ষা লাগে (SameSite + token)।

            **Stateless JWT:** একটি signed token claim বহন করে; key থাকা যেকোনো service lookup ছাড়াই verify করতে পারে।
            - সুবিধা: shared session store লাগে না, অনেক service, mobile client আর third-party API-জুড়ে ভালো কাজ করে; gateway-তে সহজে verify করা যায়।
            - অসুবিধা: expiry-র আগে revoke করা কঠিন (ছোট আয়ু + refresh token বা deny-list যোগ করতে হয় — যা আবার state ফিরিয়ে আনে), claim পুরনো হয়ে যায়, token বড়, key management, আর browser-এ রাখার দ্বিধা (memory/`localStorage` বনাম cookie)।

            **একটি backend-ওয়ালা first-party web app-এর জন্য আমার default: session**, Redis-এ, secure cookie সহ — সহজ ও নিরাপদ। JWT বেছে নিই যখন একাধিক service বা native mobile app-কে নিজে নিজে identity verify করতে হয়, অথবা token আসে কোনো identity provider (OAuth 2.0 / OpenID Connect) থেকে।
        """,
        ex_en=r"""
            - **"Stateless" is rarely fully stateless:** as soon as you need logout-everywhere, bans or refresh-token rotation, you store state again. Be honest about that trade-off in interviews.
            - **Performance:** a Redis session lookup is typically sub-millisecond; it's rarely the bottleneck people fear.
            - **Scaling sessions:** use a shared store (`connect-redis`) — the default `MemoryStore` leaks memory and isn't shared between instances, and the express-session docs say it's not meant for production.
            - **Behind a proxy:** with `cookie.secure: true`, set `app.set('trust proxy', 1)`, or express-session won't send the cookie over what it thinks is plain HTTP.
            - **Hybrid is common:** sessions for the browser app, JWT/OAuth access tokens for mobile apps and service-to-service calls.
        """,
        ex_bn=r"""
            - **"Stateless" খুব কমই পুরোপুরি stateless:** সব জায়গা থেকে logout, ban বা refresh-token rotation লাগলেই আবার state রাখতে হয়। Interview-তে এই trade-off নিয়ে সৎ থাকো।
            - **Performance:** Redis-এ session lookup সাধারণত এক millisecond-এর কম; মানুষ যতটা ভয় পায় ততটা bottleneck এটা খুব কমই হয়।
            - **Session scale করা:** shared store (`connect-redis`) ব্যবহার করো — default `MemoryStore` memory leak করে, instance-এর মধ্যে share হয় না, আর express-session-এর docs বলে এটা production-এর জন্য নয়।
            - **Proxy-র পেছনে:** `cookie.secure: true` দিলে `app.set('trust proxy', 1)` দাও, নইলে express-session যেটাকে সাধারণ HTTP মনে করে সেখানে cookie পাঠায় না।
            - **Hybrid প্রচলিত:** browser app-এর জন্য session, mobile app আর service-to-service call-এর জন্য JWT/OAuth access token।
        """,
        tip_en=r"""Don't present JWT as "modern" and sessions as "old". Compare them on revocation, state, CSRF/XSS exposure and multi-service needs, then make a clear recommendation with conditions — that's what interviewers want.""",
        tip_bn=r"""JWT-কে "আধুনিক" আর session-কে "পুরনো" হিসেবে উপস্থাপন কোরো না। Revocation, state, CSRF/XSS ঝুঁকি আর multi-service প্রয়োজনের ভিত্তিতে তুলনা করো, তারপর শর্তসহ স্পষ্ট সুপারিশ দাও — interviewer এটাই চায়।""",
        mist_en=r"""Claiming JWTs are "more secure", storing JWTs in `localStorage` by default, or using express-session's `MemoryStore` in production.""",
        mist_bn=r"""JWT-কে "বেশি নিরাপদ" দাবি করা, default-ভাবে `localStorage`-এ JWT রাখা, অথবা production-এ express-session-এর `MemoryStore` ব্যবহার করা।""",
        code=r"""
            import session from 'express-session';
            import { RedisStore } from 'connect-redis';
            import { createClient } from 'redis';

            const redis = await createClient({ url: process.env.REDIS_URL }).connect();

            app.set('trust proxy', 1); // behind NGINX/ALB: needed for secure cookies
            app.use(session({
              store: new RedisStore({ client: redis, prefix: 'sess:' }),
              secret: process.env.SESSION_SECRET,
              name: 'sid',
              resave: false,
              saveUninitialized: false,
              cookie: { httpOnly: true, secure: true, sameSite: 'lax', maxAge: 8 * 60 * 60 * 1000 },
            }));

            app.post('/auth/login', async (req, res, next) => {
              const user = await verifyCredentials(req.body.email, req.body.password);
              req.session.regenerate((err) => {          // prevent session fixation
                if (err) return next(err);
                req.session.userId = user.id;
                res.sendStatus(204);
              });
            });
        """,
        lang="javascript",
        follow=[
            ("How do you implement 'log out from all devices' with each approach?", "প্রতিটি পদ্ধতিতে 'সব device থেকে logout' কীভাবে implement করবে?"),
            ("How does CSRF risk differ between cookie sessions and bearer tokens?", "Cookie session আর bearer token-এর মধ্যে CSRF ঝুঁকি কীভাবে আলাদা?"),
        ],
        related=["express-016", "express-019", "express-023"],
        refs=[EX_SESSION, OWASP_SESSION, OWASP_JWT],
    ),
    # ------------------------------------------------------------------ express-025
    Q(
        id="express-025", sub="Production Debugging", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["production-debugging", "504", "connection-pool", "timeouts", "observability"],
        ver="Express 5.x; node-postgres (pg) 8.x", vs=False, status="stable",
        q_en=r"""After a release, a growing share of requests to your Express API hang until NGINX returns `504 Gateway Timeout` after 60 seconds. Restarting the instances fixes it for a few hours. CPU and memory look normal, and there are no error logs for the hanging requests. How do you find and fix the cause?""",
        q_bn=r"""একটি release-এর পর তোমার Express API-র ক্রমবর্ধমান অংশের request ৬০ সেকেন্ড ঝুলে থাকে, তারপর NGINX `504 Gateway Timeout` দেয়। Instance restart করলে কয়েক ঘণ্টার জন্য ঠিক হয়ে যায়। CPU আর memory স্বাভাবিক, আর ঝুলে থাকা request-গুলোর কোনো error log নেই। কারণ কীভাবে খুঁজবে আর ঠিক করবে?""",
        a_en=r"""
            **Reading the symptoms:** normal CPU rules out event-loop blocking; "gets worse over time, restart fixes it" points to a **leaked, finite resource**; hanging without errors means requests are *waiting* for something. The prime suspect is the **database connection pool**.

            My approach:
            1. **Scope it:** which routes and instances? Compare NGINX access logs (`$upstream_response_time`, status 504) with app logs using the request ID that NGINX forwards. Requests that log "started" but never "completed" show where they're stuck.
            2. **Check pool metrics:** node-postgres exposes `pool.totalCount`, `idleCount` and `waitingCount`. If `idleCount` is 0 and `waitingCount` keeps growing, connections are being checked out and never returned. In PostgreSQL, `pg_stat_activity` showing sessions `idle in transaction` confirms it.
            3. **Diff the release:** look for code that calls `pool.connect()` and releases the client only on the happy path — any thrown error skips `client.release()` and leaks a connection. After `max` (10 by default) failures, every request waits forever, because `connectionTimeoutMillis` defaults to 0 (no timeout).
            4. **Fix:** release in `finally` (with `ROLLBACK` in `catch`), or use a transaction helper / `pool.query()` for single queries.
            5. **Make it fail fast next time:** `connectionTimeoutMillis`, `statement_timeout` and `idle_in_transaction_session_timeout`; `AbortSignal.timeout()` on outbound HTTP calls; alerts on pool `waitingCount` and on the share of slow requests.
        """,
        a_bn=r"""
            **Symptom পড়া:** CPU স্বাভাবিক মানে event loop block নয়; "সময়ের সাথে খারাপ হয়, restart করলে ঠিক" মানে কোনো **leak হওয়া সীমিত resource**; error ছাড়াই ঝুলে থাকা মানে request কোনো কিছুর জন্য *অপেক্ষা* করছে। প্রধান সন্দেহভাজন **database connection pool**।

            আমার approach:
            1. **পরিধি ঠিক করা:** কোন route আর কোন instance? NGINX-এর forward করা request ID দিয়ে NGINX access log (`$upstream_response_time`, status 504) আর app log মেলাই। যে request "started" log করেছে কিন্তু কখনো "completed" নয়, সেগুলো দেখায় কোথায় আটকে আছে।
            2. **Pool metric দেখা:** node-postgres `pool.totalCount`, `idleCount` আর `waitingCount` দেয়। `idleCount` 0 আর `waitingCount` বাড়তেই থাকলে connection checkout হচ্ছে কিন্তু ফেরত আসছে না। PostgreSQL-এ `pg_stat_activity`-তে `idle in transaction` session দেখা গেলে নিশ্চিত।
            3. **Release-এর diff দেখা:** এমন code খুঁজি যা `pool.connect()` call করে কিন্তু শুধু সফল পথে `client.release()` করে — কোনো error throw হলেই release বাদ পড়ে এবং একটি connection leak হয়। `max` (default 10)টি failure-এর পর প্রতিটি request চিরকাল অপেক্ষা করে, কারণ `connectionTimeoutMillis`-এর default 0 (কোনো timeout নেই)।
            4. **Fix:** `finally`-তে release (`catch`-এ `ROLLBACK` সহ), অথবা transaction helper / একক query-র জন্য `pool.query()` ব্যবহার।
            5. **পরেরবার যেন দ্রুত fail করে:** `connectionTimeoutMillis`, `statement_timeout` আর `idle_in_transaction_session_timeout`; outbound HTTP call-এ `AbortSignal.timeout()`; pool `waitingCount` আর ধীর request-এর অনুপাতের উপর alert।
        """,
        ex_en=r"""
            **Other causes with the same "hang, no errors" signature:**
            - a middleware branch that neither responds nor calls `next()`;
            - outbound HTTP calls to a slow dependency without a timeout;
            - a promise that never settles (a callback API wrapped incorrectly);
            - database row locks held by a long transaction, so other queries wait.

            **Why there are no error logs:** nothing has failed yet — requests are queued. That's why logging both *start* and *finish* (e.g. pino-http with request IDs, plus a log or metric for requests aborted by the client) and alerting on latency, not just errors, matters.

            **Why 504 and not 500:** NGINX gave up after `proxy_read_timeout` (60 s by default). Setting app-side timeouts *below* the proxy's lets the app return a clear `503` and log it, instead of the proxy cutting the connection.

            **Verification:** reproduce in staging by forcing the failing path ~10 times, watch `waitingCount` climb, deploy the fix, and confirm it stays flat under the same test.
        """,
        ex_bn=r"""
            **একই "ঝুলে থাকে, error নেই" লক্ষণের অন্যান্য কারণ:**
            - এমন middleware branch যা response-ও দেয় না, `next()`-ও call করে না;
            - timeout ছাড়া ধীর কোনো dependency-তে outbound HTTP call;
            - এমন promise যা কখনো settle হয় না (ভুলভাবে wrap করা callback API);
            - লম্বা transaction-এর ধরে রাখা database row lock, ফলে অন্য query অপেক্ষা করে।

            **কেন কোনো error log নেই:** এখনো কিছুই fail করেনি — request-গুলো queue-তে আছে। এজন্যই *শুরু* আর *শেষ* দুটোই log করা (যেমন request ID সহ pino-http, সাথে client-এর abort করা request-এর log বা metric) এবং শুধু error নয়, latency-র উপরও alert রাখা জরুরি।

            **500 না হয়ে 504 কেন:** NGINX `proxy_read_timeout`-এর (default 60 s) পর হাল ছেড়ে দিয়েছে। App-এর timeout proxy-র চেয়ে *কম* রাখলে proxy connection কেটে দেওয়ার আগেই app একটি স্পষ্ট `503` দিয়ে log করতে পারে।

            **যাচাই:** staging-এ ব্যর্থ path প্রায় ১০ বার চালিয়ে reproduce করো, `waitingCount` বাড়তে দেখো, fix deploy করো, আর একই test-এ এটা স্থির থাকছে কি না নিশ্চিত করো।
        """,
        tip_en=r"""Reason from the symptoms out loud ("normal CPU → not blocking; restart fixes → leak; no errors → waiting"). Interviewers care more about this diagnostic reasoning than about guessing the exact bug.""",
        tip_bn=r"""Symptom থেকে মুখে মুখে যুক্তি দাও ("CPU স্বাভাবিক → blocking নয়; restart করলে ঠিক → leak; error নেই → অপেক্ষা")। Interviewer সঠিক bug আন্দাজ করার চেয়ে এই diagnostic যুক্তিকে বেশি গুরুত্ব দেয়।""",
        mist_en=r"""Increasing NGINX's timeout or the pool size (the leak just takes longer), or scheduling automatic restarts as the "fix".""",
        mist_bn=r"""NGINX-এর timeout বা pool size বাড়ানো (leak শুধু একটু দেরিতে ধরা দেয়), অথবা স্বয়ংক্রিয় restart-কেই "fix" হিসেবে চালু করা।""",
        code=r"""
            // Code added in the latest release
            app.post('/orders', async (req, res) => {
              const client = await pool.connect();
              await client.query('BEGIN');
              const order = await createOrder(client, req.body);
              await client.query('COMMIT');
              client.release();
              res.status(201).json(order);
            });
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                import pg from 'pg';

                export const pool = new pg.Pool({
                  max: 10,
                  connectionTimeoutMillis: 5_000,             // don't wait forever for a free connection
                  statement_timeout: 10_000,                  // server-side limit per statement
                  idle_in_transaction_session_timeout: 15_000,
                });

                app.post('/orders', async (req, res) => {
                  const client = await pool.connect();
                  try {
                    await client.query('BEGIN');
                    const order = await createOrder(client, req.body);
                    await client.query('COMMIT');
                    res.status(201).json(order);
                  } catch (err) {
                    await client.query('ROLLBACK');
                    throw err; // Express 5 -> error middleware
                  } finally {
                    client.release(); // always return the connection
                  }
                });

                // Expose pool health for dashboards/alerts
                setInterval(() => {
                  logger.info({ total: pool.totalCount, idle: pool.idleCount, waiting: pool.waitingCount }, 'pg pool');
                }, 30_000).unref();
            """, label_en="Fixed version (release in finally + fail-fast timeouts)", label_bn="সংশোধিত version (finally-তে release + দ্রুত fail করার timeout)"),
        ],
        follow=[
            ("How would you set app, proxy and database timeouts relative to each other?", "App, proxy আর database-এর timeout পরস্পরের তুলনায় কীভাবে ঠিক করবে?"),
            ("What metrics would have caught this before users noticed?", "কোন metric থাকলে user টের পাওয়ার আগেই এটা ধরা পড়ত?"),
        ],
        related=["express-011", "express-010", "express-007"],
        refs=[NODE_PG_POOL, PINO_HTTP, EX_PERF],
    ),
    # ------------------------------------------------------------------ express-026
    Q(
        id="express-026", sub="Testing", diff="hard", type="coding",
        prio="high", market="both", mins=10,
        tags=["testing", "supertest", "node-test", "dependency-injection", "integration-tests"],
        ver="Express 5.x; Node.js 24 LTS / 26 (node:test); supertest 7.x", vs=False, status="stable",
        q_en=r"""
            Write integration tests for `POST /api/orders` using `node:test` and supertest that check:

            1. `401` without a token;
            2. `400` for invalid input (e.g. `quantity: 0`), with nothing saved;
            3. `201` and the created order for a valid request;
            4. the order is saved with the **authenticated** user's ID, even if the body contains a different `userId`.

            The tests must not open a real port or touch the real database. Show how you'd structure the app to make that possible.
        """,
        q_bn=r"""
            `node:test` আর supertest দিয়ে `POST /api/orders`-এর integration test লেখো, যা check করবে:

            1. token ছাড়া `401`;
            2. invalid input-এ (যেমন `quantity: 0`) `400`, আর কিছুই save হবে না;
            3. valid request-এ `201` আর তৈরি হওয়া order;
            4. body-তে অন্য `userId` থাকলেও order **authenticated** user-এর ID দিয়ে save হবে।

            Test যেন আসল port না খোলে বা আসল database না ছোঁয়। এটা সম্ভব করতে app-এর structure কেমন হবে দেখাও।
        """,
        a_en=r"""
            The key is an **app factory**: `createApp({ ordersRepo, verifyToken })` builds and returns the Express app *without* calling `listen()`, and receives its dependencies as parameters. Production code passes the real PostgreSQL repository and JWT verifier; tests pass in-memory fakes.

            supertest's `request(app)` accepts the app directly and binds it to an ephemeral port internally, so no fixed port is opened and tests can run in parallel. With `node:test` I use `describe`/`it`, build a fresh app in `beforeEach` (so tests don't share state), and assert with `node:assert/strict`: status codes, response body, and — importantly — the side effects recorded by the fake repository (nothing saved on 401/400; `userId` taken from the token).
        """,
        a_bn=r"""
            মূল চাবিকাঠি একটি **app factory**: `createApp({ ordersRepo, verifyToken })` `listen()` call *না করেই* Express app বানিয়ে return করে, আর dependency-গুলো parameter হিসেবে নেয়। Production code আসল PostgreSQL repository আর JWT verifier পাঠায়; test পাঠায় in-memory fake।

            supertest-এর `request(app)` সরাসরি app নেয় এবং ভেতরে ভেতরে একটি ephemeral port-এ bind করে, ফলে কোনো নির্দিষ্ট port খোলে না এবং test parallel-এ চলতে পারে। `node:test`-এ আমি `describe`/`it` ব্যবহার করি, `beforeEach`-এ প্রতিবার নতুন app বানাই (যাতে test-গুলো state share না করে), আর `node:assert/strict` দিয়ে assert করি: status code, response body, আর — গুরুত্বপূর্ণভাবে — fake repository-তে রেকর্ড হওয়া side effect (401/400-এ কিছু save হয়নি; `userId` token থেকে নেওয়া)।
        """,
        ex_en=r"""
            - **Test behaviour, not implementation:** assert on HTTP status, body and observable side effects, not on which internal function was called.
            - **Security-relevant tests matter most:** "nothing is saved on 400" and "userId comes from the token, not the body" catch real vulnerabilities (mass assignment, IDOR) that happy-path tests miss.
            - **Layers of tests:** these fast HTTP-level tests with fakes cover routing, middleware order, validation and auth; separate repository tests against a real PostgreSQL (e.g. in a container) cover SQL. Don't mock what you're trying to test.
            - **Run:** `node --test` discovers `*.test.js` files; `node --test --watch` reruns on change. Jest or Vitest work the same way with supertest.
            - **Error paths:** add tests for the error middleware (e.g. repository throws → 500 problem JSON without leaking the message).
            - Verified: the suite passes (4 tests) on Node 22 with Express 5.3 and supertest 7.
        """,
        ex_bn=r"""
            - **Implementation নয়, behaviour test করো:** HTTP status, body আর দৃশ্যমান side effect-এর উপর assert করো, কোন internal function call হলো তার উপর নয়।
            - **Security-সংক্রান্ত test সবচেয়ে জরুরি:** "400-এ কিছু save হয় না" আর "userId body থেকে নয়, token থেকে আসে" — এগুলো এমন আসল vulnerability (mass assignment, IDOR) ধরে যা happy-path test মিস করে।
            - **Test-এর স্তর:** fake দিয়ে এই দ্রুত HTTP-level test routing, middleware order, validation আর auth ঢাকে; আসল PostgreSQL-এর বিরুদ্ধে (যেমন container-এ) আলাদা repository test SQL ঢাকে। যা test করতে চাও সেটাকেই mock কোরো না।
            - **চালানো:** `node --test` `*.test.js` file খুঁজে নেয়; `node --test --watch` পরিবর্তনে আবার চালায়। Jest বা Vitest-ও supertest-এর সাথে একইভাবে কাজ করে।
            - **Error path:** error middleware-এর জন্যও test যোগ করো (যেমন repository throw করলে message ফাঁস না করে 500 problem JSON)।
            - যাচাই করা: Express 5.3 আর supertest 7 দিয়ে Node 22-এ suite pass করে (4টি test)।
        """,
        tip_en=r"""Start by explaining the app-factory/dependency-injection structure — that's the real answer to "how do you make Express testable". Then write two or three focused tests, including one that checks a side effect.""",
        tip_bn=r"""শুরুতে app-factory/dependency-injection structure ব্যাখ্যা করো — "Express-কে কীভাবে testable বানাও" প্রশ্নের আসল উত্তর এটাই। তারপর দুই-তিনটি নির্দিষ্ট test লেখো, যার একটি side effect check করে।""",
        mist_en=r"""Calling `app.listen()` inside the module under test (port conflicts, open handles), sharing one app/fake across tests, or asserting only status codes.""",
        mist_bn=r"""Test করা module-এর ভেতরেই `app.listen()` call করা (port conflict, খোলা handle), সব test-এ একটাই app/fake share করা, অথবা শুধু status code assert করা।""",
        code=r"""
            // app.js — factory: no listen(), dependencies injected
            import express from 'express';

            export function createApp({ ordersRepo, verifyToken }) {
              const app = express();
              app.use(express.json());

              const authenticate = async (req, res, next) => {
                const token = req.get('authorization')?.replace(/^Bearer /, '');
                const user = token ? await verifyToken(token) : null;
                if (!user) return res.status(401).json({ error: 'UNAUTHENTICATED' });
                req.user = user;
                next();
              };

              app.post('/api/orders', authenticate, async (req, res) => {
                const { productId, quantity } = req.body ?? {};
                if (typeof productId !== 'string' || !Number.isInteger(quantity) || quantity < 1) {
                  return res.status(400).json({ error: 'VALIDATION_FAILED' });
                }
                const order = await ordersRepo.create({ userId: req.user.id, productId, quantity });
                res.status(201).json(order);
              });

              return app;
            }

            // orders.test.js — run with: node --test
            import { describe, it, beforeEach } from 'node:test';
            import assert from 'node:assert/strict';
            import request from 'supertest';
            import { createApp } from './app.js';

            describe('POST /api/orders', () => {
              let app;
              let saved;

              beforeEach(() => {
                saved = [];
                const ordersRepo = {
                  async create(data) {
                    const order = { id: 'ord_1', ...data };
                    saved.push(order);
                    return order;
                  },
                };
                const verifyToken = async (token) =>
                  token === 'valid-token' ? { id: 'user_42', role: 'customer' } : null;
                app = createApp({ ordersRepo, verifyToken }); // no listen(), no real DB
              });

              it('returns 401 without a token', async () => {
                const res = await request(app).post('/api/orders').send({ productId: 'p1', quantity: 1 });
                assert.equal(res.status, 401);
                assert.equal(saved.length, 0);
              });

              it('returns 400 for invalid input and saves nothing', async () => {
                const res = await request(app)
                  .post('/api/orders')
                  .set('Authorization', 'Bearer valid-token')
                  .send({ productId: 'p1', quantity: 0 });
                assert.equal(res.status, 400);
                assert.equal(saved.length, 0);
              });

              it('creates the order for the authenticated user', async () => {
                const res = await request(app)
                  .post('/api/orders')
                  .set('Authorization', 'Bearer valid-token')
                  .send({ productId: 'p1', quantity: 2 });
                assert.equal(res.status, 201);
                assert.deepEqual(res.body, { id: 'ord_1', userId: 'user_42', productId: 'p1', quantity: 2 });
              });

              it('ignores a userId sent in the body', async () => {
                await request(app)
                  .post('/api/orders')
                  .set('Authorization', 'Bearer valid-token')
                  .send({ productId: 'p1', quantity: 1, userId: 'someone_else' });
                assert.equal(saved[0].userId, 'user_42');
              });
            });
        """,
        lang="javascript",
        time="O(1) per test", space="O(1)",
        follow=[
            ("How would you test the real SQL in the repository layer?", "Repository layer-এর আসল SQL কীভাবে test করবে?"),
            ("How do you test rate limiting or time-based behaviour without waiting?", "অপেক্ষা না করে rate limiting বা সময়-নির্ভর আচরণ কীভাবে test করবে?"),
        ],
        related=["express-023", "express-012"],
        refs=[NODE_TEST, SUPERTEST],
    ),
]

if __name__ == "__main__":
    save("express", "b4", QUESTIONS)
