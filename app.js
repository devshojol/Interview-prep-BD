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
  const TYPES = ['conceptual', 'output', 'coding', 'debugging', 'scenario', 'comparison', 'system-design', 'query', 'architecture', 'security-performance', 'mcq'];
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
    { id: 'nodejs', name: 'Node.js', short: 'No', color: '#7CC66A', group: 'backend', version: 'Node.js 24 LTS · 26 Current', docs: 'https://nodejs.org/docs/latest/api/',
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
  ];
  const TECH_MAP = new Map(TECHS.map((t) => [t.id, t]));
  const TECH_GROUPS = ['frontend', 'backend', 'database', 'devops', 'ai'];

  /* Verified version table (shown on the Versions & Sources page) */
  const VERSIONS = [
    { tech: 'HTML', version: 'HTML Living Standard (WHATWG)', note: 'Browser support via Baseline (web-features 3.42.0).', url: 'https://html.spec.whatwg.org/multipage/' },
    { tech: 'CSS', version: 'Baseline 2026', note: 'Container queries, :has(), nesting, @layer widely available; @scope, container style queries newly available; anchor positioning not yet Baseline.', url: 'https://web-platform-dx.github.io/web-features/' },
    { tech: 'JavaScript', version: 'ECMAScript 2026 (approved 2026-06-30)', note: 'Math.sumPrecise, Iterator.concat, Error.isError, Map upsert, Uint8Array base64/hex, JSON.rawJSON.', url: 'https://tc39.es/ecma262/' },
    { tech: 'React', version: '19.3.0', note: 'Stable <ViewTransition>, Fragment refs, browser(); React Compiler 1.0.', url: 'https://react.dev/blog' },
    { tech: 'Next.js', version: '16.4.0', note: 'Cache Components recommended (default for new apps), proxy.ts replaces middleware.ts, Turbopack default. Next 17 not yet released.', url: 'https://nextjs.org/blog/next-16-4' },
    { tech: 'Node.js', version: '24.21.0 (Active LTS "Krypton") · 26.11.1 (Current)', note: 'v26 becomes LTS on 2026-10-28; v22 Maintenance LTS until 2027-04-30; annual releases from v27.', url: 'https://nodejs.org/en/about/previous-releases' },
    { tech: 'Express', version: '5.3.0', note: 'Express 5 is the npm default; Node.js 18+.', url: 'https://expressjs.com/en/guide/migrating-5.html' },
    { tech: 'NestJS', version: '12.1.3', note: 'ESM core packages, Standard Schema validation, Node 20.19+/22.12+.', url: 'https://docs.nestjs.com/' },
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

  /* ======================================================================
     Question bank: normalisation, validation, indexing, search
     ====================================================================== */
  function biObj(v) {
    if (isStr(v)) return { en: v, bn: '' };
    if (!isObj(v)) return { en: '', bn: '' };
    return { en: isStr(v.en) ? v.en : '', bn: isStr(v.bn) ? v.bn : '' };
  }
  function codeObj(v) {
    if (!isObj(v)) return null;
    const source = isStr(v.source) ? v.source : '';
    const output = isStr(v.output) ? v.output : '';
    if (!source && !output) return null;
    return { language: isStr(v.language) ? v.language : 'text', source, output };
  }

  function normalizeQuestion(raw) {
    if (!isObj(raw) || !isStr(raw.id) || !raw.id) return null;
    const q = {
      id: raw.id,
      technology: TECH_MAP.has(raw.technology) ? raw.technology : null,
      subtopic: isStr(raw.subtopic) ? raw.subtopic : 'General',
      difficulty: DIFFS.includes(raw.difficulty) ? raw.difficulty : 'medium',
      type: TYPES.includes(raw.type) ? raw.type : 'conceptual',
      market: MARKETS.includes(raw.market) ? raw.market : 'both',
      priority: PRIORITIES.includes(raw.priority) ? raw.priority : 'medium',
      estimatedMinutes: Number.isFinite(raw.estimatedMinutes) ? clamp(Math.round(raw.estimatedMinutes), 1, 60) : 3,
      tags: Array.isArray(raw.tags) ? raw.tags.filter(isStr) : [],
      technologyVersion: isStr(raw.technologyVersion) ? raw.technologyVersion : 'Version-independent concept',
      verifiedAt: isStr(raw.verifiedAt) ? raw.verifiedAt : '',
      versionSensitive: raw.versionSensitive === true,
      status: isStr(raw.status) ? raw.status : 'stable',
      question: biObj(raw.question),
      answer: biObj(raw.answer),
      explanation: biObj(raw.explanation),
      interviewTip: biObj(raw.interviewTip),
      commonMistakes: raw.commonMistakes ? biObj(raw.commonMistakes) : null,
      code: codeObj(raw.code),
      setup: codeObj(raw.setup),
      extraCode: Array.isArray(raw.extraCode)
        ? raw.extraCode.filter(isObj).map((x) => ({ language: isStr(x.language) ? x.language : 'text', source: isStr(x.source) ? x.source : '', label: biObj(x.label) })).filter((x) => x.source)
        : [],
      followUps: Array.isArray(raw.followUps) ? raw.followUps.map(biObj).filter((f) => f.en || f.bn) : [],
      related: Array.isArray(raw.related) ? raw.related.filter(isStr) : [],
      references: Array.isArray(raw.references)
        ? raw.references.filter((r) => isObj(r) && isStr(r.url) && /^https:\/\//.test(r.url)).map((r) => ({ title: isStr(r.title) && r.title ? r.title : r.url, url: r.url }))
        : [],
      options: Array.isArray(raw.options) ? raw.options.map(biObj) : null,
      correctIndex: Number.isInteger(raw.correctIndex) ? raw.correctIndex : null,
      complexity: isObj(raw.complexity) ? { time: String(raw.complexity.time || ''), space: String(raw.complexity.space || '') } : null,
    };
    q.documentationUrl = isStr(raw.documentationUrl) && raw.documentationUrl ? raw.documentationUrl : (q.references[0] ? q.references[0].url : (TECH_MAP.get(q.technology) || {}).docs || '');
    q.isMCQ = q.type === 'mcq' && Array.isArray(q.options) && q.options.length >= 2 && q.correctIndex != null && q.correctIndex >= 0 && q.correctIndex < q.options.length;
    if (q.type === 'mcq' && !q.isMCQ) q.type = 'conceptual'; // malformed MCQ degrades gracefully
    return q;
  }

  /* Development-time validator: reports problems in the console, never throws. */
  function validateBank(rawList) {
    const errors = [];
    const warnings = [];
    const ids = new Map();
    const list = Array.isArray(rawList) ? rawList : [];
    if (!Array.isArray(rawList)) errors.push('window.QBANK is missing or not an array.');
    const BN = /[ঀ-৿]/;
    list.forEach((q, i) => {
      const where = (q && q.id) ? q.id : ('#' + i);
      if (!isObj(q)) { errors.push(where + ': record is not an object'); return; }
      if (!isStr(q.id) || !q.id) errors.push(where + ': missing id');
      else ids.set(q.id, (ids.get(q.id) || 0) + 1);
      if (!TECH_MAP.has(q.technology)) errors.push(where + ': unknown technology "' + q.technology + '"');
      if (!DIFFS.includes(q.difficulty)) errors.push(where + ': invalid difficulty "' + q.difficulty + '"');
      if (!TYPES.includes(q.type)) errors.push(where + ': invalid type "' + q.type + '"');
      if (!MARKETS.includes(q.market)) errors.push(where + ': invalid market "' + q.market + '"');
      ['question', 'answer', 'explanation'].forEach((f) => {
        const o = q[f];
        if (!isObj(o) || !o.en) errors.push(where + ': missing English ' + f);
        if (!isObj(o) || !o.bn) errors.push(where + ': missing Bangla ' + f);
        else if (!BN.test(o.bn)) warnings.push(where + ': Bangla ' + f + ' contains no Bangla characters');
      });
      if (!isObj(q.interviewTip) || !q.interviewTip.en || !q.interviewTip.bn) warnings.push(where + ': interview tip missing a language');
      if (!isStr(q.technologyVersion) || !q.technologyVersion) errors.push(where + ': missing technologyVersion');
      if (q.versionSensitive && !/\d/.test(q.technologyVersion || '')) errors.push(where + ': versionSensitive but technologyVersion has no version number');
      if (!isStr(q.verifiedAt) || !/^\d{4}-\d{2}-\d{2}$/.test(q.verifiedAt)) warnings.push(where + ': missing/invalid verifiedAt');
      if (!Array.isArray(q.references) || !q.references.length) warnings.push(where + ': no documentation references');
      if (q.type === 'mcq') {
        if (!Array.isArray(q.options) || q.options.length !== 4) errors.push(where + ': MCQ must have 4 options');
        else q.options.forEach((o, k) => { if (!isObj(o) || !o.en || !o.bn) errors.push(where + ': MCQ option ' + k + ' missing a language'); });
        if (!Number.isInteger(q.correctIndex) || !q.options || q.correctIndex < 0 || q.correctIndex >= q.options.length) errors.push(where + ': MCQ correctIndex does not reference an option');
      }
      if (q.type === 'output' && !(isObj(q.code) && q.code.output)) errors.push(where + ': output question without expected output');
    });
    for (const [id, n] of ids) if (n > 1) errors.push(id + ': duplicate id (' + n + ' records)');
    list.forEach((q) => {
      if (isObj(q) && Array.isArray(q.related)) q.related.forEach((r) => { if (!ids.has(r)) errors.push(q.id + ': broken related reference "' + r + '"'); });
    });
    return { errors, warnings, total: list.length };
  }

  const RAW_BANK = Array.isArray(window.QBANK) ? window.QBANK : [];
  const VALIDATION = validateBank(window.QBANK);
  const QUESTIONS = [];
  const QMAP = new Map();
  for (const raw of RAW_BANK) {
    let q = null;
    try { q = normalizeQuestion(raw); } catch (e) { q = null; }
    if (!q || !q.technology || QMAP.has(q.id)) continue;
    QUESTIONS.push(q);
    QMAP.set(q.id, q);
  }
  // Stable display order: technology order, then difficulty, then id
  const TECH_ORDER = new Map(TECHS.map((t, i) => [t.id, i]));
  QUESTIONS.sort((a, b) => (TECH_ORDER.get(a.technology) - TECH_ORDER.get(b.technology)) || (DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty)) || a.id.localeCompare(b.id, 'en', { numeric: true }));
  QUESTIONS.forEach((q, i) => {
    q._order = i;
    const t = TECH_MAP.get(q.technology);
    q._sTitle = normalizeText(q.question.en + ' \n ' + q.question.bn);
    q._sMeta = normalizeText([q.subtopic, q.tags.join(' '), q.id, t ? t.name : '', q.type].join(' '));
    q._sBody = normalizeText([q.answer.en, q.answer.bn, q.explanation.en, q.explanation.bn].join(' '));
  });
  const BY_TECH = new Map(TECHS.map((t) => [t.id, []]));
  QUESTIONS.forEach((q) => BY_TECH.get(q.technology).push(q));

  function logValidation() {
    try {
      const v = VALIDATION;
      const label = '[Interview Prep BD] Question bank validation: ' + QUESTIONS.length + ' usable / ' + v.total + ' records, ' + v.errors.length + ' errors, ' + v.warnings.length + ' warnings';
      if (v.errors.length || v.warnings.length) {
        console.groupCollapsed(label);
        v.errors.forEach((e) => console.error(e));
        v.warnings.forEach((w) => console.warn(w));
        console.groupEnd();
      } else {
        console.info(label);
      }
    } catch (e) { /* console unavailable */ }
  }

  /* Search: every term must match somewhere; title matches rank higher. */
  function searchScore(q, terms) {
    let score = 0;
    for (const term of terms) {
      if (q._sTitle.includes(term)) score += 3;
      else if (q._sMeta.includes(term)) score += 2;
      else if (q._sBody.includes(term)) score += 1;
      else return 0;
    }
    return score;
  }
  function searchTerms(text) {
    return normalizeText(text).split(/\s+/).map((s) => s.trim()).filter(Boolean);
  }

  function countBy(list, key) {
    const out = {};
    for (const q of list) out[q[key]] = (out[q[key]] || 0) + 1;
    return out;
  }

  /* ======================================================================
     Persistent state (localStorage, versioned, corruption-safe)
     ====================================================================== */
  function defaultState() {
    return {
      version: STORAGE_VERSION,
      createdAt: Date.now(),
      preferences: { lang: 'en', theme: 'dark', mode: 'learning', motion: 'system', fontScale: 1, sidebarCollapsed: false },
      bookmarks: [],
      learnedQuestions: [],
      reviewQuestions: [],
      questionProgress: {},
      sessions: [],
      activeSession: null,
      planner: { dailyTarget: 10, interviewDate: '' },
      activity: {},
      daily: {},
    };
  }

  let storageOK = true;
  let storageNotice = null; // 'corrupt' | 'incompatible' | 'unavailable' | null
  function storageGet(key) { try { return window.localStorage.getItem(key); } catch (e) { storageOK = false; return null; } }
  function storageSet(key, val) { window.localStorage.setItem(key, val); }

  const strArr = (v) => (Array.isArray(v) ? Array.from(new Set(v.filter((x) => isStr(x) && x.length < 120))) : []);

  function sanitizePreferences(p) {
    const d = defaultState().preferences;
    if (!isObj(p)) return d;
    return {
      lang: ['en', 'bn', 'both'].includes(p.lang) ? p.lang : d.lang,
      theme: ['dark', 'light'].includes(p.theme) ? p.theme : d.theme,
      mode: ['learning', 'interview'].includes(p.mode) ? p.mode : d.mode,
      motion: ['system', 'reduce', 'full'].includes(p.motion) ? p.motion : d.motion,
      fontScale: [0.9, 1, 1.1, 1.2].includes(p.fontScale) ? p.fontScale : d.fontScale,
      sidebarCollapsed: p.sidebarCollapsed === true,
    };
  }
  function sanitizeProgressEntry(p) {
    if (!isObj(p)) return null;
    const history = Array.isArray(p.history)
      ? p.history.filter((e) => isObj(e) && RESULTS.includes(e.r) && Number.isFinite(e.at)).map((e) => ({ r: e.r, at: e.at, s: isStr(e.s) ? e.s : null })).slice(-20)
      : [];
    if (!history.length) return null;
    return {
      history,
      box: Number.isInteger(p.box) ? clamp(p.box, 0, REVIEW_INTERVALS.length) : null,
      due: Number.isFinite(p.due) ? p.due : null,
    };
  }
  function sanitizeSession(s) {
    if (!isObj(s) || !isStr(s.id) || !Array.isArray(s.ids)) return null;
    const ids = s.ids.filter(isStr).slice(0, 200);
    if (!ids.length) return null;
    const answers = {};
    if (isObj(s.answers)) {
      for (const id of ids) {
        const a = s.answers[id];
        if (!isObj(a)) continue;
        answers[id] = {
          result: RESULTS.includes(a.result) ? a.result : null,
          revealed: a.revealed === true,
          mcqChoice: Number.isInteger(a.mcqChoice) ? a.mcqChoice : null,
          at: Number.isFinite(a.at) ? a.at : null,
          firstSeenAt: Number.isFinite(a.firstSeenAt) ? a.firstSeenAt : null,
        };
      }
    }
    return {
      id: s.id,
      kind: ['practice', 'interview', 'daily'].includes(s.kind) ? s.kind : 'practice',
      config: isObj(s.config) ? s.config : {},
      ids,
      index: Number.isInteger(s.index) ? clamp(s.index, 0, ids.length - 1) : 0,
      answers,
      startedAt: Number.isFinite(s.startedAt) ? s.startedAt : Date.now(),
      endedAt: Number.isFinite(s.endedAt) ? s.endedAt : null,
      deadline: Number.isFinite(s.deadline) ? s.deadline : null,
      dateKey: isStr(s.dateKey) ? s.dateKey : null,
      summary: isObj(s.summary) ? s.summary : null,
    };
  }

  /* Migrations: each entry upgrades data FROM version n to n+1. */
  const MIGRATIONS = {
    // 0 = unversioned prototype format: { bookmarks, learned, review, progress, history }
    0: (d) => ({
      version: 1,
      preferences: d.preferences || d.prefs,
      bookmarks: d.bookmarks,
      learnedQuestions: d.learnedQuestions || d.learned,
      reviewQuestions: d.reviewQuestions || d.review,
      questionProgress: d.questionProgress || d.progress,
      sessions: d.sessions || d.history,
      planner: d.planner,
      activity: d.activity,
      daily: d.daily,
    }),
  };
  function migrate(data) {
    let d = data;
    let v = Number.isInteger(d.version) ? d.version : 0;
    if (v > STORAGE_VERSION) return { data: null, incompatible: true };
    while (v < STORAGE_VERSION) {
      const step = MIGRATIONS[v];
      if (!step) return { data: null, incompatible: true };
      d = step(d);
      v = d.version;
    }
    return { data: d, incompatible: false };
  }

  function sanitizeState(d) {
    const base = defaultState();
    if (!isObj(d)) return base;
    base.createdAt = Number.isFinite(d.createdAt) ? d.createdAt : base.createdAt;
    base.preferences = sanitizePreferences(d.preferences);
    base.bookmarks = strArr(d.bookmarks);
    base.learnedQuestions = strArr(d.learnedQuestions);
    base.reviewQuestions = strArr(d.reviewQuestions);
    if (isObj(d.questionProgress)) {
      for (const id of Object.keys(d.questionProgress)) {
        if (!isStr(id) || id.length > 120) continue;
        const e = sanitizeProgressEntry(d.questionProgress[id]);
        if (e) base.questionProgress[id] = e;
      }
    }
    base.sessions = Array.isArray(d.sessions) ? d.sessions.map(sanitizeSession).filter((s) => s && s.endedAt).slice(-200) : [];
    base.activeSession = d.activeSession ? sanitizeSession(d.activeSession) : null;
    if (base.activeSession && base.activeSession.endedAt) base.activeSession = null;
    if (isObj(d.planner)) {
      const t = parseInt(d.planner.dailyTarget, 10);
      base.planner.dailyTarget = Number.isFinite(t) ? clamp(t, 1, 200) : 10;
      base.planner.interviewDate = isStr(d.planner.interviewDate) && /^\d{4}-\d{2}-\d{2}$/.test(d.planner.interviewDate) ? d.planner.interviewDate : '';
    }
    if (isObj(d.activity)) {
      for (const k of Object.keys(d.activity)) {
        const n = d.activity[k];
        if (/^\d{4}-\d{2}-\d{2}$/.test(k) && Number.isFinite(n) && n > 0) base.activity[k] = Math.min(10000, Math.round(n));
      }
    }
    if (isObj(d.daily)) {
      for (const k of Object.keys(d.daily)) {
        const v = d.daily[k];
        if (/^\d{4}-\d{2}-\d{2}$/.test(k) && isObj(v) && isStr(v.sessionId)) base.daily[k] = { sessionId: v.sessionId, score: Number.isFinite(v.score) ? v.score : null };
      }
    }
    return base;
  }

  function loadState() {
    const raw = storageGet(STORAGE_KEY);
    if (!storageOK) { storageNotice = 'unavailable'; return defaultState(); }
    if (raw == null) return defaultState();
    let parsed;
    try { parsed = JSON.parse(raw); } catch (e) { parsed = undefined; }
    if (!isObj(parsed)) {
      try { storageSet(STORAGE_KEY + ':corrupt:' + Date.now(), raw); } catch (e) { /* ignore */ }
      storageNotice = 'corrupt';
      return defaultState();
    }
    const m = migrate(parsed);
    if (m.incompatible) {
      try { storageSet(STORAGE_KEY + ':backup:' + Date.now(), raw); } catch (e) { /* ignore */ }
      storageNotice = 'incompatible';
      return defaultState();
    }
    return sanitizeState(m.data);
  }

  let state = loadState();

  function saveState() {
    if (!storageOK) return false;
    try {
      storageSet(STORAGE_KEY, JSON.stringify(state));
      return true;
    } catch (e) {
      // Quota exceeded: trim history and retry once
      try {
        state.sessions = state.sessions.slice(-50);
        storageSet(STORAGE_KEY, JSON.stringify(state));
        return true;
      } catch (e2) {
        storageOK = false;
        toast(t('storageFull'), 'bad');
        return false;
      }
    }
  }

  /* ======================================================================
     Progress, scoring and review scheduling
     ====================================================================== */
  function prog(id) { return state.questionProgress[id] || null; }

  /** Latest non-skipped result (the question's "answer status"). */
  function statusOf(id) {
    const p = prog(id);
    if (!p) return null;
    for (let i = p.history.length - 1; i >= 0; i--) if (p.history[i].r !== 'skipped') return p.history[i].r;
    return 'skipped';
  }
  function lastAt(id) { const p = prog(id); return p && p.history.length ? p.history[p.history.length - 1].at : 0; }
  const isAnswered = (id) => { const s = statusOf(id); return s === 'correct' || s === 'partial' || s === 'incorrect'; };

  function bumpActivity(n) {
    const k = localDateKey();
    state.activity[k] = (state.activity[k] || 0) + (n || 1);
  }

  function scheduleReview(p, result, now) {
    if (result === 'incorrect') { p.box = 0; p.due = addDays(startOfDay(now), REVIEW_INTERVALS[0]); }
    else if (result === 'partial') { p.box = Math.min(p.box == null ? 1 : Math.max(1, p.box), REVIEW_INTERVALS.length - 1); p.due = addDays(startOfDay(now), REVIEW_INTERVALS[p.box]); }
    else if (result === 'correct') {
      if (p.due != null) {
        const next = (p.box == null ? 0 : p.box) + 1;
        if (next >= REVIEW_INTERVALS.length) { p.box = null; p.due = null; }
        else { p.box = next; p.due = addDays(startOfDay(now), REVIEW_INTERVALS[next]); }
      }
    }
  }

  /** Record a result. With a sessionId, a previous result from the same session is replaced (no double counting). */
  function recordResult(id, result, sessionId) {
    if (!QMAP.has(id) || !RESULTS.includes(result)) return;
    const now = Date.now();
    let p = state.questionProgress[id];
    if (!p) p = state.questionProgress[id] = { history: [], box: null, due: null };
    let replaced = false;
    if (sessionId) {
      const idx = p.history.findIndex((e) => e.s === sessionId);
      if (idx >= 0) { p.history.splice(idx, 1); replaced = true; }
    }
    p.history.push({ r: result, at: now, s: sessionId || null });
    if (p.history.length > 20) p.history = p.history.slice(-20);
    scheduleReview(p, result, now);
    if (!replaced && result !== 'skipped') bumpActivity(1);
    saveState();
  }

  function dueIds(now) {
    const end = addDays(startOfDay(now || Date.now()), 1) - 1;
    return QUESTIONS.filter((q) => { const p = prog(q.id); return p && p.due != null && p.due <= end; }).map((q) => q.id);
  }
  function upcomingIds(days) {
    const start = addDays(startOfDay(Date.now()), 1);
    const end = addDays(start, days);
    return QUESTIONS.filter((q) => { const p = prog(q.id); return p && p.due != null && p.due >= start && p.due < end; }).map((q) => q.id);
  }

  const setHas = (key, id) => state[key].includes(id);
  function toggleIn(key, id, force) {
    const has = state[key].includes(id);
    const want = force == null ? !has : !!force;
    if (want && !has) { state[key].push(id); if (key === 'learnedQuestions') bumpActivity(1); }
    if (!want && has) state[key] = state[key].filter((x) => x !== id);
    saveState();
    return want;
  }
  const isBookmarked = (id) => setHas('bookmarks', id);
  const isLearned = (id) => setHas('learnedQuestions', id);
  const isFlagged = (id) => setHas('reviewQuestions', id);

  /** Aggregate stats over a list of questions using each question's latest status. */
  function statsFor(list) {
    const s = { total: list.length, answered: 0, correct: 0, partial: 0, incorrect: 0, skippedOnly: 0, attempted: 0, learned: 0, bookmarked: 0, flagged: 0, earned: 0, possible: 0, completed: 0, byDiff: {} };
    DIFFS.forEach((d) => { s.byDiff[d] = { total: 0, answered: 0, correct: 0, partial: 0, incorrect: 0 }; });
    for (const q of list) {
      const st = statusOf(q.id);
      const bd = s.byDiff[q.difficulty];
      bd.total++;
      if (isLearned(q.id)) s.learned++;
      if (isBookmarked(q.id)) s.bookmarked++;
      if (isFlagged(q.id)) s.flagged++;
      if (st) {
        s.attempted++;
        s.possible += POINTS[q.difficulty];
        s.earned += POINTS[q.difficulty] * RESULT_FACTOR[st];
      }
      if (st === 'skipped') s.skippedOnly++;
      else if (st) { s.answered++; s[st]++; bd.answered++; bd[st]++; }
      if ((st && st !== 'skipped') || isLearned(q.id)) s.completed++;
    }
    s.accuracy = s.answered ? s.correct / s.answered : null;
    s.weighted = s.possible ? s.earned / s.possible : null;
    s.completion = s.total ? s.completed / s.total : 0;
    return s;
  }

  function streakInfo() {
    const today = localDateKey();
    let d = new Date();
    if (!state.activity[today]) d.setDate(d.getDate() - 1);
    let streak = 0;
    while (state.activity[localDateKey(d)]) { streak++; d.setDate(d.getDate() - 1); }
    let best = 0, run = 0;
    const keys = Object.keys(state.activity).sort();
    let prev = null;
    for (const k of keys) {
      if (prev && (startOfDay(new Date(k + 'T00:00:00')) - startOfDay(new Date(prev + 'T00:00:00'))) <= DAY * 1.5) run++;
      else run = 1;
      best = Math.max(best, run);
      prev = k;
    }
    return { current: streak, best: Math.max(best, streak), today: state.activity[today] || 0 };
  }

  /** Session summary with weighted score and accuracy. Unanswered questions count as skipped. */
  function summarizeSession(sess) {
    const sm = { total: 0, correct: 0, partial: 0, incorrect: 0, skipped: 0, earned: 0, possible: 0, byTech: {}, byDiff: {}, durationMs: 0 };
    DIFFS.forEach((d) => { sm.byDiff[d] = { total: 0, correct: 0, partial: 0, incorrect: 0, skipped: 0, earned: 0, possible: 0 }; });
    for (const id of sess.ids) {
      const q = QMAP.get(id);
      if (!q) continue;
      const a = sess.answers[id] || {};
      const r = RESULTS.includes(a.result) ? a.result : 'skipped';
      const pts = POINTS[q.difficulty];
      const earned = pts * RESULT_FACTOR[r];
      sm.total++; sm[r]++; sm.possible += pts; sm.earned += earned;
      const bt = sm.byTech[q.technology] || (sm.byTech[q.technology] = { total: 0, correct: 0, partial: 0, incorrect: 0, skipped: 0, earned: 0, possible: 0 });
      const bd = sm.byDiff[q.difficulty];
      for (const b of [bt, bd]) { b.total++; b[r]++; b.earned += earned; b.possible += pts; }
    }
    sm.answered = sm.correct + sm.partial + sm.incorrect;
    sm.accuracy = sm.answered ? sm.correct / sm.answered : null;
    sm.weighted = sm.possible ? sm.earned / sm.possible : null;
    sm.durationMs = Math.max(0, (sess.endedAt || Date.now()) - sess.startedAt);
    return sm;
  }

  /** Weak areas: subtopics/technologies with the most incorrect or partial answers (min 2 attempts). */
  function weakAreas(limit) {
    const groups = new Map();
    for (const q of QUESTIONS) {
      const p = prog(q.id);
      if (!p) continue;
      const answered = p.history.filter((e) => e.r !== 'skipped');
      if (!answered.length) continue;
      const key = q.technology + '::' + q.subtopic;
      const g = groups.get(key) || { tech: q.technology, subtopic: q.subtopic, attempts: 0, correct: 0, partial: 0, incorrect: 0, ids: new Set() };
      for (const e of answered) { g.attempts++; g[e.r]++; }
      g.ids.add(q.id);
      groups.set(key, g);
    }
    const arr = Array.from(groups.values()).filter((g) => g.attempts >= 2 && (g.incorrect + g.partial) > 0);
    arr.forEach((g) => { g.missRate = (g.incorrect + 0.5 * g.partial) / g.attempts; g.accuracy = g.correct / g.attempts; });
    arr.sort((a, b) => b.missRate - a.missRate || b.attempts - a.attempts);
    return arr.slice(0, limit || 6);
  }
  function weakDifficulties() {
    const out = [];
    for (const d of DIFFS) {
      let attempts = 0, miss = 0;
      for (const q of QUESTIONS) {
        if (q.difficulty !== d) continue;
        const p = prog(q.id);
        if (!p) continue;
        for (const e of p.history) { if (e.r === 'skipped') continue; attempts++; if (e.r === 'incorrect') miss += 1; else if (e.r === 'partial') miss += 0.5; }
      }
      out.push({ difficulty: d, attempts, missRate: attempts ? miss / attempts : null });
    }
    return out;
  }

  /* ======================================================================
     Export / import
     ====================================================================== */
  function exportData() {
    return {
      app: 'interview-prep-bd',
      appVersion: APP_VERSION,
      exportedAt: new Date().toISOString(),
      data: {
        version: STORAGE_VERSION,
        createdAt: state.createdAt,
        preferences: state.preferences,
        bookmarks: state.bookmarks,
        learnedQuestions: state.learnedQuestions,
        reviewQuestions: state.reviewQuestions,
        questionProgress: state.questionProgress,
        sessions: state.sessions,
        planner: state.planner,
        activity: state.activity,
        daily: state.daily,
      },
    };
  }
  /** Validates an imported backup. Returns { ok, data?, error?, summary? } and never mutates state. */
  function parseImport(text) {
    if (!isStr(text) || text.length > 15 * 1024 * 1024) return { ok: false, error: 'tooLarge' };
    let obj;
    try { obj = JSON.parse(text); } catch (e) { return { ok: false, error: 'invalidJson' }; }
    if (!isObj(obj) || obj.app !== 'interview-prep-bd' || !isObj(obj.data)) return { ok: false, error: 'notBackup' };
    const m = migrate(obj.data);
    if (m.incompatible) return { ok: false, error: 'incompatible' };
    const clean = sanitizeState(m.data);
    clean.activeSession = null;
    const known = (id) => QMAP.has(id);
    const summary = {
      bookmarks: clean.bookmarks.filter(known).length,
      learned: clean.learnedQuestions.filter(known).length,
      review: clean.reviewQuestions.filter(known).length,
      progress: Object.keys(clean.questionProgress).filter(known).length,
      sessions: clean.sessions.length,
      exportedAt: isStr(obj.exportedAt) ? obj.exportedAt : '',
    };
    return { ok: true, data: clean, summary };
  }

  /* ======================================================================
     i18n helpers (dictionary lives in 35-i18n.js)
     ====================================================================== */
  const lang = () => state.preferences.lang;
  function fill(str, vars) {
    if (!vars) return str;
    // {s} → English plural suffix for {n}
    return String(str).replace(/\{(\w+)\}/g, (m, k) => (vars[k] != null ? vars[k] : k === 's' && vars.n != null ? (Number(vars.n) === 1 ? '' : 's') : m));
  }
  /** Single-language UI string (Both mode → English, used for buttons, aria labels, titles). */
  function t(key, vars) {
    const e = I18N[key];
    if (!e) { if (window.console) console.warn('[i18n] missing key', key); return key; }
    const s = lang() === 'bn' ? (e.bn || e.en) : e.en;
    return fill(s, vars);
  }
  function tLang(key, lg, vars) { const e = I18N[key]; if (!e) return key; return fill(lg === 'bn' ? (e.bn || e.en) : e.en, vars); }
  /** Bilingual-aware node: in Both mode shows English with Bangla underneath. */
  function tb(key, vars, opts) {
    const L = lang();
    if (L !== 'both') return h('span', { lang: L === 'bn' ? 'bn' : 'en', class: L === 'bn' ? 'bn' : null }, inline(t(key, vars)));
    const inlineMode = opts && opts.inline;
    return h('span', { class: 'tb' },
      h('span', { lang: 'en' }, inline(tLang(key, 'en', vars))),
      inlineMode ? ' · ' : h('br'),
      h('span', { lang: 'bn', class: 'bn muted', style: { fontSize: inlineMode ? 'inherit' : '.88em' } }, inline(tLang(key, 'bn', vars))));
  }
  /** Pick text from a {en,bn} object for single-line contexts. */
  function pick(obj) {
    if (!obj) return '';
    if (lang() === 'bn') return obj.bn || obj.en || '';
    return obj.en || obj.bn || '';
  }

  /* ======================================================================
     Formatting
     ====================================================================== */
  const pct = (x) => (x == null || !Number.isFinite(x) ? '—' : Math.round(x * 100) + '%');
  const fmtNum = (n) => (Number.isFinite(n) ? (Math.round(n * 10) / 10).toLocaleString('en-US') : '—');
  function fmtDuration(ms) {
    const s = Math.max(0, Math.round(ms / 1000));
    const hh = Math.floor(s / 3600), mm = Math.floor((s % 3600) / 60), ss = s % 60;
    if (hh) return hh + 'h ' + String(mm).padStart(2, '0') + 'm';
    return mm + 'm ' + String(ss).padStart(2, '0') + 's';
  }
  function fmtClock(ms) {
    const s = Math.max(0, Math.round(ms / 1000));
    const mm = Math.floor(s / 60), ss = s % 60;
    return String(mm).padStart(2, '0') + ':' + String(ss).padStart(2, '0');
  }
  function fmtDate(ts, withTime) {
    if (!ts) return '—';
    const loc = lang() === 'bn' ? 'bn-BD' : 'en-GB';
    const opts = withTime ? { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' } : { day: 'numeric', month: 'short', year: 'numeric' };
    try { return new Date(ts).toLocaleString(loc, opts); } catch (e) { return new Date(ts).toISOString().slice(0, 10); }
  }
  function fmtDay(key) {
    try { return new Date(key + 'T00:00:00').toLocaleDateString(lang() === 'bn' ? 'bn-BD' : 'en-GB', { weekday: 'short' }); } catch (e) { return key.slice(5); }
  }

  /* ======================================================================
     Rich text (safe subset: paragraphs, lists, `code`, **bold**, ``` fences)
     ====================================================================== */
  function inline(text) {
    const out = [];
    const s = String(text || '');
    // `code`, **bold**, *emphasis* (single asterisks must hug the text, so "a * b * c" stays literal)
    const re = /(`[^`\n]+`|\*\*[^*\n]+?\*\*|(?<![\w*])\*(?![\s*])[^*\n]+?(?<![\s*])\*(?![\w*]))/g;
    let last = 0, m;
    while ((m = re.exec(s))) {
      if (m.index > last) out.push(s.slice(last, m.index));
      const tok = m[0];
      if (tok[0] === '`') out.push(h('code', null, tok.slice(1, -1)));
      else if (tok.startsWith('**')) out.push(h('strong', null, inline(tok.slice(2, -2))));
      else out.push(h('em', null, inline(tok.slice(1, -1))));
      last = m.index + tok.length;
    }
    if (last < s.length) out.push(s.slice(last));
    return out;
  }
  function renderRich(text) {
    const root = document.createDocumentFragment();
    const lines = String(text || '').replace(/\r\n?/g, '\n').split('\n');
    let para = [];
    const flush = () => { if (para.length) { root.append(h('p', null, inline(para.join(' ')))); para = []; } };
    const BUL = /^\s*[-*•]\s+/;
    const NUM = /^\s*\d+[.)]\s+/;
    let i = 0;
    while (i < lines.length) {
      const line = lines[i];
      if (/^\s*```/.test(line)) {
        flush();
        const lg = line.replace(/^\s*```/, '').trim() || 'text';
        const buf = [];
        i++;
        while (i < lines.length && !/^\s*```/.test(lines[i])) { buf.push(lines[i]); i++; }
        i++;
        root.append(codeBlock({ language: lg, source: buf.join('\n') }));
        continue;
      }
      if (BUL.test(line) || NUM.test(line)) {
        flush();
        const ordered = NUM.test(line);
        const list = h(ordered ? 'ol' : 'ul');
        const MARK = ordered ? NUM : BUL;
        while (i < lines.length && MARK.test(lines[i])) {
          let item = lines[i].replace(MARK, '');
          i++;
          while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !BUL.test(lines[i]) && !NUM.test(lines[i])) { item += ' ' + lines[i].trim(); i++; }
          list.append(h('li', null, inline(item)));
        }
        root.append(list);
        continue;
      }
      if (!line.trim()) { flush(); i++; continue; }
      if (/^#{1,4}\s+/.test(line)) { flush(); root.append(h('p', null, h('strong', null, inline(line.replace(/^#{1,4}\s+/, ''))))); i++; continue; }
      para.push(line.trim());
      i++;
    }
    flush();
    return root;
  }

  /** Shows a {en,bn} text according to the language preference. */
  function biText(obj, opts) {
    const o = opts || {};
    const L = lang();
    const en = obj && obj.en, bn = obj && obj.bn;
    const make = (txt, lg) => {
      const el = h(o.tag || 'div', { class: (o.cls || 'prose') + (lg === 'bn' ? ' bn' : ''), lang: lg });
      if (o.plain) append(el, inline(txt)); else el.append(renderRich(txt));
      return el;
    };
    if (L === 'both' && en && bn) {
      return h('div', { class: 'bi-block' },
        h('div', { class: 'bi-pane' }, o.noLabels ? null : h('span', { class: 'bi-label', 'aria-hidden': 'true' }, 'English'), make(en, 'en')),
        h('div', { class: 'bi-pane' }, o.noLabels ? null : h('span', { class: 'bi-label', 'aria-hidden': 'true' }, 'বাংলা'), make(bn, 'bn')));
    }
    if (L === 'bn') {
      if (bn) return make(bn, 'bn');
      return h('div', null, make(en || '', 'en'), h('p', { class: 'tiny faint' }, t('noTranslation')));
    }
    return make(en || bn || '', en ? 'en' : 'bn');
  }
  /** Compact title text (inline only) for lists. */
  function biTitle(obj, cls) {
    const L = lang();
    if (L === 'both' && obj.en && obj.bn) {
      return h('span', { class: cls || null }, h('span', { lang: 'en' }, inline(obj.en)), h('span', { class: 'bn', lang: 'bn' }, inline(obj.bn)));
    }
    if (L === 'bn' && obj.bn) return h('span', { class: (cls ? cls + ' ' : '') + 'bn', lang: 'bn' }, inline(obj.bn));
    return h('span', { class: cls || null, lang: 'en' }, inline(obj.en || obj.bn || ''));
  }

  /* ======================================================================
     Code blocks with a tiny, safe syntax highlighter
     ====================================================================== */
  const KW = {
    js: new Set('abstract as async await break case catch class const continue debugger declare default delete do else enum export extends false finally for from function get if implements import in infer instanceof interface keyof let namespace new null of override private protected public readonly return satisfies set static super switch this throw true try type typeof undefined using var void while with yield'.split(' ')),
    sql: new Set('add all alter analyze and any as asc begin between by cascade case check coalesce column commit concurrently constraint create cross current_date current_timestamp database default delete desc distinct do drop else end except exists explain false fetch filter first following foreign from full function generated group having if ilike in index inner insert intersect into is join key last lateral left like limit materialized not null nulls offset on or order outer over partition preceding primary procedure range recursive references replace returning returns right rollback row rows savepoint select serializable set table then to transaction trigger true truncate unbounded union unique update using values view when where window with without'.split(' ')),
    sh: new Set('if then else elif fi for in do done while case esac function return export local echo sudo cd npm npx node docker git curl apt yarn pnpm kubectl aws psql redis-cli mongosh nginx systemctl set unset'.split(' ')),
    docker: new Set('FROM AS RUN CMD LABEL EXPOSE ENV ADD COPY ENTRYPOINT VOLUME USER WORKDIR ARG ONBUILD STOPSIGNAL HEALTHCHECK SHELL'.split(' ')),
    py: new Set('and as assert async await break class continue def del elif else except False finally for from global if import in is lambda None nonlocal not or pass raise return True try while with yield'.split(' ')),
    nginx: new Set('server location upstream http events listen server_name root index proxy_pass proxy_set_header proxy_http_version proxy_read_timeout proxy_connect_timeout proxy_send_timeout proxy_cache proxy_cache_path proxy_cache_valid proxy_buffering return rewrite try_files include worker_processes worker_connections ssl_certificate ssl_certificate_key ssl_protocols http2 http3 gzip gzip_types limit_req limit_req_zone limit_conn limit_conn_zone client_max_body_size keepalive_timeout access_log error_log map add_header expires least_conn ip_hash hash if set alias default_type sendfile'.split(' ')),
  };
  function langFamily(lg) {
    const l = String(lg || '').toLowerCase();
    if (['js', 'javascript', 'jsx', 'ts', 'typescript', 'tsx', 'mjs', 'cjs', 'json', 'node'].includes(l)) return 'js';
    if (['sql', 'psql', 'postgresql', 'pgsql', 'plpgsql'].includes(l)) return 'sql';
    if (['bash', 'sh', 'shell', 'zsh', 'console', 'terminal'].includes(l)) return 'sh';
    if (['dockerfile', 'docker'].includes(l)) return 'docker';
    if (['yaml', 'yml'].includes(l)) return 'yaml';
    if (['html', 'xml', 'svg', 'vue'].includes(l)) return 'html';
    if (['css', 'scss'].includes(l)) return 'css';
    if (['nginx', 'conf'].includes(l)) return 'nginx';
    if (['python', 'py'].includes(l)) return 'py';
    return 'plain';
  }
  const HL_RE = {
    js: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|('(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*"|`(?:\\[\s\S]|[^`\\])*`)|(\b(?:0x[\da-fA-F]+|\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?n?)\b)|([A-Za-z_$][\w$]*)(?=\s*\()|([A-Za-z_$][\w$]*)/g,
    sql: /(--[^\n]*|\/\*[\s\S]*?\*\/)|('(?:''|[^'])*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][\w]*)(?=\s*\()|([A-Za-z_][\w]*)/g,
    sh: /(#[^\n]*)|('[^'\n]*'|"(?:\\.|[^"\\\n])*")|(\b\d+\b)|(\$\{?[\w]+\}?)|([A-Za-z_][\w-]*)/g,
    docker: /(#[^\n]*)|('[^'\n]*'|"(?:\\.|[^"\\\n])*")|(\b\d+\b)|(\$\{?[\w]+\}?)|([A-Za-z_][\w-]*)/g,
    py: /(#[^\n]*)|('''[\s\S]*?'''|"""[\s\S]*?"""|'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*")|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)(?=\s*\()|([A-Za-z_]\w*)/g,
    nginx: /(#[^\n]*)|('[^'\n]*'|"[^"\n]*")|(\b\d+[kmsKMGhd]?\b)|(\$[\w]+)|([A-Za-z_][\w]*)/g,
    yaml: /(#[^\n]*)|('[^'\n]*'|"(?:\\.|[^"\\\n])*")|(\b\d+(?:\.\d+)?\b)|(^\s*-?\s*[\w.\-/]+(?=:))|(\b(?:true|false|null|yes|no)\b)/gm,
    html: /(<[!]--[\s\S]*?-->)|("[^"]*"|'[^']*')|(<\/?[A-Za-z][\w-]*|\/?>)|([A-Za-z_:@][\w\-:.]*)(?==)/g,
    css: /(\/\*[\s\S]*?\*\/)|("[^"]*"|'[^']*')|(#[\da-fA-F]{3,8}\b|-?\b\d+(?:\.\d+)?(?:px|rem|em|%|vh|vw|dvh|svh|lvh|s|ms|fr|deg|ch|lh|cqi|cqw)?\b)|([\w-]+)(?=\s*:[^;{}\n]*;)|(@[\w-]+|!important)/g,
  };
  function classify(fam, m) {
    switch (fam) {
      case 'js': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return KW.js.has(m[4]) ? 'kw' : 'fn'; if (m[5]) return KW.js.has(m[5]) ? 'kw' : null; return null;
      case 'sql': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return KW.sql.has(m[4].toLowerCase()) ? 'kw' : 'fn'; if (m[5]) return KW.sql.has(m[5].toLowerCase()) ? 'kw' : null; return null;
      case 'sh': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return KW.sh.has(m[5]) ? 'kw' : null; return null;
      case 'docker': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return KW.docker.has(m[5]) ? 'kw' : null; return null;
      case 'py': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return KW.py.has(m[4]) ? 'kw' : 'fn'; if (m[5]) return KW.py.has(m[5]) ? 'kw' : null; return null;
      case 'nginx': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return KW.nginx.has(m[5]) ? 'kw' : null; return null;
      case 'yaml': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return 'kw'; return null;
      case 'html': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'tag'; if (m[4]) return 'attr'; return null;
      case 'css': if (m[1]) return 'com'; if (m[2]) return 'str'; if (m[3]) return 'num'; if (m[4]) return 'attr'; if (m[5]) return 'kw'; return null;
      default: return null;
    }
  }
  function highlight(src, lg) {
    const f = document.createDocumentFragment();
    const fam = langFamily(lg);
    const base = HL_RE[fam];
    const text = String(src || '');
    if (!base || text.length > 20000) { f.append(text); return f; }
    const re = new RegExp(base.source, base.flags);
    let last = 0, m;
    while ((m = re.exec(text))) {
      if (!m[0]) { re.lastIndex++; continue; }
      if (m.index > last) f.append(text.slice(last, m.index));
      const cls = classify(fam, m);
      f.append(cls ? h('span', { class: 'tok-' + cls }, m[0]) : m[0]);
      last = m.index + m[0].length;
    }
    if (last < text.length) f.append(text.slice(last));
    return f;
  }

  async function copyText(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return true; }
    } catch (e) { /* fall through */ }
    try {
      const ta = h('textarea', { style: { position: 'fixed', top: '-1000px', opacity: '0' }, 'aria-hidden': 'true' });
      ta.value = text;
      document.body.append(ta);
      ta.select();
      const ok = document.execCommand('copy');
      ta.remove();
      return ok;
    } catch (e) { return false; }
  }

  function codeBlock(code, opts) {
    const o = opts || {};
    const isOut = !!o.output;
    const text = isOut ? code.output : code.source;
    const copyBtn = h('button', {
      class: 'copy-btn', type: 'button', 'aria-label': t('copyCode'),
      onclick: async () => {
        const ok = await copyText(text);
        copyBtn.textContent = ok ? t('copied') : t('copyFailed');
        setTimeout(() => { copyBtn.textContent = t('copy'); }, 1500);
      },
    }, t('copy'));
    const label = o.label ? h('span', { class: 'code__label' }, o.label) : null;
    return h('figure', { class: 'code' + (isOut ? ' code--output' : '') },
      h('div', { class: 'code__bar' },
        h('span', { class: 'row', style: { gap: '8px' } }, label, h('span', { class: 'code__lang' }, isOut ? t('expectedOutput') : (code.language || 'text'))),
        copyBtn),
      h('pre', { tabindex: '0', 'aria-label': isOut ? t('expectedOutput') : t('codeExample') }, h('code', null, isOut ? text : highlight(text, code.language))));
  }

  /* ======================================================================
     Badges & small components
     ====================================================================== */
  function diffBadge(d) {
    const n = DIFFS.indexOf(d) + 1;
    return h('span', { class: 'badge badge--' + d, title: t('difficulty') + ': ' + t('diff_' + d) },
      h('span', { class: 'pips', 'aria-hidden': 'true' }, [1, 2, 3, 4].map((k) => h('i', { class: k <= n ? 'on' : null }))),
      t('diff_' + d));
  }
  const typeBadge = (ty) => h('span', { class: 'badge', title: t('questionType') }, t('type_' + ty));
  function marketBadge(m) {
    if (m === 'both') return h('span', { class: 'badge', title: t('market') }, icon('globe', 12), t('market_both'));
    return h('span', { class: 'badge badge--teal', title: t('market') }, icon('globe', 12), t('market_' + m));
  }
  const priorityBadge = (p) => h('span', { class: 'badge' + (p === 'high' ? ' badge--primary' : ''), title: t('priority') }, icon('star', 12), t('prio_' + p));
  function techBadge(id) {
    const tc = TECH_MAP.get(id);
    if (!tc) return null;
    return h('span', { class: 'badge' }, h('span', { 'aria-hidden': 'true', style: { width: '8px', height: '8px', borderRadius: '50%', background: tc.color, display: 'inline-block' } }), tc.name);
  }
  function resultBadge(r) {
    if (!r) return h('span', { class: 'badge' }, t('res_none'));
    const cls = { correct: 'ok', partial: 'partial', incorrect: 'bad', skipped: '' }[r];
    const ic = { correct: 'check', partial: 'half', incorrect: 'x', skipped: 'skip' }[r];
    return h('span', { class: 'badge' + (cls ? ' badge--' + cls : '') }, icon(ic, 12), t('res_' + r));
  }
  function featureStatusBadge(s) {
    if (!s || s === 'stable') return h('span', { class: 'badge badge--ok' }, t('st_stable'));
    return h('span', { class: 'badge badge--warn' }, icon('alert', 12), I18N['st_' + s] ? t('st_' + s) : s);
  }
  function techLogo(tc, size) {
    return h('span', { class: size === 'sm' ? 'tech-dot' : 'tech-card__logo', style: { background: tc.color }, 'aria-hidden': 'true' }, tc.short);
  }
  function progressBar(fraction, opts) {
    const o = opts || {};
    const v = clamp(fraction || 0, 0, 1);
    return h('div', { class: 'progress' + (o.thin ? ' progress--thin' : '') + (o.lg ? ' progress--lg' : ''), role: 'progressbar', 'aria-valuemin': '0', 'aria-valuemax': '100', 'aria-valuenow': String(Math.round(v * 100)), 'aria-label': o.label || t('progress') },
      h('span', { style: { width: (v * 100).toFixed(1) + '%' } }));
  }
  function stat(label, value, opts) {
    const o = opts || {};
    return h('div', { class: 'stat' + (o.tone ? ' stat--' + o.tone : '') },
      h('div', { class: 'stat__label' }, label),
      h('div', { class: 'stat__value' }, value),
      o.hint ? h('div', { class: 'stat__hint' }, o.hint) : null);
  }
  function emptyState(iconName, titleKey, textKey, actions) {
    return h('div', { class: 'empty' },
      h('div', { class: 'empty__icon' }, icon(iconName || 'info', 26)),
      h('h3', null, tb(titleKey)),
      textKey ? h('p', null, tb(textKey)) : null,
      actions ? h('div', { class: 'btn-row', style: { justifyContent: 'center' } }, actions) : null);
  }
  function linkBtn(href, label, cls, ic) {
    return h('a', { class: 'btn ' + (cls || ''), href }, ic ? icon(ic, 16) : null, label);
  }
  function btn(label, onClick, cls, ic, extra) {
    return h('button', Object.assign({ type: 'button', class: 'btn ' + (cls || ''), onclick: onClick }, extra || {}), ic ? icon(ic, 16) : null, label);
  }
  function seg(options, current, onChange, ariaLabel) {
    const wrap = h('div', { class: 'seg', role: 'group', 'aria-label': ariaLabel || '' });
    options.forEach((o) => {
      wrap.append(h('button', { type: 'button', 'aria-pressed': String(o.value === current), lang: o.lang || null, onclick: () => onChange(o.value) }, o.label));
    });
    return wrap;
  }
  function chip(label, pressed, onToggle, extra) {
    return h('button', Object.assign({ type: 'button', class: 'chip', 'aria-pressed': String(!!pressed), onclick: onToggle }, extra || {}), label);
  }

  /* ======================================================================
     Toasts & modal dialog
     ====================================================================== */
  function toast(msg, kind, ms) {
    const root = $('#toasts');
    if (!root) return;
    const el = h('div', { class: 'toast toast--' + (kind || 'info') }, icon(kind === 'ok' ? 'checkCircle' : kind === 'bad' ? 'alert' : 'info', 18), h('div', null, msg));
    root.append(el);
    setTimeout(() => { el.classList.add('is-leaving'); setTimeout(() => el.remove(), 260); }, ms || 3400);
  }

  let modalCloseHandler = null;
  function openModal(o) {
    const dlg = $('#modal');
    clear(dlg);
    const body = h('div', { class: 'modal__body' }, h('h2', { class: 'modal__title', id: 'modalTitle' }, o.title), o.body);
    const foot = h('div', { class: 'modal__foot' });
    const close = (result) => {
      if (dlg.open) dlg.close();
      const cb = modalCloseHandler; modalCloseHandler = null;
      if (cb) cb(result);
    };
    (o.actions || [{ label: t('close'), kind: 'btn--primary', value: true }]).forEach((a) => {
      const b = h('button', { type: 'button', class: 'btn ' + (a.kind || ''), onclick: () => {
        if (a.onClick && a.onClick() === false) return;
        close(a.value);
      } }, a.label);
      if (a.disabledUntil) { b.disabled = true; a.disabledUntil(b); }
      foot.append(b);
    });
    dlg.append(body, foot);
    modalCloseHandler = o.onClose || null;
    // Ignore stale close events that arrive after a new modal has already been opened.
    dlg.onclose = () => { if (dlg.open) return; const cb = modalCloseHandler; modalCloseHandler = null; if (cb) cb(undefined); };
    if (typeof dlg.showModal === 'function') {
      dlg.showModal();
      const auto = dlg.querySelector('[data-autofocus]') || foot.querySelector('.btn--primary, .btn--danger') || foot.querySelector('button');
      if (auto) auto.focus();
    } else {
      // Very old browsers: degrade to native confirm
      const ok = window.confirm(String(o.title));
      close(ok ? true : undefined);
    }
    return close;
  }
  function confirmModal(o) {
    return new Promise((resolve) => {
      let input = null;
      const parts = [h('div', { class: 'prose' }, o.message)];
      if (o.requireText) {
        input = h('input', { class: 'input', type: 'text', autocomplete: 'off', 'data-autofocus': 'true', 'aria-label': t('typeToConfirm', { word: o.requireText }) });
        parts.push(h('div', { class: 'field mt-2' }, h('label', null, t('typeToConfirm', { word: o.requireText })), input));
      }
      openModal({
        title: o.title,
        body: h('div', null, parts),
        actions: [
          { label: t('cancel'), kind: 'btn--ghost', value: false },
          {
            label: o.confirmLabel || t('confirm'), kind: o.danger ? 'btn--danger' : 'btn--primary', value: true,
            disabledUntil: input ? (b) => { input.addEventListener('input', () => { b.disabled = input.value.trim().toUpperCase() !== o.requireText; }); } : null,
          },
        ],
        onClose: (v) => resolve(v === true),
      });
    });
  }

  /* ======================================================================
     UI dictionary (English / বাংলা). Code, API and product names are never translated.
     ====================================================================== */
  const I18N = {
    // Navigation
    navLearn: { en: 'Learn', bn: 'শেখা' },
    navPractice: { en: 'Practice', bn: 'প্র্যাকটিস' },
    navProgress: { en: 'My progress', bn: 'আমার অগ্রগতি' },
    navMore: { en: 'More', bn: 'আরও' },
    navTechs: { en: 'Technologies', bn: 'টেকনোলজি' },
    nav_dashboard: { en: 'Dashboard', bn: 'ড্যাশবোর্ড' },
    nav_technologies: { en: 'Technologies', bn: 'টেকনোলজি' },
    nav_questions: { en: 'All Questions', bn: 'সব প্রশ্ন' },
    nav_flashcards: { en: 'Flashcards', bn: 'ফ্ল্যাশকার্ড' },
    nav_daily: { en: 'Daily Challenge', bn: 'আজকের চ্যালেঞ্জ' },
    nav_practice: { en: 'Practice', bn: 'প্র্যাকটিস' },
    nav_interview: { en: 'Interview Simulation', bn: 'মক ইন্টারভিউ' },
    nav_bookmarks: { en: 'Bookmarks', bn: 'বুকমার্ক' },
    nav_incorrect: { en: 'Incorrect Answers', bn: 'ভুল উত্তর' },
    nav_review: { en: 'Review Questions', bn: 'রিভিউ প্রশ্ন' },
    nav_history: { en: 'Study History', bn: 'পড়ার ইতিহাস' },
    nav_planner: { en: 'Study Planner', bn: 'স্টাডি প্ল্যানার' },
    nav_settings: { en: 'Settings', bn: 'সেটিংস' },
    nav_sources: { en: 'Versions & Sources', bn: 'ভার্সন ও সূত্র' },
    skipToContent: { en: 'Skip to main content', bn: 'মূল কনটেন্টে যাও' },
    collapseSidebar: { en: 'Collapse sidebar', bn: 'সাইডবার ছোট করো' },
    expandSidebar: { en: 'Expand sidebar', bn: 'সাইডবার বড় করো' },
    searchQuestions: { en: 'Search questions', bn: 'প্রশ্ন খুঁজুন' },
    language: { en: 'Language', bn: 'ভাষা' },
    languageHint: { en: 'Questions, answers and the interface switch together. “Both” shows English and Bangla side by side.', bn: 'প্রশ্ন, উত্তর আর interface একসাথে বদলায়। “দুটোই” দিলে English আর বাংলা পাশাপাশি দেখাবে।' },
    both: { en: 'Both', bn: 'দুটোই' },
    lightTheme: { en: 'Switch to light theme', bn: 'লাইট থিমে যাও' },
    darkTheme: { en: 'Switch to dark theme', bn: 'ডার্ক থিমে যাও' },
    items: { en: 'items', bn: 'টি' },
    localOnlyShort: { en: 'Progress is saved in this browser only.', bn: 'অগ্রগতি শুধু এই browser-এ সেভ থাকে।' },
    localOnlyLong: { en: 'Your progress is stored locally in this browser (localStorage). It is not synced across devices or browsers and no account is needed — use Export to keep a backup or move it to another device.', bn: 'তোমার অগ্রগতি এই browser-এর localStorage-এ সেভ থাকে। অন্য device বা browser-এ নিজে থেকে sync হয় না, আর কোনো account লাগে না — backup রাখতে বা অন্য device-এ নিতে Export ব্যবহার করো।' },
    verifiedOn: { en: 'Versions verified {date}', bn: 'ভার্সন যাচাই: {date}' },

    // Dashboard
    dashEyebrow: { en: 'Bilingual interview prep · Bangladesh & international', bn: 'দ্বিভাষিক ইন্টারভিউ প্রস্তুতি · বাংলাদেশ ও আন্তর্জাতিক' },
    welcomeNew: { en: 'Welcome! Let’s get you interview-ready.', bn: 'স্বাগতম! চলো ইন্টারভিউর জন্য তৈরি হই।' },
    welcomeBack: { en: 'Welcome back — keep the momentum going.', bn: 'আবার স্বাগতম — ধারাবাহিকতা ধরে রাখো।' },
    welcomeText: { en: '{n} research-backed questions across {t} technologies, from easy fundamentals to extreme system-design problems — in English and Bangla.', bn: '{t}টি টেকনোলজিতে {n}টি গবেষণাভিত্তিক প্রশ্ন — সহজ মৌলিক বিষয় থেকে কঠিন system design পর্যন্ত, English ও বাংলায়।' },
    continueLearning: { en: 'Continue learning', bn: 'শেখা চালিয়ে যাও' },
    startPractice: { en: 'Start practice', bn: 'প্র্যাকটিস শুরু করো' },
    resumeSession: { en: 'Resume session', bn: 'সেশন আবার শুরু করো' },
    gettingStarted: { en: 'Getting started', bn: 'কীভাবে শুরু করবে' },
    gs1: { en: '**Pick a technology** from the sidebar or the Technologies page. Each one has Easy, Medium, Hard and Extreme questions.', bn: 'Sidebar বা Technologies page থেকে **একটি টেকনোলজি বেছে নাও**। প্রতিটিতে Easy, Medium, Hard ও Extreme প্রশ্ন আছে।' },
    gs2: { en: '**Answer out loud first**, then reveal the reference answer and rate yourself honestly: correct, partial or incorrect.', bn: '**আগে নিজে জোরে উত্তর দাও**, তারপর reference answer দেখে নিজেকে সৎভাবে মূল্যায়ন করো: সঠিক, আংশিক বা ভুল।' },
    gs3: { en: '**Run practice sessions** or a mock interview. MCQs are graded automatically; scores are weighted by difficulty.', bn: '**প্র্যাকটিস সেশন** বা মক ইন্টারভিউ দাও। MCQ নিজে থেকেই grade হয়; score difficulty অনুযায়ী weighted।' },
    gs4: { en: '**Review your mistakes** — incorrect and partial answers come back on a simple spaced schedule.', bn: '**ভুলগুলো রিভিউ করো** — ভুল ও আংশিক উত্তরগুলো একটি সহজ spaced schedule-এ আবার ফিরে আসে।' },
    yourStats: { en: 'Your statistics', bn: 'তোমার পরিসংখ্যান' },
    statTotal: { en: 'Total questions', bn: 'মোট প্রশ্ন' },
    statAnswered: { en: 'Answered', bn: 'উত্তর দিয়েছ' },
    ofTotal: { en: 'of {n}', bn: '{n}টির মধ্যে' },
    technologiesWord: { en: 'technologies', bn: 'টেকনোলজি' },
    accuracy: { en: 'Accuracy', bn: 'নির্ভুলতা' },
    accuracyHint: { en: 'Correct ÷ answered (skips excluded)', bn: 'সঠিক ÷ উত্তর দেওয়া (skip বাদে)' },
    weightedScore: { en: 'Weighted score', bn: 'Weighted স্কোর' },
    weightedHint: { en: 'Points earned ÷ points available', bn: 'অর্জিত পয়েন্ট ÷ মোট পয়েন্ট' },
    completion: { en: 'Completion', bn: 'সম্পন্ন' },
    completionLegend: { en: 'answered or learned / total', bn: 'উত্তর দেওয়া বা শেখা / মোট' },
    needsReview: { en: 'Needs review', bn: 'রিভিউ দরকার' },
    dueToday: { en: '{n} due today', bn: 'আজ {n}টি বাকি' },
    studyStreak: { en: 'Study streak', bn: 'স্টাডি স্ট্রিক' },
    daysN: { en: '{n} day{s}', bn: '{n} দিন' },
    bestStreak: { en: 'Best: {n} day{s}', bn: 'সেরা: {n} দিন' },
    todaysGoal: { en: 'Today’s goal', bn: 'আজকের লক্ষ্য' },
    activitiesToday: { en: 'questions studied today', bn: 'আজ পড়া প্রশ্ন' },
    goalDone: { en: 'Daily goal reached — great work!', bn: 'আজকের লক্ষ্য পূরণ — দারুণ!' },
    goalLeft: { en: '{n} more to reach today’s goal.', bn: 'আজকের লক্ষ্য পূরণে আর {n}টি বাকি।' },
    recentSessions: { en: 'Recent sessions', bn: 'সাম্প্রতিক সেশন' },
    viewAll: { en: 'View all', bn: 'সব দেখো' },
    noSessionsYet: { en: 'No practice sessions yet. Your results will appear here.', bn: 'এখনও কোনো প্র্যাকটিস সেশন হয়নি। তোমার ফলাফল এখানে দেখাবে।' },
    qShort: { en: 'Q', bn: 'প্রশ্ন' },
    techProgress: { en: 'Technology progress', bn: 'টেকনোলজি অনুযায়ী অগ্রগতি' },
    difficultyDist: { en: 'Difficulty distribution', bn: 'Difficulty অনুযায়ী বিন্যাস' },
    pointsEach: { en: 'Points', bn: 'পয়েন্ট' },
    extremeNote: { en: 'Extreme questions are advanced, senior-level material — not mandatory preparation for junior roles.', bn: 'Extreme প্রশ্নগুলো senior-level-এর advanced বিষয় — junior role-এর জন্য বাধ্যতামূলক প্রস্তুতি নয়।' },
    weakTopics: { en: 'Weak topics', bn: 'দুর্বল বিষয়' },
    seePlan: { en: 'See plan', bn: 'প্ল্যান দেখো' },
    missRate: { en: 'Miss rate (incorrect + half of partial)', bn: 'ভুলের হার (ভুল + আংশিকের অর্ধেক)' },
    missRateShort: { en: '{n}% missed', bn: '{n}% ভুল' },
    practice: { en: 'Practice', bn: 'প্র্যাকটিস' },
    dailyIntroShort: { en: 'Three questions picked for today: one MCQ, one medium and one hard question.', bn: 'আজকের জন্য তিনটি প্রশ্ন: একটি MCQ, একটি medium আর একটি hard।' },
    dailyDoneShort: { en: 'Done for today — you scored {score}. Come back tomorrow for a new set.', bn: 'আজকের চ্যালেঞ্জ শেষ — তোমার স্কোর {score}। নতুন সেটের জন্য কাল আবার এসো।' },
    startChallenge: { en: 'Start challenge', bn: 'চ্যালেঞ্জ শুরু করো' },
    viewChallenge: { en: 'View challenge', bn: 'চ্যালেঞ্জ দেখো' },
    bankEmpty: { en: 'No questions loaded', bn: 'কোনো প্রশ্ন লোড হয়নি' },
    bankEmptyText: { en: 'questions.js could not be loaded or is empty. Make sure it sits next to index.html.', bn: 'questions.js লোড হয়নি বা খালি। ফাইলটি index.html-এর পাশে আছে কিনা দেখো।' },
    storageNoticeTitle: { en: 'About your saved progress', bn: 'তোমার সেভ করা অগ্রগতি সম্পর্কে' },
    storageCorrupt: { en: 'Saved progress was unreadable, so a fresh profile was started. The damaged data was kept as a backup copy in this browser.', bn: 'সেভ করা অগ্রগতি পড়া যায়নি, তাই নতুন profile শুরু হয়েছে। নষ্ট data-টি এই browser-এ backup হিসেবে রাখা আছে।' },
    storageIncompatible: { en: 'Saved progress came from an incompatible version, so a fresh profile was started. The old data was kept as a backup copy.', bn: 'সেভ করা অগ্রগতি একটি অসামঞ্জস্যপূর্ণ ভার্সনের, তাই নতুন profile শুরু হয়েছে। পুরোনো data backup হিসেবে রাখা আছে।' },
    storageUnavailable: { en: 'Browser storage is unavailable (private mode or blocked). You can study, but progress will not be saved after you close the page.', bn: 'Browser storage পাওয়া যাচ্ছে না (private mode বা blocked)। পড়তে পারবে, কিন্তু page বন্ধ করলে অগ্রগতি সেভ থাকবে না।' },
    storageFull: { en: 'Could not save progress: browser storage is full.', bn: 'অগ্রগতি সেভ করা যায়নি: browser storage পূর্ণ।' },

    // Technologies
    techLead: { en: 'All 18 technologies with real question counts by difficulty and your completion.', bn: '১৮টি টেকনোলজি — difficulty অনুযায়ী প্রকৃত প্রশ্ন সংখ্যা ও তোমার অগ্রগতিসহ।' },
    searchTechs: { en: 'Search technologies…', bn: 'টেকনোলজি খুঁজুন…' },
    search: { en: 'Search', bn: 'খুঁজুন' },
    sortBy: { en: 'Sort by', bn: 'সাজাও' },
    sortDefault: { en: 'Default order', bn: 'ডিফল্ট ক্রম' },
    sortName: { en: 'Name (A–Z)', bn: 'নাম (A–Z)' },
    sortCount: { en: 'Most questions', bn: 'বেশি প্রশ্ন আগে' },
    sortProgressDesc: { en: 'Progress (high → low)', bn: 'অগ্রগতি (বেশি → কম)' },
    sortProgressAsc: { en: 'Progress (low → high)', bn: 'অগ্রগতি (কম → বেশি)' },
    filterGroup: { en: 'Area', bn: 'ক্ষেত্র' },
    group_all: { en: 'All', bn: 'সব' },
    group_frontend: { en: 'Frontend', bn: 'Frontend' },
    group_backend: { en: 'Backend', bn: 'Backend' },
    group_database: { en: 'Databases', bn: 'Database' },
    group_devops: { en: 'DevOps & Cloud', bn: 'DevOps ও Cloud' },
    group_ai: { en: 'AI & Search', bn: 'AI ও Search' },
    noTechMatch: { en: 'No technology matches', bn: 'কোনো টেকনোলজি মেলেনি' },
    tryDifferent: { en: 'Try a different search or area.', bn: 'অন্য কিছু লিখে বা অন্য ক্ষেত্র বেছে চেষ্টা করো।' },
    questionsWord: { en: 'questions', bn: 'প্রশ্ন' },
    completeWord: { en: 'complete', bn: 'সম্পন্ন' },
    startLearning: { en: 'Start learning', bn: 'শেখা শুরু করো' },

    // Explorer
    questionsLead: { en: 'Search in English or Bangla, combine filters, and open any question.', bn: 'English বা বাংলায় খোঁজো, একাধিক filter একসাথে ব্যবহার করো, যেকোনো প্রশ্ন খোলো।' },
    filters: { en: 'Filters', bn: 'ফিল্টার' },
    filter: { en: 'Filter', bn: 'ফিল্টার' },
    searchLabel: { en: 'Search (English, বাংলা, tags, subtopics)', bn: 'খুঁজুন (English, বাংলা, tag, subtopic)' },
    searchPlaceholder: { en: 'e.g. closure, event loop, ইনডেক্স, cache…', bn: 'যেমন: closure, event loop, index, cache…' },
    technology: { en: 'Technology', bn: 'টেকনোলজি' },
    technologies: { en: 'Technologies', bn: 'টেকনোলজি' },
    difficulty: { en: 'Difficulty', bn: 'কঠিনতা' },
    questionType: { en: 'Question type', bn: 'প্রশ্নের ধরন' },
    questionTypes: { en: 'Question types', bn: 'প্রশ্নের ধরন' },
    market: { en: 'Market relevance', bn: 'মার্কেট প্রাসঙ্গিকতা' },
    allTechs: { en: 'All technologies', bn: 'সব টেকনোলজি' },
    allLevels: { en: 'All levels', bn: 'সব লেভেল' },
    allTypes: { en: 'All types', bn: 'সব ধরন' },
    allMarkets: { en: 'All markets', bn: 'সব মার্কেট' },
    onlyBookmarked: { en: 'Bookmarked only', bn: 'শুধু বুকমার্ক' },
    onlyIncorrect: { en: 'Incorrect only', bn: 'শুধু ভুল' },
    onlyUnanswered: { en: 'Unanswered only', bn: 'শুধু উত্তর না দেওয়া' },
    onlyLearned: { en: 'Learned only', bn: 'শুধু শেখা' },
    onlyReview: { en: 'Needs review only', bn: 'শুধু রিভিউ দরকার' },
    sortRelevance: { en: 'Default / relevance', bn: 'ডিফল্ট / প্রাসঙ্গিকতা' },
    sortDiffAsc: { en: 'Difficulty (easy → extreme)', bn: 'কঠিনতা (সহজ → কঠিন)' },
    sortDiffDesc: { en: 'Difficulty (extreme → easy)', bn: 'কঠিনতা (কঠিন → সহজ)' },
    sortPriority: { en: 'Priority (high first)', bn: 'অগ্রাধিকার (high আগে)' },
    sortRecent: { en: 'Recently practiced', bn: 'সম্প্রতি প্র্যাকটিস করা' },
    clearFilters: { en: 'Clear all filters', bn: 'সব ফিল্টার মুছে ফেলো' },
    matchingQuestions: { en: 'matching questions', bn: 'টি প্রশ্ন মিলেছে' },
    showingRange: { en: 'showing {a}–{b}', bn: '{a}–{b} দেখানো হচ্ছে' },
    noMatchTitle: { en: 'No questions match these filters', bn: 'এই ফিল্টারে কোনো প্রশ্ন মেলেনি' },
    noMatchText: { en: 'Try removing a filter, checking the spelling, or searching in the other language.', bn: 'একটি ফিল্টার সরিয়ে, বানান দেখে, বা অন্য ভাষায় খুঁজে চেষ্টা করো।' },
    pagination: { en: 'Pagination', bn: 'পেজ' },
    prev: { en: 'Prev', bn: 'আগের' },
    next: { en: 'Next', bn: 'পরের' },
    previous: { en: 'Previous', bn: 'আগের' },
    pageXofY: { en: 'Page {x} of {y}', bn: 'পেজ {x} / {y}' },
    practiceThese: { en: 'Practice these', bn: 'এগুলো প্র্যাকটিস করো' },
    nothingToPractice: { en: 'There are no questions to practice here yet.', bn: 'এখানে প্র্যাকটিস করার মতো কোনো প্রশ্ন নেই।' },
    minN: { en: '{n} min', bn: '{n} মিনিট' },

    // Question detail
    backToQuestions: { en: 'All questions', bn: 'সব প্রশ্ন' },
    studyMode: { en: 'Study mode', bn: 'স্টাডি মোড' },
    learningMode: { en: 'Learning', bn: 'শেখা' },
    interviewMode: { en: 'Interview', bn: 'ইন্টারভিউ' },
    estimatedTime: { en: 'Estimated answer time', bn: 'আনুমানিক উত্তরের সময়' },
    versionSensitive: { en: 'Version-sensitive', bn: 'ভার্সন-নির্ভর' },
    thinkFirst: { en: 'Answer it yourself first', bn: 'আগে নিজে উত্তর দাও' },
    answerAloud: { en: 'Answer out loud, like a real interview', bn: 'আসল ইন্টারভিউর মতো জোরে উত্তর দাও' },
    thinkFirstText: { en: 'Take about {n} min to structure your answer — say it out loud or jot down key points. Reveal the reference whenever you’re ready.', bn: 'প্রায় {n} মিনিট নিয়ে উত্তর সাজাও — জোরে বলো বা মূল পয়েন্টগুলো লিখে ফেলো। প্রস্তুত হলে যেকোনো সময় reference answer দেখো।' },
    revealAnswer: { en: 'Reveal answer', bn: 'উত্তর দেখো' },
    hideAnswer: { en: 'Hide answer', bn: 'উত্তর লুকাও' },
    revealWithoutAnswering: { en: 'Just show me the answer', bn: 'সরাসরি উত্তর দেখাও' },
    answerSection: { en: 'Reference answer', bn: 'রেফারেন্স উত্তর' },
    referenceAnswer: { en: 'Answer', bn: 'উত্তর' },
    explanation: { en: 'Explanation', bn: 'ব্যাখ্যা' },
    commonMistakes: { en: 'Common mistakes', bn: 'সাধারণ ভুল' },
    interviewTip: { en: 'Interview tip', bn: 'ইন্টারভিউ টিপ' },
    followUps: { en: 'Likely follow-up questions', bn: 'সম্ভাব্য follow-up প্রশ্ন' },
    references: { en: 'Official documentation', bn: 'অফিসিয়াল ডকুমেন্টেশন' },
    referenceSolution: { en: 'Reference solution', bn: 'রেফারেন্স সমাধান' },
    query: { en: 'Query', bn: 'Query' },
    codeExample: { en: 'Example', bn: 'উদাহরণ' },
    buggyCode: { en: 'Code', bn: 'কোড' },
    schemaAndData: { en: 'Schema & sample data', bn: 'Schema ও sample data' },
    expectedOutput: { en: 'expected output', bn: 'প্রত্যাশিত output' },
    timeComplexity: { en: 'Time', bn: 'Time' },
    spaceComplexity: { en: 'Space', bn: 'Space' },
    copy: { en: 'Copy', bn: 'কপি' },
    copied: { en: 'Copied', bn: 'কপি হয়েছে' },
    copyFailed: { en: 'Copy failed', bn: 'কপি হয়নি' },
    copyCode: { en: 'Copy code', bn: 'কোড কপি করো' },
    howDidYouDo: { en: 'How did you do?', bn: 'তুমি কেমন করলে?' },
    selfAssess: { en: 'Self-assessment', bn: 'নিজের মূল্যায়ন' },
    selfAssessHelp: { en: 'Compare your answer with the reference. Be honest — this drives your review schedule and weak-topic detection.', bn: 'তোমার উত্তর reference-এর সাথে মিলিয়ে দেখো। সৎ থাকো — এর উপর ভিত্তি করেই রিভিউ schedule আর দুর্বল বিষয় নির্ধারিত হয়।' },
    savedResult: { en: 'Saved: {r}', bn: 'সেভ হয়েছে: {r}' },
    recorded: { en: 'recorded', bn: 'রেকর্ড হবে' },
    skip: { en: 'Skip', bn: 'বাদ দাও' },
    chooseAnswer: { en: 'Choose one answer', bn: 'একটি উত্তর বেছে নাও' },
    submitAnswer: { en: 'Submit answer', bn: 'উত্তর জমা দাও' },
    mcqOnce: { en: 'Each attempt is scored once.', bn: 'প্রতিটি চেষ্টা একবারই score হয়।' },
    mcqCorrect: { en: 'Correct! Option {key} is right.', bn: 'সঠিক! Option {key}-ই ঠিক উত্তর।' },
    mcqWrong: { en: 'Not quite — the correct answer is {key}.', bn: 'হয়নি — সঠিক উত্তর হলো {key}।' },
    correctAnswer: { en: 'Correct answer', bn: 'সঠিক উত্তর' },
    yourAnswer: { en: 'Your answer', bn: 'তোমার উত্তর' },
    questionNav: { en: 'Question navigation', bn: 'প্রশ্ন নেভিগেশন' },
    questionTools: { en: 'Question tools', bn: 'প্রশ্নের টুলস' },
    myStatus: { en: 'My status', bn: 'আমার অবস্থা' },
    bookmark: { en: 'Bookmark', bn: 'বুকমার্ক করো' },
    bookmarked: { en: 'Bookmarked', bn: 'বুকমার্ক করা' },
    addedBookmark: { en: 'Added to bookmarks', bn: 'বুকমার্কে যোগ হয়েছে' },
    removedBookmark: { en: 'Removed from bookmarks', bn: 'বুকমার্ক থেকে সরানো হয়েছে' },
    markLearned: { en: 'Mark as learned', bn: 'শেখা হয়েছে চিহ্ন দাও' },
    learned: { en: 'Learned', bn: 'শেখা হয়েছে' },
    flagReview: { en: 'Flag for review', bn: 'রিভিউয়ের জন্য চিহ্ন দাও' },
    flagged: { en: 'Flagged for review', bn: 'রিভিউয়ের জন্য চিহ্নিত' },
    needsReviewBtn: { en: 'Needs review', bn: 'রিভিউ দরকার' },
    lastResult: { en: 'Latest result', bn: 'সর্বশেষ ফলাফল' },
    attempts: { en: 'Attempts', bn: 'চেষ্টা' },
    nextReview: { en: 'Next review', bn: 'পরের রিভিউ' },
    versionInfo: { en: 'Version information', bn: 'ভার্সন তথ্য' },
    version: { en: 'Version', bn: 'ভার্সন' },
    featureStatus: { en: 'Feature status', bn: 'Feature-এর অবস্থা' },
    verified: { en: 'Verified', bn: 'যাচাই করা হয়েছে' },
    officialDocs: { en: 'Docs', bn: 'ডকুমেন্টেশন' },
    openDocs: { en: 'Open official docs', bn: 'অফিসিয়াল docs খোলো' },
    yes: { en: 'Yes', bn: 'হ্যাঁ' },
    no: { en: 'No', bn: 'না' },
    relatedQuestions: { en: 'Related questions', bn: 'সম্পর্কিত প্রশ্ন' },
    noTranslation: { en: 'Translation not available — showing English.', bn: 'বাংলা অনুবাদ নেই — English দেখানো হচ্ছে।' },

    // Labels for enums
    diff_easy: { en: 'Easy', bn: 'সহজ' },
    diff_medium: { en: 'Medium', bn: 'মাঝারি' },
    diff_hard: { en: 'Hard', bn: 'কঠিন' },
    diff_extreme: { en: 'Extreme', bn: 'এক্সট্রিম' },
    type_conceptual: { en: 'Conceptual', bn: 'ধারণাগত' },
    type_output: { en: 'Output prediction', bn: 'Output অনুমান' },
    type_coding: { en: 'Coding', bn: 'কোডিং' },
    type_debugging: { en: 'Debugging', bn: 'ডিবাগিং' },
    type_scenario: { en: 'Scenario', bn: 'পরিস্থিতিভিত্তিক' },
    'type_comparison': { en: 'Comparison', bn: 'তুলনা' },
    'type_system-design': { en: 'System design', bn: 'System design' },
    type_query: { en: 'Database query', bn: 'Database query' },
    type_architecture: { en: 'Architecture', bn: 'Architecture' },
    'type_security-performance': { en: 'Security & performance', bn: 'Security ও performance' },
    type_mcq: { en: 'MCQ', bn: 'MCQ' },
    market_both: { en: 'BD + Global', bn: 'বাংলাদেশ + আন্তর্জাতিক' },
    market_bangladesh: { en: 'Bangladesh', bn: 'বাংলাদেশ' },
    market_international: { en: 'International', bn: 'আন্তর্জাতিক' },
    priority: { en: 'Priority', bn: 'অগ্রাধিকার' },
    prio_high: { en: 'High priority', bn: 'উচ্চ অগ্রাধিকার' },
    prio_medium: { en: 'Medium priority', bn: 'মাঝারি অগ্রাধিকার' },
    prio_low: { en: 'Low priority', bn: 'কম অগ্রাধিকার' },
    res_correct: { en: 'Correct', bn: 'সঠিক' },
    res_partial: { en: 'Partially correct', bn: 'আংশিক সঠিক' },
    res_incorrect: { en: 'Incorrect', bn: 'ভুল' },
    res_skipped: { en: 'Skipped', bn: 'বাদ দেওয়া' },
    res_none: { en: 'Not attempted', bn: 'চেষ্টা করা হয়নি' },
    st_stable: { en: 'Stable', bn: 'Stable' },
    st_legacy: { en: 'Legacy', bn: 'Legacy' },
    st_deprecated: { en: 'Deprecated', bn: 'Deprecated' },
    st_experimental: { en: 'Experimental', bn: 'Experimental' },
    st_preview: { en: 'Preview / RC', bn: 'Preview / RC' },
    'st_version-specific': { en: 'Version-specific', bn: 'ভার্সন-নির্দিষ্ট' },
    kind_practice: { en: 'Practice session', bn: 'প্র্যাকটিস সেশন' },
    kind_interview: { en: 'Mock interview', bn: 'মক ইন্টারভিউ' },
    kind_daily: { en: 'Daily challenge', bn: 'আজকের চ্যালেঞ্জ' },

    // Practice
    practiceLead: { en: 'Choose a preset or build a custom session. Reference answers stay hidden until you reveal them.', bn: 'একটি preset বেছে নাও বা নিজের মতো সেশন বানাও। তুমি না চাইলে reference answer লুকানো থাকবে।' },
    preset_quick: { en: 'Quick Practice', bn: 'দ্রুত প্র্যাকটিস' },
    preset_focus: { en: 'Focus Session', bn: 'ফোকাস সেশন' },
    preset_deep: { en: 'Deep Practice', bn: 'গভীর প্র্যাকটিস' },
    preset_custom: { en: 'Custom Practice', bn: 'কাস্টম প্র্যাকটিস' },
    presetCustomHint: { en: 'Pick any number', bn: 'যেকোনো সংখ্যা' },
    nQuestions: { en: '{n} questions', bn: '{n}টি প্রশ্ন' },
    numberOfQuestions: { en: 'Number of questions', bn: 'প্রশ্নের সংখ্যা' },
    all: { en: 'All', bn: 'সব' },
    selection: { en: 'Selection', bn: 'বাছাই পদ্ধতি' },
    randomized: { en: 'Randomized', bn: 'এলোমেলো' },
    priorityBased: { en: 'Priority-based', bn: 'অগ্রাধিকারভিত্তিক' },
    questionPool: { en: 'Question pool', bn: 'প্রশ্নের পুল' },
    poolAll: { en: 'All questions', bn: 'সব প্রশ্ন' },
    poolUnanswered: { en: 'Unanswered only', bn: 'শুধু উত্তর না দেওয়া' },
    poolAnswered: { en: 'Previously answered only', bn: 'শুধু আগে উত্তর দেওয়া' },
    poolMistakes: { en: 'My mistakes (incorrect + partial)', bn: 'আমার ভুলগুলো (ভুল + আংশিক)' },
    timer: { en: 'Timer', bn: 'টাইমার' },
    untimed: { en: 'Untimed', bn: 'সময়সীমা নেই' },
    minutesN: { en: '{n} minutes', bn: '{n} মিনিট' },
    startSession: { en: 'Start session', bn: 'সেশন শুরু করো' },
    noneMatchConfig: { en: 'No questions match this configuration. Remove a filter or choose a different question pool.', bn: 'এই কনফিগারেশনে কোনো প্রশ্ন মেলেনি। একটি filter সরাও বা অন্য question pool বেছে নাও।' },
    noneMatchShort: { en: 'No questions match these settings.', bn: 'এই সেটিংসে কোনো প্রশ্ন মেলেনি।' },
    fewerThanRequested: { en: 'Only {n} questions match, but you asked for {c}. Questions are never repeated to fill a session.', bn: 'মাত্র {n}টি প্রশ্ন মিলেছে, কিন্তু তুমি {c}টি চেয়েছ। সেশন পূরণ করতে কোনো প্রশ্ন পুনরাবৃত্তি করা হয় না।' },
    notEnoughTitle: { en: 'Not enough questions', bn: 'যথেষ্ট প্রশ্ন নেই' },
    startWithN: { en: 'Start with {n}', bn: '{n}টি দিয়ে শুরু করো' },
    unfinishedSession: { en: 'You have an unfinished session', bn: 'তোমার একটি অসমাপ্ত সেশন আছে' },
    unfinishedText: { en: '{n} of {total} questions answered. Resume where you left off, or finish it now.', bn: '{total}টির মধ্যে {n}টি উত্তর দেওয়া হয়েছে। যেখানে ছেড়েছিলে সেখান থেকে শুরু করো, অথবা এখনই শেষ করো।' },
    finishNow: { en: 'Finish now', bn: 'এখনই শেষ করো' },
    howScoringWorks: { en: 'How scoring works', bn: 'স্কোর যেভাবে হিসাব হয়' },
    scoringExplain: { en: 'Points by difficulty: Easy 1 · Medium 2 · Hard 3 · Extreme 4. Correct earns 100% of the points, partially correct 50%, incorrect and skipped 0% (skips are counted separately). **Weighted score** = points earned ÷ points available × 100. **Accuracy** = correct ÷ answered, excluding skips. Revealing an answer is never penalised. MCQs are graded automatically; everything else is self-assessed against the reference answer.', bn: 'Difficulty অনুযায়ী পয়েন্ট: Easy 1 · Medium 2 · Hard 3 · Extreme 4। সঠিক হলে পুরো পয়েন্ট, আংশিক সঠিক হলে ৫০%, ভুল বা skip হলে ০% (skip আলাদাভাবে গোনা হয়)। **Weighted স্কোর** = অর্জিত পয়েন্ট ÷ মোট পয়েন্ট × ১০০। **নির্ভুলতা** = সঠিক ÷ উত্তর দেওয়া (skip বাদে)। উত্তর দেখলে কোনো পয়েন্ট কাটা হয় না। MCQ নিজে থেকে grade হয়; বাকিগুলো reference answer-এর সাথে মিলিয়ে নিজে মূল্যায়ন করতে হয়।' },
    replaceSessionTitle: { en: 'Start a new session?', bn: 'নতুন সেশন শুরু করবে?' },
    replaceSessionText: { en: 'Your current session will be finished and saved to your history (unanswered questions count as skipped).', bn: 'তোমার বর্তমান সেশনটি শেষ হয়ে history-তে সেভ হবে (উত্তর না দেওয়া প্রশ্নগুলো skip হিসেবে গোনা হবে)।' },
    startNew: { en: 'Start new session', bn: 'নতুন সেশন শুরু করো' },

    // Session
    noActiveSession: { en: 'No active session', bn: 'কোনো সক্রিয় সেশন নেই' },
    noActiveSessionText: { en: 'Start a practice session or a mock interview to begin.', bn: 'শুরু করতে একটি প্র্যাকটিস সেশন বা মক ইন্টারভিউ শুরু করো।' },
    questionXofY: { en: 'Question {x} of {y}', bn: 'প্রশ্ন {x} / {y}' },
    questionN: { en: 'Question {n}', bn: 'প্রশ্ন {n}' },
    sessionProgress: { en: 'Session progress', bn: 'সেশনের অগ্রগতি' },
    doneWord: { en: 'done', bn: 'সম্পন্ন' },
    endSession: { en: 'End', bn: 'শেষ করো' },
    finishSession: { en: 'Finish session', bn: 'সেশন শেষ করো' },
    seeResults: { en: 'See results', bn: 'ফলাফল দেখো' },
    endSessionTitle: { en: 'End this session?', bn: 'সেশন শেষ করবে?' },
    endSessionText: { en: '{n} question(s) are still unanswered and will be recorded as skipped in this session’s score.', bn: 'এখনও {n}টি প্রশ্নের উত্তর দেওয়া হয়নি; এই সেশনের স্কোরে সেগুলো skip হিসেবে গোনা হবে।' },
    timeRemaining: { en: 'Time remaining', bn: 'বাকি সময়' },
    timeElapsed: { en: 'Time elapsed', bn: 'অতিবাহিত সময়' },
    thinkTime: { en: 'Time on this question', bn: 'এই প্রশ্নে সময়' },
    timeUp: { en: 'Time is up — your session has been submitted.', bn: 'সময় শেষ — তোমার সেশন জমা হয়েছে।' },
    shortcutsHint: { en: 'Shortcuts: Space reveal · 1 correct · 2 partial · 3 incorrect · S skip · ←/→ navigate · B bookmark · F flag', bn: 'শর্টকাট: Space উত্তর দেখো · 1 সঠিক · 2 আংশিক · 3 ভুল · S বাদ · ←/→ নেভিগেট · B বুকমার্ক · F চিহ্ন' },

    // Results
    results: { en: 'Results', bn: 'ফলাফল' },
    sessionStats: { en: 'Session statistics', bn: 'সেশনের পরিসংখ্যান' },
    finalScore: { en: 'Final score', bn: 'চূড়ান্ত স্কোর' },
    pointsWord: { en: 'weighted points', bn: 'weighted পয়েন্ট' },
    points: { en: 'Points', bn: 'পয়েন্ট' },
    completionTime: { en: 'Completion time', bn: 'সম্পন্ন করার সময়' },
    skippedWord: { en: 'Skipped', bn: 'বাদ দেওয়া' },
    skippedHint: { en: 'Includes unanswered', bn: 'উত্তর না দেওয়াগুলোসহ' },
    byTechnology: { en: 'Results by technology', bn: 'টেকনোলজি অনুযায়ী ফলাফল' },
    byDifficulty: { en: 'Results by difficulty', bn: 'Difficulty অনুযায়ী ফলাফল' },
    questionsToReview: { en: 'Questions to review', bn: 'রিভিউ করার মতো প্রশ্ন' },
    nothingToReview: { en: 'Everything was correct — nothing to review from this session.', bn: 'সবগুলো সঠিক — এই সেশন থেকে রিভিউ করার কিছু নেই।' },
    reviewMistakes: { en: 'Review mistakes', bn: 'ভুলগুলো রিভিউ করো' },
    practiceAgain: { en: 'Practice again', bn: 'আবার প্র্যাকটিস করো' },
    returnDashboard: { en: 'Dashboard', bn: 'ড্যাশবোর্ড' },
    fbExcellent: { en: 'Excellent work!', bn: 'অসাধারণ!' },
    fbExcellentText: { en: 'You’re answering at a strong level. Try harder difficulties or a timed mock interview next.', bn: 'তুমি বেশ শক্ত লেভেলে উত্তর দিচ্ছ। এবার আরও কঠিন প্রশ্ন বা সময় বেঁধে মক ইন্টারভিউ দাও।' },
    fbGood: { en: 'Good session!', bn: 'ভালো সেশন!' },
    fbGoodText: { en: 'Solid progress. Review the partial answers — closing those gaps gives the biggest jump.', bn: 'ভালো অগ্রগতি। আংশিক উত্তরগুলো রিভিউ করো — ওই ফাঁকগুলো পূরণ করলেই সবচেয়ে বেশি উন্নতি হবে।' },
    fbProgress: { en: 'You’re making progress', bn: 'তুমি এগোচ্ছ' },
    fbProgressText: { en: 'Every reviewed mistake is one less surprise in a real interview. Go through the questions below and try again.', bn: 'প্রতিটি রিভিউ করা ভুল মানে আসল ইন্টারভিউতে একটি কম চমক। নিচের প্রশ্নগুলো দেখে আবার চেষ্টা করো।' },
    fbKeepGoing: { en: 'Keep going — this is how learning works', bn: 'চালিয়ে যাও — শেখা এভাবেই হয়' },
    fbKeepGoingText: { en: 'Low scores early on are normal. Read the explanations, mark tricky ones for review, and start with Easy questions.', bn: 'শুরুতে কম স্কোর স্বাভাবিক। ব্যাখ্যাগুলো পড়ো, কঠিনগুলো রিভিউয়ের জন্য চিহ্নিত করো, আর Easy প্রশ্ন দিয়ে শুরু করো।' },
    sessionNotFound: { en: 'Session not found', bn: 'সেশন পাওয়া যায়নি' },
    sessionNotFoundText: { en: 'It may have been removed when progress was reset or imported.', bn: 'Progress reset বা import করার সময় এটি মুছে যেতে পারে।' },

    // Interview simulation
    interviewLead: { en: 'Questions arrive one at a time with answers hidden — just like a real technical round.', bn: 'আসল technical round-এর মতো প্রশ্ন একটা একটা করে আসবে, উত্তর লুকানো থাকবে।' },
    timeLimit: { en: 'Time limit', bn: 'সময়সীমা' },
    none: { en: 'None', bn: 'নেই' },
    includeMcq: { en: 'Include multiple-choice questions', bn: 'MCQ প্রশ্নও রাখো' },
    startInterview: { en: 'Start mock interview', bn: 'মক ইন্টারভিউ শুরু করো' },
    unfinishedInterview: { en: 'You have a mock interview in progress', bn: 'তোমার একটি মক ইন্টারভিউ চলছে' },
    howInterviewWorks: { en: 'How it works', bn: 'কীভাবে কাজ করে' },
    iw1: { en: 'Questions are ordered from easier to harder, like most real interviews.', bn: 'বেশিরভাগ আসল ইন্টারভিউর মতো প্রশ্নগুলো সহজ থেকে কঠিনের দিকে সাজানো।' },
    iw2: { en: 'Answer out loud before revealing. The timer shows how long you spend on each question.', bn: 'উত্তর দেখার আগে জোরে উত্তর দাও। প্রতিটি প্রশ্নে কত সময় লাগছে টাইমারে দেখা যাবে।' },
    iw3: { en: 'Rate yourself honestly against the reference answer, then move on.', bn: 'Reference answer-এর সাথে মিলিয়ে নিজেকে সৎভাবে মূল্যায়ন করো, তারপর এগিয়ে যাও।' },
    iw4: { en: 'With a time limit, the session is submitted automatically when time runs out.', bn: 'সময়সীমা দিলে সময় শেষ হলেই সেশন নিজে থেকে জমা হয়ে যাবে।' },

    // Daily
    dailyLead: { en: 'Three fresh questions every day, the same for everyone using this question bank — no server needed.', bn: 'প্রতিদিন তিনটি নতুন প্রশ্ন — এই question bank ব্যবহারকারী সবার জন্য একই, কোনো server লাগে না।' },
    hiddenUntilStart: { en: 'Revealed when you start', bn: 'শুরু করলে দেখা যাবে' },
    open: { en: 'Open', bn: 'খোলো' },
    viewResults: { en: 'View results', bn: 'ফলাফল দেখো' },
    dailyStatus: { en: 'Today', bn: 'আজ' },
    today: { en: 'Today', bn: 'আজ' },
    completed: { en: 'Completed', bn: 'সম্পন্ন' },
    notYet: { en: 'Not yet', bn: 'এখনও না' },
    dailyStreak: { en: 'Challenge streak', bn: 'চ্যালেঞ্জ স্ট্রিক' },
    dailyHow: { en: 'The set is chosen from your local date, so it changes at midnight on your device.', bn: 'তোমার device-এর তারিখ অনুযায়ী সেট বাছাই হয়, তাই মধ্যরাতে বদলে যায়।' },

    // Flashcards
    flashLead: { en: 'Rapid review: read the question, recall the answer, flip the card.', bn: 'দ্রুত রিভিউ: প্রশ্ন পড়ো, উত্তর মনে করো, তারপর কার্ড উল্টাও।' },
    deck: { en: 'Deck', bn: 'ডেক' },
    deckAll: { en: 'All questions', bn: 'সব প্রশ্ন' },
    deckUnlearned: { en: 'Not yet learned', bn: 'এখনও শেখা হয়নি' },
    deckDue: { en: 'Due / flagged for review', bn: 'রিভিউ বাকি / চিহ্নিত' },
    deckMistakes: { en: 'My mistakes', bn: 'আমার ভুলগুলো' },
    shuffle: { en: 'Shuffle', bn: 'এলোমেলো করো' },
    emptyDeck: { en: 'This deck is empty', bn: 'এই ডেকটি খালি' },
    emptyDeckText: { en: 'Choose another deck or technology.', bn: 'অন্য ডেক বা টেকনোলজি বেছে নাও।' },
    cardXofY: { en: 'Card {x} of {y}', bn: 'কার্ড {x} / {y}' },
    openFull: { en: 'Open full question', bn: 'পুরো প্রশ্ন খোলো' },
    tapToFlip: { en: 'Click or press Space to flip', bn: 'উল্টাতে ক্লিক করো বা Space চাপো' },
    flipCard: { en: 'Flip card', bn: 'কার্ড উল্টাও' },
    flip: { en: 'Flip', bn: 'উল্টাও' },
    flashKeys: { en: 'Space: flip · ←/→: previous / next', bn: 'Space: উল্টাও · ←/→: আগের / পরের' },

    // Bookmarks / incorrect / review
    bookmarksLead: { en: 'Questions you saved for later.', bn: 'পরে পড়ার জন্য সেভ করা প্রশ্ন।' },
    bookmarkedQuestions: { en: 'bookmarked questions', bn: 'টি বুকমার্ক করা প্রশ্ন' },
    noBookmarks: { en: 'No bookmarks yet', bn: 'এখনও কোনো বুকমার্ক নেই' },
    noBookmarksText: { en: 'Use the bookmark button on any question to save it here.', bn: 'যেকোনো প্রশ্নের বুকমার্ক বাটন চাপলে সেটি এখানে সেভ হবে।' },
    browseQuestions: { en: 'Browse questions', bn: 'প্রশ্নগুলো দেখো' },
    incorrectLead: { en: 'Questions whose latest result was incorrect or partially correct.', bn: 'যেসব প্রশ্নের সর্বশেষ ফলাফল ভুল বা আংশিক সঠিক।' },
    latestResultNote: { en: 'Based on your most recent attempt', bn: 'তোমার সর্বশেষ চেষ্টার উপর ভিত্তি করে' },
    practiceMistakes: { en: 'Practice my mistakes', bn: 'আমার ভুলগুলো প্র্যাকটিস করো' },
    noIncorrect: { en: 'No incorrect answers', bn: 'কোনো ভুল উত্তর নেই' },
    noPartial: { en: 'No partially correct answers', bn: 'কোনো আংশিক সঠিক উত্তর নেই' },
    noMistakesText: { en: 'Answers you mark as incorrect or partial will appear here so you can revisit them.', bn: 'যেগুলো ভুল বা আংশিক হিসেবে চিহ্নিত করবে, সেগুলো এখানে আসবে যাতে আবার দেখতে পারো।' },
    reviewLead: { en: 'Spaced review of past mistakes, plus questions you flagged yourself.', bn: 'আগের ভুলগুলোর spaced review, আর তুমি নিজে চিহ্নিত করা প্রশ্ন।' },
    reviewNow: { en: 'Review now', bn: 'এখনই রিভিউ করো' },
    reviewScheduleTitle: { en: 'How the review schedule works', bn: 'রিভিউ schedule কীভাবে কাজ করে' },
    reviewScheduleText: { en: 'A simple, transparent schedule (not an adaptive algorithm): an incorrect answer comes back tomorrow; a partial answer in 3 days. Each later correct answer pushes it further out — 7, 14, then 30 days — after which it leaves the queue. An incorrect answer at any point restarts the cycle.', bn: 'এটি একটি সহজ, স্বচ্ছ schedule (adaptive algorithm নয়): ভুল উত্তর পরের দিন আবার আসবে; আংশিক উত্তর ৩ দিন পর। পরে প্রতিবার সঠিক হলে আরও পিছিয়ে যায় — ৭, ১৪, তারপর ৩০ দিন — এরপর queue থেকে বের হয়ে যায়। যেকোনো সময় ভুল হলে আবার শুরু থেকে।' },
    dueForReview: { en: 'Due for review', bn: 'রিভিউ বাকি' },
    flaggedForReview: { en: 'Flagged for review', bn: 'রিভিউয়ের জন্য চিহ্নিত' },
    upcomingReviews: { en: 'Coming up in the next 7 days', bn: 'আগামী ৭ দিনে আসবে' },
    recentlyStudied: { en: 'Recently studied', bn: 'সম্প্রতি পড়া' },
    nothingDue: { en: 'Nothing is due today.', bn: 'আজ কিছু রিভিউ বাকি নেই।' },
    nothingFlagged: { en: 'You haven’t flagged any questions.', bn: 'তুমি কোনো প্রশ্ন চিহ্নিত করোনি।' },
    nothingUpcoming: { en: 'No reviews scheduled for the coming week.', bn: 'আগামী সপ্তাহে কোনো রিভিউ নেই।' },
    nothingRecent: { en: 'Questions you answer will be listed here.', bn: 'যেসব প্রশ্নের উত্তর দেবে সেগুলো এখানে দেখাবে।' },

    // History
    historyLead: { en: 'Every finished session with its score, plus your daily activity.', bn: 'প্রতিটি শেষ হওয়া সেশন ও তার স্কোর, সাথে তোমার দৈনিক activity।' },
    sessionsWord: { en: 'Sessions', bn: 'সেশন' },
    questionsPracticed: { en: 'Questions practiced', bn: 'প্র্যাকটিস করা প্রশ্ন' },
    timeSpent: { en: 'Time in sessions', bn: 'সেশনে মোট সময়' },
    activeDays: { en: 'Active days', bn: 'সক্রিয় দিন' },
    lastNWeeks: { en: 'last {n} weeks', bn: 'গত {n} সপ্তাহ' },
    activity: { en: 'Activity', bn: 'Activity' },
    heatmapLabel: { en: '{d} active days and {n} questions studied in the last {w} weeks', bn: 'গত {w} সপ্তাহে {d} দিন সক্রিয়, {n}টি প্রশ্ন পড়া হয়েছে' },
    less: { en: 'Less', bn: 'কম' },
    more: { en: 'More', bn: 'বেশি' },
    pastSessions: { en: 'Past sessions', bn: 'আগের সেশনগুলো' },
    date: { en: 'Date', bn: 'তারিখ' },
    typeWord: { en: 'Type', bn: 'ধরন' },
    duration: { en: 'Duration', bn: 'সময়' },
    details: { en: 'Details', bn: 'বিস্তারিত' },
    noHistory: { en: 'No sessions yet', bn: 'এখনও কোনো সেশন নেই' },
    noHistoryText: { en: 'Finished practice sessions, mock interviews and daily challenges are saved here.', bn: 'শেষ হওয়া প্র্যাকটিস সেশন, মক ইন্টারভিউ আর দৈনিক চ্যালেঞ্জ এখানে সেভ থাকে।' },

    // Planner
    plannerLead: { en: 'Set a daily target, track your week and get recommendations from your own results.', bn: 'দৈনিক লক্ষ্য ঠিক করো, সপ্তাহের অগ্রগতি দেখো, আর নিজের ফলাফল থেকে পরামর্শ পাও।' },
    dailyTarget: { en: 'Daily target', bn: 'দৈনিক লক্ষ্য' },
    questionsPerDay: { en: 'Questions per day', bn: 'প্রতিদিন প্রশ্ন' },
    interviewDate: { en: 'Interview date (optional)', bn: 'ইন্টারভিউর তারিখ (ঐচ্ছিক)' },
    save: { en: 'Save', bn: 'সেভ করো' },
    plannerSaved: { en: 'Planner saved', bn: 'প্ল্যানার সেভ হয়েছে' },
    invalidTarget: { en: 'Enter a daily target between 1 and 200.', bn: '১ থেকে ২০০-এর মধ্যে একটি দৈনিক লক্ষ্য দাও।' },
    todayProgress: { en: 'Today: {n} / {t}', bn: 'আজ: {n} / {t}' },
    activityDefinition: { en: 'Activity = each self-assessed or MCQ answer (not skips) plus questions you mark as learned.', bn: 'Activity মানে প্রতিটি নিজে মূল্যায়ন করা বা MCQ উত্তর (skip বাদে), আর যেসব প্রশ্ন “শেখা হয়েছে” চিহ্নিত করো।' },
    last7Days: { en: 'Last 7 days', bn: 'গত ৭ দিন' },
    goalLine: { en: 'Teal bars reached the daily target of {n}.', bn: 'সবুজাভ বারগুলো দৈনিক লক্ষ্য {n} পূরণ করেছে।' },
    remainingQuestions: { en: 'Remaining questions', bn: 'বাকি প্রশ্ন' },
    notAnsweredOrLearned: { en: 'not answered or learned yet', bn: 'এখনও উত্তর দেওয়া বা শেখা হয়নি' },
    daysUntilInterview: { en: 'Days until interview', bn: 'ইন্টারভিউর আর কত দিন' },
    passed: { en: 'Passed', bn: 'পার হয়ে গেছে' },
    setDateHint: { en: 'Set a date above', bn: 'উপরে একটি তারিখ দাও' },
    suggestedPerDay: { en: 'Suggested per day', bn: 'প্রতিদিন প্রস্তাবিত' },
    suggestedHint: { en: 'remaining ÷ days left', bn: 'বাকি প্রশ্ন ÷ বাকি দিন' },
    noWeakTopics: { en: 'Not enough data yet. Weak topics appear after at least two answered attempts in a subtopic with a mistake.', bn: 'এখনও যথেষ্ট data নেই। কোনো subtopic-এ অন্তত দুটি উত্তর ও একটি ভুল হলে দুর্বল বিষয় দেখাবে।' },
    missRateByDifficulty: { en: 'Miss rate by difficulty', bn: 'Difficulty অনুযায়ী ভুলের হার' },
    weakHow: { en: 'Calculated only from your recorded answers: (incorrect + ½ partial) ÷ attempts.', bn: 'শুধু তোমার রেকর্ড করা উত্তর থেকে হিসাব: (ভুল + ½ আংশিক) ÷ মোট চেষ্টা।' },
    recommendedNext: { en: 'Recommended next', bn: 'এরপর যা করা উচিত' },
    recDue: { en: 'You have **{n}** question(s) due for review.', bn: 'তোমার **{n}**টি প্রশ্ন রিভিউ বাকি।' },
    recDaily: { en: 'Do today’s three-question challenge to keep your streak.', bn: 'স্ট্রিক ধরে রাখতে আজকের তিন প্রশ্নের চ্যালেঞ্জটি দাও।' },
    recPractice: { en: 'Run a priority-based session of about {n} questions.', bn: 'প্রায় {n}টি প্রশ্নের একটি অগ্রাধিকারভিত্তিক সেশন দাও।' },
    recInterview: { en: 'Once a week, try a timed mock interview.', bn: 'সপ্তাহে একবার সময় বেঁধে মক ইন্টারভিউ দাও।' },

    // Settings
    settingsLead: { en: 'Preferences, backups and data tools. Everything stays in this browser.', bn: 'Preference, backup আর data টুলস। সবকিছু এই browser-এই থাকে।' },
    preferences: { en: 'Preferences', bn: 'পছন্দসমূহ' },
    theme: { en: 'Theme', bn: 'থিম' },
    dark: { en: 'Dark', bn: 'ডার্ক' },
    light: { en: 'Light', bn: 'লাইট' },
    defaultMode: { en: 'Question mode', bn: 'প্রশ্ন মোড' },
    defaultModeHint: { en: 'Learning shows answers right away; Interview hides them until you reveal.', bn: 'Learning মোডে উত্তর সাথে সাথে দেখায়; Interview মোডে তুমি না চাওয়া পর্যন্ত লুকানো থাকে।' },
    motion: { en: 'Animations', bn: 'অ্যানিমেশন' },
    motionHint: { en: 'System follows your OS “reduce motion” setting.', bn: 'System দিলে তোমার OS-এর “reduce motion” সেটিং মানা হবে।' },
    motionSystem: { en: 'System', bn: 'System' },
    motionReduce: { en: 'Reduced', bn: 'কম' },
    motionFull: { en: 'Full', bn: 'পূর্ণ' },
    textSize: { en: 'Text size', bn: 'লেখার আকার' },
    sidebar: { en: 'Sidebar', bn: 'সাইডবার' },
    expanded: { en: 'Expanded', bn: 'বড়' },
    collapsed: { en: 'Collapsed', bn: 'ছোট' },
    dataBackup: { en: 'Backup & restore', bn: 'Backup ও restore' },
    exportData: { en: 'Export JSON', bn: 'JSON export করো' },
    importData: { en: 'Import JSON', bn: 'JSON import করো' },
    importHint: { en: 'Imports are validated first and you confirm before anything is replaced. Malformed files are rejected without changing your data.', bn: 'Import করার আগে যাচাই করা হয় এবং কিছু বদলানোর আগে তোমার অনুমতি নেওয়া হয়। ভুল ফাইল হলে তোমার data না বদলেই বাতিল হয়।' },
    exported: { en: 'Backup downloaded', bn: 'Backup ডাউনলোড হয়েছে' },
    import_invalidJson: { en: 'That file is not valid JSON.', bn: 'ফাইলটি সঠিক JSON নয়।' },
    import_notBackup: { en: 'That file is not an Interview Prep BD backup.', bn: 'ফাইলটি Interview Prep BD-এর backup নয়।' },
    import_incompatible: { en: 'That backup comes from an incompatible version.', bn: 'Backup-টি একটি অসামঞ্জস্যপূর্ণ ভার্সনের।' },
    import_tooLarge: { en: 'That file is too large to be a backup.', bn: 'ফাইলটি backup হিসেবে অনেক বড়।' },
    import_readError: { en: 'The file could not be read.', bn: 'ফাইলটি পড়া যায়নি।' },
    importConfirmTitle: { en: 'Replace your data with this backup?', bn: 'এই backup দিয়ে তোমার data বদলে দেবে?' },
    importConfirmText: { en: 'Your current progress in this browser will be replaced by:', bn: 'এই browser-এ তোমার বর্তমান অগ্রগতি এগুলো দিয়ে বদলে যাবে:' },
    questionsWithProgress: { en: 'Questions with progress', bn: 'অগ্রগতিসহ প্রশ্ন' },
    exportedAt: { en: 'Exported at', bn: 'Export-এর সময়' },
    replaceMyData: { en: 'Replace my data', bn: 'আমার data বদলাও' },
    imported: { en: 'Backup imported', bn: 'Backup import হয়েছে' },
    dangerZone: { en: 'Reset', bn: 'রিসেট' },
    resetHint: { en: 'Deletes bookmarks, assessments, sessions, planner and activity. Preferences are kept. This cannot be undone — export a backup first.', bn: 'বুকমার্ক, মূল্যায়ন, সেশন, প্ল্যানার আর activity মুছে যাবে। Preference থাকবে। এটি ফেরানো যায় না — আগে একটি backup export করে নাও।' },
    resetProgress: { en: 'Reset progress', bn: 'অগ্রগতি রিসেট করো' },
    resetTitle: { en: 'Reset all progress?', bn: 'সব অগ্রগতি রিসেট করবে?' },
    resetText: { en: 'This permanently deletes your progress in this browser.', bn: 'এতে এই browser-এ তোমার অগ্রগতি স্থায়ীভাবে মুছে যাবে।' },
    typeToConfirm: { en: 'Type {word} to confirm', bn: 'নিশ্চিত করতে {word} লেখো' },
    progressReset: { en: 'Progress reset', bn: 'অগ্রগতি রিসেট হয়েছে' },
    dataHealth: { en: 'Question bank health', bn: 'Question bank-এর অবস্থা' },
    records: { en: 'Records', bn: 'রেকর্ড' },
    usableQuestions: { en: 'Usable questions', bn: 'ব্যবহারযোগ্য প্রশ্ন' },
    errors: { en: 'Errors', bn: 'ত্রুটি' },
    warnings: { en: 'Warnings', bn: 'সতর্কতা' },
    showDetails: { en: 'Show details', bn: 'বিস্তারিত দেখো' },
    noValidationIssues: { en: 'No validation issues found.', bn: 'যাচাইয়ে কোনো সমস্যা পাওয়া যায়নি।' },
    validationConsole: { en: 'The same report is printed to the browser console at startup.', bn: 'একই রিপোর্ট শুরুতেই browser console-এ দেখানো হয়।' },

    // Sources
    sourcesLead: { en: 'Technology versions verified for this question bank, the research sources used, and actual question counts.', bn: 'এই question bank-এর জন্য যাচাই করা টেকনোলজি ভার্সন, ব্যবহৃত গবেষণা সূত্র এবং প্রকৃত প্রশ্ন সংখ্যা।' },
    verifiedVersions: { en: 'Verified versions', bn: 'যাচাই করা ভার্সন' },
    notes: { en: 'Notes', bn: 'নোট' },
    source: { en: 'Source', bn: 'সূত্র' },
    versionsNote: { en: 'Checked on 2026-10-12 against official release notes and the npm registry. Software moves fast — re-check docs before relying on a version-specific detail.', bn: '২০২৬-১০-১২ তারিখে অফিসিয়াল release note ও npm registry থেকে যাচাই করা। Software দ্রুত বদলায় — ভার্সন-নির্দিষ্ট কিছুর উপর নির্ভর করার আগে docs আবার দেখে নিও।' },
    bankStats: { en: 'Question bank counts', bn: 'Question bank-এর সংখ্যা' },
    totalWord: { en: 'Total', bn: 'মোট' },
    honestyTitle: { en: 'About priorities and market labels', bn: 'অগ্রাধিকার ও মার্কেট লেবেল সম্পর্কে' },
    honestyText: { en: 'Priority and market labels are editorial judgements based on official docs, public job posts, interview reviews and developer surveys. They are not statistics about how often a question is asked, and no employer’s exact questions are claimed.', bn: 'অগ্রাধিকার ও মার্কেট লেবেলগুলো অফিসিয়াল docs, পাবলিক job post, ইন্টারভিউ রিভিউ ও developer survey দেখে করা সম্পাদকীয় বিচার। কোন প্রশ্ন কত বার জিজ্ঞেস করা হয় তার পরিসংখ্যান নয়, আর কোনো নির্দিষ্ট কোম্পানির হুবহু প্রশ্ন বলে দাবি করা হয়নি।' },
    srcVersions: { en: 'Version & release sources', bn: 'ভার্সন ও release সূত্র' },
    srcMarket: { en: 'Market research', bn: 'মার্কেট গবেষণা' },
    srcDocs: { en: 'Official documentation', bn: 'অফিসিয়াল ডকুমেন্টেশন' },

    // Generic
    close: { en: 'Close', bn: 'বন্ধ করো' },
    dataTable: { en: 'Data table (scrollable)', bn: 'ডেটা টেবিল (স্ক্রল করা যায়)' },
    cancel: { en: 'Cancel', bn: 'বাতিল' },
    confirm: { en: 'Confirm', bn: 'নিশ্চিত করো' },
    progress: { en: 'Progress', bn: 'অগ্রগতি' },
    notFound: { en: 'Page not found', bn: 'পেজ পাওয়া যায়নি' },
    notFoundText: { en: 'That page or question doesn’t exist.', bn: 'এই পেজ বা প্রশ্নটি নেই।' },
    errorTitle: { en: 'Something went wrong', bn: 'কিছু একটা সমস্যা হয়েছে' },
    errorText: { en: 'This view failed to render. Your progress is safe — try going back to the dashboard.', bn: 'এই পেজটি দেখানো যায়নি। তোমার অগ্রগতি নিরাপদ — ড্যাশবোর্ডে ফিরে চেষ্টা করো।' },
  };

  /* ======================================================================
     UI state (in-memory, not persisted)
     ====================================================================== */
  const ui = {
    nonce: 0,
    explorer: { q: '', tech: '', diff: '', type: '', market: '', bookmarked: false, incorrect: false, unanswered: false, learned: false, review: false, sort: 'default', page: 1 },
    navList: null,
    navLabel: '',
    revealed: new Set(),
    hidden: new Set(),
    mcq: {},
    techs: { q: '', sort: 'default', group: 'all' },
    incorrectTab: 'incorrect',
    timers: [],
    keyHandler: null,
  };
  function stopTimers() { ui.timers.forEach((id) => clearInterval(id)); ui.timers = []; ui.keyHandler = null; }

  /* ======================================================================
     Layout: sidebar, topbar, theme, language
     ====================================================================== */
  const NAV = [
    { group: 'navLearn', items: [['dashboard', 'dashboard', 'nav_dashboard'], ['technologies', 'layers', 'nav_technologies'], ['questions', 'list', 'nav_questions'], ['flashcards', 'cards', 'nav_flashcards'], ['daily', 'zap', 'nav_daily']] },
    { group: 'navPractice', items: [['practice', 'play', 'nav_practice'], ['interview', 'mic', 'nav_interview']] },
    { group: 'navProgress', items: [['bookmarks', 'bookmark', 'nav_bookmarks'], ['incorrect', 'xcircle', 'nav_incorrect'], ['review', 'rotate', 'nav_review'], ['history', 'clock', 'nav_history'], ['planner', 'calendar', 'nav_planner']] },
    { group: 'navMore', items: [['sources', 'book', 'nav_sources'], ['settings', 'settings', 'nav_settings']] },
  ];
  function activeNav(route) {
    if (route.name === 'q') return 'questions';
    if (route.name === 'session') return state.activeSession && state.activeSession.kind === 'interview' ? 'interview' : state.activeSession && state.activeSession.kind === 'daily' ? 'daily' : 'practice';
    if (route.name === 'results') return 'history';
    return route.name;
  }
  function navBadge(key) {
    if (key === 'bookmarks') return state.bookmarks.filter((id) => QMAP.has(id)).length;
    if (key === 'incorrect') return QUESTIONS.filter((q) => statusOf(q.id) === 'incorrect').length;
    if (key === 'review') return new Set(dueIds().concat(state.reviewQuestions.filter((id) => QMAP.has(id)))).size;
    return 0;
  }
  function renderNav(route) {
    const nav = $('#nav');
    clear(nav);
    const cur = activeNav(route);
    const L = lang();
    for (const g of NAV) {
      nav.append(h('div', { class: 'nav-group-label' }, t(g.group)));
      for (const [key, ic, label] of g.items) {
        const n = navBadge(key);
        nav.append(h('a', { class: 'nav-link', href: '#/' + key, 'aria-current': cur === key ? 'page' : null, title: tLang(label, 'en') },
          icon(ic, 18),
          h('span', { class: 'nav-label' },
            h('span', { lang: L === 'bn' ? 'bn' : 'en', class: L === 'bn' ? 'bn' : null }, t(label)),
            L === 'both' ? h('small', { lang: 'bn' }, tLang(label, 'bn')) : null),
          n ? h('span', { class: 'nav-badge', 'aria-label': n + ' ' + t('items') }, n) : null));
      }
    }
    const techWrap = $('#sidebarTechs');
    clear(techWrap);
    techWrap.append(h('div', { class: 'nav-group-label' }, t('navTechs')));
    const curTech = route.name === 'questions' ? ui.explorer.tech : (route.name === 'q' && QMAP.get(route.params[0]) ? QMAP.get(route.params[0]).technology : '');
    for (const tc of TECHS) {
      const list = BY_TECH.get(tc.id);
      const st = statsFor(list);
      techWrap.append(h('a', { class: 'tech-link', href: '#/questions?tech=' + tc.id, 'aria-current': curTech === tc.id ? 'page' : null, title: tc.name + ' — ' + list.length + ' ' + t('questionsWord') },
        techLogo(tc, 'sm'),
        h('span', { class: 'tech-name' }, tc.name),
        h('span', { class: 'mini-progress', 'aria-hidden': 'true' }, h('i', { style: { width: Math.round(st.completion * 100) + '%' } }))));
    }
    const foot = $('#sidebarFoot');
    clear(foot);
    foot.append(h('div', null, t('localOnlyShort')), h('div', null, 'v' + APP_VERSION + ' · ' + t('verifiedOn', { date: VERIFIED_AT })));
  }

  function renderTopbar(title) {
    const tt = $('#pageTitle');
    clear(tt);
    if (title) append(tt, title);
    const act = $('#topbarActions');
    clear(act);
    act.append(
      h('a', { class: 'icon-btn hide-sm', href: '#/questions', 'aria-label': t('searchQuestions'), title: t('searchQuestions') + ' (/)' }, icon('search', 18)),
      seg([
        { value: 'en', label: 'EN', lang: 'en' },
        { value: 'bn', label: 'বাংলা', lang: 'bn' },
        { value: 'both', label: lang() === 'bn' ? 'দুটোই' : 'Both' },
      ], lang(), setLang, t('language')),
      h('button', { class: 'icon-btn', type: 'button', 'aria-label': state.preferences.theme === 'dark' ? t('lightTheme') : t('darkTheme'), title: state.preferences.theme === 'dark' ? t('lightTheme') : t('darkTheme'), onclick: () => setTheme(state.preferences.theme === 'dark' ? 'light' : 'dark') },
        icon(state.preferences.theme === 'dark' ? 'sun' : 'moon', 18)));
  }

  function applyPreferences() {
    const p = state.preferences;
    const root = document.documentElement;
    root.setAttribute('data-theme', p.theme);
    root.setAttribute('lang', p.lang === 'bn' ? 'bn' : 'en');
    if (p.motion === 'system') root.removeAttribute('data-motion'); else root.setAttribute('data-motion', p.motion);
    root.style.setProperty('--fs', (15 * p.fontScale) + 'px');
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', p.theme === 'dark' ? '#0B1020' : '#F5F6FB');
    $('#app').classList.toggle('is-collapsed', p.sidebarCollapsed && window.innerWidth > 860);
    const cb = $('#collapseBtn');
    if (cb) { cb.setAttribute('aria-expanded', String(!p.sidebarCollapsed)); cb.setAttribute('aria-label', p.sidebarCollapsed ? t('expandSidebar') : t('collapseSidebar')); }
    const skip = $('.skip-link');
    if (skip) skip.textContent = t('skipToContent');
  }
  function setLang(l) {
    if (!['en', 'bn', 'both'].includes(l) || l === state.preferences.lang) return;
    state.preferences.lang = l;
    saveState();
    applyPreferences();
    rerender();
  }
  function setTheme(th) {
    state.preferences.theme = th;
    saveState();
    applyPreferences();
    renderTopbar($('#pageTitle').textContent);
  }
  function prefersReducedMotion() {
    if (state.preferences.motion === 'reduce') return true;
    if (state.preferences.motion === 'full') return false;
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /* ======================================================================
     Router
     ====================================================================== */
  function parseRoute() {
    const raw = location.hash.replace(/^#\/?/, '');
    const qi = raw.indexOf('?');
    const path = qi >= 0 ? raw.slice(0, qi) : raw;
    const qs = qi >= 0 ? raw.slice(qi + 1) : '';
    const parts = path.split('/').filter(Boolean).map((p) => { try { return decodeURIComponent(p); } catch (e) { return p; } });
    return { name: parts[0] || 'dashboard', params: parts.slice(1), query: new URLSearchParams(qs) };
  }
  function go(hash) {
    if (location.hash === hash) render({ focus: true });
    else location.hash = hash;
  }
  let currentRoute = null;
  function render(opts) {
    const o = opts || {};
    const route = parseRoute();
    currentRoute = route;
    if (o.focus) ui.nonce++;
    stopTimers();
    const VIEWS = {
      dashboard: viewDashboard, technologies: viewTechnologies, questions: viewQuestions, q: viewQuestion,
      practice: viewPractice, session: viewSession, results: viewResults, interview: viewInterview,
      bookmarks: viewBookmarks, incorrect: viewIncorrect, review: viewReview, history: viewHistory,
      planner: viewPlanner, settings: viewSettings, flashcards: viewFlashcards, daily: viewDaily, sources: viewSources,
    };
    const view = VIEWS[route.name] || viewNotFound;
    let out;
    try { out = view(route); } catch (err) {
      console.error(err);
      out = { title: t('errorTitle'), node: emptyState('alert', 'errorTitle', 'errorText', [linkBtn('#/dashboard', t('nav_dashboard'), 'btn--primary')]) };
    }
    if (!out) return; // view redirected
    const main = $('#main');
    clear(main);
    main.className = 'view' + (out.narrow ? ' view--narrow' : '');
    main.append(out.node);
    document.title = (out.titleText || tLang('nav_' + route.name, 'en') || 'Interview Prep BD').toString().replace(/^nav_.*/, 'Interview Prep BD').replace(/[`*]/g, '') + ' · Interview Prep BD';
    renderNav(route);
    renderTopbar(out.title || null);
    if (o.focus) {
      window.scrollTo(0, 0);
      main.focus({ preventScroll: true });
    }
    if (out.after) out.after();
  }
  function rerender() {
    const y = window.scrollY;
    render();
    window.scrollTo(0, y);
  }
  function viewNotFound() {
    return { title: t('notFound'), node: emptyState('alert', 'notFound', 'notFoundText', [linkBtn('#/dashboard', t('nav_dashboard'), 'btn--primary')]) };
  }

  function pageHead(titleKey, leadKey, actions, meta) {
    return h('div', { class: 'page-head' },
      h('div', null,
        h('h1', null, tb(titleKey)),
        leadKey ? h('p', { class: 'lead' }, tb(leadKey)) : null,
        meta ? h('p', { class: 'meta-line mt-1' }, meta) : null),
      actions ? h('div', { class: 'btn-row' }, actions) : null);
  }

  /* ======================================================================
     Dashboard
     ====================================================================== */
  function continueTarget() {
    if (state.activeSession) return { href: '#/session', label: t('resumeSession') };
    let tech = null, latest = 0;
    for (const id of Object.keys(state.questionProgress)) {
      const q = QMAP.get(id);
      if (!q) continue;
      const at = lastAt(id);
      if (at > latest) { latest = at; tech = q.technology; }
    }
    const pool = tech ? BY_TECH.get(tech) : BY_TECH.get('javascript');
    const prioRank = { high: 0, medium: 1, low: 2 };
    const next = (pool || QUESTIONS).filter((q) => !isAnswered(q.id) && !isLearned(q.id))
      .sort((a, b) => (DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty)) || (prioRank[a.priority] - prioRank[b.priority]) || a._order - b._order)[0]
      || QUESTIONS.find((q) => !isAnswered(q.id) && !isLearned(q.id)) || QUESTIONS[0];
    if (!next) return { href: '#/questions', label: t('continueLearning') };
    ui.navList = (pool || QUESTIONS).map((q) => q.id);
    return { href: '#/q/' + encodeURIComponent(next.id), label: t('continueLearning') };
  }

  function viewDashboard() {
    const all = statsFor(QUESTIONS);
    const streak = streakInfo();
    const isNew = all.attempted === 0 && !state.sessions.length && !state.bookmarks.length && !state.learnedQuestions.length;
    const cont = continueTarget();
    const due = dueIds();
    const needsReview = new Set(due.concat(state.reviewQuestions.filter((id) => QMAP.has(id)))).size;
    const today = streak.today;
    const target = state.planner.dailyTarget;

    const hero = h('section', { class: 'hero' },
      h('h1', null, tb(isNew ? 'welcomeNew' : 'welcomeBack')),
      h('p', null, tb('welcomeText', { n: QUESTIONS.length, t: TECHS.length })),
      h('div', { class: 'btn-row mt-2' },
        linkBtn(cont.href, cont.label, 'btn--primary', state.activeSession ? 'play' : 'book'),
        linkBtn('#/practice', t('startPractice'), 'btn--secondary', 'target'),
        linkBtn('#/daily', t('nav_daily'), 'btn--ghost', 'zap')));

    if (!QUESTIONS.length) {
      return { title: tb('nav_dashboard', null, { inline: true }), node: frag(hero, h('div', { class: 'mt-3' }, emptyState('database', 'bankEmpty', 'bankEmptyText'))) };
    }

    const gettingStarted = isNew ? h('section', { class: 'card card--pad-lg mt-3' },
      h('div', { class: 'card__head' }, h('h2', null, tb('gettingStarted'))),
      h('ol', { class: 'steps' }, ['gs1', 'gs2', 'gs3', 'gs4'].map((k) => h('li', null, h('div', null, tb(k))))),
      h('p', { class: 'small muted mt-2 mb-0' }, tb('localOnlyLong'))) : null;

    const stats = h('section', { class: 'grid grid--stats mt-3', 'aria-label': t('yourStats') },
      stat(t('statTotal'), String(QUESTIONS.length), { hint: TECHS.length + ' ' + t('technologiesWord') }),
      stat(t('statAnswered'), String(all.answered), { hint: t('ofTotal', { n: QUESTIONS.length }) }),
      stat(t('res_correct'), String(all.correct), { tone: 'ok' }),
      stat(t('res_partial'), String(all.partial), { tone: 'partial' }),
      stat(t('res_incorrect'), String(all.incorrect), { tone: 'bad' }),
      stat(t('accuracy'), pct(all.accuracy), { hint: t('accuracyHint') }),
      stat(t('weightedScore'), pct(all.weighted), { hint: t('weightedHint') }),
      stat(t('completion'), pct(all.completion), { hint: all.completed + ' / ' + all.total }),
      stat(t('nav_bookmarks'), String(all.bookmarked), null),
      stat(t('needsReview'), String(needsReview), { hint: t('dueToday', { n: due.length }) }),
      stat(t('studyStreak'), t('daysN', { n: streak.current }), { hint: t('bestStreak', { n: streak.best }) }));

    // Today's goal + recent sessions
    const goal = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('todaysGoal')), linkBtn('#/planner', t('nav_planner'), 'btn--ghost btn--sm', 'calendar')),
      h('div', { class: 'row row--between mb-1' }, h('strong', { style: { fontSize: '1.4rem' } }, today + ' / ' + target), h('span', { class: 'muted small' }, t('activitiesToday'))),
      progressBar(today / target, { lg: true, label: t('todaysGoal') }),
      h('p', { class: 'small muted mt-1 mb-0' }, today >= target ? tb('goalDone') : tb('goalLeft', { n: target - today })));

    const recent = state.sessions.slice(-5).reverse();
    const recentCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('recentSessions')), linkBtn('#/history', t('viewAll'), 'btn--ghost btn--sm')),
      recent.length ? h('ul', { class: 'list-plain' }, recent.map((s) => {
        const sm = s.summary || summarizeSession(s);
        return h('li', null,
          h('a', { href: '#/results/' + encodeURIComponent(s.id), class: 'row row--between', style: { width: '100%', color: 'inherit' } },
            h('span', null, h('strong', null, t('kind_' + s.kind)), h('span', { class: 'muted small' }, ' · ' + fmtDate(s.endedAt, true))),
            h('span', { class: 'row' }, h('span', { class: 'badge badge--primary' }, pct(sm.weighted)), h('span', { class: 'small muted' }, sm.total + ' ' + t('qShort')))));
      })) : h('p', { class: 'muted small mb-0' }, tb('noSessionsYet')));

    // Technology progress
    const techBars = h('div', { class: 'bars' }, TECHS.map((tc) => {
      const st = statsFor(BY_TECH.get(tc.id));
      return h('div', { class: 'bar-row' },
        h('a', { class: 'bar-row__label', href: '#/questions?tech=' + tc.id }, techLogo(tc, 'sm'), tc.name),
        progressBar(st.completion, { thin: true, label: tc.name + ' ' + t('completion') }),
        h('span', { class: 'bar-row__value' }, st.completed + '/' + st.total));
    }));
    const techCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('techProgress')), h('span', { class: 'card__sub' }, t('completionLegend'))),
      techBars);

    // Difficulty distribution
    const bankDiff = countBy(QUESTIONS, 'difficulty');
    const diffCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('difficultyDist'))),
      h('div', { class: 'stacked-bar', role: 'img', 'aria-label': DIFFS.map((d) => t('diff_' + d) + ' ' + (bankDiff[d] || 0)).join(', ') },
        DIFFS.map((d) => h('span', { style: { width: ((bankDiff[d] || 0) / QUESTIONS.length * 100) + '%', background: 'var(--' + d + ')' }, title: t('diff_' + d) + ': ' + (bankDiff[d] || 0) }))),
      h('div', { class: 'legend' }, DIFFS.map((d) => h('span', null, h('i', { style: { background: 'var(--' + d + ')' } }), t('diff_' + d) + ' · ' + (bankDiff[d] || 0)))),
      h('div', { class: 'table-wrap mt-2', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
        h('caption', { class: 'sr-only' }, t('difficultyDist')),
        h('thead', null, h('tr', null, h('th', null, t('difficulty')), h('th', { class: 'num' }, t('questionsWord')), h('th', { class: 'num' }, t('statAnswered')), h('th', { class: 'num' }, t('accuracy')), h('th', { class: 'num' }, t('pointsEach')))),
        h('tbody', null, DIFFS.map((d) => {
          const bd = all.byDiff[d];
          return h('tr', null, h('td', null, diffBadge(d)), h('td', { class: 'num' }, bd.total), h('td', { class: 'num' }, bd.answered), h('td', { class: 'num' }, pct(bd.answered ? bd.correct / bd.answered : null)), h('td', { class: 'num' }, POINTS[d]));
        })))),
      h('p', { class: 'small muted mt-1 mb-0' }, tb('extremeNote')));

    const weak = weakAreas(5);
    const weakCard = weak.length ? h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('weakTopics')), linkBtn('#/planner', t('seePlan'), 'btn--ghost btn--sm')),
      weakList(weak)) : null;

    const daily = dailyInfo();
    const dailyCard = h('section', { class: 'card' },
      h('div', { class: 'card__head' }, h('h2', null, tb('nav_daily')), h('span', { class: 'badge badge--teal' }, localDateKey())),
      h('p', { class: 'muted small' }, tb(daily.done ? 'dailyDoneShort' : 'dailyIntroShort', { score: pct(daily.score) })),
      h('div', { class: 'btn-row' }, linkBtn('#/daily', daily.done ? t('viewChallenge') : t('startChallenge'), daily.done ? 'btn--ghost' : 'btn--secondary', 'zap')));

    const node = frag(
      hero,
      storageBanner(),
      gettingStarted,
      stats,
      h('div', { class: 'grid grid--3 mt-3' }, goal, dailyCard, recentCard),
      h('div', { class: 'grid grid--2 dash-split mt-3' }, techCard, h('div', { class: 'stack' }, diffCard, weakCard)));
    return { title: tb('nav_dashboard', null, { inline: true }), titleText: 'Dashboard', node };
  }
  function storageBanner() {
    if (!storageNotice && storageOK) return null;
    const key = storageNotice === 'corrupt' ? 'storageCorrupt' : storageNotice === 'incompatible' ? 'storageIncompatible' : 'storageUnavailable';
    return h('div', { class: 'callout callout--warn mt-2', role: 'alert' }, h('div', { class: 'callout__title' }, icon('alert', 16), tb('storageNoticeTitle')), h('div', { class: 'small' }, tb(key)));
  }
  function weakList(weak) {
    return h('ul', { class: 'list-plain' }, weak.map((g) => {
      const tc = TECH_MAP.get(g.tech);
      return h('li', { class: 'row row--between', style: { width: '100%' } },
        h('span', { class: 'row', style: { minWidth: 0 } }, techLogo(tc, 'sm'), h('span', null, h('strong', null, g.subtopic), h('span', { class: 'muted small' }, ' · ' + tc.name))),
        h('span', { class: 'row' },
          h('span', { class: 'badge badge--bad', title: t('missRate') }, t('missRateShort', { n: Math.round(g.missRate * 100) })),
          btn(t('practice'), () => startQuickSession(Array.from(g.ids), 'practice', { label: g.subtopic }), 'btn--sm btn--secondary', 'play')));
    }));
  }

  /* ======================================================================
     Technology explorer
     ====================================================================== */
  function viewTechnologies() {
    const f = ui.techs;
    const grid = h('div', { class: 'grid grid--auto' });
    const countEl = h('p', { class: 'results-count', 'aria-live': 'polite' });
    function update() {
      clear(grid);
      const terms = searchTerms(f.q);
      let list = TECHS.map((tc) => ({ tc, list: BY_TECH.get(tc.id), st: statsFor(BY_TECH.get(tc.id)) }));
      if (terms.length) list = list.filter((x) => terms.every((term) => normalizeText(x.tc.name + ' ' + x.tc.desc.en + ' ' + x.tc.desc.bn + ' ' + x.tc.group).includes(term)));
      if (f.group !== 'all') list = list.filter((x) => x.tc.group === f.group);
      if (f.sort === 'name') list.sort((a, b) => a.tc.name.localeCompare(b.tc.name));
      else if (f.sort === 'count') list.sort((a, b) => b.list.length - a.list.length);
      else if (f.sort === 'progressDesc') list.sort((a, b) => b.st.completion - a.st.completion);
      else if (f.sort === 'progressAsc') list.sort((a, b) => a.st.completion - b.st.completion);
      clear(countEl);
      countEl.append(h('strong', null, String(list.length)), ' ', t('technologiesWord'));
      if (!list.length) { grid.append(emptyState('search', 'noTechMatch', 'tryDifferent')); return; }
      for (const { tc, list: qs, st } of list) {
        const dc = countBy(qs, 'difficulty');
        grid.append(h('article', { class: 'card card--interactive tech-card' },
          h('div', { class: 'tech-card__head' }, techLogo(tc),
            h('div', { style: { minWidth: 0 } }, h('h2', { class: 'tech-card__title' }, tc.name), h('div', { class: 'tech-card__ver' }, tc.version))),
          h('p', { class: 'tech-card__desc' + (lang() === 'bn' ? ' bn' : ''), lang: lang() === 'bn' ? 'bn' : 'en' }, lang() === 'bn' ? tc.desc.bn : tc.desc.en),
          lang() === 'both' ? h('p', { class: 'tech-card__desc bn small muted', lang: 'bn', style: { minHeight: 0 } }, tc.desc.bn) : null,
          h('div', { class: 'row row--between small' }, h('span', null, h('strong', null, qs.length), ' ', t('questionsWord')), h('span', { class: 'muted' }, pct(st.completion) + ' ' + t('completeWord'))),
          h('div', { class: 'diff-counts' }, DIFFS.map((d) => h('div', { class: 'diff-count diff-count--' + d }, h('b', null, dc[d] || 0), h('span', null, t('diff_' + d))))),
          progressBar(st.completion, { thin: true, label: tc.name + ' ' + t('completion') }),
          h('div', { class: 'btn-row' },
            linkBtn('#/questions?tech=' + tc.id, t('startLearning'), 'btn--secondary btn--sm', 'book'),
            btn(t('practice'), () => { practiceDefaults().techs = [tc.id]; go('#/practice'); }, 'btn--ghost btn--sm', 'play'))));
      }
    }
    const search = h('input', { class: 'input', type: 'search', placeholder: t('searchTechs'), value: f.q, 'aria-label': t('searchTechs'), oninput: debounce((e) => { f.q = e.target.value; update(); }, 120) });
    const sortSel = h('select', { class: 'select', 'aria-label': t('sortBy'), onchange: (e) => { f.sort = e.target.value; update(); } },
      [['default', 'sortDefault'], ['name', 'sortName'], ['count', 'sortCount'], ['progressDesc', 'sortProgressDesc'], ['progressAsc', 'sortProgressAsc']].map(([v, k]) => h('option', { value: v, selected: f.sort === v }, t(k))));
    const groups = seg(['all'].concat(TECH_GROUPS).map((g) => ({ value: g, label: t('group_' + g) })), f.group, (g) => { f.group = g; rerender(); }, t('filterGroup'));
    update();
    const node = frag(
      pageHead('nav_technologies', 'techLead'),
      h('div', { class: 'card card--flat' },
        h('div', { class: 'filters filters--2' },
          h('div', { class: 'field field--search' }, h('label', null, t('search')), h('div', { class: 'search-box' }, icon('search', 16), search)),
          h('div', { class: 'field' }, h('label', null, t('sortBy')), sortSel)),
        h('div', { class: 'filters__more' }, h('span', { class: 'field-label' }, t('filterGroup')), groups)),
      h('div', { class: 'results-bar' }, countEl),
      grid);
    return { title: tb('nav_technologies', null, { inline: true }), titleText: 'Technologies', node };
  }

  /* ======================================================================
     Question explorer
     ====================================================================== */
  function filterQuestions(f) {
    let list = QUESTIONS;
    if (f.tech) list = list.filter((q) => q.technology === f.tech);
    if (f.diff) list = list.filter((q) => q.difficulty === f.diff);
    if (f.type) list = list.filter((q) => q.type === f.type);
    if (f.market) list = list.filter((q) => q.market === f.market);
    if (f.bookmarked) list = list.filter((q) => isBookmarked(q.id));
    if (f.incorrect) list = list.filter((q) => statusOf(q.id) === 'incorrect');
    if (f.unanswered) list = list.filter((q) => !isAnswered(q.id));
    if (f.learned) list = list.filter((q) => isLearned(q.id));
    if (f.review) { const due = new Set(dueIds()); list = list.filter((q) => isFlagged(q.id) || due.has(q.id)); }
    const terms = searchTerms(f.q);
    let scored = null;
    if (terms.length) {
      scored = new Map();
      list = list.filter((q) => { const s = searchScore(q, terms); if (s) scored.set(q.id, s); return s > 0; });
    }
    const prioRank = { high: 0, medium: 1, low: 2 };
    list = list.slice();
    if (f.sort === 'diffAsc') list.sort((a, b) => DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty) || a._order - b._order);
    else if (f.sort === 'diffDesc') list.sort((a, b) => DIFFS.indexOf(b.difficulty) - DIFFS.indexOf(a.difficulty) || a._order - b._order);
    else if (f.sort === 'priority') list.sort((a, b) => prioRank[a.priority] - prioRank[b.priority] || a._order - b._order);
    else if (f.sort === 'recent') list.sort((a, b) => (lastAt(b.id) - lastAt(a.id)) || a._order - b._order);
    else if (scored) list.sort((a, b) => scored.get(b.id) - scored.get(a.id) || a._order - b._order);
    return list;
  }
  function syncExplorerHash() {
    const f = ui.explorer;
    const qs = f.tech ? '?tech=' + encodeURIComponent(f.tech) : '';
    const target = '#/questions' + qs;
    if (location.hash !== target) history.replaceState(null, '', target);
  }
  function questionItem(q, opts) {
    const st = statusOf(q.id);
    const o = opts || {};
    const dotCls = st ? 'status-dot--' + st : (isLearned(q.id) ? 'status-dot--learned' : '');
    const dotLabel = st ? t('res_' + st) : (isLearned(q.id) ? t('learned') : t('res_none'));
    return h('a', { class: 'q-item', href: '#/q/' + encodeURIComponent(q.id), onclick: () => { if (o.navList) { ui.navList = o.navList; ui.navLabel = o.navLabel || ''; } } },
      h('span', { class: 'status-dot ' + dotCls, role: 'img', 'aria-label': dotLabel, title: dotLabel }),
      h('div', { style: { minWidth: 0 } },
        h('div', { class: 'q-item__title' }, biTitle(q.question)),
        h('div', { class: 'q-item__meta' },
          techBadge(q.technology), diffBadge(q.difficulty), typeBadge(q.type),
          h('span', { class: 'badge' }, q.subtopic),
          q.market !== 'both' ? marketBadge(q.market) : null,
          q.status !== 'stable' ? featureStatusBadge(q.status) : null,
          o.extra || null)),
      h('div', { class: 'q-item__side' },
        isBookmarked(q.id) ? h('span', { class: 'badge badge--primary', title: t('bookmarked') }, icon('bookmark', 12), h('span', { class: 'sr-only' }, t('bookmarked'))) : null,
        isFlagged(q.id) ? h('span', { class: 'badge badge--warn', title: t('flagged') }, icon('flag', 12), h('span', { class: 'sr-only' }, t('flagged'))) : null,
        h('span', { class: 'small muted nowrap' }, icon('clock', 12), ' ', t('minN', { n: q.estimatedMinutes }))));
  }
  function questionList(list, navLabel, limit) {
    const ids = list.map((q) => q.id);
    const items = (limit ? list.slice(0, limit) : list).map((q) => questionItem(q, { navList: ids, navLabel }));
    return h('div', { class: 'q-list' }, items);
  }

  function viewQuestions(route) {
    const f = ui.explorer;
    const qTech = route.query.get('tech');
    if (qTech !== null && TECH_MAP.has(qTech) && qTech !== f.tech) { f.tech = qTech; f.page = 1; }
    if (qTech === null && route.query.toString() === '' && ui.lastExplorerHash && ui.lastExplorerHash !== location.hash) { /* keep state */ }

    const results = h('div');
    const countEl = h('p', { class: 'results-count', 'aria-live': 'polite' });
    const pagerTop = h('div', { class: 'row' });

    function update(resetPage) {
      if (resetPage) f.page = 1;
      const list = filterQuestions(f);
      ui.navList = list.map((q) => q.id);
      ui.navLabel = t('nav_questions');
      const pages = Math.max(1, Math.ceil(list.length / PAGE_SIZE));
      f.page = clamp(f.page, 1, pages);
      clear(countEl);
      countEl.append(h('strong', null, String(list.length)), ' ', t('matchingQuestions'), list.length ? h('span', { class: 'muted small' }, ' · ' + t('showingRange', { a: (f.page - 1) * PAGE_SIZE + 1, b: Math.min(list.length, f.page * PAGE_SIZE) })) : null);
      clear(results);
      if (!list.length) {
        results.append(emptyState('search', QUESTIONS.length ? 'noMatchTitle' : 'bankEmpty', QUESTIONS.length ? 'noMatchText' : 'bankEmptyText', QUESTIONS.length ? [btn(t('clearFilters'), clearAll, 'btn--primary', 'x')] : null));
        return;
      }
      const slice = list.slice((f.page - 1) * PAGE_SIZE, f.page * PAGE_SIZE);
      results.append(h('div', { class: 'q-list' }, slice.map((q) => questionItem(q, { navList: ui.navList, navLabel: ui.navLabel }))));
      if (pages > 1) {
        results.append(h('nav', { class: 'pager', 'aria-label': t('pagination') },
          btn(t('prev'), () => { f.page--; update(); scrollTo({ top: 0 }); }, 'btn--sm', 'chevL', { disabled: f.page <= 1 }),
          h('span', { class: 'small muted' }, t('pageXofY', { x: f.page, y: pages })),
          btn(t('next'), () => { f.page++; update(); scrollTo({ top: 0 }); }, 'btn--sm', 'chevR', { disabled: f.page >= pages })));
      }
      syncExplorerHash();
      renderNav(parseRoute());
    }
    function clearAll() {
      Object.assign(f, { q: '', tech: '', diff: '', type: '', market: '', bookmarked: false, incorrect: false, unanswered: false, learned: false, review: false, sort: 'default', page: 1 });
      history.replaceState(null, '', '#/questions');
      rerender();
    }
    const sel = (key, labelKey, options) => {
      const s = h('select', { class: 'select', id: 'f-' + key, onchange: (e) => { f[key] = e.target.value; update(true); } },
        options.map(([v, lbl]) => h('option', { value: v, selected: f[key] === v }, lbl)));
      return h('div', { class: 'field' }, h('label', { for: 'f-' + key }, t(labelKey)), s);
    };
    const search = h('input', { class: 'input', id: 'f-q', type: 'search', placeholder: t('searchPlaceholder'), value: f.q, autocomplete: 'off', oninput: debounce((e) => { f.q = e.target.value; update(true); }, 140) });
    const flag = (key, labelKey) => h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: f[key], onchange: (e) => { f[key] = e.target.checked; update(true); } }), t(labelKey));
    const counts = countBy(QUESTIONS, 'technology');
    const panel = h('section', { class: 'card card--flat', 'aria-label': t('filters') },
      h('div', { class: 'filters' },
        h('div', { class: 'field field--search' }, h('label', { for: 'f-q' }, t('searchLabel')), h('div', { class: 'search-box' }, icon('search', 16), search)),
        sel('tech', 'technology', [['', t('allTechs')]].concat(TECHS.map((tc) => [tc.id, tc.name + ' (' + (counts[tc.id] || 0) + ')']))),
        sel('diff', 'difficulty', [['', t('allLevels')]].concat(DIFFS.map((d) => [d, t('diff_' + d)]))),
        sel('type', 'questionType', [['', t('allTypes')]].concat(TYPES.map((ty) => [ty, t('type_' + ty)]))),
        sel('market', 'market', [['', t('allMarkets')]].concat(MARKETS.map((m) => [m, t('market_' + m)])))),
      h('div', { class: 'filters__more' },
        flag('bookmarked', 'onlyBookmarked'), flag('incorrect', 'onlyIncorrect'), flag('unanswered', 'onlyUnanswered'), flag('learned', 'onlyLearned'), flag('review', 'onlyReview'),
        h('span', { style: { flex: '1' } }),
        h('div', { class: 'row' },
          h('label', { class: 'field-label', for: 'f-sort' }, t('sortBy')),
          h('select', { class: 'select', id: 'f-sort', style: { width: 'auto' }, onchange: (e) => { f.sort = e.target.value; update(true); } },
            [['default', 'sortRelevance'], ['diffAsc', 'sortDiffAsc'], ['diffDesc', 'sortDiffDesc'], ['priority', 'sortPriority'], ['recent', 'sortRecent']].map(([v, k]) => h('option', { value: v, selected: f.sort === v }, t(k))))),
        h('div', { class: 'row' }, h('span', { class: 'field-label' }, t('language')), seg([{ value: 'en', label: 'EN' }, { value: 'bn', label: 'বাংলা', lang: 'bn' }, { value: 'both', label: t('both') }], lang(), setLang, t('language'))),
        btn(t('clearFilters'), clearAll, 'btn--ghost btn--sm', 'x')));
    update();
    const node = frag(
      pageHead('nav_questions', 'questionsLead', [
        btn(t('practiceThese'), () => { const ids = filterQuestions(f).map((q) => q.id); if (!ids.length) { toast(t('nothingToPractice'), 'bad'); return; } startQuickSession(shuffle(ids).slice(0, 20), 'practice', { label: t('nav_questions') }); }, 'btn--secondary', 'play'),
      ]),
      panel,
      h('div', { class: 'results-bar' }, countEl, pagerTop),
      results);
    return { title: tb('nav_questions', null, { inline: true }), titleText: 'All Questions', node, after: () => { if (route.query.get('focus') === 'search') search.focus(); } };
  }

  /* ======================================================================
     Question detail
     ====================================================================== */
  const codeInQuestion = (q) => !!(q.code && q.code.source && (q.type === 'output' || q.type === 'debugging' || q.type === 'mcq'));

  function questionBody(q) {
    const parts = [biText(q.question, { cls: 'q-title', plain: true })];
    if (q.setup && q.setup.source) parts.push(h('div', { class: 'mt-2' }, codeBlock(q.setup, { label: t('schemaAndData') })));
    if (codeInQuestion(q)) parts.push(h('div', { class: 'mt-2' }, codeBlock({ language: q.code.language, source: q.code.source }, { label: q.type === 'debugging' ? t('buggyCode') : null })));
    return h('div', { class: 'stack stack--sm' }, parts);
  }
  function metaBadges(q, withTech) {
    return h('div', { class: 'q-head' },
      withTech ? techBadge(q.technology) : null,
      diffBadge(q.difficulty), typeBadge(q.type),
      h('span', { class: 'badge' }, q.subtopic),
      marketBadge(q.market), priorityBadge(q.priority),
      h('span', { class: 'badge', title: t('estimatedTime') }, icon('clock', 12), t('minN', { n: q.estimatedMinutes })),
      q.versionSensitive ? h('span', { class: 'badge badge--teal', title: t('versionSensitive') }, icon('info', 12), q.technologyVersion) : null,
      q.status !== 'stable' ? featureStatusBadge(q.status) : null);
  }
  function section(iconName, titleKey, content) {
    return h('section', { class: 'stack stack--sm' }, h('h3', { class: 'section-title' }, icon(iconName, 15), tb(titleKey, null, { inline: true })), content);
  }
  function answerPanel(q) {
    const parts = [];
    parts.push(section('checkCircle', 'referenceAnswer', biText(q.answer)));
    if (q.complexity && (q.complexity.time || q.complexity.space)) {
      parts.push(h('div', { class: 'row' },
        q.complexity.time ? h('span', { class: 'badge badge--primary' }, t('timeComplexity') + ': ' + q.complexity.time) : null,
        q.complexity.space ? h('span', { class: 'badge badge--primary' }, t('spaceComplexity') + ': ' + q.complexity.space) : null));
    }
    if (q.code && q.code.source && !codeInQuestion(q)) {
      const label = q.type === 'coding' ? t('referenceSolution') : q.type === 'query' ? t('query') : t('codeExample');
      parts.push(codeBlock({ language: q.code.language, source: q.code.source }, { label }));
    }
    if (q.code && q.code.output) parts.push(codeBlock(q.code, { output: true }));
    q.extraCode.forEach((x) => parts.push(codeBlock(x, { label: pick(x.label) || null })));
    if (q.explanation.en || q.explanation.bn) parts.push(section('bulb', 'explanation', biText(q.explanation)));
    if (q.commonMistakes) parts.push(h('div', { class: 'callout callout--warn' }, h('div', { class: 'callout__title' }, icon('alert', 16), tb('commonMistakes', null, { inline: true })), biText(q.commonMistakes)));
    if (q.interviewTip.en || q.interviewTip.bn) parts.push(h('div', { class: 'callout callout--tip' }, h('div', { class: 'callout__title' }, icon('mic', 16), tb('interviewTip', null, { inline: true })), biText(q.interviewTip)));
    if (q.followUps.length) parts.push(section('message', 'followUps', h('ul', { class: 'list-plain' }, q.followUps.map((fu) => h('li', null, icon('chevR', 14), h('div', { style: { minWidth: 0 } }, biText(fu, { plain: true, noLabels: true })))))));
    if (q.references.length) parts.push(section('link', 'references', h('ul', { class: 'list-plain ref-list' }, q.references.map((r) => h('li', null, h('a', { href: r.url, target: '_blank', rel: 'noopener noreferrer' }, r.title, icon('external', 13)))))));
    return h('div', { class: 'stack answer-panel' }, parts);
  }
  function assessBar(current, onPick, opts) {
    const o = opts || {};
    const defs = [['correct', 'checkCircle', '100%'], ['partial', 'half', '50%'], ['incorrect', 'xcircle', '0%']];
    if (o.skip !== false) defs.push(['skipped', 'skip', t('recorded')]);
    return h('div', { class: 'assess', role: 'group', 'aria-label': t('selfAssess') },
      defs.map(([r, ic, hint], i) => h('button', { type: 'button', class: 'assess-btn assess-btn--' + r, 'aria-pressed': String(current === r), onclick: () => onPick(r), title: t('res_' + r) + (o.keys ? ' (' + (r === 'skipped' ? 'S' : i + 1) + ')' : '') },
        icon(ic, 20), h('span', null, t(r === 'skipped' ? 'skip' : 'res_' + r)), h('small', null, hint))));
  }
  function mcqBlock(q, choice, locked, onSubmit, opts) {
    const o = opts || {};
    let selected = choice;
    const L = lang();
    const keys = ['A', 'B', 'C', 'D', 'E', 'F'];
    const submit = h('button', { type: 'button', class: 'btn btn--primary', disabled: selected == null || locked, onclick: () => { if (selected != null && !locked) onSubmit(selected); } }, icon('check', 16), t('submitAnswer'));
    const opts2 = q.options.map((op, i) => {
      const isCorrect = locked && i === q.correctIndex;
      const isWrong = locked && i === choice && choice !== q.correctIndex;
      const txt = L === 'both'
        ? h('span', null, h('span', { lang: 'en' }, inline(op.en)), h('span', { class: 'bn-line bn', lang: 'bn' }, inline(op.bn)))
        : L === 'bn' ? h('span', { class: 'bn', lang: 'bn' }, inline(op.bn || op.en)) : h('span', { lang: 'en' }, inline(op.en || op.bn));
      const stateLbl = isCorrect ? h('span', { class: 'mcq-option__state', style: { color: 'var(--ok)' } }, t('correctAnswer')) : isWrong ? h('span', { class: 'mcq-option__state', style: { color: 'var(--bad)' } }, t('yourAnswer')) : h('span');
      const b = h('button', { type: 'button', role: 'radio', class: 'mcq-option' + (isCorrect ? ' is-correct' : '') + (isWrong ? ' is-wrong' : ''), 'aria-checked': String(selected === i), disabled: locked, 'data-idx': String(i),
        onclick: () => { if (locked) return; selected = i; opts2.forEach((x, k) => x.setAttribute('aria-checked', String(k === i))); submit.disabled = false; if (o.onSelect) o.onSelect(i); } },
      h('span', { class: 'mcq-option__key', 'aria-hidden': 'true' }, keys[i]), txt, stateLbl);
      return b;
    });
    const group = h('div', { class: 'mcq', role: 'radiogroup', 'aria-label': t('chooseAnswer') }, opts2);
    const wrap = h('div', { class: 'stack' }, group);
    if (!locked) wrap.append(h('div', { class: 'btn-row' }, submit, h('span', { class: 'small muted' }, t('mcqOnce'))));
    else {
      const ok = choice === q.correctIndex;
      wrap.append(h('div', { class: 'callout ' + (ok ? 'callout--tip' : 'callout--warn'), role: 'status' },
        h('div', { class: 'callout__title' }, icon(ok ? 'checkCircle' : 'xcircle', 16), tb(ok ? 'mcqCorrect' : 'mcqWrong', { key: keys[q.correctIndex] }, { inline: true }))));
    }
    wrap._select = (i) => { if (!locked && opts2[i]) opts2[i].click(); };
    wrap._submit = () => submit.click();
    return wrap;
  }
  function versionCard(q) {
    return h('section', { class: 'card' },
      h('h3', { class: 'section-title' }, icon('info', 15), t('versionInfo')),
      h('dl', { class: 'ver-box' },
        h('dt', null, t('version')), h('dd', null, q.technologyVersion),
        h('dt', null, t('featureStatus')), h('dd', null, featureStatusBadge(q.status)),
        h('dt', null, t('versionSensitive')), h('dd', null, q.versionSensitive ? t('yes') : t('no')),
        h('dt', null, t('verified')), h('dd', null, q.verifiedAt || '—'),
        q.documentationUrl ? h('dt', null, t('officialDocs')) : null,
        q.documentationUrl ? h('dd', null, h('a', { href: q.documentationUrl, target: '_blank', rel: 'noopener noreferrer' }, t('openDocs'), ' ', icon('external', 12))) : null));
  }
  function toggleBtn(pressed, ic, onLabel, offLabel, onClick) {
    return h('button', { type: 'button', class: 'btn btn--block ' + (pressed ? 'btn--secondary' : ''), 'aria-pressed': String(pressed), onclick: onClick, style: { justifyContent: 'flex-start' } }, icon(ic, 16), pressed ? onLabel : offLabel);
  }

  function viewQuestion(route) {
    const q = QMAP.get(route.params[0]);
    if (!q) return viewNotFound();
    const tc = TECH_MAP.get(q.technology);
    const mode = state.preferences.mode;
    const navList = ui.navList && ui.navList.includes(q.id) ? ui.navList : BY_TECH.get(q.technology).map((x) => x.id);
    const pos = navList.indexOf(q.id);
    const prevId = pos > 0 ? navList[pos - 1] : null;
    const nextId = pos < navList.length - 1 ? navList[pos + 1] : null;
    const attemptId = 'detail:' + q.id + ':' + ui.nonce;
    const mcqState = ui.mcq[q.id] && ui.mcq[q.id].nonce === ui.nonce ? ui.mcq[q.id] : null;
    const revealed = q.isMCQ ? (!!mcqState || ui.revealed.has(q.id)) : (mode === 'learning' ? !ui.hidden.has(q.id) : ui.revealed.has(q.id));
    const st = statusOf(q.id);
    const p = prog(q.id);

    const modeSeg = seg([{ value: 'learning', label: t('learningMode') }, { value: 'interview', label: t('interviewMode') }], mode, (m) => {
      state.preferences.mode = m; saveState(); ui.revealed.delete(q.id); ui.hidden.delete(q.id); rerender();
    }, t('studyMode'));

    const headCard = h('section', { class: 'card card--pad-lg' },
      h('div', { class: 'row row--between mb-2' },
        h('a', { href: '#/questions?tech=' + q.technology, class: 'row small', style: { gap: '8px' } }, techLogo(tc, 'sm'), tc.name),
        modeSeg),
      metaBadges(q, false),
      questionBody(q));

    let answerArea;
    if (q.isMCQ) {
      const locked = !!mcqState;
      answerArea = h('section', { class: 'card card--pad-lg stack' },
        h('h2', { class: 'section-title' }, icon('list', 15), tb('chooseAnswer', null, { inline: true })),
        mcqBlock(q, mcqState ? mcqState.choice : null, locked, (choice) => {
          ui.mcq[q.id] = { nonce: ui.nonce, choice };
          recordResult(q.id, choice === q.correctIndex ? 'correct' : 'incorrect', attemptId);
          rerender();
        }),
        !locked && !revealed ? h('div', null, btn(t('revealWithoutAnswering'), () => { ui.revealed.add(q.id); rerender(); }, 'btn--ghost btn--sm', 'eye')) : null,
        revealed ? answerPanel(q) : null);
    } else if (!revealed) {
      answerArea = h('section', { class: 'card card--pad-lg' },
        h('div', { class: 'reveal' },
          h('h2', { style: { margin: 0 } }, tb('thinkFirst')),
          h('p', { class: 'muted', style: { margin: 0, maxWidth: '52ch' } }, tb('thinkFirstText', { n: q.estimatedMinutes })),
          btn(t('revealAnswer'), () => { ui.revealed.add(q.id); ui.hidden.delete(q.id); rerender(); }, 'btn--primary btn--lg', 'eye')));
    } else {
      answerArea = frag(
        h('section', { class: 'card card--pad-lg' },
          h('div', { class: 'row row--between mb-2' },
            h('h2', { style: { margin: 0, fontSize: '1.1rem' } }, tb('answerSection', null, { inline: true })),
            mode === 'learning' ? btn(t('hideAnswer'), () => { ui.hidden.add(q.id); ui.revealed.delete(q.id); rerender(); }, 'btn--ghost btn--sm', 'eye') : null),
          answerPanel(q)),
        h('section', { class: 'card' },
          h('h2', { class: 'section-title' }, icon('target', 15), tb('howDidYouDo', null, { inline: true })),
          h('p', { class: 'small muted' }, tb('selfAssessHelp')),
          assessBar(p && p.history.length && p.history[p.history.length - 1].s === attemptId ? p.history[p.history.length - 1].r : null, (r) => {
            recordResult(q.id, r, attemptId);
            toast(tb('savedResult', { r: t('res_' + r) }, { inline: true }), r === 'correct' ? 'ok' : 'info', 1800);
            rerender();
          })));
    }

    const navRow = h('nav', { class: 'row row--between mt-2', 'aria-label': t('questionNav') },
      prevId ? linkBtn('#/q/' + encodeURIComponent(prevId), t('previous'), 'btn--ghost', 'arrowL') : h('span'),
      h('span', { class: 'small muted' }, (ui.navLabel && ui.navList === navList ? ui.navLabel + ' · ' : tc.name + ' · ') + (pos + 1) + ' / ' + navList.length),
      nextId ? h('a', { class: 'btn btn--ghost', href: '#/q/' + encodeURIComponent(nextId) }, t('next'), icon('arrowR', 16)) : h('span'));

    const related = [];
    q.related.forEach((id) => { const r = QMAP.get(id); if (r && r !== q) related.push(r); });
    BY_TECH.get(q.technology).forEach((r) => { if (related.length < 5 && r !== q && r.subtopic === q.subtopic && !related.includes(r)) related.push(r); });

    const aside = h('aside', { class: 'q-detail__aside', 'aria-label': t('questionTools') },
      h('section', { class: 'card stack stack--sm' },
        h('h3', { class: 'section-title' }, icon('bookmark', 15), t('myStatus')),
        toggleBtn(isBookmarked(q.id), 'bookmark', t('bookmarked'), t('bookmark'), () => { const v = toggleIn('bookmarks', q.id); toast(v ? t('addedBookmark') : t('removedBookmark'), 'ok', 1600); rerender(); }),
        toggleBtn(isLearned(q.id), 'grad', t('learned'), t('markLearned'), () => { toggleIn('learnedQuestions', q.id); rerender(); }),
        toggleBtn(isFlagged(q.id), 'flag', t('flagged'), t('flagReview'), () => { toggleIn('reviewQuestions', q.id); rerender(); }),
        h('dl', { class: 'kv mt-1' },
          h('dt', null, t('lastResult')), h('dd', null, resultBadge(st)),
          h('dt', null, t('attempts')), h('dd', null, p ? p.history.filter((e) => e.r !== 'skipped').length : 0),
          h('dt', null, t('nextReview')), h('dd', null, p && p.due ? fmtDate(p.due) : '—'))),
      versionCard(q),
      related.length ? h('section', { class: 'card' },
        h('h3', { class: 'section-title' }, icon('link', 15), t('relatedQuestions')),
        h('ul', { class: 'list-plain' }, related.map((r) => h('li', null, h('a', { href: '#/q/' + encodeURIComponent(r.id), class: 'small' }, pick(r.question)), ' ', diffBadge(r.difficulty))))) : null);

    const node = h('div', null,
      h('div', { class: 'row row--between mb-2' },
        h('a', { href: '#/questions', class: 'row small muted' }, icon('arrowL', 14), t('backToQuestions')),
        h('span', { class: 'tag' }, q.id)),
      h('div', { class: 'q-detail' }, h('div', { class: 'stack' }, headCard, answerArea, navRow), aside));
    return { title: h('span', null, tc.name, h('small', null, t('diff_' + q.difficulty))), titleText: pick(q.question).slice(0, 60), node };
  }

  /* ======================================================================
     Practice configuration & session engine
     ====================================================================== */
  const PRESETS = [
    { id: 'quick', count: 10, icon: 'zap' },
    { id: 'focus', count: 20, icon: 'target' },
    { id: 'deep', count: 30, icon: 'layers' },
    { id: 'custom', count: null, icon: 'settings' },
  ];
  let practiceCfg = null;
  function practiceDefaults() {
    if (!practiceCfg) practiceCfg = { preset: 'quick', count: 10, techs: [], diffs: [], types: [], market: 'all', order: 'random', pool: 'all', timer: 0 };
    return practiceCfg;
  }
  let interviewCfg = null;
  function interviewDefaults() {
    if (!interviewCfg) interviewCfg = { count: 8, techs: [], diffs: ['medium', 'hard'], timer: 30, includeMcq: false, market: 'all' };
    return interviewCfg;
  }

  function matchingPool(cfg) {
    let list = QUESTIONS;
    if (cfg.techs && cfg.techs.length) list = list.filter((q) => cfg.techs.includes(q.technology));
    if (cfg.diffs && cfg.diffs.length) list = list.filter((q) => cfg.diffs.includes(q.difficulty));
    if (cfg.types && cfg.types.length) list = list.filter((q) => cfg.types.includes(q.type));
    if (cfg.includeMcq === false) list = list.filter((q) => !q.isMCQ);
    if (cfg.market === 'bangladesh') list = list.filter((q) => q.market === 'bangladesh' || q.market === 'both');
    else if (cfg.market === 'international') list = list.filter((q) => q.market === 'international' || q.market === 'both');
    if (cfg.pool === 'unanswered') list = list.filter((q) => !isAnswered(q.id));
    else if (cfg.pool === 'answered') list = list.filter((q) => isAnswered(q.id));
    else if (cfg.pool === 'mistakes') list = list.filter((q) => { const s = statusOf(q.id); return s === 'incorrect' || s === 'partial'; });
    return list;
  }
  function orderQuestions(list, order) {
    if (order !== 'priority') return shuffle(list);
    const due = new Set(dueIds());
    const prioRank = { high: 0, medium: 1, low: 2 };
    return list.map((q) => ({ q, k: [due.has(q.id) ? 0 : 1, isAnswered(q.id) ? 1 : 0, prioRank[q.priority], Math.random()] }))
      .sort((a, b) => { for (let i = 0; i < 4; i++) if (a.k[i] !== b.k[i]) return a.k[i] - b.k[i]; return 0; })
      .map((x) => x.q);
  }

  function createSession(kind, ids, config) {
    const now = Date.now();
    const timer = Number(config.timer) || 0;
    const s = {
      id: uid('s'), kind, config: Object.assign({}, config), ids: ids.slice(), index: 0, answers: {},
      startedAt: now, endedAt: null, deadline: timer ? now + timer * 60000 : null,
      dateKey: kind === 'daily' ? localDateKey() : null, summary: null,
    };
    state.activeSession = s;
    saveState();
    return s;
  }
  async function startSession(kind, ids, config) {
    const clean = ids.filter((id) => QMAP.has(id));
    if (!clean.length) { toast(t('nothingToPractice'), 'bad'); return false; }
    if (state.activeSession) {
      const ok = await confirmModal({ title: t('replaceSessionTitle'), message: tb('replaceSessionText'), confirmLabel: t('startNew') });
      if (!ok) return false;
      finishSession(state.activeSession, { silent: true });
    }
    createSession(kind, clean, config || {});
    go('#/session');
    return true;
  }
  function startQuickSession(ids, kind, extra) {
    return startSession(kind || 'practice', ids.slice(0, 60), Object.assign({ mode: 'practice', timer: 0 }, extra || {}));
  }
  function finishSession(s, opts) {
    const o = opts || {};
    s.endedAt = Date.now();
    s.summary = summarizeSession(s);
    state.sessions.push(s);
    if (state.sessions.length > 200) state.sessions = state.sessions.slice(-200);
    if (state.activeSession && state.activeSession.id === s.id) state.activeSession = null;
    if (s.kind === 'daily') state.daily[s.dateKey || localDateKey()] = { sessionId: s.id, score: s.summary.weighted };
    saveState();
    if (!o.silent) {
      if (o.timeUp) toast(tb('timeUp', null, { inline: true }), 'info', 4000);
      go('#/results/' + encodeURIComponent(s.id));
    }
  }

  function viewPractice() {
    const cfg = practiceDefaults();
    const countEl = h('span', { class: 'results-count', 'aria-live': 'polite' });
    const warnEl = h('div');
    function refresh() {
      const n = matchingPool(cfg).length;
      clear(countEl);
      countEl.append(h('strong', null, String(n)), ' ', t('matchingQuestions'));
      clear(warnEl);
      if (n === 0) warnEl.append(h('div', { class: 'callout callout--warn mt-1', role: 'alert' }, tb('noneMatchConfig')));
      else if (n < cfg.count) warnEl.append(h('div', { class: 'callout callout--info mt-1' }, tb('fewerThanRequested', { n, c: cfg.count })));
    }
    const multi = (key, values, labelFn, extraCount) => h('div', { class: 'chip-group', role: 'group' },
      chip(t('all'), !cfg[key].length, () => { cfg[key] = []; rerender(); }),
      values.map((v) => chip(h('span', null, labelFn(v), extraCount ? h('span', { class: 'count' }, ' ' + extraCount(v)) : null), cfg[key].includes(v), () => {
        cfg[key] = cfg[key].includes(v) ? cfg[key].filter((x) => x !== v) : cfg[key].concat(v);
        rerender();
      })));
    const techCounts = countBy(QUESTIONS, 'technology');
    const resume = state.activeSession ? h('div', { class: 'callout callout--info mb-2' },
      h('div', { class: 'callout__title' }, icon('play', 16), tb('unfinishedSession')),
      h('p', { class: 'small mb-1' }, tb('unfinishedText', { n: Object.values(state.activeSession.answers).filter((a) => a.result).length, total: state.activeSession.ids.length })),
      h('div', { class: 'btn-row' },
        linkBtn('#/session', t('resumeSession'), 'btn--primary btn--sm', 'play'),
        btn(t('finishNow'), () => finishSession(state.activeSession), 'btn--ghost btn--sm', 'stop'))) : null;

    const presets = h('div', { class: 'grid grid--4' }, PRESETS.map((p) => {
      const active = cfg.preset === p.id;
      return h('button', { type: 'button', class: 'card card--interactive', 'aria-pressed': String(active), style: { textAlign: 'left', cursor: 'pointer', borderColor: active ? 'var(--primary)' : null, background: active ? 'var(--primary-soft)' : null },
        onclick: () => { cfg.preset = p.id; if (p.count) cfg.count = p.count; rerender(); } },
      h('div', { class: 'row', style: { gap: '10px' } }, h('span', { class: 'empty__icon', style: { width: '38px', height: '38px', margin: 0, borderRadius: '10px' } }, icon(p.icon, 18)),
        h('div', null, h('strong', null, t('preset_' + p.id)), h('div', { class: 'small muted' }, p.count ? t('nQuestions', { n: p.count }) : t('presetCustomHint')))));
    }));
    const countInput = cfg.preset === 'custom' ? h('div', { class: 'field', style: { maxWidth: '220px' } },
      h('label', { for: 'p-count' }, t('numberOfQuestions')),
      h('input', { class: 'input', id: 'p-count', type: 'number', min: '1', max: '100', value: String(cfg.count), oninput: (e) => { const v = parseInt(e.target.value, 10); cfg.count = Number.isFinite(v) ? clamp(v, 1, 100) : 10; refresh(); } })) : null;

    const form = h('section', { class: 'card card--pad-lg stack' },
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('technologies')), multi('techs', TECHS.map((x) => x.id), (id) => TECH_MAP.get(id).name, (id) => techCounts[id] || 0)),
      h('div', { class: 'grid grid--2' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('difficulty')), multi('diffs', DIFFS, (d) => t('diff_' + d))),
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('market')), seg([{ value: 'all', label: t('allMarkets') }, { value: 'bangladesh', label: t('market_bangladesh') }, { value: 'international', label: t('market_international') }], cfg.market, (v) => { cfg.market = v; rerender(); }, t('market')))),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('questionTypes')), multi('types', TYPES, (ty) => t('type_' + ty))),
      h('div', { class: 'grid grid--3' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('selection')), seg([{ value: 'random', label: t('randomized') }, { value: 'priority', label: t('priorityBased') }], cfg.order, (v) => { cfg.order = v; rerender(); }, t('selection'))),
        h('div', { class: 'field' }, h('label', { for: 'p-pool' }, t('questionPool')),
          h('select', { class: 'select', id: 'p-pool', onchange: (e) => { cfg.pool = e.target.value; refresh(); } },
            [['all', 'poolAll'], ['unanswered', 'poolUnanswered'], ['answered', 'poolAnswered'], ['mistakes', 'poolMistakes']].map(([v, k]) => h('option', { value: v, selected: cfg.pool === v }, t(k))))),
        h('div', { class: 'field' }, h('label', { for: 'p-timer' }, t('timer')),
          h('select', { class: 'select', id: 'p-timer', onchange: (e) => { cfg.timer = parseInt(e.target.value, 10) || 0; } },
            [0, 10, 20, 30, 45, 60].map((m) => h('option', { value: String(m), selected: cfg.timer === m }, m ? t('minutesN', { n: m }) : t('untimed')))))),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('language')), seg([{ value: 'en', label: 'English' }, { value: 'bn', label: 'বাংলা', lang: 'bn' }, { value: 'both', label: t('both') }], lang(), setLang, t('language'))),
      countInput,
      h('hr', { style: { margin: '4px 0' } }),
      h('div', { class: 'row row--between' }, countEl,
        btn(t('startSession'), async () => {
          const pool = matchingPool(cfg);
          if (!pool.length) { toast(t('noneMatchShort'), 'bad'); return; }
          let n = cfg.count;
          if (pool.length < n) {
            const ok = await confirmModal({ title: t('notEnoughTitle'), message: tb('fewerThanRequested', { n: pool.length, c: n }), confirmLabel: t('startWithN', { n: pool.length }) });
            if (!ok) return;
            n = pool.length;
          }
          startSession('practice', orderQuestions(pool, cfg.order).slice(0, n).map((q) => q.id), { mode: 'practice', timer: cfg.timer, preset: cfg.preset, filters: { techs: cfg.techs, diffs: cfg.diffs, types: cfg.types, market: cfg.market, pool: cfg.pool, order: cfg.order }, count: n });
        }, 'btn--primary btn--lg', 'play')),
      warnEl);
    refresh();
    const node = frag(
      pageHead('nav_practice', 'practiceLead'),
      resume,
      presets,
      countInput ? null : null,
      h('div', { class: 'mt-3' }, form),
      h('div', { class: 'callout callout--info mt-3' },
        h('div', { class: 'callout__title' }, icon('info', 16), tb('howScoringWorks')),
        h('div', { class: 'small' }, tb('scoringExplain'))));
    return { title: tb('nav_practice', null, { inline: true }), titleText: 'Practice', node };
  }

  function viewSession() {
    const s = state.activeSession;
    if (!s) {
      return { title: tb('nav_practice', null, { inline: true }), node: emptyState('play', 'noActiveSession', 'noActiveSessionText', [linkBtn('#/practice', t('nav_practice'), 'btn--primary', 'play'), linkBtn('#/interview', t('nav_interview'), 'btn--ghost', 'mic')]) };
    }
    if (s.deadline && Date.now() >= s.deadline) { finishSession(s, { timeUp: true }); return null; }
    s.index = clamp(s.index, 0, s.ids.length - 1);
    const id = s.ids[s.index];
    const q = QMAP.get(id);
    if (!q) {
      s.ids = s.ids.filter((x) => QMAP.has(x));
      if (!s.ids.length) { state.activeSession = null; saveState(); return viewSession(); }
      saveState();
      return viewSession();
    }
    const a = s.answers[id] || (s.answers[id] = { result: null, revealed: false, mcqChoice: null, at: null, firstSeenAt: Date.now() });
    if (!a.firstSeenAt) a.firstSeenAt = Date.now();
    saveState();
    const isInterview = s.kind === 'interview';
    const answeredCount = s.ids.filter((x) => s.answers[x] && s.answers[x].result).length;
    const total = s.ids.length;
    const isLast = s.index === total - 1;

    const goIndex = (i) => { s.index = clamp(i, 0, total - 1); saveState(); render({ focus: false }); window.scrollTo(0, 0); };
    const advance = () => {
      const nextUnanswered = s.ids.findIndex((x, i) => i > s.index && !(s.answers[x] && s.answers[x].result));
      if (nextUnanswered >= 0) goIndex(nextUnanswered);
      else if (!isLast) goIndex(s.index + 1);
      else rerender();
    };
    const assess = (r) => {
      a.result = r; a.at = Date.now();
      if (r !== 'skipped') a.revealed = true;
      recordResult(q.id, r, s.id);
      saveState();
      if (s.ids.every((x) => s.answers[x] && s.answers[x].result)) { rerender(); return; }
      setTimeout(advance, prefersReducedMotion() ? 0 : 220);
    };
    const endSession = async () => {
      const remaining = total - s.ids.filter((x) => s.answers[x] && s.answers[x].result).length;
      if (remaining > 0) {
        const ok = await confirmModal({ title: t('endSessionTitle'), message: tb('endSessionText', { n: remaining }), confirmLabel: t('finishNow') });
        if (!ok) return;
      }
      finishSession(s);
    };

    // Timer
    const timerEl = h('span', { class: 'timer', role: 'timer', 'aria-label': s.deadline ? t('timeRemaining') : t('timeElapsed') }, icon('clock', 15), h('span'));
    const thinkEl = h('span', { class: 'small muted' });
    const tick = () => {
      const now = Date.now();
      const span = timerEl.lastChild;
      if (s.deadline) {
        const left = s.deadline - now;
        span.textContent = fmtClock(left);
        timerEl.classList.toggle('is-low', left < 60000);
        if (left <= 0) { stopTimers(); finishSession(s, { timeUp: true }); }
      } else span.textContent = fmtClock(now - s.startedAt);
      if (isInterview && !a.result) thinkEl.textContent = t('thinkTime') + ': ' + fmtClock(now - a.firstSeenAt);
    };

    const top = h('div', { class: 'session-top' },
      h('strong', { class: 'nowrap' }, t('kind_' + s.kind)),
      h('span', { class: 'small muted nowrap' }, t('questionXofY', { x: s.index + 1, y: total })),
      progressBar(answeredCount / total, { label: t('sessionProgress') }),
      h('span', { class: 'small muted nowrap' }, answeredCount + '/' + total + ' ' + t('doneWord')),
      timerEl,
      btn(t('endSession'), endSession, 'btn--ghost btn--sm', 'stop'));

    const dots = h('nav', { class: 'dots mb-2', 'aria-label': t('questionNav') }, s.ids.map((x, i) => {
      const r = s.answers[x] && s.answers[x].result;
      return h('button', { type: 'button', class: 'dot-btn' + (r ? ' r-' + r : ''), 'aria-current': i === s.index ? 'step' : null, 'aria-label': t('questionN', { n: i + 1 }) + (r ? ' — ' + t('res_' + r) : ''), onclick: () => goIndex(i) }, String(i + 1));
    }));

    const tools = h('div', { class: 'row' },
      h('button', { type: 'button', class: 'icon-btn', 'aria-pressed': String(isBookmarked(q.id)), 'aria-label': t('bookmark') + ' (B)', title: t('bookmark') + ' (B)', onclick: () => { toggleIn('bookmarks', q.id); rerender(); } }, icon('bookmark', 18)),
      h('button', { type: 'button', class: 'icon-btn', 'aria-pressed': String(isFlagged(q.id)), 'aria-label': t('flagReview') + ' (F)', title: t('flagReview') + ' (F)', onclick: () => { toggleIn('reviewQuestions', q.id); rerender(); } }, icon('flag', 18)));

    const qCard = h('section', { class: 'card card--pad-lg' },
      h('div', { class: 'row row--between mb-1' }, h('div', { class: 'row' }, techBadge(q.technology), h('span', { class: 'small muted' }, t('questionN', { n: s.index + 1 }))), tools),
      metaBadges(q, false),
      questionBody(q),
      isInterview ? h('p', { class: 'mt-2 mb-0' }, thinkEl) : null);

    let answerArea;
    let mcqRef = null;
    if (q.isMCQ) {
      const locked = a.mcqChoice != null;
      mcqRef = mcqBlock(q, a.mcqChoice, locked, (choice) => {
        if (a.mcqChoice != null) return; // never score twice
        a.mcqChoice = choice; a.revealed = true;
        a.result = choice === q.correctIndex ? 'correct' : 'incorrect';
        a.at = Date.now();
        recordResult(q.id, a.result, s.id);
        saveState();
        rerender();
      });
      answerArea = h('section', { class: 'card card--pad-lg stack' },
        h('h2', { class: 'section-title' }, icon('list', 15), tb('chooseAnswer', null, { inline: true })),
        mcqRef,
        !locked ? h('div', null, btn(t('skip') + ' (S)', () => assess('skipped'), 'btn--ghost btn--sm', 'skip')) : null,
        locked ? answerPanel(q) : null);
    } else if (!a.revealed) {
      answerArea = h('section', { class: 'card card--pad-lg' },
        h('div', { class: 'reveal' },
          h('h2', { style: { margin: 0 } }, tb(isInterview ? 'answerAloud' : 'thinkFirst')),
          h('p', { class: 'muted', style: { margin: 0, maxWidth: '54ch' } }, tb('thinkFirstText', { n: q.estimatedMinutes })),
          h('div', { class: 'btn-row', style: { justifyContent: 'center' } },
            btn(t('revealAnswer'), () => { a.revealed = true; saveState(); rerender(); }, 'btn--primary btn--lg', 'eye', { title: t('revealAnswer') + ' (Space)' }),
            btn(t('skip'), () => assess('skipped'), 'btn--ghost', 'skip', { title: t('skip') + ' (S)' })),
          h('p', { class: 'tiny faint', style: { margin: 0 } }, icon('keyboard', 12), ' ', t('shortcutsHint'))));
    } else {
      answerArea = frag(
        h('section', { class: 'card card--pad-lg' }, answerPanel(q)),
        h('section', { class: 'card' },
          h('h2', { class: 'section-title' }, icon('target', 15), tb('howDidYouDo', null, { inline: true })),
          h('p', { class: 'small muted' }, tb('selfAssessHelp')),
          assessBar(a.result, assess, { keys: true })));
    }

    const allDone = s.ids.every((x) => s.answers[x] && s.answers[x].result);
    const footer = h('nav', { class: 'row row--between mt-2', 'aria-label': t('questionNav') },
      btn(t('previous'), () => goIndex(s.index - 1), 'btn--ghost', 'arrowL', { disabled: s.index === 0 }),
      allDone ? btn(t('seeResults'), () => finishSession(s), 'btn--primary btn--lg', 'trophy')
        : (isLast ? btn(t('finishSession'), endSession, 'btn--secondary', 'stop') : null),
      h('button', { type: 'button', class: 'btn btn--ghost', disabled: isLast, onclick: () => goIndex(s.index + 1) }, t('next'), icon('arrowR', 16)));

    ui.keyHandler = (e) => {
      const k = e.key;
      if (k === 'ArrowLeft') { if (s.index > 0) goIndex(s.index - 1); return true; }
      if (k === 'ArrowRight') { if (!isLast) goIndex(s.index + 1); return true; }
      if (k === 'b' || k === 'B') { toggleIn('bookmarks', q.id); rerender(); return true; }
      if (k === 'f' || k === 'F') { toggleIn('reviewQuestions', q.id); rerender(); return true; }
      if (q.isMCQ) {
        if (a.mcqChoice != null) { if (k === 'Enter' && !isLast) { advance(); return true; } return false; }
        if (['1', '2', '3', '4'].includes(k)) { mcqRef._select(parseInt(k, 10) - 1); return true; }
        if (['a', 'b', 'c', 'd'].includes(k.toLowerCase()) && k.toLowerCase() !== 'b') { mcqRef._select('abcd'.indexOf(k.toLowerCase())); return true; }
        if (k === 'Enter') { mcqRef._submit(); return true; }
        if (k === 's' || k === 'S') { assess('skipped'); return true; }
        return false;
      }
      if (!a.revealed) {
        if (k === ' ' || k === 'Enter') { a.revealed = true; saveState(); rerender(); return true; }
        if (k === 's' || k === 'S') { assess('skipped'); return true; }
        return false;
      }
      if (k === '1') { assess('correct'); return true; }
      if (k === '2') { assess('partial'); return true; }
      if (k === '3') { assess('incorrect'); return true; }
      if (k === '4' || k === 's' || k === 'S') { assess('skipped'); return true; }
      return false;
    };
    const node = h('div', null, top, dots, h('div', { class: 'stack' }, qCard, answerArea, footer));
    return {
      title: tb('kind_' + s.kind, null, { inline: true }), titleText: tLang('kind_' + s.kind, 'en'), node, narrow: true,
      after: () => { tick(); ui.timers.push(setInterval(tick, 1000)); },
    };
  }

  /* ======================================================================
     Results
     ====================================================================== */
  function scoreRing(fraction) {
    const v = clamp(fraction || 0, 0, 1);
    const r = 70, c = 2 * Math.PI * r;
    const svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 168 168');
    svg.setAttribute('aria-hidden', 'true');
    const track = document.createElementNS(SVG_NS, 'circle');
    track.setAttribute('class', 'track'); track.setAttribute('cx', '84'); track.setAttribute('cy', '84'); track.setAttribute('r', String(r));
    const bar = document.createElementNS(SVG_NS, 'circle');
    bar.setAttribute('class', 'bar'); bar.setAttribute('cx', '84'); bar.setAttribute('cy', '84'); bar.setAttribute('r', String(r));
    bar.setAttribute('stroke-dasharray', String(c));
    bar.setAttribute('stroke-dashoffset', String(c));
    svg.append(track, bar);
    requestAnimationFrame(() => requestAnimationFrame(() => bar.setAttribute('stroke-dashoffset', String(c * (1 - v)))));
    return svg;
  }
  function confetti() {
    if (prefersReducedMotion()) return null;
    const colors = ['var(--primary)', 'var(--easy)', 'var(--medium)', 'var(--partial)', 'var(--hard)'];
    const box = h('div', { class: 'confetti', 'aria-hidden': 'true' });
    for (let i = 0; i < 28; i++) box.append(h('i', { style: { left: (Math.random() * 100) + '%', background: colors[i % colors.length], animationDelay: (Math.random() * 0.5) + 's' } }));
    setTimeout(() => box.remove(), 2600);
    return box;
  }
  function breakdownTable(rows, firstColKey, labelFn) {
    return h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
      h('thead', null, h('tr', null, h('th', null, t(firstColKey)), h('th', { class: 'num' }, t('questionsWord')), h('th', { class: 'num' }, t('res_correct')), h('th', { class: 'num' }, t('res_partial')), h('th', { class: 'num' }, t('res_incorrect')), h('th', { class: 'num' }, t('skippedWord')), h('th', { class: 'num' }, t('points')), h('th', { class: 'num' }, t('weightedScore')))),
      h('tbody', null, rows.map(([key, b]) => h('tr', null, h('td', null, labelFn(key)), h('td', { class: 'num' }, b.total), h('td', { class: 'num' }, b.correct), h('td', { class: 'num' }, b.partial), h('td', { class: 'num' }, b.incorrect), h('td', { class: 'num' }, b.skipped), h('td', { class: 'num' }, fmtNum(b.earned) + ' / ' + b.possible), h('td', { class: 'num' }, pct(b.possible ? b.earned / b.possible : null)))))));
  }
  function viewResults(route) {
    const s = state.sessions.find((x) => x.id === route.params[0]);
    if (!s) return { title: t('notFound'), node: emptyState('alert', 'sessionNotFound', 'sessionNotFoundText', [linkBtn('#/history', t('nav_history'), 'btn--primary')]) };
    const sm = summarizeSession(s);
    const w = sm.weighted || 0;
    const band = w >= 0.85 ? 'fbExcellent' : w >= 0.65 ? 'fbGood' : w >= 0.4 ? 'fbProgress' : 'fbKeepGoing';
    const mistakes = s.ids.filter((id) => QMAP.has(id) && s.answers[id] && (s.answers[id].result === 'incorrect' || s.answers[id].result === 'partial'));
    const toReview = s.ids.filter((id) => QMAP.has(id) && (!s.answers[id] || s.answers[id].result !== 'correct'));
    const heroCard = h('section', { class: 'card card--pad-lg', style: { position: 'relative', overflow: 'hidden' } },
      w >= 0.8 ? confetti() : null,
      h('div', { class: 'results-hero' },
        h('div', { class: 'score-ring' }, scoreRing(w), h('div', { class: 'score-ring__label' }, h('div', null, h('b', null, pct(sm.weighted)), h('span', null, t('weightedScore'))))),
        h('div', { style: { flex: '1', minWidth: '240px' } },
          h('p', { class: 'meta-line' }, t('kind_' + s.kind) + ' · ' + fmtDate(s.endedAt, true)),
          h('h1', null, tb(band)),
          h('p', { class: 'muted' }, tb(band + 'Text')),
          h('div', { class: 'btn-row' },
            btn(t('reviewMistakes'), () => startQuickSession(mistakes, 'practice', { label: t('reviewMistakes') }), 'btn--primary', 'rotate', { disabled: !mistakes.length }),
            btn(t('practiceAgain'), () => practiceAgain(s), 'btn--secondary', 'shuffle'),
            linkBtn('#/dashboard', t('returnDashboard'), 'btn--ghost', 'dashboard')))));
    const statsGrid = h('section', { class: 'grid grid--stats mt-3', 'aria-label': t('sessionStats') },
      stat(t('finalScore'), fmtNum(sm.earned) + ' / ' + sm.possible, { hint: t('pointsWord') }),
      stat(t('weightedScore'), pct(sm.weighted), { hint: t('weightedHint') }),
      stat(t('accuracy'), pct(sm.accuracy), { hint: t('accuracyHint') }),
      stat(t('completionTime'), fmtDuration(sm.durationMs), null),
      stat(t('res_correct'), String(sm.correct), { tone: 'ok' }),
      stat(t('res_partial'), String(sm.partial), { tone: 'partial' }),
      stat(t('res_incorrect'), String(sm.incorrect), { tone: 'bad' }),
      stat(t('skippedWord'), String(sm.skipped), { hint: t('skippedHint') }));
    const techRows = Object.keys(sm.byTech).map((k) => [k, sm.byTech[k]]);
    const diffRows = DIFFS.filter((d) => sm.byDiff[d].total).map((d) => [d, sm.byDiff[d]]);
    const reviewList = toReview.length ? h('div', { class: 'q-list' }, toReview.map((id) => questionItem(QMAP.get(id), { navList: toReview, navLabel: t('questionsToReview'), extra: resultBadge(s.answers[id] && s.answers[id].result ? s.answers[id].result : 'skipped') })))
      : h('p', { class: 'muted' }, tb('nothingToReview'));
    const node = frag(
      heroCard,
      statsGrid,
      h('div', { class: 'callout callout--info mt-2 small' }, tb('scoringExplain')),
      h('div', { class: 'grid grid--2 mt-3' },
        h('section', { class: 'card' }, h('h2', null, tb('byTechnology')), breakdownTable(techRows, 'technology', (k) => techBadge(k))),
        h('section', { class: 'card' }, h('h2', null, tb('byDifficulty')), breakdownTable(diffRows, 'difficulty', (d) => diffBadge(d)))),
      h('section', { class: 'mt-3' }, h('h2', null, tb('questionsToReview')), reviewList));
    return { title: tb('results', null, { inline: true }), titleText: 'Results', node };
  }
  function practiceAgain(s) {
    const c = s.config || {};
    if (s.kind === 'daily') { startQuickSession(shuffle(s.ids), 'practice', { label: t('nav_daily') }); return; }
    if (c.filters) {
      const cfg = Object.assign({ techs: [], diffs: [], types: [], market: 'all', pool: 'all', order: 'random' }, c.filters);
      if (s.kind === 'interview') cfg.includeMcq = !!c.includeMcq;
      const pool = matchingPool(cfg);
      const ids = orderQuestions(pool.length ? pool : s.ids.map((id) => QMAP.get(id)).filter(Boolean), cfg.order).slice(0, c.count || s.ids.length).map((q) => q.id);
      startSession(s.kind, ids, c);
    } else startSession(s.kind, shuffle(s.ids), c);
  }

  /* ======================================================================
     Interview simulation
     ====================================================================== */
  function viewInterview() {
    const cfg = interviewDefaults();
    const countEl = h('span', { class: 'results-count', 'aria-live': 'polite' });
    const refresh = () => { clear(countEl); countEl.append(h('strong', null, String(matchingPool(cfg).length)), ' ', t('matchingQuestions')); };
    const multi = (key, values, labelFn) => h('div', { class: 'chip-group' },
      chip(t('all'), !cfg[key].length, () => { cfg[key] = []; rerender(); }),
      values.map((v) => chip(labelFn(v), cfg[key].includes(v), () => { cfg[key] = cfg[key].includes(v) ? cfg[key].filter((x) => x !== v) : cfg[key].concat(v); rerender(); })));
    const resume = state.activeSession && state.activeSession.kind === 'interview' ? h('div', { class: 'callout callout--info mb-2' },
      h('div', { class: 'callout__title' }, icon('mic', 16), tb('unfinishedInterview')),
      h('div', { class: 'btn-row' }, linkBtn('#/session', t('resumeSession'), 'btn--primary btn--sm', 'play'))) : null;
    const form = h('section', { class: 'card card--pad-lg stack' },
      h('div', { class: 'grid grid--2' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('numberOfQuestions')), seg([5, 8, 10, 15].map((n) => ({ value: n, label: String(n) })), cfg.count, (v) => { cfg.count = v; rerender(); }, t('numberOfQuestions'))),
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('timeLimit')), seg([0, 15, 30, 45, 60].map((m) => ({ value: m, label: m ? m + 'm' : t('none') })), cfg.timer, (v) => { cfg.timer = v; rerender(); }, t('timeLimit')))),
      h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('technologies')), multi('techs', TECHS.map((x) => x.id), (id) => TECH_MAP.get(id).name)),
      h('div', { class: 'grid grid--2' },
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('difficulty')), multi('diffs', DIFFS, (d) => t('diff_' + d))),
        h('div', { class: 'field' }, h('span', { class: 'field-label' }, t('market')), seg([{ value: 'all', label: t('allMarkets') }, { value: 'bangladesh', label: t('market_bangladesh') }, { value: 'international', label: t('market_international') }], cfg.market, (v) => { cfg.market = v; rerender(); }, t('market')))),
      h('label', { class: 'check' }, h('input', { type: 'checkbox', checked: cfg.includeMcq, onchange: (e) => { cfg.includeMcq = e.target.checked; refresh(); } }), t('includeMcq')),
      h('div', { class: 'row row--between' }, countEl,
        btn(t('startInterview'), async () => {
          const pool = matchingPool(cfg);
          if (!pool.length) { toast(t('noneMatchShort'), 'bad'); return; }
          let n = cfg.count;
          if (pool.length < n) {
            const ok = await confirmModal({ title: t('notEnoughTitle'), message: tb('fewerThanRequested', { n: pool.length, c: n }), confirmLabel: t('startWithN', { n: pool.length }) });
            if (!ok) return;
            n = pool.length;
          }
          // Interviews usually move from easier to harder questions
          const picked = shuffle(pool).slice(0, n).sort((a, b) => DIFFS.indexOf(a.difficulty) - DIFFS.indexOf(b.difficulty));
          startSession('interview', picked.map((q) => q.id), { mode: 'interview', timer: cfg.timer, includeMcq: cfg.includeMcq, count: n, filters: { techs: cfg.techs, diffs: cfg.diffs, market: cfg.market, types: [], pool: 'all', order: 'random' } });
        }, 'btn--primary btn--lg', 'mic')));
    refresh();
    const how = h('section', { class: 'card' },
      h('h2', null, tb('howInterviewWorks')),
      h('ol', { class: 'prose' }, ['iw1', 'iw2', 'iw3', 'iw4'].map((k) => h('li', null, tb(k)))));
    const node = frag(pageHead('nav_interview', 'interviewLead'), resume, h('div', { class: 'grid grid--2-1' }, form, how));
    return { title: tb('nav_interview', null, { inline: true }), titleText: 'Interview Simulation', node };
  }

  /* ======================================================================
     Daily challenge (deterministic by local date, no server)
     ====================================================================== */
  function dailyIdsFor(key) {
    const rnd = mulberry32(hashString('daily:' + key));
    const chosen = [];
    const pickFrom = (filter) => {
      const pool = QUESTIONS.filter((q) => filter(q) && !chosen.includes(q));
      if (!pool.length) return null;
      const q = pool[Math.floor(rnd() * pool.length)];
      chosen.push(q);
      return q;
    };
    pickFrom((q) => q.isMCQ && (q.difficulty === 'easy' || q.difficulty === 'medium')) || pickFrom(() => true);
    pickFrom((q) => !q.isMCQ && q.difficulty === 'medium') || pickFrom(() => true);
    pickFrom((q) => q.difficulty === 'hard') || pickFrom(() => true);
    return chosen.map((q) => q.id);
  }
  function dailyInfo() {
    const key = localDateKey();
    const rec = state.daily[key];
    return { key, ids: dailyIdsFor(key), done: !!rec, sessionId: rec ? rec.sessionId : null, score: rec ? rec.score : null };
  }
  function dailyStreak() {
    let n = 0;
    const d = new Date();
    if (!state.daily[localDateKey(d)]) d.setDate(d.getDate() - 1);
    while (state.daily[localDateKey(d)]) { n++; d.setDate(d.getDate() - 1); }
    return n;
  }
  function viewDaily() {
    const info = dailyInfo();
    const active = state.activeSession && state.activeSession.kind === 'daily' && state.activeSession.dateKey === info.key;
    const items = info.ids.map((id, i) => {
      const q = QMAP.get(id);
      return h('li', { class: 'card', style: { padding: '14px 16px' } },
        h('div', { class: 'row row--between' },
          h('div', { class: 'row' }, h('strong', null, '#' + (i + 1)), techBadge(q.technology), diffBadge(q.difficulty), typeBadge(q.type)),
          info.done ? h('a', { href: '#/q/' + encodeURIComponent(id), class: 'small' }, t('open')) : h('span', { class: 'small muted' }, t('hiddenUntilStart'))),
        info.done ? h('div', { class: 'mt-1' }, biTitle(q.question, 'q-item__title')) : null);
    });
    const node = frag(
      pageHead('nav_daily', 'dailyLead', null, info.key),
      !QUESTIONS.length ? emptyState('database', 'bankEmpty', 'bankEmptyText') : h('div', { class: 'grid grid--2-1' },
        h('section', { class: 'stack' },
          h('ol', { class: 'list-plain' }, items),
          h('div', { class: 'btn-row' },
            info.done ? linkBtn('#/results/' + encodeURIComponent(info.sessionId), t('viewResults'), 'btn--primary', 'trophy')
              : active ? linkBtn('#/session', t('resumeSession'), 'btn--primary btn--lg', 'play')
                : btn(t('startChallenge'), () => startSession('daily', info.ids, { mode: 'practice', timer: 0 }), 'btn--primary btn--lg', 'zap'),
            info.done ? btn(t('practiceAgain'), () => startQuickSession(info.ids, 'practice', { label: t('nav_daily') }), 'btn--ghost', 'shuffle') : null)),
        h('section', { class: 'card stack stack--sm' },
          h('h2', null, tb('dailyStatus')),
          h('dl', { class: 'kv' },
            h('dt', null, t('today')), h('dd', null, info.done ? h('span', { class: 'badge badge--ok' }, icon('check', 12), t('completed')) : h('span', { class: 'badge' }, t('notYet'))),
            h('dt', null, t('weightedScore')), h('dd', null, pct(info.score)),
            h('dt', null, t('dailyStreak')), h('dd', null, t('daysN', { n: dailyStreak() }))),
          h('p', { class: 'small muted mb-0' }, tb('dailyHow')))));
    return { title: tb('nav_daily', null, { inline: true }), titleText: 'Daily Challenge', node };
  }

  /* ======================================================================
     Flashcards
     ====================================================================== */
  const flash = { tech: '', diff: '', source: 'all', ids: null, index: 0, flipped: false, sig: '' };
  function flashDeck() {
    const sig = [flash.tech, flash.diff, flash.source].join('|');
    if (flash.ids && flash.sig === sig) return flash.ids.filter((id) => QMAP.has(id));
    let list = QUESTIONS;
    if (flash.tech) list = list.filter((q) => q.technology === flash.tech);
    if (flash.diff) list = list.filter((q) => q.difficulty === flash.diff);
    if (flash.source === 'bookmarked') list = list.filter((q) => isBookmarked(q.id));
    else if (flash.source === 'due') { const due = new Set(dueIds()); list = list.filter((q) => due.has(q.id) || isFlagged(q.id)); }
    else if (flash.source === 'incorrect') list = list.filter((q) => { const s = statusOf(q.id); return s === 'incorrect' || s === 'partial'; });
    else if (flash.source === 'unlearned') list = list.filter((q) => !isLearned(q.id));
    flash.ids = list.map((q) => q.id);
    flash.sig = sig;
    flash.index = 0;
    flash.flipped = false;
    return flash.ids;
  }
  function plainCode(code) {
    return h('figure', { class: 'code' }, h('div', { class: 'code__bar' }, h('span', { class: 'code__lang' }, code.language || 'text')), h('pre', null, h('code', null, highlight(code.source, code.language))));
  }
  function viewFlashcards() {
    const deck = flashDeck();
    flash.index = clamp(flash.index, 0, Math.max(0, deck.length - 1));
    const setF = (k, v) => { flash[k] = v; flash.ids = null; rerender(); };
    const controls = h('section', { class: 'card card--flat' }, h('div', { class: 'filters filters--4' },
      h('div', { class: 'field' }, h('label', { for: 'fc-tech' }, t('technology')), h('select', { class: 'select', id: 'fc-tech', onchange: (e) => setF('tech', e.target.value) }, [['', t('allTechs')]].concat(TECHS.map((x) => [x.id, x.name])).map(([v, l]) => h('option', { value: v, selected: flash.tech === v }, l)))),
      h('div', { class: 'field' }, h('label', { for: 'fc-diff' }, t('difficulty')), h('select', { class: 'select', id: 'fc-diff', onchange: (e) => setF('diff', e.target.value) }, [['', t('allLevels')]].concat(DIFFS.map((d) => [d, t('diff_' + d)])).map(([v, l]) => h('option', { value: v, selected: flash.diff === v }, l)))),
      h('div', { class: 'field' }, h('label', { for: 'fc-src' }, t('deck')), h('select', { class: 'select', id: 'fc-src', onchange: (e) => setF('source', e.target.value) }, [['all', 'deckAll'], ['unlearned', 'deckUnlearned'], ['bookmarked', 'nav_bookmarks'], ['due', 'deckDue'], ['incorrect', 'deckMistakes']].map(([v, k]) => h('option', { value: v, selected: flash.source === v }, t(k))))),
      h('div', { class: 'field' }, h('span', { class: 'field-label', 'aria-hidden': 'true' }, ' '), btn(t('shuffle'), () => { flash.ids = shuffle(deck); flash.index = 0; flash.flipped = false; rerender(); }, '', 'shuffle', { disabled: deck.length < 2 }))));
    if (!deck.length) {
      return { title: tb('nav_flashcards', null, { inline: true }), node: frag(pageHead('nav_flashcards', 'flashLead'), controls, h('div', { class: 'mt-3' }, emptyState('cards', 'emptyDeck', 'emptyDeckText'))) };
    }
    const q = QMAP.get(deck[flash.index]);
    const flip = () => { flash.flipped = !flash.flipped; card.classList.toggle('is-flipped', flash.flipped); card.setAttribute('aria-pressed', String(flash.flipped)); };
    const nav = (d) => { flash.index = clamp(flash.index + d, 0, deck.length - 1); flash.flipped = false; rerender(); };
    const front = h('div', { class: 'flashcard__face flashcard__face--front', 'aria-hidden': String(flash.flipped) },
      h('div', { class: 'row' }, techBadge(q.technology), diffBadge(q.difficulty), typeBadge(q.type)),
      biText(q.question, { cls: 'q-title', plain: true }),
      q.setup && q.setup.source ? plainCode(q.setup) : null,
      codeInQuestion(q) ? plainCode(q.code) : null,
      q.isMCQ ? h('ol', { type: 'A', class: 'prose' }, q.options.map((o) => h('li', null, pick(o)))) : null,
      h('p', { class: 'flash-hint' }, t('tapToFlip')));
    const back = h('div', { class: 'flashcard__face flashcard__face--back', 'aria-hidden': String(!flash.flipped) },
      h('div', { class: 'meta-line' }, t('referenceAnswer')),
      q.isMCQ ? h('p', null, h('strong', null, t('correctAnswer') + ': ' + 'ABCD'[q.correctIndex] + ' — '), pick(q.options[q.correctIndex])) : null,
      biText(q.answer),
      q.code && q.code.output ? h('div', null, h('div', { class: 'small muted' }, t('expectedOutput')), h('pre', { class: 'mono small' }, q.code.output)) : null);
    const card = h('button', { type: 'button', class: 'flashcard' + (flash.flipped ? ' is-flipped' : ''), 'aria-pressed': String(flash.flipped), 'aria-label': t('flipCard'), onclick: flip }, front, back);
    ui.keyHandler = (e) => {
      if (e.key === ' ' || e.key === 'Enter') { if (document.activeElement === card) return false; flip(); return true; }
      if (e.key === 'ArrowRight') { nav(1); return true; }
      if (e.key === 'ArrowLeft') { nav(-1); return true; }
      return false;
    };
    const node = frag(
      pageHead('nav_flashcards', 'flashLead'),
      controls,
      h('div', { class: 'row row--between mt-3 mb-1', style: { maxWidth: '760px', marginInline: 'auto' } },
        h('span', { class: 'small muted' }, t('cardXofY', { x: flash.index + 1, y: deck.length })),
        progressBar((flash.index + 1) / deck.length, { thin: true }),
        h('a', { href: '#/q/' + encodeURIComponent(q.id), class: 'small', onclick: () => { ui.navList = deck.slice(); ui.navLabel = t('nav_flashcards'); } }, t('openFull'))),
      h('div', { class: 'flash-wrap' }, card),
      h('div', { class: 'btn-row mt-2', style: { justifyContent: 'center' } },
        btn(t('previous'), () => nav(-1), 'btn--ghost', 'arrowL', { disabled: flash.index === 0 }),
        btn(t('flip'), flip, 'btn--secondary', 'rotate'),
        h('button', { type: 'button', class: 'btn btn--ghost', disabled: flash.index >= deck.length - 1, onclick: () => nav(1) }, t('next'), icon('arrowR', 16))),
      h('div', { class: 'btn-row mt-1', style: { justifyContent: 'center' } },
        toggleBtnInline(isLearned(q.id), 'grad', t('learned'), t('markLearned'), () => { toggleIn('learnedQuestions', q.id); rerender(); }),
        toggleBtnInline(isFlagged(q.id), 'flag', t('flagged'), t('needsReviewBtn'), () => { toggleIn('reviewQuestions', q.id); rerender(); }),
        toggleBtnInline(isBookmarked(q.id), 'bookmark', t('bookmarked'), t('bookmark'), () => { toggleIn('bookmarks', q.id); rerender(); })),
      h('p', { class: 'flash-hint' }, icon('keyboard', 12), ' ', t('flashKeys')));
    return { title: tb('nav_flashcards', null, { inline: true }), titleText: 'Flashcards', node, narrow: false };
  }
  function toggleBtnInline(pressed, ic, onLabel, offLabel, onClick) {
    return h('button', { type: 'button', class: 'btn btn--sm ' + (pressed ? 'btn--secondary' : 'btn--ghost'), 'aria-pressed': String(pressed), onclick: onClick }, icon(ic, 15), pressed ? onLabel : offLabel);
  }

  /* ======================================================================
     Bookmarks / Incorrect / Review
     ====================================================================== */
  function viewBookmarks() {
    const list = state.bookmarks.map((id) => QMAP.get(id)).filter(Boolean);
    const ids = list.map((q) => q.id);
    const node = frag(
      pageHead('nav_bookmarks', 'bookmarksLead', list.length ? [
        btn(t('practiceThese'), () => startQuickSession(shuffle(ids), 'practice', { label: t('nav_bookmarks') }), 'btn--primary', 'play'),
        btn(t('nav_flashcards'), () => { flash.source = 'bookmarked'; flash.tech = ''; flash.diff = ''; flash.ids = null; go('#/flashcards'); }, 'btn--ghost', 'cards'),
      ] : null),
      list.length ? frag(h('p', { class: 'results-count' }, h('strong', null, String(list.length)), ' ', t('bookmarkedQuestions')), questionList(list, t('nav_bookmarks')))
        : emptyState('bookmark', 'noBookmarks', 'noBookmarksText', [linkBtn('#/questions', t('browseQuestions'), 'btn--primary', 'list')]));
    return { title: tb('nav_bookmarks', null, { inline: true }), titleText: 'Bookmarks', node };
  }

  function viewIncorrect() {
    const tab = ui.incorrectTab;
    const incorrect = QUESTIONS.filter((q) => statusOf(q.id) === 'incorrect');
    const partial = QUESTIONS.filter((q) => statusOf(q.id) === 'partial');
    const list = tab === 'incorrect' ? incorrect : partial;
    const tabs = seg([
      { value: 'incorrect', label: t('res_incorrect') + ' (' + incorrect.length + ')' },
      { value: 'partial', label: t('res_partial') + ' (' + partial.length + ')' },
    ], tab, (v) => { ui.incorrectTab = v; rerender(); }, t('filter'));
    const all = incorrect.concat(partial).map((q) => q.id);
    const node = frag(
      pageHead('nav_incorrect', 'incorrectLead', all.length ? [btn(t('practiceMistakes'), () => startQuickSession(shuffle(all), 'practice', { label: t('nav_incorrect') }), 'btn--primary', 'rotate')] : null),
      h('div', { class: 'row row--between mb-2' }, tabs, h('span', { class: 'small muted' }, tb('latestResultNote'))),
      list.length ? questionList(list, t('nav_incorrect')) : emptyState('checkCircle', tab === 'incorrect' ? 'noIncorrect' : 'noPartial', 'noMistakesText', [linkBtn('#/practice', t('startPractice'), 'btn--primary', 'play')]));
    return { title: tb('nav_incorrect', null, { inline: true }), titleText: 'Incorrect Answers', node };
  }

  function viewReview() {
    const due = dueIds().map((id) => QMAP.get(id));
    const flagged = state.reviewQuestions.map((id) => QMAP.get(id)).filter(Boolean);
    const upcoming = upcomingIds(7).map((id) => QMAP.get(id));
    const recent = QUESTIONS.filter((q) => lastAt(q.id)).sort((a, b) => lastAt(b.id) - lastAt(a.id)).slice(0, 10);
    const reviewIds = Array.from(new Set(due.concat(flagged).map((q) => q.id)));
    const dueBadge = (q) => { const p = prog(q.id); return p && p.due ? h('span', { class: 'badge badge--warn' }, icon('calendar', 12), fmtDate(p.due)) : null; };
    const block = (titleKey, list, emptyKey, extraFn) => h('section', { class: 'mt-3' },
      h('div', { class: 'row row--between mb-1' }, h('h2', { class: 'mb-0' }, tb(titleKey)), h('span', { class: 'badge' }, String(list.length))),
      list.length ? h('div', { class: 'q-list' }, list.map((q) => questionItem(q, { navList: list.map((x) => x.id), navLabel: t(titleKey), extra: extraFn ? extraFn(q) : null })))
        : h('p', { class: 'muted small' }, tb(emptyKey)));
    const node = frag(
      pageHead('nav_review', 'reviewLead', reviewIds.length ? [btn(t('reviewNow'), () => startQuickSession(reviewIds, 'practice', { label: t('nav_review') }), 'btn--primary', 'rotate')] : null),
      h('div', { class: 'callout callout--info' }, h('div', { class: 'callout__title' }, icon('info', 16), tb('reviewScheduleTitle')), h('div', { class: 'small' }, tb('reviewScheduleText'))),
      block('dueForReview', due, 'nothingDue', dueBadge),
      block('flaggedForReview', flagged, 'nothingFlagged'),
      block('upcomingReviews', upcoming, 'nothingUpcoming', dueBadge),
      block('recentlyStudied', recent, 'nothingRecent', (q) => resultBadge(statusOf(q.id))));
    return { title: tb('nav_review', null, { inline: true }), titleText: 'Review Questions', node };
  }

  /* ======================================================================
     Study history
     ====================================================================== */
  function heatmap(weeks) {
    const end = new Date(); end.setHours(0, 0, 0, 0);
    const start = new Date(end); start.setDate(start.getDate() - (weeks * 7 - 1) - end.getDay());
    const cells = [];
    let activeDays = 0, totalActs = 0;
    for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
      const k = localDateKey(d);
      const n = state.activity[k] || 0;
      if (n) { activeDays++; totalActs += n; }
      const l = n === 0 ? 0 : n < 3 ? 1 : n < 8 ? 2 : n < 15 ? 3 : 4;
      cells.push(h('i', { 'data-l': String(l), title: k + ': ' + n }));
    }
    return { el: h('div', { class: 'heatmap', role: 'img', 'aria-label': t('heatmapLabel', { d: activeDays, n: totalActs, w: weeks }) }, cells), activeDays, totalActs };
  }
  function viewHistory() {
    const sessions = state.sessions.slice().reverse();
    const hm = heatmap(16);
    const streak = streakInfo();
    const totals = sessions.reduce((acc, s) => { const sm = s.summary || summarizeSession(s); acc.q += sm.total; acc.ms += sm.durationMs; return acc; }, { q: 0, ms: 0 });
    const table = sessions.length ? h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
      h('caption', { class: 'sr-only' }, t('nav_history')),
      h('thead', null, h('tr', null, h('th', null, t('date')), h('th', null, t('typeWord')), h('th', { class: 'num' }, t('questionsWord')), h('th', { class: 'num' }, t('weightedScore')), h('th', { class: 'num' }, t('accuracy')), h('th', { class: 'num' }, t('duration')), h('th', null, ''))),
      h('tbody', null, sessions.map((s) => {
        const sm = s.summary || summarizeSession(s);
        return h('tr', null,
          h('td', null, fmtDate(s.endedAt, true)),
          h('td', null, t('kind_' + s.kind), s.config && s.config.label ? h('span', { class: 'muted small' }, ' · ' + s.config.label) : null),
          h('td', { class: 'num' }, sm.total),
          h('td', { class: 'num' }, pct(sm.weighted)),
          h('td', { class: 'num' }, pct(sm.accuracy)),
          h('td', { class: 'num' }, fmtDuration(sm.durationMs)),
          h('td', null, h('a', { href: '#/results/' + encodeURIComponent(s.id) }, t('details'))));
      })))) : emptyState('clock', 'noHistory', 'noHistoryText', [linkBtn('#/practice', t('startPractice'), 'btn--primary', 'play')]);
    const node = frag(
      pageHead('nav_history', 'historyLead'),
      h('div', { class: 'grid grid--stats' },
        stat(t('sessionsWord'), String(sessions.length), null),
        stat(t('questionsPracticed'), String(totals.q), null),
        stat(t('timeSpent'), fmtDuration(totals.ms), null),
        stat(t('activeDays'), String(hm.activeDays), { hint: t('lastNWeeks', { n: 16 }) }),
        stat(t('studyStreak'), t('daysN', { n: streak.current }), { hint: t('bestStreak', { n: streak.best }) })),
      h('section', { class: 'card mt-3' },
        h('div', { class: 'card__head' }, h('h2', null, tb('activity')), h('span', { class: 'card__sub' }, t('heatmapLabel', { d: hm.activeDays, n: hm.totalActs, w: 16 }))),
        hm.el,
        h('div', { class: 'legend' }, h('span', null, t('less')), [0, 1, 2, 3, 4].map((l) => h('i', { style: { background: l ? null : 'var(--card-2)' }, class: 'hm-legend', 'data-l': String(l) })), h('span', null, t('more')))),
      h('section', { class: 'mt-3' }, h('h2', null, tb('pastSessions')), table));
    return { title: tb('nav_history', null, { inline: true }), titleText: 'Study History', node };
  }

  /* ======================================================================
     Study planner
     ====================================================================== */
  function viewPlanner() {
    const target = state.planner.dailyTarget;
    const days = [];
    for (let i = 6; i >= 0; i--) { const d = new Date(); d.setDate(d.getDate() - i); days.push(localDateKey(d)); }
    const maxV = Math.max(target, ...days.map((k) => state.activity[k] || 0), 1);
    const remaining = QUESTIONS.filter((q) => !isAnswered(q.id) && !isLearned(q.id)).length;
    let daysLeft = null;
    if (state.planner.interviewDate) {
      daysLeft = Math.round((startOfDay(new Date(state.planner.interviewDate + 'T00:00:00')) - startOfDay()) / DAY);
    }
    const suggested = daysLeft && daysLeft > 0 ? Math.ceil(remaining / daysLeft) : null;
    const today = state.activity[localDateKey()] || 0;
    const targetInput = h('input', { class: 'input', id: 'pl-target', type: 'number', min: '1', max: '200', value: String(target), style: { maxWidth: '140px' } });
    const dateInput = h('input', { class: 'input', id: 'pl-date', type: 'date', value: state.planner.interviewDate || '', style: { maxWidth: '200px' } });
    const save = () => {
      const v = parseInt(targetInput.value, 10);
      if (!Number.isFinite(v) || v < 1 || v > 200) { toast(t('invalidTarget'), 'bad'); targetInput.focus(); return; }
      state.planner.dailyTarget = v;
      state.planner.interviewDate = /^\d{4}-\d{2}-\d{2}$/.test(dateInput.value) ? dateInput.value : '';
      saveState();
      toast(t('plannerSaved'), 'ok');
      rerender();
    };
    const weak = weakAreas(6);
    const wd = weakDifficulties().filter((x) => x.attempts >= 3);
    const due = dueIds();
    const node = frag(
      pageHead('nav_planner', 'plannerLead'),
      h('div', { class: 'grid grid--2' },
        h('section', { class: 'card stack' },
          h('h2', null, tb('dailyTarget')),
          h('div', { class: 'row', style: { alignItems: 'flex-end' } },
            h('div', { class: 'field' }, h('label', { for: 'pl-target' }, t('questionsPerDay')), targetInput),
            h('div', { class: 'field' }, h('label', { for: 'pl-date' }, t('interviewDate')), dateInput),
            btn(t('save'), save, 'btn--primary', 'check')),
          h('div', null,
            h('div', { class: 'row row--between mb-1' }, h('strong', null, t('todayProgress', { n: today, t: target })), h('span', { class: 'small muted' }, pct(Math.min(1, today / target)))),
            progressBar(today / target, { lg: true, label: t('todaysGoal') })),
          h('p', { class: 'small muted mb-0' }, tb('activityDefinition'))),
        h('section', { class: 'card' },
          h('h2', null, tb('last7Days')),
          h('div', { class: 'vbars', role: 'img', 'aria-label': days.map((k) => k + ': ' + (state.activity[k] || 0)).join(', ') },
            days.map((k) => {
              const v = state.activity[k] || 0;
              return h('div', { class: 'vbar' }, h('span', { class: 'vbar__val' }, String(v)), h('div', { class: 'vbar__fill' + (v >= target ? ' is-goal' : ''), style: { height: Math.max(3, (v / maxV) * 90) + '%' } }), h('span', { class: 'vbar__label' }, fmtDay(k)));
            })),
          h('p', { class: 'small muted mt-1 mb-0' }, t('goalLine', { n: target })))),
      h('div', { class: 'grid grid--3 mt-3' },
        stat(t('remainingQuestions'), String(remaining), { hint: t('notAnsweredOrLearned') }),
        stat(t('daysUntilInterview'), daysLeft == null ? '—' : daysLeft < 0 ? t('passed') : String(daysLeft), { hint: state.planner.interviewDate || t('setDateHint') }),
        stat(t('suggestedPerDay'), suggested == null ? '—' : String(suggested), { hint: t('suggestedHint') })),
      h('div', { class: 'grid grid--2 mt-3' },
        h('section', { class: 'card' },
          h('h2', null, tb('weakTopics')),
          weak.length ? weakList(weak) : h('p', { class: 'muted small' }, tb('noWeakTopics')),
          wd.length ? h('div', { class: 'mt-2' }, h('h3', { class: 'section-title' }, t('missRateByDifficulty')),
            h('div', { class: 'bars' }, wd.map((x) => h('div', { class: 'bar-row' }, h('span', { class: 'bar-row__label' }, diffBadge(x.difficulty)), progressBar(x.missRate, { thin: true, label: t('missRate') }), h('span', { class: 'bar-row__value' }, pct(x.missRate)))))) : null,
          h('p', { class: 'tiny faint mt-2 mb-0' }, tb('weakHow'))),
        h('section', { class: 'card' },
          h('h2', null, tb('recommendedNext')),
          h('ul', { class: 'list-plain' },
            due.length ? h('li', null, icon('rotate', 16), h('div', null, tb('recDue', { n: due.length }), h('div', { class: 'mt-1' }, btn(t('reviewNow'), () => startQuickSession(due, 'practice', { label: t('nav_review') }), 'btn--sm btn--secondary', 'play')))) : null,
            h('li', null, icon('zap', 16), h('div', null, tb('recDaily'), h('div', { class: 'mt-1' }, linkBtn('#/daily', t('nav_daily'), 'btn--sm btn--ghost')))),
            h('li', null, icon('target', 16), h('div', null, tb('recPractice', { n: Math.min(target, 30) }), h('div', { class: 'mt-1' }, btn(t('startPractice'), () => { const cfg = practiceDefaults(); cfg.preset = 'custom'; cfg.count = Math.min(Math.max(target, 5), 30); cfg.order = 'priority'; cfg.pool = 'all'; go('#/practice'); }, 'btn--sm btn--ghost')))),
            h('li', null, icon('mic', 16), h('div', null, tb('recInterview'), h('div', { class: 'mt-1' }, linkBtn('#/interview', t('nav_interview'), 'btn--sm btn--ghost'))))))));
    return { title: tb('nav_planner', null, { inline: true }), titleText: 'Study Planner', node };
  }

  /* ======================================================================
     Settings: preferences, backup, reset, data health
     ====================================================================== */
  function downloadJSON(obj, filename) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = h('a', { href: url, download: filename, style: { display: 'none' } });
    document.body.append(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 500);
  }
  function viewSettings() {
    const p = state.preferences;
    const setPref = (k, v) => { p[k] = v; saveState(); applyPreferences(); rerender(); };
    const fileInput = h('input', { type: 'file', accept: 'application/json,.json', class: 'sr-only', id: 'importFile', onchange: (e) => handleImport(e.target) });
    const row = (labelKey, hintKey, control) => h('div', { class: 'row row--between', style: { padding: '12px 0', borderBottom: '1px solid var(--border)', gap: '16px' } },
      h('div', { style: { minWidth: '200px', flex: '1' } }, h('strong', null, tb(labelKey)), hintKey ? h('div', { class: 'small muted' }, tb(hintKey)) : null), control);
    const v = VALIDATION;
    const node = frag(
      pageHead('nav_settings', 'settingsLead'),
      h('div', { class: 'grid grid--2' },
        h('section', { class: 'card' },
          h('h2', null, tb('preferences')),
          row('language', 'languageHint', seg([{ value: 'en', label: 'English' }, { value: 'bn', label: 'বাংলা', lang: 'bn' }, { value: 'both', label: t('both') }], p.lang, setLang, t('language'))),
          row('theme', null, seg([{ value: 'dark', label: t('dark') }, { value: 'light', label: t('light') }], p.theme, (v2) => setPref('theme', v2), t('theme'))),
          row('defaultMode', 'defaultModeHint', seg([{ value: 'learning', label: t('learningMode') }, { value: 'interview', label: t('interviewMode') }], p.mode, (v2) => setPref('mode', v2), t('defaultMode'))),
          row('motion', 'motionHint', seg([{ value: 'system', label: t('motionSystem') }, { value: 'reduce', label: t('motionReduce') }, { value: 'full', label: t('motionFull') }], p.motion, (v2) => setPref('motion', v2), t('motion'))),
          row('textSize', null, seg([0.9, 1, 1.1, 1.2].map((x) => ({ value: x, label: Math.round(x * 100) + '%' })), p.fontScale, (v2) => setPref('fontScale', v2), t('textSize'))),
          row('sidebar', null, seg([{ value: false, label: t('expanded') }, { value: true, label: t('collapsed') }], p.sidebarCollapsed, (v2) => setPref('sidebarCollapsed', v2), t('sidebar')))),
        h('div', { class: 'stack' },
          h('section', { class: 'card stack stack--sm' },
            h('h2', null, tb('dataBackup')),
            h('p', { class: 'small muted' }, tb('localOnlyLong')),
            h('div', { class: 'btn-row' },
              btn(t('exportData'), () => { downloadJSON(exportData(), 'interview-prep-bd-backup-' + localDateKey() + '.json'); toast(t('exported'), 'ok'); }, 'btn--secondary', 'download'),
              h('label', { class: 'btn', for: 'importFile', tabindex: '0', role: 'button', onkeydown: (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); } } }, icon('upload', 16), t('importData')),
              fileInput),
            h('p', { class: 'tiny faint mb-0' }, tb('importHint'))),
          h('section', { class: 'card stack stack--sm', style: { borderColor: 'color-mix(in srgb, var(--bad) 35%, var(--border))' } },
            h('h2', null, tb('dangerZone')),
            h('p', { class: 'small muted' }, tb('resetHint')),
            h('div', null, btn(t('resetProgress'), async () => {
              const ok = await confirmModal({ title: t('resetTitle'), message: tb('resetText'), confirmLabel: t('resetProgress'), danger: true, requireText: 'RESET' });
              if (!ok) return;
              const prefs = Object.assign({}, state.preferences);
              state = defaultState();
              state.preferences = prefs;
              saveState();
              ui.revealed.clear(); ui.hidden.clear(); ui.mcq = {};
              toast(t('progressReset'), 'ok');
              rerender();
            }, 'btn--danger', 'trash'))),
          h('section', { class: 'card stack stack--sm' },
            h('h2', null, tb('dataHealth')),
            h('dl', { class: 'kv' },
              h('dt', null, t('records')), h('dd', null, String(v.total)),
              h('dt', null, t('usableQuestions')), h('dd', null, String(QUESTIONS.length)),
              h('dt', null, t('errors')), h('dd', null, h('span', { class: 'badge ' + (v.errors.length ? 'badge--bad' : 'badge--ok') }, String(v.errors.length))),
              h('dt', null, t('warnings')), h('dd', null, h('span', { class: 'badge ' + (v.warnings.length ? 'badge--warn' : 'badge--ok') }, String(v.warnings.length)))),
            h('div', null, btn(t('showDetails'), () => openModal({
              title: t('dataHealth'),
              body: v.errors.length || v.warnings.length
                ? h('div', { style: { maxHeight: '50vh', overflow: 'auto' } }, h('ul', { class: 'small mono' }, v.errors.map((e) => h('li', { style: { color: 'var(--bad)' } }, e)), v.warnings.map((w) => h('li', { style: { color: 'var(--partial)' } }, w))))
                : h('p', null, tb('noValidationIssues')),
            }), 'btn--ghost btn--sm', 'info')),
            h('p', { class: 'tiny faint mb-0' }, tb('validationConsole'))))));
    return { title: tb('nav_settings', null, { inline: true }), titleText: 'Settings', node };
  }
  function handleImport(input) {
    const file = input.files && input.files[0];
    input.value = '';
    if (!file) return;
    if (file.size > 15 * 1024 * 1024) { toast(t('import_tooLarge'), 'bad'); return; }
    const reader = new FileReader();
    reader.onerror = () => toast(t('import_readError'), 'bad');
    reader.onload = async () => {
      const res = parseImport(String(reader.result || ''));
      if (!res.ok) { toast(t('import_' + res.error), 'bad', 5000); return; }
      const s = res.summary;
      const ok = await confirmModal({
        title: t('importConfirmTitle'),
        message: h('div', null, h('p', null, tb('importConfirmText')), h('ul', null,
          h('li', null, t('nav_bookmarks') + ': ' + s.bookmarks),
          h('li', null, t('learned') + ': ' + s.learned),
          h('li', null, t('flaggedForReview') + ': ' + s.review),
          h('li', null, t('questionsWithProgress') + ': ' + s.progress),
          h('li', null, t('sessionsWord') + ': ' + s.sessions),
          s.exportedAt ? h('li', null, t('exportedAt') + ': ' + s.exportedAt) : null)),
        confirmLabel: t('replaceMyData'), danger: true,
      });
      if (!ok) return;
      state = res.data;
      saveState();
      applyPreferences();
      toast(t('imported'), 'ok');
      rerender();
    };
    reader.readAsText(file);
  }

  /* ======================================================================
     Versions & sources
     ====================================================================== */
  function viewSources() {
    const byTech = TECHS.map((tc) => [tc, countBy(BY_TECH.get(tc.id), 'difficulty'), BY_TECH.get(tc.id).length]);
    const typeCounts = countBy(QUESTIONS, 'type');
    const marketCounts = countBy(QUESTIONS, 'market');
    const group = (g, titleKey) => h('section', { class: 'card' },
      h('h2', null, tb(titleKey)),
      h('ul', { class: 'list-plain ref-list' }, SOURCES.filter((s) => s.group === g).map((s) => h('li', null, icon('link', 14), h('a', { href: s.url, target: '_blank', rel: 'noopener noreferrer' }, s.title)))));
    const node = frag(
      pageHead('nav_sources', 'sourcesLead', null, t('verifiedOn', { date: VERIFIED_AT })),
      h('section', { class: 'card' },
        h('h2', null, tb('verifiedVersions')),
        h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
          h('thead', null, h('tr', null, h('th', null, t('technology')), h('th', null, t('version')), h('th', null, t('notes')), h('th', null, t('source')))),
          h('tbody', null, VERSIONS.map((v) => h('tr', null, h('td', null, h('strong', null, v.tech)), h('td', { class: 'wrap' }, v.version), h('td', { class: 'wrap small muted' }, v.note), h('td', null, h('a', { href: v.url, target: '_blank', rel: 'noopener noreferrer' }, t('open'), ' ', icon('external', 12)))))))),
        h('p', { class: 'small muted mt-1 mb-0' }, tb('versionsNote'))),
      h('section', { class: 'card mt-3' },
        h('h2', null, tb('bankStats')),
        h('div', { class: 'table-wrap', tabindex: '0', role: 'region', 'aria-label': t('dataTable') }, h('table', { class: 'table' },
          h('thead', null, h('tr', null, h('th', null, t('technology')), DIFFS.map((d) => h('th', { class: 'num' }, t('diff_' + d))), h('th', { class: 'num' }, t('totalWord')))),
          h('tbody', null, byTech.map(([tc, dc, n]) => h('tr', null, h('td', null, tc.name), DIFFS.map((d) => h('td', { class: 'num' }, dc[d] || 0)), h('td', { class: 'num' }, h('strong', null, n)))),
            h('tr', null, h('td', null, h('strong', null, t('totalWord'))), DIFFS.map((d) => h('td', { class: 'num' }, h('strong', null, countBy(QUESTIONS, 'difficulty')[d] || 0))), h('td', { class: 'num' }, h('strong', null, QUESTIONS.length)))))),
        h('div', { class: 'row mt-2' }, TYPES.map((ty) => h('span', { class: 'badge' }, t('type_' + ty) + ': ' + (typeCounts[ty] || 0)))),
        h('div', { class: 'row mt-1' }, MARKETS.map((m) => h('span', { class: 'badge badge--teal' }, t('market_' + m) + ': ' + (marketCounts[m] || 0))))),
      h('div', { class: 'callout callout--warn mt-3' }, h('div', { class: 'callout__title' }, icon('alert', 16), tb('honestyTitle')), h('div', { class: 'small' }, tb('honestyText'))),
      h('div', { class: 'grid grid--3 mt-3' }, group('versions', 'srcVersions'), group('market', 'srcMarket'), group('docs', 'srcDocs')));
    return { title: tb('nav_sources', null, { inline: true }), titleText: 'Versions & Sources', node };
  }

  /* ======================================================================
     Boot
     ====================================================================== */
  function closeMobileNav() {
    const app = $('#app');
    app.classList.remove('is-nav-open');
    const scrim = $('#scrim');
    scrim.classList.remove('is-visible');
    scrim.hidden = true;
    $('#menuBtn').setAttribute('aria-expanded', 'false');
  }
  function openMobileNav() {
    const app = $('#app');
    app.classList.add('is-nav-open');
    const scrim = $('#scrim');
    scrim.hidden = false;
    requestAnimationFrame(() => scrim.classList.add('is-visible'));
    $('#menuBtn').setAttribute('aria-expanded', 'true');
    const first = $('#nav a');
    if (first) first.focus();
  }

  function init() {
    applyPreferences();
    logValidation();

    window.addEventListener('hashchange', () => { closeMobileNav(); render({ focus: true }); });
    $('#menuBtn').addEventListener('click', () => ($('#app').classList.contains('is-nav-open') ? closeMobileNav() : openMobileNav()));
    $('#scrim').addEventListener('click', closeMobileNav);
    $('#collapseBtn').addEventListener('click', () => {
      state.preferences.sidebarCollapsed = !state.preferences.sidebarCollapsed;
      saveState();
      applyPreferences();
    });
    window.addEventListener('resize', debounce(() => {
      $('#app').classList.toggle('is-collapsed', state.preferences.sidebarCollapsed && window.innerWidth > 860);
      if (window.innerWidth > 860) closeMobileNav();
    }, 150));

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && $('#app').classList.contains('is-nav-open')) { closeMobileNav(); $('#menuBtn').focus(); return; }
      if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
      const tg = e.target;
      const tag = tg && tg.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (tg && tg.isContentEditable)) return;
      if ($('#modal').open) return;
      if (e.key === '/' ) {
        e.preventDefault();
        const s = $('#f-q');
        if (s) s.focus(); else go('#/questions?focus=search');
        return;
      }
      // Let focused buttons/links handle Space/Enter natively.
      if ((e.key === ' ' || e.key === 'Enter') && tg && (tag === 'BUTTON' || tag === 'A' || tg.getAttribute('role') === 'button')) return;
      if (ui.keyHandler && ui.keyHandler(e)) e.preventDefault();
    });

    // Keep multiple tabs in sync
    window.addEventListener('storage', (e) => {
      if (e.key !== STORAGE_KEY || e.newValue == null) return;
      try {
        const parsed = JSON.parse(e.newValue);
        const m = migrate(parsed);
        if (!m.incompatible) { state = sanitizeState(m.data); applyPreferences(); rerender(); }
      } catch (err) { /* ignore */ }
    });

    if (storageNotice === 'corrupt') setTimeout(() => toast(tb('storageCorrupt'), 'bad', 7000), 300);
    else if (storageNotice === 'incompatible') setTimeout(() => toast(tb('storageIncompatible'), 'bad', 7000), 300);
    else if (!storageOK) setTimeout(() => toast(tb('storageUnavailable'), 'bad', 7000), 300);

    render({ focus: false });
  }

  // Expose a tiny debug API (read-only helpers) for development and testing.
  window.InterviewPrep = Object.freeze({
    version: APP_VERSION,
    validate: () => validateBank(window.QBANK),
    counts: () => {
      const out = {};
      TECHS.forEach((tc) => { out[tc.id] = Object.assign({ total: BY_TECH.get(tc.id).length }, countBy(BY_TECH.get(tc.id), 'difficulty')); });
      return out;
    },
    getState: () => JSON.parse(JSON.stringify(state)),
    scoreSession: (sess) => summarizeSession(sess),
  });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
