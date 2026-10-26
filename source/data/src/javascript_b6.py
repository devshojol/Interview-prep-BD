import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
API = "https://developer.mozilla.org/en-US/docs/Web/API"
R_GETORINSERT = ("MDN — Map.prototype.getOrInsert()", f"{MDN}/Reference/Global_Objects/Map/getOrInsert")
R_GETORINSERT_C = ("MDN — Map.prototype.getOrInsertComputed()", f"{MDN}/Reference/Global_Objects/Map/getOrInsertComputed")
R_SUMPRECISE = ("MDN — Math.sumPrecise()", f"{MDN}/Reference/Global_Objects/Math/sumPrecise")
R_STRUCTURED = ("MDN — structuredClone()", f"{API}/Window/structuredClone")
R_WEAKMAP = ("MDN — WeakMap", f"{MDN}/Reference/Global_Objects/WeakMap")
R_REFLECT_OWNKEYS = ("MDN — Reflect.ownKeys()", f"{MDN}/Reference/Global_Objects/Reflect/ownKeys")
R_PALL = ("MDN — Promise.all()", f"{MDN}/Reference/Global_Objects/Promise/all")
R_ABORT_THROW = ("MDN — AbortSignal.throwIfAborted()", f"{API}/AbortSignal/throwIfAborted")
R_ASYNC_FN = ("MDN — async function", f"{MDN}/Reference/Statements/async_function")
R_QMT = ("MDN — queueMicrotask()", f"{API}/Window/queueMicrotask")
R_SET = ("MDN — Set", f"{MDN}/Reference/Global_Objects/Set")
R_USESES = ("React — useSyncExternalStore", "https://react.dev/reference/react/useSyncExternalStore")
R_RAF = ("MDN — Window.requestAnimationFrame()", f"{API}/Window/requestAnimationFrame")
R_LAYOUT = ("web.dev — Avoid large, complex layouts and layout thrashing", "https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing")
R_LONG_TASKS = ("web.dev — Optimize long tasks", "https://web.dev/articles/optimize-long-tasks")
R_V8_MAPS = ("V8 — Maps (Hidden Classes) in V8", "https://v8.dev/docs/hidden-classes")
R_V8_PROPS = ("V8 blog — Fast properties in V8", "https://v8.dev/blog/fast-properties")
R_V8_ELEMENTS = ("V8 blog — Elements kinds in V8", "https://v8.dev/blog/elements-kinds")

