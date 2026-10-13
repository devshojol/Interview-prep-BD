# PostgreSQL batch 1 — pg-001 … pg-008 (fundamentals, easy)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_CONSTRAINTS = ("PostgreSQL docs — Constraints", "https://www.postgresql.org/docs/current/ddl-constraints.html")
PG_ARRAYS = ("PostgreSQL docs — Arrays", "https://www.postgresql.org/docs/current/arrays.html")
PG_NUMERIC = ("PostgreSQL docs — Numeric Types", "https://www.postgresql.org/docs/current/datatype-numeric.html")
PG_MONEY = ("PostgreSQL docs — Monetary Types", "https://www.postgresql.org/docs/current/datatype-money.html")
PG_INDEXES = ("PostgreSQL docs — Indexes", "https://www.postgresql.org/docs/current/indexes.html")
PG_INDEX_TYPES = ("PostgreSQL docs — Index Types", "https://www.postgresql.org/docs/current/indexes-types.html")
PG_TX_TUTORIAL = ("PostgreSQL docs — Transactions (tutorial)", "https://www.postgresql.org/docs/current/tutorial-transactions.html")
PG_SAVEPOINT = ("PostgreSQL docs — SAVEPOINT", "https://www.postgresql.org/docs/current/sql-savepoint.html")
PG_MVCC = ("PostgreSQL docs — Concurrency Control (MVCC)", "https://www.postgresql.org/docs/current/mvcc.html")
PG_MVCC_INTRO = ("PostgreSQL docs — Introduction to MVCC", "https://www.postgresql.org/docs/current/mvcc-intro.html")
PG_ISO = ("PostgreSQL docs — Transaction Isolation", "https://www.postgresql.org/docs/current/transaction-iso.html")
PG_VACUUM = ("PostgreSQL docs — Routine Vacuuming", "https://www.postgresql.org/docs/current/routine-vacuuming.html")

