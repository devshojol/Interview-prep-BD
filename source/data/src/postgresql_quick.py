# PostgreSQL quick-recall — pg-q01 … pg-q10 (short viva-style fundamentals)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_CREATE_TABLE = ("PostgreSQL docs — CREATE TABLE (identity columns)", "https://www.postgresql.org/docs/current/sql-createtable.html")
PG_SEQ_FUNCS = ("PostgreSQL docs — Sequence Manipulation Functions", "https://www.postgresql.org/docs/current/functions-sequence.html")
PG_CHAR_TYPES = ("PostgreSQL docs — Character Types", "https://www.postgresql.org/docs/current/datatype-character.html")
PG_DATETIME = ("PostgreSQL docs — Date/Time Types", "https://www.postgresql.org/docs/current/datatype-datetime.html")
PG_JSON_FUNCS = ("PostgreSQL docs — JSON Functions and Operators", "https://www.postgresql.org/docs/current/functions-json.html")
PG_SCHEMAS = ("PostgreSQL docs — Schemas", "https://www.postgresql.org/docs/current/ddl-schemas.html")
PG_VACUUM = ("PostgreSQL docs — Routine Vacuuming", "https://www.postgresql.org/docs/current/routine-vacuuming.html")
PG_USING_EXPLAIN = ("PostgreSQL docs — Using EXPLAIN", "https://www.postgresql.org/docs/current/using-explain.html")
PG_RETURNING = ("PostgreSQL docs — Returning Data from Modified Rows", "https://www.postgresql.org/docs/current/dml-returning.html")
PG_ROLES = ("PostgreSQL docs — Database Roles", "https://www.postgresql.org/docs/current/user-manag.html")

VER = "PostgreSQL 18"

