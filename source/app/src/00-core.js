/*!
 * Interview Prep BD — bilingual technical interview preparation platform
 * Vanilla JavaScript, no build step. Data: questions.js (window.QBANK).
 * Content verified against official sources on 2026-10-12.
 */
(function () {
  'use strict';

  /* ======================================================================
     Constants
     ====================================================================== */
  const APP_VERSION = '1.0.0';
  const STORAGE_KEY = 'ipbd:state';
  const STORAGE_VERSION = 1;
  const VERIFIED_AT = '2026-10-12';
  const DIFFS = ['easy', 'medium', 'hard', 'extreme'];
  const POINTS = { easy: 1, medium: 2, hard: 3, extreme: 4 };
  const TYPES = ['conceptual', 'output', 'coding', 'debugging', 'scenario', 'comparison', 'system-design', 'query', 'architecture', 'security-performance', 'mcq', 'quick', 'behavioral'];
  const SHORT_TYPES = ['quick', 'behavioral']; // the answer itself is short; no separate quick answer
  const MARKETS = ['both', 'bangladesh', 'international'];
  const PRIORITIES = ['high', 'medium', 'low'];
  const RESULTS = ['correct', 'partial', 'incorrect', 'skipped'];
  const RESULT_FACTOR = { correct: 1, partial: 0.5, incorrect: 0, skipped: 0 };
  const REVIEW_INTERVALS = [1, 3, 7, 14, 30]; // days, by review box
  const DAY = 86400000;
  const PAGE_SIZE = 20;

  const TECHS = [
    { id: 'html', name: 'HTML', short: 'H', color: '#FB7A56', group: 'frontend', version: 'HTML Living Standard', docs: 'https://developer.mozilla.org/en-US/docs/Web/HTML',
      desc: { en: 'Semantic markup, forms, accessibility, SEO, script loading and how browsers parse documents.', bn: 'Semantic markup, form, accessibility, SEO, script loading এবং browser কীভাবে document parse করে।' } },
    { id: 'css', name: 'CSS', short: 'C', color: '#5AA9FF', group: 'frontend', version: 'CSS Baseline (2026)', docs: 'https://developer.mozilla.org/en-US/docs/Web/CSS',
      desc: { en: 'Cascade, specificity, Flexbox, Grid, container queries, animation and layout debugging.', bn: 'Cascade, specificity, Flexbox, Grid, container query, animation এবং layout debugging।' } },
    { id: 'javascript', name: 'JavaScript', short: 'JS', color: '#F7DF4E', group: 'frontend', version: 'ECMAScript 2026', docs: 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
      desc: { en: 'Closures, this, prototypes, the event loop, async patterns, output prediction and coding problems.', bn: 'Closure, this, prototype, event loop, async pattern, output prediction এবং coding problem।' } },
    { id: 'react', name: 'React', short: 'Re', color: '#61DAFB', group: 'frontend', version: 'React 19.3', docs: 'https://react.dev/reference/react',
      desc: { en: 'Hooks, rendering, reconciliation, Server Components, Actions, performance and debugging.', bn: 'Hook, rendering, reconciliation, Server Component, Action, performance এবং debugging।' } },
    { id: 'nextjs', name: 'Next.js', short: 'Nx', color: '#E5E7EB', group: 'frontend', version: 'Next.js 16.4', docs: 'https://nextjs.org/docs',
      desc: { en: 'App Router, rendering strategies, Cache Components, Server Actions, proxy.ts and deployment.', bn: 'App Router, rendering strategy, Cache Components, Server Action, proxy.ts এবং deployment।' } },
    { id: 'reactnative', name: 'React Native', short: 'RN', color: '#4FC3F7', group: 'mobile', version: 'React Native 0.88 · Expo SDK 58', docs: 'https://reactnative.dev/docs/getting-started',
      desc: { en: 'Core components, styling, lists, Expo Router navigation, storage with expo-sqlite, EAS builds and OTA updates, performance and the New Architecture.', bn: 'Core component, styling, list, Expo Router navigation, expo-sqlite দিয়ে storage, EAS build ও OTA update, performance আর New Architecture।' } },
    { id: 'nodejs', name: 'Node.js', short: 'No', color: '#7CC66A', group: 'backend', version: 'Node.js 26 LTS · 24 Maintenance', docs: 'https://nodejs.org/docs/latest/api/',
      desc: { en: 'V8, libuv, the event loop, streams, workers, modules, error handling and scalability.', bn: 'V8, libuv, event loop, stream, worker, module, error handling এবং scalability।' } },
    { id: 'express', name: 'Express.js', short: 'Ex', color: '#C9D1D9', group: 'backend', version: 'Express 5.3', docs: 'https://expressjs.com/',
      desc: { en: 'Routing, middleware, REST APIs, auth, validation, security headers and error handling.', bn: 'Routing, middleware, REST API, auth, validation, security header এবং error handling।' } },
    { id: 'nestjs', name: 'NestJS', short: 'Ns', color: '#F0506E', group: 'backend', version: 'NestJS 12.1', docs: 'https://docs.nestjs.com/',
      desc: { en: 'Modules, DI, pipes, guards, interceptors, request lifecycle and architecture.', bn: 'Module, DI, pipe, guard, interceptor, request lifecycle এবং architecture।' } },
    { id: 'mongodb', name: 'MongoDB', short: 'Mg', color: '#4DB33D', group: 'database', version: 'MongoDB 9.0', docs: 'https://www.mongodb.com/docs/manual/',
      desc: { en: 'Documents, aggregation, indexing, schema design, transactions, replication and sharding.', bn: 'Document, aggregation, indexing, schema design, transaction, replication এবং sharding।' } },
    { id: 'mongoose', name: 'Mongoose', short: 'Ms', color: '#D9534F', group: 'database', version: 'Mongoose 9.11', docs: 'https://mongoosejs.com/docs/',
      desc: { en: 'Schemas, validation, middleware, populate, lean queries and transactions.', bn: 'Schema, validation, middleware, populate, lean query এবং transaction।' } },
    { id: 'postgresql', name: 'PostgreSQL', short: 'Pg', color: '#6C9BD2', group: 'database', version: 'PostgreSQL 18', docs: 'https://www.postgresql.org/docs/current/',
      desc: { en: 'MVCC, isolation levels, indexing, EXPLAIN, JSONB, locks, replication and tuning.', bn: 'MVCC, isolation level, indexing, EXPLAIN, JSONB, lock, replication এবং tuning।' } },
    { id: 'sql', name: 'SQL', short: 'SQL', color: '#F2A93B', group: 'database', version: 'SQL:2023 · PostgreSQL dialect', docs: 'https://www.postgresql.org/docs/current/sql.html',
      desc: { en: 'Joins, grouping, subqueries, CTEs, window functions and practical query writing.', bn: 'Join, grouping, subquery, CTE, window function এবং practical query writing।' } },
    { id: 'drizzle', name: 'Drizzle ORM', short: 'Dz', color: '#C5F74F', group: 'database', version: 'Drizzle 0.45 (v1 RC)', docs: 'https://orm.drizzle.team/docs/overview',
      desc: { en: 'Type-safe schemas, queries, relations, migrations with Drizzle Kit and transactions.', bn: 'Type-safe schema, query, relation, Drizzle Kit দিয়ে migration এবং transaction।' } },
    { id: 'redis', name: 'Redis', short: 'Rd', color: '#FF6B5B', group: 'database', version: 'Redis 8.10', docs: 'https://redis.io/docs/latest/',
      desc: { en: 'Data structures, caching patterns, rate limiting, streams, persistence and locks.', bn: 'Data structure, caching pattern, rate limiting, stream, persistence এবং lock।' } },
    { id: 'vectordb', name: 'Vector Databases', short: 'Vec', color: '#B794F6', group: 'ai', version: 'Concepts · pgvector 0.8', docs: 'https://github.com/pgvector/pgvector',
      desc: { en: 'Embeddings, similarity search, ANN indexes, hybrid search and RAG basics.', bn: 'Embedding, similarity search, ANN index, hybrid search এবং RAG-এর মৌলিক ধারণা।' } },
    { id: 'docker', name: 'Docker', short: 'Dk', color: '#3BA4F6', group: 'devops', version: 'Engine 29 · Compose v5', docs: 'https://docs.docker.com/',
      desc: { en: 'Images, Dockerfiles, layers, volumes, networks, Compose and production practices.', bn: 'Image, Dockerfile, layer, volume, network, Compose এবং production practice।' } },
    { id: 'nginx', name: 'NGINX', short: 'Ng', color: '#3FBF7F', group: 'devops', version: 'NGINX 1.30 stable', docs: 'https://nginx.org/en/docs/',
      desc: { en: 'Reverse proxy, load balancing, TLS, caching, rate limiting and 502/504 debugging.', bn: 'Reverse proxy, load balancing, TLS, caching, rate limiting এবং 502/504 debugging।' } },
    { id: 'aws', name: 'AWS', short: 'AWS', color: '#FF9F2E', group: 'devops', version: 'Current AWS services', docs: 'https://docs.aws.amazon.com/',
      desc: { en: 'IAM, EC2, S3, RDS, VPC, load balancing, Lambda, monitoring and architecture.', bn: 'IAM, EC2, S3, RDS, VPC, load balancing, Lambda, monitoring এবং architecture।' } },
    { id: 'behavioral', name: 'Behavioural & Projects', short: 'HR', color: '#F59EBF', group: 'career', version: 'Interview skills', docs: '',
      desc: { en: 'Introducing yourself, walking through your projects, teamwork, mistakes, pressure and the questions to ask back.', bn: 'নিজের পরিচয়, নিজের project ব্যাখ্যা, teamwork, ভুল, চাপ সামলানো আর interviewer-কে কী প্রশ্ন করবে।' } },
  ];
  const TECH_MAP = new Map(TECHS.map((t) => [t.id, t]));
  const TECH_GROUPS = ['frontend', 'mobile', 'backend', 'database', 'devops', 'ai', 'career'];

  /* Verified version table (shown on the Versions & Sources page) */
  const VERSIONS = [
    { tech: 'HTML', version: 'HTML Living Standard (WHATWG)', note: 'Browser support via Baseline (web-features 3.42.0).', url: 'https://html.spec.whatwg.org/multipage/' },
    { tech: 'CSS', version: 'Baseline 2026', note: 'Container queries, :has(), nesting, @layer widely available; @scope, container style queries newly available; anchor positioning not yet Baseline.', url: 'https://web-platform-dx.github.io/web-features/' },
    { tech: 'JavaScript', version: 'ECMAScript 2026 (approved 2026-06-30)', note: 'Math.sumPrecise, Iterator.concat, Error.isError, Map upsert, Uint8Array base64/hex, JSON.rawJSON.', url: 'https://tc39.es/ecma262/' },
    { tech: 'React', version: '19.3.0', note: 'Stable <ViewTransition>, Fragment refs, browser(); React Compiler 1.0.', url: 'https://react.dev/blog' },
    { tech: 'Next.js', version: '16.4.0', note: 'Cache Components recommended (default for new apps), proxy.ts replaces middleware.ts, Turbopack default. Next 17 not yet released.', url: 'https://nextjs.org/blog/next-16-4' },
    { tech: 'React Native', version: '0.88.0 (React 19.3) · Expo SDK 58', note: 'New Architecture only since 0.82; Hermes V1 default since 0.84. Expo SDK 58 bundles RN 0.88; libSQL support removed from expo-sqlite. Checked 2026-10-26.', url: 'https://reactnative.dev/blog' },
    { tech: 'Node.js', version: '26.12.1 (Active LTS from 2026-10-28) · 24.22.1 (Maintenance LTS "Krypton")', note: 'v24 entered Maintenance on 2026-10-20 (EOL 2028-04-30); v22 Maintenance LTS until 2027-04-30; annual releases from v27 (alpha from 2026-10-28). Re-checked 2026-10-26.', url: 'https://nodejs.org/en/about/previous-releases' },
    { tech: 'Express', version: '5.3.0', note: 'Express 5 is the npm default; Node.js 18+.', url: 'https://expressjs.com/en/guide/migrating-5.html' },
    { tech: 'NestJS', version: '12.2.0 (content written against 12.1)', note: 'ESM core packages, Standard Schema validation, Node 20.19+/22.12+.', url: 'https://docs.nestjs.com/' },
    { tech: 'MongoDB', version: '9.0 (server) · Node driver 7.7', note: '9.0.0 released 2026-09-28.', url: 'https://www.mongodb.com/docs/manual/release-notes/9.0/' },
    { tech: 'Mongoose', version: '9.11.1', note: 'Pre hooks without next(), promise-only APIs, Node 20.19+.', url: 'https://mongoosejs.com/docs/migrating_to_9.html' },
    { tech: 'PostgreSQL', version: '18 (18.6) · 19 in beta', note: 'uuidv7(), virtual generated columns, skip scan, AIO, OLD/NEW in RETURNING.', url: 'https://www.postgresql.org/docs/release/18.0/' },
    { tech: 'SQL', version: 'ISO SQL:2023 (portable) + PostgreSQL 18 dialect', note: 'PostgreSQL-specific syntax is labelled in answers.', url: 'https://www.postgresql.org/docs/current/sql.html' },
    { tech: 'Drizzle ORM', version: '0.45.4 stable · drizzle-kit 0.31.11', note: 'v1.0 is still a release candidate (npm rc tag) — treated as preview.', url: 'https://orm.drizzle.team/docs/overview' },
    { tech: 'Redis', version: 'Redis Open Source 8.10 (8.10.2)', note: 'node-redis 6.3, ioredis 6.0. 8.2 is the extended-support line.', url: 'https://redis.io/docs/latest/operate/oss_and_stack/install/version-mgmt/' },
    { tech: 'Vector DB', version: 'Concepts · pgvector 0.8.7', note: 'Product-neutral fundamentals; pgvector used for concrete examples.', url: 'https://github.com/pgvector/pgvector' },
    { tech: 'Docker', version: 'Engine 29.9.0 · Compose v5.6.0', note: 'compose.yaml without top-level version; BuildKit default.', url: 'https://docs.docker.com/engine/release-notes/' },
    { tech: 'NGINX', version: '1.30.5 stable · 1.31.6 mainline', note: '`http2 on;` directive; upstream keepalive on by default since 1.29.7; even minor = stable branch.', url: 'https://nginx.org/en/download.html' },
    { tech: 'AWS', version: 'Current services (Oct 2026)', note: 'Lambda nodejs24.x GA; Amazon Linux 2 end of support 2026-06-30; SDK for JavaScript v3.', url: 'https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html' },
  ];

  /* Research sources used to plan the question bank */
  const SOURCES = [
    { group: 'versions', title: 'npm registry dist-tags (react, next, express, @nestjs/core, mongoose, mongodb, drizzle-orm, redis, ioredis)', url: 'https://www.npmjs.com/' },
    { group: 'versions', title: 'Node.js — Previous releases & release schedule', url: 'https://nodejs.org/en/about/previous-releases' },
    { group: 'versions', title: 'React Blog — React 19.3 (2026-09-09)', url: 'https://react.dev/blog/2026/09/09/react-19-3' },
    { group: 'versions', title: 'Next.js Blog — Next.js 16', url: 'https://nextjs.org/blog/next-16' },
    { group: 'versions', title: 'Next.js Blog — Next.js 16.4', url: 'https://nextjs.org/blog/next-16-4' },
    { group: 'versions', title: 'Express blog feed & migration guide', url: 'https://expressjs.com/en/guide/migrating-5.html' },
    { group: 'versions', title: 'MongoDB 9.0 release notes', url: 'https://www.mongodb.com/docs/manual/release-notes/9.0/' },
    { group: 'versions', title: 'MongoDB versions & upgrade paths', url: 'https://www.mongodb.com/docs/mongodb-versions/' },
    { group: 'versions', title: 'Migrating to Mongoose 9', url: 'https://mongoosejs.com/docs/migrating_to_9.html' },
    { group: 'versions', title: 'PostgreSQL 18 release notes', url: 'https://www.postgresql.org/docs/release/18.0/' },
    { group: 'versions', title: 'PostgreSQL news (19 Beta 4, minor releases)', url: 'https://www.postgresql.org/' },
    { group: 'versions', title: 'Drizzle — v0 to v1 changes', url: 'https://orm.drizzle.team/docs/v0-v1-changes' },
    { group: 'versions', title: 'Redis Open Source version management', url: 'https://redis.io/docs/latest/operate/oss_and_stack/install/version-mgmt/' },
    { group: 'versions', title: 'pgvector changelog', url: 'https://pgxn.org/dist/vector/CHANGELOG.html' },
    { group: 'versions', title: 'Docker Engine release notes', url: 'https://docs.docker.com/engine/release-notes/' },
    { group: 'versions', title: 'Docker Compose releases', url: 'https://github.com/docker/compose/releases' },
    { group: 'versions', title: 'NGINX download page (stable/mainline)', url: 'https://nginx.org/en/download.html' },
    { group: 'versions', title: 'AWS Lambda runtimes', url: 'https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html' },
    { group: 'versions', title: 'Node.js — TypeScript type stripping', url: 'https://nodejs.org/api/typescript.html' },
    { group: 'versions', title: 'ECMAScript 2026 approval (InfoWorld)', url: 'https://www.infoworld.com/article/4193461/ecmascript-2026-specification-approved.html' },
    { group: 'versions', title: 'web-features / Baseline data (v3.42.0)', url: 'https://web-platform-dx.github.io/web-features/' },
    { group: 'market', title: 'Stack Overflow Developer Survey 2025 — Technology', url: 'https://survey.stackoverflow.co/2025/technology' },
    { group: 'market', title: 'JavaScript interview questions for the job market in Bangladesh (DEV Community)', url: 'https://dev.to/engrsakib/javascript-interview-questions-and-answers-for-the-job-market-in-bangladesh-a05' },
    { group: 'market', title: 'Brain Station 23 interview reviews (Glassdoor)', url: 'https://www.glassdoor.com.br/Entrevista/Brain-Station-23-Entrevista-E580909-RVW88806366.htm' },
    { group: 'market', title: 'Example Bangladesh full-stack (MERN + NestJS) job post, 2026 (LinkedIn)', url: 'https://bd.linkedin.com/in/nimur-hasan' },
    { group: 'docs', title: 'MDN Web Docs', url: 'https://developer.mozilla.org/' },
    { group: 'docs', title: 'React documentation', url: 'https://react.dev/' },
    { group: 'docs', title: 'Next.js documentation', url: 'https://nextjs.org/docs' },
    { group: 'docs', title: 'Node.js API documentation', url: 'https://nodejs.org/api/' },
    { group: 'docs', title: 'Express documentation', url: 'https://expressjs.com/' },
    { group: 'docs', title: 'NestJS documentation', url: 'https://docs.nestjs.com/' },
    { group: 'docs', title: 'MongoDB manual', url: 'https://www.mongodb.com/docs/manual/' },
    { group: 'docs', title: 'Mongoose documentation', url: 'https://mongoosejs.com/docs/' },
    { group: 'docs', title: 'PostgreSQL documentation', url: 'https://www.postgresql.org/docs/current/' },
    { group: 'docs', title: 'Drizzle ORM documentation', url: 'https://orm.drizzle.team/docs/overview' },
    { group: 'docs', title: 'Redis documentation', url: 'https://redis.io/docs/latest/' },
    { group: 'docs', title: 'Docker documentation', url: 'https://docs.docker.com/' },
    { group: 'docs', title: 'NGINX documentation', url: 'https://nginx.org/en/docs/' },
    { group: 'docs', title: 'AWS documentation', url: 'https://docs.aws.amazon.com/' },
    { group: 'docs', title: 'OWASP Cheat Sheet Series', url: 'https://cheatsheetseries.owasp.org/' },
  ];

  /* ======================================================================
     DOM helpers (safe: text is always set via textContent / createTextNode)
     ====================================================================== */
  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  function h(tag, props) {
    const el = document.createElement(tag);
    if (props) {
      for (const key of Object.keys(props)) {
        const v = props[key];
        if (v == null || v === false) continue;
        if (key === 'class') el.className = v;
        else if (key === 'text') el.textContent = v;
        else if (key === 'style' && typeof v === 'object') Object.assign(el.style, v);
        else if (key === 'dataset') Object.assign(el.dataset, v);
        else if (key.startsWith('on') && typeof v === 'function') el.addEventListener(key.slice(2).toLowerCase(), v);
        else if (key === 'value') el.value = v;
        else if (key === 'checked') el.checked = !!v;
        else if (v === true) el.setAttribute(key, '');
        else el.setAttribute(key, String(v));
      }
    }
    for (let i = 2; i < arguments.length; i++) append(el, arguments[i]);
    return el;
  }
  function append(el, child) {
    if (child == null || child === false || child === true) return el;
    if (Array.isArray(child)) { for (const c of child) append(el, c); return el; }
    el.append(child instanceof Node ? child : document.createTextNode(String(child)));
    return el;
  }
  function frag() { const f = document.createDocumentFragment(); for (const c of arguments) append(f, c); return f; }
  function clear(el) { while (el.firstChild) el.removeChild(el.firstChild); return el; }

  const SVG_NS = 'http://www.w3.org/2000/svg';
  const ICONS = {
    dashboard: 'M3 3h7v9H3z M14 3h7v5h-7z M14 12h7v9h-7z M3 16h7v5H3z',
    layers: 'M12 2 2 7l10 5 10-5-10-5z M2 17l10 5 10-5 M2 12l10 5 10-5',
    list: 'M8 6h13 M8 12h13 M8 18h13 M3.5 6h.01 M3.5 12h.01 M3.5 18h.01',
    play: 'M7 4.5v15l12-7.5z',
    mic: 'M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z M19 10v2a7 7 0 0 1-14 0v-2 M12 19v3',
    bookmark: 'M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z',
    xcircle: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M15 9l-6 6 M9 9l6 6',
    rotate: 'M3 12a9 9 0 1 0 3-6.7L3 8 M3 3v5h5',
    clock: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M12 6v6l4 2',
    calendar: 'M8 2v4 M16 2v4 M3 10h18 M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z',
    settings: 'M4 21v-7 M4 10V3 M12 21v-9 M12 8V3 M20 21v-5 M20 12V3 M1 14h6 M9 8h6 M17 16h6',
    cards: 'M7 3h12a2 2 0 0 1 2 2v12 M3 7h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z',
    zap: 'M13 2 3 14h9l-1 8 10-12h-9l1-8z',
    book: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20 M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z',
    search: 'M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z M21 21l-4.35-4.35',
    chevL: 'M15 18l-6-6 6-6',
    chevR: 'M9 18l6-6-6-6',
    arrowL: 'M19 12H5 M12 19l-7-7 7-7',
    arrowR: 'M5 12h14 M12 5l7 7-7 7',
    check: 'M20 6 9 17l-5-5',
    checkCircle: 'M22 11.08V12a10 10 0 1 1-5.93-9.14 M22 4 12 14.01l-3-3',
    half: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M12 2v20',
    skip: 'M5 4l10 8-10 8z M19 5v14',
    flag: 'M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z M4 22v-7',
    sun: 'M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10z M12 1v2 M12 21v2 M4.22 4.22l1.42 1.42 M18.36 18.36l1.42 1.42 M1 12h2 M21 12h2 M4.22 19.78l1.42-1.42 M18.36 5.64l1.42-1.42',
    moon: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z',
    globe: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M2 12h20 M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z',
    external: 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6 M15 3h6v6 M10 14 21 3',
    trash: 'M3 6h18 M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6 M10 11v6 M14 11v6 M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2',
    download: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4 M7 10l5 5 5-5 M12 15V3',
    upload: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4 M17 8l-5-5-5 5 M12 3v12',
    flame: 'M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z',
    target: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12z M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z',
    trophy: 'M6 9H4.5a2.5 2.5 0 0 1 0-5H6 M18 9h1.5a2.5 2.5 0 0 0 0-5H18 M4 22h16 M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22 M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22 M18 2H6v7a6 6 0 0 0 12 0V2z',
    info: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z M12 16v-4 M12 8h.01',
    alert: 'M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z M12 9v4 M12 17h.01',
    eye: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z',
    bulb: 'M9 18h6 M10 22h4 M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z',
    code: 'M16 18l6-6-6-6 M8 6l-6 6 6 6',
    message: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z',
    link: 'M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71 M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71',
    grad: 'M22 10 12 5 2 10l10 5 10-5z M6 12v5c3 3 9 3 12 0v-5',
    x: 'M18 6 6 18 M6 6l12 12',
    copy: 'M20 9h-9a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2z M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1',
    shuffle: 'M16 3h5v5 M4 20 21 3 M21 16v5h-5 M15 15l6 6 M4 4l5 5',
    filter: 'M22 3H2l8 9.46V19l4 2v-8.54L22 3z',
    shield: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',
    star: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
    database: 'M12 8c4.97 0 9-1.34 9-3s-4.03-3-9-3-9 1.34-9 3 4.03 3 9 3z M21 12c0 1.66-4 3-9 3s-9-1.34-9-3 M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5',
    stop: 'M6 6h12v12H6z',
    article: 'M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z M7 8h10 M7 12h10 M7 16h6',
    keyboard: 'M20 5H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2z M6 9h.01 M10 9h.01 M14 9h.01 M18 9h.01 M7 15h10',
  };
  function icon(name, size) {
    const s = size || 18;
    const svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('width', s);
    svg.setAttribute('height', s);
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    const p = document.createElementNS(SVG_NS, 'path');
    p.setAttribute('d', ICONS[name] || ICONS.info);
    p.setAttribute('fill', 'none');
    p.setAttribute('stroke', 'currentColor');
    p.setAttribute('stroke-width', '2');
    p.setAttribute('stroke-linecap', 'round');
    p.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(p);
    return svg;
  }

  /* ======================================================================
     Small utilities
     ====================================================================== */
  const clamp = (n, a, b) => Math.max(a, Math.min(b, n));
  const uid = (p) => (p || 'id') + '-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 7);
  const isObj = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
  const isStr = (v) => typeof v === 'string';
  const sum = (arr, fn) => arr.reduce((a, x) => a + (fn ? fn(x) : x), 0);

  function localDateKey(d) {
    const dt = d instanceof Date ? d : new Date(d == null ? Date.now() : d);
    const m = String(dt.getMonth() + 1).padStart(2, '0');
    const day = String(dt.getDate()).padStart(2, '0');
    return dt.getFullYear() + '-' + m + '-' + day;
  }
  function startOfDay(ts) { const d = new Date(ts == null ? Date.now() : ts); d.setHours(0, 0, 0, 0); return d.getTime(); }
  function addDays(ts, n) { const d = new Date(ts); d.setDate(d.getDate() + n); return d.getTime(); }

  function hashString(str) {
    let h1 = 2166136261 >>> 0;
    for (let i = 0; i < str.length; i++) { h1 ^= str.charCodeAt(i); h1 = Math.imul(h1, 16777619); }
    return h1 >>> 0;
  }
  function mulberry32(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function shuffle(arr, rnd) {
    const a = arr.slice();
    const r = rnd || Math.random;
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }
  function debounce(fn, ms) {
    let tm = null;
    return function () { const args = arguments; clearTimeout(tm); tm = setTimeout(() => fn.apply(null, args), ms); };
  }
  function normalizeText(s) {
    try { return String(s || '').normalize('NFC').toLowerCase(); } catch (e) { return String(s || '').toLowerCase(); }
  }
