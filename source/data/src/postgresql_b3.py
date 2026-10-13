# PostgreSQL batch 3 — pg-017 … pg-024
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_SELECT = ("PostgreSQL docs — SELECT (DISTINCT ON, locking clause)", "https://www.postgresql.org/docs/current/sql-select.html")
PG_WINDOW_TUT = ("PostgreSQL docs — Window Functions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-window.html")
PG_LATERAL = ("PostgreSQL docs — Table Expressions (LATERAL)", "https://www.postgresql.org/docs/current/queries-table-expressions.html")
PG_ROLES = ("PostgreSQL docs — Database Roles", "https://www.postgresql.org/docs/current/user-manag.html")
PG_PRIVS = ("PostgreSQL docs — Privileges", "https://www.postgresql.org/docs/current/ddl-priv.html")
PG_AUTH_PW = ("PostgreSQL docs — Password Authentication", "https://www.postgresql.org/docs/current/auth-password.html")
PG_ISO = ("PostgreSQL docs — Transaction Isolation", "https://www.postgresql.org/docs/current/transaction-iso.html")
PG_RETURNING = ("PostgreSQL docs — Returning Data from Modified Rows", "https://www.postgresql.org/docs/current/dml-returning.html")
PG_LOCKING = ("PostgreSQL docs — Explicit Locking", "https://www.postgresql.org/docs/current/explicit-locking.html")
PG_CONN = ("PostgreSQL docs — Connections and Authentication settings", "https://www.postgresql.org/docs/current/runtime-config-connection.html")
PG_STAT_ACTIVITY = ("PostgreSQL docs — Monitoring Statistics (pg_stat_activity)", "https://www.postgresql.org/docs/current/monitoring-stats.html")
PG_INSERT = ("PostgreSQL docs — INSERT (ON CONFLICT)", "https://www.postgresql.org/docs/current/sql-insert.html")
PG_MERGE = ("PostgreSQL docs — MERGE", "https://www.postgresql.org/docs/current/sql-merge.html")
PG_USING_EXPLAIN = ("PostgreSQL docs — Using EXPLAIN", "https://www.postgresql.org/docs/current/using-explain.html")
PG_PLANNER_STATS = ("PostgreSQL docs — Statistics Used by the Planner", "https://www.postgresql.org/docs/current/planner-stats.html")
PG_VACUUM = ("PostgreSQL docs — Routine Vacuuming (statistics, autovacuum)", "https://www.postgresql.org/docs/current/routine-vacuuming.html")

