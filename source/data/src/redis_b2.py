# Redis — batch 2 (redis-005, 006, 007, 014, 015, 016, 024, 025)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_TYPES = ("Redis docs — Data types", "https://redis.io/docs/latest/develop/data-types/")
R_NODE = ("Redis docs — node-redis guide", "https://redis.io/docs/latest/develop/clients/nodejs/")
R_SET = ("Redis docs — SET", "https://redis.io/docs/latest/commands/set/")
R_KEYS = ("Redis docs — KEYS", "https://redis.io/docs/latest/commands/keys/")
R_SCAN = ("Redis docs — SCAN", "https://redis.io/docs/latest/commands/scan/")
R_LATENCY = ("Redis docs — Diagnosing latency issues", "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/")
R_PERSIST = ("Redis docs — Persistence", "https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/")
R_TX = ("Redis docs — Transactions", "https://redis.io/docs/latest/develop/using-commands/transactions/")
R_PUBSUB = ("Redis docs — Pub/Sub", "https://redis.io/docs/latest/develop/pubsub/")
R_STREAMS = ("Redis docs — Streams", "https://redis.io/docs/latest/develop/data-types/streams/")
R_BLMOVE = ("Redis docs — BLMOVE", "https://redis.io/docs/latest/commands/blmove/")
R_ZRANGE = ("Redis docs — ZRANGE", "https://redis.io/docs/latest/commands/zrange/")
R_ZSETS = ("Redis docs — Sorted sets", "https://redis.io/docs/latest/develop/data-types/sorted-sets/")
R_LUA = ("Redis docs — Scripting with Lua", "https://redis.io/docs/latest/develop/programmability/eval-intro/")
R_INCR = ("Redis docs — INCR (counter & rate limiter patterns)", "https://redis.io/docs/latest/commands/incr/")
R_LOCKS = ("Redis docs — Distributed locks", "https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/")
R_DELEX = ("Redis docs — DELEX", "https://redis.io/docs/latest/commands/delex/")

