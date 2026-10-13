# Redis — batch 4 (redis-010, 011, 020, 021, 022, 028, 029, 032)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_LICENSE = ("Redis — Licenses", "https://redis.io/legal/licenses/")
R_VSETS = ("Redis docs — Vector sets", "https://redis.io/docs/latest/develop/data-types/vector-sets/")
VALKEY = ("Valkey — project site", "https://valkey.io/")
R_TYPES = ("Redis docs — Data types", "https://redis.io/docs/latest/develop/data-types/")
R_PERSIST = ("Redis docs — Persistence", "https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/")
R_SET = ("Redis docs — SET", "https://redis.io/docs/latest/commands/set/")
R_INCR = ("Redis docs — INCR", "https://redis.io/docs/latest/commands/incr/")
R_EXPIRE = ("Redis docs — EXPIRE", "https://redis.io/docs/latest/commands/expire/")
R_STREAMS = ("Redis docs — Streams", "https://redis.io/docs/latest/develop/data-types/streams/")
R_XREADGROUP = ("Redis docs — XREADGROUP", "https://redis.io/docs/latest/commands/xreadgroup/")
R_XAUTOCLAIM = ("Redis docs — XAUTOCLAIM", "https://redis.io/docs/latest/commands/xautoclaim/")
R_CLUSTER = ("Redis docs — Scale with Redis Cluster", "https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/")
R_CLUSTER_SPEC = ("Redis docs — Cluster specification", "https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/")
R_SENTINEL = ("Redis docs — High availability with Sentinel", "https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/")
R_TX = ("Redis docs — Transactions", "https://redis.io/docs/latest/develop/using-commands/transactions/")
R_LUA = ("Redis docs — Scripting with Lua", "https://redis.io/docs/latest/develop/programmability/eval-intro/")
R_LATENCY = ("Redis docs — Diagnosing latency issues", "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/")
R_UNLINK = ("Redis docs — UNLINK", "https://redis.io/docs/latest/commands/unlink/")
R_NODE = ("Redis docs — node-redis guide", "https://redis.io/docs/latest/develop/clients/nodejs/")

