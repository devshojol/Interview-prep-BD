# Next.js — batch 1 (next-001..004, 012, 013, 023, 030)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_APP = ("Next.js Docs — App Router", "https://nextjs.org/docs/app")
N_PROJECT = ("Next.js Docs — Project Structure", "https://nextjs.org/docs/app/getting-started/project-structure")
N_SC = ("Next.js Docs — Server and Client Components", "https://nextjs.org/docs/app/getting-started/server-and-client-components")
N_LAYOUTS_PAGES = ("Next.js Docs — Layouts and Pages", "https://nextjs.org/docs/app/getting-started/layouts-and-pages")
N_DYNAMIC = ("Next.js Docs — Dynamic Route Segments", "https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes")
N_LAYOUT = ("Next.js Docs — layout.js", "https://nextjs.org/docs/app/api-reference/file-conventions/layout")
N_GSP = ("Next.js Docs — getStaticProps (Pages Router)", "https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props")
N_FETCHING = ("Next.js Docs — Fetching Data", "https://nextjs.org/docs/app/getting-started/fetching-data")
N_MUTATING = ("Next.js Docs — Mutating Data", "https://nextjs.org/docs/app/getting-started/mutating-data")
N_SA_GUIDE = ("Next.js Docs — Server Actions guide", "https://nextjs.org/docs/app/guides/server-actions")
N_UPDATETAG = ("Next.js Docs — updateTag", "https://nextjs.org/docs/app/api-reference/functions/updateTag")
N_DATA_SECURITY = ("Next.js Docs — Data Security", "https://nextjs.org/docs/app/guides/data-security")
N_SA_CONFIG = ("Next.js Docs — serverActions config", "https://nextjs.org/docs/app/api-reference/config/next-config-js/serverActions")
N_SELF_HOST = ("Next.js Docs — Self-hosting", "https://nextjs.org/docs/app/guides/self-hosting")
N_CACHE_HANDLERS = ("Next.js Docs — cacheHandlers", "https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers")
N_REVALIDATION = ("Next.js Docs — How Revalidation Works", "https://nextjs.org/docs/app/guides/how-revalidation-works")
OWASP_IDOR = ("OWASP Cheat Sheet — Authorization", "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ next-001
    Q(
        id="next-001", sub="Next.js Architecture", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["nextjs", "architecture", "framework", "app-router"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""What is Next.js, and what does it add on top of React?""",
        q_bn=r"""Next.js কী, আর React-এর উপরে এটা কী কী যোগ করে?""",
        a_en=r"""
            Next.js is a full-stack React framework. React gives you components; Next.js gives you everything around them that a production app needs:

            - **File-system routing** with the App Router (`app/` folder, nested layouts, dynamic routes).
            - **Server rendering**: React Server Components by default, static prerendering, streaming with Suspense, and Partial Prerendering through **Cache Components** (`'use cache'`).
            - **Data mutations** with Server Functions/Actions and **API endpoints** with Route Handlers.
            - **Request-level logic** in `proxy.ts` (the renamed `middleware.ts`).
            - **Built-in optimisations**: `next/image`, `next/font`, `next/script`, automatic code splitting and link prefetching.
            - **Tooling and deployment**: Turbopack as the default bundler, and deployment to Vercel, a Node.js server, Docker or a static export.

            The current version is 16.4; the App Router is recommended, and the older Pages Router is still supported.
        """,
        a_bn=r"""
            Next.js হলো একটা full-stack React framework। React দেয় component; আর production app-এর জন্য component-এর চারপাশে যা যা লাগে, Next.js সেগুলো দেয়:

            - App Router দিয়ে **file-system routing** (`app/` folder, nested layout, dynamic route)।
            - **Server rendering**: default-ভাবে React Server Component, static prerendering, Suspense দিয়ে streaming, আর **Cache Components** (`'use cache'`) দিয়ে Partial Prerendering।
            - Server Function/Action দিয়ে **data mutation**, আর Route Handler দিয়ে **API endpoint**।
            - `proxy.ts`-এ **request-level logic** (আগের `middleware.ts`-এর নতুন নাম)।
            - **Built-in optimisation**: `next/image`, `next/font`, `next/script`, automatic code splitting আর link prefetching।
            - **Tooling আর deployment**: default bundler হিসেবে Turbopack, আর Vercel, Node.js server, Docker বা static export-এ deploy করা যায়।

            বর্তমান version 16.4; App Router recommended, আর পুরনো Pages Router এখনো support করে।
        """,
        quick_en=r"""Next.js is a full-stack React framework. React gives you components, and Next.js adds what surrounds them: file-system routing (App Router), server rendering with Server Components and streaming, Server Actions and Route Handlers, `proxy.ts`, and built-in image and font optimisation.""",
        quick_bn=r"""Next.js হলো একটা full-stack React framework। React শুধু component দেয়, আর Next.js তার চারপাশের বাকি সব যোগ করে: folder দিয়ে routing (App Router), Server Component ও streaming-সহ server-এ render করা, Server Action ও Route Handler, `proxy.ts`, আর ছবি ও font নিজে থেকেই optimise করার ব্যবস্থা।""",
        ex_en=r"""
            **Request flow in the App Router (simplified):**
            1. `proxy.ts` can redirect, rewrite or set headers before routing.
            2. The URL is matched to a folder; its layouts and page render as Server Components.
            3. The server sends HTML (fast first paint) plus an **RSC payload** describing the component tree; prerendered static shells can come straight from a CDN while dynamic parts stream in.
            4. The browser hydrates only the Client Components (`'use client'`).
            5. Later navigations are client-side: Next.js fetches RSC payloads (often prefetched) instead of full HTML pages.

            Practical requirements for v16: Node.js 20.9+, TypeScript 5.1+. `next lint` was removed (run ESLint or Biome directly), and AMP and runtime config were removed.
        """,
        ex_bn=r"""
            **App Router-এ request-এর প্রবাহ (সহজভাবে):**
            1. Routing-এর আগে `proxy.ts` redirect, rewrite বা header set করতে পারে।
            2. URL একটা folder-এর সাথে মেলে; তার layout আর page Server Component হিসেবে render হয়।
            3. Server HTML পাঠায় (দ্রুত first paint), সাথে একটা **RSC payload**, যেটা component tree বর্ণনা করে; prerender করা static shell সরাসরি CDN থেকে আসতে পারে, আর dynamic অংশ stream হয়ে আসে।
            4. Browser শুধু Client Component (`'use client'`) hydrate করে।
            5. পরের navigation-গুলো client-side: Next.js পুরো HTML page না এনে RSC payload আনে (প্রায়ই আগেই prefetch করা)।

            v16-এর বাস্তব শর্ত: Node.js 20.9+, TypeScript 5.1+। `next lint` সরিয়ে ফেলা হয়েছে (সরাসরি ESLint বা Biome চালাও), AMP আর runtime config-ও সরানো হয়েছে।
        """,
        tip_en=r"""Don't just list features — group them: routing, rendering, data, optimisation, deployment. Mentioning the current model (Server Components, Cache Components, `proxy.ts`) shows you're up to date.""",
        tip_bn=r"""শুধু feature-এর তালিকা দিও না — ভাগ করে বলো: routing, rendering, data, optimisation, deployment। বর্তমান model-এর কথা (Server Component, Cache Components, `proxy.ts`) বললে বোঝা যায় তুমি আপডেটেড।""",
        mist_en=r"""Describing Next.js only as "React with SSR", or presenting `getServerSideProps` and `middleware.ts` as the current way to build new apps.""",
        mist_bn=r"""Next.js-কে শুধু "SSR-সহ React" বলা, অথবা নতুন app বানানোর বর্তমান উপায় হিসেবে `getServerSideProps` আর `middleware.ts` উপস্থাপন করা।""",
        code=r"""
            my-shop/
            ├── app/
            │   ├── layout.tsx          # root layout (<html>, <body>)
            │   ├── page.tsx            # /
            │   ├── products/
            │   │   └── [id]/
            │   │       ├── page.tsx    # /products/123
            │   │       └── loading.tsx # streaming fallback
            │   └── api/
            │       └── health/
            │           └── route.ts    # GET /api/health
            ├── proxy.ts                # runs before routing (was middleware.ts)
            ├── public/                 # static files
            └── next.config.ts
        """,
        lang="text",
        follow=[
            ("What is the RSC payload and why does Next.js send it along with HTML?", "RSC payload কী, আর Next.js কেন HTML-এর সাথে এটাও পাঠায়?"),
            ("When would you choose plain React with Vite instead of Next.js?", "কখন Next.js-এর বদলে Vite-সহ সাধারণ React বেছে নেবে?"),
        ],
        refs=[N_APP, N_PROJECT, N_SC],
    ),
    # ------------------------------------------------------------------ next-002
    Q(
        id="next-002", sub="File-based Routing", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["routing", "app-router", "dynamic-routes", "file-conventions"],
        ver="Next.js 16.4 (App Router)", vs=False, status="stable",
        q_en=r"""In the App Router, which file renders a page for any URL like `/blog/hello-world` or `/blog/nextjs-16`?""",
        q_bn=r"""App Router-এ `/blog/hello-world` বা `/blog/nextjs-16`-এর মতো যেকোনো URL-এর জন্য কোন file একটা page render করে?""",
        options=[
            ("`app/blog/[slug].tsx`", "`app/blog/[slug].tsx`"),
            ("`app/blog/[slug]/page.tsx`", "`app/blog/[slug]/page.tsx`"),
            ("`app/blog/[slug]/layout.tsx`", "`app/blog/[slug]/layout.tsx`"),
            ("`app/blog/[slug]/index.tsx`", "`app/blog/[slug]/index.tsx`"),
        ],
        correct=1,
        a_en=r"""`app/blog/[slug]/page.tsx`. In the App Router, **folders** define URL segments (`[slug]` is a dynamic segment) and a segment only becomes a public route when it contains a `page` file (for UI) or a `route` file (for an API endpoint).""",
        a_bn=r"""`app/blog/[slug]/page.tsx`। App Router-এ **folder** URL segment ঠিক করে (`[slug]` হলো dynamic segment), আর কোনো segment-এ `page` file (UI-এর জন্য) বা `route` file (API endpoint-এর জন্য) থাকলেই কেবল সেটা public route হয়।""",
        quick_en=r"""`app/blog/[slug]/page.tsx`. In the App Router folders define URL segments (`[slug]` is dynamic), and a segment becomes a public route only when it has a `page` file (or a `route` file for an API).""",
        quick_bn=r"""`app/blog/[slug]/page.tsx`। App Router-এ folder দিয়ে URL segment তৈরি হয় (`[slug]` dynamic), আর কোনো segment public route হয় শুধু তখনই যখন তাতে `page` file থাকে (API-র জন্য `route` file)।""",
        ex_en=r"""
            The tempting wrong answer is `app/blog/[slug].tsx` — that file-as-route style comes from the **Pages Router** (`pages/blog/[slug].tsx`). In `app/`, a file named `[slug].tsx` is just a module, not a route. `index.tsx` has no special meaning in the App Router either, and a `layout.tsx` alone only wraps pages — it doesn't create one.

            Related conventions: `[...slug]` is a catch-all, `[[...slug]]` an optional catch-all, `(marketing)` is a route group that doesn't appear in the URL, and `_components` is a private folder. Because only `page`/`route` files are public, you can safely colocate components, tests and styles inside route folders.
        """,
        ex_bn=r"""
            লোভনীয় ভুল উত্তর হলো `app/blog/[slug].tsx` — file-কেই route ধরার এই style এসেছে **Pages Router** থেকে (`pages/blog/[slug].tsx`)। `app/`-এর ভেতরে `[slug].tsx` নামের file শুধু একটা module, route না। App Router-এ `index.tsx`-এরও বিশেষ কোনো অর্থ নেই, আর শুধু `layout.tsx` page-কে wrap করে — নিজে page তৈরি করে না।

            সংশ্লিষ্ট নিয়ম: `[...slug]` হলো catch-all, `[[...slug]]` optional catch-all, `(marketing)` হলো route group যেটা URL-এ দেখা যায় না, আর `_components` হলো private folder। যেহেতু শুধু `page`/`route` file public, তাই route folder-এর ভেতরে নিশ্চিন্তে component, test আর style রাখা যায়।
        """,
        tip_en=r"""Explain the rule ("folders = segments, `page` = public UI") rather than just picking the file. Contrasting it with the Pages Router shows you can work in both codebases.""",
        tip_bn=r"""শুধু file বেছে না দিয়ে নিয়মটা ব্যাখ্যা করো ("folder = segment, `page` = public UI")। Pages Router-এর সাথে তুলনা করলে বোঝা যায় তুমি দুই ধরনের codebase-এই কাজ করতে পারো।""",
        refs=[N_LAYOUTS_PAGES, N_DYNAMIC, N_PROJECT],
    ),
    # ------------------------------------------------------------------ next-003
    Q(
        id="next-003", sub="Layouts", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["layouts", "templates", "app-router", "nested-routes"],
        ver="Next.js 16.4 (App Router)", vs=False, status="stable",
        q_en=r"""What are layouts in the App Router, and how do they differ from pages and templates?""",
        q_bn=r"""App Router-এ layout কী, আর page ও template থেকে এটা কীভাবে আলাদা?""",
        a_en=r"""
            A **layout** (`layout.tsx`) is UI shared by a route segment and everything below it — a navbar, a dashboard sidebar. It receives `children` and wraps them. The key property: when you navigate between pages that share a layout, the layout **stays mounted** — it doesn't re-render or lose state (search box text, scroll position in a sidebar).

            The **root layout** (`app/layout.tsx`) is required and must render `<html>` and `<body>`. Layouts nest: `app/layout.tsx` wraps `app/dashboard/layout.tsx`, which wraps the dashboard pages.

            A **page** (`page.tsx`) is the unique UI of one route. A **template** (`template.tsx`) looks like a layout but gets a **new instance on every navigation**, so state resets and effects run again — useful for enter animations or per-page logging.
        """,
        a_bn=r"""
            **Layout** (`layout.tsx`) হলো একটা route segment আর তার নিচের সবকিছুর shared UI — যেমন navbar বা dashboard sidebar। এটা `children` পায় আর সেগুলো wrap করে। মূল বৈশিষ্ট্য: একই layout share করা page-গুলোর মধ্যে navigate করলে layout **mount হয়েই থাকে** — re-render হয় না, state-ও হারায় না (search box-এর লেখা, sidebar-এর scroll position)।

            **Root layout** (`app/layout.tsx`) বাধ্যতামূলক, আর এটাকে `<html>` ও `<body>` render করতে হয়। Layout nest হয়: `app/layout.tsx` wrap করে `app/dashboard/layout.tsx`-কে, যেটা আবার dashboard-এর page-গুলোকে wrap করে।

            **Page** (`page.tsx`) হলো একটা route-এর নিজস্ব UI। **Template** (`template.tsx`) দেখতে layout-এর মতো, কিন্তু **প্রতিটা navigation-এ নতুন instance** পায়, ফলে state reset হয় আর effect আবার চলে — enter animation বা প্রতি page-এ logging-এর জন্য কাজে লাগে।
        """,
        quick_en=r"""A `layout.tsx` wraps a segment and its children and stays mounted with its state when you navigate between pages under it. A `page.tsx` is one route's unique UI, and a `template.tsx` wraps like a layout but remounts on every navigation.""",
        quick_bn=r"""`layout.tsx` একটা segment আর তার children-কে wrap করে, আর তার নিচের page-গুলোর মধ্যে navigate করলেও state-সহ mounted থাকে। `page.tsx` হলো একটা route-এর নিজস্ব UI, আর `template.tsx` layout-এর মতো wrap করে কিন্তু প্রতি navigation-এ নতুন করে mount হয়।""",
        ex_en=r"""
            - Layouts receive `children` and `params` (a Promise in v16), but **not** `searchParams` — because they don't re-render on navigation, they'd show stale query values. Read search params in the page or in a Client Component with `useSearchParams()`.
            - Layouts can't know the current pathname on the server; use `usePathname()` in a Client Component for "active link" styling.
            - **Don't rely on a layout alone for authorization:** it doesn't re-render on client navigations between its child pages, and it isn't involved when a Server Action is called. Check auth close to the data.
            - Metadata (`export const metadata`) defined in layouts merges with metadata from nested layouts and pages.
        """,
        ex_bn=r"""
            - Layout `children` আর `params` পায় (v16-এ একটা Promise), কিন্তু `searchParams` **পায় না** — navigation-এ re-render হয় না বলে পুরনো query value দেখাত। Search param page-এ পড়ো, অথবা Client Component-এ `useSearchParams()` দিয়ে।
            - Server-এ layout বর্তমান pathname জানতে পারে না; "active link" style-এর জন্য Client Component-এ `usePathname()` ব্যবহার করো।
            - **শুধু layout-এর উপর authorization-এর ভরসা করো না:** child page-গুলোর মধ্যে client navigation-এ এটা re-render হয় না, আর Server Action call হলে layout জড়িতই থাকে না। Auth check data-র কাছাকাছি করো।
            - Layout-এ define করা metadata (`export const metadata`) nested layout আর page-এর metadata-র সাথে merge হয়।
        """,
        tip_en=r"""Emphasise "layouts persist across navigation" — it explains both their benefit (state, performance) and their gotchas (no `searchParams`, not a security boundary).""",
        tip_bn=r"""জোর দিয়ে বলো "navigation-এর মধ্যেও layout টিকে থাকে" — এটা দিয়েই এর সুবিধা (state, performance) আর gotcha (কোনো `searchParams` নেই, security boundary না) — দুটোই ব্যাখ্যা হয়।""",
        mist_en=r"""Putting an auth check only in a layout, or expecting `searchParams` in a layout's props.""",
        mist_bn=r"""শুধু layout-এ auth check রাখা, অথবা layout-এর props-এ `searchParams` আশা করা।""",
        code=r"""
            // app/layout.tsx — root layout (required)
            import './globals.css';

            export default function RootLayout({ children }: { children: React.ReactNode }) {
              return (
                <html lang="en">
                  <body>{children}</body>
                </html>
              );
            }

            // app/dashboard/layout.tsx — persists while moving between dashboard pages
            import { Sidebar } from './sidebar';

            export default function DashboardLayout({ children }: { children: React.ReactNode }) {
              return (
                <div className="dashboard">
                  <Sidebar />
                  <main>{children}</main>
                </div>
              );
            }
        """,
        lang="tsx",
        follow=[
            ("When would you use `template.tsx` instead of `layout.tsx`?", "কখন `layout.tsx`-এর বদলে `template.tsx` ব্যবহার করবে?"),
            ("How do route groups like `(shop)` let you have multiple root layouts?", "`(shop)`-এর মতো route group দিয়ে কীভাবে একাধিক root layout রাখা যায়?"),
        ],
        related=["next-002"],
        refs=[N_LAYOUTS_PAGES, N_LAYOUT],
    ),
    # ------------------------------------------------------------------ next-004
    Q(
        id="next-004", sub="Server Components and Client Components", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["server-components", "client-components", "use-client", "hydration"],
        ver="Next.js 16.4 (App Router, React 19.3)", vs=True, status="stable",
        q_en=r"""In the Next.js App Router, what's the difference between Server Components and Client Components, and when do you add `'use client'`?""",
        q_bn=r"""Next.js App Router-এ Server Component আর Client Component-এর পার্থক্য কী, আর কখন `'use client'` যোগ করো?""",
        a_en=r"""
            In the App Router every component is a **Server Component by default**. It runs only on the server (at build time or per request), can be `async`, can read a database or secrets directly, and ships **no JavaScript** for itself to the browser.

            A **Client Component** is marked with `'use client'` at the top of its file. It's still prerendered to HTML on the server, but its code is also sent to the browser and **hydrated**, so it can use state, effects, event handlers and browser APIs (`window`, `localStorage`).

            I add `'use client'` only where interactivity is needed — a like button, a dropdown, a form with live validation — and keep pages, layouts and data fetching as Server Components. Server data flows to Client Components as serialisable props.
        """,
        a_bn=r"""
            App Router-এ প্রতিটা component **default-ভাবে Server Component**। এটা শুধু server-এ চলে (build time-এ বা প্রতি request-এ), `async` হতে পারে, সরাসরি database বা secret পড়তে পারে, আর browser-এ নিজের জন্য **কোনো JavaScript পাঠায় না**।

            **Client Component** চিহ্নিত হয় file-এর শুরুতে `'use client'` দিয়ে। এটাও server-এ HTML হিসেবে prerender হয়, কিন্তু এর code browser-এও যায় আর **hydrate** হয়, ফলে এটা state, effect, event handler আর browser API (`window`, `localStorage`) ব্যবহার করতে পারে।

            আমি শুধু যেখানে interactivity লাগে সেখানেই `'use client'` দিই — like button, dropdown, live validation-সহ form — আর page, layout ও data fetching Server Component হিসেবে রাখি। Server-এর data serialisable props হিসেবে Client Component-এ যায়।
        """,
        quick_en=r"""Components are Server Components by default: they run only on the server, can be `async` and read data directly, and ship no JS. Add `'use client'` only where you need state, effects, event handlers or browser APIs; those are prerendered and then hydrated.""",
        quick_bn=r"""Component default-এ Server Component: শুধু server-এ চলে, `async` হতে পারে, সরাসরি data পড়তে পারে, আর কোনো JS পাঠায় না। State, effect, event handler বা browser API লাগলে শুধু সেখানেই `'use client'` দাও; সেগুলো আগে prerender হয়, তারপর hydrate হয়।""",
        ex_en=r"""
            - **Misconception:** "Client Components render only in the browser." No — they're server-rendered to HTML too; `'use client'` means "also ship and hydrate this on the client".
            - **The directive marks a boundary in the module graph:** everything a Client Component file imports becomes client code. So put it on small leaf components, not on a whole page.
            - **Composition:** a Client Component can't import a Server Component, but it can render one passed in as `children` or another prop.
            - **Protect server code** with `import 'server-only'` in modules that touch the database or secrets — the build fails if a Client Component imports them.
            - Context providers, and third-party components that use hooks but lack the directive, need a small `'use client'` wrapper.
        """,
        ex_bn=r"""
            - **ভুল ধারণা:** "Client Component শুধু browser-এ render হয়।" না — এগুলোও server-এ HTML হিসেবে render হয়; `'use client'` মানে "এটা client-এও পাঠাও আর hydrate করো"।
            - **Directive module graph-এ একটা boundary চিহ্নিত করে:** একটা Client Component file যা import করে, সবই client code হয়ে যায়। তাই এটা পুরো page-এ না, ছোট leaf component-এ দাও।
            - **Composition:** Client Component কোনো Server Component import করতে পারে না, কিন্তু `children` বা অন্য prop হিসেবে পাঠানো Server Component render করতে পারে।
            - **Server code রক্ষা করো** — যেসব module database বা secret ছোঁয়, সেখানে `import 'server-only'` দাও; কোনো Client Component এগুলো import করলে build fail করবে।
            - Context provider, আর hook ব্যবহার করে কিন্তু directive নেই এমন third-party component-এর জন্য ছোট একটা `'use client'` wrapper লাগে।
        """,
        tip_en=r"""Correct the common misconception explicitly ("Client Components are still server-rendered"). Then state your rule: Server Components by default, `'use client'` at interactive leaves.""",
        tip_bn=r"""সাধারণ ভুল ধারণাটা স্পষ্টভাবে শুধরে দাও ("Client Component-ও server-এ render হয়")। তারপর তোমার নিয়ম বলো: default-ভাবে Server Component, interactive leaf-এ `'use client'`।""",
        mist_en=r"""Adding `'use client'` to every page "to make hooks work", which ships far more JavaScript, or trying to use `useState` in a Server Component.""",
        mist_bn=r""""Hook চালানোর জন্য" প্রতিটা page-এ `'use client'` দেওয়া, যাতে অনেক বেশি JavaScript পাঠানো হয়, অথবা Server Component-এ `useState` ব্যবহারের চেষ্টা করা।""",
        code=r"""
            // app/products/[id]/page.tsx — Server Component (default)
            import { getProduct } from '@/lib/products'; // reads the DB, never shipped to the browser
            import { AddToCartButton } from './add-to-cart-button';

            export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
              const { id } = await params;
              const product = await getProduct(id);
              return (
                <article>
                  <h1>{product.name}</h1>
                  <p>{product.description}</p>
                  <AddToCartButton productId={product.id} />
                </article>
              );
            }

            // app/products/[id]/add-to-cart-button.tsx — Client Component (interactive leaf)
            'use client';
            import { useState } from 'react';

            export function AddToCartButton({ productId }: { productId: string }) {
              const [added, setAdded] = useState(false);
              return (
                <button onClick={() => setAdded(true)} disabled={added}>
                  {added ? 'Added ✓' : 'Add to cart'}
                </button>
              );
            }
        """,
        lang="tsx",
        follow=[
            ("How can a Client Component render a Server Component?", "একটা Client Component কীভাবে Server Component render করতে পারে?"),
            ("What does the `server-only` package protect you from?", "`server-only` package তোমাকে কী থেকে রক্ষা করে?"),
        ],
        related=["next-001"],
        refs=[N_SC, N_FETCHING],
    ),
    # ------------------------------------------------------------------ next-012
    Q(
        id="next-012", sub="App Router vs Pages Router", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["app-router", "pages-router", "migration", "legacy"],
        ver="Next.js 16.4 (both routers supported; Pages Router = legacy)", vs=True, status="stable",
        q_en=r"""Compare the App Router and the Pages Router. Why is the App Router recommended for new projects, and when will you still work with the Pages Router?""",
        q_bn=r"""App Router আর Pages Router-এর তুলনা করো। নতুন project-এ কেন App Router recommended, আর কখন এখনো Pages Router নিয়ে কাজ করবে?""",
        a_en=r"""
            The main differences (the Pages Router is the legacy option):

            - **Components:** App Router components are Server Components by default; Pages Router pages are all client components that hydrate in full.
            - **Data fetching:** App Router uses `async` components that read data directly, plus `'use cache'` for caching. Pages Router uses `getServerSideProps`, `getStaticProps` + `getStaticPaths`, and ISR via `revalidate`.
            - **Layouts:** nested, persistent `layout.tsx` files vs a single `_app`/`_document`.
            - **Loading and errors:** built-in streaming with `loading.tsx`/Suspense and `error.tsx` per segment vs manual handling.
            - **Mutations:** Server Actions vs API routes in `pages/api`.
            - **Metadata:** the `metadata`/`generateMetadata` API vs `next/head`.

            The App Router is recommended because it ships less JavaScript, streams UI, colocates data fetching with components and supports the new features (Cache Components, Partial Prerendering, Server Actions). I'd still work with the Pages Router when maintaining existing apps — it's supported, and both routers can coexist in one project, which allows incremental migration route by route.
        """,
        a_bn=r"""
            মূল পার্থক্যগুলো:

            - **Component:** App Router-এর component default-ভাবে Server Component; Pages Router-এর page সবই client component, যেগুলো পুরোপুরি hydrate হয়।
            - **Data fetching:** App Router-এ `async` component সরাসরি data পড়ে, আর caching-এর জন্য `'use cache'`। Pages Router-এ `getServerSideProps`, `getStaticProps` + `getStaticPaths`, আর `revalidate` দিয়ে ISR।
            - **Layout:** nested, টিকে থাকা `layout.tsx` file বনাম একটাই `_app`/`_document`।
            - **Loading আর error:** প্রতি segment-এ `loading.tsx`/Suspense দিয়ে built-in streaming আর `error.tsx` বনাম হাতে সামলানো।
            - **Mutation:** Server Action বনাম `pages/api`-এর API route।
            - **Metadata:** `metadata`/`generateMetadata` API বনাম `next/head`।

            App Router recommended, কারণ এটা কম JavaScript পাঠায়, UI stream করে, data fetching component-এর পাশেই রাখে আর নতুন feature (Cache Components, Partial Prerendering, Server Action) support করে। পুরনো app maintain করার সময় আমি এখনো Pages Router নিয়ে কাজ করব — এটা support করে, আর দুটো router একই project-এ পাশাপাশি থাকতে পারে, ফলে route ধরে ধরে ধাপে ধাপে migration করা যায়।
        """,
        quick_en=r"""The App Router uses Server Components, nested persistent layouts, async data fetching, streaming and Server Actions, so it ships less JS and supports the new features. The Pages Router is legacy but supported; you meet it in existing apps, and both can coexist for route-by-route migration.""",
        quick_bn=r"""App Router-এ আছে Server Component, nested persistent layout, async data fetching, streaming আর Server Action, তাই কম JS যায় আর নতুন feature-গুলো পাওয়া যায়। Pages Router legacy কিন্তু এখনো supported; পুরনো app-এ এটা পাবে, আর route ধরে migrate করার জন্য দুটো একসাথে চলতে পারে।""",
        ex_en=r"""
            **Coexistence details:** both `app/` and `pages/` can live in one project, but the same URL can't be defined in both. Navigating between a Pages route and an App route is a hard navigation (full page load), so migrate related routes together.

            **Mental-model shift:** in the Pages Router the unit of data fetching is the *page* (one `getServerSideProps`), and everything below gets props. In the App Router any Server Component can fetch what it needs, and React `cache`/`'use cache'` deduplicate requests, so data fetching moves down to where it's used.

            **Status labels:** Pages Router APIs aren't deprecated, but new features land in the App Router — treat the Pages Router as a legacy/maintenance option for new work.
        """,
        ex_bn=r"""
            **পাশাপাশি থাকার খুঁটিনাটি:** `app/` আর `pages/` একই project-এ থাকতে পারে, কিন্তু একই URL দুই জায়গায় define করা যায় না। Pages route আর App route-এর মধ্যে navigate করলে hard navigation হয় (পুরো page load), তাই সম্পর্কিত route-গুলো একসাথে migrate করো।

            **চিন্তার ধরনে পরিবর্তন:** Pages Router-এ data fetching-এর একক হলো *page* (একটাই `getServerSideProps`), আর নিচের সবকিছু props পায়। App Router-এ যেকোনো Server Component নিজের দরকারি data fetch করতে পারে, আর React `cache`/`'use cache'` request deduplicate করে, তাই data fetching যেখানে ব্যবহার হয় সেখানেই নেমে আসে।

            **Status label:** Pages Router-এর API deprecated না, কিন্তু নতুন feature আসে App Router-এ — নতুন কাজের জন্য Pages Router-কে legacy/maintenance option হিসেবে ধরো।
        """,
        tip_en=r"""Use a few clear comparison axes (components, data, layouts, mutations) instead of a long feature dump, and finish with the practical migration note — coexistence and route-by-route moves.""",
        tip_bn=r"""লম্বা feature-এর তালিকা না দিয়ে কয়েকটা স্পষ্ট তুলনার মাপকাঠি ব্যবহার করো (component, data, layout, mutation), আর শেষে migration-এর বাস্তব নোট দাও — পাশাপাশি থাকা আর route ধরে ধরে সরানো।""",
        mist_en=r"""Claiming the Pages Router is deprecated or removed, or using `getServerSideProps` inside the `app/` directory (it doesn't work there).""",
        mist_bn=r"""দাবি করা যে Pages Router deprecated বা সরিয়ে ফেলা হয়েছে, অথবা `app/` directory-র ভেতরে `getServerSideProps` ব্যবহার করা (সেখানে এটা কাজ করে না)।""",
        code=r"""
            // Pages Router (legacy) — pages/products/[id].tsx
            export async function getServerSideProps({ params }) {
              const product = await getProduct(params.id);
              if (!product) return { notFound: true };
              return { props: { product } };
            }

            export default function ProductPage({ product }) {
              return <ProductView product={product} />;
            }

            // App Router — app/products/[id]/page.tsx
            import { notFound } from 'next/navigation';

            export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
              const { id } = await params;
              const product = await getProduct(id);
              if (!product) notFound();
              return <ProductView product={product} />;
            }
        """,
        lang="tsx",
        follow=[
            ("What happens when a user navigates from a Pages Router route to an App Router route?", "User যখন Pages Router-এর route থেকে App Router-এর route-এ navigate করে, তখন কী হয়?"),
            ("How do `getStaticProps` + `revalidate` translate to the App Router?", "`getStaticProps` + `revalidate` App Router-এ কীভাবে রূপান্তরিত হয়?"),
        ],
        related=["next-002", "next-004"],
        refs=[N_APP, N_GSP, N_FETCHING],
    ),
    # ------------------------------------------------------------------ next-013
    Q(
        id="next-013", sub="Server Actions", diff="medium", type="coding",
        prio="high", market="both", mins=10,
        tags=["server-actions", "forms", "validation", "zod", "useactionstate"],
        ver="Next.js 16.4 (App Router, React 19.3, Zod 4)", vs=True, status="stable",
        q_en=r"""
            Implement a "create post" feature with a **Server Action**:
            - validate `title` (3–120 chars) and `body` (at least 10 chars) on the server with Zod;
            - reject the request if the user isn't logged in;
            - save the post, make the cached post list show it immediately, and redirect to the new post;
            - show field errors in the form without a page reload, and disable the button while saving.
        """,
        q_bn=r"""
            একটা **Server Action** দিয়ে "create post" feature তৈরি করো:
            - server-এ Zod দিয়ে `title` (৩–১২০ অক্ষর) আর `body` (কমপক্ষে ১০ অক্ষর) validate করো;
            - user logged in না থাকলে request বাতিল করো;
            - post save করো, cached post list-এ যেন সাথে সাথে দেখা যায় তা নিশ্চিত করো, আর নতুন post-এ redirect করো;
            - page reload ছাড়াই form-এ field error দেখাও, আর save হওয়ার সময় button disable রাখো।
        """,
        a_en=r"""
            The action lives in a file marked `'use server'`, so it runs only on the server and can be passed to a form. Because it's called with `useActionState`, its signature is `(previousState, formData)` and its return value becomes the form state.

            Inside the action I: (1) check the session — never trust that the UI hid the form; (2) parse `FormData` with a Zod schema using `safeParse`, returning `fieldErrors` instead of throwing; (3) write to the database; (4) call `updateTag('posts')` so the list cached with `cacheTag('posts')` is expired immediately (read-your-own-writes); (5) `redirect()` to the new post.

            On the client, `useActionState` gives me the returned errors and `isPending` for the button. The form also works before JavaScript loads, because `<form action>` posts natively.
        """,
        a_bn=r"""
            Action-টা থাকে `'use server'` দেওয়া একটা file-এ, তাই এটা শুধু server-এ চলে আর form-এ পাঠানো যায়। `useActionState` দিয়ে call হয় বলে এর signature হলো `(previousState, formData)`, আর এর return value-ই form-এর state হয়।

            Action-এর ভেতরে আমি: (১) session check করি — UI form লুকিয়েছে বলে কখনো ভরসা করি না; (২) Zod schema আর `safeParse` দিয়ে `FormData` parse করি, throw না করে `fieldErrors` return করি; (৩) database-এ লিখি; (৪) `updateTag('posts')` call করি, যাতে `cacheTag('posts')` দিয়ে cache করা list সাথে সাথে expire হয় (read-your-own-writes); (৫) `redirect()` দিয়ে নতুন post-এ যাই।

            Client-এ `useActionState` আমাকে return করা error আর button-এর জন্য `isPending` দেয়। JavaScript load হওয়ার আগেও form কাজ করে, কারণ `<form action>` native-ভাবে post করে।
        """,
        quick_en=r"""Write a `'use server'` action `(prevState, formData)` that checks the session, validates with Zod `safeParse` and returns field errors, saves the post, calls `updateTag('posts')` and redirects. The form uses `useActionState` for errors and `isPending`.""",
        quick_bn=r"""একটা `'use server'` action `(prevState, formData)` লেখো যেটা session check করে, Zod `safeParse` দিয়ে validate করে field error return করে, post save করে, `updateTag('posts')` call করে, তারপর redirect করে। Form-এ error আর `isPending`-এর জন্য `useActionState` ব্যবহার হয়।""",
        ex_en=r"""
            **Why these choices**
            - `safeParse` + `z.flattenError(...).fieldErrors` (Zod 4) gives a plain, serialisable object the client can render per field.
            - `updateTag` exists only in Server Actions and expires the tag right away, so the redirected page waits for fresh data. In a webhook/Route Handler you'd use `revalidateTag(tag, 'max')` instead.
            - `redirect()` throws a special control-flow error, so call it **outside** any `try/catch`, after the work is done.

            **Edge cases:** duplicate submissions (disable the button, or use an idempotency key), very large bodies (Server Actions accept 1 MB by default — `serverActions.bodySizeLimit`), and returning internal error messages (log details on the server, return a generic message).
        """,
        ex_bn=r"""
            **কেন এই সিদ্ধান্তগুলো**
            - `safeParse` + `z.flattenError(...).fieldErrors` (Zod 4) একটা সাধারণ, serialisable object দেয়, যেটা client প্রতিটা field-এর জন্য দেখাতে পারে।
            - `updateTag` শুধু Server Action-এই আছে আর tag সাথে সাথে expire করে, তাই redirect হওয়া page fresh data-র জন্য অপেক্ষা করে। Webhook/Route Handler-এ এর বদলে `revalidateTag(tag, 'max')` ব্যবহার করতে হয়।
            - `redirect()` একটা বিশেষ control-flow error throw করে, তাই কাজ শেষ হওয়ার পর যেকোনো `try/catch`-এর **বাইরে** এটা call করো।

            **Edge case:** একাধিকবার submit (button disable করো, বা idempotency key ব্যবহার করো), খুব বড় body (Server Action default-ভাবে ১ MB পর্যন্ত নেয় — `serverActions.bodySizeLimit`), আর ভেতরের error message ফেরত পাঠানো (বিস্তারিত server-এ log করো, generic message return করো)।
        """,
        tip_en=r"""Narrate the five steps in order (auth → validate → write → invalidate → redirect) and explain *why* each step lives on the server. Mentioning `updateTag` vs `revalidateTag` shows you know the v16 caching APIs.""",
        tip_bn=r"""পাঁচটা ধাপ ক্রম অনুযায়ী বলো (auth → validate → write → invalidate → redirect), আর ব্যাখ্যা করো প্রতিটা ধাপ *কেন* server-এ থাকে। `updateTag` বনাম `revalidateTag`-এর কথা বললে বোঝা যায় তুমি v16-এর caching API জানো।""",
        mist_en=r"""Validating only on the client, calling `redirect()` inside `try/catch`, or forgetting to invalidate the cache so the list doesn't show the new post.""",
        mist_bn=r"""শুধু client-এ validate করা, `try/catch`-এর ভেতরে `redirect()` call করা, অথবা cache invalidate করতে ভুলে যাওয়া — ফলে list-এ নতুন post দেখা যায় না।""",
        code=r"""
            // app/posts/actions.ts
            'use server';

            import { z } from 'zod';
            import { updateTag } from 'next/cache';
            import { redirect } from 'next/navigation';
            import { getSession } from '@/lib/auth';
            import { db } from '@/lib/db';

            const PostSchema = z.object({
              title: z.string().trim().min(3, 'Title must be at least 3 characters').max(120),
              body: z.string().trim().min(10, 'Write at least 10 characters'),
            });

            export type PostFormState = {
              errors?: { title?: string[]; body?: string[] };
              message?: string;
            };

            export async function createPost(_prev: PostFormState, formData: FormData): Promise<PostFormState> {
              const session = await getSession();
              if (!session) return { message: 'Your session expired. Please log in again.' };

              const parsed = PostSchema.safeParse({
                title: formData.get('title'),
                body: formData.get('body'),
              });
              if (!parsed.success) {
                return { errors: z.flattenError(parsed.error).fieldErrors };
              }

              const post = await db.post.create({
                data: { ...parsed.data, authorId: session.userId },
              });

              updateTag('posts');            // list cached with cacheTag('posts') is expired now
              redirect(`/posts/${post.id}`); // outside try/catch
            }

            // app/posts/new/post-form.tsx
            'use client';

            import { useActionState } from 'react';
            import { createPost, type PostFormState } from '../actions';

            export function PostForm() {
              const [state, formAction, isPending] = useActionState<PostFormState, FormData>(createPost, {});

              return (
                <form action={formAction}>
                  <label htmlFor="title">Title</label>
                  <input id="title" name="title" />
                  {state.errors?.title && <p className="error">{state.errors.title[0]}</p>}

                  <label htmlFor="body">Body</label>
                  <textarea id="body" name="body" />
                  {state.errors?.body && <p className="error">{state.errors.body[0]}</p>}

                  {state.message && <p role="alert">{state.message}</p>}
                  <button disabled={isPending}>{isPending ? 'Publishing…' : 'Publish'}</button>
                </form>
              );
            }
        """,
        lang="tsx",
        time="O(1) per request (excluding the database write)", space="O(size of the submitted form)",
        follow=[
            ("Why is a Server Action effectively a public endpoint, and what does that mean for security?", "Server Action কেন আসলে একটা public endpoint, আর security-র জন্য এর মানে কী?"),
            ("How would you add an optimistic update so the post appears before the server responds?", "Server response-এর আগেই post দেখাতে optimistic update কীভাবে যোগ করবে?"),
        ],
        related=["next-004"],
        refs=[N_MUTATING, N_SA_GUIDE, N_UPDATETAG],
    ),
    # ------------------------------------------------------------------ next-023
    Q(
        id="next-023", sub="Server Actions Security", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["server-actions", "security", "authorization", "idor", "validation"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""Server Actions look like normal function calls. What are the security risks, and how do you secure a `deletePost` action properly?""",
        q_bn=r"""Server Action দেখতে সাধারণ function call-এর মতো। এর security ঝুঁকি কী, আর একটা `deletePost` action কীভাবে ঠিকমতো সুরক্ষিত করবে?""",
        a_en=r"""
            Every exported Server Action is effectively a **public HTTP POST endpoint**. Anyone can call it directly with any arguments — not only through your form — so it needs the same protection as an API route.

            **Risks**
            - Missing **authentication/authorization** → IDOR: user A deletes user B's post by sending B's id.
            - **Unvalidated input**: TypeScript types don't exist at runtime; arguments can be anything.
            - **Data leaks** through return values (returning a whole DB row with internal fields).
            - Relying on **`proxy.ts`** for protection: actions are POSTs to the page route, and a matcher change can silently skip them.
            - **Abuse/DoS**: expensive actions without rate limits.

            **What I do in every action**
            1. Authenticate via a server-only data-access layer (`verifySession()`).
            2. Validate input with a schema (Zod).
            3. Authorize on the specific resource (owner or admin).
            4. Rate-limit sensitive or expensive actions.
            5. Return a minimal result, log details server-side.

            Next.js adds defence in depth — POST-only, an `Origin` vs host check against CSRF (`serverActions.allowedOrigins` for proxies), unguessable action IDs, dead-code elimination of unused actions, and encryption of closed-over variables — but none of that replaces your own checks.
        """,
        a_bn=r"""
            প্রতিটা export করা Server Action আসলে একটা **public HTTP POST endpoint**। যে কেউ যেকোনো argument দিয়ে সরাসরি এটা call করতে পারে — শুধু তোমার form দিয়ে না — তাই এর API route-এর মতোই সুরক্ষা দরকার।

            **ঝুঁকি**
            - **Authentication/authorization** না থাকা → IDOR: user A, user B-এর id পাঠিয়ে B-এর post মুছে দেয়।
            - **Validate না করা input**: runtime-এ TypeScript type-এর অস্তিত্ব নেই; argument যা খুশি হতে পারে।
            - Return value দিয়ে **data leak** (ভেতরের field-সহ পুরো DB row return করা)।
            - সুরক্ষার জন্য **`proxy.ts`**-এর উপর ভরসা: action হলো page route-এ POST, আর matcher বদলালে চুপচাপ এগুলো বাদ পড়তে পারে।
            - **অপব্যবহার/DoS**: rate limit ছাড়া expensive action।

            **প্রতিটা action-এ আমি যা করি**
            1. Server-only data-access layer (`verifySession()`) দিয়ে authenticate।
            2. Schema (Zod) দিয়ে input validate।
            3. নির্দিষ্ট resource-এর উপর authorize (owner বা admin)।
            4. সংবেদনশীল বা expensive action-এ rate limit।
            5. ন্যূনতম result return, বিস্তারিত server-এ log।

            Next.js বাড়তি স্তরের সুরক্ষা দেয় — শুধু POST, CSRF ঠেকাতে `Origin` বনাম host check (proxy থাকলে `serverActions.allowedOrigins`), অনুমান করা যায় না এমন action ID, ব্যবহার না হওয়া action বাদ দেওয়া, আর closure-এ ধরা variable encrypt করা — কিন্তু এগুলোর কোনোটাই তোমার নিজের check-এর বিকল্প না।
        """,
        quick_en=r"""Every exported Server Action is a public POST endpoint, so the risks are missing auth (IDOR), unvalidated input, leaky return values and abuse. In each action authenticate, validate with a schema, authorize on the specific resource, rate-limit and return minimal data; never rely on `proxy.ts`.""",
        quick_bn=r"""প্রতিটা export করা Server Action একটা public POST endpoint, তাই ঝুঁকি হলো auth না থাকা (IDOR), validate না করা input, বেশি data return করা আর অপব্যবহার। প্রতিটা action-এ authenticate করো, schema দিয়ে validate করো, নির্দিষ্ট resource-এর উপর authorize করো, rate-limit দাও আর অল্প data return করো; `proxy.ts`-এর উপর ভরসা করো না।""",
        ex_en=r"""
            - **Data Access Layer (DAL):** centralise session verification and authorization in `server-only` modules, wrapped in React `cache()` so multiple checks per request hit the session store once.
            - **Bound arguments and closures** are encrypted, but they still travel to the client and back — don't put secrets in them, and re-check authorization anyway.
            - **Errors:** thrown errors reach the client as generic messages in production; return expected errors (validation, forbidden) as values.
            - **Patch management:** React published critical Server Components vulnerabilities in December 2025 — keep `react`, `react-dom` and `next` on the latest patch releases.
            - **Body size:** actions accept 1 MB by default (`serverActions.bodySizeLimit`); increase only where needed (uploads).
        """,
        ex_bn=r"""
            - **Data Access Layer (DAL):** session verification আর authorization `server-only` module-এ এক জায়গায় রাখো, React `cache()`-এ wrap করে, যাতে এক request-এ একাধিক check হলেও session store-এ একবারই যায়।
            - **Bound argument আর closure** encrypt হয়, কিন্তু তবুও client-এ গিয়ে আবার ফিরে আসে — এগুলোতে secret রেখো না, আর authorization আবার check করো।
            - **Error:** production-এ throw করা error client-এ generic message হিসেবে পৌঁছায়; প্রত্যাশিত error (validation, forbidden) value হিসেবে return করো।
            - **Patch management:** React ২০২৫-এর ডিসেম্বরে Server Components-এর গুরুতর vulnerability প্রকাশ করেছে — `react`, `react-dom` আর `next` সর্বশেষ patch release-এ রাখো।
            - **Body size:** action default-ভাবে ১ MB পর্যন্ত নেয় (`serverActions.bodySizeLimit`); শুধু যেখানে দরকার (upload) সেখানে বাড়াও।
        """,
        tip_en=r"""Open with the one sentence that matters — "a Server Action is a public POST endpoint" — then walk through authn → validate → authz → rate-limit → minimal response. Naming IDOR and the `proxy.ts` matcher gap shows real security awareness.""",
        tip_bn=r"""সবচেয়ে গুরুত্বপূর্ণ বাক্য দিয়ে শুরু করো — "Server Action একটা public POST endpoint" — তারপর authn → validate → authz → rate-limit → ন্যূনতম response ধাপে ধাপে বলো। IDOR আর `proxy.ts` matcher-এর ফাঁকের কথা বললে আসল security সচেতনতা বোঝা যায়।""",
        mist_en=r"""Assuming an action is safe because only logged-in users see the button, trusting TypeScript parameter types, or checking only that a user is logged in without checking they own the resource.""",
        mist_bn=r"""ভাবা যে শুধু logged-in user button দেখে বলে action নিরাপদ, TypeScript parameter type-এর উপর ভরসা করা, অথবা user logged in কি না শুধু সেটা check করা — resource-টা তার কি না সেটা check না করা।""",
        code=r"""
            // lib/dal.ts — server-only data access layer
            import 'server-only';
            import { cache } from 'react';
            import { cookies } from 'next/headers';
            import { decrypt } from './session';

            export const verifySession = cache(async () => {
              const token = (await cookies()).get('session')?.value;
              const session = token ? await decrypt(token) : null;
              if (!session?.userId) throw new Error('Unauthorized');
              return { userId: String(session.userId), role: session.role as 'user' | 'admin' };
            });

            // app/posts/actions.ts
            'use server';

            import { z } from 'zod';
            import { updateTag } from 'next/cache';
            import { verifySession } from '@/lib/dal';
            import { rateLimit } from '@/lib/rate-limit';
            import { db } from '@/lib/db';

            const DeleteInput = z.object({ postId: z.uuid() });

            export async function deletePost(input: unknown) {
              const { userId, role } = await verifySession();                        // 1. authenticate
              await rateLimit(`delete-post:${userId}`, { limit: 20, windowSec: 60 });  // 2. throttle
              const parsed = DeleteInput.safeParse(input);                            // 3. validate
              if (!parsed.success) return { ok: false, error: 'Invalid input' };

              const post = await db.post.findUnique({
                where: { id: parsed.data.postId },
                select: { authorId: true },
              });
              if (!post) return { ok: false, error: 'Not found' };
              if (post.authorId !== userId && role !== 'admin') {                     // 4. authorize (no IDOR)
                return { ok: false, error: 'Forbidden' };
              }

              await db.post.delete({ where: { id: parsed.data.postId } });
              updateTag('posts');
              return { ok: true };                                                     // 5. minimal response
            }
        """,
        lang="typescript",
        follow=[
            ("Why isn't a check in `proxy.ts` enough to protect Server Actions?", "Server Action সুরক্ষিত রাখতে `proxy.ts`-এর check কেন যথেষ্ট না?"),
            ("How does Next.js protect Server Actions against CSRF, and when do you need `allowedOrigins`?", "Next.js কীভাবে Server Action-কে CSRF থেকে রক্ষা করে, আর কখন `allowedOrigins` লাগে?"),
        ],
        related=["next-013"],
        refs=[N_DATA_SECURITY, N_SA_CONFIG, OWASP_IDOR],
    ),
    # ------------------------------------------------------------------ next-030
    Q(
        id="next-030", sub="Self-hosted Caching Architecture", diff="extreme", type="system-design",
        prio="medium", market="international", mins=20,
        tags=["self-hosting", "multi-region", "cache-handlers", "version-skew", "kubernetes"],
        ver="Next.js 16.4 (Cache Components, self-hosted)", vs=True, status="stable",
        q_en=r"""
            You self-host a Next.js 16 app with Cache Components on Kubernetes: 6 pods across two regions (Mumbai and Singapore) behind a CDN. Problems: users see different content depending on which pod answers, revalidation "works sometimes", and during deploys some users get "Failed to find Server Action". Design the caching and deployment architecture.
        """,
        q_bn=r"""
            তুমি Kubernetes-এ Cache Components-সহ একটা Next.js 16 app self-host করছ: দুটো region-এ (Mumbai আর Singapore) ৬টা pod, সামনে একটা CDN। সমস্যা: কোন pod উত্তর দিচ্ছে তার উপর নির্ভর করে user আলাদা content দেখে, revalidation "মাঝে মাঝে কাজ করে", আর deploy-এর সময় কিছু user "Failed to find Server Action" পায়। Caching আর deployment architecture design করো।
        """,
        a_en=r"""
            *(Advanced, senior-level design question.)* All three symptoms come from treating six processes as one app without sharing state.

            **Root causes**
            - The default `'use cache'` handler is an **in-memory LRU per process**, and the ISR/page cache lives on each pod's disk.
            - `revalidateTag()` on one pod only invalidates **that pod**.
            - Each build generates its own Server Actions encryption key, and rolling deploys mix old clients with new servers (**version skew**).

            **Design**
            1. **Build once, deploy everywhere.** One image per commit for all pods and regions. Set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` at build time and `deploymentId` (e.g. the git SHA) so Next.js detects skew and does a hard navigation instead of calling missing actions or chunks.
            2. **Shared cache.** Configure `cacheHandlers` (for `'use cache'`/`'use cache: remote'`) and `cacheHandler` (ISR/route cache) backed by Redis. Implement `updateTags()` to write tag-invalidation timestamps to shared storage and `refreshTags()` to sync them before each request, so every pod learns about invalidations.
            3. **Cross-region.** Keep a Redis per region for low-latency reads and replicate only **invalidation events** (tiny) between regions via a stream or pub/sub. Accept bounded staleness (seconds) and use `updateTag`/`{ expire: 0 }` where correctness matters.
            4. **CDN.** Hashed static assets are immutable and cached forever; prerendered shells can be cached publicly; dynamic responses are `private`. Purge or use short `s-maxage` for HTML that tags can change. Make sure the CDN and ingress don't buffer streaming responses.
            5. **Deploys.** Rolling updates with readiness probes, keep old static assets available for clients still on the previous version, and graceful shutdown on `SIGTERM` (drain 10–30 s so `after()` callbacks finish).
        """,
        a_bn=r"""
            *(Advanced, senior-level design প্রশ্ন।)* তিনটা লক্ষণই এসেছে ছয়টা process-কে state share না করে একটা app হিসেবে চালানোর কারণে।

            **Root cause**
            - Default `'use cache'` handler হলো **প্রতি process-এ in-memory LRU**, আর ISR/page cache থাকে প্রতিটা pod-এর disk-এ।
            - এক pod-এ `revalidateTag()` call করলে শুধু **ওই pod**-ই invalidate হয়।
            - প্রতিটা build নিজের Server Actions encryption key তৈরি করে, আর rolling deploy পুরনো client-কে নতুন server-এর সাথে মিশিয়ে ফেলে (**version skew**)।

            **Design**
            1. **একবার build, সব জায়গায় deploy।** সব pod আর region-এর জন্য প্রতি commit-এ একটাই image। Build time-এ `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` আর `deploymentId` (যেমন git SHA) set করো, যাতে Next.js skew ধরতে পারে আর অনুপস্থিত action বা chunk call না করে hard navigation করে।
            2. **Shared cache।** Redis-backed `cacheHandlers` (`'use cache'`/`'use cache: remote'`-এর জন্য) আর `cacheHandler` (ISR/route cache) configure করো। `updateTags()` implement করো, যাতে tag-invalidation timestamp shared storage-এ লেখা হয়, আর `refreshTags()` প্রতিটা request-এর আগে সেগুলো sync করে — ফলে প্রতিটা pod invalidation-এর খবর পায়।
            3. **Cross-region।** কম latency-তে পড়ার জন্য প্রতি region-এ একটা Redis রাখো, আর region-গুলোর মধ্যে stream বা pub/sub দিয়ে শুধু **invalidation event** (খুব ছোট) replicate করো। সীমিত staleness (কয়েক সেকেন্ড) মেনে নাও, আর যেখানে correctness জরুরি সেখানে `updateTag`/`{ expire: 0 }` ব্যবহার করো।
            4. **CDN।** Hash-যুক্ত static asset immutable, চিরকাল cache থাকে; prerender করা shell public-ভাবে cache করা যায়; dynamic response `private`। Tag দিয়ে বদলাতে পারে এমন HTML-এর জন্য purge করো বা ছোট `s-maxage` দাও। নিশ্চিত করো CDN আর ingress streaming response buffer করে না।
            5. **Deploy।** Readiness probe-সহ rolling update, আগের version-এ থাকা client-দের জন্য পুরনো static asset রেখে দেওয়া, আর `SIGTERM`-এ graceful shutdown (১০–৩০ সেকেন্ড drain, যাতে `after()` callback শেষ হয়)।
        """,
        quick_en=r"""All three symptoms come from per-pod state: in-memory caches, per-pod revalidation and per-build action keys. Build one image with a fixed `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` and `deploymentId`, use a Redis-backed shared cache handler with tag sync, and replicate only invalidation events across regions.""",
        quick_bn=r"""তিনটা সমস্যাই আসে pod-ভিত্তিক state থেকে: in-memory cache, pod ধরে revalidation, আর প্রতি build-এ আলাদা action key। নির্দিষ্ট `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` আর `deploymentId`-সহ একটাই image বানাও, tag sync-সহ Redis-backed shared cache handler ব্যবহার করো, আর region-এর মধ্যে শুধু invalidation event replicate করো।""",
        ex_en=r"""
            **Failure scenarios**
            - **Redis unavailable:** handlers must catch errors and return a cache miss from `get()` (an unhandled error becomes a render error). Decide explicitly: serve from a short local cache (availability) or render fresh (correctness, more DB load).
            - **Thundering herd** after invalidating a hot tag: prefer `revalidateTag(tag, 'max')` (stale-while-revalidate spreads regeneration) and avoid giant catch-all tags like `products` for everything.
            - **Region partition:** invalidations queue up and apply when the link returns; monitor "invalidation lag".

            **Trade-offs:** a remote cache adds a network round trip per read, so it pays off only for expensive data with a high hit rate; keep cheap, hot data in the in-memory `default` handler. Note that cache keys include the build/deployment ID, so a new deploy starts with a cold cache — pre-warm critical routes after deploying.

            **Observability:** cache hit ratio per handler, invalidation lag, version-skew reloads, and `NEXT_PRIVATE_DEBUG_CACHE=1` in staging.
        """,
        ex_bn=r"""
            **Failure scenario**
            - **Redis পাওয়া যাচ্ছে না:** handler-কে error catch করে `get()` থেকে cache miss return করতে হবে (unhandled error render error হয়ে যায়)। স্পষ্টভাবে সিদ্ধান্ত নাও: ছোট local cache থেকে serve করবে (availability) নাকি নতুন করে render করবে (correctness, বেশি DB load)।
            - জনপ্রিয় tag invalidate করার পর **thundering herd**: `revalidateTag(tag, 'max')` পছন্দ করো (stale-while-revalidate regeneration ছড়িয়ে দেয়), আর সবকিছুর জন্য `products`-এর মতো বিশাল catch-all tag এড়িয়ে চলো।
            - **Region partition:** invalidation জমা থাকে আর সংযোগ ফিরলে apply হয়; "invalidation lag" monitor করো।

            **Trade-off:** remote cache প্রতিটা read-এ একটা network round trip যোগ করে, তাই এটা কেবল বেশি hit rate-ওয়ালা expensive data-র ক্ষেত্রে লাভজনক; সস্তা, ঘন ঘন পড়া data in-memory `default` handler-এ রাখো। মনে রেখো cache key-তে build/deployment ID থাকে, তাই নতুন deploy ঠান্ডা cache দিয়ে শুরু হয় — deploy-এর পর গুরুত্বপূর্ণ route pre-warm করো।

            **Observability:** প্রতিটা handler-এর cache hit ratio, invalidation lag, version-skew reload, আর staging-এ `NEXT_PRIVATE_DEBUG_CACHE=1`।
        """,
        tip_en=r"""Map each symptom to its root cause before proposing anything — interviewers reward diagnosis. Then cover build/deploy consistency, shared cache + tag coordination, CDN rules and failure modes, and finish with the trade-off of remote caching.""",
        tip_bn=r"""কিছু প্রস্তাব করার আগে প্রতিটা লক্ষণকে তার root cause-এর সাথে মেলাও — interviewer সঠিক diagnosis-কে মূল্য দেয়। তারপর build/deploy-এর সামঞ্জস্য, shared cache + tag coordination, CDN-এর নিয়ম আর failure mode কভার করো, আর শেষে remote caching-এর trade-off বলো।""",
        mist_en=r"""Fixing it with sticky sessions (hides the problem, breaks on pod restarts), rebuilding the image per environment with different keys, or caching dynamic personalised HTML at the CDN.""",
        mist_bn=r"""Sticky session দিয়ে "ঠিক" করা (সমস্যা লুকায়, pod restart হলে ভেঙে যায়), প্রতি environment-এ আলাদা key দিয়ে image আবার build করা, অথবা dynamic personalised HTML CDN-এ cache করা।""",
        code=r"""
            // next.config.ts
            import type { NextConfig } from 'next';

            const nextConfig: NextConfig = {
              output: 'standalone',
              cacheComponents: true,
              deploymentId: process.env.GIT_SHA,           // version-skew protection
              cacheHandler: require.resolve('./cache/isr-handler.js'),   // ISR / route cache
              cacheMaxMemorySize: 0,                         // don't keep a per-pod copy
              cacheHandlers: {
                default: require.resolve('./cache/redis-default.js'),   // 'use cache'
                remote: require.resolve('./cache/redis-remote.js'),     // 'use cache: remote'
              },
            };

            export default nextConfig;

            // cache/redis-default.js (excerpt) — distributed tag coordination
            const { createClient } = require('redis');

            const redis = createClient({ url: process.env.REDIS_URL });
            redis.connect();
            const localTagTimestamps = new Map(); // tag -> last invalidation (ms)

            module.exports = {
              // ...get() and set() store entries in the regional Redis...

              async updateTags(tags) {                 // called by revalidateTag()/updateTag()
                const now = Date.now();
                const tx = redis.multi();
                for (const tag of tags) {
                  tx.set(`tag:${tag}`, String(now));
                  tx.sAdd('revalidated-tags', tag);
                }
                await tx.exec();
                await redis.publish('tag-invalidations', JSON.stringify({ tags, at: now })); // other region
              },

              async refreshTags() {                    // runs before cache reads on each request
                const tags = await redis.sMembers('revalidated-tags');
                if (tags.length === 0) return;
                const values = await redis.mGet(tags.map((t) => `tag:${t}`));
                tags.forEach((t, i) => localTagTimestamps.set(t, Number(values[i])));
              },

              async getExpiration(tags) {
                return Math.max(0, ...tags.map((t) => localTagTimestamps.get(t) ?? 0));
              },
            };
        """,
        lang="typescript",
        follow=[
            ("How would you pre-warm the cache after a deploy without overloading the database?", "Database-এর উপর চাপ না দিয়ে deploy-এর পর cache কীভাবে pre-warm করবে?"),
            ("What happens to an open browser tab when you deploy a new version with `deploymentId` set?", "`deploymentId` set করা অবস্থায় নতুন version deploy করলে খোলা browser tab-এর কী হয়?"),
            ("When is `'use cache: remote'` worth its network cost?", "কখন `'use cache: remote'`-এর network খরচ সার্থক?"),
        ],
        related=["next-023"],
        refs=[N_SELF_HOST, N_CACHE_HANDLERS, N_REVALIDATION],
    ),
]

if __name__ == "__main__":
    save("nextjs", "b1", QUESTIONS)