QUESTIONS = [
    # ------------------------------------------------------------------ pg-017
    Q(
        id="pg-017", sub="Window Functions & DISTINCT ON", diff="medium", type="query",
        prio="high", market="both", mins=6,
        tags=["window-functions", "distinct-on", "left-join", "latest-per-group"],
        ver="PostgreSQL 18 (DISTINCT ON is PostgreSQL-specific)", vs=False, status="stable",
        q_en=r"""For every customer, return their **latest** order (id, date, amount) together with their total number of orders and lifetime spend. Customers without orders must still appear. If two orders share the same date, the one with the higher id counts as the latest. Write it in PostgreSQL.""",
        q_bn=r"""প্রতিটা customer-এর **সর্বশেষ** order (id, date, amount), সাথে তাদের মোট order সংখ্যা আর lifetime spend বের করো। যাদের কোনো order নেই, তাদেরও দেখাতে হবে। একই তারিখে দুটো order থাকলে বড় id-ওয়ালাটাকে সর্বশেষ ধরো। PostgreSQL-এ লেখো।""",
        setup=r"""
            CREATE TABLE customers (
              id   int PRIMARY KEY,
              name text NOT NULL
            );

            CREATE TABLE orders (
              id          int PRIMARY KEY,
              customer_id int NOT NULL REFERENCES customers(id),
              ordered_at  date NOT NULL,
              amount      numeric(10,2) NOT NULL
            );

            INSERT INTO customers VALUES (1, 'Rahim'), (2, 'Karim'), (3, 'Nadia'), (4, 'Sumi');

            INSERT INTO orders VALUES
              (101, 1, '2026-09-01', 1200.00),
              (102, 1, '2026-09-15',  800.00),
              (103, 2, '2026-09-03',  450.00),
              (104, 1, '2026-10-02', 2500.00),
              (105, 3, '2026-10-05',  300.00),
              (106, 3, '2026-10-05',  700.00),
              (107, 2, '2026-10-01',  950.00);
        """,
        code=r"""
            SELECT DISTINCT ON (c.id)
                   c.name,
                   o.id                                   AS last_order_id,
                   o.ordered_at                           AS last_order_at,
                   o.amount                               AS last_amount,
                   count(o.id) OVER (PARTITION BY c.id)   AS order_count,
                   coalesce(sum(o.amount) OVER (PARTITION BY c.id), 0) AS lifetime_spend
            FROM customers c
            LEFT JOIN orders o ON o.customer_id = c.id
            ORDER BY c.id, o.ordered_at DESC, o.id DESC;
        """,
        lang="sql",
        output=r"""
             name  | last_order_id | last_order_at | last_amount | order_count | lifetime_spend
            -------+---------------+---------------+-------------+-------------+----------------
             Rahim |           104 | 2026-10-02    |     2500.00 |           3 |        4500.00
             Karim |           107 | 2026-10-01    |      950.00 |           2 |        1400.00
             Nadia |           106 | 2026-10-05    |      700.00 |           2 |        1000.00
             Sumi  |               |               |             |           0 |              0
        """,
        a_en=r"""
            - `LEFT JOIN` keeps Sumi, who has no orders (her order columns are NULL).
            - The **window functions** run over all of a customer's joined rows *before* `DISTINCT ON` removes rows, so `count(o.id)` and `sum(o.amount)` see every order. `count(o.id)` (not `count(*)`) gives 0 for Sumi because NULLs aren't counted; `coalesce` turns her NULL sum into 0.
            - `DISTINCT ON (c.id)` keeps the **first** row of each `c.id` group according to `ORDER BY`. Its expressions must match the leftmost `ORDER BY` items, and the rest of the `ORDER BY` decides which row wins: newest date, then highest id — that's why Nadia's latest is 106, not 105.
        """,
        a_bn=r"""
            - `LEFT JOIN` Sumi-কে রেখে দেয়, যার কোনো order নেই (তার order column-গুলো NULL)।
            - **Window function**-গুলো `DISTINCT ON` row বাদ দেওয়ার *আগেই* customer-এর সব joined row-এর উপর চলে, তাই `count(o.id)` আর `sum(o.amount)` প্রতিটা order দেখতে পায়। `count(*)` না দিয়ে `count(o.id)` দেওয়ায় Sumi-র জন্য 0 আসে, কারণ NULL গোনা হয় না; `coalesce` তার NULL sum-কে 0 বানায়।
            - `DISTINCT ON (c.id)` প্রতিটা `c.id` group-এর `ORDER BY` অনুযায়ী **প্রথম** row রাখে। এর expression-গুলো `ORDER BY`-এর বাম দিকের item-এর সাথে মিলতে হয়, আর `ORDER BY`-এর বাকি অংশ ঠিক করে কোন row জিতবে: সবচেয়ে নতুন date, তারপর সবচেয়ে বড় id — এজন্যই Nadia-র সর্বশেষ order 106, 105 নয়।
        """,
        ex_en=r"""
            - **Portable version:** `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_at DESC, id DESC)` in a subquery, then filter `rn = 1`. `DISTINCT ON` is PostgreSQL-only, but shorter and usually fast.
            - **Top-N per customer (e.g. last 3 orders)** on big tables: `LEFT JOIN LATERAL (SELECT ... FROM orders WHERE customer_id = c.id ORDER BY ordered_at DESC LIMIT 3) o ON true` with an index on `(customer_id, ordered_at DESC)` — one short index scan per customer instead of sorting all orders.
            - Always add a tie-breaker (`id DESC`); without it, the "latest" row among equal dates is arbitrary and can change between runs.
            - Logical order matters: `FROM/JOIN` → `WHERE` → `GROUP BY` → window functions → `DISTINCT ON` → `ORDER BY` output.
        """,
        ex_bn=r"""
            - **Portable version:** subquery-তে `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ordered_at DESC, id DESC)`, তারপর `rn = 1` filter। `DISTINCT ON` শুধু PostgreSQL-এ চলে, কিন্তু ছোট আর সাধারণত দ্রুত।
            - বড় table-এ **প্রতি customer-এর top-N (যেমন শেষ ৩টা order)**: `LEFT JOIN LATERAL (SELECT ... FROM orders WHERE customer_id = c.id ORDER BY ordered_at DESC LIMIT 3) o ON true`, সাথে `(customer_id, ordered_at DESC)`-এ index — সব order sort করার বদলে প্রতি customer-এর জন্য একটা ছোট index scan।
            - সবসময় tie-breaker দাও (`id DESC`); না দিলে একই তারিখের মধ্যে "সর্বশেষ" row এলোমেলোভাবে বাছা হয় আর বিভিন্ন run-এ বদলে যেতে পারে।
            - Logical order গুরুত্বপূর্ণ: `FROM/JOIN` → `WHERE` → `GROUP BY` → window function → `DISTINCT ON` → `ORDER BY` output।
        """,
        tip_en=r"""Explain why the window counts are correct even though `DISTINCT ON` drops rows — that ordering insight is the real test. Then offer the portable `ROW_NUMBER()` version unprompted.""",
        tip_bn=r"""`DISTINCT ON` row বাদ দিলেও window count কেন ঠিক থাকে — এই ordering-এর বোঝাপড়াটাই আসল পরীক্ষা। তারপর কেউ না চাইতেই portable `ROW_NUMBER()` version-টা দেখাও।""",
        mist_en=r"""Using `count(*)` (gives 1 for customers without orders), using an inner join (drops Sumi), or omitting the tie-breaker in `ORDER BY`.""",
        mist_bn=r"""`count(*)` ব্যবহার করা (order না থাকা customer-এর জন্যও 1 দেয়), inner join ব্যবহার করা (Sumi বাদ পড়ে যায়), অথবা `ORDER BY`-তে tie-breaker না দেওয়া।""",
        follow=[
            ("Rewrite this with `ROW_NUMBER()` so it runs on MySQL 8 or SQL Server.", "এটা `ROW_NUMBER()` দিয়ে আবার লেখো যাতে MySQL 8 বা SQL Server-এ চলে।"),
            ("How would you return the last 3 orders per customer efficiently on a 50-million-row table?", "৫ কোটি row-এর table-এ প্রতি customer-এর শেষ ৩টা order দক্ষতার সাথে কীভাবে বের করবে?"),
        ],
        related=["pg-016"],
        refs=[PG_SELECT, PG_WINDOW_TUT, PG_LATERAL],
    ),
    # ------------------------------------------------------------------ pg-018
    Q(
        id="pg-018", sub="Security: Roles & Authentication", diff="medium", type="security-performance",
        prio="high", market="both", mins=6,
        tags=["roles", "least-privilege", "scram", "md5-deprecated", "pg_hba"],
        ver="PostgreSQL 18", vs=True, status="stable",
        q_en=r"""Your Node.js API connects to PostgreSQL as the `postgres` superuser, and its password is stored with MD5. What's wrong with this, and how would you set up roles and authentication properly on PostgreSQL 18?""",
        q_bn=r"""তোমার Node.js API `postgres` superuser হিসেবে PostgreSQL-এ connect করে, আর এর password MD5 দিয়ে রাখা। এতে সমস্যা কী, আর PostgreSQL 18-এ role আর authentication ঠিকভাবে কীভাবে সাজাবে?""",
        a_en=r"""
            **What's wrong:** a superuser bypasses every permission check and row-level security, and can read server files or run programs (`COPY ... PROGRAM`). One SQL-injection bug turns into a full server compromise. MD5 password auth is **deprecated in PostgreSQL 18** (it warns when you set MD5 passwords) and will be removed in a future release; the stored MD5 hash is weak and effectively password-equivalent.

            **What I'd do:**
            - An **owner role** (`NOLOGIN`) owns the schema and tables; migrations run as it.
            - An **app role** (`LOGIN`) gets only `USAGE` on the schema and `SELECT/INSERT/UPDATE/DELETE` on the tables it needs — no DDL, no superuser.
            - A **read-only role** for reporting and analysts.
            - `ALTER DEFAULT PRIVILEGES` so future tables get the same grants.
            - `password_encryption = scram-sha-256` (the default since PG14), reset existing passwords so they're stored as SCRAM, and use `hostssl ... scram-sha-256` in `pg_hba.conf`.
            - Per-role limits: `CONNECTION LIMIT`, `statement_timeout`.
        """,
        a_bn=r"""
            **সমস্যা কী:** superuser সব permission check আর row-level security এড়িয়ে যায়, আর server-এর file পড়তে বা program চালাতে পারে (`COPY ... PROGRAM`)। একটা SQL-injection bug-ই পুরো server দখলের পথ খুলে দেয়। **PostgreSQL 18-এ MD5 password auth deprecated** (MD5 password set করলে warning দেয়) আর ভবিষ্যতের কোনো release-এ এটা সরিয়ে ফেলা হবে; জমা রাখা MD5 hash দুর্বল আর কার্যত password-এর সমান।

            **আমি যা করব:**
            - একটা **owner role** (`NOLOGIN`) schema আর table-এর মালিক থাকবে; migration এটা হিসেবে চলবে।
            - একটা **app role** (`LOGIN`) শুধু schema-তে `USAGE` আর দরকারি table-এ `SELECT/INSERT/UPDATE/DELETE` পাবে — কোনো DDL নয়, superuser নয়।
            - Reporting আর analyst-দের জন্য একটা **read-only role**।
            - `ALTER DEFAULT PRIVILEGES`, যাতে ভবিষ্যতের table-গুলোও একই grant পায়।
            - `password_encryption = scram-sha-256` (PG14 থেকে default), পুরনো password reset করো যাতে SCRAM হিসেবে জমা হয়, আর `pg_hba.conf`-এ `hostssl ... scram-sha-256` ব্যবহার করো।
            - Role অনুযায়ী limit: `CONNECTION LIMIT`, `statement_timeout`।
        """,
        ex_en=r"""
            - Identity columns don't need extra grants; `serial` columns also need `USAGE` on their sequences, a common "permission denied for sequence" error.
            - Since PostgreSQL 15, ordinary users can no longer `CREATE` in the `public` schema by default — keep it that way.
            - Table owners bypass row-level security unless you use `ALTER TABLE ... FORCE ROW LEVEL SECURITY` — one more reason the app must not connect as the owner.
            - Avoid `CREATE ROLE ... PASSWORD '...'` in scripts that end up in logs or shell history; psql's `\password` sends an already-hashed password. Keep credentials in a secret manager and rotate them.
            - Network: don't expose port 5432 to the internet; restrict by security group / firewall and `pg_hba.conf` CIDR ranges, and require TLS.
            - Parameterised queries are still the primary SQL-injection defence; least privilege limits the blast radius.
        """,
        ex_bn=r"""
            - Identity column-এ বাড়তি grant লাগে না; `serial` column-এ sequence-এর উপর `USAGE`-ও দিতে হয় — "permission denied for sequence" error-এর এটা খুব সাধারণ কারণ।
            - PostgreSQL 15 থেকে সাধারণ user default-ভাবে `public` schema-তে আর `CREATE` করতে পারে না — এভাবেই রাখো।
            - `ALTER TABLE ... FORCE ROW LEVEL SECURITY` না দিলে table owner row-level security এড়িয়ে যায় — app যে owner হিসেবে connect করবে না, এটা তার আরেকটা কারণ।
            - যেসব script log বা shell history-তে যায়, সেখানে `CREATE ROLE ... PASSWORD '...'` এড়িয়ে চলো; psql-এর `\password` আগেই hash করা password পাঠায়। Credential secret manager-এ রাখো আর rotate করো।
            - Network: port 5432 internet-এ খোলা রেখো না; security group / firewall আর `pg_hba.conf`-এর CIDR range দিয়ে সীমিত করো, আর TLS বাধ্যতামূলক করো।
            - SQL injection-এর বিরুদ্ধে প্রধান প্রতিরক্ষা এখনো parameterised query; least privilege ক্ষতির পরিধি সীমিত রাখে।
        """,
        tip_en=r"""Lead with the blast-radius argument (superuser + injection = server compromise), then walk through the three roles. Mentioning the PG18 MD5 deprecation and the RLS owner-bypass detail shows current, practical knowledge.""",
        tip_bn=r"""শুরুতেই blast-radius-এর যুক্তি দাও (superuser + injection = server দখল), তারপর তিনটা role একে একে বলো। PG18-এ MD5 deprecation আর RLS-এ owner-bypass-এর খুঁটিনাটি বললে বোঝা যায় তোমার জ্ঞান হালনাগাদ আর practical।""",
        mist_en=r"""Granting `ALL PRIVILEGES` to the app role "to avoid permission errors", or switching `password_encryption` to SCRAM without resetting existing passwords (they stay MD5 until changed).""",
        mist_bn=r""""Permission error এড়াতে" app role-কে `ALL PRIVILEGES` দিয়ে দেওয়া, অথবা `password_encryption` SCRAM-এ বদলে পুরনো password reset না করা (বদলানো না পর্যন্ত সেগুলো MD5-ই থাকে)।""",
        code=r"""
            -- owner of all schema objects; used only by migrations
            CREATE ROLE shop_owner NOLOGIN;
            CREATE SCHEMA shop AUTHORIZATION shop_owner;

            -- application login role: least privilege
            CREATE ROLE shop_app LOGIN CONNECTION LIMIT 100;
            -- psql meta-command: prompts, hashes client-side (SCRAM), never logs the plain password
            \password shop_app
            GRANT USAGE ON SCHEMA shop TO shop_app;
            GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA shop TO shop_app;
            ALTER DEFAULT PRIVILEGES FOR ROLE shop_owner IN SCHEMA shop
              GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO shop_app;
            ALTER ROLE shop_app SET statement_timeout = '5s';

            -- read-only role for reporting (grant it to analyst logins)
            CREATE ROLE shop_readonly NOLOGIN;
            GRANT USAGE ON SCHEMA shop TO shop_readonly;
            GRANT SELECT ON ALL TABLES IN SCHEMA shop TO shop_readonly;
            ALTER DEFAULT PRIVILEGES FOR ROLE shop_owner IN SCHEMA shop
              GRANT SELECT ON TABLES TO shop_readonly;
        """,
        lang="sql",
        extra=[dict(lang="text", label_en="postgresql.conf and pg_hba.conf", label_bn="postgresql.conf আর pg_hba.conf", src=r"""
            # postgresql.conf
            password_encryption = scram-sha-256
            ssl = on

            # pg_hba.conf — only the app subnet, only over TLS, only SCRAM
            # TYPE    DATABASE  USER      ADDRESS        METHOD
            hostssl   shop      shop_app  10.0.0.0/16    scram-sha-256
        """)],
        follow=[
            ("How does row-level security work, and who bypasses it?", "Row-level security কীভাবে কাজ করে, আর কারা এটা bypass করে?"),
            ("How would you rotate the app's database password without downtime?", "Downtime ছাড়া app-এর database password কীভাবে rotate করবে?"),
        ],
        related=["pg-032", "pg-006"],
        refs=[PG_ROLES, PG_PRIVS, PG_AUTH_PW],
    ),
    # ------------------------------------------------------------------ pg-019
    Q(
        id="pg-019", sub="Concurrency: Lost Updates", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["lost-update", "race-condition", "row-locking", "node-pg", "returning"],
        ver="PostgreSQL 18 (OLD/NEW in RETURNING); node-postgres 8.x", vs=True, status="stable",
        q_en=r"""Users report that two quick withdrawals sometimes both succeed even when the wallet only had enough money for one, and the final balance is wrong. Find the bug in this Node.js code and fix it.""",
        q_bn=r"""User-রা জানাচ্ছে, দ্রুত পরপর দুটো withdrawal কখনো কখনো দুটোই সফল হয়ে যায়, যদিও wallet-এ একটার মতো টাকাই ছিল, আর শেষ balance-ও ভুল আসে। এই Node.js code-এর bug খুঁজে বের করো আর ঠিক করো।""",
        code=r"""
            // POST /wallet/withdraw — may be called concurrently (double taps, app retries)
            export async function withdraw(pool, userId, amount) {
              const { rows } = await pool.query(
                'SELECT balance FROM wallets WHERE user_id = $1',
                [userId],
              );
              const balance = Number(rows[0].balance);

              if (balance < amount) throw new Error('Insufficient balance');

              await pool.query(
                'UPDATE wallets SET balance = $1 WHERE user_id = $2',
                [balance - amount, userId],
              );
            }
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed: one atomic conditional UPDATE inside a transaction",
                    label_bn="সংশোধিত: transaction-এর ভেতরে একটা atomic conditional UPDATE", src=r"""
            export async function withdraw(pool, userId, amount) {
              const client = await pool.connect();
              try {
                await client.query('BEGIN');

                // check + write in ONE statement; the row lock serialises concurrent withdrawals
                const { rows, rowCount } = await client.query(
                  `UPDATE wallets
                      SET balance = balance - $1
                    WHERE user_id = $2 AND balance >= $1
                    RETURNING old.balance AS old_balance, new.balance AS new_balance`, // PG18
                  [amount, userId],
                );
                if (rowCount === 0) throw new Error('Insufficient balance');

                await client.query(
                  'INSERT INTO wallet_ledger (user_id, amount, kind) VALUES ($1, $2, $3)',
                  [userId, -amount, 'withdraw'],
                );
                await client.query('COMMIT');
                return rows[0];
              } catch (err) {
                await client.query('ROLLBACK');
                throw err;
              } finally {
                client.release();
              }
            }
        """), dict(lang="sql", label_en="Alternative: lock the row first with SELECT ... FOR UPDATE",
                   label_bn="বিকল্প: SELECT ... FOR UPDATE দিয়ে আগে row lock করা", src=r"""
            BEGIN;
            SELECT balance FROM wallets WHERE user_id = $1 FOR UPDATE;  -- others wait here
            -- application checks the balance, then:
            UPDATE wallets SET balance = balance - $2 WHERE user_id = $1;
            COMMIT;
        """)],
        a_en=r"""
            It's a classic **lost update** (read-modify-write race). Two requests run `SELECT` at the same time, both read 500, both pass the check for 400, and both write `500 - 400 = 100`. The user withdrew 800 but the balance says 100 — one update overwrote the other. MVCC doesn't save you here: plain `SELECT`s don't lock anything, and under Read Committed nothing ties the read to the later write.

            Fix: make the check and the write **one atomic statement** — `UPDATE ... SET balance = balance - $1 WHERE user_id = $2 AND balance >= $1`. The `UPDATE` takes a row lock; a concurrent withdrawal waits, then PostgreSQL re-checks the `WHERE` clause against the newly committed row. The second one sees 100, matches 0 rows, and fails cleanly. Wrap it with the ledger insert in a transaction on a single client.
        """,
        a_bn=r"""
            এটা একটা classic **lost update** (read-modify-write race)। দুটো request একই সময়ে `SELECT` চালায়, দুজনেই 500 পড়ে, দুজনেই 400-এর check পার হয়, আর দুজনেই `500 - 400 = 100` লেখে। User 800 তুলেছে, অথচ balance বলছে 100 — একটা update আরেকটাকে overwrite করে দিয়েছে। এখানে MVCC বাঁচায় না: সাধারণ `SELECT` কিছু lock করে না, আর Read Committed-এ read আর পরের write-এর মধ্যে কোনো বাঁধন নেই।

            সমাধান: check আর write-কে **একটা atomic statement** বানাও — `UPDATE ... SET balance = balance - $1 WHERE user_id = $2 AND balance >= $1`। `UPDATE` row lock নেয়; concurrent withdrawal অপেক্ষা করে, তারপর PostgreSQL নতুন commit হওয়া row-এর উপর `WHERE` আবার যাচাই করে। দ্বিতীয়টা 100 দেখে, 0 row match করে, আর পরিষ্কারভাবে fail করে। Ledger insert-সহ পুরোটা একটা client-এ transaction-এর ভেতরে রাখো।
        """,
        ex_en=r"""
            - **Other valid fixes:** `SELECT ... FOR UPDATE` inside a transaction (when the decision logic must live in the app), or Repeatable Read/Serializable with automatic retries on serialization failures (`40001`).
            - Add `CHECK (balance >= 0)` on the table as a last line of defence — a bug elsewhere then fails loudly instead of creating money.
            - `Number(rows[0].balance)`: node-postgres returns `numeric` as a string on purpose; converting money to a JS float invites rounding issues. Do the arithmetic in SQL (as in the fix) or use a decimal library.
            - The original code also ran two statements on possibly different pooled connections with no transaction.
            - PostgreSQL 18's `RETURNING old.balance, new.balance` returns the before and after values in one round trip — handy for audit logs. On older versions, `RETURNING balance` gives the new value only.
            - For client retries (double taps), also add an **idempotency key** so the same request isn't applied twice.
        """,
        ex_bn=r"""
            - **আরও কিছু সঠিক সমাধান:** transaction-এর ভেতরে `SELECT ... FOR UPDATE` (যখন সিদ্ধান্তের logic app-এই রাখতে হয়), অথবা Repeatable Read/Serializable আর serialization failure (`40001`) হলে automatic retry।
            - Table-এ শেষ প্রতিরক্ষা হিসেবে `CHECK (balance >= 0)` দাও — অন্য কোথাও bug থাকলে সেটা টাকা "তৈরি" না করে জোরেশোরে fail করবে।
            - `Number(rows[0].balance)`: node-postgres ইচ্ছা করেই `numeric`-কে string হিসেবে return করে; টাকাকে JS float-এ রূপান্তর করলে rounding সমস্যা হতে পারে। হিসাবটা SQL-এ করো (fix-এর মতো) অথবা একটা decimal library ব্যবহার করো।
            - মূল code দুটো statement সম্ভবত দুটো আলাদা pooled connection-এ, কোনো transaction ছাড়াই চালাচ্ছিল।
            - PostgreSQL 18-এর `RETURNING old.balance, new.balance` এক round trip-এ আগের আর পরের value দুটোই ফেরত দেয় — audit log-এর জন্য সুবিধাজনক। পুরনো version-এ `RETURNING balance` শুধু নতুন value দেয়।
            - Client retry (double tap)-এর জন্য একটা **idempotency key**-ও যোগ করো, যাতে একই request দুবার apply না হয়।
        """,
        tip_en=r"""Draw the two-request timeline (T1 read, T2 read, T1 write, T2 write) — it makes the race obvious. Then explain why the conditional `UPDATE` is safe: row lock + `WHERE` re-check.""",
        tip_bn=r"""দুটো request-এর timeline এঁকে দেখাও (T1 read, T2 read, T1 write, T2 write) — race-টা তখন স্পষ্ট হয়। তারপর ব্যাখ্যা করো conditional `UPDATE` কেন নিরাপদ: row lock + `WHERE`-এর পুনর্যাচাই।""",
        mist_en=r""""Fixing" it by raising the isolation level without adding retry logic, or by adding an application-level mutex that doesn't work across multiple server instances.""",
        mist_bn=r"""Retry logic ছাড়া শুধু isolation level বাড়িয়ে "ঠিক" করা, অথবা app-level mutex বসানো যেটা একাধিক server instance-এ কাজই করে না।""",
        follow=[
            ("What happens to the second `UPDATE` under Read Committed after the first one commits?", "প্রথম `UPDATE` commit হওয়ার পর Read Committed-এ দ্বিতীয় `UPDATE`-এর কী হয়?"),
            ("How would you implement idempotency keys for this endpoint?", "এই endpoint-এর জন্য idempotency key কীভাবে implement করবে?"),
        ],
        related=["pg-006", "pg-023", "pg-020"],
        refs=[PG_ISO, PG_LOCKING, PG_RETURNING],
    ),
    # ------------------------------------------------------------------ pg-020
    Q(
        id="pg-020", sub="Row Locking & Job Queues", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["skip-locked", "for-update", "job-queue", "row-locks"],
        ver="PostgreSQL 9.5+ (current: 18)", vs=False, status="stable",
        q_en=r"""Several worker processes run the query below to claim the next queued job. You want each worker to grab a **different** job without waiting on rows other workers have already locked. What belongs in the blank?""",
        q_bn=r"""কয়েকটা worker process পরের queued job নেওয়ার জন্য নিচের query চালায়। তুমি চাও প্রতিটা worker একটা **আলাদা** job নিক, আর অন্য worker যে row lock করে রেখেছে তার জন্য অপেক্ষা না করুক। ফাঁকা জায়গায় কী বসবে?""",
        code=r"""
            UPDATE jobs
               SET status = 'running', locked_at = now()
             WHERE id = (
                   SELECT id FROM jobs
                   WHERE status = 'queued'
                   ORDER BY run_at, id
                   LIMIT 1
                   ________________
             )
            RETURNING id, payload;
        """,
        lang="sql",
        options=[
            ("`FOR UPDATE NOWAIT`", "`FOR UPDATE NOWAIT`"),
            ("`FOR UPDATE SKIP LOCKED`", "`FOR UPDATE SKIP LOCKED`"),
            ("`FOR SHARE`", "`FOR SHARE`"),
            ("Nothing — Read Committed already prevents two workers from picking the same row.",
             "কিছুই না — Read Committed আগে থেকেই দুটো worker-কে একই row নিতে বাধা দেয়।"),
        ],
        correct=1,
        a_en=r"""`FOR UPDATE SKIP LOCKED`. Each worker locks the row it picks, and other workers simply **skip** rows that are already locked and take the next one, so there's no waiting and no double processing.""",
        a_bn=r"""`FOR UPDATE SKIP LOCKED`। প্রতিটা worker যে row বাছে সেটা lock করে, আর অন্য worker-রা already-locked row-গুলো শুধু **এড়িয়ে** পরেরটা নেয় — ফলে কোনো অপেক্ষা নেই, একই job দুবার process-ও হয় না।""",
        ex_en=r"""
            - `NOWAIT` is the tempting wrong answer: it doesn't skip — it raises an error immediately if the row is locked, so workers would keep failing on the same first job.
            - `FOR SHARE` lets several workers share-lock the same row; they'd all pick the same job and then block each other on the `UPDATE`.
            - With **no** locking clause, two workers can read the same id; the second `UPDATE` waits, then re-checks only `id = ...` (status isn't in the outer `WHERE`) and processes the job a second time.

            Production tips: add a partial index `ON jobs (run_at, id) WHERE status = 'queued'`, keep the claim transaction short, and handle crashed workers (e.g. requeue jobs whose `locked_at` is too old). High job churn creates dead tuples, so watch autovacuum. A PostgreSQL queue is great for moderate volumes and for enqueuing jobs in the same transaction as your business write (outbox pattern); for very high throughput, a dedicated broker may fit better.
        """,
        ex_bn=r"""
            - `NOWAIT` হলো লোভনীয় ভুল উত্তর: এটা skip করে না — row locked থাকলে সাথে সাথে error দেয়, ফলে worker-রা একই প্রথম job-এ বারবার fail করতে থাকবে।
            - `FOR SHARE` একাধিক worker-কে একই row-এ share-lock নিতে দেয়; সবাই একই job বেছে নেবে, তারপর `UPDATE`-এ একে অপরকে block করবে।
            - **কোনো** locking clause না থাকলে দুটো worker একই id পড়তে পারে; দ্বিতীয় `UPDATE` অপেক্ষা করে, তারপর শুধু `id = ...` আবার যাচাই করে (outer `WHERE`-এ status নেই), আর job-টা দ্বিতীয়বার process করে ফেলে।

            Production টিপস: `ON jobs (run_at, id) WHERE status = 'queued'` partial index দাও, claim transaction ছোট রাখো, আর crash হওয়া worker সামলাও (যেমন যেসব job-এর `locked_at` অনেক পুরনো সেগুলো আবার queue-তে ফেরত দাও)। অনেক job আসা-যাওয়া করলে dead tuple জমে, তাই autovacuum-এর দিকে নজর রাখো। মাঝারি volume আর business write-এর একই transaction-এ job enqueue করার জন্য (outbox pattern) PostgreSQL queue দারুণ; খুব বেশি throughput লাগলে আলাদা broker বেশি মানানসই হতে পারে।
        """,
        tip_en=r"""After answering, explain why `NOWAIT` is wrong — that's what the interviewer is checking. Mentioning the outbox pattern connects it to real architecture.""",
        tip_bn=r"""উত্তর দেওয়ার পর `NOWAIT` কেন ভুল সেটা ব্যাখ্যা করো — interviewer আসলে এটাই যাচাই করছে। Outbox pattern-এর কথা বললে বাস্তব architecture-এর সাথে যোগসূত্র দেখানো হয়।""",
        related=["pg-019", "pg-023"],
        refs=[PG_SELECT, PG_LOCKING],
    ),
    # ------------------------------------------------------------------ pg-021
    Q(
        id="pg-021", sub="Connection Pooling", diff="medium", type="scenario",
        prio="high", market="both", mins=7,
        tags=["connection-pooling", "pgbouncer", "max_connections", "node-pg", "kubernetes"],
        ver="PostgreSQL 18; PgBouncer (current releases); node-postgres 8.x", vs=False, status="stable",
        q_en=r"""After scaling your Node.js API to 30 Kubernetes pods (each with a `pg.Pool` of `max: 20`), PostgreSQL starts rejecting connections with `FATAL: sorry, too many clients already`. How do you diagnose and fix this?""",
        q_bn=r"""তোমার Node.js API-কে 30টা Kubernetes pod-এ scale করার পর (প্রতিটায় `max: 20`-এর `pg.Pool`), PostgreSQL `FATAL: sorry, too many clients already` দিয়ে connection reject করা শুরু করেছে। কীভাবে diagnose আর fix করবে?""",
        a_en=r"""
            **Diagnose the math first:** 30 pods × 20 = up to 600 connections, while `max_connections` defaults to 100. Then check `pg_stat_activity`: usually most connections are `idle`, and some are `idle in transaction` (leaked clients or transactions left open).

            **Why not just raise `max_connections` to 1000?** Each connection is a separate backend process with its own memory (and `work_mem` per sort/hash), and throughput peaks at a fairly small number of *active* connections — beyond that you get contention and context switching.

            **Fix, in order:**
            1. Right-size the app pools (e.g. `max: 5` per pod), set `idleTimeoutMillis`, and make sure every checked-out client is released.
            2. Set `idle_in_transaction_session_timeout` so forgotten transactions get killed.
            3. Put **PgBouncer** (or a managed proxy like RDS Proxy) in front in **transaction pooling mode**: thousands of client connections share a small server pool (say 40–60).
            4. Move heavy read traffic to read replicas if needed.
        """,
        a_bn=r"""
            **প্রথমে হিসাবটা দেখো:** 30 pod × 20 = সর্বোচ্চ 600 connection, অথচ `max_connections`-এর default 100। তারপর `pg_stat_activity` দেখো: সাধারণত বেশিরভাগ connection `idle`, আর কিছু `idle in transaction` (leak হওয়া client বা খোলা রেখে দেওয়া transaction)।

            **শুধু `max_connections` 1000 করে দিলেই কেন হবে না?** প্রতিটা connection একটা আলাদা backend process, নিজস্ব memory-সহ (আর প্রতি sort/hash-এ `work_mem`), আর throughput বেশ অল্প সংখ্যক *active* connection-এই সর্বোচ্চ হয় — এর বেশি হলে contention আর context switching বাড়ে।

            **সমাধান, ক্রমানুসারে:**
            1. App pool-এর আকার ঠিক করো (যেমন প্রতি pod-এ `max: 5`), `idleTimeoutMillis` দাও, আর নিশ্চিত করো প্রতিটা checked-out client release হচ্ছে।
            2. `idle_in_transaction_session_timeout` দাও, যাতে ভুলে খোলা রাখা transaction kill হয়।
            3. সামনে **PgBouncer** (বা RDS Proxy-র মতো managed proxy) বসাও **transaction pooling mode**-এ: হাজারো client connection একটা ছোট server pool (ধরো 40–60) ভাগাভাগি করে।
            4. দরকার হলে ভারী read traffic read replica-তে সরাও।
        """,
        ex_en=r"""
            **Transaction-mode caveats** — a client gets a server connection only for the duration of a transaction, so session state doesn't survive between transactions:
            - `SET` (use `SET LOCAL` inside a transaction instead), session-level advisory locks, `LISTEN/NOTIFY`, temporary tables, and `WITH HOLD` cursors don't work reliably.
            - SQL-level `PREPARE`/`EXECUTE` isn't tracked. Modern PgBouncer versions do support protocol-level prepared statements in transaction mode via `max_prepared_statements`.
            - Run migrations and `LISTEN` consumers on a direct (or session-mode) connection.

            Sizing hint: start the server pool near a small multiple of the DB's CPU cores and measure. Serverless functions (Lambda, edge) make this problem worse, because each instance opens its own connections — always put a pooler in front of them.
        """,
        ex_bn=r"""
            **Transaction mode-এর সতর্কতা** — client শুধু একটা transaction চলাকালীন server connection পায়, তাই session state দুটো transaction-এর মাঝে টিকে থাকে না:
            - `SET` (এর বদলে transaction-এর ভেতরে `SET LOCAL` ব্যবহার করো), session-level advisory lock, `LISTEN/NOTIFY`, temporary table আর `WITH HOLD` cursor নির্ভরযোগ্যভাবে কাজ করে না।
            - SQL-level `PREPARE`/`EXECUTE` track হয় না। আধুনিক PgBouncer version `max_prepared_statements` দিয়ে transaction mode-এ protocol-level prepared statement support করে।
            - Migration আর `LISTEN` consumer সরাসরি (বা session-mode) connection-এ চালাও।

            আকার ঠিক করার ইঙ্গিত: server pool শুরু করো DB-র CPU core-এর ছোট একটা গুণিতকের কাছাকাছি, তারপর মেপে দেখো। Serverless function (Lambda, edge) সমস্যাটা আরও বাড়ায়, কারণ প্রতিটা instance নিজের connection খোলে — এগুলোর সামনে সবসময় একটা pooler রাখো।
        """,
        tip_en=r"""Start with the multiplication (pods × pool size) — it shows you reason from numbers. Then explain why raising `max_connections` is the wrong first move, and finish with the transaction-mode caveats.""",
        tip_bn=r"""গুণ দিয়ে শুরু করো (pod × pool size) — এতে বোঝা যায় তুমি সংখ্যা দিয়ে চিন্তা করো। তারপর ব্যাখ্যা করো কেন `max_connections` বাড়ানো ভুল প্রথম পদক্ষেপ, আর শেষ করো transaction-mode-এর সতর্কতা দিয়ে।""",
        mist_en=r"""Raising `max_connections` to thousands, or enabling PgBouncer transaction mode while the app still relies on session `SET` statements or `LISTEN/NOTIFY`.""",
        mist_bn=r"""`max_connections` হাজারে তুলে দেওয়া, অথবা app এখনো session `SET` বা `LISTEN/NOTIFY`-এর উপর নির্ভর করছে অথচ PgBouncer transaction mode চালু করে দেওয়া।""",
        code=r"""
            SHOW max_connections;

            -- who is holding connections, and in what state?
            SELECT usename, application_name, state, count(*)
            FROM pg_stat_activity
            WHERE backend_type = 'client backend'
            GROUP BY usename, application_name, state
            ORDER BY count(*) DESC;

            -- kill sessions that sit idle inside a transaction for too long
            ALTER SYSTEM SET idle_in_transaction_session_timeout = '60s';
            SELECT pg_reload_conf();
        """,
        lang="sql",
        extra=[dict(lang="text", label_en="pgbouncer.ini (transaction pooling)", label_bn="pgbouncer.ini (transaction pooling)", src=r"""
            [databases]
            shop = host=10.0.1.10 port=5432 dbname=shop

            [pgbouncer]
            listen_port = 6432
            auth_type = scram-sha-256
            auth_file = /etc/pgbouncer/userlist.txt
            pool_mode = transaction
            max_client_conn = 2000
            default_pool_size = 40
            max_prepared_statements = 200
        """), dict(lang="javascript", label_en="Smaller per-pod pool in node-postgres", label_bn="node-postgres-এ প্রতি pod-এ ছোট pool", src=r"""
            import pg from 'pg';

            export const pool = new pg.Pool({
              host: process.env.PGBOUNCER_HOST,
              port: 6432,
              max: 5,                    // per pod
              idleTimeoutMillis: 30_000,
              connectionTimeoutMillis: 5_000,
            });
        """)],
        follow=[
            ("Which features break in PgBouncer transaction mode, and how do you work around them?", "PgBouncer transaction mode-এ কোন feature-গুলো কাজ করে না, আর কীভাবে সামলাবে?"),
            ("How would you connect AWS Lambda functions to PostgreSQL safely?", "AWS Lambda function-কে নিরাপদে PostgreSQL-এর সাথে কীভাবে connect করবে?"),
        ],
        related=["pg-006", "pg-031"],
        refs=[PG_CONN, PG_STAT_ACTIVITY],
    ),
    # ------------------------------------------------------------------ pg-022
    Q(
        id="pg-022", sub="Upserts: ON CONFLICT & MERGE", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["upsert", "on-conflict", "merge", "returning", "postgresql-18"],
        ver="PostgreSQL 18 (ON CONFLICT 9.5+, MERGE 15+, MERGE RETURNING 17+, OLD/NEW RETURNING 18)", vs=True, status="stable",
        q_en=r"""A supplier feed sends stock arrivals as `(sku, qty)` batches. In **one statement**, add the arriving quantity to SKUs that already exist, insert new SKUs, and return the new stock level for each SKU in the batch: `('TSHIRT-M', 20), ('JEANS-32', 5), ('CAP-RED', 12)`.""",
        q_bn=r"""একটা supplier feed stock arrival `(sku, qty)` batch হিসেবে পাঠায়। **একটা statement-এ**: যেসব SKU আগে থেকে আছে সেগুলোর qty-র সাথে নতুন qty যোগ করো, নতুন SKU insert করো, আর batch-এর প্রতিটা SKU-র নতুন stock level return করো: `('TSHIRT-M', 20), ('JEANS-32', 5), ('CAP-RED', 12)`।""",
        setup=r"""
            CREATE TABLE inventory (
              sku        text PRIMARY KEY,
              qty        int  NOT NULL CHECK (qty >= 0),
              updated_at timestamptz NOT NULL DEFAULT now()
            );

            INSERT INTO inventory (sku, qty) VALUES
              ('TSHIRT-M', 10),
              ('JEANS-32',  0),
              ('SOCKS',    50);
        """,
        code=r"""
            INSERT INTO inventory (sku, qty)
            VALUES ('TSHIRT-M', 20), ('JEANS-32', 5), ('CAP-RED', 12)
            ON CONFLICT (sku) DO UPDATE
              SET qty        = inventory.qty + EXCLUDED.qty,
                  updated_at = now()
            RETURNING sku, qty;
        """,
        lang="sql",
        output=r"""
               sku    | qty
            ----------+-----
             TSHIRT-M |  30
             JEANS-32 |   5
             CAP-RED  |  12
        """,
        a_en=r"""
            - `ON CONFLICT (sku)` names the **arbiter**: the unique index (here the primary key) whose violation turns the insert into an update.
            - `EXCLUDED` is the row that was *proposed* for insertion, so `inventory.qty + EXCLUDED.qty` adds the arriving quantity to the existing one: TSHIRT-M 10 + 20 = 30, JEANS-32 0 + 5 = 5. CAP-RED didn't exist, so it's inserted with 12. SOCKS isn't in the batch and is untouched.
            - `RETURNING` sends back the final values without a second query.
            - The whole thing is **atomic and race-safe**: two concurrent feeds can't both insert the same new SKU, unlike "SELECT, then INSERT or UPDATE" in application code.
        """,
        a_bn=r"""
            - `ON CONFLICT (sku)` **arbiter** ঠিক করে দেয়: কোন unique index (এখানে primary key) violate হলে insert-টা update-এ পরিণত হবে।
            - `EXCLUDED` হলো যে row-টা insert করার *প্রস্তাব* করা হয়েছিল, তাই `inventory.qty + EXCLUDED.qty` আগের qty-র সাথে নতুনটা যোগ করে: TSHIRT-M 10 + 20 = 30, JEANS-32 0 + 5 = 5। CAP-RED আগে ছিল না, তাই 12 দিয়ে insert হয়। SOCKS batch-এ নেই, তাই অপরিবর্তিত।
            - `RETURNING` দ্বিতীয় query ছাড়াই চূড়ান্ত value ফেরত পাঠায়।
            - পুরোটা **atomic আর race-safe**: application code-এ "আগে SELECT, তারপর INSERT বা UPDATE"-এর মতো নয় — দুটো concurrent feed একই নতুন SKU দুবার insert করতে পারে না।
        """,
        ex_en=r"""
            - If the same SKU appears twice in one batch, PostgreSQL raises `ON CONFLICT DO UPDATE command cannot affect row a second time` — aggregate the batch first (`GROUP BY sku`).
            - `ON CONFLICT DO NOTHING` is the "insert if absent" variant (e.g. idempotent event ingestion).
            - **MERGE** (PostgreSQL 15+, standard SQL) is more flexible: several `WHEN MATCHED`/`WHEN NOT MATCHED` branches with conditions, deletes, and in PG17 `WHEN NOT MATCHED BY SOURCE` plus `RETURNING` with `merge_action()`. But under concurrency MERGE can still fail with a unique violation when another session inserts the same key, so `INSERT ... ON CONFLICT` remains the go-to for concurrent upserts.
            - **PostgreSQL 18:** `RETURNING sku, old.qty AS old_qty, new.qty AS new_qty` — `old` values are NULL for newly inserted rows and non-NULL for rows updated through `ON CONFLICT`, so you can tell inserts from updates.
            - `ON CONFLICT`, `EXCLUDED`, and `RETURNING` are PostgreSQL syntax (MySQL uses `ON DUPLICATE KEY UPDATE`).
        """,
        ex_bn=r"""
            - একই batch-এ একই SKU দুবার থাকলে PostgreSQL `ON CONFLICT DO UPDATE command cannot affect row a second time` error দেয় — আগে batch-টা aggregate করে নাও (`GROUP BY sku`)।
            - `ON CONFLICT DO NOTHING` হলো "না থাকলে insert করো" রূপ (যেমন idempotent event ingestion)।
            - **MERGE** (PostgreSQL 15+, standard SQL) বেশি flexible: condition-সহ একাধিক `WHEN MATCHED`/`WHEN NOT MATCHED` branch, delete, আর PG17-এ `WHEN NOT MATCHED BY SOURCE` আর `merge_action()`-সহ `RETURNING`। কিন্তু concurrency-তে অন্য session একই key insert করলে MERGE unique violation দিয়ে fail করতে পারে, তাই concurrent upsert-এর জন্য `INSERT ... ON CONFLICT`-ই প্রথম পছন্দ।
            - **PostgreSQL 18:** `RETURNING sku, old.qty AS old_qty, new.qty AS new_qty` — নতুন insert হওয়া row-এর জন্য `old` value NULL, আর `ON CONFLICT` দিয়ে update হওয়া row-এর জন্য non-NULL, তাই insert আর update আলাদা করে চেনা যায়।
            - `ON CONFLICT`, `EXCLUDED` আর `RETURNING` PostgreSQL syntax (MySQL-এ `ON DUPLICATE KEY UPDATE`)।
        """,
        tip_en=r"""Explain `EXCLUDED` and why the statement is race-free, then contrast with MERGE's concurrency behaviour. The PG18 `old`/`new` trick to distinguish inserts from updates is a nice modern touch.""",
        tip_bn=r"""`EXCLUDED` আর statement-টা কেন race-free সেটা ব্যাখ্যা করো, তারপর MERGE-এর concurrency আচরণের সাথে তুলনা করো। Insert আর update আলাদা করতে PG18-এর `old`/`new` কৌশলটা বললে আধুনিক জ্ঞানের ছাপ পড়ে।""",
        mist_en=r"""Writing `SET qty = EXCLUDED.qty` (overwrites instead of adding), or doing upserts as SELECT-then-INSERT in application code.""",
        mist_bn=r"""`SET qty = EXCLUDED.qty` লেখা (যোগ না করে overwrite করে ফেলে), অথবা application code-এ SELECT-তারপর-INSERT করে upsert করা।""",
        follow=[
            ("How would you write the same logic with `MERGE`, and when would you prefer it?", "একই logic `MERGE` দিয়ে কীভাবে লিখবে, আর কখন সেটা বেশি পছন্দ করবে?"),
            ("How can you tell which rows were inserted vs updated?", "কোন row insert হয়েছে আর কোনটা update — কীভাবে বুঝবে?"),
        ],
        related=["pg-019"],
        refs=[PG_INSERT, PG_MERGE, PG_RETURNING],
    ),
    # ------------------------------------------------------------------ pg-023
    Q(
        id="pg-023", sub="Isolation Levels & Ledger Design", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["isolation", "serializable", "write-skew", "deadlock", "hot-row"],
        ver="PostgreSQL 18", vs=False, status="stable",
        q_en=r"""You're building a wallet service with peer-to-peer transfers (think bKash/Nagad-style) on PostgreSQL. How do you keep transfers correct under concurrency? Which isolation level and locking strategy would you choose, how do you avoid deadlocks, and what would you do when one merchant account becomes a hot row receiving thousands of payments per second?""",
        q_bn=r"""PostgreSQL-এর উপর peer-to-peer transfer-সহ একটা wallet service বানাচ্ছ (bKash/Nagad ধরনের)। Concurrency-র মধ্যে transfer কীভাবে সঠিক রাখবে? কোন isolation level আর locking strategy বেছে নেবে, deadlock কীভাবে এড়াবে, আর একটা merchant account যখন প্রতি সেকেন্ডে হাজারো payment পাওয়া hot row হয়ে যায় তখন কী করবে?""",
        a_en=r"""
            **Data model:** an append-only, double-entry `ledger_entries` table (every transfer writes a debit and a credit that sum to zero) plus an `accounts.balance` column updated in the same transaction. Add `CHECK (balance >= 0)` and a `UNIQUE` idempotency key on `transfers`, so client retries can't apply a transfer twice.

            **Isolation & locking:** I'd use **Read Committed + explicit row locks** for transfers. Lock both accounts with `SELECT ... FOR UPDATE`, debit with a guard (`WHERE balance >= amount`), credit, insert ledger rows, commit. It's fast and easy to reason about because each transfer only touches two rows.

            **Deadlocks:** A→B and B→A at the same time deadlock if each locks its "from" account first. Always lock in a **consistent order** (lowest account id first). PostgreSQL detects deadlocks after `deadlock_timeout` (1s default) and aborts one transaction with SQLSTATE `40P01`, so keep a retry path anyway.

            **When Serializable:** for invariants spanning multiple rows that row locks don't cover — e.g. "a user's daily outgoing total across all their accounts must stay under the limit" (write skew). `SERIALIZABLE` (SSI) detects such anomalies and aborts with `40001`; the app must retry the whole transaction.

            **Hot merchant row:** every credit serialises on one row lock. Options: keep the lock window tiny (lock it last, commit fast); don't update the balance synchronously for **credits** — just append ledger entries and roll them up periodically (balance = snapshot + recent entries); or split the merchant balance into N **bucket rows** and credit a random bucket (balance = sum of buckets). Debits still need a real-time check, but merchants debit far less often.
        """,
        a_bn=r"""
            **Data model:** একটা append-only, double-entry `ledger_entries` table (প্রতিটা transfer একটা debit আর একটা credit লেখে, যোগফল শূন্য) আর একই transaction-এ update হওয়া `accounts.balance` column। `CHECK (balance >= 0)` আর `transfers`-এ একটা `UNIQUE` idempotency key দাও, যাতে client retry-তে একই transfer দুবার apply না হয়।

            **Isolation আর locking:** transfer-এর জন্য আমি **Read Committed + explicit row lock** ব্যবহার করব। `SELECT ... FOR UPDATE` দিয়ে দুটো account lock করো, guard-সহ debit (`WHERE balance >= amount`), credit, ledger row insert, তারপর commit। এটা দ্রুত আর বোঝা সহজ, কারণ প্রতিটা transfer শুধু দুটো row ছোঁয়।

            **Deadlock:** A→B আর B→A একসাথে চললে, দুজনেই নিজের "from" account আগে lock করলে deadlock হয়। সবসময় **একই ক্রমে** lock করো (ছোট account id আগে)। PostgreSQL `deadlock_timeout`-এর (default 1s) পর deadlock ধরে একটা transaction-কে SQLSTATE `40P01` দিয়ে abort করে — তাই retry-র ব্যবস্থা তবুও রাখো।

            **কখন Serializable:** যখন invariant একাধিক row জুড়ে থাকে আর row lock তা ঢাকে না — যেমন "একজন user-এর সব account মিলিয়ে দিনের মোট outgoing limit-এর নিচে থাকতে হবে" (write skew)। `SERIALIZABLE` (SSI) এমন anomaly ধরে `40001` দিয়ে abort করে; app-কে পুরো transaction আবার চালাতে হয়।

            **Hot merchant row:** প্রতিটা credit একটা row lock-এর পেছনে লাইনে দাঁড়ায়। উপায়: lock-এর সময় খুব ছোট রাখো (সবশেষে lock করো, দ্রুত commit করো); **credit**-এর জন্য balance সাথে সাথে update না করে শুধু ledger entry append করো আর নিয়মিত roll up করো (balance = snapshot + সাম্প্রতিক entry); অথবা merchant balance-কে N-টা **bucket row**-তে ভাগ করে random bucket-এ credit করো (balance = bucket-গুলোর যোগফল)। Debit-এ এখনো real-time check লাগে, তবে merchant-রা debit অনেক কম করে।
        """,
        ex_en=r"""
            - **Anomalies by level (PostgreSQL):** no dirty reads at any level. Read Committed allows non-repeatable reads and lost updates if you do read-modify-write in the app. Repeatable Read gives one snapshot per transaction and raises `40001` if you try to update a row someone else changed after your snapshot — but still allows **write skew** (two transactions read overlapping data and write different rows). Serializable prevents write skew too.
            - Classic write-skew example: two on-call doctors each check "is someone else still on call?" and both go off call. Each updated a different row, so row locks never conflicted.
            - Serializable costs: extra predicate-lock tracking and false-positive aborts under high contention; keep transactions short and make retries automatic (with backoff and the idempotency key).
            - Set `lock_timeout` so a request waiting behind a hot row fails fast instead of piling up connections; enable `log_lock_waits` to see contention.
            - The ledger is your source of truth: you can always rebuild and reconcile balances from it, which also helps audits and regulators.
        """,
        ex_bn=r"""
            - **Level অনুযায়ী anomaly (PostgreSQL):** কোনো level-এই dirty read নেই। Read Committed-এ non-repeatable read হয়, আর app-এ read-modify-write করলে lost update-ও হয়। Repeatable Read পুরো transaction-এ একটা snapshot দেয়, আর তোমার snapshot-এর পরে অন্য কেউ বদলেছে এমন row update করতে গেলে `40001` দেয় — কিন্তু তবুও **write skew** হতে পারে (দুটো transaction overlapping data পড়ে আর আলাদা row-এ লেখে)। Serializable write skew-ও আটকায়।
            - Write skew-এর classic উদাহরণ: দুজন on-call doctor প্রত্যেকে দেখে "আর কেউ কি on call আছে?" আর দুজনেই off call হয়ে যায়। দুজনে আলাদা row update করেছে, তাই row lock-এ কোনো সংঘাত হয়নি।
            - Serializable-এর খরচ: বাড়তি predicate-lock tracking আর বেশি contention-এ false-positive abort; transaction ছোট রাখো আর retry automatic করো (backoff আর idempotency key-সহ)।
            - `lock_timeout` দাও, যাতে hot row-এর পেছনে অপেক্ষারত request জমে connection শেষ না করে দ্রুত fail করে; contention দেখতে `log_lock_waits` চালু করো।
            - Ledger-ই তোমার source of truth: এখান থেকে সবসময় balance আবার বানানো আর মেলানো যায়, যা audit আর regulator-এর জন্যও কাজে লাগে।
        """,
        tip_en=r"""Structure the answer: model → isolation choice with reasoning → deadlock prevention → hot-row strategy. Naming the SQLSTATE codes (`40001`, `40P01`) and giving a concrete write-skew example signals real production experience.""",
        tip_bn=r"""উত্তর সাজাও: model → কারণসহ isolation-এর পছন্দ → deadlock প্রতিরোধ → hot-row strategy। SQLSTATE code (`40001`, `40P01`) উল্লেখ করা আর write skew-এর একটা concrete উদাহরণ দেওয়া বোঝায় তোমার সত্যিকারের production অভিজ্ঞতা আছে।""",
        mist_en=r"""Choosing `SERIALIZABLE` without retry logic, locking accounts in request order (deadlocks), or storing only a mutable balance with no ledger to reconcile against.""",
        mist_bn=r"""Retry logic ছাড়া `SERIALIZABLE` বেছে নেওয়া, request-এর ক্রমে account lock করা (deadlock হয়), অথবা মেলানোর মতো কোনো ledger না রেখে শুধু পরিবর্তনশীল balance রাখা।""",
        code=r"""
            -- transfer 500.00 from account 42 to account 7
            BEGIN;

            -- 1. idempotency: a client retry with the same key fails on the UNIQUE constraint
            INSERT INTO transfers (idempotency_key, from_account, to_account, amount)
            VALUES ('9b2f6c1e-retry-safe-key', 42, 7, 500.00)
            RETURNING id;                                  -- e.g. 9001

            -- 2. lock both accounts in a consistent order (lowest id first) -> no A<->B deadlock
            SELECT id FROM accounts WHERE id IN (7, 42) ORDER BY id FOR UPDATE;

            -- 3. guarded debit, credit, double-entry ledger
            UPDATE accounts SET balance = balance - 500.00 WHERE id = 42 AND balance >= 500.00;
            -- app: if 0 rows were updated -> ROLLBACK (insufficient funds)
            UPDATE accounts SET balance = balance + 500.00 WHERE id = 7;
            INSERT INTO ledger_entries (transfer_id, account_id, amount)
            VALUES (9001, 42, -500.00), (9001, 7, 500.00);

            COMMIT;
        """,
        lang="sql",
        follow=[
            ("Show a write-skew example and how SERIALIZABLE prevents it.", "একটা write-skew উদাহরণ দেখাও, আর SERIALIZABLE কীভাবে সেটা আটকায়।"),
            ("How would you reconcile the balances table with the ledger nightly?", "প্রতি রাতে balances table-কে ledger-এর সাথে কীভাবে মেলাবে?"),
            ("How do you find which queries are waiting on locks right now?", "এই মুহূর্তে কোন query-গুলো lock-এর জন্য অপেক্ষা করছে কীভাবে খুঁজবে?"),
        ],
        related=["pg-008", "pg-019", "pg-020"],
        refs=[PG_ISO, PG_LOCKING],
    ),
    # ------------------------------------------------------------------ pg-024
    Q(
        id="pg-024", sub="Query Planning & EXPLAIN ANALYZE", diff="hard", type="debugging",
        prio="high", market="both", mins=10,
        tags=["explain-analyze", "statistics", "analyze", "nested-loop", "row-estimates"],
        ver="PostgreSQL 18 (EXPLAIN output format)", vs=True, status="stable",
        q_en=r"""Right after a release that introduced a new payment status `under_review` (and a backfill that inserted 200,000 such rows), the "payments under review" endpoint went from milliseconds to ~18 seconds. Here is the `EXPLAIN (ANALYZE)` output from PostgreSQL 18. What is wrong, and how do you fix it and prevent it from happening again?""",
        q_bn=r"""নতুন payment status `under_review` চালু করা একটা release-এর ঠিক পরে (আর একটা backfill যেটা এমন ২,০০,০০০ row insert করেছে), "under review payments" endpoint কয়েক millisecond থেকে ~১৮ সেকেন্ডে চলে গেছে। নিচে PostgreSQL 18-এর `EXPLAIN (ANALYZE)` output। সমস্যা কী, আর কীভাবে ঠিক করবে এবং ভবিষ্যতে আটকাবে?""",
        code=r"""
            EXPLAIN (ANALYZE)
            SELECT p.id, p.amount, e.event_type, e.created_at
            FROM payments p
            JOIN payment_events e ON e.payment_id = p.id
            WHERE p.status = 'under_review';

                                                    QUERY PLAN
            ---------------------------------------------------------------------------------------------------------------
             Nested Loop  (cost=0.86..13.27 rows=3 width=31) (actual time=0.061..18421.507 rows=600000.00 loops=1)
               Buffers: shared hit=612480 read=193110
               ->  Index Scan using idx_payments_status on payments p  (cost=0.43..4.76 rows=1 width=14) (actual time=0.034..612.354 rows=200000.00 loops=1)
                     Index Cond: (status = 'under_review'::text)
                     Index Searches: 1
                     Buffers: shared hit=3 read=1824
               ->  Index Scan using idx_events_payment_id on payment_events e  (cost=0.43..8.48 rows=3 width=25) (actual time=0.085..0.088 rows=3.00 loops=200000)
                     Index Cond: (payment_id = p.id)
                     Index Searches: 200000
                     Buffers: shared hit=612477 read=191286
             Planning Time: 0.573 ms
             Execution Time: 18496.120 ms
        """,
        lang="text",
        extra=[dict(lang="sql", label_en="Fix and prevention", label_bn="সমাধান আর প্রতিরোধ", src=r"""
            -- 1. confirm: statistics are stale
            SELECT n_live_tup, n_mod_since_analyze, last_analyze, last_autoanalyze
            FROM pg_stat_user_tables
            WHERE relname = 'payments';

            -- 2. immediate fix: refresh statistics (cheap: it samples rows)
            ANALYZE payments;

            -- re-check: the estimate is now close to reality and the planner switches plans
            --  Gather  (cost=9141.69..112426.20 rows=554310 width=31) (actual ... rows=600000.00 loops=1)
            --    ->  Parallel Hash Join  ... Hash Cond: (e.payment_id = p.id)
            --          ->  Parallel Seq Scan on payment_events e ...
            --          ->  Parallel Hash -> Parallel Index Scan using idx_payments_status on payments p ...

            -- 3. prevention: analyze big, hot tables more eagerly ...
            ALTER TABLE payments SET (autovacuum_analyze_scale_factor = 0.02);
            -- ... and end every backfill / bulk-load job with: ANALYZE payments;

            -- 4. if estimates are still wrong because columns are correlated:
            CREATE STATISTICS payments_status_merchant (dependencies, ndistinct, mcv)
              ON status, merchant_id FROM payments;
            ANALYZE payments;
        """)],
        a_en=r"""
            Compare **estimated vs actual rows**. The planner expected `rows=1` from `payments` with `status = 'under_review'` but got **200,000**. Because it thought one payment would match, a **Nested Loop** with an index lookup into `payment_events` looked almost free (total cost 13). In reality the inner index scan ran **200,000 times** (`loops=200000`), with ~191k buffer reads from disk — that's where the 18 seconds went.

            **Root cause:** stale statistics. The last `ANALYZE` ran before the new status existed, so the column statistics say `under_review` is essentially absent. Autovacuum's auto-analyze hadn't caught up after the backfill yet (`n_mod_since_analyze` shows the 200k changes).

            **Fix:** run `ANALYZE payments;`. With correct estimates (~550k rows), the planner picks a hash join instead. Cached plans are invalidated automatically.

            **Prevention:** make bulk-load/backfill jobs run `ANALYZE` when they finish; lower `autovacuum_analyze_scale_factor` for large hot tables; monitor `n_mod_since_analyze` and slow-query plans (`auto_explain`, `pg_stat_statements`).
        """,
        a_bn=r"""
            **Estimated বনাম actual row** তুলনা করো। Planner ভেবেছিল `status = 'under_review'` দিয়ে `payments` থেকে `rows=1` আসবে, কিন্তু এসেছে **২,০০,০০০**। একটা payment match করবে ভেবে `payment_events`-এ index lookup-সহ **Nested Loop** প্রায় বিনামূল্যে মনে হয়েছে (মোট cost 13)। বাস্তবে inner index scan **২,০০,০০০ বার** চলেছে (`loops=200000`), disk থেকে ~১,৯১,০০০ buffer read-সহ — ১৮ সেকেন্ড ওখানেই গেছে।

            **Root cause:** পুরনো (stale) statistics। শেষ `ANALYZE` নতুন status আসার আগেই চলেছিল, তাই column statistics বলছে `under_review` কার্যত নেই। Backfill-এর পর autovacuum-এর auto-analyze তখনো ধরতে পারেনি (`n_mod_since_analyze`-এ ২ লাখ পরিবর্তন দেখা যায়)।

            **সমাধান:** `ANALYZE payments;` চালাও। সঠিক estimate (~৫.৫ লাখ row) পেলে planner hash join বেছে নেয়। Cached plan নিজে থেকেই invalidate হয়ে যায়।

            **প্রতিরোধ:** bulk-load/backfill job শেষে `ANALYZE` চালাবে; বড় আর ব্যস্ত table-এর জন্য `autovacuum_analyze_scale_factor` কমাও; `n_mod_since_analyze` আর ধীর query-র plan নজরে রাখো (`auto_explain`, `pg_stat_statements`)।
        """,
        ex_en=r"""
            - **How to read it:** in each node, `cost=...rows=N` is the estimate and `actual ... rows=N loops=L` is reality (PG18 prints actual rows with decimals; total rows = rows × loops). A mismatch of 10× or more is the first thing to look for. In PG18, `BUFFERS` is included automatically with `ANALYZE`, and `Index Searches` shows how many index descents happened.
            - Auto-analyze triggers after roughly `autovacuum_analyze_threshold + autovacuum_analyze_scale_factor × rows` changes (defaults 50 + 10%). On a 100M-row table that's 10M changes — far too late for a new hot value.
            - Other estimate killers: **correlated columns** (the planner multiplies selectivities as if independent → fix with `CREATE STATISTICS`), heavily skewed values (raise the column's statistics target), functions in predicates, and generic plans for prepared statements.
            - Avoid global hacks like `SET enable_nestloop = off` — they fix one query and break others.
            - Nice PG18 detail: `pg_upgrade` now keeps optimizer statistics, so you no longer get a wave of bad plans right after a major upgrade (extended statistics still need `ANALYZE`).
        """,
        ex_bn=r"""
            - **কীভাবে পড়বে:** প্রতিটা node-এ `cost=...rows=N` হলো আনুমানিক, আর `actual ... rows=N loops=L` হলো বাস্তব (PG18 actual row দশমিকসহ দেখায়; মোট row = rows × loops)। ১০ গুণ বা তার বেশি গরমিলই প্রথমে খুঁজবে। PG18-এ `ANALYZE`-এর সাথে `BUFFERS` নিজে থেকেই আসে, আর `Index Searches` দেখায় index-এ কতবার ঢোকা হয়েছে।
            - Auto-analyze মোটামুটি `autovacuum_analyze_threshold + autovacuum_analyze_scale_factor × rows` পরিবর্তনের পর চলে (default 50 + 10%)। ১০ কোটি row-এর table-এ সেটা ১ কোটি পরিবর্তন — নতুন একটা hot value-এর জন্য অনেক দেরি।
            - Estimate নষ্ট করার আরও কারণ: **correlated column** (planner selectivity-গুলো স্বাধীন ধরে গুণ করে → `CREATE STATISTICS` দিয়ে ঠিক করো), খুব skewed value (column-এর statistics target বাড়াও), predicate-এ function, আর prepared statement-এর generic plan।
            - `SET enable_nestloop = off`-এর মতো global hack এড়িয়ে চলো — একটা query ঠিক করে অন্যগুলো ভেঙে দেয়।
            - PG18-এর একটা ভালো দিক: `pg_upgrade` এখন optimizer statistics রেখে দেয়, তাই major upgrade-এর ঠিক পরে খারাপ plan-এর ঢেউ আর আসে না (extended statistics-এর জন্য তবুও `ANALYZE` লাগে)।
        """,
        tip_en=r"""Say out loud: "estimated 1, actual 200,000 — the plan was chosen on wrong numbers." Then root cause → immediate fix → prevention. That structure is exactly what interviewers want in a production-debugging answer.""",
        tip_bn=r"""জোরে বলো: "আনুমানিক 1, বাস্তবে ২,০০,০০০ — ভুল সংখ্যার উপর plan বাছা হয়েছে।" তারপর root cause → তাৎক্ষণিক fix → প্রতিরোধ। Production-debugging উত্তরে interviewer ঠিক এই কাঠামোটাই চায়।""",
        mist_en=r"""Adding more indexes or disabling nested loops instead of fixing the estimates, or reading only the top-level execution time without comparing estimated and actual rows per node.""",
        mist_bn=r"""Estimate ঠিক না করে আরও index যোগ করা বা nested loop বন্ধ করে দেওয়া, অথবা প্রতিটা node-এ estimated আর actual row তুলনা না করে শুধু উপরের execution time পড়া।""",
        follow=[
            ("When would you use `CREATE STATISTICS`, and which kinds exist?", "কখন `CREATE STATISTICS` ব্যবহার করবে, আর কী কী ধরন আছে?"),
            ("How do generic vs custom plans for prepared statements affect this kind of problem?", "Prepared statement-এর generic বনাম custom plan এ ধরনের সমস্যায় কী প্রভাব ফেলে?"),
        ],
        related=["pg-009", "pg-031", "pg-015"],
        refs=[PG_USING_EXPLAIN, PG_PLANNER_STATS, PG_VACUUM],
    ),
]

if __name__ == "__main__":
    save("postgresql", "b3", QUESTIONS)
