# React — quick-recall questions (react-q01..q10)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

QUESTIONS = [
    # ------------------------------------------------------------------ react-q01
    Q(
        id="react-q01", sub="Rendering and Reconciliation", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["virtual-dom", "reconciliation", "rendering"],
        ver="Version-independent concept (React 19.3)", vs=False, status="stable",
        q_en=r"""What is the virtual DOM, and how does React use it?""",
        q_bn=r"""Virtual DOM কী, আর React এটা কীভাবে ব্যবহার করে?""",
        a_en=r"""The "virtual DOM" is the tree of plain JavaScript objects (React elements) that your components return to describe the UI. On each render React compares the new tree with the previous one (reconciliation) and changes only the real DOM nodes that actually differ.""",
        a_bn=r""""Virtual DOM" হলো component-গুলোর return করা সাধারণ JavaScript object (React element)-এর tree, যেটা UI কেমন হবে তার বর্ণনা দেয়। প্রতি render-এ React নতুন tree-কে আগেরটার সাথে তুলনা করে (reconciliation), আর আসল DOM-এর শুধু যেগুলো সত্যিই বদলেছে সেগুলোই update করে।""",
        ex_en=r"""React matches elements by type and position (plus `key` in lists). The follow-up trap: the virtual DOM isn't "faster than the DOM" by magic; it just lets React batch and minimise real DOM work.""",
        ex_bn=r"""React element মেলায় type আর position দেখে (list-এ `key` দিয়েও)। Follow-up-এর ফাঁদ: virtual DOM জাদুর মতো "DOM-এর চেয়ে দ্রুত" না; এটা শুধু React-কে আসল DOM-এর কাজ একসাথে করতে আর কমিয়ে আনতে সাহায্য করে।""",
        tip_en=r"""Say "describe UI as objects, diff, then patch only the changes", and mention that keys guide the diff in lists.""",
        tip_bn=r"""বলো "UI-কে object হিসেবে বর্ণনা, তারপর diff, তারপর শুধু পরিবর্তনটুকু patch", আর উল্লেখ করো যে list-এ key এই diff-কে পথ দেখায়।""",
        follow=[("Why does changing a component's type reset its state?", "Component-এর type বদলালে state reset হয় কেন?")],
        related=["react-023", "react-001", "react-004"],
        refs=[("react.dev — Render and Commit", "https://react.dev/learn/render-and-commit")],
    ),
    # ------------------------------------------------------------------ react-q02
    Q(
        id="react-q02", sub="useReducer", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["usereducer", "state", "hooks", "reducer"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What is `useReducer`, and when would you use it instead of `useState`?""",
        q_bn=r"""`useReducer` কী, আর কখন `useState`-এর বদলে এটা ব্যবহার করবে?""",
        a_en=r"""`useReducer(reducer, initialState)` returns `[state, dispatch]`; you `dispatch` an action object and a pure `reducer(state, action)` returns the next state. I use it when state has several related fields or many update types, because all the update logic lives in one testable function.""",
        a_bn=r"""`useReducer(reducer, initialState)` দেয় `[state, dispatch]`; তুমি একটা action object `dispatch` করো, আর একটা pure `reducer(state, action)` পরের state return করে। State-এ কয়েকটা সম্পর্কিত field বা অনেক ধরনের update থাকলে আমি এটা ব্যবহার করি, কারণ সব update logic এক জায়গায়, একটা test করা যায় এমন function-এ থাকে।""",
        code=r"""
            function reducer(state, action) {
              if (action.type === 'inc') return { count: state.count + 1 };
              if (action.type === 'reset') return { count: 0 };
              return state;
            }
            const s1 = reducer({ count: 0 }, { type: 'inc' });
            console.log(reducer(s1, { type: 'inc' })); // { count: 2 }
            // In a component: const [state, dispatch] = useReducer(reducer, { count: 0 });
        """, lang="javascript",
        ex_en=r"""The reducer must be pure and return a new object instead of mutating `state`, otherwise React may skip the re-render. `dispatch` is stable, so it's safe to pass down or use in effects.""",
        ex_bn=r"""Reducer-কে pure হতে হবে, আর `state` mutate না করে নতুন object return করতে হবে, নইলে React re-render বাদ দিতে পারে। `dispatch` stable, তাই নিচে পাঠানো বা effect-এ ব্যবহার করা নিরাপদ।""",
        tip_en=r"""Contrast it with `useState` in one line: "`useState` for simple values, `useReducer` when updates follow rules".""",
        tip_bn=r"""এক লাইনে `useState`-এর সাথে তুলনা করো: "সহজ value-র জন্য `useState`, update-এ নিয়ম থাকলে `useReducer`"।""",
        follow=[("How would you combine `useReducer` with Context?", "`useReducer`-কে Context-এর সাথে কীভাবে মিলিয়ে ব্যবহার করবে?")],
        related=["react-017", "react-003"],
        refs=[("react.dev — useReducer", "https://react.dev/reference/react/useReducer")],
    ),
    # ------------------------------------------------------------------ react-q03
    Q(
        id="react-q03", sub="Context API", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["prop-drilling", "context", "composition"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What is prop drilling, and when should you use Context instead?""",
        q_bn=r"""Prop drilling কী, আর কখন এর বদলে Context ব্যবহার করা উচিত?""",
        a_en=r"""Prop drilling is passing a prop through several components that don't use it, only so a deep child can get it. Use Context when many components at different depths need the same, rarely changing value (theme, user, locale); for one or two levels, plain props or passing `children` is simpler.""",
        a_bn=r"""Prop drilling মানে এমন কয়েকটা component-এর ভেতর দিয়ে prop পাঠানো যারা নিজেরা সেটা ব্যবহার করে না, শুধু একটা গভীর child-এ পৌঁছানোর জন্য। অনেক স্তরের অনেক component-এর একই, কম বদলায় এমন value (theme, user, locale) লাগলে Context ব্যবহার করো; এক-দুই level-এর জন্য সাধারণ props বা `children` পাঠানোই সহজ।""",
        ex_en=r"""Context isn't free: every consumer re-renders when the provided value changes, so fast-changing state in one big context slows the app down.""",
        ex_bn=r"""Context-এর একটা খরচ আছে: provide করা value বদলালে সব consumer re-render হয়, তাই একটা বড় context-এ ঘনঘন বদলানো state রাখলে app ধীর হয়ে যায়।""",
        tip_en=r"""Mention that props stay the default and composition (`children`) often removes drilling without Context.""",
        tip_bn=r"""বলো যে props-ই default, আর composition (`children`) দিয়ে অনেক সময় Context ছাড়াই drilling দূর করা যায়।""",
        follow=[("Why can a Context make many components re-render?", "Context কেন অনেক component-কে re-render করাতে পারে?")],
        related=["react-008", "react-025"],
        refs=[("react.dev — Passing Data Deeply with Context", "https://react.dev/learn/passing-data-deeply-with-context")],
    ),
    # ------------------------------------------------------------------ react-q04
    Q(
        id="react-q04", sub="Custom Hooks", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["hoc", "custom-hooks", "code-reuse"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What is a Higher-Order Component (HOC), and why do custom hooks usually replace it today?""",
        q_bn=r"""Higher-Order Component (HOC) কী, আর আজকাল কেন সাধারণত custom hook এর জায়গা নিয়েছে?""",
        a_en=r"""A HOC is a function that takes a component and returns a new component with extra behaviour, like `withAuth(Dashboard)`. Custom hooks (`useAuth()`) share the same logic without extra wrapper components, prop-name clashes or hidden props, so they are the default now; HOCs mostly remain in older code and some libraries.""",
        a_bn=r"""HOC হলো এমন একটা function যেটা একটা component নিয়ে বাড়তি আচরণসহ নতুন component return করে, যেমন `withAuth(Dashboard)`। Custom hook (`useAuth()`) একই logic share করে বাড়তি wrapper component, prop-এর নামের সংঘর্ষ বা লুকানো prop ছাড়াই, তাই এখন এটাই default; HOC মূলত পুরনো code আর কিছু library-তে থেকে গেছে।""",
        code=r"""
            // HOC: wraps the component
            const withUser = (Comp) => (props) => <Comp {...props} user={useUser()} />;
            const ProfileWithUser = withUser(Profile);

            // Custom hook: call it directly
            function Profile() {
              const user = useUser();
              return <h1>{user.name}</h1>;
            }
        """, lang="jsx",
        ex_en=r"""Stacking several HOCs creates "wrapper hell" in DevTools and makes it unclear which HOC injected which prop. Hooks make the data source explicit at the call site.""",
        ex_bn=r"""কয়েকটা HOC একটার উপর আরেকটা বসালে DevTools-এ "wrapper hell" তৈরি হয়, আর কোন HOC কোন prop দিল বোঝা যায় না। Hook ব্যবহার করলে data কোথা থেকে আসছে সেটা call করার জায়গাতেই পরিষ্কার থাকে।""",
        tip_en=r"""Define a HOC in one sentence, then say why you'd write a hook instead, without calling HOCs "deprecated" (they still work).""",
        tip_bn=r"""এক বাক্যে HOC-এর সংজ্ঞা দাও, তারপর বলো কেন তুমি এর বদলে hook লিখবে; HOC-কে "deprecated" বোলো না (এগুলো এখনো কাজ করে)।""",
        follow=[("Is there any case where a HOC is still useful?", "HOC এখনো কাজে লাগে এমন কোনো case আছে কি?")],
        related=["react-015"],
        refs=[("react.dev — Reusing Logic with Custom Hooks", "https://react.dev/learn/reusing-logic-with-custom-hooks")],
    ),
    # ------------------------------------------------------------------ react-q05
    Q(
        id="react-q05", sub="Controlled and Uncontrolled Components", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["controlled", "uncontrolled", "forms", "warning"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""Why does React warn "A component is changing an uncontrolled input to be controlled"?""",
        q_bn=r"""React কেন warning দেয় "A component is changing an uncontrolled input to be controlled"?""",
        a_en=r"""Because the input's `value` started as `undefined` or `null` (so React treated it as uncontrolled) and later became a string (controlled). Pick one mode for the input's whole life: initialise state with `''` for a controlled input, or use `defaultValue` for an uncontrolled one.""",
        a_bn=r"""কারণ input-এর `value` শুরুতে `undefined` বা `null` ছিল (তাই React সেটাকে uncontrolled ধরেছে), পরে string হয়ে গেছে (controlled)। Input-এর পুরো জীবনের জন্য একটা mode বেছে নাও: controlled হলে state `''` দিয়ে শুরু করো, uncontrolled হলে `defaultValue` ব্যবহার করো।""",
        code=r"""
            // ✗ const [name, setName] = useState();  // starts as undefined
            const [name, setName] = useState('');    // ✓ always a string
            <input value={name} onChange={(e) => setName(e.target.value)} />
        """, lang="jsx",
        ex_en=r"""A common source is `value={user.name}` while `user` is still loading. Use `value={user?.name ?? ''}`.""",
        ex_bn=r"""এটা প্রায়ই হয় `value={user.name}` থেকে, যখন `user` এখনো load হচ্ছে। `value={user?.name ?? ''}` ব্যবহার করো।""",
        tip_en=r"""Explain the cause in one breath ("`undefined` means uncontrolled") and give the `''` fix.""",
        tip_bn=r"""এক নিঃশ্বাসে কারণটা বলো ("`undefined` মানে uncontrolled"), আর `''` দিয়ে সমাধান দেখাও।""",
        follow=[("Is a file input controlled or uncontrolled?", "File input controlled না uncontrolled?")],
        related=["react-005"],
        refs=[("react.dev — <input>", "https://react.dev/reference/react-dom/components/input")],
    ),
    # ------------------------------------------------------------------ react-q06
    Q(
        id="react-q06", sub="Components and JSX", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["fragment", "jsx", "components"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What is a Fragment (`<>...</>`), and why do you need it?""",
        q_bn=r"""Fragment (`<>...</>`) কী, আর এটা কেন লাগে?""",
        a_en=r"""A component must return a single root, and a Fragment groups several elements without adding an extra DOM node. Use the long form `<Fragment key={id}>` when you need a `key`, for example when mapping a list to pairs of elements.""",
        a_bn=r"""Component-কে একটাই root return করতে হয়, আর Fragment বাড়তি কোনো DOM node যোগ না করেই কয়েকটা element-কে একসাথে রাখে। `key` লাগলে লম্বা রূপ `<Fragment key={id}>` ব্যবহার করো, যেমন কোনো list-কে জোড়া জোড়া element-এ map করার সময়।""",
        code=r"""
            function Row() {
              return (
                <>
                  <td>Rahim</td>
                  <td>Dhaka</td>
                </>
              ); // a <div> here would break the table markup
            }
        """, lang="jsx",
        ex_en=r"""Extra wrapper `<div>`s can break table, list and flex/grid layouts; Fragments avoid that.""",
        ex_bn=r"""বাড়তি wrapper `<div>` table, list আর flex/grid layout ভেঙে দিতে পারে; Fragment সেটা এড়ায়।""",
        tip_en=r"""Show the table-row example: it proves why an extra `<div>` is a real problem.""",
        tip_bn=r"""Table row-এর example দেখাও: এতে বোঝা যায় বাড়তি `<div>` কেন সত্যিকারের সমস্যা।""",
        follow=[("When does the short `<>` syntax not work?", "ছোট `<>` syntax কখন কাজ করে না?")],
        related=["react-001"],
        refs=[("react.dev — <Fragment>", "https://react.dev/reference/react/Fragment")],
    ),
    # ------------------------------------------------------------------ react-q07
    Q(
        id="react-q07", sub="Component Lifecycle and Effects", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["uselayouteffect", "useeffect", "effects"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What is the difference between `useEffect` and `useLayoutEffect`?""",
        q_bn=r"""`useEffect` আর `useLayoutEffect`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`useEffect` usually runs after the browser has painted, so it doesn't block the screen. `useLayoutEffect` runs after React updates the DOM but before paint, so you can measure layout (like a tooltip's size) and adjust it without a visible flicker; use it only for that, because it blocks painting.""",
        a_bn=r"""`useEffect` সাধারণত browser paint করার পরে চলে, তাই screen আটকায় না। `useLayoutEffect` চলে React DOM update করার পরে কিন্তু paint-এর আগে, তাই layout মাপা (যেমন tooltip-এর size) আর চোখে পড়ার মতো flicker ছাড়া ঠিক করা যায়; শুধু এই কাজেই ব্যবহার করো, কারণ এটা paint আটকে রাখে।""",
        ex_en=r"""Default to `useEffect`. `useLayoutEffect` doesn't run during server rendering, so layout measurement belongs to the client.""",
        ex_bn=r"""Default হিসেবে `useEffect` নাও। Server rendering-এর সময় `useLayoutEffect` চলে না, তাই layout মাপার কাজটা client-এর।""",
        tip_en=r"""Say "before paint vs after paint" and give the tooltip-position example.""",
        tip_bn=r"""বলো "paint-এর আগে বনাম paint-এর পরে", আর tooltip-এর position-এর example দাও।""",
        follow=[("Why can `useLayoutEffect` hurt performance?", "`useLayoutEffect` কেন performance খারাপ করতে পারে?")],
        related=["react-007", "react-013"],
        refs=[("react.dev — useLayoutEffect", "https://react.dev/reference/react/useLayoutEffect")],
    ),
    # ------------------------------------------------------------------ react-q08
    Q(
        id="react-q08", sub="Portals", diff="medium", type="quick",
        prio="medium", market="both", mins=1,
        tags=["portal", "createportal", "modal"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What is a portal in React, and when do you use one?""",
        q_bn=r"""React-এ portal কী, আর কখন এটা ব্যবহার করো?""",
        a_en=r"""`createPortal(children, domNode)` renders children into a different DOM node, often `document.body`, while they stay in the same place in the React tree. Use it for modals, tooltips and toasts that must escape a parent's `overflow: hidden` or stacking context.""",
        a_bn=r"""`createPortal(children, domNode)` children-কে অন্য একটা DOM node-এ render করে, প্রায়ই `document.body`-তে, কিন্তু React tree-তে সেগুলো আগের জায়গাতেই থাকে। Modal, tooltip আর toast-এর জন্য এটা ব্যবহার করো, যেগুলোকে parent-এর `overflow: hidden` বা stacking context থেকে বের হতে হয়।""",
        code=r"""
            import { createPortal } from 'react-dom';

            function Modal({ children }) {
              return createPortal(<div className="modal">{children}</div>, document.body);
            }
        """, lang="jsx",
        ex_en=r"""Because the portal stays in the React tree, context still works and events bubble to React parents, even though the DOM node lives elsewhere.""",
        ex_bn=r"""Portal React tree-তেই থাকে বলে context কাজ করে, আর DOM node অন্য জায়গায় থাকলেও event React parent পর্যন্ত bubble করে।""",
        tip_en=r"""Mention the event-bubbling detail: it shows you understand React tree vs DOM tree.""",
        tip_bn=r"""Event bubbling-এর ব্যাপারটা বলো: এতে বোঝা যায় তুমি React tree আর DOM tree-এর পার্থক্য বোঝো।""",
        follow=[("What accessibility work does a modal still need?", "Modal-এ এখনো কোন accessibility-এর কাজ বাকি থাকে?")],
        related=["react-030", "react-011"],
        refs=[("react.dev — createPortal", "https://react.dev/reference/react-dom/createPortal")],
    ),
    # ------------------------------------------------------------------ react-q09
    Q(
        id="react-q09", sub="Rules of Hooks", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["hooks", "rules-of-hooks", "eslint"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""What are the Rules of Hooks?""",
        q_bn=r"""Rules of Hooks কী?""",
        a_en=r"""Call hooks only at the top level of a function component or custom hook, never inside conditions, loops or nested functions, and never from plain JavaScript functions. React identifies each hook by its call order, so that order must be the same on every render.""",
        a_bn=r"""Hook শুধু function component বা custom hook-এর top level-এ call করো; condition, loop বা nested function-এর ভেতরে না, আর সাধারণ JavaScript function থেকেও না। React প্রতিটা hook চেনে তার call-এর ক্রম দিয়ে, তাই প্রতি render-এ এই ক্রম একই থাকতে হবে।""",
        code=r"""
            function Profile({ id }) {
              if (!id) return null;
              const [user, setUser] = useState(null); // ✗ hook after an early return
            }
        """, lang="jsx",
        ex_en=r"""The `eslint-plugin-react-hooks` rules catch these mistakes. The one exception is `use()`, which may be called inside conditions and loops.""",
        ex_bn=r"""`eslint-plugin-react-hooks`-এর rule এই ভুলগুলো ধরে। একমাত্র ব্যতিক্রম `use()`, যেটা condition আর loop-এর ভেতরেও call করা যায়।""",
        tip_en=r"""Give the reason (call order), not just the rule; that's what interviewers listen for.""",
        tip_bn=r"""শুধু নিয়ম না, কারণটাও বলো (call-এর ক্রম); interviewer এটাই শুনতে চায়।""",
        follow=[("Why does a hook after an early `return` break?", "Early `return`-এর পরে hook রাখলে কেন সমস্যা হয়?")],
        related=["react-015", "react-008"],
        refs=[("react.dev — Rules of Hooks", "https://react.dev/reference/rules/rules-of-hooks")],
    ),
    # ------------------------------------------------------------------ react-q10
    Q(
        id="react-q10", sub="Event Handling", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["events", "onclick", "handlers"],
        ver="Version-independent concept (React 19.3)", vs=False, status="stable",
        q_en=r"""What is wrong with `<button onClick={handleClick()}>`?""",
        q_bn=r"""`<button onClick={handleClick()}>`-এ সমস্যা কী?""",
        a_en=r"""It calls `handleClick` during render and passes its return value (usually `undefined`) as the handler, so it runs on every render and not on click. Pass the function itself, `onClick={handleClick}`, or wrap it when you need arguments: `onClick={() => remove(id)}`.""",
        a_bn=r"""এতে render-এর সময়েই `handleClick` call হয়ে যায়, আর তার return value (সাধারণত `undefined`) handler হিসেবে যায়, তাই click-এ না চলে প্রতি render-এ চলে। Function-টাই পাঠাও, `onClick={handleClick}`, আর argument লাগলে wrap করো: `onClick={() => remove(id)}`।""",
        code=r"""
            function handleClick() { console.log('clicked'); }
            const ok = { onClick: handleClick };      // pass the function
            const bad = { onClick: handleClick() };   // calls it right now
            console.log(typeof ok.onClick, bad.onClick);
        """, lang="javascript",
        output=r"""
            clicked
            function undefined
        """,
        ex_en=r"""If the handler sets state, calling it during render can cause a "Too many re-renders" error.""",
        ex_bn=r"""Handler যদি state set করে, তাহলে render-এর সময় call করলে "Too many re-renders" error হতে পারে।""",
        tip_en=r"""Say "pass, don't call" and show the arrow-function version for arguments.""",
        tip_bn=r"""বলো "pass করো, call করো না", আর argument-এর জন্য arrow function-এর রূপটা দেখাও।""",
        follow=[("How do you stop a form's default submit in a handler?", "Handler-এ form-এর default submit কীভাবে থামাবে?")],
        related=["react-002", "react-003"],
        refs=[("react.dev — Responding to Events", "https://react.dev/learn/responding-to-events")],
    ),
]

if __name__ == "__main__":
    save("react", "quick", QUESTIONS)
