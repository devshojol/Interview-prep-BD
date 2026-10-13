# MongoDB — batch 3 (mongo-008, 009, 010, 011, 016, 017, 026, 032)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

INDEXES = ("MongoDB Manual — Indexes", "https://www.mongodb.com/docs/manual/indexes/")
MULTIKEY = ("MongoDB Manual — Multikey Indexes", "https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/")
DATA_MODEL = ("MongoDB Manual — Data Modeling", "https://www.mongodb.com/docs/manual/data-modeling/")
EMBED_1N = ("MongoDB Manual — Model One-to-Many Relationships with Embedded Documents", "https://www.mongodb.com/docs/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/")
REPLICATION = ("MongoDB Manual — Replication", "https://www.mongodb.com/docs/manual/replication/")
ELECTIONS = ("MongoDB Manual — Replica Set Elections", "https://www.mongodb.com/docs/manual/core/replica-set-elections/")
TTL = ("MongoDB Manual — TTL Indexes", "https://www.mongodb.com/docs/manual/core/index-ttl/")
UNIQUE = ("MongoDB Manual — Unique Indexes", "https://www.mongodb.com/docs/manual/core/index-unique/")
PARTIAL = ("MongoDB Manual — Partial Indexes", "https://www.mongodb.com/docs/manual/core/index-partial/")
ATOMICITY = ("MongoDB Manual — Atomicity and Transactions", "https://www.mongodb.com/docs/manual/core/write-operations-atomicity/")
PATTERNS = ("MongoDB Manual — Schema Design Patterns", "https://www.mongodb.com/docs/manual/data-modeling/design-patterns/")
WINDOW = ("MongoDB Manual — $setWindowFields (aggregation)", "https://www.mongodb.com/docs/manual/reference/operator/aggregation/setWindowFields/")
BACKUPS = ("MongoDB Manual — Backup Methods for a Self-Managed Deployment", "https://www.mongodb.com/docs/manual/core/backups/")
MONGODUMP = ("MongoDB Database Tools — mongodump", "https://www.mongodb.com/docs/manual/reference/program/mongodump/")
SEC_CHECKLIST = ("MongoDB Manual — Security Checklist", "https://www.mongodb.com/docs/manual/administration/security-checklist/")

