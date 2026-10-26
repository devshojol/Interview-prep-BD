# Next.js content audit
Coverage: next-001, next-002, next-003, next-004, next-005, next-006, next-007, next-008, next-009, next-010, next-011, next-012, next-013, next-014, next-015, next-016, next-017, next-018, next-019, next-020, next-021, next-022, next-023, next-024, next-025, next-026, next-027, next-028, next-029, next-030, next-031, next-032. **32 of 32 reviewed.**

Distribution: easy 11 (001–011), medium 11 (012–022), hard 7 (023–029), extreme 3 (030–032). This is on target. There are 8 MCQs (002, 005, 007, 011, 015, 020, 026, 029).

## Category summary
This is a very current, technically careful category.

- **Version facts are right.** The Next.js 16 APIs are used correctly: `proxy.ts`, async request APIs, Cache Components with `'use cache'`/`cacheLife`/`cacheTag`, `updateTag` vs `revalidateTag(tag, profile)`, `refresh()`, the `default.js` requirement, removed AMP/`next lint`/runtime config, and `images.remotePatterns`.
- **Previous models are labelled.** The pre-Cache-Components model and the Pages Router are consistently marked as previous/legacy.
- **Live checks support the high-risk claims.** I checked the official docs for:
  - the `error.js` `retry` prop (stable since 16.3) and `catchError`;
  - `npx next analyze` / `--output` (since 16.1);
  - the ISR-with-Cache-Components guide and `partialPrefetching`;
  - proxy runtime rules and `unstable_doesProxyMatch`.
  All matched the content.
- **Strengths:**
  - Security is handled well: Server Actions as public endpoints, the DAL pattern, IDOR, open-redirect, timing-safe webhook secrets.
  - Production scenarios are realistic: multi-instance cache coordination, version skew, CDN layers, standalone Docker.
  - Every senior answer includes failure modes.
- **Weaknesses:**
  - **Redundancy.** "Proxy is not the security boundary / Server Actions are public POST endpoints" is taught three times (020, 023, 025). The layout-error nesting rule is taught twice (006, 029). Shared-cache/`{expire:0}` content repeats across 024/030/032.
  - **Coverage gaps.** Missing: Link/navigation & prefetching (including the 16.4 partial prefetching / `ensureStatic` / `navigation()` APIs listed in FACTS), `next/font`, testing, and `revalidatePath` as a main topic.
  - **One security-performance example has a flaw.** 028 ships unsanitised `marked` HTML via `dangerouslySetInnerHTML` in its "AFTER" (recommended) code.
  - Several minor code/text inconsistencies.
