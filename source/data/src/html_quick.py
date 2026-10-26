import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

VER = "HTML Living Standard (version-independent)"

QUESTIONS = [
    # ------------------------------------------------------------------ html-q01
    Q(
        id="html-q01", sub="Semantic HTML", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["div", "span", "block", "inline"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `<div>` and `<span>`?""",
        q_bn=r"""`<div>` আর `<span>`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""Both are generic containers with no meaning of their own. `<div>` is block-level by default (it starts on a new line and takes the full width), while `<span>` is inline (it sits inside a line of text). Use them only when no semantic element fits, mostly as hooks for CSS or JavaScript.""",
        a_bn=r"""দুটোই generic container, নিজের কোনো অর্থ নেই। `<div>` default-ভাবে block-level (নতুন line-এ শুরু হয়, পুরো width নেয়), আর `<span>` inline (text-এর line-এর ভেতরেই বসে)। কোনো semantic element না মিললে তবেই এগুলো ব্যবহার করো, মূলত CSS বা JavaScript-এর hook হিসেবে।""",
        code=r"""
            <div class="card">
              <p>Price: <span class="price">৳1,250</span></p>
            </div>
        """, lang="html",
        ex_en=r"""The block/inline look comes from the browser's default `display`, so CSS can change it. HTML's content rules don't change, though: a `<span>` may contain only phrasing content, so `<span><div>…</div></span>` is invalid.""",
        ex_bn=r"""Block/inline চেহারাটা আসে browser-এর default `display` থেকে, তাই CSS দিয়ে বদলানো যায়। তবে HTML-এর content rule বদলায় না: `<span>`-এর ভেতরে শুধু phrasing content রাখা যায়, তাই `<span><div>…</div></span>` invalid।""",
        tip_en=r"""Say "both are meaningless containers, block vs inline", then add that you reach for semantic elements first.""",
        tip_bn=r"""বলো "দুটোই অর্থহীন container, একটা block আরেকটা inline", তারপর যোগ করো যে তুমি আগে semantic element খোঁজো।""",
        follow=[
            ("Can a `<span>` contain a `<div>`?", "`<span>`-এর ভেতরে কি `<div>` রাখা যায়?"),
            ("When would you use `<section>` instead of `<div>`?", "কখন `<div>`-এর বদলে `<section>` ব্যবহার করবে?"),
        ],
        related=["html-001", "css-q01"],
        refs=[("MDN — <div>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/div")],
    ),
    # ------------------------------------------------------------------ html-q02
    Q(
        id="html-q02", sub="Accessibility", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["table", "caption", "th", "scope", "accessibility"],
        ver=VER, vs=False, status="stable",
        q_en=r"""How do you mark up an accessible data table, and should tables be used for layout?""",
        q_bn=r"""Accessible data table-এর markup কীভাবে লেখো? আর layout-এর জন্য কি table ব্যবহার করা উচিত?""",
        a_en=r"""Use `<table>` only for tabular data, never for page layout. Give it a `<caption>` as its title, put headers in `<th>` with `scope="col"` or `scope="row"`, and group rows with `<thead>` and `<tbody>`, so screen readers can announce each cell together with its header.""",
        a_bn=r"""`<table>` শুধু tabular data-র জন্য, page layout-এর জন্য কখনো নয়। Title হিসেবে `<caption>` দাও, header রাখো `scope="col"` বা `scope="row"`-সহ `<th>`-এ, আর row-গুলো `<thead>` ও `<tbody>`-তে ভাগ করো, যাতে screen reader প্রতিটা cell তার header-সহ পড়ে শোনাতে পারে।""",
        code=r"""
            <table>
              <caption>Recent orders</caption>
              <thead><tr><th scope="col">Order</th><th scope="col">Total</th></tr></thead>
              <tbody>
                <tr><th scope="row">DK-1001</th><td>৳1,850</td></tr>
              </tbody>
            </table>
        """, lang="html",
        ex_en=r"""Layout tables confuse screen readers, which announce rows and columns, and they don't reflow on phones; use CSS Grid or Flexbox for layout. Tables with multi-level headers may need the `headers` attribute pointing to header `id`s.""",
        ex_bn=r"""Layout-এর জন্য table দিলে screen reader বিভ্রান্ত হয়, কারণ সে row আর column ঘোষণা করে, আর phone-এ এমন table reflow-ও করে না; layout-এর জন্য CSS Grid বা Flexbox ব্যবহার করো। একাধিক স্তরের header থাকলে header-এর `id` নির্দেশ করে `headers` attribute লাগতে পারে।""",
        tip_en=r"""Name the four pieces (`<caption>`, `<thead>`, `<th scope>`, `<tbody>`) and say clearly "tables are for data, not layout".""",
        tip_bn=r"""চারটা অংশের নাম বলো (`<caption>`, `<thead>`, `<th scope>`, `<tbody>`) আর স্পষ্ট করে বলো "table data-র জন্য, layout-এর জন্য নয়"।""",
        follow=[
            ("How would you make a wide table usable on a phone?", "চওড়া একটা table phone-এ কীভাবে ব্যবহারযোগ্য করবে?"),
            ("What is the `headers` attribute for?", "`headers` attribute কী কাজে লাগে?"),
        ],
        related=["html-029", "html-032"],
        refs=[("MDN — <table>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/table")],
    ),
    # ------------------------------------------------------------------ html-q03
    Q(
        id="html-q03", sub="HTML Attributes", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["links", "target-blank", "noopener", "security"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What does `target="_blank"` do, and why do people add `rel="noopener noreferrer"`?""",
        q_bn=r"""`target="_blank"` কী করে, আর মানুষ কেন সাথে `rel="noopener noreferrer"` যোগ করে?""",
        a_en=r"""`target="_blank"` opens the link in a new tab or window. `rel="noopener"` stops the new page from using `window.opener` to redirect your tab (reverse tabnabbing), and `noreferrer` also hides the `Referer` header. Modern browsers already treat `target="_blank"` links as `noopener`, but writing it explicitly is still common.""",
        a_bn=r"""`target="_blank"` link-টা নতুন tab বা window-এ খোলে। `rel="noopener"` নতুন page-কে `window.opener` দিয়ে তোমার tab redirect করতে দেয় না (reverse tabnabbing), আর `noreferrer` সাথে `Referer` header-ও লুকায়। এখনকার browser `target="_blank"` link-কে নিজে থেকেই `noopener` ধরে, তবু স্পষ্ট করে লিখে দেওয়াটা প্রচলিত।""",
        code=r"""
            <a href="https://partner.example" target="_blank" rel="noopener noreferrer">
              Partner shop (opens in a new tab)
            </a>
        """, lang="html",
        ex_en=r"""The implicit `noopener` applies to `<a>`/`<area>` links, not to `window.open()`, where you pass `'noopener'` in the features string. Also tell users a link opens a new tab, because unexpected tabs disorient keyboard and screen-reader users.""",
        ex_bn=r"""এই implicit `noopener` শুধু `<a>`/`<area>` link-এ খাটে, `window.open()`-এ নয়; সেখানে features string-এ `'noopener'` দিতে হয়। আর link নতুন tab-এ খুলবে সেটা user-কে জানাও, কারণ হঠাৎ নতুন tab keyboard আর screen reader user-দের বিভ্রান্ত করে।""",
        tip_en=r"""Explain the `window.opener` risk in one line, then mention that browsers now imply `noopener`, which shows your knowledge is current.""",
        tip_bn=r"""এক লাইনে `window.opener`-এর ঝুঁকি বোঝাও, তারপর বলো যে browser এখন নিজেই `noopener` ধরে নেয়; এতে বোঝা যায় তোমার জ্ঞান up-to-date।""",
        follow=[
            ("What is reverse tabnabbing?", "Reverse tabnabbing কী?"),
            ("Why might you skip `noreferrer` on links to your own sites?", "নিজের অন্য site-এর link-এ কেন `noreferrer` বাদ দিতে পারো?"),
        ],
        related=["html-020"],
        refs=[("MDN — <a>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a")],
    ),
    # ------------------------------------------------------------------ html-q04
    Q(
        id="html-q04", sub="Security", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["iframe", "sandbox", "security", "permissions-policy"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What does the `sandbox` attribute on an `<iframe>` do?""",
        q_bn=r"""`<iframe>`-এর `sandbox` attribute কী করে?""",
        a_en=r"""`sandbox` runs the framed page with extra restrictions: an empty `sandbox` blocks scripts, form submission, popups and top-level navigation, and treats the content as a unique origin. You switch back on only what you need with tokens like `allow-scripts` or `allow-forms`. The separate `allow` attribute grants features like fullscreen or camera.""",
        a_bn=r"""`sandbox` frame-এর ভেতরের page-কে বাড়তি বিধিনিষেধে চালায়: খালি `sandbox` দিলে script, form submit, popup আর top-level navigation বন্ধ থাকে, আর content-কে একটা আলাদা unique origin ধরা হয়। যা দরকার শুধু সেটুকু `allow-scripts` বা `allow-forms`-এর মতো token দিয়ে আবার চালু করো। আলাদা `allow` attribute fullscreen বা camera-র মতো feature-এর অনুমতি দেয়।""",
        code=r"""
            <iframe src="https://widgets.example/map" title="Store location map"
                    sandbox="allow-scripts allow-popups"
                    allow="fullscreen" loading="lazy"></iframe>
        """, lang="html",
        ex_en=r"""Never combine `allow-scripts` with `allow-same-origin` for content from your own origin: the framed script could then remove its own sandbox. Every `<iframe>` also needs a `title` so screen-reader users know what it contains.""",
        ex_bn=r"""নিজের origin-এর content-এ কখনো `allow-scripts` আর `allow-same-origin` একসাথে দিও না: তাহলে frame-এর script নিজের sandbox নিজেই তুলে ফেলতে পারে। প্রতিটা `<iframe>`-এ একটা `title`-ও দরকার, যাতে screen reader user বোঝে ভেতরে কী আছে।""",
        tip_en=r"""Describe it as "start with everything blocked, then allow only what's needed", and mention the `allow-scripts` + `allow-same-origin` trap.""",
        tip_bn=r"""এভাবে বলো "শুরুতে সব বন্ধ, তারপর শুধু দরকারিটুকু চালু", আর `allow-scripts` + `allow-same-origin`-এর ফাঁদটা উল্লেখ করো।""",
        follow=[
            ("How do you stop other sites from framing your page?", "অন্য site যেন তোমার page frame করতে না পারে, সেটা কীভাবে আটকাবে?"),
        ],
        related=["html-027", "html-010"],
        refs=[("MDN — <iframe>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe")],
    ),
    # ------------------------------------------------------------------ html-q05
    Q(
        id="html-q05", sub="HTML Attributes", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["id", "class", "attributes", "selectors"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between the `id` and `class` attributes?""",
        q_bn=r"""`id` আর `class` attribute-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""An `id` must be unique in the page and identifies one element; it's used for fragment links (`#reviews`), `<label for>`, ARIA references and `getElementById()`. A `class` can be shared by many elements, and one element can have several, so classes are the usual hook for CSS styling.""",
        a_bn=r"""`id` পুরো page-এ unique হতে হয় আর একটা element-কেই চিহ্নিত করে; এটা লাগে fragment link (`#reviews`), `<label for>`, ARIA reference আর `getElementById()`-এ। `class` অনেক element-এ একসাথে থাকতে পারে, একটা element-এ কয়েকটা class-ও থাকতে পারে, তাই CSS styling-এর সাধারণ hook হলো class।""",
        code=r"""
            <section id="reviews" class="panel panel--wide">…</section>
            <a href="#reviews">Jump to reviews</a>
            <script>
              document.getElementById('reviews');          // one element
              document.querySelectorAll('.panel').length;  // every .panel
            </script>
        """, lang="html",
        ex_en=r"""ID selectors have much higher specificity than classes, so they're hard to override; many teams style with classes only. Duplicate IDs silently break labels, ARIA links and `getElementById()`.""",
        ex_bn=r"""ID selector-এর specificity class-এর চেয়ে অনেক বেশি, তাই override করা কঠিন; অনেক team শুধু class দিয়েই style করে। Duplicate ID থাকলে label, ARIA link আর `getElementById()` চুপচাপ ভেঙে যায়।""",
        tip_en=r"""Say "unique identity vs reusable group", then give one use of each.""",
        tip_bn=r"""বলো "unique পরিচয় বনাম বারবার ব্যবহারযোগ্য group", তারপর প্রতিটার একটা করে ব্যবহার দেখাও।""",
        follow=[
            ("Why do many teams avoid ID selectors in CSS?", "অনেক team CSS-এ ID selector এড়িয়ে চলে কেন?"),
        ],
        related=["html-011", "css-002"],
        refs=[("MDN — id attribute", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/id")],
    ),
    # ------------------------------------------------------------------ html-q06
    Q(
        id="html-q06", sub="Forms and Validation", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["forms", "get", "post", "http"],
        ver=VER, vs=False, status="stable",
        q_en=r"""In a form, what is the difference between `method="get"` and `method="post"`?""",
        q_bn=r"""Form-এ `method="get"` আর `method="post"`-এর পার্থক্য কী?""",
        a_en=r"""With `get` (the default) the form data is added to the URL as a query string, so it's visible and bookmarkable, which suits search and filters. With `post` the data goes in the request body, used for anything that changes data, like sign-up or placing an order. POST is not encrypted by itself; HTTPS is still required.""",
        a_bn=r"""`get` (default) দিলে form-এর data URL-এ query string হিসেবে যোগ হয়, তাই দেখা যায় আর bookmark করা যায়; search বা filter-এর জন্য এটা ঠিক আছে। `post` দিলে data যায় request body-তে; sign-up বা order দেওয়ার মতো data বদলানো কাজে এটা ব্যবহার হয়। POST নিজে থেকে encrypted নয়, HTTPS লাগবেই।""",
        code=r"""
            <form action="/search" method="get">
              <input name="q" value="panjabi">  <!-- → /search?q=panjabi -->
            </form>
            <form action="/orders" method="post">…</form>
        """, lang="html",
        ex_en=r"""GET URLs end up in history, logs and caches, so never send passwords or tokens with GET. HTML forms only support `get`, `post` and `dialog`; PUT or DELETE need `fetch`.""",
        ex_bn=r"""GET-এর URL history, log আর cache-এ থেকে যায়, তাই password বা token কখনো GET দিয়ে পাঠাবে না। HTML form শুধু `get`, `post` আর `dialog` বোঝে; PUT বা DELETE-এর জন্য `fetch` লাগে।""",
        tip_en=r"""Tie each method to a use case: "GET for reading and sharing a URL, POST for changing data".""",
        tip_bn=r"""প্রতিটা method-কে একটা use case-এর সাথে মেলাও: "পড়া আর URL share করার জন্য GET, data বদলানোর জন্য POST"।""",
        follow=[
            ("Why is a login form never sent with GET?", "Login form কেন কখনো GET দিয়ে পাঠানো হয় না?"),
        ],
        related=["html-013", "html-028"],
        refs=[("MDN — <form>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form")],
    ),
    # ------------------------------------------------------------------ html-q07
    Q(
        id="html-q07", sub="Browser Parsing", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["void-elements", "self-closing", "parsing"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are void (self-closing) elements in HTML?""",
        q_bn=r"""HTML-এ void (self-closing) element কী?""",
        a_en=r"""Void elements can't have content, so they have no closing tag: `<img>`, `<br>`, `<hr>`, `<input>`, `<meta>`, `<link>`, `<source>` and a few others. In HTML the slash in `<br />` is allowed but ignored, and it does not self-close other elements: `<div />` is just an opening `<div>`.""",
        a_bn=r"""Void element-এর ভেতরে কোনো content থাকতে পারে না, তাই closing tag-ও নেই: `<img>`, `<br>`, `<hr>`, `<input>`, `<meta>`, `<link>`, `<source>` আর আরও কয়েকটা। HTML-এ `<br />`-এর slash লেখা যায়, কিন্তু parser সেটা উপেক্ষা করে, আর অন্য element-কে এটা বন্ধ করে না: `<div />` আসলে শুধু একটা খোলা `<div>`।""",
        code=r"""
            <img src="logo.png" alt="Dokan">
            <input type="email" name="email">
            <br />            <!-- the slash is ignored -->
            <div class="x" /> <!-- parsed as <div class="x">, still open -->
        """, lang="html",
        ex_en=r"""JSX, XML and inline SVG are different: there `<div />` really is closed, which is why React code is full of it. Copying that habit into plain HTML nests the following content inside the unclosed `<div>`.""",
        ex_bn=r"""JSX, XML আর inline SVG আলাদা: সেখানে `<div />` সত্যিই বন্ধ হয়, এজন্যই React code-এ এটা এত দেখা যায়। এই অভ্যাস plain HTML-এ আনলে পরের content সব না-বন্ধ হওয়া `<div>`-এর ভেতরে ঢুকে যায়।""",
        tip_en=r"""List three void elements, then mention the `<div />` gotcha; interviewers like hearing the HTML vs JSX difference.""",
        tip_bn=r"""তিনটা void element-এর নাম বলো, তারপর `<div />`-এর ফাঁদটা বলো; HTML আর JSX-এর পার্থক্য শুনলে interviewer খুশি হয়।""",
        follow=[
            ("Why does `<div />` work in React but not in HTML?", "`<div />` React-এ কাজ করে কিন্তু HTML-এ কেন করে না?"),
        ],
        related=["html-029"],
        refs=[("MDN — Void element", "https://developer.mozilla.org/en-US/docs/Glossary/Void_element")],
    ),
    # ------------------------------------------------------------------ html-q08
    Q(
        id="html-q08", sub="Semantic HTML", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["strong", "em", "b", "i", "semantics"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `<strong>` and `<b>`, and between `<em>` and `<i>`?""",
        q_bn=r"""`<strong>` আর `<b>`, এবং `<em>` আর `<i>`-এর পার্থক্য কী?""",
        a_en=r"""`<strong>` marks strong importance and `<em>` marks stress emphasis that changes the meaning of a sentence. `<b>` and `<i>` are for text that is styled differently without extra importance, like keywords, product names or a phrase in another language. They look the same by default, so choose by meaning, not looks.""",
        a_bn=r"""`<strong>` বোঝায় বিশেষ গুরুত্ব, আর `<em>` বোঝায় এমন জোর যেটা বাক্যের অর্থ বদলে দেয়। `<b>` আর `<i>` হলো বাড়তি গুরুত্ব ছাড়া আলাদা ভাবে দেখানো text-এর জন্য, যেমন keyword, product-এর নাম বা অন্য ভাষার শব্দ। Default-ভাবে দেখতে একই, তাই চেহারা নয়, অর্থ দেখে বেছে নাও।""",
        code=r"""
            <p><strong>Warning:</strong> the payment link expires in 10 minutes.</p>
            <p>I <em>never</em> said that.</p>
            <p><b>Free delivery</b> on orders over ৳1,000.</p>
            <p>The saree is <i lang="bn">জামদানি</i>.</p>
        """, lang="html",
        ex_en=r"""If you only want bold or italic for visual design, use CSS (`font-weight`, `font-style`) instead of any of these tags.""",
        ex_bn=r"""শুধু design-এর জন্য bold বা italic চাইলে এই tag-গুলোর কোনোটাই নয়, CSS (`font-weight`, `font-style`) ব্যবহার করো।""",
        tip_en=r"""Say "`strong`/`em` carry meaning, `b`/`i` are styled text without extra importance" and give one example each.""",
        tip_bn=r"""বলো "`strong`/`em` অর্থ বহন করে, `b`/`i` বাড়তি গুরুত্ব ছাড়া আলাদা চেহারার text", আর প্রতিটার একটা example দাও।""",
        follow=[
            ("Should you use `<b>` just to make a heading bold?", "শুধু heading bold করার জন্য কি `<b>` ব্যবহার করা উচিত?"),
        ],
        related=["html-001"],
        refs=[("MDN — <strong>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/strong")],
    ),
    # ------------------------------------------------------------------ html-q09
    Q(
        id="html-q09", sub="HTML APIs", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["localstorage", "sessionstorage", "cookies", "web-storage"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `localStorage`, `sessionStorage` and cookies?""",
        q_bn=r"""`localStorage`, `sessionStorage` আর cookie-র মধ্যে পার্থক্য কী?""",
        a_en=r"""`localStorage` keeps string data per origin until it's cleared, `sessionStorage` keeps it only for that tab and clears it when the tab closes, and cookies are small values the browser sends to the server with every matching request. Avoid keeping auth tokens in Web Storage, because any XSS can read it; `HttpOnly` cookies are safer for sessions.""",
        a_bn=r"""`localStorage` প্রতিটা origin-এর string data মুছে না ফেলা পর্যন্ত রাখে, `sessionStorage` রাখে শুধু ওই tab-এর জন্য আর tab বন্ধ হলে মুছে যায়, আর cookie হলো ছোট value যেটা browser প্রতিটা মিলে যাওয়া request-এর সাথে server-এ পাঠায়। Auth token Web Storage-এ রেখো না, কারণ যেকোনো XSS সেটা পড়তে পারে; session-এর জন্য `HttpOnly` cookie বেশি নিরাপদ।""",
        code=r"""
            localStorage.setItem('cart', JSON.stringify([42, 7]));
            console.log(JSON.parse(localStorage.getItem('cart'))); // → [42, 7]
            localStorage.setItem('count', 5);
            console.log(typeof localStorage.getItem('count'));    // → "string"
            sessionStorage.setItem('step', '2'); // gone when this tab closes
        """, lang="javascript",
        ex_en=r"""Web Storage is synchronous and stores only strings, so objects need `JSON.stringify`/`JSON.parse`, and big data belongs in IndexedDB. Cookie attributes `HttpOnly`, `Secure` and `SameSite` control script access and cross-site sending.""",
        ex_bn=r"""Web Storage synchronous আর শুধু string রাখে, তাই object-এর জন্য `JSON.stringify`/`JSON.parse` লাগে, আর বড় data-র জায়গা IndexedDB। Cookie-র `HttpOnly`, `Secure` আর `SameSite` attribute ঠিক করে script পড়তে পারবে কিনা আর cross-site request-এ যাবে কিনা।""",
        tip_en=r"""Compare them on three points (lifetime, scope, sent to server or not), then add the security note about tokens.""",
        tip_bn=r"""তিনটা দিক দিয়ে তুলনা করো (কতদিন থাকে, কোথায় দেখা যায়, server-এ যায় কিনা), তারপর token নিয়ে security-র কথাটা যোগ করো।""",
        follow=[
            ("What do the `HttpOnly` and `SameSite` cookie attributes do?", "Cookie-র `HttpOnly` আর `SameSite` attribute কী করে?"),
        ],
        related=["html-027", "html-020"],
        refs=[("MDN — Web Storage API", "https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API")],
    ),
    # ------------------------------------------------------------------ html-q10
    Q(
        id="html-q10", sub="HTML APIs", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["web-components", "custom-elements", "shadow-dom"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are Web Components?""",
        q_bn=r"""Web Components কী?""",
        a_en=r"""Web Components are browser-native reusable elements. You define a custom element (a class registered with `customElements.define()`, whose name must contain a hyphen), can give it a shadow DOM that scopes its markup and styles, and can use `<template>` and `<slot>` for content. They work with any framework or none.""",
        a_bn=r"""Web Components হলো browser-এর নিজস্ব, বারবার ব্যবহারযোগ্য element। তুমি একটা custom element define করো (`customElements.define()` দিয়ে register করা একটা class, যার নামে hyphen থাকতেই হবে), চাইলে তাকে shadow DOM দাও যা তার markup আর style আলাদা করে রাখে, আর content-এর জন্য `<template>` ও `<slot>` ব্যবহার করতে পারো। যেকোনো framework-এ বা framework ছাড়াই চলে।""",
        code=r"""
            class PriceTag extends HTMLElement {
              constructor() { super(); this.attachShadow({ mode: 'open' }); }
              connectedCallback() {
                this.shadowRoot.textContent = `৳${this.getAttribute('amount')}`;
              }
            }
            customElements.define('price-tag', PriceTag);
            // <price-tag amount="1250"></price-tag> → shows ৳1250
        """, lang="javascript",
        ex_en=r"""Shadow DOM stops page CSS from leaking in (inherited properties and custom properties still pass through), which is great for widgets but makes global theming harder. Declarative shadow DOM (`<template shadowrootmode="open">`) lets the server render it without JavaScript.""",
        ex_bn=r"""Shadow DOM page-এর CSS ভেতরে ঢুকতে দেয় না (inherited property আর custom property অবশ্য ঢোকে), widget-এর জন্য এটা দারুণ, কিন্তু global theming কঠিন করে। Declarative shadow DOM (`<template shadowrootmode="open">`) দিয়ে server JavaScript ছাড়াই এটা render করতে পারে।""",
        tip_en=r"""Name the three parts (custom elements, shadow DOM, templates/slots) and say when you'd use them: widgets shared across apps with different frameworks.""",
        tip_bn=r"""তিনটা অংশের নাম বলো (custom element, shadow DOM, template/slot) আর কখন ব্যবহার করবে সেটা বলো: ভিন্ন ভিন্ন framework-এর app-এ share করা widget।""",
        follow=[
            ("How do you style a component's internals from outside its shadow DOM?", "Shadow DOM-এর বাইরে থেকে component-এর ভেতরের অংশ কীভাবে style করবে?"),
        ],
        related=["html-019"],
        refs=[("MDN — Web Components", "https://developer.mozilla.org/en-US/docs/Web/API/Web_components")],
    ),
]

if __name__ == "__main__":
    save("html", "quick", QUESTIONS)
