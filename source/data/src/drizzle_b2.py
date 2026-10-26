# Drizzle ORM — batch 2 (drizzle-009 … drizzle-016): lazy queries, relations vs FKs, raw SQL, constraints,
# joins, relational queries, transactions
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

D_SELECT = ("Drizzle ORM — Select", "https://orm.drizzle.team/docs/select")
D_DELETE = ("Drizzle ORM — Delete", "https://orm.drizzle.team/docs/delete")
D_ESLINT = ("Drizzle ORM — ESLint plugin", "https://orm.drizzle.team/docs/eslint-plugin")
D_RELATIONS = ("Drizzle ORM — Relations (incl. relations vs foreign keys)", "https://orm.drizzle.team/docs/relations")
D_RELATIONS_V1V2 = ("Drizzle ORM — Relational Queries v1 → v2", "https://orm.drizzle.team/docs/relations-v1-v2")
D_INDEXES = ("Drizzle ORM — Indexes & constraints", "https://orm.drizzle.team/docs/indexes-constraints")
D_SQL = ("Drizzle ORM — sql template", "https://orm.drizzle.team/docs/sql")
D_JOINS = ("Drizzle ORM — Joins", "https://orm.drizzle.team/docs/joins")
D_RQB = ("Drizzle ORM — Relational queries", "https://orm.drizzle.team/docs/rqb")
D_TRANSACTIONS = ("Drizzle ORM — Transactions", "https://orm.drizzle.team/docs/transactions")
PG_CONSTRAINTS = ("PostgreSQL docs — Constraints", "https://www.postgresql.org/docs/current/ddl-constraints.html")

