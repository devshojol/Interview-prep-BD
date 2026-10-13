import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NODE_ESM = ("Node.js API — ECMAScript modules", "https://nodejs.org/api/esm.html")
NODE_CJS = ("Node.js API — CommonJS modules (require(esm))", "https://nodejs.org/api/modules.html")
NODE_PACKAGES = ("Node.js API — Packages (type field, detection)", "https://nodejs.org/api/packages.html")
NPM_SEMVER = ("npm Docs — About semantic versioning", "https://docs.npmjs.com/about-semantic-versioning")
NPM_CI = ("npm Docs — npm ci", "https://docs.npmjs.com/cli/v11/commands/npm-ci")
NPM_LOCK = ("npm Docs — package-lock.json", "https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json")
NODE_STREAM = ("Node.js API — Stream (pipeline)", "https://nodejs.org/api/stream.html")
NODE_ZLIB = ("Node.js API — Zlib", "https://nodejs.org/api/zlib.html")
NODE_PROCESS = ("Node.js API — process events", "https://nodejs.org/api/process.html")
NODE_CLI = ("Node.js API — Command-line options", "https://nodejs.org/api/cli.html")
NODE_EVENT_LOOP = ("Node.js Learn — The Node.js Event Loop", "https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick")
NODE_HEAP_SNAPSHOT = ("Node.js Learn — Using Heap Snapshot", "https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot")
NODE_V8 = ("Node.js API — v8 (writeHeapSnapshot)", "https://nodejs.org/api/v8.html")