QUESTIONS = [
    # ------------------------------------------------------------------ mongo-008
    Q(
        id="mongo-008", sub="Indexes", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["indexes", "ixscan", "collscan", "write-cost", "index-types"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""What is an index in MongoDB, why do we need it, and what does it cost?""",
        q_bn=r"""MongoDB-তে index কী, এটা কেন দরকার, আর এর খরচ কী?""",
        a_en=r"""
            An index is a separate, sorted data structure (a B-tree) that stores the values of one or more fields with pointers to the documents. Without a suitable index MongoDB does a **collection scan** (`COLLSCAN`) — it reads every document. With one, it does an **index scan** (`IXSCAN`) and jumps straight to the matching range, which also lets it return results already sorted.

            Every collection has a unique index on `_id` automatically. The cost: each index uses disk and, ideally, RAM; and **every insert, update and delete must also update every index**, so too many indexes slow writes. I index for the queries the app actually runs, not for every field.
        """,
        a_bn=r"""
            Index হলো একটা আলাদা, sorted data structure (B-tree), যেখানে এক বা একাধিক field-এর value আর document-এর pointer রাখা থাকে। উপযুক্ত index না থাকলে MongoDB **collection scan** (`COLLSCAN`) করে — প্রতিটি document পড়ে। Index থাকলে **index scan** (`IXSCAN`) করে সরাসরি matching range-এ চলে যায়, আর result আগে থেকেই sorted অবস্থায় দিতে পারে।

            প্রতিটি collection-এ `_id`-এর ওপর একটা unique index automatically থাকে। খরচ: প্রতিটি index disk আর আদর্শভাবে RAM ব্যবহার করে; আর **প্রতিটি insert, update ও delete-এ সব index-ও update করতে হয়** — তাই বেশি index write slow করে। আমি app যেসব query আসলে চালায় সেগুলোর জন্য index বানাই, প্রতিটি field-এর জন্য না।
        """,
        ex_en=r"""
            **Common index types and properties:**
            - **Single field** and **compound** (order of fields matters — see the ESR guideline).
            - **Multikey:** created automatically when an indexed field holds an array; one index entry per element.
            - **Text**, **2dsphere** (geo), **hashed** (used for hashed sharding), **wildcard** (for unpredictable field names).
            - Properties: **unique**, **partial** (only documents matching a filter), **sparse**, **TTL** (auto-delete after a time).

            **Practical tips:** check plans with `explain("executionStats")`; find unused indexes with `$indexStats`; build indexes on large production collections during low traffic (index builds take locks only briefly at the start and end, but they consume I/O and CPU).
        """,
        ex_bn=r"""
            **Common index type আর property:**
            - **Single field** আর **compound** (field-এর order গুরুত্বপূর্ণ — ESR guideline দেখো)।
            - **Multikey:** indexed field-এ array থাকলে automatically তৈরি হয়; array-র প্রতিটি element-এর জন্য একটা index entry।
            - **Text**, **2dsphere** (geo), **hashed** (hashed sharding-এ ব্যবহার হয়), **wildcard** (অনিশ্চিত field name-এর জন্য)।
            - Property: **unique**, **partial** (শুধু filter-এর সাথে মেলা document), **sparse**, **TTL** (নির্দিষ্ট সময় পরে auto-delete)।

            **Practical tips:** `explain("executionStats")` দিয়ে plan দেখো; `$indexStats` দিয়ে অব্যবহৃত index খোঁজো; বড় production collection-এ কম traffic-এর সময় index build করো (build-এর শুরু আর শেষে সামান্য সময়ের জন্য lock নেয়, কিন্তু I/O আর CPU খরচ হয়)।
        """,
        tip_en=r"""Always pair "indexes speed up reads" with "and slow down writes" — mentioning the trade-off is what separates a thoughtful answer from a textbook one.""",
        tip_bn=r""""Index read দ্রুত করে" বলার সাথে সবসময় বলো "আর write slow করে" — trade-off উল্লেখ করাই একটা চিন্তাশীল উত্তরকে textbook উত্তর থেকে আলাদা করে।""",
        mist_en=r"""Indexing every field "just in case"; assuming MongoDB will efficiently combine many single-field indexes instead of using one well-designed compound index.""",
        mist_bn=r""""যদি লাগে" ভেবে প্রতিটি field-এ index দেওয়া; ধরে নেওয়া যে MongoDB একটা ভালোভাবে design করা compound index-এর বদলে অনেকগুলো single-field index দক্ষভাবে মিলিয়ে নেবে।""",
        code=r"""
            // Create an index for "orders of a customer, newest first"
            db.orders.createIndex({ customerId: 1, createdAt: -1 })

            // List indexes on the collection
            db.orders.getIndexes()

            // Check that the query uses it (look for IXSCAN, not COLLSCAN)
            db.orders.find({ customerId: 42 }).sort({ createdAt: -1 }).explain("executionStats")
        """,
        lang="javascript",
        follow=[
            ("How do you find indexes that are never used?", "যে index কখনো ব্যবহার হয় না সেগুলো কীভাবে খুঁজবে?"),
            ("What is a multikey index and what limitation does it have?", "Multikey index কী, আর এর কী সীমাবদ্ধতা আছে?"),
        ],
        related=["mongo-015", "mongo-023"],
        refs=[INDEXES, MULTIKEY],
    ),
    # ------------------------------------------------------------------ mongo-009
    Q(
        id="mongo-009", sub="Embedding vs Referencing", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["schema-design", "embedding", "referencing", "relationships"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""When would you embed related data inside a MongoDB document, and when would you reference it from another collection?""",
        q_bn=r"""কখন related data একটা MongoDB document-এর ভেতরে embed করবে, আর কখন অন্য collection থেকে reference করবে?""",
        a_en=r"""
            The rule of thumb is: **data that is read together should be stored together.**

            I **embed** when the child data belongs to the parent, is usually read with it, and stays **bounded** — a user's few addresses, the line items of an order. One read gets everything, and updates to the whole thing are atomic.

            I **reference** (store an `_id` and look it up) when the related data is **large or unbounded** (comments on a viral post, chat messages), **shared** by many parents and updated independently (an author's profile, a product's catalog data), or usually accessed on its own.

            For relationship size: one-to-few → embed; one-to-many → array of references or child-to-parent reference; one-to-"squillions" → always store the parent's ID in the child.
        """,
        a_bn=r"""
            মূল নিয়ম হলো: **যে data একসাথে read হয়, সেটা একসাথে store করো।**

            আমি **embed** করি যখন child data parent-এরই অংশ, সাধারণত parent-এর সাথে read হয়, আর **bounded** থাকে — যেমন একজন user-এর কয়েকটা address, একটা order-এর line item। এক read-এই সব পাওয়া যায়, আর পুরোটার update atomic হয়।

            আমি **reference** করি (একটা `_id` রেখে পরে lookup) যখন related data **বড় বা unbounded** (viral post-এর comment, chat message), অনেক parent-এর মধ্যে **shared** আর আলাদাভাবে update হয় (author-এর profile, product-এর catalog data), অথবা সাধারণত আলাদাভাবে access হয়।

            Relationship-এর আকার অনুযায়ী: one-to-few → embed; one-to-many → reference-এর array বা child থেকে parent-এর reference; one-to-"squillions" → সবসময় child-এ parent-এর ID রাখো।
        """,
        ex_en=r"""
            - **Why bounded matters:** documents are capped at 16 MB, and a growing array makes every update rewrite a larger document and bloats indexes on that array.
            - **Duplication is sometimes correct:** an order should embed a *snapshot* of the product name and price at purchase time, even though products also live in their own collection — that's historical truth, not a normalisation bug.
            - **Hybrid (extended reference):** store the reference plus the few fields you display often, e.g. `author: { _id, name, avatarUrl }` on a post. You accept slightly stale copies (or update them in the background) to avoid a `$lookup` on every read.
            - **Joins exist** (`$lookup`), but if every request needs one, the schema probably isn't matching the access pattern.
        """,
        ex_bn=r"""
            - **Bounded কেন জরুরি:** document-এর সর্বোচ্চ size 16 MB, আর বাড়তে থাকা array থাকলে প্রতিটি update-এ আরও বড় document rewrite হয় এবং সেই array-র index ফুলে যায়।
            - **কখনো কখনো duplication-ই সঠিক:** order-এ কেনার সময়ের product name আর price-এর একটা *snapshot* embed করা উচিত, যদিও product-এর আলাদা collection আছে — এটা ঐতিহাসিক সত্য, normalisation-এর bug না।
            - **Hybrid (extended reference):** reference-এর সাথে বারবার দেখানো কয়েকটা field রাখো, যেমন post-এ `author: { _id, name, avatarUrl }`। প্রতিটি read-এ `$lookup` এড়াতে একটু পুরনো copy মেনে নাও (বা background-এ update করো)।
            - **Join আছে** (`$lookup`), কিন্তু প্রতিটি request-এ যদি join লাগে, তাহলে সম্ভবত schema access pattern-এর সাথে মিলছে না।
        """,
        tip_en=r"""Answer with two concrete examples (order items → embed, blog comments → reference) and the word "bounded". Concrete examples are more convincing than abstract rules.""",
        tip_bn=r"""দুইটা concrete উদাহরণ দিয়ে উত্তর দাও (order item → embed, blog comment → reference) আর "bounded" শব্দটা ব্যবহার করো। Abstract নিয়মের চেয়ে concrete উদাহরণ বেশি বিশ্বাসযোগ্য।""",
        mist_en=r"""Normalising everything like in SQL and then joining on every request, or embedding everything (e.g. all of a user's orders inside the user document) until it hits the 16 MB limit.""",
        mist_bn=r"""SQL-এর মতো সব কিছু normalise করে প্রতিটি request-এ join করা, অথবা সব কিছু embed করা (যেমন একজন user-এর সব order user document-এর ভেতরে) যতক্ষণ না 16 MB limit-এ পৌঁছায়।""",
        code=r"""
            // Embedded: bounded, always read with the order
            {
              _id: ObjectId("6709b0c1d2e3f40516273849"),
              customerId: ObjectId("65aa0b1c2d3e4f5061728394"),   // reference
              items: [
                { productId: ObjectId("66c1..."), name: "Earbuds", unitPrice: 3500, qty: 1 }
              ],
              shippingAddress: { city: "Dhaka", area: "Dhanmondi" }
            }

            // Referenced: unbounded, each comment points to its post
            { _id: ObjectId("..."), postId: ObjectId("..."), userId: ObjectId("..."), text: "Nice!" }
        """,
        lang="javascript",
        follow=[
            ("How would you store comments for a post that might get 200,000 comments?", "যে post-এ 200,000 comment হতে পারে, তার comment কীভাবে store করবে?"),
            ("What problems do you get if you duplicate the author's name on every post?", "প্রতিটি post-এ author-এর নাম duplicate করলে কী সমস্যা হয়?"),
        ],
        related=["mongo-001", "mongo-013"],
        refs=[DATA_MODEL, EMBED_1N],
    ),
    # ------------------------------------------------------------------ mongo-010
    Q(
        id="mongo-010", sub="Replication & Consistency", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["replica-set", "replication", "failover", "elections", "oplog"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""What is a replica set in MongoDB, and how does automatic failover work?""",
        q_bn=r"""MongoDB-তে replica set কী, আর automatic failover কীভাবে কাজ করে?""",
        a_en=r"""
            A replica set is a group of `mongod` servers that keep copies of the same data. One member is the **primary** and accepts all writes; it records every change in its **oplog**. The **secondaries** continuously copy and apply the oplog, so they stay (asynchronously) in sync and can also serve reads if the read preference allows it.

            Members send heartbeats to each other. If the primary is unreachable for longer than the election timeout (10 seconds by default), an eligible secondary calls an **election**; the member that wins votes from a majority — usually the most up-to-date one — becomes the new primary. Drivers discover the new primary automatically and retry writes. A typical production setup is three data-bearing members in different availability zones.
        """,
        a_bn=r"""
            Replica set হলো কয়েকটা `mongod` server-এর group, যারা একই data-র copy রাখে। একজন member হয় **primary**, সব write সে-ই নেয়; প্রতিটি পরিবর্তন সে নিজের **oplog**-এ লিখে রাখে। **Secondary**-রা ক্রমাগত সেই oplog copy করে apply করে, ফলে তারা (asynchronously) sync-এ থাকে, আর read preference অনুমতি দিলে read-ও serve করতে পারে।

            Member-রা একে অপরকে heartbeat পাঠায়। Election timeout-এর (default 10 second) বেশি সময় primary-কে পাওয়া না গেলে একটা eligible secondary **election** শুরু করে; যে member majority-র vote পায় — সাধারণত সবচেয়ে up-to-date member — সে নতুন primary হয়। Driver-রা automatically নতুন primary খুঁজে নেয় আর write retry করে। সাধারণ production setup হলো ভিন্ন availability zone-এ তিনটা data-bearing member।
        """,
        ex_en=r"""
            - **Why an odd number / majority:** a primary needs a majority of voting members to be elected and to stay primary. This prevents two primaries during a network split (split brain). A set can have up to 50 members, but at most 7 voting members.
            - **Replication is not a backup:** an accidental `deleteMany` replicates to every secondary within milliseconds. You still need backups.
            - **Writes during failover:** for a few seconds there is no primary; retryable writes and sensible timeouts in the driver hide most of it from users.
            - **Durability:** whether an acknowledged write survives a failover depends on the write concern — `w: "majority"` (the default since MongoDB 5.0) is the safe choice.
            - **Reads from secondaries** can be stale because replication is asynchronous.
        """,
        ex_bn=r"""
            - **কেন বিজোড় সংখ্যা / majority:** primary হতে আর primary থাকতে voting member-দের majority লাগে। এতে network split-এর সময় দুইটা primary (split brain) হওয়া আটকায়। একটা set-এ সর্বোচ্চ 50টা member থাকতে পারে, কিন্তু voting member সর্বোচ্চ 7টা।
            - **Replication backup না:** ভুল করে চালানো `deleteMany` কয়েক millisecond-এর মধ্যে সব secondary-তে replicate হয়ে যায়। Backup তবুও লাগবে।
            - **Failover-এর সময় write:** কয়েক second কোনো primary থাকে না; driver-এর retryable write আর যুক্তিসঙ্গত timeout এর বেশিরভাগটাই user-এর কাছ থেকে আড়াল করে।
            - **Durability:** acknowledged write failover-এর পর টিকবে কি না তা write concern-এর ওপর নির্ভর করে — `w: "majority"` (MongoDB 5.0 থেকে default) নিরাপদ পছন্দ।
            - **Secondary থেকে read** stale হতে পারে, কারণ replication asynchronous।
        """,
        tip_en=r"""Add "replication is not a backup" — it's a short line that shows operational maturity and often leads into a good follow-up discussion.""",
        tip_bn=r""""Replication backup না" কথাটা যোগ করো — ছোট্ট একটা লাইন, কিন্তু operational maturity দেখায় এবং প্রায়ই ভালো follow-up আলোচনার দিকে নিয়ে যায়।""",
        mist_en=r"""Thinking secondaries are always perfectly in sync, or that a replica set protects you from accidental deletes.""",
        mist_bn=r"""ভাবা যে secondary সবসময় পুরোপুরি sync-এ থাকে, অথবা replica set ভুল করে delete হওয়া থেকে রক্ষা করে।""",
        code=r"""
            // Connection string lists several members; the driver finds the primary
            // mongodb://db1.example.internal,db2.example.internal,db3.example.internal/shop?replicaSet=rs0

            rs.status()          // member states: PRIMARY, SECONDARY, health, optime
            rs.printSecondaryReplicationInfo()  // how far behind each secondary is
        """,
        lang="javascript",
        follow=[
            ("What is an arbiter, and why is it often discouraged in production?", "Arbiter কী, আর production-এ এটা কেন প্রায়ই নিরুৎসাহিত করা হয়?"),
            ("What happens to writes that the old primary accepted but never replicated?", "পুরনো primary যে write নিয়েছিল কিন্তু replicate করেনি, সেগুলোর কী হয়?"),
        ],
        related=["mongo-031"],
        refs=[REPLICATION, ELECTIONS],
    ),
    # ------------------------------------------------------------------ mongo-011
    Q(
        id="mongo-011", sub="TTL Indexes", diff="easy", type="scenario",
        prio="medium", market="bangladesh", mins=3,
        tags=["ttl", "indexes", "otp", "expiry"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""You need to store OTP codes for phone-number login, and each OTP should disappear automatically 5 minutes after it's created. How would you do this in MongoDB, and what caveats should you keep in mind?""",
        q_bn=r"""Phone number দিয়ে login-এর জন্য OTP code store করতে হবে, আর প্রতিটি OTP তৈরির 5 minute পরে নিজে থেকেই মুছে যাওয়া উচিত। MongoDB-তে এটা কীভাবে করবে, আর কী কী সতর্কতা মাথায় রাখবে?""",
        a_en=r"""
            I'd use a **TTL index**: a single-field index on a `Date` field with `expireAfterSeconds`. A background task on the server deletes documents once `createdAt + 300 seconds` has passed.

            The key caveat: the TTL monitor runs **every 60 seconds**, and deletion can lag further under load. So an OTP may still exist a minute or more after it "expired". The verification query must therefore check the time itself (e.g. `createdAt` within the last 5 minutes); TTL is clean-up, not the security check.

            Also: the field must be a real BSON `Date` (strings never expire), and I'd hash the OTP, limit attempts, and delete it after successful use.
        """,
        a_bn=r"""
            আমি একটা **TTL index** ব্যবহার করব: একটা `Date` field-এ `expireAfterSeconds` সহ single-field index। `createdAt + 300 second` পার হয়ে গেলে server-এর একটা background task document মুছে দেয়।

            মূল সতর্কতা: TTL monitor **প্রতি 60 second-এ** একবার চলে, আর load বেশি থাকলে delete আরও দেরিতে হতে পারে। তাই "expire" হওয়ার এক মিনিট বা তারও বেশি পরে OTP থেকে যেতে পারে। এজন্য verification query-তে নিজেই সময় check করতে হবে (যেমন `createdAt` গত 5 minute-এর মধ্যে কি না); TTL হলো clean-up, security check না।

            আরও: field-টা আসল BSON `Date` হতে হবে (string কখনো expire হয় না), আর আমি OTP hash করে রাখব, attempt সীমিত করব, এবং সফলভাবে ব্যবহারের পর delete করব।
        """,
        ex_en=r"""
            - **Per-document expiry:** store `expiresAt` and create the index with `expireAfterSeconds: 0` — each document then expires at its own clock time (useful when different OTP types live for different durations).
            - **Restrictions:** TTL works only on single-field indexes (compound indexes ignore the option), not on `_id`, and documents without the field (or with a non-date value) never expire. With an array of dates, the earliest one is used.
            - **Load:** TTL deletes are normal deletes — a huge batch expiring at once (e.g. millions of sessions) creates write load and replication traffic.
            - **Alternative:** if you already run Redis, `SET otp:<phone> <hash> EX 300` gives exact expiry; MongoDB TTL is great when the data should live with your other app data.
        """,
        ex_bn=r"""
            - **প্রতি document-এ আলাদা expiry:** `expiresAt` store করে `expireAfterSeconds: 0` দিয়ে index বানাও — তখন প্রতিটি document নিজের নির্দিষ্ট সময়ে expire হয় (বিভিন্ন ধরনের OTP ভিন্ন সময় বাঁচলে কাজে লাগে)।
            - **সীমাবদ্ধতা:** TTL শুধু single-field index-এ কাজ করে (compound index এই option ignore করে), `_id`-এ না; আর যেসব document-এ field নেই (বা value date না), সেগুলো কখনো expire হয় না। Date-এর array থাকলে সবচেয়ে আগের date-টা ধরা হয়।
            - **Load:** TTL delete সাধারণ delete-ই — একসাথে বিশাল batch expire হলে (যেমন লক্ষ লক্ষ session) write load আর replication traffic তৈরি হয়।
            - **বিকল্প:** আগে থেকে Redis চালালে `SET otp:<phone> <hash> EX 300` দিয়ে exact expiry পাওয়া যায়; data যদি বাকি app data-র সাথেই থাকা উচিত হয়, তাহলে MongoDB TTL চমৎকার।
        """,
        tip_en=r"""The "60-second monitor, so verify expiry in the query" point is what interviewers are fishing for — say it explicitly.""",
        tip_bn=r""""Monitor 60 second পরপর চলে, তাই query-তেই expiry verify করো" — interviewer আসলে এই কথাটাই শুনতে চায়, তাই স্পষ্ট করে বলো।""",
        mist_en=r"""Relying on TTL for exact-time security decisions; storing `createdAt` as an ISO string; trying to add TTL to a compound index.""",
        mist_bn=r"""Exact সময়ের security সিদ্ধান্তের জন্য TTL-এর ওপর নির্ভর করা; `createdAt` ISO string হিসেবে রাখা; compound index-এ TTL যোগ করার চেষ্টা করা।""",
        code=r"""
            // Expire 300 seconds after createdAt
            db.otps.createIndex({ createdAt: 1 }, { expireAfterSeconds: 300 })

            db.otps.insertOne({ phone: "+8801711000000", codeHash: hash, attempts: 0, createdAt: new Date() })

            // Verification still checks the age itself (TTL deletion is not instant)
            db.otps.findOneAndDelete({
              phone: "+8801711000000",
              codeHash: hash,
              createdAt: { $gt: new Date(Date.now() - 5 * 60 * 1000) }
            })
        """,
        lang="javascript",
        follow=[
            ("How would you stop someone from brute-forcing a 6-digit OTP?", "কেউ যেন 6-digit OTP brute-force করতে না পারে, সেটা কীভাবে আটকাবে?"),
        ],
        related=["mongo-008"],
        refs=[TTL],
    ),
    # ------------------------------------------------------------------ mongo-016
    Q(
        id="mongo-016", sub="Unique & Partial Indexes", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["unique-index", "partial-index", "null", "e11000"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""Users can sign up with a phone number only, so many documents have no `username` field. You created `db.users.createIndex({ username: 1 }, { unique: true })` when there was just one phone-only user. What happens when a second phone-only user signs up, and what is the best fix?""",
        q_bn=r"""User-রা শুধু phone number দিয়েও sign up করতে পারে, তাই অনেক document-এ `username` field নেই। যখন মাত্র একজন phone-only user ছিল, তখন `db.users.createIndex({ username: 1 }, { unique: true })` বানানো হয়েছে। দ্বিতীয় phone-only user sign up করলে কী হবে, আর সবচেয়ে ভালো fix কী?""",
        options=[
            (r"""The insert fails with E11000, because a missing field is indexed as `null`; fix it with a partial unique index using `partialFilterExpression: { username: { $type: "string" } }`""",
             r"""Insert E11000 দিয়ে fail করে, কারণ missing field `null` হিসেবে index হয়; fix হলো `partialFilterExpression: { username: { $type: "string" } }` দিয়ে partial unique index"""),
            (r"""The insert succeeds — unique indexes ignore documents that don't have the field""",
             r"""Insert সফল হয় — unique index সেই document-গুলো ignore করে যেগুলোতে field নেই"""),
            (r"""The insert fails, and the only fix is to generate a random placeholder username for every user""",
             r"""Insert fail করে, আর একমাত্র fix হলো প্রতিটি user-এর জন্য random placeholder username তৈরি করা"""),
            (r"""The insert succeeds, but MongoDB silently drops the unique index once two null values exist""",
             r"""Insert সফল হয়, কিন্তু দুইটা null value হলে MongoDB চুপচাপ unique index drop করে দেয়"""),
        ],
        correct=0,
        a_en=r"""A unique index stores `null` for documents that lack the field, so only **one** document may be missing it. The second phone-only signup fails with an E11000 duplicate key error. A **partial** unique index that only includes documents where `username` is a string enforces uniqueness for real usernames and ignores the rest.""",
        a_bn=r"""Unique index-এ field না থাকা document-এর জন্য `null` store হয়, তাই শুধু **একটা** document-এ field missing থাকতে পারে। দ্বিতীয় phone-only signup E11000 duplicate key error দিয়ে fail করে। একটা **partial** unique index, যেটা শুধু `username` string থাকা document-গুলো নেয়, আসল username-এর uniqueness enforce করে আর বাকিগুলো ignore করে।""",
        ex_en=r"""
            Option B is the tempting one, especially for people coming from PostgreSQL, where multiple NULLs are allowed in a unique column by default. MongoDB behaves differently.

            - **Why `$type: "string"` rather than `$exists: true`:** `$exists: true` would still include documents with an explicit `username: null`, which would collide again.
            - **`sparse: true`** on the unique index also skips documents without the field, but partial indexes are more flexible and are the recommended approach.
            - **Query caveat:** the planner only uses a partial index when it can prove the query's filter falls inside the partial filter. Check username lookups with `explain()`; if the index isn't chosen, repeat the condition in the query (`{ username: "rafi", $and: [{ username: { $type: "string" } }] }`) or use `hint`.
            - **Case-insensitive uniqueness:** add a collation with `strength: 2`, or store a normalised lowercase copy.
        """,
        ex_bn=r"""
            Option B সবচেয়ে বিভ্রান্তিকর, বিশেষ করে PostgreSQL থেকে আসা developer-দের জন্য — সেখানে default-ভাবে unique column-এ একাধিক NULL চলে। MongoDB-র আচরণ আলাদা।

            - **`$exists: true`-এর বদলে `$type: "string"` কেন:** `$exists: true` দিলে explicit `username: null` থাকা document-ও ঢুকে যাবে, আবার collision হবে।
            - Unique index-এ **`sparse: true`** দিলেও field না থাকা document skip হয়, কিন্তু partial index বেশি flexible আর এটাই recommended উপায়।
            - **Query-র সতর্কতা:** planner তখনই partial index ব্যবহার করে, যখন সে প্রমাণ করতে পারে যে query-র filter partial filter-এর ভেতরে পড়ে। Username lookup `explain()` দিয়ে check করো; index বাছাই না হলে query-তে condition-টা আবার দাও (`{ username: "rafi", $and: [{ username: { $type: "string" } }] }`) অথবা `hint` ব্যবহার করো।
            - **Case-insensitive uniqueness:** `strength: 2` সহ collation দাও, অথবা একটা normalised lowercase copy রাখো।
        """,
        tip_en=r"""Contrast with PostgreSQL's NULL handling in one sentence — it shows cross-database awareness, which matters in MERN + SQL shops.""",
        tip_bn=r"""এক বাক্যে PostgreSQL-এর NULL handling-এর সাথে তুলনা করো — এতে cross-database ধারণা বোঝা যায়, যেটা MERN + SQL দুটোই ব্যবহার করা company-তে গুরুত্বপূর্ণ।""",
        code=r"""
            db.users.createIndex(
              { username: 1 },
              { unique: true, partialFilterExpression: { username: { $type: "string" } } }
            )
        """,
        lang="javascript",
        follow=[
            ("How would you make emails unique regardless of letter case?", "Letter case যাই হোক, email unique কীভাবে রাখবে?"),
        ],
        related=["mongo-007", "mongo-008"],
        refs=[UNIQUE, PARTIAL],
    ),
    # ------------------------------------------------------------------ mongo-017
    Q(
        id="mongo-017", sub="Real-World Data Modeling", diff="medium", type="scenario",
        prio="high", market="bangladesh", mins=8,
        tags=["schema-design", "e-commerce", "orders", "denormalization", "snapshot"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""You're designing the order system for a local e-commerce site. Product prices change often (flash sales, discounts), and an order must always show exactly what the customer paid. How would you model products, orders and order items in MongoDB?""",
        q_bn=r"""তুমি একটা local e-commerce site-এর order system design করছ। Product-এর দাম প্রায়ই বদলায় (flash sale, discount), আর order-এ সবসময় ঠিক সেটাই দেখাতে হবে যা customer আসলে pay করেছে। MongoDB-তে product, order আর order item কীভাবে model করবে?""",
        a_en=r"""
            **Clarify:** expected volume, whether orders are edited after placement, and which screens read them (customer "My orders", admin/ops, reports).

            **Model:**
            - `products` — catalog data: name, current price, stock, a bounded set of variants, category IDs.
            - `orders` — one document per order with the **line items embedded** as an array. Each item keeps the `productId` reference **plus a snapshot**: name, SKU/variant, unit price, quantity, discount at purchase time. Also embed the shipping address snapshot, payment summary, status and a short status history, and store computed totals (subtotal, delivery charge, discount, grand total).
            - `customerId` as a reference (plus name/phone snapshot if the ops team needs it on every screen).

            **Why:** an order is a historical record — copying prices into it isn't harmful duplication, it's the truth at that moment. Items are bounded (a handful per order), so one read renders the whole order and status updates are atomic.

            **Indexes:** `{ customerId: 1, createdAt: -1 }` for "My orders", `{ status: 1, createdAt: -1 }` for ops, unique `orderNumber`.

            **Stock:** decrement with a conditional atomic update (`stock: { $gte: qty }` + `$inc`); for multi-item checkout use a transaction or a reservation step.
        """,
        a_bn=r"""
            **আগে প্রশ্ন পরিষ্কার করো:** আনুমানিক volume কত, order দেওয়ার পর edit হয় কি না, আর কোন screen-গুলো order পড়ে (customer-এর "My orders", admin/ops, report)।

            **Model:**
            - `products` — catalog data: name, বর্তমান price, stock, সীমিত সংখ্যক variant, category ID।
            - `orders` — প্রতিটি order-এর জন্য একটা document, যেখানে **line item array হিসেবে embedded**। প্রতিটি item-এ `productId` reference **আর একটা snapshot** থাকে: কেনার সময়ের name, SKU/variant, unit price, quantity, discount। Shipping address-এর snapshot, payment summary, status আর ছোট একটা status history-ও embed করো, আর computed total (subtotal, delivery charge, discount, grand total) store করো।
            - `customerId` reference হিসেবে (ops team-এর প্রতিটি screen-এ লাগলে name/phone snapshot-ও)।

            **কেন:** order হলো একটা ঐতিহাসিক record — এতে দাম copy করা ক্ষতিকর duplication না, বরং সেই মুহূর্তের সত্য। Item সীমিত (প্রতি order-এ কয়েকটা), তাই এক read-এই পুরো order দেখানো যায়, আর status update atomic হয়।

            **Index:** "My orders"-এর জন্য `{ customerId: 1, createdAt: -1 }`, ops-এর জন্য `{ status: 1, createdAt: -1 }`, আর unique `orderNumber`।

            **Stock:** conditional atomic update দিয়ে কমাও (`stock: { $gte: qty }` + `$inc`); একাধিক item-এর checkout-এ transaction বা reservation step ব্যবহার করো।
        """,
        ex_en=r"""
            - **Don't embed orders in the customer document** — a loyal customer's order list is unbounded.
            - **Don't reference the live product price** from the order — after the next price change, old invoices would show the wrong amount (a legal/accounting problem, not just a UI bug).
            - **Status history** is bounded in practice (pending → confirmed → shipped → delivered/returned); if you need a full audit log, use a separate `orderEvents` collection.
            - **Money:** use `Decimal128` or integer poisha; never floats.
            - **Reporting:** sales dashboards read from pre-aggregated daily summaries or a secondary/analytics node, not by scanning raw orders on every request.
            - **Cancellation/refund:** keep the original amounts and add refund records rather than editing the paid totals.
        """,
        ex_bn=r"""
            - **Customer document-এ order embed কোরো না** — একজন নিয়মিত customer-এর order list unbounded।
            - **Order থেকে product-এর live price reference কোরো না** — পরের বার দাম বদলালে পুরনো invoice-এ ভুল amount দেখাবে (শুধু UI bug না, legal/accounting সমস্যা)।
            - **Status history** বাস্তবে bounded (pending → confirmed → shipped → delivered/returned); পূর্ণ audit log লাগলে আলাদা `orderEvents` collection ব্যবহার করো।
            - **টাকা:** `Decimal128` বা integer পয়সা ব্যবহার করো; কখনো float না।
            - **Reporting:** sales dashboard pre-aggregated daily summary বা secondary/analytics node থেকে পড়বে, প্রতিটি request-এ raw order scan করে না।
            - **Cancellation/refund:** আসল amount রেখে দিয়ে refund record যোগ করো, paid total edit কোরো না।
        """,
        tip_en=r"""Lead with "an order is a snapshot in time" — it justifies the denormalisation in one sentence and shows you think in business terms, not just database terms.""",
        tip_bn=r""""Order হলো একটা নির্দিষ্ট সময়ের snapshot" — এই কথা দিয়ে শুরু করো। এক বাক্যেই denormalisation-এর যুক্তি দেওয়া হয়, আর বোঝা যায় তুমি শুধু database না, business-এর দৃষ্টিতেও ভাবো।""",
        mist_en=r"""Normalising order items into a separate collection by reflex, storing only `productId` and joining for the price, or keeping an ever-growing `orders` array in the user document.""",
        mist_bn=r"""অভ্যাসবশত order item আলাদা collection-এ normalise করা, শুধু `productId` রেখে দামের জন্য join করা, অথবা user document-এ ক্রমাগত বাড়তে থাকা `orders` array রাখা।""",
        code=r"""
            {
              _id: ObjectId("6709c2d3e4f5061728394a5b"),
              orderNumber: "ORD-2026-0001842",
              customerId: ObjectId("65aa0b1c2d3e4f5061728394"),
              status: "confirmed",
              items: [
                { productId: ObjectId("66c1a2b3c4d5e6f708192a3b"), sku: "EB-QCY-T13",
                  name: "QCY T13 Earbuds", unitPrice: NumberDecimal("1899.00"), qty: 2,
                  discount: NumberDecimal("200.00") }
              ],
              shipping: { name: "Nusrat Jahan", phone: "+8801711000000",
                          city: "Dhaka", area: "Mirpur 10", charge: NumberDecimal("60.00") },
              payment: { method: "bkash", status: "paid", trxId: "BK7X2Q9P" },
              totals: { subtotal: NumberDecimal("3798.00"), discount: NumberDecimal("200.00"),
                        delivery: NumberDecimal("60.00"), grandTotal: NumberDecimal("3658.00") },
              statusHistory: [ { status: "pending", at: ISODate("2026-10-12T05:10:00Z") },
                               { status: "confirmed", at: ISODate("2026-10-12T05:12:30Z") } ],
              createdAt: ISODate("2026-10-12T05:10:00Z")
            }
        """,
        lang="javascript",
        follow=[
            ("How would you prevent overselling the last unit during a flash sale?", "Flash sale-এ শেষ unit-টা overselling হওয়া কীভাবে আটকাবে?"),
            ("A product is renamed — should old orders change? Why or why not?", "একটা product-এর নাম বদলানো হলো — পুরনো order-এ কি নামও বদলাবে? কেন বা কেন না?"),
        ],
        related=["mongo-009", "mongo-013"],
        refs=[DATA_MODEL, ATOMICITY, PATTERNS],
    ),
    # ------------------------------------------------------------------ mongo-026
    Q(
        id="mongo-026", sub="Aggregation Pipelines", diff="hard", type="query",
        prio="medium", market="both", mins=8,
        tags=["setwindowfields", "window-functions", "running-total", "rank", "aggregation"],
        ver="MongoDB 5.0+ ($setWindowFields); current: MongoDB 9.0", vs=False, status="stable",
        q_en=r"""Using `dailySales` below, return each shop's daily rows with a **running total** of `amount` in date order and the day's **rank within its shop** by amount (highest = 1). Output `{ shop, day, amount, runningTotal, rankInShop }` sorted by shop and day, with `day` formatted as `YYYY-MM-DD`.""",
        q_bn=r"""নিচের `dailySales` ব্যবহার করে প্রতিটি shop-এর দৈনিক row return করো — তারিখের ক্রমে `amount`-এর **running total**, আর amount অনুযায়ী সেই দিনের **shop-এর ভেতরে rank** (সবচেয়ে বেশি = 1)। Output হবে `{ shop, day, amount, runningTotal, rankInShop }`, shop আর day অনুযায়ী sorted, আর `day` থাকবে `YYYY-MM-DD` format-এ।""",
        setup=r"""
            db.dailySales.insertMany([
              { shop: "A", day: ISODate("2026-10-01"), amount: 500 },
              { shop: "A", day: ISODate("2026-10-02"), amount: 300 },
              { shop: "A", day: ISODate("2026-10-03"), amount: 700 },
              { shop: "B", day: ISODate("2026-10-01"), amount: 200 },
              { shop: "B", day: ISODate("2026-10-02"), amount: 900 }
            ])
        """,
        setup_lang="javascript",
        code=r"""
            db.dailySales.aggregate([
              { $setWindowFields: {
                  partitionBy: "$shop",
                  sortBy: { day: 1 },
                  output: {
                    runningTotal: {
                      $sum: "$amount",
                      window: { documents: ["unbounded", "current"] }
                    }
                  }
              } },
              { $setWindowFields: {
                  partitionBy: "$shop",
                  sortBy: { amount: -1 },
                  output: { rankInShop: { $rank: {} } }
              } },
              { $sort: { shop: 1, day: 1 } },
              { $project: {
                  _id: 0,
                  shop: "$shop",
                  day: { $dateToString: { format: "%Y-%m-%d", date: "$day" } },
                  amount: "$amount",
                  runningTotal: "$runningTotal",
                  rankInShop: "$rankInShop"
              } }
            ])
        """,
        lang="javascript",
        output=r"""
            [
              { shop: 'A', day: '2026-10-01', amount: 500, runningTotal: 500, rankInShop: 2 },
              { shop: 'A', day: '2026-10-02', amount: 300, runningTotal: 800, rankInShop: 3 },
              { shop: 'A', day: '2026-10-03', amount: 700, runningTotal: 1500, rankInShop: 1 },
              { shop: 'B', day: '2026-10-01', amount: 200, runningTotal: 200, rankInShop: 2 },
              { shop: 'B', day: '2026-10-02', amount: 900, runningTotal: 1100, rankInShop: 1 }
            ]
        """,
        a_en=r"""
            `$setWindowFields` is MongoDB's window-function stage (like SQL `OVER (PARTITION BY ... ORDER BY ...)`). Unlike `$group`, it **keeps every document** and adds computed fields.

            - **Stage 1** partitions by shop, sorts by day, and sums `amount` over a window from the first document to the current one → running totals A: 500, 800, 1500; B: 200, 1100.
            - **Stage 2** needs a different sort order (amount descending), and each stage has one `sortBy`, so a second stage computes `$rank` → A: 700 → 1, 500 → 2, 300 → 3; B: 900 → 1, 200 → 2.
            - `$sort` restores shop/day order, and `$project` formats the date and shapes the output.
        """,
        a_bn=r"""
            `$setWindowFields` হলো MongoDB-র window-function stage (SQL-এর `OVER (PARTITION BY ... ORDER BY ...)`-এর মতো)। `$group`-এর মতো না, এটা **প্রতিটি document রেখে দেয়** আর computed field যোগ করে।

            - **Stage 1** shop অনুযায়ী partition করে, day অনুযায়ী sort করে, আর প্রথম document থেকে current document পর্যন্ত window-তে `amount` যোগ করে → running total A: 500, 800, 1500; B: 200, 1100।
            - **Stage 2**-এ আলাদা sort order লাগে (amount descending), আর প্রতিটি stage-এ একটাই `sortBy` থাকে, তাই দ্বিতীয় একটা stage `$rank` হিসাব করে → A: 700 → 1, 500 → 2, 300 → 3; B: 900 → 1, 200 → 2।
            - `$sort` আবার shop/day order-এ সাজায়, আর `$project` date format করে output-এর shape ঠিক করে।
        """,
        ex_en=r"""
            - **The explicit window matters:** with `sortBy` but no `window`, `$sum` covers the whole partition — every row would show the shop's grand total (1500 or 1100) instead of a running total.
            - **Ties:** `$rank` gives tied values the same rank and leaves gaps (1, 1, 3); `$denseRank` doesn't leave gaps (1, 1, 2); `$documentNumber` always increments.
            - **Other windows:** `range: [-6, 0], unit: "day"` on a date `sortBy` gives a 7-day moving sum/average; `$shift` reads the previous/next row (day-over-day change).
            - **Timezones:** `$dateToString` formats in UTC unless you pass `timezone: "Asia/Dhaka"` — store days consistently.
            - **Performance:** each partition is sorted (100 MB per-stage memory limit, can spill to disk); `$match` first and an index on `{ shop: 1, day: 1 }` help the first stage.
        """,
        ex_bn=r"""
            - **Explicit window জরুরি:** `sortBy` দিয়ে কিন্তু `window` ছাড়া দিলে `$sum` পুরো partition জুড়ে হিসাব করে — প্রতিটি row-তে running total-এর বদলে shop-এর grand total (1500 বা 1100) দেখাত।
            - **Tie:** `$rank` সমান value-কে একই rank দেয় আর ফাঁক রাখে (1, 1, 3); `$denseRank` ফাঁক রাখে না (1, 1, 2); `$documentNumber` সবসময় বাড়ে।
            - **অন্য window:** date `sortBy`-তে `range: [-6, 0], unit: "day"` দিলে 7 দিনের moving sum/average পাওয়া যায়; `$shift` আগের/পরের row পড়ে (দিন-থেকে-দিন পরিবর্তন)।
            - **Timezone:** `timezone: "Asia/Dhaka"` না দিলে `$dateToString` UTC-তে format করে — day সবসময় consistent ভাবে store করো।
            - **Performance:** প্রতিটি partition sort হয় (প্রতি stage-এ 100 MB memory limit, disk-এ spill করতে পারে); শুরুতে `$match` আর `{ shop: 1, day: 1 }`-এ index প্রথম stage-কে সাহায্য করে।
        """,
        tip_en=r"""Relate it to SQL window functions in one line — many interviewers know SQL better than MongoDB, and the mapping makes your answer instantly clear.""",
        tip_bn=r"""এক লাইনে SQL window function-এর সাথে মিলিয়ে বলো — অনেক interviewer MongoDB-র চেয়ে SQL ভালো জানে, আর এই তুলনা তোমার উত্তরকে সাথে সাথে পরিষ্কার করে দেয়।""",
        mist_en=r"""Using `$group` (which collapses rows), forgetting the `window` bounds for a running total, or trying to use two different `sortBy` orders in one stage.""",
        mist_bn=r"""`$group` ব্যবহার করা (এতে row একত্র হয়ে যায়), running total-এর জন্য `window`-এর সীমা ভুলে যাওয়া, অথবা একটা stage-এ দুইটা ভিন্ন `sortBy` order ব্যবহারের চেষ্টা করা।""",
        follow=[
            ("How would you compute a 7-day moving average of sales per shop?", "প্রতিটি shop-এর বিক্রির 7 দিনের moving average কীভাবে হিসাব করবে?"),
            ("How would you get only the top 2 days per shop?", "প্রতিটি shop-এর শুধু top 2 দিন কীভাবে বের করবে?"),
        ],
        related=["mongo-012"],
        refs=[WINDOW],
    ),
    # ------------------------------------------------------------------ mongo-032
    Q(
        id="mongo-032", sub="Backup & Recovery", diff="extreme", type="scenario",
        prio="high", market="both", mins=20,
        tags=["backup", "point-in-time-recovery", "oplog", "mongodump", "incident", "disaster-recovery"],
        ver="Version-independent concept (current: MongoDB 9.0, Database Tools)", vs=False, status="stable",
        q_en=r"""At 14:05 (Dhaka time) a migration script on production ran `db.orders.deleteMany({})` instead of deleting only test orders. The replica set holds ~400 GB, and the only backups are nightly `mongodump` archives taken at 02:00. New orders keep coming in. How do you recover, what should the backup strategy have been, and how do you prevent this from happening again?""",
        q_bn=r"""দুপুর 14:05-এ (ঢাকার সময়) production-এ একটা migration script শুধু test order delete করার বদলে `db.orders.deleteMany({})` চালিয়ে দিয়েছে। Replica set-এ প্রায় 400 GB data, আর backup বলতে শুধু রাত 02:00-এ নেওয়া nightly `mongodump` archive। নতুন order আসতেই থাকছে। তুমি কীভাবে recover করবে, backup strategy কেমন হওয়া উচিত ছিল, আর ভবিষ্যতে এটা কীভাবে আটকাবে?""",
        a_en=r"""
            *(Advanced: production incident and disaster-recovery design.)*

            **1. Contain.** Stop the script and revoke its credentials. Don't restore over production — orders placed after 14:05 are real and must be kept. Remember replication didn't help: the deletes reached every secondary in milliseconds (unless you had a delayed hidden member).

            **2. Rebuild in an isolated recovery cluster.** Restore the 02:00 dump there. Then roll it forward with the **oplog**: dump the production oplog entries since the backup started, find the timestamp of the first delete from the script, and `mongorestore --oplogReplay --oplogLimit <that ts>` so the copy reflects everything up to 14:04:59. This only works if the oplog window still covers 02:00 → 14:05 — check it immediately, before those entries roll off.

            **3. Merge back.** `mongorestore` only inserts and never overwrites existing `_id`s, so restoring the recovered `orders` collection into production adds the deleted orders while keeping the new ones. Validate counts and totals against the payment gateway and courier records before announcing recovery.

            **4. What the strategy should be:** for 400 GB, nightly `mongodump` means a 12-hour RPO and a slow RTO. Use **snapshots + continuous oplog backup with point-in-time recovery** (Atlas cloud backup, or Ops/Cloud Manager when self-managed), defined RPO/RTO targets, backups in a separate account/region, encryption, immutability (ransomware), and regular **restore drills**. A delayed hidden secondary is a useful extra safety net, not a backup.

            **5. Prevent:** reviewed migrations with a dry-run count, a guard that refuses empty filters, least-privilege roles (the app user can't run ad-hoc admin scripts), no standing human write access to production, and soft deletes for business-critical data.
        """,
        a_bn=r"""
            *(Advanced: production incident আর disaster-recovery design।)*

            **1. Contain করো।** Script থামাও আর তার credential revoke করো। Production-এর ওপর restore কোরো না — 14:05-এর পরে আসা order-গুলো আসল, সেগুলো রাখতে হবে। মনে রেখো replication কোনো কাজে আসেনি: delete কয়েক millisecond-এর মধ্যে সব secondary-তে পৌঁছে গেছে (delayed hidden member না থাকলে)।

            **2. আলাদা একটা recovery cluster-এ data আবার তৈরি করো।** সেখানে 02:00-এর dump restore করো। তারপর **oplog** দিয়ে সামনে এগিয়ে নাও: backup শুরুর পর থেকে production-এর oplog entry dump করো, script-এর প্রথম delete-এর timestamp খুঁজে বের করো, আর `mongorestore --oplogReplay --oplogLimit <সেই ts>` চালাও — তাহলে copy-টা 14:04:59 পর্যন্ত সবকিছু প্রতিফলিত করবে। এটা শুধু তখনই সম্ভব যদি oplog window এখনো 02:00 → 14:05 cover করে — entry-গুলো হারিয়ে যাওয়ার আগে এখনই check করো।

            **3. আবার merge করো।** `mongorestore` শুধু insert করে, existing `_id` কখনো overwrite করে না — তাই recovered `orders` collection production-এ restore করলে delete হওয়া order ফিরে আসে আর নতুনগুলোও থাকে। Recovery ঘোষণার আগে payment gateway আর courier-এর record-এর সাথে count ও total মিলিয়ে নাও।

            **4. Strategy কেমন হওয়া উচিত ছিল:** 400 GB-র জন্য nightly `mongodump` মানে 12 ঘণ্টার RPO আর ধীর RTO। ব্যবহার করো **snapshot + continuous oplog backup, point-in-time recovery সহ** (Atlas cloud backup, অথবা self-managed হলে Ops/Cloud Manager), নির্দিষ্ট RPO/RTO target, আলাদা account/region-এ backup, encryption, immutability (ransomware-এর জন্য), আর নিয়মিত **restore drill**। Delayed hidden secondary একটা বাড়তি safety net, backup না।

            **5. প্রতিরোধ:** dry-run count সহ review করা migration, empty filter reject করার guard, least-privilege role (app user ad-hoc admin script চালাতে পারবে না), production-এ মানুষের স্থায়ী write access না রাখা, আর business-critical data-র জন্য soft delete।
        """,
        ex_en=r"""
            - **Why `mongodump` alone is weak at this size:** the docs position `mongodump`/`mongorestore` for small deployments; dumps are logical (indexes are rebuilt on restore, which takes hours for 400 GB) and have no point-in-time capability on their own. Filesystem/cloud snapshots restore much faster, and oplog-based continuous backup provides PITR.
            - **Finding the bad operation:** a `deleteMany` writes one delete op (`op: "d"`) per document, but since MongoDB 6.1 multi-document deletes are **batched**, so those ops are grouped inside `applyOps` entries (`op: "c"`, `ns: "admin.$cmd"`). Search for both shapes; the first matching entry for `shop.orders` after 14:05 gives the cut-off timestamp. Oplog entries also carry a `wall` clock time — remember 14:05 in Dhaka is 08:05 UTC.
            - **Sharded clusters:** a consistent point-in-time restore across shards is much harder by hand — another reason to use managed backup tooling.
            - **Communication:** an incident timeline, a status update to support and a blameless post-mortem with concrete action items are part of a senior answer.
            - **Test restores:** an untested backup is a hope, not a plan.
        """,
        ex_bn=r"""
            - **এই আকারে শুধু `mongodump` কেন দুর্বল:** docs অনুযায়ী `mongodump`/`mongorestore` ছোট deployment-এর জন্য; dump হলো logical (restore-এর সময় index আবার build হয়, 400 GB-তে ঘণ্টার পর ঘণ্টা লাগে) আর নিজে থেকে point-in-time সুবিধা নেই। Filesystem/cloud snapshot অনেক দ্রুত restore হয়, আর oplog-ভিত্তিক continuous backup PITR দেয়।
            - **খারাপ operation খুঁজে বের করা:** `deleteMany` প্রতিটি document-এর জন্য একটা করে delete op (`op: "d"`) লেখে, কিন্তু MongoDB 6.1 থেকে multi-document delete **batch** করা হয়, তাই সেই op-গুলো `applyOps` entry-র (`op: "c"`, `ns: "admin.$cmd"`) ভেতরে group হয়ে থাকে। দুই ধরনের entry-ই খোঁজো; 14:05-এর পরে `shop.orders`-এর প্রথম matching entry থেকেই cut-off timestamp পাওয়া যায়। Oplog entry-তে `wall` clock time-ও থাকে — মনে রেখো ঢাকার 14:05 মানে UTC 08:05।
            - **Sharded cluster:** সব shard জুড়ে consistent point-in-time restore হাতে করা অনেক কঠিন — managed backup tooling ব্যবহারের আরেকটা কারণ।
            - **যোগাযোগ:** incident timeline, support-কে status update, আর concrete action item সহ একটা blameless post-mortem — এগুলোও senior-level উত্তরের অংশ।
            - **Restore test করো:** test না করা backup একটা আশা মাত্র, plan না।
        """,
        tip_en=r"""Structure it as contain → recover → validate → prevent, and state RPO/RTO numbers explicitly. Saying "I'd check the oplog window first, before it rolls over" shows real incident instincts.""",
        tip_bn=r"""Contain → recover → validate → prevent — এভাবে সাজাও, আর RPO/RTO-র সংখ্যা স্পষ্ট করে বলো। "Oplog roll over হওয়ার আগে আমি প্রথমেই oplog window check করব" — এই কথাটা আসল incident সামলানোর অভিজ্ঞতা দেখায়।""",
        mist_en=r"""Restoring the nightly dump directly over production (losing 12 hours of orders plus everything after 14:05); assuming replica set members are backups; never having tested a restore.""",
        mist_bn=r"""Nightly dump সরাসরি production-এর ওপর restore করা (12 ঘণ্টার order আর 14:05-এর পরের সব হারানো); replica set member-কে backup মনে করা; কখনো restore test না করা।""",
        code=r"""
            # 1) Restore last night's dump into an isolated recovery cluster (never over prod)
            mongorestore --uri "$RECOVERY_URI" --gzip --archive=shop-2026-10-12-0200.gz

            # 2) On prod: find the first delete from the bad script (14:05 Dhaka = 08:05 UTC).
            #    Multi-deletes are batched into applyOps entries since 6.1, so match both shapes.
            mongosh "$PROD_URI" --quiet --eval '
              db.getSiblingDB("local").oplog.rs
                .find({
                  wall: { $gte: ISODate("2026-10-12T08:05:00Z") },
                  $or: [
                    { ns: "shop.orders", op: "d" },
                    { op: "c", "o.applyOps": { $elemMatch: { ns: "shop.orders", op: "d" } } }
                  ]
                })
                .sort({ $natural: 1 }).limit(1)'

            # 3) Dump oplog entries since the backup started (02:00 Dhaka = 1791748800)
            #    and replay them up to, but not including, the bad delete's ts
            mongodump --uri "$PROD_URI" -d local -c oplog.rs \
              --query '{ "ts": { "$gte": { "$timestamp": { "t": 1791748800, "i": 1 } } } }' \
              --out oplogdump
            mkdir -p replay && mv oplogdump/local/oplog.rs.bson replay/oplog.bson
            mongorestore --uri "$RECOVERY_URI" --oplogReplay --oplogLimit 1791792303:1 replay/

            # 4) Copy the recovered orders back: inserts only, existing _ids are not overwritten
            mongodump --uri "$RECOVERY_URI" -d shop -c orders --archive=orders-recovered.archive
            mongorestore --uri "$PROD_URI" --archive=orders-recovered.archive --nsInclude "shop.orders"
        """,
        lang="bash",
        follow=[
            ("How would you define RPO and RTO for an e-commerce database, and who decides them?", "একটা e-commerce database-এর RPO আর RTO কীভাবে ঠিক করবে, আর সেটা কে ঠিক করে?"),
            ("How does a delayed hidden secondary help here, and what are its limits?", "এখানে delayed hidden secondary কীভাবে সাহায্য করে, আর এর সীমাবদ্ধতা কী?"),
            ("How do you protect backups from ransomware or a compromised admin account?", "Ransomware বা compromised admin account থেকে backup কীভাবে রক্ষা করবে?"),
        ],
        related=["mongo-010", "mongo-031"],
        refs=[BACKUPS, MONGODUMP, SEC_CHECKLIST],
    ),
]

if __name__ == "__main__":
    save("mongodb", "b3", QUESTIONS)
