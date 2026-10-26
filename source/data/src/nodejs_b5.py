import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NODE_FS = ("Node.js API — File system (Promises API)", "https://nodejs.org/api/fs.html")
NODE_HTTP = ("Node.js API — HTTP (server.close)", "https://nodejs.org/api/http.html")
NODE_PROCESS = ("Node.js API — process (signal events)", "https://nodejs.org/api/process.html")
EXPRESS_SHUTDOWN = ("Express — Health Checks and Graceful Shutdown", "https://expressjs.com/en/advanced/healthcheck-graceful-shutdown.html")
NODE_ALS = ("Node.js API — Asynchronous context tracking (AsyncLocalStorage)", "https://nodejs.org/api/async_context.html")
PINO = ("pino — JSON logger (GitHub)", "https://github.com/pinojs/pino")
OWASP_LOGGING = ("OWASP — Logging Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html")
NODE_EVENTS = ("Node.js API — Events", "https://nodejs.org/api/events.html")
NODE_GLOBALS = ("Node.js API — Globals (AbortController, AbortSignal)", "https://nodejs.org/api/globals.html")
MDN_ASYNC_GEN = ("MDN — async function*", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function*")
MDN_PROMISE_ALL = ("MDN — Promise.all()", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all")
NODE_STREAM = ("Node.js API — Stream", "https://nodejs.org/api/stream.html")
NODE_BACKPRESSURE = ("Node.js Learn — Backpressuring in Streams", "https://nodejs.org/en/learn/modules/backpressuring-in-streams")
AWS_S3_PRESIGNED = ("AWS — Uploading objects with presigned URLs", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html")

QUESTIONS = [
    # ------------------------------------------------------------------ node-027
    Q(
        id="node-027", sub="File System (fs/promises)", diff="easy", type="debugging",
        prio="high", market="bangladesh", mins=4,
        tags=["fs-promises", "callbacks", "async-await", "error-handling", "try-catch"],
        ver="Node.js 26 LTS / 24", vs=False, status="stable",
        q_en=r"""`readConfig` should return the parsed JSON config, or `{}` if the file is missing or invalid. Instead it always logs `undefined`, and when the file is missing the whole process crashes. Explain both bugs and fix the function.""",
        q_bn=r"""`readConfig`-এর কাজ parse করা JSON config return করা, আর file না থাকলে বা invalid হলে `{}` return করা। কিন্তু এটা সবসময় `undefined` log করে, আর file না থাকলে পুরো process crash করে। দুটো bug ব্যাখ্যা করো এবং function-টি ঠিক করো।""",
        a_en=r"""
            Both bugs come from mixing a callback API with synchronous control flow:

            1. **`undefined`:** `fs.readFile` is asynchronous. `readConfig` starts the read and returns immediately — with nothing, so `undefined`. The `return JSON.parse(data)` inside the callback returns from the *callback*, not from `readConfig`, and nobody receives that value.
            2. **The crash:** `try/catch` only catches errors thrown *synchronously* inside the `try` block. The callback runs later, from the event loop, after `readConfig` has already returned. The `throw err` there is an uncaught exception, so the process dies and the `catch` block never runs.

            Fix: use the promise-based API from `node:fs/promises` with `async`/`await`. Now `await` suspends the function until the read finishes, a rejected promise is caught by `try/catch`, and the caller `await`s the result.
        """,
        a_bn=r"""
            দুটো bug-ই callback API-কে synchronous control flow-এর সাথে মেশানো থেকে এসেছে:

            1. **`undefined`:** `fs.readFile` asynchronous। `readConfig` read শুরু করে সাথে সাথেই return করে — কিছু না দিয়ে, তাই `undefined`। Callback-এর ভেতরের `return JSON.parse(data)` *callback* থেকে return করে, `readConfig` থেকে নয়, আর সেই value কেউ পায় না।
            2. **Crash:** `try/catch` শুধু `try` block-এর ভেতরে *synchronously* throw হওয়া error ধরে। Callback চলে পরে, event loop থেকে, যখন `readConfig` অনেক আগেই return করে ফেলেছে। সেখানকার `throw err` তাই uncaught exception — process মারা যায় এবং `catch` block কখনো চলে না।

            Fix: `async`/`await` সহ `node:fs/promises`-এর promise-based API ব্যবহার করা। এখন `await` read শেষ না হওয়া পর্যন্ত function-কে থামিয়ে রাখে, rejected promise `try/catch`-এ ধরা পড়ে, আর caller ফলাফলের জন্য `await` করে।
        """,
        quick_en=r"""`fs.readFile` is asynchronous, so `readConfig` returns `undefined` before the callback runs, and the `return` inside the callback goes nowhere. The `throw` in the callback happens later, outside `try/catch`, so it crashes the process; fix it with `node:fs/promises` and `async`/`await`.""",
        quick_bn=r"""`fs.readFile` asynchronous, তাই callback চলার আগেই `readConfig` `undefined` return করে দেয়, আর callback-এর ভেতরের `return` কারো কাছে পৌঁছায় না। Callback-এর `throw` পরে ঘটে, `try/catch`-এর বাইরে, তাই process crash করে; সমাধান হলো `node:fs/promises` আর `async`/`await`।""",
        ex_en=r"""
            - The `try/catch` now catches both `ENOENT` (missing file) and the `SyntaxError` from `JSON.parse` (invalid JSON).
            - The caller must also be async (`await readConfig(...)`), or use top-level `await` in an ES module.
            - Returning `{}` silently for *any* error can hide real problems; in production I'd return the default only for `ENOENT` and re-throw others (e.g. `EACCES` permission errors).
            - Never use `fs.readFileSync` inside a request handler — it blocks the event loop. At startup (loading config once) sync APIs are acceptable.
            - If you must call a callback API, wrap it with `util.promisify` instead of mixing styles.
        """,
        ex_bn=r"""
            - এখন `try/catch` `ENOENT` (file নেই) আর `JSON.parse`-এর `SyntaxError` (invalid JSON) দুটোই ধরে।
            - Caller-কেও async হতে হবে (`await readConfig(...)`), অথবা ES module-এ top-level `await` ব্যবহার করতে হবে।
            - *যেকোনো* error-এ চুপচাপ `{}` return করলে আসল সমস্যা লুকিয়ে যেতে পারে; production-এ আমি শুধু `ENOENT`-এ default দেব, আর অন্যগুলো (যেমন `EACCES` permission error) আবার throw করব।
            - Request handler-এর ভেতরে কখনো `fs.readFileSync` ব্যবহার করো না — এটা event loop block করে। Startup-এ (একবার config load করতে) sync API চলে।
            - Callback API ব্যবহার করতেই হলে style না মিশিয়ে `util.promisify` দিয়ে wrap করো।
        """,
        tip_en=r"""Name the two separate root causes — "the return is in the wrong function" and "try/catch can't catch async callback errors". Interviewers want both, not just "use async/await".""",
        tip_bn=r"""দুটো আলাদা মূল কারণের নাম বলো — "return ভুল function-এ" আর "try/catch async callback-এর error ধরতে পারে না"। Interviewer শুধু "async/await ব্যবহার করো" নয়, দুটোই শুনতে চায়।""",
        mist_en=r"""Fixing it by switching to `readFileSync` inside a request path, or adding `async` to `readConfig` while still using the callback version of `readFile`.""",
        mist_bn=r"""Request path-এর ভেতরে `readFileSync`-এ বদলে "ঠিক" করা, অথবা `readConfig`-এ `async` যোগ করে তখনও `readFile`-এর callback version ব্যবহার করা।""",
        code=r"""
            const fs = require('node:fs');

            function readConfig(path) {
              try {
                fs.readFile(path, 'utf8', (err, data) => {
                  if (err) throw err;
                  return JSON.parse(data);
                });
              } catch (err) {
                console.error('Could not read config:', err.message);
                return {};
              }
            }

            const config = readConfig('./config.json');
            console.log(config);
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                const { readFile } = require('node:fs/promises');

                async function readConfig(path) {
                  try {
                    const data = await readFile(path, 'utf8');
                    return JSON.parse(data);
                  } catch (err) {
                    console.error('Could not read config:', err.message);
                    return {};
                  }
                }

                async function main() {
                  const config = await readConfig('./config.json');
                  console.log(config); // { port: 3000 } or {} on error
                }

                main();
            """, label_en="Fixed version (fs/promises + async/await)", label_bn="সংশোধিত version (fs/promises + async/await)"),
        ],
        follow=[
            ("How would you return the default only when the file is missing?", "শুধু file না থাকলেই default return করতে চাইলে কী করবে?"),
            ("When is it acceptable to use synchronous fs APIs in a server?", "Server-এ কখন synchronous fs API ব্যবহার করা চলে?"),
        ],
        related=["node-012"],
        refs=[NODE_FS],
    ),
    # ------------------------------------------------------------------ node-028
    Q(
        id="node-028", sub="Graceful Shutdown", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["graceful-shutdown", "sigterm", "http-server", "readiness", "deployment"],
        ver="Node.js 19+ semantics for server.close() (current: 26 LTS / 24)", vs=True, status="stable",
        q_en=r"""
            Implement graceful shutdown for a plain `node:http` server (no framework). On `SIGTERM` or `SIGINT` it must:

            - immediately report "not ready" (`503`) on `GET /health/ready`, and wait a short, configurable delay so the load balancer stops sending traffic;
            - stop accepting new connections but let in-flight requests finish;
            - close other resources (DB pool, Redis, queue consumers);
            - exit with code `0` on success — and never hang longer than 10 seconds in total.
        """,
        q_bn=r"""
            একটি সাধারণ `node:http` server-এর (কোনো framework ছাড়া) জন্য graceful shutdown implement করো। `SIGTERM` বা `SIGINT` পেলে এটি:

            - সাথে সাথে `GET /health/ready`-এ "not ready" (`503`) জানাবে, এবং ছোট একটি configurable delay অপেক্ষা করবে যাতে load balancer traffic পাঠানো বন্ধ করে;
            - নতুন connection নেওয়া বন্ধ করবে কিন্তু চলমান request শেষ হতে দেবে;
            - অন্য resource (DB pool, Redis, queue consumer) বন্ধ করবে;
            - সফল হলে exit code `0` দিয়ে বের হবে — আর মোট 10 সেকেন্ডের বেশি কখনো আটকে থাকবে না।
        """,
        a_en=r"""
            The pattern is: flag → delay → close → clean up → exit, with a hard deadline as a safety net.

            - A `shuttingDown` flag makes the readiness endpoint return `503` and ignores repeated signals.
            - A short delay gives the load balancer (or Kubernetes endpoints) time to stop routing to this instance.
            - `server.close(callback)` stops accepting new connections; the callback runs once every open connection has closed. Since Node 19 it also closes the keep-alive sockets that are idle *at that moment* — but a socket that is still serving a request stays open for `keepAliveTimeout` after its response (and can even carry new requests). So while draining I send `Connection: close` and keep calling `server.closeIdleConnections()` until the callback fires.
            - In the callback I close DB/Redis/queue resources and set `process.exitCode` instead of calling `process.exit()`, so pending log writes can flush and the process ends naturally.
            - A `setTimeout` (unref'd) force-closes everything with `server.closeAllConnections()` and exits with `1` if draining takes too long.
        """,
        a_bn=r"""
            Pattern-টা হলো: flag → delay → close → clean up → exit, সাথে safety net হিসেবে একটি hard deadline।

            - একটি `shuttingDown` flag readiness endpoint-কে `503` return করায় এবং বারবার আসা signal ignore করে।
            - ছোট একটি delay load balancer-কে (বা Kubernetes endpoint-কে) এই instance-এ routing বন্ধ করার সময় দেয়।
            - `server.close(callback)` নতুন connection নেওয়া বন্ধ করে; সব খোলা connection বন্ধ হলে callback চলে। Node 19 থেকে এটা *সেই মুহূর্তে* idle থাকা keep-alive socket-ও বন্ধ করে — কিন্তু যে socket তখনো কোনো request serve করছে, response-এর পরও সেটা `keepAliveTimeout` পর্যন্ত খোলা থাকে (এমনকি নতুন request-ও নিতে পারে)। তাই draining-এর সময় আমি `Connection: close` পাঠাই এবং callback না আসা পর্যন্ত বারবার `server.closeIdleConnections()` call করি।
            - Callback-এ DB/Redis/queue resource বন্ধ করি এবং `process.exit()` call না করে `process.exitCode` set করি, যাতে বাকি log write flush হয় এবং process স্বাভাবিকভাবে শেষ হয়।
            - একটি (unref করা) `setTimeout` draining বেশি সময় নিলে `server.closeAllConnections()` দিয়ে সব জোর করে বন্ধ করে `1` দিয়ে exit করে।
        """,
        quick_en=r"""Set a `shuttingDown` flag so readiness returns `503`, wait briefly for the load balancer, then `server.close()` (closing idle keep-alive sockets), and in its callback close DB/Redis/queues and set `process.exitCode`. An unref'd `setTimeout` force-closes connections and exits with `1` if draining is too slow.""",
        quick_bn=r"""একটা `shuttingDown` flag set করো যাতে readiness `503` দেয়, load balancer-এর জন্য একটু অপেক্ষা করো, তারপর `server.close()` (idle keep-alive socket বন্ধ করে), আর তার callback-এ DB/Redis/queue বন্ধ করে `process.exitCode` set করো। Unref করা একটা `setTimeout` drain বেশি সময় নিলে connection জোর করে বন্ধ করে `1` দিয়ে exit করে।""",
        ex_en=r"""
            - **Why `unref()` the force timer:** if everything shuts down cleanly, an active timer would otherwise keep the event loop alive for the full 10 seconds.
            - **Why not `process.exit(0)` right away:** it kills in-flight requests and can truncate asynchronous stdout/stderr writes (lost logs).
            - **Signals:** containers send `SIGTERM` (`docker stop`, Kubernetes); `Ctrl+C` sends `SIGINT`. Installing a listener removes Node's default "exit immediately" behaviour, so your handler must eventually end the process. `SIGKILL` can't be caught — that's what arrives when the grace period expires.
            - **PID 1 in Docker:** run `node` directly (exec-form `CMD ["node", "server.js"]`) or with an init like `tini`; `npm start` as PID 1 may not forward signals properly.
            - **Edge cases:** long-lived connections (WebSockets/SSE) won't finish on their own — close them explicitly; the delay plus the longest request must fit within the orchestrator's grace period.
            - Verified on Node: an in-flight request completes after `SIGTERM`, new connections are refused after `close()`, and the process exits with code 0 right after the last response — even when the client keeps its keep-alive socket open. Without the idle-connection closer, the same test waits for `keepAliveTimeout` before exiting.
        """,
        ex_bn=r"""
            - **Force timer-এ `unref()` কেন:** সব ঠিকঠাক বন্ধ হলেও active timer না হলে পুরো 10 সেকেন্ড event loop-কে জীবিত রাখত।
            - **সাথে সাথে `process.exit(0)` কেন নয়:** এটা চলমান request মেরে ফেলে এবং asynchronous stdout/stderr write কেটে দিতে পারে (log হারায়)।
            - **Signal:** container `SIGTERM` পাঠায় (`docker stop`, Kubernetes); `Ctrl+C` পাঠায় `SIGINT`। Listener লাগালে Node-এর default "সাথে সাথে exit" আচরণ বাদ পড়ে, তাই তোমার handler-কেই শেষে process বন্ধ করতে হবে। `SIGKILL` ধরা যায় না — grace period শেষ হলে সেটাই আসে।
            - **Docker-এ PID 1:** সরাসরি `node` চালাও (exec-form `CMD ["node", "server.js"]`) অথবা `tini`-এর মতো init দিয়ে; PID 1 হিসেবে `npm start` হয়তো signal ঠিকমতো forward করে না।
            - **Edge case:** দীর্ঘস্থায়ী connection (WebSocket/SSE) নিজে থেকে শেষ হয় না — explicitly বন্ধ করো; delay আর সবচেয়ে লম্বা request মিলিয়ে orchestrator-এর grace period-এর মধ্যে থাকতে হবে।
            - Node-এ যাচাই করা: `SIGTERM`-এর পরেও চলমান request শেষ হয়, `close()`-এর পরে নতুন connection refuse হয়, আর শেষ response-এর ঠিক পরেই process exit code 0 দিয়ে বের হয় — client তার keep-alive socket খোলা রাখলেও। Idle-connection closer ছাড়া একই test-এ exit করার আগে `keepAliveTimeout` পর্যন্ত অপেক্ষা করতে হয়।
        """,
        tip_en=r"""Say the sequence out loud before coding: "flip readiness, wait, close the server, clean up, exit — with a deadline". Then mention the Node 19 change to `server.close()` and why the timer is unref'd.""",
        tip_bn=r"""Code লেখার আগে ধাপগুলো মুখে বলো: "readiness উল্টাও, অপেক্ষা করো, server বন্ধ করো, clean up, exit — একটি deadline সহ"। তারপর `server.close()`-এ Node 19-এর পরিবর্তন আর timer কেন unref করা সেটা উল্লেখ করো।""",
        mist_en=r"""Calling `process.exit()` directly in the signal handler, forgetting a hard timeout (a stuck request blocks the deploy), or not ignoring a second signal (double cleanup).""",
        mist_bn=r"""Signal handler-এ সরাসরি `process.exit()` call করা, hard timeout ভুলে যাওয়া (একটি আটকে থাকা request deploy আটকে দেয়), অথবা দ্বিতীয় signal ignore না করা (দুবার cleanup)।""",
        code=r"""
            import http from 'node:http';
            import { setTimeout as sleep } from 'node:timers/promises';

            const READINESS_DELAY_MS = Number(process.env.READINESS_DELAY_MS ?? 5_000);
            const FORCE_EXIT_MS = 10_000;
            let shuttingDown = false;

            const server = http.createServer(async (req, res) => {
              if (shuttingDown) res.setHeader('Connection', 'close'); // don't keep sockets alive while draining
              if (req.url === '/health/ready') {
                res.statusCode = shuttingDown ? 503 : 200;
                return res.end(shuttingDown ? 'draining' : 'ok');
              }
              await sleep(2_000); // simulate a slow request (DB call, external API...)
              res.end('done\n');
            });

            server.listen(3000, () => console.log('listening on :3000'));

            async function closeResources() {
              // await db.end(); await redis.quit(); await queueConsumer.close();
            }

            async function shutdown(signal) {
              if (shuttingDown) return; // ignore repeated signals
              shuttingDown = true;      // readiness now returns 503
              console.log(`${signal} received: draining`);

              // Safety net: never hang longer than FORCE_EXIT_MS
              const forceTimer = setTimeout(() => {
                console.error('drain timeout: forcing exit');
                server.closeAllConnections();
                process.exit(1);
              }, FORCE_EXIT_MS);
              forceTimer.unref();

              // Give the load balancer time to notice we're not ready
              await sleep(READINESS_DELAY_MS);

              // close() (Node 19+) closes sockets that are idle right now; a keep-alive socket
              // that is still busy would stay open for keepAliveTimeout after its response.
              const idleCloser = setInterval(() => server.closeIdleConnections(), 250);
              idleCloser.unref();

              // Stop accepting connections; the callback runs once every connection has closed.
              server.close(async (err) => {
                clearInterval(idleCloser);
                try {
                  await closeResources();
                  console.log('clean shutdown');
                  process.exitCode = err ? 1 : 0;
                } catch (cleanupErr) {
                  console.error('cleanup failed', cleanupErr);
                  process.exitCode = 1;
                } finally {
                  clearTimeout(forceTimer);
                }
              });
            }

            process.on('SIGTERM', () => shutdown('SIGTERM'));
            process.on('SIGINT', () => shutdown('SIGINT'));
        """,
        lang="javascript",
        time="O(1) work per signal (waits for in-flight requests)", space="O(1)",
        follow=[
            ("How would this change for an Express app with WebSocket connections?", "WebSocket connection থাকা Express app-এর জন্য এটা কীভাবে বদলাবে?"),
            ("Why might `npm start` as the container entrypoint break graceful shutdown?", "Container entrypoint হিসেবে `npm start` কেন graceful shutdown নষ্ট করতে পারে?"),
        ],
        related=["node-020", "node-007"],
        refs=[NODE_HTTP, NODE_PROCESS, EXPRESS_SHUTDOWN],
    ),
    # ------------------------------------------------------------------ node-029
    Q(
        id="node-029", sub="Logging", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["logging", "pino", "asynclocalstorage", "request-id", "observability"],
        ver="Node.js 26 LTS / 24; pino 10 / Express 5.x (example)", vs=False, status="stable",
        q_en=r"""How do you implement structured logging in a Node.js API so that every log line written during a request carries the same request ID — without passing a `requestId` argument through every function?""",
        q_bn=r"""Node.js API-তে structured logging কীভাবে implement করবে, যাতে একটি request চলাকালীন লেখা প্রতিটি log line-এ একই request ID থাকে — অথচ প্রতিটি function-এ `requestId` argument পাঠাতে না হয়?""",
        a_en=r"""
            Two pieces:

            1. **A structured JSON logger** such as pino. Each line is a JSON object with level, time, message and fields (`{"level":30,"requestId":"…","orderId":"42","msg":"loading order"}`), so a log platform (Loki, ELK, CloudWatch, Datadog) can filter and aggregate by field instead of grepping text.
            2. **`AsyncLocalStorage`** from `node:async_hooks` for request context. A middleware at the start of each request reads an incoming `X-Request-Id` (or generates one with `crypto.randomUUID()`), creates a child logger bound to that ID, and calls `als.run(store, next)`. Everything that runs as part of that request — including code after `await`s, deep in services and repositories — can call `als.getStore()` and get the same logger, without any parameter threading.

            I also echo the ID back in the response header so support can correlate a user's report with the logs, and forward it to downstream services.
        """,
        a_bn=r"""
            দুটি অংশ:

            1. **Structured JSON logger**, যেমন pino। প্রতিটি line একটি JSON object — level, time, message আর field সহ (`{"level":30,"requestId":"…","orderId":"42","msg":"loading order"}`), ফলে log platform (Loki, ELK, CloudWatch, Datadog) text grep না করে field দিয়ে filter ও aggregate করতে পারে।
            2. Request context-এর জন্য `node:async_hooks`-এর **`AsyncLocalStorage`**। প্রতিটি request-এর শুরুতে একটি middleware আসা `X-Request-Id` পড়ে (বা `crypto.randomUUID()` দিয়ে নতুন তৈরি করে), সেই ID-যুক্ত একটি child logger বানায় এবং `als.run(store, next)` call করে। ওই request-এর অংশ হিসেবে যা কিছু চলে — `await`-এর পরের code, service আর repository-র গভীরে থাকা code-সহ — `als.getStore()` call করে একই logger পায়, কোনো parameter পাঠানো ছাড়াই।

            আমি ID-টা response header-এও ফেরত দিই, যাতে support টিম user-এর অভিযোগ log-এর সাথে মেলাতে পারে, আর downstream service-এও forward করি।
        """,
        quick_en=r"""Use a structured JSON logger such as pino plus `AsyncLocalStorage` from `node:async_hooks`: a middleware reads or generates a request ID, creates a child logger and calls `als.run(store, next)`. Any code in that request, even after `await`s, gets the same logger with `als.getStore()`.""",
        quick_bn=r"""pino-র মতো structured JSON logger আর `node:async_hooks`-এর `AsyncLocalStorage` ব্যবহার করো: একটা middleware request ID পড়ে বা তৈরি করে, child logger বানায় আর `als.run(store, next)` call করে। ওই request-এর যেকোনো code, `await`-এর পরেও, `als.getStore()` দিয়ে একই logger পায়।""",
        ex_en=r"""
            - **Why pino:** it's fast (logs are serialised cheaply and can be written by a worker-thread transport), outputs JSON by default, and has built-in `redact` paths so passwords and `Authorization` headers never reach the logs. `pino-http` adds automatic request/response logs with timing.
            - **How ALS works:** Node tracks async resources (promises, timers, I/O callbacks) and carries the store along the async call chain started by `run()`. It's stable and much simpler than the old continuation-local-storage libraries.
            - **Validate incoming IDs** (length and characters) — otherwise clients can inject garbage into your logs.
            - **Log levels:** `info` for business events, `warn` for recoverable problems, `error` with the error object (stack included), `debug` off in production. Don't log full request bodies or personal data.
            - **Beyond logs:** OpenTelemetry uses the same context idea to propagate trace IDs across services; log lines can then include `traceId` for jumping between logs and traces.
        """,
        ex_bn=r"""
            - **কেন pino:** এটা দ্রুত (log সস্তায় serialise হয় এবং worker-thread transport দিয়ে লেখা যায়), default-ভাবে JSON দেয়, আর built-in `redact` path আছে যাতে password ও `Authorization` header কখনো log-এ না পৌঁছায়। `pino-http` timing সহ স্বয়ংক্রিয় request/response log যোগ করে।
            - **ALS কীভাবে কাজ করে:** Node async resource (promise, timer, I/O callback) track করে এবং `run()` দিয়ে শুরু হওয়া async call chain ধরে store বহন করে। এটা stable, আর পুরনো continuation-local-storage library-গুলোর চেয়ে অনেক সহজ।
            - **আসা ID validate করো** (দৈর্ঘ্য আর character) — নইলে client তোমার log-এ আবর্জনা ঢুকিয়ে দিতে পারে।
            - **Log level:** business event-এর জন্য `info`, সামলানো যায় এমন সমস্যার জন্য `warn`, error object (stack সহ) দিয়ে `error`, production-এ `debug` বন্ধ। পুরো request body বা personal data log করো না।
            - **Log-এর বাইরে:** OpenTelemetry একই context ধারণা দিয়ে service-জুড়ে trace ID propagate করে; তখন log line-এ `traceId` রাখলে log আর trace-এর মধ্যে সহজে যাওয়া যায়।
        """,
        tip_en=r"""Name both halves explicitly — "JSON logs for machines" and "AsyncLocalStorage for context" — and add one security point (redaction or validating the incoming ID). That combination sounds like production experience.""",
        tip_bn=r"""দুটো অংশের নাম স্পষ্ট করে বলো — "machine-এর জন্য JSON log" আর "context-এর জন্য AsyncLocalStorage" — এবং একটি security point যোগ করো (redaction বা আসা ID validate করা)। এই সমন্বয় production অভিজ্ঞতার মতো শোনায়।""",
        mist_en=r"""Storing the current request in a module-level variable (it gets overwritten by concurrent requests), or using `console.log` with string concatenation and hoping to grep it later.""",
        mist_bn=r"""Module-level variable-এ current request রাখা (concurrent request এসে সেটা overwrite করে দেয়), অথবা string জোড়া দিয়ে `console.log` করে পরে grep করার আশা করা।""",
        code=r"""
            import { AsyncLocalStorage } from 'node:async_hooks';
            import { randomUUID } from 'node:crypto';
            import express from 'express';
            import pino from 'pino';

            const baseLogger = pino({
              level: process.env.LOG_LEVEL ?? 'info',
              redact: ['req.headers.authorization', '*.password'],
            });
            const als = new AsyncLocalStorage();

            // Use this anywhere: services, repositories, utilities
            export const log = () => als.getStore()?.logger ?? baseLogger;

            const app = express();

            app.use((req, res, next) => {
              const incoming = req.get('x-request-id');
              const requestId = incoming && /^[\w-]{1,64}$/.test(incoming) ? incoming : randomUUID();
              res.set('x-request-id', requestId);
              als.run({ requestId, logger: baseLogger.child({ requestId }) }, next);
            });

            async function findOrder(id) {
              log().info({ orderId: id }, 'loading order'); // carries requestId automatically
              return db.orders.findById(id);
            }

            app.get('/orders/:id', async (req, res) => {
              res.json(await findOrder(req.params.id));
            });
        """,
        lang="javascript",
        follow=[
            ("How would you propagate the request ID to downstream HTTP calls and queue jobs?", "Request ID downstream HTTP call আর queue job-এ কীভাবে পাঠাবে?"),
            ("What should never be logged, and how do you enforce it?", "কী কখনো log করা উচিত নয়, আর সেটা কীভাবে নিশ্চিত করবে?"),
        ],
        related=["node-006"],
        refs=[NODE_ALS, PINO, OWASP_LOGGING],
    ),
    # ------------------------------------------------------------------ node-030
    Q(
        id="node-030", sub="API Design", diff="medium", type="conceptual",
        prio="medium", market="both", mins=6,
        tags=["api-design", "async-iterators", "eventemitter", "abortsignal", "promises"],
        ver="Node.js 26 LTS / 24", vs=False, status="stable",
        q_en=r"""Node.js offers callbacks, Promises/async-await, EventEmitters, streams and async iterators for asynchronous work. When you design a module's public API — for example a client for a payment provider or a paginated data exporter — how do you choose which style to expose, and how do you support cancellation?""",
        q_bn=r"""Asynchronous কাজের জন্য Node.js-এ আছে callback, Promise/async-await, EventEmitter, stream আর async iterator। একটি module-এর public API design করার সময় — যেমন payment provider-এর client বা paginated data exporter — কোন style expose করবে কীভাবে ঠিক করো, আর cancellation কীভাবে support করো?""",
        a_en=r"""
            I match the API style to the **shape of the result**:

            - **One result, one time** (charge a card, fetch a user) → return a **Promise** (an `async` function). This is the default for modern Node APIs; error-first callbacks are legacy, and `util.promisify` bridges old ones.
            - **Many independent events over time** with no consumer pacing (connected, message, reconnecting, error) → an **EventEmitter** (or `EventTarget`), always emitting `'error'` for failures.
            - **A large or unbounded sequence of data** where the consumer should control the pace (export 2 million rows, read pages from an API) → a **Readable stream** or an **async iterator**. An `async function*` is the simplest way: the consumer pulls with `for await`, and the producer doesn't fetch the next page until it's needed — natural backpressure.

            For **cancellation and timeouts** I accept an options object with `signal` (an `AbortSignal`). It composes with almost everything in Node — `fetch`, `timers/promises`, `stream/promises` `pipeline`, `events.once` — and callers can use `AbortSignal.timeout(ms)` or combine signals with `AbortSignal.any()`.
        """,
        a_bn=r"""
            আমি API style-কে **ফলাফলের আকৃতির** সাথে মেলাই:

            - **একটি ফলাফল, একবার** (card charge, user fetch) → **Promise** return করা (একটি `async` function)। আধুনিক Node API-র default এটাই; error-first callback legacy, আর পুরনোগুলোকে `util.promisify` দিয়ে জোড়া লাগানো যায়।
            - **সময়ের সাথে অনেক স্বাধীন event**, যেখানে consumer গতি নিয়ন্ত্রণ করে না (connected, message, reconnecting, error) → **EventEmitter** (বা `EventTarget`), failure-এ সবসময় `'error'` emit করে।
            - **বড় বা সীমাহীন data sequence**, যেখানে consumer-এর গতি নিয়ন্ত্রণ করা উচিত (২০ লাখ row export, API থেকে page পড়া) → **Readable stream** বা **async iterator**। `async function*` সবচেয়ে সহজ উপায়: consumer `for await` দিয়ে টেনে নেয়, আর দরকার না হওয়া পর্যন্ত producer পরের page fetch করে না — স্বাভাবিক backpressure।

            **Cancellation ও timeout**-এর জন্য আমি `signal` (একটি `AbortSignal`) সহ একটি options object নিই। এটা Node-এর প্রায় সবকিছুর সাথে মিলে যায় — `fetch`, `timers/promises`, `stream/promises`-এর `pipeline`, `events.once` — আর caller `AbortSignal.timeout(ms)` ব্যবহার করতে পারে বা `AbortSignal.any()` দিয়ে signal জোড়া লাগাতে পারে।
        """,
        quick_en=r"""Match the style to the shape of the result: one result → a Promise (an `async` function), many events over time → an EventEmitter, a large sequence the consumer should pace → a Readable stream or `async function*`. For cancellation and timeouts, accept an `AbortSignal` as `signal` in the options.""",
        quick_bn=r"""Result-এর ধরন দেখে style বেছে নাও: একটা result → Promise (`async` function), সময়ের সাথে অনেক event → EventEmitter, বড় sequence যার গতি consumer ঠিক করবে → Readable stream বা `async function*`। Cancellation আর timeout-এর জন্য options-এ `signal` হিসেবে একটা `AbortSignal` নাও।""",
        ex_en=r"""
            - **Don't release Zalgo:** a function must be *always* async or *always* sync. Calling a callback synchronously in one branch (e.g. a cache hit) and asynchronously in another causes ordering bugs that are hard to reproduce.
            - **Don't offer two styles in one function** (return a promise *and* accept a callback) — it doubles the surface and the error paths.
            - **Converting between styles:** `events.on(emitter, 'data', { signal })` turns events into an async iterator; `Readable.from(asyncIterable)` turns an async iterator into a stream; `for await` (or the still-experimental `readable.toArray()`) consumes streams.
            - **Breaking out of `for await`** calls the generator's `return()`, so cleanup in a `finally` block runs and no more pages are fetched.
            - **Errors:** reject with real `Error` objects with `code` properties (`err.code === 'PAYMENT_DECLINED'`) so callers can branch without parsing messages; use `cause` to wrap lower-level errors.
        """,
        ex_bn=r"""
            - **Zalgo ছেড়ে দিও না:** একটি function-কে হয় *সবসময়* async নয়তো *সবসময়* sync হতে হবে। এক branch-এ (যেমন cache hit) callback synchronously আর অন্য branch-এ asynchronously call করলে এমন ordering bug হয় যা reproduce করা কঠিন।
            - **এক function-এ দুটো style দিও না** (promise return *এবং* callback নেওয়া) — এতে surface আর error path দুটোই দ্বিগুণ হয়।
            - **Style বদলানো:** `events.on(emitter, 'data', { signal })` event-কে async iterator বানায়; `Readable.from(asyncIterable)` async iterator-কে stream বানায়; `for await` (বা এখনও experimental `readable.toArray()`) stream consume করে।
            - **`for await` থেকে `break` করলে** generator-এর `return()` call হয়, ফলে `finally` block-এর cleanup চলে এবং আর কোনো page fetch হয় না।
            - **Error:** `code` property সহ আসল `Error` object দিয়ে reject করো (`err.code === 'PAYMENT_DECLINED'`), যাতে caller message parse না করেই branch করতে পারে; নিচের স্তরের error wrap করতে `cause` ব্যবহার করো।
        """,
        tip_en=r"""Give the decision rule in one sentence ("single value → Promise, events → EventEmitter, sequence → stream/async iterator") and then show an `AbortSignal` in the signature. That reads as someone who has designed libraries, not just consumed them.""",
        tip_bn=r"""এক বাক্যে decision rule বলো ("একক value → Promise, event → EventEmitter, sequence → stream/async iterator"), তারপর signature-এ একটি `AbortSignal` দেখাও। এতে মনে হয় তুমি শুধু library ব্যবহার করোনি, design-ও করেছ।""",
        mist_en=r"""Returning a giant array for unbounded data (memory blow-up), or building cancellation with ad-hoc boolean flags instead of `AbortSignal`.""",
        mist_bn=r"""সীমাহীন data-র জন্য বিশাল array return করা (memory বিস্ফোরণ), অথবা `AbortSignal` ব্যবহার না করে নিজের মতো boolean flag দিয়ে cancellation বানানো।""",
        code=r"""
            // Paginated exporter: pull-based, cancellable, constant memory
            export async function* listInvoices({ pageSize = 100, signal } = {}) {
              let cursor;
              do {
                const url = new URL('https://billing.example.com/v1/invoices');
                url.searchParams.set('limit', String(pageSize));
                if (cursor) url.searchParams.set('cursor', cursor);

                const res = await fetch(url, { signal });
                if (!res.ok) throw new Error(`Billing API responded ${res.status}`);
                const { data, nextCursor } = await res.json();

                yield* data;        // consumer pulls one invoice at a time
                cursor = nextCursor;
              } while (cursor);
            }

            // Consumer: stops fetching pages as soon as it breaks or the signal aborts
            const signal = AbortSignal.timeout(30_000);
            for await (const invoice of listInvoices({ signal })) {
              if (invoice.status === 'overdue') await sendReminder(invoice);
            }
        """,
        lang="javascript",
        follow=[
            ("What does 'releasing Zalgo' mean, and how do you avoid it?", "'Releasing Zalgo' মানে কী, আর কীভাবে এড়াবে?"),
            ("How would you turn this async generator into a Node.js stream?", "এই async generator-কে কীভাবে Node.js stream-এ রূপান্তর করবে?"),
        ],
        related=["node-005", "node-031"],
        refs=[NODE_EVENTS, NODE_GLOBALS, MDN_ASYNC_GEN],
    ),
    # ------------------------------------------------------------------ node-031
    Q(
        id="node-031", sub="Asynchronous Programming", diff="hard", type="coding",
        prio="high", market="both", mins=10,
        tags=["concurrency-limit", "promises", "async-await", "worker-pool", "coding"],
        ver="Node.js 26 LTS / 24 (ES2017+ async/await)", vs=False, status="stable",
        q_en=r"""
            Write `mapWithConcurrency(items, limit, fn)` that calls the async function `fn(item, index)` for every item, with **at most `limit` calls in flight at once**, and resolves to the results **in input order**. If any call rejects, the returned promise must reject and no new items may be started. No libraries.

            Use case: call an external API for 10,000 product IDs without opening 10,000 connections at once.

            Example: with `fn = async (ms) => { await sleep(ms); return ms; }`, `await mapWithConcurrency([300, 100, 200], 2, fn)` resolves to `[300, 100, 200]` after about 300 ms (input order, even though `100` finishes first).
        """,
        q_bn=r"""
            `mapWithConcurrency(items, limit, fn)` লেখো, যা প্রতিটি item-এর জন্য async function `fn(item, index)` call করবে, **একসাথে সর্বোচ্চ `limit`টি call চলবে**, এবং ফলাফল **input-এর ক্রমে** resolve করবে। কোনো call reject করলে return করা promise reject হবে এবং নতুন কোনো item শুরু হবে না। কোনো library ছাড়া।

            Use case: 10,000 product ID-র জন্য একটি external API call করা, কিন্তু একসাথে 10,000 connection না খুলে।

            উদাহরণ: `fn = async (ms) => { await sleep(ms); return ms; }` হলে `await mapWithConcurrency([300, 100, 200], 2, fn)` প্রায় 300 ms পরে `[300, 100, 200]`-এ resolve হবে (input-এর ক্রমে, যদিও `100` আগে শেষ হয়)।
        """,
        a_en=r"""
            I use the **worker-pool pattern**: start `min(limit, items.length)` async "workers"; each one loops, takes the next unclaimed index, awaits `fn`, stores the result at that index, and repeats until the items run out. `Promise.all(workers)` resolves when every worker finishes, and writing results by index keeps input order. A shared `failed` flag stops workers from claiming new items after the first rejection, and `Promise.all` propagates that rejection to the caller.

            It's safe without locks because JavaScript runs one callback at a time — `nextIndex++` happens synchronously between `await`s, so two workers can never claim the same index.
        """,
        a_bn=r"""
            আমি **worker-pool pattern** ব্যবহার করি: `min(limit, items.length)`টি async "worker" চালু করি; প্রত্যেকে loop-এ পরের claim না হওয়া index নেয়, `fn`-এর জন্য await করে, ফলাফল সেই index-এ রাখে, আর item শেষ না হওয়া পর্যন্ত চালিয়ে যায়। সব worker শেষ হলে `Promise.all(workers)` resolve হয়, আর index ধরে ফলাফল লেখায় input-এর ক্রম ঠিক থাকে। একটি shared `failed` flag প্রথম rejection-এর পর worker-দের নতুন item নিতে বাধা দেয়, আর `Promise.all` সেই rejection caller-এর কাছে পৌঁছে দেয়।

            Lock ছাড়াই এটা নিরাপদ, কারণ JavaScript একবারে একটি callback চালায় — `nextIndex++` দুটো `await`-এর মাঝে synchronously ঘটে, তাই দুটো worker কখনো একই index নিতে পারে না।
        """,
        quick_en=r"""Use a worker pool: start `min(limit, items.length)` async workers that each claim the next index, await `fn`, store the result at that index and loop; `Promise.all` waits for them. Writing by index keeps input order, and a shared `failed` flag stops new work after a rejection; O(n) time and space.""",
        quick_bn=r"""Worker pool ব্যবহার করো: `min(limit, items.length)`টা async worker চালু করো, প্রত্যেকে পরের index নেয়, `fn` await করে, result সেই index-এ রাখে আর আবার ঘোরে; `Promise.all` সবগুলোর জন্য অপেক্ষা করে। Index ধরে লেখায় input order ঠিক থাকে, আর shared `failed` flag rejection-এর পরে নতুন কাজ থামায়; time আর space O(n)।""",
        ex_en=r"""
            - **Why not `Promise.all(items.map(fn))`:** it starts all 10,000 calls immediately — thousands of sockets, rate-limit bans, memory spikes, and `EMFILE`/timeouts.
            - **Why not fixed batches** (`Promise.all` on chunks of 5): each batch waits for its slowest item, so slots sit idle. The pool keeps all `limit` slots busy.
            - **Fail-fast caveat:** calls already in flight keep running after the first failure (promises can't be cancelled). For real cancellation, create an `AbortController`, pass its `signal` to `fn`, and abort it in the `catch`.
            - **Variants:** collect `{ status, value | reason }` like `Promise.allSettled` instead of failing fast; add retries with backoff inside `fn`; add a per-call timeout with `AbortSignal.timeout()`.
            - **Edge cases:** `limit` must be a positive integer (validated); an empty array resolves to `[]` immediately; `limit` larger than `items.length` just starts fewer workers.
            - In production, the well-tested `p-limit`/`p-map` packages implement the same idea.
            - Tested on Node: max 3 concurrent calls for `limit = 3`, ordered results, and no new items started after a rejection.
        """,
        ex_bn=r"""
            - **কেন `Promise.all(items.map(fn))` নয়:** এটা সাথে সাথে 10,000টি call শুরু করে — হাজার হাজার socket, rate-limit ban, memory spike, আর `EMFILE`/timeout।
            - **কেন নির্দিষ্ট batch নয়** (5টির chunk-এ `Promise.all`): প্রতিটি batch তার সবচেয়ে ধীর item-এর জন্য অপেক্ষা করে, ফলে slot অলস বসে থাকে। Pool সব `limit` slot ব্যস্ত রাখে।
            - **Fail-fast-এর সীমা:** প্রথম failure-এর পরেও যে call-গুলো চলছিল সেগুলো চলতে থাকে (promise cancel করা যায় না)। আসল cancellation-এর জন্য একটি `AbortController` বানিয়ে তার `signal` `fn`-এ পাঠাও এবং `catch`-এ abort করো।
            - **Variant:** fail-fast না করে `Promise.allSettled`-এর মতো `{ status, value | reason }` জমানো; `fn`-এর ভেতরে backoff সহ retry; `AbortSignal.timeout()` দিয়ে প্রতি call-এ timeout।
            - **Edge case:** `limit` অবশ্যই positive integer (validate করা হয়েছে); খালি array সাথে সাথে `[]`-এ resolve হয়; `limit` `items.length`-এর চেয়ে বড় হলে শুধু কম worker চালু হয়।
            - Production-এ ভালোভাবে test করা `p-limit`/`p-map` package একই ধারণা implement করে।
            - Node-এ test করা: `limit = 3`-এ সর্বোচ্চ 3টি concurrent call, ক্রম ঠিক রাখা ফলাফল, আর rejection-এর পর নতুন কোনো item শুরু হয় না।
        """,
        tip_en=r"""Explain why `Promise.all` alone and fixed-size batches are both wrong before writing code — it shows you understand the problem, not just the pattern. Then mention the in-flight-calls caveat and `AbortSignal` as the fix.""",
        tip_bn=r"""Code লেখার আগে ব্যাখ্যা করো কেন শুধু `Promise.all` আর নির্দিষ্ট আকারের batch — দুটোই ভুল; এতে বোঝা যায় তুমি শুধু pattern নয়, সমস্যাটা বুঝেছ। তারপর চলমান call-এর সীমাবদ্ধতা আর fix হিসেবে `AbortSignal`-এর কথা বলো।""",
        mist_en=r"""Pushing results in completion order (`results.push`) instead of by index, starting all promises first and then "limiting" with `await` (they're already running), or forgetting that an exception in one worker should stop the others from taking new work.""",
        mist_bn=r"""Index ধরে না রেখে শেষ হওয়ার ক্রমে (`results.push`) ফলাফল রাখা, আগে সব promise শুরু করে তারপর `await` দিয়ে "limit" করা (ততক্ষণে সেগুলো চলছেই), অথবা ভুলে যাওয়া যে একটি worker-এ exception হলে বাকিদের নতুন কাজ নেওয়া বন্ধ করা উচিত।""",
        code=r"""
            export async function mapWithConcurrency(items, limit, fn) {
              if (!Number.isInteger(limit) || limit < 1) {
                throw new RangeError('limit must be a positive integer');
              }
              const results = new Array(items.length);
              let nextIndex = 0;
              let failed = false;

              async function worker() {
                while (!failed && nextIndex < items.length) {
                  const i = nextIndex++; // claimed synchronously: no two workers get the same i
                  try {
                    results[i] = await fn(items[i], i);
                  } catch (err) {
                    failed = true; // stop other workers from starting new items
                    throw err;
                  }
                }
              }

              const workers = Array.from({ length: Math.min(limit, items.length) }, () => worker());
              await Promise.all(workers);
              return results;
            }

            // Usage: at most 5 concurrent requests, each with its own timeout
            // const products = await mapWithConcurrency(ids, 5, async (id) => {
            //   const res = await fetch(`https://api.example.com/products/${id}`, {
            //     signal: AbortSignal.timeout(5_000),
            //   });
            //   if (!res.ok) throw new Error(`product ${id}: HTTP ${res.status}`);
            //   return res.json();
            // });
        """,
        lang="javascript",
        time="O(n) scheduling overhead (plus the cost of fn)", space="O(n) for results",
        follow=[
            ("How would you add retries with exponential backoff to failed items?", "Failed item-এ exponential backoff সহ retry কীভাবে যোগ করবে?"),
            ("How would you change this to keep going and report all failures at the end?", "কীভাবে বদলাবে যাতে থেমে না গিয়ে শেষে সব failure report করে?"),
        ],
        related=["node-030", "node-007"],
        refs=[MDN_PROMISE_ALL, NODE_GLOBALS],
    ),
    # ------------------------------------------------------------------ node-032
    Q(
        id="node-032", sub="Streams", diff="extreme", type="architecture",
        prio="high", market="international", mins=20,
        tags=["file-upload", "backpressure", "streams", "s3", "presigned-url", "memory"],
        ver="Node.js 26 LTS / 24; Express 5.x; AWS SDK for JavaScript v3 (example)", vs=False, status="stable",
        q_en=r"""Incident: your Node.js API accepts video uploads (up to 2 GB) and forwards them to object storage (S3). Under load — around 20 concurrent uploads — memory spikes, containers get OOM-killed, and unrelated API requests time out. The current handler uses `multer.memoryStorage()` and then calls `PutObject` with the whole buffer. Explain the root cause and redesign the upload path.""",
        q_bn=r"""Incident: তোমার Node.js API video upload (সর্বোচ্চ 2 GB) নেয় এবং object storage-এ (S3) পাঠায়। Load-এর সময় — প্রায় 20টি concurrent upload হলে — memory হঠাৎ বেড়ে যায়, container OOM-kill হয়, আর সম্পর্কহীন API request-ও timeout হয়। বর্তমান handler `multer.memoryStorage()` ব্যবহার করে, তারপর পুরো buffer দিয়ে `PutObject` call করে। মূল কারণ ব্যাখ্যা করো এবং upload path নতুন করে design করো।""",
        a_en=r"""
            *(Advanced, senior-level answer.)* **Root cause:** the handler buffers each whole file in memory before uploading. 20 concurrent 2 GB uploads can mean tens of gigabytes of Buffers. There is **no backpressure**: the server reads from fast clients as quickly as possible regardless of how fast S3 accepts the data. GC pressure and memory exhaustion then slow the event loop for every other request, and finally the kernel OOM-kills the container.

            **Redesign, in order of preference:**

            1. **Take the bytes off the API path entirely — presigned uploads.** The API authenticates the user, validates metadata (type, declared size), and returns a presigned URL (S3 multipart presigned URLs for large files). The browser uploads directly to S3. Node handles only small JSON requests. An S3 event (or a "complete" callback) triggers post-processing — virus scan, transcoding — through a queue.
            2. **If the API must proxy the bytes** (compliance, encryption, inspection): **stream with backpressure.** Don't use memory storage; pipe the request stream through a byte-limit `Transform` into a multipart uploader whose memory is bounded (`queueSize × partSize`, e.g. 4 × 8 MiB ≈ 32 MiB per upload). `pipeline()` pauses reading from the client socket when S3 is slower, which slows the client down via TCP flow control.
            3. **Protect the service:** cap concurrent uploads per instance (return `503`/`429` when full), enforce max size early (`Content-Length` check) and while streaming, set timeouts for slow clients, run uploads on dedicated instances so they can't starve the main API, and abort multipart uploads on failure (plus an S3 lifecycle rule to clean up incomplete ones).
        """,
        a_bn=r"""
            *(Advanced, senior-level উত্তর।)* **মূল কারণ:** handler upload করার আগে প্রতিটি পুরো file memory-তে buffer করে। 20টি concurrent 2 GB upload মানে কয়েক দশ GB Buffer হতে পারে। এখানে **কোনো backpressure নেই**: S3 কত দ্রুত data নিচ্ছে তা না দেখে server দ্রুত client-দের কাছ থেকে যত দ্রুত সম্ভব পড়তে থাকে। এরপর GC-র চাপ আর memory শেষ হয়ে যাওয়া বাকি সব request-এর জন্য event loop ধীর করে দেয়, আর শেষে kernel container-কে OOM-kill করে।

            **নতুন design, পছন্দের ক্রমে:**

            1. **Byte-গুলো API path থেকে পুরোপুরি সরিয়ে দাও — presigned upload।** API user authenticate করে, metadata (type, ঘোষিত size) validate করে, এবং একটি presigned URL return করে (বড় file-এর জন্য S3 multipart presigned URL)। Browser সরাসরি S3-এ upload করে। Node শুধু ছোট JSON request সামলায়। একটি S3 event (বা "complete" callback) queue-এর মাধ্যমে post-processing — virus scan, transcoding — শুরু করে।
            2. **API-কে যদি byte proxy করতেই হয়** (compliance, encryption, inspection): **backpressure সহ stream করো।** Memory storage নয়; request stream-কে একটি byte-limit `Transform`-এর মধ্য দিয়ে এমন multipart uploader-এ pipe করো যার memory সীমিত (`queueSize × partSize`, যেমন 4 × 8 MiB ≈ upload প্রতি 32 MiB)। S3 ধীর হলে `pipeline()` client socket থেকে পড়া থামিয়ে দেয়, যা TCP flow control-এর মাধ্যমে client-কেও ধীর করে।
            3. **Service রক্ষা করো:** instance প্রতি concurrent upload সীমিত করো (ভরে গেলে `503`/`429`), সর্বোচ্চ size আগেই (`Content-Length` check) এবং stream চলাকালীনও enforce করো, ধীর client-এর জন্য timeout দাও, upload-কে dedicated instance-এ চালাও যাতে main API-কে বঞ্চিত না করে, আর failure-এ multipart upload abort করো (সাথে অসম্পূর্ণ upload পরিষ্কারের জন্য S3 lifecycle rule)।
        """,
        quick_en=r"""Root cause: `multer.memoryStorage()` buffers each whole file (up to 2 GB) in memory with no backpressure, so concurrent uploads exhaust RAM and stall the event loop. Best fix: presigned direct-to-S3 uploads; if the API must proxy, stream with `pipeline()` into a bounded multipart upload and cap concurrent uploads.""",
        quick_bn=r"""Root cause: `multer.memoryStorage()` প্রতিটা পুরো file (2 GB পর্যন্ত) কোনো backpressure ছাড়াই memory-তে রাখে, তাই একসাথে অনেক upload হলে RAM শেষ হয় আর event loop আটকে যায়। সেরা সমাধান: presigned URL দিয়ে সরাসরি S3-তে upload; API-কে proxy করতেই হলে `pipeline()` দিয়ে সীমিত-memory-র multipart upload-এ stream করো আর একসাথে upload-এর সংখ্যা সীমিত রাখো।""",
        ex_en=r"""
            - **Why other requests time out:** huge Buffers live outside the V8 heap but still trigger GC work and memory pressure; copying and concatenating them is synchronous CPU work on the main thread. One endpoint's design flaw becomes a whole-service outage.
            - **Memory budget math:** with streaming, memory ≈ concurrent uploads × (stream buffers + `queueSize × partSize`). 20 uploads × ~32 MiB ≈ 640 MiB — predictable, and tunable with the concurrency cap.
            - **Validate MIME type by content**, not by the client's `Content-Type` or file name; for presigned uploads, scan after upload and only mark the file "available" once checks pass.
            - **Presigned URL security:** short expiry, exact key chosen by the server (never client-supplied paths), content-length/type conditions where supported, and a private bucket.
            - **Failure handling:** a client disconnect destroys the request stream → `pipeline` rejects → abort the multipart upload so you don't pay for orphaned parts.
            - **Trade-off:** presigned uploads add client complexity (multipart, retries, progress) but remove the largest load from your servers; proxying keeps control centralised at the cost of bandwidth and compute.
        """,
        ex_bn=r"""
            - **অন্য request কেন timeout হয়:** বিশাল Buffer V8 heap-এর বাইরে থাকলেও GC-র কাজ আর memory চাপ তৈরি করে; এগুলো copy ও জোড়া লাগানো main thread-এ synchronous CPU কাজ। একটি endpoint-এর design-এর ত্রুটি পুরো service-এর outage হয়ে দাঁড়ায়।
            - **Memory budget-এর হিসাব:** streaming-এ memory ≈ concurrent upload × (stream buffer + `queueSize × partSize`)। 20টি upload × ~32 MiB ≈ 640 MiB — অনুমানযোগ্য, আর concurrency cap দিয়ে নিয়ন্ত্রণযোগ্য।
            - **MIME type content দেখে validate করো**, client-এর `Content-Type` বা file-এর নাম দেখে নয়; presigned upload-এ upload-এর পরে scan করো এবং check pass হলেই file-কে "available" চিহ্নিত করো।
            - **Presigned URL-এর security:** কম সময়ের expiry, server-এর ঠিক করা নির্দিষ্ট key (client-এর দেওয়া path কখনো নয়), যেখানে সম্ভব content-length/type condition, আর private bucket।
            - **Failure handling:** client disconnect হলে request stream destroy হয় → `pipeline` reject করে → multipart upload abort করো, যাতে orphan part-এর জন্য টাকা দিতে না হয়।
            - **Trade-off:** presigned upload client-এর জটিলতা বাড়ায় (multipart, retry, progress) কিন্তু server থেকে সবচেয়ে বড় load সরিয়ে দেয়; proxy করলে নিয়ন্ত্রণ কেন্দ্রীভূত থাকে, বিনিময়ে bandwidth আর compute খরচ।
        """,
        tip_en=r"""Name the root cause in one phrase — "buffering instead of streaming, so no backpressure" — then present presigned uploads as the first choice and streaming as the fallback. Quantifying memory (`queueSize × partSize`) is what makes the answer convincing.""",
        tip_bn=r"""এক বাক্যে মূল কারণ বলো — "stream না করে buffer করা, তাই backpressure নেই" — তারপর প্রথম পছন্দ হিসেবে presigned upload আর বিকল্প হিসেবে streaming উপস্থাপন করো। Memory-র হিসাব (`queueSize × partSize`) দিতে পারলেই উত্তরটা বিশ্বাসযোগ্য হয়।""",
        mist_en=r""""Fixing" it by raising container memory or `--max-old-space-size`, switching to disk storage without limits (fills the disk instead), or trusting the client's `Content-Type`.""",
        mist_bn=r"""Container memory বা `--max-old-space-size` বাড়িয়ে "ঠিক" করা, কোনো limit ছাড়া disk storage-এ যাওয়া (তখন disk ভরে যায়), অথবা client-এর `Content-Type` বিশ্বাস করা।""",
        code=r"""
            import express from 'express';
            import { randomUUID } from 'node:crypto';
            import { PassThrough, Transform } from 'node:stream';
            import { pipeline } from 'node:stream/promises';
            import { S3Client } from '@aws-sdk/client-s3';
            import { Upload } from '@aws-sdk/lib-storage';

            const s3 = new S3Client({});
            const MAX_BYTES = 2 * 1024 ** 3; // 2 GiB

            function limitBytes(max) {
              let seen = 0;
              return new Transform({
                transform(chunk, _encoding, callback) {
                  seen += chunk.length;
                  if (seen > max) {
                    return callback(Object.assign(new Error('Payload too large'), { status: 413 }));
                  }
                  callback(null, chunk);
                },
              });
            }

            const app = express();

            // No body parser on this route: we stream the raw request
            app.put('/uploads', async (req, res) => {
              const declared = Number(req.get('content-length') ?? 0);
              if (declared > MAX_BYTES) return res.sendStatus(413); // reject early when size is known

              const body = new PassThrough();
              const upload = new Upload({
                client: s3,
                params: { Bucket: process.env.UPLOAD_BUCKET, Key: `raw/${randomUUID()}`, Body: body },
                partSize: 8 * 1024 * 1024, // 8 MiB parts
                queueSize: 4,              // => at most ~32 MiB buffered per upload
                leavePartsOnError: false,
              });

              try {
                await Promise.all([pipeline(req, limitBytes(MAX_BYTES), body), upload.done()]);
              } catch (err) {
                await upload.abort().catch(() => {}); // clean up the multipart upload
                throw err; // Express 5 forwards it to the error handler (413 / 500)
              }
              res.status(201).json({ ok: true });
            });
        """,
        lang="javascript",
        follow=[
            ("How would you cap concurrent uploads per instance and what status code would you return?", "Instance প্রতি concurrent upload কীভাবে সীমিত করবে, আর কোন status code return করবে?"),
            ("How do you resume a failed 2 GB upload from a mobile client?", "Mobile client থেকে fail হওয়া 2 GB upload কীভাবে resume করবে?"),
            ("Where would you run virus scanning in the presigned-URL design?", "Presigned-URL design-এ virus scanning কোথায় চালাবে?"),
        ],
        related=["node-005", "node-011"],
        refs=[NODE_BACKPRESSURE, NODE_STREAM, AWS_S3_PRESIGNED],
    ),
]

if __name__ == "__main__":
    save("nodejs", "b5", QUESTIONS)
