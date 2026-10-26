import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

VER = "Version-independent concept (CSS Snapshot)"

QUESTIONS = [
    # ------------------------------------------------------------------ css-q01
    Q(
        id="css-q01", sub="Box Model", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["display", "block", "inline", "inline-block"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `display: block`, `inline` and `inline-block`?""",
        q_bn=r"""`display: block`, `inline` আর `inline-block`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""A `block` box starts on a new line and takes the full available width, and `width`, `height` and all margins apply. An `inline` box flows inside a line of text: `width` and `height` are ignored and vertical margins don't push other lines. `inline-block` sits in the line like text but accepts `width`, `height`, margin and padding like a block.""",
        a_bn=r"""`block` box নতুন line-এ শুরু হয় আর পুরো জায়গার width নেয়, এতে `width`, `height` আর সব margin কাজ করে। `inline` box text-এর line-এর ভেতরে চলে: `width` আর `height` উপেক্ষিত হয়, আর vertical margin অন্য line-কে সরায় না। `inline-block` text-এর মতো line-এ বসে, কিন্তু block-এর মতো `width`, `height`, margin আর padding মানে।""",
        code=r"""
            span.tag  { width: 100px; }        /* ignored: span is inline */
            span.chip { display: inline-block; width: 100px; padding: 4px 8px; }
            a.button  { display: block; }      /* own line, full width */
        """, lang="css",
        ex_en=r"""Vertical padding on an inline element is painted but doesn't push neighbouring lines away, which surprises people styling links as buttons. For rows of items, Flexbox or Grid is usually cleaner than `inline-block`, which also leaves whitespace gaps between items.""",
        ex_bn=r"""Inline element-এর vertical padding আঁকা হয় ঠিকই, কিন্তু পাশের line-গুলোকে সরায় না; link-কে button বানাতে গিয়ে অনেকে এতে অবাক হয়। Item-এর সারির জন্য `inline-block`-এর চেয়ে Flexbox বা Grid সাধারণত পরিষ্কার, কারণ `inline-block` item-এর মাঝে whitespace-এর ফাঁকও রেখে দেয়।""",
        tip_en=r"""Answer with one example element each (`<div>`, `<span>`, a button-like link) and say what happens to `width`.""",
        tip_bn=r"""প্রতিটার জন্য একটা করে example element দাও (`<div>`, `<span>`, button-এর মতো link) আর বলো `width`-এর কী হয়।""",
        follow=[
            ("Why does `width` do nothing on a `<span>`?", "`<span>`-এ `width` দিলে কিছু হয় না কেন?"),
            ("What is `display: none` vs `visibility: hidden`?", "`display: none` আর `visibility: hidden`-এর পার্থক্য কী?"),
        ],
        related=["css-006", "css-029", "html-q01"],
        refs=[("MDN — display", "https://developer.mozilla.org/en-US/docs/Web/CSS/display")],
    ),
    # ------------------------------------------------------------------ css-q02
    Q(
        id="css-q02", sub="Flexbox", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["centering", "grid", "flexbox", "margin-auto"],
        ver=VER, vs=False, status="stable",
        q_en=r"""How do you centre an element horizontally and vertically?""",
        q_bn=r"""একটা element-কে horizontally আর vertically মাঝখানে কীভাবে আনবে?""",
        a_en=r"""The shortest way is Grid on the parent: `display: grid; place-items: center;`. Flexbox works too: `display: flex; justify-content: center; align-items: center;`. To centre only horizontally a block with a width, `margin-inline: auto` is enough.""",
        a_bn=r"""সবচেয়ে ছোট উপায় parent-এ Grid: `display: grid; place-items: center;`। Flexbox-ও চলে: `display: flex; justify-content: center; align-items: center;`। শুধু horizontally মাঝে আনতে চাইলে, width আছে এমন block-এ `margin-inline: auto`-ই যথেষ্ট।""",
        code=r"""
            .parent { display: grid; place-items: center; min-height: 100dvh; }
            /* or */
            .parent { display: flex; justify-content: center; align-items: center; }
            /* horizontal only */
            .box { width: 20rem; margin-inline: auto; }
        """, lang="css",
        ex_en=r"""Vertical centring needs a parent taller than the child; a parent that is only as tall as its content has nothing to centre in. `text-align: center` centres inline content such as text, not the block itself. For overlays, `position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%)` still works.""",
        ex_bn=r"""Vertically মাঝে আনতে parent-কে child-এর চেয়ে লম্বা হতে হবে; content-এর সমান উচ্চতার parent-এ মাঝে আনার জায়গাই নেই। `text-align: center` শুধু text-এর মতো inline content মাঝে আনে, block-টাকে নয়। Overlay-এর জন্য `position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%)` এখনো কাজ করে।""",
        tip_en=r"""Lead with the Grid one-liner, mention Flexbox, then add the parent-height gotcha.""",
        tip_bn=r"""Grid-এর এক লাইনের সমাধান দিয়ে শুরু করো, Flexbox-এর কথা বলো, তারপর parent-এর height-এর ফাঁদটা যোগ করো।""",
        follow=[
            ("Why doesn't `vertical-align: middle` centre a `<div>`?", "`vertical-align: middle` দিয়ে `<div>` মাঝে আসে না কেন?"),
        ],
        related=["css-006", "css-004"],
        refs=[("MDN — place-items", "https://developer.mozilla.org/en-US/docs/Web/CSS/place-items")],
    ),
    # ------------------------------------------------------------------ css-q03
    Q(
        id="css-q03", sub="Responsive Design", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["units", "rem", "em", "px", "percent"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `px`, `em`, `rem` and `%`?""",
        q_bn=r"""`px`, `em`, `rem` আর `%`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`px` is a fixed CSS pixel. `em` is relative to the element's own font size (for `font-size` itself, the parent's), so it compounds when nested, while `rem` is always relative to the root `<html>` font size. `%` is relative to the parent, for example its width. I use `rem` for font sizes and spacing so they follow the user's font setting.""",
        a_bn=r"""`px` একটা নির্দিষ্ট CSS pixel। `em` element-এর নিজের font size অনুযায়ী (আর `font-size`-এ ব্যবহার করলে parent-এর), তাই nested হলে গুণ হতে থাকে; `rem` সবসময় root `<html>`-এর font size অনুযায়ী। `%` parent অনুযায়ী, যেমন parent-এর width। Font size আর spacing-এ আমি `rem` ব্যবহার করি, যাতে user-এর font setting মেনে চলে।""",
        code=r"""
            html  { font-size: 100%; }                  /* 16px by default */
            .card { font-size: 1.25rem; padding: 1em; } /* 20px text, 20px padding */
            .card small { font-size: 0.8em; }           /* 0.8 × 20 = 16px */
        """, lang="css",
        ex_en=r"""Percentage padding and margin resolve against the container's width, even for top and bottom, which is a common follow-up. `em` is handy for padding inside a button, so the padding grows with the button's text.""",
        ex_bn=r"""Padding আর margin-এ `%` দিলে, top আর bottom-এও, container-এর width ধরে হিসাব হয়; এটা খুব প্রচলিত follow-up। Button-এর ভেতরের padding-এ `em` সুবিধাজনক, কারণ text বড় হলে padding-ও বাড়ে।""",
        tip_en=r"""Give the "relative to what" for each unit in one breath, then say which one you use for fonts and why.""",
        tip_bn=r"""প্রতিটা unit "কীসের তুলনায়" সেটা এক নিঃশ্বাসে বলো, তারপর font-এর জন্য কোনটা ব্যবহার করো আর কেন সেটা বলো।""",
        follow=[
            ("Why can nested `em` font sizes grow out of control?", "Nested `em` font size কেন নিয়ন্ত্রণের বাইরে বড় হয়ে যেতে পারে?"),
        ],
        related=["css-021", "css-007"],
        refs=[("MDN — <length>", "https://developer.mozilla.org/en-US/docs/Web/CSS/length")],
    ),
    # ------------------------------------------------------------------ css-q04
    Q(
        id="css-q04", sub="Responsive Design", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["units", "vh", "dvh", "viewport", "mobile"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are `vw` and `vh`, and why do `dvh` and `svh` exist?""",
        q_bn=r"""`vw` আর `vh` কী, আর `dvh` ও `svh` কেন এসেছে?""",
        a_en=r"""`1vw` and `1vh` are 1% of the viewport's width and height. On most mobile browsers `100vh` equals the largest viewport (toolbars hidden), so a full-height section is cut off while the address bar shows. `dvh` follows the current visible height, `svh` is the smallest and `lvh` the largest; I use `100dvh` or `100svh` for full-screen layouts.""",
        a_bn=r"""`1vw` আর `1vh` হলো viewport-এর width আর height-এর 1%। বেশিরভাগ mobile browser-এ `100vh` মানে সবচেয়ে বড় viewport (toolbar লুকানো অবস্থায়), তাই address bar দেখা গেলে full-height section কেটে যায়। `dvh` বর্তমান দৃশ্যমান height মেনে চলে, `svh` সবচেয়ে ছোট আর `lvh` সবচেয়ে বড়; full-screen layout-এ আমি `100dvh` বা `100svh` দিই।""",
        code=r"""
            .hero {
              min-height: 100vh;   /* fallback for very old browsers */
              min-height: 100dvh;  /* follows the visible viewport */
            }
        """, lang="css",
        ex_en=r"""`dvh` changes as the toolbar shows and hides, which can make content jump while scrolling; `svh` is stable and never hidden behind the toolbar. `100vw` includes the scrollbar on desktop, a classic cause of sideways scrolling.""",
        ex_bn=r"""Toolbar দেখা-লুকানোর সাথে `dvh` বদলায়, তাই scroll করার সময় content লাফাতে পারে; `svh` স্থির থাকে আর কখনো toolbar-এর নিচে লুকায় না। Desktop-এ `100vw` scrollbar-এর width-ও ধরে, sideways scroll-এর এটা একটা পরিচিত কারণ।""",
        tip_en=r"""Describe the real bug (hero cut off by the mobile address bar) and the fix in one line: `100dvh`.""",
        tip_bn=r"""আসল bug-টা বলো (mobile-এর address bar-এ hero কেটে যাওয়া) আর এক লাইনে সমাধান: `100dvh`।""",
        follow=[
            ("Why can `width: 100vw` cause a horizontal scrollbar?", "`width: 100vw` কেন horizontal scrollbar তৈরি করতে পারে?"),
        ],
        related=["css-027", "css-020"],
        refs=[("MDN — <length> (viewport units)", "https://developer.mozilla.org/en-US/docs/Web/CSS/length")],
    ),
    # ------------------------------------------------------------------ css-q05
    Q(
        id="css-q05", sub="Box Model", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["margin", "padding", "box-model"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between margin and padding?""",
        q_bn=r"""Margin আর padding-এর পার্থক্য কী?""",
        a_en=r"""Padding is the space inside the border, between the border and the content, and the element's background shows through it. Margin is the space outside the border that pushes other elements away; it is always transparent, can be negative or `auto`, and vertical margins between blocks can collapse.""",
        a_bn=r"""Padding হলো border-এর ভেতরের জায়গা, border আর content-এর মাঝে, আর element-এর background সেখানেও দেখা যায়। Margin হলো border-এর বাইরের জায়গা, যা অন্য element-কে দূরে ঠেলে; এটা সবসময় transparent, negative বা `auto` হতে পারে, আর block-এর মাঝের vertical margin collapse করতে পারে।""",
        code=r"""
            .card {
              padding: 16px;        /* inside: background fills it */
              margin: 24px auto;    /* outside: transparent, auto centres */
              background: #fff;
              border: 1px solid #ddd;
            }
        """, lang="css",
        ex_en=r"""Padding adds to the box's size unless `box-sizing: border-box` is set. Between flex or grid items, `gap` is usually cleaner than margins on every child.""",
        ex_bn=r"""`box-sizing: border-box` না দিলে padding box-এর size বাড়িয়ে দেয়। Flex বা grid item-এর মাঝে ফাঁক রাখতে প্রতিটা child-এ margin দেওয়ার চেয়ে `gap` সাধারণত পরিষ্কার।""",
        tip_en=r"""Say "inside vs outside the border", then add one fact each: background shows in padding, margins can collapse.""",
        tip_bn=r"""বলো "border-এর ভেতরে বনাম বাইরে", তারপর প্রতিটার একটা তথ্য যোগ করো: padding-এ background দেখা যায়, margin collapse করতে পারে।""",
        follow=[
            ("When do vertical margins collapse?", "Vertical margin কখন collapse করে?"),
        ],
        related=["css-001"],
        refs=[("MDN — Introduction to the CSS box model", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model/Introduction_to_the_CSS_box_model")],
    ),
    # ------------------------------------------------------------------ css-q06
    Q(
        id="css-q06", sub="Pseudo-classes and Pseudo-elements", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["pseudo-classes", "pseudo-elements", "selectors"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between a pseudo-class and a pseudo-element?""",
        q_bn=r"""Pseudo-class আর pseudo-element-এর পার্থক্য কী?""",
        a_en=r"""A pseudo-class (one colon) selects an element in a certain state or position, like `:hover`, `:focus-visible`, `:first-child` or `:checked`. A pseudo-element (two colons) styles a part of an element or adds generated content, like `::before`, `::after`, `::first-line` or `::placeholder`.""",
        a_bn=r"""Pseudo-class (এক colon) কোনো element-কে তার বিশেষ state বা অবস্থান দেখে select করে, যেমন `:hover`, `:focus-visible`, `:first-child` বা `:checked`। Pseudo-element (দুই colon) element-এর একটা অংশ style করে বা generated content যোগ করে, যেমন `::before`, `::after`, `::first-line` বা `::placeholder`।""",
        code=r"""
            a:hover            { text-decoration: underline; }  /* state */
            li:first-child     { font-weight: 700; }            /* position */
            .badge::before     { content: "●"; color: red; }    /* generated content */
            input::placeholder { color: #666; }                 /* part of an element */
        """, lang="css",
        ex_en=r"""The single-colon form (`:before`) still works for the old CSS2 pseudo-elements, but `::` is the modern syntax. Content added with `::before`/`::after` isn't in the DOM, so don't put important information there.""",
        ex_bn=r"""পুরোনো CSS2 pseudo-element-এর জন্য এক colon-এর রূপ (`:before`) এখনো চলে, তবে আধুনিক syntax হলো `::`। `::before`/`::after` দিয়ে যোগ করা content DOM-এ থাকে না, তাই জরুরি তথ্য সেখানে রেখো না।""",
        tip_en=r"""Use the shortcut "one colon = state, two colons = part", and give two examples of each.""",
        tip_bn=r"""ছোট সূত্রটা বলো "এক colon = state, দুই colon = অংশ", আর প্রতিটার দুটো করে example দাও।""",
        follow=[
            ("Why does `::before` show nothing without `content`?", "`content` ছাড়া `::before` কেন কিছুই দেখায় না?"),
        ],
        related=["css-008", "css-013"],
        refs=[("MDN — Pseudo-elements", "https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements")],
    ),
    # ------------------------------------------------------------------ css-q07
    Q(
        id="css-q07", sub="Cascade and Layers", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["inline-css", "stylesheet", "link", "cascade"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are inline, internal and external CSS, and which should you use?""",
        q_bn=r"""Inline, internal আর external CSS কী, আর কোনটা ব্যবহার করা উচিত?""",
        a_en=r"""Inline CSS is the `style` attribute on one element, internal CSS sits in a `<style>` block in the page, and external CSS lives in a `.css` file linked with `<link rel="stylesheet">`. External files are the normal choice because they are reusable and cacheable; inline styles beat normal stylesheet rules, so they are hard to override.""",
        a_bn=r"""Inline CSS হলো একটা element-এর `style` attribute, internal CSS থাকে page-এর ভেতরের `<style>` block-এ, আর external CSS থাকে আলাদা `.css` file-এ, যা `<link rel="stylesheet">` দিয়ে যুক্ত করা হয়। সাধারণত external file-ই ব্যবহার করা হয়, কারণ বারবার ব্যবহার আর cache করা যায়; inline style সাধারণ stylesheet rule-কে হারিয়ে দেয়, তাই override করা কঠিন।""",
        code=r"""
            <link rel="stylesheet" href="/css/main.css">     <!-- external -->
            <style> .price { color: green; } </style>        <!-- internal -->
            <p class="price" style="color: red;">৳1,250</p> <!-- inline: red wins -->
        """, lang="html",
        ex_en=r"""Internal and external CSS have no priority over each other; specificity and then source order decide. Small critical CSS is sometimes inlined in a `<style>` block on purpose to speed up the first render.""",
        ex_bn=r"""Internal আর external CSS-এর মধ্যে কারো আলাদা অগ্রাধিকার নেই; আগে specificity, তারপর source order ঠিক করে কে জিতবে। প্রথম render দ্রুত করতে ছোট critical CSS কখনো কখনো ইচ্ছা করেই `<style>` block-এ inline করা হয়।""",
        tip_en=r"""Name all three with one line of markup each, then say why external is the default.""",
        tip_bn=r"""তিনটারই নাম বলো, প্রতিটার এক লাইনের markup দেখাও, তারপর বলো external কেন default।""",
        follow=[
            ("Does an internal `<style>` block beat an external stylesheet?", "Internal `<style>` block কি external stylesheet-কে হারায়?"),
        ],
        related=["css-002", "html-030"],
        refs=[("MDN — <link>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/link")],
    ),
    # ------------------------------------------------------------------ css-q08
    Q(
        id="css-q08", sub="Modern CSS Features", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["opacity", "rgba", "color", "transparency"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `opacity: 0.5` and a semi-transparent colour like `rgb(0 0 0 / 0.5)`?""",
        q_bn=r"""`opacity: 0.5` আর `rgb(0 0 0 / 0.5)`-এর মতো আধা-স্বচ্ছ রঙের মধ্যে পার্থক্য কী?""",
        a_en=r"""`opacity` makes the whole element transparent, including its text, border and children, and children can't opt out. A colour with an alpha value, like `rgb(0 0 0 / 0.5)` or the older `rgba(0, 0, 0, 0.5)`, makes only that one colour transparent, such as the background, so the text stays fully readable.""",
        a_bn=r"""`opacity` পুরো element-কে স্বচ্ছ করে, তার text, border আর child-সহ, আর child-রা এর বাইরে যেতে পারে না। Alpha-সহ রং, যেমন `rgb(0 0 0 / 0.5)` বা পুরোনো `rgba(0, 0, 0, 0.5)`, শুধু ওই একটা রংকেই স্বচ্ছ করে, যেমন background, তাই text পুরোপুরি পড়া যায়।""",
        code=r"""
            .overlay-a { background: black; opacity: 0.5; }            /* text fades too */
            .overlay-b { background: rgb(0 0 0 / 0.5); color: #fff; }  /* only bg fades */
        """, lang="css",
        ex_en=r"""`opacity` below 1 also creates a stacking context, which can change how `z-index` behaves. `rgba()` is a legacy alias that still works; modern `rgb()` takes the alpha after a slash.""",
        ex_bn=r"""1-এর কম `opacity` একটা stacking context-ও তৈরি করে, ফলে `z-index`-এর আচরণ বদলে যেতে পারে। `rgba()` একটা legacy alias যেটা এখনো চলে; আধুনিক `rgb()`-এ alpha দেওয়া হয় slash-এর পরে।""",
        tip_en=r"""Use the overlay example: "with `opacity` the white text fades too; with an alpha background it doesn't".""",
        tip_bn=r"""Overlay-এর example দাও: "`opacity` দিলে সাদা text-ও ফিকে হয়; alpha background দিলে হয় না"।""",
        follow=[
            ("Does `opacity: 0` hide an element from screen readers?", "`opacity: 0` কি element-কে screen reader থেকে লুকায়?"),
        ],
        related=["css-019", "css-029"],
        refs=[("MDN — opacity", "https://developer.mozilla.org/en-US/docs/Web/CSS/opacity")],
    ),
    # ------------------------------------------------------------------ css-q09
    Q(
        id="css-q09", sub="Specificity and Inheritance", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["important", "cascade", "specificity"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What does `!important` do, and why should you avoid it?""",
        q_bn=r"""`!important` কী করে, আর কেন এটা এড়িয়ে চলা উচিত?""",
        a_en=r"""`!important` makes a declaration beat all normal declarations, whatever their specificity or order. The only way to override it is another `!important`, so it leads to escalation and messy CSS. I use it only for utility classes that must always win or to beat third-party inline styles, and otherwise fix specificity or use `@layer`.""",
        a_bn=r"""`!important` একটা declaration-কে সব সাধারণ declaration-এর ওপরে জিতিয়ে দেয়, তাদের specificity বা order যাই হোক। এটাকে override করার একমাত্র উপায় আরেকটা `!important`, তাই ধীরে ধীরে প্রতিযোগিতা বাড়ে আর CSS অগোছালো হয়। আমি এটা শুধু যে utility class সবসময় জিততেই হবে বা third-party inline style হারাতে ব্যবহার করি; বাকি সময় specificity ঠিক করি বা `@layer` ব্যবহার করি।""",
        code=r"""
            .btn { color: white !important; }
            #checkout .btn { color: black; }   /* loses: not !important */
        """, lang="css",
        ex_en=r"""Inside cascade layers, `!important` reverses the layer order: an important rule in an earlier layer beats later layers. That is a common trap when moving old CSS into `@layer`.""",
        ex_bn=r"""Cascade layer-এর ভেতরে `!important` layer order উল্টে দেয়: আগের layer-এর important rule পরের layer-গুলোকে হারায়। পুরোনো CSS `@layer`-এ সরানোর সময় এটা একটা পরিচিত ফাঁদ।""",
        tip_en=r"""Show that you know when it's legitimate (utilities, third-party overrides), not just "never use it".""",
        tip_bn=r"""শুধু "কখনো ব্যবহার করো না" না বলে দেখাও যে কখন এটা যুক্তিসঙ্গত (utility, third-party override) সেটা তুমি জানো।""",
        follow=[
            ("How do cascade layers reduce the need for `!important`?", "Cascade layer কীভাবে `!important`-এর দরকার কমায়?"),
        ],
        related=["css-012", "css-030"],
        refs=[("MDN — !important", "https://developer.mozilla.org/en-US/docs/Web/CSS/important")],
    ),
    # ------------------------------------------------------------------ css-q10
    Q(
        id="css-q10", sub="Modern CSS Features", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["logical-properties", "rtl", "writing-mode", "i18n"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are CSS logical properties, such as `margin-inline-start`?""",
        q_bn=r"""CSS logical property কী, যেমন `margin-inline-start`?""",
        a_en=r"""Logical properties name sides by text direction instead of physical sides: `margin-inline-start` instead of `margin-left`, `padding-block` for top and bottom, `inline-size` for width in horizontal text. With `dir="rtl"` (Arabic, Urdu) they flip automatically, so one stylesheet works in both directions.""",
        a_bn=r"""Logical property বাম-ডান-উপর-নিচের বদলে text-এর দিক ধরে পাশের নাম দেয়: `margin-left`-এর বদলে `margin-inline-start`, top আর bottom-এর জন্য `padding-block`, আর horizontal text-এ width-এর জন্য `inline-size`। `dir="rtl"` (Arabic, Urdu) হলে এগুলো নিজে থেকেই উল্টে যায়, তাই একটা stylesheet দুই দিকেই কাজ করে।""",
        code=r"""
            .card { padding-block: 1rem; padding-inline: 1.5rem; }
            .icon { margin-inline-end: 0.5rem; }  /* right in LTR, left in RTL */
        """, lang="css",
        ex_en=r"""Bangla and English are both left-to-right, so you won't see a difference between them, but logical properties keep components ready for RTL languages. `inset-inline`, `border-inline-start` and `text-align: start` follow the same idea.""",
        ex_bn=r"""Bangla আর English দুটোই left-to-right, তাই এদের মধ্যে কোনো পার্থক্য দেখবে না, কিন্তু logical property component-কে RTL ভাষার জন্য তৈরি রাখে। `inset-inline`, `border-inline-start` আর `text-align: start`-ও একই ধারণায় চলে।""",
        tip_en=r"""Explain "inline = along the text, block = across lines", then give the RTL benefit.""",
        tip_bn=r"""ব্যাখ্যা করো "inline = text যে দিকে চলে, block = line-গুলো যে দিকে সাজানো", তারপর RTL-এর সুবিধাটা বলো।""",
        follow=[
            ("What does `inline-size` mean in vertical writing modes?", "Vertical writing mode-এ `inline-size` মানে কী?"),
        ],
        related=["css-032"],
        refs=[("MDN — CSS logical properties and values", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values")],
    ),
]

if __name__ == "__main__":
    save("css", "quick", QUESTIONS)