- **Bangla:** natural and technically faithful, with the same minor calques as react ("লোভনীয়", "ঠান্ডা cache") and one dropped caveat.
- **Version currency:** 019 calls Node 24 "LTS … the safe choice today". That is stale after 2026-10-20 (Maintenance) and 2026-10-28 (Node 26 LTS).

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8 | English quality 9 | Examples & code 8 | Originality/information value 7 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| NEXT-C01 | next-028 | code | P2 | Security in example | The "AFTER" code (the recommended version) in a **security-performance** question parses CMS markdown with `marked` and injects it via `dangerouslySetInnerHTML` with only a comment saying to sanitise. `marked` does not sanitise. Learners will copy an XSS-prone pattern as "best practice". | `const html = await marked.parse(post.markdown);` … `<div dangerouslySetInnerHTML={{ __html: html }} /> {/* sanitise CMS HTML */}` | Actually sanitise on the server: `const html = sanitizeHtml(await marked.parse(post.markdown))` (sanitize-html or isomorphic-dompurify). Add one sentence to "Security angle": moving parsing to the server doesn't remove the XSS risk. | High | Recommended code contains a sanitisation call; explanation mentions it. |
| NEXT-C02 | next-020, next-023, next-025 | both | P2 | Redundancy | Three questions share the same core lesson and near-identical sentences: proxy is optimistic, Server Actions are POSTs to the page route so a matcher change can skip them, and a DAL must verify. 020 is effectively an MCQ version of 023. | 020: "a matcher change or moving the action to another route can silently remove proxy coverage"; 023: "a matcher change can silently skip them"; 025: "a matcher change can silently skip them" | Keep 023 (deep) and 025 (proxy coding). Repurpose 020 into a currently missing topic (e.g. an MCQ on `<Link>` prefetching, `revalidatePath` vs `revalidateTag`, or `next/font`). | High | No two questions share the same primary learning objective. |
| NEXT-C03 | next-006, next-029 | both | P3 | Redundancy | 006 already teaches that a segment's `layout.tsx` error goes to the parent `error.tsx`, and its follow-up literally asks 029's question. 029 then repeats the nesting order verbatim. | 006: "an error thrown by a segment's own `layout.tsx` is handled by the parent segment's `error.tsx`"; 006 follow-up: "Why does an error in `app/dashboard/layout.tsx` not show `app/dashboard/error.tsx`?" | Remove that sentence and follow-up from 006, or refocus 029 on `global-error`/`catchError`/`retry` vs `reset`. | High | The fact appears as a primary point in one question only. |
| NEXT-C04 | next-001…032 (category) | both | P2 | Coverage gap | Missing or thin topics for the target audience: <br>- `<Link>`/client navigation and prefetching, including the 16.4 additions in FACTS (`partialPrefetching`, `export const ensureStatic`, `navigation()`/`prefetch()` from `next/cache`) — no question; <br>- `next/font` — only listed in 001; <br>- `revalidatePath` — mentioned only; <br>- testing a Next.js app (Playwright, testing Server Actions) — only a phrase in 031; <br>- `after()` — mention only; <br>- i18n routing — absent. | 014 code: `partialPrefetching: true` (never explained) | Add a medium question on navigation/prefetching (Link, `useRouter` from `next/navigation`, `prefetch`, Partial Prefetching/App Shell in 16.4). Fold `next/font` into 008 or 028. | High | COVERAGE + FACTS 16.4 items have at least one primary question. |
| NEXT-C05 | next-014 | both | P3 | Unexplained code | The config enables `partialPrefetching: true` (a real 16.4 option, verified), but the answer never says what it does. Readers can't tell whether it is required for Cache Components. | `const nextConfig: NextConfig = { cacheComponents: true, partialPrefetching: true };` | Either remove it, or add a bullet: "16.4 `partialPrefetching` lets Next.js serve an App Shell instantly for params not in `generateStaticParams` and prefetch only the shell; with it, await `params` inside `<Suspense>`." | High (option exists per docs) | Every config key in the example is explained. |
| NEXT-C06 | next-022 | both | P3 | Internal inconsistency | The answer text says `cacheLife('hours')`, but the code it describes uses `cacheLife('days')`. It also omits the 16.4 Partial Prefetching distinction (with it, unlisted slugs get an App Shell instantly; without it, the first request waits — equivalent to `fallback: 'blocking'` vs `fallback: true`). That distinction is the core of "ISR with Cache Components" in the docs. | Code: `cacheLife('days');` vs answer: "put `'use cache'` with `cacheLife('hours')`" (BN: "`cacheLife('hours')`") | Align on `'days'` (matches the tag-based explanation). Add one line mapping `fallback: 'blocking'` → await params outside Suspense, and `fallback: true` → Partial Prefetching + await inside Suspense. | High | Code and text match; the fallback mapping is present. |
| NEXT-C07 | next-009 | both | P3 | Accuracy of edge-case claim | The explanation says `Number()` + `Number.isInteger` + `> 0` handles the edge cases. Node shows it accepts `"0x1A"`→26, `"1e3"`→1000, `" 7 "`→7, `"1.0"`→1 and unsafe integers. Non-canonical ids are accepted and map to other products. | "`Number()` plus `Number.isInteger` and `> 0` handles them" | Validate the string first: `if (!/^[1-9]\d*$/.test(id)) return 400`, then `Number.isSafeInteger`. Mention hex/exponent strings as an edge case. | High (executed) | `/api/products/0x1A` returns 400. |
| NEXT-C08 | next-016 | both | P3 | Internal inconsistency | The question says the page is blank for "about 3.5 seconds"; the answer says the sequential awaits add up to ~3.7 s. 200 ms + 2.5 s + 1 s = 3.7 s. | Q: "shows nothing for about 3.5 seconds"; A: "sequential awaits add up to ~3.7 s" | Change the question to "about 3.7 seconds" (BN: "প্রায় ৩.৭ সেকেন্ড"). | High | Numbers agree. |
| NEXT-C09 | next-019 | both | P3 | Version currency | Recommends Node 24 as "LTS … the safe choice today" and uses `node:24-alpine`. Per FACTS, v24 entered Maintenance on 2026-10-20 and v26 becomes Active LTS on 2026-10-28 (2 days after the audit date). | "Node.js 24 LTS is the safe choice today (Next.js 16 needs at least 20.9)"; `ver=… Node.js 24 LTS` | "Use a supported LTS image: Node 24 (Maintenance LTS) or Node 26 (Active LTS from 2026-10-28); pin the major and rebuild regularly." Update `ver`. | High (per FACTS) | Text matches the FACTS release schedule. |
| NEXT-C10 | next-017 | both (code) | P3 | Robustness of fix | The fixed version formats a date with `Intl.DateTimeFormat` inside a Client Component and claims "Same output on the server and in every browser". ICU data differs between Node and browsers and across versions (e.g. spacing/format variants), so this can still mismatch. Formatting once on the server and passing a string (already mentioned in the answer) is the robust fix. | `// Same output on the server and in every browser` | Soften to "usually identical", and make "format on the server and pass the string (or render a `<time dateTime>` and `suppressHydrationWarning` on that one node)" the primary recommendation. | Medium | Comment no longer guarantees identical output. |
| NEXT-C11 | next-030 | code | P3 | Example quality | Cache-handler excerpt: <br>- `refreshTags()` runs before every request and `mGet`s every tag ever stored in an ever-growing `revalidated-tags` set (unbounded); <br>- `redis.connect()` isn't awaited or error-handled; <br>- `publish` has no subscriber shown; <br>- `require.resolve` in an ESM `next.config.ts` can confuse learners. <br>The explanation itself is excellent. | `const tags = await redis.sMembers('revalidated-tags');` (read on every request) | Add a comment: "store `tag:*` with TTL ≥ max cacheLife expire, or keep a version counter and diff". Await connect with error handling. Note the subscriber side. Use `path.resolve`/`import.meta.resolve` or `.mjs` paths as in the docs. | Medium | Excerpt has a bounded refresh strategy. |
| NEXT-C12 | next-032 | code | P3 | Validation gap | The `region` route param is used directly as a cache-key argument and for currency lookup without validation. Arbitrary `/xx/products/1` URLs create unbounded cache variants, which undermines the answer's own "small, bounded number of variants" argument. | `const { region, id } = await params;` … "keeps a small, bounded number of variants" | Add `if (!['bd','us'].includes(region)) notFound();` (or `export const dynamicParams = false` for the region segment in a layout). | Medium | Unknown region returns 404. |
| NEXT-C13 | next-023 | both | P3 | Internal inconsistency | `verifySession()` throws `new Error('Unauthorized')`, while the explanation says to "return expected errors (validation, forbidden) as values". An unauthenticated call therefore surfaces as a generic error/error boundary rather than a typed result. | `if (!session?.userId) throw new Error('Unauthorized');` vs "return expected errors … as values" | Either return `{ ok:false, error:'Unauthorized' }` in the action, or explain that the DAL throws/redirects (`redirect('/login')`) on purpose. | Medium | Code and guidance are consistent. |
| NEXT-C14 | next-002, 005, 007, 011, 015, 020, 026, 029 | both | P3 | Question quality | Every MCQ has empty follow-ups. | `FOLLOW-UPS: []` | Add 1–2 each (e.g. 015: "When would you use `refresh()`?"; 026: "How would you cache per-user data safely?"). | High | No empty follow-ups. |
| NEXT-C15 | next-009, next-021 | n/a | P3 | Labels | `market=bangladesh` on a Route Handler coding task and a provider debugging task is not justified by the FACTS rule (BD = MCQ/output-tracing fundamentals, viva definitions). | `next-009 … market=bangladesh`; `next-021 … market=bangladesh` | Set to `both`. | Medium | Labels follow FACTS guidance. |
| NEXT-C16 | next-002, 005, 007, 011, 015, 020, 026, 029; next-030; next-014; next-031; next-005 | BN | P3 | Bangla naturalness | Calques: "লোভনীয় (ভুল) উত্তর" for "tempting answer"; "ঠান্ডা cache" for "cold cache" (BD devs say "cold cache"); "দর্শনের পরিবর্তন" for "philosophy shift"; "'ঝাঁকুনি'-ময়" (031); "বড় বাড়তি নম্বর" (005). | 030 BN: "নতুন deploy ঠান্ডা cache দিয়ে শুরু হয়"; 031 BN: "অভিজ্ঞতা "ঝাঁকুনি"-ময় না হয়" | "সবচেয়ে বিভ্রান্তিকর উত্তর"; "cold cache"; "মূল ধারণার পরিবর্তন"; "অভিজ্ঞতা যেন খাপছাড়া না লাগে"; "বাড়তি সুবিধা". | Medium | BD reviewer read-through. |
| NEXT-C17 | next-012 | BN | P3 | BN meaning drift | The EN intro labels the Pages Router as legacy. The BN intro drops that caveat. | EN: "The main differences (the Pages Router is the legacy option):" / BN: "মূল পার্থক্যগুলো:" | BN: "মূল পার্থক্যগুলো (Pages Router হলো legacy option):" | High | BN carries the same caveat. |
| NEXT-C18 | next-010 | both | P3 | Difficulty label | Labelled easy, but the answer requires Cache Components, a component-level static shell and Partial Prerendering. That is medium material for juniors (the four classic definitions alone would be easy). | `next-010 | Rendering Strategies | easy` | Either relabel medium, or keep easy and move the PPR paragraph into the explanation as "bonus". | Medium | Label matches the content depth. |

