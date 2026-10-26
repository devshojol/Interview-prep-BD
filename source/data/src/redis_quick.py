# Redis — quick-recall questions (redis-q01..redis-q10)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_INTRO = ("Redis docs — Data types", "https://redis.io/docs/latest/develop/data-types/")
R_LATENCY = ("Redis docs — Diagnosing latency issues", "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/")
R_EXPIRE = ("Redis docs — EXPIRE", "https://redis.io/docs/latest/commands/expire/")
R_PERSIST = ("Redis docs — Persistence", "https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/")
R_STREAMS = ("Redis docs — Streams", "https://redis.io/docs/latest/develop/data-types/streams/")
R_EVICT = ("Redis docs — Key eviction", "https://redis.io/docs/latest/develop/reference/eviction/")
R_PIPE = ("Redis docs — Pipelining", "https://redis.io/docs/latest/develop/using-commands/pipelining/")
R_NODE = ("Redis docs — node-redis guide", "https://redis.io/docs/latest/develop/clients/nodejs/")

VER = "Redis Open Source 8.10"

QUESTIONS = [
    # ------------------------------------------------------------------ redis-q01
    Q(
        id="redis-q01", sub="In-Memory Storage", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["redis", "in-memory", "use-cases"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is Redis, and what is it commonly used for?""",
        q_bn=r"""Redis কী, আর সাধারণত কী কাজে ব্যবহার হয়?""",
        a_en=r"""Redis is an in-memory key-value data store: every value lives under a key, and a value can be a string, hash, list, set, sorted set, stream and more. Because the data is in RAM, reads and writes are very fast, so it's used for caching, sessions, rate limiting, queues, leaderboards and real-time messaging, usually next to a main database.""",
        a_bn=r"""Redis হলো একটা in-memory key-value data store: প্রতিটা value একটা key-এর অধীনে থাকে, আর value হতে পারে string, hash, list, set, sorted set, stream ইত্যাদি। Data RAM-এ থাকে বলে read/write খুব দ্রুত, তাই caching, session, rate limiting, queue, leaderboard আর real-time messaging-এ ব্যবহার হয়, সাধারণত একটা main database-এর পাশাপাশি।""",
        ex_en=r"""The usual follow-up is "can it replace my database?". For most apps, no: RAM is limited and costly, and durability is configurable rather than guaranteed, so PostgreSQL or MongoDB stay the source of truth.""",
        ex_bn=r"""সাধারণ follow-up হলো "এটা কি database-এর জায়গা নিতে পারে?"। বেশিরভাগ app-এ না: RAM সীমিত আর দামি, আর durability configurable, guaranteed না; তাই PostgreSQL বা MongoDB-ই source of truth থাকে।""",
        tip_en=r"""Give the one-line definition, then name three real uses from your own projects (cache, sessions, rate limiter).""",
        tip_bn=r"""এক line-এ definition দাও, তারপর নিজের project থেকে তিনটা আসল ব্যবহার বলো (cache, session, rate limiter)।""",
        follow=[("Can Redis be your primary database?", "Redis কি primary database হতে পারে?")],
        related=["redis-001", "redis-006"],
        refs=[R_INTRO],
    ),
    # ------------------------------------------------------------------ redis-q02
    Q(
        id="redis-q02", sub="In-Memory Storage", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["single-threaded", "atomicity", "performance"],
        ver=VER, vs=False, status="stable",
        q_en=r"""Is Redis single-threaded? If so, how is it still so fast?""",
        q_bn=r"""Redis কি single-threaded? তাহলে এত দ্রুত কীভাবে?""",
        a_en=r"""Redis executes commands on one main thread, one command at a time (I/O threads can help with network reads and writes, but commands still run serially). It's fast because the data is in RAM and most commands are O(1) or O(log N), and one thread means no locks: every single command is atomic.""",
        a_bn=r"""Redis একটা main thread-এ একবারে একটা করে command execute করে (network read/write-এ I/O thread সাহায্য করতে পারে, কিন্তু command চলে একটার পর একটা)। এটা দ্রুত কারণ data RAM-এ থাকে আর বেশিরভাগ command O(1) বা O(log N); আর এক thread মানে lock নেই: প্রতিটা command atomic।""",
        ex_en=r"""The flip side: one slow command blocks everyone. `KEYS *` or `HGETALL` on a huge hash can freeze all clients, so use `SCAN` and keep values small.""",
        ex_bn=r"""উল্টো দিকটা হলো: একটা ধীর command সবাইকে আটকে দেয়। বিশাল hash-এ `KEYS *` বা `HGETALL` সব client-কে থামিয়ে দিতে পারে, তাই `SCAN` ব্যবহার করো আর value ছোট রাখো।""",
        tip_en=r"""Say "single-threaded command execution" (not "Redis has one thread") and add the "one slow command blocks everyone" gotcha.""",
        tip_bn=r""""Single-threaded command execution" বলো ("Redis-এর একটাই thread" না), আর "একটা ধীর command সবাইকে আটকে দেয়" gotcha-টা যোগ করো।""",
        follow=[("Why is `KEYS *` dangerous in production?", "Production-এ `KEYS *` কেন বিপজ্জনক?")],
        related=["redis-001", "redis-007"],
        refs=[R_LATENCY],
    ),
    # ------------------------------------------------------------------ redis-q03
    Q(
        id="redis-q03", sub="Strings, Hashes, Lists, Sets, Sorted Sets", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["data-types", "hash", "sorted-set", "string"],
        ver=VER, vs=False, status="stable",
        q_en=r"""Which Redis data type would you pick for a page-view counter, a user profile, and a game leaderboard?""",
        q_bn=r"""Page-view counter, user profile আর game leaderboard-এর জন্য Redis-এর কোন data type বেছে নেবে?""",
        a_en=r"""A string for the counter (`INCR` is atomic), a hash for the profile (read or update single fields with `HGET`/`HSET`), and a sorted set for the leaderboard (members ordered by score, so the top N is one `ZRANGE ... REV` call).""",
        a_bn=r"""Counter-এর জন্য string (`INCR` atomic), profile-এর জন্য hash (`HGET`/`HSET` দিয়ে আলাদা field পড়া বা update করা যায়), আর leaderboard-এর জন্য sorted set (member score অনুযায়ী সাজানো, তাই top N একটাই `ZRANGE ... REV` call)।""",
        code=r"""
            INCR page:views                          # (integer) 1  → String
            HSET user:1 name "Rahim" city "Dhaka"    # (integer) 2  → Hash
            ZADD lb 120 "rahim" 95 "karim"           # (integer) 2  → Sorted set
            ZRANGE lb 0 0 REV WITHSCORES             # 1) "rahim" 2) "120"
        """, lang="text",
        ex_en=r"""Storing a profile as one JSON string also works, but then changing one field means reading, parsing and rewriting the whole value, and two writers can overwrite each other.""",
        ex_bn=r"""Profile-কে একটা JSON string হিসেবে রাখাও যায়, কিন্তু তখন একটা field বদলাতে পুরো value পড়ে, parse করে আবার লিখতে হয়, আর দুজন writer একে অপরের লেখা মুছে দিতে পারে।""",
        tip_en=r"""Match each use case to a type and name the one command that makes it a good fit.""",
        tip_bn=r"""প্রতিটা use case-এর সাথে একটা type মেলাও, আর কোন command-এর কারণে সেটা উপযুক্ত সেটা বলো।""",
        follow=[("When would you use a set instead of a list?", "কখন list-এর বদলে set ব্যবহার করবে?")],
        related=["redis-003", "redis-016"],
        refs=[R_INTRO],
    ),
    # ------------------------------------------------------------------ redis-q04
    Q(
        id="redis-q04", sub="TTL & Expiration", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["ttl", "expire", "expiration"],
        ver=VER, vs=False, status="stable",
        q_en=r"""How do you make a Redis key expire, and what do `TTL` results `-1` and `-2` mean?""",
        q_bn=r"""Redis key কীভাবে expire করাবে, আর `TTL`-এর result `-1` ও `-2` মানে কী?""",
        a_en=r"""Set the expiry when writing (`SET key value EX 60`) or on an existing key (`EXPIRE key 60`); Redis deletes the key once the time runs out. `TTL` returns the seconds left, `-1` if the key exists but has no expiry, and `-2` if the key doesn't exist.""",
        a_bn=r"""লেখার সময় expiry দাও (`SET key value EX 60`) অথবা আগে থেকে থাকা key-তে (`EXPIRE key 60`); সময় শেষ হলে Redis key-টা মুছে দেয়। `TTL` বাকি second দেয়, key আছে কিন্তু expiry নেই হলে `-1`, আর key-ই না থাকলে `-2`।""",
        code=r"""
            SET otp:017 4821 EX 60    # OK
            TTL otp:017               # (integer) 60, then 59, 58 ...
            SET user:1:name "Rahim"   # OK
            TTL user:1:name           # (integer) -1 → no expiry
            TTL nothing:here          # (integer) -2 → key doesn't exist
        """, lang="text",
        ex_en=r"""Gotcha: a plain `SET` on a key that had a TTL removes the TTL. Pass `EX` again, or `KEEPTTL` to keep the remaining time.""",
        ex_bn=r"""Gotcha: TTL-ওয়ালা key-তে সাধারণ `SET` করলে TTL মুছে যায়। আবার `EX` দাও, অথবা বাকি সময় রাখতে `KEEPTTL` দাও।""",
        tip_en=r"""Prefer `SET ... EX` in one command over `SET` then `EXPIRE`, and say why: a crash between the two leaves a key that never expires.""",
        tip_bn=r"""`SET`-এর পরে আলাদা `EXPIRE`-এর বদলে এক command-এ `SET ... EX` বলো, আর কারণও বলো: দুটোর মাঝে crash হলে key আর কখনো expire হয় না।""",
        follow=[("What happens to the TTL if you overwrite the key with a plain `SET`?", "সাধারণ `SET` দিয়ে key overwrite করলে TTL-এর কী হয়?")],
        related=["redis-004", "redis-018", "redis-020"],
        refs=[R_EXPIRE],
    ),
    # ------------------------------------------------------------------ redis-q05
    Q(
        id="redis-q05", sub="Cache-Aside", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["cache-aside", "caching", "node-redis"],
        ver="Redis Open Source 8.10; node-redis 6.3", vs=True, status="stable",
        q_en=r"""What is a cache hit and a cache miss, and what are the steps of cache-aside?""",
        q_bn=r"""Cache hit আর cache miss কী, আর cache-aside-এর ধাপগুলো কী কী?""",
        a_en=r"""A hit means the data was found in the cache; a miss means it wasn't, so you go to the database. Cache-aside: read Redis first; on a miss, read the DB, save the result in Redis with a TTL, and return it; on writes, update the DB and delete the cached key.""",
        a_bn=r"""Hit মানে data cache-এ পাওয়া গেছে; miss মানে পাওয়া যায়নি, তাই database-এ যেতে হয়। Cache-aside: আগে Redis পড়ো; miss হলে DB পড়ো, result TTL-সহ Redis-এ রাখো, তারপর return করো; write-এর সময় DB update করে cached key delete করো।""",
        code=r"""
            async function getProduct(id) {
              const key = `product:${id}`;
              const cached = await redis.get(key);
              if (cached) return JSON.parse(cached);                 // hit
              const product = await db.findProduct(id);              // miss → DB
              await redis.set(key, JSON.stringify(product), { expiration: { type: 'EX', value: 300 } });
              return product;
            }
        """, lang="javascript",
        ex_en=r"""Always set a TTL: without one, a missed invalidation means stale data forever. Delete the key on update rather than writing the new value, which avoids races between two writers.""",
        ex_bn=r"""সবসময় TTL দাও: না দিলে একবার invalidation miss হলে stale data চিরকাল থাকে। Update-এর সময় নতুন value লেখার বদলে key delete করো, তাতে দুই writer-এর race এড়ানো যায়।""",
        tip_en=r"""Say the four steps in order and finish with "TTL as a safety net, delete on write".""",
        tip_bn=r"""চারটা ধাপ ক্রম অনুযায়ী বলো, আর শেষে বলো "safety net হিসেবে TTL, write-এ delete"।""",
        follow=[("How is cache-aside different from write-through?", "Cache-aside আর write-through-এর পার্থক্য কী?")],
        related=["redis-005", "redis-013", "redis-014"],
        refs=[R_NODE],
    ),
    # ------------------------------------------------------------------ redis-q06
    Q(
        id="redis-q06", sub="Persistence (RDB/AOF)", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["persistence", "rdb", "aof"],
        ver=VER, vs=False, status="stable",
        q_en=r"""Redis keeps data in RAM. Does it lose everything on restart? What are RDB and AOF?""",
        q_bn=r"""Redis data RAM-এ রাখে। Restart করলে কি সব হারিয়ে যায়? RDB আর AOF কী?""",
        a_en=r"""Not necessarily: Redis can persist to disk. RDB saves a point-in-time snapshot every so often (compact, fast restarts, but you lose writes since the last snapshot). AOF logs every write and replays it on restart; with `appendfsync everysec` you lose about one second of writes. Many setups use both.""",
        a_bn=r"""জরুরি না: Redis disk-এ persist করতে পারে। RDB মাঝে মাঝে point-in-time snapshot নেয় (ছোট file, দ্রুত restart, কিন্তু শেষ snapshot-এর পরের write হারায়)। AOF প্রতিটা write log করে আর restart-এ replay করে; `appendfsync everysec`-এ মোটামুটি এক second-এর write হারাতে পারে। অনেক setup-এ দুটোই চালু থাকে।""",
        code=r"""
            # redis.conf
            save 3600 1 300 100 60 10000   # RDB: snapshot if N changes in M seconds
            appendonly yes                  # turn AOF on
            appendfsync everysec            # fsync once per second
        """, lang="text",
        ex_en=r"""For a pure cache you may turn persistence off: the database is the source of truth. For sessions or queues, use AOF so a restart doesn't log everyone out or drop jobs.""",
        ex_bn=r"""শুধু cache হলে persistence বন্ধ রাখতে পারো: database-ই source of truth। Session বা queue-এর জন্য AOF ব্যবহার করো, যাতে restart-এ সবাই logout না হয় বা job না হারায়।""",
        tip_en=r"""Answer "snapshot vs write log", then tie the choice to the data: cache, sessions or queue.""",
        tip_bn=r""""Snapshot বনাম write log" বলো, তারপর data অনুযায়ী choice মেলাও: cache, session নাকি queue।""",
        follow=[("Which persistence would you use for a pure cache?", "শুধু cache-এর জন্য কোন persistence ব্যবহার করবে?")],
        related=["redis-027", "redis-006"],
        refs=[R_PERSIST],
    ),
    # ------------------------------------------------------------------ redis-q07
    Q(
        id="redis-q07", sub="Pub/Sub vs Streams", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["pubsub", "streams", "messaging"],
        ver=VER, vs=False, status="stable",
        q_en=r"""In one line each: what is Redis Pub/Sub, and what is a Redis Stream?""",
        q_bn=r"""এক line করে বলো: Redis Pub/Sub কী, আর Redis Stream কী?""",
        a_en=r"""Pub/Sub is a live broadcast: a published message goes only to clients subscribed at that moment and is never stored. A Stream is a stored, append-only log: messages stay until trimmed, can be read again, and consumer groups share work with acknowledgements.""",
        a_bn=r"""Pub/Sub হলো live broadcast: publish করা message শুধু সেই মুহূর্তে subscribe করা client-রা পায়, কোথাও store হয় না। Stream হলো store করা append-only log: trim না করা পর্যন্ত message থাকে, আবার পড়া যায়, আর consumer group acknowledgement-সহ কাজ ভাগ করে নেয়।""",
        code=r"""
            PUBLISH news "hello"        # (integer) 0 → nobody subscribed, message is gone
            XADD orders * status paid   # returns an auto-generated ID like "1761460000000-0"
            XRANGE orders - +           # the entry is still there to read later
        """, lang="text",
        ex_en=r"""Rule of thumb: losing a message is fine (typing indicators, live notifications) → Pub/Sub; every message must be processed (orders, jobs) → Streams.""",
        ex_bn=r"""সহজ নিয়ম: message হারালে সমস্যা নেই (typing indicator, live notification) → Pub/Sub; প্রতিটা message process করতেই হবে (order, job) → Streams।""",
        tip_en=r"""Use the words "fire-and-forget" for Pub/Sub and "persistent log with consumer groups" for Streams.""",
        tip_bn=r"""Pub/Sub-এর জন্য "fire-and-forget" আর Streams-এর জন্য "consumer group-সহ persistent log" কথাগুলো বলো।""",
        follow=[("What happens to Pub/Sub messages while a subscriber is offline?", "Subscriber offline থাকলে Pub/Sub message-এর কী হয়?")],
        related=["redis-015", "redis-009", "redis-021"],
        refs=[R_STREAMS],
    ),
    # ------------------------------------------------------------------ redis-q08
    Q(
        id="redis-q08", sub="Redis vs Memcached", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["memcached", "comparison", "caching"],
        ver=VER, vs=False, status="stable",
        q_en=r"""Name two things Redis can do that Memcached can't.""",
        q_bn=r"""Redis পারে কিন্তু Memcached পারে না, এমন দুটো জিনিস বলো।""",
        a_en=r"""Redis has rich data types with atomic server-side operations (hashes, lists, sorted sets, streams), while Memcached stores only plain string values. Redis can also persist data to disk and replicate it, while Memcached is a purely in-memory cache that loses everything on restart.""",
        a_bn=r"""Redis-এ server-side atomic operation-সহ rich data type আছে (hash, list, sorted set, stream), আর Memcached শুধু সাধারণ string value রাখে। Redis data disk-এ persist আর replicate করতে পারে, অথচ Memcached পুরোপুরি in-memory cache, restart হলে সব হারায়।""",
        ex_en=r"""Others you can mention: Pub/Sub, Streams, Lua scripting and transactions. Memcached's strength is a simple multi-threaded string cache.""",
        ex_bn=r"""আরও বলা যায়: Pub/Sub, Streams, Lua scripting আর transaction। Memcached-এর শক্তি হলো সহজ multi-threaded string cache।""",
        tip_en=r"""Give the two differences, then say when Memcached still makes sense, so it sounds like a judgement, not a fan answer.""",
        tip_bn=r"""দুটো পার্থক্য বলো, তারপর বলো কখন Memcached এখনও ঠিক আছে, তাতে উত্তরটা fan-এর মতো না শুনিয়ে বিচার-বিবেচনার মতো শোনাবে।""",
        follow=[("When would you still choose Memcached?", "কখন এখনও Memcached বেছে নেবে?")],
        related=["redis-011"],
        refs=[R_INTRO],
    ),
    # ------------------------------------------------------------------ redis-q09
    Q(
        id="redis-q09", sub="Eviction Policies", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["eviction", "maxmemory", "ttl"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between expiry and eviction in Redis?""",
        q_bn=r"""Redis-এ expiry আর eviction-এর পার্থক্য কী?""",
        a_en=r"""Expiry is planned: you give a key a TTL and Redis deletes it when the time is up. Eviction happens when memory reaches `maxmemory`: Redis removes keys according to `maxmemory-policy`, such as `allkeys-lru` (least recently used). The default, `noeviction`, removes nothing and rejects writes instead.""",
        a_bn=r"""Expiry পরিকল্পিত: key-কে TTL দাও, সময় শেষ হলে Redis সেটা মুছে দেয়। Eviction হয় যখন memory `maxmemory`-তে পৌঁছায়: তখন Redis `maxmemory-policy` অনুযায়ী key সরায়, যেমন `allkeys-lru` (সবচেয়ে কম সম্প্রতি ব্যবহৃত)। Default `noeviction` কিছু মোছে না, বরং write reject করে।""",
        code=r"""
            # redis.conf for a pure cache
            maxmemory 2gb
            maxmemory-policy allkeys-lru
        """, lang="text",
        ex_en=r"""`volatile-*` policies only evict keys that have a TTL. If most keys have no TTL, they behave almost like `noeviction`.""",
        ex_bn=r"""`volatile-*` policy শুধু TTL-ওয়ালা key evict করে। বেশিরভাগ key-এর TTL না থাকলে এরা প্রায় `noeviction`-এর মতোই আচরণ করে।""",
        tip_en=r"""Say "expiry = time-based, eviction = memory-based", then name the default and the usual cache setting.""",
        tip_bn=r"""বলো "expiry = সময়ভিত্তিক, eviction = memory-ভিত্তিক", তারপর default আর cache-এর সাধারণ setting-এর নাম বলো।""",
        follow=[("Which policy would you use if Redis also stores sessions?", "Redis-এ session-ও থাকলে কোন policy ব্যবহার করবে?")],
        related=["redis-017", "redis-026"],
        refs=[R_EVICT],
    ),
    # ------------------------------------------------------------------ redis-q10
    Q(
        id="redis-q10", sub="Atomicity & Transactions", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["pipelining", "multi", "transactions", "performance"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is the difference between pipelining and a `MULTI`/`EXEC` transaction?""",
        q_bn=r"""Pipelining আর `MULTI`/`EXEC` transaction-এর পার্থক্য কী?""",
        a_en=r"""Pipelining is a network trick: the client sends many commands without waiting for each reply, saving round trips, but other clients' commands can run in between. `MULTI`/`EXEC` queues commands and runs them as one isolated block that nothing interrupts, though there's no rollback if one command fails.""",
        a_bn=r"""Pipelining হলো network-এর কৌশল: client প্রতিটা reply-এর অপেক্ষা না করে অনেক command পাঠায়, তাতে round trip বাঁচে, কিন্তু মাঝখানে অন্য client-এর command চলতে পারে। `MULTI`/`EXEC` command-গুলো queue করে একটা isolated block হিসেবে চালায়, মাঝে কেউ ঢুকতে পারে না, তবে কোনো command fail করলে rollback হয় না।""",
        ex_en=r"""They combine: a client can send a whole `MULTI` … `EXEC` block in one pipeline. For logic like "read, decide, then write" atomically, use a Lua script instead.""",
        ex_bn=r"""দুটো একসাথেও চলে: client পুরো `MULTI` … `EXEC` block একটা pipeline-এ পাঠাতে পারে। "পড়ো, সিদ্ধান্ত নাও, তারপর লেখো" ধরনের logic atomically করতে Lua script ব্যবহার করো।""",
        tip_en=r"""Say "pipelining = speed, `MULTI` = isolation", and mention "no rollback" to show you know the catch.""",
        tip_bn=r"""বলো "pipelining = speed, `MULTI` = isolation", আর "rollback নেই" কথাটা বলে দেখাও যে catch-টা জানো।""",
        follow=[("What happens in `EXEC` if one queued command fails at runtime?", "Queue করা একটা command runtime-এ fail করলে `EXEC`-এ কী হয়?")],
        related=["redis-029", "redis-002"],
        refs=[R_PIPE],
    ),
]

save("redis", "quick", QUESTIONS)
