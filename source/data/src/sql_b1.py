# SQL batch 1 — sql-001 … sql-008 (fundamentals, easy)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MS_SELECT = ("Microsoft Learn — SELECT (logical processing order)", "https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql")
PG_SELECT = ("PostgreSQL docs — SELECT", "https://www.postgresql.org/docs/current/sql-select.html")
PG_TABLE_EXPR = ("PostgreSQL docs — Table Expressions (JOIN, WHERE, GROUP BY, HAVING)", "https://www.postgresql.org/docs/current/queries-table-expressions.html")
PG_JOIN_TUT = ("PostgreSQL docs — Joins Between Tables", "https://www.postgresql.org/docs/current/tutorial-join.html")
PG_AGG = ("PostgreSQL docs — Aggregate Functions", "https://www.postgresql.org/docs/current/functions-aggregate.html")
PG_AGG_TUT = ("PostgreSQL docs — Aggregate Functions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-agg.html")
PG_COMPARISON = ("PostgreSQL docs — Comparison Functions and Operators", "https://www.postgresql.org/docs/current/functions-comparison.html")
PG_CONSTRAINTS = ("PostgreSQL docs — Constraints", "https://www.postgresql.org/docs/current/ddl-constraints.html")
SQLITE_SELECT = ("SQLite — SELECT", "https://www.sqlite.org/lang_select.html")

