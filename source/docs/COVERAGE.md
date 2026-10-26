# Category coverage (from the product spec). Every category must address all listed subtopics.

## html — HTML
Semantic HTML; document structure; forms and validation; accessibility; HTML attributes; `data-*` attributes; SEO-related markup; meta tags; script loading (defer/async/module); browser parsing; DOM fundamentals; HTML APIs (dialog, popover, invoker commands, details, template, etc.); common mistakes; practical implementation scenarios.

## css — CSS
Box model; specificity and inheritance; cascade (incl. @layer); stacking contexts; positioning; Flexbox; CSS Grid (incl. subgrid); responsive design; media queries; container queries; pseudo-classes and pseudo-elements (:has, :is, :where); CSS variables; transitions and animations; accessibility (prefers-reduced-motion, focus-visible, contrast); performance (reflow/repaint, compositing, content-visibility); layout debugging; responsive UI scenarios. Modern features with correct Baseline status (nesting, @scope, anchor positioning not Baseline, etc.).

## javascript — JavaScript (STRONG coverage, 40 questions)
Variables and data types; scope and hoisting; closures; `this`; arrow functions; prototypes and inheritance; objects and arrays; shallow vs deep copies (structuredClone); destructuring and spread; array methods; Promises; async/await; event loop; microtasks and tasks; call stack; execution contexts; lexical environments; modules; error handling; debouncing and throttling; event delegation; DOM manipulation; memory leaks; garbage collection; immutability; functional programming; ES modules vs CommonJS; performance; security (XSS, prototype pollution); output prediction (several!); coding exercises (several!); modern ES2025/ES2026 features.

## react — React
Components and JSX; props and state; functional components; hooks; useState; useEffect; useRef; useMemo; useCallback; useContext; custom hooks; component lifecycle concepts; rendering and reconciliation; keys; controlled and uncontrolled components; forms (Actions, useActionState, useFormStatus, useOptimistic); Context API; Redux fundamentals (Redux Toolkit); performance optimization; React.memo; effects and cleanup; stale closures; error boundaries; Suspense; lazy loading; Server Components vs Client Components; current React features (19.2 Activity/useEffectEvent, 19.3 ViewTransition/Fragment refs/browser(), React Compiler); testing concepts (React Testing Library); accessibility; production debugging.

## nextjs — Next.js
Next.js architecture; App Router; Pages Router; file-based routing; layouts; dynamic routes; route handlers; Server Components; Client Components; SSR; static generation; ISR; streaming; Suspense; hydration (and hydration errors); Server Actions; data fetching; caching and revalidation (Cache Components, 'use cache', cacheLife, cacheTag, revalidateTag(tag, profile), updateTag, refresh, revalidatePath; previous model labelled); middleware → proxy.ts conventions; authentication; metadata and SEO; image optimization; environment variables (NEXT_PUBLIC_); error handling (error.js, not-found, global-error); loading states (loading.js); deployment (Vercel, self-hosting, standalone output, Docker); performance; production problems.

## reactnative — React Native (with Expo; 40 questions)
What React Native is (native views, not a WebView) vs Flutter/native/PWA; New Architecture (Fabric, TurboModules, JSI,
bridgeless; the old bridge as history); Hermes; core components (View, Text, Image, TextInput, Pressable, ScrollView) and why
text must be inside `<Text>`; styling (StyleSheet, Flexbox defaults: column, `flex: 1`, no cascade), responsive layout
(`useWindowDimensions`, safe areas, Android edge-to-edge); platform differences (`Platform.OS`, `.ios.tsx`/`.android.tsx`);
lists (FlatList, SectionList, keys, `getItemLayout`, FlashList) and list performance; navigation (Expo Router file-based routing,
stacks/tabs/modals, dynamic routes, React Navigation 7 underneath, deep linking, typed routes); state management (Context,
Zustand/Redux Toolkit, server state with TanStack Query); forms and keyboard handling (`KeyboardAvoidingView`); networking
(fetch, offline handling with NetInfo, retry); **local storage**: AsyncStorage vs `expo-secure-store` vs MMKV vs
**expo-sqlite** (API, `SQLiteProvider`/`useSQLiteContext`, migrations with `PRAGMA user_version`, transactions, prepared
statements, WAL, SQL injection, Drizzle with expo-sqlite); offline-first sync design; **Expo**: Expo Go vs development builds,
CNG/prebuild and config plugins, `app.json`/`app.config.ts`, environment variables (`EXPO_PUBLIC_`), **EAS Build / Submit /
Update** (OTA rules, runtimeVersion); permissions (camera, location, notifications); push notifications (expo-notifications,
FCM/APNs); images and media (`expo-image`, `expo-audio`/`expo-video`); animations (Animated vs Reanimated 4 worklets, UI vs JS
thread) and gestures; native modules (Expo Modules API, when you need native code); performance (JS thread blocking, re-renders,
memo, Hermes profiling, startup time, bundle size); debugging (React Native DevTools, logs, crash reporting); security (secure
storage, certificate pinning awareness, secrets in the bundle are public); testing (Jest + React Native Testing Library, E2E with
Maestro/Detox); app store release basics (signing, versioning, store review); accessibility (`accessibilityLabel`, roles,
dynamic font size); common production problems (keyboard covering inputs, slow lists, memory from large images, OTA update
broke native compatibility). Legacy topics (`AsyncStorage` in core, Expo `expo-av`, legacy bridge, `react-native link`) only as
labelled legacy.

