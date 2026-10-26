# React — batch 3 (react-008..010, 017..019, 025, 026)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_CTX = ("react.dev — createContext", "https://react.dev/reference/react/createContext")
R_USECTX = ("react.dev — useContext", "https://react.dev/reference/react/useContext")
R_CTX_LEARN = ("react.dev — Passing Data Deeply with Context", "https://react.dev/learn/passing-data-deeply-with-context")
R_USE = ("react.dev — use", "https://react.dev/reference/react/use")
R_REF_PROP = ("react.dev — Manipulating the DOM with Refs", "https://react.dev/learn/manipulating-the-dom-with-refs")
R_FORWARDREF = ("react.dev — forwardRef", "https://react.dev/reference/react/forwardRef")
R_REACT19 = ("react.dev — React v19", "https://react.dev/blog/2024/12/05/react-19")
R_LAZY = ("react.dev — lazy", "https://react.dev/reference/react/lazy")
R_SUSPENSE = ("react.dev — Suspense", "https://react.dev/reference/react/Suspense")
R_RTK = ("Redux Toolkit (GitHub, official)", "https://github.com/reduxjs/redux-toolkit")
R_USESES = ("react.dev — useSyncExternalStore", "https://react.dev/reference/react/useSyncExternalStore")
R_USEEFFECT = ("react.dev — useEffect", "https://react.dev/reference/react/useEffect")
R_DEPS = ("react.dev — Removing Effect Dependencies", "https://react.dev/learn/removing-effect-dependencies")
R_BOUNDARY = ("react.dev — Component (error boundaries)", "https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary")
R_REB = ("react-error-boundary (GitHub)", "https://github.com/bvaughn/react-error-boundary")
R_PROFILER = ("react.dev — <Profiler>", "https://react.dev/reference/react/Profiler")
R_PERF_TRACKS = ("react.dev — React Performance Tracks", "https://react.dev/reference/dev-tools/react-performance-tracks")
R_INP = ("web.dev — Interaction to Next Paint (INP)", "https://web.dev/articles/inp")
R_USEMEMO = ("react.dev — useMemo", "https://react.dev/reference/react/useMemo")

