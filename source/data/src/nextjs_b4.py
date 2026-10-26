# Next.js — batch 4 (next-011, 020..022, 027..029, 032)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_PROXY = ("Next.js Docs — proxy.js", "https://nextjs.org/docs/app/api-reference/file-conventions/proxy")
N_PROXY_GUIDE = ("Next.js Docs — Proxy (getting started)", "https://nextjs.org/docs/app/getting-started/proxy")
N_UPGRADE16 = ("Next.js Docs — Upgrading to Version 16", "https://nextjs.org/docs/app/guides/upgrading/version-16")
N_AUTH = ("Next.js Docs — Authentication", "https://nextjs.org/docs/app/guides/authentication")
N_DATA_SECURITY = ("Next.js Docs — Data Security", "https://nextjs.org/docs/app/guides/data-security")
N_SC = ("Next.js Docs — Server and Client Components", "https://nextjs.org/docs/app/getting-started/server-and-client-components")
R_CTX = ("react.dev — createContext", "https://react.dev/reference/react/createContext")
N_ISR = ("Next.js Docs — Incremental Static Regeneration", "https://nextjs.org/docs/app/guides/incremental-static-regeneration")
N_ISR_CC = ("Next.js Docs — ISR with Cache Components", "https://nextjs.org/docs/app/guides/incremental-static-regeneration-cache-components")
N_GSP = ("Next.js Docs — getStaticProps (Pages Router)", "https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props")
N_PARALLEL = ("Next.js Docs — Parallel Routes", "https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes")
N_INTERCEPT = ("Next.js Docs — Intercepting Routes", "https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes")
N_BUNDLING = ("Next.js Docs — Optimizing package bundling", "https://nextjs.org/docs/app/guides/package-bundling")
N_LAZY = ("Next.js Docs — Lazy Loading", "https://nextjs.org/docs/app/guides/lazy-loading")
N_OPI = ("Next.js Docs — optimizePackageImports", "https://nextjs.org/docs/app/api-reference/config/next-config-js/optimizePackageImports")
N_ERROR = ("Next.js Docs — error.js", "https://nextjs.org/docs/app/api-reference/file-conventions/error")
N_ERROR_HANDLING = ("Next.js Docs — Error Handling", "https://nextjs.org/docs/app/getting-started/error-handling")
N_CACHING = ("Next.js Docs — Caching (Cache Components)", "https://nextjs.org/docs/app/getting-started/caching")
N_USE_CACHE_PRIVATE = ("Next.js Docs — 'use cache: private'", "https://nextjs.org/docs/app/api-reference/directives/use-cache-private")