## nodejs — Node.js
Node.js runtime; V8 and libuv; event loop (phases, process.nextTick, setImmediate); non-blocking I/O; asynchronous programming; streams (backpressure, pipeline); Buffers; file system APIs (fs/promises); EventEmitter; modules (ESM/CJS, require(esm)); package management (npm, lockfiles, semver); processes and environment variables (--env-file); error handling (unhandledRejection, uncaughtException); worker threads; clustering; memory management (heap, leaks); CPU-intensive tasks; API design; security (permission model, dependency risk); logging; graceful shutdown; performance and scalability; LTS release model.

## express — Express.js
Routing (Express 5 path syntax); middleware; request and response lifecycle; error-handling middleware; REST APIs; validation; authentication; authorization; JWT; cookies and sessions; CORS; rate limiting; security headers (helmet); file uploads (multer); pagination; filtering and sorting; centralized error handling (Express 5 async errors); API versioning; logging; testing (supertest); deployment; production debugging. Include practical middleware implementation questions. Express 4 → 5 migration.

## nestjs — NestJS
Modules; controllers; providers; dependency injection (scopes, custom providers); services; decorators (custom decorators); pipes; guards; interceptors; exception filters; DTOs; validation (class-validator/ValidationPipe AND v12 Standard Schema validation); middleware; authentication and authorization (Passport/JWT, RBAC); guards vs middleware; request lifecycle order; configuration (@nestjs/config); database integration (TypeORM/Prisma/Drizzle/Mongoose); testing (Test.createTestingModule); REST APIs; WebSockets and microservices fundamentals; application architecture; Express adapter vs Fastify adapter; NestJS vs Express comparisons; NestJS 12 changes (ESM, Node requirement).

## mongodb — MongoDB
Documents and collections; BSON vs JSON; CRUD; query operators; projection; aggregation pipelines ($match, $group, $lookup, $unwind, $facet); indexes; compound indexes (ESR rule); unique indexes; text indexes (and Atlas Search mention); schema design; embedding vs referencing; transactions; replication (replica sets, write/read concern); sharding (shard keys); atomicity; consistency; performance (explain); security; backup and recovery; real-world data modeling. MongoDB 9.0 notes.

## mongoose — Mongoose
Schemas and models; documents; CRUD; validation; middleware and hooks (v9: no `next()` in pre hooks); populate(); references; virtuals; instance and static methods; lean queries; indexes (autoIndex, syncIndexes); query performance; transactions (session, withTransaction / connection.transaction); error handling (ValidationError, CastError, E11000); schema design; common pitfalls; native driver vs Mongoose. Mongoose 9 changes.

## postgresql — PostgreSQL
Relational fundamentals; tables and relationships; primary and foreign keys; constraints; joins; indexes; B-tree and other index types (GIN, GiST, BRIN, hash, partial, expression, covering INCLUDE); transactions; ACID; MVCC; isolation levels; normalization; query planning; EXPLAIN and EXPLAIN ANALYZE; CTEs; window functions; JSONB; locks and deadlocks; migrations (safe zero-downtime); replication (streaming, logical); connection pooling (PgBouncer); performance optimization (VACUUM, autovacuum, bloat); backup and recovery (pg_dump, PITR, incremental backup PG17); PostgreSQL 18 features (uuidv7, virtual generated columns, skip scan, OLD/NEW RETURNING, AIO).

