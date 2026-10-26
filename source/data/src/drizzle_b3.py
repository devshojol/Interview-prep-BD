# Drizzle ORM — batch 3 (drizzle-017 … drizzle-024): migrations workflow, upserts, error handling,
# Drizzle vs Prisma, prepared statements, dynamic queries, serverless connections, PgBouncer
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

D_MIGRATIONS = ("Drizzle ORM — Migrations", "https://orm.drizzle.team/docs/migrations")
D_CONFIG = ("Drizzle Kit — drizzle.config.ts", "https://orm.drizzle.team/docs/drizzle-config-file")
D_KIT_PUSH = ("Drizzle Kit — push", "https://orm.drizzle.team/docs/drizzle-kit-push")
D_KIT_MIGRATE = ("Drizzle Kit — migrate", "https://orm.drizzle.team/docs/drizzle-kit-migrate")
D_INSERT = ("Drizzle ORM — Insert (upserts)", "https://orm.drizzle.team/docs/insert")
D_OVERVIEW = ("Drizzle ORM — Overview", "https://orm.drizzle.team/docs/overview")
D_PERF_QUERIES = ("Drizzle ORM — Query performance (prepared statements)", "https://orm.drizzle.team/docs/perf-queries")
D_DYNAMIC = ("Drizzle ORM — Dynamic query building", "https://orm.drizzle.team/docs/dynamic-query-building")
D_OPERATORS = ("Drizzle ORM — Filter operators", "https://orm.drizzle.team/docs/operators")
D_PERF_SERVERLESS = ("Drizzle ORM — Serverless performance", "https://orm.drizzle.team/docs/perf-serverless")
D_NEON = ("Drizzle ORM — Connect Neon", "https://orm.drizzle.team/docs/connect-neon")
D_SUPABASE = ("Drizzle ORM — Connect Supabase", "https://orm.drizzle.team/docs/connect-supabase")
PG_INSERT = ("PostgreSQL docs — INSERT … ON CONFLICT", "https://www.postgresql.org/docs/current/sql-insert.html")
PG_ERRCODES = ("PostgreSQL docs — Error codes", "https://www.postgresql.org/docs/current/errcodes-appendix.html")

