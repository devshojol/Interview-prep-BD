import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_FOCUS_VISIBLE = ("MDN — :focus-visible", "https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible")
WCAG_FOCUS_VISIBLE = ("W3C WAI — Understanding SC 2.4.7 Focus Visible", "https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html")
WCAG_CONTRAST = ("W3C WAI — Understanding SC 1.4.3 Contrast (Minimum)", "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html")
WCAG_NON_TEXT_CONTRAST = ("W3C WAI — Understanding SC 1.4.11 Non-text Contrast", "https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html")
MDN_POSITION = ("MDN — position (sticky)", "https://developer.mozilla.org/en-US/docs/Web/CSS/position")
MDN_OVERFLOW = ("MDN — overflow (clip vs hidden)", "https://developer.mozilla.org/en-US/docs/Web/CSS/overflow")
MDN_CLAMP = ("MDN — clamp()", "https://developer.mozilla.org/en-US/docs/Web/CSS/clamp")
WEBDEV_TYPOGRAPHY = ("web.dev — Learn Responsive Design: Typography", "https://web.dev/learn/design/typography")
WCAG_RESIZE_TEXT = ("W3C WAI — Understanding SC 1.4.4 Resize Text", "https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html")
MDN_NESTING = ("MDN — Using CSS nesting", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting/Using_CSS_nesting")
MDN_NESTING_SELECTOR = ("MDN — & nesting selector", "https://developer.mozilla.org/en-US/docs/Web/CSS/Nesting_selector")
WEBDEV_BASELINE = ("web.dev — Baseline", "https://web.dev/baseline")
MDN_ANCHOR = ("MDN — CSS anchor positioning", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning")
MDN_SUPPORTS = ("MDN — @supports", "https://developer.mozilla.org/en-US/docs/Web/CSS/@supports")
MDN_DISPLAY = ("MDN — display", "https://developer.mozilla.org/en-US/docs/Web/CSS/display")
MDN_VISIBILITY = ("MDN — visibility", "https://developer.mozilla.org/en-US/docs/Web/CSS/visibility")
MDN_CONTENT_VISIBILITY = ("MDN — content-visibility", "https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility")
MDN_LANG = ("MDN — :lang()", "https://developer.mozilla.org/en-US/docs/Web/CSS/:lang")
MDN_UNICODE_RANGE = ("MDN — @font-face unicode-range", "https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range")
MDN_CQ = ("MDN — CSS container queries", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries")

QUESTIONS = [
    # ------------------------------------------------------------------ css-010
    Q(
        id="css-010", sub="Accessibility", diff="easy", type="debugging",
        prio="high", market="both", mins=4,
        tags=["focus-visible", "outline", "keyboard", "accessibility"],
        ver="Version-independent (CSS); :focus-visible Baseline widely available", vs=False, status="stable",
        q_en=r"""A designer complained about "ugly blue rings" when clicking buttons, so a developer added the CSS below. What's wrong with it, and how would you satisfy both the designer and keyboard users?""",
        q_bn=r"""Button-এ click করলে "বিশ্রী নীল ring" দেখা যায় বলে একজন designer অভিযোগ করেছিল, তাই একজন developer নিচের CSS যোগ করেছে। এতে সমস্যা কী, আর designer ও keyboard user — দুজনকেই কীভাবে সন্তুষ্ট করবে?""",
        code=r"""
            *:focus { outline: none; }

            .btn {
              background: #0b6e4f;
              color: #fff;
              border: 0;
              border-radius: 8px;
              padding: 12px 20px;
            }
            .btn:hover { background: #095c42; }
        """,
        lang="css",
        a_en=r"""
            Removing the outline on every focused element makes focus **invisible**. Keyboard users (and many switch and voice-control users) can no longer see where they are on the page — that fails WCAG 2.4.7 *Focus Visible* (Level AA). The page is effectively unusable without a mouse.

            The fix is `:focus-visible`. Browsers use heuristics to match it only when a focus indicator is useful — after keyboard navigation, or always for text inputs — and usually *not* when a button is clicked with a mouse. So I delete the global `outline: none` and design a clear, on-brand focus style for `:focus-visible`: a thick outline with an offset, in a colour that contrasts at least 3:1 with the surrounding colours.
        """,
        a_bn=r"""
            Focus পাওয়া প্রতিটা element থেকে outline সরিয়ে দিলে focus **অদৃশ্য** হয়ে যায়। Keyboard user (আর অনেক switch ও voice-control user) আর দেখতে পায় না তারা page-এর কোথায় আছে — এটা WCAG 2.4.7 *Focus Visible* (Level AA) ভঙ্গ করে। কার্যত mouse ছাড়া page-টা ব্যবহারই করা যায় না।

            সমাধান হলো `:focus-visible`। Browser কিছু heuristic দিয়ে এটা শুধু তখনই match করায়, যখন focus indicator কাজের — keyboard দিয়ে navigate করার পর, আর text input-এ সবসময় — আর সাধারণত mouse দিয়ে button click করলে *নয়*। তাই আমি global `outline: none` মুছে ফেলি, আর `:focus-visible`-এর জন্য একটা স্পষ্ট, brand-এর সাথে মানানসই focus style বানাই: offset-সহ মোটা outline, এমন রঙে যেটা আশেপাশের রঙের সাথে কমপক্ষে 3:1 contrast রাখে।
        """,
        quick_en=r"""`*:focus { outline: none; }` makes keyboard focus invisible and fails WCAG 2.4.7 Focus Visible. Remove it and style `:focus-visible` instead, which browsers show for keyboard navigation but usually not for mouse clicks, with a clear outline at 3:1 contrast.""",
        quick_bn=r"""`*:focus { outline: none; }` keyboard focus অদৃশ্য করে দেয়, যা WCAG 2.4.7 Focus Visible ভাঙে। এটা মুছে `:focus-visible` style করো, যেটা browser keyboard navigation-এ দেখায় কিন্তু mouse click-এ সাধারণত দেখায় না, সাথে 3:1 contrast-এর স্পষ্ট outline।""",
        ex_en=r"""
            - **Outline vs box-shadow:** `outline` doesn't affect layout and remains visible in Windows forced-colours (high contrast) mode, while `box-shadow` is removed there. If you design focus with `box-shadow`, add `outline: 2px solid transparent` so a visible outline appears in forced-colours mode.
            - **Contrast:** the focus indicator is a UI component, so WCAG 1.4.11 asks for 3:1 against adjacent colours. A two-tone indicator (e.g. outline + `outline-offset` on a coloured button) works on both light and dark backgrounds.
            - **Legacy pattern:** `:focus:not(:focus-visible) { outline: none; }` was a workaround from before `:focus-visible` was widely supported; today, styling `:focus-visible` directly is enough because browser default styles already use it.
            - **Don't forget custom widgets:** anything focusable (`tabindex="0"`, links styled as cards) needs the same indicator.
        """,
        ex_bn=r"""
            - **Outline বনাম box-shadow:** `outline` layout-এ প্রভাব ফেলে না আর Windows forced-colours (high contrast) mode-এও দেখা যায়, কিন্তু সেখানে `box-shadow` সরিয়ে ফেলা হয়। `box-shadow` দিয়ে focus design করলে `outline: 2px solid transparent` যোগ করো, যাতে forced-colours mode-এ একটা দৃশ্যমান outline আসে।
            - **Contrast:** focus indicator একটা UI component, তাই WCAG 1.4.11 অনুযায়ী আশেপাশের রঙের সাথে 3:1 contrast লাগে। দুই রঙের indicator (যেমন রঙিন button-এ outline + `outline-offset`) হালকা ও গাঢ় দুই ধরনের background-এই কাজ করে।
            - **পুরোনো pattern:** `:focus:not(:focus-visible) { outline: none; }` ছিল `:focus-visible` ব্যাপকভাবে support পাওয়ার আগের একটা workaround; এখন সরাসরি `:focus-visible` style করলেই যথেষ্ট, কারণ browser-এর default style আগেই এটা ব্যবহার করে।
            - **Custom widget ভুলো না:** focus করা যায় এমন সবকিছুর (`tabindex="0"`, card-এর মতো style করা link) একই indicator লাগবে।
        """,
        tip_en=r"""Frame the fix as a win-win: "the designer's real complaint was mouse clicks, and `:focus-visible` solves exactly that without hurting keyboard users". Then mention one detail (forced colours or 3:1 contrast) to show depth.""",
        tip_bn=r"""সমাধানটা দুই পক্ষের জয় হিসেবে উপস্থাপন করো: "designer-এর আসল অভিযোগ ছিল mouse click নিয়ে, আর `:focus-visible` keyboard user-দের ক্ষতি না করে ঠিক সেটারই সমাধান করে"। তারপর গভীরতা দেখাতে একটা খুঁটিনাটি বলো (forced colours বা 3:1 contrast)।""",
        mist_en=r"""Removing outlines globally, replacing them with a colour change only (not visible enough), or relying on `box-shadow` alone for focus.""",
        mist_bn=r"""Global-ভাবে outline সরিয়ে দেওয়া, শুধু রং বদলে দেওয়া (যথেষ্ট দৃশ্যমান নয়), অথবা focus-এর জন্য শুধু `box-shadow`-এর উপর নির্ভর করা।""",
        extra=[dict(
            lang="css",
            src=r"""
                /* No global outline reset */

                .btn {
                  background: #0b6e4f;
                  color: #fff;
                  border: 0;
                  border-radius: 8px;
                  padding: 12px 20px;
                }
                .btn:hover { background: #095c42; }

                .btn:focus-visible {
                  outline: 3px solid #ffbf47;   /* high contrast against green and white */
                  outline-offset: 2px;
                }
            """,
            label_en="Fixed CSS",
            label_bn="সংশোধিত CSS",
        )],
        follow=[
            ("Why does `:focus-visible` match a text input even when you click it?", "Click করলেও text input-এ `:focus-visible` কেন match করে?"),
            ("How would you test focus visibility across a whole site?", "পুরো site-এ focus দৃশ্যমান কি না, কীভাবে test করবে?"),
        ],
        related=["css-011", "css-029"],
        refs=[MDN_FOCUS_VISIBLE, WCAG_FOCUS_VISIBLE],
    ),
    # ------------------------------------------------------------------ css-011
    Q(
        id="css-011", sub="Accessibility", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["contrast", "wcag", "colour", "accessibility"],
        ver="WCAG 2.2 (Level AA)", vs=True, status="stable",
        q_en=r"""Under WCAG 2.2 Level AA, what is the minimum contrast ratio for normal-size body text (for example 16px regular) against its background?""",
        q_bn=r"""WCAG 2.2 Level AA অনুযায়ী, সাধারণ মাপের body text-এর (যেমন 16px regular) জন্য background-এর সাথে ন্যূনতম contrast ratio কত?""",
        options=[
            ("3:1", "3:1"),
            ("4.5:1", "4.5:1"),
            ("7:1", "7:1"),
            ("4.5:1 in light mode, but only 3:1 in dark mode", "Light mode-এ 4.5:1, কিন্তু dark mode-এ মাত্র 3:1"),
        ],
        correct=1,
        a_en=r"""
            **4.5:1** (success criterion 1.4.3, *Contrast (Minimum)*). Large text — at least 24px regular or about 18.7px bold — needs 3:1, and 7:1 is the stricter AAA level.
        """,
        a_bn=r"""
            **4.5:1** (success criterion 1.4.3, *Contrast (Minimum)*)। বড় text — কমপক্ষে 24px regular বা প্রায় 18.7px bold — এর জন্য 3:1 লাগে, আর 7:1 হলো আরও কড়া AAA level।
        """,
        quick_en=r"""4.5:1 for normal text (WCAG 1.4.3). Large text, at least 24px regular or about 18.7px bold, needs 3:1, and 7:1 is the stricter AAA level.""",
        quick_bn=r"""সাধারণ text-এর জন্য 4.5:1 (WCAG 1.4.3)। বড় text, অর্থাৎ কমপক্ষে 24px regular বা প্রায় 18.7px bold, তার জন্য 3:1, আর 7:1 হলো আরও কড়া AAA level।""",
        ex_en=r"""
            The tempting wrong answer is 3:1, because that number appears twice in WCAG: for **large text** and for **non-text contrast** (1.4.11) — input borders, icons, focus indicators and chart elements against their surroundings. Option D is a misconception: the requirement doesn't change with the theme, so dark mode needs the same ratios.

            Practical notes:
            - `#767676` on white is about 4.5:1 — roughly the lightest grey that passes for body text on white. Placeholder text counts as text, which is why very light placeholders fail.
            - Logos and disabled controls are exempt, but "disabled-looking" active controls are not.
            - DevTools' colour picker shows the contrast ratio and AA/AAA thresholds live; automated checkers catch most text issues but not text over images or gradients.
            - Thin strokes (light font weights, or detailed scripts like Bangla at small sizes) look fainter than the ratio suggests — aim higher than the minimum for small text.
        """,
        ex_bn=r"""
            প্রলোভনজনক ভুল উত্তর 3:1, কারণ WCAG-এ সংখ্যাটা দুই জায়গায় আছে: **বড় text**-এর জন্য আর **non-text contrast**-এর (1.4.11) জন্য — input-এর border, icon, focus indicator আর chart-এর উপাদান তাদের আশেপাশের সাপেক্ষে। Option D একটা ভুল ধারণা: theme বদলালে শর্ত বদলায় না, তাই dark mode-এও একই ratio লাগবে।

            বাস্তব কিছু কথা:
            - সাদার উপর `#767676` প্রায় 4.5:1 — সাদা background-এ body text-এর জন্য মোটামুটি সবচেয়ে হালকা ধূসর যেটা pass করে। Placeholder text-ও text হিসেবে গণ্য, এজন্যই খুব হালকা placeholder fail করে।
            - Logo আর disabled control ছাড়ের আওতায়, কিন্তু "disabled-এর মতো দেখতে" সক্রিয় control নয়।
            - DevTools-এর colour picker সরাসরি contrast ratio আর AA/AAA সীমা দেখায়; automated checker বেশিরভাগ text-এর সমস্যা ধরে, কিন্তু image বা gradient-এর উপরের text ধরে না।
            - পাতলা stroke (হালকা font weight, বা ছোট মাপে Bangla-র মতো সূক্ষ্ম লিপি) ratio যা বলে তার চেয়েও ফ্যাকাশে দেখায় — ছোট text-এর জন্য ন্যূনতমের চেয়ে বেশি লক্ষ্য রাখো।
        """,
        tip_en=r"""Give the full set in one breath — 4.5:1 normal text, 3:1 large text and UI components, 7:1 AAA — then mention a tool you use to check it.""",
        tip_bn=r"""এক নিঃশ্বাসে পুরো সেটটা বলো — সাধারণ text 4.5:1, বড় text আর UI component 3:1, AAA 7:1 — তারপর যাচাই করতে কোন tool ব্যবহার করো তা উল্লেখ করো।""",
        refs=[WCAG_CONTRAST, WCAG_NON_TEXT_CONTRAST],
    ),
    # ------------------------------------------------------------------ css-020
    Q(
        id="css-020", sub="Positioning", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["position-sticky", "overflow", "flexbox", "debugging"],
        ver="Version-independent (CSS); overflow: clip supported in all modern browsers", vs=False, status="stable",
        q_en=r"""The filters sidebar is supposed to stay visible while the product list scrolls, but it scrolls away with the page. Find every reason `position: sticky` isn't working here and fix it.""",
        q_bn=r"""Product list scroll করার সময় filters sidebar-এর দৃশ্যমান থাকার কথা, কিন্তু সেটা page-এর সাথে scroll হয়ে চলে যাচ্ছে। এখানে `position: sticky` কাজ না করার সব কারণ খুঁজে বের করো এবং ঠিক করো।""",
        code=r"""
            <div class="page">
              <header class="site-header">…</header>
              <div class="layout">
                <aside class="filters">…filters…</aside>
                <main>…long product list…</main>
              </div>
            </div>

            <style>
              .page    { overflow-x: hidden; }   /* added to stop a horizontal scrollbar */
              .layout  { display: flex; gap: 24px; }
              .filters { position: sticky; }
            </style>
        """,
        lang="html",
        a_en=r"""
            Three separate problems:
            1. **No inset.** Sticky needs a threshold such as `top: 16px`; without one it behaves like `relative`.
            2. **`overflow-x: hidden` on an ancestor.** Setting `overflow-x` to `hidden` also makes `overflow-y` compute to `auto`, so `.page` becomes a **scroll container**. Sticky elements stick relative to their nearest scroll container — `.page` — but the user is scrolling the *viewport*, not `.page`, so nothing sticks. Use `overflow-x: clip` (clips without creating a scroll container) or, better, fix whatever caused the horizontal overflow.
            3. **Flex stretching.** In a flex row, `align-items: stretch` (the default) makes `.filters` as tall as the product list. A sticky element can't move outside its containing block, and there's no room left to "stick". Use `align-self: flex-start` (or `align-items: flex-start` on the row).

            I'd also cap the sidebar's height (`max-height: calc(100dvh - 32px); overflow-y: auto;`) so long filter lists stay scrollable.
        """,
        a_bn=r"""
            তিনটা আলাদা সমস্যা:
            1. **কোনো inset নেই।** Sticky-র জন্য `top: 16px`-এর মতো একটা সীমা লাগে; না থাকলে এটা `relative`-এর মতো আচরণ করে।
            2. **Ancestor-এ `overflow-x: hidden`।** `overflow-x`-কে `hidden` করলে `overflow-y`-ও compute হয়ে `auto` হয়ে যায়, ফলে `.page` একটা **scroll container** হয়ে যায়। Sticky element তার সবচেয়ে কাছের scroll container-এর — অর্থাৎ `.page`-এর — সাপেক্ষে আটকায়, কিন্তু user scroll করছে *viewport*, `.page` নয়, তাই কিছুই আটকায় না। `overflow-x: clip` ব্যবহার করো (scroll container না বানিয়ে clip করে), অথবা আরও ভালো, horizontal overflow যে কারণে হচ্ছিল সেটাই ঠিক করো।
            3. **Flex stretch।** Flex row-এ `align-items: stretch` (default) `.filters`-কে product list-এর সমান লম্বা করে দেয়। Sticky element তার containing block-এর বাইরে যেতে পারে না, আর "আটকে থাকার" মতো জায়গাই বাকি থাকে না। `align-self: flex-start` ব্যবহার করো (বা row-এ `align-items: flex-start`)।

            Sidebar-এর height-এও একটা সীমা দেব (`max-height: calc(100dvh - 32px); overflow-y: auto;`), যাতে লম্বা filter list নিজের ভেতরে scroll করা যায়।
        """,
        quick_en=r"""Three causes: there's no `top` inset; `overflow-x: hidden` makes `.page` a scroll container, so the sidebar sticks to the wrong scroller; and flex stretch makes `.filters` as tall as the list. Add `top: 16px`, use `overflow-x: clip` (or fix the overflow) and `align-self: flex-start`.""",
        quick_bn=r"""তিনটা কারণ: `top` inset নেই; `overflow-x: hidden` `.page`-কে scroll container বানায়, তাই sidebar ভুল scroller-এ আটকাতে চায়; আর flex stretch `.filters`-কে list-এর সমান লম্বা করে দেয়। `top: 16px` দাও, `overflow-x: clip` ব্যবহার করো (বা overflow-এর কারণ ঠিক করো), আর `align-self: flex-start` দাও।""",
        ex_en=r"""
            - **Sticky's mental model:** it's relative positioning that switches to "fixed-like" within the bounds of (a) its nearest scrolling ancestor and (b) its parent's box. Most bugs violate one of those two.
            - **`clip` vs `hidden`:** `overflow: clip` (now supported in all modern browsers) clips painting but is not a scroll container, so it doesn't capture sticky descendants and can't be scrolled programmatically.
            - **Tables and sticky headers:** `position: sticky` on `<th>` works, but a wrapper with `overflow: auto` (for horizontal table scrolling) becomes the scroll container — then the header sticks within the wrapper, which needs its own height.
            - **Debugging:** in DevTools, walk up the ancestors and check computed `overflow` values; Chrome marks scroll containers with a "scroll" badge in the Elements panel.
        """,
        ex_bn=r"""
            - **Sticky-কে কীভাবে ভাববে:** এটা relative positioning, যেটা (ক) সবচেয়ে কাছের scroll হওয়া ancestor আর (খ) parent-এর box — এই দুই সীমার মধ্যে "fixed-এর মতো" হয়ে যায়। বেশিরভাগ bug এই দুটোর একটা ভঙ্গ করে।
            - **`clip` বনাম `hidden`:** `overflow: clip` (এখন সব আধুনিক browser-এ support করে) আঁকার অংশ কাটে কিন্তু scroll container নয়, তাই এটা sticky descendant-দের আটকে রাখে না আর programmatically scroll-ও করা যায় না।
            - **Table আর sticky header:** `<th>`-এ `position: sticky` কাজ করে, কিন্তু horizontal table scroll-এর জন্য `overflow: auto` থাকা wrapper তখন scroll container হয়ে যায় — তখন header wrapper-এর ভেতরেই আটকায়, আর wrapper-এর নিজস্ব height লাগে।
            - **Debugging:** DevTools-এ ancestor ধরে উপরে উঠে প্রত্যেকের computed `overflow` দেখো; Chrome Elements panel-এ scroll container-কে একটা "scroll" badge দিয়ে চিহ্নিত করে।
        """,
        tip_en=r"""Interviewers often plant more than one bug here. Walk through the checklist out loud — inset, scrolling ancestor, parent height — instead of stopping at the first fix.""",
        tip_bn=r"""Interviewer প্রায়ই এখানে একাধিক bug রেখে দেয়। প্রথম সমাধানেই থেমে না গিয়ে checklist-টা মুখে বলে এগোও — inset, scroll হওয়া ancestor, parent-এর height।""",
        mist_en=r"""Only adding `top: 0`, switching to `position: fixed` (which breaks the layout), or adding `overflow: hidden` to more ancestors to "contain" it.""",
        mist_bn=r"""শুধু `top: 0` যোগ করা, `position: fixed`-এ বদলে ফেলা (যাতে layout ভেঙে যায়), অথবা "ধরে রাখতে" আরও ancestor-এ `overflow: hidden` যোগ করা।""",
        extra=[dict(
            lang="css",
            src=r"""
                .page   { overflow-x: clip; }   /* or remove it after fixing the real overflow */
                .layout { display: flex; gap: 24px; align-items: flex-start; }
                .filters {
                  position: sticky;
                  top: 16px;
                  max-height: calc(100dvh - 32px);
                  overflow-y: auto;
                }
            """,
            label_en="Fixed CSS",
            label_bn="সংশোধিত CSS",
        )],
        follow=[
            ("Why does `overflow-x: hidden` change `overflow-y` as well?", "`overflow-x: hidden` দিলে `overflow-y`-ও কেন বদলে যায়?"),
            ("How would you make a table header sticky inside a horizontally scrollable table?", "Horizontally scroll করা যায় এমন table-এর ভেতরে table header কীভাবে sticky করবে?"),
        ],
        related=["css-004", "css-027"],
        refs=[MDN_POSITION, MDN_OVERFLOW],
    ),
    # ------------------------------------------------------------------ css-021
    Q(
        id="css-021", sub="Responsive Design", diff="medium", type="scenario",
        prio="high", market="both", mins=6,
        tags=["clamp", "fluid-typography", "responsive", "accessibility", "rem"],
        ver="Version-independent (CSS); clamp() Baseline widely available", vs=False, status="stable",
        q_en=r"""Design wants the product page heading to be 24px on a 360px-wide phone and 40px on a 1200px-wide desktop, scaling smoothly in between and never going outside that range. Write the CSS and explain the accessibility trade-offs.""",
        q_bn=r"""Design চায় product page-এর heading 360px চওড়া phone-এ 24px আর 1200px চওড়া desktop-এ 40px হবে, মাঝের মাপগুলোতে মসৃণভাবে বাড়বে, আর কখনো এই সীমার বাইরে যাবে না। CSS লেখো এবং accessibility-র trade-off ব্যাখ্যা করো।""",
        a_en=r"""
            I'd use `clamp(min, preferred, max)` with a preferred value that's a **linear function of the viewport width** — part `rem`, part `vw`.

            The maths (assuming the default 16px root size):
            - slope = (40 − 24) / (1200 − 360) = 16 / 840 ≈ 0.019 → **1.9048vw**
            - intercept = 24 − 0.019048 × 360 ≈ 17.14px → **1.0714rem**
            - so: `font-size: clamp(1.5rem, 1.0714rem + 1.9048vw, 2.5rem);`

            Check: at 360px, 17.14 + 6.86 = 24px; at 1200px, 17.14 + 22.86 = 40px. Below 360px it stays at 24px, above 1200px at 40px.

            **Accessibility:** a pure `vw` font size ignores the user's default font size and doesn't grow with page zoom either (zooming shrinks the viewport in CSS pixels, so `vw` shrinks too) — that can fail WCAG 1.4.4 *Resize Text*. Keeping `rem` for the bounds and part of the preferred value means user font settings and zoom still have an effect. I still test at 200% zoom and with a larger default font size, and I keep body text far less fluid than headings.
        """,
        a_bn=r"""
            আমি `clamp(min, preferred, max)` ব্যবহার করব, যার preferred value হবে **viewport width-এর একটা linear function** — কিছুটা `rem`, কিছুটা `vw`।

            হিসাব (default 16px root size ধরে):
            - slope = (40 − 24) / (1200 − 360) = 16 / 840 ≈ 0.019 → **1.9048vw**
            - intercept = 24 − 0.019048 × 360 ≈ 17.14px → **1.0714rem**
            - তাই: `font-size: clamp(1.5rem, 1.0714rem + 1.9048vw, 2.5rem);`

            যাচাই: 360px-এ 17.14 + 6.86 = 24px; 1200px-এ 17.14 + 22.86 = 40px। 360px-এর নিচে এটা 24px-এই থাকে, 1200px-এর উপরে 40px।

            **Accessibility:** শুধু `vw` দিয়ে font size দিলে user browser-এর default font size বাড়ালেও এটা বাড়ে না, page zoom করলেও বাড়ে না (zoom করলে CSS pixel-এ viewport ছোট হয়, তাই `vw`-ও ছোট হয়) — এতে WCAG 1.4.4 *Resize Text* ভঙ্গ হতে পারে। সীমাগুলো আর preferred value-র একটা অংশ `rem`-এ রাখলে user-এর font setting আর zoom তখনো কাজ করে। তবুও আমি 200% zoom আর বড় default font size দিয়ে test করি, আর heading-এর তুলনায় body text-কে অনেক কম fluid রাখি।
        """,
        quick_en=r"""`font-size: clamp(1.5rem, 1.0714rem + 1.9048vw, 2.5rem)`: a linear `rem` + `vw` value that is 24px at 360px and 40px at 1200px. Pure `vw` ignores the user's font size and zoom, so keeping a `rem` part matters for accessibility.""",
        quick_bn=r"""`font-size: clamp(1.5rem, 1.0714rem + 1.9048vw, 2.5rem)`: একটা linear `rem` + `vw` value, যা 360px-এ 24px আর 1200px-এ 40px। শুধু `vw` দিলে user-এর font size আর zoom উপেক্ষিত হয়, তাই accessibility-র জন্য একটা `rem` অংশ রাখা জরুরি।""",
        ex_en=r"""
            - **Why not media-query steps?** Steps work, but they jump at each breakpoint and need several rules; `clamp()` is one declaration that's continuous.
            - **Component-level fluid type:** inside a container query container, `cqi` units (`1.0714rem + 4cqi`) make the heading respond to the card's width instead of the viewport.
            - **Don't set `html { font-size: 62.5% }`** to make maths easier; it overrides the user's preferred base size in a fragile way. Do the maths with 16px and use `rem`.
            - **Bangla headings** need a more generous `line-height` (around 1.4–1.5) than Latin headings, because vowel signs extend above and below the line; fluid sizes make clipping in tight containers more likely.
            - **`text-wrap: balance`** (Baseline newly available) evens out line lengths in multi-line headings — a nice touch alongside fluid sizing.
        """,
        ex_bn=r"""
            - **Media query-র ধাপ কেন নয়?** ধাপে ধাপে করলেও চলে, কিন্তু প্রতিটা breakpoint-এ হঠাৎ লাফ দেয় আর কয়েকটা rule লাগে; `clamp()` একটা declaration-এই নিরবচ্ছিন্ন।
            - **Component-level fluid type:** container query container-এর ভেতরে `cqi` unit (`1.0714rem + 4cqi`) দিলে heading viewport-এর বদলে card-এর width অনুযায়ী সাড়া দেয়।
            - **হিসাব সহজ করতে `html { font-size: 62.5% }` দিও না**; এটা user-এর পছন্দের base size ভঙ্গুরভাবে override করে। 16px ধরে হিসাব করো আর `rem` ব্যবহার করো।
            - **Bangla heading**-এ Latin heading-এর চেয়ে বেশি `line-height` লাগে (প্রায় 1.4–1.5), কারণ কারচিহ্ন (vowel sign) line-এর উপরে-নিচে বেরিয়ে থাকে; fluid size-এর কারণে আঁটসাঁট container-এ কেটে যাওয়ার সম্ভাবনা বাড়ে।
            - **`text-wrap: balance`** (Baseline newly available) কয়েক লাইনের heading-এর line-এর দৈর্ঘ্য সমান করে — fluid sizing-এর সাথে একটা সুন্দর সংযোজন।
        """,
        tip_en=r"""Show the slope/intercept calculation and verify both endpoints — it proves the numbers aren't magic. Then raise the zoom/`rem` issue yourself before the interviewer asks.""",
        tip_bn=r"""Slope/intercept-এর হিসাব দেখাও আর দুই প্রান্তেই যাচাই করো — এতে প্রমাণ হয় সংখ্যাগুলো জাদু নয়। তারপর interviewer জিজ্ঞেস করার আগেই zoom/`rem`-এর সমস্যাটা নিজে তোলো।""",
        mist_en=r"""Using `font-size: 5vw` with no bounds, using `px` for the clamp limits (ignores user font settings), or making body text as fluid as headings.""",
        mist_bn=r"""কোনো সীমা ছাড়া `font-size: 5vw` ব্যবহার করা, clamp-এর সীমায় `px` ব্যবহার করা (user-এর font setting উপেক্ষা করে), অথবা body text-কেও heading-এর মতো fluid করা।""",
        code=r"""
            h1.product-title {
              /* 24px at a 360px viewport → 40px at a 1200px viewport */
              font-size: clamp(1.5rem, 1.0714rem + 1.9048vw, 2.5rem);
              line-height: 1.2;
              text-wrap: balance;
            }

            h1.product-title:lang(bn) {
              line-height: 1.45;   /* room for Bangla vowel signs */
            }
        """,
        lang="css",
        follow=[
            ("How would you generate a whole fluid type scale (h1–h6) without hand-calculating each one?", "প্রতিটা হাতে হিসাব না করে পুরো একটা fluid type scale (h1–h6) কীভাবে বানাবে?"),
            ("When would you use `cqi` instead of `vw` in the preferred value?", "Preferred value-তে কখন `vw`-এর বদলে `cqi` ব্যবহার করবে?"),
        ],
        related=["css-007", "css-032"],
        refs=[MDN_CLAMP, WEBDEV_TYPOGRAPHY, WCAG_RESIZE_TEXT],
    ),
    # ------------------------------------------------------------------ css-022
    Q(
        id="css-022", sub="Modern CSS Features", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["nesting", "selectors", "sass", "modern-css"],
        ver="CSS Nesting; Baseline widely available", vs=False, status="stable",
        q_en=r"""Using native CSS nesting (no preprocessor), what do the selectors marked A, B and C match?""",
        q_bn=r"""Native CSS nesting ব্যবহার করে (কোনো preprocessor ছাড়া) A, B আর C চিহ্নিত selector-গুলো কী match করে?""",
        code=r"""
            .card {
              padding: 1rem;

              & .title { font-weight: 700; }      /* A */
              &.featured { border-color: gold; }  /* B */
              .sidebar & { padding: 0.5rem; }     /* C */
            }
        """,
        lang="css",
        options=[
            ("A: `.card .title` — B: `.card.featured` — C: `.sidebar .card`", "A: `.card .title` — B: `.card.featured` — C: `.sidebar .card`"),
            ("A: `.card .title` — B: `.card .featured` — C: `.card .sidebar`", "A: `.card .title` — B: `.card .featured` — C: `.card .sidebar`"),
            ("A: `.card.title` — B: `.card.featured` — C: `.sidebar.card`", "A: `.card.title` — B: `.card.featured` — C: `.sidebar.card`"),
            ("A and B work, but C is invalid: native nesting doesn't allow `&` at the end (Sass-only)", "A আর B কাজ করে, কিন্তু C invalid: native nesting-এ `&` শেষে বসানো যায় না (শুধু Sass-এ চলে)"),
        ],
        correct=0,
        a_en=r"""
            The first option. `&` stands for the parent selector: a space after it means a **descendant** (`.card .title`), no space means a **compound** selector on the same element (`.card.featured`), and `&` can appear anywhere — `.sidebar &` means "a `.card` inside `.sidebar`".
        """,
        a_bn=r"""
            প্রথম option-টা। `&` parent selector-এর প্রতিনিধি: এর পরে space থাকলে মানে **descendant** (`.card .title`), space না থাকলে একই element-এর **compound** selector (`.card.featured`), আর `&` যেকোনো জায়গায় বসতে পারে — `.sidebar &` মানে "`.sidebar`-এর ভেতরের একটা `.card`"।
        """,
        quick_en=r"""A is `.card .title`, B is `.card.featured` and C is `.sidebar .card`. A space after `&` means descendant, no space means the same element, and `&` can appear anywhere, including at the end.""",
        quick_bn=r"""A হলো `.card .title`, B হলো `.card.featured`, আর C হলো `.sidebar .card`। `&`-এর পরে space মানে descendant, space না থাকলে একই element, আর `&` যেকোনো জায়গায় বসতে পারে, শেষেও।""",
        ex_en=r"""
            The tempting wrong answer is D, because older docs and early browser implementations had stricter rules. Native nesting allows `&` anywhere in the nested selector, and modern browsers also accept nested selectors that don't start with `&` (`.title { … }` inside `.card` means `.card .title`).

            Important differences from Sass:
            - **No string concatenation.** Sass's BEM trick `&__title` → `.card__title` does **not** work natively — `&` represents a selector, not text.
            - **Specificity works like `:is()`.** `#a, .b { & span {} }` behaves like `:is(#a, .b) span`, so the whole nested selector gets the ID's specificity even when matched through `.b`.
            - **At-rules can nest:** `@media` and `@container` inside a rule apply to that rule's selector.

            Nesting is Baseline widely available, so it's safe to ship without a build step — but avoid nesting more than two or three levels deep; it creates long, high-specificity selectors.
        """,
        ex_bn=r"""
            প্রলোভনজনক ভুল উত্তর D, কারণ পুরোনো documentation আর browser-এর প্রথম দিকের implementation-এ নিয়ম আরও কড়া ছিল। Native nesting nested selector-এর যেকোনো জায়গায় `&` বসাতে দেয়, আর আধুনিক browser `&` দিয়ে শুরু না হওয়া nested selector-ও মেনে নেয় (`.card`-এর ভেতরে `.title { … }` মানে `.card .title`)।

            Sass থেকে গুরুত্বপূর্ণ পার্থক্য:
            - **String জোড়া লাগানো যায় না।** Sass-এর BEM trick `&__title` → `.card__title` native-এ কাজ **করে না** — `&` একটা selector-এর প্রতিনিধি, text-এর নয়।
            - **Specificity `:is()`-এর মতো কাজ করে।** `#a, .b { & span {} }` আচরণ করে `:is(#a, .b) span`-এর মতো, ফলে `.b` দিয়ে match হলেও পুরো nested selector ID-র specificity পায়।
            - **At-rule nest করা যায়:** কোনো rule-এর ভেতরে `@media` আর `@container` দিলে সেটা ওই rule-এর selector-এ প্রযোজ্য হয়।

            Nesting Baseline widely available, তাই build step ছাড়াই ship করা নিরাপদ — তবে দুই-তিন স্তরের বেশি nest কোরো না; এতে লম্বা, বেশি specificity-র selector তৈরি হয়।
        """,
        tip_en=r"""After answering, mention the BEM `&__title` difference from Sass — it's the most common surprise when teams drop their preprocessor.""",
        tip_bn=r"""উত্তর দেওয়ার পর Sass-এর সাথে BEM `&__title`-এর পার্থক্যটা বলো — team-রা preprocessor বাদ দিলে এটাই সবচেয়ে সাধারণ চমক।""",
        refs=[MDN_NESTING, MDN_NESTING_SELECTOR],
    ),
    # ------------------------------------------------------------------ css-028
    Q(
        id="css-028", sub="Modern CSS Features", diff="hard", type="conceptual",
        prio="medium", market="both", mins=8,
        tags=["baseline", "progressive-enhancement", "anchor-positioning", "scope", "supports"],
        ver="Baseline status per web-features (Oct 2026): anchor positioning & scroll-driven animations limited; @scope and style queries newly available", vs=True, status="stable",
        q_en=r"""It's October 2026. Your team wants to use modern CSS: nesting, `:has()`, container size and style queries, `@scope`, View Transitions, anchor positioning and scroll-driven animations. How do you decide what's safe to ship, and how do you use the newer features responsibly?""",
        q_bn=r"""এখন October 2026। তোমার team আধুনিক CSS ব্যবহার করতে চায়: nesting, `:has()`, container size ও style query, `@scope`, View Transitions, anchor positioning আর scroll-driven animation। কোনটা ship করা নিরাপদ তা কীভাবে ঠিক করবে, আর নতুন feature-গুলো দায়িত্বশীলভাবে কীভাবে ব্যবহার করবে?""",
        a_en=r"""
            I use **Baseline** as the shared vocabulary, then check it against our own analytics.

            - **Widely available** (supported in all core browsers for a long time) → ship freely: **nesting, `:has()`, container size queries, cascade layers, subgrid**.
            - **Newly available** (works in the latest versions of all core browsers, but older devices may lack it) → use as **progressive enhancement**, or freely if analytics show our users are on current browsers: **container style queries** (May 2026), **`@scope`** (March 2026), **same-document View Transitions** (October 2025), `@starting-style`.
            - **Limited availability (not Baseline)** → enhancement only, behind `@supports`, with a fallback that's fully usable: **anchor positioning**, **scroll-driven animations**, customizable `<select>`, cross-document view transitions, CSS `if()`.

            Techniques:
            - `@supports (anchor-name: --a)` / `@supports selector(:has(a))` to layer enhancements on top of a working baseline.
            - Write the fallback first, test it in an older browser, then add the enhancement.
            - Check analytics for in-app browsers and older Android WebViews, which can lag behind the latest Chrome — common for traffic coming from social media apps.
            - Polyfills only when the feature is essential and the polyfill is small and maintained.
        """,
        a_bn=r"""
            আমি **Baseline**-কে সবার জন্য একটা সাধারণ ভাষা হিসেবে ব্যবহার করি, তারপর আমাদের নিজস্ব analytics-এর সাথে মিলিয়ে দেখি।

            - **Widely available** (অনেক দিন ধরে সব core browser-এ support আছে) → নিশ্চিন্তে ship করো: **nesting, `:has()`, container size query, cascade layer, subgrid**।
            - **Newly available** (সব core browser-এর সর্বশেষ version-এ কাজ করে, কিন্তু পুরোনো device-এ না-ও থাকতে পারে) → **progressive enhancement** হিসেবে ব্যবহার করো, অথবা analytics-এ user-রা current browser-এ থাকলে নিশ্চিন্তে: **container style query** (May 2026), **`@scope`** (March 2026), **same-document View Transitions** (October 2025), `@starting-style`।
            - **Limited availability (Baseline নয়)** → শুধু enhancement, `@supports`-এর আড়ালে, এমন fallback-সহ যেটা পুরোপুরি ব্যবহারযোগ্য: **anchor positioning**, **scroll-driven animation**, customizable `<select>`, cross-document view transition, CSS `if()`।

            কৌশল:
            - কাজ করা একটা ভিত্তির উপরে enhancement বসাতে `@supports (anchor-name: --a)` / `@supports selector(:has(a))`।
            - আগে fallback লেখো, পুরোনো browser-এ test করো, তারপর enhancement যোগ করো।
            - In-app browser আর পুরোনো Android WebView-এর জন্য analytics দেখো, এগুলো সর্বশেষ Chrome-এর চেয়ে পিছিয়ে থাকতে পারে — social media app থেকে আসা traffic-এ এটা সাধারণ।
            - Polyfill শুধু তখনই, যখন feature-টা অপরিহার্য আর polyfill ছোট ও maintain করা হয়।
        """,
        quick_en=r"""Use Baseline plus your own analytics: ship widely available features (nesting, `:has()`, size queries, layers, subgrid) freely, use newly available ones like style queries and `@scope` as enhancements, and keep limited ones like anchor positioning behind `@supports` with a working fallback.""",
        quick_bn=r"""Baseline আর নিজের analytics মিলিয়ে ঠিক করি: widely available feature (nesting, `:has()`, size query, layer, subgrid) নির্দ্বিধায় ship করি, style query বা `@scope`-এর মতো newly available feature enhancement হিসেবে দিই, আর anchor positioning-এর মতো limited feature কার্যকর fallback-সহ `@supports`-এর পেছনে রাখি।""",
        ex_en=r"""
            **What the newer features are for:**
            - **`@scope (.card) to (.reviews)`** limits styles to a subtree with a lower boundary ("donut scope") and adds *scoping proximity* to the cascade — the closer scope root wins.
            - **Container style queries** react to custom property values (`@container style(--variant: sale)`), great for component variants.
            - **Anchor positioning** tethers a tooltip or menu to another element (`anchor-name`, `position-anchor`, `anchor()`), with automatic fallbacks when it would overflow — replacing positioning libraries eventually, but not yet Baseline.
            - **Scroll-driven animations** link animation progress to scroll position — nice for reading-progress bars, but must respect `prefers-reduced-motion` and stay optional.

            **Common mistake:** writing the enhancement *with* higher specificity than the fallback (or vice versa), so one silently never applies — keep matching selectors inside and outside `@supports`.
        """,
        ex_bn=r"""
            **নতুন feature-গুলো কীসের জন্য:**
            - **`@scope (.card) to (.reviews)`** একটা নিচের সীমাসহ ("donut scope") style-কে একটা subtree-তে সীমিত রাখে, আর cascade-এ *scoping proximity* যোগ করে — কাছের scope root জেতে।
            - **Container style query** custom property-র value-তে সাড়া দেয় (`@container style(--variant: sale)`), component variant-এর জন্য দারুণ।
            - **Anchor positioning** একটা tooltip বা menu-কে অন্য element-এর সাথে বেঁধে রাখে (`anchor-name`, `position-anchor`, `anchor()`), overflow হলে স্বয়ংক্রিয় বিকল্প অবস্থানসহ — একসময় positioning library-র জায়গা নেবে, কিন্তু এখনো Baseline নয়।
            - **Scroll-driven animation** animation-এর অগ্রগতিকে scroll position-এর সাথে যুক্ত করে — reading-progress bar-এর জন্য সুন্দর, কিন্তু `prefers-reduced-motion` মানতে হবে আর ঐচ্ছিক রাখতে হবে।

            **সাধারণ ভুল:** enhancement-কে fallback-এর চেয়ে বেশি specificity দিয়ে লেখা (বা উল্টোটা), ফলে একটা চুপচাপ কখনো প্রয়োগই হয় না — `@supports`-এর ভেতরে আর বাইরে একই selector রাখো।
        """,
        tip_en=r"""Sort the list into the three Baseline buckets out loud — that's the core of the answer. Being precise that anchor positioning and scroll-driven animations are *not* Baseline yet shows you track the platform rather than blog hype.""",
        tip_bn=r"""তালিকাটা মুখে মুখে Baseline-এর তিনটা ভাগে সাজাও — উত্তরের মূল অংশ এটাই। Anchor positioning আর scroll-driven animation যে এখনো Baseline *নয়*, সেটা নির্ভুলভাবে বললে বোঝা যায় তুমি blog-এর হুজুগ নয়, platform-এর আসল অবস্থা খেয়াল রাখো।""",
        mist_en=r"""Treating "works in my Chrome" as "safe to ship", shipping anchor positioning without a fallback, or avoiding all modern CSS out of caution even when it's widely available.""",
        mist_bn=r""""আমার Chrome-এ চলে"-কে "ship করা নিরাপদ" ধরে নেওয়া, fallback ছাড়া anchor positioning ship করা, অথবা widely available হওয়া সত্ত্বেও অতিরিক্ত সাবধানতায় সব আধুনিক CSS এড়িয়ে চলা।""",
        code=r"""
            /* Fallback that works everywhere: tooltip inside a positioned wrapper.
               The button comes before the tooltip in the HTML. */
            .info { position: relative; }
            .info .tooltip {
              position: absolute;
              top: calc(100% + 8px);
              left: 0;
            }

            /* Enhancement: anchor positioning (limited availability, not Baseline) */
            @supports (anchor-name: --a) {
              .info .info-button { anchor-name: --info; }
              .info .tooltip {
                position-anchor: --info;
                top: calc(anchor(bottom) + 8px);
                left: anchor(left);
                position-try-fallbacks: flip-block;   /* flip above if no room below */
              }
            }

            /* @scope (Baseline newly available): styles stop at .reviews */
            @scope (.product-card) to (.reviews) {
              img { border-radius: 8px; }
            }
        """,
        lang="css",
        follow=[
            ("What's the difference between `@scope` and cascade layers?", "`@scope` আর cascade layer-এর পার্থক্য কী?"),
            ("How would you decide that a 'newly available' feature is safe for your audience?", "একটা 'newly available' feature তোমার audience-এর জন্য নিরাপদ কি না, কীভাবে ঠিক করবে?"),
        ],
        related=["css-030", "css-022"],
        refs=[WEBDEV_BASELINE, MDN_ANCHOR, MDN_SUPPORTS],
    ),
    # ------------------------------------------------------------------ css-029
    Q(
        id="css-029", sub="Accessibility", diff="hard", type="comparison",
        prio="high", market="both", mins=7,
        tags=["display-none", "visibility", "visually-hidden", "aria-hidden", "accessibility"],
        ver="Version-independent (CSS/HTML); content-visibility Baseline newly available", vs=False, status="stable",
        q_en=r"""Compare the ways to hide content: `display: none`, `visibility: hidden`, `opacity: 0`, the `hidden` attribute, a "visually hidden" class, `content-visibility: hidden` and `aria-hidden="true"`. For each, does it keep layout space, is it read by screen readers, and can it still be focused or clicked?""",
        q_bn=r"""Content লুকানোর উপায়গুলো তুলনা করো: `display: none`, `visibility: hidden`, `opacity: 0`, `hidden` attribute, একটা "visually hidden" class, `content-visibility: hidden` আর `aria-hidden="true"`। প্রতিটার ক্ষেত্রে — layout-এ জায়গা থাকে কি না, screen reader পড়ে কি না, আর এখনো focus বা click করা যায় কি না?""",
        a_en=r"""
            - **`display: none`** — no box, no space; removed from the accessibility tree; not focusable or clickable. The standard "really gone" option.
            - **`hidden` attribute** — same as `display: none` via the browser's default stylesheet. **Gotcha:** any author `display` rule (e.g. `.menu { display: flex; }`) overrides it and the element reappears; many resets add `[hidden] { display: none !important; }`.
            - **`visibility: hidden`** — keeps its space; removed from the accessibility tree; not focusable or clickable. Children can opt back in with `visibility: visible`. Useful when you must keep layout stable.
            - **`opacity: 0`** — invisible but **still there**: keeps space, still read by screen readers, still focusable and clickable. Dangerous by itself — invisible buttons catch clicks and keyboard focus.
            - **Visually hidden class** (clip pattern) — no visible pixels and no layout impact, but **still read** by screen readers and focusable if interactive. Use for extra context ("(opens in new tab)"), icon-button labels and skip links that appear on focus.
            - **`content-visibility: hidden`** — the element's box stays, but its **contents** aren't rendered, read or focusable; rendering state is cached, so showing it again is fast. Good for hidden tabs or panels you toggle often.
            - **`aria-hidden="true"`** — fully visible, but **hidden from assistive tech** only. For decorative duplicates (an icon next to text). Never put it on focusable content.
        """,
        a_bn=r"""
            - **`display: none`** — কোনো box নেই, জায়গাও নেই; accessibility tree থেকে বাদ; focus বা click করা যায় না। "সত্যিই চলে গেছে"-র প্রচলিত উপায়।
            - **`hidden` attribute** — browser-এর default stylesheet দিয়ে `display: none`-এর মতোই। **ফাঁদ:** author-এর যেকোনো `display` rule (যেমন `.menu { display: flex; }`) এটাকে override করে আর element আবার দেখা দেয়; অনেক reset-এ `[hidden] { display: none !important; }` যোগ করা থাকে।
            - **`visibility: hidden`** — জায়গা ধরে রাখে; accessibility tree থেকে বাদ; focus বা click করা যায় না। Children `visibility: visible` দিয়ে আবার দৃশ্যমান হতে পারে। Layout স্থির রাখতে হলে কাজের।
            - **`opacity: 0`** — অদৃশ্য কিন্তু **এখনো আছে**: জায়গা ধরে রাখে, screen reader এখনো পড়ে, এখনো focus আর click করা যায়। একা ব্যবহার করলে বিপজ্জনক — অদৃশ্য button click আর keyboard focus ধরে ফেলে।
            - **Visually hidden class** (clip pattern) — কোনো দৃশ্যমান pixel নেই, layout-এ প্রভাবও নেই, কিন্তু screen reader **এখনো পড়ে**, আর interactive হলে focus করা যায়। বাড়তি প্রসঙ্গ ("(opens in new tab)"), icon button-এর label, আর focus পেলে দেখা দেয় এমন skip link-এর জন্য ব্যবহার করো।
            - **`content-visibility: hidden`** — element-এর box থাকে, কিন্তু এর **ভেতরের content** render হয় না, পড়া হয় না, focus-ও করা যায় না; rendering state cache থাকে, তাই আবার দেখানো দ্রুত হয়। ঘনঘন toggle করা hidden tab বা panel-এর জন্য ভালো।
            - **`aria-hidden="true"`** — পুরোপুরি দৃশ্যমান, কিন্তু শুধু **assistive tech থেকে লুকানো**। Decorative duplicate-এর জন্য (text-এর পাশের icon)। Focus করা যায় এমন content-এ কখনো দিও না।
        """,
        quick_en=r"""`display: none` and `hidden` remove the element completely; `visibility: hidden` keeps its space but hides it from everyone; `opacity: 0` still takes clicks, focus and screen readers; a visually-hidden class stays readable by screen readers; `aria-hidden="true"` hides it only from assistive tech.""",
        quick_bn=r"""`display: none` আর `hidden` element-কে পুরোপুরি সরিয়ে দেয়; `visibility: hidden` জায়গা রাখে কিন্তু সবার কাছ থেকে লুকায়; `opacity: 0`-এ click, focus আর screen reader সব চলে; visually-hidden class screen reader পড়তে পারে; `aria-hidden="true"` শুধু assistive tech থেকে লুকায়।""",
        ex_en=r"""
            - **Related tool — `inert`:** visible but not focusable, clickable or exposed to assistive tech; ideal for background content behind a custom overlay or an off-screen drawer while it's closed.
            - **Animating "hidden" states:** `display` and `visibility` can't animate smoothly on their own. Animate `opacity`/`transform`, then switch `visibility` at the end of the transition (it transitions discretely), or use `@starting-style` with `transition-behavior: allow-discrete` for `display`.
            - **Mobile menus:** a closed off-canvas menu moved off-screen with `transform` but not hidden is still in the tab order — keyboard users tab into invisible links. Add `visibility: hidden` or `inert` when closed.
            - **Find-in-page and SEO:** `display: none` content isn't found by Ctrl+F; `content-visibility: auto` content is, which is why `auto` (not `hidden`) is the choice for long pages you only want to render lazily.
        """,
        ex_bn=r"""
            - **সম্পর্কিত tool — `inert`:** দৃশ্যমান, কিন্তু focus, click বা assistive tech-এর নাগালের বাইরে; custom overlay-র পেছনের content বা বন্ধ থাকা off-screen drawer-এর জন্য আদর্শ।
            - **"Hidden" অবস্থার animation:** `display` আর `visibility` নিজে থেকে মসৃণভাবে animate হয় না। `opacity`/`transform` animate করো, তারপর transition-এর শেষে `visibility` বদলাও (এটা discrete-ভাবে transition হয়), অথবা `display`-এর জন্য `transition-behavior: allow-discrete`-সহ `@starting-style` ব্যবহার করো।
            - **Mobile menu:** `transform` দিয়ে screen-এর বাইরে সরানো কিন্তু লুকানো নয় এমন বন্ধ off-canvas menu তখনো tab order-এ থাকে — keyboard user অদৃশ্য link-এ tab করে ঢুকে পড়ে। বন্ধ অবস্থায় `visibility: hidden` বা `inert` যোগ করো।
            - **Find-in-page আর SEO:** `display: none`-এর content Ctrl+F দিয়ে খুঁজে পাওয়া যায় না; `content-visibility: auto`-এর content পাওয়া যায় — এজন্যই লম্বা page-এ শুধু lazy-ভাবে render করতে চাইলে `hidden` নয়, `auto` বেছে নেওয়া হয়।
        """,
        tip_en=r"""Answer as a mental table with three columns — space, screen readers, focus/click — and fill it row by row. Calling out `opacity: 0` as the dangerous one and the `hidden` + `display: flex` gotcha are the details that impress.""",
        tip_bn=r"""তিন column-এর একটা মানসিক table ধরে উত্তর দাও — জায়গা, screen reader, focus/click — আর সারি ধরে ধরে পূরণ করো। `opacity: 0`-কে বিপজ্জনক হিসেবে চিহ্নিত করা আর `hidden` + `display: flex`-এর ফাঁদ — এই খুঁটিনাটিগুলোই মুগ্ধ করে।""",
        mist_en=r"""Using `display: none` for screen-reader-only text, hiding focusable elements with `opacity: 0` or `aria-hidden`, and expecting the `hidden` attribute to beat an author `display` rule.""",
        mist_bn=r"""Screen reader-এর জন্য রাখা text-এ `display: none` ব্যবহার করা, focus করা যায় এমন element `opacity: 0` বা `aria-hidden` দিয়ে লুকানো, আর ভাবা যে `hidden` attribute author-এর `display` rule-কে হারাবে।""",
        code=r"""
            /* Screen-reader-only text (still announced, no visual footprint) */
            .visually-hidden:not(:focus):not(:active) {
              clip-path: inset(50%);
              height: 1px;
              width: 1px;
              overflow: hidden;
              position: absolute;
              white-space: nowrap;
            }

            /* Make the hidden attribute reliable even with author display rules */
            [hidden] { display: none !important; }

            /* Closed drawer: off-screen AND out of the tab order */
            .drawer { transform: translateX(-100%); visibility: hidden; transition: transform 250ms, visibility 0s 250ms; }
            .drawer.open { transform: none; visibility: visible; transition: transform 250ms; }
        """,
        lang="css",
        follow=[
            ("How would you label an icon-only 'Cart' button for screen readers?", "শুধু icon থাকা 'Cart' button-কে screen reader-এর জন্য কীভাবে label করবে?"),
            ("Why is `aria-hidden=\"true\"` on a focusable element a serious bug?", "Focus করা যায় এমন element-এ `aria-hidden=\"true\"` কেন গুরুতর bug?"),
        ],
        related=["css-010", "css-018"],
        refs=[MDN_DISPLAY, MDN_VISIBILITY, MDN_CONTENT_VISIBILITY],
    ),
    # ------------------------------------------------------------------ css-032
    Q(
        id="css-032", sub="Responsive UI Scenarios", diff="extreme", type="system-design",
        prio="medium", market="both", mins=20,
        tags=["responsive-design", "typography", "bangla", "container-queries", "design-system"],
        ver="Version-independent design (CSS); container size queries widely available; text-wrap: balance newly available", vs=False, status="stable",
        q_en=r"""Design the responsive layout and typography system for a bilingual (Bangla + English) e-commerce web app. Most users are on phones in Bangladesh, but there's significant desktop traffic. Components such as the product card appear in the main feed, a sidebar and a three-column desktop grid. What architecture, breakpoint strategy and typography decisions would you make?""",
        q_bn=r"""একটা দ্বিভাষিক (Bangla + English) e-commerce web app-এর responsive layout আর typography system design করো। বেশিরভাগ user বাংলাদেশে phone ব্যবহার করে, তবে desktop traffic-ও উল্লেখযোগ্য। Product card-এর মতো component main feed-এ, sidebar-এ আর তিন-column-এর desktop grid-এ দেখা যায়। কোন architecture, breakpoint কৌশল আর typography সিদ্ধান্ত নেবে?""",
        a_en=r"""
            This is advanced material. I'd split it into **macro layout**, **micro (component) layout**, **typography** and **guardrails**.

            **Requirements & constraints:** 320px phones to wide desktops; mid-range Android devices on variable mobile data; two scripts with different metrics; WCAG 2.2 AA (zoom, reflow at 320px, contrast, target size).

            **1. Macro layout — mobile-first media queries.** Single column by default; `rem`-based, content-driven breakpoints add the sidebar and then the three-column grid. CSS Grid with named areas keeps the page structure readable.

            **2. Micro layout — container queries.** Each slot (feed, sidebar, grid cell) is a size container; the product card switches between stacked and horizontal layouts based on **its slot's width**, so one component works everywhere. `cqi` units handle fluid spacing inside it.

            **3. Typography system.**
            - Fluid type scale with `clamp()` tokens in `rem` (`--step-0` … `--step-4`).
            - Mark language in HTML (`lang="bn"` / `lang="en"`, also on mixed snippets) and use `:lang(bn)` to switch font stacks and metrics.
            - Bangla needs a **larger `line-height`** (about 1.6–1.8 for body text) because vowel signs sit above and below the baseline, and conjuncts are tall; avoid `line-height: 1` and `overflow: hidden` on single-line labels, which clip glyphs.
            - **Never add `letter-spacing` or uppercase transforms to Bangla** — spacing breaks the continuous headstroke (matra) that joins letters.
            - Fonts: a well-hinted Bangla face (e.g. Noto Sans Bengali), subset with `unicode-range` so English-only pages don't download it, WOFF2, `font-display: swap`, and a system-font fallback. Consider slightly larger Bangla body size or `font-size-adjust` where supported, because many Bangla fonts look smaller than Latin at the same nominal size.

            **4. Guardrails.** Tokens as custom properties inside cascade layers; logical properties (`margin-inline`, `padding-block`) for future-proofing; touch targets at least 24×24 CSS px (WCAG 2.5.8), ideally larger; `prefers-reduced-motion`; and visual regression tests in **both languages** at 320px, 768px and 1440px.
        """,
        a_bn=r"""
            এটা advanced বিষয়। আমি এটাকে ভাগ করব **macro layout**, **micro (component) layout**, **typography** আর **guardrail**-এ।

            **প্রয়োজন ও সীমাবদ্ধতা:** 320px phone থেকে চওড়া desktop; অনিশ্চিত mobile data-য় mid-range Android device; ভিন্ন metric-এর দুটো লিপি; WCAG 2.2 AA (zoom, 320px-এ reflow, contrast, target size)।

            **1. Macro layout — mobile-first media query।** Default-ভাবে এক column; `rem`-ভিত্তিক, content অনুযায়ী ঠিক করা breakpoint প্রথমে sidebar, তারপর তিন-column grid যোগ করে। Named area-সহ CSS Grid page-এর কাঠামো পড়তে সহজ রাখে।

            **2. Micro layout — container query।** প্রতিটা slot (feed, sidebar, grid cell) একটা size container; product card **তার slot-এর width** অনুযায়ী stacked আর horizontal layout-এর মধ্যে বদলায়, ফলে একটা component সব জায়গায় কাজ করে। ভেতরের fluid spacing সামলায় `cqi` unit।

            **3. Typography system।**
            - `rem`-এ `clamp()` token দিয়ে fluid type scale (`--step-0` … `--step-4`)।
            - HTML-এ ভাষা চিহ্নিত করো (`lang="bn"` / `lang="en"`, মিশ্র অংশেও), আর `:lang(bn)` দিয়ে font stack আর metric বদলাও।
            - Bangla-য় **বেশি `line-height`** লাগে (body text-এর জন্য প্রায় 1.6–1.8), কারণ কারচিহ্ন baseline-এর উপরে-নিচে বসে, আর যুক্তাক্ষর লম্বা হয়; `line-height: 1` আর এক লাইনের label-এ `overflow: hidden` এড়িয়ে চলো, এগুলো glyph কেটে দেয়।
            - **Bangla-য় কখনো `letter-spacing` বা uppercase transform দিও না** — spacing অক্ষরগুলোকে জোড়া লাগানো নিরবচ্ছিন্ন মাত্রা ভেঙে দেয়।
            - Font: ভালোভাবে hint করা একটা Bangla font (যেমন Noto Sans Bengali), `unicode-range` দিয়ে subset করা যাতে শুধু English page-এ এটা download না হয়, WOFF2, `font-display: swap`, আর system-font fallback। অনেক Bangla font একই nominal size-এ Latin-এর চেয়ে ছোট দেখায়, তাই Bangla body size একটু বড় রাখা বা support থাকলে `font-size-adjust` বিবেচনা করো।

            **4. Guardrail।** Cascade layer-এর ভেতরে custom property হিসেবে token; ভবিষ্যতের জন্য logical property (`margin-inline`, `padding-block`); touch target কমপক্ষে 24×24 CSS px (WCAG 2.5.8), সম্ভব হলে আরও বড়; `prefers-reduced-motion`; আর **দুই ভাষাতেই** 320px, 768px আর 1440px-এ visual regression test।
        """,
        quick_en=r"""This is advanced: mobile-first media queries for the page, container queries so the card adapts to its slot, and a fluid `clamp()` type scale in `rem`. Use `:lang(bn)` for Bangla fonts with taller line-height and no letter-spacing, subset WOFF2 fonts, and test both languages at 320px.""",
        quick_bn=r"""এটা advanced বিষয়: page-এর জন্য mobile-first media query, card যাতে নিজের জায়গা অনুযায়ী বদলায় সেজন্য container query, আর `rem`-এ fluid `clamp()` type scale। Bangla font-এর জন্য `:lang(bn)` দিয়ে বেশি line-height আর letter-spacing ছাড়া style, subset করা WOFF2 font, আর 320px-এ দুই ভাষাতেই test।""",
        ex_en=r"""
            **Data flow of a layout decision:** viewport width → media query picks the page template → each slot's width → container query picks the component layout → fluid tokens size type and spacing. Each layer has one job, which keeps debugging simple.

            **Trade-offs:**
            - Container queries add a containment requirement (slots must get their width from layout, not content) — design slots deliberately.
            - Loading a Bangla web font improves consistency across devices but costs bytes on slow connections; subsetting and `swap` limit the damage, and system fonts are an acceptable fallback.
            - A single shared `line-height` is simpler, but language-specific metrics noticeably improve Bangla readability — worth the extra `:lang()` rules.

            **Failure scenarios:** long Bangla product names overflowing fixed-height cards (allow wrapping, clamp with `line-clamp` only where truncation is acceptable); mixed-script strings where Latin digits and Bangla text use mismatched fonts (define both in one stack); a CMS that forgets `lang` attributes (default the page `lang` per locale route, validate in CI).

            **Scaling the system:** document tokens and component variants in a shared library, test every component in both languages and at narrow widths, and let content designers preview real Bangla copy — lorem ipsum hides Bangla-specific problems.
        """,
        ex_bn=r"""
            **একটা layout সিদ্ধান্তের data flow:** viewport width → media query page template বেছে নেয় → প্রতিটা slot-এর width → container query component layout বেছে নেয় → fluid token type আর spacing-এর মাপ ঠিক করে। প্রতিটা স্তরের কাজ একটাই, তাই debugging সহজ থাকে।

            **Trade-off:**
            - Container query-র সাথে containment-এর একটা শর্ত আসে (slot-এর width content থেকে নয়, layout থেকে আসতে হবে) — তাই slot ভেবেচিন্তে design করো।
            - Bangla web font load করলে সব device-এ চেহারা একরকম থাকে, কিন্তু ধীর connection-এ byte-এর খরচ বাড়ে; subsetting আর `swap` ক্ষতি সীমিত রাখে, আর system font একটা গ্রহণযোগ্য fallback।
            - একটাই shared `line-height` সহজ, কিন্তু ভাষা-ভিত্তিক metric Bangla-র পাঠযোগ্যতা স্পষ্টভাবে বাড়ায় — বাড়তি `:lang()` rule-গুলো এর মূল্য রাখে।

            **ব্যর্থতার পরিস্থিতি:** লম্বা Bangla product name fixed-height card থেকে উপচে পড়া (wrap হতে দাও, যেখানে কেটে দেওয়া চলে শুধু সেখানে `line-clamp`); মিশ্র-লিপির string-এ Latin সংখ্যা আর Bangla text-এর font না মেলা (দুটোই একটা stack-এ define করো); CMS-এর `lang` attribute দিতে ভুলে যাওয়া (locale route অনুযায়ী page-এর `lang` default করে দাও, CI-তে যাচাই করো)।

            **System বড় করা:** token আর component variant একটা shared library-তে document করো, প্রতিটা component দুই ভাষায় আর সরু width-এ test করো, আর content designer-দের আসল Bangla copy দিয়ে preview করতে দাও — lorem ipsum Bangla-নির্দিষ্ট সমস্যাগুলো লুকিয়ে রাখে।
        """,
        tip_en=r"""Structure beats detail here: requirements → macro → micro → typography → guardrails. Then drop two or three Bangla-specific insights (line-height, no letter-spacing, `unicode-range` subsetting) — they show real product experience that generic answers lack.""",
        tip_bn=r"""এখানে খুঁটিনাটির চেয়ে কাঠামো বেশি গুরুত্বপূর্ণ: প্রয়োজন → macro → micro → typography → guardrail। তারপর Bangla-নির্দিষ্ট দুই-তিনটা অন্তর্দৃষ্টি যোগ করো (line-height, letter-spacing নয়, `unicode-range` subsetting) — এগুলো এমন বাস্তব product অভিজ্ঞতা দেখায় যা সাধারণ উত্তরে থাকে না।""",
        mist_en=r"""Using only viewport media queries for components, one global `line-height` tuned for Latin, letter-spacing on Bangla headings, shipping a full multi-script font file to every page, or testing only with English placeholder text.""",
        mist_bn=r"""Component-এর জন্য শুধু viewport media query ব্যবহার করা, Latin-এর জন্য ঠিক করা একটাই global `line-height`, Bangla heading-এ letter-spacing, প্রতিটা page-এ পুরো multi-script font file পাঠানো, অথবা শুধু English placeholder text দিয়ে test করা।""",
        code=r"""
            @font-face {
              font-family: "Noto Sans Bengali";
              src: url("/fonts/noto-sans-bengali-subset.woff2") format("woff2");
              font-display: swap;
              unicode-range: U+0980-09FF, U+200C-200D, U+0964-0965, U+25CC;
            }

            :root {
              --font-latin: "Inter", system-ui, sans-serif;
              --font-bangla: "Noto Sans Bengali", "Inter", system-ui, sans-serif;
              --step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
              --step-2: clamp(1.375rem, 1.1rem + 1.2vw, 2rem);
            }

            body { font-family: var(--font-latin); font-size: var(--step-0); line-height: 1.5; }
            :lang(bn) { font-family: var(--font-bangla); line-height: 1.75; letter-spacing: normal; }
            :lang(bn) :is(h1, h2, h3) { line-height: 1.45; }

            /* Macro layout: mobile-first */
            .page { display: grid; gap: 1rem; grid-template-areas: "main" "aside"; }
            @media (width >= 48rem) {
              .page { grid-template-columns: 2fr 1fr; grid-template-areas: "main aside"; }
            }

            /* Micro layout: the card adapts to its slot */
            .slot { container-type: inline-size; }
            .card { display: grid; gap: 0.5rem; }
            @container (min-width: 28rem) {
              .card { grid-template-columns: 8rem 1fr; }
            }
        """,
        lang="css",
        follow=[
            ("How would you handle prices and numbers that can appear in Bangla or Latin digits?", "Bangla বা Latin — দুই ধরনের অঙ্কে আসতে পারে এমন দাম আর সংখ্যা কীভাবে সামলাবে?"),
            ("What would you test at 320px and at 400% zoom?", "320px আর 400% zoom-এ কী কী test করবে?"),
            ("How do you stop a Bangla web font from hurting LCP on slow connections?", "ধীর connection-এ Bangla web font যাতে LCP খারাপ না করে, তা কীভাবে নিশ্চিত করবে?"),
        ],
        related=["css-016", "css-021", "css-007"],
        refs=[MDN_CQ, MDN_LANG, MDN_UNICODE_RANGE],
    ),
]

if __name__ == "__main__":
    save("css", "b4", QUESTIONS)
