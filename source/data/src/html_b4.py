import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_IMG = ("MDN — <img> (loading attribute)", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img")
WEBDEV_LAZY = ("web.dev — Browser-level image lazy loading", "https://web.dev/articles/browser-level-image-lazy-loading")
MDN_ELEMENTS = ("MDN — HTML elements reference", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements")
MDN_A = ("MDN — <a>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a")
MDN_TEXTCONTENT = ("MDN — Node.textContent", "https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent")
MDN_INNERHTML = ("MDN — Element.innerHTML (security considerations)", "https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML")
OWASP_XSS = ("OWASP — Cross Site Scripting Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html")
MDN_PRELOAD = ("MDN — rel=preload", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preload")
MDN_PRECONNECT = ("MDN — rel=preconnect", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preconnect")
WEBDEV_OPTIMIZE_LCP = ("web.dev — Optimize Largest Contentful Paint", "https://web.dev/articles/optimize-lcp")
W3C_USING_ARIA = ("W3C — Using ARIA (first rule of ARIA use)", "https://www.w3.org/TR/using-aria/")
MDN_ARIA = ("MDN — ARIA", "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA")
MDN_REQUESTSUBMIT = ("MDN — HTMLFormElement.requestSubmit()", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/requestSubmit")
MDN_FORMSUBMIT = ("MDN — HTMLFormElement.submit()", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/submit")
SPEC_PARSING = ("HTML Standard — Parsing HTML documents (tree construction)", "https://html.spec.whatwg.org/multipage/parsing.html")
MDN_P = ("MDN — <p> (end-tag omission rules)", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/p")
WEBDEV_DOM_SIZE = ("web.dev — How large DOM sizes affect interactivity", "https://web.dev/articles/dom-size-and-interactivity")
WEBDEV_CONTENT_VISIBILITY = ("web.dev — content-visibility", "https://web.dev/articles/content-visibility")
WEBDEV_LAYOUT_THRASHING = ("web.dev — Avoid large, complex layouts and layout thrashing", "https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing")

QUESTIONS = [
    # ------------------------------------------------------------------ html-010
    Q(
        id="html-010", sub="Performance", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["lazy-loading", "images", "iframes", "performance", "lcp"],
        ver="HTML Living Standard; loading=\"lazy\" Baseline widely available", vs=False, status="stable",
        q_en=r"""What does `loading="lazy"` do on `<img>` and `<iframe>`, and when should you *not* use it?""",
        q_bn=r"""`<img>` আর `<iframe>`-এ `loading="lazy"` কী করে, আর কখন এটা ব্যবহার করা *উচিত নয়*?""",
        a_en=r"""
            `loading="lazy"` tells the browser to postpone fetching an image or iframe until it's close to the viewport. Images far down a long product list, or a YouTube/Maps embed in the footer, don't compete for bandwidth with what the user sees first — a real saving on mobile data. No JavaScript or `IntersectionObserver` is needed. The default is `loading="eager"`.

            I **don't** use it on above-the-fold images, and never on the LCP image (the hero banner or the main product photo). A lazy image is only requested after layout tells the browser it's near the viewport, so lazy-loading the hero delays LCP. For that image I do the opposite: `fetchpriority="high"`.

            I always add `width` and `height` so the browser reserves space and the page doesn't jump (CLS) when lazy images arrive.
        """,
        a_bn=r"""
            `loading="lazy"` browser-কে বলে, image বা iframe viewport-এর কাছাকাছি না আসা পর্যন্ত fetch করা পিছিয়ে রাখতে। লম্বা product list-এর অনেক নিচের ছবি, বা footer-এর YouTube/Maps embed তখন user প্রথমে যা দেখে তার সাথে bandwidth নিয়ে প্রতিযোগিতা করে না — mobile data-য় এটা সত্যিকারের সাশ্রয়। কোনো JavaScript বা `IntersectionObserver` লাগে না। Default হলো `loading="eager"`।

            Above-the-fold image-এ আমি এটা ব্যবহার **করি না**, আর LCP image-এ (hero banner বা প্রধান product photo) তো কখনোই না। Lazy image request হয় তখনই, যখন layout হওয়ার পর browser বোঝে এটা viewport-এর কাছে — তাই hero lazy-load করলে LCP দেরি হয়। ওই image-এর জন্য আমি উল্টোটা করি: `fetchpriority="high"`।

            আমি সবসময় `width` আর `height` দিই, যাতে browser জায়গা রেখে দেয় আর lazy image আসার সময় page লাফিয়ে না ওঠে (CLS)।
        """,
        quick_en=r"""`loading="lazy"` delays fetching an image or iframe until it's near the viewport, saving data on content further down. Never use it on above-the-fold or LCP images, because it delays them; give the hero `fetchpriority="high"` and always set `width`/`height`.""",
        quick_bn=r"""`loading="lazy"` image বা iframe-এর fetch পিছিয়ে দেয় যতক্ষণ না সেটা viewport-এর কাছে আসে, ফলে নিচের content-এ data বাঁচে। Above-the-fold বা LCP image-এ কখনো দিও না, কারণ তাতে সেটা দেরিতে আসে; hero-তে `fetchpriority="high"` দাও আর সবসময় `width`/`height` দাও।""",
        ex_en=r"""
            - **Distance thresholds are browser-defined** and typically larger on slow connections, so images usually finish loading before the user scrolls to them.
            - **Privacy rule:** the HTML Standard disables lazy loading when scripting is disabled, because otherwise scroll position could be tracked through image requests without JavaScript.
            - **Carousels and tabs:** hidden slides can be lazy; the first visible slide should not be.
            - **`decoding="async"`** is a separate hint that lets image decoding happen off the critical path; it doesn't change *when* the image is fetched.
            - **Third-party iframes** (video, maps, chat) are often the biggest win — some pull in megabytes of JavaScript. A "click to load" facade is even cheaper.
        """,
        ex_bn=r"""
            - **কতটা দূরত্বে load শুরু হবে তা browser ঠিক করে**, আর ধীর connection-এ এই দূরত্ব সাধারণত বেশি হয়, তাই user scroll করে পৌঁছানোর আগেই ছবি সাধারণত load হয়ে যায়।
            - **Privacy-র নিয়ম:** scripting বন্ধ থাকলে HTML Standard lazy loading বন্ধ রাখে, কারণ নইলে JavaScript ছাড়াই image request দিয়ে scroll position track করা যেত।
            - **Carousel আর tab:** লুকানো slide lazy হতে পারে; কিন্তু প্রথম দৃশ্যমান slide নয়।
            - **`decoding="async"`** আলাদা একটা hint, যা image decoding-কে critical path-এর বাইরে করতে দেয়; image *কখন* fetch হবে তা এটা বদলায় না।
            - **Third-party iframe** (video, map, chat) থেকেই প্রায়ই সবচেয়ে বড় লাভ হয় — কিছু embed কয়েক megabyte JavaScript টেনে আনে। "Click করলে load হবে" এমন facade আরও সস্তা।
        """,
        tip_en=r"""Answer "what" in one sentence, then spend most of your time on "when not" — the LCP warning is what interviewers are listening for.""",
        tip_bn=r""""কী করে" এক বাক্যে বলো, তারপর বেশিরভাগ সময় দাও "কখন নয়"-এর উপর — interviewer আসলে LCP-সংক্রান্ত সতর্কবার্তাটাই শুনতে চায়।""",
        mist_en=r"""Adding `loading="lazy"` to every image via a global component default (including the hero), and omitting `width`/`height`.""",
        mist_bn=r"""Global component default দিয়ে সব image-এ (hero-সহ) `loading="lazy"` দিয়ে দেওয়া, আর `width`/`height` বাদ দেওয়া।""",
        code=r"""
            <!-- Hero / LCP image: eager (default) and high priority -->
            <img src="/img/eid-hero-960.jpg" width="960" height="540"
                 fetchpriority="high" alt="Eid sale: up to 40% off panjabis">

            <!-- Below-the-fold product thumbnails: lazy -->
            <img src="/img/p/panjabi-navy-320.jpg" width="320" height="400"
                 loading="lazy" decoding="async" alt="Navy cotton panjabi">

            <!-- Heavy third-party embed near the footer: lazy -->
            <iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID" width="560" height="315"
                    loading="lazy" title="How to choose your panjabi size"></iframe>
        """,
        lang="html",
        follow=[
            ("How would you find out which image is your LCP element?", "কোন image তোমার LCP element, তা কীভাবে খুঁজে বের করবে?"),
            ("Why might lazy-loaded images still cause layout shift?", "Lazy-load করা image কেন তবুও layout shift ঘটাতে পারে?"),
        ],
        related=["html-018", "html-030"],
        refs=[MDN_IMG, WEBDEV_LAZY],
    ),
    # ------------------------------------------------------------------ html-011
    Q(
        id="html-011", sub="Common Mistakes", diff="easy", type="debugging",
        prio="high", market="bangladesh", mins=6,
        tags=["common-mistakes", "semantic-html", "accessibility", "code-review"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""You're reviewing this markup for a product listing page. List the problems you'd flag and show a corrected version.""",
        q_bn=r"""তুমি একটা product listing page-এর এই markup review করছ। কোন কোন সমস্যা ধরবে তা বলো এবং একটা সংশোধিত version দেখাও।""",
        code=r"""
            <div class="header">
              <div class="logo" onclick="location.href='/'"><img src="logo.png"></div>
              <div class="menu">
                <a onclick="openCart()">Cart (2)</a>
              </div>
            </div>
            <div class="content">
              <h1>Eid Collection</h1>
              <h4>New arrivals</h4>
              <a href="/p/42">
                <div class="card">
                  <img src="panjabi.jpg" alt="Navy panjabi">
                  <button onclick="addToCart(42)">Add to cart</button>
                </div>
              </a>
              <br><br><br>
              <p id="price">৳1,850</p>
              <p id="price">৳2,100</p>
            </div>
        """,
        lang="html",
        a_en=r"""
            Problems I'd flag:
            1. **Div soup:** no landmarks. Use `<header>`, `<nav>` and `<main>` so screen-reader users can jump around.
            2. **Clickable `<div>` logo:** not focusable, not announced as a link, and the image has no `alt`. Use `<a href="/"><img alt="Dokan — home"></a>`.
            3. **`<a>` without `href`:** it isn't focusable or announced as a link. Opening a cart drawer is an action, so it should be a `<button type="button">` (or a real link to `/cart`).
            4. **Skipped heading level:** `<h4>` chosen because it "looks smaller". Use `<h2>` and style it with CSS.
            5. **Button inside a link:** interactive content can't be nested inside `<a>`. Clicking the button also triggers the link, and assistive tech gets confused. Put the link on the product title and keep the button separate.
            6. **`<br>` for spacing:** layout belongs in CSS (`margin`/`gap`).
            7. **Duplicate `id="price"`:** IDs must be unique; `getElementById`, `<label for>` and ARIA references break. Use a class.
        """,
        a_bn=r"""
            যে সমস্যাগুলো ধরব:
            1. **Div soup:** কোনো landmark নেই। `<header>`, `<nav>` আর `<main>` ব্যবহার করো, যাতে screen reader user এক অংশ থেকে আরেক অংশে লাফ দিতে পারে।
            2. **Click করা যায় এমন `<div>` logo:** focus করা যায় না, link হিসেবে ঘোষিত হয় না, আর image-এ `alt` নেই। `<a href="/"><img alt="Dokan — home"></a>` ব্যবহার করো।
            3. **`href` ছাড়া `<a>`:** এটা focusable নয়, link হিসেবেও ঘোষিত হয় না। Cart drawer খোলা একটা action, তাই এটা `<button type="button">` হওয়া উচিত (অথবা `/cart`-এ আসল link)।
            4. **Heading level লাফানো:** "ছোট দেখায়" বলে `<h4>` বেছে নেওয়া হয়েছে। `<h2>` ব্যবহার করে CSS দিয়ে style করো।
            5. **Link-এর ভেতরে button:** `<a>`-এর ভেতরে interactive content nest করা যায় না। Button-এ click করলে link-ও trigger হয়, আর assistive tech বিভ্রান্ত হয়। Link-টা product title-এ রাখো, আর button আলাদা রাখো।
            6. **Spacing-এর জন্য `<br>`:** layout-এর জায়গা CSS (`margin`/`gap`)।
            7. **Duplicate `id="price"`:** ID অবশ্যই unique হতে হবে; নইলে `getElementById`, `<label for>` আর ARIA reference ভেঙে যায়। Class ব্যবহার করো।
        """,
        quick_en=r"""It's div soup with fake controls: no landmarks, a clickable `<div>` logo without `alt`, an `<a>` without `href`, a skipped heading level, a button inside a link, `<br>` for spacing and duplicate `id`s. Fix it with landmarks, real `<a href>`/`<button>`, `<h2>`, CSS spacing and classes.""",
        quick_bn=r"""এটা নকল control-ভরা div soup: landmark নেই, `alt` ছাড়া clickable `<div>` logo, `href` ছাড়া `<a>`, heading level লাফানো, link-এর ভেতরে button, spacing-এর জন্য `<br>`, আর duplicate `id`। Landmark, আসল `<a href>`/`<button>`, `<h2>`, CSS spacing আর class দিয়ে ঠিক করো।""",
        ex_en=r"""
            Why these matter in practice:
            - Keyboard users can't reach the logo or the cart at all — they literally can't check out if the cart is only reachable through that `<a>` without `href`.
            - A `<div>` inside `<a>` is actually allowed (links have a transparent content model); the problem is specifically the nested **interactive** element.
            - Heading levels form the outline screen-reader users navigate by; skipping from `h1` to `h4` suggests missing sections.
            - Duplicate IDs are a frequent bug in component-based apps when a card renders many times — generate unique IDs (e.g. `useId()` in React) or avoid IDs.
            - Automated tools (axe DevTools, Lighthouse accessibility audit, the HTML validator) catch most of these in seconds; add one to CI.
        """,
        ex_bn=r"""
            বাস্তবে এগুলো কেন গুরুত্বপূর্ণ:
            - Keyboard user logo বা cart-এ পৌঁছাতেই পারে না — cart যদি শুধু ওই `href`-ছাড়া `<a>` দিয়েই খোলা যায়, তাহলে তারা আক্ষরিক অর্থেই checkout করতে পারবে না।
            - `<a>`-এর ভেতরে `<div>` আসলে অনুমোদিত (link-এর content model transparent); সমস্যাটা নির্দিষ্টভাবে nested **interactive** element-এ।
            - Heading level দিয়ে যে outline তৈরি হয়, screen reader user সেটা ধরেই navigate করে; `h1` থেকে সরাসরি `h4`-এ গেলে মনে হয় মাঝের section হারিয়ে গেছে।
            - Component-ভিত্তিক app-এ একটা card বহুবার render হলে duplicate ID খুব সাধারণ bug — unique ID তৈরি করো (যেমন React-এ `useId()`) বা ID এড়িয়ে চলো।
            - Automated tool (axe DevTools, Lighthouse accessibility audit, HTML validator) কয়েক সেকেন্ডেই এর বেশিরভাগ ধরে ফেলে; CI-তে একটা যোগ করো।
        """,
        tip_en=r"""In a code-review question, number your findings and give each one a one-line *impact* ("keyboard users can't reach the cart"). Impact-first comments sound like a senior reviewer.""",
        tip_bn=r"""Code review প্রশ্নে তোমার পাওয়া সমস্যাগুলো নম্বর দিয়ে বলো, আর প্রতিটার এক লাইনের *প্রভাব* দাও ("keyboard user cart-এ পৌঁছাতে পারে না")। প্রভাব দিয়ে শুরু করা comment শুনতে একজন senior reviewer-এর মতো লাগে।""",
        mist_en=r"""Fixing only what's visible (spacing), adding `role="button"` and `tabindex="0"` to the `<div>` instead of using a native element, or keeping the `<h4>` "because the design says so".""",
        mist_bn=r"""শুধু চোখে পড়া জিনিস (spacing) ঠিক করা, native element ব্যবহার না করে `<div>`-এ `role="button"` আর `tabindex="0"` যোগ করা, অথবা "design-এ এমনই আছে" বলে `<h4>` রেখে দেওয়া।""",
        extra=[dict(
            lang="html",
            src=r"""
                <header class="header">
                  <a href="/" class="logo"><img src="logo.png" alt="Dokan — home"></a>
                  <nav aria-label="Main">
                    <button type="button" class="cart-toggle">Cart (2)</button>
                  </nav>
                </header>
                <main class="content">
                  <h1>Eid Collection</h1>
                  <h2>New arrivals</h2>
                  <article class="card">
                    <img src="panjabi.jpg" alt="Navy panjabi">
                    <h3><a href="/p/42">Cotton Panjabi — Navy</a></h3>
                    <p class="price">৳1,850</p>
                    <button type="button" data-product-id="42">Add to cart</button>
                  </article>
                </main>
            """,
            label_en="Fixed version (spacing moved to CSS, handlers attached with addEventListener)",
            label_bn="সংশোধিত version (spacing CSS-এ, handler addEventListener দিয়ে যুক্ত)",
        )],
        follow=[
            ("How would you make the whole card clickable without nesting the button inside the link?", "Button-কে link-এর ভেতরে না রেখে পুরো card-টা কীভাবে clickable করবে?"),
            ("Which of these issues can automated tools detect, and which need manual testing?", "এর মধ্যে কোন সমস্যাগুলো automated tool ধরতে পারে, আর কোনগুলোর জন্য manual testing লাগে?"),
        ],
        related=["html-001", "html-003"],
        refs=[MDN_ELEMENTS, MDN_A],
    ),
    # ------------------------------------------------------------------ html-020
    Q(
        id="html-020", sub="Security", diff="medium", type="debugging",
        prio="high", market="both", mins=7,
        tags=["xss", "innerhtml", "textcontent", "security", "dom"],
        ver="Version-independent concept (DOM APIs)", vs=False, status="stable",
        q_en=r"""This search page shows "Results for …" and a list of matching products. A tester reports that opening `/search?q=<img src=x onerror=alert(document.cookie)>` runs the script. Find every problem in this code and fix it.""",
        q_bn=r"""এই search page "Results for …" আর মিলে যাওয়া product-এর একটা list দেখায়। একজন tester জানিয়েছে, `/search?q=<img src=x onerror=alert(document.cookie)>` খুললে script চলে যায়। এই code-এর সব সমস্যা খুঁজে বের করো এবং ঠিক করো।""",
        code=r"""
            <h1 id="title"></h1>
            <ul id="results"></ul>

            <script type="module">
              const q = new URLSearchParams(location.search).get('q') ?? '';
              document.getElementById('title').innerHTML = `Results for "${q}"`;

              const res = await fetch(`/api/search?q=${q}`);
              const items = await res.json();

              document.getElementById('results').innerHTML = items
                .map((item) => `<li><a href="${item.url}">${item.name}</a></li>`)
                .join('');
            </script>
        """,
        lang="html",
        a_en=r"""
            Three problems:
            1. **Reflected DOM XSS:** `q` comes straight from the URL and is written with `innerHTML`, so it's parsed as HTML. `<script>` tags inserted via `innerHTML` don't run, but **event-handler attributes do** — that's why `<img src=x onerror=…>` is the classic payload. Fix: `textContent`.
            2. **Stored XSS through API data:** product `name` (often user- or seller-generated) and `url` are interpolated into an HTML string. A name like `<img onerror=…>` or a `url` of `javascript:…` would execute. Fix: build elements with `createElement` + `textContent`, and only allow `http:`/`https:` URLs in `href`.
            3. **Unencoded query string:** `?q=${q}` breaks on `&`, `#` or `+` and lets users inject extra parameters. Fix: `new URLSearchParams({ q })`.
        """,
        a_bn=r"""
            তিনটা সমস্যা:
            1. **Reflected DOM XSS:** `q` সরাসরি URL থেকে আসছে আর `innerHTML` দিয়ে লেখা হচ্ছে, ফলে এটা HTML হিসেবে parse হয়। `innerHTML` দিয়ে বসানো `<script>` tag চলে না, কিন্তু **event-handler attribute চলে** — এজন্যই `<img src=x onerror=…>` classic payload। সমাধান: `textContent`।
            2. **API data দিয়ে stored XSS:** product-এর `name` (প্রায়ই user বা seller-এর লেখা) আর `url` একটা HTML string-এ বসানো হচ্ছে। `<img onerror=…>`-এর মতো নাম বা `javascript:…` url থাকলে সেটা execute হবে। সমাধান: `createElement` + `textContent` দিয়ে element বানাও, আর `href`-এ শুধু `http:`/`https:` URL অনুমোদন করো।
            3. **Encode না করা query string:** `?q=${q}` `&`, `#` বা `+` পেলে ভেঙে যায়, আর user বাড়তি parameter ঢুকিয়ে দিতে পারে। সমাধান: `new URLSearchParams({ q })`।
        """,
        quick_en=r"""The URL's `q` and the API's `name`/`url` go into `innerHTML`, so `onerror` handlers run (reflected and stored XSS), and `q` isn't encoded in the fetch URL. Fix: `textContent` and `createElement`, only `http:`/`https:` links, and `URLSearchParams` for the query.""",
        quick_bn=r"""URL-এর `q` আর API-র `name`/`url` সরাসরি `innerHTML`-এ যায়, তাই `onerror` handler চলে (reflected আর stored XSS), আর fetch URL-এ `q` encode করা হয় না। সমাধান: `textContent` আর `createElement`, শুধু `http:`/`https:` link, আর query-র জন্য `URLSearchParams`।""",
        ex_en=r"""
            - **Rule of thumb:** data goes into the DOM as *text* (`textContent`, `setAttribute` on safe attributes, `createElement`), never as *markup*. If you truly need user-provided HTML (rich-text descriptions), sanitize it with a maintained library like DOMPurify.
            - **`href` is a special sink:** `textContent` escaping doesn't help if the attribute value itself is `javascript:alert(1)`. Validate the protocol with the `URL` parser.
            - **Server-side escaping isn't enough here** — this is DOM-based XSS: the payload never needs to touch the server's HTML templates.
            - **Defence in depth:** a strict Content Security Policy blocks inline handlers like `onerror`, and Trusted Types make `innerHTML = string` throw. Frameworks such as React escape text by default, but `dangerouslySetInnerHTML` and URL props are still your responsibility.
        """,
        ex_bn=r"""
            - **সহজ নিয়ম:** data DOM-এ যাবে *text* হিসেবে (`textContent`, নিরাপদ attribute-এ `setAttribute`, `createElement`), কখনো *markup* হিসেবে নয়। User-এর দেওয়া HTML সত্যিই দরকার হলে (rich-text description), DOMPurify-এর মতো maintain করা library দিয়ে sanitize করো।
            - **`href` একটা বিশেষ sink:** attribute-এর value নিজেই যদি `javascript:alert(1)` হয়, তাহলে `textContent`-এর escaping কোনো কাজে আসে না। `URL` parser দিয়ে protocol যাচাই করো।
            - **এখানে server-side escaping যথেষ্ট নয়** — এটা DOM-based XSS: payload-কে server-এর HTML template ছুঁয়ে যেতেই হয় না।
            - **বাড়তি সুরক্ষা স্তর:** strict Content Security Policy `onerror`-এর মতো inline handler আটকে দেয়, আর Trusted Types থাকলে `innerHTML = string` সরাসরি error throw করে। React-এর মতো framework default-ভাবে text escape করে, কিন্তু `dangerouslySetInnerHTML` আর URL prop-এর দায়িত্ব তবুও তোমার।
        """,
        tip_en=r"""Don't stop at the obvious `innerHTML` line — interviewers often plant a second sink (the `href`) and a non-security bug (encoding) to see how thorough you are.""",
        tip_bn=r"""শুধু চোখে পড়া `innerHTML` line-এ থেমে যেও না — interviewer প্রায়ই দ্বিতীয় একটা sink (`href`) আর security-র বাইরের একটা bug (encoding) রেখে দেয়, তুমি কতটা খুঁটিয়ে দেখো তা যাচাই করতে।""",
        mist_en=r"""Escaping only `<script>` with a regex, assuming "`<script>` via `innerHTML` doesn't run, so we're safe", or forgetting `javascript:` URLs.""",
        mist_bn=r"""Regex দিয়ে শুধু `<script>` escape করা, "`innerHTML` দিয়ে `<script>` চলে না, তাই আমরা নিরাপদ" ভেবে নেওয়া, অথবা `javascript:` URL-এর কথা ভুলে যাওয়া।""",
        extra=[dict(
            lang="javascript",
            src=r"""
                const q = new URLSearchParams(location.search).get('q') ?? '';
                document.getElementById('title').textContent = `Results for "${q}"`;

                const res = await fetch(`/api/search?${new URLSearchParams({ q })}`);
                const items = await res.json();

                function safeHref(raw) {
                  try {
                    const url = new URL(raw, location.origin);
                    return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : '#';
                  } catch {
                    return '#';
                  }
                }

                document.getElementById('results').replaceChildren(
                  ...items.map((item) => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.href = safeHref(item.url);
                    a.textContent = item.name;
                    li.append(a);
                    return li;
                  }),
                );
            """,
            label_en="Fixed script (same module)",
            label_bn="সংশোধিত script (একই module)",
        )],
        follow=[
            ("Why does `<img onerror>` execute through `innerHTML` while `<script>` doesn't?", "`innerHTML` দিয়ে `<script>` না চললেও `<img onerror>` কেন execute হয়?"),
            ("Where else in a typical frontend can XSS sinks hide?", "একটা সাধারণ frontend-এ আর কোথায় XSS sink লুকিয়ে থাকতে পারে?"),
        ],
        related=["html-027", "html-019"],
        refs=[MDN_INNERHTML, MDN_TEXTCONTENT, OWASP_XSS],
    ),
    # ------------------------------------------------------------------ html-021
    Q(
        id="html-021", sub="Performance", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["preload", "preconnect", "resource-hints", "lcp", "fetchpriority"],
        ver="HTML Living Standard; fetchpriority Baseline newly available (Oct 2024)", vs=True, status="stable",
        q_en=r"""The LCP element is a hero banner set in `main.css`: `.hero { background-image: url(https://img.dokan-cdn.example/eid-hero.avif) }`. DevTools shows the image request starting only after `main.css` has downloaded and been parsed. Which single change most directly fixes the late discovery?""",
        q_bn=r"""LCP element হলো `main.css`-এ দেওয়া একটা hero banner: `.hero { background-image: url(https://img.dokan-cdn.example/eid-hero.avif) }`। DevTools-এ দেখা যাচ্ছে `main.css` download আর parse হওয়ার পরেই image request শুরু হচ্ছে। দেরিতে খুঁজে পাওয়ার সমস্যাটা সবচেয়ে সরাসরি কোন একটা পরিবর্তনে ঠিক হবে?""",
        options=[
            (r"""`<link rel="preconnect" href="https://img.dokan-cdn.example">`""", r"""`<link rel="preconnect" href="https://img.dokan-cdn.example">`"""),
            (r"""`<link rel="preload" as="image" type="image/avif" href="https://img.dokan-cdn.example/eid-hero.avif" fetchpriority="high">`""",
             r"""`<link rel="preload" as="image" type="image/avif" href="https://img.dokan-cdn.example/eid-hero.avif" fetchpriority="high">`"""),
            (r"""`<link rel="prefetch" href="https://img.dokan-cdn.example/eid-hero.avif">`""", r"""`<link rel="prefetch" href="https://img.dokan-cdn.example/eid-hero.avif">`"""),
            (r"""`<link rel="dns-prefetch" href="https://img.dokan-cdn.example">`""", r"""`<link rel="dns-prefetch" href="https://img.dokan-cdn.example">`"""),
        ],
        correct=1,
        a_en=r"""
            `rel="preload"` with `as="image"`. It puts the image URL in the HTML where the preload scanner sees it immediately, so the fetch starts in parallel with `main.css` instead of after it. `fetchpriority="high"` raises its priority, and `type="image/avif"` lets browsers without AVIF support skip it.
        """,
        a_bn=r"""
            `as="image"`-সহ `rel="preload"`। এটা image-এর URL HTML-এ রাখে, যেখানে preload scanner সঙ্গে সঙ্গে দেখতে পায়; ফলে fetch `main.css`-এর পরে নয়, তার সাথে সমান্তরালে শুরু হয়। `fetchpriority="high"` এর priority বাড়ায়, আর `type="image/avif"` থাকলে যে browser AVIF support করে না সে এটা বাদ দেয়।
        """,
        quick_en=r"""`<link rel="preload" as="image" type="image/avif" … fetchpriority="high">`. It puts the CSS background's URL into the HTML, so the preload scanner starts the fetch in parallel with `main.css`; preconnect only warms the connection and still waits for the CSS.""",
        quick_bn=r"""`<link rel="preload" as="image" type="image/avif" … fetchpriority="high">`। এটা CSS background-এর URL HTML-এ নিয়ে আসে, তাই preload scanner `main.css`-এর সাথে parallel-এ fetch শুরু করে; preconnect শুধু connection আগে খোলে, ছবির জন্য তবু CSS-এর অপেক্ষা করতে হয়।""",
        ex_en=r"""
            The tempting wrong answer is **preconnect**: it does help — DNS, TCP and TLS to the CDN happen early — but the browser still doesn't know *which* image to request until the CSS is parsed. Preconnect saves a connection setup; preload removes the discovery delay. (A cross-origin preload opens the connection anyway, so preconnect adds little here; it's most useful when you know the origin but not the exact URL.)

            - `prefetch` is a low-priority hint for resources needed by a *future* navigation — the opposite of what we want.
            - `dns-prefetch` only resolves DNS.
            - Preload pitfalls: `as` must match how the resource is used (otherwise it's fetched twice), fonts need `crossorigin`, responsive images need `imagesrcset`/`imagesizes`, and unused preloads waste bandwidth (browsers warn in the console).
            - The best long-term fix is often to make the hero a real `<img fetchpriority="high">` in the HTML — then no hint is needed at all.
        """,
        ex_bn=r"""
            প্রলোভনজনক ভুল উত্তর **preconnect**: এটা সাহায্য করে ঠিকই — CDN-এর সাথে DNS, TCP আর TLS আগেভাগে হয়ে যায় — কিন্তু CSS parse না হওয়া পর্যন্ত browser জানেই না *কোন* image request করতে হবে। Preconnect connection setup-এর সময় বাঁচায়; preload খুঁজে পাওয়ার দেরিটাই দূর করে। (Cross-origin preload নিজেই connection খোলে, তাই এখানে preconnect বাড়তি তেমন কিছু দেয় না; যখন origin জানা কিন্তু সঠিক URL জানা নেই, তখনই এটা সবচেয়ে কাজের।)

            - `prefetch` হলো *ভবিষ্যতের* navigation-এ লাগবে এমন resource-এর জন্য কম-priority hint — আমরা যা চাই তার উল্টো।
            - `dns-prefetch` শুধু DNS resolve করে।
            - Preload-এর ফাঁদ: resource যেভাবে ব্যবহার হবে `as` সেভাবেই হতে হবে (নইলে দুবার fetch হয়), font-এর জন্য `crossorigin` লাগে, responsive image-এর জন্য `imagesrcset`/`imagesizes` লাগে, আর ব্যবহার না হওয়া preload bandwidth নষ্ট করে (browser console-এ warning দেয়)।
            - দীর্ঘমেয়াদে সবচেয়ে ভালো সমাধান প্রায়ই hero-কে HTML-এ আসল `<img fetchpriority="high">` বানানো — তখন কোনো hint-ই লাগে না।
        """,
        tip_en=r"""Distinguish the hints by what they skip: dns-prefetch skips DNS, preconnect skips the handshake, preload skips discovery, prefetch is for the next page. That one-liner answers most resource-hint questions.""",
        tip_bn=r"""Hint-গুলোকে আলাদা করো তারা কোন ধাপ এড়ায় তা দিয়ে: dns-prefetch DNS এড়ায়, preconnect handshake এড়ায়, preload খুঁজে পাওয়ার দেরি এড়ায়, prefetch পরের page-এর জন্য। এই এক লাইন দিয়েই resource hint-এর বেশিরভাগ প্রশ্নের উত্তর হয়ে যায়।""",
        refs=[MDN_PRELOAD, MDN_PRECONNECT, WEBDEV_OPTIMIZE_LCP],
    ),
    # ------------------------------------------------------------------ html-022
    Q(
        id="html-022", sub="Accessibility", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["aria", "first-rule-of-aria", "accessibility", "semantics"],
        ver="WAI-ARIA 1.2 (version-independent)", vs=False, status="stable",
        q_en=r"""What is the "first rule of ARIA"? When is ARIA the right tool, and what goes wrong when it's misused?""",
        q_bn=r""""ARIA-র প্রথম নিয়ম" কী? কখন ARIA সঠিক tool, আর ভুলভাবে ব্যবহার করলে কী সমস্যা হয়?""",
        a_en=r"""
            The first rule of ARIA: **if a native HTML element or attribute already has the semantics and behaviour you need, use it** instead of repurposing another element and adding ARIA.

            The reason is that ARIA only changes what assistive technology is *told* — it adds **no behaviour**. `role="button"` on a `<div>` makes a screen reader say "button", but the div still isn't focusable and doesn't respond to Enter or Space. With `<button>` you get all of that for free.

            ARIA is the right tool for things HTML can't express:
            - **States:** `aria-expanded` on a disclosure button, `aria-current="page"` in navigation, `aria-pressed` on a toggle, `aria-invalid` on a field with an error.
            - **Relationships:** `aria-describedby` (hints and errors), `aria-controls`, `aria-labelledby`.
            - **Live updates:** `role="status"` / `aria-live` for "Added to cart".
            - **Custom widgets HTML doesn't have:** tabs, tree views, comboboxes — and then you must implement the full keyboard pattern too.
        """,
        a_bn=r"""
            ARIA-র প্রথম নিয়ম: **যে native HTML element বা attribute-এ তোমার দরকারি semantics আর behaviour আগে থেকেই আছে, সেটাই ব্যবহার করো** — অন্য কোনো element-কে ভিন্ন কাজে লাগিয়ে ARIA যোগ কোরো না।

            কারণ ARIA শুধু বদলায় assistive technology-কে কী *বলা* হবে — এটা কোনো **behaviour যোগ করে না**। `<div>`-এ `role="button"` দিলে screen reader "button" বলবে, কিন্তু div-টা তখনো focusable নয়, Enter বা Space-এও সাড়া দেয় না। `<button>` ব্যবহার করলে এসব ফ্রিতেই পাও।

            যেখানে HTML প্রকাশ করতে পারে না, সেখানে ARIA সঠিক tool:
            - **State:** disclosure button-এ `aria-expanded`, navigation-এ `aria-current="page"`, toggle-এ `aria-pressed`, error থাকা field-এ `aria-invalid`।
            - **সম্পর্ক:** `aria-describedby` (hint আর error), `aria-controls`, `aria-labelledby`।
            - **Live update:** "Added to cart"-এর জন্য `role="status"` / `aria-live`।
            - **HTML-এ নেই এমন custom widget:** tab, tree view, combobox — আর তখন পুরো keyboard pattern-ও তোমাকে implement করতে হবে।
        """,
        quick_en=r"""If a native element already has the semantics and behaviour you need, use it instead of ARIA, because ARIA only changes what assistive tech is told and adds no behaviour. ARIA is for states, relationships, live updates and custom widgets HTML doesn't have.""",
        quick_bn=r"""যে native element-এ দরকারি semantics আর behaviour আগে থেকেই আছে, ARIA-র বদলে সেটাই ব্যবহার করো, কারণ ARIA শুধু assistive tech-কে কী বলা হবে সেটা বদলায়, কোনো behaviour যোগ করে না। ARIA দরকার state, relationship, live update আর HTML-এ নেই এমন custom widget-এর জন্য।""",
        ex_en=r"""
            Common misuse and its effect:
            - **`aria-hidden="true"` on something focusable** — keyboard users land on an element the screen reader says nothing about.
            - **`aria-label` on a plain `<div>` or `<span>`** — the generic role doesn't support naming, so it's ignored or announced inconsistently.
            - **Overriding native roles** (`<button role="link">`, `<h2 role="button">`) — you lose the original semantics and must re-implement behaviour.
            - **Application roles on websites** — `role="menu"` for a site navigation bar makes screen readers expect desktop-app menu keyboard behaviour (arrow keys) that isn't there.
            - **Stale states** — `aria-expanded="false"` that never updates is worse than no attribute: it actively lies.

            "No ARIA is better than bad ARIA" — an incorrect role or state can make a component less accessible than plain HTML. Always test with a keyboard and at least one screen reader.
        """,
        ex_bn=r"""
            সাধারণ ভুল ব্যবহার আর তার ফল:
            - **Focus করা যায় এমন element-এ `aria-hidden="true"`** — keyboard user এমন element-এ পৌঁছায় যার সম্পর্কে screen reader কিছুই বলে না।
            - **সাধারণ `<div>` বা `<span>`-এ `aria-label`** — generic role নাম দেওয়া support করে না, তাই এটা উপেক্ষিত হয় বা অসামঞ্জস্যভাবে পড়া হয়।
            - **Native role override করা** (`<button role="link">`, `<h2 role="button">`) — আসল semantics হারিয়ে যায়, behaviour আবার নিজে বানাতে হয়।
            - **Website-এ application role** — site navigation bar-এ `role="menu"` দিলে screen reader desktop app-এর menu-র মতো keyboard আচরণ (arrow key) আশা করে, যা আসলে নেই।
            - **পুরোনো state** — যে `aria-expanded="false"` কখনো আপডেট হয় না, তা attribute না থাকার চেয়েও খারাপ: এটা সক্রিয়ভাবে ভুল তথ্য দেয়।

            "খারাপ ARIA-র চেয়ে ARIA না থাকাই ভালো" — ভুল role বা state একটা component-কে সাধারণ HTML-এর চেয়েও কম accessible করে দিতে পারে। সবসময় keyboard আর অন্তত একটা screen reader দিয়ে test করো।
        """,
        tip_en=r"""Say the rule, then the key insight — "ARIA changes semantics, not behaviour" — and give one example of good ARIA (`aria-expanded`) and one of harmful ARIA. Balanced answers beat "ARIA is bad".""",
        tip_bn=r"""নিয়মটা বলো, তারপর মূল অন্তর্দৃষ্টি — "ARIA semantics বদলায়, behaviour নয়" — আর ভালো ARIA-র একটা উদাহরণ (`aria-expanded`) ও ক্ষতিকর ARIA-র একটা উদাহরণ দাও। "ARIA খারাপ" বলার চেয়ে ভারসাম্যপূর্ণ উত্তর অনেক ভালো।""",
        mist_en=r"""Thinking `role="button"` makes an element keyboard-accessible, sprinkling `aria-label` everywhere, or using ARIA to "fix" problems that a native element would avoid.""",
        mist_bn=r"""`role="button"` দিলেই element keyboard-accessible হয়ে যায় ভাবা, সব জায়গায় `aria-label` ছিটিয়ে দেওয়া, অথবা native element ব্যবহার করলে যে সমস্যা হতোই না, তা ARIA দিয়ে "ঠিক" করার চেষ্টা করা।""",
        code=r"""
            <!-- Bad: ARIA without behaviour (not focusable, no Enter/Space) -->
            <div role="button" aria-label="Show filters" onclick="toggleFilters()">Filters</div>

            <!-- Good: native button + one state HTML can't express -->
            <button type="button" aria-expanded="false" aria-controls="filters">Filters</button>
            <div id="filters" hidden><!-- filter controls --></div>

            <script type="module">
              const button = document.querySelector('[aria-controls="filters"]');
              const panel = document.getElementById('filters');

              button.addEventListener('click', () => {
                const open = button.getAttribute('aria-expanded') === 'true';
                button.setAttribute('aria-expanded', String(!open));
                panel.hidden = open;
              });
            </script>
        """,
        lang="html",
        follow=[
            ("How would you announce 'Added to cart' without moving focus?", "Focus না সরিয়ে 'Added to cart' কীভাবে ঘোষণা করবে?"),
            ("Could `<details>`/`<summary>` replace the disclosure example? What would you gain or lose?", "Disclosure উদাহরণটা কি `<details>`/`<summary>` দিয়ে বদলানো যেত? তাতে কী লাভ বা ক্ষতি হতো?"),
        ],
        related=["html-026", "html-031", "html-003"],
        refs=[W3C_USING_ARIA, MDN_ARIA],
    ),
    # ------------------------------------------------------------------ html-028
    Q(
        id="html-028", sub="Forms and Validation", diff="hard", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["forms", "requestsubmit", "submit-event", "constraint-validation"],
        ver="HTML Living Standard; requestSubmit() supported in all modern browsers", vs=False, status="stable",
        q_en=r"""Clicking "Save" works: the field is validated and the data is sent with `fetch`. But when the user presses Ctrl+S (or Cmd+S) with an empty Name field, there's no validation message and no toast — the browser does a full page navigation to the current URL with `?name=` appended. Why?""",
        q_bn=r""""Save"-এ click করলে সব ঠিক চলে: field validate হয় আর `fetch` দিয়ে data যায়। কিন্তু Name field খালি রেখে user Ctrl+S (বা Cmd+S) চাপলে কোনো validation message বা toast দেখায় না — browser বর্তমান URL-এর শেষে `?name=` জুড়ে পুরো page navigate করে। কেন?""",
        code=r"""
            <form id="profile">
              <label for="name">Name</label>
              <input id="name" name="name" required>
              <button type="submit">Save</button>
            </form>

            <script type="module">
              const form = document.getElementById('profile');

              form.addEventListener('submit', async (event) => {
                event.preventDefault();
                await fetch('/api/profile', { method: 'POST', body: new FormData(form) });
                showToast('Saved');
              });

              document.addEventListener('keydown', (event) => {
                if ((event.ctrlKey || event.metaKey) && event.key === 's') {
                  event.preventDefault();
                  form.submit();
                }
              });
            </script>
        """,
        lang="html",
        options=[
            ("`form.submit()` skips constraint validation and doesn't fire the `submit` event, so the fetch handler never runs; use `form.requestSubmit()`.",
             "`form.submit()` constraint validation এড়িয়ে যায় আর `submit` event fire করে না, তাই fetch handler কখনো চলে না; `form.requestSubmit()` ব্যবহার করো।"),
            ("The `keydown` handler's `preventDefault()` also cancels the form's `submit` listener; it should be called after `form.submit()`.",
             "`keydown` handler-এর `preventDefault()` form-এর `submit` listener-কেও বাতিল করে দেয়; এটা `form.submit()`-এর পরে call করা উচিত।"),
            ("`submit` listeners only run for pointer clicks on a submit button; keyboard-initiated submissions need a separate `keydown` handler on the form.",
             "`submit` listener শুধু submit button-এ pointer click হলেই চলে; keyboard দিয়ে শুরু হওয়া submission-এর জন্য form-এ আলাদা `keydown` handler লাগে।"),
            ("Async `submit` handlers are ignored for programmatic submissions, so the handler must be synchronous.",
             "Programmatic submission-এর ক্ষেত্রে async `submit` handler উপেক্ষিত হয়, তাই handler-কে synchronous হতে হবে।"),
        ],
        correct=0,
        a_en=r"""
            `form.submit()` is a low-level "just send it" call: it **doesn't run constraint validation** and **doesn't dispatch the `submit` event**. So the `required` check is skipped, the `fetch` handler never runs, and the browser performs a normal form submission — with no `method`/`action`, that's a GET to the current URL. `form.requestSubmit()` behaves like clicking a submit button: validation, the `submit` event, then submission only if not prevented.
        """,
        a_bn=r"""
            `form.submit()` হলো low-level "শুধু পাঠিয়ে দাও" ধরনের call: এটা **constraint validation চালায় না** এবং **`submit` event dispatch করে না**। তাই `required` check বাদ পড়ে, `fetch` handler কখনো চলে না, আর browser সাধারণ form submission করে — `method`/`action` না থাকায় সেটা বর্তমান URL-এ একটা GET। `form.requestSubmit()` submit button-এ click করার মতো আচরণ করে: validation, `submit` event, তারপর prevent না করা হলেই কেবল submission।
        """,
        quick_en=r"""`form.submit()` skips constraint validation and doesn't fire the `submit` event, so the `fetch` handler never runs and the browser does a normal GET submission. Use `form.requestSubmit()`, which behaves like clicking the submit button.""",
        quick_bn=r"""`form.submit()` constraint validation বাদ দেয় আর `submit` event fire করে না, তাই `fetch` handler চলেই না, browser একটা সাধারণ GET submission করে ফেলে। `form.requestSubmit()` ব্যবহার করো, এটা submit button click করার মতোই কাজ করে।""",
        ex_en=r"""
            The tempting option is C, because it *feels* like keyboard vs mouse is the difference — but the real difference is which API triggers the submission. Pressing Enter in a text field (implicit submission) also goes through validation and the `submit` event, just like a click.

            More details:
            - `requestSubmit(submitter)` accepts an optional submit button; then `event.submitter` is set and that button's `formaction`, `formmethod` and `formnovalidate` apply. Without an argument, `event.submitter` is `null`.
            - Option B is wrong: `preventDefault()` on the `keydown` only stops the browser's "Save page" dialog; it has nothing to do with the form.
            - `submit()` still has legitimate uses — e.g. after you've already validated and want to submit without re-triggering your own handler — but for "act like the user pressed Save", use `requestSubmit()`.
        """,
        ex_bn=r"""
            প্রলোভনজনক option C, কারণ মনে *হয়* পার্থক্যটা keyboard বনাম mouse-এ — কিন্তু আসল পার্থক্য হলো কোন API submission শুরু করছে। Text field-এ Enter চাপলে (implicit submission) সেটাও click-এর মতোই validation আর `submit` event-এর ভেতর দিয়ে যায়।

            আরও কিছু কথা:
            - `requestSubmit(submitter)` চাইলে একটা submit button নিতে পারে; তখন `event.submitter` set হয়, আর ওই button-এর `formaction`, `formmethod`, `formnovalidate` প্রযোজ্য হয়। Argument না দিলে `event.submitter` হয় `null`।
            - Option B ভুল: `keydown`-এ `preventDefault()` শুধু browser-এর "Save page" dialog আটকায়; form-এর সাথে এর কোনো সম্পর্ক নেই।
            - `submit()`-এরও বৈধ ব্যবহার আছে — যেমন আগেই validate করা হয়ে গেছে আর নিজের handler আবার trigger না করে submit করতে চাও — কিন্তু "user যেন Save চেপেছে" এমন আচরণের জন্য `requestSubmit()` ব্যবহার করো।
        """,
        tip_en=r"""Name both missing steps (validation and the `submit` event) — candidates often remember only one. Mentioning `event.submitter` shows you've used the API, not just heard of it.""",
        tip_bn=r"""বাদ পড়া দুটো ধাপের নামই বলো (validation আর `submit` event) — candidate-রা প্রায়ই একটাই মনে রাখে। `event.submitter`-এর কথা বললে বোঝা যায় তুমি API-টা আসলেই ব্যবহার করেছ, শুধু নাম শোনোনি।""",
        refs=[MDN_REQUESTSUBMIT, MDN_FORMSUBMIT],
    ),
    # ------------------------------------------------------------------ html-029
    Q(
        id="html-029", sub="Browser Parsing", diff="hard", type="output",
        prio="medium", market="both", mins=5,
        tags=["parsing", "innerhtml", "error-recovery", "dom", "output"],
        ver="HTML Living Standard (parsing algorithm, version-independent)", vs=False, status="stable",
        q_en=r"""What does this code log? Explain how the HTML parser arrives at each result.""",
        q_bn=r"""এই code কী log করবে? প্রতিটা ফলাফলে HTML parser কীভাবে পৌঁছায়, ব্যাখ্যা করো।""",
        code=r"""
            const box = document.createElement('div');
            box.innerHTML = '<p>Hello<div>World</div></p>';
            console.log(box.innerHTML);
            console.log(box.children.length);

            const table = document.createElement('table');
            table.innerHTML = '<tr><td>1</td></tr>';
            console.log(table.innerHTML);
        """,
        lang="javascript",
        output=r"""
            <p>Hello</p><div>World</div><p></p>
            3
            <tbody><tr><td>1</td></tr></tbody>
        """,
        a_en=r"""
            The HTML parser never throws on invalid markup — it follows precise **error-recovery rules** from the spec, and the resulting DOM can differ from what you wrote.
            - A `<p>` can't contain block-level elements like `<div>`. When the parser sees `<div>` while a `<p>` is open, it **closes the `<p>` first**. So `Hello` ends up in its own paragraph and the `<div>` becomes a sibling.
            - The final `</p>` has no open `<p>` to close. The spec says to **insert an empty `<p>`** and close it — hence `<p></p>` and three children.
            - In table context, a `<tr>` can't be a direct child of `<table>` in the parsed tree, so the parser **creates an implicit `<tbody>`**.
        """,
        a_bn=r"""
            Invalid markup পেলে HTML parser কখনো error throw করে না — spec-এর নির্দিষ্ট **error-recovery নিয়ম** মেনে চলে, আর তৈরি হওয়া DOM তুমি যা লিখেছ তার থেকে আলাদা হতে পারে।
            - `<p>`-এর ভেতরে `<div>`-এর মতো block-level element থাকতে পারে না। `<p>` খোলা থাকা অবস্থায় parser `<div>` দেখলে **আগে `<p>`-টা বন্ধ করে দেয়**। ফলে `Hello` নিজের paragraph-এ থাকে আর `<div>` হয়ে যায় তার sibling।
            - শেষের `</p>`-এর বন্ধ করার মতো কোনো খোলা `<p>` নেই। Spec বলে তখন **একটা খালি `<p>` insert করে** সেটা বন্ধ করতে — তাই `<p></p>` আর মোট তিনটা child।
            - Table-এর context-এ parse করা tree-তে `<tr>` সরাসরি `<table>`-এর child হতে পারে না, তাই parser **নিজে থেকে একটা `<tbody>` তৈরি করে**।
        """,
        quick_en=r"""`<p>Hello</p><div>World</div><p></p>`, `3`, then `<tbody><tr><td>1</td></tr></tbody>`. The parser closes the open `<p>` when it meets `<div>`, turns the stray `</p>` into an empty `<p></p>`, and adds an implicit `<tbody>` for the `<tr>`.""",
        quick_bn=r"""Output: `<p>Hello</p><div>World</div><p></p>`, `3`, তারপর `<tbody><tr><td>1</td></tr></tbody>`। `<div>` পেলে parser খোলা `<p>` বন্ধ করে দেয়, বাড়তি `</p>`-কে একটা খালি `<p></p>` বানায়, আর `<tr>`-এর জন্য implicit `<tbody>` যোগ করে।""",
        ex_en=r"""
            Step by step for the first string, using the fragment parser in "in body" mode:
            1. `<p>` → open `p`; `Hello` → text inside it.
            2. `<div>` → "if a `p` is in button scope, close it" → `p` closed; open `div`; `World` → text.
            3. `</div>` → closes the `div`.
            4. `</p>` → no `p` in scope → parse error → insert a new `p` element, then close it.

            **Why this matters in real projects:**
            - **Hydration errors in React/Next.js:** if a component renders `<div>` inside `<p>` on the server, the browser re-parses the HTML into a different tree, and the client render no longer matches ("In HTML, `<div>` cannot be a descendant of `<p>`"). The fix is valid nesting, not suppressing warnings.
            - **Tables:** stray text or `<div>`s directly inside `<table>` get "foster-parented" — moved *before* the table — which surprises people building tables with string templates.
            - **Nested `<form>`/`<a>`:** a `<form>` start tag inside another form is ignored; an `<a>` inside an `<a>` closes the first one.
            - DOM-building APIs (`createElement`, `append`) don't go through the parser, so they *can* create trees the parser would never produce — another reason SSR output and client DOM can diverge.
        """,
        ex_bn=r"""
            প্রথম string-এর জন্য ধাপে ধাপে ("in body" mode-এ fragment parser):
            1. `<p>` → `p` খোলে; `Hello` → তার ভেতরের text।
            2. `<div>` → "button scope-এ কোনো `p` থাকলে সেটা বন্ধ করো" → `p` বন্ধ; `div` খোলে; `World` → text।
            3. `</div>` → `div` বন্ধ করে।
            4. `</p>` → scope-এ কোনো `p` নেই → parse error → নতুন একটা `p` element insert করে, তারপর সেটা বন্ধ করে।

            **বাস্তব project-এ কেন গুরুত্বপূর্ণ:**
            - **React/Next.js-এ hydration error:** কোনো component server-এ `<p>`-এর ভেতরে `<div>` render করলে browser HTML-টা ভিন্ন tree-তে re-parse করে, ফলে client render আর মেলে না ("In HTML, `<div>` cannot be a descendant of `<p>`")। সমাধান হলো সঠিক nesting, warning চাপা দেওয়া নয়।
            - **Table:** `<table>`-এর সরাসরি ভেতরে থাকা বিচ্ছিন্ন text বা `<div>` "foster-parented" হয় — অর্থাৎ table-এর *আগে* সরিয়ে দেওয়া হয় — string template দিয়ে table বানানো মানুষ এতে অবাক হয়।
            - **Nested `<form>`/`<a>`:** একটা form-এর ভেতরের `<form>` start tag উপেক্ষিত হয়; `<a>`-এর ভেতরে আরেকটা `<a>` এলে প্রথমটা বন্ধ হয়ে যায়।
            - DOM বানানোর API (`createElement`, `append`) parser-এর ভেতর দিয়ে যায় না, তাই তারা এমন tree *বানাতে পারে* যা parser কখনো বানাত না — SSR output আর client DOM আলাদা হওয়ার এটা আরেকটা কারণ।
        """,
        tip_en=r"""Explain the rule ("block start tags close an open `<p>`"), then the surprising extra `<p></p>`, then connect it to hydration mismatches. That last link turns parser trivia into a production-debugging story.""",
        tip_bn=r"""নিয়মটা বলো ("block start tag খোলা `<p>` বন্ধ করে দেয়"), তারপর অবাক করা বাড়তি `<p></p>`, তারপর hydration mismatch-এর সাথে যুক্ত করো। শেষের এই যোগসূত্রটাই parser-এর খুঁটিনাটিকে production debugging-এর গল্পে পরিণত করে।""",
        mist_en=r"""Expecting the markup to be preserved as written, expecting an exception for invalid HTML, or missing the extra empty paragraph.""",
        mist_bn=r"""যেভাবে লেখা হয়েছে markup সেভাবেই থাকবে বলে আশা করা, invalid HTML-এর জন্য exception আশা করা, অথবা বাড়তি খালি paragraph-টা খেয়াল না করা।""",
        follow=[
            ("Why does React warn about `<div>` inside `<p>` during hydration?", "Hydration-এর সময় React কেন `<p>`-এর ভেতরে `<div>` নিয়ে warning দেয়?"),
            ("What is foster parenting in table parsing?", "Table parsing-এ foster parenting কী?"),
        ],
        related=["html-023", "html-019"],
        refs=[SPEC_PARSING, MDN_P],
    ),
    # ------------------------------------------------------------------ html-032
    Q(
        id="html-032", sub="Performance", diff="extreme", type="security-performance",
        prio="medium", market="international", mins=20,
        tags=["dom-size", "virtualization", "content-visibility", "inp", "performance"],
        ver="Version-independent concept (content-visibility: Baseline newly available)", vs=False, status="stable",
        q_en=r"""An internal order-management dashboard renders a table of about 15,000 orders — each row has a dozen cells, status badges and action buttons, roughly 400,000 DOM nodes in total. On office laptops it's sluggish; on the mid-range Android tablets used in the warehouse, typing in the filter box lags, scrolling janks and the tab sometimes crashes. How would you diagnose and fix it?""",
        q_bn=r"""একটা internal order-management dashboard প্রায় 15,000 order-এর একটা table render করে — প্রতিটা row-এ এক ডজন cell, status badge আর action button, সব মিলিয়ে প্রায় 400,000 DOM node। অফিসের laptop-এ এটা ধীর; আর warehouse-এ ব্যবহৃত mid-range Android tablet-এ filter box-এ type করলে দেরি হয়, scroll আটকে আটকে চলে, মাঝে মাঝে tab crash করে। কীভাবে diagnose করবে আর ঠিক করবে?""",
        a_en=r"""
            This is advanced material. The core problem is rendering far more DOM than anyone can see.

            **Diagnose first**
            - DevTools **Performance** panel on a throttled CPU: look for long tasks while typing (poor INP), large "Recalculate Style" and "Layout" blocks that scale with node count, and forced-reflow warnings (layout thrashing).
            - **Memory** panel: heap snapshots for node count, detached DOM trees and duplicated data.
            - Lighthouse's DOM size audit for a quick number.

            **Fix, in order of impact**
            1. **Don't render what isn't visible.** Best: server-side filtering and pagination — the tablet never receives 15,000 rows. If the UX needs one long scrollable list, use **virtualization** (render only the ~50 visible rows plus a buffer, recycle them on scroll) — usually with a proven library rather than hand-rolled.
            2. **Make filtering cheap.** Debounce input, filter on the server or in a Web Worker, and update the DOM once per frame.
            3. **Shrink each row.** Fewer wrapper elements, badges via CSS instead of extra spans, one shared SVG sprite (`<use href>`) instead of inline icons per row, action menus rendered on demand (a single popover reused for all rows).
            4. **One listener, not 45,000.** Event delegation on the table for all row actions.
            5. **Cheaper rendering of what remains.** `table-layout: fixed` so the browser doesn't measure every cell to size columns. If the list is rendered as block or grid boxes (e.g. a card view on tablets), `content-visibility: auto` with `contain-intrinsic-size` on each group lets off-screen groups skip layout and paint. It relies on containment, which has no effect on internal table boxes like `<tbody>` and `<tr>`, so it won't help a classic table.
            6. **Avoid layout thrashing.** Batch DOM reads (e.g. `offsetHeight`) before writes; never read layout inside a loop that also writes.
        """,
        a_bn=r"""
            এটা advanced বিষয়। মূল সমস্যা হলো, কেউ যতটা দেখতে পারে তার চেয়ে অনেক বেশি DOM render করা হচ্ছে।

            **আগে diagnose করো**
            - CPU throttle করে DevTools-এর **Performance** panel: type করার সময় long task (খারাপ INP), node সংখ্যার সাথে বাড়তে থাকা বড় "Recalculate Style" আর "Layout" block, আর forced reflow warning (layout thrashing) খোঁজো।
            - **Memory** panel: heap snapshot দিয়ে node সংখ্যা, detached DOM tree আর একই data-র একাধিক copy দেখো।
            - দ্রুত একটা সংখ্যা পেতে Lighthouse-এর DOM size audit।

            **ঠিক করো, প্রভাবের ক্রমে**
            1. **যা দেখা যায় না তা render কোরো না।** সবচেয়ে ভালো: server-side filtering আর pagination — tablet-এ 15,000 row আসেই না। UX-এর জন্য যদি একটা লম্বা scroll করা list লাগেই, তাহলে **virtualization** (শুধু দৃশ্যমান ~50টা row আর কিছু buffer render করো, scroll-এ সেগুলোই আবার ব্যবহার করো) — সাধারণত নিজে না বানিয়ে পরীক্ষিত library দিয়ে।
            2. **Filtering সস্তা করো।** Input debounce করো, server-এ বা Web Worker-এ filter করো, আর প্রতি frame-এ একবার DOM update করো।
            3. **প্রতিটা row ছোট করো।** কম wrapper element, বাড়তি span-এর বদলে CSS দিয়ে badge, প্রতি row-এ inline icon-এর বদলে একটা shared SVG sprite (`<use href>`), আর action menu দরকার হলে তবেই render (সব row-এর জন্য একটাই popover আবার ব্যবহার)।
            4. **45,000 নয়, একটা listener।** সব row action-এর জন্য table-এ event delegation।
            5. **বাকি যা থাকে তার rendering সস্তা করো।** `table-layout: fixed`, যাতে column-এর মাপ ঠিক করতে browser-কে প্রতিটা cell মাপতে না হয়। List যদি block বা grid box হিসেবে render হয় (যেমন tablet-এ card view), তাহলে প্রতিটা group-এ `contain-intrinsic-size`-সহ `content-visibility: auto` দিলে screen-এর বাইরের group layout আর paint এড়িয়ে যায়। এটা containment-এর উপর নির্ভর করে, আর `<tbody>`, `<tr>`-এর মতো internal table box-এ containment কাজ করে না — তাই সাধারণ table-এ এটা কোনো উপকার করবে না।
            6. **Layout thrashing এড়াও।** DOM read (যেমন `offsetHeight`) আগে একসাথে করো, তারপর write; একই loop-এ layout পড়া আর লেখা কখনো মিশিও না।
        """,
        quick_en=r"""This is advanced: the page renders far more DOM than anyone can see. Profile on a throttled CPU, then stop rendering it all with server-side filtering and pagination or virtualization, plus debounced filtering, slimmer rows, one delegated listener and `table-layout: fixed`.""",
        quick_bn=r"""এটা advanced বিষয়: page-টা দেখার চেয়ে অনেক বেশি DOM render করছে। Throttled CPU-তে profile করি, তারপর server-side filtering আর pagination বা virtualization দিয়ে সব render করা বন্ধ করি; সাথে debounced filtering, হালকা row, একটা delegated listener আর `table-layout: fixed`।""",
        ex_en=r"""
            **Why big DOMs hurt:** every node costs memory (plus its accessibility-tree counterpart), style recalculation and layout work grow with the number of affected nodes, and a filter keystroke that re-renders 15,000 rows becomes one huge main-thread task. Low-end devices have less memory and slower CPUs, so the same page that's "sluggish" on a laptop crashes on a tablet.

            **Trade-offs:**
            - **Virtualization** breaks browser find-in-page (Ctrl+F) and printing, and complicates keyboard and screen-reader navigation; for an ARIA grid you'd need `aria-rowcount`/`aria-rowindex` so users know where they are.
            - **`content-visibility: auto`** keeps everything in the DOM (find-in-page still works) but doesn't reduce memory or node count — good for long *documents*, not a cure for 400k nodes. It's Baseline newly available, so older browsers simply render normally.
            - **Server-side pagination** needs API and UX changes (e.g. "Export CSV" for people who really need all rows) but scales indefinitely.

            **Prove the fix:** compare INP and long-task counts before/after on the actual warehouse tablets, and add a regression check (DOM node count or a Performance budget) to CI.
        """,
        ex_bn=r"""
            **বড় DOM কেন ক্ষতিকর:** প্রতিটা node memory খায় (সাথে accessibility tree-তেও তার একটা প্রতিরূপ থাকে), style recalculation আর layout-এর কাজ প্রভাবিত node-এর সংখ্যার সাথে বাড়ে, আর filter-এর একটা keystroke-এ 15,000 row re-render মানে main thread-এ একটা বিশাল task। Low-end device-এ memory কম আর CPU ধীর, তাই যে page laptop-এ "ধীর", সেটাই tablet-এ crash করে।

            **Trade-off:**
            - **Virtualization** browser-এর find-in-page (Ctrl+F) আর printing ভেঙে দেয়, আর keyboard ও screen reader navigation জটিল করে; ARIA grid হলে `aria-rowcount`/`aria-rowindex` দিতে হবে, যাতে user বোঝে সে কোথায় আছে।
            - **`content-visibility: auto`** সবকিছু DOM-এ রাখে (find-in-page তখনো কাজ করে), কিন্তু memory বা node সংখ্যা কমায় না — লম্বা *document*-এর জন্য ভালো, 400k node-এর প্রতিকার নয়। এটা Baseline newly available, তাই পুরোনো browser শুধু স্বাভাবিকভাবে render করবে।
            - **Server-side pagination**-এ API আর UX বদলাতে হয় (যেমন যাদের সত্যিই সব row লাগে তাদের জন্য "Export CSV"), কিন্তু এটা যত বড়ই হোক scale করে।

            **সমাধান প্রমাণ করো:** আসল warehouse tablet-এ আগে-পরে INP আর long task-এর সংখ্যা তুলনা করো, আর CI-তে একটা regression check (DOM node সংখ্যা বা performance budget) যোগ করো।
        """,
        tip_en=r"""Lead with measurement, then the biggest lever (render less), then the smaller ones. Explicitly naming the trade-offs of virtualization (find-in-page, accessibility) is what makes this a senior answer rather than "use react-window".""",
        tip_bn=r"""মাপজোখ দিয়ে শুরু করো, তারপর সবচেয়ে বড় হাতিয়ার (কম render করা), তারপর ছোটগুলো। Virtualization-এর trade-off (find-in-page, accessibility) স্পষ্ট করে বললেই এটা "react-window ব্যবহার করো" নয়, একটা senior উত্তর হয়ে ওঠে।""",
        mist_en=r"""Jumping straight to `will-change` or micro-optimising selectors, memoising components while still rendering 15,000 rows, or assuming `content-visibility` reduces memory.""",
        mist_bn=r"""সরাসরি `will-change` বা selector-এর ছোটখাটো optimisation-এ ঝাঁপিয়ে পড়া, 15,000 row render করা বজায় রেখে component memoise করা, অথবা ধরে নেওয়া যে `content-visibility` memory কমায়।""",
        code=r"""
            <style>
              .orders { table-layout: fixed; width: 100%; }

              /* Tablet card view: orders grouped by day as block boxes.
                 Off-screen groups skip layout and paint. */
              .order-day {
                content-visibility: auto;
                contain-intrinsic-size: auto 1200px;
              }
            </style>

            <table class="orders" id="orders">
              <!-- <thead> ... -->
              <!-- many <tbody> groups -->
            </table>

            <script type="module">
              // One delegated listener instead of one per button
              document.getElementById('orders').addEventListener('click', (event) => {
                const button = event.target.closest('button[data-action]');
                if (!button) return;
                const orderId = button.closest('tr').dataset.orderId;
                if (button.dataset.action === 'cancel') cancelOrder(orderId);
                if (button.dataset.action === 'print') printLabel(orderId);
              });

              // Debounced filter; the server returns one page of matching rows
              let timer;
              document.getElementById('filter').addEventListener('input', (event) => {
                clearTimeout(timer);
                timer = setTimeout(() => loadPage({ q: event.target.value, page: 1 }), 250);
              });
            </script>
        """,
        lang="html",
        follow=[
            ("How do you keep a virtualized table accessible to screen-reader and keyboard users?", "Virtualized table-কে screen reader আর keyboard user-দের জন্য কীভাবে accessible রাখবে?"),
            ("What is layout thrashing, and how would you spot it in a performance trace?", "Layout thrashing কী, আর performance trace-এ কীভাবে ধরবে?"),
        ],
        related=["html-019", "html-030"],
        refs=[WEBDEV_DOM_SIZE, WEBDEV_CONTENT_VISIBILITY, WEBDEV_LAYOUT_THRASHING],
    ),
]

if __name__ == "__main__":
    save("html", "b4", QUESTIONS)
