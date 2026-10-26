import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_BOX_SIZING = ("MDN — box-sizing", "https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing")
WEBDEV_BOX_MODEL = ("web.dev — Learn CSS: Box model", "https://web.dev/learn/css/box-model")
WEBDEV_SPECIFICITY = ("web.dev — Learn CSS: Specificity", "https://web.dev/learn/css/specificity")
WEBDEV_INHERITANCE = ("web.dev — Learn CSS: Inheritance", "https://web.dev/learn/css/inheritance")
WEBDEV_CASCADE = ("web.dev — Learn CSS: The cascade", "https://web.dev/learn/css/the-cascade")
MDN_LAYER = ("MDN — @layer", "https://developer.mozilla.org/en-US/docs/Web/CSS/@layer")
MDN_HAS = ("MDN — :has()", "https://developer.mozilla.org/en-US/docs/Web/CSS/:has")
MDN_MIN_WIDTH = ("MDN — min-width", "https://developer.mozilla.org/en-US/docs/Web/CSS/min-width")
MDN_OVERFLOW_WRAP = ("MDN — overflow-wrap", "https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap")
WEBDEV_FLEXBOX = ("web.dev — Learn CSS: Flexbox", "https://web.dev/learn/css/flexbox")
MDN_IS = ("MDN — :is()", "https://developer.mozilla.org/en-US/docs/Web/CSS/:is")
MDN_WHERE = ("MDN — :where()", "https://developer.mozilla.org/en-US/docs/Web/CSS/:where")
MDN_SCOPE = ("MDN — @scope", "https://developer.mozilla.org/en-US/docs/Web/CSS/@scope")
MDN_LIGHT_DARK = ("MDN — light-dark()", "https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark")

