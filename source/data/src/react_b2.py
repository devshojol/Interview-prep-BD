# React — batch 2 (react-005..007, 014..016, 024, 031)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_INPUT = ("react.dev — <input> (controlled inputs)", "https://react.dev/reference/react-dom/components/input")
R_FORM = ("react.dev — <form>", "https://react.dev/reference/react-dom/components/form")
R_USEREF = ("react.dev — useRef", "https://react.dev/reference/react/useRef")
R_REFS_LEARN = ("react.dev — Referencing Values with Refs", "https://react.dev/learn/referencing-values-with-refs")
R_USEEFFECT = ("react.dev — useEffect", "https://react.dev/reference/react/useEffect")
R_SYNC = ("react.dev — Synchronizing with Effects", "https://react.dev/learn/synchronizing-with-effects")
R_NO_EFFECT = ("react.dev — You Might Not Need an Effect", "https://react.dev/learn/you-might-not-need-an-effect")
R_USEMEMO = ("react.dev — useMemo", "https://react.dev/reference/react/useMemo")
R_MEMO = ("react.dev — memo", "https://react.dev/reference/react/memo")
R_COMPILER = ("react.dev — React Compiler v1.0", "https://react.dev/blog/2025/10/07/react-compiler-1")
R_COMPILER_INC = ("react.dev — React Compiler: Incremental Adoption", "https://react.dev/learn/react-compiler/incremental-adoption")
R_CUSTOM_HOOKS = ("react.dev — Reusing Logic with Custom Hooks", "https://react.dev/learn/reusing-logic-with-custom-hooks")
R_USEACTIONSTATE = ("react.dev — useActionState", "https://react.dev/reference/react/useActionState")
R_USEFORMSTATUS = ("react.dev — useFormStatus", "https://react.dev/reference/react-dom/hooks/useFormStatus")
R_USEOPTIMISTIC = ("react.dev — useOptimistic", "https://react.dev/reference/react/useOptimistic")
R_USETRANSITION = ("react.dev — useTransition", "https://react.dev/reference/react/useTransition")
R_USEDEFERRED = ("react.dev — useDeferredValue", "https://react.dev/reference/react/useDeferredValue")
R_UPGRADE19 = ("react.dev — React 19 Upgrade Guide", "https://react.dev/blog/2024/04/25/react-19-upgrade-guide")
R_CREATEROOT = ("react.dev — createRoot", "https://react.dev/reference/react-dom/client/createRoot")

