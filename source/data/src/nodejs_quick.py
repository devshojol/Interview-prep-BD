import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NODE_INTRO = ("Node.js Learn — Introduction to Node.js", "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs")
NODE_BLOCKING = ("Node.js Learn — Overview of Blocking vs Non-Blocking", "https://nodejs.org/en/learn/asynchronous-work/overview-of-blocking-vs-non-blocking")
NODE_EVENT_LOOP = ("Node.js Learn — The Node.js Event Loop", "https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick")
NPM_PACKAGE_JSON = ("npm Docs — package.json", "https://docs.npmjs.com/cli/v11/configuring-npm/package-json")
NODE_ESM = ("Node.js API — ECMAScript modules", "https://nodejs.org/api/esm.html")
NODE_ENV_VARS = ("Node.js API — Environment variables (.env support)", "https://nodejs.org/api/environment_variables.html")
NODE_STREAM = ("Node.js API — Stream", "https://nodejs.org/api/stream.html")
NODE_CALLBACKS = ("Node.js Learn — JavaScript Asynchronous Programming and Callbacks", "https://nodejs.org/en/learn/asynchronous-work/javascript-asynchronous-programming-and-callbacks")
NODE_EVENTS = ("Node.js API — Events", "https://nodejs.org/api/events.html")
NODE_PROCESS = ("Node.js API — process (uncaughtException)", "https://nodejs.org/api/process.html")

VER = "Node.js 26 LTS / 24 (version-independent concept)"