QUESTIONS = [
    # ------------------------------------------------------------------ pg-001
    Q(
        id="pg-001", sub="Relational Fundamentals & Normalization", diff="easy", type="scenario",
        prio="high", market="both", mins=4,
        tags=["normalization", "1nf", "many-to-many", "junction-table", "foreign-key"],
        ver="Version-independent concept (examples use PostgreSQL 18 syntax)", vs=False, status="stable",
        q_en=r"""A teammate stores product tags as a comma-separated string in `products.tags` (for example `'phone,android,5g'`). What problems does this cause, and how would you model it properly in PostgreSQL?""",
        q_bn=r"""একজন teammate product-এর tag-গুলো `products.tags` column-এ comma-separated string হিসেবে রাখছে (যেমন `'phone,android,5g'`)। এতে কী কী সমস্যা হয়, আর PostgreSQL-এ এটা ঠিকভাবে কীভাবে model করবে?""",
        a_en=r"""
            A comma-separated list breaks **First Normal Form (1NF)**: one column holds many values, so the database can't treat each tag as data. In practice:

            - Searching is fragile and slow: `tags LIKE '%5g%'` also matches `45g`, and it can't use a normal B-tree index.
            - No integrity: nothing stops typos like `andriod`, and there's no foreign key to a tags table.
            - Renaming a tag or counting products per tag needs string surgery on every row.

            Products and tags are a **many-to-many** relationship, so I'd model it with a `tags` table plus a junction table `product_tags(product_id, tag_id)` with a composite primary key and two foreign keys. One-to-many is simpler: just a foreign key column on the "many" side (e.g. `orders.customer_id`).
        """,
        a_bn=r"""
            Comma-separated list **First Normal Form (1NF)** ভাঙে: একটা column-এ অনেকগুলো value থাকে, তাই database প্রতিটা tag-কে আলাদা data হিসেবে চিনতে পারে না। বাস্তবে সমস্যা হয়:

            - Search ভঙ্গুর আর ধীর: `tags LIKE '%5g%'` দিলে `45g`-ও match করে, আর সাধারণ B-tree index কাজে লাগে না।
            - Integrity নেই: `andriod`-এর মতো typo আটকানোর কিছু নেই, tags table-এ কোনো foreign key-ও নেই।
            - একটা tag rename করা বা tag অনুযায়ী product গোনা — সবকিছুতে প্রতিটা row-এর string কাটাছেঁড়া করতে হয়।

            Product আর tag-এর সম্পর্ক **many-to-many**, তাই আমি একটা `tags` table আর একটা junction table `product_tags(product_id, tag_id)` বানাব — composite primary key আর দুটো foreign key সহ। One-to-many আরও সহজ: "many" দিকের table-এ একটা foreign key column (যেমন `orders.customer_id`)।
        """,
        ex_en=r"""
            - The junction table's primary key `(product_id, tag_id)` prevents duplicate pairs and already serves lookups by `product_id`. Add a separate index on `tag_id` for "all products with tag X" queries.
            - `ON DELETE CASCADE` on the junction table's foreign keys removes the links automatically when a product or tag is deleted.
            - **Alternative:** a `text[]` array column with a GIN index (`WHERE tags @> ARRAY['5g']`) is acceptable when tags are free-form labels with no attributes of their own and you don't need foreign-key integrity. It's simpler to read/write but you lose referential integrity and per-tag metadata.
            - Normalization is about removing redundancy and update anomalies; you may denormalize later for read performance, but start from a clean model.
        """,
        ex_bn=r"""
            - Junction table-এর primary key `(product_id, tag_id)` duplicate pair আটকায়, আর `product_id` দিয়ে lookup-এর কাজও করে। "X tag-ওয়ালা সব product" query-র জন্য `tag_id`-তে আলাদা index দাও।
            - Junction table-এর foreign key-তে `ON DELETE CASCADE` থাকলে product বা tag delete হলে link-গুলো নিজে থেকেই মুছে যায়।
            - **বিকল্প:** `text[]` array column আর GIN index (`WHERE tags @> ARRAY['5g']`) চলতে পারে, যদি tag শুধু free-form label হয়, নিজস্ব কোনো attribute না থাকে আর foreign-key integrity দরকার না হয়। পড়া-লেখা সহজ, কিন্তু referential integrity আর per-tag metadata হারাও।
            - Normalization-এর উদ্দেশ্য redundancy আর update anomaly দূর করা; পরে read performance-এর জন্য denormalize করতে পারো, কিন্তু শুরু করো একটা clean model দিয়ে।
        """,
        tip_en=r"""Name the rule (1NF), give one concrete failure (`LIKE '%5g%'` matching `45g`), then sketch the junction table. Mentioning the array + GIN alternative and its trade-off shows maturity.""",
        tip_bn=r"""প্রথমে rule-টার নাম বলো (1NF), একটা concrete failure দেখাও (`LIKE '%5g%'` দিয়ে `45g` match হওয়া), তারপর junction table-টা এঁকে দেখাও। Array + GIN বিকল্প আর তার trade-off বললে বোঝা যায় তুমি বাস্তব অভিজ্ঞতা থেকে ভাবছ।""",
        mist_en=r"""Forgetting the composite primary key on the junction table (allowing duplicate links), or forgetting an index on `tag_id` for reverse lookups.""",
        mist_bn=r"""Junction table-এ composite primary key না দেওয়া (ফলে duplicate link ঢুকে যায়), অথবা উল্টো দিকের lookup-এর জন্য `tag_id`-তে index না দেওয়া।""",
        code=r"""
            CREATE TABLE products (
              id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              name  text NOT NULL
            );

            CREATE TABLE tags (
              id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              name  text NOT NULL UNIQUE
            );

            -- junction (bridge) table for the many-to-many relationship
            CREATE TABLE product_tags (
              product_id bigint NOT NULL REFERENCES products(id) ON DELETE CASCADE,
              tag_id     bigint NOT NULL REFERENCES tags(id)     ON DELETE CASCADE,
              PRIMARY KEY (product_id, tag_id)
            );
            CREATE INDEX ON product_tags (tag_id);   -- "all products with tag X"

            -- all products tagged '5g' (no false match on '45g')
            SELECT p.id, p.name
            FROM products p
            JOIN product_tags pt ON pt.product_id = p.id
            JOIN tags t          ON t.id = pt.tag_id
            WHERE t.name = '5g';
        """,
        lang="sql",
        follow=[
            ("When would a `text[]` column with a GIN index be a reasonable choice instead?", "কখন junction table-এর বদলে GIN index সহ `text[]` column ব্যবহার করা যুক্তিসঙ্গত?"),
            ("What is 2NF and 3NF? Give an example of a 3NF violation.", "2NF আর 3NF কী? 3NF ভাঙার একটা উদাহরণ দাও।"),
        ],
        related=["pg-002", "pg-004"],
        refs=[PG_CONSTRAINTS, PG_ARRAYS],
    ),
    # ------------------------------------------------------------------ pg-002
    Q(
        id="pg-002", sub="Primary & Foreign Keys", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["foreign-key", "index", "primary-key", "performance"],
        ver="Version-independent (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""You declare `orders.customer_id bigint REFERENCES customers(id)`. Which statement about indexes is true in PostgreSQL?""",
        q_bn=r"""তুমি `orders.customer_id bigint REFERENCES customers(id)` declare করলে। PostgreSQL-এ index নিয়ে কোন কথাটা সত্য?""",
        options=[
            ("PostgreSQL automatically creates an index on `orders.customer_id` when the foreign key is created.",
             "Foreign key তৈরির সময় PostgreSQL নিজে থেকেই `orders.customer_id`-তে index বানিয়ে দেয়।"),
            ("The referenced column `customers.id` must have a primary key or unique constraint (so it is indexed), but `orders.customer_id` is not indexed automatically — you usually add that index yourself.",
             "Referenced column `customers.id`-এ primary key বা unique constraint থাকতেই হবে (তাই সেটা indexed), কিন্তু `orders.customer_id`-তে automatically index হয় না — সাধারণত সেটা নিজেকেই বানাতে হয়।"),
            ("Neither side needs an index; PostgreSQL always checks foreign keys with sequential scans by design.",
             "কোনো দিকেই index লাগে না; PostgreSQL design অনুযায়ী সবসময় sequential scan দিয়ে foreign key check করে।"),
            ("The foreign key can't be created until you manually create an index on `orders.customer_id`.",
             "`orders.customer_id`-তে নিজে index না বানানো পর্যন্ত foreign key তৈরি করা যায় না।"),
        ],
        correct=1,
        a_en=r"""The second option is correct. PostgreSQL requires the **referenced** columns to be a primary key or have a unique constraint (which is backed by an index), but it does **not** create an index on the **referencing** column. You normally add `CREATE INDEX ON orders (customer_id);` yourself.""",
        a_bn=r"""দ্বিতীয় option-টা সঠিক। PostgreSQL **referenced** column-কে primary key বা unique constraint হতে বাধ্য করে (যার পেছনে একটা index থাকে), কিন্তু **referencing** column-এ নিজে থেকে index বানায় না। সাধারণত `CREATE INDEX ON orders (customer_id);` নিজেকেই দিতে হয়।""",
        ex_en=r"""
            Why it matters: when you delete or update a row in `customers`, PostgreSQL must find matching rows in `orders` (to block the delete, or to cascade it). Without an index on `orders.customer_id`, that's a sequential scan of `orders` for every deleted customer — painful on big tables. Joins and "orders of customer X" queries also need that index.

            The first option is the tempting trap: MySQL's InnoDB does create an index on foreign-key columns automatically, so developers coming from MySQL often assume PostgreSQL does too. PostgreSQL leaves it to you because not every workload needs it (e.g. a rarely-deleted parent with a small child table).
        """,
        ex_bn=r"""
            কেন গুরুত্বপূর্ণ: `customers` থেকে কোনো row delete বা update করলে PostgreSQL-কে `orders`-এ matching row খুঁজতে হয় (delete আটকাতে বা cascade করতে)। `orders.customer_id`-তে index না থাকলে প্রতিটা customer delete-এ পুরো `orders` table sequential scan হয় — বড় table-এ এটা খুব কষ্টের। Join আর "X customer-এর order" ধরনের query-তেও এই index লাগে।

            প্রথম option-টাই আসল ফাঁদ: MySQL-এর InnoDB foreign-key column-এ automatically index বানায়, তাই MySQL থেকে আসা developer-রা ধরে নেয় PostgreSQL-ও তাই করে। PostgreSQL এটা তোমার উপর ছেড়ে দেয়, কারণ সব workload-এ এটা দরকার হয় না (যেমন parent row খুব কম delete হয় আর child table ছোট)।
        """,
        tip_en=r"""Add the "why": parent deletes/updates and joins scan the child table. Contrasting with MySQL InnoDB shows cross-database awareness.""",
        tip_bn=r""""কেন" অংশটা যোগ করো: parent delete/update আর join-এর সময় child table scan হয়। MySQL InnoDB-র সাথে তুলনা করলে বোঝা যায় তুমি একাধিক database নিয়ে সচেতন।""",
        extra=[dict(lang="sql", label_en="Foreign key plus the index you add yourself",
                    label_bn="Foreign key আর নিজে থেকে যোগ করা index", src=r"""
            CREATE TABLE orders (
              id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              customer_id bigint NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
              total       numeric(12,2) NOT NULL
            );
            CREATE INDEX idx_orders_customer_id ON orders (customer_id);
        """)],
        related=["pg-001", "pg-005"],
        refs=[PG_CONSTRAINTS, PG_INDEXES],
    ),
    # ------------------------------------------------------------------ pg-003
    Q(
        id="pg-003", sub="Data Types", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["numeric", "money", "floating-point", "data-types"],
        ver="Version-independent (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Which PostgreSQL column type is the best choice for prices and account balances such as `1999.99` BDT?""",
        q_bn=r"""`1999.99` BDT-এর মতো price আর account balance রাখার জন্য PostgreSQL-এ কোন column type সবচেয়ে ভালো?""",
        options=[
            ("`real`", "`real`"),
            ("`double precision`", "`double precision`"),
            ("`numeric(12,2)`", "`numeric(12,2)`"),
            ("`money`", "`money`"),
        ],
        correct=2,
        a_en=r"""`numeric(12,2)` (exact decimal arithmetic). `real` and `double precision` are binary floating-point types that can't represent most decimal fractions exactly, so sums drift — never acceptable for money. Another valid design is storing integer minor units (paisa) in a `bigint`.""",
        a_bn=r"""`numeric(12,2)` (exact decimal arithmetic)। `real` আর `double precision` হলো binary floating-point type — বেশিরভাগ decimal ভগ্নাংশ এগুলো হুবহু রাখতে পারে না, তাই যোগফলে ছোট ছোট ভুল জমে — টাকার হিসাবে এটা কখনোই চলে না। আরেকটা ঠিক design হলো `bigint`-এ integer minor unit (পয়সা) রাখা।""",
        ex_en=r"""
            Try it: `SELECT 0.1::float8 + 0.2::float8;` returns `0.30000000000000004`, while `0.1::numeric + 0.2::numeric` returns `0.3`.

            The tempting wrong answer is `money`. It looks purpose-built, but its output format and fractional precision depend on the `lc_monetary` locale setting, it doesn't store a currency, and it's awkward to combine with other numeric types. Most teams use `numeric` (plus a `currency` column if you handle more than one currency). `numeric` is slower than integers for heavy arithmetic, which is why some payment systems store paisa/cents as `bigint`.
        """,
        ex_bn=r"""
            চালিয়ে দেখো: `SELECT 0.1::float8 + 0.2::float8;` দেয় `0.30000000000000004`, আর `0.1::numeric + 0.2::numeric` দেয় `0.3`।

            লোভনীয় ভুল উত্তর হলো `money`। নাম দেখে মনে হয় এটা টাকার জন্যই বানানো, কিন্তু এর output format আর fractional precision `lc_monetary` locale setting-এর উপর নির্ভর করে, currency সংরক্ষণ করে না, আর অন্য numeric type-এর সাথে মেলাতে ঝামেলা। বেশিরভাগ team `numeric` ব্যবহার করে (একাধিক currency থাকলে সাথে একটা `currency` column)। ভারী arithmetic-এ `numeric` integer-এর চেয়ে ধীর — এজন্য কিছু payment system পয়সা/cent `bigint`-এ রাখে।
        """,
        tip_en=r"""Show the `0.1 + 0.2` example — it proves you understand *why*, not just the rule. Mention the integer-minor-units alternative.""",
        tip_bn=r"""`0.1 + 0.2` উদাহরণটা দেখাও — এতে বোঝা যায় তুমি শুধু rule মুখস্থ করোনি, *কেন* সেটাও জানো। Integer minor unit-এর বিকল্পটাও উল্লেখ করো।""",
        extra=[dict(lang="sql", label_en="Float vs numeric in psql", label_bn="psql-এ float বনাম numeric", src=r"""
            SELECT 0.1::float8 + 0.2::float8   AS float_sum,     -- 0.30000000000000004
                   0.1::numeric + 0.2::numeric AS numeric_sum;   -- 0.3
        """)],
        related=["pg-012"],
        refs=[PG_NUMERIC, PG_MONEY],
    ),
    # ------------------------------------------------------------------ pg-004
    Q(
        id="pg-004", sub="Constraints", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["constraints", "unique", "check", "exclude", "nulls-not-distinct"],
        ver="PostgreSQL 18 (NULLS NOT DISTINCT since 15)", vs=True, status="stable",
        q_en=r"""What kinds of constraints does PostgreSQL support, and how do NULL values behave in a `UNIQUE` constraint?""",
        q_bn=r"""PostgreSQL কী কী ধরনের constraint support করে, আর `UNIQUE` constraint-এ NULL value কেমন আচরণ করে?""",
        a_en=r"""
            PostgreSQL supports `NOT NULL`, `CHECK`, `UNIQUE`, `PRIMARY KEY` (unique + not null), `FOREIGN KEY`, and `EXCLUDE` constraints. They enforce rules in the database itself, so every app, script, or manual fix has to obey them.

            For `UNIQUE`, NULLs are treated as **distinct** by default, so you can insert many rows with a NULL in that column. Since PostgreSQL 15 you can write `UNIQUE NULLS NOT DISTINCT` to treat NULLs as equal, allowing only one.
        """,
        a_bn=r"""
            PostgreSQL `NOT NULL`, `CHECK`, `UNIQUE`, `PRIMARY KEY` (unique + not null), `FOREIGN KEY` আর `EXCLUDE` constraint support করে। এগুলো rule-গুলো database-এর ভেতরেই enforce করে, তাই যেকোনো app, script বা হাতে করা fix — সবাইকে এগুলো মানতে হয়।

            `UNIQUE`-এ default-ভাবে NULL-গুলোকে **আলাদা (distinct)** ধরা হয়, তাই ওই column-এ NULL দিয়ে অনেকগুলো row insert করা যায়। PostgreSQL 15 থেকে `UNIQUE NULLS NOT DISTINCT` লিখলে NULL-গুলোকে সমান ধরা হয়, ফলে মাত্র একটা NULL রাখা যায়।
        """,
        ex_en=r"""
            - `CHECK` can only look at the current row; it can't query other tables (use a foreign key or a trigger for that).
            - `EXCLUDE` generalises uniqueness: "no two rows may overlap". The classic use is room booking with a GiST index on a range. Using `=` on a plain integer inside it needs the `btree_gist` extension. PostgreSQL 18 also adds temporal `PRIMARY KEY`/`UNIQUE ... WITHOUT OVERLAPS`.
            - Only `UNIQUE`, `PRIMARY KEY`, `EXCLUDE`, and foreign keys can be `DEFERRABLE` (checked at commit); `NOT NULL` and `CHECK` are always checked immediately.
            - Give constraints meaningful names — error messages and migrations become much clearer.
        """,
        ex_bn=r"""
            - `CHECK` শুধু current row দেখতে পারে; অন্য table-এ query করতে পারে না (তার জন্য foreign key বা trigger লাগে)।
            - `EXCLUDE` uniqueness-এর একটা সাধারণ রূপ: "কোনো দুটো row overlap করতে পারবে না"। Classic উদাহরণ হলো room booking — range-এর উপর GiST index দিয়ে। এর ভেতরে সাধারণ integer-এ `=` ব্যবহার করতে `btree_gist` extension লাগে। PostgreSQL 18-এ temporal `PRIMARY KEY`/`UNIQUE ... WITHOUT OVERLAPS`-ও এসেছে।
            - শুধু `UNIQUE`, `PRIMARY KEY`, `EXCLUDE` আর foreign key `DEFERRABLE` হতে পারে (commit-এর সময় check হয়); `NOT NULL` আর `CHECK` সবসময় সাথে সাথেই check হয়।
            - Constraint-এর অর্থবহ নাম দাও — error message আর migration দুটোই অনেক পরিষ্কার হয়।
        """,
        tip_en=r"""List the six types quickly, then spend your time on the interesting part: NULLs in UNIQUE and `NULLS NOT DISTINCT`. A one-line `EXCLUDE` booking example is a strong bonus.""",
        tip_bn=r"""ছয়টা type দ্রুত বলে ফেলো, তারপর সময় দাও আকর্ষণীয় অংশে: UNIQUE-এ NULL আর `NULLS NOT DISTINCT`। এক লাইনের `EXCLUDE` booking উদাহরণ দিলে বাড়তি নম্বর পাবে।""",
        mist_en=r"""Assuming a `UNIQUE` column allows only one NULL (true in SQL Server, not in PostgreSQL by default), or trying to validate data from another table inside a `CHECK`.""",
        mist_bn=r"""ধরে নেওয়া যে `UNIQUE` column-এ মাত্র একটা NULL রাখা যায় (SQL Server-এ সত্য, কিন্তু PostgreSQL-এ default-ভাবে নয়), অথবা `CHECK`-এর ভেতরে অন্য table-এর data দিয়ে validation করার চেষ্টা করা।""",
        code=r"""
            CREATE TABLE users (
              id     bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              email  text NOT NULL UNIQUE,
              age    int  CONSTRAINT users_adult CHECK (age >= 18)
            );

            -- NULL store_id = coupon valid in every store; only one such global coupon per code
            CREATE TABLE coupons (
              code      text NOT NULL,
              store_id  int,
              UNIQUE NULLS NOT DISTINCT (code, store_id)      -- PostgreSQL 15+
            );

            CREATE EXTENSION IF NOT EXISTS btree_gist;        -- lets GiST handle "room_id WITH ="
            CREATE TABLE bookings (
              id       bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
              room_id  int NOT NULL,
              during   tstzrange NOT NULL,
              EXCLUDE USING gist (room_id WITH =, during WITH &&)   -- no overlapping bookings per room
            );
        """,
        lang="sql",
        follow=[
            ("What is a deferrable constraint, and when would you need one?", "Deferrable constraint কী, আর কখন এটা দরকার হয়?"),
            ("How would you add a `CHECK` constraint to a huge existing table without a long lock?", "বড় একটা existing table-এ লম্বা lock ছাড়া কীভাবে `CHECK` constraint যোগ করবে?"),
        ],
        related=["pg-001", "pg-025"],
        refs=[PG_CONSTRAINTS],
    ),
    # ------------------------------------------------------------------ pg-005
    Q(
        id="pg-005", sub="Indexes", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["index", "b-tree", "performance", "explain"],
        ver="Version-independent (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""What is an index in PostgreSQL? When does it help, and what does it cost?""",
        q_bn=r"""PostgreSQL-এ index কী? কখন এটা কাজে লাগে, আর এর খরচ কী?""",
        a_en=r"""
            An index is a separate data structure — a **B-tree** by default — that maps column values to row locations, so PostgreSQL can find matching rows without reading the whole table.

            It helps with selective `WHERE` filters, join keys, `ORDER BY ... LIMIT`, and enforcing uniqueness (primary keys and unique constraints create one automatically).

            The costs: extra disk space, and slower writes, because every `INSERT`, `DELETE`, and `UPDATE` of an indexed column must also update the index. The planner may also ignore an index when a query matches a large share of the table — a sequential scan is cheaper then. I always confirm with `EXPLAIN`.
        """,
        a_bn=r"""
            Index হলো একটা আলাদা data structure — default-ভাবে **B-tree** — যেটা column-এর value থেকে row-এর location map করে রাখে, যাতে PostgreSQL পুরো table না পড়েই matching row খুঁজে পায়।

            এটা কাজে লাগে selective `WHERE` filter, join key, `ORDER BY ... LIMIT` আর uniqueness enforce করতে (primary key আর unique constraint নিজে থেকেই একটা index বানায়)।

            খরচ: বাড়তি disk space, আর write ধীর হয় — কারণ প্রতিটা `INSERT`, `DELETE` আর indexed column-এর `UPDATE`-এ index-ও update করতে হয়। Query যদি table-এর বড় অংশ match করে, planner index উপেক্ষা করতে পারে — তখন sequential scan সস্তা। আমি সবসময় `EXPLAIN` দিয়ে নিশ্চিত হই।
        """,
        ex_en=r"""
            - A B-tree supports `=`, `<`, `>`, `BETWEEN`, `IN`, `IS NULL`, and sorting. `LIKE 'abc%'` can use it only with the `C` collation or a `text_pattern_ops` index; `LIKE '%abc'` can't.
            - Low-selectivity columns (e.g. a boolean where 50% of rows are `true`) rarely benefit; a **partial index** on the rare value is better.
            - Updating an indexed column usually prevents a **HOT** (heap-only tuple) update, so more indexes also mean more write amplification and bloat.
            - Find indexes nobody uses via `pg_stat_user_indexes.idx_scan = 0` (check replicas too before dropping).
        """,
        ex_bn=r"""
            - B-tree `=`, `<`, `>`, `BETWEEN`, `IN`, `IS NULL` আর sorting support করে। `LIKE 'abc%'` শুধু `C` collation বা `text_pattern_ops` index থাকলে এটা ব্যবহার করতে পারে; `LIKE '%abc'` পারে না।
            - কম selectivity-র column-এ (যেমন boolean, যেখানে 50% row `true`) লাভ খুব কম; বিরল value-টার উপর **partial index** ভালো।
            - Indexed column update করলে সাধারণত **HOT** (heap-only tuple) update হতে পারে না, তাই বেশি index মানে বেশি write amplification আর bloat।
            - কেউ ব্যবহার করছে না এমন index খুঁজতে `pg_stat_user_indexes.idx_scan = 0` দেখো (drop করার আগে replica-গুলোও check করো)।
        """,
        tip_en=r"""Use the book-index analogy in one sentence, then spend most of the answer on trade-offs and "the planner decides". Interviewers want to hear that indexes are not free.""",
        tip_bn=r"""এক বাক্যে বইয়ের index-এর উদাহরণ দাও, তারপর উত্তরের বেশিরভাগ সময় দাও trade-off আর "planner সিদ্ধান্ত নেয়" অংশে। Interviewer শুনতে চায় যে index free নয়।""",
        mist_en=r"""Indexing every column "just in case", or assuming that creating an index guarantees the planner will use it.""",
        mist_bn=r""""কাজে লাগতে পারে" ভেবে সব column-এ index দেওয়া, অথবা ধরে নেওয়া যে index বানালেই planner সেটা ব্যবহার করবে।""",
        code=r"""
            CREATE INDEX idx_orders_customer_id ON orders (customer_id);

            EXPLAIN SELECT * FROM orders WHERE customer_id = 42;

            -- indexes never scanned since statistics were last reset
            SELECT relname AS table_name, indexrelname AS index_name, idx_scan
            FROM pg_stat_user_indexes
            WHERE idx_scan = 0;
        """,
        lang="sql",
        follow=[
            ("Why might PostgreSQL choose a sequential scan even though an index exists?", "Index থাকা সত্ত্বেও PostgreSQL কেন sequential scan বেছে নিতে পারে?"),
            ("What is an index-only scan?", "Index-only scan কী?"),
        ],
        related=["pg-013", "pg-014", "pg-002"],
        refs=[PG_INDEXES, PG_INDEX_TYPES],
    ),
    # ------------------------------------------------------------------ pg-006
    Q(
        id="pg-006", sub="Transactions & ACID", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["transactions", "acid", "savepoint", "transactional-ddl", "node-pg"],
        ver="Version-independent (PostgreSQL 18; node-postgres 8.x)", vs=False, status="stable",
        q_en=r"""How do transactions work in PostgreSQL? Explain autocommit, what happens after an error inside a transaction, and what savepoints are for.""",
        q_bn=r"""PostgreSQL-এ transaction কীভাবে কাজ করে? Autocommit, transaction-এর ভেতরে error হলে কী হয়, আর savepoint কীসের জন্য — ব্যাখ্যা করো।""",
        a_en=r"""
            Every statement runs in its own transaction (autocommit) unless I open one with `BEGIN`. Between `BEGIN` and `COMMIT`, the changes are atomic: all of them become visible together, or none if I `ROLLBACK` or the server crashes.

            If any statement fails inside the block, PostgreSQL puts the whole transaction into an **aborted** state: every following command fails with "current transaction is aborted, commands ignored until end of transaction block". I must `ROLLBACK` (even `COMMIT` just rolls back).

            A `SAVEPOINT` lets me undo only part of the work with `ROLLBACK TO SAVEPOINT` and continue. Also, DDL is transactional in PostgreSQL — `CREATE TABLE` or `ALTER TABLE` can be rolled back, unlike MySQL where DDL commits implicitly.
        """,
        a_bn=r"""
            আমি `BEGIN` দিয়ে transaction না খুললে প্রতিটা statement নিজের আলাদা transaction-এ চলে (autocommit)। `BEGIN` আর `COMMIT`-এর মাঝের পরিবর্তনগুলো atomic: হয় সবগুলো একসাথে দেখা যাবে, নয়তো `ROLLBACK` করলে বা server crash করলে একটাও না।

            Block-এর ভেতরে কোনো statement fail করলে PostgreSQL পুরো transaction-কে **aborted** অবস্থায় নিয়ে যায়: এরপরের প্রতিটা command "current transaction is aborted, commands ignored until end of transaction block" error দেয়। তখন `ROLLBACK` করতেই হবে (এমনকি `COMMIT` দিলেও আসলে rollback হয়)।

            `SAVEPOINT` দিয়ে কাজের শুধু একটা অংশ `ROLLBACK TO SAVEPOINT` করে বাতিল করে আবার এগোনো যায়। আরেকটা ব্যাপার: PostgreSQL-এ DDL-ও transactional — `CREATE TABLE` বা `ALTER TABLE` rollback করা যায়, যেখানে MySQL-এ DDL implicitly commit হয়ে যায়।
        """,
        ex_en=r"""
            - **ACID in PostgreSQL:** Atomicity (all-or-nothing), Consistency (constraints checked), Isolation (MVCC snapshots + isolation levels), Durability (the commit record is flushed to the WAL before `COMMIT` returns, with the default `synchronous_commit = on`).
            - A few commands can't run inside a transaction block: `CREATE INDEX CONCURRENTLY`, `VACUUM`, `CREATE DATABASE`.
            - Keep transactions short. An open transaction holds row locks and stops VACUUM from cleaning dead rows; `idle_in_transaction_session_timeout` protects you from forgotten ones.
            - **Node.js gotcha:** with `pg.Pool`, `pool.query('BEGIN')` and the next `pool.query()` may run on *different* connections. Check out one client with `pool.connect()` and run the whole transaction on it (see the extra code).
        """,
        ex_bn=r"""
            - **PostgreSQL-এ ACID:** Atomicity (সব-নয়তো-কিছুই-না), Consistency (constraint check হয়), Isolation (MVCC snapshot + isolation level), Durability (`COMMIT` return করার আগেই commit record WAL-এ flush হয়, default `synchronous_commit = on` থাকলে)।
            - কিছু command transaction block-এর ভেতরে চলে না: `CREATE INDEX CONCURRENTLY`, `VACUUM`, `CREATE DATABASE`।
            - Transaction ছোট রাখো। খোলা transaction row lock ধরে রাখে আর VACUUM-কে dead row পরিষ্কার করতে দেয় না; ভুলে খোলা রাখা transaction থেকে বাঁচাতে `idle_in_transaction_session_timeout` আছে।
            - **Node.js-এর ফাঁদ:** `pg.Pool`-এ `pool.query('BEGIN')` আর পরের `pool.query()` *আলাদা* connection-এ চলতে পারে। `pool.connect()` দিয়ে একটা client নিয়ে পুরো transaction সেটাতেই চালাও (extra code দেখো)।
        """,
        tip_en=r"""Mention the aborted-transaction state and transactional DDL — both are PostgreSQL-specific and show real hands-on experience. The Node pool gotcha is a great practical bonus.""",
        tip_bn=r"""Aborted-transaction অবস্থা আর transactional DDL-এর কথা বলো — দুটোই PostgreSQL-specific, আর বোঝায় তোমার হাতে-কলমে অভিজ্ঞতা আছে। Node pool-এর ফাঁদটা বললে practical দিক থেকে বাড়তি নম্বর।""",
        mist_en=r"""Running `BEGIN`/`COMMIT` through `pool.query()` in Node.js, or retrying statements inside an aborted transaction instead of rolling back.""",
        mist_bn=r"""Node.js-এ `pool.query()` দিয়ে `BEGIN`/`COMMIT` চালানো, অথবা rollback না করে aborted transaction-এর ভেতরেই statement আবার চালানোর চেষ্টা করা।""",
        code=r"""
            BEGIN;
            INSERT INTO accounts (id, balance) VALUES (1, 500);
            SAVEPOINT before_bonus;
            UPDATE accounts SET balance = balance + 'abc' WHERE id = 1;  -- ERROR: invalid input syntax
            -- any statement here fails: "current transaction is aborted ..."
            ROLLBACK TO SAVEPOINT before_bonus;                         -- recover the transaction
            UPDATE accounts SET balance = balance + 50 WHERE id = 1;
            COMMIT;                                                     -- balance is now 550.00
        """,
        lang="sql",
        extra=[dict(lang="javascript", label_en="Transaction with node-postgres (one client for the whole transaction)",
                    label_bn="node-postgres দিয়ে transaction (পুরো transaction একই client-এ)", src=r"""
            import pg from 'pg';
            const pool = new pg.Pool();

            export async function transfer(fromId, toId, amount) {
              const client = await pool.connect();
              try {
                await client.query('BEGIN');
                await client.query('UPDATE accounts SET balance = balance - $1 WHERE id = $2', [amount, fromId]);
                await client.query('UPDATE accounts SET balance = balance + $1 WHERE id = $2', [amount, toId]);
                await client.query('COMMIT');
              } catch (err) {
                await client.query('ROLLBACK');
                throw err;
              } finally {
                client.release();
              }
            }
        """)],
        follow=[
            ("Which commands cannot run inside a transaction block, and why?", "কোন command-গুলো transaction block-এর ভেতরে চলে না, আর কেন?"),
            ("What does `synchronous_commit = off` trade away?", "`synchronous_commit = off` দিলে কী ছাড় দিতে হয়?"),
        ],
        related=["pg-007", "pg-019"],
        refs=[PG_TX_TUTORIAL, PG_SAVEPOINT],
    ),
    # ------------------------------------------------------------------ pg-007
    Q(
        id="pg-007", sub="MVCC", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["mvcc", "concurrency", "snapshot", "vacuum", "xmin"],
        ver="Version-independent (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""What is MVCC in PostgreSQL, and why don't readers block writers?""",
        q_bn=r"""PostgreSQL-এ MVCC কী, আর reader কেন writer-কে block করে না?""",
        a_en=r"""
            MVCC (Multi-Version Concurrency Control) means PostgreSQL keeps **multiple versions of a row**. An `UPDATE` doesn't overwrite the row in place; it writes a new row version and marks the old one as expired. Each version records which transaction created it (`xmin`) and which deleted or replaced it (`xmax`).

            Every query reads from a **snapshot** — the set of versions committed when the snapshot was taken. So a `SELECT` keeps reading the old version while another transaction writes a new one: readers don't block writers, and writers don't block readers. Two writers on the *same row* still wait for each other via row locks.

            The price is dead row versions, which `VACUUM` (usually autovacuum) cleans up.
        """,
        a_bn=r"""
            MVCC (Multi-Version Concurrency Control) মানে PostgreSQL একটা row-এর **একাধিক version** রাখে। `UPDATE` row-কে জায়গায় বসে overwrite করে না; নতুন একটা row version লেখে আর পুরনোটাকে expired হিসেবে mark করে। প্রতিটা version-এ লেখা থাকে কোন transaction এটা তৈরি করেছে (`xmin`) আর কোনটা delete বা replace করেছে (`xmax`)।

            প্রতিটা query একটা **snapshot** থেকে পড়ে — snapshot নেওয়ার সময় যেসব version commit হয়ে গেছে সেগুলো। তাই অন্য transaction নতুন version লিখতে থাকলেও `SELECT` পুরনো version পড়তে থাকে: reader writer-কে block করে না, writer-ও reader-কে করে না। তবে *একই row*-তে দুজন writer হলে row lock-এর কারণে একজন অপেক্ষা করে।

            এর দাম হলো dead row version, যেগুলো `VACUUM` (সাধারণত autovacuum) পরিষ্কার করে।
        """,
        ex_en=r"""
            - Under **Read Committed** (the default) each statement takes a fresh snapshot; under **Repeatable Read** the whole transaction uses one snapshot — see the example: session A keeps seeing 500.
            - Because an `UPDATE` is effectively "insert new version + expire old", heavy update traffic creates dead tuples → table and index **bloat** if vacuum can't keep up.
            - A long-running or idle-in-transaction session holds back the oldest visible snapshot, so VACUUM can't remove dead rows newer than it. That's a common cause of bloat.
            - Transaction IDs are 32-bit, so VACUUM also "freezes" old rows to prevent transaction-ID wraparound.
        """,
        ex_bn=r"""
            - **Read Committed**-এ (default) প্রতিটা statement নতুন snapshot নেয়; **Repeatable Read**-এ পুরো transaction একটাই snapshot ব্যবহার করে — উদাহরণে দেখো, session A তখনও 500 দেখছে।
            - `UPDATE` আসলে "নতুন version insert + পুরনোটা expire", তাই অনেক update হলে dead tuple জমে → vacuum তাল মেলাতে না পারলে table আর index **bloat** হয়।
            - লম্বা সময় চলা বা idle-in-transaction session সবচেয়ে পুরনো visible snapshot ধরে রাখে, ফলে VACUUM তার পরের dead row সরাতে পারে না। Bloat-এর এটা একটা সাধারণ কারণ।
            - Transaction ID 32-bit, তাই transaction-ID wraparound ঠেকাতে VACUUM পুরনো row-গুলো "freeze"-ও করে।
        """,
        tip_en=r"""Explain it as "updates create new versions + snapshots decide visibility", then immediately mention the cost (dead tuples, VACUUM). That link between MVCC and VACUUM is what interviewers look for.""",
        tip_bn=r"""এভাবে বলো: "update নতুন version তৈরি করে + snapshot ঠিক করে কে কোনটা দেখবে", তারপর সাথে সাথেই খরচটা বলো (dead tuple, VACUUM)। MVCC আর VACUUM-এর এই যোগসূত্রটাই interviewer শুনতে চায়।""",
        mist_en=r"""Saying PostgreSQL never locks rows. MVCC removes read/write blocking, but concurrent writes to the same row still take row-level locks.""",
        mist_bn=r"""বলা যে PostgreSQL কখনো row lock করে না। MVCC read/write-এর block দূর করে, কিন্তু একই row-তে একসাথে write হলে row-level lock নেওয়া হয়ই।""",
        code=r"""
            -- Session A
            BEGIN ISOLATION LEVEL REPEATABLE READ;
            SELECT balance FROM accounts WHERE id = 1;      -- 500

            -- Session B (runs immediately, not blocked by A)
            UPDATE accounts SET balance = 700 WHERE id = 1; -- autocommits

            -- Session A: same snapshot, still sees the old version
            SELECT balance FROM accounts WHERE id = 1;      -- 500 (would be 700 under READ COMMITTED)
            COMMIT;

            -- xmin = id of the transaction that created this row version
            SELECT xmin, xmax, balance FROM accounts WHERE id = 1;
        """,
        lang="sql",
        follow=[
            ("What exactly does VACUUM do, and how is it different from VACUUM FULL?", "VACUUM ঠিক কী করে, আর VACUUM FULL থেকে এটা কীভাবে আলাদা?"),
            ("What is a HOT update?", "HOT update কী?"),
        ],
        related=["pg-008", "pg-029", "pg-023"],
        refs=[PG_MVCC_INTRO, PG_ISO, PG_VACUUM],
    ),
    # ------------------------------------------------------------------ pg-008
    Q(
        id="pg-008", sub="Isolation Levels", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["isolation", "read-committed", "transactions"],
        ver="Version-independent (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""What is the default transaction isolation level in PostgreSQL?""",
        q_bn=r"""PostgreSQL-এ default transaction isolation level কোনটা?""",
        options=[
            ("Read Uncommitted", "Read Uncommitted"),
            ("Read Committed", "Read Committed"),
            ("Repeatable Read", "Repeatable Read"),
            ("Serializable", "Serializable"),
        ],
        correct=1,
        a_en=r"""**Read Committed.** Each statement sees a snapshot of data committed before that statement started, so two `SELECT`s in the same transaction can see different results if another transaction commits in between. You can check it with `SHOW default_transaction_isolation;`.""",
        a_bn=r"""**Read Committed।** প্রতিটা statement সেই statement শুরু হওয়ার আগে commit হওয়া data-র snapshot দেখে, তাই একই transaction-এর দুটো `SELECT`-এর মাঝে অন্য কেউ commit করলে দুই রকম ফল আসতে পারে। `SHOW default_transaction_isolation;` দিয়ে check করতে পারো।""",
        ex_en=r"""
            The most tempting wrong answer is **Repeatable Read**, because that's the default in MySQL's InnoDB. Some people also pick Serializable because the SQL standard names it as the default.

            Interesting detail: PostgreSQL accepts `READ UNCOMMITTED` syntax but runs it as Read Committed — PostgreSQL never allows dirty reads. Raise the level per transaction when needed: `BEGIN ISOLATION LEVEL REPEATABLE READ;` (one snapshot for the whole transaction) or `SERIALIZABLE` (full serializability; be ready to retry on serialization failures).
        """,
        ex_bn=r"""
            সবচেয়ে লোভনীয় ভুল উত্তর **Repeatable Read**, কারণ MySQL-এর InnoDB-তে সেটাই default। কেউ কেউ Serializable বেছে নেয়, কারণ SQL standard সেটাকে default বলে।

            মজার তথ্য: PostgreSQL `READ UNCOMMITTED` syntax মেনে নেয়, কিন্তু চালায় Read Committed হিসেবে — PostgreSQL কখনোই dirty read হতে দেয় না। দরকার হলে প্রতি transaction-এ level বাড়াও: `BEGIN ISOLATION LEVEL REPEATABLE READ;` (পুরো transaction-এ একটাই snapshot) অথবা `SERIALIZABLE` (পূর্ণ serializability; serialization failure হলে retry করার জন্য তৈরি থাকো)।
        """,
        tip_en=r"""Answer, then add the two differentiators: MySQL's default is Repeatable Read, and PostgreSQL has no dirty reads even at "Read Uncommitted".""",
        tip_bn=r"""উত্তর দিয়ে তারপর দুটো পার্থক্যের কথা যোগ করো: MySQL-এর default Repeatable Read, আর "Read Uncommitted" দিলেও PostgreSQL-এ dirty read হয় না।""",
        extra=[dict(lang="sql", label_en="Checking and raising the isolation level", label_bn="Isolation level দেখা আর বাড়ানো", src=r"""
            SHOW default_transaction_isolation;   -- read committed

            BEGIN ISOLATION LEVEL REPEATABLE READ;
            -- ...
            COMMIT;
        """)],
        related=["pg-007", "pg-023"],
        refs=[PG_ISO],
    ),
]

if __name__ == "__main__":
    save("postgresql", "b1", QUESTIONS)