QUESTIONS = [
    # ------------------------------------------------------------------ react-005
    Q(
        id="react-005", sub="Controlled and Uncontrolled Components", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["forms", "controlled", "uncontrolled", "formdata"],
        ver="React 19.3", vs=True, status="stable",
        q_en=r"""What is the difference between controlled and uncontrolled form inputs in React? When would you use each?""",
        q_bn=r"""React-এ controlled আর uncontrolled form input-এর পার্থক্য কী? কখন কোনটা ব্যবহার করবে?""",
        a_en=r"""
            A **controlled** input gets its value from React state: `value={name}` plus `onChange={e => setName(e.target.value)}`. React is the single source of truth, so I can validate on every keystroke, format the value, or enable/disable a button instantly.

            An **uncontrolled** input keeps its value inside the DOM. I give it a `defaultValue` and read the value when needed — through a ref or, more commonly, from `FormData` on submit.

            I use controlled inputs when the UI must react while the user types. For simple forms I prefer uncontrolled inputs, especially with React 19 form Actions (`<form action={fn}>`), which pass `FormData` to the function and avoid a re-render per keystroke. File inputs are always uncontrolled.
        """,
        a_bn=r"""
            **Controlled** input তার value পায় React state থেকে: `value={name}` আর সাথে `onChange={e => setName(e.target.value)}`। এখানে React-ই single source of truth, তাই প্রতিটা keystroke-এ validate করা, value format করা বা সাথে সাথে button enable/disable করা যায়।

            **Uncontrolled** input তার value DOM-এর ভেতরেই রাখে। আমি একটা `defaultValue` দিই আর দরকার হলে value পড়ি — ref দিয়ে, অথবা বেশিরভাগ সময় submit-এর সময় `FormData` থেকে।

            User টাইপ করার সময়ই UI-কে প্রতিক্রিয়া দেখাতে হলে আমি controlled input ব্যবহার করি। সাধারণ form-এর জন্য uncontrolled পছন্দ করি, বিশেষ করে React 19-এর form Action (`<form action={fn}>`)-এর সাথে, যেটা function-এ `FormData` পাঠায় আর প্রতিটা keystroke-এ re-render এড়ায়। File input সবসময় uncontrolled।
        """,
        ex_en=r"""
            - **Don't switch modes:** if `value` starts as `undefined` and later becomes a string, React warns that an uncontrolled input became controlled. Initialise with `''`, not `undefined`.
            - **`value` without `onChange`** makes the field read-only (React warns). Use `defaultValue` or `readOnly` if that's intended.
            - **Form Actions and reset:** in React 19, when a `<form action>` Action succeeds, React automatically resets uncontrolled fields. Controlled fields keep whatever state you hold.
            - **Performance:** a large controlled form re-renders on each keystroke; usually fine, but form libraries (e.g. React Hook Form) use uncontrolled inputs to avoid it.
        """,
        ex_bn=r"""
            - **Mode বদলাবে না:** `value` যদি শুরুতে `undefined` থাকে আর পরে string হয়, React warning দেয় যে uncontrolled input controlled হয়ে গেছে। `undefined` না, `''` দিয়ে initialize করো।
            - **`onChange` ছাড়া `value`** দিলে field read-only হয়ে যায় (React warning দেয়)। এটা ইচ্ছাকৃত হলে `defaultValue` বা `readOnly` ব্যবহার করো।
            - **Form Action আর reset:** React 19-এ `<form action>` Action সফল হলে React নিজে থেকেই uncontrolled field reset করে দেয়। Controlled field-এ তোমার রাখা state-ই থাকে।
            - **Performance:** বড় controlled form প্রতিটা keystroke-এ re-render হয়; সাধারণত সমস্যা না, তবে form library (যেমন React Hook Form) এটা এড়াতে uncontrolled input ব্যবহার করে।
        """,
        tip_en=r"""Define both in one sentence each ("React state is the source of truth" vs "the DOM is"), then give a concrete use case for each. Mentioning React 19 form Actions shows you're current.""",
        tip_bn=r"""দুটোকেই এক বাক্যে define করো ("React state হলো source of truth" বনাম "DOM হলো source of truth"), তারপর প্রতিটার একটা বাস্তব use case দাও। React 19 form Action-এর কথা বললে বোঝা যায় তুমি আপডেটেড।""",
        mist_en=r"""Initialising controlled inputs with `undefined`/`null`, or assuming uncontrolled inputs are "bad practice".""",
        mist_bn=r"""Controlled input-কে `undefined`/`null` দিয়ে initialize করা, অথবা uncontrolled input-কে "bad practice" মনে করা।""",
        code=r"""
            import { useState } from 'react';

            // Controlled: React state drives the value
            function Username() {
              const [name, setName] = useState('');
              const tooShort = name.length > 0 && name.length < 3;
              return (
                <>
                  <input value={name} onChange={(e) => setName(e.target.value)} />
                  {tooShort && <p>At least 3 characters</p>}
                </>
              );
            }

            // Uncontrolled: the DOM holds the value, read it on submit
            function Newsletter() {
              async function subscribe(formData) {
                await fetch('/api/subscribe', { method: 'POST', body: formData });
              }
              return (
                <form action={subscribe}>
                  <input name="email" type="email" defaultValue="" required />
                  <button>Subscribe</button>
                </form>
              );
            }
        """,
        lang="jsx",
        follow=[
            ("Why do file inputs have to be uncontrolled?", "File input কেন uncontrolled হতেই হয়?"),
            ("How would you reset a controlled form after a successful submit?", "সফল submit-এর পর একটা controlled form কীভাবে reset করবে?"),
        ],
        refs=[R_INPUT, R_FORM],
    ),
    # ------------------------------------------------------------------ react-006
    Q(
        id="react-006", sub="useRef", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["useref", "re-render", "mutable-value"],
        ver="Version-independent concept (React 19.3)", vs=False, status="stable",
        q_en=r"""Inside a click handler you run `countRef.current = countRef.current + 1`, where `countRef = useRef(0)`. What happens?""",
        q_bn=r"""একটা click handler-এর ভেতরে তুমি `countRef.current = countRef.current + 1` চালালে, যেখানে `countRef = useRef(0)`। কী হবে?""",
        options=[
            ("The component re-renders and shows the new value", "Component re-render হয়ে নতুন value দেখায়"),
            ("The value changes immediately, but no re-render is triggered", "Value সাথে সাথে বদলায়, কিন্তু কোনো re-render trigger হয় না"),
            ("The change is queued and applied on the next render, like state", "পরিবর্তনটা state-এর মতো queue হয়ে পরের render-এ apply হয়"),
            ("The value resets to `0` on the next render", "পরের render-এ value আবার `0` হয়ে যায়"),
        ],
        correct=1,
        a_en=r"""The value changes immediately and persists across renders, but React does not re-render. A ref is a plain mutable object (`{ current }`) that React keeps for the lifetime of the component; it isn't part of the render output.""",
        a_bn=r"""Value সাথে সাথে বদলায় আর render-এর পর render টিকে থাকে, কিন্তু React re-render করে না। Ref হলো একটা সাধারণ mutable object (`{ current }`), যেটা React component-এর পুরো জীবনকাল ধরে রেখে দেয়; এটা render output-এর অংশ না।""",
        ex_en=r"""
            The tempting answer is "it re-renders", because refs feel like state. They're not: changing `ref.current` is invisible to React. If the value must appear on screen, it belongs in state. A ref also doesn't reset — `useRef(0)` only uses `0` on the first render.

            Good uses: DOM nodes (`<input ref={inputRef}>` for focus/measurement), timer or interval ids, the previous value of something, or an instance of a non-React library. Avoid reading or writing `ref.current` *during render* (except lazy initialisation) — it makes rendering impure and can confuse React Compiler.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো "re-render হবে", কারণ ref দেখতে অনেকটা state-এর মতো। আসলে তা না: `ref.current` বদলালে React সেটা টেরই পায় না। Value যদি স্ক্রিনে দেখাতে হয়, তাহলে সেটা state-এ রাখা উচিত। Ref reset-ও হয় না — `useRef(0)` শুধু প্রথম render-এ `0` ব্যবহার করে।

            ভালো ব্যবহার: DOM node (`<input ref={inputRef}>` দিয়ে focus/measurement), timer বা interval id, কোনো কিছুর আগের value, অথবা non-React library-র instance। *Render-এর সময়* `ref.current` পড়া বা লেখা এড়িয়ে চলো (lazy initialization ছাড়া) — এতে rendering impure হয় আর React Compiler বিভ্রান্ত হতে পারে।
        """,
        tip_en=r"""Contrast them in one line — state is for values that affect what you see; refs are for values you need to remember but don't render. Then name two real uses of refs (DOM focus, timer ids).""",
        tip_bn=r"""এক লাইনে তুলনা করো — যে value স্ক্রিনে কী দেখাবে তাকে প্রভাবিত করে সেটা state; যেটা মনে রাখতে হবে কিন্তু render করতে হবে না সেটা ref। তারপর ref-এর দুটো বাস্তব ব্যবহার বলো (DOM focus, timer id)।""",
        refs=[R_USEREF, R_REFS_LEARN],
    ),
    # ------------------------------------------------------------------ react-007
    Q(
        id="react-007", sub="Component Lifecycle and Effects", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["useeffect", "lifecycle", "cleanup", "dependencies"],
        ver="React 19.3 (class lifecycle methods = legacy)", vs=False, status="stable",
        q_en=r"""What is `useEffect` for? How do the class-component lifecycle methods (mount, update, unmount) map to it?""",
        q_bn=r"""`useEffect` কী কাজে লাগে? Class component-এর lifecycle method (mount, update, unmount) এর সাথে কীভাবে মিলে যায়?""",
        a_en=r"""
            `useEffect` synchronises a component with something **outside React** — a subscription, a timer, a WebSocket, a browser API or a non-React widget. It runs after React has committed the render to the screen.

            The dependency array decides when it re-runs:
            - no array → after every render;
            - `[]` → once after mount;
            - `[roomId]` → after mount and whenever `roomId` changes.

            The function you return is the **cleanup**. React runs it before re-running the effect and when the component unmounts.

            Mapping from legacy class components: `componentDidMount` ≈ effect with `[]`, `componentDidUpdate` ≈ effect with dependencies, `componentWillUnmount` ≈ cleanup. But I think in terms of "start syncing / stop syncing", not lifecycle events.
        """,
        a_bn=r"""
            `useEffect` একটা component-কে **React-এর বাইরের** কোনো কিছুর সাথে sync রাখে — subscription, timer, WebSocket, browser API বা non-React widget। React render screen-এ commit করার পর এটা চলে।

            Dependency array ঠিক করে কখন আবার চলবে:
            - কোনো array নেই → প্রতিটা render-এর পর;
            - `[]` → mount-এর পর একবার;
            - `[roomId]` → mount-এর পর, আর যখনই `roomId` বদলায়।

            তুমি যে function return করো সেটা হলো **cleanup**। Effect আবার চালানোর আগে আর component unmount হলে React এটা চালায়।

            Legacy class component-এর সাথে মিল: `componentDidMount` ≈ `[]`-সহ effect, `componentDidUpdate` ≈ dependency-সহ effect, `componentWillUnmount` ≈ cleanup। তবে আমি lifecycle event হিসেবে না, "sync শুরু করো / sync বন্ধ করো" — এভাবে চিন্তা করি।
        """,
        ex_en=r"""
            - **Many things don't need an effect:** derived values (compute during render), reacting to a button click (do it in the event handler), resetting state when a prop changes (use a `key`).
            - **Dependencies must be honest:** every reactive value used inside (props, state, functions declared in the component) belongs in the array. The `react-hooks/exhaustive-deps` lint rule enforces this.
            - **Cleanup symmetry:** if setup connects, cleanup disconnects. In development, StrictMode runs setup → cleanup → setup once to prove this.
            - **Error boundaries** are the one lifecycle feature hooks don't replace: they still need a class component (or a library such as `react-error-boundary`).
        """,
        ex_bn=r"""
            - **অনেক কিছুর জন্য effect লাগে না:** derived value (render-এর সময় compute করো), button click-এর প্রতিক্রিয়া (event handler-এ করো), prop বদলালে state reset করা (`key` ব্যবহার করো)।
            - **Dependency সৎ হতে হবে:** effect-এর ভেতরে ব্যবহার হওয়া প্রতিটা reactive value (props, state, component-এর ভেতরে declare করা function) array-তে থাকবে। `react-hooks/exhaustive-deps` lint rule এটা নিশ্চিত করে।
            - **Cleanup-এর symmetry:** setup connect করলে cleanup disconnect করবে। Development-এ StrictMode একবার setup → cleanup → setup চালিয়ে এটা যাচাই করে।
            - **Error boundary** হলো একমাত্র lifecycle feature যেটা hook দিয়ে replace হয়নি: এখনো class component (বা `react-error-boundary`-এর মতো library) লাগে।
        """,
        tip_en=r"""Start with "effects synchronise with external systems", then the three dependency-array cases, then cleanup. Give the lifecycle mapping only as a bridge for legacy code — and add one example of "you don't need an effect here".""",
        tip_bn=r"""শুরু করো "effect বাইরের system-এর সাথে sync রাখে" দিয়ে, তারপর dependency array-র তিনটা case, তারপর cleanup। Lifecycle mapping শুধু legacy code বোঝার সেতু হিসেবে দাও — আর "এখানে effect দরকারই নেই"-এর একটা উদাহরণ যোগ করো।""",
        mist_en=r"""Using effects to compute derived state or to respond to user events, and leaving out dependencies to make an effect "run once".""",
        mist_bn=r"""Derived state হিসাব করতে বা user event-এর প্রতিক্রিয়া দিতে effect ব্যবহার করা, আর effect "একবার চালাতে" dependency বাদ দিয়ে দেওয়া।""",
        code=r"""
            import { useEffect, useState } from 'react';
            import { createConnection } from './chat';

            function ChatRoom({ roomId }) {
              const [messages, setMessages] = useState([]);

              useEffect(() => {
                const connection = createConnection(roomId);     // start syncing
                connection.on('message', (msg) => setMessages((m) => [...m, msg]));
                connection.connect();

                return () => connection.disconnect();            // stop syncing
              }, [roomId]); // re-sync when the room changes

              return <MessageList messages={messages} />;
            }
        """,
        lang="jsx",
        follow=[
            ("What is the difference between `useEffect` and `useLayoutEffect`?", "`useEffect` আর `useLayoutEffect`-এর পার্থক্য কী?"),
            ("Give an example of an effect that should be an event handler instead.", "এমন একটা effect-এর উদাহরণ দাও, যেটা আসলে event handler হওয়া উচিত।"),
        ],
        related=["react-013"],
        refs=[R_USEEFFECT, R_SYNC, R_NO_EFFECT],
    ),
    # ------------------------------------------------------------------ react-014
    Q(
        id="react-014", sub="Performance Optimization", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["usememo", "usecallback", "react-memo", "react-compiler"],
        ver="React 19.3 + React Compiler 1.0", vs=True, status="stable",
        q_en=r"""Compare `useMemo`, `useCallback` and `React.memo`. With React Compiler 1.0 available, do you still write them by hand?""",
        q_bn=r"""`useMemo`, `useCallback` আর `React.memo`-এর তুলনা করো। React Compiler 1.0 থাকা অবস্থায়ও কি এগুলো হাতে লেখো?""",
        a_en=r"""
            - **`useMemo(fn, deps)`** caches a *computed value* between renders until a dependency changes — for expensive calculations or to keep an object/array reference stable.
            - **`useCallback(fn, deps)`** caches a *function reference*; it's `useMemo(() => fn, deps)`.
            - **`React.memo(Component)`** skips re-rendering a component when its props are shallowly equal to last time.

            They work as a team: `memo` on a child only helps if the parent passes stable props, which is what `useMemo`/`useCallback` provide.

            **React Compiler 1.0** memoizes components and values automatically at build time, more precisely than most people do by hand. In compiled code I don't add manual memoization by default. I still use `useMemo`/`useCallback` as escape hatches — e.g. when a value is an effect dependency and I need precise control — and in code the compiler skips. For existing code I leave current memoization in place unless I've tested removing it, because removing it can change compiled output.
        """,
        a_bn=r"""
            - **`useMemo(fn, deps)`** render-এর মধ্যে একটা *computed value* cache করে রাখে, যতক্ষণ না কোনো dependency বদলায় — expensive calculation বা object/array-র reference স্থির রাখার জন্য।
            - **`useCallback(fn, deps)`** একটা *function reference* cache করে; এটা আসলে `useMemo(() => fn, deps)`।
            - **`React.memo(Component)`** props আগের বারের সাথে shallowly equal হলে component-এর re-render skip করে।

            এরা একসাথে কাজ করে: child-এ `memo` তখনই কাজে লাগে যখন parent স্থির props পাঠায় — আর সেটাই `useMemo`/`useCallback` নিশ্চিত করে।

            **React Compiler 1.0** build time-এ component আর value নিজে থেকেই memoize করে, বেশিরভাগ মানুষের হাতে লেখার চেয়েও নিখুঁতভাবে। Compiled code-এ আমি default-ভাবে manual memoization যোগ করি না। তবে escape hatch হিসেবে `useMemo`/`useCallback` এখনো ব্যবহার করি — যেমন কোনো value effect-এর dependency হলে আর নিখুঁত নিয়ন্ত্রণ দরকার হলে — আর compiler যে code skip করে সেখানে। পুরনো code-এ বিদ্যমান memoization রেখে দিই, যদি না সরিয়ে test করে দেখি, কারণ সরালে compiled output বদলে যেতে পারে।
        """,
        ex_en=r"""
            - **Memoization isn't free:** it costs memory and a dependency comparison each render. For cheap calculations it can be slower than recomputing.
            - **Shallow comparison pitfalls:** passing `style={{...}}`, inline arrow functions or JSX `children` creates new references every render, so `memo` never skips.
            - **Context bypasses `memo`:** a memoized component that reads a context still re-renders when the context value changes.
            - **Compiler requirements:** it only compiles code that follows the Rules of React (pure render, no mutation of props/state, no reading refs during render). It skips functions it can't prove safe; `"use no memo"` opts a function out temporarily. The `eslint-plugin-react-hooks` recommended preset includes compiler-powered rules that flag violations.
            - **Measure first:** use the React DevTools Profiler to confirm a re-render is actually slow before optimising.
        """,
        ex_bn=r"""
            - **Memoization বিনামূল্যে না:** এতে memory লাগে আর প্রতিটা render-এ dependency তুলনা করতে হয়। সস্তা calculation-এর ক্ষেত্রে নতুন করে হিসাব করার চেয়ে এটা ধীরও হতে পারে।
            - **Shallow comparison-এর ফাঁদ:** `style={{...}}`, inline arrow function বা JSX `children` পাঠালে প্রতিটা render-এ নতুন reference তৈরি হয়, ফলে `memo` কখনো skip করে না।
            - **Context `memo`-কে পাশ কাটিয়ে যায়:** memoized component যদি কোনো context পড়ে, context value বদলালে সেটা re-render হবেই।
            - **Compiler-এর শর্ত:** এটা শুধু Rules of React মানা code compile করে (pure render, props/state mutate না করা, render-এর সময় ref না পড়া)। নিরাপদ প্রমাণ করতে না পারলে function skip করে; `"use no memo"` দিয়ে সাময়িকভাবে কোনো function বাদ দেওয়া যায়। `eslint-plugin-react-hooks`-এর recommended preset-এ compiler-চালিত rule আছে, যেগুলো এই লঙ্ঘন ধরে।
            - **আগে মাপো:** optimize করার আগে React DevTools Profiler দিয়ে নিশ্চিত হও যে re-render আসলেই ধীর।
        """,
        tip_en=r"""Give one-line definitions, explain how they combine, then pivot to the compiler with nuance ("new code: rely on it; existing code: don't rip out memoization blindly"). That nuance is what makes the answer sound current rather than memorised.""",
        tip_bn=r"""এক লাইনে করে definition দাও, এরা কীভাবে একসাথে কাজ করে বোঝাও, তারপর সূক্ষ্মতাসহ compiler-এ যাও ("নতুন code: compiler-এর উপর ভরসা; পুরনো code: অন্ধভাবে memoization সরাবে না")। এই সূক্ষ্মতাই উত্তরকে মুখস্থ না, আপডেটেড শোনায়।""",
        mist_en=r"""Wrapping everything in `useCallback`/`useMemo` "for performance" without a memoized consumer, or claiming the compiler made these hooks deprecated.""",
        mist_bn=r"""কোনো memoized consumer ছাড়াই "performance-এর জন্য" সবকিছু `useCallback`/`useMemo`-এ wrap করা, অথবা দাবি করা যে compiler আসার ফলে এই hook-গুলো deprecated।""",
        code=r"""
            import { memo, useCallback, useMemo, useState } from 'react';

            const ProductList = memo(function ProductList({ products, onSelect }) {
              return products.map((p) => (
                <button key={p.id} onClick={() => onSelect(p.id)}>{p.name}</button>
              ));
            });

            export default function Shop({ allProducts }) {
              const [query, setQuery] = useState('');
              const [cartCount, setCartCount] = useState(0);

              // Without React Compiler: keep props stable so memo(ProductList) can skip
              const visible = useMemo(
                () => allProducts.filter((p) => p.name.includes(query)),
                [allProducts, query]
              );
              const handleSelect = useCallback(() => setCartCount((c) => c + 1), []);

              return (
                <>
                  <input value={query} onChange={(e) => setQuery(e.target.value)} />
                  <p>Cart: {cartCount}</p>
                  <ProductList products={visible} onSelect={handleSelect} />
                </>
              );
            }
            // With React Compiler enabled, the same component without useMemo/useCallback/memo
            // is memoized automatically at build time.
        """,
        lang="jsx",
        follow=[
            ("Why does `React.memo` stop working when you pass `children`?", "`children` পাঠালে `React.memo` কেন কাজ করা বন্ধ করে দেয়?"),
            ("How would you roll out React Compiler gradually in a large codebase?", "বড় codebase-এ React Compiler ধাপে ধাপে কীভাবে চালু করবে?"),
        ],
        refs=[R_USEMEMO, R_MEMO, R_COMPILER],
    ),
    # ------------------------------------------------------------------ react-015
    Q(
        id="react-015", sub="Custom Hooks", diff="medium", type="coding",
        prio="high", market="both", mins=10,
        tags=["custom-hooks", "data-fetching", "race-condition", "abortcontroller"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""
            Write a custom hook `useFetchJson(url)` that returns `{ data, error, loading }`.

            Requirements:
            - It fetches JSON and re-fetches whenever `url` changes.
            - It must never show data from an outdated request. Example: the user switches quickly from `/api/users/1` to `/api/users/2`; even if request 1 finishes last, the hook must end with user 2's data.
            - Non-2xx responses become an `error`; the request is cancelled when the component unmounts.
        """,
        q_bn=r"""
            একটা custom hook `useFetchJson(url)` লেখো, যেটা `{ data, error, loading }` return করবে।

            শর্ত:
            - এটা JSON fetch করবে, আর `url` বদলালেই আবার fetch করবে।
            - কখনোই পুরনো request-এর data দেখানো যাবে না। উদাহরণ: user দ্রুত `/api/users/1` থেকে `/api/users/2`-এ গেল; request 1 শেষে শেষ হলেও hook-এর শেষ অবস্থা হবে user 2-এর data।
            - Non-2xx response হলে `error` হবে; component unmount হলে request cancel হবে।
        """,
        a_en=r"""
            The effect depends on `url`, creates an `AbortController`, and aborts it in the cleanup. When `url` changes, React runs the cleanup first, which cancels the old request — so a slow old response can't overwrite the new one. On unmount the same cleanup cancels the request.

            I store the result together with the `url` it belongs to and **derive** `loading` as `result.url !== url`. That avoids calling `setState` synchronously inside the effect and guarantees I never return data that belongs to another URL. An `AbortError` is ignored because cancelling was intentional; HTTP errors are thrown manually because `fetch` only rejects on network failure.
        """,
        a_bn=r"""
            Effect-টা `url`-এর উপর নির্ভর করে, একটা `AbortController` তৈরি করে আর cleanup-এ abort করে। `url` বদলালে React আগে cleanup চালায়, যেটা পুরনো request cancel করে দেয় — ফলে ধীর পুরনো response নতুনটাকে overwrite করতে পারে না। Unmount হলেও একই cleanup request cancel করে।

            আমি result-টা যে `url`-এর, সেটাসহ store করি আর `loading` **derive** করি `result.url !== url` দিয়ে। এতে effect-এর ভেতরে synchronously `setState` call করতে হয় না, আর নিশ্চিত হয় যে অন্য URL-এর data কখনো return হবে না। `AbortError` ignore করি, কারণ cancel করাটা ইচ্ছাকৃত; HTTP error হাতে throw করি, কারণ `fetch` শুধু network failure-এ reject করে।
        """,
        ex_en=r"""
            **Why this works for the race:** request 1 is aborted the moment `url` becomes `/api/users/2`. Even if its response were already parsed and its `setResult` ran late, it would be stored under `url: '/api/users/1'`, so `loading` stays `true` for user 2 until the right data arrives.

            **Edge cases**
            - Non-JSON bodies make `res.json()` reject → returned as `error`.
            - StrictMode in dev: the first request is aborted by the extra cleanup, the second one completes — correct behaviour.
            - Same URL rendered again: no new request because the dependency didn't change.

            **In production code** I'd usually use TanStack Query/SWR, framework data loading or Server Components, which add caching, deduplication, retries and background refresh. The hook is still a great interview exercise for effect cleanup and race conditions.
        """,
        ex_bn=r"""
            **Race-এর ক্ষেত্রে কেন কাজ করে:** `url` যখনই `/api/users/2` হয়, request 1 abort হয়ে যায়। এমনকি তার response আগেই parse হয়ে থাকলে আর `setResult` দেরিতে চললেও, সেটা `url: '/api/users/1'`-এর নিচে store হবে, তাই সঠিক data না আসা পর্যন্ত user 2-এর জন্য `loading` `true`-ই থাকে।

            **Edge case**
            - Body JSON না হলে `res.json()` reject করে → `error` হিসেবে return হয়।
            - Dev-এ StrictMode: বাড়তি cleanup প্রথম request abort করে, দ্বিতীয়টা শেষ হয় — এটাই সঠিক আচরণ।
            - একই URL আবার render হলে নতুন request যায় না, কারণ dependency বদলায়নি।

            **Production code-এ** আমি সাধারণত TanStack Query/SWR, framework-এর data loading বা Server Component ব্যবহার করি — এগুলো caching, deduplication, retry আর background refresh যোগ করে। তবুও effect cleanup আর race condition বোঝানোর জন্য এই hook একটা চমৎকার interview exercise।
        """,
        tip_en=r"""Name the race condition explicitly before coding, then point at the cleanup line as the fix. Finish by saying what you'd use in a real app — interviewers like candidates who know when *not* to hand-roll.""",
        tip_bn=r"""Code লেখার আগে race condition-টার নাম স্পষ্ট করে বলো, তারপর সমাধান হিসেবে cleanup লাইনটা দেখাও। শেষে বলো আসল app-এ কী ব্যবহার করতে — interviewer পছন্দ করে যখন candidate জানে কখন নিজে লেখা *উচিত না*।""",
        mist_en=r"""Forgetting the cleanup (stale responses win), treating `fetch` as rejecting on 404/500, or putting an object/inline options in the dependency array and causing an infinite refetch loop.""",
        mist_bn=r"""Cleanup ভুলে যাওয়া (তখন পুরনো response জিতে যায়), ভাবা যে 404/500-এ `fetch` reject করে, অথবা dependency array-তে object/inline options দিয়ে অসীম refetch loop তৈরি করা।""",
        code=r"""
            import { useEffect, useState } from 'react';

            export function useFetchJson(url) {
              const [result, setResult] = useState({ url: null, data: null, error: null });

              useEffect(() => {
                const controller = new AbortController();

                fetch(url, { signal: controller.signal })
                  .then((res) => {
                    if (!res.ok) throw new Error(`HTTP ${res.status}`);
                    return res.json();
                  })
                  .then((data) => setResult({ url, data, error: null }))
                  .catch((error) => {
                    if (error.name === 'AbortError') return; // cancelled on purpose
                    setResult({ url, data: null, error });
                  });

                return () => controller.abort(); // url changed or component unmounted
              }, [url]);

              const loading = result.url !== url; // derived, not stored
              return {
                data: loading ? null : result.data,
                error: loading ? null : result.error,
                loading,
              };
            }

            // Usage
            function UserCard({ userId }) {
              const { data, error, loading } = useFetchJson(`/api/users/${userId}`);
              if (loading) return <p>Loading…</p>;
              if (error) return <p role="alert">{error.message}</p>;
              return <h2>{data.name}</h2>;
            }
        """,
        lang="jsx",
        time="O(1) work per url change (network-bound)", space="O(size of the response)",
        follow=[
            ("How would you add a cache so revisiting `/api/users/1` shows data instantly?", "আবার `/api/users/1`-এ গেলে সাথে সাথে data দেখাতে cache কীভাবে যোগ করবে?"),
            ("How does the `ignore` flag pattern compare to `AbortController`?", "`ignore` flag pattern আর `AbortController`-এর তুলনা কেমন?"),
        ],
        related=["react-013", "react-012"],
        refs=[R_CUSTOM_HOOKS, R_USEEFFECT, R_NO_EFFECT],
    ),
    # ------------------------------------------------------------------ react-016
    Q(
        id="react-016", sub="Forms and Actions", diff="medium", type="conceptual",
        prio="high", market="both", mins=7,
        tags=["actions", "useactionstate", "useformstatus", "useoptimistic", "forms"],
        ver="React 19.3 (Actions since React 19.0)", vs=True, status="stable",
        q_en=r"""How do React 19 Actions work for forms? Explain `useActionState`, `useFormStatus` and `useOptimistic` with an example.""",
        q_bn=r"""React 19-এর Action form-এর ক্ষেত্রে কীভাবে কাজ করে? একটা উদাহরণ দিয়ে `useActionState`, `useFormStatus` আর `useOptimistic` ব্যাখ্যা করো।""",
        a_en=r"""
            An **Action** is an async function that React runs inside a transition. If you pass a function to `<form action={fn}>`, React calls it with the form's `FormData`, tracks the pending state, and resets uncontrolled fields when it succeeds — no `onSubmit` + `preventDefault` + manual loading flags.

            - **`useActionState(action, initialState)`** returns `[state, formAction, isPending]`. Your action receives `(previousState, formData)` and whatever it returns becomes the new `state` — perfect for validation errors or a success message.
            - **`useFormStatus()`** (from `react-dom`) gives `{ pending, data, method, action }` for the **parent** form. It must be called in a component rendered *inside* the `<form>`, typically a reusable `SubmitButton`.
            - **`useOptimistic(state, updateFn)`** shows a temporary value while an Action is pending — e.g. a new comment appears instantly. When the Action finishes, React switches back to the real `state`, so if the request fails the optimistic item disappears.

            In frameworks like Next.js the same pattern works with Server Functions (`'use server'`).
        """,
        a_bn=r"""
            **Action** হলো একটা async function, যেটা React একটা transition-এর ভেতরে চালায়। `<form action={fn}>`-এ function দিলে React form-এর `FormData` দিয়ে সেটা call করে, pending অবস্থা track করে, আর সফল হলে uncontrolled field reset করে — `onSubmit` + `preventDefault` + হাতে loading flag রাখার দরকার নেই।

            - **`useActionState(action, initialState)`** return করে `[state, formAction, isPending]`। তোমার action পায় `(previousState, formData)`, আর সে যা return করে সেটাই নতুন `state` — validation error বা success message-এর জন্য দারুণ।
            - **`useFormStatus()`** (`react-dom` থেকে) **parent** form-এর `{ pending, data, method, action }` দেয়। এটা অবশ্যই `<form>`-এর *ভেতরে* render হওয়া কোনো component-এ call করতে হয়, সাধারণত একটা reusable `SubmitButton`-এ।
            - **`useOptimistic(state, updateFn)`** Action pending থাকা অবস্থায় একটা সাময়িক value দেখায় — যেমন নতুন comment সাথে সাথে দেখা যায়। Action শেষ হলে React আসল `state`-এ ফিরে যায়, তাই request fail করলে optimistic item উধাও হয়ে যায়।

            Next.js-এর মতো framework-এ একই pattern Server Function (`'use server'`) দিয়েও কাজ করে।
        """,
        ex_en=r"""
            - **The `useFormStatus` trap:** calling it in the same component that renders the `<form>` always returns `pending: false`, because it reads the status of a form *above* it.
            - **Optimistic + real data:** the parent must eventually pass the updated `comments` (from server revalidation or parent state). If it doesn't, the optimistic comment vanishes when the Action ends.
            - **Optimistic updates must happen inside an Action/transition** — calling `addOptimistic` in a plain event handler logs a warning and has no effect for long.
            - **Pure update function:** `useOptimistic`'s reducer may run more than once, so generate temp ids *before* calling it (as in the code).
            - **Progressive enhancement:** with Server Functions in a framework, `useActionState` forms can submit before JavaScript loads (optionally with a permalink as the third argument).
        """,
        ex_bn=r"""
            - **`useFormStatus`-এর ফাঁদ:** যে component `<form>` render করে, সেখানেই call করলে সবসময় `pending: false` আসে, কারণ এটা তার *উপরের* form-এর status পড়ে।
            - **Optimistic + আসল data:** parent-কে শেষ পর্যন্ত update হওয়া `comments` পাঠাতে হবে (server revalidation বা parent state থেকে)। না পাঠালে Action শেষ হওয়ার সাথে সাথে optimistic comment উধাও হয়ে যায়।
            - **Optimistic update অবশ্যই Action/transition-এর ভেতরে হতে হবে** — সাধারণ event handler-এ `addOptimistic` call করলে warning আসে আর এর প্রভাব বেশিক্ষণ থাকে না।
            - **Pure update function:** `useOptimistic`-এর reducer একাধিকবার চলতে পারে, তাই temp id call করার *আগেই* তৈরি করো (code-এ যেমন আছে)।
            - **Progressive enhancement:** framework-এ Server Function ব্যবহার করলে `useActionState` form JavaScript load হওয়ার আগেও submit হতে পারে (চাইলে তৃতীয় argument হিসেবে permalink দেওয়া যায়)।
        """,
        tip_en=r"""Explain the problem Actions solve first (boilerplate for pending/error/reset), then each hook in one sentence, then the `useFormStatus` placement gotcha. A small optimistic-UI example makes the answer memorable.""",
        tip_bn=r"""আগে বলো Action কোন সমস্যা সমাধান করে (pending/error/reset-এর boilerplate), তারপর প্রতিটা hook এক বাক্যে, তারপর `useFormStatus` কোথায় call করতে হয় সেই gotcha। ছোট একটা optimistic-UI উদাহরণ দিলে উত্তরটা মনে রাখার মতো হয়।""",
        mist_en=r"""Calling `useFormStatus` in the form's own component, using the old `useFormState` name (renamed to `useActionState`), or forgetting that the optimistic value reverts when the Action ends.""",
        mist_bn=r"""Form-এর নিজের component-এ `useFormStatus` call করা, পুরনো `useFormState` নাম ব্যবহার করা (এখন `useActionState`), অথবা ভুলে যাওয়া যে Action শেষ হলে optimistic value ফিরে যায়।""",
        code=r"""
            import { useActionState, useOptimistic } from 'react';
            import { useFormStatus } from 'react-dom';

            function SubmitButton() {
              const { pending } = useFormStatus(); // reads the parent <form>
              return <button disabled={pending}>{pending ? 'Posting…' : 'Post'}</button>;
            }

            export default function Comments({ comments, addComment }) {
              const [optimisticComments, addOptimistic] = useOptimistic(
                comments,
                (current, newComment) => [...current, { ...newComment, sending: true }]
              );

              const [error, formAction] = useActionState(async (prevError, formData) => {
                const text = String(formData.get('text') ?? '').trim();
                if (!text) return 'Comment cannot be empty';

                addOptimistic({ id: crypto.randomUUID(), text });
                try {
                  await addComment(text); // API call or Server Function; parent refreshes `comments`
                  return null;
                } catch {
                  return 'Could not post. Please try again.';
                }
              }, null);

              return (
                <>
                  <ul>
                    {optimisticComments.map((c) => (
                      <li key={c.id} style={{ opacity: c.sending ? 0.5 : 1 }}>{c.text}</li>
                    ))}
                  </ul>
                  <form action={formAction}>
                    <input name="text" aria-label="Comment" />
                    <SubmitButton />
                    {error && <p role="alert">{error}</p>}
                  </form>
                </>
              );
            }
        """,
        lang="jsx",
        follow=[
            ("How would you show field-level validation errors returned from a Server Function?", "Server Function থেকে আসা field-level validation error কীভাবে দেখাবে?"),
            ("What happens to the optimistic comment if `addComment` throws?", "`addComment` throw করলে optimistic comment-এর কী হয়?"),
        ],
        related=["react-005"],
        refs=[R_USEACTIONSTATE, R_USEFORMSTATUS, R_USEOPTIMISTIC],
    ),
    # ------------------------------------------------------------------ react-024
    Q(
        id="react-024", sub="Concurrent Rendering", diff="hard", type="comparison",
        prio="medium", market="both", mins=8,
        tags=["usetransition", "usedeferredvalue", "concurrency", "performance"],
        ver="React 19.3", vs=True, status="stable",
        q_en=r"""
            Compare `useTransition` and `useDeferredValue`. A search box filters a list of 5,000 products and typing feels laggy. Which would you use, and how?
        """,
        q_bn=r"""
            `useTransition` আর `useDeferredValue`-এর তুলনা করো। একটা search box ৫,০০০ product-এর list filter করে, আর টাইপ করতে গেলে lag হয়। তুমি কোনটা ব্যবহার করবে, আর কীভাবে?
        """,
        a_en=r"""
            Both mark rendering work as **non-urgent**, so React can interrupt it and keep urgent updates (typing, clicks) responsive. The difference is *where* you hook in:

            - **`useTransition`** — you own the state update: `startTransition(() => setTab(next))`. You get `isPending` for a spinner. Since React 19 the function can be async (that's what Actions build on).
            - **`useDeferredValue(value)`** — you receive a value (often a prop or state you don't set yourself) and get a "lagging" copy. React first re-renders with the old value, then renders the new value in the background and throws that work away if the value changes again.

            For the search box I keep the input update urgent — `setQuery` directly, never inside a transition, otherwise the input itself lags. Then I pass `useDeferredValue(query)` to the list and wrap the list in `memo` (or rely on React Compiler), so the urgent re-render with the old query is cheap. I show a dimmed list while `query !== deferredQuery`.

            Concurrency doesn't make rendering 5,000 rows cheaper — it only schedules it better. If each render is still slow, I also virtualise the list. And if typing triggers network requests, I debounce them; deferring doesn't reduce requests.
        """,
        a_bn=r"""
            দুটোই rendering-এর কাজকে **non-urgent** হিসেবে চিহ্নিত করে, ফলে React সেটা থামিয়ে দিয়ে urgent update (টাইপ করা, click) responsive রাখতে পারে। পার্থক্য হলো তুমি *কোথায়* যুক্ত হও:

            - **`useTransition`** — state update তোমার নিয়ন্ত্রণে: `startTransition(() => setTab(next))`। Spinner দেখানোর জন্য `isPending` পাও। React 19 থেকে function-টা async-ও হতে পারে (Action এর উপরই তৈরি)।
            - **`useDeferredValue(value)`** — তুমি একটা value পাও (প্রায়ই এমন prop বা state যেটা তুমি নিজে set করো না), আর তার একটা "পিছিয়ে থাকা" copy পাও। React আগে পুরনো value দিয়ে re-render করে, তারপর background-এ নতুন value দিয়ে render করে, আর value আবার বদলালে সেই কাজ ফেলে দেয়।

            Search box-এর ক্ষেত্রে input update urgent রাখি — সরাসরি `setQuery`, কখনো transition-এর ভেতরে না, নইলে input নিজেই lag করবে। তারপর list-এ `useDeferredValue(query)` পাঠাই আর list-কে `memo`-তে wrap করি (অথবা React Compiler-এর উপর ভরসা করি), যাতে পুরনো query দিয়ে urgent re-render সস্তা হয়। `query !== deferredQuery` থাকা অবস্থায় list একটু ঝাপসা দেখাই।

            Concurrency ৫,০০০ row render করাকে সস্তা করে না — শুধু ভালোভাবে schedule করে। প্রতিটা render এখনো ধীর হলে list virtualise-ও করি। আর টাইপ করলে network request গেলে সেগুলো debounce করি; defer করলে request কমে না।
        """,
        ex_en=r"""
            **Why `memo` matters:** with a deferred value, every keystroke causes an urgent render where the list receives the *same* old `deferredQuery`. If the list isn't memoized, it re-renders anyway and you gain nothing.

            **Deferred vs debounce/throttle:** debouncing waits a fixed time even on fast devices; deferred rendering starts immediately, adapts to device speed and is interruptible. But it doesn't reduce work sent to a server.

            **Interaction with Suspense:** a transition keeps showing the current UI instead of falling back to a Suspense fallback when new content suspends — great for tab switches.

            **React 19.x details:** `useDeferredValue(value, initialValue)` accepts an initial value for the first render; in 19.3 transitions render independently, so a slow transition no longer holds up unrelated ones.
        """,
        ex_bn=r"""
            **`memo` কেন জরুরি:** deferred value থাকলে প্রতিটা keystroke-এ একটা urgent render হয়, যেখানে list *একই* পুরনো `deferredQuery` পায়। List memoized না হলে সেটা তবুও re-render হয়, ফলে কোনো লাভই হয় না।

            **Deferred বনাম debounce/throttle:** debounce দ্রুত device-এও নির্দিষ্ট সময় অপেক্ষা করে; deferred rendering সাথে সাথে শুরু হয়, device-এর গতির সাথে মানিয়ে নেয় আর মাঝপথে থামানো যায়। তবে এটা server-এ পাঠানো কাজ কমায় না।

            **Suspense-এর সাথে সম্পর্ক:** নতুন content suspend করলে transition Suspense fallback-এ না গিয়ে বর্তমান UI দেখাতে থাকে — tab বদলানোর জন্য দারুণ।

            **React 19.x-এর খুঁটিনাটি:** `useDeferredValue(value, initialValue)` প্রথম render-এর জন্য একটা initial value নেয়; 19.3-এ transition-গুলো আলাদাভাবে render হয়, ফলে একটা ধীর transition অন্য অসম্পর্কিত transition-কে আটকে রাখে না।
        """,
        tip_en=r"""Frame it as "who owns the update?" — that one question decides between the two. Then show you know the pitfalls (input inside a transition, missing memo) and the limits (doesn't replace virtualisation or debouncing).""",
        tip_bn=r"""প্রশ্নটা এভাবে সাজাও: "update-টা কার নিয়ন্ত্রণে?" — এই একটা প্রশ্নই দুটোর মধ্যে বেছে নিতে সাহায্য করে। তারপর দেখাও তুমি ফাঁদগুলো জানো (transition-এর ভেতরে input, memo না থাকা) আর সীমাবদ্ধতাও জানো (virtualisation বা debounce-এর বিকল্প না)।""",
        mist_en=r"""Wrapping the controlled input's own `setState` in `startTransition`, or expecting `useDeferredValue` to make the expensive list faster by itself.""",
        mist_bn=r"""Controlled input-এর নিজের `setState`-কে `startTransition`-এ wrap করা, অথবা আশা করা যে `useDeferredValue` নিজে থেকেই expensive list-কে দ্রুত করে দেবে।""",
        code=r"""
            import { memo, useDeferredValue, useState } from 'react';

            const ResultList = memo(function ResultList({ query }) {
              const items = filterProducts(query); // expensive for 5,000 items
              return (
                <ul>
                  {items.map((p) => <li key={p.id}>{p.name}</li>)}
                </ul>
              );
            });

            export default function Search() {
              const [query, setQuery] = useState('');
              const deferredQuery = useDeferredValue(query);
              const isStale = query !== deferredQuery;

              return (
                <>
                  <input value={query} onChange={(e) => setQuery(e.target.value)} />
                  <div style={{ opacity: isStale ? 0.6 : 1 }}>
                    <ResultList query={deferredQuery} />
                  </div>
                </>
              );
            }
        """,
        lang="jsx",
        extra=[dict(lang="jsx", label_en="useTransition when you own the update (tabs)", label_bn="Update তোমার নিয়ন্ত্রণে থাকলে useTransition (tabs)", src=r"""
            import { useState, useTransition } from 'react';

            function Tabs() {
              const [tab, setTab] = useState('about');
              const [isPending, startTransition] = useTransition();

              function selectTab(next) {
                startTransition(() => setTab(next)); // the slow tab can be interrupted
              }

              return (
                <>
                  <TabButtons current={tab} onSelect={selectTab} />
                  {isPending && <Spinner />}
                  <TabContent tab={tab} />
                </>
              );
            }
        """)],
        follow=[
            ("Why shouldn't a controlled input's state update be marked as a transition?", "Controlled input-এর state update কেন transition হিসেবে চিহ্নিত করা উচিত না?"),
            ("How do transitions change what the user sees when a component suspends?", "কোনো component suspend করলে transition user-এর দেখা UI কীভাবে বদলায়?"),
        ],
        related=["react-014"],
        refs=[R_USETRANSITION, R_USEDEFERRED, R_MEMO],
    ),
    # ------------------------------------------------------------------ react-031
    Q(
        id="react-031", sub="Migration to React 19 and React Compiler", diff="extreme", type="scenario",
        prio="medium", market="international", mins=20,
        tags=["migration", "react-19", "react-compiler", "codemods", "legacy"],
        ver="React 19.3 + React Compiler 1.0", vs=True, status="stable",
        q_en=r"""
            You own a five-year-old, 400k-line React 17 SPA built with Create React App. Leadership wants it on React 19 with React Compiler enabled, without disrupting releases. How do you plan and execute the migration?
        """,
        q_bn=r"""
            তোমার দায়িত্বে পাঁচ বছরের পুরনো, ৪ লাখ লাইনের একটা React 17 SPA, যেটা Create React App দিয়ে তৈরি। Leadership চায় release বন্ধ না করে এটা React 19-এ নিয়ে যেতে আর React Compiler চালু করতে। Migration কীভাবে plan আর execute করবে?
        """,
        a_en=r"""
            *(Advanced, senior-level scenario.)* I'd split it into independent, reversible steps so that each one can ship on its own.

            1. **Tooling first.** Create React App is deprecated, so I move the build to Vite (or a framework if we also want SSR) while staying on the same React version. One risk at a time.
            2. **React 18.3 as a stepping stone.** It's 18.2 plus warnings for everything React 19 removes. I switch `ReactDOM.render` to `createRoot` (this also enables automatic batching and concurrent features, so I test carefully), then fix the warnings: string refs, legacy context (`contextTypes`), `propTypes`/`defaultProps` on function components, `findDOMNode`, `react-dom/test-utils`.
            3. **Codemods + dependencies.** Run `npx codemod@latest react/19/migration-recipe` and `npx types-react-codemod@latest preset-19`, then audit third-party libraries (router, state management, UI kits, testing libraries) for React 19 peer support.
            4. **Upgrade to React 19** on a branch with the full test suite and StrictMode enabled. Watch for TypeScript changes (e.g. `useRef` needs an argument, ref callbacks can return a cleanup) and for error-reporting changes: wire `onUncaughtError`/`onCaughtError` on `createRoot` into monitoring.
            5. **Progressive rollout:** canary or percentage release, compare error rates and Web Vitals, keep a rollback path.
            6. **React Compiler last.** Enable the compiler-powered lint rules first and fix Rules-of-React violations. Then adopt incrementally — per directory via Babel overrides, or `compilationMode: 'annotation'` with `"use memo"` — and opt problem components out with `"use no memo"`. Measure with the Profiler; keep existing `useMemo`/`useCallback` until tested.

            Only after that would I adopt new APIs (Actions, `use`, `ref` as a prop) feature by feature.
        """,
        a_bn=r"""
            *(Advanced, senior-level scenario।)* আমি কাজটা স্বাধীন আর ফিরিয়ে নেওয়া যায় এমন ধাপে ভাগ করব, যাতে প্রতিটা ধাপ আলাদাভাবে ship করা যায়।

            1. **আগে tooling.** Create React App deprecated, তাই একই React version-এ থেকেই build Vite-এ (বা SSR লাগলে কোনো framework-এ) সরাই। একবারে একটাই ঝুঁকি।
            2. **মধ্যবর্তী ধাপ React 18.3.** এটা 18.2-ই, শুধু React 19-এ যা সরানো হয়েছে সবকিছুর জন্য warning দেয়। `ReactDOM.render` থেকে `createRoot`-এ যাই (এতে automatic batching আর concurrent feature চালু হয়, তাই সাবধানে test করি), তারপর warning ঠিক করি: string ref, legacy context (`contextTypes`), function component-এ `propTypes`/`defaultProps`, `findDOMNode`, `react-dom/test-utils`।
            3. **Codemod + dependency.** `npx codemod@latest react/19/migration-recipe` আর `npx types-react-codemod@latest preset-19` চালাই, তারপর third-party library (router, state management, UI kit, testing library) React 19 peer support দেয় কি না যাচাই করি।
            4. **React 19-এ upgrade** একটা branch-এ, পুরো test suite আর StrictMode চালু রেখে। TypeScript পরিবর্তনগুলো খেয়াল করি (যেমন `useRef`-এ argument লাগে, ref callback cleanup return করতে পারে), আর error reporting-এর পরিবর্তন: `createRoot`-এর `onUncaughtError`/`onCaughtError` monitoring-এর সাথে যুক্ত করি।
            5. **ধাপে ধাপে rollout:** canary বা percentage release, error rate আর Web Vitals তুলনা, আর rollback-এর পথ খোলা রাখা।
            6. **সবশেষে React Compiler.** আগে compiler-চালিত lint rule চালু করে Rules of React লঙ্ঘন ঠিক করি। তারপর ধাপে ধাপে গ্রহণ — Babel overrides দিয়ে directory অনুযায়ী, অথবা `compilationMode: 'annotation'` আর `"use memo"` দিয়ে — আর সমস্যাওয়ালা component `"use no memo"` দিয়ে বাদ দিই। Profiler দিয়ে মাপি; test না করা পর্যন্ত বিদ্যমান `useMemo`/`useCallback` রেখে দিই।

            এরপরই কেবল feature ধরে ধরে নতুন API (Action, `use`, prop হিসেবে `ref`) গ্রহণ করব।
        """,
        ex_en=r"""
            **Why this order**
            - Changing the bundler, the React major and the compiler at once makes failures impossible to attribute. Each step should be releasable and revertible.
            - The jump to `createRoot` is the real behavioural change for a React 17 app: automatic batching changes how many renders happen in timeouts/promises, and StrictMode in dev double-invokes effects, exposing missing cleanups that were always bugs.

            **Risk management**
            - Libraries that use removed APIs (e.g. `findDOMNode`) block the upgrade — budget time to replace them.
            - Feature flags and canary releases limit blast radius; error boundaries + `onCaughtError` reporting catch regressions early.
            - The compiler is safe only for code that follows the Rules of React. Components that mutate props/state or read refs during render will be skipped or behave differently; lint first, compile second.

            **Communication:** publish a migration guide for teams, track progress per directory, and set a deadline for removing deprecated patterns.
        """,
        ex_bn=r"""
            **কেন এই ক্রম**
            - Bundler, React major আর compiler একসাথে বদলালে কোন failure কোন কারণে, তা বের করা অসম্ভব হয়ে যায়। প্রতিটা ধাপ আলাদাভাবে release আর revert করা যাওয়া উচিত।
            - React 17 app-এর জন্য আসল আচরণগত পরিবর্তন হলো `createRoot`-এ যাওয়া: automatic batching timeout/promise-এর ভেতরে কতবার render হবে তা বদলে দেয়, আর dev-এ StrictMode effect দুইবার চালিয়ে missing cleanup ধরিয়ে দেয় — যেগুলো আসলে সবসময়ই bug ছিল।

            **ঝুঁকি ব্যবস্থাপনা**
            - যেসব library সরানো API ব্যবহার করে (যেমন `findDOMNode`), সেগুলো upgrade আটকে দেয় — replace করার জন্য সময় রাখো।
            - Feature flag আর canary release ক্ষতির পরিধি সীমিত রাখে; error boundary + `onCaughtError` reporting regression আগেভাগে ধরে।
            - Compiler শুধু Rules of React মানা code-এর জন্য নিরাপদ। যেসব component props/state mutate করে বা render-এর সময় ref পড়ে, সেগুলো skip হবে বা ভিন্ন আচরণ করবে; আগে lint, পরে compile।

            **যোগাযোগ:** team-গুলোর জন্য migration guide প্রকাশ করো, directory অনুযায়ী অগ্রগতি track করো, আর deprecated pattern সরানোর একটা deadline ঠিক করো।
        """,
        tip_en=r"""Present a phased plan with a clear "why this order" and a rollback story. Naming the 18.3 stepping stone, the official codemods and incremental compiler adoption shows you've actually read the upgrade path rather than guessing.""",
        tip_bn=r""""কেন এই ক্রম" আর rollback-এর পরিকল্পনাসহ একটা ধাপে ধাপে plan উপস্থাপন করো। 18.3 মধ্যবর্তী ধাপ, official codemod আর compiler-এর incremental adoption-এর কথা বললে বোঝা যায় তুমি আসলেই upgrade path পড়েছ, অনুমান করছ না।""",
        mist_en=r"""A big-bang upgrade of bundler + React + compiler in one PR, enabling the compiler on code that breaks the Rules of React, or removing all `useMemo`/`useCallback` immediately "because the compiler handles it".""",
        mist_bn=r"""এক PR-এ bundler + React + compiler সব একসাথে upgrade করা, Rules of React ভাঙে এমন code-এ compiler চালু করা, অথবা "compiler সামলাবে" ভেবে সাথে সাথে সব `useMemo`/`useCallback` মুছে ফেলা।""",
        code=r"""
            // Before (React 17) — removed in React 19
            import ReactDOM from 'react-dom';
            ReactDOM.render(<App />, document.getElementById('root'));

            // After (React 18.3 / 19)
            import { createRoot } from 'react-dom/client';

            const root = createRoot(document.getElementById('root'), {
              onUncaughtError(error, errorInfo) {
                reportError(error, { componentStack: errorInfo.componentStack });
              },
              onCaughtError(error, errorInfo) {
                // errors handled by an error boundary
                reportError(error, { componentStack: errorInfo.componentStack, handled: true });
              },
            });
            root.render(<App />);

            // Temporarily keep a problematic component out of React Compiler
            function LegacyChart(props) {
              'use no memo';
              // ...
            }
        """,
        lang="jsx",
        follow=[
            ("How would you find which third-party libraries block the React 19 upgrade?", "কোন third-party library React 19 upgrade আটকে দিচ্ছে, সেটা কীভাবে খুঁজে বের করবে?"),
            ("How do you prove the compiler actually improved performance?", "Compiler যে আসলেই performance বাড়িয়েছে, সেটা কীভাবে প্রমাণ করবে?"),
        ],
        related=["react-014", "react-013"],
        refs=[R_UPGRADE19, R_COMPILER_INC, R_CREATEROOT],
    ),
]

if __name__ == "__main__":
    save("react", "b2", QUESTIONS)
