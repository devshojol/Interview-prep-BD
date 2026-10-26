# SQL batch 3 — sql-017 … sql-024
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_AGG = ("PostgreSQL docs — Aggregate Functions", "https://www.postgresql.org/docs/current/functions-aggregate.html")
PG_DELETE = ("PostgreSQL docs — DELETE", "https://www.postgresql.org/docs/current/sql-delete.html")
PG_AGG_EXPR = ("PostgreSQL docs — Aggregate Expressions (FILTER)", "https://www.postgresql.org/docs/current/sql-expressions.html")
PG_CONDITIONAL = ("PostgreSQL docs — Conditional Expressions (CASE)", "https://www.postgresql.org/docs/current/functions-conditional.html")
PG_JOIN_TUT = ("PostgreSQL docs — Joins Between Tables", "https://www.postgresql.org/docs/current/tutorial-join.html")
PG_TABLE_EXPR = ("PostgreSQL docs — Table Expressions", "https://www.postgresql.org/docs/current/queries-table-expressions.html")
PG_INDEXES_MULTI = ("PostgreSQL docs — Multicolumn Indexes", "https://www.postgresql.org/docs/current/indexes-multicolumn.html")
PG_INDEXES_EXPR = ("PostgreSQL docs — Indexes on Expressions", "https://www.postgresql.org/docs/current/indexes-expressional.html")
PG_USING_EXPLAIN = ("PostgreSQL docs — Using EXPLAIN", "https://www.postgresql.org/docs/current/using-explain.html")
OWASP_SQLI = ("OWASP — SQL Injection Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html")
OWASP_PARAMS = ("OWASP — Query Parameterization Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html")
NODE_PG = ("node-postgres (pg) — GitHub", "https://github.com/brianc/node-postgres")
PG_UPDATE = ("PostgreSQL docs — UPDATE", "https://www.postgresql.org/docs/current/sql-update.html")
PG_INSERT = ("PostgreSQL docs — INSERT", "https://www.postgresql.org/docs/current/sql-insert.html")
PG_WITH = ("PostgreSQL docs — WITH Queries (recursive CTEs)", "https://www.postgresql.org/docs/current/queries-with.html")
SQLITE_WITH = ("SQLite — WITH clause (recursive CTEs)", "https://www.sqlite.org/lang_with.html")
PG_WINDOW_FUNCS = ("PostgreSQL docs — Window Functions (LAG, LEAD)", "https://www.postgresql.org/docs/current/functions-window.html")
PG_FORMATTING = ("PostgreSQL docs — Data Type Formatting Functions (to_char)", "https://www.postgresql.org/docs/current/functions-formatting.html")

