# HTML content audit
Coverage: 32/32 questions reviewed — html-001, html-002, html-003, html-004, html-005, html-006, html-007, html-008, html-009, html-010, html-011, html-012, html-013, html-014, html-015, html-016, html-017, html-018, html-019, html-020, html-021, html-022, html-023, html-024, html-025, html-026, html-027, html-028, html-029, html-030, html-031, html-032.

## Category summary
This is a strong set. The technical accuracy is high, and every output and MCQ key I traced is correct (html-006, 007, 008, 009, 015, 021, 026, 028, 029). Answers go well beyond definitions. They give the mechanism, the trade-off and real production gotchas, for example the stale `returnValue` in html-014, `requestSubmit()` vs `submit()` in html-028, the `sizes` default of `100vw` in html-018 and the preload scanner in html-023. Version and Baseline claims match FACTS.md: popover (Jan 2025), invoker commands (Dec 2025), `<details name>`, `closedby` not Baseline and `fetchpriority`. The Trusted Types "Baseline Feb 2026" claim is not in FACTS, but I confirmed it online. Bangla is natural, contemporary and technically faithful, keeps terms in Latin script, and keeps the EN caveats almost without exception. I found no meaning drift.

The main weaknesses are few:
- A probable configuration bug in the Trusted Types CSP example (html-027).
- One overstated screen-reader claim about `role="alert"` (html-024).
- A slightly misleading performance rationale (html-019).
- Inconsistent `market` labels.
- The 8 MCQs have no follow-ups or related links.
- Some redundancy around LCP and `fetchpriority` (html-010/021/023/030).

