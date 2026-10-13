import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_ELEMENTS = ("MDN — HTML elements reference", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements")
MDN_MAIN = ("MDN — <main>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/main")
MDN_META = ("MDN — <meta>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta")
MDN_HTML_EL = ("MDN — <html> (lang)", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/html")
MDN_BUTTON = ("MDN — <button>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button")
MDN_A = ("MDN — <a>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a")
MDN_SCRIPT = ("MDN — <script>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/script")
SPEC_SCRIPTING = ("HTML Standard — Scripting", "https://html.spec.whatwg.org/multipage/scripting.html")
MDN_SETCUSTOM = ("MDN — setCustomValidity()", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/setCustomValidity")
MDN_VALIDITY = ("MDN — ValidityState", "https://developer.mozilla.org/en-US/docs/Web/API/ValidityState")
MDN_DIALOG = ("MDN — <dialog>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog")
MDN_INVOKERS = ("MDN — Invoker Commands API", "https://developer.mozilla.org/en-US/docs/Web/API/Invoker_Commands_API")
SPEC_PARSING = ("HTML Standard — Parsing HTML documents", "https://html.spec.whatwg.org/multipage/parsing.html")
WEBDEV_PRELOAD_SCANNER = ("web.dev — Don't fight the browser preload scanner", "https://web.dev/articles/preload-scanner")
WEBDEV_OPTIMIZE_LCP = ("web.dev — Optimize Largest Contentful Paint", "https://web.dev/articles/optimize-lcp")
WEBDEV_FETCHPRIORITY = ("web.dev — Optimize resource loading with the Fetch Priority API", "https://web.dev/articles/fetch-priority")

QUESTIONS = [
    # ------------------------------------------------------------------ html-001
    Q(
        id="html-001", sub="Semantic HTML", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["semantic-html", "landmarks", "accessibility", "seo"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""What is semantic HTML, and which landmark elements would you use to structure a typical web page?""",
        q_bn=r"""Semantic HTML কী? একটা সাধারণ web page-এর structure তৈরি করতে তুমি কোন কোন landmark element ব্যবহার করবে?""",
        a_en=r"""
            Semantic HTML means picking elements for their **meaning**, not their look: `<button>` for actions, `<a href>` for navigation, `<h1>`–`<h6>` for headings, `<ul>` for lists, and so on. Browsers, screen readers and search engines all read that meaning.

            For page structure I use the landmark elements:
            - `<header>` — site banner (logo, search)
            - `<nav>` — major navigation blocks
            - `<main>` — the primary content, only one visible per page
            - `<aside>` — complementary content such as filters or related products
            - `<footer>` — site info, copyright, contact
            - `<article>` for self-contained items (a blog post, a product card, a comment) and `<section>` for a themed group with its own heading

            Screen-reader users jump between landmarks and headings, so this structure is basically their table of contents. A page built only from `<div>`s ("div soup") gives them nothing to navigate.
        """,
        a_bn=r"""
            Semantic HTML মানে element বেছে নেওয়া তার **অর্থ** দেখে, চেহারা দেখে নয়: action-এর জন্য `<button>`, navigation-এর জন্য `<a href>`, heading-এর জন্য `<h1>`–`<h6>`, list-এর জন্য `<ul>` ইত্যাদি। Browser, screen reader আর search engine — সবাই এই অর্থটা পড়ে।

            Page structure-এর জন্য আমি landmark element ব্যবহার করি:
            - `<header>` — site banner (logo, search)
            - `<nav>` — প্রধান navigation block
            - `<main>` — page-এর মূল content, প্রতি page-এ একটাই visible `<main>` থাকবে
            - `<aside>` — পাশের সহায়ক content, যেমন filter বা related product
            - `<footer>` — site info, copyright, যোগাযোগ
            - স্বয়ংসম্পূর্ণ item-এর (blog post, product card, comment) জন্য `<article>`, আর নিজস্ব heading-সহ একটা বিষয়ভিত্তিক অংশের জন্য `<section>`

            Screen reader user-রা landmark আর heading ধরে ধরে page-এ ঘোরাফেরা করে, তাই এই structure-টাই তাদের কাছে সূচিপত্রের মতো কাজ করে। শুধু `<div>` দিয়ে বানানো page ("div soup") তাদের navigate করার কিছুই দেয় না।
        """,
        ex_en=r"""
            - **Accessibility:** landmarks map to ARIA roles automatically (`<nav>` → `navigation`, `<main>` → `main`). `<header>`/`<footer>` only become `banner`/`contentinfo` when they are not nested inside `<article>`, `<aside>`, `<main>`, `<nav>` or `<section>`.
            - **`<section>` is not a generic wrapper.** It's exposed as a `region` landmark only when it has an accessible name (for example `aria-labelledby` pointing to its heading). For pure styling hooks, `<div>` is still the right element.
            - **Headings are what matter, not nesting.** The old "document outline algorithm" (where every `<section>` restarts at `<h1>`) was never implemented by browsers and has been removed from the HTML Standard. Use a logical `h1` → `h2` → `h3` hierarchy.
            - **SEO and tooling:** search engines, reader modes and browser extensions use semantics to find the main content. You also get built-in behaviour for free — e.g. `<button>` is focusable and keyboard-activatable without extra code.
        """,
        ex_bn=r"""
            - **Accessibility:** landmark element নিজে থেকেই ARIA role-এ map হয় (`<nav>` → `navigation`, `<main>` → `main`)। তবে `<header>`/`<footer>` তখনই `banner`/`contentinfo` হয়, যখন সেগুলো `<article>`, `<aside>`, `<main>`, `<nav>` বা `<section>`-এর ভেতরে থাকে না।
            - **`<section>` কোনো generic wrapper নয়।** এর accessible name থাকলে (যেমন heading-কে `aria-labelledby` দিয়ে নির্দেশ করলে) তবেই এটা `region` landmark হিসেবে expose হয়। শুধু styling-এর hook দরকার হলে `<div>`-ই সঠিক element।
            - **Nesting নয়, heading-ই আসল।** পুরোনো "document outline algorithm" (যেখানে প্রতিটা `<section>`-এ আবার `<h1>` থেকে শুরু হতো) কোনো browser কখনো implement করেনি, এবং HTML Standard থেকে এটা সরিয়ে ফেলা হয়েছে। তাই `h1` → `h2` → `h3` — এভাবে যৌক্তিক heading hierarchy রাখো।
            - **SEO ও tooling:** search engine, reader mode আর browser extension main content খুঁজে বের করতে semantics ব্যবহার করে। পাশাপাশি built-in behaviour-ও ফ্রি পাও — যেমন `<button>` বাড়তি code ছাড়াই focusable ও keyboard দিয়ে চালানো যায়।
        """,
        tip_en=r"""Define it in one sentence ("elements chosen for meaning"), then name the landmarks and immediately connect them to a real user benefit — screen-reader navigation. Mentioning that the outline algorithm was removed is a nice signal that your knowledge is current.""",
        tip_bn=r"""এক বাক্যে সংজ্ঞা দাও ("অর্থ দেখে element বেছে নেওয়া"), তারপর landmark-গুলোর নাম বলো এবং সঙ্গে সঙ্গে একটা বাস্তব সুবিধার সাথে যুক্ত করো — screen reader navigation। Outline algorithm যে spec থেকে বাদ পড়েছে, সেটা উল্লেখ করলে বোঝা যায় তোমার জ্ঞান up-to-date।""",
        mist_en=r"""Wrapping everything in `<section>` "because it's semantic", using several visible `<main>` elements, or choosing heading levels by font size (`<h4>` because it looks smaller) instead of document hierarchy.""",
        mist_bn=r""""Semantic" ভেবে সবকিছু `<section>` দিয়ে wrap করা, একাধিক visible `<main>` রাখা, অথবা document hierarchy না দেখে font size দেখে heading level বেছে নেওয়া (ছোট দেখায় বলে `<h4>`)।""",
        code=r"""
            <body>
              <header>
                <a href="/"><img src="/logo.svg" alt="Dokan — home"></a>
                <form role="search" action="/search">
                  <label for="q">Search products</label>
                  <input id="q" name="q" type="search">
                </form>
              </header>

              <nav aria-label="Main">
                <ul>
                  <li><a href="/men">Men</a></li>
                  <li><a href="/women">Women</a></li>
                </ul>
              </nav>

              <main>
                <h1>Eid Collection</h1>
                <article class="product-card">
                  <h2>Cotton Panjabi — Navy</h2>
                  <p>৳1,850</p>
                </article>
              </main>

              <aside aria-label="Filters">...</aside>
              <footer>© 2026 Dokan</footer>
            </body>
        """,
        lang="html",
        follow=[
            ("When is a `<section>` exposed as a landmark?", "কখন একটা `<section>` landmark হিসেবে expose হয়?"),
            ("Can a page have more than one `<nav>`? How do you tell them apart?", "একটা page-এ কি একাধিক `<nav>` থাকতে পারে? সেগুলো আলাদা করবে কীভাবে?"),
        ],
        related=["html-011", "html-022"],
        refs=[MDN_ELEMENTS, MDN_MAIN],
    ),
    # ------------------------------------------------------------------ html-002
    Q(
        id="html-002", sub="Document Structure", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["doctype", "meta-charset", "viewport", "lang", "document-structure"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""Walk me through a minimal HTML document. What do `<!DOCTYPE html>`, the `lang` attribute, `<meta charset>` and the viewport meta tag actually do?""",
        q_bn=r"""একটা minimal HTML document ব্যাখ্যা করো। `<!DOCTYPE html>`, `lang` attribute, `<meta charset>` আর viewport meta tag আসলে কী কাজ করে?""",
        a_en=r"""
            - `<!DOCTYPE html>` switches the browser into **standards mode**. Without it the page renders in quirks mode, which emulates old browser layout bugs.
            - `<html lang="en">` (or `lang="bn"` for a Bangla page) tells screen readers which pronunciation rules to use, and helps translation tools, hyphenation and font selection.
            - `<meta charset="utf-8">` declares the character encoding. It must be within the first 1024 bytes, so I put it first in `<head>`. If the encoding is wrong, Bangla text like "বাংলা" turns into garbage characters.
            - `<meta name="viewport" content="width=device-width, initial-scale=1">` tells mobile browsers to use the device width as the layout width instead of a desktop-sized virtual viewport (typically around 980px). Without it, media queries don't work as expected on phones.
            - `<title>` is required — it's used for the tab, bookmarks, search results and is the first thing a screen reader announces.
        """,
        a_bn=r"""
            - `<!DOCTYPE html>` browser-কে **standards mode**-এ নিয়ে যায়। এটা না থাকলে page quirks mode-এ render হয়, যেখানে পুরোনো browser-এর layout bug-গুলো নকল করা হয়।
            - `<html lang="en">` (Bangla page হলে `lang="bn"`) screen reader-কে বলে দেয় কোন উচ্চারণ নিয়ম ব্যবহার করতে হবে। Translation tool, hyphenation আর font বাছাইয়েও এটা কাজে লাগে।
            - `<meta charset="utf-8">` character encoding ঘোষণা করে। এটাকে document-এর প্রথম 1024 byte-এর মধ্যে থাকতে হয়, তাই আমি এটা `<head>`-এর একদম শুরুতে রাখি। Encoding ভুল হলে "বাংলা"-র মতো Bangla text হিজিবিজি character-এ পরিণত হয়।
            - `<meta name="viewport" content="width=device-width, initial-scale=1">` mobile browser-কে বলে, desktop মাপের virtual viewport (সাধারণত প্রায় 980px) নয়, বরং device-এর width-কেই layout width হিসেবে ধরতে। এটা না দিলে phone-এ media query ঠিকমতো কাজ করে না।
            - `<title>` বাধ্যতামূলক — tab, bookmark, search result-এ এটাই দেখায়, আর screen reader সবার আগে এটাই পড়ে শোনায়।
        """,
        ex_en=r"""
            - **Encoding precedence:** a byte-order mark beats the HTTP `Content-Type: text/html; charset=utf-8` header, which beats `<meta charset>`. Ideally send the header *and* keep the meta tag (useful when the file is saved or opened locally).
            - **Quirks mode** affects things like percentage heights and some table/inline layout details, so CSS that "works" in quirks mode can break later. Any doctype other than `<!DOCTYPE html>` (or a missing one) is a red flag.
            - **Don't block zoom:** `user-scalable=no` or `maximum-scale=1` stops people with low vision from zooming. iOS Safari ignores it and other browsers offer a "force enable zoom" accessibility setting, but many users never find that setting and accessibility audits flag it.
            - **`lang` on parts of a page:** a mixed-language page can mark sections, e.g. `<p lang="en">` inside a `lang="bn"` document, so screen readers switch voices correctly.
        """,
        ex_bn=r"""
            - **Encoding-এর অগ্রাধিকার:** byte-order mark সবার আগে, তারপর HTTP `Content-Type: text/html; charset=utf-8` header, তারপর `<meta charset>`। সবচেয়ে ভালো হলো header পাঠানো *এবং* meta tag-ও রাখা (file save করে local-এ খুললে কাজে লাগে)।
            - **Quirks mode** percentage height আর কিছু table/inline layout-এর আচরণ বদলে দেয়, ফলে quirks mode-এ "কাজ করা" CSS পরে ভেঙে যেতে পারে। `<!DOCTYPE html>` ছাড়া অন্য কোনো doctype (বা doctype না থাকা) একটা সতর্কসংকেত।
            - **Zoom বন্ধ কোরো না:** `user-scalable=no` বা `maximum-scale=1` দিলে যারা চোখে কম দেখে তারা zoom করতে পারে না। iOS Safari এটা উপেক্ষা করে আর অন্য browser-এ "force enable zoom" ধরনের accessibility setting থাকে, কিন্তু অনেক user সেই setting খুঁজেই পায় না, আর accessibility audit-এ এটা ধরা পড়ে।
            - **Page-এর অংশবিশেষে `lang`:** একাধিক ভাষার page-এ আলাদা অংশ চিহ্নিত করা যায়, যেমন `lang="bn"` document-এর ভেতরে `<p lang="en">` — তাহলে screen reader সঠিকভাবে voice বদলাতে পারে।
        """,
        tip_en=r"""Go top to bottom through the skeleton and give one concrete consequence for each line ("without the viewport tag, my media queries don't fire on phones"). For a Bangladeshi product, mentioning `lang="bn"` and UTF-8 for Bangla text shows practical experience.""",
        tip_bn=r"""Skeleton-টা উপর থেকে নিচে ধরে এগোও, আর প্রতিটা line-এর জন্য একটা বাস্তব ফলাফল বলো ("viewport tag না দিলে phone-এ আমার media query কাজ করে না")। বাংলাদেশি product-এর ক্ষেত্রে `lang="bn"` আর Bangla text-এর জন্য UTF-8-এর কথা বললে বোঝা যায় তোমার হাতে-কলমে অভিজ্ঞতা আছে।""",
        mist_en=r"""Putting `<meta charset>` after a large `<style>` block or third-party scripts, forgetting `lang`, and adding `user-scalable=no` "to stop iOS zoom on inputs" (fix that with a 16px input font size instead).""",
        mist_bn=r"""বড় `<style>` block বা third-party script-এর পরে `<meta charset>` রাখা, `lang` দিতে ভুলে যাওয়া, আর "iOS-এ input-এ zoom থামাতে" `user-scalable=no` দেওয়া (এর সঠিক সমাধান হলো input-এর font size 16px রাখা)।""",
        code=r"""
            <!DOCTYPE html>
            <html lang="bn">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>অর্ডার ট্র্যাকিং — Dokan</title>
              <meta name="description" content="আপনার অর্ডার এখন কোথায় আছে দেখুন">
              <link rel="stylesheet" href="/css/main.css">
              <script src="/js/app.js" defer></script>
            </head>
            <body>
              <main>
                <h1>অর্ডার ট্র্যাকিং</h1>
                <p lang="en">Order ID: DK-2026-0042</p>
              </main>
            </body>
            </html>
        """,
        lang="html",
        follow=[
            ("What is quirks mode and how can you detect it from JavaScript?", "Quirks mode কী, আর JavaScript থেকে কীভাবে বুঝবে page quirks mode-এ আছে?"),
            ("Why must `<meta charset>` appear early in the document?", "`<meta charset>` কেন document-এর শুরুর দিকে থাকতে হয়?"),
        ],
        related=["html-001", "html-017"],
        refs=[MDN_META, MDN_HTML_EL],
    ),
    # ------------------------------------------------------------------ html-003
    Q(
        id="html-003", sub="Semantic HTML", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["button", "links", "semantics", "accessibility"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""On a product listing page, a "Load more" control fetches the next 20 products with JavaScript and appends them. The URL does not change. Which markup is the best choice?""",
        q_bn=r"""একটা product listing page-এ "Load more" control JavaScript দিয়ে পরের 20টা product এনে list-এর শেষে যোগ করে। URL বদলায় না। কোন markup সবচেয়ে উপযুক্ত?""",
        options=[
            (r"""`<a href="#" onclick="loadMore()">Load more</a>`""", r"""`<a href="#" onclick="loadMore()">Load more</a>`"""),
            (r"""`<button type="button">Load more</button>` with a click listener""", r"""click listener-সহ `<button type="button">Load more</button>`"""),
            (r"""`<div class="btn" onclick="loadMore()">Load more</div>`""", r"""`<div class="btn" onclick="loadMore()">Load more</div>`"""),
            (r"""`<a href="javascript:void(0)" role="button">Load more</a>`""", r"""`<a href="javascript:void(0)" role="button">Load more</a>`"""),
        ],
        correct=1,
        a_en=r"""
            `<button type="button">`. The rule of thumb: if it **navigates** to a URL, use `<a href>`; if it **performs an action** on the current page, use `<button>`. "Load more" without a URL change is an action.
        """,
        a_bn=r"""
            `<button type="button">`। সহজ নিয়ম: যদি এটা কোনো URL-এ **navigate** করে, তাহলে `<a href>`; আর যদি বর্তমান page-এ কোনো **action** করে, তাহলে `<button>`। URL না বদলে "Load more" করা একটা action।
        """,
        ex_en=r"""
            A native `<button>` is focusable, activates with both Enter and Space, is announced as "button" by screen readers, supports `disabled`, and `type="button"` stops it from accidentally submitting a surrounding form.

            The most tempting wrong answer is the `<a href="#">` version: it works with a mouse, but screen readers announce "link" (users expect navigation), Space doesn't activate links, `#` scrolls to the top or adds a history entry if you forget `preventDefault()`, and "open in new tab" gives a useless page. Adding `role="button"` (option D) fixes the announcement but you'd still need to hand-code Space-key handling — the first rule of ARIA says use the native element instead. The `<div>` isn't even keyboard-focusable.

            Flip side: if "Load more" changed the URL to `?page=2` and should be shareable or crawlable, a real link (`<a href="?page=2">`) enhanced with JavaScript would be the better choice.
        """,
        ex_bn=r"""
            Native `<button>` নিজে থেকেই focusable, Enter আর Space দুটো key দিয়েই চালানো যায়, screen reader একে "button" হিসেবে পড়ে, `disabled` support করে, আর `type="button"` দিলে আশেপাশের form ভুল করে submit হয় না।

            সবচেয়ে প্রলোভনজনক ভুল উত্তর হলো `<a href="#">`: mouse দিয়ে কাজ করে ঠিকই, কিন্তু screen reader বলে "link" (user ভাবে অন্য page-এ যাবে), Space দিয়ে link চালানো যায় না, `preventDefault()` ভুলে গেলে `#` page-এর উপরে scroll করে বা history-তে entry যোগ করে, আর "open in new tab" করলে অর্থহীন page খোলে। Option D-তে `role="button"` দিলে announcement ঠিক হয়, কিন্তু Space key-এর handling তখনো হাতে লিখতে হবে — ARIA-র প্রথম নিয়মই বলে native element ব্যবহার করো। আর `<div>` তো keyboard দিয়ে focus-ই করা যায় না।

            উল্টো দিকটাও ভাবো: "Load more" যদি URL বদলে `?page=2` করত এবং সেটা share বা crawl করার মতো হওয়া দরকার হতো, তাহলে JavaScript দিয়ে enhance করা একটা আসল link (`<a href="?page=2">`) বেশি ভালো হতো।
        """,
        tip_en=r"""State the navigate-vs-action rule first, then list two or three concrete things a `<button>` gives you for free. Mentioning the "real link for paginated, crawlable pages" exception shows nuance.""",
        tip_bn=r"""প্রথমে navigate বনাম action নিয়মটা বলো, তারপর `<button>` ফ্রিতে কী কী দেয় তার দুই-তিনটা উদাহরণ দাও। "Paginated ও crawlable page-এর জন্য আসল link" — এই ব্যতিক্রমটা বললে তোমার সূক্ষ্ম বোঝাপড়া বোঝা যায়।""",
        refs=[MDN_BUTTON, MDN_A],
    ),
    # ------------------------------------------------------------------ html-012
    Q(
        id="html-012", sub="Script Loading", diff="medium", type="comparison",
        prio="high", market="both", mins=5,
        tags=["defer", "async", "module", "script-loading", "performance"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""Compare a plain `<script src>`, `<script defer>`, `<script async>` and `<script type="module">`. How does each affect parsing and execution order, and when would you use each?""",
        q_bn=r"""সাধারণ `<script src>`, `<script defer>`, `<script async>` আর `<script type="module">` তুলনা করো। প্রতিটা parsing ও execution order-এ কী প্রভাব ফেলে, আর কখন কোনটা ব্যবহার করবে?""",
        a_en=r"""
            - **Plain classic script:** the parser stops, the file is downloaded (if not cached) and executed, then parsing continues. It's parser-blocking, so I avoid it in `<head>`.
            - **`defer`:** downloads in parallel while the HTML is parsed, then executes **after parsing finishes, in document order**, before `DOMContentLoaded`. This is my default for app code that touches the DOM or depends on another script.
            - **`async`:** downloads in parallel and executes **as soon as it arrives** — it can interrupt parsing, order isn't guaranteed, and `DOMContentLoaded` doesn't wait for it. Good for independent scripts like analytics.
            - **`type="module"`:** deferred by default (even inline modules), runs in strict mode with its own scope, supports `import`/`export`, is fetched with CORS and executes only once. Adding `async` makes it run as soon as it and its imports are ready.

            So: `defer` or modules for my own code, `async` only for scripts that depend on nothing and that nothing depends on.
        """,
        a_bn=r"""
            - **সাধারণ classic script:** parser থেমে যায়, file download হয় (cache-এ না থাকলে) ও execute হয়, তারপর আবার parsing চলে। এটা parser-blocking, তাই `<head>`-এ আমি এটা এড়িয়ে চলি।
            - **`defer`:** HTML parse হওয়ার সময় সমান্তরালে download হয়, আর **parsing শেষ হওয়ার পরে, document-এর ক্রম অনুযায়ী** `DOMContentLoaded`-এর আগে execute হয়। DOM ব্যবহার করে বা অন্য script-এর উপর নির্ভরশীল app code-এর জন্য এটাই আমার default।
            - **`async`:** সমান্তরালে download হয় এবং **পৌঁছানোমাত্র execute হয়** — parsing-এর মাঝখানে থামিয়ে দিতে পারে, ক্রমের নিশ্চয়তা নেই, আর `DOMContentLoaded` এর জন্য অপেক্ষা করে না। Analytics-এর মতো স্বাধীন script-এর জন্য ভালো।
            - **`type="module"`:** default-ভাবেই deferred (inline module-ও), strict mode-এ নিজস্ব scope-এ চলে, `import`/`export` support করে, CORS দিয়ে fetch হয় আর একবারই execute হয়। `async` যোগ করলে module আর তার import-গুলো ready হওয়ামাত্র চলে।

            তাই: নিজের code-এর জন্য `defer` বা module, আর `async` শুধু সেই script-এর জন্য যেটা কারও উপর নির্ভর করে না এবং কেউ যার উপর নির্ভর করে না।
        """,
        ex_en=r"""
            - `defer` and `async` are **ignored on inline classic scripts** (no `src`). Inline *module* scripts, however, are deferred, and `async` works on them.
            - `defer` has no effect on module scripts — they're already deferred.
            - Scripts inserted with `document.createElement('script')` behave like `async` by default; set `script.async = false` if you need insertion order.
            - A classic blocking script that comes after a stylesheet waits for that stylesheet to load (it might read computed styles), so CSS can indirectly delay parsing.
            - Deep `import` chains create request waterfalls. Bundling, or `<link rel="modulepreload">` for critical modules, fixes that.
            - `nomodule` fallbacks are a legacy pattern for very old browsers; most projects no longer need them.
        """,
        ex_bn=r"""
            - **Inline classic script-এ** (যার `src` নেই) `defer` আর `async` **উপেক্ষিত হয়**। তবে inline *module* script deferred থাকে, আর তাতে `async` কাজ করে।
            - Module script-এ `defer`-এর কোনো প্রভাব নেই — সেগুলো এমনিতেই deferred।
            - `document.createElement('script')` দিয়ে যোগ করা script default-ভাবে `async`-এর মতো আচরণ করে; insert করার ক্রম বজায় রাখতে চাইলে `script.async = false` দাও।
            - কোনো stylesheet-এর পরে থাকা blocking classic script ওই stylesheet load হওয়া পর্যন্ত অপেক্ষা করে (কারণ script computed style পড়তে পারে), তাই CSS পরোক্ষভাবে parsing দেরি করাতে পারে।
            - গভীর `import` chain request-এর waterfall তৈরি করে। Bundling, বা গুরুত্বপূর্ণ module-এর জন্য `<link rel="modulepreload">`, এই সমস্যা মেটায়।
            - `nomodule` fallback খুব পুরোনো browser-এর জন্য একটা legacy pattern; বেশিরভাগ project-এ এখন এর দরকার নেই।
        """,
        tip_en=r"""Draw (or describe) a timeline: HTML parsing on one line, download and execution bars for each attribute. Then finish with your default choice and why — interviewers want the decision, not just the definitions.""",
        tip_bn=r"""একটা timeline এঁকে (বা মুখে বর্ণনা করে) দেখাও: এক লাইনে HTML parsing, আর প্রতিটা attribute-এর জন্য download ও execution-এর bar। শেষে তোমার default পছন্দ আর তার কারণ বলো — interviewer শুধু সংজ্ঞা নয়, তোমার সিদ্ধান্তটা শুনতে চায়।""",
        mist_en=r"""Believing `async` preserves order, adding `defer` to inline scripts, or adding `defer` to `type="module"` thinking it's needed.""",
        mist_bn=r"""`async` ক্রম বজায় রাখে বলে মনে করা, inline script-এ `defer` দেওয়া, বা দরকার ভেবে `type="module"`-এ `defer` যোগ করা।""",
        code=r"""
            <head>
              <!-- Parser-blocking: avoid in <head> -->
              <script src="/legacy-widget.js"></script>

              <!-- Runs after parsing, in this order: vendor.js then app.js -->
              <script src="/vendor.js" defer></script>
              <script src="/app.js" defer></script>

              <!-- Independent: runs whenever it arrives -->
              <script src="https://analytics.example/tag.js" async></script>

              <!-- Deferred automatically; strict mode; own scope -->
              <script type="module" src="/main.mjs"></script>
              <link rel="modulepreload" href="/cart.mjs">
            </head>
        """,
        lang="html",
        follow=[
            ("Does `DOMContentLoaded` wait for `async` scripts? For module scripts?", "`DOMContentLoaded` কি `async` script-এর জন্য অপেক্ষা করে? Module script-এর জন্য?"),
            ("Why might moving a script to the end of `<body>` still be slower than `defer` in `<head>`?", "Script-কে `<body>`-এর শেষে সরালেও কেন সেটা `<head>`-এ `defer` দেওয়ার চেয়ে ধীর হতে পারে?"),
        ],
        related=["html-023", "html-030"],
        refs=[MDN_SCRIPT, SPEC_SCRIPTING],
    ),
    # ------------------------------------------------------------------ html-013
    Q(
        id="html-013", sub="Forms and Validation", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["forms", "constraint-validation", "setcustomvalidity", "validation"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""
            Using only the browser's Constraint Validation API (no libraries), build a sign-up form where:
            - email is required and must be a valid email address,
            - the password must be at least 8 characters,
            - "Confirm password" must match the password, otherwise the field shows the message "Passwords do not match".

            The form must not submit while it's invalid. When it is valid, send the data with `fetch` instead of a full page reload. Explain which APIs you used.
        """,
        q_bn=r"""
            শুধু browser-এর Constraint Validation API ব্যবহার করে (কোনো library ছাড়া) একটা sign-up form বানাও, যেখানে:
            - email বাধ্যতামূলক এবং valid email address হতে হবে,
            - password কমপক্ষে 8 character-এর হতে হবে,
            - "Confirm password" অবশ্যই password-এর সাথে মিলতে হবে, না মিললে field-এ "Passwords do not match" message দেখাবে।

            Form invalid থাকা অবস্থায় submit হওয়া চলবে না। Valid হলে full page reload-এর বদলে `fetch` দিয়ে data পাঠাতে হবে। কোন কোন API ব্যবহার করলে তা ব্যাখ্যা করো।
        """,
        a_en=r"""
            I let HTML attributes handle the built-in rules — `type="email"` and `required` for the email, `required minlength="8"` for the password — and use `setCustomValidity()` for the one rule HTML can't express: matching passwords.

            `setCustomValidity('Passwords do not match')` marks the confirm field invalid (`validity.customError` becomes `true`); `setCustomValidity('')` clears it. I re-check on `input` events of **both** password fields, because the user might edit the first one after filling the second.

            Without `novalidate`, the browser validates before dispatching `submit`: if anything is invalid it shows the first error and the `submit` event never fires. So inside my `submit` handler I know the form is valid, and I just `preventDefault()` and send `new FormData(form)` with `fetch`. I also style fields with `:user-invalid` so errors only show after the user interacts.
        """,
        a_bn=r"""
            Built-in নিয়মগুলো আমি HTML attribute দিয়েই সামলাই — email-এর জন্য `type="email"` ও `required`, password-এর জন্য `required minlength="8"`। আর HTML দিয়ে যে নিয়মটা প্রকাশ করা যায় না — password মেলানো — তার জন্য `setCustomValidity()` ব্যবহার করি।

            `setCustomValidity('Passwords do not match')` confirm field-কে invalid করে দেয় (`validity.customError` তখন `true`); `setCustomValidity('')` দিলে error মুছে যায়। আমি **দুটো** password field-এর `input` event-এই আবার check করি, কারণ user দ্বিতীয়টা পূরণ করার পর প্রথমটা বদলাতে পারে।

            `novalidate` না থাকলে browser `submit` event পাঠানোর আগেই validation চালায়: কিছু invalid থাকলে প্রথম error দেখায় এবং `submit` event আর fire-ই হয় না। তাই `submit` handler-এর ভেতরে আমি নিশ্চিত যে form valid; শুধু `preventDefault()` করে `new FormData(form)` `fetch` দিয়ে পাঠাই। আর `:user-invalid` দিয়ে field style করি, যাতে user interact করার পরেই শুধু error দেখা যায়।
        """,
        ex_en=r"""
            - **Key APIs:** `element.validity` (a `ValidityState` with flags like `valueMissing`, `typeMismatch`, `tooShort`, `customError`, `valid`), `element.validationMessage`, `setCustomValidity()`, `form.checkValidity()` (returns a boolean and fires `invalid` events) and `form.reportValidity()` (same, but also shows the messages).
            - **`minlength` quirk:** `tooShort` only applies to values the user typed. If a script sets the value, it won't be flagged — another reason to validate on the server.
            - **Custom error is sticky:** a non-empty custom message keeps the field invalid until you set it back to `''`. Forgetting to clear it is the classic "form never submits" bug.
            - **`novalidate`:** add it when you want to render your own inline errors (better for screen readers and consistent styling). Then you call `checkValidity()` yourself in the `submit` handler and read `validity` to build messages.
            - **Server validation is still mandatory** — client-side checks are UX, not security.
            - **Complexity:** each check is constant work per input event.
        """,
        ex_bn=r"""
            - **মূল API-গুলো:** `element.validity` (`valueMissing`, `typeMismatch`, `tooShort`, `customError`, `valid`-এর মতো flag-সহ একটা `ValidityState`), `element.validationMessage`, `setCustomValidity()`, `form.checkValidity()` (boolean return করে আর `invalid` event fire করে) এবং `form.reportValidity()` (একই কাজ, সাথে message-ও দেখায়)।
            - **`minlength`-এর একটা খুঁটিনাটি:** `tooShort` শুধু user-এর type করা value-তে প্রযোজ্য। Script দিয়ে value set করলে সেটা ধরা পড়ে না — server-এ validation করার আরেকটা কারণ।
            - **Custom error আটকে থাকে:** খালি নয় এমন custom message দিলে, আবার `''` set না করা পর্যন্ত field invalid থাকে। এটা মুছতে ভুলে যাওয়াই সেই classic "form কখনো submit হয় না" bug।
            - **`novalidate`:** নিজের মতো inline error দেখাতে চাইলে এটা দাও (screen reader-এর জন্য ভালো, style-ও একরকম থাকে)। তখন `submit` handler-এ নিজে `checkValidity()` call করে `validity` পড়ে message বানাতে হবে।
            - **Server validation তবুও বাধ্যতামূলক** — client-side check হলো UX, security নয়।
            - **Complexity:** প্রতিটা input event-এ check-এর কাজ constant।
        """,
        tip_en=r"""Start with "HTML attributes first, JavaScript only for what attributes can't express". Interviewers like hearing that the `submit` event doesn't fire for an invalid form unless `novalidate` is set — many candidates don't know that.""",
        tip_bn=r"""শুরু করো এভাবে: "আগে HTML attribute, আর attribute দিয়ে যা বলা যায় না শুধু তার জন্য JavaScript"। `novalidate` না থাকলে invalid form-এর জন্য `submit` event fire-ই হয় না — এটা বললে interviewer খুশি হয়, কারণ অনেক candidate এটা জানে না।""",
        mist_en=r"""Only listening on the confirm field, never clearing the custom message, using `form.submit()` (which skips validation), or treating client-side validation as sufficient.""",
        mist_bn=r"""শুধু confirm field-এ listener দেওয়া, custom message কখনো না মোছা, `form.submit()` ব্যবহার করা (যেটা validation এড়িয়ে যায়), অথবা client-side validation-কেই যথেষ্ট মনে করা।""",
        code=r"""
            <form id="signup">
              <label for="email">Email</label>
              <input id="email" name="email" type="email" required autocomplete="email">

              <label for="password">Password</label>
              <input id="password" name="password" type="password"
                     required minlength="8" autocomplete="new-password">

              <label for="confirm">Confirm password</label>
              <input id="confirm" name="confirm" type="password"
                     required autocomplete="new-password">

              <button type="submit">Create account</button>
            </form>

            <style>
              input:user-invalid { border-color: #b00020; }
            </style>

            <script type="module">
              const form = document.getElementById('signup');
              const { password, confirm } = form.elements;

              function checkMatch() {
                const mismatch = confirm.value !== '' && confirm.value !== password.value;
                // Empty string = valid; any other string = invalid with that message
                confirm.setCustomValidity(mismatch ? 'Passwords do not match' : '');
              }

              password.addEventListener('input', checkMatch);
              confirm.addEventListener('input', checkMatch);

              form.addEventListener('submit', async (event) => {
                // Only reached when every constraint is satisfied
                event.preventDefault();
                const res = await fetch('/api/signup', { method: 'POST', body: new FormData(form) });
                if (!res.ok) {
                  // show a server-side error message here
                }
              });
            </script>
        """,
        lang="html", time="O(1) per input event", space="O(1)",
        follow=[
            ("How would you show inline, screen-reader-friendly errors instead of the browser's bubbles?", "Browser-এর bubble-এর বদলে screen reader-বান্ধব inline error কীভাবে দেখাবে?"),
            ("What's the difference between `checkValidity()` and `reportValidity()`?", "`checkValidity()` আর `reportValidity()`-এর পার্থক্য কী?"),
        ],
        related=["html-024", "html-028"],
        refs=[MDN_SETCUSTOM, MDN_VALIDITY],
    ),
    # ------------------------------------------------------------------ html-014
    Q(
        id="html-014", sub="HTML APIs", diff="medium", type="scenario",
        prio="high", market="both", mins=7,
        tags=["dialog", "modal", "accessibility", "focus-management", "invoker-commands"],
        ver="HTML Living Standard; <dialog> Baseline widely available; invoker commands Baseline newly available (Dec 2025)", vs=True, status="stable",
        q_en=r"""You need a "Delete this address?" confirmation modal in a checkout flow. How would you build it so it's accessible, and why would you use `<dialog>` instead of a custom `div`-based modal?""",
        q_bn=r"""Checkout flow-এ একটা "এই address delete করবেন?" confirmation modal লাগবে। এটাকে accessible করে কীভাবে বানাবে, আর custom `div`-ভিত্তিক modal-এর বদলে কেন `<dialog>` ব্যবহার করবে?""",
        a_en=r"""
            I'd use a native `<dialog>` opened **modally** — with `showModal()` or declaratively with `command="show-modal"`. That gives me, for free, things that are hard to get right in a `div` modal:
            - it's rendered in the **top layer**, so no `z-index` battles, plus a styleable `::backdrop`;
            - the rest of the page becomes **inert** — focus, clicks and screen readers can't escape behind it;
            - **Esc** closes it (firing a `cancel` event first);
            - it's exposed with the dialog role and as modal.

            My checklist:
            1. Name it: `aria-labelledby` pointing at its heading (and `aria-describedby` for the explanation).
            2. Initial focus: for a destructive action I put `autofocus` on **Cancel**, the safe choice.
            3. Buttons inside `<form method="dialog">` close it and set `dialog.returnValue`, which I read in the `close` event.
            4. Focus should go back to the button that opened it — browsers handle this for modal dialogs, but I test it, especially when the trigger gets re-rendered.
            5. Optional: stop background scroll with `body:has(dialog[open]) { overflow: hidden; }` and keep animations reduced-motion friendly.
        """,
        a_bn=r"""
            আমি native `<dialog>` ব্যবহার করব এবং সেটা **modal** হিসেবে খুলব — `showModal()` দিয়ে, অথবা declaratively `command="show-modal"` দিয়ে। এতে এমন কিছু জিনিস ফ্রিতে পাই, যেগুলো `div` modal-এ ঠিকঠাক করা কঠিন:
            - এটা **top layer**-এ render হয়, তাই `z-index` নিয়ে মারামারি নেই, সাথে style করা যায় এমন `::backdrop`;
            - page-এর বাকি অংশ **inert** হয়ে যায় — focus, click বা screen reader পেছনের content-এ যেতে পারে না;
            - **Esc** চাপলে বন্ধ হয় (আগে `cancel` event fire হয়);
            - এটা dialog role-সহ modal হিসেবে expose হয়।

            আমার checklist:
            1. নাম দেওয়া: `aria-labelledby` দিয়ে এর heading-কে নির্দেশ করা (আর ব্যাখ্যার জন্য `aria-describedby`)।
            2. শুরুর focus: destructive action-এর ক্ষেত্রে নিরাপদ বিকল্প **Cancel**-এ `autofocus` দিই।
            3. `<form method="dialog">`-এর ভেতরের button dialog বন্ধ করে আর `dialog.returnValue` set করে, যেটা আমি `close` event-এ পড়ি।
            4. বন্ধ হলে focus যে button দিয়ে খোলা হয়েছিল সেখানে ফেরত যাওয়া উচিত — modal dialog-এর ক্ষেত্রে browser এটা করে, তবুও আমি test করি, বিশেষ করে trigger যদি re-render হয়।
            5. চাইলে `body:has(dialog[open]) { overflow: hidden; }` দিয়ে পেছনের scroll বন্ধ করি, আর animation reduced-motion-বান্ধব রাখি।
        """,
        ex_en=r"""
            - **`show()` vs `showModal()`:** `show()` or the `open` attribute creates a *non-modal* dialog — no inert background, no top layer, Esc doesn't close it. For confirmations you almost always want `showModal()`.
            - **Stale `returnValue` trap:** Esc (or `close()` without an argument) does **not** reset `returnValue`. If the user clicked "Delete" last time and presses Esc this time, the old `"delete"` is still there. Reset it after reading, as in the example.
            - **Invoker commands** (`commandfor` + `command="show-modal"` / `"close"`) remove the click-handler boilerplate. They're Baseline newly available since December 2025, so for users on older browsers keep a small JavaScript fallback that calls `showModal()`.
            - **Not Baseline yet:** the `closedby` attribute (for light dismiss on modal dialogs) has limited availability — don't rely on it without a fallback.
            - A hand-rolled `div` modal needs a focus trap, `inert` or `aria-hidden` on the background, Esc handling, focus restore and z-index management — every one of those is a common source of accessibility bugs.
        """,
        ex_bn=r"""
            - **`show()` বনাম `showModal()`:** `show()` বা `open` attribute একটা *non-modal* dialog বানায় — পেছনের অংশ inert হয় না, top layer-এ যায় না, Esc চাপলেও বন্ধ হয় না। Confirmation-এর জন্য প্রায় সবসময় `showModal()`-ই চাই।
            - **পুরোনো `returnValue`-এর ফাঁদ:** Esc (বা argument ছাড়া `close()`) `returnValue` reset **করে না**। আগেরবার user "Delete" চেপে থাকলে আর এবার Esc চাপলে, পুরোনো `"delete"` value-টাই থেকে যায়। উদাহরণের মতো পড়ার পর এটা reset করো।
            - **Invoker command** (`commandfor` + `command="show-modal"` / `"close"`) click handler-এর boilerplate বাদ দেয়। এটা December 2025 থেকে Baseline newly available, তাই পুরোনো browser-এর user-দের জন্য `showModal()` call করে এমন ছোট একটা JavaScript fallback রাখো।
            - **এখনো Baseline নয়:** `closedby` attribute (modal dialog-এ light dismiss-এর জন্য) সীমিত support পায় — fallback ছাড়া এর উপর ভরসা কোরো না।
            - নিজের হাতে বানানো `div` modal-এ focus trap, পেছনের অংশে `inert` বা `aria-hidden`, Esc handling, focus ফেরত দেওয়া আর z-index সামলানো — সবই লাগে, আর এর প্রতিটাই accessibility bug-এর পরিচিত উৎস।
        """,
        tip_en=r"""Structure it as "what the platform gives me" then "what I still do myself". The stale-`returnValue` detail is the kind of production gotcha that makes an answer memorable.""",
        tip_bn=r"""উত্তরটা দুই ভাগে সাজাও: "platform আমাকে কী দেয়" আর "তারপরও আমি নিজে কী করি"। পুরোনো `returnValue`-এর মতো production-এর খুঁটিনাটি উত্তরকে মনে রাখার মতো করে তোলে।""",
        mist_en=r"""Opening with `dialog.show()` or `setAttribute('open', '')` and expecting modal behaviour, putting initial focus on the destructive button, or forgetting an accessible name.""",
        mist_bn=r"""`dialog.show()` বা `setAttribute('open', '')` দিয়ে খুলে modal আচরণ আশা করা, destructive button-এ প্রথম focus দেওয়া, অথবা accessible name দিতে ভুলে যাওয়া।""",
        code=r"""
            <button type="button" commandfor="confirm-delete" command="show-modal">
              Delete address
            </button>

            <dialog id="confirm-delete" aria-labelledby="confirm-title" aria-describedby="confirm-desc">
              <h2 id="confirm-title">Delete this address?</h2>
              <p id="confirm-desc">"House 12, Road 5, Dhanmondi" will be removed from your saved addresses.</p>
              <form method="dialog">
                <button value="cancel" autofocus>Cancel</button>
                <button value="delete">Delete</button>
              </form>
            </dialog>

            <script type="module">
              const dialog = document.getElementById('confirm-delete');

              dialog.addEventListener('close', () => {
                if (dialog.returnValue === 'delete') {
                  deleteAddress(); // app logic
                }
                dialog.returnValue = ''; // Esc does not reset it
              });
            </script>
        """,
        lang="html",
        follow=[
            ("How does `<dialog>` differ from the `popover` attribute?", "`<dialog>` আর `popover` attribute-এর মধ্যে পার্থক্য কী?"),
            ("How would you animate the dialog opening and closing?", "Dialog খোলা ও বন্ধ হওয়ার animation কীভাবে করবে?"),
        ],
        related=["html-015", "html-016"],
        refs=[MDN_DIALOG, MDN_INVOKERS],
    ),
    # ------------------------------------------------------------------ html-023
    Q(
        id="html-023", sub="Browser Parsing", diff="hard", type="conceptual",
        prio="high", market="both", mins=7,
        tags=["parsing", "render-blocking", "preload-scanner", "critical-rendering-path", "dom"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""Explain how the browser turns an HTML response into pixels. What is the difference between parser-blocking and render-blocking resources, and what does the preload scanner do?""",
        q_bn=r"""Browser কীভাবে একটা HTML response-কে screen-এর pixel-এ পরিণত করে, ব্যাখ্যা করো। Parser-blocking আর render-blocking resource-এর পার্থক্য কী, আর preload scanner কী করে?""",
        a_en=r"""
            The HTML is parsed **incrementally** as bytes stream in: bytes → characters (using the encoding) → tokens → DOM nodes via the tree-construction stage. In parallel, CSS is parsed into the CSSOM. The browser combines DOM and CSSOM to compute styles, then does **layout**, **paint** and **compositing**.

            - **Parser-blocking:** a classic `<script>` without `defer`/`async` stops the parser until it's downloaded and executed, because it could call `document.write()` or read the DOM built so far.
            - **Render-blocking:** stylesheets in `<head>` block the first render, so users don't see unstyled content. They don't stop the parser directly, but a blocking classic script placed after a stylesheet waits for it — so CSS can block parsing indirectly.
            - **Preload scanner:** a lightweight secondary parser that reads ahead in the raw HTML while the main parser is blocked and starts fetching `<img>`, `<script src>`, `<link rel="stylesheet">` and similar resources early.

            The practical lesson: anything the preload scanner can't see — CSS background images, fonts referenced from CSS, `@import`ed stylesheets, scripts injected by JavaScript — is discovered late. I keep critical resources in the HTML markup, or hint them with `preload`.
        """,
        a_bn=r"""
            Byte যেমন যেমন আসে, HTML তেমন তেমন **ধাপে ধাপে (incrementally)** parse হয়: byte → character (encoding অনুযায়ী) → token → tree-construction ধাপে DOM node। একই সাথে CSS parse হয়ে CSSOM তৈরি হয়। Browser DOM আর CSSOM মিলিয়ে style হিসাব করে, তারপর **layout**, **paint** আর **compositing** করে।

            - **Parser-blocking:** `defer`/`async` ছাড়া classic `<script>` download আর execute না হওয়া পর্যন্ত parser থামিয়ে রাখে, কারণ script `document.write()` call করতে পারে বা এখন পর্যন্ত তৈরি DOM পড়তে পারে।
            - **Render-blocking:** `<head>`-এর stylesheet প্রথম render আটকে রাখে, যাতে user style-ছাড়া content না দেখে। এটা সরাসরি parser থামায় না, কিন্তু stylesheet-এর পরে থাকা blocking classic script ওই stylesheet-এর জন্য অপেক্ষা করে — ফলে CSS পরোক্ষভাবে parsing আটকাতে পারে।
            - **Preload scanner:** একটা হালকা দ্বিতীয় parser, যেটা main parser আটকে থাকার সময় raw HTML-এ সামনে পড়ে যায় আর `<img>`, `<script src>`, `<link rel="stylesheet">` জাতীয় resource আগেভাগেই fetch করা শুরু করে।

            বাস্তব শিক্ষা: preload scanner যা দেখতে পায় না — CSS background image, CSS থেকে refer করা font, `@import` করা stylesheet, JavaScript দিয়ে inject করা script — সেগুলো দেরিতে খুঁজে পাওয়া যায়। তাই আমি গুরুত্বপূর্ণ resource HTML markup-এ রাখি, অথবা `preload` দিয়ে hint দিই।
        """,
        ex_en=r"""
            - **Why scripts block:** the parser can't know whether a script will inject markup, so it has to wait. `defer`, `async` and `type="module"` are promises that the script won't use `document.write()`, which lets parsing continue.
            - **Non-render-blocking CSS:** a stylesheet whose `media` doesn't match (for example `media="print"`) is still downloaded but at low priority and without blocking render.
            - **`DOMContentLoaded` vs `load`:** `DOMContentLoaded` fires after parsing and deferred/module scripts; `load` waits for images, stylesheets and iframes too.
            - **Streaming matters:** because parsing is incremental, a server that flushes `<head>` early lets CSS and preloads start while the body is still being generated.
            - **Long JavaScript tasks** during parsing delay everything after them — this shows up as a long gap between TTFB and First Contentful Paint in the DevTools Performance panel.
        """,
        ex_bn=r"""
            - **Script কেন block করে:** script markup inject করবে কি না, parser আগে থেকে জানতে পারে না, তাই তাকে অপেক্ষা করতে হয়। `defer`, `async` আর `type="module"` আসলে একটা প্রতিশ্রুতি যে script `document.write()` ব্যবহার করবে না, তাই parsing চলতে পারে।
            - **Render-blocking নয় এমন CSS:** যে stylesheet-এর `media` match করে না (যেমন `media="print"`), সেটাও download হয়, তবে কম priority-তে এবং render আটকায় না।
            - **`DOMContentLoaded` বনাম `load`:** `DOMContentLoaded` fire হয় parsing আর deferred/module script শেষ হওয়ার পর; `load` image, stylesheet, iframe-এর জন্যও অপেক্ষা করে।
            - **Streaming গুরুত্বপূর্ণ:** parsing যেহেতু incremental, server আগেভাগে `<head>` flush করলে body তৈরি হওয়ার সময়েই CSS আর preload শুরু হয়ে যায়।
            - Parsing-এর সময় **লম্বা JavaScript task** তার পরের সবকিছু দেরি করায় — DevTools Performance panel-এ এটা TTFB আর First Contentful Paint-এর মাঝে বড় ফাঁক হিসেবে দেখা যায়।
        """,
        tip_en=r"""Use the pipeline as your skeleton (bytes → DOM/CSSOM → style → layout → paint → composite), then hang the blocking rules on it. Ending with "so I keep my LCP image in an `<img>` tag, not a CSS background" turns theory into practice.""",
        tip_bn=r"""Pipeline-টাকে কাঠামো হিসেবে ধরো (byte → DOM/CSSOM → style → layout → paint → composite), তারপর blocking-এর নিয়মগুলো তার সাথে জুড়ে দাও। শেষে "তাই আমি LCP image CSS background-এ নয়, `<img>` tag-এ রাখি" বললে theory বাস্তব কাজে রূপ নেয়।""",
        mist_en=r"""Saying CSS blocks DOM parsing directly, believing the browser waits for the entire HTML before building the DOM, or not knowing about the preload scanner at all.""",
        mist_bn=r"""CSS সরাসরি DOM parsing আটকায় বলা, browser পুরো HTML পাওয়ার পরেই DOM বানায় বলে মনে করা, অথবা preload scanner সম্পর্কে একেবারেই না জানা।""",
        code=r"""
            <head>
              <link rel="stylesheet" href="/main.css">  <!-- render-blocking -->
              <script src="/legacy.js"></script>        <!-- parser-blocking; also waits for main.css -->
              <script src="/app.js" defer></script>     <!-- neither: runs after parsing -->
            </head>
            <body>
              <!-- Invisible to the preload scanner: found only after CSS/style is processed -->
              <div class="hero" style="background-image: url(/hero.jpg)"></div>

              <!-- Discovered early by the preload scanner -->
              <img src="/product.jpg" width="600" height="400" alt="Navy cotton panjabi">
            </body>
        """,
        lang="html",
        follow=[
            ("How would you make a hero image that's set as a CSS background load earlier?", "CSS background হিসেবে দেওয়া hero image কীভাবে আগে load করাবে?"),
            ("What does `document.write()` have to do with parser-blocking scripts?", "Parser-blocking script-এর সাথে `document.write()`-এর সম্পর্ক কী?"),
        ],
        related=["html-012", "html-030", "html-029"],
        refs=[SPEC_PARSING, WEBDEV_PRELOAD_SCANNER],
    ),
    # ------------------------------------------------------------------ html-030
    Q(
        id="html-030", sub="Performance", diff="extreme", type="architecture",
        prio="high", market="both", mins=20,
        tags=["critical-rendering-path", "lcp", "performance", "slow-network", "fonts", "images"],
        ver="HTML Living Standard; fetchpriority Baseline newly available (Oct 2024)", vs=True, status="stable",
        q_en=r"""Your e-commerce landing page targets users across Bangladesh, many on mid-range Android phones with slow or unstable mobile data. Field data shows a poor Largest Contentful Paint (around 6 s at the 75th percentile). Walk me through how you'd optimise the critical rendering path, from the HTML response to the first meaningful paint.""",
        q_bn=r"""তোমার e-commerce landing page-এর লক্ষ্য সারা বাংলাদেশের user, যাদের অনেকেই mid-range Android phone আর ধীর বা অস্থির mobile data ব্যবহার করে। Field data-তে Largest Contentful Paint খারাপ (75th percentile-এ প্রায় 6 s)। HTML response থেকে শুরু করে প্রথম অর্থবহ paint পর্যন্ত critical rendering path কীভাবে optimise করবে, ধাপে ধাপে বলো।""",
        a_en=r"""
            This is advanced, so I'd approach it as a measured project rather than a list of tricks.

            **1. Measure and break LCP down.** Use real-user data (CrUX or RUM with the `web-vitals` library), segmented by connection type and device. Split LCP into TTFB, resource load delay, resource load duration and render delay — each has different fixes.

            **2. Fast first byte.** Serve HTML from a CDN edge close to Bangladesh, cache it at the edge (static generation or short-lived edge caching), use Brotli, HTTP/2 or HTTP/3, and stream/flush `<head>` early.

            **3. Make the HTML self-sufficient.** Server-render the above-the-fold content; a client-rendered shell means LCP waits for JS download + execution + API calls on a slow CPU.

            **4. Unblock rendering.** Inline small critical CSS (aim to fit critical HTML + CSS in roughly the first 14 KB, one TCP round trip, where practical), load the rest without blocking, remove `@import` chains, `defer` all scripts, and load third-party widgets (chat, pixels) after the page is interactive.

            **5. Prioritise the LCP image.** A real `<img>` in the HTML (not a CSS background), never `loading="lazy"`, `fetchpriority="high"`, responsive `srcset`/`sizes`, AVIF/WebP via `<picture>`, explicit `width`/`height`. Preconnect to the image CDN or serve it same-origin.

            **6. Fonts.** Bangla web fonts are relatively large; subset them, use WOFF2 and `unicode-range`, `font-display: swap` (or `optional`), and preload only the one font used above the fold — or use a system stack for body text.

            **7. Repeat visits.** Hashed, immutable static assets with long cache lifetimes; a service worker for an app shell and offline fallback.

            **8. Guard it.** Performance budgets in CI (e.g. Lighthouse CI), and RUM alerts so a new marketing script can't silently undo the work.
        """,
        a_bn=r"""
            এটা advanced বিষয়, তাই আমি একে কিছু trick-এর তালিকা হিসেবে না দেখে মেপে-জুখে চালানো একটা project হিসেবে দেখব।

            **1. মাপো এবং LCP ভেঙে দেখো।** আসল user-এর data (CrUX, অথবা `web-vitals` library দিয়ে RUM) ব্যবহার করো, connection type আর device অনুযায়ী ভাগ করে। LCP-কে TTFB, resource load delay, resource load duration আর render delay — এই চার ভাগে ভাঙো; প্রতিটার সমাধান আলাদা।

            **2. দ্রুত প্রথম byte।** বাংলাদেশের কাছাকাছি CDN edge থেকে HTML serve করো, edge-এ cache করো (static generation বা অল্প সময়ের edge caching), Brotli, HTTP/2 বা HTTP/3 ব্যবহার করো, আর `<head>` আগেভাগে stream/flush করো।

            **3. HTML-কে স্বয়ংসম্পূর্ণ করো।** Above-the-fold content server-এ render করো; client-rendered shell হলে ধীর CPU-তে JS download + execution + API call শেষ হওয়া পর্যন্ত LCP আটকে থাকে।

            **4. Render-এর বাধা সরাও।** ছোট critical CSS inline করো (সম্ভব হলে critical HTML + CSS মোটামুটি প্রথম 14 KB-র মধ্যে, অর্থাৎ এক TCP round trip-এ রাখার চেষ্টা করো), বাকি CSS block না করে load করো, `@import` chain সরাও, সব script-এ `defer` দাও, আর third-party widget (chat, pixel) page interactive হওয়ার পরে load করো।

            **5. LCP image-কে অগ্রাধিকার দাও।** HTML-এ আসল `<img>` (CSS background নয়), কখনোই `loading="lazy"` নয়, `fetchpriority="high"`, responsive `srcset`/`sizes`, `<picture>` দিয়ে AVIF/WebP, আর স্পষ্ট `width`/`height`। Image CDN-এ preconnect করো, অথবা same-origin থেকে serve করো।

            **6. Font।** Bangla web font তুলনামূলক বড়; subset করো, WOFF2 আর `unicode-range` ব্যবহার করো, `font-display: swap` (বা `optional`) দাও, আর above-the-fold-এ ব্যবহৃত একটা font-ই শুধু preload করো — অথবা body text-এর জন্য system font stack ব্যবহার করো।

            **7. বারবার visit।** Hash-যুক্ত, immutable static asset লম্বা cache lifetime-সহ; app shell আর offline fallback-এর জন্য service worker।

            **8. পাহারা বসাও।** CI-তে performance budget (যেমন Lighthouse CI), আর RUM alert — যাতে নতুন কোনো marketing script চুপচাপ সব কাজ নষ্ট করে দিতে না পারে।
        """,
        ex_en=r"""
            **Trade-offs to discuss:**
            - Inlined CSS isn't cached separately, so it's re-downloaded on every page view; keep it small and page-type specific.
            - `preload` and `fetchpriority="high"` are zero-sum on a thin connection — preloading five things means none of them is prioritised. Use them for the one or two truly critical resources.
            - `font-display: optional` gives the best LCP/CLS but users on slow connections may never see the brand font on the first visit; `swap` shows it later but can cause a layout shift (mitigate with fallback font metric overrides like `size-adjust`).
            - The common "`media="print"` + `onload`" trick for async CSS uses an inline event handler, which a strict Content Security Policy blocks; a tiny deferred loader script is the CSP-friendly alternative.

            **Failure scenarios:** a CDN cache miss storm after a deploy (warm the cache), an A/B testing script that hides the page until it loads (anti-flicker snippets can add seconds), and a hero carousel that swaps the LCP element via JavaScript.

            **Why it matters in Bangladesh specifically:** high-latency, variable mobile connections punish every extra round trip, and mid-range devices make JavaScript execution — not just download — a bottleneck. Lab tests should use network *and* CPU throttling.
        """,
        ex_bn=r"""
            **যেসব trade-off নিয়ে আলোচনা করা উচিত:**
            - Inline করা CSS আলাদাভাবে cache হয় না, তাই প্রতিটা page view-এ আবার download হয়; এটাকে ছোট আর page-type অনুযায়ী নির্দিষ্ট রাখো।
            - পাতলা connection-এ `preload` আর `fetchpriority="high"` হলো zero-sum — পাঁচটা জিনিস preload করলে আসলে কোনোটাই অগ্রাধিকার পায় না। সত্যিকারের গুরুত্বপূর্ণ এক-দুইটা resource-এর জন্যই এগুলো ব্যবহার করো।
            - `font-display: optional` LCP/CLS-এর জন্য সবচেয়ে ভালো, কিন্তু ধীর connection-এর user প্রথম visit-এ brand font হয়তো দেখবেই না; `swap` পরে font দেখায় কিন্তু layout shift ঘটাতে পারে (`size-adjust`-এর মতো fallback font metric override দিয়ে এটা কমাও)।
            - Async CSS-এর জনপ্রিয় "`media="print"` + `onload`" trick একটা inline event handler ব্যবহার করে, যা strict Content Security Policy আটকে দেয়; CSP-বান্ধব বিকল্প হলো ছোট একটা deferred loader script।

            **ব্যর্থতার পরিস্থিতি:** deploy-এর পর CDN cache miss-এর ঝড় (cache আগে থেকে warm করো), A/B testing script যা load না হওয়া পর্যন্ত page লুকিয়ে রাখে (anti-flicker snippet কয়েক সেকেন্ড যোগ করতে পারে), আর hero carousel যা JavaScript দিয়ে LCP element বদলে দেয়।

            **বাংলাদেশে কেন বিশেষভাবে গুরুত্বপূর্ণ:** high-latency ও অনিশ্চিত mobile connection-এ প্রতিটা বাড়তি round trip-এর মাশুল দিতে হয়, আর mid-range device-এ শুধু download নয়, JavaScript execution-ও bottleneck। Lab test-এ network *আর* CPU — দুটোই throttle করা উচিত।
        """,
        tip_en=r"""Lead with measurement and the four LCP sub-parts — it shows you won't guess. Then go in request order (server → HTML → CSS/JS → image → fonts → caching) and name one trade-off per step. Tie it back to the audience: latency and CPU, not just bandwidth.""",
        tip_bn=r"""মাপজোখ আর LCP-র চারটা ভাগ দিয়ে শুরু করো — এতে বোঝা যায় তুমি আন্দাজে কাজ করো না। তারপর request-এর ক্রম ধরে এগোও (server → HTML → CSS/JS → image → font → caching), আর প্রতিটা ধাপে একটা করে trade-off বলো। শেষে audience-এর সাথে মিলিয়ে দাও: শুধু bandwidth নয়, latency আর CPU-ও।""",
        mist_en=r"""Lazy-loading the hero image, preloading everything, optimising only bundle size while the LCP image is discovered late, or testing only on a fast laptop on office Wi-Fi.""",
        mist_bn=r"""Hero image lazy-load করা, সবকিছু preload করা, LCP image দেরিতে খুঁজে পাওয়া যাচ্ছে অথচ শুধু bundle size optimise করা, অথবা শুধু অফিসের Wi-Fi-তে দ্রুত laptop-এ test করা।""",
        code=r"""
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>Eid Sale — Dokan</title>

              <link rel="preconnect" href="https://img.dokan-cdn.example">
              <link rel="preload" href="/fonts/bangla-ui-subset.woff2" as="font" type="font/woff2" crossorigin>

              <style>/* ~10 KB critical CSS: header, hero, first product row */</style>
              <link rel="stylesheet" href="/css/rest.4f9a1c.css" media="print" onload="this.media='all'">

              <script type="module" src="/js/app.8c2d.js"></script>
            </head>
            <body>
              <picture>
                <source type="image/avif"
                        srcset="https://img.dokan-cdn.example/hero-480.avif 480w,
                                https://img.dokan-cdn.example/hero-960.avif 960w"
                        sizes="100vw">
                <img src="https://img.dokan-cdn.example/hero-960.jpg"
                     srcset="https://img.dokan-cdn.example/hero-480.jpg 480w,
                             https://img.dokan-cdn.example/hero-960.jpg 960w"
                     sizes="100vw" width="960" height="540"
                     fetchpriority="high" alt="Eid sale: up to 40% off panjabis">
              </picture>
            </body>
        """,
        lang="html",
        follow=[
            ("How would you prove that your changes improved LCP for real users, not just in Lighthouse?", "শুধু Lighthouse-এ নয়, আসল user-দের জন্য LCP যে উন্নত হয়েছে তা কীভাবে প্রমাণ করবে?"),
            ("Marketing insists on a third-party chat widget on the landing page. How do you limit its impact?", "Marketing team landing page-এ একটা third-party chat widget রাখতে চায়। এর প্রভাব কীভাবে সীমিত রাখবে?"),
            ("When would SSG at the edge be a bad fit for this page?", "কখন edge-এ SSG এই page-এর জন্য উপযুক্ত হবে না?"),
        ],
        related=["html-023", "html-012", "html-018"],
        refs=[WEBDEV_OPTIMIZE_LCP, WEBDEV_FETCHPRIORITY, WEBDEV_PRELOAD_SCANNER],
    ),
]

if __name__ == "__main__":
    save("html", "b1", QUESTIONS)
