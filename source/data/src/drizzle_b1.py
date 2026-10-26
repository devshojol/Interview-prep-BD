# Drizzle ORM — batch 1 (drizzle-001 … drizzle-008): fundamentals, schema, connection, CRUD, operators,
# type inference, drizzle-kit, SQL injection
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

D_OVERVIEW = ("Drizzle ORM — Overview", "https://orm.drizzle.team/docs/overview")
D_SCHEMA = ("Drizzle ORM — Schema declaration", "https://orm.drizzle.team/docs/sql-schema-declaration")
D_COLUMN_TYPES = ("Drizzle ORM — Column types", "https://orm.drizzle.team/docs/column-types")
D_PG = ("Drizzle ORM — Get started with PostgreSQL", "https://orm.drizzle.team/docs/get-started-postgresql")
D_CONNECT = ("Drizzle ORM — Database connection", "https://orm.drizzle.team/docs/connect-overview")
D_SELECT = ("Drizzle ORM — Select", "https://orm.drizzle.team/docs/select")
D_INSERT = ("Drizzle ORM — Insert", "https://orm.drizzle.team/docs/insert")
D_UPDATE = ("Drizzle ORM — Update", "https://orm.drizzle.team/docs/update")
D_OPERATORS = ("Drizzle ORM — Filter operators", "https://orm.drizzle.team/docs/operators")
D_GOODIES = ("Drizzle ORM — Goodies (type inference)", "https://orm.drizzle.team/docs/goodies")
D_KIT_OVERVIEW = ("Drizzle Kit — Overview", "https://orm.drizzle.team/docs/kit-overview")
D_KIT_GENERATE = ("Drizzle Kit — generate", "https://orm.drizzle.team/docs/drizzle-kit-generate")
D_SQL = ("Drizzle ORM — sql template", "https://orm.drizzle.team/docs/sql")
OWASP_SQLI = ("OWASP — SQL Injection Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ drizzle-001
    Q(
        id="drizzle-001", sub="Drizzle Fundamentals", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["drizzle", "orm", "type-safety", "typescript"],
        ver="Drizzle ORM 0.45.x (stable); v1.0 is a release candidate", vs=False, status="stable",
        q_en=r"""What is Drizzle ORM, and how is it different from traditional ORMs like TypeORM or Sequelize?""",
        q_bn=r"""Drizzle ORM কী, আর TypeORM বা Sequelize-এর মতো traditional ORM থেকে এটা কীভাবে আলাদা?""",
        a_en=r"""
            Drizzle is a TypeScript ORM for SQL databases (PostgreSQL, MySQL, SQLite and others). You define tables in TypeScript, and the query API mirrors SQL — `db.select().from(users).where(eq(users.id, 1))` reads almost like the SQL it generates.

            Key differences from traditional ORMs:
            - **TypeScript-first, no code generation:** types are inferred directly from the schema, so there's no separate "generate the client" step for types.
            - **SQL-like and explicit:** no entity manager, change tracking or lazy loading. Each call is one predictable query.
            - **Two query styles:** the SQL-like builder (selects, joins, upserts) and a relational API (`db.query.users.findMany({ with: { posts: true } })`) for nested results.
            - **Thin and driver-based:** it sits on top of drivers like `node-postgres`, `postgres.js` or Neon's serverless driver, which makes it light enough for serverless.

            Migrations are handled by the companion CLI, Drizzle Kit. The stable line is 0.45.x; v1.0 is still a release candidate.
        """,
        a_bn=r"""
            Drizzle হলো SQL database-এর (PostgreSQL, MySQL, SQLite ইত্যাদি) জন্য একটা TypeScript ORM। Table TypeScript-এ define করা হয়, আর query API SQL-এর মতোই — `db.select().from(users).where(eq(users.id, 1))` পড়তে প্রায় তার তৈরি করা SQL-এর মতো।

            Traditional ORM থেকে মূল পার্থক্য:
            - **TypeScript-first, code generation নেই:** type সরাসরি schema থেকে infer হয়, তাই type-এর জন্য আলাদা "client generate করো" step লাগে না।
            - **SQL-এর মতো আর explicit:** entity manager, change tracking বা lazy loading নেই। প্রতিটা call একটা predictable query।
            - **দুই ধরনের query:** SQL-এর মতো builder (select, join, upsert) আর nested result-এর জন্য relational API (`db.query.users.findMany({ with: { posts: true } })`)।
            - **হালকা আর driver-based:** `node-postgres`, `postgres.js` বা Neon-এর serverless driver-এর উপর বসে, তাই serverless-এর জন্যও যথেষ্ট হালকা।

            Migration সামলায় সঙ্গী CLI, Drizzle Kit। Stable line হলো 0.45.x; v1.0 এখনো release candidate।
        """,
        quick_en=r"""Drizzle is a TypeScript ORM for SQL databases: you define tables in TypeScript and the query API reads like SQL. Unlike TypeORM or Sequelize it infers types without code generation and has no entity manager, change tracking or lazy loading; 0.45.x is the stable line and v1.0 is still a release candidate.""",
        quick_bn=r"""Drizzle হলো SQL database-এর জন্য একটা TypeScript ORM: table define করা হয় TypeScript-এ, আর query API দেখতে প্রায় SQL-এর মতো। TypeORM বা Sequelize-এর মতো entity manager, change tracking বা lazy loading নেই, আর code generation ছাড়াই type infer হয়; stable line হলো 0.45.x, v1.0 এখনো release candidate।""",
        ex_en=r"""
            - **"If you know SQL, you know Drizzle"** is the design goal. The flip side: you need to understand joins, indexes and transactions yourself — Drizzle won't hide the database.
            - **No magic loading:** traditional ORMs can trigger hidden N+1 queries through lazy relations. With Drizzle you choose: a join, a relational query (compiled into one SQL statement), or separate queries.
            - **Escape hatch:** the `sql` template tag lets you write any SQL fragment with safe parameter binding when the builder doesn't cover something.
            - **Ecosystem:** Drizzle Kit (`generate`, `migrate`, `push`, `pull`, `studio`, `check`), and validator integrations such as `drizzle-zod` (in v1 RC these move into `drizzle-orm/zod`).
            - It's a library that builds SQL, not a database or a server; connection pooling and performance still depend on the driver and PostgreSQL.
        """,
        ex_bn=r"""
            - **"SQL জানলে Drizzle জানো"** — এটাই design-এর লক্ষ্য। উল্টো দিক হলো: join, index আর transaction নিজেকেই বুঝতে হবে — Drizzle database লুকিয়ে রাখে না।
            - **Magic loading নেই:** traditional ORM lazy relation-এর মাধ্যমে লুকানো N+1 query চালিয়ে দিতে পারে। Drizzle-এ তুমি বেছে নাও: join, relational query (একটা SQL statement-এ compile হয়), নাকি আলাদা query।
            - **Escape hatch:** builder কোনো কিছু cover না করলে `sql` template tag দিয়ে নিরাপদ parameter binding সহ যেকোনো SQL fragment লেখা যায়।
            - **Ecosystem:** Drizzle Kit (`generate`, `migrate`, `push`, `pull`, `studio`, `check`), আর `drizzle-zod`-এর মতো validator integration (v1 RC-তে এগুলো `drizzle-orm/zod`-এ চলে যাচ্ছে)।
            - এটা SQL তৈরি করা একটা library, database বা server না; connection pooling আর performance এখনো driver আর PostgreSQL-এর উপর নির্ভর করে।
        """,
        tip_en=r"""Contrast "explicit, SQL-like, inferred types" with "entity-based, implicit loading". Mentioning that the stable line is 0.45 and v1 is an RC shows you track versions accurately.""",
        tip_bn=r""""Explicit, SQL-এর মতো, inferred type" বনাম "entity-based, implicit loading" — এভাবে তুলনা করো। Stable line 0.45 আর v1 এখনো RC — এটা বললে বোঝা যায় তুমি version ঠিকঠাক খেয়াল রাখো।""",
        mist_en=r"""Calling Drizzle a "query builder only" (it also has a relational API and migrations tooling); claiming it needs a code-generation step like Prisma; saying v1.0 is already stable.""",
        mist_bn=r"""Drizzle-কে "শুধু query builder" বলা (এর relational API আর migration tooling-ও আছে); দাবি করা যে Prisma-র মতো code-generation step লাগে; বলা যে v1.0 আগেই stable।""",
        code=r"""
            import { drizzle } from 'drizzle-orm/node-postgres';
            import { eq } from 'drizzle-orm';
            import { integer, pgTable, text } from 'drizzle-orm/pg-core';

            export const users = pgTable('users', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              name: text().notNull(),
            });

            const db = drizzle(process.env.DATABASE_URL!);

            // SQL: select "id", "name" from "users" where "users"."id" = $1
            const rows = await db.select().from(users).where(eq(users.id, 1));
            //    ^? { id: number; name: string }[]  — inferred, no codegen
        """,
        lang="typescript",
        follow=[
            ("When would you still prefer a traditional ORM over Drizzle?", "কখন Drizzle-এর বদলে traditional ORM পছন্দ করবে?"),
            ("What are the two query APIs in Drizzle and when do you use each?", "Drizzle-এর দুটো query API কী, আর কখন কোনটা ব্যবহার করো?"),
        ],
        related=["drizzle-011", "drizzle-020"],
        refs=[D_OVERVIEW],
    ),
    # ------------------------------------------------------------------ drizzle-002
    Q(
        id="drizzle-002", sub="Schema Definitions", diff="easy", type="coding",
        prio="high", market="both", mins=5,
        tags=["schema", "pgtable", "identity", "pgenum", "timestamps"],
        ver="Drizzle ORM 0.45.x / drizzle-kit 0.31", vs=True, status="stable",
        q_en=r"""
            Define a PostgreSQL `users` table with Drizzle:

            - `id` — integer primary key, generated as an identity column
            - `email` — `varchar(255)`, required, unique
            - `name` — required text; `bio` — optional text
            - `role` — enum `user` / `admin`, default `user`
            - `created_at` — `timestamptz`, required, defaults to now

            Also export the TypeScript types for a selected row and for an insert.
        """,
        q_bn=r"""
            Drizzle দিয়ে একটা PostgreSQL `users` table define করো:

            - `id` — integer primary key, identity column হিসেবে generate হবে
            - `email` — `varchar(255)`, required, unique
            - `name` — required text; `bio` — optional text
            - `role` — enum `user` / `admin`, default `user`
            - `created_at` — `timestamptz`, required, default now

            সাথে select করা row আর insert-এর জন্য TypeScript type export করো।
        """,
        a_en=r"""
            - Tables come from `pgTable(name, columns)` in `drizzle-orm/pg-core`; each column is a builder (`integer()`, `varchar({ length })`, `text()`, `timestamp()`), chained with modifiers like `.notNull()`, `.unique()`, `.default()`, `.defaultNow()`.
            - `integer().primaryKey().generatedAlwaysAsIdentity()` creates a SQL-standard identity column — the modern replacement for `serial`.
            - `pgEnum('role', ['user', 'admin'])` defines a PostgreSQL enum type; the column uses `roleEnum()`.
            - The TypeScript key becomes the column name unless you pass one, so `timestamp('created_at', { withTimezone: true })` maps `createdAt` to `created_at`.
            - `typeof users.$inferSelect` and `typeof users.$inferInsert` give the row and insert types with no code generation.

            The expected output shows the SQL that `drizzle-kit generate` produces for this schema.
        """,
        a_bn=r"""
            - Table আসে `drizzle-orm/pg-core`-এর `pgTable(name, columns)` থেকে; প্রতিটা column একটা builder (`integer()`, `varchar({ length })`, `text()`, `timestamp()`), যার সাথে `.notNull()`, `.unique()`, `.default()`, `.defaultNow()`-এর মতো modifier chain করা যায়।
            - `integer().primaryKey().generatedAlwaysAsIdentity()` একটা SQL-standard identity column বানায় — `serial`-এর আধুনিক বিকল্প।
            - `pgEnum('role', ['user', 'admin'])` একটা PostgreSQL enum type define করে; column-এ ব্যবহার হয় `roleEnum()`।
            - আলাদা নাম না দিলে TypeScript key-টাই column-এর নাম হয়, তাই `timestamp('created_at', { withTimezone: true })` দিয়ে `createdAt`-কে `created_at`-এ map করা হয়েছে।
            - `typeof users.$inferSelect` আর `typeof users.$inferInsert` কোনো code generation ছাড়াই row আর insert-এর type দেয়।

            Expected output-এ দেখানো আছে এই schema থেকে `drizzle-kit generate` কোন SQL তৈরি করে।
        """,
        quick_en=r"""Use `pgTable('users', {...})` with `integer().primaryKey().generatedAlwaysAsIdentity()`, `varchar({ length: 255 }).notNull().unique()`, a `pgEnum` column with `.default('user')` and `timestamp('created_at', { withTimezone: true }).notNull().defaultNow()`. Types come from `$inferSelect` and `$inferInsert`.""",
        quick_bn=r"""`pgTable('users', {...})`-এ `integer().primaryKey().generatedAlwaysAsIdentity()`, `varchar({ length: 255 }).notNull().unique()`, `.default('user')`-সহ একটা `pgEnum` column আর `timestamp('created_at', { withTimezone: true }).notNull().defaultNow()` লিখি। Type আসে `$inferSelect` আর `$inferInsert` থেকে।""",
        ex_en=r"""
            - **Identity vs serial:** identity columns are the SQL standard and PostgreSQL's recommendation. `generatedAlwaysAsIdentity()` rejects manual ids (and Drizzle removes `id` from the insert type); `generatedByDefaultAsIdentity()` allows overriding, which is handy for data imports.
            - **Always use `timestamptz`** (`withTimezone: true`) for points in time — it stores an absolute instant, so servers in Dhaka and Frankfurt agree. Plain `timestamp` silently drops the offset.
            - **Naming:** instead of naming every column, you can set `casing: 'snake_case'` on both `drizzle()` and the Drizzle Kit config so `createdAt` maps to `created_at` automatically.
            - **Enums:** adding a value later is easy; removing or renaming one is a real migration. For frequently changing lists, a lookup table or a text column with a `CHECK` constraint can be simpler.
            - Older tutorials always pass the column name first (`integer('id')`); in current versions it's optional and the object key is used.
        """,
        ex_bn=r"""
            - **Identity বনাম serial:** identity column SQL standard আর PostgreSQL-এর সুপারিশ। `generatedAlwaysAsIdentity()` হাতে দেওয়া id reject করে (আর Drizzle insert type থেকে `id` বাদ দেয়); `generatedByDefaultAsIdentity()` override করতে দেয়, data import-এর সময় কাজে লাগে।
            - **সময়ের মুহূর্তের জন্য সবসময় `timestamptz`** (`withTimezone: true`) — এটা absolute instant রাখে, তাই ঢাকা আর Frankfurt-এর server একমত থাকে। Plain `timestamp` চুপচাপ offset বাদ দেয়।
            - **Naming:** প্রতিটা column-এর নাম না দিয়ে `drizzle()` আর Drizzle Kit config দুটোতেই `casing: 'snake_case'` দিলে `createdAt` নিজে থেকেই `created_at`-এ map হয়।
            - **Enum:** পরে value যোগ করা সহজ; কিন্তু সরানো বা নাম বদলানো আসল migration। ঘনঘন বদলায় এমন list-এর জন্য lookup table বা `CHECK` constraint সহ text column সহজ হতে পারে।
            - পুরোনো tutorial-এ সবসময় প্রথমে column-এর নাম দেওয়া থাকে (`integer('id')`); এখনকার version-এ এটা optional, object key-টাই নাম হিসেবে ব্যবহার হয়।
        """,
        tip_en=r"""Mention identity over serial and `timestamptz` over `timestamp` without being asked — these two choices quickly signal PostgreSQL maturity.""",
        tip_bn=r"""জিজ্ঞেস না করলেও serial-এর বদলে identity আর `timestamp`-এর বদলে `timestamptz`-এর কথা বলো — এই দুটো সিদ্ধান্ত দ্রুত PostgreSQL-এ তোমার পরিপক্বতা বোঝায়।""",
        mist_en=r"""Using `serial` in new schemas; using `timestamp` without time zone for events; forgetting `.notNull()` (columns are nullable by default); defining the enum but not exporting it, so Drizzle Kit doesn't create the type.""",
        mist_bn=r"""নতুন schema-য় `serial` ব্যবহার করা; event-এর জন্য time zone ছাড়া `timestamp`; `.notNull()` ভুলে যাওয়া (default-এ column nullable); enum define করে export না করা, ফলে Drizzle Kit type-টা তৈরি করে না।""",
        code=r"""
            // src/db/schema.ts
            import { integer, pgEnum, pgTable, text, timestamp, varchar } from 'drizzle-orm/pg-core';

            export const roleEnum = pgEnum('role', ['user', 'admin']);

            export const users = pgTable('users', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              email: varchar({ length: 255 }).notNull().unique(),
              name: text().notNull(),
              bio: text(),
              role: roleEnum().notNull().default('user'),
              createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
            });

            export type User = typeof users.$inferSelect;    // row returned by select
            export type NewUser = typeof users.$inferInsert; // object accepted by insert
        """,
        lang="typescript",
        output=r"""
            -- generated by `drizzle-kit generate`
            CREATE TYPE "public"."role" AS ENUM('user', 'admin');--> statement-breakpoint
            CREATE TABLE "users" (
              "id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "users_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
              "email" varchar(255) NOT NULL,
              "name" text NOT NULL,
              "bio" text,
              "role" "role" DEFAULT 'user' NOT NULL,
              "created_at" timestamp with time zone DEFAULT now() NOT NULL,
              CONSTRAINT "users_email_unique" UNIQUE("email")
            );
        """,
        time="Not applicable (schema definition)",
        space="Not applicable",
        follow=[
            ("When would you use `generatedByDefaultAsIdentity()` instead?", "কখন এর বদলে `generatedByDefaultAsIdentity()` ব্যবহার করবে?"),
            ("How would you add a composite index on (role, created_at)?", "(role, created_at)-এর উপর composite index কীভাবে যোগ করবে?"),
        ],
        related=["drizzle-006", "drizzle-012"],
        refs=[D_SCHEMA, D_COLUMN_TYPES],
    ),
    # ------------------------------------------------------------------ drizzle-003
    Q(
        id="drizzle-003", sub="PostgreSQL Integration", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["node-postgres", "postgres-js", "connection", "pool", "drivers"],
        ver="Drizzle ORM 0.45.x / pg 8 / postgres.js 3", vs=True, status="stable",
        q_en=r"""How do you connect Drizzle to PostgreSQL in a Node.js app? Which drivers can you use, and where should the `db` instance be created?""",
        q_bn=r"""একটা Node.js app-এ Drizzle-কে PostgreSQL-এর সাথে কীভাবে connect করো? কোন কোন driver ব্যবহার করা যায়, আর `db` instance কোথায় তৈরি করা উচিত?""",
        a_en=r"""
            Drizzle doesn't open connections itself — it wraps a PostgreSQL driver:

            - **node-postgres (`pg`)** via `drizzle-orm/node-postgres`. Shortest form: `drizzle(process.env.DATABASE_URL!)`, which creates a pool for you. For control over pool size and timeouts, create a `Pool` and pass it: `drizzle({ client: pool, schema })`.
            - **postgres.js** via `drizzle-orm/postgres-js`: `drizzle({ client: postgres(url, { max: 10 }) })`.
            - **Serverless drivers** (e.g. Neon's HTTP driver via `drizzle-orm/neon-http`) for edge/serverless runtimes.

            I create the `db` **once per process** in a module (or a NestJS provider) and reuse it everywhere — never per request. Passing `schema` (tables + relations) is required if I want the relational API `db.query.*`. On shutdown I close the pool (`pool.end()`).
        """,
        a_bn=r"""
            Drizzle নিজে connection খোলে না — এটা একটা PostgreSQL driver-কে wrap করে:

            - **node-postgres (`pg`)**, `drizzle-orm/node-postgres` দিয়ে। সবচেয়ে ছোট রূপ: `drizzle(process.env.DATABASE_URL!)`, এটা নিজেই একটা pool বানায়। Pool size আর timeout নিয়ন্ত্রণ করতে নিজে একটা `Pool` বানিয়ে pass করো: `drizzle({ client: pool, schema })`।
            - **postgres.js**, `drizzle-orm/postgres-js` দিয়ে: `drizzle({ client: postgres(url, { max: 10 }) })`।
            - **Serverless driver** (যেমন `drizzle-orm/neon-http` দিয়ে Neon-এর HTTP driver) edge/serverless runtime-এর জন্য।

            আমি `db` একটা module-এ (বা NestJS provider-এ) **প্রতি process-এ একবার** তৈরি করি আর সব জায়গায় reuse করি — কখনো per request না। Relational API `db.query.*` চাইলে `schema` (table + relation) pass করা বাধ্যতামূলক। Shutdown-এর সময় pool বন্ধ করি (`pool.end()`)।
        """,
        quick_en=r"""Drizzle wraps a driver: node-postgres (`drizzle-orm/node-postgres`, optionally with your own `Pool`), postgres.js, or a serverless driver such as Neon HTTP. Create `db` once per process and reuse it, pass `schema` if you want `db.query`, and close the pool on shutdown.""",
        quick_bn=r"""Drizzle নিজে connection খোলে না, একটা driver-কে wrap করে: node-postgres (`drizzle-orm/node-postgres`, চাইলে নিজের `Pool` দিয়ে), postgres.js, বা Neon HTTP-র মতো serverless driver। `db` প্রতি process-এ একবার তৈরি করে সব জায়গায় reuse করি, `db.query` চাইলে `schema` pass করি, আর shutdown-এ pool বন্ধ করি।""",
        ex_en=r"""
            - **Why a single instance:** each `Pool` holds up to `max` connections. Creating one per request (or per hot-reload in dev) quickly hits PostgreSQL's `max_connections`.
            - **Choosing a driver:** `pg` is the most widely used and battle-tested; postgres.js is fast and has tagged-template ergonomics; both work well. Pick one and stay consistent.
            - **`schema` gotcha:** without `schema`, `db.query.users` is `undefined` at runtime (and a type error) — a very common "why doesn't findMany exist?" question.
            - **Pool errors:** node-postgres emits `error` on the pool if an idle connection dies (DB restart/failover). Attach `pool.on('error', ...)` so it's logged rather than crashing the process.
            - **Config:** keep the URL in env vars; enable TLS (`sslmode=require` or the driver's `ssl` option) for managed databases.
        """,
        ex_bn=r"""
            - **কেন একটাই instance:** প্রতিটা `Pool` সর্বোচ্চ `max`টা connection রাখে। প্রতি request-এ (বা dev-এ প্রতিটা hot-reload-এ) একটা করে বানালে খুব দ্রুত PostgreSQL-এর `max_connections` ছুঁয়ে ফেলে।
            - **Driver বাছাই:** `pg` সবচেয়ে বেশি ব্যবহৃত আর পরীক্ষিত; postgres.js দ্রুত আর tagged-template-এ সুবিধাজনক; দুটোই ভালো চলে। একটা বেছে consistent থাকো।
            - **`schema`-র ফাঁদ:** `schema` না দিলে runtime-এ `db.query.users` হয় `undefined` (আর type error) — "findMany কেন নেই?" খুব common প্রশ্ন।
            - **Pool error:** idle connection মারা গেলে (DB restart/failover) node-postgres pool-এ `error` emit করে। `pool.on('error', ...)` লাগাও, যাতে process crash না করে log হয়।
            - **Config:** URL env var-এ রাখো; managed database-এর জন্য TLS চালু করো (`sslmode=require` বা driver-এর `ssl` option)।
        """,
        tip_en=r"""Say "one pool per process, created at startup, closed on shutdown" — it covers correctness, performance and operations in one sentence.""",
        tip_bn=r""""প্রতি process-এ একটা pool, startup-এ তৈরি, shutdown-এ বন্ধ" — এক বাক্যেই correctness, performance আর operations কভার হয়।""",
        mist_en=r"""Creating a new client or pool inside request handlers; forgetting to pass `schema` and then using `db.query`; never closing the pool, which keeps tests and scripts hanging.""",
        mist_bn=r"""Request handler-এর ভেতরে নতুন client বা pool তৈরি করা; `schema` pass না করে `db.query` ব্যবহার করা; pool কখনো বন্ধ না করা, ফলে test আর script আটকে থাকে।""",
        code=r"""
            // src/db/index.ts — node-postgres with an explicit pool
            import { drizzle } from 'drizzle-orm/node-postgres';
            import { Pool } from 'pg';
            import * as schema from './schema';

            export const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 10 });
            pool.on('error', (err) => console.error('Idle PostgreSQL client error', err));

            export const db = drizzle({ client: pool, schema }); // schema enables db.query.*

            // Shortest form — Drizzle creates the pool:
            // export const db = drizzle(process.env.DATABASE_URL!);

            // postgres.js alternative:
            // import postgres from 'postgres';
            // import { drizzle } from 'drizzle-orm/postgres-js';
            // export const db = drizzle({ client: postgres(process.env.DATABASE_URL!, { max: 10 }), schema });
        """,
        lang="typescript",
        follow=[
            ("How would you size the pool when running 6 instances of the app?", "App-এর ৬টা instance চললে pool size কীভাবে ঠিক করবে?"),
            ("What changes in a serverless environment?", "Serverless environment-এ কী বদলায়?"),
        ],
        related=["drizzle-023", "nest-022"],
        refs=[D_PG, D_CONNECT],
    ),
    # ------------------------------------------------------------------ drizzle-004
    Q(
        id="drizzle-004", sub="CRUD Queries", diff="easy", type="coding",
        prio="high", market="both", mins=6,
        tags=["select", "insert", "update", "delete", "returning"],
        ver="Drizzle ORM 0.45.x", vs=False, status="stable",
        q_en=r"""
            Using the `users` table (`id`, `email`, `name`, `bio`, `role`, `createdAt`), write Drizzle queries to:

            1. fetch the user with id 1;
            2. list admins whose email ends with `@example.com`, returning only `id` and `email`;
            3. insert a user and get the created row back;
            4. rename user 1 and return `id` and `name`;
            5. delete user 2 and return its id;
            6. count all users.
        """,
        q_bn=r"""
            `users` table (`id`, `email`, `name`, `bio`, `role`, `createdAt`) ব্যবহার করে Drizzle query লেখো:

            1. id 1-এর user আনো;
            2. যেসব admin-এর email `@example.com` দিয়ে শেষ, তাদের list — শুধু `id` আর `email` return করবে;
            3. একটা user insert করে তৈরি হওয়া row ফেরত নাও;
            4. user 1-এর নাম বদলাও আর `id` ও `name` return করো;
            5. user 2 delete করে তার id return করো;
            6. মোট user count করো।
        """,
        a_en=r"""
            - **Select:** `db.select().from(users).where(eq(users.id, 1))` returns an **array** — destructure `const [user] = ...` for a single row. Pass an object to `select({...})` for a partial selection; the result type follows it.
            - **Filters** come from `drizzle-orm`: `eq`, `and`, `or`, `ilike`, `inArray`, `gt`, `isNull` and more.
            - **Insert:** `db.insert(users).values({...}).returning()` — `returning()` gives back the inserted row(s) including defaults like `id` and `createdAt`. `values([...])` inserts many rows in one statement.
            - **Update:** `db.update(users).set({ name }).where(...)` — always with a `where`.
            - **Delete:** `db.delete(users).where(...)`, optionally `.returning({ id: users.id })`.
            - **Count:** `db.$count(users)` or `db.select({ total: count() }).from(users)`.

            Every builder must be awaited — nothing runs until then.
        """,
        a_bn=r"""
            - **Select:** `db.select().from(users).where(eq(users.id, 1))` একটা **array** return করে — একটা row-এর জন্য `const [user] = ...` দিয়ে destructure করো। Partial selection-এর জন্য `select({...})`-এ object দাও; result type সেটাই অনুসরণ করে।
            - **Filter** আসে `drizzle-orm` থেকে: `eq`, `and`, `or`, `ilike`, `inArray`, `gt`, `isNull` ইত্যাদি।
            - **Insert:** `db.insert(users).values({...}).returning()` — `returning()` insert হওয়া row ফেরত দেয়, `id` আর `createdAt`-এর মতো default সহ। `values([...])` এক statement-এ অনেক row insert করে।
            - **Update:** `db.update(users).set({ name }).where(...)` — সবসময় `where` সহ।
            - **Delete:** `db.delete(users).where(...)`, চাইলে `.returning({ id: users.id })`।
            - **Count:** `db.$count(users)` বা `db.select({ total: count() }).from(users)`।

            প্রতিটা builder await করতে হবে — তার আগে কিছুই চলে না।
        """,
        quick_en=r"""`db.select().from(users).where(eq(users.id, 1))` returns an array; combine `and()` and `ilike()` with a partial `select({ id, email })`; use `insert().values().returning()`, `update().set().where()`, `delete().where().returning()` and `db.$count(users)`. Every builder runs only when awaited.""",
        quick_bn=r"""`db.select().from(users).where(eq(users.id, 1))` একটা array দেয়; partial `select({ id, email })`-এর সাথে `and()` আর `ilike()` ব্যবহার করি; তারপর `insert().values().returning()`, `update().set().where()`, `delete().where().returning()` আর `db.$count(users)`। প্রতিটা builder শুধু `await` করলেই চলে।""",
        ex_en=r"""
            - **`returning()` is PostgreSQL-friendly:** it avoids a second round trip to read generated values. (MySQL doesn't support it; Drizzle offers `$returningId()` there.)
            - **Update/delete without `where`** affect every row. The official `eslint-plugin-drizzle` has `enforce-update-with-where` and `enforce-delete-with-where` rules to catch this in CI.
            - **Values are parameterised** (`$1`, `$2`), so user input in `eq()`/`ilike()` is safe from SQL injection.
            - **`count()` mapping:** PostgreSQL returns `count(*)` as `bigint`; Drizzle's `count()` maps it to a JS number for you, while a hand-written `count(*)` inside the `sql` tag needs `.mapWith(Number)`.
            - For "find or 404" in an API, check `if (!user)` after destructuring and throw your framework's NotFound error.
        """,
        ex_bn=r"""
            - **`returning()` PostgreSQL-এ খুব কাজের:** generated value পড়তে দ্বিতীয় round trip লাগে না। (MySQL এটা support করে না; সেখানে Drizzle `$returningId()` দেয়।)
            - **`where` ছাড়া update/delete** সব row-কে প্রভাবিত করে। Official `eslint-plugin-drizzle`-এর `enforce-update-with-where` আর `enforce-delete-with-where` rule CI-তে এটা ধরে।
            - **Value parameterised হয়** (`$1`, `$2`), তাই `eq()`/`ilike()`-এ user input SQL injection থেকে নিরাপদ।
            - **`count()` mapping:** PostgreSQL `count(*)`-কে `bigint` হিসেবে দেয়; Drizzle-এর `count()` তোমার জন্য JS number-এ map করে, কিন্তু `sql` tag-এর ভেতরে নিজে লেখা `count(*)`-এর জন্য `.mapWith(Number)` লাগে।
            - API-তে "খুঁজে না পেলে 404"-এর জন্য destructure করার পর `if (!user)` check করো আর framework-এর NotFound error throw করো।
        """,
        tip_en=r"""Write the queries and say the SQL out loud for one of them ("this becomes `UPDATE users SET name = $1 WHERE id = $2 RETURNING ...`"). It shows you understand what Drizzle sends to the database.""",
        tip_bn=r"""Query লেখো আর একটার জন্য SQL-টা মুখে বলো ("এটা হবে `UPDATE users SET name = $1 WHERE id = $2 RETURNING ...`")। এতে বোঝা যায় Drizzle database-এ কী পাঠায় তুমি বোঝো।""",
        mist_en=r"""Expecting `select()` to return a single object; forgetting `await`; update/delete without `where`; using `like` for case-insensitive search in PostgreSQL.""",
        mist_bn=r"""ভাবা যে `select()` একটা object return করবে; `await` ভুলে যাওয়া; `where` ছাড়া update/delete; PostgreSQL-এ case-insensitive search-এর জন্য `like` ব্যবহার করা।""",
        code=r"""
            import { and, count, eq, ilike } from 'drizzle-orm';
            import { db } from './db';
            import { users } from './db/schema';

            // 1) by id — select returns an array
            const [user] = await db.select().from(users).where(eq(users.id, 1));

            // 2) partial select with combined filters
            const admins = await db
              .select({ id: users.id, email: users.email })
              .from(users)
              .where(and(eq(users.role, 'admin'), ilike(users.email, '%@example.com')));

            // 3) insert and return the created row
            const [created] = await db
              .insert(users)
              .values({ email: 'rahim@example.com', name: 'Rahim' })
              .returning();

            // 4) update
            const renamed = await db
              .update(users)
              .set({ name: 'Rahim Uddin' })
              .where(eq(users.id, 1))
              .returning({ id: users.id, name: users.name });

            // 5) delete
            const deleted = await db.delete(users).where(eq(users.id, 2)).returning({ id: users.id });

            // 6) count
            const total = await db.$count(users);
            // or: const [{ total }] = await db.select({ total: count() }).from(users);
        """,
        lang="typescript",
        output=r"""
            -- before: users 1 (karim@example.com), 2 (sumi@example.com), 3 (nadia@example.com, admin)
            user     -> { id: 1, email: 'karim@example.com', name: 'Karim', bio: null, role: 'user', createdAt: 2026-10-12T... }
            admins   -> [ { id: 3, email: 'nadia@example.com' } ]
            created  -> { id: 4, email: 'rahim@example.com', name: 'Rahim', bio: null, role: 'user', createdAt: 2026-10-12T... }
            renamed  -> [ { id: 1, name: 'Rahim Uddin' } ]
            deleted  -> [ { id: 2 } ]
            total    -> 3
        """,
        time="O(log n) per indexed lookup; the email filter scans unless indexed for it",
        space="O(k) for k returned rows",
        follow=[
            ("How would you insert 10,000 rows efficiently?", "১০,০০০ row কীভাবে efficient ভাবে insert করবে?"),
            ("How do you make the email search use an index?", "Email search কীভাবে index ব্যবহার করবে?"),
        ],
        related=["drizzle-005", "drizzle-009", "drizzle-022"],
        refs=[D_SELECT, D_INSERT, D_UPDATE],
    ),
    # ------------------------------------------------------------------ drizzle-005
    Q(
        id="drizzle-005", sub="Type-safe Queries & Filters", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=1,
        tags=["operators", "ilike", "like", "filters"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""You need all users whose email ends with `@gmail.com`, regardless of letter case (`@Gmail.com` must match too), in PostgreSQL. Which Drizzle filter is correct?""",
        q_bn=r"""PostgreSQL-এ এমন সব user দরকার যাদের email `@gmail.com` দিয়ে শেষ, letter case যাই হোক (`@Gmail.com`-ও match করতে হবে)। কোন Drizzle filter সঠিক?""",
        options=[
            ("`like(users.email, '%@gmail.com')`", "`like(users.email, '%@gmail.com')`"),
            ("`eq(users.email, '%@gmail.com')`", "`eq(users.email, '%@gmail.com')`"),
            ("`ilike(users.email, '%@gmail.com')`", "`ilike(users.email, '%@gmail.com')`"),
            ("`users.email.ilike('%@gmail.com')`", "`users.email.ilike('%@gmail.com')`"),
        ],
        correct=2,
        a_en=r"""`ilike(users.email, '%@gmail.com')`. It compiles to `"users"."email" ilike $1` — PostgreSQL's case-insensitive `LIKE` — with the pattern sent as a bound parameter.""",
        a_bn=r"""`ilike(users.email, '%@gmail.com')`। এটা compile হয় `"users"."email" ilike $1`-এ — PostgreSQL-এর case-insensitive `LIKE` — আর pattern-টা bound parameter হিসেবে যায়।""",
        quick_en=r"""`ilike(users.email, '%@gmail.com')`: it compiles to PostgreSQL's case-insensitive `ILIKE` with the pattern sent as a bound parameter, while `like` is case-sensitive and `eq` does no pattern matching.""",
        quick_bn=r"""`ilike(users.email, '%@gmail.com')`: এটা PostgreSQL-এর case-insensitive `ILIKE`-এ compile হয় আর pattern যায় bound parameter হিসেবে; `like` case-sensitive, আর `eq` কোনো pattern matching-ই করে না।""",
        ex_en=r"""
            - `like` is the tempting option, but in PostgreSQL `LIKE` is **case-sensitive**, so `@Gmail.com` wouldn't match.
            - `eq` compares literally — `%` is not a wildcard there.
            - Drizzle filters are standalone functions imported from `drizzle-orm` (`eq`, `ilike`, `and`...), not methods on columns, so option D doesn't exist.

            Performance note: a pattern starting with `%` can't use a normal B-tree index. For frequent suffix/contains searches, consider a `pg_trgm` GIN index, or store a normalised lower-case email with an index on it.
        """,
        ex_bn=r"""
            - `like` লোভনীয় option, কিন্তু PostgreSQL-এ `LIKE` **case-sensitive**, তাই `@Gmail.com` match করত না।
            - `eq` হুবহু তুলনা করে — সেখানে `%` wildcard না।
            - Drizzle filter হলো `drizzle-orm` থেকে import করা আলাদা function (`eq`, `ilike`, `and`...), column-এর method না, তাই option D-র অস্তিত্বই নেই।

            Performance নোট: `%` দিয়ে শুরু হওয়া pattern সাধারণ B-tree index ব্যবহার করতে পারে না। ঘনঘন suffix/contains search হলে `pg_trgm` GIN index ভাবো, অথবা normalised lower-case email রেখে তার উপর index দাও।
        """,
        tip_en=r"""Mention that `ilike` is PostgreSQL-specific and that leading wildcards defeat B-tree indexes — a small performance remark lifts an easy answer.""",
        tip_bn=r"""বলো যে `ilike` PostgreSQL-specific, আর শুরুতে wildcard থাকলে B-tree index কাজে লাগে না — ছোট একটা performance মন্তব্য সহজ উত্তরকেও উঁচু করে।""",
        related=["drizzle-004", "drizzle-028"],
        refs=[D_OPERATORS],
    ),
    # ------------------------------------------------------------------ drizzle-006
    Q(
        id="drizzle-006", sub="Type Inference", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["type-inference", "inferinsert", "inferselect", "typescript"],
        ver="Drizzle ORM 0.45.x", vs=False, status="stable",
        q_en=r"""Given this table, which fields are **required** in `typeof users.$inferInsert`?""",
        q_bn=r"""এই table অনুযায়ী `typeof users.$inferInsert`-এ কোন field গুলো **required**?""",
        code=r"""
            export const users = pgTable('users', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              name: text().notNull(),
              bio: text(),
              createdAt: timestamp().defaultNow(),
            });

            type NewUser = typeof users.$inferInsert;
        """,
        lang="typescript",
        options=[
            ("All four: `id`, `name`, `bio`, `createdAt`", "চারটাই: `id`, `name`, `bio`, `createdAt`"),
            ("Only `name`", "শুধু `name`"),
            ("`name` and `createdAt`", "`name` আর `createdAt`"),
            ("`name` and `bio`", "`name` আর `bio`"),
        ],
        correct=1,
        a_en=r"""Only `name`. The insert type is `{ name: string; bio?: string | null; createdAt?: Date | null }`: nullable columns and columns with defaults become optional, and an *always*-generated identity `id` is left out entirely.""",
        a_bn=r"""শুধু `name`। Insert type হলো `{ name: string; bio?: string | null; createdAt?: Date | null }`: nullable column আর default থাকা column optional হয়ে যায়, আর *always*-generated identity `id` পুরোপুরি বাদ পড়ে।""",
        quick_en=r"""Only `name`. In `$inferInsert`, nullable columns and columns with defaults become optional, and an always-generated identity `id` is left out entirely.""",
        quick_bn=r"""শুধু `name`। `$inferInsert`-এ nullable column আর default থাকা column optional হয়ে যায়, আর always-generated identity `id` পুরোপুরি বাদ পড়ে।""",
        ex_en=r"""
            - `$inferInsert` reflects what the **database** requires on insert: `NOT NULL` without a default → required.
            - `createdAt` has a default (`now()`), so it's optional — the tempting answer C forgets that defaults make fields optional. It's also nullable here because there's no `.notNull()`, so `$inferSelect` gives `Date | null` — a hint that you probably want `.notNull().defaultNow()`.
            - With `generatedAlwaysAsIdentity()`, passing `id` is a type error (PostgreSQL would reject it too). `generatedByDefaultAsIdentity()` would make `id` optional instead.
            - `$inferSelect` is the row you get back: `{ id: number; name: string; bio: string | null; createdAt: Date | null }`. The helper types `InferSelectModel` / `InferInsertModel` are equivalent.
        """,
        ex_bn=r"""
            - `$inferInsert` দেখায় insert-এর সময় **database** কী চায়: default ছাড়া `NOT NULL` → required।
            - `createdAt`-এর default আছে (`now()`), তাই optional — লোভনীয় উত্তর C ভুলে যায় যে default থাকলে field optional হয়। এখানে `.notNull()` নেই বলে এটা nullable-ও, তাই `$inferSelect` দেয় `Date | null` — ইঙ্গিত যে সম্ভবত `.notNull().defaultNow()` চাওয়া উচিত ছিল।
            - `generatedAlwaysAsIdentity()` থাকলে `id` দেওয়া type error (PostgreSQL-ও reject করত)। `generatedByDefaultAsIdentity()` হলে বরং `id` optional হতো।
            - `$inferSelect` হলো ফেরত পাওয়া row: `{ id: number; name: string; bio: string | null; createdAt: Date | null }`। Helper type `InferSelectModel` / `InferInsertModel` একই কাজ করে।
        """,
        tip_en=r"""Explain the rule ("required = NOT NULL and no default") rather than memorising the answer. Then point out the nullable `createdAt` as a schema smell — that shows review instincts.""",
        tip_bn=r"""উত্তর মুখস্থ না করে নিয়মটা বলো ("required = NOT NULL আর default নেই")। তারপর nullable `createdAt`-কে schema-র দুর্বলতা হিসেবে দেখাও — এতে review করার দক্ষতা বোঝা যায়।""",
        related=["drizzle-002"],
        refs=[D_GOODIES],
    ),
    # ------------------------------------------------------------------ drizzle-007
    Q(
        id="drizzle-007", sub="Drizzle Kit", diff="easy", type="mcq",
        prio="high", market="both", mins=1,
        tags=["drizzle-kit", "migrations", "generate"],
        ver="drizzle-kit 0.31", vs=True, status="stable",
        q_en=r"""You added a column in `schema.ts` and want a reviewable SQL migration file that you commit to git and apply in every environment. Which Drizzle Kit command creates that file?""",
        q_bn=r"""তুমি `schema.ts`-এ একটা column যোগ করেছ, আর এমন একটা reviewable SQL migration file চাও যেটা git-এ commit করে প্রতিটা environment-এ apply করবে। কোন Drizzle Kit command সেই file তৈরি করে?""",
        options=[
            ("`drizzle-kit push`", "`drizzle-kit push`"),
            ("`drizzle-kit migrate`", "`drizzle-kit migrate`"),
            ("`drizzle-kit pull`", "`drizzle-kit pull`"),
            ("`drizzle-kit generate`", "`drizzle-kit generate`"),
        ],
        correct=3,
        a_en=r"""`drizzle-kit generate`. It compares your TypeScript schema with the last snapshot in the migrations folder and writes a new SQL file (e.g. `drizzle/0001_add_phone.sql`) — no database connection needed.""",
        a_bn=r"""`drizzle-kit generate`। এটা তোমার TypeScript schema-কে migrations folder-এর শেষ snapshot-এর সাথে তুলনা করে একটা নতুন SQL file লেখে (যেমন `drizzle/0001_add_phone.sql`) — database connection লাগে না।""",
        quick_en=r"""`drizzle-kit generate`: it diffs your TypeScript schema against the last snapshot and writes a new SQL migration file to review and commit, without connecting to the database.""",
        quick_bn=r"""`drizzle-kit generate`: এটা তোমার TypeScript schema-কে আগের snapshot-এর সাথে তুলনা করে একটা নতুন SQL migration file লেখে, যেটা review করে commit করা যায় — database-এ connect করারও দরকার হয় না।""",
        ex_en=r"""
            - `migrate` **applies** already-generated files to a database and records them in the `drizzle.__drizzle_migrations` table. It's the second half of the workflow.
            - `push` (the tempting answer) applies schema changes **directly** without creating a file — great for prototyping and local dev, risky for production because there's nothing to review or replay.
            - `pull` does the reverse: introspects an existing database and generates `schema.ts`.
            - Others: `studio` (browser data viewer), `check` (consistency of the migration history — useful when several developers generate migrations on different branches), `export`.
            - In drizzle-kit 0.31 the folder holds numbered `.sql` files plus `meta/_journal.json` and snapshots; the v1 RC switches to one folder per migration without a journal.
        """,
        ex_bn=r"""
            - `migrate` আগে থেকে generate করা file database-এ **apply** করে আর `drizzle.__drizzle_migrations` table-এ record রাখে। এটা workflow-এর দ্বিতীয় অর্ধেক।
            - `push` (লোভনীয় উত্তর) কোনো file না বানিয়ে **সরাসরি** schema change apply করে — prototype আর local dev-এর জন্য দারুণ, production-এর জন্য ঝুঁকিপূর্ণ, কারণ review বা replay করার কিছু থাকে না।
            - `pull` উল্টো কাজ করে: existing database introspect করে `schema.ts` তৈরি করে।
            - বাকিগুলো: `studio` (browser-এ data দেখার tool), `check` (migration history-র consistency — কয়েকজন developer আলাদা branch-এ migration generate করলে কাজে লাগে), `export`।
            - drizzle-kit 0.31-এ folder-এ থাকে numbered `.sql` file আর `meta/_journal.json` ও snapshot; v1 RC-তে প্রতিটা migration-এর আলাদা folder, journal ছাড়া।
        """,
        tip_en=r"""Describe the full loop in one breath: "edit schema → `generate` → review SQL in the PR → `migrate` in CI/CD". That's what interviewers want to hear.""",
        tip_bn=r"""পুরো চক্রটা এক নিঃশ্বাসে বলো: "schema edit → `generate` → PR-এ SQL review → CI/CD-তে `migrate`"। Interviewer এটাই শুনতে চায়।""",
        related=["drizzle-017", "drizzle-026"],
        refs=[D_KIT_GENERATE, D_KIT_OVERVIEW],
    ),
    # ------------------------------------------------------------------ drizzle-008
    Q(
        id="drizzle-008", sub="Security: SQL Injection", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["sql-injection", "sql-template", "sql-raw", "security"],
        ver="Drizzle ORM 0.45.x", vs=False, status="stable",
        q_en=r"""`name` comes straight from the query string. Which of the lines A–D is vulnerable to SQL injection?""",
        q_bn=r"""`name` সরাসরি query string থেকে আসছে। A–D লাইনগুলোর মধ্যে কোনটা SQL injection-এর ঝুঁকিতে আছে?""",
        code=r"""
            const name = String(req.query.name); // untrusted input

            // A
            await db.select().from(users).where(eq(users.name, name));
            // B
            await db.select().from(users).where(sql`${users.name} = ${name}`);
            // C
            await db.execute(sql`select * from users where name = ${name}`);
            // D
            await db.execute(sql.raw(`select * from users where name = '${name}'`));
        """,
        lang="typescript",
        options=[
            ("Only D — `sql.raw()` puts the string into the SQL text without parameters", "শুধু D — `sql.raw()` parameter ছাড়াই string-টা SQL text-এ বসিয়ে দেয়"),
            ("B and C — interpolating into the `sql` tag concatenates the value into the query", "B আর C — `sql` tag-এ interpolate করলে value query-তে জুড়ে যায়"),
            ("Only C — `db.execute()` bypasses parameter binding", "শুধু C — `db.execute()` parameter binding এড়িয়ে যায়"),
            ("None — Drizzle escapes all input automatically", "কোনোটাই না — Drizzle সব input নিজে থেকেই escape করে"),
        ],
        correct=0,
        a_en=r"""Only D. In A, B and C the value becomes a bound parameter (`$1`). `sql.raw()` inserts its argument verbatim into the SQL text, and here that argument is a JavaScript template string built from user input — classic injection.""",
        a_bn=r"""শুধু D। A, B আর C-তে value একটা bound parameter (`$1`) হয়ে যায়। `sql.raw()` তার argument হুবহু SQL text-এ বসিয়ে দেয়, আর এখানে সেই argument user input দিয়ে বানানো একটা JavaScript template string — classic injection।""",
        quick_en=r"""Only D: `sql.raw()` inserts its string into the SQL text verbatim, so a template string built from user input is injectable. Values interpolated into the `sql` tag or passed to the builders become bound parameters.""",
        quick_bn=r"""শুধু D: `sql.raw()` তার string হুবহু SQL text-এ বসিয়ে দেয়, তাই user input দিয়ে বানানো template string থাকলে SQL injection হয়। `sql` tag-এ interpolate করা বা builder-এ দেওয়া value bound parameter হিসেবে যায়।""",
        ex_en=r"""
            The tempting wrong answer is B/C: they *look* like string interpolation, but `sql` is a **tagged template**. Drizzle receives the static parts and the values separately, and sends values as parameters — verified output for B: `where "users"."name" = $1` with `params: ["x' OR 1=1 --"]`.

            `sql.raw()` exists for trusted, static SQL fragments (e.g. a sort direction you chose from a whitelist). Never pass user input to it. For dynamic identifiers like a sort column, map the input to a known column object (`{ name: users.name, created: users.createdAt }[key]`) instead of building SQL text.

            Option D in the list ("Drizzle escapes everything") is the dangerous belief that leads to bugs like line D.
        """,
        ex_bn=r"""
            লোভনীয় ভুল উত্তর হলো B/C: দেখতে string interpolation-এর মতো, কিন্তু `sql` একটা **tagged template**। Drizzle static অংশ আর value আলাদাভাবে পায়, আর value parameter হিসেবে পাঠায় — B-এর যাচাই করা output: `where "users"."name" = $1`, `params: ["x' OR 1=1 --"]`।

            `sql.raw()` আছে বিশ্বস্ত, static SQL fragment-এর জন্য (যেমন whitelist থেকে বেছে নেওয়া sort direction)। এতে কখনো user input দিও না। Sort column-এর মতো dynamic identifier-এর জন্য SQL text না বানিয়ে input-কে একটা পরিচিত column object-এ map করো (`{ name: users.name, created: users.createdAt }[key]`)।

            List-এর option D ("Drizzle সব escape করে") হলো সেই বিপজ্জনক বিশ্বাস, যেটা line D-র মতো bug তৈরি করে।
        """,
        tip_en=r"""Use the words "tagged template" and "bound parameter". Then mention the whitelist approach for dynamic column names — that's the real-world follow-up.""",
        tip_bn=r""""Tagged template" আর "bound parameter" কথাগুলো ব্যবহার করো। তারপর dynamic column name-এর জন্য whitelist পদ্ধতির কথা বলো — বাস্তবে follow-up প্রশ্ন এটাই আসে।""",
        related=["drizzle-011", "drizzle-028"],
        refs=[D_SQL, OWASP_SQLI],
    ),
]

if __name__ == "__main__":
    save("drizzle", "b1", QUESTIONS)