QUESTIONS = [
    # ------------------------------------------------------------------ drizzle-017
    Q(
        id="drizzle-017", sub="Migrations (Drizzle Kit)", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["migrations", "drizzle-kit", "push", "generate", "migrate"],
        ver="drizzle-kit 0.31 / Drizzle ORM 0.45.x", vs=True, status="stable",
        q_en=r"""Compare the two Drizzle Kit workflows — `generate` + `migrate` versus `push`. How do you configure Drizzle Kit, and which workflow would you use locally, in CI and in production?""",
        q_bn=r"""Drizzle Kit-এর দুটো workflow তুলনা করো — `generate` + `migrate` বনাম `push`। Drizzle Kit কীভাবে configure করো, আর local, CI আর production-এ কোন workflow ব্যবহার করবে?""",
        a_en=r"""
            **Config:** `drizzle.config.ts` exports `defineConfig({ dialect: 'postgresql', schema, out, dbCredentials: { url } })` from `drizzle-kit`.

            **`generate` + `migrate` (versioned migrations):**
            - `drizzle-kit generate` diffs the TypeScript schema against the last snapshot and writes a SQL file into `out` — no DB needed.
            - The SQL is reviewed in the pull request and committed.
            - `drizzle-kit migrate` (or `migrate()` from `drizzle-orm/node-postgres/migrator` in a deploy script) applies pending files and records them in `drizzle.__drizzle_migrations`.
            - Reproducible, reviewable, works for every environment → **CI and production**.

            **`push` (state sync):**
            - Introspects the target database, diffs it with the schema and applies the changes directly. No files, no history.
            - Very fast for **local prototyping** or throwaway preview databases; risky for production because changes aren't reviewed or replayable, and destructive diffs (drops, type changes) are easy to apply by accident.

            My setup: `push` only on my local DB while iterating, then `generate` once the schema settles; CI runs `migrate` against a fresh database to prove the migrations apply; production runs `migrate` as a separate release step.
        """,
        a_bn=r"""
            **Config:** `drizzle.config.ts`, `drizzle-kit` থেকে `defineConfig({ dialect: 'postgresql', schema, out, dbCredentials: { url } })` export করে।

            **`generate` + `migrate` (versioned migration):**
            - `drizzle-kit generate` TypeScript schema-কে শেষ snapshot-এর সাথে diff করে `out`-এ একটা SQL file লেখে — DB লাগে না।
            - Pull request-এ SQL review হয় আর commit হয়।
            - `drizzle-kit migrate` (বা deploy script-এ `drizzle-orm/node-postgres/migrator`-এর `migrate()`) pending file apply করে আর `drizzle.__drizzle_migrations`-এ record রাখে।
            - Reproducible, reviewable, সব environment-এ কাজ করে → **CI আর production**।

            **`push` (state sync):**
            - Target database introspect করে, schema-র সাথে diff করে, সরাসরি change apply করে। কোনো file নেই, history নেই।
            - **Local prototyping** বা অস্থায়ী preview database-এর জন্য খুব দ্রুত; production-এর জন্য ঝুঁকিপূর্ণ, কারণ change review বা replay করা যায় না, আর destructive diff (drop, type change) ভুল করে apply হয়ে যাওয়া সহজ।

            আমার setup: iterate করার সময় শুধু local DB-তে `push`, schema স্থির হলে `generate`; CI একটা fresh database-এ `migrate` চালিয়ে প্রমাণ করে migration apply হয়; production-এ আলাদা release step হিসেবে `migrate`।
        """,
        quick_en=r"""Configure it with `defineConfig({ dialect, schema, out, dbCredentials })` in `drizzle.config.ts`. `generate` + `migrate` produces reviewed, versioned SQL files and suits CI and production; `push` syncs the schema straight to a database with no files or history, so keep it for local prototyping.""",
        quick_bn=r"""`drizzle.config.ts`-এ `defineConfig({ dialect, schema, out, dbCredentials })` দিয়ে configure করি। `generate` + `migrate` review করা, versioned SQL file বানায় — CI আর production-এর জন্য এটাই; `push` কোনো file বা history ছাড়াই schema সরাসরি database-এ বসিয়ে দেয়, তাই এটা শুধু local prototyping-এর জন্য।""",
        ex_en=r"""
            - **Atomic batch:** Drizzle's PostgreSQL migrator applies all pending migrations of a run inside **one transaction** — if one statement fails, the whole run rolls back. Great for safety, but it means statements that can't run in a transaction (`CREATE INDEX CONCURRENTLY`) must be handled outside the migrator.
            - **Teams:** two branches can generate conflicting migrations; `drizzle-kit check` validates the history, and you regenerate after rebasing.
            - **Custom SQL:** `drizzle-kit generate --custom --name backfill_x` creates an empty migration for data backfills or anything Drizzle doesn't model (triggers, functions).
            - **Don't migrate from every app instance at startup** — run it once per release (CI job, Kubernetes Job, or a pre-deploy hook).
            - Useful extras: `strict: true` (confirm before `push`), `verbose: true` (print SQL), `casing: 'snake_case'`; `drizzle-kit studio` for browsing data.
        """,
        ex_bn=r"""
            - **Atomic batch:** Drizzle-এর PostgreSQL migrator একবারের সব pending migration **একটা transaction-এর** ভেতরে apply করে — একটা statement fail করলে পুরো run rollback হয়। নিরাপত্তার জন্য দারুণ, কিন্তু এর মানে যেসব statement transaction-এ চলে না (`CREATE INDEX CONCURRENTLY`), সেগুলো migrator-এর বাইরে সামলাতে হয়।
            - **Team:** দুটো branch conflict করা migration generate করতে পারে; `drizzle-kit check` history যাচাই করে, আর rebase-এর পর আবার generate করো।
            - **Custom SQL:** `drizzle-kit generate --custom --name backfill_x` data backfill বা Drizzle যা model করে না (trigger, function) তার জন্য একটা ফাঁকা migration বানায়।
            - **প্রতিটা app instance-এর startup থেকে migrate কোরো না** — প্রতি release-এ একবার চালাও (CI job, Kubernetes Job, বা pre-deploy hook)।
            - কাজের extra: `strict: true` (`push`-এর আগে confirm), `verbose: true` (SQL print), `casing: 'snake_case'`; data দেখতে `drizzle-kit studio`।
        """,
        tip_en=r"""Frame it as "state sync vs versioned history". Then state a clear policy per environment — interviewers want to know you won't run `push` against production.""",
        tip_bn=r""""State sync বনাম versioned history" হিসেবে বলো। তারপর প্রতিটা environment-এর জন্য পরিষ্কার নীতি বলো — interviewer জানতে চায় তুমি production-এ `push` চালাবে না।""",
        mist_en=r"""Using `push` in production; editing an already-applied migration file instead of adding a new one; running migrations concurrently from several pods; not committing the `meta` folder (snapshots/journal), which breaks the next `generate`.""",
        mist_bn=r"""Production-এ `push` ব্যবহার করা; apply হয়ে যাওয়া migration file edit করা, নতুন না বানিয়ে; কয়েকটা pod থেকে একসাথে migration চালানো; `meta` folder (snapshot/journal) commit না করা, ফলে পরের `generate` ভেঙে যায়।""",
        code=r"""
            // drizzle.config.ts
            import { defineConfig } from 'drizzle-kit';

            export default defineConfig({
              dialect: 'postgresql',
              schema: './src/db/schema.ts',
              out: './drizzle',
              dbCredentials: { url: process.env.DATABASE_URL! },
              strict: true,   // ask before applying `push` changes
              verbose: true,  // print the SQL
            });

            // package.json scripts
            // "db:generate": "drizzle-kit generate",
            // "db:migrate":  "drizzle-kit migrate",
            // "db:push":     "drizzle-kit push",      <- local prototyping only
            // "db:check":    "drizzle-kit check",
            // "db:studio":   "drizzle-kit studio"

            // scripts/migrate.ts — programmatic alternative for a release step
            import { drizzle } from 'drizzle-orm/node-postgres';
            import { migrate } from 'drizzle-orm/node-postgres/migrator';

            const db = drizzle(process.env.DATABASE_URL!);
            await migrate(db, { migrationsFolder: './drizzle' });
            await db.$client.end();
        """,
        lang="typescript",
        follow=[
            ("How do you resolve two developers generating migration 0007 on different branches?", "দুজন developer আলাদা branch-এ migration 0007 generate করলে কীভাবে সমাধান করবে?"),
            ("Where should migrations run in a Kubernetes deployment?", "Kubernetes deployment-এ migration কোথায় চলা উচিত?"),
        ],
        related=["drizzle-007", "drizzle-026", "drizzle-032"],
        refs=[D_MIGRATIONS, D_CONFIG, D_KIT_PUSH],
    ),
    # ------------------------------------------------------------------ drizzle-018
    Q(
        id="drizzle-018", sub="Upserts (onConflictDoUpdate)", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["upsert", "on-conflict", "unique-constraint", "postgresql"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""The `label` column has **no** unique constraint or unique index. What happens when this upsert runs?""",
        q_bn=r"""`label` column-এ **কোনো** unique constraint বা unique index নেই। এই upsert চালালে কী হবে?""",
        code=r"""
            export const tags = pgTable('tags', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              label: text().notNull(),
              usageCount: integer('usage_count').notNull().default(0),
            });

            await db
              .insert(tags)
              .values({ label: 'nestjs', usageCount: 1 })
              .onConflictDoUpdate({
                target: tags.label,
                set: { usageCount: sql`${tags.usageCount} + 1` },
              });
        """,
        lang="typescript",
        options=[
            ("It inserts a new duplicate row every time, because nothing can conflict", "প্রতিবার একটা নতুন duplicate row insert করে, কারণ conflict হওয়ার কিছু নেই"),
            ("PostgreSQL rejects it with error `42P10`: there is no unique or exclusion constraint matching the ON CONFLICT specification", "PostgreSQL error `42P10` দিয়ে reject করে: ON CONFLICT specification-এর সাথে মেলে এমন কোনো unique বা exclusion constraint নেই"),
            ("Drizzle detects the missing constraint and falls back to UPDATE when the label exists", "Drizzle constraint না থাকা ধরে ফেলে, আর label থাকলে UPDATE-এ চলে যায়"),
            ("TypeScript fails to compile because `target` must be the primary key", "TypeScript compile হয় না, কারণ `target` অবশ্যই primary key হতে হবে"),
        ],
        correct=1,
        a_en=r"""PostgreSQL rejects the statement with SQLSTATE `42P10` ("there is no unique or exclusion constraint matching the ON CONFLICT specification"), wrapped by Drizzle in a `DrizzleQueryError`. `ON CONFLICT (label)` needs an arbiter: a unique index or constraint on exactly that column set.""",
        a_bn=r"""PostgreSQL SQLSTATE `42P10` ("there is no unique or exclusion constraint matching the ON CONFLICT specification") দিয়ে statement reject করে, যেটা Drizzle একটা `DrizzleQueryError`-এ wrap করে। `ON CONFLICT (label)`-এর একটা arbiter লাগে: ঠিক সেই column set-এর উপর একটা unique index বা constraint।""",
        quick_en=r"""PostgreSQL rejects it with `42P10` (no unique or exclusion constraint matching the ON CONFLICT specification), wrapped in a `DrizzleQueryError`, because `ON CONFLICT (label)` needs a unique index or constraint on exactly that column.""",
        quick_bn=r"""PostgreSQL `42P10` error দিয়ে statement reject করে (ON CONFLICT-এর সাথে মেলে এমন unique বা exclusion constraint নেই), আর Drizzle সেটা `DrizzleQueryError`-এ wrap করে; কারণ `ON CONFLICT (label)`-এর জন্য ঠিক ওই column-এ unique index বা constraint লাগে।""",
        ex_en=r"""
            - Option A is tempting ("no constraint, so no conflict"), but PostgreSQL validates the `ON CONFLICT` target at planning time and refuses the statement — verified on PostgreSQL.
            - **Fix:** `label: text().notNull().unique()` (or a `uniqueIndex` in the third `pgTable` argument), generate and apply the migration. Then the same code works: three runs return `usageCount` 1, 2, 3.
            - **`set` references:** `${tags.usageCount}` refers to the **existing** row's value; use an `excluded.usage_count` reference inside the `sql` tag to read the value you tried to insert (the `excluded` pseudo-table).
            - **Partial unique indexes** need `targetWhere` so PostgreSQL can match the right arbiter.
            - Upsert is the concurrency-safe alternative to "SELECT, then INSERT or UPDATE", which races under load.
        """,
        ex_bn=r"""
            - Option A লোভনীয় ("constraint নেই, তাই conflict-ও নেই"), কিন্তু PostgreSQL planning-এর সময়েই `ON CONFLICT` target যাচাই করে আর statement প্রত্যাখ্যান করে — PostgreSQL-এ যাচাই করা।
            - **সমাধান:** `label: text().notNull().unique()` (বা `pgTable`-এর তৃতীয় argument-এ একটা `uniqueIndex`), তারপর migration generate করে apply করো। তখন একই code কাজ করে: তিনবার চালালে `usageCount` আসে 1, 2, 3।
            - **`set`-এর reference:** `${tags.usageCount}` **existing** row-এর value বোঝায়; যে value insert করার চেষ্টা করেছিলে সেটা পড়তে `sql` tag-এর ভেতরে `excluded.usage_count` reference ব্যবহার করো (`excluded` pseudo-table)।
            - **Partial unique index** হলে `targetWhere` লাগে, যাতে PostgreSQL সঠিক arbiter মেলাতে পারে।
            - "SELECT, তারপর INSERT বা UPDATE"-এর concurrency-safe বিকল্প হলো upsert; ওই পদ্ধতি load-এর সময় race করে।
        """,
        tip_en=r"""Explain *why* PostgreSQL needs an arbiter index — the conflict is detected by the index, not by scanning the table. That one sentence shows you understand how upserts work.""",
        tip_bn=r"""PostgreSQL-এর কেন arbiter index লাগে সেটা ব্যাখ্যা করো — conflict ধরা পড়ে index দিয়ে, table scan করে না। এই এক বাক্যেই বোঝা যায় upsert কীভাবে কাজ করে তুমি জানো।""",
        related=["drizzle-019", "drizzle-012"],
        refs=[D_INSERT, PG_INSERT],
    ),
    # ------------------------------------------------------------------ drizzle-019
    Q(
        id="drizzle-019", sub="Error Handling", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["error-handling", "drizzlequeryerror", "unique-violation", "23505"],
        ver="Drizzle ORM 0.45.x (DrizzleQueryError since 0.44)", vs=True, status="version-specific",
        q_en=r"""After upgrading Drizzle from 0.43 to 0.45, registering with an existing email returns **500** instead of **409 Conflict**. The registration code didn't change. Why, and how do you fix it robustly?""",
        q_bn=r"""Drizzle 0.43 থেকে 0.45-এ upgrade করার পর existing email দিয়ে register করলে **409 Conflict**-এর বদলে **500** আসছে। Registration code বদলায়নি। কেন, আর কীভাবে মজবুতভাবে ঠিক করবে?""",
        code=r"""
            export async function register(dto: { email: string; name: string }) {
              try {
                const [user] = await db.insert(users).values(dto).returning();
                return user;
              } catch (err: any) {
                if (err.code === '23505') {
                  throw new ConflictException('Email is already registered');
                }
                throw err;
              }
            }
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                import { DrizzleQueryError } from 'drizzle-orm';

                type PgError = { code?: string; constraint?: string };

                export function pgError(err: unknown): PgError | undefined {
                  const cause = err instanceof DrizzleQueryError ? err.cause : err;
                  return typeof cause === 'object' && cause !== null ? (cause as PgError) : undefined;
                }

                export function isUniqueViolation(err: unknown, constraint?: string): boolean {
                  const e = pgError(err);
                  return e?.code === '23505' && (!constraint || e.constraint === constraint);
                }

                export async function register(dto: { email: string; name: string }) {
                  try {
                    const [user] = await db.insert(users).values(dto).returning();
                    return user;
                  } catch (err) {
                    if (isUniqueViolation(err, 'users_email_unique')) {
                      throw new ConflictException('Email is already registered');
                    }
                    throw err;
                  }
                }
            """),
        ],
        a_en=r"""
            Since **Drizzle 0.44**, errors from database drivers are wrapped in a `DrizzleQueryError`. Its message contains the failed SQL and params, and the **original driver error** (from `pg`, with `code`, `constraint`, `detail`) is in `err.cause`. So `err.code` is now `undefined`, the check never matches, and the error falls through to a generic 500.

            Fix: unwrap first — `const e = err instanceof DrizzleQueryError ? err.cause : err` — then check `e.code === '23505'`. I also check `e.constraint` (here the generated name `users_email_unique`), so a unique violation on another column isn't reported as "email taken". Putting this in a small helper keeps every caller correct and makes the next upgrade a one-line change.
        """,
        a_bn=r"""
            **Drizzle 0.44** থেকে database driver-এর error একটা `DrizzleQueryError`-এ wrap হয়। এর message-এ fail করা SQL আর params থাকে, আর **আসল driver error** (`pg` থেকে, `code`, `constraint`, `detail` সহ) থাকে `err.cause`-এ। তাই `err.code` এখন `undefined`, check কখনো match করে না, আর error সাধারণ 500 হয়ে যায়।

            সমাধান: আগে unwrap করো — `const e = err instanceof DrizzleQueryError ? err.cause : err` — তারপর `e.code === '23505'` check করো। আমি `e.constraint`-ও check করি (এখানে generated নাম `users_email_unique`), যাতে অন্য column-এর unique violation-কে "email taken" বলা না হয়। এটা একটা ছোট helper-এ রাখলে সব caller ঠিক থাকে, আর পরের upgrade-এ এক লাইনের পরিবর্তনেই কাজ হয়।
        """,
        quick_en=r"""Since Drizzle 0.44, driver errors are wrapped in `DrizzleQueryError`, so `err.code` is undefined and the `23505` check never matches. Unwrap `err.cause` first, then check `code === '23505'` (and the constraint name) in one shared helper.""",
        quick_bn=r"""Drizzle 0.44 থেকে driver error `DrizzleQueryError`-এ wrap হয়ে আসে, তাই `err.code` এখন undefined আর `23505` check কখনো মেলে না। আগে `err.cause` unwrap করি, তারপর একটা shared helper-এ `code === '23505'` (আর constraint-এর নাম) check করি।""",
        ex_en=r"""
            - **Why a status-code test didn't catch it:** most tests used a mocked repository; only an integration test against real PostgreSQL would have shown the new error shape. Add one for each mapped error.
            - **Useful SQLSTATEs:** `23505` unique violation, `23503` foreign-key violation, `23502` not-null violation, `23514` check violation, `40001` serialization failure (retry), `40P01` deadlock (retry).
            - **Logging risk:** the `DrizzleQueryError` message includes the query **params** — emails, names, maybe password hashes. Redact or log only `err.cause.code` and the constraint name in production logs.
            - **Prefer constraints over pre-checks:** "SELECT to see if the email exists, then INSERT" races under concurrency; letting the unique constraint decide and mapping `23505` is correct and cheaper.
        """,
        ex_bn=r"""
            - **Status-code test কেন ধরেনি:** বেশিরভাগ test mock repository ব্যবহার করেছিল; শুধু আসল PostgreSQL-এর বিরুদ্ধে integration test নতুন error shape দেখাত। প্রতিটা map করা error-এর জন্য একটা করে লেখো।
            - **কাজের SQLSTATE:** `23505` unique violation, `23503` foreign-key violation, `23502` not-null violation, `23514` check violation, `40001` serialization failure (retry), `40P01` deadlock (retry)।
            - **Logging-এর ঝুঁকি:** `DrizzleQueryError`-এর message-এ query-র **params** থাকে — email, নাম, হয়তো password hash। Production log-এ redact করো, বা শুধু `err.cause.code` আর constraint-এর নাম log করো।
            - **Pre-check-এর বদলে constraint:** "email আছে কি না SELECT করে দেখো, তারপর INSERT" concurrency-তে race করে; unique constraint-কে সিদ্ধান্ত নিতে দিয়ে `23505` map করা সঠিক আর সস্তাও।
        """,
        tip_en=r"""Name the change precisely ("0.44 wraps driver errors in `DrizzleQueryError`, original in `.cause`") and propose the helper plus an integration test. Mentioning that the message leaks params into logs is a strong security bonus.""",
        tip_bn=r"""পরিবর্তনটা নির্দিষ্টভাবে বলো ("0.44 driver error-কে `DrizzleQueryError`-এ wrap করে, আসলটা `.cause`-এ") আর helper ও integration test প্রস্তাব করো। Message যে log-এ params leak করে, সেটা বললে security-তে বাড়তি নম্বর।""",
        mist_en=r"""Matching on the error message text; checking only `err.code`; mapping every 23505 to "email taken" without checking the constraint; logging the full error message with user data.""",
        mist_bn=r"""Error message-এর text দিয়ে match করা; শুধু `err.code` check করা; constraint না দেখে প্রতিটা 23505-কে "email taken" বানানো; user data সহ পুরো error message log করা।""",
        follow=[
            ("Which errors would you retry automatically, and how many times?", "কোন error গুলো automatically retry করবে, আর কতবার?"),
            ("How would you map a foreign-key violation for an API client?", "API client-এর জন্য foreign-key violation কীভাবে map করবে?"),
        ],
        related=["drizzle-018", "nest-025"],
        refs=[D_OVERVIEW, PG_ERRCODES],
    ),
    # ------------------------------------------------------------------ drizzle-020
    Q(
        id="drizzle-020", sub="Drizzle vs Prisma", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["prisma", "drizzle", "orm-comparison", "codegen", "trade-offs"],
        ver="Drizzle ORM 0.45.x / Prisma ORM 7.x", vs=True, status="stable",
        q_en=r"""Drizzle vs Prisma: what are the key differences, and how would you choose between them for a new TypeScript backend?""",
        q_bn=r"""Drizzle বনাম Prisma: মূল পার্থক্যগুলো কী, আর একটা নতুন TypeScript backend-এর জন্য কীভাবে বেছে নেবে?""",
        a_en=r"""
            - **Schema:** Prisma uses its own schema language (`schema.prisma`); Drizzle schemas are plain TypeScript.
            - **Types:** Prisma generates a client (`prisma generate`) — types come from code generation. Drizzle infers types directly from the TypeScript schema; there's no generate step for the query types.
            - **Query style:** Prisma offers a high-level object API (`findMany({ where, include })`, nested writes). Drizzle offers a SQL-like builder (joins, subqueries, upserts close to SQL) plus a relational API for nested reads.
            - **Control vs abstraction:** Drizzle makes the SQL obvious and keeps you close to PostgreSQL features; Prisma hides more SQL, which many teams find faster to start with.
            - **Migrations:** both have tooling — Prisma Migrate vs Drizzle Kit (`generate`/`migrate`/`push`).

            **How I choose:** a team comfortable with SQL that wants fine control, serverless-friendly footprint and PostgreSQL-specific features → Drizzle. A team that values a polished high-level API, nested writes and Prisma's ecosystem (Studio, docs, wide adoption) → Prisma. Both are solid; consistency within the codebase matters more than the pick.
        """,
        a_bn=r"""
            - **Schema:** Prisma নিজের schema language (`schema.prisma`) ব্যবহার করে; Drizzle-এর schema সাধারণ TypeScript।
            - **Type:** Prisma একটা client generate করে (`prisma generate`) — type আসে code generation থেকে। Drizzle সরাসরি TypeScript schema থেকে type infer করে; query type-এর জন্য generate step নেই।
            - **Query style:** Prisma high-level object API দেয় (`findMany({ where, include })`, nested write)। Drizzle দেয় SQL-এর মতো builder (join, subquery, upsert — SQL-এর কাছাকাছি) আর nested read-এর জন্য relational API।
            - **Control বনাম abstraction:** Drizzle SQL স্পষ্ট রাখে আর PostgreSQL-এর feature-এর কাছাকাছি রাখে; Prisma বেশি SQL লুকায়, যেটা দিয়ে অনেক team দ্রুত শুরু করতে পারে।
            - **Migration:** দুটোরই tooling আছে — Prisma Migrate বনাম Drizzle Kit (`generate`/`migrate`/`push`)।

            **আমি কীভাবে বেছে নিই:** SQL-এ স্বচ্ছন্দ team যারা সূক্ষ্ম control, serverless-friendly footprint আর PostgreSQL-specific feature চায় → Drizzle। যে team polished high-level API, nested write আর Prisma-র ecosystem (Studio, docs, ব্যাপক ব্যবহার) মূল্য দেয় → Prisma। দুটোই ভালো; কোনটা বাছলে তার চেয়ে codebase-এ consistency বেশি গুরুত্বপূর্ণ।
        """,
        quick_en=r"""Prisma has its own schema language, a generated client and a high-level object API with nested writes; Drizzle schemas are plain TypeScript, types are inferred without a generate step, and queries stay close to SQL. Pick Drizzle for SQL control, Prisma for a polished high-level API.""",
        quick_bn=r"""Prisma-র নিজস্ব schema language, generate করা client আর nested write-সহ high-level object API আছে; Drizzle-এর schema সাধারণ TypeScript, generate step ছাড়াই type infer হয়, আর query SQL-এর কাছাকাছি থাকে। SQL-এর উপর control চাইলে Drizzle, polished high-level API চাইলে Prisma।""",
        ex_en=r"""
            - **Raw SQL:** Prisma has `$queryRaw` (tagged template, parameterised) and typed SQL files; Drizzle has the `sql` tag that composes inside typed queries.
            - **Transactions:** Prisma's nested writes and `$transaction` cover many cases implicitly; in Drizzle you write `db.transaction(async (tx) => ...)` explicitly.
            - **Performance:** for typical CRUD both are fast enough — the database, indexes and query shape matter far more. Measure your own hot queries instead of trusting benchmark charts.
            - **Keep comparisons current:** both projects change quickly (Prisma's 6.x–7.x architecture changes, Drizzle's v1 RC with RQB v2). Older blog posts about bundle size or engines may be outdated — check the current docs.
            - **Migration between them** is mostly rewriting the data-access layer; keeping repositories as a boundary makes such a switch (or a mixed period) manageable.
        """,
        ex_bn=r"""
            - **Raw SQL:** Prisma-র আছে `$queryRaw` (tagged template, parameterised) আর typed SQL file; Drizzle-এর আছে `sql` tag, যেটা typed query-র ভেতরেই compose হয়।
            - **Transaction:** Prisma-র nested write আর `$transaction` অনেক ক্ষেত্র implicitly সামলায়; Drizzle-এ `db.transaction(async (tx) => ...)` explicitly লিখতে হয়।
            - **Performance:** সাধারণ CRUD-এ দুটোই যথেষ্ট দ্রুত — database, index আর query-র গঠন অনেক বেশি গুরুত্বপূর্ণ। Benchmark chart বিশ্বাস না করে নিজের hot query মাপো।
            - **তুলনা হালনাগাদ রাখো:** দুটো project-ই দ্রুত বদলায় (Prisma-র 6.x–7.x architecture পরিবর্তন, Drizzle-এর RQB v2 সহ v1 RC)। Bundle size বা engine নিয়ে পুরোনো blog post পুরোনো হয়ে থাকতে পারে — current docs দেখো।
            - **একটা থেকে আরেকটায় যাওয়া** মূলত data-access layer আবার লেখা; repository-কে boundary হিসেবে রাখলে এমন switch (বা মিশ্র সময়) সামলানো যায়।
        """,
        tip_en=r"""Avoid tribal answers. Compare on 3–4 concrete axes (schema, type generation, query style, migrations), then tie the choice to the team and the project. Saying "consistency matters more than the pick" sounds senior.""",
        tip_bn=r"""দলবাজি উত্তর এড়াও। ৩–৪টা নির্দিষ্ট দিক ধরে তুলনা করো (schema, type generation, query style, migration), তারপর বাছাইটা team আর project-এর সাথে যুক্ত করো। "কোনটা বাছলে তার চেয়ে consistency বেশি গুরুত্বপূর্ণ" বললে senior শোনায়।""",
        mist_en=r"""Claiming one is "always faster"; repeating outdated claims about engines or bundle size; saying Drizzle has no migrations or Prisma can't run raw SQL.""",
        mist_bn=r"""দাবি করা যে একটা "সবসময় দ্রুত"; engine বা bundle size নিয়ে পুরোনো দাবি আবার বলা; বলা যে Drizzle-এর migration নেই বা Prisma raw SQL চালাতে পারে না।""",
        code=r"""
            // Prisma (schema.prisma + generated client)
            // model User { id Int @id @default(autoincrement())  email String @unique  posts Post[] }
            const prismaUsers = await prisma.user.findMany({
              where: { email: { endsWith: '@example.com' } },
              include: { posts: true },
            });

            // Drizzle (TypeScript schema, no client generation)
            const drizzleUsers = await db.query.users.findMany({
              where: (u, { like }) => like(u.email, '%@example.com'),
              with: { posts: true },
            });

            // Drizzle SQL-like builder when you want the join shape explicitly
            const rows = await db
              .select({ email: users.email, title: posts.title })
              .from(users)
              .leftJoin(posts, eq(posts.authorId, users.id));
        """,
        lang="typescript",
        follow=[
            ("How would you migrate an existing Prisma project to Drizzle incrementally?", "একটা existing Prisma project ধাপে ধাপে Drizzle-এ কীভাবে migrate করবে?"),
            ("Which features of PostgreSQL are easier to use from Drizzle?", "PostgreSQL-এর কোন feature গুলো Drizzle থেকে ব্যবহার করা সহজ?"),
        ],
        related=["drizzle-001", "drizzle-031"],
        refs=[D_OVERVIEW, D_MIGRATIONS],
    ),
    # ------------------------------------------------------------------ drizzle-021
    Q(
        id="drizzle-021", sub="Prepared Statements", diff="medium", type="conceptual",
        prio="medium", market="both", mins=5,
        tags=["prepared-statements", "placeholders", "performance"],
        ver="Drizzle ORM 0.45.x / pg 8", vs=False, status="stable",
        q_en=r"""What are prepared statements in Drizzle (`.prepare()` with `sql.placeholder()`), what do they actually speed up, and what caveats should you know?""",
        q_bn=r"""Drizzle-এ prepared statement (`sql.placeholder()` সহ `.prepare()`) কী, এগুলো আসলে কী দ্রুত করে, আর কোন সতর্কতা জানা দরকার?""",
        a_en=r"""
            A prepared statement is a query built **once** with placeholders and executed many times with different values:

            `const userById = db.select().from(users).where(eq(users.id, sql.placeholder('id'))).prepare('user_by_id');` then `await userById.execute({ id: 42 })`.

            Two things get faster:
            - **In Node.js:** Drizzle skips rebuilding the query object and SQL string on every call.
            - **In PostgreSQL:** with node-postgres, a named statement is parsed and planned once per connection; later executions only bind parameters. That matters most for large, complex queries on hot paths.

            It's a performance tool, not a security feature — normal Drizzle queries are already parameterised.
        """,
        a_bn=r"""
            Prepared statement হলো placeholder সহ **একবার** বানানো query, যেটা বিভিন্ন value দিয়ে বারবার execute হয়:

            `const userById = db.select().from(users).where(eq(users.id, sql.placeholder('id'))).prepare('user_by_id');` তারপর `await userById.execute({ id: 42 })`।

            দুটো জিনিস দ্রুত হয়:
            - **Node.js-এ:** প্রতিটা call-এ query object আর SQL string আবার বানাতে হয় না।
            - **PostgreSQL-এ:** node-postgres-এ named statement প্রতি connection-এ একবার parse আর plan হয়; পরের execution-এ শুধু parameter bind হয়। Hot path-এ বড়, জটিল query-তে এটাই সবচেয়ে কাজে লাগে।

            এটা performance tool, security feature না — সাধারণ Drizzle query আগে থেকেই parameterised।
        """,
        quick_en=r"""A prepared statement is built once with `sql.placeholder()` and `.prepare()`, then run many times with `.execute({ ... })`. Drizzle skips rebuilding the query, and with node-postgres the server reuses the named statement per connection; it's a performance tool, not a security feature.""",
        quick_bn=r"""Prepared statement একবার `sql.placeholder()` আর `.prepare()` দিয়ে বানানো হয়, তারপর `.execute({ ... })` দিয়ে বারবার চালানো হয়। Drizzle-কে প্রতিবার query নতুন করে বানাতে হয় না, আর node-postgres-এ server প্রতিটা connection-এ named statement reuse করে; এটা performance-এর tool, security-র নয়।""",
        ex_en=r"""
            - **Per connection:** prepared statements live in a single PostgreSQL session. With a pool, each connection prepares the statement the first time it runs it there.
            - **Unique names:** two different queries prepared with the same name on one connection conflict. Use descriptive, unique names.
            - **Poolers:** PgBouncer in transaction mode hands each transaction to any server connection, so named statements can "disappear" — disable prepares (postgres.js `prepare: false`) or use a pooler version/configuration that supports protocol-level prepared statements.
            - **Generic plans:** after several executions PostgreSQL may switch to a generic plan that ignores the actual parameter values. On skewed data (one huge tenant) that plan can be worse; `plan_cache_mode` controls this.
            - **When it's not worth it:** simple primary-key lookups barely benefit; measure before sprinkling `.prepare()` everywhere.
        """,
        ex_bn=r"""
            - **Connection অনুযায়ী:** prepared statement একটা PostgreSQL session-এই থাকে। Pool থাকলে প্রতিটা connection প্রথমবার চালানোর সময় statement prepare করে।
            - **Unique নাম:** এক connection-এ একই নামে দুটো আলাদা query prepare করলে conflict হয়। বর্ণনামূলক, unique নাম দাও।
            - **Pooler:** transaction mode-এ PgBouncer প্রতিটা transaction যেকোনো server connection-এ দেয়, তাই named statement "হারিয়ে" যেতে পারে — prepare বন্ধ করো (postgres.js `prepare: false`) অথবা এমন pooler version/configuration ব্যবহার করো যা protocol-level prepared statement support করে।
            - **Generic plan:** কয়েকবার execute হওয়ার পর PostgreSQL একটা generic plan-এ চলে যেতে পারে যা আসল parameter value উপেক্ষা করে। Skewed data-য় (একটা বিশাল tenant) সেই plan খারাপ হতে পারে; `plan_cache_mode` এটা নিয়ন্ত্রণ করে।
            - **কখন লাভ নেই:** সাধারণ primary-key lookup-এ লাভ সামান্য; সব জায়গায় `.prepare()` ছড়ানোর আগে মেপে দেখো।
        """,
        tip_en=r"""Separate the two speed-ups (JS-side building vs DB-side parsing/planning) and state clearly that it's not about SQL injection. Then raise the PgBouncer caveat — it's the most common production surprise.""",
        tip_bn=r"""দুই ধরনের speed-up আলাদা করো (JS-এ query বানানো বনাম DB-তে parse/plan), আর স্পষ্ট বলো এটা SQL injection নিয়ে না। তারপর PgBouncer-এর সতর্কতা তোলো — production-এ এটাই সবচেয়ে common চমক।""",
        mist_en=r"""Thinking prepared statements are needed to prevent SQL injection in Drizzle; reusing the same name for different queries; using named statements behind a transaction-mode pooler.""",
        mist_bn=r"""ভাবা যে Drizzle-এ SQL injection আটকাতে prepared statement লাগে; আলাদা query-তে একই নাম আবার ব্যবহার করা; transaction-mode pooler-এর পেছনে named statement ব্যবহার করা।""",
        code=r"""
            import { eq, sql } from 'drizzle-orm';

            // Built once at module load
            const userById = db
              .select()
              .from(users)
              .where(eq(users.id, sql.placeholder('id')))
              .prepare('user_by_id');

            const postsByAuthor = db
              .select({ id: posts.id, title: posts.title })
              .from(posts)
              .where(eq(posts.authorId, sql.placeholder('authorId')))
              .limit(sql.placeholder('limit'))
              .prepare('posts_by_author');

            // Executed many times with different values
            const [user] = await userById.execute({ id: 42 });
            const latest = await postsByAuthor.execute({ authorId: 42, limit: 10 });
        """,
        lang="typescript",
        follow=[
            ("Why might a prepared statement get a worse plan than an ad-hoc query?", "কেন একটা prepared statement ad-hoc query-র চেয়ে খারাপ plan পেতে পারে?"),
            ("How do prepared statements interact with PgBouncer?", "PgBouncer-এর সাথে prepared statement কীভাবে কাজ করে?"),
        ],
        related=["drizzle-024", "drizzle-009"],
        refs=[D_PERF_QUERIES],
    ),
    # ------------------------------------------------------------------ drizzle-022
    Q(
        id="drizzle-022", sub="Type-safe Dynamic Queries", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["dynamic-queries", "pagination", "keyset", "filters", "dynamic"],
        ver="Drizzle ORM 0.45.x", vs=False, status="stable",
        q_en=r"""
            Implement `listPosts(filters)` for `GET /posts` with optional filters — `search` (case-insensitive title match), `authorId`, `publishedOnly` — and **cursor (keyset) pagination** by `id` descending with a `limit` capped at 100. Return `{ items, nextCursor }`, where each item has `id`, `title` and the author's name.

            Example: with posts 3, 2, 1 and `limit: 2`, the first call returns ids `[3, 2]` with `nextCursor: 2`; calling again with `cursor: 2` returns `[1]` with `nextCursor: null`.
        """,
        q_bn=r"""
            `GET /posts`-এর জন্য `listPosts(filters)` implement করো, optional filter সহ — `search` (title-এ case-insensitive match), `authorId`, `publishedOnly` — আর `id` descending অনুযায়ী **cursor (keyset) pagination**, `limit` সর্বোচ্চ 100। Return করবে `{ items, nextCursor }`, প্রতিটা item-এ `id`, `title` আর author-এর নাম।

            উদাহরণ: post 3, 2, 1 আর `limit: 2` হলে প্রথম call দেয় id `[3, 2]` আর `nextCursor: 2`; `cursor: 2` দিয়ে আবার call করলে দেয় `[1]` আর `nextCursor: null`।
        """,
        a_en=r"""
            - Collect conditions in an array of `SQL` filters and pass them with `and(...filters)`. Drizzle ignores `undefined`, and `and()` with no arguments produces no `WHERE` at all — so optional filters need no `if/else` query copies.
            - Values go through `ilike`/`eq`/`lt`, so they're bound parameters — safe for user input.
            - **Keyset pagination:** `WHERE id < cursor ORDER BY id DESC LIMIT limit + 1`. Fetching one extra row tells me whether there's a next page without a `COUNT(*)`.
            - A partial `select({...})` with an `innerJoin` returns exactly the fields the API needs, fully typed.
            - Clamp `limit` server-side so clients can't request 100,000 rows.

            For reusable building blocks (e.g. a generic `withPagination(qb)` helper), Drizzle's `.$dynamic()` lets you pass a query builder into functions and keep chaining.
        """,
        a_bn=r"""
            - শর্তগুলো `SQL` filter-এর একটা array-তে জমা করো আর `and(...filters)` দিয়ে দাও। Drizzle `undefined` উপেক্ষা করে, আর argument ছাড়া `and()` কোনো `WHERE`-ই তৈরি করে না — তাই optional filter-এর জন্য `if/else` দিয়ে query-র কপি লাগে না।
            - Value যায় `ilike`/`eq`/`lt` দিয়ে, তাই bound parameter হয় — user input-এর জন্য নিরাপদ।
            - **Keyset pagination:** `WHERE id < cursor ORDER BY id DESC LIMIT limit + 1`। একটা বাড়তি row আনলেই বোঝা যায় পরের page আছে কি না, `COUNT(*)` লাগে না।
            - `innerJoin` সহ partial `select({...})` API-র ঠিক যে field লাগে সেগুলোই দেয়, পুরোপুরি typed।
            - Server-side-এ `limit` সীমিত করো, যাতে client ১,০০,০০০ row চাইতে না পারে।

            Reusable building block-এর জন্য (যেমন একটা generic `withPagination(qb)` helper), Drizzle-এর `.$dynamic()` query builder-কে function-এ pass করে chain চালিয়ে যেতে দেয়।
        """,
        quick_en=r"""Collect optional `SQL` filters in an array and pass `and(...filters)`, since `undefined` is ignored. Paginate with `WHERE id < cursor ORDER BY id DESC LIMIT limit + 1`, using the extra row to set `nextCursor`, select only the needed fields with an `innerJoin`, and cap `limit` at 100.""",
        quick_bn=r"""Optional `SQL` filter-গুলো একটা array-তে জমিয়ে `and(...filters)` দিই, কারণ `undefined` ignore হয়। Pagination করি `WHERE id < cursor ORDER BY id DESC LIMIT limit + 1` দিয়ে — বাড়তি row-টা দেখে `nextCursor` ঠিক করি, `innerJoin`-সহ শুধু দরকারি field select করি, আর `limit` 100-এ আটকে রাখি।""",
        ex_en=r"""
            - **Why keyset over OFFSET:** `OFFSET 100000` makes PostgreSQL read and discard 100k rows, and results shift when new posts arrive. Keyset uses the index on `id` and stays fast at any depth.
            - **Sorting by non-unique columns** (e.g. `publishedAt`) needs a tie-breaker: cursor on `(published_at, id)` and compare both columns.
            - **Search performance:** `ilike '%term%'` can't use a B-tree index; for real search use `pg_trgm` or full-text search (`to_tsvector`) via the `sql` tag.
            - **`$dynamic()`** exists because builders are strongly typed: without it, calling `.limit()` inside a generic helper would fail type-checking. Verified: `withPagination(db.select().from(posts).orderBy(asc(posts.id)).$dynamic(), 2, 2)` returns page 2.
            - Validate and coerce query params (zod or a framework pipe) before they reach `listPosts`.
        """,
        ex_bn=r"""
            - **OFFSET-এর বদলে keyset কেন:** `OFFSET 100000` দিলে PostgreSQL ১,০০,০০০ row পড়ে ফেলে দেয়, আর নতুন post এলে result সরে যায়। Keyset `id`-এর index ব্যবহার করে, যেকোনো গভীরতায় দ্রুত থাকে।
            - **Non-unique column-এ sort** (যেমন `publishedAt`) করলে tie-breaker লাগে: `(published_at, id)`-এর উপর cursor, আর দুটো column-ই compare করো।
            - **Search performance:** `ilike '%term%'` B-tree index ব্যবহার করতে পারে না; আসল search-এর জন্য `sql` tag দিয়ে `pg_trgm` বা full-text search (`to_tsvector`) ব্যবহার করো।
            - **`$dynamic()`** আছে কারণ builder কড়াভাবে typed: এটা ছাড়া generic helper-এর ভেতরে `.limit()` call করলে type-check fail করত। যাচাই করা: `withPagination(db.select().from(posts).orderBy(asc(posts.id)).$dynamic(), 2, 2)` page 2 দেয়।
            - `listPosts`-এ পৌঁছানোর আগে query param validate আর coerce করো (zod বা framework pipe দিয়ে)।
        """,
        tip_en=r"""Mention three things explicitly: optional filters via an array + `and()`, the `limit + 1` trick, and why keyset beats OFFSET. That's a complete, production-ready answer.""",
        tip_bn=r"""তিনটা জিনিস স্পষ্ট বলো: array + `and()` দিয়ে optional filter, `limit + 1` কৌশল, আর keyset কেন OFFSET-এর চেয়ে ভালো। এটাই একটা সম্পূর্ণ, production-ready উত্তর।""",
        mist_en=r"""Building different query strings per filter combination; OFFSET pagination on large tables; trusting the client's `limit`; sorting without a unique tie-breaker so pages skip or repeat rows.""",
        mist_bn=r"""প্রতিটা filter combination-এর জন্য আলাদা query string বানানো; বড় table-এ OFFSET pagination; client-এর `limit` বিশ্বাস করা; unique tie-breaker ছাড়া sort করা, ফলে page-এ row বাদ পড়ে বা repeat হয়।""",
        code=r"""
            import { and, asc, desc, eq, ilike, lt, type SQL } from 'drizzle-orm';
            import type { PgSelect } from 'drizzle-orm/pg-core';

            interface PostFilters {
              search?: string;
              authorId?: number;
              publishedOnly?: boolean;
              cursor?: number;
              limit?: number;
            }

            export async function listPosts(f: PostFilters) {
              const filters: SQL[] = [];
              if (f.search) filters.push(ilike(posts.title, `%${f.search}%`));
              if (f.authorId) filters.push(eq(posts.authorId, f.authorId));
              if (f.publishedOnly) filters.push(eq(posts.published, true));
              if (f.cursor) filters.push(lt(posts.id, f.cursor));
              const limit = Math.min(f.limit ?? 20, 100);

              const rows = await db
                .select({ id: posts.id, title: posts.title, author: users.name })
                .from(posts)
                .innerJoin(users, eq(users.id, posts.authorId))
                .where(and(...filters))
                .orderBy(desc(posts.id))
                .limit(limit + 1); // one extra row = "there is a next page"

              const hasMore = rows.length > limit;
              const items = hasMore ? rows.slice(0, limit) : rows;
              return { items, nextCursor: hasMore ? items[items.length - 1].id : null };
            }

            // Reusable helper with $dynamic()
            export function withPagination<T extends PgSelect>(qb: T, page: number, pageSize: number) {
              return qb.limit(pageSize).offset((page - 1) * pageSize);
            }
            const page2 = await withPagination(db.select().from(posts).orderBy(asc(posts.id)).$dynamic(), 2, 20);
        """,
        lang="typescript",
        output=r"""
            listPosts({ limit: 2 })            -> { items: [ {id: 3, ...}, {id: 2, ...} ], nextCursor: 2 }
            listPosts({ limit: 2, cursor: 2 }) -> { items: [ {id: 1, ...} ], nextCursor: null }
        """,
        time="O(log n + k) with an index on the sort key (k = page size)",
        space="O(k)",
        follow=[
            ("How would you paginate by `publishedAt` when many posts share the same timestamp?", "অনেক post-এর একই timestamp থাকলে `publishedAt` অনুযায়ী কীভাবে paginate করবে?"),
            ("How would you add full-text search with ranking?", "Ranking সহ full-text search কীভাবে যোগ করবে?"),
        ],
        related=["drizzle-004", "drizzle-028"],
        refs=[D_DYNAMIC, D_OPERATORS],
    ),
    # ------------------------------------------------------------------ drizzle-023
    Q(
        id="drizzle-023", sub="Connection Management (Serverless)", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["serverless", "connection-pooling", "lambda", "neon", "pgbouncer"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=True, status="stable",
        q_en=r"""Your Next.js API routes (deployed on a serverless platform) use Drizzle with node-postgres. During a traffic spike, requests start failing with `sorry, too many clients already` / `remaining connection slots are reserved`. What's happening, and how would you fix it?""",
        q_bn=r"""তোমার Next.js API route (serverless platform-এ deploy করা) node-postgres সহ Drizzle ব্যবহার করে। Traffic spike-এর সময় request গুলো `sorry, too many clients already` / `remaining connection slots are reserved` দিয়ে fail করতে শুরু করে। কী হচ্ছে, আর কীভাবে ঠিক করবে?""",
        a_en=r"""
            **What's happening:** each serverless instance runs its own Node process with its own pool. During a spike the platform starts hundreds of instances; each opens up to `max` connections (default 10 for `pg`). 200 instances × 10 = 2,000 connections against a database that allows maybe 100. Instances also freeze without closing sockets, so idle connections linger.

            **Fixes, in order:**
            1. **Create `db` at module scope**, not inside the handler, so warm invocations reuse it; in Next.js dev, cache it on `globalThis` to survive hot reloads.
            2. **Cap the pool per instance** at 1–2 connections with a short idle timeout.
            3. **Put a pooler in front of PostgreSQL:** PgBouncer, RDS Proxy (AWS), or the provider's pooled endpoint (Neon, Supabase). Thousands of client connections are multiplexed onto a small number of real ones. With transaction-mode pooling, avoid session state (`SET`, advisory locks, `LISTEN`) and named prepared statements (postgres.js: `prepare: false`).
            4. **Or use an HTTP/WebSocket serverless driver** (e.g. `drizzle-orm/neon-http`): no long-lived TCP connections at all. Trade-off: the HTTP driver doesn't support interactive transactions (Drizzle throws "No transactions support in neon-http driver"); use `db.batch([...])` for atomic multi-statement writes, or the WebSocket driver when you need `db.transaction()`.
            5. **Edge runtimes** can't open raw TCP sockets — they need an HTTP/WebSocket driver.
        """,
        a_bn=r"""
            **কী হচ্ছে:** প্রতিটা serverless instance নিজের Node process আর নিজের pool নিয়ে চলে। Spike-এর সময় platform শত শত instance চালু করে; প্রত্যেকে সর্বোচ্চ `max`টা connection খোলে (`pg`-এর default 10)। ২০০ instance × ১০ = ২,০০০ connection, অথচ database হয়তো ১০০টা allow করে। Instance socket বন্ধ না করেই freeze হয়ে যায়, তাই idle connection-ও ঝুলে থাকে।

            **সমাধান, ক্রম অনুযায়ী:**
            1. Handler-এর ভেতরে না, **module scope-এ `db` তৈরি করো**, যাতে warm invocation reuse করে; Next.js dev-এ hot reload টিকে থাকতে `globalThis`-এ cache করো।
            2. **প্রতি instance-এ pool সীমিত করো** ১–২টা connection-এ, ছোট idle timeout সহ।
            3. **PostgreSQL-এর সামনে একটা pooler দাও:** PgBouncer, RDS Proxy (AWS), বা provider-এর pooled endpoint (Neon, Supabase)। হাজার হাজার client connection অল্প কয়েকটা আসল connection-এ multiplex হয়। Transaction-mode pooling-এ session state (`SET`, advisory lock, `LISTEN`) আর named prepared statement এড়াও (postgres.js: `prepare: false`)।
            4. **অথবা HTTP/WebSocket serverless driver ব্যবহার করো** (যেমন `drizzle-orm/neon-http`): দীর্ঘস্থায়ী TCP connection-ই নেই। Trade-off: HTTP driver interactive transaction support করে না (Drizzle throw করে "No transactions support in neon-http driver"); atomic multi-statement write-এর জন্য `db.batch([...])`, আর `db.transaction()` লাগলে WebSocket driver ব্যবহার করো।
            5. **Edge runtime** raw TCP socket খুলতে পারে না — HTTP/WebSocket driver লাগে।
        """,
        quick_en=r"""Every serverless instance opens its own pool, so a spike multiplies connections past PostgreSQL's limit. Create `db` at module scope, cap each pool at 1–2 connections and put a pooler (PgBouncer, RDS Proxy or a pooled endpoint) in front, or use an HTTP driver, which can't run interactive transactions.""",
        quick_bn=r"""প্রতিটা serverless instance নিজের pool খোলে, তাই traffic spike-এ connection সংখ্যা PostgreSQL-এর limit ছাড়িয়ে যায়। `db` module scope-এ বানাই, প্রতি pool-এ 1–2 connection রাখি আর সামনে pooler (PgBouncer, RDS Proxy বা pooled endpoint) বসাই, অথবা HTTP driver নিই — যদিও সেটা interactive transaction চালাতে পারে না।""",
        ex_en=r"""
            - **Capacity math:** max concurrent instances × pool size must stay below what the pooler/database accepts, with headroom for migrations, admin tools and replicas.
            - **Timeouts:** set `connectionTimeoutMillis` so requests fail fast instead of hanging when the pool is exhausted, and `statement_timeout` on the database role so runaway queries don't hold connections.
            - **Long-lived servers are different:** a NestJS/Express container keeps one pool for its lifetime; the serverless problem is the *number of processes*, not the pool itself.
            - **Observability:** watch `pg_stat_activity` (connections by state), pooler stats, and the platform's concurrency metrics during spikes.
            - Keep migrations out of the request path entirely — never run `migrate()` on cold start.
        """,
        ex_bn=r"""
            - **Capacity-র হিসাব:** সর্বোচ্চ concurrent instance × pool size অবশ্যই pooler/database যা নেয় তার নিচে থাকবে, migration, admin tool আর replica-র জন্য জায়গা রেখে।
            - **Timeout:** `connectionTimeoutMillis` দাও, যাতে pool শেষ হলে request ঝুলে না থেকে দ্রুত fail করে, আর database role-এ `statement_timeout`, যাতে অনিয়ন্ত্রিত query connection আটকে না রাখে।
            - **দীর্ঘস্থায়ী server আলাদা:** একটা NestJS/Express container সারাজীবন একটা pool রাখে; serverless-এর সমস্যা হলো *process-এর সংখ্যা*, pool নিজে না।
            - **Observability:** spike-এর সময় `pg_stat_activity` (state অনুযায়ী connection), pooler-এর stats আর platform-এর concurrency metric দেখো।
            - Migration-কে request path থেকে পুরোপুরি দূরে রাখো — cold start-এ কখনো `migrate()` চালিও না।
        """,
        tip_en=r"""Start with the multiplication (instances × pool size) — it proves you understand the root cause. Then give layered fixes and the transaction trade-off of HTTP drivers.""",
        tip_bn=r"""গুণটা দিয়ে শুরু করো (instance × pool size) — এতে প্রমাণ হয় তুমি root cause বোঝো। তারপর ধাপে ধাপে সমাধান আর HTTP driver-এর transaction trade-off বলো।""",
        mist_en=r"""Creating the pool inside the request handler; "fixing" it by raising `max_connections` to thousands (each connection costs memory); using session-level features behind a transaction-mode pooler; expecting `db.transaction()` to work on the HTTP driver.""",
        mist_bn=r"""Request handler-এর ভেতরে pool তৈরি করা; `max_connections` হাজারে তুলে "সমাধান" করা (প্রতিটা connection-এ memory খরচ); transaction-mode pooler-এর পেছনে session-level feature ব্যবহার করা; HTTP driver-এ `db.transaction()` কাজ করবে আশা করা।""",
        code=r"""
            // lib/db.ts — serverless (Node.js runtime) with a pooler URL
            import { drizzle, type NodePgDatabase } from 'drizzle-orm/node-postgres';
            import { Pool } from 'pg';
            import * as schema from './schema';

            const globalForDb = globalThis as unknown as { db?: NodePgDatabase<typeof schema> };

            function createDb() {
              const pool = new Pool({
                connectionString: process.env.DATABASE_URL, // pooled endpoint / PgBouncer / RDS Proxy
                max: 1,                                    // one connection per function instance
                idleTimeoutMillis: 5_000,
                connectionTimeoutMillis: 3_000,
              });
              return drizzle({ client: pool, schema });
            }

            export const db = globalForDb.db ?? createDb(); // module scope: reused while the instance is warm
            if (process.env.NODE_ENV !== 'production') globalForDb.db = db; // survive Next.js dev hot reloads

            // Alternative: HTTP driver, no TCP pool (no interactive transactions; use db.batch for atomic writes)
            // import { neon } from '@neondatabase/serverless';
            // import { drizzle } from 'drizzle-orm/neon-http';
            // export const db = drizzle({ client: neon(process.env.DATABASE_URL!), schema });
        """,
        lang="typescript",
        follow=[
            ("What breaks when you put PgBouncer in transaction mode in front of an app?", "App-এর সামনে transaction mode-এ PgBouncer দিলে কী ভাঙে?"),
            ("How would you do an atomic multi-step write with the neon-http driver?", "neon-http driver দিয়ে atomic multi-step write কীভাবে করবে?"),
        ],
        related=["drizzle-003", "drizzle-024", "nest-022"],
        refs=[D_PERF_SERVERLESS, D_NEON],
    ),
    # ------------------------------------------------------------------ drizzle-024
    Q(
        id="drizzle-024", sub="Connection Pooling (PgBouncer)", diff="hard", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["pgbouncer", "transaction-pooling", "postgres-js", "prepared-statements"],
        ver="Drizzle ORM 0.45.x / postgres.js 3 / PgBouncer", vs=True, status="stable",
        q_en=r"""After switching the connection string to a **transaction-mode** pooler (PgBouncer or a provider's pooled endpoint), a Drizzle app using the postgres.js driver intermittently fails with errors like `prepared statement "..." does not exist`. What's the right fix?""",
        q_bn=r"""Connection string **transaction-mode** pooler-এ (PgBouncer বা provider-এর pooled endpoint) বদলানোর পর postgres.js driver ব্যবহার করা একটা Drizzle app মাঝে মাঝে `prepared statement "..." does not exist`-এর মতো error দিয়ে fail করছে। সঠিক সমাধান কী?""",
        options=[
            ("Increase the pooler's `default_pool_size` so each client keeps its own server connection", "Pooler-এর `default_pool_size` বাড়াও, যাতে প্রতিটা client নিজের server connection রাখে"),
            ("Wrap every query in `db.transaction()` so it stays on one connection", "প্রতিটা query `db.transaction()`-এ wrap করো, যাতে এক connection-এ থাকে"),
            ("Switch the tables from identity columns to `serial` ids", "Table গুলো identity column থেকে `serial` id-তে বদলাও"),
            ("Create the client with `postgres(url, { prepare: false })` so the driver stops relying on named prepared statements across pooled connections", "`postgres(url, { prepare: false })` দিয়ে client তৈরি করো, যাতে driver pooled connection জুড়ে named prepared statement-এর উপর নির্ভর না করে"),
        ],
        correct=3,
        a_en=r"""`prepare: false`. In transaction pooling, each transaction may run on a different server connection, but prepared statements belong to the server connection that created them. postgres.js prepares statements by default, so a later execution can land on a connection where that statement doesn't exist.""",
        a_bn=r"""`prepare: false`। Transaction pooling-এ প্রতিটা transaction আলাদা server connection-এ চলতে পারে, কিন্তু prepared statement থাকে যে server connection সেটা বানিয়েছে তার কাছে। postgres.js default-এ statement prepare করে, তাই পরের execution এমন connection-এ পড়তে পারে যেখানে ওই statement নেই।""",
        quick_en=r"""Create the client with `postgres(url, { prepare: false })`. In transaction pooling each transaction can land on a different server connection, but a prepared statement only exists on the connection that created it.""",
        quick_bn=r"""Client বানাই `postgres(url, { prepare: false })` দিয়ে। Transaction pooling-এ প্রতিটা transaction আলাদা server connection-এ যেতে পারে, কিন্তু prepared statement থাকে শুধু যে connection তাকে বানিয়েছে সেখানেই।""",
        ex_en=r"""
            - Option B is tempting: a transaction does stay on one server connection, but only for its duration — the next transaction gets another connection, and wrapping everything adds latency and lock time. It treats the symptom.
            - Option A misunderstands pooling: the point of transaction mode is *sharing* server connections.
            - The same problem hits Drizzle's own `.prepare('name')` with node-postgres (named statements). Plain node-postgres queries use unnamed statements and are fine.
            - Newer PgBouncer versions (1.21+) can track protocol-level prepared statements in transaction mode (`max_prepared_statements`), and some managed poolers support it too — check your pooler before deciding; `prepare: false` is the universally safe setting.
            - Other session-level features also break in transaction mode: `SET` (use `SET LOCAL` / `set_config(..., true)` inside a transaction), advisory locks held across transactions, `LISTEN/NOTIFY`, temporary tables.
        """,
        ex_bn=r"""
            - Option B লোভনীয়: একটা transaction সত্যিই এক server connection-এ থাকে, কিন্তু শুধু তার মেয়াদকালে — পরের transaction অন্য connection পায়, আর সব কিছু wrap করলে latency আর lock time বাড়ে। এটা উপসর্গের চিকিৎসা।
            - Option A pooling ভুল বোঝে: transaction mode-এর উদ্দেশ্যই server connection *share* করা।
            - একই সমস্যা হয় node-postgres-এ Drizzle-এর নিজের `.prepare('name')`-এ (named statement)। সাধারণ node-postgres query unnamed statement ব্যবহার করে, সেগুলো ঠিক আছে।
            - নতুন PgBouncer version (1.21+) transaction mode-এ protocol-level prepared statement track করতে পারে (`max_prepared_statements`), কিছু managed pooler-ও পারে — সিদ্ধান্তের আগে তোমার pooler check করো; `prepare: false` সব জায়গায় নিরাপদ setting।
            - আরও কিছু session-level feature transaction mode-এ ভাঙে: `SET` (transaction-এর ভেতরে `SET LOCAL` / `set_config(..., true)` ব্যবহার করো), transaction পেরিয়ে ধরে রাখা advisory lock, `LISTEN/NOTIFY`, temporary table।
        """,
        tip_en=r"""Explain the root cause in one line: "prepared statements are per server connection; transaction pooling reassigns connections". Then list the other session features that break — that's the senior follow-up.""",
        tip_bn=r"""এক লাইনে root cause বলো: "prepared statement server connection অনুযায়ী থাকে; transaction pooling connection বদলে দেয়"। তারপর আর কোন session feature ভাঙে তার list দাও — এটাই senior-level follow-up।""",
        related=["drizzle-021", "drizzle-023"],
        refs=[D_SUPABASE, D_PERF_QUERIES],
    ),
]

if __name__ == "__main__":
    save("drizzle", "b3", QUESTIONS)
