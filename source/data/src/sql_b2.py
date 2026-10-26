# SQL batch 2 — sql-009 … sql-016
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_TRUNCATE = ("PostgreSQL docs — TRUNCATE", "https://www.postgresql.org/docs/current/sql-truncate.html")
PG_DELETE = ("PostgreSQL docs — DELETE", "https://www.postgresql.org/docs/current/sql-delete.html")
PG_TX_TUT = ("PostgreSQL docs — Transactions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-transactions.html")
PG_WAL = ("PostgreSQL docs — Write-Ahead Logging", "https://www.postgresql.org/docs/current/wal-intro.html")
MS_NORMALIZATION = ("Microsoft Learn — Database normalization description", "https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description")
WIKI_NORMALIZATION = ("Wikipedia — Database normalization", "https://en.wikipedia.org/wiki/Database_normalization")
PG_WINDOW_FUNCS = ("PostgreSQL docs — Window Functions", "https://www.postgresql.org/docs/current/functions-window.html")
PG_WINDOW_TUT = ("PostgreSQL docs — Window Functions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-window.html")
SQLITE_WINDOW = ("SQLite — Window Functions", "https://www.sqlite.org/windowfunctions.html")
PG_SUBQUERY = ("PostgreSQL docs — Subquery Expressions (EXISTS, IN, NOT IN)", "https://www.postgresql.org/docs/current/functions-subquery.html")
PG_JOIN_TUT = ("PostgreSQL docs — Joins Between Tables", "https://www.postgresql.org/docs/current/tutorial-join.html")