## Per-question notes
- next-001 — OK
- next-002 — issues: NEXT-C14, C16; scores acc 10 / depth 8 / BN 8 / EN 9
- next-003 — OK (layout persistence, no `searchParams`, "not involved when a Server Action is called" — all correct)
- next-004 — OK
- next-005 — issues: NEXT-C14, C16; scores acc 10 / depth 9 / BN 8 / EN 9
- next-006 — issues: NEXT-C03; scores acc 10 / depth 9 / BN 9 / EN 9 (`retry` prop verified: unstable 16.2, stable 16.3; `reset` still documented)
- next-007 — issues: NEXT-C14, C16; scores acc 10 / depth 9 / BN 8 / EN 9
- next-008 — OK (see Needs verification for 16.x image defaults)
- next-009 — issues: NEXT-C07, C15; scores acc 8 / depth 9 / BN 9 / EN 9
- next-010 — issues: NEXT-C18; scores acc 10 / depth 9 / BN 9 / EN 9
- next-011 — issues: NEXT-C14, C16; scores acc 10 / depth 9 / BN 8 / EN 9 (Node default runtime / codemod verified)
- next-012 — issues: NEXT-C17; scores acc 10 / depth 9 / BN 8 / EN 9
- next-013 — OK
- next-014 — issues: NEXT-C05; scores acc 9 / depth 10 / BN 8 / EN 9
- next-015 — issues: NEXT-C14, C16; scores acc 9 / depth 9 / BN 8 / EN 9
- next-016 — issues: NEXT-C08; scores acc 9 / depth 10 / BN 9 / EN 9
- next-017 — issues: NEXT-C10; scores acc 9 / depth 10 / BN 9 / EN 9
- next-018 — OK
- next-019 — issues: NEXT-C09; scores acc 9 / depth 10 / BN 9 / EN 9
- next-020 — issues: NEXT-C02, C14, C16; scores acc 10 / depth 9 / BN 8 / EN 9
- next-021 — issues: NEXT-C15; scores acc 10 / depth 9 / BN 9 / EN 9 (19.3 context claim verified)
- next-022 — issues: NEXT-C06; scores acc 9 / depth 9 / BN 9 / EN 9
- next-023 — issues: NEXT-C02, C13; scores acc 9 / depth 10 / BN 9 / EN 9
- next-024 — OK (layered debugging, timing-safe secret compare correct)
- next-025 — issues: NEXT-C02 (overlap); scores acc 10 / depth 10 / BN 9 / EN 9 (matcher, runtime rule, `unstable_doesProxyMatch` verified)
- next-026 — issues: NEXT-C14, C16; scores acc 10 / depth 9 / BN 8 / EN 9
- next-027 — OK
- next-028 — issues: NEXT-C01; scores acc 9 / depth 9 / BN 9 / EN 9 (`next analyze` + `--output` verified)
- next-029 — issues: NEXT-C03, C14, C16; scores acc 10 / depth 8 / BN 8 / EN 9 (`catchError` verified in docs)
- next-030 — issues: NEXT-C11, C16; scores acc 9 / depth 10 / BN 8 / EN 9
- next-031 — issues: NEXT-C16 (minor); scores acc 10 / depth 10 / BN 8 / EN 9
- next-032 — issues: NEXT-C12; scores acc 9 / depth 10 / BN 9 / EN 9

