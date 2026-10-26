# React content audit
Coverage: react-001, react-002, react-003, react-004, react-005, react-006, react-007, react-008, react-009, react-010, react-011, react-012, react-013, react-014, react-015, react-016, react-017, react-018, react-019, react-020, react-021, react-022, react-023, react-024, react-025, react-026, react-027, react-028, react-029, react-030, react-031, react-032. **32 of 32 reviewed.**

Distribution: easy 11 (001–011), medium 11 (012–022), hard 7 (023–029), extreme 3 (030–032). This is on target. There are 8 MCQs (004, 006, 009, 010, 019, 022, 023, 028).

## Category summary
This is a strong category. The answers are technically accurate, current to React 19.x, and written the way an experienced interviewer would want to hear them.

- **Output and debugging questions are correct.** I traced react-003, 012, 013, 021 and 023 by hand. The MCQs each have exactly one defensible key. None of the shown code leaks the answer.
- **Version claims hold up.** The claims that could be checked (19.2 `<Activity>`/`useEffectEvent`; 19.3 `<ViewTransition>`, Fragment refs, `browser()`, Server Components rendering `<Context value>`, independent Transitions) match FACTS.md and the React 19.3 blog post, which I fetched.
- **Strengths:**
  - Every answer has a clear mechanism ("snapshot / queue / batching", "type + position", "Object.is").
  - Production angles appear throughout: INP, Performance Tracks, chunk-load failures and virtualisation trade-offs.
  - Legacy APIs are labelled consistently (forwardRef, class lifecycles, CRA).
  - Senior questions (030–032) are realistic architecture problems, not trivia.
- **Weaknesses:**
  - There is no React security question. 029 is the only `security-performance` item, and it is pure performance.
  - `useReducer` is missing.
  - The headline 19.3 features (Fragment refs, `browser()`) appear only as side notes in an MCQ explanation.
  - All 8 MCQs have empty follow-ups.
  - There is some redundancy (index keys twice; `useEffectEvent` twice).
