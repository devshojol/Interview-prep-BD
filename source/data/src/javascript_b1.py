import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
R_TYPEOF = ("MDN — typeof", f"{MDN}/Reference/Operators/typeof")
R_TYPES = ("MDN — JavaScript data types and data structures", f"{MDN}/Data_structures")
R_HOIST = ("MDN — Hoisting (glossary)", "https://developer.mozilla.org/en-US/docs/Glossary/Hoisting")
R_FUNC = ("MDN — function declaration", f"{MDN}/Reference/Statements/function")
R_VAR = ("MDN — var", f"{MDN}/Reference/Statements/var")
R_CLOSURES = ("MDN — Closures", f"{MDN}/Guide/Closures")
R_LET = ("MDN — let", f"{MDN}/Reference/Statements/let")
R_EQUALITY = ("MDN — Equality comparisons and sameness", f"{MDN}/Guide/Equality_comparisons_and_sameness")
R_ADD = ("MDN — Addition (+)", f"{MDN}/Reference/Operators/Addition")
R_ARROW = ("MDN — Arrow function expressions", f"{MDN}/Reference/Functions/Arrow_functions")
R_THIS = ("MDN — this", f"{MDN}/Reference/Operators/this")
R_TOSORTED = ("MDN — Array.prototype.toSorted()", f"{MDN}/Reference/Global_Objects/Array/toSorted")
R_SORT = ("MDN — Array.prototype.sort()", f"{MDN}/Reference/Global_Objects/Array/sort")