QUESTIONS = [
    # ------------------------------------------------------------------ redis-005
    Q(
        id="redis-005", sub="Cache-Aside", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["cache-aside", "caching", "node-redis", "write-through"],
        ver="node-redis 6.3; Redis Open Source 8.10", vs=True, status="stable",
        q_en=r"""What is the cache-aside (lazy loading) pattern? Show how you would implement it in Node.js with Redis, and how it differs from write-through and write-behind caching.""",
        q_bn=r"""Cache-aside (lazy loading) pattern কী? Node.js-এ Redis দিয়ে এটা কীভাবে implement করবে দেখাও, আর write-through ও write-behind caching থেকে এটা কীভাবে আলাদা?""",
        a_en=r"""
            In **cache-aside**, the application owns the cache logic:
            1. Read from Redis first.
            2. On a **hit**, return the cached value.
            3. On a **miss**, read from the database, store the result in Redis **with a TTL**, and return it.
            4. On writes, update the database and then **delete** the cache key so the next read reloads fresh data.

            It's the most common pattern because only data that's actually requested gets cached, and if Redis goes down the app can still read from the database.

            By contrast, **write-through** writes to the cache and the database together on every write, so the cache is always warm but writes are slower. **Write-behind** writes to the cache first and flushes to the database asynchronously — fast writes, but you risk losing data if the cache fails before the flush.
        """,
        a_bn=r"""
            **Cache-aside**-এ cache-এর logic application নিজে সামলায়:
            1. প্রথমে Redis থেকে পড়ো।
            2. **Hit** হলে cached value return করো।
            3. **Miss** হলে database থেকে পড়ো, result-টা **TTL সহ** Redis-এ রাখো, তারপর return করো।
            4. Write-এর সময় আগে database update করো, তারপর cache key **delete** করো, যাতে পরের read-এ fresh data load হয়।

            এটাই সবচেয়ে প্রচলিত pattern, কারণ শুধু যে data আসলে চাওয়া হয় সেটাই cache হয়, আর Redis down হলেও app database থেকে পড়তে পারে।

            বিপরীতে, **write-through**-এ প্রতিটা write-এ cache আর database দুটোতেই একসাথে লেখা হয় — cache সবসময় warm থাকে, কিন্তু write ধীর হয়। **Write-behind**-এ আগে cache-এ লেখা হয়, পরে asynchronously database-এ flush হয় — write দ্রুত, কিন্তু flush-এর আগে cache fail করলে data হারানোর ঝুঁকি।
        """,
        ex_en=r"""
            - **TTL is your safety net:** even with delete-on-write, some invalidations will be missed (bugs, failed deletes, other services writing to the DB). A TTL bounds how stale data can get.
            - **First request is slow:** a cold cache (after deploy or restart) sends traffic to the DB; warm critical keys or protect against stampedes.
            - **node-redis v6 syntax:** expiry is passed as `{ expiration: { type: 'EX', value: 300 } }`. The older `{ EX: 300 }` shorthand still works but is marked deprecated in the client's types.
            - **Serialization:** strings hold JSON; parse on read and be careful with `Date` objects, which come back as strings.
        """,
        ex_bn=r"""
            - **TTL হলো safety net:** delete-on-write থাকলেও কিছু invalidation miss হবেই (bug, fail হওয়া delete, অন্য service সরাসরি DB-তে লিখছে)। TTL ঠিক করে দেয় data সর্বোচ্চ কতটা পুরনো হতে পারে।
            - **প্রথম request ধীর:** cold cache (deploy বা restart-এর পর) সব traffic DB-তে পাঠায়; জরুরি key আগেই warm করো বা stampede থেকে সুরক্ষা রাখো।
            - **node-redis v6 syntax:** expiry দেওয়া হয় `{ expiration: { type: 'EX', value: 300 } }` দিয়ে। পুরনো `{ EX: 300 }` shorthand এখনো কাজ করে, কিন্তু client-এর type-এ deprecated হিসেবে চিহ্নিত।
            - **Serialization:** string-এ JSON থাকে; read-এর সময় parse করো, আর `Date` object-এর ব্যাপারে সাবধান — এগুলো string হয়ে ফেরত আসে।
        """,
        tip_en=r"""Walk through the read path and the write path separately, then name one failure mode (stale data or stampede). Comparing with write-through/write-behind in one sentence each is usually enough.""",
        tip_bn=r"""Read path আর write path আলাদা করে বুঝিয়ে বলো, তারপর একটা failure mode (stale data বা stampede) উল্লেখ করো। Write-through/write-behind-এর সাথে তুলনা প্রতিটার জন্য এক লাইনে করলেই সাধারণত যথেষ্ট।""",
        mist_en=r"""Forgetting the TTL, updating the cache before the database commit, or treating Redis as the source of truth in a cache-aside setup.""",
        mist_bn=r"""TTL দিতে ভুলে যাওয়া, database commit-এর আগে cache update করা, অথবা cache-aside setup-এ Redis-কেই source of truth ভেবে নেওয়া।""",
        code=r"""
            import { createClient } from 'redis';
            import { db } from './db.js';

            const redis = await createClient({ url: process.env.REDIS_URL })
              .on('error', (err) => console.error('Redis error', err))
              .connect();

            export async function getUser(id) {
              const key = `user:${id}`;
              const cached = await redis.get(key);
              if (cached !== null) return JSON.parse(cached);   // 1. hit

              const user = await db.users.findById(id);         // 2. miss -> DB
              if (user) {
                await redis.set(key, JSON.stringify(user), {    // 3. populate with TTL
                  expiration: { type: 'EX', value: 300 },
                });
              }
              return user;
            }

            export async function updateUser(id, changes) {
              await db.users.update(id, changes);               // 4. write DB first
              await redis.del(`user:${id}`);                    //    then invalidate
            }
        """,
        lang="javascript",
        follow=[
            ("When would write-through be a better choice than cache-aside?", "কখন cache-aside-এর চেয়ে write-through ভালো হবে?"),
            ("Why delete the key on update instead of setting the new value?", "Update-এর সময় নতুন value set না করে key delete করা কেন?"),
        ],
        related=["redis-013", "redis-014", "redis-023"],
        refs=[R_NODE, R_SET],
    ),
    # ------------------------------------------------------------------ redis-006
    Q(
        id="redis-006", sub="Redis vs Traditional Databases", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["redis", "postgresql", "mongodb", "durability", "primary-database"],
        ver="Redis Open Source 8.10", vs=False, status="stable",
        q_en=r"""How is Redis different from a traditional database like PostgreSQL or MongoDB? Can Redis be your primary database?""",
        q_bn=r"""PostgreSQL বা MongoDB-এর মতো traditional database থেকে Redis কীভাবে আলাদা? Redis কি তোমার primary database হতে পারে?""",
        a_en=r"""
            - **Storage:** Redis keeps the whole dataset in RAM; PostgreSQL/MongoDB keep data on disk and cache hot pages in memory. So Redis is faster but the dataset is limited by memory and cost.
            - **Query model:** Redis is accessed by key with data-structure commands (`HGET`, `ZADD`). Traditional databases support rich queries — joins, aggregations, secondary indexes, ad-hoc filters.
            - **Durability:** PostgreSQL commits are durable once the WAL is flushed. Redis persistence (RDB/AOF) is configurable; with the common `everysec` setting you can lose about a second of writes on a crash.
            - **Transactions:** Redis `MULTI`/`EXEC` runs commands in isolation but has no rollback; relational databases give full ACID with constraints and foreign keys.

            Redis *can* be a primary store for data that is naturally key-based and tolerant of small loss — sessions, rate-limit counters, leaderboards, real-time presence. For orders, payments or anything relational, I keep PostgreSQL or MongoDB as the source of truth and use Redis beside it.
        """,
        a_bn=r"""
            - **Storage:** Redis পুরো dataset RAM-এ রাখে; PostgreSQL/MongoDB data disk-এ রাখে আর hot page memory-তে cache করে। তাই Redis দ্রুত, কিন্তু dataset-এর আকার memory আর খরচ দিয়ে সীমিত।
            - **Query model:** Redis-এ key ধরে data-structure command (`HGET`, `ZADD`) দিয়ে কাজ হয়। Traditional database-এ rich query চলে — join, aggregation, secondary index, যেকোনো filter।
            - **Durability:** PostgreSQL-এ WAL flush হলেই commit durable। Redis-এর persistence (RDB/AOF) configure করা যায়; প্রচলিত `everysec` setting-এ crash হলে প্রায় এক সেকেন্ডের write হারাতে পারে।
            - **Transaction:** Redis-এর `MULTI`/`EXEC` command-গুলো isolation-এ চালায়, কিন্তু rollback নেই; relational database constraint আর foreign key সহ পূর্ণ ACID দেয়।

            যে data স্বাভাবিকভাবে key-based আর সামান্য loss সহ্য করতে পারে — session, rate-limit counter, leaderboard, real-time presence — সেগুলোর জন্য Redis primary store *হতে পারে*। Order, payment বা relational কিছুর জন্য আমি PostgreSQL বা MongoDB-কেই source of truth রাখি আর পাশে Redis ব্যবহার করি।
        """,
        ex_en=r"""
            - **Redis 8 narrows the gap a little:** the built-in Query Engine adds secondary indexing, full-text and vector search over hashes and JSON documents. It's powerful for search use cases, but it doesn't replace relational modelling, constraints or multi-row ACID transactions.
            - **Cost thinking:** 100 GB of RAM costs far more than 100 GB of SSD, so "put everything in Redis" rarely makes sense economically.
            - **Operational view:** if Redis is primary, you must design persistence, replication, backups and failover with the same care as any database.
        """,
        ex_bn=r"""
            - **Redis 8 ব্যবধান কিছুটা কমিয়েছে:** built-in Query Engine hash আর JSON document-এর ওপর secondary indexing, full-text আর vector search যোগ করে। Search-এর কাজে এটা শক্তিশালী, কিন্তু relational modelling, constraint বা multi-row ACID transaction-এর বিকল্প নয়।
            - **খরচের হিসাব:** 100 GB RAM-এর দাম 100 GB SSD-এর চেয়ে অনেক বেশি, তাই "সবকিছু Redis-এ রাখো" অর্থনৈতিকভাবে খুব কমই যুক্তিসঙ্গত।
            - **Operational দিক:** Redis primary হলে persistence, replication, backup আর failover অন্য যেকোনো database-এর মতোই যত্ন নিয়ে design করতে হবে।
        """,
        tip_en=r"""Answer the "can it be primary?" part with "it depends on the data" and give one example each way. A nuanced yes/no beats an absolute answer.""",
        tip_bn=r""""Primary হতে পারে কি?" অংশের উত্তর দাও "data-র ওপর নির্ভর করে" বলে, আর দুই দিকেই একটা করে উদাহরণ দাও। একেবারে হ্যাঁ/না-এর চেয়ে nuanced উত্তর ভালো শোনায়।""",
        mist_en=r"""Claiming Redis "has no persistence", or claiming it's a drop-in replacement for a relational database because it's faster.""",
        mist_bn=r"""দাবি করা যে Redis-এ "কোনো persistence নেই", অথবা দ্রুত বলে এটা relational database-এর সরাসরি বিকল্প।""",
        follow=[
            ("Which Redis persistence settings would you use if Redis stored user sessions?", "Redis-এ user session রাখলে কোন persistence setting ব্যবহার করবে?"),
            ("What does Redis `MULTI`/`EXEC` guarantee, and what doesn't it guarantee?", "Redis `MULTI`/`EXEC` কী guarantee দেয়, আর কী দেয় না?"),
        ],
        related=["redis-001", "redis-027", "redis-029"],
        refs=[R_TYPES, R_PERSIST, R_TX],
    ),
    # ------------------------------------------------------------------ redis-007
    Q(
        id="redis-007", sub="Memory Usage", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["keys", "scan", "latency", "production"],
        ver="Version-independent concept (Redis Open Source 8.10)", vs=False, status="stable",
        q_en=r"""A teammate adds `await redis.keys('session:*')` to a cron job that cleans up sessions. Why is this dangerous in production?""",
        q_bn=r"""একজন teammate session পরিষ্কারের একটা cron job-এ `await redis.keys('session:*')` যোগ করেছে। Production-এ এটা কেন বিপজ্জনক?""",
        options=[
            ("`KEYS` only searches database 0, so sessions in other databases are missed", "`KEYS` শুধু database 0-এ খোঁজে, তাই অন্য database-এর session বাদ পড়ে যায়"),
            ("`KEYS` was removed in Redis 8, so the call will throw an error", "Redis 8-এ `KEYS` remove হয়ে গেছে, তাই call-টা error throw করবে"),
            ("`KEYS` returns keys in random order, so some sessions are deleted twice", "`KEYS` random order-এ key দেয়, তাই কিছু session দুইবার delete হবে"),
            ("`KEYS` scans the whole keyspace in one blocking O(N) call, freezing all other clients; use `SCAN` with `MATCH` instead", "`KEYS` এক blocking O(N) call-এ পুরো keyspace scan করে, বাকি সব client আটকে যায়; বদলে `MATCH` সহ `SCAN` ব্যবহার করো"),
        ],
        correct=3,
        a_en=r"""`KEYS` walks every key in the database in a single command. Because command execution is single-threaded, all other clients wait until it finishes — with millions of keys that can be hundreds of milliseconds or more. Use the cursor-based `SCAN` instead.""",
        a_bn=r"""`KEYS` একটাই command-এ database-এর প্রতিটা key ঘুরে দেখে। Command execution single-threaded বলে এটা শেষ না হওয়া পর্যন্ত বাকি সব client অপেক্ষা করে — লাখো key থাকলে সেটা কয়েকশো millisecond বা তারও বেশি হতে পারে। বদলে cursor-based `SCAN` ব্যবহার করো।""",
        ex_en=r"""
            The Redis docs explicitly warn against using `KEYS` in regular application code. `SCAN cursor MATCH session:* COUNT 1000` returns a small batch and a new cursor each time, so other commands run in between. Its guarantees are weaker: a key may be returned more than once, and keys added or removed during the scan may or may not appear — so make your processing idempotent. In node-redis v5+, `scanIterator()` yields **arrays of keys** per batch, which pairs nicely with `UNLINK` or `MGET`.

            Option A is tempting but irrelevant — the real issue is blocking. And `KEYS` still exists in Redis 8; it's simply meant for debugging. Better still: if you need to find all sessions often, give them a TTL so Redis expires them itself, or index them in a set.
        """,
        ex_bn=r"""
            Redis docs স্পষ্টভাবে বলে, সাধারণ application code-এ `KEYS` ব্যবহার কোরো না। `SCAN cursor MATCH session:* COUNT 1000` প্রতিবার ছোট একটা batch আর নতুন cursor দেয়, তাই মাঝখানে অন্য command-ও চলতে পারে। এর guarantee একটু দুর্বল: একই key একাধিকবার আসতে পারে, আর scan চলাকালীন যোগ বা মুছে যাওয়া key আসতেও পারে, না-ও পারে — তাই processing idempotent রাখো। node-redis v5+-এ `scanIterator()` প্রতি batch-এ **key-এর array** দেয়, যেটা `UNLINK` বা `MGET`-এর সাথে ভালো মেলে।

            Option A আকর্ষণীয় মনে হলেও অপ্রাসঙ্গিক — আসল সমস্যা blocking। আর Redis 8-এও `KEYS` আছে; এটা শুধু debugging-এর জন্য। আরও ভালো উপায়: সব session প্রায়ই খুঁজতে হলে তাদের TTL দাও যাতে Redis নিজেই expire করে, অথবা একটা set-এ index রাখো।
        """,
        tip_en=r"""Link the answer back to Redis's single-threaded execution — that one idea explains `KEYS`, big `DEL`s and slow Lua scripts. Then mention `SCAN`'s weaker guarantees.""",
        tip_bn=r"""উত্তরটাকে Redis-এর single-threaded execution-এর সাথে যুক্ত করো — এই একটা ধারণাই `KEYS`, বড় `DEL` আর slow Lua script-এর সমস্যা ব্যাখ্যা করে। তারপর `SCAN`-এর দুর্বল guarantee-গুলো উল্লেখ করো।""",
        extra=[dict(lang="javascript", label_en="Safer cleanup with SCAN", label_bn="SCAN দিয়ে নিরাপদ cleanup", src=r"""
            // node-redis v5+/v6: scanIterator yields batches (arrays) of keys
            for await (const keys of redis.scanIterator({ MATCH: 'session:*', COUNT: 1000 })) {
              if (keys.length) await redis.unlink(keys);
            }
        """)],
        refs=[R_KEYS, R_SCAN, R_LATENCY],
        related=["redis-026", "redis-032"],
    ),
    # ------------------------------------------------------------------ redis-014
    Q(
        id="redis-014", sub="Cache Invalidation", diff="medium", type="scenario",
        prio="high", market="both", mins=8,
        tags=["cache-invalidation", "ttl", "versioned-keys", "pubsub", "e-commerce"],
        ver="Redis Open Source 8.10", vs=False, status="stable",
        q_en=r"""On your e-commerce site, an admin changes a product's price, but customers keep seeing the old price for up to 10 minutes. The product is cached as `product:{id}`, and it also appears inside cached category pages and search results. How would you design cache invalidation?""",
        q_bn=r"""তোমার e-commerce site-এ admin একটা product-এর দাম বদলাল, কিন্তু customer-রা 10 মিনিট পর্যন্ত পুরনো দাম দেখছে। Product-টা `product:{id}` হিসেবে cache করা আছে, আবার cached category page আর search result-এর ভেতরেও আছে। Cache invalidation কীভাবে design করবে?""",
        a_en=r"""
            **1. Clarify freshness needs.** Price and stock must be fresh within seconds; descriptions and images can be minutes old. That decides where TTL alone is acceptable.

            **2. Options:**
            - **TTL only** — simple, but staleness equals the TTL (today's bug).
            - **Delete on write** — after the DB commit, `DEL product:v1:{id}`. Fixes the product page immediately.
            - **Versioned keys for aggregates** — category pages include a version: `category:{cid}:v{n}:page:{p}`. On any product change, `INCR catver:{cid}`; readers build the key with the new version, and old pages simply expire by TTL. No need to find and delete every page.
            - **Event-driven invalidation** — publish a `product.updated` event (ideally via a transactional outbox) so every service that caches product data invalidates its own keys.
            - **Split volatile fields** — cache the product body for longer, but read price/stock from a short-TTL key or the DB.

            **3. Recommendation:** delete-on-write for `product:{id}`, versioned keys for category and search pages, an outbox-driven event for other services, and keep a short TTL everywhere as a safety net. Monitor by sampling cached vs DB prices.
        """,
        a_bn=r"""
            **1. Freshness-এর প্রয়োজন পরিষ্কার করো।** দাম আর stock কয়েক সেকেন্ডের মধ্যে fresh হতে হবে; description আর ছবি কয়েক মিনিট পুরনো হলেও চলে। এটাই ঠিক করে কোথায় শুধু TTL যথেষ্ট।

            **2. Option-গুলো:**
            - **শুধু TTL** — সহজ, কিন্তু staleness TTL-এর সমান (আজকের bug-টাই এটা)।
            - **Write-এর সময় delete** — DB commit-এর পর `DEL product:v1:{id}`। Product page সাথে সাথে ঠিক হয়ে যায়।
            - **Aggregate-এর জন্য versioned key** — category page-এর key-তে version থাকে: `category:{cid}:v{n}:page:{p}`। কোনো product বদলালে `INCR catver:{cid}`; reader নতুন version দিয়ে key বানায়, আর পুরনো page-গুলো TTL-এ নিজে থেকেই expire হয়। প্রতিটা page খুঁজে delete করার দরকার নেই।
            - **Event-driven invalidation** — একটা `product.updated` event publish করো (সবচেয়ে ভালো transactional outbox দিয়ে), যাতে product data cache করা প্রতিটা service নিজের key invalidate করে।
            - **Volatile field আলাদা করো** — product-এর মূল অংশ বেশি সময় cache করো, কিন্তু price/stock পড়ো short-TTL key বা DB থেকে।

            **3. Recommendation:** `product:{id}`-এর জন্য delete-on-write, category আর search page-এর জন্য versioned key, অন্য service-এর জন্য outbox-চালিত event, আর safety net হিসেবে সব জায়গায় ছোট TTL। Cached দাম আর DB-র দাম sample করে মিলিয়ে monitor করো।
        """,
        ex_en=r"""
            - **Order matters:** write the DB first, then invalidate. Invalidating first lets a concurrent reader re-cache the old value before the DB commit.
            - **Why an outbox?** If the app commits to the DB and crashes before publishing the event, invalidation is lost. Writing the event into an outbox table in the same DB transaction, then relaying it, makes delivery reliable.
            - **Redis Pub/Sub for in-process caches:** if each Node instance also keeps a small in-memory LRU, broadcast invalidations with Pub/Sub. Pub/Sub is fire-and-forget, so keep TTLs as a backstop.
            - **Avoid pattern deletes:** "delete all `category:*`" with `KEYS` blocks Redis; versioned keys avoid it entirely.
            - **CDN layer:** if pages are also cached at a CDN, purge or use short `s-maxage` there too — otherwise Redis is fresh but users still see old HTML.
        """,
        ex_bn=r"""
            - **ক্রম গুরুত্বপূর্ণ:** আগে DB-তে লেখো, তারপর invalidate করো। আগে invalidate করলে একজন concurrent reader DB commit-এর আগেই পুরনো value আবার cache করে ফেলতে পারে।
            - **Outbox কেন?** App DB-তে commit করে event publish করার আগেই crash করলে invalidation হারিয়ে যায়। একই DB transaction-এ event-টা outbox table-এ লিখে পরে relay করলে delivery নির্ভরযোগ্য হয়।
            - **In-process cache-এর জন্য Redis Pub/Sub:** প্রতিটা Node instance যদি ছোট in-memory LRU-ও রাখে, Pub/Sub দিয়ে invalidation broadcast করো। Pub/Sub fire-and-forget, তাই backstop হিসেবে TTL রেখে দাও।
            - **Pattern delete এড়াও:** `KEYS` দিয়ে "সব `category:*` delete" করলে Redis block হয়; versioned key এই সমস্যা পুরোপুরি এড়ায়।
            - **CDN layer:** page যদি CDN-এও cache থাকে, সেখানেও purge করো বা ছোট `s-maxage` দাও — নইলে Redis fresh থাকলেও user পুরনো HTML দেখবে।
        """,
        tip_en=r"""Follow the scenario structure out loud: clarify freshness → list options → trade-offs → recommendation. Mentioning the DB-first-then-invalidate order and the outbox pattern stands out.""",
        tip_bn=r"""Scenario-র কাঠামো মেনে জোরে জোরে বলো: freshness পরিষ্কার করা → option → trade-off → recommendation। DB-আগে-তারপর-invalidate ক্রম আর outbox pattern উল্লেখ করলে উত্তরটা আলাদা হয়ে দাঁড়ায়।""",
        mist_en=r"""Answering only "reduce the TTL" (more DB load, still stale), or deleting keys with `KEYS category:*` in the request path.""",
        mist_bn=r"""শুধু "TTL কমিয়ে দাও" বলা (DB load বাড়ে, তবুও stale থাকে), অথবা request path-এ `KEYS category:*` দিয়ে key delete করা।""",
        code=r"""
            // Write path: after the DB transaction commits
            await redis.del(`product:v1:${productId}`);
            await redis.incr(`catver:${categoryId}`);          // bump listing version

            // Read path for a category page
            const ver = (await redis.get(`catver:${categoryId}`)) ?? '0';
            const pageKey = `category:${categoryId}:v${ver}:page:${page}`;
            const cached = await redis.get(pageKey);
            // ...on miss, build the page and SET it with a TTL; old versions expire on their own
        """,
        lang="javascript",
        follow=[
            ("What is the transactional outbox pattern and why does it help here?", "Transactional outbox pattern কী, আর এখানে এটা কীভাবে সাহায্য করে?"),
            ("How would you invalidate in-memory caches running inside 10 Node.js instances?", "10টা Node.js instance-এর ভেতরে চলা in-memory cache কীভাবে invalidate করবে?"),
        ],
        related=["redis-005", "redis-013", "redis-015"],
        refs=[R_SET, R_PUBSUB],
    ),
    # ------------------------------------------------------------------ redis-015
    Q(
        id="redis-015", sub="Pub/Sub vs Streams", diff="medium", type="comparison",
        prio="high", market="both", mins=7,
        tags=["pubsub", "streams", "lists", "queues", "consumer-groups"],
        ver="Redis Open Source 8.10", vs=False, status="stable",
        q_en=r"""Compare Redis Pub/Sub, Lists and Streams for passing messages between services. Which would you use for (a) live chat typing indicators, (b) a background email job queue, and (c) an order-events log consumed by several services?""",
        q_bn=r"""Service-গুলোর মধ্যে message পাঠানোর জন্য Redis Pub/Sub, List আর Stream তুলনা করো। (a) live chat-এর typing indicator, (b) background email job queue, আর (c) একাধিক service consume করবে এমন order-events log — কোনটার জন্য কী ব্যবহার করবে?""",
        a_en=r"""
            - **Pub/Sub:** push-based broadcast to whoever is subscribed *right now*. Nothing is stored — at-most-once delivery. If a subscriber is disconnected, it misses the message. Very low latency.
            - **Lists:** a simple queue (`LPUSH` + `BRPOP`). Each message goes to one consumer and stays until popped. Popping removes it, so a worker crash after `BRPOP` loses the job — the reliable variant is `BLMOVE` into a per-worker processing list, then remove it after success.
            - **Streams:** an append-only log with IDs. Messages persist (trim with `MAXLEN`), can be re-read, and **consumer groups** spread messages across workers with acknowledgements (`XACK`), a pending-entries list and re-claiming of stuck messages (`XAUTOCLAIM`) — at-least-once delivery.

            My choices: **(a) Pub/Sub** — typing indicators are ephemeral, so losing one is harmless. **(b) A Stream with a consumer group** (or a List with `BLMOVE` for something very simple; in Node, libraries like BullMQ build on Redis for this). **(c) A Stream** — each service gets its own consumer group, so every service sees every event independently and can replay after downtime.
        """,
        a_bn=r"""
            - **Pub/Sub:** push-based broadcast — শুধু *এই মুহূর্তে* যারা subscribe করে আছে তাদের কাছে যায়। কিছুই store হয় না — at-most-once delivery। Subscriber disconnected থাকলে message miss করে। Latency খুবই কম।
            - **List:** সাধারণ queue (`LPUSH` + `BRPOP`)। প্রতিটা message একজন consumer পায়, আর pop না হওয়া পর্যন্ত থেকে যায়। Pop করলেই মুছে যায়, তাই `BRPOP`-এর পর worker crash করলে job হারায় — নির্ভরযোগ্য উপায় হলো `BLMOVE` দিয়ে প্রতি-worker processing list-এ সরানো, সফল হলে তারপর মুছে ফেলা।
            - **Stream:** ID সহ append-only log। Message থেকে যায় (`MAXLEN` দিয়ে trim করা যায়), আবার পড়া যায়, আর **consumer group** acknowledgement (`XACK`), pending-entries list আর আটকে থাকা message re-claim (`XAUTOCLAIM`) সহ worker-দের মধ্যে message ভাগ করে দেয় — at-least-once delivery।

            আমার পছন্দ: **(a) Pub/Sub** — typing indicator ক্ষণস্থায়ী, একটা হারালে ক্ষতি নেই। **(b) Consumer group সহ Stream** (খুব সাধারণ কিছুর জন্য `BLMOVE` সহ List; Node-এ BullMQ-এর মতো library এই কাজে Redis-এর ওপর তৈরি)। **(c) Stream** — প্রতিটা service নিজস্ব consumer group পায়, তাই প্রতিটা service আলাদাভাবে প্রতিটা event দেখে আর downtime-এর পর replay করতে পারে।
        """,
        ex_en=r"""
            - **Delivery semantics:** Pub/Sub is at-most-once; Streams with consumer groups give at-least-once, so consumers must be **idempotent** (the same message can be delivered again after a crash).
            - **Fan-out vs work-sharing:** in Streams, *different* consumer groups each get every message (fan-out); consumers *within* one group share the work.
            - **Memory:** Streams grow until trimmed — use `XADD ... MAXLEN ~ 100000` or `XTRIM`. Lists grow if producers outpace workers.
            - **Connections:** a subscribed client (and a client blocked on `BRPOP`/`XREADGROUP BLOCK`) can't run other commands, so use a dedicated connection for it.
            - **Sharded Pub/Sub** (`SPUBLISH`/`SSUBSCRIBE`, Redis 7.0+) scales Pub/Sub in Redis Cluster by keeping messages within a shard.
            - **Not Kafka:** Streams are great for moderate volumes inside one Redis deployment; for very high-throughput, long-retention event pipelines a dedicated log (Kafka and similar) is usually a better fit.
        """,
        ex_bn=r"""
            - **Delivery semantics:** Pub/Sub at-most-once; consumer group সহ Stream at-least-once দেয়, তাই consumer-কে **idempotent** হতে হবে (crash-এর পর একই message আবার আসতে পারে)।
            - **Fan-out বনাম work-sharing:** Stream-এ *আলাদা আলাদা* consumer group প্রতিটা message পায় (fan-out); *একই* group-এর consumer-রা কাজ ভাগ করে নেয়।
            - **Memory:** Stream trim না করলে বাড়তেই থাকে — `XADD ... MAXLEN ~ 100000` বা `XTRIM` ব্যবহার করো। Producer worker-এর চেয়ে দ্রুত হলে List-ও বাড়ে।
            - **Connection:** subscribe করা client (আর `BRPOP`/`XREADGROUP BLOCK`-এ আটকে থাকা client) অন্য command চালাতে পারে না, তাই এর জন্য আলাদা connection ব্যবহার করো।
            - **Sharded Pub/Sub** (`SPUBLISH`/`SSUBSCRIBE`, Redis 7.0+) Redis Cluster-এ message-কে একটা shard-এর ভেতরে রেখে Pub/Sub scale করে।
            - **Kafka নয়:** একটা Redis deployment-এর ভেতরে মাঝারি volume-এর জন্য Stream দারুণ; খুব high-throughput আর দীর্ঘ retention-এর event pipeline-এর জন্য dedicated log (Kafka বা এরকম কিছু) সাধারণত বেশি উপযুক্ত।
        """,
        tip_en=r"""Anchor everything on delivery semantics (at-most-once vs at-least-once) and persistence. Then map each use case to a tool in one line — interviewers like decisive, justified choices.""",
        tip_bn=r"""সবকিছু delivery semantics (at-most-once বনাম at-least-once) আর persistence-এর ওপর দাঁড় করাও। তারপর প্রতিটা use case-কে এক লাইনে একটা tool-এর সাথে মেলাও — interviewer-রা দৃঢ়, যুক্তিসহ সিদ্ধান্ত পছন্দ করে।""",
        mist_en=r"""Using Pub/Sub as a job queue (jobs vanish when no worker is connected), or assuming Streams deliver exactly once.""",
        mist_bn=r"""Pub/Sub-কে job queue হিসেবে ব্যবহার করা (কোনো worker connected না থাকলে job উধাও হয়ে যায়), অথবা ধরে নেওয়া যে Stream exactly-once delivery দেয়।""",
        code=r"""
            # (a) Pub/Sub — ephemeral broadcast
            PUBLISH chat:room:12:typing "user:7"

            # (b) Reliable list queue — move the job instead of popping it
            LPUSH jobs:email '{"to":"a@example.com","template":"welcome"}'
            BLMOVE jobs:email jobs:email:processing:worker-1 RIGHT LEFT 5
            LREM jobs:email:processing:worker-1 1 '{"to":"a@example.com","template":"welcome"}'

            # (c) Stream + consumer groups — every service gets every event
            #     (create the groups first: "$" means "only events added from now on")
            XGROUP CREATE orders:events billing $ MKSTREAM
            XGROUP CREATE orders:events notifications $
            XADD orders:events MAXLEN ~ 100000 * type created orderId 981
            XREADGROUP GROUP billing worker-1 COUNT 10 BLOCK 5000 STREAMS orders:events >
            XACK orders:events billing 1728712345678-0
        """,
        lang="text",
        follow=[
            ("What happens to a stream message if the consumer crashes before `XACK`?", "`XACK`-এর আগে consumer crash করলে stream message-এর কী হয়?"),
            ("Why does a subscriber need its own Redis connection?", "Subscriber-এর নিজের আলাদা Redis connection কেন লাগে?"),
        ],
        related=["redis-009", "redis-021"],
        refs=[R_PUBSUB, R_STREAMS, R_BLMOVE],
    ),
    # ------------------------------------------------------------------ redis-016
    Q(
        id="redis-016", sub="Strings, Hashes, Lists, Sets, Sorted Sets", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["sorted-sets", "leaderboard", "zrange", "zadd"],
        ver="Redis Open Source 8.10 (ZRANGE REV since 6.2)", vs=True, status="stable",
        q_en=r"""A weekly leaderboard is stored with `ZADD lb:weekly <score> <player>`. Which command returns the **top 3 players with their scores, highest score first**?""",
        q_bn=r"""একটা weekly leaderboard `ZADD lb:weekly <score> <player>` দিয়ে রাখা আছে। কোন command **সবচেয়ে বেশি score আগে রেখে, score সহ top 3 player** return করবে?""",
        options=[
            ("`ZRANGE lb:weekly 0 2 WITHSCORES`", "`ZRANGE lb:weekly 0 2 WITHSCORES`"),
            ("`ZRANGE lb:weekly 0 2 REV WITHSCORES`", "`ZRANGE lb:weekly 0 2 REV WITHSCORES`"),
            ("`ZRANGE lb:weekly -3 -1 WITHSCORES`", "`ZRANGE lb:weekly -3 -1 WITHSCORES`"),
            ("`ZRANGEBYSCORE lb:weekly +inf -inf LIMIT 0 3`", "`ZRANGEBYSCORE lb:weekly +inf -inf LIMIT 0 3`"),
        ],
        correct=1,
        a_en=r"""`ZRANGE lb:weekly 0 2 REV WITHSCORES`. Sorted sets are ordered by ascending score; `REV` (Redis 6.2+) reverses the order so index 0 is the highest score.""",
        a_bn=r"""`ZRANGE lb:weekly 0 2 REV WITHSCORES`। Sorted set ascending score অনুযায়ী সাজানো থাকে; `REV` (Redis 6.2+) ক্রম উল্টে দেয়, ফলে index 0 হয় সবচেয়ে বেশি score।""",
        ex_en=r"""
            - **A** returns the *lowest* three scores.
            - **C** is the tempting one: it returns the right three players, but in ascending order — the third-best comes first. You'd have to reverse it in code.
            - **D** returns an empty result: `ZRANGEBYSCORE` expects `min max`, so `+inf -inf` matches nothing. (The reverse form would be `ZRANGE lb:weekly +inf -inf BYSCORE REV LIMIT 0 3`.)

            `ZREVRANGE` also works but is deprecated since 6.2 in favour of `ZRANGE ... REV`. Related leaderboard commands: `ZINCRBY` to add points atomically, `ZREVRANK` for a player's position, `ZSCORE` for their score. Reads are O(log N + M), so leaderboards with millions of players stay fast.
        """,
        ex_bn=r"""
            - **A** সবচেয়ে *কম* তিনটা score দেয়।
            - **C** সবচেয়ে বিভ্রান্তিকর: সঠিক তিনজন player-ই দেয়, কিন্তু ascending order-এ — তৃতীয় সেরা আগে আসে। Code-এ উল্টাতে হবে।
            - **D** খালি result দেয়: `ZRANGEBYSCORE` আশা করে `min max`, তাই `+inf -inf` কিছুই match করে না। (উল্টো রূপ হবে `ZRANGE lb:weekly +inf -inf BYSCORE REV LIMIT 0 3`।)

            `ZREVRANGE`-ও কাজ করে, কিন্তু 6.2 থেকে `ZRANGE ... REV`-এর পক্ষে deprecated। Leaderboard-এর অন্য command: atomically point যোগ করতে `ZINCRBY`, player-এর অবস্থান জানতে `ZREVRANK`, score জানতে `ZSCORE`। Read O(log N + M), তাই লাখো player-এর leaderboard-ও দ্রুত থাকে।
        """,
        tip_en=r"""Mention the unified `ZRANGE` syntax (`BYSCORE`, `BYLEX`, `REV`, `LIMIT`) from Redis 6.2 — it shows you're current, not relying on older command names.""",
        tip_bn=r"""Redis 6.2-এর unified `ZRANGE` syntax (`BYSCORE`, `BYLEX`, `REV`, `LIMIT`) উল্লেখ করো — এতে বোঝা যায় তুমি পুরনো command নামের ওপর নির্ভর না করে হালনাগাদ আছো।""",
        refs=[R_ZRANGE, R_ZSETS],
        related=["redis-003", "redis-024"],
    ),
    # ------------------------------------------------------------------ redis-024
    Q(
        id="redis-024", sub="Rate Limiting", diff="hard", type="coding",
        prio="high", market="both", mins=12,
        tags=["rate-limiting", "sliding-window", "lua", "sorted-sets", "token-bucket"],
        ver="Redis Open Source 8.10; node-redis 6.3", vs=True, status="stable",
        q_en=r"""
            The fixed-window limiter lets clients burst up to twice the limit around window boundaries. Implement a **sliding-window log** rate limiter in Redis that allows at most `limit` requests in any rolling `windowMs` period, using a sorted set and a Lua script for atomicity. Return `{ allowed, remaining, retryAfterMs }`.

            Example: `limit = 3`, `windowMs = 1000`. Five calls in quick succession return allowed, allowed, allowed, then two rejections with `retryAfterMs` just under 1000. After one second, calls are allowed again.
        """,
        q_bn=r"""
            Fixed-window limiter window boundary-র আশেপাশে client-কে limit-এর দ্বিগুণ পর্যন্ত burst করতে দেয়। Redis-এ একটা **sliding-window log** rate limiter implement করো, যেটা যেকোনো চলমান `windowMs` সময়ের মধ্যে সর্বোচ্চ `limit`টা request অনুমতি দেবে — atomicity-র জন্য sorted set আর Lua script ব্যবহার করে। Return করবে `{ allowed, remaining, retryAfterMs }`।

            উদাহরণ: `limit = 3`, `windowMs = 1000`। পরপর পাঁচটা call-এ ফল হবে allowed, allowed, allowed, তারপর দুইটা rejection, যেখানে `retryAfterMs` 1000-এর একটু কম। এক সেকেন্ড পরে আবার allowed হবে।
        """,
        a_en=r"""
            Each client gets a sorted set where every request is a member scored by its timestamp in milliseconds. In one Lua script I:
            1. Read the server time with `TIME` (so app servers' clock skew doesn't matter).
            2. `ZREMRANGEBYSCORE` to drop entries older than `now - windowMs`.
            3. `ZCARD` to count what's left.
            4. If below the limit, `ZADD` the current request with a unique member and `PEXPIRE` the key; otherwise compute `retryAfterMs` from the oldest entry.

            Running this as a Lua script makes the check-and-add atomic — two concurrent requests can't both see "2 of 3" and both get in. The key expires on its own when a client goes quiet.
        """,
        a_bn=r"""
            প্রতিটা client-এর জন্য একটা sorted set থাকে, যেখানে প্রতিটা request একটা member আর তার score হলো millisecond-এ timestamp। একটা Lua script-এর ভেতরে আমি:
            1. `TIME` দিয়ে server-এর সময় পড়ি (তাই app server-গুলোর clock skew কোনো সমস্যা করে না)।
            2. `ZREMRANGEBYSCORE` দিয়ে `now - windowMs`-এর চেয়ে পুরনো entry মুছে দিই।
            3. `ZCARD` দিয়ে বাকি entry গুনি।
            4. Limit-এর নিচে থাকলে unique member দিয়ে বর্তমান request `ZADD` করি আর key-তে `PEXPIRE` দিই; না হলে সবচেয়ে পুরনো entry থেকে `retryAfterMs` হিসাব করি।

            পুরোটা Lua script হিসেবে চালানোয় check-and-add atomic হয় — দুইটা concurrent request দুজনেই "3-এর মধ্যে 2" দেখে একসাথে ঢুকে পড়তে পারে না। Client চুপ হয়ে গেলে key নিজে থেকেই expire হয়।
        """,
        ex_en=r"""
            - **Why Lua and not `MULTI`?** `MULTI` can't branch on an intermediate result (count < limit). A script runs atomically and can make decisions.
            - **Unique members:** if two requests share a timestamp and you use the timestamp as the member, `ZADD` overwrites instead of adding. Use a request id (UUID).
            - **Memory trade-off:** the log stores one entry per allowed request — up to `limit` entries per client. For large limits (10,000/min) use a **sliding-window counter** (weighted current + previous fixed-window counts) or a **token bucket** (store `tokens` and `lastRefill` in a hash, refill by elapsed time in Lua) — both are O(1) memory.
            - **Script performance:** avoid sending the script text on every call; node-redis's `defineScript` runs it via `EVALSHA` and falls back to `EVAL` on `NOSCRIPT`.
            - **Cluster:** the script touches one key, so it works in Redis Cluster as long as the key is passed in `KEYS`.
            - **Rejected requests aren't recorded**, so a client hammering the API doesn't extend its own ban — decide whether that's the policy you want.
        """,
        ex_bn=r"""
            - **`MULTI` নয়, Lua কেন?** `MULTI` মাঝের কোনো result (count < limit)-এর ওপর ভিত্তি করে branch করতে পারে না। Script atomically চলে আর সিদ্ধান্ত নিতে পারে।
            - **Unique member:** দুইটা request-এর timestamp একই হলে আর timestamp-কেই member বানালে `ZADD` নতুন যোগ না করে overwrite করে। Request id (UUID) ব্যবহার করো।
            - **Memory trade-off:** log প্রতিটা allowed request-এর জন্য একটা entry রাখে — প্রতি client-এ সর্বোচ্চ `limit`টা। বড় limit-এর (প্রতি মিনিটে 10,000) জন্য **sliding-window counter** (বর্তমান আর আগের fixed-window count-এর weighted যোগফল) বা **token bucket** (hash-এ `tokens` আর `lastRefill` রেখে Lua-তে elapsed time অনুযায়ী refill) ব্যবহার করো — দুটোই O(1) memory।
            - **Script performance:** প্রতিটা call-এ script-এর পুরো text পাঠিও না; node-redis-এর `defineScript` এটা `EVALSHA` দিয়ে চালায় আর `NOSCRIPT` হলে `EVAL`-এ fallback করে।
            - **Cluster:** script একটাই key ছোঁয়, তাই key `KEYS`-এ পাঠালে Redis Cluster-এও কাজ করে।
            - **Reject হওয়া request record হয় না**, তাই যে client API-তে বারবার আঘাত করছে সে নিজের ban বাড়ায় না — এটা তোমার কাঙ্ক্ষিত policy কিনা ঠিক করে নাও।
        """,
        tip_en=r"""Start by naming the fixed-window boundary problem, then explain why the check must be atomic, then write the script. Close by comparing memory use with the token bucket — that's the senior-level trade-off.""",
        tip_bn=r"""শুরুতে fixed-window-এর boundary সমস্যার নাম বলো, তারপর ব্যাখ্যা করো check কেন atomic হতে হবে, তারপর script লেখো। শেষে token bucket-এর সাথে memory ব্যবহারের তুলনা করো — এটাই senior-level trade-off।""",
        mist_en=r"""Doing `ZCARD` and `ZADD` as separate commands from Node (race condition), using the timestamp as the member, or forgetting the expiry so idle clients' sets live forever.""",
        mist_bn=r"""Node থেকে `ZCARD` আর `ZADD` আলাদা command হিসেবে চালানো (race condition), timestamp-কেই member বানানো, অথবা expiry ভুলে যাওয়া — ফলে idle client-এর set চিরকাল থেকে যায়।""",
        code=r"""
            import { randomUUID } from 'node:crypto';

            const SLIDING_WINDOW_LUA = `
            local key      = KEYS[1]
            local windowMs = tonumber(ARGV[1])
            local limit    = tonumber(ARGV[2])
            local member   = ARGV[3]

            local t   = redis.call('TIME')
            local now = tonumber(t[1]) * 1000 + math.floor(tonumber(t[2]) / 1000)

            redis.call('ZREMRANGEBYSCORE', key, 0, now - windowMs)
            local count = redis.call('ZCARD', key)

            if count < limit then
              redis.call('ZADD', key, now, member)
              redis.call('PEXPIRE', key, windowMs)
              return {1, limit - count - 1, 0}
            end

            local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
            return {0, 0, tonumber(oldest[2]) + windowMs - now}
            `;

            export async function slidingWindowAllow(redis, clientId, { limit = 100, windowMs = 60_000 } = {}) {
              const [allowed, remaining, retryAfterMs] = await redis.eval(SLIDING_WINDOW_LUA, {
                keys: [`rl:sw:${clientId}`],
                arguments: [String(windowMs), String(limit), randomUUID()],
              });
              return { allowed: allowed === 1, remaining, retryAfterMs };
            }
        """,
        lang="javascript",
        output=r"""
            // limit = 3, windowMs = 1000, five quick calls (retryAfterMs varies by a few ms per run):
            { allowed: true, remaining: 2, retryAfterMs: 0 }
            { allowed: true, remaining: 1, retryAfterMs: 0 }
            { allowed: true, remaining: 0, retryAfterMs: 0 }
            { allowed: false, remaining: 0, retryAfterMs: 996 }
            { allowed: false, remaining: 0, retryAfterMs: 995 }
            // ~1.1 s later:
            { allowed: true, remaining: 2, retryAfterMs: 0 }
        """,
        time="O(log N) per request (N = entries in the window, at most limit)", space="O(limit) per active client",
        follow=[
            ("Implement a token bucket in Lua. What do you store in Redis?", "Lua-তে একটা token bucket implement করো। Redis-এ কী কী store করবে?"),
            ("How would you apply different limits for free and paid API keys?", "Free আর paid API key-এর জন্য আলাদা limit কীভাবে প্রয়োগ করবে?"),
            ("Why use the Redis server's `TIME` instead of `Date.now()` from Node?", "Node-এর `Date.now()`-এর বদলে Redis server-এর `TIME` কেন ব্যবহার করা?"),
        ],
        related=["redis-012", "redis-016"],
        refs=[R_LUA, R_INCR, R_ZSETS],
    ),
    # ------------------------------------------------------------------ redis-025
    Q(
        id="redis-025", sub="Distributed Locks & Limitations", diff="hard", type="debugging",
        prio="high", market="both", mins=10,
        tags=["distributed-lock", "setnx", "lua", "delex", "debugging"],
        ver="Redis Open Source 8.10 (DELEX since 8.4); node-redis 6.3", vs=True, status="stable",
        q_en=r"""This helper is used to make sure only one instance runs the nightly invoice job. Occasionally the job never runs again until someone deletes the key by hand, and once two instances ran it at the same time. Find the bugs and fix the helper.""",
        q_bn=r"""এই helper ব্যবহার করা হয় যাতে nightly invoice job শুধু একটা instance চালায়। মাঝে মাঝে কেউ হাতে key delete না করা পর্যন্ত job আর কখনো চলে না, আর একবার দুইটা instance একসাথে এটা চালিয়েছে। Bug-গুলো খুঁজে helper-টা ঠিক করো।""",
        a_en=r"""
            1. **`SETNX` + `EXPIRE` are two commands.** If the process crashes or the connection drops between them, the lock has no TTL and is held forever — that's the "job never runs again" bug. Acquire with one atomic command: `SET key token NX PX ttl`.
            2. **The value is the constant `'1'`,** so the lock has no owner identity.
            3. **`DEL` in `finally` can delete someone else's lock.** If the job takes longer than 10 seconds, the lock expires, instance B acquires it, and then A's `finally` deletes B's lock — letting instance C in as well. That's the "two instances at once" bug (plus the TTL being shorter than the job).
            4. **TTL shorter than the work:** pick a TTL comfortably above the job's duration, or extend it while working.

            The fix: a random token per acquisition, atomic `SET ... NX PX`, and release with **compare-and-delete** — `DELEX key IFEQ token` on Redis 8.4+, or a small Lua script on older versions — so you only ever delete your own lock.
        """,
        a_bn=r"""
            1. **`SETNX` + `EXPIRE` দুইটা আলাদা command।** মাঝখানে process crash করলে বা connection কেটে গেলে lock-এর কোনো TTL থাকে না আর চিরকাল ধরা থাকে — এটাই "job আর কখনো চলে না" bug। একটা atomic command দিয়ে নাও: `SET key token NX PX ttl`।
            2. **Value হলো constant `'1'`,** তাই lock-এর কোনো মালিক-পরিচয় নেই।
            3. **`finally`-এর `DEL` অন্যের lock মুছে দিতে পারে।** Job 10 সেকেন্ডের বেশি নিলে lock expire হয়, instance B সেটা নেয়, তারপর A-র `finally` B-র lock মুছে দেয় — ফলে instance C-ও ঢুকে পড়ে। এটাই "একসাথে দুইটা instance" bug (সাথে TTL job-এর চেয়ে ছোট হওয়া)।
            4. **কাজের চেয়ে TTL ছোট:** job-এর সময়ের চেয়ে যথেষ্ট বড় TTL দাও, অথবা কাজ চলাকালীন TTL বাড়াও।

            সমাধান: প্রতিবার lock নেওয়ার সময় random token, atomic `SET ... NX PX`, আর **compare-and-delete** দিয়ে release — Redis 8.4+-এ `DELEX key IFEQ token`, পুরনো version-এ ছোট একটা Lua script — যাতে তুমি শুধু নিজের lock-ই মুছতে পারো।
        """,
        ex_en=r"""
            - **Why compare-and-delete must be atomic:** doing `GET` then `DEL` from Node has the same race — the lock can expire and be re-acquired between your two commands. Lua (or `DELEX`) runs both steps inside Redis.
            - **`SETNX` is a legacy command:** the docs treat it as deprecated in favour of `SET` with `NX`.
            - **Waiting:** instead of failing immediately, retry with a short backoff plus jitter and a deadline.
            - **Still a lease:** even the fixed version can't protect against a process that pauses longer than the TTL. For a nightly job that's acceptable if the job is idempotent (e.g. "create invoice if not exists" with a unique constraint). For money movement, add fencing tokens or DB-level guarantees.
            - **Redis 8.4+ note:** besides `DELEX`, `SET` also gained `IFEQ`, useful to *extend* a lock only if you still own it.
        """,
        ex_bn=r"""
            - **Compare-and-delete কেন atomic হতে হবে:** Node থেকে `GET` তারপর `DEL` করলে একই race থাকে — দুই command-এর মাঝখানে lock expire হয়ে অন্য কেউ নিয়ে নিতে পারে। Lua (বা `DELEX`) দুটো ধাপই Redis-এর ভেতরে চালায়।
            - **`SETNX` একটা legacy command:** docs এটাকে `NX` সহ `SET`-এর পক্ষে deprecated হিসেবে দেখায়।
            - **অপেক্ষা:** সাথে সাথে fail না করে ছোট backoff আর jitter সহ deadline পর্যন্ত retry করো।
            - **তবুও এটা lease:** ঠিক করা version-ও এমন process থেকে রক্ষা করতে পারে না যেটা TTL-এর চেয়ে বেশি সময় থেমে থাকে। Nightly job idempotent হলে (যেমন unique constraint সহ "invoice না থাকলে তৈরি করো") এটা গ্রহণযোগ্য। টাকা লেনদেনের ক্ষেত্রে fencing token বা DB-level guarantee যোগ করো।
            - **Redis 8.4+ note:** `DELEX`-এর পাশাপাশি `SET`-এও `IFEQ` এসেছে — শুধু নিজের lock থাকলেই সেটা *extend* করতে কাজে লাগে।
        """,
        tip_en=r"""Explain each bug as a timeline ("A acquires, A pauses 12 s, lock expires, B acquires, A deletes B's lock"). Timelines make concurrency bugs easy for the interviewer to follow.""",
        tip_bn=r"""প্রতিটা bug একটা timeline হিসেবে বলো ("A lock নিল, A 12 সেকেন্ড থেমে থাকল, lock expire হলো, B নিল, A B-র lock মুছে দিল")। Timeline দিলে concurrency bug interviewer-এর পক্ষে সহজে বোঝা যায়।""",
        mist_en=r"""Fixing only the atomic acquire and still releasing with plain `DEL`, or doing the ownership check with a separate `GET` before `DEL`.""",
        mist_bn=r"""শুধু atomic acquire ঠিক করে release-এ এখনো সাধারণ `DEL` রাখা, অথবা `DEL`-এর আগে আলাদা `GET` দিয়ে মালিকানা check করা।""",
        code=r"""
            export async function withLock(redis, name, fn) {
              const acquired = await redis.setNX(`lock:${name}`, '1');
              if (!acquired) throw new Error('locked');
              await redis.expire(`lock:${name}`, 10);
              try {
                return await fn();
              } finally {
                await redis.del(`lock:${name}`);
              }
            }
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            import { randomUUID } from 'node:crypto';
            import { setTimeout as sleep } from 'node:timers/promises';

            // Compare-and-delete for Redis < 8.4 (on 8.4+: DELEX key IFEQ token)
            const RELEASE_LUA = `
            if redis.call('GET', KEYS[1]) == ARGV[1] then
              return redis.call('DEL', KEYS[1])
            end
            return 0`;

            export async function withLock(redis, name, fn, { ttlMs = 15 * 60_000, waitMs = 2_000 } = {}) {
              const key = `lock:${name}`;
              const token = randomUUID();
              const deadline = Date.now() + waitMs;

              // One atomic command: set only if absent, with an expiry
              while (!(await redis.set(key, token, {
                condition: 'NX',
                expiration: { type: 'PX', value: ttlMs },
              }))) {
                if (Date.now() > deadline) throw new Error(`Could not acquire ${key}`);
                await sleep(50 + Math.random() * 50); // backoff + jitter
              }

              try {
                return await fn();
              } finally {
                await redis.eval(RELEASE_LUA, { keys: [key], arguments: [token] });
              }
            }
        """)],
        follow=[
            ("How would you extend the lock safely while a long job is still running?", "লম্বা job চলার সময় lock নিরাপদে extend কীভাবে করবে?"),
            ("Why isn't `GET` followed by `DEL` from Node.js good enough for release?", "Release-এর জন্য Node.js থেকে `GET`-এর পর `DEL` কেন যথেষ্ট নয়?"),
        ],
        related=["redis-030", "redis-023"],
        refs=[R_LOCKS, R_DELEX, R_SET],
    ),
]

if __name__ == "__main__":
    save("redis", "b2", QUESTIONS)
