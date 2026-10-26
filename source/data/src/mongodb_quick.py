# MongoDB — quick-recall questions (mongo-q01..mongo-q10)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

INTRO = ("MongoDB Manual — Introduction to MongoDB", "https://www.mongodb.com/docs/manual/introduction/")
DOC = ("MongoDB Manual — Documents", "https://www.mongodb.com/docs/manual/core/document/")
UPDATE_ONE = ("MongoDB Manual — db.collection.updateOne()", "https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/")
REPLACE_ONE = ("MongoDB Manual — db.collection.replaceOne()", "https://www.mongodb.com/docs/manual/reference/method/db.collection.replaceOne/")
FIND = ("MongoDB Manual — db.collection.find()", "https://www.mongodb.com/docs/manual/reference/method/db.collection.find/")
AGG = ("MongoDB Manual — Aggregation Operations", "https://www.mongodb.com/docs/manual/aggregation/")
EXPLAIN = ("MongoDB Manual — Explain Results", "https://www.mongodb.com/docs/manual/reference/explain-results/")
POS_FILTERED = ("MongoDB Manual — $[<identifier>] (filtered positional operator)", "https://www.mongodb.com/docs/manual/reference/operator/update/positional-filtered/")
CHANGE_STREAMS = ("MongoDB Manual — Change Streams", "https://www.mongodb.com/docs/manual/changestreams/")
SCHEMA_VALIDATION = ("MongoDB Manual — Schema Validation", "https://www.mongodb.com/docs/manual/core/schema-validation/")

