# PostgreSQL batch 4 — pg-025 … pg-032 (hard & extreme)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PG_ALTER_TABLE = ("PostgreSQL docs — ALTER TABLE", "https://www.postgresql.org/docs/current/sql-altertable.html")
PG_CREATE_INDEX = ("PostgreSQL docs — CREATE INDEX (CONCURRENTLY)", "https://www.postgresql.org/docs/current/sql-createindex.html")
PG_LOCKING = ("PostgreSQL docs — Explicit Locking", "https://www.postgresql.org/docs/current/explicit-locking.html")
PG_PITR = ("PostgreSQL docs — Continuous Archiving and PITR", "https://www.postgresql.org/docs/current/continuous-archiving.html")
PG_COMBINEBACKUP = ("PostgreSQL docs — pg_combinebackup", "https://www.postgresql.org/docs/current/app-pgcombinebackup.html")
PG_RECOVERY_CFG = ("PostgreSQL docs — WAL / recovery target settings", "https://www.postgresql.org/docs/current/runtime-config-wal.html")
PG_STREAMING = ("PostgreSQL docs — Log-Shipping Standby Servers", "https://www.postgresql.org/docs/current/warm-standby.html")
PG_LOGICAL = ("PostgreSQL docs — Logical Replication", "https://www.postgresql.org/docs/current/logical-replication.html")
PG_MONITORING = ("PostgreSQL docs — Monitoring Statistics", "https://www.postgresql.org/docs/current/monitoring-stats.html")
PG_MULTICOL = ("PostgreSQL docs — Multicolumn Indexes (skip scan)", "https://www.postgresql.org/docs/current/indexes-multicolumn.html")
PG_RELEASE_18 = ("PostgreSQL 18 release notes", "https://www.postgresql.org/docs/18/release-18.html")
PG_VACUUM = ("PostgreSQL docs — Routine Vacuuming", "https://www.postgresql.org/docs/current/routine-vacuuming.html")
PG_AUTOVAC_CFG = ("PostgreSQL docs — Autovacuum settings", "https://www.postgresql.org/docs/current/runtime-config-autovacuum.html")
PG_PARTITIONING = ("PostgreSQL docs — Table Partitioning", "https://www.postgresql.org/docs/current/ddl-partitioning.html")
PG_STAT_STATEMENTS = ("PostgreSQL docs — pg_stat_statements", "https://www.postgresql.org/docs/current/pgstatstatements.html")
PG_ADMIN_FUNCS = ("PostgreSQL docs — System Administration Functions", "https://www.postgresql.org/docs/current/functions-admin.html")
PG_RLS = ("PostgreSQL docs — Row Security Policies", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html")
PG_SCHEMAS = ("PostgreSQL docs — Schemas", "https://www.postgresql.org/docs/current/ddl-schemas.html")

QUESTIONS = [
    # ------------------------------------------------------------------ pg-025
    Q(
        id="pg-025", sub="Migrations (Zero-Downtime)", diff="hard", type="scenario",
        prio="high", market="both", mins=10,
        tags=["migrations", "zero-downtime", "not-valid", "lock-timeout", "create-index-concurrently"],
        ver="PostgreSQL 18", vs=True, status="stable",
        q_en=r"""You need to add a required `merchant_id` column — with a foreign key to `merchants` and an index — to a 300-million-row `orders` table that serves live traffic. How do you roll this out with zero downtime?""",
        q_bn=r"""Live traffic চলা ৩০ কোটি row-এর `orders` table-এ একটা বাধ্যতামূলক `merchant_id` column যোগ করতে হবে — `merchants`-এর সাথে foreign key আর একটা index-সহ। Zero downtime-এ কীভাবে rollout করবে?""",
        a_en=r"""
            The danger isn't only long table scans; it's **locks**. Most `ALTER TABLE` forms need an `ACCESS EXCLUSIVE` lock. Even if the change itself is instant, the `ALTER` waits behind any long-running query — and every new query queues behind the waiting `ALTER`. That's how a "1 ms migration" takes the site down. So every DDL step runs with `SET lock_timeout = '5s'` and is retried if it times out.

            The rollout (expand → backfill → enforce):
            1. `ADD COLUMN merchant_id bigint` — nullable with no default is metadata-only, so it's instant.
            2. Deploy app code that writes `merchant_id` for new and updated rows.
            3. **Backfill in batches** (e.g. 10k rows per short transaction by id range), throttled while watching replication lag.
            4. `CREATE INDEX CONCURRENTLY` — doesn't block writes; check it isn't left `INVALID`.
            5. Add the foreign key as `NOT VALID` (brief lock, only checks new writes), then `VALIDATE CONSTRAINT`, which scans under a `SHARE UPDATE EXCLUSIVE` lock that doesn't block reads or writes.
            6. For `NOT NULL`: add `CHECK (merchant_id IS NOT NULL) NOT VALID`, validate it, then `SET NOT NULL` — PostgreSQL skips the full scan because the valid check proves there are no NULLs. Drop the helper check. (PG18 can also add a `NOT NULL` constraint directly as `NOT VALID`.)
        """,
        a_bn=r"""
            বিপদ শুধু লম্বা table scan নয়; আসল বিপদ **lock**। বেশিরভাগ `ALTER TABLE`-এর জন্য `ACCESS EXCLUSIVE` lock লাগে। পরিবর্তনটা নিজে instant হলেও `ALTER` যেকোনো লম্বা চলা query-র পেছনে অপেক্ষা করে — আর প্রতিটা নতুন query সেই অপেক্ষমাণ `ALTER`-এর পেছনে লাইনে দাঁড়ায়। এভাবেই "১ ms-এর migration" পুরো site বসিয়ে দেয়। তাই প্রতিটা DDL step `SET lock_timeout = '5s'` দিয়ে চালাই, আর timeout হলে আবার চেষ্টা করি।

            Rollout (expand → backfill → enforce):
            1. `ADD COLUMN merchant_id bigint` — default ছাড়া nullable column শুধু metadata বদলায়, তাই instant।
            2. App code deploy করো যেটা নতুন আর update হওয়া row-এ `merchant_id` লেখে।
            3. **Batch-এ backfill** (যেমন id range ধরে প্রতি ছোট transaction-এ ১০ হাজার row), replication lag দেখে গতি নিয়ন্ত্রণ করে।
            4. `CREATE INDEX CONCURRENTLY` — write block করে না; দেখে নাও এটা `INVALID` হয়ে পড়ে আছে কিনা।
            5. Foreign key প্রথমে `NOT VALID` হিসেবে যোগ করো (অল্প সময়ের lock, শুধু নতুন write check করে), তারপর `VALIDATE CONSTRAINT` — এটা `SHARE UPDATE EXCLUSIVE` lock নিয়ে scan করে, যা read বা write block করে না।
            6. `NOT NULL`-এর জন্য: `CHECK (merchant_id IS NOT NULL) NOT VALID` যোগ করো, validate করো, তারপর `SET NOT NULL` — valid check প্রমাণ করে NULL নেই, তাই PostgreSQL পুরো scan বাদ দেয়। এরপর helper check-টা drop করো। (PG18-এ সরাসরি `NOT NULL` constraint-ও `NOT VALID` হিসেবে যোগ করা যায়।)
        """,
        quick_en=r"""The real danger is `ACCESS EXCLUSIVE` locks queueing behind long queries, so run every DDL step with a short `lock_timeout` and retry. Expand, backfill, enforce: add a nullable column, backfill in batches, `CREATE INDEX CONCURRENTLY`, add the FK and `NOT NULL` check as `NOT VALID`, then `VALIDATE`.""",
        quick_bn=r"""আসল বিপদ হলো long query-র পেছনে `ACCESS EXCLUSIVE` lock-এর queue, তাই প্রতিটা DDL step ছোট `lock_timeout` দিয়ে চালাও আর retry করো। Expand, backfill, enforce: nullable column যোগ করো, batch-এ backfill, `CREATE INDEX CONCURRENTLY`, FK আর `NOT NULL` check `NOT VALID` হিসেবে যোগ করো, তারপর `VALIDATE`।""",
        ex_en=r"""
            - Since PostgreSQL 11, `ADD COLUMN ... DEFAULT <constant>` is also metadata-only; a **volatile** default (e.g. `DEFAULT random()`) or a type change such as `int → bigint` still rewrites the whole table under `ACCESS EXCLUSIVE`. For type changes, use a new column + backfill + swap.
            - Batch backfills keep each transaction short (small lock footprint, less replication lag, autovacuum can keep up). One giant `UPDATE` creates 300M dead tuples and one huge transaction.
            - `CREATE INDEX CONCURRENTLY` can't run inside a transaction block — many migration tools wrap migrations in transactions by default, so disable that for this step.
            - Renames and drops follow **expand/contract**: add the new thing, migrate readers and writers, and remove the old thing in a later release so old app versions still work during the deploy.
            - Test the migration on a production-sized copy and time each step.
        """,
        ex_bn=r"""
            - PostgreSQL 11 থেকে `ADD COLUMN ... DEFAULT <constant>`-ও শুধু metadata বদলায়; কিন্তু **volatile** default (যেমন `DEFAULT random()`) বা `int → bigint`-এর মতো type পরিবর্তন এখনো `ACCESS EXCLUSIVE` lock নিয়ে পুরো table আবার লেখে। Type পরিবর্তনের জন্য নতুন column + backfill + swap ব্যবহার করো।
            - Batch backfill প্রতিটা transaction ছোট রাখে (lock কম, replication lag কম, autovacuum তাল মেলাতে পারে)। একটা বিশাল `UPDATE` ৩০ কোটি dead tuple আর একটা অতিকায় transaction তৈরি করে।
            - `CREATE INDEX CONCURRENTLY` transaction block-এর ভেতরে চলে না — অনেক migration tool default-ভাবে migration-কে transaction-এ মুড়ে দেয়, তাই এই step-এর জন্য সেটা বন্ধ করো।
            - Rename আর drop **expand/contract** মেনে চলে: নতুনটা যোগ করো, reader আর writer-দের সরাও, আর পুরনোটা পরের কোনো release-এ মুছে ফেলো — যাতে deploy চলাকালীন পুরনো app version-ও কাজ করে।
            - Production-আকারের একটা copy-তে migration test করো আর প্রতিটা step-এর সময় মেপে নাও।
        """,
        tip_en=r"""Open with the lock-queue insight — it's the thing most candidates miss. Then walk through the six steps, naming the lock level for `VALIDATE` and the `lock_timeout` safety net.""",
        tip_bn=r"""Lock-queue-এর বোঝাপড়া দিয়ে শুরু করো — বেশিরভাগ candidate এটাই মিস করে। তারপর ছয়টা step বলো, `VALIDATE`-এর lock level আর `lock_timeout` safety net-এর নাম উল্লেখ করে।""",
        mist_en=r"""Running `ALTER TABLE orders ADD COLUMN merchant_id bigint NOT NULL REFERENCES merchants(id)` in one go, backfilling with a single `UPDATE`, or running DDL without `lock_timeout`.""",
        mist_bn=r"""এক ধাক্কায় `ALTER TABLE orders ADD COLUMN merchant_id bigint NOT NULL REFERENCES merchants(id)` চালানো, একটা মাত্র `UPDATE` দিয়ে backfill করা, অথবা `lock_timeout` ছাড়া DDL চালানো।""",
        code=r"""
            SET lock_timeout = '5s';      -- fail fast instead of blocking traffic; retry later

            -- 1. expand: metadata-only change
            ALTER TABLE orders ADD COLUMN merchant_id bigint;

            -- 3. (after the app writes merchant_id) backfill in batches — see the script below

            -- 4. index without blocking writes (must run outside a transaction block)
            CREATE INDEX CONCURRENTLY idx_orders_merchant_id ON orders (merchant_id);

            -- 5. foreign key: add NOT VALID (instant), validate separately (non-blocking scan)
            ALTER TABLE orders ADD CONSTRAINT orders_merchant_fk
              FOREIGN KEY (merchant_id) REFERENCES merchants(id) NOT VALID;
            ALTER TABLE orders VALIDATE CONSTRAINT orders_merchant_fk;

            -- 6. NOT NULL without a long exclusive lock
            ALTER TABLE orders ADD CONSTRAINT orders_merchant_id_nn
              CHECK (merchant_id IS NOT NULL) NOT VALID;
            ALTER TABLE orders VALIDATE CONSTRAINT orders_merchant_id_nn;
            ALTER TABLE orders ALTER COLUMN merchant_id SET NOT NULL;   -- uses the valid CHECK, no scan
            ALTER TABLE orders DROP CONSTRAINT orders_merchant_id_nn;
        """,
        lang="sql",
        extra=[dict(lang="javascript", label_en="Batched backfill (each batch is its own short transaction)",
                    label_bn="Batch-এ backfill (প্রতিটা batch আলাদা ছোট transaction)", src=r"""
            const BATCH = 10_000;
            const { rows } = await pool.query('SELECT max(id) AS max_id FROM orders');
            const maxId = Number(rows[0].max_id);

            for (let from = 0; from < maxId; from += BATCH) {
              await pool.query(
                `UPDATE orders o
                    SET merchant_id = s.merchant_id
                   FROM stores s
                  WHERE s.id = o.store_id
                    AND o.id > $1 AND o.id <= $1 + ${BATCH}
                    AND o.merchant_id IS NULL`,
                [from],
              );
              await new Promise((r) => setTimeout(r, 100)); // let replicas and autovacuum keep up
            }
        """)],
        follow=[
            ("How would you change a column from `int` to `bigint` on a huge table without downtime?", "বিশাল একটা table-এ downtime ছাড়া একটা column `int` থেকে `bigint`-এ কীভাবে বদলাবে?"),
            ("Why can a fast `ALTER TABLE` still cause an outage?", "দ্রুত চলা একটা `ALTER TABLE`-ও কেন outage ঘটাতে পারে?"),
        ],
        related=["pg-014", "pg-004", "pg-029"],
        refs=[PG_ALTER_TABLE, PG_CREATE_INDEX, PG_LOCKING],
    ),
    # ------------------------------------------------------------------ pg-026
    Q(
        id="pg-026", sub="Backup & Recovery (PITR)", diff="hard", type="scenario",
        prio="high", market="both", mins=10,
        tags=["pitr", "wal-archiving", "incremental-backup", "disaster-recovery", "pg_combinebackup"],
        ver="PostgreSQL 18 (incremental backup since 17)", vs=True, status="stable",
        q_en=r"""At 14:32 (Dhaka time) a developer accidentally ran `DELETE FROM orders;` on production. It's now 15:10 and the application has kept writing other data in the meantime. You have nightly base backups (`pg_basebackup`) and continuous WAL archiving. How do you recover the lost orders with minimal data loss?""",
        q_bn=r"""দুপুর ১৪:৩২-এ (ঢাকা সময়) একজন developer ভুল করে production-এ `DELETE FROM orders;` চালিয়ে ফেলেছে। এখন ১৫:১০, আর এর মধ্যে application অন্য data লিখেই চলেছে। তোমার কাছে প্রতি রাতের base backup (`pg_basebackup`) আর continuous WAL archiving আছে। সবচেয়ে কম data হারিয়ে হারানো order-গুলো কীভাবে ফেরত আনবে?""",
        a_en=r"""
            **Don't restore over production.** Rolling the whole cluster back to 14:31 would throw away 38 minutes of valid writes in every other table. Instead:

            1. **Pin down the moment.** Use app/audit logs, or `pg_waldump` on the archived WAL, to find the time — ideally the transaction ID — of the `DELETE`.
            2. **Restore the last base backup taken before 14:32 onto a separate server.** Set `restore_command` to fetch archived WAL, set a recovery target just before the delete (`recovery_target_time`, or better `recovery_target_xid` with `recovery_target_inclusive = false`), set `recovery_target_action = 'pause'`, create `recovery.signal`, and start it.
            3. **Verify while paused:** check that `orders` looks complete. If the target was too early or late, adjust it and restart recovery from the backup.
            4. **Copy the rows back:** dump just `orders` from the recovered instance (`pg_dump -t orders --data-only`) or connect it with `postgres_fdw`, and insert the missing rows into production (`INSERT ... SELECT ... WHERE NOT EXISTS`). New orders created after 14:32 stay untouched.
            5. **Post-mortem and prevention:** least privilege (people shouldn't have ad-hoc write access to production), mandatory review for manual SQL, soft deletes for critical data, a **delayed replica** (`recovery_min_apply_delay = '1h'`) for fast recovery, and regular restore drills to prove your RPO/RTO.
        """,
        a_bn=r"""
            **Production-এর উপর restore কোরো না।** পুরো cluster ১৪:৩১-এ ফিরিয়ে নিলে বাকি সব table-এর ৩৮ মিনিটের সঠিক write হারিয়ে যাবে। বরং:

            1. **মুহূর্তটা নিশ্চিত করো।** App/audit log, অথবা archived WAL-এ `pg_waldump` চালিয়ে `DELETE`-এর সময় — আদর্শভাবে transaction ID — বের করো।
            2. **১৪:৩২-এর আগের শেষ base backup একটা আলাদা server-এ restore করো।** Archived WAL আনার জন্য `restore_command` দাও, delete-এর ঠিক আগে recovery target দাও (`recovery_target_time`, অথবা আরও ভালো `recovery_target_inclusive = false`-সহ `recovery_target_xid`), `recovery_target_action = 'pause'` দাও, `recovery.signal` তৈরি করো, তারপর start করো।
            3. **Pause অবস্থায় যাচাই করো:** `orders` সম্পূর্ণ আছে কিনা দেখো। Target বেশি আগে বা পরে হলে বদলে আবার backup থেকে recovery শুরু করো।
            4. **Row-গুলো ফেরত কপি করো:** recovered instance থেকে শুধু `orders` dump করো (`pg_dump -t orders --data-only`) বা `postgres_fdw` দিয়ে যুক্ত করো, আর production-এ হারানো row-গুলো insert করো (`INSERT ... SELECT ... WHERE NOT EXISTS`)। ১৪:৩২-এর পরে তৈরি নতুন order অক্ষত থাকে।
            5. **Post-mortem আর প্রতিরোধ:** least privilege (মানুষের production-এ ad-hoc write access থাকা উচিত না), manual SQL-এর জন্য বাধ্যতামূলক review, গুরুত্বপূর্ণ data-র জন্য soft delete, দ্রুত recovery-র জন্য একটা **delayed replica** (`recovery_min_apply_delay = '1h'`), আর RPO/RTO প্রমাণ করতে নিয়মিত restore drill।
        """,
        quick_en=r"""Don't roll production back, because that loses 38 minutes of other writes. Restore the last base backup on a separate server, replay WAL to just before the `DELETE` (ideally `recovery_target_xid`), pause and verify, then copy the missing orders back into production.""",
        quick_bn=r"""Production-কে পিছিয়ে নিয়ো না, তাতে অন্য table-এর 38 মিনিটের write হারিয়ে যাবে। আলাদা server-এ শেষ base backup restore করো, `DELETE`-এর ঠিক আগ পর্যন্ত WAL replay করো (সম্ভব হলে `recovery_target_xid` দিয়ে), pause করে যাচাই করো, তারপর হারানো order-গুলো production-এ ফেরত copy করো।""",
        ex_en=r"""
            - **Why `pg_dump` alone fails here:** last night's dump would lose every order between the dump and 14:32. PITR replays WAL up to any moment, so the only loss is what you choose to exclude.
            - The recovery target must be later than the end of the base backup; you can't stop in the middle of a backup.
            - **Incremental backups (PostgreSQL 17+):** with `summarize_wal = on`, `pg_basebackup --incremental=<previous backup_manifest>` copies only changed blocks. To restore, `pg_combinebackup` merges the full backup and every incremental in the chain into a synthetic full backup, then you replay WAL as usual. This cuts backup time and storage for large databases; you still need the whole chain.
            - In practice, tools such as pgBackRest, Barman, or WAL-G (or your cloud provider's PITR) manage base backups, WAL archives, retention, and verification for you.
            - Also restore sequences and check foreign-key dependants (e.g. `order_items` rows may have been deleted by `ON DELETE CASCADE` — recover them too).
        """,
        ex_bn=r"""
            - **শুধু `pg_dump` দিয়ে কেন হবে না:** গত রাতের dump থেকে restore করলে dump-এর পর থেকে ১৪:৩২ পর্যন্ত সব order হারাবে। PITR যেকোনো মুহূর্ত পর্যন্ত WAL replay করে, তাই শুধু যেটুকু তুমি বাদ দিতে চাও সেটুকুই হারায়।
            - Recovery target-কে base backup শেষ হওয়ার পরের সময় হতে হবে; backup চলার মাঝখানে থামা যায় না।
            - **Incremental backup (PostgreSQL 17+):** `summarize_wal = on` থাকলে `pg_basebackup --incremental=<আগের backup_manifest>` শুধু বদলানো block কপি করে। Restore করতে `pg_combinebackup` full backup আর chain-এর সব incremental মিলিয়ে একটা synthetic full backup বানায়, তারপর যথারীতি WAL replay করো। বড় database-এ backup-এর সময় আর storage কমে; তবে পুরো chain-টাই লাগে।
            - বাস্তবে pgBackRest, Barman বা WAL-G (অথবা cloud provider-এর PITR) base backup, WAL archive, retention আর verification সামলায়।
            - Sequence-ও restore করো আর foreign-key-নির্ভর table দেখো (যেমন `ON DELETE CASCADE`-এর কারণে `order_items`-এর row-ও মুছে যেতে পারে — সেগুলোও উদ্ধার করো)।
        """,
        tip_en=r"""The key sentence is "restore to a separate instance, then copy the rows back" — it shows you protect the other 38 minutes of data. Mention RPO/RTO and restore drills to sound like someone who has run production.""",
        tip_bn=r"""মূল বাক্যটা হলো "আলাদা instance-এ restore করে তারপর row-গুলো ফেরত কপি করব" — এতে বোঝা যায় তুমি বাকি ৩৮ মিনিটের data রক্ষা করছ। RPO/RTO আর restore drill-এর কথা বললে মনে হবে তুমি সত্যিই production চালিয়েছ।""",
        mist_en=r"""Restoring the whole production cluster to 14:31, or restoring last night's `pg_dump` and losing the day's orders.""",
        mist_bn=r"""পুরো production cluster ১৪:৩১-এ ফিরিয়ে নেওয়া, অথবা গত রাতের `pg_dump` restore করে সারা দিনের order হারানো।""",
        code=r"""
            # 1. restore the last base backup taken before 14:32 onto a NEW instance
            #    (PG17+ incremental chain: pg_combinebackup full/ incr1/ incr2/ -o /restore/data)
            mkdir -p /restore/data
            tar -xzf /backups/base_2026-10-12_0200/base.tar.gz -C /restore/data

            # 2. recovery settings for the restored instance
            cat >> /restore/data/postgresql.conf <<'CONF'
            restore_command        = 'cp /wal_archive/%f %p'
            recovery_target_time   = '2026-10-12 14:31:30+06'
            recovery_target_action = 'pause'
            CONF
            touch /restore/data/recovery.signal
            pg_ctl -D /restore/data -o "-p 5433" start

            # 3. inspect while paused, then export just the lost table
            psql -p 5433 -d shop -c "SELECT count(*), max(created_at) FROM orders"
            pg_dump -p 5433 -d shop -t orders --data-only -Fc -f orders_recovered.dump
        """,
        lang="bash",
        follow=[
            ("What are RPO and RTO, and how does your backup strategy map to them?", "RPO আর RTO কী, আর তোমার backup strategy কীভাবে এগুলোর সাথে মেলে?"),
            ("How does a delayed replica help in this incident?", "এই ধরনের incident-এ delayed replica কীভাবে সাহায্য করে?"),
        ],
        related=["pg-011", "pg-027"],
        refs=[PG_PITR, PG_COMBINEBACKUP, PG_RECOVERY_CFG],
    ),
    # ------------------------------------------------------------------ pg-027
    Q(
        id="pg-027", sub="Replication", diff="hard", type="comparison",
        prio="high", market="both", mins=8,
        tags=["streaming-replication", "logical-replication", "read-replicas", "replication-lag", "read-your-writes"],
        ver="PostgreSQL 18", vs=False, status="stable",
        q_en=r"""Compare physical streaming replication and logical replication in PostgreSQL. When would you use each, and how do you deal with replication lag when you send reads to replicas?""",
        q_bn=r"""PostgreSQL-এ physical streaming replication আর logical replication-এর তুলনা করো। কোনটা কখন ব্যবহার করবে, আর replica-তে read পাঠালে replication lag কীভাবে সামলাবে?""",
        a_en=r"""
            **Physical streaming replication** ships the WAL byte stream. The standby is a block-for-block copy of the **entire cluster**, read-only (hot standby), and must run the same major version. Use it for high availability/failover and for scaling reads.

            **Logical replication** decodes WAL into row-level changes and publishes chosen tables (`PUBLICATION` / `SUBSCRIPTION`). The subscriber is a normal, writable database and can run a **different major version**. Use it for near-zero-downtime major upgrades, replicating a subset of tables, consolidating data, or change-data-capture into other systems.

            **Lag:** replicas are usually asynchronous, so a user who just updated their profile may read stale data from a replica. Fixes: route a user's reads to the primary for a short window after they write; or wait until the replica has replayed the write's LSN; or use synchronous replication for the data that needs it (at a write-latency cost). And monitor lag via `pg_stat_replication`.
        """,
        a_bn=r"""
            **Physical streaming replication** WAL-এর byte stream পাঠায়। Standby হলো **পুরো cluster**-এর block-by-block copy, read-only (hot standby), আর একই major version-এ চলতে হয়। High availability/failover আর read scale করার জন্য এটা ব্যবহার করো।

            **Logical replication** WAL-কে row-level পরিবর্তনে decode করে আর বাছাই করা table publish করে (`PUBLICATION` / `SUBSCRIPTION`)। Subscriber একটা সাধারণ, writable database, আর **ভিন্ন major version**-এ চলতে পারে। প্রায় zero-downtime major upgrade, কিছু table-এর replication, data একত্র করা, বা অন্য system-এ change-data-capture-এর জন্য এটা ব্যবহার করো।

            **Lag:** replica সাধারণত asynchronous, তাই যে user এইমাত্র profile update করেছে সে replica থেকে পুরনো data পড়তে পারে। সমাধান: write-এর পর কিছুক্ষণ সেই user-এর read primary-তে পাঠাও; অথবা replica write-এর LSN replay না করা পর্যন্ত অপেক্ষা করো; অথবা যে data-তে দরকার সেখানে synchronous replication ব্যবহার করো (write latency-র বিনিময়ে)। আর `pg_stat_replication` দিয়ে lag monitor করো।
        """,
        quick_en=r"""Physical streaming replication copies the whole cluster block for block, read-only and same major version, for HA and read scaling. Logical replication publishes chosen tables to a writable subscriber that can run another major version, for upgrades and CDC. Replicas lag, so read-your-writes needs routing to the primary.""",
        quick_bn=r"""Physical streaming replication পুরো cluster block ধরে ধরে copy করে, read-only আর একই major version, HA আর read scaling-এর জন্য। Logical replication বাছাই করা table একটা writable subscriber-এ পাঠায়, যেটা অন্য major version-এও চলতে পারে, upgrade আর CDC-র জন্য। Replica পিছিয়ে থাকে, তাই নিজের write পড়তে হলে primary-তে route করো।""",
        ex_en=r"""
            - **Logical replication limits:** DDL isn't replicated (apply schema changes on both sides), sequence values aren't replicated as of PG18 (bump them before cutover), and `UPDATE`/`DELETE` need a replica identity — usually the primary key. A conflicting row on the subscriber (e.g. a duplicate key) stops replication until fixed.
            - **Replication slots** stop the primary from removing WAL a consumer still needs. An abandoned slot can fill the primary's disk — cap it with `max_slot_wal_keep_size`; PG18 adds `idle_replication_slot_timeout` to invalidate inactive slots.
            - **Long queries on standbys** can be cancelled when replay needs to remove rows they still see. `hot_standby_feedback = on` avoids that but lets standby queries hold back vacuum (bloat) on the primary.
            - **Synchronous replication** (`synchronous_standby_names`) gives zero data loss on failover but each commit waits for the standby; usually used with at least two standbys.
            - Failover needs tooling (Patroni, or a managed service like RDS/Aurora Multi-AZ) — PostgreSQL itself doesn't promote automatically.
        """,
        ex_bn=r"""
            - **Logical replication-এর সীমাবদ্ধতা:** DDL replicate হয় না (schema পরিবর্তন দুই দিকেই apply করতে হয়), PG18 পর্যন্ত sequence-এর value replicate হয় না (cutover-এর আগে বাড়িয়ে নাও), আর `UPDATE`/`DELETE`-এর জন্য replica identity লাগে — সাধারণত primary key। Subscriber-এ conflict হলে (যেমন duplicate key) ঠিক না করা পর্যন্ত replication থেমে থাকে।
            - **Replication slot** primary-কে সেই WAL মুছতে দেয় না যেটা কোনো consumer-এর এখনো দরকার। পরিত্যক্ত slot primary-র disk ভরিয়ে ফেলতে পারে — `max_slot_wal_keep_size` দিয়ে সীমা দাও; PG18-এ inactive slot invalidate করার জন্য `idle_replication_slot_timeout` এসেছে।
            - Replay যখন এমন row সরাতে চায় যেটা standby-র কোনো query এখনো দেখছে, তখন **standby-র লম্বা query** cancel হয়ে যেতে পারে। `hot_standby_feedback = on` এটা এড়ায়, কিন্তু তখন standby-র query primary-তে vacuum আটকে রাখতে পারে (bloat)।
            - **Synchronous replication** (`synchronous_standby_names`) failover-এ শূন্য data loss দেয়, কিন্তু প্রতিটা commit standby-র জন্য অপেক্ষা করে; সাধারণত অন্তত দুটো standby-সহ ব্যবহার হয়।
            - Failover-এর জন্য tooling লাগে (Patroni, বা RDS/Aurora Multi-AZ-এর মতো managed service) — PostgreSQL নিজে automatic promote করে না।
        """,
        tip_en=r"""Use a two-column mental table: what is copied (bytes vs rows), scope (cluster vs tables), versions (same vs different), writable or not. Then spend real time on read-your-writes — that's the practical part interviewers probe.""",
        tip_bn=r"""মাথায় একটা দুই-কলামের table রাখো: কী কপি হয় (byte বনাম row), পরিধি (cluster বনাম table), version (একই বনাম ভিন্ন), writable কিনা। তারপর read-your-writes-এ ভালো করে সময় দাও — interviewer এই practical অংশটাই খোঁচায়।""",
        mist_en=r"""Assuming replicas are always up to date, or expecting logical replication to copy schema changes and sequences automatically.""",
        mist_bn=r"""ধরে নেওয়া যে replica সবসময় up to date, অথবা আশা করা যে logical replication schema পরিবর্তন আর sequence নিজে থেকেই কপি করবে।""",
        code=r"""
            -- on the primary: how far behind is each standby?
            SELECT application_name, state, sync_state, write_lag, flush_lag, replay_lag
            FROM pg_stat_replication;

            -- on a standby: how stale is this replica?
            SELECT now() - pg_last_xact_replay_timestamp() AS replay_delay;

            -- logical replication: publisher ...
            CREATE PUBLICATION shop_pub FOR TABLE orders, order_items;

            -- ... and subscriber (may run a newer major version)
            CREATE SUBSCRIPTION shop_sub
              CONNECTION 'host=old-primary dbname=shop user=replicator'
              PUBLICATION shop_pub;
        """,
        lang="sql",
        follow=[
            ("How would you upgrade from PostgreSQL 16 to 18 with only seconds of downtime?", "মাত্র কয়েক সেকেন্ডের downtime-এ PostgreSQL 16 থেকে 18-এ কীভাবে upgrade করবে?"),
            ("What is a replication slot, and what can go wrong with it?", "Replication slot কী, আর এতে কী ভুল হতে পারে?"),
        ],
        related=["pg-026", "pg-021"],
        refs=[PG_STREAMING, PG_LOGICAL, PG_MONITORING],
    ),
    # ------------------------------------------------------------------ pg-028
    Q(
        id="pg-028", sub="PostgreSQL 18: B-tree Skip Scan", diff="hard", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["skip-scan", "multicolumn-index", "b-tree", "postgresql-18"],
        ver="PostgreSQL 18", vs=True, status="version-specific",
        q_en=r"""On PostgreSQL 18 there is an index `ON events (tenant_id, created_at)`. The table has 400 million rows but only **12 distinct `tenant_id` values**. A dashboard runs `SELECT count(*) FROM events WHERE created_at >= now() - interval '1 hour';` with no tenant filter. Which statement is most accurate?""",
        q_bn=r"""PostgreSQL 18-এ `ON events (tenant_id, created_at)` index আছে। Table-এ ৪০ কোটি row, কিন্তু **মাত্র ১২টা distinct `tenant_id`**। একটা dashboard tenant filter ছাড়াই `SELECT count(*) FROM events WHERE created_at >= now() - interval '1 hour';` চালায়। কোন কথাটা সবচেয়ে সঠিক?""",
        options=[
            ("The index can't help at all, because the leading column `tenant_id` isn't in the `WHERE` clause; a separate index on `created_at` is the only option.",
             "Index কোনো কাজেই আসবে না, কারণ প্রথম column `tenant_id` `WHERE`-এ নেই; `created_at`-এ আলাদা index বানানোই একমাত্র উপায়।"),
            ("PG18's B-tree skip scan can use the index by doing one `created_at` range search per distinct `tenant_id` value, so the planner may choose it without a new index.",
             "PG18-এর B-tree skip scan প্রতিটা distinct `tenant_id`-এর জন্য একটা করে `created_at` range search করে index ব্যবহার করতে পারে, তাই নতুন index ছাড়াই planner এটা বেছে নিতে পারে।"),
            ("The planner rewrites the query into 12 `UNION ALL` branches, which appear as an `Append` node in `EXPLAIN`.",
             "Planner query-টাকে ১২টা `UNION ALL` branch-এ রূপান্তর করে, যেটা `EXPLAIN`-এ একটা `Append` node হিসেবে দেখা যায়।"),
            ("Skip scan only works when the leading column has many distinct values, so it won't apply here.",
             "Skip scan কেবল তখনই কাজ করে যখন প্রথম column-এ অনেক distinct value থাকে, তাই এখানে প্রযোজ্য নয়।"),
        ],
        correct=1,
        a_en=r"""**Skip scan** (new in PostgreSQL 18) lets a multicolumn B-tree be used even without a condition on the leading column. Internally it repeats the search for each distinct `tenant_id` (`tenant_id = N AND created_at >= ...`), skipping the rest of the index. With only 12 tenants that's about 12 small descents, so the planner may well pick it.""",
        a_bn=r"""**Skip scan** (PostgreSQL 18-এ নতুন) প্রথম column-এ কোনো condition না থাকলেও multicolumn B-tree ব্যবহার করতে দেয়। ভেতরে ভেতরে এটা প্রতিটা distinct `tenant_id`-এর জন্য search আবার চালায় (`tenant_id = N AND created_at >= ...`), index-এর বাকি অংশ লাফিয়ে পার হয়ে। মাত্র ১২টা tenant হলে সেটা প্রায় ১২টা ছোট descent, তাই planner এটা বেছে নিতেই পারে।""",
        quick_en=r"""PG18's B-tree skip scan can use the `(tenant_id, created_at)` index without a `tenant_id` filter by doing one `created_at` range search per distinct tenant. With only 12 tenants that's about 12 small descents, so the planner may pick it without a new index.""",
        quick_bn=r"""PG18-এর B-tree skip scan `tenant_id` filter ছাড়াও `(tenant_id, created_at)` index ব্যবহার করতে পারে, প্রতিটা আলাদা tenant-এর জন্য একবার করে `created_at` range search করে। মাত্র 12টা tenant হলে এটা প্রায় 12টা ছোট search, তাই নতুন index ছাড়াই planner এটা বেছে নিতে পারে।""",
        ex_en=r"""
            - Option A was essentially the rule **before PG18** (at best a full index scan), which is why it's tempting. "Leading column first" is still the right default when designing indexes.
            - Option D is backwards: skip scan pays off only when the skipped column has **few** distinct values. With millions of distinct leading values, the planner prefers a sequential scan or a different index.
            - Option C is wrong: skip scan happens inside a single index scan node. In `EXPLAIN ANALYZE` (PG18) you'll see one `Index Scan`/`Index Only Scan`, and its `Index Searches:` count reveals the repeated descents.
            - It's a planner decision based on statistics — confirm with `EXPLAIN`. For a hot dashboard query, a dedicated `(created_at)` index (or a BRIN index on an append-only table, or a rollup table) may still be the better long-term design.
        """,
        ex_bn=r"""
            - Option A মূলত **PG18-এর আগের** নিয়ম ছিল (বড়জোর একটা full index scan) — এজন্যই এটা লোভনীয়। Index design-এর সময় "প্রথম column আগে" এখনো সঠিক default।
            - Option D উল্টো: skip scan তখনই লাভজনক যখন skip করা column-এ **কম** distinct value থাকে। প্রথম column-এ লাখ লাখ distinct value থাকলে planner sequential scan বা অন্য index বেছে নেয়।
            - Option C ভুল: skip scan একটা index scan node-এর ভেতরেই ঘটে। `EXPLAIN ANALYZE`-এ (PG18) একটাই `Index Scan`/`Index Only Scan` দেখবে, আর এর `Index Searches:` সংখ্যা বারবার descent হওয়ার কথা জানিয়ে দেয়।
            - এটা statistics-নির্ভর planner-এর সিদ্ধান্ত — `EXPLAIN` দিয়ে নিশ্চিত হও। ঘনঘন চলা dashboard query-র জন্য আলাদা `(created_at)` index (বা append-only table-এ BRIN index, বা rollup table) দীর্ঘমেয়াদে এখনো ভালো design হতে পারে।
        """,
        tip_en=r"""Explain the mechanism ("one descent per distinct leading value") and the condition (low cardinality). Saying you'd still verify with `EXPLAIN` and consider a dedicated index shows judgement, not just release-note recall.""",
        tip_bn=r"""Mechanism ("প্রথম column-এর প্রতিটা distinct value-র জন্য একটা descent") আর শর্ত (কম cardinality) ব্যাখ্যা করো। বলো যে তবুও `EXPLAIN` দিয়ে যাচাই করবে আর আলাদা index বিবেচনা করবে — এতে release note মুখস্থের বদলে বিচারবুদ্ধি দেখা যায়।""",
        related=["pg-013", "pg-005"],
        refs=[PG_MULTICOL, PG_RELEASE_18],
    ),
    # ------------------------------------------------------------------ pg-029
    Q(
        id="pg-029", sub="VACUUM, Bloat & Wraparound", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["vacuum", "autovacuum", "bloat", "xid-wraparound", "fillfactor"],
        ver="PostgreSQL 18", vs=True, status="stable",
        q_en=r"""An `orders` table with heavy `UPDATE` traffic has grown from 8 GB to 60 GB although its row count barely changed. Queries are getting slower, and monitoring warns that `age(datfrozenxid)` keeps rising. What's going on, and how do you fix it?""",
        q_bn=r"""ভারী `UPDATE` traffic-ওয়ালা একটা `orders` table 8 GB থেকে 60 GB হয়ে গেছে, অথচ row সংখ্যা প্রায় একই। Query ধীর হচ্ছে, আর monitoring সতর্ক করছে যে `age(datfrozenxid)` বেড়েই চলেছে। কী ঘটছে, আর কীভাবে ঠিক করবে?""",
        a_en=r"""
            It's MVCC **bloat**: every `UPDATE` leaves a dead row version, and VACUUM isn't reclaiming them fast enough. The rising XID age is the more dangerous symptom — VACUUM also isn't **freezing** old rows.

            Two usual causes:
            1. **Something holds back the "xmin horizon"**, so VACUUM may not remove dead rows that some snapshot could still see: a long-running or `idle in transaction` session, an abandoned replication slot, a forgotten prepared transaction, or a standby with `hot_standby_feedback`. This is the first thing I check, because no amount of vacuum tuning helps until it's gone.
            2. **Autovacuum can't keep up**: by default it waits until ~20% of a table is dead, which on a big table is a lot, and it's throttled by cost limits.

            Fix: find and remove the blocker; tune autovacuum per table (lower `autovacuum_vacuum_scale_factor`, raise the cost limit); run a manual `VACUUM (VERBOSE)`; and reclaim disk with `pg_repack` (online) or `VACUUM FULL` (exclusive lock — a maintenance window). Lower `fillfactor` so more updates are HOT.
        """,
        a_bn=r"""
            এটা MVCC **bloat**: প্রতিটা `UPDATE` একটা dead row version রেখে যায়, আর VACUUM যথেষ্ট দ্রুত সেগুলো ফেরত নিতে পারছে না। বেড়ে চলা XID age আরও বিপজ্জনক লক্ষণ — VACUUM পুরনো row-গুলো **freeze**-ও করতে পারছে না।

            সাধারণত দুটো কারণ:
            1. **কিছু একটা "xmin horizon" আটকে রেখেছে**, ফলে কোনো snapshot এখনো দেখতে পারে এমন dead row VACUUM সরাতে পারে না: লম্বা চলা বা `idle in transaction` session, পরিত্যক্ত replication slot, ভুলে যাওয়া prepared transaction, বা `hot_standby_feedback`-ওয়ালা standby। আমি এটাই প্রথমে দেখি, কারণ এটা না সরানো পর্যন্ত vacuum tuning কোনো কাজে আসে না।
            2. **Autovacuum তাল মেলাতে পারছে না**: default-ভাবে এটা table-এর প্রায় 20% dead না হওয়া পর্যন্ত অপেক্ষা করে — বড় table-এ সেটা অনেক — আর cost limit দিয়ে এর গতিও সীমিত।

            সমাধান: blocker খুঁজে সরাও; table অনুযায়ী autovacuum tune করো (`autovacuum_vacuum_scale_factor` কমাও, cost limit বাড়াও); হাতে একবার `VACUUM (VERBOSE)` চালাও; আর disk ফেরত পেতে `pg_repack` (online) বা `VACUUM FULL` (exclusive lock — maintenance window লাগে) ব্যবহার করো। `fillfactor` কমাও যাতে বেশি update HOT হয়।
        """,
        quick_en=r"""It's MVCC bloat plus missed freezing: dead row versions aren't being vacuumed. First find what holds back the xmin horizon (long or idle-in-transaction sessions, abandoned replication slots), then tune autovacuum per table and reclaim space with `pg_repack` or `VACUUM FULL`.""",
        quick_bn=r"""এটা MVCC bloat, সাথে freezing-ও হচ্ছে না: dead row version-গুলো vacuum হচ্ছে না। আগে খুঁজে বের করো xmin horizon কে আটকে রাখছে (long বা idle-in-transaction session, পরিত্যক্ত replication slot), তারপর table অনুযায়ী autovacuum tune করো আর `pg_repack` বা `VACUUM FULL` দিয়ে জায়গা ফেরত নাও।""",
        ex_en=r"""
            - **Plain `VACUUM`** marks dead space reusable but rarely shrinks the file; **`VACUUM FULL`** rewrites the table compactly but holds an `ACCESS EXCLUSIVE` lock for the whole run. `pg_repack` (an extension) rebuilds online with only brief locks.
            - **Wraparound:** transaction IDs are 32-bit and compared modulo 2³², so rows must be frozen before they look like they're "from the future". Autovacuum launches aggressive anti-wraparound vacuums when a table's XID age passes `autovacuum_freeze_max_age` (200 million by default) — don't cancel them. If freezing keeps failing, PostgreSQL eventually stops assigning new transaction IDs to protect data: an outage for all writes.
            - **HOT updates** (heap-only tuples) avoid index updates when no indexed column changes and the page has free space — `fillfactor = 85–90` leaves that space; avoid indexing frequently updated columns.
            - PG18 adds `autovacuum_vacuum_max_threshold`, a cap on the dead-tuple threshold so huge tables don't wait for a percentage of billions of rows. Set `idle_in_transaction_session_timeout` (and PG17's `transaction_timeout`) so sessions can't hold the horizon forever.
            - Monitor: `n_dead_tup`, `last_autovacuum`, oldest `backend_xmin`, slot status, and `age(datfrozenxid)` with alerts.
        """,
        ex_bn=r"""
            - **সাধারণ `VACUUM`** dead space আবার ব্যবহারযোগ্য করে, কিন্তু file খুব কমই ছোট করে; **`VACUUM FULL`** table-টা গুছিয়ে নতুন করে লেখে, কিন্তু পুরো সময় `ACCESS EXCLUSIVE` lock ধরে রাখে। `pg_repack` (একটা extension) অল্প সময়ের lock নিয়ে online-এ rebuild করে।
            - **Wraparound:** transaction ID 32-bit আর 2³² modulo-তে তুলনা হয়, তাই row-গুলোকে "ভবিষ্যতের" মনে হওয়ার আগেই freeze করতে হয়। কোনো table-এর XID age `autovacuum_freeze_max_age` (default ২০ কোটি) পার হলে autovacuum aggressive anti-wraparound vacuum চালায় — এগুলো cancel কোরো না। Freeze বারবার ব্যর্থ হলে data রক্ষা করতে PostgreSQL শেষ পর্যন্ত নতুন transaction ID দেওয়া বন্ধ করে দেয়: সব write-এর জন্য outage।
            - **HOT update** (heap-only tuple) index update এড়ায়, যদি কোনো indexed column না বদলায় আর page-এ ফাঁকা জায়গা থাকে — `fillfactor = 85–90` সেই জায়গা রাখে; ঘনঘন update হওয়া column-এ index দেওয়া এড়িয়ে চলো।
            - PG18-এ `autovacuum_vacuum_max_threshold` এসেছে — dead-tuple threshold-এর একটা উপরের সীমা, যাতে বিশাল table-কে শত কোটি row-এর শতাংশের জন্য অপেক্ষা করতে না হয়। `idle_in_transaction_session_timeout` (আর PG17-এর `transaction_timeout`) দাও, যাতে কোনো session চিরকাল horizon আটকে রাখতে না পারে।
            - Monitor করো: `n_dead_tup`, `last_autovacuum`, সবচেয়ে পুরনো `backend_xmin`, slot-এর অবস্থা, আর alert-সহ `age(datfrozenxid)`।
        """,
        tip_en=r"""Separate the two problems (bloat vs wraparound), then say "first I look for whatever is holding back the xmin horizon". That single diagnostic step is what experienced DBAs check first.""",
        tip_bn=r"""দুটো সমস্যা আলাদা করো (bloat বনাম wraparound), তারপর বলো "প্রথমে আমি দেখি কে xmin horizon আটকে রেখেছে"। অভিজ্ঞ DBA-রা ঠিক এই diagnostic step-টাই আগে দেখে।""",
        mist_en=r"""Running `VACUUM FULL` on a busy production table during peak hours, disabling autovacuum because it "uses I/O", or cancelling anti-wraparound vacuums.""",
        mist_bn=r"""ব্যস্ত সময়ে busy production table-এ `VACUUM FULL` চালানো, "I/O খায়" বলে autovacuum বন্ধ করা, অথবা anti-wraparound vacuum cancel করা।""",
        code=r"""
            -- 1. who is holding back cleanup? (oldest snapshots first)
            SELECT pid, state, now() - xact_start AS xact_age, backend_xmin, left(query, 60) AS query
            FROM pg_stat_activity
            WHERE backend_xmin IS NOT NULL
            ORDER BY age(backend_xmin) DESC
            LIMIT 5;

            SELECT slot_name, active, xmin, catalog_xmin, wal_status FROM pg_replication_slots;
            SELECT gid, prepared FROM pg_prepared_xacts;

            -- 2. dead tuples and vacuum history
            SELECT relname, n_live_tup, n_dead_tup, last_autovacuum
            FROM pg_stat_user_tables
            ORDER BY n_dead_tup DESC
            LIMIT 10;

            -- 3. wraparound risk
            SELECT datname, age(datfrozenxid) AS xid_age FROM pg_database ORDER BY xid_age DESC;

            -- 4. per-table tuning for a big, hot table
            ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.01,
                                    autovacuum_vacuum_cost_limit   = 2000,
                                    fillfactor                     = 85);
            VACUUM (VERBOSE) orders;
        """,
        lang="sql",
        follow=[
            ("Why doesn't plain `VACUUM` return disk space to the operating system?", "সাধারণ `VACUUM` কেন operating system-কে disk space ফেরত দেয় না?"),
            ("What happens if a database gets close to transaction ID wraparound?", "কোনো database transaction ID wraparound-এর কাছাকাছি চলে গেলে কী ঘটে?"),
        ],
        related=["pg-007", "pg-025", "pg-031"],
        refs=[PG_VACUUM, PG_AUTOVAC_CFG, PG_RELEASE_18],
    ),
    # ------------------------------------------------------------------ pg-030
    Q(
        id="pg-030", sub="Partitioning at Scale", diff="extreme", type="system-design",
        prio="medium", market="international", mins=20,
        tags=["partitioning", "retention", "time-series", "partition-pruning", "rollups"],
        ver="PostgreSQL 18 (identity on partitioned tables since 17)", vs=True, status="stable",
        q_en=r"""Design PostgreSQL storage for an `events` table that receives ~20 million rows per day and keeps 90 days (about 2 billion rows). It serves (a) a user's recent activity feed and (b) dashboards with event counts by type over time ranges. Data older than 90 days must be removed. How would you design it, and what can go wrong?""",
        q_bn=r"""এমন একটা `events` table-এর PostgreSQL storage design করো যেটা দিনে ~২ কোটি row পায় আর ৯০ দিনের data রাখে (প্রায় ২০০ কোটি row)। এটা (a) একজন user-এর সাম্প্রতিক activity feed আর (b) সময়ের range ধরে event type অনুযায়ী count-এর dashboard সার্ভ করে। ৯০ দিনের পুরনো data মুছে ফেলতে হবে। কীভাবে design করবে, আর কী কী ভুল হতে পারে?""",
        a_en=r"""
            This is advanced material; I'd structure it like this.

            **Core decision: declarative range partitioning by `created_at`, one partition per day.**
            - **Retention becomes metadata:** `DETACH PARTITION ... CONCURRENTLY` + `DROP TABLE` removes a day instantly. Deleting 20M rows a day would create huge WAL, 20M dead tuples, and endless vacuum work.
            - **Partition pruning:** queries with a `created_at` range touch only the relevant partitions — both feeds and dashboards naturally filter by time, so every query must include that predicate.
            - **Smaller units of maintenance:** vacuum, index builds, and backups of old data operate per partition.

            **Keys and indexes**
            - Primary/unique keys must include the partition key: `PRIMARY KEY (id, created_at)`. Global uniqueness of `id` alone can't be enforced, so generate ids centrally (identity or `uuidv7()`).
            - Feed: `(user_id, created_at DESC)` B-tree on each partition. Keep the index count low — every index multiplies write cost at 230 inserts/second average (and much higher peaks).

            **Dashboards:** don't aggregate 2 billion raw rows on every page load. Maintain an hourly rollup table (`bucket, event_type, count`) updated by a scheduled job (or incrementally on ingest); dashboards read the rollup. If analytics needs grow, ship events to a columnar/OLAP store.

            **Operations:** create future partitions ahead of time (pg_partman or a cron job) and alert if tomorrow's partition is missing; ingest in batches (`COPY` / multi-row `INSERT`); keep replicas and autovacuum healthy.
        """,
        a_bn=r"""
            এটা advanced বিষয়; আমি এভাবে সাজাব।

            **মূল সিদ্ধান্ত: `created_at` ধরে declarative range partitioning, প্রতিদিনের জন্য একটা partition।**
            - **Retention শুধু metadata-র কাজ হয়ে যায়:** `DETACH PARTITION ... CONCURRENTLY` + `DROP TABLE` এক দিনের data সাথে সাথে সরিয়ে দেয়। দিনে ২ কোটি row `DELETE` করলে বিশাল WAL, ২ কোটি dead tuple আর অন্তহীন vacuum-এর কাজ তৈরি হতো।
            - **Partition pruning:** `created_at` range-সহ query শুধু প্রাসঙ্গিক partition ছোঁয় — feed আর dashboard দুটোই স্বাভাবিকভাবে সময় দিয়ে filter করে, তাই প্রতিটা query-তে ওই predicate থাকতেই হবে।
            - **Maintenance-এর ছোট একক:** vacuum, index build আর পুরনো data-র backup partition ধরে চলে।

            **Key আর index**
            - Primary/unique key-তে partition key থাকতেই হবে: `PRIMARY KEY (id, created_at)`। শুধু `id`-এর global uniqueness enforce করা যায় না, তাই id কেন্দ্রীয়ভাবে তৈরি করো (identity বা `uuidv7()`)।
            - Feed: প্রতিটা partition-এ `(user_id, created_at DESC)` B-tree। Index কম রাখো — গড়ে সেকেন্ডে ২৩০টা insert-এ (আর peak-এ অনেক বেশি) প্রতিটা index write-এর খরচ বাড়ায়।

            **Dashboard:** প্রতিবার page load-এ ২০০ কোটি কাঁচা row aggregate কোরো না। একটা hourly rollup table (`bucket, event_type, count`) রাখো যেটা scheduled job (বা ingest-এর সময় incremental) update করে; dashboard rollup পড়ে। Analytics-এর চাহিদা বাড়লে event-গুলো একটা columnar/OLAP store-এ পাঠাও।

            **Operations:** ভবিষ্যতের partition আগেই তৈরি করো (pg_partman বা cron job) আর কালকের partition না থাকলে alert দাও; batch-এ ingest করো (`COPY` / multi-row `INSERT`); replica আর autovacuum সুস্থ রাখো।
        """,
        quick_en=r"""Range-partition `events` by `created_at`, one partition per day, so retention is a cheap detach-and-drop and time filters prune partitions. Keys must include the partition key, keep indexes few, serve dashboards from an hourly rollup table, and create future partitions ahead of time.""",
        quick_bn=r"""`events`-কে `created_at` দিয়ে দিনে একটা করে range partition করো, তাহলে পুরোনো data সরানো মানে সস্তা detach আর drop, আর time filter দিলে partition pruning হয়। Key-তে partition key রাখতেই হবে, index কম রাখো, dashboard চালাও hourly rollup table থেকে, আর ভবিষ্যতের partition আগে থেকেই বানিয়ে রাখো।""",
        ex_en=r"""
            **What can go wrong**
            - **Missing future partition** → inserts fail ("no partition of relation found for row"). A `DEFAULT` partition catches strays but makes creating new partitions slower (PostgreSQL must check the default for rows that belong to the new range) and blocks `DETACH ... CONCURRENTLY` — keep it empty or avoid it.
            - **Queries without the partition key** (e.g. "all events of user X ever") scan all 90 partitions; planning and execution overhead grows with the partition count, so avoid thousands of tiny partitions.
            - **Index builds:** `CREATE INDEX ... CONCURRENTLY` isn't supported on the partitioned parent. Use `CREATE INDEX ... ON ONLY events`, build each partition's index `CONCURRENTLY`, then `ALTER INDEX ... ATTACH PARTITION`.
            - **Migrating an existing 2B-row table:** create the partitioned table, route new writes to it, backfill old data in batches, or attach the old table as one big partition after adding a validated `CHECK` constraint that matches the bounds (so `ATTACH` can skip the scan).
            - **Alternatives / extras:** BRIN on `created_at` inside weekly/monthly partitions; archiving old partitions to object storage (e.g. Parquet) before dropping; extensions like TimescaleDB or Citus when you outgrow one node.
        """,
        ex_bn=r"""
            **কী কী ভুল হতে পারে**
            - **ভবিষ্যতের partition নেই** → insert fail করে ("no partition of relation found for row")। একটা `DEFAULT` partition বিপথে যাওয়া row ধরে, কিন্তু নতুন partition তৈরি ধীর করে (নতুন range-এর row default-এ আছে কিনা PostgreSQL-কে দেখতে হয়) আর `DETACH ... CONCURRENTLY` আটকে দেয় — এটা খালি রাখো বা এড়িয়ে চলো।
            - **Partition key ছাড়া query** (যেমন "user X-এর সব সময়ের সব event") ৯০টা partition-ই scan করে; partition সংখ্যার সাথে planning আর execution-এর overhead বাড়ে, তাই হাজার হাজার ছোট partition এড়িয়ে চলো।
            - **Index build:** partitioned parent-এ `CREATE INDEX ... CONCURRENTLY` support করে না। `CREATE INDEX ... ON ONLY events` দাও, প্রতিটা partition-এর index `CONCURRENTLY` বানাও, তারপর `ALTER INDEX ... ATTACH PARTITION`।
            - **বিদ্যমান ২০০ কোটি row-এর table migrate করা:** partitioned table বানাও, নতুন write সেখানে পাঠাও, পুরনো data batch-এ backfill করো — অথবা bound-এর সাথে মেলে এমন একটা validated `CHECK` constraint যোগ করে পুরনো table-টাকে একটা বড় partition হিসেবে attach করো (যাতে `ATTACH` scan বাদ দিতে পারে)।
            - **বিকল্প / বাড়তি:** weekly/monthly partition-এর ভেতরে `created_at`-এ BRIN; drop করার আগে পুরনো partition object storage-এ archive (যেমন Parquet); এক node-এ না কুলোলে TimescaleDB বা Citus-এর মতো extension।
        """,
        tip_en=r"""Lead with "retention by dropping partitions instead of DELETE" — it's the strongest single argument. Then cover keys, indexes, rollups, and two or three concrete failure modes. Quote numbers (20M/day ≈ 230 rows/s average) to show you size things.""",
        tip_bn=r""""DELETE-এর বদলে partition drop করে retention" — এই যুক্তি দিয়ে শুরু করো, এটাই সবচেয়ে শক্তিশালী। তারপর key, index, rollup আর দুই-তিনটা concrete failure mode বলো। সংখ্যা উল্লেখ করো (দিনে ২ কোটি ≈ গড়ে সেকেন্ডে ২৩০ row) — বোঝা যাবে তুমি আকার মেপে design করো।""",
        mist_en=r"""Partitioning by `user_id` when every query and the retention policy are time-based, creating hourly partitions (thousands of tables), or forgetting that unique keys must include the partition key.""",
        mist_bn=r"""সব query আর retention policy সময়-ভিত্তিক হওয়া সত্ত্বেও `user_id` ধরে partition করা, ঘণ্টাভিত্তিক partition বানানো (হাজার হাজার table), অথবা ভুলে যাওয়া যে unique key-তে partition key থাকতেই হবে।""",
        code=r"""
            CREATE TABLE events (
              id          bigint GENERATED ALWAYS AS IDENTITY,   -- identity on partitioned tables: PG17+
              user_id     bigint      NOT NULL,
              event_type  text        NOT NULL,
              payload     jsonb,
              created_at  timestamptz NOT NULL DEFAULT now(),
              PRIMARY KEY (id, created_at)                       -- must include the partition key
            ) PARTITION BY RANGE (created_at);

            CREATE TABLE events_2026_10_12 PARTITION OF events
              FOR VALUES FROM ('2026-10-12 00:00+06') TO ('2026-10-13 00:00+06');

            -- defined on the parent, created on every partition (incl. future ones)
            CREATE INDEX ON events (user_id, created_at DESC);

            -- retention: detach without blocking queries, then drop (instant, no bloat)
            ALTER TABLE events DETACH PARTITION events_2026_07_13 CONCURRENTLY;
            DROP TABLE events_2026_07_13;

            -- dashboards read a small rollup instead of raw events
            CREATE TABLE event_counts_hourly (
              bucket      timestamptz NOT NULL,
              event_type  text        NOT NULL,
              n           bigint      NOT NULL,
              PRIMARY KEY (bucket, event_type)
            );
        """,
        lang="sql",
        follow=[
            ("How would you add a new index to all 90 partitions without blocking writes?", "Write block না করে ৯০টা partition-এই নতুন index কীভাবে যোগ করবে?"),
            ("When would you partition by hash of `user_id` instead?", "কখন এর বদলে `user_id`-এর hash ধরে partition করবে?"),
            ("At what point would you move analytics out of PostgreSQL?", "কোন পর্যায়ে analytics PostgreSQL থেকে বের করে নেবে?"),
        ],
        related=["pg-013", "pg-029"],
        refs=[PG_PARTITIONING, PG_ALTER_TABLE],
    ),
    # ------------------------------------------------------------------ pg-031
    Q(
        id="pg-031", sub="Production Performance Incident", diff="extreme", type="scenario",
        prio="high", market="international", mins=20,
        tags=["incident", "pg_stat_statements", "pg_stat_activity", "performance-tuning", "work_mem"],
        ver="PostgreSQL 18", vs=False, status="stable",
        q_en=r"""At 11:05 on a weekday, p95 latency of your checkout API jumps from 80 ms to 4 s and database CPU sits at 95%. Nothing was deployed today. Walk me through how you would diagnose and stabilise PostgreSQL in the next 30 minutes, and what you would change afterwards.""",
        q_bn=r"""এক কর্মদিবসে সকাল ১১:০৫-এ তোমার checkout API-র p95 latency 80 ms থেকে 4 s-এ লাফিয়ে উঠল, আর database CPU 95%-এ আটকে আছে। আজ কোনো deploy হয়নি। পরের ৩০ মিনিটে PostgreSQL কীভাবে diagnose আর স্থিতিশীল করবে, আর পরে কী বদলাবে — ধাপে ধাপে বলো।""",
        a_en=r"""
            This is an advanced, open-ended incident question. My approach: **stabilise first, then find the root cause.**

            **1. Triage (first ~5 minutes)**
            - Confirm it's the database (APM traces show time spent in queries, not in the app or network).
            - `pg_stat_activity`: how many sessions are `active`? What are they waiting on (`wait_event_type`: `Lock`, `IO`, `LWLock`, or none = burning CPU)? Which queries run longest? `pg_blocking_pids()` shows lock chains.

            **2. Find the expensive statements**
            - `pg_stat_statements` sorted by `total_exec_time` (compare against an earlier snapshot): is it one query whose **mean time jumped** (a plan change), a **new heavy query** (someone's report, a cron job), or a **call-count explosion** (N+1, retry storm, cache failure sending traffic to the DB)?
            - `EXPLAIN (ANALYZE)` the suspect with real parameters and compare with the last known-good plan (from `auto_explain` logs).

            **3. Stabilise**
            - Cancel or terminate runaway queries (`pg_cancel_backend` / `pg_terminate_backend`); kill a lock blocker.
            - Contain the source: disable the feature flag or job, rate-limit, move reporting to a replica, set `statement_timeout` for that role.
            - Targeted fix if clear: `ANALYZE` the table, `CREATE INDEX CONCURRENTLY` for a missing index.

            **4. Common "nothing deployed" causes:** a plan flip after auto-analyze or data growth crossing a threshold; a prepared statement switching to a generic plan; a cache (e.g. Redis) outage causing a thundering herd; a big ad-hoc query or `ALTER TABLE` waiting on a lock; an anti-wraparound vacuum on a hot table; bloat; replica lag pushing reads to the primary.
        """,
        a_bn=r"""
            এটা একটা advanced, open-ended incident প্রশ্ন। আমার পদ্ধতি: **আগে স্থিতিশীল করো, তারপর root cause খোঁজো।**

            **1. Triage (প্রথম ~৫ মিনিট)**
            - নিশ্চিত হও সমস্যা database-এ (APM trace দেখায় সময় query-তে যাচ্ছে, app বা network-এ নয়)।
            - `pg_stat_activity`: কতগুলো session `active`? কীসের জন্য অপেক্ষা করছে (`wait_event_type`: `Lock`, `IO`, `LWLock`, নাকি কিছুই না = CPU পোড়াচ্ছে)? কোন query সবচেয়ে বেশি সময় চলছে? `pg_blocking_pids()` lock-এর chain দেখায়।

            **2. ব্যয়বহুল statement খোঁজো**
            - `pg_stat_statements`-কে `total_exec_time` অনুযায়ী sort করো (আগের একটা snapshot-এর সাথে তুলনা করে): একটা query-র **mean time লাফিয়ে বেড়েছে** (plan বদলেছে), নাকি একটা **নতুন ভারী query** (কারো report, cron job), নাকি **call সংখ্যা বিস্ফোরিত** (N+1, retry storm, cache fail করে সব traffic DB-তে)?
            - সন্দেহজনক query-টা আসল parameter দিয়ে `EXPLAIN (ANALYZE)` করো আর শেষ ভালো plan-এর সাথে মেলাও (`auto_explain` log থেকে)।

            **3. স্থিতিশীল করো**
            - Runaway query cancel বা terminate করো (`pg_cancel_backend` / `pg_terminate_backend`); lock blocker-কে kill করো।
            - উৎস আটকাও: feature flag বা job বন্ধ করো, rate-limit করো, reporting replica-তে সরাও, ওই role-এর জন্য `statement_timeout` দাও।
            - পরিষ্কার হলে নির্দিষ্ট fix: table-এ `ANALYZE`, অনুপস্থিত index-এর জন্য `CREATE INDEX CONCURRENTLY`।

            **4. "কিছুই deploy হয়নি" অবস্থার সাধারণ কারণ:** auto-analyze বা data বেড়ে কোনো সীমা পার হওয়ায় plan flip; prepared statement generic plan-এ চলে যাওয়া; cache (যেমন Redis) outage-এ thundering herd; বড় ad-hoc query বা lock-এর জন্য অপেক্ষমাণ `ALTER TABLE`; ব্যস্ত table-এ anti-wraparound vacuum; bloat; replica lag-এর কারণে read primary-তে চলে আসা।
        """,
        quick_en=r"""Stabilise first, then find the cause: check `pg_stat_activity` for wait events and lock chains, and `pg_stat_statements` for a query whose time or call count jumped. Cancel runaway queries, contain the source with a flag or `statement_timeout`, then fix the plan, index or statistics.""",
        quick_bn=r"""আগে system স্থির করো, তারপর কারণ খোঁজো: `pg_stat_activity`-তে wait event আর lock chain দেখো, আর `pg_stat_statements`-এ দেখো কোন query-র সময় বা call সংখ্যা হঠাৎ বেড়েছে। লাগামছাড়া query cancel করো, flag বা `statement_timeout` দিয়ে উৎস আটকাও, তারপর plan, index বা statistics ঠিক করো।""",
        ex_en=r"""
            **Afterwards (prevention)**
            - Enable `pg_stat_statements` and `auto_explain` (`auto_explain.log_min_duration`) permanently so the next incident has evidence; keep snapshots of query stats to diff against.
            - Default `statement_timeout`/`idle_in_transaction_session_timeout` per role; analysts on a replica, never on the primary.
            - Alert on leading indicators: active sessions, lock waits, replication lag, dead tuples, XID age, cache hit ratio, slow-query count.
            - **Memory settings worth knowing:** `shared_buffers` (commonly ~25% of RAM as a starting point), `work_mem` (per sort/hash *operation*, per backend — a "Sort Method: external merge Disk" line means the sort spilled; raise it per role or per query, not globally to a huge value), `effective_cache_size` (planner hint only), `maintenance_work_mem` (vacuum and index builds).
            - Fix N+1 patterns in the ORM with joins or batched `WHERE id = ANY($1)` lookups.
            - Write a blameless post-mortem with timeline, root cause, and action items.
        """,
        ex_bn=r"""
            **পরে (প্রতিরোধ)**
            - `pg_stat_statements` আর `auto_explain` (`auto_explain.log_min_duration`) স্থায়ীভাবে চালু রাখো, যাতে পরের incident-এ প্রমাণ থাকে; তুলনার জন্য query stats-এর snapshot রেখে দাও।
            - Role অনুযায়ী default `statement_timeout`/`idle_in_transaction_session_timeout`; analyst-রা replica-তে, কখনো primary-তে নয়।
            - আগাম সংকেতে alert: active session, lock wait, replication lag, dead tuple, XID age, cache hit ratio, slow-query সংখ্যা।
            - **জানা দরকার এমন memory setting:** `shared_buffers` (শুরু হিসেবে সাধারণত RAM-এর ~25%), `work_mem` (প্রতি backend-এ প্রতিটা sort/hash *operation*-এর জন্য — "Sort Method: external merge Disk" লাইন মানে sort disk-এ spill করেছে; role বা query অনুযায়ী বাড়াও, globally বিশাল value দিয়ো না), `effective_cache_size` (শুধু planner-এর জন্য ইঙ্গিত), `maintenance_work_mem` (vacuum আর index build)।
            - ORM-এর N+1 pattern join বা batch করা `WHERE id = ANY($1)` lookup দিয়ে ঠিক করো।
            - Timeline, root cause আর action item-সহ একটা blameless post-mortem লেখো।
        """,
        tip_en=r"""Say "stabilise first, root-cause second" up front, then narrate the exact views and functions you'd query. Listing the likely "no deploy" causes shows pattern recognition from real incidents.""",
        tip_bn=r"""শুরুতেই বলো "আগে স্থিতিশীল, পরে root cause", তারপর কোন view আর function query করবে সেগুলো হুবহু বলে যাও। "কোনো deploy হয়নি" অবস্থার সম্ভাব্য কারণগুলো বললে বোঝা যায় বাস্তব incident থেকে তুমি pattern চিনতে শিখেছ।""",
        mist_en=r"""Restarting PostgreSQL first (losing all evidence and the cache), raising `max_connections` or `work_mem` globally in a panic, or adding indexes blindly without `CONCURRENTLY`.""",
        mist_bn=r"""প্রথমেই PostgreSQL restart করা (সব প্রমাণ আর cache হারানো), আতঙ্কে globally `max_connections` বা `work_mem` বাড়ানো, অথবা `CONCURRENTLY` ছাড়া অন্ধভাবে index যোগ করা।""",
        code=r"""
            -- 1. what is running right now, and what is it waiting on?
            SELECT pid, now() - query_start AS runtime, state, wait_event_type, wait_event,
                   pg_blocking_pids(pid) AS blocked_by, left(query, 80) AS query
            FROM pg_stat_activity
            WHERE state <> 'idle' AND backend_type = 'client backend'
            ORDER BY runtime DESC
            LIMIT 20;

            -- 2. which statements consume the most time? (needs the pg_stat_statements extension)
            SELECT queryid, calls, round(total_exec_time) AS total_ms,
                   round(mean_exec_time::numeric, 1) AS mean_ms, rows, left(query, 80) AS query
            FROM pg_stat_statements
            ORDER BY total_exec_time DESC
            LIMIT 10;

            -- 3. stop the bleeding
            SELECT pg_cancel_backend(12345);      -- cancel the current query of pid 12345
            SELECT pg_terminate_backend(12345);   -- or end the whole session
            ALTER ROLE reporting SET statement_timeout = '30s';
        """,
        lang="sql",
        follow=[
            ("How do generic plans for prepared statements cause sudden slowdowns, and how do you fix them?", "Prepared statement-এর generic plan কীভাবে হঠাৎ ধীরগতির কারণ হয়, আর কীভাবে ঠিক করবে?"),
            ("What does `Sort Method: external merge  Disk: 120MB` tell you?", "`Sort Method: external merge  Disk: 120MB` তোমাকে কী জানায়?"),
        ],
        related=["pg-024", "pg-021", "pg-029"],
        refs=[PG_STAT_STATEMENTS, PG_MONITORING, PG_ADMIN_FUNCS],
    ),
    # ------------------------------------------------------------------ pg-032
    Q(
        id="pg-032", sub="Multi-Tenant Architecture & Row-Level Security", diff="extreme", type="architecture",
        prio="high", market="international", mins=20,
        tags=["multi-tenancy", "row-level-security", "saas", "schema-per-tenant", "isolation"],
        ver="PostgreSQL 18", vs=False, status="stable",
        q_en=r"""You're building a B2B SaaS (e.g. a POS or payroll product) on PostgreSQL for about 5,000 tenants — mostly small shops plus a few large enterprises. Compare a shared schema with `tenant_id` + row-level security, schema-per-tenant, and database-per-tenant. What would you choose, and how would you enforce tenant isolation safely?""",
        q_bn=r"""PostgreSQL-এর উপর প্রায় ৫,০০০ tenant-এর জন্য একটা B2B SaaS বানাচ্ছ (যেমন POS বা payroll product) — বেশিরভাগ ছোট দোকান, সাথে কয়েকটা বড় enterprise। `tenant_id` + row-level security-সহ shared schema, schema-per-tenant আর database-per-tenant — তুলনা করো। তুমি কোনটা বেছে নেবে, আর tenant isolation নিরাপদে কীভাবে enforce করবে?""",
        a_en=r"""
            Advanced question — the answer is a trade-off, so I'd compare first and then recommend.

            - **Shared schema + `tenant_id` + RLS:** one set of tables and one migration run; very efficient for thousands of small tenants; connection pooling is simple. Risks: noisy neighbours, a missing filter leaking data (RLS is the safety net), and per-tenant restore/export is harder.
            - **Schema-per-tenant:** clearer separation and easy per-tenant `pg_dump -n`. But 5,000 schemas × 50 tables = 250,000 tables: catalog bloat, high per-connection metadata cache memory, and migrations that must run 5,000 times and can fail halfway. Switching `search_path` per tenant is session state, which fights transaction-mode pooling.
            - **Database-per-tenant:** strongest isolation, per-tenant tuning, data residency, trivial delete/restore. Highest operational cost; connections can't be shared across databases, and cross-tenant analytics is hard.

            **My choice: a hybrid.** Shared schema with RLS for the long tail of small tenants; dedicated databases (or clusters) for the few enterprises that need isolation, compliance, or heavy capacity. A small tenant catalog maps each tenant to its location so the app routes connections.

            **Enforcing isolation in the shared schema**
            - `tenant_id` in every tenant-owned table, leading in primary keys and indexes (`PRIMARY KEY (tenant_id, id)`); composite foreign keys `(tenant_id, customer_id)` so rows can't reference another tenant's data.
            - `ENABLE` **and** `FORCE ROW LEVEL SECURITY`, with a policy comparing `tenant_id` to a per-transaction setting.
            - The app sets it with `set_config('app.tenant_id', $1, true)` at the start of each transaction (transaction-local, so it's safe with PgBouncer transaction mode).
            - The app role is not a superuser, not the table owner, and has no `BYPASSRLS`. Admin/migration roles are separate.
            - Automated tests that try cross-tenant reads and writes on every endpoint.
        """,
        a_bn=r"""
            Advanced প্রশ্ন — উত্তরটা একটা trade-off, তাই আগে তুলনা করে তারপর recommend করব।

            - **Shared schema + `tenant_id` + RLS:** একটাই table-এর set, একবারই migration চালানো; হাজারো ছোট tenant-এর জন্য খুবই efficient; connection pooling সহজ। ঝুঁকি: noisy neighbour, একটা filter বাদ পড়লে data leak (RLS হলো safety net), আর tenant অনুযায়ী restore/export কঠিন।
            - **Schema-per-tenant:** পরিষ্কার বিভাজন আর সহজ per-tenant `pg_dump -n`। কিন্তু ৫,০০০ schema × ৫০ table = ২,৫০,০০০ table: catalog bloat, প্রতি connection-এ metadata cache-এর জন্য বেশি memory, আর migration ৫,০০০ বার চালাতে হয় যেটা মাঝপথে fail করতে পারে। প্রতি tenant-এ `search_path` বদলানো session state, যা transaction-mode pooling-এর সাথে খাপ খায় না।
            - **Database-per-tenant:** সবচেয়ে শক্ত isolation, tenant অনুযায়ী tuning, data residency, delete/restore সহজ। Operational খরচ সবচেয়ে বেশি; database-এর মধ্যে connection ভাগ করা যায় না, আর cross-tenant analytics কঠিন।

            **আমার পছন্দ: hybrid।** ছোট tenant-দের লম্বা তালিকার জন্য RLS-সহ shared schema; isolation, compliance বা বেশি capacity লাগে এমন কয়েকটা enterprise-এর জন্য আলাদা database (বা cluster)। একটা ছোট tenant catalog প্রতিটা tenant কোথায় আছে সেটা map করে, যাতে app সঠিক জায়গায় connection পাঠায়।

            **Shared schema-তে isolation enforce করা**
            - প্রতিটা tenant-এর table-এ `tenant_id`, primary key আর index-এ সবার আগে (`PRIMARY KEY (tenant_id, id)`); composite foreign key `(tenant_id, customer_id)`, যাতে কোনো row অন্য tenant-এর data refer করতে না পারে।
            - `ENABLE` **আর** `FORCE ROW LEVEL SECURITY`, সাথে এমন policy যেটা `tenant_id`-কে প্রতি-transaction setting-এর সাথে মেলায়।
            - App প্রতিটা transaction-এর শুরুতে `set_config('app.tenant_id', $1, true)` দিয়ে এটা set করে (transaction-local, তাই PgBouncer transaction mode-এও নিরাপদ)।
            - App role superuser নয়, table owner নয়, আর এর `BYPASSRLS` নেই। Admin/migration role আলাদা।
            - প্রতিটা endpoint-এ cross-tenant read আর write-এর চেষ্টা করে এমন automated test।
        """,
        quick_en=r"""A hybrid: a shared schema with `tenant_id` and row-level security for the many small tenants, and dedicated databases for the few enterprises. Enforce isolation with `tenant_id` in keys, `FORCE ROW LEVEL SECURITY`, a transaction-local `app.tenant_id` setting, and an app role that isn't the owner or superuser.""",
        quick_bn=r"""একটা hybrid: অনেকগুলো ছোট tenant-এর জন্য `tenant_id` আর row-level security-সহ shared schema, আর অল্প কয়েকটা enterprise-এর জন্য আলাদা database। Isolation নিশ্চিত করো key-তে `tenant_id`, `FORCE ROW LEVEL SECURITY`, transaction-local `app.tenant_id` setting আর এমন app role দিয়ে যেটা owner বা superuser নয়।""",
        ex_en=r"""
            - **Fail closed:** if the app forgets to set `app.tenant_id`, `current_setting('app.tenant_id')` raises "unrecognized configuration parameter" (or, later in the same session, the empty string fails the `::bigint` cast) — the query errors instead of returning other tenants' rows.
            - **Performance:** the policy predicate is added to every query; with `tenant_id` leading your indexes, it becomes an index condition. Check plans with `EXPLAIN`. Functions used in policies should be simple; non-`LEAKPROOF` functions can prevent some optimisations.
            - **Noisy neighbours:** per-tenant rate limits and `statement_timeout`; for very large tenants in the shared cluster, `LIST`/`HASH` partitioning by `tenant_id` or moving them to their own database.
            - **Scaling out:** Citus (an extension) can distribute tables by `tenant_id` across nodes when one server isn't enough.
            - **Operational must-haves:** per-tenant export/delete tooling (GDPR-style requests), audit logs, and backups that let you restore one tenant (logical export from a PITR copy).
        """,
        ex_bn=r"""
            - **Fail closed:** app যদি `app.tenant_id` set করতে ভুলে যায়, `current_setting('app.tenant_id')` "unrecognized configuration parameter" error দেয় (অথবা একই session-এ পরে খালি string `::bigint` cast-এ fail করে) — অন্য tenant-এর row ফেরত না দিয়ে query error দেয়।
            - **Performance:** policy-র predicate প্রতিটা query-তে যোগ হয়; index-এর শুরুতে `tenant_id` থাকলে এটা index condition হয়ে যায়। `EXPLAIN` দিয়ে plan দেখো। Policy-তে ব্যবহৃত function সরল রাখো; non-`LEAKPROOF` function কিছু optimisation আটকে দিতে পারে।
            - **Noisy neighbour:** tenant অনুযায়ী rate limit আর `statement_timeout`; shared cluster-এ খুব বড় tenant থাকলে `tenant_id` ধরে `LIST`/`HASH` partitioning, বা তাদের আলাদা database-এ সরানো।
            - **Scale out:** এক server-এ না কুলোলে Citus (একটা extension) `tenant_id` ধরে table-গুলো একাধিক node-এ ভাগ করতে পারে।
            - **Operational-এ যা লাগবেই:** tenant অনুযায়ী export/delete tooling (GDPR ধরনের request), audit log, আর এমন backup যা দিয়ে একটা tenant restore করা যায় (PITR copy থেকে logical export)।
        """,
        tip_en=r"""Compare on the same axes for all three (isolation, ops cost, migrations, pooling, per-tenant restore), then commit to a recommendation. Showing the RLS policy *and* how the app sets the tenant per transaction is what makes the answer credible.""",
        tip_bn=r"""তিনটাকেই একই মাপকাঠিতে তুলনা করো (isolation, ops খরচ, migration, pooling, per-tenant restore), তারপর একটা recommendation-এ স্থির হও। RLS policy *আর* app কীভাবে প্রতি transaction-এ tenant set করে — দুটোই দেখালে উত্তর বিশ্বাসযোগ্য হয়।""",
        mist_en=r"""Connecting as the table owner (RLS silently doesn't apply without `FORCE`), using session-level `SET app.tenant_id` behind a transaction-mode pooler (the setting leaks to the next tenant's transaction), or choosing schema-per-tenant for thousands of tenants without considering migrations and catalog size.""",
        mist_bn=r"""Table owner হিসেবে connect করা (`FORCE` ছাড়া RLS নীরবে প্রয়োগ হয় না), transaction-mode pooler-এর পেছনে session-level `SET app.tenant_id` ব্যবহার করা (setting পরের tenant-এর transaction-এ চলে যায়), অথবা migration আর catalog-এর আকার না ভেবে হাজারো tenant-এর জন্য schema-per-tenant বেছে নেওয়া।""",
        code=r"""
            CREATE TABLE invoices (
              tenant_id   bigint NOT NULL,
              id          bigint GENERATED ALWAYS AS IDENTITY,
              customer_id bigint NOT NULL,
              amount      numeric(12,2) NOT NULL,
              PRIMARY KEY (tenant_id, id),
              FOREIGN KEY (tenant_id, customer_id) REFERENCES customers (tenant_id, id)
            );

            ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
            ALTER TABLE invoices FORCE ROW LEVEL SECURITY;   -- applies to the table owner too

            CREATE POLICY tenant_isolation ON invoices
              USING      (tenant_id = current_setting('app.tenant_id')::bigint)
              WITH CHECK (tenant_id = current_setting('app.tenant_id')::bigint);
        """,
        lang="sql",
        extra=[dict(lang="javascript", label_en="Setting the tenant per transaction (node-postgres)",
                    label_bn="প্রতি transaction-এ tenant set করা (node-postgres)", src=r"""
            export async function withTenant(pool, tenantId, fn) {
              const client = await pool.connect();
              try {
                await client.query('BEGIN');
                // third argument true = local to this transaction (safe behind PgBouncer transaction mode)
                await client.query("SELECT set_config('app.tenant_id', $1, true)", [String(tenantId)]);
                const result = await fn(client);
                await client.query('COMMIT');
                return result;
              } catch (err) {
                await client.query('ROLLBACK');
                throw err;
              } finally {
                client.release();
              }
            }

            // usage: RLS filters every query to tenant 42
            const invoices = await withTenant(pool, 42, (c) =>
              c.query('SELECT id, amount FROM invoices ORDER BY id DESC LIMIT 20'));
        """)],
        follow=[
            ("How would you move one large tenant from the shared database to its own database without downtime?", "Downtime ছাড়া একটা বড় tenant-কে shared database থেকে তার নিজের database-এ কীভাবে সরাবে?"),
            ("How do you test that RLS policies really prevent cross-tenant access?", "RLS policy যে সত্যিই cross-tenant access আটকায়, সেটা কীভাবে test করবে?"),
        ],
        related=["pg-018", "pg-021", "pg-030"],
        refs=[PG_RLS, PG_SCHEMAS, PG_PARTITIONING],
    ),
]

if __name__ == "__main__":
    save("postgresql", "b4", QUESTIONS)
