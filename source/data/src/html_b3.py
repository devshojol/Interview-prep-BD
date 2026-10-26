import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_GETATTRIBUTE = ("MDN — Element.getAttribute()", "https://developer.mozilla.org/en-US/docs/Web/API/Element/getAttribute")
MDN_INPUT = ("MDN — <input>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input")
MDN_BUTTON = ("MDN — <button>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button")
SPEC_IMPLICIT_SUBMIT = ("HTML Standard — Form submission (implicit submission)", "https://html.spec.whatwg.org/multipage/form-control-infrastructure.html")
SPEC_BOOLEAN = ("HTML Standard — Boolean attributes", "https://html.spec.whatwg.org/multipage/common-microsyntaxes.html")
MDN_DISABLED = ("MDN — HTML attribute: disabled", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/disabled")
MDN_IMG = ("MDN — <img>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img")
MDN_PICTURE = ("MDN — <picture>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/picture")
WEBDEV_RESPONSIVE_IMAGES = ("web.dev — Learn Responsive Design: Responsive images", "https://web.dev/learn/design/responsive-images")
MDN_TEMPLATE = ("MDN — <template>", "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/template")
MDN_REPLACECHILDREN = ("MDN — Element.replaceChildren()", "https://developer.mozilla.org/en-US/docs/Web/API/Element/replaceChildren")
W3C_ACCNAME = ("W3C — Accessible Name and Description Computation 1.2", "https://www.w3.org/TR/accname-1.2/")
WCAG_LABEL_IN_NAME = ("W3C WAI — Understanding SC 2.5.3 Label in Name", "https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html")
MDN_TRUSTED_TYPES = ("MDN — Trusted Types API", "https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API")
MDN_CSP = ("MDN — Content-Security-Policy header", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy")
OWASP_DOM_XSS = ("OWASP — DOM based XSS Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html")
APG_COMBOBOX = ("W3C WAI-ARIA APG — Combobox pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/combobox/")
MDN_ACTIVEDESCENDANT = ("MDN — aria-activedescendant", "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-activedescendant")

QUESTIONS = [
    # ------------------------------------------------------------------ html-007
    Q(
        id="html-007", sub="DOM Fundamentals", diff="easy", type="output",
        prio="high", market="bangladesh", mins=4,
        tags=["dom", "attributes", "properties", "output"],
        ver="HTML Living Standard / DOM Standard (version-independent)", vs=False, status="stable",
        q_en=r"""The page is served from `https://dokan.example/account/`. What does this code log?""",
        q_bn=r"""Page-টা `https://dokan.example/account/` থেকে serve হচ্ছে। এই code কী log করবে?""",
        a_en=r"""
            HTML **attributes** are the initial values written in the markup; DOM **properties** are the live state of the object.
            - After `input.value = 'Karim'`, the attribute still says `Rahim`, but the property is `Karim`.
            - Setting the `value` *attribute* afterwards only changes the **default value** (`defaultValue`). Because the value was already changed (the field is "dirty"), the current `value` stays `Karim`.
            - `getAttribute('href')` returns exactly what's written (`/orders`), while the `href` property returns the resolved absolute URL.
        """,
        a_bn=r"""
            HTML **attribute** হলো markup-এ লেখা শুরুর value; DOM **property** হলো object-এর বর্তমান (live) অবস্থা।
            - `input.value = 'Karim'` করার পরেও attribute-এ লেখা থাকে `Rahim`, কিন্তু property হয়ে যায় `Karim`।
            - এরপর `value` *attribute* বদলালে শুধু **default value** (`defaultValue`) বদলায়। Value যেহেতু আগেই বদলানো হয়েছে (field-টা "dirty"), বর্তমান `value` `Karim`-ই থাকে।
            - `getAttribute('href')` যা লেখা আছে ঠিক তাই দেয় (`/orders`), আর `href` property resolve করা absolute URL দেয়।
        """,
        quick_en=r"""`Rahim`, `Karim`, `Karim`, `Jamal`, `/orders`, `https://dokan.example/orders`. Attributes hold the initial markup values and properties the live state: setting the `value` attribute on an already-changed field only updates `defaultValue`, and `link.href` is the resolved URL.""",
        quick_bn=r"""Output: `Rahim`, `Karim`, `Karim`, `Jamal`, `/orders`, `https://dokan.example/orders`। Attribute হলো markup-এর শুরুর value, আর property হলো live state: আগেই বদলানো field-এ `value` attribute set করলে শুধু `defaultValue` বদলায়, আর `link.href` পুরো resolved URL দেয়।""",
        ex_en=r"""
            Line by line:
            1. `getAttribute('value')` → `Rahim` (markup untouched).
            2. `input.value` → `Karim` (live property).
            3. `setAttribute('value', 'Jamal')` updates the default; the dirty value flag (set when `input.value` was assigned) means `value` is still `Karim`.
            4. `defaultValue` reflects the attribute → `Jamal`.
            5. `getAttribute('href')` → `/orders`.
            6. `link.href` → resolved against the page URL → `https://dokan.example/orders`.

            Real-world consequences: "reset" buttons restore `defaultValue`; `el.checked` vs the `checked` attribute behaves the same way; frameworks set properties, not attributes, for form state; and `[value="x"]` CSS selectors match the attribute, not what the user typed.
        """,
        ex_bn=r"""
            Line ধরে ধরে:
            1. `getAttribute('value')` → `Rahim` (markup অপরিবর্তিত)।
            2. `input.value` → `Karim` (live property)।
            3. `setAttribute('value', 'Jamal')` শুধু default বদলায়; আগের ধাপে value বদলানোয় dirty flag set হয়ে গেছে, তাই `value` এখনো `Karim`।
            4. `defaultValue` attribute-কে প্রতিফলিত করে → `Jamal`।
            5. `getAttribute('href')` → `/orders`।
            6. `link.href` → page URL-এর সাপেক্ষে resolve হয়ে → `https://dokan.example/orders`।

            বাস্তব প্রভাব: "reset" button `defaultValue` ফিরিয়ে আনে; `el.checked` আর `checked` attribute-ও একইভাবে আচরণ করে; framework-গুলো form state-এর জন্য attribute নয়, property set করে; আর `[value="x"]` CSS selector user-এর type করা value নয়, attribute match করে।
        """,
        tip_en=r"""Open with the one-line distinction "attribute = initial markup, property = live state", then trace. Mentioning `defaultValue` and the resolved `href` shows you understand reflection, not just the trivia.""",
        tip_bn=r"""শুরুতেই এক লাইনে পার্থক্যটা বলো — "attribute = শুরুর markup, property = live state" — তারপর trace করো। `defaultValue` আর resolve হওয়া `href`-এর কথা বললে বোঝা যায় তুমি reflection বোঝো, শুধু খুঁটিনাটি মুখস্থ নয়।""",
        mist_en=r"""Assuming `setAttribute('value', …)` updates what the user sees after they've typed, or expecting `link.href` to return the relative path.""",
        mist_bn=r"""User type করার পরেও `setAttribute('value', …)` দিলে দেখানো value বদলাবে বলে ধরে নেওয়া, অথবা `link.href` relative path ফেরত দেবে বলে আশা করা।""",
        code=r"""
            <input id="name" value="Rahim">
            <a id="link" href="/orders">Orders</a>

            <script>
              const input = document.getElementById('name');
              const link = document.getElementById('link');

              input.value = 'Karim';
              console.log(input.getAttribute('value'));
              console.log(input.value);

              input.setAttribute('value', 'Jamal');
              console.log(input.value);
              console.log(input.defaultValue);

              console.log(link.getAttribute('href'));
              console.log(link.href);
            </script>
        """,
        lang="html",
        output=r"""
            Rahim
            Karim
            Karim
            Jamal
            /orders
            https://dokan.example/orders
        """,
        follow=[
            ("What happens if you call `form.reset()` after this code?", "এই code-এর পরে `form.reset()` call করলে কী হবে?"),
            ("Which attributes reflect to properties with a different name (e.g. `class`)?", "কোন কোন attribute ভিন্ন নামের property-তে reflect হয় (যেমন `class`)?"),
        ],
        related=["html-006", "html-009"],
        refs=[MDN_GETATTRIBUTE, MDN_INPUT],
    ),
    # ------------------------------------------------------------------ html-008
    Q(
        id="html-008", sub="Forms and Validation", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["forms", "button", "submit", "common-mistakes"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""In this checkout form, clicking "Apply coupon" reloads the page and submits the whole order instead of only checking the coupon. What is the cause?""",
        q_bn=r"""এই checkout form-এ "Apply coupon"-এ click করলে শুধু coupon check না হয়ে page reload হয় আর পুরো order submit হয়ে যায়। কারণ কী?""",
        code=r"""
            <form action="/orders" method="post">
              <label for="coupon">Coupon code</label>
              <input id="coupon" name="coupon">
              <button onclick="applyCoupon()">Apply coupon</button>

              <!-- ...address and payment fields... -->

              <button>Place order</button>
            </form>
        """,
        lang="html",
        options=[
            ("A `<button>` inside a form defaults to `type=\"submit\"`, so after the click handler runs, the form is submitted.",
             "Form-এর ভেতরের `<button>`-এর default `type` হলো `\"submit\"`, তাই click handler চলার পর form submit হয়ে যায়।"),
            ("Inline `onclick` handlers always cause a page reload; it must be attached with `addEventListener` instead.",
             "Inline `onclick` handler সবসময় page reload ঘটায়; এর বদলে `addEventListener` দিয়ে যুক্ত করতে হবে।"),
            ("The form is missing `novalidate`, so the browser submits it in order to validate the fields.",
             "Form-এ `novalidate` নেই, তাই field validate করার জন্য browser form submit করে দেয়।"),
            ("The coupon `<input>` has no `type`, which triggers implicit submission when a nearby button is clicked.",
             "Coupon `<input>`-এ কোনো `type` নেই, তাই পাশের button-এ click করলে implicit submission ঘটে।"),
        ],
        correct=0,
        a_en=r"""
            A `<button>` associated with a form defaults to `type="submit"` when the attribute is missing. The click handler runs, then the default action submits the form. The fix is `<button type="button">` for any button that isn't meant to submit.
        """,
        a_bn=r"""
            কোনো form-এর সাথে যুক্ত `<button>`-এ `type` না দিলে তার default হয় `type="submit"`। Click handler চলে, তারপর default action হিসেবে form submit হয়। সমাধান: যে button submit করার জন্য নয়, তাতে `<button type="button">` দাও।
        """,
        quick_en=r"""A `<button>` in a form defaults to `type="submit"`, so after the click handler runs, the whole form is submitted. Give buttons that shouldn't submit `type="button"`.""",
        quick_bn=r"""Form-এর ভেতরের `<button>`-এর default `type="submit"`, তাই click handler চলার পরে পুরো form submit হয়ে যায়। যে button submit করবে না, তাতে `type="button"` দাও।""",
        ex_en=r"""
            Option B is the tempting one because inline handlers *are* discouraged (and blocked by a strict CSP) — but switching to `addEventListener` alone changes nothing; the button is still a submit button. Calling `event.preventDefault()` would work, but `type="button"` states the intent in the markup.

            Option D mixes up a related behaviour: **implicit submission** happens when the user presses **Enter** inside a text field — the form is submitted via its default (first) submit button. That's a second bug here: pressing Enter in the coupon field will place the order even after you add `type="button"`. Handle Enter in that field, or move the coupon into its own `<form>` placed outside and associate controls with it using the `form="coupon-form"` attribute (forms can't be nested).
        """,
        ex_bn=r"""
            Option B প্রলোভনজনক, কারণ inline handler আসলেই নিরুৎসাহিত (আর strict CSP এগুলো আটকে দেয়) — কিন্তু শুধু `addEventListener`-এ গেলে কিছুই বদলায় না; button তখনো submit button-ই থাকে। `event.preventDefault()` দিলেও কাজ হবে, তবে `type="button"` markup-এই উদ্দেশ্যটা স্পষ্ট করে।

            Option D একটা সম্পর্কিত আচরণের সাথে গুলিয়ে ফেলেছে: **implicit submission** ঘটে যখন user কোনো text field-এ **Enter** চাপে — তখন form তার default (প্রথম) submit button দিয়ে submit হয়। এখানে এটা দ্বিতীয় একটা bug: `type="button"` দেওয়ার পরেও coupon field-এ Enter চাপলে order place হয়ে যাবে। ওই field-এ Enter আলাদাভাবে handle করো, অথবা coupon-এর জন্য বাইরে আলাদা একটা `<form>` রেখে `form="coupon-form"` attribute দিয়ে control-গুলো তার সাথে যুক্ত করো (form-এর ভেতরে form nest করা যায় না)।
        """,
        tip_en=r"""Give the fix (`type="button"`) in the first sentence, then mention the Enter-key implicit submission edge case — it shows you've debugged real checkout forms.""",
        tip_bn=r"""প্রথম বাক্যেই সমাধান (`type="button"`) বলো, তারপর Enter key-এর implicit submission-এর edge case উল্লেখ করো — এতে বোঝা যায় তুমি আসল checkout form debug করেছ।""",
        refs=[MDN_BUTTON, SPEC_IMPLICIT_SUBMIT],
    ),
    # ------------------------------------------------------------------ html-009
    Q(
        id="html-009", sub="HTML Attributes", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=2,
        tags=["boolean-attributes", "disabled", "attributes"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""What is the state of this button: `<button disabled="false">Pay now</button>`?""",
        q_bn=r"""এই button-এর অবস্থা কী: `<button disabled="false">Pay now</button>`?""",
        options=[
            ("Enabled, because the value of `disabled` is `\"false\"`.", "Enabled, কারণ `disabled`-এর value `\"false\"`।"),
            ("Disabled — for a boolean attribute, its presence means true, whatever the value is.", "Disabled — boolean attribute-এর ক্ষেত্রে value যাই হোক, attribute থাকা মানেই true।"),
            ("Enabled, because `\"false\"` is an invalid value and browsers drop invalid attributes.", "Enabled, কারণ `\"false\"` একটা invalid value আর browser invalid attribute বাদ দিয়ে দেয়।"),
            ("It depends on the browser: Chromium treats it as disabled, Firefox as enabled.", "Browser-এর উপর নির্ভর করে: Chromium একে disabled ধরে, Firefox enabled ধরে।"),
        ],
        correct=1,
        a_en=r"""
            It's **disabled**. `disabled` is a boolean attribute: if it's present, it's true — `disabled`, `disabled=""`, `disabled="disabled"` and even `disabled="false"` all disable the button. To enable it, **remove** the attribute (`btn.removeAttribute('disabled')` or `btn.disabled = false`).
        """,
        a_bn=r"""
            এটা **disabled**। `disabled` একটা boolean attribute: থাকলেই true — `disabled`, `disabled=""`, `disabled="disabled"`, এমনকি `disabled="false"` — সবগুলোই button disable করে। Enable করতে হলে attribute-টা **সরিয়ে ফেলতে** হবে (`btn.removeAttribute('disabled')` বা `btn.disabled = false`)।
        """,
        quick_en=r"""It's disabled: `disabled` is a boolean attribute, so its presence means true whatever the value, even `"false"`. To enable it, remove the attribute or set `btn.disabled = false`.""",
        quick_bn=r"""Button-টা disabled: `disabled` একটা boolean attribute, তাই value যাই হোক, এমনকি `"false"` হলেও, attribute থাকলেই true। Enable করতে attribute-টা সরাও বা `btn.disabled = false` দাও।""",
        ex_en=r"""
            The tempting answer is A, because the string reads like a value. But the HTML Standard defines boolean attributes by presence; the only valid values are the empty string or the attribute's own name, and any value still means "on". Browsers are consistent about this (so D is wrong), and they don't drop the attribute (C is wrong).

            The same trap appears in JavaScript: `btn.setAttribute('disabled', false)` *disables* the button, because the attribute now exists with the value `"false"`. Other boolean attributes behave the same: `hidden`, `required`, `checked`, `readonly`, `open`, `autofocus`.

            Don't confuse these with ARIA states such as `aria-expanded="false"` or `aria-hidden="false"`, which are real string values that matter. JSX libraries handle this for you: React omits `disabled` when you pass `disabled={false}`.
        """,
        ex_bn=r"""
            প্রলোভনজনক উত্তর A, কারণ string-টা value-র মতো শোনায়। কিন্তু HTML Standard boolean attribute-কে উপস্থিতি দিয়ে সংজ্ঞায়িত করে; valid value শুধু খালি string বা attribute-এর নিজের নাম, আর যেকোনো value থাকলেই মানে "on"। সব browser এ ব্যাপারে একমত (তাই D ভুল), আর তারা attribute বাদও দেয় না (C ভুল)।

            JavaScript-এও একই ফাঁদ আছে: `btn.setAttribute('disabled', false)` button-টাকে *disable* করে দেয়, কারণ attribute-টা এখন `"false"` value নিয়ে উপস্থিত। অন্য boolean attribute-ও একইরকম: `hidden`, `required`, `checked`, `readonly`, `open`, `autofocus`।

            এগুলোকে `aria-expanded="false"` বা `aria-hidden="false"`-এর মতো ARIA state-এর সাথে গুলিয়ে ফেলো না — ওগুলো আসল string value, আর সেগুলোর অর্থ আছে। JSX library এটা সামলে নেয়: React-এ `disabled={false}` দিলে `disabled` attribute বাদ পড়ে যায়।
        """,
        tip_en=r"""Say "presence, not value" and immediately give the JavaScript version of the trap (`setAttribute('disabled', false)`). That's the bug people actually ship.""",
        tip_bn=r"""বলো "value নয়, উপস্থিতি" — আর সঙ্গে সঙ্গে এই ফাঁদের JavaScript রূপটা দেখাও (`setAttribute('disabled', false)`)। মানুষ আসলে এই bug-টাই production-এ পাঠায়।""",
        refs=[SPEC_BOOLEAN, MDN_DISABLED],
    ),
    # ------------------------------------------------------------------ html-018
    Q(
        id="html-018", sub="HTML Attributes", diff="medium", type="comparison",
        prio="high", market="both", mins=5,
        tags=["srcset", "sizes", "picture", "responsive-images", "performance"],
        ver="HTML Living Standard (version-independent)", vs=False, status="stable",
        q_en=r"""When do you use `<img srcset sizes>` and when do you need `<picture>`? What goes wrong if you leave out `sizes`?""",
        q_bn=r"""কখন `<img srcset sizes>` ব্যবহার করবে আর কখন `<picture>` লাগবে? `sizes` বাদ দিলে কী সমস্যা হয়?""",
        a_en=r"""
            - **`srcset` + `sizes` = resolution switching.** Same image, different sizes. With `w` descriptors (`hero-480.jpg 480w, hero-960.jpg 960w`) plus `sizes` (how wide the image will be in the layout), the **browser chooses** the best file for the slot width × device pixel ratio — and it may also factor in things like network conditions. For fixed-size images like a logo, `x` descriptors (`1x`, `2x`) are enough.
            - **`<picture>` = art direction or format fallback.** Use it when you need a *different image* — a tighter crop for phones (`<source media="(max-width: 600px)">`) — or newer formats with fallback (`<source type="image/avif">`, then WebP, then JPEG in the `<img>`). Here the browser **must** use the first `<source>` whose `media`/`type` matches.
            - **Missing `sizes`:** with `w` descriptors, `sizes` defaults to `100vw`. In a 4-column product grid the browser then thinks each thumbnail is full-screen width and downloads images roughly four times larger than needed — very costly on mobile data.

            In both cases the `<img>` stays the real element: it carries `alt`, `width`/`height`, `loading` and `fetchpriority`.
        """,
        a_bn=r"""
            - **`srcset` + `sizes` = resolution switching।** একই ছবি, ভিন্ন ভিন্ন মাপ। `w` descriptor (`hero-480.jpg 480w, hero-960.jpg 960w`) আর `sizes` (layout-এ ছবিটা কতটা চওড়া হবে) দিলে **browser নিজেই বেছে নেয়** slot width × device pixel ratio অনুযায়ী কোন file সবচেয়ে উপযুক্ত — network-এর অবস্থার মতো বিষয়ও সে বিবেচনা করতে পারে। Logo-র মতো নির্দিষ্ট মাপের ছবির জন্য `x` descriptor (`1x`, `2x`)-ই যথেষ্ট।
            - **`<picture>` = art direction বা format fallback।** যখন *আলাদা ছবি* দরকার — phone-এর জন্য আরও কাছ থেকে crop করা ছবি (`<source media="(max-width: 600px)">`) — অথবা fallback-সহ নতুন format (`<source type="image/avif">`, তারপর WebP, তারপর `<img>`-এ JPEG), তখন এটা ব্যবহার করো। এখানে যে `<source>`-এর `media`/`type` প্রথম match করে, browser **বাধ্য** সেটাই ব্যবহার করতে।
            - **`sizes` না দিলে:** `w` descriptor থাকলে `sizes`-এর default `100vw`। 4-column product grid-এ browser তখন ভাবে প্রতিটা thumbnail পুরো screen-এর সমান চওড়া, ফলে দরকারের চেয়ে প্রায় চারগুণ বড় ছবি download করে — mobile data-য় যা খুবই ব্যয়বহুল।

            দুই ক্ষেত্রেই আসল element হলো `<img>`: `alt`, `width`/`height`, `loading` আর `fetchpriority` এতেই থাকে।
        """,
        quick_en=r"""`srcset` + `sizes` serves the same image at different sizes and lets the browser pick; `<picture>` is for art direction or format fallback, where the first matching `<source>` must be used. Without `sizes`, it defaults to `100vw`, so grid thumbnails download far too large.""",
        quick_bn=r"""`srcset` + `sizes` একই ছবির ভিন্ন size দেয়, file বেছে নেয় browser; `<picture>` art direction বা format fallback-এর জন্য, যেখানে প্রথম মিলে যাওয়া `<source>`-ই ব্যবহার করতে হয়। `sizes` না দিলে default `100vw` ধরা হয়, তাই grid-এর thumbnail অনেক বড় download হয়।""",
        ex_en=r"""
            - **`sizes` syntax:** a list of media conditions with slot widths, first match wins, last entry has no condition: `sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"`. Keep it in sync with your CSS breakpoints — a wrong `sizes` is just as bad as none.
            - **Why the browser chooses with `srcset`:** it knows the DPR, zoom level and sometimes the user's data-saving preference; your job is to give honest candidates and slot widths.
            - **`width` and `height` attributes** let the browser reserve the right aspect ratio before the image loads, preventing layout shift (CLS). CSS `max-width: 100%; height: auto;` keeps it responsive.
            - **Art direction mistakes:** using `<picture>` just to serve different *sizes* of the same crop throws away the browser's ability to choose — use `srcset` for that.
            - A CDN that resizes on the fly (`?w=480`) makes generating candidates easy, but you still need correct `sizes`.
        """,
        ex_bn=r"""
            - **`sizes`-এর syntax:** media condition আর slot width-এর একটা list, প্রথম যেটা match করে সেটাই জেতে, শেষ entry-তে কোনো condition থাকে না: `sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"`। এটা CSS breakpoint-এর সাথে মিলিয়ে রাখো — ভুল `sizes` দেওয়া আর না দেওয়া প্রায় সমান খারাপ।
            - **`srcset`-এ browser কেন বেছে নেয়:** সে DPR, zoom level আর কখনো কখনো user-এর data-saving পছন্দও জানে; তোমার কাজ হলো সঠিক candidate আর slot width দেওয়া।
            - **`width` আর `height` attribute** দিলে ছবি load হওয়ার আগেই browser সঠিক aspect ratio-র জায়গা রেখে দেয়, ফলে layout shift (CLS) হয় না। CSS-এ `max-width: 100%; height: auto;` দিলে responsive-ও থাকে।
            - **Art direction-এর ভুল:** একই crop-এর শুধু ভিন্ন *মাপ* দেওয়ার জন্য `<picture>` ব্যবহার করলে browser-এর বেছে নেওয়ার ক্ষমতাটাই নষ্ট হয় — এর জন্য `srcset` ব্যবহার করো।
            - যে CDN চাহিদামতো resize করে (`?w=480`), তাতে candidate বানানো সহজ হয়, কিন্তু সঠিক `sizes` তবুও লাগবে।
        """,
        tip_en=r"""Frame it as two different problems — "same image, different sizes" vs "different image or format" — then land the punchline about `sizes` defaulting to `100vw`. Quantifying the wasted bytes ("4× too large in a 4-column grid") makes it stick.""",
        tip_bn=r"""দুটো আলাদা সমস্যা হিসেবে উপস্থাপন করো — "একই ছবি, ভিন্ন মাপ" বনাম "ভিন্ন ছবি বা format" — তারপর মূল কথাটা বলো: `sizes`-এর default `100vw`। নষ্ট হওয়া byte-এর হিসাব দিলে ("4-column grid-এ 4 গুণ বড়") কথাটা মনে থাকে।""",
        mist_en=r"""Omitting `sizes` with `w` descriptors, putting `alt` on `<source>` instead of `<img>`, or using `<picture>` for plain resolution switching.""",
        mist_bn=r"""`w` descriptor দিয়ে `sizes` বাদ দেওয়া, `alt` `<img>`-এ না দিয়ে `<source>`-এ দেওয়া, অথবা সাধারণ resolution switching-এর জন্য `<picture>` ব্যবহার করা।""",
        code=r"""
            <!-- Resolution switching: browser picks the file -->
            <img src="/p/panjabi-480.jpg"
                 srcset="/p/panjabi-240.jpg 240w, /p/panjabi-480.jpg 480w, /p/panjabi-960.jpg 960w"
                 sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"
                 width="480" height="600" loading="lazy" alt="Navy cotton panjabi, front view">

            <!-- Art direction + format fallback: first matching <source> wins -->
            <picture>
              <source media="(max-width: 600px)" type="image/avif" srcset="/banner-mobile.avif">
              <source media="(max-width: 600px)" srcset="/banner-mobile.jpg">
              <source type="image/avif" srcset="/banner-wide.avif">
              <img src="/banner-wide.jpg" width="1600" height="500" alt="Eid sale: up to 40% off">
            </picture>
        """,
        lang="html",
        follow=[
            ("How would you check in DevTools which `srcset` candidate was actually downloaded?", "DevTools-এ কীভাবে দেখবে `srcset`-এর কোন candidate আসলে download হয়েছে?"),
            ("Why might a browser download a smaller candidate than you expected?", "Browser কেন তোমার প্রত্যাশার চেয়ে ছোট candidate download করতে পারে?"),
        ],
        related=["html-010", "html-030"],
        refs=[MDN_IMG, MDN_PICTURE, WEBDEV_RESPONSIVE_IMAGES],
    ),
    # ------------------------------------------------------------------ html-019
    Q(
        id="html-019", sub="HTML APIs", diff="medium", type="coding",
        prio="medium", market="both", mins=8,
        tags=["template", "dom", "documentfragment", "xss", "rendering"],
        ver="HTML Living Standard / DOM Standard (version-independent)", vs=False, status="stable",
        q_en=r"""
            Without a framework, write `renderOrders(orders)` that renders orders into `<tbody id="orders">` using a `<template>` element.

            Each order looks like `{ id: 'DK-1001', customer: 'Rahim', total: 1850, status: 'shipped' }`. Requirements:
            - customer names come from users, so rendering must be XSS-safe;
            - all rows should be inserted with a single DOM update;
            - calling it again replaces the previous rows;
            - the total is shown formatted as BDT currency.
        """,
        q_bn=r"""
            কোনো framework ছাড়া `renderOrders(orders)` function লেখো, যেটা একটা `<template>` element ব্যবহার করে `<tbody id="orders">`-এ order-গুলো render করবে।

            প্রতিটা order দেখতে এমন: `{ id: 'DK-1001', customer: 'Rahim', total: 1850, status: 'shipped' }`। শর্তগুলো:
            - customer-এর নাম user-রা দেয়, তাই rendering XSS-safe হতে হবে;
            - সব row একবারের DOM update-এ insert করতে হবে;
            - আবার call করলে আগের row-গুলো replace হবে;
            - total BDT currency format-এ দেখাতে হবে।
        """,
        a_en=r"""
            I define the row markup once in a `<template>`. Its `content` is an inert `DocumentFragment` — scripts inside don't run and images don't load until it's cloned into the document.

            For each order I `cloneNode(true)` the template content, fill the cells with **`textContent`** (never `innerHTML` for user data, so `<img onerror=…>` in a name is rendered as plain text), and append the clone to one `DocumentFragment`. Finally `tbody.replaceChildren(fragment)` removes old rows and inserts all new rows in a single DOM operation, which means one style/layout pass instead of one per row. Currency is formatted with `Intl.NumberFormat`.
        """,
        a_bn=r"""
            Row-এর markup আমি একবারই একটা `<template>`-এ লিখে রাখি। এর `content` একটা inert `DocumentFragment` — document-এ clone করে বসানোর আগ পর্যন্ত ভেতরের script চলে না, image-ও load হয় না।

            প্রতিটা order-এর জন্য template-এর content `cloneNode(true)` করি, cell-গুলো **`textContent`** দিয়ে পূরণ করি (user data-র জন্য কখনোই `innerHTML` নয়, ফলে নামের ভেতরে `<img onerror=…>` থাকলেও তা সাধারণ text হিসেবে দেখায়), আর clone-টা একটা `DocumentFragment`-এ append করি। শেষে `tbody.replaceChildren(fragment)` এক DOM operation-এ পুরোনো row সরিয়ে সব নতুন row বসিয়ে দেয় — অর্থাৎ প্রতি row-এ একবার নয়, পুরোটার জন্য একবার style/layout হয়। Currency format করি `Intl.NumberFormat` দিয়ে।
        """,
        quick_en=r"""Clone a `<template>` row per order, fill the cells with `textContent` (never `innerHTML`) so names are XSS-safe, format the total with `Intl.NumberFormat`, collect rows in a `DocumentFragment` and call `tbody.replaceChildren(fragment)` once. O(n) time and space.""",
        quick_bn=r"""প্রতিটা order-এর জন্য `<template>`-এর row clone করি, cell-এ `textContent` দিয়ে লিখি (`innerHTML` কখনো নয়), তাই নাম XSS-safe থাকে; total format করি `Intl.NumberFormat` দিয়ে; সব row একটা `DocumentFragment`-এ জমিয়ে একবার `tbody.replaceChildren(fragment)` call করি। Time আর space O(n)।""",
        ex_en=r"""
            - **Query before appending:** once a cloned fragment is appended, it becomes empty (its children move). That's why each row is filled *before* `fragment.append(row)`.
            - **Template parsing perks:** `<template>` can contain `<tr>` directly; a `<div>` with `innerHTML = '<tr>…'` would drop the table parts because of HTML parsing rules.
            - **`cloneNode` vs `importNode`:** `document.importNode(template.content, true)` is equivalent for same-document use; either is fine.
            - **Events:** attach one listener to `tbody` (event delegation) rather than one per row — it survives re-renders.
            - **Edge cases:** empty array (show an empty-state row), missing fields (default to `''`), very large lists (thousands of rows → paginate or virtualize).
            - **Complexity:** O(n) time for n orders, O(n) extra nodes in the fragment.
        """,
        ex_bn=r"""
            - **Append করার আগে query করো:** clone করা fragment append করলে সেটা খালি হয়ে যায় (children সরে যায়)। তাই `fragment.append(row)`-এর *আগেই* প্রতিটা row পূরণ করা হয়েছে।
            - **Template parsing-এর সুবিধা:** `<template>`-এর ভেতরে সরাসরি `<tr>` রাখা যায়; কিন্তু একটা `<div>`-এ `innerHTML = '<tr>…'` দিলে HTML parsing-এর নিয়মের কারণে table-এর অংশগুলো বাদ পড়ে যায়।
            - **`cloneNode` বনাম `importNode`:** একই document-এর মধ্যে `document.importNode(template.content, true)` একই কাজ করে; যেকোনোটা চলবে।
            - **Event:** প্রতিটা row-এ listener না দিয়ে `tbody`-তে একটা listener দাও (event delegation) — re-render হলেও এটা টিকে থাকে।
            - **Edge case:** খালি array (একটা empty-state row দেখাও), field না থাকা (default `''`), খুব বড় list (হাজার হাজার row → pagination বা virtualization)।
            - **Complexity:** n-টা order-এর জন্য O(n) time, আর fragment-এ O(n) অতিরিক্ত node।
        """,
        tip_en=r"""Name the three properties that make this solution good — inert template, `textContent` for safety, one batched insertion — before walking through the code.""",
        tip_bn=r"""Code ব্যাখ্যা করার আগে এই solution-কে ভালো বানানো তিনটা বৈশিষ্ট্যের নাম বলো — inert template, নিরাপত্তার জন্য `textContent`, আর একবারে batch insertion।""",
        mist_en=r"""Building rows with template literals and `innerHTML` (XSS), appending rows one by one inside the loop, or forgetting that `template.content` must be cloned (appending it directly works only once).""",
        mist_bn=r"""Template literal আর `innerHTML` দিয়ে row বানানো (XSS), loop-এর ভেতরে একটা একটা করে row append করা, অথবা ভুলে যাওয়া যে `template.content` clone করতে হয় (সরাসরি append করলে মাত্র একবারই কাজ করে)।""",
        code=r"""
            <table>
              <thead>
                <tr><th>Order</th><th>Customer</th><th>Total</th><th>Status</th></tr>
              </thead>
              <tbody id="orders"></tbody>
            </table>

            <template id="order-row">
              <tr>
                <td class="id"></td>
                <td class="customer"></td>
                <td class="total"></td>
                <td><span class="status"></span></td>
              </tr>
            </template>

            <script>
              const tbody = document.getElementById('orders');
              const rowTemplate = document.getElementById('order-row');
              const bdt = new Intl.NumberFormat('en-BD', { style: 'currency', currency: 'BDT' });

              function renderOrders(orders) {
                const fragment = document.createDocumentFragment();

                for (const order of orders) {
                  const row = rowTemplate.content.cloneNode(true);
                  row.querySelector('.id').textContent = order.id;
                  row.querySelector('.customer').textContent = order.customer ?? '';
                  row.querySelector('.total').textContent = bdt.format(order.total);

                  const status = row.querySelector('.status');
                  status.textContent = order.status;
                  status.dataset.status = order.status; // CSS hook: [data-status="shipped"]

                  fragment.append(row);
                }

                tbody.replaceChildren(fragment); // removes old rows, inserts new ones at once
              }

              renderOrders([
                { id: 'DK-1001', customer: 'Rahim', total: 1850, status: 'shipped' },
                { id: 'DK-1002', customer: '<img src=x onerror=alert(1)>', total: 920, status: 'pending' },
              ]);
            </script>
        """,
        lang="html", time="O(n)", space="O(n)",
        follow=[
            ("How would you handle a click on a 'Cancel order' button inside each row?", "প্রতিটা row-এর ভেতরের 'Cancel order' button-এর click কীভাবে handle করবে?"),
            ("What changes if the list has 20,000 orders?", "List-এ 20,000 order থাকলে কী বদলাতে হবে?"),
        ],
        related=["html-020", "html-032"],
        refs=[MDN_TEMPLATE, MDN_REPLACECHILDREN],
    ),
    # ------------------------------------------------------------------ html-026
    Q(
        id="html-026", sub="Accessibility", diff="hard", type="mcq",
        prio="medium", market="international", mins=3,
        tags=["accessible-name", "aria-labelledby", "aria-label", "wcag"],
        ver="WAI-ARIA 1.2 / AccName 1.2 (version-independent)", vs=False, status="stable",
        q_en=r"""What accessible name will a screen reader announce for this search input?""",
        q_bn=r"""এই search input-এর জন্য screen reader কোন accessible name পড়বে?""",
        code=r"""
            <span id="hint">Find a product</span>
            <label for="q">Search products</label>
            <input id="q" type="search"
                   aria-labelledby="hint"
                   aria-label="Search"
                   placeholder="e.g. panjabi"
                   title="Type a product name">
        """,
        lang="html",
        options=[
            ("\"Search products\" — the `<label>` always wins for form controls.", "\"Search products\" — form control-এর ক্ষেত্রে `<label>` সবসময় জেতে।"),
            ("\"Search\" — `aria-label` overrides everything else.", "\"Search\" — `aria-label` বাকি সবকিছুকে override করে।"),
            ("\"Find a product\" — `aria-labelledby` has the highest priority.", "\"Find a product\" — `aria-labelledby`-এর priority সবচেয়ে বেশি।"),
            ("\"e.g. panjabi\" — the placeholder is used because it's visible inside the field.", "\"e.g. panjabi\" — placeholder ব্যবহার হয়, কারণ এটা field-এর ভেতরেই দেখা যায়।"),
        ],
        correct=2,
        a_en=r"""
            "Find a product". In the accessible name computation, `aria-labelledby` comes first, then `aria-label`, then the native label (`<label>`, `alt`, `<caption>`, or text content for buttons and links), and only then fallbacks like `title` or `placeholder`.
        """,
        a_bn=r"""
            "Find a product"। Accessible name হিসাবের নিয়মে সবার আগে `aria-labelledby`, তারপর `aria-label`, তারপর native label (`<label>`, `alt`, `<caption>`, বা button ও link-এর text content), আর একদম শেষে `title` বা `placeholder`-এর মতো fallback।
        """,
        quick_en=r""""Find a product". In the accessible name computation `aria-labelledby` wins, then `aria-label`, then the native `<label>`, and only after that fallbacks like `title` or `placeholder`.""",
        quick_bn=r""""Find a product"। Accessible name হিসাবের সময় `aria-labelledby` সবার আগে, তারপর `aria-label`, তারপর native `<label>`, আর সবশেষে `title` বা `placeholder`-এর মতো fallback।""",
        ex_en=r"""
            The tempting answer is B, because many people think of `aria-label` as the "strongest" label. It does override the native `<label>`, but `aria-labelledby` beats it.

            The real lesson is that this markup is an **anti-pattern**:
            - Sighted users see "Search products", but the announced name is "Find a product". That fails WCAG 2.5.3 **Label in Name**: a voice-control user saying "click Search products" won't hit the field.
            - Stacking labels like this happens when several developers "fix" accessibility independently. The first rule of ARIA applies: the visible `<label>` was already correct — remove `aria-labelledby` and `aria-label`.
            - `aria-labelledby` is still the right tool when the visible label is elsewhere in the DOM or composed from several elements (e.g. `aria-labelledby="row-name col-price"` in a grid).

            Debug tip: the Accessibility pane in browser DevTools shows the computed name and which source it came from.
        """,
        ex_bn=r"""
            প্রলোভনজনক উত্তর B, কারণ অনেকে `aria-label`-কে "সবচেয়ে শক্তিশালী" label ভাবে। এটা native `<label>`-কে override করে ঠিকই, কিন্তু `aria-labelledby` এর চেয়েও এগিয়ে।

            আসল শিক্ষা হলো, এই markup একটা **anti-pattern**:
            - যারা দেখতে পায় তারা দেখে "Search products", কিন্তু ঘোষিত নাম "Find a product"। এটা WCAG 2.5.3 **Label in Name** ভঙ্গ করে: voice control user "click Search products" বললে field-টা খুঁজে পাবে না।
            - কয়েকজন developer আলাদা আলাদা করে accessibility "ঠিক" করতে গেলে এভাবে label জমে যায়। ARIA-র প্রথম নিয়ম এখানে খাটে: দৃশ্যমান `<label>`-টাই আগে থেকে সঠিক ছিল — `aria-labelledby` আর `aria-label` সরিয়ে ফেলো।
            - তবে দৃশ্যমান label যখন DOM-এর অন্য কোথাও থাকে বা কয়েকটা element মিলিয়ে তৈরি হয় (যেমন grid-এ `aria-labelledby="row-name col-price"`), তখন `aria-labelledby`-ই সঠিক tool।

            Debug tip: browser DevTools-এর Accessibility pane-এ computed name আর সেটা কোন উৎস থেকে এসেছে, দুটোই দেখা যায়।
        """,
        tip_en=r"""Recite the precedence order, then pivot: "but I'd never ship this — it fails Label in Name". Turning a trivia question into a code-review comment is what senior candidates do.""",
        tip_bn=r"""অগ্রাধিকারের ক্রমটা বলো, তারপর মোড় ঘোরাও: "তবে আমি এটা কখনো ship করতাম না — এটা Label in Name ভঙ্গ করে"। একটা trivia প্রশ্নকে code review comment-এ পরিণত করা — senior candidate-রা এটাই করে।""",
        refs=[W3C_ACCNAME, WCAG_LABEL_IN_NAME],
    ),
    # ------------------------------------------------------------------ html-027
    Q(
        id="html-027", sub="Security", diff="hard", type="security-performance",
        prio="high", market="international", mins=10,
        tags=["xss", "csp", "trusted-types", "security", "innerhtml"],
        ver="CSP Level 3; Trusted Types API Baseline newly available (Feb 2026)", vs=True, status="stable",
        q_en=r"""A security review found a DOM-based XSS bug: user-supplied text reached `innerHTML`. Beyond fixing that one line, how would you use Content Security Policy and Trusted Types so this class of bug is much harder to reintroduce?""",
        q_bn=r"""Security review-তে একটা DOM-based XSS bug ধরা পড়েছে: user-এর দেওয়া text `innerHTML`-এ পৌঁছে গেছে। শুধু ওই একটা line ঠিক করার বাইরে, Content Security Policy আর Trusted Types দিয়ে কীভাবে এমন ব্যবস্থা করবে যাতে এই ধরনের bug আবার ঢোকা অনেক কঠিন হয়?""",
        a_en=r"""
            **1. Fix the sink.** Use `textContent` (or safe DOM APIs) for plain text. If rich HTML is genuinely needed (product descriptions, comments with formatting), sanitize it with a well-maintained sanitizer such as DOMPurify right before insertion.

            **2. Strict CSP for scripts.** A nonce- or hash-based policy — `script-src 'nonce-…' 'strict-dynamic'; object-src 'none'; base-uri 'none'` — blocks injected `<script>` tags and inline event handlers (`onerror=…`) even if markup gets in. The nonce must be random per response. I avoid domain allowlists; they're easy to bypass through JSONP endpoints or script gadgets on allowed CDNs.

            **3. Trusted Types to lock the sinks.** Adding `require-trusted-types-for 'script'` makes DOM XSS sinks (`innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, script `src`, `eval`-like APIs) **throw a `TypeError` when given a plain string**. Code must pass a `TrustedHTML` value created by a named policy, and the `trusted-types` directive allowlists those policy names. The result: there are only one or two reviewed places in the codebase that can turn strings into HTML, so a careless `innerHTML = userInput` fails loudly in development instead of becoming a vulnerability.

            **4. Roll out safely.** Start with `Content-Security-Policy-Report-Only` plus a reporting endpoint, fix the violations (third-party scripts usually cause most of them), then enforce. A temporary `default` policy can log and sanitize legacy sinks during migration.

            Trusted Types has been Baseline newly available since February 2026, so users on older browsers won't get the protection — it's defence in depth on top of correct code, not a replacement for it.
        """,
        a_bn=r"""
            **1. Sink ঠিক করো।** Plain text-এর জন্য `textContent` (বা নিরাপদ DOM API) ব্যবহার করো। সত্যিই rich HTML দরকার হলে (product description, formatting-সহ comment), insert করার ঠিক আগে DOMPurify-এর মতো ভালোভাবে maintain করা sanitizer দিয়ে sanitize করো।

            **2. Script-এর জন্য strict CSP।** Nonce- বা hash-ভিত্তিক policy — `script-src 'nonce-…' 'strict-dynamic'; object-src 'none'; base-uri 'none'` — markup ঢুকে পড়লেও inject করা `<script>` tag আর inline event handler (`onerror=…`) আটকে দেয়। প্রতিটা response-এ nonce অবশ্যই random হতে হবে। আমি domain allowlist এড়িয়ে চলি; অনুমোদিত CDN-এর JSONP endpoint বা script gadget দিয়ে এগুলো সহজেই bypass করা যায়।

            **3. Trusted Types দিয়ে sink-গুলো তালাবদ্ধ করো।** `require-trusted-types-for 'script'` যোগ করলে DOM XSS sink-গুলো (`innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, script-এর `src`, `eval`-জাতীয় API) **plain string পেলে `TypeError` throw করে**। Code-কে তখন একটা নামযুক্ত policy দিয়ে বানানো `TrustedHTML` value দিতে হয়, আর `trusted-types` directive সেই policy-র নামগুলো allowlist করে। ফল: পুরো codebase-এ মাত্র এক-দুইটা review করা জায়গা থাকে যেখানে string থেকে HTML বানানো যায়, ফলে অসতর্ক `innerHTML = userInput` vulnerability না হয়ে development-এই জোরালোভাবে fail করে।

            **4. নিরাপদে চালু করো।** প্রথমে reporting endpoint-সহ `Content-Security-Policy-Report-Only` দিয়ে শুরু করো, violation-গুলো ঠিক করো (বেশিরভাগই সাধারণত third-party script থেকে আসে), তারপর enforce করো। Migration-এর সময় একটা অস্থায়ী `default` policy পুরোনো sink-গুলো log ও sanitize করতে পারে।

            Trusted Types February 2026 থেকে Baseline newly available, তাই পুরোনো browser-এর user-রা এই সুরক্ষা পাবে না — এটা সঠিক code-এর উপরে বাড়তি একটা স্তর (defence in depth), সঠিক code-এর বিকল্প নয়।
        """,
        quick_en=r"""Fix the sink with `textContent` or a sanitizer, add a strict nonce-based CSP, and enforce Trusted Types so `innerHTML` throws on plain strings except through a few reviewed policies. Roll out in Report-Only mode first; it's defence in depth, as older browsers lack Trusted Types.""",
        quick_bn=r"""`textContent` বা sanitizer দিয়ে sink ঠিক করি, nonce-based strict CSP দিই, আর Trusted Types enforce করি যাতে অল্প কয়েকটা review করা policy ছাড়া plain string দিলে `innerHTML` error throw করে। আগে Report-Only mode-এ চালাই; পুরোনো browser-এ Trusted Types নেই, তাই এটা defence in depth।""",
        ex_en=r"""
            - **Why both?** CSP limits what injected markup can *do* (no script execution); Trusted Types limits where markup can *enter*. HTML injection without script can still deface pages or phish (fake login forms), so you want both layers.
            - **Framework notes:** React escapes text by default, but `dangerouslySetInnerHTML`, `javascript:` URLs in `href`, and third-party widgets remain sinks. React 19.3 added Trusted Types support, so TrustedHTML values can flow through.
            - **Performance:** sanitizing is not free — sanitize once when storing or rendering, not on every re-render, and cache the result.
            - **Operational pitfalls:** caching an HTML page that contains a nonce at a CDN reuses the same nonce for everyone, which defeats it — use hashes for static pages or make HTML uncacheable. Inline `onload=` tricks for CSS loading also break under strict CSP.
            - **Also relevant:** `HttpOnly` cookies limit what a successful XSS can steal, but don't prevent XSS.
        """,
        ex_bn=r"""
            - **দুটোই কেন?** CSP সীমিত করে inject হওয়া markup কী *করতে* পারবে (script চালাতে পারবে না); Trusted Types সীমিত করে markup কোথা দিয়ে *ঢুকতে* পারবে। Script ছাড়াও HTML injection দিয়ে page বিকৃত করা বা phishing (ভুয়া login form) করা যায়, তাই দুটো স্তরই দরকার।
            - **Framework-এর কথা:** React default-ভাবে text escape করে, কিন্তু `dangerouslySetInnerHTML`, `href`-এ `javascript:` URL আর third-party widget তবুও sink হয়ে থাকে। React 19.3 Trusted Types support যোগ করেছে, ফলে TrustedHTML value এর ভেতর দিয়ে যেতে পারে।
            - **Performance:** sanitize করা ফ্রি নয় — প্রতিটা re-render-এ নয়, store বা render করার সময় একবার sanitize করো আর ফলাফল cache করো।
            - **Operational ফাঁদ:** nonce-যুক্ত HTML page CDN-এ cache করলে সবার জন্য একই nonce ব্যবহার হয়, ফলে nonce-এর উদ্দেশ্যই ব্যর্থ হয় — static page-এর জন্য hash ব্যবহার করো, অথবা HTML cache-অযোগ্য করো। CSS load করার inline `onload=` trick-ও strict CSP-তে ভেঙে যায়।
            - **আরও প্রাসঙ্গিক:** `HttpOnly` cookie সফল XSS কী চুরি করতে পারবে তা সীমিত করে, কিন্তু XSS ঠেকায় না।
        """,
        tip_en=r"""Structure it as layers: fix the code, limit execution (CSP), limit the sinks (Trusted Types), then roll out with report-only. Mentioning that Trusted Types turns a silent vulnerability into a loud `TypeError` is the key insight interviewers look for.""",
        tip_bn=r"""স্তর হিসেবে সাজাও: code ঠিক করো, execution সীমিত করো (CSP), sink সীমিত করো (Trusted Types), তারপর report-only দিয়ে চালু করো। Trusted Types যে নীরব vulnerability-কে জোরালো `TypeError`-এ পরিণত করে — interviewer এই মূল অন্তর্দৃষ্টিটাই খোঁজে।""",
        mist_en=r"""Relying on escaping in one place only, using `'unsafe-inline'` in `script-src`, allowlisting whole CDNs, reusing a static nonce, or enforcing Trusted Types on day one without a report-only phase.""",
        mist_bn=r"""শুধু এক জায়গায় escaping-এর উপর ভরসা করা, `script-src`-এ `'unsafe-inline'` রাখা, পুরো CDN allowlist করা, একই nonce বারবার ব্যবহার করা, অথবা report-only ধাপ ছাড়াই প্রথম দিনেই Trusted Types enforce করা।""",
        code=r"""
            import DOMPurify from 'dompurify';

            // The ONE reviewed place where strings become HTML
            const sanitizer = window.trustedTypes?.createPolicy('app-sanitizer', {
              createHTML: (dirty) => DOMPurify.sanitize(dirty),
            });

            export function renderComment(container, comment) {
              // Plain text: no HTML parsing at all
              container.querySelector('.author').textContent = comment.author;

              // Rich text (bold, italics, links): sanitized and typed
              const safe = sanitizer
                ? sanitizer.createHTML(comment.bodyHtml)
                : DOMPurify.sanitize(comment.bodyHtml); // browsers without Trusted Types
              container.querySelector('.body').innerHTML = safe;
            }

            // With Trusted Types enforced, this line now throws a TypeError:
            // container.innerHTML = location.hash.slice(1);
        """,
        lang="javascript",
        extra=[dict(
            lang="text",
            src=r"""
                # Response header (wrapped here for readability; send it as one line)
                Content-Security-Policy: script-src 'nonce-R4nd0mPerResponse' 'strict-dynamic';
                  object-src 'none'; base-uri 'none';
                  require-trusted-types-for 'script'; trusted-types app-sanitizer;
                  report-to csp-endpoint
            """,
            label_en="Enforced CSP header (start with Content-Security-Policy-Report-Only)",
            label_bn="Enforce করা CSP header (শুরু করো Content-Security-Policy-Report-Only দিয়ে)",
        )],
        follow=[
            ("Why is an allowlist-based `script-src` considered weak?", "Allowlist-ভিত্তিক `script-src` কেন দুর্বল বলে ধরা হয়?"),
            ("How do you handle third-party scripts that use `innerHTML` internally once Trusted Types is enforced?", "Trusted Types enforce করার পর যেসব third-party script ভেতরে `innerHTML` ব্যবহার করে, সেগুলো কীভাবে সামলাবে?"),
        ],
        related=["html-020", "html-017"],
        refs=[MDN_TRUSTED_TYPES, MDN_CSP, OWASP_DOM_XSS],
    ),
    # ------------------------------------------------------------------ html-031
    Q(
        id="html-031", sub="Accessibility", diff="extreme", type="coding",
        prio="medium", market="international", mins=25,
        tags=["combobox", "aria", "keyboard", "autocomplete", "accessibility"],
        ver="WAI-ARIA 1.2 / ARIA Authoring Practices Guide (version-independent)", vs=False, status="stable",
        q_en=r"""
            Build an accessible autocomplete combobox for a "District" field (the 64 districts of Bangladesh) without a UI library.

            Requirements: typing filters the list; Down/Up arrows move through suggestions; Enter picks the highlighted one; Escape closes the list; mouse users can click a suggestion; screen-reader users must hear the highlighted option and how many results there are. Describe the markup and keyboard model, write the core JavaScript, and explain why you wouldn't simply use `<datalist>` or a custom-styled `<select>`.
        """,
        q_bn=r"""
            কোনো UI library ছাড়া "District" field-এর (বাংলাদেশের 64টা জেলা) জন্য একটা accessible autocomplete combobox বানাও।

            শর্ত: type করলে list filter হবে; Down/Up arrow দিয়ে suggestion-গুলোর মধ্যে ঘোরা যাবে; Enter চাপলে highlight করা option বেছে নেওয়া হবে; Escape চাপলে list বন্ধ হবে; mouse user suggestion-এ click করতে পারবে; screen reader user highlight করা option আর কতগুলো result আছে তা শুনতে পাবে। Markup আর keyboard model বর্ণনা করো, মূল JavaScript লেখো, আর ব্যাখ্যা করো কেন সরাসরি `<datalist>` বা custom-style করা `<select>` ব্যবহার করবে না।
        """,
        a_en=r"""
            This is advanced material; I follow the ARIA Authoring Practices "combobox with list autocomplete" pattern.

            **Markup (ARIA 1.2 model):**
            - A real `<label>` and an `<input role="combobox">` with `aria-autocomplete="list"`, `aria-expanded`, `aria-controls` pointing at the list, and `autocomplete="off"` so the browser's own suggestions don't compete.
            - A `<ul role="listbox">` with `<li role="option" id="…">` children.
            - A visually hidden `role="status"` element for "5 results available".

            **Focus model:** DOM focus **stays on the input** the whole time. The "highlighted" option is communicated with `aria-activedescendant="<option id>"` on the input, plus `aria-selected="true"` on the option and a visible highlight style. Screen readers announce the option as if it were focused, and the user can keep typing.

            **Keyboard:** Down opens the list (highlighting the first match) or moves next; Up moves previous; Enter accepts; Escape closes, and a second Escape clears the field; Tab moves on normally. Mouse: `mousedown` on the list is `preventDefault()`-ed so the input doesn't blur before the click is handled.

            **Why not the alternatives?** `<datalist>` gives no control over filtering, styling or screen-reader behaviour, which vary a lot between browsers. A customizable `<select>` (`appearance: base-select`) is **not Baseline yet**. And honestly, for a fixed list of 64 items a plain native `<select>` is often the most accessible option — I'd build a combobox only when filtering, async search or rich options are really needed.
        """,
        a_bn=r"""
            এটা advanced বিষয়; আমি ARIA Authoring Practices-এর "combobox with list autocomplete" pattern অনুসরণ করি।

            **Markup (ARIA 1.2 model):**
            - একটা আসল `<label>` আর `<input role="combobox">`, যাতে থাকবে `aria-autocomplete="list"`, `aria-expanded`, list-কে নির্দেশ করা `aria-controls`, আর `autocomplete="off"`, যাতে browser-এর নিজস্ব suggestion পাল্লা না দেয়।
            - `<li role="option" id="…">` children-সহ একটা `<ul role="listbox">`।
            - "5 results available" জানানোর জন্য visually hidden একটা `role="status"` element।

            **Focus model:** DOM focus পুরো সময় **input-এই থাকে**। কোন option "highlight" হয়ে আছে তা জানানো হয় input-এ `aria-activedescendant="<option id>"` দিয়ে, সাথে option-এ `aria-selected="true"` আর দৃশ্যমান highlight style। Screen reader option-টাকে focus পাওয়ার মতো করেই পড়ে, আর user type করা চালিয়ে যেতে পারে।

            **Keyboard:** Down list খোলে (প্রথম match highlight করে) বা পরেরটায় যায়; Up আগেরটায় যায়; Enter গ্রহণ করে; Escape list বন্ধ করে, আর দ্বিতীয়বার Escape field খালি করে; Tab স্বাভাবিকভাবে পরের element-এ যায়। Mouse: list-এ `mousedown`-এ `preventDefault()` করি, যাতে click handle হওয়ার আগে input blur না হয়।

            **বিকল্পগুলো কেন নয়?** `<datalist>`-এ filtering, styling বা screen reader-এর আচরণের উপর কোনো নিয়ন্ত্রণ নেই, আর এগুলো browser ভেদে অনেক আলাদা। Customizable `<select>` (`appearance: base-select`) **এখনো Baseline নয়**। আর সত্যি বলতে, 64টা item-এর নির্দিষ্ট list-এর জন্য সাধারণ native `<select>`-ই প্রায়ই সবচেয়ে accessible বিকল্প — আমি combobox তখনই বানাব যখন filtering, async search বা rich option সত্যিই দরকার।
        """,
        quick_en=r"""Follow the ARIA combobox pattern: an input with `role="combobox"`, `aria-expanded` and `aria-controls`, a `role="listbox"` of options, focus kept on the input with `aria-activedescendant` marking the highlight, and a `role="status"` result count. For 64 fixed items, a plain `<select>` may be enough.""",
        quick_bn=r"""ARIA combobox pattern মেনে চলি: `role="combobox"`, `aria-expanded` আর `aria-controls`-সহ input, option-গুলোর জন্য `role="listbox"`, focus input-এই থাকে আর `aria-activedescendant` দিয়ে highlight বোঝাই, সাথে result সংখ্যার জন্য `role="status"`। মাত্র 64-টা নির্দিষ্ট item-এর জন্য সাধারণ `<select>`-ই যথেষ্ট হতে পারে।""",
        ex_en=r"""
            - **Why `aria-activedescendant` instead of moving focus into the list?** Moving real focus to options would take the caret away from the input, so typing would stop working. Active-descendant keeps one focus point while still announcing the option.
            - **Announcement noise:** updating the results count on every keystroke can be chatty; debounce it (~300 ms) or only announce when the count changes.
            - **Validation:** the field's value must end up as one of the 64 districts. Use `setCustomValidity()` on submit if the text doesn't match exactly, and validate on the server.
            - **Localisation:** let users match both "Dhaka" and "ঢাকা" by storing search keys per option; matching only on the English name is a real usability gap for Bangladeshi users.
            - **Async data:** for server-side search, cancel stale requests with `AbortController` and show a "Loading…" status.
            - **Test with real assistive tech** (NVDA + Firefox/Chrome, VoiceOver + Safari, TalkBack on Android); combobox support differs more than for most widgets.
            - **Complexity:** filtering is O(n) per keystroke with n = 64 — trivial; for large or remote datasets, filter on the server.
        """,
        ex_bn=r"""
            - **List-এ focus না সরিয়ে কেন `aria-activedescendant`?** আসল focus option-এ সরালে input থেকে caret চলে যায়, ফলে type করা বন্ধ হয়ে যায়। Active-descendant একটাই focus point রেখে option-টা ঘোষণা করে।
            - **অতিরিক্ত announcement:** প্রতিটা keystroke-এ result count আপডেট করলে অনেক কথা বলে; debounce করো (~300 ms) অথবা count বদলালেই শুধু ঘোষণা করো।
            - **Validation:** field-এর শেষ value অবশ্যই 64টা জেলার একটা হতে হবে। Text হুবহু না মিললে submit-এর সময় `setCustomValidity()` ব্যবহার করো, আর server-এও validate করো।
            - **Localisation:** প্রতিটা option-এর search key রেখে "Dhaka" আর "ঢাকা" দুটো দিয়েই match করতে দাও; শুধু English নাম দিয়ে match করা বাংলাদেশি user-দের জন্য বাস্তব একটা usability ঘাটতি।
            - **Async data:** server-side search-এর জন্য `AbortController` দিয়ে পুরোনো request cancel করো আর "Loading…" status দেখাও।
            - **আসল assistive tech দিয়ে test করো** (NVDA + Firefox/Chrome, VoiceOver + Safari, Android-এ TalkBack); বেশিরভাগ widget-এর তুলনায় combobox support অনেক বেশি আলাদা।
            - **Complexity:** প্রতিটা keystroke-এ filtering O(n), যেখানে n = 64 — নগণ্য; বড় বা remote dataset হলে server-এ filter করো।
        """,
        tip_en=r"""Start by questioning the requirement ("would a native `<select>` do?") — that's the senior move. Then explain the single most important design decision, `aria-activedescendant` keeping focus on the input, before showing code.""",
        tip_bn=r"""শুরুতেই requirement নিয়ে প্রশ্ন তোলো ("native `<select>` দিয়েই কি হবে?") — এটাই senior-দের মতো পদক্ষেপ। তারপর code দেখানোর আগে সবচেয়ে গুরুত্বপূর্ণ design সিদ্ধান্তটা ব্যাখ্যা করো — `aria-activedescendant` দিয়ে focus input-এ রাখা।""",
        mist_en=r"""Putting `role="combobox"` on a wrapper `div` (the old ARIA 1.1 pattern), moving DOM focus into the list, forgetting `aria-expanded`, letting the input blur on mousedown so clicks are lost, or relying on colour alone for the highlighted option.""",
        mist_bn=r"""Wrapper `div`-এ `role="combobox"` দেওয়া (পুরোনো ARIA 1.1 pattern), DOM focus list-এ সরিয়ে নেওয়া, `aria-expanded` ভুলে যাওয়া, mousedown-এ input blur হতে দেওয়া (ফলে click হারিয়ে যায়), অথবা highlight করা option বোঝাতে শুধু রঙের উপর নির্ভর করা।""",
        code=r"""
            <label for="district">District</label>
            <input id="district" name="district" type="text" role="combobox"
                   aria-autocomplete="list" aria-expanded="false"
                   aria-controls="district-listbox" autocomplete="off">
            <ul id="district-listbox" role="listbox" aria-label="Districts" hidden></ul>
            <p id="district-status" role="status" class="visually-hidden"></p>

            <script type="module">
              const DISTRICTS = ['Bagerhat', 'Bandarban', 'Barguna', 'Barishal', /* ...all 64... */ 'Dhaka', 'Sylhet'];

              const input = document.getElementById('district');
              const listbox = document.getElementById('district-listbox');
              const status = document.getElementById('district-status');
              let options = [];
              let active = -1;

              function setActive(index) {
                options[active]?.setAttribute('aria-selected', 'false');
                active = index;
                const option = options[active];
                if (option) {
                  option.setAttribute('aria-selected', 'true');
                  input.setAttribute('aria-activedescendant', option.id);
                  option.scrollIntoView({ block: 'nearest' });
                } else {
                  input.removeAttribute('aria-activedescendant');
                }
              }

              function setOpen(open) {
                listbox.hidden = !open;
                input.setAttribute('aria-expanded', String(open));
                if (!open) setActive(-1);
              }

              function render(query) {
                const q = query.trim().toLowerCase();
                const matches = DISTRICTS.filter((d) => d.toLowerCase().startsWith(q)).slice(0, 10);
                options = matches.map((name, i) => {
                  const li = document.createElement('li');
                  li.id = `district-option-${i}`;
                  li.setAttribute('role', 'option');
                  li.setAttribute('aria-selected', 'false');
                  li.textContent = name;
                  return li;
                });
                listbox.replaceChildren(...options);
                active = -1;
                input.removeAttribute('aria-activedescendant');
                setOpen(matches.length > 0);
                status.textContent = `${matches.length} result${matches.length === 1 ? '' : 's'} available`;
              }

              function choose(index) {
                const option = options[index];
                if (!option) return;
                input.value = option.textContent;
                setOpen(false);
              }

              input.addEventListener('input', () => render(input.value));

              input.addEventListener('keydown', (event) => {
                const open = !listbox.hidden;
                switch (event.key) {
                  case 'ArrowDown':
                    event.preventDefault();
                    if (!open) {
                      render(input.value);
                      if (options.length) setActive(0);
                    } else {
                      setActive((active + 1) % options.length);
                    }
                    break;
                  case 'ArrowUp':
                    if (open) {
                      event.preventDefault();
                      setActive(active <= 0 ? options.length - 1 : active - 1);
                    }
                    break;
                  case 'Enter':
                    if (open && active >= 0) {
                      event.preventDefault(); // don't submit the form while choosing
                      choose(active);
                    }
                    break;
                  case 'Escape':
                    if (open) setOpen(false);
                    else input.value = '';
                    break;
                }
              });

              // Keep focus in the input so the click below is not lost
              listbox.addEventListener('mousedown', (event) => event.preventDefault());
              listbox.addEventListener('click', (event) => {
                const li = event.target.closest('[role="option"]');
                if (li) choose(options.indexOf(li));
              });
              input.addEventListener('blur', () => setOpen(false));
            </script>
        """,
        lang="html", time="O(n) per keystroke (n = 64)", space="O(k) rendered options (k ≤ 10)",
        follow=[
            ("How would you change this to search a remote API with thousands of results?", "হাজার হাজার result-সহ remote API search করতে হলে এটা কীভাবে বদলাবে?"),
            ("How would you test this combobox automatically, and what still needs manual screen-reader testing?", "এই combobox automatically কীভাবে test করবে, আর কোন অংশ এখনো screen reader দিয়ে হাতে test করতে হবে?"),
        ],
        related=["html-022", "html-026"],
        refs=[APG_COMBOBOX, MDN_ACTIVEDESCENDANT],
    ),
]

if __name__ == "__main__":
    save("html", "b3", QUESTIONS)
