# SQL batch 4 — sql-025 … sql-032 (hard & extreme)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_WINDOW_CALLS = ("PostgreSQL docs — Window Function Calls (frames)", "https://www.postgresql.org/docs/current/sql-expressions.html")
PG_WINDOW_TUT = ("PostgreSQL docs — Window Functions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-window.html")
SQLITE_WINDOW = ("SQLite — Window Functions", "https://www.sqlite.org/windowfunctions.html")
PG_LIMIT = ("PostgreSQL docs — LIMIT and OFFSET", "https://www.postgresql.org/docs/current/queries-limit.html")
PG_ROW_COMPARISON = ("PostgreSQL docs — Row Constructor Comparison", "https://www.postgresql.org/docs/current/functions-comparisons.html")
PG_VIEWS = ("PostgreSQL docs — CREATE VIEW", "https://www.postgresql.org/docs/current/sql-createview.html")
PG_MATVIEWS = ("PostgreSQL docs — Materialized Views", "https://www.postgresql.org/docs/current/rules-materializedviews.html")
PG_REFRESH_MV = ("PostgreSQL docs — REFRESH MATERIALIZED VIEW", "https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html")
PG_TRIGGERS = ("PostgreSQL docs — Triggers", "https://www.postgresql.org/docs/current/triggers.html")
PG_PROCEDURE = ("PostgreSQL docs — CREATE PROCEDURE", "https://www.postgresql.org/docs/current/sql-createprocedure.html")
PG_ISO = ("PostgreSQL docs — Transaction Isolation", "https://www.postgresql.org/docs/current/transaction-iso.html")
MS_ISO = ("Microsoft Learn — SET TRANSACTION ISOLATION LEVEL", "https://learn.microsoft.com/en-us/sql/t-sql/statements/set-transaction-isolation-level-transact-sql")
PG_DATETIME_OPS = ("PostgreSQL docs — Date/Time Functions and Operators", "https://www.postgresql.org/docs/current/functions-datetime.html")
PG_USING_EXPLAIN = ("PostgreSQL docs — Using EXPLAIN", "https://www.postgresql.org/docs/current/using-explain.html")
PG_PARTITIONING = ("PostgreSQL docs — Table Partitioning", "https://www.postgresql.org/docs/current/ddl-partitioning.html")
PG_CONSTRAINTS = ("PostgreSQL docs — Constraints", "https://www.postgresql.org/docs/current/ddl-constraints.html")
PG_INDEXES = ("PostgreSQL docs — Indexes", "https://www.postgresql.org/docs/current/indexes.html")