- **Bangla:** natural, contemporary developer Bangla, with tech terms kept in Latin script and the same caveats as the EN. Minor issues: the literal "লোভনীয়" for "tempting" recurs, there are a few calques ("সাধারণ অপরাধী", "পরিবহনের মাধ্যম"), and Bangla and Latin numerals are mixed.
- **Labels:** a couple of `market` labels are unjustified.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8 | English quality 9 | Examples & code 9 | Originality/information value 8 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| REACT-C01 | react-029 (category-level) | both | P2 | Coverage gap | No React security question. COVERAGE lists accessibility and production debugging, and AUTHORING asks for a security-performance item. The only one (029) is about performance; security gets a single line ("never ship 10,000 rows… filter on the server"). XSS via `dangerouslySetInnerHTML`, `javascript:` URLs in `href`, sanitising CMS HTML, and keeping React/RSC patched after the Dec-2025 RSC CVEs (FACTS) are never taught. | 029 EXPLANATION: "Security/perf angle: never ship 10,000 rows of data the user isn't allowed to see" | Add one medium/hard security question: a `dangerouslySetInnerHTML` + `href={userUrl}` debugging task with a DOMPurify/URL-allowlist fix, plus a note on RSC patching (react-dom 19.x security releases). | High | The category contains a question whose answer covers sanitisation, `javascript:` URL blocking and dependency patching. |
| REACT-C02 | react-007 | both | P3 | Accuracy (simplification) | Says error boundaries are "the one" lifecycle feature with no hook equivalent. `getSnapshotBeforeUpdate` also has none (react.dev: "There are no Hook equivalents for getSnapshotBeforeUpdate, getDerivedStateFromError and componentDidCatch"). The mapping "`componentDidUpdate` ≈ effect with dependencies" also omits that the effect runs on mount too. | "Error boundaries are the one lifecycle feature hooks don't replace" / BN "Error boundary হলো একমাত্র lifecycle feature যেটা hook দিয়ে replace হয়নি" | "Error boundaries (and the rarely used `getSnapshotBeforeUpdate`) have no hook equivalent." Add "(it also runs after mount)" to the componentDidUpdate mapping. | High | Text no longer says "the one". |
| REACT-C03 | react-031 | both (code) | P3 | Code/version accuracy | The code comment labels the `createRoot` example "React 18.3 / 19", but `onUncaughtError`/`onCaughtError` root options exist only in React 19. Copying it on 18.3 silently ignores them. | `// After (React 18.3 / 19)` followed by `createRoot(..., { onUncaughtError ..., onCaughtError ... })` | Split it: `createRoot(el).render(<App/>)` for 18.3, and add the error options under a "React 19+" comment. | High | Comment matches API availability. |
| REACT-C04 | react-030 | code | P3 | Accessibility in example | `TabPanel` returns `null` for inactive tabs, but every `TabTrigger` sets `aria-controls` to that panel's id. Inactive triggers therefore reference non-existent elements. For an answer that stresses "accessible by default", this is a flaw. | `if (current !== value) return null;` together with `aria-controls={`${baseId}-panel-${value}`}` | Render inactive panels with `hidden` (or set `aria-controls` only when the panel is mounted). Also add `tabIndex={0}` on the panel per the WAI-ARIA tabs pattern. | Medium | All `aria-controls` ids resolve in the DOM. |
| REACT-C05 | react-029 | code | P3 | Accessibility in example | The explanation recommends `aria-rowcount`/`aria-rowindex`, but the example renders plain `<div>`s with no `role="table"/"grid"`/`"row"`. Those attributes do nothing without table/grid roles. | `<div ref={scrollRef} ...>` … `<div key={order.id} style={{ position: 'absolute' …}}>` | Add `role="table"` (or `grid`) + `aria-rowcount={rows.length}` on the container, and `role="row"` + `aria-rowindex={item.index + 2}` on rows, or mention it explicitly. | Medium | Example markup has roles that support the ARIA attributes it recommends. |
| REACT-C06 | react-004, 006, 009, 010, 019, 022, 023, 028 | both | P3 | Question quality | Every MCQ has empty follow-ups. AUTHORING asks for 1–3 per question, and the MCQs are good jumping-off points (e.g. 023 → "how would you force a reset?"). | `FOLLOW-UPS: []` (all eight) | Add 1–2 follow-ups each, e.g. 010: "How do you recover from a chunk-load error after a deploy?"; 019: "How would you report caught errors to monitoring?" | High | No question has empty follow-ups. |
| REACT-C07 | react-004 / react-021; react-012 / react-027; react-008 / react-025 | both | P3 | Redundancy | Near-duplicate knowledge. 004 (MCQ) and 021 (debugging) both test index-as-key with the same input-state bug. 012's fix and 027 both teach `useEffectEvent` with the same "non-reactive logic" framing. 008's re-render explanation is repeated in 025. | 004: "an input's text … 'jumps' to a different row"; 021: "keeps the first `<li>` and its DOM input (with "urgent")" | Keep 021 (richer). Change 004 to a different key concept (e.g. using `key` to reset state, or keys on Fragments). The others are acceptable as progression. | Medium | No two questions share the same primary learning objective. |
| REACT-C08 | react-001…032 (category) | both | P3 | Coverage gap | Missing or thin: `useReducer` (absent); `use()` with promises / Suspense data fetching (only an MCQ distractor in 022); 19.3 Fragment refs and `browser()` (only one bullet each in 028's explanation, although COVERAGE lists them); `useLayoutEffect`, portals and `useImperativeHandle` (only follow-ups or mentions). | 028: "Other React 19.3 additions worth knowing: Fragment refs… `browser()`…" | Add a medium question on `useReducer` vs `useState` (or fold it into 017). Add one item where `use(promise)` + Suspense is the main answer. Consider replacing the 004 duplicate with a Fragment-ref/`browser()` question. | Medium | COVERAGE subtopics each have a primary question. |
| REACT-C09 | react-017, react-021, react-028 | n/a | P3 | Labels | `market=bangladesh` on 017 (Redux Toolkit conceptual) and 021 (debugging) is not justified by FACTS guidance (BD = MCQ/output-tracing fundamentals, viva definitions). Redux is equally common internationally. 028 is a narrow API MCQ labelled `international` with prio low, but FACTS reserves `international` for system-design/scale questions. | `react-017 … market=bangladesh`; `react-028 … market=international prio=low` | Set all three to `both`. | Medium | Labels follow the FACTS research-note rule. |
| REACT-C10 | react-004, 006, 009, 010, 019, 022, 023, 028 (also 024 mistakes) | BN | P3 | Bangla naturalness | "লোভনীয়" ("appetising/tempting") is a literal calque for "the tempting wrong answer". A BD developer would say "যে ভুল উত্তরটা সবচেয়ে বেশি মনে আসে" or "সবচেয়ে বিভ্রান্তিকর option". | "সবচেয়ে লোভনীয় ভুল উত্তর হলো **index**"; "লোভনীয় উত্তর হলো `forwardRef`" | Replace with "সবচেয়ে বিভ্রান্তিকর (ভুল) উত্তর" / "অনেকেই ভুল করে যে উত্তরটা দেয়". | Medium | Phrase no longer appears. |
| REACT-C11 | react-026, react-008, react-006 | BN | P3 | Bangla naturalness | Calques: "সাধারণ অপরাধী" for "typical culprits"; "Context হলো পরিবহনের মাধ্যম" for "transport"; "render-এর পর render টিকে থাকে" (awkward). | "**সাধারণ অপরাধী:**"; "Context হলো পরিবহনের মাধ্যম, state management না।" | "সাধারণ কারণগুলো:"; "Context শুধু value পৌঁছে দেওয়ার উপায়, state management না"; "একাধিক render জুড়ে value টিকে থাকে". | Medium | Re-read by a BD reviewer. |
| REACT-C12 | react-024, 029, 032 | BN | P3 | Consistency | Numerals are mixed within the same answers: Bangla digits for some values ("৫,০০০", "১০,০০০", "~৩০–৫০", "২০০ ms") and Latin digits for others ("4–6x", "INP"). | 029 BN: "১০,০০০ row × ৮টা cell" vs 026 BN "4–6x CPU throttling" | Pick one convention for numbers next to units and tech terms (Latin digits are more common in BD tech writing) and apply it bank-wide. | Medium | Style guide decision applied. |
| REACT-C13 | react-017, react-020, react-029 | n/a | P3 | References | The refs use GitHub repos rather than the official docs sites, and 017 adds a tangential `useSyncExternalStore` link. Query priority (020) is documented at testing-library.com. | 017: "Redux Toolkit (GitHub, official)", "react.dev — useSyncExternalStore"; 020: "React Testing Library (GitHub)" | 017 → https://redux-toolkit.js.org/introduction/getting-started (+ redux.js.org usage page); 020 → https://testing-library.com/docs/queries/about (priority); 029 → https://tanstack.com/virtual/latest. | Medium | Refs point to the canonical docs pages. |

## Per-question notes
- react-001 — OK (jsx/jsxs output correct; `0 &&` gotcha good)
- react-002 — OK
- react-003 — OK (traced: render 0 / clicked 0 / render 2, button 2; StrictMode/prod caveat stated)
- react-004 — issues: REACT-C06, C07, C10; scores acc 10 / depth 8 / BN 8 / EN 9
- react-005 — OK (auto-reset of uncontrolled fields after a successful Action is correct)
- react-006 — issues: REACT-C06, C10, C11; scores acc 10 / depth 8 / BN 8 / EN 9
- react-007 — issues: REACT-C02; scores acc 8 / depth 9 / BN 9 / EN 9
- react-008 — issues: REACT-C11 (minor); scores acc 10 / depth 9 / BN 8 / EN 9 (19.3 `<Context value>` claim verified against the 19.3 blog)
- react-009 — issues: REACT-C06, C10; scores acc 10 / depth 8 / BN 8 / EN 9
- react-010 — issues: REACT-C06, C10; scores acc 10 / depth 9 / BN 8 / EN 9
- react-011 — OK
- react-012 — OK (traced: three "tick 0" lines, screen 1)
- react-013 — OK (StrictMode order correct; React 19 dims rather than suppresses the second log — correct)
- react-014 — OK
- react-015 — OK (URL-tagged result + AbortController correctly prevents stale data)
- react-016 — OK
- react-017 — issues: REACT-C09, C13; scores acc 9 / depth 9 / BN 9 / EN 9
- react-018 — OK
- react-019 — issues: REACT-C06, C10; scores acc 10 / depth 9 / BN 8 / EN 9
- react-020 — issues: REACT-C13; scores acc 10 / depth 9 / BN 9 / EN 9
- react-021 — issues: REACT-C07, C09; scores acc 10 / depth 9 / BN 9 / EN 9
- react-022 — issues: REACT-C06, C10; scores acc 10 / depth 9 / BN 8 / EN 9
- react-023 — issues: REACT-C06, C10; scores acc 10 / depth 9 / BN 8 / EN 9
- react-024 — issues: REACT-C12 (minor); scores acc 10 / depth 10 / BN 8 / EN 9
- react-025 — OK
- react-026 — issues: REACT-C11, C12; scores acc 9 / depth 10 / BN 8 / EN 9
- react-027 — issues: REACT-C07 (overlap with 012); scores acc 10 / depth 9 / BN 9 / EN 9
- react-028 — issues: REACT-C06, C09, C10; scores acc 10 / depth 9 / BN 8 / EN 9 (key verified against the React 19.3 blog: only Transition / useDeferredValue / Suspense reveal activate ViewTransition)
- react-029 — issues: REACT-C01, C05, C12, C13; scores acc 9 / depth 9 / BN 8 / EN 9
- react-030 — issues: REACT-C04; scores acc 9 / depth 10 / BN 9 / EN 9
- react-031 — issues: REACT-C03; scores acc 9 / depth 10 / BN 9 / EN 9
- react-032 — issues: REACT-C12 (minor); scores acc 10 / depth 10 / BN 9 / EN 9

## Coverage & gaps
- **Covered well:** JSX, props/state, useState, useEffect/cleanup, useRef, memo/useMemo/useCallback, Context (+ performance), custom hooks, keys, controlled/uncontrolled inputs, Actions/useActionState/useFormStatus/useOptimistic, RTK, error boundaries, Suspense/lazy, RSC boundary, stale closures, reconciliation, concurrency, 19.2/19.3 features, React Compiler, RTL, a11y, production debugging, virtualisation, architecture.
- **Real gaps:** a React security question (REACT-C01); `useReducer`; `use(promise)` as a primary topic; Fragment refs and `browser()` as primary topics (COVERAGE lists them explicitly); `useLayoutEffect` vs `useEffect` (only a follow-up); portals; SSR/hydration from the React side (only in nextjs).
- **Redundant pairs:** 004/021 (index keys); 012/027 (useEffectEvent); 008/025 (context re-renders — acceptable as easy → hard progression).
- **Cross-tech overlap with nextjs:** react-022 vs next-004 (the 'use client' boundary and serialisable props); react-008 vs next-021 (identical 19.3 `<Context value>` paragraph); react-017 vs next-021/031 (store per request). Acceptable, but the identical wording could be varied.
- **Difficulty labels:** appropriate throughout. 023 (hard MCQ on type+position state preservation) is arguably medium, but it is a common trap, so hard is defensible.

## Needs verification
- react-014 / react-031: "The `eslint-plugin-react-hooks` recommended preset includes compiler-powered rules"; `compilationMode: 'annotation'` with `"use memo"`; codemods `npx codemod@latest react/19/migration-recipe` and `npx types-react-codemod@latest preset-19`. These are consistent with my knowledge of the Oct-2025 docs; I did not re-check them live.
- react-026: "In a profiling build only the Scheduler tracks are on by default, and the Components track covers subtrees wrapped in `<Profiler>` (or all components if React DevTools is installed)". This matches my memory of the 19.2 docs (Medium confidence).
- react-024: "`useDeferredValue(value, initialValue)`" (React 19.0). This is believed correct.
- react-009: "React plans to deprecate [forwardRef]". This matches the React 19 blog wording ("In future versions we will deprecate and remove forwardRef").

## Verified
- WebFetch https://react.dev/blog/2026/09/09/react-19-3: the page exists (used as a ref in 028). It confirms:
  - `<ViewTransition>` is stable in 19.3.
  - Only Transition updates, Suspense reveals and `useDeferredValue` updates animate it.
  - The FragmentInstance methods are `addEventListener`, `focus`, `focusLast`, `observeUsing`, `getClientRects`, etc.
  - `use(browser())` suspends on the server only.
  - Server Components can render `<Context value>` imported from a `'use client'` module.
  - "Render Transitions independently … a slow Transition no longer holds up unrelated ones".
  - This supports react-008, 024, 028 and next-017/021.
- Hand-traced output questions react-003, 012, 013, 021 and 023: all expected outputs are correct.
