# CSS content audit
Coverage: 32/32 questions reviewed — css-001, css-002, css-003, css-004, css-005, css-006, css-007, css-008, css-009, css-010, css-011, css-012, css-013, css-014, css-015, css-016, css-017, css-018, css-019, css-020, css-021, css-022, css-023, css-024, css-025, css-026, css-027, css-028, css-029, css-030, css-031, css-032.

## Category summary
This is a high-quality category. Every output and MCQ key I checked is correct: the box-model arithmetic, specificity tuples (css-002, css-023), layer ordering (css-012), the auto-fill/auto-fit maths (238px vs 492px) and the `clamp()` slope/intercept (css-021). The material is current: cascade layers, `:has()`, container size and style queries, subgrid, `@property`, `@scope`, `@starting-style`, `light-dark()`, and Baseline buckets consistent with FACTS.md. The debugging questions (css-014 `min-width: auto`, css-020 sticky, css-027 horizontal overflow) are realistic and give root causes, not symptoms. The Bangla-specific typography advice (line-height, no letter-spacing, `unicode-range`) adds real value for the target audience. Bangla is natural and faithful to the EN.

Weaknesses:
- The anchor-positioning status in FACTS and css-028 may now be stale (Firefox 147 shipped it in Jan 2026).
- A few mechanism-level imprecisions: the registered-property "discarded" wording, the z-index fix in css-019, and the `62.5%` claim in css-021.
- `market` labels are inconsistent.
- The 7 MCQs have no follow-ups, and one MCQ has a duplicated distractor.
- The `min-width: auto` and compositor/`will-change` topics are repeated 3× each.
- Classic junior topics are missing: `display` block/inline/inline-block, centering, and units (rem/em/%/vh/dvh).

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 9 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| CSS-C01 | css-028 (and FACTS.md Baseline list) | both | P2 | Version currency | Anchor positioning is taught as "limited availability, not Baseline". Caniuse and several sources report Firefox 147 (Jan 2026) shipping it unflagged; Chrome 125+ and Safari 26 already had it. The core feature may now be Baseline newly available, with the group status possibly still "limited" for newer sub-features (`position-visibility`, `anchor-size()`). The question presents itself as authoritative "It's October 2026" content, so a stale status here is costly. | "Enhancement: anchor positioning (limited availability, not Baseline)"; "**anchor positioning**, **scroll-driven animations** … not Baseline yet" | Check web-features/webstatus.dev for the current status. If it is newly available, move it to the "Newly available" bucket and keep the `@supports` fallback advice. If the group is still limited, say "core anchoring works in all engines since early 2026, but the feature group is still flagged limited". | Medium | webstatus.dev/features/anchor-positioning shows the status, and the text matches it. |
| CSS-C02 | css-009, css-026 | both | P3 | Mechanism imprecision | Registered custom properties are **not** syntax-checked at parse time. A value that doesn't match `syntax` makes the custom property invalid at computed-value time, so it takes its inherited value (`inherits: true`) or `initial-value`. The stated outcome is right, but "the declaration itself would be discarded" describes parse-time dropping. That would differ if an earlier lower-priority declaration existed. | css-009: "the bad declaration itself would be discarded"; css-026: "An invalid value … is discarded for the registered property" | Say "the custom property becomes invalid at computed-value time and falls back to its inherited/initial value (the declaration still wins the cascade)". | Medium | Matches the CSS Properties & Values API L1 computed-value-time rule. |
| CSS-C03 | css-019 | both | P3 | Incomplete fix / precision | `z-index` applies only to positioned elements or flex/grid items. A header that has a stacking context only because of `transform`/`opacity` ignores `z-index` unless it is also positioned. The scenario also needs the hero to be positioned or to create a stacking context; a non-positioned hero would paint *below* the header's stacking context. | "Fix it by giving the header a `z-index` higher than the hero" | "Give the header `position: relative` (or sticky) plus a `z-index` higher than the hero's stacking context". Note that the hero must be positioned or stacked for the bug to appear. | Medium-High | Reproduce in a sandbox: header `transform` + `z-index: 10` without `position` has no effect. |
| CSS-C04 | css-021 | both | P3 | Inaccurate claim | `html { font-size: 62.5% }` is relative to the user's default, so it does **not** override the user's preferred size. Its real downsides are elsewhere: body text must be reset, third-party rem-sized components shrink, and it causes confusion. | "it overrides the user's preferred base size in a fragile way" | "It still scales with user settings, but it shrinks every third-party `rem` value and forces you to reset body text; just do the maths at 16px". | Medium | Set browser default font 20px: 62.5% gives 12.5px, which scales. |
| CSS-C05 | css-022 | both | P3 | Misleading history | The explanation implies `.sidebar &` (option D) used to be invalid. Even the first-shipped nesting rules (Chrome 112 / Safari 16.5) allowed any nested selector that contained `&` or began with a symbol. The old restriction was on selectors starting with an identifier, such as `div &`/`p {}`. | "The tempting wrong answer is D, because older docs and early browser implementations had stricter rules." | Reword: "early implementations rejected nested selectors starting with a type selector (e.g. `p { }`) unless written `& p`; `&` at the end was always valid". | Medium | Compare with the 2023 nesting spec history. |
| CSS-C06 | css-002 | both | P3 | MCQ distractor quality | Options B and D both answer "Green". Two options give the same colour, which weakens the four-way choice. | "OPTION B: Green" / "OPTION D: Green, because it has two classes and appears after `#main p`" | Replace D with a distinct plausible wrong answer, e.g. "Blue — `p.text` is last in source order". | High | Four distinct answers. |
| CSS-C07 | css-008 | both | P3 | Overgeneralisation | "`::before`/`::after` don't render on replaced or void elements like `<img>` and `<input>`". Chromium and WebKit do render them on checkbox/radio inputs, and on `<img>` when the image fails to load. | "don't render on **replaced or void elements** like `<img>` and `<input>`" | "generally aren't rendered (or are inconsistent across browsers) on replaced elements such as `<img>`, `<input>`" | Medium | Test `input[type=checkbox]::before` in Chrome: it renders. |
| CSS-C08 | css-017 | code | P3 | Code labelling | Sass syntax (`$bp-tablet`, `min-width: $bp-tablet`) sits inside a block labelled `css`. Learners may copy it into a `.css` file. | `/* Sass (compile-time) … */ $bp-tablet: 48rem;` in `CODE (css)` | Move the Sass part to an `extra` block with `lang="scss"`, or note "SCSS". | High | Code block languages are correct. |
| CSS-C09 | css-001, css-002, css-004, css-005, css-007, css-008, css-026, css-030, css-031 | meta/both | P3 | market label / unsupported claim | Universal fundamentals (box model, specificity, position, flex, media queries, pseudo-elements) are labelled `bangladesh`. css-026 (`@property`) is `international`, which doesn't match FACTS's system-design criterion. css-031 is `international` but says "the devices most of your BD customers use". css-007 asserts "In Bangladesh most traffic is on phones" without a source. | css-031: "unusable on the devices most of your BD customers use"; css-007: "In Bangladesh most traffic is on phones" | Use `both` for fundamentals and for css-026. Make css-031 market-neutral ("your mobile-heavy audience") or set it to `both`. Soften or cite the css-007 statistic (e.g. "mobile-heavy markets like Bangladesh"). | High | Labels follow the FACTS criteria. |
| CSS-C10 | css-013 | meta | P3 | Version label | `ver` says ":has() Baseline widely available (since Dec 2023)". Dec 2023 is when it became *newly* available; widely available came about 30 months later. | "ver=CSS Selectors Level 4; :has() Baseline widely available (since Dec 2023)" | "Baseline newly available Dec 2023; widely available 2026". | High | Label is accurate. |
| CSS-C11 | css-002, css-005, css-008, css-011, css-019, css-022, css-023 | both | P3 | Weak/missing follow-ups | Every MCQ has empty follow-ups and related links. | `FOLLOW-UPS: []` | Add 1–2 each. Examples: css-019 "How would `isolation: isolate` help here?"; css-023 "How would you rewrite these rules with `@layer` instead of `:not(#x)`?". | High | No empty follow-ups. |
| CSS-C12 | css-005, css-014, css-027; css-018, css-024, css-031 | both | P3 | Redundancy | `min-width: auto` / `minmax(0,1fr)` is explained in full three times. Compositor-only properties and `will-change` misuse are explained in full three times. | css-005 "add `min-width: 0`"; css-014 root cause; css-027 "flex/grid items stuck at `min-width: auto`"; css-024/css-031 will-change bullets | Keep the deep treatment in css-014 and css-024. Shorten the others to a cross-reference. | Medium | Less duplicated text. |
| CSS-C13 | css-002, css-005, css-008, css-011, css-019, css-022, css-023 | BN | P3 | Bangla polish | "প্রলোভনজনক (ভুল) উত্তর" is repeated in every MCQ explanation and reads stiffly. | "প্রলোভনজনক উত্তর সবুজ" | Vary it: "ফাঁদের উত্তর", "বেশিরভাগ মানুষ যেটা বেছে নেয়". | Medium | Natural variation. |

