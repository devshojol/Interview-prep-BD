# Redis — batch 1 (redis-001..004, redis-012, redis-013, redis-023, redis-030)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_TYPES = ("Redis docs — Data types", "https://redis.io/docs/latest/develop/data-types/")
R_LATENCY = ("Redis docs — Diagnosing latency issues", "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/")
R_INCR = ("Redis docs — INCR (counter & rate limiter patterns)", "https://redis.io/docs/latest/commands/incr/")
R_SET = ("Redis docs — SET", "https://redis.io/docs/latest/commands/set/")
R_EXPIRE = ("Redis docs — EXPIRE", "https://redis.io/docs/latest/commands/expire/")
R_NODE = ("Redis docs — node-redis guide", "https://redis.io/docs/latest/develop/clients/nodejs/")
R_TX = ("Redis docs — Transactions", "https://redis.io/docs/latest/develop/using-commands/transactions/")
R_LOCKS = ("Redis docs — Distributed locks", "https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/")
R_KLEPPMANN = ("Martin Kleppmann — How to do distributed locking", "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html")
R_LUA = ("Redis docs — Scripting with Lua", "https://redis.io/docs/latest/develop/programmability/eval-intro/")

QUESTIONS = [
    # ------------------------------------------------------------------ redis-001
    Q(
        id="redis-001", sub="In-Memory Storage", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["redis", "in-memory", "single-threaded", "performance"],
        ver="Redis Open Source 8.10", vs=False, status="stable",
        q_en=r"""What is Redis, and why is it so fast compared with a disk-based database?""",
        q_bn=r"""Redis কী, আর disk-based database-এর তুলনায় এটা এত দ্রুত কেন?""",
        a_en=r"""
            Redis is an **in-memory data structure server**. You store values under keys, and a value can be a string, hash, list, set, sorted set, stream and more. Because the dataset lives in RAM, most commands finish in well under a millisecond.

            It's fast for three main reasons:
            - **Memory, not disk:** there is no disk read on the request path; persistence (if enabled) happens in the background.
            - **Purpose-built data structures:** commands like `INCR`, `LPUSH` or `ZADD` work directly on optimised in-memory structures, mostly in O(1) or O(log N).
            - **Single-threaded command execution:** one event loop runs commands one at a time, so there are no locks or context switches, and every individual command is atomic. I/O threads can help with socket reads/writes, but commands still execute serially.

            In Node.js projects I use it for caching, sessions, rate limiting, queues and leaderboards — usually next to a primary database, not instead of it.
        """,
        a_bn=r"""
            Redis হলো একটি **in-memory data structure server**। এখানে key-এর অধীনে value রাখা হয়, আর value হতে পারে string, hash, list, set, sorted set, stream ইত্যাদি। পুরো dataset RAM-এ থাকে বলে বেশিরভাগ command এক millisecond-এর অনেক কম সময়ে শেষ হয়ে যায়।

            দ্রুত হওয়ার মূল তিনটা কারণ:
            - **Disk নয়, memory:** request-এর পথে কোনো disk read নেই; persistence চালু থাকলে সেটা background-এ হয়।
            - **বিশেষভাবে তৈরি data structure:** `INCR`, `LPUSH` বা `ZADD`-এর মতো command সরাসরি optimised in-memory structure-এর ওপর কাজ করে, বেশিরভাগই O(1) বা O(log N)।
            - **Single-threaded command execution:** একটা event loop একবারে একটা করে command চালায়, তাই lock বা context switch লাগে না, আর প্রতিটা আলাদা command atomic হয়। I/O thread socket read/write-এ সাহায্য করতে পারে, কিন্তু command execution serial-ই থাকে।

            Node.js project-এ আমি Redis ব্যবহার করি caching, session, rate limiting, queue আর leaderboard-এর জন্য — সাধারণত primary database-এর পাশাপাশি, তার বদলে নয়।
        """,
        ex_en=r"""
            - **RAM is the limit:** the dataset must fit in memory (`maxmemory`), so you plan eviction policies and TTLs. RAM also costs more than disk.
            - **The single-thread trade-off:** one slow command — `KEYS *` on millions of keys, deleting a huge key with `DEL`, a long Lua script — blocks every other client for that duration.
            - **Network usually dominates:** a round trip costs far more than the command itself, so pipelining and multi-key commands like `MGET` often matter more than raw server speed.
            - **Durability is configurable:** RDB snapshots and/or AOF logs, but with defaults there is a window where recent writes can be lost.
            - **Redis 8:** Redis Open Source now ships JSON, the Query Engine (search and vector search), time series, probabilistic types and Vector Sets built in.
        """,
        ex_bn=r"""
            - **RAM-ই সীমা:** dataset-কে memory-তে (`maxmemory`) আঁটতে হবে, তাই eviction policy আর TTL আগে থেকে plan করতে হয়। RAM-এর খরচও disk-এর চেয়ে বেশি।
            - **Single-thread-এর trade-off:** একটা slow command — লাখো key-এর ওপর `KEYS *`, বিশাল key `DEL` করা, লম্বা Lua script — চলার সময় বাকি সব client block হয়ে থাকে।
            - **সাধারণত network-ই বড় খরচ:** একটা round trip command-এর চেয়ে অনেক বেশি সময় নেয়, তাই pipelining আর `MGET`-এর মতো multi-key command অনেক সময় server-এর raw speed-এর চেয়েও বেশি গুরুত্বপূর্ণ।
            - **Durability configure করা যায়:** RDB snapshot আর/অথবা AOF log, তবে default setting-এ সাম্প্রতিক কিছু write হারানোর একটা window থাকে।
            - **Redis 8:** Redis Open Source-এ এখন JSON, Query Engine (search ও vector search), time series, probabilistic type আর Vector Sets built-in থাকে।
        """,
        tip_en=r"""Give a one-line definition, then the three reasons for speed, then one real use case from your own project. Mentioning the single-threaded downside (one slow command blocks everyone) shows you understand the trade-off, not just the marketing.""",
        tip_bn=r"""এক লাইনে definition দাও, তারপর দ্রুততার তিনটা কারণ, শেষে নিজের project থেকে একটা বাস্তব use case বলো। Single-threaded হওয়ার অসুবিধা (একটা slow command সবাইকে block করে) উল্লেখ করলে বোঝা যায় তুমি শুধু সুবিধা নয়, trade-off-ও জানো।""",
        mist_en=r"""Saying Redis is fast "because it is multi-threaded", calling it "just a cache", or claiming it can never lose data.""",
        mist_bn=r"""Redis "multi-threaded বলে দ্রুত" বলা, একে "শুধু একটা cache" বলা, অথবা দাবি করা যে Redis-এ কখনো data হারায় না।""",
        code=r"""
            127.0.0.1:6379> SET greeting "hello"
            OK
            127.0.0.1:6379> GET greeting
            "hello"
            127.0.0.1:6379> INCR visits
            (integer) 1
            127.0.0.1:6379> TYPE visits
            string
        """,
        lang="text",
        follow=[
            ("If command execution is single-threaded, how does Redis serve thousands of concurrent clients?", "Command execution single-threaded হলে Redis একসাথে হাজারো client-কে কীভাবে serve করে?"),
            ("What happens to the data when the Redis server restarts?", "Redis server restart হলে data-র কী হয়?"),
        ],
        related=["redis-003", "redis-006", "redis-027"],
        refs=[R_TYPES, R_LATENCY],
    ),
    # ------------------------------------------------------------------ redis-002
    Q(
        id="redis-002", sub="Key-Value Fundamentals", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=1,
        tags=["incr", "atomicity", "counter", "concurrency"],
        ver="Version-independent concept (Redis Open Source 8.10)", vs=False, status="stable",
        q_en=r"""The key `page:views` holds `10`. Two Node.js servers run `INCR page:views` at exactly the same moment. What is the value afterwards?""",
        q_bn=r"""`page:views` key-এর value `10`। দুইটা Node.js server ঠিক একই মুহূর্তে `INCR page:views` চালাল। এরপর value কত হবে?""",
        options=[
            ("`12`, because each `INCR` runs atomically, one after the other", "`12`, কারণ প্রতিটা `INCR` atomically একটার পর একটা execute হয়"),
            ("`11`, because one increment overwrites the other", "`11`, কারণ একটা increment অন্যটাকে overwrite করে দেয়"),
            ("Either `11` or `12`, depending on network timing", "Network timing-এর ওপর নির্ভর করে `11` অথবা `12`"),
            ("An error, because concurrent writes must be wrapped in `MULTI`", "Error হবে, কারণ concurrent write-কে `MULTI`-এর ভেতরে রাখতে হয়"),
        ],
        correct=0,
        a_en=r"""The value will be `12`. Redis executes commands one at a time, and `INCR` is a single atomic read-modify-write on the server, so neither increment can be lost.""",
        a_bn=r"""Value হবে `12`। Redis একবারে একটা করে command execute করে, আর `INCR` server-এর ভেতরে একটাই atomic read-modify-write, তাই কোনো increment হারায় না।""",
        ex_en=r"""
            Option C is the tempting one: it *would* be true if the app did `GET`, added 1 in JavaScript, then `SET` the result — two clients could both read `10` and both write `11` (a lost update). `INCR` avoids that because the read and the write happen inside one command on the single command-execution thread. You don't need `MULTI` for a single command; `MULTI`/`EXEC` or Lua is for making *several* commands atomic together. A missing key is treated as `0`, and `INCR` works on 64-bit signed integers.
        """,
        ex_bn=r"""
            Option C-টাই সবচেয়ে বিভ্রান্তিকর: app যদি `GET` করে JavaScript-এ 1 যোগ করে আবার `SET` করত, তাহলে দুই client-ই `10` পড়ে দুজনেই `11` লিখতে পারত (lost update)। `INCR`-এ সেটা হয় না, কারণ read আর write দুটোই single command-execution thread-এ একটা command-এর ভেতরেই হয়। একটা command-এর জন্য `MULTI` লাগে না; `MULTI`/`EXEC` বা Lua দরকার *একাধিক* command একসাথে atomic করতে। Key না থাকলে `INCR` সেটাকে `0` ধরে নেয়, আর এটা 64-bit signed integer-এ কাজ করে।
        """,
        tip_en=r"""Contrast `INCR` with the GET → modify → SET pattern in application code. Naming the "lost update" problem shows you understand why atomic server-side commands matter.""",
        tip_bn=r"""Application code-এর GET → modify → SET pattern-এর সাথে `INCR`-এর তুলনা করো। "Lost update" সমস্যার নাম বললে বোঝা যায় server-side atomic command কেন জরুরি সেটা তুমি জানো।""",
        refs=[R_INCR],
        related=["redis-001", "redis-029"],
    ),
    # ------------------------------------------------------------------ redis-003
    Q(
        id="redis-003", sub="Strings, Hashes, Lists, Sets, Sorted Sets", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["data-types", "hashes", "lists", "sets", "sorted-sets"],
        ver="Redis Open Source 8.10", vs=False, status="stable",
        q_en=r"""Explain Redis's core data types — strings, hashes, lists, sets and sorted sets — with a real use case for each.""",
        q_bn=r"""Redis-এর মূল data type — string, hash, list, set আর sorted set — প্রতিটার একটা বাস্তব use case সহ ব্যাখ্যা করো।""",
        a_en=r"""
            - **String:** a binary-safe value up to 512 MB — text, a number or serialized JSON. Use for cached API responses, feature flags and counters (`SET`, `GET`, `INCR`).
            - **Hash:** a map of field → value under one key, like a small object. Use for a user profile or session where you read/update single fields (`HSET`, `HGET`, `HGETALL`).
            - **List:** an ordered sequence with fast push/pop at both ends. Use for simple job queues or "latest 50 notifications" (`LPUSH`, `RPOP`, `LRANGE`, `LTRIM`).
            - **Set:** unordered unique members with membership checks and set algebra. Use for tags, "users who liked this post", or unique visitors per day (`SADD`, `SISMEMBER`, `SINTER`).
            - **Sorted set:** unique members ordered by a numeric score. Use for leaderboards, priority queues and time-based indexes (`ZADD`, `ZRANGE ... REV`, `ZINCRBY`).

            Picking the right type matters: it decides which operations are atomic and cheap on the server.
        """,
        a_bn=r"""
            - **String:** 512 MB পর্যন্ত binary-safe value — text, number বা serialized JSON। Cached API response, feature flag আর counter-এর জন্য (`SET`, `GET`, `INCR`)।
            - **Hash:** একটা key-এর অধীনে field → value-এর map, অনেকটা ছোট object-এর মতো। User profile বা session-এর জন্য ভালো, যেখানে আলাদা আলাদা field read/update করতে হয় (`HSET`, `HGET`, `HGETALL`)।
            - **List:** ordered sequence, দুই মাথাতেই দ্রুত push/pop করা যায়। Simple job queue বা "সর্বশেষ ৫০টা notification"-এর জন্য (`LPUSH`, `RPOP`, `LRANGE`, `LTRIM`)।
            - **Set:** unordered unique member, membership check আর set operation (union/intersection) করা যায়। Tag, "কারা এই post like করেছে", বা দিনে unique visitor গোনার জন্য (`SADD`, `SISMEMBER`, `SINTER`)।
            - **Sorted set:** numeric score অনুযায়ী সাজানো unique member। Leaderboard, priority queue আর time-based index-এর জন্য (`ZADD`, `ZRANGE ... REV`, `ZINCRBY`)।

            সঠিক type বেছে নেওয়া জরুরি, কারণ এটাই ঠিক করে server-এ কোন operation atomic আর সস্তা হবে।
        """,
        ex_en=r"""
            - **Hash vs JSON string:** a JSON string must be read and rewritten entirely to change one field; a hash lets you `HSET` or `HINCRBY` one field atomically. Since Redis 7.4 you can even expire individual hash fields (`HEXPIRE`).
            - **Complexities to remember:** `LPUSH`/`RPOP` are O(1), but `LRANGE` on a huge list or `SMEMBERS` on a huge set is O(N) — avoid unbounded collections ("big keys").
            - **Other types:** streams (append-only log with consumer groups), bitmaps and HyperLogLog (compact counting), geospatial indexes, and in Redis 8 the built-in JSON, time series, probabilistic types and Vector Sets.
        """,
        ex_bn=r"""
            - **Hash বনাম JSON string:** JSON string-এ একটা field বদলাতে পুরো value পড়ে আবার লিখতে হয়; hash-এ `HSET` বা `HINCRBY` দিয়ে একটা field atomically বদলানো যায়। Redis 7.4 থেকে আলাদা hash field-এ expiry-ও দেওয়া যায় (`HEXPIRE`)।
            - **Complexity মনে রাখো:** `LPUSH`/`RPOP` O(1), কিন্তু বিশাল list-এ `LRANGE` বা বিশাল set-এ `SMEMBERS` O(N) — সীমাহীন collection ("big key") এড়িয়ে চলো।
            - **অন্যান্য type:** stream (consumer group সহ append-only log), bitmap আর HyperLogLog (কম memory-তে গণনা), geospatial index, আর Redis 8-এ built-in JSON, time series, probabilistic type ও Vector Sets।
        """,
        tip_en=r"""Don't just list the types — attach a use case from an app you built (e.g. "we stored OTP attempts in a hash with a TTL"). Interviewers remember concrete examples.""",
        tip_bn=r"""শুধু type-এর নাম বলে থেমো না — নিজের বানানো app থেকে use case জুড়ে দাও (যেমন "OTP attempt আমরা TTL সহ একটা hash-এ রাখতাম")। Interviewer-রা concrete উদাহরণ মনে রাখে।""",
        mist_en=r"""Storing everything as JSON strings, or using a list where uniqueness is needed (a set) or ordering by score is needed (a sorted set).""",
        mist_bn=r"""সবকিছু JSON string হিসেবে রাখা, অথবা যেখানে uniqueness দরকার (set) বা score অনুযায়ী ordering দরকার (sorted set) সেখানে list ব্যবহার করা।""",
        code=r"""
            SET product:42:cache '{"id":42,"name":"Panjabi","price":1450}' EX 300
            HSET user:7 name "Nusrat" city "Dhaka" plan "pro"
            HINCRBY user:7 loginCount 1
            LPUSH notifications:7 "Order #981 shipped"
            LTRIM notifications:7 0 49
            SADD post:55:likes user:7 user:9
            SISMEMBER post:55:likes user:7
            ZADD leaderboard 1200 "rahim" 1850 "karim"
            ZRANGE leaderboard 0 9 REV WITHSCORES
        """,
        lang="text",
        follow=[
            ("When would you store an object as a hash instead of a JSON string?", "কখন একটা object-কে JSON string-এর বদলে hash হিসেবে রাখবে?"),
            ("What is a 'big key' and why is it a problem?", "'Big key' কী, আর এটা কেন সমস্যা?"),
        ],
        related=["redis-016", "redis-018", "redis-015"],
        refs=[R_TYPES, R_SET],
    ),
    # ------------------------------------------------------------------ redis-004
    Q(
        id="redis-004", sub="TTL & Expiration", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["ttl", "expire", "set", "keepttl"],
        ver="Redis Open Source 8.10 (KEEPTTL since 6.0)", vs=False, status="stable",
        q_en=r"""You store an OTP with `SET otp:01712 4821 EX 120`. A few seconds later another code path runs `SET otp:01712 9999` (no options). What does `TTL otp:01712` return now?""",
        q_bn=r"""তুমি `SET otp:01712 4821 EX 120` দিয়ে একটা OTP রাখলে। কয়েক সেকেন্ড পরে অন্য একটা code path `SET otp:01712 9999` (কোনো option ছাড়া) চালাল। এখন `TTL otp:01712` কী return করবে?""",
        options=[
            ("About `115` — the original countdown continues", "প্রায় `115` — আগের countdown চলতেই থাকবে"),
            ("`-2` — the key was deleted by the second `SET`", "`-2` — দ্বিতীয় `SET` key-টাকে delete করে দিয়েছে"),
            ("`-1` — the key now exists without any expiry", "`-1` — key আছে কিন্তু কোনো expiry নেই"),
            ("`120` — the TTL is reset to its original value", "`120` — TTL আবার আগের মানে reset হয়েছে"),
        ],
        correct=2,
        a_en=r"""`-1`. A successful `SET` without an expiry option discards the key's previous TTL, so the OTP now lives forever — a real security bug for OTPs and sessions.""",
        a_bn=r"""`-1`। Expiry option ছাড়া সফল `SET` key-এর আগের TTL মুছে দেয়, ফলে OTP-টা এখন চিরকাল থেকে যাবে — OTP বা session-এর জন্য এটা সত্যিকারের security bug।""",
        ex_en=r"""
            Option A is the trap: many people assume the countdown survives an overwrite. It doesn't — the docs state that any previous TTL is discarded on a successful `SET`. Fix it by passing the expiry again (`SET ... EX 120`) or, if you really want to keep the remaining time, `SET ... KEEPTTL` (Redis 6.0+).

            Remember the special values: `TTL` returns `-1` when the key exists without an expiry and `-2` when the key doesn't exist. Commands that *modify* a value in place (`INCR`, `HSET`, `LPUSH`) keep the TTL; commands that *replace* the value (`SET`, `GETSET`) clear it.
        """,
        ex_bn=r"""
            Option A-টাই ফাঁদ: অনেকে ভাবে overwrite করলেও countdown চলতে থাকে। আসলে না — docs-এ স্পষ্ট বলা আছে, সফল `SET` হলে আগের TTL বাতিল হয়ে যায়। সমাধান: আবার expiry দাও (`SET ... EX 120`), অথবা বাকি সময়টাই রাখতে চাইলে `SET ... KEEPTTL` (Redis 6.0+)।

            Special value মনে রাখো: key আছে কিন্তু expiry নেই হলে `TTL` দেয় `-1`, আর key-ই না থাকলে `-2`। যেসব command value-কে জায়গায় বসে *পরিবর্তন* করে (`INCR`, `HSET`, `LPUSH`) সেগুলো TTL রেখে দেয়; আর যেগুলো value *replace* করে (`SET`, `GETSET`) সেগুলো TTL মুছে দেয়।
        """,
        tip_en=r"""Mention the security angle: an OTP, password-reset token or session that silently loses its TTL becomes valid forever. That turns a trivia question into a production insight.""",
        tip_bn=r"""Security-র দিকটা বলো: OTP, password-reset token বা session-এর TTL চুপচাপ হারিয়ে গেলে সেটা চিরকাল valid থেকে যায়। এতে একটা সাধারণ প্রশ্ন production-এর অভিজ্ঞতা দেখানোর সুযোগ হয়ে যায়।""",
        code=r"""
            SET otp:01712 4821 EX 120
            SET otp:01712 9999
            TTL otp:01712
        """,
        lang="text",
        refs=[R_SET, R_EXPIRE],
        related=["redis-018", "redis-020"],
    ),
    # ------------------------------------------------------------------ redis-012
    Q(
        id="redis-012", sub="Rate Limiting", diff="medium", type="coding",
        prio="high", market="both", mins=10,
        tags=["rate-limiting", "express", "middleware", "incr", "node-redis"],
        ver="Redis Open Source 8.10 (EXPIRE NX since 7.0); node-redis 6.3; Express 5.3", vs=True, status="stable",
        q_en=r"""
            Write an Express 5 middleware that limits each client to **100 requests per 60-second fixed window** using Redis (node-redis v6).

            Requirements:
            - Identify the client by `req.user.id` if logged in, otherwise by `req.ip`.
            - Return `429 Too Many Requests` with a `Retry-After` header once the limit is exceeded.
            - Never leave a counter key without an expiry, even if the Node process crashes mid-request.
            - If Redis is down, decide whether to fail open or fail closed and justify it.

            Example: with `limit = 3`, requests 1–3 in the same minute get `200`, request 4 gets `429` with `Retry-After` set to the seconds left in the window.
        """,
        q_bn=r"""
            Redis (node-redis v6) ব্যবহার করে একটা Express 5 middleware লেখো, যেটা প্রতিটা client-কে **প্রতি 60-second fixed window-এ 100টা request**-এ সীমিত রাখবে।

            Requirement:
            - Login করা থাকলে `req.user.id` দিয়ে, না হলে `req.ip` দিয়ে client চিনবে।
            - Limit পার হলে `Retry-After` header সহ `429 Too Many Requests` return করবে।
            - Request-এর মাঝখানে Node process crash করলেও কোনো counter key যেন expiry ছাড়া থেকে না যায়।
            - Redis down থাকলে fail open নাকি fail closed করবে, সেটা ঠিক করে যুক্তি দাও।

            উদাহরণ: `limit = 3` হলে একই মিনিটে request 1–3 পাবে `200`, request 4 পাবে `429`, আর `Retry-After`-এ থাকবে window শেষ হতে বাকি কত সেকেন্ড।
        """,
        a_en=r"""
            I build the key from the client id plus the current window number (`Math.floor(now / windowSec)`), then send `INCR` and `EXPIRE key windowSec NX` together in a `MULTI` transaction. `INCR` is atomic, so concurrent requests can't lose counts, and because both commands execute together on the server, a crash in the Node process can't leave a counter without a TTL. `EXPIRE ... NX` (Redis 7.0+) sets the TTL only on the first hit of the window.

            If the returned count is above the limit I respond `429` with `Retry-After`; otherwise I set the remaining-quota headers and call `next()`.

            For a general public API I **fail open** (log and allow the request) when Redis is unavailable, because blocking all traffic is worse than briefly losing rate limiting. For security-sensitive endpoints like login or OTP I'd **fail closed**.
        """,
        a_bn=r"""
            আমি client id আর বর্তমান window number (`Math.floor(now / windowSec)`) মিলিয়ে key বানাই, তারপর `INCR` আর `EXPIRE key windowSec NX` একসাথে একটা `MULTI` transaction-এ পাঠাই। `INCR` atomic, তাই concurrent request-এ count হারায় না; আর দুটো command server-এ একসাথে execute হয় বলে Node process crash করলেও কোনো counter TTL ছাড়া থেকে যায় না। `EXPIRE ... NX` (Redis 7.0+) শুধু window-এর প্রথম hit-এ TTL বসায়।

            Return হওয়া count limit-এর বেশি হলে `Retry-After` সহ `429` দিই; না হলে remaining-quota header বসিয়ে `next()` call করি।

            সাধারণ public API-তে Redis unavailable হলে আমি **fail open** করি (log করে request যেতে দিই), কারণ সব traffic আটকে দেওয়া কিছুক্ষণ rate limiting না থাকার চেয়ে খারাপ। Login বা OTP-এর মতো security-sensitive endpoint-এ **fail closed** করব।
        """,
        ex_en=r"""
            - **Why not plain `INCR` then `EXPIRE` as two awaits?** If the process dies between them, the key never expires and that client is blocked forever. The INCR docs call out exactly this race. `MULTI`/`EXEC` or a Lua script fixes it.
            - **Fixed-window weakness:** a client can send 100 requests at 12:00:59 and 100 more at 12:01:00 — 200 in two seconds. If that matters, use a sliding window (sorted set + Lua) or a token bucket.
            - **`req.ip` behind a proxy:** with NGINX or a load balancer in front, configure `app.set('trust proxy', ...)` correctly, otherwise every user shares the proxy's IP — and never trust a raw `X-Forwarded-For` blindly.
            - **Headers:** `Retry-After` is standard; the `RateLimit-*` headers follow an IETF draft that libraries like `express-rate-limit` also use.
            - **Cost:** one round trip per request; memory is one small key per active client per window.
        """,
        ex_bn=r"""
            - **দুইটা আলাদা await-এ `INCR` তারপর `EXPIRE` কেন নয়?** মাঝখানে process মারা গেলে key কখনো expire হবে না, আর ওই client চিরকাল block থাকবে। INCR docs-এ ঠিক এই race-এর কথাই বলা আছে। `MULTI`/`EXEC` বা Lua script দিয়ে এটা ঠিক হয়।
            - **Fixed window-এর দুর্বলতা:** একজন client 12:00:59-এ 100টা আর 12:01:00-এ আরও 100টা request পাঠাতে পারে — দুই সেকেন্ডে 200টা। এটা সমস্যা হলে sliding window (sorted set + Lua) বা token bucket ব্যবহার করো।
            - **Proxy-র পেছনে `req.ip`:** সামনে NGINX বা load balancer থাকলে `app.set('trust proxy', ...)` ঠিকভাবে configure করো, নইলে সব user proxy-র একই IP share করবে — আর raw `X-Forwarded-For` চোখ বুজে বিশ্বাস কোরো না।
            - **Header:** `Retry-After` standard; `RateLimit-*` header-গুলো একটা IETF draft অনুসরণ করে, যেটা `express-rate-limit`-এর মতো library-ও ব্যবহার করে।
            - **খরচ:** প্রতি request-এ একটা round trip; memory লাগে প্রতি active client-এর প্রতি window-এ একটা ছোট key।
        """,
        tip_en=r"""Say the race condition out loud ("INCR and EXPIRE must be atomic together") before writing code, then mention the boundary-burst weakness and offer sliding window as the upgrade. That sequence shows depth.""",
        tip_bn=r"""Code লেখার আগেই race condition-টা বলো ("INCR আর EXPIRE একসাথে atomic হতে হবে"), তারপর window boundary-তে burst-এর দুর্বলতা উল্লেখ করে sliding window-কে upgrade হিসেবে প্রস্তাব করো। এই ধারাবাহিকতা তোমার গভীরতা দেখায়।""",
        mist_en=r"""Calling `expire()` in a separate await after `incr()`, resetting the TTL on every request (turning the window into "100 per minute of silence"), or keying only by IP behind a reverse proxy.""",
        mist_bn=r"""`incr()`-এর পর আলাদা await-এ `expire()` call করা, প্রতিটা request-এ TTL reset করা (তাতে window হয়ে যায় "চুপ থাকার প্রতি মিনিটে 100"), অথবা reverse proxy-র পেছনে শুধু IP দিয়ে key বানানো।""",
        code=r"""
            import express from 'express';
            import { createClient } from 'redis';

            const redis = await createClient({ url: process.env.REDIS_URL })
              .on('error', (err) => console.error('Redis error', err))
              .connect();

            export function fixedWindowLimiter({ limit = 100, windowSec = 60, prefix = 'rl' } = {}) {
              return async function rateLimit(req, res, next) {
                const id = req.user?.id ?? req.ip;
                const nowSec = Math.floor(Date.now() / 1000);
                const windowId = Math.floor(nowSec / windowSec);
                const key = `${prefix}:${id}:${windowId}`;

                let count;
                try {
                  // INCR + EXPIRE NX run together on the server
                  [count] = await redis.multi()
                    .incr(key)
                    .expire(key, windowSec, 'NX')
                    .exec();
                } catch (err) {
                  console.error('Rate limiter unavailable, failing open:', err.message);
                  return next();
                }

                const resetSec = windowSec - (nowSec % windowSec);
                res.set('RateLimit-Limit', String(limit));
                res.set('RateLimit-Remaining', String(Math.max(0, limit - count)));
                res.set('RateLimit-Reset', String(resetSec));

                if (count > limit) {
                  res.set('Retry-After', String(resetSec));
                  return res.status(429).json({ error: 'Too many requests' });
                }
                return next();
              };
            }

            const app = express();
            app.set('trust proxy', 1); // one trusted reverse proxy (e.g. NGINX) in front
            app.use('/api', fixedWindowLimiter({ limit: 100, windowSec: 60 }));
        """,
        lang="javascript",
        output=r"""
            # with limit = 3
            GET /api/products -> 200 (RateLimit-Remaining: 2)
            GET /api/products -> 200 (RateLimit-Remaining: 1)
            GET /api/products -> 200 (RateLimit-Remaining: 0)
            GET /api/products -> 429 (Retry-After: seconds left in the window)
        """,
        time="O(1) per request", space="O(number of active clients per window)",
        follow=[
            ("How would you change this to a sliding window?", "এটাকে sliding window-এ কীভাবে বদলাবে?"),
            ("How do you rate-limit across several Redis Cluster shards?", "একাধিক Redis Cluster shard জুড়ে rate limit কীভাবে করবে?"),
            ("Why might a fixed window allow twice the limit?", "Fixed window কেন limit-এর দ্বিগুণ request ঢুকতে দিতে পারে?"),
        ],
        related=["redis-024", "redis-002"],
        refs=[R_INCR, R_EXPIRE, R_TX],
    ),
    # ------------------------------------------------------------------ redis-013
    Q(
        id="redis-013", sub="Cache-Aside", diff="medium", type="debugging",
        prio="high", market="both", mins=7,
        tags=["cache-aside", "ttl", "invalidation", "node-redis", "debugging"],
        ver="node-redis 6.3; Redis Open Source 8.10", vs=True, status="stable",
        q_en=r"""This cache-aside code for a product page "works" in development, but in production customers see old prices for days, Redis memory keeps growing, and sometimes the API returns a JSON string instead of an object. Find the bugs and fix them.""",
        q_bn=r"""Product page-এর এই cache-aside code development-এ "চলে", কিন্তু production-এ customer-রা দিনের পর দিন পুরনো দাম দেখে, Redis-এর memory বাড়তেই থাকে, আর মাঝে মাঝে API object-এর বদলে JSON string return করে। Bug-গুলো খুঁজে বের করে ঠিক করো।""",
        a_en=r"""
            There are five problems:
            1. **No TTL** on `redis.set` — entries never expire, so stale data lives forever and memory grows until `maxmemory` is hit.
            2. **No invalidation on write** — `updateProductPrice` changes the database but leaves the old cached product.
            3. **Inconsistent return type** — on a hit it returns the raw string; on a miss it returns an object. It must `JSON.parse` the cached value.
            4. **"Not found" cached forever** — `JSON.stringify(null)` is `"null"`, which is truthy, so a missing product is cached permanently and returned as the string `"null"`.
            5. **Redis failures break the page** — there's no `'error'` listener and no fallback, so a Redis outage turns into a 500 instead of a slower DB read.

            The fix: parse on hit, set a TTL (with a little jitter), cache misses briefly, delete the key after a successful DB update, and wrap cache calls so Redis is an optimisation, not a dependency.
        """,
        a_bn=r"""
            এখানে পাঁচটা সমস্যা:
            1. `redis.set`-এ **কোনো TTL নেই** — entry কখনো expire হয় না, তাই stale data চিরকাল থাকে আর `maxmemory` না ছোঁয়া পর্যন্ত memory বাড়তে থাকে।
            2. **Write-এর সময় invalidation নেই** — `updateProductPrice` database বদলায়, কিন্তু পুরনো cached product রেখে দেয়।
            3. **Return type অসামঞ্জস্যপূর্ণ** — hit হলে raw string, miss হলে object return করে। Cached value-কে `JSON.parse` করতে হবে।
            4. **"Not found" চিরকাল cache হয়** — `JSON.stringify(null)` হলো `"null"`, যেটা truthy; ফলে না-থাকা product স্থায়ীভাবে cache হয় আর string `"null"` return হয়।
            5. **Redis fail করলে page ভেঙে যায়** — কোনো `'error'` listener বা fallback নেই, তাই Redis outage হলে ধীর DB read-এর বদলে 500 error হয়।

            সমাধান: hit হলে parse করো, TTL দাও (একটু jitter সহ), miss অল্প সময়ের জন্য cache করো, সফল DB update-এর পর key delete করো, আর cache call-গুলো এমনভাবে wrap করো যাতে Redis একটা optimisation থাকে, dependency না হয়ে যায়।
        """,
        ex_en=r"""
            - **Delete, don't update, on writes:** deleting the key after the DB commit is simpler and safer than writing the new value into the cache — two concurrent writers could otherwise leave the older value cached.
            - **Remaining race:** a reader can load the old row, the writer updates and deletes, then the reader writes the old value back. The TTL bounds how long that can last; for stricter needs use versioned keys or a delayed second delete.
            - **Jitter:** adding a random few seconds to the TTL prevents thousands of keys created together from expiring together (cache avalanche).
            - **Negative caching:** caching "not found" for ~30 s protects the DB from repeated lookups for IDs that don't exist (cache penetration).
            - **Key versioning:** a prefix like `product:v1:` lets you change the cached shape on deploy without serving incompatible old entries.
        """,
        ex_bn=r"""
            - **Write-এর সময় update নয়, delete করো:** DB commit-এর পর key delete করা নতুন value cache-এ লেখার চেয়ে সহজ ও নিরাপদ — নইলে দুইটা concurrent writer মিলে পুরনো value-টা cache-এ রেখে দিতে পারে।
            - **যে race থেকেই যায়:** একজন reader পুরনো row পড়ল, writer update করে delete করল, তারপর reader পুরনো value আবার cache-এ লিখে দিল। TTL এই সমস্যার সময়সীমা বেঁধে দেয়; আরও কড়া দরকার হলে versioned key বা দেরিতে দ্বিতীয়বার delete ব্যবহার করো।
            - **Jitter:** TTL-এ কয়েক সেকেন্ড random যোগ করলে একসাথে তৈরি হাজারো key একসাথে expire হয় না (cache avalanche)।
            - **Negative caching:** "not found" ~30 সেকেন্ড cache করলে না-থাকা ID-র জন্য বারবার lookup থেকে DB বাঁচে (cache penetration)।
            - **Key versioning:** `product:v1:`-এর মতো prefix থাকলে deploy-এর সময় cached data-র shape বদলালেও পুরনো, অসামঞ্জস্যপূর্ণ entry serve হয় না।
        """,
        tip_en=r"""Number the bugs as you find them and tie each one to the production symptom it causes (stale prices, memory growth, wrong type). That mapping is what interviewers look for in debugging questions.""",
        tip_bn=r"""Bug খুঁজে পাওয়ার সাথে সাথে নম্বর দাও, আর প্রতিটাকে production-এর কোন symptom-এর (পুরনো দাম, memory বৃদ্ধি, ভুল type) সাথে যুক্ত সেটা বলো। Debugging প্রশ্নে interviewer ঠিক এই mapping-টাই দেখতে চায়।""",
        mist_en=r"""Fixing only the TTL and forgetting invalidation, updating the cache instead of deleting it, or using `if (cached)` instead of `cached !== null`, which treats a legitimately cached empty string as a miss.""",
        mist_bn=r"""শুধু TTL ঠিক করে invalidation ভুলে যাওয়া, cache delete না করে update করা, অথবা `cached !== null`-এর বদলে `if (cached)` ব্যবহার করা — যেটা বৈধভাবে cache করা empty string-কে miss হিসেবে ধরে।""",
        code=r"""
            import { createClient } from 'redis';
            import { db } from './db.js';

            const redis = await createClient({ url: process.env.REDIS_URL }).connect();

            export async function getProduct(id) {
              const cached = await redis.get(`product:${id}`);
              if (cached) return cached;

              const product = await db.product.findById(id);
              await redis.set(`product:${id}`, JSON.stringify(product));
              return product;
            }

            export async function updateProductPrice(id, price) {
              await db.product.update(id, { price });
            }
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            import { createClient } from 'redis';
            import { db } from './db.js';

            const TTL_SECONDS = 300;
            const NOT_FOUND_TTL_SECONDS = 30;
            const key = (id) => `product:v1:${id}`;

            const redis = await createClient({ url: process.env.REDIS_URL })
              .on('error', (err) => console.error('Redis error', err))
              .connect();

            export async function getProduct(id) {
              try {
                const cached = await redis.get(key(id));
                if (cached !== null) return JSON.parse(cached); // may be null = cached "not found"
              } catch (err) {
                console.warn('Cache read failed, falling back to DB', err.message);
              }

              const product = await db.product.findById(id);

              const ttl = product
                ? TTL_SECONDS + Math.floor(Math.random() * 60) // jitter
                : NOT_FOUND_TTL_SECONDS;                       // short negative cache
              try {
                await redis.set(key(id), JSON.stringify(product ?? null), {
                  expiration: { type: 'EX', value: ttl },
                });
              } catch (err) {
                console.warn('Cache write failed', err.message);
              }
              return product;
            }

            export async function updateProductPrice(id, price) {
              await db.product.update(id, { price }); // 1. commit to the source of truth
              await redis.del(key(id));               // 2. then invalidate the cache
            }
        """)],
        follow=[
            ("Why delete the cache key instead of writing the new value into it?", "Cache-এ নতুন value না লিখে key delete করা কেন ভালো?"),
            ("What happens if `redis.del` fails after the DB update succeeded?", "DB update সফল হওয়ার পর `redis.del` fail করলে কী হবে?"),
        ],
        related=["redis-005", "redis-014", "redis-023"],
        refs=[R_NODE, R_SET],
    ),
    # ------------------------------------------------------------------ redis-023
    Q(
        id="redis-023", sub="Cache Stampedes", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["cache-stampede", "thundering-herd", "penetration", "avalanche", "jitter"],
        ver="Redis Open Source 8.10; node-redis 6.3", vs=False, status="stable",
        q_en=r"""Every 10 minutes your database CPU spikes to 100% for a few seconds, right when the cached homepage feed expires. Explain cache stampede, cache penetration and cache avalanche, and how you would protect the database from each.""",
        q_bn=r"""প্রতি 10 মিনিট পরপর কয়েক সেকেন্ডের জন্য তোমার database CPU 100% হয়ে যায় — ঠিক যখন cached homepage feed expire হয়। Cache stampede, cache penetration আর cache avalanche ব্যাখ্যা করো, আর প্রতিটা থেকে database-কে কীভাবে রক্ষা করবে বলো।""",
        a_en=r"""
            **Cache stampede (thundering herd):** a hot key expires and hundreds of concurrent requests miss at once, all running the same expensive query. Fixes:
            - **Single-flight / mutex:** only the request that wins `SET lock:key token NX PX 5000` rebuilds; others wait briefly and re-read the cache. Inside one Node process, share one in-flight promise per key.
            - **Serve stale while revalidating:** keep a soft expiry inside the value and a longer hard TTL; return the stale value while one worker refreshes in the background.
            - **Probabilistic early expiration:** each reader refreshes slightly before expiry with a probability that rises as the expiry approaches, so one request refreshes early instead of all at once.

            **Cache penetration:** requests for keys that don't exist anywhere (random IDs, bots) always miss and always hit the DB. Fixes: cache "not found" with a short TTL, validate input, rate-limit, or check a Bloom filter first (Redis 8 includes `BF.*` commands).

            **Cache avalanche:** many keys expire at the same moment, or Redis restarts empty. Fixes: add random jitter to TTLs, warm critical keys on deploy, make Redis highly available, and cap DB concurrency with a circuit breaker or connection-pool limit so the DB degrades instead of collapsing.
        """,
        a_bn=r"""
            **Cache stampede (thundering herd):** একটা hot key expire হলো আর শত শত concurrent request একসাথে miss করে একই ভারী query চালাল। সমাধান:
            - **Single-flight / mutex:** শুধু যে request `SET lock:key token NX PX 5000` জিতবে সে-ই rebuild করবে; বাকিরা একটু অপেক্ষা করে আবার cache পড়বে। একটা Node process-এর ভেতরে প্রতি key-এর জন্য একটাই in-flight promise share করো।
            - **Stale serve করে background-এ refresh:** value-এর ভেতরে একটা soft expiry আর তার চেয়ে লম্বা hard TTL রাখো; একজন worker refresh করার সময় বাকিদের stale value দাও।
            - **Probabilistic early expiration:** প্রতিটা reader expiry-র একটু আগেই এমন probability-তে refresh করে যেটা expiry যত কাছে আসে তত বাড়ে — ফলে সবাই একসাথে না করে একজন আগেভাগে refresh করে।

            **Cache penetration:** এমন key-এর request যেটা কোথাও নেই (random ID, bot) — সবসময় miss হয়, সবসময় DB-তে যায়। সমাধান: "not found" অল্প TTL দিয়ে cache করো, input validate করো, rate-limit করো, অথবা আগে Bloom filter check করো (Redis 8-এ `BF.*` command আছে)।

            **Cache avalanche:** অনেক key একই মুহূর্তে expire হয়, অথবা Redis খালি অবস্থায় restart হয়। সমাধান: TTL-এ random jitter যোগ করো, deploy-এর সময় জরুরি key warm করো, Redis-কে highly available রাখো, আর circuit breaker বা connection-pool limit দিয়ে DB concurrency সীমিত রাখো যাতে DB ভেঙে না পড়ে ধীরে ধীরে degrade করে।
        """,
        ex_en=r"""
            - **Diagnosing your symptom:** a CPU spike exactly every TTL period, correlated with a burst of identical slow queries, is the stampede signature. Check slow-query logs and cache hit ratio around expiry time.
            - **Lock details:** give the lock a short TTL (longer than the typical rebuild), release it with compare-and-delete so you never delete someone else's lock, and bound the wait — after a few hundred ms, fall back to stale data or the DB rather than hanging requests.
            - **Two layers:** the in-process promise map removes duplicates inside one instance; the Redis lock removes duplicates across instances. Large deployments usually need both.
            - **Background refresh:** for a handful of very hot keys (homepage, category menu), a scheduled job that refreshes before expiry is simpler than any lock.
            - **Watch the trade-off:** every mitigation serves slightly stale data for a moment. Make that explicit with the product team.
        """,
        ex_bn=r"""
            - **তোমার symptom-এর diagnosis:** ঠিক প্রতিটা TTL period-এ CPU spike, আর তার সাথে একই রকম slow query-র ঢেউ — এটাই stampede-এর চেনা লক্ষণ। Expiry-র সময়ের আশেপাশে slow-query log আর cache hit ratio দেখো।
            - **Lock-এর খুঁটিনাটি:** lock-কে ছোট TTL দাও (সাধারণ rebuild time-এর চেয়ে একটু বেশি), compare-and-delete দিয়ে release করো যাতে অন্যের lock মুছে না ফেলো, আর wait-এর সীমা রাখো — কয়েকশো ms পরে request ঝুলিয়ে না রেখে stale data বা DB-তে fallback করো।
            - **দুই স্তর:** in-process promise map একটা instance-এর ভেতরের duplicate দূর করে; Redis lock instance-গুলোর মধ্যে duplicate দূর করে। বড় deployment-এ সাধারণত দুটোই লাগে।
            - **Background refresh:** অল্প কয়েকটা খুব hot key-এর (homepage, category menu) জন্য expiry-র আগে refresh করা একটা scheduled job যেকোনো lock-এর চেয়ে সহজ।
            - **Trade-off খেয়াল রাখো:** প্রতিটা সমাধানই কিছুক্ষণের জন্য একটু stale data দেখায়। Product team-এর সাথে এটা স্পষ্ট করে নাও।
        """,
        tip_en=r"""Define the three terms crisply first (they're often confused), then go deep on one mitigation with code. Ending with "and I'd monitor hit ratio and DB QPS around expiry" signals production experience.""",
        tip_bn=r"""আগে তিনটা term পরিষ্কারভাবে define করো (এগুলো প্রায়ই গুলিয়ে যায়), তারপর একটা সমাধান code সহ গভীরভাবে বলো। শেষে "expiry-র সময় hit ratio আর DB QPS monitor করব" বললে production অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Solving a stampede by simply making the TTL longer (it just moves the spike), or using a lock with no TTL and no wait limit, which can freeze every request if the rebuilder crashes.""",
        mist_bn=r"""শুধু TTL বাড়িয়ে stampede সমাধান করা (এতে spike শুধু সরে যায়), অথবা TTL আর wait limit ছাড়া lock ব্যবহার করা — rebuilder crash করলে যেটা সব request আটকে দিতে পারে।""",
        code=r"""
            import { randomUUID } from 'node:crypto';
            import { setTimeout as sleep } from 'node:timers/promises';

            const UNLOCK = `if redis.call('GET', KEYS[1]) == ARGV[1] then
              return redis.call('DEL', KEYS[1]) else return 0 end`;
            const inflight = new Map(); // per-process request coalescing

            export async function getOrRebuild(redis, key, ttlSec, loader) {
              const hit = await redis.get(key);
              if (hit !== null) return JSON.parse(hit);
              if (inflight.has(key)) return inflight.get(key);

              const work = (async () => {
                const lockKey = `lock:${key}`;
                const token = randomUUID();
                const gotLock = await redis.set(lockKey, token, {
                  condition: 'NX',
                  expiration: { type: 'PX', value: 5000 },
                });

                if (!gotLock) {
                  for (let i = 0; i < 10; i++) {          // wait up to ~1s for the winner
                    await sleep(100);
                    const v = await redis.get(key);
                    if (v !== null) return JSON.parse(v);
                  }
                  return loader();                          // last resort
                }

                try {
                  const value = await loader();
                  const jitter = Math.floor(Math.random() * ttlSec * 0.1);
                  await redis.set(key, JSON.stringify(value), {
                    expiration: { type: 'EX', value: ttlSec + jitter },
                  });
                  return value;
                } finally {
                  await redis.eval(UNLOCK, { keys: [lockKey], arguments: [token] });
                }
              })().finally(() => inflight.delete(key));

              inflight.set(key, work);
              return work;
            }
        """,
        lang="javascript",
        follow=[
            ("How does probabilistic early expiration decide when to refresh?", "Probabilistic early expiration কীভাবে ঠিক করে কখন refresh করতে হবে?"),
            ("What happens if the process holding the rebuild lock crashes?", "Rebuild lock ধরে রাখা process crash করলে কী হয়?"),
            ("How would a Bloom filter help with cache penetration, and what is its false-positive trade-off?", "Cache penetration-এ Bloom filter কীভাবে সাহায্য করে, আর এর false-positive trade-off কী?"),
        ],
        related=["redis-013", "redis-031", "redis-025"],
        refs=[R_SET, R_LOCKS],
    ),
    # ------------------------------------------------------------------ redis-030
    Q(
        id="redis-030", sub="Distributed Locks & Limitations", diff="extreme", type="architecture",
        prio="medium", market="international", mins=20,
        tags=["distributed-lock", "redlock", "fencing-token", "idempotency", "payments"],
        ver="Redis Open Source 8.10 (DELEX IFEQ since 8.4); node-redis 6.3", vs=True, status="stable",
        q_en=r"""Your order service uses a Redis lock (`SET lock:order:{id} <token> NX PX 30000`) so that only one worker charges the customer. Yet a customer was charged twice in production. How can that happen, would Redlock fix it, and how would you design this correctly?""",
        q_bn=r"""তোমার order service একটা Redis lock (`SET lock:order:{id} <token> NX PX 30000`) ব্যবহার করে যাতে শুধু একজন worker customer-কে charge করে। তবুও production-এ একজন customer দুইবার charged হয়েছে। এটা কীভাবে সম্ভব, Redlock কি এটা ঠিক করবে, আর সঠিক design কী হবে?""",
        a_en=r"""
            *(Advanced distributed-systems question.)* A Redis lock is really a **lease**: it's valid only until its TTL runs out, and the holder can't know exactly when that happens. Double execution can occur when:
            - **The holder pauses past the TTL** — a long GC pause, a blocked event loop or a slow network call. The lock expires, worker B acquires it, then worker A wakes up and still charges.
            - **Failover loses the lock** — replication is asynchronous, so a primary can acknowledge the `SET`, crash before replicating, and the promoted replica has no lock.
            - **Unsafe release** — a plain `DEL` can delete a lock that now belongs to someone else.

            **Redlock** (acquiring a majority of independent Redis masters) tackles the single-node failover case, but it still relies on timing assumptions about pauses and clock drift, so it can't guarantee mutual exclusion for correctness-critical work. That's the core of Martin Kleppmann's critique (and the Redis docs themselves recommend fencing tokens).

            **Correct design:** treat the Redis lock as an *efficiency* optimisation (avoid duplicate work), and enforce *correctness* where the side effect happens:
            - **Idempotency key** for the payment (e.g. the order id) sent to the payment provider, and a unique constraint in the database.
            - **Conditional state transitions** in the DB: `UPDATE orders SET status='charging' WHERE id=$1 AND status='pending'` — only one worker gets a row back.
            - **Fencing tokens** when the protected resource can check them: issue a monotonically increasing number atomically with the lock and have the storage reject writes carrying an older token.
            - Release locks with compare-and-delete (`DELEX key IFEQ token` on Redis 8.4+, or a Lua script).
        """,
        a_bn=r"""
            *(Advanced distributed-systems প্রশ্ন।)* Redis lock আসলে একটা **lease**: TTL শেষ হওয়া পর্যন্তই valid, আর holder নিশ্চিতভাবে জানতে পারে না ঠিক কখন সেটা শেষ হলো। দুইবার execute হতে পারে যখন:
            - **Holder TTL-এর চেয়ে বেশি সময় থেমে থাকে** — লম্বা GC pause, block হওয়া event loop, বা ধীর network call। Lock expire হয়, worker B সেটা নেয়, তারপর worker A জেগে উঠে তবুও charge করে।
            - **Failover-এ lock হারায়** — replication asynchronous, তাই primary `SET` acknowledge করে replicate করার আগেই crash করতে পারে, আর promote হওয়া replica-তে কোনো lock থাকে না।
            - **অনিরাপদ release** — সাধারণ `DEL` এমন lock মুছে দিতে পারে যেটা এখন অন্য কারো।

            **Redlock** (একাধিক independent Redis master-এর majority নেওয়া) single-node failover-এর সমস্যা কমায়, কিন্তু pause আর clock drift নিয়ে timing assumption-এর ওপর নির্ভর করে, তাই correctness-critical কাজের জন্য mutual exclusion guarantee দিতে পারে না। Martin Kleppmann-এর সমালোচনার মূল কথাই এটা (আর Redis docs নিজেও fencing token ব্যবহার করতে বলে)।

            **সঠিক design:** Redis lock-কে *efficiency* optimisation হিসেবে দেখো (duplicate কাজ এড়ানো), আর *correctness* নিশ্চিত করো যেখানে আসল side effect ঘটে সেখানে:
            - Payment provider-এর কাছে **idempotency key** (যেমন order id) পাঠাও, আর database-এ unique constraint রাখো।
            - DB-তে **conditional state transition**: `UPDATE orders SET status='charging' WHERE id=$1 AND status='pending'` — শুধু একজন worker row ফেরত পাবে।
            - Protected resource check করতে পারলে **fencing token**: lock-এর সাথে atomically একটা ক্রমবর্ধমান number দাও, আর storage যেন পুরনো token-ওয়ালা write reject করে।
            - Lock release করো compare-and-delete দিয়ে (Redis 8.4+-এ `DELEX key IFEQ token`, নইলে Lua script)।
        """,
        ex_en=r"""
            - **Why fencing works:** the storage, not the client, decides. If A (token 33) resumes after B (token 34) has written, the storage has already seen 34 and rejects 33. Note the token must be issued atomically with acquisition — if A paused between acquiring and `INCR`, it could get the *newer* token. Hence the Lua script below.
            - **The limit of fencing:** external APIs (a card network, SMS gateway) can't check your tokens. That's why idempotency keys at the provider are the real protection for payments.
            - **Lock renewal ("watchdog")** extends the TTL while work is running; it reduces but doesn't eliminate the pause problem, because the pause can happen right before the side effect.
            - **`WAIT` / `min-replicas-to-write`** reduce failover loss but don't make Redis strongly consistent.
            - **When a Redis lock is fine:** deduplicating cache rebuilds, cron jobs that are safe to run twice, or reducing contention — cases where an occasional double run is merely wasteful.
            - **Cluster note:** the lock key and the fence key in one script must share a hash slot, hence `{order:42}` hash tags.
        """,
        ex_bn=r"""
            - **Fencing কেন কাজ করে:** সিদ্ধান্ত নেয় storage, client নয়। A (token 33) যদি B (token 34)-এর লেখার পরে আবার চালু হয়, storage ইতিমধ্যে 34 দেখেছে, তাই 33 reject করবে। খেয়াল রাখো, token lock নেওয়ার সাথে atomically দিতে হবে — A যদি lock নেওয়া আর `INCR`-এর মাঝখানে থেমে যায়, তাহলে সে-ই *নতুন* token পেয়ে যেতে পারে। তাই নিচে Lua script।
            - **Fencing-এর সীমা:** external API (card network, SMS gateway) তোমার token check করতে পারে না। তাই payment-এর আসল সুরক্ষা হলো provider-এর কাছে idempotency key।
            - **Lock renewal ("watchdog")** কাজ চলার সময় TTL বাড়ায়; এতে pause-সমস্যা কমে কিন্তু দূর হয় না, কারণ pause ঠিক side effect-এর আগেও হতে পারে।
            - **`WAIT` / `min-replicas-to-write`** failover-এ data হারানো কমায়, কিন্তু Redis-কে strongly consistent করে না।
            - **কখন Redis lock যথেষ্ট:** cache rebuild deduplicate করা, এমন cron job যেটা দুইবার চললেও সমস্যা নেই, বা contention কমানো — যেখানে মাঝেমধ্যে দুইবার চলা শুধু অপচয়, ক্ষতি নয়।
            - **Cluster note:** একটা script-এর lock key আর fence key-কে একই hash slot-এ থাকতে হবে, তাই `{order:42}` hash tag।
        """,
        tip_en=r"""Structure it as: (1) why the lock failed — lease + pauses + failover, (2) Redlock and its limits, (3) the real fix — idempotency, conditional writes, fencing. Saying "locks for efficiency, idempotency for correctness" is the line senior interviewers want to hear.""",
        tip_bn=r"""এভাবে সাজাও: (1) lock কেন fail করল — lease + pause + failover, (2) Redlock আর তার সীমাবদ্ধতা, (3) আসল সমাধান — idempotency, conditional write, fencing। "Efficiency-র জন্য lock, correctness-এর জন্য idempotency" — senior interviewer ঠিক এই কথাটাই শুনতে চায়।""",
        mist_en=r"""Believing a longer TTL or Redlock makes the lock "safe", releasing with plain `DEL`, or generating the fencing token in a separate call after acquiring the lock.""",
        mist_bn=r"""ভাবা যে TTL বাড়ালে বা Redlock ব্যবহার করলে lock "safe" হয়ে যায়, সাধারণ `DEL` দিয়ে release করা, অথবা lock নেওয়ার পর আলাদা call-এ fencing token তৈরি করা।""",
        code=r"""
            import { randomUUID } from 'node:crypto';

            // Acquire the lock AND issue a fencing token in one atomic step
            const ACQUIRE_WITH_FENCE = `
            if redis.call('SET', KEYS[1], ARGV[1], 'NX', 'PX', ARGV[2]) then
              return redis.call('INCR', KEYS[2])
            end
            return 0`;

            export async function chargeOrder(redis, sql, orderId, paymentApi) {
              const token = randomUUID();
              const fence = await redis.eval(ACQUIRE_WITH_FENCE, {
                keys: [`lock:{order:${orderId}}`, `fence:{order:${orderId}}`],
                arguments: [token, '30000'],
              });
              if (fence === 0) return 'busy';

              // Correctness lives in the database, not in the lock
              const rows = await sql`
                UPDATE orders SET status = 'charging', fence = ${fence}
                WHERE id = ${orderId} AND status = 'pending' AND fence < ${fence}
                RETURNING id`;
              if (rows.length === 0) return 'already-handled';

              // The provider deduplicates retries with the idempotency key
              await paymentApi.charge({ orderId, idempotencyKey: `order-${orderId}` });
              await sql`UPDATE orders SET status = 'charged' WHERE id = ${orderId} AND fence = ${fence}`;

              // Release only our own lock (Redis 8.4+; use a Lua compare-and-delete on older versions)
              await redis.sendCommand(['DELEX', `lock:{order:${orderId}}`, 'IFEQ', token]);
              return 'charged';
            }
        """,
        lang="javascript",
        follow=[
            ("How exactly does Redlock acquire a lock, and what timing assumptions does it make?", "Redlock ঠিক কীভাবে lock নেয়, আর কোন কোন timing assumption করে?"),
            ("How would you implement fencing if the protected resource is an S3 object?", "Protected resource একটা S3 object হলে fencing কীভাবে implement করবে?"),
            ("When would you choose a database row lock (`SELECT ... FOR UPDATE`) over a Redis lock?", "কখন Redis lock-এর বদলে database row lock (`SELECT ... FOR UPDATE`) বেছে নেবে?"),
        ],
        related=["redis-025", "redis-028"],
        refs=[R_LOCKS, R_KLEPPMANN, R_LUA],
    ),
]

if __name__ == "__main__":
    save("redis", "b1", QUESTIONS)