QUESTIONS = [
    # ------------------------------------------------------------------ redis-010
    Q(
        id="redis-010", sub="Redis 8, Licensing & Valkey", diff="easy", type="conceptual",
        prio="low", market="both", mins=3,
        tags=["redis-8", "licensing", "valkey", "agpl", "vector-sets"],
        ver="Redis Open Source 8.10", vs=True, status="stable",
        q_en=r"""What changed with Redis 8 ("Redis Open Source"), and what is Valkey? Why might this matter when your team picks a managed Redis-compatible service?""",
        q_bn=r"""Redis 8 ("Redis Open Source")-এ কী বদলেছে, আর Valkey কী? তোমার team যখন managed Redis-compatible service বেছে নেয়, তখন এটা কেন গুরুত্বপূর্ণ হতে পারে?""",
        a_en=r"""
            A short history:
            - Redis up to **7.2** was BSD-licensed.
            - With **7.4** (2024), Redis switched to a dual source-available licence (RSALv2 / SSPLv1). In response, the Linux Foundation started **Valkey**, a BSD-licensed fork of Redis 7.2.4, backed by several cloud vendors.
            - **Redis 8** (2025) added **AGPLv3**, an OSI-approved open-source licence, as a third option and rebranded the project as **Redis Open Source**. It also bundles what used to be separate modules — JSON, the Query Engine (search and vector search), time series and probabilistic types — and adds a new **Vector Sets** data type.

            For a typical Node.js app using core commands through node-redis or ioredis, Redis and Valkey behave the same. Differences show up with newer features (Redis 8 Query Engine, Vector Sets, recent commands), so check that your provider supports what you use. Licensing mainly matters if you modify and redistribute Redis or offer it as a service — that's a question for your legal team, not a reason to panic.
        """,
        a_bn=r"""
            সংক্ষিপ্ত ইতিহাস:
            - **7.2** পর্যন্ত Redis ছিল BSD-licensed।
            - **7.4**-এ (2024) Redis একটা dual source-available licence-এ (RSALv2 / SSPLv1) চলে যায়। এর জবাবে Linux Foundation শুরু করে **Valkey** — Redis 7.2.4-এর একটা BSD-licensed fork, যার পেছনে বেশ কয়েকটা cloud vendor আছে।
            - **Redis 8** (2025) তৃতীয় option হিসেবে **AGPLv3** যোগ করে, যেটা OSI-approved open-source licence, আর project-এর নাম হয় **Redis Open Source**। আগে যেগুলো আলাদা module ছিল — JSON, Query Engine (search ও vector search), time series আর probabilistic type — সেগুলো এখন built-in, সাথে নতুন **Vector Sets** data type।

            node-redis বা ioredis দিয়ে core command ব্যবহার করা সাধারণ Node.js app-এ Redis আর Valkey একই রকম আচরণ করে। পার্থক্য দেখা যায় নতুন feature-এ (Redis 8 Query Engine, Vector Sets, সাম্প্রতিক command), তাই তুমি যা ব্যবহার করো provider সেটা support করে কিনা দেখে নাও। Licensing মূলত গুরুত্বপূর্ণ যদি তুমি Redis modify করে redistribute করো বা service হিসেবে দাও — সেটা legal team-এর প্রশ্ন, আতঙ্কিত হওয়ার কারণ নয়।
        """,
        ex_en=r"""
            - **Vector Sets** (Redis 8.0+) store elements with vectors and answer similarity queries (`VADD`, `VSIM`), using an HNSW graph with quantisation by default — handy for small semantic-search features without a separate vector database.
            - **Release lines:** Redis 8.2 is an extended-support line, and 8.10 is the current stable release.
            - **Interview angle:** you're not expected to be a lawyer; showing that you know *why* Valkey exists and that features may diverge is enough.
        """,
        ex_bn=r"""
            - **Vector Sets** (Redis 8.0+) vector সহ element রাখে আর similarity query-র উত্তর দেয় (`VADD`, `VSIM`), default-এ quantisation সহ HNSW graph ব্যবহার করে — আলাদা vector database ছাড়াই ছোট semantic-search feature-এর জন্য কাজের।
            - **Release line:** Redis 8.2 একটা extended-support line, আর 8.10 বর্তমান stable release।
            - **Interview-এর দৃষ্টিকোণ:** তোমার কাছে আইনজীবীর মতো উত্তর আশা করা হয় না; Valkey *কেন* তৈরি হলো আর feature যে আলাদা হয়ে যেতে পারে — এটুকু জানলেই যথেষ্ট।
        """,
        tip_en=r"""Keep it factual and neutral — a 30-second timeline plus the practical takeaway ("check feature support of your provider"). Avoid strong opinions on licensing politics in an interview.""",
        tip_bn=r"""তথ্যভিত্তিক আর নিরপেক্ষ থাকো — 30 সেকেন্ডের একটা timeline আর বাস্তব শিক্ষা ("provider-এর feature support দেখে নাও")। Interview-এ licensing রাজনীতি নিয়ে জোরালো মত এড়িয়ে চলো।""",
        mist_en=r"""Saying "Redis is no longer open source" (Redis 8 offers AGPLv3), or assuming Valkey and Redis 8 support exactly the same newest commands.""",
        mist_bn=r""""Redis আর open source নয়" বলা (Redis 8 AGPLv3 option দেয়), অথবা ধরে নেওয়া যে Valkey আর Redis 8 হুবহু একই নতুন command support করে।""",
        code=r"""
            # Redis 8 Vector Sets: tiny semantic-similarity example
            VADD products VALUES 3 0.9 0.1 0.0 sku:saree-red
            VADD products VALUES 3 0.2 0.9 0.1 sku:panjabi
            VSIM products VALUES 3 1.0 0.0 0.0 COUNT 1
        """,
        lang="text",
        follow=[
            ("What are Vector Sets and when would you use them instead of a vector database?", "Vector Sets কী, আর কখন vector database-এর বদলে এগুলো ব্যবহার করবে?"),
            ("How would you check that a managed Redis/Valkey service supports the commands your app uses?", "Managed Redis/Valkey service তোমার app-এর ব্যবহার করা command support করে কিনা কীভাবে check করবে?"),
        ],
        related=["redis-001", "redis-011"],
        refs=[R_LICENSE, R_VSETS, VALKEY],
    ),
    # ------------------------------------------------------------------ redis-011
    Q(
        id="redis-011", sub="Redis vs Memcached", diff="easy", type="comparison",
        prio="medium", market="both", mins=3,
        tags=["memcached", "caching", "comparison", "data-types"],
        ver="Redis Open Source 8.10", vs=False, status="stable",
        q_en=r"""Redis vs Memcached: what are the main differences, and when would you still choose Memcached?""",
        q_bn=r"""Redis বনাম Memcached: প্রধান পার্থক্যগুলো কী, আর কখন তুমি এখনো Memcached বেছে নেবে?""",
        a_en=r"""
            - **Data model:** Memcached stores opaque strings (blobs). Redis has rich types — hashes, lists, sets, sorted sets, streams, JSON — with atomic server-side operations on them.
            - **Persistence & HA:** Memcached is purely in-memory, with no persistence or built-in replication. Redis offers RDB/AOF persistence, replicas, Sentinel and Cluster.
            - **Threading:** Memcached is multi-threaded and scales across cores for simple get/set. Redis executes commands on one thread (plus I/O threads), and scales out with Cluster.
            - **Features:** Redis adds Pub/Sub, Streams, Lua scripting, transactions, configurable eviction policies and TTLs on hash fields. Memcached keeps things deliberately minimal.
            - **Value size:** Memcached's default item size limit is 1 MB (configurable); Redis strings can be up to 512 MB.

            I'd pick Memcached only for a very simple, huge, multi-core string cache where nothing else is needed and the team already runs it. For almost any new Node.js project, Redis covers caching plus sessions, rate limiting and queues with one tool.
        """,
        a_bn=r"""
            - **Data model:** Memcached opaque string (blob) রাখে। Redis-এ আছে rich type — hash, list, set, sorted set, stream, JSON — আর সেগুলোর ওপর server-side atomic operation।
            - **Persistence ও HA:** Memcached পুরোপুরি in-memory, কোনো persistence বা built-in replication নেই। Redis-এ আছে RDB/AOF persistence, replica, Sentinel আর Cluster।
            - **Threading:** Memcached multi-threaded, সাধারণ get/set-এ একাধিক core জুড়ে scale করে। Redis এক thread-এ command চালায় (সাথে I/O thread), আর Cluster দিয়ে scale out করে।
            - **Feature:** Redis-এ বাড়তি আছে Pub/Sub, Streams, Lua scripting, transaction, configurable eviction policy আর hash field-এ TTL। Memcached ইচ্ছা করেই minimal।
            - **Value size:** Memcached-এর default item size limit 1 MB (configure করা যায়); Redis string 512 MB পর্যন্ত হতে পারে।

            আমি Memcached বেছে নেব শুধু খুব সাধারণ, বিশাল, multi-core string cache-এর জন্য, যেখানে আর কিছু লাগবে না আর team আগে থেকেই এটা চালায়। প্রায় যেকোনো নতুন Node.js project-এ Redis একটা tool দিয়েই caching, session, rate limiting আর queue সামলে নেয়।
        """,
        ex_en=r"""
            - **Operational simplicity** is Memcached's real strength: no persistence to tune, no data-structure misuse, predictable memory (slab allocator).
            - **Consistency of comparison:** both are cache-first tools; neither replaces a primary database for relational data.
            - **Managed options:** cloud providers offer both engines as managed caches, so the decision is usually about features, not hosting.
        """,
        ex_bn=r"""
            - **Operational সরলতা**-ই Memcached-এর আসল শক্তি: tune করার মতো persistence নেই, data structure-এর অপব্যবহারের সুযোগ নেই, memory অনুমানযোগ্য (slab allocator)।
            - **তুলনার ভারসাম্য:** দুটোই মূলত cache tool; কোনোটাই relational data-র জন্য primary database-এর বিকল্প নয়।
            - **Managed option:** cloud provider-রা দুটো engine-ই managed cache হিসেবে দেয়, তাই সিদ্ধান্ত সাধারণত hosting নয়, feature-এর ওপর নির্ভর করে।
        """,
        tip_en=r"""Present it as a small table in words (data model, persistence, threading, features), then give a clear recommendation with one exception. Balanced answers sound more senior than "Redis is just better".""",
        tip_bn=r"""কথায় একটা ছোট table-এর মতো সাজাও (data model, persistence, threading, feature), তারপর একটা ব্যতিক্রম সহ স্পষ্ট recommendation দাও। "Redis সবসময় ভালো" বলার চেয়ে ভারসাম্যপূর্ণ উত্তর বেশি senior শোনায়।""",
        mist_en=r"""Claiming Memcached is "obsolete" or that Redis is "multi-threaded like Memcached".""",
        mist_bn=r"""Memcached-কে "অচল" বলা, অথবা দাবি করা যে Redis-ও "Memcached-এর মতো multi-threaded"।""",
        follow=[
            ("How does Memcached distribute keys across multiple servers?", "Memcached একাধিক server-এ key কীভাবে ভাগ করে?"),
            ("Why can a single Redis instance still handle very high throughput on one thread?", "এক thread-এ চলেও একটা Redis instance কীভাবে খুব high throughput সামলাতে পারে?"),
        ],
        related=["redis-001", "redis-006"],
        refs=[R_TYPES, R_PERSIST],
    ),
    # ------------------------------------------------------------------ redis-020
    Q(
        id="redis-020", sub="Key-Value Fundamentals", diff="medium", type="output",
        prio="medium", market="bangladesh", mins=5,
        tags=["output", "redis-cli", "ttl", "incr", "nx"],
        ver="Version-independent (Redis Open Source 8.10)", vs=False, status="stable",
        q_en=r"""What does `redis-cli` print for each of these commands, run in order on an empty database?""",
        q_bn=r"""খালি database-এ ক্রমানুসারে এই command-গুলো চালালে প্রতিটার জন্য `redis-cli` কী print করবে?""",
        a_en=r"""
            1. `OK` 2. `(integer) 7` 3. `(integer) 1` 4. `(nil)` 5. `"7"` 6. `OK` 7. `(error) ERR value is not an integer or out of range` 8. `(integer) 0` 9. `OK` 10. `(integer) 1` 11. `(integer) -1` 12. `(integer) -2`

            The traps are `SET ... NX` on an existing key (nil, no change), `INCR` on a non-numeric string (error), `EXPIRE` on a missing key (0), and the two special `TTL` values: `-1` = no expiry, `-2` = key doesn't exist.
        """,
        a_bn=r"""
            1. `OK` 2. `(integer) 7` 3. `(integer) 1` 4. `(nil)` 5. `"7"` 6. `OK` 7. `(error) ERR value is not an integer or out of range` 8. `(integer) 0` 9. `OK` 10. `(integer) 1` 11. `(integer) -1` 12. `(integer) -2`

            ফাঁদগুলো হলো: আগে থেকে থাকা key-এ `SET ... NX` (nil, কোনো পরিবর্তন নেই), non-numeric string-এ `INCR` (error), না-থাকা key-এ `EXPIRE` (0), আর `TTL`-এর দুইটা বিশেষ value: `-1` = expiry নেই, `-2` = key-ই নেই।
        """,
        ex_en=r"""
            1. `SET stock:42 10` → `OK`.
            2. `DECRBY stock:42 3` → 10 − 3 = `7` (integers are stored as strings but parsed for arithmetic).
            3. `INCR page:views` → the key doesn't exist, so it's treated as 0 → `1`.
            4. `SET stock:42 99 NX` → `NX` means "only if not exists"; the key exists, so nothing is written and the reply is `(nil)`.
            5. `GET stock:42` → still `"7"` (GET returns a bulk string, hence the quotes).
            6. `SET user:1:name "Rahim"` → `OK`.
            7. `INCR user:1:name` → "Rahim" isn't an integer → error; the value is unchanged.
            8. `EXPIRE missing:key 60` → returns `0` because there's no such key.
            9. `SET otp:017 "4821" EX 120` → `OK` with a 120-second TTL.
            10. `PERSIST otp:017` → removes the TTL, returns `1`.
            11. `TTL otp:017` → `-1`: exists, no expiry.
            12. `TTL missing:key` → `-2`: doesn't exist.
        """,
        ex_bn=r"""
            1. `SET stock:42 10` → `OK`।
            2. `DECRBY stock:42 3` → 10 − 3 = `7` (integer string হিসেবে store হয়, কিন্তু হিসাবের সময় parse করা হয়)।
            3. `INCR page:views` → key নেই, তাই 0 ধরে → `1`।
            4. `SET stock:42 99 NX` → `NX` মানে "না থাকলেই শুধু"; key আছে, তাই কিছু লেখা হয় না, reply `(nil)`।
            5. `GET stock:42` → এখনো `"7"` (GET bulk string দেয়, তাই quote)।
            6. `SET user:1:name "Rahim"` → `OK`।
            7. `INCR user:1:name` → "Rahim" integer নয় → error; value অপরিবর্তিত।
            8. `EXPIRE missing:key 60` → key নেই বলে `0` return করে।
            9. `SET otp:017 "4821" EX 120` → 120 সেকেন্ড TTL সহ `OK`।
            10. `PERSIST otp:017` → TTL সরিয়ে দেয়, return করে `1`।
            11. `TTL otp:017` → `-1`: key আছে, expiry নেই।
            12. `TTL missing:key` → `-2`: key নেই।
        """,
        tip_en=r"""Trace line by line and say the *state* after each command (value + TTL), not just the reply. That habit prevents mistakes on longer sequences.""",
        tip_bn=r"""লাইন ধরে ধরে trace করো, আর প্রতিটা command-এর পর শুধু reply নয়, *state* (value + TTL) বলো। এই অভ্যাস লম্বা sequence-এ ভুল ঠেকায়।""",
        mist_en=r"""Expecting `SET ... NX` to return an error or `0`, thinking `INCR` on a missing key fails, or mixing up `-1` and `-2` from `TTL`.""",
        mist_bn=r"""`SET ... NX` থেকে error বা `0` আশা করা, ভাবা যে না-থাকা key-এ `INCR` fail করে, অথবা `TTL`-এর `-1` আর `-2` গুলিয়ে ফেলা।""",
        code=r"""
            SET stock:42 10
            DECRBY stock:42 3
            INCR page:views
            SET stock:42 99 NX
            GET stock:42
            SET user:1:name "Rahim"
            INCR user:1:name
            EXPIRE missing:key 60
            SET otp:017 "4821" EX 120
            PERSIST otp:017
            TTL otp:017
            TTL missing:key
        """,
        lang="text",
        output=r"""
            OK
            (integer) 7
            (integer) 1
            (nil)
            "7"
            OK
            (error) ERR value is not an integer or out of range
            (integer) 0
            OK
            (integer) 1
            (integer) -1
            (integer) -2
        """,
        follow=[
            ("What would `SET stock:42 99 XX GET` return here?", "এখানে `SET stock:42 99 XX GET` কী return করত?"),
            ("Why does Redis store `7` as a string but still allow `DECRBY`?", "Redis `7`-কে string হিসেবে রাখলেও `DECRBY` কীভাবে চলে?"),
        ],
        related=["redis-002", "redis-004"],
        refs=[R_SET, R_INCR, R_EXPIRE],
    ),
    # ------------------------------------------------------------------ redis-021
    Q(
        id="redis-021", sub="Streams & Consumer Groups", diff="medium", type="scenario",
        prio="medium", market="both", mins=8,
        tags=["streams", "consumer-groups", "xautoclaim", "idempotency", "node-redis"],
        ver="Redis Open Source 8.10 (XAUTOCLAIM since 6.2); node-redis 6.3", vs=True, status="stable",
        q_en=r"""Three Node.js workers process order events from a Redis Stream using one consumer group. One worker crashes in the middle of handling a batch. What happens to its messages, how do you recover them, and how do you avoid processing an order twice?""",
        q_bn=r"""তিনটা Node.js worker একটা consumer group দিয়ে Redis Stream থেকে order event process করে। একটা batch handle করার মাঝখানে একটা worker crash করল। তার message-গুলোর কী হবে, কীভাবে recover করবে, আর একটা order দুইবার process হওয়া কীভাবে ঠেকাবে?""",
        a_en=r"""
            **What happens:** when `XREADGROUP ... >` delivers a message to a consumer, Redis records it in the group's **Pending Entries List (PEL)** under that consumer. It stays pending until someone calls `XACK`. A crash doesn't lose it — it just sits there, unacknowledged.

            **Recovery:**
            - If the same worker restarts with the **same consumer name**, it can read its own pending messages with ID `0` instead of `>`.
            - Otherwise, healthy workers periodically run **`XAUTOCLAIM`** with a minimum idle time (e.g. 60 s) to take over messages stuck with dead consumers.
            - `XPENDING` shows the delivery count; after N failed deliveries, move the message to a dead-letter stream and `XACK` it so one poison message doesn't loop forever.

            **Avoiding double processing:** Streams give **at-least-once** delivery — a worker might finish the work and crash right before `XACK`, so the message is delivered again. Make the handler **idempotent**: e.g. insert into the DB with the order id as a unique key (`ON CONFLICT DO NOTHING`), and only `XACK` after the DB commit succeeds.
        """,
        a_bn=r"""
            **কী হয়:** `XREADGROUP ... >` কোনো consumer-কে message দিলে Redis সেটা group-এর **Pending Entries List (PEL)**-এ ওই consumer-এর নামে লিখে রাখে। কেউ `XACK` না করা পর্যন্ত এটা pending থাকে। Crash হলে message হারায় না — শুধু acknowledge ছাড়া পড়ে থাকে।

            **Recovery:**
            - একই worker যদি **একই consumer name** নিয়ে restart হয়, `>`-এর বদলে ID `0` দিয়ে নিজের pending message পড়তে পারে।
            - নইলে সুস্থ worker-রা নিয়মিত একটা minimum idle time (যেমন 60 সেকেন্ড) দিয়ে **`XAUTOCLAIM`** চালায়, যাতে মৃত consumer-এর কাছে আটকে থাকা message নিজেরা নিয়ে নেয়।
            - `XPENDING` delivery count দেখায়; N বার fail হওয়ার পর message-টা একটা dead-letter stream-এ সরিয়ে `XACK` করো, যাতে একটা poison message অনন্তকাল ঘুরতে না থাকে।

            **দুইবার process ঠেকানো:** Streams **at-least-once** delivery দেয় — worker কাজ শেষ করে `XACK`-এর ঠিক আগে crash করতে পারে, তখন message আবার আসবে। Handler-কে **idempotent** বানাও: যেমন order id-কে unique key রেখে DB-তে insert (`ON CONFLICT DO NOTHING`), আর DB commit সফল হলেই শুধু `XACK`।
        """,
        ex_en=r"""
            - **Consumer names:** use a stable name per worker (e.g. pod name) so a restarted worker can reclaim its own backlog; random names leave orphans that only `XAUTOCLAIM` will rescue.
            - **`XAUTOCLAIM` is cursor-based:** loop with the returned `nextId` until it's `0-0` to scan the whole PEL.
            - **Trimming:** `XADD ... MAXLEN ~ N` caps memory; make sure N is large enough that unprocessed messages aren't trimmed away. Redis 8.2 added options (e.g. `XACKDEL`) to acknowledge and delete entries in one step across groups.
            - **Ordering:** with several consumers, messages for the same order may be processed in parallel. If per-order ordering matters, partition by order id (e.g. multiple streams) or serialise in the handler.
        """,
        ex_bn=r"""
            - **Consumer name:** প্রতিটা worker-এর জন্য স্থির নাম দাও (যেমন pod-এর নাম), যাতে restart হওয়া worker নিজের backlog ফেরত নিতে পারে; random নাম দিলে অনাথ message তৈরি হয় যেগুলো শুধু `XAUTOCLAIM` উদ্ধার করতে পারে।
            - **`XAUTOCLAIM` cursor-based:** পুরো PEL scan করতে return হওয়া `nextId` `0-0` না হওয়া পর্যন্ত loop করো।
            - **Trimming:** `XADD ... MAXLEN ~ N` memory সীমিত রাখে; N যেন যথেষ্ট বড় হয়, যাতে process না হওয়া message trim হয়ে না যায়। Redis 8.2 group জুড়ে এক ধাপে acknowledge আর delete করার option (যেমন `XACKDEL`) যোগ করেছে।
            - **Ordering:** একাধিক consumer থাকলে একই order-এর message parallel-এ process হতে পারে। প্রতি order-এ ordering জরুরি হলে order id দিয়ে partition করো (যেমন একাধিক stream) বা handler-এ serialise করো।
        """,
        tip_en=r"""Use the exact vocabulary — PEL, `XACK`, `XAUTOCLAIM`, at-least-once, idempotent consumer. Then describe the order: process → commit → ack. That sequence is the heart of the answer.""",
        tip_bn=r"""সঠিক শব্দগুলো ব্যবহার করো — PEL, `XACK`, `XAUTOCLAIM`, at-least-once, idempotent consumer। তারপর ক্রমটা বলো: process → commit → ack। উত্তরের মূল কথা এই ক্রমটাই।""",
        mist_en=r"""Acknowledging the message before doing the work (a crash then loses it), or assuming the message is gone forever when the consumer dies.""",
        mist_bn=r"""কাজ করার আগেই message acknowledge করা (তখন crash হলে সেটা হারায়), অথবা ধরে নেওয়া যে consumer মরে গেলে message চিরতরে হারিয়ে গেছে।""",
        code=r"""
            const STREAM = 'orders:events';
            const GROUP = 'billing';
            const CONSUMER = process.env.HOSTNAME;          // stable name per worker

            await redis.xGroupCreate(STREAM, GROUP, '$', { MKSTREAM: true }).catch((err) => {
              if (!err.message.includes('BUSYGROUP')) throw err;   // group already exists
            });

            async function handle({ id, message }) {
              await createInvoiceIdempotently(message.orderId);  // INSERT ... ON CONFLICT DO NOTHING
              await redis.xAck(STREAM, GROUP, id);                // ack only after the DB commit
            }

            while (running) {
              // 1. Take over messages idle for > 60 s (e.g. from a crashed worker)
              const { messages: stuck } = await redis.xAutoClaim(STREAM, GROUP, CONSUMER, 60_000, '0-0', { COUNT: 10 });
              for (const m of stuck) if (m) await handle(m);

              // 2. Read new messages (blocking read -> use a dedicated connection)
              const res = await redis.xReadGroup(GROUP, CONSUMER, { key: STREAM, id: '>' }, { COUNT: 10, BLOCK: 5_000 });
              for (const m of res?.[0]?.messages ?? []) await handle(m);
            }
        """,
        lang="javascript",
        follow=[
            ("How would you implement a dead-letter stream for poison messages?", "Poison message-এর জন্য dead-letter stream কীভাবে implement করবে?"),
            ("Streams vs a dedicated broker like Kafka or RabbitMQ — when would you switch?", "Streams বনাম Kafka বা RabbitMQ-এর মতো dedicated broker — কখন বদলাবে?"),
        ],
        related=["redis-015", "redis-009"],
        refs=[R_STREAMS, R_XREADGROUP, R_XAUTOCLAIM],
    ),
    # ------------------------------------------------------------------ redis-022
    Q(
        id="redis-022", sub="Cluster & Sentinel Basics", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["redis-cluster", "hash-slots", "hash-tags", "crossslot"],
        ver="Redis Open Source 8.10 (Redis Cluster)", vs=False, status="stable",
        q_en=r"""After moving to Redis Cluster, this transaction fails with a `CROSSSLOT` error: `MULTI` → `SET user:42:profile ...` → `SET user:42:settings ...` → `EXEC`. What is the correct fix?""",
        q_bn=r"""Redis Cluster-এ যাওয়ার পর এই transaction `CROSSSLOT` error দিয়ে fail করছে: `MULTI` → `SET user:42:profile ...` → `SET user:42:settings ...` → `EXEC`। সঠিক সমাধান কী?""",
        options=[
            ("Run `SELECT 1` so both keys live in the same logical database", "`SELECT 1` চালানো, যাতে দুটো key একই logical database-এ থাকে"),
            ("Increase the number of hash slots so related keys collide less", "Hash slot-এর সংখ্যা বাড়ানো, যাতে সম্পর্কিত key কম আলাদা হয়"),
            ("Replace `MULTI`/`EXEC` with pipelining, which works across slots", "`MULTI`/`EXEC`-এর বদলে pipelining ব্যবহার করা, যেটা slot জুড়ে কাজ করে"),
            ("Rename the keys with a hash tag, e.g. `user:{42}:profile` and `user:{42}:settings`", "Hash tag দিয়ে key rename করা, যেমন `user:{42}:profile` আর `user:{42}:settings`"),
        ],
        correct=3,
        a_en=r"""Use a **hash tag**. In Redis Cluster a key's slot is `CRC16(key) mod 16384`, but if the key contains `{...}`, only the part inside the braces is hashed. `user:{42}:profile` and `user:{42}:settings` both hash `42`, land in the same slot, and can be used together in one transaction or script.""",
        a_bn=r"""**Hash tag** ব্যবহার করো। Redis Cluster-এ key-এর slot হলো `CRC16(key) mod 16384`, কিন্তু key-তে `{...}` থাকলে শুধু brace-এর ভেতরের অংশ hash হয়। `user:{42}:profile` আর `user:{42}:settings` দুটোই `42` hash করে, একই slot-এ পড়ে, আর একটা transaction বা script-এ একসাথে ব্যবহার করা যায়।""",
        ex_en=r"""
            Multi-key commands, transactions and Lua scripts only work when every key involved is in the **same hash slot**. Option A fails because Redis Cluster supports only database 0 — `SELECT` to another DB isn't allowed. Option B is impossible: the slot count is fixed at 16384. Option C is tempting: pipelining does work across slots because the client splits commands per node, but it is **not atomic**, so you lose the transaction guarantee.

            Don't overuse hash tags: if you tag everything with the same value (e.g. `{app}`), all keys pile onto one shard and you lose the point of clustering. Tag by an entity that naturally groups data, like a user or order id.
        """,
        ex_bn=r"""
            Multi-key command, transaction আর Lua script তখনই কাজ করে যখন জড়িত সব key **একই hash slot**-এ থাকে। Option A fail করে কারণ Redis Cluster শুধু database 0 support করে — অন্য DB-তে `SELECT` চলে না। Option B অসম্ভব: slot-এর সংখ্যা 16384-এ স্থির। Option C আকর্ষণীয় মনে হয়: client command-গুলো node অনুযায়ী ভাগ করে দেয় বলে pipelining slot জুড়ে কাজ করে ঠিকই, কিন্তু এটা **atomic নয়**, তাই transaction-এর guarantee হারাও।

            Hash tag অতিরিক্ত ব্যবহার কোরো না: সবকিছুতে একই value দিয়ে tag দিলে (যেমন `{app}`) সব key একটা shard-এ জমা হয়, clustering-এর উদ্দেশ্যই নষ্ট হয়। এমন entity দিয়ে tag দাও যেটা স্বাভাবিকভাবে data-কে group করে, যেমন user বা order id।
        """,
        tip_en=r"""Mention the hot-shard downside of hash tags — knowing when *not* to use a fix is what makes the answer senior.""",
        tip_bn=r"""Hash tag-এর hot-shard অসুবিধাটা উল্লেখ করো — কোনো সমাধান কখন ব্যবহার *করা উচিত নয়* সেটা জানাই উত্তরকে senior করে তোলে।""",
        refs=[R_CLUSTER, R_CLUSTER_SPEC],
        related=["redis-028", "redis-031"],
    ),
    # ------------------------------------------------------------------ redis-028
    Q(
        id="redis-028", sub="Cluster & Sentinel Basics", diff="hard", type="architecture",
        prio="medium", market="international", mins=12,
        tags=["sentinel", "redis-cluster", "high-availability", "replication", "failover"],
        ver="Redis Open Source 8.10; node-redis 6.3", vs=False, status="stable",
        q_en=r"""Explain Redis replication, Sentinel and Cluster. How does failover work in each, what must the client do, and how would you decide between Sentinel and Cluster for a growing Node.js product?""",
        q_bn=r"""Redis replication, Sentinel আর Cluster ব্যাখ্যা করো। প্রতিটাতে failover কীভাবে কাজ করে, client-কে কী করতে হয়, আর বাড়তে থাকা একটা Node.js product-এর জন্য Sentinel আর Cluster-এর মধ্যে কীভাবে সিদ্ধান্ত নেবে?""",
        a_en=r"""
            **Replication:** a primary streams writes to one or more replicas **asynchronously**. Replicas can serve reads and act as hot standbys, but on their own nothing promotes them automatically.

            **Sentinel = high availability for one dataset:**
            - A group of Sentinel processes (at least **3**, on independent machines) monitors the primary. When a quorum agrees it's down, a majority authorises a failover: one replica is promoted and the others re-point to it.
            - Sentinel is also the **configuration provider** — clients ask Sentinel "who is the primary?" and reconnect after failover.
            - Scales reads with replicas but not writes; the whole dataset must fit on one node.

            **Cluster = sharding + built-in HA:**
            - The keyspace is split into **16,384 hash slots** spread over several primaries, each with replicas. Failover is built in — no Sentinel needed.
            - Clients cache the slot → node map and follow `MOVED`/`ASK` redirects when slots move.
            - Constraints: multi-key commands, transactions and scripts must stay within one slot (hash tags), and only database 0 exists.

            **Decision:** if the dataset and write throughput fit one machine comfortably, I start with primary + replicas + Sentinel (or a managed equivalent) — simpler, no cross-slot rules. When memory or write load outgrows a node, I move to Cluster and design keys with hash tags up front.
        """,
        a_bn=r"""
            **Replication:** একটা primary এক বা একাধিক replica-তে **asynchronously** write পাঠায়। Replica read serve করতে পারে আর hot standby হিসেবে থাকে, কিন্তু নিজে থেকে কেউ তাদের automatically promote করে না।

            **Sentinel = একটা dataset-এর high availability:**
            - কয়েকটা Sentinel process (কমপক্ষে **3**টা, আলাদা আলাদা machine-এ) primary-কে monitor করে। Quorum একমত হলে যে primary down, majority failover অনুমোদন করে: একটা replica promote হয়, বাকিরা তার দিকে point করে।
            - Sentinel **configuration provider**-ও — client Sentinel-কে জিজ্ঞেস করে "primary কে?" আর failover-এর পর reconnect করে।
            - Replica দিয়ে read scale হয়, write নয়; পুরো dataset একটা node-এ আঁটতে হবে।

            **Cluster = sharding + built-in HA:**
            - Keyspace **16,384টা hash slot**-এ ভাগ হয়ে কয়েকটা primary-তে ছড়ানো থাকে, প্রতিটার replica সহ। Failover built-in — Sentinel লাগে না।
            - Client slot → node map cache করে, আর slot সরলে `MOVED`/`ASK` redirect অনুসরণ করে।
            - সীমাবদ্ধতা: multi-key command, transaction আর script একটা slot-এর ভেতরে থাকতে হবে (hash tag), আর শুধু database 0 আছে।

            **সিদ্ধান্ত:** dataset আর write throughput একটা machine-এ স্বচ্ছন্দে আঁটলে আমি primary + replica + Sentinel (বা managed সমতুল্য) দিয়ে শুরু করি — সহজ, cross-slot নিয়ম নেই। Memory বা write load একটা node ছাড়িয়ে গেলে Cluster-এ যাই, আর শুরু থেকেই hash tag মাথায় রেখে key design করি।
        """,
        ex_en=r"""
            - **Data loss window:** because replication is async, a primary can acknowledge a write and die before replicating it — the promoted replica won't have it. `WAIT numreplicas timeout` and `min-replicas-to-write` shrink the window but don't make Redis strongly consistent.
            - **Split brain:** a primary isolated in a minority partition may keep accepting writes for a while; those are discarded when it rejoins as a replica.
            - **Why 3 Sentinels:** with two, losing the box that runs the primary and one Sentinel leaves no majority to authorise failover.
            - **Client config:** node-redis has `createSentinel` and `createCluster`; ioredis supports `sentinels` and `Redis.Cluster`. Never hard-code the primary's IP.
            - **Managed services** (e.g. ElastiCache, Redis Cloud, Azure) handle failover for you, but the async-replication caveats still apply.
        """,
        ex_bn=r"""
            - **Data loss window:** replication async বলে primary একটা write acknowledge করে replicate করার আগেই মারা যেতে পারে — promote হওয়া replica-তে সেটা থাকবে না। `WAIT numreplicas timeout` আর `min-replicas-to-write` window ছোট করে, কিন্তু Redis-কে strongly consistent করে না।
            - **Split brain:** minority partition-এ বিচ্ছিন্ন primary কিছুক্ষণ write নিতে পারে; replica হিসেবে ফিরে এলে সেই write-গুলো বাতিল হয়।
            - **কেন 3টা Sentinel:** দুইটা থাকলে primary আর একটা Sentinel চলা machine হারালে failover অনুমোদনের মতো majority থাকে না।
            - **Client config:** node-redis-এ আছে `createSentinel` আর `createCluster`; ioredis support করে `sentinels` আর `Redis.Cluster`। Primary-র IP কখনো hard-code কোরো না।
            - **Managed service** (যেমন ElastiCache, Redis Cloud, Azure) failover সামলায়, কিন্তু async replication-এর সতর্কতা তখনও প্রযোজ্য।
        """,
        tip_en=r"""Separate the two concerns clearly: Sentinel solves *availability*, Cluster solves *availability + scale*. Then state the async-replication caveat — that's the detail most candidates miss.""",
        tip_bn=r"""দুইটা বিষয় পরিষ্কারভাবে আলাদা করো: Sentinel সমাধান করে *availability*, Cluster করে *availability + scale*। তারপর async replication-এর সতর্কতা বলো — বেশিরভাগ প্রার্থী এই detail-টাই miss করে।""",
        mist_en=r"""Saying replicas make Redis "lossless", running two Sentinels, or moving to Cluster without checking for multi-key commands and Lua scripts that span slots.""",
        mist_bn=r"""বলা যে replica থাকলে Redis "lossless" হয়, দুইটা Sentinel চালানো, অথবা slot জুড়ে থাকা multi-key command আর Lua script check না করেই Cluster-এ চলে যাওয়া।""",
        code=r"""
            import { createCluster, createSentinel } from 'redis';

            // Redis Cluster: give a few seed nodes; the client discovers the rest
            export const cluster = await createCluster({
              rootNodes: [{ url: 'redis://10.0.1.10:6379' }, { url: 'redis://10.0.1.11:6379' }],
              defaults: { password: process.env.REDIS_PASSWORD },
            }).on('error', (err) => console.error('Cluster error', err)).connect();

            await cluster.set('user:{42}:profile', JSON.stringify({ name: 'Nusrat' }));

            // Sentinel: ask Sentinels for the current primary of "mymaster"
            export const sentinel = await createSentinel({
              name: 'mymaster',
              sentinelRootNodes: [
                { host: '10.0.2.10', port: 26379 },
                { host: '10.0.2.11', port: 26379 },
                { host: '10.0.2.12', port: 26379 },
              ],
            }).on('error', (err) => console.error('Sentinel error', err)).connect();
        """,
        lang="javascript",
        follow=[
            ("What is the difference between `MOVED` and `ASK` redirects?", "`MOVED` আর `ASK` redirect-এর পার্থক্য কী?"),
            ("How would you migrate a running app from a single Redis to Redis Cluster?", "চলমান একটা app-কে single Redis থেকে Redis Cluster-এ কীভাবে migrate করবে?"),
        ],
        related=["redis-022", "redis-027", "redis-030"],
        refs=[R_SENTINEL, R_CLUSTER, R_CLUSTER_SPEC],
    ),
    # ------------------------------------------------------------------ redis-029
    Q(
        id="redis-029", sub="Atomicity & Transactions", diff="hard", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["multi", "exec", "transactions", "no-rollback", "lua"],
        ver="Version-independent (Redis Open Source 8.10)", vs=False, status="stable",
        q_en=r"""The key `name` holds a string. What is the result of running this transaction, and what is the value of `counter` afterwards (it didn't exist before)?""",
        q_bn=r"""`name` key-এ একটা string আছে। এই transaction চালালে কী ফল হবে, আর এরপর `counter`-এর value কত হবে (আগে এটা ছিল না)?""",
        options=[
            ("`EXEC` returns `1`, a WRONGTYPE error, and `2`; `counter` is `2` — Redis does not roll back", "`EXEC` return করে `1`, একটা WRONGTYPE error, আর `2`; `counter` হয় `2` — Redis rollback করে না"),
            ("The whole transaction is rolled back; `counter` doesn't exist", "পুরো transaction rollback হয়; `counter` থাকে না"),
            ("Redis refuses to queue `LPUSH`, and `EXEC` aborts the whole transaction", "Redis `LPUSH` queue করতে অস্বীকার করে, আর `EXEC` পুরো transaction বাতিল করে"),
            ("Execution stops at `LPUSH`: `counter` is `1`", "`LPUSH`-এ গিয়ে execution থেমে যায়: `counter` হয় `1`"),
        ],
        correct=0,
        a_en=r"""`EXEC` returns `1`, a `WRONGTYPE` error and `2`, and `counter` ends up as `2`. A command that fails *at runtime* inside a transaction returns its error in the `EXEC` reply, but the other commands still run — Redis transactions have no rollback.""",
        a_bn=r"""`EXEC` return করে `1`, একটা `WRONGTYPE` error আর `2`, আর `counter` শেষে হয় `2`। Transaction-এর ভেতরে কোনো command *runtime-এ* fail করলে `EXEC` reply-তে তার error আসে, কিন্তু বাকি command-গুলো চলতেই থাকে — Redis transaction-এ rollback নেই।""",
        ex_en=r"""
            Redis distinguishes two kinds of errors:
            - **Queue-time errors** (unknown command, wrong number of arguments) are detected before `EXEC`; the server then refuses to run the transaction (`EXECABORT`). That's option C — tempting, but `LPUSH name x` is syntactically valid, so it queues fine.
            - **Runtime errors** (like `WRONGTYPE`, because `name` holds a string, not a list) only happen during `EXEC`. The failing command reports an error; the rest execute.

            What `MULTI`/`EXEC` *does* guarantee is isolation: the queued commands run back-to-back with no other client's commands in between. For "check then act" logic use `WATCH` (optimistic locking — `EXEC` returns null if a watched key changed) or a Lua script, which can branch and validate before writing. Pipelining, by contrast, only saves round trips and isn't atomic at all.
        """,
        ex_bn=r"""
            Redis দুই ধরনের error আলাদা করে:
            - **Queue-time error** (অজানা command, ভুল সংখ্যক argument) `EXEC`-এর আগেই ধরা পড়ে; তখন server transaction চালাতে অস্বীকার করে (`EXECABORT`)। এটাই option C — আকর্ষণীয়, কিন্তু `LPUSH name x` syntax-এর দিক থেকে সঠিক, তাই এটা ঠিকঠাক queue হয়।
            - **Runtime error** (যেমন `WRONGTYPE`, কারণ `name`-এ list নয়, string আছে) শুধু `EXEC`-এর সময় ঘটে। Fail হওয়া command error দেয়; বাকিগুলো execute হয়।

            `MULTI`/`EXEC` যা *guarantee* দেয় তা হলো isolation: queue করা command-গুলো পরপর চলে, মাঝখানে অন্য কোনো client-এর command ঢোকে না। "Check করে তারপর কাজ" ধরনের logic-এর জন্য `WATCH` (optimistic locking — watched key বদলালে `EXEC` null দেয়) বা Lua script ব্যবহার করো, যেটা লেখার আগে branch আর validate করতে পারে। অন্যদিকে pipelining শুধু round trip বাঁচায়, এটা মোটেই atomic নয়।
        """,
        tip_en=r"""Explicitly separate queue-time and runtime errors, then contrast MULTI, WATCH, Lua and pipelining in one sentence each. That shows a complete mental model of atomicity in Redis.""",
        tip_bn=r"""Queue-time আর runtime error স্পষ্টভাবে আলাদা করো, তারপর MULTI, WATCH, Lua আর pipelining প্রতিটার এক বাক্যে তুলনা দাও। এতে Redis-এর atomicity নিয়ে তোমার পূর্ণ mental model দেখা যায়।""",
        code=r"""
            SET name "bd"
            MULTI
            INCR counter
            LPUSH name x
            INCR counter
            EXEC
            GET counter
        """,
        lang="text",
        refs=[R_TX, R_LUA],
        related=["redis-002", "redis-006"],
    ),
    # ------------------------------------------------------------------ redis-032
    Q(
        id="redis-032", sub="Production Failure Scenarios", diff="extreme", type="scenario",
        prio="medium", market="international", mins=20,
        tags=["latency", "incident", "fork", "slowlog", "big-keys", "aof"],
        ver="Redis Open Source 8.10; node-redis 6.3", vs=False, status="stable",
        q_en=r"""Every few minutes your API's p99 latency jumps from 20 ms to several seconds, and some requests hit node-redis's command timeout. Redis CPU looks low on average. The instance holds 30 GB with RDB snapshots and AOF enabled. How do you investigate and fix this?""",
        q_bn=r"""প্রতি কয়েক মিনিট পরপর তোমার API-এর p99 latency 20 ms থেকে লাফিয়ে কয়েক সেকেন্ডে ওঠে, আর কিছু request node-redis-এর command timeout-এ পড়ে। গড় হিসেবে Redis-এর CPU কম দেখাচ্ছে। Instance-এ 30 GB data, RDB snapshot আর AOF দুটোই চালু। কীভাবে investigate আর fix করবে?""",
        a_en=r"""
            *(Advanced incident question.)* Periodic multi-second stalls with low average CPU point to something that **blocks the single command thread briefly** or stalls the process. I'd test hypotheses in this order, correlating timestamps:

            1. **Slow commands:** `SLOWLOG GET 50` and `INFO commandstats` (`usec_per_call`). Look for `KEYS`, `SMEMBERS`/`HGETALL`/`LRANGE 0 -1` on huge keys, `DEL` of big keys, or long Lua scripts — often from a cron job that runs every few minutes.
            2. **Fork stalls:** `INFO stats` → `latest_fork_usec`. Forking a 30 GB process for `BGSAVE` or AOF rewrite copies large page tables; with **transparent huge pages** enabled, copy-on-write makes it far worse. If spikes line up with the `save` schedule, this is it.
            3. **Disk / AOF fsync:** the Redis log warning "Asynchronous AOF fsync is taking too long (disk is busy?)" and `aof_delayed_fsync` in `INFO persistence` mean the disk can't keep up — often worse while a snapshot is also writing.
            4. **Mass expiry:** a batch job that sets millions of keys with the same TTL makes the active-expire cycle work hard when they all expire together.
            5. **Swapping or the client side:** check `vmstat` for swap-in/out, and Node event-loop lag — a blocked Node process looks like "Redis is slow" from the app's metrics. Compare with `redis-cli --latency` run on the app host.

            **Fixes, matching the cause:** replace `KEYS` with `SCAN`, delete big keys with `UNLINK` and split them; disable THP; move RDB snapshots to a replica (or reduce snapshot frequency) and consider `no-appendfsync-on-rewrite`; faster disks; add TTL jitter; shard the 30 GB dataset so each fork is smaller. Then enable the latency monitor (`latency-monitor-threshold`) and alert on fork time and slow-log entries.
        """,
        a_bn=r"""
            *(Advanced incident প্রশ্ন।)* গড় CPU কম অথচ পর্যায়ক্রমিক কয়েক সেকেন্ডের থমকে যাওয়া মানে এমন কিছু যা **single command thread-কে অল্প সময়ের জন্য block করে** বা process-কে আটকে দেয়। আমি timestamp মিলিয়ে এই ক্রমে hypothesis পরীক্ষা করব:

            1. **Slow command:** `SLOWLOG GET 50` আর `INFO commandstats` (`usec_per_call`)। খুঁজব `KEYS`, বিশাল key-এ `SMEMBERS`/`HGETALL`/`LRANGE 0 -1`, বড় key-এর `DEL`, বা লম্বা Lua script — প্রায়ই কয়েক মিনিট পরপর চলা কোনো cron job থেকে।
            2. **Fork-এর থমকানো:** `INFO stats` → `latest_fork_usec`। `BGSAVE` বা AOF rewrite-এর জন্য 30 GB process fork করলে বড় page table কপি হয়; **transparent huge pages** চালু থাকলে copy-on-write পরিস্থিতি আরও খারাপ করে। Spike যদি `save` schedule-এর সাথে মিলে যায়, কারণ এটাই।
            3. **Disk / AOF fsync:** Redis log-এ "Asynchronous AOF fsync is taking too long (disk is busy?)" warning আর `INFO persistence`-এ `aof_delayed_fsync` মানে disk তাল রাখতে পারছে না — snapshot-ও একসাথে লিখলে আরও খারাপ।
            4. **একসাথে অনেক expiry:** কোনো batch job একই TTL দিয়ে লাখো key set করলে সব একসাথে expire হওয়ার সময় active-expire cycle-কে অনেক খাটতে হয়।
            5. **Swapping বা client-এর দিক:** swap-in/out-এর জন্য `vmstat` দেখো, আর Node-এর event-loop lag — block হওয়া Node process app-এর metric-এ "Redis ধীর" হিসেবেই দেখায়। App host থেকে `redis-cli --latency` চালিয়ে তুলনা করো।

            **কারণ অনুযায়ী সমাধান:** `KEYS`-এর বদলে `SCAN`, বড় key `UNLINK` দিয়ে delete করে ভাগ করো; THP বন্ধ করো; RDB snapshot একটা replica-তে সরাও (বা snapshot কম ঘনঘন করো) আর `no-appendfsync-on-rewrite` বিবেচনা করো; দ্রুত disk; TTL-এ jitter; 30 GB dataset shard করো যাতে প্রতিটা fork ছোট হয়। তারপর latency monitor (`latency-monitor-threshold`) চালু করে fork time আর slow-log entry-তে alert দাও।
        """,
        ex_en=r"""
            - **Why average CPU misleads:** a 2-second stall every 5 minutes barely moves a CPU average but wrecks p99. Always look at max/percentile latency and event timelines.
            - **`SLOWLOG` measures execution time only** — it won't show time spent waiting on fork or disk, which is why you also need `latest_fork_usec`, the latency monitor (`LATENCY DOCTOR`, `LATENCY LATEST`) and the Redis log.
            - **The fork itself scales with memory size** (page tables to copy), while copy-on-write overhead grows with write churn during the snapshot — a strong argument for several smaller shards instead of one 30 GB instance.
            - **Client timeouts matter too:** node-redis v6 defaults to a 5 s command timeout; set timeouts deliberately and make cache reads fall back instead of failing the request.
            - **Write it up:** record the root cause, the graph that proved it, and the alert that would have caught it earlier.
        """,
        ex_bn=r"""
            - **গড় CPU কেন ভুল দিকে নেয়:** প্রতি 5 মিনিটে 2 সেকেন্ডের থমকানো CPU-র গড়ে প্রায় কোনো প্রভাব ফেলে না, কিন্তু p99 নষ্ট করে দেয়। সবসময় max/percentile latency আর event-এর timeline দেখো।
            - **`SLOWLOG` শুধু execution time মাপে** — fork বা disk-এর জন্য অপেক্ষার সময় দেখায় না, তাই `latest_fork_usec`, latency monitor (`LATENCY DOCTOR`, `LATENCY LATEST`) আর Redis log-ও লাগে।
            - **Fork নিজে memory-র আকারের সাথে বাড়ে** (কপি করার মতো page table), আর snapshot চলাকালীন যত বেশি write হয় copy-on-write-এর খরচ তত বাড়ে — একটা 30 GB instance-এর বদলে কয়েকটা ছোট shard রাখার পক্ষে এটা শক্ত যুক্তি।
            - **Client timeout-ও গুরুত্বপূর্ণ:** node-redis v6-এর default command timeout 5 সেকেন্ড; ভেবেচিন্তে timeout দাও, আর cache read fail হলে request fail না করিয়ে fallback করো।
            - **লিখে রাখো:** root cause, যে graph সেটা প্রমাণ করল, আর যে alert থাকলে আগেই ধরা পড়ত — সব document করো।
        """,
        tip_en=r"""Lead with "periodic + low average CPU = something blocking", list hypotheses with the exact command that confirms each, and only then propose fixes. Hypothesis → evidence → fix is the structure senior interviewers reward.""",
        tip_bn=r""""পর্যায়ক্রমিক + কম গড় CPU = কিছু একটা block করছে" দিয়ে শুরু করো, প্রতিটা hypothesis-এর সাথে কোন command দিয়ে নিশ্চিত হবে সেটা বলো, তারপরই সমাধান দাও। Hypothesis → প্রমাণ → সমাধান — senior interviewer-রা এই কাঠামোকেই মূল্য দেয়।""",
        mist_en=r"""Jumping straight to "add more CPU" or "upgrade the instance", running `KEYS *` or `MONITOR` on the struggling production node, or blaming the network without measuring.""",
        mist_bn=r"""সরাসরি "CPU বাড়াও" বা "instance upgrade করো"-তে চলে যাওয়া, চাপে থাকা production node-এ `KEYS *` বা `MONITOR` চালানো, অথবা না মেপেই network-কে দোষ দেওয়া।""",
        code=r"""
            redis-cli SLOWLOG GET 20
            redis-cli INFO commandstats | sort -t= -k4 -n | tail -5    # highest usec_per_call
            redis-cli INFO stats | grep latest_fork_usec
            redis-cli INFO persistence | grep -E "aof_delayed_fsync|rdb_last_bgsave_time_sec"
            redis-cli CONFIG SET latency-monitor-threshold 100
            redis-cli LATENCY DOCTOR
            cat /sys/kernel/mm/transparent_hugepage/enabled              # should be [never]
            vmstat 1 5                                                    # si/so columns = swapping
            redis-cli --latency -h redis.internal                         # run from the app host
        """,
        lang="bash",
        follow=[
            ("Why does disabling transparent huge pages reduce fork-related latency?", "Transparent huge pages বন্ধ করলে fork-সংক্রান্ত latency কেন কমে?"),
            ("How would you safely delete a 5-million-member set in production?", "Production-এ 5 million member-এর একটা set নিরাপদে কীভাবে delete করবে?"),
            ("What alerts would have caught this before users noticed?", "User-রা টের পাওয়ার আগেই কোন alert থাকলে এটা ধরা পড়ত?"),
        ],
        related=["redis-026", "redis-007", "redis-027"],
        refs=[R_LATENCY, R_PERSIST, R_UNLINK],
    ),
]

if __name__ == "__main__":
    save("redis", "b4", QUESTIONS)