QUESTIONS = [
    # ------------------------------------------------------------------ node-008
    Q(
        id="node-008", sub="Modules (ESM & CommonJS)", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["esm", "commonjs", "require-esm", "import-meta", "modules"],
        ver="Node.js 24 LTS / 26", vs=True, status="stable",
        q_en=r"""Compare CommonJS and ES modules in Node.js. How does Node decide which module system a file uses, and can the two be mixed?""",
        q_bn=r"""Node.js-এ CommonJS আর ES module-এর তুলনা করো। একটি file কোন module system ব্যবহার করবে Node সেটা কীভাবে ঠিক করে, আর দুটো কি একসাথে ব্যবহার করা যায়?""",
        a_en=r"""
            - **CommonJS (CJS):** `require()` / `module.exports`, loaded synchronously, `__dirname` and `__filename` available, `require` can be called anywhere at runtime.
            - **ES modules (ESM):** `import` / `export`, static structure that tools can analyse, top-level `await`, strict mode by default, relative imports need the file extension, and `import.meta.dirname` / `import.meta.filename` replace `__dirname` / `__filename`.

            **How Node decides:** `.mjs` is always ESM, `.cjs` is always CJS, and `.js` follows the nearest `package.json` `"type"` field (`"module"` → ESM, missing or `"commonjs"` → CJS). If there's no `"type"`, current Node also sniffs the syntax, but I always set `"type"` explicitly.

            **Mixing:** ESM can `import` a CJS module (its `module.exports` becomes the default export). Since Node 22.12 / 20.19, CJS can also `require()` an ES module, as long as that module graph has no top-level `await`; otherwise use `await import()`. For new projects I use ESM.
        """,
        a_bn=r"""
            - **CommonJS (CJS):** `require()` / `module.exports`, synchronous ভাবে load হয়, `__dirname` ও `__filename` পাওয়া যায়, runtime-এ যেকোনো জায়গায় `require` call করা যায়।
            - **ES module (ESM):** `import` / `export`, static structure যা tool analyse করতে পারে, top-level `await`, default-ভাবে strict mode, relative import-এ file extension লাগে, আর `__dirname` / `__filename`-এর বদলে `import.meta.dirname` / `import.meta.filename`।

            **Node কীভাবে ঠিক করে:** `.mjs` সবসময় ESM, `.cjs` সবসময় CJS, আর `.js` file সবচেয়ে কাছের `package.json`-এর `"type"` field দেখে (`"module"` → ESM, না থাকলে বা `"commonjs"` হলে → CJS)। `"type"` না থাকলে current Node syntax দেখে আন্দাজও করে, কিন্তু আমি সবসময় `"type"` স্পষ্ট করে দিই।

            **একসাথে ব্যবহার:** ESM থেকে CJS module `import` করা যায় (তার `module.exports` default export হয়ে যায়)। Node 22.12 / 20.19 থেকে CJS-ও ES module `require()` করতে পারে, যদি সেই module graph-এ top-level `await` না থাকে; থাকলে `await import()` ব্যবহার করতে হয়। নতুন project-এ আমি ESM ব্যবহার করি।
        """,
        ex_en=r"""
            - **`require(esm)` details:** it returns the module namespace object, so a default export is at `.default`. A module with top-level `await` (anywhere in its import graph) throws `ERR_REQUIRE_ASYNC_MODULE`. The feature was unflagged in v22.12 / v20.19 and marked stable in v25.4.
            - **Syntax detection** (treating an ambiguous `.js` file with `import`/`export` as ESM) is on by default since v22.7 / v20.19 but still "release candidate" — another reason to set `"type"` explicitly.
            - **`import.meta.dirname` / `filename`** are no longer experimental since v24.0 / v22.16.
            - **Named imports from CJS** work only when Node can detect the export names statically; `import pkg from 'cjs-lib'` (default import) always works.
            - **Dual packages** use the `"exports"` field with `"import"` and `"require"` conditions — watch out for the "dual package hazard" (two copies of module state).
        """,
        ex_bn=r"""
            - **`require(esm)`-এর খুঁটিনাটি:** এটা module namespace object return করে, তাই default export থাকে `.default`-এ। Import graph-এর কোথাও top-level `await` থাকলে `ERR_REQUIRE_ASYNC_MODULE` throw হয়। Feature-টি v22.12 / v20.19-এ flag ছাড়া চালু হয় এবং v25.4-এ stable ঘোষণা করা হয়।
            - **Syntax detection** (`import`/`export` থাকা ambiguous `.js` file-কে ESM ধরা) v22.7 / v20.19 থেকে default-ভাবে চালু, কিন্তু এখনও "release candidate" — `"type"` স্পষ্ট করে দেওয়ার আরেকটি কারণ।
            - **`import.meta.dirname` / `filename`** v24.0 / v22.16 থেকে আর experimental নয়।
            - **CJS থেকে named import** শুধু তখনই কাজ করে যখন Node static ভাবে export-এর নাম ধরতে পারে; `import pkg from 'cjs-lib'` (default import) সবসময় কাজ করে।
            - **Dual package** `"exports"` field-এ `"import"` ও `"require"` condition ব্যবহার করে — "dual package hazard" (module state-এর দুটি কপি) নিয়ে সতর্ক থাকো।
        """,
        tip_en=r"""Give the decision rules in one breath (".mjs, .cjs, then the type field") and then mention `require(esm)` with its top-level-await limit. That one modern detail shows you're current.""",
        tip_bn=r"""Decision rule-গুলো এক নিঃশ্বাসে বলো (".mjs, .cjs, তারপর type field"), তারপর top-level-await-এর সীমাসহ `require(esm)`-এর কথা বলো। এই একটি আধুনিক detail দেখায় তুমি আপডেটেড।""",
        mist_en=r"""Saying CommonJS can never load ES modules (outdated since v22.12), or using `__dirname` inside an ES module (it's not defined there).""",
        mist_bn=r"""CommonJS কখনোই ES module load করতে পারে না বলা (v22.12 থেকে এটা পুরনো তথ্য), অথবা ES module-এর ভেতরে `__dirname` ব্যবহার করা (সেখানে এটা defined নয়)।""",
        code=r"""
            // utils.mjs (ES module)
            export const greet = (name) => `Hello, ${name}`;
            export default function version() { return '1.0.0'; }
            console.log(import.meta.dirname); // ESM replacement for __dirname

            // legacy.cjs (CommonJS) — works by default on Node 22.12+ / 24 / 26
            const utils = require('./utils.mjs');
            console.log(utils.greet('Rahim'));   // named export
            console.log(utils.default());        // default export lives on .default

            // If the ES module (or anything it imports) uses top-level await:
            // require() throws ERR_REQUIRE_ASYNC_MODULE -> use: const m = await import('./x.mjs');
        """,
        lang="javascript",
        follow=[
            ("What is the dual package hazard?", "Dual package hazard কী?"),
            ("Why do relative ESM imports need the file extension?", "Relative ESM import-এ file extension কেন লাগে?"),
        ],
        related=["node-024"],
        refs=[NODE_ESM, NODE_CJS, NODE_PACKAGES],
    ),
    # ------------------------------------------------------------------ node-009
    Q(
        id="node-009", sub="Package Management (npm)", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["npm", "semver", "caret", "dependencies"],
        ver="npm 11 (ships with Node.js 24+)", vs=False, status="stable",
        q_en=r"""`package.json` contains `"express": "^5.1.0"` and there is no lockfile. Which version may `npm install` choose?""",
        q_bn=r"""`package.json`-এ আছে `"express": "^5.1.0"` এবং কোনো lockfile নেই। `npm install` কোন version বেছে নিতে পারে?""",
        options=[
            ("`5.3.0`", "`5.3.0`"),
            ("`6.0.0`", "`6.0.0`"),
            ("`5.0.1`", "`5.0.1`"),
            ("Only exactly `5.1.0`", "শুধু ঠিক `5.1.0`"),
        ],
        correct=0,
        a_en=r"""
            `5.3.0`. The caret range `^5.1.0` means `>=5.1.0 <6.0.0` — any newer minor or patch release of major version 5, but never a new major. npm picks the highest version that satisfies the range.
        """,
        a_bn=r"""
            সঠিক উত্তর `5.3.0`। Caret range `^5.1.0` মানে `>=5.1.0 <6.0.0` — major version 5-এর যেকোনো নতুন minor বা patch release, কিন্তু কখনো নতুন major নয়। npm range-এর মধ্যে সবচেয়ে উঁচু version বেছে নেয়।
        """,
        ex_en=r"""
            Semantic versioning is `MAJOR.MINOR.PATCH`: breaking changes bump MAJOR, new features MINOR, fixes PATCH.

            - `^5.1.0` → `>=5.1.0 <6.0.0` (minor + patch updates).
            - `~5.1.0` → `>=5.1.0 <5.2.0` (patch updates only).
            - `5.1.0` → exactly that version.
            - For `0.x` versions the caret is stricter: `^0.2.3` → `>=0.2.3 <0.3.0`, because in `0.x` a minor bump may break things.

            `6.0.0` is the tempting wrong answer — the caret never crosses a major version. `5.0.1` is below the lower bound. And "only exactly 5.1.0" is what a **lockfile** gives you, not the range itself — that's why you commit `package-lock.json`.
        """,
        ex_bn=r"""
            Semantic versioning হলো `MAJOR.MINOR.PATCH`: breaking change হলে MAJOR, নতুন feature হলে MINOR, bug fix হলে PATCH বাড়ে।

            - `^5.1.0` → `>=5.1.0 <6.0.0` (minor + patch update)।
            - `~5.1.0` → `>=5.1.0 <5.2.0` (শুধু patch update)।
            - `5.1.0` → ঠিক ওই version।
            - `0.x` version-এ caret আরও কড়া: `^0.2.3` → `>=0.2.3 <0.3.0`, কারণ `0.x`-এ minor bump-ও কিছু ভাঙতে পারে।

            `6.0.0` হলো প্রলোভনের ভুল উত্তর — caret কখনো major version পার হয় না। `5.0.1` lower bound-এর নিচে। আর "শুধু ঠিক 5.1.0" দেয় **lockfile**, range নিজে নয় — এজন্যই `package-lock.json` commit করা হয়।
        """,
        tip_en=r"""Answer with the explicit range (`>=5.1.0 <6.0.0`) and then add the `0.x` caveat — few candidates know it.""",
        tip_bn=r"""উত্তরে স্পষ্ট range (`>=5.1.0 <6.0.0`) বলো, তারপর `0.x`-এর caveat যোগ করো — খুব কম candidate এটা জানে।""",
        refs=[NPM_SEMVER, NPM_LOCK],
    ),
    # ------------------------------------------------------------------ node-010
    Q(
        id="node-010", sub="Package Management (npm)", diff="easy", type="scenario",
        prio="high", market="both", mins=4,
        tags=["npm", "lockfile", "npm-ci", "ci-cd", "reproducible-builds"],
        ver="npm 11 / Node.js 24 LTS", vs=False, status="stable",
        q_en=r"""Code works on a developer's laptop, but the CI build fails because a dependency resolved to a different version, and production sometimes behaves differently from staging. What is likely going on, and how would you make installs reproducible?""",
        q_bn=r"""Code developer-এর laptop-এ ঠিকমতো চলে, কিন্তু CI build fail করছে কারণ একটি dependency অন্য version-এ resolve হয়েছে, আর production মাঝে মাঝে staging থেকে আলাদা আচরণ করে। সম্ভবত কী হচ্ছে, আর install-কে কীভাবে reproducible করবে?""",
        a_en=r"""
            Most likely each environment is resolving version **ranges** at install time instead of installing the exact same dependency tree — for example `package-lock.json` isn't committed (or is in `.gitignore`), CI runs plain `npm install`, or people use different npm/Node versions.

            My fix:

            1. **Commit `package-lock.json`** — it records the exact version and integrity hash of every package, including transitive dependencies.
            2. **Use `npm ci` in CI and Docker builds.** It installs exactly what the lockfile says, deletes `node_modules` first, and fails if `package.json` and the lockfile disagree instead of silently "fixing" it.
            3. **Pin the runtime:** `engines` in `package.json`, an `.nvmrc`, and a specific Node image tag (e.g. `node:24-…`) so everyone uses the same Node and npm.
            4. **Update deliberately:** use Dependabot/Renovate PRs that run tests, rather than drifting versions on random installs.
        """,
        a_bn=r"""
            সম্ভবত প্রতিটি environment install-এর সময় হুবহু একই dependency tree install না করে version **range** resolve করছে — যেমন `package-lock.json` commit করা হয়নি (বা `.gitignore`-এ আছে), CI-তে সাধারণ `npm install` চলছে, অথবা সবাই আলাদা npm/Node version ব্যবহার করছে।

            আমার সমাধান:

            1. **`package-lock.json` commit করা** — এটা প্রতিটি package-এর (transitive dependency সহ) নির্দিষ্ট version আর integrity hash রেকর্ড করে।
            2. **CI ও Docker build-এ `npm ci` ব্যবহার করা।** এটা lockfile-এ যা আছে হুবহু তাই install করে, আগে `node_modules` মুছে দেয়, আর `package.json` ও lockfile না মিললে চুপচাপ "ঠিক" না করে fail করে।
            3. **Runtime pin করা:** `package.json`-এ `engines`, একটি `.nvmrc`, আর নির্দিষ্ট Node image tag (যেমন `node:24-…`), যাতে সবাই একই Node ও npm ব্যবহার করে।
            4. **পরিকল্পিতভাবে update করা:** random install-এ version বদলে যেতে না দিয়ে Dependabot/Renovate-এর PR ব্যবহার করা, যেগুলোতে test চলে।
        """,
        ex_en=r"""
            - **`npm install` vs `npm ci`:** `npm install` may update the lockfile when `package.json` changed and is meant for development; `npm ci` never writes to `package.json` or the lockfile and can't add single packages.
            - **Production images:** `npm ci --omit=dev` keeps dev dependencies out of the runtime image.
            - **Integrity hashes** in the lockfile also protect against a tampered tarball being installed silently.
            - **One package manager per repo:** mixing `yarn.lock` and `package-lock.json` gives two sources of truth.
            - **Libraries vs apps:** a published library's lockfile is not used by its consumers, so libraries must still test against the ranges they declare.
        """,
        ex_bn=r"""
            - **`npm install` বনাম `npm ci`:** `package.json` বদলালে `npm install` lockfile update করতে পারে, এটা development-এর জন্য; `npm ci` কখনো `package.json` বা lockfile-এ লেখে না এবং একক package যোগ করতে পারে না।
            - **Production image:** `npm ci --omit=dev` দিলে dev dependency runtime image-এ ঢোকে না।
            - Lockfile-এর **integrity hash** কোনো tampered tarball চুপচাপ install হওয়া থেকেও রক্ষা করে।
            - **এক repo-তে একটাই package manager:** `yarn.lock` আর `package-lock.json` একসাথে রাখলে সত্যের উৎস দুটো হয়ে যায়।
            - **Library বনাম app:** publish করা library-র lockfile তার consumer-রা ব্যবহার করে না, তাই library-কে তার declare করা range-এর বিরুদ্ধেও test করতে হয়।
        """,
        tip_en=r"""Name the root cause in one sentence ("ranges resolved at different times"), then give the three concrete fixes: commit the lockfile, `npm ci`, pin Node. Interviewers like answers that end in a checklist.""",
        tip_bn=r"""এক বাক্যে মূল কারণ বলো ("ভিন্ন সময়ে range resolve হচ্ছে"), তারপর তিনটি বাস্তব সমাধান দাও: lockfile commit, `npm ci`, Node pin করা। Checklist দিয়ে শেষ হওয়া উত্তর interviewer-রা পছন্দ করে।""",
        mist_en=r"""Deleting `package-lock.json` "to fix conflicts", or pinning every dependency to an exact version in `package.json` while still not committing the lockfile (transitive dependencies still float).""",
        mist_bn=r""""Conflict ঠিক করতে" `package-lock.json` মুছে ফেলা, অথবা `package.json`-এ সব dependency exact version-এ pin করা কিন্তু lockfile commit না করা (transitive dependency তখনও বদলাতে থাকে)।""",
        code=r"""
            # CI / Dockerfile
            npm ci                 # exact, clean install from package-lock.json
            npm ci --omit=dev      # production image without devDependencies

            # Local development (adding/updating packages updates the lockfile)
            npm install zod@4
        """,
        lang="bash",
        follow=[
            ("What does the `integrity` field in the lockfile protect against?", "Lockfile-এর `integrity` field কীসের বিরুদ্ধে সুরক্ষা দেয়?"),
            ("How would you handle a critical security fix in a transitive dependency?", "Transitive dependency-তে জরুরি security fix এলে কীভাবে handle করবে?"),
        ],
        related=["node-009", "node-025"],
        refs=[NPM_CI, NPM_LOCK],
    ),
    # ------------------------------------------------------------------ node-011
    Q(
        id="node-011", sub="Streams", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["streams", "pipeline", "zlib", "transform", "abortsignal"],
        ver="Node.js 24 LTS / 26", vs=False, status="stable",
        q_en=r"""
            Write an async function `compressFile(src, dest, { signal })` that gzips a very large log file (several GB) without loading it into memory.

            Requirements:
            - Return the number of **uncompressed** bytes processed.
            - If anything fails (source missing, disk full, cancelled), reject with the error and delete any half-written output file.
            - Support cancellation through an optional `AbortSignal`.

            Example: `await compressFile('app.log', 'app.log.gz')` resolves to `6754388` for a 6.7 MB file.
        """,
        q_bn=r"""
            একটি async function `compressFile(src, dest, { signal })` লেখো, যা অনেক বড় একটি log file (কয়েক GB) memory-তে load না করেই gzip করবে।

            শর্ত:
            - কত **uncompressed** byte process হয়েছে সেটা return করবে।
            - কিছু fail করলে (source নেই, disk full, cancel হয়েছে) error দিয়ে reject করবে এবং অর্ধেক লেখা output file মুছে ফেলবে।
            - Optional `AbortSignal` দিয়ে cancel করা যাবে।

            উদাহরণ: 6.7 MB-র একটি file-এর জন্য `await compressFile('app.log', 'app.log.gz')` resolve হবে `6754388`-এ।
        """,
        a_en=r"""
            I'd build it as a stream chain with `pipeline()` from `node:stream/promises`: file read stream → a small `Transform` that counts bytes → `createGzip()` → file write stream. `pipeline` handles backpressure between every stage, rejects if any stage errors, destroys all streams so no file descriptors leak, and accepts an `AbortSignal` for cancellation. In the `catch` block I remove the partial `.gz` file and re-throw. Memory stays roughly constant (a few buffers of `highWaterMark` size) no matter how big the file is.
        """,
        a_bn=r"""
            আমি `node:stream/promises`-এর `pipeline()` দিয়ে একটি stream chain বানাব: file read stream → byte গোনার জন্য ছোট একটি `Transform` → `createGzip()` → file write stream। `pipeline` প্রতিটি ধাপের মধ্যে backpressure handle করে, কোনো ধাপে error হলে reject করে, সব stream destroy করে যাতে file descriptor leak না হয়, আর cancel করার জন্য `AbortSignal` নেয়। `catch` block-এ অর্ধেক লেখা `.gz` file মুছে error আবার throw করি। File যত বড়ই হোক, memory প্রায় স্থির থাকে (`highWaterMark` সাইজের কয়েকটি buffer মাত্র)।
        """,
        ex_en=r"""
            - **Why not `fs.readFile` + `zlib.gzipSync`:** that loads the whole file into memory (and blocks the event loop while compressing). For multi-GB files it simply crashes.
            - **Why not `.pipe()`:** if the write stream fails (disk full), `.pipe()` does not destroy the read stream or surface the error in one place; `pipeline` does.
            - **Counting bytes:** the `Transform` passes chunks through unchanged with `callback(null, chunk)`; counting before gzip gives uncompressed bytes.
            - **Cancellation:** when the signal aborts, `pipeline` rejects with an `AbortError` (`code: 'ABORT_ERR'`) and destroys the streams; our `catch` still deletes the partial file.
            - **Edge cases:** source missing → `ENOENT`; `dest` in a missing directory → `ENOENT` from the write stream; `src === dest` would corrupt data, so validate it in real code. `rm(dest, { force: true })` doesn't throw if the file was never created.
        """,
        ex_bn=r"""
            - **কেন `fs.readFile` + `zlib.gzipSync` নয়:** এতে পুরো file memory-তে আসে (আর compress করার সময় event loop block হয়)। Multi-GB file-এ সরাসরি crash করে।
            - **কেন `.pipe()` নয়:** write stream fail করলে (disk full) `.pipe()` read stream destroy করে না, error-ও এক জায়গায় পাওয়া যায় না; `pipeline` দুটোই করে।
            - **Byte গোনা:** `Transform` `callback(null, chunk)` দিয়ে chunk অপরিবর্তিত রেখে পাঠিয়ে দেয়; gzip-এর আগে গুনলে uncompressed byte পাওয়া যায়।
            - **Cancellation:** signal abort হলে `pipeline` একটি `AbortError` (`code: 'ABORT_ERR'`) দিয়ে reject করে এবং stream-গুলো destroy করে; আমাদের `catch` তখনও অর্ধেক file মুছে দেয়।
            - **Edge case:** source না থাকলে `ENOENT`; `dest`-এর directory না থাকলে write stream থেকে `ENOENT`; `src === dest` হলে data নষ্ট হবে, তাই আসল code-এ এটা validate করো। File তৈরি না হয়ে থাকলেও `rm(dest, { force: true })` throw করে না।
        """,
        tip_en=r"""Say "pipeline, not pipe" early and explain why in one sentence (errors + cleanup). Then mention memory is O(1) regardless of file size — that's the point of the exercise.""",
        tip_bn=r"""শুরুতেই বলো "pipe নয়, pipeline" এবং এক বাক্যে কারণ বলো (error + cleanup)। তারপর উল্লেখ করো file-এর সাইজ যাই হোক memory O(1) — এই exercise-এর মূল কথাই এটা।""",
        mist_en=r"""Accumulating chunks in an array "to count them", forgetting to delete the partial output, or attaching separate `'error'` handlers to each stream and still missing one.""",
        mist_bn=r""""গোনার জন্য" chunk-গুলো array-তে জমানো, অর্ধেক output file মুছতে ভুলে যাওয়া, অথবা প্রতিটি stream-এ আলাদা `'error'` handler লাগিয়েও কোনো একটা বাদ পড়ে যাওয়া।""",
        code=r"""
            import { createReadStream, createWriteStream } from 'node:fs';
            import { rm } from 'node:fs/promises';
            import { Transform } from 'node:stream';
            import { pipeline } from 'node:stream/promises';
            import { createGzip } from 'node:zlib';

            export async function compressFile(src, dest, { signal } = {}) {
              let bytes = 0;
              const counter = new Transform({
                transform(chunk, _encoding, callback) {
                  bytes += chunk.length;
                  callback(null, chunk); // pass through unchanged
                },
              });

              try {
                await pipeline(
                  createReadStream(src),
                  counter,
                  createGzip(),
                  createWriteStream(dest),
                  { signal },
                );
                return bytes;
              } catch (err) {
                await rm(dest, { force: true }); // don't leave a half-written .gz behind
                throw err;
              }
            }

            // Usage with a timeout-based cancellation
            const bytes = await compressFile('app.log', 'app.log.gz', {
              signal: AbortSignal.timeout(60_000),
            });
            console.log(`compressed ${bytes} bytes`);
        """,
        lang="javascript",
        time="O(n) in file size", space="O(1) (bounded by stream buffers)",
        follow=[
            ("How would you compress many files concurrently without overwhelming the disk?", "Disk-এর উপর চাপ না দিয়ে অনেকগুলো file একসাথে কীভাবে compress করবে?"),
            ("How would you stream the gzipped output directly as an HTTP response?", "Gzip করা output সরাসরি HTTP response হিসেবে কীভাবে stream করবে?"),
        ],
        related=["node-005", "node-032"],
        refs=[NODE_STREAM, NODE_ZLIB],
    ),
    # ------------------------------------------------------------------ node-012
    Q(
        id="node-012", sub="Error Handling", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["unhandled-rejection", "promises", "error-handling", "process"],
        ver="Node.js 15+ (current: 24 LTS / 26)", vs=True, status="stable",
        q_en=r"""What happens when this CommonJS script runs on Node.js 24 with default flags?""",
        q_bn=r"""Default flag দিয়ে Node.js 24-এ এই CommonJS script চালালে কী হবে?""",
        code=r"""
            async function loadConfig() {
              throw new Error('config service down');
            }

            loadConfig(); // called without await or .catch()

            setTimeout(() => console.log('still running'), 1000);
        """,
        lang="javascript",
        options=[
            ("A warning is printed and the process keeps running, so `still running` is logged", "একটি warning print হবে এবং process চলতে থাকবে, তাই `still running` log হবে"),
            ("The rejection is silently ignored and `still running` is logged", "Rejection চুপচাপ ignore হবে এবং `still running` log হবে"),
            ("The process crashes with the error and exits with code 1; `still running` is never logged", "Error সহ process crash করবে এবং exit code 1 দিয়ে বন্ধ হবে; `still running` কখনো log হবে না"),
            ("Node retries the rejected promise once, then logs `still running`", "Node rejected promise-টি একবার retry করবে, তারপর `still running` log করবে"),
        ],
        correct=2,
        a_en=r"""
            The process crashes. Since Node.js 15 the default `--unhandled-rejections` mode is `throw`: an unhandled rejection is raised as an uncaught exception, the stack trace is printed and the process exits with code 1 before the timer fires.
        """,
        a_bn=r"""
            Process crash করবে। Node.js 15 থেকে default `--unhandled-rejections` mode হলো `throw`: unhandled rejection-কে uncaught exception হিসেবে raise করা হয়, stack trace print হয় এবং timer fire হওয়ার আগেই process exit code 1 দিয়ে বন্ধ হয়ে যায়।
        """,
        ex_en=r"""
            Option A was the behaviour in Node 14 and earlier (a warning plus a deprecation notice), which is why it's the most tempting wrong answer — many old blog posts still describe it.

            Details worth knowing:
            - If a `process.on('unhandledRejection', ...)` listener exists, the event goes to that listener instead of crashing. Use it for **logging and a controlled shutdown**, not to keep running in an unknown state.
            - The real fix is in the code: `await loadConfig()` inside a `try/catch`, or `loadConfig().catch(handleError)`.
            - Fire-and-forget calls (`sendEmail()` without `await`) are the classic source of these crashes in Express handlers.
            - Modes can be changed with `--unhandled-rejections=strict|warn|none|...`, but changing the default in production usually hides bugs.
        """,
        ex_bn=r"""
            Option A ছিল Node 14 ও তার আগের আচরণ (একটি warning আর deprecation notice) — এজন্যই এটা সবচেয়ে প্রলোভনের ভুল উত্তর, অনেক পুরনো blog post এখনও এটাই বলে।

            যা জানা দরকার:
            - `process.on('unhandledRejection', ...)` listener থাকলে event crash না করে সেই listener-এ যায়। এটা **logging আর নিয়ন্ত্রিত shutdown**-এর জন্য ব্যবহার করো, অজানা অবস্থায় চালিয়ে যাওয়ার জন্য নয়।
            - আসল fix code-এ: `try/catch`-এর ভেতরে `await loadConfig()`, অথবা `loadConfig().catch(handleError)`।
            - Fire-and-forget call (`await` ছাড়া `sendEmail()`) Express handler-এ এই ধরনের crash-এর classic উৎস।
            - `--unhandled-rejections=strict|warn|none|...` দিয়ে mode বদলানো যায়, কিন্তু production-এ default বদলালে সাধারণত bug লুকিয়ে যায়।
        """,
        tip_en=r"""Mention the version boundary ("since Node 15, default mode is throw") — it shows you know why older answers say "just a warning".""",
        tip_bn=r"""Version-এর সীমারেখা উল্লেখ করো ("Node 15 থেকে default mode throw") — এতে বোঝা যায় পুরনো উত্তরে কেন "শুধু warning" লেখা থাকে সেটা তুমি জানো।""",
        refs=[NODE_PROCESS, NODE_CLI],
    ),
    # ------------------------------------------------------------------ node-013
    Q(
        id="node-013", sub="Event Loop", diff="hard", type="output",
        prio="medium", market="both", mins=6,
        tags=["event-loop", "microtasks", "nexttick", "setimmediate", "output"],
        ver="Node.js 11+ semantics (current: 24 LTS / 26)", vs=False, status="stable",
        q_en=r"""Predict the exact output of this CommonJS script and explain each step.""",
        q_bn=r"""এই CommonJS script-এর exact output কী হবে বলো এবং প্রতিটি ধাপ ব্যাখ্যা করো।""",
        a_en=r"""
            Output: `sync`, `n1`, `p1`, `p2`, `n2`, `i1`, `n3`, `p3`, `i2`, `t1`.

            Three rules produce it: (1) after the main script — and after every individual callback — Node drains the whole nextTick queue, then the whole promise microtask queue, and repeats until both are empty; (2) since Node 11, that draining also happens between individual `setImmediate`/timer callbacks; (3) inside an I/O callback, the check phase (`setImmediate`) comes before the next timers phase.
        """,
        a_bn=r"""
            Output: `sync`, `n1`, `p1`, `p2`, `n2`, `i1`, `n3`, `p3`, `i2`, `t1`।

            তিনটি নিয়মে এটা হয়: (1) main script-এর পরে — এবং প্রতিটি আলাদা callback-এর পরে — Node পুরো nextTick queue, তারপর পুরো promise microtask queue খালি করে, এবং দুটোই খালি না হওয়া পর্যন্ত এটা চলতে থাকে; (2) Node 11 থেকে এই draining আলাদা আলাদা `setImmediate`/timer callback-এর মাঝেও হয়; (3) I/O callback-এর ভেতর থেকে check phase (`setImmediate`) পরের timers phase-এর আগে আসে।
        """,
        ex_en=r"""
            Step by step:

            1. Main script: queues microtask `p1`, nextTick `n1`, starts `readFile`, logs `sync`.
            2. Script ends → nextTick queue: `n1` runs and queues microtask `p2`.
            3. nextTick queue empty → microtasks: `p1` (queues nextTick `n2`), then `p2`.
            4. Microtasks empty → Node checks the nextTick queue again: `n2`.
            5. The read finishes; in the poll phase the `readFile` callback schedules timer `t1` and immediates `i1`, `i2`.
            6. Check phase: `i1` runs and queues `n3` and `p3`. Before `i2`, Node drains nextTick then microtasks: `n3`, `p3`. Then `i2`.
            7. Next loop iteration, timers phase: `t1`.

            Before Node 11, all queued immediates ran back-to-back, so you would have seen `i1 i2 n3 p3`. Modern Node matches browser semantics.
        """,
        ex_bn=r"""
            ধাপে ধাপে:

            1. Main script: microtask `p1`, nextTick `n1` queue করে, `readFile` শুরু করে, `sync` log করে।
            2. Script শেষ → nextTick queue: `n1` চলে এবং microtask `p2` queue করে।
            3. nextTick queue খালি → microtask: `p1` (nextTick `n2` queue করে), তারপর `p2`।
            4. Microtask খালি → Node আবার nextTick queue দেখে: `n2`।
            5. Read শেষ হলে poll phase-এ `readFile` callback timer `t1` আর immediate `i1`, `i2` schedule করে।
            6. Check phase: `i1` চলে এবং `n3` ও `p3` queue করে। `i2`-এর আগে Node nextTick, তারপর microtask খালি করে: `n3`, `p3`। এরপর `i2`।
            7. পরের loop iteration-এ timers phase: `t1`।

            Node 11-এর আগে queue-তে থাকা সব immediate একটানা চলত, তখন দেখা যেত `i1 i2 n3 p3`। আধুনিক Node browser-এর semantics মেনে চলে।
        """,
        tip_en=r"""Don't rush to the answer — narrate the queues as a small table (nextTick queue / microtasks / phase). Even if you slip on one line, a clear model earns most of the credit.""",
        tip_bn=r"""তাড়াহুড়ো করে উত্তর বলো না — queue-গুলোকে ছোট একটি table-এর মতো করে বর্ণনা করো (nextTick queue / microtask / phase)। একটা লাইনে ভুল হলেও পরিষ্কার model দেখালে বেশিরভাগ নম্বর পাবে।""",
        mist_en=r"""Assuming a nextTick scheduled from inside a promise callback runs before the remaining promise callbacks, or running both immediates before their microtasks (pre-Node 11 behaviour).""",
        mist_bn=r"""Promise callback-এর ভেতর থেকে schedule করা nextTick বাকি promise callback-গুলোর আগে চলবে ধরে নেওয়া, অথবা microtask-এর আগে দুটো immediate-ই চালিয়ে দেওয়া (Node 11-এর আগের আচরণ)।""",
        code=r"""
            const { readFile } = require('node:fs');

            Promise.resolve().then(() => {
              console.log('p1');
              process.nextTick(() => console.log('n2'));
            });

            process.nextTick(() => {
              console.log('n1');
              Promise.resolve().then(() => console.log('p2'));
            });

            readFile(__filename, () => {
              setTimeout(() => console.log('t1'), 0);
              setImmediate(() => {
                console.log('i1');
                process.nextTick(() => console.log('n3'));
                Promise.resolve().then(() => console.log('p3'));
              });
              setImmediate(() => console.log('i2'));
            });

            console.log('sync');
        """,
        lang="javascript",
        output=r"""
            sync
            n1
            p1
            p2
            n2
            i1
            n3
            p3
            i2
            t1
        """,
        follow=[
            ("How would the first lines change if this file were an ES module?", "এই file যদি ES module হতো, তাহলে প্রথম দিকের লাইনগুলো কীভাবে বদলাত?"),
            ("Why is `process.nextTick` considered dangerous in recursive code?", "Recursive code-এ `process.nextTick` কেন বিপজ্জনক ধরা হয়?"),
        ],
        related=["node-002", "node-004"],
        refs=[NODE_EVENT_LOOP, NODE_PROCESS],
    ),
    # ------------------------------------------------------------------ node-014
    Q(
        id="node-014", sub="Memory Management", diff="hard", type="debugging",
        prio="high", market="both", mins=10,
        tags=["memory-leak", "heap-snapshot", "cache", "gc", "production-debugging"],
        ver="Node.js 24 LTS / 26; Express 5.x", vs=False, status="stable",
        q_en=r"""This Express service's memory grows steadily for days until the process crashes with "JavaScript heap out of memory", then it restarts and the cycle repeats. Latency also creeps up before each crash. Find the leak, explain how you would prove it with tools, and fix it.""",
        q_bn=r"""এই Express service-এর memory কয়েকদিন ধরে ধীরে ধীরে বাড়তে থাকে, শেষে "JavaScript heap out of memory" দিয়ে process crash করে, তারপর restart হয়ে আবার একই চক্র চলে। প্রতিটি crash-এর আগে latency-ও বাড়তে থাকে। Leak-টা খুঁজে বের করো, tool দিয়ে কীভাবে প্রমাণ করবে ব্যাখ্যা করো, এবং ঠিক করো।""",
        a_en=r"""
            The leak is the module-level `cache` Map. It is keyed by `req.originalUrl`, which includes the full query string, and entries are never evicted. Every unique URL — `?page=1…∞`, search terms, tracking parameters, bots adding random query strings — adds an entry that stays reachable forever, so the garbage collector can't free it. As the heap grows, GC runs longer and more often (latency creeps up) until V8 hits the heap limit.

            To prove it: watch `heapUsed` over time, then take two or three **heap snapshots** a few minutes apart under traffic and open them in Chrome DevTools' Memory tab using the **Comparison** view. The growing objects (arrays of products) will show `cache` (a `Map`) in their retainer chain.

            Fix: bound the cache — a max size with LRU eviction plus a TTL — and build the key from **whitelisted, normalised** parameters instead of the raw URL. For multiple instances, a shared Redis cache with TTLs is usually better anyway.
        """,
        a_bn=r"""
            Leak হলো module-level `cache` Map। এর key হলো `req.originalUrl`, যাতে পুরো query string থাকে, আর কোনো entry কখনো evict হয় না। প্রতিটি নতুন URL — `?page=1…∞`, search term, tracking parameter, random query string যোগ করা bot — একটি entry যোগ করে যা চিরকাল reachable থাকে, তাই garbage collector সেটা free করতে পারে না। Heap বাড়ার সাথে GC আরও লম্বা ও ঘন ঘন চলে (latency বাড়ে), শেষে V8 heap limit-এ পৌঁছে যায়।

            প্রমাণ করতে: সময়ের সাথে `heapUsed` দেখি, তারপর traffic চলাকালীন কয়েক মিনিট পরপর দুই-তিনটি **heap snapshot** নিই এবং Chrome DevTools-এর Memory tab-এ **Comparison** view-তে খুলি। বাড়তে থাকা object-গুলোর (product-এর array) retainer chain-এ `cache` (একটি `Map`) দেখা যাবে।

            Fix: cache-কে সীমিত করা — LRU eviction সহ max size আর একটি TTL — এবং raw URL-এর বদলে **whitelist করা, normalise করা** parameter দিয়ে key বানানো। একাধিক instance থাকলে TTL সহ shared Redis cache সাধারণত এমনিতেই ভালো।
        """,
        ex_en=r"""
            - **A leak in a GC language means "unintentionally reachable".** Common Node sources: unbounded caches/Maps, arrays used as in-memory logs or metrics, event listeners added per request and never removed, `setInterval`s that are never cleared, and closures that capture large objects.
            - **Getting snapshots in production:** `node --heapsnapshot-signal=SIGUSR2 server.js` then `kill -USR2 <pid>`; or `v8.writeHeapSnapshot()` from an admin-only endpoint; or `--heapsnapshot-near-heap-limit=2` to capture automatically just before an OOM. Snapshots pause the process and can be as large as the heap — take them on one instance, out of rotation if possible.
            - **`--max-old-space-size` is not a fix.** A bigger heap only delays the crash (and in containers, setting it above the memory limit gets the process OOM-killed by the kernel instead).
            - **`WeakMap`** helps when the key is an object whose lifetime you don't control; it doesn't help with string keys like URLs.
            - In production I'd use a maintained LRU library (e.g. `lru-cache`) instead of hand-rolling one; the fixed version shows the idea.
        """,
        ex_bn=r"""
            - **GC-ভিত্তিক language-এ leak মানে "অনিচ্ছাকৃতভাবে reachable"।** Node-এ সাধারণ উৎস: unbounded cache/Map, in-memory log বা metric হিসেবে ব্যবহার করা array, প্রতি request-এ যোগ করা কিন্তু কখনো remove না করা event listener, clear না করা `setInterval`, আর বড় object ধরে রাখা closure।
            - **Production-এ snapshot নেওয়া:** `node --heapsnapshot-signal=SIGUSR2 server.js` দিয়ে চালিয়ে `kill -USR2 <pid>`; অথবা admin-only endpoint থেকে `v8.writeHeapSnapshot()`; অথবা `--heapsnapshot-near-heap-limit=2` দিয়ে OOM-এর ঠিক আগে নিজে থেকেই snapshot নেওয়া। Snapshot নেওয়ার সময় process থেমে যায় এবং file heap-এর সমান বড় হতে পারে — একটি instance-এ নাও, সম্ভব হলে traffic rotation-এর বাইরে রেখে।
            - **`--max-old-space-size` কোনো fix নয়।** বড় heap শুধু crash পিছিয়ে দেয় (আর container-এ memory limit-এর চেয়ে বেশি দিলে kernel process-কে OOM-kill করে দেয়)।
            - **`WeakMap`** কাজে লাগে যখন key এমন object যার lifetime তুমি নিয়ন্ত্রণ করো না; URL-এর মতো string key-তে এটা কাজ করে না।
            - Production-এ আমি নিজে না লিখে maintained LRU library (যেমন `lru-cache`) ব্যবহার করব; fixed version-টা শুধু ধারণাটা দেখায়।
        """,
        tip_en=r"""Use the words "retainer chain" and "comparison view" — it shows you've actually hunted a leak. Then explain why raising the heap limit is not a fix.""",
        tip_bn=r""""Retainer chain" আর "comparison view" শব্দগুলো ব্যবহার করো — এতে বোঝা যায় তুমি সত্যিই leak খুঁজেছ। তারপর ব্যাখ্যা করো কেন heap limit বাড়ানো কোনো fix নয়।""",
        mist_en=r"""Calling `global.gc()` in a loop, restarting the process on a cron as the "solution", or assuming Node has no leaks because it has a garbage collector.""",
        mist_bn=r"""Loop-এ `global.gc()` call করা, cron দিয়ে process restart করাকেই "সমাধান" ধরা, অথবা garbage collector আছে বলে Node-এ leak হয় না ধরে নেওয়া।""",
        code=r"""
            import express from 'express';
            import { db } from './db.js';

            const app = express();
            const cache = new Map();

            app.get('/api/products', async (req, res) => {
              const key = req.originalUrl;
              if (cache.has(key)) return res.json(cache.get(key));

              const products = await db.findProducts(req.query);
              cache.set(key, products);
              res.json(products);
            });

            app.listen(3000);
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", src=r"""
                const MAX_ENTRIES = 500;
                const TTL_MS = 60_000;
                const cache = new Map(); // key -> { value, expires }; Map keeps insertion order

                function getCached(key) {
                  const hit = cache.get(key);
                  if (!hit) return undefined;
                  if (hit.expires < Date.now()) {
                    cache.delete(key);
                    return undefined;
                  }
                  cache.delete(key); // move to the "most recently used" end
                  cache.set(key, hit);
                  return hit.value;
                }

                function setCached(key, value) {
                  cache.set(key, { value, expires: Date.now() + TTL_MS });
                  if (cache.size > MAX_ENTRIES) {
                    cache.delete(cache.keys().next().value); // evict least recently used
                  }
                }

                app.get('/api/products', async (req, res) => {
                  // Whitelisted, normalised key -> bounded key space
                  const page = Math.max(1, Number.parseInt(req.query.page ?? '1', 10) || 1);
                  const category = typeof req.query.category === 'string' ? req.query.category : 'all';
                  const key = `products:${category}:${page}`;

                  const cached = getCached(key);
                  if (cached) return res.json(cached);

                  const products = await db.findProducts({ category, page });
                  setCached(key, products);
                  res.json(products);
                });
            """, label_en="Fixed version (bounded LRU + TTL, normalised key)", label_bn="সংশোধিত version (সীমিত LRU + TTL, normalise করা key)"),
            dict(lang="bash", src=r"""
                # Take heap snapshots on demand (writes Heap.*.heapsnapshot to the cwd)
                node --heapsnapshot-signal=SIGUSR2 server.js
                kill -USR2 <pid>    # take one now, another after 10 minutes of traffic

                # Or capture automatically right before an out-of-memory crash
                node --heapsnapshot-near-heap-limit=2 server.js
            """, label_en="Capturing heap snapshots", label_bn="Heap snapshot নেওয়া"),
        ],
        follow=[
            ("What's the difference between `heapUsed`, `heapTotal` and `rss` in `process.memoryUsage()`?", "`process.memoryUsage()`-এ `heapUsed`, `heapTotal` আর `rss`-এর পার্থক্য কী?"),
            ("How can Buffers make RSS grow while the JS heap looks stable?", "JS heap স্থির দেখালেও Buffer কীভাবে RSS বাড়িয়ে দিতে পারে?"),
        ],
        related=["node-023", "node-006"],
        refs=[NODE_HEAP_SNAPSHOT, NODE_V8, NODE_CLI],
    ),
]

if __name__ == "__main__":
    save("nodejs", "b2", QUESTIONS)
