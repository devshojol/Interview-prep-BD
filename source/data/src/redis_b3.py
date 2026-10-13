# Redis — batch 3 (redis-008, 009, 017, 018, 019, 026, 027, 031)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_NODE = ("Redis docs — node-redis guide", "https://redis.io/docs/latest/develop/clients/nodejs/")
R_IOREDIS = ("Redis docs — ioredis guide", "https://redis.io/docs/latest/develop/clients/ioredis/")
R_SET = ("Redis docs — SET", "https://redis.io/docs/latest/commands/set/")
R_EXPIRE = ("Redis docs — EXPIRE", "https://redis.io/docs/latest/commands/expire/")
R_HEXPIRE = ("Redis docs — HEXPIRE", "https://redis.io/docs/latest/commands/hexpire/")
R_HSETEX = ("Redis docs — HSETEX", "https://redis.io/docs/latest/commands/hsetex/")
R_PUBSUB = ("Redis docs — Pub/Sub", "https://redis.io/docs/latest/develop/pubsub/")
R_EVICTION = ("Redis docs — Key eviction", "https://redis.io/docs/latest/develop/reference/eviction/")
R_MEMUSAGE = ("Redis docs — MEMORY USAGE", "https://redis.io/docs/latest/commands/memory-usage/")
R_INFO = ("Redis docs — INFO", "https://redis.io/docs/latest/commands/info/")
R_PERSIST = ("Redis docs — Persistence", "https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/")
R_LATENCY = ("Redis docs — Diagnosing latency issues", "https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/")
R_LUA = ("Redis docs — Scripting with Lua", "https://redis.io/docs/latest/develop/programmability/eval-intro/")
R_CLUSTER = ("Redis docs — Scale with Redis Cluster", "https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/")
R_STREAMS = ("Redis docs — Streams", "https://redis.io/docs/latest/develop/data-types/streams/")
OWASP_SESSION = ("OWASP — Session Management Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ redis-008
    Q(
        id="redis-008", sub="Session Storage", diff="easy", type="scenario",
        prio="high", market="both", mins=5,
        tags=["sessions", "express", "load-balancer", "ttl", "cookies"],
        ver="node-redis 6.3; Redis Open Source 8.10; Express 5.3", vs=True, status="stable",
        q_en=r"""Your Express app runs 3 instances behind a load balancer and stores sessions in memory (the default store). Users complain they get logged out randomly. Why, and how would you fix it with Redis?""",
        q_bn=r"""তোমার Express app load balancer-এর পেছনে 3টা instance-এ চলে, আর session রাখে memory-তে (default store)। User-রা অভিযোগ করছে যে তারা হঠাৎ হঠাৎ logout হয়ে যায়। কেন, আর Redis দিয়ে কীভাবে ঠিক করবে?""",
        a_en=r"""
            Each instance has its own memory, so a session created on instance A doesn't exist on B or C. When the load balancer sends the next request elsewhere, the user looks logged out. Restarts and deploys also wipe in-memory sessions.

            Fix: move sessions to a **shared Redis store**:
            - At login, generate a random session id, store `sess:<id>` in Redis with a TTL (e.g. 24 h), and send only the id in a cookie.
            - On each request, load the session by id; refresh the TTL for **sliding expiration** if you want "log out after 24 h of inactivity".
            - On logout, `DEL` the key — the session is revoked immediately on every instance.

            Sticky sessions at the load balancer would hide the symptom but break on restarts and uneven load, so a shared store is the proper fix. In practice `express-session` with a Redis store package does this for you; the logic underneath is the same.
        """,
        a_bn=r"""
            প্রতিটা instance-এর memory আলাদা, তাই instance A-তে তৈরি হওয়া session B বা C-তে থাকে না। Load balancer পরের request অন্য instance-এ পাঠালেই user-কে logged out দেখায়। Restart আর deploy-এও in-memory session মুছে যায়।

            সমাধান: session-গুলো একটা **shared Redis store**-এ সরাও:
            - Login-এর সময় random session id তৈরি করো, Redis-এ TTL (যেমন 24 ঘণ্টা) সহ `sess:<id>` রাখো, আর cookie-তে শুধু id পাঠাও।
            - প্রতিটা request-এ id দিয়ে session load করো; "24 ঘণ্টা inactive থাকলে logout" চাইলে **sliding expiration**-এর জন্য TTL refresh করো।
            - Logout-এ key `DEL` করো — সব instance-এ session সাথে সাথে বাতিল হয়ে যায়।

            Load balancer-এ sticky session দিলে symptom লুকানো যায়, কিন্তু restart আর অসম load-এ সেটা ভেঙে পড়ে; তাই shared store-ই সঠিক সমাধান। বাস্তবে Redis store package সহ `express-session` এই কাজটা করে দেয়; ভেতরের logic একই।
        """,
        ex_en=r"""
            - **Security basics:** the session id must be long and random (e.g. 32 bytes from `crypto.randomBytes`); the cookie should be `HttpOnly`, `Secure` and `SameSite`; regenerate the id after login to prevent session fixation.
            - **What to store:** keep sessions small — user id, role, CSRF token. Don't cache the whole user profile there.
            - **Logout everywhere:** keep a set `user:<id>:sessions` of session ids so "log out of all devices" can delete them all.
            - **Durability:** if Redis restarts without persistence, everyone is logged out. Enable RDB/AOF or use a replicated setup for session data, and use the `noeviction` policy so live sessions aren't evicted under memory pressure — `volatile-*` policies wouldn't protect them, because every session key has a TTL.
            - **Default MemoryStore** in `express-session` is explicitly not meant for production — it leaks memory and doesn't scale past one process.
        """,
        ex_bn=r"""
            - **Security-র মৌলিক দিক:** session id লম্বা আর random হতে হবে (যেমন `crypto.randomBytes` থেকে 32 byte); cookie হবে `HttpOnly`, `Secure` আর `SameSite`; session fixation ঠেকাতে login-এর পর id নতুন করে তৈরি করো।
            - **কী রাখবে:** session ছোট রাখো — user id, role, CSRF token। পুরো user profile সেখানে cache কোরো না।
            - **সব জায়গা থেকে logout:** `user:<id>:sessions` নামে একটা set-এ session id-গুলো রাখো, যাতে "সব device থেকে logout" করলে সবগুলো delete করা যায়।
            - **Durability:** persistence ছাড়া Redis restart হলে সবাই logout হয়ে যাবে। Session data-র জন্য RDB/AOF চালু করো বা replicated setup রাখো, আর `noeviction` policy দাও যাতে memory চাপে live session evict না হয় — `volatile-*` policy এখানে রক্ষা করবে না, কারণ প্রতিটা session key-এরই TTL আছে।
            - `express-session`-এর **default MemoryStore** স্পষ্টভাবেই production-এর জন্য নয় — এটা memory leak করে আর এক process-এর বাইরে scale করে না।
        """,
        tip_en=r"""Explain the root cause (per-process memory) before the fix, then mention one security detail (cookie flags or session fixation). That shows you think beyond "just use Redis".""",
        tip_bn=r"""সমাধানের আগে root cause (প্রতিটা process-এর আলাদা memory) ব্যাখ্যা করো, তারপর একটা security detail (cookie flag বা session fixation) উল্লেখ করো। এতে বোঝা যায় তুমি "শুধু Redis ব্যবহার করো"-র বাইরেও ভাবো।""",
        mist_en=r"""Storing the whole session in a JWT/cookie and calling it the same thing (you lose server-side revocation), or putting sessions in a cache instance with `allkeys-lru`, where active users can be evicted.""",
        mist_bn=r"""পুরো session JWT/cookie-তে রেখে একই জিনিস বলে দাবি করা (server-side revocation হারাও), অথবা `allkeys-lru` policy-র cache instance-এ session রাখা — যেখানে active user-ও evict হয়ে যেতে পারে।""",
        code=r"""
            import { randomBytes } from 'node:crypto';

            const SESSION_TTL = 60 * 60 * 24; // 24 h

            // Login: create the session
            export async function createSession(redis, res, user) {
              const sid = randomBytes(32).toString('base64url');
              await redis.set(`sess:${sid}`, JSON.stringify({ userId: user.id, role: user.role }), {
                expiration: { type: 'EX', value: SESSION_TTL },
              });
              res.cookie('sid', sid, { httpOnly: true, secure: true, sameSite: 'lax', maxAge: SESSION_TTL * 1000 });
            }

            // Middleware: load the session and slide its expiry (GETEX = GET + new TTL)
            export function sessionMiddleware(redis) {
              return async (req, res, next) => {
                const sid = req.cookies?.sid;
                if (!sid) return next();
                const raw = await redis.getEx(`sess:${sid}`, { type: 'EX', value: SESSION_TTL });
                req.session = raw ? JSON.parse(raw) : null;
                next();
              };
            }

            // Logout: revoke immediately on every instance
            export const destroySession = (redis, sid) => redis.del(`sess:${sid}`);
        """,
        lang="javascript",
        follow=[
            ("Sessions in Redis or JWTs — what are the trade-offs?", "Redis-এ session নাকি JWT — trade-off কী কী?"),
            ("Which eviction policy should a Redis instance that stores sessions use?", "Session রাখা Redis instance-এ কোন eviction policy ব্যবহার করা উচিত?"),
        ],
        related=["redis-004", "redis-017"],
        refs=[R_NODE, OWASP_SESSION],
    ),
    # ------------------------------------------------------------------ redis-009
    Q(
        id="redis-009", sub="Pub/Sub", diff="easy", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["pubsub", "delivery-semantics", "messaging"],
        ver="Version-independent concept (Redis Open Source 8.10)", vs=False, status="stable",
        q_en=r"""A notification service subscribes to the Redis Pub/Sub channel `orders`. It restarts and is offline for 30 seconds, during which 50 messages are published. What happens to those 50 messages?""",
        q_bn=r"""একটা notification service Redis Pub/Sub channel `orders`-এ subscribe করা। Service-টা restart হয়ে 30 সেকেন্ড offline ছিল, আর এই সময়ে 50টা message publish হয়েছে। ওই 50টা message-এর কী হবে?""",
        options=[
            ("Redis buffers them and delivers all 50 when the service re-subscribes", "Redis এগুলো buffer করে রাখে, আর service আবার subscribe করলে 50টাই deliver করে"),
            ("`PUBLISH` fails with an error while there are no subscribers", "কোনো subscriber না থাকলে `PUBLISH` error দিয়ে fail করে"),
            ("They are lost — Pub/Sub only delivers to subscribers connected at publish time", "এগুলো হারিয়ে যায় — Pub/Sub শুধু publish-এর সময় connected subscriber-দের কাছেই পাঠায়"),
            ("They are kept only if AOF persistence is enabled", "শুধু AOF persistence চালু থাকলে এগুলো রাখা হয়"),
        ],
        correct=2,
        a_en=r"""They are lost. Redis Pub/Sub is fire-and-forget with at-most-once delivery: a message goes only to clients subscribed at that instant and is never stored.""",
        a_bn=r"""এগুলো হারিয়ে যায়। Redis Pub/Sub fire-and-forget, at-most-once delivery: message শুধু ওই মুহূর্তে subscribe করা client-দের কাছে যায়, কখনো store হয় না।""",
        ex_en=r"""
            Option A is what people *expect* from a message broker, but Pub/Sub has no queue or history. `PUBLISH` doesn't fail when nobody is listening — it simply returns the number of clients that received the message (here `0`). Persistence settings (option D) are irrelevant because messages never enter the keyspace.

            If missed messages matter, use **Redis Streams** with consumer groups: messages are stored, consumers resume from where they left off, and unacknowledged messages can be re-delivered. Also note that a very slow subscriber can be disconnected when its output buffer exceeds `client-output-buffer-limit pubsub`, losing messages too.
        """,
        ex_bn=r"""
            Option A হলো message broker-এর কাছে মানুষ যা *আশা* করে, কিন্তু Pub/Sub-এ কোনো queue বা history নেই। কেউ না শুনলেও `PUBLISH` fail করে না — শুধু কতজন client message পেয়েছে সেই সংখ্যা return করে (এখানে `0`)। Persistence setting (option D) এখানে অপ্রাসঙ্গিক, কারণ message কখনো keyspace-এ ঢোকেই না।

            Miss হওয়া message গুরুত্বপূর্ণ হলে consumer group সহ **Redis Streams** ব্যবহার করো: message store হয়, consumer যেখানে থেমেছিল সেখান থেকে আবার শুরু করে, আর acknowledge না হওয়া message আবার deliver করা যায়। আরও মনে রাখো, খুব ধীর subscriber-এর output buffer `client-output-buffer-limit pubsub` ছাড়িয়ে গেলে তাকে disconnect করে দেওয়া হয়, তাতেও message হারায়।
        """,
        tip_en=r"""Say "at-most-once" explicitly and name Streams as the alternative. Knowing the return value of `PUBLISH` is a nice extra detail.""",
        tip_bn=r""""At-most-once" কথাটা স্পষ্ট করে বলো আর বিকল্প হিসেবে Streams-এর নাম বলো। `PUBLISH`-এর return value জানা থাকলে সেটা বাড়তি ভালো detail।""",
        extra=[dict(lang="text", label_en="PUBLISH with no subscriber connected", label_bn="কোনো subscriber connected না থাকলে PUBLISH", src=r"""
            127.0.0.1:6379> PUBLISH orders "order:981 created"
            (integer) 0
        """)],
        refs=[R_PUBSUB, R_STREAMS],
        related=["redis-015", "redis-021"],
    ),
    # ------------------------------------------------------------------ redis-017
    Q(
        id="redis-017", sub="Eviction Policies", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["eviction", "maxmemory", "allkeys-lru", "oom"],
        ver="Redis Open Source 8.10 (LRM policies since 8.6)", vs=True, status="stable",
        q_en=r"""Redis is used **only as a cache** for API responses with `maxmemory 2gb`. After a week, writes fail with `OOM command not allowed when used memory > 'maxmemory'`. Most keys were written without a TTL. What is the best configuration fix?""",
        q_bn=r"""Redis **শুধু cache** হিসেবে API response রাখার কাজে ব্যবহার হচ্ছে, `maxmemory 2gb` দেওয়া। এক সপ্তাহ পরে write-গুলো `OOM command not allowed when used memory > 'maxmemory'` error দিয়ে fail করছে। বেশিরভাগ key TTL ছাড়া লেখা হয়েছিল। সবচেয়ে ভালো configuration fix কী?""",
        options=[
            ("Set `maxmemory-policy volatile-lru`", "`maxmemory-policy volatile-lru` set করা"),
            ("Set `maxmemory-policy allkeys-lru` (or `allkeys-lfu`)", "`maxmemory-policy allkeys-lru` (বা `allkeys-lfu`) set করা"),
            ("Remove `maxmemory` so Redis can use all the RAM on the server", "`maxmemory` সরিয়ে দেওয়া, যাতে Redis server-এর সব RAM ব্যবহার করতে পারে"),
            ("Enable AOF so that data overflows to disk when memory is full", "AOF চালু করা, যাতে memory ভরে গেলে data disk-এ চলে যায়"),
        ],
        correct=1,
        a_en=r"""Set `maxmemory-policy allkeys-lru` (or `allkeys-lfu`). The default policy is `noeviction`, which rejects writes at the limit; an `allkeys-*` policy lets Redis evict any key, which is exactly what a pure cache wants.""",
        a_bn=r"""`maxmemory-policy allkeys-lru` (বা `allkeys-lfu`) set করো। Default policy হলো `noeviction`, যেটা limit-এ পৌঁছালে write reject করে; `allkeys-*` policy Redis-কে যেকোনো key evict করতে দেয় — pure cache-এর ঠিক এটাই দরকার।""",
        ex_en=r"""
            Option A is the trap: `volatile-*` policies only evict keys that **have a TTL**. With most keys lacking one, Redis finds little or nothing to evict and behaves like `noeviction`. Option C risks the OS swapping or the OOM killer terminating Redis. Option D confuses persistence with memory — AOF is a durability log, not overflow storage.

            Choosing between them: `allkeys-lru` evicts least recently used keys; `allkeys-lfu` evicts least frequently used ones, which works better when a small set of keys is consistently popular. Redis 8.6 added `allkeys-lrm`/`volatile-lrm` (least recently *modified*). LRU/LFU are approximated by sampling (`maxmemory-samples`). Even with eviction, still give cache keys TTLs so stale data disappears on its own, and watch `evicted_keys` in `INFO stats`.
        """,
        ex_bn=r"""
            Option A-টাই ফাঁদ: `volatile-*` policy শুধু **TTL আছে এমন** key evict করে। বেশিরভাগ key-এ TTL না থাকায় Redis evict করার মতো প্রায় কিছুই পায় না, ফলে আচরণ `noeviction`-এর মতোই হয়। Option C-তে OS swap করতে পারে বা OOM killer Redis-কে মেরে ফেলতে পারে। Option D persistence আর memory গুলিয়ে ফেলে — AOF হলো durability log, overflow storage নয়।

            কোনটা বেছে নেবে: `allkeys-lru` সবচেয়ে কম সম্প্রতি ব্যবহৃত key evict করে; `allkeys-lfu` সবচেয়ে কম ঘনঘন ব্যবহৃত key evict করে — অল্প কিছু key নিয়মিত জনপ্রিয় থাকলে এটা ভালো কাজ করে। Redis 8.6 যোগ করেছে `allkeys-lrm`/`volatile-lrm` (least recently *modified*)। LRU/LFU sampling দিয়ে approximate করা হয় (`maxmemory-samples`)। Eviction থাকলেও cache key-গুলোতে TTL দাও যাতে stale data নিজে থেকেই মুছে যায়, আর `INFO stats`-এ `evicted_keys` নজরে রাখো।
        """,
        tip_en=r"""Mention that the right policy depends on what the instance stores: `allkeys-*` for a pure cache, `noeviction` for queues, sessions or anything you can't lose — and that's why many teams run separate Redis instances for each.""",
        tip_bn=r"""বলো যে সঠিক policy নির্ভর করে instance-এ কী রাখা হচ্ছে তার ওপর: pure cache-এর জন্য `allkeys-*`, আর queue, session বা হারানো যাবে না এমন কিছুর জন্য `noeviction` — এজন্যই অনেক team প্রতিটার জন্য আলাদা Redis instance চালায়।""",
        extra=[dict(lang="text", label_en="Cache instance configuration", label_bn="Cache instance-এর configuration", src=r"""
            # redis.conf (or CONFIG SET at runtime)
            maxmemory 2gb
            maxmemory-policy allkeys-lru
        """)],
        refs=[R_EVICTION, R_INFO],
        related=["redis-026", "redis-008"],
    ),
    # ------------------------------------------------------------------ redis-018
    Q(
        id="redis-018", sub="TTL & Expiration", diff="medium", type="conceptual",
        prio="medium", market="both", mins=6,
        tags=["ttl", "expiration", "hexpire", "hsetex", "hash-field-expiration"],
        ver="Redis Open Source 8.10 (HEXPIRE since 7.4; HGETEX/HSETEX since 8.0)", vs=True, status="version-specific",
        q_en=r"""How does Redis actually expire keys internally? Why might memory not drop immediately after many keys expire, and how can you expire individual fields inside a hash?""",
        q_bn=r"""Redis ভেতরে ভেতরে আসলে কীভাবে key expire করে? অনেক key expire হওয়ার পরও memory সাথে সাথে কমে না কেন, আর hash-এর ভেতরের আলাদা field কীভাবে expire করা যায়?""",
        a_en=r"""
            Redis combines two mechanisms:
            - **Passive (lazy) expiry:** when a client touches a key, Redis checks its expiry time and deletes it if it has passed, so you never read an expired key.
            - **Active expiry:** a background cycle runs several times per second, samples keys that have a TTL, deletes the expired ones, and repeats while a large share of the sample is expired.

            Because active expiry is sampling-based, expired keys that nobody reads can linger briefly. And even after deletion, the process's RSS may stay high because the allocator doesn't always return freed memory to the OS — you'll see that as fragmentation in `INFO memory`.

            For **per-field expiry** in hashes (Redis 7.4+), use `HEXPIRE`/`HPEXPIRE`, inspect with `HTTL`, remove with `HPERSIST`. Redis 8.0 added `HSETEX` (set fields with a TTL in one command) and `HGETEX` (read fields and set/clear their TTL). Before this, people split such data into separate keys just to get separate TTLs.
        """,
        a_bn=r"""
            Redis দুইটা পদ্ধতি একসাথে ব্যবহার করে:
            - **Passive (lazy) expiry:** client কোনো key ছুঁলে Redis তার expiry time check করে, পেরিয়ে গেলে delete করে দেয় — তাই expired key কখনো পড়া যায় না।
            - **Active expiry:** একটা background cycle প্রতি সেকেন্ডে কয়েকবার চলে, TTL-ওয়ালা key থেকে sample নেয়, expired গুলো delete করে, আর sample-এর বড় অংশ expired হলে আবার চালায়।

            Active expiry sampling-ভিত্তিক বলে যে expired key কেউ পড়ে না সেগুলো কিছুক্ষণ থেকে যেতে পারে। আর delete হওয়ার পরও process-এর RSS বেশি থাকতে পারে, কারণ allocator সবসময় মুক্ত memory OS-কে ফেরত দেয় না — `INFO memory`-তে এটা fragmentation হিসেবে দেখা যায়।

            Hash-এ **per-field expiry**-র জন্য (Redis 7.4+) `HEXPIRE`/`HPEXPIRE` ব্যবহার করো, `HTTL` দিয়ে দেখো, `HPERSIST` দিয়ে সরাও। Redis 8.0 যোগ করেছে `HSETEX` (এক command-এ TTL সহ field set) আর `HGETEX` (field পড়া আর তার TTL set/clear করা)। আগে আলাদা TTL পাওয়ার জন্যই মানুষ এই data আলাদা আলাদা key-তে ভাগ করত।
        """,
        ex_en=r"""
            - **Replicas:** replicas don't expire keys on their own; they wait for the primary to send a `DEL`. They do, however, report logically expired keys as missing on reads, so clients stay consistent.
            - **Mass expiry and latency:** if a huge number of keys share the same expiry second, the active cycle can spend noticeable time deleting them — another reason to add jitter to TTLs.
            - **Hash field expiry use case:** one hash per user holding short-lived items, e.g. `otp:attempts:<phone>` with one field per attempt that expires after 10 minutes, or a cart hash where reserved items expire individually.
            - **What clears a TTL:** commands that replace the value (`SET`, `GETSET`) or `PERSIST`; renaming keeps it.
        """,
        ex_bn=r"""
            - **Replica:** replica নিজে থেকে key expire করে না; primary `DEL` পাঠানো পর্যন্ত অপেক্ষা করে। তবে read-এর সময় logically expired key-কে নেই হিসেবেই দেখায়, তাই client-এর কাছে ফল সামঞ্জস্যপূর্ণ থাকে।
            - **একসাথে অনেক expiry আর latency:** বিশাল সংখ্যক key একই সেকেন্ডে expire হলে active cycle সেগুলো delete করতে উল্লেখযোগ্য সময় নিতে পারে — TTL-এ jitter দেওয়ার আরেকটা কারণ।
            - **Hash field expiry-র use case:** প্রতি user-এর জন্য একটা hash-এ স্বল্পস্থায়ী item রাখা, যেমন `otp:attempts:<phone>`-এ প্রতিটা attempt একটা field যেটা 10 মিনিট পরে expire হয়, বা cart hash যেখানে reserved item আলাদাভাবে expire হয়।
            - **কী কী TTL মুছে দেয়:** value replace করা command (`SET`, `GETSET`) বা `PERSIST`; rename করলে TTL থেকে যায়।
        """,
        tip_en=r"""Explain lazy + active expiry in two sentences, then show you're current by mentioning hash field expiration and the Redis 8 `HSETEX`/`HGETEX` commands.""",
        tip_bn=r"""Lazy + active expiry দুই বাক্যে ব্যাখ্যা করো, তারপর hash field expiration আর Redis 8-এর `HSETEX`/`HGETEX` command উল্লেখ করে দেখাও তুমি হালনাগাদ আছো।""",
        mist_en=r"""Thinking Redis runs a timer per key, or assuming `EXPIRE` on a hash key expires individual fields (it expires the whole hash).""",
        mist_bn=r"""ভাবা যে Redis প্রতিটা key-এর জন্য আলাদা timer চালায়, অথবা ধরে নেওয়া যে hash key-তে `EXPIRE` দিলে আলাদা field expire হয় (আসলে পুরো hash expire হয়)।""",
        code=r"""
            # Redis 7.4+: expire individual hash fields
            HSET cart:7 item:101 "2" item:205 "1"
            HEXPIRE cart:7 900 FIELDS 1 item:205
            HTTL cart:7 FIELDS 2 item:101 item:205
            # 1) (integer) -1     <- no TTL on item:101
            # 2) (integer) 900    <- item:205 expires in 15 min

            # Redis 8.0+: set fields and their TTL in one command
            HSETEX otp:attempts:01712 EX 600 FIELDS 1 attempt:1 "failed"
            HGETEX otp:attempts:01712 PERSIST FIELDS 1 attempt:1
        """,
        lang="text",
        follow=[
            ("Why do replicas wait for the primary to delete expired keys?", "Replica কেন expired key delete করার জন্য primary-র অপেক্ষা করে?"),
            ("How would you model per-item expiry in a shopping cart before Redis 7.4?", "Redis 7.4-এর আগে shopping cart-এ প্রতি item-এর আলাদা expiry কীভাবে model করতে?"),
        ],
        related=["redis-004", "redis-003", "redis-032"],
        refs=[R_EXPIRE, R_HEXPIRE, R_HSETEX],
    ),
    # ------------------------------------------------------------------ redis-019
    Q(
        id="redis-019", sub="Node.js Integration", diff="medium", type="conceptual",
        prio="high", market="both", mins=7,
        tags=["node-redis", "ioredis", "nodejs", "connections", "resp3"],
        ver="node-redis 6.3; ioredis 6.0; Node.js 24 LTS", vs=True, status="stable",
        q_en=r"""How do you integrate Redis into a production Node.js service? Compare node-redis and ioredis, and explain how you handle connections, errors and shutdown.""",
        q_bn=r"""Production Node.js service-এ Redis কীভাবে integrate করো? node-redis আর ioredis তুলনা করো, আর connection, error ও shutdown কীভাবে সামলাও ব্যাখ্যা করো।""",
        a_en=r"""
            **Client choice:**
            - **node-redis (`redis` package, v6.3)** is the client Redis recommends for new projects: promise-based, camelCase commands (`hSet`, `zAdd`), first-class support for Redis 8 features (JSON, Query Engine, Vector Sets), plus `createCluster`, `createSentinel` and `createClientPool`.
            - **ioredis (v6.0)** is still maintained and very common — BullMQ, for example, builds on it. It has built-in Cluster and Sentinel support and a slightly different API (`redis.set(k, v, 'EX', 60)`).
            Both v6 lines default to **RESP3** and require Node.js 20+.

            **Connection handling:**
            - Create **one long-lived client per process** at startup and reuse it; Redis pipelines concurrent commands over one connection. Don't connect per request.
            - **Always attach an `'error'` listener** — an unhandled `'error'` event crashes the process.
            - Configure reconnects and timeouts; node-redis v6 has a default command timeout of 5 s.
            - Use **dedicated connections** for `SUBSCRIBE` and blocking commands (`BLMOVE`, `XREADGROUP BLOCK`), since they tie up the connection.
            - On shutdown (`SIGTERM`), stop accepting work and call `client.close()` so in-flight commands finish.
        """,
        a_bn=r"""
            **Client বাছাই:**
            - **node-redis (`redis` package, v6.3)** নতুন project-এর জন্য Redis-এর recommended client: promise-based, camelCase command (`hSet`, `zAdd`), Redis 8-এর feature-গুলোর (JSON, Query Engine, Vector Sets) পূর্ণ support, সাথে `createCluster`, `createSentinel` আর `createClientPool`।
            - **ioredis (v6.0)** এখনো maintained আর খুব প্রচলিত — যেমন BullMQ এর ওপর তৈরি। এতে built-in Cluster ও Sentinel support আছে, API একটু আলাদা (`redis.set(k, v, 'EX', 60)`)।
            দুটোরই v6 line default হিসেবে **RESP3** ব্যবহার করে আর Node.js 20+ লাগে।

            **Connection সামলানো:**
            - Startup-এ **প্রতি process-এ একটা long-lived client** তৈরি করে বারবার ব্যবহার করো; Redis একটা connection-এই concurrent command pipeline করে। প্রতি request-এ connect কোরো না।
            - **সবসময় `'error'` listener দাও** — handle না করা `'error'` event process crash করায়।
            - Reconnect আর timeout configure করো; node-redis v6-এ default command timeout 5 সেকেন্ড।
            - `SUBSCRIBE` আর blocking command (`BLMOVE`, `XREADGROUP BLOCK`)-এর জন্য **আলাদা connection** ব্যবহার করো, কারণ এগুলো connection আটকে রাখে।
            - Shutdown-এ (`SIGTERM`) নতুন কাজ নেওয়া বন্ধ করে `client.close()` call করো, যাতে চলমান command-গুলো শেষ হয়।
        """,
        ex_en=r"""
            - **Offline queue:** by default node-redis queues commands while disconnected and sends them after reconnecting. For a cache that's often wrong — requests hang instead of falling back to the DB. `disableOfflineQueue: true` makes commands fail fast.
            - **RESP3 default (v6):** some reply shapes changed compared with v5; pin `RESP: 2` (node-redis) or `protocol: 2` (ioredis) if you're mid-migration.
            - **node-redis v5+ API changes:** `quit()` → `close()`, `disconnect()` → `destroy()`, `scanIterator()` yields batches of keys, and expiry options use `{ expiration: { type: 'EX', value } }`.
            - **Security:** use `rediss://` (TLS) for managed Redis, an ACL user with least privilege, and keep the URL in an environment variable or secret store.
            - **Serverless:** in Lambda-style environments, create the client outside the handler so warm invocations reuse it.
        """,
        ex_bn=r"""
            - **Offline queue:** default-এ node-redis disconnected অবস্থায় command queue করে রাখে আর reconnect হলে পাঠায়। Cache-এর জন্য এটা প্রায়ই ভুল — DB-তে fallback না করে request ঝুলে থাকে। `disableOfflineQueue: true` দিলে command সাথে সাথে fail করে।
            - **RESP3 default (v6):** v5-এর তুলনায় কিছু reply-এর আকার বদলেছে; migration-এর মাঝামাঝি থাকলে `RESP: 2` (node-redis) বা `protocol: 2` (ioredis) pin করো।
            - **node-redis v5+-এর API পরিবর্তন:** `quit()` → `close()`, `disconnect()` → `destroy()`, `scanIterator()` key-এর batch দেয়, আর expiry option লেখা হয় `{ expiration: { type: 'EX', value } }` দিয়ে।
            - **Security:** managed Redis-এর জন্য `rediss://` (TLS), least privilege সহ ACL user, আর URL environment variable বা secret store-এ রাখো।
            - **Serverless:** Lambda-জাতীয় environment-এ client handler-এর বাইরে তৈরি করো, যাতে warm invocation সেটা আবার ব্যবহার করতে পারে।
        """,
        tip_en=r"""Show a small "redis.js" module from memory — single client, error listener, reconnect strategy, graceful shutdown. Concrete code beats listing features.""",
        tip_bn=r"""মনে থেকে একটা ছোট "redis.js" module দেখাও — একটা client, error listener, reconnect strategy, graceful shutdown। Feature-এর তালিকার চেয়ে concrete code বেশি কার্যকর।""",
        mist_en=r"""Creating a new Redis connection per HTTP request, forgetting the `'error'` listener, or running `SUBSCRIBE` on the same client used for normal commands.""",
        mist_bn=r"""প্রতিটা HTTP request-এ নতুন Redis connection তৈরি করা, `'error'` listener ভুলে যাওয়া, অথবা সাধারণ command-এর client-এই `SUBSCRIBE` চালানো।""",
        code=r"""
            // redis.js — one shared client per process (node-redis v6)
            import { createClient } from 'redis';

            export const redis = createClient({
              url: process.env.REDIS_URL,              // e.g. rediss://user:pass@host:6380
              disableOfflineQueue: true,               // fail fast instead of queueing while down
              socket: {
                connectTimeout: 5_000,
                reconnectStrategy: (retries) => Math.min(retries * 100, 3_000),
              },
            });

            redis.on('error', (err) => console.error('Redis error:', err.message));
            await redis.connect();

            // Dedicated connection for Pub/Sub
            export const subscriber = redis.duplicate();
            subscriber.on('error', (err) => console.error('Redis sub error:', err.message));
            await subscriber.connect();

            process.on('SIGTERM', async () => {
              await Promise.allSettled([subscriber.close(), redis.close()]);
              process.exit(0);
            });
        """,
        lang="javascript",
        follow=[
            ("Why can a blocking command like `BLMOVE` stall other requests if it shares a connection?", "`BLMOVE`-এর মতো blocking command একই connection share করলে অন্য request কেন আটকে যেতে পারে?"),
            ("How do you connect to Redis Cluster or Sentinel from node-redis?", "node-redis থেকে Redis Cluster বা Sentinel-এ কীভাবে connect করো?"),
        ],
        related=["redis-005", "redis-028"],
        refs=[R_NODE, R_IOREDIS],
    ),
    # ------------------------------------------------------------------ redis-026
    Q(
        id="redis-026", sub="Production Failure Scenarios", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["oom", "maxmemory", "big-keys", "memory-usage", "incident"],
        ver="Redis Open Source 8.10", vs=False, status="stable",
        q_en=r"""At 9 PM during a sale campaign, your API starts failing with `OOM command not allowed when used memory > 'maxmemory'` from Redis. Walk through how you'd diagnose and fix it — both right now and long term.""",
        q_bn=r"""একটা sale campaign চলাকালীন রাত 9টায় তোমার API Redis থেকে `OOM command not allowed when used memory > 'maxmemory'` error দিয়ে fail করা শুরু করল। এখনই আর দীর্ঘমেয়াদে কীভাবে diagnose ও fix করবে, ধাপে ধাপে বলো।""",
        a_en=r"""
            **1. Stabilise (minutes):**
            - `INFO memory` — compare `used_memory` with `maxmemory`, check `mem_fragmentation_ratio`. `CONFIG GET maxmemory-policy` — it's probably `noeviction`.
            - If this instance is a **pure cache**, switch to `allkeys-lru` with `CONFIG SET` so it evicts instead of rejecting writes. If it also holds sessions or queues, don't — raise `maxmemory` temporarily if the host has headroom, or free known-safe keys with `UNLINK`.
            - Make the app degrade gracefully: cache writes should fail softly and fall back to the DB.

            **2. Find what grew:**
            - `INFO keyspace` — compare `keys` with `expires`; many keys without TTL is a red flag.
            - `redis-cli --bigkeys` / `--memkeys` (SCAN-based sampling) and `MEMORY USAGE <key>` for suspects: unbounded lists, streams without `MAXLEN`, giant hashes, huge cached JSON blobs.
            - `INFO clients` / `CLIENT LIST` — large output buffers from slow Pub/Sub subscribers or replicas can eat memory too.
            - Check recent deploys: a new key pattern without a TTL is the most common culprit.

            **3. Fix for good:**
            - TTL on every cache key; cap collections (`LTRIM`, `XADD ... MAXLEN ~`).
            - Separate instances: a cache with `allkeys-*`, and a durable instance (sessions, queues) with `noeviction`.
            - Alert at ~75–80% of `maxmemory` and on `evicted_keys`; leave headroom for fork copy-on-write during RDB/AOF rewrites.
            - Capacity-plan for campaign peaks.
        """,
        a_bn=r"""
            **1. আগে স্থির করো (কয়েক মিনিটে):**
            - `INFO memory` — `used_memory` আর `maxmemory` তুলনা করো, `mem_fragmentation_ratio` দেখো। `CONFIG GET maxmemory-policy` — সম্ভবত `noeviction`।
            - Instance-টা যদি **pure cache** হয়, `CONFIG SET` দিয়ে `allkeys-lru`-তে বদলাও, যাতে write reject না করে evict করে। যদি এতে session বা queue-ও থাকে, এটা কোরো না — host-এ জায়গা থাকলে সাময়িকভাবে `maxmemory` বাড়াও, অথবা নিরাপদে মোছা যায় এমন key `UNLINK` করো।
            - App যেন সুন্দরভাবে degrade করে: cache write fail হলে চুপচাপ DB-তে fallback করবে।

            **2. কী বেড়েছে খুঁজে বের করো:**
            - `INFO keyspace` — `keys` আর `expires` তুলনা করো; TTL ছাড়া অনেক key থাকা বিপদের সংকেত।
            - `redis-cli --bigkeys` / `--memkeys` (SCAN-ভিত্তিক sampling) আর সন্দেহজনক key-এ `MEMORY USAGE <key>`: সীমাহীন list, `MAXLEN` ছাড়া stream, বিশাল hash, বড় cached JSON blob।
            - `INFO clients` / `CLIENT LIST` — ধীর Pub/Sub subscriber বা replica-র বড় output buffer-ও memory খেয়ে ফেলতে পারে।
            - সাম্প্রতিক deploy দেখো: TTL ছাড়া নতুন কোনো key pattern-ই সবচেয়ে সাধারণ কারণ।

            **3. স্থায়ী সমাধান:**
            - প্রতিটা cache key-এ TTL; collection-এর সীমা বেঁধে দাও (`LTRIM`, `XADD ... MAXLEN ~`)।
            - আলাদা instance: `allkeys-*` সহ cache, আর `noeviction` সহ durable instance (session, queue)।
            - `maxmemory`-র ~75–80%-এ আর `evicted_keys`-এ alert দাও; RDB/AOF rewrite-এর সময় fork-এর copy-on-write-এর জন্য জায়গা রাখো।
            - Campaign peak-এর জন্য capacity plan করো।
        """,
        ex_en=r"""
            - **Why `UNLINK`, not `DEL`, for big keys:** `DEL` frees memory synchronously on the main thread — deleting a key with millions of elements can block Redis. `UNLINK` removes the key immediately and reclaims memory in a background thread.
            - **Fragmentation:** if `used_memory` is moderate but RSS is much higher (ratio well above ~1.5), the allocator is holding freed memory; active defragmentation (`activedefrag`) can help.
            - **Fork overhead:** `BGSAVE`/AOF rewrite forks the process; heavy writes during the snapshot cause copy-on-write page duplication, so the host needs RAM beyond `maxmemory` or the kernel may OOM-kill Redis.
            - **Postmortem:** add a lint/check that every `set` in the codebase passes an expiration for cache keys; it's cheap insurance.
        """,
        ex_bn=r"""
            - **বড় key-এর জন্য `DEL` নয়, `UNLINK` কেন:** `DEL` main thread-এ synchronously memory মুক্ত করে — লাখো element-এর key delete করলে Redis block হতে পারে। `UNLINK` key-টা সাথে সাথে সরিয়ে দেয় আর memory background thread-এ ফেরত নেয়।
            - **Fragmentation:** `used_memory` মাঝারি অথচ RSS অনেক বেশি (ratio ~1.5-এর বেশ ওপরে) হলে allocator মুক্ত memory ধরে রেখেছে; active defragmentation (`activedefrag`) সাহায্য করতে পারে।
            - **Fork-এর খরচ:** `BGSAVE`/AOF rewrite process fork করে; snapshot চলাকালীন বেশি write হলে copy-on-write-এ page duplicate হয়, তাই host-এ `maxmemory`-র বাইরেও RAM লাগে, নইলে kernel Redis-কে OOM-kill করতে পারে।
            - **Postmortem:** codebase-এ cache key-এর প্রতিটা `set` expiration দিচ্ছে কিনা তার একটা lint/check যোগ করো; এটা সস্তা বীমা।
        """,
        tip_en=r"""Split your answer into "stop the bleeding", "find the cause", "prevent recurrence". Interviewers for international roles especially look for that incident-response structure.""",
        tip_bn=r"""উত্তরটা "রক্তক্ষরণ থামাও", "কারণ খোঁজো", "পুনরাবৃত্তি ঠেকাও" — এই তিন ভাগে সাজাও। International role-এর interviewer-রা বিশেষ করে এই incident-response কাঠামোটা খোঁজে।""",
        mist_en=r"""Running `KEYS *` on the struggling instance to "look around", flipping a mixed cache+queue instance to `allkeys-lru` (silently evicting jobs), or restarting Redis and losing data.""",
        mist_bn=r"""চাপে থাকা instance-এ "খুঁজে দেখতে" `KEYS *` চালানো, cache+queue মেশানো instance-কে `allkeys-lru`-তে বদলে দেওয়া (চুপচাপ job evict হয়ে যায়), অথবা Redis restart করে data হারানো।""",
        code=r"""
            redis-cli INFO memory | grep -E "used_memory_human|maxmemory_human|mem_fragmentation_ratio"
            redis-cli CONFIG GET maxmemory-policy
            redis-cli INFO keyspace          # db0:keys=8123456,expires=1203,...  <- most keys have no TTL
            redis-cli --memkeys              # sample the biggest keys by memory
            redis-cli MEMORY USAGE feed:all:cache
            redis-cli UNLINK feed:all:cache  # free a huge key without blocking
            redis-cli CONFIG SET maxmemory-policy allkeys-lru   # only if the instance is a pure cache
        """,
        lang="bash",
        follow=[
            ("How would you find which application code path creates the keys without TTL?", "TTL ছাড়া key কোন application code path তৈরি করছে, কীভাবে খুঁজে বের করবে?"),
            ("Why does Redis need memory headroom beyond `maxmemory` during `BGSAVE`?", "`BGSAVE`-এর সময় Redis-এর `maxmemory`-র বাইরেও memory headroom কেন লাগে?"),
        ],
        related=["redis-017", "redis-007", "redis-032"],
        refs=[R_EVICTION, R_MEMUSAGE, R_INFO],
    ),
    # ------------------------------------------------------------------ redis-027
    Q(
        id="redis-027", sub="Persistence (RDB/AOF)", diff="hard", type="comparison",
        prio="medium", market="both", mins=10,
        tags=["persistence", "rdb", "aof", "appendfsync", "durability"],
        ver="Redis Open Source 8.10 (multi-part AOF since 7.0)", vs=True, status="stable",
        q_en=r"""Compare RDB snapshots and AOF persistence in Redis. Which configuration would you choose for (a) a pure cache, (b) a session store, and (c) a Redis Streams job queue — and why?""",
        q_bn=r"""Redis-এর RDB snapshot আর AOF persistence তুলনা করো। (a) pure cache, (b) session store, আর (c) Redis Streams job queue — প্রতিটার জন্য কোন configuration বেছে নেবে, এবং কেন?""",
        a_en=r"""
            **RDB** writes a compact point-in-time snapshot (`BGSAVE` forks a child that writes the file).
            - Pros: small file, fast restarts, perfect for backups and copying off-host.
            - Cons: you lose everything since the last snapshot (often minutes).

            **AOF** logs every write command and replays it on restart.
            - `appendfsync everysec` (default when AOF is on): fsync once per second in the background — at most about one second of writes lost.
            - `always`: fsync before replying — safest, much slower. `no`: let the OS decide — fastest, least safe.
            - Cons: bigger files, slower restarts; periodic rewrites (also via fork) compact it. Since Redis 7, AOF is multi-part (base + incremental files + manifest), and the base is RDB-formatted by default (`aof-use-rdb-preamble yes`), so restarts load faster.

            **My choices:**
            - **(a) Pure cache:** persistence off, or RDB only for a faster warm restart. Losing the cache is fine; the DB is the source of truth.
            - **(b) Session store:** AOF with `everysec` plus RDB for backups, and a replica. Losing a second of logins is acceptable; losing all sessions isn't.
            - **(c) Stream job queue:** AOF `everysec` (or `always` if a lost job is costly) plus RDB backups and replication; make consumers idempotent because a crash can still lose or replay the last moment.
        """,
        a_bn=r"""
            **RDB** একটা compact point-in-time snapshot লেখে (`BGSAVE` একটা child process fork করে, সে file লেখে)।
            - সুবিধা: ছোট file, দ্রুত restart, backup আর অন্য host-এ কপি করার জন্য দারুণ।
            - অসুবিধা: শেষ snapshot-এর পর থেকে সবকিছু হারাতে পারো (প্রায়ই কয়েক মিনিট)।

            **AOF** প্রতিটা write command log করে আর restart-এ replay করে।
            - `appendfsync everysec` (AOF চালু হলে default): background-এ প্রতি সেকেন্ডে একবার fsync — সর্বোচ্চ প্রায় এক সেকেন্ডের write হারায়।
            - `always`: reply দেওয়ার আগেই fsync — সবচেয়ে নিরাপদ, অনেক ধীর। `no`: OS-কে সিদ্ধান্ত নিতে দাও — সবচেয়ে দ্রুত, সবচেয়ে কম নিরাপদ।
            - অসুবিধা: বড় file, ধীর restart; নিয়মিত rewrite (এটাও fork দিয়ে) file ছোট করে। Redis 7 থেকে AOF multi-part (base + incremental file + manifest), আর default-এ base RDB format-এ থাকে (`aof-use-rdb-preamble yes`), তাই restart দ্রুত load হয়।

            **আমার পছন্দ:**
            - **(a) Pure cache:** persistence বন্ধ, অথবা দ্রুত warm restart-এর জন্য শুধু RDB। Cache হারালে সমস্যা নেই; DB-ই source of truth।
            - **(b) Session store:** `everysec` সহ AOF, backup-এর জন্য RDB, আর একটা replica। এক সেকেন্ডের login হারানো চলে; সব session হারানো চলে না।
            - **(c) Stream job queue:** AOF `everysec` (job হারানো ব্যয়বহুল হলে `always`) সাথে RDB backup আর replication; consumer-কে idempotent রাখো, কারণ crash হলে শেষ মুহূর্তের কিছু হারাতে বা replay হতে পারে।
        """,
        ex_en=r"""
            - **Defaults:** in the stock `redis.conf`, AOF is off (`appendonly no`); RDB snapshots run on the default save schedule unless disabled. Managed services have their own defaults — check them.
            - **Both enabled:** on restart Redis loads the AOF, since it's the most complete. The Redis docs suggest using both if you want durability comparable to a traditional database.
            - **Fork cost:** the fork copies page tables and then relies on copy-on-write; large instances with heavy writes need spare RAM and can see latency spikes when forking (disable transparent huge pages).
            - **Replication is not backup:** a replica faithfully copies a `FLUSHALL` too. Keep RDB files off-host (e.g. object storage) with retention.
            - **Durability ceiling:** even with AOF `always`, replication is asynchronous, so a failover can still lose acknowledged writes.
        """,
        ex_bn=r"""
            - **Default:** সাধারণ `redis.conf`-এ AOF বন্ধ (`appendonly no`); বন্ধ না করলে default save schedule অনুযায়ী RDB snapshot চলে। Managed service-এর নিজস্ব default থাকে — সেগুলো দেখে নাও।
            - **দুটোই চালু থাকলে:** restart-এ Redis AOF load করে, কারণ সেটাই সবচেয়ে সম্পূর্ণ। Traditional database-এর কাছাকাছি durability চাইলে Redis docs দুটোই ব্যবহার করতে বলে।
            - **Fork-এর খরচ:** fork page table কপি করে তারপর copy-on-write-এর ওপর নির্ভর করে; বেশি write-ওয়ালা বড় instance-এ বাড়তি RAM লাগে আর fork-এর সময় latency spike হতে পারে (transparent huge pages বন্ধ রাখো)।
            - **Replication মানে backup নয়:** replica একটা `FLUSHALL`-ও বিশ্বস্তভাবে কপি করে। RDB file retention সহ অন্য host-এ (যেমন object storage) রাখো।
            - **Durability-র সীমা:** AOF `always` থাকলেও replication asynchronous, তাই failover-এ acknowledged write-ও হারাতে পারে।
        """,
        tip_en=r"""Frame persistence as a "how much data can we lose?" (RPO) question and answer per use case. Interviewers like it when you tie a config flag to a business requirement.""",
        tip_bn=r"""Persistence-কে "কতটা data হারানো চলে?" (RPO) প্রশ্ন হিসেবে সাজাও আর প্রতিটা use case অনুযায়ী উত্তর দাও। Config flag-কে business requirement-এর সাথে যুক্ত করলে interviewer-রা পছন্দ করে।""",
        mist_en=r"""Saying AOF means "zero data loss", thinking replication replaces backups, or enabling `appendfsync always` everywhere without measuring the write-latency cost.""",
        mist_bn=r"""AOF মানেই "শূন্য data loss" বলা, replication-কে backup-এর বিকল্প ভাবা, অথবা write-latency-র খরচ না মেপেই সব জায়গায় `appendfsync always` চালু করা।""",
        code=r"""
            # (b) session store / (c) queue — redis.conf excerpt
            appendonly yes
            appendfsync everysec
            aof-use-rdb-preamble yes
            save 3600 1 300 100 60 10000     # RDB snapshots for backups

            # (a) pure cache
            appendonly no
            save ""                          # disable RDB snapshots
            maxmemory-policy allkeys-lru
        """,
        lang="text",
        follow=[
            ("What happens to latency when Redis forks for a snapshot on a 40 GB instance?", "40 GB instance-এ snapshot-এর জন্য Redis fork করলে latency-র কী হয়?"),
            ("How would you restore Redis from an RDB backup?", "RDB backup থেকে Redis কীভাবে restore করবে?"),
        ],
        related=["redis-006", "redis-028"],
        refs=[R_PERSIST, R_LATENCY],
    ),
    # ------------------------------------------------------------------ redis-031
    Q(
        id="redis-031", sub="Caching Architecture at Scale", diff="extreme", type="system-design",
        prio="medium", market="international", mins=25,
        tags=["system-design", "flash-sale", "hot-keys", "inventory", "lua", "streams"],
        ver="Redis Open Source 8.10; node-redis 6.3", vs=False, status="stable",
        q_en=r"""Design the Redis layer for an 11.11 flash sale on a Bangladeshi e-commerce site: 1,000 units of a phone at a discounted price go live at 8 PM, around 200,000 users are waiting, and the product page peaks at ~50,000 requests per second. You must not oversell, and PostgreSQL must survive.""",
        q_bn=r"""একটা বাংলাদেশি e-commerce site-এর 11.11 flash sale-এর জন্য Redis layer design করো: রাত 8টায় discount দামে একটা phone-এর 1,000 unit ছাড়া হবে, প্রায় 200,000 user অপেক্ষা করছে, আর product page-এ peak-এ প্রতি সেকেন্ডে ~50,000 request আসে। Oversell করা যাবে না, আর PostgreSQL-কে টিকে থাকতে হবে।""",
        a_en=r"""
            *(Advanced system-design question.)*

            **Read path (product page):**
            - Pre-warm the product data in Redis before 8 PM; refresh it in the background rather than letting it expire mid-sale.
            - The page is one **hot key**. Add a tiny in-process cache (1–2 s) in each Node instance and put static parts behind a CDN, so Redis sees thousands, not 50k, reads per second. Stock shown on the page can be approximate.

            **Write path (buying):**
            - **Admission control first:** per-user rate limiting and a waiting-room token so only a manageable number of buy attempts reach the reservation step.
            - **Atomic reservation in Redis with Lua:** one script checks "has this user already bought?", checks `stock >= qty`, decrements stock, records the buyer, adds a reservation with an expiry time to a sorted set, and appends an event to a Stream — all atomically. No oversell is possible inside Redis because the check and decrement can't interleave.
            - **Async order creation:** workers read the Stream with a consumer group and create orders in PostgreSQL at a controlled rate, idempotently (reservation id as a unique key).
            - **Payment timeout:** a sweeper reads expired reservations from the sorted set and returns stock with another Lua script.

            **Source of truth & safety:** PostgreSQL holds final orders, with a constraint that stock can't go negative as a last line of defence. A reconciliation job compares Redis counters with DB orders.

            **Failure modes:** Redis failover can lose the last moment of decrements (async replication) — use `WAIT` after reserving to reduce the window and rely on the DB constraint. If Redis is down, fail **closed** for buying ("try again") and serve the product page from CDN/DB with strict concurrency limits.
        """,
        a_bn=r"""
            *(Advanced system-design প্রশ্ন।)*

            **Read path (product page):**
            - রাত 8টার আগেই product data Redis-এ pre-warm করো; sale-এর মাঝখানে expire হতে না দিয়ে background-এ refresh করো।
            - Page-টা একটা **hot key**। প্রতিটা Node instance-এ খুব ছোট in-process cache (1–2 সেকেন্ড) দাও আর static অংশ CDN-এর পেছনে রাখো, যাতে Redis প্রতি সেকেন্ডে 50k নয়, কয়েক হাজার read দেখে। Page-এ দেখানো stock আনুমানিক হলেও চলে।

            **Write path (কেনা):**
            - **আগে admission control:** per-user rate limiting আর একটা waiting-room token, যাতে শুধু সামলানো যায় এমন সংখ্যক buy attempt reservation ধাপে পৌঁছায়।
            - **Lua দিয়ে Redis-এ atomic reservation:** একটা script-ই check করে "এই user আগে কিনেছে কি?", check করে `stock >= qty`, stock কমায়, buyer record করে, expiry time সহ reservation একটা sorted set-এ যোগ করে, আর একটা Stream-এ event append করে — সবকিছু atomically। Check আর decrement-এর মাঝে অন্য কিছু ঢুকতে পারে না বলে Redis-এর ভেতরে oversell অসম্ভব।
            - **Async order তৈরি:** worker-রা consumer group দিয়ে Stream পড়ে নিয়ন্ত্রিত হারে PostgreSQL-এ idempotently order তৈরি করে (reservation id unique key হিসেবে)।
            - **Payment timeout:** একটা sweeper sorted set থেকে expired reservation পড়ে আরেকটা Lua script দিয়ে stock ফেরত দেয়।

            **Source of truth ও নিরাপত্তা:** চূড়ান্ত order থাকে PostgreSQL-এ, শেষ প্রতিরক্ষা হিসেবে stock negative হতে না দেওয়ার constraint সহ। একটা reconciliation job Redis counter আর DB order মিলিয়ে দেখে।

            **Failure mode:** Redis failover-এ শেষ মুহূর্তের decrement হারাতে পারে (async replication) — reserve করার পর `WAIT` দিয়ে window কমাও আর DB constraint-এর ওপর ভরসা রাখো। Redis down হলে কেনার জন্য **fail closed** ("আবার চেষ্টা করুন"), আর product page কঠোর concurrency limit সহ CDN/DB থেকে serve করো।
        """,
        ex_en=r"""
            - **Why not decrement stock in PostgreSQL directly?** 200k users hitting one row means massive lock contention on a single hot row. Redis serialises the decrements in memory at very high throughput, and the DB receives only successful reservations.
            - **Cluster note:** all keys used by one script must share a hash slot — `stock:{sku42}`, `buyers:{sku42}`, `reservations:{sku42}`, `orders:pending:{sku42}`. That deliberately puts this SKU on one shard; if a single key becomes too hot, split stock into N buckets (`stock:{sku42:0}`…) and pick one at random.
            - **Don't rely on keyspace notifications** for reservation expiry — they're Pub/Sub-based and fire-and-forget. A sorted set scanned by a sweeper is reliable.
            - **Idempotency everywhere:** the client retries, the worker retries, the payment callback retries. Reservation id and payment idempotency keys make retries safe.
            - **Load test** the exact flow at 2× expected peak before the event, and rehearse a Redis failover.
        """,
        ex_bn=r"""
            - **সরাসরি PostgreSQL-এ stock কমানো নয় কেন?** 200k user একটা row-এ আঘাত করলে একটা hot row-এ বিশাল lock contention হয়। Redis memory-তে খুব high throughput-এ decrement-গুলো একটার পর একটা সাজায়, আর DB শুধু সফল reservation পায়।
            - **Cluster note:** একটা script-এর ব্যবহার করা সব key একই hash slot-এ থাকতে হবে — `stock:{sku42}`, `buyers:{sku42}`, `reservations:{sku42}`, `orders:pending:{sku42}`। এতে জেনেবুঝেই এই SKU একটা shard-এ থাকে; একটা key খুব বেশি hot হলে stock-কে N bucket-এ ভাগ করো (`stock:{sku42:0}`…) আর random একটা বেছে নাও।
            - **Reservation expiry-র জন্য keyspace notification-এর ওপর ভরসা কোরো না** — এগুলো Pub/Sub-ভিত্তিক, fire-and-forget। Sweeper দিয়ে scan করা sorted set নির্ভরযোগ্য।
            - **সব জায়গায় idempotency:** client retry করে, worker retry করে, payment callback retry করে। Reservation id আর payment idempotency key থাকলে retry নিরাপদ।
            - Event-এর আগে প্রত্যাশিত peak-এর 2× load-এ ঠিক এই flow-টা **load test** করো, আর একবার Redis failover-এর মহড়া দাও।
        """,
        tip_en=r"""Draw two paths — read and write — and spend most of the time on correctness of the write path (atomic Lua reservation + DB as source of truth). Close with failure modes; that's what separates senior answers.""",
        tip_bn=r"""দুইটা path আঁকো — read আর write — আর বেশিরভাগ সময় দাও write path-এর correctness-এ (atomic Lua reservation + DB-কে source of truth রাখা)। শেষ করো failure mode দিয়ে; senior উত্তরকে আলাদা করে এটাই।""",
        mist_en=r"""Doing `GET stock` then `DECR` from Node (race → oversell), letting the hot product key expire at peak, or treating Redis as the only record of who bought what.""",
        mist_bn=r"""Node থেকে `GET stock` তারপর `DECR` করা (race → oversell), peak-এর সময় hot product key expire হতে দেওয়া, অথবা কে কী কিনল তার একমাত্র record হিসেবে Redis-কে ধরা।""",
        code=r"""
            -- reserve.lua  (all keys share the {sku42} hash tag)
            -- KEYS: stock:{sku42}, buyers:{sku42}, reservations:{sku42}, orders:pending:{sku42}
            -- ARGV: userId, qty, reservationId, expiresAtMs
            local stockKey, buyersKey, resKey, streamKey = KEYS[1], KEYS[2], KEYS[3], KEYS[4]
            local userId, qty, resId, expiresAt = ARGV[1], tonumber(ARGV[2]), ARGV[3], ARGV[4]

            if redis.call('SISMEMBER', buyersKey, userId) == 1 then return -2 end  -- one per user
            local stock = tonumber(redis.call('GET', stockKey) or '0')
            if stock < qty then return -1 end                                      -- sold out

            redis.call('DECRBY', stockKey, qty)
            redis.call('SADD', buyersKey, userId)
            redis.call('ZADD', resKey, expiresAt, resId)                           -- for the timeout sweeper
            redis.call('XADD', streamKey, '*', 'reservationId', resId, 'userId', userId, 'qty', qty)
            return stock - qty                                                     -- remaining stock
        """,
        lang="text",
        follow=[
            ("How would you return stock for unpaid reservations without double-returning it?", "Payment না হওয়া reservation-এর stock দুইবার ফেরত না দিয়ে কীভাবে ফেরত দেবে?"),
            ("How do you handle a single hot key in Redis Cluster?", "Redis Cluster-এ একটা hot key কীভাবে সামলাবে?"),
            ("What does `WAIT` guarantee, and what doesn't it?", "`WAIT` কী guarantee দেয়, আর কী দেয় না?"),
        ],
        related=["redis-023", "redis-024", "redis-028"],
        refs=[R_LUA, R_CLUSTER, R_STREAMS],
    ),
]

if __name__ == "__main__":
    save("redis", "b3", QUESTIONS)
