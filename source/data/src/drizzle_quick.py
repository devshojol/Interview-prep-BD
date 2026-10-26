# Drizzle ORM — quick-recall questions (drizzle-q01 … drizzle-q10): short viva-style fundamentals
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

DRZ_VER = "Drizzle ORM 0.45 (stable)"
KIT_VER = "Drizzle ORM 0.45 / drizzle-kit 0.31 (stable)"

QUESTIONS = [
    # ------------------------------------------------------------------ drizzle-q01
    Q(
        id="drizzle-q01", sub="Schema Definitions", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["schema", "pgtable", "basics"],
        ver=DRZ_VER, vs=False, status="stable",
        q_en=r"""What is the schema in Drizzle, and what is it used for?""",
        q_bn=r"""Drizzle-এ schema কী, আর এটা কী কাজে লাগে?""",
        a_en=r"""The schema is plain TypeScript where you declare your tables with functions like `pgTable()`, columns, constraints and indexes. It is the single source of truth: queries use it for type checking, TypeScript types are inferred from it, and Drizzle Kit compares it with the database to create migrations.""",
        a_bn=r"""Schema হলো সাধারণ TypeScript, যেখানে `pgTable()`-এর মতো function দিয়ে table, column, constraint আর index declare করা হয়। এটাই single source of truth: query এটা দিয়ে type check হয়, TypeScript type এখান থেকেই infer হয়, আর Drizzle Kit এটাকে database-এর সাথে তুলনা করে migration বানায়।""",
        code=r"""
            import { pgTable, integer, text } from 'drizzle-orm/pg-core';

            export const users = pgTable('users', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              name: text().notNull(),
            });
        """, lang="typescript",
        ex_en=r"""Changing the schema file does not change the database by itself; you still run `drizzle-kit generate` + `migrate` (or `push` locally).""",
        ex_bn=r"""Schema file বদলালেই database বদলায় না; তার জন্য এখনো `drizzle-kit generate` + `migrate` (বা local-এ `push`) চালাতে হয়।""",
        tip_en=r"""Say "TypeScript tables, one source for types, queries and migrations".""",
        tip_bn=r"""বলো "TypeScript-এ table, type, query আর migration — সবকিছুর একটাই উৎস"।""",
        follow=[("What does `.references()` add to a column?", "Column-এ `.references()` কী যোগ করে?")],
        related=["drizzle-002", "drizzle-010"],
        refs=[("Drizzle docs — Schema declaration", "https://orm.drizzle.team/docs/sql-schema-declaration")],
    ),
    # ------------------------------------------------------------------ drizzle-q02
    Q(
        id="drizzle-q02", sub="Drizzle Kit", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["drizzle-kit", "migrations", "generate", "push"],
        ver=KIT_VER, vs=True, status="stable",
        q_en=r"""What do `drizzle-kit generate`, `migrate`, `push` and `pull` do?""",
        q_bn=r"""`drizzle-kit generate`, `migrate`, `push` আর `pull` কী করে?""",
        a_en=r"""`generate` compares your schema with the last snapshot and writes a SQL migration file; `migrate` applies the pending migration files to the database. `push` applies schema changes directly with no migration files (good for local prototyping), and `pull` introspects an existing database and generates the TypeScript schema from it.""",
        a_bn=r"""`generate` schema-কে আগের snapshot-এর সাথে তুলনা করে একটা SQL migration file লেখে; `migrate` বাকি থাকা migration file-গুলো database-এ চালায়। `push` কোনো migration file ছাড়াই সরাসরি schema-র পরিবর্তন database-এ বসায় (local prototyping-এর জন্য ভালো), আর `pull` পুরোনো database introspect করে তার TypeScript schema বানিয়ে দেয়।""",
        code=r"""
            npx drizzle-kit generate   # schema.ts → drizzle/0001_xxx.sql (no DB connection)
            npx drizzle-kit migrate    # runs pending .sql files, records them in the DB
            npx drizzle-kit push       # syncs schema straight to the DB, no files
            npx drizzle-kit pull       # existing DB → schema.ts
        """, lang="bash",
        ex_en=r"""Use `generate` + `migrate` for anything shared (CI, staging, production) because the SQL is reviewed and replayable; `push` leaves no history.""",
        ex_bn=r"""Shared যেকোনো জায়গায় (CI, staging, production) `generate` + `migrate` ব্যবহার করো, কারণ SQL review আর replay করা যায়; `push` কোনো history রাখে না।""",
        tip_en=r"""Give one line per command, then add "push locally, migrate in production".""",
        tip_bn=r"""প্রতিটা command-এর জন্য এক line বলো, তারপর যোগ করো "local-এ push, production-এ migrate"।""",
        follow=[("Where do you configure Drizzle Kit?", "Drizzle Kit কোথায় configure করো?")],
        related=["drizzle-007", "drizzle-017", "drizzle-029"],
        refs=[("Drizzle docs — Migrations", "https://orm.drizzle.team/docs/migrations")],
    ),
    # ------------------------------------------------------------------ drizzle-q03
    Q(
        id="drizzle-q03", sub="Type Inference", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["typescript", "inferselect", "inferinsert"],
        ver=DRZ_VER, vs=False, status="stable",
        q_en=r"""What are `$inferSelect` and `$inferInsert` in Drizzle?""",
        q_bn=r"""Drizzle-এ `$inferSelect` আর `$inferInsert` কী?""",
        a_en=r"""They give you TypeScript types straight from a table, with no code generation. `typeof users.$inferSelect` is the shape of a row you read back; `typeof users.$inferInsert` is what you pass to `insert()`, where columns that are nullable or have defaults become optional.""",
        a_bn=r"""এগুলো code generation ছাড়াই সরাসরি table থেকে TypeScript type দেয়। `typeof users.$inferSelect` হলো পড়ে আনা row-এর shape; `typeof users.$inferInsert` হলো `insert()`-এ যা পাঠাও, যেখানে nullable বা default থাকা column optional হয়ে যায়।""",
        code=r"""
            export type User = typeof users.$inferSelect;    // { id: number; name: string; bio: string | null }
            export type NewUser = typeof users.$inferInsert; // { name: string; bio?: string | null }
            // (id is an always-generated identity, so it is not in NewUser)
        """, lang="typescript",
        ex_en=r"""Because the types come from the schema, renaming a column breaks every wrong query at compile time instead of at runtime.""",
        ex_bn=r"""Type যেহেতু schema থেকে আসে, column rename করলে ভুল query-গুলো runtime-এ নয়, compile time-এই ধরা পড়ে।""",
        tip_en=r"""Say "select type for reading, insert type for writing; defaults make insert fields optional".""",
        tip_bn=r"""বলো "পড়ার জন্য select type, লেখার জন্য insert type; default থাকলে insert field optional"।""",
        follow=[("Why is a generated identity `id` missing from the insert type?", "Insert type-এ generated identity `id` কেন থাকে না?")],
        related=["drizzle-006", "drizzle-002"],
        refs=[("Drizzle docs — Goodies (type API)", "https://orm.drizzle.team/docs/goodies")],
    ),
    # ------------------------------------------------------------------ drizzle-q04
    Q(
        id="drizzle-q04", sub="Relational Queries", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["select", "rqb", "relations", "joins"],
        ver=DRZ_VER + "; v1 RC = preview", vs=True, status="stable",
        q_en=r"""What is the difference between `db.select()` and `db.query` (relational queries) in Drizzle?""",
        q_bn=r"""Drizzle-এ `db.select()` আর `db.query` (relational query)-এর পার্থক্য কী?""",
        a_en=r"""`db.select()` is the SQL-like builder: you write joins, filters and grouping yourself, and joined results come back as flat rows. `db.query.users.findMany({ with: { posts: true } })` uses the relations you defined to return nested objects in one SQL statement, but it needs `schema` passed to `drizzle()`.""",
        a_bn=r"""`db.select()` হলো SQL-এর মতো builder: join, filter, grouping নিজে লেখো, আর join-এর result আসে flat row হিসেবে। `db.query.users.findMany({ with: { posts: true } })` তোমার define করা relation ব্যবহার করে একটাই SQL statement-এ nested object ফেরত দেয়, তবে এর জন্য `drizzle()`-এ `schema` দিতে হয়।""",
        code=r"""
            await db.select().from(users).leftJoin(posts, eq(posts.authorId, users.id));
            // → [{ users: {...}, posts: {...} }, { users: {...}, posts: null }]   (flat rows)

            await db.query.users.findMany({ with: { posts: true } });
            // → [{ id: 1, name: 'Rahim', posts: [{...}] }, { id: 2, name: 'Karim', posts: [] }]
        """, lang="typescript",
        ex_en=r"""Use `select()` for reports, aggregates and complex joins, and `db.query` for reading entity trees. The v1 release candidate changes the relational API (`defineRelations`, object-style `where`), but that is still preview.""",
        ex_bn=r"""Report, aggregate আর জটিল join-এর জন্য `select()`, entity tree পড়ার জন্য `db.query`। v1 release candidate-এ relational API বদলাচ্ছে (`defineRelations`, object-style `where`), তবে সেটা এখনো preview।""",
        tip_en=r"""Contrast "flat rows you shape yourself" with "nested objects from relations".""",
        tip_bn=r"""এই তুলনাটা করো: "নিজে সাজানো flat row" বনাম "relation থেকে nested object"।""",
        follow=[("Does `with` cause N+1 queries?", "`with` কি N+1 query তৈরি করে?")],
        related=["drizzle-014", "drizzle-015", "drizzle-027"],
        refs=[("Drizzle docs — Relational queries", "https://orm.drizzle.team/docs/rqb"),
              ("Drizzle docs — Select", "https://orm.drizzle.team/docs/select")],
    ),
    # ------------------------------------------------------------------ drizzle-q05
    Q(
        id="drizzle-q05", sub="Drizzle vs Raw SQL", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["sql-template", "parameters", "sql-injection"],
        ver=DRZ_VER, vs=False, status="stable",
        q_en=r"""What is the `sql` template tag in Drizzle, and is it safe from SQL injection?""",
        q_bn=r"""Drizzle-এর `sql` template tag কী, আর এটা কি SQL injection থেকে নিরাপদ?""",
        a_en=r"""`sql` lets you write raw SQL fragments when the builder doesn't cover something, like a database function. It is safe for values: everything you interpolate with `${}` is sent as a bound parameter, and interpolated columns become quoted column names. Only `sql.raw()` inserts text unescaped, so never pass user input to it.""",
        a_bn=r"""Builder যেটা পারে না, যেমন কোনো database function, সেখানে `sql` দিয়ে raw SQL-এর টুকরো লেখা যায়। Value-র জন্য এটা নিরাপদ: `${}` দিয়ে যা interpolate করো সব bound parameter হিসেবে যায়, আর column দিলে সেটা quoted column name হয়। শুধু `sql.raw()` text হুবহু বসায়, তাই তাতে কখনো user input দিও না।""",
        code=r"""
            const email = req.query.email; // user input
            await db.select().from(users).where(sql`lower(${users.email}) = ${email}`);
            // → ... where lower("users"."email") = $1   (email sent separately as a parameter)
        """, lang="typescript",
        ex_en=r"""Write `sql<number>` (with the fragment after it) to give an expression's result a TypeScript type, for example a `count(*)` in a select.""",
        ex_bn=r"""কোনো expression-এর result-এ TypeScript type দিতে `sql<number>` লেখো (তার পরে fragment), যেমন select-এর ভেতরে একটা `count(*)`।""",
        tip_en=r"""Say "values become parameters; only `sql.raw()` is dangerous".""",
        tip_bn=r"""বলো "value parameter হয়ে যায়; বিপদ শুধু `sql.raw()`-এ"।""",
        follow=[("How would you allow a user-chosen sort column safely?", "User-এর বেছে নেওয়া sort column নিরাপদে কীভাবে দেবে?")],
        related=["drizzle-008", "drizzle-011"],
        refs=[("Drizzle docs — Magic sql operator", "https://orm.drizzle.team/docs/sql")],
    ),
    # ------------------------------------------------------------------ drizzle-q06
    Q(
        id="drizzle-q06", sub="Drizzle vs Prisma", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["prisma", "codegen", "comparison"],
        ver=DRZ_VER + " / Prisma ORM 7", vs=True, status="stable",
        q_en=r"""Does Drizzle need a code-generation step like `prisma generate`?""",
        q_bn=r"""Drizzle-এ কি `prisma generate`-এর মতো code-generation step লাগে?""",
        a_en=r"""No. Prisma reads its own `schema.prisma` file and generates a client, so you rerun `prisma generate` after every schema change to update the types. Drizzle's schema is already TypeScript, so types are inferred instantly by the compiler; Drizzle Kit only generates SQL migrations, not a client.""",
        a_bn=r"""না। Prisma নিজের `schema.prisma` file পড়ে একটা client generate করে, তাই schema বদলালেই type update করতে আবার `prisma generate` চালাতে হয়। Drizzle-এর schema আগে থেকেই TypeScript, তাই compiler সাথে সাথে type infer করে; Drizzle Kit শুধু SQL migration বানায়, কোনো client নয়।""",
        ex_en=r"""Beyond codegen, the bigger difference is style: Prisma offers a high-level object API with nested writes, Drizzle stays close to SQL.""",
        ex_bn=r"""Codegen-এর বাইরে বড় পার্থক্য হলো style: Prisma-র high-level object API-তে nested write আছে, আর Drizzle SQL-এর কাছাকাছি থাকে।""",
        tip_en=r"""Answer "no", then name the one-line reason: the schema is TypeScript.""",
        tip_bn=r"""আগে "না" বলো, তারপর এক line-এ কারণ: schema-টাই TypeScript।""",
        follow=[("When would you still choose Prisma?", "কখন তবুও Prisma বেছে নেবে?")],
        related=["drizzle-020", "drizzle-001"],
        refs=[("Drizzle docs — Overview", "https://orm.drizzle.team/docs/overview")],
    ),
    # ------------------------------------------------------------------ drizzle-q07
    Q(
        id="drizzle-q07", sub="CRUD Queries", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["insert", "bulk-insert", "returning"],
        ver=DRZ_VER, vs=False, status="stable",
        q_en=r"""How do you insert several rows at once in Drizzle and get the created rows back?""",
        q_bn=r"""Drizzle-এ একসাথে কয়েকটা row insert করে তৈরি হওয়া row-গুলো কীভাবে ফেরত পাবে?""",
        a_en=r"""Pass an array to `values()`, which builds one multi-row `INSERT` statement, and add `.returning()` to get the inserted rows with generated values such as `id`. Without `.returning()` you only get the driver's query result (such as the row count), not the rows.""",
        a_bn=r"""`values()`-এ একটা array দাও, তাতে একটাই multi-row `INSERT` statement তৈরি হয়, আর `.returning()` যোগ করলে `id`-র মতো generated value-সহ insert হওয়া row-গুলো ফেরত আসে। `.returning()` ছাড়া শুধু driver-এর query result (যেমন row count) পাও, row-গুলো নয়।""",
        code=r"""
            const rows = await db.insert(users)
              .values([{ name: 'Rahim' }, { name: 'Karim' }])
              .returning({ id: users.id, name: users.name });
            // → [ { id: 1, name: 'Rahim' }, { id: 2, name: 'Karim' } ]
        """, lang="typescript",
        ex_en=r"""For very large imports, split the array into chunks: one statement has a limit on bound parameters, and huge statements hold locks longer.""",
        ex_bn=r"""অনেক বড় import হলে array-কে ভাগ করে নাও: একটা statement-এ bound parameter-এর সীমা আছে, আর বিশাল statement বেশি সময় lock ধরে রাখে।""",
        tip_en=r"""Mention "one statement, not a loop of inserts" and `.returning()`.""",
        tip_bn=r"""বলো "loop-এ অনেক insert নয়, একটাই statement", আর `.returning()`-এর কথা বলো।""",
        follow=[("What happens if one row violates a unique constraint?", "একটা row unique constraint ভাঙলে কী হয়?")],
        related=["drizzle-004"],
        refs=[("Drizzle docs — Insert", "https://orm.drizzle.team/docs/insert")],
    ),
    # ------------------------------------------------------------------ drizzle-q08
    Q(
        id="drizzle-q08", sub="Upserts (onConflictDoUpdate)", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["upsert", "on-conflict", "insert"],
        ver=DRZ_VER, vs=False, status="stable",
        q_en=r"""How do you write an upsert ("insert or update") in Drizzle?""",
        q_bn=r"""Drizzle-এ upsert ("insert, নয়তো update") কীভাবে লেখো?""",
        a_en=r"""Chain `.onConflictDoUpdate({ target, set })` on an insert: if a row with the same value in the `target` column already exists, it is updated with `set` instead. `.onConflictDoNothing()` simply skips the duplicate. The target column must have a unique constraint or index.""",
        a_bn=r"""Insert-এর সাথে `.onConflictDoUpdate({ target, set })` জুড়ে দাও: `target` column-এ একই value-র row আগে থেকে থাকলে নতুন row না বানিয়ে `set` দিয়ে সেটাকে update করে। `.onConflictDoNothing()` duplicate-টা শুধু বাদ দেয়। Target column-এ unique constraint বা index থাকতেই হবে।""",
        code=r"""
            await db.insert(users)
              .values({ email: 'a@x.com', name: 'Rahim Uddin' })
              .onConflictDoUpdate({ target: users.email, set: { name: 'Rahim Uddin' } })
              .returning({ id: users.id, name: users.name });
            // email exists as id 1 → [ { id: 1, name: 'Rahim Uddin' } ]   (no new row)
        """, lang="typescript",
        ex_en=r"""It compiles to PostgreSQL's `INSERT ... ON CONFLICT`, so it is atomic, unlike "select, then insert or update" in application code.""",
        ex_bn=r"""এটা PostgreSQL-এর `INSERT ... ON CONFLICT`-এ compile হয়, তাই atomic — application code-এ "আগে select, তারপর insert বা update" করার মতো race হয় না।""",
        tip_en=r"""Name both methods and mention the unique-constraint requirement.""",
        tip_bn=r"""দুটো method-এর নাম বলো আর unique constraint লাগার শর্তটা উল্লেখ করো।""",
        follow=[("How do you use the incoming value in a multi-row upsert?", "Multi-row upsert-এ নতুন আসা value কীভাবে ব্যবহার করবে?")],
        related=["drizzle-018", "drizzle-004"],
        refs=[("Drizzle docs — Insert (upserts and conflicts)", "https://orm.drizzle.team/docs/insert")],
    ),
    # ------------------------------------------------------------------ drizzle-q09
    Q(
        id="drizzle-q09", sub="Column Types", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["jsonb", "type", "column-types"],
        ver=DRZ_VER, vs=False, status="stable",
        q_en=r"""How do you type a `jsonb` column in Drizzle, and does that validate the data?""",
        q_bn=r"""Drizzle-এ `jsonb` column-এর type কীভাবে দেবে, আর তাতে কি data validate হয়?""",
        a_en=r"""Add `.$type<T>()` to the column, for example `jsonb().$type<{ theme: string }>()`, and selects and inserts use that type. It is compile-time only: Drizzle does not check the JSON at runtime, so validate incoming data yourself (with zod, for example).""",
        a_bn=r"""Column-এ `.$type<T>()` যোগ করো, যেমন `jsonb().$type<{ theme: string }>()`, তাহলে select আর insert সেই type ব্যবহার করবে। এটা শুধু compile-time-এর: Drizzle runtime-এ JSON check করে না, তাই আসা data নিজে validate করো (যেমন zod দিয়ে)।""",
        code=r"""
            export const profiles = pgTable('profiles', {
              id: integer().primaryKey().generatedAlwaysAsIdentity(),
              settings: jsonb().$type<{ theme: 'light' | 'dark' }>().notNull(),
            });
            // insert({ settings: { theme: 'blue' } }) → TypeScript error, but raw SQL could still store it
        """, lang="typescript",
        ex_en=r"""Prefer `jsonb` over `json` in PostgreSQL: it is stored in a binary form that can be indexed and queried efficiently.""",
        ex_bn=r"""PostgreSQL-এ `json`-এর চেয়ে `jsonb` ভালো: এটা binary আকারে থাকে, তাই index করা আর দ্রুত query করা যায়।""",
        tip_en=r"""Stress "type only, no runtime check"; that is the point interviewers probe.""",
        tip_bn=r"""জোর দিয়ে বলো "শুধু type, runtime check নেই"; interviewer এটাই যাচাই করে।""",
        follow=[("How would you validate request bodies before inserting?", "Insert-এর আগে request body কীভাবে validate করবে?")],
        related=["drizzle-002"],
        refs=[("Drizzle docs — PostgreSQL column types", "https://orm.drizzle.team/docs/column-types/pg")],
    ),
    # ------------------------------------------------------------------ drizzle-q10
    Q(
        id="drizzle-q10", sub="Transactions", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["transactions", "rollback", "tx"],
        ver=DRZ_VER, vs=False, status="stable",
        q_en=r"""How do you run a transaction in Drizzle?""",
        q_bn=r"""Drizzle-এ transaction কীভাবে চালাও?""",
        a_en=r"""Call `db.transaction(async (tx) => { ... })` and run every query inside through `tx`. If the callback finishes, Drizzle commits; if it throws (or you call `tx.rollback()`), everything inside is rolled back.""",
        a_bn=r"""`db.transaction(async (tx) => { ... })` call করো আর ভেতরের প্রতিটা query `tx` দিয়ে চালাও। Callback ঠিকমতো শেষ হলে Drizzle commit করে; আর throw হলে (বা `tx.rollback()` call করলে) ভেতরের সবকিছু rollback হয়।""",
        code=r"""
            await db.transaction(async (tx) => {
              await tx.update(accounts).set({ balance: sql`${accounts.balance} - 100` }).where(eq(accounts.id, 1));
              await tx.update(accounts).set({ balance: sql`${accounts.balance} + 100` }).where(eq(accounts.id, 2));
            }); // both updates commit together, or neither does
        """, lang="typescript",
        ex_en=r"""The classic bug is using `db` instead of `tx` inside the callback: that query runs on another connection outside the transaction and is not rolled back.""",
        ex_bn=r"""সাধারণ bug হলো callback-এর ভেতরে `tx`-এর বদলে `db` ব্যবহার করা: সেই query অন্য connection-এ transaction-এর বাইরে চলে, তাই rollback হয় না।""",
        tip_en=r"""Say "commit on return, rollback on throw, always use `tx`".""",
        tip_bn=r"""বলো "return হলে commit, throw হলে rollback, আর সবসময় `tx`"।""",
        follow=[("Why keep HTTP calls out of a transaction?", "Transaction-এর ভেতরে HTTP call কেন রাখবে না?")],
        related=["drizzle-016", "drizzle-025"],
        refs=[("Drizzle docs — Transactions", "https://orm.drizzle.team/docs/transactions")],
    ),
]

if __name__ == "__main__":
    save("drizzle", "quick", QUESTIONS)
