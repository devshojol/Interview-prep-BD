import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
API = "https://developer.mozilla.org/en-US/docs/Web/API"
R_THIS = ("MDN — this", f"{MDN}/Reference/Operators/this")
R_BIND = ("MDN — Function.prototype.bind()", f"{MDN}/Reference/Global_Objects/Function/bind")
R_CALL = ("MDN — Function.prototype.call()", f"{MDN}/Reference/Global_Objects/Function/call")
R_EXEC_MODEL = ("MDN — JavaScript execution model", f"{MDN}/Reference/Execution_model")
R_MICROTASK = ("MDN — Using microtasks with queueMicrotask()", f"{API}/HTML_DOM_API/Microtask_guide")
R_AWAIT = ("MDN — await", f"{MDN}/Reference/Operators/await")
R_ASYNC_FN = ("MDN — async function", f"{MDN}/Reference/Statements/async_function")
R_PROTO_CHAIN = ("MDN — Inheritance and the prototype chain", f"{MDN}/Guide/Inheritance_and_the_prototype_chain")
R_HASOWN = ("MDN — Object.hasOwn()", f"{MDN}/Reference/Global_Objects/Object/hasOwn")
R_CAUSE = ("MDN — Error: cause", f"{MDN}/Reference/Global_Objects/Error/cause")
R_AGG = ("MDN — AggregateError", f"{MDN}/Reference/Global_Objects/AggregateError")
R_ISERROR = ("MDN — Error.isError()", f"{MDN}/Reference/Global_Objects/Error/isError")
R_DEBOUNCE = ("MDN — Debounce (glossary)", "https://developer.mozilla.org/en-US/docs/Glossary/Debounce")
R_THROTTLE = ("MDN — Throttle (glossary)", "https://developer.mozilla.org/en-US/docs/Glossary/Throttle")
R_PALL = ("MDN — Promise.all()", f"{MDN}/Reference/Global_Objects/Promise/all")
R_PROMISE = ("MDN — Promise", f"{MDN}/Reference/Global_Objects/Promise")

