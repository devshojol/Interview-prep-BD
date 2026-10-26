# Drizzle ORM — batch 4 (drizzle-025 … drizzle-032): transaction bugs, zero-downtime migrations, v1 RC,
# performance & security review, brownfield adoption, flash-sale design, data-layer architecture, migration incident
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

D_TRANSACTIONS = ("Drizzle ORM — Transactions", "https://orm.drizzle.team/docs/transactions")
D_SELECT = ("Drizzle ORM — Select (incl. locking clauses)", "https://orm.drizzle.team/docs/select")
D_KIT_CUSTOM = ("Drizzle Kit — Custom migrations", "https://orm.drizzle.team/docs/kit-custom-migrations")
D_KIT_GENERATE = ("Drizzle Kit — generate", "https://orm.drizzle.team/docs/drizzle-kit-generate")
D_UPGRADE_V1 = ("Drizzle ORM — Upgrade to v1", "https://orm.drizzle.team/docs/upgrade-v1")
D_RELATIONS_V1V2 = ("Drizzle ORM — Relational Queries v1 → v2", "https://orm.drizzle.team/docs/relations-v1-v2")
D_RQB = ("Drizzle ORM — Relational queries", "https://orm.drizzle.team/docs/rqb")
D_JOINS = ("Drizzle ORM — Joins", "https://orm.drizzle.team/docs/joins")
D_OPERATORS = ("Drizzle ORM — Filter operators", "https://orm.drizzle.team/docs/operators")
D_KIT_PULL = ("Drizzle Kit — pull", "https://orm.drizzle.team/docs/drizzle-kit-pull")
D_CONFIG = ("Drizzle Kit — drizzle.config.ts", "https://orm.drizzle.team/docs/drizzle-config-file")
D_READ_REPLICAS = ("Drizzle ORM — Read replicas", "https://orm.drizzle.team/docs/read-replicas")
D_MIGRATIONS = ("Drizzle ORM — Migrations", "https://orm.drizzle.team/docs/migrations")
D_OVERVIEW = ("Drizzle ORM — Overview", "https://orm.drizzle.team/docs/overview")
D_SQL = ("Drizzle ORM — sql template", "https://orm.drizzle.team/docs/sql")
PG_LOCKING = ("PostgreSQL docs — Explicit locking", "https://www.postgresql.org/docs/current/explicit-locking.html")
PG_CREATEINDEX = ("PostgreSQL docs — CREATE INDEX (CONCURRENTLY)", "https://www.postgresql.org/docs/current/sql-createindex.html")
PG_EXPLAIN = ("PostgreSQL docs — EXPLAIN", "https://www.postgresql.org/docs/current/sql-explain.html")
OWASP_MASS = ("OWASP — Mass Assignment Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ drizzle-025
    Q(
        id="drizzle-025", sub="Transactions & Concurrency", diff="hard", type="debugging",
        prio="high", market="both", mins=10,
        tags=["transactions", "race-condition", "lost-update", "row-locking", "debugging"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""This checkout function oversells stock during sales, sometimes leaves stock reduced for orders whose payment failed, and once hung forever in an integration test that used a single-connection database. Find all the bugs and fix them.""",
        q_bn=r"""এই checkout function sale-এর সময় stock-এর চেয়ে বেশি বিক্রি করে ফেলে, কখনো payment fail হওয়া order-এর stock কমিয়ে রেখে দেয়, আর একবার single-connection database ব্যবহার করা একটা integration test-এ চিরকালের জন্য আটকে গিয়েছিল। সব bug খুঁজে বের করে ঠিক করো।""",
        code=r"""
            export async function placeOrder(userId: number, productId: number, qty: number) {
              return db.transaction(async (tx) => {
                const [product] = await tx.select().from(products).where(eq(products.id, productId));
                if (!product || product.stock < qty) throw new OutOfStockError();

                await db
                  .update(products)
                  .set({ stock: product.stock - qty })
                  .where(eq(products.id, productId));

                const [order] = await tx.insert(orders).values({ userId, productId, qty }).returning();
                await payments.charge(userId, order.id); // calls the payment gateway's HTTP API
                return order;
              });
            }
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                export async function placeOrder(userId: number, productId: number, qty: number) {
                  // Short transaction: reserve stock + create order + outbox event, nothing slow inside
                  return db.transaction(async (tx) => {
                    const reserved = await tx
                      .update(products)
                      .set({ stock: sql`${products.stock} - ${qty}` })            // computed in SQL
                      .where(and(eq(products.id, productId), gte(products.stock, qty))) // check + write atomically
                      .returning({ id: products.id });
                    if (reserved.length === 0) throw new OutOfStockError();

                    const [order] = await tx
                      .insert(orders)
                      .values({ userId, productId, qty, status: 'pending_payment' })
                      .returning();

                    await tx.insert(outbox).values({ type: 'order.created', payload: { orderId: order.id } });
                    return order;
                  });
                  // Payment runs after commit (worker/next request). On failure, a compensating
                  // transaction cancels the order and returns the stock.
                }

                // Alternative when you need the row first: lock it for the rest of the transaction
                // const [product] = await tx.select().from(products)
                //   .where(eq(products.id, productId)).for('update');
            """),
        ],
        a_en=r"""
            There are three separate bugs:

            1. **`db` instead of `tx`.** The update runs on a *different* pooled connection, outside the transaction. It autocommits immediately, so if anything later throws (payment fails), the order insert rolls back but the stock reduction stays. With a single-connection client (or an exhausted pool) it can't get a connection at all while the transaction holds the only one → the test hung forever (verified with a one-connection PGlite setup).
            2. **Lost update (read–modify–write in JavaScript).** Two concurrent checkouts both read `stock = 1`, both pass the check, both write `stock = 0` → two orders for one item. Under READ COMMITTED a plain `SELECT` doesn't lock anything. Fix: make the check and the write **one atomic statement** — `SET stock = stock - qty WHERE id = ? AND stock >= qty RETURNING` — or lock the row first with `.for('update')`.
            3. **External call inside the transaction.** The payment HTTP call keeps the transaction (row locks + connection) open for seconds, and the two systems can disagree: the charge can succeed and then the commit fail. Fix: keep the transaction short, write an outbox event, and charge after commit with a compensating action on failure.

            A `CHECK (stock >= 0)` constraint is the final safety net.
        """,
        a_bn=r"""
            এখানে তিনটা আলাদা bug আছে:

            1. **`tx`-এর বদলে `db`।** Update-টা transaction-এর বাইরে, একটা *আলাদা* pooled connection-এ চলে। সাথে সাথে autocommit হয়, তাই পরে কিছু throw করলে (payment fail) order insert rollback হয় কিন্তু stock কমানো থেকে যায়। Single-connection client-এ (বা pool শেষ হয়ে গেলে) transaction একমাত্র connection ধরে রাখে বলে এটা connection-ই পায় না → test চিরকাল আটকে ছিল (এক-connection PGlite setup-এ যাচাই করা)।
            2. **Lost update (JavaScript-এ read–modify–write)।** দুটো একসাথে চলা checkout দুজনেই `stock = 1` পড়ে, দুজনেই check পার হয়, দুজনেই `stock = 0` লেখে → একটা item-এর জন্য দুটো order। READ COMMITTED-এ সাধারণ `SELECT` কিছুই lock করে না। সমাধান: check আর write-কে **একটা atomic statement** বানাও — `SET stock = stock - qty WHERE id = ? AND stock >= qty RETURNING` — অথবা আগে `.for('update')` দিয়ে row lock করো।
            3. **Transaction-এর ভেতরে external call।** Payment-এর HTTP call কয়েক সেকেন্ড transaction (row lock + connection) খোলা রাখে, আর দুই system-এর মধ্যে অমিল হতে পারে: charge সফল হয়ে তারপর commit fail করতে পারে। সমাধান: transaction ছোট রাখো, একটা outbox event লেখো, আর commit-এর পরে charge করো, fail করলে compensating action।

            `CHECK (stock >= 0)` constraint হলো শেষ safety net।
        """,
        quick_en=r"""Three bugs: the update uses `db` instead of `tx`, so it commits outside the transaction (and hangs a one-connection pool); the read-check-write in JavaScript loses updates, so use one `UPDATE ... WHERE stock >= qty RETURNING`; and the payment call inside the transaction should move after commit via an outbox.""",
        quick_bn=r"""তিনটা bug: update-এ `tx`-এর বদলে `db`, তাই সেটা transaction-এর বাইরে commit হয় (আর one-connection pool-এ আটকে যায়); JavaScript-এ read-check-write করায় update হারায়, তাই একটাই `UPDATE ... WHERE stock >= qty RETURNING` লাগে; আর transaction-এর ভেতরের payment call outbox দিয়ে commit-এর পরে সরাতে হবে।""",
        ex_en=r"""
            - **Why the atomic UPDATE works:** PostgreSQL row-locks the product while updating. A concurrent UPDATE waits, then re-evaluates its `WHERE` against the *new* row version — so the second buyer sees `stock >= qty` is false and gets zero rows back. Verified: three concurrent reservations of 1 unit with stock 2 returned `[1, 0, null]`.
            - **`for('update')`** is the alternative when business logic needs to read several columns first; it serialises buyers on that row for the transaction's duration, so keep the transaction short.
            - **Isolation levels:** SERIALIZABLE would also prevent the anomaly but forces you to retry on `40001` errors — fine for low-contention flows, costly for hot rows.
            - **Spotting `db` vs `tx` in review:** a lint rule or a repository API that *requires* a `tx` parameter for write methods makes this mistake hard to write.
            - **Testing:** concurrency bugs need concurrent tests — fire N parallel checkouts against real PostgreSQL and assert stock never goes negative and orders ≤ initial stock.
        """,
        ex_bn=r"""
            - **Atomic UPDATE কেন কাজ করে:** update করার সময় PostgreSQL product row lock করে। একসাথে আসা আরেকটা UPDATE অপেক্ষা করে, তারপর *নতুন* row version-এর বিরুদ্ধে তার `WHERE` আবার যাচাই করে — তাই দ্বিতীয় ক্রেতা দেখে `stock >= qty` মিথ্যা আর শূন্য row ফেরত পায়। যাচাই করা: stock 2 থাকা অবস্থায় ১ unit করে তিনটা একসাথে reservation দিলে ফল এসেছে `[1, 0, null]`।
            - Business logic-এর জন্য আগে কয়েকটা column পড়তে হলে **`for('update')`** বিকল্প; এটা transaction চলাকালীন ওই row-এ ক্রেতাদের এক এক করে চালায়, তাই transaction ছোট রাখো।
            - **Isolation level:** SERIALIZABLE-ও এই anomaly আটকাত, কিন্তু `40001` error-এ retry করতে বাধ্য করে — কম contention-এর flow-এ ঠিক আছে, hot row-এ ব্যয়বহুল।
            - **Review-তে `db` বনাম `tx` ধরা:** একটা lint rule বা এমন repository API যেটা write method-এ `tx` parameter *বাধ্যতামূলক* করে, এই ভুল লেখাকেই কঠিন করে দেয়।
            - **Testing:** concurrency bug-এর জন্য concurrent test লাগে — আসল PostgreSQL-এর বিরুদ্ধে N টা parallel checkout চালাও আর assert করো stock কখনো negative হয় না আর order ≤ শুরুর stock।
        """,
        tip_en=r"""Number the bugs and give each a root cause and a fix. Explaining *why* the conditional UPDATE is safe (row lock + re-check of `WHERE`) is what makes this a hard-level answer.""",
        tip_bn=r"""Bug গুলো নম্বর দিয়ে বলো, প্রতিটার root cause আর fix সহ। Conditional UPDATE *কেন* নিরাপদ (row lock + `WHERE` আবার যাচাই) সেটা ব্যাখ্যা করাই উত্তরটাকে hard-level বানায়।""",
        mist_en=r"""Fixing only `db` → `tx` and keeping the read-modify-write race; "fixing" the race with an application-level mutex (doesn't work across instances); calling external services inside long transactions.""",
        mist_bn=r"""শুধু `db` → `tx` ঠিক করে read-modify-write race রেখে দেওয়া; application-level mutex দিয়ে race "ঠিক" করা (একাধিক instance-এ কাজ করে না); দীর্ঘ transaction-এর ভেতরে external service call করা।""",
        follow=[
            ("When would you choose `SELECT ... FOR UPDATE SKIP LOCKED`?", "কখন `SELECT ... FOR UPDATE SKIP LOCKED` বেছে নেবে?"),
            ("How would you design the compensation when payment fails after the order commits?", "Order commit হওয়ার পরে payment fail করলে compensation কীভাবে design করবে?"),
        ],
        related=["drizzle-016", "drizzle-030"],
        refs=[D_TRANSACTIONS, D_SELECT, PG_LOCKING],
    ),
    # ------------------------------------------------------------------ drizzle-026
    Q(
        id="drizzle-026", sub="Zero-downtime Migrations", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["migrations", "expand-contract", "drizzle-kit", "rolling-deploy", "not-null"],
        ver="drizzle-kit 0.31 / PostgreSQL 18", vs=True, status="stable",
        q_en=r"""On a live `users` table with 5 million rows and rolling deploys (old and new app versions run side by side for a few minutes), you must (1) rename `name` to `full_name` and (2) make `phone` NOT NULL. When you run `drizzle-kit generate`, it asks whether `full_name` is a renamed column or a new one. How do you ship this safely?""",
        q_bn=r"""৫০ লাখ row-এর একটা live `users` table-এ, rolling deploy সহ (কয়েক মিনিট পুরোনো আর নতুন app version পাশাপাশি চলে), তোমাকে (1) `name`-কে `full_name` নাম দিতে হবে আর (2) `phone`-কে NOT NULL করতে হবে। `drizzle-kit generate` চালালে এটা জিজ্ঞেস করে `full_name` rename করা column নাকি নতুন। কীভাবে নিরাপদে ship করবে?""",
        a_en=r"""
            **Don't do it in one migration.** A direct `RENAME COLUMN` breaks the old pods that still query `name` during the rollout; choosing "create new column" in the prompt generates `ADD full_name` + `DROP name` — instant data loss. I use **expand → migrate → contract** over several releases:

            **Rename (`name` → `full_name`):**
            1. *Expand:* add nullable `full_name`; deploy code that writes **both** columns and reads `full_name ?? name`.
            2. *Backfill* in batches from a script (e.g. 10k rows per transaction), not as one giant `UPDATE` inside the migration.
            3. *Switch:* deploy code that only reads/writes `full_name`.
            4. *Contract:* a later release drops `name`.

            **NOT NULL on a big table:** `SET NOT NULL` alone scans the whole table under an exclusive lock. Instead, with custom migrations (`drizzle-kit generate --custom`):
            1. backfill missing phones;
            2. `ADD CONSTRAINT ... CHECK (phone IS NOT NULL) NOT VALID` (brief lock, no scan);
            3. in a **separate** run, `VALIDATE CONSTRAINT` (scans without blocking reads/writes);
            4. `SET NOT NULL` — PostgreSQL uses the validated CHECK to skip the scan — then drop the CHECK.

            **Drizzle-specific caveat:** the migrator applies all pending migrations in **one transaction**, so locks taken early are held until the end. Ship lock-sensitive steps as separate releases (separate `migrate` runs), set `SET LOCAL lock_timeout = '5s'` so a migration fails fast instead of queueing behind long transactions, and always review the generated SQL in the PR.
        """,
        a_bn=r"""
            **এক migration-এ কোরো না।** সরাসরি `RENAME COLUMN` rollout-এর সময় পুরোনো pod-গুলোকে ভেঙে দেয়, যেগুলো তখনো `name` query করে; আর prompt-এ "নতুন column" বেছে নিলে generate হয় `ADD full_name` + `DROP name` — সাথে সাথে data loss। আমি কয়েকটা release জুড়ে **expand → migrate → contract** করি:

            **Rename (`name` → `full_name`):**
            1. *Expand:* nullable `full_name` যোগ করো; এমন code deploy করো যেটা **দুটো** column-এই লেখে আর পড়ে `full_name ?? name`।
            2. *Backfill* করো script থেকে batch-এ (যেমন প্রতি transaction-এ ১০ হাজার row), migration-এর ভেতরে একটা বিশাল `UPDATE` দিয়ে না।
            3. *Switch:* এমন code deploy করো যেটা শুধু `full_name` পড়ে/লেখে।
            4. *Contract:* পরের কোনো release-এ `name` drop করো।

            **বড় table-এ NOT NULL:** শুধু `SET NOT NULL` exclusive lock নিয়ে পুরো table scan করে। তার বদলে custom migration দিয়ে (`drizzle-kit generate --custom`):
            1. যাদের phone নেই তাদের backfill;
            2. `ADD CONSTRAINT ... CHECK (phone IS NOT NULL) NOT VALID` (অল্প সময়ের lock, scan নেই);
            3. **আলাদা** run-এ `VALIDATE CONSTRAINT` (read/write block না করে scan করে);
            4. `SET NOT NULL` — validated CHECK দেখে PostgreSQL scan বাদ দেয় — তারপর CHECK drop করো।

            **Drizzle-specific সতর্কতা:** migrator সব pending migration **একটা transaction-এ** apply করে, তাই শুরুতে নেওয়া lock শেষ পর্যন্ত থাকে। Lock-sensitive ধাপগুলো আলাদা release-এ (আলাদা `migrate` run) পাঠাও, `SET LOCAL lock_timeout = '5s'` দাও যাতে লম্বা transaction-এর পেছনে queue না করে migration দ্রুত fail করে, আর PR-এ generated SQL সবসময় review করো।
        """,
        quick_en=r"""Don't do it in one migration; use expand → migrate → contract: add `full_name`, write both columns, backfill in batches, switch reads, and drop `name` in a later release. For NOT NULL, add a `CHECK (phone IS NOT NULL) NOT VALID`, validate it in a separate run, then `SET NOT NULL` without a long locking scan.""",
        quick_bn=r"""এক migration-এ করি না; expand → migrate → contract: `full_name` যোগ করি, দুই column-এই লিখি, batch-এ backfill করি, read switch করি, আর পরের release-এ `name` drop করি। NOT NULL-এর জন্য আগে `CHECK (phone IS NOT NULL) NOT VALID`, আলাদা run-এ validate, তারপর `SET NOT NULL` — লম্বা lock-ধরা scan ছাড়াই।""",
        ex_en=r"""
            - **The lock queue problem:** `ALTER TABLE` needs a strong lock. If a long-running query holds a weaker lock, the `ALTER` waits — and every new query queues behind the `ALTER`. A 2-second migration can cause a multi-minute outage; `lock_timeout` plus retries prevents this.
            - **When "rename" in the prompt is fine:** single-instance apps or a maintenance window. `RENAME COLUMN` itself is metadata-only and instant.
            - **Drizzle schema during expand:** both columns exist in `schema.ts`; remove `name` from the schema only in the contract step, then generate the drop.
            - **Backfill hygiene:** batch by primary-key ranges, sleep between batches, monitor replication lag and autovacuum.
            - **Rollback plan:** every step is backwards-compatible with the previous app version, so you can roll back the app without touching the database.
        """,
        ex_bn=r"""
            - **Lock queue সমস্যা:** `ALTER TABLE`-এর শক্ত lock লাগে। একটা দীর্ঘ query দুর্বল lock ধরে থাকলে `ALTER` অপেক্ষা করে — আর প্রতিটা নতুন query `ALTER`-এর পেছনে লাইনে দাঁড়ায়। ২ সেকেন্ডের migration কয়েক মিনিটের outage ঘটাতে পারে; `lock_timeout` আর retry এটা আটকায়।
            - **Prompt-এ "rename" কখন ঠিক:** single-instance app বা maintenance window। `RENAME COLUMN` নিজে শুধু metadata বদলায়, তাৎক্ষণিক।
            - **Expand-এর সময় Drizzle schema:** `schema.ts`-এ দুটো column-ই থাকে; শুধু contract ধাপে schema থেকে `name` সরাও, তারপর drop generate করো।
            - **Backfill-এর নিয়ম:** primary-key range ধরে batch করো, batch-এর মাঝে বিরতি দাও, replication lag আর autovacuum দেখো।
            - **Rollback plan:** প্রতিটা ধাপ আগের app version-এর সাথে backwards-compatible, তাই database না ছুঁয়েই app rollback করা যায়।
        """,
        tip_en=r"""Say "expand–contract" early, then show you know two PostgreSQL tricks (NOT VALID + VALIDATE, `lock_timeout`) and one Drizzle-specific fact (single-transaction migrator, the rename prompt). That combination stands out.""",
        tip_bn=r"""শুরুতেই "expand–contract" বলো, তারপর দেখাও তুমি দুটো PostgreSQL কৌশল জানো (NOT VALID + VALIDATE, `lock_timeout`) আর একটা Drizzle-specific তথ্য (single-transaction migrator, rename prompt)। এই মিশ্রণই তোমাকে আলাদা করে।""",
        mist_en=r"""Answering "create" in the rename prompt (drop + add = data loss); renaming in one step during a rolling deploy; backfilling millions of rows in one transaction; putting ADD NOT VALID and VALIDATE in the same migrator run.""",
        mist_bn=r"""Rename prompt-এ "create" বেছে নেওয়া (drop + add = data loss); rolling deploy-এর সময় এক ধাপে rename করা; এক transaction-এ লাখ লাখ row backfill করা; ADD NOT VALID আর VALIDATE একই migrator run-এ রাখা।""",
        code=r"""
            -- Release 1 (expand) — generated: drizzle-kit generate
            ALTER TABLE "users" ADD COLUMN "full_name" text;

            -- (backfill full_name from name in batches via a script, between releases)

            -- Release 2 — custom: drizzle-kit generate --custom --name phone_check
            SET LOCAL lock_timeout = '5s';
            ALTER TABLE "users" ADD CONSTRAINT "users_phone_not_null" CHECK ("phone" IS NOT NULL) NOT VALID;

            -- Release 3 — custom: validate without blocking writes, then flip to NOT NULL
            SET LOCAL lock_timeout = '5s';
            ALTER TABLE "users" VALIDATE CONSTRAINT "users_phone_not_null";
            ALTER TABLE "users" ALTER COLUMN "phone" SET NOT NULL; -- uses the valid CHECK, no full scan
            ALTER TABLE "users" DROP CONSTRAINT "users_phone_not_null";

            -- Release 4 (contract) — after all running code uses full_name
            ALTER TABLE "users" DROP COLUMN "name";
        """,
        lang="sql",
        follow=[
            ("Why can a 2-second `ALTER TABLE` cause a 5-minute outage?", "২ সেকেন্ডের একটা `ALTER TABLE` কেন ৫ মিনিটের outage ঘটাতে পারে?"),
            ("How do you test that a migration is backwards-compatible?", "একটা migration backwards-compatible কি না কীভাবে test করবে?"),
        ],
        related=["drizzle-017", "drizzle-032"],
        refs=[D_KIT_CUSTOM, D_KIT_GENERATE, PG_LOCKING],
    ),
    # ------------------------------------------------------------------ drizzle-027
    Q(
        id="drizzle-027", sub="Drizzle v1 RC Changes", diff="hard", type="conceptual",
        prio="medium", market="both", mins=7,
        tags=["drizzle-v1", "definerelations", "rqb-v2", "upgrade", "preview"],
        ver="Drizzle ORM 1.0.0-rc (preview); stable line is 0.45.x", vs=True, status="preview",
        q_en=r"""Drizzle ORM v1.0 is in release-candidate stage. What are the main changes compared with the stable 0.45 line, and how would you plan an upgrade for a production app?""",
        q_bn=r"""Drizzle ORM v1.0 এখন release-candidate পর্যায়ে। Stable 0.45 line-এর তুলনায় মূল পরিবর্তনগুলো কী, আর একটা production app-এর upgrade কীভাবে plan করবে?""",
        a_en=r"""
            v1.0 is a **release candidate (preview)** — 0.45.x is what I'd run in production today. The headline changes:

            - **Relations v2:** one `defineRelations(schema, (r) => ({ ... }))` call replaces per-table `relations()`. Links use `r.one.users({ from: r.posts.authorId, to: r.users.id })` and `r.many.posts()`; many-to-many can go `through` a junction table, and a relation can carry its own `where`.
            - **Relational Queries v2:** `drizzle(url, { relations })` instead of `{ schema }`, and **object-style** filters and ordering — `where: { role: 'user' }`, `orderBy: { id: 'asc' }`, with `AND`/`OR`/`NOT` and a `RAW` escape hatch — instead of v1 callbacks like `(u, { eq }) => eq(u.role, 'user')`.
            - **Validators move in:** schema generators such as `createInsertSchema` are imported from `drizzle-orm/zod` (and siblings for other libraries) instead of separate `drizzle-zod`-style packages.
            - **Drizzle Kit:** a new migrations layout — one folder per migration (SQL + snapshot), no `_journal.json`, which reduces merge conflicts; `drizzle-kit up` converts the old layout; `check` gains commutativity checks for migrations from different branches; `drop` is removed.

            **Upgrade plan:** wait for GA (or pilot on a non-critical service), upgrade `drizzle-orm` and `drizzle-kit` together, run `drizzle-kit up` on a branch, migrate relation definitions and RQB queries module by module (follow the official v1→v2 guide), and run the full integration test suite against real PostgreSQL. The SQL-like builder (`select/insert/update`) changes far less than the relational API.
        """,
        a_bn=r"""
            v1.0 একটা **release candidate (preview)** — আজ production-এ আমি 0.45.x-ই চালাব। প্রধান পরিবর্তন:

            - **Relations v2:** table-প্রতি `relations()`-এর জায়গায় একটাই `defineRelations(schema, (r) => ({ ... }))` call। Link হয় `r.one.users({ from: r.posts.authorId, to: r.users.id })` আর `r.many.posts()` দিয়ে; many-to-many একটা junction table-এর `through` দিয়ে যেতে পারে, আর একটা relation নিজের `where` রাখতে পারে।
            - **Relational Queries v2:** `{ schema }`-এর বদলে `drizzle(url, { relations })`, আর **object-style** filter ও ordering — `where: { role: 'user' }`, `orderBy: { id: 'asc' }`, সাথে `AND`/`OR`/`NOT` আর `RAW` escape hatch — v1-এর `(u, { eq }) => eq(u.role, 'user')`-এর মতো callback-এর বদলে।
            - **Validator ভেতরে চলে আসছে:** `createInsertSchema`-এর মতো schema generator আলাদা `drizzle-zod`-ধরনের package-এর বদলে import হয় `drizzle-orm/zod` (আর অন্য library-র জন্য একই রকম path) থেকে।
            - **Drizzle Kit:** নতুন migration layout — প্রতিটা migration-এর আলাদা folder (SQL + snapshot), `_journal.json` নেই, ফলে merge conflict কমে; `drizzle-kit up` পুরোনো layout convert করে; `check`-এ আলাদা branch-এর migration-এর জন্য commutativity check যোগ হয়েছে; `drop` সরানো হয়েছে।

            **Upgrade plan:** GA-র জন্য অপেক্ষা করো (বা একটা কম গুরুত্বপূর্ণ service-এ pilot), `drizzle-orm` আর `drizzle-kit` একসাথে upgrade করো, একটা branch-এ `drizzle-kit up` চালাও, relation definition আর RQB query module ধরে ধরে migrate করো (official v1→v2 guide মেনে), আর আসল PostgreSQL-এর বিরুদ্ধে পুরো integration test suite চালাও। SQL-এর মতো builder (`select/insert/update`) relational API-র চেয়ে অনেক কম বদলায়।
        """,
        quick_en=r"""v1.0 is still a release candidate, so 0.45.x stays in production. It brings `defineRelations()`, Relational Queries v2 with object-style `where`/`orderBy`, validators under `drizzle-orm/zod` and a new migration folder layout; upgrade after GA or on a pilot service, with `drizzle-kit up` and full integration tests.""",
        quick_bn=r"""v1.0 এখনো release candidate, তাই production-এ 0.45.x-ই থাকে। এতে আসছে `defineRelations()`, object-style `where`/`orderBy`-সহ Relational Queries v2, `drizzle-orm/zod`-এ validator আর নতুন migration folder layout; upgrade করি GA-র পরে বা একটা pilot service-এ, `drizzle-kit up` আর পুরো integration test চালিয়ে।""",
        ex_en=r"""
            - **Why RQB v2:** object filters are easier to serialise and compose (e.g. building filters from API query params), relation-level `where` lets you define "published posts" once, and `through` removes the boilerplate of exposing junction tables in results.
            - **Mixed codebases:** during migration, keep relation definitions in one module so the switch is contained; isolate RQB usage behind repositories so callers don't change.
            - **Version pinning:** RC releases can change between candidates — pin exact versions, read release notes, and don't mix `drizzle-orm@rc` with a 0.x `drizzle-kit`.
            - **Interview angle:** being precise that v1 is RC (not "the latest stable") and knowing *what* changes shows you follow the ecosystem without chasing pre-releases in production.
        """,
        ex_bn=r"""
            - **RQB v2 কেন:** object filter serialise আর compose করা সহজ (যেমন API query param থেকে filter বানানো), relation-level `where` দিয়ে "published posts" একবারেই define করা যায়, আর `through` result-এ junction table দেখানোর boilerplate সরিয়ে দেয়।
            - **মিশ্র codebase:** migration-এর সময় relation definition এক module-এ রাখো যাতে পরিবর্তন সীমিত থাকে; RQB-র ব্যবহার repository-র পেছনে রাখো যাতে caller বদলাতে না হয়।
            - **Version pinning:** RC release candidate থেকে candidate-এ বদলাতে পারে — exact version pin করো, release note পড়ো, আর `drizzle-orm@rc`-এর সাথে 0.x `drizzle-kit` মিশিও না।
            - **Interview-এর দিক:** v1 যে RC ("সর্বশেষ stable" না) এটা নির্ভুলভাবে বলা আর *কী* বদলাচ্ছে জানা — এতে বোঝা যায় তুমি ecosystem খেয়াল রাখো, কিন্তু production-এ pre-release-এর পেছনে ছোটো না।
        """,
        tip_en=r"""Lead with the status ("RC, not stable") and then group changes into relations, queries, validators and tooling. Ending with a cautious upgrade plan shows production judgement.""",
        tip_bn=r"""Status দিয়ে শুরু করো ("RC, stable না"), তারপর পরিবর্তনগুলো relations, queries, validators আর tooling-এ ভাগ করে বলো। সাবধানী upgrade plan দিয়ে শেষ করলে production-এর বিচারবুদ্ধি বোঝা যায়।""",
        mist_en=r"""Calling v1 "the current stable version"; copying v2 object-style `where` into 0.45 code; upgrading `drizzle-orm` without `drizzle-kit`; assuming the migration folder format is unchanged.""",
        mist_bn=r"""v1-কে "বর্তমান stable version" বলা; 0.45-এর code-এ v2-এর object-style `where` কপি করা; `drizzle-kit` ছাড়া `drizzle-orm` upgrade করা; ধরে নেওয়া যে migration folder-এর format বদলায়নি।""",
        code=r"""
            // Drizzle v1 RC (preview) — relations.ts
            import { defineRelations } from 'drizzle-orm';
            import { posts, users } from './schema';

            export const relations = defineRelations({ users, posts }, (r) => ({
              users: { posts: r.many.posts() },
              posts: { author: r.one.users({ from: r.posts.authorId, to: r.users.id }) },
            }));

            // db.ts
            export const db = drizzle(process.env.DATABASE_URL!, { relations });

            // RQB v2: object-style filters and ordering
            const authors = await db.query.users.findMany({
              where: { role: 'user' },
              orderBy: { id: 'asc' },
              columns: { id: true, name: true },
              with: { posts: { where: { published: true }, columns: { title: true } } },
            });

            // Same query in stable 0.45 (RQB v1) for comparison:
            // db.query.users.findMany({
            //   where: (u, { eq }) => eq(u.role, 'user'),
            //   orderBy: (u, { asc }) => [asc(u.id)],
            //   with: { posts: { where: (p, { eq }) => eq(p.published, true) } },
            // });
        """,
        lang="typescript",
        follow=[
            ("What does `drizzle-kit up` do, and when do you run it?", "`drizzle-kit up` কী করে, আর কখন চালাও?"),
            ("Why might object-style filters be easier to build from API query parameters?", "API query parameter থেকে object-style filter বানানো কেন সহজ হতে পারে?"),
        ],
        related=["drizzle-014", "drizzle-010"],
        refs=[D_UPGRADE_V1, D_RELATIONS_V1V2, D_RQB],
    ),
    # ------------------------------------------------------------------ drizzle-028
    Q(
        id="drizzle-028", sub="Performance & Security Review", diff="hard", type="debugging",
        prio="high", market="both", mins=12,
        tags=["n-plus-one", "pagination", "sql-injection", "mass-assignment", "indexes"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18 / Express 5", vs=False, status="stable",
        q_en=r"""This order-history API has p95 latency of 2 seconds for large customers, and a security review flagged it as well. Identify the performance and security problems and describe the fixes.""",
        q_bn=r"""এই order-history API-র p95 latency বড় customer-দের জন্য ২ সেকেন্ড, আর একটা security review-তেও এটা ধরা পড়েছে। Performance আর security সমস্যাগুলো চিহ্নিত করো আর সমাধান বর্ণনা করো।""",
        code=r"""
            app.get('/orders', async (req, res) => {
              const page = Number(req.query.page ?? 1);
              const rows = await db
                .select()
                .from(orders)
                .where(eq(orders.customerId, req.user.id))
                .orderBy(sql.raw(String(req.query.sort ?? 'created_at desc')))
                .limit(20)
                .offset((page - 1) * 20);

              const result = [];
              for (const order of rows) {
                const items = await db.select().from(orderItems).where(eq(orderItems.orderId, order.id));
                result.push({ ...order, items });
              }
              res.json(result);
            });

            app.post('/orders', async (req, res) => {
              const [order] = await db.insert(orders).values(req.body).returning();
              res.status(201).json(order);
            });
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                const listQuery = z.object({
                  cursor: z.coerce.number().int().positive().optional(),
                  order: z.enum(['newest', 'oldest']).default('newest'), // whitelist, never raw SQL
                });

                app.get('/orders', async (req, res) => {
                  const { cursor, order } = listQuery.parse(req.query);
                  const newest = order === 'newest';

                  const page = await db
                    .select({ id: orders.id, status: orders.status, total: orders.total, createdAt: orders.createdAt })
                    .from(orders)
                    .where(and(
                      eq(orders.customerId, req.user.id),
                      cursor ? (newest ? lt(orders.id, cursor) : gt(orders.id, cursor)) : undefined,
                    ))
                    .orderBy(newest ? desc(orders.id) : asc(orders.id))
                    .limit(20);

                  const ids = page.map((o) => o.id);
                  const items = ids.length
                    ? await db
                        .select({ orderId: orderItems.orderId, productId: orderItems.productId, qty: orderItems.qty })
                        .from(orderItems)
                        .where(inArray(orderItems.orderId, ids)) // one query instead of 20
                    : [];

                  const byOrder = Map.groupBy(items, (i) => i.orderId);
                  res.json(page.map((o) => ({ ...o, items: byOrder.get(o.id) ?? [] })));
                });

                const createOrder = z.strictObject({
                  items: z.array(z.strictObject({ productId: z.number().int(), qty: z.number().int().min(1).max(50) })).min(1),
                });

                app.post('/orders', async (req, res) => {
                  const input = createOrder.parse(req.body);
                  // customerId from the session, status and totals computed on the server
                  const order = await ordersService.create(req.user.id, input.items);
                  res.status(201).json(order);
                });

                // Indexes (schema): orders (customer_id, id); order_items (order_id)
            """),
        ],
        a_en=r"""
            **Performance**
            - **N+1 queries:** one query for orders plus one per order for items — 21 round trips per page. Fetch items for all orders with a single `inArray(orderItems.orderId, ids)` query (or a relational query with `with: { items: ... }`, which compiles to one statement) and group in memory.
            - **OFFSET pagination:** deep pages make PostgreSQL scan and discard rows; large customers page deep. Use keyset pagination on `id`.
            - **`select()` of every column** (including large JSON/address blobs) — select only what the API returns.
            - **Missing indexes:** PostgreSQL doesn't index foreign keys automatically. Add `orders (customer_id, id)` for the filtered, ordered scan and `order_items (order_id)` for the item lookup. Confirm with `EXPLAIN ANALYZE`.

            **Security**
            - **SQL injection:** `sql.raw(req.query.sort)` puts user input straight into the SQL text (`?sort=1; DROP TABLE ...` or data-exfiltrating subqueries). Whitelist allowed sorts and map them to column objects.
            - **Mass assignment:** `values(req.body)` lets a client set `status: 'paid'`, `total: 0` or another `customerId`. Validate with a strict schema, take `customerId` from the session and compute prices and totals on the server.
            - **Input validation:** `Number(req.query.page)` can be `NaN` or huge; validate and cap all query params.
        """,
        a_bn=r"""
            **Performance**
            - **N+1 query:** order-এর জন্য একটা query আর প্রতিটা order-এর item-এর জন্য একটা করে — প্রতি page-এ ২১টা round trip। একটাই `inArray(orderItems.orderId, ids)` query দিয়ে সব order-এর item আনো (অথবা `with: { items: ... }` সহ relational query, যেটা একটা statement-এ compile হয়) আর memory-তে group করো।
            - **OFFSET pagination:** গভীর page-এ PostgreSQL row scan করে ফেলে দেয়; বড় customer-রা অনেক গভীরে page করে। `id`-এর উপর keyset pagination ব্যবহার করো।
            - **সব column `select()` করা** (বড় JSON/address blob সহ) — API যা return করে শুধু সেটাই select করো।
            - **Index নেই:** PostgreSQL foreign key নিজে থেকে index করে না। Filtered, ordered scan-এর জন্য `orders (customer_id, id)` আর item lookup-এর জন্য `order_items (order_id)` যোগ করো। `EXPLAIN ANALYZE` দিয়ে নিশ্চিত হও।

            **Security**
            - **SQL injection:** `sql.raw(req.query.sort)` user input সরাসরি SQL text-এ বসিয়ে দেয় (`?sort=1; DROP TABLE ...` বা data বের করে নেওয়া subquery)। অনুমোদিত sort whitelist করো আর column object-এ map করো।
            - **Mass assignment:** `values(req.body)` দিয়ে client `status: 'paid'`, `total: 0` বা অন্য `customerId` set করতে পারে। Strict schema দিয়ে validate করো, `customerId` session থেকে নাও, আর price ও total server-এ হিসাব করো।
            - **Input validation:** `Number(req.query.page)` `NaN` বা বিশাল হতে পারে; সব query param validate আর সীমিত করো।
        """,
        quick_en=r"""Performance: N+1 item queries (batch with `inArray`), deep OFFSET paging (use keyset), selecting every column and missing FK indexes. Security: `sql.raw(req.query.sort)` is SQL injection (whitelist sorts), `values(req.body)` allows mass assignment, and query params aren't validated.""",
        quick_bn=r"""Performance: N+1 item query (`inArray` দিয়ে একবারে আনো), গভীর OFFSET paging (keyset ব্যবহার করো), সব column select, আর FK-তে index নেই। Security: `sql.raw(req.query.sort)` সরাসরি SQL injection (sort whitelist করো), `values(req.body)` mass assignment-এর সুযোগ দেয়, আর query param validate হয় না।""",
        ex_en=r"""
            - **How to find these in production:** enable query logging in staging (`drizzle({ client, logger: true })`), use `pg_stat_statements` to find the most expensive statements, and look for the same query repeated many times per request (the N+1 signature) in traces.
            - **Why the composite index `(customer_id, id)`:** it serves both the `WHERE customer_id = ?` filter and the `ORDER BY id` with a `LIMIT`, so PostgreSQL reads only 20 index entries instead of sorting all of a customer's orders.
            - **`inArray` with an empty list** compiles to `false` in Drizzle 0.45 (no crash), but skipping the query when there are no ids saves a round trip.
            - **Authorization:** filtering by `req.user.id` is correct; make sure every query for customer data is scoped the same way (or use row-level security as defence in depth).
            - `Map.groupBy` is ES2024 and available in current Node.js LTS.
        """,
        ex_bn=r"""
            - **Production-এ এগুলো কীভাবে খুঁজবে:** staging-এ query logging চালু করো (`drizzle({ client, logger: true })`), সবচেয়ে ব্যয়বহুল statement খুঁজতে `pg_stat_statements` ব্যবহার করো, আর trace-এ দেখো একই query প্রতি request-এ বহুবার চলছে কি না (N+1-এর চিহ্ন)।
            - **Composite index `(customer_id, id)` কেন:** এটা `WHERE customer_id = ?` filter আর `LIMIT` সহ `ORDER BY id` দুটোই সামলায়, তাই PostgreSQL একজন customer-এর সব order sort না করে শুধু ২০টা index entry পড়ে।
            - **ফাঁকা list-এ `inArray`** Drizzle 0.45-এ `false`-এ compile হয় (crash করে না), তবে id না থাকলে query skip করলে একটা round trip বাঁচে।
            - **Authorization:** `req.user.id` দিয়ে filter করা ঠিক আছে; নিশ্চিত করো customer data-র প্রতিটা query একইভাবে scoped (অথবা defence in depth হিসেবে row-level security)।
            - `Map.groupBy` হলো ES2024, current Node.js LTS-এ আছে।
        """,
        tip_en=r"""Split your answer into "performance" and "security" and rank by impact (injection and mass assignment first, then N+1). Mention how you'd *measure* (`EXPLAIN ANALYZE`, `pg_stat_statements`) rather than guess.""",
        tip_bn=r"""উত্তর "performance" আর "security"-তে ভাগ করো আর প্রভাব অনুযায়ী সাজাও (আগে injection আর mass assignment, তারপর N+1)। আন্দাজ না করে কীভাবে *মাপবে* সেটা বলো (`EXPLAIN ANALYZE`, `pg_stat_statements`)।""",
        mist_en=r"""Fixing N+1 with `Promise.all` over 20 queries (still 20 round trips and 20 pooled connections); escaping the sort string manually instead of whitelisting; adding indexes without checking the plan.""",
        mist_bn=r"""২০টা query-তে `Promise.all` দিয়ে N+1 "ঠিক" করা (তখনও ২০টা round trip আর ২০টা pooled connection); whitelist না করে sort string নিজে escape করা; plan না দেখে index যোগ করা।""",
        follow=[
            ("How would you confirm the new index is used?", "নতুন index ব্যবহার হচ্ছে কি না কীভাবে নিশ্চিত হবে?"),
            ("When is a relational query (`with`) better than two queries + grouping?", "কখন দুটো query + grouping-এর চেয়ে relational query (`with`) ভালো?"),
        ],
        related=["drizzle-008", "drizzle-015", "drizzle-022"],
        refs=[D_JOINS, PG_EXPLAIN, OWASP_MASS],
    ),
    # ------------------------------------------------------------------ drizzle-029
    Q(
        id="drizzle-029", sub="Schema Introspection (drizzle-kit pull)", diff="hard", type="scenario",
        prio="medium", market="both", mins=10,
        tags=["drizzle-kit-pull", "introspection", "brownfield", "baseline-migration"],
        ver="drizzle-kit 0.31 / Drizzle ORM 0.45.x", vs=True, status="stable",
        q_en=r"""You're introducing Drizzle into a 4-year-old production PostgreSQL database with 60 tables that has been managed with hand-written SQL scripts. How do you adopt Drizzle (schema and migrations) without breaking anything?""",
        q_bn=r"""তুমি ৪ বছরের পুরোনো একটা production PostgreSQL database-এ Drizzle আনছ, যেখানে ৬০টা table আছে আর এতদিন হাতে লেখা SQL script দিয়ে manage হয়েছে। কিছু না ভেঙে কীভাবে Drizzle (schema আর migration) চালু করবে?""",
        a_en=r"""
            1. **Work on a copy first:** restore a recent production backup to staging; never introspect and experiment against production.
            2. **Configure Drizzle Kit** with `schemaFilter` / `tablesFilter` if only some schemas or tables should be managed, and `introspect: { casing }` to choose the generated TypeScript keys (`'camel'`, the default, turns `created_at` into `createdAt`; `'preserve'` keeps database names).
            3. **Introspect:** `drizzle-kit pull` generates `schema.ts`, `relations.ts` and an initial SQL migration from the live database. In drizzle-kit 0.31 that SQL is **commented out** by design — the tables already exist, so applying it must be a no-op.
            4. **Review the generated schema:** column types, defaults, enums, indexes, FK actions. Rename TypeScript keys if needed (the database names stay the same). Then run `drizzle-kit generate` — it should report **no changes**; if it doesn't, the schema doesn't match reality yet.
            5. **Baseline:** record that initial migration as applied without running any DDL. Careful: the migrator splits files on `--> statement-breakpoint` even inside the `/* ... */` block, so running the file as generated fails with `unterminated /* comment` (SQLSTATE `42601`). Remove those markers inside the comment (or replace the body with a single `-- baseline` comment line), then run `migrate` — it records `0000` in `drizzle.__drizzle_migrations` and changes nothing. (The v1 RC adds `drizzle-kit pull --init` for this — preview.) From now on, every change goes through `generate` → review → `migrate`.
            6. **Adopt queries incrementally:** new features use Drizzle; existing raw SQL keeps working (wrap it in `db.execute(sql...)` to share the pool and transactions). Freeze the old script folder.

            Anything Drizzle doesn't model — triggers, functions, custom types or extensions — stays in **custom migrations** (`generate --custom`) so it's still versioned.
        """,
        a_bn=r"""
            1. **আগে কপিতে কাজ করো:** সাম্প্রতিক production backup staging-এ restore করো; production-এর বিরুদ্ধে কখনো introspect আর experiment কোরো না।
            2. **Drizzle Kit configure করো:** শুধু কিছু schema বা table manage করতে চাইলে `schemaFilter` / `tablesFilter`, আর generated TypeScript key বেছে নিতে `introspect: { casing }` (`'camel'`, যেটা default, `created_at`-কে `createdAt` বানায়; `'preserve'` database-এর নামই রাখে)।
            3. **Introspect:** `drizzle-kit pull` live database থেকে `schema.ts`, `relations.ts` আর একটা initial SQL migration তৈরি করে। drizzle-kit 0.31-এ সেই SQL design অনুযায়ী **comment করা** থাকে — table আগে থেকেই আছে, তাই apply করলে কিছুই হওয়া উচিত না।
            4. **Generated schema review করো:** column type, default, enum, index, FK action। দরকার হলে TypeScript key-এর নাম বদলাও (database-এর নাম একই থাকে)। তারপর `drizzle-kit generate` চালাও — এটার **কোনো পরিবর্তন নেই** বলা উচিত; যদি বলে, schema এখনো বাস্তবের সাথে মেলেনি।
            5. **Baseline:** কোনো DDL না চালিয়ে initial migration-টাকে applied হিসেবে record করো। সাবধান: migrator `/* ... */` block-এর ভেতরেও `--> statement-breakpoint` দেখে file ভাগ করে, তাই generate হওয়া file যেমন আছে তেমন চালালে `unterminated /* comment` (SQLSTATE `42601`) দিয়ে fail করে। Comment-এর ভেতরের ওই marker গুলো মুছে দাও (বা body-টা একটা `-- baseline` comment line দিয়ে বদলে দাও), তারপর `migrate` চালাও — এটা `drizzle.__drizzle_migrations`-এ `0000` record করে, কিছুই বদলায় না। (v1 RC-তে এর জন্য `drizzle-kit pull --init` আছে — preview।) এখন থেকে প্রতিটা পরিবর্তন যাবে `generate` → review → `migrate` দিয়ে।
            6. **ধাপে ধাপে query adopt করো:** নতুন feature Drizzle ব্যবহার করবে; existing raw SQL চলতে থাকবে (pool আর transaction share করতে `db.execute(sql...)`-এ wrap করো)। পুরোনো script folder freeze করো।

            Drizzle যা model করে না — trigger, function, custom type বা extension — সেগুলো **custom migration**-এ (`generate --custom`) থাকে, যাতে versioned থাকে।
        """,
        quick_en=r"""Work on a restored copy, run `drizzle-kit pull` to generate the schema, review it until `generate` reports no changes, then record the initial migration as applied without running any DDL. After that every change goes through `generate` → review → `migrate`, while old raw SQL keeps working through `db.execute(sql...)`.""",
        quick_bn=r"""Restore করা copy-তে কাজ করি, `drizzle-kit pull` দিয়ে schema বানাই, `generate` "no changes" না বলা পর্যন্ত review করি, তারপর কোনো DDL না চালিয়ে initial migration-কে applied হিসেবে record করি। এরপর প্রতিটা change যায় `generate` → review → `migrate` পথে, আর পুরোনো raw SQL `db.execute(sql...)` দিয়ে চলতে থাকে।""",
        ex_en=r"""
            - **Why "no changes" after pull matters:** it proves the TypeScript schema is a faithful model. If you skip this, the first real `generate` may include surprise `ALTER`s that "fix" differences you didn't intend to change.
            - **Drift between environments:** staging and production may have diverged over 4 years (hotfixes applied by hand). Introspect each, diff them, and reconcile before baselining.
            - **Ownership:** decide one source of truth from now on — the Drizzle schema plus migrations — and block manual DDL in production (restricted roles).
            - **Testing:** run the app's test suite against a database built only from migrations (empty DB → `migrate`) to catch anything missing from the baseline.
            - **Team rollout:** a short guide in the repo ("how to add a column") prevents people from going back to ad-hoc scripts.
        """,
        ex_bn=r"""
            - **Pull-এর পরে "no changes" কেন গুরুত্বপূর্ণ:** এতে প্রমাণ হয় TypeScript schema বাস্তবের বিশ্বস্ত model। এটা বাদ দিলে প্রথম আসল `generate`-এ অপ্রত্যাশিত `ALTER` থাকতে পারে, যেগুলো এমন পার্থক্য "ঠিক" করে যা তুমি বদলাতে চাওনি।
            - **Environment-এর মধ্যে drift:** ৪ বছরে staging আর production আলাদা হয়ে যেতে পারে (হাতে apply করা hotfix)। প্রতিটা introspect করো, diff করো, baseline করার আগে মিলিয়ে নাও।
            - **মালিকানা:** এখন থেকে একটাই source of truth ঠিক করো — Drizzle schema আর migration — আর production-এ হাতে DDL চালানো বন্ধ করো (সীমিত role)।
            - **Testing:** শুধু migration দিয়ে তৈরি database-এ (ফাঁকা DB → `migrate`) app-এর test suite চালাও, যাতে baseline-এ কিছু বাদ পড়লে ধরা পড়ে।
            - **Team rollout:** repo-তে একটা ছোট guide ("কীভাবে column যোগ করবে") মানুষকে আবার ad-hoc script-এ ফিরে যাওয়া থেকে আটকায়।
        """,
        tip_en=r"""Emphasise risk control: copy of production, verified "no diff" after pull, baseline without DDL, incremental adoption. Interviewers for senior roles care more about the safety steps than the commands.""",
        tip_bn=r"""ঝুঁকি নিয়ন্ত্রণে জোর দাও: production-এর কপি, pull-এর পরে যাচাই করা "no diff", DDL ছাড়া baseline, ধাপে ধাপে adoption। Senior role-এর interviewer command-এর চেয়ে নিরাপত্তার ধাপগুলোকে বেশি গুরুত্ব দেয়।""",
        mist_en=r"""Running `drizzle-kit push` against the legacy production database; uncommenting the introspected SQL and running it (fails or duplicates objects); rewriting all queries at once; ignoring objects Drizzle doesn't model.""",
        mist_bn=r"""Legacy production database-এ `drizzle-kit push` চালানো; introspect করা SQL uncomment করে চালানো (fail করে বা object duplicate হয়); সব query একবারে আবার লেখা; Drizzle যা model করে না সেগুলো উপেক্ষা করা।""",
        code=r"""
            // drizzle.config.ts — manage only the app schema
            import { defineConfig } from 'drizzle-kit';

            export default defineConfig({
              dialect: 'postgresql',
              schema: './src/db/schema.ts',
              out: './drizzle',
              dbCredentials: { url: process.env.DATABASE_URL! },
              schemaFilter: ['public'],
              tablesFilter: ['!legacy_*'], // skip tables you don't want Drizzle to manage
              introspect: { casing: 'camel' }, // TS keys for pulled columns (default; 'preserve' keeps DB names)
            });

            // $ npx drizzle-kit pull       -> drizzle/schema.ts, drizzle/relations.ts, drizzle/0000_*.sql
            // The 0000 SQL starts with:
            //   -- Current sql file was generated after introspecting the database
            //   -- If you want to run this migration please uncomment this code before executing migrations
            //   /* CREATE TABLE ... */
            // $ npx drizzle-kit generate   -> should report no schema changes
            // Before migrating: delete the "--> statement-breakpoint" markers inside the /* */ block
            // (otherwise migrate splits the comment and fails with 42601 "unterminated /* comment")
            // $ npx drizzle-kit migrate    -> records the baseline, executes no DDL
        """,
        lang="typescript",
        follow=[
            ("How would you detect schema drift between staging and production?", "Staging আর production-এর মধ্যে schema drift কীভাবে ধরবে?"),
            ("How do you version database functions and triggers with Drizzle Kit?", "Drizzle Kit দিয়ে database function আর trigger কীভাবে version করবে?"),
        ],
        related=["drizzle-017", "drizzle-031"],
        refs=[D_KIT_PULL, D_CONFIG],
    ),
    # ------------------------------------------------------------------ drizzle-030
    Q(
        id="drizzle-030", sub="Data-layer System Design", diff="extreme", type="system-design",
        prio="medium", market="international", mins=25,
        tags=["flash-sale", "inventory", "contention", "skip-locked", "read-replicas"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""Design the order/inventory data layer (TypeScript + Drizzle + PostgreSQL) for a flash sale: e.g. a big-sale event where 50,000 users try to buy 1,000 units of a few hot products in the first minute. Requirements: never oversell, keep checkout fast, release unpaid reservations after 10 minutes, and keep product pages responsive.""",
        q_bn=r"""একটা flash sale-এর জন্য order/inventory data layer (TypeScript + Drizzle + PostgreSQL) design করো: যেমন একটা বড় sale event, যেখানে প্রথম মিনিটে ৫০,০০০ user কয়েকটা hot product-এর ১,০০০ unit কিনতে চেষ্টা করে। Requirement: কখনো oversell হবে না, checkout দ্রুত থাকবে, ১০ মিনিটে payment না হলে reservation ছেড়ে দেবে, আর product page responsive থাকবে।""",
        a_en=r"""
            This is an advanced system-design scenario.

            **1. Source of truth:** stock lives in PostgreSQL with `CHECK (stock >= 0)`. Reservations are rows: `reservations(id, product_id, user_id, qty, status, expires_at)` with a unique `(user_id, product_id, sale_id)` to stop one user grabbing everything.

            **2. Reserve atomically:** one short transaction: `UPDATE products SET stock = stock - :qty WHERE id = :id AND stock >= :qty RETURNING` + `INSERT reservation`. No `SELECT` then `UPDATE`, no external calls. Under READ COMMITTED the row lock + re-check guarantees no oversell.

            **3. Hot-row contention:** every buyer updates the same row, so throughput ≈ 1 / (lock hold time). Keep transactions tiny, and if that's not enough:
            - **Admission control:** a Redis atomic counter (or a queue) in front lets only roughly `stock` requests through to PostgreSQL; the rest get "sold out" instantly. PostgreSQL stays the authority; reconcile counters after the sale.
            - **Bucketed stock:** split 1,000 units into e.g. 10 rows of 100 and pick a random non-empty bucket, spreading locks.
            - **Async checkout:** enqueue purchase requests and process them with a few workers; clients poll or get a push.

            **4. Expiry:** a worker claims expired reservations with `SELECT ... FOR UPDATE SKIP LOCKED LIMIT 100`, returns stock and marks them expired in the same transaction — several workers can run without blocking each other.

            **5. Reads:** product pages come from cache/CDN with approximate stock; browsing queries go to read replicas (Drizzle `withReplicas`), while checkout always hits the primary (replica lag is fine for "only a few left", not for reservations).

            **6. Operational guardrails:** PgBouncer for connection fan-in, `statement_timeout`/`lock_timeout`, idempotency keys on "reserve", rate limiting per user, and a load test that replays sale traffic before the event.
        """,
        a_bn=r"""
            এটা একটা advanced system-design scenario।

            **১. Source of truth:** stock থাকে PostgreSQL-এ, `CHECK (stock >= 0)` সহ। Reservation হলো row: `reservations(id, product_id, user_id, qty, status, expires_at)`, unique `(user_id, product_id, sale_id)` সহ, যাতে একজন user সব কিনে নিতে না পারে।

            **২. Atomically reserve:** একটা ছোট transaction: `UPDATE products SET stock = stock - :qty WHERE id = :id AND stock >= :qty RETURNING` + `INSERT reservation`। আগে `SELECT` তারপর `UPDATE` না, কোনো external call না। READ COMMITTED-এ row lock + আবার যাচাই নিশ্চিত করে oversell হবে না।

            **৩. Hot-row contention:** প্রত্যেক ক্রেতা একই row update করে, তাই throughput ≈ 1 / (lock ধরে রাখার সময়)। Transaction খুব ছোট রাখো, আর তাতেও না হলে:
            - **Admission control:** সামনে একটা Redis atomic counter (বা queue) মোটামুটি `stock` সংখ্যক request-কেই PostgreSQL পর্যন্ত যেতে দেয়; বাকিরা সাথে সাথে "sold out" পায়। PostgreSQL-ই কর্তৃপক্ষ থাকে; sale-এর পরে counter মিলিয়ে নাও।
            - **Bucketed stock:** ১,০০০ unit-কে যেমন ১০০ করে ১০টা row-এ ভাগ করো আর random একটা non-empty bucket বেছে নাও, এতে lock ছড়িয়ে যায়।
            - **Async checkout:** purchase request queue-তে রাখো আর কয়েকটা worker দিয়ে process করো; client poll করে বা push পায়।

            **৪. Expiry:** একটা worker `SELECT ... FOR UPDATE SKIP LOCKED LIMIT 100` দিয়ে মেয়াদোত্তীর্ণ reservation দখল করে, একই transaction-এ stock ফেরত দেয় আর expired mark করে — কয়েকটা worker একে অপরকে block না করেই চলতে পারে।

            **৫. Read:** product page আসে cache/CDN থেকে, আনুমানিক stock সহ; browsing query যায় read replica-তে (Drizzle `withReplicas`), আর checkout সবসময় primary-তে (replica lag "আর অল্প কয়েকটা বাকি"-র জন্য ঠিক আছে, reservation-এর জন্য না)।

            **৬. Operational guardrail:** connection fan-in-এর জন্য PgBouncer, `statement_timeout`/`lock_timeout`, "reserve"-এ idempotency key, user প্রতি rate limiting, আর event-এর আগে sale traffic replay করে load test।
        """,
        quick_en=r"""Keep stock in PostgreSQL with `CHECK (stock >= 0)` and reserve with one short guarded `UPDATE ... WHERE stock >= qty` plus a reservation row, so it can't oversell. Add admission control or bucketed stock for the hot rows, expire reservations with `FOR UPDATE SKIP LOCKED` workers, and serve product pages from cache.""",
        quick_bn=r"""Stock থাকে PostgreSQL-এ `CHECK (stock >= 0)`-সহ, আর reserve করি একটাই ছোট guarded `UPDATE ... WHERE stock >= qty` আর একটা reservation row দিয়ে — তাই oversell হয় না। Hot row-এর জন্য admission control বা bucketed stock, `FOR UPDATE SKIP LOCKED` worker দিয়ে reservation expire, আর product page cache থেকে।""",
        ex_en=r"""
            **Failure scenarios to discuss:**
            - *Payment succeeds after the reservation expired:* the payment handler must check the reservation status in a transaction; if expired, either re-reserve if stock remains or refund automatically.
            - *Redis counter and PostgreSQL disagree:* Redis is only a gate. A rejected-by-PostgreSQL request (stock already 0) returns "sold out" even if Redis let it through.
            - *Replica lag:* a user sees "in stock" on a lagging replica; checkout still decides on the primary, so the worst case is a polite "sold out".
            - *Retry storms:* clients hammering "buy" — rate limit per user and return `Retry-After`.

            **Why not SERIALIZABLE for everything?** On a hot row it produces many `40001` failures that must be retried, adding load exactly when you have the least capacity. The conditional UPDATE has the same safety for this invariant with far less overhead.

            **Drizzle specifics:** `.for('update', { skipLocked: true })` for the sweeper, `withReplicas(primary, [replica])` (reads go to replicas; writes and transactions go to the primary; `db.$primary` forces a primary read).
        """,
        ex_bn=r"""
            **যে failure scenario আলোচনা করবে:**
            - *Reservation-এর মেয়াদ শেষ হওয়ার পর payment সফল:* payment handler-কে একটা transaction-এ reservation-এর status check করতে হবে; expired হলে stock থাকলে আবার reserve করো, নাহলে automatically refund।
            - *Redis counter আর PostgreSQL মেলে না:* Redis শুধু একটা gate। PostgreSQL যদি reject করে (stock আগেই 0), Redis ঢুকতে দিলেও উত্তর "sold out"।
            - *Replica lag:* পিছিয়ে থাকা replica-য় user "in stock" দেখে; checkout তবুও primary-তে সিদ্ধান্ত নেয়, তাই সবচেয়ে খারাপ ক্ষেত্রে একটা ভদ্র "sold out"।
            - *Retry storm:* client বারবার "buy" চাপে — user প্রতি rate limit দাও আর `Retry-After` return করো।

            **সবকিছুর জন্য SERIALIZABLE কেন না?** Hot row-এ এটা অনেক `40001` failure দেয় যেগুলো retry করতে হয়, ঠিক যখন capacity সবচেয়ে কম তখন load বাড়ায়। এই invariant-এর জন্য conditional UPDATE একই নিরাপত্তা দেয়, অনেক কম overhead-এ।

            **Drizzle-এর দিক:** sweeper-এর জন্য `.for('update', { skipLocked: true })`, `withReplicas(primary, [replica])` (read যায় replica-তে; write আর transaction যায় primary-তে; `db.$primary` primary থেকে পড়তে বাধ্য করে)।
        """,
        tip_en=r"""Anchor the design on the invariant ("stock never below zero") and show where it's enforced (one atomic statement + CHECK). Then talk throughput limits of a hot row and layered mitigations — that's what separates senior answers.""",
        tip_bn=r"""Design-কে invariant-এর উপর দাঁড় করাও ("stock কখনো শূন্যের নিচে না") আর দেখাও এটা কোথায় enforce হয় (একটা atomic statement + CHECK)। তারপর hot row-এর throughput সীমা আর ধাপে ধাপে প্রতিকার নিয়ে কথা বলো — senior উত্তর এখানেই আলাদা হয়।""",
        mist_en=r"""Using Redis as the only source of truth for stock; reading stock from a replica during checkout; holding a transaction open across the payment call; one global lock (advisory lock or mutex) that serialises every product.""",
        mist_bn=r"""Stock-এর একমাত্র source of truth হিসেবে Redis ব্যবহার করা; checkout-এর সময় replica থেকে stock পড়া; payment call জুড়ে transaction খোলা রাখা; সব product-কে এক লাইনে দাঁড় করানো একটা global lock (advisory lock বা mutex)।""",
        code=r"""
            import { and, eq, gte, inArray, lt, sql } from 'drizzle-orm';
            import { withReplicas } from 'drizzle-orm/pg-core';

            export const db = withReplicas(primaryDb, [replicaDb]); // selects -> replica, writes/tx -> primary

            // Reserve: one short transaction, invariant enforced by the conditional UPDATE
            export async function reserve(userId: number, productId: number, qty: number) {
              return db.transaction(async (tx) => {
                const updated = await tx
                  .update(products)
                  .set({ stock: sql`${products.stock} - ${qty}` })
                  .where(and(eq(products.id, productId), gte(products.stock, qty)))
                  .returning({ stock: products.stock });
                if (updated.length === 0) return null; // sold out

                const [r] = await tx
                  .insert(reservations)
                  .values({ userId, productId, qty, status: 'pending', expiresAt: sql`now() + interval '10 minutes'` })
                  .returning({ id: reservations.id });
                return r;
              });
            }

            // Sweeper: many workers can run in parallel thanks to SKIP LOCKED
            export async function releaseExpired() {
              return db.transaction(async (tx) => {
                const expired = await tx
                  .select({ id: reservations.id, productId: reservations.productId, qty: reservations.qty })
                  .from(reservations)
                  .where(and(eq(reservations.status, 'pending'), lt(reservations.expiresAt, sql`now()`)))
                  .orderBy(reservations.id)
                  .limit(100)
                  .for('update', { skipLocked: true });

                for (const r of expired) {
                  await tx.update(products).set({ stock: sql`${products.stock} + ${r.qty}` }).where(eq(products.id, r.productId));
                }
                if (expired.length > 0) {
                  await tx.update(reservations).set({ status: 'expired' })
                    .where(inArray(reservations.id, expired.map((r) => r.id)));
                }
                return expired.length;
              });
            }
        """,
        lang="typescript",
        follow=[
            ("How would you estimate the maximum checkouts per second on a single hot row?", "একটা hot row-এ প্রতি সেকেন্ডে সর্বোচ্চ কতগুলো checkout হতে পারে কীভাবে আন্দাজ করবে?"),
            ("What happens if the sweeper crashes halfway through a batch?", "Sweeper একটা batch-এর মাঝপথে crash করলে কী হয়?"),
        ],
        related=["drizzle-025", "drizzle-016", "nest-032"],
        refs=[D_TRANSACTIONS, D_READ_REPLICAS, PG_LOCKING],
    ),
    # ------------------------------------------------------------------ drizzle-031
    Q(
        id="drizzle-031", sub="Data Access Architecture", diff="extreme", type="architecture",
        prio="medium", market="international", mins=20,
        tags=["architecture", "repositories", "unit-of-work", "orm-vs-sql", "testing"],
        ver="Drizzle ORM 0.45.x / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""You're the tech lead for a TypeScript backend with ~150 tables and 12 developers, using Drizzle and PostgreSQL. How would you structure the data-access layer: schema organisation, repositories, transactions across services, reporting queries, read replicas and testing? Where is an ORM the right tool, and where isn't it?""",
        q_bn=r"""তুমি প্রায় ১৫০টা table আর ১২ জন developer-এর একটা TypeScript backend-এর tech lead, Drizzle আর PostgreSQL ব্যবহার হচ্ছে। Data-access layer কীভাবে সাজাবে: schema organisation, repository, service জুড়ে transaction, reporting query, read replica আর testing? কোথায় ORM সঠিক tool, আর কোথায় না?""",
        a_en=r"""
            This is advanced architecture material.

            **Schema organisation:** one schema file per bounded context (`orders/schema.ts`, `catalog/schema.ts`), re-exported from a single `db/schema.ts` that Drizzle Kit points at. Each context owns its tables; cross-context access goes through that context's service, not its tables.

            **Repositories:** thin, intention-revealing functions (`ordersRepo.findOpenByCustomer(conn, id)`) instead of generic `BaseRepository<T>` wrappers that hide Drizzle's power. Every repository method takes a `DbOrTx` parameter.

            **Transactions (unit of work):** the *service* layer owns transaction boundaries: `db.transaction(async (tx) => { await ordersRepo.create(tx, ...); await inventoryRepo.reserve(tx, ...); })`. Passing `tx` explicitly makes it visible in code review which writes are atomic. (AsyncLocalStorage-based propagation is an alternative but hides the boundary.)

            **Where the ORM fits:** CRUD, filtering, joins and entity graphs — type safety and refactoring support pay off daily. **Where it doesn't:** heavy analytics (window functions, recursive CTEs, rollups), bulk ETL, and DB-specific tuning. Write those as SQL — via the `sql` tag, views (`pgView`) or materialised views — keeping parameters bound and results typed with a declared row type.

            **Read replicas:** `withReplicas()` for read-heavy endpoints; anything that must read its own writes uses the primary (`db.$primary`).

            **Testing:** unit-test services with fake repositories; integration-test repositories and migrations against real PostgreSQL (disposable containers in CI, migrated from scratch); add concurrency tests for invariants (stock, balances).
        """,
        a_bn=r"""
            এটা advanced architecture বিষয়।

            **Schema organisation:** প্রতিটা bounded context-এর জন্য একটা schema file (`orders/schema.ts`, `catalog/schema.ts`), একটা `db/schema.ts` থেকে re-export করা, যেটার দিকে Drizzle Kit point করে। প্রতিটা context নিজের table-এর মালিক; অন্য context-এ যেতে হলে ওই context-এর service দিয়ে, তার table দিয়ে না।

            **Repository:** Drizzle-এর ক্ষমতা লুকিয়ে ফেলা generic `BaseRepository<T>` wrapper-এর বদলে পাতলা, উদ্দেশ্য-স্পষ্ট function (`ordersRepo.findOpenByCustomer(conn, id)`)। প্রতিটা repository method একটা `DbOrTx` parameter নেয়।

            **Transaction (unit of work):** transaction-এর সীমানা *service* layer-এর হাতে: `db.transaction(async (tx) => { await ordersRepo.create(tx, ...); await inventoryRepo.reserve(tx, ...); })`। `tx` explicitly pass করলে code review-তে স্পষ্ট দেখা যায় কোন write গুলো atomic। (AsyncLocalStorage-based propagation একটা বিকল্প, কিন্তু সীমানা লুকিয়ে ফেলে।)

            **ORM কোথায় মানায়:** CRUD, filtering, join আর entity graph — type safety আর refactoring support প্রতিদিন কাজে লাগে। **কোথায় মানায় না:** ভারী analytics (window function, recursive CTE, rollup), bulk ETL, আর DB-specific tuning। এগুলো SQL হিসেবে লেখো — `sql` tag, view (`pgView`) বা materialised view দিয়ে — parameter bound রেখে, আর declared row type দিয়ে result typed করে।

            **Read replica:** read-heavy endpoint-এর জন্য `withReplicas()`; যেটাকে নিজের write পড়তে হবে সেটা primary ব্যবহার করে (`db.$primary`)।

            **Testing:** fake repository দিয়ে service-এর unit test; আসল PostgreSQL-এর বিরুদ্ধে repository আর migration-এর integration test (CI-তে disposable container, শুরু থেকে migrate করা); invariant-এর (stock, balance) জন্য concurrency test।
        """,
        quick_en=r"""Split the schema per bounded context, use thin repositories that accept `db` or `tx`, and let services own transaction boundaries by passing `tx` explicitly. Use Drizzle for CRUD and joins but plain SQL (`sql` tag, views) for heavy analytics, `withReplicas()` for reads, and integration tests on real PostgreSQL.""",
        quick_bn=r"""Schema bounded context ধরে ভাগ করি, পাতলা repository বানাই যেগুলো `db` বা `tx` নেয়, আর `tx` explicitly pass করে transaction-এর সীমা service-এর হাতে রাখি। CRUD আর join-এ Drizzle, ভারী analytics-এ সাধারণ SQL (`sql` tag, view), read-এ `withReplicas()`, আর আসল PostgreSQL-এ integration test।""",
        ex_en=r"""
            **Trade-offs to discuss:**
            - *Explicit `tx` vs ambient context:* explicit is verbose but impossible to misuse silently; ambient (ALS) is convenient but makes "is this inside a transaction?" invisible — a common source of the `db`-instead-of-`tx` bug.
            - *Generic repositories:* they look DRY but end up re-implementing a worse query builder. Prefer specific methods and let Drizzle be the query language.
            - *One schema module vs many:* many files scale better for ownership (CODEOWNERS per context); a single barrel keeps Drizzle Kit and relational queries simple.

            **Governance at 12 developers:** migration review checklist (locks, backfills, expand–contract), `drizzle-kit check` in CI, lint rules (`no-floating-promises` with `checkThenables: true`, `eslint-plugin-drizzle`), and query budgets per endpoint watched via `pg_stat_statements`.

            **Failure modes:** connection exhaustion from per-request pools, accidental cross-context joins that block future extraction, and reports running on the primary during peak hours (move them to a replica or a warehouse).
        """,
        ex_bn=r"""
            **যে trade-off গুলো আলোচনা করবে:**
            - *Explicit `tx` বনাম ambient context:* explicit একটু লম্বা, কিন্তু চুপচাপ ভুল ব্যবহার অসম্ভব; ambient (ALS) সুবিধাজনক, কিন্তু "এটা কি transaction-এর ভেতরে?" অদৃশ্য করে দেয় — `tx`-এর বদলে `db` bug-এর common উৎস।
            - *Generic repository:* দেখতে DRY লাগে, কিন্তু শেষে একটা খারাপ query builder আবার বানানো হয়। নির্দিষ্ট method রাখো আর Drizzle-কেই query language হতে দাও।
            - *একটা schema module বনাম অনেক:* অনেক file ownership-এর জন্য ভালো scale করে (context প্রতি CODEOWNERS); একটা barrel Drizzle Kit আর relational query সহজ রাখে।

            **১২ জন developer-এ governance:** migration review checklist (lock, backfill, expand–contract), CI-তে `drizzle-kit check`, lint rule (`checkThenables: true` সহ `no-floating-promises`, `eslint-plugin-drizzle`), আর `pg_stat_statements` দিয়ে endpoint প্রতি query budget নজরে রাখা।

            **Failure mode:** per-request pool থেকে connection শেষ হয়ে যাওয়া, অসাবধান cross-context join যা ভবিষ্যতে আলাদা করা আটকায়, আর peak hour-এ primary-তে report চলা (replica বা warehouse-এ সরাও)।
        """,
        tip_en=r"""Show principles, not just folders: ownership per context, explicit transaction boundaries, "ORM for OLTP, SQL for analytics", and tests against real PostgreSQL. Concrete trade-offs (explicit `tx` vs ALS) make it a senior answer.""",
        tip_bn=r"""শুধু folder না, নীতি দেখাও: context প্রতি মালিকানা, explicit transaction boundary, "OLTP-র জন্য ORM, analytics-এর জন্য SQL", আর আসল PostgreSQL-এর বিরুদ্ধে test। নির্দিষ্ট trade-off (explicit `tx` বনাম ALS) উত্তরটাকে senior-level করে।""",
        mist_en=r"""Wrapping Drizzle in a generic repository that hides joins and SQL; letting each repository open its own transaction; mocking the database in all tests; forcing complex reports through the query builder.""",
        mist_bn=r"""Drizzle-কে এমন generic repository-তে wrap করা যা join আর SQL লুকিয়ে ফেলে; প্রতিটা repository-কে নিজের transaction খুলতে দেওয়া; সব test-এ database mock করা; জটিল report জোর করে query builder দিয়ে লেখা।""",
        code=r"""
            // db/types.ts
            export type Db = typeof db;
            export type Tx = Parameters<Parameters<Db['transaction']>[0]>[0];
            export type DbOrTx = Db | Tx;

            // orders/orders.repository.ts — specific, tx-aware methods
            export const ordersRepo = {
              async create(conn: DbOrTx, data: NewOrder) {
                const [order] = await conn.insert(orders).values(data).returning();
                return order;
              },
              findOpenByCustomer(conn: DbOrTx, customerId: number) {
                return conn.select().from(orders)
                  .where(and(eq(orders.customerId, customerId), eq(orders.status, 'open')));
              },
            };

            // orders/orders.service.ts — the service owns the transaction boundary
            export async function checkout(customerId: number, items: CartItem[]) {
              return db.transaction(async (tx) => {
                await inventoryRepo.reserveAll(tx, items);
                return ordersRepo.create(tx, { customerId, status: 'open' });
              });
            }

            // reports/revenue.ts — analytics in SQL, still parameterised and typed
            type RevenueRow = { day: string; revenue: string; rank: number };
            export function topDays(from: Date) {
              return db.execute<RevenueRow>(sql`
                select day, revenue, rank() over (order by revenue desc)::int as rank
                from (
                  select date_trunc('day', ${orders.createdAt})::date::text as day, sum(${orders.total}) as revenue
                  from ${orders}
                  where ${orders.createdAt} >= ${from}
                  group by 1
                ) d
                order by rank
                limit 10`);
            }
        """,
        lang="typescript",
        follow=[
            ("Explicit `tx` parameters or AsyncLocalStorage — which would you standardise on and why?", "Explicit `tx` parameter নাকি AsyncLocalStorage — কোনটাকে standard করবে আর কেন?"),
            ("How do you keep integration tests fast with a real PostgreSQL?", "আসল PostgreSQL দিয়ে integration test দ্রুত কীভাবে রাখবে?"),
        ],
        related=["drizzle-011", "drizzle-020", "drizzle-025"],
        refs=[D_OVERVIEW, D_SQL, D_READ_REPLICAS],
    ),
    # ------------------------------------------------------------------ drizzle-032
    Q(
        id="drizzle-032", sub="Migrations in Production (Incident)", diff="extreme", type="scenario",
        prio="high", market="both", mins=20,
        tags=["incident", "migrations", "create-index-concurrently", "locks", "drizzle-kit"],
        ver="drizzle-kit 0.31 / Drizzle ORM 0.45.x / PostgreSQL 18", vs=True, status="stable",
        q_en=r"""Incident: a release added `index('orders_customer_id_idx').on(t.customerId)` to the Drizzle schema. CI ran `drizzle-kit migrate` against production during business hours. For 7 minutes, checkouts timed out (the `orders` table has 40M rows). A teammate's quick fix — adding `.concurrently()` to the index — made the next deploy's migration fail with `CREATE INDEX CONCURRENTLY cannot run inside a transaction block`, and the deploy pipeline was blocked. What happened, how do you respond now, and how do you prevent it?""",
        q_bn=r"""Incident: একটা release Drizzle schema-য় `index('orders_customer_id_idx').on(t.customerId)` যোগ করেছিল। CI business hour-এ production-এ `drizzle-kit migrate` চালায়। ৭ মিনিট ধরে checkout timeout হচ্ছিল (`orders` table-এ ৪ কোটি row)। একজন teammate দ্রুত সমাধান হিসেবে index-এ `.concurrently()` যোগ করেন — এতে পরের deploy-এর migration `CREATE INDEX CONCURRENTLY cannot run inside a transaction block` দিয়ে fail করে, আর deploy pipeline আটকে যায়। কী হয়েছিল, এখন কীভাবে সামলাবে, আর ভবিষ্যতে কীভাবে আটকাবে?""",
        a_en=r"""
            This is an advanced production-incident scenario.

            **What happened:**
            1. Drizzle Kit generated a plain `CREATE INDEX ... ON "orders"`. A normal index build takes a lock that **blocks all writes** (inserts/updates/deletes) on the table until the build finishes — on 40M rows, minutes. Checkouts insert into `orders`, so they queued and timed out.
            2. `.concurrently()` makes Drizzle Kit emit `CREATE INDEX CONCURRENTLY`, which doesn't block writes — but PostgreSQL forbids it inside a transaction, and Drizzle's migrator runs **all pending migrations of a run in a single transaction**. So the run failed (SQLSTATE `25001`) and rolled back everything in it, including unrelated migrations queued in the same deploy.

            **Respond now:**
            - Unblock the pipeline: the failing migration never applied anywhere, so replace its SQL with a comment-only no-op ("index created out-of-band, see incident #123"). The migrator then records it and the other pending migrations can run again.
            - Build the index manually **outside any transaction** (psql or an online-DDL job): `CREATE INDEX CONCURRENTLY IF NOT EXISTS ...` with `lock_timeout` set, during low traffic, and monitor `pg_stat_progress_create_index`.
            - Check for an `INVALID` index left by a failed concurrent attempt (`pg_index.indisvalid = false`) and drop it before retrying.
            - Keep the index in the Drizzle schema so the snapshot matches the database and future diffs stay clean.

            **Prevent:**
            - A migration review checklist: any index/constraint on a large table must be concurrent and shipped as its own step outside the migrator transaction.
            - A separate "online DDL" job/runner for non-transactional statements; normal `migrate` for everything else.
            - Run migrations as a dedicated, observable release step with `lock_timeout`/`statement_timeout`, not silently inside CI, and not at peak hours for risky changes.
            - Test migrations against a production-sized copy to measure lock duration.
        """,
        a_bn=r"""
            এটা একটা advanced production-incident scenario।

            **কী হয়েছিল:**
            1. Drizzle Kit একটা সাধারণ `CREATE INDEX ... ON "orders"` generate করেছিল। সাধারণ index build এমন lock নেয় যেটা build শেষ না হওয়া পর্যন্ত table-এর **সব write** (insert/update/delete) block করে — ৪ কোটি row-এ কয়েক মিনিট। Checkout `orders`-এ insert করে, তাই সেগুলো লাইনে দাঁড়িয়ে timeout হয়েছে।
            2. `.concurrently()` দিলে Drizzle Kit `CREATE INDEX CONCURRENTLY` emit করে, যেটা write block করে না — কিন্তু PostgreSQL এটা transaction-এর ভেতরে নিষেধ করে, আর Drizzle-এর migrator **একবারের সব pending migration একটা transaction-এ** চালায়। তাই run fail করেছে (SQLSTATE `25001`) আর তার ভেতরের সব কিছু rollback হয়েছে, একই deploy-এর সম্পর্কহীন migration সহ।

            **এখন সামলাও:**
            - Pipeline খুলে দাও: fail করা migration কোথাও apply হয়নি, তাই এর SQL বদলে শুধু একটা comment রাখো ("index out-of-band তৈরি, incident #123 দেখো")। তখন migrator এটাকে record করবে আর বাকি pending migration আবার চলতে পারবে।
            - **যেকোনো transaction-এর বাইরে** হাতে index বানাও (psql বা online-DDL job দিয়ে): `lock_timeout` set করে কম traffic-এর সময় `CREATE INDEX CONCURRENTLY IF NOT EXISTS ...`, আর `pg_stat_progress_create_index` দেখো।
            - ব্যর্থ concurrent চেষ্টা কোনো `INVALID` index রেখে গেছে কি না দেখো (`pg_index.indisvalid = false`), আবার চেষ্টার আগে সেটা drop করো।
            - Drizzle schema-য় index রেখে দাও, যাতে snapshot database-এর সাথে মেলে আর ভবিষ্যতের diff পরিষ্কার থাকে।

            **প্রতিরোধ:**
            - Migration review checklist: বড় table-এ যেকোনো index/constraint concurrent হবে আর migrator transaction-এর বাইরে আলাদা ধাপ হিসেবে যাবে।
            - Non-transactional statement-এর জন্য আলাদা "online DDL" job/runner; বাকি সব কিছুর জন্য সাধারণ `migrate`।
            - Migration চালাও একটা নির্দিষ্ট, observable release step হিসেবে, `lock_timeout`/`statement_timeout` সহ — CI-এর ভেতরে চুপচাপ না, আর ঝুঁকিপূর্ণ পরিবর্তন peak hour-এ না।
            - Production-আকারের কপিতে migration test করে lock-এর সময় মাপো।
        """,
        quick_en=r"""A plain `CREATE INDEX` blocked writes on the 40M-row table until it finished, and `CONCURRENTLY` can't run inside the migrator's single transaction. Unblock by turning that migration into a no-op, build the index concurrently outside a transaction, drop any invalid leftover, and run online DDL as a separate step.""",
        quick_bn=r"""সাধারণ `CREATE INDEX` শেষ না হওয়া পর্যন্ত 40M row-এর table-এ write আটকে রেখেছিল, আর `CONCURRENTLY` migrator-এর single transaction-এর ভেতরে চলতে পারে না। ওই migration-কে no-op বানিয়ে pipeline খুলি, transaction-এর বাইরে concurrently index বানাই, invalid index থাকলে drop করি, আর online DDL আলাদা step হিসেবে চালাই।""",
        ex_en=r"""
            - **Verified behaviour:** with drizzle-kit 0.31 / Drizzle 0.45, `index(...).concurrently()` generates `CREATE INDEX CONCURRENTLY "orders_customer_id_idx" ON "orders" USING btree ("customer_id")`, and running it through `migrate()` fails with `25001`, rolling back the other pending migrations of that run.
            - **Lock details:** a plain `CREATE INDEX` takes a SHARE lock (reads continue, writes block). `CONCURRENTLY` takes a weaker lock and scans twice, so it's slower overall and can fail leaving an INVALID index — that's the price of not blocking writes.
            - **Lock queue amplification:** even a short `ALTER TABLE` waiting behind a long transaction blocks every query that arrives after it. Always set `lock_timeout` for DDL.
            - **Postmortem framing:** blameless — the root cause is a process gap (no review of lock impact, migrations auto-run at peak), not the individual. Action items: checklist, separate online-DDL step, alerting on long lock waits.
            - Also note the FK lesson: `orders.customer_id` likely existed as a foreign key without an index for years — PostgreSQL never creates FK indexes automatically.
        """,
        ex_bn=r"""
            - **যাচাই করা behaviour:** drizzle-kit 0.31 / Drizzle 0.45-এ `index(...).concurrently()` generate করে `CREATE INDEX CONCURRENTLY "orders_customer_id_idx" ON "orders" USING btree ("customer_id")`, আর `migrate()` দিয়ে চালালে `25001` দিয়ে fail করে, ওই run-এর অন্য pending migration-ও rollback হয়।
            - **Lock-এর detail:** সাধারণ `CREATE INDEX` একটা SHARE lock নেয় (read চলে, write block হয়)। `CONCURRENTLY` দুর্বল lock নেয় আর দুবার scan করে, তাই মোটের উপর ধীর আর fail করলে একটা INVALID index রেখে যেতে পারে — write block না করার দাম এটাই।
            - **Lock queue বেড়ে যাওয়া:** লম্বা transaction-এর পেছনে অপেক্ষা করা ছোট একটা `ALTER TABLE`-ও তার পরে আসা প্রতিটা query block করে। DDL-এর জন্য সবসময় `lock_timeout` দাও।
            - **Postmortem-এর ভঙ্গি:** blameless — root cause হলো process-এর ফাঁক (lock-এর প্রভাব review হয়নি, peak-এ migration নিজে থেকে চলেছে), ব্যক্তি না। Action item: checklist, আলাদা online-DDL ধাপ, দীর্ঘ lock wait-এ alert।
            - FK-র শিক্ষাটাও খেয়াল করো: `orders.customer_id` সম্ভবত বছরের পর বছর index ছাড়াই foreign key হিসেবে ছিল — PostgreSQL কখনো নিজে FK index বানায় না।
        """,
        tip_en=r"""Use incident structure: impact → timeline → root causes (two!) → immediate mitigation → prevention. Knowing that Drizzle's migrator wraps a run in one transaction is the detail that explains the second failure — say it clearly.""",
        tip_bn=r"""Incident-এর কাঠামো ব্যবহার করো: impact → timeline → root cause (দুটো!) → তাৎক্ষণিক প্রতিকার → প্রতিরোধ। Drizzle-এর migrator যে একটা run-কে এক transaction-এ মোড়ে, এই detail-টাই দ্বিতীয় failure ব্যাখ্যা করে — স্পষ্ট করে বলো।""",
        mist_en=r"""Assuming every Drizzle-generated migration is safe for large tables; "fixing" by disabling the migrator transaction globally; retrying CONCURRENTLY without dropping the INVALID index; running risky DDL at peak hours.""",
        mist_bn=r"""ধরে নেওয়া যে Drizzle-generated সব migration বড় table-এর জন্য নিরাপদ; migrator-এর transaction globally বন্ধ করে "সমাধান" করা; INVALID index drop না করে আবার CONCURRENTLY চেষ্টা করা; peak hour-এ ঝুঁকিপূর্ণ DDL চালানো।""",
        code=r"""
            -- What drizzle-kit generated (blocks writes on a 40M-row table)
            CREATE INDEX "orders_customer_id_idx" ON "orders" USING btree ("customer_id");

            -- What `.concurrently()` generates — fails inside Drizzle's migrator transaction (SQLSTATE 25001)
            CREATE INDEX CONCURRENTLY "orders_customer_id_idx" ON "orders" USING btree ("customer_id");

            -- Manual, outside any transaction (psql / online-DDL job), during low traffic:
            SET lock_timeout = '5s';
            CREATE INDEX CONCURRENTLY IF NOT EXISTS "orders_customer_id_idx" ON "orders" USING btree ("customer_id");

            -- Watch progress and check for leftovers from failed attempts
            SELECT phase, blocks_done, blocks_total FROM pg_stat_progress_create_index;
            SELECT indexrelid::regclass AS index_name
            FROM pg_index WHERE NOT indisvalid;              -- drop INVALID indexes before retrying
        """,
        lang="sql",
        follow=[
            ("How would you build an 'online DDL' step into your deployment pipeline?", "Deployment pipeline-এ একটা 'online DDL' ধাপ কীভাবে বানাবে?"),
            ("What other DDL operations are dangerous on large PostgreSQL tables?", "বড় PostgreSQL table-এ আর কোন DDL operation বিপজ্জনক?"),
        ],
        related=["drizzle-012", "drizzle-017", "drizzle-026"],
        refs=[PG_CREATEINDEX, D_MIGRATIONS, PG_LOCKING],
    ),
]

if __name__ == "__main__":
    save("drizzle", "b4", QUESTIONS)