QUESTIONS = [
    # ------------------------------------------------------------------ js-035
    Q(
        id="js-035", sub="Modern JavaScript (ES2025/ES2026)", diff="hard", type="mcq",
        prio="medium", market="both", mins=4,
        tags=["es2026", "map-upsert", "getorinsert", "modern-javascript", "baseline"],
        ver="ECMAScript 2026 (Map upsert: Baseline newly available since 2026-02; Node.js 26, not Node.js 24)", vs=True, status="stable",
        q_en=r"""This snippet uses the ES2026 `Map` "upsert" methods. What does it log?""",
        q_bn=r"""এই snippet ES2026-এর `Map` "upsert" method ব্যবহার করছে। এটা কী log করবে?""",
        code=r"""
            const visits = new Map();
            for (const page of ['home', 'cart', 'home', 'home']) {
              visits.set(page, visits.getOrInsert(page, 0) + 1);
            }

            let factoryCalls = 0;
            const byInitial = new Map();
            for (const name of ['rina', 'sakib', 'rafi']) {
              byInitial
                .getOrInsertComputed(name[0], () => {
                  factoryCalls++;
                  return [];
                })
                .push(name);
            }

            console.log(visits.get('home'), factoryCalls, byInitial.get('r').length);
        """,
        lang="javascript",
        output=r"""3 2 2""",
        options=[
            ("`3 2 2`", "`3 2 2`"),
            ("`1 3 2`", "`1 3 2`"),
            ("`3 3 2`", "`3 3 2`"),
            ("`3 2 1`", "`3 2 1`"),
        ],
        correct=0,
        a_en=r"""
            `3 2 2`.

            - `getOrInsert(key, defaultValue)` returns the **existing** value if the key is present; otherwise it inserts `defaultValue` and returns it. So the counter works like `(map.get(k) ?? 0) + 1`, and `'home'` reaches `3`.
            - `getOrInsertComputed(key, callback)` is the **lazy** version: the callback runs only when the key is missing, receives the key, and its result is inserted. Keys `'r'` and `'s'` are new → 2 factory calls; `'rafi'` reuses the existing `'r'` array → it holds `['rina', 'rafi']`.
        """,
        a_bn=r"""
            `3 2 2`।

            - `getOrInsert(key, defaultValue)` key থাকলে **আগের** value return করে; না থাকলে `defaultValue` insert করে সেটা return করে। তাই counter-টা `(map.get(k) ?? 0) + 1`-এর মতো কাজ করে, আর `'home'` পৌঁছায় `3`-এ।
            - `getOrInsertComputed(key, callback)` হলো **lazy** version: key না থাকলেই কেবল callback চলে, key-টা argument হিসেবে পায়, আর তার result insert হয়। `'r'` আর `'s'` নতুন key → ২ বার factory call; `'rafi'` আগের `'r'` array-টাই ব্যবহার করে → তাতে থাকে `['rina', 'rafi']`।
        """,
        quick_en=r"""`3 2 2`. `getOrInsert` returns the existing value or inserts the default, so `'home'` counts up to `3`; `getOrInsertComputed` runs its callback only for missing keys (`'r'` and `'s'`, so 2 calls), and `'rafi'` reuses the `'r'` array, which ends up with 2 names.""",
        quick_bn=r"""`3 2 2`। `getOrInsert` key থাকলে পুরনো value দেয়, না থাকলে default insert করে, তাই `'home'` গুনে `3` হয়; `getOrInsertComputed` callback চালায় শুধু key না থাকলে (`'r'` আর `'s'`, তাই 2 বার), আর `'rafi'` আগের `'r'` array-ই ব্যবহার করে, যেখানে শেষে 2টা নাম থাকে।""",
        ex_en=r"""
            - **Option B** assumes `getOrInsert` always returns the default (so `home` stays at 1) and that the factory runs every time.
            - **Option C** treats `getOrInsertComputed` like `getOrInsert(key, factory())`, where the argument is evaluated eagerly on every call. Avoiding that wasted work is exactly why the computed variant exists.
            - **Option D** assumes the existing array is replaced.

            Support: Map/WeakMap upsert is ES2026 and Baseline newly available since February 2026 (Chrome 145, Firefox 144, Safari 26.2). It's in Node.js 26 but **not** Node.js 24 — polyfill (core-js) or fall back to `has`/`get`/`set` there.

            Other ES2026 additions worth knowing, with status:
            - `Math.sumPrecise([0.1, 0.2, 0.3])` → `0.6` (exact sum, rounded once), while `0.1 + 0.2 + 0.3` → `0.6000000000000001`. Baseline since April 2026; not yet in Node.js 26.
            - `Uint8Array.fromBase64()`, `.toBase64()`, `.toHex()`, `fromHex()` — Baseline since September 2025, Node.js 26.
            - `Iterator.concat()` (Baseline 2026-03), `Array.fromAsync()` (widely available), `JSON.rawJSON` / source text access.
            - `Error.isError()` — standard, but **not Baseline** (Safari's implementation is still partial).
            - Still **not** Baseline: Temporal and `using` declarations — label them experimental if you mention them.
        """,
        ex_bn=r"""
            - **Option B** ধরে নেয় `getOrInsert` সবসময় default return করে (ফলে `home` 1-এই থাকে) আর factory প্রতিবার চলে।
            - **Option C** `getOrInsertComputed`-কে `getOrInsert(key, factory())`-এর মতো ভাবে, যেখানে argument প্রতিটি call-এ আগেভাগে evaluate হয়। এই অপচয় এড়ানোর জন্যই computed version-টা আছে।
            - **Option D** ধরে নেয় আগের array replace হয়ে যায়।

            Support: Map/WeakMap upsert ES2026-এর অংশ এবং February 2026 থেকে Baseline newly available (Chrome 145, Firefox 144, Safari 26.2)। Node.js 26-এ আছে, কিন্তু Node.js 24-এ **নেই** — সেখানে polyfill (core-js) বা `has`/`get`/`set` fallback ব্যবহার করো।

            ES2026-এর আরও কিছু সংযোজন, অবস্থা সহ:
            - `Math.sumPrecise([0.1, 0.2, 0.3])` → `0.6` (নিখুঁত যোগফল, একবারই round হয়), যেখানে `0.1 + 0.2 + 0.3` → `0.6000000000000001`। April 2026 থেকে Baseline; Node.js 26-এ এখনো নেই।
            - `Uint8Array.fromBase64()`, `.toBase64()`, `.toHex()`, `fromHex()` — September 2025 থেকে Baseline, Node.js 26-এ আছে।
            - `Iterator.concat()` (Baseline 2026-03), `Array.fromAsync()` (widely available), `JSON.rawJSON` / source text access।
            - `Error.isError()` — standard, কিন্তু **Baseline নয়** (Safari-র implementation এখনো আংশিক)।
            - এখনো Baseline **নয়**: Temporal আর `using` declaration — উল্লেখ করলে experimental হিসেবে চিহ্নিত করো।
        """,
        tip_en=r"""Explain the eager-vs-lazy difference between the two methods, then immediately give the support status (Baseline 2026, Node 26 yes, Node 24 no). Knowing *where* a new feature runs is what makes the answer production-grade.""",
        tip_bn=r"""দুটো method-এর eager বনাম lazy পার্থক্য ব্যাখ্যা করো, তারপর সাথে সাথে support status বলো (Baseline 2026, Node 26-এ আছে, Node 24-এ নেই)। নতুন feature *কোথায়* চলে সেটা জানাই উত্তরকে production-grade বানায়।""",
        follow=[
            ("How would you write the same grouping code for Node.js 24?", "Node.js 24-এর জন্য একই grouping code কীভাবে লিখবে?"),
        ],
        related=["js-027", "js-022", "js-012"],
        refs=[R_GETORINSERT, R_GETORINSERT_C, R_SUMPRECISE],
    ),
    # ------------------------------------------------------------------ js-036
    Q(
        id="js-036", sub="Shallow vs Deep Copy", diff="hard", type="coding",
        prio="high", market="both", mins=12,
        tags=["deep-clone", "structuredclone", "circular-references", "weakmap", "recursion"],
        ver="Manual version: ES2015+; `structuredClone` Baseline widely available (Node.js 17+)", vs=True, status="stable",
        q_en=r"""
            Implement `deepClone(value)` that copies nested objects and arrays and also handles:

            - `Date`, `RegExp`, `Map` and `Set`;
            - symbol-keyed properties;
            - class instances (keep their prototype);
            - **circular references** (`obj.self = obj` must not overflow the stack).

            Then explain when you would simply use `structuredClone` or `JSON.parse(JSON.stringify(x))` instead, and what each approach loses.
        """,
        q_bn=r"""
            `deepClone(value)` implement করো, যেটা nested object আর array copy করবে এবং এগুলোও handle করবে:

            - `Date`, `RegExp`, `Map` আর `Set`;
            - symbol-key-ওয়ালা property;
            - class instance (তাদের prototype ঠিক রেখে);
            - **circular reference** (`obj.self = obj` হলে stack overflow হওয়া চলবে না)।

            এরপর ব্যাখ্যা করো কখন সরাসরি `structuredClone` বা `JSON.parse(JSON.stringify(x))` ব্যবহার করবে, আর প্রতিটি পদ্ধতিতে কী হারায়।
        """,
        a_en=r"""
            I recurse with a `WeakMap` called `seen` that maps each original object to its copy:

            1. Primitives (and functions) are returned as-is.
            2. If the object was already cloned, return the existing copy — this handles cycles **and** keeps shared references shared.
            3. Special-case `Date`, `RegExp`, `Map` and `Set`. For `Map`/`Set`, register the empty copy in `seen` **before** filling it, so entries pointing back to the container resolve correctly.
            4. For arrays and plain/class objects, create the shell (`new Array(length)` or `Object.create(Object.getPrototypeOf(value))`), register it, then copy every own enumerable key from `Reflect.ownKeys` (strings and symbols). I use `Object.defineProperty` so a key named `"__proto__"` becomes a normal own property instead of triggering the prototype setter.

            It's O(n) time and space in the number of reachable values.

            In practice, I reach for **`structuredClone`** first: it's built in (Baseline widely available, Node 17+), handles cycles, `Date`, `RegExp`, `Map`, `Set`, typed arrays and more. I write a custom clone only when I need things it doesn't do: keeping class prototypes, symbol keys, or sharing functions.
        """,
        a_bn=r"""
            আমি `seen` নামের একটা `WeakMap` নিয়ে recursion করি, যেটা প্রতিটি original object-কে তার copy-র সাথে map করে:

            1. Primitive (আর function) যেমন আছে তেমনই return করি।
            2. Object আগেই clone হয়ে থাকলে আগের copy-টাই return করি — এতে cycle handle হয় **এবং** shared reference shared-ই থাকে।
            3. `Date`, `RegExp`, `Map` আর `Set` আলাদাভাবে handle করি। `Map`/`Set`-এর ক্ষেত্রে খালি copy-টা ভরার **আগেই** `seen`-এ register করি, যাতে container-কে ফিরে point করা entry ঠিকভাবে resolve হয়।
            4. Array আর plain/class object-এর জন্য খোলসটা তৈরি করি (`new Array(length)` বা `Object.create(Object.getPrototypeOf(value))`), register করি, তারপর `Reflect.ownKeys` থেকে প্রতিটি নিজস্ব enumerable key (string আর symbol) copy করি। `Object.defineProperty` ব্যবহার করি, যাতে `"__proto__"` নামের key prototype setter trigger না করে সাধারণ নিজস্ব property হয়।

            Reachable value-র সংখ্যার হিসাবে time আর space O(n)।

            বাস্তবে আমি প্রথমে **`structuredClone`** ব্যবহার করি: এটা built-in (Baseline widely available, Node 17+), cycle, `Date`, `RegExp`, `Map`, `Set`, typed array সহ আরও অনেক কিছু handle করে। Custom clone লিখি কেবল তখনই, যখন এমন কিছু দরকার যা এটা করে না: class prototype রাখা, symbol key, বা function share করা।
        """,
        quick_en=r"""Recurse with a `WeakMap` from original to copy, which handles cycles and shared references; special-case `Date`, `RegExp`, `Map` and `Set`, and keep prototypes and symbol keys with `Object.create` and `Reflect.ownKeys`. It's O(n); in practice I use `structuredClone` unless I need those extras.""",
        quick_bn=r"""একটা `WeakMap`-এ original থেকে copy-র map রেখে recursion করি, এতে cycle আর shared reference দুটোই সামলানো যায়; `Date`, `RegExp`, `Map` আর `Set` আলাদাভাবে handle করি, আর `Object.create` ও `Reflect.ownKeys` দিয়ে prototype আর symbol key রেখে দিই। এটা O(n); বাস্তবে এগুলো না লাগলে আমি `structuredClone`-ই ব্যবহার করি।""",
        ex_en=r"""
            What each approach loses:

            - **`JSON.parse(JSON.stringify(x))`:** drops `undefined`, functions and symbols; turns `Date` into a string, `Map`/`Set` into `{}`, `NaN`/`Infinity` into `null`; loses prototypes; throws on cycles and `BigInt`. Fine only for plain JSON-shaped data.
            - **`structuredClone(x)`:** throws `DataCloneError` for functions and DOM nodes; class instances come back as plain objects; symbol-keyed properties, getters/setters (only their current values survive), property descriptors and private `#fields` are not preserved. It also supports a `transfer` option to move `ArrayBuffer`s instead of copying.
            - **My `deepClone`:** keeps prototypes and symbol keys, shares functions by reference, snapshots getter values, and skips non-enumerable properties. It doesn't handle typed arrays, `ArrayBuffer`, `Error` or private fields (no generic code can copy `#private` state).

            Edge cases to mention: very deep structures can overflow the call stack with recursion — an explicit stack/queue makes it iterative. Cloning is also a security boundary: never deep-merge/clone untrusted input with code that assigns `obj[key] = ...` blindly (prototype pollution).
        """,
        ex_bn=r"""
            প্রতিটি পদ্ধতিতে কী হারায়:

            - **`JSON.parse(JSON.stringify(x))`:** `undefined`, function আর symbol বাদ পড়ে; `Date` string হয়ে যায়, `Map`/`Set` হয়ে যায় `{}`, `NaN`/`Infinity` হয়ে যায় `null`; prototype হারায়; cycle আর `BigInt` পেলে throw করে। শুধু সাধারণ JSON-আকৃতির data-র জন্য ঠিক আছে।
            - **`structuredClone(x)`:** function আর DOM node পেলে `DataCloneError` throw করে; class instance plain object হয়ে ফেরে; symbol-key-ওয়ালা property, getter/setter (শুধু তাদের current value থাকে), property descriptor আর private `#field` রক্ষা হয় না। এতে একটা `transfer` option-ও আছে, যা `ArrayBuffer` copy না করে সরিয়ে দেয়।
            - **আমার `deepClone`:** prototype আর symbol key রাখে, function reference দিয়ে share করে, getter-এর value-র snapshot নেয়, আর non-enumerable property বাদ দেয়। এটা typed array, `ArrayBuffer`, `Error` বা private field handle করে না (কোনো generic code-ই `#private` state copy করতে পারে না)।

            যে edge case-গুলো বলা ভালো: খুব গভীর structure-এ recursion call stack overflow করতে পারে — explicit stack/queue দিয়ে iterative করা যায়। Cloning একটা security boundary-ও: অবিশ্বস্ত input-কে এমন code দিয়ে deep-merge/clone কোরো না যেটা অন্ধভাবে `obj[key] = ...` assign করে (prototype pollution)।
        """,
        tip_en=r"""Start by asking which types must be supported — it shows you know there's no universal deep clone. Code the cycle handling early (it's what's being tested), then close with "in production I'd use `structuredClone` unless I need prototypes".""",
        tip_bn=r"""শুরুতেই জিজ্ঞেস করো কোন কোন type support করতে হবে — এতে বোঝা যায় তুমি জানো যে সর্বজনীন deep clone বলে কিছু নেই। Cycle handling আগে লেখো (এটাই মূলত যাচাই হচ্ছে), তারপর শেষ করো "production-এ prototype দরকার না হলে আমি `structuredClone` ব্যবহার করব" দিয়ে।""",
        mist_en=r"""Forgetting cycles (infinite recursion), registering the copy in `seen` *after* recursing into children, using `{}` for class instances (losing methods), or treating `JSON.parse(JSON.stringify())` as a general deep clone.""",
        mist_bn=r"""Cycle ভুলে যাওয়া (অসীম recursion), child-এ recurse করার *পরে* copy-টা `seen`-এ register করা, class instance-এর জন্য `{}` ব্যবহার করা (method হারিয়ে যায়), অথবা `JSON.parse(JSON.stringify())`-কে সাধারণ deep clone ভাবা।""",
        code=r"""
            function deepClone(value, seen = new WeakMap()) {
              if (value === null || typeof value !== 'object') return value; // primitives, functions
              if (seen.has(value)) return seen.get(value); // cycles & shared references

              if (value instanceof Date) return new Date(value.getTime());
              if (value instanceof RegExp) return new RegExp(value.source, value.flags);

              if (value instanceof Map) {
                const copy = new Map();
                seen.set(value, copy);
                for (const [k, v] of value) copy.set(deepClone(k, seen), deepClone(v, seen));
                return copy;
              }

              if (value instanceof Set) {
                const copy = new Set();
                seen.set(value, copy);
                for (const v of value) copy.add(deepClone(v, seen));
                return copy;
              }

              const copy = Array.isArray(value)
                ? new Array(value.length)
                : Object.create(Object.getPrototypeOf(value)); // keep class prototype
              seen.set(value, copy);

              for (const key of Reflect.ownKeys(value)) { // string + symbol keys
                if (!Object.getOwnPropertyDescriptor(value, key).enumerable) continue;
                Object.defineProperty(copy, key, { // avoids the __proto__ setter
                  value: deepClone(value[key], seen),
                  writable: true,
                  enumerable: true,
                  configurable: true,
                });
              }
              return copy;
            }

            class Point {
              constructor(x, y) { this.x = x; this.y = y; }
              norm() { return Math.hypot(this.x, this.y); }
            }

            const original = {
              createdAt: new Date('2026-01-01T00:00:00Z'),
              tags: new Set(['js', 'bd']),
              point: new Point(3, 4),
              [Symbol.for('meta')]: 'kept',
            };
            original.self = original;

            const copy = deepClone(original);
            console.log(copy.self === copy, copy.point.norm(), copy.createdAt !== original.createdAt); // true 5 true
            console.log(structuredClone(original).point instanceof Point); // false — prototype lost
        """,
        lang="javascript",
        time="O(n) — n reachable values", space="O(n)",
        follow=[
            ("How would you make it iterative to avoid stack overflow on very deep data?", "খুব গভীর data-তে stack overflow এড়াতে এটা iterative কীভাবে করবে?"),
            ("Why is `WeakMap` used for `seen` instead of `Map`?", "`seen`-এর জন্য `Map`-এর বদলে `WeakMap` কেন?"),
        ],
        related=["js-009", "js-030", "js-014"],
        refs=[R_STRUCTURED, R_WEAKMAP, R_REFLECT_OWNKEYS],
    ),
    # ------------------------------------------------------------------ js-037
    Q(
        id="js-037", sub="Concurrency & Async Patterns", diff="extreme", type="coding",
        prio="high", market="both", mins=18,
        tags=["concurrency", "promise-pool", "rate-limiting", "abortcontroller", "async-patterns"],
        ver="ES2017+ async/await; `AbortSignal.throwIfAborted` Baseline widely available; Node.js 24/26", vs=False, status="stable",
        q_en=r"""
            You must call an API for 10,000 items, but the server allows at most 5 concurrent requests. Implement `promisePool(tasks, limit, { signal })` where `tasks` is an array of **functions** that return promises.

            Requirements:
            - never more than `limit` tasks in flight;
            - results in **input order**;
            - fail fast: after the first failure, start no new tasks and reject with that error;
            - cancellation via an `AbortSignal`.

            Discuss the design choices and how this differs from processing in batches of 5.
        """,
        q_bn=r"""
            তোমাকে ১০,০০০ item-এর জন্য একটা API call করতে হবে, কিন্তু server একসাথে সর্বোচ্চ ৫টা concurrent request নিতে পারে। `promisePool(tasks, limit, { signal })` implement করো, যেখানে `tasks` হলো promise return করা **function**-এর array।

            Requirement:
            - কখনো `limit`-এর বেশি task একসাথে চলবে না;
            - result আসবে **input-এর ক্রমে**;
            - fail fast: প্রথম failure-এর পর নতুন কোনো task শুরু হবে না, আর সেই error দিয়ে reject করবে;
            - একটা `AbortSignal` দিয়ে cancellation।

            Design-এর সিদ্ধান্তগুলো আলোচনা করো, আর ৫টা করে batch-এ process করার সাথে এর পার্থক্য কী সেটা বলো।
        """,
        a_en=r"""
            (Advanced.) I use the **worker-pool** pattern: start `min(limit, tasks.length)` async workers that all pull from a shared index.

            - Each worker loops: check the abort signal, take `nextIndex++`, `await tasks[index]()`, store the result at `results[index]`. Taking the index is race-free because JavaScript runs one piece of code at a time on a thread — there's no interleaving between reading and incrementing.
            - `Promise.all(workers)` resolves when every worker has run out of work, and returns the ordered `results`.
            - **Fail fast:** a worker that catches an error sets a shared `failed` flag and rethrows. The other workers check the flag before taking new work, and `Promise.all` rejects with the first error. Tasks already in flight can't be force-stopped; they receive the `signal` so they can abort themselves.
            - **Cancellation:** `signal.throwIfAborted()` before each new task.

            Why `tasks` must be functions: a promise starts running the moment it's created. If the caller passed 10,000 promises, all 10,000 requests would already be in flight and no pool could limit them.

            **Vs batches of 5** (`Promise.all` on chunks): each batch waits for its slowest request, so slots sit idle (head-of-line blocking). The pool refills a slot the moment any task finishes, keeping exactly `limit` requests busy — usually much faster overall.
        """,
        a_bn=r"""
            (Advanced বিষয়।) আমি **worker-pool** pattern ব্যবহার করি: `min(limit, tasks.length)`-টা async worker শুরু করি, যারা সবাই একটা shared index থেকে কাজ টেনে নেয়।

            - প্রতিটি worker loop করে: abort signal check করে, `nextIndex++` নেয়, `await tasks[index]()` করে, result রাখে `results[index]`-এ। Index নেওয়াটা race-free, কারণ JavaScript একটা thread-এ একবারে একটাই code চালায় — পড়া আর বাড়ানোর মাঝখানে অন্য কিছু ঢুকতে পারে না।
            - সব worker-এর কাজ ফুরালে `Promise.all(workers)` resolve হয়, আর ক্রমানুসারে সাজানো `results` return করে।
            - **Fail fast:** কোনো worker error ধরলে একটা shared `failed` flag সেট করে আবার throw করে। বাকি worker-রা নতুন কাজ নেওয়ার আগে flag check করে, আর `Promise.all` প্রথম error দিয়ে reject করে। ইতিমধ্যে চলমান task জোর করে থামানো যায় না; তারা `signal` পায়, যাতে নিজেরাই abort করতে পারে।
            - **Cancellation:** প্রতিটি নতুন task-এর আগে `signal.throwIfAborted()`।

            `tasks` কেন function হতে হবে: promise তৈরি হওয়ার মুহূর্তেই চলতে শুরু করে। Caller যদি ১০,০০০টা promise পাঠাত, তাহলে ১০,০০০টা request ইতিমধ্যেই চলত, আর কোনো pool সেগুলো সীমিত করতে পারত না।

            **৫টা করে batch-এর সাথে পার্থক্য** (chunk-এ `Promise.all`): প্রতিটি batch তার সবচেয়ে ধীর request-এর জন্য অপেক্ষা করে, ফলে slot খালি পড়ে থাকে (head-of-line blocking)। Pool যেকোনো task শেষ হওয়ার সাথে সাথে slot ভরে ফেলে, ঠিক `limit`-সংখ্যক request সবসময় ব্যস্ত রাখে — সাধারণত মোট সময় অনেক কম লাগে।
        """,
        quick_en=r"""Use a worker pool: start `min(limit, tasks.length)` async workers that pull from a shared `nextIndex`, store each result at its index, and stop taking work after a failure or abort. Unlike batches of 5, a slot refills as soon as any task finishes; tasks are functions so they don't start early.""",
        quick_bn=r"""Worker pool ব্যবহার করি: `min(limit, tasks.length)`টা async worker চালাই, যারা একটা shared `nextIndex` থেকে কাজ নেয়, result রাখে নিজের index-এ, আর failure বা abort হলে নতুন কাজ নেয় না। ৫টার batch-এর মতো নয়, এখানে কোনো task শেষ হলেই slot আবার ভরে যায়; আর task-গুলো function বলে আগেভাগে শুরু হয়ে যায় না।""",
        ex_en=r"""
            Design variations an interviewer may push on:

            - **Settle-all mode:** instead of fail-fast, store `{ status, value | reason }` per item (like `allSettled`) and keep going — better for bulk jobs where you report failures at the end.
            - **Retries per task:** wrap each task with the retry-with-backoff helper; count retries against a global budget so an outage doesn't multiply load.
            - **Lazy input / backpressure:** accept an iterable or async iterable instead of an array, so you don't materialise 10,000 functions (or millions of rows) up front. Workers pull the next item only when they're free.
            - **Streaming results:** expose an async generator so the caller can process results as they complete instead of waiting for all of them.
            - **Concurrency ≠ rate limit:** "max 5 in flight" is different from "max 50 requests per second". A rate limit needs a token bucket or a scheduled release, and you should honour `429` + `Retry-After` from the server.
            - **Node specifics:** HTTP clients have their own connection-pool settings (e.g. `maxSockets` on an `http.Agent`), and database pools (e.g. `pg.Pool({ max })`) already limit concurrency — know which limit is actually in effect instead of stacking them blindly.
            - Production libraries such as `p-limit` implement the same idea; knowing how they work lets you debug them.
        """,
        ex_bn=r"""
            Interviewer যেসব variation নিয়ে চাপ দিতে পারেন:

            - **Settle-all mode:** fail-fast-এর বদলে প্রতিটি item-এর জন্য `{ status, value | reason }` রাখো (`allSettled`-এর মতো) আর কাজ চালিয়ে যাও — bulk job-এর জন্য ভালো, যেখানে শেষে failure report করা হয়।
            - **প্রতি task-এ retry:** প্রতিটি task-কে retry-with-backoff helper দিয়ে wrap করো; retry-গুলো একটা global budget-এর মধ্যে গোনো, যাতে outage-এর সময় load কয়েকগুণ না হয়।
            - **Lazy input / backpressure:** array-র বদলে iterable বা async iterable নাও, যাতে শুরুতেই ১০,০০০টা function (বা লাখো row) তৈরি করতে না হয়। Worker ফাঁকা হলেই কেবল পরের item টানে।
            - **Streaming result:** একটা async generator দাও, যাতে caller সবগুলোর জন্য অপেক্ষা না করে যেটা শেষ হচ্ছে সেটা process করতে পারে।
            - **Concurrency ≠ rate limit:** "একসাথে সর্বোচ্চ ৫টা" আর "প্রতি second-এ সর্বোচ্চ ৫০টা request" আলাদা জিনিস। Rate limit-এর জন্য token bucket বা নির্ধারিত সময়ে ছাড়া লাগে, আর server-এর `429` + `Retry-After` মানা উচিত।
            - **Node-এর খুঁটিনাটি:** HTTP client-এর নিজস্ব connection-pool setting থাকে (যেমন `http.Agent`-এর `maxSockets`), আর database pool (যেমন `pg.Pool({ max })`) আগে থেকেই concurrency সীমিত করে — না বুঝে limit-এর উপর limit না চাপিয়ে জেনে নাও আসলে কোনটা কার্যকর।
            - `p-limit`-এর মতো production library একই ধারণা implement করে; কীভাবে কাজ করে জানলে এগুলো debug করতে পারবে।
        """,
        tip_en=r"""Start by explaining why the input must be functions — it's the insight most candidates miss. Then code the worker loop, and only after it works add fail-fast and cancellation. Comparing with naive batching shows you think about throughput, not just correctness.""",
        tip_bn=r"""শুরুতেই ব্যাখ্যা করো কেন input function হতে হবে — বেশিরভাগ candidate এই অন্তর্দৃষ্টিটা মিস করে। তারপর worker loop লেখো, আর সেটা কাজ করার পরেই fail-fast ও cancellation যোগ করো। সাধারণ batching-এর সাথে তুলনা করলে বোঝা যায় তুমি শুধু সঠিকতা নয়, throughput নিয়েও ভাবো।""",
        mist_en=r"""Passing already-created promises (no limit is possible), pushing results in completion order, using `setInterval` polling to manage slots, or forgetting the empty-array and `limit < 1` cases.""",
        mist_bn=r"""আগেই তৈরি promise pass করা (তখন কোনো limit সম্ভব নয়), শেষ হওয়ার ক্রমে result push করা, slot সামলাতে `setInterval` দিয়ে polling করা, অথবা খালি array আর `limit < 1`-এর case ভুলে যাওয়া।""",
        code=r"""
            async function promisePool(tasks, limit, { signal } = {}) {
              if (!Number.isInteger(limit) || limit < 1) {
                throw new RangeError('limit must be a positive integer');
              }

              const results = new Array(tasks.length);
              let nextIndex = 0;
              let failed = false;

              async function worker() {
                while (!failed && nextIndex < tasks.length) {
                  signal?.throwIfAborted();
                  const index = nextIndex++; // safe: no other code runs between read and increment
                  try {
                    results[index] = await tasks[index]({ signal });
                  } catch (err) {
                    failed = true; // other workers stop picking up new tasks
                    throw err;
                  }
                }
              }

              const workerCount = Math.min(limit, tasks.length);
              await Promise.all(Array.from({ length: workerCount }, worker));
              return results;
            }

            // Usage: 10,000 items, max 5 requests in flight, cancellable
            const controller = new AbortController();
            const tasks = itemIds.map((id) => ({ signal }) =>
              fetch(`/api/items/${id}`, { signal }).then((res) => {
                if (!res.ok) throw new Error(`Item ${id}: HTTP ${res.status}`);
                return res.json();
              }),
            );

            const items = await promisePool(tasks, 5, { signal: controller.signal });
        """,
        lang="javascript",
        time="O(n) scheduling overhead; wall time ≈ total work / limit", space="O(n) results + O(limit) in flight",
        follow=[
            ("How would you turn this into an async generator that yields results as they finish?", "এটাকে এমন async generator-এ কীভাবে রূপান্তর করবে, যেটা কাজ শেষ হওয়ার সাথে সাথে result yield করবে?"),
            ("How is a concurrency limit different from a rate limit, and how would you implement the latter?", "Concurrency limit আর rate limit-এর পার্থক্য কী, আর rate limit কীভাবে implement করবে?"),
        ],
        related=["js-021", "js-024", "js-033"],
        refs=[R_PALL, R_ABORT_THROW, R_ASYNC_FN],
    ),
    # ------------------------------------------------------------------ js-038
    Q(
        id="js-038", sub="Design Patterns (Observer & Reactive State)", diff="extreme", type="architecture",
        prio="medium", market="both", mins=20,
        tags=["observer-pattern", "state-management", "immutability", "batching", "use-sync-external-store"],
        ver="ECMAScript 2026 (framework-agnostic); React 19.3 `useSyncExternalStore` for integration", vs=False, status="stable",
        q_en=r"""Design and implement a tiny framework-agnostic reactive state store: `getState`, `setState`, `subscribe`, plus selector-based subscriptions so a UI part is notified only when the slice it uses changes. Discuss batching, immutability, error isolation, memory, and how you would plug it into React.""",
        q_bn=r"""একটা ছোট, framework-নিরপেক্ষ reactive state store design ও implement করো: `getState`, `setState`, `subscribe`, সাথে selector-ভিত্তিক subscription, যাতে UI-এর একটা অংশ কেবল তখনই notify হয় যখন তার ব্যবহৃত slice বদলায়। Batching, immutability, error isolation, memory, আর React-এ কীভাবে যুক্ত করবে — এগুলো আলোচনা করো।""",
        a_en=r"""
            (Advanced design question.) My design is the observer pattern around a single immutable state value.

            **Core API**
            - `state` lives in a closure; `getState()` returns it.
            - `setState(update)` accepts a new state or an updater `(prev) => next`. If `Object.is(next, prev)`, nothing happens — cheap no-op detection that only works because state is treated as **immutable** (updates create new objects; unchanged branches keep their references).
            - `subscribe(listener)` adds to a `Set` and returns an `unsubscribe` function.

            **Batching:** several `setState` calls in the same tick schedule **one** notification via `queueMicrotask`. Listeners see only the final, consistent state (no intermediate "glitches"), and the UI renders once instead of three times. Trade-off: notifications are asynchronous, so tests must `await` a microtask.

            **Selectors:** `subscribeSelector(store, selector, onChange)` remembers the last selected value and calls `onChange` only when `Object.is` (or a supplied `shallowEqual`) says it changed. Because untouched slices keep their references, most selectors short-circuit.

            **Robustness:** iterate over a copy of the listener set (unsubscribing during notify is safe), and wrap each listener in `try/catch` so one buggy subscriber can't break the others; report errors instead of swallowing them.

            **Memory:** every subscription must be undone; the returned unsubscribe makes cleanup explicit, and in React the hook handles it.

            **React integration:** `useSyncExternalStore(store.subscribe, () => selector(store.getState()))` subscribes safely with concurrent rendering and avoids tearing. Zustand and Redux Toolkit are production versions of this model; signals (Preact, Solid, Angular, Vue refs) are the fine-grained alternative.
        """,
        a_bn=r"""
            (Advanced design প্রশ্ন।) আমার design হলো একটা single immutable state value ঘিরে observer pattern।

            **মূল API**
            - `state` থাকে একটা closure-এ; `getState()` সেটা return করে।
            - `setState(update)` নতুন state বা একটা updater `(prev) => next` নেয়। `Object.is(next, prev)` হলে কিছুই হয় না — সস্তায় no-op ধরা, যেটা কাজ করে কারণ state-কে **immutable** হিসেবে ধরা হয় (update নতুন object তৈরি করে; অপরিবর্তিত branch তাদের reference রেখে দেয়)।
            - `subscribe(listener)` listener-কে একটা `Set`-এ যোগ করে আর একটা `unsubscribe` function return করে।

            **Batching:** একই tick-এ কয়েকটা `setState` হলে `queueMicrotask` দিয়ে **একটাই** notification schedule হয়। Listener শুধু চূড়ান্ত, সামঞ্জস্যপূর্ণ state দেখে (মাঝখানের কোনো "glitch" নয়), আর UI তিনবারের বদলে একবার render হয়। Trade-off: notification asynchronous, তাই test-এ একটা microtask `await` করতে হয়।

            **Selector:** `subscribeSelector(store, selector, onChange)` শেষ selected value মনে রাখে, আর `Object.is` (বা দেওয়া `shallowEqual`) বদল দেখালেই কেবল `onChange` call করে। অপরিবর্তিত slice-গুলো reference রাখে বলে বেশিরভাগ selector তাড়াতাড়ি থেমে যায়।

            **Robustness:** listener set-এর একটা copy ঘুরে notify করো (notify চলাকালীন unsubscribe নিরাপদ থাকে), আর প্রতিটি listener `try/catch`-এ রাখো যাতে একটা buggy subscriber বাকিদের ভাঙতে না পারে; error গিলে না ফেলে report করো।

            **Memory:** প্রতিটি subscription-কে অবশ্যই undo করতে হবে; return করা unsubscribe cleanup-কে স্পষ্ট করে, আর React-এ hook নিজেই এটা সামলায়।

            **React-এ যুক্ত করা:** `useSyncExternalStore(store.subscribe, () => selector(store.getState()))` concurrent rendering-এর সাথে নিরাপদে subscribe করে আর tearing এড়ায়। Zustand আর Redux Toolkit এই model-এরই production version; signals (Preact, Solid, Angular, Vue ref) হলো fine-grained বিকল্প।
        """,
        quick_en=r"""Keep immutable state in a closure with `getState`, `setState` (skipped when `Object.is` sees no change) and `subscribe` returning an unsubscribe. Batch notifications with `queueMicrotask`, isolate listener errors, fire selector subscriptions only when their slice changes, and use `useSyncExternalStore` in React.""",
        quick_bn=r"""Immutable state একটা closure-এ রাখি, সাথে `getState`, `setState` (`Object.is` অনুযায়ী কিছু না বদলালে কিছুই করে না) আর `subscribe`, যেটা unsubscribe function return করে। `queueMicrotask` দিয়ে notification batch করি, listener-এর error আলাদা করে রাখি, selector subscription শুধু নিজের slice বদলালে চলে, আর React-এর সাথে যুক্ত করি `useSyncExternalStore` দিয়ে।""",
        ex_en=r"""
            Trade-offs and failure scenarios to discuss:

            - **Sync vs batched notifications:** sync notification is simpler to test but causes multiple renders and lets listeners observe half-finished multi-step updates. UI frameworks batch updates (React's automatic batching, Vue's microtask scheduler), while stores such as Redux and Zustand notify synchronously and leave batching to the UI layer — both are valid choices. With microtask batching, add a `flush()` for tests.
            - **Mutation bugs:** if someone mutates `state.cart.push(x)` and calls `setState(state)`, `Object.is` sees no change and nobody is notified. Freeze state in development (`Object.freeze` recursively) or use Immer to make accidental mutation fail loudly.
            - **Derived data:** a selector that returns a new array every time (`state.items.filter(...)`) always looks "changed" — memoize derived selectors or compare with `shallowEqual`.
            - **Re-entrancy:** a listener that calls `setState` schedules another batch instead of recursing — safe, but watch for infinite update loops.
            - **Middleware & devtools:** wrapping `setState` gives logging, persistence (`localStorage` with try/catch), undo/time-travel (immutable snapshots make this cheap).
            - **Scaling:** split into slices or multiple stores; keep server state (fetching, caching) in a dedicated tool instead of a global store.
            - **Standards note:** a Signals proposal exists at TC39 but is early-stage and not part of ECMAScript — use library implementations.
        """,
        ex_bn=r"""
            যেসব trade-off আর failure scenario আলোচনা করা উচিত:

            - **Sync বনাম batched notification:** sync notification test করা সহজ, কিন্তু একাধিক render ঘটায় এবং listener-কে বহু-ধাপের update-এর অর্ধেক অবস্থা দেখতে দেয়। UI framework update batch করে (React-এর automatic batching, Vue-র microtask scheduler), আর Redux বা Zustand-এর মতো store synchronously notify করে batching-এর দায়িত্ব UI layer-কে দেয় — দুটোই গ্রহণযোগ্য পছন্দ। Microtask batching করলে test-এর জন্য একটা `flush()` যোগ করো।
            - **Mutation bug:** কেউ যদি `state.cart.push(x)` করে `setState(state)` call করে, `Object.is` কোনো বদল দেখে না আর কেউ notify হয় না। Development-এ state freeze করো (recursively `Object.freeze`) বা Immer ব্যবহার করো, যাতে ভুল করে mutate করলে জোরালোভাবে fail করে।
            - **Derived data:** যে selector প্রতিবার নতুন array return করে (`state.items.filter(...)`), সেটা সবসময় "বদলেছে" মনে হয় — derived selector memoize করো বা `shallowEqual` দিয়ে compare করো।
            - **Re-entrancy:** কোনো listener `setState` call করলে recursion না হয়ে আরেকটা batch schedule হয় — নিরাপদ, তবে অসীম update loop-এর দিকে খেয়াল রাখো।
            - **Middleware ও devtools:** `setState` wrap করে logging, persistence (try/catch সহ `localStorage`), undo/time-travel পাওয়া যায় (immutable snapshot থাকায় এটা সস্তা)।
            - **Scaling:** slice বা একাধিক store-এ ভাগ করো; server state (fetching, caching) global store-এ না রেখে আলাদা tool-এ রাখো।
            - **Standard-এর কথা:** TC39-তে একটা Signals proposal আছে, তবে সেটা প্রাথমিক পর্যায়ে এবং ECMAScript-এর অংশ নয় — library implementation ব্যবহার করো।
        """,
        tip_en=r"""Structure it like a design review: requirements → API → core implementation → batching → selectors → failure modes → integration. Writing the 30-line store live and then discussing trade-offs is far more convincing than naming libraries.""",
        tip_bn=r"""এটাকে design review-এর মতো সাজাও: requirement → API → মূল implementation → batching → selector → failure mode → integration। ৩০ লাইনের store সরাসরি লিখে তারপর trade-off আলোচনা করা, শুধু library-র নাম বলার চেয়ে অনেক বেশি বিশ্বাসযোগ্য।""",
        mist_en=r"""Mutating state in place (breaking change detection), notifying synchronously inside a loop of updates, forgetting to return an unsubscribe function, or letting one throwing listener stop the rest.""",
        mist_bn=r"""State সরাসরি mutate করা (change detection ভেঙে যায়), update-এর loop-এর ভেতরে synchronously notify করা, unsubscribe function return করতে ভুলে যাওয়া, অথবা একটা throw করা listener-কে বাকিদের থামিয়ে দিতে দেওয়া।""",
        code=r"""
            function createStore(initialState) {
              let state = initialState;
              const listeners = new Set();
              let scheduled = false;

              function notify() {
                scheduled = false;
                const snapshot = state;
                for (const listener of [...listeners]) { // copy: safe if a listener unsubscribes
                  try {
                    listener(snapshot);
                  } catch (err) {
                    console.error('Store listener failed', err); // isolate failures
                  }
                }
              }

              return {
                getState: () => state,
                setState(update) {
                  const next = typeof update === 'function' ? update(state) : update;
                  if (Object.is(next, state)) return; // immutable updates → cheap change check
                  state = next;
                  if (!scheduled) {
                    scheduled = true;
                    queueMicrotask(notify); // batch: one notification per tick
                  }
                },
                subscribe(listener) {
                  listeners.add(listener);
                  return () => listeners.delete(listener);
                },
              };
            }

            function subscribeSelector(store, selector, onChange, isEqual = Object.is) {
              let current = selector(store.getState());
              return store.subscribe((state) => {
                const next = selector(state);
                if (isEqual(next, current)) return;
                const previous = current;
                current = next;
                onChange(next, previous);
              });
            }

            // Usage
            const store = createStore({ cart: [], user: null });
            const stop = subscribeSelector(store, (s) => s.cart.length, (n, prev) => console.log(`cart: ${prev} -> ${n}`));

            store.setState((s) => ({ ...s, cart: [...s.cart, 'mouse'] }));
            store.setState((s) => ({ ...s, cart: [...s.cart, 'keyboard'] }));
            // one log after the current tick: "cart: 0 -> 2"

            // React integration
            // const cartCount = useSyncExternalStore(store.subscribe, () => store.getState().cart.length);
        """,
        lang="javascript",
        follow=[
            ("Why does `useSyncExternalStore` exist instead of `useEffect` + `useState` for external stores?", "External store-এর জন্য `useEffect` + `useState`-এর বদলে `useSyncExternalStore` কেন আছে?"),
            ("How would you add computed (derived) values that update automatically?", "স্বয়ংক্রিয়ভাবে update হওয়া computed (derived) value কীভাবে যোগ করবে?"),
        ],
        related=["js-014", "js-032", "js-016"],
        refs=[R_QMT, R_SET, R_USESES],
    ),
    # ------------------------------------------------------------------ js-039
    Q(
        id="js-039", sub="DOM Manipulation & Performance", diff="extreme", type="scenario",
        prio="medium", market="international", mins=20,
        tags=["performance", "dom", "requestanimationframe", "web-workers", "virtualization", "websocket"],
        ver="Web platform, 2026 (rAF, Web Workers, `content-visibility` Baseline newly available)", vs=False, status="stable",
        q_en=r"""A live market-price dashboard receives about 1,000 WebSocket messages per second and shows a table of 5,000 rows. The UI stutters, CPU usage is high and clicks feel laggy. How do you find the bottlenecks and re-architect the client so it stays smooth at 60 fps?""",
        q_bn=r"""একটা live market-price dashboard প্রতি second-এ প্রায় ১,০০০টা WebSocket message পায় আর ৫,০০০ row-এর একটা table দেখায়। UI আটকে আটকে চলে, CPU usage বেশি, আর click করলে দেরিতে সাড়া দেয়। Bottleneck কীভাবে খুঁজবে, আর client-কে কীভাবে নতুন করে সাজাবে যাতে 60 fps-এ smooth থাকে?""",
        a_en=r"""
            (Advanced scenario.) At 60 fps each frame has about 16 ms for JavaScript, style, layout and paint combined. Updating the DOM once per message — 1,000 times a second — can't fit.

            **1. Clarify & measure.** How many rows are visible? Do users need every tick or only the latest price? Record a DevTools Performance profile: look for long tasks, "Forced reflow" warnings (layout thrashing) and per-message work. Track INP for click latency.

            **2. Decouple message rate from render rate.** Buffer incoming ticks in a `Map` keyed by symbol (latest value wins), and flush **once per frame** with `requestAnimationFrame`. 1,000 messages/s become at most 60 DOM updates/s, and the buffer stays bounded because coalescing overwrites old ticks.

            **3. Move parsing off the main thread.** Run the WebSocket, `JSON.parse` and aggregation inside a **Web Worker**; post one batched diff per frame to the UI thread (transfer `ArrayBuffer`s for binary data).

            **4. Touch less DOM.** Virtualise the table (render only the ~40 visible rows plus a buffer), keep references to cell nodes and update only changed cells via `textContent`, use event delegation for row clicks, and use CSS `transform`/`opacity` for "price flash" effects so they run on the compositor.

            **5. Avoid layout thrashing.** Within a frame, do all reads (measurements) first, then all writes. Never read `offsetHeight` or `getBoundingClientRect()` inside the update loop.

            **6. Protect the system.** Cap history arrays (ring buffers), handle hidden tabs (rAF pauses, so coalescing keeps the buffer small), reconnect with backoff and resync from a snapshot using sequence numbers. Ask the backend to send only subscribed/visible symbols or pre-aggregate.
        """,
        a_bn=r"""
            (Advanced scenario।) 60 fps-এ প্রতিটি frame-এ JavaScript, style, layout আর paint মিলিয়ে মোটামুটি 16 ms সময় থাকে। প্রতিটি message-এ একবার করে DOM update — second-এ ১,০০০ বার — এর মধ্যে আঁটে না।

            **1. পরিষ্কার করো ও মাপো।** কয়টা row দেখা যায়? User-এর কি প্রতিটি tick দরকার, নাকি শুধু সর্বশেষ দাম? DevTools Performance profile record করো: long task, "Forced reflow" warning (layout thrashing) আর প্রতি message-এর কাজ খোঁজো। Click-এর দেরির জন্য INP মাপো।

            **2. Message-এর হার আর render-এর হার আলাদা করো।** আসা tick-গুলো symbol-কে key ধরে একটা `Map`-এ buffer করো (সর্বশেষ value জেতে), আর `requestAnimationFrame` দিয়ে **প্রতি frame-এ একবার** flush করো। ১,০০০ message/s হয়ে যায় সর্বোচ্চ 60টা DOM update/s, আর coalescing পুরনো tick overwrite করে বলে buffer সীমিত থাকে।

            **3. Parsing main thread থেকে সরাও।** WebSocket, `JSON.parse` আর aggregation একটা **Web Worker**-এর ভেতরে চালাও; প্রতি frame-এ UI thread-এ একটা batched diff পাঠাও (binary data হলে `ArrayBuffer` transfer করো)।

            **4. কম DOM ছোঁও।** Table virtualise করো (শুধু দৃশ্যমান ~৪০টা row আর একটু buffer render), cell node-এর reference রেখে শুধু বদলানো cell `textContent` দিয়ে update করো, row click-এর জন্য event delegation ব্যবহার করো, আর "price flash" effect-এর জন্য CSS `transform`/`opacity` ব্যবহার করো যাতে সেটা compositor-এ চলে।

            **5. Layout thrashing এড়াও।** একটা frame-এর মধ্যে আগে সব read (measurement), তারপর সব write। Update loop-এর ভেতরে কখনো `offsetHeight` বা `getBoundingClientRect()` পড়ো না।

            **6. System রক্ষা করো।** History array-র সীমা দাও (ring buffer), hidden tab handle করো (rAF থেমে যায়, তাই coalescing buffer ছোট রাখে), backoff সহ reconnect করো আর sequence number দিয়ে snapshot থেকে resync করো। Backend-কে বলো শুধু subscribed/দৃশ্যমান symbol পাঠাতে বা আগে থেকে aggregate করতে।
        """,
        quick_en=r"""Profile first, then decouple the message rate from the render rate: coalesce ticks in a `Map` by symbol and flush once per `requestAnimationFrame`. Then parse in a Web Worker, virtualise the table to the visible rows, update only changed cells, and do all layout reads before writes.""",
        quick_bn=r"""আগে profile করি, তারপর message rate আর render rate আলাদা করি: tick-গুলো symbol অনুযায়ী একটা `Map`-এ জমিয়ে প্রতি `requestAnimationFrame`-এ একবার flush করি। এরপর parsing Web Worker-এ পাঠাই, table virtualise করে শুধু দেখা যাওয়া row render করি, শুধু বদলানো cell update করি, আর সব layout read আগে করে তারপর write করি।""",
        ex_en=r"""
            - **Why rAF and not a timer?** `requestAnimationFrame` runs right before the browser paints, so all DOM writes for a frame land together. A `setInterval(16)` drifts relative to the display and can update twice in one frame or miss frames.
            - **Layout thrashing explained:** writing a style then reading a layout property forces the browser to recalculate layout synchronously. In a loop over 5,000 rows that's 5,000 forced layouts per frame.
            - **Rendering cost levers:** `content-visibility: auto` (Baseline newly available) skips rendering work for off-screen sections; CSS `contain` limits how far layout changes propagate.
            - **Worker trade-offs:** messages are structured-cloned, so post compact diffs, not the whole table. If the main thread still dominates, the bottleneck is DOM work, not parsing — measure before and after.
            - **Success criteria:** no long tasks during steady load, frame time under ~16 ms, INP under 200 ms, flat memory over hours.
            - **Framework note:** in React, keep the high-frequency stream outside component state (an external store read with `useSyncExternalStore` per visible row, or direct DOM updates in a ref) so 1,000 messages don't trigger 1,000 renders.
        """,
        ex_bn=r"""
            - **Timer নয়, rAF কেন?** `requestAnimationFrame` browser paint করার ঠিক আগে চলে, তাই একটা frame-এর সব DOM write একসাথে পড়ে। `setInterval(16)` display-এর সাথে তাল হারায় — এক frame-এ দুইবার update করতে পারে বা frame মিস করতে পারে।
            - **Layout thrashing-এর ব্যাখ্যা:** style লিখে তারপর layout property পড়লে browser-কে synchronously layout আবার হিসাব করতে হয়। ৫,০০০ row-এর loop-এ সেটা প্রতি frame-এ ৫,০০০টা forced layout।
            - **Rendering খরচ কমানোর উপায়:** `content-visibility: auto` (Baseline newly available) screen-এর বাইরের অংশের rendering-এর কাজ বাদ দেয়; CSS `contain` layout change কতদূর ছড়াবে তা সীমিত করে।
            - **Worker-এর trade-off:** message structured-clone হয়, তাই পুরো table নয়, ছোট diff পাঠাও। তারপরও main thread ব্যস্ত থাকলে bottleneck parsing নয়, DOM-এর কাজ — আগে-পরে মেপে দেখো।
            - **সাফল্যের মাপকাঠি:** স্থির load-এ কোনো long task নেই, frame time ~16 ms-এর নিচে, INP 200 ms-এর নিচে, ঘণ্টার পর ঘণ্টা memory সমতল।
            - **Framework-এর কথা:** React-এ high-frequency stream component state-এর বাইরে রাখো (প্রতি দৃশ্যমান row-এ `useSyncExternalStore` দিয়ে পড়া একটা external store, বা ref-এ সরাসরি DOM update), যাতে ১,০০০ message ১,০০০টা render না ঘটায়।
        """,
        tip_en=r"""Open with the frame budget ("~16 ms per frame, 1,000 updates/s can't fit"), then present the fixes in order of impact: coalesce per frame → virtualise → worker → layout hygiene. Ending with measurable success criteria makes it a senior answer.""",
        tip_bn=r"""শুরু করো frame budget দিয়ে ("প্রতি frame-এ ~16 ms, ১,০০০ update/s আঁটবে না"), তারপর প্রভাব অনুযায়ী সমাধান সাজাও: প্রতি frame-এ coalesce → virtualise → worker → layout-এর পরিচ্ছন্নতা। মাপা যায় এমন সাফল্যের মাপকাঠি দিয়ে শেষ করলে উত্তরটা senior-level হয়।""",
        mist_en=r"""Re-rendering the whole table with `innerHTML` on every message, throttling with `setTimeout` but still doing per-message DOM work, or moving work to a worker without measuring that parsing was the bottleneck.""",
        mist_bn=r"""প্রতিটি message-এ `innerHTML` দিয়ে পুরো table আবার render করা, `setTimeout` দিয়ে throttle করেও প্রতি message-এ DOM-এর কাজ করা, অথবা parsing-ই যে bottleneck তা না মেপে কাজ worker-এ সরিয়ে দেওয়া।""",
        code=r"""
            const pending = new Map(); // symbol -> latest tick (coalesced)
            let frameRequested = false;

            socket.addEventListener('message', (event) => {
              const tick = JSON.parse(event.data); // move to a Worker if profiling shows parsing is heavy
              pending.set(tick.symbol, tick);
              if (!frameRequested) {
                frameRequested = true;
                requestAnimationFrame(flush);
              }
            });

            function flush() {
              frameRequested = false;
              // Writes only — no layout reads inside this loop
              for (const [symbol, tick] of pending) {
                const row = visibleRows.get(symbol); // only rows currently rendered (virtualised)
                if (!row) continue;
                row.priceCell.textContent = tick.price.toFixed(2);
                row.el.classList.toggle('up', tick.change >= 0);
              }
              pending.clear();
            }

            // Layout thrashing (avoid): read → write → read → write ... forces layout every iteration
            // for (const el of cells) { el.style.width = el.parentNode.offsetWidth / 2 + 'px'; }
            // Better: read everything first, then write everything
            // const widths = cells.map((el) => el.parentNode.offsetWidth);
            // cells.forEach((el, i) => { el.style.width = widths[i] / 2 + 'px'; });
        """,
        lang="javascript",
        follow=[
            ("How would you implement list virtualisation without a library?", "Library ছাড়া list virtualisation কীভাবে implement করবে?"),
            ("What changes if users need every tick for an audit log, not only the latest price?", "User-দের যদি শুধু সর্বশেষ দাম নয়, audit log-এর জন্য প্রতিটি tick দরকার হয়, তাহলে কী বদলাবে?"),
        ],
        related=["js-034", "js-020", "js-010", "js-032"],
        refs=[R_RAF, R_LAYOUT, R_LONG_TASKS],
    ),
    # ------------------------------------------------------------------ js-040
    Q(
        id="js-040", sub="Performance (Engine Optimisations)", diff="extreme", type="security-performance",
        prio="low", market="international", mins=15,
        tags=["performance", "v8", "hidden-classes", "inline-caches", "deoptimization", "nodejs"],
        ver="V8 (Chrome, Node.js 24/26) — engine internals, may change between versions", vs=False, status="stable",
        q_en=r"""After a refactor, a Node.js service that transforms about a million order objects per minute became several times slower, although the algorithm didn't change. The diff shows that objects now get optional fields added conditionally, some fields are removed with `delete`, and one hot function now receives objects from many different sources. What likely happened inside V8, how would you confirm it, and how would you fix it?""",
        q_bn=r"""একটা refactor-এর পর প্রতি মিনিটে প্রায় ১০ লাখ order object transform করা একটা Node.js service কয়েকগুণ ধীর হয়ে গেছে, যদিও algorithm বদলায়নি। Diff-এ দেখা যাচ্ছে object-এ এখন শর্তসাপেক্ষে optional field যোগ হয়, কিছু field `delete` দিয়ে মোছা হয়, আর একটা hot function এখন অনেক আলাদা উৎস থেকে object পায়। V8-এর ভেতরে সম্ভবত কী ঘটেছে, কীভাবে নিশ্চিত হবে, আর কীভাবে ঠিক করবে?""",
        a_en=r"""
            (Advanced — engine internals; profile before acting on any of this.)

            **What probably happened:** V8 gives every object a hidden class (V8 calls it a *Map*, often called a "shape") describing which properties it has and in what order. Objects created the same way share a shape, and optimised code uses **inline caches** keyed by shape to read a property with a single check and a fixed offset.

            - Adding properties conditionally or in different orders produces **different shapes** for "the same" kind of object.
            - A hot function that sees one shape is *monomorphic* (fastest); a few shapes is *polymorphic*; many shapes makes the access site *megamorphic*, falling back to a slower generic lookup.
            - `delete` usually switches the object to **dictionary (slow) mode** — properties are then stored in a hash table.
            - Optimised code built on assumptions that are later violated gets **deoptimised** back to the interpreter, sometimes repeatedly.

            **Confirm:** profile first (`node --cpu-prof`, flame graphs) to find the hot function. Then run with `--trace-deopt` to see deopt reasons such as "wrong map". In a micro-test with `--allow-natives-syntax`, `%HaveSameMap(a, b)` and `%HasFastProperties(obj)` show the shape problem directly.

            **Fix:**
            - Create objects in one place with **all fields in the same order** (a factory or class), using `null`/`undefined` for "missing" instead of adding fields later.
            - Replace `delete obj.field` with `obj.field = undefined`, or build a new object without the field at the boundary.
            - Normalise heterogeneous inputs into one internal shape at the edge of the system, so the hot path stays monomorphic.
            - Keep arrays dense and homogeneous (no holes; don't mix integers, doubles and objects).
            - Use `Map` for genuinely dynamic keys — that's what it's for.
        """,
        a_bn=r"""
            (Advanced — engine-এর ভেতরের বিষয়; এর কোনোটার উপর কাজ করার আগে profile করো।)

            **সম্ভবত যা ঘটেছে:** V8 প্রতিটি object-কে একটা hidden class দেয় (V8 একে *Map* বলে, প্রায়ই "shape" বলা হয়), যেটা বলে object-এ কোন property আছে আর কোন ক্রমে। একইভাবে তৈরি object একই shape share করে, আর optimised code shape-কে key ধরে **inline cache** ব্যবহার করে — একটা check আর নির্দিষ্ট offset দিয়েই property পড়ে ফেলে।

            - শর্তসাপেক্ষে বা ভিন্ন ক্রমে property যোগ করলে "একই" ধরনের object-এর **আলাদা shape** তৈরি হয়।
            - কোনো hot function একটা shape দেখলে সেটা *monomorphic* (সবচেয়ে দ্রুত); কয়েকটা shape হলে *polymorphic*; অনেক shape হলে access site *megamorphic* হয়ে ধীর generic lookup-এ ফিরে যায়।
            - `delete` সাধারণত object-কে **dictionary (slow) mode**-এ নিয়ে যায় — তখন property একটা hash table-এ থাকে।
            - যে optimised code-এর অনুমান পরে ভেঙে যায়, সেটা **deoptimise** হয়ে আবার interpreter-এ ফেরে, কখনো বারবার।

            **নিশ্চিত হওয়া:** আগে profile করো (`node --cpu-prof`, flame graph) hot function খুঁজতে। তারপর `--trace-deopt` দিয়ে চালিয়ে "wrong map"-এর মতো deopt-এর কারণ দেখো। `--allow-natives-syntax` সহ একটা micro-test-এ `%HaveSameMap(a, b)` আর `%HasFastProperties(obj)` সরাসরি shape-এর সমস্যা দেখায়।

            **সমাধান:**
            - Object এক জায়গায় তৈরি করো, **সব field একই ক্রমে** (factory বা class), পরে field যোগ না করে "নেই" বোঝাতে `null`/`undefined` ব্যবহার করো।
            - `delete obj.field`-এর বদলে `obj.field = undefined`, অথবা boundary-তে field ছাড়া নতুন object বানাও।
            - System-এর প্রান্তে ভিন্ন ভিন্ন input-কে একটা internal shape-এ normalise করো, যাতে hot path monomorphic থাকে।
            - Array dense আর একই ধরনের রাখো (hole নয়; integer, double আর object মেশানো নয়)।
            - সত্যিকারের dynamic key-এর জন্য `Map` ব্যবহার করো — এটা সেজন্যই।
        """,
        quick_en=r"""Conditional fields, changing property order and `delete` create many hidden classes (shapes), so hot accesses go polymorphic or megamorphic, `delete` forces slow dictionary mode, and V8 deoptimises. Confirm with a CPU profile and `--trace-deopt`, then build every object in one factory with the same fields in the same order.""",
        quick_bn=r"""Conditional field, বদলে যাওয়া property order আর `delete`-এর কারণে object-গুলোর অনেক hidden class (shape) তৈরি হয়, তাই hot property access polymorphic বা megamorphic হয়ে যায়, `delete` object-কে ধীর dictionary mode-এ পাঠায়, আর V8 deoptimise করে। CPU profile আর `--trace-deopt` দিয়ে নিশ্চিত হও, তারপর প্রতিটা object একটা factory-তে একই order-এ সব field দিয়ে তৈরি করো।""",
        ex_en=r"""
            - **Elements kinds:** V8 also tracks array element types (small integers → doubles → generic objects, packed vs holey). Transitions only go towards the more general kind — one `arr.push(1.5)` or a hole can permanently slow down a hot array.
            - **Type stability:** changing a field's type (number ↔ string) also creates new shapes/representations; keep fields monomorphic in type, not just in presence.
            - **Other engines** (SpiderMonkey "shapes", JavaScriptCore "structures") use similar ideas, but details differ and change between versions — that's why you verify with a profiler on your target runtime instead of following folklore.
            - **When it matters:** only in genuinely hot paths (millions of operations). For typical app code, readability wins; these rules are cheap to follow in factories/classes anyway.
            - **Prevent regressions:** add a benchmark (e.g. with `node:test` + a timing budget or a dedicated benchmark suite) for the hot transform so a future refactor that changes shapes is caught in CI.
            - TypeScript helps indirectly: well-typed objects with fixed fields tend to produce consistent shapes, but types are erased at runtime, so they guarantee nothing by themselves.
        """,
        ex_bn=r"""
            - **Elements kinds:** V8 array-র element type-ও track করে (ছোট integer → double → generic object, packed বনাম holey)। Transition শুধু আরও সাধারণ kind-এর দিকে যায় — একটা `arr.push(1.5)` বা একটা hole একটা hot array-কে স্থায়ীভাবে ধীর করে দিতে পারে।
            - **Type stability:** কোনো field-এর type বদলালে (number ↔ string) নতুন shape/representation তৈরি হয়; field শুধু উপস্থিতিতে নয়, type-এও monomorphic রাখো।
            - **অন্য engine** (SpiderMonkey-র "shapes", JavaScriptCore-এর "structures") একই রকম ধারণা ব্যবহার করে, কিন্তু খুঁটিনাটি আলাদা এবং version-ভেদে বদলায় — এজন্যই প্রচলিত ধারণা না মেনে নিজের target runtime-এ profiler দিয়ে যাচাই করো।
            - **কখন গুরুত্বপূর্ণ:** শুধু সত্যিকারের hot path-এ (লাখো operation)। সাধারণ app code-এ readability-ই জেতে; তবে factory/class-এ এই নিয়মগুলো মানা এমনিতেই সস্তা।
            - **Regression ঠেকাও:** hot transform-এর জন্য একটা benchmark যোগ করো (যেমন `node:test` + timing budget বা আলাদা benchmark suite), যাতে ভবিষ্যতের কোনো refactor shape বদলালে CI-তেই ধরা পড়ে।
            - TypeScript পরোক্ষভাবে সাহায্য করে: নির্দিষ্ট field সহ ভালোভাবে typed object সাধারণত একই shape তৈরি করে, কিন্তু runtime-এ type মুছে যায়, তাই নিজে থেকে কিছুই নিশ্চিত করে না।
        """,
        tip_en=r"""Say "I'd profile first" before any theory. Then explain shapes → inline caches → megamorphic/deopt in three sentences, and finish with concrete code-level fixes. Interviewers value the measured approach more than V8 vocabulary.""",
        tip_bn=r"""যেকোনো তত্ত্বের আগে বলো "আমি আগে profile করব"। তারপর তিন বাক্যে shape → inline cache → megamorphic/deopt ব্যাখ্যা করো, আর শেষ করো code-level-এর নির্দিষ্ট সমাধান দিয়ে। Interviewer V8-এর শব্দভান্ডারের চেয়ে মেপে কাজ করার পদ্ধতিকে বেশি মূল্য দেন।""",
        mist_en=r"""Micro-optimising without a profile, believing `delete` is "free", or assuming TypeScript types guarantee consistent runtime shapes.""",
        mist_bn=r"""Profile ছাড়াই micro-optimise করা, ভাবা যে `delete` "বিনামূল্যে", অথবা ধরে নেওয়া যে TypeScript type runtime-এ একই shape নিশ্চিত করে।""",
        code=r"""
            // Slow: shape depends on the input → polymorphic/megamorphic access, plus dictionary mode
            function toOrderSlow(raw) {
              const order = {};
              if (raw.coupon) order.discount = raw.coupon.amount; // optional field first, sometimes
              order.id = raw.id;
              order.total = raw.total;
              if (order.discount === 0) delete order.discount;     // delete → slow properties
              return order;
            }

            // Fast: one factory, same fields, same order, every time
            function toOrder(raw) {
              return {
                id: raw.id,
                total: raw.total,
                discount: raw.coupon ? raw.coupon.amount : 0,
                giftNote: raw.isGift ? raw.note : null,
              };
            }

            // Verify in a micro-test:  node --allow-natives-syntax shapes.js
            // console.log(%HaveSameMap(toOrder(a), toOrder(b)));   // true
            // console.log(%HasFastProperties(toOrderSlow({ id: 3, total: 30, coupon: { amount: 0 } }))); // false after delete
            // Find deopts in the real service:  node --trace-deopt server.js | grep -i "wrong map"
        """,
        lang="javascript",
        follow=[
            ("What is the difference between monomorphic, polymorphic and megamorphic inline caches?", "Monomorphic, polymorphic আর megamorphic inline cache-এর পার্থক্য কী?"),
            ("How would you add a performance regression test to CI?", "CI-তে একটা performance regression test কীভাবে যোগ করবে?"),
        ],
        related=["js-039", "js-036"],
        refs=[R_V8_MAPS, R_V8_PROPS, R_V8_ELEMENTS],
    ),
]

if __name__ == "__main__":
    save("javascript", "b6", QUESTIONS)