QUESTIONS = [
    # ------------------------------------------------------------------ sql-025
    Q(
        id="sql-025", sub="Window Frames (RANGE vs ROWS)", diff="hard", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["window-frame", "range", "rows", "running-total", "output"],
        ver="SQL:2003 window functions (PostgreSQL, MySQL 8+, SQL Server, Oracle, SQLite 3.25+)", vs=False, status="stable",
        q_en=r"""What values appear in the `running` column, in `id` order?""",
        q_bn=r"""`id`-এর ক্রমে `running` column-এ কী কী value আসবে?""",
        code=r"""
            CREATE TABLE payments (id INT PRIMARY KEY, paid_on DATE NOT NULL, amount INT NOT NULL);
            INSERT INTO payments (id, paid_on, amount) VALUES
              (1, '2026-10-01', 100),
              (2, '2026-10-02',  50),
              (3, '2026-10-02',  30),
              (4, '2026-10-03',  20);

            SELECT id, paid_on, amount,
                   SUM(amount) OVER (ORDER BY paid_on) AS running
            FROM payments
            ORDER BY id;
        """,
        lang="sql",
        output=r"""
             id |  paid_on   | amount | running
            ----+------------+--------+---------
              1 | 2026-10-01 |    100 |     100
              2 | 2026-10-02 |     50 |     180
              3 | 2026-10-02 |     30 |     180
              4 | 2026-10-03 |     20 |     200
        """,
        options=[
            ("`100, 150, 180, 200`", "`100, 150, 180, 200`"),
            ("`100, 180, 180, 200`", "`100, 180, 180, 200`"),
            ("`100, 50, 30, 20`", "`100, 50, 30, 20`"),
            ("`200, 200, 200, 200`", "`200, 200, 200, 200`"),
        ],
        correct=1,
        a_en=r"""`100, 180, 180, 200`. With `ORDER BY` and no explicit frame, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. `RANGE` includes all **peers** — rows with the same `paid_on` — so both 2026-10-02 rows get 100 + 50 + 30 = 180.""",
        a_bn=r"""`100, 180, 180, 200`। `ORDER BY` থাকলে আর frame স্পষ্ট করে না দিলে default frame হয় `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`। `RANGE` সব **peer**-কে ধরে — যেসব row-এর `paid_on` একই — তাই 2026-10-02-এর দুটো row-ই পায় 100 + 50 + 30 = 180।""",
        ex_en=r"""
            - The tempting answer `100, 150, 180, 200` is what you get with `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` **plus** a unique ordering such as `ORDER BY paid_on, id`. `ROWS` counts physical rows one by one.
            - With `ROWS` but *without* a unique order key, the order of the two peers is arbitrary, so the intermediate value (150 or 130) can change between runs — always add a tie-breaker.
            - `200, 200, 200, 200` is what you'd get with no `ORDER BY` in the window at all (`SUM(amount) OVER ()`): the frame is then the whole partition.
            - Rule of thumb for running balances (bank statements, ledgers): `ORDER BY <time>, <id> ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.
            - `LAST_VALUE()` has the same trap: with the default frame it returns the current row's last peer, not the partition's last row — use `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.
        """,
        ex_bn=r"""
            - লোভনীয় উত্তর `100, 150, 180, 200` আসে `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` **আর** `ORDER BY paid_on, id`-এর মতো unique ordering দিলে। `ROWS` physical row একটা একটা করে গোনে।
            - `ROWS` দিলেও unique order key *না* থাকলে দুটো peer-এর ক্রম এলোমেলো, তাই মাঝের value (150 বা 130) বিভিন্ন run-এ বদলাতে পারে — সবসময় tie-breaker দাও।
            - Window-এ একেবারেই `ORDER BY` না দিলে (`SUM(amount) OVER ()`) পাওয়া যেত `200, 200, 200, 200`: তখন frame পুরো partition।
            - Running balance-এর (bank statement, ledger) জন্য সহজ নিয়ম: `ORDER BY <time>, <id> ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`।
            - `LAST_VALUE()`-এও একই ফাঁদ: default frame-এ এটা partition-এর শেষ row নয়, current row-এর শেষ peer দেয় — `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` ব্যবহার করো।
        """,
        tip_en=r"""Name the default frame exactly (`RANGE ... CURRENT ROW`) and explain "peers". Then show the `ROWS` + tie-breaker fix — that's the practical takeaway interviewers want.""",
        tip_bn=r"""Default frame-এর নাম হুবহু বলো (`RANGE ... CURRENT ROW`) আর "peer" ব্যাখ্যা করো। তারপর `ROWS` + tie-breaker দিয়ে সমাধান দেখাও — interviewer এই practical শিক্ষাটাই চায়।""",
        related=["sql-014"],
        refs=[PG_WINDOW_CALLS, SQLITE_WINDOW],
    ),
    # ------------------------------------------------------------------ sql-026
    Q(
        id="sql-026", sub="Keyset Pagination & Query Optimization", diff="hard", type="query",
        prio="high", market="both", mins=8,
        tags=["pagination", "keyset", "offset", "row-values", "performance"],
        ver="Row-value comparison: PostgreSQL, MySQL 8, SQLite 3.15+; output from PostgreSQL 18", vs=False, status="stable",
        q_en=r"""A feed shows posts newest first (`ORDER BY created_at DESC, id DESC`), 3 per page. The last post on the current page is `(created_at = '2026-10-10 09:00:00', id = 5)`. Write the query for the **next page using keyset (seek) pagination**, and explain why it beats `LIMIT ... OFFSET` on large tables.""",
        q_bn=r"""একটা feed সবচেয়ে নতুন post আগে দেখায় (`ORDER BY created_at DESC, id DESC`), প্রতি page-এ ৩টা। বর্তমান page-এর শেষ post হলো `(created_at = '2026-10-10 09:00:00', id = 5)`। **Keyset (seek) pagination দিয়ে পরের page**-এর query লেখো, আর বড় table-এ এটা কেন `LIMIT ... OFFSET`-এর চেয়ে ভালো ব্যাখ্যা করো।""",
        setup=r"""
            CREATE TABLE posts (
              id         INT PRIMARY KEY,
              title      VARCHAR(100) NOT NULL,
              created_at TIMESTAMP NOT NULL
            );

            INSERT INTO posts (id, title, created_at) VALUES
              (1, 'Intro to SQL',     '2026-10-05 10:00:00'),
              (2, 'Joins explained',  '2026-10-06 12:00:00'),
              (3, 'Indexes 101',      '2026-10-08 09:00:00'),
              (4, 'Window functions', '2026-10-10 09:00:00'),
              (5, 'CTEs',             '2026-10-10 09:00:00'),
              (6, 'Transactions',     '2026-10-11 15:00:00'),
              (7, 'Normalization',    '2026-10-12 08:00:00'),
              (8, 'Query plans',      '2026-10-12 11:30:00');

            CREATE INDEX idx_posts_created_id ON posts (created_at, id);
        """,
        code=r"""
            SELECT id, title, created_at
            FROM posts
            WHERE (created_at, id) < ('2026-10-10 09:00:00', 5)   -- "after" the last row seen
            ORDER BY created_at DESC, id DESC
            LIMIT 3;                                             -- standard: FETCH FIRST 3 ROWS ONLY
        """,
        lang="sql",
        output=r"""
             id |      title       |     created_at
            ----+------------------+---------------------
              4 | Window functions | 2026-10-10 09:00:00
              3 | Indexes 101      | 2026-10-08 09:00:00
              2 | Joins explained  | 2026-10-06 12:00:00
        """,
        extra=[dict(lang="sql", label_en="Expanded form (for databases without row-value comparison) and the OFFSET version",
                    label_bn="বিস্তৃত রূপ (row-value comparison নেই এমন database-এর জন্য) আর OFFSET version", src=r"""
            -- equivalent without row values (works everywhere, e.g. SQL Server)
            SELECT id, title, created_at
            FROM posts
            WHERE created_at < '2026-10-10 09:00:00'
               OR (created_at = '2026-10-10 09:00:00' AND id < 5)
            ORDER BY created_at DESC, id DESC
            FETCH FIRST 3 ROWS ONLY;     -- SQL Server needs OFFSET 0 ROWS before FETCH

            -- OFFSET pagination: page 3 = skip 6 rows; cost grows with the offset
            SELECT id, title, created_at
            FROM posts
            ORDER BY created_at DESC, id DESC
            LIMIT 3 OFFSET 6;
        """)],
        a_en=r"""
            The sort key is `(created_at, id)`; `id` is the tie-breaker that makes it unique. The next page is "every row that comes **after** `(2026-10-10 09:00:00, 5)` in descending order", i.e. `(created_at, id) < (that pair)`. A row-value comparison is lexicographic: compare `created_at` first, and only when equal compare `id`. So post 4 — same timestamp as the cursor but smaller id — is correctly included, and post 5 isn't repeated.

            **Why it beats OFFSET:** `OFFSET 100000` makes the database produce and throw away 100,000 rows before returning 3, so deep pages get linearly slower. The keyset query seeks straight into the `(created_at, id)` index and reads only 3 rows — constant time at any depth. It's also stable: if new posts arrive while a user scrolls, OFFSET shifts everything and shows duplicates or skips rows; a keyset cursor doesn't.
        """,
        a_bn=r"""
            Sort key হলো `(created_at, id)`; `id` হলো tie-breaker, যা key-টাকে unique করে। পরের page মানে "descending ক্রমে `(2026-10-10 09:00:00, 5)`-এর **পরে** আসা সব row", অর্থাৎ `(created_at, id) < (ওই জোড়া)`। Row-value comparison lexicographic: আগে `created_at` তুলনা হয়, সমান হলে তবেই `id`। তাই post 4 — cursor-এর সমান timestamp কিন্তু ছোট id — ঠিকভাবেই আসে, আর post 5 আবার আসে না।

            **কেন OFFSET-এর চেয়ে ভালো:** `OFFSET 100000` দিলে database ৩টা row দেওয়ার আগে ১,০০,০০০ row তৈরি করে ফেলে দেয়, তাই যত গভীর page তত ধীর। Keyset query সরাসরি `(created_at, id)` index-এ seek করে মাত্র ৩টা row পড়ে — যেকোনো গভীরতায় একই সময়। এটা stable-ও: user scroll করার সময় নতুন post এলে OFFSET সব সরিয়ে দেয়, ফলে duplicate দেখায় বা row বাদ পড়ে; keyset cursor-এ তা হয় না।
        """,
        ex_en=r"""
            - **Index:** `(created_at, id)` serves both directions — a B-tree can be scanned backwards for `DESC, DESC`. The `ORDER BY` must match the index and the cursor columns exactly.
            - **API design:** return an opaque cursor (e.g. base64 of `created_at|id`) instead of page numbers. Trade-off: no "jump to page 57" — fine for infinite scroll and APIs, less so for admin tables (where OFFSET on small, filtered sets is acceptable).
            - **Dialects:** row-value `<`/`>` comparisons work in PostgreSQL, MySQL, and SQLite 3.15+, but not in SQL Server or Oracle, and some optimizers (older MySQL) don't use the index well for them — the expanded `OR` form is the portable fallback. `LIMIT/OFFSET` is PostgreSQL/MySQL/SQLite; the standard is `OFFSET n ROWS FETCH FIRST m ROWS ONLY`.
            - **Time zones & precision:** use the exact stored value in the cursor (including microseconds); rounding it can skip or repeat rows.
            - Also avoid `SELECT COUNT(*)` on every page for huge tables; show "more results" instead of an exact total.
        """,
        ex_bn=r"""
            - **Index:** `(created_at, id)` দুই দিকই সামলায় — `DESC, DESC`-এর জন্য B-tree উল্টো দিকে scan করা যায়। `ORDER BY`-কে index আর cursor column-এর সাথে হুবহু মিলতে হবে।
            - **API design:** page number-এর বদলে একটা opaque cursor দাও (যেমন `created_at|id`-এর base64)। Trade-off: "সরাসরি ৫৭ নম্বর page-এ যাও" করা যায় না — infinite scroll আর API-র জন্য ঠিক আছে, admin table-এর জন্য কম (সেখানে ছোট, filter করা set-এ OFFSET চলে)।
            - **Dialect:** row-value `<`/`>` তুলনা PostgreSQL, MySQL আর SQLite 3.15+-এ চলে, কিন্তু SQL Server বা Oracle-এ চলে না, আর কিছু optimizer (পুরনো MySQL) এগুলোর জন্য index ভালোভাবে ব্যবহার করে না — বিস্তৃত `OR` রূপটাই portable বিকল্প। `LIMIT/OFFSET` হলো PostgreSQL/MySQL/SQLite-এর; standard হলো `OFFSET n ROWS FETCH FIRST m ROWS ONLY`।
            - **Time zone আর precision:** cursor-এ হুবহু জমা থাকা value ব্যবহার করো (microsecond-সহ); round করলে row বাদ পড়তে বা দুবার আসতে পারে।
            - বিশাল table-এ প্রতিটা page-এ `SELECT COUNT(*)` এড়িয়ে চলো; সঠিক মোট সংখ্যার বদলে "আরও আছে" দেখাও।
        """,
        tip_en=r"""Point out the tie on `2026-10-10 09:00:00` and show why `id` must be part of the cursor — that's the bug most implementations have. Then quantify the OFFSET cost ("reads offset + limit rows").""",
        tip_bn=r"""`2026-10-10 09:00:00`-এর tie-টা দেখাও আর বোঝাও কেন `id`-কে cursor-এর অংশ হতেই হবে — বেশিরভাগ implementation-এ এই bug-টাই থাকে। তারপর OFFSET-এর খরচ সংখ্যায় বলো ("offset + limit সংখ্যক row পড়ে")।""",
        mist_en=r"""Using only `WHERE created_at < :last_created_at` (skips post 4, which shares the timestamp), or ordering by a non-unique column so pages overlap.""",
        mist_bn=r"""শুধু `WHERE created_at < :last_created_at` ব্যবহার করা (একই timestamp-এর post 4 বাদ পড়ে যায়), অথবা non-unique column দিয়ে order করা, যাতে page-গুলো একে অপরের সাথে মিশে যায়।""",
        follow=[
            ("How would you support a 'previous page' button with keyset pagination?", "Keyset pagination-এ 'আগের page' button কীভাবে support করবে?"),
            ("How do you paginate when users can sort by price or rating instead?", "User যদি price বা rating দিয়ে sort করতে পারে, তখন pagination কীভাবে করবে?"),
        ],
        related=["sql-020", "sql-031"],
        refs=[PG_LIMIT, PG_ROW_COMPARISON, PG_USING_EXPLAIN],
    ),
    # ------------------------------------------------------------------ sql-027
    Q(
        id="sql-027", sub="Views & Materialized Views", diff="hard", type="comparison",
        prio="medium", market="both", mins=7,
        tags=["views", "materialized-views", "refresh", "reporting", "security"],
        ver="PostgreSQL 18 syntax for materialized views (feature varies by database)", vs=False, status="stable",
        q_en=r"""Compare views and materialized views. When would you use each, how do you keep a materialized view fresh, and what are the pitfalls?""",
        q_bn=r"""View আর materialized view-এর তুলনা করো। কোনটা কখন ব্যবহার করবে, materialized view কীভাবে হালনাগাদ রাখবে, আর ফাঁদগুলো কী?""",
        a_en=r"""
            - **View:** a saved query with a name; it stores no data. Every time you select from it, the underlying query runs, so results are always current. Uses: hide complexity (joins/filters behind one name), present a stable interface while tables change, and limit access to certain rows or columns.
            - **Materialized view:** stores the query's **result** on disk like a table, so reads are fast, and you can index it. But the data is a snapshot — stale until you refresh it.

            I use a view for reusable logic and access control, and a materialized view for expensive aggregations that can tolerate some staleness (dashboards, leaderboards, daily reports).

            **Keeping it fresh (PostgreSQL):** `REFRESH MATERIALIZED VIEW` recomputes the whole thing. Plain refresh locks out readers while it runs; `REFRESH MATERIALIZED VIEW CONCURRENTLY` lets reads continue but requires a unique index on the view and is slower. Schedule refreshes (cron/pg_cron/a job) based on how fresh the data must be.
        """,
        a_bn=r"""
            - **View:** নামসহ সংরক্ষিত একটা query; কোনো data রাখে না। যতবার এখান থেকে select করো, ভেতরের query ততবার চলে, তাই ফলাফল সবসময় হালনাগাদ। ব্যবহার: জটিলতা লুকানো (join/filter এক নামের পেছনে), table বদলালেও একটা stable interface রাখা, আর নির্দিষ্ট row বা column-এ access সীমিত করা।
            - **Materialized view:** query-র **ফলাফল** table-এর মতো disk-এ রাখে, তাই read দ্রুত, আর এতে index দেওয়া যায়। কিন্তু data একটা snapshot — refresh না করা পর্যন্ত পুরনো।

            পুনর্ব্যবহারযোগ্য logic আর access control-এর জন্য আমি view, আর কিছুটা পুরনো data মেনে নেওয়া যায় এমন ব্যয়বহুল aggregation-এর জন্য (dashboard, leaderboard, দৈনিক report) materialized view ব্যবহার করি।

            **হালনাগাদ রাখা (PostgreSQL):** `REFRESH MATERIALIZED VIEW` পুরোটা আবার হিসাব করে। সাধারণ refresh চলার সময় reader-দের আটকে রাখে; `REFRESH MATERIALIZED VIEW CONCURRENTLY` read চলতে দেয়, কিন্তু view-তে একটা unique index লাগে আর এটা ধীর। Data কতটা হালনাগাদ লাগবে সেই অনুযায়ী refresh schedule করো (cron/pg_cron/একটা job)।
        """,
        ex_en=r"""
            - **Views aren't a performance feature by themselves** — the optimizer usually inlines them. Stacking views on views can hide very expensive queries.
            - **Updatable views:** simple single-table views can accept `INSERT/UPDATE/DELETE`; add `WITH CHECK OPTION` so writes can't create rows the view wouldn't show.
            - **Security:** grant `SELECT` on the view but not the base table to expose only certain columns. In PostgreSQL, views run with the owner's privileges by default; `security_invoker` (PG15+) makes them use the caller's, which matters with row-level security. `security_barrier` prevents leaky functions from seeing hidden rows.
            - **Database support differs:** PostgreSQL and Oracle have materialized views (Oracle also supports incremental "fast refresh"); SQL Server has *indexed views* that are maintained automatically on every write; MySQL has none — use a summary table updated by a job or triggers.
            - **Full refresh cost grows with data.** For very large aggregates, an incrementally maintained summary table (recompute only recent days) often beats a materialized view.
            - Dependencies: you can't change a column's type while views depend on it — migrations must drop and recreate them.
        """,
        ex_bn=r"""
            - **View নিজে কোনো performance feature নয়** — optimizer সাধারণত এগুলো inline করে দেয়। View-এর উপর view চাপালে খুব ব্যয়বহুল query লুকিয়ে থাকতে পারে।
            - **Updatable view:** সাধারণ single-table view `INSERT/UPDATE/DELETE` নিতে পারে; `WITH CHECK OPTION` দাও, যাতে write এমন row তৈরি করতে না পারে যেটা view দেখাবে না।
            - **Security:** base table-এ না দিয়ে শুধু view-তে `SELECT` grant করো, তাহলে শুধু নির্দিষ্ট column দেখানো যায়। PostgreSQL-এ view default-ভাবে owner-এর privilege নিয়ে চলে; `security_invoker` (PG15+) caller-এর privilege ব্যবহার করায়, যা row-level security-র সাথে গুরুত্বপূর্ণ। `security_barrier` leaky function-কে লুকানো row দেখতে দেয় না।
            - **Database-ভেদে support আলাদা:** PostgreSQL আর Oracle-এ materialized view আছে (Oracle incremental "fast refresh"-ও support করে); SQL Server-এ *indexed view* আছে, যা প্রতিটা write-এ automatically maintain হয়; MySQL-এ নেই — job বা trigger দিয়ে update হওয়া summary table ব্যবহার করো।
            - **Data বাড়লে full refresh-এর খরচও বাড়ে।** খুব বড় aggregate-এর জন্য incremental-ভাবে maintain করা summary table (শুধু সাম্প্রতিক দিনগুলো আবার হিসাব) প্রায়ই materialized view-এর চেয়ে ভালো।
            - Dependency: কোনো column-এর উপর view নির্ভর করলে তার type বদলানো যায় না — migration-এ এগুলো drop করে আবার বানাতে হয়।
        """,
        tip_en=r"""Frame it as "freshness vs read cost". Mentioning `CONCURRENTLY` + the unique-index requirement and the per-database differences (SQL Server indexed views, MySQL none) shows breadth.""",
        tip_bn=r""""হালনাগাদ থাকা বনাম read-এর খরচ" — এভাবে সাজাও। `CONCURRENTLY` + unique index-এর শর্ত আর database-ভেদে পার্থক্য (SQL Server-এর indexed view, MySQL-এ নেই) বললে জ্ঞানের বিস্তৃতি দেখা যায়।""",
        mist_en=r"""Expecting a normal view to make a slow query fast, or forgetting that a materialized view is stale until refreshed (and that plain refresh blocks readers in PostgreSQL).""",
        mist_bn=r"""ভাবা যে সাধারণ view একটা ধীর query-কে দ্রুত করে দেবে, অথবা ভুলে যাওয়া যে materialized view refresh না করা পর্যন্ত পুরনো থাকে (আর PostgreSQL-এ সাধারণ refresh reader-দের আটকে দেয়)।""",
        code=r"""
            -- view: always fresh, stores nothing; also a simple access-control layer
            CREATE VIEW paid_orders AS
            SELECT id, customer_id, amount, created_at
            FROM orders
            WHERE status = 'paid';

            GRANT SELECT ON paid_orders TO reporting;   -- no access to the base table needed

            -- materialized view (PostgreSQL): stores the result, must be refreshed
            CREATE MATERIALIZED VIEW daily_revenue AS
            SELECT CAST(created_at AS DATE) AS day,
                   SUM(amount)              AS revenue,
                   COUNT(*)                 AS orders
            FROM orders
            WHERE status = 'paid'
            GROUP BY CAST(created_at AS DATE);

            CREATE UNIQUE INDEX daily_revenue_day_uq ON daily_revenue (day);  -- required for CONCURRENTLY

            REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;             -- readers are not blocked
        """,
        lang="sql",
        follow=[
            ("How would you get near-real-time dashboard numbers without refreshing a huge materialized view?", "বিশাল materialized view refresh না করে প্রায় real-time dashboard-এর সংখ্যা কীভাবে পাবে?"),
            ("What does `WITH CHECK OPTION` do on an updatable view?", "Updatable view-তে `WITH CHECK OPTION` কী করে?"),
        ],
        related=["sql-031", "sql-028"],
        refs=[PG_VIEWS, PG_MATVIEWS, PG_REFRESH_MV],
    ),
    # ------------------------------------------------------------------ sql-028
    Q(
        id="sql-028", sub="Stored Procedures & Triggers", diff="hard", type="architecture",
        prio="medium", market="both", mins=10,
        tags=["stored-procedures", "triggers", "business-logic", "plpgsql", "architecture"],
        ver="PostgreSQL 18 examples (PL/pgSQL; procedures since 11)", vs=False, status="stable",
        q_en=r"""Your team is debating whether to put business logic in stored procedures and triggers or keep it in the Node.js/NestJS application. What are the trade-offs, and where do you draw the line?""",
        q_bn=r"""তোমার team তর্ক করছে business logic stored procedure আর trigger-এ রাখবে, নাকি Node.js/NestJS application-এ। Trade-off-গুলো কী, আর তুমি সীমারেখা কোথায় টানবে?""",
        a_en=r"""
            **Database-side logic — pros**
            - Runs next to the data: set-based operations over millions of rows without shipping them over the network.
            - Enforced for **every** writer — the app, scripts, admin tools, other services.
            - Atomic with the data change, and you can grant `EXECUTE` on a procedure instead of table access.

            **Cons**
            - Harder to version, review, unit-test, debug, and observe than application code; fewer developers know PL/pgSQL or T-SQL well.
            - Vendor lock-in.
            - The primary database is the hardest component to scale; CPU spent on business logic there is expensive.
            - **Triggers are invisible side effects:** an `UPDATE` that silently fires three triggers surprises people, slows bulk operations (row-level triggers run per row), and makes behaviour hard to reason about.

            **Where I draw the line**
            - Declarative constraints first (`NOT NULL`, `CHECK`, `UNIQUE`, FKs) — always in the database.
            - Triggers only for small, data-centric rules that must hold for every writer: `updated_at`, audit/history rows, maintaining a denormalized counter, or writing an outbox row.
            - Procedures/functions for data-heavy batch work (archiving, backfills, ETL) and occasional performance-critical set operations.
            - Business workflows — pricing rules, emails, payments, calling external APIs — stay in the application, where they're testable and observable.
        """,
        a_bn=r"""
            **Database-এর ভেতরে logic — সুবিধা**
            - Data-র পাশেই চলে: লাখো row network দিয়ে না পাঠিয়েই set-based operation।
            - **প্রতিটা** writer-এর জন্য enforce হয় — app, script, admin tool, অন্য service।
            - Data পরিবর্তনের সাথে atomic, আর table access-এর বদলে procedure-এ `EXECUTE` grant করা যায়।

            **অসুবিধা**
            - Application code-এর চেয়ে version, review, unit-test, debug আর observe করা কঠিন; PL/pgSQL বা T-SQL ভালো জানে এমন developer কম।
            - Vendor lock-in।
            - Primary database scale করা সবচেয়ে কঠিন; সেখানে business logic-এ খরচ হওয়া CPU দামি।
            - **Trigger হলো অদৃশ্য side effect:** একটা `UPDATE` নীরবে তিনটা trigger চালালে মানুষ অবাক হয়, bulk operation ধীর হয় (row-level trigger প্রতি row-এ চলে), আর আচরণ বোঝা কঠিন হয়ে যায়।

            **আমি সীমারেখা যেখানে টানি**
            - আগে declarative constraint (`NOT NULL`, `CHECK`, `UNIQUE`, FK) — এগুলো সবসময় database-এ।
            - Trigger শুধু ছোট, data-কেন্দ্রিক নিয়মের জন্য যা প্রতিটা writer-এর জন্য খাটতে হবে: `updated_at`, audit/history row, denormalized counter maintain করা, বা outbox row লেখা।
            - Data-ভারী batch কাজের জন্য procedure/function (archiving, backfill, ETL), আর মাঝে মাঝে performance-critical set operation।
            - Business workflow — pricing rule, email, payment, external API call — application-এই থাকে, যেখানে এগুলো test আর observe করা যায়।
        """,
        ex_en=r"""
            - **Function vs procedure in PostgreSQL:** a `FUNCTION` returns a value and runs inside the caller's transaction; a `PROCEDURE` (PG11+) is invoked with `CALL` and can `COMMIT` inside, which suits batch jobs like the archiving loop in the example.
            - **Testing:** if you do put logic in the database, keep it in migrations under version control and test it (e.g. pgTAP, or integration tests against a real database in CI).
            - **Trigger pitfalls:** recursion (a trigger updating the same table), ordering between multiple triggers, and the fact that `TRUNCATE` and bulk loads may bypass row-level triggers. Use `WHEN (...)` conditions and `AFTER UPDATE OF column` to fire only when needed.
            - **Outbox pattern:** writing an event row in the same transaction (from the app or a trigger) and publishing it asynchronously avoids "DB committed but message lost" bugs — a good use of database-side guarantees.
            - In the Bangladesh market, legacy banking/ERP systems often keep heavy logic in Oracle/SQL Server procedures; being able to read and migrate them is a valuable skill.
        """,
        ex_bn=r"""
            - **PostgreSQL-এ function বনাম procedure:** `FUNCTION` একটা value return করে আর caller-এর transaction-এর ভেতরে চলে; `PROCEDURE` (PG11+) `CALL` দিয়ে চালানো হয় আর ভেতরে `COMMIT` করতে পারে, যা উদাহরণের archiving loop-এর মতো batch job-এর জন্য মানানসই।
            - **Testing:** database-এ logic রাখলে সেটা version control-এ migration হিসেবে রাখো আর test করো (যেমন pgTAP, বা CI-তে আসল database-এর বিরুদ্ধে integration test)।
            - **Trigger-এর ফাঁদ:** recursion (trigger একই table update করে), একাধিক trigger-এর মধ্যে ক্রম, আর `TRUNCATE` ও bulk load-এ row-level trigger এড়িয়ে যাওয়ার সম্ভাবনা। শুধু দরকার হলেই চালাতে `WHEN (...)` condition আর `AFTER UPDATE OF column` ব্যবহার করো।
            - **Outbox pattern:** একই transaction-এ একটা event row লেখা (app বা trigger থেকে) আর পরে asynchronously publish করা "DB commit হলো কিন্তু message হারিয়ে গেল" ধরনের bug এড়ায় — database-এর guarantee-র একটা ভালো ব্যবহার।
            - বাংলাদেশের বাজারে legacy banking/ERP system প্রায়ই ভারী logic Oracle/SQL Server procedure-এ রাখে; এগুলো পড়তে আর migrate করতে পারা একটা মূল্যবান দক্ষতা।
        """,
        tip_en=r"""Avoid a dogmatic answer. Give pros/cons, then a clear rule of thumb with concrete examples on each side of the line — interviewers want judgement, not ideology.""",
        tip_bn=r"""গোঁড়া উত্তর এড়িয়ে চলো। সুবিধা/অসুবিধা দাও, তারপর সীমারেখার দুই পাশের concrete উদাহরণসহ একটা পরিষ্কার নিয়ম বলো — interviewer মতবাদ নয়, বিচারবুদ্ধি দেখতে চায়।""",
        mist_en=r"""Putting external API calls or emails inside triggers, or rejecting database-side logic entirely and losing guarantees that only constraints/triggers can give for all writers.""",
        mist_bn=r"""Trigger-এর ভেতরে external API call বা email পাঠানো, অথবা database-এর ভেতরের logic পুরোপুরি বাতিল করে সেই guarantee হারানো যা সব writer-এর জন্য শুধু constraint/trigger-ই দিতে পারে।""",
        code=r"""
            -- trigger 1: keep updated_at correct for every writer
            CREATE FUNCTION set_updated_at() RETURNS trigger
            LANGUAGE plpgsql AS $$
            BEGIN
              NEW.updated_at := now();
              RETURN NEW;
            END;
            $$;

            CREATE TRIGGER orders_set_updated_at
            BEFORE UPDATE ON orders
            FOR EACH ROW EXECUTE FUNCTION set_updated_at();

            -- trigger 2: audit status changes only when the status really changes
            CREATE FUNCTION audit_order_status() RETURNS trigger
            LANGUAGE plpgsql AS $$
            BEGIN
              INSERT INTO order_audit (order_id, old_status, new_status)
              VALUES (OLD.id, OLD.status, NEW.status);
              RETURN NULL;
            END;
            $$;

            CREATE TRIGGER orders_audit_status
            AFTER UPDATE OF status ON orders
            FOR EACH ROW
            WHEN (OLD.status IS DISTINCT FROM NEW.status)
            EXECUTE FUNCTION audit_order_status();

            -- procedure: batch archiving that commits per batch (PostgreSQL 11+)
            CREATE PROCEDURE archive_old_orders(cutoff DATE, batch_size INT)
            LANGUAGE plpgsql AS $$
            DECLARE
              moved INT;
            BEGIN
              LOOP
                WITH batch AS (
                  DELETE FROM orders
                  WHERE id IN (SELECT id FROM orders WHERE created_at < cutoff ORDER BY id LIMIT batch_size)
                  RETURNING *
                )
                INSERT INTO orders_archive SELECT * FROM batch;
                GET DIAGNOSTICS moved = ROW_COUNT;
                EXIT WHEN moved = 0;
                COMMIT;
              END LOOP;
            END;
            $$;

            CALL archive_old_orders('2025-01-01', 5000);
        """,
        lang="sql",
        follow=[
            ("How would you test a trigger as part of CI?", "CI-র অংশ হিসেবে একটা trigger কীভাবে test করবে?"),
            ("What is the transactional outbox pattern, and why might you implement it with a trigger?", "Transactional outbox pattern কী, আর কেন এটা trigger দিয়ে implement করতে পারো?"),
        ],
        related=["sql-027", "sql-022", "sql-021"],
        refs=[PG_TRIGGERS, PG_PROCEDURE],
    ),
    # ------------------------------------------------------------------ sql-029
    Q(
        id="sql-029", sub="Isolation Levels & Read Phenomena", diff="hard", type="conceptual",
        prio="high", market="both", mins=8,
        tags=["isolation-levels", "dirty-read", "non-repeatable-read", "phantom-read", "transactions"],
        ver="ISO SQL isolation levels; defaults per database as of 2026", vs=False, status="stable",
        q_en=r"""Explain the four standard transaction isolation levels and the read phenomena each one allows (dirty reads, non-repeatable reads, phantoms). What are the defaults in common databases, and how do you choose a level?""",
        q_bn=r"""চারটা standard transaction isolation level আর প্রতিটা কোন read phenomenon হতে দেয় (dirty read, non-repeatable read, phantom) — ব্যাখ্যা করো। জনপ্রিয় database-গুলোর default কী, আর তুমি কীভাবে level বেছে নাও?""",
        a_en=r"""
            **The phenomena**
            - **Dirty read:** reading another transaction's *uncommitted* change (which might be rolled back).
            - **Non-repeatable read:** reading the same row twice in one transaction and getting different values because someone committed an update in between.
            - **Phantom read:** re-running a query with a `WHERE` condition and getting a different *set* of rows because someone inserted/deleted matching rows.

            **The levels (per the SQL standard)**
            - **Read Uncommitted:** allows all three.
            - **Read Committed:** no dirty reads; non-repeatable reads and phantoms possible.
            - **Repeatable Read:** no dirty or non-repeatable reads; the standard still allows phantoms.
            - **Serializable:** results equal *some* serial order of the transactions — none of the anomalies.

            **Defaults:** PostgreSQL, Oracle, and SQL Server use Read Committed; MySQL InnoDB uses Repeatable Read.

            **Choosing:** Read Committed plus explicit row locks or atomic conditional updates covers most OLTP work. Use Repeatable Read for consistent multi-query reports, and Serializable when correctness depends on invariants across rows — with automatic retries on serialization failures.
        """,
        a_bn=r"""
            **Phenomenon-গুলো**
            - **Dirty read:** অন্য transaction-এর *uncommitted* পরিবর্তন পড়া (যেটা rollback হয়ে যেতে পারে)।
            - **Non-repeatable read:** একই transaction-এ একই row দুবার পড়ে আলাদা value পাওয়া, কারণ মাঝখানে কেউ update commit করেছে।
            - **Phantom read:** `WHERE` condition-সহ একটা query আবার চালিয়ে row-এর ভিন্ন *set* পাওয়া, কারণ কেউ matching row insert/delete করেছে।

            **Level-গুলো (SQL standard অনুযায়ী)**
            - **Read Uncommitted:** তিনটাই হতে দেয়।
            - **Read Committed:** dirty read নেই; non-repeatable read আর phantom হতে পারে।
            - **Repeatable Read:** dirty বা non-repeatable read নেই; standard তবুও phantom হতে দেয়।
            - **Serializable:** ফলাফল transaction-গুলোর *কোনো একটা* serial ক্রমের সমান — কোনো anomaly নেই।

            **Default:** PostgreSQL, Oracle আর SQL Server-এ Read Committed; MySQL InnoDB-তে Repeatable Read।

            **বাছাই:** বেশিরভাগ OLTP কাজে Read Committed + explicit row lock বা atomic conditional update যথেষ্ট। একাধিক query-র consistent report-এর জন্য Repeatable Read, আর correctness যখন একাধিক row জুড়ে থাকা invariant-এর উপর নির্ভর করে তখন Serializable — serialization failure হলে automatic retry-সহ।
        """,
        ex_en=r"""
            - **The standard defines minimums; implementations differ.** PostgreSQL's Repeatable Read is snapshot-based and also prevents phantoms, and PostgreSQL never allows dirty reads (Read Uncommitted behaves like Read Committed). MySQL InnoDB's Repeatable Read uses a consistent snapshot for plain `SELECT`s, but locking reads and `UPDATE`s see the latest committed rows and use gap/next-key locks.
            - **SQL Server's** Read Committed is lock-based by default (writers block readers, and readers' shared locks can block writers) unless `READ_COMMITTED_SNAPSHOT` is enabled (it is on by default in Azure SQL Database). It also offers a separate `SNAPSHOT` level.
            - **Anomalies outside the original three:** *lost updates* (two read-modify-write transactions overwrite each other) and *write skew* (two transactions each check a condition, then update different rows, breaking a shared invariant). Snapshot isolation alone does not prevent write skew; true Serializable does.
            - Higher isolation = more blocking or more aborted transactions. Keep transactions short and design for retries (idempotency keys).
        """,
        ex_bn=r"""
            - **Standard শুধু ন্যূনতম শর্ত দেয়; implementation আলাদা।** PostgreSQL-এর Repeatable Read snapshot-ভিত্তিক আর phantom-ও আটকায়, আর PostgreSQL কখনো dirty read হতে দেয় না (Read Uncommitted আসলে Read Committed-এর মতো আচরণ করে)। MySQL InnoDB-র Repeatable Read সাধারণ `SELECT`-এর জন্য consistent snapshot ব্যবহার করে, কিন্তু locking read আর `UPDATE` সর্বশেষ committed row দেখে আর gap/next-key lock ব্যবহার করে।
            - **SQL Server**-এর Read Committed default-ভাবে lock-ভিত্তিক (writer reader-কে block করে, আর reader-এর shared lock-ও writer-কে block করতে পারে), যদি না `READ_COMMITTED_SNAPSHOT` চালু থাকে (Azure SQL Database-এ এটা default-ভাবে চালু)। এর আলাদা একটা `SNAPSHOT` level-ও আছে।
            - **মূল তিনটার বাইরের anomaly:** *lost update* (দুটো read-modify-write transaction একে অপরকে overwrite করে) আর *write skew* (দুটো transaction প্রত্যেকে একটা শর্ত যাচাই করে, তারপর আলাদা row update করে, একটা যৌথ invariant ভেঙে ফেলে)। শুধু snapshot isolation write skew আটকায় না; আসল Serializable আটকায়।
            - Isolation যত বেশি = তত বেশি blocking বা abort হওয়া transaction। Transaction ছোট রাখো আর retry-র জন্য design করো (idempotency key)।
        """,
        tip_en=r"""Define each phenomenon with a tiny two-session example, then map levels to phenomena. Adding "the standard sets minimums — PostgreSQL's RR also blocks phantoms, MySQL's default is RR" shows you know real engines, not just textbooks.""",
        tip_bn=r"""প্রতিটা phenomenon ছোট্ট দুই-session-এর উদাহরণ দিয়ে সংজ্ঞায়িত করো, তারপর level-গুলোকে phenomenon-এর সাথে মেলাও। "Standard ন্যূনতম শর্ত দেয় — PostgreSQL-এর RR phantom-ও আটকায়, MySQL-এর default RR" — এটা যোগ করলে বোঝা যায় তুমি শুধু বই নয়, আসল engine চেনো।""",
        mist_en=r"""Assuming every database implements a level the same way, or believing Repeatable Read prevents lost updates and write skew in all engines.""",
        mist_bn=r"""ধরে নেওয়া যে প্রতিটা database একটা level একইভাবে implement করে, অথবা বিশ্বাস করা যে Repeatable Read সব engine-এ lost update আর write skew আটকায়।""",
        code=r"""
            Level              | Dirty read | Non-repeatable read | Phantom read
            -------------------+------------+---------------------+---------------------------
            READ UNCOMMITTED   | possible   | possible            | possible
            READ COMMITTED     | prevented  | possible            | possible
            REPEATABLE READ    | prevented  | prevented           | possible (per the standard)
            SERIALIZABLE       | prevented  | prevented           | prevented
        """,
        lang="text",
        extra=[dict(lang="sql", label_en="Non-repeatable read under READ COMMITTED (two sessions)",
                    label_bn="READ COMMITTED-এ non-repeatable read (দুটো session)", src=r"""
            -- Session A
            START TRANSACTION;                 -- READ COMMITTED
            SELECT balance FROM accounts WHERE id = 1;   -- 500

            -- Session B
            UPDATE accounts SET balance = 300 WHERE id = 1;
            COMMIT;

            -- Session A (same transaction)
            SELECT balance FROM accounts WHERE id = 1;   -- 300  <- non-repeatable read
            COMMIT;

            -- under REPEATABLE READ, Session A would still see 500 in its second SELECT
        """)],
        follow=[
            ("Give an example of write skew and explain which isolation level prevents it.", "Write skew-এর একটা উদাহরণ দাও, আর কোন isolation level এটা আটকায় ব্যাখ্যা করো।"),
            ("How should application code handle serialization failures?", "Application code-কে serialization failure কীভাবে সামলাতে হবে?"),
        ],
        related=["sql-010"],
        refs=[PG_ISO, MS_ISO],
    ),
    # ------------------------------------------------------------------ sql-030
    Q(
        id="sql-030", sub="Gaps and Islands", diff="extreme", type="query",
        prio="medium", market="both", mins=12,
        tags=["gaps-and-islands", "window-functions", "streaks", "row-number", "date-arithmetic"],
        ver="Window functions are standard; date − integer arithmetic shown is PostgreSQL-specific (output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""The `logins` table records the days each user logged in (a user can log in several times a day). For each user, find their **longest streak of consecutive login days**: start date, end date, and length. If a user has two equally long streaks, return the earlier one.""",
        q_bn=r"""`logins` table-এ প্রতিটা user কোন কোন দিন login করেছে তা রাখা আছে (একজন user দিনে একাধিকবার login করতে পারে)। প্রতিটা user-এর **টানা login দিনের সবচেয়ে লম্বা streak** বের করো: শুরুর তারিখ, শেষের তারিখ আর দৈর্ঘ্য। কোনো user-এর সমান দৈর্ঘ্যের দুটো streak থাকলে আগেরটা return করো।""",
        setup=r"""
            CREATE TABLE logins (
              user_id    INT  NOT NULL,
              login_date DATE NOT NULL
            );

            INSERT INTO logins (user_id, login_date) VALUES
              (1, '2026-10-01'), (1, '2026-10-02'), (1, '2026-10-02'), (1, '2026-10-03'),
              (1, '2026-10-05'), (1, '2026-10-06'),
              (2, '2026-10-02'), (2, '2026-10-04'), (2, '2026-10-05'), (2, '2026-10-06'), (2, '2026-10-07'),
              (3, '2026-10-03');
        """,
        code=r"""
            WITH days AS (                       -- 1. one row per user per day
              SELECT DISTINCT user_id, login_date
              FROM logins
            ),
            islands AS (                         -- 2. date minus row number is constant inside a streak
              SELECT user_id, login_date,
                     login_date - CAST(ROW_NUMBER() OVER (PARTITION BY user_id
                                                          ORDER BY login_date) AS INT) AS grp
              FROM days
            ),
            streaks AS (                         -- 3. one row per streak
              SELECT user_id,
                     MIN(login_date) AS streak_start,
                     MAX(login_date) AS streak_end,
                     COUNT(*)        AS streak_days
              FROM islands
              GROUP BY user_id, grp
            ),
            ranked AS (                          -- 4. longest streak per user, earliest on ties
              SELECT s.*,
                     ROW_NUMBER() OVER (PARTITION BY user_id
                                        ORDER BY streak_days DESC, streak_start) AS rn
              FROM streaks s
            )
            SELECT user_id, streak_start, streak_end, streak_days
            FROM ranked
            WHERE rn = 1
            ORDER BY user_id;
        """,
        lang="sql",
        output=r"""
             user_id | streak_start | streak_end | streak_days
            ---------+--------------+------------+-------------
                   1 | 2026-10-01   | 2026-10-03 |           3
                   2 | 2026-10-04   | 2026-10-07 |           4
                   3 | 2026-10-03   | 2026-10-03 |           1
        """,
        extra=[dict(lang="text", label_en="Intermediate step for user 1: the grp key", label_bn="User 1-এর মাঝের ধাপ: grp key", src=r"""
             user_id | login_date |    grp
            ---------+------------+------------
                   1 | 2026-10-01 | 2026-09-30     (Oct 1 - 1 day)
                   1 | 2026-10-02 | 2026-09-30     (Oct 2 - 2 days)
                   1 | 2026-10-03 | 2026-09-30     (Oct 3 - 3 days)
                   1 | 2026-10-05 | 2026-10-01     (Oct 5 - 4 days)  <- gap: new island
                   1 | 2026-10-06 | 2026-10-01     (Oct 6 - 5 days)
        """)],
        a_en=r"""
            This is the classic **gaps-and-islands** pattern (advanced material).
            1. `DISTINCT` removes duplicate logins on the same day (user 1 logged in twice on Oct 2) — otherwise row numbers would break streaks.
            2. Within one user, number the days 1, 2, 3... in date order. For consecutive days, the date and the row number both increase by 1, so **`date − row_number` stays constant**. When a day is skipped, the date jumps by 2 while the row number jumps by 1, so the difference changes. That difference (`grp`) labels each island (see the intermediate table: Oct 1–3 → Sep 30, Oct 5–6 → Oct 1).
            3. `GROUP BY user_id, grp` collapses each island into one streak with its start, end, and length.
            4. `ROW_NUMBER()` ordered by `streak_days DESC, streak_start` picks the longest streak, earliest first on ties.

            Result: user 1's best streak is Oct 1–3 (3 days), user 2's is Oct 4–7 (4 days), user 3 has a single day.
        """,
        a_bn=r"""
            এটা classic **gaps-and-islands** pattern (advanced বিষয়)।
            1. `DISTINCT` একই দিনের duplicate login বাদ দেয় (user 1 Oct 2-এ দুবার login করেছে) — নাহলে row number streak ভেঙে দিত।
            2. প্রতিটা user-এর ভেতরে দিনগুলোকে তারিখের ক্রমে 1, 2, 3... নম্বর দাও। টানা দিনে date আর row number দুটোই ১ করে বাড়ে, তাই **`date − row_number` একই থাকে**। কোনো দিন বাদ গেলে date ২ লাফায় কিন্তু row number ১, তাই পার্থক্যটা বদলে যায়। ওই পার্থক্য (`grp`) প্রতিটা island-কে চিহ্নিত করে (মাঝের table দেখো: Oct 1–3 → Sep 30, Oct 5–6 → Oct 1)।
            3. `GROUP BY user_id, grp` প্রতিটা island-কে শুরু, শেষ আর দৈর্ঘ্য-সহ একটা streak-এ পরিণত করে।
            4. `streak_days DESC, streak_start` দিয়ে সাজানো `ROW_NUMBER()` সবচেয়ে লম্বা streak বাছে, tie হলে আগেরটা।

            ফলাফল: user 1-এর সেরা streak Oct 1–3 (৩ দিন), user 2-এর Oct 4–7 (৪ দিন), user 3-এর একটাই দিন।
        """,
        ex_en=r"""
            - **Date arithmetic is dialect-specific:** PostgreSQL `date - integer` returns a date (used here). MySQL: `DATE_SUB(login_date, INTERVAL rn DAY)`; SQL Server: `DATEADD(day, -rn, login_date)`; SQLite: `date(login_date, '-' || rn || ' days')`. The window-function logic is identical everywhere.
            - **Alternative (LAG-based):** flag a new island when `login_date <> LAG(login_date) + 1 day`, then build island ids with a running `SUM(flag) OVER (...)`. It's longer but adapts to rules like "a gap of up to 1 day doesn't break the streak".
            - **Timestamps & time zones:** if logins are `timestamptz`, convert to the business time zone *before* taking the date (`(login_at AT TIME ZONE 'Asia/Dhaka')::date`), or streaks break at UTC midnight instead of Dhaka midnight.
            - **Same pattern elsewhere:** consecutive seat numbers, uninterrupted service uptime, sessionization (gap > 30 minutes = new session), finding missing invoice numbers (the gaps).
            - **Performance:** an index on `(user_id, login_date)` lets the window functions read rows in order without a big sort.
        """,
        ex_bn=r"""
            - **Date arithmetic dialect-নির্ভর:** PostgreSQL-এ `date - integer` একটা date দেয় (এখানে এটাই ব্যবহার হয়েছে)। MySQL: `DATE_SUB(login_date, INTERVAL rn DAY)`; SQL Server: `DATEADD(day, -rn, login_date)`; SQLite: `date(login_date, '-' || rn || ' days')`। Window function-এর logic সব জায়গায় একই।
            - **বিকল্প (LAG-ভিত্তিক):** `login_date <> LAG(login_date) + 1 দিন` হলে নতুন island-এর flag দাও, তারপর running `SUM(flag) OVER (...)` দিয়ে island id বানাও। এটা লম্বা, কিন্তু "১ দিন পর্যন্ত ফাঁক streak ভাঙবে না"-এর মতো নিয়মে মানিয়ে নেওয়া যায়।
            - **Timestamp আর time zone:** login যদি `timestamptz` হয়, date নেওয়ার *আগে* business time zone-এ রূপান্তর করো (`(login_at AT TIME ZONE 'Asia/Dhaka')::date`), নাহলে streak ঢাকার মধ্যরাতের বদলে UTC মধ্যরাতে ভাঙবে।
            - **অন্য জায়গায় একই pattern:** পরপর seat number, নিরবচ্ছিন্ন service uptime, sessionization (৩০ মিনিটের বেশি ফাঁক = নতুন session), হারিয়ে যাওয়া invoice number খোঁজা (ফাঁকগুলো)।
            - **Performance:** `(user_id, login_date)`-এ index থাকলে window function বড় sort ছাড়াই ক্রম অনুযায়ী row পড়তে পারে।
        """,
        tip_en=r"""Explain the "date minus row number is constant" insight with two or three rows on the whiteboard before writing SQL — once the interviewer sees the invariant, the rest is routine. Mention de-duplication and time zones as the real-world traps.""",
        tip_bn=r"""SQL লেখার আগে whiteboard-এ দুই-তিনটা row দিয়ে "date বিয়োগ row number একই থাকে" ধারণাটা বোঝাও — interviewer invariant-টা দেখে ফেললে বাকিটা সাধারণ কাজ। বাস্তবের ফাঁদ হিসেবে de-duplication আর time zone-এর কথা বলো।""",
        mist_en=r"""Forgetting `DISTINCT` (duplicate logins split streaks), using `RANK()` instead of `ROW_NUMBER()` for the per-user pick (returns several rows on ties), or ignoring time zones when converting timestamps to dates.""",
        mist_bn=r"""`DISTINCT` ভুলে যাওয়া (duplicate login streak ভেঙে দেয়), প্রতি user-এর জন্য বাছাইয়ে `ROW_NUMBER()`-এর বদলে `RANK()` ব্যবহার করা (tie হলে একাধিক row আসে), অথবা timestamp থেকে date বানানোর সময় time zone উপেক্ষা করা।""",
        follow=[
            ("Find users who are currently on a streak of at least 3 days (ending today).", "যেসব user এই মুহূর্তে অন্তত ৩ দিনের streak-এ আছে (আজকে শেষ হওয়া), তাদের বের করো।"),
            ("How would you find gaps in a sequence of invoice numbers?", "Invoice number-এর ক্রমে ফাঁকগুলো কীভাবে খুঁজবে?"),
        ],
        related=["sql-024", "sql-013"],
        refs=[PG_WINDOW_TUT, PG_DATETIME_OPS],
    ),
    # ------------------------------------------------------------------ sql-031
    Q(
        id="sql-031", sub="Query Optimization at Scale", diff="extreme", type="scenario",
        prio="high", market="international", mins=18,
        tags=["query-optimization", "pre-aggregation", "read-replica", "partitioning", "reporting"],
        ver="Version-independent concepts; examples in PostgreSQL 18 syntax", vs=False, status="stable",
        q_en=r"""A "sales by category per day for the last 90 days" dashboard query joins `orders`, `order_items` (300 million rows), and `products`. It takes 45 seconds, and when several managers open the dashboard, checkout latency rises. How would you make the dashboard fast and stop it from hurting checkout?""",
        q_bn=r"""একটা "গত ৯০ দিনের প্রতিদিনের category-ভিত্তিক sales" dashboard query `orders`, `order_items` (৩০ কোটি row) আর `products` join করে। এটা ৪৫ সেকেন্ড নেয়, আর কয়েকজন manager একসাথে dashboard খুললে checkout-এর latency বেড়ে যায়। Dashboard কীভাবে দ্রুত করবে, আর checkout-এর ক্ষতি কীভাবে থামাবে?""",
        a_en=r"""
            This is advanced; I'd structure it as **clarify → measure → isolate → fix → scale**.

            **1. Clarify:** how fresh must the numbers be (real-time, 5 minutes, yesterday)? How many viewers? Do refunds/cancellations change past days?

            **2. Measure:** `EXPLAIN (ANALYZE, BUFFERS)` the query. Typical findings: a sequential scan of all 300M `order_items` because the date filter is on `orders` and not sargable, a huge hash join, sorts spilling to disk, `SELECT *` pulling unneeded columns.

            **3. Isolate immediately:** the dashboard is analytics, checkout is OLTP — they shouldn't compete. Route reporting to a **read replica**, give the reporting role a `statement_timeout`, and cache the dashboard response for a few minutes.

            **4. Fix the query:** filter `orders` by a sargable range on an indexed `created_at` first, join only the needed columns, aggregate before joining to `products` when possible; add a covering index on `order_items (order_id) INCLUDE (product_id, quantity, unit_price)` if lookups dominate.

            **5. Don't recompute history on every page view:** maintain a **summary table** `daily_category_sales (sales_date, category_id, revenue, units)`. A job every few minutes recomputes only the last 2–3 days (to catch late refunds) inside a transaction; the dashboard then reads ~90 × N small rows in milliseconds.

            **6. At larger scale:** partition `orders`/`order_items` by month for pruning and cheap archiving, and stream changes (CDC) to an OLAP/columnar warehouse (BigQuery, ClickHouse, Redshift) for ad-hoc analytics.
        """,
        a_bn=r"""
            এটা advanced বিষয়; আমি সাজাব এভাবে: **পরিষ্কার করা → মাপা → আলাদা করা → ঠিক করা → scale**।

            **1. পরিষ্কার করা:** সংখ্যা কতটা হালনাগাদ লাগবে (real-time, ৫ মিনিট, গতকাল)? কতজন দেখবে? Refund/cancellation কি অতীতের দিন বদলায়?

            **2. মাপা:** query-টার `EXPLAIN (ANALYZE, BUFFERS)` দেখো। সাধারণত যা পাওয়া যায়: ৩০ কোটি `order_items`-এর পুরো sequential scan, কারণ date filter `orders`-এ আর সেটা sargable নয়; বিশাল hash join; disk-এ spill করা sort; অপ্রয়োজনীয় column টেনে আনা `SELECT *`।

            **3. সাথে সাথে আলাদা করা:** dashboard হলো analytics, checkout হলো OLTP — এদের প্রতিযোগিতা করা উচিত না। Reporting **read replica**-তে পাঠাও, reporting role-কে `statement_timeout` দাও, আর dashboard-এর response কয়েক মিনিট cache করো।

            **4. Query ঠিক করা:** আগে indexed `created_at`-এর উপর sargable range দিয়ে `orders` filter করো, শুধু দরকারি column join করো, সম্ভব হলে `products`-এর সাথে join-এর আগে aggregate করো; lookup বেশি হলে `order_items (order_id) INCLUDE (product_id, quantity, unit_price)` covering index দাও।

            **5. প্রতিটা page view-এ ইতিহাস আবার হিসাব কোরো না:** একটা **summary table** `daily_category_sales (sales_date, category_id, revenue, units)` রাখো। প্রতি কয়েক মিনিটে একটা job transaction-এর ভেতরে শুধু শেষ ২–৩ দিন আবার হিসাব করে (দেরিতে আসা refund ধরতে); dashboard তখন millisecond-এ ~৯০ × N ছোট row পড়ে।

            **6. আরও বড় scale-এ:** pruning আর সস্তা archiving-এর জন্য `orders`/`order_items` মাস ধরে partition করো, আর ad-hoc analytics-এর জন্য পরিবর্তনগুলো (CDC) একটা OLAP/columnar warehouse-এ stream করো (BigQuery, ClickHouse, Redshift)।
        """,
        ex_en=r"""
            - **Why a summary table beats a materialized view here:** a full `REFRESH` recomputes 90+ days every time; the incremental job only touches recent days. Delete-and-reinsert the window in one transaction so categories whose sales dropped to zero don't keep stale rows.
            - **Correctness details:** compute the date in the business time zone (Asia/Dhaka), decide which order statuses count as revenue, and keep the logic in one place so the dashboard and finance reports agree.
            - **Replica caveats:** replicas lag, and long analytical queries on a standby can be cancelled or (with `hot_standby_feedback`) cause bloat on the primary — a separate analytics store avoids both.
            - **Memory:** a reporting session can use a larger `work_mem` (set per role) so big sorts/hashes don't spill — never raise it globally for all OLTP connections.
            - **Measure success:** p95 dashboard latency, checkout p95 during dashboard use, DB CPU, and data freshness lag.
        """,
        ex_bn=r"""
            - **এখানে summary table কেন materialized view-এর চেয়ে ভালো:** পুরো `REFRESH` প্রতিবার ৯০+ দিন আবার হিসাব করে; incremental job শুধু সাম্প্রতিক দিনগুলো ছোঁয়। একটা transaction-এ window-টা delete করে আবার insert করো, যাতে যেসব category-র sale শূন্যে নেমেছে তাদের পুরনো row থেকে না যায়।
            - **Correctness-এর খুঁটিনাটি:** তারিখ হিসাব করো business time zone-এ (Asia/Dhaka), কোন order status revenue ধরা হবে ঠিক করো, আর logic এক জায়গায় রাখো যাতে dashboard আর finance report মেলে।
            - **Replica-র সতর্কতা:** replica পিছিয়ে থাকে, আর standby-তে লম্বা analytical query cancel হতে পারে বা (`hot_standby_feedback` থাকলে) primary-তে bloat ঘটাতে পারে — আলাদা analytics store দুটোই এড়ায়।
            - **Memory:** reporting session বড় `work_mem` ব্যবহার করতে পারে (role অনুযায়ী set করো), যাতে বড় sort/hash disk-এ spill না করে — সব OLTP connection-এর জন্য globally কখনো বাড়িয়ো না।
            - **সাফল্য মাপো:** dashboard-এর p95 latency, dashboard চলাকালীন checkout-এর p95, DB CPU, আর data কতটা পিছিয়ে আছে।
        """,
        tip_en=r"""Start with the freshness question — it decides everything. Then separate "stop the harm now" (replica, timeout, cache) from "make it fast" (query + pre-aggregation) and "long term" (partitioning, warehouse). Concrete numbers (90 × N rows) make the design tangible.""",
        tip_bn=r"""হালনাগাদ থাকার প্রশ্ন দিয়ে শুরু করো — এটাই সবকিছু ঠিক করে দেয়। তারপর "এখনই ক্ষতি থামাও" (replica, timeout, cache), "দ্রুত করো" (query + pre-aggregation) আর "দীর্ঘমেয়াদি" (partitioning, warehouse) আলাদা করো। Concrete সংখ্যা (৯০ × N row) design-টাকে বাস্তব করে তোলে।""",
        mist_en=r"""Only adding indexes to the 300M-row table, raising `work_mem` globally, or running heavy analytics on the primary that serves checkout.""",
        mist_bn=r"""শুধু ৩০ কোটি row-এর table-এ index যোগ করা, globally `work_mem` বাড়ানো, অথবা checkout চালানো primary-তেই ভারী analytics চালানো।""",
        code=r"""
            CREATE TABLE daily_category_sales (
              sales_date  DATE          NOT NULL,
              category_id INT           NOT NULL,
              revenue     NUMERIC(14,2) NOT NULL,
              units       BIGINT        NOT NULL,
              PRIMARY KEY (sales_date, category_id)
            );

            -- every few minutes: recompute only the recent window (catches late refunds)
            START TRANSACTION;

            DELETE FROM daily_category_sales
            WHERE sales_date >= CURRENT_DATE - 2;

            INSERT INTO daily_category_sales (sales_date, category_id, revenue, units)
            SELECT CAST(o.created_at AS DATE),
                   p.category_id,
                   SUM(oi.quantity * oi.unit_price),
                   SUM(oi.quantity)
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.id
            JOIN products p     ON p.id = oi.product_id
            WHERE o.created_at >= CURRENT_DATE - 2      -- sargable, uses an index on orders(created_at)
              AND o.status = 'paid'
            GROUP BY CAST(o.created_at AS DATE), p.category_id;

            COMMIT;

            -- the dashboard now reads a few thousand small rows
            SELECT sales_date, category_id, revenue, units
            FROM daily_category_sales
            WHERE sales_date >= CURRENT_DATE - 90
            ORDER BY sales_date, category_id;
        """,
        lang="sql",
        follow=[
            ("How would you keep the summary table correct if an order from 10 days ago is refunded?", "১০ দিন আগের একটা order refund হলে summary table কীভাবে সঠিক রাখবে?"),
            ("When would you move this workload to a data warehouse instead?", "কখন এই workload একটা data warehouse-এ সরিয়ে নেবে?"),
        ],
        related=["sql-027", "sql-020", "sql-026"],
        refs=[PG_USING_EXPLAIN, PG_PARTITIONING, PG_MATVIEWS],
    ),
    # ------------------------------------------------------------------ sql-032
    Q(
        id="sql-032", sub="Schema Design: E-commerce Marketplace", diff="extreme", type="system-design",
        prio="high", market="international", mins=20,
        tags=["schema-design", "normalization", "constraints", "inventory", "e-commerce"],
        ver="ISO SQL (identity columns SQL:2003); tested on PostgreSQL 18", vs=False, status="stable",
        q_en=r"""Design the relational schema for a multi-vendor e-commerce marketplace (like Daraz): customers, vendors, products with variants (size/colour), inventory, orders containing items from several vendors, payments, and reviews. Explain your keys, constraints, normalization decisions, indexes, and how you'd prevent overselling during a flash sale.""",
        q_bn=r"""একটা multi-vendor e-commerce marketplace-এর (Daraz-এর মতো) relational schema design করো: customer, vendor, variant-সহ product (size/colour), inventory, একাধিক vendor-এর item-ওয়ালা order, payment আর review। তোমার key, constraint, normalization-এর সিদ্ধান্ত, index, আর flash sale-এর সময় overselling কীভাবে আটকাবে — ব্যাখ্যা করো।""",
        a_en=r"""
            Advanced design question — I'd start from entities and invariants, then performance.

            **Core entities and keys** (surrogate `BIGINT` identity keys, natural keys as `UNIQUE`):
            - `customers` (email/phone unique), `vendors`, `products` (belongs to a vendor and category), `product_variants` (the sellable SKU: size, colour, price, stock — `UNIQUE (sku)` and `UNIQUE (product_id, size, colour)`).
            - `orders` (customer, status, totals, shipping address) → `order_items` (order, variant, vendor, quantity, **unit_price snapshot**), composite PK `(order_id, variant_id)`.
            - `payments` (order, provider, `UNIQUE (provider, provider_txn_id)` so duplicate gateway callbacks are idempotent), `reviews` (PK `(customer_id, product_id)`, `CHECK (rating BETWEEN 1 AND 5)`).
            - Optional `shipments` grouping one vendor's items within an order, since each vendor ships separately.

            **Normalization decisions:** start in 3NF. Deliberate denormalizations: `unit_price` and the shipping address are copied into the order (historical facts, not redundancy — later price/address changes must not rewrite past orders); `orders.total` and a product's average rating are cached for reads, maintained in the same transaction or by a job.

            **Constraints:** FKs everywhere, `CHECK (quantity > 0)`, `CHECK (stock >= 0)`, `CHECK (price >= 0)`, status values restricted by `CHECK` or a lookup table, money as `NUMERIC(12,2)`, times as `TIMESTAMPTZ`.

            **Indexes:** every FK used in joins (`order_items(variant_id)`, `products(vendor_id)`), `orders (customer_id, created_at DESC)` for "my orders", a partial index for active products by category; product search goes to full-text search or a search engine, not `LIKE '%...%'`.

            **Overselling in a flash sale:** decrement stock with one atomic conditional statement inside the order transaction — `UPDATE product_variants SET stock = stock - :qty WHERE id = :id AND stock >= :qty`. If 0 rows change, the item is sold out; the `CHECK (stock >= 0)` is the safety net. For extremely hot SKUs, put a fast gate in front (a Redis counter or a queue that admits buyers in order) and keep the database as the source of truth, with short reservations that expire if payment doesn't complete.
        """,
        a_bn=r"""
            Advanced design প্রশ্ন — আমি entity আর invariant দিয়ে শুরু করব, তারপর performance।

            **মূল entity আর key** (surrogate `BIGINT` identity key, natural key-গুলো `UNIQUE`):
            - `customers` (email/phone unique), `vendors`, `products` (একজন vendor আর category-র অধীনে), `product_variants` (বিক্রয়যোগ্য SKU: size, colour, price, stock — `UNIQUE (sku)` আর `UNIQUE (product_id, size, colour)`)।
            - `orders` (customer, status, total, shipping address) → `order_items` (order, variant, vendor, quantity, **unit_price snapshot**), composite PK `(order_id, variant_id)`।
            - `payments` (order, provider, `UNIQUE (provider, provider_txn_id)` যাতে gateway-র duplicate callback idempotent হয়), `reviews` (PK `(customer_id, product_id)`, `CHECK (rating BETWEEN 1 AND 5)`)।
            - ঐচ্ছিক `shipments`, যা একটা order-এর ভেতরে একজন vendor-এর item-গুলো একসাথে রাখে, কারণ প্রতিটা vendor আলাদাভাবে ship করে।

            **Normalization-এর সিদ্ধান্ত:** 3NF থেকে শুরু। ইচ্ছাকৃত denormalization: `unit_price` আর shipping address order-এ কপি করা হয় (এগুলো ঐতিহাসিক তথ্য, redundancy নয় — পরে দাম/ঠিকানা বদলালে পুরনো order বদলানো যাবে না); `orders.total` আর product-এর গড় rating পড়ার সুবিধার জন্য cache করা, একই transaction-এ বা একটা job দিয়ে maintain করা।

            **Constraint:** সব জায়গায় FK, `CHECK (quantity > 0)`, `CHECK (stock >= 0)`, `CHECK (price >= 0)`, status value `CHECK` বা lookup table দিয়ে সীমিত, টাকা `NUMERIC(12,2)`-এ, সময় `TIMESTAMPTZ`-এ।

            **Index:** join-এ ব্যবহৃত প্রতিটা FK (`order_items(variant_id)`, `products(vendor_id)`), "আমার order"-এর জন্য `orders (customer_id, created_at DESC)`, category অনুযায়ী active product-এর জন্য partial index; product search যাবে full-text search বা search engine-এ, `LIKE '%...%'`-এ নয়।

            **Flash sale-এ overselling:** order transaction-এর ভেতরে একটা atomic conditional statement দিয়ে stock কমাও — `UPDATE product_variants SET stock = stock - :qty WHERE id = :id AND stock >= :qty`। ০টা row বদলালে item শেষ; `CHECK (stock >= 0)` হলো safety net। খুব hot SKU-র জন্য সামনে একটা দ্রুত gate বসাও (Redis counter বা ক্রমানুসারে buyer ঢোকানো একটা queue), আর database-কে source of truth রাখো — payment সম্পূর্ণ না হলে মেয়াদ শেষ হয়ে যায় এমন ছোট reservation-সহ।
        """,
        ex_en=r"""
            - **Why variants hold stock and price:** "Panjabi, size M, white" and "size L, blue" are different SKUs with different stock; putting stock on `products` can't represent that.
            - **Why `vendor_id` on `order_items`:** it's derivable through variant → product → vendor, but storing it makes vendor payouts, vendor dashboards, and per-vendor shipments simple and keeps the historical seller even if a product changes hands. Enforce consistency in the insert path.
            - **Order state machine:** model statuses explicitly (`pending_payment → paid → shipped → delivered`, or `cancelled`), keep an `order_status_history` table, and make payment webhooks idempotent.
            - **Scale later:** read replicas and caching for the catalogue; partition `orders`/`order_items` by month once they reach hundreds of millions of rows; archive old orders. Inventory reservations with expiry (`reserved_until`) prevent carts from locking stock forever.
            - **Bangladesh-specific realities:** cash-on-delivery orders (payment row created at delivery), mobile-wallet gateways (bKash/Nagad) with asynchronous callbacks, and BDT-only pricing to start — but keep a currency column if cross-border selling is on the roadmap.
        """,
        ex_bn=r"""
            - **Variant-এ কেন stock আর price:** "Panjabi, size M, সাদা" আর "size L, নীল" আলাদা SKU, আলাদা stock; `products`-এ stock রাখলে এটা দেখানো যায় না।
            - **`order_items`-এ কেন `vendor_id`:** এটা variant → product → vendor ধরে বের করা যায়, কিন্তু রেখে দিলে vendor payout, vendor dashboard আর vendor-ভিত্তিক shipment সহজ হয়, আর product অন্য কারো হাতে গেলেও ঐতিহাসিক seller থেকে যায়। Insert-এর পথে consistency enforce করো।
            - **Order state machine:** status স্পষ্টভাবে model করো (`pending_payment → paid → shipped → delivered`, বা `cancelled`), একটা `order_status_history` table রাখো, আর payment webhook idempotent করো।
            - **পরে scale:** catalogue-এর জন্য read replica আর caching; `orders`/`order_items` শত কোটি row-এ পৌঁছালে মাস ধরে partition; পুরনো order archive করা। মেয়াদসহ inventory reservation (`reserved_until`) cart-কে চিরকাল stock আটকে রাখতে দেয় না।
            - **বাংলাদেশের বাস্তবতা:** cash-on-delivery order (delivery-র সময় payment row তৈরি হয়), asynchronous callback-ওয়ালা mobile-wallet gateway (bKash/Nagad), আর শুরুতে শুধু BDT-তে দাম — তবে cross-border বিক্রির পরিকল্পনা থাকলে একটা currency column রেখে দাও।
        """,
        tip_en=r"""Draw the entities first, then walk through one order end to end (add to cart → reserve stock → pay → ship). Calling out the intentional denormalizations (price snapshot) and the atomic stock decrement shows you design for real failure modes.""",
        tip_bn=r"""আগে entity-গুলো এঁকে নাও, তারপর একটা order শুরু থেকে শেষ পর্যন্ত দেখাও (cart-এ যোগ → stock reserve → payment → ship)। ইচ্ছাকৃত denormalization (দামের snapshot) আর atomic stock decrement-এর কথা বললে বোঝা যায় তুমি বাস্তব failure mode মাথায় রেখে design করো।""",
        mist_en=r"""Reading the price from `products` when displaying old orders, storing stock on `products` instead of variants, or checking stock with a `SELECT` and decrementing it in a separate statement (race condition → overselling).""",
        mist_bn=r"""পুরনো order দেখানোর সময় `products` থেকে দাম পড়া, variant-এর বদলে `products`-এ stock রাখা, অথবা `SELECT` দিয়ে stock check করে আলাদা statement-এ কমানো (race condition → overselling)।""",
        code=r"""
            CREATE TABLE product_variants (
              id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              product_id  BIGINT NOT NULL REFERENCES products(id),
              sku         VARCHAR(64) NOT NULL UNIQUE,
              size        VARCHAR(10),
              color       VARCHAR(30),
              price       NUMERIC(12,2) NOT NULL CHECK (price >= 0),
              stock       INT NOT NULL CHECK (stock >= 0),
              UNIQUE (product_id, size, color)
            );

            CREATE TABLE orders (
              id               BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              customer_id      BIGINT NOT NULL REFERENCES customers(id),
              status           VARCHAR(20) NOT NULL
                               CHECK (status IN ('pending_payment', 'paid', 'shipped', 'delivered', 'cancelled')),
              shipping_address TEXT NOT NULL,                       -- snapshot at order time
              total            NUMERIC(12,2) NOT NULL CHECK (total >= 0),
              created_at       TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE order_items (
              order_id    BIGINT NOT NULL REFERENCES orders(id),
              variant_id  BIGINT NOT NULL REFERENCES product_variants(id),
              vendor_id   BIGINT NOT NULL REFERENCES vendors(id),
              quantity    INT NOT NULL CHECK (quantity > 0),
              unit_price  NUMERIC(12,2) NOT NULL,                   -- price charged, not today's price
              PRIMARY KEY (order_id, variant_id)
            );

            CREATE TABLE payments (
              id               BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              order_id         BIGINT NOT NULL REFERENCES orders(id),
              provider         VARCHAR(30)  NOT NULL,                -- 'bkash', 'nagad', 'card', 'cod'
              provider_txn_id  VARCHAR(100) NOT NULL,
              amount           NUMERIC(12,2) NOT NULL,
              status           VARCHAR(20)  NOT NULL,
              UNIQUE (provider, provider_txn_id)                     -- idempotent webhooks
            );

            CREATE INDEX ON orders (customer_id, created_at DESC);
            CREATE INDEX ON order_items (variant_id);
            CREATE INDEX ON order_items (vendor_id);

            -- flash sale: atomic, race-free stock decrement (inside the order transaction)
            UPDATE product_variants
               SET stock = stock - 2
             WHERE id = 1 AND stock >= 2;      -- 0 rows updated => sold out, roll back the order
        """,
        lang="sql",
        follow=[
            ("How would you implement cart reservations that expire after 10 minutes?", "১০ মিনিট পর মেয়াদ শেষ হয় এমন cart reservation কীভাবে implement করবে?"),
            ("A product's name changes after it was ordered — what should old invoices show, and how does your schema support that?", "Order-এর পরে একটা product-এর নাম বদলে গেল — পুরনো invoice-এ কী দেখাবে, আর তোমার schema এটা কীভাবে support করে?"),
            ("How would you split one customer order into per-vendor shipments?", "একটা customer order-কে vendor-ভিত্তিক shipment-এ কীভাবে ভাগ করবে?"),
        ],
        related=["sql-011", "sql-007", "sql-010"],
        refs=[PG_CONSTRAINTS, PG_INDEXES],
    ),
]

if __name__ == "__main__":
    save("sql", "b4", QUESTIONS)
