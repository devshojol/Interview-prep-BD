# Next.js — batch 2 (next-005..007, 014..016, 024, 031)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_DYNAMIC = ("Next.js Docs — Dynamic Route Segments", "https://nextjs.org/docs/app/api-reference/file-conventions/dynamic-routes")
N_PAGE = ("Next.js Docs — page.js", "https://nextjs.org/docs/app/api-reference/file-conventions/page")
N_UPGRADE16 = ("Next.js Docs — Upgrading to Version 16", "https://nextjs.org/docs/app/guides/upgrading/version-16")
N_ERROR = ("Next.js Docs — error.js", "https://nextjs.org/docs/app/api-reference/file-conventions/error")
N_ERROR_HANDLING = ("Next.js Docs — Error Handling", "https://nextjs.org/docs/app/getting-started/error-handling")
N_LOADING = ("Next.js Docs — loading.js", "https://nextjs.org/docs/app/api-reference/file-conventions/loading")
N_ENV = ("Next.js Docs — Environment Variables", "https://nextjs.org/docs/app/guides/environment-variables")
N_SELF_HOST = ("Next.js Docs — Self-hosting", "https://nextjs.org/docs/app/guides/self-hosting")
N_CACHING = ("Next.js Docs — Caching (Cache Components)", "https://nextjs.org/docs/app/getting-started/caching")
N_USE_CACHE = ("Next.js Docs — 'use cache'", "https://nextjs.org/docs/app/api-reference/directives/use-cache")
N_PREV_MODEL = ("Next.js Docs — Caching and Revalidating (Previous Model)", "https://nextjs.org/docs/app/guides/caching-without-cache-components")
N_UPDATETAG = ("Next.js Docs — updateTag", "https://nextjs.org/docs/app/api-reference/functions/updateTag")
N_REVALIDATETAG = ("Next.js Docs — revalidateTag", "https://nextjs.org/docs/app/api-reference/functions/revalidateTag")
N_REFRESH = ("Next.js Docs — refresh", "https://nextjs.org/docs/app/api-reference/functions/refresh")
N_STREAMING = ("Next.js Docs — Streaming", "https://nextjs.org/docs/app/guides/streaming")
N_FETCHING = ("Next.js Docs — Fetching Data", "https://nextjs.org/docs/app/getting-started/fetching-data")
N_CACHE_HANDLERS = ("Next.js Docs — cacheHandlers", "https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheHandlers")
N_CDN = ("Next.js Docs — CDN Caching", "https://nextjs.org/docs/app/guides/cdn-caching")
N_MIGRATE_APP = ("Next.js Docs — Migrating from the Pages Router to the App Router", "https://nextjs.org/docs/app/guides/migrating/app-router-migration")
N_PROXY = ("Next.js Docs — proxy.js", "https://nextjs.org/docs/app/api-reference/file-conventions/proxy")

