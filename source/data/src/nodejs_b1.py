import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NODE_INTRO = ("Node.js Learn — Introduction to Node.js", "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs")
NODE_EVENT_LOOP = ("Node.js Learn — The Node.js Event Loop", "https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick")
NODE_DONT_BLOCK = ("Node.js Learn — Don't Block the Event Loop (or the Worker Pool)", "https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop")
NODE_PROCESS = ("Node.js API — process (nextTick)", "https://nodejs.org/api/process.html")
NODE_CLI = ("Node.js API — Command-line options", "https://nodejs.org/api/cli.html")
NODE_GLOBALS = ("Node.js API — Globals (fetch)", "https://nodejs.org/api/globals.html")
NODE_TEST = ("Node.js API — Test runner", "https://nodejs.org/api/test.html")
NODE_STREAM = ("Node.js API — Stream", "https://nodejs.org/api/stream.html")
NODE_BACKPRESSURE = ("Node.js Learn — Backpressuring in Streams", "https://nodejs.org/en/learn/modules/backpressuring-in-streams")
NODE_PERF_HOOKS = ("Node.js API — Performance measurement APIs", "https://nodejs.org/api/perf_hooks.html")
BULLMQ = ("BullMQ (GitHub)", "https://github.com/taskforcesh/bullmq")

