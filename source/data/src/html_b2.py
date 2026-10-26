import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_IMG = ("MDN — <img>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img")
WAI_IMAGES = ("W3C WAI — Images tutorial", "https://www.w3.org/WAI/tutorials/images/")
MDN_LABEL = ("MDN — <label>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/label")
MDN_FIELDSET = ("MDN — <fieldset>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/fieldset")
MDN_DATASET = ("MDN — HTMLElement.dataset", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/dataset")
MDN_POPOVER = ("MDN — Popover API", "https://developer.mozilla.org/en-US/docs/Web/API/Popover_API")
MDN_INVOKERS = ("MDN — Invoker Commands API", "https://developer.mozilla.org/en-US/docs/Web/API/Invoker_Commands_API")
MDN_DETAILS = ("MDN — <details>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details")
MDN_META = ("MDN — <meta>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta")
MDN_REL = ("MDN — HTML attribute: rel", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel")
W3C_JSONLD = ("W3C — JSON-LD 1.1", "https://www.w3.org/TR/json-ld11/")
MDN_ARIA_INVALID = ("MDN — aria-invalid", "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid")
MDN_VALIDITY = ("MDN — ValidityState", "https://developer.mozilla.org/en-US/docs/Web/API/ValidityState")
WAI_FORM_NOTIFY = ("W3C WAI — Forms tutorial: user notifications", "https://www.w3.org/WAI/tutorials/forms/notifications/")
WEBDEV_RENDERING = ("web.dev — Rendering on the Web", "https://web.dev/articles/rendering-on-the-web")
MDN_HISTORY = ("MDN — History API", "https://developer.mozilla.org/en-US/docs/Web/API/History_API")

QUESTIONS = [
    # ------------------------------------------------------------------ html-004
    Q(
        id="html-004", sub="Accessibility", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["alt-text", "images", "accessibility"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""A product page has (1) a purely decorative wave divider image and (2) the shop logo, which is the only content of a link to the home page. Which markup is correct?""",
        q_bn=r"""একটা product page-এ আছে (1) শুধু সাজানোর জন্য একটা wave divider image, আর (2) দোকানের logo, যেটা home page-এর link-এর একমাত্র content। কোন markup সঠিক?""",
        options=[
            (r"""Divider: `<img src="wave.svg" alt="">` — Logo: `<a href="/"><img src="logo.png" alt="Dokan — home"></a>`""",
             r"""Divider: `<img src="wave.svg" alt="">` — Logo: `<a href="/"><img src="logo.png" alt="Dokan — home"></a>`"""),
            (r"""Divider: `<img src="wave.svg">` (no `alt`) — Logo: `<a href="/"><img src="logo.png" alt="logo"></a>`""",
             r"""Divider: `<img src="wave.svg">` (`alt` নেই) — Logo: `<a href="/"><img src="logo.png" alt="logo"></a>`"""),
            (r"""Divider: `<img src="wave.svg" alt="decorative wave image">` — Logo: `<a href="/"><img src="logo.png" alt="Dokan logo image"></a>`""",
             r"""Divider: `<img src="wave.svg" alt="decorative wave image">` — Logo: `<a href="/"><img src="logo.png" alt="Dokan logo image"></a>`"""),
            (r"""Divider: `<img src="wave.svg" alt="wave.svg">` — Logo: `<a href="/"><img src="logo.png" alt=""></a>`""",
             r"""Divider: `<img src="wave.svg" alt="wave.svg">` — Logo: `<a href="/"><img src="logo.png" alt=""></a>`"""),
        ],
        correct=0,
        a_en=r"""
            The first option. A decorative image gets an **empty** `alt=""` so screen readers skip it, and an image that is the only content of a link is a *functional* image — its `alt` should describe the link's purpose ("Dokan — home"), not the picture.
        """,
        a_bn=r"""
            প্রথম option-টা। Decorative image-এ **খালি** `alt=""` দিতে হয়, যাতে screen reader সেটা এড়িয়ে যায়। আর যে image একটা link-এর একমাত্র content, সেটা একটা *functional* image — তার `alt`-এ ছবির বর্ণনা নয়, link-এর উদ্দেশ্য লিখতে হয় ("Dokan — home")।
        """,
        quick_en=r"""The decorative divider gets `alt=""` so screen readers skip it, and the logo inside the home link gets an `alt` that describes the link's purpose ("Dokan — home"), not the picture.""",
        quick_bn=r"""Decorative divider-এ `alt=""` দিই যাতে screen reader সেটা skip করে, আর home link-এর ভেতরের logo-র `alt` হবে link-এর উদ্দেশ্য ("Dokan — home"), ছবির বর্ণনা নয়।""",
        ex_en=r"""
            The most tempting wrong option is the third one: it *has* alt text everywhere, but "decorative wave image" makes a screen reader announce noise for something that carries no information, and "logo image" is redundant — screen readers already say "image" or "graphic". The logo `alt` should tell users where the link goes.

            Option B is wrong because a missing `alt` is not the same as an empty one: many screen readers fall back to reading the file name ("wave dot svg"). Option D is the worst for the logo: an empty `alt` inside a link leaves the link with **no accessible name**, so it's announced as just "link".

            Quick rules: informative image → describe the information; functional image → describe the action/destination; decorative → `alt=""`; complex charts → short `alt` plus a longer description nearby. Decorative images that are purely visual are often better as CSS backgrounds anyway.
        """,
        ex_bn=r"""
            সবচেয়ে প্রলোভনজনক ভুল উত্তর তৃতীয়টা: সব জায়গায় alt text *আছে* ঠিকই, কিন্তু "decorative wave image" দিলে screen reader এমন একটা জিনিসের কথা অযথা পড়ে শোনায় যার কোনো তথ্য নেই, আর "logo image"-এর "image" শব্দটা অপ্রয়োজনীয় — screen reader নিজেই "image" বা "graphic" বলে। Logo-র `alt`-এ বলা উচিত link-টা কোথায় নিয়ে যায়।

            Option B ভুল, কারণ `alt` না থাকা আর খালি `alt` এক জিনিস নয়: অনেক screen reader তখন file-এর নাম পড়ে ফেলে ("wave dot svg")। Logo-র জন্য option D সবচেয়ে খারাপ: link-এর ভেতরে খালি `alt` থাকলে link-টার **কোনো accessible name থাকে না**, ফলে শুধু "link" বলে শোনায়।

            দ্রুত নিয়ম: তথ্যবহ image → তথ্যটা বর্ণনা করো; functional image → action বা গন্তব্য বর্ণনা করো; decorative → `alt=""`; জটিল chart → ছোট `alt` আর পাশে বিস্তারিত বর্ণনা। শুধু দেখার জন্য থাকা decorative image অনেক সময় CSS background হিসেবেই ভালো।
        """,
        tip_en=r"""Name the category of each image (decorative vs functional) before giving the markup — the categories are what interviewers want to hear.""",
        tip_bn=r"""Markup বলার আগে প্রতিটা image কোন শ্রেণির (decorative নাকি functional) সেটা বলো — interviewer আসলে এই শ্রেণিবিভাগটাই শুনতে চায়।""",
        refs=[MDN_IMG, WAI_IMAGES],
    ),
    # ------------------------------------------------------------------ html-005
    Q(
        id="html-005", sub="Accessibility", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["forms", "label", "placeholder", "fieldset", "accessibility"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""How do you correctly label a form input in HTML, and why isn't a `placeholder` enough?""",
        q_bn=r"""HTML-এ একটা form input-কে সঠিকভাবে label করবে কীভাবে? আর শুধু `placeholder` দিলে কেন যথেষ্ট নয়?""",
        a_en=r"""
            Use a `<label>` element, either with `for` matching the input's `id`, or by wrapping the input inside the label. That gives the input an **accessible name**, so screen readers announce "Mobile number, edit text", and clicking the label focuses the input — for checkboxes and radios that also makes the tap target much bigger on phones.

            A `placeholder` isn't a label: it disappears as soon as the user types (so they forget what the field was), it's usually low-contrast grey, and it isn't reliably used as the accessible name. Placeholders are fine for an *example format*, like `01712345678`, alongside a real label.

            For a group of radio buttons or checkboxes, I wrap them in `<fieldset>` with a `<legend>` so the question ("Payment method") is announced together with each option.
        """,
        a_bn=r"""
            `<label>` element ব্যবহার করো — হয় `for` দিয়ে input-এর `id`-এর সাথে মিলিয়ে, নয়তো input-কে label-এর ভেতরে wrap করে। এতে input একটা **accessible name** পায়, ফলে screen reader বলে "Mobile number, edit text", আর label-এ click করলে input-এ focus যায় — checkbox ও radio-র ক্ষেত্রে এতে phone-এ tap করার জায়গাও অনেক বড় হয়।

            `placeholder` কোনো label নয়: user type করা শুরু করলেই এটা মুছে যায় (তখন field-টা কীসের ছিল ভুলে যায়), সাধারণত হালকা ধূসর আর কম contrast-এর হয়, আর এটা নির্ভরযোগ্যভাবে accessible name হিসেবে ব্যবহৃত হয় না। আসল label-এর পাশাপাশি *উদাহরণ format* দেখাতে placeholder ঠিক আছে, যেমন `01712345678`।

            একগুচ্ছ radio button বা checkbox-এর জন্য আমি সেগুলোকে `<legend>`-সহ `<fieldset>`-এ wrap করি, যাতে প্রতিটা option-এর সাথে প্রশ্নটাও ("Payment method") শোনা যায়।
        """,
        quick_en=r"""Use a `<label>` whose `for` matches the input's `id` (or wrap the input in it): that gives an accessible name and a bigger click target. A `placeholder` disappears when you type, is low-contrast and isn't a reliable name, so use it only for an example format.""",
        quick_bn=r"""Input-এর `id`-এর সাথে মিলিয়ে `for`-সহ `<label>` দাও (বা input-কে label-এর ভেতরে রাখো); এতে accessible name আর বড় click target দুটোই পাওয়া যায়। `placeholder` type করলেই হারিয়ে যায়, রং হালকা, আর নির্ভরযোগ্য name নয়, তাই এটা শুধু example format দেখানোর জন্য।""",
        ex_en=r"""
            - **Explicit vs implicit:** `for`/`id` works even when the label and input are far apart in the DOM; wrapping is handy for checkboxes. Both are valid; explicit association is the most robust across assistive tech.
            - **`for` points to an `id`, not a `name`.** And IDs must be unique — two inputs with `id="email"` (common when a component renders twice) break the association.
            - **Visually hidden labels:** if the design truly has no visible label (e.g. a search box with a button labelled "Search"), use a visually-hidden `<label>` or `aria-label`. But visible labels help everyone, including users with cognitive disabilities.
            - **Helpful extras:** `autocomplete="tel"`, `inputmode="numeric"` and the right `type` make mobile keyboards and autofill work — a big win on phones.
        """,
        ex_bn=r"""
            - **Explicit বনাম implicit:** `for`/`id` তখনো কাজ করে, যখন DOM-এ label আর input অনেক দূরে থাকে; checkbox-এর জন্য wrap করা সুবিধাজনক। দুটোই valid; তবে assistive tech-এ explicit association সবচেয়ে নির্ভরযোগ্য।
            - **`for` একটা `id`-কে নির্দেশ করে, `name`-কে নয়।** আর ID অবশ্যই unique হতে হবে — দুটো input-এ `id="email"` থাকলে (একই component দুবার render হলে প্রায়ই এমন হয়) association ভেঙে যায়।
            - **Visually hidden label:** design-এ যদি সত্যিই দেখা যায় এমন label না থাকে (যেমন পাশে "Search" button-সহ search box), তাহলে visually-hidden `<label>` বা `aria-label` ব্যবহার করো। তবে দৃশ্যমান label সবার উপকারে আসে, cognitive disability থাকা user-দেরও।
            - **কাজের বাড়তি জিনিস:** `autocomplete="tel"`, `inputmode="numeric"` আর সঠিক `type` দিলে mobile keyboard আর autofill ঠিকমতো কাজ করে — phone-এ এটা বড় সুবিধা।
        """,
        tip_en=r"""Give the two association methods, then one concrete user benefit (screen reader announcement, bigger tap target). Calling placeholder "a hint, not a label" is a crisp line to use.""",
        tip_bn=r"""দুটো association পদ্ধতি বলো, তারপর user-এর একটা বাস্তব সুবিধা উল্লেখ করো (screen reader-এর ঘোষণা, বড় tap target)। Placeholder হলো "hint, label নয়" — এই ছোট কথাটা ব্যবহার করতে পারো।""",
        mist_en=r"""Using `for` with the input's `name`, duplicate IDs, styling a `<span>` or `<p>` as a label, and relying on placeholders alone.""",
        mist_bn=r"""Input-এর `name` দিয়ে `for` লেখা, duplicate ID, `<span>` বা `<p>`-কে label-এর মতো style করা, আর শুধু placeholder-এর উপর ভরসা করা।""",
        code=r"""
            <!-- Explicit association -->
            <label for="phone">Mobile number</label>
            <input id="phone" name="phone" type="tel" inputmode="numeric"
                   autocomplete="tel" placeholder="01712345678">

            <!-- Implicit association + grouped options -->
            <fieldset>
              <legend>Payment method</legend>
              <label><input type="radio" name="pay" value="cod"> Cash on delivery</label>
              <label><input type="radio" name="pay" value="card"> Card</label>
              <label><input type="radio" name="pay" value="mobile"> Mobile banking</label>
            </fieldset>
        """,
        lang="html",
        follow=[
            ("When is `aria-label` acceptable instead of a visible label?", "কখন দৃশ্যমান label-এর বদলে `aria-label` গ্রহণযোগ্য?"),
            ("How do you associate a hint or an error message with an input?", "একটা hint বা error message-কে input-এর সাথে কীভাবে যুক্ত করবে?"),
        ],
        related=["html-024", "html-026"],
        refs=[MDN_LABEL, MDN_FIELDSET],
    ),
    # ------------------------------------------------------------------ html-006
    Q(
        id="html-006", sub="Data Attributes", diff="easy", type="output",
        prio="medium", market="bangladesh", mins=3,
        tags=["data-attributes", "dataset", "dom", "output"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""What does this code log to the console?""",
        q_bn=r"""এই code console-এ কী log করবে?""",
        a_en=r"""
            `data-*` attributes are exposed through `element.dataset`, with the `data-` prefix removed and kebab-case converted to camelCase (`data-product-id` → `dataset.productId`). The key point is that **every value is a string**:
            - `productId + 1` is string concatenation → `"421"`.
            - `inStock` is the string `"false"`, which is truthy → `"available"`.
            - `typeof price` is `"string"`.
            - Assigning `dataset.discountRate` creates a new attribute `data-discount-rate`, added after the existing ones.
        """,
        a_bn=r"""
            `data-*` attribute-গুলো `element.dataset` দিয়ে পাওয়া যায় — `data-` prefix বাদ যায় আর kebab-case camelCase-এ বদলে যায় (`data-product-id` → `dataset.productId`)। মূল কথা হলো **প্রতিটা value string**:
            - `productId + 1` হলো string concatenation → `"421"`।
            - `inStock` হলো string `"false"`, যেটা truthy → `"available"`।
            - `typeof price` হলো `"string"`।
            - `dataset.discountRate`-এ value assign করলে নতুন একটা `data-discount-rate` attribute তৈরি হয়, যেটা আগের attribute-গুলোর পরে যোগ হয়।
        """,
        quick_en=r"""It logs `421`, `available`, `string`, then the button's HTML with a new `data-discount-rate="10"` at the end. Every `dataset` value is a string, so `"42" + 1` concatenates and `"false"` is truthy.""",
        quick_bn=r"""Output: `421`, `available`, `string`, তারপর শেষে নতুন `data-discount-rate="10"`-সহ button-এর HTML। `dataset`-এর সব value string, তাই `"42" + 1` জোড়া লাগে, আর `"false"` truthy।""",
        ex_en=r"""
            Step by step:
            1. Destructuring reads three string values: `"42"`, `"false"`, `"1250.50"`.
            2. `"42" + 1` → `"421"` because `+` with a string concatenates.
            3. Any non-empty string is truthy, so `"false"` takes the `'available'` branch. Convert explicitly: `dataset.inStock === 'true'`.
            4. Numbers need `Number(price)` (or `parseFloat`). For money, keep integer paisa/cents to avoid floating-point issues.
            5. Setting a camelCase key writes a kebab-case attribute; `delete btn.dataset.discountRate` would remove it.

            When to use `data-*`: small bits of per-element data for scripts or CSS hooks (`[data-state="open"]`). Don't store large JSON or sensitive data in them — it's visible in the HTML, and the DOM is not a database.
        """,
        ex_bn=r"""
            ধাপে ধাপে:
            1. Destructuring তিনটা string value পড়ে: `"42"`, `"false"`, `"1250.50"`।
            2. `"42" + 1` → `"421"`, কারণ string থাকলে `+` concatenate করে।
            3. খালি নয় এমন যেকোনো string truthy, তাই `"false"` থাকা সত্ত্বেও `'available'` branch চলে। স্পষ্টভাবে convert করো: `dataset.inStock === 'true'`।
            4. Number লাগলে `Number(price)` (বা `parseFloat`) ব্যবহার করো। টাকার হিসাবের জন্য floating-point সমস্যা এড়াতে পয়সা/cents-এ integer রাখো।
            5. camelCase key set করলে kebab-case attribute লেখা হয়; `delete btn.dataset.discountRate` দিলে সেটা মুছে যাবে।

            কখন `data-*` ব্যবহার করবে: script বা CSS hook-এর জন্য element-ভিত্তিক ছোটখাটো data (`[data-state="open"]`)। এতে বড় JSON বা sensitive data রেখো না — এটা HTML-এ সবাই দেখতে পায়, আর DOM কোনো database নয়।
        """,
        tip_en=r"""Say "dataset values are always strings" before tracing the lines — that one fact explains every surprising output here.""",
        tip_bn=r"""Line ধরে trace করার আগেই বলো "dataset-এর value সবসময় string" — এই একটা তথ্যই এখানকার প্রতিটা অবাক করা output ব্যাখ্যা করে।""",
        mist_en=r"""Expecting `43`, expecting `'sold out'`, or writing `dataset['product-id']` (it's `dataset.productId`).""",
        mist_bn=r"""`43` আশা করা, `'sold out'` আশা করা, অথবা `dataset['product-id']` লেখা (সঠিক হলো `dataset.productId`)।""",
        code=r"""
            <button id="buy" data-product-id="42" data-in-stock="false" data-price="1250.50">Buy</button>

            <script>
              const btn = document.getElementById('buy');
              const { productId, inStock, price } = btn.dataset;

              console.log(productId + 1);
              console.log(inStock ? 'available' : 'sold out');
              console.log(typeof price);

              btn.dataset.discountRate = '10';
              console.log(btn.outerHTML);
            </script>
        """,
        lang="html",
        output=r"""
            421
            available
            string
            <button id="buy" data-product-id="42" data-in-stock="false" data-price="1250.50" data-discount-rate="10">Buy</button>
        """,
        follow=[
            ("How would you select elements by a data attribute in CSS and in `querySelector`?", "CSS-এ আর `querySelector`-এ data attribute দিয়ে element কীভাবে select করবে?"),
            ("When would you avoid storing state in `data-*` attributes?", "কখন `data-*` attribute-এ state রাখা এড়িয়ে চলবে?"),
        ],
        related=["html-007"],
        refs=[MDN_DATASET],
    ),
    # ------------------------------------------------------------------ html-015
    Q(
        id="html-015", sub="HTML APIs", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["popover", "top-layer", "light-dismiss", "html-apis"],
        ver="HTML Living Standard; popover Baseline newly available (Jan 2025)", vs=True, status="stable",
        q_en=r"""Given `<button popovertarget="menu">Menu</button>` and `<div id="menu" popover>…</div>` (so `popover="auto"`), which statement is correct?""",
        q_bn=r"""`<button popovertarget="menu">Menu</button>` আর `<div id="menu" popover>…</div>` (অর্থাৎ `popover="auto"`) দেওয়া আছে। কোন কথাটা সঠিক?""",
        options=[
            ("It's modal: the rest of the page becomes inert and focus is trapped inside, like `showModal()`.",
             "এটা modal: `showModal()`-এর মতো page-এর বাকি অংশ inert হয়ে যায় আর focus ভেতরে আটকে থাকে।"),
            ("It's shown in the top layer, light-dismisses on an outside click or Esc, and opening it closes other unrelated `auto` popovers.",
             "এটা top layer-এ দেখায়, বাইরে click করলে বা Esc চাপলে light dismiss হয়, আর এটা খুললে অন্য অসম্পর্কিত `auto` popover বন্ধ হয়ে যায়।"),
            ("It needs `position: fixed` and a high `z-index` to appear above other content.",
             "অন্য content-এর উপরে দেখাতে এর জন্য `position: fixed` আর বড় `z-index` লাগে।"),
            ("It only works with JavaScript: you must call `menu.showPopover()` in a click handler.",
             "এটা শুধু JavaScript দিয়ে কাজ করে: click handler-এ অবশ্যই `menu.showPopover()` call করতে হবে।"),
        ],
        correct=1,
        a_en=r"""
            The second statement. An `auto` popover is rendered in the **top layer**, supports **light dismiss** (click outside or Esc), and only one unrelated `auto` popover can be open at a time — opening one closes the others (nested popovers opened from inside it stay open). It is **non-modal**.
        """,
        a_bn=r"""
            দ্বিতীয় কথাটা। `auto` popover **top layer**-এ render হয়, **light dismiss** support করে (বাইরে click বা Esc), আর একসাথে একটাই অসম্পর্কিত `auto` popover খোলা থাকতে পারে — একটা খুললে বাকিগুলো বন্ধ হয় (এর ভেতর থেকে খোলা nested popover খোলা থাকে)। এটা **non-modal**।
        """,
        quick_en=r"""An `auto` popover is shown in the top layer, light-dismisses on an outside click or Esc, and opening it closes other unrelated `auto` popovers. It is non-modal and needs no `z-index` or JavaScript.""",
        quick_bn=r"""`auto` popover top layer-এ দেখায়, বাইরে click বা Esc চাপলে light dismiss হয়, আর খুললে অন্য unrelated `auto` popover বন্ধ হয়ে যায়। এটা non-modal, আর `z-index` বা JavaScript লাগে না।""",
        ex_en=r"""
            The tempting wrong answer is the first one, because popovers and modal dialogs both appear "on top". But a popover never makes the page inert or traps focus — the user can keep interacting with the page. For a blocking confirmation, use `<dialog>` with `showModal()`.

            Other details worth knowing:
            - Because it's in the top layer, no `z-index` or `position: fixed` is needed (option C), and it escapes `overflow: hidden` ancestors.
            - `popovertarget` wires it up with zero JavaScript (option D is wrong); `popovertargetaction` can be `show`, `hide` or `toggle` (the default). The browser also creates the `aria-expanded` relationship on the invoking button.
            - `popover="manual"` turns off light dismiss and lets several popovers stay open — useful for toasts.
            - Popover has been Baseline newly available since January 2025. The more general invoker commands (`commandfor` + `command="toggle-popover"`) do the same job and also work for dialogs.
        """,
        ex_bn=r"""
            প্রলোভনজনক ভুল উত্তর প্রথমটা, কারণ popover আর modal dialog দুটোই "উপরে" দেখায়। কিন্তু popover কখনো page-কে inert করে না বা focus আটকায় না — user page-এর সাথে কাজ চালিয়ে যেতে পারে। Blocking confirmation-এর জন্য `showModal()`-সহ `<dialog>` ব্যবহার করো।

            আরও কিছু জানার মতো বিষয়:
            - Top layer-এ থাকায় `z-index` বা `position: fixed` লাগে না (option C ভুল), আর এটা `overflow: hidden` থাকা ancestor-এর বাইরেও দেখা যায়।
            - `popovertarget` কোনো JavaScript ছাড়াই এটাকে যুক্ত করে দেয় (তাই option D ভুল); `popovertargetaction` হতে পারে `show`, `hide` বা `toggle` (default)। Browser invoking button-এ `aria-expanded` সম্পর্কও তৈরি করে দেয়।
            - `popover="manual"` light dismiss বন্ধ করে আর একসাথে কয়েকটা popover খোলা রাখতে দেয় — toast-এর জন্য কাজের।
            - Popover January 2025 থেকে Baseline newly available। আরও সাধারণ invoker command (`commandfor` + `command="toggle-popover"`) একই কাজ করে, আর dialog-এর জন্যও কাজ করে।
        """,
        tip_en=r"""Contrast it with `<dialog>` in one line: "popover = non-modal, light-dismissable, top layer; modal dialog = blocks the page". That comparison is usually the real question behind this one.""",
        tip_bn=r"""এক লাইনে `<dialog>`-এর সাথে তুলনা করো: "popover = non-modal, light dismiss হয়, top layer; modal dialog = পুরো page আটকে দেয়"। এই প্রশ্নের পেছনে আসল প্রশ্ন সাধারণত এই তুলনাটাই।""",
        refs=[MDN_POPOVER],
    ),
    # ------------------------------------------------------------------ html-016
    Q(
        id="html-016", sub="HTML APIs", diff="medium", type="conceptual",
        prio="medium", market="both", mins=5,
        tags=["invoker-commands", "commandfor", "details", "accordion", "html-apis"],
        ver="HTML Living Standard; invoker commands Baseline newly available (Dec 2025); <details name> Baseline newly available", vs=True, status="stable",
        q_en=r"""Modern HTML lets you build interactive UI with little or no JavaScript. Explain invoker commands (`command` / `commandfor`) and exclusive accordions with `<details name>`. What are their limits?""",
        q_bn=r"""আধুনিক HTML দিয়ে খুব কম বা একদম JavaScript ছাড়াই interactive UI বানানো যায়। Invoker command (`command` / `commandfor`) আর `<details name>` দিয়ে exclusive accordion ব্যাখ্যা করো। এগুলোর সীমাবদ্ধতা কী?""",
        a_en=r"""
            **Invoker commands** let a `<button>` control another element declaratively. `commandfor` takes the target's `id`, and `command` says what to do. Built-in commands are `show-modal`, `close` and `request-close` for `<dialog>`, and `show-popover`, `hide-popover` and `toggle-popover` for popovers. You can also define **custom commands** that start with `--` (like `--rotate-left`): the button then dispatches a `command` event (a `CommandEvent` with a `.command` property) on the target, so the logic lives in one listener on the target instead of a click handler per button. It's a generalisation of `popovertarget`.

            **`<details>`/`<summary>`** is a native disclosure widget with keyboard and screen-reader support built in. Giving several `<details>` the same `name` turns them into an **exclusive accordion**: opening one closes the others in the group.

            Limits: invoker commands have only been Baseline (newly available) since December 2025, so older browsers need a JavaScript fallback; built-in commands only cover dialogs and popovers. Exclusive accordions are wrong when users need to compare several sections at once, and heavy custom styling of `<summary>` can accidentally remove its semantics or focus styles.
        """,
        a_bn=r"""
            **Invoker command** দিয়ে একটা `<button>` declaratively অন্য একটা element নিয়ন্ত্রণ করতে পারে। `commandfor` target-এর `id` নেয়, আর `command` বলে দেয় কী করতে হবে। Built-in command হলো `<dialog>`-এর জন্য `show-modal`, `close` আর `request-close`, আর popover-এর জন্য `show-popover`, `hide-popover` আর `toggle-popover`। `--` দিয়ে শুরু হওয়া **custom command**-ও (যেমন `--rotate-left`) বানানো যায়: তখন button target-এর উপর একটা `command` event (`.command` property-সহ একটা `CommandEvent`) dispatch করে, ফলে প্রতিটা button-এ click handler না লিখে target-এর একটা listener-এ সব logic রাখা যায়। এটা `popovertarget`-এর একটা সাধারণ রূপ।

            **`<details>`/`<summary>`** একটা native disclosure widget, যাতে keyboard আর screen reader support আগে থেকেই আছে। কয়েকটা `<details>`-কে একই `name` দিলে সেগুলো একটা **exclusive accordion** হয়ে যায়: group-এর একটা খুললে বাকিগুলো বন্ধ হয়।

            সীমাবদ্ধতা: invoker command December 2025 থেকে মাত্র Baseline (newly available), তাই পুরোনো browser-এর জন্য JavaScript fallback লাগবে; built-in command শুধু dialog আর popover কভার করে। যখন user-কে একসাথে কয়েকটা section মিলিয়ে দেখতে হয়, তখন exclusive accordion ভুল পছন্দ, আর `<summary>`-কে বেশি custom style করতে গিয়ে অনেক সময় এর semantics বা focus style হারিয়ে যায়।
        """,
        quick_en=r"""Invoker commands let a `<button>` with `commandfor` and `command` open or close a dialog or popover, or send a custom `--` command event, without click handlers. `<details>` sharing a `name` form an exclusive accordion. Invoker commands are Baseline only since December 2025, so keep a fallback.""",
        quick_bn=r"""Invoker command দিয়ে `commandfor` আর `command`-সহ একটা `<button>` click handler ছাড়াই dialog বা popover খুলতে-বন্ধ করতে, বা `--` দিয়ে শুরু custom command event পাঠাতে পারে। একই `name`-এর `<details>`-গুলো মিলে exclusive accordion হয়। Invoker command মাত্র December 2025 থেকে Baseline, তাই fallback রাখো।""",
        ex_en=r"""
            - **Why declarative matters:** fewer event listeners, works before your JavaScript bundle has loaded (useful on slow networks), and the browser wires up accessibility relationships for you.
            - **`request-close` vs `close`:** `request-close` fires the dialog's `cancel` event first, so your code can `preventDefault()` (for example, "You have unsaved changes"); `close` closes immediately.
            - **Progressive enhancement:** feature-detect with `'command' in HTMLButtonElement.prototype` and attach a fallback click handler if it's missing.
            - **`<details>` events:** listen to the `toggle` event to lazy-load content when a section opens. The `open` attribute reflects state, so CSS like `details[open] summary` works without JavaScript.
            - Don't put interactive elements such as links or buttons inside `<summary>` — nested interactive content confuses keyboard and screen-reader users.
        """,
        ex_bn=r"""
            - **Declarative কেন গুরুত্বপূর্ণ:** event listener কম লাগে, JavaScript bundle load হওয়ার আগেই কাজ করে (ধীর network-এ কাজের), আর browser নিজেই accessibility সম্পর্কগুলো যুক্ত করে দেয়।
            - **`request-close` বনাম `close`:** `request-close` আগে dialog-এর `cancel` event fire করে, ফলে তোমার code `preventDefault()` করতে পারে (যেমন "আপনার পরিবর্তনগুলো save হয়নি"); `close` সঙ্গে সঙ্গে বন্ধ করে দেয়।
            - **Progressive enhancement:** `'command' in HTMLButtonElement.prototype` দিয়ে feature detect করো, না থাকলে fallback click handler যোগ করো।
            - **`<details>`-এর event:** কোনো section খুললে content lazy-load করতে `toggle` event-এ listen করো। `open` attribute state প্রতিফলিত করে, তাই `details[open] summary`-এর মতো CSS JavaScript ছাড়াই কাজ করে।
            - `<summary>`-এর ভেতরে link বা button-এর মতো interactive element রেখো না — nested interactive content keyboard আর screen reader user-দের বিভ্রান্ত করে।
        """,
        tip_en=r"""Show you know the exact attribute names and a couple of built-in commands, then immediately mention Baseline status and a fallback — that's what separates "read a blog post" from "would ship it".""",
        tip_bn=r"""দেখাও যে তুমি attribute-এর সঠিক নাম আর কয়েকটা built-in command জানো, তারপর সঙ্গে সঙ্গে Baseline status আর fallback-এর কথা বলো — "একটা blog post পড়েছি" আর "production-এ ship করব"-এর পার্থক্য এখানেই।""",
        mist_en=r"""Writing `commandfor` with a CSS selector instead of an ID, forgetting the `--` prefix on custom commands, or assuming every visitor's browser supports invoker commands.""",
        mist_bn=r"""`commandfor`-এ ID-র বদলে CSS selector লেখা, custom command-এ `--` prefix দিতে ভুলে যাওয়া, অথবা ধরে নেওয়া যে প্রত্যেক visitor-এর browser invoker command support করে।""",
        code=r"""
            <!-- Built-in commands: no JavaScript needed -->
            <button type="button" commandfor="filters" command="show-modal">Filters</button>
            <dialog id="filters" aria-labelledby="filters-title">
              <h2 id="filters-title">Filter products</h2>
              <!-- ...filter controls... -->
              <button type="button" commandfor="filters" command="close">Done</button>
            </dialog>

            <!-- Custom command handled on the target -->
            <button type="button" commandfor="gallery" command="--next">Next photo</button>
            <div id="gallery"><!-- slides --></div>
            <script type="module">
              document.getElementById('gallery').addEventListener('command', (event) => {
                if (event.command === '--next') showNextPhoto();
              });
            </script>

            <!-- Exclusive accordion -->
            <details name="faq" open>
              <summary>How long does delivery take inside Dhaka?</summary>
              <p>Usually 1–2 days.</p>
            </details>
            <details name="faq">
              <summary>Can I pay with mobile banking?</summary>
              <p>Yes, along with cards and cash on delivery.</p>
            </details>
        """,
        lang="html",
        follow=[
            ("How would you feature-detect invoker commands and provide a fallback?", "Invoker command-এর feature detection আর fallback কীভাবে করবে?"),
            ("When is an accordion a bad UX choice?", "কখন accordion খারাপ UX পছন্দ?"),
        ],
        related=["html-014", "html-015"],
        refs=[MDN_INVOKERS, MDN_DETAILS],
    ),
    # ------------------------------------------------------------------ html-017
    Q(
        id="html-017", sub="SEO and Meta Tags", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["seo", "meta-tags", "open-graph", "canonical", "json-ld"],
        ver="HTML Living Standard; schema.org vocabulary (version-independent)", vs=False, status="stable",
        q_en=r"""Which SEO- and sharing-related tags would you put in the `<head>` of a product page, and what does each one do? Include canonical, Open Graph and structured data.""",
        q_bn=r"""একটা product page-এর `<head>`-এ SEO আর sharing-এর জন্য কোন কোন tag রাখবে, আর প্রতিটা কী কাজ করে? Canonical, Open Graph আর structured data অবশ্যই বলবে।""",
        a_en=r"""
            - `<title>` — unique and descriptive per page (product name + brand). It's the clickable headline in search results.
            - `<meta name="description">` — a candidate for the search snippet. It doesn't directly boost rankings, but a good one improves click-through.
            - `<link rel="canonical" href="…">` — the preferred absolute URL when the same product is reachable through several URLs (`?utm_source=…`, `?sort=…`, category paths), so ranking signals aren't split.
            - **Open Graph** (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) — controls the preview card when the link is shared on Facebook, Messenger, WhatsApp, LinkedIn and others. For Bangladeshi shops, where a lot of discovery happens through Facebook, this is just as important as search.
            - **Structured data** as JSON-LD (`<script type="application/ld+json">`) using schema.org `Product` and `Offer` — price, currency (`BDT`), availability — which makes the page eligible for rich results.
            - Optionally `hreflang` alternates for Bangla and English versions, and `<meta name="robots" content="noindex">` only on pages that shouldn't be indexed (cart, internal search).
        """,
        a_bn=r"""
            - `<title>` — প্রতিটা page-এর জন্য আলাদা ও বর্ণনামূলক (product-এর নাম + brand)। Search result-এ click করার headline এটাই।
            - `<meta name="description">` — search snippet-এর সম্ভাব্য উৎস। এটা সরাসরি ranking বাড়ায় না, তবে ভালো description click-through বাড়ায়।
            - `<link rel="canonical" href="…">` — একই product যখন কয়েকটা URL দিয়ে পাওয়া যায় (`?utm_source=…`, `?sort=…`, category path), তখন পছন্দের absolute URL কোনটা তা জানায়, যাতে ranking signal ভাগ হয়ে না যায়।
            - **Open Graph** (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) — Facebook, Messenger, WhatsApp, LinkedIn ইত্যাদিতে link share করলে preview card কেমন দেখাবে তা নিয়ন্ত্রণ করে। বাংলাদেশি দোকানের ক্ষেত্রে, যেখানে অনেক customer Facebook থেকে আসে, এটা search-এর মতোই গুরুত্বপূর্ণ।
            - JSON-LD আকারে **structured data** (`<script type="application/ld+json">`), schema.org-এর `Product` আর `Offer` দিয়ে — দাম, currency (`BDT`), stock-এর অবস্থা — এতে page rich result-এর যোগ্য হয়।
            - চাইলে Bangla আর English version-এর জন্য `hreflang` alternate, আর যেসব page index হওয়া উচিত নয় (cart, internal search) শুধু সেখানে `<meta name="robots" content="noindex">`।
        """,
        quick_en=r"""A unique `<title>` and meta description for the search result, `rel="canonical"` so duplicate URLs don't split ranking, Open Graph tags for Facebook and WhatsApp share previews, and JSON-LD with schema.org `Product`/`Offer` for rich results.""",
        quick_bn=r"""Search result-এর জন্য unique `<title>` আর meta description, duplicate URL-এ ranking ভাগ না হতে `rel="canonical"`, Facebook আর WhatsApp share preview-এর জন্য Open Graph tag, আর rich result-এর জন্য JSON-LD-তে schema.org `Product`/`Offer`।""",
        ex_en=r"""
            - **Open Graph uses `property`, not `name`:** `<meta property="og:image" content="…">`. Use an absolute image URL; around 1200×630 works well across platforms.
            - **Social crawlers generally don't run JavaScript.** If these tags are injected client-side by an SPA, previews will show your default tags — they must be in the server HTML.
            - **Canonical is a hint, not a command.** Keep it consistent with internal links, sitemaps and redirects, and always use absolute URLs.
            - **Structured data must match visible content.** Marking up a price or rating that isn't on the page can get rich results removed. When generating JSON-LD from user-supplied data, serialize it safely — a product name containing `</script>` must not be able to break out of the script block.
            - `<meta name="keywords">` is ignored by major search engines; don't spend time on it.
        """,
        ex_bn=r"""
            - **Open Graph-এ `name` নয়, `property` লাগে:** `<meta property="og:image" content="…">`। Image URL absolute দাও; সব platform-এ মোটামুটি 1200×630 ভালো কাজ করে।
            - **Social crawler সাধারণত JavaScript চালায় না।** কোনো SPA যদি client-side-এ এই tag inject করে, তাহলে preview-তে default tag-ই দেখাবে — এগুলো অবশ্যই server-এর HTML-এ থাকতে হবে।
            - **Canonical একটা hint, আদেশ নয়।** Internal link, sitemap আর redirect-এর সাথে এটা সামঞ্জস্যপূর্ণ রাখো, আর সবসময় absolute URL দাও।
            - **Structured data অবশ্যই দৃশ্যমান content-এর সাথে মিলতে হবে।** Page-এ নেই এমন দাম বা rating markup করলে rich result বাতিল হতে পারে। User-এর দেওয়া data থেকে JSON-LD বানালে নিরাপদভাবে serialize করো — কোনো product-এর নামে `</script>` থাকলে সেটা যেন script block ভেঙে বের হতে না পারে।
            - বড় search engine-গুলো `<meta name="keywords">` উপেক্ষা করে; এতে সময় নষ্ট কোরো না।
        """,
        tip_en=r"""Group your answer by audience: search engines (title, description, canonical, robots, JSON-LD) and social platforms (Open Graph). Mentioning that social crawlers don't run JavaScript connects nicely to SPA/SSR discussions.""",
        tip_bn=r"""উত্তরটা audience অনুযায়ী ভাগ করো: search engine (title, description, canonical, robots, JSON-LD) আর social platform (Open Graph)। Social crawler যে JavaScript চালায় না — এটা বললে আলোচনাটা সুন্দরভাবে SPA/SSR-এর দিকে যায়।""",
        mist_en=r"""Using relative canonical URLs, `name="og:title"` instead of `property`, the same title/description on every page, or adding tags only on the client in an SPA.""",
        mist_bn=r"""Relative canonical URL দেওয়া, `property`-র বদলে `name="og:title"` লেখা, সব page-এ একই title/description রাখা, অথবা SPA-তে শুধু client-side-এ tag যোগ করা।""",
        code=r"""
            <head>
              <meta charset="utf-8">
              <title>Cotton Panjabi — Navy | Dokan</title>
              <meta name="description" content="Breathable navy cotton panjabi, sizes 38–46. Free delivery inside Dhaka.">
              <link rel="canonical" href="https://dokan.example/products/panjabi-navy">
              <link rel="alternate" hreflang="bn" href="https://dokan.example/bn/products/panjabi-navy">

              <meta property="og:type" content="product">
              <meta property="og:title" content="Cotton Panjabi — Navy">
              <meta property="og:description" content="Breathable navy cotton panjabi, sizes 38–46.">
              <meta property="og:image" content="https://dokan.example/img/panjabi-navy-1200x630.jpg">
              <meta property="og:url" content="https://dokan.example/products/panjabi-navy">

              <script type="application/ld+json">
              {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": "Cotton Panjabi — Navy",
                "image": ["https://dokan.example/img/panjabi-navy-1200.jpg"],
                "sku": "PJ-NAVY-42",
                "offers": {
                  "@type": "Offer",
                  "price": "1850.00",
                  "priceCurrency": "BDT",
                  "availability": "https://schema.org/InStock",
                  "url": "https://dokan.example/products/panjabi-navy"
                }
              }
              </script>
            </head>
        """,
        lang="html",
        follow=[
            ("Why does a shared link still show an old preview image after you updated `og:image`?", "`og:image` বদলানোর পরও share করা link-এ কেন পুরোনো preview image দেখায়?"),
            ("When would you use `noindex` vs a canonical tag?", "কখন `noindex` আর কখন canonical tag ব্যবহার করবে?"),
        ],
        related=["html-025", "html-002"],
        refs=[MDN_META, MDN_REL, W3C_JSONLD],
    ),
    # ------------------------------------------------------------------ html-024
    Q(
        id="html-024", sub="Practical Scenarios", diff="hard", type="scenario",
        prio="high", market="both", mins=10,
        tags=["forms", "accessibility", "error-handling", "aria", "validation"],
        ver="HTML Living Standard; WAI-ARIA 1.2 (version-independent)", vs=False, status="stable",
        q_en=r"""Users of a checkout form — some using screen readers, most on mobile — say they can't tell what went wrong after pressing "Place order". Design an accessible approach for showing both client-side and server-side validation errors.""",
        q_bn=r"""একটা checkout form-এর user-রা — কেউ কেউ screen reader ব্যবহার করে, বেশিরভাগই mobile-এ — বলছে "Place order" চাপার পর কী ভুল হয়েছে তারা বুঝতে পারছে না। Client-side আর server-side দুই ধরনের validation error দেখানোর জন্য একটা accessible পদ্ধতি design করো।""",
        a_en=r"""
            My approach:

            1. **Keep native constraints, own the presentation.** Keep `required`, `type`, `pattern` and friends, but add `novalidate` to the form so I can render consistent inline errors instead of the browser's disappearing bubbles. I still use the Constraint Validation API (`input.validity`) to decide *what* is wrong.
            2. **Per-field errors:** set `aria-invalid="true"` on the input, write the message into an element referenced by `aria-describedby`, keep it visible next to the field, and don't rely on red colour alone (text plus an icon).
            3. **On submit with errors:** show an error summary at the top ("There are 2 problems") listing links to each field, and move focus to that summary. Screen-reader users hear the problems immediately, and everyone can jump to the fields.
            4. **Server-side errors** ("This mobile number is already registered", "Payment declined") go through exactly the same slots — field message + summary — so the UI is consistent. Preserve everything the user typed.
            5. **Timing:** validate on submit, and re-validate a field on `blur`/`input` once it's been marked invalid, so errors clear as soon as they're fixed — not shouting errors while the user is still typing.
            6. **Write useful messages:** "Enter an 11-digit mobile number starting with 01, like 01712345678", not "Invalid input".
        """,
        a_bn=r"""
            আমার পদ্ধতি:

            1. **Native constraint রাখো, দেখানোর দায়িত্ব নিজে নাও।** `required`, `type`, `pattern` ইত্যাদি রেখে দিই, কিন্তু form-এ `novalidate` যোগ করি, যাতে browser-এর হারিয়ে যাওয়া bubble-এর বদলে একরকম inline error দেখাতে পারি। *কী* ভুল হয়েছে তা ঠিক করতে তবুও Constraint Validation API (`input.validity`) ব্যবহার করি।
            2. **প্রতিটা field-এর error:** input-এ `aria-invalid="true"` দিই, message-টা এমন element-এ লিখি যেটা `aria-describedby` দিয়ে যুক্ত, field-এর পাশেই দৃশ্যমান রাখি, আর শুধু লাল রঙের উপর নির্ভর করি না (text আর icon দুটোই)।
            3. **Error-সহ submit হলে:** উপরে একটা error summary দেখাই ("There are 2 problems"), যেখানে প্রতিটা field-এর link থাকে, আর focus ওই summary-তে নিয়ে যাই। Screen reader user সঙ্গে সঙ্গে সমস্যাগুলো শুনতে পায়, আর সবাই সরাসরি field-এ যেতে পারে।
            4. **Server-side error** ("এই mobile number আগেই registered", "Payment declined") ঠিক একই জায়গাগুলো দিয়ে দেখাই — field message + summary — যাতে UI একরকম থাকে। User যা লিখেছে সব রেখে দিই।
            5. **সময় নির্ধারণ:** submit-এ validate করি, আর কোনো field একবার invalid হলে `blur`/`input`-এ আবার validate করি, যাতে ঠিক করামাত্র error মুছে যায় — user type করার মাঝেই চিৎকার করে error দেখাই না।
            6. **কাজের message লেখো:** "Invalid input" নয়, বরং "01 দিয়ে শুরু হওয়া 11 সংখ্যার mobile number দিন, যেমন 01712345678"।
        """,
        quick_en=r"""Add `novalidate` but keep using the Constraint Validation API; mark bad fields with `aria-invalid` and a visible message linked by `aria-describedby`; on submit, show an error summary with links and move focus to it. Server errors use the same slots, and the user's input is kept.""",
        quick_bn=r"""`novalidate` দিলেও Constraint Validation API ব্যবহার করি; ভুল field-এ `aria-invalid` আর `aria-describedby` দিয়ে যুক্ত দৃশ্যমান message দিই; submit-এ link-সহ error summary দেখিয়ে focus সেখানে নিই। Server error-ও একই জায়গায় দেখাই, আর user যা লিখেছে তা রেখে দিই।""",
        ex_en=r"""
            - **Why focus the summary instead of using a live region?** Moving focus is reliable across screen readers and also scrolls sighted users to the problem. If you can't move focus (e.g. inline async check while typing), use a live region that already exists in the DOM before you inject text — live regions added together with their content are often not announced.
            - **`aria-describedby` can list several IDs** (hint + error), read in order. An empty error element simply adds nothing.
            - **Clear state properly:** remove `aria-invalid` (or set it to `false`) and empty the message when the field becomes valid; stale errors are confusing.
            - **Links in the summary** should move focus to the input; some teams add a small script so the field's label is also scrolled into view.
            - **Mobile details:** the right `type`, `inputmode` and `autocomplete` reduce errors in the first place; on small screens, the summary keeps errors from being hidden below the virtual keyboard.
            - This pattern is used by large public-sector design systems because it tests well with real users, including screen-reader users.
        """,
        ex_bn=r"""
            - **Live region-এর বদলে কেন summary-তে focus?** Focus সরানো সব screen reader-এ নির্ভরযোগ্যভাবে কাজ করে, আর যারা দেখতে পায় তাদেরও সমস্যার জায়গায় scroll করে নিয়ে যায়। যদি focus সরানো না যায় (যেমন type করার সময় inline async check), তাহলে এমন live region ব্যবহার করো যেটা text inject করার আগেই DOM-এ আছে — content-এর সাথে একসাথে যোগ করা live region প্রায়ই announce হয় না।
            - **`aria-describedby`-তে একাধিক ID দেওয়া যায়** (hint + error), সেগুলো ক্রমানুসারে পড়া হয়। খালি error element কিছুই যোগ করে না।
            - **State ঠিকভাবে মুছে ফেলো:** field valid হলে `aria-invalid` সরিয়ে দাও (বা `false` করো) আর message খালি করো; পুরোনো error বিভ্রান্তি তৈরি করে।
            - **Summary-র link** যেন input-এ focus নিয়ে যায়; কিছু team ছোট একটা script যোগ করে, যাতে field-এর label-ও scroll হয়ে দেখা যায়।
            - **Mobile-এর খুঁটিনাটি:** সঠিক `type`, `inputmode` আর `autocomplete` শুরু থেকেই ভুল কমায়; ছোট screen-এ summary থাকলে error virtual keyboard-এর নিচে চাপা পড়ে না।
            - বড় বড় সরকারি design system এই pattern ব্যবহার করে, কারণ screen reader user-সহ আসল user-দের সাথে test করে এটা ভালো ফল দিয়েছে।
        """,
        tip_en=r"""Answer in layers: field level, form level (summary + focus), server errors, then message quality. Concrete markup like `aria-invalid` + `aria-describedby` shows you've actually built this, not just read about it.""",
        tip_bn=r"""স্তরে স্তরে উত্তর দাও: field level, form level (summary + focus), server error, তারপর message-এর মান। `aria-invalid` + `aria-describedby`-এর মতো নির্দিষ্ট markup বললে বোঝা যায় তুমি এটা সত্যিই বানিয়েছ, শুধু পড়োনি।""",
        mist_en=r"""Showing errors only in red, using a toast that disappears, validating on every keystroke from the first character, clearing the form after a server error, or injecting a `role="alert"` element together with its text and expecting it to be announced.""",
        mist_bn=r"""শুধু লাল রঙে error দেখানো, হারিয়ে যাওয়া toast ব্যবহার করা, প্রথম character থেকেই প্রতিটা keystroke-এ validate করা, server error-এর পর form খালি করে দেওয়া, অথবা text-সহ একসাথে `role="alert"` element inject করে আশা করা যে সেটা announce হবে।""",
        code=r"""
            <form id="checkout" novalidate>
              <div id="error-summary" tabindex="-1" hidden>
                <h2>There is a problem</h2>
                <ul></ul>
              </div>

              <label for="phone">Mobile number</label>
              <p id="phone-hint">11 digits, e.g. 01712345678</p>
              <input id="phone" name="phone" type="tel" inputmode="numeric" autocomplete="tel"
                     required pattern="01[3-9][0-9]{8}" aria-describedby="phone-hint phone-error">
              <p id="phone-error" class="error"></p>

              <button type="submit">Place order</button>
            </form>

            <script type="module">
              const form = document.getElementById('checkout');
              const summary = document.getElementById('error-summary');
              const messages = {
                phone: {
                  valueMissing: 'Enter your mobile number',
                  patternMismatch: 'Enter an 11-digit mobile number starting with 01, like 01712345678',
                },
              };

              function setFieldError(input, text) {
                document.getElementById(`${input.id}-error`).textContent = text;
                if (text) input.setAttribute('aria-invalid', 'true');
                else input.removeAttribute('aria-invalid');
              }

              form.addEventListener('submit', (event) => {
                const problems = [];
                for (const input of form.querySelectorAll('input[name]')) {
                  const rules = messages[input.name] ?? {};
                  const failed = Object.keys(rules).find((flag) => input.validity[flag]);
                  const text = input.validity.valid ? '' : (rules[failed] ?? input.validationMessage);
                  setFieldError(input, text);
                  if (text) problems.push({ input, text });
                }
                if (problems.length === 0) return; // valid: let it submit (or send with fetch)

                event.preventDefault();
                summary.querySelector('ul').replaceChildren(...problems.map(({ input, text }) => {
                  const li = document.createElement('li');
                  const link = document.createElement('a');
                  link.href = `#${input.id}`;
                  link.textContent = text;
                  li.append(link);
                  return li;
                }));
                summary.hidden = false;
                summary.focus();
              });
            </script>
        """,
        lang="html",
        follow=[
            ("How would you show a server-side error that arrives asynchronously after a `fetch`?", "`fetch`-এর পরে asynchronously আসা server-side error কীভাবে দেখাবে?"),
            ("When would you use `role=\"alert\"` versus `aria-live=\"polite\"`?", "কখন `role=\"alert\"` আর কখন `aria-live=\"polite\"` ব্যবহার করবে?"),
        ],
        related=["html-013", "html-005"],
        refs=[WAI_FORM_NOTIFY, MDN_ARIA_INVALID, MDN_VALIDITY],
    ),
    # ------------------------------------------------------------------ html-025
    Q(
        id="html-025", sub="Practical Scenarios", diff="hard", type="scenario",
        prio="high", market="both", mins=10,
        tags=["seo", "spa", "ssr", "open-graph", "rendering"],
        ver="Version-independent concept (applies to any client-rendered SPA)", vs=False, status="stable",
        q_en=r"""A client-side rendered React SPA (built with Vite) has poor Google indexing for its product pages, and links shared on Facebook or WhatsApp show the same generic title and image for every page. What's going wrong, and how would you fix it?""",
        q_bn=r"""একটা client-side rendered React SPA (Vite দিয়ে বানানো)-র product page-গুলো Google-এ ঠিকমতো index হচ্ছে না, আর Facebook বা WhatsApp-এ share করা link-এ প্রতিটা page-এর জন্য একই সাধারণ title আর image দেখাচ্ছে। সমস্যাটা কোথায়, আর কীভাবে ঠিক করবে?""",
        a_en=r"""
            **Root cause:** the server returns the same shell `index.html` — default `<title>`, default Open Graph tags and an empty `<div id="root">` — for every URL. All the real content and per-page tags appear only after JavaScript runs and fetches data.
            - Social crawlers (Facebook, WhatsApp, LinkedIn, X) generally **don't execute JavaScript**, so they only ever see the shell's default tags.
            - Google can render JavaScript, but rendering is deferred and resource-limited; content that depends on slow API calls, client-only routing or runtime errors can be missed. Other search engines and AI crawlers vary even more.

            **Fixes, best first:**
            1. **Server-render or pre-render** the routes — move to an SSR/SSG-capable framework (Next.js, React Router in framework mode, Astro), or pre-render product pages at build time if the catalogue is manageable. The HTML response then contains the content and the right tags.
            2. If a migration isn't possible right now: have the server or edge **inject per-route head tags** (title, description, canonical, OG, JSON-LD) into the shell based on the URL. It's a cheap, effective fix for share previews.
            3. "Dynamic rendering" (serving bots a pre-rendered snapshot) is a workaround Google itself no longer recommends — I'd treat it as temporary at best.

            **Also fix the fundamentals:** real `<a href>` links for navigation (not `onClick` + `navigate()` on a `div`), History API URLs instead of `#/` hash routes, unique titles/descriptions per route, a real **404 status** for missing products (avoid soft 404s), an XML sitemap, and don't block JS/CSS in `robots.txt`.
        """,
        a_bn=r"""
            **মূল কারণ:** server প্রতিটা URL-এর জন্য একই shell `index.html` ফেরত দেয় — default `<title>`, default Open Graph tag আর একটা খালি `<div id="root">`। আসল content আর page-ভিত্তিক tag আসে শুধু JavaScript চলে data fetch করার পরে।
            - Social crawler (Facebook, WhatsApp, LinkedIn, X) সাধারণত **JavaScript চালায় না**, তাই তারা সবসময় shell-এর default tag-ই দেখে।
            - Google JavaScript render করতে পারে, কিন্তু rendering দেরিতে হয় আর resource সীমিত; ধীর API call, শুধু client-side routing বা runtime error-এর উপর নির্ভরশীল content বাদ পড়ে যেতে পারে। অন্য search engine আর AI crawler-দের আচরণ আরও ভিন্ন।

            **সমাধান, সবচেয়ে ভালোটা আগে:**
            1. Route-গুলো **server-render বা pre-render** করো — SSR/SSG করতে পারে এমন framework-এ যাও (Next.js, framework mode-এ React Router, Astro), অথবা catalogue সামলানোর মতো হলে build-এর সময়েই product page pre-render করো। তখন HTML response-এই content আর সঠিক tag থাকে।
            2. এখনই migration সম্ভব না হলে: server বা edge থেকে URL দেখে shell-এ **route-ভিত্তিক head tag inject করো** (title, description, canonical, OG, JSON-LD)। Share preview-এর জন্য এটা সস্তা অথচ কার্যকর সমাধান।
            3. "Dynamic rendering" (bot-দের pre-render করা snapshot দেওয়া) এমন একটা workaround যেটা Google নিজেই এখন আর recommend করে না — বড়জোর সাময়িক সমাধান হিসেবে দেখব।

            **মৌলিক বিষয়গুলোও ঠিক করো:** navigation-এর জন্য আসল `<a href>` link (কোনো `div`-এ `onClick` + `navigate()` নয়), `#/` hash route-এর বদলে History API URL, প্রতিটা route-এর আলাদা title/description, না-থাকা product-এর জন্য আসল **404 status** (soft 404 এড়াও), একটা XML sitemap, আর `robots.txt`-এ JS/CSS block কোরো না।
        """,
        quick_en=r"""The server sends the same empty shell with default tags for every URL: social crawlers don't run JavaScript, and Google renders it late and unreliably. Server-render or pre-render the routes, or at least inject per-route title, OG and canonical tags at the server or edge.""",
        quick_bn=r"""Server প্রতিটা URL-এ default tag-সহ একই খালি shell পাঠায়: social crawler JavaScript চালায় না, আর Google দেরিতে ও অনির্ভরযোগ্যভাবে render করে। Route-গুলো server-render বা pre-render করো, নইলে অন্তত server বা edge-এ প্রতি route-এর title, OG আর canonical tag inject করো।""",
        ex_en=r"""
            **How to verify:** `curl` the product URL (or "View source", not DevTools Elements) — if you can't see the product name and tags in the raw HTML, crawlers that don't run JavaScript can't either. Use the platforms' own debugging tools (e.g. Google's URL Inspection, Facebook's Sharing Debugger) to see what they fetched; they also let you refresh cached previews.

            **Trade-offs:**
            - SSR adds server cost and complexity (caching, hydration errors), but also improves LCP on slow devices because content arrives in the HTML.
            - Build-time pre-rendering is cheap to host but stale for prices and stock — combine it with revalidation or client-side refresh of volatile data.
            - Head-tag injection fixes previews quickly but leaves the body empty for crawlers, so it's only a partial SEO fix.

            **Soft 404s** are a classic SPA problem: the shell returns `200 OK` for `/products/does-not-exist` and the app shows "Not found" client-side. Search engines then index error pages. The server must know which routes exist to return a real 404.
        """,
        ex_bn=r"""
            **কীভাবে যাচাই করবে:** product URL-টা `curl` করো (অথবা "View source" দেখো, DevTools Elements নয়) — raw HTML-এ product-এর নাম আর tag না দেখা গেলে, যেসব crawler JavaScript চালায় না তারাও দেখতে পায় না। Platform-গুলোর নিজস্ব debugging tool (যেমন Google-এর URL Inspection, Facebook-এর Sharing Debugger) দিয়ে দেখো তারা কী fetch করেছে; এগুলো দিয়ে cache হয়ে থাকা preview refresh-ও করা যায়।

            **Trade-off:**
            - SSR-এ server খরচ আর জটিলতা বাড়ে (caching, hydration error), তবে ধীর device-এ LCP-ও ভালো হয়, কারণ content HTML-এর সাথেই আসে।
            - Build-time pre-rendering host করা সস্তা, কিন্তু দাম আর stock-এর তথ্য পুরোনো হয়ে যায় — revalidation বা পরিবর্তনশীল data-র client-side refresh-এর সাথে মিলিয়ে ব্যবহার করো।
            - Head tag inject করলে preview দ্রুত ঠিক হয়, কিন্তু crawler-দের জন্য body খালিই থাকে, তাই SEO-র ক্ষেত্রে এটা আংশিক সমাধান।

            **Soft 404** SPA-র একটা classic সমস্যা: shell `/products/does-not-exist`-এর জন্যও `200 OK` দেয় আর app client-side-এ "Not found" দেখায়। ফলে search engine error page index করে ফেলে। আসল 404 দিতে হলে server-কে জানতে হবে কোন route-গুলো আসলে আছে।
        """,
        tip_en=r"""Separate the two audiences — social crawlers (no JS at all) and search engines (JS, but deferred and fragile) — then give options in order of effort. Ending with "I'd verify with curl / view-source" shows a practical debugging habit.""",
        tip_bn=r"""দুই ধরনের audience আলাদা করো — social crawler (একদমই JS চালায় না) আর search engine (JS চালায়, কিন্তু দেরিতে ও ভঙ্গুরভাবে) — তারপর পরিশ্রমের ক্রমে সমাধানগুলো বলো। শেষে "আমি curl / view-source দিয়ে যাচাই করব" বললে তোমার বাস্তব debugging অভ্যাস বোঝা যায়।""",
        mist_en=r"""Assuming "Google runs JavaScript, so SEO is fine", updating `document.title` client-side and expecting share previews to change, using hash routing, or returning 200 for not-found pages.""",
        mist_bn=r""""Google তো JavaScript চালায়, তাই SEO ঠিক আছে" ধরে নেওয়া, client-side-এ `document.title` বদলে share preview বদলাবে আশা করা, hash routing ব্যবহার করা, অথবা not-found page-এর জন্য 200 ফেরত দেওয়া।""",
        follow=[
            ("How would you handle prices and stock that change every few minutes on pre-rendered pages?", "Pre-render করা page-এ যে দাম আর stock কয়েক মিনিট পরপর বদলায়, সেটা কীভাবে সামলাবে?"),
            ("What's a soft 404 and how do you avoid it in an SPA?", "Soft 404 কী, আর SPA-তে কীভাবে এড়াবে?"),
        ],
        related=["html-017", "html-030"],
        refs=[WEBDEV_RENDERING, MDN_HISTORY],
    ),
]

if __name__ == "__main__":
    save("html", "b2", QUESTIONS)
