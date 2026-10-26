# SQL quick-recall — sql-q01 … sql-q10 (short viva-style fundamentals)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_CONSTRAINTS = ("PostgreSQL docs — Constraints", "https://www.postgresql.org/docs/current/ddl-constraints.html")
PG_COMMANDS = ("PostgreSQL docs — SQL Commands", "https://www.postgresql.org/docs/current/sql-commands.html")
PG_TABLE_EXPR = ("PostgreSQL docs — Table Expressions (WHERE, GROUP BY, HAVING)", "https://www.postgresql.org/docs/current/queries-table-expressions.html")
PG_AGG_TUT = ("PostgreSQL docs — Aggregate Functions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-agg.html")
PG_UNION = ("PostgreSQL docs — Combining Queries (UNION, INTERSECT, EXCEPT)", "https://www.postgresql.org/docs/current/queries-union.html")
PG_COMPARISON = ("PostgreSQL docs — Comparison Functions and Operators", "https://www.postgresql.org/docs/current/functions-comparison.html")
MS_NORMALIZATION = ("Microsoft Learn — Database normalization description", "https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description")
PG_TX_TUT = ("PostgreSQL docs — Transactions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-transactions.html")
MS_CLUSTERED = ("Microsoft Learn — Clustered and nonclustered indexes", "https://learn.microsoft.com/en-us/sql/relational-databases/indexes/clustered-and-nonclustered-indexes-described")

VER = "Version-independent (ISO SQL)"