QUESTIONS = [
    # ------------------------------------------------------------------ next-005
    Q(
        id="next-005", sub="Dynamic Routes", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["dynamic-routes", "params", "async-request-apis", "nextjs-16"],
        ver="Next.js 16.4 (App Router)", vs=True, status="stable",
        q_en=r"""In Next.js 16, how do you read the `slug` inside `app/blog/[slug]/page.tsx`?""",
        q_bn=r"""Next.js 16-এ `app/blog/[slug]/page.tsx`-এর ভেতরে `slug` কীভাবে পড়বে?""",
        options=[
            ("`export default function Page({ params }) { const slug = params.slug; }`", "`export default function Page({ params }) { const slug = params.slug; }`"),
            ("`export default async function Page({ params }) { const { slug } = await params; }`", "`export default async function Page({ params }) { const { slug } = await params; }`"),
            ("`const { slug } = useRouter().query;` using `next/router`", "`next/router` থেকে `const { slug } = useRouter().query;`"),
            ("Export `getServerSideProps` and read `context.params.slug`", "`getServerSideProps` export করে `context.params.slug` পড়া"),
        ],
        correct=1,
        a_en=r"""`params` is a **Promise** in the App Router, so the page is `async` and does `const { slug } = await params`. The same applies to `searchParams`, `cookies()`, `headers()` and `draftMode()` — all request APIs are async-only in Next.js 16.""",
        a_bn=r"""App Router-এ `params` একটা **Promise**, তাই page-টা `async` হয় আর `const { slug } = await params` করে। `searchParams`, `cookies()`, `headers()` আর `draftMode()`-এর ক্ষেত্রেও একই কথা — Next.js 16-এ সব request API শুধু async।""",
        ex_en=r"""
            The tempting answer is the synchronous `params.slug`. That's how Next.js 13/14 worked; Next.js 15 made these APIs async but kept temporary synchronous access with warnings, and **Next.js 16 removed synchronous access**. The `next-async-request-api` codemod migrates most code.

            Options C and D are **Pages Router** APIs: `next/router` and `getServerSideProps` don't work in `app/`. In a Client Component you can use `useParams()` from `next/navigation`, or unwrap a passed-in promise with React's `use()`.

            Why a Promise? It lets Next.js start rendering (and prerender static parts) before request-specific values are known. With Cache Components, awaiting `params` makes that part request-time unless you provide `generateStaticParams`, so you either wrap the awaiting component in `<Suspense>` or prerender known values.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো synchronous `params.slug`। Next.js 13/14 এভাবেই কাজ করত; Next.js 15 এই API-গুলো async করে, তবে warning-সহ সাময়িকভাবে synchronous access রেখেছিল, আর **Next.js 16 synchronous access সরিয়ে দিয়েছে**। `next-async-request-api` codemod বেশিরভাগ code migrate করে দেয়।

            Option C আর D হলো **Pages Router**-এর API: `next/router` আর `getServerSideProps` `app/`-এর ভেতরে কাজ করে না। Client Component-এ `next/navigation` থেকে `useParams()` ব্যবহার করা যায়, অথবা পাঠানো promise React-এর `use()` দিয়ে unwrap করা যায়।

            Promise কেন? এতে request-নির্দিষ্ট value জানার আগেই Next.js rendering শুরু করতে (আর static অংশ prerender করতে) পারে। Cache Components থাকলে `params` await করলে সেই অংশ request-time-এ চলে যায়, যদি না তুমি `generateStaticParams` দাও — তাই হয় await করা component-কে `<Suspense>`-এ wrap করো, নয়তো জানা value-গুলো prerender করো।
        """,
        tip_en=r"""Say "request APIs are async in Next.js 16" and list them (`params`, `searchParams`, `cookies()`, `headers()`, `draftMode()`). Knowing *why* they became promises (prerendering/streaming) is a strong bonus.""",
        tip_bn=r"""বলো "Next.js 16-এ request API async" আর সেগুলোর তালিকা দাও (`params`, `searchParams`, `cookies()`, `headers()`, `draftMode()`)। এগুলো *কেন* promise হলো (prerendering/streaming) সেটা জানা থাকলে বড় বাড়তি নম্বর।""",
        refs=[N_DYNAMIC, N_PAGE, N_UPGRADE16],
    ),
    # ------------------------------------------------------------------ next-006
    Q(
        id="next-006", sub="Loading and Error Handling", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["loading", "error-boundary", "not-found", "global-error", "file-conventions"],
        ver="Next.js 16.4 (App Router; error `retry` prop stable since 16.3)", vs=True, status="stable",
        q_en=r"""What do `loading.tsx`, `error.tsx`, `not-found.tsx` and `global-error.tsx` do in the App Router?""",
        q_bn=r"""App Router-এ `loading.tsx`, `error.tsx`, `not-found.tsx` আর `global-error.tsx` কী কাজ করে?""",
        a_en=r"""
            They're special files that add React boundaries around a route segment:

            - **`loading.tsx`** wraps the segment's page in a `<Suspense>` boundary. Its UI (a skeleton) shows instantly while the page's data loads and streams in, and navigation stays responsive.
            - **`error.tsx`** wraps the segment in an **error boundary**. It must be a Client Component and receives `error` and `retry` — `retry()` re-fetches and re-renders the segment (the older `reset()` clears the error state and re-renders *without* re-fetching).
            - **`not-found.tsx`** renders when you call `notFound()` from `next/navigation` (e.g. a product id doesn't exist) and, at the root level, for any unmatched URL.
            - **`global-error.tsx`** catches errors in the root layout itself. It replaces the root layout, so it must render its own `<html>` and `<body>`.
        """,
        a_bn=r"""
            এগুলো বিশেষ file, যেগুলো একটা route segment-এর চারপাশে React boundary যোগ করে:

            - **`loading.tsx`** segment-এর page-কে একটা `<Suspense>` boundary-তে wrap করে। Page-এর data load হয়ে stream হওয়ার সময় এর UI (একটা skeleton) সাথে সাথে দেখায়, আর navigation responsive থাকে।
            - **`error.tsx`** segment-কে একটা **error boundary**-তে wrap করে। এটা অবশ্যই Client Component হতে হবে, আর এটা `error` ও `retry` পায় — `retry()` segment আবার fetch করে re-render করে (পুরনো `reset()` error state মুছে আবার fetch *না করেই* re-render করে)।
            - **`not-found.tsx`** render হয় যখন তুমি `next/navigation` থেকে `notFound()` call করো (যেমন product id নেই), আর root স্তরে থাকলে যেকোনো না মেলা URL-এর জন্যও।
            - **`global-error.tsx`** root layout-এর নিজের error ধরে। এটা root layout-কে replace করে, তাই একে নিজের `<html>` আর `<body>` render করতে হয়।
        """,
        ex_en=r"""
            **Nesting order inside a segment:** `layout` → `template` → `error` → `loading` → `not-found` → `page`. Because the error boundary sits *inside* the layout, an error thrown by a segment's own `layout.tsx` is handled by the parent segment's `error.tsx`.

            **Production behaviour:** errors from Server Components reach `error.tsx` with a generic message and an `error.digest` hash, so secrets don't leak; use the digest to find the full error in server logs.

            **Expected vs unexpected errors:** don't throw for validation problems — return them as values (e.g. from a Server Action). Use error boundaries for unexpected failures, and `notFound()` for missing resources.
        """,
        ex_bn=r"""
            **একটা segment-এর ভেতরে nesting-এর ক্রম:** `layout` → `template` → `error` → `loading` → `not-found` → `page`। যেহেতু error boundary layout-এর *ভেতরে* থাকে, তাই কোনো segment-এর নিজের `layout.tsx`-এ throw হওয়া error সামলায় parent segment-এর `error.tsx`।

            **Production-এ আচরণ:** Server Component-এর error `error.tsx`-এ পৌঁছায় একটা generic message আর একটা `error.digest` hash-সহ, যাতে secret leak না হয়; server log-এ পুরো error খুঁজতে digest ব্যবহার করো।

            **প্রত্যাশিত বনাম অপ্রত্যাশিত error:** validation সমস্যার জন্য throw করো না — value হিসেবে return করো (যেমন Server Action থেকে)। অপ্রত্যাশিত failure-এর জন্য error boundary, আর না থাকা resource-এর জন্য `notFound()` ব্যবহার করো।
        """,
        tip_en=r"""Describe each file in one line as "which React boundary it creates". Mentioning the nesting order (and the layout-error consequence) shows you understand how they compose.""",
        tip_bn=r"""প্রতিটা file এক লাইনে বর্ণনা করো — "এটা কোন React boundary তৈরি করে"। Nesting-এর ক্রম (আর layout-error-এর ফলাফল) উল্লেখ করলে বোঝা যায় তুমি এগুলো কীভাবে একসাথে কাজ করে তা বোঝো।""",
        mist_en=r"""Writing `error.tsx` as a Server Component (it must be `'use client'`), or forgetting `<html>`/`<body>` in `global-error.tsx`.""",
        mist_bn=r"""`error.tsx`-কে Server Component হিসেবে লেখা (এটা অবশ্যই `'use client'` হতে হবে), অথবা `global-error.tsx`-এ `<html>`/`<body>` ভুলে যাওয়া।""",
        code=r"""
            // app/products/[id]/loading.tsx
            export default function Loading() {
              return <ProductSkeleton />;
            }

            // app/products/[id]/error.tsx
            'use client';

            export default function ProductError({
              error,
              retry,
            }: {
              error: Error & { digest?: string };
              retry: () => void;
            }) {
              return (
                <div role="alert">
                  <p>We couldn't load this product.</p>
                  <button onClick={() => retry()}>Try again</button>
                </div>
              );
            }

            // app/products/[id]/page.tsx
            import { notFound } from 'next/navigation';

            export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
              const { id } = await params;
              const product = await getProduct(id);
              if (!product) notFound(); // renders the nearest not-found.tsx
              return <ProductView product={product} />;
            }
        """,
        lang="tsx",
        follow=[
            ("Why does an error in `app/dashboard/layout.tsx` not show `app/dashboard/error.tsx`?", "`app/dashboard/layout.tsx`-এ error হলে কেন `app/dashboard/error.tsx` দেখায় না?"),
            ("What's the difference between `retry()` and `reset()` in `error.tsx`?", "`error.tsx`-এ `retry()` আর `reset()`-এর পার্থক্য কী?"),
        ],
        related=["next-003"],
        refs=[N_ERROR, N_LOADING, N_ERROR_HANDLING],
    ),
    # ------------------------------------------------------------------ next-007
    Q(
        id="next-007", sub="Environment Variables", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["environment-variables", "next-public", "security", "build-time"],
        ver="Next.js 16.4", vs=False, status="stable",
        q_en=r"""`process.env.API_URL` works in a Server Component but is `undefined` inside a Client Component in production. What is the most likely reason?""",
        q_bn=r"""`process.env.API_URL` একটা Server Component-এ কাজ করে, কিন্তু production-এ একটা Client Component-এর ভেতরে `undefined`। সবচেয়ে সম্ভাব্য কারণ কী?""",
        options=[
            ("Only variables prefixed with `NEXT_PUBLIC_` are exposed to the browser, and they are inlined into the JavaScript bundle at build time", "শুধু `NEXT_PUBLIC_` prefix-যুক্ত variable browser-এ যায়, আর সেগুলো build time-এ JavaScript bundle-এ বসিয়ে দেওয়া হয়"),
            ("`.env` files are ignored in production; variables must be set in `next.config.js` instead", "Production-এ `.env` file ignore হয়; variable-গুলো `next.config.js`-এ set করতে হয়"),
            ("Client Components must read variables through a `useEnv()` hook", "Client Component-কে `useEnv()` hook দিয়ে variable পড়তে হয়"),
            ("The variable must be defined in `.env.local` instead of `.env`", "Variable-টা `.env`-এর বদলে `.env.local`-এ define করতে হবে"),
        ],
        correct=0,
        a_en=r"""By default environment variables are **server-only**. To use one in browser code it must be named `NEXT_PUBLIC_API_URL`; during `next build` Next.js replaces each `process.env.NEXT_PUBLIC_*` reference with the literal value.""",
        a_bn=r"""Default-ভাবে environment variable **শুধু server-এর জন্য**। Browser code-এ ব্যবহার করতে হলে নাম হতে হবে `NEXT_PUBLIC_API_URL`; `next build`-এর সময় Next.js প্রতিটা `process.env.NEXT_PUBLIC_*` reference আসল value দিয়ে বদলে দেয়।""",
        ex_en=r"""
            The server-only default is a security feature: database URLs and API secrets never end up in the bundle. The flip side is that **anything with `NEXT_PUBLIC_` is public** — never put secrets there.

            Two production gotchas:
            - Because public variables are **inlined at build time**, changing them in the container's runtime environment does nothing — you must rebuild. For one Docker image promoted across staging/production, read config on the server at request time and pass it to Client Components as props.
            - Inlining only works for direct references like `process.env.NEXT_PUBLIC_API_URL`; dynamic lookups such as `process.env[name]` aren't replaced.

            Option D is tempting but wrong: `.env.local` only changes load priority (and is usually git-ignored); it doesn't make a variable public. Runtime config (`publicRuntimeConfig`) was removed in Next.js 16.
        """,
        ex_bn=r"""
            Server-only default-টা একটা security feature: database URL আর API secret কখনো bundle-এ যায় না। উল্টো দিক হলো **`NEXT_PUBLIC_` দেওয়া সবকিছুই public** — সেখানে কখনো secret রাখবে না।

            Production-এর দুটো gotcha:
            - Public variable **build time-এ বসিয়ে দেওয়া হয়**, তাই container-এর runtime environment-এ বদলালে কিছুই হয় না — আবার build করতে হয়। একটা Docker image staging/production-এ promote করতে চাইলে request time-এ server-এ config পড়ো আর props হিসেবে Client Component-এ পাঠাও।
            - Inlining শুধু `process.env.NEXT_PUBLIC_API_URL`-এর মতো সরাসরি reference-এ কাজ করে; `process.env[name]`-এর মতো dynamic lookup বদলানো হয় না।

            Option D লোভনীয় কিন্তু ভুল: `.env.local` শুধু load priority বদলায় (আর সাধারণত git-ignore করা থাকে); variable-কে public করে না। Runtime config (`publicRuntimeConfig`) Next.js 16-এ সরিয়ে ফেলা হয়েছে।
        """,
        tip_en=r"""Answer with the rule, then immediately add the two consequences: "public means public" (no secrets) and "inlined at build time" (rebuild to change). That's exactly the production knowledge interviewers probe.""",
        tip_bn=r"""নিয়মটা বলো, তারপর সাথে সাথে দুটো ফলাফল যোগ করো: "public মানে public" (secret না) আর "build time-এ বসানো" (বদলাতে হলে rebuild)। Interviewer ঠিক এই production জ্ঞানটাই যাচাই করে।""",
        refs=[N_ENV, N_SELF_HOST],
    ),
    # ------------------------------------------------------------------ next-014
    Q(
        id="next-014", sub="Caching with Cache Components", diff="medium", type="conceptual",
        prio="high", market="both", mins=7,
        tags=["cache-components", "use-cache", "cachelife", "cachetag", "caching"],
        ver="Next.js 16.4 (Cache Components; default for new apps)", vs=True, status="stable",
        q_en=r"""What are Cache Components in Next.js 16? Explain `'use cache'`, `cacheLife()` and `cacheTag()`, and how this differs from the previous caching model.""",
        q_bn=r"""Next.js 16-এ Cache Components কী? `'use cache'`, `cacheLife()` আর `cacheTag()` ব্যাখ্যা করো, আর আগের caching model থেকে এটা কীভাবে আলাদা।""",
        a_en=r"""
            Cache Components (`cacheComponents: true` in `next.config`) is the current caching and rendering model. New `create-next-app` projects enable it by default in 16.4, and it becomes the default in Next.js 17. The core idea: **everything is dynamic by default, and caching is explicit**.

            - **`'use cache'`** at the top of an async function, component or file caches its return value. The cache key includes the build ID, the function's identity, its serialisable arguments and any closed-over values.
            - **`cacheLife('hours')`** sets how long the entry is fresh (profiles like `'minutes'`, `'hours'`, `'days'`, `'max'`, or a custom `{ stale, revalidate, expire }`). Without it, the `default` profile applies.
            - **`cacheTag('products')`** labels the entry so you can invalidate it on demand with `updateTag()` (Server Actions) or `revalidateTag(tag, 'max')`.

            Data that isn't cached — `cookies()`, `headers()`, uncached fetches — must sit inside a `<Suspense>` boundary. At build time Next.js prerenders a **static shell** (static + cached parts + fallbacks) and streams the dynamic parts per request: Partial Prerendering.

            In the **previous model** (still used when the flag is off) caching was configured per route or per fetch: `export const revalidate = 60`, `export const dynamic = 'force-dynamic'`, `fetch(url, { next: { revalidate, tags } })` and `unstable_cache`. Since Next.js 15, `fetch` isn't cached by default there either.
        """,
        a_bn=r"""
            Cache Components (`next.config`-এ `cacheComponents: true`) হলো বর্তমান caching আর rendering model। 16.4-এ নতুন `create-next-app` project-এ এটা default-ভাবে চালু থাকে, আর Next.js 17-এ এটাই default হবে। মূল ধারণা: **default-ভাবে সবকিছু dynamic, আর caching স্পষ্টভাবে বলে দিতে হয়**।

            - Async function, component বা file-এর শুরুতে **`'use cache'`** দিলে তার return value cache হয়। Cache key-তে থাকে build ID, function-এর identity, তার serialisable argument আর closure-এ ধরা value।
            - **`cacheLife('hours')`** ঠিক করে entry কতক্ষণ fresh থাকবে (`'minutes'`, `'hours'`, `'days'`, `'max'`-এর মতো profile, অথবা custom `{ stale, revalidate, expire }`)। না দিলে `default` profile প্রযোজ্য হয়।
            - **`cacheTag('products')`** entry-তে একটা label দেয়, যাতে `updateTag()` (Server Action) বা `revalidateTag(tag, 'max')` দিয়ে দরকারমতো invalidate করা যায়।

            যে data cache হয় না — `cookies()`, `headers()`, uncached fetch — সেগুলো অবশ্যই একটা `<Suspense>` boundary-র ভেতরে থাকতে হবে। Build time-এ Next.js একটা **static shell** prerender করে (static + cached অংশ + fallback), আর dynamic অংশ প্রতি request-এ stream করে: এটাই Partial Prerendering।

            **আগের model**-এ (flag বন্ধ থাকলে এখনো এটাই চলে) caching route বা fetch অনুযায়ী configure করা হতো: `export const revalidate = 60`, `export const dynamic = 'force-dynamic'`, `fetch(url, { next: { revalidate, tags } })` আর `unstable_cache`। Next.js 15 থেকে সেখানেও `fetch` default-ভাবে cache হয় না।
        """,
        ex_en=r"""
            - **No request data inside a cache scope:** calling `cookies()`/`headers()` inside `'use cache'` is an error. Read them outside and pass the *values* as arguments (they become part of the key). `'use cache: private'` exists for rare cases that must read runtime data directly; `'use cache: remote'` stores entries in a shared cache handler.
            - **Runtime storage:** by default entries live in an in-memory LRU per server instance. On serverless they often don't survive between requests; self-hosted multi-instance setups need a shared `cacheHandlers` implementation.
            - **Client side:** cached content is also kept in the browser router for the profile's `stale` time (minimum 30 seconds).
            - **Segment config:** with Cache Components enabled, `dynamic`, `revalidate` and `fetchCache` route segment options are no longer used — caching lives next to the data.
            - **Debugging:** `NEXT_PRIVATE_DEBUG_CACHE=1` logs cache activity.
        """,
        ex_bn=r"""
            - **Cache scope-এর ভেতরে request data না:** `'use cache'`-এর ভেতরে `cookies()`/`headers()` call করা error। এগুলো বাইরে পড়ো আর *value* argument হিসেবে পাঠাও (তখন এগুলো key-এর অংশ হয়)। যে বিরল ক্ষেত্রে সরাসরি runtime data পড়তেই হবে, তার জন্য `'use cache: private'` আছে; আর `'use cache: remote'` entry একটা shared cache handler-এ রাখে।
            - **Runtime storage:** default-ভাবে entry থাকে প্রতিটা server instance-এর in-memory LRU-তে। Serverless-এ প্রায়ই এগুলো এক request থেকে আরেক request পর্যন্ত টেকে না; self-hosted multi-instance setup-এ shared `cacheHandlers` implementation লাগে।
            - **Client side:** cached content profile-এর `stale` সময় পর্যন্ত browser router-এও থাকে (ন্যূনতম ৩০ সেকেন্ড)।
            - **Segment config:** Cache Components চালু থাকলে `dynamic`, `revalidate` আর `fetchCache` route segment option আর ব্যবহার হয় না — caching থাকে data-র পাশেই।
            - **Debugging:** `NEXT_PRIVATE_DEBUG_CACHE=1` cache-এর কার্যকলাপ log করে।
        """,
        tip_en=r"""Lead with the philosophy shift ("dynamic by default, cache explicitly"), then the three APIs, then the Suspense requirement. Clearly labelling `revalidate`/`force-dynamic` as the previous model shows you won't mix versions in a real codebase.""",
        tip_bn=r"""দর্শনের পরিবর্তন দিয়ে শুরু করো ("default-ভাবে dynamic, cache স্পষ্টভাবে"), তারপর তিনটা API, তারপর Suspense-এর শর্ত। `revalidate`/`force-dynamic`-কে স্পষ্টভাবে আগের model বললে বোঝা যায় তুমি আসল codebase-এ version গুলিয়ে ফেলবে না।""",
        mist_en=r"""Assuming `fetch` is cached by default (that was Next.js 14), reading `cookies()` inside a `'use cache'` function, or adding `export const revalidate` to a Cache Components app.""",
        mist_bn=r"""ধরে নেওয়া যে `fetch` default-ভাবে cache হয় (সেটা ছিল Next.js 14-এ), `'use cache'` function-এর ভেতরে `cookies()` পড়া, অথবা Cache Components app-এ `export const revalidate` যোগ করা।""",
        code=r"""
            // next.config.ts
            import type { NextConfig } from 'next';
            const nextConfig: NextConfig = { cacheComponents: true, partialPrefetching: true };
            export default nextConfig;

            // lib/products.ts
            import { cacheLife, cacheTag } from 'next/cache';

            export async function getFeaturedProducts() {
              'use cache';
              cacheLife('hours');
              cacheTag('products');
              return db.product.findMany({ where: { featured: true }, take: 12 });
            }

            // app/page.tsx
            import { Suspense } from 'react';
            import { cookies } from 'next/headers';

            export default async function HomePage() {
              const products = await getFeaturedProducts(); // cached → part of the static shell
              return (
                <>
                  <ProductGrid products={products} />
                  <Suspense fallback={<p>Loading your cart…</p>}>
                    <CartSummary /> {/* runtime data → streams per request */}
                  </Suspense>
                </>
              );
            }

            async function CartSummary() {
              const cartId = (await cookies()).get('cartId')?.value;
              const cart = await getCart(cartId); // uncached, per user
              return <p>{cart.items.length} items in your cart</p>;
            }
        """,
        lang="tsx",
        follow=[
            ("Why can't a `'use cache'` function call `cookies()`, and what do you do instead?", "`'use cache'` function কেন `cookies()` call করতে পারে না, আর এর বদলে কী করো?"),
            ("How would you translate `export const revalidate = 3600` into Cache Components?", "`export const revalidate = 3600`-কে Cache Components-এ কীভাবে রূপান্তর করবে?"),
        ],
        related=["next-004"],
        refs=[N_CACHING, N_USE_CACHE, N_PREV_MODEL],
    ),
    # ------------------------------------------------------------------ next-015
    Q(
        id="next-015", sub="Revalidation APIs", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["updatetag", "revalidatetag", "refresh", "read-your-own-writes"],
        ver="Next.js 16.4 (Cache Components)", vs=True, status="stable",
        q_en=r"""
            A user edits their display name through a Server Action. The profile data is cached with `'use cache'` and `cacheTag('user-42')`. After the action redirects back to the profile, the user must see the new name immediately. Which call belongs in the Server Action?
        """,
        q_bn=r"""
            একজন user একটা Server Action দিয়ে নিজের display name বদলাল। Profile data `'use cache'` আর `cacheTag('user-42')` দিয়ে cache করা। Action profile-এ redirect করার পর user-কে সাথে সাথে নতুন নাম দেখতে হবে। Server Action-এ কোন call থাকা উচিত?
        """,
        options=[
            ("`revalidateTag('user-42', 'max')`", "`revalidateTag('user-42', 'max')`"),
            ("`updateTag('user-42')`", "`updateTag('user-42')`"),
            ("`refresh()`", "`refresh()`"),
            ("Nothing — `'use cache'` entries are skipped automatically after any Server Action", "কিছুই না — যেকোনো Server Action-এর পর `'use cache'` entry নিজে থেকেই skip হয়"),
        ],
        correct=1,
        a_en=r"""`updateTag('user-42')`. It can only be called in Server Actions and **expires the tag immediately**, so the next request waits for fresh data instead of serving the stale entry — designed for read-your-own-writes.""",
        a_bn=r"""`updateTag('user-42')`। এটা শুধু Server Action-এ call করা যায় আর **tag সাথে সাথে expire করে**, ফলে পরের request পুরনো entry না দেখিয়ে fresh data-র জন্য অপেক্ষা করে — read-your-own-writes-এর জন্যই এটা তৈরি।""",
        ex_en=r"""
            The tempting wrong answer is `revalidateTag('user-42', 'max')`. It marks the data stale with **stale-while-revalidate** semantics: the next request is still served the cached (old) name while fresh data loads in the background. That's ideal for content where a short delay is fine — e.g. a CMS webhook calling a Route Handler (where `updateTag` isn't allowed) — but wrong for "I just changed it".

            `refresh()` (also Server Actions only) refreshes the client router so uncached data is re-rendered; it doesn't expire tagged cache entries. Nothing invalidates `'use cache'` entries automatically.

            Version note: the single-argument `revalidateTag(tag)` is deprecated; it behaves like `{ expire: 0 }`. Use `updateTag` in Server Actions or pass a profile.
        """,
        ex_bn=r"""
            লোভনীয় ভুল উত্তর হলো `revalidateTag('user-42', 'max')`। এটা data-কে **stale-while-revalidate** নিয়মে stale চিহ্নিত করে: পরের request-এ তখনো cached (পুরনো) নাম দেখায়, আর background-এ fresh data load হয়। যেখানে সামান্য দেরি চলে সেখানে এটা আদর্শ — যেমন CMS webhook একটা Route Handler call করছে (যেখানে `updateTag` চলে না) — কিন্তু "আমি এইমাত্র বদলালাম"-এর জন্য ভুল।

            `refresh()` (এটাও শুধু Server Action-এ) client router refresh করে, যাতে uncached data আবার render হয়; tag করা cache entry expire করে না। আর কোনো কিছুই `'use cache'` entry নিজে থেকে invalidate করে না।

            Version নোট: এক argument-এর `revalidateTag(tag)` deprecated; এটা `{ expire: 0 }`-এর মতো আচরণ করে। Server Action-এ `updateTag` ব্যবহার করো, অথবা একটা profile দাও।
        """,
        tip_en=r"""Name the semantics, not just the function: "updateTag = expire now, read-your-own-writes; revalidateTag with 'max' = stale-while-revalidate". Then say where each can be called.""",
        tip_bn=r"""শুধু function-এর নাম না, semantics বলো: "updateTag = এখনই expire, read-your-own-writes; 'max'-সহ revalidateTag = stale-while-revalidate"। তারপর বলো কোনটা কোথায় call করা যায়।""",
        related=["next-014"],
        refs=[N_UPDATETAG, N_REVALIDATETAG, N_REFRESH],
    ),
    # ------------------------------------------------------------------ next-016
    Q(
        id="next-016", sub="Streaming and Suspense", diff="medium", type="scenario",
        prio="high", market="both", mins=7,
        tags=["streaming", "suspense", "waterfalls", "performance", "ppr"],
        ver="Next.js 16.4 (App Router, Cache Components)", vs=True, status="stable",
        q_en=r"""
            A product page shows nothing for about 3.5 seconds. It awaits, one after another: product details (200 ms), reviews from a third-party API (2.5 s) and recommendations (1 s). How would you make it feel fast with the App Router?
        """,
        q_bn=r"""
            একটা product page প্রায় ৩.৫ সেকেন্ড কিছুই দেখায় না। এটা একটার পর একটা await করে: product details (২০০ ms), third-party API থেকে review (২.৫ s) আর recommendation (১ s)। App Router দিয়ে এটা কীভাবে দ্রুত অনুভূত করাবে?
        """,
        a_en=r"""
            Two problems: a **waterfall** (sequential awaits add up to ~3.7 s) and **all-or-nothing rendering** (nothing is sent until the slowest call finishes).

            1. **Split the page into independent async components** — `ProductDetails`, `Reviews`, `Recommendations` — each fetching its own data. Sibling components render concurrently, so their requests run in parallel instead of in sequence.
            2. **Wrap slow parts in `<Suspense>`** with skeleton fallbacks. The server sends the page shell and product details first, then **streams** reviews and recommendations into place as they resolve.
            3. **Cache what's shareable** with `'use cache'`: product details (`cacheLife('hours')`, `cacheTag('product-<id>')`) and recommendations. Cached parts join the prerendered static shell, so they can even come from a CDN.
            4. **Isolate failures:** a slow or failing reviews API shouldn't break the page — add a timeout and an error boundary around that section.

            Result: the user sees the product almost immediately; reviews arrive later without blocking anything.
        """,
        a_bn=r"""
            দুটো সমস্যা: একটা **waterfall** (একটার পর একটা await মিলে ~৩.৭ s) আর **হয় সব, নয় কিছুই না** ধরনের rendering (সবচেয়ে ধীর call শেষ না হওয়া পর্যন্ত কিছুই পাঠানো হয় না)।

            1. **Page-কে স্বাধীন async component-এ ভাগ করো** — `ProductDetails`, `Reviews`, `Recommendations` — প্রত্যেকে নিজের data fetch করবে। পাশাপাশি থাকা component-গুলো একসাথে render হয়, তাই এদের request ক্রমানুসারে না, parallel-এ চলে।
            2. **ধীর অংশগুলো `<Suspense>`-এ wrap করো**, skeleton fallback-সহ। Server আগে page shell আর product details পাঠায়, তারপর review আর recommendation resolve হওয়ার সাথে সাথে জায়গামতো **stream** করে।
            3. **Share করা যায় এমন জিনিস cache করো** `'use cache'` দিয়ে: product details (`cacheLife('hours')`, `cacheTag('product-<id>')`) আর recommendation। Cached অংশ prerender করা static shell-এ যোগ হয়, ফলে এগুলো CDN থেকেও আসতে পারে।
            4. **Failure আলাদা রাখো:** ধীর বা fail করা review API যেন পুরো page না ভাঙে — ওই অংশে timeout আর একটা error boundary দাও।

            ফলাফল: user প্রায় সাথে সাথে product দেখে; review পরে আসে, কোনো কিছু আটকে না রেখে।
        """,
        ex_en=r"""
            **Why the page doesn't await `params` itself:** with Cache Components, awaiting runtime data (like `params` without `generateStaticParams`) outside `<Suspense>` blocks prerendering. Passing the `params` promise down and awaiting it inside each Suspense boundary keeps the shell static.

            **`loading.tsx` vs granular Suspense:** `loading.tsx` gives one fallback for the whole page — good for instant navigation feedback. Granular boundaries let fast sections appear first. Use both.

            **Infrastructure:** streaming only helps if nothing buffers the response — configure NGINX (`X-Accel-Buffering: no`) and load balancers accordingly when self-hosting.

            **SEO:** streamed content is still in the HTML response, so crawlers that read the full response see it.
        """,
        ex_bn=r"""
            **Page নিজে কেন `params` await করে না:** Cache Components থাকলে `<Suspense>`-এর বাইরে runtime data await করা (যেমন `generateStaticParams` ছাড়া `params`) prerendering আটকে দেয়। `params` promise নিচে পাঠিয়ে প্রতিটা Suspense boundary-র ভেতরে await করলে shell static থাকে।

            **`loading.tsx` বনাম আলাদা আলাদা Suspense:** `loading.tsx` পুরো page-এর জন্য একটা fallback দেয় — navigation-এ সাথে সাথে feedback-এর জন্য ভালো। আলাদা boundary দিলে দ্রুত অংশগুলো আগে দেখা যায়। দুটোই ব্যবহার করো।

            **Infrastructure:** কোনো কিছু response buffer না করলেই কেবল streaming কাজে আসে — self-host করলে NGINX (`X-Accel-Buffering: no`) আর load balancer সেভাবে configure করো।

            **SEO:** stream হওয়া content-ও HTML response-এর ভেতরেই থাকে, তাই যে crawler পুরো response পড়ে সে এটা দেখে।
        """,
        tip_en=r"""Name both problems (waterfall and blocking render) before solving them. Then explain parallel fetching, Suspense streaming and caching in that order — it shows a structured performance mindset.""",
        tip_bn=r"""সমাধানের আগে দুটো সমস্যারই নাম বলো (waterfall আর blocking render)। তারপর এই ক্রমে ব্যাখ্যা করো: parallel fetching, Suspense streaming, caching — এতে একটা গোছানো performance-চিন্তা বোঝা যায়।""",
        mist_en=r"""Only adding `loading.tsx` (the whole page still waits for the slowest call), or using `Promise.all` but keeping everything under a single boundary so reviews still block the product.""",
        mist_bn=r"""শুধু `loading.tsx` যোগ করা (পুরো page তখনো সবচেয়ে ধীর call-এর জন্য অপেক্ষা করে), অথবা `Promise.all` ব্যবহার করে সবকিছু একটাই boundary-র নিচে রাখা — ফলে review তখনো product আটকে রাখে।""",
        code=r"""
            // app/products/[id]/page.tsx
            import { Suspense } from 'react';

            type Params = Promise<{ id: string }>;

            export default function ProductPage({ params }: { params: Params }) {
              return (
                <main>
                  <Suspense fallback={<ProductSkeleton />}>
                    <ProductDetails params={params} />
                  </Suspense>
                  <Suspense fallback={<ReviewsSkeleton />}>
                    <Reviews params={params} />
                  </Suspense>
                  <Suspense fallback={<RecommendationsSkeleton />}>
                    <Recommendations params={params} />
                  </Suspense>
                </main>
              );
            }

            async function ProductDetails({ params }: { params: Params }) {
              const { id } = await params;
              const product = await getProduct(id); // 'use cache' + cacheTag(`product-${id}`)
              return <ProductView product={product} />;
            }

            async function Reviews({ params }: { params: Params }) {
              const { id } = await params;
              const reviews = await getReviews(id, { timeoutMs: 3000 }); // slow third-party API
              return <ReviewList reviews={reviews} />;
            }

            async function Recommendations({ params }: { params: Params }) {
              const { id } = await params;
              const items = await getRecommendations(id); // 'use cache' + cacheLife('hours')
              return <ProductCarousel items={items} />;
            }
        """,
        lang="tsx",
        follow=[
            ("How would you stop a failing reviews API from showing the page-level `error.tsx`?", "Review API fail করলে page-level `error.tsx` দেখানো কীভাবে আটকাবে?"),
            ("What has to be configured in NGINX for streaming to work when self-hosting?", "Self-host করার সময় streaming কাজ করাতে NGINX-এ কী configure করতে হয়?"),
        ],
        related=["next-014", "next-006"],
        refs=[N_STREAMING, N_FETCHING, N_CACHING],
    ),
    # ------------------------------------------------------------------ next-024
    Q(
        id="next-024", sub="Production Caching Problems", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["caching", "revalidation", "production", "cdn", "debugging"],
        ver="Next.js 16.4 (Cache Components, self-hosted)", vs=True, status="stable",
        q_en=r"""
            An admin changes a product price in the CMS. The database is correct, but customers keep seeing the old price on the product page — sometimes even after a hard refresh. The app runs Next.js 16 with Cache Components on three self-hosted instances behind a load balancer and a CDN. How do you debug and fix it?
        """,
        q_bn=r"""
            একজন admin CMS-এ একটা product-এর দাম বদলাল। Database-এ সঠিক আছে, কিন্তু customer-রা product page-এ পুরনো দামই দেখছে — কখনো hard refresh করার পরও। App চলছে Cache Components-সহ Next.js 16-এ, তিনটা self-hosted instance-এ, সামনে load balancer আর CDN। কীভাবে debug আর fix করবে?
        """,
        a_en=r"""
            I'd walk the cache layers from the user inwards and verify each one with evidence (response headers, logs), instead of guessing.

            1. **Browser router cache.** Cached content is kept client-side for the profile's `stale` time. A hard refresh bypasses it — since the old price survives a hard refresh, the problem is further in.
            2. **CDN.** Check `Cache-Control`, `Age` and the CDN's hit/miss header. If the HTML shell is cached at the CDN, a Next.js revalidation won't reach users until the CDN entry expires or is purged.
            3. **Is the data tagged and invalidated at all?** The price function needs a tag such as `cacheTag('product-42')`, and the CMS webhook must hit a Route Handler that calls `revalidateTag()` with the same tag string. A long `cacheLife` with no tag means it never updates early.
            4. **Semantics.** `revalidateTag(tag, 'max')` is stale-while-revalidate: the first visitor after the change still gets the old price. For prices use `{ expire: 0 }` in the webhook (or `updateTag` when the admin edits via a Server Action).
            5. **Multiple instances.** By default `revalidateTag` only invalidates the instance that received the webhook; the other two keep serving their own cached copy — that's why it's "random". Fix with a shared cache handler that coordinates tags (`updateTags()`/`refreshTags()` backed by Redis).

            Verify by hitting each instance directly, with `NEXT_PRIVATE_DEBUG_CACHE=1` in staging. And for money, the checkout Server Action must always re-read the price from the database — the cache is never the source of truth.
        """,
        a_bn=r"""
            আমি user-এর দিক থেকে ভেতরের দিকে cache-এর প্রতিটা স্তর ধরে এগোব, আর অনুমান না করে প্রতিটা প্রমাণ (response header, log) দিয়ে যাচাই করব।

            1. **Browser router cache।** Cached content profile-এর `stale` সময় পর্যন্ত client-এ থাকে। Hard refresh এটা bypass করে — যেহেতু hard refresh-এর পরও পুরনো দাম থাকে, সমস্যা আরও ভেতরে।
            2. **CDN।** `Cache-Control`, `Age` আর CDN-এর hit/miss header দেখো। HTML shell যদি CDN-এ cache থাকে, তাহলে CDN entry expire বা purge না হওয়া পর্যন্ত Next.js-এর revalidation user-এর কাছে পৌঁছাবে না।
            3. **Data আদৌ tag আর invalidate হচ্ছে কি?** দামের function-এ `cacheTag('product-42')`-এর মতো একটা tag থাকতে হবে, আর CMS webhook-কে এমন একটা Route Handler-এ যেতে হবে যেটা একই tag string দিয়ে `revalidateTag()` call করে। Tag ছাড়া লম্বা `cacheLife` মানে এটা আগেভাগে কখনো update হবে না।
            4. **Semantics।** `revalidateTag(tag, 'max')` হলো stale-while-revalidate: পরিবর্তনের পর প্রথম visitor তখনো পুরনো দাম পায়। দামের জন্য webhook-এ `{ expire: 0 }` ব্যবহার করো (অথবা admin Server Action দিয়ে বদলালে `updateTag`)।
            5. **একাধিক instance।** Default-ভাবে `revalidateTag` শুধু যে instance webhook পেয়েছে সেটাকেই invalidate করে; বাকি দুটো নিজেদের cached copy দেখাতেই থাকে — এজন্যই সমস্যাটা "এলোমেলো"। সমাধান: tag coordinate করে এমন shared cache handler (Redis-backed `updateTags()`/`refreshTags()`)।

            প্রতিটা instance-এ সরাসরি request পাঠিয়ে যাচাই করো, staging-এ `NEXT_PRIVATE_DEBUG_CACHE=1` দিয়ে। আর টাকার ব্যাপারে checkout Server Action-কে সবসময় database থেকে দাম আবার পড়তে হবে — cache কখনো source of truth না।
        """,
        ex_en=r"""
            **Common root causes, in order of how often I'd expect them:** tag mismatch (`product:42` vs `product-42`), webhook never reaching the app (wrong URL, failing secret check, firewall), per-instance caches, CDN caching HTML longer than the app's revalidation window, and SWR semantics misunderstood as "immediate".

            **Securing the webhook:** compare the secret in constant time, validate the payload, and rate-limit — an open revalidation endpoint lets anyone force expensive re-renders.

            **Previous-model apps** (Cache Components off) have the same layers: `fetch(..., { next: { tags } })`, `export const revalidate`, and the ISR cache on each instance's disk — the debugging approach is identical.
        """,
        ex_bn=r"""
            **সাধারণ root cause, যেগুলো আমি সবচেয়ে বেশি আশা করব সেই ক্রমে:** tag না মেলা (`product:42` বনাম `product-42`), webhook app-এ পৌঁছাচ্ছেই না (ভুল URL, secret check fail, firewall), প্রতি instance-এর আলাদা cache, app-এর revalidation সময়ের চেয়ে বেশি সময় CDN-এ HTML cache, আর SWR semantics-কে "সাথে সাথে" বলে ভুল বোঝা।

            **Webhook সুরক্ষিত করা:** secret constant time-এ তুলনা করো, payload validate করো, আর rate-limit দাও — খোলা revalidation endpoint থাকলে যে কেউ বারবার expensive re-render করাতে পারে।

            **আগের model-এর app**-এও (Cache Components বন্ধ) একই স্তরগুলো থাকে: `fetch(..., { next: { tags } })`, `export const revalidate`, আর প্রতিটা instance-এর disk-এ ISR cache — debugging-এর পদ্ধতি একই।
        """,
        tip_en=r"""Structure the answer as a layer-by-layer investigation (browser → CDN → app cache → instances) with how you'd *prove* each hypothesis. Ending with "the cache is never the source of truth for prices" shows business judgement.""",
        tip_bn=r"""উত্তরটা স্তর ধরে ধরে investigation হিসেবে সাজাও (browser → CDN → app cache → instance), আর প্রতিটা অনুমান কীভাবে *প্রমাণ* করবে সেটাও বলো। শেষে "দামের ক্ষেত্রে cache কখনো source of truth না" বললে ব্যবসায়িক বিচারবুদ্ধি বোঝা যায়।""",
        mist_en=r"""Disabling caching entirely, restarting servers as a "fix", or assuming `revalidateTag` on one instance updates all of them.""",
        mist_bn=r"""Caching পুরোপুরি বন্ধ করে দেওয়া, "সমাধান" হিসেবে server restart করা, অথবা ধরে নেওয়া যে এক instance-এ `revalidateTag` দিলে সবগুলো update হয়।""",
        code=r"""
            // lib/pricing.ts
            import { cacheLife, cacheTag } from 'next/cache';

            export async function getPrice(productId: string) {
              'use cache';
              cacheLife('hours');
              cacheTag(`product-${productId}`); // must match the webhook exactly
              return db.price.findUnique({ where: { productId } });
            }

            // app/api/cms-webhook/route.ts
            import { revalidateTag } from 'next/cache';
            import { timingSafeEqual } from 'node:crypto';

            export async function POST(request: Request) {
              const expected = Buffer.from(process.env.CMS_WEBHOOK_SECRET ?? '');
              const received = Buffer.from(request.headers.get('x-webhook-secret') ?? '');
              const valid =
                expected.length > 0 &&
                received.length === expected.length && // compare byte lengths (timingSafeEqual throws otherwise)
                timingSafeEqual(received, expected);
              if (!valid) return Response.json({ error: 'Unauthorized' }, { status: 401 });

              const { productId } = await request.json();
              if (typeof productId !== 'string') {
                return Response.json({ error: 'Invalid payload' }, { status: 400 });
              }

              revalidateTag(`product-${productId}`, { expire: 0 }); // prices: never serve stale
              revalidateTag('product-list', 'max');                  // listings: SWR is fine
              return Response.json({ revalidated: true });
            }
        """,
        lang="typescript",
        follow=[
            ("Why might the first visitor after `revalidateTag(tag, 'max')` still see the old price?", "`revalidateTag(tag, 'max')`-এর পর প্রথম visitor কেন তখনো পুরনো দাম দেখতে পারে?"),
            ("How would you make tag invalidation reach all three instances?", "Tag invalidation কীভাবে তিনটা instance-এই পৌঁছে দেবে?"),
        ],
        related=["next-015", "next-014", "next-030"],
        refs=[N_REVALIDATETAG, N_CACHE_HANDLERS, N_CDN],
    ),
    # ------------------------------------------------------------------ next-031
    Q(
        id="next-031", sub="Pages Router to App Router Migration", diff="extreme", type="scenario",
        prio="medium", market="international", mins=20,
        tags=["migration", "pages-router", "app-router", "incremental", "legacy"],
        ver="Next.js 16.4 (Pages Router legacy → App Router)", vs=True, status="stable",
        q_en=r"""
            A six-year-old e-commerce site has ~300 routes on the Pages Router: `getServerSideProps` almost everywhere, a custom `_app` with Redux, `next/head`, API routes used by the UI, and a `middleware.ts` for auth. You must move it to the App Router on Next.js 16 without a feature freeze. What's your plan?
        """,
        q_bn=r"""
            ছয় বছরের পুরনো একটা e-commerce site-এ Pages Router-এ ~৩০০টা route: প্রায় সব জায়গায় `getServerSideProps`, Redux-সহ custom `_app`, `next/head`, UI-এর ব্যবহৃত API route, আর auth-এর জন্য একটা `middleware.ts`। Feature freeze ছাড়াই এটাকে Next.js 16-এর App Router-এ নিতে হবে। তোমার পরিকল্পনা কী?
        """,
        a_en=r"""
            *(Advanced, senior-level scenario.)* The key fact: `pages/` and `app/` can coexist, so I migrate **incrementally, route by route**, shipping continuously.

            **Phase 0 — upgrade in place.** Move to Next.js 16 while still on the Pages Router (`npx @next/codemod@canary upgrade latest`): Node 20.9+, rename `middleware.ts` → `proxy.ts` (codemod `middleware-to-proxy`; proxy runs on Node.js), replace `next lint` with the ESLint CLI, runtime config → env vars, `images.domains` → `remotePatterns`, and check custom webpack config now that Turbopack is the default.

            **Phase 1 — foundation in `app/`.** Root layout (html/body, fonts, global CSS), a `'use client'` providers component (Redux store created **per request**, not as a module singleton), default metadata, error/not-found pages, and `cacheComponents` enabled from day one so routes aren't migrated twice.

            **Phase 2 — move routes in risk order:** static/marketing pages → category listings → product detail → account → cart and checkout last. The same URL can't live in both routers, so each move is a file move plus tests. Translate patterns:
            - `getServerSideProps` → async Server Components reading data directly; `getStaticProps`/`revalidate` → `'use cache'` + `cacheLife` + `cacheTag`; `getStaticPaths` → `generateStaticParams`.
            - `next/head` → `metadata`/`generateMetadata`; `next/router` → `next/navigation`.
            - Internal API routes used only by the UI → Server Actions; keep public/mobile APIs as Route Handlers.
            - Auth → optimistic check in `proxy.ts` plus a data-access layer verifying access in every Server Component/Action.

            **Rollout safety:** Playwright tests per route, canary releases, and SEO checks (status codes, canonical URLs, sitemap, structured data). Watch Core Web Vitals and conversion per migrated route.
        """,
        a_bn=r"""
            *(Advanced, senior-level scenario।)* মূল তথ্য: `pages/` আর `app/` পাশাপাশি থাকতে পারে, তাই আমি **ধাপে ধাপে, route ধরে ধরে** migrate করব, আর নিয়মিত ship করতে থাকব।

            **Phase 0 — যেখানে আছে সেখানেই upgrade।** Pages Router-এ থেকেই Next.js 16-এ যাও (`npx @next/codemod@canary upgrade latest`): Node 20.9+, `middleware.ts` → `proxy.ts` rename (codemod `middleware-to-proxy`; proxy Node.js-এ চলে), `next lint`-এর বদলে ESLint CLI, runtime config → env var, `images.domains` → `remotePatterns`, আর Turbopack default হওয়ায় custom webpack config যাচাই।

            **Phase 1 — `app/`-এ ভিত্তি।** Root layout (html/body, font, global CSS), একটা `'use client'` providers component (Redux store **প্রতি request-এ** তৈরি, module singleton হিসেবে না), default metadata, error/not-found page, আর প্রথম দিন থেকেই `cacheComponents` চালু, যাতে route দুইবার migrate করতে না হয়।

            **Phase 2 — ঝুঁকির ক্রমে route সরানো:** static/marketing page → category listing → product detail → account → সবশেষে cart আর checkout। একই URL দুই router-এ থাকতে পারে না, তাই প্রতিটা সরানো মানে file সরানো আর test। Pattern-এর রূপান্তর:
            - `getServerSideProps` → সরাসরি data পড়া async Server Component; `getStaticProps`/`revalidate` → `'use cache'` + `cacheLife` + `cacheTag`; `getStaticPaths` → `generateStaticParams`।
            - `next/head` → `metadata`/`generateMetadata`; `next/router` → `next/navigation`।
            - শুধু UI-এর ব্যবহৃত internal API route → Server Action; public/mobile API Route Handler হিসেবেই থাকবে।
            - Auth → `proxy.ts`-এ optimistic check, আর প্রতিটা Server Component/Action-এ access যাচাই করে এমন একটা data-access layer।

            **Rollout-এর নিরাপত্তা:** প্রতি route-এ Playwright test, canary release, আর SEO check (status code, canonical URL, sitemap, structured data)। প্রতিটা migrate হওয়া route-এর Core Web Vitals আর conversion পর্যবেক্ষণ।
        """,
        ex_en=r"""
            **Risks and how I'd handle them**
            - **Hard navigations between routers:** moving from a `pages/` route to an `app/` route is a full page load. Migrate tightly linked routes (category ↔ product) in the same release to avoid a "flickery" experience.
            - **Shared state:** Redux state in `_app` doesn't carry over into `app/` routes. Server data should move to Server Components anyway; keep Redux only for real client state.
            - **CSS-in-JS and third-party components** may need a client registry or `'use client'` wrappers.
            - **Bundle duplication** while both routers ship runtimes — temporary, but monitor it.
            - **Team process:** a migration guide, lint rules banning new `pages/` files, and a dashboard tracking migrated routes.

            **Trade-off:** a big-bang rewrite looks faster but freezes features and concentrates risk; incremental migration takes longer but every step is reversible.
        """,
        ex_bn=r"""
            **ঝুঁকি আর আমি কীভাবে সামলাব**
            - **Router-এর মধ্যে hard navigation:** `pages/` route থেকে `app/` route-এ যাওয়া মানে পুরো page load। ঘনিষ্ঠভাবে যুক্ত route (category ↔ product) একই release-এ migrate করো, যাতে অভিজ্ঞতা "ঝাঁকুনি"-ময় না হয়।
            - **Shared state:** `_app`-এর Redux state `app/` route-এ যায় না। Server data এমনিতেই Server Component-এ সরানো উচিত; Redux শুধু আসল client state-এর জন্য রাখো।
            - **CSS-in-JS আর third-party component**-এর জন্য client registry বা `'use client'` wrapper লাগতে পারে।
            - দুটো router-ই runtime পাঠানোর সময় **bundle duplication** — সাময়িক, তবে পর্যবেক্ষণে রাখো।
            - **Team process:** migration guide, নতুন `pages/` file নিষিদ্ধ করে এমন lint rule, আর migrate হওয়া route track করার dashboard।

            **Trade-off:** একবারে পুরোটা rewrite দেখতে দ্রুত মনে হয়, কিন্তু feature আটকে যায় আর ঝুঁকি এক জায়গায় জমে; ধাপে ধাপে migration বেশি সময় নেয়, কিন্তু প্রতিটা ধাপ ফিরিয়ে নেওয়া যায়।
        """,
        tip_en=r"""Lead with "both routers coexist, so it's incremental", then phases with a clear risk order. Showing exact pattern translations (gSSP → async Server Component, `next/head` → metadata) proves hands-on knowledge of both worlds.""",
        tip_bn=r"""শুরু করো "দুটো router পাশাপাশি থাকে, তাই এটা ধাপে ধাপে" দিয়ে, তারপর ঝুঁকির স্পষ্ট ক্রমসহ phase-গুলো বলো। নির্দিষ্ট pattern-এর রূপান্তর দেখালে (gSSP → async Server Component, `next/head` → metadata) দুই জগতেই হাতে-কলমে জ্ঞান প্রমাণ হয়।""",
        mist_en=r"""Starting with checkout, keeping a module-level Redux store (shared between users on the server), or assuming `middleware.ts` keeps working unchanged as the long-term solution.""",
        mist_bn=r"""Checkout দিয়ে শুরু করা, module-level Redux store রাখা (server-এ বিভিন্ন user-এর মধ্যে share হয়ে যায়), অথবা ধরে নেওয়া যে `middleware.ts` কোনো পরিবর্তন ছাড়াই দীর্ঘমেয়াদি সমাধান হিসেবে চলবে।""",
        code=r"""
            // BEFORE — pages/products/[id].tsx (Pages Router, legacy)
            import Head from 'next/head';

            export async function getServerSideProps({ params }) {
              const product = await getProduct(params.id);
              if (!product) return { notFound: true };
              return { props: { product } };
            }

            export default function ProductPage({ product }) {
              return (
                <>
                  <Head><title>{product.name} | Shop</title></Head>
                  <ProductView product={product} />
                </>
              );
            }

            // AFTER — app/products/[id]/page.tsx (App Router + Cache Components)
            import { notFound } from 'next/navigation';
            import { cacheLife, cacheTag } from 'next/cache';

            async function getProductCached(id: string) {
              'use cache';
              cacheLife('hours');
              cacheTag(`product-${id}`);
              return getProduct(id);
            }

            export async function generateStaticParams() {
              const ids = await getBestSellerIds(200); // prerender popular products at build
              return ids.map((id) => ({ id }));
            }

            export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
              const { id } = await params;
              const product = await getProductCached(id);
              return { title: product?.name ?? 'Product not found' }; // root layout adds "| Shop"
            }

            export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
              const { id } = await params;
              const product = await getProductCached(id);
              if (!product) notFound();
              return <ProductView product={product} />;
            }
        """,
        lang="tsx",
        follow=[
            ("How would you A/B test a migrated route against the old one?", "Migrate হওয়া route-কে পুরনোটার বিরুদ্ধে কীভাবে A/B test করবে?"),
            ("How do you create a Redux store per request in the App Router, and why does it matter?", "App Router-এ প্রতি request-এ Redux store কীভাবে তৈরি করবে, আর এটা কেন জরুরি?"),
        ],
        related=["next-012", "next-014"],
        refs=[N_MIGRATE_APP, N_UPGRADE16, N_PROXY],
    ),
]

if __name__ == "__main__":
    save("nextjs", "b2", QUESTIONS)
