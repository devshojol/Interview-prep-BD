# React — batch 1 (react-001..004, 012, 013, 023, 030)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_JSX = ("react.dev — Writing Markup with JSX", "https://react.dev/learn/writing-markup-with-jsx")
R_JSX_CURLY = ("react.dev — JavaScript in JSX with Curly Braces", "https://react.dev/learn/javascript-in-jsx-with-curly-braces")
R_PROPS = ("react.dev — Passing Props to a Component", "https://react.dev/learn/passing-props-to-a-component")
R_STATE = ("react.dev — State: A Component's Memory", "https://react.dev/learn/state-a-components-memory")
R_SHARE = ("react.dev — Sharing State Between Components", "https://react.dev/learn/sharing-state-between-components")
R_QUEUE = ("react.dev — Queueing a Series of State Updates", "https://react.dev/learn/queueing-a-series-of-state-updates")
R_USESTATE = ("react.dev — useState", "https://react.dev/reference/react/useState")
R_LISTS = ("react.dev — Rendering Lists", "https://react.dev/learn/rendering-lists")
R_PRESERVE = ("react.dev — Preserving and Resetting State", "https://react.dev/learn/preserving-and-resetting-state")
R_STRICT = ("react.dev — StrictMode", "https://react.dev/reference/react/StrictMode")
R_USEEFFECT = ("react.dev — useEffect", "https://react.dev/reference/react/useEffect")
R_SYNC = ("react.dev — Synchronizing with Effects", "https://react.dev/learn/synchronizing-with-effects")
R_EFFECT_EVENT = ("react.dev — useEffectEvent", "https://react.dev/reference/react/useEffectEvent")
R_RENDER_COMMIT = ("react.dev — Render and Commit", "https://react.dev/learn/render-and-commit")
R_CTX = ("react.dev — createContext", "https://react.dev/reference/react/createContext")
R_USEID = ("react.dev — useId", "https://react.dev/reference/react/useId")
R_COMPILER = ("react.dev — React Compiler v1.0", "https://react.dev/blog/2025/10/07/react-compiler-1")