QUESTIONS = [
    # ------------------------------------------------------------------ js-001
    Q(
        id="js-001", sub="Variables & Data Types", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["typeof", "data-types", "primitives", "null"],
        ver="Version-independent concept (ECMAScript 2026)", vs=False, status="stable",
        q_en=r"""What does this line print?""",
        q_bn=r"""এই line-টি কী print করবে?""",
        code=r"""
            console.log(typeof null, typeof [], typeof function () {}, typeof NaN, typeof undefined);
        """,
        lang="javascript",
        output=r"""object object function number undefined""",
        options=[
            ("`null object function NaN undefined`", "`null object function NaN undefined`"),
            ("`object object function number undefined`", "`object object function number undefined`"),
            ("`object array function number undefined`", "`object array function number undefined`"),
            ("`null array object number undefined`", "`null array object number undefined`"),
        ],
        correct=1,
        a_en=r"""
            It prints `object object function number undefined`.

            `typeof null` returns `"object"` — a bug from the very first JavaScript implementation that was never fixed because fixing it would break the web. Arrays are ordinary objects, so `typeof []` is `"object"`. Functions are objects too, but `typeof` gives them a special `"function"` result. `NaN` ("not a number") is still a value of the `number` type.
        """,
        a_bn=r"""
            Output হবে `object object function number undefined`।

            `typeof null` দেয় `"object"` — এটা JavaScript-এর একদম প্রথম implementation-এর একটা bug, যেটা ঠিক করলে পুরনো website ভেঙে যাবে বলে আর fix করা হয়নি। Array আসলে সাধারণ object, তাই `typeof []` হলো `"object"`। Function-ও object, কিন্তু `typeof` এদের জন্য আলাদা করে `"function"` দেয়। আর `NaN` ("not a number") নাম শুনে অদ্ভুত লাগলেও এটা `number` type-এরই একটা value।
        """,
        ex_en=r"""
            JavaScript has **8 data types**: 7 primitives (`string`, `number`, `bigint`, `boolean`, `undefined`, `symbol`, `null`) and `object` (which includes arrays, functions, dates, maps, etc.).

            - Option C is the most tempting trap: `typeof` **never** returns `"array"`. Use `Array.isArray(value)` to detect arrays.
            - Option A assumes `typeof null` is `"null"` — it isn't. Check null with `value === null`.
            - For `NaN`, use `Number.isNaN(value)`. The global `isNaN('abc')` returns `true` because it coerces the string to a number first.
            - A safe "is this a non-null object?" check is `value !== null && typeof value === 'object'`.
        """,
        ex_bn=r"""
            JavaScript-এ **৮টি data type** আছে: ৭টি primitive (`string`, `number`, `bigint`, `boolean`, `undefined`, `symbol`, `null`) আর `object` (array, function, date, map সবই এর মধ্যে পড়ে)।

            - সবচেয়ে বড় ফাঁদ হলো option C: `typeof` **কখনোই** `"array"` return করে না। Array চেনার জন্য `Array.isArray(value)` ব্যবহার করতে হয়।
            - Option A ধরে নেয় `typeof null` হলো `"null"` — এটা ভুল। Null check করতে `value === null` লেখো।
            - `NaN` check করতে `Number.isNaN(value)` ব্যবহার করো। Global `isNaN('abc')` `true` দেয়, কারণ সে আগে string-টাকে number-এ coerce করে।
            - "এটা কি null নয় এমন object?" — নিরাপদ check হলো `value !== null && typeof value === 'object'`।
        """,
        tip_en=r"""After answering, list the 8 data types and the reliable checks (`=== null`, `Array.isArray`, `Number.isNaN`). Interviewers like hearing *why* `typeof null` is `"object"` (historical bug kept for compatibility).""",
        tip_bn=r"""উত্তর দেওয়ার পর ৮টি data type আর নির্ভরযোগ্য check-গুলো (`=== null`, `Array.isArray`, `Number.isNaN`) বলো। `typeof null` কেন `"object"` (backward compatibility-র জন্য রেখে দেওয়া পুরনো bug) — এটা বললে interviewer খুশি হয়।""",
        mist_en=r"""Writing `if (typeof data === 'object')` and then reading `data.length` — it crashes when `data` is `null`. Also using the global `isNaN()` instead of `Number.isNaN()`.""",
        mist_bn=r"""`if (typeof data === 'object')` লিখে তারপর `data.length` পড়া — `data` যদি `null` হয় তাহলে crash করবে। আরেকটা ভুল হলো `Number.isNaN()`-এর বদলে global `isNaN()` ব্যবহার করা।""",
        follow=[
            ("How do you reliably check whether a value is a plain object?", "একটা value plain object কিনা সেটা নির্ভরযোগ্যভাবে কীভাবে check করবে?"),
            ("What is the difference between `null` and `undefined`?", "`null` আর `undefined`-এর মধ্যে পার্থক্য কী?"),
        ],
        related=["js-005"],
        refs=[R_TYPEOF, R_TYPES],
    ),
    # ------------------------------------------------------------------ js-002
    Q(
        id="js-002", sub="Scope & Hoisting", diff="easy", type="output",
        prio="high", market="bangladesh", mins=3,
        tags=["hoisting", "function-declaration", "var", "function-expression"],
        ver="Version-independent concept (ECMAScript 2026)", vs=False, status="stable",
        q_en=r"""What is the output of this code? Explain what hoisting does to each declaration.""",
        q_bn=r"""এই code-এর output কী হবে? প্রতিটি declaration-এর উপর hoisting কী প্রভাব ফেলে, ব্যাখ্যা করো।""",
        code=r"""
            console.log(add(2, 3));
            console.log(typeof multiply);
            console.log(total);

            try {
              multiply(2, 3);
            } catch (err) {
              console.log(err.name);
            }

            var total = 10;

            function add(a, b) {
              return a + b;
            }

            var multiply = function (a, b) {
              return a * b;
            };

            console.log(multiply(2, 3), total);
        """,
        lang="javascript",
        output=r"""
            5
            undefined
            undefined
            TypeError
            6 10
        """,
        a_en=r"""
            Before any line runs, the engine sets up the scope: the **function declaration** `add` is hoisted together with its body, while the `var` declarations `total` and `multiply` are hoisted but initialised to `undefined`. The assignments stay where they are written.

            So `add(2, 3)` already works (`5`), `typeof multiply` is `"undefined"`, `total` is `undefined`, and calling `multiply` before the assignment throws a `TypeError` ("multiply is not a function"). At the end both assignments have run, so we get `6 10`.
        """,
        a_bn=r"""
            কোনো line চলার আগেই engine scope তৈরি করে ফেলে: **function declaration** `add` তার পুরো body সহ hoist হয়, আর `var` দিয়ে declare করা `total` ও `multiply` hoist হয় কিন্তু `undefined` দিয়ে initialize হয়। Assignment-গুলো যেখানে লেখা, সেখানেই চলে।

            তাই `add(2, 3)` শুরুতেই কাজ করে (`5`), `typeof multiply` হয় `"undefined"`, `total` হয় `undefined`, আর assignment-এর আগে `multiply` call করলে `TypeError` ("multiply is not a function") throw হয়। শেষে দুটো assignment-ই হয়ে গেছে, তাই output `6 10`।
        """,
        ex_en=r"""
            Step by step:

            1. **Creation phase:** `add` → full function object; `total` → `undefined`; `multiply` → `undefined`.
            2. `add(2, 3)` → `5`.
            3. `typeof multiply` → `"undefined"` (the variable exists, its value is `undefined`).
            4. `total` → `undefined` — no ReferenceError, because `var` is hoisted and initialised.
            5. `multiply(2, 3)` → calling `undefined` throws `TypeError`, so the `catch` prints `err.name`.
            6. `total = 10` and `multiply = function...` run.
            7. Last line → `6 10`.

            Why `TypeError` and not `ReferenceError`? The binding exists, but its value is not callable. If `multiply` were declared with `let` or `const`, line 2 would already throw a `ReferenceError` because of the temporal dead zone. Arrow functions and function expressions follow the hoisting rules of the variable they are assigned to — only function **declarations** are hoisted with their body.
        """,
        ex_bn=r"""
            ধাপে ধাপে:

            1. **Creation phase:** `add` → পুরো function object; `total` → `undefined`; `multiply` → `undefined`।
            2. `add(2, 3)` → `5`।
            3. `typeof multiply` → `"undefined"` (variable আছে, কিন্তু value `undefined`)।
            4. `total` → `undefined` — ReferenceError হয় না, কারণ `var` hoist হয়ে initialize হয়ে আছে।
            5. `multiply(2, 3)` → `undefined`-কে call করায় `TypeError` throw হয়, তাই `catch` block `err.name` print করে।
            6. এরপর `total = 10` আর `multiply = function...` চলে।
            7. শেষ line → `6 10`।

            `ReferenceError` না হয়ে `TypeError` কেন? কারণ binding আছে, শুধু তার value call করা যায় না। `multiply` যদি `let` বা `const` দিয়ে declare করা হতো, তাহলে temporal dead zone-এর কারণে দ্বিতীয় line-এই `ReferenceError` হতো। Arrow function বা function expression যে variable-এ assign করা হয়, সেই variable-এর hoisting নিয়ম মেনে চলে — শুধু function **declaration** body সহ hoist হয়।
        """,
        tip_en=r"""Talk in terms of the "creation phase" vs "execution phase" — it shows you understand *why* hoisting happens instead of memorising rules. Then mention how the answer changes with `let`/`const`.""",
        tip_bn=r""""Creation phase" আর "execution phase" — এই দুই ভাগে ব্যাখ্যা করো। এতে বোঝা যায় তুমি নিয়ম মুখস্থ না করে hoisting *কেন* হয় সেটা বোঝো। শেষে `let`/`const` হলে উত্তর কীভাবে বদলাত, সেটাও বলো।""",
        mist_en=r"""Saying the code "physically moves to the top", or assuming function expressions are hoisted like function declarations.""",
        mist_bn=r"""Code "physically উপরে চলে যায়" বলা, অথবা ধরে নেওয়া যে function expression-ও function declaration-এর মতো body সহ hoist হয়।""",
        follow=[
            ("What would change if `multiply` were declared with `const`?", "`multiply` যদি `const` দিয়ে declare করা হতো, তাহলে কী বদলাত?"),
            ("Are class declarations hoisted?", "Class declaration কি hoist হয়?"),
        ],
        related=["js-025", "js-003"],
        refs=[R_HOIST, R_FUNC, R_VAR],
    ),
    # ------------------------------------------------------------------ js-003
    Q(
        id="js-003", sub="Closures", diff="easy", type="output",
        prio="high", market="both", mins=3,
        tags=["closures", "var", "let", "settimeout", "loops"],
        ver="Version-independent concept (ES2015+ for let)", vs=False, status="stable",
        q_en=r"""What does this code print, and why do the two loops behave differently?""",
        q_bn=r"""এই code কী print করবে, আর দুটো loop আলাদা আচরণ করে কেন?""",
        code=r"""
            for (var i = 0; i < 3; i++) {
              setTimeout(() => console.log('var', i), 0);
            }

            for (let j = 0; j < 3; j++) {
              setTimeout(() => console.log('let', j), 0);
            }
        """,
        lang="javascript",
        output=r"""
            var 3
            var 3
            var 3
            let 0
            let 1
            let 2
        """,
        a_en=r"""
            The `var` loop prints `3` three times; the `let` loop prints `0`, `1`, `2`.

            Each arrow function is a **closure** — it remembers the variable, not a snapshot of its value. With `var` there is only **one** `i` for the whole function scope, and the callbacks run only after the loop has finished (setTimeout schedules a task), when `i` is already `3`. With `let`, the loop creates a **new binding for every iteration**, so each callback closes over its own `j`.
        """,
        a_bn=r"""
            `var` loop তিনবার `3` print করে; `let` loop print করে `0`, `1`, `2`।

            প্রতিটি arrow function একটা **closure** — সে variable-টাকে মনে রাখে, value-র কোনো snapshot নয়। `var` হলে পুরো function scope-এ `i` মাত্র **একটা**, আর callback-গুলো চলে loop শেষ হওয়ার পরে (setTimeout একটা task schedule করে), তখন `i` ইতিমধ্যে `3`। `let` হলে loop **প্রতিটি iteration-এর জন্য নতুন binding** তৈরি করে, তাই প্রতিটি callback নিজের আলাদা `j` ধরে রাখে।
        """,
        ex_en=r"""
            - The loop body runs synchronously and only *schedules* six callbacks. They run later, in order, after the call stack is empty.
            - `var i` is function-scoped (or global here), so all three closures share it. After the last `i++`, the condition `i < 3` fails with `i === 3`.
            - For `let` in a `for` header, the spec copies the current value into a fresh per-iteration environment before each iteration, so the three closures see `0`, `1` and `2`.
            - The order is `var` first because those timers were registered first and have the same delay.

            Before ES2015 the fix was an IIFE (or `setTimeout`'s extra arguments) to capture the value; today just use `let`.
        """,
        ex_bn=r"""
            - Loop-এর body synchronously চলে এবং শুধু ছয়টা callback *schedule* করে। এগুলো পরে, call stack খালি হলে, ক্রমানুসারে চলে।
            - `var i` function-scoped (এখানে global), তাই তিনটা closure-ই একই `i` share করে। শেষ `i++`-এর পর `i === 3` হয়ে `i < 3` condition fail করে।
            - `for` header-এ `let` থাকলে spec অনুযায়ী প্রতিটি iteration-এর আগে current value একটা নতুন per-iteration environment-এ copy হয়, তাই তিনটা closure যথাক্রমে `0`, `1`, `2` দেখে।
            - `var`-এর লাইনগুলো আগে আসে কারণ ওই timer-গুলো আগে register হয়েছে এবং delay একই।

            ES2015-এর আগে value ধরে রাখতে IIFE (বা `setTimeout`-এর extra argument) ব্যবহার করা হতো; এখন শুধু `let` ব্যবহার করলেই হয়।
        """,
        tip_en=r"""Use the phrase "closures capture variables, not values". Then explain the per-iteration binding of `let` — that's the part most candidates can't explain precisely.""",
        tip_bn=r""""Closure value নয়, variable capture করে" — এই কথাটা বলো। তারপর `let`-এর per-iteration binding ব্যাখ্যা করো; বেশিরভাগ candidate এই অংশটা ঠিকভাবে বোঝাতে পারে না।""",
        mist_en=r"""Saying the `var` loop prints `0 1 2` "because setTimeout has 0 delay", or thinking `let` works because it is "not hoisted".""",
        mist_bn=r""""setTimeout-এর delay 0, তাই `var` loop `0 1 2` print করবে" — এমন ভাবা, অথবা মনে করা `let` কাজ করে কারণ এটা "hoist হয় না"।""",
        extra=[
            dict(lang="javascript", label_en="Pre-ES2015 fix with an IIFE", label_bn="ES2015-এর আগের সমাধান (IIFE দিয়ে)", src=r"""
                for (var i = 0; i < 3; i++) {
                  (function (captured) {
                    setTimeout(function () {
                      console.log('var', captured); // 0, 1, 2
                    }, 0);
                  })(i);
                }
            """),
        ],
        follow=[
            ("How would you fix the `var` version without changing `var` to `let`?", "`var`-কে `let` না করে `var` version-টা কীভাবে ঠিক করবে?"),
            ("Why do the callbacks run only after the loop finishes?", "Callback-গুলো loop শেষ হওয়ার পরেই কেন চলে?"),
        ],
        related=["js-004", "js-016"],
        refs=[R_CLOSURES, R_LET],
    ),
    # ------------------------------------------------------------------ js-004
    Q(
        id="js-004", sub="Closures", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["closures", "lexical-scope", "encapsulation", "factory-functions"],
        ver="Version-independent concept (ECMAScript 2026)", vs=False, status="stable",
        q_en=r"""What is a closure in JavaScript? Give a practical example of where you would use one.""",
        q_bn=r"""JavaScript-এ closure কী? কোথায় closure ব্যবহার করবে, একটা বাস্তব উদাহরণ দাও।""",
        a_en=r"""
            A closure is a function together with a reference to the scope it was **created** in. Because of that reference, the function can keep reading and updating those outer variables even after the outer function has returned.

            A common practical use is private state. In the example, `count` can't be reached from outside — only through the functions returned by `createCounter`. I also use closures every day without naming them: event handlers that use a component's variables, `debounce`/`memoize` helpers that keep a timer or cache, and factory functions like `makeLogger('auth')`.
        """,
        a_bn=r"""
            Closure হলো একটা function আর সে যে scope-এ **তৈরি** হয়েছে, সেই scope-এর reference — দুটো মিলে। এই reference-এর কারণে outer function return করার পরেও function-টা বাইরের variable-গুলো পড়তে ও update করতে পারে।

            বাস্তবে সবচেয়ে common ব্যবহার হলো private state রাখা। উদাহরণে `count` বাইরে থেকে access করা যায় না — শুধু `createCounter`-এর return করা function-গুলোর মাধ্যমে। নাম না নিয়েও আমি প্রতিদিন closure ব্যবহার করি: component-এর variable ব্যবহার করা event handler, timer বা cache ধরে রাখা `debounce`/`memoize` helper, আর `makeLogger('auth')`-এর মতো factory function।
        """,
        ex_en=r"""
            - **Lexical scoping:** what a function can see is decided by *where it is written*, not where it is called. Each function object keeps a hidden link (`[[Environment]]`) to its outer lexical environment.
            - **Live, not copied:** a closure sees the current value of the variable. Two closures created in the same call share the same variables (`increment` and `reset` below share `count`).
            - **Each call creates a new scope:** `createCounter(5)` and `createCounter(0)` produce independent counters.
            - **Memory:** captured variables stay alive as long as the closure is reachable. A long-lived listener or timer that closes over a big object keeps it in memory — a classic leak source.
            - Closures are the basis of the module pattern, partial application/currying, memoization and React hooks (where *stale* closures are a common bug).
        """,
        ex_bn=r"""
            - **Lexical scoping:** একটা function কী দেখতে পাবে সেটা ঠিক হয় function-টা *কোথায় লেখা হয়েছে* তা দিয়ে, কোথায় call হচ্ছে তা দিয়ে নয়। প্রতিটি function object তার outer lexical environment-এর একটা hidden link (`[[Environment]]`) রাখে।
            - **Copy নয়, live:** closure variable-এর current value দেখে। একই call-এ তৈরি দুটো closure একই variable share করে (নিচে `increment` আর `reset` একই `count` share করছে)।
            - **প্রতিটি call নতুন scope তৈরি করে:** `createCounter(5)` আর `createCounter(0)` দুটো আলাদা, স্বাধীন counter দেয়।
            - **Memory:** closure যতক্ষণ reachable, capture করা variable-গুলোও ততক্ষণ memory-তে থাকে। দীর্ঘ সময় বেঁচে থাকা listener বা timer যদি বড় কোনো object ধরে রাখে, সেটা memory leak-এর একটা classic কারণ।
            - Module pattern, partial application/currying, memoization আর React hooks — সবকিছুর ভিত্তি closure (React-এ *stale* closure একটা common bug)।
        """,
        tip_en=r"""Give the one-sentence definition, show a 5-line counter, then name 2–3 real uses (debounce, event handlers, private state). Mentioning the memory trade-off shows maturity.""",
        tip_bn=r"""এক লাইনের definition দাও, ৫ লাইনের একটা counter দেখাও, তারপর ২–৩টা বাস্তব ব্যবহার (debounce, event handler, private state) বলো। Memory-র trade-off উল্লেখ করলে তোমাকে অভিজ্ঞ মনে হবে।""",
        mist_en=r"""Defining a closure as "a function inside a function" (nesting alone isn't the point — the retained scope is), or believing closures copy values at creation time.""",
        mist_bn=r"""Closure-কে শুধু "function-এর ভেতরে function" বলা (nesting মূল কথা নয় — scope ধরে রাখাটাই আসল), অথবা ভাবা যে closure তৈরি হওয়ার সময় value copy করে রাখে।""",
        code=r"""
            function createCounter(start = 0) {
              let count = start; // private: not reachable from outside

              return {
                increment: () => ++count,
                reset: () => (count = start),
                get value() {
                  return count;
                },
              };
            }

            const counter = createCounter(5);
            counter.increment();
            counter.increment();
            console.log(counter.value); // 7
            console.log(counter.count); // undefined — no direct access

            const other = createCounter();
            console.log(other.value); // 0 — independent scope
        """,
        lang="javascript",
        follow=[
            ("What is a stale closure and where have you seen one?", "Stale closure কী, আর তুমি কোথায় এটা দেখেছ?"),
            ("Can closures cause memory leaks? How?", "Closure কি memory leak ঘটাতে পারে? কীভাবে?"),
        ],
        related=["js-003", "js-025", "js-022"],
        refs=[R_CLOSURES],
    ),
    # ------------------------------------------------------------------ js-005
    Q(
        id="js-005", sub="Type Coercion & Equality", diff="easy", type="output",
        prio="high", market="bangladesh", mins=4,
        tags=["coercion", "equality", "nan", "operators"],
        ver="Version-independent concept (ECMAScript 2026)", vs=False, status="stable",
        q_en=r"""Predict the output of each line.""",
        q_bn=r"""প্রতিটি line-এর output কী হবে, বলো।""",
        code=r"""
            console.log(1 + '2');
            console.log('5' - 2);
            console.log('5' * '2');
            console.log(true + 1);
            console.log([] + {});
            console.log([1, 2] + [3]);
            console.log(null == undefined, null === undefined);
            console.log(NaN === NaN, Object.is(NaN, NaN));
            console.log('0' == false, Boolean('0'));
        """,
        lang="javascript",
        output=r"""
            12
            3
            10
            2
            [object Object]
            1,23
            true false
            false true
            true true
        """,
        a_en=r"""
            The key rule: `+` concatenates as soon as one operand (after conversion to a primitive) is a string; every other arithmetic operator converts to numbers. `==` converts types before comparing, `===` does not.

            So `1 + '2'` is `'12'`, `'5' - 2` is `3`, `'5' * '2'` is `10`, `true + 1` is `2`. Objects become strings: `[]` → `''`, `{}` → `'[object Object]'`, `[1, 2]` → `'1,2'`. `null == undefined` is a special case that is `true`. `NaN` is never equal to itself, but `Object.is` treats it as the same value. Finally `'0' == false` is `true` (both become `0`), even though `'0'` itself is truthy.
        """,
        a_bn=r"""
            মূল নিয়ম: primitive-এ convert করার পর যেকোনো একটা operand string হলেই `+` concatenation করে; বাকি সব arithmetic operator number-এ convert করে। `==` compare করার আগে type convert করে, `===` করে না।

            তাই `1 + '2'` হয় `'12'`, `'5' - 2` হয় `3`, `'5' * '2'` হয় `10`, `true + 1` হয় `2`। Object string হয়ে যায়: `[]` → `''`, `{}` → `'[object Object]'`, `[1, 2]` → `'1,2'`। `null == undefined` একটা special case, ফল `true`। `NaN` কখনো নিজের সমান নয়, কিন্তু `Object.is` এটাকে একই value ধরে। শেষে `'0' == false` হয় `true` (দুটোই `0` হয়ে যায়), যদিও `'0'` নিজে truthy।
        """,
        ex_en=r"""
            Line by line:

            1. `1 + '2'` → one side is a string → concatenation → `12`.
            2. `'5' - 2` → `-` is numeric only → `5 - 2` → `3`.
            3. `'5' * '2'` → both converted to numbers → `10`.
            4. `true + 1` → `true` becomes `1` → `2`.
            5. `[] + {}` → both objects go through ToPrimitive: `''` + `'[object Object]'`.
            6. `[1, 2] + [3]` → `'1,2'` + `'3'` → `1,23`.
            7. `null == undefined` → `true` by a dedicated rule; `===` → `false` (different types).
            8. `NaN === NaN` → `false` (IEEE 754); `Object.is(NaN, NaN)` → `true`.
            9. `'0' == false` → `false` → `0`, `'0'` → `0` → `true`; `Boolean('0')` → non-empty string → `true`.

            Line 9 shows why `==` is dangerous: a value can be "equal to false" and truthy at the same time.
        """,
        ex_bn=r"""
            Line ধরে ধরে:

            1. `1 + '2'` → এক পাশে string → concatenation → `12`।
            2. `'5' - 2` → `-` শুধু number নিয়ে কাজ করে → `5 - 2` → `3`।
            3. `'5' * '2'` → দুটোই number-এ convert হয় → `10`।
            4. `true + 1` → `true` হয়ে যায় `1` → `2`।
            5. `[] + {}` → দুটো object-ই ToPrimitive-এর মধ্য দিয়ে যায়: `''` + `'[object Object]'`।
            6. `[1, 2] + [3]` → `'1,2'` + `'3'` → `1,23`।
            7. `null == undefined` → আলাদা একটা নিয়মে `true`; `===` → `false` (type আলাদা)।
            8. `NaN === NaN` → `false` (IEEE 754 অনুযায়ী); `Object.is(NaN, NaN)` → `true`।
            9. `'0' == false` → `false` → `0`, `'0'` → `0` → `true`; `Boolean('0')` → খালি নয় এমন string → `true`।

            ৯ নম্বর line দেখায় কেন `==` বিপজ্জনক: একটা value একই সাথে "false-এর সমান" আবার truthy-ও হতে পারে।
        """,
        tip_en=r"""Don't just recite results — state the two rules (`+` with a string concatenates; other operators convert to number) and derive each line from them. Close by saying you use `===` everywhere, except the `x == null` idiom that catches both `null` and `undefined` on purpose.""",
        tip_bn=r"""শুধু ফলাফল মুখস্থ বলো না — দুটো নিয়ম (`+`-এর সাথে string থাকলে concatenation; বাকি operator number-এ convert করে) বলে প্রতিটি line সেখান থেকে বের করো। শেষে বলো যে তুমি সব জায়গায় `===` ব্যবহার করো, শুধু `null` আর `undefined` দুটো একসাথে ধরার জন্য ইচ্ছাকৃতভাবে `x == null` idiom ছাড়া।""",
        mist_en=r"""Expecting `'5' - 2` to be `'52'`, or thinking `[] + {}` throws an error. Another trap: using `arr.includes(NaN)` vs `arr.indexOf(NaN)` — `includes` finds `NaN`, `indexOf` does not.""",
        mist_bn=r"""`'5' - 2`-এর ফল `'52'` আশা করা, অথবা ভাবা `[] + {}` error throw করবে। আরেকটা ফাঁদ: `arr.includes(NaN)` আর `arr.indexOf(NaN)` — `includes` `NaN` খুঁজে পায়, `indexOf` পায় না।""",
        follow=[
            ("When, if ever, would you use `==` in production code?", "Production code-এ কখনো `==` ব্যবহার করবে কি? করলে কখন?"),
            ("What is the difference between `===` and `Object.is`?", "`===` আর `Object.is`-এর মধ্যে পার্থক্য কী?"),
        ],
        related=["js-001"],
        refs=[R_EQUALITY, R_ADD],
    ),
    # ------------------------------------------------------------------ js-006
    Q(
        id="js-006", sub="Arrow Functions", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["arrow-functions", "this", "arguments", "functions"],
        ver="Version-independent concept (ES2015+)", vs=False, status="stable",
        q_en=r"""How are arrow functions different from regular functions? When should you NOT use an arrow function?""",
        q_bn=r"""Arrow function আর regular function-এর মধ্যে পার্থক্য কী? কখন arrow function ব্যবহার করা উচিত নয়?""",
        a_en=r"""
            The big difference is `this`. A regular function gets its `this` from **how it is called**; an arrow function has no `this` of its own and uses the `this` of the surrounding scope (lexical `this`).

            Other differences:
            - Arrow functions have no own `arguments` object — use rest parameters (`...args`).
            - They can't be used with `new` and have no `prototype` property.
            - They can't be generators (`function*`).
            - Concise syntax with implicit return: `x => x * 2`.

            I don't use arrows for object methods or prototype/class methods that need `this` from the call site, for constructors, or for DOM handlers where I want `this` to be the element. I do use them for callbacks (`map`, `then`, `setTimeout`) inside methods, where lexical `this` is exactly what I want.
        """,
        a_bn=r"""
            সবচেয়ে বড় পার্থক্য `this`-এ। Regular function-এর `this` ঠিক হয় **কীভাবে call করা হলো** তা দিয়ে; arrow function-এর নিজের কোনো `this` নেই, সে চারপাশের scope-এর `this` ব্যবহার করে (lexical `this`)।

            আরও পার্থক্য:
            - Arrow function-এর নিজস্ব `arguments` object নেই — rest parameter (`...args`) ব্যবহার করতে হয়।
            - `new` দিয়ে call করা যায় না, `prototype` property-ও নেই।
            - Generator (`function*`) হিসেবে লেখা যায় না।
            - ছোট syntax, implicit return সহ: `x => x * 2`।

            যেসব object method বা prototype/class method-এ call site থেকে `this` দরকার, constructor-এ, বা যে DOM handler-এ `this` হিসেবে element চাই — সেখানে আমি arrow ব্যবহার করি না। কিন্তু method-এর ভেতরের callback-এ (`map`, `then`, `setTimeout`) arrow ব্যবহার করি, কারণ সেখানে lexical `this`-ই দরকার।
        """,
        ex_en=r"""
            Regular function vs arrow function, point by point:

            - **`this`:** dynamic (method call → the object; plain call → `undefined` in strict mode / global object in sloppy mode; `call`/`apply`/`bind` → what you pass) vs lexical (fixed at creation; `call`/`bind` can't change it).
            - **`arguments`:** available vs not available (refers to the outer function's `arguments` if any).
            - **Constructor:** `new Fn()` works vs `TypeError: ... is not a constructor`.
            - **Hoisting:** function declarations are hoisted with their body; arrows are expressions, so they follow `const`/`let` rules.
            - **Object literal trap:** `const obj = { name: 'A', hi: () => this.name }` — `this` is the outer (module/global) `this`, not `obj`.
            - **Class fields:** `handleClick = () => {...}` as a class field *is* a valid pattern: the arrow is created per instance, so `this` is bound to the instance (costs one function per instance).
        """,
        ex_bn=r"""
            Regular function বনাম arrow function, পয়েন্ট ধরে ধরে:

            - **`this`:** regular function-এ dynamic (method call → সেই object; সাধারণ call → strict mode-এ `undefined` / sloppy mode-এ global object; `call`/`apply`/`bind` → যা pass করবে) আর arrow-এ lexical (তৈরির সময় ঠিক হয়ে যায়; `call`/`bind` দিয়ে বদলানো যায় না)।
            - **`arguments`:** regular-এ পাওয়া যায়, arrow-এ যায় না (থাকলে outer function-এর `arguments`-কে নির্দেশ করে)।
            - **Constructor:** `new Fn()` কাজ করে বনাম `TypeError: ... is not a constructor`।
            - **Hoisting:** function declaration body সহ hoist হয়; arrow হলো expression, তাই `const`/`let`-এর নিয়ম মেনে চলে।
            - **Object literal-এর ফাঁদ:** `const obj = { name: 'A', hi: () => this.name }` — এখানে `this` হলো বাইরের (module/global) `this`, `obj` নয়।
            - **Class field:** class field হিসেবে `handleClick = () => {...}` একটা valid pattern: প্রতিটি instance-এর জন্য আলাদা arrow তৈরি হয়, তাই `this` instance-এ bind থাকে (খরচ: প্রতি instance-এ একটা করে function)।
        """,
        tip_en=r"""Lead with lexical `this` — it's the answer interviewers are waiting for — then list the rest quickly. A short "method with a callback inside" example makes it concrete.""",
        tip_bn=r"""শুরুতেই lexical `this`-এর কথা বলো — interviewer মূলত এটাই শুনতে চান — তারপর বাকিগুলো দ্রুত বলে যাও। "Method-এর ভেতরে callback" ধরনের ছোট একটা উদাহরণ দিলে ব্যাপারটা পরিষ্কার হয়।""",
        mist_en=r"""Saying arrow functions "bind `this` to the object they are defined in" — they don't bind anything; an arrow in an object literal does not see that object as `this`.""",
        mist_bn=r"""বলা যে arrow function "যে object-এ define করা, সেই object-এ `this` bind করে" — আসলে arrow কিছুই bind করে না; object literal-এর ভেতরের arrow সেই object-কে `this` হিসেবে দেখে না।""",
        code=r"""
            const team = {
              name: 'Dhaka Devs',
              members: ['Rafi', 'Mitu'],

              listWithRegular() {
                // `this` inside the callback depends on how map calls it → undefined (strict mode)
                return this.members.map(function (m) {
                  return `${m} @ ${this?.name}`;
                });
              },

              listWithArrow() {
                // arrow uses listWithArrow's `this` → team
                return this.members.map((m) => `${m} @ ${this.name}`);
              },

              broken: () => typeof this, // NOT team — outer (module) `this`
            };

            console.log(team.listWithArrow()); // ['Rafi @ Dhaka Devs', 'Mitu @ Dhaka Devs']

            const Person = (name) => {
              this.name = name;
            };
            // new Person('Asif'); // TypeError: Person is not a constructor
        """,
        lang="javascript",
        follow=[
            ("Can you change an arrow function's `this` with `bind`?", "`bind` দিয়ে কি arrow function-এর `this` বদলানো যায়?"),
            ("Why are arrow functions in class fields popular for event handlers?", "Event handler-এর জন্য class field-এ arrow function কেন জনপ্রিয়?"),
        ],
        related=["js-015"],
        refs=[R_ARROW, R_THIS],
    ),
    # ------------------------------------------------------------------ js-007
    Q(
        id="js-007", sub="Array Methods", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["arrays", "tosorted", "sort", "immutability", "es2023"],
        ver="ECMAScript 2023+ (`toSorted`, change-array-by-copy); Baseline widely available", vs=True, status="stable",
        q_en=r"""Given the array below, what is logged after calling `toSorted()` and `reverse()`?""",
        q_bn=r"""নিচের array-তে `toSorted()` আর `reverse()` call করার পর কী log হবে?""",
        code=r"""
            const scores = [40, 100, 1, 5];
            const sorted = scores.toSorted();
            scores.reverse();
            console.log(sorted, scores);
        """,
        lang="javascript",
        output=r"""[ 1, 100, 40, 5 ] [ 5, 1, 100, 40 ]""",
        options=[
            ("`[1, 5, 40, 100]` and `[5, 1, 100, 40]`", "`[1, 5, 40, 100]` এবং `[5, 1, 100, 40]`"),
            ("`[1, 100, 40, 5]` and `[5, 1, 100, 40]`", "`[1, 100, 40, 5]` এবং `[5, 1, 100, 40]`"),
            ("`[1, 100, 40, 5]` and `[40, 100, 1, 5]`", "`[1, 100, 40, 5]` এবং `[40, 100, 1, 5]`"),
            ("`[1, 5, 40, 100]` and `[40, 100, 1, 5]`", "`[1, 5, 40, 100]` এবং `[40, 100, 1, 5]`"),
        ],
        correct=1,
        a_en=r"""
            `[1, 100, 40, 5]` and `[5, 1, 100, 40]`.

            Two things are being tested. First, without a compare function, `sort`/`toSorted` compare elements **as strings**, so `"100"` comes before `"40"`. Second, `toSorted()` (ES2023) returns a **new** array and leaves `scores` alone, while `reverse()` **mutates** `scores` in place.
        """,
        a_bn=r"""
            `[1, 100, 40, 5]` এবং `[5, 1, 100, 40]`।

            এখানে দুটো জিনিস যাচাই হচ্ছে। প্রথমত, compare function না দিলে `sort`/`toSorted` element-গুলোকে **string হিসেবে** compare করে, তাই `"100"` আসে `"40"`-এর আগে। দ্বিতীয়ত, `toSorted()` (ES2023) একটা **নতুন** array return করে এবং `scores`-কে বদলায় না, কিন্তু `reverse()` `scores`-কে সরাসরি **mutate** করে।
        """,
        ex_en=r"""
            - The tempting option A assumes numeric sorting. For numbers always pass a comparator: `scores.toSorted((a, b) => a - b)` → `[1, 5, 40, 100]`.
            - Options C/D assume `reverse()` returns a copy. It doesn't — `sort`, `reverse`, `splice`, `fill`, `copyWithin`, `push/pop/shift/unshift` all mutate.
            - ES2023 added non-mutating twins: `toSorted`, `toReversed`, `toSpliced`, and `with(index, value)`. They are Baseline widely available and very handy for immutable state updates (e.g. React state, Redux reducers).
            - Mutating a shared array is a common bug source: if `scores` came from props or a store, `reverse()` silently changes the caller's data.
        """,
        ex_bn=r"""
            - লোভনীয় option A ধরে নেয় যে sort numeric হবে। Number sort করতে সবসময় comparator দাও: `scores.toSorted((a, b) => a - b)` → `[1, 5, 40, 100]`।
            - Option C/D ধরে নেয় `reverse()` একটা copy return করে। আসলে করে না — `sort`, `reverse`, `splice`, `fill`, `copyWithin`, `push/pop/shift/unshift` সবই original array mutate করে।
            - ES2023 এদের non-mutating জোড়া যোগ করেছে: `toSorted`, `toReversed`, `toSpliced` আর `with(index, value)`। এগুলো Baseline widely available, আর immutable state update-এ (যেমন React state, Redux reducer) খুব কাজে লাগে।
            - Shared array mutate করা bug-এর একটা common উৎস: `scores` যদি props বা store থেকে আসে, `reverse()` চুপচাপ caller-এর data বদলে দেয়।
        """,
        tip_en=r"""Name both traps explicitly (string comparison + mutation) and mention the ES2023 change-array-by-copy methods — it shows you keep up with the language.""",
        tip_bn=r"""দুটো ফাঁদই (string comparison + mutation) স্পষ্ট করে বলো, আর ES2023-এর change-array-by-copy method-গুলোর কথা উল্লেখ করো — এতে বোঝা যায় তুমি language-এর আপডেট খোঁজ রাখো।""",
        mist_en=r"""Using `arr.sort()` on numbers without a comparator, or calling `sort()` on an array you don't own (props/state) instead of `toSorted()` or `[...arr].sort()`.""",
        mist_bn=r"""Comparator ছাড়া number-এর array-তে `arr.sort()` ব্যবহার করা, অথবা নিজের নয় এমন array-তে (props/state) `toSorted()` বা `[...arr].sort()`-এর বদলে সরাসরি `sort()` call করা।""",
        follow=[
            ("How would you sort an array of objects by price, then by name?", "Object-এর array-কে আগে price, তারপর name অনুযায়ী কীভাবে sort করবে?"),
        ],
        related=["js-013", "js-014"],
        refs=[R_TOSORTED, R_SORT],
    ),
]

if __name__ == "__main__":
    save("javascript", "b1", QUESTIONS)