QUESTIONS = [
    # ------------------------------------------------------------------ drizzle-009
    Q(
        id="drizzle-009", sub="Query Execution (Debugging)", diff="easy", type="debugging",
        prio="high", market="both", mins=3,
        tags=["await", "lazy-queries", "thenable", "debugging"],
        ver="Drizzle ORM 0.45.x", vs=False, status="stable",
        q_en=r"""A "Log out from all devices" button returns success, the audit log entry is written — but the user's other sessions still work. No error is logged. What's wrong?""",
        q_bn=r"""একটা "সব device থেকে log out" button success দেয়, audit log entry-ও লেখা হয় — কিন্তু user-এর অন্য session গুলো এখনো কাজ করছে। কোনো error log হয়নি। সমস্যাটা কী?""",
        code=r"""
            export async function logoutEverywhere(userId: number) {
              db.delete(sessions).where(eq(sessions.userId, userId));
              await auditLog.record('logout_all', userId);
              return { ok: true };
            }
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                export async function logoutEverywhere(userId: number) {
                  const revoked = await db
                    .delete(sessions)
                    .where(eq(sessions.userId, userId))
                    .returning({ id: sessions.id });

                  await auditLog.record('logout_all', userId, { revoked: revoked.length });
                  return { ok: true, revoked: revoked.length };
                }
            """),
        ],
        a_en=r"""
            The delete is never executed because it isn't awaited. Drizzle query builders are **lazy thenables**: building `db.delete(...).where(...)` only creates an object. The SQL is generated and sent when the builder's `then()` is called — that is, when you `await` it (or call `.execute()`).

            So the function logs success while the sessions stay valid — a real security bug, because a stolen session isn't revoked. Fix: `await` the delete (and use `.returning()` to know how many sessions were revoked).
        """,
        a_bn=r"""
            Delete কখনো execute হয়নি, কারণ এটা await করা হয়নি। Drizzle-এর query builder হলো **lazy thenable**: `db.delete(...).where(...)` বানালে শুধু একটা object তৈরি হয়। SQL তৈরি হয়ে পাঠানো হয় তখনই, যখন builder-এর `then()` call হয় — মানে যখন তুমি `await` করো (বা `.execute()` call করো)।

            তাই function success log করে কিন্তু session গুলো valid থেকে যায় — এটা একটা আসল security bug, কারণ চুরি হওয়া session revoke হয় না। সমাধান: delete-টা `await` করো (আর কয়টা session revoke হলো জানতে `.returning()` ব্যবহার করো)।
        """,
        quick_en=r"""The delete is never awaited, and Drizzle builders are lazy thenables that send SQL only when awaited (or `.execute()` is called), so the other sessions are never revoked. Fix it by awaiting the delete, ideally with `.returning()` to see what was removed.""",
        quick_bn=r"""Delete-টা `await` করা হয়নি, আর Drizzle builder হলো lazy thenable — `await` (বা `.execute()`) না করলে SQL পাঠায়ই না, তাই অন্য session-গুলো revoke হয় না। Fix: delete-টা `await` করো, সম্ভব হলে `.returning()` দিয়ে দেখো কী মুছলো।""",
        ex_en=r"""
            - **Lazy vs eager:** a normal Promise starts work immediately; Drizzle builders don't, because you can keep chaining (`.where()`, `.limit()`, `.prepare()`) before execution. Verified: an un-awaited `db.update(...)` leaves the row unchanged.
            - **Catch it automatically:** enable `@typescript-eslint/no-floating-promises` with `checkThenables: true` — with its default options (typescript-eslint v8) it only checks native Promises, so an un-awaited Drizzle builder is **not** reported (verified). The official `eslint-plugin-drizzle` adds `enforce-delete-with-where` / `enforce-update-with-where`.
            - **Fire-and-forget is still wrong** even if you call `.execute()` without awaiting: errors become unhandled rejections and the response may go out before the write finishes.
            - Tests should assert the **effect** (sessions count is 0), not just the return value — that's how this bug slips through.
        """,
        ex_bn=r"""
            - **Lazy বনাম eager:** সাধারণ Promise সাথে সাথে কাজ শুরু করে; Drizzle builder করে না, কারণ execution-এর আগে আরও chain করা যায় (`.where()`, `.limit()`, `.prepare()`)। যাচাই করা: await না করা `db.update(...)` row অপরিবর্তিত রাখে।
            - **নিজে থেকে ধরো:** `@typescript-eslint/no-floating-promises` চালু করো `checkThenables: true` সহ — default option-এ (typescript-eslint v8) এটা শুধু native Promise check করে, তাই await না করা Drizzle builder report **হয় না** (যাচাই করা)। Official `eslint-plugin-drizzle` যোগ করে `enforce-delete-with-where` / `enforce-update-with-where`।
            - **Fire-and-forget তখনও ভুল**, এমনকি await না করে `.execute()` call করলেও: error unhandled rejection হয়ে যায়, আর write শেষ হওয়ার আগেই response চলে যেতে পারে।
            - Test-এ শুধু return value না, **প্রভাব** assert করো (session count 0) — এভাবেই এই bug ফাঁক দিয়ে বেরিয়ে যায়।
        """,
        tip_en=r"""Name the mechanism ("lazy thenable") and the security impact ("stolen sessions stay valid"). Then propose the lint rule — prevention is what makes a strong debugging answer.""",
        tip_bn=r"""Mechanism-এর নাম বলো ("lazy thenable") আর security প্রভাব বলো ("চুরি হওয়া session valid থাকে")। তারপর lint rule প্রস্তাব করো — প্রতিরোধের কথাই debugging উত্তরকে শক্তিশালী করে।""",
        mist_en=r"""Assuming the query runs as soon as it's built; "fixing" it with `void db.delete(...)` (still never executes); testing only the returned `{ ok: true }`.""",
        mist_bn=r"""ভাবা যে query তৈরি হলেই চলে; `void db.delete(...)` দিয়ে "fix" করা (তখনও execute হয় না); শুধু return করা `{ ok: true }` test করা।""",
        follow=[
            ("Why are Drizzle builders lazy instead of returning a Promise immediately?", "Drizzle builder সাথে সাথে Promise না দিয়ে lazy কেন?"),
            ("How would you run several independent queries in parallel safely?", "কয়েকটা স্বাধীন query নিরাপদে parallel-এ কীভাবে চালাবে?"),
        ],
        related=["drizzle-004", "drizzle-021"],
        refs=[D_DELETE, D_ESLINT],
    ),
    # ------------------------------------------------------------------ drizzle-010
    Q(
        id="drizzle-010", sub="Relations vs Foreign Keys", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["relations", "foreign-keys", "constraints", "rqb"],
        ver="Drizzle ORM 0.45.x (relations() helper; v1 RC uses defineRelations)", vs=True, status="stable",
        q_en=r"""In Drizzle, what's the difference between a foreign key (`.references()`) and a relation (`relations()`)? Do you need both?""",
        q_bn=r"""Drizzle-এ foreign key (`.references()`) আর relation (`relations()`)-এর পার্থক্য কী? দুটোই কি লাগে?""",
        a_en=r"""
            - A **foreign key** is a **database constraint**. `.references(() => users.id, { onDelete: 'cascade' })` makes Drizzle Kit generate `FOREIGN KEY ... REFERENCES ...`, and PostgreSQL checks it on every insert, update and delete. It guarantees integrity even for writes that don't come from your app.
            - A **relation** is **application-level metadata** for Drizzle's relational query API. `relations()` tells Drizzle how tables connect so `db.query.users.findMany({ with: { posts: true } })` can build nested results. It generates no SQL in migrations and creates no constraint.

            They're independent: you can have FKs without relations (if you only use joins) or relations without FKs (legacy tables, cross-database links). In most apps I use **both** — FKs for integrity, relations for convenient nested queries.
        """,
        a_bn=r"""
            - **Foreign key** হলো একটা **database constraint**। `.references(() => users.id, { onDelete: 'cascade' })` দিলে Drizzle Kit `FOREIGN KEY ... REFERENCES ...` generate করে, আর PostgreSQL প্রতিটা insert, update আর delete-এ এটা check করে। App থেকে না আসা write-এর ক্ষেত্রেও integrity নিশ্চিত করে।
            - **Relation** হলো Drizzle-এর relational query API-র জন্য **application-level metadata**। `relations()` Drizzle-কে জানায় table গুলো কীভাবে যুক্ত, যাতে `db.query.users.findMany({ with: { posts: true } })` nested result বানাতে পারে। Migration-এ কোনো SQL তৈরি করে না, কোনো constraint-ও না।

            দুটো স্বাধীন: relation ছাড়াও FK থাকতে পারে (শুধু join ব্যবহার করলে), আবার FK ছাড়াও relation থাকতে পারে (legacy table, cross-database link)। বেশিরভাগ app-এ আমি **দুটোই** ব্যবহার করি — integrity-র জন্য FK, সুবিধাজনক nested query-র জন্য relation।
        """,
        quick_en=r"""A foreign key (`.references()`) is a database constraint that PostgreSQL enforces on every write; `relations()` is app-level metadata that only powers nested `db.query` results and generates no SQL. They're independent, and most apps use both.""",
        quick_bn=r"""Foreign key (`.references()`) হলো database constraint, যেটা PostgreSQL প্রতিটা write-এ check করে; `relations()` হলো app-level metadata, যেটা শুধু `db.query`-এর nested result-এর কাজে লাগে আর কোনো SQL তৈরি করে না। দুটো স্বাধীন, আর বেশিরভাগ app-এ দুটোই ব্যবহার করি।""",
        ex_en=r"""
            - **Without an FK**, a relation happily "works" while the database fills with orphan rows (posts whose author was deleted). Relations don't protect data.
            - **`onDelete` choices:** `cascade` (delete children), `restrict`/`no action` (block the delete), `set null` (keep child, clear link). Pick per business rule — cascading deletes on orders or payments are usually a bad idea.
            - **Indexes:** PostgreSQL does **not** index foreign-key columns automatically. Add an index on `posts.author_id` or joins and cascades get slow.
            - **v1 RC (preview):** `relations()` is replaced by a single `defineRelations()` call with `r.one.users({ from, to })` / `r.many.posts()`; the FK-vs-relation distinction stays the same.
        """,
        ex_bn=r"""
            - **FK ছাড়া** relation দিব্যি "কাজ করে", অথচ database-এ orphan row জমতে থাকে (যেসব post-এর author delete হয়ে গেছে)। Relation data রক্ষা করে না।
            - **`onDelete`-এর বিকল্প:** `cascade` (child delete), `restrict`/`no action` (delete আটকানো), `set null` (child রেখে link মুছে দেওয়া)। Business rule অনুযায়ী বেছে নাও — order বা payment-এ cascading delete সাধারণত খারাপ ধারণা।
            - **Index:** PostgreSQL foreign-key column নিজে থেকে index **করে না**। `posts.author_id`-এ index দাও, নাহলে join আর cascade ধীর হয়।
            - **v1 RC (preview):** `relations()`-এর জায়গায় আসছে একটাই `defineRelations()` call, `r.one.users({ from, to })` / `r.many.posts()` দিয়ে; FK আর relation-এর পার্থক্য একই থাকছে।
        """,
        tip_en=r"""Answer with one sentence each: "FK = enforced by PostgreSQL; relation = Drizzle metadata for `with`". Then add the "PostgreSQL doesn't index FKs" tip — it's a frequent production issue.""",
        tip_bn=r"""এক বাক্য করে বলো: "FK = PostgreSQL enforce করে; relation = `with`-এর জন্য Drizzle metadata"। তারপর "PostgreSQL FK-তে index দেয় না" tip-টা যোগ করো — production-এ এটা প্রায়ই সমস্যা করে।""",
        mist_en=r"""Thinking `relations()` creates foreign keys; skipping FKs because "the ORM handles relations"; forgetting to index FK columns.""",
        mist_bn=r"""ভাবা যে `relations()` foreign key তৈরি করে; "ORM তো relation সামলায়" ভেবে FK বাদ দেওয়া; FK column-এ index দিতে ভুলে যাওয়া।""",
        code=r"""
            import { relations } from 'drizzle-orm';
            import { integer, pgTable, text } from 'drizzle-orm/pg-core';

            export const posts = pgTable('posts', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              // Foreign key: a real constraint in PostgreSQL (appears in generated SQL)
              authorId: integer('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
              title: text().notNull(),
            });

            // Relations: Drizzle-only metadata for db.query.* (no SQL, no constraint)
            export const usersRelations = relations(users, ({ many }) => ({
              posts: many(posts),
            }));

            export const postsRelations = relations(posts, ({ one }) => ({
              author: one(users, { fields: [posts.authorId], references: [users.id] }),
            }));
        """,
        lang="typescript",
        follow=[
            ("When would you deliberately skip a foreign key?", "কখন ইচ্ছা করে foreign key বাদ দেবে?"),
            ("Which `onDelete` behaviour would you choose for orders → order_items, and why?", "orders → order_items-এর জন্য কোন `onDelete` behaviour বেছে নেবে, আর কেন?"),
        ],
        related=["drizzle-012", "drizzle-014"],
        refs=[D_RELATIONS, D_RELATIONS_V1V2],
    ),
    # ------------------------------------------------------------------ drizzle-011
    Q(
        id="drizzle-011", sub="Drizzle vs Raw SQL", diff="easy", type="comparison",
        prio="medium", market="both", mins=4,
        tags=["raw-sql", "sql-template", "query-builder", "type-safety"],
        ver="Drizzle ORM 0.45.x / pg 8", vs=False, status="stable",
        q_en=r"""Compare writing queries with raw SQL through the `pg` driver, Drizzle's query builder, and Drizzle's `sql` template tag. When would you use each?""",
        q_bn=r"""`pg` driver দিয়ে raw SQL, Drizzle-এর query builder, আর Drizzle-এর `sql` template tag — এই তিনভাবে query লেখার তুলনা করো। কখন কোনটা ব্যবহার করবে?""",
        a_en=r"""
            - **Raw SQL with `pg`:** full control and zero abstraction, but results are untyped (`any[]`), column renames aren't caught at compile time, and building dynamic queries means string assembly — easy to get wrong.
            - **Drizzle query builder:** still reads like SQL, but every column is typed, results are inferred, filters compose as values (`and(...conditions)`), and parameters are bound automatically. My default for CRUD and dynamic filters.
            - **`sql` template inside Drizzle:** the escape hatch for what the builder doesn't model — `to_char`, window functions, PostgreSQL-specific operators. Interpolated values are still bound parameters, interpolated columns are typed references, and `sql<T>` gives the result a type.

            So: builder by default, `sql` fragments for special expressions, and fully raw queries (`db.execute(sql...)`) for complex reports — all through the same connection and transactions.
        """,
        a_bn=r"""
            - **`pg` দিয়ে raw SQL:** পুরো control, কোনো abstraction নেই, কিন্তু result untyped (`any[]`), column rename compile-time-এ ধরা পড়ে না, আর dynamic query বানাতে string জোড়া লাগাতে হয় — ভুল হওয়া সহজ।
            - **Drizzle query builder:** দেখতে এখনো SQL-এর মতো, কিন্তু প্রতিটা column typed, result infer হয়, filter value হিসেবে compose হয় (`and(...conditions)`), আর parameter নিজে থেকেই bind হয়। CRUD আর dynamic filter-এর জন্য আমার default।
            - **Drizzle-এর ভেতরে `sql` template:** builder যা model করে না তার জন্য escape hatch — `to_char`, window function, PostgreSQL-specific operator। Interpolate করা value তখনও bound parameter, interpolate করা column typed reference, আর `sql<T>` result-কে type দেয়।

            তাই: default-এ builder, বিশেষ expression-এর জন্য `sql` fragment, আর জটিল report-এর জন্য পুরো raw query (`db.execute(sql...)`) — সবই একই connection আর transaction দিয়ে।
        """,
        quick_en=r"""Raw SQL through `pg` gives full control but untyped results and string-built dynamic queries; Drizzle's builder is typed, composable and parameterised; the `sql` tag is the escape hatch for expressions the builder lacks, still with bound parameters. Use the builder by default and `sql` for the special cases.""",
        quick_bn=r"""`pg` দিয়ে raw SQL-এ পুরো control থাকে, কিন্তু result untyped আর dynamic query string জোড়া দিয়ে বানাতে হয়; Drizzle-এর builder typed, composable আর parameterised; `sql` tag হলো builder যা পারে না তার escape hatch, সেখানেও value bound parameter থাকে। Default হিসেবে builder, বিশেষ ক্ষেত্রে `sql`।""",
        ex_en=r"""
            - **Type of `sql<T>`** is a promise to TypeScript, not a runtime check. If PostgreSQL returns `bigint` as a string, use `.mapWith(Number)` to convert.
            - **`db.execute()` results** are driver-specific: with node-postgres you read `result.rows`.
            - **Readability:** for a 60-line analytics query with CTEs and window functions, plain SQL (in a `.sql` file or a `sql` block) is often clearer than a deeply nested builder chain. Drizzle also supports CTEs (`db.$with(...)`) when you want to stay in the builder.
            - **Safety rule:** never build SQL strings with `+` or `sql.raw()` from user input; keep values as interpolations in the `sql` tag.
        """,
        ex_bn=r"""
            - **`sql<T>`-এর type** TypeScript-কে দেওয়া একটা প্রতিশ্রুতি, runtime check না। PostgreSQL যদি `bigint` string হিসেবে দেয়, convert করতে `.mapWith(Number)` ব্যবহার করো।
            - **`db.execute()`-এর result** driver অনুযায়ী আলাদা: node-postgres-এ `result.rows` পড়তে হয়।
            - **Readability:** CTE আর window function সহ ৬০ লাইনের analytics query-র জন্য অনেক সময় গভীরভাবে nested builder chain-এর চেয়ে plain SQL (`.sql` file-এ বা `sql` block-এ) বেশি পরিষ্কার। Builder-এ থাকতে চাইলে Drizzle CTE-ও support করে (`db.$with(...)`)।
            - **Safety rule:** user input থেকে `+` বা `sql.raw()` দিয়ে কখনো SQL string বানিও না; value-কে `sql` tag-এর interpolation হিসেবেই রাখো।
        """,
        tip_en=r"""Show you're not dogmatic: "ORM for the 90% CRUD, SQL for the 10% that needs it, both safely parameterised." That balance is what interviewers look for.""",
        tip_bn=r"""দেখাও তুমি গোঁড়া না: "৯০% CRUD-এর জন্য ORM, যে ১০%-এ দরকার সেখানে SQL, দুটোই নিরাপদে parameterised।" Interviewer এই ভারসাম্যই খোঁজে।""",
        mist_en=r"""Believing an ORM means you can't write SQL; trusting `sql<number>` without `.mapWith(Number)` for bigint results; concatenating strings for dynamic filters in raw `pg` code.""",
        mist_bn=r"""ভাবা যে ORM ব্যবহার করলে SQL লেখা যায় না; bigint result-এর জন্য `.mapWith(Number)` ছাড়া `sql<number>`-এর উপর ভরসা করা; raw `pg` code-এ dynamic filter-এর জন্য string জোড়া লাগানো।""",
        code=r"""
            // 1) Raw SQL with node-postgres: full control, untyped result
            const { rows } = await pool.query('select id, email from users where role = $1 order by id', ['admin']);
            //      ^? any[]

            // 2) Drizzle query builder: typed and composable
            const admins = await db
              .select({ id: users.id, email: users.email })
              .from(users)
              .where(eq(users.role, 'admin'))
              .orderBy(users.id);
            //      ^? { id: number; email: string }[]

            // 3) sql template for expressions the builder doesn't model
            const month = sql<string>`to_char(${users.createdAt}, 'YYYY-MM')`;
            const signups = await db
              .select({ month, signups: count() })
              .from(users)
              .groupBy(month)
              .orderBy(month);
            // -> [ { month: '2026-08', signups: 2 }, { month: '2026-09', signups: 1 } ]

            // Fully raw query through Drizzle (same pool, still parameterised)
            const result = await db.execute<{ id: number; email: string }>(
              sql`select id, email from ${users} where ${users.role} = ${'admin'}`,
            );
            console.log(result.rows);
        """,
        lang="typescript",
        follow=[
            ("How would you write a window-function query (e.g. rank orders per customer) with Drizzle?", "Drizzle দিয়ে window-function query (যেমন customer প্রতি order rank) কীভাবে লিখবে?"),
            ("When is an ORM the wrong tool entirely?", "কখন ORM পুরোপুরি ভুল tool?"),
        ],
        related=["drizzle-001", "drizzle-008", "drizzle-031"],
        refs=[D_SQL, D_SELECT],
    ),
    # ------------------------------------------------------------------ drizzle-012
    Q(
        id="drizzle-012", sub="Tables, Constraints & Indexes", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["foreign-keys", "indexes", "unique", "many-to-many", "partial-index"],
        ver="Drizzle ORM 0.45.x / drizzle-kit 0.31", vs=True, status="stable",
        q_en=r"""
            Extend the `users` schema for a blog:

            - `posts` belong to a user; deleting a user deletes their posts.
            - A post `slug` must be unique **per author** (two authors may use the same slug).
            - Listing an author's posts must be fast; listing recently published posts must be fast too.
            - `tags` with a unique `name`, and a many-to-many `post_tags` table. Deleting a tag that is still used must **fail**.
        """,
        q_bn=r"""
            একটা blog-এর জন্য `users` schema বাড়াও:

            - `posts` একজন user-এর; user delete করলে তার post-ও delete হবে।
            - Post-এর `slug` **প্রতি author-এ** unique হবে (দুজন author একই slug ব্যবহার করতে পারে)।
            - একজন author-এর post list দ্রুত হতে হবে; সম্প্রতি published post-এর list-ও দ্রুত হতে হবে।
            - Unique `name` সহ `tags`, আর একটা many-to-many `post_tags` table। ব্যবহৃত tag delete করতে গেলে **fail** করতে হবে।
        """,
        a_en=r"""
            - **FK with cascade:** `authorId: integer('author_id').notNull().references(() => users.id, { onDelete: 'cascade' })`.
            - **Per-author uniqueness:** a composite unique index in the table's third argument: `uniqueIndex('posts_author_slug_uq').on(t.authorId, t.slug)`.
            - **Fast author listing:** an index on `author_id` — PostgreSQL doesn't create one for FKs. (The composite unique index starting with `author_id` can also serve this; I keep an explicit one when queries filter only by author and sort differently.)
            - **Recent published posts:** a **partial index** on `published_at` with a `.where(...)` condition (`published = true`) — smaller and faster because unpublished rows are excluded.
            - **Many-to-many:** `post_tags` with a composite primary key `primaryKey({ columns: [t.postId, t.tagId] })`, `cascade` from posts and `restrict` from tags so a used tag can't be deleted.

            The third argument of `pgTable` returns an **array** of indexes/constraints (the current form; the older object form is deprecated).
        """,
        a_bn=r"""
            - **Cascade সহ FK:** `authorId: integer('author_id').notNull().references(() => users.id, { onDelete: 'cascade' })`।
            - **Author অনুযায়ী unique:** table-এর তৃতীয় argument-এ composite unique index: `uniqueIndex('posts_author_slug_uq').on(t.authorId, t.slug)`।
            - **Author-এর list দ্রুত:** `author_id`-এর উপর index — PostgreSQL FK-এর জন্য নিজে index বানায় না। (`author_id` দিয়ে শুরু হওয়া composite unique index-ও এই কাজ করতে পারে; query যখন শুধু author দিয়ে filter করে আর অন্যভাবে sort করে, তখন আমি আলাদা একটা index রাখি।)
            - **সম্প্রতি published post:** `published_at`-এর উপর একটা **partial index**, `.where(...)` সহ — unpublished row বাদ যায় বলে ছোট আর দ্রুত।
            - **Many-to-many:** composite primary key `primaryKey({ columns: [t.postId, t.tagId] })` সহ `post_tags`; post থেকে `cascade` আর tag থেকে `restrict`, যাতে ব্যবহৃত tag delete না করা যায়।

            `pgTable`-এর তৃতীয় argument index/constraint-এর একটা **array** return করে (এখনকার রূপ; পুরোনো object রূপ deprecated)।
        """,
        quick_en=r"""Use an `authorId` FK with `onDelete: 'cascade'`, a composite `uniqueIndex` on `(authorId, slug)`, an index on `author_id` (PostgreSQL doesn't index FKs) and a partial index on `published_at` where `published = true`. `post_tags` gets a composite primary key, cascade from posts and restrict from tags.""",
        quick_bn=r"""`onDelete: 'cascade'`-সহ `authorId` FK, `(authorId, slug)`-এ composite `uniqueIndex`, `author_id`-এ একটা index (PostgreSQL FK-তে নিজে index বানায় না), আর `published = true` শর্তে `published_at`-এ partial index। `post_tags`-এ composite primary key, posts থেকে cascade আর tags থেকে restrict।""",
        ex_en=r"""
            - **Why `restrict` on tags:** the database refuses `DELETE FROM tags` while `post_tags` rows reference it (SQLSTATE `23503`), so the app can show "tag is in use" instead of silently removing it from posts.
            - **Composite index column order matters:** `(author_id, slug)` serves "find by author + slug" and "filter by author", but not "find by slug" alone.
            - **Partial index usage:** the planner only uses it when the query's `WHERE` implies the index predicate (`published = true`).
            - **Constraint names:** naming indexes explicitly (`posts_author_slug_uq`) makes error handling clearer — the PostgreSQL error's `constraint` field tells you which rule was violated.
            - Review the generated SQL (shown in the expected output) in the PR — that's the contract with the database.
        """,
        ex_bn=r"""
            - **Tag-এ কেন `restrict`:** `post_tags`-এর row যতক্ষণ reference করে, database `DELETE FROM tags` প্রত্যাখ্যান করে (SQLSTATE `23503`), ফলে app চুপচাপ post থেকে সরিয়ে না দিয়ে "tag ব্যবহৃত হচ্ছে" দেখাতে পারে।
            - **Composite index-এ column-এর ক্রম গুরুত্বপূর্ণ:** `(author_id, slug)` "author + slug দিয়ে খোঁজা" আর "author দিয়ে filter" সামলায়, কিন্তু শুধু "slug দিয়ে খোঁজা" না।
            - **Partial index-এর ব্যবহার:** query-র `WHERE` যখন index-এর শর্ত (`published = true`) বোঝায়, planner কেবল তখনই এটা ব্যবহার করে।
            - **Constraint-এর নাম:** index-এর নাম নিজে দিলে (`posts_author_slug_uq`) error handling পরিষ্কার হয় — PostgreSQL error-এর `constraint` field বলে দেয় কোন নিয়ম ভাঙা হয়েছে।
            - Generated SQL (expected output-এ দেখানো) PR-এ review করো — database-এর সাথে চুক্তি এটাই।
        """,
        tip_en=r"""Justify every index with the query it serves ("author listing", "recent published"). Interviewers care less about syntax than about whether you design indexes from access patterns.""",
        tip_bn=r"""প্রতিটা index-এর পক্ষে যুক্তি দাও সে কোন query সামলায় ("author listing", "recent published")। Interviewer syntax-এর চেয়ে বেশি দেখে তুমি access pattern থেকে index design করো কি না।""",
        mist_en=r"""Making `slug` globally unique when the rule is per author; assuming FKs are indexed automatically; cascading deletes from tags into posts; using the deprecated object form for the third `pgTable` argument.""",
        mist_bn=r"""নিয়ম যেখানে author অনুযায়ী, সেখানে `slug`-কে globally unique করা; ধরে নেওয়া যে FK নিজে থেকে index হয়; tag থেকে post-এ cascading delete; `pgTable`-এর তৃতীয় argument-এ deprecated object রূপ ব্যবহার করা।""",
        code=r"""
            import { sql } from 'drizzle-orm';
            import {
              boolean, index, integer, pgTable, primaryKey, text, timestamp, uniqueIndex, varchar,
            } from 'drizzle-orm/pg-core';

            export const posts = pgTable('posts', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              authorId: integer('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
              slug: varchar({ length: 200 }).notNull(),
              title: text().notNull(),
              published: boolean().notNull().default(false),
              publishedAt: timestamp('published_at', { withTimezone: true }),
            }, (t) => [
              index('posts_author_id_idx').on(t.authorId),
              uniqueIndex('posts_author_slug_uq').on(t.authorId, t.slug),
              index('posts_published_at_idx').on(t.publishedAt).where(sql`${t.published} = true`),
            ]);

            export const tags = pgTable('tags', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              name: varchar({ length: 50 }).notNull().unique(),
            });

            export const postTags = pgTable('post_tags', {
              postId: integer('post_id').notNull().references(() => posts.id, { onDelete: 'cascade' }),
              tagId: integer('tag_id').notNull().references(() => tags.id, { onDelete: 'restrict' }),
            }, (t) => [primaryKey({ columns: [t.postId, t.tagId] })]);
        """,
        lang="typescript",
        output=r"""
            -- excerpt from `drizzle-kit generate`
            CONSTRAINT "post_tags_post_id_tag_id_pk" PRIMARY KEY("post_id","tag_id")
            ALTER TABLE "posts" ADD CONSTRAINT "posts_author_id_users_id_fk" FOREIGN KEY ("author_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;
            ALTER TABLE "post_tags" ADD CONSTRAINT "post_tags_tag_id_tags_id_fk" FOREIGN KEY ("tag_id") REFERENCES "public"."tags"("id") ON DELETE restrict ON UPDATE no action;
            CREATE INDEX "posts_author_id_idx" ON "posts" USING btree ("author_id");
            CREATE UNIQUE INDEX "posts_author_slug_uq" ON "posts" USING btree ("author_id","slug");
            CREATE INDEX "posts_published_at_idx" ON "posts" USING btree ("published_at") WHERE "posts"."published" = true;
        """,
        time="Index lookups O(log n); each index adds a small cost to every write",
        space="O(n) per index",
        follow=[
            ("When is a partial index better than a full index?", "কখন full index-এর চেয়ে partial index ভালো?"),
            ("How would you add one of these indexes to a 50M-row table without blocking writes?", "৫ কোটি row-এর table-এ write block না করে এর একটা index কীভাবে যোগ করবে?"),
        ],
        related=["drizzle-002", "drizzle-010", "drizzle-032"],
        refs=[D_INDEXES, PG_CONSTRAINTS],
    ),
    # ------------------------------------------------------------------ drizzle-013
    Q(
        id="drizzle-013", sub="Joins & Aggregation", diff="medium", type="query",
        prio="high", market="both", mins=6,
        tags=["left-join", "group-by", "count", "aggregation"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""Using the schema and data shown, write a Drizzle query that lists **every** user with their number of **published** posts — including users with zero — ordered by that count (highest first), then by name.""",
        q_bn=r"""দেখানো schema আর data ব্যবহার করে এমন একটা Drizzle query লেখো যেটা **প্রত্যেক** user-কে তার **published** post-এর সংখ্যা সহ দেখাবে — যাদের শূন্য তারাও থাকবে — সংখ্যা অনুযায়ী (বেশি থেকে কম), তারপর নাম অনুযায়ী সাজানো।""",
        setup=r"""
            // schema.ts
            export const users = pgTable('users', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              name: text().notNull(),
            });

            export const posts = pgTable('posts', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              authorId: integer('author_id').notNull().references(() => users.id),
              title: text().notNull(),
              published: boolean().notNull().default(false),
            });

            // sample data
            // users: (1, 'Rahim'), (2, 'Karim'), (3, 'Nadia')
            // posts: (1, author 1, 'Intro to NestJS', published)
            //        (2, author 1, 'Drizzle tips',    draft)
            //        (3, author 3, 'PostgreSQL 18',   published)
            //        (4, author 3, 'Indexes 101',     published)
        """,
        setup_lang="typescript",
        code=r"""
            import { and, asc, count, desc, eq } from 'drizzle-orm';

            const rows = await db
              .select({
                id: users.id,
                name: users.name,
                publishedPosts: count(posts.id),
              })
              .from(users)
              .leftJoin(posts, and(eq(posts.authorId, users.id), eq(posts.published, true)))
              .groupBy(users.id)
              .orderBy(desc(count(posts.id)), asc(users.name));

            // SQL:
            // select "users"."id", "users"."name", count("posts"."id") from "users"
            // left join "posts" on ("posts"."author_id" = "users"."id" and "posts"."published" = $1)
            // group by "users"."id" order by count("posts"."id") desc, "users"."name" asc
        """,
        lang="typescript",
        output=r"""
            [
              { id: 3, name: 'Nadia', publishedPosts: 2 },
              { id: 1, name: 'Rahim', publishedPosts: 1 },
              { id: 2, name: 'Karim', publishedPosts: 0 }
            ]
        """,
        a_en=r"""
            - **`leftJoin`** keeps every user even without matching posts (Karim).
            - The **`published = true` condition goes into the join's `ON` clause**, not into `.where()`. A `WHERE posts.published = true` would filter out the `NULL` rows produced for users without posts, and Karim would disappear — verified: the `WHERE` version returns only Nadia and Rahim.
            - **`count(posts.id)`** counts non-null values, so users with no matching post get 0. `count()` without an argument would count the joined row and give Karim 1.
            - **`groupBy(users.id)`** is enough even though `users.name` is selected, because `id` is the primary key and PostgreSQL knows `name` depends on it.
            - Ordering by the aggregate (`desc(count(posts.id))`) then `asc(users.name)` gives a deterministic order.
        """,
        a_bn=r"""
            - **`leftJoin`** প্রত্যেক user-কে রাখে, match করা post না থাকলেও (Karim)।
            - **`published = true` শর্তটা join-এর `ON` clause-এ যায়**, `.where()`-এ না। `WHERE posts.published = true` দিলে post ছাড়া user-দের জন্য তৈরি `NULL` row বাদ পড়ে যেত, আর Karim হারিয়ে যেত — যাচাই করা: `WHERE` version শুধু Nadia আর Rahim দেয়।
            - **`count(posts.id)`** শুধু non-null value গোনে, তাই match না থাকা user পায় 0। Argument ছাড়া `count()` join করা row-টাকেই গুনত, Karim পেত 1।
            - `users.name` select করলেও **`groupBy(users.id)`** যথেষ্ট, কারণ `id` primary key আর PostgreSQL জানে `name` এর উপর নির্ভরশীল।
            - Aggregate (`desc(count(posts.id))`) তারপর `asc(users.name)` দিয়ে sort করলে ক্রম নির্দিষ্ট হয়।
        """,
        quick_en=r"""`leftJoin` posts with `published = true` inside the join's ON clause (a WHERE would drop Karim), use `count(posts.id)` so users without posts get 0, `groupBy(users.id)`, and order by `desc(count(posts.id))` then `asc(users.name)`. Result: Nadia 2, Rahim 1, Karim 0.""",
        quick_bn=r"""posts-কে `leftJoin` করি আর `published = true` শর্তটা join-এর ON-এ রাখি (WHERE-এ রাখলে Karim বাদ পড়ে), `count(posts.id)` দিই যাতে post ছাড়া user 0 পায়, `groupBy(users.id)` করি, তারপর `desc(count(posts.id))` আর `asc(users.name)` দিয়ে sort। Result: Nadia 2, Rahim 1, Karim 0।""",
        ex_en=r"""
            - **Result shape:** with a field object in `select({...})`, Drizzle returns flat rows. Without it, `select().from(users).leftJoin(posts, ...)` returns `{ users: {...}, posts: {...} | null }` per row — the joined side is nullable in the type, mirroring SQL.
            - **ON vs WHERE** is the classic outer-join trap in any SQL dialect, and it's the main thing this question tests.
            - **Performance:** an index on `posts(author_id)` (optionally partial `WHERE published`) keeps the join fast as data grows.
            - The same result could come from the relational API with `extras`/subqueries, but for aggregates the SQL-like builder is clearer.
        """,
        ex_bn=r"""
            - **Result-এর shape:** `select({...})`-এ field object দিলে Drizzle flat row দেয়। না দিলে `select().from(users).leftJoin(posts, ...)` প্রতিটা row-এ `{ users: {...}, posts: {...} | null }` দেয় — join করা দিকটা type-এ nullable, ঠিক SQL-এর মতো।
            - **ON বনাম WHERE** যেকোনো SQL dialect-এ classic outer-join ফাঁদ, আর এই প্রশ্ন মূলত এটাই যাচাই করে।
            - **Performance:** data বাড়লেও join দ্রুত রাখতে `posts(author_id)`-এ index (চাইলে partial `WHERE published`)।
            - Relational API-তে `extras`/subquery দিয়েও একই result পাওয়া যায়, কিন্তু aggregate-এর জন্য SQL-এর মতো builder বেশি পরিষ্কার।
        """,
        tip_en=r"""Say out loud why the filter is in `ON` and why you count `posts.id` rather than rows — those two sentences are the whole answer.""",
        tip_bn=r"""জোরে বলো filter কেন `ON`-এ আর কেন row না গুনে `posts.id` গুনছ — এই দুটো বাক্যই পুরো উত্তর।""",
        mist_en=r"""Putting `eq(posts.published, true)` in `.where()` after a left join; using `count()` (counts the null row as 1); using `innerJoin`, which drops users with no posts.""",
        mist_bn=r"""Left join-এর পরে `eq(posts.published, true)` `.where()`-এ দেওয়া; `count()` ব্যবহার করা (null row-কেও 1 গোনে); `innerJoin` ব্যবহার করা, যেটা post ছাড়া user বাদ দেয়।""",
        follow=[
            ("How would you also return each user's latest published post title?", "প্রত্যেক user-এর সর্বশেষ published post-এর title-ও কীভাবে return করবে?"),
            ("What does the result look like with `select()` and no field object?", "Field object ছাড়া `select()` দিলে result দেখতে কেমন হয়?"),
        ],
        related=["drizzle-014", "drizzle-015"],
        refs=[D_JOINS, D_SELECT],
    ),
    # ------------------------------------------------------------------ drizzle-014
    Q(
        id="drizzle-014", sub="Relational Queries", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["relational-queries", "relations", "findmany", "with", "nested-results"],
        ver="Drizzle ORM 0.45.x (Relational Queries v1; v1.0 RC introduces RQB v2)", vs=True, status="stable",
        q_en=r"""
            With `users`, `posts`, `tags` and the `post_tags` join table, use Drizzle's **relational query API** to return users with role `user`, each with their **published** posts (newest first, only `title` and `publishedAt`) and each post's tag names.

            Expected shape: `[{ id, name, posts: [{ title, publishedAt, postTags: [{ tag: { name } }] }] }]`. Show the relation definitions and the `db` setup too.

            Sample data: Rahim (`user`) has one published post tagged `nestjs` and one draft; Karim (`user`) has no posts; Nadia is an `admin`.
        """,
        q_bn=r"""
            `users`, `posts`, `tags` আর `post_tags` join table ব্যবহার করে Drizzle-এর **relational query API** দিয়ে role `user` থাকা user-দের return করো, প্রত্যেকের **published** post সহ (নতুনটা আগে, শুধু `title` আর `publishedAt`) আর প্রতিটা post-এর tag-এর নাম সহ।

            প্রত্যাশিত shape: `[{ id, name, posts: [{ title, publishedAt, postTags: [{ tag: { name } }] }] }]`। Relation definition আর `db` setup-ও দেখাও।

            Sample data: Rahim (`user`)-এর একটা published post আছে যার tag `nestjs`, আর একটা draft; Karim (`user`)-এর কোনো post নেই; Nadia একজন `admin`।
        """,
        a_en=r"""
            1. **Define relations** with `relations()`: `users` has `many(posts)`; `posts` has `one(users, { fields, references })` and `many(postTags)`; `postTags` has `one(posts)` and `one(tags)`. Many-to-many goes through the join table explicitly in 0.45.
            2. **Pass the schema** — tables *and* relations — to `drizzle({ client, schema })`; otherwise `db.query` is empty.
            3. **Query** with `db.query.users.findMany({ columns, where, with })`. In 0.45 (RQB v1), `where` and `orderBy` are callbacks receiving the table and operators: `where: (u, { eq }) => eq(u.role, 'user')`. Nested `with` objects accept their own `columns`, `where`, `orderBy`, `limit`.

            The result is fully typed from the relation definitions, and Drizzle compiles the whole tree into a single SQL statement.
        """,
        a_bn=r"""
            1. **Relation define করো** `relations()` দিয়ে: `users`-এর `many(posts)`; `posts`-এর `one(users, { fields, references })` আর `many(postTags)`; `postTags`-এর `one(posts)` আর `one(tags)`। 0.45-এ many-to-many join table-এর মধ্য দিয়েই explicitly যায়।
            2. **Schema pass করো** — table *এবং* relation দুটোই — `drizzle({ client, schema })`-এ; নাহলে `db.query` ফাঁকা থাকে।
            3. **Query** করো `db.query.users.findMany({ columns, where, with })` দিয়ে। 0.45-এ (RQB v1) `where` আর `orderBy` হলো callback, যেটা table আর operator পায়: `where: (u, { eq }) => eq(u.role, 'user')`। Nested `with` object নিজের `columns`, `where`, `orderBy`, `limit` নিতে পারে।

            Relation definition থেকে result পুরোপুরি typed, আর Drizzle পুরো tree-টাকে একটাই SQL statement-এ compile করে।
        """,
        quick_en=r"""Define `relations()` from users to posts to `postTags` to tags, pass tables and relations as `schema` to `drizzle()`, then call `db.query.users.findMany()` with `columns`, a callback `where` and nested `with` options. Drizzle builds the whole typed tree in one SQL statement.""",
        quick_bn=r"""users থেকে posts, `postTags` হয়ে tags পর্যন্ত `relations()` define করি, table আর relation দুটোই `schema` হিসেবে `drizzle()`-এ দিই, তারপর `columns`, callback `where` আর nested `with` দিয়ে `db.query.users.findMany()` call করি। Drizzle পুরো typed tree একটাই SQL statement-এ বানায়।""",
        ex_en=r"""
            - **`findFirst`** adds `limit 1` and returns an object or `undefined`; `where` can also be a plain filter: `findFirst({ where: eq(posts.slug, 'pg-18'), with: { author: true } })`.
            - **When to prefer the builder:** aggregates, complex joins and reporting. RQB shines for "load this entity graph for an API response".
            - **Over-fetching:** `with: { posts: true }` loads every column of every post. Use `columns` and `limit` on nested relations for list endpoints.
            - **v1 RC (preview):** relations move to one `defineRelations()` call, `drizzle(url, { relations })`, and object-style filters (`where: { role: 'user' }`, `orderBy: { id: 'asc' }`); many-to-many can use `through` instead of exposing the join table.
        """,
        ex_bn=r"""
            - **`findFirst`** `limit 1` যোগ করে আর একটা object বা `undefined` return করে; `where` সাধারণ filter-ও হতে পারে: `findFirst({ where: eq(posts.slug, 'pg-18'), with: { author: true } })`।
            - **কখন builder ভালো:** aggregate, জটিল join আর reporting। "API response-এর জন্য এই entity graph load করো" — এই কাজে RQB সবচেয়ে ভালো।
            - **Over-fetching:** `with: { posts: true }` প্রতিটা post-এর সব column load করে। List endpoint-এ nested relation-এ `columns` আর `limit` ব্যবহার করো।
            - **v1 RC (preview):** relation চলে যাচ্ছে একটাই `defineRelations()` call-এ, `drizzle(url, { relations })`, আর object-style filter (`where: { role: 'user' }`, `orderBy: { id: 'asc' }`); many-to-many-তে join table সামনে না এনে `through` ব্যবহার করা যায়।
        """,
        tip_en=r"""Mention the two classic setup mistakes (schema not passed, relations not exported) and that the query is a single SQL statement — that answers the N+1 follow-up before it's asked.""",
        tip_bn=r"""দুটো classic setup ভুলের কথা বলো (schema pass না করা, relation export না করা), আর বলো যে query-টা একটাই SQL statement — এতে N+1-এর follow-up জিজ্ঞেস করার আগেই উত্তর হয়ে যায়।""",
        mist_en=r"""Defining relations but not including them in the `schema` passed to `drizzle()`; mixing v2 object-style `where` into 0.45 code; loading full nested graphs for list pages.""",
        mist_bn=r"""Relation define করে `drizzle()`-এ দেওয়া `schema`-তে না রাখা; 0.45-এর code-এ v2-এর object-style `where` মিশিয়ে ফেলা; list page-এর জন্য পুরো nested graph load করা।""",
        code=r"""
            // relations.ts (Drizzle 0.45 — Relational Queries v1)
            import { relations } from 'drizzle-orm';
            import { posts, postTags, tags, users } from './schema';

            export const usersRelations = relations(users, ({ many }) => ({ posts: many(posts) }));
            export const postsRelations = relations(posts, ({ one, many }) => ({
              author: one(users, { fields: [posts.authorId], references: [users.id] }),
              postTags: many(postTags),
            }));
            export const tagsRelations = relations(tags, ({ many }) => ({ postTags: many(postTags) }));
            export const postTagsRelations = relations(postTags, ({ one }) => ({
              post: one(posts, { fields: [postTags.postId], references: [posts.id] }),
              tag: one(tags, { fields: [postTags.tagId], references: [tags.id] }),
            }));

            // db.ts
            import * as tables from './schema';
            import * as rels from './relations';
            export const db = drizzle({ client: pool, schema: { ...tables, ...rels } });

            // query
            const authors = await db.query.users.findMany({
              columns: { id: true, name: true },
              where: (u, { eq }) => eq(u.role, 'user'),
              with: {
                posts: {
                  columns: { title: true, publishedAt: true },
                  where: (p, { eq }) => eq(p.published, true),
                  orderBy: (p, { desc }) => [desc(p.publishedAt)],
                  with: { postTags: { columns: {}, with: { tag: { columns: { name: true } } } } },
                },
              },
            });
        """,
        lang="typescript",
        output=r"""
            [
              {
                "id": 1,
                "name": "Rahim",
                "posts": [
                  {
                    "title": "Intro to NestJS",
                    "publishedAt": "2026-10-01T00:00:00.000Z",
                    "postTags": [{ "tag": { "name": "nestjs" } }]
                  }
                ]
              },
              { "id": 2, "name": "Karim", "posts": [] }
            ]
        """,
        time="One SQL statement; cost depends on indexes on the FK columns",
        space="O(size of the returned graph)",
        follow=[
            ("How many SQL statements does this send, and how does Drizzle build the nesting?", "এটা কয়টা SQL statement পাঠায়, আর Drizzle nesting কীভাবে বানায়?"),
            ("How would the same query look in the v1 RC (RQB v2)?", "v1 RC-তে (RQB v2) একই query দেখতে কেমন হবে?"),
        ],
        related=["drizzle-010", "drizzle-015", "drizzle-027"],
        refs=[D_RQB, D_RELATIONS_V1V2],
    ),
    # ------------------------------------------------------------------ drizzle-015
    Q(
        id="drizzle-015", sub="Relational Queries", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["relational-queries", "n-plus-one", "lateral-join", "performance"],
        ver="Drizzle ORM 0.45.x (PostgreSQL)", vs=False, status="stable",
        q_en=r"""On PostgreSQL, how many SQL statements does `db.query.users.findMany({ with: { posts: true } })` send to the database?""",
        q_bn=r"""PostgreSQL-এ `db.query.users.findMany({ with: { posts: true } })` database-এ কয়টা SQL statement পাঠায়?""",
        options=[
            ("One for the users, then one per user to load their posts (N+1)", "User-দের জন্য একটা, তারপর প্রত্যেক user-এর post load করতে একটা করে (N+1)"),
            ("Exactly one — nested rows are built inside PostgreSQL with lateral subqueries and JSON aggregation", "ঠিক একটা — nested row PostgreSQL-এর ভেতরেই lateral subquery আর JSON aggregation দিয়ে তৈরি হয়"),
            ("Two — users first, then all their posts with `WHERE author_id IN (...)`, merged in JavaScript", "দুটো — আগে user, তারপর `WHERE author_id IN (...)` দিয়ে তাদের সব post, JavaScript-এ মেলানো"),
            ("It depends on the number of users — Drizzle switches strategy above a threshold", "User-এর সংখ্যার উপর নির্ভর করে — একটা সীমার পরে Drizzle কৌশল বদলায়"),
        ],
        correct=1,
        a_en=r"""Exactly one statement. Drizzle compiles the relational query into a single SQL query that uses `left join lateral (...)` subqueries with `json_agg` to build the nested arrays, then maps the JSON into typed objects.""",
        a_bn=r"""ঠিক একটা statement। Drizzle relational query-টাকে একটাই SQL query-তে compile করে, যেটা nested array বানাতে `json_agg` সহ `left join lateral (...)` subquery ব্যবহার করে, তারপর JSON-কে typed object-এ map করে।""",
        quick_en=r"""Exactly one: Drizzle compiles the relational query into a single SQL statement with lateral subqueries and `json_agg`, then maps the JSON into typed objects, so there's no N+1.""",
        quick_bn=r"""ঠিক একটা: Drizzle relational query-কে lateral subquery আর `json_agg` দিয়ে একটাই SQL statement-এ compile করে, তারপর JSON-কে typed object-এ map করে — তাই কোনো N+1 হয় না।""",
        ex_en=r"""
            Verified SQL (shape) for a filtered version:

            `select "users"."id", "users"."name", "users_posts"."data" as "posts" from "users" "users" left join lateral (select coalesce(json_agg(json_build_array("users_posts"."title")), '[]'::json) as "data" from "posts" "users_posts" where ("users_posts"."author_id" = "users"."id" and "users_posts"."published" = $1)) "users_posts" on true where "users"."id" in ($2, $3)`

            Option C is tempting because that's how many ORMs (and Prisma's `include`) have traditionally worked — separate queries stitched together in the application. Drizzle's docs state that the relational API always outputs a single SQL statement.

            Caveats: one big query isn't automatically fast. Deep or wide `with` trees on large tables still need indexes on the FK columns, `columns` selection and `limit`s on nested relations; check with `EXPLAIN ANALYZE`.
        """,
        ex_bn=r"""
            একটা filtered version-এর যাচাই করা SQL (shape):

            `select "users"."id", "users"."name", "users_posts"."data" as "posts" from "users" "users" left join lateral (select coalesce(json_agg(json_build_array("users_posts"."title")), '[]'::json) as "data" from "posts" "users_posts" where ("users_posts"."author_id" = "users"."id" and "users_posts"."published" = $1)) "users_posts" on true where "users"."id" in ($2, $3)`

            Option C লোভনীয়, কারণ অনেক ORM (আর Prisma-র `include`) ঐতিহ্যগতভাবে এভাবেই কাজ করেছে — আলাদা query application-এ জোড়া লাগানো। Drizzle-এর docs বলে relational API সবসময় একটা SQL statement তৈরি করে।

            সতর্কতা: একটা বড় query মানেই দ্রুত না। বড় table-এ গভীর বা চওড়া `with` tree-র জন্য এখনো FK column-এ index, `columns` selection আর nested relation-এ `limit` লাগে; `EXPLAIN ANALYZE` দিয়ে যাচাই করো।
        """,
        tip_en=r"""After answering, add the caveat that "one query" still needs indexes — it shows you think about the database's work, not just round trips.""",
        tip_bn=r"""উত্তর দেওয়ার পর সতর্কতাটা যোগ করো যে "একটা query"-তেও index লাগে — এতে বোঝা যায় তুমি শুধু round trip না, database-এর কাজ নিয়েও ভাবো।""",
        related=["drizzle-014", "drizzle-028"],
        refs=[D_RQB],
    ),
    # ------------------------------------------------------------------ drizzle-016
    Q(
        id="drizzle-016", sub="Transactions", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["transactions", "rollback", "isolation-level", "atomicity"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""
            Implement `transfer(fromId, toId, amount)` for a wallet app with Drizzle:

            - debit the sender, credit the receiver, and insert a row into `transfers` — all or nothing;
            - fail with an `InsufficientFundsError` if the sender doesn't have enough balance (no partial changes);
            - roll back if the receiver account doesn't exist;
            - be safe when two transfers from the same account run at the same time.

            Example: balances `{1: 500.00, 2: 100.00}`; `transfer(1, 2, '200.00')` → `{1: 300.00, 2: 300.00}`, one `transfers` row.
        """,
        q_bn=r"""
            Drizzle দিয়ে একটা wallet app-এর জন্য `transfer(fromId, toId, amount)` implement করো:

            - sender থেকে debit, receiver-এ credit, আর `transfers`-এ একটা row insert — সব হবে, নয়তো কিছুই না;
            - sender-এর যথেষ্ট balance না থাকলে `InsufficientFundsError` দিয়ে fail করবে (আংশিক পরিবর্তন ছাড়া);
            - receiver account না থাকলে rollback করবে;
            - একই account থেকে দুটো transfer একসাথে চললেও নিরাপদ থাকবে।

            উদাহরণ: balance `{1: 500.00, 2: 100.00}`; `transfer(1, 2, '200.00')` → `{1: 300.00, 2: 300.00}`, `transfers`-এ একটা row।
        """,
        a_en=r"""
            - `db.transaction(async (tx) => { ... })` runs the callback in `BEGIN ... COMMIT`. If the callback throws, Drizzle issues `ROLLBACK` and rethrows. **Every query inside must use `tx`**, not `db`.
            - **Debit atomically with a guard:** `UPDATE accounts SET balance = balance - $amount WHERE id = $from AND balance >= $amount RETURNING ...`. If no row comes back, funds are insufficient → throw. Because the check and the write are one statement, two concurrent transfers can't both pass a stale check — the second waits for the row lock and re-evaluates the condition.
            - **Credit** the receiver; if `returning()` is empty, call `tx.rollback()` — it throws a `TransactionRollbackError`, which rolls back the debit too.
            - Insert the `transfers` row and return it.
            - Money uses `numeric(12, 2)`, which Drizzle returns as a **string** to avoid floating-point errors; a `CHECK (balance >= 0)` constraint is a final safety net.
        """,
        a_bn=r"""
            - `db.transaction(async (tx) => { ... })` callback-টা `BEGIN ... COMMIT`-এর ভেতরে চালায়। Callback throw করলে Drizzle `ROLLBACK` দেয় আর error আবার throw করে। **ভেতরের প্রতিটা query-তে `tx` ব্যবহার করতে হবে**, `db` না।
            - **Guard সহ atomically debit:** `UPDATE accounts SET balance = balance - $amount WHERE id = $from AND balance >= $amount RETURNING ...`। কোনো row ফেরত না এলে balance যথেষ্ট না → throw। Check আর write একই statement বলে দুটো একসাথে চলা transfer পুরোনো check দিয়ে দুজনেই পার পায় না — দ্বিতীয়টা row lock-এর জন্য অপেক্ষা করে আর শর্ত আবার যাচাই করে।
            - Receiver-কে **credit** করো; `returning()` ফাঁকা হলে `tx.rollback()` call করো — এটা একটা `TransactionRollbackError` throw করে, যেটা debit-ও rollback করে দেয়।
            - `transfers` row insert করে return করো।
            - টাকার জন্য `numeric(12, 2)`, যেটা Drizzle floating-point ভুল এড়াতে **string** হিসেবে দেয়; `CHECK (balance >= 0)` constraint শেষ safety net।
        """,
        quick_en=r"""Run everything in `db.transaction(async (tx) => ...)` and use `tx` for every query. Debit with one guarded `UPDATE ... WHERE id = from AND balance >= amount RETURNING`, throw `InsufficientFundsError` if no row returns, call `tx.rollback()` if the credit finds no receiver, then insert the transfer row.""",
        quick_bn=r"""সব কাজ `db.transaction(async (tx) => ...)`-এর ভেতরে, আর প্রতিটা query `tx` দিয়ে। Debit করি একটাই guarded `UPDATE ... WHERE id = from AND balance >= amount RETURNING` দিয়ে, কোনো row না ফিরলে `InsufficientFundsError` throw করি, receiver না পেলে `tx.rollback()`, তারপর transfer row insert।""",
        ex_en=r"""
            - **Verified behaviour:** `transfer(1, 2, '200.00')` → balances 300.00 / 300.00; `transfer(2, 1, '1000.00')` → `InsufficientFundsError`, nothing changed; `transfer(1, 99, '10.00')` → `TransactionRollbackError`, the debit is undone.
            - **Why not SELECT then UPDATE:** reading the balance and writing `balance - amount` from JavaScript is a lost-update race under the default READ COMMITTED isolation. Either use the conditional update (above), `SELECT ... FOR UPDATE` (`.for('update')`), or SERIALIZABLE isolation with retries on `40001`.
            - **Deadlocks:** two opposite transfers (A→B and B→A) can lock rows in different orders. Locking accounts in a consistent order (lowest id first) avoids it; otherwise retry on `40P01`.
            - **Config:** `db.transaction(fn, { isolationLevel: 'serializable' | 'repeatable read' | 'read committed', accessMode, deferrable })`. Nested `tx.transaction()` creates a savepoint.
            - Keep transactions short: no HTTP calls or emails inside them.
        """,
        ex_bn=r"""
            - **যাচাই করা behaviour:** `transfer(1, 2, '200.00')` → balance 300.00 / 300.00; `transfer(2, 1, '1000.00')` → `InsufficientFundsError`, কিছুই বদলায়নি; `transfer(1, 99, '10.00')` → `TransactionRollbackError`, debit ফিরিয়ে নেওয়া হয়েছে।
            - **SELECT তারপর UPDATE কেন না:** JavaScript থেকে balance পড়ে `balance - amount` লেখা default READ COMMITTED isolation-এ lost-update race। হয় উপরের conditional update, নয়তো `SELECT ... FOR UPDATE` (`.for('update')`), নয়তো `40001`-এ retry সহ SERIALIZABLE isolation।
            - **Deadlock:** বিপরীত দুটো transfer (A→B আর B→A) ভিন্ন ক্রমে row lock করতে পারে। Account গুলো একটা নির্দিষ্ট ক্রমে lock করলে (ছোট id আগে) এটা এড়ানো যায়; নাহলে `40P01`-এ retry।
            - **Config:** `db.transaction(fn, { isolationLevel: 'serializable' | 'repeatable read' | 'read committed', accessMode, deferrable })`। Nested `tx.transaction()` একটা savepoint তৈরি করে।
            - Transaction ছোট রাখো: ভেতরে HTTP call বা email না।
        """,
        tip_en=r"""Highlight "check and write in one statement" as the concurrency fix, and mention `tx` vs `db`. Those two points separate a working answer from a correct one.""",
        tip_bn=r""""Check আর write এক statement-এ" — concurrency-র সমাধান হিসেবে এটা তুলে ধরো, আর `tx` বনাম `db`-এর কথা বলো। এই দুটো point-ই চলনসই উত্তর আর সঠিক উত্তরের পার্থক্য।""",
        mist_en=r"""Using `db` instead of `tx` inside the callback; reading the balance into JS and writing it back; using JavaScript numbers (floats) for money; catching errors inside the callback and not rethrowing, which commits a half-done transfer.""",
        mist_bn=r"""Callback-এর ভেতরে `tx`-এর বদলে `db` ব্যবহার করা; balance JS-এ পড়ে আবার লিখে দেওয়া; টাকার জন্য JavaScript number (float) ব্যবহার করা; callback-এর ভেতরে error ধরে আবার throw না করা, ফলে অর্ধেক হওয়া transfer commit হয়ে যায়।""",
        code=r"""
            import { and, eq, gte, sql } from 'drizzle-orm';
            import { accounts, transfers } from './schema'; // balance: numeric(12, 2) with CHECK (balance >= 0)

            export class InsufficientFundsError extends Error {}

            export async function transfer(fromId: number, toId: number, amount: string) {
              return db.transaction(async (tx) => {
                const debited = await tx
                  .update(accounts)
                  .set({ balance: sql`${accounts.balance} - ${amount}` })
                  .where(and(eq(accounts.id, fromId), gte(accounts.balance, amount)))
                  .returning({ balance: accounts.balance });
                if (debited.length === 0) {
                  throw new InsufficientFundsError(`Account ${fromId} has insufficient funds`);
                }

                const credited = await tx
                  .update(accounts)
                  .set({ balance: sql`${accounts.balance} + ${amount}` })
                  .where(eq(accounts.id, toId))
                  .returning({ id: accounts.id });
                if (credited.length === 0) tx.rollback(); // throws TransactionRollbackError

                const [row] = await tx
                  .insert(transfers)
                  .values({ fromId, toId, amount })
                  .returning({ id: transfers.id });
                return row;
              }, { isolationLevel: 'read committed' });
            }
        """,
        lang="typescript",
        output=r"""
            transfer(1, 2, '200.00')   -> { id: 1 }        balances: 1 = '300.00', 2 = '300.00'
            transfer(2, 1, '1000.00')  -> InsufficientFundsError: Account 2 has insufficient funds
            transfer(1, 99, '10.00')   -> TransactionRollbackError (debit rolled back)
        """,
        time="O(log n) per indexed update; three statements per transfer",
        space="O(1)",
        follow=[
            ("How would you avoid deadlocks between A→B and B→A transfers?", "A→B আর B→A transfer-এর মধ্যে deadlock কীভাবে এড়াবে?"),
            ("When would you choose SERIALIZABLE, and what must the caller do?", "কখন SERIALIZABLE বেছে নেবে, আর caller-কে কী করতে হবে?"),
        ],
        related=["drizzle-025", "nest-032"],
        refs=[D_TRANSACTIONS],
    ),
]

if __name__ == "__main__":
    save("drizzle", "b2", QUESTIONS)
