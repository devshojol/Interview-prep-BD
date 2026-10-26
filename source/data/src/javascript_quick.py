import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
VER = "Version-independent concept (ECMAScript 2026)"

QUESTIONS = [
    Q(
        id="js-q01", sub="Scope & Hoisting", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["hoisting", "tdz", "var", "let"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is hoisting, and how do `var`, `let` and `const` differ?""",
        q_bn=r"""Hoisting কী, আর `var`, `let` ও `const`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""Before running a scope, JavaScript registers all its declarations, so you can refer to them before the line that declares them. A `var` starts as `undefined`, while `let` and `const` stay in the temporal dead zone (TDZ) until their declaration runs, so reading them early throws a `ReferenceError`.""",
        a_bn=r"""কোনো scope চালানোর আগে JavaScript তার সব declaration register করে নেয়, তাই declaration-এর line-এর আগেও সেগুলোর নাম ব্যবহার করা যায়। `var` শুরুতে `undefined` থাকে, কিন্তু `let` আর `const` declaration-এর line চলা পর্যন্ত temporal dead zone (TDZ)-এ থাকে, তাই আগে পড়তে গেলে `ReferenceError` হয়।""",
        code=r"""
            console.log(a); // undefined
            var a = 1;
            console.log(b); // ReferenceError: Cannot access 'b' before initialization
            let b = 2;
        """, lang="javascript",
        ex_en=r"""Nothing is physically moved. Function declarations are hoisted with their body, so you can call them before they appear; function expressions assigned to `let`/`const` are not.""",
        ex_bn=r"""আসলে code সরানো হয় না। Function declaration body-সহ hoist হয়, তাই আগে call করা যায়; কিন্তু `let`/`const`-এ রাখা function expression-কে আগে call করা যায় না।""",
        tip_en=r"""Say "declarations are registered first; `let`/`const` sit in the TDZ" and show the two-line example.""",
        tip_bn=r"""বলো "declaration আগে register হয়; `let`/`const` TDZ-এ থাকে", তারপর দুই line-এর example-টা দেখাও।""",
        follow=[("Are function expressions hoisted?", "Function expression কি hoist হয়?")],
        related=["js-002"],
        refs=[("MDN — Hoisting", "https://developer.mozilla.org/en-US/docs/Glossary/Hoisting")],
    ),
    Q(
        id="js-q02", sub="`this` Keyword", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["call", "apply", "bind", "this"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `call`, `apply` and `bind`?""",
        q_bn=r"""`call`, `apply` আর `bind`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""All three let you choose `this` for a regular function. `call` invokes the function immediately with the arguments listed one by one, `apply` invokes it immediately with the arguments as an array, and `bind` doesn't call it at all: it returns a new function with `this` (and optionally the first arguments) fixed.""",
        a_bn=r"""তিনটা দিয়েই একটা regular function-এর `this` ঠিক করে দেওয়া যায়। `call` function-টাকে সাথে সাথে চালায়, argument দেয় একটা একটা করে; `apply`-ও সাথে সাথে চালায়, কিন্তু argument দেয় একটা array হিসেবে; আর `bind` function চালায় না, `this` (আর চাইলে প্রথম কয়েকটা argument) বসানো একটা নতুন function return করে।""",
        code=r"""
            function greet(greeting, mark) {
              return `${greeting}, ${this.name}${mark}`;
            }
            const user = { name: 'Rafi' };
            console.log(greet.call(user, 'Hi', '!'));        // Hi, Rafi!
            console.log(greet.apply(user, ['Hello', '?']));  // Hello, Rafi?
            const later = greet.bind(user, 'Salam');
            console.log(later('.'));                          // Salam, Rafi.
        """, lang="javascript",
        ex_en=r"""A bound function's `this` can't be changed again with `call` or `apply`, and arrow functions ignore the `this` you pass to any of the three. With spread syntax, `fn.call(obj, ...args)` covers most old uses of `apply`.""",
        ex_bn=r"""`bind` করা function-এর `this` পরে `call` বা `apply` দিয়ে আর বদলানো যায় না, আর arrow function এই তিনটার কোনোটা দিয়ে দেওয়া `this` মানে না। Spread syntax আসার পর `fn.call(obj, ...args)` দিয়েই `apply`-এর বেশিরভাগ পুরনো কাজ হয়ে যায়।""",
        tip_en=r"""Use the memory hook "call = comma, apply = array, bind = later", then show one line of each.""",
        tip_bn=r"""মনে রাখার সহজ উপায় বলো: "call = comma, apply = array, bind = পরে চালানোর জন্য", তারপর প্রতিটার এক line করে example দেখাও।""",
        follow=[("How would you implement `bind` yourself?", "নিজে `bind` implement করবে কীভাবে?")],
        related=["js-015", "js-006"],
        refs=[("MDN — Function.prototype.bind()", f"{MDN}/Reference/Global_Objects/Function/bind")],
    ),
    Q(
        id="js-q03", sub="`this` Keyword", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["this", "strict-mode", "arrow-functions"],
        ver=VER, vs=False, status="stable",
        q_en=r"""How is the value of `this` decided in JavaScript?""",
        q_bn=r"""JavaScript-এ `this`-এর value কীভাবে ঠিক হয়?""",
        a_en=r"""For a regular function, `this` depends on how it is called: `obj.method()` gives `obj`, a plain call gives `undefined` in strict mode (the global object in sloppy scripts), `call`/`apply`/`bind` set it explicitly, and `new` gives the newly created object. Arrow functions have no `this` of their own and use the `this` of the surrounding code.""",
        a_bn=r"""Regular function-এ `this` নির্ভর করে function-টা কীভাবে call করা হলো তার উপর: `obj.method()` হলে `obj`, সাধারণ call হলে strict mode-এ `undefined` (non-strict script-এ global object), `call`/`apply`/`bind` দিলে যা বলে দেওয়া হয়, আর `new` দিলে নতুন তৈরি হওয়া object। Arrow function-এর নিজের `this` নেই, সে চারপাশের code-এর `this` ব্যবহার করে।""",
        code=r"""
            'use strict';
            const user = { name: 'Mitu', hi() { return this?.name; } };
            const hi = user.hi;
            console.log(user.hi());                  // Mitu
            console.log(hi());                       // undefined (receiver lost)
            console.log(hi.call({ name: 'Asif' }));  // Asif
        """, lang="javascript",
        ex_en=r"""The classic bug is passing a method as a callback, like `setTimeout(user.hi, 100)`: the function is called without its object, so `this` is lost. Fix it with `user.hi.bind(user)` or an arrow wrapper `() => user.hi()`.""",
        ex_bn=r"""সবচেয়ে common bug হলো method-কে callback হিসেবে পাঠানো, যেমন `setTimeout(user.hi, 100)`: function-টা object ছাড়াই call হয়, তাই `this` হারিয়ে যায়। `user.hi.bind(user)` বা arrow wrapper `() => user.hi()` দিয়ে ঠিক করো।""",
        tip_en=r"""List the rules in order (`new`, explicit binding, method call, plain call) and finish with "arrows don't have their own `this`".""",
        tip_bn=r"""নিয়মগুলো ক্রম অনুযায়ী বলো (`new`, explicit binding, method call, plain call), শেষে বলো "arrow function-এর নিজের `this` নেই"।""",
        follow=[("Why does `this` get lost when you pass `obj.method` to `setTimeout`?", "`obj.method`-কে `setTimeout`-এ পাঠালে `this` হারিয়ে যায় কেন?")],
        related=["js-015", "js-006"],
        refs=[("MDN — this", f"{MDN}/Reference/Operators/this")],
    ),
    Q(
        id="js-q04", sub="Type Coercion & Equality", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["equality", "coercion", "strict-equality"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `==` and `===`?""",
        q_bn=r"""`==` আর `===`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`===` (strict equality) compares value and type without any conversion. `==` (loose equality) first converts the operands to a common type, which gives surprises like `'0' == false` being `true`. Use `===` by default; `x == null` is the one common exception, because it matches both `null` and `undefined`.""",
        a_bn=r"""`===` (strict equality) কোনো conversion ছাড়াই value আর type দুটোই compare করে। `==` (loose equality) আগে দুই পাশকে একই type-এ convert করে নেয়, তাই `'0' == false`-এর মতো অদ্ভুত ফল `true` আসে। Default হিসেবে `===` ব্যবহার করো; একমাত্র common ব্যতিক্রম `x == null`, কারণ এটা `null` আর `undefined` দুটোকেই ধরে।""",
        code=r"""
            console.log(1 == '1', 1 === '1');                    // true false
            console.log('0' == false, '' == 0);                  // true true
            console.log(null == undefined, null === undefined);  // true false
            console.log(NaN === NaN, Object.is(NaN, NaN));       // false true
        """, lang="javascript",
        ex_en=r"""Objects are compared by reference with both operators, so `{} === {}` is `false`. `NaN` is not equal to anything, itself included; check it with `Number.isNaN`.""",
        ex_bn=r"""দুই operator-ই object compare করে reference দিয়ে, তাই `{} === {}` হলো `false`। `NaN` নিজের সাথেও equal নয়; এটা check করতে `Number.isNaN` ব্যবহার করো।""",
        tip_en=r"""Give one surprising `==` example, then say "I use `===` everywhere, except `x == null` when I mean null or undefined".""",
        tip_bn=r"""`==`-এর একটা অবাক করা example দাও, তারপর বলো "আমি সব জায়গায় `===` ব্যবহার করি, শুধু null বা undefined বোঝাতে `x == null` লিখি"।""",
        follow=[("Why is `NaN === NaN` false, and how do you check for `NaN`?", "`NaN === NaN` কেন false, আর `NaN` check করবে কীভাবে?")],
        related=["js-005"],
        refs=[("MDN — Equality comparisons and sameness", f"{MDN}/Guide/Equality_comparisons_and_sameness")],
    ),
    Q(
        id="js-q05", sub="Variables & Data Types", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["null", "undefined", "data-types"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `null` and `undefined`?""",
        q_bn=r"""`null` আর `undefined`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`undefined` means a value was never assigned: an uninitialised variable, a missing property or argument, or a function without `return`. `null` is a value you assign on purpose to mean "no value". `typeof undefined` is `'undefined'` but `typeof null` is `'object'` (a historic bug), and `null == undefined` is `true` while `null === undefined` is `false`.""",
        a_bn=r"""`undefined` মানে কোনো value কখনো assign করা হয়নি: initialise না করা variable, না থাকা property বা argument, কিংবা `return` ছাড়া function। `null` হলো "কোনো value নেই" বোঝাতে ইচ্ছা করে বসানো একটা value। `typeof undefined` হলো `'undefined'`, কিন্তু `typeof null` হলো `'object'` (পুরনো একটা bug), আর `null == undefined` `true` হলেও `null === undefined` `false`।""",
        code=r"""
            let a;
            const user = { name: 'Rina', phone: null };
            console.log(a, user.email, user.phone);                // undefined undefined null
            console.log(typeof undefined, typeof null);            // undefined object
            console.log(JSON.stringify({ x: undefined, y: null })); // {"y":null}
        """, lang="javascript",
        ex_en=r"""Default parameters apply only for `undefined`, not `null`, and `JSON.stringify` drops `undefined` properties but keeps `null`. The `??` and `?.` operators treat both the same.""",
        ex_bn=r"""Default parameter শুধু `undefined` হলে কাজ করে, `null` হলে নয়; আর `JSON.stringify` `undefined` property বাদ দেয় কিন্তু `null` রেখে দেয়। `??` আর `?.` operator দুটোকে একইভাবে ধরে।""",
        tip_en=r"""Frame it as "`undefined` = not set yet, `null` = deliberately empty", then mention the `typeof null` quirk.""",
        tip_bn=r"""এভাবে বলো: "`undefined` = এখনও set হয়নি, `null` = ইচ্ছা করে খালি রাখা", তারপর `typeof null`-এর অদ্ভুত ব্যাপারটা উল্লেখ করো।""",
        follow=[("Does a default parameter apply when you pass `null`?", "`null` pass করলে কি default parameter কাজ করে?")],
        related=["js-001", "js-005"],
        refs=[("MDN — null", f"{MDN}/Reference/Operators/null")],
    ),
    Q(
        id="js-q06", sub="Debouncing & Throttling", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["debounce", "throttle", "performance", "events"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between debouncing and throttling?""",
        q_bn=r"""Debouncing আর throttling-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""Both limit how often a function runs during a burst of events. Debounce waits until the calls have stopped for a set time and then runs once (search-as-you-type, autosave). Throttle runs at most once per interval while the calls keep coming (scroll, resize or mousemove handlers).""",
        a_bn=r"""দুটোই একটানা অনেক event আসার সময় একটা function কতবার চলবে তা সীমিত করে। Debounce অপেক্ষা করে যতক্ষণ না call একটা নির্দিষ্ট সময় থেমে থাকে, তারপর একবার চালায় (search-as-you-type, autosave)। Throttle call আসতে থাকলেও প্রতি interval-এ সর্বোচ্চ একবার চালায় (scroll, resize বা mousemove handler)।""",
        ex_en=r"""Debounce delays the work until the user pauses; throttle gives regular updates during the activity. In a UI component, create the debounced function once and cancel its pending timer when the component unmounts.""",
        ex_bn=r"""Debounce user থামা পর্যন্ত কাজ পিছিয়ে দেয়; throttle কাজ চলার সময়ই নিয়মিত update দেয়। UI component-এ debounced function একবারই তৈরি করো, আর component unmount হলে pending timer cancel করো।""",
        tip_en=r"""Say "debounce = after the user stops, throttle = at most every N ms" and give one real use case for each.""",
        tip_bn=r"""বলো "debounce = user থামার পরে, throttle = প্রতি N ms-এ সর্বোচ্চ একবার", আর প্রতিটার একটা বাস্তব use case দাও।""",
        follow=[("Which one would you use for a search box that calls an API?", "API call করা একটা search box-এর জন্য কোনটা ব্যবহার করবে?")],
        related=["js-020"],
        refs=[("MDN — Debounce (glossary)", "https://developer.mozilla.org/en-US/docs/Glossary/Debounce")],
    ),
    Q(
        id="js-q07", sub="Promises", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["promise", "async", "then", "catch"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is a Promise, and what states can it be in?""",
        q_bn=r"""Promise কী, আর এর কয়টা state থাকতে পারে?""",
        a_en=r"""A Promise is an object that represents the result of an asynchronous operation that finishes later. It starts `pending` and settles exactly once, either `fulfilled` with a value or `rejected` with a reason. You handle it with `.then()`, `.catch()` and `.finally()`, or with `await` inside an `async` function.""",
        a_bn=r"""Promise হলো এমন একটা object, যেটা পরে শেষ হবে এমন একটা asynchronous কাজের result বোঝায়। এটা শুরু হয় `pending` অবস্থায় আর ঠিক একবার settle হয়: হয় একটা value নিয়ে `fulfilled`, নয়তো একটা কারণ নিয়ে `rejected`। একে handle করা হয় `.then()`, `.catch()` আর `.finally()` দিয়ে, অথবা `async` function-এর ভেতরে `await` দিয়ে।""",
        code=r"""
            const wait = (ms, value) => new Promise((resolve) => setTimeout(() => resolve(value), ms));
            wait(100, 'done')
              .then((value) => console.log(value))
              .catch((err) => console.log('error:', err.message))
              .finally(() => console.log('finished'));
            console.log('sync first');
        """, lang="javascript",
        output=r"""
            sync first
            done
            finished
        """,
        ex_en=r"""`.then` callbacks always run asynchronously as microtasks, even on an already-resolved promise. Always handle rejections: in Node.js an unhandled rejection terminates the process by default.""",
        ex_bn=r"""Promise আগে থেকেই resolve হয়ে থাকলেও `.then` callback সবসময় পরে, microtask হিসেবে চলে। Rejection সবসময় handle করো: Node.js-এ default-ভাবে unhandled rejection process বন্ধ করে দেয়।""",
        tip_en=r"""Name the three states, say "settles once", and show a `.then().catch()` chain next to the `await` + `try/catch` version.""",
        tip_bn=r"""তিনটা state-এর নাম বলো, বলো "একবারই settle হয়", তারপর `.then().catch()` chain আর `await` + `try/catch` version পাশাপাশি দেখাও।""",
        follow=[("What is the difference between `Promise.all` and `Promise.allSettled`?", "`Promise.all` আর `Promise.allSettled`-এর পার্থক্য কী?")],
        related=["js-011", "js-021", "js-023"],
        refs=[("MDN — Promise", f"{MDN}/Reference/Global_Objects/Promise")],
    ),
    Q(
        id="js-q08", sub="Event Delegation & DOM Events", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["dom-events", "preventdefault", "stoppropagation", "bubbling"],
        ver="Version-independent concept (DOM Living Standard)", vs=False, status="stable",
        q_en=r"""What is the difference between `event.preventDefault()` and `event.stopPropagation()`?""",
        q_bn=r"""`event.preventDefault()` আর `event.stopPropagation()`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`preventDefault()` cancels the browser's default action, such as following a link or submitting a form, but the event still bubbles to parent elements. `stopPropagation()` stops the event from travelling further up (or down) the DOM, but the default action still happens. They are independent, so call both if you need both.""",
        a_bn=r"""`preventDefault()` browser-এর default কাজ বাতিল করে, যেমন link-এ যাওয়া বা form submit হওয়া, কিন্তু event তখনও parent element-গুলোতে bubble করে। `stopPropagation()` event-কে DOM-এ আর সামনে যেতে দেয় না, কিন্তু default কাজ ঠিকই হয়। দুটো আলাদা জিনিস, তাই দুটোই দরকার হলে দুটোই call করো।""",
        code=r"""
            form.addEventListener('submit', (event) => {
              event.preventDefault(); // no page reload; send it with fetch instead
              sendWithFetch(new FormData(form));
            });
            menu.addEventListener('click', (event) => {
              event.stopPropagation(); // the document's "close menu" listener won't run
            });
        """, lang="javascript",
        ex_en=r"""Overusing `stopPropagation()` breaks event delegation and any listener on a parent (analytics, "click outside to close"). Prefer checking `event.target` in the parent handler instead.""",
        ex_bn=r"""বেশি বেশি `stopPropagation()` ব্যবহার করলে event delegation আর parent-এর listener (analytics, "বাইরে click করলে বন্ধ হও") কাজ করে না। তার বদলে parent handler-এ `event.target` check করা ভালো।""",
        tip_en=r"""Use the form-submit example for `preventDefault` and the dropdown example for `stopPropagation`; it shows you know when each is needed.""",
        tip_bn=r"""`preventDefault`-এর জন্য form submit আর `stopPropagation`-এর জন্য dropdown-এর example দাও; এতে বোঝা যায় কখন কোনটা লাগে তুমি জানো।""",
        follow=[("What does `stopImmediatePropagation()` do differently?", "`stopImmediatePropagation()` আলাদাভাবে কী করে?")],
        related=["js-010"],
        refs=[("MDN — Event.preventDefault()", "https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault")],
    ),
    Q(
        id="js-q09", sub="Shallow vs Deep Copy", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["shallow-copy", "deep-copy", "structuredclone", "spread"],
        ver="Version-independent concept (`structuredClone`: Baseline widely available)", vs=False, status="stable",
        q_en=r"""What is the difference between a shallow copy and a deep copy?""",
        q_bn=r"""Shallow copy আর deep copy-র মধ্যে পার্থক্য কী?""",
        a_en=r"""A shallow copy creates a new top-level object or array, but nested objects are still shared with the original; spread, `Object.assign` and `Array.from` all make shallow copies. A deep copy duplicates every nested level, so changes never leak back to the original; `structuredClone` makes one.""",
        a_bn=r"""Shallow copy উপরের স্তরে নতুন object বা array বানায়, কিন্তু ভেতরের nested object-গুলো original-এর সাথে share-ই থাকে; spread, `Object.assign` আর `Array.from` সবই shallow copy করে। Deep copy প্রতিটা nested স্তর আলাদা করে copy করে, তাই কোনো পরিবর্তন original-এ ফিরে যায় না; `structuredClone` দিয়ে deep copy করা যায়।""",
        code=r"""
            const user = { name: 'Nadia', address: { city: 'Dhaka' } };
            const shallow = { ...user };
            const deep = structuredClone(user);
            shallow.address.city = 'Sylhet';
            console.log(user.address.city); // Sylhet (shared)
            console.log(deep.address.city); // Dhaka (independent)
        """, lang="javascript",
        ex_en=r"""The old `JSON.parse(JSON.stringify(x))` trick turns `Date` into strings, drops `undefined` and functions, and fails on cycles. `structuredClone` handles dates, maps, sets and cycles, but it can't clone functions and doesn't keep class prototypes.""",
        ex_bn=r"""পুরনো `JSON.parse(JSON.stringify(x))` কৌশল `Date`-কে string বানিয়ে দেয়, `undefined` আর function বাদ দেয়, আর cycle থাকলে fail করে। `structuredClone` date, map, set আর cycle সামলায়, কিন্তু function clone করতে পারে না আর class prototype রাখে না।""",
        tip_en=r"""Show the nested `address` example; interviewers want to hear that spread is shallow.""",
        tip_bn=r"""Nested `address`-এর example দেখাও; interviewer শুনতে চায় যে spread shallow copy করে।""",
        follow=[("What does `JSON.parse(JSON.stringify(obj))` lose?", "`JSON.parse(JSON.stringify(obj))` কী কী হারায়?")],
        related=["js-009", "js-036"],
        refs=[("MDN — structuredClone()", "https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone")],
    ),
    Q(
        id="js-q10", sub="Array Methods", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["map", "filter", "reduce", "foreach"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What do `map`, `filter`, `reduce` and `forEach` do, and how are they different?""",
        q_bn=r"""`map`, `filter`, `reduce` আর `forEach` কী করে, আর এদের মধ্যে পার্থক্য কী?""",
        a_en=r"""`map` returns a new array with every element transformed, `filter` returns a new array with only the elements whose callback returns a truthy value, and `reduce` combines all elements into a single value (a sum, an object, anything). `forEach` just runs a callback for each element and returns `undefined`. None of them change the original array by themselves.""",
        a_bn=r"""`map` প্রতিটা element বদলে একটা নতুন array return করে, `filter` শুধু সেই element-গুলো নিয়ে নতুন array দেয় যেগুলোর জন্য callback truthy return করে, আর `reduce` সব element মিলিয়ে একটা value বানায় (যোগফল, object, যা খুশি)। `forEach` শুধু প্রতিটা element-এর জন্য callback চালায় আর `undefined` return করে। এদের কোনোটাই নিজে থেকে original array বদলায় না।""",
        code=r"""
            const prices = [100, 250, 40];
            console.log(prices.map((p) => p * 2));              // [ 200, 500, 80 ]
            console.log(prices.filter((p) => p >= 100));        // [ 100, 250 ]
            console.log(prices.reduce((sum, p) => sum + p, 0)); // 390
            console.log(prices.forEach((p) => p));              // undefined
        """, lang="javascript",
        ex_en=r"""Always give `reduce` an initial value: on an empty array without one it throws a `TypeError`. Using `map` only for side effects, or `forEach` with `async` callbacks, are common code-review comments.""",
        ex_bn=r"""`reduce`-এ সবসময় initial value দাও: না দিলে empty array-তে `TypeError` হয়। শুধু side effect-এর জন্য `map` ব্যবহার করা, বা `async` callback দিয়ে `forEach` লেখা code review-তে খুব common comment।""",
        tip_en=r"""Answer with one line per method on the same small array, and say which ones return a new array.""",
        tip_bn=r"""একই ছোট array-তে প্রতিটা method-এর এক line করে example দাও, আর কোনগুলো নতুন array return করে সেটা বলো।""",
        follow=[("Why doesn't `await` inside a `forEach` callback wait?", "`forEach` callback-এর ভেতরে `await` দিলে অপেক্ষা করে না কেন?")],
        related=["js-013", "js-012", "js-024"],
        refs=[("MDN — Array.prototype.reduce()", f"{MDN}/Reference/Global_Objects/Array/reduce")],
    ),
]

if __name__ == "__main__":
    save("javascript", "quick", QUESTIONS)