QUESTIONS = [
    # ------------------------------------------------------------------ sql-001
    Q(
        id="sql-001", sub="Logical Query Processing Order", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["select", "where", "group-by", "having", "order-by"],
        ver="Version-independent (ISO SQL)", vs=False, status="stable",
        q_en=r"""Which sequence shows the correct **logical** processing order of the clauses in a `SELECT` statement?""",
        q_bn=r"""একটা `SELECT` statement-এর clause-গুলোর সঠিক **logical** processing order কোনটা?""",
        options=[
            ("`SELECT` → `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY`", "`SELECT` → `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY`"),
            ("`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`", "`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`"),
            ("`FROM` → `SELECT` → `WHERE` → `GROUP BY` → `ORDER BY` → `HAVING`", "`FROM` → `SELECT` → `WHERE` → `GROUP BY` → `ORDER BY` → `HAVING`"),
            ("`FROM` → `GROUP BY` → `WHERE` → `HAVING` → `SELECT` → `ORDER BY`", "`FROM` → `GROUP BY` → `WHERE` → `HAVING` → `SELECT` → `ORDER BY`"),
        ],
        correct=1,
        a_en=r"""`FROM` (including joins) → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` (then `LIMIT`/`FETCH`). We *write* `SELECT` first, but it's evaluated after the rows are filtered and grouped.""",
        a_bn=r"""`FROM` (join-সহ) → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` (তারপর `LIMIT`/`FETCH`)। আমরা `SELECT` আগে *লিখি*, কিন্তু row filter আর group হওয়ার পরে এটা evaluate হয়।""",
        ex_en=r"""
            This order explains several everyday errors:
            - `SELECT salary * 12 AS annual FROM employees WHERE annual > 600000;` fails — the alias `annual` doesn't exist yet when `WHERE` runs. Repeat the expression or use a subquery/CTE.
            - An alias **can** be used in `ORDER BY`, because `ORDER BY` runs after `SELECT`.
            - Aggregates like `COUNT(*)` can't appear in `WHERE` (groups don't exist yet) — that's what `HAVING` is for.
            - Window functions are computed after `HAVING`, so you can't filter on them in `WHERE` either.

            It's a *logical* order: the optimizer may physically execute things differently (e.g. push filters into joins) as long as the result is the same. The tempting wrong answer is the first option, because it matches the order in which we type the clauses.
        """,
        ex_bn=r"""
            এই ক্রম দিয়ে প্রতিদিনের কিছু error বোঝা যায়:
            - `SELECT salary * 12 AS annual FROM employees WHERE annual > 600000;` fail করে — `WHERE` চলার সময় `annual` alias-টা তখনো তৈরিই হয়নি। Expression-টা আবার লেখো, অথবা subquery/CTE ব্যবহার করো।
            - `ORDER BY`-তে alias **ব্যবহার করা যায়**, কারণ `ORDER BY` `SELECT`-এর পরে চলে।
            - `COUNT(*)`-এর মতো aggregate `WHERE`-এ দেওয়া যায় না (তখনো group তৈরিই হয়নি) — এর জন্যই `HAVING`।
            - Window function `HAVING`-এর পরে হিসাব হয়, তাই এগুলো দিয়েও `WHERE`-এ filter করা যায় না।

            এটা একটা *logical* ক্রম: ফলাফল একই থাকলে optimizer বাস্তবে অন্যভাবে execute করতে পারে (যেমন filter-কে join-এর ভেতরে ঠেলে দেওয়া)। লোভনীয় ভুল উত্তর প্রথম option-টা, কারণ আমরা clause-গুলো ঠিক ওই ক্রমেই লিখি।
        """,
        tip_en=r"""After giving the order, immediately use it to explain the "alias in WHERE" error — applying the concept impresses more than reciting it.""",
        tip_bn=r"""ক্রমটা বলার পরপরই এটা দিয়ে "WHERE-এ alias" error ব্যাখ্যা করো — শুধু মুখস্থ বলার চেয়ে concept প্রয়োগ করে দেখালে বেশি ভালো লাগে।""",
        related=["sql-004"],
        refs=[MS_SELECT, PG_SELECT],
    ),
    # ------------------------------------------------------------------ sql-002
    Q(
        id="sql-002", sub="JOIN Types", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["joins", "inner-join", "left-join", "full-outer-join", "cross-join"],
        ver="Version-independent (ISO SQL)", vs=False, status="stable",
        q_en=r"""Explain the different JOIN types in SQL: INNER, LEFT, RIGHT, FULL OUTER, CROSS, and SELF join. When would you use each?""",
        q_bn=r"""SQL-এর বিভিন্ন JOIN type ব্যাখ্যা করো: INNER, LEFT, RIGHT, FULL OUTER, CROSS আর SELF join। কোনটা কখন ব্যবহার করবে?""",
        a_en=r"""
            - **INNER JOIN:** only rows that match on both sides — e.g. orders with their customer.
            - **LEFT (OUTER) JOIN:** all rows from the left table, plus matches from the right; no match → NULLs. E.g. all customers, including those with no orders.
            - **RIGHT JOIN:** the mirror image; I usually rewrite it as a LEFT JOIN for readability.
            - **FULL OUTER JOIN:** all rows from both sides, matched where possible — useful for reconciling two data sources (e.g. bank statement vs internal ledger).
            - **CROSS JOIN:** every combination (Cartesian product) — e.g. every product × every size to generate a grid.
            - **SELF JOIN:** a table joined to itself with aliases — e.g. employees and their managers in the same table.
        """,
        a_bn=r"""
            - **INNER JOIN:** শুধু দুই দিকেই match করা row — যেমন order আর তার customer।
            - **LEFT (OUTER) JOIN:** বাম table-এর সব row, সাথে ডান দিকের match; match না থাকলে NULL। যেমন সব customer, যাদের কোনো order নেই তারাও।
            - **RIGHT JOIN:** উল্টো রূপ; পড়ার সুবিধার জন্য আমি সাধারণত এটাকে LEFT JOIN হিসেবে আবার লিখি।
            - **FULL OUTER JOIN:** দুই দিকেরই সব row, যেখানে সম্ভব match করে — দুটো data source মেলাতে কাজে লাগে (যেমন bank statement বনাম internal ledger)।
            - **CROSS JOIN:** সব combination (Cartesian product) — যেমন একটা grid বানাতে প্রতিটা product × প্রতিটা size।
            - **SELF JOIN:** alias দিয়ে একটা table-কে নিজের সাথেই join করা — যেমন একই table-এ employee আর তার manager।
        """,
        ex_en=r"""
            - **Row counts multiply:** a join returns one row per matching *pair*. A customer with 3 orders appears 3 times; with a LEFT JOIN, a customer with no orders still appears once (with NULLs). Aggregating after a join that fans out can double-count.
            - **Classic trap — `WHERE` on the right table after a LEFT JOIN:** `LEFT JOIN orders o ... WHERE o.status = 'paid'` removes the NULL rows and silently turns it into an inner join. Put that condition in the `ON` clause instead if you want to keep unmatched customers.
            - MySQL has no `FULL OUTER JOIN`; emulate it with a `LEFT JOIN ... UNION ... RIGHT JOIN`.
            - Avoid `NATURAL JOIN` / `USING` on wide schemas: adding a column with the same name can silently change the join.
        """,
        ex_bn=r"""
            - **Row সংখ্যা গুণ হয়:** join প্রতিটা matching *জোড়ার* জন্য একটা row দেয়। ৩টা order থাকা customer ৩ বার আসে; LEFT JOIN-এ order না থাকা customer-ও একবার আসে (NULL-সহ)। Fan out হওয়া join-এর পরে aggregate করলে double-count হতে পারে।
            - **Classic ফাঁদ — LEFT JOIN-এর পরে ডান table-এ `WHERE`:** `LEFT JOIN orders o ... WHERE o.status = 'paid'` NULL row-গুলো বাদ দিয়ে নীরবে এটাকে inner join বানিয়ে ফেলে। Unmatched customer রাখতে চাইলে condition-টা `ON` clause-এ দাও।
            - MySQL-এ `FULL OUTER JOIN` নেই; `LEFT JOIN ... UNION ... RIGHT JOIN` দিয়ে এর কাজ করানো হয়।
            - বড় schema-তে `NATURAL JOIN` / `USING` এড়িয়ে চলো: একই নামের নতুন column যোগ হলে join নীরবে বদলে যেতে পারে।
        """,
        tip_en=r"""Give a one-line business example for each type, then mention the `WHERE`-after-LEFT-JOIN trap — interviewers often follow up on exactly that.""",
        tip_bn=r"""প্রতিটা type-এর জন্য এক লাইনের business উদাহরণ দাও, তারপর LEFT JOIN-এর পরে `WHERE`-এর ফাঁদটা বলো — interviewer প্রায়ই ঠিক এটা নিয়েই পরের প্রশ্ন করে।""",
        mist_en=r"""Expecting a LEFT JOIN to return exactly one row per left-table row (it returns one per match), or filtering the right table in `WHERE` and losing unmatched rows.""",
        mist_bn=r"""ধরে নেওয়া যে LEFT JOIN বাম table-এর প্রতিটা row-এর জন্য ঠিক একটা row দেয় (আসলে প্রতিটা match-এর জন্য একটা দেয়), অথবা `WHERE`-এ ডান table filter করে unmatched row হারিয়ে ফেলা।""",
        code=r"""
            -- all customers, with their PAID orders if any (filter in ON keeps unmatched customers)
            SELECT c.name, o.id AS order_id, o.amount
            FROM customers c
            LEFT JOIN orders o
                   ON o.customer_id = c.id
                  AND o.status = 'paid';

            -- every product in every size
            SELECT p.name, s.size
            FROM products p
            CROSS JOIN sizes s;

            -- self join: each employee with their manager's name
            SELECT e.name AS employee, m.name AS manager
            FROM employees e
            LEFT JOIN employees m ON m.id = e.manager_id;
        """,
        lang="sql",
        follow=[
            ("What's the difference between putting a condition in `ON` vs `WHERE` for a LEFT JOIN?", "LEFT JOIN-এ condition `ON`-এ দেওয়া আর `WHERE`-এ দেওয়ার মধ্যে পার্থক্য কী?"),
            ("How would you emulate FULL OUTER JOIN in MySQL?", "MySQL-এ FULL OUTER JOIN-এর কাজ কীভাবে করাবে?"),
        ],
        related=["sql-019", "sql-008"],
        refs=[PG_JOIN_TUT, PG_TABLE_EXPR],
    ),
    # ------------------------------------------------------------------ sql-003
    Q(
        id="sql-003", sub="SELECT, JOIN, GROUP BY & ORDER BY", diff="easy", type="query",
        prio="high", market="both", mins=4,
        tags=["select", "join", "group-by", "order-by", "aggregates"],
        ver="Version-independent (ISO SQL; output shown from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Using the `customers` and `orders` tables below, list each customer's number of **delivered** orders and the total delivered amount, highest spender first. Only customers with at least one delivered order should appear.""",
        q_bn=r"""নিচের `customers` আর `orders` table ব্যবহার করে প্রতিটা customer-এর **delivered** order-এর সংখ্যা আর মোট delivered amount বের করো, সবচেয়ে বেশি খরচ করা customer আগে। শুধু যাদের অন্তত একটা delivered order আছে তারাই আসবে।""",
        setup=r"""
            CREATE TABLE customers (
              id   INT PRIMARY KEY,
              name VARCHAR(50) NOT NULL,
              city VARCHAR(50)
            );

            CREATE TABLE orders (
              id          INT PRIMARY KEY,
              customer_id INT NOT NULL REFERENCES customers(id),
              amount      NUMERIC(10,2) NOT NULL,
              status      VARCHAR(20) NOT NULL
            );

            INSERT INTO customers (id, name, city) VALUES
              (1, 'Rahim',  'Dhaka'),
              (2, 'Karim',  'Chattogram'),
              (3, 'Nadia',  'Dhaka'),
              (4, 'Sumi',   'Sylhet'),
              (5, 'Tanvir', 'Khulna');

            INSERT INTO orders (id, customer_id, amount, status) VALUES
              (1, 1, 1500.00, 'delivered'),
              (2, 1,  700.00, 'delivered'),
              (3, 2, 2200.00, 'delivered'),
              (4, 3,  300.00, 'cancelled'),
              (5, 3, 1200.00, 'delivered'),
              (6, 2,  800.00, 'delivered'),
              (7, 4,  950.00, 'pending'),
              (8, 1,  400.00, 'cancelled');
        """,
        code=r"""
            SELECT c.name,
                   COUNT(*)      AS delivered_orders,
                   SUM(o.amount) AS total_spent
            FROM customers c
            JOIN orders o ON o.customer_id = c.id
            WHERE o.status = 'delivered'
            GROUP BY c.id, c.name
            ORDER BY total_spent DESC;
        """,
        lang="sql",
        output=r"""
             name  | delivered_orders | total_spent
            -------+------------------+-------------
             Karim |                2 |     3000.00
             Rahim |                2 |     2200.00
             Nadia |                1 |     1200.00
        """,
        a_en=r"""
            - `JOIN` pairs every order with its customer (inner join: customers without orders disappear, which is what we want here).
            - `WHERE o.status = 'delivered'` removes cancelled and pending orders **before** grouping. So Sumi (only a pending order) and Tanvir (no orders) don't appear, and Rahim's cancelled 400 isn't counted.
            - `GROUP BY c.id, c.name` makes one group per customer; `COUNT(*)` and `SUM(o.amount)` are computed per group. Grouping by `id` too keeps two customers with the same name separate.
            - `ORDER BY total_spent DESC` can use the alias because `ORDER BY` runs after `SELECT`.
        """,
        a_bn=r"""
            - `JOIN` প্রতিটা order-কে তার customer-এর সাথে জোড়া লাগায় (inner join: যাদের order নেই তারা বাদ পড়ে — এখানে আমরা সেটাই চাই)।
            - `WHERE o.status = 'delivered'` group করার **আগেই** cancelled আর pending order বাদ দেয়। তাই Sumi (শুধু pending order) আর Tanvir (কোনো order নেই) আসে না, আর Rahim-এর cancelled 400 গোনা হয় না।
            - `GROUP BY c.id, c.name` প্রতিটা customer-এর জন্য একটা group বানায়; `COUNT(*)` আর `SUM(o.amount)` প্রতিটা group-এর জন্য হিসাব হয়। `id` দিয়েও group করায় একই নামের দুজন customer আলাদা থাকে।
            - `ORDER BY total_spent DESC`-এ alias ব্যবহার করা যায়, কারণ `ORDER BY` `SELECT`-এর পরে চলে।
        """,
        ex_en=r"""
            - Every non-aggregated column in `SELECT` must be in `GROUP BY` (or functionally dependent on it — PostgreSQL accepts `GROUP BY c.id` alone because `id` is the primary key). Older MySQL modes allowed ungrouped columns and returned arbitrary values — don't rely on that.
            - To include customers with zero delivered orders, switch to `LEFT JOIN` and move the status filter into the `ON` clause, then use `COUNT(o.id)` and `COALESCE(SUM(o.amount), 0)`.
            - If two customers tie on `total_spent`, the order between them is undefined — add a tie-breaker like `, c.name`.
            - The output formatting (e.g. `3000.00`) is PostgreSQL's; other databases may print `3000` or `3000.0`.
        """,
        ex_bn=r"""
            - `SELECT`-এর প্রতিটা non-aggregated column `GROUP BY`-তে থাকতে হবে (অথবা তার উপর functionally dependent হতে হবে — PostgreSQL শুধু `GROUP BY c.id` মেনে নেয়, কারণ `id` primary key)। পুরনো MySQL mode-এ group না করা column-ও চলত আর এলোমেলো value দিত — এর উপর ভরসা কোরো না।
            - শূন্য delivered order-ওয়ালা customer-দেরও আনতে চাইলে `LEFT JOIN`-এ যাও, status filter-টা `ON` clause-এ সরাও, তারপর `COUNT(o.id)` আর `COALESCE(SUM(o.amount), 0)` ব্যবহার করো।
            - দুজন customer-এর `total_spent` সমান হলে তাদের ক্রম নির্দিষ্ট থাকে না — `, c.name`-এর মতো একটা tie-breaker যোগ করো।
            - Output-এর format (যেমন `3000.00`) PostgreSQL-এর; অন্য database `3000` বা `3000.0` দেখাতে পারে।
        """,
        tip_en=r"""Narrate the query in execution order: join, filter, group, aggregate, sort. Pointing out why Sumi and Tanvir are missing shows you trace data, not just syntax.""",
        tip_bn=r"""Query-টা execution-এর ক্রমে বলে যাও: join, filter, group, aggregate, sort। Sumi আর Tanvir কেন নেই সেটা দেখালে বোঝা যায় তুমি শুধু syntax না, data-ও trace করো।""",
        mist_en=r"""Grouping only by `name` (merges different customers with the same name), or filtering status in `HAVING` instead of `WHERE`.""",
        mist_bn=r"""শুধু `name` দিয়ে group করা (একই নামের আলাদা customer মিশে যায়), অথবা status filter `WHERE`-এর বদলে `HAVING`-এ দেওয়া।""",
        follow=[
            ("How would you include customers with zero delivered orders?", "শূন্য delivered order-ওয়ালা customer-দেরও কীভাবে দেখাবে?"),
            ("Show only customers whose delivered total is above 2,000.", "শুধু তাদের দেখাও যাদের delivered total 2,000-এর বেশি।"),
        ],
        related=["sql-004", "sql-002"],
        refs=[PG_TABLE_EXPR, PG_AGG_TUT],
    ),
    # ------------------------------------------------------------------ sql-004
    Q(
        id="sql-004", sub="WHERE vs HAVING", diff="easy", type="query",
        prio="high", market="both", mins=4,
        tags=["where", "having", "group-by", "aggregates"],
        ver="Version-independent (ISO SQL; output shown from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Find the departments that have **at least 2 employees earning more than 50,000**. For each such department, show how many such employees it has and their average salary.""",
        q_bn=r"""যেসব department-এ **৫০,০০০-এর বেশি বেতন পাওয়া অন্তত ২ জন employee** আছে, সেগুলো বের করো। প্রতিটা department-এর জন্য এমন employee কতজন আর তাদের গড় বেতন দেখাও।""",
        setup=r"""
            CREATE TABLE employees (
              id     INT PRIMARY KEY,
              name   VARCHAR(50) NOT NULL,
              dept   VARCHAR(30) NOT NULL,
              salary NUMERIC(10,2) NOT NULL
            );

            INSERT INTO employees (id, name, dept, salary) VALUES
              (1, 'Ayesha',  'Engineering', 95000),
              (2, 'Bilal',   'Engineering', 72000),
              (3, 'Chandni', 'Engineering', 48000),
              (4, 'Dipu',    'Sales',       55000),
              (5, 'Esha',    'Sales',       45000),
              (6, 'Farhan',  'Sales',       41000),
              (7, 'Gazi',    'HR',          60000),
              (8, 'Hasan',   'HR',          52000);
        """,
        code=r"""
            SELECT dept,
                   COUNT(*)              AS high_earners,
                   ROUND(AVG(salary), 2) AS avg_high_salary
            FROM employees
            WHERE salary > 50000          -- filters ROWS, before grouping
            GROUP BY dept
            HAVING COUNT(*) >= 2          -- filters GROUPS, after aggregation
            ORDER BY dept;
        """,
        lang="sql",
        output=r"""
                dept     | high_earners | avg_high_salary
            -------------+--------------+-----------------
             Engineering |            2 |        83500.00
             HR          |            2 |        56000.00
        """,
        a_en=r"""
            - `WHERE salary > 50000` runs first and keeps only individual high earners: Ayesha, Bilal, Dipu, Gazi, Hasan.
            - `GROUP BY dept` then forms groups: Engineering (2), Sales (1: Dipu), HR (2).
            - `HAVING COUNT(*) >= 2` filters **groups** using an aggregate, dropping Sales.
            - The average is over the remaining rows only: Engineering (95000 + 72000) / 2 = 83500, HR (60000 + 52000) / 2 = 56000.

            Rule of thumb: conditions on individual rows go in `WHERE`; conditions on aggregates (`COUNT`, `SUM`, `AVG`...) go in `HAVING`.
        """,
        a_bn=r"""
            - `WHERE salary > 50000` আগে চলে আর শুধু আলাদা আলাদা বেশি বেতনের employee রাখে: Ayesha, Bilal, Dipu, Gazi, Hasan।
            - এরপর `GROUP BY dept` group বানায়: Engineering (২), Sales (১: Dipu), HR (২)।
            - `HAVING COUNT(*) >= 2` aggregate দিয়ে **group** filter করে, Sales বাদ পড়ে।
            - গড় হিসাব হয় শুধু বাকি row-গুলো দিয়ে: Engineering (95000 + 72000) / 2 = 83500, HR (60000 + 52000) / 2 = 56000।

            সহজ নিয়ম: আলাদা row-এর condition যায় `WHERE`-এ; aggregate-এর (`COUNT`, `SUM`, `AVG`...) condition যায় `HAVING`-এ।
        """,
        ex_en=r"""
            - `WHERE COUNT(*) >= 2` is an error: aggregates don't exist yet when `WHERE` runs.
            - Putting `salary > 50000` in `HAVING` instead is also wrong here: `salary` isn't grouped, so most databases reject it, and even `HAVING MAX(salary) > 50000` would answer a different question.
            - Filtering early in `WHERE` is also faster: fewer rows reach the grouping step. Use `HAVING` only for conditions that truly need aggregates.
            - The engine may give `AVG` a different type or scale (PostgreSQL returns `numeric`, hence `ROUND(..., 2)` → `83500.00`).
        """,
        ex_bn=r"""
            - `WHERE COUNT(*) >= 2` error দেয়: `WHERE` চলার সময় aggregate-এর অস্তিত্বই থাকে না।
            - এখানে `salary > 50000` `HAVING`-এ দেওয়াও ভুল: `salary` group করা হয়নি, তাই বেশিরভাগ database এটা reject করে, আর `HAVING MAX(salary) > 50000` দিলেও সেটা অন্য প্রশ্নের উত্তর দেবে।
            - আগেভাগে `WHERE`-এ filter করা দ্রুতও: grouping step-এ কম row পৌঁছায়। শুধু যেসব condition-এ সত্যিই aggregate লাগে, সেগুলোর জন্য `HAVING` ব্যবহার করো।
            - Engine ভেদে `AVG`-এর type বা scale আলাদা হতে পারে (PostgreSQL `numeric` দেয়, তাই `ROUND(..., 2)` → `83500.00`)।
        """,
        tip_en=r"""State the one-line rule ("WHERE filters rows, HAVING filters groups"), then walk through which rows survive each step with the sample data.""",
        tip_bn=r"""এক লাইনের নিয়মটা বলো ("WHERE row filter করে, HAVING group filter করে"), তারপর sample data দিয়ে দেখাও প্রতিটা ধাপে কোন row-গুলো টিকে থাকে।""",
        mist_en=r"""Writing `HAVING salary > 50000` (wrong question / error), or using `WHERE COUNT(*) >= 2`.""",
        mist_bn=r"""`HAVING salary > 50000` লেখা (ভুল প্রশ্ন / error), অথবা `WHERE COUNT(*) >= 2` ব্যবহার করা।""",
        follow=[
            ("Can a query have `HAVING` without `GROUP BY`? What does it do?", "`GROUP BY` ছাড়া কি query-তে `HAVING` থাকতে পারে? তখন এটা কী করে?"),
            ("How would you also show departments with zero high earners?", "শূন্য বেশি-বেতনের employee থাকা department-গুলোও কীভাবে দেখাবে?"),
        ],
        related=["sql-001", "sql-003"],
        refs=[PG_TABLE_EXPR, PG_AGG_TUT],
    ),
    # ------------------------------------------------------------------ sql-005
    Q(
        id="sql-005", sub="Aggregate Functions & NULL", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["count", "avg", "null", "aggregates", "output"],
        ver="Version-independent (ISO SQL)", vs=False, status="stable",
        q_en=r"""What does this query return?""",
        q_bn=r"""এই query কী return করবে?""",
        code=r"""
            CREATE TABLE bonuses (emp_id INT PRIMARY KEY, bonus INT);
            INSERT INTO bonuses (emp_id, bonus) VALUES
              (1, 500), (2, NULL), (3, 500), (4, NULL), (5, 300);

            SELECT COUNT(*)              AS all_rows,
                   COUNT(bonus)          AS with_bonus,
                   COUNT(DISTINCT bonus) AS distinct_bonus,
                   ROUND(AVG(bonus), 2)  AS avg_bonus
            FROM bonuses;
        """,
        lang="sql",
        output=r"""
             all_rows | with_bonus | distinct_bonus | avg_bonus
            ----------+------------+----------------+-----------
                    5 |          3 |              2 |    433.33
        """,
        options=[
            ("`5 | 5 | 3 | 260.00`", "`5 | 5 | 3 | 260.00`"),
            ("`5 | 3 | 2 | 433.33`", "`5 | 3 | 2 | 433.33`"),
            ("`3 | 3 | 2 | 433.33`", "`3 | 3 | 2 | 433.33`"),
            ("`5 | 3 | 3 | 260.00`", "`5 | 3 | 3 | 260.00`"),
        ],
        correct=1,
        a_en=r"""`5 | 3 | 2 | 433.33`. `COUNT(*)` counts rows (5); `COUNT(bonus)` skips NULLs (3); `COUNT(DISTINCT bonus)` counts distinct non-NULL values {500, 300} (2); `AVG` ignores NULLs, so it's 1300 / 3 = 433.33, not 1300 / 5.""",
        a_bn=r"""`5 | 3 | 2 | 433.33`। `COUNT(*)` row গোনে (5); `COUNT(bonus)` NULL বাদ দেয় (3); `COUNT(DISTINCT bonus)` আলাদা non-NULL value গোনে {500, 300} (2); `AVG` NULL উপেক্ষা করে, তাই 1300 / 3 = 433.33, 1300 / 5 নয়।""",
        ex_en=r"""
            All standard aggregates except `COUNT(*)` ignore NULLs. The tempting trap is `AVG = 260` (treating NULL as 0). If the business rule says "no bonus means 0", make it explicit: `AVG(COALESCE(bonus, 0))` → 260.00.

            Also remember: `SUM` over zero rows (or only NULLs) returns NULL, not 0 — wrap it in `COALESCE(SUM(x), 0)` when you need a number.

            Engine detail: PostgreSQL, MySQL, and SQLite return a fractional average here (433.33 after rounding), but SQL Server's `AVG` over an `INT` column returns an integer (433) — use `AVG(CAST(bonus AS DECIMAL(10,2)))` there.
        """,
        ex_bn=r"""
            `COUNT(*)` ছাড়া সব standard aggregate NULL উপেক্ষা করে। লোভনীয় ফাঁদ হলো `AVG = 260` (NULL-কে 0 ধরা)। যদি business rule বলে "bonus নেই মানে 0", তাহলে সেটা স্পষ্ট করে লেখো: `AVG(COALESCE(bonus, 0))` → 260.00।

            আরও মনে রাখো: শূন্য row-এর (বা শুধু NULL-এর) উপর `SUM` 0 নয়, NULL দেয় — সংখ্যা দরকার হলে `COALESCE(SUM(x), 0)` দিয়ে মুড়ে দাও।

            Engine-এর খুঁটিনাটি: PostgreSQL, MySQL আর SQLite এখানে ভগ্নাংশসহ গড় দেয় (round করে 433.33), কিন্তু SQL Server-এ `INT` column-এর `AVG` integer দেয় (433) — সেখানে `AVG(CAST(bonus AS DECIMAL(10,2)))` ব্যবহার করো।
        """,
        tip_en=r"""Explain each column separately in one breath, then mention the `COALESCE` fix — it shows you think about business meaning, not just syntax.""",
        tip_bn=r"""প্রতিটা column আলাদা করে এক নিঃশ্বাসে ব্যাখ্যা করো, তারপর `COALESCE` দিয়ে সমাধানের কথা বলো — এতে বোঝা যায় তুমি শুধু syntax নয়, business-এর অর্থ নিয়েও ভাবো।""",
        related=["sql-006"],
        refs=[PG_AGG, PG_AGG_TUT],
    ),
    # ------------------------------------------------------------------ sql-006
    Q(
        id="sql-006", sub="NULL & Three-Valued Logic", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["null", "three-valued-logic", "where", "is-distinct-from"],
        ver="Version-independent (ISO SQL)", vs=False, status="stable",
        q_en=r"""How many rows does the final `SELECT` count?""",
        q_bn=r"""শেষ `SELECT` কতগুলো row গুনবে?""",
        code=r"""
            CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(50), city VARCHAR(50));
            INSERT INTO customers (id, name, city) VALUES
              (1, 'Rahim',  'Dhaka'),
              (2, 'Karim',  'Sylhet'),
              (3, 'Nadia',  NULL),
              (4, 'Sumi',   'Dhaka'),
              (5, 'Tanvir', NULL);

            SELECT COUNT(*) AS cnt FROM customers WHERE city <> 'Dhaka';
        """,
        lang="sql",
        output=r"""
             cnt
            -----
               1
        """,
        options=[("1", "1"), ("3", "3"), ("2", "2"), ("0", "0")],
        correct=0,
        a_en=r"""**1** — only Karim (Sylhet). For Nadia and Tanvir, `NULL <> 'Dhaka'` is **UNKNOWN**, not TRUE, and `WHERE` keeps only rows where the condition is TRUE.""",
        a_bn=r"""**1** — শুধু Karim (Sylhet)। Nadia আর Tanvir-এর ক্ষেত্রে `NULL <> 'Dhaka'`-এর ফল **UNKNOWN**, TRUE নয়, আর `WHERE` শুধু সেসব row রাখে যেখানে condition TRUE।""",
        ex_en=r"""
            SQL uses three-valued logic: TRUE, FALSE, UNKNOWN. Any comparison with NULL (`=`, `<>`, `<`, even `NULL = NULL`) is UNKNOWN. The tempting answer is 3 — "NULL isn't Dhaka, so it should count".

            To include unknown cities:
            - `WHERE city IS NULL OR city <> 'Dhaka'` → 3
            - `WHERE city IS DISTINCT FROM 'Dhaka'` → 3 (standard SQL; supported by PostgreSQL, SQLite, SQL Server 2022+; MySQL uses `NOT (city <=> 'Dhaka')`)

            Related traps: `NOT IN (subquery)` returns nothing if the subquery contains a NULL, and `CHECK` constraints *pass* on UNKNOWN.
        """,
        ex_bn=r"""
            SQL three-valued logic ব্যবহার করে: TRUE, FALSE, UNKNOWN। NULL-এর সাথে যেকোনো তুলনা (`=`, `<>`, `<`, এমনকি `NULL = NULL`) UNKNOWN। লোভনীয় উত্তর 3 — "NULL তো Dhaka না, তাহলে গোনা উচিত"।

            অজানা city-গুলোও ধরতে চাইলে:
            - `WHERE city IS NULL OR city <> 'Dhaka'` → 3
            - `WHERE city IS DISTINCT FROM 'Dhaka'` → 3 (standard SQL; PostgreSQL, SQLite, SQL Server 2022+ support করে; MySQL-এ `NOT (city <=> 'Dhaka')`)

            সম্পর্কিত ফাঁদ: subquery-তে একটা NULL থাকলে `NOT IN (subquery)` কিছুই return করে না, আর UNKNOWN হলে `CHECK` constraint *pass* করে যায়।
        """,
        tip_en=r"""Say "three-valued logic" by name and show the `IS DISTINCT FROM` fix. Linking it to the `NOT IN` + NULL trap is a strong follow-through.""",
        tip_bn=r""""Three-valued logic" নাম ধরে বলো আর `IS DISTINCT FROM` দিয়ে সমাধান দেখাও। এটাকে `NOT IN` + NULL ফাঁদের সাথে যুক্ত করলে উত্তর আরও জোরালো হয়।""",
        related=["sql-005", "sql-016"],
        refs=[PG_COMPARISON],
    ),
    # ------------------------------------------------------------------ sql-007
    Q(
        id="sql-007", sub="Constraints & Keys", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["primary-key", "foreign-key", "unique", "check", "candidate-key"],
        ver="Version-independent (ISO SQL)", vs=False, status="stable",
        q_en=r"""What are primary keys, foreign keys, and other constraints in SQL? Also explain candidate, composite, natural, and surrogate keys.""",
        q_bn=r"""SQL-এ primary key, foreign key আর অন্যান্য constraint কী? সাথে candidate, composite, natural আর surrogate key ব্যাখ্যা করো।""",
        a_en=r"""
            Constraints are rules the database enforces on every write:
            - **PRIMARY KEY:** uniquely identifies each row; unique + not null; one per table.
            - **FOREIGN KEY:** a column that must match a key in another table (referential integrity), with actions like `ON DELETE CASCADE / RESTRICT / SET NULL`.
            - **UNIQUE:** no duplicate values (e.g. email); usually allows NULLs.
            - **NOT NULL**, **CHECK** (e.g. `CHECK (price >= 0)`), and **DEFAULT**.

            Key vocabulary:
            - **Candidate key:** any minimal set of columns that could uniquely identify a row (e.g. `id`, `email`, `nid_number`). One is chosen as the primary key; the others are alternate keys (enforce them with `UNIQUE`).
            - **Composite key:** made of several columns, e.g. `(order_id, product_id)` in `order_items`.
            - **Natural key:** a real-world value (email, NID). **Surrogate key:** a meaningless generated id (identity/UUID). I usually use a surrogate primary key plus `UNIQUE` constraints on the natural keys.
        """,
        a_bn=r"""
            Constraint হলো এমন নিয়ম যা database প্রতিটা write-এ enforce করে:
            - **PRIMARY KEY:** প্রতিটা row-কে আলাদাভাবে চেনায়; unique + not null; table-প্রতি একটা।
            - **FOREIGN KEY:** এমন column যার value অন্য table-এর key-এর সাথে মিলতেই হবে (referential integrity), সাথে `ON DELETE CASCADE / RESTRICT / SET NULL`-এর মতো action।
            - **UNIQUE:** কোনো duplicate value চলবে না (যেমন email); সাধারণত NULL রাখা যায়।
            - **NOT NULL**, **CHECK** (যেমন `CHECK (price >= 0)`) আর **DEFAULT**।

            Key-এর পরিভাষা:
            - **Candidate key:** column-এর এমন যেকোনো ন্যূনতম set যা একটা row-কে আলাদাভাবে চিনতে পারে (যেমন `id`, `email`, `nid_number`)। এর একটাকে primary key বানানো হয়; বাকিগুলো alternate key (`UNIQUE` দিয়ে enforce করো)।
            - **Composite key:** একাধিক column মিলে তৈরি, যেমন `order_items`-এ `(order_id, product_id)`।
            - **Natural key:** বাস্তব জগতের value (email, NID)। **Surrogate key:** অর্থহীন generated id (identity/UUID)। আমি সাধারণত surrogate primary key রাখি, আর natural key-গুলোতে `UNIQUE` constraint দিই।
        """,
        ex_en=r"""
            - **Why enforce in the database, not only in code?** Multiple apps, scripts, admin fixes, and race conditions bypass application checks. A `UNIQUE` constraint is the only reliable way to prevent duplicate emails under concurrency.
            - Natural keys can change (people change emails/phones) — changing a primary key ripples through every foreign key. That's the main argument for surrogate keys.
            - A **super key** is any set of columns that uniquely identifies rows (a candidate key is a minimal super key) — a common viva definition.
            - Database differences: MySQL enforces `CHECK` only since 8.0.16 (older versions parsed and ignored it); SQL Server allows only one NULL in a `UNIQUE` column, while PostgreSQL allows many by default.
        """,
        ex_bn=r"""
            - **শুধু code-এ না রেখে database-এ কেন enforce করব?** একাধিক app, script, admin-এর হাতে করা fix আর race condition — সবাই application-এর check এড়িয়ে যেতে পারে। Concurrency-র মধ্যে duplicate email আটকানোর একমাত্র নির্ভরযোগ্য উপায় `UNIQUE` constraint।
            - Natural key বদলাতে পারে (মানুষ email/phone বদলায়) — primary key বদলালে সেটা প্রতিটা foreign key-তে ছড়িয়ে পড়ে। Surrogate key-এর পক্ষে এটাই প্রধান যুক্তি।
            - **Super key** হলো column-এর এমন যেকোনো set যা row-কে আলাদাভাবে চেনায় (candidate key হলো ন্যূনতম super key) — viva-তে প্রায়ই জিজ্ঞেস করা সংজ্ঞা।
            - Database-ভেদে পার্থক্য: MySQL `CHECK` enforce করে কেবল 8.0.16 থেকে (পুরনো version parse করে উপেক্ষা করত); SQL Server একটা `UNIQUE` column-এ মাত্র একটা NULL রাখতে দেয়, আর PostgreSQL default-ভাবে অনেকগুলো রাখতে দেয়।
        """,
        tip_en=r"""Define each key with a concrete example from one schema (e.g. users/orders). Ending with "surrogate PK + UNIQUE natural keys" shows a practical design opinion.""",
        tip_bn=r"""একটা schema (যেমন users/orders) থেকে concrete উদাহরণ দিয়ে প্রতিটা key-এর সংজ্ঞা দাও। শেষে "surrogate PK + UNIQUE natural key" বললে একটা practical design মতামত দেখানো হয়।""",
        mist_en=r"""Confusing a candidate key with a foreign key, or relying only on application validation for uniqueness.""",
        mist_bn=r"""Candidate key আর foreign key গুলিয়ে ফেলা, অথবা uniqueness-এর জন্য শুধু application validation-এর উপর ভরসা করা।""",
        code=r"""
            CREATE TABLE users (
              id          INT PRIMARY KEY,                    -- surrogate primary key
              email       VARCHAR(255) NOT NULL UNIQUE,       -- natural key, alternate key
              nid_number  VARCHAR(17) UNIQUE,
              created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE order_items (
              order_id    INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
              product_id  INT NOT NULL REFERENCES products(id),
              quantity    INT NOT NULL CHECK (quantity > 0),
              unit_price  NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
              PRIMARY KEY (order_id, product_id)              -- composite key
            );
        """,
        lang="sql",
        follow=[
            ("What do `ON DELETE CASCADE`, `RESTRICT`, and `SET NULL` do?", "`ON DELETE CASCADE`, `RESTRICT` আর `SET NULL` কী করে?"),
            ("Natural or surrogate primary key for a `users` table — which and why?", "`users` table-এর জন্য natural নাকি surrogate primary key — কোনটা আর কেন?"),
        ],
        related=["sql-011", "sql-032"],
        refs=[PG_CONSTRAINTS],
    ),
    # ------------------------------------------------------------------ sql-008
    Q(
        id="sql-008", sub="Self Join", diff="easy", type="query",
        prio="high", market="both", mins=4,
        tags=["self-join", "employees", "managers", "aliases"],
        ver="Version-independent (ISO SQL; output shown from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""The `employees` table stores each employee's `manager_id` (which is another employee's `id`). Find every employee who earns **more than their direct manager**, showing both names and salaries.""",
        q_bn=r"""`employees` table-এ প্রতিটা employee-এর `manager_id` রাখা আছে (যেটা আরেকজন employee-এর `id`)। যেসব employee তাদের **সরাসরি manager-এর চেয়ে বেশি** বেতন পায় তাদের বের করো — দুজনেরই নাম আর বেতন দেখাও।""",
        setup=r"""
            CREATE TABLE employees (
              id         INT PRIMARY KEY,
              name       VARCHAR(50) NOT NULL,
              salary     INT NOT NULL,
              manager_id INT REFERENCES employees(id)
            );

            INSERT INTO employees (id, name, salary, manager_id) VALUES
              (1, 'Shafiq', 200000, NULL),
              (2, 'Mitu',   120000, 1),
              (3, 'Rafi',    90000, 1),
              (4, 'Joy',    125000, 2),
              (5, 'Lina',    85000, 2),
              (6, 'Omar',    95000, 3),
              (7, 'Puja',    70000, 3);
        """,
        code=r"""
            SELECT e.name   AS employee,
                   e.salary AS salary,
                   m.name   AS manager,
                   m.salary AS manager_salary
            FROM employees e
            JOIN employees m ON m.id = e.manager_id
            WHERE e.salary > m.salary
            ORDER BY e.name;
        """,
        lang="sql",
        output=r"""
             employee | salary | manager | manager_salary
            ----------+--------+---------+----------------
             Joy      | 125000 | Mitu    |         120000
             Omar     |  95000 | Rafi    |          90000
        """,
        a_en=r"""
            A **self join** treats the same table as two roles using aliases: `e` is the employee, `m` is the manager. The join condition `m.id = e.manager_id` attaches each employee to their manager's row, and then `WHERE e.salary > m.salary` compares the two salaries on the same result row.

            Joy (125,000) earns more than Mitu (120,000), and Omar (95,000) more than Rafi (90,000). Shafiq has no manager (`manager_id` is NULL), so the inner join drops him — which is correct here because he has no one to compare against.
        """,
        a_bn=r"""
            **Self join** alias দিয়ে একই table-কে দুটো ভূমিকায় দেখে: `e` হলো employee, `m` হলো manager। Join condition `m.id = e.manager_id` প্রতিটা employee-কে তার manager-এর row-এর সাথে জুড়ে দেয়, তারপর `WHERE e.salary > m.salary` একই result row-এ দুটো বেতন তুলনা করে।

            Joy (১,২৫,০০০) Mitu-র (১,২০,০০০) চেয়ে বেশি পায়, আর Omar (৯৫,০০০) Rafi-র (৯০,০০০) চেয়ে বেশি। Shafiq-এর কোনো manager নেই (`manager_id` NULL), তাই inner join তাকে বাদ দেয় — এখানে সেটাই ঠিক, কারণ তুলনা করার কেউ নেই।
        """,
        ex_en=r"""
            - Use `LEFT JOIN` instead when you want to list *all* employees with their manager's name (the CEO then shows a NULL manager).
            - Self joins only go one level. For "everyone under Mitu at any depth" you need a **recursive CTE**.
            - Aliases are mandatory here — without them the database can't tell which copy of `employees` a column refers to.
            - Index `manager_id` on large tables: it's used both by this join and by the foreign-key checks when a manager row is deleted.
        """,
        ex_bn=r"""
            - সব employee-কে তাদের manager-এর নামসহ দেখাতে চাইলে এর বদলে `LEFT JOIN` ব্যবহার করো (তখন CEO-র manager NULL দেখাবে)।
            - Self join শুধু এক ধাপ যায়। "যেকোনো গভীরতায় Mitu-র অধীনে থাকা সবাই" বের করতে **recursive CTE** লাগে।
            - এখানে alias বাধ্যতামূলক — না দিলে database বুঝতে পারে না column-টা `employees`-এর কোন copy থেকে আসছে।
            - বড় table-এ `manager_id`-তে index দাও: এই join আর কোনো manager-এর row delete করার সময় foreign-key check — দুটোতেই এটা কাজে লাগে।
        """,
        tip_en=r"""Name the aliases by role (`e` employee, `m` manager) and say the join condition out loud — it shows you understand the direction of the relationship. Mention why the CEO disappears.""",
        tip_bn=r"""Alias-গুলোর নাম ভূমিকা অনুযায়ী দাও (`e` employee, `m` manager) আর join condition জোরে বলো — এতে বোঝা যায় তুমি সম্পর্কের দিকটা বুঝেছ। CEO কেন বাদ পড়ল সেটাও বলো।""",
        mist_en=r"""Reversing the join condition (`e.id = m.manager_id`), which compares managers with their reports the wrong way around.""",
        mist_bn=r"""Join condition উল্টে দেওয়া (`e.id = m.manager_id`), যাতে manager আর তার অধীনস্থদের তুলনা উল্টো দিক থেকে হয়।""",
        follow=[
            ("List every employee with their manager's name, including the CEO.", "CEO-সহ প্রত্যেক employee-কে তার manager-এর নামসহ দেখাও।"),
            ("How would you find all employees under Mitu at any level?", "যেকোনো স্তরে Mitu-র অধীনে থাকা সব employee কীভাবে বের করবে?"),
        ],
        related=["sql-002", "sql-023"],
        refs=[PG_JOIN_TUT, SQLITE_SELECT],
    ),
]

if __name__ == "__main__":
    save("sql", "b1", QUESTIONS)