QUESTIONS = [
    # ------------------------------------------------------------------ sql-q01
    Q(
        id="sql-q01", sub="Constraints & Keys", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["primary-key", "foreign-key", "constraints"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between a primary key and a foreign key?""",
        q_bn=r"""Primary key আর foreign key-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""A primary key uniquely identifies each row in its own table: it must be unique and not NULL, and a table has only one. A foreign key is a column in another table that must match an existing primary (or unique) key value, so it links the two tables and blocks references to rows that don't exist.""",
        a_bn=r"""Primary key নিজের table-এর প্রতিটা row-কে আলাদাভাবে চেনায়: এটা unique আর NULL হতে পারে না, আর একটা table-এ একটাই থাকে। Foreign key হলো আরেকটা table-এর column, যার value-কে কোনো বিদ্যমান primary (বা unique) key-এর সাথে মিলতে হয়; এভাবে দুটো table যুক্ত হয়, আর নেই এমন row-কে reference করা আটকে যায়।""",
        code=r"""
            CREATE TABLE customers (id INT PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE orders (
              id          INT PRIMARY KEY,
              customer_id INT REFERENCES customers(id)   -- foreign key
            );
            INSERT INTO customers VALUES (1, 'Rahim');
            INSERT INTO orders VALUES (10, 1);   -- ok
            INSERT INTO orders VALUES (11, 99);  -- error: foreign key violation (no customer 99)
        """, lang="sql",
        ex_en=r"""A foreign key column can repeat (one customer, many orders) and can be NULL unless you add `NOT NULL`. Its `ON DELETE` action (`RESTRICT`, `CASCADE`, `SET NULL`) decides what happens when the parent row is deleted.""",
        ex_bn=r"""Foreign key column-এ value বারবার আসতে পারে (একজন customer, অনেক order), আর `NOT NULL` না দিলে NULL-ও হতে পারে। Parent row delete হলে কী হবে সেটা ঠিক করে এর `ON DELETE` action (`RESTRICT`, `CASCADE`, `SET NULL`)।""",
        tip_en=r"""Say "PK identifies, FK references", then mention that a foreign key column can repeat and can be NULL.""",
        tip_bn=r"""বলো "PK চেনায়, FK reference করে", তারপর উল্লেখ করো যে foreign key column-এ value বারবার আসতে পারে আর NULL-ও হতে পারে।""",
        follow=[
            ("What does `ON DELETE CASCADE` do?", "`ON DELETE CASCADE` কী করে?"),
            ("Can a table have more than one unique key?", "একটা table-এ কি একাধিক unique key থাকতে পারে?"),
        ],
        related=["sql-007", "pg-002"],
        refs=[PG_CONSTRAINTS],
    ),
    # ------------------------------------------------------------------ sql-q02
    Q(
        id="sql-q02", sub="SQL Command Categories", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["ddl", "dml", "dcl", "tcl"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are DDL, DML, DCL and TCL? Give an example command for each.""",
        q_bn=r"""DDL, DML, DCL আর TCL কী? প্রতিটার একটা করে command-এর উদাহরণ দাও।""",
        a_en=r"""DDL (Data Definition Language) defines structure: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`. DML (Data Manipulation Language) works with rows: `SELECT`, `INSERT`, `UPDATE`, `DELETE`. DCL controls permissions with `GRANT` and `REVOKE`, and TCL controls transactions with `BEGIN`, `COMMIT`, `ROLLBACK` and `SAVEPOINT`.""",
        a_bn=r"""DDL (Data Definition Language) structure ঠিক করে: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`। DML (Data Manipulation Language) row নিয়ে কাজ করে: `SELECT`, `INSERT`, `UPDATE`, `DELETE`। DCL `GRANT` আর `REVOKE` দিয়ে permission নিয়ন্ত্রণ করে, আর TCL `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` দিয়ে transaction নিয়ন্ত্রণ করে।""",
        ex_en=r"""Some books put `SELECT` in its own group, DQL. The split matters in practice: in MySQL and Oracle, DDL commits the open transaction implicitly, while PostgreSQL can roll DDL back.""",
        ex_bn=r"""কিছু বইয়ে `SELECT`-কে আলাদা group, DQL-এ রাখা হয়। ভাগটা বাস্তবেও কাজে লাগে: MySQL আর Oracle-এ DDL চালালে খোলা transaction নিজে থেকেই commit হয়ে যায়, কিন্তু PostgreSQL-এ DDL rollback করা যায়।""",
        tip_en=r"""List the four groups with two commands each; adding that `TRUNCATE` counts as DDL shows you know the edge cases.""",
        tip_bn=r"""চারটা group আর প্রতিটায় দুটো করে command বলো; `TRUNCATE` যে DDL ধরা হয় সেটা যোগ করলে বোঝা যায় তুমি edge case-ও জানো।""",
        follow=[("Why is `TRUNCATE` DDL while `DELETE` is DML?", "`DELETE` DML হলেও `TRUNCATE` কেন DDL?")],
        related=["sql-009", "pg-006"],
        refs=[PG_COMMANDS],
    ),
    # ------------------------------------------------------------------ sql-q03
    Q(
        id="sql-q03", sub="WHERE vs HAVING", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["where", "having", "group-by", "aggregates"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `WHERE` and `HAVING`?""",
        q_bn=r"""`WHERE` আর `HAVING`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`WHERE` filters individual rows before grouping, so it can't use aggregates like `COUNT(*)`. `HAVING` filters groups after `GROUP BY`, so it can. You can use both in one query: `WHERE` first narrows the rows, then `HAVING` drops the groups you don't want.""",
        a_bn=r"""`WHERE` group করার আগে প্রতিটা row filter করে, তাই এতে `COUNT(*)`-এর মতো aggregate ব্যবহার করা যায় না। `HAVING` `GROUP BY`-এর পরে group filter করে, তাই এতে করা যায়। একই query-তে দুটোই দেওয়া যায়: আগে `WHERE` row কমায়, তারপর `HAVING` অদরকারি group বাদ দেয়।""",
        code=r"""
            -- employees: IT (60000, 45000), HR (50000, 30000), Sales (40000)
            SELECT dept, COUNT(*) AS staff
            FROM employees
            WHERE salary >= 40000        -- rows: drops the 30000 HR employee
            GROUP BY dept
            HAVING COUNT(*) >= 2;        -- groups: keeps only IT
            -- → IT | 2
        """, lang="sql",
        ex_en=r"""Putting `COUNT(*) >= 2` in `WHERE` is an error, because groups don't exist yet when `WHERE` runs. A plain row condition works in `HAVING` too, but it belongs in `WHERE`, which filters before the grouping work.""",
        ex_bn=r"""`COUNT(*) >= 2` `WHERE`-এ দিলে error হয়, কারণ `WHERE` চলার সময় group তৈরিই হয়নি। সাধারণ row condition `HAVING`-এও চলে, কিন্তু সেটা `WHERE`-এ রাখাই ঠিক, কারণ তাহলে grouping-এর আগেই row কমে যায়।""",
        tip_en=r"""Say "`WHERE` filters rows, `HAVING` filters groups" and tie it to the order: `FROM` → `WHERE` → `GROUP BY` → `HAVING`.""",
        tip_bn=r"""বলো "`WHERE` row filter করে, `HAVING` group filter করে", তারপর ক্রমটার সাথে মেলাও: `FROM` → `WHERE` → `GROUP BY` → `HAVING`।""",
        follow=[("Can you use a `SELECT` alias in `WHERE`?", "`SELECT`-এর alias কি `WHERE`-এ ব্যবহার করা যায়?")],
        related=["sql-004", "sql-001"],
        refs=[PG_TABLE_EXPR],
    ),
    # ------------------------------------------------------------------ sql-q04
    Q(
        id="sql-q04", sub="GROUP BY & Aggregates", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["group-by", "aggregates", "count", "sum"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What does `GROUP BY` do, and which columns are you allowed to put in the `SELECT` list with it?""",
        q_bn=r"""`GROUP BY` কী করে, আর এর সাথে `SELECT` list-এ কোন কোন column রাখা যায়?""",
        a_en=r"""`GROUP BY` puts rows with the same value in the listed columns into one group and returns one row per group, so aggregates like `COUNT`, `SUM` and `AVG` are computed per group. Every column in `SELECT` must either be in `GROUP BY` or be inside an aggregate function.""",
        a_bn=r"""`GROUP BY` উল্লেখ করা column-এ একই value থাকা row-গুলোকে একটা group-এ রাখে আর প্রতিটা group-এর জন্য একটা row দেয়, তাই `COUNT`, `SUM`, `AVG`-এর মতো aggregate প্রতিটা group-এর জন্য আলাদা হিসাব হয়। `SELECT`-এর প্রতিটা column হয় `GROUP BY`-এ থাকতে হবে, নয়তো কোনো aggregate function-এর ভেতরে।""",
        code=r"""
            SELECT dept, COUNT(*) AS staff, SUM(salary) AS total
            FROM employees
            GROUP BY dept
            ORDER BY dept;
        """, lang="sql",
        output=r"""
             dept  | staff | total
            -------+-------+--------
             HR    |     2 |  80000
             IT    |     2 | 105000
             Sales |     1 |  40000
        """,
        ex_en=r"""`SELECT dept, name, COUNT(*) ... GROUP BY dept` fails in PostgreSQL ("must appear in the GROUP BY clause or be used in an aggregate function") because a group has many names. Exception: PostgreSQL allows a column that depends on a grouped primary key.""",
        ex_bn=r"""`SELECT dept, name, COUNT(*) ... GROUP BY dept` PostgreSQL-এ fail করে ("must appear in the GROUP BY clause or be used in an aggregate function"), কারণ এক group-এ অনেকগুলো name থাকে। ব্যতিক্রম: group করা primary key-এর ওপর নির্ভরশীল column PostgreSQL মেনে নেয়।""",
        tip_en=r"""State the rule "grouped or aggregated" and explain it: one output row per group can't show many different names.""",
        tip_bn=r"""নিয়মটা বলো "হয় group করা, নয়তো aggregate", আর কারণটা ব্যাখ্যা করো: প্রতি group-এ একটা output row অনেকগুলো আলাদা name দেখাতে পারে না।""",
        follow=[("How do aggregate functions treat NULL values?", "Aggregate function NULL value-কে কীভাবে ধরে?")],
        related=["sql-003", "sql-005"],
        refs=[PG_AGG_TUT],
    ),
    # ------------------------------------------------------------------ sql-q05
    Q(
        id="sql-q05", sub="Set Operations", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["union", "union-all", "set-operations"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between `UNION` and `UNION ALL`?""",
        q_bn=r"""`UNION` আর `UNION ALL`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""Both stack the results of two queries on top of each other. `UNION` removes duplicate rows, which costs a sort or hash step, while `UNION ALL` keeps every row and is faster. Both queries must return the same number of columns with compatible types.""",
        a_bn=r"""দুটোই দুটো query-র result একটার নিচে আরেকটা জুড়ে দেয়। `UNION` duplicate row বাদ দেয়, তাই একটা sort বা hash ধাপের খরচ লাগে; `UNION ALL` সব row রাখে আর বেশি দ্রুত। দুটো query-কে একই সংখ্যক column আর মিলযোগ্য type দিতে হবে।""",
        code=r"""
            -- dhaka_customers: Rahim, Karim    ctg_customers: Karim, Nadia
            SELECT name FROM dhaka_customers
            UNION
            SELECT name FROM ctg_customers;   -- → Karim, Nadia, Rahim (3 rows)

            -- with UNION ALL instead → Rahim, Karim, Karim, Nadia (4 rows)
        """, lang="sql",
        ex_en=r"""Use `UNION ALL` when the parts can't overlap or duplicates are fine. Column names come from the first query, and an `ORDER BY` at the end sorts the combined result.""",
        ex_bn=r"""অংশগুলো একে অপরের সাথে মিলতে না পারলে বা duplicate থাকলে সমস্যা না হলে `UNION ALL` নাও। Column-এর নাম আসে প্রথম query থেকে, আর শেষে `ORDER BY` দিলে পুরো জোড়া result sort হয়।""",
        tip_en=r"""Mention the cost: "`UNION` = `UNION ALL` + duplicate removal", so default to `UNION ALL` when duplicates are impossible.""",
        tip_bn=r"""খরচটা বলো: "`UNION` = `UNION ALL` + duplicate বাদ দেওয়া", তাই duplicate সম্ভব না হলে `UNION ALL`-ই নাও।""",
        follow=[("What do `INTERSECT` and `EXCEPT` return?", "`INTERSECT` আর `EXCEPT` কী return করে?")],
        related=["sql-q06", "sql-023"],
        refs=[PG_UNION],
    ),
    # ------------------------------------------------------------------ sql-q06
    Q(
        id="sql-q06", sub="Set Operations", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["intersect", "except", "set-operations"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What do `INTERSECT` and `EXCEPT` do?""",
        q_bn=r"""`INTERSECT` আর `EXCEPT` কী করে?""",
        a_en=r"""`INTERSECT` returns the rows that appear in both query results, and `EXCEPT` returns the rows of the first query that are not in the second. Like `UNION`, they remove duplicates unless you add `ALL`, and both queries need matching columns.""",
        a_bn=r"""`INTERSECT` সেই row-গুলো দেয় যেগুলো দুটো query-র result-এই আছে, আর `EXCEPT` প্রথম query-র সেই row-গুলো দেয় যেগুলো দ্বিতীয়টায় নেই। `UNION`-এর মতোই `ALL` না দিলে এরা duplicate বাদ দেয়, আর দুটো query-র column মিলতে হবে।""",
        code=r"""
            -- dhaka_customers: Rahim, Karim    ctg_customers: Karim, Nadia
            SELECT name FROM dhaka_customers
            INTERSECT
            SELECT name FROM ctg_customers;   -- → Karim

            -- with EXCEPT instead → Rahim (in Dhaka, not in Ctg)
        """, lang="sql",
        ex_en=r"""Oracle has traditionally called `EXCEPT` `MINUS`, and MySQL added both operators only in 8.0.31. Set operators compare whole rows and treat two NULLs as equal, unlike `NOT IN`.""",
        ex_bn=r"""Oracle-এ `EXCEPT`-কে প্রচলিতভাবে `MINUS` বলা হয়, আর MySQL দুটো operator যোগ করেছে কেবল 8.0.31-এ। Set operator পুরো row তুলনা করে আর `NOT IN`-এর মতো নয়, দুটো NULL-কে সমান ধরে।""",
        tip_en=r"""Use a two-list example ("customers in Dhaka and Ctg") and say `EXCEPT` is a readable anti-join.""",
        tip_bn=r"""দুটো list-এর উদাহরণ দাও ("Dhaka আর Ctg-এর customer"), আর বলো `EXCEPT` হলো পড়তে সহজ একটা anti-join।""",
        follow=[("How else can you find rows in A that are not in B?", "A-তে আছে কিন্তু B-তে নেই এমন row আর কীভাবে বের করা যায়?")],
        related=["sql-q05", "sql-016"],
        refs=[PG_UNION],
    ),
    # ------------------------------------------------------------------ sql-q07
    Q(
        id="sql-q07", sub="NULL Handling", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["null", "is-null", "coalesce"],
        ver=VER, vs=False, status="stable",
        q_en=r"""How do you check for NULL in SQL, and why doesn't `= NULL` work?""",
        q_bn=r"""SQL-এ NULL কীভাবে check করো, আর `= NULL` কেন কাজ করে না?""",
        a_en=r"""NULL means "unknown", so any comparison with it, even `NULL = NULL`, gives UNKNOWN instead of TRUE, and `WHERE` drops the row. Use `IS NULL` / `IS NOT NULL` to test for it, and `COALESCE(col, default)` to replace NULL with a value.""",
        a_bn=r"""NULL মানে "অজানা", তাই এর সাথে যেকোনো তুলনা, এমনকি `NULL = NULL`-ও, TRUE না হয়ে UNKNOWN হয়, আর `WHERE` row-টা বাদ দেয়। NULL check করতে `IS NULL` / `IS NOT NULL` ব্যবহার করো, আর NULL-এর জায়গায় কোনো value বসাতে `COALESCE(col, default)`।""",
        code=r"""
            -- customers: ('Rahim', 'Dhaka'), ('Nadia', NULL)
            SELECT name FROM customers WHERE city = NULL;   -- → no rows
            SELECT name FROM customers WHERE city IS NULL;  -- → Nadia
            SELECT name, COALESCE(city, 'Unknown') AS city
            FROM customers;                                 -- → Rahim | Dhaka, Nadia | Unknown
        """, lang="sql",
        ex_en=r"""NULL also spreads through arithmetic: `5 + NULL` is NULL. Aggregates like `SUM` and `AVG` skip NULLs, while `COUNT(*)` still counts the row.""",
        ex_bn=r"""Arithmetic-এও NULL ছড়িয়ে পড়ে: `5 + NULL`-এর ফল NULL। `SUM` আর `AVG`-এর মতো aggregate NULL বাদ দেয়, কিন্তু `COUNT(*)` row-টা ঠিকই গোনে।""",
        tip_en=r"""Say "NULL is unknown, not zero or empty", then show `IS NULL` and `COALESCE` in one line each.""",
        tip_bn=r"""বলো "NULL মানে অজানা, শূন্য বা খালি নয়", তারপর `IS NULL` আর `COALESCE` এক line করে দেখাও।""",
        follow=[
            ("Why can `NOT IN` with a subquery return no rows?", "Subquery-সহ `NOT IN` কেন কোনো row না-ও দিতে পারে?"),
            ("What is the difference between NULL and an empty string?", "NULL আর empty string-এর মধ্যে পার্থক্য কী?"),
        ],
        related=["sql-006", "sql-016", "sql-005"],
        refs=[PG_COMPARISON],
    ),
    # ------------------------------------------------------------------ sql-q08
    Q(
        id="sql-q08", sub="Normalization", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["normalization", "1nf", "2nf", "3nf"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What are 1NF, 2NF and 3NF?""",
        q_bn=r"""1NF, 2NF আর 3NF কী?""",
        a_en=r"""1NF: every column holds a single value and there are no repeating groups. 2NF: 1NF, and no non-key column depends on only part of a composite key. 3NF: 2NF, and no non-key column depends on another non-key column (no transitive dependency), so each fact is stored once.""",
        a_bn=r"""1NF: প্রতিটা column-এ একটাই value, কোনো repeating group নেই। 2NF: 1NF, আর কোনো non-key column composite key-এর শুধু একটা অংশের ওপর নির্ভর করে না। 3NF: 2NF, আর কোনো non-key column অন্য কোনো non-key column-এর ওপর নির্ভর করে না (transitive dependency নেই), তাই প্রতিটা তথ্য একবারই রাখা হয়।""",
        ex_en=r"""Example 3NF break: `employees(id, dept_id, dept_name)`, where `dept_name` depends on `dept_id`, not on `id`; move it to a `departments` table. The goal is avoiding update, insert and delete anomalies.""",
        ex_bn=r"""3NF ভাঙার উদাহরণ: `employees(id, dept_id, dept_name)`, এখানে `dept_name` নির্ভর করে `dept_id`-এর ওপর, `id`-এর ওপর নয়; এটাকে একটা `departments` table-এ সরাও। উদ্দেশ্য হলো update, insert আর delete anomaly এড়ানো।""",
        tip_en=r"""Give one tiny example per form; the phrase "the key, the whole key, and nothing but the key" summarises 1NF to 3NF.""",
        tip_bn=r"""প্রতিটা form-এর জন্য একটা ছোট উদাহরণ দাও; "the key, the whole key, and nothing but the key" কথাটা 1NF থেকে 3NF-এর সারাংশ।""",
        follow=[("When would you deliberately denormalize?", "কখন ইচ্ছা করে denormalize করবে?")],
        related=["sql-011", "pg-001", "sql-032"],
        refs=[MS_NORMALIZATION],
    ),
    # ------------------------------------------------------------------ sql-q09
    Q(
        id="sql-q09", sub="Transactions & ACID", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["acid", "transactions"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What does ACID stand for?""",
        q_bn=r"""ACID বলতে কী বোঝায়?""",
        a_en=r"""ACID is the set of guarantees a transaction gives. Atomicity: all of its changes happen or none do. Consistency: it moves the database from one valid state to another, respecting constraints. Isolation: concurrent transactions don't see each other's half-done work. Durability: once committed, changes survive a crash.""",
        a_bn=r"""ACID হলো transaction যে নিশ্চয়তাগুলো দেয়। Atomicity: হয় সব change হবে, নয়তো কোনোটাই না। Consistency: constraint মেনে database এক valid অবস্থা থেকে আরেক valid অবস্থায় যায়। Isolation: একসাথে চলা transaction একে অপরের অর্ধেক কাজ দেখে না। Durability: commit হয়ে গেলে change crash-এও টিকে থাকে।""",
        code=r"""
            BEGIN;
            UPDATE accounts SET balance = balance - 500 WHERE id = 1;
            UPDATE accounts SET balance = balance + 500 WHERE id = 2;
            COMMIT;   -- both updates or neither (atomicity)
        """, lang="sql",
        ex_en=r"""Isolation isn't all-or-nothing: the isolation level (Read Committed by default in PostgreSQL) decides which effects of concurrent transactions you can see.""",
        ex_bn=r"""Isolation পুরোপুরি হ্যাঁ বা না নয়: কোন isolation level (PostgreSQL-এ default Read Committed) সেটা ঠিক করে একসাথে চলা transaction-এর কোন প্রভাব তুমি দেখতে পাবে।""",
        tip_en=r"""Explain each letter with the money-transfer example instead of reciting four definitions.""",
        tip_bn=r"""চারটা সংজ্ঞা মুখস্থ বলার বদলে money transfer-এর উদাহরণ দিয়ে প্রতিটা অক্ষর ব্যাখ্যা করো।""",
        follow=[("What are the transaction isolation levels?", "Transaction isolation level-গুলো কী কী?")],
        related=["sql-010", "sql-029", "pg-006"],
        refs=[PG_TX_TUT],
    ),
    # ------------------------------------------------------------------ sql-q10
    Q(
        id="sql-q10", sub="Indexes", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["indexes", "clustered-index", "non-clustered-index"],
        ver="Engine-specific (SQL Server, MySQL InnoDB, PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""What is the difference between a clustered and a non-clustered index?""",
        q_bn=r"""Clustered আর non-clustered index-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""A clustered index stores the table rows themselves in index-key order, so a table can have only one. A non-clustered index is a separate structure holding key values plus a pointer to the row, and a table can have many. In SQL Server and MySQL InnoDB the primary key is clustered by default.""",
        a_bn=r"""Clustered index-এ table-এর row-গুলোই index key-এর ক্রমে রাখা হয়, তাই একটা table-এ একটাই থাকতে পারে। Non-clustered index একটা আলাদা structure, যেখানে key value আর row-এর একটা pointer থাকে, আর একটা table-এ এরকম অনেকগুলো থাকতে পারে। SQL Server আর MySQL InnoDB-তে primary key default-ভাবে clustered।""",
        ex_en=r"""PostgreSQL has no maintained clustered index: tables are heaps and every index is secondary. Its `CLUSTER` command reorders the table once, and new rows don't keep that order.""",
        ex_bn=r"""PostgreSQL-এ সবসময় বজায় থাকা clustered index নেই: table হলো heap, আর প্রতিটা index secondary। এর `CLUSTER` command table-টা একবার সাজিয়ে দেয়, নতুন row সেই ক্রম মানে না।""",
        tip_en=r"""Use the book analogy carefully: a clustered index is like a dictionary sorted by word; a non-clustered one is the index at the back of a book.""",
        tip_bn=r"""Book-এর উপমাটা সাবধানে দাও: clustered index হলো শব্দ অনুযায়ী সাজানো অভিধানের মতো; non-clustered হলো বইয়ের শেষের index-এর মতো।""",
        follow=[("Why do indexes slow down writes?", "Index কেন write ধীর করে?")],
        related=["pg-005", "sql-020"],
        refs=[MS_CLUSTERED],
    ),
]

if __name__ == "__main__":
    save("sql", "quick", QUESTIONS)
