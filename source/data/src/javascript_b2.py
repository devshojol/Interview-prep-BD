import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN = "https://developer.mozilla.org/en-US/docs/Web/JavaScript"
API = "https://developer.mozilla.org/en-US/docs/Web/API"
R_MAP = ("MDN — Map", f"{MDN}/Reference/Global_Objects/Map")
R_FOROF = ("MDN — for...of", f"{MDN}/Reference/Statements/for...of")
R_DESTRUCT = ("MDN — Destructuring", f"{MDN}/Reference/Operators/Destructuring")
R_SPREAD = ("MDN — Spread syntax (...)", f"{MDN}/Reference/Operators/Spread_syntax")
R_BUBBLING = ("MDN — Event bubbling", "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling")
R_ADDEVT = ("MDN — EventTarget.addEventListener()", f"{API}/EventTarget/addEventListener")
R_CLOSEST = ("MDN — Element.closest()", f"{API}/Element/closest")
R_ANY = ("MDN — Promise.any()", f"{MDN}/Reference/Global_Objects/Promise/any")
R_RACE = ("MDN — Promise.race()", f"{MDN}/Reference/Global_Objects/Promise/race")
R_ALLSETTLED = ("MDN — Promise.allSettled()", f"{MDN}/Reference/Global_Objects/Promise/allSettled")
R_GROUPBY = ("MDN — Object.groupBy()", f"{MDN}/Reference/Global_Objects/Object/groupBy")
R_MAPGROUPBY = ("MDN — Map.groupBy()", f"{MDN}/Reference/Global_Objects/Map/groupBy")
R_REDUCE = ("MDN — Array.prototype.reduce()", f"{MDN}/Reference/Global_Objects/Array/reduce")
R_ARROW = ("MDN — Arrow function expressions", f"{MDN}/Reference/Functions/Arrow_functions")
R_FREEZE = ("MDN — Object.freeze()", f"{MDN}/Reference/Global_Objects/Object/freeze")
R_ISFROZEN = ("MDN — Object.isFrozen()", f"{MDN}/Reference/Global_Objects/Object/isFrozen")

