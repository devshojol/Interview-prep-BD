# Next.js — batch 3 (next-008..010, 017..019, 025, 026)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_IMAGE = ("Next.js Docs — Image Component", "https://nextjs.org/docs/app/api-reference/components/image")
N_IMAGES_GUIDE = ("Next.js Docs — Image Optimization", "https://nextjs.org/docs/app/getting-started/images")
N_ROUTE = ("Next.js Docs — route.js", "https://nextjs.org/docs/app/api-reference/file-conventions/route")
N_ROUTE_HANDLERS = ("Next.js Docs — Route Handlers", "https://nextjs.org/docs/app/getting-started/route-handlers")
N_CACHING = ("Next.js Docs — Caching (Cache Components)", "https://nextjs.org/docs/app/getting-started/caching")
N_GSP = ("Next.js Docs — getStaticProps (Pages Router)", "https://nextjs.org/docs/pages/building-your-application/data-fetching/get-static-props")
N_HYDRATION = ("Next.js Docs — Text content does not match server-rendered HTML", "https://nextjs.org/docs/messages/react-hydration-error")
R_HYDRATEROOT = ("react.dev — hydrateRoot", "https://react.dev/reference/react-dom/client/hydrateRoot")
N_METADATA = ("Next.js Docs — Metadata and OG images", "https://nextjs.org/docs/app/getting-started/metadata-and-og-images")
N_GEN_METADATA = ("Next.js Docs — generateMetadata", "https://nextjs.org/docs/app/api-reference/functions/generate-metadata")
N_SITEMAP = ("Next.js Docs — sitemap.xml", "https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap")
N_OUTPUT = ("Next.js Docs — output (standalone)", "https://nextjs.org/docs/app/api-reference/config/next-config-js/output")
N_DEPLOYING = ("Next.js Docs — Deploying", "https://nextjs.org/docs/app/getting-started/deploying")
N_SELF_HOST = ("Next.js Docs — Self-hosting", "https://nextjs.org/docs/app/guides/self-hosting")
N_PROXY = ("Next.js Docs — proxy.js", "https://nextjs.org/docs/app/api-reference/file-conventions/proxy")
N_AUTH = ("Next.js Docs — Authentication", "https://nextjs.org/docs/app/guides/authentication")
N_DATA_SECURITY = ("Next.js Docs — Data Security", "https://nextjs.org/docs/app/guides/data-security")
N_BLOCKING = ("Next.js Docs — Uncached data was accessed outside of <Suspense>", "https://nextjs.org/docs/messages/blocking-route")
N_SEGMENT_CONFIG = ("Next.js Docs — Route Segment Config", "https://nextjs.org/docs/app/api-reference/file-conventions/route-segment-config")
DOCKER_MULTISTAGE = ("Docker Docs — Multi-stage builds", "https://docs.docker.com/build/building/multi-stage/")

