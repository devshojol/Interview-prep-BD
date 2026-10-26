import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NODE_BUFFER = ("Node.js API — Buffer", "https://nodejs.org/api/buffer.html")
NODE_RELEASES = ("Node.js — Releases (LTS schedule)", "https://nodejs.org/en/about/previous-releases")
NODE_EVENTS = ("Node.js API — Events (setMaxListeners)", "https://nodejs.org/api/events.html")
NODE_HTTP = ("Node.js API — HTTP", "https://nodejs.org/api/http.html")
NODE_TS = ("Node.js API — Modules: TypeScript", "https://nodejs.org/api/typescript.html")
NODE_PERMISSIONS = ("Node.js API — Permissions", "https://nodejs.org/api/permissions.html")
NODE_SEC_BP = ("Node.js Learn — Security Best Practices", "https://nodejs.org/en/learn/getting-started/security-best-practices")
OWASP_NPM = ("OWASP — NPM Security Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/NPM_Security_Cheat_Sheet.html")
NODE_CLUSTER = ("Node.js API — Cluster", "https://nodejs.org/api/cluster.html")
NODE_OS = ("Node.js API — os (availableParallelism)", "https://nodejs.org/api/os.html")

QUESTIONS = [
    # ------------------------------------------------------------------ node-021
    Q(
        id="node-021", sub="Buffers", diff="easy", type="output",
        prio="medium", market="bangladesh", mins=3,
        tags=["buffer", "utf-8", "encoding", "bytelength", "output"],
        ver="Version-independent (Node.js 26 LTS / 24)", vs=False, status="stable",
        q_en=r"""What does this script print? (The first string is the Bangla word `বাংলা`.)""",
        q_bn=r"""এই script কী print করবে? (প্রথম string-টি বাংলা শব্দ `বাংলা`।)""",
        a_en=r"""
            It prints `5`, `15`, `<Buffer 48 69 21>`, `SGkh` and `3`.

            `word.length` counts UTF-16 code units — `বাংলা` is five code points (`ব`, `া`, `ং`, `ল`, `া`), each one code unit. `Buffer.byteLength` counts bytes after UTF-8 encoding, and each of those Bangla characters takes 3 bytes, so 15. `Buffer.from('Hi!')` stores the bytes 0x48, 0x69, 0x21, which encode to `SGkh` in base64, and a Buffer's `length` is its size in bytes (3).
        """,
        a_bn=r"""
            Output হবে `5`, `15`, `<Buffer 48 69 21>`, `SGkh` আর `3`।

            `word.length` UTF-16 code unit গোনে — `বাংলা`-তে পাঁচটি code point (`ব`, `া`, `ং`, `ল`, `া`), প্রতিটি একটি করে code unit। `Buffer.byteLength` UTF-8 encode করার পর byte গোনে, আর এই প্রতিটি বাংলা character-এ 3 byte লাগে, তাই 15। `Buffer.from('Hi!')` byte 0x48, 0x69, 0x21 রাখে, base64-এ যা `SGkh`, আর Buffer-এর `length` হলো byte-এ তার size (3)।
        """,
        quick_en=r"""It prints `5`, `15`, `<Buffer 48 69 21>`, `SGkh`, `3`. A string's `length` counts UTF-16 code units (5), `Buffer.byteLength` counts UTF-8 bytes (3 per Bangla character, so 15), and `Hi!` is the bytes 48 69 21, which is `SGkh` in base64 and 3 bytes long.""",
        quick_bn=r"""Print হবে `5`, `15`, `<Buffer 48 69 21>`, `SGkh`, `3`। String-এর `length` UTF-16 code unit গোনে (5), `Buffer.byteLength` UTF-8 byte গোনে (প্রতিটা বাংলা অক্ষর 3 byte, তাই 15), আর `Hi!` হলো byte 48 69 21, যেটা base64-এ `SGkh` এবং length 3 byte।""",
        ex_en=r"""
            - **What a Buffer is:** a fixed-size sequence of raw bytes (a `Uint8Array` subclass). Node uses it for files, sockets, crypto and compression — anything binary.
            - **Why it matters in real code:** the HTTP `Content-Length` header, database column limits and protocol frames are in **bytes**, not characters. Using `str.length` for Bangla, emoji or any non-ASCII text gives wrong sizes.
            - **Splitting is dangerous:** cutting a Buffer in the middle of a multi-byte character produces `�` when decoded. When decoding streamed chunks, use `setEncoding('utf8')`, `StringDecoder`, or `TextDecoder` with `{ stream: true }`.
            - **`Buffer.alloc(n)` vs `Buffer.allocUnsafe(n)`:** `alloc` zero-fills; `allocUnsafe` is faster but may contain old memory contents, so only use it when you overwrite every byte.
            - Large Buffers live outside the V8 heap (`external` / `arrayBuffers` in `process.memoryUsage()`), which is why RSS can grow while `heapUsed` stays flat.
        """,
        ex_bn=r"""
            - **Buffer কী:** raw byte-এর একটি নির্দিষ্ট আকারের sequence (`Uint8Array`-এর subclass)। File, socket, crypto, compression — যেকোনো binary কাজে Node এটা ব্যবহার করে।
            - **বাস্তব code-এ কেন জরুরি:** HTTP `Content-Length` header, database column limit আর protocol frame — সবই **byte**-এ মাপা হয়, character-এ নয়। বাংলা, emoji বা যেকোনো non-ASCII text-এ `str.length` ব্যবহার করলে ভুল size আসে।
            - **ভাগ করা বিপজ্জনক:** multi-byte character-এর মাঝখানে Buffer কাটলে decode করার সময় `�` আসে। Stream-এর chunk decode করার সময় `setEncoding('utf8')`, `StringDecoder`, বা `{ stream: true }` সহ `TextDecoder` ব্যবহার করো।
            - **`Buffer.alloc(n)` বনাম `Buffer.allocUnsafe(n)`:** `alloc` শূন্য দিয়ে ভরে; `allocUnsafe` দ্রুত কিন্তু পুরনো memory-র content থাকতে পারে, তাই শুধু তখনই ব্যবহার করো যখন প্রতিটি byte overwrite করবে।
            - বড় Buffer V8 heap-এর বাইরে থাকে (`process.memoryUsage()`-এ `external` / `arrayBuffers`), এজন্যই `heapUsed` স্থির থাকলেও RSS বাড়তে পারে।
        """,
        tip_en=r"""Use the Bangla example to make the byte-vs-character point — it's memorable and directly relevant to apps that store Bangla text.""",
        tip_bn=r"""Byte বনাম character-এর বিষয়টা বোঝাতে বাংলা উদাহরণ ব্যবহার করো — এটা মনে রাখার মতো এবং বাংলা text রাখা app-এর জন্য সরাসরি প্রাসঙ্গিক।""",
        mist_en=r"""Assuming one character equals one byte, or computing `Content-Length` with `body.length` for a string body.""",
        mist_bn=r"""এক character মানে এক byte ধরে নেওয়া, অথবা string body-র জন্য `body.length` দিয়ে `Content-Length` হিসাব করা।""",
        code=r"""
            const word = 'বাংলা';
            console.log(word.length);
            console.log(Buffer.byteLength(word));

            const buf = Buffer.from('Hi!');
            console.log(buf);
            console.log(buf.toString('base64'));
            console.log(buf.length);
        """,
        lang="javascript",
        output=r"""
            5
            15
            <Buffer 48 69 21>
            SGkh
            3
        """,
        follow=[
            ("How would you safely decode UTF-8 text that arrives in arbitrary stream chunks?", "যেকোনো আকারের stream chunk-এ আসা UTF-8 text নিরাপদে কীভাবে decode করবে?"),
            ("When is `Buffer.allocUnsafe` acceptable?", "কখন `Buffer.allocUnsafe` ব্যবহার করা চলে?"),
        ],
        related=["node-005"],
        refs=[NODE_BUFFER],
    ),
    # ------------------------------------------------------------------ node-022
    Q(
        id="node-022", sub="LTS Release Model", diff="easy", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["lts", "release-schedule", "versions", "production"],
        ver="Node.js release schedule as of 2026-10-26 (v26 Active LTS from 2026-10-28, v24 Maintenance LTS)", vs=True, status="version-specific",
        q_en=r"""It is November 2026 and you are starting a new production API. Which Node.js release line should you choose by default?""",
        q_bn=r"""এখন নভেম্বর 2026, তুমি একটি নতুন production API শুরু করছ। Default হিসেবে কোন Node.js release line বেছে নেবে?""",
        options=[
            ("Node.js 27, because its alpha has the newest features", "Node.js 27, কারণ এর alpha-তে সবচেয়ে নতুন feature আছে"),
            ("Node.js 26, the Active LTS line", "Node.js 26, যেটা Active LTS line"),
            ("Node.js 25, because odd-numbered releases get the longest support", "Node.js 25, কারণ odd-numbered release সবচেয়ে বেশি দিন support পায়"),
            ("Node.js 20, because older LTS lines are the most battle-tested", "Node.js 20, কারণ পুরনো LTS line সবচেয়ে বেশি পরীক্ষিত"),
        ],
        correct=1,
        a_en=r"""
            **B**: Node.js 26. The Node.js project says production applications should only use Active LTS or Maintenance LTS releases. v26 was promoted to Active LTS on 28 October 2026, so it's the natural default for a new project: it gets fixes and backports for the longest time. v24 is still supported, but it entered Maintenance LTS on 20 October 2026 (security and critical fixes only, until 30 April 2028), so it suits existing apps rather than new ones.
        """,
        a_bn=r"""
            **B**: Node.js 26। Node.js project-এর নির্দেশনা হলো production application-এ শুধু Active LTS বা Maintenance LTS release ব্যবহার করা। v26 28 অক্টোবর 2026-এ Active LTS হয়েছে, তাই নতুন project-এর জন্য এটাই স্বাভাবিক default: এটা সবচেয়ে বেশি দিন fix আর backport পাবে। v24 এখনও supported, কিন্তু 20 অক্টোবর 2026-এ Maintenance LTS-এ চলে গেছে (30 এপ্রিল 2028 পর্যন্ত শুধু security আর critical fix), তাই এটা নতুন app-এর চেয়ে চালু app-এর জন্য বেশি মানানসই।
        """,
        quick_en=r"""Node.js 26: it became Active LTS on 28 October 2026, and production apps should run only Active or Maintenance LTS lines. Node.js 24 is still supported but is in Maintenance LTS (security and critical fixes only), so it suits existing apps rather than new ones.""",
        quick_bn=r"""Node.js 26: এটা 28 October 2026-এ Active LTS হয়েছে, আর production app-এ শুধু Active বা Maintenance LTS line চালানো উচিত। Node.js 24 এখনো supported, কিন্তু Maintenance LTS-এ আছে (শুধু security ও critical fix), তাই এটা নতুন নয়, পুরোনো app-এর জন্য মানানসই।""",
        ex_en=r"""
            - **Option A (Node 27)** is the most common wrong choice. Under the new release model, 27 starts as an **alpha** on 28 October 2026 and only ships as 27.0.0 in April 2027. Alpha and Current releases get new features (and occasionally breaking changes), and libraries may not support them yet, so they aren't a production default.
            - Until Node 26, **odd-numbered releases never became LTS**: v25 is already end-of-life (option C is backwards).
            - **v20 reached end-of-life on 30 April 2026**, so it no longer gets security fixes (option D). v22 is in Maintenance LTS until 30 April 2027, and v24 until 30 April 2028: fine for existing apps, not ideal for new ones.
            - **New model from Node 27:** one major release per year (April), an alpha phase before it, and *every* release becomes LTS in October. The even/odd rule disappears.
            - Practical habit: pin the major in `engines`, `.nvmrc` and your Docker image tag, and plan upgrades before a line leaves Maintenance.
        """,
        ex_bn=r"""
            - **Option A (Node 27)** হলো সবচেয়ে বেশি বেছে নেওয়া ভুল উত্তর। নতুন release model-এ 27 শুরু হয় **alpha** হিসেবে, 28 অক্টোবর 2026-এ, আর 27.0.0 হিসেবে আসে এপ্রিল 2027-এ। Alpha আর Current release নতুন feature (আর মাঝে মাঝে breaking change) পায়, library-গুলো হয়তো তখনও support করে না, তাই production-এর default হিসেবে এগুলো চলে না।
            - Node 26 পর্যন্ত **odd-numbered release কখনো LTS হয়নি**: v25 ইতিমধ্যে end-of-life (option C উল্টো কথা)।
            - **v20 30 এপ্রিল 2026-এ end-of-life** হয়েছে, তাই আর security fix পায় না (option D)। v22 30 এপ্রিল 2027 পর্যন্ত আর v24 30 এপ্রিল 2028 পর্যন্ত Maintenance LTS-এ: চালু app-এর জন্য ঠিক আছে, নতুন app-এর জন্য আদর্শ নয়।
            - **Node 27 থেকে নতুন model:** বছরে একটি major release (এপ্রিলে), তার আগে একটি alpha phase, আর *প্রতিটি* release অক্টোবরে LTS হবে। Even/odd নিয়ম আর থাকবে না।
            - বাস্তব অভ্যাস: `engines`, `.nvmrc` আর Docker image tag-এ major version pin করো, আর কোনো line Maintenance থেকে বের হওয়ার আগেই upgrade-এর পরিকল্পনা করো।
        """,
        tip_en=r"""Quote the rule ("production → Active or Maintenance LTS") and then show you know the calendar: which line is LTS now, and that the even/odd scheme ends with Node 27.""",
        tip_bn=r"""নিয়মটা বলো ("production → Active বা Maintenance LTS"), তারপর দেখাও তুমি calendar জানো: এখন কোন line LTS, আর Node 27 থেকে even/odd পদ্ধতি শেষ হচ্ছে।""",
        follow=[
            ("What's the difference between Active LTS and Maintenance LTS?", "Active LTS আর Maintenance LTS-এর মধ্যে পার্থক্য কী?"),
            ("Your team runs Node.js 24 in production. When should you plan the upgrade to 26, and how?", "তোমার team production-এ Node.js 24 চালায়। 26-এ upgrade-এর পরিকল্পনা কখন আর কীভাবে করবে?"),
        ],
        refs=[NODE_RELEASES],
    ),
    # ------------------------------------------------------------------ node-023
    Q(
        id="node-023", sub="EventEmitter", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["eventemitter", "memory-leak", "sse", "listeners", "maxlisteners"],
        ver="Node.js 26 LTS / 24; Express 5.x", vs=False, status="stable",
        q_en=r"""This Server-Sent Events endpoint pushes price updates to browsers. After a few hours in production the logs show `MaxListenersExceededWarning: Possible EventEmitter memory leak detected`, memory keeps growing, and there are occasional "write after end" errors. What's wrong, and how do you fix it?""",
        q_bn=r"""এই Server-Sent Events endpoint browser-এ price update push করে। Production-এ কয়েক ঘণ্টা পর log-এ দেখা যায় `MaxListenersExceededWarning: Possible EventEmitter memory leak detected`, memory বাড়তেই থাকে, আর মাঝে মাঝে "write after end" error আসে। সমস্যা কী, আর কীভাবে ঠিক করবে?""",
        a_en=r"""
            Every request adds a new `'price'` listener to a shared, long-lived emitter, and nothing ever removes it. When a client disconnects, its listener stays registered — and because the listener's closure references `res`, the whole response object (and its socket state) can't be garbage-collected. That's the memory growth. The next price event still calls the dead client's listener, which writes to a closed response — the "write after end" errors. The warning appears once more than 10 listeners are attached to one event.

            Fix: keep a reference to the handler and remove it when the response closes (`res.on('close', ...)` fires both on normal completion and when the client disconnects). Only after the cleanup is correct, raise the limit with `setMaxListeners()` if you legitimately expect many concurrent subscribers.
        """,
        a_bn=r"""
            প্রতিটি request একটি shared, দীর্ঘজীবী emitter-এ নতুন `'price'` listener যোগ করে, আর কেউ কখনো সেটা remove করে না। Client disconnect হলেও তার listener register করা থেকে যায় — আর listener-এর closure `res`-কে reference করে বলে পুরো response object (আর তার socket state) garbage-collect হতে পারে না। এটাই memory বাড়ার কারণ। পরের price event-এ মৃত client-এর listener-ও call হয়, যা বন্ধ response-এ লিখতে চায় — এটাই "write after end" error। এক event-এ 10টির বেশি listener লাগলে warning দেখা যায়।

            Fix: handler-এর reference রাখো এবং response close হলে সেটা remove করো (`res.on('close', ...)` স্বাভাবিকভাবে শেষ হলে এবং client disconnect হলে — দুই ক্ষেত্রেই fire হয়)। Cleanup ঠিক হওয়ার পরেই, যদি সত্যিই অনেক subscriber একসাথে আশা করো, তবে `setMaxListeners()` দিয়ে limit বাড়াও।
        """,
        quick_en=r"""Every request adds a `'price'` listener to a shared emitter and nothing removes it, so listeners of disconnected clients keep their `res` alive: memory grows, the warning fires past 10 listeners, and dead responses get written to. Fix: remove the listener in `res.on('close')`.""",
        quick_bn=r"""প্রতিটা request shared emitter-এ একটা `'price'` listener যোগ করে কিন্তু কেউ সেটা সরায় না, তাই disconnect হওয়া client-এর listener তাদের `res` বাঁচিয়ে রাখে: memory বাড়ে, 10টার বেশি listener হলে warning আসে, আর বন্ধ response-এ write হয়। সমাধান: `res.on('close')`-এ listener সরাও।""",
        ex_en=r"""
            - **The warning is a hint, not the bug.** Calling `setMaxListeners(0)` first just hides the symptom while memory keeps leaking.
            - **Anonymous listeners can't be removed** — `off()` needs the same function reference, so store it in a variable.
            - **`res.on('close')` vs `req.on('close')`:** both fire when a GET client disconnects, but `res`'s `'close'` is documented as "response completed or connection terminated", so it's the more reliable hook for response-scoped cleanup.
            - **Alternatives:** keep connected clients in a `Set` and broadcast by iterating it (one listener total), or use `events.on(emitter, 'price', { signal })` with an `AbortController` tied to the response.
            - **Scale-out note:** with several instances, a local EventEmitter only sees local events; publish price updates through Redis Pub/Sub (or similar) and let each instance fan out to its own clients.
        """,
        ex_bn=r"""
            - **Warning হলো ইঙ্গিত, bug নয়।** আগেই `setMaxListeners(0)` দিলে শুধু symptom লুকায়, memory leak চলতেই থাকে।
            - **Anonymous listener remove করা যায় না** — `off()`-এর জন্য একই function reference লাগে, তাই সেটা variable-এ রাখো।
            - **`res.on('close')` বনাম `req.on('close')`:** GET client disconnect হলে দুটোই fire হয়, কিন্তু `res`-এর `'close'`-কে documentation-এ বলা হয়েছে "response সম্পূর্ণ বা connection বিচ্ছিন্ন", তাই response-কেন্দ্রিক cleanup-এর জন্য এটাই বেশি নির্ভরযোগ্য।
            - **বিকল্প:** connected client-দের একটি `Set`-এ রেখে iterate করে broadcast করা (মোট একটি listener), অথবা response-এর সাথে যুক্ত `AbortController` সহ `events.on(emitter, 'price', { signal })` ব্যবহার করা।
            - **Scale-out নোট:** কয়েকটি instance থাকলে local EventEmitter শুধু local event দেখে; price update Redis Pub/Sub (বা এ জাতীয় কিছু) দিয়ে publish করো, আর প্রতিটি instance নিজের client-দের কাছে পাঠাক।
        """,
        tip_en=r"""Explain the chain: listener per request → closure retains `res` → no removal → leak + writes to dead sockets. Then say clearly that raising the max listeners is not the fix.""",
        tip_bn=r"""শৃঙ্খলটা ব্যাখ্যা করো: প্রতি request-এ listener → closure `res` ধরে রাখে → remove হয় না → leak + মৃত socket-এ write। তারপর স্পষ্ট বলো যে max listener বাড়ানো fix নয়।""",
        mist_en=r"""Silencing the warning with `setMaxListeners(0)` or `process.removeAllListeners('warning')` instead of removing listeners on disconnect.""",
        mist_bn=r"""Disconnect-এ listener remove না করে `setMaxListeners(0)` বা `process.removeAllListeners('warning')` দিয়ে warning চুপ করিয়ে দেওয়া।""",
        code=r"""
            import express from 'express';
            import { EventEmitter } from 'node:events';

            const app = express();
            export const priceUpdates = new EventEmitter(); // shared, lives forever

            app.get('/prices/stream', (req, res) => {
              res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' });
              res.flushHeaders();

              priceUpdates.on('price', (price) => {
                res.write(`data: ${JSON.stringify(price)}\n\n`);
              });
            });

            app.listen(3000);
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                app.get('/prices/stream', (req, res) => {
                  res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' });
                  res.flushHeaders();

                  const onPrice = (price) => res.write(`data: ${JSON.stringify(price)}\n\n`);
                  priceUpdates.on('price', onPrice);

                  // Fires when the response ends or the client disconnects
                  res.on('close', () => {
                    priceUpdates.off('price', onPrice);
                  });
                });

                // Many concurrent subscribers are legitimate here, so raise the limit
                // only AFTER cleanup is correct (keeps the warning useful for real leaks).
                priceUpdates.setMaxListeners(5_000);
            """, label_en="Fixed version", label_bn="সংশোধিত version"),
        ],
        follow=[
            ("How would you broadcast these events across multiple Node instances?", "একাধিক Node instance-এ এই event কীভাবে broadcast করবে?"),
            ("How can you find which code added the extra listeners?", "কোন code বাড়তি listener যোগ করেছে কীভাবে খুঁজে বের করবে?"),
        ],
        related=["node-014", "node-016"],
        refs=[NODE_EVENTS, NODE_HTTP],
    ),
    # ------------------------------------------------------------------ node-024
    Q(
        id="node-024", sub="Modules (ESM & CommonJS)", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["typescript", "type-stripping", "erasable-syntax", "tooling"],
        ver="Node.js 26 LTS / 24.12+ (type stripping stable)", vs=True, status="stable",
        q_en=r"""Node.js 24.12+ and 26 can run TypeScript files directly with built-in type stripping (`node app.ts`, no flags). Which of these files runs without a TypeScript-related error?""",
        q_bn=r"""Node.js 24.12+ ও 26 built-in type stripping দিয়ে সরাসরি TypeScript file চালাতে পারে (`node app.ts`, কোনো flag ছাড়া)। নিচের কোন file TypeScript-সংক্রান্ত কোনো error ছাড়া চলবে?""",
        options=[
            ("A file that declares `enum Role { Admin, User }` and uses `Role.Admin`", "যে file `enum Role { Admin, User }` declare করে এবং `Role.Admin` ব্যবহার করে"),
            ("A file with `interface User { id: number }`, typed function parameters and `import type { Server } from 'node:http'`", "যে file-এ `interface User { id: number }`, typed function parameter আর `import type { Server } from 'node:http'` আছে"),
            ("A class that uses a parameter property: `constructor(private repo: UserRepo) {}`", "যে class parameter property ব্যবহার করে: `constructor(private repo: UserRepo) {}`"),
            ("A file that imports `@/utils/date` through a `paths` alias defined in `tsconfig.json`", "যে file `tsconfig.json`-এ define করা `paths` alias দিয়ে `@/utils/date` import করে"),
        ],
        correct=1,
        a_en=r"""
            The file with interfaces, type annotations and `import type`. Type stripping only removes **erasable** syntax — it replaces types with whitespace and runs the remaining JavaScript. Interfaces, type aliases, annotations and type-only imports disappear cleanly, so that file runs.
        """,
        a_bn=r"""
            Interface, type annotation আর `import type` থাকা file-টি। Type stripping শুধু **erasable** syntax সরায় — type-গুলোকে whitespace দিয়ে replace করে বাকি JavaScript চালায়। Interface, type alias, annotation আর type-only import পরিষ্কারভাবে মুছে যায়, তাই ওই file চলে।
        """,
        quick_en=r"""The file with interfaces, type annotations and `import type`: built-in type stripping only erases type-only syntax and runs the remaining JavaScript. Enums and parameter properties generate runtime code, so they fail, and Node never reads `tsconfig.json`, so `paths` aliases don't resolve.""",
        quick_bn=r"""Interface, type annotation আর `import type` থাকা file-টা: built-in type stripping শুধু type-এর syntax মুছে দিয়ে বাকি JavaScript চালায়। Enum আর parameter property runtime code তৈরি করে, তাই সেগুলো fail করে, আর Node কখনো `tsconfig.json` পড়ে না, তাই `paths` alias resolve হয় না।""",
        ex_en=r"""
            - **Enums and parameter properties** (options A and C) generate runtime JavaScript, so they can't just be erased — Node throws `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` (verified). Same for namespaces with runtime code and import aliases. These options are tempting because NestJS-style code uses them everywhere — such projects still need a compiler or a tool like `tsx`.
            - **Node never reads `tsconfig.json`** (option D), so `paths` aliases don't resolve; use package.json subpath imports (`#utils/date.ts`) instead.
            - **No type checking happens.** Run `tsc --noEmit` in CI (TypeScript 7's native compiler makes this fast).
            - Imports need real extensions (`./user.ts`), type-only imports must use `import type`, and `.tsx` is not supported.
            - Helpful tsconfig settings: `erasableSyntaxOnly`, `verbatimModuleSyntax`, `allowImportingTsExtensions`.
            - Timeline: enabled by default in v23.6 / v22.18, stable in v25.2 / v24.12; `--experimental-transform-types` was removed in v26.
        """,
        ex_bn=r"""
            - **Enum আর parameter property** (option A ও C) runtime JavaScript তৈরি করে, তাই এগুলো শুধু মুছে ফেলা যায় না — Node `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` throw করে (যাচাই করা)। Runtime code সহ namespace আর import alias-এর ক্ষেত্রেও একই। এই option-গুলো প্রলোভনের, কারণ NestJS-ধাঁচের code-এ এগুলো সর্বত্র — এমন project-এ এখনও compiler বা `tsx`-এর মতো tool লাগে।
            - **Node কখনো `tsconfig.json` পড়ে না** (option D), তাই `paths` alias resolve হয় না; এর বদলে package.json-এর subpath import (`#utils/date.ts`) ব্যবহার করো।
            - **কোনো type checking হয় না।** CI-তে `tsc --noEmit` চালাও (TypeScript 7-এর native compiler এটাকে দ্রুত করেছে)।
            - Import-এ আসল extension লাগে (`./user.ts`), type-only import-এ `import type` লাগে, আর `.tsx` support নেই।
            - কাজের tsconfig setting: `erasableSyntaxOnly`, `verbatimModuleSyntax`, `allowImportingTsExtensions`।
            - Timeline: v23.6 / v22.18-এ default-ভাবে চালু, v25.2 / v24.12-এ stable; v26-এ `--experimental-transform-types` সরিয়ে দেওয়া হয়েছে।
        """,
        tip_en=r"""Use the phrase "erasable syntax only" and add "it doesn't type-check, so `tsc --noEmit` still runs in CI". Those two sentences cover what interviewers want to hear.""",
        tip_bn=r""""Erasable syntax only" কথাটা বলো এবং যোগ করো "এটা type-check করে না, তাই CI-তে এখনও `tsc --noEmit` চলে"। Interviewer যা শুনতে চায়, এই দুই বাক্যেই তা এসে যায়।""",
        refs=[NODE_TS],
    ),
    # ------------------------------------------------------------------ node-025
    Q(
        id="node-025", sub="Security", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["security", "supply-chain", "npm-audit", "permission-model", "prototype-pollution"],
        ver="Node.js 26 LTS / 24 (permission model stable for fs since v23.5 / v22.13)", vs=True, status="stable",
        q_en=r"""How do you protect a Node.js service against its main runtime and supply-chain risks? Include what Node's permission model (`--permission`) does — and what it does not protect against.""",
        q_bn=r"""একটি Node.js service-কে তার প্রধান runtime ও supply-chain ঝুঁকি থেকে কীভাবে রক্ষা করবে? Node-এর permission model (`--permission`) কী করে — এবং কীসের বিরুদ্ধে রক্ষা করে না — সেটাও বলো।""",
        a_en=r"""
            I think about it in layers:

            **1. Supply chain (usually the biggest risk).** Commit the lockfile and install with `npm ci`; run `npm audit` (or Dependabot/Renovate alerts) in CI and fail on high/critical issues; keep dependencies few and vet new ones (maintainers, activity, install scripts, typosquatted names); consider `npm ci --ignore-scripts` and only rebuild packages that truly need native builds; use scoped/private registries correctly to avoid dependency confusion; enable 2FA and trusted publishing for packages we publish.

            **2. Runtime and platform.** Stay on a supported LTS and apply Node security releases quickly; run as a non-root user in a minimal container; give the process only the secrets it needs and never log them.

            **3. Application code.** Validate all input with a schema; parameterised queries; no `eval`/`new Function` on user data; `execFile`/`spawn` with argument arrays instead of `exec`; guard against **prototype pollution** (don't deep-merge untrusted objects, block `__proto__`/`constructor` keys, use `Map` or `Object.create(null)` for dictionaries); avoid ReDoS-prone regexes; limit body sizes and set server timeouts.

            **4. Permission model as a seat belt.** `node --permission --allow-fs-read=/app --allow-fs-write=/app/uploads server.js` restricts file system access, child processes, worker threads, native addons and WASI (and, on Node 25+/26, network access unless `--allow-net` is passed). It stops *trusted* code from accidentally touching things it shouldn't. But the docs are explicit: it **does not protect against malicious code**, which can bypass it. Real isolation for untrusted code needs OS/container-level sandboxing.
        """,
        a_bn=r"""
            আমি স্তরে স্তরে চিন্তা করি:

            **1. Supply chain (সাধারণত সবচেয়ে বড় ঝুঁকি)।** Lockfile commit করে `npm ci` দিয়ে install; CI-তে `npm audit` (বা Dependabot/Renovate alert) চালিয়ে high/critical issue-তে build fail করানো; dependency কম রাখা এবং নতুনগুলো যাচাই করা (maintainer, activity, install script, typosquat করা নাম); `npm ci --ignore-scripts` বিবেচনা করা এবং শুধু যেসব package-এর সত্যিই native build লাগে সেগুলো rebuild করা; dependency confusion এড়াতে scoped/private registry সঠিকভাবে ব্যবহার করা; নিজেদের publish করা package-এ 2FA আর trusted publishing চালু রাখা।

            **2. Runtime ও platform।** Supported LTS-এ থাকা এবং Node security release দ্রুত apply করা; minimal container-এ non-root user হিসেবে চালানো; process-কে শুধু দরকারি secret দেওয়া এবং কখনো log না করা।

            **3. Application code।** সব input schema দিয়ে validate; parameterised query; user data-র উপর `eval`/`new Function` নয়; `exec`-এর বদলে argument array সহ `execFile`/`spawn`; **prototype pollution** ঠেকানো (untrusted object deep-merge না করা, `__proto__`/`constructor` key block করা, dictionary-র জন্য `Map` বা `Object.create(null)`); ReDoS-প্রবণ regex এড়ানো; body size সীমিত করা ও server timeout set করা।

            **4. Seat belt হিসেবে permission model।** `node --permission --allow-fs-read=/app --allow-fs-write=/app/uploads server.js` file system access, child process, worker thread, native addon আর WASI সীমিত করে (আর Node 25+/26-এ `--allow-net` না দিলে network access-ও)। এটা *trusted* code-কে ভুলবশত অনাকাঙ্ক্ষিত জিনিস ছোঁয়া থেকে আটকায়। কিন্তু docs স্পষ্ট বলে: এটা **malicious code-এর বিরুদ্ধে রক্ষা করে না**, malicious code একে bypass করতে পারে। Untrusted code-এর আসল isolation-এর জন্য OS/container-level sandboxing লাগে।
        """,
        quick_en=r"""Defend in layers: supply chain first (lockfile + `npm ci`, `npm audit` in CI, few vetted dependencies), then a patched LTS running as non-root, then safe code (validation, no `eval`, no prototype pollution). `--permission` restricts what trusted code can touch, but it does not protect against malicious code.""",
        quick_bn=r"""কয়েকটা layer-এ সুরক্ষা দাও: আগে supply chain (lockfile + `npm ci`, CI-তে `npm audit`, অল্প আর যাচাই করা dependency), তারপর non-root হিসেবে চলা patched LTS, তারপর নিরাপদ code (validation, `eval` নয়, prototype pollution ঠেকানো)। `--permission` trusted code কী ছুঁতে পারবে তা সীমিত করে, কিন্তু malicious code থেকে রক্ষা করে না।""",
        ex_en=r"""
            - **Status details:** the permission model and the `--allow-fs-*` flags are stable since v23.5 / v22.13; `--allow-child-process`, `--allow-worker` and `--allow-net` (added in v25) are still marked "active development". On Node 24 there is no network restriction at all.
            - **`npm audit` limits:** it only knows published advisories, reports many unreachable issues, and can't detect a freshly compromised package. Pair it with lockfile review, provenance (`npm audit signatures`) and minimal dependencies.
            - **Why prototype pollution matters:** one polluted property (e.g. `isAdmin`) appears on *every* object in the process, which can bypass authorization checks or crash the app. See the extra snippet.
            - **DoS hygiene:** body-size limits, `server.requestTimeout`/`headersTimeout`, rate limiting and safe regexes protect the single event loop, which is a shared resource for all users.
            - **Secrets:** use pino's `redact` (or similar) so tokens and passwords never reach logs.
        """,
        ex_bn=r"""
            - **Status-এর খুঁটিনাটি:** permission model আর `--allow-fs-*` flag v23.5 / v22.13 থেকে stable; `--allow-child-process`, `--allow-worker` আর `--allow-net` (v25-এ যোগ হয়েছে) এখনও "active development" হিসেবে চিহ্নিত। Node 24-এ network-এর উপর কোনো restriction নেই।
            - **`npm audit`-এর সীমা:** এটা শুধু publish হওয়া advisory জানে, অনেক unreachable issue report করে, আর সদ্য compromise হওয়া package ধরতে পারে না। এর সাথে lockfile review, provenance (`npm audit signatures`) আর কম dependency রাখো।
            - **Prototype pollution কেন গুরুত্বপূর্ণ:** একটি polluted property (যেমন `isAdmin`) process-এর *প্রতিটি* object-এ দেখা দেয়, যা authorization check bypass করতে বা app crash করাতে পারে। Extra snippet দেখো।
            - **DoS-এর বিরুদ্ধে অভ্যাস:** body-size limit, `server.requestTimeout`/`headersTimeout`, rate limiting আর নিরাপদ regex — এগুলো একক event loop-কে রক্ষা করে, যা সব user-এর shared resource।
            - **Secret:** pino-র `redact` (বা এ জাতীয় কিছু) ব্যবহার করো, যাতে token আর password কখনো log-এ না পৌঁছায়।
        """,
        tip_en=r"""Lead with supply chain — it's where real Node incidents come from — then code-level issues, then the permission model with its "seat belt, not sandbox" caveat. Quoting that limitation correctly is a strong senior signal.""",
        tip_bn=r"""Supply chain দিয়ে শুরু করো — Node-এর আসল incident বেশিরভাগ সেখান থেকেই আসে — তারপর code-level issue, তারপর permission model ও তার "seat belt, sandbox নয়" সীমাবদ্ধতা। এই সীমাবদ্ধতা সঠিকভাবে বলতে পারা senior হওয়ার শক্ত ইঙ্গিত।""",
        mist_en=r"""Treating `--permission` as a sandbox for untrusted plugins, or treating a clean `npm audit` as proof that dependencies are safe.""",
        mist_bn=r"""Untrusted plugin-এর জন্য `--permission`-কে sandbox মনে করা, অথবা `npm audit` পরিষ্কার এলে dependency নিরাপদ বলে ধরে নেওয়া।""",
        code=r"""
            # Supply-chain hygiene in CI
            npm ci --ignore-scripts          # no lifecycle scripts from dependencies
            npm rebuild sharp                # explicitly allow the few that need native builds
            npm audit --audit-level=high     # fail on high/critical advisories
            npm audit signatures             # verify registry signatures / provenance

            # Seat belt for trusted code (Node 24 / 26)
            node --permission \
              --allow-fs-read=/app \
              --allow-fs-write=/app/uploads \
              server.js
            # Node 25+ / 26: network is denied under --permission unless you add --allow-net
        """,
        lang="bash",
        extra=[
            dict(lang="javascript", src=r"""
                // Vulnerable: naive deep merge of user-controlled JSON
                function merge(target, source) {
                  for (const key of Object.keys(source)) {
                    if (typeof source[key] === 'object' && source[key] !== null) {
                      target[key] ??= {};
                      merge(target[key], source[key]);
                    } else {
                      target[key] = source[key];
                    }
                  }
                  return target;
                }

                const userInput = JSON.parse('{"theme": "dark", "__proto__": {"isAdmin": true}}');
                merge({}, userInput);
                console.log({}.isAdmin); // true  <- every object is now "admin"

                // Fix: skip dangerous keys (better: validate input with a strict schema first)
                const FORBIDDEN = new Set(['__proto__', 'constructor', 'prototype']);
                // ...inside the loop: if (FORBIDDEN.has(key)) continue;
            """, label_en="Prototype pollution in a naive deep merge", label_bn="সাধারণ deep merge-এ prototype pollution"),
        ],
        follow=[
            ("What is dependency confusion, and how do scoped packages help?", "Dependency confusion কী, আর scoped package কীভাবে সাহায্য করে?"),
            ("How would you safely run user-supplied scripts or plugins?", "User-এর দেওয়া script বা plugin নিরাপদে কীভাবে চালাবে?"),
        ],
        related=["node-010", "node-017"],
        refs=[NODE_PERMISSIONS, NODE_SEC_BP, OWASP_NPM],
    ),
    # ------------------------------------------------------------------ node-026
    Q(
        id="node-026", sub="Performance & Scalability", diff="hard", type="architecture",
        prio="high", market="both", mins=12,
        tags=["scalability", "cluster", "stateless", "load-balancing", "redis", "connection-pool"],
        ver="Node.js 26 LTS / 24", vs=False, status="stable",
        q_en=r"""Your Node.js API runs as a single process on an 8-vCPU VM. At peak, one core sits at 100% while the others are idle, and latency climbs. How would you scale it — first across cores, then across machines — and what has to change in the application itself?""",
        q_bn=r"""তোমার Node.js API একটি 8-vCPU VM-এ একটি মাত্র process হিসেবে চলে। Peak সময়ে একটি core 100%-এ থাকে, বাকিগুলো অলস, আর latency বাড়তে থাকে। প্রথমে core-জুড়ে, তারপর machine-জুড়ে কীভাবে scale করবে — আর application-এর ভেতরে কী কী বদলাতে হবে?""",
        a_en=r"""
            First I'd confirm the CPU is spent on legitimate work and not on one blocking hot path (profile it) — scaling a bug just multiplies it. Then:

            **Across cores (one machine):** run one process per core — `node:cluster`, PM2 cluster mode (`pm2 start server.js -i max`), or simply N containers. The OS/primary distributes connections, and a supervisor restarts crashed workers.

            **Across machines:** put stateless instances behind a load balancer (NGINX or a cloud ALB) and autoscale on CPU, latency or request rate. In Kubernetes/ECS I run one Node process per container and let the orchestrator handle restarts and scaling.

            **What must change — make every instance disposable and stateless:**
            - Sessions → Redis/database (or signed tokens), not in-process memory.
            - Caches → Redis, or accept per-process caches with short TTLs and pub/sub invalidation.
            - Rate limiting → a shared store (Redis), otherwise each process counts separately.
            - WebSockets/Socket.IO → sticky sessions where needed plus a Redis adapter so broadcasts reach all instances.
            - Scheduled jobs → run once (a dedicated worker or queue scheduler), not in every process.
            - Uploads → object storage, not local disk.
            - **Database connections:** pool size × number of processes must stay below the DB's connection limit — shrink per-process pools and add PgBouncer/RDS Proxy.
        """,
        a_bn=r"""
            প্রথমে নিশ্চিত হব CPU আসলেই বৈধ কাজে খরচ হচ্ছে, কোনো একটি blocking hot path-এ নয় (profile করে) — একটি bug-কে scale করলে সেটা শুধু গুণিত হয়। তারপর:

            **Core-জুড়ে (এক machine):** প্রতি core-এ একটি process — `node:cluster`, PM2 cluster mode (`pm2 start server.js -i max`), অথবা সরাসরি N-টি container। OS/primary connection ভাগ করে দেয়, আর একজন supervisor crash হওয়া worker restart করে।

            **Machine-জুড়ে:** stateless instance-গুলোকে load balancer-এর (NGINX বা cloud ALB) পেছনে রাখা এবং CPU, latency বা request rate দেখে autoscale করা। Kubernetes/ECS-এ আমি প্রতি container-এ একটি Node process চালাই এবং restart ও scaling orchestrator-কে করতে দিই।

            **যা বদলাতে হবে — প্রতিটি instance-কে disposable আর stateless বানানো:**
            - Session → in-process memory নয়, Redis/database (বা signed token)।
            - Cache → Redis, অথবা ছোট TTL আর pub/sub invalidation সহ per-process cache মেনে নেওয়া।
            - Rate limiting → shared store (Redis), না হলে প্রতিটি process আলাদা গোনে।
            - WebSocket/Socket.IO → দরকার হলে sticky session আর Redis adapter, যাতে broadcast সব instance-এ পৌঁছায়।
            - Scheduled job → প্রতিটি process-এ নয়, একবারই চালানো (dedicated worker বা queue scheduler)।
            - Upload → local disk নয়, object storage।
            - **Database connection:** pool size × process সংখ্যা DB-র connection limit-এর নিচে থাকতে হবে — per-process pool ছোট করো এবং PgBouncer/RDS Proxy যোগ করো।
        """,
        quick_en=r"""First profile it to make sure it's real work, not a blocking bug. Then run one process per core (`node:cluster`, PM2 or containers) and stateless instances behind a load balancer, with sessions, caches, rate limits and scheduled jobs in shared stores like Redis, and DB connections kept under the limit.""",
        quick_bn=r"""আগে profile করে নিশ্চিত হও যে এটা আসল কাজ, কোনো blocking bug নয়। তারপর প্রতি core-এ একটা process চালাও (`node:cluster`, PM2 বা container) আর load balancer-এর পেছনে stateless instance রাখো; session, cache, rate limit আর scheduled job Redis-এর মতো shared store-এ রাখো, আর DB connection limit-এর নিচে রাখো।""",
        ex_en=r"""
            **Trade-offs:**
            - **cluster/PM2 on one VM:** simple and cheap, but the VM is a single failure domain and deploys need care (`pm2 reload` for rolling restarts).
            - **Containers + orchestrator:** better isolation, autoscaling and rolling deploys, but more moving parts. Running `cluster` *inside* each container usually just complicates resource limits and health checks.
            - **Memory:** each process has its own V8 heap; 8 processes × 500 MB is 4 GB. Size `--max-old-space-size` and container limits together.

            **Failure scenarios:** a crashed worker should be replaced automatically; a hot shard of traffic (one big tenant) may need separate capacity; Redis becomes a new critical dependency — plan for its failure (timeouts, fallbacks).

            **Observability:** include the instance/pid in logs, aggregate metrics per instance, and propagate request IDs so a request can be traced across services.
        """,
        ex_bn=r"""
            **Trade-off:**
            - **এক VM-এ cluster/PM2:** সহজ ও সস্তা, কিন্তু VM-টি একটি single failure domain এবং deploy-এ সতর্কতা লাগে (rolling restart-এর জন্য `pm2 reload`)।
            - **Container + orchestrator:** ভালো isolation, autoscaling আর rolling deploy, কিন্তু চলমান অংশ বেশি। প্রতিটি container-এর *ভেতরে* `cluster` চালালে সাধারণত resource limit আর health check শুধু জটিল হয়।
            - **Memory:** প্রতিটি process-এর নিজস্ব V8 heap; 8টি process × 500 MB মানে 4 GB। `--max-old-space-size` আর container limit একসাথে ঠিক করো।

            **Failure scenario:** crash হওয়া worker স্বয়ংক্রিয়ভাবে প্রতিস্থাপিত হওয়া উচিত; traffic-এর একটি hot অংশ (একটি বড় tenant)-এর জন্য আলাদা capacity লাগতে পারে; Redis একটি নতুন critical dependency হয়ে যায় — তার failure-এর পরিকল্পনা রাখো (timeout, fallback)।

            **Observability:** log-এ instance/pid রাখো, instance অনুযায়ী metric aggregate করো, আর request ID propagate করো যাতে একটি request service-জুড়ে trace করা যায়।
        """,
        tip_en=r"""The scaling mechanics are easy; what interviewers probe is the *state* checklist. Go through sessions, caches, rate limits, sockets, cron, uploads and DB connections — and mention the connection-pool multiplication explicitly.""",
        tip_bn=r"""Scaling-এর কৌশল সহজ; interviewer আসলে যাচাই করে *state*-এর checklist। Session, cache, rate limit, socket, cron, upload আর DB connection — একে একে বলো, আর connection pool গুণিত হওয়ার কথা স্পষ্টভাবে উল্লেখ করো।""",
        mist_en=r"""Scaling out while keeping in-memory sessions or rate-limit counters, or running the same cron job in every instance (duplicate emails, double charges).""",
        mist_bn=r"""In-memory session বা rate-limit counter রেখেই scale out করা, অথবা প্রতিটি instance-এ একই cron job চালানো (duplicate email, দুবার charge)।""",
        code=r"""
            // primary.js — one worker process per CPU (useful on a plain VM)
            import cluster from 'node:cluster';
            import { availableParallelism } from 'node:os';

            if (cluster.isPrimary) {
              for (let i = 0; i < availableParallelism(); i++) cluster.fork();

              cluster.on('exit', (worker, code, signal) => {
                console.warn(`worker ${worker.process.pid} died (${signal ?? code}); starting a new one`);
                cluster.fork();
              });
            } else {
              await import('./server.js'); // each worker runs the same HTTP server on the shared port
            }
        """,
        lang="javascript",
        follow=[
            ("How do you size the database pool when you have 12 instances?", "12টি instance থাকলে database pool-এর size কীভাবে ঠিক করবে?"),
            ("Why do Socket.IO deployments often need sticky sessions?", "Socket.IO deployment-এ কেন প্রায়ই sticky session লাগে?"),
        ],
        related=["node-017", "node-006", "node-020"],
        refs=[NODE_CLUSTER, NODE_OS],
    ),
]

if __name__ == "__main__":
    save("nodejs", "b4", QUESTIONS)