QUESTIONS = [
    # ------------------------------------------------------------------ js-015
    Q(
        id="js-015", sub="`this` Keyword", diff="medium", type="output",
        prio="high", market="both", mins=5,
        tags=["this", "call-apply-bind", "arrow-functions", "method-extraction"],
        ver="Version-independent concept (ES2020+ for `?.`; ES module = strict mode)", vs=False, status="stable",
        q_en=r"""This file runs as an **ES module** (strict mode). What does it print? Explain how `this` is decided for each call.""",
        q_bn=r"""এই file-টা **ES module** (strict mode) হিসেবে চলে। এটা কী print করবে? প্রতিটি call-এ `this` কীভাবে ঠিক হয়, ব্যাখ্যা করো।""",
        code=r"""
            const user = {
              name: 'Rahim',
              regular() {
                return this?.name;
              },
              arrow: () => this?.name,
              delayed() {
                return [1].map(() => this.name)[0];
              },
            };

            const extracted = user.regular;
            const other = { name: 'Karim' };

            console.log(user.regular());
            console.log(extracted());
            console.log(user.arrow());
            console.log(user.delayed());
            console.log(user.regular.call(other));
            console.log(user.regular.bind(other).call(user));
        """,
        lang="javascript",
        output=r"""
            Rahim
            undefined
            undefined
            Rahim
            Karim
            Karim
        """,
        a_en=r"""
            For a regular function, `this` is decided **at call time** by how it is called; an arrow function has no `this` and uses the one from where it was written.

            1. `user.regular()` — method call, `this` is `user` → `Rahim`.
            2. `extracted()` — the function was copied off the object and called plainly. No receiver, strict mode → `this` is `undefined` → `undefined`.
            3. `user.arrow()` — the arrow was created at module top level, where `this` is `undefined` → `undefined`. Being "inside" the object literal doesn't matter.
            4. `user.delayed()` — the arrow callback inherits `delayed`'s `this`, which is `user` → `Rahim`.
            5. `.call(other)` — explicit binding → `Karim`.
            6. `bind(other)` creates a permanently bound function; a later `.call(user)` can't override it → `Karim`.
        """,
        a_bn=r"""
            Regular function-এর `this` ঠিক হয় **call করার সময়**, কীভাবে call করা হলো তা দিয়ে; arrow function-এর নিজের `this` নেই, সে যেখানে লেখা হয়েছে সেখানকার `this` ব্যবহার করে।

            1. `user.regular()` — method call, `this` হলো `user` → `Rahim`।
            2. `extracted()` — function-টা object থেকে আলাদা করে সাধারণভাবে call করা হয়েছে। কোনো receiver নেই, strict mode → `this` হলো `undefined` → `undefined`।
            3. `user.arrow()` — arrow-টা তৈরি হয়েছে module-এর top level-এ, যেখানে `this` হলো `undefined` → `undefined`। Object literal-এর "ভেতরে" থাকাটা কোনো ব্যাপার নয়।
            4. `user.delayed()` — arrow callback `delayed`-এর `this` পায়, যেটা `user` → `Rahim`।
            5. `.call(other)` — explicit binding → `Karim`।
            6. `bind(other)` একটা স্থায়ীভাবে bound function তৈরি করে; পরে `.call(user)` দিয়েও সেটা বদলানো যায় না → `Karim`।
        """,
        quick_en=r"""`Rahim`, `undefined`, `undefined`, `Rahim`, `Karim`, `Karim`. A regular function's `this` comes from how it is called (`undefined` for a plain call in strict mode), an arrow uses the `this` of where it was written, and a bound function can't be re-bound with `.call`.""",
        quick_bn=r"""`Rahim`, `undefined`, `undefined`, `Rahim`, `Karim`, `Karim`। Regular function-এর `this` ঠিক হয় কীভাবে call করা হলো তা দিয়ে (strict mode-এ plain call হলে `undefined`), arrow function যেখানে লেখা হয়েছে সেখানকার `this` নেয়, আর `bind` করা function-কে `.call` দিয়ে আবার বদলানো যায় না।""",
        ex_en=r"""
            Precedence for regular functions, highest first:

            1. `new Fn()` → the newly created object.
            2. Bound function (`bind`) → the bound value (only `new` can override it).
            3. `call` / `apply` → the first argument.
            4. Method call `obj.fn()` → `obj` (the object *before the dot at call time*).
            5. Plain call `fn()` → `undefined` in strict mode, `globalThis` in sloppy mode.

            Arrow functions skip all of these rules — even `call`, `apply` and `bind` can't change their `this`.

            Why the "ES module" detail matters: in a classic browser script (sloppy mode), line 2 would read `window.name` (usually an empty string) and line 3 would also see `window`. In a Node CommonJS file, top-level `this` is `module.exports` (`{}`).

            The real-world bug is line 2: passing a method as a callback — `setTimeout(user.regular, 100)` or `button.addEventListener('click', this.handleClick)` — loses the receiver. Fix with an arrow wrapper, `bind`, or a class-field arrow.
        """,
        ex_bn=r"""
            Regular function-এর ক্ষেত্রে অগ্রাধিকার (সবচেয়ে বেশি থেকে):

            1. `new Fn()` → নতুন তৈরি হওয়া object।
            2. Bound function (`bind`) → bind করা value (শুধু `new` এটা override করতে পারে)।
            3. `call` / `apply` → প্রথম argument।
            4. Method call `obj.fn()` → `obj` (*call করার মুহূর্তে dot-এর আগে* যে object)।
            5. সাধারণ call `fn()` → strict mode-এ `undefined`, sloppy mode-এ `globalThis`।

            Arrow function এই সব নিয়ম এড়িয়ে যায় — `call`, `apply`, `bind` দিয়েও এর `this` বদলানো যায় না।

            "ES module" কথাটা কেন জরুরি: classic browser script-এ (sloppy mode) line 2 পড়ত `window.name` (সাধারণত খালি string), আর line 3-ও `window` দেখত। Node-এর CommonJS file-এ top-level `this` হলো `module.exports` (`{}`)।

            বাস্তবের bug হলো line 2: method-কে callback হিসেবে pass করা — `setTimeout(user.regular, 100)` বা `button.addEventListener('click', this.handleClick)` — এতে receiver হারিয়ে যায়। Arrow wrapper, `bind`, বা class-field arrow দিয়ে ঠিক করো।
        """,
        tip_en=r"""Answer each line with the rule name ("implicit binding", "default binding", "lexical this", "explicit", "hard binding"). Then connect line 2 to the real callback bug — interviewers love that link.""",
        tip_bn=r"""প্রতিটি line-এর উত্তরে নিয়মের নামটা বলো ("implicit binding", "default binding", "lexical this", "explicit", "hard binding")। তারপর line 2-কে বাস্তবের callback bug-এর সাথে যুক্ত করো — interviewer এই সংযোগটা খুব পছন্দ করেন।""",
        mist_en=r"""Thinking `this` is fixed where the function is defined (true only for arrows), or that an arrow inside an object literal gets the object as `this`.""",
        mist_bn=r"""ভাবা যে function যেখানে define করা সেখানেই `this` ঠিক হয়ে যায় (এটা শুধু arrow-এর জন্য সত্য), অথবা object literal-এর ভেতরের arrow সেই object-কে `this` হিসেবে পায়।""",
        follow=[
            ("What does `this` refer to inside a DOM event handler declared with `function`?", "`function` দিয়ে লেখা DOM event handler-এর ভেতরে `this` কী নির্দেশ করে?"),
            ("Can you `bind` a function twice? What happens?", "একটা function-কে কি দুইবার `bind` করা যায়? করলে কী হয়?"),
        ],
        related=["js-006", "js-020"],
        refs=[R_THIS, R_BIND, R_CALL],
    ),
    # ------------------------------------------------------------------ js-016
    Q(
        id="js-016", sub="Event Loop, Microtasks & Tasks", diff="medium", type="output",
        prio="high", market="both", mins=5,
        tags=["event-loop", "microtasks", "settimeout", "queuemicrotask", "await"],
        ver="Version-independent concept (HTML event loop & ECMAScript jobs; same in Node.js 24/26)", vs=False, status="stable",
        q_en=r"""In what order are the letters logged? Explain using the call stack, the microtask queue and the task queue.""",
        q_bn=r"""Letter-গুলো কোন ক্রমে log হবে? Call stack, microtask queue আর task queue দিয়ে ব্যাখ্যা করো।""",
        code=r"""
            console.log('A');

            setTimeout(() => console.log('B'), 0);

            Promise.resolve().then(() => console.log('C'));

            queueMicrotask(() => console.log('D'));

            (async () => {
              console.log('E');
              await null;
              console.log('F');
            })();

            console.log('G');
        """,
        lang="javascript",
        output=r"""
            A
            E
            G
            C
            D
            F
            B
        """,
        a_en=r"""
            The rule: run all **synchronous** code first; when the call stack is empty, drain **every microtask** (promise reactions, `queueMicrotask`, `await` continuations) in FIFO order; only then take the next **task** (like a `setTimeout` callback).

            - Sync: `A`, then the async function runs synchronously until its first `await` → `E`, then `G`.
            - Microtasks, in the order they were queued: `C` (the `.then` on an already-resolved promise), `D` (`queueMicrotask`), `F` (the continuation after `await null`).
            - Task: `B` from `setTimeout(..., 0)`.

            So: `A E G C D F B`.
        """,
        a_bn=r"""
            নিয়ম হলো: আগে সব **synchronous** code চলে; call stack খালি হলে **সব microtask** (promise reaction, `queueMicrotask`, `await`-এর পরের অংশ) FIFO ক্রমে শেষ করা হয়; তারপরই কেবল পরের **task** (যেমন `setTimeout` callback) নেওয়া হয়।

            - Sync: `A`, তারপর async function প্রথম `await` পর্যন্ত synchronously চলে → `E`, তারপর `G`।
            - Microtask, যে ক্রমে queue-তে ঢুকেছে: `C` (আগেই resolved promise-এর `.then`), `D` (`queueMicrotask`), `F` (`await null`-এর পরের অংশ)।
            - Task: `setTimeout(..., 0)` থেকে `B`।

            তাই: `A E G C D F B`।
        """,
        quick_en=r"""`A E G C D F B`. Synchronous code runs first (the async function runs until its `await`), then every microtask in FIFO order (`C`, `D`, then the `await` continuation `F`), and only then the `setTimeout` task `B`.""",
        quick_bn=r"""`A E G C D F B`। আগে synchronous code চলে (async function তার `await` পর্যন্ত চলে), তারপর সব microtask FIFO order-এ (`C`, `D`, তারপর `await`-এর পরের অংশ `F`), আর সবশেষে `setTimeout`-এর task `B`।""",
        ex_en=r"""
            Step by step:

            1. `A` logs. `setTimeout` hands the callback to the timer system; when it expires it goes to the **task queue**.
            2. `Promise.resolve().then(C)` — the promise is already fulfilled, so the reaction job `C` is queued as a **microtask** immediately.
            3. `queueMicrotask(D)` → microtask queue: `[C, D]`.
            4. The async IIFE runs synchronously: logs `E`, hits `await null`. `await` always suspends (even for a non-promise), so the rest of the function is queued as a microtask: `[C, D, F]`.
            5. `G` logs; the script ends and the call stack is empty.
            6. Microtask checkpoint: `C`, `D`, `F`.
            7. Next task: `B`.

            `setTimeout(fn, 0)` means "not before the next task", not "immediately" — browsers even clamp deeply nested timers (after five levels) to at least 4 ms. Rendering in a browser can only happen between tasks, after the microtask queue is empty.
        """,
        ex_bn=r"""
            ধাপে ধাপে:

            1. `A` log হয়। `setTimeout` callback-টা timer system-এর হাতে দেয়; সময় শেষ হলে সেটা **task queue**-তে যায়।
            2. `Promise.resolve().then(C)` — promise আগে থেকেই fulfilled, তাই reaction job `C` সাথে সাথে **microtask** হিসেবে queue হয়।
            3. `queueMicrotask(D)` → microtask queue: `[C, D]`।
            4. Async IIFE synchronously চলে: `E` log করে, `await null`-এ পৌঁছায়। `await` সবসময় function থামায় (non-promise হলেও), তাই function-এর বাকি অংশ microtask হিসেবে queue হয়: `[C, D, F]`।
            5. `G` log হয়; script শেষ, call stack খালি।
            6. Microtask checkpoint: `C`, `D`, `F`।
            7. পরের task: `B`।

            `setTimeout(fn, 0)` মানে "পরের task-এর আগে নয়", "এখনই" নয় — অনেক গভীরে nested timer-কে (পাঁচ স্তরের পর) browser কমপক্ষে 4 ms-এ clamp-ও করে। Browser-এ rendering শুধু দুই task-এর মাঝে, microtask queue খালি হওয়ার পরে হতে পারে।
        """,
        tip_en=r"""Draw three boxes — call stack, microtask queue, task queue — and move each callback between them as you talk. Explicitly say "`await` continuation is a microtask"; many candidates forget it.""",
        tip_bn=r"""তিনটা বাক্স আঁকো — call stack, microtask queue, task queue — আর কথা বলতে বলতে প্রতিটি callback এক বাক্স থেকে আরেক বাক্সে সরাও। স্পষ্ট করে বলো "`await`-এর continuation একটা microtask" — অনেক candidate এটা ভুলে যায়।""",
        mist_en=r"""Putting `B` before the promise callbacks because "the timer was registered first", or treating `E` as asynchronous — the body of an async function runs synchronously until the first `await`.""",
        mist_bn=r""""Timer আগে register হয়েছে" ভেবে `B`-কে promise callback-গুলোর আগে বসানো, অথবা `E`-কে asynchronous মনে করা — async function-এর body প্রথম `await` পর্যন্ত synchronously চলে।""",
        follow=[
            ("Where would `process.nextTick` fit in this order in Node.js?", "Node.js-এ `process.nextTick` এই ক্রমে কোথায় বসবে?"),
            ("Can a page re-render between two microtasks?", "দুটো microtask-এর মাঝখানে কি page re-render হতে পারে?"),
        ],
        related=["js-017", "js-029", "js-034"],
        refs=[R_EXEC_MODEL, R_MICROTASK],
    ),
    # ------------------------------------------------------------------ js-017
    Q(
        id="js-017", sub="Async/Await", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["async-await", "event-loop", "microtasks", "promises"],
        ver="ES2017+ async/await with the ES2019 await optimisation (all current engines)", vs=True, status="stable",
        q_en=r"""What is the order of the logs?""",
        q_bn=r"""Log-গুলো কোন ক্রমে আসবে?""",
        code=r"""
            async function first() {
              console.log('first start');
              await second();
              console.log('first end');
            }

            async function second() {
              console.log('second');
            }

            console.log('script start');
            setTimeout(() => console.log('timeout'), 0);
            first();
            new Promise((resolve) => {
              console.log('promise executor');
              resolve();
            })
              .then(() => console.log('then 1'))
              .then(() => console.log('then 2'));
            console.log('script end');
        """,
        lang="javascript",
        output=r"""
            script start
            first start
            second
            promise executor
            script end
            first end
            then 1
            then 2
            timeout
        """,
        options=[
            ("script start → first start → second → promise executor → script end → first end → then 1 → then 2 → timeout",
             "script start → first start → second → promise executor → script end → first end → then 1 → then 2 → timeout"),
            ("script start → first start → second → first end → promise executor → script end → then 1 → then 2 → timeout",
             "script start → first start → second → first end → promise executor → script end → then 1 → then 2 → timeout"),
            ("script start → first start → second → promise executor → script end → then 1 → then 2 → first end → timeout",
             "script start → first start → second → promise executor → script end → then 1 → then 2 → first end → timeout"),
            ("script start → first start → second → promise executor → script end → timeout → first end → then 1 → then 2",
             "script start → first start → second → promise executor → script end → timeout → first end → then 1 → then 2"),
        ],
        correct=0,
        a_en=r"""
            Option A. `first()` runs synchronously and calls `second()`, which logs `second` and returns an already-fulfilled promise. `await` still **suspends** `first`, queuing `first end` as a microtask. The `Promise` executor runs synchronously (`promise executor`), and `resolve()` queues `then 1`. After `script end`, microtasks run in FIFO order: `first end`, `then 1`, and `then 1` finishing queues `then 2`. The `setTimeout` task runs last.
        """,
        a_bn=r"""
            Option A। `first()` synchronously চলে আর `second()` call করে, যেটা `second` log করে একটা আগেই fulfilled promise return করে। তবুও `await` `first`-কে **থামায়**, আর `first end`-কে microtask হিসেবে queue করে। `Promise`-এর executor synchronously চলে (`promise executor`), আর `resolve()` `then 1`-কে queue করে। `script end`-এর পর microtask-গুলো FIFO ক্রমে চলে: `first end`, `then 1`, আর `then 1` শেষ হলে `then 2` queue হয়। `setTimeout`-এর task সবার শেষে।
        """,
        quick_en=r"""Option A: the sync logs come first (`script start`, `first start`, `second`, `promise executor`, `script end`), then the microtasks `first end`, `then 1`, `then 2`, and finally `timeout`. `await` suspends `first` even though `second()` is already fulfilled, and its continuation is queued before `then 1`.""",
        quick_bn=r"""Option A: আগে sync log-গুলো (`script start`, `first start`, `second`, `promise executor`, `script end`), তারপর microtask `first end`, `then 1`, `then 2`, আর শেষে `timeout`। `second()` আগেই fulfil হলেও `await` `first`-কে থামিয়ে দেয়, আর তার পরের অংশ `then 1`-এর আগেই queue-তে ঢোকে।""",
        ex_en=r"""
            - **Option B** (the most tempting) assumes `await` continues synchronously when the awaited function has no real async work. It never does — `await` always yields to the microtask queue at least once.
            - **Option C** was actually the behaviour of older engines: before a 2019 spec optimisation (e.g. in Node 10), awaiting a native promise cost three microtask ticks, so both `then 1` and `then 2` ran before `first end`. All current engines take a single tick here. Don't write code that depends on these tick counts.
            - **Option D** puts a task before microtasks, which breaks the basic event-loop rule.

            Two facts worth stating: the `new Promise` executor is synchronous, and `.then` callbacks are queued only when their promise settles — that's why `then 2` waits for `then 1`.
        """,
        ex_bn=r"""
            - **Option B** (সবচেয়ে লোভনীয়) ধরে নেয় যে await করা function-এ আসল async কাজ না থাকলে `await` synchronously এগিয়ে যায়। তা কখনোই হয় না — `await` সবসময় অন্তত একবার microtask queue-কে সুযোগ দেয়।
            - **Option C** আসলে পুরনো engine-এর আচরণ ছিল: ২০১৯ সালের একটা spec optimisation-এর আগে (যেমন Node 10-এ) native promise await করতে তিনটা microtask tick লাগত, তাই `then 1` আর `then 2` দুটোই `first end`-এর আগে চলত। এখনকার সব engine-এ এখানে একটাই tick লাগে। এমন tick-সংখ্যার উপর নির্ভর করে code লিখো না।
            - **Option D** microtask-এর আগে task চালায়, যেটা event loop-এর মৌলিক নিয়ম ভাঙে।

            দুটো তথ্য বলা ভালো: `new Promise`-এর executor synchronous, আর `.then` callback queue হয় কেবল তার promise settle হলে — এজন্যই `then 2` `then 1`-এর জন্য অপেক্ষা করে।
        """,
        tip_en=r"""Narrate it as "sync phase → microtasks → tasks" and say out loud that `await` always yields. Mentioning that older engines behaved like option C is a strong signal of depth — but add that production code must not rely on tick ordering.""",
        tip_bn=r""""Sync phase → microtask → task" — এভাবে বর্ণনা করো, আর জোর দিয়ে বলো যে `await` সবসময় yield করে। পুরনো engine option C-এর মতো আচরণ করত — এটা বললে গভীর জ্ঞান বোঝা যায়, তবে সাথে বলো production code-এ tick-এর ক্রমের উপর নির্ভর করা উচিত নয়।""",
        follow=[
            ("How many microtask ticks does `return somePromise` inside an async function add compared with `return await`?", "Async function-এর ভেতরে `return somePromise` আর `return await`-এর মধ্যে microtask tick-এর পার্থক্য কেমন?"),
        ],
        related=["js-016", "js-023"],
        refs=[R_AWAIT, R_ASYNC_FN],
    ),
    # ------------------------------------------------------------------ js-018
    Q(
        id="js-018", sub="Prototypes & Inheritance", diff="medium", type="output",
        prio="high", market="both", mins=5,
        tags=["prototypes", "prototype-chain", "shadowing", "constructor-functions"],
        ver="Version-independent concept (ES2022+ for `Object.hasOwn`)", vs=False, status="stable",
        q_en=r"""What does this code print? Explain each property lookup.""",
        q_bn=r"""এই code কী print করবে? প্রতিটি property lookup ব্যাখ্যা করো।""",
        code=r"""
            function Animal(name) {
              this.name = name;
            }
            Animal.prototype.legs = 4;
            Animal.prototype.speak = function () {
              return `${this.name} makes a sound`;
            };

            const dog = new Animal('Tommy');
            dog.legs = 3;

            console.log(dog.speak());
            console.log(dog.legs, Animal.prototype.legs);

            delete dog.legs;
            console.log(dog.legs);

            console.log(Object.hasOwn(dog, 'speak'), 'speak' in dog);

            Animal.prototype.speak = function () {
              return `${this.name} barks`;
            };
            console.log(dog.speak());

            Animal.prototype = {
              speak() {
                return 'replaced';
              },
            };
            console.log(dog.speak(), new Animal('Lucy').speak());
        """,
        lang="javascript",
        output=r"""
            Tommy makes a sound
            3 4
            4
            false true
            Tommy barks
            Tommy barks replaced
        """,
        a_en=r"""
            Reading a property first checks the object's **own** properties, then walks up its `[[Prototype]]` chain until it finds the key or reaches `null`. Writing a property always creates/updates an **own** property.

            - `speak` isn't on `dog`, so it's found on `Animal.prototype`, called with `this = dog`.
            - `dog.legs = 3` creates an own property that **shadows** the prototype's `4`; the prototype is untouched.
            - After `delete`, the own property is gone, so the lookup falls back to `4`.
            - `Object.hasOwn` checks only own keys (`false`); `in` checks the whole chain (`true`).
            - Changing a method on the prototype is visible to existing instances because lookup is live → `Tommy barks`.
            - Replacing `Animal.prototype` with a new object does **not** affect `dog` — its `[[Prototype]]` was fixed when it was created. Only new instances use the new object.
        """,
        a_bn=r"""
            Property পড়ার সময় আগে object-এর **নিজস্ব** property দেখা হয়, তারপর `[[Prototype]]` chain ধরে উপরে যাওয়া হয়, key পাওয়া বা `null`-এ পৌঁছানো পর্যন্ত। আর property লিখলে সবসময় **নিজস্ব** property তৈরি/update হয়।

            - `speak` `dog`-এ নেই, তাই `Animal.prototype`-এ পাওয়া যায় এবং `this = dog` দিয়ে call হয়।
            - `dog.legs = 3` একটা নিজস্ব property তৈরি করে, যেটা prototype-এর `4`-কে **shadow** করে; prototype অপরিবর্তিত থাকে।
            - `delete`-এর পর নিজস্ব property চলে যায়, তাই lookup আবার `4`-এ ফিরে যায়।
            - `Object.hasOwn` শুধু নিজস্ব key দেখে (`false`); `in` পুরো chain দেখে (`true`)।
            - Prototype-এর method বদলালে আগের instance-গুলোও সেটা দেখে, কারণ lookup live → `Tommy barks`।
            - `Animal.prototype`-কে নতুন object দিয়ে replace করলে `dog`-এর উপর **কোনো প্রভাব পড়ে না** — তৈরির সময়ই তার `[[Prototype]]` ঠিক হয়ে গেছে। শুধু নতুন instance নতুন object ব্যবহার করে।
        """,
        quick_en=r"""`Tommy makes a sound`, `3 4`, `4`, `false true`, `Tommy barks`, `Tommy barks replaced`. Reads check own properties first and then walk the prototype chain live, but replacing `Animal.prototype` affects only new instances, because `dog` keeps the prototype it was created with.""",
        quick_bn=r"""`Tommy makes a sound`, `3 4`, `4`, `false true`, `Tommy barks`, `Tommy barks replaced`। Property পড়ার সময় আগে নিজের property, তারপর live prototype chain দেখা হয়; কিন্তু `Animal.prototype` পুরো বদলে দিলে শুধু নতুন instance-এ প্রভাব পড়ে, কারণ `dog` তৈরির সময়ের prototype-ই ধরে রাখে।""",
        ex_en=r"""
            Line by line:

            1. `dog.speak()` → own? no → `Animal.prototype.speak` → `Tommy makes a sound`.
            2. `3 4` — own `legs` shadows the prototype's.
            3. `delete dog.legs` removes only the own property → `4`.
            4. `false true`.
            5. Prototype method mutated → `Tommy barks`.
            6. `new Animal(...)` sets the new instance's `[[Prototype]]` to whatever `Animal.prototype` is **at that moment**. `dog` still points to the old object (which has the `barks` version), Lucy points to the new one → `Tommy barks replaced`.

            Notes:
            - `class Animal { speak() {} }` is mostly syntax sugar over the same mechanism: methods live on `Animal.prototype`, and `extends` links `Dog.prototype` to `Animal.prototype`.
            - Replacing `prototype` wholesale also drops the default `constructor` property — a common gotcha in older inheritance code.
            - Put shared methods on the prototype (one copy for all instances) and per-instance data in the constructor.
        """,
        ex_bn=r"""
            Line ধরে ধরে:

            1. `dog.speak()` → নিজস্ব? না → `Animal.prototype.speak` → `Tommy makes a sound`।
            2. `3 4` — নিজস্ব `legs` prototype-এরটাকে shadow করে।
            3. `delete dog.legs` শুধু নিজস্ব property মুছে দেয় → `4`।
            4. `false true`।
            5. Prototype-এর method বদলানো হয়েছে → `Tommy barks`।
            6. `new Animal(...)` নতুন instance-এর `[[Prototype]]` সেট করে **ঠিক সেই মুহূর্তে** `Animal.prototype` যা আছে তাতে। `dog` এখনো পুরনো object-কে point করে (যেখানে `barks` version আছে), Lucy নতুনটাকে → `Tommy barks replaced`।

            কিছু কথা:
            - `class Animal { speak() {} }` মূলত একই mechanism-এর উপর syntax sugar: method-গুলো থাকে `Animal.prototype`-এ, আর `extends` `Dog.prototype`-কে `Animal.prototype`-এর সাথে link করে।
            - পুরো `prototype` replace করলে default `constructor` property-ও হারিয়ে যায় — পুরনো inheritance code-এ এটা একটা common ফাঁদ।
            - Shared method prototype-এ রাখো (সব instance-এর জন্য একটাই copy), আর প্রতি-instance data constructor-এ।
        """,
        tip_en=r"""Use the words "own property", "shadowing" and "`[[Prototype]]` link set at creation". The last line is the differentiator: explain that `new` copies the *reference* at construction time.""",
        tip_bn=r""""Own property", "shadowing" আর "তৈরির সময় সেট হওয়া `[[Prototype]]` link" — এই শব্দগুলো ব্যবহার করো। শেষ line-টাই পার্থক্য গড়ে দেয়: ব্যাখ্যা করো যে `new` construct করার মুহূর্তে *reference*-টা নেয়।""",
        mist_en=r"""Thinking `dog.legs = 3` changes the prototype, or that replacing `Animal.prototype` updates all existing instances.""",
        mist_bn=r"""ভাবা যে `dog.legs = 3` prototype বদলে দেয়, অথবা `Animal.prototype` replace করলে আগের সব instance update হয়ে যায়।""",
        follow=[
            ("How would you rewrite this with `class` and `extends`?", "এটা `class` আর `extends` দিয়ে কীভাবে লিখবে?"),
            ("What does `Object.create(null)` give you and when is it useful?", "`Object.create(null)` কী দেয়, আর কখন এটা কাজে লাগে?"),
        ],
        related=["js-028", "js-030"],
        refs=[R_PROTO_CHAIN, R_HASOWN],
    ),
    # ------------------------------------------------------------------ js-019
    Q(
        id="js-019", sub="Error Handling", diff="medium", type="mcq",
        prio="high", market="both", mins=4,
        tags=["error-handling", "error-cause", "aggregateerror", "promise-any", "error-iserror"],
        ver="ES2022 (`Error.cause`), ES2021 (`Promise.any`/`AggregateError`), ES2026 (`Error.isError`)", vs=True, status="stable",
        q_en=r"""This ES module combines `Error.cause` with `Promise.any`. What does it log?""",
        q_bn=r"""এই ES module-এ `Error.cause` আর `Promise.any` একসাথে ব্যবহার করা হয়েছে। এটা কী log করবে?""",
        code=r"""
            async function loadConfig() {
              try {
                JSON.parse('{ invalid json');
              } catch (err) {
                throw new Error('Config could not be loaded', { cause: err });
              }
            }

            try {
              await Promise.any([
                loadConfig(),
                Promise.reject(new RangeError('Backup config missing')),
              ]);
            } catch (err) {
              console.log(err.name, err.errors.length, err.errors[0].cause.name);
            }
        """,
        lang="javascript",
        output=r"""AggregateError 2 SyntaxError""",
        options=[
            ("`AggregateError 2 SyntaxError`", "`AggregateError 2 SyntaxError`"),
            ("`Error 1 SyntaxError`", "`Error 1 SyntaxError`"),
            ("`RangeError 2 undefined`", "`RangeError 2 undefined`"),
            ("`AggregateError 2 Error`", "`AggregateError 2 Error`"),
        ],
        correct=0,
        a_en=r"""
            `AggregateError 2 SyntaxError`.

            `JSON.parse` throws a `SyntaxError`, which is wrapped in a new `Error` with `{ cause: err }`, so `loadConfig()` rejects with that wrapper. Both inputs to `Promise.any` reject, so it rejects with an `AggregateError` whose `errors` array lists the reasons **in input order**. `errors[0]` is the wrapper, and its `cause` is the original `SyntaxError`.
        """,
        a_bn=r"""
            `AggregateError 2 SyntaxError`।

            `JSON.parse` একটা `SyntaxError` throw করে, যেটাকে `{ cause: err }` দিয়ে নতুন একটা `Error`-এ wrap করা হয়, তাই `loadConfig()` সেই wrapper দিয়ে reject করে। `Promise.any`-এর দুটো input-ই reject করে, তাই এটা একটা `AggregateError` দিয়ে reject করে, যার `errors` array-তে কারণগুলো **input-এর ক্রমে** থাকে। `errors[0]` হলো wrapper, আর তার `cause` হলো আসল `SyntaxError`।
        """,
        quick_en=r"""`AggregateError 2 SyntaxError`. Both inputs reject, so `Promise.any` rejects with an `AggregateError` whose `errors` keep input order; `errors[0]` is the wrapper `Error`, and its `cause` is the original `SyntaxError` from `JSON.parse`.""",
        quick_bn=r"""`AggregateError 2 SyntaxError`। দুটো input-ই reject করে, তাই `Promise.any` একটা `AggregateError` দেয় যার `errors` input order-এ থাকে; `errors[0]` হলো wrapper `Error`, আর তার `cause` হলো `JSON.parse`-এর আসল `SyntaxError`।""",
        ex_en=r"""
            - **Option B** assumes `Promise.any` rejects with the first error like `Promise.all`. It doesn't: it only rejects when *all* inputs reject, and always with an `AggregateError`.
            - **Option D** reads `errors[0].name` instead of `errors[0].cause.name` — the wrapper is a plain `Error`; the root cause is one level deeper.
            - `errors` is ordered by input position, not by which promise rejected first.

            Good error-handling habits this shows:
            - **Wrap, don't swallow:** `throw new Error('context', { cause: err })` adds context ("which config?") without losing the original stack. Loggers and Node's `util.inspect` print the cause chain.
            - **Throw `Error` objects, never strings** — strings have no stack trace.
            - **Custom classes** (`class ValidationError extends Error`) let callers branch on `err instanceof ValidationError` or `err.name`.
            - **`Error.isError(value)`** (ES2026) reliably detects real errors, even across realms (iframes, `vm` contexts) where `instanceof Error` fails. It's not Baseline yet (full support in Chrome/Edge 134+, Firefox 138+ and Node 24.3+; Safari 18.4+ ships only a partial implementation that returns `false` for `DOMException`), so feature-detect it.
            - Always handle rejections: an unhandled rejection crashes a Node process by default and shows up as `unhandledrejection` in browsers.
        """,
        ex_bn=r"""
            - **Option B** ধরে নেয় `Promise.all`-এর মতো `Promise.any`-ও প্রথম error দিয়ে reject করে। তা করে না: *সব* input reject করলেই কেবল reject করে, এবং সবসময় `AggregateError` দিয়ে।
            - **Option D** `errors[0].cause.name`-এর বদলে `errors[0].name` পড়ে — wrapper-টা সাধারণ `Error`; root cause আরেক ধাপ ভেতরে।
            - `errors` সাজানো থাকে input-এর অবস্থান অনুযায়ী, কোন promise আগে reject করেছে সেই অনুযায়ী নয়।

            এখান থেকে ভালো error handling-এর অভ্যাস:
            - **Wrap করো, গিলে ফেলো না:** `throw new Error('context', { cause: err })` দিয়ে context ("কোন config?") যোগ হয়, আর original stack হারায় না। Logger আর Node-এর `util.inspect` পুরো cause chain print করে।
            - **সবসময় `Error` object throw করো, string নয়** — string-এর কোনো stack trace থাকে না।
            - **Custom class** (`class ValidationError extends Error`) থাকলে caller `err instanceof ValidationError` বা `err.name` দিয়ে আলাদা আচরণ করতে পারে।
            - **`Error.isError(value)`** (ES2026) নির্ভরযোগ্যভাবে আসল error চেনে, এমনকি ভিন্ন realm-এও (iframe, `vm` context), যেখানে `instanceof Error` fail করে। এটা এখনো Baseline নয় (Chrome/Edge 134+, Firefox 138+ আর Node 24.3+-এ পুরো support আছে; Safari 18.4+-এ আংশিক implementation, যেটা `DOMException`-এর জন্য `false` দেয়), তাই feature-detect করে ব্যবহার করো।
            - Rejection সবসময় handle করো: unhandled rejection default-ভাবে Node process crash করায়, আর browser-এ `unhandledrejection` event হিসেবে আসে।
        """,
        tip_en=r"""After the answer, zoom out: explain *why* you wrap errors with `cause` (context + root cause) and mention `Error.isError` with its support status. That turns a trivia question into a design discussion.""",
        tip_bn=r"""উত্তরের পর একটু বড় পরিসরে কথা বলো: `cause` দিয়ে error wrap *কেন* করো (context + root cause) সেটা ব্যাখ্যা করো, আর support status সহ `Error.isError`-এর কথা বলো। এতে একটা trivia প্রশ্ন design আলোচনায় পরিণত হয়।""",
        mist_en=r"""Re-throwing with `throw new Error(err.message)` — the original stack and type are lost. Use `{ cause: err }` instead.""",
        mist_bn=r"""`throw new Error(err.message)` দিয়ে আবার throw করা — এতে original stack আর type হারিয়ে যায়। এর বদলে `{ cause: err }` ব্যবহার করো।""",
        follow=[
            ("How would you design a custom error hierarchy for an API client?", "একটা API client-এর জন্য custom error hierarchy কীভাবে design করবে?"),
        ],
        related=["js-011", "js-023", "js-033"],
        refs=[R_CAUSE, R_AGG, R_ISERROR],
    ),
    # ------------------------------------------------------------------ js-020
    Q(
        id="js-020", sub="Debouncing & Throttling", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["debounce", "throttle", "closures", "performance", "timers"],
        ver="Version-independent concept (ECMAScript 2026)", vs=False, status="stable",
        q_en=r"""
            Implement `debounce(fn, wait)`. The returned function should call `fn` only after it has **stopped being called** for `wait` ms, using the latest arguments and the correct `this`. Add a `cancel()` method.

            Example: a search box calls `search('d')`, `search('dh')`, `search('dha')` within 100 ms → `fn` runs **once**, 300 ms after the last call, with `'dha'`.

            Then explain how `throttle` differs and when you would use each.
        """,
        q_bn=r"""
            `debounce(fn, wait)` implement করো। Return করা function-টা `fn`-কে call করবে কেবল তখনই, যখন `wait` ms ধরে তাকে আর **call করা হয়নি** — শেষ argument আর সঠিক `this` সহ। একটা `cancel()` method-ও যোগ করো।

            উদাহরণ: একটা search box 100 ms-এর মধ্যে `search('d')`, `search('dh')`, `search('dha')` call করল → `fn` **একবারই** চলবে, শেষ call-এর 300 ms পরে, `'dha'` দিয়ে।

            এরপর ব্যাখ্যা করো `throttle` কীভাবে আলাদা, আর কখন কোনটা ব্যবহার করবে।
        """,
        a_en=r"""
            Debounce is a closure around a timer id. Every call clears the previous timer and starts a new one; only when the calls stop for `wait` ms does the timer fire and run `fn` with the **latest** arguments. I return a regular `function` (not an arrow) so the caller's `this` is captured, and use an arrow inside `setTimeout` to keep it. `cancel()` clears the pending timer — useful when a component unmounts.

            **Throttle** is different: it runs `fn` **at most once per interval** while calls keep coming (usually first call immediately, plus a trailing call with the latest args).

            - Debounce → "wait until the user stops": search-as-you-type, autosave, form validation, window resize *end*.
            - Throttle → "update regularly during continuous activity": scroll position, infinite-scroll checks, mousemove/drag, progress reporting.

            Each call is O(1) time and O(1) space.
        """,
        a_bn=r"""
            Debounce হলো একটা timer id ঘিরে closure। প্রতিটি call আগের timer clear করে নতুন একটা শুরু করে; call বন্ধ হওয়ার পর `wait` ms পার হলেই কেবল timer fire করে আর **সর্বশেষ** argument দিয়ে `fn` চালায়। আমি একটা regular `function` (arrow নয়) return করি যাতে caller-এর `this` ধরা থাকে, আর `setTimeout`-এর ভেতরে arrow ব্যবহার করি যাতে সেটা হারিয়ে না যায়। `cancel()` pending timer clear করে — component unmount হলে কাজে লাগে।

            **Throttle** আলাদা: call আসতে থাকলেও এটা `fn`-কে **প্রতি interval-এ সর্বোচ্চ একবার** চালায় (সাধারণত প্রথম call সাথে সাথে, আর শেষ argument দিয়ে একটা trailing call)।

            - Debounce → "user থামা পর্যন্ত অপেক্ষা করো": search-as-you-type, autosave, form validation, window resize *শেষ হলে*।
            - Throttle → "চলমান কাজের মধ্যে নিয়মিত update দাও": scroll position, infinite-scroll check, mousemove/drag, progress reporting।

            প্রতিটি call O(1) time আর O(1) space।
        """,
        quick_en=r"""Debounce keeps a timer id in a closure: each call clears the old timer and starts a new one, so `fn` runs once, with the latest arguments and `this`, after calls stop for `wait` ms, and `cancel()` clears the timer. Throttle instead runs `fn` at most once per interval while calls keep coming (scroll, mousemove).""",
        quick_bn=r"""Debounce একটা closure-এ timer id রাখে: প্রতিটা call পুরনো timer clear করে নতুন timer শুরু করে, তাই call থামার `wait` ms পরে `fn` একবারই চলে, সর্বশেষ argument আর সঠিক `this` নিয়ে; `cancel()` timer clear করে দেয়। Throttle এর বদলে call চলতে থাকলেও প্রতি interval-এ সর্বোচ্চ একবার `fn` চালায় (scroll, mousemove)।""",
        ex_en=r"""
            - **`this` and arguments:** `fn.apply(this, args)` forwards both. Returning an arrow function from `debounce` would lose the call-site `this` (e.g. when used as an object method).
            - **Leading vs trailing:** my debounce is trailing-only. A `leading` option fires on the first call and ignores the rest of the burst — good for a "submit" button to block double-clicks.
            - **`maxWait`:** with pure debounce, a user typing non-stop never triggers `fn`. Libraries like lodash add `maxWait` (debounce + throttle hybrid) to guarantee progress.
            - **Cleanup:** call `cancel()` on unmount/route change; otherwise the late callback may update UI that no longer exists.
            - **Debouncing doesn't fix races:** a slow response for `'dh'` can still arrive after the response for `'dha'`. Combine it with `AbortController` or a "latest request wins" check.
            - **Animation work:** for visual updates on scroll, throttling with `requestAnimationFrame` (once per frame) is usually smoother than a fixed millisecond interval.
        """,
        ex_bn=r"""
            - **`this` আর argument:** `fn.apply(this, args)` দুটোই সঠিকভাবে পৌঁছে দেয়। `debounce` থেকে arrow function return করলে call-site-এর `this` হারিয়ে যেত (যেমন object method হিসেবে ব্যবহার করলে)।
            - **Leading বনাম trailing:** আমার debounce শুধু trailing। `leading` option থাকলে প্রথম call-এই fire করে আর burst-এর বাকিগুলো উপেক্ষা করে — "submit" button-এ double-click আটকাতে ভালো।
            - **`maxWait`:** শুধু debounce হলে, কেউ একটানা type করতে থাকলে `fn` কখনো চলবে না। lodash-এর মতো library `maxWait` (debounce + throttle-এর মিশ্রণ) যোগ করে, যাতে নিয়মিত অগ্রগতি নিশ্চিত হয়।
            - **Cleanup:** unmount/route change-এ `cancel()` call করো; নাহলে দেরিতে আসা callback এমন UI update করতে পারে যেটা আর নেই।
            - **Debounce race condition ঠিক করে না:** `'dh'`-এর ধীর response `'dha'`-এর response-এর পরেও আসতে পারে। এর সাথে `AbortController` বা "শেষ request-ই জিতবে" check ব্যবহার করো।
            - **Animation-এর কাজ:** scroll-এর সময় visual update-এর জন্য নির্দিষ্ট millisecond interval-এর চেয়ে `requestAnimationFrame` দিয়ে throttle (প্রতি frame-এ একবার) সাধারণত বেশি smooth হয়।
        """,
        tip_en=r"""Write debounce first (it's shorter), test it aloud with the 'd' → 'dh' → 'dha' timeline, then sketch throttle. Mentioning `this` forwarding, `cancel` on unmount and the race-condition caveat separates you from candidates who memorised the snippet.""",
        tip_bn=r"""আগে debounce লেখো (এটা ছোট), 'd' → 'dh' → 'dha' timeline দিয়ে জোরে জোরে test করো, তারপর throttle-এর একটা খসড়া দাও। `this` forwarding, unmount-এ `cancel` আর race-condition-এর সতর্কতা উল্লেখ করলে snippet মুখস্থ করা candidate-দের থেকে তুমি আলাদা হবে।""",
        mist_en=r"""Creating a new debounced function on every render/keystroke (so the timer is never shared), or swapping the definitions of debounce and throttle.""",
        mist_bn=r"""প্রতিটি render/keystroke-এ নতুন debounced function তৈরি করা (ফলে timer কখনো share হয় না), অথবা debounce আর throttle-এর সংজ্ঞা উল্টে ফেলা।""",
        code=r"""
            function debounce(fn, wait = 300) {
              let timerId;

              function debounced(...args) {
                clearTimeout(timerId);
                timerId = setTimeout(() => {
                  timerId = undefined;
                  fn.apply(this, args); // latest args, caller's `this`
                }, wait);
              }

              debounced.cancel = () => {
                clearTimeout(timerId);
                timerId = undefined;
              };

              return debounced;
            }

            // Usage
            const search = debounce((query) => console.log('search:', query), 300);
            search('d');
            search('dh');
            search('dha'); // → one call: "search: dha" ~300 ms later
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Throttle (leading + trailing)", label_bn="Throttle (leading + trailing)", src=r"""
                function throttle(fn, interval = 200) {
                  let lastRun = 0;
                  let trailingTimer;
                  let lastArgs;
                  let lastThis;

                  return function throttled(...args) {
                    lastArgs = args;
                    lastThis = this;
                    const remaining = interval - (Date.now() - lastRun);

                    if (remaining <= 0) {
                      clearTimeout(trailingTimer);
                      trailingTimer = undefined;
                      lastRun = Date.now();
                      fn.apply(lastThis, lastArgs); // leading call
                    } else if (!trailingTimer) {
                      trailingTimer = setTimeout(() => {
                        trailingTimer = undefined;
                        lastRun = Date.now();
                        fn.apply(lastThis, lastArgs); // trailing call with the latest args
                      }, remaining);
                    }
                  };
                }

                window.addEventListener('scroll', throttle(() => updateProgressBar(window.scrollY), 100));
            """),
        ],
        time="O(1) per call", space="O(1)",
        follow=[
            ("How would you add a `leading` option to `debounce`?", "`debounce`-এ একটা `leading` option কীভাবে যোগ করবে?"),
            ("How do you use a debounced function correctly inside a React component?", "React component-এর ভেতরে debounced function সঠিকভাবে কীভাবে ব্যবহার করবে?"),
        ],
        related=["js-004", "js-033", "js-039"],
        refs=[R_DEBOUNCE, R_THROTTLE],
    ),
    # ------------------------------------------------------------------ js-021
    Q(
        id="js-021", sub="Promises", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["promises", "promise-all", "implementation", "async"],
        ver="Version-independent concept (ES2015+ Promises)", vs=False, status="stable",
        q_en=r"""
            Implement `promiseAll(iterable)` that behaves like `Promise.all`:

            - resolves with an array of results **in input order** (not completion order);
            - accepts plain values and thenables, not only promises;
            - resolves with `[]` for an empty input;
            - rejects as soon as any input rejects, with that reason.

            Example: `promiseAll([delay(30, 'a'), 42, delay(10, 'c')])` → `['a', 42, 'c']`.
        """,
        q_bn=r"""
            `promiseAll(iterable)` implement করো, যেটা `Promise.all`-এর মতো আচরণ করবে:

            - result-এর array দিয়ে resolve করবে **input-এর ক্রমে** (শেষ হওয়ার ক্রমে নয়);
            - শুধু promise নয়, সাধারণ value আর thenable-ও নেবে;
            - খালি input হলে `[]` দিয়ে resolve করবে;
            - কোনো input reject করলেই সাথে সাথে সেই কারণ দিয়ে reject করবে।

            উদাহরণ: `promiseAll([delay(30, 'a'), 42, delay(10, 'c')])` → `['a', 42, 'c']`।
        """,
        a_en=r"""
            I return a new Promise, convert the iterable to an array, and wrap every item with `Promise.resolve(item)` so plain values and thenables are handled uniformly. Each fulfilment is stored at its **original index** — not pushed — so the order matches the input. A `remaining` counter tells me when everything has fulfilled; at zero I resolve with the results.

            For rejection I pass the outer `reject` directly: the first rejection settles the outer promise, and later calls to `resolve`/`reject` are ignored because a promise can only settle once. An empty input resolves immediately with `[]`, otherwise the promise would hang forever.

            Time O(n), space O(n).
        """,
        a_bn=r"""
            আমি একটা নতুন Promise return করি, iterable-কে array-তে রূপান্তর করি, আর প্রতিটি item-কে `Promise.resolve(item)` দিয়ে wrap করি যাতে সাধারণ value আর thenable একইভাবে handle হয়। প্রতিটি fulfilment রাখি তার **মূল index-এ** — push করি না — যাতে ক্রম input-এর সাথে মেলে। একটা `remaining` counter দিয়ে বুঝি কখন সব fulfil হয়েছে; শূন্য হলে result দিয়ে resolve করি।

            Rejection-এর জন্য বাইরের `reject`-টাই সরাসরি দিই: প্রথম rejection বাইরের promise settle করে দেয়, আর পরের `resolve`/`reject` call উপেক্ষিত হয়, কারণ একটা promise কেবল একবারই settle হয়। খালি input হলে সাথে সাথে `[]` দিয়ে resolve করি, নাহলে promise চিরকাল ঝুলে থাকত।

            Time O(n), space O(n)।
        """,
        quick_en=r"""Return a new Promise, wrap each item in `Promise.resolve`, store each result at its original index, and resolve when a `remaining` counter reaches zero (resolve `[]` right away for empty input). Pass the outer `reject` directly so the first rejection wins; O(n) time and space.""",
        quick_bn=r"""একটা নতুন Promise return করি, প্রতিটা item-কে `Promise.resolve` দিয়ে wrap করি, result রাখি তার আসল index-এ, আর `remaining` counter শূন্য হলে resolve করি (empty input-এ সাথে সাথে `[]`)। বাইরের `reject` সরাসরি দিয়ে দিই, তাই প্রথম rejection-ই জেতে; time আর space O(n)।""",
        ex_en=r"""
            - **Why a counter, not `results.length`?** Assigning `results[2]` first makes `length` 3 immediately even though slots 0–1 are empty.
            - **Why `Array.from`?** `Promise.all` accepts any iterable (a `Set`, a generator). If iteration itself throws, the error is thrown inside the executor, which rejects the returned promise — the same as the native behaviour (e.g. `promiseAll(null)` rejects with a `TypeError`).
            - **No cancellation:** after a rejection, the other operations keep running; their results are just ignored. Use `AbortController` if they should stop.
            - **Variant — `allSettled`:** instead of calling `reject`, store `{ status: 'rejected', reason }` and count it as done.
            - **Variant — `race`:** `items.forEach((p) => Promise.resolve(p).then(resolve, reject))`.
            - **Variant — concurrency limit:** don't start all tasks at once; run a pool of N workers (see the promise-pool question).
            - In modern code, `Promise.withResolvers()` (ES2024) can replace the executor pattern when the resolve/reject functions need to be passed around.
        """,
        ex_bn=r"""
            - **`results.length` না দিয়ে counter কেন?** আগে `results[2]` assign করলে slot 0–1 খালি থাকলেও `length` সাথে সাথে 3 হয়ে যায়।
            - **`Array.from` কেন?** `Promise.all` যেকোনো iterable নেয় (`Set`, generator)। Iterate করতে গিয়েই error হলে সেটা executor-এর ভেতরে throw হয়, ফলে return করা promise reject করে — native আচরণের মতোই (যেমন `promiseAll(null)` `TypeError` দিয়ে reject করে)।
            - **Cancellation নেই:** একটা rejection-এর পরও বাকি কাজগুলো চলতে থাকে; শুধু তাদের result উপেক্ষা করা হয়। থামাতে চাইলে `AbortController` ব্যবহার করো।
            - **Variant — `allSettled`:** `reject` call না করে `{ status: 'rejected', reason }` জমা রাখো আর সেটাকেও শেষ হওয়া হিসেবে গোনো।
            - **Variant — `race`:** `items.forEach((p) => Promise.resolve(p).then(resolve, reject))`।
            - **Variant — concurrency limit:** সব task একসাথে শুরু কোরো না; N-টা worker-এর pool চালাও (promise-pool প্রশ্নটা দেখো)।
            - Modern code-এ resolve/reject function অন্য জায়গায় পাঠাতে হলে executor pattern-এর বদলে `Promise.withResolvers()` (ES2024) ব্যবহার করা যায়।
        """,
        tip_en=r"""List the requirements back to the interviewer (order, non-promises, empty input, fail-fast) before coding — then show how each line satisfies one. Finish by mentioning that `Promise.all` doesn't cancel the losers.""",
        tip_bn=r"""Code লেখার আগে requirement-গুলো interviewer-কে আবার বলে নাও (ক্রম, non-promise, খালি input, fail-fast) — তারপর দেখাও কোন line কোন requirement পূরণ করছে। শেষে বলো যে `Promise.all` হেরে যাওয়া কাজগুলো cancel করে না।""",
        mist_en=r"""Using `results.push(value)` (wrong order), forgetting the empty-array case (never resolves), or `await`-ing each promise in a loop — the results are in order, but it isn't fail-fast, and a later rejection can be reported as unhandled while you are still awaiting an earlier promise.""",
        mist_bn=r"""`results.push(value)` ব্যবহার করা (ক্রম ভুল হয়), খালি array-র case ভুলে যাওয়া (কখনো resolve হয় না), অথবা loop-এ একটা একটা করে `await` করা — result ক্রমমতো আসে ঠিকই, কিন্তু এটা fail-fast নয়, আর আগের promise-এর জন্য অপেক্ষা করার সময় পরের কোনো rejection unhandled হিসেবে report হতে পারে।""",
        code=r"""
            function promiseAll(iterable) {
              return new Promise((resolve, reject) => {
                const items = Array.from(iterable);
                const results = new Array(items.length);
                let remaining = items.length;

                if (remaining === 0) {
                  resolve(results);
                  return;
                }

                items.forEach((item, index) => {
                  Promise.resolve(item).then((value) => {
                    results[index] = value; // keep input order
                    remaining -= 1;
                    if (remaining === 0) resolve(results);
                  }, reject); // first rejection wins; later calls are ignored
                });
              });
            }

            const delay = (ms, value) => new Promise((r) => setTimeout(() => r(value), ms));

            promiseAll([delay(30, 'a'), 42, delay(10, 'c')]).then(console.log); // ['a', 42, 'c']
            promiseAll([]).then(console.log);                                   // []
            promiseAll([delay(10, 'x'), Promise.reject(new Error('boom'))])
              .catch((err) => console.log(err.message));                        // 'boom'
        """,
        lang="javascript",
        time="O(n)", space="O(n)",
        follow=[
            ("Now implement `Promise.allSettled`.", "এবার `Promise.allSettled` implement করো।"),
            ("What happens to the other promises after one rejects?", "একটা reject করার পর বাকি promise-গুলোর কী হয়?"),
        ],
        related=["js-011", "js-037"],
        refs=[R_PALL, R_PROMISE],
    ),
]

if __name__ == "__main__":
    save("javascript", "b3", QUESTIONS)