QUESTIONS = [
    # ------------------------------------------------------------------ next-008
    Q(
        id="next-008", sub="Image Optimization", diff="easy", type="debugging",
        prio="high", market="both", mins=4,
        tags=["next-image", "remote-patterns", "lcp", "cls"],
        ver="Next.js 16.4", vs=True, status="stable",
        q_en=r"""
            This product card throws an error in development, and the reviewer says the image config uses an outdated option. Find the problems and fix them.
        """,
        q_bn=r"""
            এই product card development-এ error দিচ্ছে, আর reviewer বলছে image config-এ একটা পুরনো option ব্যবহার হয়েছে। সমস্যাগুলো খুঁজে বের করো আর ঠিক করো।
        """,
        a_en=r"""
            1. **Missing `width` and `height`.** For remote images Next.js can't read the file at build time, so it needs the dimensions (or `fill` with a sized parent). They're also what reserves space and prevents layout shift (CLS).
            2. **`images.domains` is deprecated** (since v14). Use `images.remotePatterns`, which can restrict protocol, hostname and path — otherwise anyone could use your optimiser for arbitrary images on that host.
            3. **No `sizes`** for a responsive grid: without it the browser may download a larger image than needed.

            For the main above-the-fold product image I'd also preload it to improve LCP — in Next.js 16 that's `preload` (the old `priority` prop is deprecated), or simply `loading="eager"`/`fetchPriority="high"`.
        """,
        a_bn=r"""
            1. **`width` আর `height` নেই।** Remote image-এর file Next.js build time-এ পড়তে পারে না, তাই মাপ দিতে হয় (অথবা মাপ দেওয়া parent-সহ `fill`)। এগুলোই জায়গা ধরে রাখে আর layout shift (CLS) ঠেকায়।
            2. **`images.domains` deprecated** (v14 থেকে)। `images.remotePatterns` ব্যবহার করো, যেটা protocol, hostname আর path সীমিত করতে পারে — নইলে যে কেউ ওই host-এর যেকোনো image-এর জন্য তোমার optimiser ব্যবহার করতে পারে।
            3. Responsive grid-এর জন্য **`sizes` নেই**: এটা না দিলে browser দরকারের চেয়ে বড় image download করতে পারে।

            Screen-এর উপরের দিকের মূল product image-এর জন্য LCP ভালো করতে আমি এটা preload-ও করব — Next.js 16-এ সেটা `preload` (পুরনো `priority` prop deprecated), অথবা সহজভাবে `loading="eager"`/`fetchPriority="high"`।
        """,
        ex_en=r"""
            **What `next/image` does:** serves resized images per device (`srcset`), modern formats like WebP/AVIF, lazy-loads by default, and caches optimised results (default `minimumCacheTTL` is 4 hours in v16).

            **Other Next.js 16 image changes worth knowing:** `images.qualities` now defaults to `[75]` (other `quality` values are coerced unless you allow them), `next/legacy/image` is deprecated, and local images with query strings need `localPatterns`.

            **Self-hosting note:** image optimisation runs on your server and uses CPU/memory; for heavy traffic consider a custom `loader` pointing to an image CDN.
        """,
        ex_bn=r"""
            **`next/image` কী করে:** প্রতিটা device-এর জন্য মাপমতো image দেয় (`srcset`), WebP/AVIF-এর মতো আধুনিক format দেয়, default-ভাবে lazy-load করে, আর optimise করা result cache করে (v16-এ default `minimumCacheTTL` ৪ ঘণ্টা)।

            **Next.js 16-এর আরও কিছু image পরিবর্তন:** `images.qualities` এখন default-ভাবে `[75]` (অনুমতি না দিলে অন্য `quality` value কাছের মানে বদলে যায়), `next/legacy/image` deprecated, আর query string-সহ local image-এর জন্য `localPatterns` লাগে।

            **Self-hosting নোট:** image optimisation তোমার server-এ চলে আর CPU/memory খরচ করে; বেশি traffic হলে image CDN-এর দিকে নির্দেশ করে এমন custom `loader` বিবেচনা করো।
        """,
        tip_en=r"""Fix the error first (dimensions), then the security/config issue (`remotePatterns`), then performance (`sizes`, `preload`). Mentioning the v16 `priority` → `preload` change shows you track releases.""",
        tip_bn=r"""আগে error ঠিক করো (মাপ), তারপর security/config সমস্যা (`remotePatterns`), তারপর performance (`sizes`, `preload`)। v16-এর `priority` → `preload` পরিবর্তনের কথা বললে বোঝা যায় তুমি release-এর খবর রাখো।""",
        mist_en=r"""Using `unoptimized` everywhere to silence errors, or allowing all hosts with a `**` wildcard hostname.""",
        mist_bn=r"""Error চুপ করাতে সব জায়গায় `unoptimized` ব্যবহার করা, অথবা `**` wildcard hostname দিয়ে সব host-কে অনুমতি দেওয়া।""",
        code=r"""
            // components/product-card.tsx
            import Image from 'next/image';

            export function ProductCard({ product }: { product: { name: string; image: string } }) {
              return (
                <article>
                  <Image
                    src={`https://cdn.shop-bd.com/products/${product.image}`}
                    alt={product.name}
                  />
                  <h3>{product.name}</h3>
                </article>
              );
            }

            // next.config.ts
            const nextConfig = {
              images: {
                domains: ['cdn.shop-bd.com'],
              },
            };
            export default nextConfig;
        """,
        lang="tsx",
        extra=[dict(lang="tsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            // components/product-card.tsx
            import Image from 'next/image';

            export function ProductCard({ product }: { product: { name: string; image: string } }) {
              return (
                <article>
                  <Image
                    src={`https://cdn.shop-bd.com/products/${product.image}`}
                    alt={product.name}
                    width={400}
                    height={400}
                    sizes="(max-width: 768px) 50vw, 25vw"
                  />
                  <h3>{product.name}</h3>
                </article>
              );
            }

            // next.config.ts
            import type { NextConfig } from 'next';

            const nextConfig: NextConfig = {
              images: {
                remotePatterns: [
                  { protocol: 'https', hostname: 'cdn.shop-bd.com', pathname: '/products/**' },
                ],
              },
            };
            export default nextConfig;
        """)],
        follow=[
            ("When would you use `fill` instead of `width` and `height`?", "কখন `width` আর `height`-এর বদলে `fill` ব্যবহার করবে?"),
            ("How does `next/image` help Core Web Vitals (LCP and CLS)?", "`next/image` কীভাবে Core Web Vitals (LCP আর CLS)-এ সাহায্য করে?"),
        ],
        refs=[N_IMAGE, N_IMAGES_GUIDE],
    ),
    # ------------------------------------------------------------------ next-009
    Q(
        id="next-009", sub="Route Handlers", diff="easy", type="coding",
        prio="high", market="bangladesh", mins=6,
        tags=["route-handlers", "api", "rest", "validation"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""
            Write a Route Handler for `GET /api/products/[id]` that:
            - returns the product as JSON with status 200;
            - returns `400` with `{ "error": "Invalid product id" }` if `id` isn't a positive integer;
            - returns `404` with `{ "error": "Product not found" }` if it doesn't exist.
            Assume a helper `getProductById(id: number)` that returns the product or `null`.
        """,
        q_bn=r"""
            `GET /api/products/[id]`-এর জন্য একটা Route Handler লেখো, যেটা:
            - product-টা JSON হিসেবে status 200-সহ return করবে;
            - `id` positive integer না হলে `{ "error": "Invalid product id" }`-সহ `400` return করবে;
            - product না থাকলে `{ "error": "Product not found" }`-সহ `404` return করবে।
            ধরে নাও একটা helper `getProductById(id: number)` আছে, যেটা product বা `null` return করে।
        """,
        a_en=r"""
            A Route Handler is a `route.ts` file that exports functions named after HTTP methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`). It uses the standard Web `Request`/`Response` APIs.

            The second argument contains `params`, which is a **Promise** in Next.js 16, so I `await` it. Route params are always strings, so I convert and validate before touching the database, then return `Response.json(body, { status })` for each case.

            I use Route Handlers for endpoints other clients call — mobile apps, webhooks, third parties. For mutations triggered from my own React UI, Server Actions are usually simpler.
        """,
        a_bn=r"""
            Route Handler হলো একটা `route.ts` file, যেটা HTTP method-এর নামে function export করে (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`)। এটা standard Web `Request`/`Response` API ব্যবহার করে।

            দ্বিতীয় argument-এ থাকে `params`, যেটা Next.js 16-এ একটা **Promise**, তাই আমি `await` করি। Route param সবসময় string, তাই database ছোঁয়ার আগে convert আর validate করি, তারপর প্রতিটা ক্ষেত্রে `Response.json(body, { status })` return করি।

            অন্য client যে endpoint call করে — mobile app, webhook, third party — সেগুলোর জন্য আমি Route Handler ব্যবহার করি। নিজের React UI থেকে হওয়া mutation-এর জন্য সাধারণত Server Action বেশি সহজ।
        """,
        ex_en=r"""
            - **Edge cases:** `"12abc"`, `"1.5"`, `"-3"` and `"0"` must all return 400 — `Number()` plus `Number.isInteger` and `> 0` handles them (`Number('12abc')` is `NaN`).
            - **A `route.ts` and a `page.tsx` can't live in the same segment** — that's why APIs usually sit under `app/api/`.
            - **Caching:** with Cache Components, `GET` handlers follow the same prerendering model as pages; this handler reads request-specific `params`, so it runs per request. Wrap `getProductById` in `'use cache'` if the data can be cached.
            - **Security:** add auth checks, rate limiting and CORS headers for public endpoints; never return internal error details.
        """,
        ex_bn=r"""
            - **Edge case:** `"12abc"`, `"1.5"`, `"-3"` আর `"0"` — সবগুলোর জন্য 400 return করতে হবে — `Number()`-এর সাথে `Number.isInteger` আর `> 0` এগুলো সামলায় (`Number('12abc')` হলো `NaN`)।
            - **একই segment-এ `route.ts` আর `page.tsx` থাকতে পারে না** — এজন্যই API সাধারণত `app/api/`-এর নিচে থাকে।
            - **Caching:** Cache Components থাকলে `GET` handler page-এর মতো একই prerendering model মানে; এই handler request-নির্দিষ্ট `params` পড়ে, তাই প্রতি request-এ চলে। Data cache করা গেলে `getProductById`-কে `'use cache'`-এ wrap করো।
            - **Security:** public endpoint-এ auth check, rate limiting আর CORS header যোগ করো; ভেতরের error-এর বিস্তারিত কখনো return করবে না।
        """,
        tip_en=r"""Write the validation before the database call and say why ("params are strings and untrusted"). Ending with when you'd choose a Route Handler vs a Server Action shows architectural judgement.""",
        tip_bn=r"""Database call-এর আগে validation লেখো আর কারণ বলো ("params string, আর বিশ্বাসযোগ্য না")। শেষে কখন Route Handler আর কখন Server Action বেছে নেবে বললে architecture-এর বিচারবুদ্ধি বোঝা যায়।""",
        mist_en=r"""Reading `params.id` synchronously, using `parseInt` (which accepts `"12abc"` as 12), or returning 200 with an error body.""",
        mist_bn=r"""`params.id` synchronously পড়া, `parseInt` ব্যবহার করা (যেটা `"12abc"`-কে 12 হিসেবে মেনে নেয়), অথবা error body-সহ 200 return করা।""",
        code=r"""
            // app/api/products/[id]/route.ts
            import { getProductById } from '@/lib/products';

            export async function GET(
              _request: Request,
              { params }: { params: Promise<{ id: string }> }
            ) {
              const { id } = await params;
              const productId = Number(id);

              if (!Number.isInteger(productId) || productId <= 0) {
                return Response.json({ error: 'Invalid product id' }, { status: 400 });
              }

              const product = await getProductById(productId);
              if (!product) {
                return Response.json({ error: 'Product not found' }, { status: 404 });
              }

              return Response.json(product); // 200 by default
            }
        """,
        lang="typescript",
        time="O(1) (plus one database lookup)", space="O(1)",
        follow=[
            ("How would you add CORS support for a mobile web client on another domain?", "অন্য domain-এর একটা mobile web client-এর জন্য CORS support কীভাবে যোগ করবে?"),
            ("When would you use a Server Action instead of this Route Handler?", "কখন এই Route Handler-এর বদলে Server Action ব্যবহার করবে?"),
        ],
        refs=[N_ROUTE, N_ROUTE_HANDLERS],
    ),
    # ------------------------------------------------------------------ next-010
    Q(
        id="next-010", sub="Rendering Strategies", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["ssr", "ssg", "isr", "csr", "ppr"],
        ver="Next.js 16.4 (App Router with Cache Components; Pages Router = legacy)", vs=True, status="stable",
        q_en=r"""Explain static generation (SSG), server-side rendering (SSR), incremental static regeneration (ISR) and client-side rendering (CSR). How do they map to Next.js 16?""",
        q_bn=r"""Static generation (SSG), server-side rendering (SSR), incremental static regeneration (ISR) আর client-side rendering (CSR) ব্যাখ্যা করো। Next.js 16-এ এগুলো কীভাবে মেলে?""",
        a_en=r"""
            - **SSG:** HTML is generated at build time and served from a CDN. Fastest and cheapest, but the same for everyone until the next build.
            - **SSR:** HTML is generated on every request. Always fresh and can be personalised, but costs server time on each request.
            - **ISR:** static pages that regenerate in the background after a time window or on demand — static speed with periodic freshness.
            - **CSR:** the browser downloads JavaScript, then fetches data and renders. Fine for private, highly interactive dashboards, weaker for first paint and SEO.

            In Next.js 16 with Cache Components you don't pick one mode per page — you choose **per component**. Static parts and `'use cache'` data are prerendered into a static shell (SSG/ISR-like, refreshed by `cacheLife` or tags), while runtime data inside `<Suspense>` is rendered per request and streamed (SSR-like). This mix is **Partial Prerendering**. Client Components that fetch in the browser are still CSR.

            In the legacy Pages Router the mapping is per page: `getStaticProps` (SSG), `getServerSideProps` (SSR), and `revalidate` returned from `getStaticProps` (ISR).
        """,
        a_bn=r"""
            - **SSG:** build time-এ HTML তৈরি হয় আর CDN থেকে serve হয়। সবচেয়ে দ্রুত আর সস্তা, কিন্তু পরের build পর্যন্ত সবার জন্য একই।
            - **SSR:** প্রতিটা request-এ HTML তৈরি হয়। সবসময় fresh আর personalise করা যায়, কিন্তু প্রতিটা request-এ server-এর সময় খরচ হয়।
            - **ISR:** static page, যেটা একটা সময়ের পর বা দরকারমতো background-এ আবার তৈরি হয় — static-এর গতি আর মাঝে মাঝে fresh data।
            - **CSR:** browser JavaScript download করে, তারপর data fetch করে render করে। Private, খুব interactive dashboard-এর জন্য ঠিক আছে, কিন্তু first paint আর SEO-তে দুর্বল।

            Cache Components-সহ Next.js 16-এ প্রতি page-এ একটা mode বেছে নিতে হয় না — বেছে নাও **প্রতি component অনুযায়ী**। Static অংশ আর `'use cache'` data একটা static shell-এ prerender হয় (SSG/ISR-এর মতো, `cacheLife` বা tag দিয়ে refresh হয়), আর `<Suspense>`-এর ভেতরের runtime data প্রতি request-এ render হয়ে stream হয় (SSR-এর মতো)। এই মিশ্রণই **Partial Prerendering**। Browser-এ fetch করা Client Component এখনো CSR।

            Legacy Pages Router-এ mapping প্রতি page অনুযায়ী: `getStaticProps` (SSG), `getServerSideProps` (SSR), আর `getStaticProps` থেকে return করা `revalidate` (ISR)।
        """,
        ex_en=r"""
            **How to choose:** ask "is this data the same for every visitor, and how fresh must it be?"
            - Same for everyone, rarely changes → cache it (`cacheLife('days')` + tags).
            - Same for everyone, changes often → shorter `cacheLife` or tag invalidation on change.
            - Different per user (cookies, auth) → dynamic, inside `<Suspense>`.

            The win of the component-level model: one page can serve a cached product description instantly while streaming the user's cart, instead of making the whole page dynamic because one small part reads a cookie (which is what happened in the previous model).
        """,
        ex_bn=r"""
            **কীভাবে বেছে নেবে:** প্রশ্ন করো "এই data কি প্রত্যেক visitor-এর জন্য একই, আর কতটা fresh হতে হবে?"
            - সবার জন্য একই, কম বদলায় → cache করো (`cacheLife('days')` + tag)।
            - সবার জন্য একই, ঘন ঘন বদলায় → ছোট `cacheLife`, বা পরিবর্তনের সময় tag invalidation।
            - প্রতি user-এ আলাদা (cookie, auth) → dynamic, `<Suspense>`-এর ভেতরে।

            Component-level model-এর লাভ: একটা page cached product description সাথে সাথে দেখাতে পারে আর user-এর cart stream করতে পারে — ছোট একটা অংশ cookie পড়ে বলে পুরো page dynamic করতে হয় না (আগের model-এ যেটা হতো)।
        """,
        tip_en=r"""Define the four classic terms briefly, then show you know the modern twist: "in Next.js 16 it's per component, not per page — that's Partial Prerendering". Label the Pages Router functions as legacy.""",
        tip_bn=r"""চারটা classic term সংক্ষেপে define করো, তারপর দেখাও তুমি আধুনিক পরিবর্তনটা জানো: "Next.js 16-এ এটা প্রতি page না, প্রতি component — এটাই Partial Prerendering"। Pages Router-এর function-গুলোকে legacy বলো।""",
        mist_en=r"""Saying the App Router uses `getServerSideProps`, or claiming a page is "either static or dynamic" in a Cache Components app.""",
        mist_bn=r"""বলা যে App Router `getServerSideProps` ব্যবহার করে, অথবা দাবি করা যে Cache Components app-এ একটা page "হয় static, নয় dynamic"।""",
        code=r"""
            // app/page.tsx — one page, three strategies
            import { Suspense } from 'react';
            import { cacheLife } from 'next/cache';

            export default function Home() {
              return (
                <>
                  <Hero />                       {/* static: prerendered at build */}
                  <TopDeals />                   {/* cached: part of the static shell, refreshed hourly */}
                  <Suspense fallback={<p>Loading your picks…</p>}>
                    <PersonalPicks />            {/* dynamic: reads cookies, streamed per request */}
                  </Suspense>
                </>
              );
            }

            async function TopDeals() {
              'use cache';
              cacheLife('hours');
              const deals = await getTopDeals();
              return <DealList deals={deals} />;
            }
        """,
        lang="tsx",
        follow=[
            ("Why did reading a cookie make the whole route dynamic in the previous model?", "আগের model-এ একটা cookie পড়লেই কেন পুরো route dynamic হয়ে যেত?"),
            ("When is client-side rendering still the right choice?", "কখন এখনো client-side rendering সঠিক পছন্দ?"),
        ],
        refs=[N_CACHING, N_GSP],
    ),
    # ------------------------------------------------------------------ next-017
    Q(
        id="next-017", sub="Hydration Errors", diff="medium", type="debugging",
        prio="high", market="both", mins=7,
        tags=["hydration", "ssr", "debugging", "client-components"],
        ver="Next.js 16.4 (React 19.3)", vs=True, status="stable",
        q_en=r"""
            Users in Dhaka see the error "Hydration failed because the server rendered HTML didn't match the client" on the order page, mostly on phones. Find every cause of the mismatch in this component and fix it.
        """,
        q_bn=r"""
            Dhaka-র user-রা order page-এ "Hydration failed because the server rendered HTML didn't match the client" error দেখছে, বেশিরভাগ phone-এ। এই component-এ mismatch-এর সব কারণ খুঁজে বের করো আর ঠিক করো।
        """,
        a_en=r"""
            Hydration means React attaches to the server HTML and expects the first client render to produce **exactly the same markup**. This component breaks that in three ways:

            1. **`typeof window` branch:** on the server `isMobile` is always `false`; on a phone the client computes `true` and renders an extra `<span>`. Responsive differences belong in CSS media queries (or in client-only rendering after hydration).
            2. **`toLocaleString()` without a fixed locale and time zone:** the server (often UTC, `en-US`) and the browser (Asia/Dhaka, maybe `bn-BD`) produce different text. Format with an explicit locale and `timeZone`, or format once on the server and pass the string.
            3. **Invalid HTML nesting:** a `<div>` inside a `<p>` isn't allowed; the browser's parser closes the `<p>` early, so the DOM no longer matches what React expects. Use valid nesting.

            After fixing, the server and client produce identical HTML, and the error disappears.
        """,
        a_bn=r"""
            Hydration মানে React server-এর HTML-এর সাথে যুক্ত হয়, আর আশা করে client-এর প্রথম render **হুবহু একই markup** তৈরি করবে। এই component তিনভাবে সেটা ভাঙছে:

            1. **`typeof window` branch:** server-এ `isMobile` সবসময় `false`; phone-এ client হিসাব করে `true` আর একটা বাড়তি `<span>` render করে। Responsive পার্থক্য CSS media query-তে রাখা উচিত (অথবা hydration-এর পর শুধু client-এ render)।
            2. **নির্দিষ্ট locale আর time zone ছাড়া `toLocaleString()`:** server (প্রায়ই UTC, `en-US`) আর browser (Asia/Dhaka, হয়তো `bn-BD`) আলাদা text তৈরি করে। নির্দিষ্ট locale আর `timeZone` দিয়ে format করো, অথবা server-এ একবার format করে string পাঠাও।
            3. **ভুল HTML nesting:** `<p>`-এর ভেতরে `<div>` বৈধ না; browser-এর parser `<p>` আগেই বন্ধ করে দেয়, ফলে DOM আর React-এর প্রত্যাশার সাথে মেলে না। বৈধ nesting ব্যবহার করো।

            ঠিক করার পর server আর client হুবহু একই HTML তৈরি করে, আর error চলে যায়।
        """,
        ex_en=r"""
            **Other common causes:** `Math.random()`/`Date.now()` in render (use `useId` for ids), reading `localStorage` during render, browser extensions that inject attributes into the HTML (out of your control — test in a clean profile), and CSS-in-JS libraries without proper SSR setup.

            **Escape hatches, used sparingly:**
            - `suppressHydrationWarning` on an element whose text *must* differ (e.g. a timestamp) — works one level deep only.
            - Render client-only UI after hydration: in React 19.3, `use(browser())` (from `react-dom`) inside a `<Suspense>` boundary suspends on the server so the fallback goes into the HTML; previously people used a "mounted" state set in an effect.

            **Debugging:** React 19 prints a diff of the mismatching markup in the console; reproduce with the browser's time zone and locale changed in DevTools sensors.
        """,
        ex_bn=r"""
            **আরও সাধারণ কারণ:** render-এর সময় `Math.random()`/`Date.now()` (id-র জন্য `useId` ব্যবহার করো), render-এর সময় `localStorage` পড়া, browser extension যেগুলো HTML-এ attribute ঢুকিয়ে দেয় (তোমার নিয়ন্ত্রণের বাইরে — একটা পরিষ্কার profile-এ test করো), আর ঠিকমতো SSR setup ছাড়া CSS-in-JS library।

            **Escape hatch, কম কম ব্যবহার করো:**
            - যে element-এর text-কে আলাদা *হতেই হবে* (যেমন timestamp), সেখানে `suppressHydrationWarning` — শুধু এক স্তর গভীর পর্যন্ত কাজ করে।
            - Hydration-এর পর client-only UI render করা: React 19.3-এ `<Suspense>` boundary-র ভেতরে `use(browser())` (`react-dom` থেকে) server-এ suspend করে, ফলে fallback HTML-এ যায়; আগে মানুষ effect-এ set করা একটা "mounted" state ব্যবহার করত।

            **Debugging:** React 19 console-এ না মেলা markup-এর একটা diff দেখায়; DevTools sensors-এ browser-এর time zone আর locale বদলে reproduce করো।
        """,
        tip_en=r"""Start by defining hydration in one sentence ("the first client render must match the server HTML"), then classify causes: environment-dependent values, non-deterministic values, invalid HTML. That framework lets you debug any hydration bug, not just this one.""",
        tip_bn=r"""এক বাক্যে hydration define করে শুরু করো ("client-এর প্রথম render server-এর HTML-এর সাথে মিলতে হবে"), তারপর কারণগুলো ভাগ করো: environment-নির্ভর value, non-deterministic value, ভুল HTML। এই কাঠামো দিয়ে শুধু এটা না, যেকোনো hydration bug debug করা যায়।""",
        mist_en=r"""Wrapping the whole page in `suppressHydrationWarning`, or disabling SSR for the entire route to hide the error.""",
        mist_bn=r"""পুরো page-কে `suppressHydrationWarning`-এ wrap করা, অথবা error লুকাতে পুরো route-এর SSR বন্ধ করে দেওয়া।""",
        code=r"""
            'use client';

            export function OrderSummary({ order }: { order: { createdAt: string; status: string } }) {
              const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;

              return (
                <p>
                  Ordered {new Date(order.createdAt).toLocaleString()}
                  {isMobile ? <span> (tap for details)</span> : null}
                  <div className="badge">{order.status}</div>
                </p>
              );
            }
        """,
        lang="tsx",
        extra=[dict(lang="tsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            'use client';

            // Same output on the server and in every browser
            const dhakaTime = new Intl.DateTimeFormat('en-GB', {
              dateStyle: 'medium',
              timeStyle: 'short',
              timeZone: 'Asia/Dhaka',
            });

            export function OrderSummary({ order }: { order: { createdAt: string; status: string } }) {
              return (
                <div>
                  <p>
                    Ordered {dhakaTime.format(new Date(order.createdAt))}
                    {/* shown only on small screens via CSS: .mobile-only { display: none } + media query */}
                    <span className="mobile-only"> (tap for details)</span>
                  </p>
                  <div className="badge">{order.status}</div>
                </div>
              );
            }
        """)],
        follow=[
            ("Why is `suppressHydrationWarning` acceptable for a timestamp but not as a general fix?", "Timestamp-এর জন্য `suppressHydrationWarning` কেন গ্রহণযোগ্য, কিন্তু সাধারণ সমাধান হিসেবে না?"),
            ("How would you render a component only in the browser without causing a mismatch?", "Mismatch না ঘটিয়ে কোনো component শুধু browser-এ কীভাবে render করবে?"),
        ],
        refs=[N_HYDRATION, R_HYDRATEROOT],
    ),
    # ------------------------------------------------------------------ next-018
    Q(
        id="next-018", sub="Metadata and SEO", diff="medium", type="conceptual",
        prio="high", market="both", mins=6,
        tags=["seo", "metadata", "generatemetadata", "sitemap", "open-graph"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""How do you handle SEO in the App Router? Cover static and dynamic metadata, Open Graph images, sitemaps and robots.""",
        q_bn=r"""App Router-এ SEO কীভাবে সামলাও? Static আর dynamic metadata, Open Graph image, sitemap আর robots — সব কভার করো।""",
        a_en=r"""
            - **Static metadata:** export a `metadata` object from a `layout.tsx` or `page.tsx`. In the root layout I set `metadataBase` (so relative URLs resolve), a title template like `'%s | Shop'`, and defaults for description and Open Graph.
            - **Dynamic metadata:** export `async function generateMetadata({ params })`, await `params`, load the data and return title, description, `alternates.canonical` and `openGraph`. The data function is cached/deduplicated (`'use cache'` or React `cache`) so the page and the metadata don't fetch twice.
            - **Open Graph images:** an `opengraph-image.tsx` file next to a page can generate the image with `ImageResponse`, or you point `openGraph.images` to a static file.
            - **Sitemap and robots:** `app/sitemap.ts` returns a `MetadataRoute.Sitemap` array (can be generated from the database); `app/robots.ts` returns rules and the sitemap URL.
            - **Structured data:** render JSON-LD in a `<script type="application/ld+json">` tag in the page.

            Server rendering is the biggest SEO win itself: crawlers get real HTML instead of an empty shell.
        """,
        a_bn=r"""
            - **Static metadata:** `layout.tsx` বা `page.tsx` থেকে একটা `metadata` object export করো। Root layout-এ আমি `metadataBase` set করি (যাতে relative URL ঠিকমতো resolve হয়), `'%s | Shop'`-এর মতো একটা title template, আর description ও Open Graph-এর default।
            - **Dynamic metadata:** `async function generateMetadata({ params })` export করো, `params` await করো, data load করো, আর title, description, `alternates.canonical` ও `openGraph` return করো। Data function cache/deduplicate করা থাকে (`'use cache'` বা React `cache`), যাতে page আর metadata দুইবার fetch না করে।
            - **Open Graph image:** page-এর পাশে একটা `opengraph-image.tsx` file `ImageResponse` দিয়ে image তৈরি করতে পারে, অথবা `openGraph.images`-কে একটা static file-এর দিকে নির্দেশ করো।
            - **Sitemap আর robots:** `app/sitemap.ts` একটা `MetadataRoute.Sitemap` array return করে (database থেকে তৈরি করা যায়); `app/robots.ts` নিয়মগুলো আর sitemap URL return করে।
            - **Structured data:** page-এ একটা `<script type="application/ld+json">` tag-এ JSON-LD render করো।

            Server rendering নিজেই সবচেয়ে বড় SEO সুবিধা: crawler খালি shell না, আসল HTML পায়।
        """,
        ex_en=r"""
            - **Metadata merges** from the root layout down to the page; nested values override parent ones (and the `title.template` from a parent applies to child titles).
            - **Metadata only works in Server Components** — a `'use client'` page can't export `metadata`. That's one more reason to keep pages as Server Components.
            - **Streaming metadata:** with Partial Prerendering, dynamic metadata can stream after the shell. Crawlers that can't handle that are detected by user agent and get a fully rendered response instead.
            - **Handle missing content properly:** call `notFound()` for missing products (it also adds a `noindex` robots meta tag) so search engines don't index soft-404 pages.
        """,
        ex_bn=r"""
            - **Metadata merge হয়** root layout থেকে page পর্যন্ত; nested value parent-এর value override করে (আর parent-এর `title.template` child-এর title-এ প্রযোজ্য হয়)।
            - **Metadata শুধু Server Component-এ কাজ করে** — `'use client'` page `metadata` export করতে পারে না। Page-কে Server Component রাখার এটা আরেকটা কারণ।
            - **Streaming metadata:** Partial Prerendering-এ dynamic metadata shell-এর পরে stream হতে পারে। যে crawler এটা সামলাতে পারে না, user agent দিয়ে তাকে চিনে পুরোপুরি render করা response দেওয়া হয়।
            - **না থাকা content ঠিকভাবে সামলাও:** না থাকা product-এর জন্য `notFound()` call করো (এটা একটা `noindex` robots meta tag-ও যোগ করে), যাতে search engine soft-404 page index না করে।
        """,
        tip_en=r"""Organise the answer by file/API (`metadata`, `generateMetadata`, `opengraph-image`, `sitemap.ts`, `robots.ts`) and finish with one SEO pitfall you've seen (missing canonicals, soft 404s). Concrete beats generic.""",
        tip_bn=r"""উত্তরটা file/API অনুযায়ী সাজাও (`metadata`, `generateMetadata`, `opengraph-image`, `sitemap.ts`, `robots.ts`), আর শেষে নিজের দেখা একটা SEO ভুল বলো (canonical না থাকা, soft 404)। সাধারণ কথার চেয়ে নির্দিষ্ট উদাহরণ বেশি কাজে দেয়।""",
        mist_en=r"""Using `next/head` in the App Router (that's the Pages Router API), or exporting `metadata` from a Client Component.""",
        mist_bn=r"""App Router-এ `next/head` ব্যবহার করা (এটা Pages Router-এর API), অথবা Client Component থেকে `metadata` export করা।""",
        code=r"""
            // app/products/[slug]/page.tsx
            import type { Metadata } from 'next';
            import { getProduct } from '@/lib/products'; // cached with 'use cache'

            export async function generateMetadata(
              { params }: { params: Promise<{ slug: string }> }
            ): Promise<Metadata> {
              const { slug } = await params;
              const product = await getProduct(slug);
              return {
                title: product.name,                       // root template: '%s | Shop'
                description: product.summary,
                alternates: { canonical: `/products/${slug}` },
                openGraph: { images: [{ url: product.imageUrl, width: 1200, height: 630 }] },
              };
            }

            // app/sitemap.ts
            import type { MetadataRoute } from 'next';

            export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
              const products = await getAllProductSlugs();
              return [
                { url: 'https://shop.example.com', lastModified: new Date() },
                ...products.map((p) => ({
                  url: `https://shop.example.com/products/${p.slug}`,
                  lastModified: p.updatedAt,
                })),
              ];
            }

            // app/robots.ts
            import type { MetadataRoute } from 'next';

            export default function robots(): MetadataRoute.Robots {
              return {
                rules: { userAgent: '*', allow: '/', disallow: ['/account', '/checkout'] },
                sitemap: 'https://shop.example.com/sitemap.xml',
              };
            }
        """,
        lang="tsx",
        follow=[
            ("How do you avoid fetching the same product twice in `generateMetadata` and the page?", "`generateMetadata` আর page-এ একই product দুইবার fetch হওয়া কীভাবে এড়াবে?"),
            ("How would you generate a sitemap for 2 million products?", "২০ লাখ product-এর জন্য sitemap কীভাবে তৈরি করবে?"),
        ],
        refs=[N_METADATA, N_GEN_METADATA, N_SITEMAP],
    ),
    # ------------------------------------------------------------------ next-019
    Q(
        id="next-019", sub="Deployment and Self-hosting", diff="medium", type="scenario",
        prio="high", market="both", mins=8,
        tags=["docker", "standalone", "self-hosting", "deployment", "nginx"],
        ver="Next.js 16.4, Node.js 24 LTS, Docker Engine 29", vs=True, status="stable",
        q_en=r"""
            Your company wants to self-host a Next.js 16 app on a VPS (later on AWS ECS) using Docker instead of Vercel. How do you build a small, secure image, and what production issues do you plan for?
        """,
        q_bn=r"""
            তোমার company Vercel-এর বদলে Docker দিয়ে একটা VPS-এ (পরে AWS ECS-এ) Next.js 16 app self-host করতে চায়। ছোট, নিরাপদ image কীভাবে build করবে, আর production-এর কোন কোন সমস্যার জন্য পরিকল্পনা করবে?
        """,
        a_en=r"""
            **Image:** set `output: 'standalone'` in `next.config`. `next build` then creates `.next/standalone` with a minimal `server.js` and only the `node_modules` files the app actually uses. A multi-stage Dockerfile installs dependencies, builds, and copies just three things into a slim runtime image: the standalone folder, `.next/static` and `public` (standalone doesn't include those two). It runs as the non-root `node` user with `node server.js`, `HOSTNAME=0.0.0.0` and `PORT=3000`.

            **Plan for:**
            - **Environment variables:** `NEXT_PUBLIC_*` values are inlined at build time, so one image can't switch them per environment. Read config on the server at request time and pass it down, or build per environment.
            - **Reverse proxy:** NGINX or a load balancer in front for TLS, compression and request limits — with response buffering disabled so streaming works.
            - **Multiple containers:** share the cache (cache handlers), use the same `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` for all, and set `deploymentId` for rolling deploys.
            - **Operations:** a health-check route, logs to stdout, graceful shutdown on `SIGTERM`, and memory limits (image optimisation is CPU/memory hungry).
        """,
        a_bn=r"""
            **Image:** `next.config`-এ `output: 'standalone'` দাও। তখন `next build` একটা ছোট `server.js` আর app আসলে যেসব `node_modules` file ব্যবহার করে শুধু সেগুলো নিয়ে `.next/standalone` তৈরি করে। একটা multi-stage Dockerfile dependency install করে, build করে, আর একটা হালকা runtime image-এ শুধু তিনটা জিনিস copy করে: standalone folder, `.next/static` আর `public` (standalone এই দুটো নিজে রাখে না)। এটা non-root `node` user হিসেবে `node server.js` দিয়ে চলে, `HOSTNAME=0.0.0.0` আর `PORT=3000`-সহ।

            **পরিকল্পনা রাখতে হবে:**
            - **Environment variable:** `NEXT_PUBLIC_*` value build time-এ বসিয়ে দেওয়া হয়, তাই একটা image প্রতি environment-এ এগুলো বদলাতে পারে না। Request time-এ server-এ config পড়ে নিচে পাঠাও, অথবা প্রতি environment-এ আলাদা build করো।
            - **Reverse proxy:** TLS, compression আর request limit-এর জন্য সামনে NGINX বা load balancer — response buffering বন্ধ রেখে, যাতে streaming কাজ করে।
            - **একাধিক container:** cache share করো (cache handler), সবগুলোর জন্য একই `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` ব্যবহার করো, আর rolling deploy-এর জন্য `deploymentId` set করো।
            - **Operations:** একটা health-check route, stdout-এ log, `SIGTERM`-এ graceful shutdown, আর memory limit (image optimisation অনেক CPU/memory খায়)।
        """,
        ex_en=r"""
            **Why standalone:** a full `node_modules` can be hundreds of MB; output file tracing copies only what's needed, which shrinks images and attack surface and speeds up deploys.

            **Common mistakes in production:**
            - Forgetting to copy `.next/static` → CSS/JS 404s, unstyled pages.
            - Binding to `localhost` inside the container → the app isn't reachable from outside; `HOSTNAME=0.0.0.0` fixes it.
            - Running as root, or baking secrets into image layers via `ENV`/`COPY .env` — pass secrets at runtime instead.
            - Using an EOL Node.js base image — Node.js 24 LTS is the safe choice today (Next.js 16 needs at least 20.9).

            **Vercel vs self-hosting:** Vercel handles the CDN, image optimisation, cache sharing, skew protection and scaling for you; self-hosting gives cost control and data residency but you own all of that.
        """,
        ex_bn=r"""
            **Standalone কেন:** পুরো `node_modules` কয়েকশো MB হতে পারে; output file tracing শুধু দরকারি জিনিস copy করে, ফলে image ছোট হয়, attack surface কমে আর deploy দ্রুত হয়।

            **Production-এর সাধারণ ভুল:**
            - `.next/static` copy করতে ভুলে যাওয়া → CSS/JS 404, style ছাড়া page।
            - Container-এর ভেতরে `localhost`-এ bind করা → বাইরে থেকে app-এ পৌঁছানো যায় না; `HOSTNAME=0.0.0.0` এটা ঠিক করে।
            - Root হিসেবে চালানো, অথবা `ENV`/`COPY .env` দিয়ে image layer-এ secret ঢুকিয়ে ফেলা — secret runtime-এ পাঠাও।
            - EOL Node.js base image ব্যবহার করা — আজকের দিনে Node.js 24 LTS নিরাপদ পছন্দ (Next.js 16-এর জন্য কমপক্ষে 20.9 লাগে)।

            **Vercel বনাম self-hosting:** Vercel তোমার হয়ে CDN, image optimisation, cache sharing, skew protection আর scaling সামলায়; self-hosting খরচের নিয়ন্ত্রণ আর data residency দেয়, কিন্তু এসবের দায়িত্ব তোমার।
        """,
        tip_en=r"""Show the Dockerfile reasoning (standalone, multi-stage, non-root), then pivot to "what bites you in production" — env-var inlining and multi-instance consistency are the points that impress.""",
        tip_bn=r"""Dockerfile-এর যুক্তি দেখাও (standalone, multi-stage, non-root), তারপর "production-এ কী সমস্যায় ফেলে" সেদিকে যাও — env-var inlining আর multi-instance consistency হলো সেই পয়েন্ট, যেগুলো প্রভাব ফেলে।""",
        mist_en=r"""Copying the whole project and `node_modules` into a single-stage image, or expecting a `NEXT_PUBLIC_` variable set with `docker run -e` to change the client bundle.""",
        mist_bn=r"""পুরো project আর `node_modules` একটা single-stage image-এ copy করা, অথবা আশা করা যে `docker run -e` দিয়ে set করা `NEXT_PUBLIC_` variable client bundle বদলে দেবে।""",
        code=r"""
            # syntax=docker/dockerfile:1
            FROM node:24-alpine AS deps
            WORKDIR /app
            COPY package.json package-lock.json ./
            RUN npm ci

            FROM node:24-alpine AS builder
            WORKDIR /app
            COPY --from=deps /app/node_modules ./node_modules
            COPY . .
            ENV NEXT_TELEMETRY_DISABLED=1
            RUN npm run build            # next.config.ts has output: 'standalone'

            FROM node:24-alpine AS runner
            WORKDIR /app
            ENV NODE_ENV=production \
                NEXT_TELEMETRY_DISABLED=1 \
                HOSTNAME=0.0.0.0 \
                PORT=3000
            COPY --from=builder --chown=node:node /app/public ./public
            COPY --from=builder --chown=node:node /app/.next/standalone ./
            COPY --from=builder --chown=node:node /app/.next/static ./.next/static
            USER node
            EXPOSE 3000
            HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1:3000/api/health || exit 1
            CMD ["node", "server.js"]
        """,
        lang="dockerfile",
        follow=[
            ("How would you use one Docker image for staging and production if the client needs different API URLs?", "Client-এর আলাদা API URL লাগলে staging আর production-এ একটাই Docker image কীভাবে ব্যবহার করবে?"),
            ("What changes when you scale from one container to five?", "একটা container থেকে পাঁচটায় scale করলে কী কী বদলায়?"),
        ],
        related=["next-007"],
        refs=[N_OUTPUT, N_SELF_HOST, DOCKER_MULTISTAGE],
    ),
    # ------------------------------------------------------------------ next-025
    Q(
        id="next-025", sub="Proxy (formerly Middleware)", diff="hard", type="coding",
        prio="high", market="both", mins=10,
        tags=["proxy", "middleware", "authentication", "redirects", "nextjs-16"],
        ver="Next.js 16.4 (proxy.ts; middleware.ts deprecated)", vs=True, status="stable",
        q_en=r"""
            Write a `proxy.ts` for Next.js 16 that:
            - redirects signed-out users from `/dashboard` and anything below it to `/login?from=<original path and query>`;
            - redirects signed-in users who open `/login` or `/signup` to `/dashboard`;
            - does not run for API routes, `_next/static`, `_next/image`, `favicon.ico`, or image files.
            Then explain what should **not** be done in proxy.
        """,
        q_bn=r"""
            Next.js 16-এর জন্য একটা `proxy.ts` লেখো, যেটা:
            - sign-out থাকা user-কে `/dashboard` আর তার নিচের সবকিছু থেকে `/login?from=<আসল path আর query>`-এ redirect করবে;
            - sign-in থাকা user `/login` বা `/signup` খুললে `/dashboard`-এ redirect করবে;
            - API route, `_next/static`, `_next/image`, `favicon.ico` বা image file-এর জন্য চলবে না।
            তারপর ব্যাখ্যা করো proxy-তে কী **করা উচিত না**।
        """,
        a_en=r"""
            In Next.js 16, `middleware.ts` is deprecated and renamed to **`proxy.ts`**, exporting a `proxy` function (or a default export). It runs before routing on the **Node.js runtime** by default, and the `matcher` in `config` limits where it runs — the matcher values must be static constants.

            My proxy only does an **optimistic check**: it decrypts/verifies the session cookie (no database call) and redirects accordingly. The `from` parameter keeps the original destination for after login.

            What not to do in proxy:
            - **Authoritative authorization** — it's a fast first filter, not the security boundary. Server Actions are POSTs to the page route, and a matcher change can silently skip them, so every Server Component, Server Action and Route Handler must verify access itself (a data-access layer).
            - **Slow work** like database queries or large fetches — proxy runs on every matched request, including prefetches, and adds latency everywhere.
            - Relying on **shared globals/module state** between invocations.
        """,
        a_bn=r"""
            Next.js 16-এ `middleware.ts` deprecated, নতুন নাম **`proxy.ts`**, যেটা একটা `proxy` function (বা default export) export করে। এটা default-ভাবে routing-এর আগে **Node.js runtime**-এ চলে, আর `config`-এর `matcher` ঠিক করে এটা কোথায় চলবে — matcher-এর value অবশ্যই static constant হতে হবে।

            আমার proxy শুধু একটা **optimistic check** করে: session cookie decrypt/verify করে (কোনো database call না) আর সেই অনুযায়ী redirect করে। `from` parameter login-এর পরের জন্য আসল গন্তব্য মনে রাখে।

            Proxy-তে যা করা উচিত না:
            - **চূড়ান্ত authorization** — এটা দ্রুত প্রথম ছাঁকনি, security boundary না। Server Action হলো page route-এ POST, আর matcher বদলালে চুপচাপ বাদ পড়তে পারে, তাই প্রতিটা Server Component, Server Action আর Route Handler-কে নিজেই access যাচাই করতে হবে (একটা data-access layer)।
            - Database query বা বড় fetch-এর মতো **ধীর কাজ** — proxy প্রতিটা matched request-এ চলে, prefetch-সহ, আর সব জায়গায় latency বাড়ায়।
            - Invocation-গুলোর মধ্যে **shared global/module state**-এর উপর নির্ভর করা।
        """,
        ex_en=r"""
            - **Open-redirect risk:** the login page must only follow `from` values that are relative paths (start with `/` but not `//`); otherwise attackers can craft `?from=https://evil.example`.
            - **Prefix check:** `pathname.startsWith('/dashboard')` alone would also match `/dashboard-promo`; checking `=== p || startsWith(p + '/')` avoids that.
            - **Runtime:** proxy uses Node.js by default and the `runtime` option isn't allowed in proxy files. `middleware.ts` still exists only for Edge-runtime use cases and is deprecated; migrate with `npx @next/codemod@canary middleware-to-proxy .`.
            - **Testing:** `unstable_doesProxyMatch` from `next/experimental/testing/server` can unit-test the matcher.
        """,
        ex_bn=r"""
            - **Open-redirect ঝুঁকি:** login page-কে শুধু relative path-এর `from` value (`/` দিয়ে শুরু, কিন্তু `//` না) মানতে হবে; নইলে attacker `?from=https://evil.example` বানাতে পারে।
            - **Prefix check:** শুধু `pathname.startsWith('/dashboard')` দিলে `/dashboard-promo`-ও মিলে যাবে; `=== p || startsWith(p + '/')` check করলে এটা এড়ানো যায়।
            - **Runtime:** proxy default-ভাবে Node.js ব্যবহার করে, আর proxy file-এ `runtime` option দেওয়া যায় না। `middleware.ts` এখনো আছে শুধু Edge-runtime-এর ক্ষেত্রে, আর এটা deprecated; `npx @next/codemod@canary middleware-to-proxy .` দিয়ে migrate করো।
            - **Testing:** `next/experimental/testing/server` থেকে `unstable_doesProxyMatch` দিয়ে matcher unit-test করা যায়।
        """,
        tip_en=r"""Say "proxy.ts replaced middleware.ts in v16" up front, write the code, then spend real time on what proxy must NOT do — interviewers use this question to check you don't treat it as your security layer.""",
        tip_bn=r"""শুরুতেই বলো "v16-এ proxy.ts, middleware.ts-কে replace করেছে", code লেখো, তারপর proxy কী করবে *না* সেটায় ভালো সময় দাও — interviewer এই প্রশ্ন দিয়ে যাচাই করে তুমি একে security layer ভাবো কি না।""",
        mist_en=r"""Naming the file `middleware.ts` in a new v16 project, querying the database in proxy on every request, or forgetting the matcher so static assets get redirected to the login page.""",
        mist_bn=r"""নতুন v16 project-এ file-এর নাম `middleware.ts` রাখা, প্রতিটা request-এ proxy-তে database query করা, অথবা matcher ভুলে যাওয়া — ফলে static asset-ও login page-এ redirect হয়।""",
        code=r"""
            // proxy.ts — project root (next to app/)
            import { NextResponse, type NextRequest } from 'next/server';
            import { decryptSession } from '@/lib/session'; // verifies a signed/encrypted cookie, no DB call

            const PROTECTED = ['/dashboard'];
            const AUTH_PAGES = ['/login', '/signup'];

            export async function proxy(request: NextRequest) {
              const { pathname, search } = request.nextUrl;
              const token = request.cookies.get('session')?.value;
              const session = token ? await decryptSession(token) : null;
              const isSignedIn = Boolean(session?.userId);

              const isProtected = PROTECTED.some((p) => pathname === p || pathname.startsWith(`${p}/`));
              if (isProtected && !isSignedIn) {
                const loginUrl = new URL('/login', request.url);
                loginUrl.searchParams.set('from', pathname + search);
                return NextResponse.redirect(loginUrl);
              }

              if (AUTH_PAGES.includes(pathname) && isSignedIn) {
                return NextResponse.redirect(new URL('/dashboard', request.url));
              }

              return NextResponse.next();
            }

            export const config = {
              matcher: [
                '/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:png|jpg|jpeg|gif|svg|webp|avif)$).*)',
              ],
            };
        """,
        lang="typescript",
        time="O(1) per request (one cookie decryption)", space="O(1)",
        follow=[
            ("How would you safely validate the `from` parameter on the login page?", "Login page-এ `from` parameter নিরাপদে কীভাবে validate করবে?"),
            ("Why is a check in `proxy.ts` not enough to protect a Server Action?", "Server Action সুরক্ষিত রাখতে `proxy.ts`-এর check কেন যথেষ্ট না?"),
        ],
        related=["next-023"],
        refs=[N_PROXY, N_AUTH, N_DATA_SECURITY],
    ),
    # ------------------------------------------------------------------ next-026
    Q(
        id="next-026", sub="Partial Prerendering", diff="hard", type="mcq",
        prio="medium", market="both", mins=4,
        tags=["cache-components", "ppr", "suspense", "prerendering", "runtime-data"],
        ver="Next.js 16.4 (Cache Components enabled)", vs=True, status="stable",
        q_en=r"""
            With `cacheComponents: true`, this page (no `loading.tsx`, no `generateStaticParams`) shows an error in `next dev` and fails `next build`. What is the cause?
        """,
        q_bn=r"""
            `cacheComponents: true` থাকা অবস্থায় এই page (কোনো `loading.tsx` বা `generateStaticParams` নেই) `next dev`-এ error দেখায় আর `next build` fail করে। কারণ কী?
        """,
        code=r"""
            // app/account/page.tsx
            import { cookies } from 'next/headers';

            export default async function AccountPage() {
              const session = (await cookies()).get('session')?.value;
              const orders = await getOrders(session); // uncached database query

              return (
                <main>
                  <h1>Your account</h1>
                  <OrderList orders={orders} />
                </main>
              );
            }
        """,
        lang="tsx",
        options=[
            ("Runtime data (`cookies()`) and an uncached query are accessed outside any `<Suspense>` boundary, so Next.js can't produce a static shell for the route", "Runtime data (`cookies()`) আর একটা uncached query কোনো `<Suspense>` boundary-র বাইরে access করা হয়েছে, তাই Next.js route-টার জন্য static shell তৈরি করতে পারে না"),
            ("`cookies()` is synchronous in Next.js 16, so `await cookies()` throws", "Next.js 16-এ `cookies()` synchronous, তাই `await cookies()` throw করে"),
            ("With Cache Components every page must start with `'use cache'`", "Cache Components থাকলে প্রতিটা page `'use cache'` দিয়ে শুরু করতে হয়"),
            ("Pages that read cookies must export `const dynamic = 'force-dynamic'`", "যে page cookie পড়ে, তাকে `const dynamic = 'force-dynamic'` export করতে হয়"),
        ],
        correct=0,
        a_en=r"""With Cache Components, anything that depends on the request (`cookies()`, `headers()`, `searchParams`, uncached I/O) must be either cached or placed behind a `<Suspense>` boundary. Here the whole page awaits it at the top, so there's nothing to prerender — Next.js reports "Uncached data was accessed outside of `<Suspense>`".""",
        a_bn=r"""Cache Components থাকলে request-এর উপর নির্ভরশীল সবকিছু (`cookies()`, `headers()`, `searchParams`, uncached I/O) হয় cache করতে হবে, নয়তো একটা `<Suspense>` boundary-র পেছনে রাখতে হবে। এখানে পুরো page শুরুতেই এটা await করে, তাই prerender করার মতো কিছুই থাকে না — Next.js জানায় "Uncached data was accessed outside of `<Suspense>`"।""",
        ex_en=r"""
            The most tempting wrong answer is `dynamic = 'force-dynamic'` — that's how you opted out in the **previous model**. With Cache Components enabled, the `dynamic`, `revalidate` and `fetchCache` segment options aren't used; instead you describe intent in the component tree.

            Fixes:
            - Keep `<h1>` static and move the cookie read + query into an `<Orders />` component wrapped in `<Suspense fallback={<OrdersSkeleton />}>` — the shell (heading + fallback) is prerendered and orders stream per request.
            - Or add `loading.tsx` if the whole page depends on the request.
            - Cache only what is shareable: read the cookie *outside* a `'use cache'` scope and pass the value in as an argument if per-user caching makes sense.

            `await cookies()` is correct — request APIs are async-only in Next.js 16 — and `'use cache'` is opt-in, not required. If the error only appears in CI, `next build --debug-prerender` shows the exact component.
        """,
        ex_bn=r"""
            সবচেয়ে লোভনীয় ভুল উত্তর হলো `dynamic = 'force-dynamic'` — **আগের model**-এ এভাবেই opt out করা হতো। Cache Components চালু থাকলে `dynamic`, `revalidate` আর `fetchCache` segment option ব্যবহার হয় না; এর বদলে component tree-তেই উদ্দেশ্য বুঝিয়ে দিতে হয়।

            সমাধান:
            - `<h1>` static রাখো আর cookie পড়া + query একটা `<Orders />` component-এ সরাও, যেটা `<Suspense fallback={<OrdersSkeleton />}>`-এ wrap করা — shell (heading + fallback) prerender হয় আর order প্রতি request-এ stream হয়।
            - অথবা পুরো page যদি request-এর উপর নির্ভর করে, `loading.tsx` যোগ করো।
            - শুধু share করা যায় এমন জিনিস cache করো: per-user caching অর্থপূর্ণ হলে `'use cache'` scope-এর *বাইরে* cookie পড়ো আর value argument হিসেবে পাঠাও।

            `await cookies()` সঠিক — Next.js 16-এ request API শুধু async — আর `'use cache'` ঐচ্ছিক, বাধ্যতামূলক না। Error শুধু CI-তে দেখা দিলে `next build --debug-prerender` ঠিক কোন component তা দেখায়।
        """,
        tip_en=r"""Explain the rule behind the error ("every route must produce a static shell; request data needs a Suspense boundary") rather than only the fix. Calling out `force-dynamic` as the previous model shows you won't mix the two models.""",
        tip_bn=r"""শুধু সমাধান না, error-এর পেছনের নিয়মটা ব্যাখ্যা করো ("প্রতিটা route-কে static shell তৈরি করতে হবে; request data-র জন্য Suspense boundary লাগে")। `force-dynamic`-কে আগের model বললে বোঝা যায় তুমি দুই model গুলিয়ে ফেলবে না।""",
        extra=[dict(lang="tsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            // app/account/page.tsx
            import { Suspense } from 'react';
            import { cookies } from 'next/headers';

            export default function AccountPage() {
              return (
                <main>
                  <h1>Your account</h1>                          {/* static shell */}
                  <Suspense fallback={<OrdersSkeleton />}>
                    <Orders />                                  {/* streams per request */}
                  </Suspense>
                </main>
              );
            }

            async function Orders() {
              const session = (await cookies()).get('session')?.value;
              const orders = await getOrders(session);
              return <OrderList orders={orders} />;
            }
        """)],
        related=["next-014", "next-016"],
        refs=[N_BLOCKING, N_CACHING, N_SEGMENT_CONFIG],
    ),
]

if __name__ == "__main__":
    save("nextjs", "b3", QUESTIONS)