QUESTIONS = [
    # ------------------------------------------------------------------ react-008
    Q(
        id="react-008", sub="Context API", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["context", "usecontext", "prop-drilling", "react-19"],
        ver="React 19.3", vs=True, status="stable",
        q_en=r"""What problem does the Context API solve, and how do you create, provide and read a context in React 19?""",
        q_bn=r"""Context API কোন সমস্যার সমাধান করে? React 19-এ কীভাবে context তৈরি, provide আর read করো?""",
        a_en=r"""
            Context solves **prop drilling** — passing the same data (theme, logged-in user, locale) through many components that don't use it, just to reach a deep child.

            1. Create it: `const ThemeContext = createContext('light')` — the argument is the default value used when there's no provider above.
            2. Provide it: in React 19 you render the context itself, `<ThemeContext value={theme}>…</ThemeContext>`. The older `<ThemeContext.Provider>` still works but is the legacy form.
            3. Read it: `useContext(ThemeContext)` or `use(ThemeContext)` in any component below. `use` can even be called inside conditions.

            A component always reads the **nearest** provider above it, so you can override values for a subtree.
        """,
        a_bn=r"""
            Context **prop drilling**-এর সমস্যা সমাধান করে — একই data (theme, logged-in user, locale) এমন অনেক component-এর ভেতর দিয়ে পাঠানো, যারা নিজেরা সেটা ব্যবহারই করে না, শুধু গভীরে থাকা কোনো child-এর কাছে পৌঁছানোর জন্য।

            1. তৈরি করো: `const ThemeContext = createContext('light')` — argument-টা default value, উপরে কোনো provider না থাকলে এটাই ব্যবহার হয়।
            2. Provide করো: React 19-এ context-টাকেই render করো, `<ThemeContext value={theme}>…</ThemeContext>`। পুরনো `<ThemeContext.Provider>` এখনো কাজ করে, তবে এটা legacy form।
            3. Read করো: নিচের যেকোনো component-এ `useContext(ThemeContext)` বা `use(ThemeContext)`। `use` এমনকি condition-এর ভেতরেও call করা যায়।

            একটা component সবসময় তার উপরের **সবচেয়ে কাছের** provider থেকে পড়ে, তাই কোনো subtree-র জন্য value override করা যায়।
        """,
        quick_en=r"""Context fixes prop drilling: passing data like theme or user through many components that don't need it. Create it with `createContext(default)`, provide it in React 19 with `<ThemeContext value={...}>`, and read the nearest value with `useContext` or `use`.""",
        quick_bn=r"""Context prop drilling-এর সমস্যা মেটায়: theme বা user-এর মতো data এমন অনেক component-এর ভেতর দিয়ে পাঠানো, যাদের সেটা লাগে না। `createContext(default)` দিয়ে বানাও, React 19-এ `<ThemeContext value={...}>` দিয়ে provide করো, আর `useContext` বা `use` দিয়ে সবচেয়ে কাছের value পড়ো।""",
        ex_en=r"""
            - **Context is transport, not state management.** It just delivers a value; the state usually lives in `useState`/`useReducer` in the provider component.
            - **Re-renders:** when the provider's `value` changes (by `Object.is`), every component reading that context re-renders, even if it's wrapped in `memo`. Passing a new object literal every render therefore re-renders all consumers — memoize the value or split contexts.
            - **Try composition first:** often you can avoid drilling by passing JSX as `children` instead of passing data down.
            - **Server Components (19.3):** a Server Component can render `<SomeContext value={…}>` when the context is imported from a `'use client'` module, but it still can't create or read context.
        """,
        ex_bn=r"""
            - **Context হলো পরিবহনের মাধ্যম, state management না।** এটা শুধু একটা value পৌঁছে দেয়; state সাধারণত provider component-এর `useState`/`useReducer`-এ থাকে।
            - **Re-render:** provider-এর `value` বদলালে (`Object.is` অনুযায়ী) ওই context পড়া প্রতিটা component re-render হয়, `memo`-তে wrap করা থাকলেও। তাই প্রতিটা render-এ নতুন object literal পাঠালে সব consumer re-render হয় — value memoize করো বা context ভাগ করো।
            - **আগে composition চেষ্টা করো:** অনেক সময় data নিচে না পাঠিয়ে JSX-কে `children` হিসেবে পাঠালেই drilling এড়ানো যায়।
            - **Server Component (19.3):** context যদি কোনো `'use client'` module থেকে import করা হয়, Server Component `<SomeContext value={…}>` render করতে পারে, কিন্তু এখনো context তৈরি বা read করতে পারে না।
        """,
        tip_en=r"""Name the problem (prop drilling), show the three steps, and mention the React 19 `<Context value>` syntax. Adding "every consumer re-renders when the value changes" shows you know the performance cost.""",
        tip_bn=r"""সমস্যার নাম বলো (prop drilling), তিনটা ধাপ দেখাও, আর React 19-এর `<Context value>` syntax উল্লেখ করো। "value বদলালে প্রতিটা consumer re-render হয়" — এটা যোগ করলে বোঝা যায় তুমি performance-এর খরচটাও জানো।""",
        mist_en=r"""Putting all app state into one giant context, or forgetting that without a provider the default value is used silently.""",
        mist_bn=r"""পুরো app-এর state একটা বিশাল context-এ রেখে দেওয়া, অথবা ভুলে যাওয়া যে provider না থাকলে চুপচাপ default value ব্যবহার হয়।""",
        code=r"""
            import { createContext, use, useState } from 'react';

            const ThemeContext = createContext('light');

            export default function App() {
              const [theme, setTheme] = useState('dark');
              return (
                <ThemeContext value={theme}>
                  <Toolbar />
                  <button onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}>
                    Toggle theme
                  </button>
                </ThemeContext>
              );
            }

            function Toolbar() {
              return <SaveButton />; // no theme prop drilled through here
            }

            function SaveButton() {
              const theme = use(ThemeContext); // or useContext(ThemeContext)
              return <button className={`btn btn-${theme}`}>Save</button>;
            }
        """,
        lang="jsx",
        follow=[
            ("Why might a component wrapped in `memo` still re-render because of context?", "`memo`-তে wrap করা component-ও context-এর কারণে কেন re-render হতে পারে?"),
            ("When would you choose Redux Toolkit or Zustand instead of Context?", "কখন Context-এর বদলে Redux Toolkit বা Zustand বেছে নেবে?"),
        ],
        related=["react-002"],
        refs=[R_CTX, R_CTX_LEARN, R_USE],
    ),
    # ------------------------------------------------------------------ react-009
    Q(
        id="react-009", sub="Refs and DOM Access", diff="easy", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["refs", "ref-as-prop", "forwardref", "react-19"],
        ver="React 19.3 (ref as a prop since React 19.0)", vs=True, status="stable",
        q_en=r"""In a React 19 app, your own function component `TextInput` renders an `<input>`. How should it let a parent component focus that input?""",
        q_bn=r"""একটা React 19 app-এ তোমার নিজের function component `TextInput` একটা `<input>` render করে। Parent component যাতে ওই input-এ focus করতে পারে, তার জন্য কী করা উচিত?""",
        options=[
            ("Wrap it in `forwardRef`, because function components can't receive `ref`", "`forwardRef`-এ wrap করো, কারণ function component `ref` পেতে পারে না"),
            ("Accept `ref` as a regular prop and pass it to the `<input>`", "`ref`-কে সাধারণ prop হিসেবে নাও আর `<input>`-এ পাঠিয়ে দাও"),
            ("Use a string ref (`ref=\"input\"`) and read `this.refs.input` in the parent", "String ref (`ref=\"input\"`) ব্যবহার করো আর parent-এ `this.refs.input` পড়ো"),
            ("Call `ReactDOM.findDOMNode()` in the parent to get the input", "Input পেতে parent-এ `ReactDOM.findDOMNode()` call করো"),
        ],
        correct=1,
        a_en=r"""Since React 19, function components receive `ref` as a normal prop. `function TextInput({ ref, ...props }) { return <input ref={ref} {...props} />; }` is enough — no `forwardRef` wrapper needed.""",
        a_bn=r"""React 19 থেকে function component `ref`-কে সাধারণ prop হিসেবে পায়। `function TextInput({ ref, ...props }) { return <input ref={ref} {...props} />; }` লিখলেই চলে — `forwardRef` wrapper লাগে না।""",
        quick_en=r"""Accept `ref` as a regular prop and pass it to the `<input>`: since React 19, function components receive `ref` like any other prop, so `forwardRef` is no longer needed.""",
        quick_bn=r"""`ref`-কে সাধারণ prop হিসেবে নিয়ে `<input>`-এ পাঠিয়ে দাও: React 19 থেকে function component অন্য prop-এর মতোই `ref` পায়, তাই `forwardRef` আর লাগে না।""",
        ex_en=r"""
            The tempting answer is `forwardRef`, because that was required for years and you'll still see it everywhere. It still works in React 19, but it's no longer needed for function components and React plans to deprecate it; you only keep it if your library must support React 18.

            String refs and `findDOMNode` were **removed** in React 19 (they were legacy class-component APIs). Related React 19 improvements: ref callbacks can now return a cleanup function, and `useImperativeHandle` is still the way to expose a limited API (e.g. only `focus()`) instead of the raw DOM node.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো `forwardRef`, কারণ বছরের পর বছর এটা বাধ্যতামূলক ছিল আর এখনো সব জায়গায় দেখা যায়। React 19-এও এটা কাজ করে, কিন্তু function component-এর জন্য আর দরকার নেই, আর React এটাকে deprecate করার পরিকল্পনা করছে; তোমার library-কে React 18 support করতে হলেই কেবল রাখবে।

            String ref আর `findDOMNode` React 19-এ **সরিয়ে ফেলা হয়েছে** (এগুলো ছিল legacy class-component API)। React 19-এর সংশ্লিষ্ট উন্নতি: ref callback এখন একটা cleanup function return করতে পারে, আর raw DOM node-এর বদলে সীমিত API (যেমন শুধু `focus()`) expose করতে এখনো `useImperativeHandle`-ই উপায়।
        """,
        tip_en=r"""Say what changed in React 19 and why `forwardRef` still appears in codebases. Interviewers like candidates who can read old code and know the current pattern.""",
        tip_bn=r"""React 19-এ কী বদলেছে আর codebase-এ এখনো কেন `forwardRef` দেখা যায় — দুটোই বলো। যে candidate পুরনো code পড়তে পারে আর বর্তমান pattern-ও জানে, interviewer তাকে পছন্দ করে।""",
        refs=[R_REACT19, R_REF_PROP, R_FORWARDREF],
    ),
    # ------------------------------------------------------------------ react-010
    Q(
        id="react-010", sub="Suspense and Lazy Loading", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["lazy", "suspense", "code-splitting"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""You write `const Chart = lazy(() => import('./Chart'))` and render `<Chart />`. Which statement is correct?""",
        q_bn=r"""তুমি লিখলে `const Chart = lazy(() => import('./Chart'))` আর `<Chart />` render করলে। কোন কথাটা সঠিক?""",
        options=[
            ("`./Chart` must provide a default export, and a `<Suspense>` boundary above `<Chart />` shows a fallback while the code loads", "`./Chart`-এ default export থাকতে হবে, আর code load হওয়ার সময় `<Chart />`-এর উপরের একটা `<Suspense>` boundary fallback দেখায়"),
            ("`lazy` picks up named exports automatically, so `export function Chart` works without changes", "`lazy` নিজে থেকেই named export ধরে নেয়, তাই `export function Chart` কোনো পরিবর্তন ছাড়াই কাজ করে"),
            ("No `<Suspense>` is needed; React renders `null` until the chunk arrives", "`<Suspense>` লাগে না; chunk না আসা পর্যন্ত React `null` render করে"),
            ("Call `lazy` inside the component body so the import only happens on demand", "Component-এর body-র ভেতরে `lazy` call করো, যাতে দরকার হলেই কেবল import হয়"),
        ],
        correct=0,
        a_en=r"""`lazy` expects a function returning a promise for a module with a **default export** that is a component. While the code downloads, the component suspends, and the nearest `<Suspense fallback={...}>` above it shows the fallback.""",
        a_bn=r"""`lazy` এমন একটা function চায়, যেটা এমন module-এর promise return করে যার **default export** একটা component। Code download হওয়ার সময় component-টা suspend করে, আর তার উপরের সবচেয়ে কাছের `<Suspense fallback={...}>` fallback দেখায়।""",
        quick_en=r"""`./Chart` must have a default export, and a `<Suspense>` boundary above `<Chart />` shows a fallback while its code downloads. `lazy` expects a promise for a module whose default export is a component.""",
        quick_bn=r"""`./Chart`-এ একটা default export থাকতে হবে, আর code download হওয়ার সময় `<Chart />`-এর উপরের `<Suspense>` boundary fallback দেখায়। `lazy` এমন একটা module-এর promise চায় যার default export একটা component।""",
        ex_en=r"""
            The most tempting wrong option is "no Suspense needed" — without a boundary above, the suspension has nowhere to show a fallback, so React suspends a much larger part of the tree (or the root), which is rarely what you want.

            Named exports need a small adapter: `lazy(() => import('./Chart').then((m) => ({ default: m.Chart })))`. Always declare `lazy` at the **top level** of a module: calling it inside a component creates a new component type on every render, which resets its state.

            Production tips: wrap lazy parts in an error boundary too (a chunk can fail to load after a deploy), and preload on hover/intent by calling the `import()` early. In Next.js, routes are code-split automatically and `next/dynamic` covers similar cases.
        """,
        ex_bn=r"""
            সবচেয়ে লোভনীয় ভুল option হলো "Suspense লাগে না" — উপরে কোনো boundary না থাকলে suspension-এর fallback দেখানোর জায়গা থাকে না, তাই React tree-র অনেক বড় অংশ (বা root) suspend করে দেয়, যেটা প্রায় কখনোই কাম্য না।

            Named export-এর জন্য ছোট একটা adapter লাগে: `lazy(() => import('./Chart').then((m) => ({ default: m.Chart })))`। `lazy` সবসময় module-এর **top level**-এ declare করো: component-এর ভেতরে call করলে প্রতিটা render-এ নতুন component type তৈরি হয়, ফলে তার state reset হয়ে যায়।

            Production tip: lazy অংশগুলোকে error boundary দিয়েও wrap করো (deploy-এর পর কোনো chunk load fail করতে পারে), আর hover/intent-এর সময় আগেভাগে `import()` call করে preload করো। Next.js-এ route নিজে থেকেই code-split হয়, আর একই ধরনের কাজে `next/dynamic` আছে।
        """,
        tip_en=r"""Mention both requirements (default export + Suspense boundary) and one production concern like chunk-load failures after deployment.""",
        tip_bn=r"""দুটো শর্তই বলো (default export + Suspense boundary), আর production-এর একটা চিন্তা যোগ করো, যেমন deploy-এর পর chunk load fail করা।""",
        refs=[R_LAZY, R_SUSPENSE],
    ),
    # ------------------------------------------------------------------ react-017
    Q(
        id="react-017", sub="Redux Toolkit", diff="medium", type="conceptual",
        prio="medium", market="bangladesh", mins=6,
        tags=["redux", "redux-toolkit", "createslice", "rtk-query", "state-management"],
        ver="React 19.3 with Redux Toolkit (createSlice / RTK Query APIs)", vs=True, status="stable",
        q_en=r"""Explain the fundamentals of Redux Toolkit (store, slices, actions, reducers, selectors). When would you choose it over Context or a server-state library?""",
        q_bn=r"""Redux Toolkit-এর মূল বিষয়গুলো ব্যাখ্যা করো (store, slice, action, reducer, selector)। কখন Context বা server-state library-র বদলে এটা বেছে নেবে?""",
        a_en=r"""
            Redux Toolkit (RTK) is the official, recommended way to write Redux today.

            - **`configureStore`** creates the single store with good defaults: Redux DevTools, thunk middleware and dev-time checks for accidental mutation and non-serialisable values.
            - **`createSlice`** takes a name, initial state and "case reducers", and generates the reducer plus action creators (`itemAdded(payload)`). It uses **Immer**, so you can write `state.items.push(item)` and still get an immutable update.
            - Components **read** with `useSelector(selector)` and **write** with `useDispatch()`. A component re-renders only when the value its selector returns changes (by reference).
            - For server data, **RTK Query** (`createApi`) handles fetching, caching, deduplication and invalidation by tags.

            I pick RTK when a lot of client state is shared across distant parts of the app and changes often (carts, editors, complex filters), when the team benefits from DevTools/time-travel and a strict pattern. For server data I'd use RTK Query or TanStack Query; for simple, rarely-changing values like theme, Context is enough.
        """,
        a_bn=r"""
            Redux Toolkit (RTK) হলো এখনকার দিনে Redux লেখার official ও recommended উপায়।

            - **`configureStore`** ভালো default-সহ একটাই store তৈরি করে: Redux DevTools, thunk middleware, আর ভুল করে mutation বা non-serialisable value থাকলে dev-time check।
            - **`createSlice`** একটা name, initial state আর "case reducer" নেয়, আর reducer ও action creator (`itemAdded(payload)`) তৈরি করে দেয়। এটা **Immer** ব্যবহার করে, তাই `state.items.push(item)` লিখলেও immutable update-ই হয়।
            - Component `useSelector(selector)` দিয়ে **পড়ে** আর `useDispatch()` দিয়ে **লেখে**। Selector যে value return করে সেটা (reference অনুযায়ী) বদলালেই কেবল component re-render হয়।
            - Server data-র জন্য **RTK Query** (`createApi`) fetching, caching, deduplication আর tag দিয়ে invalidation সামলায়।

            App-এর দূরবর্তী অংশগুলোর মধ্যে অনেক client state share হলে আর ঘন ঘন বদলালে (cart, editor, জটিল filter), আর team DevTools/time-travel ও একটা কঠোর pattern থেকে উপকার পেলে আমি RTK বেছে নিই। Server data-র জন্য RTK Query বা TanStack Query; theme-এর মতো সাধারণ, কম বদলানো value-র জন্য Context-ই যথেষ্ট।
        """,
        quick_en=r"""RTK is the official way to write Redux: `configureStore` creates the store, `createSlice` generates reducers and actions (with Immer), and components use `useSelector`/`useDispatch`. Use it for large, often-changing shared client state; RTK Query or TanStack Query for server data; Context for theme.""",
        quick_bn=r"""RTK হলো Redux লেখার official উপায়: `configureStore` store বানায়, `createSlice` (Immer-সহ) reducer আর action তৈরি করে, আর component `useSelector`/`useDispatch` ব্যবহার করে। বড়, ঘনঘন বদলানো shared client state-এর জন্য এটা নিই; server data-র জন্য RTK Query বা TanStack Query, আর theme-এর মতো সহজ value-র জন্য Context।""",
        ex_en=r"""
            - **Immer only works inside `createSlice`/`createReducer`.** Mutating state anywhere else (components, selectors) is still a bug.
            - **Selector pitfalls:** `useSelector(s => s.items.filter(...))` returns a new array every time and re-renders on every store update. Use `createSelector` (Reselect, re-exported by RTK) for derived data.
            - **Normalise collections** with `createEntityAdapter` for fast lookups by id.
            - **TypeScript:** create typed hooks once, e.g. `useSelector.withTypes<RootState>()`.
            - **Context vs Redux:** Context has no selector mechanism — every consumer re-renders when the value changes — while Redux subscriptions are selective. That's the real performance difference.
        """,
        ex_bn=r"""
            - **Immer শুধু `createSlice`/`createReducer`-এর ভেতরেই কাজ করে।** অন্য কোথাও (component, selector) state mutate করা এখনো bug।
            - **Selector-এর ফাঁদ:** `useSelector(s => s.items.filter(...))` প্রতিবার নতুন array return করে, ফলে store-এর প্রতিটা update-এ re-render হয়। Derived data-র জন্য `createSelector` (Reselect, RTK নিজেই re-export করে) ব্যবহার করো।
            - **Collection normalise করো** `createEntityAdapter` দিয়ে, যাতে id দিয়ে দ্রুত খোঁজা যায়।
            - **TypeScript:** একবারই typed hook তৈরি করো, যেমন `useSelector.withTypes<RootState>()`।
            - **Context বনাম Redux:** Context-এ কোনো selector ব্যবস্থা নেই — value বদলালে প্রতিটা consumer re-render হয় — আর Redux-এর subscription selective। আসল performance পার্থক্য এটাই।
        """,
        tip_en=r"""Walk through the data flow (dispatch → reducer → new state → selectors → re-render), then say when you *wouldn't* use Redux. Distinguishing client state from server state is what senior interviewers look for.""",
        tip_bn=r"""Data flow ধরে ধরে বলো (dispatch → reducer → নতুন state → selector → re-render), তারপর বলো কখন Redux *ব্যবহার করবে না*। Client state আর server state আলাদা করে বলতে পারাটাই senior interviewer খোঁজে।""",
        mist_en=r"""Writing hand-made action types/switch reducers in new code (pre-RTK style), storing server cache in slices with manual loading flags, or returning new objects from selectors.""",
        mist_bn=r"""নতুন code-এ হাতে action type/switch reducer লেখা (RTK-এর আগের style), হাতে loading flag দিয়ে server cache slice-এ রাখা, অথবা selector থেকে নতুন object return করা।""",
        code=r"""
            // features/cart/cartSlice.js
            import { createSlice } from '@reduxjs/toolkit';

            const cartSlice = createSlice({
              name: 'cart',
              initialState: { items: [] },
              reducers: {
                itemAdded(state, action) {
                  // Immer: looks like mutation, produces a new immutable state
                  const existing = state.items.find((i) => i.id === action.payload.id);
                  if (existing) existing.qty += 1;
                  else state.items.push({ ...action.payload, qty: 1 });
                },
                itemRemoved(state, action) {
                  state.items = state.items.filter((i) => i.id !== action.payload);
                },
              },
            });

            export const { itemAdded, itemRemoved } = cartSlice.actions;
            export const selectCartCount = (state) =>
              state.cart.items.reduce((sum, i) => sum + i.qty, 0);
            export default cartSlice.reducer;

            // app/store.js
            import { configureStore } from '@reduxjs/toolkit';
            import cartReducer from '../features/cart/cartSlice';

            export const store = configureStore({ reducer: { cart: cartReducer } });

            // components/CartBadge.jsx (the app is wrapped in <Provider store={store}>)
            import { useDispatch, useSelector } from 'react-redux';

            export function CartBadge({ product }) {
              const count = useSelector(selectCartCount);
              const dispatch = useDispatch();
              return (
                <button onClick={() => dispatch(itemAdded(product))}>
                  Add to cart ({count})
                </button>
              );
            }
        """,
        lang="jsx",
        follow=[
            ("How does RTK Query decide when to refetch data after a mutation?", "Mutation-এর পর RTK Query কীভাবে ঠিক করে কখন আবার data fetch করবে?"),
            ("Why must Redux state be serialisable?", "Redux state কেন serialisable হতে হবে?"),
        ],
        related=["react-008"],
        refs=[R_RTK, R_USESES],
    ),
    # ------------------------------------------------------------------ react-018
    Q(
        id="react-018", sub="Effects Debugging", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["useeffect", "infinite-loop", "dependencies", "debugging"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""
            After this component was added, the API receives hundreds of requests per second and the browser tab becomes sluggish. Find the bug, explain the root cause and fix it.
        """,
        q_bn=r"""
            এই component যোগ করার পর API প্রতি সেকেন্ডে শত শত request পাচ্ছে, আর browser tab ধীর হয়ে যাচ্ছে। Bug-টা খুঁজে বের করো, root cause ব্যাখ্যা করো আর ঠিক করো।
        """,
        a_en=r"""
            It's an **infinite effect loop**. `filters` is a new object on every render, and the effect depends on it. React compares dependencies with `Object.is`, so the dependency "changes" every time:

            render → new `filters` → effect runs → fetch → `setProducts(newArray)` → re-render → new `filters` → effect runs again… forever.

            The fix is to depend on **primitive values**. I build the query inside the effect and depend only on `category`. I also add an `AbortController` cleanup so a slow old response can't overwrite a newer one when the category changes.
        """,
        a_bn=r"""
            এটা একটা **infinite effect loop**। প্রতিটা render-এ `filters` একটা নতুন object, আর effect এর উপর নির্ভর করে। React dependency তুলনা করে `Object.is` দিয়ে, তাই প্রতিবারই dependency "বদলে যায়":

            render → নতুন `filters` → effect চলে → fetch → `setProducts(newArray)` → re-render → নতুন `filters` → effect আবার চলে… চলতেই থাকে।

            সমাধান হলো **primitive value**-এর উপর নির্ভর করা। আমি effect-এর ভেতরেই query তৈরি করি আর শুধু `category`-র উপর নির্ভর করি। সাথে একটা `AbortController` cleanup যোগ করি, যাতে category বদলালে ধীর পুরনো response নতুনটাকে overwrite করতে না পারে।
        """,
        quick_en=r"""It's an infinite effect loop: `filters` is a new object every render, so the dependency always changes, the fetch sets state, and that renders again. Build the query inside the effect, depend on the primitive `category`, and abort the old request in the cleanup.""",
        quick_bn=r"""এটা একটা infinite effect loop: প্রতি render-এ `filters` নতুন object, তাই dependency সবসময় বদলায়, fetch state set করে, আর আবার render হয়। Query-টা effect-এর ভেতরে বানাও, শুধু primitive `category`-র উপর depend করো, আর cleanup-এ পুরনো request abort করো।""",
        ex_en=r"""
            Other common infinite-loop patterns:
            - An effect with **no dependency array** that sets state.
            - `useEffect(() => setCount(count + 1), [count])` — the effect changes its own dependency.
            - A **function** declared in the component used as a dependency (new every render). Move it inside the effect, or extract non-reactive logic with `useEffectEvent`.
            - Calling `setState` directly during render.

            **How I'd debug it:** the Network tab shows the request storm; a `console.log` in the effect confirms it re-runs every render; React DevTools "Highlight updates" shows the component flashing. The `exhaustive-deps` lint rule would also warn that `filters` changes on every render.

            Note: React Compiler would memoize `filters` here and hide the loop, but memoization is a performance optimisation, not a correctness guarantee — depend on primitives anyway.
        """,
        ex_bn=r"""
            আরও কিছু সাধারণ infinite-loop pattern:
            - **Dependency array ছাড়া** এমন effect, যেটা state set করে।
            - `useEffect(() => setCount(count + 1), [count])` — effect নিজেই নিজের dependency বদলায়।
            - Component-এর ভেতরে declare করা কোনো **function** dependency হিসেবে (প্রতিটা render-এ নতুন)। এটাকে effect-এর ভেতরে নিয়ে যাও, অথবা non-reactive logic `useEffectEvent` দিয়ে আলাদা করো।
            - Render-এর সময় সরাসরি `setState` call করা।

            **আমি কীভাবে debug করতাম:** Network tab-এ request-এর ঝড় দেখা যায়; effect-এ একটা `console.log` দিলে নিশ্চিত হওয়া যায় যে প্রতিটা render-এ এটা আবার চলছে; React DevTools-এর "Highlight updates" দিয়ে component-কে বারবার জ্বলতে দেখা যায়। `exhaustive-deps` lint rule-ও warning দিত যে `filters` প্রতিটা render-এ বদলায়।

            নোট: React Compiler এখানে `filters` memoize করে loop-টা লুকিয়ে ফেলত, কিন্তু memoization হলো performance optimisation, correctness-এর নিশ্চয়তা না — তবুও primitive-এর উপর নির্ভর করো।
        """,
        tip_en=r"""Draw the loop as a cycle (render → effect → setState → render) and name `Object.is` as the reason the dependency changes. Then mention how you'd spot it in DevTools — that's the production-debugging angle interviewers like.""",
        tip_bn=r"""Loop-টা একটা চক্র হিসেবে আঁকো (render → effect → setState → render) আর বলো যে `Object.is`-এর কারণে dependency বদলায়। তারপর DevTools-এ কীভাবে ধরবে সেটা বলো — interviewer production-debugging-এর এই দিকটা পছন্দ করে।""",
        mist_en=r""""Fixing" it with an empty dependency array (now the list never updates when `category` changes) or with `JSON.stringify(filters)` hacks instead of depending on the real primitives.""",
        mist_bn=r"""খালি dependency array দিয়ে "ঠিক" করা (তখন `category` বদলালেও list আর update হয় না), অথবা আসল primitive-এর উপর নির্ভর না করে `JSON.stringify(filters)`-এর মতো hack ব্যবহার করা।""",
        code=r"""
            import { useEffect, useState } from 'react';

            export default function ProductList({ category }) {
              const [products, setProducts] = useState([]);
              const filters = { category, inStock: 'true' };

              useEffect(() => {
                fetch(`/api/products?${new URLSearchParams(filters)}`)
                  .then((res) => res.json())
                  .then((data) => setProducts(data));
              }, [filters]);

              return products.map((p) => <ProductCard key={p.id} product={p} />);
            }
        """,
        lang="jsx",
        extra=[dict(lang="jsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            import { useEffect, useState } from 'react';

            export default function ProductList({ category }) {
              const [products, setProducts] = useState([]);

              useEffect(() => {
                const controller = new AbortController();
                const params = new URLSearchParams({ category, inStock: 'true' });

                fetch(`/api/products?${params}`, { signal: controller.signal })
                  .then((res) => res.json())
                  .then(setProducts)
                  .catch((err) => {
                    if (err.name !== 'AbortError') console.error(err);
                  });

                return () => controller.abort();
              }, [category]); // primitive dependency

              return products.map((p) => <ProductCard key={p.id} product={p} />);
            }
        """)],
        follow=[
            ("If the effect needs a callback prop like `onLoaded`, how do you avoid re-running it when the parent passes a new function?", "Effect-এর যদি `onLoaded`-এর মতো callback prop লাগে, parent নতুন function পাঠালে effect আবার চলা কীভাবে ঠেকাবে?"),
            ("Why is an empty dependency array not a real fix here?", "এখানে খালি dependency array কেন আসল সমাধান না?"),
        ],
        related=["react-007", "react-015"],
        refs=[R_USEEFFECT, R_DEPS],
    ),
    # ------------------------------------------------------------------ react-019
    Q(
        id="react-019", sub="Error Boundaries", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["error-boundary", "error-handling", "resilience"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""Which of these errors is caught by a React error boundary placed above the component?""",
        q_bn=r"""Component-এর উপরে রাখা একটা React error boundary নিচের কোন error-টা ধরবে?""",
        options=[
            ("An error thrown inside a button's `onClick` handler", "Button-এর `onClick` handler-এর ভেতরে throw হওয়া error"),
            ("An error thrown while a child component is rendering", "কোনো child component render হওয়ার সময় throw হওয়া error"),
            ("An error thrown inside a `setTimeout` callback", "`setTimeout` callback-এর ভেতরে throw হওয়া error"),
            ("An error thrown inside the error boundary's own fallback rendering", "Error boundary-র নিজের fallback render করার সময় throw হওয়া error"),
        ],
        correct=1,
        a_en=r"""Error boundaries catch errors thrown **while rendering** the tree below them (and in their lifecycle/effects), then show a fallback UI instead of unmounting the whole app.""",
        a_bn=r"""Error boundary তার নিচের tree **render হওয়ার সময়** (আর তাদের lifecycle/effect-এ) throw হওয়া error ধরে, তারপর পুরো app unmount না করে একটা fallback UI দেখায়।""",
        quick_en=r"""An error thrown while a child component is rendering. Error boundaries catch errors during rendering (and in lifecycles/effects) of the tree below them, not in event handlers, `setTimeout` callbacks or their own fallback.""",
        quick_bn=r"""Child component render হওয়ার সময় throw হওয়া error। Error boundary নিচের tree-র rendering (আর lifecycle/effect)-এর error ধরে; event handler, `setTimeout` callback বা নিজের fallback-এর error ধরে না।""",
        ex_en=r"""
            The tempting wrong answer is the `onClick` error. Event handlers run outside rendering, so React doesn't need a fallback to keep the UI consistent — you handle those with `try/catch` and state. The same applies to async code such as `setTimeout` or promise callbacks. An error inside the boundary itself (including its fallback) propagates to the next boundary above.

            Implementation: error boundaries are still **class components** (`static getDerivedStateFromError` + `componentDidCatch`), or you use the `react-error-boundary` package. Useful nuances:
            - Errors thrown inside a transition/Action (e.g. `startTransition(async () => { … })`) are shown by the nearest error boundary.
            - In React 19, `createRoot` options `onCaughtError` / `onUncaughtError` let you report errors to monitoring in one place.
            - Next.js `error.js` files are error boundaries per route segment.
        """,
        ex_bn=r"""
            লোভনীয় ভুল উত্তর হলো `onClick`-এর error। Event handler rendering-এর বাইরে চলে, তাই UI ঠিক রাখতে React-এর কোনো fallback লাগে না — এগুলো `try/catch` আর state দিয়ে সামলাতে হয়। `setTimeout` বা promise callback-এর মতো async code-এর ক্ষেত্রেও একই কথা। Boundary-র নিজের ভেতরে (fallback-সহ) error হলে সেটা উপরের পরের boundary-তে চলে যায়।

            Implementation: error boundary এখনো **class component** (`static getDerivedStateFromError` + `componentDidCatch`), অথবা `react-error-boundary` package ব্যবহার করো। কাজের কিছু সূক্ষ্মতা:
            - Transition/Action-এর ভেতরে throw হওয়া error (যেমন `startTransition(async () => { … })`) সবচেয়ে কাছের error boundary দেখায়।
            - React 19-এ `createRoot`-এর `onCaughtError` / `onUncaughtError` option দিয়ে এক জায়গা থেকে monitoring-এ error report করা যায়।
            - Next.js-এর `error.js` file হলো প্রতিটা route segment-এর error boundary।
        """,
        tip_en=r"""List what boundaries catch and what they don't (events, async, the boundary itself), then mention how you'd report errors in production. That's a complete, practical answer.""",
        tip_bn=r"""Boundary কী ধরে আর কী ধরে না (event, async, boundary নিজে) — তালিকা করে বলো, তারপর production-এ error কীভাবে report করবে সেটা উল্লেখ করো। এটাই একটা পূর্ণাঙ্গ, ব্যবহারিক উত্তর।""",
        refs=[R_BOUNDARY, R_REB],
    ),
    # ------------------------------------------------------------------ react-025
    Q(
        id="react-025", sub="Context Performance", diff="hard", type="debugging",
        prio="high", market="both", mins=8,
        tags=["context", "re-renders", "performance", "state-colocation"],
        ver="React 19.3", vs=True, status="stable",
        q_en=r"""
            Typing in the search box makes the whole app stutter. The React Profiler shows `Header`, `Sidebar` and 200 `ProductCard`s (which read `theme` via `useApp()`) re-rendering on **every keystroke**, even though none of them use `searchText`. Explain the root cause and refactor it.
        """,
        q_bn=r"""
            Search box-এ টাইপ করলে পুরো app আটকে আটকে চলে। React Profiler দেখাচ্ছে `Header`, `Sidebar` আর ২০০টা `ProductCard` (যারা `useApp()` দিয়ে `theme` পড়ে) **প্রতিটা keystroke-এ** re-render হচ্ছে, যদিও এদের কেউই `searchText` ব্যবহার করে না। Root cause ব্যাখ্যা করো আর refactor করো।
        """,
        a_en=r"""
            There is one context carrying everything, and its `value` is a **new object literal** on every render of `AppProvider`. Each keystroke updates `searchText` → `AppProvider` re-renders → new value object → React re-renders **every component that reads `AppContext`**, no matter which field it uses. Context has no selector mechanism, and `memo` doesn't help because context updates bypass it.

            Refactor:
            1. **Colocate fast-changing state.** `searchText` belongs in `SearchBox` (or the URL), not in global context.
            2. **Split contexts** by concern and update frequency: `UserContext`, `ThemeContext`. Setters from `useState` are stable, so they can live in a separate "actions" context if needed.
            3. **Memoize each value** (`useMemo`, or let React Compiler do it), so a provider re-render without a real change doesn't notify consumers.
            4. If many components need *slices* of frequently changing global state, use an external store with selectors (Redux Toolkit, Zustand — built on `useSyncExternalStore`).

            After that, a keystroke re-renders only the search UI, and `ProductCard`s re-render only when the theme actually changes.
        """,
        a_bn=r"""
            একটাই context সবকিছু বহন করছে, আর `AppProvider`-এর প্রতিটা render-এ এর `value` একটা **নতুন object literal**। প্রতিটা keystroke-এ `searchText` update হয় → `AppProvider` re-render হয় → নতুন value object → React **`AppContext` পড়া প্রতিটা component** re-render করে, সে যে field-ই ব্যবহার করুক না কেন। Context-এ কোনো selector ব্যবস্থা নেই, আর `memo`-তেও লাভ নেই, কারণ context update `memo`-কে পাশ কাটিয়ে যায়।

            Refactor:
            1. **দ্রুত বদলানো state কাছাকাছি রাখো।** `searchText`-এর জায়গা `SearchBox`-এ (বা URL-এ), global context-এ না।
            2. **Context ভাগ করো** কাজ আর update-এর হার অনুযায়ী: `UserContext`, `ThemeContext`। `useState`-এর setter stable, তাই দরকার হলে এগুলো আলাদা একটা "actions" context-এ রাখা যায়।
            3. **প্রতিটা value memoize করো** (`useMemo`, বা React Compiler-কে করতে দাও), যাতে আসল পরিবর্তন ছাড়া provider re-render হলে consumer-রা খবর না পায়।
            4. অনেক component-এর যদি ঘন ঘন বদলানো global state-এর *অংশবিশেষ* লাগে, selector-সহ external store ব্যবহার করো (Redux Toolkit, Zustand — `useSyncExternalStore`-এর উপর তৈরি)।

            এরপর একটা keystroke-এ শুধু search UI re-render হয়, আর theme আসলেই বদলালে তবেই `ProductCard` re-render হয়।
        """,
        quick_en=r"""One context holds everything and its value is a new object every render, so each keystroke re-renders every consumer. Move `searchText` into `SearchBox`, split contexts by concern, and memoize each value (or use a store with selectors).""",
        quick_bn=r"""একটা context-এ সবকিছু রাখা, আর প্রতি render-এ তার value নতুন object, তাই প্রতি keystroke-এ সব consumer re-render হয়। `searchText`-কে `SearchBox`-এ নিয়ে যাও, concern অনুযায়ী context ভাগ করো, আর প্রতিটা value memoize করো (বা selector-সহ store ব্যবহার করো)।""",
        ex_en=r"""
            **Why `children` aren't the problem:** `AppProvider` receives `children` as an element created by its parent, so a state change inside `AppProvider` doesn't re-create them. The re-renders come purely from *context consumers* — that's why splitting/memoizing the value fixes it.

            **How to confirm:** in the React DevTools Profiler enable "Record why each component rendered" — it reports "Context changed". React 19.2 Performance Tracks in the Chrome Performance panel show the same cascade on the Components track.

            **Trade-offs:** many tiny contexts add boilerplate and provider nesting; an external store adds a dependency but gives fine-grained subscriptions. For a theme/user/locale, split contexts are enough; for a big, fast-changing domain model, a store is better.
        """,
        ex_bn=r"""
            **`children` কেন সমস্যা না:** `AppProvider` তার parent-এর তৈরি element হিসেবে `children` পায়, তাই `AppProvider`-এর ভেতরে state বদলালে সেগুলো নতুন করে তৈরি হয় না। Re-render আসে পুরোপুরি *context consumer*-দের কাছ থেকে — এজন্যই value ভাগ/memoize করলে সমস্যা মিটে যায়।

            **কীভাবে নিশ্চিত হবে:** React DevTools Profiler-এ "Record why each component rendered" চালু করো — এটা "Context changed" দেখায়। React 19.2-এর Performance Tracks-এ Chrome Performance panel-এর Components track-এ একই cascade দেখা যায়।

            **Trade-off:** অনেকগুলো ছোট context boilerplate আর provider-এর nesting বাড়ায়; external store একটা dependency যোগ করে, কিন্তু সূক্ষ্ম subscription দেয়। Theme/user/locale-এর জন্য আলাদা context-ই যথেষ্ট; বড়, দ্রুত বদলানো domain model-এর জন্য store ভালো।
        """,
        tip_en=r"""Explain the mechanism precisely ("new value identity → all consumers re-render, memo can't stop it"), then give fixes in order of simplicity: colocate state, split, memoize, external store. Mention how you'd prove it with the Profiler.""",
        tip_bn=r"""Mechanism-টা নিখুঁতভাবে বলো ("value-র নতুন identity → সব consumer re-render, memo থামাতে পারে না"), তারপর সহজ থেকে কঠিন ক্রমে সমাধান দাও: state কাছাকাছি রাখা, ভাগ করা, memoize, external store। Profiler দিয়ে কীভাবে প্রমাণ করবে সেটাও বলো।""",
        mist_en=r"""Wrapping consumers in `memo` (doesn't stop context re-renders), or only adding `useMemo` while `searchText` stays in the same context (the value still changes on every keystroke).""",
        mist_bn=r"""Consumer-দের `memo`-তে wrap করা (context re-render থামায় না), অথবা `searchText` একই context-এ রেখে শুধু `useMemo` যোগ করা (তখনো প্রতিটা keystroke-এ value বদলায়)।""",
        code=r"""
            import { createContext, use, useState } from 'react';

            const AppContext = createContext(null);

            export function AppProvider({ children }) {
              const [user, setUser] = useState(null);
              const [theme, setTheme] = useState('light');
              const [searchText, setSearchText] = useState('');

              return (
                <AppContext value={{ user, setUser, theme, setTheme, searchText, setSearchText }}>
                  {children}
                </AppContext>
              );
            }

            export const useApp = () => use(AppContext);

            function ProductCard({ product }) {
              const { theme } = useApp();
              return <article className={`card card-${theme}`}>{product.name}</article>;
            }

            function SearchBox() {
              const { searchText, setSearchText } = useApp();
              return <input value={searchText} onChange={(e) => setSearchText(e.target.value)} />;
            }
        """,
        lang="jsx",
        extra=[dict(lang="jsx", label_en="Refactored version", label_bn="Refactor করা version", src=r"""
            import { createContext, use, useMemo, useState } from 'react';

            const UserContext = createContext(null);
            const ThemeContext = createContext(null);

            export function AppProvider({ children }) {
              const [user, setUser] = useState(null);
              const [theme, setTheme] = useState('light');

              const userValue = useMemo(() => ({ user, setUser }), [user]);
              const themeValue = useMemo(() => ({ theme, setTheme }), [theme]);

              return (
                <UserContext value={userValue}>
                  <ThemeContext value={themeValue}>{children}</ThemeContext>
                </UserContext>
              );
            }

            export const useTheme = () => use(ThemeContext);
            export const useUser = () => use(UserContext);

            function ProductCard({ product }) {
              const { theme } = useTheme(); // re-renders only when the theme changes
              return <article className={`card card-${theme}`}>{product.name}</article>;
            }

            // Fast-changing state stays local (or goes into the URL)
            function SearchBox({ onSearch }) {
              const [text, setText] = useState('');
              return (
                <input
                  value={text}
                  onChange={(e) => {
                    setText(e.target.value);
                    onSearch(e.target.value);
                  }}
                />
              );
            }
        """)],
        follow=[
            ("How does `useSyncExternalStore` let a store re-render only the components whose selected value changed?", "`useSyncExternalStore` কীভাবে একটা store-কে শুধু সেই component-গুলো re-render করতে দেয়, যাদের selected value বদলেছে?"),
            ("Would React Compiler alone fix this problem? Why or why not?", "শুধু React Compiler কি এই সমস্যা ঠিক করে দিত? কেন বা কেন না?"),
        ],
        related=["react-008", "react-014"],
        refs=[R_CTX, R_USESES, R_USEMEMO],
    ),
    # ------------------------------------------------------------------ react-026
    Q(
        id="react-026", sub="Production Debugging", diff="hard", type="scenario",
        prio="high", market="international", mins=10,
        tags=["profiler", "performance-tracks", "inp", "devtools", "production"],
        ver="React 19.3 (Performance Tracks since 19.2)", vs=True, status="stable",
        q_en=r"""
            After a release, users report that the analytics dashboard "freezes for about a second" when they change a filter. It feels fine on developer laptops. How do you investigate and fix this?
        """,
        q_bn=r"""
            একটা release-এর পর user-রা জানাচ্ছে, analytics dashboard-এ filter বদলালে "প্রায় এক সেকেন্ড আটকে যায়"। Developer-দের laptop-এ ঠিকঠাক মনে হয়। তুমি কীভাবে এটা investigate আর ঠিক করবে?
        """,
        a_en=r"""
            I'd treat it as a measurable **interaction latency (INP)** problem, not a guess.

            1. **Confirm and scope.** Check real-user monitoring for INP on that page, by device class and browser. A "fine on my laptop" bug usually means mid-range Android phones — so I reproduce with 4–6x CPU throttling in Chrome DevTools.
            2. **Profile the interaction.** Record in the Chrome **Performance** panel. With a development or profiling build, React's **Performance Tracks** (React 19.2+) show the Scheduler track (blocking vs transition work, render vs commit vs effects) and the Components track (which components rendered and for how long) right next to long tasks.
            3. **Find why things render.** In the React DevTools Profiler, use the ranked chart and "Record why each component rendered" to spot unnecessary re-renders (context changes, new props every render).
            4. **Typical culprits:** a context value that re-renders the whole dashboard, sorting/aggregating thousands of rows during render, an unvirtualised table, a chart library re-initialising on every render, or an effect chain (effect sets state → another render).
            5. **Fix by cause:** move state down or split context, memoize (or enable React Compiler), mark the filter update as a transition so the click stays responsive, virtualise the table, move heavy aggregation to a Web Worker or the server.
            6. **Verify** with the same throttled profile, then watch INP in RUM after the next release.
        """,
        a_bn=r"""
            আমি এটাকে অনুমান না করে একটা মাপা যায় এমন **interaction latency (INP)** সমস্যা হিসেবে দেখব।

            1. **নিশ্চিত হওয়া আর পরিধি ঠিক করা।** ওই page-এর INP real-user monitoring-এ device class আর browser অনুযায়ী দেখি। "আমার laptop-এ ঠিক আছে" ধরনের bug মানে সাধারণত মাঝারি মানের Android phone — তাই Chrome DevTools-এ 4–6x CPU throttling দিয়ে reproduce করি।
            2. **Interaction-টা profile করা।** Chrome-এর **Performance** panel-এ record করি। Development বা profiling build-এ React-এর **Performance Tracks** (React 19.2+) long task-এর ঠিক পাশেই Scheduler track (blocking বনাম transition কাজ, render বনাম commit বনাম effect) আর Components track (কোন component render হয়েছে আর কতক্ষণ) দেখায়।
            3. **কেন render হচ্ছে খোঁজা।** React DevTools Profiler-এ ranked chart আর "Record why each component rendered" দিয়ে অপ্রয়োজনীয় re-render ধরি (context পরিবর্তন, প্রতিটা render-এ নতুন props)।
            4. **সাধারণ অপরাধী:** এমন context value যেটা পুরো dashboard re-render করায়, render-এর সময় হাজার হাজার row sort/aggregate করা, virtualise না করা table, প্রতিটা render-এ নতুন করে initialise হওয়া chart library, অথবা effect-এর শিকল (effect state set করে → আরেকটা render)।
            5. **কারণ অনুযায়ী সমাধান:** state নিচে নামানো বা context ভাগ করা, memoize করা (বা React Compiler চালু করা), filter update-কে transition হিসেবে চিহ্নিত করা যাতে click responsive থাকে, table virtualise করা, ভারী aggregation Web Worker বা server-এ সরানো।
            6. **যাচাই** একই throttled profile দিয়ে, তারপর পরের release-এর পর RUM-এ INP পর্যবেক্ষণ।
        """,
        quick_en=r"""Treat it as an INP problem: reproduce with CPU throttling, profile the interaction in the Performance panel and React Profiler, then fix the real cause. Typical fixes are splitting context, memoizing, a transition for the filter, virtualising the table or moving heavy work off the main thread.""",
        quick_bn=r"""এটাকে INP সমস্যা হিসেবে দেখো: CPU throttling দিয়ে reproduce করো, Performance panel আর React Profiler-এ interaction profile করো, তারপর আসল কারণ ঠিক করো। সাধারণ সমাধান: context ভাগ করা, memoize করা, filter-কে transition-এ রাখা, table virtualise করা, বা ভারী কাজ main thread থেকে সরানো।""",
        ex_en=r"""
            **Builds matter:** React's profiling instrumentation is disabled in normal production builds. Performance Tracks are available in development and profiling builds; to profile something close to production, alias `react-dom/client` to `react-dom/profiling` in a dedicated build. In a profiling build only the Scheduler tracks are on by default, and the Components track covers subtrees wrapped in `<Profiler>` (or all components if React DevTools is installed).

            **Production telemetry:** the `<Profiler onRender>` callback (in a profiling build) or plain `performance.mark`/`measure` around the interaction can send slow-render data to analytics.

            **Don't stop at React:** the Performance panel may reveal that the time is in layout/style recalculation (huge DOM, forced reflows) or a third-party script, not in React rendering.
        """,
        ex_bn=r"""
            **Build-এর গুরুত্ব:** সাধারণ production build-এ React-এর profiling instrumentation বন্ধ থাকে। Performance Tracks development আর profiling build-এ পাওয়া যায়; production-এর কাছাকাছি কিছু profile করতে আলাদা একটা build-এ `react-dom/client`-কে `react-dom/profiling`-এ alias করো। Profiling build-এ default-ভাবে শুধু Scheduler track চালু থাকে, আর Components track শুধু `<Profiler>`-এ wrap করা subtree দেখায় (React DevTools install করা থাকলে সব component)।

            **Production telemetry:** `<Profiler onRender>` callback (profiling build-এ) অথবা interaction-এর চারপাশে সাধারণ `performance.mark`/`measure` দিয়ে ধীর render-এর data analytics-এ পাঠানো যায়।

            **শুধু React-এ থেমো না:** Performance panel হয়তো দেখাবে সময়টা যাচ্ছে layout/style recalculation-এ (বিশাল DOM, forced reflow) বা কোনো third-party script-এ, React rendering-এ না।
        """,
        tip_en=r"""Use a clear structure: reproduce → measure → identify cause → fix → verify in production. Naming INP, CPU throttling, the Profiler's "why did this render" and React Performance Tracks shows real production experience.""",
        tip_bn=r"""একটা স্পষ্ট কাঠামো ব্যবহার করো: reproduce → measure → কারণ খোঁজা → fix → production-এ যাচাই। INP, CPU throttling, Profiler-এর "why did this render" আর React Performance Tracks-এর নাম বললে আসল production অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Jumping straight to "add `useMemo` everywhere" without profiling, profiling only in development on a fast laptop, or assuming the Profiler works in a normal production build.""",
        mist_bn=r"""Profile না করেই সরাসরি "সব জায়গায় `useMemo` দাও" বলা, শুধু দ্রুত laptop-এ development mode-এ profile করা, অথবা ভাবা যে সাধারণ production build-এ Profiler কাজ করে।""",
        code=r"""
            import { Profiler } from 'react';

            // Works in development and in a profiling build (react-dom/profiling)
            function onRender(id, phase, actualDuration, baseDuration) {
              if (actualDuration > 50) {
                sendToAnalytics({ id, phase, actualDuration, baseDuration });
              }
            }

            export default function DashboardPage() {
              return (
                <Profiler id="Dashboard" onRender={onRender}>
                  <Filters />
                  <ChartsGrid />
                  <ReportTable />
                </Profiler>
              );
            }
        """,
        lang="jsx",
        follow=[
            ("What is INP and why does it matter more than load time for this bug?", "INP কী, আর এই bug-এর ক্ষেত্রে load time-এর চেয়ে এটা কেন বেশি গুরুত্বপূর্ণ?"),
            ("How would you move heavy aggregation off the main thread?", "ভারী aggregation main thread থেকে কীভাবে সরাবে?"),
        ],
        related=["react-024", "react-025"],
        refs=[R_PERF_TRACKS, R_PROFILER, R_INP],
    ),
]

if __name__ == "__main__":
    save("react", "b3", QUESTIONS)
