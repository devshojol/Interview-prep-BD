# PostgreSQL batch 2 — pg-009 … pg-016
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_EXPLAIN = ("PostgreSQL docs — EXPLAIN", "https://www.postgresql.org/docs/current/sql-explain.html")
PG_USING_EXPLAIN = ("PostgreSQL docs — Using EXPLAIN", "https://www.postgresql.org/docs/current/using-explain.html")
PG_RELEASE_18 = ("PostgreSQL 18 release notes", "https://www.postgresql.org/docs/18/release-18.html")
PG_JSON_TYPES = ("PostgreSQL docs — JSON Types", "https://www.postgresql.org/docs/current/datatype-json.html")
PG_JSON_FUNCS = ("PostgreSQL docs — JSON Functions and Operators", "https://www.postgresql.org/docs/current/functions-json.html")
PG_BACKUP_DUMP = ("PostgreSQL docs — SQL Dump", "https://www.postgresql.org/docs/current/backup-dump.html")
PG_PGDUMP = ("PostgreSQL docs — pg_dump", "https://www.postgresql.org/docs/current/app-pgdump.html")
PG_BASEBACKUP = ("PostgreSQL docs — pg_basebackup", "https://www.postgresql.org/docs/current/app-pgbasebackup.html")
PG_IDENTITY = ("PostgreSQL docs — CREATE TABLE (identity & generated columns)", "https://www.postgresql.org/docs/current/sql-createtable.html")
PG_GENERATED = ("PostgreSQL docs — Generated Columns", "https://www.postgresql.org/docs/current/ddl-generated-columns.html")
PG_UUID_FUNCS = ("PostgreSQL docs — UUID Functions", "https://www.postgresql.org/docs/current/functions-uuid.html")
PG_INDEX_TYPES = ("PostgreSQL docs — Index Types", "https://www.postgresql.org/docs/current/indexes-types.html")
PG_BRIN = ("PostgreSQL docs — BRIN Indexes", "https://www.postgresql.org/docs/current/brin.html")
PG_GIN = ("PostgreSQL docs — GIN Indexes", "https://www.postgresql.org/docs/current/gin.html")
PG_EXPR_INDEX = ("PostgreSQL docs — Indexes on Expressions", "https://www.postgresql.org/docs/current/indexes-expressional.html")
PG_PARTIAL_INDEX = ("PostgreSQL docs — Partial Indexes", "https://www.postgresql.org/docs/current/indexes-partial.html")
PG_INDEX_ONLY = ("PostgreSQL docs — Index-Only Scans and Covering Indexes", "https://www.postgresql.org/docs/current/indexes-index-only-scans.html")
PG_WITH = ("PostgreSQL docs — WITH Queries (CTEs)", "https://www.postgresql.org/docs/current/queries-with.html")