QUESTIONS = [
    # ------------------------------------------------------------------ mongo-q01
    Q(
        id="mongo-q01", sub="Documents & Collections", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["sql-vs-nosql", "document-database", "basics"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""What is the difference between SQL and NoSQL databases, and when would you choose MongoDB?""",
        q_bn=r"""SQL আর NoSQL database-এর পার্থক্য কী, আর কখন তুমি MongoDB বেছে নেবে?""",
        a_en=r"""SQL databases store data in tables with a fixed schema and combine tables with joins; NoSQL is a family of other models (document, key-value, wide-column, graph). MongoDB is a document database: it stores flexible, JSON-like documents, so data that is read together can live together. I choose it when the data is naturally nested and evolving; for highly relational data with many joins, a SQL database fits better.""",
        a_bn=r"""SQL database data রাখে fixed schema-র table-এ আর join দিয়ে table মেলায়; NoSQL হলো অন্য কয়েক ধরনের model-এর একটা পরিবার (document, key-value, wide-column, graph)। MongoDB একটা document database: flexible, JSON-এর মতো document রাখে, তাই যে data একসাথে read হয় সেটা একসাথেই রাখা যায়। Data স্বাভাবিকভাবে nested আর পরিবর্তনশীল হলে আমি MongoDB নিই; অনেক join-ওয়ালা relational data-র জন্য SQL database বেশি মানানসই।""",
        ex_en=r"""Don't repeat old myths: MongoDB has indexes, joins (`$lookup`) and multi-document ACID transactions, and a SQL database can store JSON too. The real difference is the data model and how you design for your access patterns.""",
        ex_bn=r"""পুরনো ভুল ধারণা বলবে না: MongoDB-তে index, join (`$lookup`) আর multi-document ACID transaction আছে, আর SQL database-ও JSON রাখতে পারে। আসল পার্থক্য data model-এ, আর access pattern অনুযায়ী কীভাবে design করছ তাতে।""",
        tip_en=r"""Give one example for each side, such as a product catalogue with varying attributes for MongoDB and double-entry accounting for SQL.""",
        tip_bn=r"""দুই দিকেরই একটা করে উদাহরণ দাও, যেমন ভিন্ন ভিন্ন attribute-ওয়ালা product catalogue-এর জন্য MongoDB আর double-entry accounting-এর জন্য SQL।""",
        follow=[
            ("Does MongoDB support transactions?", "MongoDB কি transaction support করে?"),
            ("What does \"flexible schema\" mean in practice?", "বাস্তবে \"flexible schema\" মানে কী?"),
        ],
        related=["mongo-001", "mongo-009"],
        refs=[INTRO],
    ),
    # ------------------------------------------------------------------ mongo-q02
    Q(
        id="mongo-q02", sub="Documents & Collections", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["_id", "objectid", "primary-key"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""What is the `_id` field in MongoDB? Can you set it yourself?""",
        q_bn=r"""MongoDB-তে `_id` field কী? এটা কি নিজে set করা যায়?""",
        a_en=r"""`_id` is the primary key every document must have: it is unique within the collection and always indexed. If you don't provide one, the driver adds an `ObjectId`. You can set your own value (a string, number or UUID, but not an array), but it must be unique and can't be changed after insert.""",
        a_bn=r"""`_id` হলো primary key, যেটা প্রতিটি document-এ থাকতেই হবে: collection-এর ভেতরে unique, আর সবসময় index করা থাকে। তুমি না দিলে driver একটা `ObjectId` বসিয়ে দেয়। নিজের value-ও দেওয়া যায় (string, number বা UUID, তবে array না), কিন্তু সেটা unique হতে হবে আর insert-এর পর বদলানো যায় না।""",
        code=r"""
            db.users.insertOne({ _id: "rafi@example.com", name: "Rafi" })   // → insertedId: 'rafi@example.com'
            db.users.insertOne({ _id: "rafi@example.com", name: "Rafi 2" }) // → E11000 duplicate key error
            db.users.insertOne({ name: "Mitu" })                            // → insertedId: ObjectId('...')
            db.users.updateOne({ name: "Mitu" }, { $set: { _id: 5 } })
            // → error: ... would modify the immutable field '_id'
        """,
        lang="javascript",
        ex_en=r"""To "change" an `_id` you insert a copy with the new value and delete the old document. A natural key like an email as `_id` is fine only if it never changes.""",
        ex_bn=r"""`_id` "বদলাতে" হলে নতুন value দিয়ে একটা copy insert করে পুরনো document delete করতে হয়। Email-এর মতো natural key `_id` হিসেবে রাখা ঠিক আছে, যদি সেটা কখনো না বদলায়।""",
        tip_en=r"""Say the three facts in one breath: required, unique and indexed, immutable.""",
        tip_bn=r"""তিনটা কথা একসাথে বলো: বাধ্যতামূলক, unique ও indexed, আর immutable।""",
        follow=[("What is stored inside an ObjectId?", "একটা ObjectId-এর ভেতরে কী কী থাকে?")],
        related=["mongo-003", "mongo-001"],
        refs=[DOC],
    ),
    # ------------------------------------------------------------------ mongo-q03
    Q(
        id="mongo-q03", sub="CRUD", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["updateone", "replaceone", "set", "crud"],
        ver="Version-independent concept (current: MongoDB 9.0, mongosh / Node.js driver)", vs=False, status="stable",
        q_en=r"""What is the difference between `updateOne()` with `$set` and `replaceOne()`?""",
        q_bn=r"""`$set` সহ `updateOne()` আর `replaceOne()`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`updateOne()` changes only the fields named in update operators such as `$set` or `$inc` and leaves the rest of the document alone. `replaceOne()` swaps the whole document (except `_id`) for the new one, so any field you leave out is gone. In mongosh and the driver, `updateOne()` with a plain object and no operators throws an error.""",
        a_bn=r"""`updateOne()` শুধু `$set` বা `$inc`-এর মতো update operator-এ লেখা field-গুলো বদলায়, document-এর বাকি অংশ যেমন ছিল তেমনই থাকে। `replaceOne()` পুরো document-টাই (`_id` বাদে) নতুনটা দিয়ে বদলে দেয়, তাই যে field লেখোনি সেটা মুছে যায়। mongosh আর driver-এ operator ছাড়া plain object দিয়ে `updateOne()` করলে error হয়।""",
        code=r"""
            // { _id: 1, name: "Karim", city: "Dhaka", points: 10 }
            db.users.updateOne({ _id: 1 }, { $set: { city: "Sylhet" } })
            // → { _id: 1, name: 'Karim', city: 'Sylhet', points: 10 }
            db.users.replaceOne({ _id: 1 }, { name: "Karim" })
            // → { _id: 1, name: 'Karim' }
            db.users.updateOne({ _id: 1 }, { name: "X" })
            // → error: Update document requires atomic operators
        """,
        lang="javascript",
        ex_en=r"""Mongoose behaves differently: its `updateOne()` wraps top-level fields in `$set` for you, so the same call there updates `name` instead of throwing.""",
        ex_bn=r"""Mongoose-এ আচরণ আলাদা: এর `updateOne()` top-level field-গুলো নিজে থেকেই `$set`-এ মুড়ে দেয়, তাই সেখানে একই call error না দিয়ে `name` update করে।""",
        tip_en=r"""Say "update = change some fields, replace = new whole document" and mention the missing-fields risk.""",
        tip_bn=r"""বলো "update মানে কিছু field বদলানো, replace মানে পুরো নতুন document", আর field হারিয়ে যাওয়ার ঝুঁকিটা উল্লেখ করো।""",
        follow=[("How do you update a field inside a nested object without overwriting the object?", "Nested object-এর ভেতরের একটা field কীভাবে update করবে, পুরো object overwrite না করে?")],
        related=["mongo-004"],
        refs=[UPDATE_ONE, REPLACE_ONE],
    ),
    # ------------------------------------------------------------------ mongo-q04
    Q(
        id="mongo-q04", sub="CRUD", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["upsert", "setoninsert", "updateone"],
        ver="Version-independent concept (current: MongoDB 9.0, mongosh / Node.js driver)", vs=False, status="stable",
        q_en=r"""What is an upsert in MongoDB?""",
        q_bn=r"""MongoDB-তে upsert কী?""",
        a_en=r"""An upsert is an update with `{ upsert: true }`: if a document matches the filter it is updated, otherwise a new one is inserted, built from the filter's equality fields plus the update. Use `$setOnInsert` for fields that should only be set when the document is created.""",
        a_bn=r"""Upsert হলো `{ upsert: true }` দেওয়া একটা update: filter-এর সাথে কোনো document match করলে সেটা update হয়, না করলে নতুন একটা document insert হয়, যেটা filter-এর equality field আর update মিলিয়ে তৈরি হয়। যে field শুধু document তৈরির সময় set হওয়া উচিত, সেটার জন্য `$setOnInsert` ব্যবহার করো।""",
        code=r"""
            db.carts.updateOne(
              { phone: "01711000000" },
              { $inc: { visits: 1 }, $setOnInsert: { createdAt: new Date() } },
              { upsert: true }
            )
            // 1st run → upsertedCount: 1 (new cart with visits: 1)
            // 2nd run → matchedCount: 1, modifiedCount: 1 (visits: 2)
        """,
        lang="javascript",
        ex_en=r"""Two requests upserting the same new key at the same moment can both insert. A unique index on the filter field (here `phone`) prevents the duplicate.""",
        ex_bn=r"""একই নতুন key-র জন্য একই মুহূর্তে দুইটা request upsert করলে দুটোই insert করে ফেলতে পারে। Filter field-এ (এখানে `phone`) unique index দিলে duplicate আটকায়।""",
        tip_en=r"""Describe it as "update if exists, insert if not" and show `$setOnInsert`.""",
        tip_bn=r"""বলো "থাকলে update, না থাকলে insert", তারপর `$setOnInsert` দেখাও।""",
        follow=[("What does `findOneAndUpdate` return on an upsert by default?", "Upsert-এর সময় `findOneAndUpdate` default-ভাবে কী return করে?")],
        related=["mongo-021", "mongo-004"],
        refs=[UPDATE_ONE],
    ),
    # ------------------------------------------------------------------ mongo-q05
    Q(
        id="mongo-q05", sub="CRUD", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["cursor", "find", "findone", "nodejs-driver"],
        ver="MongoDB Node.js driver 7.x (current: MongoDB 9.0)", vs=True, status="stable",
        q_en=r"""What does `find()` return in the MongoDB Node.js driver, and how is it different from `findOne()`?""",
        q_bn=r"""MongoDB Node.js driver-এ `find()` কী return করে, আর সেটা `findOne()` থেকে কীভাবে আলাদা?""",
        a_en=r"""`find()` returns a cursor, not an array: a pointer to the results that fetches documents in batches as you read them. Call `.toArray()` or loop with `for await`. `findOne()` returns a promise for a single document, or `null` if nothing matches.""",
        a_bn=r"""`find()` array না, একটা cursor return করে: result-এর একটা pointer, যেটা তুমি পড়তে থাকলে batch করে document আনে। `.toArray()` call করো বা `for await` দিয়ে loop চালাও। `findOne()` একটা document-এর promise দেয়, কিছু match না করলে `null`।""",
        code=r"""
            const cursor = db.collection("users").find({ city: "Dhaka" });
            console.log(cursor instanceof Promise);              // false: it's a FindCursor
            const users = await cursor.toArray();                // → array of documents
            for await (const u of db.collection("users").find()) console.log(u.name);
            console.log(await db.collection("users").findOne({ _id: 99 })); // → null
        """,
        lang="javascript",
        ex_en=r"""A common bug is `const users = await col.find(...)`: awaiting a cursor gives back the cursor itself, not the documents. For a big result set, iterate instead of calling `toArray()`, which loads everything into memory.""",
        ex_bn=r"""একটা common bug হলো `const users = await col.find(...)`: cursor-কে await করলে document না, cursor-টাই ফেরত আসে। Result অনেক বড় হলে `toArray()` না করে iterate করো, কারণ `toArray()` সবকিছু memory-তে তোলে।""",
        tip_en=r"""Say "cursor, read lazily in batches" and mention the `toArray()` memory trade-off.""",
        tip_bn=r"""বলো "cursor, batch করে ধীরে ধীরে পড়া হয়", আর `toArray()`-এর memory খরচের কথা উল্লেখ করো।""",
        follow=[("How would you paginate a large result without `skip()`?", "`skip()` ছাড়া বড় result কীভাবে paginate করবে?")],
        related=["mongo-006"],
        refs=[FIND],
    ),
    # ------------------------------------------------------------------ mongo-q06
    Q(
        id="mongo-q06", sub="Aggregation Pipelines", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["aggregation", "match", "group", "sort"],
        ver="Version-independent concept (current: MongoDB 9.0, mongosh)", vs=False, status="stable",
        q_en=r"""What is the aggregation pipeline in MongoDB?""",
        q_bn=r"""MongoDB-তে aggregation pipeline কী?""",
        a_en=r"""The aggregation pipeline is a list of stages: each stage transforms the documents and passes the result to the next, like an assembly line. Common stages are `$match` (filter), `$group` (group and compute sums or counts), `$sort`, `$project`, `$lookup` (join) and `$limit`. Put `$match` early so it can use an index and shrink the data.""",
        a_bn=r"""Aggregation pipeline হলো কয়েকটা stage-এর list: প্রতিটি stage document-গুলো বদলে result পরের stage-এ পাঠায়, অনেকটা কারখানার assembly line-এর মতো। Common stage হলো `$match` (filter), `$group` (group করে sum বা count), `$sort`, `$project`, `$lookup` (join) আর `$limit`। `$match` শুরুর দিকে রাখো, যাতে index ব্যবহার করতে পারে আর data কমে যায়।""",
        code=r"""
            db.orders.insertMany([
              { city: "Dhaka", amount: 500, status: "delivered" }, { city: "Dhaka", amount: 1000, status: "delivered" },
              { city: "Sylhet", amount: 300, status: "delivered" }, { city: "Dhaka", amount: 900, status: "cancelled" } ])
            db.orders.aggregate([
              { $match: { status: "delivered" } },
              { $group: { _id: "$city", total: { $sum: "$amount" }, orders: { $sum: 1 } } },
              { $sort: { total: -1 } } ])
        """,
        lang="javascript",
        output=r"""
            [
              { _id: 'Dhaka', total: 1500, orders: 2 },
              { _id: 'Sylhet', total: 300, orders: 1 }
            ]
        """,
        ex_en=r"""The cancelled order is dropped by `$match` before grouping. `$group` output has no guaranteed order, which is why the `$sort` stage is needed.""",
        ex_bn=r"""Cancelled order-টা group করার আগেই `$match`-এ বাদ পড়ে। `$group`-এর output-এর কোনো নিশ্চিত order নেই, তাই `$sort` stage লাগে।""",
        tip_en=r"""Compare it to SQL: `$match` ≈ `WHERE`, `$group` ≈ `GROUP BY`, `$sort` ≈ `ORDER BY`.""",
        tip_bn=r"""SQL-এর সাথে মিলিয়ে বলো: `$match` ≈ `WHERE`, `$group` ≈ `GROUP BY`, `$sort` ≈ `ORDER BY`।""",
        follow=[
            ("Why should `$match` come before `$lookup` when possible?", "সম্ভব হলে `$match` কেন `$lookup`-এর আগে রাখা উচিত?"),
            ("What does `$unwind` do?", "`$unwind` কী করে?"),
        ],
        related=["mongo-012", "mongo-013", "mongo-024"],
        refs=[AGG],
    ),
    # ------------------------------------------------------------------ mongo-q07
    Q(
        id="mongo-q07", sub="Performance & Explain", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["explain", "ixscan", "collscan", "indexes"],
        ver="Version-independent concept (current: MongoDB 9.0, mongosh)", vs=False, status="stable",
        q_en=r"""How do you check whether a MongoDB query uses an index?""",
        q_bn=r"""MongoDB-র একটা query index ব্যবহার করছে কিনা, কীভাবে check করবে?""",
        a_en=r"""Run the query with `.explain("executionStats")`. `IXSCAN` in the winning plan means an index was used; `COLLSCAN` means every document was read. Then compare `totalKeysExamined` and `totalDocsExamined` with `nReturned`: for a good index they are close.""",
        a_bn=r"""Query-টা `.explain("executionStats")` দিয়ে চালাও। Winning plan-এ `IXSCAN` থাকলে index ব্যবহার হয়েছে; `COLLSCAN` মানে সব document পড়া হয়েছে। তারপর `totalKeysExamined` আর `totalDocsExamined`-কে `nReturned`-এর সাথে মেলাও: ভালো index হলে সংখ্যাগুলো কাছাকাছি থাকে।""",
        code=r"""
            // 10,000 users, no index on email yet
            db.users.find({ email: "u42@x.com" }).explain("executionStats")
            // → winningPlan.stage: 'COLLSCAN', nReturned: 1, totalDocsExamined: 10000
            db.users.createIndex({ email: 1 })
            db.users.find({ email: "u42@x.com" }).explain("executionStats")
            // → 'FETCH' ← 'IXSCAN', nReturned: 1, totalKeysExamined: 1, totalDocsExamined: 1
        """,
        lang="javascript",
        ex_en=r"""Also look for a `SORT` stage: it means the sort happened in memory instead of reading the index in order.""",
        ex_bn=r"""`SORT` stage আছে কিনা-ও দেখো: থাকলে বুঝবে sort memory-তে হয়েছে, index-এর order থেকে পড়া হয়নি।""",
        tip_en=r"""Name the three numbers (`nReturned`, keys examined, docs examined) and what a healthy ratio looks like.""",
        tip_bn=r"""তিনটা সংখ্যার নাম বলো (`nReturned`, examined key, examined doc), আর ভালো অনুপাত দেখতে কেমন সেটা বলো।""",
        follow=[("Why can wrapping a field in a function (like `$year`) stop index use?", "কোনো field-কে function-এ (যেমন `$year`) মুড়ে দিলে index কেন ব্যবহার হয় না?")],
        related=["mongo-008", "mongo-023", "mongo-015"],
        refs=[EXPLAIN],
    ),
    # ------------------------------------------------------------------ mongo-q08
    Q(
        id="mongo-q08", sub="CRUD", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["arrays", "positional-operator", "arrayfilters", "update-operators"],
        ver="Version-independent concept (current: MongoDB 9.0, mongosh)", vs=False, status="stable",
        q_en=r"""How do you update one element inside an array, like one item's `qty` in an order?""",
        q_bn=r"""Array-র ভেতরের একটা element কীভাবে update করবে, যেমন একটা order-এর একটা item-এর `qty`?""",
        a_en=r"""Use the positional operators. `$` updates the first array element matched by the query filter, `$[]` updates every element, and `$[<id>]` with `arrayFilters` updates every element that matches a condition you give.""",
        a_bn=r"""Positional operator ব্যবহার করো। `$` query filter-এ match করা প্রথম array element-টা update করে, `$[]` সব element update করে, আর `arrayFilters`-সহ `$[<id>]` তোমার দেওয়া শর্ত মানা সব element update করে।""",
        code=r"""
            // { _id: 1, items: [ { sku: "A", qty: 1 }, { sku: "B", qty: 2 } ] }
            db.orders.updateOne({ _id: 1, "items.sku": "B" }, { $inc: { "items.$.qty": 3 } })
            // → items: [ { sku: 'A', qty: 1 }, { sku: 'B', qty: 5 } ]
            db.orders.updateOne({ _id: 1 }, { $set: { "items.$[it].qty": 0 } },
                                { arrayFilters: [ { "it.sku": "A" } ] })
            // → items: [ { sku: 'A', qty: 0 }, { sku: 'B', qty: 5 } ]
        """,
        lang="javascript",
        ex_en=r"""For `$`, the array field must appear in the query filter (here `"items.sku": "B"`), or MongoDB doesn't know which position to update. The whole update is still atomic for that one document.""",
        ex_bn=r"""`$`-এর জন্য array field-টা query filter-এ থাকতেই হবে (এখানে `"items.sku": "B"`), না হলে MongoDB জানে না কোন position update করবে। পুরো update-টা ওই একটা document-এর জন্য atomic-ই থাকে।""",
        tip_en=r"""Show the `$` example first, then say `arrayFilters` is for "every element that matches" cases.""",
        tip_bn=r"""আগে `$`-এর example দেখাও, তারপর বলো "শর্ত মানা সব element"-এর ক্ষেত্রে `arrayFilters` লাগে।""",
        follow=[("How would you remove one item from the array?", "Array থেকে একটা item কীভাবে সরাবে?")],
        related=["mongo-004", "mongo-014"],
        refs=[POS_FILTERED, UPDATE_ONE],
    ),
    # ------------------------------------------------------------------ mongo-q09
    Q(
        id="mongo-q09", sub="Change Streams", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["change-streams", "watch", "realtime", "resume-token"],
        ver="MongoDB 9.0, Node.js driver 7.x (replica set or sharded cluster)", vs=True, status="stable",
        q_en=r"""What is a change stream in MongoDB?""",
        q_bn=r"""MongoDB-তে change stream কী?""",
        a_en=r"""A change stream lets your app subscribe to inserts, updates and deletes on a collection, database or whole deployment in real time with `watch()`; it is built on the oplog. It only works on a replica set or sharded cluster, and every event has a resume token, so a restarted listener can continue where it stopped.""",
        a_bn=r"""Change stream দিয়ে তোমার app `watch()` call করে একটা collection, database বা পুরো deployment-এর insert, update আর delete real time-এ শুনতে পারে; এটা oplog-এর ওপর তৈরি। এটা শুধু replica set বা sharded cluster-এ চলে, আর প্রতিটি event-এ একটা resume token থাকে, তাই listener restart হলে যেখানে থেমেছিল সেখান থেকে আবার শুরু করতে পারে।""",
        code=r"""
            const orders = db.collection("orders");
            const stream = orders.watch([{ $match: { operationType: "insert" } }]);
            stream.on("change", (ev) => console.log(ev.operationType, ev.fullDocument.total));
            await orders.insertOne({ total: 450 });   // → insert 450
            // later: orders.watch([], { resumeAfter: savedToken }) continues after that event
        """,
        lang="javascript",
        ex_en=r"""Typical uses: notifications, cache invalidation, syncing to a search index. Save the last `ev._id` (the resume token) somewhere durable; if the oplog has already moved past it, resuming fails and you need a full resync.""",
        ex_bn=r"""সাধারণ ব্যবহার: notification, cache invalidation, search index-এ sync। শেষ `ev._id` (resume token) কোথাও durable জায়গায় save করো; oplog যদি ততক্ষণে সেটা পার হয়ে যায়, resume fail করে আর পুরো resync লাগে।""",
        tip_en=r"""Say "real-time feed of changes, needs a replica set, resumable with a token": that covers what interviewers check.""",
        tip_bn=r"""বলো "change-এর real-time feed, replica set লাগে, token দিয়ে resume করা যায়": interviewer যা দেখতে চায় তার সবই এতে আছে।""",
        follow=[("Why not poll the collection every few seconds instead?", "এর বদলে কয়েক second পরপর collection poll করলে সমস্যা কী?")],
        related=["mongo-010", "mongo-030"],
        refs=[CHANGE_STREAMS],
    ),
    # ------------------------------------------------------------------ mongo-q10
    Q(
        id="mongo-q10", sub="Schema Design", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["schema-validation", "jsonschema", "validator"],
        ver="Version-independent concept (current: MongoDB 9.0, mongosh)", vs=False, status="stable",
        q_en=r"""How can MongoDB itself enforce a schema on a collection?""",
        q_bn=r"""MongoDB নিজেই কীভাবে একটা collection-এ schema enforce করতে পারে?""",
        a_en=r"""Add a `$jsonSchema` validator to the collection with `createCollection()` or `collMod`: you can require fields and restrict BSON types, ranges and enum values. With the default settings, an insert or update that breaks the rules fails with "Document failed validation", whichever app or tool sends it.""",
        a_bn=r"""`createCollection()` বা `collMod` দিয়ে collection-এ একটা `$jsonSchema` validator যোগ করো: field required করা যায়, আর BSON type, range ও enum value সীমিত করা যায়। Default setting-এ নিয়ম ভাঙা insert বা update "Document failed validation" error দিয়ে fail করে, যে app বা tool-ই পাঠাক না কেন।""",
        code=r"""
            db.createCollection("products", { validator: { $jsonSchema: {
              bsonType: "object", required: ["name", "price"],
              properties: { name: { bsonType: "string" }, price: { bsonType: "number", minimum: 0 } }
            } } })
            db.products.insertOne({ name: "Pen", price: -5 })  // → MongoServerError: Document failed validation
            db.products.insertOne({ name: "Pen", price: 20 })  // → acknowledged: true
        """,
        lang="javascript",
        ex_en=r"""`validationLevel` and `validationAction` control how strictly existing documents and updates are checked, and whether a violation is rejected or only logged. Mongoose validation runs only inside your app; a database validator also protects against scripts and other services.""",
        ex_bn=r"""`validationLevel` আর `validationAction` ঠিক করে আগের document আর update কতটা কড়াভাবে check হবে, আর নিয়ম ভাঙলে reject হবে নাকি শুধু log হবে। Mongoose validation শুধু তোমার app-এর ভেতরে চলে; database validator script আর অন্য service থেকেও রক্ষা করে।""",
        tip_en=r"""Contrast it with Mongoose: app-level vs database-level validation, and say when you'd want both.""",
        tip_bn=r"""Mongoose-এর সাথে তুলনা করো: app-level বনাম database-level validation, আর কখন দুটোই চাইবে সেটা বলো।""",
        follow=[("What happens to existing documents that don't match a newly added validator?", "নতুন validator যোগ করলে আগের যেসব document নিয়ম মানে না, সেগুলোর কী হয়?")],
        related=["mongo-022", "mongo-001"],
        refs=[SCHEMA_VALIDATION],
    ),
]

save("mongodb", "quick", QUESTIONS)
