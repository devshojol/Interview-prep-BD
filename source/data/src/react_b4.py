# React — batch 4 (react-011, 020..022, 027..029, 032)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_COMMON = ("react.dev — Common components (e.g. <div>)", "https://react.dev/reference/react-dom/components/common")
R_MDN_A11Y = ("MDN — Accessibility", "https://developer.mozilla.org/en-US/docs/Web/Accessibility")
R_MDN_BUTTON = ("MDN — <button>: The Button element", "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button")
R_RTL = ("React Testing Library (GitHub)", "https://github.com/testing-library/react-testing-library")
R_USER_EVENT = ("user-event (GitHub)", "https://github.com/testing-library/user-event")
R_LISTS = ("react.dev — Rendering Lists", "https://react.dev/learn/rendering-lists")
R_PRESERVE = ("react.dev — Preserving and Resetting State", "https://react.dev/learn/preserving-and-resetting-state")
R_USE_CLIENT = ("react.dev — 'use client'", "https://react.dev/reference/rsc/use-client")
R_RSC = ("react.dev — Server Components", "https://react.dev/reference/rsc/server-components")
R_ACTIVITY = ("react.dev — <Activity>", "https://react.dev/reference/react/Activity")
R_EFFECT_EVENT = ("react.dev — useEffectEvent", "https://react.dev/reference/react/useEffectEvent")
R_REACT192 = ("react.dev — React 19.2", "https://react.dev/blog/2025/10/01/react-19-2")
R_VT = ("react.dev — <ViewTransition>", "https://react.dev/reference/react/ViewTransition")
R_REACT193 = ("react.dev — React 19.3", "https://react.dev/blog/2026/09/09/react-19-3")
R_FRAGMENT = ("react.dev — <Fragment>", "https://react.dev/reference/react/Fragment")
R_TANSTACK_VIRTUAL = ("TanStack Virtual (GitHub)", "https://github.com/TanStack/virtual")
R_CONTENT_VIS = ("web.dev — content-visibility", "https://web.dev/articles/content-visibility")
R_USEDEFERRED = ("react.dev — useDeferredValue", "https://react.dev/reference/react/useDeferredValue")
R_USESES = ("react.dev — useSyncExternalStore", "https://react.dev/reference/react/useSyncExternalStore")
R_MDN_WS = ("MDN — WebSocket", "https://developer.mozilla.org/en-US/docs/Web/API/WebSocket")