Coverage of COVERAGE.md is complete. Small gaps are table semantics, `target="_blank"`/`rel`, iframe `sandbox`, and Web Components.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 9 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| HTML-C01 | html-027 | both | P2 | Technical correctness (code/config) | The CSP allowlists only `app-sanitizer`. DOMPurify tries to create its own Trusted Types policy named `dompurify`, and internally calls `DOMParser.parseFromString`, which is itself a Trusted Types sink. With `trusted-types app-sanitizer` and enforcement on, DOMPurify's policy creation is blocked. Its parse step then receives a plain string, so sanitizing can throw a TypeError. The "one reviewed place" design breaks exactly where it is meant to work. | Header: `require-trusted-types-for 'script'; trusted-types app-sanitizer;` with `createHTML: (dirty) => DOMPurify.sanitize(dirty)` | Allowlist both names (`trusted-types app-sanitizer dompurify`), or mention that DOMPurify needs its own policy name or `RETURN_TRUSTED_TYPE`. Add one sentence: "sanitizer libraries need their own policy name allowlisted". | Medium | In Chrome, serve the page with the header and call `renderComment` with HTML input. There should be no TypeError and no "policy dompurify could not be created" warning. |
| HTML-C02 | html-024 | both | P2 | Technical correctness (a11y) | The common-mistakes section lists "injecting a `role="alert"` element together with its text and expecting it to be announced" as a mistake. In practice `role="alert"` is the exception: most screen readers announce it even when it is inserted along with its content. Generic `aria-live`/`role="status"` regions are the ones that must already exist in the DOM. The explanation bullet about live regions is correct, but this mistake is overstated. | "or injecting a `role="alert"` element together with its text and expecting it to be announced." | Reword: "injecting an `aria-live`/`role="status"` region together with its text (it often isn't announced); `role="alert"` is more forgiving but still most reliable when the container already exists". | Medium | Test with NVDA+Chrome and VoiceOver+Safari: inject `<div role=alert>Error</div>`. It is announced. |
| HTML-C03 | html-019 | both | P3 | Misleading simplification (performance) | The answer says batching gives "one style/layout pass instead of one per row". Browsers already coalesce style and layout until the next frame or the next layout read. Appending in a loop without reading layout does not cause one layout per row. The real wins are fewer DOM mutations and a single atomic replace (no flash of half-rendered rows, one MutationObserver batch). | "which means one style/layout pass instead of one per row" | Say that it avoids repeated DOM mutations and gives an atomic swap. Layout is per frame unless you force it by reading layout inside the loop. | Medium-High | Profile a 1,000-row loop append in DevTools. There is a single Layout event, with no per-row layouts. |
| HTML-C04 | html-006, html-007, html-008, html-009, html-011, html-026, html-027, html-031, html-032 | meta | P3 | market label | These fundamentals are universal, but html-006/007/008/009/011 are labelled `bangladesh`. FACTS limits that label to BD-reported styles (MCQ/output tracing). html-011 is a code-review/debugging task, and filtering would hide these from international users. html-026 (an accessible-name MCQ) is labelled `international`, but it is not system design or scale, which is FACTS's criterion. | `html-011 \| … \| debugging \| market=bangladesh`; `html-026 \| … \| mcq \| market=international` | Use `both` for html-011 and html-026. Consider `both` for html-006 to html-009 too, since these fundamentals matter everywhere. | High | Labels follow the FACTS criteria. |
| HTML-C05 | html-003, html-004, html-008, html-009, html-015, html-021, html-026, html-028 | both | P3 | Weak/missing follow-ups | Every MCQ has empty follow-ups and related links. Interview drilling stops at the key. | `FOLLOW-UPS: []` / `RELATED: []` | Add 1–2 follow-ups each. Examples: html-015 "How do you anchor the popover to its button?"; html-028 "What is `event.submitter`?"; html-021 "When is preconnect the right hint?". | High | No MCQ has empty follow-ups. |
| HTML-C06 | html-011 | EN/BN | P3 | Code/label mismatch | The extra-code label says handlers are attached with `addEventListener`, but the fixed snippet contains no script. | "Fixed version (spacing moved to CSS, handlers attached with addEventListener)" | Add a 3-line delegated listener, or change the label to "handlers attached in JS (not shown)". | High | The label matches the snippet. |
| HTML-C07 | html-017 | both | P3 | Unsupported market claim / refs | "For Bangladeshi shops, where a lot of discovery happens through Facebook" is plausible (f-commerce) but unsourced. The refs cite the W3C JSON-LD spec instead of the schema.org/Product vocabulary actually used. | "For Bangladeshi shops, where a lot of discovery happens through Facebook, this is just as important as search." | Soften to "for shops that sell heavily through Facebook/Messenger". Swap or add a ref: `https://schema.org/Product`. | Medium | Claim softened and ref relevant. |
| HTML-C08 | html-024 | both | P3 | Vague authority claim | "This pattern is used by large public-sector design systems" names nobody. | "This pattern is used by large public-sector design systems because it tests well with real users" | Name it: the GOV.UK Design System "Error summary" component (`https://design-system.service.gov.uk/components/error-summary/`). | High | Concrete source named. |
| HTML-C09 | html-027 | both | P3 | Incomplete config | `report-to csp-endpoint` only works if a `Reporting-Endpoints` header defines `csp-endpoint`. The example omits it. | "report-to csp-endpoint" | Add `Reporting-Endpoints: csp-endpoint="https://…/csp"` in the extra block, or a one-line note. | High | Example shows both headers. |
| HTML-C10 | html-010, html-021, html-023, html-030 | both | P3 | Redundancy | "Don't lazy-load the LCP image, use `fetchpriority="high"`, use a real `<img>` not a CSS background" is repeated in four questions. Each is still useful, but the overlap is high. | html-010 "never on the LCP image"; html-021 "make the hero a real `<img fetchpriority="high">`"; html-023 "keep my LCP image in an `<img>` tag"; html-030 step 5 | Keep it in 010/030 and trim the repeats in 021 and 023 (or cross-reference via RELATED). | Medium | Less duplicated text. |
| HTML-C11 | html-003, html-004, html-008, html-009, html-015, html-021, html-026, html-028 | BN | P3 | Bangla polish | "প্রলোভনজনক ভুল উত্তর" ("most tempting wrong answer") is repeated in every MCQ. It is understandable but stiff. | "সবচেয়ে প্রলোভনজনক ভুল উত্তর হলো `<a href="#">`" | Vary it: "সবচেয়ে বেশি মানুষ যেটা বেছে নেয়" / "সবচেয়ে বিভ্রান্তিকর option" / "ফাঁদের উত্তর". | Medium | Phrase varies naturally. |

