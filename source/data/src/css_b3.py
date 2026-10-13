import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_USING_MQ = ("MDN — Using media queries", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries")
WEBDEV_MEDIA_QUERIES = ("web.dev — Learn Responsive Design: Media queries", "https://web.dev/learn/design/media-queries")
MDN_BEFORE = ("MDN — ::before", "https://developer.mozilla.org/en-US/docs/Web/CSS/::before")
WEBDEV_PSEUDO_ELEMENTS = ("web.dev — Learn CSS: Pseudo-elements", "https://web.dev/learn/css/pseudo-elements")
MDN_VAR = ("MDN — var()", "https://developer.mozilla.org/en-US/docs/Web/CSS/var")
MDN_TRANSITION = ("MDN — transition", "https://developer.mozilla.org/en-US/docs/Web/CSS/transition")
MDN_ANIMATION = ("MDN — animation", "https://developer.mozilla.org/en-US/docs/Web/CSS/animation")
MDN_REDUCED_MOTION = ("MDN — prefers-reduced-motion", "https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion")
MDN_STACKING = ("MDN — Stacking context", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Stacking_context")
WEBDEV_ZINDEX = ("web.dev — Learn CSS: Z-index and stacking contexts", "https://web.dev/learn/css/z-index")
MDN_PROPERTY = ("MDN — @property", "https://developer.mozilla.org/en-US/docs/Web/CSS/@property")
MDN_REGISTER = ("MDN — CSS.registerProperty()", "https://developer.mozilla.org/en-US/docs/Web/API/CSS/registerProperty_static")
MDN_OVERFLOW = ("MDN — overflow", "https://developer.mozilla.org/en-US/docs/Web/CSS/overflow")
MDN_OVERFLOW_WRAP = ("MDN — overflow-wrap", "https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap")
WCAG_REFLOW = ("W3C WAI — Understanding SC 1.4.10 Reflow", "https://www.w3.org/WAI/WCAG22/Understanding/reflow.html")
WEBDEV_COMPOSITOR = ("web.dev — Stick to compositor-only properties and manage layer count", "https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count")
MDN_HAS = ("MDN — :has() (performance considerations)", "https://developer.mozilla.org/en-US/docs/Web/CSS/:has")
WEBDEV_INP = ("web.dev — Interaction to Next Paint (INP)", "https://web.dev/articles/inp")

QUESTIONS = [
    # ------------------------------------------------------------------ css-007
    Q(
        id="css-007", sub="Media Queries", diff="easy", type="conceptual",
        prio="high", market="bangladesh", mins=4,
        tags=["media-queries", "mobile-first", "breakpoints", "responsive"],
        ver="CSS Media Queries Level 4 (range syntax supported in all modern browsers)", vs=False, status="stable",
        q_en=r"""What does "mobile-first" CSS mean, and how do you choose breakpoints? Which media features besides width are useful?""",
        q_bn=r""""Mobile-first" CSS মানে কী, আর breakpoint কীভাবে ঠিক করো? Width ছাড়া আর কোন media feature কাজের?""",
        a_en=r"""
            **Mobile-first** means the base styles (outside any media query) are for the **smallest screens**, and I add `min-width` media queries to *enhance* the layout as space grows. In Bangladesh most traffic is on phones, so the default experience should be the phone one, not a squeezed desktop.

            Benefits: simpler CSS (you add columns rather than undo them), small screens don't need overrides, and it nudges you toward progressive enhancement.

            **Breakpoints:** I choose them where the **content** breaks — when lines get too long or cards get too cramped — not by device names. I write them in `rem` (e.g. `48rem`), so they scale when a user increases their default font size.

            **Other useful features:** `hover` and `pointer` (don't rely on hover on touch devices), `prefers-reduced-motion`, `prefers-color-scheme`, and `orientation` in rare cases. The modern range syntax — `@media (width >= 48rem)` — works in all current browsers.
        """,
        a_bn=r"""
            **Mobile-first** মানে base style (কোনো media query-র বাইরে) হলো **সবচেয়ে ছোট screen**-এর জন্য, আর জায়গা বাড়ার সাথে সাথে layout *উন্নত* করতে আমি `min-width` media query যোগ করি। বাংলাদেশে বেশিরভাগ traffic phone থেকে আসে, তাই default অভিজ্ঞতা হওয়া উচিত phone-এর, চেপে ছোট করা desktop নয়।

            সুবিধা: CSS সহজ হয় (column বাতিল না করে যোগ করো), ছোট screen-এ override লাগে না, আর এটা progressive enhancement-এর দিকে ঠেলে দেয়।

            **Breakpoint:** device-এর নাম দেখে নয়, যেখানে **content** ভাঙে — line খুব লম্বা হয়ে যায় বা card খুব ঠাসাঠাসি হয় — সেখানে breakpoint দিই। এগুলো `rem`-এ লিখি (যেমন `48rem`), যাতে user default font size বাড়ালে breakpoint-ও সেই অনুপাতে বদলায়।

            **অন্যান্য কাজের feature:** `hover` আর `pointer` (touch device-এ hover-এর উপর ভরসা কোরো না), `prefers-reduced-motion`, `prefers-color-scheme`, আর কখনো কখনো `orientation`। আধুনিক range syntax — `@media (width >= 48rem)` — এখনকার সব browser-এ কাজ করে।
        """,
        ex_en=r"""
            - **The viewport meta tag is a prerequisite** — without `<meta name="viewport" content="width=device-width, initial-scale=1">`, phones report a desktop-like width and your media queries never match.
            - **`rem`/`em` in media queries** are based on the browser's default font size, not on a `font-size` you set on `html`, so they respect user settings.
            - **Desktop-first** (`max-width` queries) isn't wrong, but it usually means writing desktop styles and then undoing them — more CSS for the devices with the least power and slowest connections.
            - **Media queries vs container queries:** media queries for page-level layout and user preferences; container queries when a component should adapt to the space it's placed in.
        """,
        ex_bn=r"""
            - **Viewport meta tag পূর্বশর্ত** — `<meta name="viewport" content="width=device-width, initial-scale=1">` না থাকলে phone desktop-এর মতো width জানায়, আর তোমার media query কখনো match করে না।
            - **Media query-তে `rem`/`em`** browser-এর default font size-এর উপর নির্ভর করে, তুমি `html`-এ যে `font-size` দিয়েছ তার উপর নয় — তাই এগুলো user-এর setting মেনে চলে।
            - **Desktop-first** (`max-width` query) ভুল নয়, কিন্তু সাধারণত এর মানে desktop style লিখে তারপর সেগুলো বাতিল করা — যে device-এর শক্তি সবচেয়ে কম আর connection সবচেয়ে ধীর, তাদের জন্যই বেশি CSS।
            - **Media query বনাম container query:** page-level layout আর user preference-এর জন্য media query; কোনো component-কে তার বসানো জায়গা অনুযায়ী মানিয়ে নিতে হলে container query।
        """,
        tip_en=r"""Define mobile-first in one sentence, then say "breakpoints follow content, not devices". Mentioning `hover`/`pointer` queries shows you think about touch users, not just widths.""",
        tip_bn=r"""এক বাক্যে mobile-first-এর সংজ্ঞা দাও, তারপর বলো "breakpoint content অনুসরণ করে, device নয়"। `hover`/`pointer` query-র কথা বললে বোঝা যায় তুমি শুধু width নয়, touch user-দের কথাও ভাবো।""",
        mist_en=r"""Using device-named breakpoints ("iPhone", "iPad"), writing breakpoints in `px` only, relying on `:hover` for essential actions, or forgetting the viewport meta tag.""",
        mist_bn=r"""Device-এর নামে breakpoint ("iPhone", "iPad"), শুধু `px`-এ breakpoint লেখা, জরুরি action-এর জন্য `:hover`-এর উপর নির্ভর করা, অথবা viewport meta tag ভুলে যাওয়া।""",
        code=r"""
            /* Base: small screens, no media query */
            .products { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
            .filters  { display: none; }

            /* Enhance as space allows (content-based, in rem) */
            @media (width >= 48rem) {
              .products { grid-template-columns: repeat(3, 1fr); }
            }
            @media (width >= 64rem) {
              .layout  { display: grid; grid-template-columns: 16rem 1fr; gap: 24px; }
              .filters { display: block; }
            }

            /* Capability query: hover effects only where hover exists */
            @media (hover: hover) and (pointer: fine) {
              .card:hover { box-shadow: 0 4px 16px rgb(0 0 0 / 0.12); }
            }
        """,
        lang="css",
        follow=[
            ("How would you test your breakpoints with a user's larger default font size?", "User-এর বড় default font size-এ তোমার breakpoint কীভাবে test করবে?"),
            ("Why is relying on `:hover` risky on mobile?", "Mobile-এ `:hover`-এর উপর নির্ভর করা কেন ঝুঁকিপূর্ণ?"),
        ],
        related=["css-016", "css-021"],
        refs=[MDN_USING_MQ, WEBDEV_MEDIA_QUERIES],
    ),
    # ------------------------------------------------------------------ css-008
    Q(
        id="css-008", sub="Pseudo-classes and Pseudo-elements", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=2,
        tags=["pseudo-elements", "before", "content", "selectors"],
        ver="Version-independent (CSS)", vs=False, status="stable",
        q_en=r"""This should show a small red dot before the "New" badge, but nothing appears. Why?""",
        q_bn=r"""এখানে "New" badge-এর আগে একটা ছোট লাল বিন্দু দেখানোর কথা, কিন্তু কিছুই দেখা যাচ্ছে না। কেন?""",
        code=r"""
            <span class="badge">New</span>

            <style>
              .badge::before {
                display: inline-block;
                width: 8px;
                height: 8px;
                margin-right: 6px;
                border-radius: 50%;
                background: #e63946;
              }
            </style>
        """,
        lang="html",
        options=[
            ("The `content` property is missing, so the pseudo-element is never generated.", "`content` property নেই, তাই pseudo-element তৈরিই হয় না।"),
            ("`::before` doesn't work on inline elements like `<span>`; it needs a block element.", "`<span>`-এর মতো inline element-এ `::before` কাজ করে না; block element লাগে।"),
            ("Modern browsers only support the single-colon form `:before`.", "আধুনিক browser শুধু single-colon রূপ `:before` support করে।"),
            ("`border-radius: 50%` on an 8px box rounds it away to nothing.", "8px-এর box-এ `border-radius: 50%` দিলে সেটা গোল হতে হতে মিলিয়ে যায়।"),
        ],
        correct=0,
        a_en=r"""
            `::before` and `::after` are only generated when `content` has a value other than `none`/`normal`. For a purely decorative shape, `content: ""` is enough — the rest of the styles then apply to the generated box.
        """,
        a_bn=r"""
            `::before` আর `::after` তখনই তৈরি হয়, যখন `content`-এর value `none`/`normal` ছাড়া অন্য কিছু হয়। শুধু সাজানোর জন্য একটা আকৃতি হলে `content: ""` দিলেই যথেষ্ট — তারপর বাকি style-গুলো তৈরি হওয়া box-এ প্রয়োগ হয়।
        """,
        ex_en=r"""
            The tempting distractor is B, because there *is* a related rule: `::before`/`::after` don't render on **replaced or void elements** like `<img>` and `<input>`, which have no content box to insert into. A `<span>` is fine — and `display: inline-block` already takes care of `width`/`height` applying.

            C is backwards: the double colon is the modern syntax that distinguishes pseudo-*elements* (`::before`, `::marker`, `::placeholder`, `::selection`, `::backdrop`) from pseudo-*classes* (`:hover`, `:focus-visible`, `:nth-child()`). Browsers still accept the single colon for the four legacy pseudo-elements. D is wrong — 50% radius on a square makes a circle.

            Accessibility note: text in `content` can be read by screen readers, so keep meaningful content in the HTML and use pseudo-elements for decoration.
        """,
        ex_bn=r"""
            প্রলোভনজনক distractor B, কারণ এর সাথে সম্পর্কিত একটা নিয়ম *আছে*: `<img>` আর `<input>`-এর মতো **replaced বা void element**-এ `::before`/`::after` render হয় না, কারণ এদের ভেতরে বসানোর মতো content box নেই। `<span>`-এ কোনো সমস্যা নেই — আর `display: inline-block` থাকায় `width`/`height`-ও প্রয়োগ হয়।

            C উল্টো কথা: double colon হলো আধুনিক syntax, যা pseudo-*element* (`::before`, `::marker`, `::placeholder`, `::selection`, `::backdrop`)-কে pseudo-*class* (`:hover`, `:focus-visible`, `:nth-child()`) থেকে আলাদা করে। পুরোনো চারটা pseudo-element-এর জন্য browser এখনো single colon মেনে নেয়। D ভুল — বর্গাকার box-এ 50% radius দিলে বৃত্ত হয়।

            Accessibility-র কথা: `content`-এর text screen reader পড়তে পারে, তাই অর্থবহ content HTML-এ রাখো আর pseudo-element ব্যবহার করো সাজসজ্জার জন্য।
        """,
        tip_en=r"""Give the fix (`content: ""`) immediately, then explain pseudo-class vs pseudo-element in one line — "state vs part of an element".""",
        tip_bn=r"""সঙ্গে সঙ্গে সমাধান (`content: ""`) বলো, তারপর এক লাইনে pseudo-class বনাম pseudo-element ব্যাখ্যা করো — "অবস্থা বনাম element-এর একটা অংশ"।""",
        refs=[MDN_BEFORE, WEBDEV_PSEUDO_ELEMENTS],
    ),
    # ------------------------------------------------------------------ css-009
    Q(
        id="css-009", sub="CSS Variables", diff="easy", type="output",
        prio="high", market="both", mins=3,
        tags=["custom-properties", "var", "fallback", "inheritance", "output"],
        ver="Version-independent (CSS Custom Properties)", vs=False, status="stable",
        q_en=r"""What colour are the heading and the note?""",
        q_bn=r"""Heading আর note-এর রং কী হবে?""",
        code=r"""
            <div class="card">
              <h2 class="title">Eid Offer</h2>
              <p class="note">Ends today</p>
            </div>

            <style>
              :root  { --accent: blue; }
              .card  { --accent: green; }
              .title { color: var(--accent, red); }
              .note  { color: var(--muted, gray); }
            </style>
        """,
        lang="html",
        output=r"""
            .title → green
            .note  → gray
        """,
        a_en=r"""
            Custom properties are **inherited** and resolved on the element that uses them.
            - `.title` looks up `--accent`: the nearest ancestor that sets it is `.card` (green), which overrides `:root` (blue). The fallback `red` is only used when the property isn't defined at all, so the heading is **green**.
            - `.note` asks for `--muted`, which is never defined, so the fallback is used → **gray**.
        """,
        a_bn=r"""
            Custom property **inherit** হয়, আর যে element এটা ব্যবহার করে সেখানেই resolve হয়।
            - `.title` `--accent` খোঁজে: এটা set করেছে এমন সবচেয়ে কাছের ancestor হলো `.card` (green), যেটা `:root`-কে (blue) override করে। Fallback `red` তখনই ব্যবহার হয়, যখন property-টা একেবারেই define করা নেই — তাই heading **সবুজ (green)**।
            - `.note` চায় `--muted`, যেটা কোথাও define করা নেই, তাই fallback ব্যবহার হয় → **ধূসর (gray)**।
        """,
        ex_en=r"""
            - **Custom properties aren't global variables.** They're properties on elements that inherit like `color` does, which is why setting `--accent` on `.card` re-themes everything inside it — the basis of component theming and dark mode.
            - **The fallback is for "missing", not "wrong".** If `.card` set `--accent: 20px`, the heading would *not* turn red: `color: 20px` is invalid at computed-value time, so `color` behaves like `unset` and simply inherits the parent's text colour. If `--accent` were registered with `@property` and a `<color>` syntax, the bad declaration itself would be discarded: with `inherits: true` the heading would get the inherited `blue` from `:root`, and with `inherits: false` the declared `initial-value`.
            - **Fallbacks can nest:** `var(--accent, var(--brand, black))`.
            - **DevTools** shows the resolved value and where each custom property was defined, which makes debugging themes easy.
        """,
        ex_bn=r"""
            - **Custom property global variable নয়।** এগুলো element-এর property, যেগুলো `color`-এর মতোই inherit হয় — এজন্যই `.card`-এ `--accent` set করলে তার ভেতরের সবকিছুর theme বদলে যায়; component theming আর dark mode-এর ভিত্তি এটাই।
            - **Fallback হলো "নেই"-এর জন্য, "ভুল"-এর জন্য নয়।** `.card` যদি `--accent: 20px` set করত, heading তাহলেও লাল হতো *না*: `color: 20px` computed-value time-এ invalid, তাই `color` `unset`-এর মতো আচরণ করে আর শুধু parent-এর text colour inherit করে। `--accent`-কে যদি `@property` দিয়ে `<color>` syntax-সহ register করা থাকত, তাহলে ভুল declaration-টাই বাতিল হতো: `inherits: true` হলে heading `:root` থেকে inherit হওয়া `blue` পেত, আর `inherits: false` হলে ঘোষিত `initial-value`।
            - **Fallback nest করা যায়:** `var(--accent, var(--brand, black))`।
            - **DevTools** resolve হওয়া value আর প্রতিটা custom property কোথায় define করা হয়েছে তা দেখায়, ফলে theme debug করা সহজ।
        """,
        tip_en=r"""Say "custom properties inherit and resolve where they're used" before tracing. If there's time, the "fallback is for missing, not invalid" nuance is a great differentiator.""",
        tip_bn=r"""Trace করার আগে বলো "custom property inherit হয় আর যেখানে ব্যবহার হয় সেখানে resolve হয়"। সময় থাকলে "fallback হলো না-থাকার জন্য, invalid-এর জন্য নয়" — এই সূক্ষ্ম কথাটা তোমাকে আলাদা করে তুলবে।""",
        mist_en=r"""Answering blue because `:root` is "global", or red because a fallback was provided.""",
        mist_bn=r"""`:root` "global" বলে নীল বলা, অথবা fallback দেওয়া আছে বলে লাল বলা।""",
        follow=[
            ("What happens if `--accent` is set to an invalid colour value?", "`--accent`-এ invalid colour value দিলে কী হবে?"),
            ("How would you implement a dark theme using only custom properties?", "শুধু custom property দিয়ে dark theme কীভাবে implement করবে?"),
        ],
        related=["css-017", "css-003"],
        refs=[MDN_VAR],
    ),
    # ------------------------------------------------------------------ css-018
    Q(
        id="css-018", sub="Transitions and Animations", diff="medium", type="conceptual",
        prio="high", market="both", mins=6,
        tags=["transitions", "animations", "keyframes", "prefers-reduced-motion", "accessibility"],
        ver="CSS Transitions/Animations; @starting-style Baseline newly available; scroll-driven animations not Baseline (status as of Oct 2026)", vs=True, status="stable",
        q_en=r"""When do you use a CSS transition and when a keyframe animation? How do you make motion respect users who prefer reduced motion?""",
        q_bn=r"""কখন CSS transition আর কখন keyframe animation ব্যবহার করবে? যারা কম motion পছন্দ করে, সেই user-দের জন্য motion কীভাবে মানিয়ে নেবে?""",
        a_en=r"""
            - **Transitions** animate between **two states** when a property value changes — hover, focus, a class toggle. They need a trigger, run from the current value to the new one, and reverse naturally. Example: a button that scales slightly when pressed.
            - **Animations** (`@keyframes`) describe **multi-step** motion that can run on their own — on page load, in a loop, alternating, with delays and `animation-fill-mode`. Example: a loading spinner or a "pulse" on the cart badge after adding an item.

            For performance I animate `transform` and `opacity` wherever possible, since those can be handled by the compositor.

            **Reduced motion:** some users (for example people with vestibular disorders) enable "reduce motion" in their OS. I respect `prefers-reduced-motion` by making large or decorative motion **opt-in**: write it inside `@media (prefers-reduced-motion: no-preference)`. Essential feedback stays, but as a fade or instant change instead of sliding, zooming or parallax.
        """,
        a_bn=r"""
            - **Transition** কোনো property-র value বদলালে **দুটো অবস্থার** মাঝে animate করে — hover, focus, class toggle। এর একটা trigger লাগে, বর্তমান value থেকে নতুন value-তে যায়, আর স্বাভাবিকভাবে উল্টো দিকেও ফেরে। উদাহরণ: চাপ দিলে একটু ছোট হয়ে যাওয়া button।
            - **Animation** (`@keyframes`) **একাধিক ধাপের** motion বর্ণনা করে, যা নিজে নিজেই চলতে পারে — page load-এ, loop-এ, alternate করে, delay আর `animation-fill-mode`-সহ। উদাহরণ: loading spinner, বা item যোগ করার পর cart badge-এ একটা "pulse"।

            Performance-এর জন্য যেখানে সম্ভব `transform` আর `opacity` animate করি, কারণ এগুলো compositor সামলাতে পারে।

            **Reduced motion:** কিছু user (যেমন vestibular disorder আছে এমন মানুষ) তাদের OS-এ "reduce motion" চালু রাখে। আমি `prefers-reduced-motion` মেনে চলি — বড় বা শুধু সাজসজ্জার motion **opt-in** করে: সেগুলো `@media (prefers-reduced-motion: no-preference)`-এর ভেতরে লিখি। জরুরি feedback থাকে, তবে slide, zoom বা parallax-এর বদলে fade বা তাৎক্ষণিক পরিবর্তন হিসেবে।
        """,
        ex_en=r"""
            - **Reduced ≠ none.** A subtle opacity fade is usually fine; what hurts is large movement, zooming, parallax and auto-playing motion.
            - **The "global kill switch"** (`animation-duration: 0.01ms !important` inside `prefers-reduced-motion: reduce`) is a quick safety net. It uses `0.01ms` rather than `0` because a zero-duration transition never starts, so `transitionend` would never fire for scripts that wait on it (zero-duration animations still fire `animationend`).
            - **JavaScript-driven motion** must check too: `matchMedia('(prefers-reduced-motion: reduce)').matches` (and listen for changes) before running carousels, smooth scrolling or Web Animations API effects.
            - **Entry animations from `display: none`** used to need JavaScript. `@starting-style` (Baseline newly available) defines the "before" state for the first style update, and `transition-behavior: allow-discrete` lets `display`/`overlay` participate — useful for dialogs and popovers.
            - **Scroll-driven animations** (`animation-timeline: scroll()`/`view()`) are **not Baseline** yet (limited availability) — use them only as an enhancement behind `@supports`.
        """,
        ex_bn=r"""
            - **Reduced মানে none নয়।** হালকা একটা opacity fade সাধারণত ঠিক আছে; কষ্ট দেয় বড় নড়াচড়া, zoom, parallax আর নিজে নিজে চলা motion।
            - **"Global kill switch"** (`prefers-reduced-motion: reduce`-এর ভেতরে `animation-duration: 0.01ms !important`) দ্রুত একটা নিরাপত্তা জাল। এখানে `0` নয়, `0.01ms` ব্যবহার করা হয়, কারণ শূন্য duration-এর transition শুরুই হয় না, ফলে যেসব script `transitionend`-এর জন্য অপেক্ষা করে তাদের event কখনো fire হতো না (শূন্য duration-এর animation-এ অবশ্য `animationend` ঠিকই fire হয়)।
            - **JavaScript দিয়ে চালানো motion**-কেও check করতে হবে: carousel, smooth scrolling বা Web Animations API effect চালানোর আগে `matchMedia('(prefers-reduced-motion: reduce)').matches` দেখো (আর পরিবর্তনের জন্য listen করো)।
            - **`display: none` থেকে entry animation**-এর জন্য আগে JavaScript লাগত। `@starting-style` (Baseline newly available) প্রথম style update-এর "আগের" অবস্থা ঠিক করে, আর `transition-behavior: allow-discrete` `display`/`overlay`-কে transition-এ অংশ নিতে দেয় — dialog আর popover-এর জন্য কাজের।
            - **Scroll-driven animation** (`animation-timeline: scroll()`/`view()`) এখনো **Baseline নয়** (সীমিত support) — শুধু `@supports`-এর আড়ালে enhancement হিসেবে ব্যবহার করো।
        """,
        tip_en=r"""Frame it as "state change vs timeline". Then show reduced motion as a design decision (opt-in motion), not just a media query you remembered — and mention JavaScript animations need the check too.""",
        tip_bn=r"""এভাবে উপস্থাপন করো: "অবস্থার পরিবর্তন বনাম timeline"। তারপর reduced motion-কে শুধু মনে রাখা একটা media query হিসেবে নয়, একটা design সিদ্ধান্ত (opt-in motion) হিসেবে দেখাও — আর বলো যে JavaScript animation-এরও এই check লাগে।""",
        mist_en=r"""Animating `height`, `top` or `left` for routine effects, removing *all* feedback for reduced-motion users, using `0s` transition durations that stop `transitionend` from ever firing, or ignoring JavaScript-driven motion.""",
        mist_bn=r"""সাধারণ effect-এর জন্য `height`, `top` বা `left` animate করা, reduced-motion user-দের জন্য *সব* feedback সরিয়ে ফেলা, এমন `0s` transition duration ব্যবহার করা যাতে `transitionend` কখনো fire-ই হয় না, অথবা JavaScript দিয়ে চালানো motion উপেক্ষা করা।""",
        code=r"""
            /* Transition: two states, needs a trigger */
            .add-to-cart {
              transition: transform 150ms ease-out, background-color 150ms ease-out;
            }
            .add-to-cart:active { transform: scale(0.96); }

            /* Animation: multi-step, runs on its own */
            @keyframes pulse {
              0%, 100% { transform: scale(1); }
              50%      { transform: scale(1.15); }
            }

            /* Motion is opt-in */
            @media (prefers-reduced-motion: no-preference) {
              .cart-badge.updated { animation: pulse 400ms ease-in-out 2; }
              html { scroll-behavior: smooth; }
            }

            /* Safety net for third-party or legacy animations */
            @media (prefers-reduced-motion: reduce) {
              *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
              }
            }
        """,
        lang="css",
        follow=[
            ("How would you animate a `<dialog>` opening when it starts from `display: none`?", "`display: none` থেকে শুরু হওয়া একটা `<dialog>` খোলার animation কীভাবে করবে?"),
            ("Which properties are cheap to animate, and why?", "কোন property animate করা সস্তা, আর কেন?"),
        ],
        related=["css-024", "css-026"],
        refs=[MDN_TRANSITION, MDN_ANIMATION, MDN_REDUCED_MOTION],
    ),
    # ------------------------------------------------------------------ css-019
    Q(
        id="css-019", sub="Stacking Contexts", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["stacking-context", "z-index", "transform", "opacity"],
        ver="Version-independent (CSS)", vs=False, status="stable",
        q_en=r"""A dropdown inside the site header has `z-index: 9999` but still renders *under* the hero banner below it. While debugging, you check the header's styles. Which of these declarations does **not**, on its own, create a new stacking context?""",
        q_bn=r"""Site header-এর ভেতরের একটা dropdown-এ `z-index: 9999` দেওয়া, তবুও সেটা নিচের hero banner-এর *তলায়* দেখা যাচ্ছে। Debug করার সময় তুমি header-এর style দেখছ। নিচের কোন declaration একা একা নতুন stacking context তৈরি **করে না**?""",
        options=[
            ("`opacity: 0.99`", "`opacity: 0.99`"),
            ("`transform: translateZ(0)`", "`transform: translateZ(0)`"),
            ("`position: relative; z-index: auto;`", "`position: relative; z-index: auto;`"),
            ("`isolation: isolate`", "`isolation: isolate`"),
        ],
        correct=2,
        a_en=r"""
            `position: relative` with `z-index: auto` does **not** create a stacking context. The other three all do: `opacity` below 1, any `transform` other than `none` (even `translateZ(0)`), and `isolation: isolate` (whose only job is to create one).
        """,
        a_bn=r"""
            `z-index: auto`-সহ `position: relative` stacking context তৈরি **করে না**। বাকি তিনটা করে: 1-এর কম `opacity`, `none` ছাড়া যেকোনো `transform` (এমনকি `translateZ(0)`-ও), আর `isolation: isolate` (যার একমাত্র কাজই একটা stacking context তৈরি করা)।
        """,
        ex_en=r"""
            **Why the dropdown is stuck:** `z-index` only competes **within the same stacking context**. If the header creates one (say, via `transform` from a scroll animation, or `opacity: 0.99`), then `z-index: 9999` means "9999 *inside the header*". The header as a whole is then compared with the hero — and if the hero comes later in the DOM at the same level, it paints on top. Fix it by giving the header a `z-index` higher than the hero, removing the accidental stacking context, or rendering the dropdown in the top layer (the `popover` attribute).

            The tempting wrong answer is **B**: `translateZ(0)` is often added as a "GPU acceleration hack" without realising it creates a stacking context — and a containing block for `position: fixed` children.

            Other common creators: `position: fixed`/`sticky`; positioned elements with a non-`auto` `z-index`; flex/grid items with a non-`auto` `z-index`; `filter`, `backdrop-filter`, `mix-blend-mode`, `clip-path`, `mask`; `will-change` naming one of those properties; `contain: layout`/`paint`.
        """,
        ex_bn=r"""
            **Dropdown কেন আটকে আছে:** `z-index` শুধু **একই stacking context-এর ভেতরে** প্রতিযোগিতা করে। Header যদি একটা stacking context তৈরি করে (ধরো scroll animation-এর `transform` বা `opacity: 0.99` থেকে), তাহলে `z-index: 9999` মানে "*header-এর ভেতরে* 9999"। তখন পুরো header-কে hero-র সাথে তুলনা করা হয় — আর একই স্তরে DOM-এ hero পরে এলে সেটাই উপরে আঁকা হয়। সমাধান: header-কে hero-র চেয়ে বড় `z-index` দাও, অনিচ্ছাকৃত stacking context সরাও, অথবা dropdown-কে top layer-এ render করো (`popover` attribute)।

            প্রলোভনজনক ভুল উত্তর **B**: `translateZ(0)` প্রায়ই "GPU acceleration hack" হিসেবে যোগ করা হয়, না বুঝেই যে এটা একটা stacking context তৈরি করে — আর `position: fixed` children-এর জন্য একটা containing block-ও।

            আরও প্রচলিত কারণ: `position: fixed`/`sticky`; `auto` ছাড়া `z-index`-সহ positioned element; `auto` ছাড়া `z-index`-সহ flex/grid item; `filter`, `backdrop-filter`, `mix-blend-mode`, `clip-path`, `mask`; এগুলোর কোনো property-র নাম দেওয়া `will-change`; `contain: layout`/`paint`।
        """,
        tip_en=r"""After answering, explain why `9999` "doesn't work" — "z-index is local to its stacking context". That explanation is what interviewers really want from this question.""",
        tip_bn=r"""উত্তর দেওয়ার পর ব্যাখ্যা করো কেন `9999` "কাজ করে না" — "z-index তার stacking context-এর ভেতরেই সীমাবদ্ধ"। এই প্রশ্ন থেকে interviewer আসলে এই ব্যাখ্যাটাই চায়।""",
        refs=[MDN_STACKING, WEBDEV_ZINDEX],
    ),
    # ------------------------------------------------------------------ css-026
    Q(
        id="css-026", sub="CSS Variables", diff="hard", type="conceptual",
        prio="medium", market="international", mins=7,
        tags=["property", "custom-properties", "houdini", "animation"],
        ver="CSS Properties and Values API; @property Baseline newly available (Jul 2024)", vs=True, status="stable",
        q_en=r"""What does `@property` add over a normal custom property? Show a case where it's required, and explain the trade-offs.""",
        q_bn=r"""সাধারণ custom property-র তুলনায় `@property` কী যোগ করে? এমন একটা উদাহরণ দেখাও যেখানে এটা ছাড়া চলে না, আর trade-off-গুলো ব্যাখ্যা করো।""",
        a_en=r"""
            `@property` **registers** a custom property with a **type** (`syntax`), an **`inherits`** flag and an **`initial-value`**. Unregistered custom properties are just token streams to the browser; once registered, the browser knows what the value *is*.

            What that unlocks:
            - **Animation and transitions.** The browser can interpolate a registered `<angle>`, `<length>`, `<percentage>` or `<color>`. An unregistered custom property can only flip from one value to the other. The classic case is animating a gradient — gradients can't be transitioned directly, but a registered `--angle` or `--progress` used *inside* the gradient can.
            - **Type safety.** An invalid value (say, `--progress: red`) is discarded for the registered property, which falls back to its `initial-value` (with `inherits: false`, as below) or to the inherited value (with `inherits: true`), instead of leaving the consuming property "invalid at computed-value time".
            - **Controlled inheritance.** `inherits: false` stops the value flowing down the tree, which is clearer for component-local values and avoids unnecessary style recalculation.
            - **Computed values.** A registered `<length>` is computed (e.g. `2em` becomes pixels), so `getComputedStyle` returns a usable value.

            The JavaScript equivalent is `CSS.registerProperty()`. `@property` has been Baseline newly available since July 2024; in older browsers it degrades to a normal custom property — the animation simply jumps — so treat it as an enhancement.
        """,
        a_bn=r"""
            `@property` একটা custom property-কে একটা **type** (`syntax`), একটা **`inherits`** flag আর একটা **`initial-value`**-সহ **register** করে। Register না করা custom property browser-এর কাছে শুধুই token-এর ধারা; register করার পর browser জানে value-টা আসলে *কী*।

            এতে যা সম্ভব হয়:
            - **Animation আর transition।** Browser register করা `<angle>`, `<length>`, `<percentage>` বা `<color>`-এর মাঝামাঝি মান হিসাব (interpolate) করতে পারে। Register না করা custom property শুধু এক value থেকে আরেক value-তে লাফ দিতে পারে। Classic উদাহরণ হলো gradient animate করা — gradient সরাসরি transition করা যায় না, কিন্তু gradient-এর *ভেতরে* ব্যবহৃত register করা `--angle` বা `--progress` করা যায়।
            - **Type safety।** Invalid value দিলে (ধরো `--progress: red`) register করা property সেটা বাতিল করে তার `initial-value`-তে (`inherits: false` হলে, নিচের উদাহরণের মতো) বা inherit হওয়া value-তে (`inherits: true` হলে) ফিরে যায়, ব্যবহারকারী property-কে "invalid at computed-value time" অবস্থায় ফেলে রাখে না।
            - **নিয়ন্ত্রিত inheritance।** `inherits: false` দিলে value tree ধরে নিচে নামে না — component-এর নিজস্ব value-র জন্য এটা বেশি স্পষ্ট, আর অপ্রয়োজনীয় style recalculation-ও এড়ায়।
            - **Computed value।** Register করা `<length>` compute হয়ে যায় (যেমন `2em` pixel হয়ে যায়), তাই `getComputedStyle` ব্যবহারযোগ্য value দেয়।

            JavaScript-এ এর সমতুল্য হলো `CSS.registerProperty()`। `@property` July 2024 থেকে Baseline newly available; পুরোনো browser-এ এটা সাধারণ custom property-তে নেমে আসে — animation শুধু লাফ দেয় — তাই এটাকে enhancement হিসেবে ব্যবহার করো।
        """,
        ex_en=r"""
            **Rules that trip people up:**
            - `syntax` and `inherits` are required; `initial-value` is required unless `syntax` is `"*"`. A missing required descriptor makes the whole rule invalid and silently ignored.
            - `initial-value` must be computationally independent — `10px` is fine, `3em` is not.
            - Registration is global per document; registering the same name twice with different definitions leads to confusing results, so keep registrations in one shared file.

            **Trade-offs:** registered properties are less flexible (you can't put arbitrary tokens in them), and animating a registered custom property on `:root` with `inherits: true` restyles the whole tree every frame — keep animated properties `inherits: false` and set them on the element that animates. Gradient animation still repaints every frame, so use it for small elements, not full-page backgrounds, and respect `prefers-reduced-motion`.
        """,
        ex_bn=r"""
            **যে নিয়মগুলোতে মানুষ হোঁচট খায়:**
            - `syntax` আর `inherits` বাধ্যতামূলক; `syntax` যদি `"*"` না হয়, তাহলে `initial-value`-ও বাধ্যতামূলক। বাধ্যতামূলক descriptor না থাকলে পুরো rule invalid হয়ে চুপচাপ উপেক্ষিত হয়।
            - `initial-value` অবশ্যই computationally independent হতে হবে — `10px` চলবে, `3em` চলবে না।
            - Registration পুরো document-এর জন্য global; একই নাম দুবার ভিন্ন সংজ্ঞায় register করলে বিভ্রান্তিকর ফল হয়, তাই registration-গুলো একটা shared file-এ রাখো।

            **Trade-off:** register করা property কম নমনীয় (যেকোনো token রাখা যায় না), আর `:root`-এ `inherits: true`-সহ register করা custom property animate করলে প্রতি frame-এ পুরো tree-র style আবার হিসাব হয় — animate করা property `inherits: false` রাখো আর যে element animate করে সেখানেই set করো। Gradient animation তবুও প্রতি frame-এ repaint করে, তাই পুরো page-এর background-এ নয়, ছোট element-এ ব্যবহার করো, আর `prefers-reduced-motion` মেনে চলো।
        """,
        tip_en=r"""Lead with the one thing you *can't* do without it — animating a value inside a gradient — then list type safety and inheritance control. Mentioning the Baseline status and graceful degradation shows production thinking.""",
        tip_bn=r"""যেটা এটা ছাড়া *করা যায় না* — gradient-এর ভেতরের value animate করা — সেটা দিয়ে শুরু করো, তারপর type safety আর inheritance নিয়ন্ত্রণের কথা বলো। Baseline status আর graceful degradation-এর কথা বললে production-এর মতো চিন্তা বোঝা যায়।""",
        mist_en=r"""Forgetting `inherits` or `initial-value` (the rule is silently ignored), using `3em` as an initial value, or expecting unregistered custom properties to animate smoothly.""",
        mist_bn=r"""`inherits` বা `initial-value` ভুলে যাওয়া (rule চুপচাপ উপেক্ষিত হয়), initial value হিসেবে `3em` দেওয়া, অথবা register না করা custom property মসৃণভাবে animate হবে বলে আশা করা।""",
        code=r"""
            @property --progress {
              syntax: '<percentage>';
              inherits: false;
              initial-value: 0%;
            }

            /* Delivery progress bar: the gradient stop animates smoothly */
            .delivery-bar {
              height: 8px;
              border-radius: 4px;
              background: linear-gradient(to right, #0b6e4f var(--progress), #e0e0e0 var(--progress));
              transition: --progress 600ms ease-out;
            }
            .delivery-bar[data-step="packed"]  { --progress: 33%; }
            .delivery-bar[data-step="shipped"] { --progress: 66%; }
            .delivery-bar[data-step="done"]    { --progress: 100%; }

            @media (prefers-reduced-motion: reduce) {
              .delivery-bar { transition: none; }
            }
        """,
        lang="css",
        follow=[
            ("Why can't you transition `background: linear-gradient(...)` directly?", "`background: linear-gradient(...)` সরাসরি transition করা যায় না কেন?"),
            ("When would you use `CSS.registerProperty()` instead of `@property`?", "কখন `@property`-র বদলে `CSS.registerProperty()` ব্যবহার করবে?"),
        ],
        related=["css-017", "css-018"],
        refs=[MDN_PROPERTY, MDN_REGISTER],
    ),
    # ------------------------------------------------------------------ css-027
    Q(
        id="css-027", sub="Layout Debugging", diff="hard", type="scenario",
        prio="high", market="both", mins=8,
        tags=["overflow", "debugging", "devtools", "responsive", "mobile"],
        ver="Version-independent (CSS; overflow: clip supported in all modern browsers)", vs=False, status="stable",
        q_en=r"""On phones, a product page can be swiped sideways and shows blank space on the right. It's not obvious which element causes it. How do you find the culprit, what are the usual causes, and how do you fix it properly?""",
        q_bn=r"""Phone-এ একটা product page পাশে swipe করা যায় আর ডান দিকে ফাঁকা জায়গা দেখা যায়। কোন element এর জন্য দায়ী তা স্পষ্ট নয়। কীভাবে দায়ী element খুঁজে বের করবে, সাধারণ কারণগুলো কী, আর সঠিকভাবে কীভাবে ঠিক করবে?""",
        a_en=r"""
            **1. Reproduce:** DevTools device mode at 360px and 320px (WCAG's reflow criterion expects content to work at 320 CSS px without horizontal scrolling).

            **2. Find the culprit — systematically:**
            - Temporarily add `* { outline: 1px solid red; }` — boxes sticking out past the right edge become obvious.
            - Or run a snippet that lists every element whose box extends beyond the viewport (see the code), then inspect the outermost one.
            - Delete or hide sections in the Elements panel until the scrollbar disappears (binary search).

            **3. Usual causes:**
            - fixed widths (`width: 400px`, `min-width` on a table or iframe);
            - `width: 100vw` (includes the scrollbar width on desktop, so it's wider than the layout viewport);
            - long unbreakable strings — URLs, emails, tracking IDs;
            - flex/grid items stuck at `min-width: auto`;
            - images, videos, iframes or tables without `max-width: 100%`;
            - off-canvas menus hidden with `transform: translateX(100%)` or negative margins — transformed boxes still extend the scrollable area.

            **4. Fix the cause, not the symptom:** `max-width: 100%`, `min-width: 0` / `minmax(0, 1fr)`, `overflow-wrap: anywhere` for long strings, wrap wide tables in a scrollable container, and build off-canvas menus with `position: fixed` (fixed boxes don't extend the page's scrollable area) or set them to `display: none` when closed. I avoid `overflow-x: hidden` on `body`/`html` as a blanket fix: it hides content, breaks `position: sticky` as soon as it lands on a wrapper or on both `html` and `body` (on `body` alone it propagates to the viewport), and doesn't reliably stop sideways panning on every mobile browser. If clipping is truly intended, I use `overflow-x: clip` on the specific wrapper.
        """,
        a_bn=r"""
            **1. সমস্যাটা আবার ঘটাও:** DevTools device mode-এ 360px আর 320px-এ দেখো (WCAG-এর reflow criterion আশা করে 320 CSS px-এ horizontal scroll ছাড়াই content কাজ করবে)।

            **2. দায়ী element খোঁজো — পদ্ধতিগতভাবে:**
            - সাময়িকভাবে `* { outline: 1px solid red; }` যোগ করো — ডান দিকের কিনারা পেরিয়ে যাওয়া box-গুলো চোখে পড়বে।
            - অথবা একটা snippet চালাও, যেটা viewport-এর বাইরে বেরিয়ে যাওয়া প্রতিটা element-এর তালিকা দেয় (code দেখো), তারপর সবচেয়ে বাইরেরটা inspect করো।
            - Scrollbar না যাওয়া পর্যন্ত Elements panel-এ section-গুলো delete বা hide করতে থাকো (binary search)।

            **3. সাধারণ কারণ:**
            - নির্দিষ্ট width (`width: 400px`, table বা iframe-এ `min-width`);
            - `width: 100vw` (desktop-এ scrollbar-এর width-ও এর মধ্যে ধরা হয়, তাই এটা layout viewport-এর চেয়ে চওড়া);
            - ভাঙা যায় না এমন লম্বা string — URL, email, tracking ID;
            - `min-width: auto`-তে আটকে থাকা flex/grid item;
            - `max-width: 100%` ছাড়া image, video, iframe বা table;
            - `transform: translateX(100%)` বা negative margin দিয়ে লুকানো off-canvas menu — transform করা box-ও scroll করা যায় এমন এলাকা বাড়িয়ে দেয়।

            **4. উপসর্গ নয়, কারণ ঠিক করো:** `max-width: 100%`, `min-width: 0` / `minmax(0, 1fr)`, লম্বা string-এর জন্য `overflow-wrap: anywhere`, চওড়া table-কে scroll করা যায় এমন container-এ রাখা, আর off-canvas menu `position: fixed` দিয়ে বানানো (fixed box page-এর scroll করা যায় এমন এলাকা বাড়ায় না) অথবা বন্ধ অবস্থায় `display: none` করে দেওয়া। ঢালাও সমাধান হিসেবে আমি `body`/`html`-এ `overflow-x: hidden` এড়িয়ে চলি: এটা content লুকায়, কোনো wrapper-এ বা `html` আর `body` দুটোতেই দিলে `position: sticky` ভেঙে দেয় (শুধু `body`-তে দিলে সেটা viewport-এ চলে যায়), আর সব mobile browser-এ পাশে সরে যাওয়া নির্ভরযোগ্যভাবে থামায় না। সত্যিই clip করতে চাইলে নির্দিষ্ট wrapper-এ `overflow-x: clip` ব্যবহার করি।
        """,
        ex_en=r"""
            - **Why `100vw` bites:** on desktop browsers with classic scrollbars, `100vw` is the viewport *including* the scrollbar, so a "full-bleed" section is a few pixels wider than the page. Use `width: 100%` or let the element stretch naturally.
            - **`overflow: hidden` vs `overflow: clip`:** `hidden` turns the element into a scroll container (programmatically scrollable, and it becomes the reference for `position: sticky` descendants); `clip` just clips painting without creating a scroll container.
            - **User-generated content** (seller descriptions, addresses, long Bangla or English words without spaces) is the most common source in e-commerce — defensive `overflow-wrap: anywhere` on text containers prevents a whole class of bugs.
            - **Prevent regressions:** add a visual regression test at 320px, and a lint rule or code review checklist item against fixed pixel widths on layout elements.
        """,
        ex_bn=r"""
            - **`100vw` কেন বিপদে ফেলে:** classic scrollbar থাকা desktop browser-এ `100vw` হলো scrollbar-*সহ* viewport, তাই একটা "full-bleed" section page-এর চেয়ে কয়েক pixel চওড়া হয়। `width: 100%` ব্যবহার করো, অথবা element-কে স্বাভাবিকভাবে প্রসারিত হতে দাও।
            - **`overflow: hidden` বনাম `overflow: clip`:** `hidden` element-কে scroll container বানিয়ে দেয় (programmatically scroll করা যায়, আর `position: sticky` descendant-দের reference হয়ে যায়); `clip` scroll container না বানিয়ে শুধু আঁকার অংশ কেটে দেয়।
            - **User-এর তৈরি content** (seller-এর description, address, space ছাড়া লম্বা Bangla বা English শব্দ) e-commerce-এ সবচেয়ে সাধারণ উৎস — text container-এ সতর্কতামূলক `overflow-wrap: anywhere` দিলে এক শ্রেণির bug পুরোপুরি এড়ানো যায়।
            - **আবার যেন না হয়:** 320px-এ একটা visual regression test যোগ করো, আর layout element-এ fixed pixel width-এর বিরুদ্ধে একটা lint rule বা code review checklist রাখো।
        """,
        tip_en=r"""Show a *method* (reproduce → locate → classify → fix root cause → prevent regressions). The snippet and the "don't just `overflow-x: hidden` the body" stance signal real debugging experience.""",
        tip_bn=r"""একটা *পদ্ধতি* দেখাও (আবার ঘটাও → খুঁজে বের করো → শ্রেণিবিভাগ করো → মূল কারণ ঠিক করো → regression ঠেকাও)। Snippet-টা আর "শুধু body-তে `overflow-x: hidden` দিও না" অবস্থান — দুটোই বাস্তব debugging অভিজ্ঞতার ইঙ্গিত দেয়।""",
        mist_en=r"""Slapping `overflow-x: hidden` on `body`/`html`, using `100vw` for full-width sections, or hunting randomly instead of measuring element boxes.""",
        mist_bn=r"""`body`/`html`-এ `overflow-x: hidden` চাপিয়ে দেওয়া, full-width section-এর জন্য `100vw` ব্যবহার করা, অথবা element-এর box না মেপে এলোমেলোভাবে খোঁজা।""",
        code=r"""
            // Paste into the DevTools console at a narrow viewport
            const vw = document.documentElement.clientWidth;
            for (const el of document.querySelectorAll('body *')) {
              const r = el.getBoundingClientRect();
              if (r.right > vw + 1 || r.left < -1) {
                console.log(el, `left=${Math.round(r.left)} right=${Math.round(r.right)}`);
              }
            }
        """,
        lang="javascript",
        extra=[dict(
            lang="css",
            src=r"""
                img, video, iframe { max-width: 100%; height: auto; }
                .content, .product-description { overflow-wrap: anywhere; }
                .layout > * { min-width: 0; }                 /* flex/grid children */
                .table-scroll { overflow-x: auto; }            /* wrap wide tables */
                .full-bleed { width: 100%; }                   /* not 100vw */
                .off-canvas { position: fixed; inset-block: 0; right: 0; transform: translateX(100%); } /* fixed: no page overflow */
                .page { overflow-x: clip; }                    /* only if clipping is really intended */
            """,
            label_en="Typical root-cause fixes",
            label_bn="মূল কারণের সাধারণ সমাধান",
        )],
        follow=[
            ("Why does `overflow-x: hidden` on an ancestor break `position: sticky`?", "Ancestor-এ `overflow-x: hidden` দিলে `position: sticky` কেন ভেঙে যায়?"),
            ("How would you stop this class of bug from coming back?", "এই ধরনের bug যাতে আবার না আসে, তা কীভাবে নিশ্চিত করবে?"),
        ],
        related=["css-014", "css-020"],
        refs=[MDN_OVERFLOW, MDN_OVERFLOW_WRAP, WCAG_REFLOW],
    ),
    # ------------------------------------------------------------------ css-031
    Q(
        id="css-031", sub="Performance", diff="extreme", type="security-performance",
        prio="medium", market="international", mins=20,
        tags=["performance", "paint", "compositing", "will-change", "inp", "has"],
        ver="Version-independent concept (browser rendering); content-visibility Baseline newly available", vs=False, status="stable",
        q_en=r"""After a visual redesign, the product listing page on mid-range Android phones scrolls at around 20 fps, and Interaction to Next Paint got worse when opening the filter panel. The redesign added: a sticky header with `backdrop-filter: blur(20px)`, cards with a large spread `box-shadow` that animates on hover, `will-change: transform` on every card "for smoothness", `filter: drop-shadow()` on product images, and the rule `body:has(.filters-open) .card { … }`. Walk me through your investigation and fixes.""",
        q_bn=r"""একটা visual redesign-এর পর mid-range Android phone-এ product listing page প্রায় 20 fps-এ scroll করছে, আর filter panel খোলার সময় Interaction to Next Paint খারাপ হয়েছে। Redesign-এ যোগ হয়েছে: `backdrop-filter: blur(20px)`-সহ sticky header, hover-এ animate হওয়া বড় spread-এর `box-shadow`-যুক্ত card, "মসৃণতার জন্য" প্রতিটা card-এ `will-change: transform`, product image-এ `filter: drop-shadow()`, আর rule `body:has(.filters-open) .card { … }`। তোমার তদন্ত আর সমাধান ধাপে ধাপে বলো।""",
        a_en=r"""
            This is advanced material; I'd treat it as a performance incident: measure, attribute, fix, verify.

            **Investigate**
            - Profile on a **real device** via remote debugging (plus CPU throttling in DevTools). In the Performance panel, look at frame timing during scroll: are frames dropped because of main-thread work, **Paint**, or **compositing/raster** on the GPU?
            - Record the filter-panel interaction: a large **Recalculate Style** block right after the class toggle points at selector invalidation.
            - Rendering tab: **Paint flashing** (what repaints on scroll) and **Layer borders**; the Layers panel shows layer count and memory.

            **Likely culprits and fixes**
            1. **`will-change: transform` on every card** → hundreds of compositor layers, high GPU memory, and slower compositing — plus each card becomes a stacking context and containing block. Remove it; the browser promotes elements while they're actually animating.
            2. **`backdrop-filter: blur(20px)` on a sticky header** → the content behind it must be re-blurred every scroll frame, expensive on mobile GPUs. Use a smaller radius, a smaller blurred area, or an opaque/semi-opaque background on this page.
            3. **Animating a large `box-shadow` on hover** → repaints every frame. Put the shadow on a pseudo-element and animate its `opacity` (compositor-friendly), and only apply hover effects under `@media (hover: hover)`.
            4. **`filter: drop-shadow()` on many images** → expensive paint per image. Bake the shadow into the asset or use a cheap `box-shadow` on the wrapper.
            5. **`body:has(.filters-open) .card`** → toggling a class anywhere under `body` makes the browser re-evaluate the `:has()` anchor and restyle every card. Toggle a class on the listing container itself (`.listing.filters-open .card`) or scope `:has()` to a small container.
            6. **Long list:** `content-visibility: auto` with `contain-intrinsic-size` on card groups so off-screen groups skip layout and paint; `contain: content` on cards to limit invalidation.

            **Verify:** compare traces before/after on the same device and watch field INP and scroll-jank metrics after release.
        """,
        a_bn=r"""
            এটা advanced বিষয়; আমি একে একটা performance incident হিসেবে দেখব: মাপো, দায় নির্ধারণ করো, ঠিক করো, যাচাই করো।

            **তদন্ত**
            - Remote debugging দিয়ে **আসল device**-এ profile করো (সাথে DevTools-এ CPU throttling)। Performance panel-এ scroll-এর সময় frame timing দেখো: frame কি main thread-এর কাজের জন্য, **Paint**-এর জন্য, নাকি GPU-তে **compositing/raster**-এর জন্য বাদ পড়ছে?
            - Filter panel-এর interaction record করো: class toggle-এর ঠিক পরে বড় **Recalculate Style** block মানে selector invalidation-ই সমস্যা।
            - Rendering tab: **Paint flashing** (scroll-এ কী আবার paint হচ্ছে) আর **Layer borders**; Layers panel layer-এর সংখ্যা আর memory দেখায়।

            **সম্ভাব্য দোষী আর সমাধান**
            1. **প্রতিটা card-এ `will-change: transform`** → শত শত compositor layer, বেশি GPU memory, আর ধীর compositing — সাথে প্রতিটা card stacking context আর containing block হয়ে যায়। এটা সরাও; element সত্যিই animate হওয়ার সময় browser নিজেই promote করে।
            2. **Sticky header-এ `backdrop-filter: blur(20px)`** → প্রতি scroll frame-এ পেছনের content আবার blur করতে হয়, mobile GPU-তে যা ব্যয়বহুল। ছোট radius, ছোট blur এলাকা, অথবা এই page-এ অস্বচ্ছ/আধা-স্বচ্ছ background ব্যবহার করো।
            3. **Hover-এ বড় `box-shadow` animate করা** → প্রতি frame-এ repaint। Shadow একটা pseudo-element-এ রেখে তার `opacity` animate করো (compositor-বান্ধব), আর hover effect শুধু `@media (hover: hover)`-এর ভেতরে দাও।
            4. **অনেক image-এ `filter: drop-shadow()`** → প্রতিটা image-এ ব্যয়বহুল paint। Shadow asset-এর মধ্যেই বসিয়ে দাও, বা wrapper-এ সস্তা `box-shadow` ব্যবহার করো।
            5. **`body:has(.filters-open) .card`** → `body`-র নিচে কোথাও class toggle হলেই browser-কে `:has()` anchor আবার যাচাই করে প্রতিটা card-এর style আবার হিসাব করতে হয়। Listing container-এই class toggle করো (`.listing.filters-open .card`), অথবা `:has()`-কে ছোট container-এ সীমিত রাখো।
            6. **লম্বা list:** card group-এ `contain-intrinsic-size`-সহ `content-visibility: auto`, যাতে screen-এর বাইরের group layout আর paint এড়িয়ে যায়; invalidation সীমিত রাখতে card-এ `contain: content`।

            **যাচাই:** একই device-এ আগে-পরে trace তুলনা করো, আর release-এর পর field INP আর scroll jank-এর metric নজরে রাখো।
        """,
        ex_en=r"""
            **Why mid-range Android suffers most:** less GPU memory and fill-rate, slower CPUs, and high-DPR screens mean every blurred or shadowed pixel costs more. A redesign that's smooth on a designer's laptop can be unusable on the devices most of your BD customers use.

            **Trade-offs to discuss with design:**
            - Glassmorphism (`backdrop-filter`) is a visual choice with a real runtime cost — offer a cheaper variant on long, scroll-heavy pages.
            - Removing `will-change` might cause a tiny first-frame hitch on hover; that's far cheaper than hundreds of permanent layers.
            - `content-visibility` can make the scrollbar "jump" if `contain-intrinsic-size` estimates are poor; `auto` remembers the last rendered size to reduce this.

            **Prevent it next time:** a performance checklist for design reviews ("expensive effects": blur, large shadows, filters, layer promotion), a lab budget for scroll and interaction traces in CI, and RUM dashboards segmented by device class.
        """,
        ex_bn=r"""
            **Mid-range Android সবচেয়ে বেশি ভোগে কেন:** কম GPU memory আর fill-rate, ধীর CPU, আর high-DPR screen মানে প্রতিটা blur বা shadow-যুক্ত pixel-এর খরচ বেশি। Designer-এর laptop-এ মসৃণ একটা redesign তোমার বেশিরভাগ বাংলাদেশি customer-এর device-এ অচল হয়ে যেতে পারে।

            **Design team-এর সাথে যেসব trade-off আলোচনা করা উচিত:**
            - Glassmorphism (`backdrop-filter`) একটা visual পছন্দ, যার runtime খরচ বাস্তব — লম্বা, scroll-ভারী page-এ একটা সস্তা বিকল্প দাও।
            - `will-change` সরালে hover-এ প্রথম frame-এ সামান্য একটা ঝাঁকুনি হতে পারে; শত শত স্থায়ী layer-এর তুলনায় সেটা অনেক সস্তা।
            - `contain-intrinsic-size`-এর আন্দাজ খারাপ হলে `content-visibility`-র কারণে scrollbar "লাফাতে" পারে; `auto` শেষবার render হওয়া মাপ মনে রেখে এটা কমায়।

            **পরেরবার যেন না হয়:** design review-এর জন্য একটা performance checklist ("ব্যয়বহুল effect": blur, বড় shadow, filter, layer promotion), CI-তে scroll আর interaction trace-এর lab budget, আর device শ্রেণি অনুযায়ী ভাগ করা RUM dashboard।
        """,
        tip_en=r"""Don't jump straight to fixes. Say how you'd *attribute* the cost (main thread vs paint vs compositor) first, then go through the suspects in order of likely impact. Tying each fix to the pipeline stage it relieves shows real understanding.""",
        tip_bn=r"""সরাসরি সমাধানে ঝাঁপিয়ে পোড়ো না। আগে বলো খরচটা কোথায় হচ্ছে তা কীভাবে *নির্ধারণ* করবে (main thread বনাম paint বনাম compositor), তারপর সম্ভাব্য প্রভাবের ক্রমে সন্দেহভাজনদের ধরে এগোও। প্রতিটা সমাধানকে pipeline-এর যে ধাপে স্বস্তি দেয় তার সাথে যুক্ত করলে আসল বোঝাপড়া প্রকাশ পায়।""",
        mist_en=r"""Adding even more `will-change` or `translateZ(0)` to "force GPU", profiling only on a desktop, fixing all suspects at once without measuring which mattered, or assuming `:has()` cost is negligible at `body` level.""",
        mist_bn=r""""GPU জোর করে চালাতে" আরও `will-change` বা `translateZ(0)` যোগ করা, শুধু desktop-এ profile করা, কোনটা আসলে দায়ী তা না মেপে সব সন্দেহভাজন একসাথে ঠিক করা, অথবা `body` level-এ `:has()`-এর খরচ নগণ্য বলে ধরে নেওয়া।""",
        code=r"""
            /* Shadow on hover without repainting every frame */
            .card { position: relative; transition: transform 200ms ease-out; }
            .card::after {
              content: "";
              position: absolute;
              inset: 0;
              border-radius: inherit;
              box-shadow: 0 12px 32px rgb(0 0 0 / 0.18);
              opacity: 0;
              transition: opacity 200ms ease-out;
              pointer-events: none;
            }
            @media (hover: hover) {
              .card:hover { transform: translateY(-2px); }
              .card:hover::after { opacity: 1; }
            }

            /* Scope state to the listing, not body:has(...) */
            .listing.filters-open .card { opacity: 0.6; }

            /* Cheaper header on this page */
            .site-header { background: rgb(255 255 255 / 0.96); }

            /* Off-screen card groups skip layout and paint */
            .card-group {
              content-visibility: auto;
              contain-intrinsic-size: auto 900px;
            }
        """,
        lang="css",
        follow=[
            ("How would you convince the design team to drop or tone down `backdrop-filter`?", "Design team-কে `backdrop-filter` বাদ দিতে বা কমাতে কীভাবে রাজি করাবে?"),
            ("How do you tell from a trace whether jank is caused by paint or by compositing?", "Trace দেখে কীভাবে বুঝবে jank paint-এর কারণে নাকি compositing-এর কারণে?"),
        ],
        related=["css-024", "css-013"],
        refs=[WEBDEV_COMPOSITOR, MDN_HAS, WEBDEV_INP],
    ),
]

if __name__ == "__main__":
    save("css", "b3", QUESTIONS)
