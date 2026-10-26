import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NODE_ENV_VARS = ("Node.js API — Environment variables (.env support)", "https://nodejs.org/api/environment_variables.html")
NODE_CLI = ("Node.js API — Command-line options (--env-file)", "https://nodejs.org/api/cli.html")
NODE_PROCESS = ("Node.js API — process", "https://nodejs.org/api/process.html")
NODE_EVENTS = ("Node.js API — Events", "https://nodejs.org/api/events.html")
NODE_WORKERS = ("Node.js API — Worker threads", "https://nodejs.org/api/worker_threads.html")
NODE_CLUSTER = ("Node.js API — Cluster", "https://nodejs.org/api/cluster.html")
NODE_CHILD = ("Node.js API — Child process", "https://nodejs.org/api/child_process.html")
NODE_DONT_BLOCK = ("Node.js Learn — Don't Block the Event Loop (or the Worker Pool)", "https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop")
NODE_CRYPTO = ("Node.js API — Crypto (pbkdf2)", "https://nodejs.org/api/crypto.html")
NODE_HTTP = ("Node.js API — HTTP (server.close, keepAliveTimeout)", "https://nodejs.org/api/http.html")
PISCINA = ("Piscina — worker thread pool (GitHub)", "https://github.com/piscinajs/piscina")
ALB_DOCS = ("AWS — Troubleshoot Application Load Balancers (HTTP 502, keep-alive)", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html")
K8S_POD_LIFECYCLE = ("Kubernetes — Pod lifecycle (termination)", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/")

QUESTIONS = [
    # ------------------------------------------------------------------ node-015
    Q(
        id="node-015", sub="Processes & Environment Variables", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["env-vars", "env-file", "configuration", "process-env", "twelve-factor"],
        ver="Node.js 26 LTS / 24; zod 4.x (example)", vs=True, status="stable",
        q_en=r"""How do you manage environment variables and configuration in a Node.js 24 application? Do you still need the `dotenv` package?""",
        q_bn=r"""Node.js 24 application-এ environment variable আর configuration কীভাবে manage করো? এখনও কি `dotenv` package লাগে?""",
        a_en=r"""
            Anything that changes between environments — database URL, API keys, port, feature flags — comes from environment variables through `process.env`, not from code.

            For local development Node can load a `.env` file itself: `node --env-file=.env server.js` (or `--env-file-if-exists`), or `process.loadEnvFile()` from code. So for normal apps I don't need `dotenv` anymore.

            Three rules I always follow:
            - **Everything in `process.env` is a string** — `'false'` is truthy and `'3000'` isn't a number — so I parse and validate config **once at startup** (for example with a zod schema) and exit immediately if something required is missing.
            - **Real environment variables win** over values in the `.env` file, so the platform can override local defaults.
            - **Never commit secrets.** Commit a `.env.example`; in production, inject values from the platform or a secrets manager instead of baking a `.env` into the image.
        """,
        a_bn=r"""
            Environment অনুযায়ী যা বদলায় — database URL, API key, port, feature flag — সেগুলো code থেকে নয়, `process.env`-এর মাধ্যমে environment variable থেকে আসে।

            Local development-এ Node নিজেই `.env` file load করতে পারে: `node --env-file=.env server.js` (বা `--env-file-if-exists`), অথবা code থেকে `process.loadEnvFile()`। তাই সাধারণ app-এ আমার আর `dotenv` লাগে না।

            তিনটি নিয়ম আমি সবসময় মানি:
            - **`process.env`-এর সবকিছু string** — `'false'` truthy, আর `'3000'` কোনো number নয় — তাই config **startup-এর সময় একবার** parse ও validate করি (যেমন zod schema দিয়ে), আর দরকারি কিছু না থাকলে সাথে সাথে exit করি।
            - **আসল environment variable** `.env` file-এর value-এর উপর জয়ী হয়, ফলে platform local default override করতে পারে।
            - **কখনো secret commit করি না।** একটি `.env.example` commit করি; production-এ image-এর ভেতরে `.env` না রেখে platform বা secrets manager থেকে value inject করি।
        """,
        quick_en=r"""Read config from `process.env`; for local development Node loads a `.env` file itself with `--env-file=.env` or `process.loadEnvFile()`, so `dotenv` isn't needed anymore. Every value is a string, so parse and validate config once at startup, and never commit secrets (commit a `.env.example`).""",
        quick_bn=r"""Config `process.env` থেকে পড়ো; local development-এ Node নিজেই `--env-file=.env` বা `process.loadEnvFile()` দিয়ে `.env` file load করতে পারে, তাই এখন আর `dotenv` লাগে না। সব value string, তাই startup-এ একবার config parse ও validate করো, আর secret কখনো commit কোরো না (শুধু `.env.example` commit করো)।""",
        ex_en=r"""
            - `--env-file` and `--env-file-if-exists` stopped being experimental in v24.10 / v22.21; the `.env` utilities are documented as stable in current docs. Multi-line values are supported.
            - **Fail fast:** a missing `DATABASE_URL` should crash at boot with a clear message, not at 3 a.m. on the first query.
            - **Freeze the config object** and import it everywhere instead of reading `process.env` all over the code base — easier to test and to audit.
            - `NODE_ENV=production` still matters: many libraries (Express included) switch to production behaviour based on it, e.g. hiding stack traces in the default error handler.
            - Reading `process.env` is relatively slow compared with a normal object property, which is one more reason to read it once.
        """,
        ex_bn=r"""
            - `--env-file` ও `--env-file-if-exists` v24.10 / v22.21-এ experimental থেকে বের হয়েছে; current docs-এ `.env` utility-গুলো stable হিসেবে উল্লেখ করা আছে। Multi-line value-ও support করে।
            - **Fail fast:** `DATABASE_URL` না থাকলে প্রথম query-র সময় রাত ৩টায় নয়, boot-এর সময়ই স্পষ্ট message দিয়ে crash করা উচিত।
            - **Config object freeze করো** এবং পুরো code base-এ জায়গায় জায়গায় `process.env` না পড়ে সেটাই import করো — test ও audit দুটোই সহজ হয়।
            - `NODE_ENV=production` এখনও গুরুত্বপূর্ণ: Express সহ অনেক library এটা দেখে production আচরণে যায়, যেমন default error handler-এ stack trace লুকানো।
            - সাধারণ object property-র তুলনায় `process.env` পড়া তুলনামূলক ধীর — একবার পড়ার এটাও একটি কারণ।
        """,
        tip_en=r"""Mention "strings only → validate at startup" and "`--env-file` replaces dotenv". Those two points show both practical experience and up-to-date knowledge.""",
        tip_bn=r""""শুধু string → startup-এ validate" এবং "`--env-file` dotenv-এর জায়গা নিয়েছে" — এই দুটো কথা বলো। এতে বাস্তব অভিজ্ঞতা আর আপডেটেড জ্ঞান দুটোই বোঝা যায়।""",
        mist_en=r"""Writing `if (process.env.DEBUG)` and expecting `DEBUG=false` to disable it, or committing `.env` files with real credentials.""",
        mist_bn=r"""`if (process.env.DEBUG)` লিখে আশা করা যে `DEBUG=false` দিলে এটা বন্ধ হবে, অথবা আসল credential সহ `.env` file commit করা।""",
        code=r"""
            // config.js — parse once at startup, fail fast
            import { z } from 'zod';

            const schema = z.object({
              NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
              PORT: z.coerce.number().int().positive().default(3000),
              DATABASE_URL: z.url(),
              ENABLE_CACHE: z.stringbool().default(false), // 'true'/'false'/'1'/'0' -> boolean
            });

            const parsed = schema.safeParse(process.env);
            if (!parsed.success) {
              console.error('Invalid environment:', z.flattenError(parsed.error).fieldErrors);
              process.exit(1);
            }

            export const config = Object.freeze(parsed.data);

            // Run locally:  node --env-file=.env server.js
        """,
        lang="javascript",
        follow=[
            ("Where would you store secrets for a production deployment?", "Production deployment-এ secret কোথায় রাখবে?"),
            ("Why is `Boolean(process.env.FLAG)` a bug?", "`Boolean(process.env.FLAG)` কেন একটি bug?"),
        ],
        related=["node-003"],
        refs=[NODE_ENV_VARS, NODE_CLI, NODE_PROCESS],
    ),
    # ------------------------------------------------------------------ node-016
    Q(
        id="node-016", sub="EventEmitter", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["eventemitter", "error-event", "events", "crash"],
        ver="Version-independent (Node.js 26 LTS / 24)", vs=False, status="stable",
        q_en=r"""What happens when this code runs?""",
        q_bn=r"""এই code চালালে কী হবে?""",
        code=r"""
            const { EventEmitter } = require('node:events');

            const orders = new EventEmitter();
            orders.on('created', (order) => console.log('created', order.id));

            orders.emit('error', new Error('payment gateway timeout'));
            console.log('after emit');
        """,
        lang="javascript",
        options=[
            ("Nothing special: there is no `'error'` listener, so `emit()` returns `false` and `after emit` is logged", "বিশেষ কিছু হবে না: `'error'` listener নেই, তাই `emit()` `false` return করবে এবং `after emit` log হবে"),
            ("`emit()` throws the error, the process crashes and `after emit` is never logged", "`emit()` error-টি throw করবে, process crash করবে এবং `after emit` কখনো log হবে না"),
            ("The `'created'` listener receives the error object", "`'created'` listener error object-টি পাবে"),
            ("A `MaxListenersExceededWarning` is printed and execution continues", "একটি `MaxListenersExceededWarning` print হবে এবং execution চলতে থাকবে"),
        ],
        correct=1,
        a_en=r"""
            `emit()` throws. `'error'` is a special event: if it is emitted and no `'error'` listener is registered, the EventEmitter throws the error, so the process crashes (exit code 1) and `after emit` never runs.
        """,
        a_bn=r"""
            `emit()` throw করবে। `'error'` একটি বিশেষ event: এটা emit হলে এবং কোনো `'error'` listener না থাকলে EventEmitter error-টি throw করে, ফলে process crash করে (exit code 1) এবং `after emit` কখনো চলে না।
        """,
        quick_en=r"""`emit()` throws: `'error'` is a special event, and if no `'error'` listener is registered the EventEmitter throws the error, so the process crashes with exit code 1 and `after emit` never runs.""",
        quick_bn=r"""`emit()` নিজেই throw করে: `'error'` একটা বিশেষ event, আর কোনো `'error'` listener না থাকলে EventEmitter error-টা throw করে, ফলে process exit code 1 দিয়ে crash করে এবং `after emit` কখনো চলে না।""",
        ex_en=r"""
            Option A is tempting because that *is* what happens for every other event name — emitting an event nobody listens to just returns `false`. Only `'error'` gets this "throw if unhandled" treatment, so failures can't be silently lost.

            Practical consequences:
            - Always attach an `'error'` listener to emitters you own and to streams, sockets, and servers — an unhandled stream error is a classic production crash.
            - If you emit a non-`Error` value with no listener, Node throws an `ERR_UNHANDLED_ERROR` wrapping it.
            - `events.once(emitter, 'x')` returns a promise that rejects if `'error'` is emitted first, which is handy in async code.
            - The `MaxListenersExceededWarning` (option D) is unrelated: it appears when more than 10 listeners are added for one event, a hint of a listener leak.
        """,
        ex_bn=r"""
            Option A প্রলোভনের, কারণ অন্য সব event-এর ক্ষেত্রে *ঠিক এটাই* হয় — কেউ listen না করলে emit শুধু `false` return করে। কেবল `'error'`-এর জন্যই "handle না হলে throw" নিয়ম, যাতে failure চুপচাপ হারিয়ে না যায়।

            বাস্তব প্রভাব:
            - নিজের emitter-এ, আর stream, socket, server-এ সবসময় `'error'` listener লাগাও — unhandled stream error production-এ crash-এর classic কারণ।
            - Listener ছাড়া non-`Error` value emit করলে Node সেটাকে wrap করে `ERR_UNHANDLED_ERROR` throw করে।
            - `events.once(emitter, 'x')` একটি promise দেয়, যা আগে `'error'` emit হলে reject করে — async code-এ খুব কাজের।
            - `MaxListenersExceededWarning` (option D)-এর সাথে এর সম্পর্ক নেই: এক event-এ 10টির বেশি listener যোগ হলে এটা দেখায়, যা listener leak-এর ইঙ্গিত।
        """,
        tip_en=r"""Follow up with the real-world lesson: "this is why every stream and socket needs an error handler — or use `pipeline`, which wires errors for you".""",
        tip_bn=r"""বাস্তব শিক্ষাটা যোগ করো: "এজন্যই প্রতিটি stream ও socket-এ error handler লাগে — অথবা `pipeline` ব্যবহার করো, যা নিজেই error সামলায়"।""",
        refs=[NODE_EVENTS],
    ),
    # ------------------------------------------------------------------ node-017
    Q(
        id="node-017", sub="Worker Threads & Clustering", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["worker-threads", "cluster", "child-process", "concurrency", "multi-core"],
        ver="Node.js 26 LTS / 24", vs=False, status="stable",
        q_en=r"""Compare `worker_threads`, `cluster` and `child_process`. When would you use each one?""",
        q_bn=r"""`worker_threads`, `cluster` আর `child_process`-এর তুলনা করো। কোনটা কখন ব্যবহার করবে?""",
        a_en=r"""
            - **`worker_threads`** — extra threads *inside the same process*. Each worker has its own V8 isolate and event loop; they talk via `postMessage` and can transfer `ArrayBuffer`s or share a `SharedArrayBuffer`. I use them for **CPU-heavy JavaScript** (image processing, parsing huge files, compression in JS) so the main event loop stays responsive — always through a pool such as Piscina, because creating a worker per task is expensive.
            - **`cluster`** — forks **several processes of the same server** that share one listening port; the primary distributes incoming connections. It's a way to use all CPU cores for an HTTP server on one machine. No shared memory, so sessions, caches and rate-limit counters must live in Redis or a database. In Kubernetes/ECS I usually skip it and run one process per container.
            - **`child_process`** — runs **another program** (`ffmpeg`, `git`, a Python script) or a separate Node script with `fork()` and an IPC channel. Good for using external tools or isolating risky work in a separate process.

            Rule of thumb: CPU-bound JS → worker threads; more throughput from cores → cluster or more containers; external binaries → child processes.
        """,
        a_bn=r"""
            - **`worker_threads`** — *একই process-এর ভেতরে* বাড়তি thread। প্রতিটি worker-এর নিজস্ব V8 isolate ও event loop থাকে; এরা `postMessage` দিয়ে কথা বলে এবং `ArrayBuffer` transfer বা `SharedArrayBuffer` share করতে পারে। আমি এগুলো ব্যবহার করি **CPU-heavy JavaScript**-এর জন্য (image processing, বিশাল file parse করা, JS-এ compression), যাতে main event loop responsive থাকে — সবসময় Piscina-র মতো pool-এর মাধ্যমে, কারণ প্রতি task-এ নতুন worker বানানো ব্যয়বহুল।
            - **`cluster`** — **একই server-এর কয়েকটি process** fork করে, যারা একটি listening port share করে; primary process আসা connection ভাগ করে দেয়। এক machine-এ HTTP server-এর জন্য সব CPU core ব্যবহারের উপায়। Shared memory নেই, তাই session, cache, rate-limit counter Redis বা database-এ রাখতে হয়। Kubernetes/ECS-এ আমি সাধারণত এটা বাদ দিয়ে প্রতি container-এ একটি process চালাই।
            - **`child_process`** — **অন্য কোনো program** চালায় (`ffmpeg`, `git`, Python script), অথবা `fork()` দিয়ে IPC channel সহ আলাদা Node script। External tool ব্যবহার বা ঝুঁকিপূর্ণ কাজ আলাদা process-এ isolate করার জন্য ভালো।

            মোটা দাগে: CPU-bound JS → worker thread; core থেকে বেশি throughput → cluster বা বেশি container; external binary → child process।
        """,
        quick_en=r"""`worker_threads` are extra threads in one process for CPU-heavy JavaScript; `cluster` forks several processes of the same server that share one port; `child_process` runs another program like `ffmpeg`. Rule: CPU-bound JS → workers, more cores for HTTP → cluster or containers, external tools → child processes.""",
        quick_bn=r"""`worker_threads` হলো একটা process-এর ভেতরে CPU-heavy JavaScript-এর জন্য বাড়তি thread; `cluster` একই server-এর কয়েকটা process fork করে, যারা একটা port share করে; `child_process` অন্য program চালায়, যেমন `ffmpeg`। নিয়ম: CPU-bound JS → worker, HTTP-র জন্য বেশি core → cluster বা container, বাইরের tool → child process।""",
        ex_en=r"""
            - **Workers don't speed up I/O.** The Node docs say it plainly: built-in async I/O is more efficient than workers can be.
            - **Messages are copied** with the structured clone algorithm unless you transfer them; sending huge objects back and forth can cost more than the work itself.
            - **Isolation:** a crashing worker thread emits `'error'` on the `Worker` object; a fatal native crash still takes down the whole process. Separate processes (cluster/child) isolate failures better.
            - **Memory:** each worker or process has its own heap — 8 cluster workers means 8 heaps and 8 database pools.
            - **Security:** with `child_process`, prefer `execFile`/`spawn` with an argument array. `exec` runs a shell, so user input in the command string means command injection.
        """,
        ex_bn=r"""
            - **Worker I/O দ্রুত করে না।** Node docs স্পষ্ট বলে: built-in async I/O worker-এর চেয়ে বেশি efficient।
            - **Message copy হয়** structured clone algorithm দিয়ে, যদি না transfer করো; বিশাল object বারবার আদান-প্রদান করলে আসল কাজের চেয়েও বেশি খরচ হতে পারে।
            - **Isolation:** worker thread crash করলে `Worker` object-এ `'error'` emit হয়; কিন্তু native fatal crash পুরো process-কেই বন্ধ করে দেয়। আলাদা process (cluster/child) failure ভালোভাবে isolate করে।
            - **Memory:** প্রতিটি worker বা process-এর নিজস্ব heap — 8টি cluster worker মানে 8টি heap আর 8টি database pool।
            - **Security:** `child_process`-এ argument array সহ `execFile`/`spawn` ব্যবহার করো। `exec` shell চালায়, তাই command string-এ user input থাকলে command injection হয়।
        """,
        tip_en=r"""Anchor each option to a concrete job ("resize images → worker pool", "use 8 cores → cluster or 8 containers", "call ffmpeg → spawn"). Concrete mapping beats abstract definitions.""",
        tip_bn=r"""প্রতিটি option-কে একটি বাস্তব কাজের সাথে জুড়ে দাও ("image resize → worker pool", "8টি core ব্যবহার → cluster বা 8টি container", "ffmpeg চালানো → spawn")। বিমূর্ত definition-এর চেয়ে বাস্তব mapping বেশি কার্যকর।""",
        mist_en=r"""Using worker threads to "speed up" database calls, or assuming cluster workers share in-memory state such as sessions.""",
        mist_bn=r"""Database call "দ্রুত" করতে worker thread ব্যবহার করা, অথবা ধরে নেওয়া যে cluster worker-রা session-এর মতো in-memory state share করে।""",
        code=r"""
            import { Worker } from 'node:worker_threads';
            import { execFile } from 'node:child_process';
            import { promisify } from 'node:util';

            // 1) CPU-heavy JS on a worker thread (use a pool like Piscina in real apps)
            export function resizeInWorker(imagePath) {
              return new Promise((resolve, reject) => {
                const worker = new Worker(new URL('./resize-worker.js', import.meta.url), {
                  workerData: { imagePath },
                });
                worker.once('message', resolve);
                worker.once('error', reject);
                worker.once('exit', (code) => {
                  if (code !== 0) reject(new Error(`worker exited with code ${code}`));
                });
              });
            }

            // 2) External program as a child process — argument array, no shell
            const run = promisify(execFile);
            export async function probeVideo(filePath) {
              const { stdout } = await run('ffprobe', ['-v', 'error', '-show_format', '-of', 'json', filePath]);
              return JSON.parse(stdout);
            }
        """,
        lang="javascript",
        follow=[
            ("How do worker threads share memory, and when is that worth the complexity?", "Worker thread কীভাবে memory share করে, আর কখন সেই জটিলতা নেওয়ার মতো?"),
            ("Why might you not use `cluster` inside a Docker container?", "Docker container-এর ভেতরে কেন `cluster` ব্যবহার না-ও করতে পারো?"),
        ],
        related=["node-018", "node-026"],
        refs=[NODE_WORKERS, NODE_CLUSTER, NODE_CHILD],
    ),
    # ------------------------------------------------------------------ node-018
    Q(
        id="node-018", sub="CPU-Intensive Tasks", diff="medium", type="scenario",
        prio="high", market="both", mins=6,
        tags=["cpu-bound", "worker-pool", "piscina", "job-queue", "event-loop"],
        ver="Node.js 26 LTS / 24; Express 5.x; Piscina 5 (example)", vs=False, status="stable",
        q_en=r"""An Express endpoint `POST /reports` builds a PDF report from about 200k rows. While one report is being generated (around 3 seconds), every other request on that instance — even `/health` — stalls. What are your options, and which would you choose?""",
        q_bn=r"""একটি Express endpoint `POST /reports` প্রায় 200k row থেকে PDF report বানায়। একটি report তৈরি হওয়ার সময় (প্রায় ৩ সেকেন্ড) ওই instance-এর বাকি সব request — এমনকি `/health`-ও — আটকে থাকে। তোমার কাছে কী কী option আছে, আর কোনটা বেছে নেবে?""",
        a_en=r"""
            First I'd clarify: how often are reports requested, how big can they get, and does the user need the file in the same HTTP response? Then the options:

            1. **Make the work cheaper.** Push aggregation into the database (`GROUP BY` instead of looping over 200k rows in JS), stream rows with a cursor instead of loading them all, and stream the output.
            2. **Offload to a worker-thread pool** (e.g. Piscina) in the same service. The main event loop stays free; throughput is limited by spare cores. Good when reports take seconds and users expect the file immediately.
            3. **Make it asynchronous with a job queue.** Return `202 Accepted` with a job ID, generate the report in a separate worker service, upload it to object storage, and let the client poll or get notified. Best for heavy, bursty or long-running reports.
            4. **Chunk and yield** with `setImmediate` between batches — only a stop-gap; it keeps the loop responsive but makes the report slower.

            My choice: fix the data access first (DB aggregation + streaming), then use a worker pool with a bounded queue for typical reports, and move to the job-queue design if reports grow or get frequent. In all cases I'd add per-user rate limits and a timeout.
        """,
        a_bn=r"""
            প্রথমে আমি জেনে নেব: report কত ঘন ঘন চাওয়া হয়, কত বড় হতে পারে, আর user কি একই HTTP response-এ file চায়? তারপর option-গুলো:

            1. **কাজটা সস্তা করা।** Aggregation database-এ পাঠানো (JS-এ 200k row loop না করে `GROUP BY`), সব row একসাথে load না করে cursor দিয়ে stream করা, আর output-ও stream করা।
            2. **একই service-এ worker-thread pool-এ পাঠানো** (যেমন Piscina)। Main event loop মুক্ত থাকে; throughput খালি core-এর সংখ্যায় সীমিত। Report কয়েক সেকেন্ডের হলে এবং user সাথে সাথে file চাইলে ভালো।
            3. **Job queue দিয়ে asynchronous করা।** Job ID সহ `202 Accepted` return করা, আলাদা worker service-এ report বানিয়ে object storage-এ upload করা, আর client poll করবে বা notification পাবে। ভারী, burst-প্রবণ বা দীর্ঘ report-এর জন্য সেরা।
            4. **ভাগ করে yield করা** — batch-এর মাঝে `setImmediate` দিয়ে। এটা কেবল সাময়িক সমাধান; loop responsive থাকে কিন্তু report আরও ধীর হয়।

            আমার পছন্দ: আগে data access ঠিক করা (DB aggregation + streaming), তারপর সাধারণ report-এর জন্য bounded queue সহ worker pool, আর report বড় বা ঘন ঘন হলে job-queue design-এ যাওয়া। সব ক্ষেত্রেই per-user rate limit আর timeout যোগ করব।
        """,
        quick_en=r"""The 3-second synchronous job blocks the event loop for everyone. First make the work cheaper (aggregate in the database, stream rows), then move generation to a worker-thread pool, or to a job queue that returns `202 Accepted` if reports are heavy or bursty; chunking with `setImmediate` is only a stop-gap.""",
        quick_bn=r"""৩ সেকেন্ডের synchronous কাজটা সবার জন্য event loop আটকে দেয়। আগে কাজটা হালকা করো (database-এ aggregate করো, row stream করো), তারপর report তৈরি worker-thread pool-এ সরাও, আর report ভারী বা হঠাৎ অনেক হলে job queue ব্যবহার করে `202 Accepted` return করো; `setImmediate` দিয়ে টুকরো করা শুধু সাময়িক সমাধান।""",
        ex_en=r"""
            - **What does *not* help:** raising `UV_THREADPOOL_SIZE` (your JavaScript doesn't run in the libuv pool) or `cluster` alone (each process still blocks its own requests during a report).
            - **Bounded queues matter:** `maxQueue` in the pool means overload is rejected quickly (return `503` or `429`) instead of piling up memory and latency.
            - **Data transfer cost:** results come back from the worker by structured clone; returning a `Uint8Array`/`Buffer` is cheap compared with huge object graphs.
            - **Health checks** should be cheap and must not wait on the report path — but the real fix is not blocking the loop at all.
            - The async design also gives retries, progress tracking and protection against a user refreshing the page ten times.
        """,
        ex_bn=r"""
            - **যা সাহায্য *করে না*:** `UV_THREADPOOL_SIZE` বাড়ানো (তোমার JavaScript libuv pool-এ চলে না) বা শুধু `cluster` (report চলার সময় প্রতিটি process নিজের request block করে)।
            - **Bounded queue জরুরি:** pool-এ `maxQueue` থাকলে overload হলে memory আর latency জমতে না দিয়ে দ্রুত reject করা যায় (`503` বা `429` return)।
            - **Data transfer-এর খরচ:** worker থেকে result structured clone হয়ে আসে; বিশাল object graph-এর তুলনায় `Uint8Array`/`Buffer` return করা সস্তা।
            - **Health check** হালকা হওয়া উচিত এবং report path-এর উপর অপেক্ষা করা উচিত নয় — তবে আসল fix হলো loop একদমই block না করা।
            - Async design-এ retry, progress tracking, আর user দশবার page refresh করলে তার থেকে সুরক্ষাও পাওয়া যায়।
        """,
        tip_en=r"""Follow the scenario structure: clarify → list options → trade-offs → recommendation. Mentioning what does NOT work (thread pool size, cluster alone) is a strong signal of real understanding.""",
        tip_bn=r"""Scenario-র structure মেনে চলো: প্রশ্ন করে স্পষ্ট হওয়া → option-গুলো → trade-off → সুপারিশ। কী কাজ *করে না* (thread pool size, শুধু cluster) সেটা বলা সত্যিকারের বোঝাপড়ার শক্ত প্রমাণ।""",
        mist_en=r"""Wrapping the CPU work in `async`/`Promise` and assuming it no longer blocks — an async function still runs its synchronous code on the main thread.""",
        mist_bn=r"""CPU কাজকে `async`/`Promise`-এ মুড়ে দিয়ে ধরে নেওয়া যে এটা আর block করে না — async function-এর synchronous অংশ তখনও main thread-এই চলে।""",
        code=r"""
            // server.js
            import express from 'express';
            import { Piscina } from 'piscina';

            const pool = new Piscina({
              filename: new URL('./report-worker.js', import.meta.url).href,
              maxThreads: 4,   // roughly the cores you can spare
              maxQueue: 100,   // reject when overloaded instead of queueing forever
            });

            const app = express();
            app.use(express.json());

            app.post('/reports', async (req, res) => {
              const pdfBytes = await pool.run({ filters: req.body?.filters ?? {} });
              res.type('application/pdf').send(Buffer.from(pdfBytes));
            }); // Express 5 forwards a rejected promise (e.g. queue full) to the error handler

            app.listen(3000);

            // report-worker.js (runs on a worker thread)
            // export default async function ({ filters }) {
            //   const rows = await loadRows(filters);
            //   return renderPdf(rows); // CPU-heavy, but off the main thread
            // }
        """,
        lang="javascript",
        follow=[
            ("How would you report progress to the user for the async job approach?", "Async job approach-এ user-কে progress কীভাবে জানাবে?"),
            ("How would you size the worker pool on a 4-core container?", "4-core container-এ worker pool-এর size কীভাবে ঠিক করবে?"),
        ],
        related=["node-017", "node-006", "node-007"],
        refs=[NODE_DONT_BLOCK, NODE_WORKERS, PISCINA],
    ),
    # ------------------------------------------------------------------ node-019
    Q(
        id="node-019", sub="V8 & libuv", diff="hard", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["libuv", "thread-pool", "uv-threadpool-size", "crypto", "performance"],
        ver="Node.js 26 LTS / 24 (libuv default pool size 4)", vs=False, status="stable",
        q_en=r"""On an 8-core server with default settings, this code starts six `crypto.pbkdf2` calls at once. A single call takes about 1 second when run alone. Roughly when do the six callbacks fire?""",
        q_bn=r"""Default setting সহ একটি 8-core server-এ এই code একসাথে ছয়টি `crypto.pbkdf2` call শুরু করে। একা চালালে একটি call প্রায় ১ সেকেন্ড নেয়। ছয়টি callback মোটামুটি কখন fire হবে?""",
        code=r"""
            const crypto = require('node:crypto');

            const start = Date.now();
            for (let i = 1; i <= 6; i++) {
              crypto.pbkdf2('secret', 'salt', 600_000, 64, 'sha512', () => {
                console.log(`hash ${i}: ${Date.now() - start} ms`);
              });
            }
        """,
        lang="javascript",
        options=[
            ("All six after about 1 s, because each call gets its own thread", "ছয়টিই প্রায় ১ সেকেন্ড পরে, কারণ প্রতিটি call নিজস্ব thread পায়"),
            ("Four after about 1 s, and the remaining two after about 2 s", "চারটি প্রায় ১ সেকেন্ড পরে, আর বাকি দুটি প্রায় ২ সেকেন্ড পরে"),
            ("One after another at about 1 s, 2 s, 3 s … 6 s, because JavaScript is single-threaded", "একটার পর একটা — প্রায় ১, ২, ৩ … ৬ সেকেন্ডে, কারণ JavaScript single-threaded"),
            ("All six together after about 6 s, because the event loop is blocked until every hash finishes", "ছয়টিই একসাথে প্রায় ৬ সেকেন্ড পরে, কারণ সব hash শেষ না হওয়া পর্যন্ত event loop block থাকে"),
        ],
        correct=1,
        a_en=r"""
            Four after ~1 s, two after ~2 s. Async `crypto.pbkdf2` runs in libuv's thread pool, which has **4 threads by default**. The first four hashes run in parallel; the other two wait in the pool's queue until a thread frees up. The main thread stays free the whole time.
        """,
        a_bn=r"""
            চারটি ~১ সেকেন্ডে, দুটি ~২ সেকেন্ডে। Async `crypto.pbkdf2` চলে libuv-এর thread pool-এ, যেখানে **default 4টি thread**। প্রথম চারটি hash একসাথে চলে; বাকি দুটি thread খালি না হওয়া পর্যন্ত pool-এর queue-তে অপেক্ষা করে। পুরো সময় main thread মুক্ত থাকে।
        """,
        quick_en=r"""Four after about 1 s and two after about 2 s: async `crypto.pbkdf2` runs in libuv's thread pool, which has 4 threads by default, so the last two wait in its queue. The main thread stays free the whole time.""",
        quick_bn=r"""চারটা প্রায় 1 s পরে আর দুটো প্রায় 2 s পরে: async `crypto.pbkdf2` চলে libuv-এর thread pool-এ, যেখানে default 4টা thread, তাই শেষ দুটো queue-তে অপেক্ষা করে। পুরো সময় main thread কিন্তু free থাকে।""",
        ex_en=r"""
            Option C is the tempting wrong answer — it's what `pbkdf2Sync` would do: six sequential hashes on the main thread, blocking the event loop for ~6 s. The async version is parallel, but only up to the pool size.

            What senior engineers add:
            - **`UV_THREADPOOL_SIZE`** (max 1024) changes the pool size. Set it as an environment variable before the process starts (`UV_THREADPOOL_SIZE=8 node app.js`); the pool is created on first use, so setting `process.env` later in code is unreliable.
            - **More threads than cores doesn't help CPU-bound work** — six hashes on four cores still contend for CPU.
            - **The pool is shared:** `fs`, `dns.lookup`, `zlib` and these crypto calls all use it. A burst of password hashing can delay unrelated file reads and DNS lookups — a sneaky latency source.
            - Network sockets do not use the pool, so HTTP traffic itself isn't limited to four concurrent requests.
        """,
        ex_bn=r"""
            Option C হলো প্রলোভনের ভুল উত্তর — এটা `pbkdf2Sync`-এর আচরণ: main thread-এ ছয়টি hash পরপর, ~৬ সেকেন্ড event loop block। Async version parallel চলে, কিন্তু শুধু pool size পর্যন্ত।

            Senior engineer যা যোগ করে:
            - **`UV_THREADPOOL_SIZE`** (সর্বোচ্চ 1024) দিয়ে pool size বদলানো যায়। Process শুরুর আগেই environment variable হিসেবে দাও (`UV_THREADPOOL_SIZE=8 node app.js`); pool প্রথম ব্যবহারের সময় তৈরি হয়, তাই পরে code-এ `process.env` set করা নির্ভরযোগ্য নয়।
            - **Core-এর চেয়ে বেশি thread দিলে CPU-bound কাজে লাভ নেই** — চারটি core-এ ছয়টি hash তখনও CPU-র জন্য প্রতিযোগিতা করে।
            - **Pool shared:** `fs`, `dns.lookup`, `zlib` আর এই crypto call — সবাই এটা ব্যবহার করে। হঠাৎ অনেক password hashing হলে সম্পর্কহীন file read আর DNS lookup-ও দেরি হতে পারে — লুকানো latency-র উৎস।
            - Network socket pool ব্যবহার করে না, তাই HTTP traffic নিজে চারটি concurrent request-এ সীমিত নয়।
        """,
        tip_en=r"""After choosing B, contrast it with `pbkdf2Sync` and mention that the pool is shared with `fs` and `dns.lookup`. That turns a trivia answer into a production insight.""",
        tip_bn=r"""B বেছে নেওয়ার পর `pbkdf2Sync`-এর সাথে তুলনা করো এবং বলো যে pool `fs` আর `dns.lookup`-এর সাথে shared। এতে একটি trivia উত্তর production-এর অন্তর্দৃষ্টিতে পরিণত হয়।""",
        refs=[NODE_DONT_BLOCK, NODE_CRYPTO, NODE_CLI],
    ),
    # ------------------------------------------------------------------ node-020
    Q(
        id="node-020", sub="Graceful Shutdown", diff="extreme", type="scenario",
        prio="high", market="international", mins=18,
        tags=["zero-downtime", "deployment", "keep-alive", "graceful-shutdown", "migrations", "kubernetes"],
        ver="Node.js 26 LTS / 24; Kubernetes + AWS ALB (example platform)", vs=False, status="stable",
        q_en=r"""Your Node.js API runs as several containers behind a load balancer (for example Kubernetes with an AWS ALB). Every deploy causes a burst of 502 errors and a few failed requests, and occasionally errors right after a database migration. How do you achieve truly zero-downtime deployments?""",
        q_bn=r"""তোমার Node.js API একটি load balancer-এর পেছনে কয়েকটি container হিসেবে চলে (যেমন AWS ALB সহ Kubernetes)। প্রতিটি deploy-তে একঝাঁক 502 error আর কিছু failed request দেখা যায়, আর মাঝে মাঝে database migration-এর ঠিক পরে error হয়। সত্যিকারের zero-downtime deployment কীভাবে নিশ্চিত করবে?""",
        a_en=r"""
            *(Advanced, senior-level answer.)* Zero downtime needs four things to line up: traffic shifting, graceful shutdown, connection handling, and backward-compatible changes.

            1. **Rolling update that never removes capacity first:** `maxUnavailable: 0`, `maxSurge: 1`, and a readiness probe that turns green only when the app can really serve (DB pool connected, config loaded).
            2. **Graceful shutdown on `SIGTERM`:** fail the readiness check, wait a few seconds so the load balancer and endpoints stop sending new requests, then `server.close()` to finish in-flight requests, close DB/Redis pools and exit — all within the termination grace period, with a hard timeout as a safety net.
            3. **Fix the keep-alive race:** the ALB reuses idle connections for up to 60 s by default, but Node's `server.keepAliveTimeout` is 5 s. If Node closes an idle socket just as the ALB sends a request on it, the ALB returns 502. Set `keepAliveTimeout` above the load balancer's idle timeout (e.g. 65 s) and `headersTimeout` a bit higher.
            4. **Backward-compatible changes:** during a rollout, old and new versions run at the same time against the same database. Use expand/contract migrations: add the new column (nullable) first, deploy code that writes both and reads the new one, backfill, and drop the old column in a later release. Same idea for API contracts and queue message formats; use feature flags for risky behaviour.
            5. **Verify and roll back automatically:** canary or blue/green with error-rate and latency checks, plus smoke tests.
        """,
        a_bn=r"""
            *(Advanced, senior-level উত্তর।)* Zero downtime-এর জন্য চারটি জিনিস মেলাতে হয়: traffic সরানো, graceful shutdown, connection handling, আর backward-compatible পরিবর্তন।

            1. **এমন rolling update যা আগে capacity কমায় না:** `maxUnavailable: 0`, `maxSurge: 1`, আর এমন readiness probe যা app সত্যিই serve করতে পারলে (DB pool connected, config loaded) তবেই সবুজ হয়।
            2. **`SIGTERM`-এ graceful shutdown:** readiness check fail করানো, কয়েক সেকেন্ড অপেক্ষা যাতে load balancer ও endpoint নতুন request পাঠানো বন্ধ করে, তারপর `server.close()` দিয়ে চলমান request শেষ করা, DB/Redis pool বন্ধ করে exit — সবকিছু termination grace period-এর মধ্যে, safety net হিসেবে একটি hard timeout সহ।
            3. **Keep-alive race ঠিক করা:** ALB default-ভাবে 60 s পর্যন্ত idle connection reuse করে, কিন্তু Node-এর `server.keepAliveTimeout` 5 s। ALB যখন একটি idle socket-এ request পাঠাচ্ছে ঠিক তখনই Node সেটা বন্ধ করলে ALB 502 return করে। `keepAliveTimeout` load balancer-এর idle timeout-এর চেয়ে বেশি রাখো (যেমন 65 s), আর `headersTimeout` তার চেয়ে একটু বেশি।
            4. **Backward-compatible পরিবর্তন:** rollout-এর সময় পুরনো ও নতুন version একই database-এর সাথে একসাথে চলে। Expand/contract migration ব্যবহার করো: আগে নতুন column (nullable) যোগ, তারপর এমন code deploy যা দুটোতেই লেখে আর নতুনটা পড়ে, backfill, আর পরের release-এ পুরনো column drop। API contract আর queue message format-এর ক্ষেত্রেও একই নীতি; ঝুঁকিপূর্ণ আচরণের জন্য feature flag।
            5. **যাচাই ও স্বয়ংক্রিয় rollback:** error rate আর latency check সহ canary বা blue/green, সাথে smoke test।
        """,
        quick_en=r"""Zero downtime needs a rolling update that never removes capacity first, graceful `SIGTERM` handling (fail readiness, wait, `server.close()`), a `keepAliveTimeout` above the load balancer's idle timeout to stop 502s, and backward-compatible expand/contract migrations, plus canaries with automatic rollback.""",
        quick_bn=r"""Zero downtime-এর জন্য লাগে: এমন rolling update যেটা আগে capacity কমায় না, `SIGTERM`-এ graceful shutdown (readiness fail, একটু অপেক্ষা, `server.close()`), 502 ঠেকাতে load balancer-এর idle timeout-এর চেয়ে বড় `keepAliveTimeout`, আর backward-compatible expand/contract migration, সাথে canary ও automatic rollback।""",
        ex_en=r"""
            - **Why the readiness delay:** `SIGTERM` and endpoint removal happen in parallel in Kubernetes. If the app closes its listener immediately, requests that were already routed to it get connection errors. A short sleep (or a `preStop` hook) closes that gap.
            - **Since Node 19, `server.close()` also closes idle keep-alive connections** — but only those idle at that moment. A socket that is still serving a request stays open for `keepAliveTimeout` (65 s here) after its response, so the close callback would wait until the hard deadline. Send `Connection: close` while draining and call `server.closeIdleConnections()` repeatedly; `server.closeAllConnections()` force-closes the rest at the deadline.
            - **Long-lived connections** (WebSockets, SSE) won't drain on their own — send a reconnect message and let clients reconnect with jittered backoff.
            - **PM2 on a single VM:** `pm2 reload` in cluster mode restarts workers one by one, but you still need graceful shutdown and backward-compatible migrations.
            - **Destructive migrations** (rename/drop column, add `NOT NULL` without default) in the same deploy as the code change are the most common cause of "errors right after migration".
        """,
        ex_bn=r"""
            - **Readiness delay কেন:** Kubernetes-এ `SIGTERM` আর endpoint থেকে সরানো একসাথে ঘটে। App সাথে সাথে listener বন্ধ করলে যে request ইতিমধ্যে তার দিকে route হয়েছে সেগুলো connection error পায়। ছোট একটি sleep (বা `preStop` hook) এই ফাঁক বন্ধ করে।
            - **Node 19 থেকে `server.close()` idle keep-alive connection-ও বন্ধ করে** — তবে শুধু সেই মুহূর্তে idle থাকা connection। যে socket তখনো কোনো request serve করছে, response-এর পরও সেটা `keepAliveTimeout` (এখানে 65 s) পর্যন্ত খোলা থাকে, ফলে close callback hard deadline পর্যন্ত অপেক্ষা করত। Draining-এর সময় `Connection: close` পাঠাও আর বারবার `server.closeIdleConnections()` call করো; deadline-এ বাকিগুলো জোর করে বন্ধ করতে `server.closeAllConnections()` আছে।
            - **দীর্ঘস্থায়ী connection** (WebSocket, SSE) নিজে থেকে drain হয় না — reconnect message পাঠাও এবং client-কে jitter সহ backoff দিয়ে reconnect করতে দাও।
            - **একটি VM-এ PM2:** cluster mode-এ `pm2 reload` worker-গুলো একে একে restart করে, কিন্তু তবুও graceful shutdown আর backward-compatible migration লাগবে।
            - **Destructive migration** (column rename/drop, default ছাড়া `NOT NULL` যোগ) code change-এর একই deploy-তে করা "migration-এর ঠিক পরে error"-এর সবচেয়ে সাধারণ কারণ।
        """,
        tip_en=r"""Walk the lifecycle of one pod during a deploy: start → ready → receiving traffic → SIGTERM → not ready → drain → exit. Then add the database angle (expand/contract). Covering both infrastructure and data is what makes this answer senior.""",
        tip_bn=r"""Deploy-এর সময় একটি pod-এর জীবনচক্র ধরে ধরে বলো: start → ready → traffic পাচ্ছে → SIGTERM → not ready → drain → exit। তারপর database-এর দিকটা (expand/contract) যোগ করো। Infrastructure আর data দুটোই ঢাকলে উত্তরটা senior মানের হয়।""",
        mist_en=r"""Calling `process.exit()` immediately on `SIGTERM`, leaving `keepAliveTimeout` at 5 s behind a 60 s idle-timeout load balancer, or running a destructive migration before the old pods are gone.""",
        mist_bn=r"""`SIGTERM` পেয়েই সাথে সাথে `process.exit()` call করা, 60 s idle-timeout load balancer-এর পেছনে `keepAliveTimeout` 5 s রেখে দেওয়া, অথবা পুরনো pod চলে যাওয়ার আগেই destructive migration চালানো।""",
        code=r"""
            import express from 'express';
            import { setTimeout as sleep } from 'node:timers/promises';

            const app = express();
            let ready = true;

            app.use((req, res, next) => {
              if (!ready) res.set('Connection', 'close'); // draining: don't reuse this socket
              next();
            });
            app.get('/health/ready', (req, res) => res.sendStatus(ready ? 200 : 503));
            app.get('/health/live', (req, res) => res.sendStatus(200));
            // ...routes

            const server = app.listen(3000);
            server.keepAliveTimeout = 65_000; // > load balancer idle timeout (ALB default: 60 s)
            server.headersTimeout = 66_000;   // keep it above keepAliveTimeout

            process.on('SIGTERM', async () => {
              ready = false;          // readiness fails -> no new traffic routed here
              await sleep(10_000);    // let the LB / endpoints catch up
              const force = setTimeout(() => {
                server.closeAllConnections();
                process.exit(1);
              }, 20_000);
              force.unref();
              // close() only closes sockets idle *now*; busy keep-alive sockets would
              // otherwise stay open for keepAliveTimeout (65 s) after their last response
              setInterval(() => server.closeIdleConnections(), 250).unref();
              server.close(async () => {
                await db.end();       // close pools, flush logs
                process.exit(0);
              });
            });
        """,
        lang="javascript",
        extra=[
            dict(lang="yaml", src=r"""
                # Deployment excerpt
                spec:
                  strategy:
                    type: RollingUpdate
                    rollingUpdate:
                      maxUnavailable: 0
                      maxSurge: 1
                  template:
                    spec:
                      terminationGracePeriodSeconds: 45   # > readiness delay + longest request
                      containers:
                        - name: api
                          readinessProbe:
                            httpGet: { path: /health/ready, port: 3000 }
                            periodSeconds: 5
                          livenessProbe:
                            httpGet: { path: /health/live, port: 3000 }
            """, label_en="Kubernetes rolling update settings", label_bn="Kubernetes rolling update setting"),
        ],
        follow=[
            ("How would you rename a heavily used database column without downtime?", "বহুল ব্যবহৃত একটি database column downtime ছাড়া কীভাবে rename করবে?"),
            ("Why should the liveness probe not check the database?", "Liveness probe-এ কেন database check করা উচিত নয়?"),
            ("How do you handle WebSocket clients during a rolling deploy?", "Rolling deploy-এর সময় WebSocket client-দের কীভাবে handle করবে?"),
        ],
        related=["node-028", "node-026"],
        refs=[NODE_HTTP, ALB_DOCS, K8S_POD_LIFECYCLE],
    ),
]

if __name__ == "__main__":
    save("nodejs", "b3", QUESTIONS)
