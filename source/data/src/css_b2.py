import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_POSITION = ("MDN — position", "https://developer.mozilla.org/en-US/docs/Web/CSS/position")
MDN_CONTAINING_BLOCK = ("MDN — Layout and the containing block", "https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block")
MDN_FLEX = ("MDN — flex", "https://developer.mozilla.org/en-US/docs/Web/CSS/flex")
WEBDEV_FLEXBOX = ("web.dev — Learn CSS: Flexbox", "https://web.dev/learn/css/flexbox")
WEBDEV_GRID = ("web.dev — Learn CSS: Grid", "https://web.dev/learn/css/grid")
MDN_REPEAT = ("MDN — repeat()", "https://developer.mozilla.org/en-US/docs/Web/CSS/repeat")
MDN_MINMAX = ("MDN — minmax()", "https://developer.mozilla.org/en-US/docs/Web/CSS/minmax")
MDN_CQ = ("MDN — CSS container queries", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries")
MDN_CONTAINER = ("MDN — @container", "https://developer.mozilla.org/en-US/docs/Web/CSS/@container")
MDN_VAR = ("MDN — var()", "https://developer.mozilla.org/en-US/docs/Web/CSS/var")
MDN_PROPERTY = ("MDN — @property", "https://developer.mozilla.org/en-US/docs/Web/CSS/@property")
WEBDEV_COMPOSITOR = ("web.dev — Stick to compositor-only properties and manage layer count", "https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count")
MDN_WILL_CHANGE = ("MDN — will-change", "https://developer.mozilla.org/en-US/docs/Web/CSS/will-change")
WEBDEV_RENDERING_PERF = ("web.dev — Rendering performance", "https://web.dev/articles/rendering-performance")
MDN_SUBGRID = ("MDN — Subgrid", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid")

QUESTIONS = [
    # ------------------------------------------------------------------ css-004
    Q(
        id="css-004", sub="Positioning", diff="easy", type="conceptual",
        prio="high", market="bangladesh", mins=4,
        tags=["position", "absolute", "fixed", "sticky", "containing-block"],
        ver="Version-independent (CSS)", vs=False, status="stable",
        q_en=r"""Explain the values of the `position` property: `static`, `relative`, `absolute`, `fixed` and `sticky`. What is each one positioned relative to?""",
        q_bn=r"""`position` property-র value-গুলো ব্যাখ্যা করো: `static`, `relative`, `absolute`, `fixed` আর `sticky`। প্রতিটা কোন জিনিসের সাপেক্ষে position হয়?""",
        a_en=r"""
            - **`static`** (default): normal document flow. `top`/`left` have no effect, and neither does `z-index` (except on flex and grid items).
            - **`relative`**: stays in the flow and keeps its original space, but can be nudged with `top`/`left`. Its most common job is to become the **containing block** for absolutely positioned children.
            - **`absolute`**: removed from the flow (other elements act as if it isn't there) and positioned relative to the nearest **positioned ancestor** (any `position` other than `static`), or the initial containing block if there is none.
            - **`fixed`**: removed from the flow and positioned relative to the **viewport**, so it stays put while scrolling — headers, chat buttons.
            - **`sticky`**: behaves like `relative` until the user scrolls past a threshold (e.g. `top: 0`), then sticks within its scroll container — but only while its parent is still on screen.

            Typical example: a "−20%" badge on a product card — the card is `position: relative`, the badge is `position: absolute; top: 8px; right: 8px`.
        """,
        a_bn=r"""
            - **`static`** (default): সাধারণ document flow। `top`/`left`-এর কোনো প্রভাব নেই, `z-index`-এরও নেই (তবে flex আর grid item-এ `z-index` কাজ করে)।
            - **`relative`**: flow-তেই থাকে আর নিজের আসল জায়গা ধরে রাখে, তবে `top`/`left` দিয়ে একটু সরানো যায়। এর সবচেয়ে প্রচলিত কাজ হলো absolutely positioned children-এর **containing block** হওয়া।
            - **`absolute`**: flow থেকে বাদ পড়ে (অন্য element-গুলো এমন আচরণ করে যেন এটা নেই), আর সবচেয়ে কাছের **positioned ancestor**-এর (যার `position` `static` নয়) সাপেক্ষে বসে; এমন কেউ না থাকলে initial containing block-এর সাপেক্ষে।
            - **`fixed`**: flow থেকে বাদ পড়ে আর **viewport**-এর সাপেক্ষে বসে, তাই scroll করলেও একই জায়গায় থাকে — header, chat button।
            - **`sticky`**: user একটা সীমা (যেমন `top: 0`) পার হয়ে scroll না করা পর্যন্ত `relative`-এর মতো আচরণ করে, তারপর তার scroll container-এর মধ্যে আটকে থাকে — তবে কেবল যতক্ষণ এর parent screen-এ থাকে।

            সাধারণ উদাহরণ: product card-এর উপর "−20%" badge — card-এ `position: relative`, badge-এ `position: absolute; top: 8px; right: 8px`।
        """,
        quick_en=r"""`static` is normal flow; `relative` stays in flow and can be nudged, often as the containing block; `absolute` leaves the flow and uses the nearest positioned ancestor; `fixed` uses the viewport; `sticky` acts like `relative` until a scroll threshold, then sticks.""",
        quick_bn=r"""`static` সাধারণ flow; `relative` flow-তেই থাকে, একটু সরানো যায়, আর প্রায়ই containing block হয়; `absolute` flow থেকে বেরিয়ে নিকটতম positioned ancestor ধরে বসে; `fixed` বসে viewport ধরে; `sticky` scroll-এর একটা সীমা পর্যন্ত `relative`-এর মতো, তারপর আটকে যায়।""",
        ex_en=r"""
            - **The `fixed` gotcha:** if any ancestor has `transform`, `filter`, `perspective`, `contain: paint` or `will-change: transform`, that ancestor becomes the containing block. Your "fixed" header or modal then scrolls with that ancestor — a common bug when a page wrapper gets an animation.
            - **Sticky gotchas:** it needs an inset (`top`, `bottom`…), it stops working if an ancestor between it and the scrolling element has `overflow: hidden/auto`, and it can't stick beyond its parent's box.
            - **Absolute + percentage:** `width: 50%` on an absolute element is 50% of the containing block's padding box, not of its direct parent if the parent isn't positioned.
            - **Stacking:** `fixed` and `sticky` always create a stacking context; `relative`/`absolute` do when combined with a `z-index` other than `auto`.
        """,
        ex_bn=r"""
            - **`fixed`-এর ফাঁদ:** কোনো ancestor-এ `transform`, `filter`, `perspective`, `contain: paint` বা `will-change: transform` থাকলে সেই ancestor-ই containing block হয়ে যায়। তখন তোমার "fixed" header বা modal ওই ancestor-এর সাথে scroll করে — page wrapper-এ animation যোগ করলে এটা খুব সাধারণ bug।
            - **Sticky-র ফাঁদ:** এর একটা inset (`top`, `bottom`…) লাগে, এটা আর scroll হওয়া element-এর মাঝে কোনো ancestor-এ `overflow: hidden/auto` থাকলে কাজ করে না, আর এটা parent-এর box-এর বাইরে আটকে থাকতে পারে না।
            - **Absolute + percentage:** absolute element-এ `width: 50%` মানে containing block-এর padding box-এর 50%, parent positioned না হলে সরাসরি parent-এর নয়।
            - **Stacking:** `fixed` আর `sticky` সবসময় stacking context তৈরি করে; `relative`/`absolute` তৈরি করে যখন সাথে `auto` ছাড়া অন্য কোনো `z-index` থাকে।
        """,
        tip_en=r"""For each value, answer two things: "is it still in the flow?" and "relative to what?". That compact structure covers everything; add the `transform` + `fixed` gotcha for bonus points.""",
        tip_bn=r"""প্রতিটা value-র জন্য দুটো প্রশ্নের উত্তর দাও: "এটা কি এখনো flow-তে আছে?" আর "কীসের সাপেক্ষে?"। এই ছোট কাঠামোতেই সব কভার হয়; বাড়তি নম্বরের জন্য `transform` + `fixed`-এর ফাঁদটা যোগ করো।""",
        mist_en=r"""Saying `absolute` is relative to the parent (it's the nearest *positioned* ancestor), or thinking `fixed` is always relative to the viewport.""",
        mist_bn=r"""`absolute` parent-এর সাপেক্ষে বলা (আসলে সবচেয়ে কাছের *positioned* ancestor-এর সাপেক্ষে), অথবা `fixed` সবসময় viewport-এর সাপেক্ষে ভাবা।""",
        code=r"""
            .product-card { position: relative; }

            .product-card .discount {
              position: absolute;
              top: 8px;
              right: 8px;
            }

            .site-header {
              position: sticky;
              top: 0;
              z-index: 10;
            }

            .chat-button {
              position: fixed;
              right: 16px;
              bottom: 16px;
            }
        """,
        lang="css",
        follow=[
            ("Why might a `position: fixed` modal scroll with the page?", "`position: fixed` modal কেন page-এর সাথে scroll করতে পারে?"),
            ("What's the difference between `position: absolute` and using CSS Grid to overlap elements?", "`position: absolute` আর CSS Grid দিয়ে element একটার উপর আরেকটা বসানোর পার্থক্য কী?"),
        ],
        related=["css-020", "css-019"],
        refs=[MDN_POSITION, MDN_CONTAINING_BLOCK],
    ),
    # ------------------------------------------------------------------ css-005
    Q(
        id="css-005", sub="Flexbox", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["flexbox", "flex-shorthand", "flex-grow", "flex-basis"],
        ver="Version-independent (CSS Flexbox)", vs=False, status="stable",
        q_en=r"""What does `flex: 1` on a flex item expand to?""",
        q_bn=r"""Flex item-এ `flex: 1` দিলে সেটা কীসের সমান হয়?""",
        options=[
            ("`flex-grow: 1; flex-shrink: 1; flex-basis: 0%`", "`flex-grow: 1; flex-shrink: 1; flex-basis: 0%`"),
            ("`flex-grow: 1; flex-shrink: 0; flex-basis: auto`", "`flex-grow: 1; flex-shrink: 0; flex-basis: auto`"),
            ("`flex-grow: 1; flex-shrink: 1; flex-basis: auto`", "`flex-grow: 1; flex-shrink: 1; flex-basis: auto`"),
            ("Only `flex-grow: 1`; shrink and basis keep their current values", "শুধু `flex-grow: 1`; shrink আর basis আগের মানেই থাকে"),
        ],
        correct=0,
        a_en=r"""
            `flex: 1` means grow 1, shrink 1, **basis 0** (browsers serialize it as `0%`). Because every item starts from zero, the free space is shared equally — that's why `flex: 1` on all items gives equal-width columns.
        """,
        a_bn=r"""
            `flex: 1` মানে grow 1, shrink 1, **basis 0** (browser এটাকে `0%` হিসেবে দেখায়)। প্রতিটা item শূন্য থেকে শুরু করে বলে ফাঁকা জায়গা সমানভাবে ভাগ হয় — এজন্যই সব item-এ `flex: 1` দিলে সমান চওড়া column পাওয়া যায়।
        """,
        quick_en=r"""`flex-grow: 1; flex-shrink: 1; flex-basis: 0%`. Because every item starts from a zero basis, free space is shared equally, which is why `flex: 1` on all items gives equal-width columns.""",
        quick_bn=r"""`flex-grow: 1; flex-shrink: 1; flex-basis: 0%`। প্রতিটা item শূন্য basis থেকে শুরু করে বলে খালি জায়গা সমানভাবে ভাগ হয়, এজন্যই সব item-এ `flex: 1` দিলে সমান চওড়া column হয়।""",
        ex_en=r"""
            The tempting wrong answer is C — that's `flex: auto` (`1 1 auto`). With basis `auto`, each item starts at its content size and only the *leftover* space is shared, so items with longer text end up wider.

            Other keywords worth knowing: `flex: none` = `0 0 auto` (rigid), `flex: initial` = `0 1 auto` (the default: don't grow, may shrink). The shorthand also resets the parts you don't mention, which is why D is wrong.

            One caveat: even with `flex: 1`, items won't shrink below their min-content width because of `min-width: auto`. A long unbreakable word makes "equal" columns unequal — add `min-width: 0` when that matters.
        """,
        ex_bn=r"""
            প্রলোভনজনক ভুল উত্তর C — ওটা আসলে `flex: auto` (`1 1 auto`)। Basis `auto` হলে প্রতিটা item তার content-এর মাপ থেকে শুরু করে, আর শুধু *বাকি থাকা* জায়গা ভাগ হয়, ফলে লম্বা text-এর item বেশি চওড়া হয়।

            আরও কিছু keyword জানা দরকার: `flex: none` = `0 0 auto` (অনমনীয়), `flex: initial` = `0 1 auto` (default: বড় হয় না, ছোট হতে পারে)। Shorthand যে অংশগুলো বলোনি সেগুলোও reset করে — এজন্যই D ভুল।

            একটা সতর্কতা: `flex: 1` থাকলেও `min-width: auto`-এর কারণে item তার min-content width-এর চেয়ে ছোট হয় না। ভাঙা যায় না এমন একটা লম্বা শব্দ থাকলে "সমান" column-গুলো অসমান হয়ে যায় — দরকার হলে `min-width: 0` যোগ করো।
        """,
        tip_en=r"""Contrast `flex: 1` with `flex: auto` in one sentence — "basis 0 shares all space, basis auto shares leftover space". That's the real understanding being tested.""",
        tip_bn=r"""এক বাক্যে `flex: 1` আর `flex: auto`-এর তুলনা করো — "basis 0 পুরো জায়গা ভাগ করে, basis auto বাকি জায়গা ভাগ করে"। আসলে এই বোঝাপড়াটাই যাচাই করা হচ্ছে।""",
        refs=[MDN_FLEX, WEBDEV_FLEXBOX],
    ),
    # ------------------------------------------------------------------ css-006
    Q(
        id="css-006", sub="CSS Grid", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["flexbox", "grid", "fr-unit", "layout"],
        ver="Version-independent (CSS Flexbox & Grid)", vs=False, status="stable",
        q_en=r"""When do you reach for Flexbox and when for CSS Grid? What does the `fr` unit mean?""",
        q_bn=r"""কখন Flexbox আর কখন CSS Grid ব্যবহার করবে? `fr` unit মানে কী?""",
        a_en=r"""
            - **Flexbox is one-dimensional** — it lays items out along a single row *or* column, and sizes are driven by the content ("content-out"). Great for navigation bars, toolbars, a button row, centring something, or chips that wrap.
            - **Grid is two-dimensional** — you define rows *and* columns and place items into that structure ("layout-in"). Great for page layouts, product galleries, dashboards and forms where labels and inputs must line up in both directions.

            They combine well: Grid for the page and the card gallery, Flexbox inside each card for the price-and-button row.

            **`fr`** is a fraction of the **free space** in the grid container after fixed-size tracks and gaps are subtracted. `grid-template-columns: 200px 1fr 2fr` gives 200px to the first column and splits the rest 1 : 2.
        """,
        a_bn=r"""
            - **Flexbox হলো এক-মাত্রিক** — item-গুলোকে একটা row *অথবা* column বরাবর সাজায়, আর মাপ ঠিক হয় content দেখে ("content-out")। Navigation bar, toolbar, button-এর সারি, কিছু center করা, বা wrap হওয়া chip-এর জন্য দারুণ।
            - **Grid হলো দ্বি-মাত্রিক** — row *এবং* column দুটোই নির্ধারণ করে item-গুলো সেই কাঠামোয় বসাও ("layout-in")। Page layout, product gallery, dashboard আর এমন form-এর জন্য দারুণ যেখানে label আর input দুই দিকেই সারিবদ্ধ হতে হবে।

            দুটো একসাথে ভালো কাজ করে: page আর card gallery-র জন্য Grid, আর প্রতিটা card-এর ভেতরে দাম ও button-এর সারির জন্য Flexbox।

            **`fr`** হলো fixed-size track আর gap বাদ দেওয়ার পর grid container-এর **ফাঁকা জায়গার** একটা ভগ্নাংশ। `grid-template-columns: 200px 1fr 2fr` দিলে প্রথম column 200px পায়, আর বাকি জায়গা 1 : 2 অনুপাতে ভাগ হয়।
        """,
        quick_en=r"""Flexbox is one-dimensional and content-driven, good for navbars, button rows and centring; Grid is two-dimensional, good for page layouts and galleries, and the two combine well. `fr` is a fraction of the grid's free space after fixed tracks and gaps.""",
        quick_bn=r"""Flexbox এক-মাত্রিক আর content অনুযায়ী চলে, navbar, button-এর সারি বা centring-এর জন্য ভালো; Grid দুই-মাত্রিক, page layout আর gallery-র জন্য ভালো, আর দুটো একসাথে ভালো চলে। `fr` হলো fixed track আর gap বাদে grid-এর খালি জায়গার একটা ভাগ।""",
        ex_en=r"""
            - **Alignment across items:** in a wrapping flex row, each line is independent, so items in different lines don't align into columns. If you find yourself fighting that, you want Grid.
            - **`gap`** works in both Flexbox and Grid today, so margin hacks aren't needed.
            - **`1fr` has a minimum:** it's really `minmax(auto, 1fr)`, so long content can push a column wider than its share. Use `minmax(0, 1fr)` for strict proportions.
            - **Source order and accessibility:** both can visually reorder items (`order`, grid placement), but keyboard and screen-reader order follow the DOM — don't create a mismatch.
        """,
        ex_bn=r"""
            - **Item-গুলোর মধ্যে সারিবদ্ধতা:** wrap হওয়া flex row-এ প্রতিটা line স্বাধীন, তাই ভিন্ন line-এর item-গুলো column বরাবর মেলে না। এই নিয়ে লড়াই করতে হলে বুঝবে তোমার আসলে Grid দরকার।
            - **`gap`** এখন Flexbox আর Grid দুটোতেই কাজ করে, তাই margin hack লাগে না।
            - **`1fr`-এর একটা minimum আছে:** এটা আসলে `minmax(auto, 1fr)`, তাই লম্বা content একটা column-কে তার ভাগের চেয়ে চওড়া করে দিতে পারে। কড়া অনুপাত চাইলে `minmax(0, 1fr)` ব্যবহার করো।
            - **Source order আর accessibility:** দুটো দিয়েই দৃশ্যত item-এর ক্রম বদলানো যায় (`order`, grid placement), কিন্তু keyboard আর screen reader DOM-এর ক্রম মেনে চলে — অমিল তৈরি কোরো না।
        """,
        tip_en=r"""Use "one dimension vs two" and "content-out vs layout-in" as your two anchors, then give one concrete UI example of each. Mentioning that you combine them shows practical judgement.""",
        tip_bn=r""""এক মাত্রা বনাম দুই মাত্রা" আর "content-out বনাম layout-in" — এই দুটোকে মূল ভিত্তি করো, তারপর প্রতিটার একটা করে বাস্তব UI উদাহরণ দাও। দুটো যে একসাথে ব্যবহার করো, তা বললে তোমার বাস্তব বিচারবুদ্ধি বোঝা যায়।""",
        mist_en=r"""Saying "Grid replaces Flexbox", or thinking `1fr` is a fraction of the *total* width (it's of the remaining free space).""",
        mist_bn=r""""Grid Flexbox-কে প্রতিস্থাপন করে" বলা, অথবা `1fr`-কে *মোট* width-এর ভগ্নাংশ ভাবা (আসলে এটা বাকি ফাঁকা জায়গার ভগ্নাংশ)।""",
        code=r"""
            /* Grid: page and gallery structure */
            .page {
              display: grid;
              grid-template-columns: 240px 1fr;   /* sidebar + main */
              gap: 24px;
            }
            .gallery {
              display: grid;
              grid-template-columns: repeat(3, 1fr);
              gap: 16px;
            }

            /* Flexbox: a row inside a card */
            .card-footer {
              display: flex;
              align-items: center;
              justify-content: space-between;
              gap: 8px;
            }
        """,
        lang="css",
        follow=[
            ("How would you build a layout that's 1 column on phones and 3 on desktops without media queries?", "Media query ছাড়া phone-এ 1 column আর desktop-এ 3 column layout কীভাবে বানাবে?"),
            ("What does `minmax(0, 1fr)` fix?", "`minmax(0, 1fr)` কোন সমস্যা ঠিক করে?"),
        ],
        related=["css-015", "css-025"],
        refs=[WEBDEV_GRID, WEBDEV_FLEXBOX],
    ),
    # ------------------------------------------------------------------ css-015
    Q(
        id="css-015", sub="CSS Grid", diff="medium", type="comparison",
        prio="high", market="both", mins=5,
        tags=["grid", "auto-fill", "auto-fit", "minmax", "responsive"],
        ver="Version-independent (CSS Grid)", vs=False, status="stable",
        q_en=r"""What's the difference between `repeat(auto-fill, minmax(200px, 1fr))` and `repeat(auto-fit, minmax(200px, 1fr))`? Describe what happens with only two cards in a 1000px-wide container (gap 16px).""",
        q_bn=r"""`repeat(auto-fill, minmax(200px, 1fr))` আর `repeat(auto-fit, minmax(200px, 1fr))`-এর পার্থক্য কী? 1000px চওড়া container-এ (gap 16px) মাত্র দুটো card থাকলে কী হয়, বর্ণনা করো।""",
        a_en=r"""
            Both create as many columns of at least 200px as fit in the container, which gives a responsive grid without media queries. The difference is what happens to **empty tracks**:
            - **`auto-fill`** keeps the empty columns. Four columns fit (4 × 200 + 3 × 16 = 848 ≤ 1000), so each is (1000 − 48) / 4 = **238px**; the two cards take two of them and the other two stay empty.
            - **`auto-fit`** collapses empty columns to zero (and the gaps around them), so the remaining tracks absorb the space: the two cards become (1000 − 16) / 2 = **492px** each.

            With enough items to fill a row, both behave the same. I use `auto-fill` when cards should keep a consistent size (a product grid where a lonely last card shouldn't balloon), and `auto-fit` when a few items should stretch to fill the row.
        """,
        a_bn=r"""
            দুটোই container-এ যতগুলো কমপক্ষে 200px-এর column আঁটে ততগুলো বানায়, ফলে media query ছাড়াই responsive grid পাওয়া যায়। পার্থক্য হলো **খালি track**-এর কী হয়:
            - **`auto-fill`** খালি column রেখে দেয়। চারটা column আঁটে (4 × 200 + 3 × 16 = 848 ≤ 1000), তাই প্রতিটা হয় (1000 − 48) / 4 = **238px**; দুটো card দুটো column নেয়, বাকি দুটো খালি থাকে।
            - **`auto-fit`** খালি column-গুলো (আর তাদের আশেপাশের gap) শূন্যে নামিয়ে দেয়, ফলে বাকি track-গুলো পুরো জায়গা নেয়: দুটো card প্রতিটা হয় (1000 − 16) / 2 = **492px**।

            একটা row পূরণ করার মতো যথেষ্ট item থাকলে দুটো একই আচরণ করে। Card-এর মাপ একরকম রাখতে চাইলে আমি `auto-fill` ব্যবহার করি (product grid, যেখানে শেষের একা card হঠাৎ বিশাল হওয়া উচিত নয়), আর কয়েকটা item দিয়ে পুরো row ভরাতে চাইলে `auto-fit`।
        """,
        quick_en=r"""Both create as many 200px-plus columns as fit, but `auto-fill` keeps empty tracks and `auto-fit` collapses them. With two cards in 1000px, `auto-fill` gives four 238px columns (two empty) and `auto-fit` stretches the two cards to 492px each.""",
        quick_bn=r"""দুটোই যতগুলো কমপক্ষে 200px-এর column ধরে ততগুলো বানায়, কিন্তু `auto-fill` খালি track রেখে দেয় আর `auto-fit` সেগুলো collapse করে। 1000px-এ দুটো card থাকলে `auto-fill`-এ 238px-এর চারটা column হয় (দুটো খালি), আর `auto-fit`-এ দুটো card 492px করে ছড়িয়ে যায়।""",
        ex_en=r"""
            - **`minmax(200px, 1fr)`** means "never narrower than 200px, otherwise share the free space equally".
            - **Narrow containers:** on a 180px-wide container, a 200px minimum overflows. The robust version is `minmax(min(200px, 100%), 1fr)` — the minimum shrinks to the container width when needed.
            - **Why it beats media queries for galleries:** it reacts to the *container* width, so the same component works in a sidebar and in the main area. For more complex component changes (layout switches, not just column counts), use container queries.
            - **DevTools:** the Grid overlay shows the implicit tracks, including empty `auto-fill` columns, which makes the difference obvious.
        """,
        ex_bn=r"""
            - **`minmax(200px, 1fr)`** মানে "কখনো 200px-এর চেয়ে সরু নয়, নইলে ফাঁকা জায়গা সমানভাবে ভাগ করো"।
            - **সরু container:** 180px চওড়া container-এ 200px-এর minimum overflow করে। নির্ভরযোগ্য রূপ হলো `minmax(min(200px, 100%), 1fr)` — দরকার হলে minimum container-এর width পর্যন্ত ছোট হয়।
            - **Gallery-র জন্য media query-র চেয়ে কেন ভালো:** এটা *container*-এর width-এ সাড়া দেয়, তাই একই component sidebar আর main area দুই জায়গাতেই কাজ করে। আরও জটিল component পরিবর্তনের জন্য (শুধু column সংখ্যা নয়, layout বদলানো) container query ব্যবহার করো।
            - **DevTools:** Grid overlay implicit track দেখায়, খালি `auto-fill` column-সহ — এতে পার্থক্যটা চোখের সামনে পরিষ্কার হয়।
        """,
        tip_en=r"""Do the arithmetic out loud (238px vs 492px). Concrete numbers prove you understand track collapsing, not just the slogan "auto-fit stretches".""",
        tip_bn=r"""হিসাবটা মুখে করে দেখাও (238px বনাম 492px)। নির্দিষ্ট সংখ্যা প্রমাণ করে তুমি track collapse আসলেই বোঝো, শুধু "auto-fit stretch করে" slogan মুখস্থ নয়।""",
        mist_en=r"""Saying the two are identical, forgetting that gaps around collapsed tracks also collapse, or using a fixed `minmax(300px, 1fr)` that overflows on 320px phones.""",
        mist_bn=r"""দুটোকে একই বলা, collapse হওয়া track-এর আশেপাশের gap-ও যে collapse হয় তা ভুলে যাওয়া, অথবা নির্দিষ্ট `minmax(300px, 1fr)` ব্যবহার করা যা 320px phone-এ overflow করে।""",
        code=r"""
            .grid-fill {
              display: grid;
              grid-template-columns: repeat(auto-fill, minmax(min(200px, 100%), 1fr));
              gap: 16px;
            }

            .grid-fit {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr));
              gap: 16px;
            }
        """,
        lang="css",
        follow=[
            ("Why does `minmax(min(200px, 100%), 1fr)` prevent overflow?", "`minmax(min(200px, 100%), 1fr)` কেন overflow ঠেকায়?"),
            ("When would you choose container queries over this pattern?", "কখন এই pattern-এর বদলে container query বেছে নেবে?"),
        ],
        related=["css-006", "css-016"],
        refs=[MDN_REPEAT, MDN_MINMAX, WEBDEV_GRID],
    ),
    # ------------------------------------------------------------------ css-016
    Q(
        id="css-016", sub="Container Queries", diff="medium", type="conceptual",
        prio="high", market="both", mins=6,
        tags=["container-queries", "responsive", "components", "cqi", "style-queries"],
        ver="CSS Containment 3; size queries Baseline widely available; style queries Baseline newly available (May 2026)", vs=True, status="stable",
        q_en=r"""What problem do container queries solve that media queries can't? Show how you'd use them for a product card, and explain the rules and pitfalls.""",
        q_bn=r"""Container query এমন কোন সমস্যার সমাধান করে যা media query পারে না? একটা product card-এ কীভাবে ব্যবহার করবে দেখাও, আর এর নিয়ম ও ফাঁদগুলো ব্যাখ্যা করো।""",
        a_en=r"""
            Media queries look at the **viewport**. But a reusable component doesn't care how wide the screen is — it cares how much space **its slot** has. The same product card might sit in a wide main column and in a narrow sidebar on the same desktop page. Container queries let the card respond to its **container's** size.

            How it works:
            1. Mark an ancestor as a container: `container-type: inline-size` (optionally named with `container-name`).
            2. Write `@container (min-width: 420px) { … }` — the rules apply to **descendants** of that container when it matches.
            3. Use container units like `cqi` (1% of the container's inline size) for fluid sizing inside the component.

            Size queries are Baseline widely available. **Style queries** — `@container style(--variant: sale)`, which react to a custom property's value — became Baseline newly available in May 2026, so I treat them as progressive enhancement for now.
        """,
        a_bn=r"""
            Media query দেখে **viewport**। কিন্তু একটা reusable component-এর কাছে screen কত চওড়া তা গুরুত্বপূর্ণ নয় — গুরুত্বপূর্ণ হলো **তার নিজের জায়গায়** কতটা space আছে। একই desktop page-এ একই product card চওড়া main column-এও থাকতে পারে, আবার সরু sidebar-এও। Container query card-কে তার **container**-এর মাপ অনুযায়ী সাড়া দিতে দেয়।

            কীভাবে কাজ করে:
            1. একটা ancestor-কে container হিসেবে চিহ্নিত করো: `container-type: inline-size` (চাইলে `container-name` দিয়ে নামও দাও)।
            2. `@container (min-width: 420px) { … }` লেখো — container match করলে তার **descendant**-দের উপর rule-গুলো প্রযোজ্য হয়।
            3. Component-এর ভেতরে fluid sizing-এর জন্য `cqi`-এর মতো container unit ব্যবহার করো (container-এর inline size-এর 1%)।

            Size query Baseline widely available। **Style query** — `@container style(--variant: sale)`, যা কোনো custom property-র value-তে সাড়া দেয় — May 2026-এ Baseline newly available হয়েছে, তাই আপাতত আমি এটাকে progressive enhancement হিসেবে ব্যবহার করি।
        """,
        quick_en=r"""Media queries respond to the viewport; container queries respond to the component's own slot. Set `container-type: inline-size` on a parent, then `@container (min-width: 420px)` styles the card inside it. Size queries are widely available; style queries only became newly available in May 2026.""",
        quick_bn=r"""Media query viewport দেখে; container query দেখে component যে জায়গায় বসেছে সেটা। Parent-এ `container-type: inline-size` দাও, তারপর `@container (min-width: 420px)` ভেতরের card-কে style করে। Size query widely available; style query মাত্র May 2026-এ newly available হয়েছে।""",
        ex_en=r"""
            **Rules and pitfalls:**
            - **A container can't query itself.** `@container` rules style its descendants. Put `container-type` on a wrapper (the slot), not on the card you want to restyle.
            - **Containment side effects:** `inline-size` containment means the container's width can't depend on its children. On a shrink-to-fit element (an inline-block, a flex item without a set width, an absolutely positioned box) the container can collapse to zero width. Put it on elements whose width comes from the layout.
            - **`container-type: size`** also contains the block axis, so the element needs an explicit height — rarely what you want for content components.
            - **Media vs container:** keep media queries for page-level (macro) layout and user preferences (`prefers-reduced-motion`, `prefers-color-scheme`); use container queries for component (micro) layout.
            - **Style queries** currently work with custom properties; they're handy for variants (`--variant: sale`) without adding modifier classes everywhere.
        """,
        ex_bn=r"""
            **নিয়ম আর ফাঁদ:**
            - **Container নিজেকে query করতে পারে না।** `@container` rule তার descendant-দের style করে। যে card-এর style বদলাতে চাও তাতে নয়, বরং wrapper-এ (অর্থাৎ slot-এ) `container-type` দাও।
            - **Containment-এর পার্শ্বপ্রতিক্রিয়া:** `inline-size` containment মানে container-এর width তার children-এর উপর নির্ভর করতে পারে না। Shrink-to-fit element-এ (inline-block, width ঠিক করা নেই এমন flex item, absolutely positioned box) container-এর width শূন্যে নেমে যেতে পারে। যেসব element-এর width layout থেকে আসে, সেগুলোতে এটা দাও।
            - **`container-type: size`** block axis-ও contain করে, তাই element-এর স্পষ্ট height লাগে — content component-এর জন্য খুব কমই এটা চাওয়া হয়।
            - **Media বনাম container:** page-level (macro) layout আর user preference-এর (`prefers-reduced-motion`, `prefers-color-scheme`) জন্য media query রাখো; component-এর (micro) layout-এর জন্য container query ব্যবহার করো।
            - **Style query** এখন custom property-র সাথে কাজ করে; সব জায়গায় modifier class না যোগ করে variant (`--variant: sale`) সামলাতে এটা কাজের।
        """,
        tip_en=r"""Open with the "same card in a sidebar and in the main column" example — it makes the problem obvious in one sentence. Then mention "a container can't query itself"; that's the mistake almost everyone makes first.""",
        tip_bn=r""""একই card sidebar-এও, main column-এও" — এই উদাহরণ দিয়ে শুরু করো, এক বাক্যেই সমস্যাটা পরিষ্কার হয়ে যায়। তারপর বলো "container নিজেকে query করতে পারে না"; প্রায় সবাই প্রথমে এই ভুলটাই করে।""",
        mist_en=r"""Putting `container-type` on the element you're trying to restyle, using `container-type: size` without a height, or replacing all media queries with container queries.""",
        mist_bn=r"""যে element-এর style বদলাতে চাও তাতেই `container-type` দেওয়া, height ছাড়া `container-type: size` ব্যবহার করা, অথবা সব media query container query দিয়ে বদলে ফেলা।""",
        code=r"""
            /* The slot is the container, not the card */
            .main-column,
            .sidebar {
              container-type: inline-size;
            }

            .card { display: grid; gap: 0.5rem; }
            .card-title { font-size: clamp(1rem, 0.9rem + 2cqi, 1.375rem); }

            @container (min-width: 420px) {
              .card {
                grid-template-columns: 140px 1fr;
                align-items: start;
              }
            }

            /* Style query (Baseline newly available): react to a custom property */
            .promo-slot { --variant: sale; }
            @container style(--variant: sale) {
              .card-badge { display: inline-block; }
            }
        """,
        lang="css",
        follow=[
            ("Why might an element with `container-type: inline-size` suddenly collapse to zero width?", "`container-type: inline-size` দেওয়া element কেন হঠাৎ শূন্য width-এ নেমে আসতে পারে?"),
            ("When would you still use a media query instead of a container query?", "কখন container query-র বদলে এখনো media query ব্যবহার করবে?"),
        ],
        related=["css-015", "css-032"],
        refs=[MDN_CQ, MDN_CONTAINER],
    ),
    # ------------------------------------------------------------------ css-017
    Q(
        id="css-017", sub="CSS Variables", diff="medium", type="comparison",
        prio="high", market="both", mins=5,
        tags=["custom-properties", "sass", "theming", "variables"],
        ver="Version-independent (CSS Custom Properties; Sass)", vs=False, status="stable",
        q_en=r"""How are CSS custom properties (`--brand`) different from preprocessor variables like Sass `$brand`? When would you use each?""",
        q_bn=r"""CSS custom property (`--brand`) আর Sass-এর `$brand`-এর মতো preprocessor variable-এর মধ্যে পার্থক্য কী? কখন কোনটা ব্যবহার করবে?""",
        a_en=r"""
            **Sass variables are compile-time constants.** The build replaces `$brand` with its value; the browser never sees the variable. They follow Sass's lexical scope, can be used anywhere in the source (including media query conditions and selectors) and support build-time maths, loops and mixins.

            **Custom properties are runtime values in the cascade.** They're set on elements, **inherit** down the DOM, can be overridden per component, per media query or per theme, can be read and changed with JavaScript (`el.style.setProperty('--brand', …)`), and show up in DevTools. But they can't be used in media query conditions (`@media (min-width: var(--bp))` doesn't work) or in selectors.

            I use **custom properties for anything that changes at runtime or by context** — themes, dark mode, design tokens, component variants — and Sass (if the project uses it) for build-time concerns like breakpoint constants and mixins.
        """,
        a_bn=r"""
            **Sass variable হলো compile-time constant।** Build-এর সময় `$brand` তার value দিয়ে বদলে যায়; browser কখনো variable-টা দেখেই না। এগুলো Sass-এর lexical scope মেনে চলে, source-এর যেকোনো জায়গায় ব্যবহার করা যায় (media query-র condition আর selector-সহ), আর build-time-এর হিসাব, loop আর mixin support করে।

            **Custom property হলো cascade-এর ভেতরের runtime value।** এগুলো element-এ set হয়, DOM ধরে নিচে **inherit** হয়, প্রতিটা component, media query বা theme অনুযায়ী override করা যায়, JavaScript দিয়ে পড়া ও বদলানো যায় (`el.style.setProperty('--brand', …)`), আর DevTools-এ দেখা যায়। তবে media query-র condition-এ (`@media (min-width: var(--bp))` কাজ করে না) বা selector-এ এগুলো ব্যবহার করা যায় না।

            **Runtime-এ বা context অনুযায়ী যা বদলায়** — theme, dark mode, design token, component variant — তার জন্য আমি custom property ব্যবহার করি, আর project-এ Sass থাকলে build-time-এর কাজের জন্য (breakpoint constant, mixin) Sass।
        """,
        quick_en=r"""Sass variables are compile-time constants the browser never sees; custom properties are runtime values that inherit, can be overridden per context and changed with JavaScript, but can't be used in media query conditions. I use custom properties for themes and tokens, Sass for build-time constants.""",
        quick_bn=r"""Sass variable compile-time constant, browser এগুলো দেখেই না; custom property runtime value, inherit হয়, context অনুযায়ী override করা যায় আর JavaScript দিয়ে বদলানো যায়, তবে media query condition-এ চলে না। Theme আর token-এর জন্য আমি custom property, আর build-time constant-এর জন্য Sass ব্যবহার করি।""",
        ex_en=r"""
            - **Dark mode shows the difference best:** with Sass you'd compile two stylesheets or duplicate rules; with custom properties you override a handful of tokens under `[data-theme="dark"]` and every component updates instantly.
            - **Invalid values behave differently:** if `--gap: red` is used in `margin: var(--gap)`, the declaration becomes "invalid at computed-value time" and the property falls back to its inherited or initial value — not to the `var()` fallback. `@property` can register a type to make this stricter and enable animation.
            - **Performance note:** changing a custom property high in the tree (on `:root`) restyles everything that inherits it. Usually fine, but avoid animating root-level custom properties every frame; register with `inherits: false` where inheritance isn't needed.
            - **Native CSS has caught up on many Sass features** — nesting, `color-mix()`, `calc()`, cascade layers — so many new projects use plain CSS plus a bundler.
        """,
        ex_bn=r"""
            - **Dark mode-এ পার্থক্যটা সবচেয়ে ভালো বোঝা যায়:** Sass-এ দুটো stylesheet compile করতে হতো বা rule duplicate করতে হতো; custom property দিয়ে `[data-theme="dark"]`-এর নিচে কয়েকটা token override করলেই প্রতিটা component সঙ্গে সঙ্গে আপডেট হয়।
            - **Invalid value-এর আচরণ আলাদা:** `margin: var(--gap)`-এ যদি `--gap: red` ব্যবহার হয়, declaration-টা "invalid at computed-value time" হয়ে যায় আর property তার inherited বা initial value-তে ফিরে যায় — `var()`-এর fallback-এ নয়। `@property` দিয়ে type register করলে এটা আরও কড়া হয় আর animation-ও সম্ভব হয়।
            - **Performance-এর কথা:** tree-এর উঁচুতে (`:root`-এ) একটা custom property বদলালে যারা এটা inherit করে তাদের সবার style আবার হিসাব হয়। সাধারণত ঠিক আছে, কিন্তু প্রতি frame-এ root-level custom property animate কোরো না; inheritance দরকার না হলে `inherits: false` দিয়ে register করো।
            - **Native CSS এখন Sass-এর অনেক feature ধরে ফেলেছে** — nesting, `color-mix()`, `calc()`, cascade layer — তাই অনেক নতুন project শুধু plain CSS আর একটা bundler ব্যবহার করে।
        """,
        tip_en=r"""Use the words "compile-time" vs "runtime + cascade" early, then prove it with dark mode. Mentioning that custom properties can't be used in media query conditions shows you've hit the limit in practice.""",
        tip_bn=r"""শুরুতেই "compile-time" বনাম "runtime + cascade" শব্দগুলো ব্যবহার করো, তারপর dark mode দিয়ে প্রমাণ করো। Custom property যে media query-র condition-এ ব্যবহার করা যায় না — এটা বললে বোঝা যায় তুমি বাস্তবে এই সীমায় ধাক্কা খেয়েছ।""",
        mist_en=r"""Calling custom properties "global variables" (they're scoped to elements and inherit), trying `@media (min-width: var(--bp))`, or expecting the `var()` fallback to rescue a value of the wrong type.""",
        mist_bn=r"""Custom property-কে "global variable" বলা (এগুলো element-ভিত্তিক scope-এ থাকে আর inherit হয়), `@media (min-width: var(--bp))` চেষ্টা করা, অথবা ভুল type-এর value-কে `var()`-এর fallback রক্ষা করবে বলে আশা করা।""",
        code=r"""
            /* Sass (compile-time): fine for build constants */
            $bp-tablet: 48rem;
            @media (min-width: $bp-tablet) { .grid { grid-template-columns: 1fr 1fr; } }

            /* CSS custom properties (runtime, cascade-aware) */
            :root {
              --brand: #0b6e4f;
              --surface: #ffffff;
              --text: #1a1a1a;
            }
            [data-theme="dark"] {
              --surface: #121212;
              --text: #f1f1f1;
            }
            .card {
              background: var(--surface);
              color: var(--text);
              border-top: 4px solid var(--brand);
            }
            .card.is-sale { --brand: #c1121f; }   /* per-component override */
        """,
        lang="css",
        follow=[
            ("Why doesn't `@media (min-width: var(--bp))` work?", "`@media (min-width: var(--bp))` কেন কাজ করে না?"),
            ("What does \"invalid at computed-value time\" mean for custom properties?", "Custom property-র ক্ষেত্রে \"invalid at computed-value time\" মানে কী?"),
        ],
        related=["css-009", "css-026"],
        refs=[MDN_VAR, MDN_PROPERTY],
    ),
    # ------------------------------------------------------------------ css-024
    Q(
        id="css-024", sub="Performance", diff="hard", type="security-performance",
        prio="high", market="both", mins=8,
        tags=["rendering-pipeline", "reflow", "repaint", "compositing", "will-change"],
        ver="Version-independent concept (browser rendering)", vs=False, status="stable",
        q_en=r"""Walk me through the browser's rendering pipeline from a CSS point of view. Which property changes trigger layout, which trigger paint, and which only compositing? Why is `will-change` so often misused?""",
        q_bn=r"""CSS-এর দৃষ্টিকোণ থেকে browser-এর rendering pipeline ব্যাখ্যা করো। কোন property বদলালে layout হয়, কোনটায় paint, আর কোনটায় শুধু compositing? `will-change` কেন এত বেশি ভুলভাবে ব্যবহার হয়?""",
        a_en=r"""
            The pipeline after a change is roughly **Style → Layout → Paint → Composite**, and you pay for every stage from the first one your change touches:
            - **Layout (reflow):** geometry changes — `width`, `height`, `top`/`left`, `margin`, `padding`, `font-size`, `border-width`, adding/removing elements. The browser recalculates positions and sizes, often for ancestors and siblings too, then repaints.
            - **Paint (repaint):** visual-only changes — `color`, `background`, `box-shadow`, `border-radius`, `outline`. No geometry change, but pixels must be redrawn.
            - **Composite only:** `transform` and `opacity` on an element that has its own compositor layer. The compositor just moves or fades an existing bitmap, often off the main thread, so it stays smooth even when JavaScript is busy.

            So for animations I use `transform: translate()` instead of animating `left`, `scale()` instead of `width`, and `opacity` for fades.

            **`will-change`** tells the browser in advance that a property will change, so it can promote the element to its own layer. It's misused when applied broadly or permanently:
            - every layer costs GPU memory — hundreds of `will-change: transform` cards can exhaust memory on low-end phones and make things slower;
            - it creates a **stacking context** and, for `transform`, a **containing block** for fixed-position descendants — which can break `z-index` and `position: fixed` layouts;
            - browsers already promote elements that are actively animating `transform`/`opacity`.

            Use it sparingly, just before an animation starts, and remove it afterwards.
        """,
        a_bn=r"""
            কোনো পরিবর্তনের পর pipeline মোটামুটি এরকম: **Style → Layout → Paint → Composite**, আর তোমার পরিবর্তন যে ধাপ থেকে শুরু হয়, সেখান থেকে পরের প্রতিটা ধাপের খরচ দিতে হয়:
            - **Layout (reflow):** geometry-র পরিবর্তন — `width`, `height`, `top`/`left`, `margin`, `padding`, `font-size`, `border-width`, element যোগ/বাদ দেওয়া। Browser অবস্থান আর মাপ আবার হিসাব করে, প্রায়ই ancestor আর sibling-দেরও, তারপর আবার paint করে।
            - **Paint (repaint):** শুধু দেখার পরিবর্তন — `color`, `background`, `box-shadow`, `border-radius`, `outline`। Geometry বদলায় না, কিন্তু pixel আবার আঁকতে হয়।
            - **শুধু Composite:** যে element-এর নিজস্ব compositor layer আছে তাতে `transform` আর `opacity`। Compositor শুধু আগে থেকে তৈরি bitmap সরায় বা ঝাপসা করে, প্রায়ই main thread-এর বাইরে, তাই JavaScript ব্যস্ত থাকলেও এটা মসৃণ থাকে।

            তাই animation-এর জন্য আমি `left` animate না করে `transform: translate()`, `width`-এর বদলে `scale()`, আর fade-এর জন্য `opacity` ব্যবহার করি।

            **`will-change`** browser-কে আগেই জানায় যে একটা property বদলাবে, যাতে সে element-টাকে নিজস্ব layer-এ নিয়ে যেতে পারে। ব্যাপকভাবে বা স্থায়ীভাবে দিলে এটা অপব্যবহার হয়:
            - প্রতিটা layer GPU memory খায় — শত শত `will-change: transform` card low-end phone-এর memory শেষ করে দিতে পারে আর সবকিছু আরও ধীর করে দেয়;
            - এটা একটা **stacking context** তৈরি করে, আর `transform`-এর ক্ষেত্রে fixed-position descendant-দের জন্য একটা **containing block**-ও — ফলে `z-index` আর `position: fixed` layout ভেঙে যেতে পারে;
            - যে element সক্রিয়ভাবে `transform`/`opacity` animate করছে, browser এমনিতেই সেটাকে promote করে।

            এটা কম ব্যবহার করো — animation শুরুর ঠিক আগে দাও, আর পরে সরিয়ে ফেলো।
        """,
        quick_en=r"""Style → Layout → Paint → Composite: geometry changes like `width` or `top` trigger layout, visual ones like `color` trigger paint, and `transform`/`opacity` can be composite-only. `will-change` is misused when applied widely, because every layer costs GPU memory and creates a stacking context.""",
        quick_bn=r"""Style → Layout → Paint → Composite: `width` বা `top`-এর মতো geometry বদলালে layout, `color`-এর মতো চেহারা বদলালে paint, আর `transform`/`opacity` শুধু composite-এই হতে পারে। `will-change` ঢালাওভাবে দিলে সমস্যা, কারণ প্রতিটা layer GPU memory খায় আর stacking context তৈরি করে।""",
        ex_en=r"""
            - **Layout thrashing:** reading layout (`offsetHeight`, `getBoundingClientRect()`) right after writing styles forces a synchronous layout. Doing that in a loop multiplies the cost — batch all reads, then all writes.
            - **"Cheap" isn't free:** a large blurred `box-shadow`, `filter: blur()` or `backdrop-filter` can make *paint* or *composite* expensive, especially on mobile GPUs.
            - **Scope the work:** `contain: layout paint` (or `content-visibility: auto` for off-screen sections) limits how far a change propagates.
            - **Measure, don't guess:** the DevTools Performance panel shows Layout/Paint blocks and forced-reflow warnings; the Rendering tab's *Paint flashing* and *Layer borders*, and the Layers panel, show what repaints and what got promoted.
        """,
        ex_bn=r"""
            - **Layout thrashing:** style লেখার ঠিক পরেই layout পড়লে (`offsetHeight`, `getBoundingClientRect()`) browser-কে synchronous layout করতে বাধ্য করা হয়। Loop-এর ভেতরে এটা করলে খরচ বহুগুণ বাড়ে — সব read একসাথে, তারপর সব write।
            - **"সস্তা" মানে ফ্রি নয়:** বড় ঝাপসা `box-shadow`, `filter: blur()` বা `backdrop-filter` *paint* বা *composite*-কে ব্যয়বহুল করে তুলতে পারে, বিশেষ করে mobile GPU-তে।
            - **কাজের পরিধি সীমিত করো:** `contain: layout paint` (বা screen-এর বাইরের section-এর জন্য `content-visibility: auto`) একটা পরিবর্তন কতদূর ছড়াবে তা সীমিত করে।
            - **আন্দাজ নয়, মাপো:** DevTools-এর Performance panel Layout/Paint block আর forced-reflow warning দেখায়; Rendering tab-এর *Paint flashing* আর *Layer borders*, আর Layers panel দেখায় কী আবার paint হচ্ছে আর কী promote হয়েছে।
        """,
        tip_en=r"""Draw the four boxes (Style → Layout → Paint → Composite) and map each property group to its entry point. Then name *two* concrete downsides of `will-change` — memory and stacking/containing-block side effects — rather than just "don't overuse it".""",
        tip_bn=r"""চারটা ধাপ এঁকে দেখাও (Style → Layout → Paint → Composite), আর প্রতিটা property-গোষ্ঠী কোন ধাপ থেকে শুরু হয় তা মিলিয়ে দাও। তারপর শুধু "বেশি ব্যবহার কোরো না" না বলে `will-change`-এর *দুটো* নির্দিষ্ট অসুবিধা বলো — memory আর stacking/containing-block-এর পার্শ্বপ্রতিক্রিয়া।""",
        mist_en=r"""Adding `will-change: transform` (or `translateZ(0)`) to everything "for GPU acceleration", animating `top`/`left` or `height`, and assuming composited properties have no cost at all.""",
        mist_bn=r""""GPU acceleration-এর জন্য" সবকিছুতে `will-change: transform` (বা `translateZ(0)`) দেওয়া, `top`/`left` বা `height` animate করা, আর ধরে নেওয়া যে composited property-র কোনো খরচই নেই।""",
        code=r"""
            /* Janky: animates layout every frame */
            .drawer-bad { transition: left 300ms ease; left: -320px; }
            .drawer-bad.open { left: 0; }

            /* Smooth: compositor-only */
            .drawer {
              transform: translateX(-100%);
              transition: transform 300ms ease;
            }
            .drawer.open { transform: translateX(0); }

            /* will-change only while it's about to animate */
            .menu-button:hover + .drawer,
            .menu-button:focus-visible + .drawer {
              will-change: transform;
            }
        """,
        lang="css",
        follow=[
            ("What is layout thrashing, and how do you fix it in JavaScript?", "Layout thrashing কী, আর JavaScript-এ কীভাবে ঠিক করবে?"),
            ("Why can `will-change: transform` break a `position: fixed` child?", "`will-change: transform` কেন একটা `position: fixed` child ভেঙে দিতে পারে?"),
        ],
        related=["css-019", "css-031"],
        refs=[WEBDEV_RENDERING_PERF, WEBDEV_COMPOSITOR, MDN_WILL_CHANGE],
    ),
    # ------------------------------------------------------------------ css-025
    Q(
        id="css-025", sub="CSS Grid", diff="hard", type="scenario",
        prio="medium", market="both", mins=8,
        tags=["subgrid", "grid", "alignment", "cards"],
        ver="CSS Grid Level 2; subgrid Baseline widely available", vs=False, status="stable",
        q_en=r"""Product cards in a responsive grid each have an image, a title (1–3 lines), a price and an "Add to cart" button. The designer complains that titles, prices and buttons don't line up across cards in the same row. How would you fix this with CSS only?""",
        q_bn=r"""একটা responsive grid-এর প্রতিটা product card-এ আছে একটা image, একটা title (1–3 লাইন), দাম আর "Add to cart" button। Designer অভিযোগ করছে, একই row-এর card-গুলোতে title, দাম আর button এক লাইনে মিলছে না। শুধু CSS দিয়ে কীভাবে ঠিক করবে?""",
        a_en=r"""
            **The cause:** each card is laid out independently, so a card with a three-line title pushes its price and button lower than its neighbours.

            **The fix: subgrid.** Let each card span several rows of the *parent* grid and adopt those rows as its own:
            - The parent grid defines the columns (e.g. `repeat(auto-fill, minmax(min(14rem, 100%), 1fr))`); rows are created implicitly.
            - Each card gets `grid-row: span 4` (image, title, price, button), `display: grid` and `grid-template-rows: subgrid`.
            - Now the internal rows of every card in the same visual row share **the same track sizes** — the tallest title in that row sets the title row's height for all cards, so prices and buttons line up.

            Subgrid is Baseline widely available, so this is production-safe.

            **Before subgrid,** people used fixed heights with title truncation (loses content), JavaScript that equalised heights on resize (fragile, causes layout shift), or a flex column with `margin-top: auto` on the button (aligns the buttons but not titles or prices).
        """,
        a_bn=r"""
            **কারণ:** প্রতিটা card আলাদাভাবে layout হয়, তাই তিন লাইনের title থাকা card তার দাম আর button-কে পাশের card-গুলোর চেয়ে নিচে ঠেলে দেয়।

            **সমাধান: subgrid।** প্রতিটা card-কে *parent* grid-এর কয়েকটা row জুড়ে বসাও, আর সেই row-গুলোকেই নিজের row হিসেবে নিতে দাও:
            - Parent grid column ঠিক করে (যেমন `repeat(auto-fill, minmax(min(14rem, 100%), 1fr))`); row তৈরি হয় implicitly।
            - প্রতিটা card পায় `grid-row: span 4` (image, title, দাম, button), `display: grid` আর `grid-template-rows: subgrid`।
            - এখন একই দৃশ্যমান row-এর প্রতিটা card-এর ভেতরের row-গুলো **একই track size** ভাগ করে — ওই row-এর সবচেয়ে লম্বা title সব card-এর title row-এর height ঠিক করে, ফলে দাম আর button এক লাইনে চলে আসে।

            Subgrid Baseline widely available, তাই production-এ নিরাপদ।

            **Subgrid-এর আগে** মানুষ ব্যবহার করত title কেটে দিয়ে fixed height (content হারায়), resize-এ height সমান করা JavaScript (ভঙ্গুর, layout shift ঘটায়), অথবা button-এ `margin-top: auto`-সহ flex column (button মেলে, কিন্তু title বা দাম মেলে না)।
        """,
        quick_en=r"""Use subgrid: the parent grid defines the columns, and each card spans four rows with `display: grid; grid-template-rows: subgrid`, so cards in the same row share track sizes and titles, prices and buttons line up. Subgrid is Baseline widely available.""",
        quick_bn=r"""Subgrid ব্যবহার করো: parent grid column ঠিক করে, আর প্রতিটা card `display: grid; grid-template-rows: subgrid` দিয়ে চারটা row জুড়ে থাকে, তাই একই সারির card-গুলো একই track size পায় আর title, price, button এক লাইনে আসে। Subgrid Baseline widely available।""",
        ex_en=r"""
            - **Gaps:** a subgrid inherits the parent's gaps. If the parent uses a large `row-gap` between card rows, set a smaller `row-gap` on the card to override it inside the card.
            - **Count must match:** the `span` must equal the number of child rows. An extra element (e.g. a "Sale" badge) needs its own row, or must be positioned so it doesn't create a new track.
            - **Card padding and borders** still work — they sit outside the subgridded tracks.
            - **Why not `display: contents`?** Dropping the card's box loses its background, border and, historically in some browsers, its semantics/accessibility role — subgrid keeps the card as a real box.
            - **Mixed content:** cards without an image should still output an (empty) image row, or the alignment shifts.
        """,
        ex_bn=r"""
            - **Gap:** subgrid parent-এর gap inherit করে। Parent যদি card-এর row-গুলোর মাঝে বড় `row-gap` ব্যবহার করে, তাহলে card-এর ভেতরে override করতে card-এ ছোট একটা `row-gap` দাও।
            - **সংখ্যা মিলতে হবে:** `span` অবশ্যই child row-এর সংখ্যার সমান হতে হবে। বাড়তি কোনো element (যেমন "Sale" badge)-এর নিজের row লাগবে, অথবা এমনভাবে position করতে হবে যাতে নতুন track তৈরি না হয়।
            - **Card-এর padding আর border** তখনো কাজ করে — এগুলো subgrid করা track-গুলোর বাইরে থাকে।
            - **`display: contents` কেন নয়?** Card-এর box বাদ দিলে তার background, border, আর কিছু browser-এ অতীতে তার semantics/accessibility role-ও হারিয়ে যেত — subgrid card-কে আসল box হিসেবেই রাখে।
            - **মিশ্র content:** যে card-এ image নেই, তাকেও একটা (খালি) image row রাখতে হবে, নইলে সারিবদ্ধতা সরে যায়।
        """,
        tip_en=r"""Explain the cause before the fix ("each card is its own layout context"), then show subgrid. Briefly listing the pre-subgrid workarounds and their downsides shows why subgrid is the right tool.""",
        tip_bn=r"""সমাধানের আগে কারণটা ব্যাখ্যা করো ("প্রতিটা card নিজস্ব layout context"), তারপর subgrid দেখাও। Subgrid-এর আগের workaround আর তাদের অসুবিধা সংক্ষেপে বললে বোঝা যায় কেন subgrid-ই সঠিক tool।""",
        mist_en=r"""Fixing it with fixed heights or JavaScript, forgetting `grid-row: span N` on the card (then `subgrid` has only one row to inherit), or a mismatch between the span and the number of children.""",
        mist_bn=r"""Fixed height বা JavaScript দিয়ে ঠিক করা, card-এ `grid-row: span N` দিতে ভুলে যাওয়া (তখন `subgrid`-এর inherit করার মতো মাত্র একটা row থাকে), অথবা span আর children-এর সংখ্যায় অমিল।""",
        code=r"""
            <ul class="products">
              <li class="card">
                <img src="/p/panjabi.jpg" alt="Navy cotton panjabi" width="320" height="400">
                <h3>Cotton Panjabi — Navy, Slim Fit, Eid Collection 2026</h3>
                <p class="price">৳1,850</p>
                <button type="button">Add to cart</button>
              </li>
              <!-- more cards -->
            </ul>

            <style>
              .products {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(min(14rem, 100%), 1fr));
                gap: 1.5rem 1rem;
                list-style: none;
                padding: 0;
              }
              .card {
                display: grid;
                grid-row: span 4;              /* image, title, price, button */
                grid-template-rows: subgrid;
                row-gap: 0.5rem;               /* tighter than the parent's 1.5rem */
                padding: 0.75rem;
                border: 1px solid #ddd;
                border-radius: 12px;
              }
              .card img { width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; }
              .card .price { align-self: end; }
            </style>
        """,
        lang="html",
        follow=[
            ("How would you handle a card that sometimes has an extra 'Sale' badge row?", "যে card-এ মাঝে মাঝে বাড়তি একটা 'Sale' badge row থাকে, সেটা কীভাবে সামলাবে?"),
            ("Can subgrid be used for columns as well as rows? Give an example.", "Subgrid কি row-এর মতো column-এর জন্যও ব্যবহার করা যায়? উদাহরণ দাও।"),
        ],
        related=["css-006", "css-015"],
        refs=[MDN_SUBGRID, WEBDEV_GRID],
    ),
]

if __name__ == "__main__":
    save("css", "b2", QUESTIONS)
