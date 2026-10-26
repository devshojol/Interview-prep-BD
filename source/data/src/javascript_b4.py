import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
R_CLOSURES = ("MDN — Closures", f"{MDN}/Guide/Closures")
R_MAP = ("MDN — Map", f"{MDN}/Reference/Global_Objects/Map")
R_GETORINSERT_C = ("MDN — Map.prototype.getOrInsertComputed()", f"{MDN}/Reference/Global_Objects/Map/getOrInsertComputed")
R_ASYNC_FN = ("MDN — async function", f"{MDN}/Reference/Statements/async_function")
R_TRYCATCH = ("MDN — try...catch", f"{MDN}/Reference/Statements/try...catch")
R_FOREACH = ("MDN — Array.prototype.forEach()", f"{MDN}/Reference/Global_Objects/Array/forEach")
R_FOROF = ("MDN — for...of", f"{MDN}/Reference/Statements/for...of")
R_EXEC_MODEL = ("MDN — JavaScript execution model", f"{MDN}/Reference/Execution_model")
R_MODULES = ("MDN — JavaScript modules", f"{MDN}/Guide/Modules")
R_NODE_ESM = ("Node.js — ECMAScript modules", "https://nodejs.org/api/esm.html")
R_NODE_CJS = ("Node.js — CommonJS modules", "https://nodejs.org/api/modules.html")
R_ITERATOR = ("MDN — Iterator", f"{MDN}/Reference/Global_Objects/Iterator")
R_ITER_TAKE = ("MDN — Iterator.prototype.take()", f"{MDN}/Reference/Global_Objects/Iterator/take")
R_PRIVATE = ("MDN — Private elements", f"{MDN}/Reference/Classes/Private_elements")
R_CLASSES = ("MDN — Classes", f"{MDN}/Reference/Classes")

