# MongoDB — batch 4 (mongo-018..022, mongo-027..029)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

TXN = ("MongoDB Manual — Transactions", "https://www.mongodb.com/docs/manual/core/transactions/")
TXN_PROD = ("MongoDB Manual — Production Considerations (Transactions)", "https://www.mongodb.com/docs/manual/core/transactions-production-consideration/")
ATOMICITY = ("MongoDB Manual — Atomicity and Transactions", "https://www.mongodb.com/docs/manual/core/write-operations-atomicity/")
NODE_TXN = ("MongoDB Node.js Driver — Transactions", "https://www.mongodb.com/docs/drivers/node/current/crud/transactions/")
WRITE_CONCERN = ("MongoDB Manual — Write Concern", "https://www.mongodb.com/docs/manual/reference/write-concern/")
READ_CONCERN = ("MongoDB Manual — Read Concern", "https://www.mongodb.com/docs/manual/reference/read-concern/")
TEXT_INDEX = ("MongoDB Manual — Text Indexes", "https://www.mongodb.com/docs/manual/core/indexes/index-types/index-text/")
ATLAS_SEARCH = ("MongoDB Atlas — Atlas Search", "https://www.mongodb.com/docs/atlas/atlas-search/")
REGEX = ("MongoDB Manual — $regex", "https://www.mongodb.com/docs/manual/reference/operator/query/regex/")
FOAU = ("MongoDB Manual — db.collection.findOneAndUpdate()", "https://www.mongodb.com/docs/manual/reference/method/db.collection.findOneAndUpdate/")
NODE_DRIVER = ("MongoDB Node.js Driver documentation", "https://www.mongodb.com/docs/drivers/node/current/")
RN_90 = ("MongoDB 9.0 Release Notes", "https://www.mongodb.com/docs/manual/release-notes/9.0/")
VERSIONS = ("MongoDB Versions and Upgrade Paths", "https://www.mongodb.com/docs/mongodb-versions/")
VALIDATION = ("MongoDB Manual — Schema Validation", "https://www.mongodb.com/docs/manual/core/schema-validation/")
SEC_CHECKLIST = ("MongoDB Manual — Security Checklist", "https://www.mongodb.com/docs/manual/administration/security-checklist/")
OWASP_NOSQL = ("OWASP — NoSQL Security Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Security_Cheat_Sheet.html")
RBAC = ("MongoDB Manual — Role-Based Access Control", "https://www.mongodb.com/docs/manual/core/authorization/")
PATTERNS = ("MongoDB Manual — Schema Design Patterns", "https://www.mongodb.com/docs/manual/data-modeling/design-patterns/")
GROUP_DATA = ("MongoDB Manual — Group Data (bucket & outlier patterns)", "https://www.mongodb.com/docs/manual/data-modeling/design-patterns/group-data/")
COMPUTED = ("MongoDB Manual — Handle Computed Values", "https://www.mongodb.com/docs/manual/data-modeling/design-patterns/handle-computed-values/")