QUESTIONS = [
    # ------------------------------------------------------------------ react-001
    Q(
        id="react-001", sub="Components and JSX", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["jsx", "components", "react-element", "jsx-runtime"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What is JSX, and what does it compile to?""",
        q_bn=r"""JSX কী, আর এটা compile হয়ে কী-তে পরিণত হয়?""",
        a_en=r"""
            JSX is a syntax extension that lets you write HTML-like markup inside JavaScript. Browsers can't run it directly, so a compiler (Babel, SWC, esbuild or TypeScript) turns every tag into a function call. With the modern **automatic JSX runtime**, `<h1 className="title">Hi</h1>` becomes roughly `jsx("h1", { className: "title", children: "Hi" })`, imported automatically from `react/jsx-runtime`.

            That call returns a **React element** — a plain, lightweight object that *describes* the UI. It is not a DOM node. React later compares these descriptions and updates the real DOM.

            A component is just a function that returns JSX. Lowercase tags (`div`) are DOM elements; capitalised names (`UserCard`) are components.
        """,
        a_bn=r"""
            JSX হলো একটা syntax extension, যেটা দিয়ে JavaScript-এর ভেতরেই HTML-এর মতো markup লেখা যায়। Browser সরাসরি JSX চালাতে পারে না, তাই একটা compiler (Babel, SWC, esbuild বা TypeScript) প্রতিটা tag-কে function call-এ রূপান্তর করে। আধুনিক **automatic JSX runtime**-এ `<h1 className="title">Hi</h1>` মোটামুটি `jsx("h1", { className: "title", children: "Hi" })` হয়ে যায়, আর `react/jsx-runtime` থেকে এটা নিজে থেকেই import হয়।

            এই call একটা **React element** return করে — একটা সাধারণ, হালকা object যেটা UI দেখতে কেমন হবে তার *বর্ণনা* দেয়। এটা DOM node নয়। পরে React এই বর্ণনাগুলো তুলনা করে আসল DOM update করে।

            Component হলো এমন একটা function যেটা JSX return করে। ছোট হাতের tag (`div`) মানে DOM element, আর বড় হাতের নাম (`UserCard`) মানে component।
        """,
        quick_en=r"""JSX is HTML-like syntax inside JavaScript that a compiler (Babel, SWC, TypeScript) turns into function calls like `jsx("h1", props)` from `react/jsx-runtime`. Each call returns a React element, a plain object that describes the UI, not a real DOM node.""",
        quick_bn=r"""JSX হলো JavaScript-এর ভেতরে HTML-এর মতো syntax, যেটাকে compiler (Babel, SWC, TypeScript) `react/jsx-runtime`-এর `jsx("h1", props)`-এর মতো function call-এ বদলে দেয়। প্রতিটা call একটা React element return করে, যেটা UI-এর বর্ণনা দেওয়া একটা সাধারণ object, আসল DOM node না।""",
        ex_en=r"""
            - **Why no `import React`?** Since the automatic runtime (React 17+), the compiler injects the `react/jsx-runtime` import, so you don't need `React` in scope just for JSX.
            - **Rules:** return a single root (use a Fragment `<>...</>` if needed), close every tag (`<img />`), use camelCase attributes (`className`, `htmlFor`, `onClick`, `tabIndex`).
            - **Curly braces take expressions, not statements:** use a ternary, `&&` or `.map()` instead of `if`/`for` inside JSX.
            - **Escaping:** strings in `{}` are escaped automatically, which protects against XSS. Only `dangerouslySetInnerHTML` bypasses this.
            - **Gotcha:** `{items.length && <List />}` renders `0` when the list is empty, because `0` is a valid React child. Use `items.length > 0 && ...`.
        """,
        ex_bn=r"""
            - **কেন `import React` লাগে না?** Automatic runtime (React 17+) থেকে compiler নিজেই `react/jsx-runtime` import যোগ করে দেয়, তাই শুধু JSX-এর জন্য scope-এ `React` রাখার দরকার নেই।
            - **নিয়ম:** একটাই root element return করতে হয় (দরকার হলে Fragment `<>...</>`), প্রতিটা tag বন্ধ করতে হয় (`<img />`), আর attribute camelCase-এ লিখতে হয় (`className`, `htmlFor`, `onClick`, `tabIndex`)।
            - **Curly brace-এ expression চলে, statement না:** JSX-এর ভেতরে `if`/`for`-এর বদলে ternary, `&&` বা `.map()` ব্যবহার করো।
            - **Escaping:** `{}`-এর ভেতরের string নিজে থেকেই escape হয়, ফলে XSS থেকে সুরক্ষা পাওয়া যায়। শুধু `dangerouslySetInnerHTML` এই সুরক্ষা bypass করে।
            - **Gotcha:** list খালি হলে `{items.length && <List />}` স্ক্রিনে `0` দেখায়, কারণ `0` একটা valid React child। এর বদলে `items.length > 0 && ...` লেখো।
        """,
        tip_en=r"""Say "JSX compiles to function calls that return plain objects (React elements)". Then mention the automatic runtime and one gotcha like the `0 &&` bug — it shows hands-on experience.""",
        tip_bn=r"""বলো "JSX compile হয়ে function call হয়, যেটা সাধারণ object (React element) return করে"। এরপর automatic runtime আর `0 &&` bug-এর মতো একটা gotcha উল্লেখ করো — এতে বোঝা যায় তোমার হাতে-কলমে অভিজ্ঞতা আছে।""",
        mist_en=r"""Saying JSX is "HTML inside JavaScript" or that it creates DOM nodes directly. JSX creates element objects; React DOM creates and updates the real nodes.""",
        mist_bn=r"""JSX-কে "JavaScript-এর ভেতরে HTML" বলা, বা বলা যে এটা সরাসরি DOM node তৈরি করে। আসলে JSX element object তৈরি করে; আসল node তৈরি ও update করে React DOM।""",
        code=r"""
            // What you write
            function Greeting({ name }) {
              return <h1 className="title">Hello, {name}</h1>;
            }

            // Roughly what the compiler emits (automatic runtime)
            // (jsxs = the variant used for several static children)
            import { jsxs as _jsxs } from 'react/jsx-runtime';

            function Greeting({ name }) {
              return _jsxs('h1', { className: 'title', children: ['Hello, ', name] });
            }
        """,
        lang="jsx",
        follow=[
            ("Why must component names start with a capital letter?", "Component-এর নাম কেন বড় হাতের অক্ষর দিয়ে শুরু করতে হয়?"),
            ("How does JSX help prevent XSS, and when does that protection not apply?", "JSX কীভাবে XSS ঠেকাতে সাহায্য করে, আর কখন এই সুরক্ষা কাজ করে না?"),
        ],
        refs=[R_JSX, R_JSX_CURLY],
    ),
    # ------------------------------------------------------------------ react-002
    Q(
        id="react-002", sub="Props and State", diff="easy", type="comparison",
        prio="high", market="both", mins=3,
        tags=["props", "state", "data-flow", "lifting-state"],
        ver="Version-independent concept (React 19.3)", vs=False, status="stable",
        q_en=r"""What is the difference between props and state in React?""",
        q_bn=r"""React-এ props আর state-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""
            **Props** are inputs a parent passes to a child, like function arguments. The child must treat them as read-only. **State** is data a component owns and changes over time with its setter (`setCount`); updating state schedules a re-render of that component and its children.

            Data flows one way: down through props. If a child needs to change parent data, the parent passes a callback prop (`onChange`) and keeps the state itself — this is called **lifting state up**.

            My rule: if a value can be calculated from props or other state, it shouldn't be state at all — I compute it during render.
        """,
        a_bn=r"""
            **Props** হলো parent থেকে child-এ পাঠানো input, অনেকটা function argument-এর মতো। Child-কে এগুলো read-only হিসেবে ব্যবহার করতে হয়। **State** হলো component-এর নিজের data, যেটা সময়ের সাথে setter (`setCount`) দিয়ে বদলায়; state update করলে ওই component আর তার children-এর re-render schedule হয়।

            Data একদিকে প্রবাহিত হয়: props দিয়ে নিচের দিকে। Child যদি parent-এর data বদলাতে চায়, parent একটা callback prop (`onChange`) পাঠায় আর state নিজের কাছেই রাখে — একে বলে **lifting state up**।

            আমার নিয়ম: কোনো value যদি props বা অন্য state থেকে হিসাব করে বের করা যায়, তাহলে সেটা state-এ রাখাই উচিত না — আমি render-এর সময়ই সেটা compute করি।
        """,
        quick_en=r"""Props are read-only inputs a parent passes to a child, like function arguments. State is data a component owns and changes with its setter, and changing it re-renders the component. Data flows down through props; a child changes parent data through a callback prop.""",
        quick_bn=r"""Props হলো parent থেকে child-এ পাঠানো read-only input, অনেকটা function argument-এর মতো। State হলো component-এর নিজের data, setter দিয়ে বদলায়, আর বদলালে component re-render হয়। Data props দিয়ে নিচে নামে; child-কে parent-এর data বদলাতে হলে callback prop ব্যবহার করে।""",
        ex_en=r"""
            - **Owner:** props are owned by the parent; state is owned by the component that declares it.
            - **Mutability:** never mutate props (`props.user.name = 'x'` is a bug). State changes only through the setter with a new value.
            - **Re-render trigger:** a state change re-renders the owner; new props arrive because the parent re-rendered.
            - **Copying props into state** (`useState(props.color)`) only uses the *initial* value — later prop changes are ignored. If that's intended, name it `initialColor`; if not, read the prop directly. To reset a child's state when an id changes, give it a `key`.
        """,
        ex_bn=r"""
            - **মালিক কে:** props-এর মালিক parent; state-এর মালিক যে component সেটা declare করে।
            - **পরিবর্তন:** props কখনো mutate করবে না (`props.user.name = 'x'` একটা bug)। State শুধু setter দিয়ে নতুন value দিয়ে বদলায়।
            - **Re-render কখন হয়:** state বদলালে owner component re-render হয়; parent re-render হলে child নতুন props পায়।
            - **Props-কে state-এ copy করা** (`useState(props.color)`) শুধু *প্রথম* value নেয় — পরে prop বদলালেও state বদলায় না। এটা ইচ্ছাকৃত হলে নাম দাও `initialColor`; না হলে সরাসরি prop পড়ো। কোনো id বদলালে child-এর state reset করতে চাইলে তাকে একটা `key` দাও।
        """,
        tip_en=r"""Structure it as a quick comparison (owner, mutability, what triggers re-render), then add "lifting state up" and "derived values shouldn't be state" — those two points separate juniors from strong candidates.""",
        tip_bn=r"""ছোট একটা তুলনা দিয়ে শুরু করো (মালিক, mutability, কী কারণে re-render হয়), তারপর "lifting state up" আর "derived value state-এ রাখা উচিত না" — এই দুইটা পয়েন্ট বললে তুমি সাধারণ junior-দের থেকে আলাদা হয়ে যাবে।""",
        mist_en=r"""Storing derived data (e.g. `fullName`, filtered lists) in state and syncing it with effects, which causes extra renders and out-of-sync bugs.""",
        mist_bn=r"""Derived data (যেমন `fullName` বা filter করা list) state-এ রেখে effect দিয়ে sync করা — এতে বাড়তি render হয় আর data মিলিয়ে না যাওয়ার bug তৈরি হয়।""",
        code=r"""
            import { useState } from 'react';

            function Stepper({ value, onIncrement }) {
              // value and onIncrement are props: read-only here
              return <button onClick={onIncrement}>Count: {value}</button>;
            }

            export default function App() {
              const [count, setCount] = useState(0); // state lives in the parent
              const isEven = count % 2 === 0;         // derived, not state

              return (
                <>
                  <Stepper value={count} onIncrement={() => setCount((c) => c + 1)} />
                  <p>{isEven ? 'Even' : 'Odd'}</p>
                </>
              );
            }
        """,
        lang="jsx",
        follow=[
            ("When would you lift state up versus use Context?", "কখন lifting state up করবে আর কখন Context ব্যবহার করবে?"),
            ("Why is `useState(props.value)` often a bug?", "`useState(props.value)` প্রায়ই কেন bug তৈরি করে?"),
        ],
        refs=[R_PROPS, R_STATE, R_SHARE],
    ),
    # ------------------------------------------------------------------ react-003
    Q(
        id="react-003", sub="useState", diff="easy", type="output",
        prio="high", market="bangladesh", mins=3,
        tags=["usestate", "batching", "updater-function", "snapshot"],
        ver="React 19.3 (automatic batching since React 18)", vs=True, status="stable",
        q_en=r"""
            The component below renders once and then the button is clicked **once**. Assume a production build without StrictMode. What is logged to the console, and what number does the button show after the click?
        """,
        q_bn=r"""
            নিচের component একবার render হলো, তারপর button-এ **একবার** click করা হলো। ধরে নাও এটা production build, StrictMode নেই। Console-এ কী log হবে, আর click-এর পর button-এ কোন সংখ্যা দেখাবে?
        """,
        a_en=r"""
            The console shows `render: 0`, then `clicked: 0`, then `render: 2`. The button shows **2**.

            `count` is a snapshot: during this render it is `0`, so both `setCount(count + 1)` calls queue "replace with 1". The updater `setCount(c => c + 1)` receives the queued value `1` and returns `2`. The `console.log` inside the handler still sees the old snapshot `0`, because state only changes in the *next* render. React batches all three updates into a single re-render, so `render` is logged only once more.
        """,
        a_bn=r"""
            Console-এ প্রথমে `render: 0`, তারপর `clicked: 0`, তারপর `render: 2` আসবে। Button-এ দেখাবে **2**।

            `count` হলো একটা snapshot: এই render-এ এর মান `0`, তাই দুটো `setCount(count + 1)` call-ই "1 দিয়ে replace করো" queue করে। Updater `setCount(c => c + 1)` queue-তে থাকা `1` পায় আর `2` return করে। Handler-এর ভেতরের `console.log` তখনো পুরনো snapshot `0` দেখে, কারণ state বদলায় শুধু *পরের* render-এ। React তিনটা update batch করে একটাই re-render করে, তাই `render` আর মাত্র একবার log হয়।
        """,
        quick_en=r"""It logs `render: 0`, `clicked: 0`, `render: 2`, and the button shows 2. `count` is a snapshot (0), so both `setCount(count + 1)` queue 1, the updater turns that into 2, and React batches all three into one re-render.""",
        quick_bn=r"""Log হবে `render: 0`, `clicked: 0`, `render: 2`, আর button-এ দেখাবে 2। `count` একটা snapshot (0), তাই দুইটা `setCount(count + 1)`-ই 1 queue করে, updater সেটাকে 2 বানায়, আর React তিনটা update মিলিয়ে একবারই re-render করে।""",
        ex_en=r"""
            Step by step:

            1. Initial render logs `render: 0`.
            2. Click → `setCount(0 + 1)` queues *replace with 1*.
            3. `setCount(0 + 1)` again queues *replace with 1* (still 1).
            4. `setCount(c => c + 1)` queues an updater: 1 → 2.
            5. `console.log('clicked:', count)` prints the snapshot `0`.
            6. The event handler finishes, React processes the queue once (automatic batching) and re-renders with `count = 2` → `render: 2`.

            If all three calls used the updater form, the result would be 3. Use the updater whenever the new state depends on the previous state, especially for multiple updates in one event or in async callbacks.
        """,
        ex_bn=r"""
            ধাপে ধাপে:

            1. প্রথম render-এ `render: 0` log হয়।
            2. Click → `setCount(0 + 1)` queue করে *1 দিয়ে replace*।
            3. আবার `setCount(0 + 1)` → আবারও *1 দিয়ে replace* (এখনো 1)।
            4. `setCount(c => c + 1)` একটা updater queue করে: 1 → 2।
            5. `console.log('clicked:', count)` snapshot `0` print করে।
            6. Event handler শেষ হলে React একবারেই পুরো queue process করে (automatic batching) আর `count = 2` দিয়ে re-render করে → `render: 2`।

            তিনটা call-ই যদি updater form-এ হতো, ফল হতো 3। নতুন state আগের state-এর উপর নির্ভর করলে updater ব্যবহার করো, বিশেষ করে একই event-এ একাধিক update বা async callback-এর ভেতরে।
        """,
        tip_en=r"""Walk through the queue line by line out loud. Use the words "snapshot", "queue" and "batching" — interviewers listen for exactly those concepts.""",
        tip_bn=r"""Queue-টা লাইন ধরে ধরে মুখে ব্যাখ্যা করো। "snapshot", "queue" আর "batching" শব্দগুলো ব্যবহার করো — interviewer ঠিক এই ধারণাগুলোই শুনতে চায়।""",
        mist_en=r"""Answering 3 (assuming each call sees the updated value), or expecting `clicked:` to print the new value immediately after calling the setter.""",
        mist_bn=r"""উত্তর 3 বলা (ভাবা যে প্রতিটা call update হওয়া value দেখে), অথবা setter call করার সাথে সাথে `clicked:` নতুন value print করবে বলে আশা করা।""",
        code=r"""
            import { useState } from 'react';

            export default function Counter() {
              const [count, setCount] = useState(0);

              function handleClick() {
                setCount(count + 1);
                setCount(count + 1);
                setCount((c) => c + 1);
                console.log('clicked:', count);
              }

              console.log('render:', count);
              return <button onClick={handleClick}>{count}</button>;
            }
        """,
        lang="jsx",
        output=r"""
            render: 0
            clicked: 0
            render: 2
            (button shows 2)
        """,
        follow=[
            ("What would change if all three calls used the updater form?", "তিনটা call-ই updater form-এ হলে কী বদলাত?"),
            ("Are updates inside `setTimeout` or a resolved promise also batched in React 18+?", "React 18+-এ `setTimeout` বা resolved promise-এর ভেতরের update-ও কি batch হয়?"),
        ],
        refs=[R_QUEUE, R_USESTATE],
    ),
    # ------------------------------------------------------------------ react-004
    Q(
        id="react-004", sub="Keys", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["keys", "lists", "reconciliation"],
        ver="Version-independent concept (React 19.3)", vs=False, status="stable",
        q_en=r"""You render a todo list where users can add, delete and reorder items. Which `key` should each `<TodoItem>` get?""",
        q_bn=r"""তুমি একটা todo list render করছ, যেখানে user item যোগ, মুছে ফেলা আর reorder করতে পারে। প্রতিটা `<TodoItem>`-কে কোন `key` দেওয়া উচিত?""",
        options=[
            ("The array index: `key={index}`", "Array-এর index: `key={index}`"),
            ("A stable unique id from the data: `key={todo.id}`", "Data থেকে পাওয়া স্থায়ী unique id: `key={todo.id}`"),
            ("A random value: `key={Math.random()}`", "একটা random value: `key={Math.random()}`"),
            ("No key — React generates keys automatically for lists", "কোনো key না — list-এর জন্য React নিজেই key তৈরি করে নেয়"),
        ],
        correct=1,
        a_en=r"""Use a stable, unique id from the data, such as `todo.id`. Keys tell React which item is which between renders, so state, focus and DOM nodes stay attached to the right item when the list changes.""",
        a_bn=r"""Data থেকে পাওয়া স্থায়ী, unique id ব্যবহার করো, যেমন `todo.id`। Key দিয়ে React বুঝতে পারে কোন item কোনটা, ফলে list বদলালেও state, focus আর DOM node সঠিক item-এর সাথেই থাকে।""",
        quick_en=r"""Use a stable unique id from the data, `key={todo.id}`. Keys tell React which item is which between renders, so state, focus and DOM nodes stay with the right item when items are added, deleted or reordered.""",
        quick_bn=r"""Data থেকে আসা স্থায়ী unique id ব্যবহার করো, `key={todo.id}`। Key দিয়ে React বোঝে কোন item কোনটা, তাই item যোগ, delete বা reorder হলেও state, focus আর DOM node ঠিক item-এর সাথেই থাকে।""",
        ex_en=r"""
            The tempting wrong answer is the **index**: it removes the warning and works for static lists, but when you insert, delete or reorder, the indexes shift. React then reuses the wrong component instance, so an input's text or a checkbox's checked state "jumps" to a different row.

            `Math.random()` is worse: every render produces new keys, so React unmounts and remounts every item — you lose state and focus, and performance drops. Omitting the key makes React fall back to the index and log a warning. Keys only need to be unique among siblings, and they are not passed to the component as a prop. If the data has no id, generate one when the item is *created* (e.g. `crypto.randomUUID()`), not during render.
        """,
        ex_bn=r"""
            সবচেয়ে লোভনীয় ভুল উত্তর হলো **index**: এতে warning চলে যায় আর static list-এ ঠিকঠাক চলে, কিন্তু item যোগ, মুছে ফেলা বা reorder করলে index সরে যায়। তখন React ভুল component instance আবার ব্যবহার করে, ফলে কোনো input-এর লেখা বা checkbox-এর checked অবস্থা অন্য row-তে "লাফিয়ে" চলে যায়।

            `Math.random()` আরও খারাপ: প্রতিটা render-এ নতুন key তৈরি হয়, ফলে React প্রতিটা item unmount করে আবার mount করে — state আর focus হারায়, performance-ও কমে। Key না দিলে React index ব্যবহার করে আর warning দেয়। Key শুধু sibling-দের মধ্যে unique হলেই চলে, আর এটা component-এ prop হিসেবে যায় না। Data-তে id না থাকলে item *তৈরির সময়* একটা id বানাও (যেমন `crypto.randomUUID()`), render-এর সময় না।
        """,
        tip_en=r"""Explain *what keys are for* (identity across renders), then give the concrete index-key bug with input fields. That example is what interviewers want to hear.""",
        tip_bn=r"""আগে বলো key *কী কাজে লাগে* (render-এর মধ্যে identity ধরে রাখা), তারপর input field-সহ index-key bug-এর বাস্তব উদাহরণ দাও। Interviewer ঠিক এই উদাহরণটাই শুনতে চায়।""",
        refs=[R_LISTS, R_PRESERVE],
    ),
    # ------------------------------------------------------------------ react-012
    Q(
        id="react-012", sub="Stale Closures", diff="medium", type="output",
        prio="high", market="both", mins=5,
        tags=["stale-closure", "setinterval", "useeffect", "useeffectevent"],
        ver="React 19.3 (useEffectEvent stable since 19.2)", vs=True, status="stable",
        q_en=r"""
            The `Timer` component mounts and stays on screen for about **3.5 seconds**. What is logged, what number is on the screen, and why? How would you fix it?
        """,
        q_bn=r"""
            `Timer` component mount হয়ে প্রায় **3.5 সেকেন্ড** স্ক্রিনে থাকল। কী log হবে, স্ক্রিনে কোন সংখ্যা দেখাবে, আর কেন? তুমি এটা কীভাবে ঠিক করবে?
        """,
        a_en=r"""
            It logs `tick 0` three times and the screen shows **1** forever.

            The effect runs once (empty dependency array), so the interval callback is a **closure over the first render**, where `count` is `0`. Every tick calls `setCount(0 + 1)`, which sets `1` again and again — after the first tick React sees the same value and nothing changes.

            Fixes:
            - Use the updater form `setCount(c => c + 1)`, which doesn't need the closed-over value.
            - To *read* the latest value inside the interval (e.g. for logging), wrap that logic in `useEffectEvent` (stable since React 19.2) or keep it in a ref.
            - Adding `count` to the dependency array also works, but it clears and recreates the interval on every tick.
        """,
        a_bn=r"""
            তিনবার `tick 0` log হবে, আর স্ক্রিনে সবসময় **1** দেখাবে।

            Effect-টা একবারই চলে (dependency array খালি), তাই interval callback হলো **প্রথম render-এর closure**, যেখানে `count`-এর মান `0`। প্রতিটা tick-এ `setCount(0 + 1)` call হয়, অর্থাৎ বারবার `1` set হয় — প্রথম tick-এর পর React একই value দেখে, কিছুই বদলায় না।

            সমাধান:
            - Updater form `setCount(c => c + 1)` ব্যবহার করো, এতে closure-এর পুরনো value লাগে না।
            - Interval-এর ভেতরে সর্বশেষ value *পড়তে* চাইলে (যেমন log করার জন্য) সেই logic `useEffectEvent`-এ রাখো (React 19.2 থেকে stable) অথবা ref-এ রাখো।
            - Dependency array-তে `count` দিলেও কাজ হয়, কিন্তু তখন প্রতিটা tick-এ interval clear হয়ে নতুন করে তৈরি হয়।
        """,
        quick_en=r"""It logs `tick 0` three times and the screen stays at 1. The effect runs once, so the interval closes over the first render where `count` is 0 and keeps setting 1; fix it with the updater `setCount(c => c + 1)`.""",
        quick_bn=r"""`tick 0` তিনবার log হয় আর screen-এ 1-ই থেকে যায়। Effect একবারই চলে, তাই interval প্রথম render-এর closure ধরে রাখে যেখানে `count` 0, আর বারবার 1 set করে; সমাধান হলো updater `setCount(c => c + 1)`।""",
        ex_en=r"""
            Each render has its own props, state and functions. A function created in render 1 "remembers" render 1's values forever — that's a normal JavaScript closure, not a React bug. The problem appears when a long-lived callback (interval, subscription, WebSocket handler) is created once and never refreshed.

            Timeline: mount → effect creates the interval with `count = 0`. At 1s it logs `tick 0` and sets 1 → re-render shows 1. At 2s and 3s the same old closure logs `tick 0` and sets 1 again, so React bails out.

            In development with StrictMode, the effect runs setup → cleanup → setup, but the cleanup clears the first interval, so the visible behaviour is the same. The fixed version uses the updater for state and `useEffectEvent` for the "non-reactive" logging logic, so the effect still subscribes only once.
        """,
        ex_bn=r"""
            প্রতিটা render-এর নিজস্ব props, state আর function থাকে। Render 1-এ তৈরি হওয়া function চিরকাল render 1-এর value "মনে রাখে" — এটা সাধারণ JavaScript closure, React-এর bug না। সমস্যা হয় যখন দীর্ঘস্থায়ী callback (interval, subscription, WebSocket handler) একবার তৈরি হয় আর কখনো refresh হয় না।

            Timeline: mount → effect `count = 0` দিয়ে interval তৈরি করে। 1s-এ `tick 0` log হয় আর 1 set হয় → re-render-এ 1 দেখায়। 2s আর 3s-এ সেই পুরনো closure আবার `tick 0` log করে আর আবার 1 set করে, তাই React কিছু বদলায় না।

            Development-এ StrictMode থাকলে effect setup → cleanup → setup হয়, কিন্তু cleanup প্রথম interval clear করে দেয়, তাই দৃশ্যমান আচরণ একই থাকে। সংশোধিত version-এ state-এর জন্য updater আর "non-reactive" logging logic-এর জন্য `useEffectEvent` ব্যবহার করা হয়েছে, ফলে effect এখনো মাত্র একবার subscribe করে।
        """,
        tip_en=r"""Say the word "closure" early and explain *which render* the callback belongs to. Offering two fixes with their trade-offs (updater vs dependency array vs `useEffectEvent`) shows senior-level thinking.""",
        tip_bn=r"""শুরুতেই "closure" শব্দটা বলো, আর ব্যাখ্যা করো callback-টা *কোন render*-এর। Trade-off-সহ একাধিক সমাধান দিলে (updater বনাম dependency array বনাম `useEffectEvent`) senior-level চিন্তা বোঝা যায়।""",
        mist_en=r"""Silencing the exhaustive-deps lint rule instead of fixing the closure, or thinking the screen keeps counting up because the interval keeps firing.""",
        mist_bn=r"""Closure ঠিক না করে exhaustive-deps lint rule বন্ধ করে দেওয়া, অথবা ভাবা যে interval চলছে বলে স্ক্রিনের সংখ্যা বাড়তেই থাকবে।""",
        code=r"""
            import { useEffect, useState } from 'react';

            export default function Timer() {
              const [count, setCount] = useState(0);

              useEffect(() => {
                const id = setInterval(() => {
                  console.log('tick', count);
                  setCount(count + 1);
                }, 1000);
                return () => clearInterval(id);
              }, []);

              return <p>{count}</p>;
            }
        """,
        lang="jsx",
        output=r"""
            tick 0
            tick 0
            tick 0
            (screen shows: 1)
        """,
        extra=[dict(lang="jsx", label_en="Fixed version (React 19.2+)", label_bn="সংশোধিত version (React 19.2+)", src=r"""
            import { useEffect, useEffectEvent, useState } from 'react';

            export default function Timer() {
              const [count, setCount] = useState(0);

              // Always sees the latest committed `count`, but is not a dependency
              const onTick = useEffectEvent(() => {
                console.log('tick', count);
              });

              useEffect(() => {
                const id = setInterval(() => {
                  onTick();
                  setCount((c) => c + 1); // updater: no stale value needed
                }, 1000);
                return () => clearInterval(id);
              }, []);

              return <p>{count}</p>;
            }
        """)],
        follow=[
            ("Why must a `useEffectEvent` function not be added to the dependency array or passed to children?", "`useEffectEvent` function কেন dependency array-তে দেওয়া বা child-এ পাঠানো যাবে না?"),
            ("How would you solve the same problem with `useRef` in older React versions?", "পুরনো React version-এ একই সমস্যা `useRef` দিয়ে কীভাবে সমাধান করবে?"),
        ],
        related=["react-003"],
        refs=[R_EFFECT_EVENT, R_QUEUE, R_SYNC],
    ),
    # ------------------------------------------------------------------ react-013
    Q(
        id="react-013", sub="Effects and Cleanup", diff="medium", type="output",
        prio="high", market="both", mins=4,
        tags=["strictmode", "useeffect", "cleanup", "render-order"],
        ver="React 19.3", vs=True, status="stable",
        q_en=r"""
            What does the console show on the **first mount in development**? What is different in a **production** build, and why does React behave this way?
        """,
        q_bn=r"""
            **Development-এ প্রথম mount**-এর সময় console-এ কী দেখাবে? **Production** build-এ কী আলাদা হবে, আর React কেন এমন আচরণ করে?
        """,
        a_en=r"""
            In development with `<StrictMode>` the log is: `render Rahim`, `render Rahim`, `effect: subscribe`, `cleanup: unsubscribe`, `effect: subscribe`. In production it is just `render Rahim` and `effect: subscribe`.

            StrictMode does two extra checks in development only:
            - It calls the component function **twice** to catch impure rendering (side effects in render).
            - After mounting, it runs every effect's **cleanup and setup one extra time**, simulating unmount + remount, to catch effects that are missing a cleanup.

            If your app breaks under this (double subscriptions, two API calls with conflicting results), the bug is real — it would also show up when the user navigates away and back, or with features like `<Activity>`.
        """,
        a_bn=r"""
            Development-এ `<StrictMode>` থাকলে log হবে: `render Rahim`, `render Rahim`, `effect: subscribe`, `cleanup: unsubscribe`, `effect: subscribe`। Production-এ শুধু `render Rahim` আর `effect: subscribe`।

            StrictMode শুধু development-এ দুটো বাড়তি check করে:
            - Impure rendering (render-এর ভেতরে side effect) ধরার জন্য component function **দুইবার** call করে।
            - Mount হওয়ার পর প্রতিটা effect-এর **cleanup আর setup একবার বাড়তি** চালায় — unmount + remount simulate করে, যাতে cleanup ছাড়া effect ধরা পড়ে।

            এতে যদি তোমার app ভেঙে যায় (double subscription, দুটো API call-এর conflicting result), তাহলে bug-টা আসল — user অন্য page-এ গিয়ে ফিরে এলে বা `<Activity>`-এর মতো feature-এও এটা দেখা দিত।
        """,
        quick_en=r"""In development with StrictMode: `render Rahim` twice, then `effect: subscribe`, `cleanup: unsubscribe`, `effect: subscribe`; in production just one render and one subscribe. StrictMode double-renders and re-runs effects in dev only, to expose impure renders and missing cleanups.""",
        quick_bn=r"""Development-এ StrictMode থাকলে: `render Rahim` দুইবার, তারপর `effect: subscribe`, `cleanup: unsubscribe`, `effect: subscribe`; production-এ শুধু একবার render আর একবার subscribe। StrictMode শুধু dev-এ দুইবার render করে আর effect আবার চালায়, যাতে impure render আর missing cleanup ধরা পড়ে।""",
        ex_en=r"""
            Order of events on mount: React renders (twice in StrictMode — both renders happen before anything is committed), commits the DOM, then runs effects. StrictMode then calls the cleanup and the setup again. Your effect should be **symmetrical**: whatever setup does (subscribe, connect, add listener), cleanup undoes.

            Notes:
            - React DevTools can show the second render's `console.log` dimmed; without DevTools you see both lines.
            - Don't "fix" the double effect with a `useRef` flag to run only once. Fix the cleanup instead, or move one-off app initialisation outside components.
            - For data fetching, the dev-only double request is harmless if you ignore/abort the stale response in cleanup — or use a framework or a data library that caches requests.
        """,
        ex_bn=r"""
            Mount-এর সময় ঘটনার ক্রম: React render করে (StrictMode-এ দুইবার — দুটো render-ই commit-এর আগে হয়), DOM commit করে, তারপর effect চালায়। এরপর StrictMode আবার cleanup আর setup call করে। তোমার effect হওয়া উচিত **symmetrical**: setup যা করে (subscribe, connect, listener যোগ), cleanup ঠিক সেটাই undo করে।

            কিছু নোট:
            - React DevTools দ্বিতীয় render-এর `console.log` হালকা রঙে (dimmed) দেখাতে পারে; DevTools ছাড়া দুটো লাইনই দেখবে।
            - শুধু একবার চালানোর জন্য `useRef` flag দিয়ে double effect "ঠিক" করো না। বরং cleanup ঠিক করো, অথবা এককালীন app initialization component-এর বাইরে নিয়ে যাও।
            - Data fetching-এর ক্ষেত্রে cleanup-এ পুরনো response ignore/abort করলে dev-only double request ক্ষতিকর না — অথবা এমন framework বা data library ব্যবহার করো যেটা request cache করে।
        """,
        tip_en=r"""Give the exact sequence first, then explain *why* StrictMode does it ("it's a dev-only stress test for missing cleanups"). Mentioning that production runs once avoids the common panic about duplicate API calls.""",
        tip_bn=r"""প্রথমে সঠিক ক্রমটা বলো, তারপর ব্যাখ্যা করো StrictMode *কেন* এটা করে ("এটা missing cleanup ধরার জন্য dev-only stress test")। Production-এ একবারই চলে — এটা বললে duplicate API call নিয়ে সাধারণ দুশ্চিন্তাটা দূর হয়।""",
        mist_en=r"""Removing StrictMode to "fix" double effects, or believing the effect runs twice in production too.""",
        mist_bn=r"""Double effect "ঠিক" করতে StrictMode সরিয়ে দেওয়া, অথবা ভাবা যে production-এও effect দুইবার চলে।""",
        code=r"""
            import { StrictMode, useEffect, useState } from 'react';
            import { createRoot } from 'react-dom/client';

            function Profile() {
              const [name] = useState('Rahim');
              console.log('render', name);

              useEffect(() => {
                console.log('effect: subscribe');
                return () => console.log('cleanup: unsubscribe');
              }, []);

              return <h1>{name}</h1>;
            }

            createRoot(document.getElementById('root')).render(
              <StrictMode>
                <Profile />
              </StrictMode>
            );
        """,
        lang="jsx",
        output=r"""
            Development (StrictMode):
            render Rahim
            render Rahim
            effect: subscribe
            cleanup: unsubscribe
            effect: subscribe

            Production:
            render Rahim
            effect: subscribe
        """,
        follow=[
            ("How do you prevent a fetch effect from setting state with a stale response?", "Fetch effect যাতে পুরনো response দিয়ে state set না করে, সেটা কীভাবে ঠেকাবে?"),
            ("Which other things does StrictMode double-invoke in development?", "StrictMode development-এ আর কী কী দুইবার invoke করে?"),
        ],
        related=["react-012"],
        refs=[R_STRICT, R_USEEFFECT, R_SYNC],
    ),
    # ------------------------------------------------------------------ react-023
    Q(
        id="react-023", sub="Rendering and Reconciliation", diff="hard", type="mcq",
        prio="high", market="both", mins=4,
        tags=["reconciliation", "state-preservation", "keys", "fiber"],
        ver="Version-independent concept (React 19.3)", vs=False, status="stable",
        q_en=r"""
            The user clicks the counter three times (it shows `Guest: 3`) and then ticks the **Admin mode** checkbox. What does the button show now?
        """,
        q_bn=r"""
            User counter-এ তিনবার click করল (এখন দেখাচ্ছে `Guest: 3`), তারপর **Admin mode** checkbox tick করল। এখন button-এ কী দেখাবে?
        """,
        code=r"""
            import { useState } from 'react';

            function Counter({ label }) {
              const [count, setCount] = useState(0);
              return (
                <button onClick={() => setCount(count + 1)}>
                  {label}: {count}
                </button>
              );
            }

            export default function App() {
              const [isAdmin, setIsAdmin] = useState(false);
              return (
                <div>
                  {isAdmin ? <Counter label="Admin" /> : <Counter label="Guest" />}
                  <label>
                    <input
                      type="checkbox"
                      checked={isAdmin}
                      onChange={(e) => setIsAdmin(e.target.checked)}
                    />
                    Admin mode
                  </label>
                </div>
              );
            }
        """,
        lang="jsx",
        options=[
            ("`Admin: 0` — the other branch of the ternary creates a new component instance", "`Admin: 0` — ternary-এর অন্য branch একটা নতুন component instance তৈরি করে"),
            ("`Admin: 3` — same component type at the same position, so React keeps the state and only updates the `label` prop", "`Admin: 3` — একই position-এ একই component type, তাই React state রেখে দেয় আর শুধু `label` prop update করে"),
            ("`Guest: 3` — the new `label` prop is not read until the next click", "`Guest: 3` — নতুন `label` prop পরের click-এর আগে পড়া হয় না"),
            ("React logs a missing-`key` warning and remounts the counter", "React missing-`key` warning দেয় আর counter remount করে"),
        ],
        correct=1,
        a_en=r"""It shows `Admin: 3`. React decides whether to keep state by looking at the **element type and its position in the tree**, not at which line of JSX produced it. Both branches render a `<Counter>` as the first child of the same `<div>`, so React treats it as the same component and preserves its state.""",
        a_bn=r"""দেখাবে `Admin: 3`। State রাখবে কি না, React সেটা ঠিক করে **element type আর tree-তে তার position** দেখে — JSX-এর কোন লাইন থেকে element এসেছে সেটা দেখে না। দুই branch-ই একই `<div>`-এর প্রথম child হিসেবে `<Counter>` render করে, তাই React এটাকে একই component ধরে state রেখে দেয়।""",
        quick_en=r"""It shows `Admin: 3`. React keeps state based on element type and position in the tree, and both branches render a `<Counter>` in the same spot, so the state is kept and only `label` changes.""",
        quick_bn=r"""দেখাবে `Admin: 3`। React state রাখে element-এর type আর tree-তে তার position দেখে, আর দুই branch-ই একই জায়গায় `<Counter>` render করে, তাই state থেকে যায়, শুধু `label` বদলায়।""",
        ex_en=r"""
            The tempting answer is `Admin: 0`, because the code *looks* like two different counters. But reconciliation only sees "position 0 of this div: was `Counter`, is still `Counter`" → same fiber, update props, keep state.

            How to get a fresh counter when the mode changes:
            - Give different keys: `<Counter key={isAdmin ? 'admin' : 'guest'} ... />` — a different key means a different identity.
            - Or render them at different positions: `{isAdmin && <Counter label="Admin" />}{!isAdmin && <Counter label="Guest" />}`.

            The opposite trap: if the *type* changes at a position (e.g. `<div><Counter /></div>` → `<section><Counter /></section>`), React destroys the whole subtree and its state. That's also why you must never declare a component inside another component's body — it becomes a new type on every render, so its state resets each time. No key warning appears here because keys are only required for arrays of children.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো `Admin: 0`, কারণ code দেখে মনে হয় দুটো আলাদা counter। কিন্তু reconciliation শুধু দেখে "এই div-এর position 0: আগে ছিল `Counter`, এখনো `Counter`" → একই fiber, props update করো, state রেখে দাও।

            Mode বদলালে নতুন counter পেতে চাইলে:
            - আলাদা key দাও: `<Counter key={isAdmin ? 'admin' : 'guest'} ... />` — আলাদা key মানে আলাদা identity।
            - অথবা আলাদা position-এ render করো: `{isAdmin && <Counter label="Admin" />}{!isAdmin && <Counter label="Guest" />}`।

            উল্টো ফাঁদ: কোনো position-এ যদি *type* বদলায় (যেমন `<div><Counter /></div>` → `<section><Counter /></section>`), React পুরো subtree আর তার state ধ্বংস করে দেয়। এজন্যই কখনো একটা component-এর body-র ভেতরে আরেকটা component declare করা যাবে না — প্রতিটা render-এ এটা নতুন type হয়ে যায়, ফলে প্রতিবার state reset হয়। এখানে key warning আসে না, কারণ key শুধু children-এর array-র জন্য দরকার।
        """,
        tip_en=r"""State the rule in one sentence: "React preserves state while the same type renders at the same position." Then show both ways to reset (key, different position). That's a strong signal you understand reconciliation, not just keys in lists.""",
        tip_bn=r"""নিয়মটা এক বাক্যে বলো: "একই position-এ একই type render হলে React state রেখে দেয়।" তারপর reset করার দুটো উপায় দেখাও (key, আলাদা position)। এতে বোঝা যায় তুমি শুধু list-এর key না, পুরো reconciliation বোঝো।""",
        related=["react-004"],
        refs=[R_PRESERVE, R_RENDER_COMMIT],
    ),
    # ------------------------------------------------------------------ react-030
    Q(
        id="react-030", sub="Component API Design", diff="extreme", type="architecture",
        prio="medium", market="international", mins=20,
        tags=["design-system", "compound-components", "accessibility", "api-design", "server-components"],
        ver="React 19.3", vs=True, status="stable",
        q_en=r"""
            You lead a design-system team. Twenty product teams will use your React component library (Button, Dialog, Tabs, Combobox…) in both Next.js App Router apps and Vite SPAs. How do you design the component APIs and the library architecture?
        """,
        q_bn=r"""
            তুমি একটা design-system team-এর lead। বিশটা product team তোমার React component library (Button, Dialog, Tabs, Combobox…) Next.js App Router app আর Vite SPA — দুই জায়গাতেই ব্যবহার করবে। Component API আর library architecture কীভাবে design করবে?
        """,
        a_en=r"""
            *(Advanced, senior-level question.)* I'd start from requirements: accessible by default, themeable, composable, type-safe, small bundles, works in Server Component apps, and a stable API that 20 teams can upgrade safely.

            **API patterns**
            - **Compound components** for complex widgets: `<Tabs> <TabList> <TabTrigger value="a"/> </TabList> <TabPanel value="a"/> </Tabs>`. Shared state goes through Context, so consumers control layout without prop explosions.
            - **Controlled and uncontrolled** support everywhere: `value` / `defaultValue` / `onValueChange`, implemented once in a `useControllableState` hook.
            - **Behave like the DOM element**: spread remaining props onto the root, accept `ref` as a normal prop (React 19 — no `forwardRef`), compose event handlers instead of overriding them.
            - **Variants, not style props**: `variant="danger" size="sm"` mapped to classes; an `asChild`/slot pattern for "render as a link".
            - **Accessibility built in**: follow WAI-ARIA patterns (roles, keyboard navigation, focus trapping in Dialog), `useId` for ARIA relationships, respect `prefers-reduced-motion`.

            **Architecture**
            - Interactive components ship with `'use client'` at their own entry files; purely presentational ones (Badge, Card) stay server-compatible.
            - Styling with CSS variables (design tokens) and `@layer` so apps can override without specificity wars; avoid runtime CSS-in-JS that breaks with Server Components.
            - ESM output, per-component `exports`, `"sideEffects"` declared → good tree-shaking.
            - Quality gates: RTL + axe tests, visual regression, Storybook docs, React Compiler-friendly pure components.
            - Releases: semver, changesets, deprecation warnings one major ahead, codemods for breaking changes.

            Trade-off: building on a headless library (React Aria, Radix) saves months of accessibility work but adds a dependency you don't control.
        """,
        a_bn=r"""
            *(Advanced, senior-level প্রশ্ন।)* আমি requirement দিয়ে শুরু করব: default-ভাবে accessible, themeable, composable, type-safe, ছোট bundle, Server Component app-এ চলে, আর এমন stable API যেটা বিশটা team নিরাপদে upgrade করতে পারে।

            **API pattern**
            - জটিল widget-এর জন্য **compound component**: `<Tabs> <TabList> <TabTrigger value="a"/> </TabList> <TabPanel value="a"/> </Tabs>`। Shared state Context দিয়ে যায়, ফলে consumer layout নিয়ন্ত্রণ করতে পারে, prop-এর বিস্ফোরণ হয় না।
            - সব জায়গায় **controlled আর uncontrolled** দুটোই: `value` / `defaultValue` / `onValueChange` — একবার `useControllableState` hook-এ implement করা।
            - **DOM element-এর মতো আচরণ**: বাকি props root-এ spread করা, `ref` সাধারণ prop হিসেবে নেওয়া (React 19 — `forwardRef` লাগে না), event handler override না করে compose করা।
            - **Style prop না, variant**: `variant="danger" size="sm"` class-এ map হয়; "link হিসেবে render" করার জন্য `asChild`/slot pattern।
            - **Accessibility ভেতরেই**: WAI-ARIA pattern মানা (role, keyboard navigation, Dialog-এ focus trap), ARIA সম্পর্কের জন্য `useId`, `prefers-reduced-motion` মানা।

            **Architecture**
            - Interactive component-গুলোর নিজস্ব entry file-এ `'use client'` থাকবে; শুধু presentational component (Badge, Card) server-compatible থাকবে।
            - CSS variable (design token) আর `@layer` দিয়ে styling, যাতে app specificity-যুদ্ধ ছাড়াই override করতে পারে; Server Component-এ ভেঙে যায় এমন runtime CSS-in-JS এড়ানো।
            - ESM output, প্রতিটা component-এর জন্য `exports`, `"sideEffects"` declare করা → ভালো tree-shaking।
            - Quality gate: RTL + axe test, visual regression, Storybook docs, React Compiler-friendly pure component।
            - Release: semver, changesets, এক major আগে থেকে deprecation warning, breaking change-এর জন্য codemod।

            Trade-off: headless library-র (React Aria, Radix) উপর তৈরি করলে accessibility-র কয়েক মাসের কাজ বাঁচে, কিন্তু এমন একটা dependency যোগ হয় যেটা তোমার নিয়ন্ত্রণে নেই।
        """,
        quick_en=r"""Use compound components with Context, support both controlled and uncontrolled modes, behave like the native element (spread props, `ref` as a prop) and build accessibility in. Ship `'use client'` only on interactive entries, style with CSS variables, tree-shakeable ESM and semver with codemods.""",
        quick_bn=r"""Context-সহ compound component ব্যবহার করো, controlled আর uncontrolled দুই mode-ই support করো, native element-এর মতো আচরণ করো (props spread, `ref` prop হিসেবে), আর accessibility শুরু থেকেই রাখো। শুধু interactive entry-তে `'use client'`, styling-এ CSS variable, tree-shake করা যায় এমন ESM, আর codemod-সহ semver।""",
        ex_en=r"""
            **Why these choices**
            - Compound components + Context keep each piece small and let teams insert their own markup between parts. The cost: misuse outside the parent must be caught with a clear runtime error (see `useTabs` in the code).
            - Controlled/uncontrolled hybrids prevent the classic bug where a component silently switches modes. Warn in dev if `value` changes from `undefined` to defined.
            - With React 19, `ref` is a regular prop for function components, so spreading props passes it through; legacy `forwardRef` is only needed if you still support React 18 consumers.
            - The context value object is recreated each render; with React Compiler it's memoized automatically, otherwise wrap it in `useMemo` so every consumer doesn't re-render on unrelated parent renders.

            **Failure scenarios to plan for:** a team pins an old major for a year (support window policy), a CSS reset in an app overrides your styles (layers), a Server Component imports an interactive component without the directive (lint rule + entry-point design), and accessibility regressions (automated axe checks in CI plus manual screen-reader testing for complex widgets).
        """,
        ex_bn=r"""
            **কেন এই সিদ্ধান্তগুলো**
            - Compound component + Context প্রতিটা অংশ ছোট রাখে, আর team-গুলো অংশগুলোর মাঝে নিজের markup বসাতে পারে। খরচ: parent-এর বাইরে ভুল ব্যবহার হলে স্পষ্ট runtime error দিয়ে ধরতে হয় (code-এ `useTabs` দেখো)।
            - Controlled/uncontrolled hybrid সেই classic bug ঠেকায়, যেখানে component চুপচাপ mode বদলে ফেলে। `value` যদি `undefined` থেকে defined হয়, dev-এ warning দাও।
            - React 19-এ function component-এর জন্য `ref` একটা সাধারণ prop, তাই props spread করলে এটাও চলে যায়; React 18 consumer support করলে তবেই legacy `forwardRef` দরকার।
            - Context value object প্রতিটা render-এ নতুন তৈরি হয়; React Compiler থাকলে এটা নিজে থেকেই memoize হয়, না থাকলে `useMemo` দিয়ে wrap করো, যাতে parent-এর অপ্রাসঙ্গিক render-এ সব consumer re-render না হয়।

            **যেসব failure scenario আগে থেকে ভাবতে হবে:** কোনো team এক বছর পুরনো major-এ আটকে থাকে (support window policy), কোনো app-এর CSS reset তোমার style override করে (layers), কোনো Server Component directive ছাড়া interactive component import করে (lint rule + entry-point design), আর accessibility regression (CI-তে automated axe check, আর জটিল widget-এর জন্য manual screen-reader testing)।
        """,
        tip_en=r"""Open with requirements and consumers before naming patterns. Then cover API (compound, controlled/uncontrolled, ref, a11y), architecture (RSC boundaries, styling, bundling) and process (versioning, codemods). Ending with a build-vs-buy trade-off sounds like a real tech lead.""",
        tip_bn=r"""Pattern-এর নাম বলার আগে requirement আর consumer কারা সেটা দিয়ে শুরু করো। তারপর API (compound, controlled/uncontrolled, ref, a11y), architecture (RSC boundary, styling, bundling) আর process (versioning, codemod) কভার করো। শেষে build-vs-buy trade-off বললে একজন আসল tech lead-এর মতো শোনায়।""",
        mist_en=r"""Designing a single mega-component with 40 boolean props, forgetting keyboard and screen-reader support, or marking the whole library entry `'use client'` so nothing can render on the server.""",
        mist_bn=r"""৪০টা boolean prop-সহ একটা বিশাল component বানানো, keyboard আর screen-reader support ভুলে যাওয়া, অথবা পুরো library-র entry-তে `'use client'` দিয়ে দেওয়া, ফলে কিছুই server-এ render হতে পারে না।""",
        code=r"""
            'use client';
            import { createContext, use, useId, useState, type ComponentProps } from 'react';

            type TabsCtx = { value: string; select: (v: string) => void; baseId: string };
            const TabsContext = createContext<TabsCtx | null>(null);

            function useTabs() {
              const ctx = use(TabsContext);
              if (!ctx) throw new Error('<TabTrigger> and <TabPanel> must be inside <Tabs>');
              return ctx;
            }

            type TabsProps = {
              value?: string;                      // controlled
              defaultValue?: string;               // uncontrolled
              onValueChange?: (value: string) => void;
            } & ComponentProps<'div'>;

            export function Tabs({ value, defaultValue = '', onValueChange, ...rest }: TabsProps) {
              const [inner, setInner] = useState(defaultValue);
              const isControlled = value !== undefined;
              const current = isControlled ? value : inner;
              const baseId = useId();

              const select = (next: string) => {
                if (!isControlled) setInner(next);
                onValueChange?.(next);
              };

              return (
                <TabsContext value={{ value: current, select, baseId }}>
                  <div {...rest} />
                </TabsContext>
              );
            }

            export function TabTrigger({ value, onClick, ...rest }: { value: string } & ComponentProps<'button'>) {
              const { value: current, select, baseId } = useTabs();
              const selected = current === value;
              return (
                <button
                  {...rest} // includes `ref` in React 19
                  type="button"
                  role="tab"
                  id={`${baseId}-tab-${value}`}
                  aria-selected={selected}
                  aria-controls={`${baseId}-panel-${value}`}
                  tabIndex={selected ? 0 : -1}
                  onClick={(e) => {
                    onClick?.(e);                      // compose, don't override
                    if (!e.defaultPrevented) select(value);
                  }}
                />
              );
            }

            export function TabPanel({ value, ...rest }: { value: string } & ComponentProps<'div'>) {
              const { value: current, baseId } = useTabs();
              if (current !== value) return null;
              return (
                <div
                  {...rest}
                  role="tabpanel"
                  id={`${baseId}-panel-${value}`}
                  aria-labelledby={`${baseId}-tab-${value}`}
                />
              );
            }
        """,
        lang="tsx",
        follow=[
            ("How would you add arrow-key navigation between tabs without breaking composition?", "Composition না ভেঙে tab-গুলোর মধ্যে arrow-key navigation কীভাবে যোগ করবে?"),
            ("How do you ship a breaking API change to 20 teams with minimal pain?", "কম কষ্টে বিশটা team-এর কাছে একটা breaking API change কীভাবে পৌঁছে দেবে?"),
            ("When would you choose a headless library instead of building widgets yourself?", "নিজে widget বানানোর বদলে কখন headless library বেছে নেবে?"),
        ],
        related=["react-002"],
        refs=[R_CTX, R_USEID, R_COMPILER],
    ),
]

if __name__ == "__main__":
    save("react", "b1", QUESTIONS)