QUESTIONS = [
    # ------------------------------------------------------------------ sql-017
    Q(
        id="sql-017", sub="Finding & Deleting Duplicates", diff="medium", type="query",
        prio="high", market="both", mins=6,
        tags=["duplicates", "group-by", "having", "delete", "data-cleaning"],
        ver="Version-independent (ISO SQL; output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""The `users` table has duplicate accounts whose emails differ only in letter case. (1) Find each duplicated email (case-insensitive), how many copies exist, and which `id` to keep (the oldest, i.e. the lowest id). (2) Then delete the extra copies.""",
        q_bn=r"""`users` table-এ কিছু duplicate account আছে, যাদের email শুধু বড়-ছোট হাতের অক্ষরে আলাদা। (1) প্রতিটা duplicate email (case-insensitive), তার কয়টা copy আছে আর কোন `id` রাখতে হবে (সবচেয়ে পুরনো, মানে সবচেয়ে ছোট id) — বের করো। (2) তারপর বাড়তি copy-গুলো delete করো।""",
        setup=r"""
            CREATE TABLE users (
              id    INT PRIMARY KEY,
              email VARCHAR(255) NOT NULL,
              name  VARCHAR(50) NOT NULL
            );

            INSERT INTO users (id, email, name) VALUES
              (1, 'rahim@example.com', 'Rahim'),
              (2, 'karim@example.com', 'Karim'),
              (3, 'Rahim@Example.com', 'Rahim U.'),
              (4, 'nadia@example.com', 'Nadia'),
              (5, 'karim@example.com', 'Karim A.'),
              (6, 'sumi@example.com',  'Sumi');
        """,
        code=r"""
            SELECT LOWER(email) AS email,
                   COUNT(*)     AS copies,
                   MIN(id)      AS keep_id
            FROM users
            GROUP BY LOWER(email)
            HAVING COUNT(*) > 1
            ORDER BY email;
        """,
        lang="sql",
        output=r"""
                   email       | copies | keep_id
            -------------------+--------+---------
             karim@example.com |      2 |       2
             rahim@example.com |      2 |       1
        """,
        extra=[dict(lang="sql", label_en="Step 2: delete the extra copies (portable), then prevent new duplicates",
                    label_bn="ধাপ ২: বাড়তি copy delete (portable), তারপর নতুন duplicate আটকানো", src=r"""
            -- keep the lowest id per normalised email; the extra derived table also keeps MySQL happy
            DELETE FROM users
            WHERE id NOT IN (
              SELECT keep_id FROM (
                SELECT MIN(id) AS keep_id FROM users GROUP BY LOWER(email)
              ) AS keepers
            );

            SELECT id, email, name FROM users ORDER BY id;
            --  id |       email       | name
            -- ----+-------------------+-------
            --   1 | rahim@example.com | Rahim
            --   2 | karim@example.com | Karim
            --   4 | nadia@example.com | Nadia
            --   6 | sumi@example.com  | Sumi

            -- window-function alternative: rows with rn > 1 are the duplicates
            -- SELECT id FROM (SELECT id, ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY id) AS rn FROM users) t WHERE rn > 1;

            -- prevent it from happening again (expression index; MySQL 8.0.13+ writes ((LOWER(email))))
            CREATE UNIQUE INDEX users_email_lower_uq ON users (LOWER(email));
        """)],
        a_en=r"""
            - `GROUP BY LOWER(email)` puts `rahim@example.com` and `Rahim@Example.com` in the same group.
            - `HAVING COUNT(*) > 1` keeps only groups with duplicates (a condition on an aggregate, so it must be `HAVING`).
            - `MIN(id)` picks the row to keep — the oldest account.
            - For deletion, I delete every row whose id is **not** one of the keepers. `NOT IN` is safe here because `MIN(id)` from a `NOT NULL` primary key can't be NULL.

            Before running the `DELETE` on real data, I'd run it as a `SELECT` first, do it in a transaction, and make sure related rows (orders, sessions) are re-pointed to the kept account — otherwise foreign keys will block the delete or cascade away real data.
        """,
        a_bn=r"""
            - `GROUP BY LOWER(email)` `rahim@example.com` আর `Rahim@Example.com`-কে একই group-এ রাখে।
            - `HAVING COUNT(*) > 1` শুধু duplicate-ওয়ালা group রাখে (aggregate-এর উপর condition, তাই `HAVING`-এই দিতে হবে)।
            - `MIN(id)` কোন row রাখা হবে সেটা বাছে — সবচেয়ে পুরনো account।
            - Delete-এর জন্য আমি সেসব row মুছি যাদের id keeper-দের মধ্যে **নেই**। এখানে `NOT IN` নিরাপদ, কারণ `NOT NULL` primary key থেকে নেওয়া `MIN(id)` কখনো NULL হতে পারে না।

            আসল data-য় `DELETE` চালানোর আগে আমি প্রথমে এটাকে `SELECT` হিসেবে চালাই, transaction-এর ভেতরে করি, আর নিশ্চিত হই যে সম্পর্কিত row (order, session) রাখা account-এর দিকে সরানো হয়েছে — না হলে foreign key delete আটকে দেবে, বা cascade করে আসল data মুছে ফেলবে।
        """,
        quick_en=r"""`GROUP BY LOWER(email) HAVING COUNT(*) > 1` finds the duplicates, and `MIN(id)` picks the oldest row to keep. Then delete every row whose id isn't a keeper, after running it as a `SELECT` first, inside a transaction, with related rows re-pointed.""",
        quick_bn=r"""`GROUP BY LOWER(email) HAVING COUNT(*) > 1` duplicate খুঁজে বের করে, আর `MIN(id)` রাখার জন্য সবচেয়ে পুরোনো row বাছে। তারপর যেসব row-এর id keeper নয় সেগুলো delete করো, তবে আগে `SELECT` হিসেবে চালিয়ে দেখো, transaction-এর ভেতরে করো, আর related row-গুলো রাখা account-এ সরিয়ে নাও।""",
        ex_en=r"""
            - **Decide what "duplicate" means** with the business first: case-insensitive email? Trimmed whitespace? Same phone number? Gmail dots? The normalisation expression in `GROUP BY` encodes that decision.
            - **Window-function version:** `ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY id)` marks the first row 1 and duplicates 2, 3...; delete rows with `rn > 1`. It's handy when you want to keep "the newest" or "the most complete" row instead.
            - **Database quirks:** MySQL refuses `DELETE ... WHERE id IN (SELECT ... FROM users)` on the same table (error 1093) — wrapping the subquery in a derived table, as above, works around it. PostgreSQL also offers `DELETE ... USING` for self-join deletes.
            - **Root cause:** add a `UNIQUE` index on the normalised value so the application can't create duplicates again, even under concurrent sign-ups.
        """,
        ex_bn=r"""
            - **"Duplicate" মানে কী, আগে business-এর সাথে ঠিক করো:** case-insensitive email? সামনে-পেছনে ফাঁকা জায়গা বাদ? একই phone number? Gmail-এর dot? `GROUP BY`-এর normalisation expression সেই সিদ্ধান্তটাই ধারণ করে।
            - **Window-function version:** `ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY id)` প্রথম row-কে 1 আর duplicate-দের 2, 3... দেয়; `rn > 1` row-গুলো delete করো। "সবচেয়ে নতুন" বা "সবচেয়ে সম্পূর্ণ" row রাখতে চাইলে এটা কাজে লাগে।
            - **Database-এর খুঁটিনাটি:** MySQL একই table-এ `DELETE ... WHERE id IN (SELECT ... FROM users)` মানে না (error 1093) — উপরের মতো subquery-টা derived table-এ মুড়ে দিলে সমস্যা মেটে। PostgreSQL-এ self-join delete-এর জন্য `DELETE ... USING`-ও আছে।
            - **মূল কারণ:** normalised value-এর উপর `UNIQUE` index দাও, যাতে একসাথে অনেক sign-up হলেও application আর duplicate তৈরি করতে না পারে।
        """,
        tip_en=r"""Split it into "find" and "delete", and say you'd preview the delete with a `SELECT` inside a transaction. Ending with the unique index shows you fix root causes, not just symptoms.""",
        tip_bn=r""""খোঁজা" আর "মোছা" — দুই ভাগে ভাগ করো, আর বলো যে transaction-এর ভেতরে `SELECT` দিয়ে আগে delete-এর preview দেখবে। শেষে unique index-এর কথা বললে বোঝা যায় তুমি শুধু লক্ষণ নয়, মূল কারণ ঠিক করো।""",
        mist_en=r"""Grouping by the raw `email` (misses case variants), deleting without a transaction or preview, or deleting duplicates that still own orders.""",
        mist_bn=r"""কাঁচা `email` দিয়ে group করা (case-এর ভিন্নতা ধরা পড়ে না), transaction বা preview ছাড়া delete করা, অথবা এমন duplicate মুছে ফেলা যাদের নামে এখনো order আছে।""",
        follow=[
            ("Keep the most recently active account instead of the oldest — how does the query change?", "সবচেয়ে পুরনোর বদলে সবচেয়ে সম্প্রতি সক্রিয় account রাখতে চাইলে query কীভাবে বদলাবে?"),
            ("How would you merge the duplicates' orders into the kept account first?", "আগে duplicate-দের order-গুলো রাখা account-এ কীভাবে merge করবে?"),
        ],
        related=["sql-009", "sql-007"],
        refs=[PG_AGG, PG_DELETE],
    ),
    # ------------------------------------------------------------------ sql-018
    Q(
        id="sql-018", sub="Pivoting with CASE & FILTER", diff="medium", type="query",
        prio="medium", market="both", mins=5,
        tags=["pivot", "case", "filter", "conditional-aggregation", "reporting"],
        ver="ISO SQL (CASE); FILTER clause: PostgreSQL 9.4+, SQLite 3.30+", vs=False, status="stable",
        q_en=r"""Turn the monthly sales rows into a report with **one row per category and one column per month** (July, August, September), plus a total column. Months with no sales should show 0.""",
        q_bn=r"""মাসিক sales-এর row-গুলোকে এমন একটা report-এ রূপান্তর করো যেখানে **প্রতি category-র জন্য একটা row আর প্রতি মাসের জন্য একটা column** (July, August, September) থাকবে, সাথে একটা total column। যে মাসে sale নেই সেখানে 0 দেখাবে।""",
        setup=r"""
            CREATE TABLE sales (
              id         INT PRIMARY KEY,
              category   VARCHAR(30) NOT NULL,
              sale_month CHAR(7) NOT NULL,      -- 'YYYY-MM'
              amount     INT NOT NULL
            );

            INSERT INTO sales (id, category, sale_month, amount) VALUES
              (1, 'Electronics', '2026-07', 1200),
              (2, 'Electronics', '2026-08',  800),
              (3, 'Fashion',     '2026-07',  300),
              (4, 'Fashion',     '2026-08',  450),
              (5, 'Fashion',     '2026-09',  500),
              (6, 'Grocery',     '2026-09',  220),
              (7, 'Electronics', '2026-09', 1500),
              (8, 'Grocery',     '2026-07',  180);
        """,
        code=r"""
            SELECT category,
                   SUM(CASE WHEN sale_month = '2026-07' THEN amount ELSE 0 END) AS jul,
                   SUM(CASE WHEN sale_month = '2026-08' THEN amount ELSE 0 END) AS aug,
                   SUM(CASE WHEN sale_month = '2026-09' THEN amount ELSE 0 END) AS sep,
                   SUM(amount)                                                  AS total
            FROM sales
            GROUP BY category
            ORDER BY category;
        """,
        lang="sql",
        output=r"""
              category   | jul  | aug | sep  | total
            -------------+------+-----+------+-------
             Electronics | 1200 | 800 | 1500 |  3500
             Fashion     |  300 | 450 |  500 |  1250
             Grocery     |  180 |   0 |  220 |   400
        """,
        extra=[dict(lang="sql", label_en="PostgreSQL FILTER syntax (note the NULL for Grocery in August)",
                    label_bn="PostgreSQL-এর FILTER syntax (August-এ Grocery-র NULL খেয়াল করো)", src=r"""
            SELECT category,
                   SUM(amount) FILTER (WHERE sale_month = '2026-07') AS jul,
                   SUM(amount) FILTER (WHERE sale_month = '2026-08') AS aug,
                   SUM(amount) FILTER (WHERE sale_month = '2026-09') AS sep
            FROM sales
            GROUP BY category
            ORDER BY category;

            --   category   | jul  | aug | sep
            -- -------------+------+-----+------
            --  Electronics | 1200 | 800 | 1500
            --  Fashion     |  300 | 450 |  500
            --  Grocery     |  180 |     |  220      <- NULL: wrap in COALESCE(..., 0)
        """)],
        a_en=r"""
            This is **conditional aggregation**. `GROUP BY category` makes one output row per category; each month column is a `SUM` over only the rows matching that month — the `CASE` turns other months' amounts into 0. Grocery has no August sales, so its `aug` is 0 + 0 = 0.

            The `FILTER (WHERE ...)` clause (standard SQL, supported by PostgreSQL and SQLite) expresses the same thing more readably. The subtle difference: if no rows match, `SUM ... FILTER` returns **NULL**, while `SUM(CASE ... ELSE 0 END)` returns 0. Use `COALESCE(..., 0)` with `FILTER` when the report needs zeros.
        """,
        a_bn=r"""
            এটা হলো **conditional aggregation**। `GROUP BY category` প্রতি category-র জন্য একটা output row বানায়; প্রতিটা মাসের column হলো শুধু সেই মাসের row-গুলোর `SUM` — `CASE` অন্য মাসের amount-কে 0 বানিয়ে দেয়। Grocery-র August-এ কোনো sale নেই, তাই এর `aug` হয় 0 + 0 = 0।

            `FILTER (WHERE ...)` clause (standard SQL, PostgreSQL আর SQLite support করে) একই কাজ আরও পড়ার মতো করে লেখে। সূক্ষ্ম পার্থক্য: কোনো row match না করলে `SUM ... FILTER` **NULL** দেয়, আর `SUM(CASE ... ELSE 0 END)` দেয় 0। Report-এ শূন্য লাগলে `FILTER`-এর সাথে `COALESCE(..., 0)` ব্যবহার করো।
        """,
        quick_en=r"""Conditional aggregation: `GROUP BY category` with one `SUM(CASE WHEN month = ... THEN amount ELSE 0 END)` per month. `SUM(...) FILTER (WHERE ...)` reads better, but returns NULL instead of 0 when no rows match, so wrap it in `COALESCE`.""",
        quick_bn=r"""Conditional aggregation: `GROUP BY category`, আর প্রতিটা মাসের জন্য একটা করে `SUM(CASE WHEN month = ... THEN amount ELSE 0 END)`। `SUM(...) FILTER (WHERE ...)` পড়তে সহজ, কিন্তু কোনো row না মিললে 0-এর বদলে NULL দেয়, তাই `COALESCE` দিয়ে মুড়ে দাও।""",
        ex_en=r"""
            - **Portability:** `SUM(CASE ...)` works everywhere (MySQL, SQL Server, Oracle, PostgreSQL, SQLite). `FILTER` is PostgreSQL/SQLite; SQL Server and Oracle also have a `PIVOT` operator, and PostgreSQL's `tablefunc` extension offers `crosstab()`.
            - **Dynamic columns:** SQL needs the output columns known when the query is written. If months change every time, either build the SQL dynamically (carefully — never from raw user input) or return long-format rows and pivot in the application/BI tool.
            - The same trick counts things conditionally: `COUNT(*) FILTER (WHERE status = 'cancelled')` or `SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)`.
            - With real dates, group by a month expression (`date_trunc('month', ordered_at)` in PostgreSQL) instead of storing a `'YYYY-MM'` string.
        """,
        ex_bn=r"""
            - **Portability:** `SUM(CASE ...)` সব জায়গায় চলে (MySQL, SQL Server, Oracle, PostgreSQL, SQLite)। `FILTER` হলো PostgreSQL/SQLite-এর; SQL Server আর Oracle-এ `PIVOT` operator-ও আছে, আর PostgreSQL-এর `tablefunc` extension `crosstab()` দেয়।
            - **Dynamic column:** query লেখার সময়ই SQL-কে output column জানতে হয়। মাস যদি প্রতিবার বদলায়, তাহলে হয় SQL dynamically বানাও (সাবধানে — কখনো কাঁচা user input থেকে নয়), নয়তো long-format row return করে application/BI tool-এ pivot করো।
            - একই কৌশলে শর্তসাপেক্ষে গোনাও যায়: `COUNT(*) FILTER (WHERE status = 'cancelled')` বা `SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)`।
            - আসল date থাকলে `'YYYY-MM'` string রাখার বদলে একটা month expression দিয়ে group করো (PostgreSQL-এ `date_trunc('month', ordered_at)`)।
        """,
        tip_en=r"""Call it "conditional aggregation" by name, show the portable `CASE` version first, then mention `FILTER` and the NULL-vs-0 difference. Raising the dynamic-columns limitation shows real reporting experience.""",
        tip_bn=r"""নাম ধরে বলো "conditional aggregation", আগে portable `CASE` version দেখাও, তারপর `FILTER` আর NULL বনাম 0-এর পার্থক্য বলো। Dynamic column-এর সীমাবদ্ধতা তুললে বোঝা যায় তোমার সত্যিকারের reporting অভিজ্ঞতা আছে।""",
        mist_en=r"""Counting matches with `COUNT(CASE WHEN ... THEN 1 ELSE 0 END)` — it counts every row, because 0 is not NULL (use `SUM`, or drop the `ELSE`) — or also grouping by `sale_month`, which undoes the pivot.""",
        mist_bn=r"""Match গুনতে `COUNT(CASE WHEN ... THEN 1 ELSE 0 END)` ব্যবহার করা — এটা প্রতিটা row গোনে, কারণ 0 তো NULL নয় (`SUM` ব্যবহার করো, বা `ELSE` বাদ দাও) — অথবা `sale_month` দিয়েও group করা, যাতে pivot-টাই নষ্ট হয়ে যায়।""",
        follow=[
            ("Add a column showing each category's share of September revenue as a percentage.", "September-এর revenue-তে প্রতিটা category-র অংশ শতাংশে দেখানোর একটা column যোগ করো।"),
            ("How would you handle a report where the months are chosen by the user?", "যে report-এ মাসগুলো user বেছে নেয়, সেটা কীভাবে সামলাবে?"),
        ],
        related=["sql-004", "sql-024"],
        refs=[PG_CONDITIONAL, PG_AGG_EXPR],
    ),
    # ------------------------------------------------------------------ sql-019
    Q(
        id="sql-019", sub="JOIN Row Counts", diff="medium", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["left-join", "row-count", "joins", "output"],
        ver="Version-independent (ISO SQL)", vs=False, status="stable",
        q_en=r"""How many rows does the `LEFT JOIN` query return?""",
        q_bn=r"""`LEFT JOIN` query-টা কতগুলো row return করবে?""",
        code=r"""
            CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(50) NOT NULL);
            CREATE TABLE orders    (id INT PRIMARY KEY, customer_id INT);

            INSERT INTO customers (id, name) VALUES (1, 'Rahim'), (2, 'Karim'), (3, 'Nadia');
            INSERT INTO orders (id, customer_id) VALUES (10, 1), (11, 1), (12, 2), (13, NULL);

            SELECT c.name, o.id AS order_id
            FROM customers c
            LEFT JOIN orders o ON o.customer_id = c.id;
        """,
        lang="sql",
        output=r"""
             name  | order_id
            -------+----------
             Rahim |       10
             Rahim |       11
             Karim |       12
             Nadia |
        """,
        options=[("3", "3"), ("4", "4"), ("5", "5"), ("12", "12")],
        correct=1,
        a_en=r"""**4.** Rahim matches two orders (2 rows), Karim matches one (1 row), and Nadia has no orders, so the LEFT JOIN keeps her once with a NULL `order_id` (1 row). Order 13 has no customer and isn't returned, because a LEFT JOIN keeps unmatched rows from the **left** table only.""",
        a_bn=r"""**4।** Rahim দুটো order-এর সাথে মেলে (২ row), Karim একটার সাথে (১ row), আর Nadia-র কোনো order নেই, তাই LEFT JOIN তাকে NULL `order_id`-সহ একবার রাখে (১ row)। Order 13-এর কোনো customer নেই, তাই আসে না, কারণ LEFT JOIN শুধু **বাম** table-এর unmatched row রাখে।""",
        quick_en=r"""4 rows. Rahim matches two orders, Karim one, and Nadia has none, so LEFT JOIN keeps her once with a NULL `order_id`; the order with no customer is dropped because only unmatched left rows are kept.""",
        quick_bn=r"""4টা row। Rahim দুটো order-এর সাথে মেলে, Karim একটার সাথে, আর Nadia-র কোনো order নেই, তাই LEFT JOIN তাকে NULL `order_id`-সহ একবার রাখে; customer ছাড়া order-টা বাদ যায়, কারণ শুধু বাঁ দিকের না-মেলা row রাখা হয়।""",
        ex_en=r"""
            - **3** is the tempting answer ("one row per customer"), but a join produces one row per matching *pair*, so customers with several orders repeat.
            - **5** would be a `FULL OUTER JOIN` (adds the orphan order 13 with a NULL name).
            - **12** is the `CROSS JOIN` count (3 × 4).
            - An INNER JOIN would return 3 rows (Rahim ×2, Karim ×1).

            Practical consequence: if you `SUM(c.credit_limit)` after joining to orders, Rahim's limit is counted twice. Aggregate the many-side first (in a subquery/CTE), then join.
        """,
        ex_bn=r"""
            - **3** লোভনীয় উত্তর ("প্রতি customer-এ একটা row"), কিন্তু join প্রতিটা matching *জোড়ার* জন্য একটা row দেয়, তাই একাধিক order-ওয়ালা customer বারবার আসে।
            - **5** হতো `FULL OUTER JOIN` হলে (অনাথ order 13 NULL নাম-সহ যোগ হয়)।
            - **12** হলো `CROSS JOIN`-এর সংখ্যা (3 × 4)।
            - INNER JOIN দিলে 3টা row আসত (Rahim ×2, Karim ×1)।

            বাস্তব প্রভাব: orders-এর সাথে join করার পর `SUM(c.credit_limit)` করলে Rahim-এর limit দুবার গোনা হয়। আগে "many" দিকটা aggregate করো (subquery/CTE-তে), তারপর join করো।
        """,
        tip_en=r"""Count it per customer out loud (2 + 1 + 1), then quickly give the INNER, FULL, and CROSS counts too — it shows you can reason about any join type, not just this one.""",
        tip_bn=r"""Customer ধরে ধরে জোরে গুনে দেখাও (2 + 1 + 1), তারপর দ্রুত INNER, FULL আর CROSS-এর সংখ্যাও বলে দাও — এতে বোঝা যায় তুমি শুধু এটা না, যেকোনো join type নিয়েই যুক্তি দিতে পারো।""",
        related=["sql-002", "sql-016"],
        refs=[PG_JOIN_TUT, PG_TABLE_EXPR],
    ),
    # ------------------------------------------------------------------ sql-020
    Q(
        id="sql-020", sub="Indexes & Sargability", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["indexes", "sargability", "composite-index", "query-optimization", "explain"],
        ver="Version-independent (examples tested on PostgreSQL 18 semantics)", vs=False, status="stable",
        q_en=r"""All three queries below are slow on large tables even though the listed indexes exist. Explain why each one can't use its index efficiently and how you'd fix it.""",
        q_bn=r"""নিচের তিনটা query-ই বড় table-এ ধীর, যদিও উল্লেখ করা index-গুলো আছে। প্রতিটা কেন তার index ভালোভাবে ব্যবহার করতে পারছে না, আর কীভাবে ঠিক করবে — ব্যাখ্যা করো।""",
        code=r"""
            -- existing indexes
            CREATE INDEX idx_orders_created_at ON orders (created_at);
            CREATE INDEX idx_customers_name    ON customers (last_name, first_name);
            CREATE INDEX idx_customers_phone   ON customers (phone);

            -- Q1: orders placed in 2025
            SELECT * FROM orders
            WHERE EXTRACT(YEAR FROM created_at) = 2025;

            -- Q2: customers by first name
            SELECT * FROM customers
            WHERE first_name = 'Nadia';

            -- Q3: customers whose phone ends in 4567
            SELECT * FROM customers
            WHERE phone LIKE '%4567';
        """,
        lang="sql",
        extra=[dict(lang="sql", label_en="Fixed versions", label_bn="সংশোধিত version", src=r"""
            -- Q1: compare the bare column with a half-open range (sargable)
            SELECT * FROM orders
            WHERE created_at >= '2025-01-01'
              AND created_at <  '2026-01-01';

            -- Q2: the composite index starts with last_name; add an index that starts with first_name
            CREATE INDEX idx_customers_first_name ON customers (first_name);
            -- (or reorder the composite index if most queries filter by first_name)

            -- Q3: a leading wildcard can't use a B-tree; index the reversed value (or use a trigram index)
            -- expression index; in PostgreSQL, text_pattern_ops lets LIKE 'prefix%' use it under any collation
            CREATE INDEX idx_customers_phone_rev ON customers (REVERSE(phone) text_pattern_ops);
            SELECT * FROM customers
            WHERE REVERSE(phone) LIKE '7654%';
            -- PostgreSQL alternative: CREATE EXTENSION pg_trgm;
            --   CREATE INDEX ON customers USING gin (phone gin_trgm_ops);  -- supports LIKE '%4567'

            -- always confirm with the plan
            EXPLAIN SELECT * FROM orders WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';
        """)],
        a_en=r"""
            A predicate is **sargable** (Search ARGument-able) when the database can turn it into a range seek on an index.

            - **Q1 — function on the indexed column.** The index stores `created_at` values, not `EXTRACT(YEAR ...)` results, so the database must compute the function for every row. Rewrite as a half-open range on the bare column: `created_at >= '2025-01-01' AND created_at < '2026-01-01'`.
            - **Q2 — wrong column order.** A composite B-tree on `(last_name, first_name)` is sorted by `last_name` first, like a phone book. Searching only by `first_name` can't use the sort order (leftmost-prefix rule). Add an index on `first_name`, or reorder the composite index if that's the common query.
            - **Q3 — leading wildcard.** `LIKE '%4567'` has no fixed prefix, so a B-tree can't seek. Index `REVERSE(phone)` and search for the reversed prefix, or use a trigram index (`pg_trgm` in PostgreSQL).
        """,
        a_bn=r"""
            একটা predicate **sargable** (Search ARGument-able) হয় যখন database এটাকে index-এর উপর range seek-এ রূপান্তর করতে পারে।

            - **Q1 — indexed column-এর উপর function।** Index-এ `created_at`-এর value রাখা আছে, `EXTRACT(YEAR ...)`-এর ফল নয়, তাই database-কে প্রতিটা row-এর জন্য function হিসাব করতে হয়। কাঁচা column-এর উপর half-open range দিয়ে আবার লেখো: `created_at >= '2025-01-01' AND created_at < '2026-01-01'`।
            - **Q2 — column-এর ভুল ক্রম।** `(last_name, first_name)`-এর composite B-tree phone book-এর মতো আগে `last_name` অনুযায়ী সাজানো। শুধু `first_name` দিয়ে খুঁজলে এই সাজানো ক্রম কাজে লাগে না (leftmost-prefix rule)। `first_name`-এ একটা index দাও, অথবা সেটাই যদি সাধারণ query হয় তবে composite index-এর ক্রম বদলাও।
            - **Q3 — শুরুতে wildcard।** `LIKE '%4567'`-এর কোনো নির্দিষ্ট prefix নেই, তাই B-tree seek করতে পারে না। `REVERSE(phone)`-এ index দিয়ে উল্টো prefix খোঁজো, অথবা trigram index ব্যবহার করো (PostgreSQL-এ `pg_trgm`)।
        """,
        quick_en=r"""All three predicates aren't sargable: a function on the indexed column, a search on only the second column of a composite index, and a leading-wildcard `LIKE`. Fix them with a half-open range on the bare column, an index on `first_name`, and a reversed-value or trigram index.""",
        quick_bn=r"""তিনটা predicate-ই sargable নয়: indexed column-এর ওপর function, composite index-এর শুধু দ্বিতীয় column দিয়ে search, আর শুরুতে wildcard-সহ `LIKE`। Fix: খালি column-এর ওপর half-open range, `first_name`-এ index, আর reverse করা value বা trigram index।""",
        ex_en=r"""
            - **Composite index column order:** put columns used with equality first and range/sort columns last, e.g. `(customer_id, created_at)` serves `WHERE customer_id = ? AND created_at >= ?` and `ORDER BY created_at` for one customer. The index also serves queries on just `customer_id`, but not on just `created_at`. (PostgreSQL 18's skip scan can sometimes use a non-leading column when the leading column has very few distinct values — it doesn't help here, since `last_name` has many.)
            - **Other sargability killers:** arithmetic on the column (`WHERE price * 1.15 > 1000` → `WHERE price > 1000 / 1.15`), implicit type conversions (comparing a `VARCHAR` column to a number in MySQL), `OR` across different columns (sometimes rewrite as `UNION`), and `LOWER(email) = ...` without a matching expression index.
            - Half-open ranges (`>=` start, `<` next start) are safer than `BETWEEN '2025-01-01' AND '2025-12-31'`, which misses times on Dec 31 for timestamp columns.
            - Verify with `EXPLAIN` — look for an Index/Bitmap Index Scan instead of a Seq Scan, and remember that for low-selectivity filters a full scan may legitimately be cheaper.
        """,
        ex_bn=r"""
            - **Composite index-এ column-এর ক্রম:** equality দিয়ে ব্যবহার হওয়া column আগে, range/sort-এর column পরে রাখো, যেমন `(customer_id, created_at)` একজন customer-এর জন্য `WHERE customer_id = ? AND created_at >= ?` আর `ORDER BY created_at` দুটোই সামলায়। Index-টা শুধু `customer_id`-এর query-ও সামলায়, কিন্তু শুধু `created_at`-এর নয়। (PostgreSQL 18-এর skip scan কখনো কখনো প্রথম column-এর distinct value খুব কম হলে পরের column ব্যবহার করতে পারে — এখানে কাজে আসে না, কারণ `last_name`-এর value অনেক।)
            - **Sargability নষ্ট করার আরও কারণ:** column-এর উপর অঙ্ক (`WHERE price * 1.15 > 1000` → `WHERE price > 1000 / 1.15`), implicit type conversion (MySQL-এ `VARCHAR` column-কে সংখ্যার সাথে তুলনা), ভিন্ন column-এর মধ্যে `OR` (কখনো `UNION` দিয়ে আবার লেখা যায়), আর মিলে যাওয়া expression index ছাড়া `LOWER(email) = ...`।
            - Half-open range (`>=` শুরু, `<` পরের শুরু) `BETWEEN '2025-01-01' AND '2025-12-31'`-এর চেয়ে নিরাপদ — timestamp column-এ ওটা Dec 31-এর দিনের সময়গুলো বাদ দিয়ে দেয়।
            - `EXPLAIN` দিয়ে যাচাই করো — Seq Scan-এর বদলে Index/Bitmap Index Scan খোঁজো, আর মনে রেখো কম selectivity-র filter-এ পুরো scan আসলেই সস্তা হতে পারে।
        """,
        tip_en=r"""Use the word "sargable" and the phone-book analogy for composite indexes. For each query, give root cause → rewrite → how you'd verify with `EXPLAIN`.""",
        tip_bn=r""""Sargable" শব্দটা ব্যবহার করো, আর composite index-এর জন্য phone book-এর উপমা দাও। প্রতিটা query-র জন্য বলো: root cause → নতুন করে লেখা → `EXPLAIN` দিয়ে কীভাবে যাচাই করবে।""",
        mist_en=r"""Adding more indexes without rewriting the predicates, using `BETWEEN ... '2025-12-31'` on timestamps, or assuming a composite index helps any query that mentions any of its columns.""",
        mist_bn=r"""Predicate না বদলে শুধু আরও index যোগ করা, timestamp-এ `BETWEEN ... '2025-12-31'` ব্যবহার করা, অথবা ধরে নেওয়া যে composite index তার যেকোনো column উল্লেখ করা query-কেই সাহায্য করবে।""",
        follow=[
            ("Which queries can use an index on `(customer_id, status, created_at)`?", "`(customer_id, status, created_at)`-এর index কোন কোন query ব্যবহার করতে পারে?"),
            ("Why might the database ignore a perfectly good index?", "একটা ভালো index থাকা সত্ত্বেও database কেন সেটা উপেক্ষা করতে পারে?"),
        ],
        related=["sql-026", "sql-031"],
        refs=[PG_INDEXES_MULTI, PG_INDEXES_EXPR, PG_USING_EXPLAIN],
    ),
    # ------------------------------------------------------------------ sql-021
    Q(
        id="sql-021", sub="SQL Injection & Parameterized Queries", diff="medium", type="security-performance",
        prio="high", market="both", mins=6,
        tags=["sql-injection", "parameterized-queries", "node-pg", "security", "owasp"],
        ver="node-postgres 8.x on Node.js 26 LTS; Express 5.x", vs=False, status="stable",
        q_en=r"""This Express endpoint builds SQL with template strings. Show how it can be exploited and rewrite it safely, including the user-controlled sort order.""",
        q_bn=r"""এই Express endpoint template string দিয়ে SQL বানায়। এটা কীভাবে exploit করা যায় দেখাও, আর user-নিয়ন্ত্রিত sort order-সহ নিরাপদভাবে আবার লেখো।""",
        code=r"""
            app.get('/products', async (req, res) => {
              const { search = '', sort = 'name' } = req.query;

              const sql = `SELECT id, name, price
                           FROM products
                           WHERE name ILIKE '%${search}%'
                           ORDER BY ${sort}`;

              const { rows } = await pool.query(sql);
              res.json(rows);
            });
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Safe version: parameters for values, an allowlist for identifiers",
                    label_bn="নিরাপদ version: value-র জন্য parameter, identifier-এর জন্য allowlist", src=r"""
            const SORTS = new Map([
              ['name',       'name ASC'],
              ['price_asc',  'price ASC'],
              ['price_desc', 'price DESC'],
            ]);

            // escape LIKE wildcards so "%" or "_" typed by the user are matched literally
            const escapeLike = (s) => s.replace(/[\\%_]/g, (m) => '\\' + m);

            app.get('/products', async (req, res) => {
              const search  = typeof req.query.search === 'string' ? req.query.search : '';
              const orderBy = SORTS.get(req.query.sort) ?? 'name ASC';   // never user text in SQL

              const { rows } = await pool.query(
                `SELECT id, name, price
                   FROM products
                  WHERE name ILIKE '%' || $1 || '%'
                  ORDER BY ${orderBy}, id
                  LIMIT 50`,
                [escapeLike(search)],          // value travels separately from the SQL text
              );
              res.json(rows);
            });
        """)],
        a_en=r"""
            User input is pasted into the SQL text, so the attacker controls the query's *structure*:
            - `search = ' OR 1=1 --` → `WHERE name ILIKE '%' OR 1=1 --%'` returns every row (and the same idea leaks other tables with `UNION SELECT`).
            - Because `pool.query(sql)` is called **without parameters**, node-postgres uses the simple query protocol, which accepts several statements — so `'; DROP TABLE products; --` could run too.
            - `sort` is injected as an expression: a payload like `(CASE WHEN <condition on secret data> THEN name ELSE id::text END)` leaks data one bit at a time through the sort order (blind injection).

            Fix: **parameterized queries** — `$1` placeholders with values passed separately, so input is always data, never SQL. Identifiers (column names, sort direction) can't be parameters, so map user choices through an **allowlist**. Defence in depth: a least-privilege DB role, input validation, `LIMIT`, and no raw SQL error messages to clients.
        """,
        a_bn=r"""
            User input সরাসরি SQL text-এ বসানো হচ্ছে, তাই attacker query-র *গঠনই* নিয়ন্ত্রণ করে:
            - `search = ' OR 1=1 --` → `WHERE name ILIKE '%' OR 1=1 --%'` সব row ফেরত দেয় (আর একই কৌশলে `UNION SELECT` দিয়ে অন্য table-এর data বের করা যায়)।
            - `pool.query(sql)` **parameter ছাড়া** call হওয়ায় node-postgres simple query protocol ব্যবহার করে, যা একাধিক statement মেনে নেয় — তাই `'; DROP TABLE products; --`-ও চলে যেতে পারে।
            - `sort` expression হিসেবে inject হয়: `(CASE WHEN <গোপন data-র উপর condition> THEN name ELSE id::text END)`-এর মতো payload দিয়ে sort order-এর মাধ্যমে একটু একটু করে data ফাঁস করা যায় (blind injection)।

            সমাধান: **parameterized query** — `$1` placeholder, value আলাদাভাবে পাঠানো, তাই input সবসময় data, কখনো SQL নয়। Identifier (column-এর নাম, sort direction) parameter হতে পারে না, তাই user-এর পছন্দ একটা **allowlist** দিয়ে map করো। বাড়তি সুরক্ষা: least-privilege DB role, input validation, `LIMIT`, আর client-কে কাঁচা SQL error message না দেখানো।
        """,
        quick_en=r"""Pasting input into SQL lets an attacker change the query: `' OR 1=1 --` returns every row, and `sort` can leak data. Use parameterized queries with `$1` placeholders for values, and an allowlist for identifiers like the sort column, which can't be parameters.""",
        quick_bn=r"""Input সরাসরি SQL-এ বসালে attacker query বদলে দিতে পারে: `' OR 1=1 --` সব row ফেরত দেয়, আর `sort` দিয়ে data ফাঁস হতে পারে। Value-র জন্য `$1` placeholder-সহ parameterized query ব্যবহার করো, আর sort column-এর মতো identifier, যেগুলো parameter হতে পারে না, সেগুলোর জন্য allowlist।""",
        ex_en=r"""
            - **Why parameters work:** with `pool.query(text, values)`, node-postgres uses the extended protocol — the SQL is parsed first, and `$1` is bound to a value afterwards. Nothing in the value can change the parse tree.
            - **Escaping by hand is fragile** (encodings, quotes, backslashes, numeric contexts). Use parameters; reserve escaping for LIKE wildcards inside an already-parameterized value.
            - **ORMs aren't automatically safe:** raw-query helpers (`sequelize.query`, Prisma `$queryRawUnsafe`, string-built Knex/Drizzle `sql.raw`) reintroduce injection if you interpolate input.
            - **Stored procedures** help only if they don't build dynamic SQL from their arguments internally.
            - Placeholder syntax differs: PostgreSQL drivers use `$1`, MySQL drivers `?`, SQL Server `@name`. `ILIKE` is PostgreSQL-specific (use `LOWER(name) LIKE LOWER(?)` elsewhere).
        """,
        ex_bn=r"""
            - **Parameter কেন কাজ করে:** `pool.query(text, values)`-এ node-postgres extended protocol ব্যবহার করে — SQL আগে parse হয়, তারপর `$1`-এ value বসানো হয়। Value-এর ভেতরের কিছুই parse tree বদলাতে পারে না।
            - **হাতে escape করা ভঙ্গুর** (encoding, quote, backslash, numeric context)। Parameter ব্যবহার করো; escape শুধু আগে থেকেই parameterized value-এর ভেতরের LIKE wildcard-এর জন্য রাখো।
            - **ORM মানেই নিরাপদ নয়:** raw-query helper (`sequelize.query`, Prisma `$queryRawUnsafe`, string দিয়ে বানানো Knex/Drizzle `sql.raw`)-এ input interpolate করলে injection আবার ফিরে আসে।
            - **Stored procedure** তখনই সাহায্য করে যখন এর ভেতরে argument থেকে dynamic SQL বানানো হয় না।
            - Placeholder syntax আলাদা: PostgreSQL driver `$1`, MySQL driver `?`, SQL Server `@name`। `ILIKE` PostgreSQL-specific (অন্য জায়গায় `LOWER(name) LIKE LOWER(?)` ব্যবহার করো)।
        """,
        tip_en=r"""Demonstrate one concrete payload, then explain *why* parameters fix it (parse first, bind later). Calling out that identifiers need an allowlist is the detail most candidates miss.""",
        tip_bn=r"""একটা concrete payload দেখাও, তারপর ব্যাখ্যা করো parameter *কেন* সমস্যা মেটায় (আগে parse, পরে bind)। Identifier-এর জন্য যে allowlist লাগে — এই খুঁটিনাটি বেশিরভাগ candidate মিস করে।""",
        mist_en=r"""Trying to pass the `ORDER BY` column as `$2` (it becomes a constant, so sorting silently does nothing), escaping quotes manually, or trusting "frontend validation".""",
        mist_bn=r"""`ORDER BY` column-কে `$2` হিসেবে পাঠানোর চেষ্টা করা (তখন এটা constant হয়ে যায়, sort নীরবে কিছুই করে না), হাতে quote escape করা, অথবা "frontend validation"-এর উপর ভরসা করা।""",
        follow=[
            ("Why can't you pass a table or column name as a query parameter?", "Table বা column-এর নাম কেন query parameter হিসেবে পাঠানো যায় না?"),
            ("What is second-order SQL injection?", "Second-order SQL injection কী?"),
        ],
        related=["sql-028"],
        refs=[OWASP_SQLI, OWASP_PARAMS, NODE_PG],
    ),
    # ------------------------------------------------------------------ sql-022
    Q(
        id="sql-022", sub="INSERT, UPDATE & DELETE", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["update", "subquery", "dml", "insert-select", "returning"],
        ver="Version-independent (ISO SQL; output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Increase the price of every product in the **Electronics** category by 10% (rounded to 2 decimals), using the `categories` table to find the category. Then show all products.""",
        q_bn=r"""`categories` table থেকে category খুঁজে **Electronics** category-র প্রতিটা product-এর দাম 10% বাড়াও (2 দশমিক পর্যন্ত round করে)। তারপর সব product দেখাও।""",
        setup=r"""
            CREATE TABLE categories (
              id   INT PRIMARY KEY,
              name VARCHAR(30) NOT NULL
            );

            CREATE TABLE products (
              id          INT PRIMARY KEY,
              name        VARCHAR(50) NOT NULL,
              category_id INT NOT NULL REFERENCES categories(id),
              price       NUMERIC(10,2) NOT NULL
            );

            INSERT INTO categories (id, name) VALUES (1, 'Electronics'), (2, 'Fashion'), (3, 'Grocery');

            INSERT INTO products (id, name, category_id, price) VALUES
              (1, 'Walton Table Fan', 1, 3500.00),
              (2, 'Rice Cooker',      1, 2800.00),
              (3, 'Panjabi',          2, 1800.00),
              (4, 'Jamdani Saree',    2, 4500.00),
              (5, 'Mustard Oil 1L',   3,  280.00);
        """,
        code=r"""
            UPDATE products
            SET price = ROUND(price * 1.10, 2)
            WHERE category_id IN (
              SELECT id FROM categories WHERE name = 'Electronics'
            );

            SELECT id, name, price
            FROM products
            ORDER BY id;
        """,
        lang="sql",
        output=r"""
             id |       name       |  price
            ----+------------------+---------
              1 | Walton Table Fan | 3850.00
              2 | Rice Cooker      | 3080.00
              3 | Panjabi          | 1800.00
              4 | Jamdani Saree    | 4500.00
              5 | Mustard Oil 1L   |  280.00
        """,
        extra=[dict(lang="sql", label_en="Dialect variants and other DML patterns", label_bn="Dialect-ভেদে রূপ আর অন্যান্য DML pattern", src=r"""
            -- PostgreSQL: UPDATE ... FROM (join syntax) + RETURNING
            UPDATE products p
            SET price = ROUND(p.price * 1.10, 2)
            FROM categories c
            WHERE c.id = p.category_id AND c.name = 'Electronics'
            RETURNING p.id, p.price;

            -- MySQL: UPDATE ... JOIN
            -- UPDATE products p JOIN categories c ON c.id = p.category_id
            -- SET p.price = ROUND(p.price * 1.10, 2) WHERE c.name = 'Electronics';

            -- INSERT ... SELECT: copy rows from a query
            INSERT INTO price_history (product_id, old_price, changed_at)
            SELECT id, price, CURRENT_TIMESTAMP
            FROM products
            WHERE category_id = 1;

            -- DELETE with a subquery
            DELETE FROM products
            WHERE category_id IN (SELECT id FROM categories WHERE name = 'Discontinued');
        """)],
        a_en=r"""
            The `WHERE category_id IN (SELECT id FROM categories WHERE name = 'Electronics')` subquery resolves the category name to its id, so only products 1 and 2 are updated: 3500.00 × 1.10 = 3850.00 and 2800.00 × 1.10 = 3080.00. `ROUND(..., 2)` keeps exactly two decimals; the other categories are untouched.

            This subquery form is portable across databases. PostgreSQL also supports `UPDATE ... FROM` (a join), and MySQL `UPDATE ... JOIN` — handy when you need columns from the other table in the `SET` clause.
        """,
        a_bn=r"""
            `WHERE category_id IN (SELECT id FROM categories WHERE name = 'Electronics')` subquery category-র নাম থেকে তার id বের করে, তাই শুধু product 1 আর 2 update হয়: 3500.00 × 1.10 = 3850.00 আর 2800.00 × 1.10 = 3080.00। `ROUND(..., 2)` ঠিক দুই দশমিক রাখে; বাকি category-গুলো অপরিবর্তিত থাকে।

            এই subquery-রূপ সব database-এ চলে। PostgreSQL-এ `UPDATE ... FROM` (join), আর MySQL-এ `UPDATE ... JOIN`-ও আছে — `SET` clause-এ অন্য table-এর column দরকার হলে এগুলো কাজে লাগে।
        """,
        quick_en=r"""`UPDATE products SET price = ROUND(price * 1.10, 2) WHERE category_id IN (SELECT id FROM categories WHERE name = 'Electronics')`. The subquery form is portable; PostgreSQL also has `UPDATE ... FROM` and MySQL `UPDATE ... JOIN`.""",
        quick_bn=r"""`UPDATE products SET price = ROUND(price * 1.10, 2) WHERE category_id IN (SELECT id FROM categories WHERE name = 'Electronics')`। Subquery-র রূপটা সব database-এ চলে; PostgreSQL-এ `UPDATE ... FROM` আর MySQL-এ `UPDATE ... JOIN`-ও আছে।""",
        ex_en=r"""
            **Safe habits for writes on production data:**
            - Run the `WHERE` clause as a `SELECT` first and check the row count.
            - Wrap it in a transaction; check the affected-row count before `COMMIT`.
            - Never run `UPDATE`/`DELETE` without a `WHERE` unless you really mean "every row" (some tools offer a safe-updates mode for this).
            - Large updates: do them in batches to avoid long locks and huge transactions.

            **Useful patterns:** `INSERT ... SELECT` copies query results into a table (archiving, history); PostgreSQL's `RETURNING` (also in SQLite 3.35+, and similar `OUTPUT` in SQL Server) gives back the changed rows without a second query.

            Store money as `NUMERIC/DECIMAL`, not `FLOAT`, so `3500.00 × 1.10` is exactly `3850.00`.
        """,
        ex_bn=r"""
            **Production data-য় write করার নিরাপদ অভ্যাস:**
            - আগে `WHERE` clause-টা `SELECT` হিসেবে চালিয়ে row সংখ্যা দেখে নাও।
            - Transaction-এ মুড়ে নাও; `COMMIT`-এর আগে affected-row সংখ্যা check করো।
            - সত্যিই "সব row" বোঝাতে না চাইলে কখনো `WHERE` ছাড়া `UPDATE`/`DELETE` চালিয়ো না (কিছু tool-এ এর জন্য safe-updates mode আছে)।
            - বড় update: লম্বা lock আর বিশাল transaction এড়াতে batch-এ করো।

            **কাজের pattern:** `INSERT ... SELECT` query-র ফলাফল একটা table-এ কপি করে (archiving, history); PostgreSQL-এর `RETURNING` (SQLite 3.35+-এও আছে, SQL Server-এ একই রকম `OUTPUT`) দ্বিতীয় query ছাড়াই পরিবর্তিত row-গুলো ফেরত দেয়।

            টাকা `FLOAT`-এ নয়, `NUMERIC/DECIMAL`-এ রাখো, যাতে `3500.00 × 1.10` ঠিক `3850.00` হয়।
        """,
        tip_en=r"""Write the portable subquery version first, then mention the PostgreSQL/MySQL join variants. Saying you'd preview with a `SELECT` and wrap it in a transaction shows production discipline.""",
        tip_bn=r"""আগে portable subquery version লেখো, তারপর PostgreSQL/MySQL-এর join রূপের কথা বলো। `SELECT` দিয়ে preview দেখে transaction-এ মুড়ে চালাবে বললে production-এর শৃঙ্খলা দেখা যায়।""",
        mist_en=r"""Using `= (SELECT id ...)` when the subquery can return several rows (runtime error), or forgetting the `WHERE` and updating every product.""",
        mist_bn=r"""Subquery একাধিক row দিতে পারলেও `= (SELECT id ...)` ব্যবহার করা (runtime error), অথবা `WHERE` ভুলে গিয়ে সব product update করে ফেলা।""",
        follow=[
            ("How would you log every old and new price change automatically?", "প্রতিটা পুরনো আর নতুন দামের পরিবর্তন automatically কীভাবে log করবে?"),
            ("How do you update 50 million rows without locking the table for minutes?", "Table কয়েক মিনিট lock না করে ৫ কোটি row কীভাবে update করবে?"),
        ],
        related=["sql-010", "sql-028"],
        refs=[PG_UPDATE, PG_INSERT],
    ),
    # ------------------------------------------------------------------ sql-023
    Q(
        id="sql-023", sub="Recursive CTEs", diff="hard", type="query",
        prio="high", market="both", mins=8,
        tags=["recursive-cte", "hierarchy", "org-chart", "with-recursive"],
        ver="SQL:1999 recursive CTE (PostgreSQL, SQLite 3.8.3+, MySQL 8+, SQL Server, Oracle 11gR2+); output from PostgreSQL 18", vs=False, status="stable",
        q_en=r"""Using the `employees` table (each row has a `manager_id`), list **everyone in the CTO's (Mitu's) reporting line at any depth**, including Mitu herself, with their depth below her and the full path (e.g. `Mitu > Joy > Omar`).""",
        q_bn=r"""`employees` table ব্যবহার করে (প্রতিটা row-এ `manager_id` আছে) **CTO (Mitu)-র reporting line-এর যেকোনো গভীরতার সবাইকে** বের করো, Mitu-সহ — Mitu-র নিচে তাদের depth আর পুরো path-সহ (যেমন `Mitu > Joy > Omar`)।""",
        setup=r"""
            CREATE TABLE employees (
              id         INT PRIMARY KEY,
              name       VARCHAR(50) NOT NULL,
              title      VARCHAR(50) NOT NULL,
              manager_id INT REFERENCES employees(id)
            );

            INSERT INTO employees (id, name, title, manager_id) VALUES
              (1, 'Shafiq', 'CEO',                 NULL),
              (2, 'Mitu',   'CTO',                 1),
              (3, 'Rafi',   'CFO',                 1),
              (4, 'Joy',    'Engineering Manager', 2),
              (5, 'Lina',   'Accountant',          3),
              (6, 'Omar',   'Backend Developer',   4),
              (7, 'Puja',   'Frontend Developer',  4);
        """,
        code=r"""
            WITH RECURSIVE org AS (
              -- anchor: the starting employee
              SELECT id, name, title, 0 AS depth,
                     CAST(name AS VARCHAR(500)) AS path
              FROM employees
              WHERE id = 2
              UNION ALL
              -- recursive step: direct reports of the rows found so far
              SELECT e.id, e.name, e.title, o.depth + 1,
                     CAST(o.path || ' > ' || e.name AS VARCHAR(500))
              FROM employees e
              JOIN org o ON e.manager_id = o.id
            )
            SELECT name, title, depth, path
            FROM org
            ORDER BY path;
        """,
        lang="sql",
        output=r"""
             name |        title        | depth |       path
            ------+---------------------+-------+-------------------
             Mitu | CTO                 |     0 | Mitu
             Joy  | Engineering Manager |     1 | Mitu > Joy
             Omar | Backend Developer   |     2 | Mitu > Joy > Omar
             Puja | Frontend Developer  |     2 | Mitu > Joy > Puja
        """,
        a_en=r"""
            A recursive CTE has two parts joined by `UNION ALL`:
            1. **Anchor** — runs once: Mitu (depth 0, path `Mitu`).
            2. **Recursive member** — joins `employees` to the rows produced in the *previous* iteration (`e.manager_id = o.id`). Iteration 1 finds Joy (depth 1); iteration 2 finds Omar and Puja (depth 2); iteration 3 finds nobody, so recursion stops.

            Each step carries `depth + 1` and extends `path`, which is also a convenient sort key that prints the tree in order. Rafi, Lina, and Shafiq are outside Mitu's line, so they never appear.
        """,
        a_bn=r"""
            Recursive CTE-র দুটো অংশ থাকে, `UNION ALL` দিয়ে জোড়া:
            1. **Anchor** — একবার চলে: Mitu (depth 0, path `Mitu`)।
            2. **Recursive member** — `employees`-কে *আগের* iteration-এ পাওয়া row-গুলোর সাথে join করে (`e.manager_id = o.id`)। Iteration 1-এ Joy পাওয়া যায় (depth 1); iteration 2-এ Omar আর Puja (depth 2); iteration 3-এ কেউ নেই, তাই recursion থেমে যায়।

            প্রতিটা ধাপ `depth + 1` বহন করে আর `path` বাড়ায় — এটা একটা সুবিধাজনক sort key-ও, যা tree-টাকে ক্রম অনুযায়ী দেখায়। Rafi, Lina আর Shafiq Mitu-র line-এর বাইরে, তাই কখনো আসে না।
        """,
        quick_en=r"""Use `WITH RECURSIVE`: the anchor selects Mitu at depth 0, and the recursive member joins employees whose `manager_id` matches the previous level, adding `depth + 1` and extending the path. It stops when a level returns no rows.""",
        quick_bn=r"""`WITH RECURSIVE` ব্যবহার করো: anchor depth 0-তে Mitu-কে নেয়, আর recursive অংশ আগের level-এর সাথে `manager_id` মেলে এমন employee join করে, `depth + 1` আর path বাড়িয়ে। কোনো level-এ row না এলে recursion থেমে যায়।""",
        ex_en=r"""
            - **Cycles:** if bad data makes A manage B and B manage A, recursion never ends. Guard with a depth limit (`WHERE o.depth < 20`) or by checking the path; PostgreSQL 14+ has a standard `CYCLE` clause, and SQL Server stops at `MAXRECURSION` (default 100).
            - **Type matching:** the anchor and recursive parts must produce compatible column types — that's why `path` is cast to the same `VARCHAR(500)` in both (PostgreSQL is strict about this).
            - **Dialects:** `||` concatenation works in PostgreSQL, SQLite, and Oracle; MySQL needs `CONCAT()`, SQL Server uses `+` or `CONCAT()`. SQL Server and Oracle omit the `RECURSIVE` keyword.
            - **Going up** the tree (Omar's chain of managers) just flips the join: `JOIN org o ON e.id = o.manager_id`.
            - For very deep or read-heavy hierarchies, alternatives include materialized paths, closure tables, or PostgreSQL's `ltree` extension.
        """,
        ex_bn=r"""
            - **Cycle:** ভুল data-র কারণে A যদি B-র manager হয় আর B হয় A-র, recursion কখনো শেষ হবে না। Depth limit (`WHERE o.depth < 20`) বা path check করে পাহারা দাও; PostgreSQL 14+-এ standard `CYCLE` clause আছে, আর SQL Server `MAXRECURSION`-এ (default 100) থেমে যায়।
            - **Type মেলানো:** anchor আর recursive অংশকে compatible column type দিতে হয় — এজন্যই দুই জায়গাতেই `path`-কে একই `VARCHAR(500)`-এ cast করা হয়েছে (PostgreSQL এ ব্যাপারে কড়া)।
            - **Dialect:** `||` concatenation PostgreSQL, SQLite আর Oracle-এ চলে; MySQL-এ `CONCAT()` লাগে, SQL Server-এ `+` বা `CONCAT()`। SQL Server আর Oracle-এ `RECURSIVE` keyword লাগে না।
            - Tree-তে **উপরের দিকে যাওয়া** (Omar-এর manager-দের chain) — শুধু join উল্টে দাও: `JOIN org o ON e.id = o.manager_id`।
            - খুব গভীর বা বেশি পড়া হয় এমন hierarchy-র জন্য বিকল্প: materialized path, closure table, বা PostgreSQL-এর `ltree` extension।
        """,
        tip_en=r"""Explain anchor vs recursive member and walk through the iterations with the sample data. Raising cycle protection unprompted signals production experience.""",
        tip_bn=r"""Anchor বনাম recursive member ব্যাখ্যা করো, আর sample data দিয়ে iteration-গুলো একে একে দেখাও। কেউ না চাইতেই cycle protection-এর কথা তুললে production অভিজ্ঞতার ছাপ পড়ে।""",
        mist_en=r"""Using `UNION` instead of `UNION ALL` without understanding the deduplication cost, reversing the join direction, or forgetting cycle protection on user-editable hierarchies.""",
        mist_bn=r"""Deduplication-এর খরচ না বুঝে `UNION ALL`-এর বদলে `UNION` ব্যবহার করা, join-এর দিক উল্টে ফেলা, অথবা user-এর edit করা hierarchy-তে cycle protection ভুলে যাওয়া।""",
        follow=[
            ("Show the chain of managers above Omar up to the CEO.", "Omar-এর উপরে CEO পর্যন্ত manager-দের chain দেখাও।"),
            ("How would you count the total number of people under each manager?", "প্রতিটা manager-এর অধীনে মোট কতজন আছে কীভাবে গুনবে?"),
        ],
        related=["sql-008"],
        refs=[PG_WITH, SQLITE_WITH],
    ),
    # ------------------------------------------------------------------ sql-024
    Q(
        id="sql-024", sub="LAG & Month-over-Month Growth", diff="hard", type="query",
        prio="high", market="both", mins=8,
        tags=["lag", "window-functions", "growth", "cte", "nullif"],
        ver="SQL:2003 window functions; to_char() is PostgreSQL-specific; output from PostgreSQL 18", vs=False, status="stable",
        q_en=r"""From the `orders` table, compute **monthly revenue**, the previous month's revenue, and the **month-over-month growth percentage** (one decimal place). Avoid division-by-zero errors.""",
        q_bn=r"""`orders` table থেকে **মাসিক revenue**, আগের মাসের revenue আর **month-over-month growth percentage** (এক দশমিক পর্যন্ত) বের করো। Division-by-zero error এড়াতে হবে।""",
        setup=r"""
            CREATE TABLE orders (
              id         INT PRIMARY KEY,
              ordered_at DATE NOT NULL,
              amount     NUMERIC(12,2) NOT NULL
            );

            INSERT INTO orders (id, ordered_at, amount) VALUES
              (1, '2026-05-03',  60000.00),
              (2, '2026-05-20',  40000.00),
              (3, '2026-06-11', 120000.00),
              (4, '2026-07-02',  50000.00),
              (5, '2026-07-25',  40000.00),
              (6, '2026-08-09', 135000.00),
              (7, '2026-09-14', 100000.00),
              (8, '2026-09-29',  35000.00);
        """,
        code=r"""
            WITH monthly AS (
              SELECT to_char(ordered_at, 'YYYY-MM') AS month,     -- PostgreSQL-specific
                     SUM(amount)                    AS revenue
              FROM orders
              GROUP BY to_char(ordered_at, 'YYYY-MM')
            )
            SELECT month,
                   revenue,
                   LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
                   ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
                         / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
            FROM monthly
            ORDER BY month;
        """,
        lang="sql",
        output=r"""
              month  |  revenue  | prev_revenue | growth_pct
            ---------+-----------+--------------+------------
             2026-05 | 100000.00 |              |
             2026-06 | 120000.00 |    100000.00 |       20.0
             2026-07 |  90000.00 |    120000.00 |      -25.0
             2026-08 | 135000.00 |     90000.00 |       50.0
             2026-09 | 135000.00 |    135000.00 |        0.0
        """,
        a_en=r"""
            1. The CTE aggregates orders into one row per month (`GROUP BY` the month string).
            2. `LAG(revenue) OVER (ORDER BY month)` reads the value from the **previous row** in month order, so each month sees last month's revenue. The first month has no previous row → NULL.
            3. Growth = (current − previous) / previous × 100. `NULLIF(prev, 0)` turns a zero denominator into NULL, so the result is NULL instead of a division-by-zero error. Multiplying by `100.0` (not `100`) avoids integer division on databases where both sides would be integers.

            July: (90,000 − 120,000) / 120,000 = −25.0%; August: (135,000 − 90,000) / 90,000 = +50.0%.
        """,
        a_bn=r"""
            1. CTE order-গুলোকে প্রতি মাসে একটা row-তে aggregate করে (month string দিয়ে `GROUP BY`)।
            2. `LAG(revenue) OVER (ORDER BY month)` মাসের ক্রমে **আগের row** থেকে value পড়ে, তাই প্রতিটা মাস আগের মাসের revenue দেখতে পায়। প্রথম মাসের আগে কোনো row নেই → NULL।
            3. Growth = (বর্তমান − আগের) / আগের × 100। `NULLIF(prev, 0)` শূন্য denominator-কে NULL বানায়, ফলে division-by-zero error-এর বদলে ফলাফল NULL হয়। `100` না দিয়ে `100.0` দিয়ে গুণ করলে, যেসব database-এ দুই দিকই integer, সেখানে integer division এড়ানো যায়।

            July: (90,000 − 120,000) / 120,000 = −25.0%; August: (135,000 − 90,000) / 90,000 = +50.0%।
        """,
        quick_en=r"""Aggregate revenue per month in a CTE, read last month with `LAG(revenue) OVER (ORDER BY month)`, and compute `100.0 * (revenue - prev) / NULLIF(prev, 0)`. `NULLIF` turns a zero denominator into NULL instead of an error, and `100.0` avoids integer division.""",
        quick_bn=r"""CTE-তে মাস অনুযায়ী revenue যোগ করো, `LAG(revenue) OVER (ORDER BY month)` দিয়ে আগের মাসেরটা পড়ো, আর হিসাব করো `100.0 * (revenue - prev) / NULLIF(prev, 0)`। `NULLIF` শূন্য denominator-কে error-এর বদলে NULL বানায়, আর `100.0` integer division ঠেকায়।""",
        ex_en=r"""
            - **Missing months are the hidden bug:** `LAG` looks at the previous *row*, not the previous *calendar month*. If June had no orders, July would be compared with May. Fix by generating a month calendar (PostgreSQL: `generate_series(date '2026-05-01', date '2026-09-01', interval '1 month')`, or a recursive CTE elsewhere) and `LEFT JOIN`ing revenue to it with `COALESCE(revenue, 0)`.
            - A named window avoids repeating the definition: `... LAG(revenue) OVER w ... WINDOW w AS (ORDER BY month)`.
            - **Month expression by dialect:** PostgreSQL `to_char(d, 'YYYY-MM')` or `date_trunc('month', d)`; MySQL `DATE_FORMAT(d, '%Y-%m')`; SQLite `strftime('%Y-%m', d)`; SQL Server `FORMAT(d, 'yyyy-MM')` or `DATEFROMPARTS(YEAR(d), MONTH(d), 1)`. Grouping by a real date (first day of month) sorts correctly and is easier to join than a string.
            - `LAG(revenue, 12)` gives year-over-year; `LEAD` looks forward.
            - On big tables, index `ordered_at` and filter the date range before aggregating; precompute monthly totals if the dashboard runs often.
        """,
        ex_bn=r"""
            - **হারিয়ে যাওয়া মাস হলো লুকানো bug:** `LAG` আগের *row* দেখে, আগের *calendar মাস* নয়। June-এ কোনো order না থাকলে July-কে May-এর সাথে তুলনা করা হতো। সমাধান: একটা মাসের calendar বানাও (PostgreSQL: `generate_series(date '2026-05-01', date '2026-09-01', interval '1 month')`, অন্য জায়গায় recursive CTE) আর `COALESCE(revenue, 0)`-সহ revenue-কে তার সাথে `LEFT JOIN` করো।
            - Named window দিলে definition বারবার লিখতে হয় না: `... LAG(revenue) OVER w ... WINDOW w AS (ORDER BY month)`।
            - **Dialect অনুযায়ী month expression:** PostgreSQL `to_char(d, 'YYYY-MM')` বা `date_trunc('month', d)`; MySQL `DATE_FORMAT(d, '%Y-%m')`; SQLite `strftime('%Y-%m', d)`; SQL Server `FORMAT(d, 'yyyy-MM')` বা `DATEFROMPARTS(YEAR(d), MONTH(d), 1)`। আসল date (মাসের প্রথম দিন) দিয়ে group করলে sort ঠিক থাকে আর string-এর চেয়ে join করা সহজ।
            - `LAG(revenue, 12)` দেয় year-over-year; `LEAD` সামনের দিকে তাকায়।
            - বড় table-এ `ordered_at`-এ index দাও আর aggregate করার আগে date range filter করো; dashboard ঘনঘন চললে মাসিক total আগেই হিসাব করে রাখো।
        """,
        tip_en=r"""Mention three robustness details without being asked: NULL for the first month, `NULLIF` for zero, and the missing-month problem with `LAG`. The last one is what senior interviewers look for.""",
        tip_bn=r"""কেউ না চাইতেই তিনটা robustness-এর খুঁটিনাটি বলো: প্রথম মাসের NULL, শূন্যের জন্য `NULLIF`, আর `LAG`-এর হারিয়ে-যাওয়া-মাসের সমস্যা। শেষেরটাই senior interviewer খোঁজে।""",
        mist_en=r"""Dividing without `NULLIF` (division-by-zero error), integer division (`100 * x / y` truncating), or assuming `LAG` handles gaps in the calendar.""",
        mist_bn=r"""`NULLIF` ছাড়া ভাগ করা (division-by-zero error), integer division (`100 * x / y` কেটে ছোট হয়ে যাওয়া), অথবা ধরে নেওয়া যে `LAG` calendar-এর ফাঁক সামলায়।""",
        follow=[
            ("How would you fill in months that have no orders?", "যে মাসগুলোতে কোনো order নেই, সেগুলো কীভাবে পূরণ করবে?"),
            ("Compute a 3-month moving average of revenue.", "Revenue-এর 3-মাসের moving average হিসাব করো।"),
        ],
        related=["sql-014", "sql-018"],
        refs=[PG_WINDOW_FUNCS, PG_FORMATTING],
    ),
]

if __name__ == "__main__":
    save("sql", "b3", QUESTIONS)