QUESTIONS = [
    # ------------------------------------------------------------------ mongo-018
    Q(
        id="mongo-018", sub="Transactions & Atomicity", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["transactions", "atomicity", "single-document", "replica-set"],
        ver="Version-independent concept (multi-document transactions since 4.0/4.2; current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""MongoDB guarantees atomicity for single-document writes. When do you actually need a multi-document transaction, and what should you keep in mind when you use one?""",
        q_bn=r"""MongoDB single-document write-এর জন্য atomicity guarantee করে। তাহলে কখন আসলে multi-document transaction লাগে, আর ব্যবহার করার সময় কী কী মাথায় রাখবে?""",
        a_en=r"""
            A write to one document — including all its embedded objects and arrays — is always atomic. So my first move is to **model the data so an invariant lives in one document** (an order with its items, a wallet with its balance) and use operators like `$inc` with a conditional filter. That covers most cases without a transaction.

            I use a multi-document transaction when an invariant spans several documents or collections that must change together: moving money between two wallets, or creating an order + decrementing stock for several products + writing a ledger entry.

            Things to keep in mind:
            - Transactions need a **replica set or sharded cluster** (a single-node replica set works for local development).
            - Keep them **short**: by default a transaction is aborted after 60 seconds, and long transactions hold resources and cause write conflicts. No external API calls or user interaction inside.
            - **Retry** on `TransientTransactionError` / `UnknownTransactionCommitResult` — the driver's `withTransaction()` does this for you.
            - Commit with `w: "majority"`.
        """,
        a_bn=r"""
            একটা document-এ write — তার সব embedded object আর array সহ — সবসময় atomic। তাই আমার প্রথম পদক্ষেপ হলো **data এমনভাবে model করা যাতে একটা invariant একটা document-এর মধ্যেই থাকে** (item সহ order, balance সহ wallet), আর conditional filter সহ `$inc`-এর মতো operator ব্যবহার করা। বেশিরভাগ ক্ষেত্রে transaction ছাড়াই এতে কাজ হয়ে যায়।

            Multi-document transaction ব্যবহার করি যখন একটা invariant কয়েকটা document বা collection জুড়ে থাকে, যেগুলো একসাথে বদলাতে হবে: দুইটা wallet-এর মধ্যে টাকা সরানো, অথবা order তৈরি + কয়েকটা product-এর stock কমানো + ledger entry লেখা।

            যা মাথায় রাখতে হবে:
            - Transaction-এর জন্য **replica set বা sharded cluster** লাগে (local development-এ single-node replica set চলে)।
            - **ছোট রাখো**: default-ভাবে 60 second পর transaction abort হয়, আর লম্বা transaction resource ধরে রাখে ও write conflict তৈরি করে। ভেতরে কোনো external API call বা user interaction না।
            - `TransientTransactionError` / `UnknownTransactionCommitResult`-এ **retry** করো — driver-এর `withTransaction()` এটা নিজেই করে।
            - `w: "majority"` দিয়ে commit করো।
        """,
        ex_en=r"""
            - **Cost:** transactions add latency and coordination (especially across shards), and conflicting writes abort with `WriteConflict` and get retried. They're a tool, not a default.
            - **Size:** there's no hard document limit, but MongoDB recommends modifying no more than about 1,000 documents per transaction; break up bulk jobs.
            - **Isolation:** reads inside a transaction see a consistent snapshot; outside readers don't see uncommitted changes.
            - **MongoDB 9.0:** `maxConcurrentMultiDocumentTransactions` defaults to 10,000; beyond that new transactions fail with `TooManyOpenTransactions` — another reason to keep them short.
            - **Idempotency:** because the callback may run more than once, side effects (emails, SMS, payment calls) belong *after* the commit, not inside.
        """,
        ex_bn=r"""
            - **খরচ:** transaction latency আর coordination বাড়ায় (বিশেষ করে shard-এর মধ্যে), আর conflicting write `WriteConflict` দিয়ে abort হয়ে retry হয়। এটা একটা tool, default পছন্দ না।
            - **Size:** document-এর কোনো hard limit নেই, কিন্তু MongoDB একটা transaction-এ মোটামুটি 1,000-এর বেশি document modify না করার পরামর্শ দেয়; bulk job ভেঙে নাও।
            - **Isolation:** transaction-এর ভেতরের read একটা consistent snapshot দেখে; বাইরের reader uncommitted পরিবর্তন দেখে না।
            - **MongoDB 9.0:** `maxConcurrentMultiDocumentTransactions`-এর default 10,000; এর বেশি হলে নতুন transaction `TooManyOpenTransactions` দিয়ে fail করে — transaction ছোট রাখার আরেকটা কারণ।
            - **Idempotency:** callback একাধিকবার চলতে পারে, তাই side effect (email, SMS, payment call) commit-এর *পরে* রাখো, ভেতরে না।
        """,
        tip_en=r"""Start with "first, can I avoid it with a single-document design?" — interviewers want to see that you don't reach for transactions by reflex, then show you know how to use them correctly when needed.""",
        tip_bn=r""""প্রথমে দেখি single-document design দিয়ে এড়ানো যায় কি না" — এভাবে শুরু করো। Interviewer দেখতে চায় তুমি অভ্যাসবশত transaction ব্যবহার করো না, আর দরকার হলে সঠিকভাবে ব্যবহার করতে জানো।""",
        mist_en=r"""Claiming MongoDB has no transactions; wrapping every request in a transaction; running transactions against a standalone `mongod`; calling a payment API inside the transaction callback.""",
        mist_bn=r"""MongoDB-তে transaction নেই বলা; প্রতিটি request transaction-এ মুড়ে দেওয়া; standalone `mongod`-এ transaction চালানো; transaction callback-এর ভেতরে payment API call করা।""",
        code=r"""
            // Often no transaction is needed: one atomic, conditional update
            db.wallets.updateOne(
              { _id: userId, balance: { $gte: 500 } },          // only if enough balance
              {
                $inc: { balance: -500 },
                $push: { recentTx: { $each: [tx], $slice: -20 } } // bounded history
              }
            )
            // matchedCount === 0  →  insufficient balance (nothing changed)
        """,
        lang="javascript",
        follow=[
            ("How would you run transactions in local development and CI?", "Local development আর CI-তে transaction কীভাবে চালাবে?"),
            ("What happens if two transactions update the same document at the same time?", "দুইটা transaction একই সময়ে একই document update করলে কী হয়?"),
        ],
        related=["mongo-004", "mongo-017"],
        refs=[ATOMICITY, TXN, TXN_PROD],
    ),
    # ------------------------------------------------------------------ mongo-019
    Q(
        id="mongo-019", sub="Replication & Consistency", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["write-concern", "majority", "durability", "replica-set"],
        ver="Version-independent concept (default w:majority since MongoDB 5.0; current: 9.0)", vs=False, status="stable",
        q_en=r"""In a replica set, what does `writeConcern: { w: "majority" }` guarantee once the write is acknowledged?""",
        q_bn=r"""একটা replica set-এ write acknowledge হওয়ার পর `writeConcern: { w: "majority" }` কী guarantee করে?""",
        options=[
            (r"""The write has been applied on every member of the replica set, including all secondaries""",
             r"""Write-টা replica set-এর প্রতিটি member-এ, সব secondary সহ, apply হয়ে গেছে"""),
            (r"""The write is in the primary's memory, and it will be replicated later without any durability guarantee""",
             r"""Write-টা primary-র memory-তে আছে, পরে replicate হবে, কিন্তু durability-র কোনো guarantee নেই"""),
            (r"""The write is durable on a majority of data-bearing voting members, so it won't be rolled back if the primary fails""",
             r"""Write-টা data-bearing voting member-দের majority-তে durable হয়েছে, তাই primary fail করলেও rollback হবে না"""),
            (r"""Any read from any secondary immediately afterwards is guaranteed to see the write""",
             r"""এরপর সাথে সাথে যেকোনো secondary থেকে যেকোনো read-এ write-টা দেখা যাবেই"""),
        ],
        correct=2,
        a_en=r"""`w: "majority"` waits until a majority of the data-bearing voting members have applied (and, by default, journaled) the write. Any newly elected primary must come from that majority, so the write survives failover and won't be rolled back.""",
        a_bn=r"""`w: "majority"` ততক্ষণ অপেক্ষা করে যতক্ষণ না data-bearing voting member-দের majority write-টা apply (আর default-ভাবে journal) করে। নতুন যে primary-ই elect হোক, তাকে ওই majority থেকেই আসতে হবে — তাই write failover-এর পরও টিকে থাকে, rollback হয় না।""",
        ex_en=r"""
            Option D is the tempting one: majority acknowledgement says nothing about **which** secondaries have the write. A lagging secondary outside that majority can still return stale data. For read-your-writes you read from the primary, or use `readConcern: "majority"` with a causally consistent session.

            Option A would be `w: <number of all members>` — rarely used because one slow or down member blocks every write. Option B roughly describes `w: 1` with no journaling, which is fast but can lose acknowledged writes during a failover. Since MongoDB 5.0 the implicit default write concern is `majority` for most replica sets.
        """,
        ex_bn=r"""
            সবচেয়ে বিভ্রান্তিকর হলো option D: majority acknowledgement **কোন** secondary-তে write আছে সে বিষয়ে কিছুই বলে না। ওই majority-র বাইরের পিছিয়ে থাকা secondary তখনও stale data দিতে পারে। Read-your-writes-এর জন্য primary থেকে পড়ো, অথবা causally consistent session-এ `readConcern: "majority"` ব্যবহার করো।

            Option A হবে `w: <সব member-এর সংখ্যা>` — খুব কম ব্যবহার হয়, কারণ একটা slow বা down member থাকলে সব write আটকে যায়। Option B মোটামুটি journaling ছাড়া `w: 1`-এর বর্ণনা — দ্রুত, কিন্তু failover-এ acknowledged write হারাতে পারে। MongoDB 5.0 থেকে বেশিরভাগ replica set-এ implicit default write concern হলো `majority`।
        """,
        tip_en=r"""Separate durability (write concern) from visibility (read concern / read preference) — mixing them up is the most common mistake, and naming the distinction is a strong signal.""",
        tip_bn=r"""Durability (write concern) আর visibility (read concern / read preference) আলাদা করে বলো — এই দুটো গুলিয়ে ফেলাই সবচেয়ে common ভুল, আর পার্থক্যটা স্পষ্ট করলে শক্তিশালী signal যায়।""",
        follow=[
            ("What is the latency cost of `w: \"majority\"` in a multi-region replica set?", "Multi-region replica set-এ `w: \"majority\"`-এর latency খরচ কেমন?"),
        ],
        related=["mongo-010", "mongo-031"],
        refs=[WRITE_CONCERN, READ_CONCERN],
    ),
    # ------------------------------------------------------------------ mongo-020
    Q(
        id="mongo-020", sub="Text Indexes & Atlas Search", diff="medium", type="comparison",
        prio="medium", market="both", mins=6,
        tags=["text-index", "atlas-search", "regex", "search", "relevance"],
        ver="Version-independent concept (current: MongoDB 9.0; Atlas Search / MongoDB Search on Atlas or self-managed via mongot)", vs=False, status="stable",
        q_en=r"""Your product search uses `{ name: { $regex: term, $options: "i" } }` and is getting slow. Compare `$regex`, a MongoDB **text index**, and **Atlas Search** for a product search box. Which would you choose?""",
        q_bn=r"""তোমার product search `{ name: { $regex: term, $options: "i" } }` ব্যবহার করে, আর এটা slow হয়ে যাচ্ছে। একটা product search box-এর জন্য `$regex`, MongoDB **text index** আর **Atlas Search**-এর তুলনা করো। তুমি কোনটা বেছে নেবে?""",
        a_en=r"""
            - **`$regex`:** simple, but a case-insensitive or "contains" regex can't use an index efficiently — at best it scans the whole index. No relevance ranking, no stemming, no typo tolerance. User input must be escaped. Fine for small admin filters or case-sensitive prefix searches (`^abc`).
            - **Text index (`$text`):** tokenises and stems words for supported languages, ignores stop words and ranks by `textScore`. One text index per collection (it can cover several weighted fields). But no fuzzy matching, no autocomplete / partial words, and limited language support.
            - **Atlas Search (`$search`, now branded MongoDB Search):** a Lucene-based search process (`mongot`) that runs alongside the database and keeps its indexes in sync automatically. Atlas manages it for you; since mid-2026 it is also GA for self-managed Community Edition, where you deploy and operate `mongot` yourself. It supports fuzzy matching (typos), autocomplete, synonyms, highlighting, facets, custom analyzers and relevance tuning.

            For a customer-facing search box I'd choose **`$search`** — users type "wirless earbud" and still expect results. On Atlas it's the obvious choice. Self-managed, I'd compare running `mongot` ourselves with a dedicated engine we may already operate (OpenSearch/Elasticsearch, Meilisearch); a text index is only enough when typo tolerance, autocomplete and facets aren't requirements.
        """,
        a_bn=r"""
            - **`$regex`:** সহজ, কিন্তু case-insensitive বা "contains" regex দক্ষভাবে index ব্যবহার করতে পারে না — বড়জোর পুরো index scan করে। Relevance ranking নেই, stemming নেই, typo tolerance নেই। User input escape করতে হয়। ছোট admin filter বা case-sensitive prefix search-এর (`^abc`) জন্য ঠিক আছে।
            - **Text index (`$text`):** supported language-এ শব্দ tokenise আর stem করে, stop word বাদ দেয় আর `textScore` দিয়ে rank করে। প্রতি collection-এ একটাই text index (কয়েকটা weighted field cover করতে পারে)। কিন্তু fuzzy matching নেই, autocomplete / আংশিক শব্দ নেই, আর language support সীমিত।
            - **Atlas Search (`$search`, এখন MongoDB Search নামে):** database-এর পাশাপাশি চলা একটা Lucene-ভিত্তিক search process (`mongot`), যেটা নিজের index automatically sync রাখে। Atlas-এ এটা Atlas নিজেই manage করে; 2026-এর মাঝামাঝি থেকে self-managed Community Edition-এও এটা GA, সেখানে `mongot` নিজেকে deploy আর চালাতে হয়। Fuzzy matching (typo), autocomplete, synonym, highlighting, facet, custom analyzer আর relevance tuning support করে।

            Customer-facing search box-এর জন্য আমি **`$search`** বেছে নেব — user "wirless earbud" লিখলেও result আশা করে। Atlas-এ থাকলে এটাই স্বাভাবিক পছন্দ। Self-managed হলে নিজে `mongot` চালানো আর আগে থেকে চালানো কোনো dedicated engine-এর (OpenSearch/Elasticsearch, Meilisearch) মধ্যে তুলনা করব; typo tolerance, autocomplete আর facet দরকার না হলেই কেবল text index যথেষ্ট।
        """,
        ex_en=r"""
            - **Banglish & Bangla text:** many local users search in romanised Bangla ("chal", "dal") or Bangla script. The built-in text index has no Bangla stemming, so you'd use language `"none"` (exact tokens) — another argument for a configurable analyzer or synonyms.
            - **Regex safety:** build regexes from user input only after escaping special characters (otherwise `.*` patterns or catastrophic backtracking can hurt the server), and cap the input length.
            - **Operational cost:** `$search` runs separate `mongot` processes with their own resources and index sync lag (usually seconds) — on self-managed deployments you size, monitor and upgrade them yourself. An external engine means another system to run plus a sync pipeline (change streams/CDC).
            - **Sorting:** with `$text`, sort by `{ score: { $meta: "textScore" } }`; with Atlas Search, results come back in relevance order and `$meta: "searchScore"` exposes the score.
        """,
        ex_bn=r"""
            - **Banglish ও বাংলা text:** অনেক local user romanised Bangla ("chal", "dal") বা বাংলা হরফে search করে। Built-in text index-এ বাংলা stemming নেই, তাই language `"none"` (exact token) ব্যবহার করতে হয় — configurable analyzer বা synonym-এর পক্ষে আরেকটা যুক্তি।
            - **Regex safety:** user input থেকে regex বানানোর আগে special character escape করো (না হলে `.*` pattern বা catastrophic backtracking server-এর ক্ষতি করতে পারে), আর input-এর length সীমিত রাখো।
            - **Operational খরচ:** `$search` আলাদা `mongot` process চালায়, তার নিজস্ব resource আর index sync lag (সাধারণত কয়েক second) থাকে — self-managed deployment-এ এগুলোর sizing, monitoring আর upgrade তোমাকেই করতে হয়। External engine মানে আরেকটা system চালানো আর একটা sync pipeline (change stream/CDC)।
            - **Sorting:** `$text`-এ `{ score: { $meta: "textScore" } }` দিয়ে sort করো; Atlas Search-এ result relevance order-এ আসে, আর `$meta: "searchScore"` দিয়ে score দেখা যায়।
        """,
        tip_en=r"""Frame it by user experience (typos, ranking, autocomplete) rather than by features — then the choice becomes obvious and you sound product-minded.""",
        tip_bn=r"""Feature দিয়ে না, user experience (typo, ranking, autocomplete) দিয়ে তুলনাটা সাজাও — তাহলে পছন্দটা স্বাভাবিকভাবেই পরিষ্কার হয়, আর তোমাকে product-minded মনে হয়।""",
        mist_en=r"""Assuming a regular index makes `/term/i` fast; creating multiple text indexes on one collection; passing raw user input into `$regex`.""",
        mist_bn=r"""ধরে নেওয়া যে সাধারণ index `/term/i`-কে দ্রুত করবে; এক collection-এ একাধিক text index বানানো; raw user input সরাসরি `$regex`-এ দেওয়া।""",
        code=r"""
            // Text index: one per collection, weighted fields
            db.products.createIndex(
              { name: "text", description: "text" },
              { weights: { name: 10, description: 2 }, default_language: "english" }
            )
            db.products.find(
              { $text: { $search: "wireless earbuds" } },
              { name: 1, price: 1, score: { $meta: "textScore" } }
            ).sort({ score: { $meta: "textScore" } }).limit(20)

            // Atlas Search: fuzzy matching handles the typo (needs an Atlas Search index "products")
            db.products.aggregate([
              { $search: {
                  index: "products",
                  text: { query: "wirless earbud", path: ["name", "description"], fuzzy: { maxEdits: 1 } }
              } },
              { $limit: 20 },
              { $project: { name: 1, price: 1, score: { $meta: "searchScore" } } }
            ])
        """,
        lang="javascript",
        follow=[
            ("How would you implement search-as-you-type autocomplete?", "Type করার সাথে সাথে autocomplete কীভাবে implement করবে?"),
            ("How would you keep an external search engine in sync with MongoDB?", "External search engine-কে MongoDB-র সাথে কীভাবে sync রাখবে?"),
        ],
        related=["mongo-006", "mongo-008"],
        refs=[TEXT_INDEX, ATLAS_SEARCH, REGEX],
    ),
    # ------------------------------------------------------------------ mongo-021
    Q(
        id="mongo-021", sub="CRUD", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["findoneandupdate", "upsert", "returndocument", "node-driver"],
        ver="MongoDB Node.js driver 7.7 (return shape since driver v6)", vs=True, status="stable",
        q_en=r"""With the MongoDB Node.js driver (v7), what is logged the **first** time this runs for a phone number that has no cart yet?""",
        q_bn=r"""MongoDB Node.js driver (v7) দিয়ে, যে phone number-এর এখনো কোনো cart নেই, তার জন্য এই code **প্রথমবার** চললে কী log হবে?""",
        code=r"""
            const cart = await db.collection("carts").findOneAndUpdate(
              { phone: "+8801711000000" },
              { $setOnInsert: { createdAt: new Date() }, $inc: { visits: 1 } },
              { upsert: true }
            );
            console.log(cart);
        """,
        lang="javascript",
        options=[
            (r"""The newly inserted cart document, with `visits: 1`""",
             r"""নতুন insert হওয়া cart document, `visits: 1` সহ"""),
            (r"""It throws, because `findOneAndUpdate` doesn't support `upsert`""",
             r"""Error throw করে, কারণ `findOneAndUpdate` `upsert` support করে না"""),
            (r"""An object like `{ value: {...}, ok: 1, lastErrorObject: {...} }`""",
             r"""`{ value: {...}, ok: 1, lastErrorObject: {...} }`-এর মতো একটা object"""),
            (r"""`null`, because by default it returns the document as it was before the update — and there was none""",
             r"""`null`, কারণ default-ভাবে এটা update-এর আগের document return করে — আর আগে কোনো document ছিল না"""),
        ],
        correct=3,
        a_en=r"""`findOneAndUpdate` returns the **pre-update** document by default (`returnDocument: "before"`). On an upsert there was no document before, so it returns `null` even though a cart was inserted. Pass `{ upsert: true, returnDocument: "after" }` to get the new document.""",
        a_bn=r"""`findOneAndUpdate` default-ভাবে **update-এর আগের** document return করে (`returnDocument: "before"`)। Upsert-এর ক্ষেত্রে আগে কোনো document ছিল না, তাই cart insert হলেও `null` return করে। নতুন document পেতে `{ upsert: true, returnDocument: "after" }` দাও।""",
        ex_en=r"""
            Option C is the tempting one if you learned the driver before v6: older drivers returned a `ModifyResult` wrapper (`{ value, ok, lastErrorObject }`). Since driver v6 the method returns the document (or `null`) directly, unless you pass `includeResultMetadata: true`.

            Related points:
            - `$setOnInsert` only applies when the upsert inserts; `$inc` on a missing field starts from 0.
            - Add a **unique index on `phone`** — two concurrent upserts for the same new phone could otherwise race and create duplicates.
            - In mongosh the option can also be written `returnNewDocument: true`; in Mongoose 9 use `returnDocument: "after"` (the old `new: true` is deprecated since 9.2).
        """,
        ex_bn=r"""
            Driver v6-এর আগে শিখে থাকলে option C বিভ্রান্তিকর মনে হবে: পুরনো driver একটা `ModifyResult` wrapper (`{ value, ok, lastErrorObject }`) return করত। Driver v6 থেকে method সরাসরি document (বা `null`) return করে, যদি না তুমি `includeResultMetadata: true` দাও।

            সম্পর্কিত বিষয়:
            - `$setOnInsert` শুধু upsert insert করলেই apply হয়; missing field-এ `$inc` 0 থেকে শুরু হয়।
            - **`phone`-এ unique index** যোগ করো — না হলে একই নতুন phone-এর জন্য দুইটা concurrent upsert race করে duplicate তৈরি করতে পারে।
            - mongosh-এ option-টা `returnNewDocument: true` হিসেবেও লেখা যায়; Mongoose 9-এ `returnDocument: "after"` ব্যবহার করো (পুরনো `new: true` 9.2 থেকে deprecated)।
        """,
        tip_en=r"""Mention the driver-version change in return shape — it's a real migration bug when upgrading old Express projects, and shows you've read release notes.""",
        tip_bn=r"""Return shape-এ driver version অনুযায়ী পরিবর্তনের কথা বলো — পুরনো Express project upgrade করার সময় এটা বাস্তব একটা migration bug, আর এতে বোঝা যায় তুমি release note পড়ো।""",
        follow=[
            ("How would you implement 'get or create' for a user profile safely under concurrency?", "Concurrency-র মধ্যে নিরাপদে user profile-এর 'get or create' কীভাবে implement করবে?"),
        ],
        related=["mongo-004", "mongo-016"],
        refs=[FOAU, NODE_DRIVER],
    ),
    # ------------------------------------------------------------------ mongo-022
    Q(
        id="mongo-022", sub="MongoDB 9.0", diff="medium", type="conceptual",
        prio="medium", market="both", mins=6,
        tags=["mongodb-9", "upgrade", "release-model", "memory-limit", "validation"],
        ver="MongoDB 9.0 (released 2026-09-28)", vs=True, status="version-specific",
        q_en=r"""Your team plans to upgrade from MongoDB 8.0 to 9.0. Which 9.0 changes should an application developer know about, and how does MongoDB's newer release model affect upgrade planning?""",
        q_bn=r"""তোমার team MongoDB 8.0 থেকে 9.0-তে upgrade করার plan করছে। একজন application developer-এর কোন 9.0 পরিবর্তনগুলো জানা দরকার, আর MongoDB-র নতুন release model upgrade planning-এ কী প্রভাব ফেলে?""",
        a_en=r"""
            **Changes that can affect app code:**
            - **Per-operation memory limit:** a single query/aggregation can now use at most the greater of 1 GB or 20% of server memory by default. Heavy reports that worked on 8.0 can fail with `ExceededMemoryLimit` — test them. (The 100 MB per-stage limit and spilling are unchanged.)
            - **`$where`, `$function`, `$accumulator` are un-deprecated** and run on a sandboxed WebAssembly-based JavaScript engine. Still, native operators are faster and index-friendly, so they remain a last resort.
            - **`constraint` validation level:** applies schema validation to all inserts and updates *and* guarantees every document in the collection satisfies the rules.
            - **`maxConcurrentMultiDocumentTransactions`** defaults to 10,000 (`TooManyOpenTransactions` beyond that).
            - Queryable Encryption prefix/suffix/substring queries are GA, and `$queryStats` is on by default (sampled).
            - Known issue: at FCV 9.0, Mongoose's `syncIndexes()` may rebuild unchanged indexes on every start unless Mongoose is ≥ 9.10.4 / 8.24.5.

            **Release model:** from 9.0, minor releases (9.1, 9.2…) ship only on Atlas; self-managed users get the major release plus an annual "Feature Update" (X.5). Majors are supported for 5 years. So self-managed teams plan around 9.0 → 9.5 → next major, while Atlas clusters get features continuously.

            **Plan:** check driver/ODM compatibility (Node driver 7.x, Mongoose 9.10.4+), run tests and heavy aggregations against 9.0 in staging, do a rolling upgrade, keep FCV at 8.0 until stable (so you can still downgrade), then set FCV to 9.0.
        """,
        a_bn=r"""
            **যে পরিবর্তনগুলো app code-এ প্রভাব ফেলতে পারে:**
            - **Per-operation memory limit:** এখন default-ভাবে একটা query/aggregation সর্বোচ্চ 1 GB বা server memory-র 20% — যেটা বড় — ব্যবহার করতে পারে। 8.0-তে চলা ভারী report `ExceededMemoryLimit` দিয়ে fail করতে পারে — test করো। (প্রতি stage-এর 100 MB limit আর spilling অপরিবর্তিত।)
            - **`$where`, `$function`, `$accumulator` আর deprecated নয়**, এগুলো sandboxed WebAssembly-ভিত্তিক JavaScript engine-এ চলে। তবুও native operator দ্রুত আর index-friendly, তাই এগুলো শেষ উপায় হিসেবেই থাকে।
            - **`constraint` validation level:** সব insert আর update-এ schema validation apply করে, *এবং* guarantee দেয় যে collection-এর প্রতিটি document নিয়ম মেনে চলে।
            - **`maxConcurrentMultiDocumentTransactions`**-এর default 10,000 (এর বেশি হলে `TooManyOpenTransactions`)।
            - Queryable Encryption-এর prefix/suffix/substring query GA হয়েছে, আর `$queryStats` default-ভাবে চালু (sampled)।
            - Known issue: FCV 9.0-তে Mongoose ≥ 9.10.4 / 8.24.5 না হলে `syncIndexes()` প্রতিবার start-এ অপরিবর্তিত index-ও rebuild করতে পারে।

            **Release model:** 9.0 থেকে minor release (9.1, 9.2…) শুধু Atlas-এ আসে; self-managed user-রা major release আর বছরে একটা "Feature Update" (X.5) পায়। Major release 5 বছর support পায়। তাই self-managed team 9.0 → 9.5 → পরের major ধরে plan করে, আর Atlas cluster ধারাবাহিকভাবে feature পায়।

            **Plan:** driver/ODM compatibility check করো (Node driver 7.x, Mongoose 9.10.4+), staging-এ 9.0-এর বিরুদ্ধে test আর ভারী aggregation চালাও, rolling upgrade করো, stable না হওয়া পর্যন্ত FCV 8.0-তে রাখো (যাতে downgrade করা যায়), তারপর FCV 9.0 set করো।
        """,
        ex_en=r"""
            - **FCV (featureCompatibilityVersion)** controls which new on-disk features are enabled. Upgrading binaries with FCV still at the old version keeps a downgrade path; raising it (`setFeatureCompatibilityVersion` with `confirm: true`) enables 9.0 features and makes downgrading harder.
            - **Rolling upgrade order:** secondaries first, then step down the primary and upgrade it — the application sees only a short election.
            - **Server-side JavaScript:** "un-deprecated" doesn't mean "recommended". Never build `$where`/`$function` code from user input, and remember they can't use indexes for the JavaScript part. They're also not available on `ppc64le`.
            - **Validation levels:** `moderate` only checks updates to documents that were already valid; `strict` checks all inserts and updates; `constraint` (new) additionally guarantees the whole collection is valid.
            - Always read the release notes' compatibility and known-issues sections before scheduling the upgrade.
        """,
        ex_bn=r"""
            - **FCV (featureCompatibilityVersion)** ঠিক করে কোন নতুন on-disk feature চালু থাকবে। Binary upgrade করে FCV পুরনো version-এ রাখলে downgrade-এর পথ খোলা থাকে; FCV বাড়ালে (`confirm: true` সহ `setFeatureCompatibilityVersion`) 9.0-এর feature চালু হয় আর downgrade কঠিন হয়ে যায়।
            - **Rolling upgrade-এর ক্রম:** আগে secondary, তারপর primary-কে step down করে upgrade — application শুধু একটা ছোট election দেখে।
            - **Server-side JavaScript:** "আর deprecated নয়" মানে "recommended" না। কখনো user input থেকে `$where`/`$function` code বানিও না, আর মনে রেখো JavaScript অংশের জন্য এগুলো index ব্যবহার করতে পারে না। `ppc64le`-এ এগুলো available-ও না।
            - **Validation level:** `moderate` শুধু আগে থেকে valid document-এর update check করে; `strict` সব insert আর update check করে; `constraint` (নতুন) এর ওপর পুরো collection valid থাকার guarantee দেয়।
            - Upgrade schedule করার আগে সবসময় release note-এর compatibility আর known-issues অংশ পড়ো।
        """,
        tip_en=r"""Prioritise: lead with the change most likely to break production (the per-operation memory limit), then the process (staging tests, rolling upgrade, FCV). Listing features without impact sounds like reciting a changelog.""",
        tip_bn=r"""অগ্রাধিকার দাও: production ভাঙার সবচেয়ে বেশি সম্ভাবনা যে পরিবর্তনের (per-operation memory limit) সেটা দিয়ে শুরু করো, তারপর process (staging test, rolling upgrade, FCV)। প্রভাব না বলে শুধু feature-এর তালিকা দিলে changelog মুখস্থ বলার মতো শোনায়।""",
        mist_en=r"""Assuming self-managed deployments get 9.1/9.2 minor releases; raising FCV immediately after swapping binaries; treating the un-deprecation of `$where` as permission to use it widely.""",
        mist_bn=r"""ধরে নেওয়া যে self-managed deployment 9.1/9.2 minor release পাবে; binary বদলানোর সাথে সাথেই FCV বাড়িয়ে দেওয়া; `$where` আর deprecated নয় বলে সেটা ব্যাপকভাবে ব্যবহারের অনুমতি মনে করা।""",
        code=r"""
            // After all members run 9.0 binaries and the app is verified:
            db.adminCommand({ getParameter: 1, featureCompatibilityVersion: 1 })
            db.adminCommand({ setFeatureCompatibilityVersion: "9.0", confirm: true })

            // New in 9.0: guarantee every document matches the validator
            db.runCommand({
              collMod: "orders",
              validator: { $jsonSchema: { required: ["customerId", "items", "status"] } },
              validationLevel: "constraint"
            })
        """,
        lang="javascript",
        follow=[
            ("What would you do if a monthly report starts failing with ExceededMemoryLimit after the upgrade?", "Upgrade-এর পর একটা monthly report ExceededMemoryLimit দিয়ে fail করা শুরু করলে কী করবে?"),
            ("Why keep the FCV at the old version for a while after upgrading binaries?", "Binary upgrade-এর পর কিছুদিন FCV পুরনো version-এ রাখার কারণ কী?"),
        ],
        related=["mongo-024", "mongo-018"],
        refs=[RN_90, VERSIONS, VALIDATION],
    ),
    # ------------------------------------------------------------------ mongo-027
    Q(
        id="mongo-027", sub="Transactions & Atomicity", diff="hard", type="coding",
        prio="high", market="both", mins=12,
        tags=["transactions", "withtransaction", "node-driver", "retry", "idempotency"],
        ver="MongoDB Node.js driver 7.7 (withTransaction returns the callback value since v6); MongoDB 9.0 replica set", vs=True, status="stable",
        q_en=r"""Write `transferCredits(fromId, toId, amount, requestId)` with the MongoDB Node.js driver. It must move wallet credits atomically between two users, fail without changing anything if the sender's balance is too low, write one ledger entry, retry safely on transient errors, and not apply the same `requestId` twice.

Example: Rahim has 500 and Karim has 100. Transferring 200 → Rahim 300, Karim 300, one ledger document. Transferring 1,000 → throws "Insufficient balance", nothing changes.""",
        q_bn=r"""MongoDB Node.js driver দিয়ে `transferCredits(fromId, toId, amount, requestId)` লেখো। এটা দুইজন user-এর wallet-এর মধ্যে atomically credit সরাবে, sender-এর balance কম থাকলে কিছু না বদলে fail করবে, একটা ledger entry লিখবে, transient error-এ নিরাপদে retry করবে, আর একই `requestId` দুইবার apply করবে না।

উদাহরণ: Rahim-এর 500, Karim-এর 100। 200 transfer করলে → Rahim 300, Karim 300, একটা ledger document। 1,000 transfer করলে → "Insufficient balance" throw করবে, কিছুই বদলাবে না।""",
        code=r"""
            import { MongoClient } from "mongodb";

            const client = new MongoClient(process.env.MONGODB_URI); // replica set / Atlas
            const db = client.db("wallet");
            const wallets = db.collection("wallets");
            const ledger = db.collection("ledger");

            // Run once at deploy time: makes each requestId usable only once
            await ledger.createIndex({ requestId: 1 }, { unique: true });

            export async function transferCredits(fromId, toId, amount, requestId) {
              if (!Number.isInteger(amount) || amount <= 0) throw new Error("Invalid amount");
              if (fromId === toId) throw new Error("Cannot transfer to the same wallet");

              const session = client.startSession();
              try {
                // Starts, commits, aborts on throw, and retries the callback on
                // TransientTransactionError / UnknownTransactionCommitResult.
                return await session.withTransaction(
                  async () => {
                    const debit = await wallets.updateOne(
                      { _id: fromId, balance: { $gte: amount } },
                      { $inc: { balance: -amount } },
                      { session }
                    );
                    if (debit.matchedCount === 0) throw new Error("Insufficient balance");

                    const credit = await wallets.updateOne(
                      { _id: toId },
                      { $inc: { balance: amount } },
                      { session }
                    );
                    if (credit.matchedCount === 0) throw new Error("Receiver wallet not found");

                    // Duplicate requestId → E11000 → whole transaction aborts
                    await ledger.insertOne(
                      { requestId, fromId, toId, amount, createdAt: new Date() },
                      { session }
                    );
                    return { ok: true, requestId };
                  },
                  { readConcern: { level: "snapshot" }, writeConcern: { w: "majority" } }
                );
              } catch (err) {
                if (err?.code === 11000) return { ok: true, requestId, duplicate: true };
                throw err;
              } finally {
                await session.endSession();
              }
            }
        """,
        lang="javascript",
        time="O(log n) per transfer (three indexed single-document writes)",
        space="O(1)",
        a_en=r"""
            The core ideas:

            - **Conditional debit:** `{ _id: fromId, balance: { $gte: amount } }` + `$inc` checks and debits in one atomic step. If `matchedCount` is 0, the balance was too low, so I throw — `withTransaction` aborts and nothing is written.
            - **Transaction for the multi-document invariant:** debit, credit and ledger entry commit together or not at all. Every operation gets `{ session }` — an operation without it runs outside the transaction.
            - **Retries:** `withTransaction()` retries the whole callback on transient errors (e.g. a `WriteConflict` when two transfers touch the same wallet, or a primary election) and retries the commit on `UnknownTransactionCommitResult`. So the callback must be safe to re-run: only database work inside, no SMS or payment API calls.
            - **Idempotency:** a unique index on `ledger.requestId`. If the client retries the HTTP request, the duplicate insert fails with E11000, the transaction aborts, and I report "already processed" instead of moving money twice.
            - Amounts are integers (poisha) to avoid floating-point errors.
        """,
        a_bn=r"""
            মূল ধারণাগুলো:

            - **Conditional debit:** `{ _id: fromId, balance: { $gte: amount } }` + `$inc` এক atomic ধাপে check আর debit দুটোই করে। `matchedCount` 0 হলে balance কম ছিল, তাই throw করি — `withTransaction` abort করে আর কিছুই লেখা হয় না।
            - **Multi-document invariant-এর জন্য transaction:** debit, credit আর ledger entry হয় একসাথে commit হবে, নয়তো কিছুই না। প্রতিটি operation-এ `{ session }` দিতে হয় — না দিলে সেই operation transaction-এর বাইরে চলে।
            - **Retry:** `withTransaction()` transient error-এ (যেমন দুইটা transfer একই wallet ছুঁলে `WriteConflict`, বা primary election) পুরো callback আবার চালায়, আর `UnknownTransactionCommitResult`-এ commit retry করে। তাই callback বারবার চালানো নিরাপদ হতে হবে: ভেতরে শুধু database-এর কাজ, কোনো SMS বা payment API call না।
            - **Idempotency:** `ledger.requestId`-এ unique index। Client HTTP request retry করলে duplicate insert E11000 দিয়ে fail করে, transaction abort হয়, আর আমি দুইবার টাকা না সরিয়ে "already processed" জানাই।
            - Floating-point error এড়াতে amount integer (পয়সা) হিসেবে রাখা।
        """,
        ex_en=r"""
            - **Edge cases:** zero/negative/non-integer amounts, self-transfer, missing receiver (throwing after the debit is fine — the abort undoes it), and the duplicate `requestId`.
            - **Concurrency:** MongoDB doesn't use lock-wait deadlocks for this; conflicting transactions get a `WriteConflict` and one is retried. Hot wallets (e.g. a merchant receiving thousands of payments) can see many retries — batching or a per-merchant ledger with periodic settlement helps.
            - **Without a transaction?** You could write a "pending transfer" document and apply debit/credit with idempotent steps (a two-phase pattern), but it's more code and needs recovery logic. With replica sets, transactions are simpler and correct.
            - **Read concern `snapshot`** makes reads inside the transaction consistent; `w: "majority"` on commit makes the result durable across failover.
            - **Testing:** run against a single-node replica set (`mongod --replSet rs0` + `rs.initiate()`) — a standalone server rejects transactions.
        """,
        ex_bn=r"""
            - **Edge case:** শূন্য/negative/non-integer amount, নিজের wallet-এ transfer, receiver না থাকা (debit-এর পরে throw করা ঠিক আছে — abort সেটা ফিরিয়ে দেয়), আর duplicate `requestId`।
            - **Concurrency:** MongoDB এখানে lock-wait deadlock ব্যবহার করে না; conflicting transaction `WriteConflict` পায় আর একটা retry হয়। Hot wallet-এ (যেমন হাজার হাজার payment পাওয়া একজন merchant) অনেক retry হতে পারে — batching বা periodic settlement সহ per-merchant ledger সাহায্য করে।
            - **Transaction ছাড়া?** একটা "pending transfer" document লিখে idempotent ধাপে debit/credit apply করা যায় (two-phase pattern), কিন্তু তাতে code বেশি আর recovery logic লাগে। Replica set থাকলে transaction সহজ আর সঠিক।
            - **Read concern `snapshot`** transaction-এর ভেতরের read consistent রাখে; commit-এ `w: "majority"` failover-এর পরেও result durable রাখে।
            - **Testing:** single-node replica set-এর বিরুদ্ধে চালাও (`mongod --replSet rs0` + `rs.initiate()`) — standalone server transaction reject করে।
        """,
        tip_en=r"""Say out loud why the callback must be side-effect-free ("it can run more than once") — that single insight is what separates people who've used transactions in production from those who've only read about them.""",
        tip_bn=r"""জোরে বলো কেন callback side-effect-free হতে হবে ("এটা একাধিকবার চলতে পারে") — এই একটা কথাই আলাদা করে দেয় কে production-এ transaction ব্যবহার করেছে আর কে শুধু পড়েছে।""",
        mist_en=r"""Reading the balance with `findOne` and then updating (race condition); forgetting `{ session }` on one operation; sending the SMS inside the callback; catching the error inside the callback so the transaction commits anyway.""",
        mist_bn=r"""`findOne` দিয়ে balance পড়ে তারপর update করা (race condition); কোনো একটা operation-এ `{ session }` ভুলে যাওয়া; callback-এর ভেতরে SMS পাঠানো; callback-এর ভেতরেই error catch করে ফেলা, ফলে transaction তবুও commit হয়ে যায়।""",
        follow=[
            ("How would you notify both users by SMS without risking duplicate messages?", "Duplicate message-এর ঝুঁকি ছাড়া দুইজন user-কেই SMS দিয়ে কীভাবে জানাবে?"),
            ("How would this design change if wallets lived on different shards?", "Wallet-গুলো ভিন্ন shard-এ থাকলে এই design কীভাবে বদলাবে?"),
        ],
        related=["mongo-018", "mongo-031"],
        refs=[NODE_TXN, TXN, TXN_PROD],
    ),
    # ------------------------------------------------------------------ mongo-028
    Q(
        id="mongo-028", sub="Security", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["security", "nosql-injection", "authentication", "rbac", "tls", "hardening"],
        ver="Version-independent concept (current: MongoDB 9.0, Express 5, zod 4)", vs=False, status="stable",
        q_en=r"""
            You're reviewing a login API and its deployment:

            - The Express route runs `db.collection("users").findOne({ email: req.body.email, password: req.body.password })` and issues a JWT if a user is found.
            - `mongod` runs on a VPS with `net.bindIp: 0.0.0.0`, port 27017 open to the internet, and authorization disabled.
            - The app connects as a user with the `root` role.

            What security problems do you see, and how would you harden both the code and the MongoDB deployment?
        """,
        q_bn=r"""
            তুমি একটা login API আর তার deployment review করছ:

            - Express route-টা `db.collection("users").findOne({ email: req.body.email, password: req.body.password })` চালায়, আর user পাওয়া গেলে একটা JWT দেয়।
            - `mongod` একটা VPS-এ চলে, `net.bindIp: 0.0.0.0`, port 27017 internet-এ খোলা, আর authorization বন্ধ।
            - App `root` role-ওয়ালা একটা user হিসেবে connect করে।

            কী কী security সমস্যা দেখছ, আর code ও MongoDB deployment — দুটোকেই কীভাবে harden করবে?
        """,
        code=r"""
            app.post("/api/login", async (req, res) => {
              const { email, password } = req.body;
              const user = await db.collection("users").findOne({ email, password });
              if (!user) return res.status(401).json({ error: "Invalid credentials" });
              res.json({ token: issueJwt(user) });
            });

            // Deployment notes:
            // - mongod runs on a VPS with net.bindIp 0.0.0.0, port 27017 open, authorization disabled
            // - the app connects as a user with the "root" role
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Fixed endpoint", label_bn="সংশোধিত endpoint", src=r"""
                import { z } from "zod";
                import bcrypt from "bcrypt";

                const LoginBody = z.object({
                  email: z.email().max(254),
                  password: z.string().min(8).max(128),
                });

                app.post("/api/login", loginRateLimiter, async (req, res) => {
                  const parsed = LoginBody.safeParse(req.body);
                  if (!parsed.success) return res.status(400).json({ error: "Invalid input" });
                  const { email, password } = parsed.data;          // guaranteed strings

                  const user = await db.collection("users").findOne(
                    { email: email.toLowerCase() },
                    { projection: { passwordHash: 1, role: 1 } }
                  );
                  const ok = user && (await bcrypt.compare(password, user.passwordHash));
                  if (!ok) return res.status(401).json({ error: "Invalid credentials" });

                  res.json({ token: issueJwt(user) });
                });
            """),
            dict(lang="yaml", label_en="mongod.conf hardening (self-managed)", label_bn="mongod.conf hardening (self-managed)", src=r"""
                net:
                  port: 27017
                  bindIp: 127.0.0.1,10.0.1.12        # private interface only, never 0.0.0.0 on a public host
                  tls:
                    mode: requireTLS
                    certificateKeyFile: /etc/ssl/mongodb.pem
                security:
                  authorization: enabled
            """),
            dict(lang="javascript", label_en="Least-privilege application user (mongosh)", label_bn="Least-privilege application user (mongosh)", src=r"""
                use shop
                db.createUser({
                  user: "shop_api",
                  pwd: passwordPrompt(),
                  roles: [{ role: "readWrite", db: "shop" }]
                })
            """),
        ],
        a_en=r"""
            **Code problems:**
            1. **NoSQL operator injection.** `req.body` is parsed JSON, so an attacker can send `{ "email": "admin@shop.com", "password": { "$ne": null } }`. The filter becomes "password not equal to null", which matches — **login bypass** without knowing the password.
            2. **Plain-text passwords** are stored and compared in the query. Store a slow hash (bcrypt/argon2), fetch the user by email only, and compare the hash in the app.
            3. No input validation or rate limiting → brute force and credential stuffing.

            **Fix in code:** validate types with a schema (zod) so `email` and `password` are guaranteed strings; query only by a normalised email; compare with `bcrypt.compare`; return the same generic error for every failure; rate-limit the route. With Mongoose, `sanitizeFilter` adds another layer.

            **Deployment problems:** a public `0.0.0.0:27017` with no auth is exactly what automated scanners find — databases like this get dumped and replaced with ransom notes. And a `root` app user turns any bug into full-cluster compromise.

            **Hardening:** enable authentication (SCRAM) and **RBAC** with a least-privilege role per service (`readWrite` on one DB); bind to private interfaces and firewall/VPC-restrict the port; **TLS** for all connections; encryption at rest; secrets in a secret manager, not in the repo; auditing; keep MongoDB patched (9.0.1 included a security fix); and tested backups.
        """,
        a_bn=r"""
            **Code-এর সমস্যা:**
            1. **NoSQL operator injection।** `req.body` হলো parsed JSON, তাই attacker পাঠাতে পারে `{ "email": "admin@shop.com", "password": { "$ne": null } }`। তখন filter হয়ে যায় "password null-এর সমান না", যেটা match করে — password না জেনেই **login bypass**।
            2. **Plain-text password** store করে query-তেই compare করা হচ্ছে। ধীর hash (bcrypt/argon2) store করো, শুধু email দিয়ে user আনো, আর app-এ hash compare করো।
            3. কোনো input validation বা rate limiting নেই → brute force আর credential stuffing।

            **Code-এ fix:** schema (zod) দিয়ে type validate করো, যাতে `email` আর `password` নিশ্চিতভাবে string হয়; শুধু normalised email দিয়ে query করো; `bcrypt.compare` দিয়ে মেলাও; সব failure-এ একই generic error দাও; route-এ rate limit দাও। Mongoose হলে `sanitizeFilter` আরেকটা স্তর যোগ করে।

            **Deployment-এর সমস্যা:** auth ছাড়া public `0.0.0.0:27017` ঠিক সেটাই, যা automated scanner খুঁজে বেড়ায় — এমন database dump হয়ে ransom note দিয়ে replace হয়ে যায়। আর `root` app user থাকলে যেকোনো bug পুরো cluster compromise-এ পরিণত হয়।

            **Hardening:** authentication (SCRAM) আর প্রতিটি service-এর জন্য least-privilege role সহ **RBAC** চালু করো (একটা DB-তে `readWrite`); private interface-এ bind করো আর firewall/VPC দিয়ে port সীমিত করো; সব connection-এ **TLS**; encryption at rest; secret repo-তে না রেখে secret manager-এ; auditing; MongoDB patch করা রাখো (9.0.1-এ একটা security fix ছিল); আর test করা backup।
        """,
        ex_en=r"""
            - **Where injection comes from:** any place user-controlled objects reach a filter — `req.body`, and `req.query` when a parser builds nested objects (`?email[$ne]=x`). Express 5's default `'simple'` query parser doesn't build nested objects, but don't rely on that; validate everything.
            - **Server-side JavaScript:** never build `$where`, `$function` or `$accumulator` code from user input — that's code injection, not just operator injection.
            - **Mass assignment:** `insertOne(req.body)` lets users set `role: "admin"`; whitelist fields.
            - **Timing/enumeration:** returning early when the user doesn't exist makes responses faster for unknown emails; comparing against a dummy hash in that case evens it out.
            - **Atlas:** IP access lists / private endpoints, database users with scoped roles and enforced TLS are the managed equivalents of the self-managed settings.
            - **Performance angle:** an index on `email` (unique) keeps login a single index lookup; bcrypt cost should be tuned (it's intentionally slow) and protected by rate limiting so it can't be used for CPU exhaustion.
        """,
        ex_bn=r"""
            - **Injection কোথা থেকে আসে:** যেখানেই user-controlled object filter-এ পৌঁছায় — `req.body`, আর parser nested object বানালে `req.query` (`?email[$ne]=x`)। Express 5-এর default `'simple'` query parser nested object বানায় না, কিন্তু এর ওপর ভরসা কোরো না; সব validate করো।
            - **Server-side JavaScript:** কখনো user input থেকে `$where`, `$function` বা `$accumulator` code বানিও না — এটা শুধু operator injection না, code injection।
            - **Mass assignment:** `insertOne(req.body)` দিলে user `role: "admin"` set করতে পারে; field whitelist করো।
            - **Timing/enumeration:** user না থাকলে আগেভাগে return করলে অজানা email-এর response দ্রুত আসে; সেক্ষেত্রে একটা dummy hash-এর সাথে compare করলে সময় সমান হয়।
            - **Atlas:** IP access list / private endpoint, scoped role সহ database user আর enforced TLS — এগুলোই self-managed setting-এর managed সমতুল্য।
            - **Performance দিক:** `email`-এ (unique) index থাকলে login একটা index lookup-এই হয়; bcrypt-এর cost tune করতে হয় (এটা ইচ্ছাকৃতভাবে ধীর) আর rate limiting দিয়ে রক্ষা করতে হয়, যাতে এটা CPU exhaustion-এ ব্যবহার না হয়।
        """,
        tip_en=r"""Demonstrate the exploit payload concretely, then split the fix into code / database / network layers. Interviewers look for defence in depth, not a single "use an ORM" answer.""",
        tip_bn=r"""Exploit payload-টা concrete ভাবে দেখাও, তারপর fix-কে code / database / network — এই স্তরে ভাগ করো। Interviewer defence in depth খোঁজে, শুধু "ORM ব্যবহার করো" ধরনের একটা উত্তর না।""",
        mist_en=r"""Believing MongoDB is immune to injection because it "doesn't use SQL"; relying on Mongoose alone without validating types; fixing the code but leaving port 27017 open to the internet.""",
        mist_bn=r"""MongoDB "SQL ব্যবহার করে না" বলে injection থেকে নিরাপদ মনে করা; type validate না করে শুধু Mongoose-এর ওপর নির্ভর করা; code ঠিক করে port 27017 internet-এ খোলা রেখে দেওয়া।""",
        follow=[
            ("How would you detect that someone already exploited this bypass?", "কেউ আগেই এই bypass exploit করেছে কি না, কীভাবে বুঝবে?"),
            ("What roles would you give to the API, a reporting job and a backup job?", "API, একটা reporting job আর একটা backup job-কে কোন কোন role দেবে?"),
        ],
        related=["mongo-006", "mongo-022"],
        refs=[SEC_CHECKLIST, RBAC, OWASP_NOSQL],
    ),
    # ------------------------------------------------------------------ mongo-029
    Q(
        id="mongo-029", sub="Schema Design Patterns", diff="hard", type="architecture",
        prio="high", market="both", mins=12,
        tags=["schema-design", "unbounded-arrays", "outlier-pattern", "computed-pattern", "bucket-pattern", "social-app"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""A social app stores `followers: [userId]` inside each user document and `likes: [userId]` inside each post. It worked in beta, but now a few celebrity accounts have millions of followers: profile loads are slow and some follow requests fail. Explain what's wrong and redesign the schema using appropriate patterns.""",
        q_bn=r"""একটা social app প্রতিটি user document-এর ভেতরে `followers: [userId]` আর প্রতিটি post-এর ভেতরে `likes: [userId]` রাখে। Beta-তে ঠিক ছিল, কিন্তু এখন কয়েকটা celebrity account-এর লক্ষ লক্ষ follower: profile load slow, আর কিছু follow request fail করছে। সমস্যা কী ব্যাখ্যা করো, আর উপযুক্ত pattern ব্যবহার করে schema আবার design করো।""",
        a_en=r"""
            **What's wrong — the unbounded array anti-pattern:**
            - Each array element costs roughly 15–20 bytes in BSON, so ~1 million followers pushes a user document toward the **16 MB limit** — follows then fail outright.
            - Every `$addToSet` rewrites and replicates a huge document; a multikey index on `followers` grows with every element; reading a profile drags the whole array over the wire unless projected away.
            - One celebrity document becomes a write hotspot.

            **Redesign:**
            - **Edges in their own collection:** `follows { followerId, followeeId, createdAt }` with a unique index `{ followerId: 1, followeeId: 1 }` and `{ followeeId: 1, createdAt: -1 }` for "followers list" pages. This scales to any number of followers (one-to-squillions).
            - **Computed pattern:** keep `followerCount` / `followingCount` on users and `likeCount` on posts, maintained with `$inc` when an edge is inserted — never `countDocuments` over millions on each profile view.
            - **Outlier pattern:** most posts have few likes, so a post keeps a small embedded `recentLikers` preview (bounded with `$push` + `$slice`). The full like list lives in a `likes` collection (unique `{ postId, userId }`); only viral posts really need it, but the code path is the same.
            - **Bucket pattern** for high-volume small events (profile views, activity): group them per user per hour/day into one document with a count and a capped array, or use a time series collection.

            **Migration:** backfill edges from the arrays in a background job, dual-write during the transition, switch reads, then `$unset` the old arrays.
        """,
        a_bn=r"""
            **সমস্যা — unbounded array anti-pattern:**
            - BSON-এ প্রতিটি array element-এ মোটামুটি 15–20 byte লাগে, তাই ~10 লাখ follower হলে user document **16 MB limit**-এর দিকে চলে যায় — তখন follow সরাসরি fail করে।
            - প্রতিটি `$addToSet` একটা বিশাল document rewrite আর replicate করে; `followers`-এর multikey index প্রতিটি element-এর সাথে বড় হয়; project করে বাদ না দিলে profile পড়তেই পুরো array network-এ আসে।
            - একটা celebrity document write hotspot হয়ে যায়।

            **নতুন design:**
            - **Edge আলাদা collection-এ:** `follows { followerId, followeeId, createdAt }`, unique index `{ followerId: 1, followeeId: 1 }` আর "followers list" page-এর জন্য `{ followeeId: 1, createdAt: -1 }`। Follower যত বেশিই হোক scale করে (one-to-squillions)।
            - **Computed pattern:** user-এ `followerCount` / `followingCount` আর post-এ `likeCount` রাখো, edge insert হলে `$inc` দিয়ে update করো — প্রতিটি profile view-এ লক্ষ লক্ষ document-এর ওপর `countDocuments` কখনো না।
            - **Outlier pattern:** বেশিরভাগ post-এ like কম, তাই post-এ ছোট একটা embedded `recentLikers` preview রাখো (`$push` + `$slice` দিয়ে bounded)। পুরো like list থাকে `likes` collection-এ (unique `{ postId, userId }`); আসলে শুধু viral post-এর এটা দরকার, কিন্তু code path একই।
            - বেশি পরিমাণ ছোট event-এর (profile view, activity) জন্য **bucket pattern**: প্রতি user-এর প্রতি ঘণ্টা/দিনের event একটা document-এ count আর capped array সহ group করো, অথবা time series collection ব্যবহার করো।

            **Migration:** background job দিয়ে array থেকে edge backfill করো, transition-এর সময় dual-write করো, read switch করো, তারপর পুরনো array `$unset` করো।
        """,
        ex_en=r"""
            - **Counter consistency:** insert the edge first (the unique index rejects double-follows/likes) and only `$inc` if the insert succeeded. Update counters in the same transaction, or asynchronously via a queue/change stream and accept brief drift; a periodic job can reconcile.
            - **Hot counters:** a celebrity post can receive thousands of likes per second on one document. Options: buffer increments in Redis and flush periodically, or split the counter into N sub-documents and sum them when reading.
            - **Feeds:** fan-out on write (push post IDs into followers' feeds) is cheap to read but explodes for celebrities; a hybrid uses fan-out on write for normal accounts and fan-out on read for very large ones.
            - **Pattern names:** MongoDB's docs now group these under "Handle Computed Values" and "Group Data" (bucket/outlier); the classic names are still what interviewers use.
            - **Rule of thumb:** if an array can grow without a business limit, it doesn't belong inside the parent document.
        """,
        ex_bn=r"""
            - **Counter consistency:** আগে edge insert করো (unique index দুইবার follow/like reject করে), আর insert সফল হলেই কেবল `$inc` করো। Counter একই transaction-এ, অথবা queue/change stream দিয়ে asynchronously update করো আর সামান্য সময়ের drift মেনে নাও; একটা periodic job reconcile করতে পারে।
            - **Hot counter:** celebrity-র একটা post-এ এক document-এ প্রতি second হাজার হাজার like আসতে পারে। উপায়: Redis-এ increment জমিয়ে periodically flush করা, অথবা counter-কে Nটা sub-document-এ ভাগ করে read-এর সময় যোগ করা।
            - **Feed:** fan-out on write (follower-দের feed-এ post ID push করা) read-এ সস্তা কিন্তু celebrity-র জন্য বিস্ফোরিত হয়; hybrid পদ্ধতিতে সাধারণ account-এ fan-out on write আর খুব বড় account-এ fan-out on read।
            - **Pattern-এর নাম:** MongoDB docs এখন এগুলো "Handle Computed Values" আর "Group Data" (bucket/outlier)-এর অধীনে রাখে; interviewer-রা তবুও classic নামগুলোই ব্যবহার করে।
            - **মূল নিয়ম:** কোনো array যদি business limit ছাড়া বাড়তে পারে, তাহলে সেটা parent document-এর ভেতরে থাকার যোগ্য না।
        """,
        tip_en=r"""Quantify the problem (bytes per element × followers vs 16 MB) before redesigning — numbers make the diagnosis convincing. Then name each pattern and the exact problem it solves.""",
        tip_bn=r"""Redesign-এর আগে সমস্যাটা সংখ্যা দিয়ে দেখাও (প্রতি element-এর byte × follower বনাম 16 MB) — সংখ্যা থাকলে diagnosis বিশ্বাসযোগ্য হয়। তারপর প্রতিটি pattern-এর নাম আর সেটা ঠিক কোন সমস্যার সমাধান করে তা বলো।""",
        mist_en=r""""Fixing" it with GridFS or by splitting the array into `followers2`, `followers3` fields; counting followers with `countDocuments` on every profile view; incrementing counters even when the like already existed.""",
        mist_bn=r"""GridFS দিয়ে বা array-কে `followers2`, `followers3` field-এ ভাগ করে "fix" করা; প্রতিটি profile view-এ `countDocuments` দিয়ে follower গোনা; like আগে থেকে থাকলেও counter বাড়ানো।""",
        code=r"""
            // One document per follow edge
            db.follows.createIndex({ followerId: 1, followeeId: 1 }, { unique: true })
            db.follows.createIndex({ followeeId: 1, createdAt: -1 })

            // Follow: insert the edge first; only then maintain the computed counters
            db.follows.insertOne({ followerId: me, followeeId: star, createdAt: new Date() })
            db.users.updateOne({ _id: star }, { $inc: { followerCount: 1 } })
            db.users.updateOne({ _id: me },   { $inc: { followingCount: 1 } })

            // Like: full list in its own collection, small preview on the post
            db.likes.createIndex({ postId: 1, userId: 1 }, { unique: true })
            db.likes.insertOne({ postId, userId: me, createdAt: new Date() })
            db.posts.updateOne(
              { _id: postId },
              {
                $inc: { likeCount: 1 },
                $push: { recentLikers: { $each: [{ userId: me, at: new Date() }], $slice: -20 } }
              }
            )
        """,
        lang="javascript",
        follow=[
            ("How would you show 'followed by 3 people you know' on a profile?", "Profile-এ 'তোমার চেনা 3 জন follow করে' কীভাবে দেখাবে?"),
            ("Would you shard the `follows` collection? On which key?", "`follows` collection কি shard করবে? কোন key দিয়ে?"),
        ],
        related=["mongo-009", "mongo-030"],
        refs=[PATTERNS, GROUP_DATA, COMPUTED],
    ),
]

if __name__ == "__main__":
    save("mongodb", "b4", QUESTIONS)