QUESTIONS = [
    # ------------------------------------------------------------------ node-001
    Q(
        id="node-001", sub="Node.js Runtime", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["runtime", "v8", "libuv", "non-blocking-io", "event-loop"],
        ver="Node.js 26 LTS / 24 (version-independent concept)", vs=False, status="stable",
        q_en=r"""What is Node.js, and how can a single-threaded JavaScript runtime handle thousands of concurrent connections?""",
        q_bn=r"""Node.js কী? JavaScript একটি single thread-এ চললেও Node.js কীভাবে একসাথে হাজার হাজার connection handle করতে পারে?""",
        a_en=r"""
            Node.js is a server-side JavaScript runtime built from two main pieces: **V8**, the engine that compiles and runs JavaScript and manages the heap and garbage collection, and **libuv**, a C library that provides the event loop and asynchronous I/O.

            My JavaScript runs on one main thread, but that thread almost never *waits* for I/O. Network sockets use the operating system's non-blocking APIs (epoll, kqueue, IOCP). Work without a good non-blocking OS API — file system calls, `dns.lookup`, some `crypto` and `zlib` operations — goes to libuv's thread pool (4 threads by default). When the work finishes, its callback is queued and the event loop runs it on the main thread.

            So one thread can serve thousands of connections because it only runs short callbacks. The trade-off: any long synchronous CPU work blocks *every* request.
        """,
        a_bn=r"""
            Node.js হলো server-side JavaScript runtime, যার মূল দুটি অংশ: **V8** — যে engine JavaScript compile ও run করে এবং heap ও garbage collection manage করে, আর **libuv** — একটি C library যা event loop এবং asynchronous I/O দেয়।

            আমার JavaScript code একটি main thread-এ চলে, কিন্তু এই thread প্রায় কখনোই I/O-এর জন্য *অপেক্ষা* করে না। Network socket চলে operating system-এর non-blocking API (epoll, kqueue, IOCP) দিয়ে। যেসব কাজের ভালো non-blocking OS API নেই — file system call, `dns.lookup`, কিছু `crypto` ও `zlib` operation — সেগুলো যায় libuv-এর thread pool-এ (default 4টি thread)। কাজ শেষ হলে callback queue-তে ঢোকে, আর event loop সেটা main thread-এ চালায়।

            তাই একটি thread দিয়েই হাজার হাজার connection serve করা যায়, কারণ thread-টি শুধু ছোট ছোট callback চালায়। Trade-off হলো: লম্বা কোনো synchronous CPU কাজ চললে *সব* request আটকে যায়।
        """,
        quick_en=r"""Node.js is a server-side JavaScript runtime built on V8 (runs the JavaScript) and libuv (event loop and async I/O). Your code runs on one main thread that never waits for I/O: the OS or libuv's thread pool waits, and the event loop runs the callbacks, so long synchronous CPU work blocks every request.""",
        quick_bn=r"""Node.js হলো server-side JavaScript runtime, যেটা V8 (JavaScript চালায়) আর libuv (event loop ও async I/O) দিয়ে তৈরি। আমাদের code একটা main thread-এ চলে, যেটা I/O-এর জন্য অপেক্ষা করে না: অপেক্ষাটা করে OS বা libuv-এর thread pool, আর event loop callback চালায়; তাই লম্বা synchronous CPU কাজ সব request আটকে দেয়।""",
        ex_en=r"""
            - **"Single-threaded" refers to JavaScript execution**, not the whole process. A Node process also has V8 background threads (GC, compilation) and the libuv thread pool.
            - **Layers:** your code → core modules (`http`, `fs`, `stream`) → C++ bindings → V8 / libuv → OS.
            - **Where it shines:** I/O-bound work — REST/GraphQL APIs, real-time apps (WebSockets), proxies, BFFs, streaming.
            - **Where it struggles:** CPU-bound work (image processing, huge JSON transforms, password hashing) on the main thread. Move that to `worker_threads`, a job queue, or a separate service.
            - Compared with a thread-per-request server, there is no thread stack per connection, so an idle connection costs very little memory.
        """,
        ex_bn=r"""
            - **"Single-threaded" মানে JavaScript execution**, পুরো process নয়। একটি Node process-এ V8-এর background thread (GC, compilation) এবং libuv thread pool-ও থাকে।
            - **Layer-গুলো:** আমাদের code → core module (`http`, `fs`, `stream`) → C++ binding → V8 / libuv → OS।
            - **কোথায় ভালো:** I/O-bound কাজ — REST/GraphQL API, real-time app (WebSocket), proxy, BFF, streaming।
            - **কোথায় সমস্যা:** main thread-এ CPU-bound কাজ (image processing, বিশাল JSON transform, password hashing)। এগুলো `worker_threads`, job queue বা আলাদা service-এ সরাতে হয়।
            - Thread-per-request server-এর তুলনায় এখানে প্রতি connection-এর জন্য আলাদা thread stack লাগে না, তাই idle connection-এ memory খরচ খুব কম।
        """,
        tip_en=r"""Sketch the flow out loud: "JS thread → libuv → OS or thread pool → callback queue → event loop". Then name the trade-off (blocking the event loop) right away — it shows you understand the model, not just the definition.""",
        tip_bn=r"""Flow-টা মুখে মুখে এঁকে দেখাও: "JS thread → libuv → OS বা thread pool → callback queue → event loop"। তারপর সাথে সাথেই trade-off (event loop block হওয়া) উল্লেখ করো — এতে বোঝা যায় তুমি শুধু definition মুখস্থ করোনি, model-টা বুঝেছ।""",
        mist_en=r"""Saying Node runs JavaScript on many threads, or that *all* async operations use the thread pool. Network I/O does not — it uses the OS's non-blocking sockets.""",
        mist_bn=r"""Node একাধিক thread-এ JavaScript চালায় বলা, অথবা *সব* async operation thread pool ব্যবহার করে বলা। Network I/O thread pool ব্যবহার করে না — এটা OS-এর non-blocking socket ব্যবহার করে।""",
        follow=[
            ("Which operations use the libuv thread pool, and how do you change its size?", "কোন কোন operation libuv thread pool ব্যবহার করে, আর এর size কীভাবে পরিবর্তন করা যায়?"),
            ("What happens to other users if one request handler runs a 2-second synchronous loop?", "একটি request handler যদি ২ সেকেন্ডের synchronous loop চালায়, তাহলে অন্য user-দের কী হবে?"),
        ],
        related=["node-002", "node-006"],
        refs=[NODE_INTRO, NODE_DONT_BLOCK],
    ),
    # ------------------------------------------------------------------ node-002
    Q(
        id="node-002", sub="Event Loop", diff="easy", type="output",
        prio="high", market="bangladesh", mins=3,
        tags=["event-loop", "nexttick", "microtasks", "settimeout", "output"],
        ver="Node.js 26 LTS / 24 (behaviour unchanged across versions)", vs=False, status="stable",
        q_en=r"""What does this script print? It is saved as `order.js` (CommonJS — no `"type": "module"` in package.json) and run with `node order.js`.""",
        q_bn=r"""এই script কী print করবে? এটি `order.js` নামে save করা (CommonJS — package.json-এ `"type": "module"` নেই) এবং `node order.js` দিয়ে run করা হয়েছে।""",
        a_en=r"""
            It prints `A`, `E`, `D`, `C`, `B` (one per line).

            Synchronous code runs first (`A`, `E`). When the main script finishes, Node drains the `process.nextTick` queue (`D`), then the Promise microtask queue (`C`). Only after both queues are empty does the event loop move to the timers phase and run the `setTimeout` callback (`B`).
        """,
        a_bn=r"""
            Output হবে `A`, `E`, `D`, `C`, `B` (প্রতিটি আলাদা লাইনে)।

            প্রথমে synchronous code চলে (`A`, `E`)। Main script শেষ হলে Node আগে `process.nextTick` queue খালি করে (`D`), তারপর Promise microtask queue (`C`)। দুটো queue খালি হওয়ার পরই event loop timers phase-এ গিয়ে `setTimeout`-এর callback চালায় (`B`)।
        """,
        quick_en=r"""It prints `A`, `E`, `D`, `C`, `B`. Synchronous code runs first, then Node drains the `process.nextTick` queue (`D`), then the Promise microtasks (`C`), and only then does the event loop reach the timers phase for `setTimeout` (`B`).""",
        quick_bn=r"""Print হবে `A`, `E`, `D`, `C`, `B`। আগে synchronous code চলে, তারপর Node `process.nextTick` queue খালি করে (`D`), তারপর Promise microtask (`C`), আর এরপরই event loop timers phase-এ গিয়ে `setTimeout` চালায় (`B`)।""",
        ex_en=r"""
            Step by step:

            1. `console.log('A')` runs immediately.
            2. `setTimeout(..., 0)` schedules `B` for the timers phase (the delay is really at least 1 ms).
            3. `Promise.resolve().then(...)` queues `C` as a microtask.
            4. `process.nextTick(...)` queues `D` in the nextTick queue.
            5. `console.log('E')` runs immediately.
            6. The script ends. In CommonJS, Node processes the **nextTick queue first**, then the **promise microtask queue** → `D`, `C`.
            7. The event loop starts; the timers phase runs `B`.

            **ESM twist (verified on Node):** the same code saved as `order.mjs` prints `A E C D B`. An ES module body is evaluated inside a promise job, so the microtask queue drains before Node gets to the nextTick queue. Mentioning this shows real depth.
        """,
        ex_bn=r"""
            ধাপে ধাপে:

            1. `console.log('A')` সাথে সাথে চলে।
            2. `setTimeout(..., 0)` `B`-কে timers phase-এর জন্য schedule করে (delay আসলে কমপক্ষে 1 ms)।
            3. `Promise.resolve().then(...)` `C`-কে microtask হিসেবে queue করে।
            4. `process.nextTick(...)` `D`-কে nextTick queue-তে রাখে।
            5. `console.log('E')` সাথে সাথে চলে।
            6. Script শেষ। CommonJS-এ Node **আগে nextTick queue**, তারপর **promise microtask queue** process করে → `D`, `C`।
            7. Event loop শুরু হয়; timers phase `B` চালায়।

            **ESM-এর twist (Node-এ যাচাই করা):** একই code `order.mjs` হিসেবে save করলে output হয় `A E C D B`। ES module-এর body একটি promise job-এর ভেতরে evaluate হয়, তাই Node nextTick queue-তে যাওয়ার আগেই microtask queue খালি হয়ে যায়। এটা উল্লেখ করলে তোমার গভীর জ্ঞান বোঝা যায়।
        """,
        tip_en=r"""Name the queues explicitly — "sync code, then nextTick queue, then promise microtasks, then the event loop phases". Interviewers care more about the model than the letters.""",
        tip_bn=r"""Queue-গুলোর নাম স্পষ্টভাবে বলো — "আগে sync code, তারপর nextTick queue, তারপর promise microtask, তারপর event loop-এর phase"। Interviewer অক্ষরের চেয়ে তোমার mental model-কে বেশি গুরুত্ব দেয়।""",
        mist_en=r"""Thinking `setTimeout(fn, 0)` runs "immediately", or assuming promises always run before `nextTick` (true in ESM, not in CommonJS).""",
        mist_bn=r"""`setTimeout(fn, 0)` "সাথে সাথে" চলে ভাবা, অথবা promise সবসময় `nextTick`-এর আগে চলে ধরে নেওয়া (ESM-এ সত্য, CommonJS-এ নয়)।""",
        code=r"""
            console.log('A');

            setTimeout(() => console.log('B'), 0);

            Promise.resolve().then(() => console.log('C'));

            process.nextTick(() => console.log('D'));

            console.log('E');
        """,
        lang="javascript",
        output=r"""
            A
            E
            D
            C
            B
        """,
        follow=[
            ("Why can recursive `process.nextTick` calls starve I/O?", "Recursive `process.nextTick` call কেন I/O-কে starve করতে পারে?"),
            ("When would you prefer `queueMicrotask` or `setImmediate` over `process.nextTick`?", "কখন `process.nextTick`-এর বদলে `queueMicrotask` বা `setImmediate` ব্যবহার করবে?"),
        ],
        related=["node-004", "node-013"],
        refs=[NODE_EVENT_LOOP, NODE_PROCESS],
    ),
    # ------------------------------------------------------------------ node-003
    Q(
        id="node-003", sub="Node.js Runtime", diff="easy", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["built-ins", "fetch", "node-test", "env-file", "tooling"],
        ver="Node.js 26 LTS / 24", vs=True, status="stable",
        q_en=r"""In a new Node.js 26 LTS project, which of these tasks still requires a third-party npm package?""",
        q_bn=r"""একটি নতুন Node.js 26 LTS project-এ নিচের কোন কাজের জন্য এখনও third-party npm package লাগবে?""",
        options=[
            ("Making HTTP requests with `fetch()`", "`fetch()` দিয়ে HTTP request পাঠানো"),
            ("Running unit tests with a test runner and assertions", "Test runner ও assertion দিয়ে unit test চালানো"),
            ("Loading configuration from a `.env` file", "`.env` file থেকে configuration load করা"),
            ("Connecting to a PostgreSQL database", "PostgreSQL database-এ connect করা"),
        ],
        correct=3,
        a_en=r"""
            Connecting to PostgreSQL. Node.js doesn't ship a PostgreSQL client, so you still install a driver such as `pg` (or an ORM on top of it). The other three are built in: global `fetch()`, the `node:test` runner with `node:assert`, and `.env` loading via `--env-file` or `process.loadEnvFile()`.
        """,
        a_bn=r"""
            সঠিক উত্তর PostgreSQL-এ connect করা। Node.js-এর সাথে কোনো PostgreSQL client আসে না, তাই `pg`-এর মতো driver (বা তার উপর কোনো ORM) install করতে হয়। বাকি তিনটি built-in: global `fetch()`, `node:assert` সহ `node:test` runner, আর `--env-file` বা `process.loadEnvFile()` দিয়ে `.env` load করা।
        """,
        quick_en=r"""Connecting to PostgreSQL: Node ships no PostgreSQL client, so you still install a driver such as `pg`. HTTP requests (`fetch()`), unit tests (`node:test` with `node:assert`) and `.env` loading (`--env-file` or `process.loadEnvFile()`) are all built in.""",
        quick_bn=r"""PostgreSQL-এ connect করা: Node-এ কোনো PostgreSQL client নেই, তাই `pg`-এর মতো driver install করতেই হয়। HTTP request (`fetch()`), unit test (`node:test` আর `node:assert`) আর `.env` load করা (`--env-file` বা `process.loadEnvFile()`) সবই built-in।""",
        ex_en=r"""
            - `fetch` (built on undici) is a stable global since Node 21.
            - `node --test` with `node:test` and `node:assert` has been stable since Node 20; it supports mocking, coverage and watch mode.
            - `node --env-file=.env app.js` and `process.loadEnvFile()` replace `dotenv` in most apps.
            - Other "you may not need a package" built-ins: `--watch` instead of nodemon, TypeScript type stripping instead of ts-node for erasable syntax, `util.parseArgs` for CLI flags, `crypto.randomUUID()` instead of `uuid` for v4 ids.

            The most tempting wrong option is the `.env` one — many tutorials still install `dotenv`, but it hasn't been necessary for simple cases in current LTS versions. Dedicated tools like Jest/Vitest are still fine when you need their extra features.
        """,
        ex_bn=r"""
            - `fetch` (undici-র উপর তৈরি) Node 21 থেকে stable global।
            - `node --test`, `node:test` ও `node:assert` Node 20 থেকে stable; mocking, coverage আর watch mode-ও আছে।
            - `node --env-file=.env app.js` আর `process.loadEnvFile()` বেশিরভাগ app-এ `dotenv`-এর জায়গা নিতে পারে।
            - আরও কিছু built-in যেগুলোর জন্য package লাগে না: nodemon-এর বদলে `--watch`, erasable syntax-এর জন্য ts-node-এর বদলে TypeScript type stripping, CLI flag-এর জন্য `util.parseArgs`, v4 id-র জন্য `uuid`-এর বদলে `crypto.randomUUID()`।

            সবচেয়ে বেশি ভুল হয় `.env` option-টায় — অনেক tutorial এখনও `dotenv` install করে, কিন্তু current LTS-এ সাধারণ ক্ষেত্রে এর দরকার নেই। তবে Jest/Vitest-এর বাড়তি feature লাগলে সেগুলো ব্যবহার করা এখনও ঠিক আছে।
        """,
        tip_en=r"""After answering, list two or three built-ins you actually use (`--env-file`, `node --test`, `--watch`). It signals you keep up with the platform instead of copying old tutorials.""",
        tip_bn=r"""উত্তর দেওয়ার পর নিজে ব্যবহার করো এমন দুই-তিনটি built-in-এর নাম বলো (`--env-file`, `node --test`, `--watch`)। এতে বোঝা যায় তুমি পুরনো tutorial কপি না করে platform-এর আপডেট রাখো।""",
        refs=[NODE_GLOBALS, NODE_TEST, NODE_CLI],
    ),
    # ------------------------------------------------------------------ node-004
    Q(
        id="node-004", sub="Event Loop", diff="medium", type="output",
        prio="high", market="both", mins=4,
        tags=["event-loop", "setimmediate", "settimeout", "phases", "output"],
        ver="Node.js 26 LTS / 24 (behaviour unchanged across versions)", vs=False, status="stable",
        q_en=r"""What does this CommonJS script print, and is the order guaranteed? Explain how the event loop phases decide it.""",
        q_bn=r"""এই CommonJS script কী print করবে, আর এই order কি guaranteed? Event loop-এর phase-গুলো কীভাবে এটা ঠিক করে ব্যাখ্যা করো।""",
        a_en=r"""
            It prints `sync`, `nextTick`, `promise`, `immediate`, `timeout` — and inside an I/O callback this order is guaranteed.

            The `readFile` callback runs in the **poll** phase. When it returns, Node first drains the nextTick queue and then the promise microtasks. The next phase after poll is **check**, which runs `setImmediate` callbacks, so `immediate` comes before `timeout`; the timer only runs when the loop wraps around to the timers phase.

            At the top level of the main module, `setTimeout(fn, 0)` vs `setImmediate` is **not** deterministic — it depends on process timing.
        """,
        a_bn=r"""
            Output হবে `sync`, `nextTick`, `promise`, `immediate`, `timeout` — আর I/O callback-এর ভেতরে এই order guaranteed।

            `readFile`-এর callback চলে **poll** phase-এ। Callback শেষ হলে Node আগে nextTick queue, তারপর promise microtask খালি করে। Poll-এর পরের phase হলো **check**, যেখানে `setImmediate` callback চলে, তাই `immediate` আগে আসে `timeout`-এর; timer চলবে loop আবার timers phase-এ ফিরে এলে।

            কিন্তু main module-এর top level-এ `setTimeout(fn, 0)` বনাম `setImmediate`-এর order **deterministic নয়** — এটা process-এর timing-এর উপর নির্ভর করে।
        """,
        quick_en=r"""It prints `sync`, `nextTick`, `promise`, `immediate`, `timeout`, and inside an I/O callback the order is guaranteed: after the poll phase Node drains nextTicks and promises, then the check phase (`setImmediate`) runs before the next timers phase. At the top level, `setTimeout` 0 vs `setImmediate` is not deterministic.""",
        quick_bn=r"""Print হবে `sync`, `nextTick`, `promise`, `immediate`, `timeout`, আর I/O callback-এর ভেতরে এই order নিশ্চিত: poll phase-এর পরে Node nextTick আর promise queue খালি করে, তারপর পরের timers phase-এর আগেই check phase (`setImmediate`) চলে। Top level-এ কিন্তু `setTimeout` 0 আর `setImmediate`-এর order নিশ্চিত নয়।""",
        ex_en=r"""
            Event loop phases in order: **timers** (`setTimeout`/`setInterval`) → **pending callbacks** (some deferred system errors) → idle/prepare (internal) → **poll** (I/O callbacks, waits for I/O) → **check** (`setImmediate`) → **close callbacks** (`'close'` events).

            1. `sync` is logged while the main script runs; `readFile` hands the read to the thread pool.
            2. The read completes; its callback runs in the poll phase and schedules four things.
            3. After the callback: nextTick queue → `nextTick`, then microtasks → `promise`.
            4. Poll → check: `immediate`.
            5. Next iteration, timers: `timeout`.

            Why the top-level case is random: when the main module finishes, the loop may enter the timers phase before or after the 1 ms timer threshold has passed, depending on how fast the process booted. If you need "run after I/O, before timers", use `setImmediate` from inside an I/O callback.
        """,
        ex_bn=r"""
            Event loop-এর phase-গুলো ক্রমানুসারে: **timers** (`setTimeout`/`setInterval`) → **pending callbacks** (কিছু deferred system error) → idle/prepare (internal) → **poll** (I/O callback, I/O-এর জন্য অপেক্ষা) → **check** (`setImmediate`) → **close callbacks** (`'close'` event)।

            1. Main script চলার সময় `sync` log হয়; `readFile` read-এর কাজ thread pool-এ পাঠিয়ে দেয়।
            2. Read শেষ হলে poll phase-এ callback চলে এবং চারটি জিনিস schedule করে।
            3. Callback-এর পরে: nextTick queue → `nextTick`, তারপর microtask → `promise`।
            4. Poll থেকে check: `immediate`।
            5. পরের iteration-এ timers: `timeout`।

            Top level-এ কেন random: main module শেষ হওয়ার পর loop timers phase-এ ঢোকার সময় 1 ms threshold পার হয়েছে কি না, সেটা process কত দ্রুত boot হলো তার উপর নির্ভর করে। "I/O-এর পরে, timer-এর আগে চালাও" দরকার হলে I/O callback-এর ভেতর থেকে `setImmediate` ব্যবহার করো।
        """,
        tip_en=r"""Say the phase names in order and point at which phase you're "in" when the callback runs. Then volunteer the top-level non-determinism — it's the follow-up most interviewers are waiting for.""",
        tip_bn=r"""Phase-গুলোর নাম ক্রমানুসারে বলো এবং callback চলার সময় loop কোন phase-এ আছে সেটা দেখাও। তারপর নিজে থেকেই top level-এর non-determinism-এর কথা বলো — বেশিরভাগ interviewer এই follow-up-টাই আশা করে।""",
        mist_en=r"""Claiming `setTimeout(fn, 0)` always runs before `setImmediate` (or always after) regardless of where it is called.""",
        mist_bn=r"""কোথা থেকে call করা হচ্ছে তা না দেখে বলা যে `setTimeout(fn, 0)` সবসময় `setImmediate`-এর আগে (বা সবসময় পরে) চলে।""",
        code=r"""
            const fs = require('node:fs');

            fs.readFile(__filename, () => {
              setTimeout(() => console.log('timeout'), 0);
              setImmediate(() => console.log('immediate'));
              process.nextTick(() => console.log('nextTick'));
              Promise.resolve().then(() => console.log('promise'));
            });

            console.log('sync');
        """,
        lang="javascript",
        output=r"""
            sync
            nextTick
            promise
            immediate
            timeout
        """,
        follow=[
            ("What runs in the 'close callbacks' phase?", "'close callbacks' phase-এ কী চলে?"),
            ("Where do microtasks run when there are two `setImmediate` callbacks queued?", "দুটি `setImmediate` callback queue-তে থাকলে microtask কখন চলে?"),
        ],
        related=["node-002", "node-013"],
        refs=[NODE_EVENT_LOOP, NODE_PROCESS],
    ),
    # ------------------------------------------------------------------ node-005
    Q(
        id="node-005", sub="Streams", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["streams", "backpressure", "highwatermark", "pipeline", "drain"],
        ver="Node.js 26 LTS / 24", vs=False, status="stable",
        q_en=r"""What is backpressure in Node.js streams, and how do you handle it correctly?""",
        q_bn=r"""Node.js stream-এ backpressure কী, আর এটা সঠিকভাবে কীভাবে handle করতে হয়?""",
        a_en=r"""
            Backpressure is what happens when data is produced faster than it can be consumed — for example, reading a file from a fast disk and uploading it over a slow network. Without control, the unsent chunks pile up in memory until the process runs out of it.

            Node's streams signal this through the **`highWaterMark`**: `writable.write(chunk)` returns `false` once the internal buffer is above that threshold. The producer should then stop writing and wait for the `'drain'` event before continuing.

            In practice I let Node do it for me: `pipeline()` from `node:stream/promises` (or `.pipe()`) pauses the readable and resumes it on `'drain'` automatically, and `pipeline` also propagates errors and destroys every stream on failure. I only handle `write()`/`'drain'` manually when I'm writing in a loop myself.
        """,
        a_bn=r"""
            Backpressure হলো এমন অবস্থা যখন data যত দ্রুত তৈরি হচ্ছে, তত দ্রুত consume করা যাচ্ছে না — যেমন দ্রুত disk থেকে file পড়ে ধীর network-এ upload করা। নিয়ন্ত্রণ না থাকলে না-পাঠানো chunk-গুলো memory-তে জমতে থাকে, শেষে process-এর memory শেষ হয়ে যায়।

            Node-এর stream এটা **`highWaterMark`** দিয়ে জানায়: internal buffer এই সীমা ছাড়ালে `writable.write(chunk)` `false` return করে। তখন producer-এর উচিত লেখা থামিয়ে `'drain'` event-এর জন্য অপেক্ষা করা।

            বাস্তবে আমি কাজটা Node-কেই করতে দিই: `node:stream/promises`-এর `pipeline()` (বা `.pipe()`) নিজে থেকেই readable-কে pause করে এবং `'drain'` হলে আবার resume করে; আর `pipeline` error propagate করে এবং failure হলে সব stream destroy করে। শুধু নিজে loop-এ লিখলে `write()`/`'drain'` manually handle করি।
        """,
        quick_en=r"""Backpressure is when data is produced faster than it can be consumed, so chunks pile up in memory. `write()` returns `false` once the buffer passes `highWaterMark`, and you wait for `'drain'`; in practice `pipeline()` from `node:stream/promises` does this for you and also handles errors and cleanup.""",
        quick_bn=r"""Backpressure হলো যখন data যত দ্রুত তৈরি হচ্ছে তত দ্রুত consume হচ্ছে না, ফলে chunk-গুলো memory-তে জমতে থাকে। Buffer `highWaterMark` পার হলে `write()` `false` return করে, তখন `'drain'` event-এর জন্য অপেক্ষা করতে হয়; বাস্তবে `node:stream/promises`-এর `pipeline()` এটা নিজেই করে, সাথে error আর cleanup-ও সামলায়।""",
        ex_en=r"""
            - **`highWaterMark` is a threshold, not a hard limit.** `write()` still accepts data after returning `false`; ignoring the return value is exactly how memory explodes. Byte streams default to 64 KiB in current Node versions (16 KiB in older ones); object-mode streams count objects (16).
            - **Readable side:** a paused readable stops calling `_read()` once its buffer is full, which in turn stops reading from the source (e.g. the TCP socket's receive window fills up, so the client slows down).
            - **`.pipe()` vs `pipeline()`:** `.pipe()` handles backpressure but not errors — if the destination fails, the source is not destroyed and you can leak file descriptors. `pipeline()` fixes that and supports an `AbortSignal`.
            - **Async iteration** (`for await (const chunk of readable)`) also respects backpressure because it pulls one chunk at a time.
            - **Transforms** apply backpressure too: if a transform's push buffer is full, it stops accepting writes.
        """,
        ex_bn=r"""
            - **`highWaterMark` একটি threshold, hard limit নয়।** `false` return করার পরেও `write()` data নেয়; return value ignore করলেই memory বিস্ফোরিত হয়। Current Node version-এ byte stream-এর default 64 KiB (পুরনো version-এ 16 KiB); object-mode stream object গোনে (16টি)।
            - **Readable দিক:** buffer ভরে গেলে paused readable `_read()` call করা বন্ধ করে, ফলে source থেকেও পড়া থেমে যায় (যেমন TCP socket-এর receive window ভরে যায়, client নিজেই ধীর হয়)।
            - **`.pipe()` বনাম `pipeline()`:** `.pipe()` backpressure handle করে কিন্তু error নয় — destination fail করলে source destroy হয় না, file descriptor leak হতে পারে। `pipeline()` এই সমস্যা ঠিক করে এবং `AbortSignal` support করে।
            - **Async iteration** (`for await (const chunk of readable)`) একটার পর একটা chunk টেনে আনে, তাই এটাও backpressure মানে।
            - **Transform**-ও backpressure দেয়: transform-এর push buffer ভরে গেলে সে আর write নেয় না।
        """,
        tip_en=r"""Use a concrete story: "fast disk, slow S3 upload — without backpressure the process OOMs". Then say "`write()` returns false → wait for drain, or just use `pipeline`". Short, concrete and correct.""",
        tip_bn=r"""একটা বাস্তব উদাহরণ দিয়ে শুরু করো: "দ্রুত disk, ধীর S3 upload — backpressure না থাকলে process OOM হয়"। তারপর বলো "`write()` false দিলে drain-এর জন্য অপেক্ষা করো, অথবা সরাসরি `pipeline` ব্যবহার করো"। ছোট, বাস্তব এবং সঠিক।""",
        mist_en=r"""Ignoring the return value of `write()`, or using `readable.on('data', chunk => writable.write(chunk))`, which has no backpressure at all.""",
        mist_bn=r"""`write()`-এর return value ignore করা, অথবা `readable.on('data', chunk => writable.write(chunk))` ব্যবহার করা — যেখানে কোনো backpressure-ই নেই।""",
        code=r"""
            import { createWriteStream } from 'node:fs';
            import { once } from 'node:events';

            // Writing in a loop by hand: respect write()'s return value
            const out = createWriteStream('numbers.txt');

            for (let i = 0; i < 1_000_000; i++) {
              if (!out.write(`${i}\n`)) {
                await once(out, 'drain'); // pause until the buffer is flushed
              }
            }

            out.end();
            await once(out, 'finish');
        """,
        lang="javascript",
        follow=[
            ("Why is `pipeline()` preferred over `.pipe()`?", "`.pipe()`-এর চেয়ে `pipeline()` কেন ভালো?"),
            ("How does backpressure propagate back to a TCP client?", "Backpressure কীভাবে TCP client পর্যন্ত ফিরে যায়?"),
        ],
        related=["node-011", "node-032"],
        refs=[NODE_BACKPRESSURE, NODE_STREAM],
    ),
    # ------------------------------------------------------------------ node-006
    Q(
        id="node-006", sub="Performance & Scalability", diff="hard", type="scenario",
        prio="high", market="both", mins=10,
        tags=["event-loop-lag", "cpu-profiling", "production-debugging", "performance", "redos"],
        ver="Node.js 26 LTS / 24", vs=False, status="stable",
        q_en=r"""A Node.js API's p99 latency jumps from about 80 ms to 4 s a few times an hour. During those spikes one CPU core is at 100%, health checks time out, but database metrics look normal. How do you find and fix the cause?""",
        q_bn=r"""একটি Node.js API-এর p99 latency ঘণ্টায় কয়েকবার প্রায় 80 ms থেকে 4 s-এ লাফ দেয়। ওই spike-এর সময় একটি CPU core 100%-এ থাকে, health check timeout হয়, কিন্তু database metric স্বাভাবিক। তুমি কীভাবে কারণ খুঁজে বের করবে এবং ঠিক করবে?""",
        a_en=r"""
            One core pegged, all requests slow at once and a healthy database point to **event-loop blocking**: some synchronous code is hogging the main thread, so every other request (and the health check) waits.

            My approach:

            1. **Confirm it with metrics.** Export event-loop delay (`monitorEventLoopDelay`) and event-loop utilization (`performance.eventLoopUtilization()`). If loop delay p99 jumps to seconds during the spikes, it's blocking, not slow I/O.
            2. **Find the request.** Log duration per request with a request ID, and correlate the spike with the slow routes and their input sizes.
            3. **Profile.** Reproduce with a load test and capture a CPU profile (`node --cpu-prof`, or attach DevTools via `--inspect`) and read the flame graph. Typical culprits: `JSON.parse`/`JSON.stringify` on huge payloads, `*Sync` APIs (`fs.readFileSync`, `crypto.pbkdf2Sync`), a catastrophic-backtracking regex (ReDoS), big in-memory sorts or loops over unbounded input, sync compression or templating.
            4. **Fix the root cause.** Bound input sizes and paginate, switch to async/streaming APIs, rewrite the regex, and move unavoidable CPU work to a worker pool (`worker_threads` or a job queue).
            5. **Prevent regressions.** Alert on loop delay, add request size limits and timeouts, and include a load test in CI for the hot endpoints.
        """,
        a_bn=r"""
            একটি core পুরো ব্যস্ত, সব request একসাথে ধীর, আর database সুস্থ — এগুলো **event loop block হওয়ার** লক্ষণ: কোনো synchronous code main thread দখল করে রাখছে, তাই বাকি সব request (এবং health check) অপেক্ষা করছে।

            আমার approach:

            1. **Metric দিয়ে নিশ্চিত হওয়া।** Event loop delay (`monitorEventLoopDelay`) এবং event loop utilization (`performance.eventLoopUtilization()`) export করি। Spike-এর সময় loop delay-এর p99 সেকেন্ডে উঠে গেলে সমস্যা blocking, ধীর I/O নয়।
            2. **কোন request দায়ী খুঁজে বের করা।** Request ID সহ প্রতিটি request-এর duration log করি, তারপর spike-এর সময়ের ধীর route এবং তাদের input size মিলিয়ে দেখি।
            3. **Profile করা।** Load test দিয়ে সমস্যাটা reproduce করে CPU profile নিই (`node --cpu-prof`, বা `--inspect` দিয়ে DevTools attach করে) এবং flame graph পড়ি। সাধারণ অপরাধী: বিশাল payload-এ `JSON.parse`/`JSON.stringify`, `*Sync` API (`fs.readFileSync`, `crypto.pbkdf2Sync`), catastrophic backtracking করা regex (ReDoS), unbounded input-এর উপর বড় sort বা loop, sync compression বা templating।
            4. **মূল কারণ ঠিক করা।** Input size সীমিত করা ও pagination, async/streaming API ব্যবহার, regex পুনর্লিখন, আর এড়ানো যায় না এমন CPU কাজ worker pool-এ (`worker_threads` বা job queue) সরানো।
            5. **ভবিষ্যতে আটকানো।** Loop delay-এর উপর alert, request size limit ও timeout যোগ করা, আর hot endpoint-গুলোর জন্য CI-তে load test রাখা।
        """,
        quick_en=r"""It's event-loop blocking: one pegged core, everything slow at once and a healthy database mean synchronous code is hogging the main thread. Confirm it with event-loop delay metrics, find the hot path with a CPU profile, then bound inputs, use async APIs, or move CPU work to worker threads or a queue.""",
        quick_bn=r"""এটা event loop block হওয়ার লক্ষণ: একটা core 100%, সব request একসাথে slow, অথচ database ঠিক আছে, মানে কোনো synchronous code main thread আটকে রাখছে। Event-loop delay metric দিয়ে নিশ্চিত হও, CPU profile দিয়ে hot path খুঁজে বের করো, তারপর input সীমিত করো, async API ব্যবহার করো, অথবা CPU কাজ worker thread বা queue-তে সরাও।""",
        ex_en=r"""
            - **Why health checks fail:** the health endpoint is just another callback on the same blocked loop. Orchestrators may then restart a healthy-but-busy pod, making the incident worse.
            - **Event-loop delay vs utilization:** delay tells you how late timers fire (user-visible latency); utilization tells you how busy the loop is. High utilization with low delay is fine; high delay is the alarm.
            - **Profiling in production:** `--cpu-prof` writes a `.cpuprofile` only when the process exits normally — if `SIGINT`/`SIGTERM` kills it without a handler that calls `process.exit()`, no profile is written. It fits a canary or a reproduction environment better than the main fleet. Tools such as Clinic.js or 0x wrap the same idea into flame graphs.
            - **ReDoS** is easy to miss: a regex like `/(\/.+)+$/` can take exponential time on crafted input. Avoid nested quantifiers or use a linear-time engine (RE2).
            - **Don't "fix" it by adding instances only.** More pods dilute the symptom but every request that hits the bad path still blocks its own process.
        """,
        ex_bn=r"""
            - **Health check কেন fail করে:** health endpoint-ও একই blocked loop-এর আরেকটি callback। তখন orchestrator একটি সুস্থ-কিন্তু-ব্যস্ত pod-কে restart করে দিতে পারে, যা incident আরও খারাপ করে।
            - **Event loop delay বনাম utilization:** delay বলে timer কত দেরিতে fire হচ্ছে (user যে latency দেখে); utilization বলে loop কতটা ব্যস্ত। Utilization বেশি কিন্তু delay কম হলে সমস্যা নেই; delay বেশি হওয়াটাই আসল alarm।
            - **Production-এ profiling:** `--cpu-prof` শুধু process স্বাভাবিকভাবে exit করলেই `.cpuprofile` file লেখে — `process.exit()` call করে এমন handler ছাড়া `SIGINT`/`SIGTERM` process মেরে ফেললে কোনো profile লেখা হয় না। এটা পুরো fleet-এর চেয়ে canary বা reproduction environment-এ বেশি উপযোগী। Clinic.js বা 0x-এর মতো tool একই ধারণাকে flame graph আকারে দেখায়।
            - **ReDoS** সহজে চোখ এড়িয়ে যায়: `/(\/.+)+$/`-এর মতো regex বিশেষভাবে বানানো input-এ exponential সময় নিতে পারে। Nested quantifier এড়াও অথবা linear-time engine (RE2) ব্যবহার করো।
            - **শুধু instance বাড়িয়ে "ঠিক" করো না।** বেশি pod দিলে symptom কমে, কিন্তু খারাপ path-এ যাওয়া প্রতিটি request তখনও নিজের process block করে।
        """,
        tip_en=r"""Structure it as hypothesis → evidence → root cause → fix → prevention. Naming a concrete metric (event-loop delay p99) and a concrete tool (`--cpu-prof` + flame graph) is what separates a senior answer from "I'd add more servers".""",
        tip_bn=r"""উত্তর সাজাও এভাবে: hypothesis → প্রমাণ → মূল কারণ → fix → prevention। নির্দিষ্ট metric (event loop delay p99) আর নির্দিষ্ট tool (`--cpu-prof` + flame graph)-এর নাম বলাই senior উত্তরকে "আরও server যোগ করব" থেকে আলাদা করে।""",
        mist_en=r"""Blaming the database or network without evidence, or adding `UV_THREADPOOL_SIZE` — the thread pool doesn't help when JavaScript itself is blocking the main thread.""",
        mist_bn=r"""প্রমাণ ছাড়াই database বা network-কে দোষ দেওয়া, অথবা `UV_THREADPOOL_SIZE` বাড়ানো — JavaScript নিজেই main thread block করলে thread pool কোনো সাহায্য করে না।""",
        code=r"""
            import { monitorEventLoopDelay, performance } from 'node:perf_hooks';

            const histogram = monitorEventLoopDelay({ resolution: 20 });
            histogram.enable();
            let lastELU = performance.eventLoopUtilization();

            setInterval(() => {
              const elu = performance.eventLoopUtilization(lastELU); // delta since last tick
              lastELU = performance.eventLoopUtilization();
              console.log({
                loopDelayP99Ms: Math.round(histogram.percentile(99) / 1e6),
                loopDelayMaxMs: Math.round(histogram.max / 1e6),
                utilization: Number(elu.utilization.toFixed(2)),
              }); // ship these to your metrics system instead of console
              histogram.reset();
            }, 10_000).unref();
        """,
        lang="javascript",
        extra=[
            dict(lang="bash", src=r"""
                # Reproduce with load, then inspect the .cpuprofile in Chrome DevTools (Performance tab)
                node --cpu-prof --cpu-prof-dir=./profiles server.js
                # ...run the load test against the slow endpoint, then stop the server.
                # The profile is written only on a normal exit, so the server needs a
                # SIGINT/SIGTERM handler that ends with process.exit() (or let it exit by itself).
            """, label_en="Capturing a CPU profile", label_bn="CPU profile নেওয়া"),
        ],
        follow=[
            ("How would you make a CPU-heavy endpoint non-blocking without rewriting it?", "পুরো code না বদলে একটি CPU-heavy endpoint-কে কীভাবে non-blocking করবে?"),
            ("How can a regex cause a denial of service?", "একটি regex কীভাবে denial of service ঘটাতে পারে?"),
        ],
        related=["node-001", "node-018", "node-019"],
        refs=[NODE_DONT_BLOCK, NODE_PERF_HOOKS, NODE_CLI],
    ),
    # ------------------------------------------------------------------ node-007
    Q(
        id="node-007", sub="Asynchronous Programming", diff="extreme", type="system-design",
        prio="high", market="international", mins=20,
        tags=["job-queue", "workers", "idempotency", "retries", "bullmq", "system-design"],
        ver="Node.js 26 LTS / 24; BullMQ 5+ (example)", vs=False, status="stable",
        q_en=r"""Design a background job system in Node.js for sending invoice emails and generating PDF invoices: about 200k jobs per day with big spikes during sales campaigns. Jobs must not be lost, customers must not receive duplicate emails, and deploying workers must not drop work.""",
        q_bn=r"""Node.js-এ invoice email পাঠানো এবং PDF invoice তৈরির জন্য একটি background job system design করো: দিনে প্রায় 200k job, sales campaign-এর সময় বড় spike। কোনো job হারানো যাবে না, customer যেন duplicate email না পায়, আর worker deploy করার সময় কোনো কাজ হারানো যাবে না।""",
        a_en=r"""
            *(Advanced, senior-level answer.)* I'd separate **accepting work** from **doing work** with a durable queue, and design for **at-least-once delivery + idempotent handlers**, because exactly-once delivery isn't realistic across a network.

            - **Producer (API):** validates the request and enqueues a job with a deterministic ID (e.g. `invoice-email-<orderId>`). If the job must be consistent with a DB write, use a **transactional outbox**: write the order and an outbox row in one transaction, and a relay publishes to the queue.
            - **Broker:** Redis + BullMQ is a common Node choice; SQS or RabbitMQ are alternatives. Separate queues for `email` and `pdf` so slow PDFs don't block emails (head-of-line blocking).
            - **Workers:** a separate deployment from the API. Email workers are I/O-bound (high concurrency, e.g. 20 per process). PDF rendering is CPU-bound, so lower concurrency per process or `worker_threads`.
            - **Idempotency:** before sending, check a `sent_emails` table with a unique key on `orderId` (or the provider's idempotency key). A retried job then becomes a no-op.
            - **Retries:** exponential backoff with jitter and a max attempts count; classify errors — permanent (invalid address) fail fast, transient (timeout, 5xx) retry. After the last attempt, the job lands in a failed set / DLQ for inspection and replay.
            - **Rate limits & spikes:** queue absorbs bursts; a global rate limit protects the email provider; autoscale workers on queue depth and age of the oldest job.
            - **Stalled jobs:** if a worker dies mid-job, the lock/visibility timeout expires and the job is retried — another reason handlers must be idempotent.
            - **Graceful deploys:** on `SIGTERM`, stop fetching new jobs, finish active ones (`worker.close()`), then exit; the orchestrator's grace period must exceed the longest job.
            - **Observability:** queue depth, oldest-job age, throughput, failure rate, processing time per job type; propagate a trace/request ID in job data; alert when the DLQ grows.
        """,
        a_bn=r"""
            *(Advanced, senior-level উত্তর।)* আমি একটি durable queue দিয়ে **কাজ গ্রহণ করা** আর **কাজ করা**-কে আলাদা করব, এবং design করব **at-least-once delivery + idempotent handler** ধরে, কারণ network-এর উপর exactly-once delivery বাস্তবসম্মত নয়।

            - **Producer (API):** request validate করে deterministic ID দিয়ে job enqueue করে (যেমন `invoice-email-<orderId>`)। Job-কে যদি DB write-এর সাথে consistent হতে হয়, তাহলে **transactional outbox** ব্যবহার করি: order এবং একটি outbox row একই transaction-এ লিখি, আর একটি relay সেটা queue-তে publish করে।
            - **Broker:** Node-এ Redis + BullMQ জনপ্রিয়; SQS বা RabbitMQ-ও বিকল্প। `email` আর `pdf`-এর জন্য আলাদা queue, যাতে ধীর PDF email-কে আটকে না দেয় (head-of-line blocking)।
            - **Worker:** API থেকে আলাদা deployment। Email worker I/O-bound (বেশি concurrency, যেমন process প্রতি 20)। PDF rendering CPU-bound, তাই process প্রতি কম concurrency বা `worker_threads`।
            - **Idempotency:** পাঠানোর আগে `sent_emails` table-এ `orderId`-এর unique key (বা provider-এর idempotency key) check করি। ফলে retry হওয়া job কিছুই করে না।
            - **Retry:** jitter সহ exponential backoff আর max attempts; error ভাগ করা — permanent (ভুল address) হলে সাথে সাথে fail, transient (timeout, 5xx) হলে retry। শেষ attempt-এর পর job failed set / DLQ-তে যায়, যেখান থেকে দেখে replay করা যায়।
            - **Rate limit ও spike:** queue burst শোষণ করে; global rate limit email provider-কে রক্ষা করে; queue depth আর সবচেয়ে পুরনো job-এর বয়স দেখে worker autoscale করি।
            - **Stalled job:** কাজের মাঝখানে worker মারা গেলে lock/visibility timeout শেষ হয়ে job আবার retry হয় — handler idempotent হওয়ার আরেকটি কারণ।
            - **Graceful deploy:** `SIGTERM` পেলে নতুন job নেওয়া বন্ধ, চলমান job শেষ করা (`worker.close()`), তারপর exit; orchestrator-এর grace period সবচেয়ে লম্বা job-এর চেয়ে বেশি হতে হবে।
            - **Observability:** queue depth, oldest-job age, throughput, failure rate, job type অনুযায়ী processing time; job data-তে trace/request ID পাঠানো; DLQ বাড়লে alert।
        """,
        quick_en=r"""Put a durable queue (BullMQ on Redis, or SQS) between the API and separate worker deployments, and design for at-least-once delivery with idempotent handlers, because exactly-once isn't realistic. Add deterministic job IDs, retries with backoff and a dead-letter queue, and graceful worker shutdown on `SIGTERM`.""",
        quick_bn=r"""API আর আলাদা worker deployment-এর মাঝে একটা durable queue (Redis-এর উপর BullMQ, বা SQS) রাখো, আর at-least-once delivery ধরে নিয়ে handler-গুলো idempotent বানাও, কারণ exactly-once বাস্তবে সম্ভব নয়। সাথে deterministic job ID, backoff-সহ retry, dead-letter queue আর `SIGTERM`-এ worker-এর graceful shutdown রাখো।""",
        ex_en=r"""
            **Failure scenarios to discuss:**

            - **Redis/broker down:** the API can't enqueue. With an outbox, orders are still saved and the relay catches up later; without it, you must fail the request or buffer somewhere durable.
            - **Poison message:** a job that always crashes the worker. Max attempts + DLQ stop it from looping forever; alert on it.
            - **Duplicate delivery:** happens after worker crashes, lock expiry or network partitions. Idempotency keys make it harmless.
            - **Provider outage:** a circuit breaker pauses the queue instead of burning all retries in minutes.
            - **Memory leak in a worker:** process restarts are safe because jobs are durable — but monitor restart counts.

            **Trade-offs:** Redis-based queues are fast and simple but need Redis persistence (AOF) and memory headroom; SQS gives managed durability and visibility timeouts but has message size and latency limits. Keep job payloads small (IDs, not whole documents) and load fresh data inside the worker.

            Note: BullMQ rejects custom job IDs that are plain integers or contain `:`, so use a dash-separated ID.
        """,
        ex_bn=r"""
            **যেসব failure scenario আলোচনা করা উচিত:**

            - **Redis/broker down:** API enqueue করতে পারে না। Outbox থাকলে order তবুও save হয়, পরে relay সেটা পাঠিয়ে দেয়; outbox না থাকলে request fail করাতে হবে বা কোনো durable জায়গায় buffer করতে হবে।
            - **Poison message:** যে job প্রতিবার worker crash করায়। Max attempts + DLQ একে অনন্তকাল loop করা থেকে আটকায়; এর উপর alert রাখো।
            - **Duplicate delivery:** worker crash, lock expiry বা network partition-এর পরে হয়। Idempotency key থাকলে এটা ক্ষতিকর নয়।
            - **Provider outage:** circuit breaker queue-কে pause করে, যাতে কয়েক মিনিটেই সব retry শেষ না হয়ে যায়।
            - **Worker-এ memory leak:** job durable বলে process restart নিরাপদ — তবে restart count monitor করো।

            **Trade-off:** Redis-based queue দ্রুত ও সহজ, কিন্তু Redis persistence (AOF) আর পর্যাপ্ত memory লাগে; SQS managed durability ও visibility timeout দেয়, কিন্তু message size ও latency-র সীমা আছে। Job payload ছোট রাখো (পুরো document নয়, শুধু ID) এবং worker-এর ভেতরে fresh data load করো।

            খেয়াল রাখো: BullMQ এমন custom job ID reject করে যা শুধু integer বা যাতে `:` আছে, তাই dash দিয়ে ID বানাও।
        """,
        tip_en=r"""Start by stating the delivery guarantee ("at-least-once, so handlers are idempotent"). Everything else — dedupe keys, retries, DLQ, graceful shutdown — follows from that sentence, and interviewers notice when you lead with it.""",
        tip_bn=r"""শুরুতেই delivery guarantee বলে দাও ("at-least-once, তাই handler idempotent")। বাকি সবকিছু — dedupe key, retry, DLQ, graceful shutdown — এই এক বাক্য থেকেই আসে, আর interviewer লক্ষ্য করে তুমি এটা দিয়ে শুরু করেছ কি না।""",
        mist_en=r"""Promising "exactly-once" processing, running CPU-heavy PDF work in the API process, or retrying every error forever without a DLQ.""",
        mist_bn=r""""Exactly-once" processing-এর প্রতিশ্রুতি দেওয়া, API process-এর ভেতরেই CPU-heavy PDF কাজ চালানো, অথবা DLQ ছাড়া প্রতিটি error অনন্তকাল retry করা।""",
        code=r"""
            import { Queue, Worker } from 'bullmq';

            const connection = { host: process.env.REDIS_HOST, port: 6379 };
            export const emailQueue = new Queue('email', { connection });

            // Producer (API): same jobId is ignored while that job still exists
            export async function enqueueInvoiceEmail(orderId, to) {
              await emailQueue.add(
                'invoice-email',
                { orderId, to },
                {
                  jobId: `invoice-email-${orderId}`,
                  attempts: 5,
                  backoff: { type: 'exponential', delay: 2_000 },
                  removeOnComplete: { age: 24 * 3600 },
                  removeOnFail: false, // keep failures for inspection and replay
                },
              );
            }

            // Consumer (separate worker deployment)
            const worker = new Worker(
              'email',
              async (job) => {
                if (await alreadySent(job.data.orderId)) return 'skipped'; // idempotency
                await sendInvoiceEmail(job.data);
                await markSent(job.data.orderId); // unique key on orderId
              },
              { connection, concurrency: 20 },
            );

            worker.on('failed', (job, err) => {
              console.error({ jobId: job?.id, attempts: job?.attemptsMade, err: err.message });
            });

            process.on('SIGTERM', async () => {
              await worker.close(); // stop fetching, let active jobs finish
              process.exit(0);
            });
        """,
        lang="javascript",
        follow=[
            ("How does a transactional outbox prevent lost jobs?", "Transactional outbox কীভাবে job হারানো আটকায়?"),
            ("How would you prioritise password-reset emails over marketing emails?", "Marketing email-এর চেয়ে password-reset email-কে কীভাবে priority দেবে?"),
            ("What metric would you autoscale workers on, and why?", "কোন metric দেখে worker autoscale করবে, এবং কেন?"),
        ],
        related=["node-018", "node-020"],
        refs=[BULLMQ, NODE_DONT_BLOCK],
    ),
]

if __name__ == "__main__":
    save("nodejs", "b1", QUESTIONS)