QUESTIONS = [
    # ------------------------------------------------------------------ css-001
    Q(
        id="css-001", sub="Box Model", diff="easy", type="output",
        prio="high", market="bangladesh", mins=3,
        tags=["box-model", "box-sizing", "padding", "margin", "output"],
        ver="Version-independent (CSS)", vs=False, status="stable",
        q_en=r"""What is the rendered width (border edge to border edge) of `.a` and of `.b`, and how wide is the content area of `.b`? How much vertical space separates the two boxes?""",
        q_bn=r"""`.a` আর `.b`-এর rendered width (এক border থেকে আরেক border পর্যন্ত) কত, আর `.b`-এর content area কতটা চওড়া? দুটো box-এর মাঝে vertical ফাঁক কতটুকু?""",
        code=r"""
            <div class="a">A</div>
            <div class="b">B</div>

            <style>
              .a, .b {
                width: 200px;
                padding: 20px;
                border: 5px solid #333;
                margin: 10px;
              }
              .b { box-sizing: border-box; }
            </style>
        """,
        lang="html",
        output=r"""
            .a → 250px wide (200 content + 2×20 padding + 2×5 border)
            .b → 200px wide; its content area shrinks to 150px
            Gap between them → 10px (the vertical margins collapse)
        """,
        a_en=r"""
            With the default `box-sizing: content-box`, `width` sets only the **content** width; padding and border are added on top, so `.a` is 200 + 40 + 10 = **250px**. With `box-sizing: border-box`, `width` includes padding and border, so `.b` stays **200px** and its content area becomes 200 − 40 − 10 = **150px**. Margin is never part of the box's width.

            The gap between them is **10px**, not 20px: adjacent vertical margins of block boxes in normal flow **collapse** to the larger of the two.
        """,
        a_bn=r"""
            Default `box-sizing: content-box`-এ `width` শুধু **content**-এর width ঠিক করে; padding আর border তার উপর যোগ হয়, তাই `.a` হয় 200 + 40 + 10 = **250px**। `box-sizing: border-box`-এ `width`-এর মধ্যেই padding আর border ধরা হয়, তাই `.b` **200px**-ই থাকে আর তার content area হয় 200 − 40 − 10 = **150px**। Margin কখনো box-এর width-এর অংশ নয়।

            দুটোর মাঝের ফাঁক **10px**, 20px নয়: normal flow-তে পাশাপাশি থাকা block box-এর vertical margin **collapse** করে দুটোর মধ্যে বড়টার সমান হয়।
        """,
        quick_en=r"""`.a` is 250px wide because `content-box` adds padding and border to `width`; `.b` is 200px with a 150px content area because `border-box` includes them. The gap is 10px, since adjacent vertical margins collapse to the larger one.""",
        quick_bn=r"""`.a` 250px চওড়া, কারণ `content-box`-এ `width`-এর সাথে padding আর border যোগ হয়; `.b` 200px আর তার content area 150px, কারণ `border-box`-এ এগুলো `width`-এর ভেতরেই। মাঝের gap 10px, কারণ পাশাপাশি vertical margin collapse হয়ে বড়টা থাকে।""",
        ex_en=r"""
            - **Why teams reset to `border-box`:** it makes `width: 50%` plus padding behave intuitively. The common reset is `*, *::before, *::after { box-sizing: border-box; }`.
            - **Edge case:** with `border-box`, if padding + border exceed the width, the content area becomes 0 and the box grows anyway.
            - **Margin collapsing** only happens to vertical margins of blocks in normal flow. It doesn't happen inside flex or grid containers, or for floated/absolutely positioned elements, which is why the same margins can "double" after switching a parent to `display: flex`.
            - **DevTools:** the box-model diagram in the Computed tab shows content, padding, border and margin values — the fastest way to settle "why is this box wider than I expected?".
        """,
        ex_bn=r"""
            - **Team-রা কেন `border-box`-এ reset করে:** এতে padding-সহ `width: 50%` প্রত্যাশামতো আচরণ করে। সাধারণ reset হলো `*, *::before, *::after { box-sizing: border-box; }`।
            - **Edge case:** `border-box`-এ padding + border যদি width-এর চেয়ে বেশি হয়, তাহলে content area 0 হয়ে যায় আর box তবুও বড় হয়।
            - **Margin collapsing** শুধু normal flow-এর block-এর vertical margin-এ ঘটে। Flex বা grid container-এর ভেতরে, কিংবা float/absolutely positioned element-এ এটা হয় না — তাই parent-কে `display: flex` করার পর একই margin "দ্বিগুণ" হয়ে যেতে পারে।
            - **DevTools:** Computed tab-এর box-model diagram-এ content, padding, border আর margin-এর মান দেখা যায় — "box-টা কেন প্রত্যাশার চেয়ে চওড়া?" প্রশ্নের দ্রুততম সমাধান।
        """,
        tip_en=r"""Show the arithmetic aloud for both boxes, then add the margin-collapse twist — interviewers often hide it in box-model questions to see if you notice.""",
        tip_bn=r"""দুটো box-এর হিসাবই মুখে মুখে দেখাও, তারপর margin collapse-এর মোড়টা যোগ করো — interviewer প্রায়ই box-model প্রশ্নে এটা লুকিয়ে রাখে, তুমি খেয়াল করো কি না দেখতে।""",
        mist_en=r"""Including margin in the width, assuming `border-box` is the default, or answering 20px for the gap.""",
        mist_bn=r"""Width-এর মধ্যে margin ধরা, `border-box`-কে default ভাবা, অথবা ফাঁক 20px বলা।""",
        follow=[
            ("When do vertical margins NOT collapse?", "কখন vertical margin collapse করে না?"),
            ("Why is `box-sizing` often set with `inherit` on `*` and `border-box` on `html`?", "কেন অনেক সময় `html`-এ `border-box` আর `*`-এ `inherit` দিয়ে `box-sizing` set করা হয়?"),
        ],
        related=["css-014"],
        refs=[MDN_BOX_SIZING, WEBDEV_BOX_MODEL],
    ),
    # ------------------------------------------------------------------ css-002
    Q(
        id="css-002", sub="Specificity and Inheritance", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["specificity", "cascade", "selectors"],
        ver="Version-independent (CSS)", vs=False, status="stable",
        q_en=r"""What colour is the text "Hello"?""",
        q_bn=r""""Hello" text-এর রং কী হবে?""",
        code=r"""
            <div id="main" class="content">
              <p class="text">Hello</p>
            </div>

            <style>
              #main p        { color: red; }
              .content .text { color: green; }
              p.text         { color: blue; }
            </style>
        """,
        lang="html",
        options=[
            ("Red", "লাল (red)"),
            ("Green", "সবুজ (green)"),
            ("Blue", "নীল (blue)"),
            ("Green, because it has two classes and appears after `#main p`", "সবুজ, কারণ এতে দুটো class আছে আর এটা `#main p`-এর পরে লেখা"),
        ],
        correct=0,
        a_en=r"""
            **Red.** Specificity is compared as a tuple (IDs, classes/attributes/pseudo-classes, elements/pseudo-elements):
            - `#main p` → (1, 0, 1)
            - `.content .text` → (0, 2, 0)
            - `p.text` → (0, 1, 1)

            The ID column is compared first, so (1, 0, 1) wins.
        """,
        a_bn=r"""
            **লাল (red)।** Specificity একটা tuple হিসেবে তুলনা করা হয় (ID, class/attribute/pseudo-class, element/pseudo-element):
            - `#main p` → (1, 0, 1)
            - `.content .text` → (0, 2, 0)
            - `p.text` → (0, 1, 1)

            ID column আগে তুলনা হয়, তাই (1, 0, 1) জেতে।
        """,
        quick_en=r"""Red. `#main p` has specificity (1, 0, 1), and the ID column is compared first, so it beats `.content .text` (0, 2, 0) and `p.text` (0, 1, 1) regardless of source order.""",
        quick_bn=r"""লাল। `#main p`-এর specificity (1, 0, 1), আর ID-র ঘর সবার আগে তুলনা হয়, তাই source order যাই হোক এটা `.content .text` (0, 2, 0) আর `p.text` (0, 1, 1)-কে হারায়।""",
        ex_en=r"""
            The tempting answer is green: "two classes beat one ID plus one element" sounds reasonable if you add up points. But specificity isn't a single number — columns are compared left to right, and no number of classes ever beats one ID ((0, 11, 0) still loses to (1, 0, 0)).

            Source order only matters when specificity is equal. Above all of this sit inline `style` attributes and `!important` declarations, and — in modern CSS — cascade layers, which are compared *before* specificity.

            Practical takeaway: avoid IDs in selectors for styling. They create specificity "spikes" that force others to escalate with more IDs or `!important`.
        """,
        ex_bn=r"""
            প্রলোভনজনক উত্তর সবুজ: point যোগ করে ভাবলে "দুটো class একটা ID আর একটা element-কে হারায়" যুক্তিসংগত শোনায়। কিন্তু specificity একক কোনো সংখ্যা নয় — column-গুলো বাঁ থেকে ডানে তুলনা হয়, আর যত class-ই থাকুক, একটা ID-কে কখনো হারাতে পারে না ((0, 11, 0) তখনো (1, 0, 0)-এর কাছে হারে)।

            Specificity সমান হলেই কেবল source order গুরুত্বপূর্ণ। এসবের উপরে আছে inline `style` attribute আর `!important` declaration, আর আধুনিক CSS-এ cascade layer, যেগুলো specificity-র *আগেই* তুলনা হয়।

            বাস্তব শিক্ষা: styling-এর selector-এ ID এড়িয়ে চলো। এগুলো specificity-তে হঠাৎ "লাফ" তৈরি করে, ফলে অন্যদের আরও ID বা `!important` দিয়ে পাল্লা দিতে হয়।
        """,
        tip_en=r"""Write the three tuples out loud before answering. Saying "columns, not points" signals you know why the intuitive answer is wrong.""",
        tip_bn=r"""উত্তর দেওয়ার আগে তিনটা tuple মুখে বলো। "Point নয়, column" — এটা বললে বোঝা যায় তুমি জানো সহজাত উত্তরটা কেন ভুল।""",
        refs=[WEBDEV_SPECIFICITY],
    ),
    # ------------------------------------------------------------------ css-003
    Q(
        id="css-003", sub="Specificity and Inheritance", diff="easy", type="output",
        prio="high", market="both", mins=3,
        tags=["inheritance", "specificity", "cascade", "output"],
        ver="Version-independent (CSS)", vs=False, status="stable",
        q_en=r"""What colour and font weight do the paragraph text and the `<span>` end up with?""",
        q_bn=r"""Paragraph-এর text আর `<span>` শেষ পর্যন্ত কোন রং আর কোন font weight পাবে?""",
        code=r"""
            <div id="card">
              <p>Price: <span>৳1,250</span></p>
            </div>

            <style>
              #card { color: red; font-weight: bold; }
              p     { color: blue; }
            </style>
        """,
        lang="html",
        output=r"""
            <p> text  → blue, bold
            <span>    → blue, bold
        """,
        a_en=r"""
            - `<p>` is **blue**: a rule that targets an element directly always beats a value it would inherit — no matter how specific the ancestor's selector is. `#card` has high specificity, but specificity only competes between rules that match the *same* element.
            - `<p>` is **bold**: no rule sets `font-weight` on `<p>`, and `font-weight` is an inherited property, so it inherits from `#card`.
            - `<span>` is **blue and bold**: nothing targets the span, so it inherits both values from its parent `<p>`.
        """,
        a_bn=r"""
            - `<p>` **নীল**: যে rule সরাসরি element-টাকে target করে, সেটা সবসময় inherit হয়ে আসা value-কে হারায় — ancestor-এর selector যত specific-ই হোক। `#card`-এর specificity বেশি, কিন্তু specificity-র প্রতিযোগিতা শুধু *একই* element-কে match করা rule-গুলোর মধ্যে।
            - `<p>` **bold**: কোনো rule `<p>`-এ `font-weight` set করেনি, আর `font-weight` একটা inherited property, তাই এটা `#card` থেকে inherit করে।
            - `<span>` **নীল আর bold**: কোনো rule span-কে target করেনি, তাই দুটো value-ই parent `<p>` থেকে inherit করে।
        """,
        quick_en=r"""The `<p>` is blue and bold, and so is the `<span>`. A rule that targets the `<p>` directly beats any inherited value however specific; `font-weight` is inherited from `#card`, and the span inherits both values from the `<p>`.""",
        quick_bn=r"""`<p>` নীল আর bold, `<span>`-ও নীল আর bold। `<p>`-কে সরাসরি target করা rule যেকোনো inherited value-কে হারায়, ancestor-এর selector যত specific-ই হোক; `font-weight` আসে `#card` থেকে inherit হয়ে, আর span দুটো value-ই `<p>` থেকে পায়।""",
        ex_en=r"""
            - **Inherited vs non-inherited properties:** text-related properties (`color`, `font-*`, `line-height`, `letter-spacing`, `visibility`, `cursor`) inherit by default; box-related ones (`margin`, `padding`, `border`, `background`, `width`) don't.
            - **Keywords to control it:** `inherit` (take the parent's value), `initial` (the property's spec default — e.g. `display: initial` is `inline`, which surprises people), `unset` (inherit if inheritable, else initial) and `revert` (go back to the browser's default style), plus `revert-layer`.
            - **Classic surprise:** form controls don't inherit `font` from the page in most browser default styles — that's why resets include `button, input, select, textarea { font: inherit; }`.
        """,
        ex_bn=r"""
            - **Inherited বনাম non-inherited property:** text-সংক্রান্ত property (`color`, `font-*`, `line-height`, `letter-spacing`, `visibility`, `cursor`) default-ভাবে inherit হয়; box-সংক্রান্তগুলো (`margin`, `padding`, `border`, `background`, `width`) হয় না।
            - **নিয়ন্ত্রণের keyword:** `inherit` (parent-এর value নাও), `initial` (property-র spec অনুযায়ী default — যেমন `display: initial` হলো `inline`, যা অনেককে অবাক করে), `unset` (inheritable হলে inherit, নইলে initial) আর `revert` (browser-এর default style-এ ফিরে যাও), সাথে `revert-layer`।
            - **পরিচিত চমক:** বেশিরভাগ browser-এর default style-এ form control page থেকে `font` inherit করে না — এজন্যই reset-এ থাকে `button, input, select, textarea { font: inherit; }`।
        """,
        tip_en=r"""State the rule in one line — "an inherited value has no specificity; any matching rule beats it" — then apply it to each element.""",
        tip_bn=r"""এক লাইনে নিয়মটা বলো — "inherit হওয়া value-র কোনো specificity নেই; match করা যেকোনো rule তাকে হারায়" — তারপর প্রতিটা element-এ প্রয়োগ করো।""",
        mist_en=r"""Answering red because `#card` "has higher specificity", or assuming `font-weight` stops at the `<p>`.""",
        mist_bn=r"""`#card`-এর "specificity বেশি" বলে লাল বলা, অথবা `font-weight` `<p>`-এ গিয়ে থেমে যায় বলে ধরে নেওয়া।""",
        follow=[
            ("What's the difference between `initial`, `unset` and `revert`?", "`initial`, `unset` আর `revert`-এর পার্থক্য কী?"),
            ("Why don't buttons pick up your page font by default?", "Button কেন default-ভাবে তোমার page-এর font নেয় না?"),
        ],
        related=["css-002", "css-009"],
        refs=[WEBDEV_INHERITANCE, WEBDEV_SPECIFICITY],
    ),
    # ------------------------------------------------------------------ css-012
    Q(
        id="css-012", sub="Cascade and Layers", diff="medium", type="output",
        prio="high", market="both", mins=5,
        tags=["cascade-layers", "layer", "cascade", "specificity", "output"],
        ver="CSS Cascade Level 5; @layer Baseline widely available", vs=False, status="stable",
        q_en=r"""What background colour does each element get?""",
        q_bn=r"""প্রতিটা element কোন background colour পাবে?""",
        code=r"""
            <button class="btn" id="buy">Buy now</button>
            <a class="btn" id="cart" href="/cart">Cart</a>

            <style>
              @layer reset, base, components;

              @layer components {
                .btn { background: green; }
              }

              @layer base {
                #buy.btn, #cart { background: red; }
              }

              button { background: gray; }
            </style>
        """,
        lang="html",
        output=r"""
            #buy  (button) → gray
            #cart (link)   → green
        """,
        a_en=r"""
            In the cascade, **layer order is decided before specificity**.
            - The `@layer reset, base, components;` statement fixes the order: later layers win, so `components` beats `base`.
            - Styles **not in any layer** form an implicit final layer that beats all layered styles (for normal, non-`!important` declarations).

            So `#buy` is **gray**: the unlayered `button` selector, with a tiny specificity of (0, 0, 1), beats both layered rules. `#cart` is **green**: `.btn` in `components` beats the ID selector in `base`, because the layer comparison happens first.
        """,
        a_bn=r"""
            Cascade-এ **specificity-র আগেই layer-এর ক্রম ঠিক হয়**।
            - `@layer reset, base, components;` statement ক্রমটা ঠিক করে দেয়: পরের layer জেতে, তাই `components` `base`-কে হারায়।
            - **কোনো layer-এ নেই** এমন style একটা অদৃশ্য শেষ layer তৈরি করে, যেটা সব layered style-কে হারায় (normal, অর্থাৎ `!important` নয় এমন declaration-এর ক্ষেত্রে)।

            তাই `#buy` **ধূসর (gray)**: unlayered `button` selector, যার specificity মাত্র (0, 0, 1), দুটো layered rule-কেই হারায়। `#cart` **সবুজ (green)**: `components`-এর `.btn` `base`-এর ID selector-কে হারায়, কারণ layer-এর তুলনা আগে হয়।
        """,
        quick_en=r"""`#buy` is gray and `#cart` is green. Layer order is checked before specificity: unlayered styles beat every layer, and the later `components` layer beats `base` even against an ID selector.""",
        quick_bn=r"""`#buy` ধূসর আর `#cart` সবুজ। Specificity-র আগে layer order দেখা হয়: layer-এর বাইরের style সব layer-কে হারায়, আর পরের `components` layer ID selector থাকা সত্ত্বেও `base`-কে হারায়।""",
        ex_en=r"""
            Step by step for `#cart`: candidates are `base` → red (specificity 1,0,0) and `components` → green (0,1,0). Different layers, so specificity is never compared — the later layer wins.

            **`!important` reverses layer order:** an `!important` declaration in an *earlier* layer beats `!important` in later layers, and layered `!important` beats unlayered `!important`. This lets a `reset` layer protect a few critical rules.

            **Why it's useful:**
            - Put third-party CSS in a low layer — `@import url("vendor.css") layer(vendor);` — and your component styles override it without specificity hacks.
            - Layer order is declared once at the top, so file load order stops mattering.
            - Gotcha during migration: unlayered legacy CSS beats everything you put in layers. Wrap legacy code in its own layer too.
        """,
        ex_bn=r"""
            `#cart`-এর জন্য ধাপে ধাপে: প্রার্থী দুটো — `base` → লাল (specificity 1,0,0) আর `components` → সবুজ (0,1,0)। দুটো আলাদা layer-এ, তাই specificity তুলনাই হয় না — পরের layer জেতে।

            **`!important` layer-এর ক্রম উল্টে দেয়:** *আগের* layer-এর `!important` declaration পরের layer-এর `!important`-কে হারায়, আর layered `!important` unlayered `!important`-কে হারায়। এতে একটা `reset` layer কয়েকটা গুরুত্বপূর্ণ rule রক্ষা করতে পারে।

            **কেন কাজের:**
            - Third-party CSS নিচের দিকের একটা layer-এ রাখো — `@import url("vendor.css") layer(vendor);` — তাহলে specificity hack ছাড়াই তোমার component style সেটাকে override করবে।
            - Layer-এর ক্রম শুরুতে একবারই ঘোষণা করা হয়, তাই file কোন ক্রমে load হলো তা আর গুরুত্বপূর্ণ থাকে না।
            - Migration-এর সময়ের ফাঁদ: unlayered legacy CSS layer-এ রাখা সবকিছুকে হারায়। তাই legacy code-কেও নিজস্ব একটা layer-এ wrap করো।
        """,
        tip_en=r"""Say the cascade order explicitly — origin/importance → layers → specificity → source order — then apply it. Mentioning that unlayered styles win shows you've actually migrated code to layers.""",
        tip_bn=r"""Cascade-এর ক্রম স্পষ্ট করে বলো — origin/importance → layer → specificity → source order — তারপর প্রয়োগ করো। Unlayered style যে জেতে, এটা বললে বোঝা যায় তুমি সত্যিই code layer-এ migrate করেছ।""",
        mist_en=r"""Assuming the ID selector wins because of specificity, assuming unlayered styles have the *lowest* priority, or forgetting that `!important` flips layer order.""",
        mist_bn=r"""Specificity-র কারণে ID selector জিতবে ধরে নেওয়া, unlayered style-এর priority *সবচেয়ে কম* ভাবা, অথবা ভুলে যাওয়া যে `!important` layer-এর ক্রম উল্টে দেয়।""",
        follow=[
            ("What happens if a rule in the `reset` layer uses `!important`?", "`reset` layer-এর কোনো rule-এ `!important` থাকলে কী হবে?"),
            ("How would you bring Bootstrap into a layer?", "Bootstrap-কে কীভাবে একটা layer-এ আনবে?"),
        ],
        related=["css-002", "css-030"],
        refs=[MDN_LAYER, WEBDEV_CASCADE],
    ),
    # ------------------------------------------------------------------ css-013
    Q(
        id="css-013", sub="Pseudo-classes and Pseudo-elements", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["has", "parent-selector", "selectors", "performance"],
        ver="CSS Selectors Level 4; :has() Baseline widely available (since Dec 2023)", vs=True, status="stable",
        q_en=r"""What does `:has()` let you do that CSS couldn't do before? Give practical examples, and explain its limits and performance considerations.""",
        q_bn=r"""`:has()` দিয়ে এমন কী করা যায় যা আগে CSS-এ করা যেত না? বাস্তব উদাহরণ দাও, আর এর সীমাবদ্ধতা ও performance-এর দিকগুলো ব্যাখ্যা করো।""",
        a_en=r"""
            `:has()` is the long-awaited **"parent" (relational) selector**: it matches an element based on what's inside it or after it. `.card:has(img)` selects cards that *contain* an image — previously you needed JavaScript to add a class.

            Practical uses:
            - **Form state:** highlight a whole field group when its input is invalid — `.field:has(input:user-invalid)`.
            - **Layout by content:** a card switches to a two-column layout only if it has an image — `.card:has(> img)`.
            - **Quantity queries:** compact rows when a list has five or more items — `.cart-items:has(> li:nth-child(5))`.
            - **Sibling-aware styling:** `h2:has(+ p)` styles a heading only when a paragraph follows it.

            Limits: `:has()` can't be nested inside another `:has()`, pseudo-elements aren't allowed inside it, and its specificity is that of its most specific argument (like `:is()`). It's Baseline widely available, so it's safe to use; for very old browsers, design it as an enhancement.
        """,
        a_bn=r"""
            `:has()` হলো বহু প্রতীক্ষিত **"parent" (relational) selector**: কোনো element-এর ভেতরে বা পরে কী আছে তার ভিত্তিতে সেটাকে match করে। `.card:has(img)` সেই card-গুলো select করে যাদের ভেতরে image *আছে* — আগে এর জন্য JavaScript দিয়ে class যোগ করতে হতো।

            বাস্তব ব্যবহার:
            - **Form state:** input invalid হলে পুরো field group highlight করা — `.field:has(input:user-invalid)`।
            - **Content অনুযায়ী layout:** card-এ image থাকলেই কেবল দুই-column layout — `.card:has(> img)`।
            - **Quantity query:** list-এ পাঁচ বা তার বেশি item থাকলে compact row — `.cart-items:has(> li:nth-child(5))`।
            - **Sibling দেখে styling:** `h2:has(+ p)` heading-কে শুধু তখনই style করে, যখন তার পরে একটা paragraph থাকে।

            সীমাবদ্ধতা: `:has()`-এর ভেতরে আরেকটা `:has()` nest করা যায় না, এর ভেতরে pseudo-element চলে না, আর এর specificity হয় এর সবচেয়ে specific argument-এর সমান (`:is()`-এর মতো)। এটা Baseline widely available, তাই নিরাপদে ব্যবহার করা যায়; খুব পুরোনো browser-এর জন্য এটাকে enhancement হিসেবে design করো।
        """,
        quick_en=r"""`:has()` is a relational "parent" selector: it matches an element by what it contains or what follows it, like `.card:has(img)`, which used to need JavaScript. It can't be nested inside another `:has()` or contain pseudo-elements, and it's Baseline widely available.""",
        quick_bn=r"""`:has()` একটা relational "parent" selector: ভেতরে কী আছে বা পরে কী আছে দেখে element match করে, যেমন `.card:has(img)`, যেটা আগে JavaScript ছাড়া হতো না। একটা `:has()`-এর ভেতরে আরেকটা বা pseudo-element রাখা যায় না, আর এটা Baseline widely available।""",
        ex_en=r"""
            **Performance:** `:has()` makes the browser re-check the subject element when its descendants change. Keep it cheap:
            - Anchor it to a specific, small container (`.filters:has(...)`), not `body`, `:root` or `*` — on a big page every DOM change below the anchor can trigger re-evaluation.
            - Constrain the inner selector with `>` or `+` instead of open-ended descendant matching.
            - Patterns like `body:has(dialog[open])` for scroll locking are common and fine in moderation, but don't build your whole state system on body-level `:has()`.

            **Robustness:** unlike `:is()`/`:where()`, an unsupported or invalid selector inside `:has()` invalidates the whole rule, so test new pseudo-classes carefully. Feature-detect with `@supports selector(:has(a))` if you need a fallback.

            **Combined with `:user-invalid`**, `:has()` gives you "show errors only after interaction" styling with zero JavaScript.
        """,
        ex_bn=r"""
            **Performance:** descendant বদলালে `:has()`-এর কারণে browser-কে subject element আবার check করতে হয়। খরচ কম রাখতে:
            - একে নির্দিষ্ট, ছোট container-এ anchor করো (`.filters:has(...)`), `body`, `:root` বা `*`-এ নয় — বড় page-এ anchor-এর নিচের প্রতিটা DOM পরিবর্তন re-evaluation ঘটাতে পারে।
            - ভেতরের selector খোলা descendant matching না করে `>` বা `+` দিয়ে সীমিত করো।
            - Scroll lock-এর জন্য `body:has(dialog[open])`-এর মতো pattern প্রচলিত এবং পরিমিতভাবে ঠিক আছে, কিন্তু পুরো state system body-level `:has()`-এর উপর দাঁড় করিও না।

            **নির্ভরযোগ্যতা:** `:is()`/`:where()`-এর মতো নয় — `:has()`-এর ভেতরে unsupported বা invalid selector থাকলে পুরো rule-টাই invalid হয়ে যায়, তাই নতুন pseudo-class সাবধানে test করো। Fallback লাগলে `@supports selector(:has(a))` দিয়ে feature detect করো।

            **`:user-invalid`-এর সাথে মিলিয়ে** `:has()` দিয়ে কোনো JavaScript ছাড়াই "interaction-এর পরেই শুধু error দেখাও" ধরনের styling করা যায়।
        """,
        tip_en=r"""Give one example that used to require JavaScript (form group error state) — that's the "why it matters". Then show you know the performance guidance about broad anchors; few candidates mention it.""",
        tip_bn=r"""এমন একটা উদাহরণ দাও যেটার জন্য আগে JavaScript লাগত (form group-এর error state) — এটাই "কেন গুরুত্বপূর্ণ"। তারপর দেখাও যে তুমি broad anchor নিয়ে performance-এর নির্দেশনা জানো; খুব কম candidate এটা বলে।""",
        mist_en=r"""Calling it "only a parent selector" (it also handles siblings), using `body:has(...)` for everything, or assuming `:has()` adds zero specificity like `:where()`.""",
        mist_bn=r"""একে "শুধু parent selector" বলা (এটা sibling-ও সামলায়), সবকিছুর জন্য `body:has(...)` ব্যবহার করা, অথবা ধরে নেওয়া যে `:where()`-এর মতো `:has()`-ও কোনো specificity যোগ করে না।""",
        code=r"""
            /* Error state on the whole field after the user interacts */
            .field:has(input:user-invalid) {
              border-inline-start: 4px solid #b00020;
            }
            .field:has(input:user-invalid) .hint { color: #b00020; }

            /* Two-column card only when it has a direct image child */
            .card:has(> img) {
              display: grid;
              grid-template-columns: 7.5rem 1fr;
              gap: 0.75rem;
            }

            /* Quantity query: tighter rows when the cart has 5+ items */
            .cart-items:has(> li:nth-child(5)) { --row-padding: 0.25rem; }

            /* Fallback-aware enhancement */
            @supports not selector(:has(a)) {
              .field.is-invalid { border-inline-start: 4px solid #b00020; }
            }
        """,
        lang="css",
        follow=[
            ("How is `:has()` specificity calculated for `.card:has(#promo, .badge)`?", "`.card:has(#promo, .badge)`-এর specificity কীভাবে হিসাব হয়?"),
            ("What's the difference between `:invalid` and `:user-invalid`?", "`:invalid` আর `:user-invalid`-এর পার্থক্য কী?"),
        ],
        related=["css-023", "css-031"],
        refs=[MDN_HAS],
    ),
    # ------------------------------------------------------------------ css-014
    Q(
        id="css-014", sub="Flexbox", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["flexbox", "min-width", "overflow", "text-overflow", "debugging"],
        ver="Version-independent (CSS Flexbox)", vs=False, status="stable",
        q_en=r"""On a 360px-wide phone, this contact row overflows horizontally: the long name doesn't get an ellipsis, the "Call" button is pushed off-screen, and the page scrolls sideways. Why, and how do you fix it?""",
        q_bn=r"""360px চওড়া phone-এ এই contact row horizontally overflow করছে: লম্বা নামে ellipsis আসছে না, "Call" button screen-এর বাইরে চলে যাচ্ছে, আর page পাশে scroll হচ্ছে। কেন, আর কীভাবে ঠিক করবে?""",
        code=r"""
            <div class="row">
              <img class="avatar" src="/u/42.jpg" width="48" height="48" alt="">
              <div class="body">
                <p class="name">Mohammad Abdullah Al Mamun — Senior Procurement Officer, Chattogram</p>
                <code class="tracking">DK-TRACK-2026-000000000000000000000042</code>
              </div>
              <button type="button">Call</button>
            </div>

            <style>
              .row  { display: flex; gap: 12px; align-items: center; }
              .body { flex: 1; }
              .name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            </style>
        """,
        lang="html",
        a_en=r"""
            **Root cause:** flex items have `min-width: auto` by default, which means they can't shrink below their **min-content width**. `.body` contains a `nowrap` line and a long unbreakable tracking code, so its min-content width is huge. `flex: 1` asks it to shrink, but `min-width: auto` forbids it — the row overflows, and the ellipsis never triggers because `.name` is never narrower than its text.

            **Fix:**
            - `min-width: 0` on `.body` lets it shrink below its content size, so `overflow: hidden` + `text-overflow: ellipsis` on `.name` can finally kick in.
            - `overflow-wrap: anywhere` on the tracking code lets the long string wrap (and, unlike `break-word`, it also reduces the min-content size).
            - `flex-shrink: 0` on the avatar and button makes it explicit that those keep their size.
        """,
        a_bn=r"""
            **মূল কারণ:** flex item-এর default `min-width: auto`, অর্থাৎ এগুলো নিজের **min-content width**-এর চেয়ে ছোট হতে পারে না। `.body`-র ভেতরে একটা `nowrap` line আর ভাঙা যায় না এমন লম্বা tracking code আছে, তাই এর min-content width বিশাল। `flex: 1` একে ছোট হতে বলে, কিন্তু `min-width: auto` তা হতে দেয় না — row overflow করে, আর ellipsis কখনো কাজ করে না কারণ `.name` কখনো তার text-এর চেয়ে সরু হয় না।

            **সমাধান:**
            - `.body`-তে `min-width: 0` দিলে এটা content size-এর চেয়েও ছোট হতে পারে, তখন `.name`-এর `overflow: hidden` + `text-overflow: ellipsis` অবশেষে কাজ করে।
            - Tracking code-এ `overflow-wrap: anywhere` দিলে লম্বা string wrap হতে পারে (আর `break-word`-এর মতো নয়, এটা min-content size-ও কমায়)।
            - Avatar আর button-এ `flex-shrink: 0` দিলে স্পষ্ট হয় যে এগুলো নিজেদের মাপ বজায় রাখবে।
        """,
        quick_en=r"""Flex items default to `min-width: auto`, so `.body` can't shrink below its long content and the row overflows. Add `min-width: 0` to `.body` so the ellipsis works, `overflow-wrap: anywhere` to the tracking code, and `flex-shrink: 0` to the avatar and button.""",
        quick_bn=r"""Flex item-এর default `min-width: auto`, তাই `.body` তার লম্বা content-এর চেয়ে ছোট হতে পারে না, ফলে row overflow করে। `.body`-তে `min-width: 0` দাও যাতে ellipsis কাজ করে, tracking code-এ `overflow-wrap: anywhere`, আর avatar ও button-এ `flex-shrink: 0`।""",
        ex_en=r"""
            - **Why `min-width: auto` exists:** it protects content from being crushed by default. The downside shows up with long words, URLs, `<pre>`/`<code>`, tables or nested flex containers.
            - **Same bug in Grid:** `1fr` means `minmax(auto, 1fr)`, so a grid column with a long `<pre>` refuses to shrink. Use `minmax(0, 1fr)`.
            - **Nested flex:** if `.body` is itself a flex container, its children may need `min-width: 0` too — the constraint applies at each level.
            - **Debugging tip:** in DevTools, hover the flex item and check its computed `min-width`; Chrome's flexbox overlay also shows how much each item shrank or grew.
            - `overflow: hidden` on the item also resets the automatic minimum (because it's a scroll container), but `min-width: 0` is the clearer intent.
        """,
        ex_bn=r"""
            - **`min-width: auto` কেন আছে:** default-ভাবে content যেন চেপে না যায়, সেজন্য। এর অসুবিধা দেখা দেয় লম্বা শব্দ, URL, `<pre>`/`<code>`, table বা nested flex container থাকলে।
            - **Grid-এ একই bug:** `1fr` মানে `minmax(auto, 1fr)`, তাই লম্বা `<pre>` থাকা grid column ছোট হতে চায় না। `minmax(0, 1fr)` ব্যবহার করো।
            - **Nested flex:** `.body` নিজেও যদি flex container হয়, তাহলে তার children-এরও `min-width: 0` লাগতে পারে — এই সীমাবদ্ধতা প্রতিটা স্তরে প্রযোজ্য।
            - **Debugging tip:** DevTools-এ flex item-এর উপর hover করে তার computed `min-width` দেখো; Chrome-এর flexbox overlay প্রতিটা item কতটা ছোট বা বড় হলো তাও দেখায়।
            - Item-এ `overflow: hidden` দিলেও automatic minimum reset হয় (কারণ এটা তখন scroll container), তবে `min-width: 0` উদ্দেশ্যটা বেশি স্পষ্ট করে।
        """,
        tip_en=r"""Name the property (`min-width: auto`) and the concept (min-content size) in your first sentence. That's the insight; the fix is one line once you've said it.""",
        tip_bn=r"""প্রথম বাক্যেই property (`min-width: auto`) আর ধারণাটার (min-content size) নাম বলো। মূল অন্তর্দৃষ্টি এটাই; এটা বলার পর সমাধান মাত্র এক লাইন।""",
        mist_en=r"""Adding `overflow: hidden` to `body`, setting a fixed `width` on `.body`, or putting `text-overflow` on the flex item instead of the element whose text overflows.""",
        mist_bn=r"""`body`-তে `overflow: hidden` দেওয়া, `.body`-তে নির্দিষ্ট `width` দেওয়া, অথবা যে element-এর text overflow করছে তাতে না দিয়ে flex item-এ `text-overflow` দেওয়া।""",
        extra=[dict(
            lang="css",
            src=r"""
                .row  { display: flex; gap: 12px; align-items: center; }
                .avatar, .row > button { flex-shrink: 0; }
                .body { flex: 1; min-width: 0; }   /* allow shrinking below min-content */
                .name { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
                .tracking { overflow-wrap: anywhere; }
            """,
            label_en="Fixed CSS",
            label_bn="সংশোধিত CSS",
        )],
        follow=[
            ("Why does `1fr` in a grid sometimes overflow, and what's the fix?", "Grid-এ `1fr` কেন মাঝে মাঝে overflow করে, আর সমাধান কী?"),
            ("What's the difference between `overflow-wrap: break-word` and `anywhere`?", "`overflow-wrap: break-word` আর `anywhere`-এর পার্থক্য কী?"),
        ],
        related=["css-005", "css-027"],
        refs=[MDN_MIN_WIDTH, MDN_OVERFLOW_WRAP, WEBDEV_FLEXBOX],
    ),
    # ------------------------------------------------------------------ css-023
    Q(
        id="css-023", sub="Specificity and Inheritance", diff="hard", type="mcq",
        prio="medium", market="both", mins=4,
        tags=["specificity", "is", "where", "not", "selectors"],
        ver="CSS Selectors Level 4; :is()/:where()/:not() lists Baseline widely available", vs=False, status="stable",
        q_en=r"""What colour is the "Home" link?""",
        q_bn=r""""Home" link-এর রং কী হবে?""",
        code=r"""
            <nav id="site-nav" class="nav">
              <a class="link active" href="/">Home</a>
            </nav>

            <style>
              :where(#site-nav) .link.active  { color: red; }
              .nav a:not(#x)                  { color: green; }
              :is(.nav, #site-nav) .link      { color: blue; }
              nav > a.link.active             { color: orange; }
            </style>
        """,
        lang="html",
        options=[
            ("Red", "লাল (red)"),
            ("Green", "সবুজ (green)"),
            ("Blue", "নীল (blue)"),
            ("Orange", "কমলা (orange)"),
        ],
        correct=1,
        a_en=r"""
            **Green.** Specificities:
            - `:where(#site-nav) .link.active` → `:where()` always counts as **zero** → (0, 2, 0)
            - `.nav a:not(#x)` → `:not()` takes its most specific argument, `#x` → (1, 1, 1)
            - `:is(.nav, #site-nav) .link` → `:is()` takes its most specific argument, `#site-nav` → (1, 1, 0)
            - `nav > a.link.active` → (0, 2, 2)

            (1, 1, 1) is the highest.
        """,
        a_bn=r"""
            **সবুজ (green)।** Specificity-গুলো:
            - `:where(#site-nav) .link.active` → `:where()` সবসময় **শূন্য** গণ্য হয় → (0, 2, 0)
            - `.nav a:not(#x)` → `:not()` তার সবচেয়ে specific argument নেয়, `#x` → (1, 1, 1)
            - `:is(.nav, #site-nav) .link` → `:is()` তার সবচেয়ে specific argument নেয়, `#site-nav` → (1, 1, 0)
            - `nav > a.link.active` → (0, 2, 2)

            (1, 1, 1) সবচেয়ে বেশি।
        """,
        quick_en=r"""Green. `.nav a:not(#x)` scores (1, 1, 1) because `:not()` takes its most specific argument, beating `:is(.nav, #site-nav) .link` at (1, 1, 0); `:where()` always counts as zero.""",
        quick_bn=r"""সবুজ। `.nav a:not(#x)`-এর specificity (1, 1, 1), কারণ `:not()` তার সবচেয়ে specific argument ধরে, তাই এটা (1, 1, 0)-এর `:is(.nav, #site-nav) .link`-কে হারায়; `:where()` সবসময় শূন্য।""",
        ex_en=r"""
            The tempting answer is **blue**, for one of two reasons: people either think `:is()` only counts the argument that actually matched (it doesn't — it always uses the most specific argument in the list), or they forget that `:not(#x)` contributes a full ID even though the element doesn't have that ID. Both rules give green the edge: (1, 1, 1) beats (1, 1, 0) in the last column.

            Practical uses of these rules:
            - **`:where()`** is perfect for resets and library defaults that should be trivially overridable — zero specificity no matter what's inside.
            - **`:is()`** shortens long selector lists, but one ID inside it raises the whole selector's specificity — a hidden source of "why can't I override this?".
            - **`:not(#something)`** is an old hack to bump specificity; prefer cascade layers to control priority instead.
            - Native nesting's `&` behaves like `:is()` for specificity, so the same rule applies to nested selectors.
        """,
        ex_bn=r"""
            প্রলোভনজনক উত্তর **নীল**, দুটো কারণের একটায়: অনেকে ভাবে `:is()` শুধু আসলে match করা argument-টা গোনে (তা নয় — এটা সবসময় list-এর সবচেয়ে specific argument ব্যবহার করে), অথবা ভুলে যায় যে element-এর ওই ID না থাকলেও `:not(#x)` একটা পূর্ণ ID যোগ করে। এই দুই নিয়মে সবুজ এগিয়ে থাকে: শেষ column-এ (1, 1, 1) (1, 1, 0)-কে হারায়।

            এই নিয়মগুলোর বাস্তব ব্যবহার:
            - **`:where()`** reset আর library-র default-এর জন্য চমৎকার, যেগুলো সহজেই override করা যাওয়া উচিত — ভেতরে যাই থাকুক, specificity শূন্য।
            - **`:is()`** লম্বা selector list ছোট করে, কিন্তু এর ভেতরে একটা ID থাকলে পুরো selector-এর specificity বেড়ে যায় — "এটা override করতে পারছি না কেন?" সমস্যার একটা লুকানো উৎস।
            - **`:not(#something)`** specificity বাড়ানোর একটা পুরোনো hack; priority নিয়ন্ত্রণের জন্য এর বদলে cascade layer ব্যবহার করো।
            - Native nesting-এর `&` specificity-র ক্ষেত্রে `:is()`-এর মতো আচরণ করে, তাই nested selector-এও একই নিয়ম খাটে।
        """,
        tip_en=r"""Compute all four tuples before picking. Then add one sentence on *when you'd use* `:where()` deliberately — that moves the answer from arithmetic to design.""",
        tip_bn=r"""উত্তর বাছার আগে চারটা tuple-ই হিসাব করো। তারপর এক বাক্যে বলো তুমি কখন ইচ্ছা করে `:where()` ব্যবহার করবে — এতে উত্তরটা শুধু অঙ্ক থেকে design-এর আলোচনায় পৌঁছায়।""",
        refs=[MDN_IS, MDN_WHERE, WEBDEV_SPECIFICITY],
    ),
    # ------------------------------------------------------------------ css-030
    Q(
        id="css-030", sub="CSS Architecture", diff="extreme", type="architecture",
        prio="medium", market="international", mins=20,
        tags=["css-architecture", "cascade-layers", "design-tokens", "scope", "migration"],
        ver="CSS Cascade 5/6; @layer widely available; @scope Baseline newly available (Mar 2026); light-dark() newly available", vs=True, status="stable",
        q_en=r"""You join a five-year-old e-commerce codebase with about 40,000 lines of CSS: Bootstrap overrides, page-specific files from three teams, `!important` everywhere, and nobody dares delete anything. Design a CSS architecture that brings it under control without a full rewrite, and that supports a new design system with dark mode.""",
        q_bn=r"""তুমি একটা পাঁচ বছরের পুরোনো e-commerce codebase-এ যোগ দিয়েছ, যেখানে প্রায় 40,000 লাইন CSS: Bootstrap override, তিনটা team-এর page-ভিত্তিক file, সব জায়গায় `!important`, আর কেউ কিছু delete করার সাহস পায় না। পুরোটা rewrite না করে এটাকে নিয়ন্ত্রণে আনার মতো একটা CSS architecture design করো, যেটা dark mode-সহ নতুন একটা design system-ও support করবে।""",
        a_en=r"""
            This is advanced material; the goal is a **predictable cascade** and **safe, incremental change**.

            **1. Cascade layers as the backbone.** Declare the order once: `@layer reset, vendor, legacy, tokens, base, components, utilities;`. Import Bootstrap with `layer(vendor)` and wrap all existing CSS in `legacy`. New component code in later layers now wins *without* specificity battles.
            - Gotcha 1: unlayered CSS beats every layer, so legacy code **must** go into a layer, or it will override the new system.
            - Gotcha 2: `!important` reverses layer order — a legacy `!important` beats even an `!important` in `components`. Inventory and remove legacy `!important` early; lint against new ones.

            **2. Design tokens as custom properties.** Primitive tokens (`--green-600`) → semantic tokens (`--color-action-bg`, `--color-surface`) → used by components. Dark mode switches semantic tokens only: `color-scheme: light dark` plus `light-dark()` or a `[data-theme="dark"]` override. Components never hard-code colours.

            **3. Component boundaries.** One convention for new code: CSS Modules (build-time scoping) or `@scope` (Baseline newly available since March 2026, so with a fallback plan). Keep selector specificity flat — single classes, `:where()` for defaults — and use container queries so components adapt to their slot.

            **4. Migrate with a strangler pattern.** Rebuild one component or page at a time in the new layers; delete the matching legacy rules once screenshots match. Use the DevTools **Coverage** panel and visual regression tests to delete dead CSS safely.

            **5. Guardrails.** Stylelint rules (no IDs, no new `!important`, max specificity, token-only colours), code ownership per team, and a CSS size budget in CI.
        """,
        a_bn=r"""
            এটা advanced বিষয়; লক্ষ্য হলো একটা **অনুমানযোগ্য cascade** আর **নিরাপদ, ধাপে ধাপে পরিবর্তন**।

            **1. মেরুদণ্ড হিসেবে cascade layer।** শুরুতে একবারই ক্রম ঘোষণা করো: `@layer reset, vendor, legacy, tokens, base, components, utilities;`। Bootstrap `layer(vendor)` দিয়ে import করো আর বিদ্যমান সব CSS `legacy`-তে wrap করো। এখন পরের layer-এর নতুন component code specificity-র লড়াই *ছাড়াই* জেতে।
            - ফাঁদ 1: unlayered CSS সব layer-কে হারায়, তাই legacy code-কে **অবশ্যই** একটা layer-এ রাখতে হবে, নইলে সেটা নতুন system-কে override করবে।
            - ফাঁদ 2: `!important` layer-এর ক্রম উল্টে দেয় — legacy-র একটা `!important` এমনকি `components`-এর `!important`-কেও হারায়। শুরুতেই legacy `!important`-এর তালিকা করে সরাও; নতুনগুলো lint দিয়ে আটকাও।

            **2. Custom property হিসেবে design token।** Primitive token (`--green-600`) → semantic token (`--color-action-bg`, `--color-surface`) → component সেগুলো ব্যবহার করে। Dark mode শুধু semantic token বদলায়: `color-scheme: light dark` সাথে `light-dark()`, অথবা `[data-theme="dark"]` override। Component কখনো রং hard-code করে না।

            **3. Component-এর সীমানা।** নতুন code-এর জন্য একটাই নিয়ম: CSS Modules (build-time scoping) অথবা `@scope` (March 2026 থেকে Baseline newly available, তাই fallback পরিকল্পনাসহ)। Selector specificity সমতল রাখো — single class, default-এর জন্য `:where()` — আর container query ব্যবহার করো যাতে component তার জায়গা অনুযায়ী মানিয়ে নেয়।

            **4. Strangler pattern-এ migrate করো।** একবারে একটা component বা page নতুন layer-এ বানাও; screenshot মিলে গেলে সংশ্লিষ্ট legacy rule delete করো। নিরাপদে dead CSS মুছতে DevTools-এর **Coverage** panel আর visual regression test ব্যবহার করো।

            **5. পাহারাদার নিয়ম।** Stylelint rule (ID নয়, নতুন `!important` নয়, সর্বোচ্চ specificity সীমা, শুধু token দিয়ে রং), team অনুযায়ী code ownership, আর CI-তে CSS size budget।
        """,
        quick_en=r"""This is advanced: declare cascade layers and move Bootstrap into `vendor` and all old CSS into `legacy`, so new code wins without specificity fights. Add semantic token custom properties for dark mode, scoped components, a page-by-page migration and Stylelint guardrails against new `!important`.""",
        quick_bn=r"""এটা advanced বিষয়: cascade layer declare করে Bootstrap-কে `vendor` আর সব পুরোনো CSS-কে `legacy` layer-এ রাখি, যাতে নতুন code specificity-র লড়াই ছাড়াই জেতে। সাথে dark mode-এর জন্য semantic token custom property, scoped component, page ধরে ধরে migration, আর নতুন `!important` আটকাতে Stylelint।""",
        ex_en=r"""
            **Trade-offs:**
            - Layers vs CSS Modules/`@scope` solve different problems: layers control *priority*, scoping controls *reach*. Large codebases usually want both.
            - Wrapping legacy CSS in a layer can change today's rendering where legacy rules used to win over unlayered third-party CSS — do it behind visual regression tests.
            - Utility-first frameworks (e.g. Tailwind) reduce cascade problems but move complexity into markup; mixing paradigms without layers recreates the specificity war.

            **Failure scenarios:** a team ships a new unlayered stylesheet and silently overrides the design system (lint for unlayered CSS); token renames break pages (keep aliases for one release); dark mode misses third-party widgets (audit with `color-scheme`).

            **Performance:** split CSS by route, inline critical CSS for landing pages, and remove dead CSS — on slow mobile connections, 40k lines is also a loading problem, not just a maintenance one.
        """,
        ex_bn=r"""
            **Trade-off:**
            - Layer আর CSS Modules/`@scope` আলাদা সমস্যার সমাধান করে: layer নিয়ন্ত্রণ করে *priority*, scoping নিয়ন্ত্রণ করে *নাগাল (reach)*। বড় codebase-এ সাধারণত দুটোই দরকার।
            - Legacy CSS layer-এ wrap করলে বর্তমান rendering বদলে যেতে পারে, যেখানে আগে legacy rule unlayered third-party CSS-কে হারাত — তাই এটা visual regression test-এর পাহারায় করো।
            - Utility-first framework (যেমন Tailwind) cascade-এর সমস্যা কমায়, কিন্তু জটিলতা markup-এ সরিয়ে দেয়; layer ছাড়া বিভিন্ন পদ্ধতি মেশালে আবার সেই specificity-র যুদ্ধ ফিরে আসে।

            **ব্যর্থতার পরিস্থিতি:** কোনো team নতুন unlayered stylesheet ship করে চুপচাপ design system override করে ফেলে (unlayered CSS-এর জন্য lint করো); token-এর নাম বদলালে page ভেঙে যায় (এক release-এর জন্য alias রাখো); dark mode-এ third-party widget বাদ পড়ে যায় (`color-scheme` দিয়ে audit করো)।

            **Performance:** route অনুযায়ী CSS ভাগ করো, landing page-এর জন্য critical CSS inline করো, আর dead CSS মুছে ফেলো — ধীর mobile connection-এ 40k লাইন শুধু maintenance নয়, loading-এরও সমস্যা।
        """,
        tip_en=r"""Lead with the two layer gotchas (unlayered wins; `!important` reverses) — they prove hands-on experience. Then talk about migration and guardrails; interviewers care more about how you change a live system safely than about the ideal end state.""",
        tip_bn=r"""Layer-এর দুটো ফাঁদ দিয়ে শুরু করো (unlayered জেতে; `!important` ক্রম উল্টায়) — এতে হাতে-কলমে অভিজ্ঞতা প্রমাণ হয়। তারপর migration আর guardrail নিয়ে বলো; আদর্শ শেষ অবস্থার চেয়ে চালু system নিরাপদে কীভাবে বদলাবে, interviewer সেটাই বেশি জানতে চায়।""",
        mist_en=r"""Proposing a big-bang rewrite, adding layers but leaving legacy CSS unlayered, ignoring legacy `!important`, or hard-coding dark-mode colours per component.""",
        mist_bn=r"""একবারে সব rewrite করার প্রস্তাব দেওয়া, layer যোগ করে legacy CSS unlayered রেখে দেওয়া, legacy `!important` উপেক্ষা করা, অথবা প্রতিটা component-এ আলাদা করে dark-mode-এর রং hard-code করা।""",
        code=r"""
            /* main.css — the only file that defines layer order */
            @layer reset, vendor, legacy, tokens, base, components, utilities;

            @import url("reset.css") layer(reset);
            @import url("bootstrap.min.css") layer(vendor);
            @import url("legacy/all.css") layer(legacy);

            @layer tokens {
              :root {
                color-scheme: light dark;
                --green-600: #0b6e4f;
                --color-action-bg: var(--green-600);
                --color-on-action: #ffffff;
                --color-surface: light-dark(#ffffff, #121212);
                --color-text: light-dark(#1a1a1a, #f1f1f1);
              }
              [data-theme="dark"] { color-scheme: dark; }
            }

            @layer components {
              .button {
                background: var(--color-action-bg);
                color: var(--color-on-action);
              }
              .card {
                background: var(--color-surface);
                color: var(--color-text);
              }
            }

            @layer utilities {
              .visually-hidden { /* ... */ }
            }
        """,
        lang="css",
        follow=[
            ("How would you stop a team from shipping a new unlayered stylesheet?", "কোনো team যাতে নতুন unlayered stylesheet ship না করে, তা কীভাবে ঠেকাবে?"),
            ("Layers or CSS Modules — which would you introduce first, and why?", "Layer নাকি CSS Modules — কোনটা আগে চালু করবে, আর কেন?"),
            ("How do you measure progress on a CSS cleanup?", "CSS cleanup-এর অগ্রগতি কীভাবে মাপবে?"),
        ],
        related=["css-012", "css-028"],
        refs=[MDN_LAYER, MDN_SCOPE, MDN_LIGHT_DARK],
    ),
]

if __name__ == "__main__":
    save("css", "b1", QUESTIONS)