QUESTIONS = [
    # ------------------------------------------------------------------ js-008
    Q(
        id="js-008", sub="Coding: Strings & Frequency Counting", diff="easy", type="coding",
        prio="high", market="bangladesh", mins=6,
        tags=["strings", "hash-map", "frequency-count", "coding-test"],
        ver="Version-independent (ES2015+ Map, for...of; ES2020 ??)", vs=False, status="stable",
        q_en=r"""
            Write `firstNonRepeatingChar(str)` that returns the first character that appears **exactly once** in the string, or `null` if there is none. It should be case-sensitive.

            - `firstNonRepeatingChar('swiss')` → `'w'`
            - `firstNonRepeatingChar('aabbcc')` → `null`
            - `firstNonRepeatingChar('Dhaka')` → `'D'`
            - `firstNonRepeatingChar('')` → `null`

            State the time and space complexity.
        """,
        q_bn=r"""
            `firstNonRepeatingChar(str)` নামে একটা function লেখো, যেটা string-এর প্রথম সেই character return করবে যেটা **ঠিক একবার** আছে; এমন কিছু না থাকলে `null`। Function-টা case-sensitive হবে।

            - `firstNonRepeatingChar('swiss')` → `'w'`
            - `firstNonRepeatingChar('aabbcc')` → `null`
            - `firstNonRepeatingChar('Dhaka')` → `'D'`
            - `firstNonRepeatingChar('')` → `null`

            Time ও space complexity বলো।
        """,
        a_en=r"""
            I use **frequency counting** with a `Map` in two passes. The first pass counts every character; the second pass walks the string again in order and returns the first character whose count is `1`. Both passes are linear, so time is **O(n)** and extra space is **O(k)**, where `k` is the number of distinct characters (bounded by the alphabet size).

            I iterate with `for...of` rather than an index loop because `for...of` walks Unicode code points, so an emoji like 😀 is treated as one character instead of two UTF-16 halves.
        """,
        a_bn=r"""
            আমি `Map` দিয়ে দুই pass-এ **frequency counting** করি। প্রথম pass-এ প্রতিটি character গুনি; দ্বিতীয় pass-এ string-টা আবার ক্রমানুসারে ঘুরে প্রথম যে character-এর count `1`, সেটাই return করি। দুটো pass-ই linear, তাই time **O(n)**, আর extra space **O(k)** — যেখানে `k` হলো distinct character-এর সংখ্যা (alphabet size দিয়ে সীমাবদ্ধ)।

            Index loop-এর বদলে `for...of` ব্যবহার করি, কারণ `for...of` Unicode code point ধরে চলে — ফলে 😀-এর মতো emoji দুটো UTF-16 অংশ না হয়ে একটা character হিসেবে গণ্য হয়।
        """,
        ex_en=r"""
            - **Why not `indexOf === lastIndexOf`?** Calling `str.indexOf(ch) === str.lastIndexOf(ch)` inside a loop is O(n²) — fine for 10 characters, slow for 100k. Interviewers usually want you to spot this.
            - **Map vs object:** a `Map` keeps insertion order and has no inherited keys. An optimisation: because the `Map` keeps the order in which characters first appeared, the second pass can loop over the map entries (O(k)) instead of the whole string.
            - **Edge cases:** empty string → `null`; all characters repeated → `null`; case sensitivity (`'D'` vs `'d'`). For a case-insensitive version, count `ch.toLowerCase()` but return the original character.
            - **Unicode:** `for...of` handles surrogate pairs, but not grapheme clusters (e.g. a flag emoji or `e` + combining accent). For those, split with `Intl.Segmenter`.
            - The same counting idea solves other common written-test problems: anagram check (see the extra block), most frequent character, and "two-sum" with a `Map` of seen values.
        """,
        ex_bn=r"""
            - **`indexOf === lastIndexOf` কেন নয়?** Loop-এর ভেতরে `str.indexOf(ch) === str.lastIndexOf(ch)` ব্যবহার করলে complexity O(n²) — ১০টা character-এ সমস্যা নেই, কিন্তু ১ লাখ character-এ ধীর। Interviewer সাধারণত এটা ধরতে পারো কিনা দেখতে চান।
            - **Map বনাম object:** `Map` insertion order রাখে আর এতে কোনো inherited key থাকে না। একটা optimisation: `Map` যেহেতু character-গুলো প্রথম যে ক্রমে এসেছে সেটা মনে রাখে, দ্বিতীয় pass-এ পুরো string-এর বদলে map-এর entry-গুলো (O(k)) ঘুরলেই চলে।
            - **Edge case:** খালি string → `null`; সব character repeat হলে → `null`; case sensitivity (`'D'` বনাম `'d'`)। Case-insensitive চাইলে `ch.toLowerCase()` দিয়ে count করো, কিন্তু return করো original character।
            - **Unicode:** `for...of` surrogate pair ঠিকভাবে handle করে, কিন্তু grapheme cluster (যেমন flag emoji বা `e` + combining accent) নয়। সেগুলোর জন্য `Intl.Segmenter` দিয়ে ভাগ করতে হয়।
            - একই counting কৌশলে written test-এর আরও কিছু common সমস্যা সমাধান হয়: anagram check (extra block দেখো), সবচেয়ে বেশি আসা character, আর আগের value-গুলোর `Map` রেখে "two-sum"।
        """,
        tip_en=r"""Say the brute-force idea and its O(n²) cost first, then improve it to O(n) with a Map. Walk through `'swiss'` out loud and mention the empty-string and Unicode edge cases before the interviewer asks.""",
        tip_bn=r"""আগে brute-force পদ্ধতি আর তার O(n²) খরচের কথা বলো, তারপর Map দিয়ে O(n)-এ উন্নত করো। `'swiss'` দিয়ে জোরে জোরে dry run করো, আর interviewer জিজ্ঞেস করার আগেই খালি string ও Unicode edge case-এর কথা বলো।""",
        mist_en=r"""Returning the first character with count 1 by iterating over a plain object (key order differs for integer-like keys such as `'1'`), or using `str[i]` and breaking emoji into two halves.""",
        mist_bn=r"""Plain object-এর key ঘুরে count 1 পাওয়া প্রথম character return করা (`'1'`-এর মতো integer-like key-এর order আলাদা হয়), অথবা `str[i]` ব্যবহার করে emoji-কে দুই টুকরো করে ফেলা।""",
        code=r"""
            function firstNonRepeatingChar(str) {
              const counts = new Map();

              for (const ch of str) {
                counts.set(ch, (counts.get(ch) ?? 0) + 1);
              }

              for (const ch of str) {
                if (counts.get(ch) === 1) return ch;
              }

              return null;
            }

            console.log(firstNonRepeatingChar('swiss'));  // 'w'
            console.log(firstNonRepeatingChar('aabbcc')); // null
            console.log(firstNonRepeatingChar('Dhaka'));  // 'D' (case-sensitive: 'a' repeats)
            console.log(firstNonRepeatingChar(''));       // null
            console.log(firstNonRepeatingChar('😀ab😀a')); // 'b'
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Same technique: anagram check", label_bn="একই কৌশল: anagram check", src=r"""
                function isAnagram(a, b) {
                  const clean = (s) => s.toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
                  const x = clean(a);
                  const y = clean(b);
                  if (x.length !== y.length) return false;

                  const counts = new Map();
                  for (const ch of x) counts.set(ch, (counts.get(ch) ?? 0) + 1);
                  for (const ch of y) {
                    const n = counts.get(ch);
                    if (!n) return false;
                    counts.set(ch, n - 1);
                  }
                  return true;
                }

                console.log(isAnagram('Listen', 'Silent'));         // true
                console.log(isAnagram('Dormitory', 'Dirty room!')); // true
                console.log(isAnagram('aab', 'abb'));               // false
            """),
        ],
        time="O(n)", space="O(k) — k distinct characters",
        follow=[
            ("How would you make it case-insensitive but still return the original character?", "Case-insensitive করেও original character return করবে কীভাবে?"),
            ("What if the input is a stream of characters that never ends?", "Input যদি কখনো শেষ না হওয়া character-এর stream হয়, তাহলে কী করবে?"),
        ],
        related=["js-012"],
        refs=[R_MAP, R_FOROF],
    ),
    # ------------------------------------------------------------------ js-009
    Q(
        id="js-009", sub="Destructuring & Spread", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["destructuring", "spread", "rest", "default-values", "es2015"],
        ver="Version-independent (ES2015+; object spread/rest ES2018)", vs=False, status="stable",
        q_en=r"""Explain destructuring, the rest pattern and spread syntax. What is the most common pitfall when copying objects with spread?""",
        q_bn=r"""Destructuring, rest pattern আর spread syntax ব্যাখ্যা করো। Spread দিয়ে object copy করার সময় সবচেয়ে common ভুল কোনটা?""",
        a_en=r"""
            **Destructuring** unpacks values from arrays (by position) or objects (by property name) into variables. It supports default values, renaming (`address: { city }`, `id: userId`), nesting and skipping array items.

            **Rest** (`...rest`) on the left side *collects* the remaining items or properties into a new array/object. **Spread** (`...value`) on the right side *expands* an iterable or object into a new array, object or function arguments.

            The pitfall: spread (like `Object.assign`) makes a **shallow copy**. `{ ...user }` is a new object, but `copy.address` still points to the same nested object, so changing `copy.address.city` also changes the original. For a deep copy I use `structuredClone`, or I copy each level I change (`{ ...user, address: { ...user.address, city: 'Sylhet' } }`).
        """,
        a_bn=r"""
            **Destructuring** array (position অনুযায়ী) বা object (property name অনুযায়ী) থেকে value বের করে variable-এ বসায়। এতে default value, নাম বদলানো (`address: { city }`, `id: userId`), nesting আর array item skip করা — সবই করা যায়।

            বাম পাশে **rest** (`...rest`) বাকি item বা property-গুলো *জড়ো করে* একটা নতুন array/object বানায়। ডান পাশে **spread** (`...value`) কোনো iterable বা object-কে নতুন array, object বা function argument-এ *ছড়িয়ে দেয়*।

            ভুলটা হলো: spread (`Object.assign`-এর মতোই) **shallow copy** করে। `{ ...user }` নতুন object ঠিকই, কিন্তু `copy.address` এখনো একই nested object-কে point করে, তাই `copy.address.city` বদলালে original-ও বদলে যায়। Deep copy-র জন্য আমি `structuredClone` ব্যবহার করি, অথবা যে level বদলাচ্ছি সেটা আলাদা করে copy করি (`{ ...user, address: { ...user.address, city: 'Sylhet' } }`)।
        """,
        ex_en=r"""
            - **Defaults apply only to `undefined`**, not `null`: `const { role = 'viewer' } = { role: null }` gives `null`.
            - **Destructuring `null`/`undefined` throws** a `TypeError`. For function parameters, add a default: `function createUser({ name, role = 'viewer' } = {})`, otherwise `createUser()` crashes.
            - **Rest must be last** and collects only own enumerable properties; it's handy for omitting a field: `const { password, ...safeUser } = user`.
            - **Spread order matters:** later properties win — `{ ...defaults, ...options }` lets options override defaults.
            - **Spread works on any iterable for arrays** (`[...new Set(arr)]` removes duplicates, `[...'hello']`), but object spread copies own enumerable properties only — no prototype, no getters (it copies their current values).
            - **Swapping:** `[a, b] = [b, a]`.
        """,
        ex_bn=r"""
            - **Default শুধু `undefined`-এ কাজ করে**, `null`-এ নয়: `const { role = 'viewer' } = { role: null }` দিলে ফল `null`।
            - **`null`/`undefined`-কে destructure করলে** `TypeError` throw হয়। Function parameter-এ default দাও: `function createUser({ name, role = 'viewer' } = {})`, নাহলে `createUser()` crash করবে।
            - **Rest সবসময় শেষে থাকতে হবে**, আর এটা শুধু own enumerable property জড়ো করে; কোনো field বাদ দিতে কাজে লাগে: `const { password, ...safeUser } = user`।
            - **Spread-এ order গুরুত্বপূর্ণ:** পরের property জেতে — `{ ...defaults, ...options }` লিখলে options দিয়ে defaults override হয়।
            - **Array spread যেকোনো iterable-এ কাজ করে** (`[...new Set(arr)]` দিয়ে duplicate বাদ, `[...'hello']`), কিন্তু object spread শুধু own enumerable property copy করে — prototype বা getter নয় (getter-এর current value copy হয়)।
            - **Swap করা:** `[a, b] = [b, a]`।
        """,
        tip_en=r"""Show one object example and one array example, then volunteer the shallow-copy pitfall with a nested `address` object. Mentioning "defaults only for undefined" is a nice precise detail.""",
        tip_bn=r"""একটা object আর একটা array-র উদাহরণ দেখাও, তারপর নিজে থেকেই nested `address` object দিয়ে shallow copy-র ফাঁদটা বলো। "Default শুধু undefined-এর জন্য" — এই সূক্ষ্ম কথাটা বললে ভালো impression হয়।""",
        mist_en=r"""Believing `{ ...obj }` is a deep copy, or expecting a default value to replace `null`.""",
        mist_bn=r"""ভাবা যে `{ ...obj }` deep copy করে, অথবা আশা করা যে default value `null`-কেও replace করবে।""",
        code=r"""
            const user = { id: 7, name: 'Nusrat', address: { city: 'Dhaka' }, role: undefined };

            // Object destructuring: rename via nesting, default, rest
            const { name, role = 'viewer', address: { city }, ...rest } = user;
            console.log(name, role, city, rest); // Nusrat viewer Dhaka { id: 7 }

            // Array destructuring: skip, default, rest
            const [first, , third = 0, ...others] = [10, 20, undefined, 40, 50];
            console.log(first, third, others); // 10 0 [40, 50]

            // Spread = shallow copy
            const copy = { ...user, name: 'Nusrat J.' };
            copy.address.city = 'Sylhet';
            console.log(user.address.city); // 'Sylhet' — nested object is shared!

            // Safe parameter destructuring
            function createUser({ name, role = 'viewer' } = {}) {
              return { name, role };
            }
            console.log(createUser()); // { name: undefined, role: 'viewer' }
        """,
        lang="javascript",
        follow=[
            ("How would you deep-copy an object that contains a `Date` and a `Map`?", "যে object-এ `Date` আর `Map` আছে, সেটা কীভাবে deep copy করবে?"),
            ("How do you remove a property from an object without mutating it?", "Object mutate না করে তার একটা property কীভাবে বাদ দেবে?"),
        ],
        related=["js-036", "js-014"],
        refs=[R_DESTRUCT, R_SPREAD],
    ),
    # ------------------------------------------------------------------ js-010
    Q(
        id="js-010", sub="Event Delegation & DOM Events", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["dom", "events", "bubbling", "capturing", "event-delegation"],
        ver="DOM Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""Explain event bubbling and capturing. What is event delegation and why is it useful?""",
        q_bn=r"""Event bubbling আর capturing ব্যাখ্যা করো। Event delegation কী, আর এটা কেন কাজে লাগে?""",
        a_en=r"""
            When you click an element, the event travels in three phases: **capturing** (from `window` down to the target), **target**, and **bubbling** (from the target back up to `window`). By default `addEventListener` listens in the bubbling phase; passing `{ capture: true }` listens on the way down.

            **Event delegation** uses bubbling: instead of attaching a listener to every child, I attach one listener to a common parent and check `event.target` (usually with `closest()`) to find which child was clicked. It means fewer listeners and less memory, and it automatically works for elements added later — perfect for lists, tables and dynamic content.
        """,
        a_bn=r"""
            কোনো element-এ click করলে event তিনটা phase-এ চলে: **capturing** (`window` থেকে নিচে target পর্যন্ত), **target**, আর **bubbling** (target থেকে আবার উপরে `window` পর্যন্ত)। Default-ভাবে `addEventListener` bubbling phase-এ শোনে; `{ capture: true }` দিলে নিচে নামার পথে শোনে।

            **Event delegation** bubbling-কে কাজে লাগায়: প্রতিটি child-এ listener না বসিয়ে আমি একটা common parent-এ একটা listener বসাই, তারপর `event.target` (সাধারণত `closest()` দিয়ে) check করে বুঝি কোন child-এ click হয়েছে। এতে listener কম লাগে, memory কম খরচ হয়, আর পরে যোগ হওয়া element-এর জন্যও এটা আপনা-আপনি কাজ করে — list, table বা dynamic content-এর জন্য একদম উপযুক্ত।
        """,
        ex_en=r"""
            - **`event.target` vs `event.currentTarget`:** `target` is the deepest element that was actually clicked (maybe a `<span>` inside your button); `currentTarget` is the element the listener is attached to. That's why `closest('button[data-action]')` is used — it walks up from the target.
            - **Check the match is inside the container:** `closest()` can match an ancestor *outside* the delegating parent, so guard with `list.contains(button)` in nested layouts.
            - **Events that don't bubble:** `focus`/`blur` (use `focusin`/`focusout`), `mouseenter`/`mouseleave` (use `mouseover`/`mouseout`), and some media events.
            - **`stopPropagation()`** stops further travel and can silently break delegated handlers higher up — avoid it unless you really need it. **`preventDefault()`** is different: it cancels the browser's default action (link navigation, form submit) but the event still bubbles.
            - Frameworks use the same idea: React attaches its listeners at the root container and dispatches internally.
        """,
        ex_bn=r"""
            - **`event.target` বনাম `event.currentTarget`:** `target` হলো আসলে যে সবচেয়ে ভেতরের element-এ click হয়েছে (হয়তো button-এর ভেতরের একটা `<span>`); `currentTarget` হলো যে element-এ listener বসানো। এজন্যই `closest('button[data-action]')` ব্যবহার করা হয় — এটা target থেকে উপরের দিকে খোঁজে।
            - **Match-টা container-এর ভেতরে কিনা দেখো:** `closest()` delegating parent-এর *বাইরের* কোনো ancestor-কেও match করতে পারে, তাই nested layout-এ `list.contains(button)` দিয়ে guard দাও।
            - **যেসব event bubble করে না:** `focus`/`blur` (এর বদলে `focusin`/`focusout`), `mouseenter`/`mouseleave` (এর বদলে `mouseover`/`mouseout`), আর কিছু media event।
            - **`stopPropagation()`** event-এর যাত্রা থামিয়ে দেয়, ফলে উপরের delegated handler চুপচাপ ভেঙে যেতে পারে — খুব দরকার না হলে এড়িয়ে চলো। **`preventDefault()`** আলাদা জিনিস: এটা browser-এর default action (link navigation, form submit) বাতিল করে, কিন্তু event তবুও bubble করে।
            - Framework-গুলোও একই ধারণা ব্যবহার করে: React তার listener root container-এ বসিয়ে ভেতরে ভেতরে dispatch করে।
        """,
        tip_en=r"""Draw the three phases quickly (down, target, up), then show a 6-line delegation example with `closest()`. Mentioning `target` vs `currentTarget` and non-bubbling events shows real DOM experience.""",
        tip_bn=r"""তিনটা phase (নিচে, target, উপরে) দ্রুত এঁকে বা বলে দাও, তারপর `closest()` দিয়ে ৬ লাইনের একটা delegation উদাহরণ দেখাও। `target` বনাম `currentTarget` আর যেসব event bubble করে না সেগুলো বললে বোঝা যায় তোমার বাস্তব DOM অভিজ্ঞতা আছে।""",
        mist_en=r"""Comparing `event.target` directly to the button (fails when the click lands on an icon inside it), or confusing `stopPropagation()` with `preventDefault()`.""",
        mist_bn=r"""`event.target`-কে সরাসরি button-এর সাথে compare করা (button-এর ভেতরের icon-এ click পড়লে fail করে), অথবা `stopPropagation()` আর `preventDefault()` গুলিয়ে ফেলা।""",
        code=r"""
            const list = document.querySelector('#todo-list');

            // One listener handles every current and future <li>
            list.addEventListener('click', (event) => {
              const button = event.target.closest('button[data-action]');
              if (!button || !list.contains(button)) return;

              const item = button.closest('li');
              if (button.dataset.action === 'delete') item.remove();
              if (button.dataset.action === 'done') item.classList.toggle('done');
            });

            // Capturing-phase listener runs before any bubbling listener
            document.addEventListener('click', () => console.log('capture'), { capture: true });
        """,
        lang="javascript",
        follow=[
            ("How would you delegate `focus` events?", "`focus` event কীভাবে delegate করবে?"),
            ("What is the difference between `stopPropagation` and `stopImmediatePropagation`?", "`stopPropagation` আর `stopImmediatePropagation`-এর পার্থক্য কী?"),
        ],
        related=["js-039"],
        refs=[R_BUBBLING, R_ADDEVT, R_CLOSEST],
    ),
    # ------------------------------------------------------------------ js-011
    Q(
        id="js-011", sub="Promises", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["promises", "promise-any", "promise-race", "combinators"],
        ver="ES2021+ (`Promise.any`); Baseline widely available", vs=True, status="stable",
        q_en=r"""You request the same config file from three CDN mirrors and want the **first successful** response. A fast mirror that *fails* should be ignored unless every mirror fails. Which combinator fits best?""",
        q_bn=r"""তুমি একই config file তিনটা CDN mirror থেকে request করছ, আর **প্রথম সফল** response-টা চাও। দ্রুত কোনো mirror *fail* করলে সেটা উপেক্ষা করতে হবে, যদি না সব mirror-ই fail করে। কোন combinator সবচেয়ে উপযুক্ত?""",
        options=[
            ("`Promise.all`", "`Promise.all`"),
            ("`Promise.race`", "`Promise.race`"),
            ("`Promise.any`", "`Promise.any`"),
            ("`Promise.allSettled`", "`Promise.allSettled`"),
        ],
        correct=2,
        a_en=r"""
            `Promise.any`. It fulfils with the **first fulfilled** promise and ignores rejections. It rejects only if **all** inputs reject, and then it rejects with an `AggregateError` whose `errors` array holds every reason.
        """,
        a_bn=r"""
            `Promise.any`। এটা **প্রথম fulfilled** promise-এর value দিয়ে fulfil হয় এবং rejection-গুলো উপেক্ষা করে। **সব** input reject করলেই শুধু এটা reject করে — তখন একটা `AggregateError` দেয়, যার `errors` array-তে প্রতিটি কারণ থাকে।
        """,
        ex_en=r"""
            The four combinators:

            - `Promise.all` — waits for all to fulfil; rejects as soon as **one** rejects (fail-fast). Use when you need every result.
            - `Promise.race` — settles like the **first promise to settle**, fulfilled *or rejected*. This is the tempting wrong answer: if the fastest mirror fails in 20 ms, `race` rejects even though the other mirrors would succeed. `race` is good for timeouts.
            - `Promise.any` — first **fulfilment** wins; `AggregateError` only if all fail.
            - `Promise.allSettled` — waits for everything and never rejects; returns `{ status, value | reason }` objects. Use for "run all, report partial failures".

            None of them cancels the losing requests. With `fetch`, give each request its own `AbortController` and abort the others after the winner arrives (see the example).
        """,
        ex_bn=r"""
            চারটা combinator:

            - `Promise.all` — সবগুলো fulfil হওয়া পর্যন্ত অপেক্ষা করে; **একটা** reject করলেই সাথে সাথে reject (fail-fast)। প্রতিটি result দরকার হলে ব্যবহার করো।
            - `Promise.race` — **প্রথম যে promise settle হয়**, fulfilled *বা rejected*, সেটার মতোই settle হয়। এটাই লোভনীয় ভুল উত্তর: সবচেয়ে দ্রুত mirror যদি 20 ms-এ fail করে, বাকি mirror সফল হলেও `race` reject করবে। Timeout বানাতে `race` ভালো।
            - `Promise.any` — প্রথম **fulfilment** জেতে; সব fail করলেই শুধু `AggregateError`।
            - `Promise.allSettled` — সবকিছুর জন্য অপেক্ষা করে, কখনো reject করে না; `{ status, value | reason }` object-এর array দেয়। "সব চালাও, আংশিক failure report করো" — এমন ক্ষেত্রে ব্যবহার করো।

            এদের কোনোটাই হেরে যাওয়া request cancel করে না। `fetch`-এর ক্ষেত্রে প্রতিটি request-কে আলাদা `AbortController` দাও, আর winner পাওয়ার পর বাকিগুলো abort করো (উদাহরণ দেখো)।
        """,
        tip_en=r"""Answer with the one-line behaviour of all four combinators — interviewers often follow up with "and when would you use race?". Mentioning `AggregateError` and cancellation shows production thinking.""",
        tip_bn=r"""চারটা combinator-এর আচরণ এক লাইনে করে বলো — interviewer প্রায়ই পরের প্রশ্নে জিজ্ঞেস করেন "তাহলে race কখন ব্যবহার করবে?"। `AggregateError` আর cancellation-এর কথা বললে বোঝা যায় তুমি production-এর দৃষ্টিতে ভাবো।""",
        mist_en=r"""Using `Promise.race` for "first success", or assuming the slower promises are cancelled automatically.""",
        mist_bn=r""""প্রথম সফল" পাওয়ার জন্য `Promise.race` ব্যবহার করা, অথবা ধরে নেওয়া যে ধীর promise-গুলো আপনা-আপনি cancel হয়ে যায়।""",
        extra=[
            dict(lang="javascript", label_en="First successful mirror, then cancel the rest", label_bn="প্রথম সফল mirror, তারপর বাকিগুলো cancel", src=r"""
                const mirrors = ['https://cdn1.example.com', 'https://cdn2.example.com', 'https://cdn3.example.com'];
                const controllers = mirrors.map(() => new AbortController());

                try {
                  const winner = await Promise.any(
                    mirrors.map(async (base, i) => {
                      const res = await fetch(`${base}/config.json`, { signal: controllers[i].signal });
                      if (!res.ok) throw new Error(`${base}: HTTP ${res.status}`);
                      return { i, config: await res.json() };
                    }),
                  );
                  controllers.forEach((c, i) => i !== winner.i && c.abort()); // stop the slower requests
                  console.log(winner.config);
                } catch (err) {
                  console.error('All mirrors failed', err.errors); // AggregateError
                }
            """),
        ],
        follow=[
            ("How would you implement a timeout for a fetch call?", "একটা fetch call-এ timeout কীভাবে implement করবে?"),
        ],
        related=["js-021", "js-019"],
        refs=[R_ANY, R_RACE, R_ALLSETTLED],
    ),
    # ------------------------------------------------------------------ js-012
    Q(
        id="js-012", sub="Objects & Arrays", diff="easy", type="coding",
        prio="high", market="both", mins=5,
        tags=["group-by", "reduce", "object-groupby", "map", "es2024"],
        ver="ES2024 (`Object.groupBy`, `Map.groupBy`; Baseline widely available); manual version ES2021+", vs=True, status="stable",
        q_en=r"""
            Implement `groupBy(items, getKey)` that groups an array into an object of arrays, keyed by whatever `getKey(item)` returns.

            Example: grouping orders by `status` should give `{ paid: [order1, order3], pending: [order2] }`.

            Then explain how you would do the same with built-in methods in modern JavaScript.
        """,
        q_bn=r"""
            `groupBy(items, getKey)` implement করো, যেটা একটা array-কে `getKey(item)` যা return করে সেই key অনুযায়ী array-র object-এ group করবে।

            উদাহরণ: order-গুলোকে `status` অনুযায়ী group করলে পাওয়া উচিত `{ paid: [order1, order3], pending: [order2] }`।

            এরপর বলো, modern JavaScript-এর built-in method দিয়ে একই কাজ কীভাবে করবে।
        """,
        a_en=r"""
            I loop once with `reduce`, compute the key for each item and push the item into that key's array, creating the array the first time with `??=`. I start from `Object.create(null)` so the result has no inherited properties — keys like `'toString'` or `'__proto__'` can't clash with `Object.prototype`. It's **O(n)** time and **O(n)** space.

            In modern code I'd use the built-ins (ES2024, Baseline widely available, Node 21+): `Object.groupBy(items, fn)` returns a null-prototype object, and `Map.groupBy(items, fn)` returns a `Map` — better when keys aren't strings (objects, numbers you don't want stringified) or when you want map methods like `.get()` and `.size`.
        """,
        a_bn=r"""
            আমি `reduce` দিয়ে একবার loop করি, প্রতিটি item-এর key বের করি আর সেই key-র array-তে item push করি; প্রথমবার array তৈরি করি `??=` দিয়ে। শুরু করি `Object.create(null)` থেকে, যাতে result-এ কোনো inherited property না থাকে — `'toString'` বা `'__proto__'`-এর মতো key `Object.prototype`-এর সাথে সংঘর্ষ না করে। Time **O(n)**, space **O(n)**।

            Modern code-এ আমি built-in ব্যবহার করব (ES2024, Baseline widely available, Node 21+): `Object.groupBy(items, fn)` একটা null-prototype object দেয়, আর `Map.groupBy(items, fn)` দেয় একটা `Map` — key যখন string নয় (object, বা এমন number যা string-এ বদলাতে চাও না) অথবা `.get()`, `.size`-এর মতো map method দরকার, তখন এটা ভালো।
        """,
        ex_en=r"""
            - **Why not `{}` as the accumulator?** With a plain object, `groups['constructor']` already exists (inherited), so `(groups[key] ??= [])` would try to push into a function. A null-prototype object avoids this.
            - **Keys are strings** in `Object.groupBy`: `getKey` returning `1` and `'1'` end up in the same group. `Map.groupBy` keeps them separate.
            - **Callback args:** both built-ins pass `(item, index)`, like most array methods — my version does too.
            - **Edge cases:** empty array → empty object; `getKey` returning `undefined` → an `'undefined'` group (decide whether that's acceptable).
            - **Before ES2024** people used lodash's `_.groupBy`. Note the old proposal name `Array.prototype.group` was dropped because of web-compatibility issues — that's why it became a static method.
        """,
        ex_bn=r"""
            - **Accumulator হিসেবে `{}` কেন নয়?** Plain object-এ `groups['constructor']` আগে থেকেই আছে (inherited), তাই `(groups[key] ??= [])` একটা function-এ push করার চেষ্টা করবে। Null-prototype object এই সমস্যা এড়ায়।
            - `Object.groupBy`-এ **key সবসময় string**: `getKey` যদি `1` আর `'1'` return করে, দুটো একই group-এ পড়বে। `Map.groupBy` এগুলো আলাদা রাখে।
            - **Callback argument:** বেশিরভাগ array method-এর মতো দুটো built-in-ই `(item, index)` pass করে — আমার version-ও তাই করে।
            - **Edge case:** খালি array → খালি object; `getKey` `undefined` return করলে → `'undefined'` নামে group (এটা মেনে নেওয়া যায় কিনা ঠিক করো)।
            - **ES2024-এর আগে** মানুষ lodash-এর `_.groupBy` ব্যবহার করত। পুরনো proposal-এর নাম `Array.prototype.group` web-compatibility সমস্যার কারণে বাদ পড়েছিল — এজন্যই এটা static method হয়েছে।
        """,
        tip_en=r"""Write the 6-line `reduce` version first, then say "in production I'd use `Object.groupBy` or `Map.groupBy`" and explain when you'd choose the Map. Knowing the null-prototype detail stands out.""",
        tip_bn=r"""আগে ৬ লাইনের `reduce` version লেখো, তারপর বলো "production-এ আমি `Object.groupBy` বা `Map.groupBy` ব্যবহার করব", আর কখন Map বেছে নেবে সেটা ব্যাখ্যা করো। Null-prototype-এর খুঁটিনাটি জানা থাকলে তুমি আলাদা হয়ে উঠবে।""",
        mist_en=r"""Forgetting to `return groups` from the reducer (the accumulator becomes `undefined` after the first item), or calling `items.groupBy(...)` — it's a static method, not an array method.""",
        mist_bn=r"""Reducer থেকে `return groups` করতে ভুলে যাওয়া (প্রথম item-এর পর accumulator `undefined` হয়ে যায়), অথবা `items.groupBy(...)` call করা — এটা static method, array method নয়।""",
        code=r"""
            function groupBy(items, getKey) {
              return items.reduce((groups, item, index) => {
                const key = getKey(item, index);
                (groups[key] ??= []).push(item);
                return groups;
              }, Object.create(null));
            }

            const orders = [
              { id: 1, status: 'paid', amount: 500 },
              { id: 2, status: 'pending', amount: 1200 },
              { id: 3, status: 'paid', amount: 300 },
            ];

            const byStatus = groupBy(orders, (order) => order.status);
            console.log(Object.keys(byStatus));                // ['paid', 'pending']
            console.log(byStatus.paid.map((order) => order.id)); // [1, 3]

            // Built-ins (ES2024)
            const native = Object.groupBy(orders, (order) => order.status);
            console.log(native.pending.length); // 1

            const bySize = Map.groupBy(orders, (order) => (order.amount >= 1000 ? 'large' : 'small'));
            console.log(bySize.get('small').length); // 2
        """,
        lang="javascript",
        time="O(n)", space="O(n)",
        follow=[
            ("How would you count items per group instead of collecting them?", "Item জমানোর বদলে প্রতিটি group-এ কতগুলো item আছে, সেটা কীভাবে গুনবে?"),
            ("Why is `Object.groupBy` a static method instead of `Array.prototype.groupBy`?", "`Object.groupBy` কেন `Array.prototype.groupBy` না হয়ে static method হলো?"),
        ],
        related=["js-008", "js-013"],
        refs=[R_GROUPBY, R_MAPGROUPBY, R_REDUCE],
    ),
    # ------------------------------------------------------------------ js-013
    Q(
        id="js-013", sub="Array Methods", diff="easy", type="debugging",
        prio="high", market="both", mins=4,
        tags=["reduce", "arrow-functions", "debugging", "arrays"],
        ver="Version-independent concept (ECMAScript 2026)", vs=False, status="stable",
        q_en=r"""This code should print the cart total, `3800`, but it prints `undefined`. Find the bugs and fix them.""",
        q_bn=r"""এই code-এর cart total `3800` print করার কথা, কিন্তু print করছে `undefined`। Bug-গুলো খুঁজে বের করে ঠিক করো।""",
        code=r"""
            const cart = [
              { name: 'Keyboard', price: 1500, qty: 2 },
              { name: 'Mouse', price: 800, qty: 1 },
            ];

            const total = cart.reduce((sum, item) => {
              sum + item.price * item.qty;
            });

            console.log(total);
        """,
        lang="javascript",
        output=r"""undefined""",
        a_en=r"""
            There are two bugs:

            1. **Missing `return`.** The arrow function has a block body `{ ... }`, so the expression is calculated and thrown away — the callback returns `undefined`. Either add `return` or use a concise body without braces.
            2. **No initial value.** Without the second argument, `reduce` uses the **first item object** as the starting `sum` and starts looping from index 1. So even with `return`, the result would be `'[object Object]800'` (object + number → string). It also throws a `TypeError` for an empty cart.

            Fix: `cart.reduce((sum, item) => sum + item.price * item.qty, 0)` → `3800`.
        """,
        a_bn=r"""
            এখানে দুটো bug:

            1. **`return` নেই।** Arrow function-এর body block `{ ... }` আকারে, তাই expression-টা হিসাব হয়ে ফেলে দেওয়া হয় — callback `undefined` return করে। হয় `return` যোগ করো, নয়তো brace ছাড়া concise body ব্যবহার করো।
            2. **Initial value নেই।** দ্বিতীয় argument না দিলে `reduce` **প্রথম item object**-টাকেই শুরুর `sum` ধরে এবং index 1 থেকে loop শুরু করে। তাই `return` দিলেও ফল হতো `'[object Object]800'` (object + number → string)। আর cart খালি হলে `TypeError` throw হয়।

            Fix: `cart.reduce((sum, item) => sum + item.price * item.qty, 0)` → `3800`।
        """,
        ex_en=r"""
            Tracing the buggy version: no initial value → `sum = cart[0]` (the Keyboard object), loop starts at the Mouse. The callback runs once and returns `undefined`, so `total` is `undefined`.

            Edge cases worth mentioning:
            - Empty array without an initial value → `TypeError: Reduce of empty array with no initial value`.
            - Single-item array without an initial value → the callback **never runs** and `reduce` returns that item object as-is.
            - Always pass the initial value matching the result type (`0` for sums, `{}`/`Object.create(null)` for lookups, `[]` for arrays).

            Real-world note: for money, store amounts as integers in the smallest unit (paisa/cents) to avoid floating-point errors like `0.1 + 0.2`.
        """,
        ex_bn=r"""
            Buggy version trace করলে: initial value নেই → `sum = cart[0]` (Keyboard object), loop শুরু হয় Mouse থেকে। Callback একবার চলে আর `undefined` return করে, তাই `total` হয় `undefined`।

            যে edge case-গুলো বলা ভালো:
            - Initial value ছাড়া খালি array → `TypeError: Reduce of empty array with no initial value`।
            - Initial value ছাড়া এক item-এর array → callback **একবারও চলে না**, `reduce` ওই item object-টাই সরাসরি return করে।
            - সবসময় result-এর type অনুযায়ী initial value দাও (sum-এর জন্য `0`, lookup-এর জন্য `{}`/`Object.create(null)`, array-র জন্য `[]`)।

            বাস্তব পরামর্শ: টাকার হিসাবে amount-কে সবচেয়ে ছোট unit-এ (পয়সা/cents) integer হিসেবে রাখো, যাতে `0.1 + 0.2`-এর মতো floating-point ভুল না হয়।
        """,
        tip_en=r"""Point out *both* bugs even though fixing the first one seems enough — explaining what would happen with only the `return` fix (`'[object Object]800'`) shows you really understand `reduce`.""",
        tip_bn=r"""প্রথম bug ঠিক করলেই যথেষ্ট মনে হলেও *দুটো* bug-ই দেখাও — শুধু `return` ঠিক করলে কী হতো (`'[object Object]800'`) সেটা ব্যাখ্যা করলে বোঝা যায় তুমি `reduce` সত্যিই বোঝো।""",
        mist_en=r"""Adding `return` but still omitting the initial value, or "fixing" it with `map` + `forEach` and an outer mutable variable.""",
        mist_bn=r"""`return` যোগ করেও initial value না দেওয়া, অথবা `map` + `forEach` আর বাইরের একটা mutable variable দিয়ে "fix" করা।""",
        extra=[
            dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                const cart = [
                  { name: 'Keyboard', price: 1500, qty: 2 },
                  { name: 'Mouse', price: 800, qty: 1 },
                ];

                const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
                console.log(total); // 3800

                console.log([].reduce((sum, item) => sum + item.price * item.qty, 0)); // 0 — no crash
            """),
        ],
        follow=[
            ("When would you prefer a plain `for...of` loop over `reduce`?", "কখন `reduce`-এর বদলে সাধারণ `for...of` loop পছন্দ করবে?"),
            ("Why should money be stored as integers?", "টাকার পরিমাণ কেন integer হিসেবে রাখা উচিত?"),
        ],
        related=["js-007", "js-012", "js-006"],
        refs=[R_REDUCE, R_ARROW],
    ),
    # ------------------------------------------------------------------ js-014
    Q(
        id="js-014", sub="Immutability", diff="easy", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["immutability", "object-freeze", "shallow", "strict-mode"],
        ver="Version-independent concept (ES5+)", vs=False, status="stable",
        q_en=r"""A settings object is frozen and then one of its nested values is changed. What is logged?""",
        q_bn=r"""একটা settings object freeze করার পর তার একটা nested value বদলানো হলো। কী log হবে?""",
        code=r"""
            const settings = Object.freeze({
              theme: 'dark',
              api: { retries: 3 },
            });

            settings.api.retries = 5;
            console.log(Object.isFrozen(settings), settings.api.retries);
        """,
        lang="javascript",
        output=r"""true 5""",
        options=[
            ("`true 3`", "`true 3`"),
            ("`true 5`", "`true 5`"),
            ("`false 5`", "`false 5`"),
            ("A `TypeError` is thrown", "একটা `TypeError` throw হবে"),
        ],
        correct=1,
        a_en=r"""
            `true 5`. `Object.freeze` is **shallow**: the outer object is frozen (so `isFrozen` is `true`), but the nested `api` object is a separate, unfrozen object, so changing `settings.api.retries` works.
        """,
        a_bn=r"""
            `true 5`। `Object.freeze` **shallow**: বাইরের object freeze হয় (তাই `isFrozen` হলো `true`), কিন্তু ভেতরের `api` একটা আলাদা, freeze না করা object — তাই `settings.api.retries` বদলানো যায়।
        """,
        ex_en=r"""
            - Option A assumes freeze is deep — the most common misconception.
            - Option D is tempting if you know frozen writes throw in strict mode. That's true, but only for the frozen object's **own** properties: `settings.theme = 'light'` throws a `TypeError` in strict mode (ES modules, classes) and is silently ignored in sloppy scripts. Here we write to the unfrozen nested object, so nothing throws in either mode.
            - `const` is different again: it prevents **reassigning the variable**, not mutating the object.
            - For deep immutability, freeze recursively (a small `deepFreeze` helper) or, more commonly, follow an immutable-update discipline: never mutate, create new objects with spread (`{ ...s, api: { ...s.api, retries: 5 } }`), `toSorted`/`with` for arrays, or use a library like Immer.
            - Freezing has a cost on large objects; many teams freeze only in development to catch accidental mutation.
        """,
        ex_bn=r"""
            - Option A ধরে নেয় freeze deep — এটাই সবচেয়ে common ভুল ধারণা।
            - Option D লোভনীয় মনে হতে পারে যদি জানো যে strict mode-এ frozen object-এ লিখলে error হয়। কথাটা ঠিক, কিন্তু শুধু frozen object-এর **নিজস্ব** property-র জন্য: `settings.theme = 'light'` strict mode-এ (ES module, class) `TypeError` throw করে, আর sloppy script-এ চুপচাপ উপেক্ষিত হয়। এখানে আমরা freeze না করা nested object-এ লিখছি, তাই কোনো mode-এই error হয় না।
            - `const` আবার আলাদা জিনিস: এটা **variable reassign** আটকায়, object mutate করা নয়।
            - Deep immutability-র জন্য recursively freeze করো (ছোট একটা `deepFreeze` helper), অথবা বেশি প্রচলিত উপায়ে immutable update-এর নিয়ম মেনে চলো: কখনো mutate নয়, spread দিয়ে নতুন object (`{ ...s, api: { ...s.api, retries: 5 } }`), array-র জন্য `toSorted`/`with`, বা Immer-এর মতো library।
            - বড় object freeze করার একটা খরচ আছে; অনেক team শুধু development-এ freeze করে, যাতে ভুল করে mutate করলে ধরা পড়ে।
        """,
        tip_en=r"""Say "shallow" in your first sentence, then distinguish `const` vs `freeze` vs strict-mode behaviour. Offer the immutable-update pattern as the practical alternative.""",
        tip_bn=r"""প্রথম বাক্যেই "shallow" শব্দটা বলো, তারপর `const`, `freeze` আর strict-mode-এর আচরণ আলাদা করে বোঝাও। বাস্তব বিকল্প হিসেবে immutable update pattern-এর কথা বলো।""",
        follow=[
            ("Write a `deepFreeze` function.", "একটা `deepFreeze` function লেখো।"),
            ("What is the difference between `Object.freeze`, `Object.seal` and `Object.preventExtensions`?", "`Object.freeze`, `Object.seal` আর `Object.preventExtensions`-এর পার্থক্য কী?"),
        ],
        related=["js-009", "js-007"],
        refs=[R_FREEZE, R_ISFROZEN],
    ),
]

if __name__ == "__main__":
    save("javascript", "b2", QUESTIONS)