## Per-question notes
- css-001 — issues: CSS-C09; scores acc 10 / depth 9 / BN 9 / EN 9 (250px / 200px / 150px / 10px verified)
- css-002 — issues: CSS-C06, CSS-C09, CSS-C11, CSS-C13; scores 10/8/9/9
- css-003 — OK
- css-004 — issues: CSS-C09; scores 10/9/9/9
- css-005 — issues: CSS-C09, CSS-C11, CSS-C12, CSS-C13; scores 10/9/9/9
- css-006 — OK
- css-007 — issues: CSS-C09; scores 10/9/9/9
- css-008 — issues: CSS-C07, CSS-C09, CSS-C11, CSS-C13; scores 9/9/9/9
- css-009 — issues: CSS-C02; scores 9/10/9/9
- css-010 — OK
- css-011 — issues: CSS-C11, CSS-C13; scores 10/9/9/9
- css-012 — OK (gray / green verified)
- css-013 — issues: CSS-C10; scores 10/10/9/9
- css-014 — OK
- css-015 — OK (238px / 492px verified)
- css-016 — OK
- css-017 — issues: CSS-C08; scores 10/9/9/9
- css-018 — issues: CSS-C12 (minor); scores 10/9/9/9
- css-019 — issues: CSS-C03, CSS-C11, CSS-C13; scores 9/9/9/9
- css-020 — OK
- css-021 — issues: CSS-C04; scores 9/10/9/9 (clamp maths verified)
- css-022 — issues: CSS-C05, CSS-C11, CSS-C13; scores 9/9/9/9
- css-023 — issues: CSS-C11, CSS-C13; scores 10/9/9/9 ((0,2,0) / (1,1,1) / (1,1,0) / (0,2,2), green verified)
- css-024 — OK
- css-025 — OK
- css-026 — issues: CSS-C02, CSS-C09; scores 9/10/9/9
- css-027 — issues: CSS-C12 (minor); scores 10/10/9/9
- css-028 — issues: CSS-C01; scores 8/9/9/9
- css-029 — OK
- css-030 — issues: CSS-C09 (label only; `international` is acceptable here); scores 10/10/9/9
- css-031 — issues: CSS-C09, CSS-C12; scores 10/10/9/9
- css-032 — OK