QUESTIONS = [
    # ------------------------------------------------------------------ js-022
    Q(
        id="js-022", sub="Functional Programming", diff="medium", type="coding",
        prio="medium", market="both", mins=8,
        tags=["memoization", "pure-functions", "higher-order-functions", "lru-cache", "currying"],
        ver="ECMAScript 2026 (manual version works in any ES2015+ runtime; `getOrInsertComputed` is ES2026)", vs=True, status="stable",
        q_en=r"""
            Implement `memoize(fn, options)` that caches the results of a function by its arguments.

            - Optional `getKey(...args)` to build the cache key (default: `JSON.stringify(args)`).
            - Optional `maxSize`; when the cache is full, evict the **least recently used** entry.
            - `this` and all arguments must be forwarded to `fn`.

            Example: `const charge = memoize(deliveryCharge, { maxSize: 100 }); charge('Dhaka', 2); charge('Dhaka', 2);` → the second call returns the cached value without calling `deliveryCharge`.

            When is memoization safe, and how does it relate to functional-programming ideas?
        """,
        q_bn=r"""
            `memoize(fn, options)` implement করো, যেটা argument অনুযায়ী একটা function-এর result cache করবে।

            - Optional `getKey(...args)` দিয়ে cache key তৈরি হবে (default: `JSON.stringify(args)`)।
            - Optional `maxSize`; cache ভরে গেলে **সবচেয়ে কম সম্প্রতি ব্যবহৃত** (LRU) entry বাদ দেবে।
            - `this` আর সব argument `fn`-এ পৌঁছাতে হবে।

            উদাহরণ: `const charge = memoize(deliveryCharge, { maxSize: 100 }); charge('Dhaka', 2); charge('Dhaka', 2);` → দ্বিতীয় call `deliveryCharge` call না করেই cache থেকে value দেবে।

            Memoization কখন নিরাপদ, আর functional programming-এর ধারণাগুলোর সাথে এর সম্পর্ক কী?
        """,
        a_en=r"""
            `memoize` is a **higher-order function**: it takes a function and returns a new one that closes over a `Map`. On each call I build a key; on a hit I return the cached value, on a miss I call `fn.apply(this, args)`, store the result and return it. For LRU I use the fact that a `Map` keeps insertion order: on a hit I delete and re-insert the key (moving it to the "newest" end), and when the size exceeds `maxSize` I delete the first key, `cache.keys().next().value`. Lookups are O(1) on average, plus the cost of building the key.

            Memoization is only safe for **pure functions** — same inputs always give the same output and there are no side effects (no network calls, no reading `Date.now()`, no mutating arguments). That's the core FP idea: pure functions are referentially transparent, so a call can be replaced by its result. Memoize, debounce, compose and curry are all examples of higher-order functions built on closures.
        """,
        a_bn=r"""
            `memoize` একটা **higher-order function**: এটা একটা function নেয় আর নতুন একটা function return করে, যেটা একটা `Map`-কে closure-এ ধরে রাখে। প্রতিটি call-এ key তৈরি করি; cache-এ পেলে সেই value return করি, না পেলে `fn.apply(this, args)` call করে result জমা রেখে return করি। LRU-র জন্য কাজে লাগাই যে `Map` insertion order রাখে: hit হলে key-টা delete করে আবার insert করি (ফলে সেটা "নতুনতম" প্রান্তে চলে যায়), আর size `maxSize` ছাড়িয়ে গেলে প্রথম key, `cache.keys().next().value`, মুছে দিই। Lookup গড়ে O(1), সাথে key তৈরির খরচ।

            Memoization কেবল **pure function**-এর জন্য নিরাপদ — একই input-এ সবসময় একই output, কোনো side effect নেই (network call নেই, `Date.now()` পড়া নেই, argument mutate করা নেই)। এটাই FP-এর মূল ধারণা: pure function referentially transparent, তাই একটা call-কে তার result দিয়ে বদলে দেওয়া যায়। Memoize, debounce, compose, curry — সবই closure-এর উপর তৈরি higher-order function-এর উদাহরণ।
        """,
        quick_en=r"""Return a function that closes over a `Map`: build a key, return the cached value on a hit, otherwise call `fn.apply(this, args)` and store the result. For LRU, delete and re-insert the key on a hit and evict the first key when the size passes `maxSize`; memoize only pure functions.""",
        quick_bn=r"""এমন একটা function return করি যেটা একটা `Map`-এর উপর closure রাখে: key বানাই, cache-এ থাকলে সেটা return করি, না থাকলে `fn.apply(this, args)` call করে result রেখে দিই। LRU-র জন্য hit হলে key delete করে আবার insert করি, আর size `maxSize` ছাড়ালে প্রথম key বাদ দিই; memoize শুধু pure function-এর জন্য নিরাপদ।""",
        ex_en=r"""
            - **Key pitfalls:** `JSON.stringify` treats `{a:1,b:2}` and `{b:2,a:1}` as different keys, turns `undefined` and functions into `null` inside arrays (so two different callback arguments produce the same key), drops them from objects, and throws on cycles/BigInt. For a single object argument, key by identity with a `WeakMap` — entries disappear when the object is garbage-collected.
            - **Recursion:** `fib` must call the *memoized* version, otherwise only the top-level call is cached.
            - **Async functions:** cache the promise (so concurrent callers share one request) and delete the entry if it rejects, or you'll cache the failure forever.
            - **Unbounded caches are memory leaks** in long-running apps — hence `maxSize` or a TTL.
            - **ES2026:** `cache.getOrInsertComputed(key, () => fn(...args))` (Map upsert, Baseline 2026 / Node 26) replaces the `has`/`get`/`set` dance for simple caches; the callback runs only on a miss.
            - **Currying** (bonus block) turns `f(a, b, c)` into `f(a)(b)(c)` — handy for building specialised functions like `const dhakaCharge = charge('Dhaka')`.
            - In React, `useMemo`/`React.memo` and the React Compiler apply the same idea at component level.
        """,
        ex_bn=r"""
            - **Key-এর ফাঁদ:** `JSON.stringify` `{a:1,b:2}` আর `{b:2,a:1}`-কে আলাদা key ধরে, array-র ভেতরের `undefined` আর function-কে `null` বানায় (ফলে দুটো আলাদা callback argument একই key দেয়), object থেকে এগুলো বাদ দেয়, আর cycle/BigInt পেলে throw করে। একটাই object argument হলে `WeakMap` দিয়ে identity অনুযায়ী key রাখো — object garbage-collect হলে entry-ও চলে যায়।
            - **Recursion:** `fib`-কে অবশ্যই *memoized* version call করতে হবে, নাহলে শুধু top-level call cache হবে।
            - **Async function:** promise-টাই cache করো (যাতে একসাথে আসা caller-রা একটাই request share করে), আর reject করলে entry মুছে দাও — নাহলে failure চিরকাল cache-এ থেকে যাবে।
            - **সীমাহীন cache মানেই memory leak**, বিশেষ করে দীর্ঘক্ষণ চলা app-এ — এজন্যই `maxSize` বা TTL।
            - **ES2026:** সাধারণ cache-এর জন্য `has`/`get`/`set`-এর ঝামেলার বদলে `cache.getOrInsertComputed(key, () => fn(...args))` (Map upsert, Baseline 2026 / Node 26) ব্যবহার করা যায়; callback শুধু miss হলেই চলে।
            - **Currying** (bonus block) `f(a, b, c)`-কে `f(a)(b)(c)` বানায় — `const dhakaCharge = charge('Dhaka')`-এর মতো specialised function তৈরিতে কাজে লাগে।
            - React-এ `useMemo`/`React.memo` আর React Compiler component-level-এ একই ধারণা প্রয়োগ করে।
        """,
        tip_en=r"""Start with the 6-line unbounded version, then add LRU using Map ordering — interviewers like seeing you iterate. Say "only for pure functions" early, and mention the async/rejection and memory-growth caveats.""",
        tip_bn=r"""আগে ৬ লাইনের সীমাহীন version লেখো, তারপর Map-এর ordering দিয়ে LRU যোগ করো — interviewer ধাপে ধাপে উন্নতি দেখতে পছন্দ করেন। শুরুতেই "শুধু pure function-এর জন্য" বলো, আর async/rejection ও memory বেড়ে যাওয়ার সতর্কতা উল্লেখ করো।""",
        mist_en=r"""Memoizing impure functions (e.g. ones that read the current time or the DOM), using an object as the cache with arbitrary string keys like `'__proto__'`, or forgetting to forward `this`.""",
        mist_bn=r"""Impure function memoize করা (যেমন যেগুলো current time বা DOM পড়ে), arbitrary string key (যেমন `'__proto__'`) সহ object-কে cache হিসেবে ব্যবহার করা, অথবা `this` forward করতে ভুলে যাওয়া।""",
        code=r"""
            function memoize(fn, { getKey = (...args) => JSON.stringify(args), maxSize = Infinity } = {}) {
              const cache = new Map();

              return function memoized(...args) {
                const key = getKey(...args);

                if (cache.has(key)) {
                  const cached = cache.get(key);
                  cache.delete(key); // move to the "most recently used" end
                  cache.set(key, cached);
                  return cached;
                }

                const result = fn.apply(this, args);
                cache.set(key, result);
                if (cache.size > maxSize) {
                  cache.delete(cache.keys().next().value); // evict least recently used
                }
                return result;
              };
            }

            let calls = 0;
            const deliveryCharge = memoize((district, weightKg) => {
              calls++;
              return district === 'Dhaka' ? 60 + weightKg * 10 : 120 + weightKg * 20;
            }, { maxSize: 2 });

            console.log(deliveryCharge('Dhaka', 2), deliveryCharge('Dhaka', 2), calls); // 80 80 1

            const fib = memoize((n) => (n < 2 ? n : fib(n - 1) + fib(n - 2)));
            console.log(fib(50)); // 12586269025 — instant, O(n) calls
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Bonus: curry", label_bn="Bonus: curry", src=r"""
                const curry = (fn) =>
                  function curried(...args) {
                    return args.length >= fn.length
                      ? fn.apply(this, args)
                      : (...more) => curried.apply(this, [...args, ...more]);
                  };

                const add3 = curry((a, b, c) => a + b + c);
                console.log(add3(1)(2)(3), add3(1, 2)(3), add3(1)(2, 3)); // 6 6 6
            """),
        ],
        time="O(1) average per call + key-building cost", space="O(min(distinct inputs, maxSize))",
        follow=[
            ("How would you memoize an async function safely?", "একটা async function নিরাপদে কীভাবে memoize করবে?"),
            ("Why does `curry` rely on `fn.length`, and when does that break?", "`curry` কেন `fn.length`-এর উপর নির্ভর করে, আর কখন সেটা ভেঙে যায়?"),
        ],
        related=["js-004", "js-020"],
        refs=[R_CLOSURES, R_MAP, R_GETORINSERT_C],
    ),
    # ------------------------------------------------------------------ js-023
    Q(
        id="js-023", sub="Async/Await", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["async-await", "error-handling", "try-catch", "return-await"],
        ver="Version-independent concept (ES2017+ async/await)", vs=False, status="stable",
        q_en=r"""`getUserName` wraps the call in `try/catch` to fall back to `'Guest'`. What gets logged?""",
        q_bn=r"""`'Guest'`-এ fallback করার জন্য `getUserName` call-টাকে `try/catch`-এ রেখেছে। কী log হবে?""",
        code=r"""
            async function getUserName(id) {
              try {
                return fetchUser(id);
              } catch {
                return 'Guest';
              }
            }

            async function fetchUser(id) {
              throw new Error(`User ${id} not found`);
            }

            getUserName(7)
              .then((name) => console.log('resolved:', name))
              .catch((err) => console.log('rejected:', err.message));
        """,
        lang="javascript",
        output=r"""rejected: User 7 not found""",
        options=[
            ("`resolved: Guest`", "`resolved: Guest`"),
            ("`rejected: User 7 not found`", "`rejected: User 7 not found`"),
            ("`resolved: undefined`", "`resolved: undefined`"),
            ("An uncaught error is thrown synchronously when `getUserName(7)` is called", "`getUserName(7)` call করার সাথে সাথেই synchronously একটা uncaught error throw হবে"),
        ],
        correct=1,
        a_en=r"""
            `rejected: User 7 not found`. `return fetchUser(id)` returns the promise **without awaiting it**. The `try` block completes successfully the moment the (still pending) promise is returned, so the `catch` never runs. The rejection happens afterwards, and `getUserName`'s promise simply adopts it. The fix is `return await fetchUser(id);` — then the rejection is thrown inside the `try` and caught.
        """,
        a_bn=r"""
            `rejected: User 7 not found`। `return fetchUser(id)` promise-টাকে **await না করেই** return করে। (তখনও pending) promise return হওয়ার মুহূর্তেই `try` block সফলভাবে শেষ হয়ে যায়, তাই `catch` কখনো চলে না। Rejection ঘটে তার পরে, আর `getUserName`-এর promise সেটাই গ্রহণ করে। সমাধান হলো `return await fetchUser(id);` — তাহলে rejection `try`-এর ভেতরেই throw হয় এবং catch হয়।
        """,
        quick_en=r"""`rejected: User 7 not found`. `return fetchUser(id)` returns the pending promise without awaiting it, so the `try` block finishes before the rejection happens and the `catch` never runs; `return await fetchUser(id)` fixes it.""",
        quick_bn=r"""`rejected: User 7 not found`। `return fetchUser(id)` promise-টা await না করেই return করে, তাই rejection ঘটার আগেই `try` block শেষ হয়ে যায় আর `catch` কখনো চলে না; `return await fetchUser(id)` লিখলে ঠিক হয়।""",
        ex_en=r"""
            - **Option A** is what the author intended — and the reason this bug survives code review.
            - **Option D** is wrong because an async function never throws synchronously: any error inside it becomes a rejection of its returned promise.
            - **Option C** would need the callback to return nothing; here the rejection propagates instead.

            When does `return await` matter?
            - Inside `try/catch` (to catch) and `try/finally` (so `finally` runs *after* the operation, e.g. releasing a lock or closing a connection).
            - For better async stack traces — the current function stays in the trace.

            Outside `try` blocks, `return promise` and `return await promise` behave the same apart from timing. That's why ESLint deprecated its old `no-return-await` rule, and typescript-eslint's `return-await` rule requires `await` inside `try/catch` by default.
        """,
        ex_bn=r"""
            - **Option A** লেখকের উদ্দেশ্য ছিল — আর এজন্যই এই bug code review পার হয়ে যায়।
            - **Option D** ভুল, কারণ async function কখনো synchronously throw করে না: এর ভেতরের যেকোনো error return করা promise-এর rejection হয়ে যায়।
            - **Option C** হতে হলে callback-এর কিছু return না করা লাগত; এখানে বরং rejection উপরে চলে যায়।

            `return await` কখন গুরুত্বপূর্ণ?
            - `try/catch`-এর ভেতরে (catch করার জন্য) আর `try/finally`-এর ভেতরে (যাতে `finally` কাজ শেষ হওয়ার *পরে* চলে, যেমন lock ছাড়া বা connection বন্ধ করা)।
            - ভালো async stack trace-এর জন্য — current function-টা trace-এ থেকে যায়।

            `try` block-এর বাইরে `return promise` আর `return await promise` timing ছাড়া একই আচরণ করে। এজন্যই ESLint তার পুরনো `no-return-await` rule deprecate করেছে, আর typescript-eslint-এর `return-await` rule default-ভাবে `try/catch`-এর ভেতরে `await` বাধ্যতামূলক করে।
        """,
        tip_en=r"""Explain *when* the try block finishes (at the return of a pending promise) — that's the insight. Then mention the `finally` case (cleanup running too early), which shows production experience.""",
        tip_bn=r"""`try` block *কখন* শেষ হয় (pending promise return করার মুহূর্তে) — এটাই মূল অন্তর্দৃষ্টি, এটা ব্যাখ্যা করো। তারপর `finally`-র case (cleanup খুব আগে চলে যাওয়া) উল্লেখ করো — এতে production অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Believing `try/catch` around any expression that "involves" a promise will catch its rejection — only an awaited rejection is thrown at that point.""",
        mist_bn=r"""ভাবা যে promise "জড়িত" এমন যেকোনো expression `try/catch`-এ রাখলেই তার rejection ধরা পড়বে — আসলে শুধু await করা rejection-ই ওই জায়গায় throw হয়।""",
        follow=[
            ("Why might `finally` release a database connection too early without `await`?", "`await` না থাকলে `finally` কেন database connection খুব আগেই ছেড়ে দিতে পারে?"),
        ],
        related=["js-017", "js-019", "js-024"],
        refs=[R_ASYNC_FN, R_TRYCATCH],
    ),
    # ------------------------------------------------------------------ js-024
    Q(
        id="js-024", sub="Async/Await", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["async-await", "foreach", "promise-all", "debugging", "unhandled-rejection"],
        ver="Version-independent concept (ES2017+; `Promise.allSettled` ES2020)", vs=False, status="stable",
        q_en=r"""`saveAll` should save every order and return how many were saved. Instead it logs `Saved 0 orders`, returns `0`, and failed saves show up as unhandled promise rejections. Explain the root cause and fix it.""",
        q_bn=r"""`saveAll`-এর কাজ প্রতিটি order save করে কয়টা save হলো সেটা return করা। কিন্তু এটা `Saved 0 orders` log করে, `0` return করে, আর fail হওয়া save-গুলো unhandled promise rejection হিসেবে দেখা দেয়। Root cause ব্যাখ্যা করো এবং ঠিক করো।""",
        code=r"""
            async function saveAll(orders) {
              let saved = 0;

              orders.forEach(async (order) => {
                await db.save(order);
                saved++;
              });

              console.log(`Saved ${saved} orders`);
              return saved;
            }
        """,
        lang="javascript",
        a_en=r"""
            `forEach` ignores whatever its callback returns. An `async` callback returns a promise, so `forEach` starts every save, throws the promises away, and returns `undefined` immediately. Nothing awaits them: `console.log` and `return` run while all saves are still pending, so `saved` is `0`. And because those promises aren't connected to `saveAll`'s promise, a failed save can't be caught by the caller — it becomes an unhandled rejection.

            Fix it by making the promises visible:
            - **Sequential** (order matters or the DB can't take parallel writes): `for...of` with `await`.
            - **Parallel** (independent writes): `await Promise.all(orders.map((o) => db.save(o)))`, or `Promise.allSettled` if I want to report partial failures.

            For thousands of orders I'd add a concurrency limit instead of firing everything at once.
        """,
        a_bn=r"""
            `forEach` তার callback যা return করে সেটা উপেক্ষা করে। একটা `async` callback promise return করে, তাই `forEach` প্রতিটি save শুরু করে, promise-গুলো ফেলে দেয়, আর সাথে সাথে `undefined` return করে। কেউ এগুলোর জন্য await করে না: সব save তখনও pending থাকতেই `console.log` আর `return` চলে যায়, তাই `saved` হয় `0`। আর এই promise-গুলো `saveAll`-এর promise-এর সাথে যুক্ত না থাকায় কোনো save fail করলে caller সেটা catch করতে পারে না — সেটা unhandled rejection হয়ে যায়।

            সমাধান হলো promise-গুলোকে দৃশ্যমান করা:
            - **Sequential** (ক্রম গুরুত্বপূর্ণ, বা DB parallel write নিতে পারে না): `await` সহ `for...of`।
            - **Parallel** (স্বাধীন write): `await Promise.all(orders.map((o) => db.save(o)))`, অথবা আংশিক failure report করতে চাইলে `Promise.allSettled`।

            হাজার হাজার order হলে সব একসাথে না পাঠিয়ে concurrency limit যোগ করব।
        """,
        quick_en=r"""`forEach` ignores the promises its `async` callback returns, so nothing awaits the saves: the log and `return` run while `saved` is still `0`, and failed saves become unhandled rejections. Use `for...of` with `await` for sequential saves, or `await Promise.all(orders.map(...))` for parallel ones.""",
        quick_bn=r"""`forEach` তার `async` callback-এর return করা promise-গুলো ফেলে দেয়, তাই কেউ save-গুলোর জন্য অপেক্ষা করে না: `saved` তখনও `0` থাকতেই log আর `return` চলে যায়, আর fail করা save unhandled rejection হয়ে যায়। একটার পর একটা save করতে `for...of` + `await`, আর parallel-এ করতে `await Promise.all(orders.map(...))` ব্যবহার করো।""",
        ex_en=r"""
            - The same trap exists with `map` used without `Promise.all`, with `filter(async ...)` (an async predicate always returns a truthy promise, so nothing is filtered), and with `reduce(async ...)` unless you await the accumulator.
            - `for...of` + `await` is O(n) round-trips in series — simple but slow. `Promise.all` overlaps them but is fail-fast: the first rejection rejects the whole call while other saves keep running.
            - `Promise.allSettled` never rejects; I collect the failures and throw an `AggregateError` (or return a report) so the caller knows exactly which orders failed.
            - Database note: if the saves must be atomic (all or nothing), neither approach is enough — use a transaction or a bulk insert instead.
            - Linters help: typescript-eslint's `no-floating-promises` and `no-misused-promises` rules flag promises that are created but never awaited or handled.
        """,
        ex_bn=r"""
            - একই ফাঁদ আছে `Promise.all` ছাড়া `map`-এ, `filter(async ...)`-এ (async predicate সবসময় truthy promise return করে, তাই কিছুই filter হয় না), আর accumulator await না করলে `reduce(async ...)`-এ।
            - `for...of` + `await` মানে একটার পর একটা O(n) round-trip — সহজ কিন্তু ধীর। `Promise.all` এগুলো একসাথে চালায়, কিন্তু fail-fast: প্রথম rejection-এই পুরো call reject হয়, যদিও বাকি save-গুলো চলতে থাকে।
            - `Promise.allSettled` কখনো reject করে না; আমি failure-গুলো জড়ো করে একটা `AggregateError` throw করি (বা একটা report return করি), যাতে caller ঠিক জানে কোন order fail করেছে।
            - Database-এর কথা: save-গুলো যদি atomic হতে হয় (হয় সব, নয়তো কিছুই না), তাহলে এর কোনোটাই যথেষ্ট নয় — transaction বা bulk insert ব্যবহার করো।
            - Linter সাহায্য করে: typescript-eslint-এর `no-floating-promises` আর `no-misused-promises` rule এমন promise ধরে ফেলে যেগুলো তৈরি হয় কিন্তু কখনো await বা handle করা হয় না।
        """,
        tip_en=r"""Say the root cause in one sentence ("`forEach` doesn't await and drops the promises"), then offer both fixes and ask the interviewer whether order or speed matters — clarifying requirements scores points.""",
        tip_bn=r"""Root cause এক বাক্যে বলো ("`forEach` await করে না, promise-গুলো ফেলে দেয়"), তারপর দুটো সমাধানই দাও এবং interviewer-কে জিজ্ঞেস করো ক্রম গুরুত্বপূর্ণ নাকি গতি — requirement পরিষ্কার করে নিলে নম্বর বাড়ে।""",
        mist_en=r""""Fixing" it by adding `await` before `orders.forEach(...)` — `forEach` returns `undefined`, so there is nothing to await.""",
        mist_bn=r"""`orders.forEach(...)`-এর আগে `await` বসিয়ে "fix" করা — `forEach` `undefined` return করে, তাই await করার মতো কিছুই নেই।""",
        extra=[
            dict(lang="javascript", label_en="Fixed: sequential and parallel versions", label_bn="সংশোধিত: sequential আর parallel version", src=r"""
                // Sequential: one at a time, stops at the first failure
                async function saveAllSequential(orders) {
                  for (const order of orders) {
                    await db.save(order);
                  }
                  return orders.length;
                }

                // Parallel: all at once, report every failure
                async function saveAllParallel(orders) {
                  const results = await Promise.allSettled(orders.map((order) => db.save(order)));
                  const failed = results.filter((r) => r.status === 'rejected');
                  if (failed.length > 0) {
                    throw new AggregateError(
                      failed.map((r) => r.reason),
                      `${failed.length} of ${orders.length} orders failed to save`,
                    );
                  }
                  return results.length;
                }
            """),
        ],
        follow=[
            ("How would you save 10,000 orders with at most 5 in flight?", "একসাথে সর্বোচ্চ ৫টা চালু রেখে ১০,০০০ order কীভাবে save করবে?"),
            ("What does `filter` do with an async predicate?", "Async predicate দিলে `filter` কী করে?"),
        ],
        related=["js-023", "js-021", "js-037"],
        refs=[R_FOREACH, R_FOROF, R_ASYNC_FN],
    ),
    # ------------------------------------------------------------------ js-025
    Q(
        id="js-025", sub="Execution Context & Call Stack", diff="medium", type="conceptual",
        prio="high", market="both", mins=6,
        tags=["execution-context", "call-stack", "lexical-environment", "scope-chain", "closures"],
        ver="Version-independent concept (ECMAScript 2026 spec terminology)", vs=False, status="stable",
        q_en=r"""What happens inside the engine when a function is called? Explain execution contexts, the call stack and lexical environments, and how they explain scope and closures.""",
        q_bn=r"""একটা function call হলে engine-এর ভেতরে কী ঘটে? Execution context, call stack আর lexical environment ব্যাখ্যা করো, আর এগুলো দিয়ে scope ও closure কীভাবে বোঝা যায় সেটা বলো।""",
        a_en=r"""
            Every time code runs, the engine creates an **execution context**: one global context for the script/module, and a new one for **each function call**. The contexts are managed by the **call stack** (LIFO): calling a function pushes its context, returning pops it. JavaScript runs one context at a time — the one on top.

            Each context has a **lexical environment**: an environment record holding its variables (parameters, `let`/`const`, function declarations, and — for function contexts — `var`) plus a reference to the **outer** environment. Setting up the record before the code runs is what we call hoisting. Variable lookup walks this chain of outer references — the **scope chain** — until it finds the name or throws a `ReferenceError`.

            The outer reference is taken from where the function was **defined**, not where it's called (lexical scoping). A function object stores that environment, so if the function outlives its parent call, the parent's environment stays alive — that's a closure. The context also determines `this`.
        """,
        a_bn=r"""
            Code চলার সময় প্রতিবার engine একটা **execution context** তৈরি করে: script/module-এর জন্য একটা global context, আর **প্রতিটি function call**-এর জন্য নতুন একটা। এই context-গুলো সামলায় **call stack** (LIFO): function call হলে তার context push হয়, return করলে pop হয়। JavaScript একবারে একটাই context চালায় — যেটা সবার উপরে।

            প্রতিটি context-এর একটা **lexical environment** থাকে: একটা environment record যেখানে তার variable-গুলো থাকে (parameter, `let`/`const`, function declaration, আর function context হলে `var`-ও) আর থাকে **outer** environment-এর একটা reference। Code চলার আগেই এই record তৈরি হয়ে যাওয়াটাকেই আমরা hoisting বলি। Variable খোঁজার সময় এই outer reference-এর chain — **scope chain** — ধরে উপরে যাওয়া হয়, নাম পাওয়া পর্যন্ত, না পেলে `ReferenceError`।

            Outer reference নেওয়া হয় function যেখানে **define** করা হয়েছে সেখান থেকে, যেখানে call হচ্ছে সেখান থেকে নয় (lexical scoping)। Function object ওই environment-টা সংরক্ষণ করে, তাই function যদি তার parent call-এর চেয়ে বেশি দিন বাঁচে, parent-এর environment-ও বেঁচে থাকে — এটাই closure। `this`-ও context থেকেই ঠিক হয়।
        """,
        quick_en=r"""Each function call creates an execution context, pushed onto the call stack (LIFO) and popped on return. Its lexical environment holds its variables plus a link to the outer environment where the function was defined; lookups walk that scope chain, and a function that outlives its parent keeps that environment alive (a closure).""",
        quick_bn=r"""প্রতিটা function call একটা execution context তৈরি করে, যেটা call stack-এ (LIFO) push হয় আর return করলে pop হয়। তার lexical environment-এ থাকে নিজের variable আর function যেখানে define হয়েছে সেই outer environment-এর reference; variable খোঁজা হয় এই scope chain ধরে, আর function তার parent call-এর পরেও বেঁচে থাকলে parent-এর environment-ও closure হিসেবে বেঁচে থাকে।""",
        ex_en=r"""
            - **Two phases per context:** creation (environment record set up: function declarations get their value, `var` → `undefined`, `let`/`const`/`class` stay uninitialised → temporal dead zone) and execution (code runs line by line).
            - **Block scopes:** `{ }`, `for`, `if` blocks with `let`/`const` get their own small lexical environments inside the function's context.
            - **Stack overflow:** unbounded recursion keeps pushing contexts until the engine throws `RangeError: Maximum call stack size exceeded`. Fix with a base case, iteration, or chunking work.
            - **Async code:** when an async function hits `await`, its context is suspended and popped; the continuation is pushed again later from the microtask queue. That's why the call stack is empty when timers and promise callbacks run, and why plain stack traces across async boundaries are limited (engines add "async stack traces").
            - **Debugging link:** the "Call Stack" and "Scope" panels in DevTools show exactly these structures — local, closure and global scopes.
        """,
        ex_bn=r"""
            - **প্রতিটি context-এর দুটো phase:** creation (environment record তৈরি: function declaration তার value পায়, `var` → `undefined`, `let`/`const`/`class` uninitialised থাকে → temporal dead zone) আর execution (code line ধরে ধরে চলে)।
            - **Block scope:** `let`/`const` সহ `{ }`, `for`, `if` block function-এর context-এর ভেতরে নিজেদের ছোট lexical environment পায়।
            - **Stack overflow:** সীমাহীন recursion context push করতেই থাকে, শেষে engine `RangeError: Maximum call stack size exceeded` throw করে। Base case, iteration বা কাজকে টুকরো করে এটা ঠিক করো।
            - **Async code:** async function `await`-এ পৌঁছালে তার context suspend হয়ে pop হয়; পরে microtask queue থেকে continuation আবার push হয়। এজন্যই timer বা promise callback চলার সময় call stack খালি থাকে, আর async boundary পেরিয়ে সাধারণ stack trace সীমিত হয় (engine "async stack trace" যোগ করে)।
            - **Debugging-এর সংযোগ:** DevTools-এর "Call Stack" আর "Scope" panel ঠিক এই structure-গুলোই দেখায় — local, closure আর global scope।
        """,
        tip_en=r"""Use a tiny example and literally "push" and "pop" contexts while you talk. Then connect the outer reference to closures and the creation phase to hoisting — one model explains three topics.""",
        tip_bn=r"""ছোট একটা উদাহরণ নিয়ে কথা বলার সময় context-গুলো আক্ষরিক অর্থে "push" আর "pop" করে দেখাও। তারপর outer reference-কে closure-এর সাথে আর creation phase-কে hoisting-এর সাথে যুক্ত করো — একটা model দিয়েই তিনটা topic বোঝানো যায়।""",
        mist_en=r"""Saying scope is determined by where a function is *called* (that's dynamic scoping, which JavaScript doesn't use — only `this` is call-site dependent).""",
        mist_bn=r"""বলা যে function যেখানে *call* হয় সেখান থেকে scope ঠিক হয় (এটা dynamic scoping, JavaScript তা ব্যবহার করে না — শুধু `this` call site-এর উপর নির্ভর করে)।""",
        code=r"""
            const rate = 0.05; // global environment record

            function makeTaxCalculator(country) {
              const rate = country === 'BD' ? 0.15 : 0.1; // makeTaxCalculator's environment
              return function calc(amount) {
                return amount * rate; // found via calc's outer reference, not the global `rate`
              };
            }

            const bdTax = makeTaxCalculator('BD'); // context pushed, then popped — environment survives
            console.log(bdTax(1000)); // 150

            function recurse(n) {
              return recurse(n + 1); // no base case
            }
            // recurse(0); // RangeError: Maximum call stack size exceeded
        """,
        lang="javascript",
        follow=[
            ("Why is the call stack empty when a `setTimeout` callback runs?", "`setTimeout` callback চলার সময় call stack খালি থাকে কেন?"),
            ("What is the difference between the VariableEnvironment and the LexicalEnvironment?", "VariableEnvironment আর LexicalEnvironment-এর পার্থক্য কী?"),
        ],
        related=["js-002", "js-004", "js-016"],
        refs=[R_EXEC_MODEL, R_CLOSURES],
    ),
    # ------------------------------------------------------------------ js-026
    Q(
        id="js-026", sub="Modules (ESM vs CommonJS)", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["esm", "commonjs", "modules", "node", "require-esm"],
        ver="ES2015+ modules; ES2025 import attributes; Node.js 26 LTS / 24 (`require(esm)` since 22.12 / 20.19)", vs=True, status="stable",
        q_en=r"""Compare ES modules (`import`/`export`) with CommonJS (`require`/`module.exports`). What are the practical differences in Node.js today?""",
        q_bn=r"""ES module (`import`/`export`) আর CommonJS (`require`/`module.exports`) তুলনা করো। আজকের Node.js-এ বাস্তবে পার্থক্যগুলো কী?""",
        a_en=r"""
            ES modules are the standard JavaScript module system; CommonJS is Node's original one.

            - **Static vs dynamic:** `import`/`export` are static declarations analysed before the code runs, which enables tree-shaking and early errors. `require()` is an ordinary function call evaluated at runtime.
            - **Bindings:** ESM imports are **live, read-only bindings** to the exporter's variables. CommonJS copies whatever is on `module.exports` when you destructure it.
            - **Loading:** ESM loading is asynchronous-capable and supports **top-level `await`**; `require` is synchronous.
            - **Defaults:** ESM is always strict mode, top-level `this` is `undefined`, and there's no `__dirname`/`require` — use `import.meta.dirname`, `import.meta.filename`, `import.meta.url`. Relative imports need the file extension (`./utils.js`).
            - **In Node:** a file is ESM if it's `.mjs` or the nearest `package.json` has `"type": "module"`; `.cjs` is always CommonJS. ESM can import CJS. CJS can `require()` a synchronous ES module by default since Node 22.12 / 20.19 (it throws if the module uses top-level `await`); otherwise use dynamic `import()`.

            For new projects I use ESM everywhere.
        """,
        a_bn=r"""
            ES module হলো JavaScript-এর standard module system; CommonJS হলো Node-এর মূল/পুরনো system।

            - **Static বনাম dynamic:** `import`/`export` হলো static declaration, code চলার আগেই analyse হয় — এতে tree-shaking আর আগেভাগে error ধরা সম্ভব হয়। `require()` একটা সাধারণ function call, runtime-এ evaluate হয়।
            - **Binding:** ESM import হলো exporter-এর variable-এর সাথে **live, read-only binding**। CommonJS-এ destructure করলে সেই মুহূর্তে `module.exports`-এ যা আছে তার copy পাও।
            - **Loading:** ESM loading asynchronous হতে পারে এবং **top-level `await`** support করে; `require` synchronous।
            - **Default আচরণ:** ESM সবসময় strict mode, top-level `this` হলো `undefined`, আর `__dirname`/`require` নেই — `import.meta.dirname`, `import.meta.filename`, `import.meta.url` ব্যবহার করো। Relative import-এ file extension লাগে (`./utils.js`)।
            - **Node-এ:** file `.mjs` হলে বা সবচেয়ে কাছের `package.json`-এ `"type": "module"` থাকলে সেটা ESM; `.cjs` সবসময় CommonJS। ESM, CJS import করতে পারে। Node 22.12 / 20.19 থেকে CJS default-ভাবেই synchronous ES module `require()` করতে পারে (module-এ top-level `await` থাকলে throw করে); নাহলে dynamic `import()` ব্যবহার করো।

            নতুন project-এ আমি সব জায়গায় ESM ব্যবহার করি।
        """,
        quick_en=r"""ES modules are the standard: static `import`/`export`, live read-only bindings, top-level `await`, strict mode, no `__dirname`. CommonJS `require()` is a synchronous runtime call that returns whatever is on `module.exports`; in Node, ESM can import CJS, and CJS can `require()` synchronous ESM since 22.12 / 20.19.""",
        quick_bn=r"""ES module হলো standard: static `import`/`export`, live read-only binding, top-level `await`, strict mode, আর `__dirname` নেই। CommonJS-এর `require()` runtime-এ চলা একটা synchronous call, যেটা `module.exports`-এ যা আছে তা-ই দেয়; Node-এ ESM CJS import করতে পারে, আর 22.12 / 20.19 থেকে CJS synchronous ESM-কে `require()` করতে পারে।""",
        ex_en=r"""
            - **Live bindings demo:** in the example, ESM prints `1` after `increment()` because `count` is a live view of the exporter's variable; CommonJS prints `0` because destructuring copied the number.
            - **Circular dependencies:** CommonJS gives you a *partially filled* `module.exports`; ESM gives live bindings, and reading a `let`/`const`/`class` export before it's initialised throws a `ReferenceError` (TDZ) — both mean "restructure the code".
            - **JSON:** `import data from './config.json' with { type: 'json' }` uses ES2025 import attributes; in CommonJS you just `require('./config.json')`.
            - **Interop details:** importing a CJS module from ESM gives `module.exports` as the default export (named exports only when Node can detect them statically).
            - **Library authors:** shipping both formats can cause the "dual package hazard" (two copies of the same package with separate state). Prefer ESM-only now that `require(esm)` works, or point both `exports` conditions to one implementation.
            - Browsers only understand ESM (`<script type="module">`); bundlers convert as needed.
        """,
        ex_bn=r"""
            - **Live binding-এর demo:** উদাহরণে `increment()`-এর পর ESM `1` print করে, কারণ `count` হলো exporter-এর variable-এর live view; CommonJS `0` print করে, কারণ destructure করার সময় number-টা copy হয়ে গেছে।
            - **Circular dependency:** CommonJS দেয় *আংশিক ভরা* `module.exports`; ESM দেয় live binding, আর `let`/`const`/`class` export initialise হওয়ার আগে পড়লে `ReferenceError` (TDZ) throw করে — দুটোরই মানে "code-এর গঠন বদলাও"।
            - **JSON:** `import data from './config.json' with { type: 'json' }` — এটা ES2025-এর import attributes; CommonJS-এ শুধু `require('./config.json')`।
            - **Interop-এর খুঁটিনাটি:** ESM থেকে CJS module import করলে `module.exports` default export হিসেবে আসে (Node static-ভাবে detect করতে পারলে তবেই named export)।
            - **Library লেখকদের জন্য:** দুটো format একসাথে ship করলে "dual package hazard" হতে পারে (একই package-এর দুটো copy, আলাদা state সহ)। এখন যেহেতু `require(esm)` কাজ করে, ESM-only ship করাই ভালো, নয়তো `exports`-এর দুটো condition-কেই একটা implementation-এ point করাও।
            - Browser শুধু ESM বোঝে (`<script type="module">`); দরকার হলে bundler convert করে নেয়।
        """,
        tip_en=r"""Lead with static vs dynamic and live bindings (the conceptual differences), then the Node-specific rules (`type`, extensions, `import.meta.dirname`, `require(esm)`). Mentioning the current `require(esm)` status shows you're up to date.""",
        tip_bn=r"""শুরু করো static বনাম dynamic আর live binding দিয়ে (ধারণাগত পার্থক্য), তারপর Node-এর নিয়মগুলো (`type`, extension, `import.meta.dirname`, `require(esm)`)। `require(esm)`-এর বর্তমান অবস্থা বললে বোঝা যায় তুমি আপডেটেড।""",
        mist_en=r"""Saying CommonJS can never load ES modules (outdated since Node 22.12 / 20.19), or forgetting the `.js` extension in ESM relative imports in Node.""",
        mist_bn=r"""বলা যে CommonJS কখনোই ES module load করতে পারে না (Node 22.12 / 20.19 থেকে এটা পুরনো তথ্য), অথবা Node-এ ESM-এর relative import-এ `.js` extension দিতে ভুলে যাওয়া।""",
        code=r"""
            // counter.mjs (ESM)
            export let count = 0;
            export function increment() {
              count++;
            }

            // main.mjs
            import { count, increment } from './counter.mjs';
            increment();
            console.log(count); // 1 — live binding
            console.log(import.meta.dirname); // folder path; no __dirname in ESM

            // counter.cjs (CommonJS)
            let count = 0;
            module.exports = { count, increment() { count++; } };

            // main.cjs
            const { count, increment } = require('./counter.cjs');
            increment();
            console.log(count); // 0 — copied value
            const esm = require('./counter.mjs'); // works in Node 22.12+ / 20.19+ (sync ESM only)
        """,
        lang="javascript",
        follow=[
            ("How do you get `__dirname` in an ES module?", "ES module-এ `__dirname` কীভাবে পাবে?"),
            ("What is the dual package hazard?", "Dual package hazard কী?"),
        ],
        related=["js-025"],
        refs=[R_MODULES, R_NODE_ESM, R_NODE_CJS],
    ),
    # ------------------------------------------------------------------ js-027
    Q(
        id="js-027", sub="Modern JavaScript (ES2025/ES2026)", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["iterator-helpers", "generators", "lazy-evaluation", "es2025"],
        ver="ES2025 iterator helpers (Baseline newly available since 2025-03; Node.js 22+)", vs=True, status="stable",
        q_en=r"""This code uses ES2025 iterator helpers on an infinite generator. What happens?""",
        q_bn=r"""এই code একটা অসীম generator-এর উপর ES2025-এর iterator helper ব্যবহার করছে। কী ঘটবে?""",
        code=r"""
            function* naturals() {
              let n = 1;
              while (true) yield n++;
            }

            const result = naturals()
              .filter((n) => n % 2 === 0)
              .map((n) => n * n)
              .take(3)
              .toArray();

            console.log(result);
        """,
        lang="javascript",
        output=r"""[ 4, 16, 36 ]""",
        options=[
            ("It logs `[4, 16, 36]`", "`[4, 16, 36]` log হবে"),
            ("It hangs forever — `filter` tries to consume the whole infinite generator first", "চিরকাল আটকে থাকবে — `filter` আগে পুরো অসীম generator শেষ করতে চাইবে"),
            ("It logs `[1, 4, 9]`", "`[1, 4, 9]` log হবে"),
            ("It throws `TypeError: naturals(...).filter is not a function`, because only arrays have `filter`", "`TypeError: naturals(...).filter is not a function` throw হবে, কারণ শুধু array-র `filter` আছে"),
        ],
        correct=0,
        a_en=r"""
            It logs `[4, 16, 36]`. Iterator helpers are **lazy**: nothing runs until `toArray()` pulls values. Each pull flows through the chain one value at a time — `filter` keeps 2, 4, 6…, `map` squares them, and `take(3)` stops after three values and closes the generator. Generator objects inherit from `Iterator.prototype`, so they have these methods.
        """,
        a_bn=r"""
            `[4, 16, 36]` log হবে। Iterator helper **lazy**: `toArray()` value টেনে না নেওয়া পর্যন্ত কিছুই চলে না। প্রতিটি টান chain-এর মধ্য দিয়ে একবারে একটা value নিয়ে যায় — `filter` রাখে 2, 4, 6…, `map` সেগুলোর বর্গ করে, আর `take(3)` তিনটা value পেলেই থেমে generator বন্ধ করে দেয়। Generator object `Iterator.prototype` থেকে inherit করে, তাই এই method-গুলো তাদের আছে।
        """,
        quick_en=r"""It logs `[4, 16, 36]`. Iterator helpers are lazy: values are pulled one at a time through `filter`, `map` and `take(3)`, which stops after three values and closes the generator, so the infinite generator never has to finish.""",
        quick_bn=r"""এটা `[4, 16, 36]` log করে। Iterator helper lazy: value একটা একটা করে `filter`, `map` আর `take(3)` দিয়ে টানা হয়, আর `take(3)` তিনটা value পেয়েই থেমে generator বন্ধ করে দেয়, তাই infinite generator-কে কখনো শেষ হতে হয় না।""",
        ex_en=r"""
            - **Option B** is how *array* methods behave: `[...].filter()` builds a full new array before `map` runs. With an infinite source that would never finish — which is exactly what iterator helpers avoid.
            - **Option C** assumes `take` runs before `filter`; the chain order is respected.
            - **Option D** was true in runtimes before ES2025. Iterator helpers are Baseline newly available (since March 2025: Chrome 122, Firefox 131, Safari 18.4) and in Node 22+. For older targets, use a polyfill (core-js) or convert with `Array.from` first.

            Available helpers: `map`, `filter`, `take`, `drop`, `flatMap`, `reduce`, `toArray`, `forEach`, `some`, `every`, `find`, plus `Iterator.from()` to wrap any iterator. ES2026 adds `Iterator.concat()`.

            Practical use: processing large or streaming data (paginated results, log lines, `Map.prototype.entries()`) without allocating intermediate arrays. Related ES2025 additions: Set methods like `a.union(b)`, `a.intersection(b)`, `a.difference(b)`, `a.isSubsetOf(b)`.
        """,
        ex_bn=r"""
            - **Option B** হলো *array* method-এর আচরণ: `[...].filter()` পুরো নতুন array বানিয়ে ফেলে, তারপর `map` চলে। অসীম source হলে সেটা কখনো শেষ হতো না — iterator helper ঠিক এটাই এড়ায়।
            - **Option C** ধরে নেয় `take` `filter`-এর আগে চলে; আসলে chain-এর ক্রম মেনেই চলে।
            - **Option D** ES2025-এর আগের runtime-এ সত্য ছিল। Iterator helper এখন Baseline newly available (March 2025 থেকে: Chrome 122, Firefox 131, Safari 18.4) এবং Node 22+-এ আছে। পুরনো target-এর জন্য polyfill (core-js) ব্যবহার করো, বা আগে `Array.from` দিয়ে convert করো।

            পাওয়া যায়: `map`, `filter`, `take`, `drop`, `flatMap`, `reduce`, `toArray`, `forEach`, `some`, `every`, `find`, আর যেকোনো iterator wrap করতে `Iterator.from()`। ES2026 যোগ করেছে `Iterator.concat()`।

            বাস্তব ব্যবহার: বড় বা streaming data (paginated result, log line, `Map.prototype.entries()`) intermediate array তৈরি না করেই process করা। ES2025-এর সম্পর্কিত সংযোজন: Set method যেমন `a.union(b)`, `a.intersection(b)`, `a.difference(b)`, `a.isSubsetOf(b)`।
        """,
        tip_en=r"""Contrast "lazy pull-based iterators" with "eager arrays" in one sentence, then give the Baseline/Node support status. Showing you know *when* the feature is safe to use matters as much as knowing it exists.""",
        tip_bn=r"""এক বাক্যে "lazy, pull-based iterator" আর "eager array"-এর পার্থক্য বলো, তারপর Baseline/Node support-এর অবস্থা জানাও। Feature আছে জানার মতোই গুরুত্বপূর্ণ হলো *কখন* সেটা নিরাপদে ব্যবহার করা যায় তা জানা।""",
        follow=[
            ("How would you implement `take` yourself with a generator function?", "Generator function দিয়ে নিজে `take` কীভাবে implement করবে?"),
        ],
        related=["js-035"],
        refs=[R_ITERATOR, R_ITER_TAKE],
    ),
    # ------------------------------------------------------------------ js-028
    Q(
        id="js-028", sub="Classes & Private Fields", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["classes", "private-fields", "encapsulation", "es2022", "brand-check"],
        ver="ES2022 (private fields/methods, `#x in obj` brand checks); Baseline widely available", vs=True, status="stable",
        q_en=r"""What does this `Wallet` class example log?""",
        q_bn=r"""এই `Wallet` class-এর উদাহরণ কী log করবে?""",
        code=r"""
            class Wallet {
              #balance = 0;
              static #count = 0;

              constructor(owner) {
                this.owner = owner;
                Wallet.#count++;
              }

              deposit(amount) {
                this.#balance += amount;
                return this;
              }

              get balance() {
                return this.#balance;
              }

              static isWallet(obj) {
                return #balance in obj;
              }

              static get count() {
                return Wallet.#count;
              }
            }

            const w = new Wallet('Nadia').deposit(500).deposit(250);
            console.log(w.balance, w['#balance'], Object.keys(w), Wallet.isWallet({ balance: 750 }), Wallet.count);
        """,
        lang="javascript",
        output=r"""750 undefined [ 'owner' ] false 1""",
        options=[
            ("`750 undefined ['owner'] false 1`", "`750 undefined ['owner'] false 1`"),
            ("`750 750 ['owner', '#balance'] false 1`", "`750 750 ['owner', '#balance'] false 1`"),
            ("`750 undefined ['owner'] true 1`", "`750 undefined ['owner'] true 1`"),
            ("A `SyntaxError`, because `#balance in obj` is not valid JavaScript", "একটা `SyntaxError`, কারণ `#balance in obj` valid JavaScript নয়"),
        ],
        correct=0,
        a_en=r"""
            `750 undefined ['owner'] false 1`. `#balance` is a real **private field** (ES2022), not a property with a funny name: `w['#balance']` looks up a normal string key and finds nothing, and `Object.keys` (also `JSON.stringify`, spread, `structuredClone`) can't see it. `#balance in obj` is a valid ES2022 **brand check** that returns `true` only for objects that were actually constructed by `Wallet`. The static private `#count` was incremented once.
        """,
        a_bn=r"""
            `750 undefined ['owner'] false 1`। `#balance` একটা আসল **private field** (ES2022), অদ্ভুত নামের property নয়: `w['#balance']` সাধারণ string key খোঁজে এবং কিছুই পায় না, আর `Object.keys` (সাথে `JSON.stringify`, spread, `structuredClone`-ও) এটা দেখতে পায় না। `#balance in obj` হলো valid ES2022 **brand check**, যেটা কেবল সেই object-এর জন্য `true` দেয় যেটা সত্যিই `Wallet` দিয়ে construct হয়েছে। Static private `#count` একবার বেড়েছে।
        """,
        quick_en=r"""`750 undefined ['owner'] false 1`. `#balance` is a real private field, so `w['#balance']` and `Object.keys` can't see it, and `#balance in obj` is a valid brand check that is `true` only for objects actually created by `Wallet`.""",
        quick_bn=r"""`750 undefined ['owner'] false 1`। `#balance` সত্যিকারের private field, তাই `w['#balance']` বা `Object.keys` এটা দেখতে পায় না; আর `#balance in obj` একটা valid brand check, যেটা শুধু `Wallet` দিয়ে তৈরি object-এর জন্য `true` হয়।""",
        ex_en=r"""
            - **Option C** is the duck-typing trap: `{ balance: 750 }` *looks* like a wallet, but it has no `#balance` slot, so the brand check is `false`.
            - **Option B** treats `#balance` like a string key — it isn't one; the `#` is part of the syntax.
            - **Option D:** ergonomic brand checks (`#x in obj`) are standard since ES2022.

            Why private fields matter:
            - **Hard privacy** enforced by the engine, unlike the `_balance` naming convention or TypeScript's `private` (compile-time only; the property is still visible at runtime).
            - Reading `obj.#balance` on an object without that field throws a `TypeError` — the `in` check lets you test safely first.
            - You also get private methods (`#validate()`), private getters and `static` blocks for one-time class setup.
            - Trade-offs: private fields don't work through a `Proxy` wrapping the instance, and only code inside the declaring class body can access them — a subclass can't read the parent's `#balance`, so expose what subclasses need through methods or getters.
        """,
        ex_bn=r"""
            - **Option C** হলো duck-typing-এর ফাঁদ: `{ balance: 750 }` দেখতে wallet-এর মতো, কিন্তু এতে `#balance` slot নেই, তাই brand check `false`।
            - **Option B** `#balance`-কে string key-এর মতো ধরে নেয় — এটা তা নয়; `#` syntax-এরই অংশ।
            - **Option D:** ergonomic brand check (`#x in obj`) ES2022 থেকেই standard।

            Private field কেন গুরুত্বপূর্ণ:
            - Engine নিজে **hard privacy** নিশ্চিত করে — `_balance` নামকরণের রীতি বা TypeScript-এর `private` (শুধু compile-time-এ; runtime-এ property দেখা যায়) থেকে আলাদা।
            - যে object-এ field নেই তাতে `obj.#balance` পড়লে `TypeError` throw হয় — `in` check দিয়ে আগে নিরাপদে পরীক্ষা করা যায়।
            - এছাড়া private method (`#validate()`), private getter আর এককালীন class setup-এর জন্য `static` block পাওয়া যায়।
            - Trade-off: instance-কে `Proxy` দিয়ে wrap করলে private field কাজ করে না, আর শুধু যে class body-তে declare করা সেখানকার code-ই এগুলো access করতে পারে — subclass parent-এর `#balance` পড়তে পারে না, তাই subclass-এর যা দরকার তা method বা getter দিয়ে দাও।
        """,
        tip_en=r"""Contrast three levels of "private": `_convention`, TypeScript `private`, and `#private`. Mentioning the `#x in obj` brand check and the `Proxy` limitation shows you've used them for real.""",
        tip_bn=r""""Private"-এর তিনটা স্তর তুলনা করো: `_convention`, TypeScript `private`, আর `#private`। `#x in obj` brand check আর `Proxy`-এর সীমাবদ্ধতার কথা বললে বোঝা যায় তুমি এগুলো বাস্তবে ব্যবহার করেছ।""",
        follow=[
            ("How is a class method different from an arrow-function class field?", "Class method আর arrow-function class field-এর পার্থক্য কী?"),
        ],
        related=["js-018"],
        refs=[R_PRIVATE, R_CLASSES],
    ),
]

if __name__ == "__main__":
    save("javascript", "b4", QUESTIONS)