## Coverage & gaps
- **Covered:** architecture, App/Pages Router, file routing, layouts/templates, dynamic routes, route handlers, RSC/client components and providers, SSR/SSG/ISR/CSR, streaming/Suspense, hydration errors, Server Actions (+ security), Cache Components, revalidation APIs, the previous model (labelled), proxy, auth, metadata/SEO, images, env vars, error/not-found/global-error, loading, Docker/standalone, bundle performance, parallel/intercepting routes, multi-instance caching, migration.
- **Gaps (NEXT-C04):**
  - Link/navigation/prefetching, including the 16.4 `partialPrefetching`, `ensureStatic` and `navigation()`/`prefetch()` APIs that FACTS lists;
  - `next/font`;
  - `revalidatePath` as a primary topic;
  - testing;
  - `after()`;
  - i18n;
  - static export (one mention).
- **Redundant:** 020/023/025 (NEXT-C02); 006/029 (NEXT-C03); 024/030/032 all re-teach shared cache handlers + `{ expire: 0 }` (acceptable progression, but trim the repeated sentences); 010/014/022 overlap on the cache model.
- **Difficulty:** 010 is arguably medium (NEXT-C18). Otherwise the progression is good.
- **Cross-tech duplicates:** react-008 and next-021 share the identical 19.3 `<Context value>` paragraph; react-022 and next-004 overlap on the serialisable-props boundary.