QUESTIONS = [
    # ------------------------------------------------------------------ pg-q01
    Q(
        id="pg-q01", sub="Data Types & Keys", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["serial", "identity", "primary-key", "sequence"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `SERIAL` and an identity column in PostgreSQL?""",
        q_bn=r"""PostgreSQL-এ `SERIAL` আর identity column-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`SERIAL` isn't a real type: it's shorthand for an `integer` column with a sequence and a `DEFAULT nextval(...)`, and it's the legacy approach. `GENERATED ... AS IDENTITY` is the SQL-standard replacement with the sequence tied to the column; `ALWAYS` even rejects manually supplied ids.""",
        a_bn=r"""`SERIAL` আসল কোনো type নয়: এটা একটা sequence আর `DEFAULT nextval(...)`-সহ `integer` column-এর সংক্ষিপ্ত রূপ, আর এটা legacy পদ্ধতি। `GENERATED ... AS IDENTITY` হলো SQL-standard বিকল্প, যেখানে sequence column-এর সাথে বাঁধা; `ALWAYS` দিলে হাতে দেওয়া id-ও প্রত্যাখ্যান করে।""",
        code=r"""
            CREATE TABLE old_style (id serial PRIMARY KEY);   -- legacy: int + sequence + default
            CREATE TABLE users (
              id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              email text NOT NULL
            );
            INSERT INTO users (email) VALUES ('rahim@example.com');  -- id = 1
            INSERT INTO users (id, email) VALUES (5, 'x@example.com'); -- error: id is GENERATED ALWAYS
        """, lang="sql",
        ex_en=r"""With `serial` or `BY DEFAULT`, a manually inserted id doesn't move the sequence, so a later insert can hit a duplicate-key error. `serial` is also 4-byte `integer`; use `bigint` for big tables.""",
        ex_bn=r"""`serial` বা `BY DEFAULT`-এ হাতে insert করা id sequence-কে এগিয়ে দেয় না, তাই পরে কোনো insert duplicate-key error খেতে পারে। তাছাড়া `serial` 4-byte `integer`; বড় table-এর জন্য `bigint` নাও।""",
        tip_en=r"""Say "identity is the modern standard, `serial` is legacy" and give the `ALWAYS` vs `BY DEFAULT` difference.""",
        tip_bn=r"""বলো "identity হলো আধুনিক standard, `serial` legacy", তারপর `ALWAYS` আর `BY DEFAULT`-এর পার্থক্যটা বলো।""",
        follow=[("When would you use a UUID instead of an identity column?", "কখন identity column-এর বদলে UUID ব্যবহার করবে?")],
        related=["pg-012", "pg-q02"],
        refs=[PG_CREATE_TABLE],
    ),
    # ------------------------------------------------------------------ pg-q02
    Q(
        id="pg-q02", sub="Sequences", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["sequence", "nextval", "currval"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is a sequence in PostgreSQL, and why can ids have gaps?""",
        q_bn=r"""PostgreSQL-এ sequence কী, আর id-তে কেন ফাঁক (gap) থাকতে পারে?""",
        a_en=r"""A sequence is a database object that hands out increasing numbers with `nextval()`; identity and `serial` columns use one behind the scenes. `nextval()` is never rolled back, so a failed or rolled-back insert still uses up its number, which is why ids can have gaps.""",
        a_bn=r"""Sequence হলো একটা database object, যেটা `nextval()` দিয়ে ক্রমবর্ধমান সংখ্যা দেয়; identity আর `serial` column পেছনে এটাই ব্যবহার করে। `nextval()` কখনো rollback হয় না, তাই fail বা rollback হওয়া insert-ও তার সংখ্যাটা খরচ করে ফেলে; এজন্যই id-তে gap থাকতে পারে।""",
        code=r"""
            CREATE SEQUENCE invoice_no START 1000;
            SELECT nextval('invoice_no');   -- → 1000
            SELECT nextval('invoice_no');   -- → 1001
            SELECT currval('invoice_no');   -- → 1001 (last value in this session)
        """, lang="sql",
        ex_en=r"""Never rely on ids being gap-free; if the business needs consecutive invoice numbers, generate them separately under a lock. `currval()` is per session and errors if `nextval()` wasn't called in that session.""",
        ex_bn=r"""Id-তে gap থাকবে না, এমন ধরে নিয়ো না; business-এর যদি টানা invoice নম্বর লাগে, সেটা lock নিয়ে আলাদাভাবে বানাও। `currval()` session অনুযায়ী কাজ করে, আর ওই session-এ `nextval()` না ডাকলে error দেয়।""",
        tip_en=r"""Mention the gap behaviour; it's the follow-up most interviewers are waiting for.""",
        tip_bn=r"""Gap-এর আচরণটা উল্লেখ করো; বেশিরভাগ interviewer এই follow-up-এর জন্যই অপেক্ষা করে।""",
        follow=[("How do you reset a sequence after a bulk import?", "Bulk import-এর পরে sequence কীভাবে reset করবে?")],
        related=["pg-q01", "pg-012"],
        refs=[PG_SEQ_FUNCS],
    ),
    # ------------------------------------------------------------------ pg-q03
    Q(
        id="pg-q03", sub="Data Types", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["text", "varchar", "char", "data-types"],
        ver=VER, vs=False, status="stable",
        q_en=r"""In PostgreSQL, what is the difference between `text`, `varchar(n)` and `char(n)`?""",
        q_bn=r"""PostgreSQL-এ `text`, `varchar(n)` আর `char(n)`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""All three store strings with the same performance. `varchar(n)` only adds a length check and errors on longer values, `char(n)` pads with spaces to exactly n, and `text` has no limit. Most teams use `text`, or `varchar(n)` when a real maximum length is a business rule.""",
        a_bn=r"""তিনটাই string রাখে, performance একই। `varchar(n)` শুধু একটা length check যোগ করে আর বেশি লম্বা value-তে error দেয়, `char(n)` space দিয়ে ঠিক n পর্যন্ত ভরে দেয়, আর `text`-এর কোনো সীমা নেই। বেশিরভাগ team `text` ব্যবহার করে, অথবা সর্বোচ্চ দৈর্ঘ্য সত্যিই business rule হলে `varchar(n)`।""",
        code=r"""
            CREATE TABLE people (code char(5), name varchar(10), bio text);
            INSERT INTO people VALUES ('ab', 'Muhammad Rahim', '...');
            -- ERROR: value too long for type character varying(10)
        """, lang="sql",
        ex_en=r"""This differs from some other databases, where `char` can be faster; in PostgreSQL `char(n)` is usually the slowest because of the padding. A `CHECK` constraint is another way to limit length.""",
        ex_bn=r"""এটা অন্য কিছু database থেকে আলাদা, যেখানে `char` দ্রুত হতে পারে; PostgreSQL-এ padding-এর কারণে `char(n)` সাধারণত সবচেয়ে ধীর। দৈর্ঘ্য সীমিত করার আরেক উপায় হলো `CHECK` constraint।""",
        tip_en=r"""Say "no performance difference in PostgreSQL" first; that's the point that separates a PostgreSQL answer from a generic one.""",
        tip_bn=r"""শুরুতেই বলো "PostgreSQL-এ performance-এর কোনো পার্থক্য নেই"; এই কথাটাই PostgreSQL-এর উত্তরকে সাধারণ উত্তর থেকে আলাদা করে।""",
        follow=[("Which type would you use for money?", "টাকার পরিমাণের জন্য কোন type নেবে?")],
        related=["pg-003", "pg-012"],
        refs=[PG_CHAR_TYPES],
    ),
    # ------------------------------------------------------------------ pg-q04
    Q(
        id="pg-q04", sub="Data Types", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["timestamptz", "timestamp", "time-zones"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `timestamp` and `timestamptz`, and which should you use?""",
        q_bn=r"""`timestamp` আর `timestamptz`-এর মধ্যে পার্থক্য কী, আর কোনটা ব্যবহার করা উচিত?""",
        a_en=r"""`timestamptz` stores an exact moment: input is converted to UTC and shown in the session's `TimeZone`. `timestamp` (without time zone) stores just a date and clock time and silently ignores any offset you give. Use `timestamptz` for events like `created_at`.""",
        a_bn=r"""`timestamptz` একটা নির্দিষ্ট মুহূর্ত রাখে: input UTC-তে রূপান্তর হয়, আর session-এর `TimeZone` অনুযায়ী দেখানো হয়। `timestamp` (without time zone) শুধু তারিখ আর ঘড়ির সময় রাখে, আর দেওয়া offset চুপচাপ উপেক্ষা করে। `created_at`-এর মতো event-এর জন্য `timestamptz` নাও।""",
        code=r"""
            SET TimeZone = 'Asia/Dhaka';
            SELECT '2026-10-26 10:00:00+00'::timestamptz;  -- → 2026-10-26 16:00:00+06
            SELECT '2026-10-26 10:00:00+00'::timestamp;    -- → 2026-10-26 10:00:00 (offset ignored)
        """, lang="sql",
        ex_en=r"""Despite the name, `timestamptz` doesn't store the zone itself, only the UTC instant. If you need the user's original zone, store it in a separate column.""",
        ex_bn=r"""নামে time zone থাকলেও `timestamptz` zone-টা নিজে রাখে না, শুধু UTC মুহূর্তটা রাখে। ব্যবহারকারীর আসল zone দরকার হলে সেটা আলাদা column-এ রাখো।""",
        tip_en=r"""Use the Dhaka example: the same instant prints as 16:00+06 in Dhaka, which shows you understand conversion on output.""",
        tip_bn=r"""Dhaka-র উদাহরণ দাও: একই মুহূর্ত Dhaka-তে 16:00+06 হিসেবে দেখায়; এতে বোঝা যায় output-এর সময় conversion হয় সেটা তুমি জানো।""",
        follow=[("Does `timestamptz` store the original time zone?", "`timestamptz` কি আসল time zone-টা জমা রাখে?")],
        related=["pg-012", "pg-003"],
        refs=[PG_DATETIME],
    ),
    # ------------------------------------------------------------------ pg-q05
    Q(
        id="pg-q05", sub="JSONB", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["jsonb", "operators", "json"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between the `->` and `->>` operators on `jsonb`?""",
        q_bn=r"""`jsonb`-এ `->` আর `->>` operator-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""Both read a key (or an array element by index). `->` returns the value as `jsonb`, so you can keep navigating into it, while `->>` returns it as `text`, which is what you want for display, comparisons with strings, or casting like `(data->>'age')::int`.""",
        a_bn=r"""দুটোই একটা key (বা index দিয়ে array-র element) পড়ে। `->` value-টা `jsonb` হিসেবে দেয়, তাই এর ভেতরে আরও যাওয়া যায়; আর `->>` দেয় `text` হিসেবে, যেটা দেখানো, string-এর সাথে তুলনা বা `(data->>'age')::int`-এর মতো cast করার জন্য দরকার।""",
        code=r"""
            SELECT '{"name": "Rahim", "address": {"city": "Dhaka"}}'::jsonb -> 'name';
            -- → "Rahim"   (jsonb, keeps the quotes)
            SELECT '{"name": "Rahim", "address": {"city": "Dhaka"}}'::jsonb ->> 'name';
            -- → Rahim     (text)
            SELECT '{"name": "Rahim", "address": {"city": "Dhaka"}}'::jsonb -> 'address' ->> 'city';
            -- → Dhaka
        """, lang="sql",
        ex_en=r"""A common bug is `WHERE data->'city' = 'Dhaka'`: it compares `jsonb` with a JSON value and errors because `Dhaka` isn't valid JSON. Use `->>` for text, or containment `@>`, which a GIN index can serve.""",
        ex_bn=r"""একটা সাধারণ bug হলো `WHERE data->'city' = 'Dhaka'`: এটা `jsonb`-কে একটা JSON value-এর সাথে তুলনা করে, আর `Dhaka` valid JSON না হওয়ায় error দেয়। Text-এর জন্য `->>` নাও, অথবা containment `@>`, যেটা GIN index ব্যবহার করতে পারে।""",
        tip_en=r"""Say "one arrow keeps JSON, two arrows give text" and show chaining `-> 'address' ->> 'city'`.""",
        tip_bn=r"""বলো "এক arrow JSON রাখে, দুই arrow text দেয়", তারপর `-> 'address' ->> 'city'` chain করে দেখাও।""",
        follow=[("Why would you choose `jsonb` over `json`?", "`json`-এর বদলে কেন `jsonb` বেছে নেবে?")],
        related=["pg-010", "pg-016"],
        refs=[PG_JSON_FUNCS],
    ),
    # ------------------------------------------------------------------ pg-q06
    Q(
        id="pg-q06", sub="Schemas", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["schema", "search-path", "public"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is a schema in PostgreSQL, and what is `search_path`?""",
        q_bn=r"""PostgreSQL-এ schema কী, আর `search_path` কী?""",
        a_en=r"""A schema is a namespace inside a database that groups tables, views and functions, so `billing.invoices` and `sales.invoices` can both exist. The hierarchy is cluster → database → schema → table. `search_path` lists the schemas PostgreSQL searches for unqualified names; by default it's `"$user", public`.""",
        a_bn=r"""Schema হলো database-এর ভেতরের একটা namespace, যেটা table, view আর function একসাথে রাখে, তাই `billing.invoices` আর `sales.invoices` দুটোই থাকতে পারে। ক্রমটা হলো cluster → database → schema → table। Schema-র নাম ছাড়া কোনো নাম পেলে PostgreSQL কোন schema-গুলোতে খুঁজবে সেটা `search_path`-এ থাকে; default হলো `"$user", public`।""",
        code=r"""
            CREATE SCHEMA billing;
            CREATE TABLE billing.invoices (id bigint PRIMARY KEY);
            SHOW search_path;                   -- → "$user", public
            SET search_path = billing, public;
            SELECT * FROM invoices;             -- now resolves to billing.invoices
        """, lang="sql",
        ex_en=r"""Schemas also separate permissions: you grant `USAGE` on a schema plus rights on its tables. Since PostgreSQL 15, ordinary users can no longer create objects in `public` by default.""",
        ex_bn=r"""Schema দিয়ে permission-ও আলাদা করা যায়: schema-তে `USAGE` আর তার table-গুলোর ওপর অধিকার grant করতে হয়। PostgreSQL 15 থেকে সাধারণ user default-ভাবে আর `public`-এ object বানাতে পারে না।""",
        tip_en=r"""Contrast it with MySQL, where "schema" and "database" mean the same thing; in PostgreSQL a database contains many schemas.""",
        tip_bn=r"""MySQL-এর সাথে তুলনা করো, যেখানে "schema" আর "database" একই জিনিস; PostgreSQL-এ একটা database-এর ভেতরে অনেকগুলো schema থাকে।""",
        follow=[("Can you join tables from two different databases in one query?", "দুটো আলাদা database-এর table কি একটা query-তে join করা যায়?")],
        related=["pg-018", "pg-032"],
        refs=[PG_SCHEMAS],
    ),
    # ------------------------------------------------------------------ pg-q07
    Q(
        id="pg-q07", sub="VACUUM", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["vacuum", "autovacuum", "mvcc", "bloat"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What does `VACUUM` do, and how is it different from `VACUUM FULL`?""",
        q_bn=r"""`VACUUM` কী করে, আর `VACUUM FULL` থেকে এটা কীভাবে আলাদা?""",
        a_en=r"""Because of MVCC, updates and deletes leave dead row versions. `VACUUM` marks their space as reusable and freezes old rows, without blocking normal reads and writes; autovacuum runs it for you. `VACUUM FULL` rewrites the whole table to give space back to the OS, but holds an exclusive lock the whole time.""",
        a_bn=r"""MVCC-র কারণে update আর delete dead row version রেখে যায়। `VACUUM` সেগুলোর জায়গা আবার ব্যবহারযোগ্য করে আর পুরোনো row freeze করে, সাধারণ read/write block না করেই; autovacuum এটা নিজে থেকেই চালায়। `VACUUM FULL` পুরো table নতুন করে লিখে OS-কে জায়গা ফেরত দেয়, কিন্তু পুরো সময় একটা exclusive lock ধরে রাখে।""",
        code=r"""
            VACUUM (VERBOSE, ANALYZE) orders;   -- clean dead rows + refresh planner stats
            VACUUM FULL orders;                 -- rewrite table; blocks reads and writes
            SELECT relname, n_dead_tup, last_autovacuum
            FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 5;
        """, lang="sql",
        ex_en=r"""Plain `VACUUM` usually doesn't shrink the file; it makes room for new rows. Use `VACUUM FULL` only in a maintenance window, or `pg_repack` online.""",
        ex_bn=r"""সাধারণ `VACUUM` সাধারণত file ছোট করে না; নতুন row-এর জন্য জায়গা করে দেয়। `VACUUM FULL` শুধু maintenance window-তে চালাও, অথবা online করতে চাইলে `pg_repack`।""",
        tip_en=r"""Link it to MVCC in one sentence ("updates leave dead rows"), then stress the lock difference.""",
        tip_bn=r"""এক বাক্যে MVCC-র সাথে যুক্ত করো ("update dead row রেখে যায়"), তারপর lock-এর পার্থক্যটায় জোর দাও।""",
        follow=[("What is transaction ID wraparound?", "Transaction ID wraparound কী?")],
        related=["pg-007", "pg-029"],
        refs=[PG_VACUUM],
    ),
    # ------------------------------------------------------------------ pg-q08
    Q(
        id="pg-q08", sub="EXPLAIN & EXPLAIN ANALYZE", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["explain", "seq-scan", "index-scan", "query-plan"],
        ver=VER, vs=False, status="stable",
        q_en=r"""In an `EXPLAIN` plan, what is the difference between a Seq Scan and an Index Scan?""",
        q_bn=r"""`EXPLAIN` plan-এ Seq Scan আর Index Scan-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""A Seq Scan reads every row of the table and checks the filter on each one. An Index Scan walks an index to find the matching rows and then fetches only those. A Seq Scan isn't always bad: when a query matches a large share of the table, reading it straight through is cheaper, so the planner picks it.""",
        a_bn=r"""Seq Scan table-এর প্রতিটা row পড়ে আর প্রতিটায় filter check করে। Index Scan index ধরে মেলে এমন row খুঁজে শুধু সেগুলোই আনে। Seq Scan সবসময় খারাপ নয়: query table-এর বড় একটা অংশ মেলালে সরাসরি পুরোটা পড়াই সস্তা, তাই planner সেটাই বাছে।""",
        code=r"""
            EXPLAIN SELECT * FROM users WHERE id = 42;
            -- Index Scan using users_pkey on users  (cost=... rows=1 ...)

            EXPLAIN SELECT * FROM users WHERE is_active;
            -- Seq Scan on users  (cost=... rows=...)  Filter: is_active
        """, lang="sql",
        ex_en=r"""You'll also see Bitmap Heap Scan (many matches, fetched in page order) and Index Only Scan (all needed columns are in the index). `EXPLAIN` shows estimates; `EXPLAIN ANALYZE` runs the query and adds actual rows and timings.""",
        ex_bn=r"""Bitmap Heap Scan (অনেক match, page-এর ক্রমে আনা হয়) আর Index Only Scan (দরকারি সব column index-এই আছে)-ও দেখতে পাবে। `EXPLAIN` শুধু estimate দেখায়; `EXPLAIN ANALYZE` query-টা চালিয়ে আসল row আর timing যোগ করে।""",
        tip_en=r"""Don't say "Seq Scan means a missing index"; say you compare estimated vs actual rows to judge the plan.""",
        tip_bn=r"""বলো না "Seq Scan মানে index নেই"; বরং বলো plan বিচার করতে তুমি estimated আর actual row তুলনা করো।""",
        follow=[("Does `EXPLAIN ANALYZE` run the query?", "`EXPLAIN ANALYZE` কি query-টা সত্যিই চালায়?")],
        related=["pg-009", "pg-005", "pg-024"],
        refs=[PG_USING_EXPLAIN],
    ),
    # ------------------------------------------------------------------ pg-q09
    Q(
        id="pg-q09", sub="RETURNING", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["returning", "insert", "update", "delete"],
        ver=VER, vs=True, status="stable",
        q_en=r"""What does the `RETURNING` clause do in PostgreSQL?""",
        q_bn=r"""PostgreSQL-এ `RETURNING` clause কী করে?""",
        a_en=r"""`RETURNING` makes `INSERT`, `UPDATE`, `DELETE` (and `MERGE`) send back columns of the rows they changed, in the same statement. The classic use is getting the generated id after an insert without a second query. In PostgreSQL 18 you can also return `OLD` and `NEW` values.""",
        a_bn=r"""`RETURNING` দিলে `INSERT`, `UPDATE`, `DELETE` (আর `MERGE`) একই statement-এ পরিবর্তিত row-গুলোর column ফেরত পাঠায়। সবচেয়ে পরিচিত ব্যবহার হলো দ্বিতীয় query ছাড়াই insert-এর পরে generate হওয়া id পাওয়া। PostgreSQL 18-এ `OLD` আর `NEW` value-ও return করা যায়।""",
        code=r"""
            INSERT INTO users (email) VALUES ('rahim@example.com')
            RETURNING id, created_at;                 -- → 1 | 2026-10-26 ...
            DELETE FROM sessions WHERE expires_at < now()
            RETURNING user_id;                        -- the deleted rows' user_ids
            UPDATE products SET price = price * 1.1 WHERE id = 7
            RETURNING old.price, new.price;           -- PostgreSQL 18+
        """, lang="sql",
        ex_en=r"""It saves a round trip and avoids races, because a separate `SELECT` afterwards might see someone else's change. SQLite also supports `RETURNING`; MySQL doesn't.""",
        ex_bn=r"""এতে একটা round trip বাঁচে আর race এড়ানো যায়, কারণ পরে আলাদা `SELECT` চালালে অন্য কারো change দেখা যেতে পারে। SQLite-ও `RETURNING` support করে; MySQL করে না।""",
        tip_en=r"""Show `INSERT ... RETURNING id`; it's what node-postgres code uses instead of MySQL's `insertId`.""",
        tip_bn=r"""`INSERT ... RETURNING id` দেখাও; MySQL-এর `insertId`-এর বদলে node-postgres code এটাই ব্যবহার করে।""",
        follow=[("How would you do an upsert in PostgreSQL?", "PostgreSQL-এ upsert কীভাবে করবে?")],
        related=["pg-022"],
        refs=[PG_RETURNING],
    ),
    # ------------------------------------------------------------------ pg-q10
    Q(
        id="pg-q10", sub="Security: Roles & Authentication", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["roles", "users", "grant", "privileges"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between a role and a user in PostgreSQL?""",
        q_bn=r"""PostgreSQL-এ role আর user-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""PostgreSQL only has roles. A "user" is simply a role with the `LOGIN` attribute (`CREATE USER` = `CREATE ROLE ... LOGIN`), and a "group" is a role without login that other roles are granted membership in. Privileges are granted to roles, and members inherit them.""",
        a_bn=r"""PostgreSQL-এ আসলে শুধু role আছে। "User" হলো `LOGIN` attribute-সহ একটা role (`CREATE USER` = `CREATE ROLE ... LOGIN`), আর "group" হলো login ছাড়া একটা role, যার membership অন্য role-দের দেওয়া হয়। Privilege role-কে grant করা হয়, আর member-রা সেটা inherit করে।""",
        code=r"""
            CREATE ROLE readers;                    -- group role (NOLOGIN by default)
            GRANT SELECT ON ALL TABLES IN SCHEMA public TO readers;
            CREATE USER rahim;                      -- = CREATE ROLE rahim LOGIN
            GRANT readers TO rahim;                 -- rahim can now read those tables
        """, lang="sql",
        ex_en=r"""Roles are cluster-wide, not per database. Give the app its own least-privilege login role instead of connecting as the `postgres` superuser.""",
        ex_bn=r"""Role পুরো cluster-এর জন্য, আলাদা database-এর জন্য নয়। App-কে `postgres` superuser হিসেবে connect না করিয়ে কম privilege-এর নিজস্ব login role দাও।""",
        tip_en=r"""Say "a user is a role that can log in", then add the least-privilege point for the app connection.""",
        tip_bn=r"""বলো "user হলো এমন role যেটা login করতে পারে", তারপর app connection-এর জন্য least privilege-এর কথাটা যোগ করো।""",
        follow=[("Why shouldn't your app connect as the `postgres` superuser?", "App কেন `postgres` superuser হিসেবে connect করা উচিত নয়?")],
        related=["pg-018", "pg-032"],
        refs=[PG_ROLES],
    ),
]

if __name__ == "__main__":
    save("postgresql", "quick", QUESTIONS)