QUESTIONS = [
    # ------------------------------------------------------------------ node-q01
    Q(
        id="node-q01", sub="Node.js Runtime", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["runtime", "v8", "libuv"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is Node.js? Is it a language, a framework or a JavaScript engine?""",
        q_bn=r"""Node.js কী? এটা কি একটা language, framework, নাকি JavaScript engine?""",
        a_en=r"""None of those: Node.js is a **runtime** that lets you run JavaScript outside the browser, mostly for servers and tools. It is built on Google's V8 engine (which executes the JavaScript) plus libuv (event loop and async I/O), and it adds server APIs such as `fs`, `http` and `process` instead of browser APIs like `window` and the DOM.""",
        a_bn=r"""কোনোটাই না: Node.js হলো একটা **runtime**, যেটা browser-এর বাইরে JavaScript চালাতে দেয়, মূলত server আর tool বানাতে। এটা Google-এর V8 engine (যেটা JavaScript execute করে) আর libuv (event loop ও async I/O) দিয়ে তৈরি, আর browser-এর `window` বা DOM-এর বদলে `fs`, `http`, `process`-এর মতো server API দেয়।""",
        code=r"""
            console.log(typeof window);  // → undefined (no browser globals)
            console.log(typeof process, typeof require('node:fs').readFile);
            // → object function
        """, lang="javascript",
        ex_en=r"""V8 is the engine; Node.js wraps it. Express, NestJS and Next.js are frameworks that run *on* Node.js.""",
        ex_bn=r"""Engine হলো V8; Node.js সেটাকে ঘিরে তৈরি। Express, NestJS, Next.js হলো framework, যেগুলো Node.js-এর *উপর* চলে।""",
        tip_en=r"""Say "runtime built on V8 and libuv", never "a JavaScript engine": interviewers listen for that distinction.""",
        tip_bn=r"""বলো "V8 আর libuv-এর উপর তৈরি runtime", কখনো "JavaScript engine" বোলো না: interviewer ঠিক এই পার্থক্যটাই শুনতে চায়।""",
        mist_en=r"""Calling Node.js a programming language or "the V8 engine". JavaScript is the language and V8 is the engine.""",
        mist_bn=r"""Node.js-কে programming language বা "V8 engine" বলা। Language হলো JavaScript, আর engine হলো V8।""",
        follow=[("What does libuv do inside Node.js?", "Node.js-এর ভেতরে libuv কী কাজ করে?")],
        related=["node-001"],
        refs=[NODE_INTRO],
    ),
    # ------------------------------------------------------------------ node-q02
    Q(
        id="node-q02", sub="Node.js Runtime", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["single-threaded", "non-blocking-io", "async"],
        ver=VER, vs=False, status="stable",
        q_en=r"""Is Node.js single-threaded? What does "non-blocking I/O" mean?""",
        q_bn=r"""Node.js কি single-threaded? "Non-blocking I/O" মানে কী?""",
        a_en=r"""Your JavaScript runs on one main thread, but Node.js as a whole is not single-threaded: libuv's thread pool and the OS handle I/O in the background. Non-blocking means an I/O call like `fs.readFile` starts the work and returns immediately, so the thread keeps serving other requests, and the result arrives later through a callback or promise.""",
        a_bn=r"""আমাদের JavaScript একটা main thread-এ চলে, কিন্তু পুরো Node.js single-threaded নয়: libuv-এর thread pool আর OS background-এ I/O সামলায়। Non-blocking মানে `fs.readFile`-এর মতো I/O call কাজটা শুরু করেই সাথে সাথে return করে, ফলে thread অন্য request serve করতে থাকে, আর result পরে callback বা promise দিয়ে আসে।""",
        code=r"""
            const fs = require('node:fs');
            console.log('start');
            fs.readFile(__filename, () => console.log('file read'));
            console.log('end');
            // → start, end, file read
        """, lang="javascript",
        ex_en=r"""The flip side: CPU-heavy synchronous code (a huge loop, `readFileSync` in a request handler) blocks that one thread, so every other request waits.""",
        ex_bn=r"""উল্টো দিকটা হলো: CPU-heavy synchronous code (বিশাল loop, request handler-এ `readFileSync`) ওই একটা thread আটকে দেয়, তাই বাকি সব request অপেক্ষা করে।""",
        tip_en=r"""Answer "JavaScript runs on one thread, I/O doesn't block it", then name the risk: blocking the event loop.""",
        tip_bn=r"""উত্তর দাও "JavaScript একটা thread-এ চলে, I/O সেটাকে আটকায় না", তারপর ঝুঁকিটা বলো: event loop block হওয়া।""",
        follow=[("What happens to other users if one request runs a 3-second synchronous loop?", "একটা request ৩ সেকেন্ডের synchronous loop চালালে অন্য user-দের কী হয়?")],
        related=["node-001", "node-006"],
        refs=[NODE_BLOCKING],
    ),
    # ------------------------------------------------------------------ node-q03
    Q(
        id="node-q03", sub="Event Loop", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["event-loop", "microtasks", "settimeout"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the event loop in Node.js? Explain it in one breath.""",
        q_bn=r"""Node.js-এ event loop কী? এক নিঃশ্বাসে ব্যাখ্যা করো।""",
        a_en=r"""The event loop is the loop that keeps a Node.js process running: once the synchronous code finishes, it repeatedly picks up ready callbacks (timers, finished I/O, `setImmediate`) and runs them one at a time on the main thread. Between callbacks, Node first empties the `process.nextTick` queue and the promise microtask queue.""",
        a_bn=r"""Event loop হলো সেই loop যেটা Node.js process-কে চালু রাখে: synchronous code শেষ হলে এটা বারবার প্রস্তুত callback-গুলো (timer, শেষ হওয়া I/O, `setImmediate`) তুলে নিয়ে main thread-এ একটা একটা করে চালায়। দুই callback-এর মাঝে Node আগে `process.nextTick` queue আর promise microtask queue খালি করে।""",
        code=r"""
            setTimeout(() => console.log('timeout'), 0);
            Promise.resolve().then(() => console.log('promise'));
            console.log('sync');
            // → sync, promise, timeout
        """, lang="javascript",
        ex_en=r"""The main phases are timers → poll (I/O) → check (`setImmediate`) → close callbacks. When nothing is left to wait for, the process exits.""",
        ex_bn=r"""মূল phase-গুলো: timers → poll (I/O) → check (`setImmediate`) → close callbacks। অপেক্ষা করার মতো কিছু না থাকলে process বন্ধ হয়ে যায়।""",
        tip_en=r"""Give the one-line definition, then the order "sync → nextTick → promises → timers/I/O" with the three-line example.""",
        tip_bn=r"""এক লাইনের definition দাও, তারপর তিন লাইনের example দিয়ে order বলো: "sync → nextTick → promise → timer/I/O"।""",
        follow=[("Why does a promise callback run before a `setTimeout(fn, 0)` callback?", "`setTimeout(fn, 0)`-এর আগে promise callback কেন চলে?")],
        related=["node-002", "node-004", "node-013"],
        refs=[NODE_EVENT_LOOP],
    ),
    # ------------------------------------------------------------------ node-q04
    Q(
        id="node-q04", sub="Package Management (npm)", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["npm", "package-json", "lockfile"],
        ver="npm 11 (ships with Node.js 24+)", vs=False, status="stable",
        q_en=r"""What are npm, `package.json` and `package-lock.json`?""",
        q_bn=r"""npm, `package.json` আর `package-lock.json` কী?""",
        a_en=r"""npm is Node's default package manager. `package.json` describes your project: name, scripts and the dependency **ranges** you allow (like `^5.3.0`). `package-lock.json` records the **exact** version of every installed package, including nested ones, so everyone installs the same tree; commit both files.""",
        a_bn=r"""npm হলো Node-এর default package manager। `package.json` project-এর বর্ণনা দেয়: নাম, script, আর কোন dependency-র কোন **range** চলবে (যেমন `^5.3.0`)। `package-lock.json` প্রতিটা install হওয়া package-এর (nested-সহ) **exact** version লিখে রাখে, যাতে সবাই একই tree install করে; দুটো file-ই commit করো।""",
        code=r"""
            npm install express        # adds to "dependencies" + updates the lockfile
            npm install -D typescript  # adds to "devDependencies" (build/test only)
            npm ci                     # CI/Docker: installs exactly what the lockfile says
            npm run dev                # runs the "dev" script from package.json
        """, lang="bash",
        ex_en=r"""`dependencies` are needed at runtime; `devDependencies` only for building and testing. Never edit `node_modules` and don't commit it.""",
        ex_bn=r"""`dependencies` runtime-এ লাগে; `devDependencies` শুধু build আর test-এর জন্য। `node_modules` কখনো edit কোরো না, commit-ও কোরো না।""",
        tip_en=r"""Contrast them in one line: "`package.json` says what I allow, the lockfile says what I actually got".""",
        tip_bn=r"""এক লাইনে পার্থক্য বলো: "`package.json` বলে আমি কী allow করি, lockfile বলে আমি আসলে কী পেয়েছি"।""",
        follow=[("What is the difference between `npm install` and `npm ci`?", "`npm install` আর `npm ci`-এর পার্থক্য কী?")],
        related=["node-009", "node-010"],
        refs=[NPM_PACKAGE_JSON],
    ),
    # ------------------------------------------------------------------ node-q05
    Q(
        id="node-q05", sub="Modules (ESM & CommonJS)", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["require", "import", "esm", "commonjs"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `require` and `import` in Node.js?""",
        q_bn=r"""Node.js-এ `require` আর `import`-এর পার্থক্য কী?""",
        a_en=r"""`require()` and `module.exports` belong to CommonJS, Node's original module system: loaded synchronously and callable anywhere. `import`/`export` are ES modules, the JavaScript standard: static, strict mode, with top-level `await`. A `.js` file is ESM when `package.json` has `"type": "module"` (or it's `.mjs`); new projects usually use ESM.""",
        a_bn=r"""`require()` আর `module.exports` হলো CommonJS, Node-এর পুরোনো module system: synchronously load হয়, যেকোনো জায়গায় call করা যায়। `import`/`export` হলো ES module, JavaScript-এর standard: static, strict mode, top-level `await` চলে। `package.json`-এ `"type": "module"` থাকলে (বা file `.mjs` হলে) `.js` file ESM হয়; নতুন project-এ সাধারণত ESM ব্যবহার হয়।""",
        code=r"""
            // math.cjs (CommonJS)
            module.exports = { add: (a, b) => a + b };
            // app.cjs
            const { add } = require('./math.cjs');

            // math.mjs (ES module)
            export const add = (a, b) => a + b;
            // app.mjs
            import { add } from './math.mjs';  // extension required
        """, lang="javascript",
        ex_en=r"""ESM can import CommonJS packages. Since Node 22.12, CommonJS can also `require()` an ES module, as long as it has no top-level `await`.""",
        ex_bn=r"""ESM থেকে CommonJS package import করা যায়। Node 22.12 থেকে CommonJS-ও ES module `require()` করতে পারে, যদি তাতে top-level `await` না থাকে।""",
        tip_en=r"""Mention how Node decides (`"type"` field or `.mjs`/`.cjs`); that's the follow-up interviewers usually ask.""",
        tip_bn=r"""Node কীভাবে ঠিক করে সেটাও বলো (`"type"` field বা `.mjs`/`.cjs`); interviewer সাধারণত এটাই পরের প্রশ্নে জিজ্ঞেস করে।""",
        follow=[("How do you get `__dirname` in an ES module?", "ES module-এ `__dirname` কীভাবে পাবে?")],
        related=["node-008"],
        refs=[NODE_ESM],
    ),
    # ------------------------------------------------------------------ node-q06
    Q(
        id="node-q06", sub="Processes & Environment Variables", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["process-env", "dotenv", "env-file", "config"],
        ver="Node.js 26 LTS / 24 (--env-file stable since v24.10 / v22.21)", vs=True, status="stable",
        q_en=r"""What is `process.env`, and how do you use a `.env` file in Node.js?""",
        q_bn=r"""`process.env` কী, আর Node.js-এ `.env` file কীভাবে ব্যবহার করো?""",
        a_en=r"""`process.env` is an object holding the process's environment variables, used for config that changes per environment (port, database URL, API keys). For local development, Node can load a `.env` file itself with `node --env-file=.env app.js`, so the `dotenv` package is no longer needed. Every value is a **string**, so convert and validate it.""",
        a_bn=r"""`process.env` হলো process-এর environment variable রাখা একটা object, যেটা environment অনুযায়ী বদলানো config-এর জন্য ব্যবহার হয় (port, database URL, API key)। Local development-এ Node নিজেই `node --env-file=.env app.js` দিয়ে `.env` file load করতে পারে, তাই এখন আর `dotenv` package লাগে না। সব value **string**, তাই convert আর validate করে নিতে হয়।""",
        code=r"""
            // .env  →  PORT=4000
            // run:     node --env-file=.env app.js
            console.log(process.env.PORT, typeof process.env.PORT); // → 4000 string
            const port = Number(process.env.PORT ?? 3000);
            console.log(port + 1);                                  // → 4001
        """, lang="javascript",
        ex_en=r"""Never commit `.env` (commit a `.env.example` instead). In production, the platform or a secrets manager sets real environment variables.""",
        ex_bn=r"""`.env` কখনো commit কোরো না (তার বদলে `.env.example` commit করো)। Production-এ আসল environment variable platform বা secrets manager set করে।""",
        tip_en=r"""Mention the string gotcha (`'false'` is truthy) and that secrets stay out of Git.""",
        tip_bn=r"""String-এর ফাঁদটা বলো (`'false'` truthy) আর বলো যে secret Git-এ যায় না।""",
        follow=[("Why is `if (process.env.DEBUG)` true when `DEBUG=false`?", "`DEBUG=false` হলেও `if (process.env.DEBUG)` কেন true হয়?")],
        related=["node-015"],
        refs=[NODE_ENV_VARS],
    ),
    # ------------------------------------------------------------------ node-q07
    Q(
        id="node-q07", sub="Streams", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["streams", "pipeline", "memory"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are streams in Node.js, and why use them?""",
        q_bn=r"""Node.js-এ stream কী, আর কেন ব্যবহার করা হয়?""",
        a_en=r"""A stream processes data piece by piece (in chunks) instead of loading it all into memory, so a 5 GB file uses only a few kilobytes of memory at a time. There are four types: **Readable** (file read, HTTP request), **Writable** (file write, HTTP response), **Duplex** (TCP socket) and **Transform** (gzip). Connect them with `pipeline()`.""",
        a_bn=r"""Stream পুরো data একবারে memory-তে না এনে টুকরো টুকরো (chunk) করে process করে, তাই 5 GB file-এও একসাথে মাত্র কয়েক kilobyte memory লাগে। চার ধরনের stream: **Readable** (file read, HTTP request), **Writable** (file write, HTTP response), **Duplex** (TCP socket) আর **Transform** (gzip)। এগুলো `pipeline()` দিয়ে জোড়া দাও।""",
        code=r"""
            import { createReadStream, createWriteStream } from 'node:fs';
            import { createGzip } from 'node:zlib';
            import { pipeline } from 'node:stream/promises';

            await pipeline(createReadStream('big.log'), createGzip(), createWriteStream('big.log.gz'));
            console.log('done'); // → done (memory stays small for any file size)
        """, lang="javascript",
        ex_en=r"""`pipeline()` also handles backpressure (pauses a fast reader for a slow writer) and destroys every stream if one fails.""",
        ex_bn=r"""`pipeline()` backpressure-ও সামলায় (ধীর writer-এর জন্য দ্রুত reader-কে থামায়), আর কোনো একটা fail করলে সব stream destroy করে।""",
        tip_en=r"""Name the four types with one real example each, then say "I connect them with `pipeline()`".""",
        tip_bn=r"""চার ধরনের নাম একটা করে বাস্তব example-সহ বলো, তারপর বলো "আমি এগুলো `pipeline()` দিয়ে জুড়ি"।""",
        follow=[("What is backpressure?", "Backpressure কী?")],
        related=["node-005", "node-011"],
        refs=[NODE_STREAM],
    ),
    # ------------------------------------------------------------------ node-q08
    Q(
        id="node-q08", sub="Asynchronous Programming", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["callbacks", "error-first", "promises", "async-await"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is an error-first callback, and what replaced it in modern Node.js code?""",
        q_bn=r"""Error-first callback কী, আর আধুনিক Node.js code-এ এর জায়গা কী নিয়েছে?""",
        a_en=r"""In Node's classic callback style, the callback's first argument is the error (`null` on success) and the result comes next: `(err, data) => {}`. Nesting many of them leads to "callback hell", so modern code uses the promise APIs (`node:fs/promises`) with `async`/`await` and `try/catch`.""",
        a_bn=r"""Node-এর পুরোনো callback style-এ callback-এর প্রথম argument হলো error (সফল হলে `null`), তারপর result: `(err, data) => {}`। অনেকগুলো nest করলে "callback hell" হয়, তাই আধুনিক code-এ promise API (`node:fs/promises`) আর `async`/`await` ও `try/catch` ব্যবহার করা হয়।""",
        code=r"""
            const fs = require('node:fs');
            fs.readFile('missing.txt', 'utf8', (err, data) => {
              if (err) return console.log('error:', err.code); // → error: ENOENT
              console.log(data);
            });
            // modern: try { await readFile(...) } catch (err) { ... } from 'node:fs/promises'
        """, lang="javascript",
        ex_en=r"""Always check `err` first and `return`. A `try/catch` around a callback-style call does not catch errors raised later inside the callback.""",
        ex_bn=r"""সবসময় আগে `err` check করে `return` করো। Callback-style call-এর চারপাশে `try/catch` দিলে পরে callback-এর ভেতরে হওয়া error ধরা পড়ে না।""",
        tip_en=r"""Show the `(err, data)` signature, then say you use `fs/promises` and `async`/`await` today (`util.promisify` for old APIs).""",
        tip_bn=r"""`(err, data)` signature দেখাও, তারপর বলো এখন তুমি `fs/promises` আর `async`/`await` ব্যবহার করো (পুরোনো API-র জন্য `util.promisify`)।""",
        follow=[("What does `util.promisify` do?", "`util.promisify` কী করে?")],
        related=["node-027", "node-030"],
        refs=[NODE_CALLBACKS],
    ),
    # ------------------------------------------------------------------ node-q09
    Q(
        id="node-q09", sub="EventEmitter", diff="easy", type="quick",
        prio="medium", market="both", mins=2,
        tags=["eventemitter", "events", "on", "once"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is `EventEmitter` in Node.js?""",
        q_bn=r"""Node.js-এ `EventEmitter` কী?""",
        a_en=r"""`EventEmitter` from `node:events` is Node's built-in publish/subscribe class: you register listeners with `on()` (or `once()` for a single call) and trigger them with `emit()`. Listeners run synchronously, in the order they were added. Streams, HTTP servers and sockets are all EventEmitters.""",
        a_bn=r"""`node:events`-এর `EventEmitter` হলো Node-এর built-in publish/subscribe class: `on()` দিয়ে listener register করো (একবারের জন্য `once()`), আর `emit()` দিয়ে সেগুলো চালাও। Listener-গুলো synchronously, যোগ করার ক্রমে চলে। Stream, HTTP server, socket সবই EventEmitter।""",
        code=r"""
            const { EventEmitter } = require('node:events');
            const orders = new EventEmitter();
            orders.on('created', (id) => console.log('send email for', id));
            orders.once('created', (id) => console.log('first order:', id));
            orders.emit('created', 1); // → send email for 1, first order: 1
            orders.emit('created', 2); // → send email for 2
        """, lang="javascript",
        ex_en=r"""Gotcha: emitting `'error'` with no `'error'` listener throws and can crash the process. Remove listeners you no longer need (`off()`) to avoid leaks.""",
        ex_bn=r"""ফাঁদ: কোনো `'error'` listener ছাড়া `'error'` emit করলে throw হয় আর process crash করতে পারে। Leak এড়াতে অপ্রয়োজনীয় listener `off()` দিয়ে সরাও।""",
        tip_en=r"""Define it as pub/sub, then mention the special `'error'` event; that shows real-world experience.""",
        tip_bn=r"""এটাকে pub/sub হিসেবে define করো, তারপর বিশেষ `'error'` event-এর কথা বলো; এতে বাস্তব অভিজ্ঞতা বোঝা যায়।""",
        follow=[("Are EventEmitter listeners called synchronously or asynchronously?", "EventEmitter-এর listener synchronously চলে, নাকি asynchronously?")],
        related=["node-016", "node-023"],
        refs=[NODE_EVENTS],
    ),
    # ------------------------------------------------------------------ node-q10
    Q(
        id="node-q10", sub="Error Handling", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["uncaughtexception", "process", "crash", "error-handling"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is `process.on('uncaughtException')`, and should you use it to keep the server running?""",
        q_bn=r"""`process.on('uncaughtException')` কী, আর server চালু রাখতে কি এটা ব্যবহার করা উচিত?""",
        a_en=r"""It is a last-resort handler for errors that nothing caught; without it Node prints the stack and exits with code 1. Don't use it to keep running: after an unknown error the app may be in a broken state. Log the error, clean up quickly, call `process.exit(1)`, and let a process manager (Docker, Kubernetes, PM2) restart it.""",
        a_bn=r"""এটা হলো সেইসব error-এর শেষ handler যেগুলো কেউ catch করেনি; এটা না থাকলে Node stack print করে exit code 1 দিয়ে বন্ধ হয়। Server চালু রাখতে এটা ব্যবহার কোরো না: অজানা error-এর পরে app ভাঙা অবস্থায় থাকতে পারে। Error log করো, দ্রুত cleanup করো, `process.exit(1)` call করো, আর process manager (Docker, Kubernetes, PM2)-কে restart করতে দাও।""",
        code=r"""
            process.on('uncaughtException', (err) => {
              console.error('fatal:', err.message); // → fatal: boom
              process.exit(1);                      // exit; the process manager restarts it
            });
            setTimeout(() => { throw new Error('boom'); }, 10);
        """, lang="javascript",
        ex_en=r"""Unhandled promise rejections also crash the process by default (`--unhandled-rejections=throw`). Handle expected errors where they happen, with `try/catch` or `.catch()`.""",
        ex_bn=r"""Unhandled promise rejection-ও default-এ process crash করায় (`--unhandled-rejections=throw`)। প্রত্যাশিত error যেখানে ঘটে সেখানেই `try/catch` বা `.catch()` দিয়ে সামলাও।""",
        tip_en=r"""Say "log, clean up, exit, restart" and explain why resuming is unsafe.""",
        tip_bn=r"""বলো "log, cleanup, exit, restart", আর ব্যাখ্যা করো কেন আবার চালিয়ে যাওয়া নিরাপদ নয়।""",
        mist_en=r"""Adding an `uncaughtException` handler that only logs, so the server keeps running with corrupted state.""",
        mist_bn=r"""শুধু log করে এমন `uncaughtException` handler রাখা, ফলে server নষ্ট state নিয়ে চলতেই থাকে।""",
        follow=[("What happens by default when a promise rejection is never handled?", "কোনো promise rejection কখনো handle না হলে default-এ কী হয়?")],
        related=["node-012", "node-020"],
        refs=[NODE_PROCESS],
    ),
]

save("nodejs", "quick", QUESTIONS)
