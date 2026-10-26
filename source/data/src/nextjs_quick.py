# Next.js — quick-recall questions (next-q01..q10)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

QUESTIONS = [
    # ------------------------------------------------------------------ next-q01
    Q(
        id="next-q01", sub="Navigation and Prefetching", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["link", "navigation", "prefetching"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""Why use `<Link>` from `next/link` instead of a plain `<a>` tag, and what is prefetching?""",
        q_bn=r"""সাধারণ `<a>` tag-এর বদলে `next/link`-এর `<Link>` কেন ব্যবহার করবে, আর prefetching কী?""",
        a_en=r"""`<Link>` renders an `<a>` but navigates on the client, so shared layouts stay mounted and only the new segment loads, instead of a full page reload. In production it also prefetches the linked route in the background when the link enters the viewport, so the click feels instant; `prefetch={false}` turns that off.""",
        a_bn=r"""`<Link>` একটা `<a>` render করে, কিন্তু navigation হয় client-এ, তাই পুরো page reload না হয়ে shared layout mounted থাকে আর শুধু নতুন segment load হয়। Production-এ link viewport-এ এলে এটা পেছনে route-টা prefetch-ও করে রাখে, তাই click করলে প্রায় সাথে সাথে খোলে; `prefetch={false}` দিয়ে এটা বন্ধ করা যায়।""",
        code=r"""
            import Link from 'next/link';

            <Link href={`/blog/${post.slug}`}>{post.title}</Link>
            <Link href="/admin" prefetch={false}>Admin</Link>
        """, lang="tsx",
        ex_en=r"""By default a static route is prefetched in full, while a dynamic route is prefetched only down to the nearest `loading.js` boundary. Prefetching doesn't run in `next dev`.""",
        ex_bn=r"""Default-এ static route পুরোটা prefetch হয়, আর dynamic route শুধু সবচেয়ে কাছের `loading.js` boundary পর্যন্ত। `next dev`-এ prefetching চলে না।""",
        tip_en=r"""Say "client-side navigation plus viewport prefetching", and note it's production-only.""",
        tip_bn=r"""বলো "client-side navigation আর viewport-এ এলে prefetching", আর উল্লেখ করো এটা শুধু production-এ।""",
        follow=[("How do you navigate programmatically after a form succeeds?", "Form সফল হওয়ার পর code থেকে কীভাবে navigate করবে?")],
        related=["next-003", "next-001"],
        refs=[("Next.js Docs — Link Component", "https://nextjs.org/docs/app/api-reference/components/link")],
    ),
    # ------------------------------------------------------------------ next-q02
    Q(
        id="next-q02", sub="Navigation and Prefetching", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["userouter", "next-navigation", "usepathname"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""How do you navigate in code in the App Router, and which `useRouter` do you import?""",
        q_bn=r"""App Router-এ code থেকে কীভাবে navigate করো, আর কোন `useRouter` import করো?""",
        a_en=r"""In a Client Component, import `useRouter` from `next/navigation` and call `router.push('/path')`, `router.replace()` or `router.back()`; read the URL with `usePathname()` and `useSearchParams()`. `useRouter` from `next/router` is the legacy Pages Router API, and on the server you use `redirect()` instead.""",
        a_bn=r"""Client Component-এ `next/navigation` থেকে `useRouter` import করে `router.push('/path')`, `router.replace()` বা `router.back()` call করো; URL পড়তে `usePathname()` আর `useSearchParams()`। `next/router`-এর `useRouter` হলো legacy Pages Router API, আর server-এ এর বদলে `redirect()` ব্যবহার করো।""",
        code=r"""
            'use client';
            import { useRouter } from 'next/navigation';

            export function SaveButton() {
              const router = useRouter();
              return <button onClick={() => router.push('/dashboard')}>Save</button>;
            }
        """, lang="tsx",
        ex_en=r"""Importing from `next/router` inside `app/` is a classic migration bug. Prefer `<Link>` for normal links; use the router only for navigation that follows an action.""",
        ex_bn=r"""`app/`-এর ভেতরে `next/router` থেকে import করা migration-এর একটা পরিচিত bug। সাধারণ link-এর জন্য `<Link>` নাও; router শুধু কোনো কাজের পরে navigate করতে।""",
        tip_en=r"""Name the import path explicitly: `next/navigation` for the App Router.""",
        tip_bn=r"""Import path-টা স্পষ্ট করে বলো: App Router-এর জন্য `next/navigation`।""",
        follow=[("How do you redirect from a Server Component or Server Action?", "Server Component বা Server Action থেকে কীভাবে redirect করবে?")],
        related=["next-012", "next-031"],
        refs=[("Next.js Docs — useRouter", "https://nextjs.org/docs/app/api-reference/functions/use-router")],
    ),
    # ------------------------------------------------------------------ next-q03
    Q(
        id="next-q03", sub="Rendering Strategies", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["static", "dynamic", "rendering", "cache-components"],
        ver="Next.js 16.4 (App Router, Cache Components)", vs=True, status="stable",
        q_en=r"""In the App Router, what makes a part of a page static or dynamic?""",
        q_bn=r"""App Router-এ page-এর কোনো অংশ static নাকি dynamic হবে, সেটা কী ঠিক করে?""",
        a_en=r"""Anything that needs the request makes it dynamic: `cookies()`, `headers()`, `searchParams` or uncached data. With Cache Components, code that doesn't need the request, or is cached with `'use cache'`, is prerendered into a static shell, and request-time parts must sit inside `<Suspense>` to stream per request.""",
        a_bn=r"""Request লাগে এমন যেকোনো কিছু অংশটাকে dynamic করে: `cookies()`, `headers()`, `searchParams` বা uncached data। Cache Components-এ যে code-এর request লাগে না, বা `'use cache'` দিয়ে cache করা, সেটা static shell-এ prerender হয়; আর request-time অংশকে `<Suspense>`-এর ভেতরে রাখতে হয় যাতে প্রতি request-এ stream হয়।""",
        ex_en=r"""So "static vs dynamic" is decided per component, not per page. In the previous model (Cache Components off) you could force it per route with `export const dynamic = 'force-dynamic'`.""",
        ex_bn=r"""তাই "static না dynamic" ঠিক হয় component ধরে, page ধরে না। আগের model-এ (Cache Components বন্ধ) route-এ `export const dynamic = 'force-dynamic'` দিয়ে জোর করে ঠিক করা যেত।""",
        tip_en=r"""List the request-time APIs, then say "cached or inside Suspense".""",
        tip_bn=r"""Request-time API-গুলোর নাম বলো, তারপর বলো "হয় cached, নয়তো Suspense-এর ভেতরে"।""",
        follow=[("What error do you get if you read cookies outside Suspense?", "Suspense-এর বাইরে cookie পড়লে কী error হয়?")],
        related=["next-010", "next-026", "next-014"],
        refs=[("Next.js Docs — Caching (Cache Components)", "https://nextjs.org/docs/app/getting-started/caching")],
    ),
    # ------------------------------------------------------------------ next-q04
    Q(
        id="next-q04", sub="Dynamic Routes", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["generatestaticparams", "dynamic-routes", "ssg"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""What does `generateStaticParams` do?""",
        q_bn=r"""`generateStaticParams` কী করে?""",
        a_en=r"""Exported from a dynamic route like `app/blog/[slug]/page.tsx`, it returns the list of params to prerender at build time, such as `[{ slug: 'hello' }]`. Those pages are built as static HTML; other slugs can still be rendered on first request. It replaces the legacy Pages Router `getStaticPaths`.""",
        a_bn=r"""`app/blog/[slug]/page.tsx`-এর মতো dynamic route থেকে export করলে এটা build-এর সময় prerender করার param-এর list return করে, যেমন `[{ slug: 'hello' }]`। ওই page-গুলো static HTML হিসেবে তৈরি হয়; বাকি slug প্রথম request-এ render হতে পারে। এটা legacy Pages Router-এর `getStaticPaths`-এর জায়গা নিয়েছে।""",
        code=r"""
            // app/blog/[slug]/page.tsx
            export async function generateStaticParams() {
              const posts = await getPosts();
              return posts.map((p) => ({ slug: p.slug }));
            }
        """, lang="tsx",
        ex_en=r"""The page still reads the value with `const { slug } = await params`. Prebuild only popular items; prerendering millions of pages makes builds slow.""",
        ex_bn=r"""Page তখনও `const { slug } = await params` দিয়ে value পড়ে। শুধু জনপ্রিয় item আগে build করো; লাখ লাখ page prerender করলে build ধীর হয়ে যায়।""",
        tip_en=r"""Connect it to SSG: "it's how a dynamic route gets static pages".""",
        tip_bn=r"""SSG-র সাথে মিলিয়ে বলো: "এভাবেই একটা dynamic route static page পায়"।""",
        follow=[("What happens to a slug that wasn't returned at build time?", "Build-এর সময় return হয়নি এমন slug-এর কী হয়?")],
        related=["next-022", "next-005"],
        refs=[("Next.js Docs — generateStaticParams", "https://nextjs.org/docs/app/api-reference/functions/generate-static-params")],
    ),
    # ------------------------------------------------------------------ next-q05
    Q(
        id="next-q05", sub="File-based Routing", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["catch-all", "dynamic-routes", "routing"],
        ver="Next.js 16.4 (App Router)", vs=False, status="stable",
        q_en=r"""What is the difference between `[slug]`, `[...slug]` and `[[...slug]]` folders?""",
        q_bn=r"""`[slug]`, `[...slug]` আর `[[...slug]]` folder-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`[slug]` matches exactly one segment (`/docs/a`). `[...slug]` is a catch-all that matches one or more segments (`/docs/a/b`), giving `slug` as an array. `[[...slug]]` is an optional catch-all that also matches the bare `/docs`, where `slug` is `undefined`.""",
        a_bn=r"""`[slug]` ঠিক একটা segment মেলায় (`/docs/a`)। `[...slug]` হলো catch-all, এক বা একাধিক segment মেলায় (`/docs/a/b`), আর `slug` আসে array হিসেবে। `[[...slug]]` হলো optional catch-all, যেটা শুধু `/docs`-ও মেলায়, তখন `slug` হয় `undefined`।""",
        code=r"""
            app/docs/[slug]/page.tsx       /docs/a    → { slug: 'a' }
            app/docs/[...slug]/page.tsx    /docs/a/b  → { slug: ['a', 'b'] }
            app/docs/[[...slug]]/page.tsx  /docs      → { slug: undefined }
        """, lang="text",
        ex_en=r"""All of them arrive through the async `params` prop in Next.js 16. Catch-alls are handy for docs and CMS pages with nested paths.""",
        ex_bn=r"""Next.js 16-এ সবগুলোই async `params` prop দিয়ে আসে। Nested path-ওয়ালা docs আর CMS page-এর জন্য catch-all কাজে লাগে।""",
        tip_en=r"""Give one URL example per pattern; that's faster than defining them.""",
        tip_bn=r"""প্রতিটা pattern-এর জন্য একটা করে URL example দাও; সংজ্ঞা দেওয়ার চেয়ে এটা দ্রুত।""",
        follow=[("What are route groups like `(marketing)` for?", "`(marketing)`-এর মতো route group কীসের জন্য?")],
        related=["next-002", "next-005"],
        refs=[("Next.js Docs — Dynamic Route Segments", "https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes")],
    ),
    # ------------------------------------------------------------------ next-q06
    Q(
        id="next-q06", sub="Font Optimization", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["next-font", "fonts", "cls", "performance"],
        ver="Next.js 16.4 (App Router)", vs=False, status="stable",
        q_en=r"""What does `next/font` do?""",
        q_bn=r"""`next/font` কী করে?""",
        a_en=r"""`next/font` downloads Google or local fonts at build time and self-hosts them with your static assets, so the browser never requests Google. It preloads the font and uses an adjusted fallback font to avoid layout shift (CLS); you apply it with `className` or a CSS variable.""",
        a_bn=r"""`next/font` build-এর সময় Google বা local font download করে তোমার static asset-এর সাথে self-host করে, তাই browser কখনো Google-এ request পাঠায় না। এটা font preload করে আর layout shift (CLS) এড়াতে মাপমতো fallback font ব্যবহার করে; `className` বা CSS variable দিয়ে প্রয়োগ করো।""",
        code=r"""
            // app/layout.tsx
            import { Inter } from 'next/font/google';
            const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

            // <html lang="en" className={inter.variable}>
        """, lang="tsx",
        ex_en=r"""Load each font once (in the root layout or a shared `fonts.ts`) and reuse it; every call creates another hosted font instance.""",
        ex_bn=r"""প্রতিটা font একবারই load করো (root layout বা একটা shared `fonts.ts`-এ), তারপর বারবার ব্যবহার করো; প্রতিবার call করলে আরেকটা font instance host হয়।""",
        tip_en=r"""Mention the two wins: privacy (no Google request) and no layout shift.""",
        tip_bn=r"""দুটো লাভের কথা বলো: privacy (Google-এ request যায় না) আর layout shift নেই।""",
        follow=[("How would you use a font file you own?", "নিজের একটা font file কীভাবে ব্যবহার করবে?")],
        related=["next-001", "next-028"],
        refs=[("Next.js Docs — Font Module", "https://nextjs.org/docs/app/api-reference/components/font")],
    ),
    # ------------------------------------------------------------------ next-q07
    Q(
        id="next-q07", sub="Revalidation APIs", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["revalidatepath", "revalidation", "cache"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""What does `revalidatePath` do, and how is it different from `revalidateTag`?""",
        q_bn=r"""`revalidatePath` কী করে, আর এটা `revalidateTag` থেকে কীভাবে আলাদা?""",
        a_en=r"""`revalidatePath('/blog')` invalidates the cached data for one route path, so that path gets fresh data; you call it from a Server Action or Route Handler, not from Client Components or `proxy.ts`. `revalidateTag` targets data by tag, so every page that uses that tag is refreshed.""",
        a_bn=r"""`revalidatePath('/blog')` একটা route path-এর cached data invalidate করে, ফলে ওই path fresh data পায়; এটা Server Action বা Route Handler থেকে call করো, Client Component বা `proxy.ts` থেকে না। `revalidateTag` tag ধরে data-কে লক্ষ্য করে, তাই ওই tag ব্যবহার করা সব page refresh হয়।""",
        code=r"""
            'use server';
            import { revalidatePath } from 'next/cache';

            export async function publishPost(id: string) {
              await db.post.publish(id);
              revalidatePath('/blog');
            }
        """, lang="ts",
        ex_en=r"""For a dynamic pattern pass the type: `revalidatePath('/blog/[slug]', 'page')`. From a Route Handler the path is only marked and re-rendered on its next visit.""",
        ex_bn=r"""Dynamic pattern-এর জন্য type দাও: `revalidatePath('/blog/[slug]', 'page')`। Route Handler থেকে call করলে path শুধু mark হয়, আর পরের visit-এ নতুন করে render হয়।""",
        tip_en=r"""Say "path = one page, tag = the data everywhere" and pick tags when the same data appears on many pages.""",
        tip_bn=r"""বলো "path = একটা page, tag = সব জায়গার সেই data", আর একই data অনেক page-এ থাকলে tag বেছে নাও।""",
        follow=[("When would you use `updateTag` instead?", "কখন এর বদলে `updateTag` ব্যবহার করবে?")],
        related=["next-015", "next-022"],
        refs=[("Next.js Docs — revalidatePath", "https://nextjs.org/docs/app/api-reference/functions/revalidatePath")],
    ),
    # ------------------------------------------------------------------ next-q08
    Q(
        id="next-q08", sub="Server Functions", diff="medium", type="quick",
        prio="medium", market="both", mins=1,
        tags=["after", "logging", "next-server"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""What is `after()` in Next.js used for?""",
        q_bn=r"""Next.js-এ `after()` কীসের জন্য ব্যবহার হয়?""",
        a_en=r"""`after(callback)` from `next/server` schedules work to run after the response is finished, such as logging or analytics, so the user doesn't wait for it. It works in Server Components, Server Actions, Route Handlers and `proxy.ts`, and it is stable since Next.js 15.1.""",
        a_bn=r"""`next/server`-এর `after(callback)` এমন কাজ schedule করে যেটা response শেষ হওয়ার পরে চলবে, যেমন logging বা analytics, তাই user-কে এর জন্য অপেক্ষা করতে হয় না। এটা Server Component, Server Action, Route Handler আর `proxy.ts`-এ কাজ করে, আর Next.js 15.1 থেকে stable।""",
        code=r"""
            import { after } from 'next/server';

            export async function POST(request: Request) {
              const order = await createOrder(await request.json());
              after(() => logEvent('order_created', order.id));
              return Response.json(order, { status: 201 });
            }
        """, lang="ts",
        ex_en=r"""In Server Components you can't call `cookies()` or `headers()` inside the callback: read them during render and pass the values in.""",
        ex_bn=r"""Server Component-এ callback-এর ভেতরে `cookies()` বা `headers()` call করা যায় না: render-এর সময় পড়ে value-গুলো ভেতরে পাঠাও।""",
        tip_en=r"""Give a concrete use (analytics after a checkout) and say it doesn't delay the response.""",
        tip_bn=r"""একটা বাস্তব ব্যবহার বলো (checkout-এর পরে analytics), আর বলো এটা response দেরি করায় না।""",
        follow=[("What must a self-hosted setup do so `after()` callbacks finish during shutdown?", "Self-hosted setup-এ shutdown-এর সময় `after()` callback শেষ করতে কী করতে হবে?")],
        related=["next-009", "next-030"],
        refs=[("Next.js Docs — after", "https://nextjs.org/docs/app/api-reference/functions/after")],
    ),
    # ------------------------------------------------------------------ next-q09
    Q(
        id="next-q09", sub="Deployment and Self-hosting", diff="medium", type="quick",
        prio="medium", market="both", mins=1,
        tags=["static-export", "output-export", "deployment"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""What is a static export (`output: 'export'`), and what can't you use with it?""",
        q_bn=r"""Static export (`output: 'export'`) কী, আর এতে কী কী ব্যবহার করা যায় না?""",
        a_en=r"""Setting `output: 'export'` makes `next build` write plain HTML, CSS and JS into an `out` folder that any static host (NGINX, S3, GitHub Pages) can serve. Anything that needs a server is unsupported: Server Actions, `cookies()`, `proxy.ts`, ISR, rewrites/redirects, default image optimisation and dynamic routes without `generateStaticParams`.""",
        a_bn=r"""`output: 'export'` দিলে `next build` সাধারণ HTML, CSS আর JS একটা `out` folder-এ লেখে, যেটা যেকোনো static host (NGINX, S3, GitHub Pages) serve করতে পারে। Server লাগে এমন কিছুই চলে না: Server Action, `cookies()`, `proxy.ts`, ISR, rewrite/redirect, default image optimisation, আর `generateStaticParams` ছাড়া dynamic route।""",
        code=r"""
            // next.config.ts
            const nextConfig = { output: 'export' };
            export default nextConfig;
        """, lang="ts",
        ex_en=r"""Server Components still run, but only at build time. The old `next export` command was removed in Next.js 14.""",
        ex_bn=r"""Server Component তখনও চলে, তবে শুধু build-এর সময়। পুরনো `next export` command Next.js 14-এ সরিয়ে ফেলা হয়েছে।""",
        tip_en=r"""Frame it as "a Next.js SPA/static site with no Node server" and list two or three missing features.""",
        tip_bn=r"""এভাবে বলো "Node server ছাড়া একটা Next.js SPA/static site", আর না-থাকা দুই-তিনটা feature-এর নাম বলো।""",
        follow=[("How would you show images with `next/image` in a static export?", "Static export-এ `next/image` দিয়ে image কীভাবে দেখাবে?")],
        related=["next-019"],
        refs=[("Next.js Docs — Static Exports", "https://nextjs.org/docs/app/guides/static-exports")],
    ),
    # ------------------------------------------------------------------ next-q10
    Q(
        id="next-q10", sub="Server Components and Client Components", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["use-server", "use-client", "server-functions"],
        ver="Next.js 16.4 (App Router)", vs=False, status="stable",
        q_en=r"""What is the difference between `'use client'` and `'use server'`?""",
        q_bn=r"""`'use client'` আর `'use server'`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`'use client'` at the top of a file makes its components Client Components that ship to and hydrate in the browser. `'use server'` marks Server Functions (Server Actions) that the client can call over the network; it is not needed for Server Components, which are already the default.""",
        a_bn=r"""File-এর শুরুতে `'use client'` দিলে সেই file-এর component-গুলো Client Component হয়, যেগুলো browser-এ যায় আর hydrate হয়। `'use server'` এমন Server Function (Server Action) চিহ্নিত করে যেটা client network-এর মাধ্যমে call করতে পারে; Server Component-এর জন্য এটা লাগে না, কারণ ওগুলো আগে থেকেই default।""",
        ex_en=r"""A common mistake is adding `'use server'` to a component file to "make it a Server Component". Every `'use server'` export is a public endpoint, so check auth inside it.""",
        ex_bn=r"""একটা সাধারণ ভুল হলো "Server Component বানাতে" component file-এ `'use server'` দেওয়া। প্রতিটা `'use server'` export একটা public endpoint, তাই এর ভেতরে auth check করো।""",
        tip_en=r"""Say "`'use client'` = a boundary for components, `'use server'` = callable functions" in one line.""",
        tip_bn=r"""এক লাইনে বলো "`'use client'` = component-এর boundary, `'use server'` = call করা যায় এমন function"।""",
        follow=[("Can a Client Component import a Server Action?", "Client Component কি একটা Server Action import করতে পারে?")],
        related=["next-004", "next-013", "next-020"],
        refs=[("Next.js Docs — Server and Client Components", "https://nextjs.org/docs/app/getting-started/server-and-client-components")],
    ),
]

if __name__ == "__main__":
    save("nextjs", "quick", QUESTIONS)