QUESTIONS = [
    # ------------------------------------------------------------------ next-011
    Q(
        id="next-011", sub="Proxy (formerly Middleware)", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["proxy", "middleware", "nextjs-16", "file-conventions"],
        ver="Next.js 16.4", vs=True, status="stable",
        q_en=r"""In a new Next.js 16 project you want to redirect some requests based on a cookie **before** routing happens. Which file do you create?""",
        q_bn=r"""একটা নতুন Next.js 16 project-এ তুমি cookie দেখে কিছু request routing হওয়ার **আগেই** redirect করতে চাও। কোন file তৈরি করবে?""",
        options=[
            ("`middleware.ts` in the project root, exporting a `middleware` function", "Project root-এ `middleware.ts`, যেটা একটা `middleware` function export করে"),
            ("`proxy.ts` in the project root (next to `app/`), exporting a `proxy` function", "Project root-এ (`app/`-এর পাশে) `proxy.ts`, যেটা একটা `proxy` function export করে"),
            ("`pages/_middleware.ts`, exporting a default function", "`pages/_middleware.ts`, যেটা একটা default function export করে"),
            ("`app/proxy/route.ts`, exporting a `GET` handler", "`app/proxy/route.ts`, যেটা একটা `GET` handler export করে"),
        ],
        correct=1,
        a_en=r"""Next.js 16 renamed Middleware to **Proxy**: create `proxy.ts` (or `.js`) at the project root — or inside `src/` — at the same level as `app/`, and export a `proxy` function (or a default export). An optional `config.matcher` limits which paths it runs on.""",
        a_bn=r"""Next.js 16 Middleware-এর নাম বদলে **Proxy** রেখেছে: project root-এ — অথবা `src/`-এর ভেতরে — `app/`-এর একই স্তরে `proxy.ts` (বা `.js`) তৈরি করো, আর একটা `proxy` function (বা default export) export করো। ঐচ্ছিক `config.matcher` ঠিক করে এটা কোন path-এ চলবে।""",
        quick_en=r"""Create `proxy.ts` at the project root (or in `src/`, next to `app/`) exporting a `proxy` function. Next.js 16 renamed Middleware to Proxy, so `middleware.ts` is the deprecated legacy name; use `config.matcher` to limit which paths it runs on.""",
        quick_bn=r"""Project root-এ (বা `src/`-এ, `app/`-এর পাশে) `proxy.ts` বানাও যেটা একটা `proxy` function export করে। Next.js 16 Middleware-এর নাম বদলে Proxy রেখেছে, তাই `middleware.ts` এখন deprecated legacy নাম; কোন path-এ চলবে তা `config.matcher` দিয়ে সীমিত করো।""",
        ex_en=r"""
            The tempting answer is `middleware.ts` — it's in countless tutorials and still exists, but it's **deprecated** in v16 (kept only for Edge-runtime use cases). The rename makes the purpose clearer: it's a network-boundary layer in front of the app, not Express-style middleware. `proxy.ts` runs on the **Node.js runtime** by default, and `npx @next/codemod@canary middleware-to-proxy .` renames both the file and the function.

            `pages/_middleware.ts` was the short-lived Next.js 12 beta convention, and a Route Handler only runs when its own URL is requested — it can't intercept other routes.

            Typical uses: auth redirects (optimistic, cookie-based), locale redirects, rewrites for A/B tests, and setting headers. Keep it fast and don't use it as your only authorization layer.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো `middleware.ts` — অসংখ্য tutorial-এ আছে আর এখনো এর অস্তিত্ব আছে, কিন্তু v16-এ এটা **deprecated** (শুধু Edge-runtime-এর ক্ষেত্রে রাখা হয়েছে)। নাম বদলানোয় উদ্দেশ্যটা স্পষ্ট হয়েছে: এটা app-এর সামনের একটা network-boundary layer, Express-ধরনের middleware না। `proxy.ts` default-ভাবে **Node.js runtime**-এ চলে, আর `npx @next/codemod@canary middleware-to-proxy .` file আর function — দুটোরই নাম বদলে দেয়।

            `pages/_middleware.ts` ছিল Next.js 12 beta-র স্বল্পস্থায়ী নিয়ম, আর Route Handler শুধু তার নিজের URL-এ request এলেই চলে — অন্য route intercept করতে পারে না।

            সাধারণ ব্যবহার: auth redirect (optimistic, cookie-ভিত্তিক), locale redirect, A/B test-এর জন্য rewrite, আর header set করা। এটা দ্রুত রাখো, আর একমাত্র authorization layer হিসেবে ব্যবহার করো না।
        """,
        tip_en=r"""Mention the rename *and* the reason (clearer purpose, Node.js runtime by default). Interviewers often ask this to see whether your knowledge is current.""",
        tip_bn=r"""নাম বদল *আর* তার কারণ — দুটোই বলো (উদ্দেশ্য স্পষ্ট, default-ভাবে Node.js runtime)। তোমার জ্ঞান আপডেটেড কি না দেখতে interviewer প্রায়ই এটা জিজ্ঞেস করে।""",
        refs=[N_PROXY, N_PROXY_GUIDE, N_UPGRADE16],
    ),
    # ------------------------------------------------------------------ next-020
    Q(
        id="next-020", sub="Authentication", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["authentication", "authorization", "server-actions", "proxy", "dal"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""
            `proxy.ts` redirects users without a session cookie away from `/dashboard`. The dashboard has a delete button that calls the `deletePost` Server Action. Where must the **authoritative** check "is this user allowed to delete this post?" happen?
        """,
        q_bn=r"""
            `proxy.ts` session cookie ছাড়া user-দের `/dashboard` থেকে সরিয়ে দেয়। Dashboard-এ একটা delete button আছে, যেটা `deletePost` Server Action call করে। "এই user কি এই post মুছতে পারবে?" — এই **চূড়ান্ত** check কোথায় হতে হবে?
        """,
        options=[
            ("Only in `proxy.ts`, because it runs before every request to `/dashboard`", "শুধু `proxy.ts`-এ, কারণ এটা `/dashboard`-এর প্রতিটা request-এর আগে চলে"),
            ("Inside the `deletePost` Server Action (or the data-access function it calls), on every call", "`deletePost` Server Action-এর ভেতরে (বা এটা যে data-access function call করে সেখানে), প্রতিটা call-এ"),
            ("In `app/dashboard/layout.tsx`, since every dashboard page renders inside it", "`app/dashboard/layout.tsx`-এ, কারণ প্রতিটা dashboard page এর ভেতরেই render হয়"),
            ("In the Client Component, by hiding the delete button from users who don't own the post", "Client Component-এ, post-এর মালিক না এমন user-দের থেকে delete button লুকিয়ে"),
        ],
        correct=1,
        a_en=r"""Inside the Server Action (ideally via a server-only data-access layer). A Server Action is a public POST endpoint: anyone can call it directly with any post id, so it must verify the session **and** ownership/role itself every time.""",
        a_bn=r"""Server Action-এর ভেতরে (আদর্শভাবে একটা server-only data-access layer-এর মাধ্যমে)। Server Action হলো একটা public POST endpoint: যে কেউ যেকোনো post id দিয়ে সরাসরি এটা call করতে পারে, তাই প্রতিবার এটাকে নিজেই session **আর** ownership/role যাচাই করতে হবে।""",
        quick_en=r"""Inside the `deletePost` Server Action (or the data-access function it calls), on every call. A Server Action is a public POST endpoint anyone can call with any id, so `proxy.ts` and hidden buttons are not enough.""",
        quick_bn=r"""`deletePost` Server Action-এর ভেতরে (বা যে data-access function-কে এটা call করে সেখানে), প্রতিবার call-এ। Server Action হলো একটা public POST endpoint, যেকেউ যেকোনো id দিয়ে call করতে পারে, তাই `proxy.ts` বা button লুকানো যথেষ্ট না।""",
        ex_en=r"""
            The tempting answer is `proxy.ts`. Proxy is great for **optimistic** checks (is there a session cookie? redirect early), but it isn't the security boundary: Server Actions are handled as POST requests to the route where they're used, so a matcher change or moving the action to another route can silently remove proxy coverage — and proxy doesn't know who owns post 123 anyway.

            The layout is wrong too: layouts don't re-render on every client navigation and aren't involved when an action is invoked. Hiding the button is UX, not security.

            Recommended pattern: a **Data Access Layer** — `server-only` functions such as `verifySession()` and `canDeletePost(user, post)` — called from every Server Component, Server Action and Route Handler that touches protected data.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো `proxy.ts`। **Optimistic** check-এর জন্য proxy দারুণ (session cookie আছে কি? আগেভাগেই redirect), কিন্তু এটা security boundary না: Server Action যে route-এ ব্যবহার হয় সেখানে POST request হিসেবে সামলানো হয়, তাই matcher বদলালে বা action অন্য route-এ সরালে চুপচাপ proxy-র সুরক্ষা হারিয়ে যেতে পারে — আর post 123-এর মালিক কে, proxy সেটা জানেই না।

            Layout-ও ভুল: প্রতিটা client navigation-এ layout re-render হয় না, আর action call হলে layout জড়িতই থাকে না। Button লুকানো হলো UX, security না।

            Recommended pattern: একটা **Data Access Layer** — `verifySession()` আর `canDeletePost(user, post)`-এর মতো `server-only` function — যেগুলো protected data ছোঁয় এমন প্রতিটা Server Component, Server Action আর Route Handler থেকে call হয়।
        """,
        tip_en=r"""Distinguish "optimistic checks" (proxy, UI) from "authoritative checks" (next to the data). That vocabulary, straight from how Next.js recommends structuring auth, signals real experience.""",
        tip_bn=r""""Optimistic check" (proxy, UI) আর "authoritative check" (data-র পাশে) আলাদা করে বলো। Next.js যেভাবে auth সাজাতে recommend করে, সেখান থেকে আসা এই শব্দগুলো আসল অভিজ্ঞতার ইঙ্গিত দেয়।""",
        related=["next-011"],
        refs=[N_AUTH, N_DATA_SECURITY, N_PROXY],
    ),
    # ------------------------------------------------------------------ next-021
    Q(
        id="next-021", sub="Client Components and Providers", diff="medium", type="debugging",
        prio="high", market="bangladesh", mins=5,
        tags=["context", "providers", "use-client", "root-layout", "debugging"],
        ver="Next.js 16.4 (App Router, React 19.3)", vs=True, status="stable",
        q_en=r"""
            A developer moving from a Vite SPA adds a theme provider to the root layout. The build fails with an error saying `useState` only works in a Client Component. Why does it fail, and what's the right fix?
        """,
        q_bn=r"""
            Vite SPA থেকে আসা একজন developer root layout-এ একটা theme provider যোগ করল। Build fail করছে, error বলছে `useState` শুধু Client Component-এ কাজ করে। কেন fail করছে, আর সঠিক সমাধান কী?
        """,
        a_en=r"""
            In the App Router, `layout.tsx` is a **Server Component** by default. Server Components run once on the server and can't hold state, run effects, or create context — so `useState` and `createContext` fail there.

            The fix is to move the stateful provider into its own **Client Component** file (`app/providers.tsx` with `'use client'`) and render it from the layout around `{children}`.

            The layout stays a Server Component (so it can still export `metadata`), and the pages passed as `children` **stay Server Components too** — a Client Component can render Server Components it receives as children. Only the provider's own code ships to the browser.
        """,
        a_bn=r"""
            App Router-এ `layout.tsx` default-ভাবে একটা **Server Component**। Server Component server-এ একবার চলে, আর state রাখতে, effect চালাতে বা context তৈরি করতে পারে না — তাই সেখানে `useState` আর `createContext` fail করে।

            সমাধান হলো stateful provider-টাকে তার নিজস্ব **Client Component** file-এ সরানো (`'use client'`-সহ `app/providers.tsx`), আর layout থেকে `{children}`-এর চারপাশে এটা render করা।

            Layout Server Component-ই থাকে (তাই এখনো `metadata` export করতে পারে), আর `children` হিসেবে পাঠানো page-গুলোও **Server Component-ই থাকে** — Client Component তার children হিসেবে পাওয়া Server Component render করতে পারে। শুধু provider-এর নিজের code browser-এ যায়।
        """,
        quick_en=r"""`layout.tsx` is a Server Component, which can't use `useState` or create context. Move the provider into a `'use client'` file like `app/providers.tsx` and wrap `{children}` with it; the layout and the pages stay Server Components.""",
        quick_bn=r"""`layout.tsx` একটা Server Component, যেখানে `useState` বা context তৈরি চলে না। Provider-টা `app/providers.tsx`-এর মতো একটা `'use client'` file-এ সরাও আর সেটা দিয়ে `{children}` wrap করো; layout আর page-গুলো Server Component-ই থাকে।""",
        ex_en=r"""
            - **Don't put `'use client'` on the root layout itself.** It would turn the layout and everything it imports into client code and you'd lose the `metadata` export.
            - **Render providers as deep as possible**, e.g. a cart provider only around the shop section, so more of the tree can be optimised.
            - **Store libraries:** create Redux/Zustand stores inside the client provider per request (e.g. in a `useRef`/`useState` initialiser), never as a module-level singleton that the server would share between users.
            - **React 19.3 detail:** a Server Component can now render `<SomeContext value={…}>` directly when the context is imported from a `'use client'` module — handy for passing server data (like the current user) into client context. Stateful providers still need a Client Component.
        """,
        ex_bn=r"""
            - **Root layout-এ নিজেই `'use client'` দিও না।** তাহলে layout আর সে যা import করে সব client code হয়ে যাবে, আর `metadata` export হারাবে।
            - **Provider যত গভীরে সম্ভব render করো**, যেমন cart provider শুধু shop section-এর চারপাশে, যাতে tree-র বেশি অংশ optimise করা যায়।
            - **Store library:** Redux/Zustand store client provider-এর ভেতরে প্রতি request-এ তৈরি করো (যেমন `useRef`/`useState` initialiser-এ), কখনো module-level singleton হিসেবে না — সেটা server-এ বিভিন্ন user-এর মধ্যে share হয়ে যেত।
            - **React 19.3-এর খুঁটিনাটি:** context যদি `'use client'` module থেকে import করা হয়, Server Component এখন সরাসরি `<SomeContext value={…}>` render করতে পারে — server data (যেমন current user) client context-এ পাঠানোর জন্য সুবিধাজনক। তবে stateful provider-এর জন্য এখনো Client Component লাগে।
        """,
        tip_en=r"""Explain the root cause in one line ("layouts are Server Components; state needs a Client Component"), then the providers pattern, then the key insight that children stay Server Components. That last point is what most candidates miss.""",
        tip_bn=r"""এক লাইনে root cause বলো ("layout হলো Server Component; state-এর জন্য Client Component লাগে"), তারপর providers pattern, তারপর মূল অন্তর্দৃষ্টি — children Server Component-ই থাকে। বেশিরভাগ candidate শেষের পয়েন্টটাই মিস করে।""",
        mist_en=r"""Adding `'use client'` to `app/layout.tsx`, or believing that everything rendered inside a client provider becomes a Client Component.""",
        mist_bn=r"""`app/layout.tsx`-এ `'use client'` দেওয়া, অথবা ভাবা যে client provider-এর ভেতরে render হওয়া সবকিছুই Client Component হয়ে যায়।""",
        code=r"""
            // app/layout.tsx
            import { createContext, useState } from 'react';

            export const ThemeContext = createContext('light');

            export default function RootLayout({ children }: { children: React.ReactNode }) {
              const [theme, setTheme] = useState('light');
              return (
                <html lang="en">
                  <body>
                    <ThemeContext value={theme}>{children}</ThemeContext>
                  </body>
                </html>
              );
            }
        """,
        lang="tsx",
        extra=[dict(lang="tsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            // app/providers.tsx
            'use client';

            import { createContext, useState } from 'react';

            type Theme = 'light' | 'dark';
            export const ThemeContext = createContext<{ theme: Theme; setTheme: (t: Theme) => void } | null>(null);

            export function Providers({ children }: { children: React.ReactNode }) {
              const [theme, setTheme] = useState<Theme>('light');
              return <ThemeContext value={{ theme, setTheme }}>{children}</ThemeContext>;
            }

            // app/layout.tsx — still a Server Component
            import type { Metadata } from 'next';
            import { Providers } from './providers';

            export const metadata: Metadata = { title: { default: 'Shop', template: '%s | Shop' } };

            export default function RootLayout({ children }: { children: React.ReactNode }) {
              return (
                <html lang="en">
                  <body>
                    <Providers>{children}</Providers>
                  </body>
                </html>
              );
            }
        """)],
        follow=[
            ("Why do pages passed as `children` to a Client Component remain Server Components?", "Client Component-এ `children` হিসেবে পাঠানো page কেন Server Component-ই থাকে?"),
            ("Why must a Redux store not be a module-level singleton in a Next.js app?", "Next.js app-এ Redux store কেন module-level singleton হওয়া উচিত না?"),
        ],
        related=["next-004", "next-003"],
        refs=[N_SC, R_CTX],
    ),
    # ------------------------------------------------------------------ next-022
    Q(
        id="next-022", sub="ISR and Static Generation", diff="medium", type="conceptual",
        prio="high", market="both", mins=7,
        tags=["isr", "static-generation", "generatestaticparams", "revalidation", "legacy"],
        ver="Next.js 16.4 (Cache Components; previous model and Pages Router labelled)", vs=True, status="stable",
        q_en=r"""How do you implement Incremental Static Regeneration (ISR) for a blog in Next.js 16? Compare the Pages Router, the previous App Router model and Cache Components.""",
        q_bn=r"""Next.js 16-এ একটা blog-এর জন্য Incremental Static Regeneration (ISR) কীভাবে implement করবে? Pages Router, আগের App Router model আর Cache Components-এর তুলনা করো।""",
        a_en=r"""
            ISR means: serve a static page, and regenerate it in the background after a time window or when content changes — static speed with fresh-enough data.

            - **Pages Router (legacy):** `getStaticProps` returns `{ props, revalidate: 3600 }`; `getStaticPaths` lists slugs to prebuild with `fallback: 'blocking'` for the rest; on-demand regeneration uses `res.revalidate('/blog/slug')` from an API route.
            - **App Router, previous model** (Cache Components off): `export const revalidate = 3600` in the page, or per request `fetch(url, { next: { revalidate: 3600, tags: ['post-x'] } })`; `generateStaticParams` replaces `getStaticPaths`; on-demand with `revalidateTag`/`revalidatePath`.
            - **Cache Components (current):** put `'use cache'` with `cacheLife('hours')` and `cacheTag('post-' + slug)` in the data function; `generateStaticParams` prerenders known slugs at build; other slugs are rendered on first request and then cached. When the CMS publishes, a webhook Route Handler calls `revalidateTag('post-' + slug, 'max')`; an editor's Server Action can call `updateTag` for an immediate update.

            In all models, time-based (and `'max'` tag-based) regeneration is stale-while-revalidate: the first visitor after the revalidation window still gets the old page and triggers the rebuild. Exceptions: `updateTag` / `revalidateTag(tag, { expire: 0 })`, and with Cache Components an entry past its `cacheLife` `expire` time, make the next request wait for fresh content.
        """,
        a_bn=r"""
            ISR মানে: একটা static page serve করো, আর নির্দিষ্ট সময় পর বা content বদলালে background-এ সেটা আবার তৈরি করো — static-এর গতি আর যথেষ্ট fresh data।

            - **Pages Router (legacy):** `getStaticProps` return করে `{ props, revalidate: 3600 }`; `getStaticPaths` কোন slug আগে build হবে তার তালিকা দেয়, বাকিগুলোর জন্য `fallback: 'blocking'`; দরকারমতো regeneration হয় API route থেকে `res.revalidate('/blog/slug')` দিয়ে।
            - **App Router, আগের model** (Cache Components বন্ধ): page-এ `export const revalidate = 3600`, অথবা প্রতি request-এ `fetch(url, { next: { revalidate: 3600, tags: ['post-x'] } })`; `getStaticPaths`-এর জায়গায় `generateStaticParams`; দরকারমতো `revalidateTag`/`revalidatePath`।
            - **Cache Components (বর্তমান):** data function-এ `cacheLife('hours')` আর `cacheTag('post-' + slug)`-সহ `'use cache'` দাও; `generateStaticParams` build-এ জানা slug prerender করে; বাকি slug প্রথম request-এ render হয়ে তারপর cache হয়। CMS publish করলে একটা webhook Route Handler `revalidateTag('post-' + slug, 'max')` call করে; editor-এর Server Action সাথে সাথে update-এর জন্য `updateTag` call করতে পারে।

            সব model-এই time-based (আর `'max'`-সহ tag-based) regeneration হলো stale-while-revalidate: revalidation সময় পার হওয়ার পর প্রথম visitor তখনো পুরনো page পায় আর নতুন build শুরু করিয়ে দেয়। ব্যতিক্রম: `updateTag` / `revalidateTag(tag, { expire: 0 })`, আর Cache Components-এ `cacheLife`-এর `expire` সময় পার হওয়া entry — এসব ক্ষেত্রে পরের request fresh content-এর জন্য অপেক্ষা করে।
        """,
        quick_en=r"""ISR serves a static page and regenerates it later. Today you use `'use cache'` with `cacheLife` and `cacheTag`, prebuild known slugs with `generateStaticParams`, and revalidate the tag from a CMS webhook; legacy equivalents are `export const revalidate` and Pages Router `getStaticProps` with `revalidate`.""",
        quick_bn=r"""ISR static page দেয় আর পরে সেটা regenerate করে। এখন `cacheLife` ও `cacheTag`-সহ `'use cache'` ব্যবহার করো, `generateStaticParams` দিয়ে জানা slug আগে build করো, আর CMS webhook থেকে tag revalidate করো; legacy উপায় হলো `export const revalidate` আর Pages Router-এর `revalidate`-সহ `getStaticProps`।""",
        ex_en=r"""
            - **Why tags beat time-based revalidation for a blog:** with a long `cacheLife` plus a tag, posts update within seconds of publishing but aren't regenerated needlessly every hour.
            - **Don't mix models:** in a Cache Components app, `export const revalidate` and `fetch(..., { next: { revalidate } })` are the old way; caching belongs in `'use cache'` scopes.
            - **Self-hosting:** the regenerated pages live in the server cache (disk/memory per instance by default). With several instances you need a shared cache handler, or instances serve different versions.
            - **`generateStaticParams` size:** prebuild only popular slugs to keep build times short; the rest are generated on demand.
        """,
        ex_bn=r"""
            - **Blog-এর জন্য tag কেন time-based revalidation-এর চেয়ে ভালো:** লম্বা `cacheLife` আর একটা tag থাকলে publish-এর কয়েক সেকেন্ডের মধ্যে post update হয়, কিন্তু প্রতি ঘণ্টায় অকারণে regenerate হয় না।
            - **Model গুলিয়ে ফেলো না:** Cache Components app-এ `export const revalidate` আর `fetch(..., { next: { revalidate } })` পুরনো উপায়; caching থাকবে `'use cache'` scope-এ।
            - **Self-hosting:** regenerate হওয়া page থাকে server cache-এ (default-ভাবে প্রতি instance-এর disk/memory)। একাধিক instance থাকলে shared cache handler লাগে, নইলে instance-গুলো আলাদা version দেখায়।
            - **`generateStaticParams`-এর আকার:** build time কম রাখতে শুধু জনপ্রিয় slug আগে build করো; বাকিগুলো দরকারমতো তৈরি হয়।
        """,
        tip_en=r"""Define ISR first, then present the three models side by side with clear labels (legacy / previous / current). Finishing with stale-while-revalidate semantics shows you understand what users actually see.""",
        tip_bn=r"""আগে ISR define করো, তারপর তিনটা model স্পষ্ট label-সহ পাশাপাশি দেখাও (legacy / আগের / বর্তমান)। শেষে stale-while-revalidate semantics বললে বোঝা যায় user আসলে কী দেখে তা তুমি বোঝো।""",
        mist_en=r"""Expecting `revalidate: 60` to update the page exactly every 60 seconds for everyone (it only marks it stale; regeneration happens on the next request), or using `getStaticProps` inside `app/`.""",
        mist_bn=r"""আশা করা যে `revalidate: 60` সবার জন্য ঠিক প্রতি ৬০ সেকেন্ডে page update করবে (এটা শুধু stale চিহ্নিত করে; regeneration হয় পরের request-এ), অথবা `app/`-এর ভেতরে `getStaticProps` ব্যবহার করা।""",
        code=r"""
            // 1) Pages Router (legacy) — pages/blog/[slug].tsx
            export async function getStaticProps({ params }) {
              const post = await cms.getPost(params.slug);
              if (!post) return { notFound: true };
              return { props: { post }, revalidate: 3600 };
            }
            export async function getStaticPaths() {
              return { paths: [], fallback: 'blocking' };
            }

            // 2) App Router, previous model (cacheComponents: false) — app/blog/[slug]/page.tsx
            export const revalidate = 3600;
            export default async function Post({ params }: { params: Promise<{ slug: string }> }) {
              const { slug } = await params;
              const post = await fetch(`https://cms.example.com/posts/${slug}`, {
                next: { tags: [`post-${slug}`] },
              }).then((r) => r.json());
              return <Article post={post} />;
            }

            // 3) Cache Components (current) — app/blog/[slug]/page.tsx
            import { cacheLife, cacheTag } from 'next/cache';

            async function getPost(slug: string) {
              'use cache';
              cacheLife('days');           // long lifetime…
              cacheTag(`post-${slug}`);    // …but invalidated on publish
              return cms.getPost(slug);
            }

            export async function generateStaticParams() {
              const slugs = await cms.getPopularSlugs(100);
              return slugs.map((slug) => ({ slug }));
            }

            export default async function Post({ params }: { params: Promise<{ slug: string }> }) {
              const { slug } = await params;
              const post = await getPost(slug);
              return <Article post={post} />;
            }

            // app/api/cms-webhook/route.ts → revalidateTag(`post-${slug}`, 'max')
        """,
        lang="tsx",
        follow=[
            ("What does the first visitor see after a page's revalidation time has passed?", "Page-এর revalidation সময় পার হওয়ার পর প্রথম visitor কী দেখে?"),
            ("Why might different users see different versions of a page on a self-hosted cluster?", "Self-hosted cluster-এ বিভিন্ন user কেন একই page-এর আলাদা version দেখতে পারে?"),
        ],
        related=["next-014", "next-015", "next-010"],
        refs=[N_ISR, N_ISR_CC, N_GSP],
    ),
    # ------------------------------------------------------------------ next-027
    Q(
        id="next-027", sub="Parallel and Intercepting Routes", diff="hard", type="conceptual",
        prio="medium", market="international", mins=8,
        tags=["parallel-routes", "intercepting-routes", "modals", "default-js"],
        ver="Next.js 16.4 (App Router; default.js required for parallel slots since v16)", vs=True, status="stable",
        q_en=r"""
            Build an Instagram-style photo modal: clicking a photo in the feed opens it in a modal with its own shareable URL (`/photos/42`), but visiting that URL directly or refreshing shows a full photo page. Explain how parallel routes, intercepting routes and `default.tsx` make this work.
        """,
        q_bn=r"""
            Instagram-ধরনের একটা photo modal বানাও: feed-এ কোনো photo-তে click করলে সেটা নিজস্ব শেয়ারযোগ্য URL (`/photos/42`)-সহ একটা modal-এ খোলে, কিন্তু সরাসরি ওই URL-এ গেলে বা refresh করলে পুরো photo page দেখায়। Parallel route, intercepting route আর `default.tsx` কীভাবে এটা সম্ভব করে, ব্যাখ্যা করো।
        """,
        a_en=r"""
            **Parallel routes** let a layout render more than one page at the same time. A folder named with `@`, like `app/@modal`, is a **slot**: the root layout receives it as a `modal` prop next to `children`. Slots don't change the URL.

            **Intercepting routes** let you show a different route for a URL when you navigate to it **from inside the app** (a soft navigation). `app/@modal/(.)photos/[id]/page.tsx` intercepts `/photos/[id]`: clicking a photo in the feed keeps the feed in `children` and renders the photo inside the `modal` slot. The convention is `(.)` same level, `(..)` one level up, `(..)(..)` two levels up, `(...)` from the app root — based on route segments, so slots don't count.

            On a **hard navigation** (direct visit, refresh, shared link) there's no interception, so `app/photos/[id]/page.tsx` renders the full page.

            **`default.tsx`** tells Next.js what a slot shows when it has no matching active state — for example on a hard load of `/` the `@modal` slot has nothing to show, so `@modal/default.tsx` returns `null`. Since Next.js 16 every parallel slot needs a `default` file, or the build fails.

            To close the modal, a Client Component calls `router.back()`; the user gets a shareable URL, a working back button, and context preserved behind the modal.
        """,
        a_bn=r"""
            **Parallel route** একটা layout-কে একসাথে একাধিক page render করতে দেয়। `@` দিয়ে নাম দেওয়া folder, যেমন `app/@modal`, হলো একটা **slot**: root layout এটাকে `children`-এর পাশে একটা `modal` prop হিসেবে পায়। Slot URL বদলায় না।

            **Intercepting route** দিয়ে কোনো URL-এ **app-এর ভেতর থেকে** navigate করলে (soft navigation) আলাদা একটা route দেখানো যায়। `app/@modal/(.)photos/[id]/page.tsx` `/photos/[id]`-কে intercept করে: feed-এ photo-তে click করলে feed `children`-এ থেকে যায়, আর photo render হয় `modal` slot-এর ভেতরে। নিয়ম হলো `(.)` একই স্তর, `(..)` এক স্তর উপরে, `(..)(..)` দুই স্তর উপরে, `(...)` app root থেকে — route segment অনুযায়ী, তাই slot গোনা হয় না।

            **Hard navigation**-এ (সরাসরি visit, refresh, শেয়ার করা link) কোনো interception হয় না, তাই `app/photos/[id]/page.tsx` পুরো page render করে।

            **`default.tsx`** Next.js-কে বলে কোনো slot-এর মেলানো active state না থাকলে সে কী দেখাবে — যেমন `/` hard load করলে `@modal` slot-এর দেখানোর কিছু নেই, তাই `@modal/default.tsx` `null` return করে। Next.js 16 থেকে প্রতিটা parallel slot-এ একটা `default` file লাগে, নইলে build fail করে।

            Modal বন্ধ করতে একটা Client Component `router.back()` call করে; user পায় শেয়ারযোগ্য URL, কাজ করা back button, আর modal-এর পেছনে আগের context অক্ষত।
        """,
        quick_en=r"""An `@modal` slot (parallel route) renders next to `children`, and `@modal/(.)photos/[id]` intercepts soft navigations to show the photo in the modal. A hard load renders the normal `app/photos/[id]` page, and `@modal/default.tsx` returns `null` when the slot has nothing to show.""",
        quick_bn=r"""একটা `@modal` slot (parallel route) `children`-এর পাশে render হয়, আর `@modal/(.)photos/[id]` soft navigation intercept করে photo-টা modal-এ দেখায়। Hard load-এ সাধারণ `app/photos/[id]` page দেখায়, আর slot-এ দেখানোর কিছু না থাকলে `@modal/default.tsx` `null` return করে।""",
        ex_en=r"""
            - **Why `default.tsx` matters:** on soft navigation Next.js remembers each slot's active state; on a hard load it can't, so it needs a fallback. Before v16 a missing default led to a 404 on hard navigation; now the build fails instead — a common upgrade failure.
            - **Closing on other navigations:** add a catch-all `@modal/[...catchAll]/page.tsx` returning `null`, so navigating to another page via `<Link>` clears the modal.
            - **Other uses of parallel routes:** dashboards with independent sections that load and error separately (each slot can have its own `loading.tsx` and `error.tsx`), and conditional UI by role (`{isAdmin ? admin : user}`).
            - **Accessibility:** the modal component still needs focus management, `Escape` to close and `aria-modal` — the routing pattern doesn't provide that.
        """,
        ex_bn=r"""
            - **`default.tsx` কেন জরুরি:** soft navigation-এ Next.js প্রতিটা slot-এর active state মনে রাখে; hard load-এ পারে না, তাই একটা fallback লাগে। v16-এর আগে default না থাকলে hard navigation-এ 404 দেখাত; এখন এর বদলে build fail করে — upgrade-এর সময় সাধারণ একটা ব্যর্থতা।
            - **অন্য navigation-এ বন্ধ করা:** একটা catch-all `@modal/[...catchAll]/page.tsx` যোগ করো, যেটা `null` return করে, যাতে `<Link>` দিয়ে অন্য page-এ গেলে modal মুছে যায়।
            - **Parallel route-এর অন্য ব্যবহার:** এমন dashboard যার অংশগুলো আলাদাভাবে load আর error হয় (প্রতিটা slot-এর নিজস্ব `loading.tsx` আর `error.tsx` থাকতে পারে), আর role অনুযায়ী conditional UI (`{isAdmin ? admin : user}`)।
            - **Accessibility:** modal component-এর এখনো focus management, `Escape` চাপলে বন্ধ হওয়া আর `aria-modal` লাগে — routing pattern এগুলো দেয় না।
        """,
        tip_en=r"""Explain the two navigation types first (soft vs hard) — the whole pattern depends on them. Then map files to behaviour, and mention the v16 `default.tsx` requirement as a practical gotcha.""",
        tip_bn=r"""আগে দুই ধরনের navigation ব্যাখ্যা করো (soft বনাম hard) — পুরো pattern-টাই এর উপর নির্ভর করে। তারপর কোন file কী আচরণ দেয় মিলিয়ে দেখাও, আর ব্যবহারিক gotcha হিসেবে v16-এর `default.tsx` শর্তের কথা বলো।""",
        mist_en=r"""Counting the `@modal` slot as a route segment when choosing `(.)` vs `(..)`, or forgetting `default.tsx` so the v16 build fails.""",
        mist_bn=r"""`(.)` বনাম `(..)` বেছে নেওয়ার সময় `@modal` slot-কে route segment হিসেবে গোনা, অথবা `default.tsx` ভুলে যাওয়া — ফলে v16 build fail করে।""",
        code=r"""
            app/
            ├── layout.tsx                 // renders {children} and {modal}
            ├── page.tsx                   // the feed
            ├── photos/
            │   └── [id]/
            │       └── page.tsx           // full page: direct visit / refresh
            └── @modal/
                ├── default.tsx            // returns null when no modal is active
                ├── [...catchAll]/
                │   └── page.tsx           // returns null: closes the modal on other navigations
                └── (.)photos/
                    └── [id]/
                        └── page.tsx       // modal version: soft navigation from the feed

            // app/layout.tsx
            export default function RootLayout({
              children,
              modal,
            }: {
              children: React.ReactNode;
              modal: React.ReactNode;
            }) {
              return (
                <html lang="en">
                  <body>
                    {children}
                    {modal}
                  </body>
                </html>
              );
            }

            // app/@modal/(.)photos/[id]/page.tsx
            import { Modal } from '@/components/modal'; // 'use client', calls router.back() on close

            export default async function PhotoModal({ params }: { params: Promise<{ id: string }> }) {
              const { id } = await params;
              const photo = await getPhoto(id);
              return (
                <Modal>
                  <img src={photo.url} alt={photo.caption} />
                </Modal>
              );
            }

            // app/@modal/default.tsx
            export default function Default() {
              return null;
            }
        """,
        lang="tsx",
        follow=[
            ("What exactly happens if `@modal/default.tsx` is missing in Next.js 16?", "Next.js 16-এ `@modal/default.tsx` না থাকলে ঠিক কী হয়?"),
            ("How would you use parallel routes to let dashboard sections fail independently?", "Dashboard-এর অংশগুলো যাতে আলাদাভাবে fail করতে পারে, তার জন্য parallel route কীভাবে ব্যবহার করবে?"),
        ],
        related=["next-003", "next-006"],
        refs=[N_PARALLEL, N_INTERCEPT, N_UPGRADE16],
    ),
    # ------------------------------------------------------------------ next-028
    Q(
        id="next-028", sub="Performance and Bundle Size", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["bundle-size", "performance", "use-client", "code-splitting", "inp"],
        ver="Next.js 16.4 (Turbopack; `next analyze` since 16.1)", vs=True, status="stable",
        q_en=r"""
            Lighthouse reports about 900 KB of client JavaScript on your Next.js home page, and real-user data shows poor INP on mid-range Android phones. How do you find what's in the bundle and reduce it?
        """,
        q_bn=r"""
            Lighthouse জানাচ্ছে তোমার Next.js home page-এ প্রায় ৯০০ KB client JavaScript, আর real-user data দেখাচ্ছে মাঝারি মানের Android phone-এ INP খারাপ। Bundle-এ কী আছে কীভাবে খুঁজবে, আর কীভাবে কমাবে?
        """,
        a_en=r"""
            **Measure first.** Next.js 16 removed the per-route `size` / `First Load JS` columns from `next build` output (they were inaccurate with Server Components), so I run the Turbopack bundle analyzer, `npx next analyze` (available since 16.1), to see every client and server module per route with its import chain; `next analyze --output` saves a snapshot to compare before/after. (With `--webpack` builds, `@next/bundle-analyzer` does the same job.) Lighthouse and real-user data confirm what actually ships and how it affects the page.

            **Typical causes and fixes:**
            1. **`'use client'` too high in the tree.** A `'use client'` on a page or big layout pulls everything it imports into the browser. Push it down to small interactive leaves and keep pages as Server Components.
            2. **Heavy work that could run on the server.** Markdown parsing, syntax highlighting, date formatting libraries, chart-to-SVG rendering — do them in Server Components so the libraries never ship.
            3. **Code needed later.** Lazy-load below-the-fold or on-interaction widgets (rich text editor, map, chart) with `next/dynamic` or `React.lazy`.
            4. **Packages with many exports.** Icon and utility libraries: use `experimental.optimizePackageImports` (many popular ones are optimised automatically) and per-function imports.
            5. **Third-party scripts.** Load analytics/chat widgets with `next/script` and a non-blocking strategy (`afterInteractive`/`lazyOnload`).

            Then verify: compare analyzer snapshots and watch INP and LCP in real-user monitoring. Less JavaScript means less parsing and hydration work on the main thread, which directly helps INP.
        """,
        a_bn=r"""
            **আগে মাপো।** Next.js 16 `next build` output থেকে প্রতিটা route-এর `size` / `First Load JS` column সরিয়ে দিয়েছে (Server Components-এর সাথে এগুলো সঠিক হিসাব দিত না), তাই আমি Turbopack bundle analyzer চালাই, `npx next analyze` (16.1 থেকে আছে), যেটা প্রতিটা route-এর প্রতিটা client আর server module import chain-সহ দেখায়; `next analyze --output` আগে-পরে তুলনার জন্য snapshot save করে। (`--webpack` build-এ `@next/bundle-analyzer` একই কাজ করে।) আসলে কী ship হচ্ছে আর page-এ তার প্রভাব কী, তা Lighthouse আর real-user data দিয়ে নিশ্চিত করি।

            **সাধারণ কারণ আর সমাধান:**
            1. **Tree-র অনেক উপরে `'use client'`।** Page বা বড় layout-এ `'use client'` থাকলে সে যা import করে সব browser-এ চলে যায়। এটা ছোট interactive leaf-এ নামিয়ে আনো, আর page Server Component রাখো।
            2. **Server-এ চালানো যায় এমন ভারী কাজ।** Markdown parsing, syntax highlighting, date formatting library, chart থেকে SVG rendering — এগুলো Server Component-এ করো, তাহলে library-গুলো কখনো browser-এ যায় না।
            3. **পরে দরকার হবে এমন code।** Screen-এর নিচের বা interaction-এ লাগে এমন widget (rich text editor, map, chart) `next/dynamic` বা `React.lazy` দিয়ে lazy-load করো।
            4. **অনেক export-ওয়ালা package।** Icon আর utility library: `experimental.optimizePackageImports` ব্যবহার করো (অনেক জনপ্রিয় library নিজে থেকেই optimise হয়) আর function ধরে import করো।
            5. **Third-party script।** Analytics/chat widget `next/script` আর non-blocking strategy (`afterInteractive`/`lazyOnload`) দিয়ে load করো।

            তারপর যাচাই: analyzer snapshot তুলনা করো আর real-user monitoring-এ INP আর LCP দেখো। কম JavaScript মানে main thread-এ কম parsing আর hydration-এর কাজ, যেটা সরাসরি INP-তে সাহায্য করে।
        """,
        quick_en=r"""Measure first with `next analyze` (the Turbopack bundle analyzer). Then push `'use client'` down to small leaves, do heavy work in Server Components, lazy-load late widgets with `next/dynamic`, optimise package imports and load third-party scripts with `next/script`.""",
        quick_bn=r"""আগে `next analyze` (Turbopack bundle analyzer) দিয়ে মাপো। তারপর `'use client'`-কে ছোট leaf component-এ নামাও, ভারী কাজ Server Component-এ করো, পরে লাগবে এমন widget `next/dynamic` দিয়ে lazy-load করো, package import optimise করো, আর third-party script `next/script` দিয়ে load করো।""",
        ex_en=r"""
            **Why `'use client'` placement is the biggest lever:** the directive marks a module-graph boundary. One directive on `app/page.tsx` can drag a CMS SDK, a markdown parser and every child component into the client bundle, even though the output is static HTML.

            **Security angle:** the same boundary mistake can leak server-only code (API keys in imported config, internal URLs). Import `server-only` in such modules so the build fails instead of shipping them.

            **Don't over-split:** too many tiny lazy chunks add request overhead and loading spinners; lazy-load what is big *and* not needed for first interaction.

            **INP specifically:** besides bundle size, long tasks during interactions (expensive re-renders) hurt INP — React Compiler, memoization, transitions and virtualisation address that part.
        """,
        ex_bn=r"""
            **`'use client'`-এর জায়গাই কেন সবচেয়ে বড় হাতিয়ার:** directive একটা module-graph boundary চিহ্নিত করে। `app/page.tsx`-এ একটা directive একটা CMS SDK, একটা markdown parser আর প্রতিটা child component client bundle-এ টেনে আনতে পারে, যদিও output হলো static HTML।

            **Security দিক:** একই boundary-র ভুলে server-only code leak হতে পারে (import করা config-এ API key, internal URL)। এমন module-এ `server-only` import করো, যাতে ship না করে build fail করে।

            **অতিরিক্ত ভাগ করো না:** অনেক ছোট ছোট lazy chunk request-এর খরচ আর loading spinner বাড়ায়; যা বড় *আর* প্রথম interaction-এ দরকার নেই, সেটাই lazy-load করো।

            **বিশেষ করে INP:** bundle size ছাড়াও interaction-এর সময় long task (expensive re-render) INP খারাপ করে — React Compiler, memoization, transition আর virtualisation সেই অংশটা সামলায়।
        """,
        tip_en=r"""Follow measure → identify → fix → verify. Naming `next analyze` and the `'use client'` boundary as the main lever shows App Router-specific expertise rather than generic web-performance advice.""",
        tip_bn=r"""Measure → identify → fix → verify — এই ক্রম মেনে চলো। `next analyze` আর প্রধান হাতিয়ার হিসেবে `'use client'` boundary-র নাম বললে সাধারণ web-performance পরামর্শের বদলে App Router-নির্দিষ্ট দক্ষতা বোঝা যায়।""",
        mist_en=r"""Starting with micro-optimisations (minifier settings) before measuring, lazy-loading above-the-fold content, or making the whole page a Client Component "because it has one button".""",
        mist_bn=r"""মাপার আগেই micro-optimisation (minifier setting) দিয়ে শুরু করা, screen-এর উপরের দিকের content lazy-load করা, অথবা "একটা button আছে বলে" পুরো page Client Component বানিয়ে ফেলা।""",
        code=r"""
            // BEFORE — app/blog/[slug]/page.tsx: the whole page ships to the browser
            'use client';
            import { marked } from 'marked';
            import { format } from 'date-fns';
            // ...page renders markdown + a like button

            // AFTER — page stays a Server Component; only the button is a client island
            // app/blog/[slug]/page.tsx
            import { marked } from 'marked';            // runs on the server only
            import { LikeButton } from './like-button'; // 'use client' leaf
            import { CommentsSection } from './comments-section';

            export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
              const { slug } = await params;
              const post = await getPost(slug);
              const html = await marked.parse(post.markdown);
              return (
                <article>
                  <h1>{post.title}</h1>
                  <div dangerouslySetInnerHTML={{ __html: html }} /> {/* sanitise CMS HTML */}
                  <LikeButton postId={post.id} />
                  <CommentsSection postId={post.id} />
                </article>
              );
            }

            // app/blog/[slug]/comments-section.tsx
            'use client';
            import dynamic from 'next/dynamic';

            // Heavy editor loads only in the browser, after the page is interactive
            const CommentEditor = dynamic(() => import('./comment-editor'), {
              ssr: false,
              loading: () => <p>Loading editor…</p>,
            });

            export function CommentsSection({ postId }: { postId: string }) {
              return <CommentEditor postId={postId} />;
            }
        """,
        lang="tsx",
        follow=[
            ("Why can't you use `next/dynamic` with `ssr: false` directly in a Server Component?", "Server Component-এ সরাসরি `ssr: false`-সহ `next/dynamic` কেন ব্যবহার করা যায় না?"),
            ("How would you stop a server-only module from ever being imported into client code?", "Server-only কোনো module যাতে কখনো client code-এ import না হয়, সেটা কীভাবে নিশ্চিত করবে?"),
        ],
        related=["next-004", "next-019"],
        refs=[N_BUNDLING, N_LAZY, N_OPI],
    ),
    # ------------------------------------------------------------------ next-029
    Q(
        id="next-029", sub="Error Handling", diff="hard", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["error-boundary", "error-js", "layouts", "global-error"],
        ver="Next.js 16.4 (App Router)", vs=False, status="stable",
        q_en=r"""
            `app/dashboard/layout.tsx` throws while loading the current user. Both `app/error.tsx` and `app/dashboard/error.tsx` exist. Which error UI does the user see?
        """,
        q_bn=r"""
            `app/dashboard/layout.tsx` current user load করার সময় throw করল। `app/error.tsx` আর `app/dashboard/error.tsx` — দুটোই আছে। User কোন error UI দেখবে?
        """,
        code=r"""
            app/
            ├── layout.tsx
            ├── error.tsx
            └── dashboard/
                ├── layout.tsx     ← throws
                ├── error.tsx
                └── page.tsx
        """,
        lang="text",
        options=[
            ("`app/dashboard/error.tsx`, because it's in the same folder as the failing layout", "`app/dashboard/error.tsx`, কারণ এটা ব্যর্থ layout-এর একই folder-এ আছে"),
            ("`app/error.tsx`, because a segment's `error.tsx` wraps its page and children but not that segment's own `layout.tsx`", "`app/error.tsx`, কারণ একটা segment-এর `error.tsx` তার page আর children-কে wrap করে, কিন্তু ওই segment-এর নিজের `layout.tsx`-কে না"),
            ("`app/global-error.tsx`, which always handles errors thrown in any layout", "`app/global-error.tsx`, যেটা যেকোনো layout-এ throw হওয়া error সবসময় সামলায়"),
            ("No error UI — the error is swallowed and the page renders without the layout", "কোনো error UI না — error চাপা পড়ে যায় আর page layout ছাড়াই render হয়"),
        ],
        correct=1,
        a_en=r"""`app/error.tsx`. Inside a segment the nesting is `layout` → `template` → `error` → `loading` → `not-found` → `page`, so the error boundary from `dashboard/error.tsx` sits **inside** `dashboard/layout.tsx` and can't catch what the layout throws. The error bubbles to the nearest boundary above — the parent segment's `error.tsx`, rendered inside the root layout.""",
        a_bn=r"""`app/error.tsx`। একটা segment-এর ভেতরে nesting হলো `layout` → `template` → `error` → `loading` → `not-found` → `page`, তাই `dashboard/error.tsx`-এর error boundary `dashboard/layout.tsx`-এর **ভেতরে** বসে, আর layout যা throw করে তা ধরতে পারে না। Error উপরের সবচেয়ে কাছের boundary-তে যায় — parent segment-এর `error.tsx`, যেটা root layout-এর ভেতরে render হয়।""",
        quick_en=r"""`app/error.tsx`. A segment's `error.tsx` sits inside that segment's own `layout.tsx`, so it can't catch errors the layout throws; the error bubbles to the parent segment's boundary.""",
        quick_bn=r"""`app/error.tsx`। কোনো segment-এর `error.tsx` সেই segment-এর নিজের `layout.tsx`-এর ভেতরে থাকে, তাই layout-এর throw করা error ধরতে পারে না; error উপরের segment-এর boundary-তে চলে যায়।""",
        ex_en=r"""
            The tempting answer is the same-folder `dashboard/error.tsx`. It *does* catch errors from `dashboard/page.tsx` and nested segments — just not from its sibling layout, because a boundary can't catch errors in the component that renders it.

            `global-error.tsx` is only for errors in the **root** layout/template; it replaces the root layout and must render its own `<html>` and `<body>`.

            Practical consequences: keep risky data fetching out of layouts where possible (or handle failures inside the layout), and if a layout *must* fetch, make sure the parent segment has a sensible `error.tsx`. In production, errors from Server Components arrive with a generic message plus `error.digest` for log correlation; the `retry()` prop (stable since 16.3) re-fetches and re-renders the segment. For component-level boundaries that aren't tied to route segments, Next.js also documents a `catchError` helper.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো একই folder-এর `dashboard/error.tsx`। এটা `dashboard/page.tsx` আর nested segment-এর error *ধরে* — শুধু তার পাশের layout-এর error ধরে না, কারণ যে component একটা boundary render করে, সেই boundary তার error ধরতে পারে না।

            `global-error.tsx` শুধু **root** layout/template-এর error-এর জন্য; এটা root layout-কে replace করে আর নিজের `<html>` ও `<body>` render করতে হয়।

            বাস্তব ফলাফল: সম্ভব হলে ঝুঁকিপূর্ণ data fetching layout-এর বাইরে রাখো (অথবা layout-এর ভেতরেই failure সামলাও), আর layout-কে fetch করতেই হলে নিশ্চিত করো parent segment-এ একটা যুক্তিসঙ্গত `error.tsx` আছে। Production-এ Server Component-এর error আসে একটা generic message আর log মেলানোর জন্য `error.digest`-সহ; `retry()` prop (16.3 থেকে stable) segment আবার fetch করে re-render করে। Route segment-এর সাথে যুক্ত না এমন component-level boundary-র জন্য Next.js একটা `catchError` helper-ও document করে।
        """,
        tip_en=r"""Quote the nesting order — it answers this question and several follow-ups (why `loading.tsx` doesn't cover layouts, why `not-found` sits inside the error boundary).""",
        tip_bn=r"""Nesting-এর ক্রমটা বলো — এটা দিয়েই এই প্রশ্ন আর পরের কয়েকটা প্রশ্নের উত্তর হয়ে যায় (কেন `loading.tsx` layout কভার করে না, কেন `not-found` error boundary-র ভেতরে থাকে)।""",
        related=["next-006", "next-003"],
        refs=[N_ERROR, N_ERROR_HANDLING],
    ),
    # ------------------------------------------------------------------ next-032
    Q(
        id="next-032", sub="Caching Architecture for Personalised E-commerce", diff="extreme", type="architecture",
        prio="medium", market="international", mins=25,
        tags=["caching", "e-commerce", "personalisation", "cache-components", "architecture"],
        ver="Next.js 16.4 (Cache Components)", vs=True, status="stable",
        q_en=r"""
            Design the rendering and caching strategy for a large marketplace on Next.js 16 with Cache Components: 2 million products, flash sales, regional prices (BDT for Bangladesh, USD elsewhere) and logged-in personalisation (cart count, "recommended for you"). Product pages must load fast on 4G, and prices and stock must never be wrong at checkout.
        """,
        q_bn=r"""
            Cache Components-সহ Next.js 16-এ একটা বড় marketplace-এর rendering আর caching strategy design করো: ২০ লাখ product, flash sale, অঞ্চলভিত্তিক দাম (বাংলাদেশে BDT, অন্য জায়গায় USD) আর logged-in personalisation (cart count, "recommended for you")। 4G-তে product page দ্রুত load হতে হবে, আর checkout-এ দাম ও stock কখনো ভুল হওয়া চলবে না।
        """,
        a_en=r"""
            *(Advanced, senior-level architecture question.)* I'd classify every piece of data by **who it's for** and **how fresh it must be**, then map each class to a caching tool.

            1. **Public, slow-changing** (title, images, specs): `'use cache'` + `cacheLife('days')` + `cacheTag('product-<id>')`. Prerender the top sellers with `generateStaticParams`; the long tail is rendered on first visit and cached.
            2. **Public, fast-changing** (price, stock badge, flash-sale state): a separate cached function with a short profile (`'minutes'`) and its own tag (`price-<id>`). The pricing system's webhook calls `revalidateTag('price-<id>', { expire: 0 })` so prices never stay stale; admin edits via Server Actions use `updateTag`.
            3. **Per region/currency:** put the region in the URL (`/bd/...`, `/us/...`) and pass it as an argument to cached functions. That keeps a small, bounded number of variants, stays prerenderable and is SEO-friendly — better than reading a currency cookie.
            4. **Per user** (cart count, recommendations, wishlist): read cookies inside `<Suspense>` boundaries so they stream after the static shell. Never put this in a shared cache; `'use cache: private'` can make per-user results prefetchable in the browser.
            5. **Checkout:** always dynamic. The order Server Action re-reads price and stock inside a database transaction — the cache is never the source of truth for money.

            **Infrastructure:** CDN for static shells and hashed assets, a shared cache handler (Redis) with tag coordination across instances, an image CDN, and streaming-capable proxies.
        """,
        a_bn=r"""
            *(Advanced, senior-level architecture প্রশ্ন।)* আমি প্রতিটা data-কে ভাগ করব **কার জন্য** আর **কতটা fresh হতে হবে** অনুযায়ী, তারপর প্রতিটা ভাগকে একটা caching tool-এর সাথে মেলাব।

            1. **Public, ধীরে বদলায়** (title, image, spec): `'use cache'` + `cacheLife('days')` + `cacheTag('product-<id>')`। Top seller-গুলো `generateStaticParams` দিয়ে prerender করো; বাকি long tail প্রথম visit-এ render হয়ে cache হয়।
            2. **Public, দ্রুত বদলায়** (দাম, stock badge, flash-sale অবস্থা): ছোট profile (`'minutes'`) আর নিজস্ব tag (`price-<id>`)-সহ আলাদা একটা cached function। Pricing system-এর webhook `revalidateTag('price-<id>', { expire: 0 })` call করে, যাতে দাম কখনো stale না থাকে; Server Action দিয়ে admin-এর edit-এ `updateTag`।
            3. **অঞ্চল/currency অনুযায়ী:** অঞ্চলটা URL-এ রাখো (`/bd/...`, `/us/...`) আর cached function-এ argument হিসেবে পাঠাও। এতে variant-এর সংখ্যা ছোট আর সীমিত থাকে, prerender করা যায় আর SEO-বান্ধব — currency cookie পড়ার চেয়ে ভালো।
            4. **প্রতি user-এ আলাদা** (cart count, recommendation, wishlist): `<Suspense>` boundary-র ভেতরে cookie পড়ো, যাতে static shell-এর পরে stream হয়। এগুলো কখনো shared cache-এ রাখবে না; `'use cache: private'` per-user result browser-এ prefetch করার উপযোগী করতে পারে।
            5. **Checkout:** সবসময় dynamic। Order Server Action একটা database transaction-এর ভেতরে দাম আর stock আবার পড়ে — টাকার ব্যাপারে cache কখনো source of truth না।

            **Infrastructure:** static shell আর hash-যুক্ত asset-এর জন্য CDN, instance-গুলোর মধ্যে tag coordination-সহ shared cache handler (Redis), image CDN, আর streaming সমর্থন করে এমন proxy।
        """,
        quick_en=r"""Classify data by audience and freshness: product details cached for days with tags, prices and stock in a short-lived separately tagged cache, region in the URL, and per-user data streamed inside `<Suspense>`. Checkout is always dynamic and re-reads price and stock from the database.""",
        quick_bn=r"""Data-কে কার জন্য আর কতটা fresh দরকার সেই অনুযায়ী ভাগ করো: product details tag-সহ কয়েক দিনের জন্য cache, price আর stock আলাদা tag-সহ অল্প সময়ের cache-এ, region URL-এ, আর user-ভিত্তিক data `<Suspense>`-এর ভেতরে stream। Checkout সবসময় dynamic, আর database থেকে price ও stock আবার পড়ে।""",
        ex_en=r"""
            **Tag taxonomy:** `product-<id>`, `price-<id>`, `category-<slug>`, `sale-<id>`. Fine-grained tags avoid invalidating millions of entries at once; a single `products` tag for everything would cause a regeneration stampede.

            **Flash sales:** the sale page and its shell are prerendered *before* the start time; the sale state (started/ended, remaining stock) is a small, short-lived or dynamic hole. Expect traffic spikes — stale-while-revalidate (`'max'`) on non-price data spreads regeneration load.

            **Failure scenarios**
            - Cache handler down → fall back to rendering from the database with rate limits; prices are still correct because checkout re-validates.
            - Price shown on the page changed before payment → checkout shows "price updated" and asks for confirmation.
            - Crawlers that can't handle streamed metadata are served a fully rendered response — capacity-plan for bot traffic hitting dynamic rendering.

            **Measure:** cache hit ratio per tag family, LCP/INP by region, invalidation latency, and checkout price-mismatch rate.
        """,
        ex_bn=r"""
            **Tag-এর বিন্যাস:** `product-<id>`, `price-<id>`, `category-<slug>`, `sale-<id>`। সূক্ষ্ম tag থাকলে একসাথে লাখ লাখ entry invalidate হয় না; সবকিছুর জন্য একটাই `products` tag থাকলে regeneration-এর হুড়োহুড়ি (stampede) লেগে যেত।

            **Flash sale:** sale page আর তার shell শুরু হওয়ার *আগেই* prerender করা থাকে; sale-এর অবস্থা (শুরু/শেষ, বাকি stock) একটা ছোট, স্বল্পস্থায়ী বা dynamic অংশ। Traffic হঠাৎ বাড়বে ধরে নাও — দাম ছাড়া অন্য data-য় stale-while-revalidate (`'max'`) regeneration-এর চাপ ছড়িয়ে দেয়।

            **Failure scenario**
            - Cache handler বন্ধ → rate limit-সহ database থেকে render করার fallback; checkout আবার যাচাই করে বলে দাম তখনো সঠিক থাকে।
            - Payment-এর আগে page-এ দেখানো দাম বদলে গেছে → checkout "দাম update হয়েছে" দেখিয়ে নিশ্চিত করতে বলে।
            - যে crawler stream হওয়া metadata সামলাতে পারে না, তাকে পুরোপুরি render করা response দেওয়া হয় — dynamic rendering-এ আসা bot traffic-এর জন্য capacity পরিকল্পনা করো।

            **যা মাপবে:** প্রতিটা tag family-র cache hit ratio, অঞ্চল অনুযায়ী LCP/INP, invalidation latency, আর checkout-এ দাম না মেলার হার।
        """,
        tip_en=r"""Lead with the classification ("who is it for, how fresh must it be?") — it turns a vague question into a clear design. Then map each class to concrete APIs and finish with correctness at checkout and failure scenarios. That's what separates architects from framework users.""",
        tip_bn=r"""শ্রেণিবিভাগ দিয়ে শুরু করো ("কার জন্য, কতটা fresh হতে হবে?") — এতে অস্পষ্ট প্রশ্ন একটা স্পষ্ট design-এ পরিণত হয়। তারপর প্রতিটা ভাগকে নির্দিষ্ট API-র সাথে মেলাও, আর শেষে checkout-এর correctness আর failure scenario বলো। এটাই architect-কে সাধারণ framework user থেকে আলাদা করে।""",
        mist_en=r"""Making the whole product page dynamic because it shows a cart badge, caching per-user data in a shared cache, keying caches by a currency cookie (unbounded variants, not prerenderable), or trusting cached prices at checkout.""",
        mist_bn=r"""একটা cart badge দেখায় বলে পুরো product page dynamic করে ফেলা, per-user data shared cache-এ রাখা, currency cookie দিয়ে cache key বানানো (সীমাহীন variant, prerender করা যায় না), অথবা checkout-এ cached দামের উপর ভরসা করা।""",
        code=r"""
            // app/[region]/products/[id]/page.tsx
            import { Suspense } from 'react';
            import { notFound } from 'next/navigation';
            import { cacheLife, cacheTag } from 'next/cache';

            async function getProduct(id: string, region: string) {
              'use cache';
              cacheLife('days');
              cacheTag(`product-${id}`);
              return catalog.getProduct(id, region);
            }

            async function getPrice(id: string, region: string) {
              'use cache';
              cacheLife('minutes');
              cacheTag(`price-${id}`);
              return pricing.getPrice(id, region); // BDT for 'bd', USD otherwise
            }

            export async function generateStaticParams() {
              const ids = await catalog.getTopSellerIds(1000);
              return ['bd', 'us'].flatMap((region) => ids.map((id) => ({ region, id })));
            }

            export default async function ProductPage({
              params,
            }: {
              params: Promise<{ region: string; id: string }>;
            }) {
              const { region, id } = await params;
              const [product, price] = await Promise.all([getProduct(id, region), getPrice(id, region)]);
              if (!product) notFound();

              return (
                <main>
                  <ProductGallery images={product.images} />
                  <h1>{product.title}</h1>
                  <PriceTag price={price} />
                  <Suspense fallback={<CartBadgeSkeleton />}>
                    <CartBadge />                       {/* reads cookies(): per user, streamed */}
                  </Suspense>
                  <Suspense fallback={<RecommendationsSkeleton />}>
                    <PersonalRecommendations productId={id} />
                  </Suspense>
                </main>
              );
            }
        """,
        lang="tsx",
        follow=[
            ("How would you prevent a cache stampede at the exact second a flash sale starts?", "Flash sale ঠিক যে সেকেন্ডে শুরু হয়, তখন cache stampede কীভাবে ঠেকাবে?"),
            ("Why is the region in the URL better than a currency cookie for caching and SEO?", "Caching আর SEO-র জন্য currency cookie-র চেয়ে URL-এ region রাখা কেন ভালো?"),
            ("Where exactly do you guarantee price correctness, and why there?", "দামের correctness ঠিক কোথায় নিশ্চিত করো, আর কেন সেখানে?"),
        ],
        related=["next-014", "next-024", "next-030"],
        refs=[N_CACHING, N_USE_CACHE_PRIVATE, N_ISR_CC],
    ),
]

if __name__ == "__main__":
    save("nextjs", "b4", QUESTIONS)