QUESTIONS = [
    # ------------------------------------------------------------------ react-011
    Q(
        id="react-011", sub="Accessibility", diff="easy", type="debugging",
        prio="medium", market="both", mins=4,
        tags=["accessibility", "a11y", "forms", "semantic-html"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""
            A screen-reader user and a keyboard-only user both say they can't use this login form. Find the accessibility problems and fix them.
        """,
        q_bn=r"""
            একজন screen-reader user আর একজন শুধু keyboard ব্যবহারকারী — দুজনই বলছেন তারা এই login form ব্যবহার করতে পারছেন না। Accessibility সমস্যাগুলো খুঁজে বের করো আর ঠিক করো।
        """,
        a_en=r"""
            There are four problems:
            1. **The "button" is a `<div>`** — it isn't focusable, doesn't respond to Enter/Space and isn't announced as a button. Use a real `<button type="submit">`.
            2. **Inputs have no labels.** A placeholder disappears when you type and isn't a reliable accessible name. Add `<label htmlFor>` (note `htmlFor`, not `for`, in JSX).
            3. **The image has no `alt`.** Screen readers may read the file name. Give meaningful `alt`, or `alt=""` if it's decorative.
            4. **No `<form>` element**, so pressing Enter doesn't submit and assistive tech doesn't see a form. Wrap the fields in `<form>`.

            I'd also add `autoComplete` hints and announce errors with `role="alert"`.
        """,
        a_bn=r"""
            চারটা সমস্যা আছে:
            1. **"Button"-টা আসলে একটা `<div>`** — এটা focus করা যায় না, Enter/Space-এ সাড়া দেয় না, আর button হিসেবে announce-ও হয় না। আসল `<button type="submit">` ব্যবহার করো।
            2. **Input-এর কোনো label নেই।** টাইপ শুরু করলে placeholder চলে যায়, আর এটা নির্ভরযোগ্য accessible name না। `<label htmlFor>` যোগ করো (JSX-এ `for` না, `htmlFor`)।
            3. **Image-এ `alt` নেই।** Screen reader হয়তো file-এর নাম পড়ে শোনাবে। অর্থপূর্ণ `alt` দাও, আর শুধু সাজসজ্জার হলে `alt=""`।
            4. **কোনো `<form>` element নেই**, তাই Enter চাপলে submit হয় না, আর assistive tech এটাকে form হিসেবে চেনে না। Field-গুলো `<form>`-এ wrap করো।

            সাথে `autoComplete` hint যোগ করব আর error `role="alert"` দিয়ে announce করব।
        """,
        ex_en=r"""
            **Rule of thumb:** use the native HTML element first. A `<button>` gives you focus, keyboard activation, the `button` role and form submission for free; recreating that on a `<div>` needs `role`, `tabIndex`, key handlers and still misses details.

            **React specifics:** JSX uses `htmlFor` and `className`, while `aria-*` and `data-*` attributes keep their hyphenated names. In reusable components generate ids with `useId` so two forms on one page don't share the same `id`.

            **How to catch these early:** `eslint-plugin-jsx-a11y`, automated axe checks in tests/CI, React Testing Library queries like `getByRole('button', { name: /log in/i })` (they fail when roles/labels are missing), and a quick manual test with only the keyboard and a screen reader.
        """,
        ex_bn=r"""
            **মূল নিয়ম:** আগে native HTML element ব্যবহার করো। `<button>` বিনা খরচে focus, keyboard দিয়ে চালানো, `button` role আর form submission দেয়; `<div>`-এ এগুলো নতুন করে বানাতে `role`, `tabIndex`, key handler লাগে, তারপরও কিছু খুঁটিনাটি বাদ পড়ে।

            **React-এর বিশেষ দিক:** JSX-এ `htmlFor` আর `className` ব্যবহার হয়, কিন্তু `aria-*` আর `data-*` attribute hyphen-সহ নামেই থাকে। Reusable component-এ `useId` দিয়ে id তৈরি করো, যাতে একই page-এ দুটো form একই `id` share না করে।

            **আগেভাগে কীভাবে ধরবে:** `eslint-plugin-jsx-a11y`, test/CI-তে automated axe check, React Testing Library-র `getByRole('button', { name: /log in/i })`-এর মতো query (role/label না থাকলে fail করে), আর শুধু keyboard ও screen reader দিয়ে একটা দ্রুত manual test।
        """,
        tip_en=r"""List the issues from most to least severe and give the fix for each. Saying "native elements first, ARIA second" is the principle interviewers want to hear.""",
        tip_bn=r"""সমস্যাগুলো সবচেয়ে গুরুতর থেকে কম গুরুতর ক্রমে বলো আর প্রতিটার সমাধান দাও। "আগে native element, তারপর ARIA" — interviewer ঠিক এই নীতিটাই শুনতে চায়।""",
        mist_en=r"""Adding `role="button"` to the `<div>` and stopping there (still not focusable or keyboard-operable), or treating placeholders as labels.""",
        mist_bn=r"""`<div>`-এ শুধু `role="button"` যোগ করে থেমে যাওয়া (তবুও focus বা keyboard দিয়ে চালানো যায় না), অথবা placeholder-কে label মনে করা।""",
        code=r"""
            export default function LoginForm({ onLogin }) {
              return (
                <div>
                  <img src="/logo.svg" />
                  <input type="email" placeholder="Email" />
                  <input type="password" placeholder="Password" />
                  <div className="btn" onClick={onLogin}>Log in</div>
                </div>
              );
            }
        """,
        lang="jsx",
        extra=[dict(lang="jsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            import { useId } from 'react';

            export default function LoginForm({ loginAction, error }) {
              const id = useId();
              return (
                <form action={loginAction}>
                  <img src="/logo.svg" alt="Acme Shop" />

                  <label htmlFor={`${id}-email`}>Email</label>
                  <input id={`${id}-email`} name="email" type="email" autoComplete="email" required />

                  <label htmlFor={`${id}-password`}>Password</label>
                  <input
                    id={`${id}-password`}
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                  />

                  {error && <p role="alert">{error}</p>}
                  <button type="submit">Log in</button>
                </form>
              );
            }
        """)],
        follow=[
            ("When is `alt=\"\"` the correct choice for an image?", "কোনো image-এর জন্য কখন `alt=\"\"` সঠিক?"),
            ("How would you move focus to an error summary after a failed submit?", "Submit fail করার পর focus কীভাবে error summary-তে নিয়ে যাবে?"),
        ],
        refs=[R_COMMON, R_MDN_BUTTON, R_MDN_A11Y],
    ),
    # ------------------------------------------------------------------ react-020
    Q(
        id="react-020", sub="Testing with React Testing Library", diff="medium", type="conceptual",
        prio="high", market="both", mins=6,
        tags=["testing", "react-testing-library", "user-event", "queries"],
        ver="React 19.3 with React Testing Library + user-event", vs=True, status="stable",
        q_en=r"""How do you test React components with React Testing Library? Explain the query priority, `user-event`, and how you test asynchronous UI.""",
        q_bn=r"""React Testing Library দিয়ে React component কীভাবে test করো? Query priority, `user-event` আর asynchronous UI কীভাবে test করো তা ব্যাখ্যা করো।""",
        a_en=r"""
            RTL's idea is to **test behaviour the way a user experiences it**, not implementation details. I render the component, find elements the way a user or screen reader would, interact, and assert on what's on screen — never on internal state or hook calls.

            **Query priority:** `getByRole` (with `{ name }`) first, then `getByLabelText`, `getByPlaceholderText`, `getByText`, `getByDisplayValue`, `getByAltText`, `getByTitle`, and `getByTestId` only as a last resort. Role-based queries also double as an accessibility check.

            **Query variants:** `getBy…` throws if the element isn't there (use for things that must exist now), `queryBy…` returns `null` (use to assert something is *absent*), and `findBy…` returns a promise that waits — that's how I test async UI.

            **Interactions:** `@testing-library/user-event` (`const user = userEvent.setup(); await user.click(...)`) simulates real typing and clicking, including focus and keyboard events, which is more realistic than `fireEvent`. For network calls I mock at the HTTP level (e.g. MSW) rather than mocking my own modules.
        """,
        a_bn=r"""
            RTL-এর মূল ধারণা হলো **user যেভাবে অনুভব করে সেভাবে behaviour test করা**, implementation-এর খুঁটিনাটি না। আমি component render করি, user বা screen reader যেভাবে খোঁজে সেভাবে element খুঁজি, interact করি, আর স্ক্রিনে কী আছে তার উপর assert করি — কখনো internal state বা hook call-এর উপর না।

            **Query priority:** প্রথমে `getByRole` (`{ name }`-সহ), তারপর `getByLabelText`, `getByPlaceholderText`, `getByText`, `getByDisplayValue`, `getByAltText`, `getByTitle`, আর একদম শেষ উপায় হিসেবে `getByTestId`। Role-ভিত্তিক query একসাথে accessibility check-এর কাজও করে।

            **Query-র ধরন:** element না থাকলে `getBy…` throw করে (যা এখনই থাকা উচিত তার জন্য), `queryBy…` `null` return করে (কিছু *নেই* সেটা assert করতে), আর `findBy…` একটা promise return করে যেটা অপেক্ষা করে — async UI এভাবেই test করি।

            **Interaction:** `@testing-library/user-event` (`const user = userEvent.setup(); await user.click(...)`) focus আর keyboard event-সহ আসল টাইপ ও click simulate করে, যেটা `fireEvent`-এর চেয়ে বাস্তবসম্মত। Network call-এর জন্য নিজের module mock না করে HTTP level-এ mock করি (যেমন MSW)।
        """,
        ex_en=r"""
            - **Avoid `act` warnings properly:** awaiting `user-event` calls and `findBy…` queries keeps updates inside `act` automatically. If you see an `act` warning, something updated after the test stopped waiting — usually a missing `await`.
            - **`waitFor`** is for assertions that become true later; don't put side effects (clicks) inside it.
            - **Matchers** like `toBeInTheDocument` and `toHaveTextContent` come from `@testing-library/jest-dom` (with Vitest, import `@testing-library/jest-dom/vitest` in the setup file).
            - **What not to test:** internal state values, the number of renders, or that a specific hook was called. Those tests break on refactors without catching real bugs.
            - **Layering:** unit/component tests with RTL + Vitest/Jest, a few end-to-end tests (Playwright) for critical flows like checkout and login.
        """,
        ex_bn=r"""
            - **`act` warning ঠিকভাবে এড়াও:** `user-event` call আর `findBy…` query await করলে update নিজে থেকেই `act`-এর ভেতরে থাকে। `act` warning দেখলে বুঝবে test অপেক্ষা থামানোর পর কিছু update হয়েছে — সাধারণত কোথাও `await` বাদ পড়েছে।
            - **`waitFor`** এমন assertion-এর জন্য, যেটা পরে সত্য হবে; এর ভেতরে side effect (click) রাখবে না।
            - **Matcher** যেমন `toBeInTheDocument` আর `toHaveTextContent` আসে `@testing-library/jest-dom` থেকে (Vitest-এ setup file-এ `@testing-library/jest-dom/vitest` import করো)।
            - **কী test করবে না:** internal state-এর value, কতবার render হলো, বা নির্দিষ্ট hook call হয়েছে কি না। এমন test refactor করলেই ভাঙে, অথচ আসল bug ধরে না।
            - **স্তর ভাগ:** RTL + Vitest/Jest দিয়ে unit/component test, আর login ও checkout-এর মতো গুরুত্বপূর্ণ flow-এর জন্য কয়েকটা end-to-end test (Playwright)।
        """,
        tip_en=r"""Lead with the philosophy ("test what the user sees"), then show you know the practical tools: query priority, get/query/find, `user-event` with `await`. A short example test makes the answer concrete.""",
        tip_bn=r"""দর্শন দিয়ে শুরু করো ("user যা দেখে সেটা test করো"), তারপর দেখাও তুমি ব্যবহারিক tool-গুলো জানো: query priority, get/query/find, `await`-সহ `user-event`। ছোট একটা উদাহরণ test দিলে উত্তরটা বাস্তব হয়।""",
        mist_en=r"""Using `getByTestId` everywhere, asserting on component state, forgetting to `await` user-event calls, or using `getBy…` to check that something is *not* rendered (it throws).""",
        mist_bn=r"""সব জায়গায় `getByTestId` ব্যবহার করা, component state-এর উপর assert করা, user-event call `await` করতে ভুলে যাওয়া, অথবা কিছু render *হয়নি* তা যাচাই করতে `getBy…` ব্যবহার করা (এটা throw করে)।""",
        code=r"""
            import { render, screen } from '@testing-library/react';
            import userEvent from '@testing-library/user-event';
            import { expect, test } from 'vitest';
            import LoginPage from './LoginPage';

            test('shows an error when the password is wrong', async () => {
              const user = userEvent.setup();
              render(<LoginPage />); // the API is mocked with MSW to return 401

              await user.type(screen.getByLabelText(/email/i), 'rahim@example.com');
              await user.type(screen.getByLabelText(/password/i), 'wrong-pass');
              await user.click(screen.getByRole('button', { name: /log in/i }));

              // findBy waits for the async error to appear
              expect(await screen.findByRole('alert')).toHaveTextContent(/invalid email or password/i);
              // queryBy returns null instead of throwing
              expect(screen.queryByText(/welcome back/i)).not.toBeInTheDocument();
            });
        """,
        lang="jsx",
        follow=[
            ("How would you test a component that uses a Context provider or a Redux store?", "Context provider বা Redux store ব্যবহার করে এমন component কীভাবে test করবে?"),
            ("When would you write an end-to-end test instead of a component test?", "কখন component test-এর বদলে end-to-end test লিখবে?"),
        ],
        related=["react-011"],
        refs=[R_RTL, R_USER_EVENT],
    ),
    # ------------------------------------------------------------------ react-021
    Q(
        id="react-021", sub="Keys and List Rendering", diff="medium", type="debugging",
        prio="high", market="bangladesh", mins=5,
        tags=["keys", "index-as-key", "lists", "state-bug"],
        ver="Version-independent concept (React 19.3)", vs=False, status="stable",
        q_en=r"""
            QA reports: "I typed `urgent` in the note field of **Buy milk**, then deleted **Buy milk**. Now **Call Karim** shows the note `urgent`." Explain why this happens and fix it.
        """,
        q_bn=r"""
            QA জানাল: "**Buy milk**-এর note field-এ `urgent` লিখলাম, তারপর **Buy milk** delete করলাম। এখন **Call Karim**-এর পাশে note দেখাচ্ছে `urgent`।" কেন এমন হচ্ছে ব্যাখ্যা করো আর ঠিক করো।
        """,
        a_en=r"""
            The list uses the **array index as the key**. Keys tell React which element is which between renders.

            Before deleting: key `0` = Buy milk, `1` = Call Karim, `2` = Pay bills. After deleting the first item the array is shorter, so now key `0` = Call Karim and key `1` = Pay bills. React compares by key: it sees that `0` and `1` still exist and only key `2` disappeared. So it **keeps the first `<li>` and its DOM input (with "urgent")**, just updating the text to "Call Karim", and removes the *last* row.

            Fix: use a stable id from the data as the key (`key={todo.id}`) and delete by id, not by index. Then React removes exactly the `<li>` for Buy milk, together with its input.
        """,
        a_bn=r"""
            List-এ **array index-কে key** হিসেবে ব্যবহার করা হয়েছে। Render-এর মধ্যে কোন element কোনটা, সেটা React key দিয়ে বোঝে।

            Delete-এর আগে: key `0` = Buy milk, `1` = Call Karim, `2` = Pay bills। প্রথম item delete করার পর array ছোট হয়ে যায়, ফলে এখন key `0` = Call Karim আর key `1` = Pay bills। React key দিয়ে তুলনা করে: দেখে `0` আর `1` এখনো আছে, শুধু key `2` নেই। তাই সে **প্রথম `<li>` আর তার DOM input ("urgent"-সহ) রেখে দেয়**, শুধু লেখাটা "Call Karim"-এ update করে, আর *শেষের* row সরিয়ে দেয়।

            সমাধান: data থেকে আসা স্থায়ী id-কে key হিসেবে ব্যবহার করো (`key={todo.id}`) আর index না, id দিয়ে delete করো। তখন React ঠিক Buy milk-এর `<li>`-টাই তার input-সহ সরিয়ে দেয়।
        """,
        ex_en=r"""
            The note lives in **uncontrolled DOM state** (and the same happens with component state inside each row). React attaches that state to the key, not to the data, so when keys shift, state "moves" to another item.

            Index keys are only safe when the list is static: never reordered, filtered, or has items inserted/removed in the middle. Also avoid generating keys during render (`Math.random()`, `crypto.randomUUID()` in `map`), which remounts every row each time. If items come without ids, assign one when they're created.

            This bug is easy to miss in demos because adding to the *end* of the list works fine — it only shows up on deletion, insertion at the top, sorting or filtering.
        """,
        ex_bn=r"""
            Note-টা থাকে **uncontrolled DOM state**-এ (প্রতিটা row-এর ভেতরের component state-এর ক্ষেত্রেও একই ঘটনা ঘটে)। React এই state data-র সাথে না, key-র সাথে যুক্ত রাখে, তাই key সরে গেলে state অন্য item-এ "চলে যায়"।

            Index key শুধু তখনই নিরাপদ, যখন list static: কখনো reorder, filter হয় না, বা মাঝখানে item যোগ/মুছে ফেলা হয় না। Render-এর সময় key তৈরি করাও (`map`-এর ভেতরে `Math.random()`, `crypto.randomUUID()`) এড়িয়ে চলো — এতে প্রতিবার প্রতিটা row remount হয়। Item-এর id না থাকলে তৈরি করার সময়ই একটা id দাও।

            Demo-তে এই bug সহজে চোখে পড়ে না, কারণ list-এর *শেষে* যোগ করলে সব ঠিক থাকে — delete, উপরে insert, sort বা filter করলেই কেবল দেখা দেয়।
        """,
        tip_en=r"""Walk through the keys before and after the deletion — interviewers love seeing you "be the reconciler". Then state when index keys are acceptable.""",
        tip_bn=r"""Delete-এর আগে আর পরে key-গুলো ধাপে ধাপে দেখাও — interviewer তোমাকে "reconciler-এর মতো চিন্তা করতে" দেখতে পছন্দ করে। তারপর বলো কখন index key চলে।""",
        mist_en=r"""Thinking the bug is in the `filter` logic, or "fixing" it by making the input controlled while still using index keys (row components with their own state would still mix up).""",
        mist_bn=r"""ভাবা যে bug-টা `filter` logic-এ, অথবা index key রেখেই input controlled করে "ঠিক" করা (নিজস্ব state-ওয়ালা row component তখনো এলোমেলো হবে)।""",
        code=r"""
            import { useState } from 'react';

            export default function TodoList() {
              const [todos, setTodos] = useState([
                { id: 'a1', title: 'Buy milk' },
                { id: 'b2', title: 'Call Karim' },
                { id: 'c3', title: 'Pay bills' },
              ]);

              function remove(index) {
                setTodos(todos.filter((_, i) => i !== index));
              }

              return (
                <ul>
                  {todos.map((todo, index) => (
                    <li key={index}>
                      {todo.title}
                      <input placeholder="Add a note" />
                      <button onClick={() => remove(index)}>Delete</button>
                    </li>
                  ))}
                </ul>
              );
            }
        """,
        lang="jsx",
        extra=[dict(lang="jsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            import { useState } from 'react';

            export default function TodoList() {
              const [todos, setTodos] = useState([
                { id: 'a1', title: 'Buy milk' },
                { id: 'b2', title: 'Call Karim' },
                { id: 'c3', title: 'Pay bills' },
              ]);

              function remove(id) {
                setTodos((prev) => prev.filter((t) => t.id !== id));
              }

              return (
                <ul>
                  {todos.map((todo) => (
                    <li key={todo.id}>
                      {todo.title}
                      <input placeholder="Add a note" aria-label={`Note for ${todo.title}`} />
                      <button onClick={() => remove(todo.id)}>Delete</button>
                    </li>
                  ))}
                </ul>
              );
            }
        """)],
        follow=[
            ("When is using the index as a key acceptable?", "কখন index-কে key হিসেবে ব্যবহার করা গ্রহণযোগ্য?"),
            ("How can you intentionally reset a component's state using `key`?", "`key` দিয়ে ইচ্ছাকৃতভাবে কোনো component-এর state কীভাবে reset করবে?"),
        ],
        related=["react-004", "react-023"],
        refs=[R_LISTS, R_PRESERVE],
    ),
    # ------------------------------------------------------------------ react-022
    Q(
        id="react-022", sub="Server and Client Components", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["server-components", "use-client", "serialization", "rsc"],
        ver="React 19.3 (Server Components via a framework, e.g. Next.js 16.4)", vs=True, status="stable",
        q_en=r"""A Server Component renders a Client Component (a module marked with `'use client'`). Which prop can **not** be passed from the Server Component to the Client Component?""",
        q_bn=r"""একটা Server Component একটা Client Component (`'use client'` দেওয়া module) render করছে। Server Component থেকে Client Component-এ নিচের কোন prop পাঠানো **যাবে না**?""",
        options=[
            ("A plain object like `{ id: 1, name: 'Rahim', joinedAt: new Date() }`", "একটা plain object, যেমন `{ id: 1, name: 'Rahim', joinedAt: new Date() }`"),
            ("A `Promise` that the Client Component unwraps with `use()`", "একটা `Promise`, যেটা Client Component `use()` দিয়ে unwrap করে"),
            ("An inline handler such as `onSelect={(id) => console.log(id)}`", "Inline handler, যেমন `onSelect={(id) => console.log(id)}`"),
            ("Server-rendered JSX passed as `children`", "Server-এ render হওয়া JSX, `children` হিসেবে পাঠানো"),
        ],
        correct=2,
        a_en=r"""A regular function can't cross the server→client boundary, because props are **serialised** and sent over the network. The only functions allowed are Server Functions (marked `'use server'`), which are sent as references the client can call.""",
        a_bn=r"""সাধারণ function server→client boundary পার হতে পারে না, কারণ props **serialise** করে network দিয়ে পাঠানো হয়। শুধু Server Function (`'use server'` দেওয়া) পাঠানো যায়, যেগুলো এমন reference হিসেবে যায় যেটা client call করতে পারে।""",
        ex_en=r"""
            The tempting wrong answer is the **Promise**. React can serialise promises: the server starts the fetch, passes the promise, and the Client Component reads it with `use()` inside a `<Suspense>` boundary — a useful streaming pattern. Plain objects, arrays, `Date`, `Map`, `Set`, typed arrays and JSX (including Server Component output as `children`) are all supported.

            Not supported: ordinary functions, class instances, and symbols that aren't registered globally. Fixes for the handler: define it **inside** the Client Component, or pass a Server Function if the work must happen on the server.

            Related rules: `'use client'` marks a module boundary — that module and everything it imports become client code. Keep the directive on interactive leaves so most of the tree stays on the server, and import the `server-only` package in modules that must never reach the client bundle (database code, secrets).
        """,
        ex_bn=r"""
            লোভনীয় ভুল উত্তর হলো **Promise**। React promise serialise করতে পারে: server fetch শুরু করে, promise-টা পাঠায়, আর Client Component একটা `<Suspense>` boundary-র ভেতরে `use()` দিয়ে সেটা পড়ে — এটা streaming-এর একটা কাজের pattern। Plain object, array, `Date`, `Map`, `Set`, typed array আর JSX (`children` হিসেবে Server Component-এর output-সহ) — সবই support করে।

            Support করে না: সাধারণ function, class instance, আর globally register না করা symbol। Handler-এর সমাধান: এটাকে Client Component-এর **ভেতরে** define করো, অথবা কাজটা server-এ করতে হলে একটা Server Function পাঠাও।

            সংশ্লিষ্ট নিয়ম: `'use client'` একটা module boundary চিহ্নিত করে — ওই module আর সে যা import করে সব client code হয়ে যায়। Directive-টা interactive leaf-এ রাখো, যাতে tree-র বেশিরভাগ অংশ server-এ থাকে, আর যেসব module কখনো client bundle-এ যাওয়া উচিত না (database code, secret), সেখানে `server-only` package import করো।
        """,
        tip_en=r"""Say the key word "serialisable" and list what *is* allowed (including promises and JSX) — knowing the surprising "yes" cases impresses more than only knowing functions are forbidden.""",
        tip_bn=r"""মূল শব্দ "serialisable" বলো, আর কী কী *পাঠানো যায়* তার তালিকা দাও (promise আর JSX-সহ) — শুধু function নিষেধ জানার চেয়ে অপ্রত্যাশিত "হ্যাঁ" case-গুলো জানা বেশি প্রভাব ফেলে।""",
        refs=[R_USE_CLIENT, R_RSC],
    ),
    # ------------------------------------------------------------------ react-027
    Q(
        id="react-027", sub="Activity and useEffectEvent", diff="hard", type="conceptual",
        prio="medium", market="both", mins=8,
        tags=["activity", "useeffectevent", "react-19-2", "effects"],
        ver="React 19.3 (both APIs stable since 19.2)", vs=True, status="stable",
        q_en=r"""React 19.2 introduced `<Activity>` and `useEffectEvent`. What problem does each solve, and what are the gotchas?""",
        q_bn=r"""React 19.2-এ `<Activity>` আর `useEffectEvent` এসেছে। প্রতিটা কোন সমস্যার সমাধান করে, আর এদের gotcha কী কী?""",
        a_en=r"""
            **`<Activity mode="visible" | "hidden">`** hides part of the UI **without unmounting it**. Before, you had two bad options: conditional rendering (`{show && <Tab />}`) loses state and DOM, while CSS hiding keeps everything running at full priority. When an Activity is hidden, React hides its DOM (`display: none`), **cleans up its effects**, and defers its updates until there's nothing more urgent — but keeps its state. When it becomes visible again, effects re-run and the user finds their draft, scroll position or form input intact. It's also useful to pre-render a likely next screen in the background.

            **`useEffectEvent(fn)`** separates *non-reactive* logic from an effect. The returned function always sees the latest props and state, but it's not a dependency, so changing those values doesn't re-run the effect. Classic case: a chat effect should reconnect when `roomId` changes, but not when `theme` changes, even though the "connected" notification uses the theme.

            Gotchas: Effect Events must only be called from inside effects (not during render, not passed to children), and must not be listed in dependencies — the updated `eslint-plugin-react-hooks` knows this. For Activity, effects need proper cleanup, because hiding runs it — e.g. a video must pause in its effect cleanup, or it keeps playing while hidden.
        """,
        a_bn=r"""
            **`<Activity mode="visible" | "hidden">`** UI-র কোনো অংশ **unmount না করেই** লুকিয়ে রাখে। আগে দুটো খারাপ উপায় ছিল: conditional rendering (`{show && <Tab />}`) state আর DOM হারায়, আর CSS দিয়ে লুকালে সবকিছু পূর্ণ priority-তে চলতে থাকে। Activity hidden হলে React তার DOM লুকিয়ে রাখে (`display: none`), **তার effect cleanup করে**, আর আরও জরুরি কিছু না থাকা পর্যন্ত update পিছিয়ে দেয় — কিন্তু state রেখে দেয়। আবার visible হলে effect নতুন করে চলে, আর user তার draft, scroll position বা form input অক্ষত পায়। সম্ভাব্য পরের screen background-এ pre-render করতেও এটা কাজে লাগে।

            **`useEffectEvent(fn)`** effect থেকে *non-reactive* logic আলাদা করে। Return হওয়া function সবসময় সর্বশেষ props আর state দেখে, কিন্তু এটা dependency না, তাই ওই value বদলালে effect আবার চলে না। Classic উদাহরণ: chat effect `roomId` বদলালে reconnect করবে, কিন্তু `theme` বদলালে না — যদিও "connected" notification theme ব্যবহার করে।

            Gotcha: Effect Event শুধু effect-এর ভেতর থেকে call করতে হবে (render-এর সময় না, child-এ পাঠিয়ে না), আর dependency-তে রাখা যাবে না — আপডেট হওয়া `eslint-plugin-react-hooks` এটা জানে। Activity-র ক্ষেত্রে effect-এর সঠিক cleanup থাকতে হবে, কারণ hide করলে cleanup চলে — যেমন video-কে effect cleanup-এ pause করতে হবে, নইলে লুকানো অবস্থাতেও চলতে থাকবে।
        """,
        ex_en=r"""
            **Why Activity cleans up effects:** hidden UI shouldn't keep subscriptions, timers or network polling alive. Treating hide/show like unmount/remount for effects (but not for state) is exactly what StrictMode's double-effect check prepares you for — symmetrical effects "just work".

            **Rendering while hidden:** a hidden subtree can still re-render at low priority when its props change, so it's ready when shown. Don't put dozens of heavy screens in hidden Activities — they still consume memory.

            **Don't misuse `useEffectEvent`:** it's for logic that truly shouldn't trigger re-synchronisation (logging, notifications, reading the latest settings). Using it to hide a real dependency recreates the stale-data bugs the dependency array protects you from.
        """,
        ex_bn=r"""
            **Activity কেন effect cleanup করে:** লুকানো UI-এর subscription, timer বা network polling চালু রাখা উচিত না। Effect-এর জন্য hide/show-কে unmount/remount-এর মতো ধরা (কিন্তু state-এর জন্য না) — ঠিক এটার জন্যই StrictMode-এর double-effect check তোমাকে প্রস্তুত করে; symmetrical effect থাকলে সব নিজে থেকেই ঠিকঠাক চলে।

            **Hidden অবস্থায় rendering:** props বদলালে hidden subtree কম priority-তে re-render হতে পারে, যাতে দেখানোর সময় প্রস্তুত থাকে। ডজনখানেক ভারী screen hidden Activity-তে রেখো না — এরা তবুও memory খরচ করে।

            **`useEffectEvent`-এর অপব্যবহার করো না:** এটা এমন logic-এর জন্য, যেটা আসলেই re-synchronisation trigger করা উচিত না (logging, notification, সর্বশেষ setting পড়া)। আসল dependency লুকাতে এটা ব্যবহার করলে dependency array যে stale-data bug থেকে রক্ষা করে, সেগুলোই আবার ফিরে আসে।
        """,
        tip_en=r"""For each API, state "before / after": what people did before and why it was painful. Then give one concrete use case and one gotcha each — that structure makes a new-feature answer sound experienced rather than memorised from a blog post.""",
        tip_bn=r"""প্রতিটা API-র জন্য "আগে / পরে" বলো: আগে মানুষ কী করত আর সেটা কেন কষ্টকর ছিল। তারপর প্রতিটার একটা বাস্তব use case আর একটা gotcha দাও — এই কাঠামোয় নতুন feature-এর উত্তর blog থেকে মুখস্থ না, অভিজ্ঞ মানুষের মতো শোনায়।""",
        mist_en=r"""Thinking effects keep running inside a hidden Activity, or calling an Effect Event from an event handler or during render.""",
        mist_bn=r"""ভাবা যে hidden Activity-র ভেতরে effect চলতেই থাকে, অথবা event handler থেকে বা render-এর সময় Effect Event call করা।""",
        code=r"""
            import { Activity, useEffect, useEffectEvent, useState } from 'react';

            // 1) Activity: keep the draft when switching tabs
            export function Mailbox() {
              const [tab, setTab] = useState('inbox');
              return (
                <>
                  <TabBar current={tab} onSelect={setTab} />
                  <Activity mode={tab === 'inbox' ? 'visible' : 'hidden'}>
                    <Inbox />
                  </Activity>
                  <Activity mode={tab === 'compose' ? 'visible' : 'hidden'}>
                    <ComposeEmail /> {/* draft state survives tab switches */}
                  </Activity>
                </>
              );
            }

            // 2) useEffectEvent: reconnect on roomId, not on theme
            export function ChatRoom({ roomId, theme }) {
              const onConnected = useEffectEvent(() => {
                showNotification('Connected!', theme); // always the latest theme
              });

              useEffect(() => {
                const connection = createConnection(roomId);
                connection.on('connected', () => onConnected());
                connection.connect();
                return () => connection.disconnect();
              }, [roomId]); // theme is intentionally not a dependency

              return <Messages roomId={roomId} />;
            }
        """,
        lang="jsx",
        follow=[
            ("How is `<Activity mode=\"hidden\">` different from rendering with `display: none` yourself?", "নিজে `display: none` দিয়ে render করা আর `<Activity mode=\"hidden\">`-এর মধ্যে পার্থক্য কী?"),
            ("How did people solve the `theme`-in-effect problem before `useEffectEvent`?", "`useEffectEvent`-এর আগে মানুষ effect-এর ভেতরে `theme`-এর সমস্যা কীভাবে সমাধান করত?"),
        ],
        related=["react-012", "react-013"],
        refs=[R_ACTIVITY, R_EFFECT_EVENT, R_REACT192],
    ),
    # ------------------------------------------------------------------ react-028
    Q(
        id="react-028", sub="React 19.3 Features", diff="hard", type="mcq",
        prio="low", market="international", mins=4,
        tags=["viewtransition", "react-19-3", "transitions", "animation"],
        ver="React 19.3 (<ViewTransition> stable since 19.3)", vs=True, status="stable",
        q_en=r"""
            In React 19.3 you wrap the gallery image in `<ViewTransition>`. Clicking **Next** switches the photo instantly, with no animation. What is the reason?
        """,
        q_bn=r"""
            React 19.3-এ তুমি gallery-র image-টা `<ViewTransition>`-এ wrap করেছ। **Next**-এ click করলে photo সাথে সাথে বদলে যায়, কোনো animation হয় না। কারণ কী?
        """,
        code=r"""
            import { useState, ViewTransition } from 'react';

            export default function Gallery({ photos }) {
              const [index, setIndex] = useState(0);
              const photo = photos[index];

              return (
                <>
                  <ViewTransition key={photo.id}>
                    <img src={photo.url} alt={photo.alt} />
                  </ViewTransition>
                  <button onClick={() => setIndex((i) => (i + 1) % photos.length)}>
                    Next
                  </button>
                </>
              );
            }
        """,
        lang="jsx",
        options=[
            ("`<ViewTransition>` only animates updates that come from a Transition (e.g. `startTransition`), a `useDeferredValue` update or a Suspense reveal — a plain urgent `setState` doesn't activate it", "`<ViewTransition>` শুধু Transition (যেমন `startTransition`), `useDeferredValue` update বা Suspense reveal থেকে আসা update animate করে — সাধারণ urgent `setState` এটাকে চালু করে না"),
            ("Changing the `key` remounts `<ViewTransition>`, and remounting cancels any running animation", "`key` বদলালে `<ViewTransition>` remount হয়, আর remount চলমান যেকোনো animation বাতিল করে দেয়"),
            ("`<ViewTransition>` is still canary-only in React 19.3", "React 19.3-এ `<ViewTransition>` এখনো শুধু canary-তে আছে"),
            ("The image must be wrapped in a `<Fragment ref>` so React can measure its DOM nodes", "Image-কে `<Fragment ref>`-এ wrap করতে হবে, যাতে React তার DOM node মাপতে পারে"),
        ],
        correct=0,
        a_en=r"""`<ViewTransition>` (stable in React 19.3) is activated only by **non-urgent** updates: `startTransition`, `useDeferredValue` or a Suspense boundary revealing content. Urgent updates apply immediately. Fix: `onClick={() => startTransition(() => setIndex(...))}`.""",
        a_bn=r"""`<ViewTransition>` (React 19.3-এ stable) শুধু **non-urgent** update-এ চালু হয়: `startTransition`, `useDeferredValue` বা কোনো Suspense boundary content দেখানো। Urgent update সাথে সাথে apply হয়। সমাধান: `onClick={() => startTransition(() => setIndex(...))}`।""",
        ex_en=r"""
            The tempting wrong answer is the `key`: changing the key is actually what makes this work — the old `<ViewTransition>` "exits" and the new one "enters" in the same Transition, and React runs a cross-fade by default using the browser's View Transition API. You can then customise it with View Transition classes in CSS, and with `addTransitionType('next')` inside `startTransition` you can animate "next" and "previous" differently (e.g. `enter={{ next: 'from-right', previous: 'from-left' }}`). Respect `prefers-reduced-motion`.

            Other React 19.3 additions worth knowing:
            - **Fragment refs (stable):** `<Fragment ref={ref}>` gives a `FragmentInstance` with methods like `addEventListener`, `focus`, `focusLast`, `observeUsing` (Intersection/ResizeObserver) and `getClientRects` that act on the Fragment's first-level DOM children — no wrapper `<div>` needed.
            - **`browser()` from `react-dom`:** `use(browser())` suspends during server rendering, so the nearest `<Suspense>` fallback goes into the HTML and the component renders only in the browser after hydration — replacing the old "`mounted` state set in an effect" trick.
        """,
        ex_bn=r"""
            লোভনীয় ভুল উত্তর হলো `key`: আসলে key বদলানোর কারণেই এটা কাজ করে — একই Transition-এ পুরনো `<ViewTransition>` "exit" করে আর নতুনটা "enter" করে, আর React default-ভাবে browser-এর View Transition API দিয়ে একটা cross-fade চালায়। এরপর CSS-এ View Transition class দিয়ে এটা customise করা যায়, আর `startTransition`-এর ভেতরে `addTransitionType('next')` দিয়ে "next" আর "previous" আলাদাভাবে animate করা যায় (যেমন `enter={{ next: 'from-right', previous: 'from-left' }}`)। `prefers-reduced-motion` মেনে চলো।

            React 19.3-এর আরও কিছু জানার মতো সংযোজন:
            - **Fragment ref (stable):** `<Fragment ref={ref}>` একটা `FragmentInstance` দেয়, যার `addEventListener`, `focus`, `focusLast`, `observeUsing` (Intersection/ResizeObserver) আর `getClientRects`-এর মতো method Fragment-এর প্রথম স্তরের DOM children-এর উপর কাজ করে — বাড়তি wrapper `<div>` লাগে না।
            - **`react-dom` থেকে `browser()`:** server rendering-এর সময় `use(browser())` suspend করে, ফলে সবচেয়ে কাছের `<Suspense>` fallback HTML-এ যায় আর component শুধু hydration-এর পর browser-এ render হয় — পুরনো "effect-এ `mounted` state set করা" কৌশলের বদলে।
        """,
        tip_en=r"""Connect the new API to concepts you already know: "ViewTransition is driven by transitions — the same urgent vs non-urgent split as `useTransition`." Linking features to fundamentals shows understanding, not just release-note memory.""",
        tip_bn=r"""নতুন API-কে পরিচিত ধারণার সাথে যুক্ত করো: "ViewTransition চলে transition দিয়ে — `useTransition`-এর মতোই urgent বনাম non-urgent ভাগ।" Feature-কে মূল ধারণার সাথে যুক্ত করলে বোঝা যায় তুমি বোঝো, শুধু release note মুখস্থ করোনি।""",
        related=["react-024", "react-027"],
        refs=[R_VT, R_REACT193, R_FRAGMENT],
    ),
    # ------------------------------------------------------------------ react-029
    Q(
        id="react-029", sub="Rendering Large Lists", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["virtualization", "large-lists", "performance", "windowing"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""
            An orders table must show 10,000 rows with sorting and a search box. The first render takes about 3 seconds and scrolling is janky. How do you make it fast?
        """,
        q_bn=r"""
            একটা orders table-এ sorting আর search box-সহ ১০,০০০ row দেখাতে হবে। প্রথম render-এ প্রায় ৩ সেকেন্ড লাগে আর scroll করলে আটকে আটকে যায়। এটা কীভাবে দ্রুত করবে?
        """,
        a_en=r"""
            The real bottleneck is the **DOM size**: 10,000 rows × 8 cells is 80,000+ elements that React must create and the browser must lay out and paint. Memoization alone can't fix that.

            1. **Virtualise (windowing).** Render only the rows in the viewport plus a small overscan (so only ~30–50 rows are mounted) inside a tall spacer, using a library like TanStack Virtual or react-window. The DOM size stays constant no matter how many rows exist.
            2. **Make each row cheap.** Stable keys (`order.id`), a memoized row component (or React Compiler), no inline objects created per row, and sorting/filtering done once per change (`useMemo`), not inside rows.
            3. **Keep interactions responsive.** Keep the search input urgent and render results from `useDeferredValue(query)`; trigger sorting inside `startTransition`.
            4. **Move work off the client if possible.** For very large or growing datasets, sort/filter/paginate on the server (cursor-based pagination or infinite loading); for heavy client computation, use a Web Worker.
            5. **Measure** before and after with the React Profiler and the Performance panel.
        """,
        a_bn=r"""
            আসল bottleneck হলো **DOM-এর আকার**: ১০,০০০ row × ৮টা cell মানে ৮০,০০০+ element, যেগুলো React-কে তৈরি করতে হয় আর browser-কে layout ও paint করতে হয়। শুধু memoization দিয়ে এটা ঠিক হবে না।

            1. **Virtualise (windowing) করো।** শুধু viewport-এ থাকা row আর সামান্য overscan একটা লম্বা spacer-এর ভেতরে render করো (ফলে একসাথে মাত্র ~৩০–৫০টা row mount থাকে) — TanStack Virtual বা react-window-এর মতো library দিয়ে। Row যত বেশিই হোক, DOM-এর আকার স্থির থাকে।
            2. **প্রতিটা row সস্তা করো।** Stable key (`order.id`), memoized row component (বা React Compiler), প্রতি row-এ নতুন inline object না, আর sorting/filtering প্রতিটা পরিবর্তনে একবার (`useMemo`), row-এর ভেতরে না।
            3. **Interaction responsive রাখো।** Search input urgent রাখো আর result render করো `useDeferredValue(query)` থেকে; sorting চালাও `startTransition`-এর ভেতরে।
            4. **সম্ভব হলে কাজ client থেকে সরাও।** খুব বড় বা বাড়তে থাকা dataset-এর জন্য server-এ sort/filter/paginate করো (cursor-based pagination বা infinite loading); client-এ ভারী হিসাবের জন্য Web Worker।
            5. **আগে-পরে মাপো** React Profiler আর Performance panel দিয়ে।
        """,
        ex_en=r"""
            **Trade-offs of virtualisation**
            - Browser find (Ctrl+F) and screen readers only "see" mounted rows. Mitigate with your own search, `aria-rowcount` on the table plus `aria-rowindex` on each row, and keyboard navigation that scrolls the virtualizer.
            - Variable row heights need measuring (`measureElement` in TanStack Virtual), which costs layout work.
            - Printing or "select all" needs special handling.

            **Simpler alternatives:** pagination is often the best UX for business tables. For long *documents* (not interactive tables), CSS `content-visibility: auto` lets the browser skip rendering off-screen sections while keeping them in the DOM — easy, but the React render cost remains.

            **Security/perf angle:** never ship 10,000 rows of data the user isn't allowed to see "because the UI filters it" — filter on the server.
        """,
        ex_bn=r"""
            **Virtualisation-এর trade-off**
            - Browser find (Ctrl+F) আর screen reader শুধু mount হওয়া row-ই "দেখে"। নিজস্ব search, table-এ `aria-rowcount` আর প্রতিটা row-এ `aria-rowindex`, আর virtualizer scroll করে এমন keyboard navigation দিয়ে এটা সামলাও।
            - Row-এর উচ্চতা আলাদা আলাদা হলে মাপতে হয় (TanStack Virtual-এ `measureElement`), যাতে layout-এর খরচ লাগে।
            - Print বা "select all"-এর জন্য বিশেষ ব্যবস্থা লাগে।

            **সহজ বিকল্প:** business table-এর জন্য প্রায়ই pagination-ই সবচেয়ে ভালো UX। লম্বা *document*-এর জন্য (interactive table না), CSS `content-visibility: auto` browser-কে screen-এর বাইরের অংশ render না করে DOM-এ রেখে দিতে দেয় — সহজ, কিন্তু React-এর render খরচ থেকেই যায়।

            **Security/perf দিক:** "UI তো filter করে দেয়" ভেবে user-এর দেখার অনুমতি নেই এমন ১০,০০০ row-এর data কখনো পাঠাবে না — server-এ filter করো।
        """,
        tip_en=r"""Name the root cause first (DOM size), then layer the fixes from biggest impact (virtualisation, server pagination) to smaller ones (memo, deferred values). Mentioning the accessibility trade-off of virtualisation is a senior-level touch.""",
        tip_bn=r"""আগে root cause-এর নাম বলো (DOM-এর আকার), তারপর সবচেয়ে বড় প্রভাব (virtualisation, server pagination) থেকে ছোট প্রভাবের (memo, deferred value) ক্রমে সমাধান সাজাও। Virtualisation-এর accessibility trade-off উল্লেখ করা senior-level ছোঁয়া।""",
        mist_en=r"""Answering only "use `React.memo`/`useMemo`", which doesn't reduce the number of DOM nodes, or virtualising without stable keys.""",
        mist_bn=r"""শুধু "`React.memo`/`useMemo` ব্যবহার করো" বলা, যেটা DOM node-এর সংখ্যা কমায় না, অথবা stable key ছাড়া virtualise করা।""",
        code=r"""
            import { useRef } from 'react';
            import { useVirtualizer } from '@tanstack/react-virtual';

            export function OrdersTable({ rows }) {
              const scrollRef = useRef(null);
              const virtualizer = useVirtualizer({
                count: rows.length,
                getScrollElement: () => scrollRef.current,
                estimateSize: () => 40, // px per row
                overscan: 10,
              });

              return (
                <div ref={scrollRef} style={{ height: 600, overflow: 'auto' }}>
                  <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
                    {virtualizer.getVirtualItems().map((item) => {
                      const order = rows[item.index];
                      return (
                        <div
                          key={order.id}
                          style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '100%',
                            height: item.size,
                            transform: `translateY(${item.start}px)`,
                          }}
                        >
                          <OrderRow order={order} />
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            }
        """,
        lang="jsx",
        follow=[
            ("How would you keep keyboard navigation and screen-reader support in a virtualised table?", "Virtualised table-এ keyboard navigation আর screen-reader support কীভাবে রাখবে?"),
            ("When would you choose server-side pagination over client-side virtualisation?", "কখন client-side virtualisation-এর বদলে server-side pagination বেছে নেবে?"),
        ],
        related=["react-024", "react-026"],
        refs=[R_TANSTACK_VIRTUAL, R_CONTENT_VIS, R_USEDEFERRED],
    ),
    # ------------------------------------------------------------------ react-032
    Q(
        id="react-032", sub="Real-time UI Architecture", diff="extreme", type="system-design",
        prio="medium", market="international", mins=20,
        tags=["websocket", "usesyncexternalstore", "real-time", "batching", "memory-leaks"],
        ver="React 19.3", vs=False, status="stable",
        q_en=r"""
            A logistics dashboard receives about 50 WebSocket messages per second (position/status updates for 2,000 vehicles) and shows a live table, charts and alerts. The first version stores every message in React state; after a few minutes the tab freezes and memory keeps growing. Design a client architecture that stays responsive for hours.
        """,
        q_bn=r"""
            একটা logistics dashboard প্রতি সেকেন্ডে প্রায় ৫০টা WebSocket message পায় (২,০০০ গাড়ির position/status update), আর live table, chart ও alert দেখায়। প্রথম version প্রতিটা message React state-এ রাখে; কয়েক মিনিট পর tab আটকে যায় আর memory বাড়তেই থাকে। এমন একটা client architecture design করো, যেটা ঘণ্টার পর ঘণ্টা responsive থাকে।
        """,
        a_en=r"""
            *(Advanced, senior-level design question.)* Goals: sub-second freshness, interactions under ~200 ms (INP), flat memory over hours, and no out-of-order data.

            **1. Connection layer outside React.** A single WebSocket manager module handles connect, heartbeat, reconnect with exponential backoff + jitter, and resubscription. Messages carry a sequence number or timestamp so stale/out-of-order updates are dropped. Heavy parsing can move to a Web Worker.

            **2. An external store, not React state per message.** Keep a normalised `Map` by vehicle id outside React. Buffer incoming messages and **coalesce** them (only the latest per id), then flush at most once per animation frame (or every 100–250 ms). One flush = one notification, instead of 50 `setState` calls per second.

            **3. Selective subscriptions.** Components read the store through `useSyncExternalStore` with a per-item selector, so when vehicle 42 changes only the row showing vehicle 42 re-renders. The table is virtualised, so only ~50 rows subscribe at a time.

            **4. Charts and alerts at their own pace.** Update charts imperatively through the chart library's API at a capped rate (2–4 fps) and keep history in bounded ring buffers. Alerts are derived from the store and de-duplicated.

            **5. Memory hygiene.** Every subscription, listener and interval has a cleanup; no unbounded arrays in state; verify with heap snapshots over a long session.

            **6. Server cooperation.** Send deltas, aggregate on the server, and let the client subscribe only to what's visible (viewport-based subscriptions) to cut traffic.

            Trade-off: coalescing trades a little freshness for a lot of CPU; immutable per-item objects make change detection cheap but allocate more.
        """,
        a_bn=r"""
            *(Advanced, senior-level design প্রশ্ন।)* লক্ষ্য: এক সেকেন্ডের কম সময়ে fresh data, ~২০০ ms-এর কম interaction (INP), ঘণ্টার পর ঘণ্টা স্থির memory, আর ক্রমের বাইরে আসা data না দেখানো।

            **১. React-এর বাইরে connection layer।** একটাই WebSocket manager module connect, heartbeat, exponential backoff + jitter-সহ reconnect আর resubscription সামলায়। প্রতিটা message-এ sequence number বা timestamp থাকে, যাতে পুরনো/ক্রমের বাইরের update বাদ দেওয়া যায়। ভারী parsing Web Worker-এ সরানো যায়।

            **২. প্রতি message-এ React state না, একটা external store।** React-এর বাইরে vehicle id অনুযায়ী একটা normalised `Map` রাখো। আসা message buffer করো আর **coalesce** করো (প্রতি id-র শুধু সর্বশেষটা), তারপর প্রতি animation frame-এ (বা প্রতি ১০০–২৫০ ms-এ) সর্বোচ্চ একবার flush করো। এক flush = এক notification, প্রতি সেকেন্ডে ৫০টা `setState`-এর বদলে।

            **৩. বেছে বেছে subscription।** Component-গুলো প্রতি item-এর selector-সহ `useSyncExternalStore` দিয়ে store পড়ে, তাই vehicle 42 বদলালে শুধু vehicle 42 দেখানো row-টাই re-render হয়। Table virtualised, তাই একসাথে মাত্র ~৫০টা row subscribe করে।

            **৪. Chart আর alert নিজের গতিতে।** Chart library-র API দিয়ে imperatively, সীমিত হারে (২–৪ fps) chart update করো, আর history রাখো সীমিত ring buffer-এ। Alert store থেকে derive হয় আর duplicate বাদ দেওয়া হয়।

            **৫. Memory-র পরিচ্ছন্নতা।** প্রতিটা subscription, listener আর interval-এর cleanup আছে; state-এ সীমাহীন array নেই; লম্বা session ধরে heap snapshot দিয়ে যাচাই।

            **৬. Server-এর সহযোগিতা।** Delta পাঠানো, server-এ aggregate করা, আর client যেন শুধু দৃশ্যমান জিনিসে subscribe করে (viewport-ভিত্তিক subscription) — এতে traffic কমে।

            Trade-off: coalescing সামান্য freshness ছেড়ে অনেক CPU বাঁচায়; প্রতি item-এ immutable object change detection সস্তা করে, কিন্তু বেশি allocate করে।
        """,
        ex_en=r"""
            **Why the first version froze:** 50 `setState` calls per second, each copying a growing array, re-rendering a 2,000-row table and every chart. Garbage collection pauses plus long render tasks → frozen tab; the unbounded message array → memory growth.

            **Failure scenarios to design for**
            - **Background tabs:** browsers throttle timers and pause `requestAnimationFrame`. Because pending updates are coalesced per id, the buffer is bounded (≤ 2,000 entries) and one flush catches up when the tab returns (listen to `visibilitychange`).
            - **Reconnect storms** after a server restart → jittered backoff; request a fresh snapshot after reconnecting, then apply deltas newer than its sequence number.
            - **Slow devices:** adapt flush frequency, or show "live updates paused" while the user interacts with heavy views; user-triggered re-sorts go into `startTransition`.

            **Observability:** track long tasks, INP and JS heap size in RUM; use React Performance Tracks in a profiling build to confirm only changed rows render.
        """,
        ex_bn=r"""
            **প্রথম version কেন আটকে যেত:** প্রতি সেকেন্ডে ৫০টা `setState`, প্রতিবার একটা বাড়তে থাকা array copy করা, ২,০০০ row-এর table আর প্রতিটা chart re-render করা। Garbage collection-এর বিরতি আর লম্বা render task মিলে tab আটকে যায়; আর সীমাহীন message array-র কারণে memory বাড়ে।

            **যেসব failure scenario মাথায় রেখে design করতে হবে**
            - **Background tab:** browser timer ধীর করে দেয় আর `requestAnimationFrame` থামিয়ে রাখে। Pending update id অনুযায়ী coalesce হয় বলে buffer সীমিত থাকে (≤ ২,০০০ entry), আর tab ফিরে এলে এক flush-এই সব ধরে ফেলে (`visibilitychange` শোনো)।
            - Server restart-এর পর **reconnect-এর ঝড়** → jitter-সহ backoff; reconnect করার পর একটা নতুন snapshot নাও, তারপর তার sequence number-এর চেয়ে নতুন delta apply করো।
            - **ধীর device:** flush-এর হার মানিয়ে নাও, অথবা user ভারী view-তে কাজ করার সময় "live update থামানো আছে" দেখাও; user-এর চালানো re-sort `startTransition`-এ যায়।

            **Observability:** RUM-এ long task, INP আর JS heap size track করো; profiling build-এ React Performance Tracks দিয়ে নিশ্চিত হও যে শুধু বদলানো row-ই render হচ্ছে।
        """,
        tip_en=r"""Start by explaining *why* the naive version fails (render storm + unbounded memory), then present layers: connection → store → subscriptions → rendering → server. Ending with failure scenarios (background tabs, reconnects) is what distinguishes a senior answer.""",
        tip_bn=r"""আগে ব্যাখ্যা করো সাধারণ version *কেন* ব্যর্থ হয় (render-এর ঝড় + সীমাহীন memory), তারপর স্তরগুলো দেখাও: connection → store → subscription → rendering → server। শেষে failure scenario (background tab, reconnect) বললে উত্তরটা senior-level হয়ে ওঠে।""",
        mist_en=r"""Putting the socket inside a component effect without cleanup (duplicate connections), storing every message in a Context (whole app re-renders 50 times a second), or throttling with `setTimeout` per message instead of coalescing.""",
        mist_bn=r"""Cleanup ছাড়া component-এর effect-এর ভেতরে socket রাখা (duplicate connection), প্রতিটা message Context-এ রাখা (পুরো app প্রতি সেকেন্ডে ৫০ বার re-render), অথবা coalesce না করে প্রতি message-এ `setTimeout` দিয়ে throttle করা।""",
        code=r"""
            // vehicleStore.js — lives outside React
            const vehicles = new Map();   // id -> { lat, lng, status, seq }
            const listeners = new Set();
            let pending = new Map();
            let scheduled = false;

            export function receive(msg) {             // called by the WebSocket manager
              const known = pending.get(msg.id) ?? vehicles.get(msg.id);
              if (known && known.seq >= msg.seq) return; // drop stale / out-of-order
              pending.set(msg.id, msg);                  // coalesce: latest per id only
              if (!scheduled) {
                scheduled = true;
                requestAnimationFrame(flush);            // at most one flush per frame
              }
            }

            function flush() {
              scheduled = false;
              for (const [id, msg] of pending) {
                vehicles.set(id, { lat: msg.lat, lng: msg.lng, status: msg.status, seq: msg.seq });
              }
              pending = new Map();
              listeners.forEach((notify) => notify());
            }

            export function subscribe(listener) {
              listeners.add(listener);
              return () => listeners.delete(listener);
            }

            export const getVehicle = (id) => vehicles.get(id);

            // useVehicle.js
            import { memo, useSyncExternalStore } from 'react';
            import { getVehicle, subscribe } from './vehicleStore';

            export function useVehicle(id) {
              // re-renders only when this vehicle's object changes
              return useSyncExternalStore(subscribe, () => getVehicle(id));
            }

            export const VehicleRow = memo(function VehicleRow({ id }) {
              const v = useVehicle(id);
              if (!v) return null;
              return (
                <tr>
                  <td>{id}</td>
                  <td>{v.status}</td>
                  <td>{v.lat.toFixed(4)}, {v.lng.toFixed(4)}</td>
                </tr>
              );
            });
        """,
        lang="jsx",
        follow=[
            ("How would you guarantee the client doesn't miss updates during a reconnect?", "Reconnect-এর সময় client যাতে কোনো update মিস না করে, সেটা কীভাবে নিশ্চিত করবে?"),
            ("How would you detect and debug a memory leak that only appears after hours?", "যে memory leak কয়েক ঘণ্টা পর দেখা দেয়, সেটা কীভাবে ধরবে আর debug করবে?"),
            ("Would Server-Sent Events be a better fit than WebSockets here?", "এখানে কি WebSocket-এর চেয়ে Server-Sent Events বেশি উপযুক্ত হতো?"),
        ],
        related=["react-029", "react-026", "react-025"],
        refs=[R_USESES, R_MDN_WS, R_USEDEFERRED],
    ),
]

if __name__ == "__main__":
    save("react", "b4", QUESTIONS)