## Needs verification
- next-008: "in Next.js 16 that's `preload` (the old `priority` prop is deprecated)"; "default `minimumCacheTTL` is 4 hours in v16"; "`images.qualities` now defaults to `[75]`"; "local images with query strings need `localPatterns`". These are consistent with my recollection of the Next 16 upgrade guide; not fetched.
- next-015: "the single-argument `revalidateTag(tag)` is deprecated; it behaves like `{ expire: 0 }`". The deprecation is in FACTS; the exact legacy behaviour was not verified (Low–Medium).
- next-014: "`'use cache: private'` exists for rare cases" (status stable vs experimental not verified); "cached content is also kept in the browser router for the profile's `stale` time (minimum 30 seconds)"; "`NEXT_PRIVATE_DEBUG_CACHE=1`".
- next-024 / next-030: the cache handler interface method names `updateTags()`, `refreshTags()`, `getExpiration()`. These match my memory of the `cacheHandlers` docs; not re-fetched.
- next-028: "Next.js 16 removed the per-route `size` / `First Load JS` columns from `next build` output". Believed correct; not fetched.
- next-019 / next-030: `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` must be set at build time; `deploymentId` triggers a hard navigation on skew.
- next-013: Zod 4 `z.flattenError(error).fieldErrors` and `z.uuid()` (next-023). Believed correct for Zod 4.
- next-032: "`'use cache: private'` can make per-user results prefetchable in the browser". Plausible; not verified.

## Verified
- WebFetch https://nextjs.org/docs/app/api-reference/file-conventions/error:
  - The `retry` prop exists; the version history says "v16.3.0 `retry` prop became stable; v16.2.0 `unstable_retry` added".
  - `reset` is still documented as "re-render … without re-fetching".
  - `catchError` is documented for component-level boundaries.
  - It confirms that error.js "does not wrap the layout.js or template.js above it in the same segment".
  - This supports next-006 and next-029.
- WebFetch https://nextjs.org/docs/app/guides/package-bundling:
  - `npx next analyze` is "Available in v16.1 and later"; `--output` writes to `.next/diagnostics/analyze`.
  - `experimental.optimizePackageImports` is confirmed.
  - This supports next-028.
  - (A WebSearch result mentioned `next experimental-analyze` from the 16.1 launch period; the current docs use `next analyze`.)
- WebFetch https://nextjs.org/docs/app/guides/incremental-static-regeneration-cache-components:
  - The page exists (ref used in 022/032).
  - `partialPrefetching: true` is a real next.config option.
  - Without Partial Prefetching, `params` must be awaited outside `<Suspense>` to create per-URL ISR entries (consistent with 022/032 code). With it, await inside Suspense.
  - The App Shell for unlisted params is served from 16.3. This is the basis for NEXT-C05/C06.
- WebFetch https://nextjs.org/docs/app/api-reference/file-conventions/proxy:
  - "Proxy defaults to using the Node.js runtime. The `runtime` config option is not available in Proxy files."
  - Codemod `npx @next/codemod@canary middleware-to-proxy .`
  - `unstable_doesProxyMatch` from `next/experimental/testing/server`.
  - Server Functions are POSTs to the route, "A matcher change … can silently remove Proxy coverage".
  - Matcher values must be constants.
  - This supports next-011, 020, 023 and 025.
- WebFetch https://react.dev/blog/2026/09/09/react-19-3: confirms the `browser()` usage in next-017 and the Context rendering in next-021.
- Executed with `/usr/local/bin/node` (SCRATCH/run/num.js): `Number()` validation for next-009. Output: `"0x1A" 26 true`, `"1e3" 1000 true`, `" 7 " 7 true`, `"1.0" 1 true`; `"12abc"`, `"1.5"`, `"-3"`, `"0"` are correctly rejected. `Intl.DateTimeFormat('en-GB', {dateStyle:'medium', timeStyle:'short', timeZone:'Asia/Dhaka'})` → "26 Oct 2026, 09:05" in Node (browser comparison not possible here).