QUESTIONS = [
    # ------------------------------------------------------------------ sql-009
    Q(
        id="sql-009", sub="DELETE vs TRUNCATE vs DROP", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["delete", "truncate", "drop", "ddl", "dml"],
        ver="Version-independent (behaviour varies by database)", vs=False, status="stable",
        q_en=r"""Which statement about `DELETE`, `TRUNCATE`, and `DROP TABLE` is correct?""",
        q_bn=r"""`DELETE`, `TRUNCATE` আর `DROP TABLE` নিয়ে কোন কথাটা সঠিক?""",
        options=[
            ("`TRUNCATE` removes the rows and the table definition, while `DROP` removes only the rows.",
             "`TRUNCATE` row আর table definition দুটোই মুছে দেয়, আর `DROP` শুধু row মোছে।"),
            ("`DELETE` without `WHERE` removes rows one by one (row-level delete triggers fire), `TRUNCATE` empties the table quickly without scanning rows, and `DROP TABLE` removes the table itself.",
             "`WHERE` ছাড়া `DELETE` row-গুলো একটা একটা করে মোছে (row-level delete trigger চলে), `TRUNCATE` row scan না করে দ্রুত table খালি করে, আর `DROP TABLE` table-টাই মুছে ফেলে।"),
            ("`TRUNCATE` accepts a `WHERE` clause and removes the selected rows faster than `DELETE`.",
             "`TRUNCATE` `WHERE` clause নেয় আর বাছাই করা row `DELETE`-এর চেয়ে দ্রুত মোছে।"),
            ("`DELETE` can never be rolled back, while `TRUNCATE` always can.",
             "`DELETE` কখনো rollback করা যায় না, আর `TRUNCATE` সবসময় rollback করা যায়।"),
        ],
        correct=1,
        a_en=r"""The second option. `DELETE` is DML: it can filter with `WHERE`, removes rows individually, and fires row-level triggers. `TRUNCATE` removes **all** rows at once by deallocating the table's storage (no `WHERE`, no per-row work). `DROP TABLE` deletes the table definition, its data, indexes, and constraints.""",
        a_bn=r"""দ্বিতীয় option। `DELETE` হলো DML: `WHERE` দিয়ে filter করা যায়, row আলাদা আলাদাভাবে মোছে, আর row-level trigger চালায়। `TRUNCATE` table-এর storage ছেড়ে দিয়ে একবারে **সব** row মোছে (`WHERE` নেই, প্রতি row-এর কাজ নেই)। `DROP TABLE` table definition, data, index আর constraint সব মুছে ফেলে।""",
        quick_en=r"""`DELETE` removes rows one by one, can use `WHERE`, and fires row-level triggers; `TRUNCATE` empties the whole table at once without scanning rows; `DROP TABLE` removes the table itself, with its data, indexes and constraints.""",
        quick_bn=r"""`DELETE` row ধরে ধরে মোছে, `WHERE` নিতে পারে আর row-level trigger চালায়; `TRUNCATE` row scan না করে পুরো table একবারে খালি করে; `DROP TABLE` table-টাই মুছে দেয়, তার data, index আর constraint-সহ।""",
        ex_en=r"""
            Option D is the tempting trap, and it's backwards *and* database-dependent:
            - `DELETE` inside a transaction can always be rolled back.
            - `TRUNCATE` is transactional in PostgreSQL (can be rolled back), but in MySQL and Oracle it's treated as DDL with an implicit commit, so it **can't** be rolled back there.

            Other differences worth mentioning:
            - `TRUNCATE` doesn't fire `ON DELETE` triggers, and fails if another table's foreign key references the table (PostgreSQL offers `TRUNCATE ... CASCADE`).
            - `TRUNCATE` can reset identity/auto-increment counters (`RESTART IDENTITY` in PostgreSQL; MySQL resets `AUTO_INCREMENT` automatically).
            - A big `DELETE` writes a log record per row and, in PostgreSQL, leaves dead tuples for VACUUM — use `TRUNCATE` (or drop a partition) to empty large tables.
        """,
        ex_bn=r"""
            Option D হলো লোভনীয় ফাঁদ, আর এটা উল্টো *এবং* database-নির্ভর:
            - Transaction-এর ভেতরে `DELETE` সবসময় rollback করা যায়।
            - PostgreSQL-এ `TRUNCATE` transactional (rollback করা যায়), কিন্তু MySQL আর Oracle-এ এটাকে implicit commit-সহ DDL ধরা হয়, তাই সেখানে rollback **করা যায় না**।

            আরও কিছু পার্থক্য যা বলার মতো:
            - `TRUNCATE` `ON DELETE` trigger চালায় না, আর অন্য table-এর foreign key এই table-কে refer করলে fail করে (PostgreSQL-এ `TRUNCATE ... CASCADE` আছে)।
            - `TRUNCATE` identity/auto-increment counter reset করতে পারে (PostgreSQL-এ `RESTART IDENTITY`; MySQL নিজে থেকেই `AUTO_INCREMENT` reset করে)।
            - বড় `DELETE` প্রতিটা row-এর জন্য log record লেখে, আর PostgreSQL-এ VACUUM-এর জন্য dead tuple রেখে যায় — বড় table খালি করতে `TRUNCATE` (বা partition drop) ব্যবহার করো।
        """,
        tip_en=r"""Give the three-way difference in one sentence each, then add the rollback nuance across databases — that detail separates memorised answers from real understanding.""",
        tip_bn=r"""তিনটার পার্থক্য এক বাক্যে করে বলো, তারপর বিভিন্ন database-এ rollback-এর সূক্ষ্ম পার্থক্যটা যোগ করো — এই খুঁটিনাটিই মুখস্থ উত্তর আর আসল বোঝাপড়ার পার্থক্য গড়ে দেয়।""",
        related=["sql-017"],
        refs=[PG_TRUNCATE, PG_DELETE],
    ),
    # ------------------------------------------------------------------ sql-010
    Q(
        id="sql-010", sub="Transactions & ACID", diff="easy", type="scenario",
        prio="high", market="both", mins=4,
        tags=["transactions", "acid", "commit", "rollback", "bank-transfer"],
        ver="Version-independent (ISO SQL)", vs=False, status="stable",
        q_en=r"""During a money transfer, the database server crashes right after debiting 500 from account A but before crediting account B. How do transactions and the ACID properties prevent the money from disappearing? Write the SQL you would use.""",
        q_bn=r"""টাকা transfer করার সময় account A থেকে 500 কেটে নেওয়ার ঠিক পরে, কিন্তু account B-তে জমা হওয়ার আগে database server crash করল। Transaction আর ACID property কীভাবে টাকা হারিয়ে যাওয়া ঠেকায়? তুমি যে SQL ব্যবহার করবে সেটা লেখো।""",
        a_en=r"""
            I wrap the debit, the credit, and the transfer record in **one transaction**. Until `COMMIT` succeeds, none of the changes are permanent. If the server crashes in the middle, crash recovery replays the write-ahead log and treats the unfinished transaction as aborted (PostgreSQL simply never marks it committed, so its row versions stay invisible; engines like InnoDB or Oracle roll it back with their undo logs). After restart account A still has its 500 — as if the transfer never started.

            ACID in this example:
            - **Atomicity:** debit and credit happen together or not at all.
            - **Consistency:** constraints (e.g. `CHECK (balance >= 0)`, foreign keys) hold before and after.
            - **Isolation:** other transactions don't see the half-done state (A debited, B not yet credited).
            - **Durability:** once `COMMIT` returns, the transfer survives a crash or power loss, because the log is flushed to disk first.
        """,
        a_bn=r"""
            আমি debit, credit আর transfer record — তিনটাকেই **একটা transaction**-এ মুড়ে দিই। `COMMIT` সফল না হওয়া পর্যন্ত কোনো পরিবর্তন স্থায়ী হয় না। মাঝপথে server crash করলে crash recovery write-ahead log replay করে আর অসমাপ্ত transaction-টাকে aborted ধরে (PostgreSQL এটাকে কখনো committed হিসেবে চিহ্নিতই করে না, তাই এর row version-গুলো অদৃশ্য থাকে; InnoDB বা Oracle-এর মতো engine undo log দিয়ে rollback করে)। তাই restart-এর পর account A-তে তার 500 থেকেই যায় — যেন transfer শুরুই হয়নি।

            এই উদাহরণে ACID:
            - **Atomicity:** debit আর credit একসাথে হয়, নয়তো একটাও হয় না।
            - **Consistency:** আগে-পরে constraint (যেমন `CHECK (balance >= 0)`, foreign key) ঠিক থাকে।
            - **Isolation:** অন্য transaction অর্ধেক-হওয়া অবস্থা দেখে না (A থেকে কাটা হয়েছে, B-তে এখনো জমা হয়নি)।
            - **Durability:** `COMMIT` return করার পর crash বা বিদ্যুৎ চলে গেলেও transfer টিকে থাকে, কারণ log আগে disk-এ flush হয়।
        """,
        quick_en=r"""Put the debit, the credit and the transfer record in one transaction. If the server crashes before `COMMIT`, recovery treats it as aborted, so account A keeps its money; once `COMMIT` returns, the change survives a crash. That is atomicity and durability, with consistency and isolation around it.""",
        quick_bn=r"""Debit, credit আর transfer record একটাই transaction-এ রাখো। `COMMIT`-এর আগে server crash করলে recovery সেটাকে aborted ধরে, তাই account A-র টাকা থেকে যায়; আর `COMMIT` return করার পরে change crash-এও টিকে থাকে। এটাই atomicity আর durability, সাথে consistency আর isolation।""",
        ex_en=r"""
            - Most databases run in **autocommit** mode by default: each statement commits on its own. Without an explicit transaction, the debit would be committed alone — exactly the bug in this scenario.
            - The guard `AND balance >= 500` plus checking the affected-row count prevents overdrafts even with concurrent transfers (the `UPDATE` locks the row).
            - On any application error, send `ROLLBACK`. Keep transactions short and never wait for user input or slow external API calls inside one — they hold locks.
            - Syntax differs slightly: standard `START TRANSACTION` (PostgreSQL, MySQL); `BEGIN` also works in PostgreSQL and MySQL and is the only form SQLite accepts; SQL Server uses `BEGIN TRANSACTION`.
            - Concurrency anomalies and isolation levels are the next layer of this topic.
        """,
        ex_bn=r"""
            - বেশিরভাগ database default-ভাবে **autocommit** mode-এ চলে: প্রতিটা statement নিজে নিজে commit হয়। Explicit transaction না থাকলে debit-টা একাই commit হয়ে যেত — এই scenario-র ঠিক সেই bug।
            - `AND balance >= 500` guard আর কতগুলো row affected হলো সেটা check করা — concurrent transfer-এর মধ্যেও overdraft আটকায় (`UPDATE` row lock করে)।
            - Application-এ যেকোনো error হলে `ROLLBACK` পাঠাও। Transaction ছোট রাখো, আর এর ভেতরে কখনো user input বা ধীর external API call-এর জন্য অপেক্ষা কোরো না — এগুলো lock ধরে রাখে।
            - Syntax একটু আলাদা: standard `START TRANSACTION` (PostgreSQL, MySQL); PostgreSQL আর MySQL-এ `BEGIN`-ও চলে, আর SQLite শুধু `BEGIN`-ই মানে; SQL Server-এ `BEGIN TRANSACTION`।
            - Concurrency anomaly আর isolation level এই বিষয়ের পরের স্তর।
        """,
        tip_en=r"""Map each ACID letter to the transfer example rather than reciting definitions. Mentioning autocommit as the root cause of the bug shows practical insight.""",
        tip_bn=r"""সংজ্ঞা মুখস্থ না বলে ACID-এর প্রতিটা অক্ষরকে transfer-এর উদাহরণের সাথে মেলাও। Bug-এর মূল কারণ হিসেবে autocommit-এর কথা বললে practical বোঝাপড়া দেখা যায়।""",
        mist_en=r"""Saying "Consistency" means replicas are in sync (that's the CAP-theorem meaning, not ACID), or running the two `UPDATE`s as separate autocommitted statements.""",
        mist_bn=r""""Consistency" মানে replica-গুলো sync-এ আছে বলা (ওটা CAP theorem-এর অর্থ, ACID-এর নয়), অথবা দুটো `UPDATE` আলাদা autocommit statement হিসেবে চালানো।""",
        code=r"""
            START TRANSACTION;          -- SQLite: BEGIN;  SQL Server: BEGIN TRANSACTION;

            UPDATE accounts
               SET balance = balance - 500
             WHERE id = 1 AND balance >= 500;
            -- application: if 0 rows were updated -> ROLLBACK (insufficient funds)

            UPDATE accounts
               SET balance = balance + 500
             WHERE id = 2;

            INSERT INTO transfers (from_account, to_account, amount)
            VALUES (1, 2, 500);

            COMMIT;                     -- on any error: ROLLBACK;
        """,
        lang="sql",
        follow=[
            ("What happens if two transfers from the same account run at the same time?", "একই account থেকে দুটো transfer একসাথে চললে কী হয়?"),
            ("What is autocommit, and how do you turn it off in your client?", "Autocommit কী, আর তোমার client-এ এটা কীভাবে বন্ধ করো?"),
        ],
        related=["sql-029"],
        refs=[PG_TX_TUT, PG_WAL],
    ),
    # ------------------------------------------------------------------ sql-011
    Q(
        id="sql-011", sub="Normalization", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=3,
        tags=["normalization", "2nf", "3nf", "bcnf", "denormalization"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""In the table below, `product_name` depends only on `product_id`, while `quantity` and `unit_price` (the price charged in that order) depend on the whole key. Which normal form does this table violate?""",
        q_bn=r"""নিচের table-এ `product_name` শুধু `product_id`-এর উপর নির্ভর করে, আর `quantity` ও `unit_price` (ওই order-এ নেওয়া দাম) পুরো key-এর উপর নির্ভর করে। Table-টা কোন normal form ভাঙছে?""",
        code=r"""
            CREATE TABLE order_items (
              order_id     INT,
              product_id   INT,
              quantity     INT,
              unit_price   NUMERIC(10,2),   -- price charged in this order
              product_name VARCHAR(100),
              PRIMARY KEY (order_id, product_id)
            );
        """,
        lang="sql",
        options=[
            ("First Normal Form (1NF)", "First Normal Form (1NF)"),
            ("Second Normal Form (2NF)", "Second Normal Form (2NF)"),
            ("Third Normal Form (3NF), because of a transitive dependency", "Third Normal Form (3NF), transitive dependency-র কারণে"),
            ("None — the table is already in BCNF", "কোনোটাই না — table-টা আগে থেকেই BCNF-এ আছে"),
        ],
        correct=1,
        a_en=r"""**2NF.** The key is composite `(order_id, product_id)`, and `product_name` depends on only *part* of it (`product_id`) — a **partial dependency**. Fix: move `product_name` into a `products(product_id, product_name, ...)` table and keep only `product_id` in `order_items`.""",
        a_bn=r"""**2NF।** Key-টা composite `(order_id, product_id)`, আর `product_name` এর শুধু *একটা অংশের* (`product_id`) উপর নির্ভর করে — এটা **partial dependency**। সমাধান: `product_name`-কে একটা `products(product_id, product_name, ...)` table-এ সরাও, আর `order_items`-এ শুধু `product_id` রাখো।""",
        quick_en=r"""2NF. The key is `(order_id, product_id)`, and `product_name` depends on only part of it (`product_id`), which is a partial dependency. Move `product_name` into a `products` table.""",
        quick_bn=r"""2NF। Key হলো `(order_id, product_id)`, আর `product_name` তার শুধু একটা অংশের (`product_id`) ওপর নির্ভর করে, এটাই partial dependency। `product_name`-কে একটা `products` table-এ সরিয়ে নাও।""",
        ex_en=r"""
            The normal forms in one line each:
            - **1NF:** atomic values, no repeating groups (no comma-separated lists, no `phone1, phone2, phone3`). This table is fine there.
            - **2NF:** 1NF + no non-key column depends on only part of a composite key. Violated here.
            - **3NF:** 2NF + no **transitive** dependency (non-key → non-key), e.g. `customers(id, zip_code, city)` where `city` depends on `zip_code`. Option C is the tempting wrong answer because people mix up partial and transitive dependencies.
            - **BCNF:** every determinant must be a candidate key — a stricter 3NF that matters with overlapping candidate keys.

            Why it matters: with `product_name` repeated in every order line, renaming a product means updating thousands of rows (update anomaly), and the copies can disagree.

            Note that `unit_price` is **not** redundant: it records what the customer paid at that time, which can differ from today's catalogue price. Deliberate denormalization (snapshots, cached totals, reporting tables) is fine when you know why you're doing it.
        """,
        ex_bn=r"""
            এক লাইনে normal form-গুলো:
            - **1NF:** atomic value, কোনো repeating group নেই (comma-separated list নেই, `phone1, phone2, phone3` নেই)। এই table এখানে ঠিক আছে।
            - **2NF:** 1NF + কোনো non-key column composite key-এর শুধু একটা অংশের উপর নির্ভর করবে না। এখানে এটাই ভেঙেছে।
            - **3NF:** 2NF + কোনো **transitive** dependency নেই (non-key → non-key), যেমন `customers(id, zip_code, city)`, যেখানে `city` নির্ভর করে `zip_code`-এর উপর। Option C লোভনীয় ভুল উত্তর, কারণ অনেকে partial আর transitive dependency গুলিয়ে ফেলে।
            - **BCNF:** প্রতিটা determinant-কে candidate key হতে হবে — 3NF-এর কড়া রূপ, যা overlapping candidate key থাকলে গুরুত্বপূর্ণ।

            কেন গুরুত্বপূর্ণ: প্রতিটা order line-এ `product_name` বারবার থাকলে একটা product rename করতে হাজারো row update করতে হয় (update anomaly), আর copy-গুলো একে অপরের সাথে না-ও মিলতে পারে।

            খেয়াল করো, `unit_price` redundant **নয়**: এটা সেই সময়ে customer কত দিয়েছে তা রেকর্ড করে, যা আজকের catalogue দাম থেকে আলাদা হতে পারে। কেন করছ জানলে ইচ্ছাকৃত denormalization (snapshot, cached total, reporting table) ঠিক আছে।
        """,
        tip_en=r"""Name the dependency type ("partial dependency on a composite key"), then contrast with a 3NF transitive example. Bringing up the `unit_price` snapshot shows you understand when denormalization is intentional.""",
        tip_bn=r"""Dependency-র ধরনের নাম বলো ("composite key-এর উপর partial dependency"), তারপর 3NF-এর একটা transitive উদাহরণের সাথে তুলনা করো। `unit_price` snapshot-এর কথা তুললে বোঝা যায় তুমি জানো কখন denormalization ইচ্ছাকৃত।""",
        related=["sql-007", "sql-032"],
        refs=[MS_NORMALIZATION, WIKI_NORMALIZATION],
    ),
    # ------------------------------------------------------------------ sql-012
    Q(
        id="sql-012", sub="Ranking: Second-Highest Salary", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["dense-rank", "window-functions", "subquery", "nth-highest", "ties"],
        ver="Version-independent (SQL:2003 window functions; output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Find the employee(s) with the **second-highest salary**. Several employees can share the same salary, so return everyone at that salary level.""",
        q_bn=r"""**দ্বিতীয় সর্বোচ্চ বেতন** পাওয়া employee(-দের) বের করো। একাধিক employee-এর বেতন সমান হতে পারে, তাই ওই বেতন-স্তরের সবাইকে return করো।""",
        setup=r"""
            CREATE TABLE employees (
              id     INT PRIMARY KEY,
              name   VARCHAR(50) NOT NULL,
              salary INT NOT NULL
            );

            INSERT INTO employees (id, name, salary) VALUES
              (1, 'Ayesha',   95000),
              (2, 'Bilal',   120000),
              (3, 'Chandni', 120000),
              (4, 'Dipu',     87000),
              (5, 'Esha',     95000),
              (6, 'Farhan',   60000);
        """,
        code=r"""
            WITH ranked AS (
              SELECT name, salary,
                     DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_rank
              FROM employees
            )
            SELECT name, salary
            FROM ranked
            WHERE salary_rank = 2
            ORDER BY name;
        """,
        lang="sql",
        output=r"""
              name  | salary
            --------+--------
             Ayesha |  95000
             Esha   |  95000
        """,
        extra=[dict(lang="sql", label_en="Other approaches and the classic trap", label_bn="অন্য পদ্ধতি আর classic ফাঁদ", src=r"""
            -- value only (works everywhere, even without window functions) -> 95000
            SELECT MAX(salary) AS second_highest
            FROM employees
            WHERE salary < (SELECT MAX(salary) FROM employees);

            -- TRAP: ignores ties -> returns 120000 (Chandni), not the second-highest salary
            SELECT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;
            -- fix: SELECT DISTINCT salary ... ORDER BY salary DESC LIMIT 1 OFFSET 1;
            -- standard syntax: ... OFFSET 1 ROWS FETCH FIRST 1 ROW ONLY
        """), dict(lang="text", label_en="ROW_NUMBER vs RANK vs DENSE_RANK on this data", label_bn="এই data-য় ROW_NUMBER বনাম RANK বনাম DENSE_RANK", src=r"""
              name   | salary | row_number | rank | dense_rank
            ---------+--------+------------+------+------------
             Bilal   | 120000 |          1 |    1 |          1
             Chandni | 120000 |          2 |    1 |          1
             Ayesha  |  95000 |          3 |    3 |          2
             Esha    |  95000 |          4 |    3 |          2
             Dipu    |  87000 |          5 |    5 |          3
             Farhan  |  60000 |          6 |    6 |          4
        """)],
        a_en=r"""
            `DENSE_RANK()` numbers the **distinct salary levels** without gaps: 120000 → 1, 95000 → 2, 87000 → 3. Filtering `salary_rank = 2` returns everyone earning 95000 — Ayesha and Esha. The window function can't go in `WHERE` directly (it's computed after `WHERE`), so it's wrapped in a CTE.

            Why not the others?
            - `ROW_NUMBER()` gives every row a unique number, so "row 2" is Chandni (120000) — wrong with ties.
            - `RANK()` leaves gaps after ties (1, 1, **3**), so `RANK() = 2` returns nothing here.
            - `LIMIT 1 OFFSET 1` has the same problem as `ROW_NUMBER()`.

            For the N-th highest salary, just change `2` to `N`.
        """,
        a_bn=r"""
            `DENSE_RANK()` **আলাদা বেতন-স্তরগুলোকে** ফাঁক ছাড়াই নম্বর দেয়: 120000 → 1, 95000 → 2, 87000 → 3। `salary_rank = 2` filter করলে 95000 পাওয়া সবাই আসে — Ayesha আর Esha। Window function সরাসরি `WHERE`-এ বসানো যায় না (এটা `WHERE`-এর পরে হিসাব হয়), তাই CTE-তে মুড়ে নেওয়া হয়েছে।

            অন্যগুলো কেন নয়?
            - `ROW_NUMBER()` প্রতিটা row-কে আলাদা নম্বর দেয়, তাই "row 2" হলো Chandni (120000) — tie থাকলে ভুল।
            - `RANK()` tie-এর পরে ফাঁক রাখে (1, 1, **3**), তাই এখানে `RANK() = 2` কিছুই return করে না।
            - `LIMIT 1 OFFSET 1`-এরও `ROW_NUMBER()`-এর মতো একই সমস্যা।

            N-তম সর্বোচ্চ বেতনের জন্য শুধু `2`-কে `N` করে দাও।
        """,
        quick_en=r"""Use `DENSE_RANK() OVER (ORDER BY salary DESC)` in a CTE and filter `= 2`, which returns everyone at the second salary level. `ROW_NUMBER()` and `LIMIT 1 OFFSET 1` break with ties, and `RANK()` leaves a gap after ties.""",
        quick_bn=r"""একটা CTE-তে `DENSE_RANK() OVER (ORDER BY salary DESC)` হিসাব করে `= 2` দিয়ে filter করো, তাহলে দ্বিতীয় salary level-এর সবাই আসবে। Tie থাকলে `ROW_NUMBER()` আর `LIMIT 1 OFFSET 1` ভুল করে, আর `RANK()` tie-এর পরে একটা নম্বর বাদ দেয়।""",
        ex_en=r"""
            - **Edge case:** if everyone has the same salary, the `DENSE_RANK` query returns no rows, while the `MAX(...) WHERE salary < MAX(...)` version returns a single NULL. Clarify which behaviour the caller expects.
            - The `MAX` subquery version only returns the *value*; to get names you'd need `WHERE salary = (that subquery)`.
            - `LIMIT/OFFSET` is PostgreSQL/MySQL/SQLite syntax; the SQL standard (also supported by PostgreSQL, Oracle, SQL Server) is `OFFSET 1 ROWS FETCH FIRST 1 ROW ONLY`.
            - Window functions are available in PostgreSQL, MySQL 8+, SQL Server, Oracle, and SQLite 3.25+.
        """,
        ex_bn=r"""
            - **Edge case:** সবার বেতন সমান হলে `DENSE_RANK` query কোনো row দেয় না, আর `MAX(...) WHERE salary < MAX(...)` version একটা NULL দেয়। Caller কোন আচরণ চায় সেটা জিজ্ঞেস করে নাও।
            - `MAX` subquery version শুধু *value* দেয়; নাম পেতে হলে `WHERE salary = (ওই subquery)` লাগবে।
            - `LIMIT/OFFSET` হলো PostgreSQL/MySQL/SQLite syntax; SQL standard (PostgreSQL, Oracle, SQL Server-ও support করে) হলো `OFFSET 1 ROWS FETCH FIRST 1 ROW ONLY`।
            - Window function PostgreSQL, MySQL 8+, SQL Server, Oracle আর SQLite 3.25+-এ আছে।
        """,
        tip_en=r"""Ask "what about ties?" before writing anything — interviewers love that question. Then show the DENSE_RANK solution and explain the ROW_NUMBER/RANK/DENSE_RANK difference with the sample data.""",
        tip_bn=r"""কিছু লেখার আগেই জিজ্ঞেস করো "tie থাকলে কী হবে?" — interviewer এই প্রশ্নটা খুব পছন্দ করে। তারপর DENSE_RANK সমাধান দেখাও আর sample data দিয়ে ROW_NUMBER/RANK/DENSE_RANK-এর পার্থক্য বোঝাও।""",
        mist_en=r"""Using `ORDER BY salary DESC LIMIT 1 OFFSET 1` (fails with ties), or using `RANK()` and getting an empty result.""",
        mist_bn=r"""`ORDER BY salary DESC LIMIT 1 OFFSET 1` ব্যবহার করা (tie থাকলে ভুল হয়), অথবা `RANK()` ব্যবহার করে খালি ফলাফল পাওয়া।""",
        follow=[
            ("Return the third-highest salary in each department.", "প্রতিটা department-এর তৃতীয় সর্বোচ্চ বেতন বের করো।"),
            ("How would you solve this on a database without window functions?", "Window function নেই এমন database-এ এটা কীভাবে সমাধান করবে?"),
        ],
        related=["sql-013", "sql-025"],
        refs=[PG_WINDOW_FUNCS, PG_WINDOW_TUT, SQLITE_WINDOW],
    ),
    # ------------------------------------------------------------------ sql-013
    Q(
        id="sql-013", sub="Top-N per Group", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["row-number", "partition-by", "top-n", "window-functions"],
        ver="Version-independent (SQL:2003 window functions; output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Return the **top 2 highest-paid employees in each department** (department name, employee name, salary, and position). If two employees in a department have the same salary, break the tie alphabetically by name.""",
        q_bn=r"""**প্রতিটা department-এর সবচেয়ে বেশি বেতন পাওয়া ২ জন employee** বের করো (department-এর নাম, employee-এর নাম, বেতন আর অবস্থান)। একই department-এ দুজনের বেতন সমান হলে নামের বর্ণানুক্রমে tie ভাঙো।""",
        setup=r"""
            CREATE TABLE departments (
              id   INT PRIMARY KEY,
              name VARCHAR(30) NOT NULL
            );

            CREATE TABLE employees (
              id      INT PRIMARY KEY,
              name    VARCHAR(50) NOT NULL,
              dept_id INT NOT NULL REFERENCES departments(id),
              salary  INT NOT NULL
            );

            INSERT INTO departments (id, name) VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'HR');

            INSERT INTO employees (id, name, dept_id, salary) VALUES
              (1, 'Ayesha',  1,  95000),
              (2, 'Bilal',   1, 120000),
              (3, 'Chandni', 1,  87000),
              (4, 'Dipu',    2,  55000),
              (5, 'Esha',    2,  61000),
              (6, 'Farhan',  2,  61000),
              (7, 'Gazi',    2,  40000),
              (8, 'Hasan',   3,  52000);
        """,
        code=r"""
            WITH ranked AS (
              SELECT d.name AS department,
                     e.name AS employee,
                     e.salary,
                     ROW_NUMBER() OVER (PARTITION BY e.dept_id
                                        ORDER BY e.salary DESC, e.name) AS rn
              FROM employees e
              JOIN departments d ON d.id = e.dept_id
            )
            SELECT department, employee, salary, rn
            FROM ranked
            WHERE rn <= 2
            ORDER BY department, rn;
        """,
        lang="sql",
        output=r"""
             department  | employee | salary | rn
            -------------+----------+--------+----
             Engineering | Bilal    | 120000 |  1
             Engineering | Ayesha   |  95000 |  2
             HR          | Hasan    |  52000 |  1
             Sales       | Esha     |  61000 |  1
             Sales       | Farhan   |  61000 |  2
        """,
        extra=[dict(lang="text", label_en="Same query with DENSE_RANK() <= 2 (top 2 salary LEVELS instead of top 2 people)",
                    label_bn="একই query DENSE_RANK() <= 2 দিয়ে (শীর্ষ ২ জন মানুষ নয়, শীর্ষ ২টা বেতন-স্তর)", src=r"""
             department  | employee | salary | dr
            -------------+----------+--------+----
             Engineering | Bilal    | 120000 |  1
             Engineering | Ayesha   |  95000 |  2
             HR          | Hasan    |  52000 |  1
             Sales       | Esha     |  61000 |  1
             Sales       | Farhan   |  61000 |  1
             Sales       | Dipu     |  55000 |  2
        """)],
        a_en=r"""
            - `PARTITION BY e.dept_id` restarts the numbering for each department; `ORDER BY e.salary DESC, e.name` decides the order inside it, with the name as the tie-breaker the question asked for.
            - `ROW_NUMBER()` gives 1, 2, 3... with no duplicates, so `rn <= 2` returns **exactly two people** per department (or fewer — HR has only Hasan).
            - In Sales, Esha and Farhan both earn 61,000; the alphabetical tie-breaker makes Esha 1 and Farhan 2, and Dipu (55,000) is excluded.
            - The filter is applied in the outer query because window functions are evaluated after `WHERE`.
        """,
        a_bn=r"""
            - `PARTITION BY e.dept_id` প্রতিটা department-এর জন্য নম্বর আবার শুরু করে; `ORDER BY e.salary DESC, e.name` তার ভেতরের ক্রম ঠিক করে, প্রশ্ন অনুযায়ী নামকে tie-breaker রেখে।
            - `ROW_NUMBER()` 1, 2, 3... দেয়, কোনো duplicate নেই, তাই `rn <= 2` প্রতি department-এ **ঠিক দুজন মানুষ** দেয় (বা কম — HR-এ শুধু Hasan)।
            - Sales-এ Esha আর Farhan দুজনেই 61,000 পায়; বর্ণানুক্রমিক tie-breaker-এ Esha 1 আর Farhan 2, আর Dipu (55,000) বাদ পড়ে।
            - Filter-টা outer query-তে দেওয়া হয়েছে, কারণ window function `WHERE`-এর পরে evaluate হয়।
        """,
        quick_en=r"""Number rows with `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, name)` in a subquery or CTE, then keep `rn <= 2` in the outer query. The name breaks ties, and the filter sits outside because window functions run after `WHERE`.""",
        quick_bn=r"""Subquery বা CTE-তে `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, name)` দিয়ে নম্বর দাও, তারপর outer query-তে `rn <= 2` রাখো। Tie ভাঙে name দিয়ে, আর filter বাইরে রাখতে হয় কারণ window function `WHERE`-এর পরে চলে।""",
        ex_en=r"""
            - **Clarify the requirement:** "top 2 per department" can mean two *people* (`ROW_NUMBER`), or everyone in the top two *salary levels* (`DENSE_RANK`, see the extra output — Sales returns three people), or the top two with ties at the boundary included (`RANK`).
            - Without a deterministic tie-breaker, `ROW_NUMBER` may pick a different person between runs.
            - Performance on big tables: an index on `(dept_id, salary DESC)` helps. In PostgreSQL, a `LATERAL` subquery with `ORDER BY salary DESC LIMIT 2` per department can be much faster when there are few departments and many employees. PostgreSQL also has `DISTINCT ON` for the top-1 case.
            - Some databases offer `QUALIFY rn <= 2` (Snowflake, BigQuery, DuckDB) to filter window results without a subquery; it isn't available in PostgreSQL or MySQL.
        """,
        ex_bn=r"""
            - **Requirement পরিষ্কার করো:** "প্রতি department-এ শীর্ষ ২" মানে হতে পারে দুজন *মানুষ* (`ROW_NUMBER`), অথবা শীর্ষ দুটো *বেতন-স্তরের* সবাই (`DENSE_RANK`, extra output দেখো — Sales-এ তিনজন আসে), অথবা সীমানায় tie থাকলে তাদেরও রেখে শীর্ষ দুই (`RANK`)।
            - Deterministic tie-breaker না থাকলে `ROW_NUMBER` বিভিন্ন run-এ আলাদা মানুষকে বেছে নিতে পারে।
            - বড় table-এ performance: `(dept_id, salary DESC)`-এ index সাহায্য করে। PostgreSQL-এ department কম আর employee অনেক হলে প্রতি department-এর জন্য `ORDER BY salary DESC LIMIT 2`-সহ `LATERAL` subquery অনেক দ্রুত হতে পারে। Top-1-এর জন্য PostgreSQL-এ `DISTINCT ON`-ও আছে।
            - কিছু database-এ subquery ছাড়াই window result filter করার জন্য `QUALIFY rn <= 2` আছে (Snowflake, BigQuery, DuckDB); PostgreSQL বা MySQL-এ এটা নেই।
        """,
        tip_en=r"""Before writing the query, ask which tie semantics they want — then pick `ROW_NUMBER`, `RANK`, or `DENSE_RANK` accordingly. That clarifying question is often what the interviewer is waiting for.""",
        tip_bn=r"""Query লেখার আগে জিজ্ঞেস করো tie-এর ক্ষেত্রে কোন অর্থ চায় — তারপর সেই অনুযায়ী `ROW_NUMBER`, `RANK` বা `DENSE_RANK` বেছে নাও। Interviewer প্রায়ই ঠিক এই প্রশ্নটার অপেক্ষাতেই থাকে।""",
        mist_en=r"""Writing `WHERE ROW_NUMBER() OVER (...) <= 2` directly (not allowed), forgetting `PARTITION BY` (gives the top 2 overall), or omitting a tie-breaker.""",
        mist_bn=r"""সরাসরি `WHERE ROW_NUMBER() OVER (...) <= 2` লেখা (অনুমোদিত নয়), `PARTITION BY` ভুলে যাওয়া (তখন পুরো company-র শীর্ষ ২ আসে), অথবা tie-breaker না দেওয়া।""",
        follow=[
            ("How would you write this without window functions (e.g. MySQL 5.7)?", "Window function ছাড়া এটা কীভাবে লিখবে (যেমন MySQL 5.7-এ)?"),
            ("Return the latest order per customer.", "প্রতি customer-এর সর্বশেষ order বের করো।"),
        ],
        related=["sql-012", "sql-014"],
        refs=[PG_WINDOW_FUNCS, PG_WINDOW_TUT, SQLITE_WINDOW],
    ),
    # ------------------------------------------------------------------ sql-014
    Q(
        id="sql-014", sub="Running Totals", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["running-total", "window-functions", "sum-over", "window-frame"],
        ver="Version-independent (SQL:2003 window functions; output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Show each day's sales with a **running total per region** (cumulative sum from the region's first sale up to that day).""",
        q_bn=r"""প্রতিদিনের sale-এর সাথে **প্রতি region-এর running total** দেখাও (region-এর প্রথম sale থেকে ওই দিন পর্যন্ত cumulative যোগফল)।""",
        setup=r"""
            CREATE TABLE sales (
              id        INT PRIMARY KEY,
              region    VARCHAR(20) NOT NULL,
              sale_date DATE NOT NULL,
              amount    INT NOT NULL
            );

            INSERT INTO sales (id, region, sale_date, amount) VALUES
              (1, 'Dhaka', '2026-10-01', 500),
              (2, 'Dhaka', '2026-10-02', 300),
              (3, 'Dhaka', '2026-10-04', 700),
              (4, 'Ctg',   '2026-10-01', 400),
              (5, 'Ctg',   '2026-10-03', 250),
              (6, 'Ctg',   '2026-10-04', 100);
        """,
        code=r"""
            SELECT region,
                   sale_date,
                   amount,
                   SUM(amount) OVER (PARTITION BY region
                                     ORDER BY sale_date
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
            FROM sales
            ORDER BY region, sale_date;
        """,
        lang="sql",
        output=r"""
             region | sale_date  | amount | running_total
            --------+------------+--------+---------------
             Ctg    | 2026-10-01 |    400 |           400
             Ctg    | 2026-10-03 |    250 |           650
             Ctg    | 2026-10-04 |    100 |           750
             Dhaka  | 2026-10-01 |    500 |           500
             Dhaka  | 2026-10-02 |    300 |           800
             Dhaka  | 2026-10-04 |    700 |          1500
        """,
        a_en=r"""
            `SUM(amount) OVER (...)` is an aggregate used as a **window function**: unlike `GROUP BY`, it keeps every row and adds a computed column.
            - `PARTITION BY region` restarts the sum for each region (Ctg and Dhaka are independent).
            - `ORDER BY sale_date` defines the sequence inside each region.
            - `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` is the **frame**: sum from the first row of the partition up to the current one. For Dhaka: 500 → 500 + 300 = 800 → 800 + 700 = 1500.
        """,
        a_bn=r"""
            `SUM(amount) OVER (...)` হলো **window function** হিসেবে ব্যবহার করা একটা aggregate: `GROUP BY`-এর মতো row কমায় না, প্রতিটা row রেখে একটা হিসাব করা column যোগ করে।
            - `PARTITION BY region` প্রতিটা region-এর জন্য যোগফল আবার শুরু করে (Ctg আর Dhaka আলাদা)।
            - `ORDER BY sale_date` প্রতিটা region-এর ভেতরের ক্রম ঠিক করে।
            - `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` হলো **frame**: partition-এর প্রথম row থেকে current row পর্যন্ত যোগফল। Dhaka-র জন্য: 500 → 500 + 300 = 800 → 800 + 700 = 1500।
        """,
        quick_en=r"""Use `SUM(amount) OVER (PARTITION BY region ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`. Unlike `GROUP BY`, a window function keeps every row and adds the cumulative sum, restarting for each region.""",
        quick_bn=r"""`SUM(amount) OVER (PARTITION BY region ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` ব্যবহার করো। `GROUP BY`-এর মতো নয়, window function প্রতিটা row রেখে cumulative যোগফল যোগ করে, আর প্রতিটা region-এর জন্য আবার শুরু করে।""",
        ex_en=r"""
            - **Why spell out the frame?** With `ORDER BY` but no frame, the default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which treats rows with the same `sale_date` as **peers** and gives them all the same (combined) total. With one row per day it makes no difference, but with several sales on the same day it surprises people. `ROWS` counts physical rows.
            - Other useful frames: a 7-day moving average with `AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` (7 rows, assuming one row per day).
            - Missing days (Dhaka has no 10-03 row) simply don't appear — generate a calendar and `LEFT JOIN` if the report needs every day.
            - The old pre-window way was a correlated subquery (`SELECT SUM(...) WHERE s2.sale_date <= s.sale_date`), which is O(n²) and much slower.
        """,
        ex_bn=r"""
            - **Frame কেন স্পষ্ট করে লিখব?** `ORDER BY` থাকলে কিন্তু frame না দিলে default হয় `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, যেটা একই `sale_date`-এর row-গুলোকে **peer** ধরে সবাইকে একই (মিলিত) total দেয়। দিনে একটা row হলে পার্থক্য নেই, কিন্তু একই দিনে একাধিক sale থাকলে মানুষ অবাক হয়। `ROWS` physical row গোনে।
            - আরও কাজের frame: `AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` দিয়ে 7-দিনের moving average (৭টা row, ধরে নিচ্ছি দিনে একটা row)।
            - যেদিন sale নেই (Dhaka-র 10-03 row নেই) সেদিন আসেই না — report-এ প্রতিটা দিন লাগলে একটা calendar বানিয়ে `LEFT JOIN` করো।
            - Window function-এর আগের পুরনো পদ্ধতি ছিল correlated subquery (`SELECT SUM(...) WHERE s2.sale_date <= s.sale_date`), যেটা O(n²) আর অনেক ধীর।
        """,
        tip_en=r"""Explain the three parts of `OVER (...)` — partition, order, frame — and mention the RANGE-vs-ROWS default. That frame detail is what distinguishes a mid-level answer.""",
        tip_bn=r"""`OVER (...)`-এর তিনটা অংশ ব্যাখ্যা করো — partition, order, frame — আর RANGE বনাম ROWS default-এর কথা বলো। এই frame-এর খুঁটিনাটিই mid-level উত্তরকে আলাদা করে।""",
        mist_en=r"""Using `GROUP BY` (which collapses rows) for a running total, or forgetting `PARTITION BY` so the total runs across all regions.""",
        mist_bn=r"""Running total-এর জন্য `GROUP BY` ব্যবহার করা (যা row-গুলো এক করে ফেলে), অথবা `PARTITION BY` ভুলে যাওয়া যাতে সব region মিলিয়ে total চলতে থাকে।""",
        follow=[
            ("Add a 3-day moving average column.", "একটা 3-দিনের moving average column যোগ করো।"),
            ("What changes if there are two sales on the same day and you omit the frame clause?", "একই দিনে দুটো sale থাকলে আর frame clause না দিলে কী বদলায়?"),
        ],
        related=["sql-025", "sql-024"],
        refs=[PG_WINDOW_TUT, PG_WINDOW_FUNCS, SQLITE_WINDOW],
    ),
    # ------------------------------------------------------------------ sql-015
    Q(
        id="sql-015", sub="Correlated Subqueries", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["correlated-subquery", "avg", "window-functions", "employees"],
        ver="Version-independent (ISO SQL; output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""List the employees who earn **more than the average salary of their own department**.""",
        q_bn=r"""যেসব employee **নিজের department-এর গড় বেতনের চেয়ে বেশি** পায়, তাদের তালিকা বের করো।""",
        setup=r"""
            CREATE TABLE employees (
              id     INT PRIMARY KEY,
              name   VARCHAR(50) NOT NULL,
              dept   VARCHAR(30) NOT NULL,
              salary INT NOT NULL
            );

            INSERT INTO employees (id, name, dept, salary) VALUES
              (1, 'Ayesha',  'Engineering',  95000),
              (2, 'Bilal',   'Engineering', 120000),
              (3, 'Chandni', 'Engineering',  70000),
              (4, 'Dipu',    'Sales',        55000),
              (5, 'Esha',    'Sales',        61000),
              (6, 'Farhan',  'Sales',        40000),
              (7, 'Gazi',    'HR',           52000);
        """,
        code=r"""
            SELECT e.name, e.dept, e.salary
            FROM employees e
            WHERE e.salary > (
              SELECT AVG(e2.salary)
              FROM employees e2
              WHERE e2.dept = e.dept        -- correlated: refers to the outer row
            )
            ORDER BY e.dept, e.salary DESC;
        """,
        lang="sql",
        output=r"""
             name  |    dept     | salary
            -------+-------------+--------
             Bilal | Engineering | 120000
             Esha  | Sales       |  61000
             Dipu  | Sales       |  55000
        """,
        extra=[dict(lang="sql", label_en="Window-function version (one pass, can also show the average)",
                    label_bn="Window-function version (এক pass-এ, গড়-ও দেখানো যায়)", src=r"""
            SELECT name, dept, salary, dept_avg
            FROM (
              SELECT name, dept, salary,
                     ROUND(AVG(salary) OVER (PARTITION BY dept), 2) AS dept_avg
              FROM employees
            ) t
            WHERE salary > dept_avg
            ORDER BY dept, salary DESC;

            --  name  |    dept     | salary | dept_avg
            -- -------+-------------+--------+----------
            --  Bilal | Engineering | 120000 | 95000.00
            --  Esha  | Sales       |  61000 | 52000.00
            --  Dipu  | Sales       |  55000 | 52000.00
        """)],
        a_en=r"""
            A **correlated subquery** references a column from the outer query (`e.dept`), so conceptually it's re-evaluated for each outer row: "what's the average salary of *this* employee's department?"
            - Engineering average = (95000 + 120000 + 70000) / 3 = 95000 → only Bilal is above. Ayesha earns exactly the average, and `>` is strict, so she's excluded.
            - Sales average = (55000 + 61000 + 40000) / 3 = 52000 → Esha and Dipu.
            - HR has only Gazi, who equals his own average → nobody.

            The window-function version computes each department's average once with `AVG(salary) OVER (PARTITION BY dept)` and can show it alongside each row.
        """,
        a_bn=r"""
            **Correlated subquery** outer query-র একটা column (`e.dept`) refer করে, তাই ধারণাগতভাবে প্রতিটা outer row-এর জন্য এটা আবার evaluate হয়: "*এই* employee-এর department-এর গড় বেতন কত?"
            - Engineering-এর গড় = (95000 + 120000 + 70000) / 3 = 95000 → শুধু Bilal বেশি পায়। Ayesha ঠিক গড়ের সমান পায়, আর `>` strict, তাই সে বাদ।
            - Sales-এর গড় = (55000 + 61000 + 40000) / 3 = 52000 → Esha আর Dipu।
            - HR-এ শুধু Gazi, যে নিজের গড়ের সমান → কেউ না।

            Window-function version প্রতিটা department-এর গড় একবারই হিসাব করে `AVG(salary) OVER (PARTITION BY dept)` দিয়ে, আর প্রতিটা row-এর পাশে সেটা দেখাতেও পারে।
        """,
        quick_en=r"""Use a correlated subquery: `WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept = e.dept)`, evaluated per outer row. `>` is strict, so someone earning exactly the average is excluded; `AVG(...) OVER (PARTITION BY dept)` is the window alternative.""",
        quick_bn=r"""Correlated subquery ব্যবহার করো: `WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept = e.dept)`, যেটা outer query-র প্রতিটা row-এর জন্য হিসাব হয়। `>` strict, তাই ঠিক average-এর সমান বেতনের কেউ বাদ যায়; window বিকল্প হলো `AVG(...) OVER (PARTITION BY dept)`।""",
        ex_en=r"""
            - **Correlated vs non-correlated:** a non-correlated subquery (e.g. `WHERE salary > (SELECT AVG(salary) FROM employees)`) runs once and compares against the company-wide average — a different question.
            - **Performance:** "re-evaluated per row" is the logical model. Modern optimizers often decorrelate it into a join with a grouped derived table, but not always — check `EXPLAIN` on big tables. An index on `(dept, salary)` helps the subquery.
            - A third option is joining to a pre-aggregated derived table: `JOIN (SELECT dept, AVG(salary) AS avg_sal FROM employees GROUP BY dept) a ON a.dept = e.dept`.
            - A scalar subquery must return at most one row; if it can return more, the query errors at runtime.
        """,
        ex_bn=r"""
            - **Correlated বনাম non-correlated:** non-correlated subquery (যেমন `WHERE salary > (SELECT AVG(salary) FROM employees)`) একবারই চলে আর পুরো company-র গড়ের সাথে তুলনা করে — এটা ভিন্ন প্রশ্ন।
            - **Performance:** "প্রতি row-এ আবার evaluate" হলো logical model। আধুনিক optimizer প্রায়ই এটাকে grouped derived table-এর সাথে join-এ রূপান্তর (decorrelate) করে, কিন্তু সবসময় না — বড় table-এ `EXPLAIN` দেখো। `(dept, salary)`-এ index subquery-কে সাহায্য করে।
            - তৃতীয় উপায় হলো আগে aggregate করা derived table-এর সাথে join: `JOIN (SELECT dept, AVG(salary) AS avg_sal FROM employees GROUP BY dept) a ON a.dept = e.dept`।
            - Scalar subquery সর্বোচ্চ একটা row দিতে পারে; বেশি দিলে runtime-এ query error দেয়।
        """,
        tip_en=r"""Explicitly say "correlated, because it references `e.dept`", then offer the window-function alternative and when you'd prefer it. Mentioning the strict `>` edge case (Ayesha) shows care with data.""",
        tip_bn=r"""স্পষ্ট করে বলো "correlated, কারণ এটা `e.dept` refer করছে", তারপর window-function বিকল্পটা দাও আর কখন সেটা বেশি পছন্দ করবে বলো। Strict `>`-এর edge case (Ayesha) উল্লেখ করলে বোঝা যায় তুমি data নিয়ে সতর্ক।""",
        mist_en=r"""Comparing against the overall average (non-correlated), or trying `WHERE salary > AVG(salary)` directly (aggregates aren't allowed in `WHERE`).""",
        mist_bn=r"""পুরো company-র গড়ের সাথে তুলনা করা (non-correlated), অথবা সরাসরি `WHERE salary > AVG(salary)` লেখার চেষ্টা করা (`WHERE`-এ aggregate অনুমোদিত নয়)।""",
        follow=[
            ("Rewrite it with a JOIN to a grouped derived table.", "Grouped derived table-এর সাথে JOIN করে এটা আবার লেখো।"),
            ("How would you also show by how much each employee exceeds the average?", "প্রত্যেক employee গড়ের চেয়ে কত বেশি পায় সেটাও কীভাবে দেখাবে?"),
        ],
        related=["sql-016", "sql-013"],
        refs=[PG_SUBQUERY, PG_WINDOW_TUT],
    ),
    # ------------------------------------------------------------------ sql-016
    Q(
        id="sql-016", sub="Anti-Joins & the NOT IN NULL Trap", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["not-exists", "not-in", "left-join", "anti-join", "null"],
        ver="Version-independent (ISO SQL; output from PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Find the customers who have **never placed an order**. Note that `orders` contains a guest checkout with `customer_id = NULL`. Also explain why `WHERE id NOT IN (SELECT customer_id FROM orders)` returns no rows on this data.""",
        q_bn=r"""যেসব customer **কখনো কোনো order দেয়নি** তাদের বের করো। খেয়াল করো, `orders`-এ একটা guest checkout আছে যার `customer_id = NULL`। আর ব্যাখ্যা করো কেন এই data-য় `WHERE id NOT IN (SELECT customer_id FROM orders)` কোনো row return করে না।""",
        setup=r"""
            CREATE TABLE customers (
              id   INT PRIMARY KEY,
              name VARCHAR(50) NOT NULL
            );

            CREATE TABLE orders (
              id          INT PRIMARY KEY,
              customer_id INT REFERENCES customers(id),   -- NULL = guest checkout
              amount      NUMERIC(10,2) NOT NULL
            );

            INSERT INTO customers (id, name) VALUES
              (1, 'Rahim'), (2, 'Karim'), (3, 'Nadia'), (4, 'Sumi');

            INSERT INTO orders (id, customer_id, amount) VALUES
              (101, 1,    1500.00),
              (102, 1,     700.00),
              (103, 3,    1200.00),
              (104, NULL,  450.00);
        """,
        code=r"""
            SELECT c.id, c.name
            FROM customers c
            WHERE NOT EXISTS (
              SELECT 1
              FROM orders o
              WHERE o.customer_id = c.id
            )
            ORDER BY c.id;
        """,
        lang="sql",
        output=r"""
             id | name
            ----+-------
              2 | Karim
              4 | Sumi
        """,
        extra=[dict(lang="sql", label_en="LEFT JOIN version (same result) and the NOT IN trap (0 rows)",
                    label_bn="LEFT JOIN version (একই ফলাফল) আর NOT IN ফাঁদ (0 row)", src=r"""
            -- LEFT JOIN ... IS NULL: also returns Karim and Sumi
            SELECT c.id, c.name
            FROM customers c
            LEFT JOIN orders o ON o.customer_id = c.id
            WHERE o.id IS NULL
            ORDER BY c.id;

            -- TRAP: returns 0 rows, because the subquery contains a NULL
            SELECT c.id, c.name
            FROM customers c
            WHERE c.id NOT IN (SELECT customer_id FROM orders);

            -- if you must use NOT IN, exclude NULLs explicitly
            SELECT c.id, c.name
            FROM customers c
            WHERE c.id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);
        """)],
        a_en=r"""
            `NOT EXISTS` keeps a customer when the correlated subquery finds **no** matching order. Rahim and Nadia have orders; Karim and Sumi don't. The guest order (NULL) can never equal any `c.id`, so it's simply ignored — exactly what we want.

            **Why `NOT IN` returns nothing:** `2 NOT IN (1, 1, 3, NULL)` expands to `2 <> 1 AND 2 <> 1 AND 2 <> 3 AND 2 <> NULL`. The last comparison is UNKNOWN, so the whole `AND` chain is UNKNOWN (never TRUE), and `WHERE` drops every row. One NULL in the subquery wipes out the result.

            So I default to `NOT EXISTS` (or `LEFT JOIN ... IS NULL`) for anti-joins.
        """,
        a_bn=r"""
            Correlated subquery যদি কোনো matching order **না** পায়, তাহলে `NOT EXISTS` customer-টাকে রাখে। Rahim আর Nadia-র order আছে; Karim আর Sumi-র নেই। Guest order (NULL) কখনো কোনো `c.id`-এর সমান হতে পারে না, তাই সেটা স্বাভাবিকভাবেই উপেক্ষিত হয় — ঠিক যা আমরা চাই।

            **`NOT IN` কেন কিছুই দেয় না:** `2 NOT IN (1, 1, 3, NULL)` ভাঙলে দাঁড়ায় `2 <> 1 AND 2 <> 1 AND 2 <> 3 AND 2 <> NULL`। শেষ তুলনাটা UNKNOWN, তাই পুরো `AND` chain UNKNOWN (কখনো TRUE নয়), আর `WHERE` প্রতিটা row বাদ দেয়। Subquery-তে একটা NULL পুরো ফলাফল মুছে দেয়।

            তাই anti-join-এর জন্য আমি default হিসেবে `NOT EXISTS` (বা `LEFT JOIN ... IS NULL`) ব্যবহার করি।
        """,
        quick_en=r"""Use `NOT EXISTS` (or `LEFT JOIN ... IS NULL`), which returns Karim and Sumi. `NOT IN` returns nothing because the guest order's NULL makes `id <> NULL` UNKNOWN, so the whole condition is never TRUE.""",
        quick_bn=r"""`NOT EXISTS` (বা `LEFT JOIN ... IS NULL`) ব্যবহার করো, তাতে Karim আর Sumi আসে। `NOT IN` কিছুই দেয় না, কারণ guest order-এর NULL-এর জন্য `id <> NULL` UNKNOWN হয়, ফলে পুরো condition কখনো TRUE হয় না।""",
        ex_en=r"""
            - **`LEFT JOIN ... WHERE o.id IS NULL`:** check a column that can't be NULL in a real match (the primary key), not a nullable column.
            - **Performance:** PostgreSQL, SQL Server, and Oracle plan `NOT EXISTS` as an efficient anti-join. `NOT IN` can't always be turned into an anti-join precisely *because* of the NULL semantics, so it may be slower too.
            - `IN` (without `NOT`) is safe with NULLs: `1 IN (1, NULL)` is TRUE. The trap is specific to `NOT IN`.
            - Make the foreign key `NOT NULL` when a NULL has no business meaning; here NULL meaningfully represents a guest checkout.
        """,
        ex_bn=r"""
            - **`LEFT JOIN ... WHERE o.id IS NULL`:** এমন column check করো যেটা আসল match-এ কখনো NULL হতে পারে না (primary key), nullable column নয়।
            - **Performance:** PostgreSQL, SQL Server আর Oracle `NOT EXISTS`-কে একটা দক্ষ anti-join হিসেবে plan করে। NULL-এর এই অর্থের *কারণেই* `NOT IN`-কে সবসময় anti-join-এ রূপান্তর করা যায় না, তাই এটা ধীরও হতে পারে।
            - `NOT` ছাড়া `IN` NULL-এর সাথে নিরাপদ: `1 IN (1, NULL)` TRUE। ফাঁদটা শুধু `NOT IN`-এর।
            - NULL-এর কোনো business অর্থ না থাকলে foreign key `NOT NULL` করো; এখানে NULL অর্থবহভাবে guest checkout বোঝায়।
        """,
        tip_en=r"""Write `NOT EXISTS` first, then volunteer the `NOT IN` + NULL explanation by expanding it into `<>` comparisons — that expansion is the clearest way to show you truly understand three-valued logic.""",
        tip_bn=r"""আগে `NOT EXISTS` লেখো, তারপর নিজে থেকেই `NOT IN` + NULL ব্যাখ্যা দাও — `<>` তুলনাগুলোতে ভেঙে দেখিয়ে। Three-valued logic যে তুমি সত্যিই বোঝো, সেটা দেখানোর সবচেয়ে পরিষ্কার উপায় এই ভেঙে দেখানো।""",
        mist_en=r"""Using `NOT IN` against a nullable column, or checking a nullable right-table column for `IS NULL` in the LEFT JOIN version.""",
        mist_bn=r"""Nullable column-এর বিরুদ্ধে `NOT IN` ব্যবহার করা, অথবা LEFT JOIN version-এ ডান table-এর nullable column-এ `IS NULL` check করা।""",
        follow=[
            ("Find customers who ordered in September but not in October.", "যারা September-এ order দিয়েছে কিন্তু October-এ দেয়নি, তাদের বের করো।"),
            ("Is `EXCEPT` another way to do this? What are its limitations?", "`EXCEPT` কি এটা করার আরেকটা উপায়? এর সীমাবদ্ধতা কী?"),
        ],
        related=["sql-006", "sql-015"],
        refs=[PG_SUBQUERY, PG_JOIN_TUT],
    ),
]

if __name__ == "__main__":
    save("sql", "b2", QUESTIONS)