## sql — SQL (portable SQL; label PostgreSQL-specific syntax)
SELECT; WHERE; ORDER BY; GROUP BY; HAVING; JOIN types; subqueries; CTEs (incl. recursive); aggregate functions; window functions; INSERT/UPDATE/DELETE; constraints; keys; normalization; transactions; ACID; NULL behaviour (three-valued logic); indexes; views; stored procedures and triggers; query optimization; SQL injection (parameterized queries); practical query-writing exercises with realistic schemas (users, employees, departments, orders, products) — e.g. second highest salary, top N per group, running totals, customers without orders, duplicates. Each query question: schema + sample data + query + expected result + logic.

## drizzle — Drizzle ORM (stable 0.45.x; v1.0 is RC → label as preview)
Type-safe queries; schema definitions (pgTable, column types, identity columns); tables and relations; select/insert/update/delete; joins; relational queries (`db.query.users.findMany({ with })`, relations()); migrations (drizzle-kit generate/migrate/push/pull, drizzle.config.ts); schema generation; transactions; prepared statements (placeholder); PostgreSQL integration (node-postgres / postgres.js drivers); type inference ($inferSelect/$inferInsert); relations vs foreign keys; Drizzle Kit; error handling; connection management (pooling, serverless); Drizzle vs Prisma; Drizzle vs raw SQL (sql template); when an ORM is appropriate; Drizzle v1 RC changes (defineRelations, RQB v2) as preview.

## redis — Redis
In-memory storage; key-value fundamentals; strings, hashes, lists, sets, sorted sets; TTL and expiration (incl. hash field expiration); cache-aside; cache invalidation; session storage; rate limiting (fixed window, sliding window, token bucket with Lua/sorted sets); Pub/Sub; Streams (consumer groups); persistence (RDB/AOF); eviction policies; memory usage; cache stampedes; distributed locks and limitations (Redlock, fencing tokens); Redis vs traditional databases; Redis vs Memcached; Node.js integration (node-redis v5/6, ioredis); production failure scenarios; Redis 8 (Open Source, licensing, Vector Sets), Valkey awareness; cluster/sentinel basics.

## vectordb — Vector Databases (basic; beginner-friendly + some intermediate)
Embeddings; vectors and dimensions; similarity search; cosine similarity; Euclidean distance (and dot product); approximate nearest neighbour (ANN) search (HNSW, IVF intuition); semantic search; metadata filtering (pre vs post filtering); chunking; vector indexing fundamentals; vector DBs vs relational DBs (pgvector option); vector DBs vs full-text search; hybrid search (BM25 + vectors, RRF); RAG architecture; retrieval quality (recall@k, reranking); embedding model changes (re-embedding, versioning, dimension mismatch); data privacy; basic production use cases. No heavy math for easy questions. Product-neutral, mention pgvector 0.8.x / Redis / Pinecone / Qdrant / Weaviate / Milvus only as examples.

## docker — Docker
Containers vs VMs; images and containers; Dockerfiles; layers and caching; build contexts (.dockerignore); volumes; bind mounts; networks (bridge, user-defined, DNS); port mapping; environment variables; Docker Compose (compose.yaml, no `version:`); multi-stage builds; non-root containers; health checks; container logs; image optimization; secrets (build secrets, runtime); production deployment; container debugging (exec, inspect, logs, exit codes 137/OOM); Docker vs Kubernetes fundamentals. Practical Dockerfile and Compose questions (Node.js/Next.js apps).

## nginx — NGINX
Web server fundamentals (master/worker, event-driven); reverse proxy; forward vs reverse proxy; load balancing (algorithms, health checks passive); HTTP and HTTPS; TLS termination; static file serving; upstream servers; proxy headers; WebSocket proxying; caching (proxy_cache); rate limiting; compression (gzip); request size limits (413); timeouts; logging; configuration blocks (main/http/server/location, location matching order); troubleshooting 502 and 504; NGINX with Node.js; NGINX with Docker; deployment architecture; SPA fallback; HTTP/2 `http2 on;` syntax.

## aws — AWS
Cloud computing (IaaS/PaaS/SaaS, shared responsibility); Regions and AZs; IAM users, roles, policies; EC2; S3; RDS; VPC; security groups (vs NACLs); load balancers (ALB/NLB); Auto Scaling; Route 53; CloudFront; Lambda; API Gateway; CloudWatch; ECS and ECR fundamentals; Secrets Manager; SSM Parameter Store; least-privilege IAM; deployment strategies (blue/green, rolling, canary); backups and disaster recovery (RPO/RTO strategies); cost optimization; high availability; security; monitoring; basic architecture design. Distinguish junior deployment questions (deploy a Node app on EC2 with NGINX + PM2, S3 static hosting) from advanced architecture questions.