QUESTIONS = [
    # ------------------------------------------------------------------ pg-009
    Q(
        id="pg-009", sub="EXPLAIN & EXPLAIN ANALYZE", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["explain", "explain-analyze", "query-planning", "production-safety"],
        ver="PostgreSQL 18", vs=True, status="stable",
        q_en=r"""A teammate runs `EXPLAIN ANALYZE DELETE FROM sessions WHERE expires_at < now();` on production "just to see the plan". What happens?""",
        q_bn=r"""একজন teammate production-এ "শুধু plan দেখার জন্য" `EXPLAIN ANALYZE DELETE FROM sessions WHERE expires_at < now();` চালালো। কী ঘটবে?""",
        options=[
            ("Nothing changes — `EXPLAIN ANALYZE` only shows the estimated plan without running the statement.",
             "কিছুই বদলাবে না — `EXPLAIN ANALYZE` statement না চালিয়ে শুধু estimated plan দেখায়।"),
            ("The `DELETE` really executes and the rows are deleted, unless it was wrapped in a transaction that is rolled back.",
             "`DELETE` সত্যিই execute হবে আর row-গুলো মুছে যাবে — যদি না এটা এমন একটা transaction-এর ভেতরে চালানো হয় যেটা পরে rollback করা হয়।"),
            ("PostgreSQL rejects it, because `EXPLAIN ANALYZE` is only allowed for `SELECT` statements.",
             "PostgreSQL এটা reject করবে, কারণ `EXPLAIN ANALYZE` শুধু `SELECT` statement-এর জন্য অনুমোদিত।"),
            ("The `DELETE` runs, but PostgreSQL automatically rolls it back after measuring the timings.",
             "`DELETE` চলবে, কিন্তু timing মাপার পর PostgreSQL নিজে থেকেই সেটা rollback করে দেবে।"),
        ],
        correct=1,
        a_en=r"""The `DELETE` really runs. `EXPLAIN` alone only plans the statement; `EXPLAIN ANALYZE` **executes** it to measure actual row counts and timings, so its side effects (deleted rows, fired triggers) are real. To analyse a write safely, wrap it: `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`.""",
        a_bn=r"""`DELETE` সত্যিই চলবে। শুধু `EXPLAIN` statement-টার plan বানায়; কিন্তু `EXPLAIN ANALYZE` আসল row সংখ্যা আর timing মাপার জন্য statement-টা **execute** করে, তাই এর side effect (row মুছে যাওয়া, trigger চলা) সত্যিকারের। কোনো write নিরাপদে analyse করতে চাইলে এভাবে মুড়ে নাও: `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`।""",
        quick_en=r"""The `DELETE` really runs and the rows are gone: `EXPLAIN ANALYZE` executes the statement to measure real timings. To inspect a write safely, wrap it in `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`.""",
        quick_bn=r"""`DELETE` সত্যিই চলে আর row-গুলো মুছে যায়: আসল timing মাপতে `EXPLAIN ANALYZE` statement-টা execute করে। কোনো write নিরাপদে দেখতে চাইলে `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`-এর ভেতরে চালাও।""",
        ex_en=r"""
            - `EXPLAIN` → estimated plan: `cost=startup..total`, estimated `rows`, `width`.
            - `EXPLAIN ANALYZE` → also `actual time`, actual `rows`, and `loops`. Comparing estimated vs actual rows is the fastest way to spot bad statistics.
            - In PostgreSQL 18, `EXPLAIN ANALYZE` includes `BUFFERS` output automatically (shared hit/read counts), and actual row counts are shown with decimals (e.g. `rows=1.00`).

            The tempting wrong answer is the last option: there is no automatic rollback. The rollback only happens if *you* open a transaction and roll it back.
        """,
        ex_bn=r"""
            - `EXPLAIN` → estimated plan: `cost=startup..total`, আনুমানিক `rows`, `width`।
            - `EXPLAIN ANALYZE` → সাথে `actual time`, আসল `rows` আর `loops`। Estimated আর actual row তুলনা করাই খারাপ statistics ধরার সবচেয়ে দ্রুত উপায়।
            - PostgreSQL 18-এ `EXPLAIN ANALYZE` নিজে থেকেই `BUFFERS` output দেখায় (shared hit/read সংখ্যা), আর actual row সংখ্যা দশমিকসহ দেখায় (যেমন `rows=1.00`)।

            লোভনীয় ভুল উত্তর হলো শেষ option-টা: কোনো automatic rollback নেই। Rollback তখনই হয় যখন *তুমি নিজে* transaction খুলে rollback করো।
        """,
        tip_en=r"""Say "ANALYZE means execute" first, then show the `BEGIN ... ROLLBACK` pattern. Mentioning the PG18 BUFFERS default shows you follow recent releases.""",
        tip_bn=r"""প্রথমেই বলো "ANALYZE মানে execute করা", তারপর `BEGIN ... ROLLBACK` pattern-টা দেখাও। PG18-এ BUFFERS default হওয়ার কথা বললে বোঝা যায় তুমি নতুন release-এর খোঁজ রাখো।""",
        extra=[dict(lang="sql", label_en="Safely analysing a write", label_bn="নিরাপদে একটা write analyse করা", src=r"""
            BEGIN;
            EXPLAIN (ANALYZE) DELETE FROM sessions WHERE expires_at < now();
            ROLLBACK;   -- the DELETE really ran inside the transaction; this undoes it
        """)],
        related=["pg-024"],
        refs=[PG_EXPLAIN, PG_USING_EXPLAIN, PG_RELEASE_18],
    ),
    # ------------------------------------------------------------------ pg-010
    Q(
        id="pg-010", sub="JSONB", diff="easy", type="comparison",
        prio="high", market="both", mins=3,
        tags=["json", "jsonb", "data-types", "gin"],
        ver="Version-independent (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""What is the difference between `json` and `jsonb` in PostgreSQL, and which one would you use?""",
        q_bn=r"""PostgreSQL-এ `json` আর `jsonb`-এর পার্থক্য কী, আর তুমি কোনটা ব্যবহার করবে?""",
        a_en=r"""
            `json` stores the input text exactly as sent — whitespace, key order, and duplicate keys are kept — and re-parses it on every access. `jsonb` stores a decomposed binary format: inserts are slightly slower, but reads and queries are much faster, duplicate keys are collapsed (the last one wins), and key order isn't preserved.

            The big win is that `jsonb` supports indexing (GIN) and rich operators such as containment `@>` and key-exists `?`. I use `jsonb` by default and only pick `json` if I truly need the original text preserved.
        """,
        a_bn=r"""
            `json` input text-টা হুবহু রেখে দেয় — whitespace, key-এর ক্রম, duplicate key সব থাকে — আর প্রতিবার access-এর সময় আবার parse করে। `jsonb` একটা decomposed binary format-এ রাখে: insert একটু ধীর, কিন্তু read আর query অনেক দ্রুত; duplicate key একটায় মিশে যায় (শেষেরটা থাকে), আর key-এর ক্রম রাখা হয় না।

            সবচেয়ে বড় সুবিধা হলো `jsonb` indexing (GIN) আর containment `@>`, key-exists `?`-এর মতো operator support করে। আমি default-ভাবে `jsonb` ব্যবহার করি; মূল text হুবহু রাখা সত্যিই দরকার হলে তবেই `json`।
        """,
        quick_en=r"""`json` keeps the exact input text (whitespace, key order, duplicate keys) and re-parses it on every read; `jsonb` stores a parsed binary form that is faster to query and supports GIN indexes and operators like `@>`. Use `jsonb` unless you must keep the original text.""",
        quick_bn=r"""`json` হুবহু input text রাখে (whitespace, key order, duplicate key) আর প্রতিবার পড়ার সময় আবার parse করে; `jsonb` parse করা binary রূপে রাখে, তাই query দ্রুত হয় আর GIN index ও `@>`-এর মতো operator চলে। মূল text রাখার দরকার না থাকলে `jsonb` নাও।""",
        ex_en=r"""
            When **not** to use JSONB:
            - Core fields you filter, join, sort, or constrain on all the time (price, status, customer_id) belong in real columns: you get types, `NOT NULL`/`CHECK`/foreign keys, and proper planner statistics.
            - PostgreSQL keeps no per-key statistics inside a `jsonb` value, so row estimates for `attrs->>'x' = ...` filters can be poor.
            - Updating one key rewrites the whole value; very large, frequently-updated documents cause write amplification.

            Good uses: flexible product attributes, third-party webhook payloads, sparse user settings — usually next to normal columns (a hybrid model).
        """,
        ex_bn=r"""
            কখন JSONB **ব্যবহার করবে না**:
            - যে মূল field-গুলো দিয়ে সবসময় filter, join, sort বা constraint দাও (price, status, customer_id) — সেগুলো আসল column-এ রাখো: type, `NOT NULL`/`CHECK`/foreign key আর ঠিকঠাক planner statistics পাবে।
            - `jsonb` value-এর ভেতরের key-গুলোর জন্য PostgreSQL আলাদা statistics রাখে না, তাই `attrs->>'x' = ...` ধরনের filter-এ row estimate খারাপ হতে পারে।
            - একটা key update করলেও পুরো value আবার লেখা হয়; অনেক বড় আর ঘনঘন update হওয়া document-এ write amplification হয়।

            ভালো ব্যবহার: flexible product attribute, third-party webhook payload, sparse user setting — সাধারণত সাধারণ column-এর পাশাপাশি (hybrid model)।
        """,
        tip_en=r"""Give the storage difference in one line, then pivot to "when not to use JSONB" — interviewers often probe whether you'd dump everything into a JSON column.""",
        tip_bn=r"""Storage-এর পার্থক্য এক লাইনে বলো, তারপর "কখন JSONB ব্যবহার করব না"-তে চলে যাও — interviewer প্রায়ই যাচাই করে তুমি সবকিছু একটা JSON column-এ ঢেলে দেবে কিনা।""",
        mist_en=r"""Treating `jsonb` as a replacement for schema design, or expecting `jsonb` to preserve key order and duplicate keys.""",
        mist_bn=r"""`jsonb`-কে schema design-এর বিকল্প ভাবা, অথবা আশা করা যে `jsonb` key-এর ক্রম আর duplicate key রেখে দেবে।""",
        code=r"""
            SELECT '{"b": 1, "a": 2, "a": 3}'::json  AS j,
                   '{"b": 1, "a": 2, "a": 3}'::jsonb AS jb;
        """,
        lang="sql",
        output=r"""
                        j             |        jb
            --------------------------+------------------
             {"b": 1, "a": 2, "a": 3} | {"a": 3, "b": 1}
        """,
        follow=[
            ("How would you index a `jsonb` column for `@>` queries?", "`@>` query-র জন্য `jsonb` column-এ কীভাবে index দেবে?"),
            ("How do you query a single numeric key efficiently with a range filter?", "একটা numeric key-তে range filter দিয়ে কীভাবে দ্রুত query করবে?"),
        ],
        related=["pg-016"],
        refs=[PG_JSON_TYPES, PG_JSON_FUNCS],
    ),
    # ------------------------------------------------------------------ pg-011
    Q(
        id="pg-011", sub="Backup & Recovery", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["backup", "pg_dump", "pg_restore", "pg_basebackup"],
        ver="Version-independent (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""How do you back up and restore a single PostgreSQL database? How is `pg_dump` different from `pg_basebackup`?""",
        q_bn=r"""একটা PostgreSQL database-এর backup আর restore কীভাবে করো? `pg_dump` আর `pg_basebackup`-এর পার্থক্য কী?""",
        a_en=r"""
            For one database I use `pg_dump`, which produces a **logical** backup — SQL or an archive of the schema and data — from a consistent snapshot without blocking normal reads and writes. I prefer the custom format (`-Fc`): it's compressed and lets `pg_restore` restore selectively and in parallel (`-j`).

            `pg_basebackup` takes a **physical** copy of the whole cluster's data files. It's what you use to build a streaming replica or, together with archived WAL, to do point-in-time recovery.

            Rule of thumb: `pg_dump` for portable, per-database backups and migrations between major versions; physical backups + WAL archiving for production disaster recovery. And a backup isn't real until you've tested a restore.
        """,
        a_bn=r"""
            একটা database-এর জন্য আমি `pg_dump` ব্যবহার করি — এটা একটা **logical** backup বানায় (SQL অথবা schema ও data-র archive), একটা consistent snapshot থেকে, সাধারণ read/write block না করে। আমি custom format (`-Fc`) পছন্দ করি: compressed হয়, আর `pg_restore` দিয়ে বেছে বেছে এবং parallel-এ (`-j`) restore করা যায়।

            `pg_basebackup` পুরো cluster-এর data file-গুলোর একটা **physical** copy নেয়। Streaming replica বানাতে, বা archived WAL-এর সাথে মিলিয়ে point-in-time recovery করতে এটাই লাগে।

            সহজ নিয়ম: portable, per-database backup আর major version-এর মধ্যে migration-এর জন্য `pg_dump`; production disaster recovery-র জন্য physical backup + WAL archiving। আর restore test না করা পর্যন্ত backup আসলে backup না।
        """,
        quick_en=r"""`pg_dump` makes a logical backup of one database from a consistent snapshot without blocking normal reads and writes; use `-Fc` so `pg_restore` can restore selectively and in parallel. `pg_basebackup` copies the whole cluster physically, for replicas and point-in-time recovery with WAL. Always test the restore.""",
        quick_bn=r"""`pg_dump` একটা database-এর logical backup নেয় consistent snapshot থেকে, সাধারণ read/write block না করে; `-Fc` দিলে `pg_restore` বেছে বেছে আর parallel-এ restore করতে পারে। `pg_basebackup` পুরো cluster-এর physical copy নেয়, replica আর WAL দিয়ে point-in-time recovery-র জন্য। Restore সবসময় test করো।""",
        ex_en=r"""
            - `pg_dump` does not include cluster-wide objects such as roles and tablespaces — dump them with `pg_dumpall --globals-only`.
            - It takes `ACCESS SHARE` locks, so it doesn't block DML, but it does block DDL like `ALTER TABLE`/`DROP TABLE` on dumped tables, and it holds a long transaction (which delays VACUUM cleanup) on big databases.
            - A dump is a snapshot from one moment: restoring it loses everything written after the dump started. That's why production also needs WAL-based PITR.
            - For very large databases, logical dumps and restores get slow (indexes must be rebuilt on restore); physical backups scale better.
        """,
        ex_bn=r"""
            - `pg_dump`-এ role আর tablespace-এর মতো cluster-wide object থাকে না — এগুলোর জন্য `pg_dumpall --globals-only` চালাও।
            - এটা `ACCESS SHARE` lock নেয়, তাই DML block করে না, কিন্তু dump হতে থাকা table-এ `ALTER TABLE`/`DROP TABLE`-এর মতো DDL block করে; আর বড় database-এ লম্বা একটা transaction ধরে রাখে (যা VACUUM-এর cleanup দেরি করায়)।
            - Dump হলো এক মুহূর্তের snapshot: restore করলে dump শুরুর পরের সব write হারিয়ে যায়। এজন্যই production-এ WAL-based PITR-ও লাগে।
            - খুব বড় database-এ logical dump আর restore ধীর হয়ে যায় (restore-এর সময় index আবার বানাতে হয়); physical backup বেশি ভালোভাবে scale করে।
        """,
        tip_en=r"""Frame it as logical vs physical, then mention globals, restore testing, and that dumps alone can't give you point-in-time recovery.""",
        tip_bn=r"""Logical বনাম physical — এভাবে সাজিয়ে বলো, তারপর globals, restore test আর শুধু dump দিয়ে যে point-in-time recovery হয় না — এগুলো উল্লেখ করো।""",
        mist_en=r"""Forgetting roles (`--globals-only`), never testing restores, or relying only on nightly dumps for a system that can't lose a day of data.""",
        mist_bn=r"""Role-এর কথা ভুলে যাওয়া (`--globals-only`), কখনো restore test না করা, অথবা এক দিনের data হারানো যায় না এমন system-এ শুধু রাতের dump-এর উপর ভরসা করা।""",
        code=r"""
            # logical backup of one database (custom format: compressed, selective/parallel restore)
            pg_dump -h db.internal -U backup_user -d shop -Fc -f shop_2026-10-12.dump

            # roles and tablespaces are cluster-wide, so dump them separately
            pg_dumpall -h db.internal -U postgres --globals-only -f globals.sql

            # restore into a new, empty database with 4 parallel jobs
            createdb -h staging-db -U postgres shop_restore
            pg_restore -h staging-db -U postgres -d shop_restore -j 4 shop_2026-10-12.dump

            # physical base backup of the whole cluster (for replicas / PITR)
            pg_basebackup -h db.internal -U replicator -D /backups/base_2026-10-12 -Ft -z -P
        """,
        lang="bash",
        follow=[
            ("How would you recover a table that someone accidentally emptied at 14:32 today?", "আজ ১৪:৩২-এ কেউ ভুল করে একটা table খালি করে ফেলেছে — কীভাবে recover করবে?"),
            ("How do you upgrade PostgreSQL 16 to 18 — `pg_dump`/`pg_restore` or `pg_upgrade`?", "PostgreSQL 16 থেকে 18-এ কীভাবে upgrade করবে — `pg_dump`/`pg_restore` নাকি `pg_upgrade`?"),
        ],
        related=["pg-026"],
        refs=[PG_BACKUP_DUMP, PG_PGDUMP, PG_BASEBACKUP],
    ),
    # ------------------------------------------------------------------ pg-012
    Q(
        id="pg-012", sub="Data Types & Keys (PostgreSQL 18)", diff="medium", type="comparison",
        prio="high", market="both", mins=5,
        tags=["identity", "serial", "uuidv7", "generated-columns", "postgresql-18"],
        ver="PostgreSQL 18", vs=True, status="version-specific",
        q_en=r"""You're designing a new table on PostgreSQL 18. Compare `serial` vs identity columns, `gen_random_uuid()` vs `uuidv7()` for keys, and stored vs virtual generated columns. What would you choose?""",
        q_bn=r"""PostgreSQL 18-এ একটা নতুন table design করছ। `serial` বনাম identity column, key-এর জন্য `gen_random_uuid()` বনাম `uuidv7()`, আর stored বনাম virtual generated column — তুলনা করো। তুমি কোনগুলো বেছে নেবে?""",
        a_en=r"""
            - **Identity over serial.** `GENERATED ALWAYS AS IDENTITY` is SQL-standard, its sequence is tied to the column (no separate grants, cleaner copies/drops), and `ALWAYS` rejects accidental manual ids. `serial` still works but is the legacy approach.
            - **UUIDs only when you need them** (ids generated outside the DB, merging data across systems, non-guessable public ids). Then prefer **`uuidv7()`** (new in PG18): it's time-ordered, so inserts land at the "right edge" of the B-tree like a `bigint`. `gen_random_uuid()` (v4) is fully random, so inserts hit random index pages — more page splits, worse cache hit rate, more WAL on big tables.
            - **Generated columns:** in PG18 the default is **virtual** — computed on read, no storage. Use `STORED` when you need to index the value (PG18 can't index virtual generated columns) or when the expression is expensive to recompute on every read.
        """,
        a_bn=r"""
            - **Serial-এর বদলে identity।** `GENERATED ALWAYS AS IDENTITY` SQL-standard, এর sequence column-এর সাথে বাঁধা থাকে (আলাদা grant লাগে না, copy/drop পরিষ্কার), আর `ALWAYS` ভুল করে হাতে id দেওয়া আটকায়। `serial` এখনো কাজ করে, কিন্তু এটা legacy পদ্ধতি।
            - **UUID শুধু দরকার হলে** (DB-র বাইরে id তৈরি হয়, বিভিন্ন system-এর data merge করতে হয়, অনুমান-অযোগ্য public id লাগে)। তখন **`uuidv7()`** (PG18-এ নতুন) বেছে নাও: এটা time-ordered, তাই insert B-tree-র "ডান প্রান্তে" গিয়ে পড়ে, ঠিক `bigint`-এর মতো। `gen_random_uuid()` (v4) পুরোপুরি random, তাই insert এলোমেলো index page-এ পড়ে — বড় table-এ বেশি page split, cache hit কম, WAL বেশি।
            - **Generated column:** PG18-এ default হলো **virtual** — read-এর সময় হিসাব হয়, storage লাগে না। Value-টা index করতে হলে (PG18 virtual generated column index করতে পারে না) বা expression প্রতিবার হিসাব করা ব্যয়বহুল হলে `STORED` ব্যবহার করো।
        """,
        quick_en=r"""Prefer `GENERATED ALWAYS AS IDENTITY` over legacy `serial`. Use UUIDs only when you need them, and then PG18's time-ordered `uuidv7()` over random `gen_random_uuid()` for index locality. Generated columns are virtual by default in PG18; use `STORED` when you need to index the value.""",
        quick_bn=r"""Legacy `serial`-এর বদলে `GENERATED ALWAYS AS IDENTITY` নাও। UUID শুধু দরকার হলে নাও, আর তখন index locality-র জন্য random `gen_random_uuid()`-এর বদলে PG18-এর time-ordered `uuidv7()`। PG18-এ generated column default-ভাবে virtual; value-টার index লাগলে `STORED` দাও।""",
        ex_en=r"""
            - `bigint` identity is still the smallest and fastest key (8 bytes vs 16 for a UUID). A common pattern is a `bigint` internal key plus a UUID public id.
            - UUIDv7 embeds the creation time; `uuid_extract_timestamp(id)` returns it. Don't use it where revealing creation time is a privacy problem.
            - With `GENERATED ALWAYS`, inserting an explicit id fails unless you write `OVERRIDING SYSTEM VALUE` (useful for data migrations). `GENERATED BY DEFAULT` allows manual values.
            - Generated-column rules: the expression must be immutable, can't reference other generated columns or other tables; virtual ones may only use built-in functions and types. Before PG18 only `STORED` existed and the keyword was mandatory, so `GENERATED ALWAYS AS (...)` without `STORED` is a syntax error on PostgreSQL 12–17 — watch this when the same migration must run on older servers.
            - Bangladesh example: a 15% VAT computed from `subtotal` is a natural generated column — no app can store an inconsistent `total`.
        """,
        ex_bn=r"""
            - `bigint` identity এখনো সবচেয়ে ছোট আর দ্রুত key (UUID-এর 16 byte-এর বিপরীতে 8 byte)। একটা প্রচলিত pattern: ভেতরে `bigint` key, বাইরে দেখানোর জন্য UUID public id।
            - UUIDv7-এর ভেতরে তৈরির সময় লুকানো থাকে; `uuid_extract_timestamp(id)` সেটা বের করে দেয়। তৈরির সময় প্রকাশ পাওয়া privacy সমস্যা হলে এটা ব্যবহার কোরো না।
            - `GENERATED ALWAYS`-এ নিজে id দিয়ে insert করলে fail হয়, যদি না `OVERRIDING SYSTEM VALUE` লেখো (data migration-এ কাজে লাগে)। `GENERATED BY DEFAULT` হাতে value দিতে দেয়।
            - Generated column-এর নিয়ম: expression immutable হতে হবে, অন্য generated column বা অন্য table refer করা যাবে না; virtual হলে শুধু built-in function আর type ব্যবহার করা যায়। PG18-এর আগে শুধু `STORED` ছিল আর keyword-টা বাধ্যতামূলক ছিল, তাই PostgreSQL 12–17-এ `STORED` ছাড়া `GENERATED ALWAYS AS (...)` লিখলে syntax error হয় — একই migration পুরনো server-এও চালাতে হলে এটা খেয়াল রাখো।
            - বাংলাদেশি উদাহরণ: `subtotal` থেকে 15% VAT হিসাব করা generated column-এর জন্য একদম মানানসই — কোনো app ভুল `total` রাখতে পারবে না।
        """,
        tip_en=r"""Structure it as three mini-comparisons, each ending with your pick and one reason. The "random UUID inserts fragment the B-tree" point is what separates senior answers.""",
        tip_bn=r"""তিনটা ছোট তুলনা হিসেবে সাজাও, প্রতিটার শেষে তোমার পছন্দ আর একটা কারণ বলো। "Random UUID insert B-tree-কে এলোমেলো করে" — এই কথাটাই senior-level উত্তরকে আলাদা করে।""",
        mist_en=r"""Using UUIDv4 primary keys "for scale" without knowing the index-locality cost, or expecting to index a virtual generated column in PG18.""",
        mist_bn=r"""Index locality-র খরচ না জেনে "scale-এর জন্য" UUIDv4 primary key ব্যবহার করা, অথবা PG18-এ virtual generated column-এ index দেওয়া যাবে বলে আশা করা।""",
        code=r"""
            CREATE TABLE orders (
              id          uuid PRIMARY KEY DEFAULT uuidv7(),           -- PG18: time-ordered UUID
              order_no    bigint GENERATED ALWAYS AS IDENTITY UNIQUE,  -- human-friendly number
              customer_id bigint NOT NULL,
              subtotal    numeric(12,2) NOT NULL,
              vat_rate    numeric(4,3)  NOT NULL DEFAULT 0.150,
              -- VIRTUAL by default in PG18: computed on read, no storage, not indexable
              vat         numeric(12,2) GENERATED ALWAYS AS (round(subtotal * vat_rate, 2)),
              -- STORED: written on insert/update, can be indexed
              total       numeric(12,2) GENERATED ALWAYS AS (subtotal + round(subtotal * vat_rate, 2)) STORED,
              created_at  timestamptz NOT NULL DEFAULT now()
            );

            CREATE INDEX ON orders (total);

            SELECT uuid_extract_timestamp(id) AS id_created_at, order_no, vat, total FROM orders;
        """,
        lang="sql",
        follow=[
            ("How would you migrate an existing `serial` column to an identity column?", "একটা existing `serial` column-কে identity column-এ কীভাবে migrate করবে?"),
            ("Why would a random UUID primary key slow down inserts on a 500-million-row table?", "৫০ কোটি row-এর table-এ random UUID primary key কেন insert ধীর করে দিতে পারে?"),
        ],
        related=["pg-003", "pg-013"],
        refs=[PG_UUID_FUNCS, PG_GENERATED, PG_IDENTITY],
    ),
    # ------------------------------------------------------------------ pg-013
    Q(
        id="pg-013", sub="Index Types", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["b-tree", "gin", "gist", "brin", "hash"],
        ver="PostgreSQL 18", vs=False, status="stable",
        q_en=r"""PostgreSQL offers B-tree, Hash, GIN, GiST, SP-GiST, and BRIN indexes. When would you use each?""",
        q_bn=r"""PostgreSQL-এ B-tree, Hash, GIN, GiST, SP-GiST আর BRIN index আছে। কোনটা কখন ব্যবহার করবে?""",
        a_en=r"""
            - **B-tree (default):** equality, ranges, `ORDER BY`, uniqueness. Covers most needs, including multicolumn indexes.
            - **Hash:** equality only. Smaller for long keys in some cases, but it can't do ranges, sorting, or uniqueness — B-tree is usually fine.
            - **GIN (Generalized Inverted Index):** "does this value contain X?" — `jsonb` containment (`@>`), arrays, full-text search (`tsvector`), and trigram search with `pg_trgm` for `LIKE '%abc%'`. Fast reads, slower and bigger writes.
            - **GiST / SP-GiST:** geometric and range data — overlaps (`&&`), nearest-neighbour (`<->`), PostGIS, and `EXCLUDE` constraints (e.g. no overlapping bookings).
            - **BRIN (Block Range INdex):** huge, append-only tables where the column follows the physical order, like `created_at` on an events/log table. It stores min/max per block range, so it's tiny.
        """,
        a_bn=r"""
            - **B-tree (default):** equality, range, `ORDER BY`, uniqueness। Multicolumn index সহ বেশিরভাগ প্রয়োজন এটাতেই মেটে।
            - **Hash:** শুধু equality। কিছু ক্ষেত্রে লম্বা key-এর জন্য ছোট হয়, কিন্তু range, sorting বা uniqueness পারে না — সাধারণত B-tree-ই যথেষ্ট।
            - **GIN (Generalized Inverted Index):** "এই value-এর ভেতরে X আছে কি?" — `jsonb` containment (`@>`), array, full-text search (`tsvector`), আর `LIKE '%abc%'`-এর জন্য `pg_trgm` দিয়ে trigram search। Read দ্রুত, write ধীর আর index বড়।
            - **GiST / SP-GiST:** geometric আর range data — overlap (`&&`), nearest-neighbour (`<->`), PostGIS, আর `EXCLUDE` constraint (যেমন booking overlap করতে পারবে না)।
            - **BRIN (Block Range INdex):** বিশাল, append-only table যেখানে column-এর value physical order মেনে চলে — যেমন events/log table-এর `created_at`। প্রতি block range-এর min/max রাখে, তাই খুবই ছোট।
        """,
        quick_en=r"""B-tree is the default for equality, ranges, sorting and uniqueness; Hash is equality only. GIN handles "contains" searches (`jsonb`, arrays, full-text, trigrams), GiST/SP-GiST handle geometric and range data like overlaps, and BRIN is a tiny index for huge append-only tables ordered by a column like `created_at`.""",
        quick_bn=r"""B-tree হলো default: equality, range, sorting আর uniqueness-এর জন্য; Hash শুধু equality। GIN "contains" ধরনের search সামলায় (`jsonb`, array, full-text, trigram), GiST/SP-GiST geometric আর range data (যেমন overlap), আর BRIN হলো `created_at`-এর মতো column-এ সাজানো বিশাল append-only table-এর জন্য খুব ছোট index।""",
        ex_en=r"""
            - BRIN only works well when values correlate with physical row order; after lots of updates or out-of-order inserts it degrades into scanning most of the table. Check `pg_stats.correlation` for the column.
            - For `jsonb`, the `jsonb_path_ops` GIN operator class is smaller and faster for `@>` but doesn't support key-exists operators (`?`, `?|`, `?&`); the default `jsonb_ops` does.
            - Partial (`WHERE status = 'pending'`), expression (`lower(email)`), and covering (`INCLUDE (...)`) indexes are *features* you can combine with these types, not separate types.
            - PostgreSQL 18 adds **skip scan** for multicolumn B-trees, so an index on `(a, b)` can sometimes serve `WHERE b = ?` when `a` has few distinct values.
            - Extensions add more, e.g. HNSW/IVFFlat from pgvector for vector similarity.
        """,
        ex_bn=r"""
            - BRIN তখনই ভালো কাজ করে যখন value-গুলো physical row order-এর সাথে মিলে চলে; অনেক update বা এলোমেলো insert-এর পর এটা প্রায় পুরো table scan-এ পরিণত হয়। Column-টার `pg_stats.correlation` দেখে নাও।
            - `jsonb`-এর জন্য `jsonb_path_ops` GIN operator class `@>`-এর জন্য ছোট আর দ্রুত, কিন্তু key-exists operator (`?`, `?|`, `?&`) support করে না; default `jsonb_ops` করে।
            - Partial (`WHERE status = 'pending'`), expression (`lower(email)`) আর covering (`INCLUDE (...)`) index হলো *feature*, যেগুলো এই type-গুলোর সাথে মেলানো যায় — আলাদা type নয়।
            - PostgreSQL 18-এ multicolumn B-tree-র জন্য **skip scan** এসেছে, ফলে `(a, b)`-এর index কখনো কখনো `WHERE b = ?` query-ও সামলাতে পারে, যদি `a`-র distinct value কম থাকে।
            - Extension আরও type যোগ করে, যেমন vector similarity-র জন্য pgvector-এর HNSW/IVFFlat।
        """,
        tip_en=r"""Pair each index type with a concrete query it accelerates. Ending with "partial/expression/covering are features, not types" shows precise understanding.""",
        tip_bn=r"""প্রতিটা index type-এর সাথে একটা concrete query জুড়ে দাও যেটা এটা দ্রুত করে। শেষে "partial/expression/covering আসলে feature, type নয়" বললে বোঝা যায় তোমার ধারণা পরিষ্কার।""",
        mist_en=r"""Using BRIN on a randomly-ordered column, or expecting a B-tree to speed up `LIKE '%term%'` (use `pg_trgm` + GIN, or full-text search).""",
        mist_bn=r"""এলোমেলো ক্রমের column-এ BRIN ব্যবহার করা, অথবা আশা করা যে B-tree `LIKE '%term%'` দ্রুত করবে (এর জন্য `pg_trgm` + GIN, বা full-text search লাগে)।""",
        code=r"""
            -- B-tree (default): equality, ranges, sorting
            CREATE INDEX ON orders (customer_id, created_at);

            -- GIN: containment on jsonb, arrays, full-text, trigram LIKE '%...%'
            CREATE INDEX ON products USING gin (attrs jsonb_path_ops);
            CREATE INDEX ON articles USING gin (to_tsvector('english', body));
            CREATE EXTENSION IF NOT EXISTS pg_trgm;
            CREATE INDEX ON customers USING gin (name gin_trgm_ops);

            -- GiST: ranges / geometry / nearest neighbour / exclusion constraints
            CREATE INDEX ON bookings USING gist (during);

            -- BRIN: huge append-only table, values follow insertion order
            CREATE INDEX ON events USING brin (created_at);

            -- Hash: equality only
            CREATE INDEX ON sessions USING hash (token);
        """,
        lang="sql",
        follow=[
            ("Why might a BRIN index stop being useful after a large backfill?", "বড় একটা backfill-এর পর BRIN index কেন আর কাজে নাও লাগতে পারে?"),
            ("What are the write-side costs of GIN indexes and how does `fastupdate` help?", "GIN index-এর write-এর দিকের খরচ কী, আর `fastupdate` কীভাবে সাহায্য করে?"),
        ],
        related=["pg-005", "pg-014", "pg-028", "pg-016"],
        refs=[PG_INDEX_TYPES, PG_GIN, PG_BRIN],
    ),
    # ------------------------------------------------------------------ pg-014
    Q(
        id="pg-014", sub="Expression, Partial & Covering Indexes", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["expression-index", "partial-index", "covering-index", "sargability", "explain"],
        ver="PostgreSQL 18", vs=False, status="stable",
        q_en=r"""The login query below is slow even though `users.email` has an index. The plan shows a sequential scan on a 100,000-row table. What's wrong, and how would you fix it?""",
        q_bn=r"""নিচের login query-টা ধীর, যদিও `users.email`-এ index আছে। Plan-এ ১,০০,০০০ row-এর table-এ sequential scan দেখা যাচ্ছে। সমস্যা কোথায়, আর কীভাবে ঠিক করবে?""",
        a_en=r"""
            The query filters on `lower(email)`, but the index is on plain `email`. A B-tree stores the raw column values, so it can't answer a condition on a *function* of the column — the predicate isn't sargable for that index, and PostgreSQL must compute `lower(email)` for every row.

            Fix: create an **expression index** that matches the expression exactly — `CREATE INDEX CONCURRENTLY ... ON users (lower(email))` — then `ANALYZE` so the planner has statistics on the expression. If emails must be unique case-insensitively, make it a `UNIQUE` expression index, which also enforces the rule.

            I'd go further: if most queries skip soft-deleted users, a **partial index** (`WHERE deleted_at IS NULL`) is smaller. A covering index (`INCLUDE (...)`) can even enable an index-only scan, but only if it holds every column the query reads.
        """,
        a_bn=r"""
            Query filter করছে `lower(email)` দিয়ে, কিন্তু index আছে সাধারণ `email`-এর উপর। B-tree column-এর কাঁচা value রাখে, তাই column-এর উপর *function* লাগানো condition সে সামলাতে পারে না — ওই index-এর জন্য predicate-টা sargable নয়, তাই PostgreSQL-কে প্রতিটা row-এর জন্য `lower(email)` হিসাব করতে হয়।

            সমাধান: হুবহু একই expression দিয়ে একটা **expression index** বানাও — `CREATE INDEX CONCURRENTLY ... ON users (lower(email))` — তারপর `ANALYZE` চালাও যাতে planner expression-টার statistics পায়। Email যদি case-insensitive-ভাবে unique হতে হয়, তাহলে `UNIQUE` expression index বানাও — এতে rule-টাও enforce হয়।

            আমি আরেকটু এগোব: বেশিরভাগ query যদি soft-deleted user বাদ দেয়, তাহলে একটা **partial index** (`WHERE deleted_at IS NULL`) ছোট হয়। Covering index (`INCLUDE (...)`) দিলে index-only scan-ও সম্ভব, তবে শুধু তখনই যখন query যত column পড়ে সবগুলো index-এ থাকে।
        """,
        quick_en=r"""The query filters on `lower(email)` but the index stores plain `email`, so PostgreSQL computes the function for every row and scans the table. Fix: an expression index on `(lower(email))`, created `CONCURRENTLY` and made `UNIQUE` if emails must be unique case-insensitively, then `ANALYZE`.""",
        quick_bn=r"""Query filter করছে `lower(email)` দিয়ে, কিন্তু index-এ আছে সাধারণ `email`, তাই PostgreSQL প্রতিটা row-এর জন্য function হিসাব করে পুরো table scan করে। Fix: `(lower(email))`-এর ওপর expression index, `CONCURRENTLY` দিয়ে বানাও, case-insensitive unique দরকার হলে `UNIQUE` করো, তারপর `ANALYZE`।""",
        ex_en=r"""
            - The expression in the query must match the index expression (`lower(email)`, not `upper(email)` or `lower(trim(email))`).
            - Use `CONCURRENTLY` on a live table so writes aren't blocked during the build. It can't run inside a transaction block, and a failed build leaves an `INVALID` index you must drop and recreate.
            - A partial index is only used when the query's `WHERE` clause implies the index predicate — so the query must also say `deleted_at IS NULL`.
            - `INCLUDE` columns are stored in the leaf pages but aren't part of the search key. An index-only scan needs **every** column the query reads in the index — here `id` and `password_hash`, plus the raw `email` column, because the planner only considers index-only scans on an expression index like `lower(email)` when the underlying column is available too. It also needs an up-to-date visibility map (VACUUM). For a single-row login lookup the gain is small; the partial index is the bigger win.
            - Alternatives: normalise emails to lowercase on write (simplest), or use the `citext` extension type.
        """,
        ex_bn=r"""
            - Query-র expression index-এর expression-এর সাথে হুবহু মিলতে হবে (`lower(email)`, `upper(email)` বা `lower(trim(email))` নয়)।
            - Live table-এ `CONCURRENTLY` ব্যবহার করো, যাতে build-এর সময় write block না হয়। এটা transaction block-এর ভেতরে চলে না, আর build fail করলে একটা `INVALID` index থেকে যায় যেটা drop করে আবার বানাতে হয়।
            - Partial index তখনই ব্যবহার হয় যখন query-র `WHERE` থেকে index-এর predicate বোঝা যায় — তাই query-তেও `deleted_at IS NULL` থাকতে হবে।
            - `INCLUDE` column leaf page-এ রাখা হয়, কিন্তু search key-এর অংশ নয়। Index-only scan-এর জন্য query যত column পড়ে **সবগুলো** index-এ থাকতে হয় — এখানে `id` আর `password_hash`, সাথে কাঁচা `email` column-ও, কারণ `lower(email)`-এর মতো expression index-এ planner তখনই index-only scan বিবেচনা করে যখন মূল column-টাও index-এ পাওয়া যায়। Visibility map-ও up to date থাকতে হয় (VACUUM)। একটা row-এর login lookup-এ লাভ সামান্য; আসল লাভ partial index-এ।
            - বিকল্প: write-এর সময়ই email lowercase করে রাখা (সবচেয়ে সহজ), অথবা `citext` extension type ব্যবহার করা।
        """,
        tip_en=r"""Name the root cause in one word — "sargability" — then give the exact fix and the `CONCURRENTLY` detail. Interviewers love hearing you'd verify with `EXPLAIN` afterwards.""",
        tip_bn=r"""Root cause এক শব্দে বলো — "sargability" — তারপর হুবহু fix আর `CONCURRENTLY`-র খুঁটিনাটি বলো। পরে `EXPLAIN` দিয়ে যাচাই করবে বললে interviewer খুশি হয়।""",
        mist_en=r"""Creating the expression index without `CONCURRENTLY` on a busy production table (blocking writes), or writing the query with a slightly different expression than the index.""",
        mist_bn=r"""Busy production table-এ `CONCURRENTLY` ছাড়া expression index বানানো (write block হয়ে যায়), অথবা index-এর চেয়ে সামান্য আলাদা expression দিয়ে query লেখা।""",
        code=r"""
            CREATE INDEX idx_users_email ON users (email);

            EXPLAIN SELECT id, password_hash
            FROM users
            WHERE lower(email) = 'rahim@example.com';

            --                         QUERY PLAN
            -- -----------------------------------------------------------
            --  Seq Scan on users  (cost=0.00..2637.00 rows=500 width=41)
            --    Filter: (lower(email) = 'rahim@example.com'::text)
        """,
        lang="sql",
        extra=[dict(lang="sql", label_en="Fix: expression index (plus partial/covering variant)",
                    label_bn="সমাধান: expression index (সাথে partial/covering রূপ)", src=r"""
            -- matches the query expression exactly; UNIQUE also enforces case-insensitive uniqueness
            CREATE UNIQUE INDEX CONCURRENTLY idx_users_lower_email ON users (lower(email));
            ANALYZE users;

            EXPLAIN SELECT id, password_hash FROM users WHERE lower(email) = 'rahim@example.com';
            --  Index Scan using idx_users_lower_email on users  (cost=0.42..8.44 rows=1 width=41)
            --    Index Cond: (lower(email) = 'rahim@example.com'::text)

            -- variant: only active users, covering every column the query reads
            -- (email is included because index-only scans on lower(email) need the raw column too)
            CREATE INDEX CONCURRENTLY idx_users_active_login
              ON users (lower(email)) INCLUDE (id, password_hash, email)
              WHERE deleted_at IS NULL;

            SELECT id, password_hash FROM users
            WHERE lower(email) = $1 AND deleted_at IS NULL;   -- query must repeat the predicate
        """)],
        follow=[
            ("Why is `WHERE created_at::date = '2026-10-12'` slow, and how would you rewrite it?", "`WHERE created_at::date = '2026-10-12'` কেন ধীর, আর কীভাবে আবার লিখবে?"),
            ("What happens if `CREATE INDEX CONCURRENTLY` fails halfway?", "`CREATE INDEX CONCURRENTLY` মাঝপথে fail করলে কী হয়?"),
        ],
        related=["pg-005", "pg-013", "pg-025"],
        refs=[PG_EXPR_INDEX, PG_PARTIAL_INDEX, PG_INDEX_ONLY],
    ),
    # ------------------------------------------------------------------ pg-015
    Q(
        id="pg-015", sub="CTEs", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["cte", "with", "materialized", "query-planning"],
        ver="PostgreSQL 12+ (current: 18)", vs=True, status="stable",
        q_en=r"""On PostgreSQL 18, how is the CTE in this query executed? Assume an index exists on `orders (customer_id, created_at)`.""",
        q_bn=r"""PostgreSQL 18-এ এই query-র CTE কীভাবে execute হবে? ধরে নাও `orders (customer_id, created_at)`-এ একটা index আছে।""",
        code=r"""
            WITH recent AS (
              SELECT * FROM orders
              WHERE created_at > now() - interval '7 days'
            )
            SELECT * FROM recent
            WHERE customer_id = 42;
        """,
        lang="sql",
        options=[
            ("It's always materialized first (an \"optimization fence\"), so all recent orders are computed before `customer_id = 42` is applied.",
             "এটা সবসময় আগে materialize হয় (একটা \"optimization fence\"), তাই `customer_id = 42` প্রয়োগের আগে সব recent order হিসাব হয়।"),
            ("Because it's non-recursive, side-effect-free, and referenced once, the planner inlines it into the outer query, so both conditions can use the index.",
             "যেহেতু এটা non-recursive, side-effect-free আর মাত্র একবার reference হয়েছে, planner এটাকে outer query-র ভেতরে inline করে দেয়, ফলে দুটো condition-ই index ব্যবহার করতে পারে।"),
            ("It's materialized only if its result fits in `work_mem`; otherwise it's inlined.",
             "এর result `work_mem`-এ এঁটে গেলে তবেই materialize হয়; না হলে inline হয়।"),
            ("PostgreSQL inlines every CTE, even ones referenced several times or containing `DELETE ... RETURNING`.",
             "PostgreSQL সব CTE inline করে, এমনকি যেগুলো কয়েকবার reference হয় বা যেগুলোর ভেতরে `DELETE ... RETURNING` আছে সেগুলোও।"),
        ],
        correct=1,
        a_en=r"""Since PostgreSQL 12, a non-recursive, side-effect-free CTE that is referenced only once is **inlined** like a subquery. The planner sees `created_at > ... AND customer_id = 42` together and can use the `(customer_id, created_at)` index.""",
        a_bn=r"""PostgreSQL 12 থেকে, non-recursive আর side-effect-free CTE যদি মাত্র একবার reference হয়, তাহলে সেটা subquery-র মতো **inline** হয়ে যায়। Planner `created_at > ... AND customer_id = 42` একসাথে দেখে, তাই `(customer_id, created_at)` index ব্যবহার করতে পারে।""",
        quick_en=r"""It is inlined into the outer query: since PostgreSQL 12 a non-recursive, side-effect-free CTE referenced once is treated like a subquery. So the planner sees both conditions together and can use the `(customer_id, created_at)` index.""",
        quick_bn=r"""এটা outer query-র ভেতরে inline হয়ে যায়: PostgreSQL 12 থেকে non-recursive, side-effect ছাড়া আর একবার reference করা CTE subquery-র মতো ধরা হয়। তাই planner দুটো condition একসাথে দেখে আর `(customer_id, created_at)` index ব্যবহার করতে পারে।""",
        ex_en=r"""
            The first option was true **before PostgreSQL 12** — CTEs were always materialized, and many old blog posts still describe them as optimization fences. That's why it's tempting.

            Current rules:
            - Referenced once, no side effects, not recursive → inlined by default.
            - Referenced **more than once** → materialized by default (computed once, reused).
            - Recursive CTEs and data-modifying CTEs (`INSERT/UPDATE/DELETE ... RETURNING` inside `WITH`) are always executed exactly once.
            - You can override: `WITH x AS MATERIALIZED (...)` forces a fence (handy to compute an expensive result once or to stop a bad plan); `AS NOT MATERIALIZED` forces inlining even when referenced twice.
        """,
        ex_bn=r"""
            প্রথম option-টা **PostgreSQL 12-এর আগে** সত্য ছিল — তখন CTE সবসময় materialize হতো, আর অনেক পুরনো blog post এখনো এগুলোকে optimization fence বলে। এজন্যই এটা লোভনীয়।

            এখনকার নিয়ম:
            - একবার reference, side effect নেই, recursive নয় → default-ভাবে inline।
            - **একাধিকবার** reference → default-ভাবে materialize (একবার হিসাব হয়, বারবার ব্যবহার হয়)।
            - Recursive CTE আর data-modifying CTE (`WITH`-এর ভেতরে `INSERT/UPDATE/DELETE ... RETURNING`) সবসময় ঠিক একবার execute হয়।
            - চাইলে বদলাতে পারো: `WITH x AS MATERIALIZED (...)` fence বসিয়ে দেয় (ব্যয়বহুল result একবার হিসাব করতে বা খারাপ plan ঠেকাতে কাজে লাগে); `AS NOT MATERIALIZED` দুবার reference হলেও inline করতে বাধ্য করে।
        """,
        tip_en=r"""Mention the PG12 change explicitly and the `MATERIALIZED` / `NOT MATERIALIZED` keywords — it shows your knowledge isn't based on outdated articles.""",
        tip_bn=r"""PG12-এর পরিবর্তন আর `MATERIALIZED` / `NOT MATERIALIZED` keyword-এর কথা স্পষ্ট করে বলো — এতে বোঝা যায় তোমার জ্ঞান পুরনো article-নির্ভর নয়।""",
        related=["pg-024"],
        refs=[PG_WITH],
    ),
    # ------------------------------------------------------------------ pg-016
    Q(
        id="pg-016", sub="JSONB", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["jsonb", "gin", "operators", "containment", "nulls-last"],
        ver="PostgreSQL 18 (PostgreSQL-specific operators)", vs=False, status="stable",
        q_en=r"""Using the `products` table below, return the name, color, RAM (as an integer), and whether the product is tagged `5g` for every **Walton** product. Sort by RAM from highest to lowest, with products that have no RAM value last. The query should be able to use the GIN index.""",
        q_bn=r"""নিচের `products` table থেকে সব **Walton** product-এর name, color, RAM (integer হিসেবে) আর product-টা `5g` tag করা কিনা — বের করো। RAM বেশি থেকে কম ক্রমে sort করো, আর যেসব product-এর RAM value নেই সেগুলো শেষে রাখো। Query-টা যেন GIN index ব্যবহার করতে পারে।""",
        setup=r"""
            CREATE TABLE products (
              id    int PRIMARY KEY,
              name  text NOT NULL,
              attrs jsonb NOT NULL
            );

            INSERT INTO products VALUES
              (1, 'Walton Primo X', '{"brand": "Walton", "color": "black", "ram_gb": 8, "tags": ["5g", "android"]}'),
              (2, 'Symphony Z60',   '{"brand": "Symphony", "color": "blue", "ram_gb": 4, "tags": ["android"]}'),
              (3, 'Walton Fridge',  '{"brand": "Walton", "color": "silver", "capacity_l": 250}'),
              (4, 'Walton Tab T1',  '{"brand": "Walton", "color": "black", "ram_gb": 4, "tags": ["android", "tablet"]}'),
              (5, 'Xiaomi 14',      '{"brand": "Xiaomi", "color": "black", "ram_gb": 12, "tags": ["5g", "android"]}');

            CREATE INDEX idx_products_attrs ON products USING gin (attrs jsonb_path_ops);
        """,
        code=r"""
            SELECT name,
                   attrs->>'color'          AS color,
                   (attrs->>'ram_gb')::int  AS ram_gb,
                   attrs->'tags' ? '5g'     AS has_5g
            FROM products
            WHERE attrs @> '{"brand": "Walton"}'
            ORDER BY ram_gb DESC NULLS LAST;
        """,
        lang="sql",
        output=r"""
                  name      | color  | ram_gb | has_5g
            ----------------+--------+--------+--------
             Walton Primo X | black  |      8 | t
             Walton Tab T1  | black  |      4 | f
             Walton Fridge  | silver |        |
        """,
        a_en=r"""
            - `attrs @> '{"brand": "Walton"}'` is a **containment** test: "does `attrs` contain this JSON?" It's the operator the `jsonb_path_ops` GIN index supports, so the filter can use a Bitmap Index Scan.
            - `->>` returns **text** (good for display); `->` returns **jsonb** (needed to keep navigating, as in `attrs->'tags'`).
            - `(attrs->>'ram_gb')::int` casts to integer so sorting is numeric; text sorting would put `'12'` before `'4'`.
            - `attrs->'tags' ? '5g'` checks whether the array contains the string `5g`. The fridge has no `tags` key, so `attrs->'tags'` is NULL and the result is NULL (shown empty).
            - `DESC NULLS LAST`: in PostgreSQL, NULLs sort as larger than any value, so plain `DESC` would put the fridge **first**.
        """,
        a_bn=r"""
            - `attrs @> '{"brand": "Walton"}'` হলো **containment** test: "`attrs`-এর ভেতরে কি এই JSON আছে?" `jsonb_path_ops` GIN index ঠিক এই operator-টাই support করে, তাই filter-টা Bitmap Index Scan ব্যবহার করতে পারে।
            - `->>` **text** return করে (দেখানোর জন্য ভালো); `->` **jsonb** return করে (ভেতরে আরও ঢুকতে লাগে, যেমন `attrs->'tags'`)।
            - `(attrs->>'ram_gb')::int` integer-এ cast করে, যাতে sort সংখ্যা হিসেবে হয়; text হিসেবে sort করলে `'12'`, `'4'`-এর আগে চলে আসত।
            - `attrs->'tags' ? '5g'` দেখে array-তে `5g` string আছে কিনা। Fridge-এর `tags` key নেই, তাই `attrs->'tags'` NULL, ফলাফলও NULL (খালি দেখায়)।
            - `DESC NULLS LAST`: PostgreSQL-এ NULL-কে সব value-এর চেয়ে বড় ধরা হয়, তাই শুধু `DESC` দিলে fridge **প্রথমে** চলে আসত।
        """,
        quick_en=r"""Filter with containment `attrs @> '{"brand": "Walton"}'` so the GIN index can be used, read fields with `->>`, cast `(attrs->>'ram_gb')::int` so sorting is numeric, and test the tag with `attrs->'tags' ? '5g'`. Sort `DESC NULLS LAST`, because NULLs sort first under plain `DESC`.""",
        quick_bn=r"""`attrs @> '{"brand": "Walton"}'` containment দিয়ে filter করো যাতে GIN index কাজে লাগে, field পড়ো `->>` দিয়ে, `(attrs->>'ram_gb')::int` cast করো যাতে sorting সংখ্যা হিসেবে হয়, আর tag দেখো `attrs->'tags' ? '5g'` দিয়ে। `DESC NULLS LAST` দাও, কারণ শুধু `DESC`-এ NULL সবার আগে আসে।""",
        ex_en=r"""
            - **Index caveat:** a range filter like `(attrs->>'ram_gb')::int >= 8` can't use the GIN index. If that's a hot query, add a B-tree expression index on `((attrs->>'ram_gb')::int)` — or promote `ram_gb` to a real column.
            - `jsonb_path_ops` supports `@>`, `@?`, and `@@` but **not** `?`. If you filter with `attrs ? 'ram_gb'`, use the default `jsonb_ops` class.
            - SQL/JSON path is an alternative: `WHERE attrs @? '$.tags[*] ? (@ == "5g")'` finds 5G products and can use the GIN index too; `jsonb_path_query()` returns matching elements.
            - All of these operators (`->`, `->>`, `@>`, `?`, `::`) are PostgreSQL-specific syntax.
        """,
        ex_bn=r"""
            - **Index-এর সতর্কতা:** `(attrs->>'ram_gb')::int >= 8`-এর মতো range filter GIN index ব্যবহার করতে পারে না। এটা যদি ঘনঘন চলা query হয়, `((attrs->>'ram_gb')::int)`-এর উপর একটা B-tree expression index দাও — অথবা `ram_gb`-কে আসল column বানাও।
            - `jsonb_path_ops` `@>`, `@?` আর `@@` support করে, কিন্তু `?` **করে না**। `attrs ? 'ram_gb'` দিয়ে filter করলে default `jsonb_ops` class ব্যবহার করো।
            - বিকল্প হিসেবে SQL/JSON path: `WHERE attrs @? '$.tags[*] ? (@ == "5g")'` 5G product খুঁজে দেয় আর GIN index-ও ব্যবহার করতে পারে; `jsonb_path_query()` matching element-গুলো return করে।
            - এই সব operator (`->`, `->>`, `@>`, `?`, `::`) PostgreSQL-specific syntax।
        """,
        tip_en=r"""Explain `->` vs `->>` and why containment is index-friendly. Catching the NULL-ordering detail without being asked is a strong signal.""",
        tip_bn=r"""`->` বনাম `->>` আর containment কেন index-friendly — ব্যাখ্যা করো। কেউ জিজ্ঞেস না করতেই NULL-ordering-এর খুঁটিনাটি ধরলে খুব ভালো impression পড়ে।""",
        mist_en=r"""Comparing `attrs->>'ram_gb'` as text, or using `?` with a `jsonb_path_ops` index and wondering why it isn't used. Some drivers (JDBC, PDO) treat `?` as a parameter placeholder — use `jsonb_exists()` or the driver's escape there.""",
        mist_bn=r"""`attrs->>'ram_gb'`-কে text হিসেবে তুলনা করা, অথবা `jsonb_path_ops` index থাকা অবস্থায় `?` ব্যবহার করে অবাক হওয়া যে index কেন কাজে লাগছে না। কিছু driver (JDBC, PDO) `?`-কে parameter placeholder ধরে — সেখানে `jsonb_exists()` বা driver-এর escape ব্যবহার করো।""",
        follow=[
            ("How would you find products whose `tags` array contains `5g` using a JSON path expression?", "JSON path expression দিয়ে কীভাবে সেসব product খুঁজবে যাদের `tags` array-তে `5g` আছে?"),
            ("When would you move a JSONB key into its own column?", "কখন একটা JSONB key-কে আলাদা column-এ সরিয়ে নেবে?"),
        ],
        related=["pg-010", "pg-013"],
        refs=[PG_JSON_FUNCS, PG_JSON_TYPES, PG_GIN],
    ),
]

if __name__ == "__main__":
    save("postgresql", "b2", QUESTIONS)