## Coverage & gaps
- Every COVERAGE.md subtopic is present: box model, specificity/inheritance, cascade + `@layer`, stacking contexts, positioning, Flexbox, Grid + subgrid, responsive, media and container queries, `:has`/`:is`/`:where`, custom properties, transitions/animations, accessibility (reduced motion, focus-visible, contrast), performance (reflow/repaint/compositing/`content-visibility`), layout debugging, scenarios, and modern features with Baseline. Difficulty mix is 11/11/7/3, with 7 MCQs.
- Real gaps for junior candidates (common in BD written and viva rounds as well as international screens):
  1. `display: block` vs `inline` vs `inline-block` (and why width doesn't apply to inline).
  2. "How do you centre an element horizontally and vertically?" (flex, grid `place-items`, absolute + transform).
  3. CSS units: `px`/`em`/`rem`/`%`/`vw`/`vh` vs `dvh`/`svh`, and when to use which.
  4. Optionally, logical properties and RTL, and colour functions (`oklch()`, `color-mix()`), which are mentioned only in passing.
- Redundancy: see CSS-C12. css-020 and css-027 overlap on `overflow: clip` vs `hidden` (acceptable).
- Cross-tech overlap with HTML: css-031 vs html-032 (`content-visibility`, big lists), css-032 vs html-030 (Bangla fonts, preload), css-018 vs html-014 (dialog animation follow-up).
- Difficulty labels look appropriate.

## Needs verification
- css-028 and FACTS: the anchor positioning "not Baseline" claim (see CSS-C01; evidence conflicts).
- css-016 and css-028: "container style queries Baseline newly available (May 2026)" (matches FACTS, not independently verified).
- css-028 and css-030: "`@scope` Baseline newly available (March 2026)" (matches FACTS).
- css-028: "same-document View Transitions … (October 2025)" (matches FACTS).
- css-018 and css-028: "scroll-driven animations not Baseline" (matches FACTS; not verified).
- css-021: "`text-wrap: balance` Baseline newly available"; css-030: "`light-dark()` newly available" (both match FACTS).

## Verified
- WebSearch "CSS anchor positioning Baseline status 2026 Firefox support": the caniuse entry (https://caniuse.com/css-anchor-positioning) lists Firefox 147+ as supported (145–146 behind a flag). Secondary sources (https://www.oddbird.net/tags/anchor-positioning/, https://www.buildmvpfast.com/blog/css-anchor-positioning-baseline-delete-floating-ui-2026) say Firefox 147 (Jan 2026) made the core feature Baseline. One source notes that the web-platform-status group may still read "limited". WebFetch of webstatus.dev and of the MDN anchor positioning page did not return a readable Baseline banner, so this is unresolved and listed as CSS-C01 at Medium confidence.
- Arithmetic re-checked by hand:
  - css-001: 200+40+10 = 250; 200−50 = 150.
  - css-015: 4×200+3×16 = 848 ≤ 1000, and (1000−48)/4 = 238. Five columns need 1064 > 1000. (1000−16)/2 = 492.
  - css-021: 16/840 = 0.019048, giving 1.9048vw. 24 − 6.857 = 17.143px = 1.0714rem.
- Specificity, cascade and layer outcomes were traced by hand: css-002, css-003, css-009, css-012, css-023. All are correct.