## Per-question notes
- html-001 — OK
- html-002 — OK (minor: the answer says `<html lang="en">` while the code uses `lang="bn"`; the text says "or bn", so acceptable)
- html-003 — issues: HTML-C05, HTML-C11; scores acc 10 / depth 9 / BN 9 / EN 9
- html-004 — issues: HTML-C05, HTML-C11; scores 10/9/9/9
- html-005 — OK
- html-006 — issues: HTML-C04; scores 10/9/9/9 (output verified by reasoning: `"421"`, `available`, `string`, attribute appended last)
- html-007 — issues: HTML-C04; scores 10/9/9/9 (dirty-value behaviour correct)
- html-008 — issues: HTML-C04, HTML-C05, HTML-C11; scores 10/9/9/9
- html-009 — issues: HTML-C04, HTML-C05, HTML-C11; scores 10/9/9/9
- html-010 — issues: HTML-C10; scores 10/9/9/9
- html-011 — issues: HTML-C04, HTML-C06; scores 10/9/9/9
- html-012 — OK
- html-013 — OK
- html-014 — OK
- html-015 — issues: HTML-C05, HTML-C11; scores 10/9/9/9
- html-016 — OK
- html-017 — issues: HTML-C07; scores 9/9/9/9
- html-018 — OK
- html-019 — issues: HTML-C03; scores 9/9/9/9
- html-020 — OK
- html-021 — issues: HTML-C05, HTML-C10, HTML-C11; scores 10/9/9/9
- html-022 — OK
- html-023 — issues: HTML-C10; scores 10/9/9/9
- html-024 — issues: HTML-C02, HTML-C08; scores 8/9/9/9
- html-025 — OK
- html-026 — issues: HTML-C04, HTML-C05, HTML-C11; scores 10/9/9/9
- html-027 — issues: HTML-C01, HTML-C04, HTML-C09; scores 7/9/9/9
- html-028 — issues: HTML-C05, HTML-C11; scores 10/9/9/9
- html-029 — OK (expected output correct per the HTML parsing algorithm: p closed by div, empty `<p>` for stray `</p>`, implicit tbody in "in table" context)
- html-030 — issues: HTML-C10; scores 9/10/9/9
- html-031 — issues: HTML-C04; scores 9/10/9/9
- html-032 — issues: HTML-C04; scores 10/10/9/9

## Coverage & gaps
- Every COVERAGE.md subtopic is covered: semantic HTML, document structure, forms/validation (4 questions), accessibility (6), attributes, `data-*`, SEO/meta, script loading, parsing, DOM, HTML APIs (dialog, popover, invoker commands, details, template), common mistakes and scenarios. Difficulty mix is 11/11/7/3 and on target.
- Real gaps worth adding:
  1. Accessible data tables (`<caption>`, `<th scope>`, when not to use tables for layout). This is a common junior question.
  2. Link security and behaviour: `target="_blank"` with `rel="noopener noreferrer"` (and that modern browsers imply `noopener`), plus `<iframe sandbox>`/`allow`.
  3. Optionally, Web Components (custom elements, shadow DOM, declarative shadow DOM). This is not in COVERAGE but is common in international interviews.
- Redundancy: LCP image guidance appears 4× (HTML-C10). Forms/validation in html-013, html-024 and html-028 overlap a little but each tests something distinct.
- Cross-tech overlap with CSS: html-032 and css-031 both teach `content-visibility` and large-DOM performance; html-030 font loading overlaps css-032. This is acceptable but should be cross-linked.
- Difficulty labels look right. html-026 (accessible-name precedence MCQ) is arguably medium rather than hard.

## Needs verification
- html-014 / html-016: "invoker commands … Baseline newly available since December 2025". This matches FACTS; I did not verify it independently.
- html-015: "Popover has been Baseline newly available since January 2025". This matches FACTS.
- html-027: "React 19.3 added Trusted Types support". This matches FACTS and is after my training cutoff.
- html-032: "`content-visibility` … Baseline newly available". This matches FACTS.

## Verified
- WebSearch "Trusted Types Baseline newly available 2026 Firefox": the web.dev February 2026 Baseline digest (https://web.dev/blog/baseline-digest-feb-2026) and MDN (https://developer.mozilla.org/en-US/docs/Web/API/trustedTypes) both say it has been available across browsers since February 2026. This confirms the html-027 claim.
- `node -e "new Intl.NumberFormat('en-BD',{style:'currency',currency:'BDT'}).format(1850)"` gives `BDT 1,850.00`. The html-019 currency formatting is valid.
- MCQ keys and outputs were traced by hand against the spec rules: html-006, html-007, html-008, html-009, html-015, html-021, html-026, html-028, html-029. All are correct.
- The DOMPurify/Trusted Types interaction (HTML-C01) comes from my knowledge of DOMPurify's built-in `dompurify` policy and the TT sink list. I did not execute it, so confidence is Medium.
