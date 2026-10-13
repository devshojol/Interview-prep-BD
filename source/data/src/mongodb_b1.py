# MongoDB — batch 1 (mongo-001..005, mongo-012, mongo-023, mongo-030)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

DOC = ("MongoDB Manual — Documents", "https://www.mongodb.com/docs/manual/core/document/")
BSON_TYPES = ("MongoDB Manual — BSON Types", "https://www.mongodb.com/docs/manual/reference/bson-types/")
OBJECTID = ("MongoDB Manual — ObjectId()", "https://www.mongodb.com/docs/manual/reference/method/ObjectId/")
LIMITS = ("MongoDB Manual — Limits and Thresholds", "https://www.mongodb.com/docs/manual/reference/limits/")
UPDATE_OPS = ("MongoDB Manual — Update Operators", "https://www.mongodb.com/docs/manual/reference/operator/update/")
UPDATE_ONE = ("MongoDB Manual — db.collection.updateOne()", "https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/")
INSERT_MANY = ("MongoDB Manual — db.collection.insertMany()", "https://www.mongodb.com/docs/manual/reference/method/db.collection.insertMany/")
AGG = ("MongoDB Manual — Aggregation Operations", "https://www.mongodb.com/docs/manual/aggregation/")
GROUP = ("MongoDB Manual — $group (aggregation)", "https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/")
EXPLAIN = ("MongoDB Manual — Explain Results", "https://www.mongodb.com/docs/manual/reference/explain-results/")
EXPR = ("MongoDB Manual — $expr", "https://www.mongodb.com/docs/manual/reference/operator/query/expr/")
SHARD_KEY = ("MongoDB Manual — Choose a Shard Key", "https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/")
UNBOUNDED = ("MongoDB Manual — Schema Design Patterns", "https://www.mongodb.com/docs/manual/data-modeling/design-patterns/")
SHARDING = ("MongoDB Manual — Sharding", "https://www.mongodb.com/docs/manual/sharding/")

QUESTIONS = [
    # ------------------------------------------------------------------ mongo-001
    Q(
        id="mongo-001", sub="Documents & Collections", diff="easy", type="conceptual",
        prio="high", market="both", mins=2,
        tags=["documents", "collections", "schema", "basics"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""What are documents and collections in MongoDB, and how do they compare to rows and tables in a relational database?""",
        q_bn=r"""MongoDB-তে document আর collection কী? Relational database-এর row আর table-এর সাথে এদের তুলনা কীভাবে করবে?""",
        a_en=r"""
            A **document** is a single record: a set of field–value pairs stored as BSON. Values can be nested objects and arrays, so one document can hold what would be several joined rows in SQL. A **collection** is a group of documents — roughly the equivalent of a table — and a database holds many collections.

            The big differences from tables: there's no fixed schema enforced by default (documents in the same collection can have different fields), related data is often **nested** instead of joined, and every document has a unique, immutable `_id` primary key (the driver generates an `ObjectId` if you don't provide one). Collections are created automatically on the first insert.
        """,
        a_bn=r"""
            **Document** হলো একটি single record — field-value pair-এর একটা set, যা BSON format-এ store হয়। Value হিসেবে nested object আর array রাখা যায়, তাই SQL-এ যেটা কয়েকটা row join করে আনতে হতো, সেটা একটা document-এই রাখা যায়। **Collection** হলো document-এর group — মোটামুটি table-এর মতো, আর একটা database-এ অনেকগুলো collection থাকে।

            Table-এর সাথে মূল পার্থক্য: default-ভাবে কোনো fixed schema enforce হয় না (একই collection-এর document-এ ভিন্ন ভিন্ন field থাকতে পারে), related data অনেক সময় join না করে **nested** রাখা হয়, আর প্রতিটি document-এর একটা unique, immutable `_id` primary key থাকে (না দিলে driver নিজেই `ObjectId` generate করে)। প্রথম insert-এর সময় collection automatically তৈরি হয়ে যায়।
        """,
        ex_en=r"""
            - **Flexible schema ≠ no schema.** Your application still has a schema; MongoDB just doesn't force it unless you add a `$jsonSchema` validator (or use an ODM like Mongoose). In production, unvalidated data drift (e.g. `price` stored as a string in some documents) is a common source of bugs.
            - **Design by access pattern.** In SQL you normalise first and query later; in MongoDB you ask "what does the app read together?" and shape documents around that.
            - **`_id`** always has a unique index, cannot be changed after insert, and can be any BSON type except an array, regex or undefined (ObjectId, string, number, UUID, even an embedded document...).
            - **Limits:** a document can be at most 16 MB, which is one reason unbounded nested arrays are an anti-pattern.
        """,
        ex_bn=r"""
            - **Flexible schema মানে schema নেই — তা নয়।** Application-এর একটা schema থাকেই; MongoDB শুধু সেটা force করে না, যদি না তুমি `$jsonSchema` validator যোগ করো (বা Mongoose-এর মতো ODM ব্যবহার করো)। Production-এ validation ছাড়া data drift (যেমন কিছু document-এ `price` string হিসেবে save হওয়া) bug-এর একটা common কারণ।
            - **Access pattern অনুযায়ী design করো।** SQL-এ আগে normalise করে পরে query লেখা হয়; MongoDB-তে প্রশ্ন হলো "app কোন data একসাথে read করে?" — সেই অনুযায়ী document-এর shape ঠিক করা হয়।
            - **`_id`**-এ সবসময় একটা unique index থাকে, insert-এর পর এটা change করা যায় না, আর array, regex বা undefined ছাড়া যেকোনো BSON type (ObjectId, string, number, UUID, এমনকি embedded document...) হতে পারে।
            - **Limit:** একটা document সর্বোচ্চ 16 MB হতে পারে — এজন্যই unbounded nested array একটা anti-pattern।
        """,
        tip_en=r"""Use the table/row analogy to start, then immediately say where it breaks down (nesting, flexible schema, design by access pattern). That shows you don't think of MongoDB as "SQL without joins".""",
        tip_bn=r"""শুরুতে table/row-এর analogy দাও, তারপর সাথে সাথে বলো কোথায় analogy-টা আর খাটে না (nesting, flexible schema, access pattern অনুযায়ী design)। এতে বোঝা যায় তুমি MongoDB-কে শুধু "join ছাড়া SQL" ভাবো না।""",
        mist_en=r"""Saying MongoDB is "schemaless" so you never need to think about schema, or assuming `_id` must always be an ObjectId.""",
        mist_bn=r"""MongoDB "schemaless", তাই schema নিয়ে ভাবতে হয় না — এমন বলা; অথবা ধরে নেওয়া যে `_id` সবসময় ObjectId-ই হতে হবে।""",
        code=r"""
            // One document in the "users" collection (mongosh syntax)
            {
              _id: ObjectId("6709a1f2c3d4e5f601234567"),
              name: "Nusrat Jahan",
              email: "nusrat@example.com",
              roles: ["customer"],                       // array instead of a join table
              address: { city: "Dhaka", area: "Mirpur" }, // nested object
              createdAt: ISODate("2026-10-01T08:30:00Z")
            }
        """,
        lang="javascript",
        follow=[
            ("How would you enforce a schema at the database level in MongoDB?", "MongoDB-তে database level-এ schema কীভাবে enforce করবে?"),
            ("Can two documents in the same collection have different fields? Is that a good idea?", "একই collection-এর দুইটা document-এ কি ভিন্ন field থাকতে পারে? সেটা কি ভালো আইডিয়া?"),
        ],
        refs=[DOC, LIMITS],
    ),
    # ------------------------------------------------------------------ mongo-002
    Q(
        id="mongo-002", sub="BSON vs JSON", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["bson", "json", "data-types", "decimal128", "document-size"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""What is BSON and how is it different from JSON? Why does it matter which BSON type you store a value as?""",
        q_bn=r"""BSON কী, আর JSON থেকে এটা কীভাবে আলাদা? কোনো value কোন BSON type হিসেবে store করছ — সেটা কেন গুরুত্বপূর্ণ?""",
        a_en=r"""
            BSON (Binary JSON) is the binary format MongoDB uses to store documents and send them over the network. It looks like JSON conceptually, but:

            - It's **binary**, with length prefixes, so the server can traverse and skip fields quickly.
            - It has **more types**: `ObjectId`, `Date`, 32/64-bit integers, `Double`, `Decimal128`, binary data (incl. UUID), regex, `Timestamp` and more. JSON only has string, number, boolean, null, object and array.
            - A single BSON document is limited to **16 MB**.

            Types matter because queries, sorting and indexes compare by type. Store dates as `Date`, not strings, and money as `Decimal128` (or integer poisha/cents), not a floating-point double.
        """,
        a_bn=r"""
            BSON (Binary JSON) হলো সেই binary format যেটা দিয়ে MongoDB document store করে এবং network-এ পাঠায়। ধারণাগতভাবে JSON-এর মতোই, কিন্তু:

            - এটা **binary**, length prefix সহ — তাই server দ্রুত field traverse ও skip করতে পারে।
            - এতে **বেশি type** আছে: `ObjectId`, `Date`, 32/64-bit integer, `Double`, `Decimal128`, binary data (UUID সহ), regex, `Timestamp` ইত্যাদি। JSON-এ শুধু string, number, boolean, null, object আর array।
            - একটা BSON document সর্বোচ্চ **16 MB** হতে পারে।

            Type গুরুত্বপূর্ণ কারণ query, sorting আর index type অনুযায়ী compare করে। Date-কে string না রেখে `Date` হিসেবে রাখো, আর টাকার amount floating-point double না রেখে `Decimal128` (বা integer পয়সা/cents) হিসেবে রাখো।
        """,
        ex_en=r"""
            - **Dates as strings** break range queries and sorting unless the format is perfectly consistent, and TTL indexes only work on real `Date` values.
            - **Money as doubles** gives rounding errors (`0.1 + 0.2 !== 0.3`). `Decimal128` stores exact decimal values.
            - **Mixed types** in one field (`"25"` vs `25`) mean `{ age: { $gt: 18 } }` silently skips the string ones — numeric comparison only matches numbers.
            - **Extended JSON (EJSON)** is how BSON-only types are written in JSON, e.g. `{"$oid": "..."}`, `{"$date": "..."}`, `{"$numberDecimal": "649.50"}` — you see it in `mongoexport` and some APIs.
            - **16 MB limit:** large files go to object storage (S3) or GridFS, never into one huge document. BSON isn't always smaller than JSON — field names are repeated in every document.
        """,
        ex_bn=r"""
            - **Date-কে string হিসেবে রাখলে** format পুরোপুরি consistent না হলে range query আর sorting ভেঙে যায়, আর TTL index শুধু আসল `Date` value-তেই কাজ করে।
            - **টাকা double হিসেবে রাখলে** rounding error হয় (`0.1 + 0.2 !== 0.3`)। `Decimal128` exact decimal value store করে।
            - একই field-এ **mixed type** থাকলে (`"25"` আর `25`) `{ age: { $gt: 18 } }` চুপচাপ string-গুলো বাদ দিয়ে দেয় — numeric comparison শুধু number-কেই match করে।
            - **Extended JSON (EJSON)** দিয়ে BSON-only type-গুলো JSON-এ লেখা হয়, যেমন `{"$oid": "..."}`, `{"$date": "..."}`, `{"$numberDecimal": "649.50"}` — `mongoexport` আর কিছু API-তে এটা দেখবে।
            - **16 MB limit:** বড় file object storage (S3) বা GridFS-এ যায়, কখনো একটা বিশাল document-এ না। আর BSON সবসময় JSON-এর চেয়ে ছোট নয় — প্রতিটি document-এ field name বারবার store হয়।
        """,
        tip_en=r"""Give one concrete bug story — e.g. prices stored as strings so sorting by price was wrong — it proves you've seen type issues in real data.""",
        tip_bn=r"""একটা বাস্তব bug-এর উদাহরণ দাও — যেমন price string হিসেবে save হওয়ায় price অনুযায়ী sort ভুল আসছিল। এতে বোঝা যায় তুমি real data-তে type-এর সমস্যা দেখেছ।""",
        mist_en=r"""Saying BSON is "just compressed JSON", or storing dates and prices as strings because "MongoDB is flexible".""",
        mist_bn=r"""BSON-কে "শুধু compressed JSON" বলা, অথবা "MongoDB তো flexible" ভেবে date আর price string হিসেবে store করা।""",
        code=r"""
            db.products.insertOne({
              name: "Miniket Rice 5kg",
              price: NumberDecimal("649.50"),      // exact decimal for money
              stock: NumberInt(120),               // 32-bit integer
              soldCount: NumberLong("1500000"),    // 64-bit integer
              createdAt: new Date(),               // BSON Date (UTC milliseconds)
              tags: ["grocery", "rice"]
            })

            // The same values in Extended JSON (e.g. from mongoexport):
            // { "price": { "$numberDecimal": "649.50" },
            //   "createdAt": { "$date": "2026-10-12T06:00:00Z" } }
        """,
        lang="javascript",
        follow=[
            ("How would you store a 50 MB PDF that belongs to a user?", "একজন user-এর 50 MB PDF কোথায় এবং কীভাবে store করবে?"),
            ("What problems do you get if one field holds both strings and numbers?", "একই field-এ string আর number দুটোই থাকলে কী সমস্যা হয়?"),
        ],
        related=["mongo-001"],
        refs=[BSON_TYPES, LIMITS],
    ),
    # ------------------------------------------------------------------ mongo-003
    Q(
        id="mongo-003", sub="BSON vs JSON", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=1,
        tags=["objectid", "bson", "_id"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""Which statement about MongoDB's default `_id` value, the `ObjectId`, is correct?""",
        q_bn=r"""MongoDB-র default `_id` value, অর্থাৎ `ObjectId` সম্পর্কে কোন statement-টি সঠিক?""",
        options=[
            ("It is a 12-byte value whose first 4 bytes are a timestamp, so it roughly reflects creation time",
             "এটা 12-byte-এর value, যার প্রথম 4 byte একটা timestamp — তাই এটা মোটামুটি তৈরির সময় বোঝায়"),
            ("It is a random UUID v4 generated by the server, so it carries no time information",
             "এটা server-এর তৈরি একটা random UUID v4, তাই এতে সময়ের কোনো তথ্য থাকে না"),
            ("It is an auto-incrementing 64-bit integer that is sequential across the whole cluster",
             "এটা auto-increment হওয়া 64-bit integer, যা পুরো cluster জুড়ে sequential"),
            ("It is a 24-byte string, and two ObjectIds created in the same second are always equal",
             "এটা 24-byte-এর string, আর একই second-এ তৈরি দুইটা ObjectId সবসময় সমান হয়"),
        ],
        correct=0,
        a_en=r"""An `ObjectId` is 12 bytes: a 4-byte timestamp (seconds since the Unix epoch), a 5-byte random value unique to the machine/process, and a 3-byte incrementing counter. Because the timestamp comes first, ObjectIds sort roughly by creation time and `getTimestamp()` can read it back.""",
        a_bn=r"""`ObjectId` হলো 12 byte: 4-byte timestamp (Unix epoch থেকে seconds), machine/process-এর জন্য unique একটা 5-byte random value, আর একটা 3-byte incrementing counter। Timestamp শুরুতে থাকায় ObjectId মোটামুটি তৈরির সময় অনুযায়ী sort হয়, আর `getTimestamp()` দিয়ে সময়টা বের করা যায়।""",
        ex_en=r"""
            The tempting wrong answer is the **auto-increment integer** — developers coming from MySQL expect it. MongoDB has no built-in auto-increment; ObjectIds are usually generated by the **driver on the client**, which is why they're unique without coordinating with the server.

            The "24" in option D is the length of the **hex string** representation, not the byte size, and the counter + random part keep IDs unique even within the same second. Ordering by `_id` is only approximately chronological (second precision, and clocks differ between app servers), so use a real `createdAt` field when exact ordering matters.
        """,
        ex_bn=r"""
            সবচেয়ে বেশি ভুল হয় **auto-increment integer** option-এ — MySQL থেকে আসা developer-রা এটাই আশা করে। MongoDB-তে built-in auto-increment নেই; ObjectId সাধারণত **client-এ driver** generate করে, এজন্যই server-এর সাথে coordinate না করেও এটা unique থাকে।

            Option D-এর "24" হলো **hex string** রূপের length, byte size না; আর counter ও random অংশের কারণে একই second-এও ID unique থাকে। `_id` দিয়ে ordering শুধু আনুমানিকভাবে chronological (second precision, আর বিভিন্ন app server-এর clock আলাদা হতে পারে) — তাই exact order দরকার হলে আসল `createdAt` field ব্যবহার করো।
        """,
        tip_en=r"""Mention that the client generates ObjectIds — it explains why inserts don't need a round trip to get an ID, and why `_id` order is only approximate.""",
        tip_bn=r"""উল্লেখ করো যে ObjectId client-ই generate করে — এতে বোঝা যায় কেন ID পেতে server-এ আলাদা round trip লাগে না, আর কেন `_id`-এর order শুধু আনুমানিক।""",
        follow=[
            ("Can you use `_id` for keyset pagination instead of `skip()`?", "`skip()`-এর বদলে `_id` দিয়ে keyset pagination করা যায় কি?"),
        ],
        related=["mongo-002"],
        refs=[OBJECTID, BSON_TYPES],
    ),
    # ------------------------------------------------------------------ mongo-004
    Q(
        id="mongo-004", sub="CRUD", diff="easy", type="query",
        prio="high", market="both", mins=3,
        tags=["updateone", "update-operators", "set", "inc", "push", "addtoset"],
        ver="Version-independent (MongoDB 5.0+ field ordering; current: MongoDB 9.0, mongosh)", vs=False, status="stable",
        q_en=r"""Given the `users` document below, write an update that changes the city to "Chattogram", marks the user as verified, adds 5 points, appends the tag "premium", and adds the badge "early-bird" only if it isn't already present. What does the document look like afterwards?""",
        q_bn=r"""নিচের `users` document-টার জন্য এমন একটা update লেখো যেটা city বদলে "Chattogram" করবে, user-কে verified mark করবে, points-এ 5 যোগ করবে, tag "premium" append করবে, আর badge "early-bird" যোগ করবে কেবল যদি সেটা আগে থেকে না থাকে। Update-এর পর document-টা দেখতে কেমন হবে?""",
        setup=r"""
            db.users.insertOne({
              _id: 1,
              name: "Karim",
              points: 10,
              tags: ["new"],
              address: { city: "Dhaka" }
            })
        """,
        setup_lang="javascript",
        code=r"""
            db.users.updateOne(
              { _id: 1 },
              {
                $set: { "address.city": "Chattogram", verified: true },
                $inc: { points: 5 },
                $push: { tags: "premium" },
                $addToSet: { badges: "early-bird" }
              }
            )

            db.users.findOne({ _id: 1 })
        """,
        lang="javascript",
        output=r"""
            { acknowledged: true, insertedId: null, matchedCount: 1, modifiedCount: 1, upsertedCount: 0 }

            {
              _id: 1,
              name: 'Karim',
              points: 15,
              tags: [ 'new', 'premium' ],
              address: { city: 'Chattogram' },
              badges: [ 'early-bird' ],
              verified: true
            }
        """,
        a_en=r"""
            Use a single `updateOne` with several update operators: `$set` with dot notation for the nested city (so the rest of `address` isn't overwritten) plus the new `verified` field, `$inc` for points, `$push` to append the tag, and `$addToSet` for the badge. `$addToSet` creates the `badges` array because it doesn't exist yet, and it would skip the value if it were already there.

            The whole update is applied **atomically** to that one document.
        """,
        a_bn=r"""
            একটা `updateOne`-এ কয়েকটা update operator ব্যবহার করো: nested city-র জন্য dot notation সহ `$set` (যাতে `address`-এর বাকি অংশ overwrite না হয়) আর নতুন `verified` field, points-এর জন্য `$inc`, tag append করতে `$push`, আর badge-এর জন্য `$addToSet`। `badges` array আগে না থাকায় `$addToSet` সেটা তৈরি করে, আর value আগে থেকে থাকলে আবার যোগ করত না।

            পুরো update-টা ওই একটা document-এর ওপর **atomically** apply হয়।
        """,
        ex_en=r"""
            - **Dot notation matters:** `$set: { address: { city: "Chattogram" } }` would replace the whole `address` object and drop any other sub-fields.
            - **New fields are appended** to the end of the document. Since MongoDB 5.0, update operators process field names in lexicographic order, which is why `badges` appears before `verified` — but your code should never depend on field order.
            - **`updateOne` needs operators.** Passing a plain object like `{ name: "X" }` is rejected; to swap the entire document (keeping `_id`) use `replaceOne`.
            - **Related operators:** `$pull` removes matching array elements, `$unset` removes a field, and `{ upsert: true }` inserts a new document when nothing matches.
            - `modifiedCount` is 0 if the update didn't actually change anything (e.g. setting the same value again).
        """,
        ex_bn=r"""
            - **Dot notation জরুরি:** `$set: { address: { city: "Chattogram" } }` দিলে পুরো `address` object replace হয়ে যেত, অন্য sub-field থাকলে মুছে যেত।
            - **নতুন field document-এর শেষে যোগ হয়।** MongoDB 5.0 থেকে update operator field name-গুলো lexicographic order-এ process করে, তাই `badges` আগে আর `verified` পরে এসেছে — তবে তোমার code কখনো field order-এর ওপর নির্ভর করা উচিত না।
            - **`updateOne`-এ operator লাগে।** শুধু `{ name: "X" }`-এর মতো plain object দিলে reject হয়; পুরো document বদলাতে (`_id` রেখে) `replaceOne` ব্যবহার করো।
            - **আরও operator:** `$pull` array থেকে matching element সরায়, `$unset` field মুছে দেয়, আর কিছু match না করলে `{ upsert: true }` নতুন document insert করে।
            - Update-এ আসলে কিছু না বদলালে (যেমন একই value আবার set করা) `modifiedCount` 0 হয়।
        """,
        tip_en=r"""Say "atomic on a single document" out loud — interviewers often follow up with "what if two requests increment points at the same time?" and `$inc` is the answer.""",
        tip_bn=r"""জোর দিয়ে বলো "single document-এ atomic" — interviewer প্রায়ই জিজ্ঞেস করে "দুইটা request একসাথে points বাড়ালে কী হবে?" — আর তার উত্তর হলো `$inc`।""",
        mist_en=r"""Reading the document, changing it in JavaScript and writing it back (lost updates under concurrency) instead of using `$inc`/`$push`; or using `$set` on the whole nested object.""",
        mist_bn=r"""`$inc`/`$push` ব্যবহার না করে document read করে JavaScript-এ বদলে আবার write করা (concurrency-তে lost update হয়); অথবা পুরো nested object-এ `$set` ব্যবহার করা।""",
        follow=[
            ("What's the difference between `$push` and `$addToSet` for an array of objects?", "Object-এর array-তে `$push` আর `$addToSet`-এর পার্থক্য কী?"),
            ("When would you use `replaceOne` instead of `updateOne`?", "কখন `updateOne`-এর বদলে `replaceOne` ব্যবহার করবে?"),
        ],
        related=["mongo-001"],
        refs=[UPDATE_OPS, UPDATE_ONE],
    ),
    # ------------------------------------------------------------------ mongo-005
    Q(
        id="mongo-005", sub="CRUD", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=2,
        tags=["insertmany", "ordered", "bulk-write", "duplicate-key"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""The `users` collection is empty and has a unique index on `email`. You run the `insertMany` below with default options. What is the result?""",
        q_bn=r"""`users` collection খালি, আর `email`-এ একটা unique index আছে। নিচের `insertMany` default option দিয়ে run করলে ফলাফল কী হবে?""",
        code=r"""
            db.users.insertMany([
              { email: "a@x.com" },
              { email: "b@x.com" },
              { email: "a@x.com" },
              { email: "c@x.com" }
            ])
        """,
        lang="javascript",
        options=[
            (r"""Nothing is inserted — the whole `insertMany` is rolled back like a transaction""",
             r"""কিছুই insert হয় না — পুরো `insertMany` একটা transaction-এর মতো rollback হয়ে যায়"""),
            (r"""`a@x.com`, `b@x.com` and `c@x.com` are inserted, the duplicate is skipped silently and no error is thrown""",
             r"""`a@x.com`, `b@x.com` আর `c@x.com` insert হয়, duplicate-টা চুপচাপ skip হয় এবং কোনো error throw হয় না"""),
            (r"""`a@x.com` and `b@x.com` are inserted, then a duplicate key error is thrown and `c@x.com` is not inserted""",
             r"""`a@x.com` আর `b@x.com` insert হয়, তারপর duplicate key error throw হয় এবং `c@x.com` insert হয় না"""),
            (r"""All four documents are inserted because `insertMany` skips unique index checks for speed""",
             r"""চারটা document-ই insert হয়, কারণ speed-এর জন্য `insertMany` unique index check skip করে"""),
        ],
        correct=2,
        a_en=r"""`insertMany` is **ordered by default**: it inserts documents in order and stops at the first error. The first two are inserted, the third fails with an E11000 duplicate key error, and the fourth is never attempted. The earlier inserts are **not** rolled back.""",
        a_bn=r"""`insertMany` **default-ভাবে ordered**: document-গুলো ক্রমানুসারে insert করে আর প্রথম error-এই থেমে যায়। প্রথম দুইটা insert হয়, তৃতীয়টা E11000 duplicate key error দিয়ে fail করে, আর চতুর্থটা চেষ্টাই করা হয় না। আগের insert-গুলো **rollback হয় না**।""",
        ex_en=r"""
            A bulk insert is not a transaction — each document insert is atomic on its own, so option A is wrong unless you explicitly wrap it in a multi-document transaction.

            Option B is the tempting one: with `{ ordered: false }` MongoDB **does** continue past the failure and inserts `c@x.com`, but it still reports an error (in the Node.js driver a `MongoBulkWriteError` listing the failed index and the `insertedCount`). So you'd use `ordered: false` for imports where you want "insert everything valid", and then inspect the error for the failed documents.
        """,
        ex_bn=r"""
            Bulk insert কোনো transaction না — প্রতিটি document insert আলাদাভাবে atomic, তাই explicitly multi-document transaction-এ না রাখলে option A ভুল।

            সবচেয়ে বিভ্রান্তিকর option হলো B: `{ ordered: false }` দিলে MongoDB failure-এর পরেও **চালিয়ে যায়** এবং `c@x.com` insert করে, কিন্তু তখনও একটা error report করে (Node.js driver-এ `MongoBulkWriteError`, যেখানে কোন index fail করেছে আর `insertedCount` থাকে)। তাই data import-এ "যত valid আছে সব insert করো" চাইলে `ordered: false` ব্যবহার করবে, তারপর error থেকে fail হওয়া document-গুলো দেখে নেবে।
        """,
        tip_en=r"""Mention both modes and what the error object contains — it shows you've actually handled bulk-import failures, not just memorised the default.""",
        tip_bn=r"""দুইটা mode-ই বলো আর error object-এ কী থাকে সেটাও উল্লেখ করো — এতে বোঝা যায় তুমি আসলেই bulk import-এর failure handle করেছ, শুধু default মুখস্থ করোনি।""",
        follow=[
            ("How would you make a CSV import of 100,000 users skip duplicates but report them?", "100,000 user-এর একটা CSV import-এ duplicate skip করে সেগুলো report করবে কীভাবে?"),
        ],
        related=["mongo-004"],
        refs=[INSERT_MANY],
    ),
    # ------------------------------------------------------------------ mongo-012
    Q(
        id="mongo-012", sub="Aggregation Pipelines", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["aggregation", "match", "group", "map", "sort"],
        ver="Version-independent (MongoDB 4.x+; current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""Using the `orders` collection below, write an aggregation that returns, for **delivered** orders only, each customer's total revenue (sum of `qty × price` across all items) and number of orders, sorted by revenue from highest to lowest.""",
        q_bn=r"""নিচের `orders` collection ব্যবহার করে একটা aggregation লেখো, যেটা শুধু **delivered** order-এর জন্য প্রতিটি customer-এর মোট revenue (সব item-এর `qty × price`-এর যোগফল) আর order সংখ্যা দেবে, revenue বেশি থেকে কম ক্রমে sort করে।""",
        setup=r"""
            db.orders.insertMany([
              { _id: 1, customer: "Rahim", status: "delivered",
                items: [ { sku: "A", qty: 2, price: 100 }, { sku: "B", qty: 1, price: 250 } ] },
              { _id: 2, customer: "Karim", status: "delivered",
                items: [ { sku: "A", qty: 1, price: 100 } ] },
              { _id: 3, customer: "Rahim", status: "cancelled",
                items: [ { sku: "C", qty: 5, price: 80 } ] },
              { _id: 4, customer: "Sumi", status: "delivered",
                items: [ { sku: "B", qty: 2, price: 250 }, { sku: "C", qty: 1, price: 80 } ] },
              { _id: 5, customer: "Karim", status: "delivered",
                items: [ { sku: "C", qty: 3, price: 80 } ] }
            ])
        """,
        setup_lang="javascript",
        code=r"""
            db.orders.aggregate([
              { $match: { status: "delivered" } },
              { $project: {
                  customer: 1,
                  orderTotal: {
                    $sum: {
                      $map: {
                        input: "$items",
                        as: "i",
                        in: { $multiply: ["$$i.qty", "$$i.price"] }
                      }
                    }
                  }
              } },
              { $group: {
                  _id: "$customer",
                  revenue: { $sum: "$orderTotal" },
                  orders: { $sum: 1 }
              } },
              { $sort: { revenue: -1 } }
            ])
        """,
        lang="javascript",
        output=r"""
            [
              { _id: 'Sumi', revenue: 580, orders: 1 },
              { _id: 'Rahim', revenue: 450, orders: 1 },
              { _id: 'Karim', revenue: 340, orders: 2 }
            ]
        """,
        a_en=r"""
            The pipeline filters first, computes a per-order total, then groups by customer:

            1. `$match` keeps only delivered orders (order 3 is dropped), and can use an index on `status`.
            2. `$project` computes `orderTotal` with `$map` + `$multiply` over the `items` array, then `$sum` adds the array up: Rahim #1 = 2×100 + 1×250 = 450, Karim #2 = 100, Sumi #4 = 500 + 80 = 580, Karim #5 = 240.
            3. `$group` by `customer` sums the totals and counts orders with `{ $sum: 1 }` → Karim = 100 + 240 = 340 from 2 orders.
            4. `$sort` orders the result, because `$group` output order is not guaranteed.
        """,
        a_bn=r"""
            Pipeline-টা আগে filter করে, তারপর প্রতিটি order-এর total হিসাব করে, তারপর customer অনুযায়ী group করে:

            1. `$match` শুধু delivered order রাখে (order 3 বাদ পড়ে), আর `status`-এ index থাকলে সেটা ব্যবহার করতে পারে।
            2. `$project`-এ `items` array-এর ওপর `$map` + `$multiply` দিয়ে প্রতিটি item-এর দাম বের করে `$sum` দিয়ে যোগ করে `orderTotal` হয়: Rahim #1 = 2×100 + 1×250 = 450, Karim #2 = 100, Sumi #4 = 500 + 80 = 580, Karim #5 = 240।
            3. `customer` অনুযায়ী `$group` করে total যোগ হয় আর `{ $sum: 1 }` দিয়ে order গোনা হয় → Karim = 100 + 240 = 340, 2টা order।
            4. শেষে `$sort` করা দরকার, কারণ `$group`-এর output order guaranteed না।
        """,
        ex_en=r"""
            - **Why not `$unwind`?** `$unwind: "$items"` + `$group` also works, but it multiplies documents (one per item) and then counting orders needs `$addToSet` of `_id` + `$size`. Computing the order total inside the document with `$map` keeps one document per order, which is cheaper and makes `{ $sum: 1 }` count orders correctly.
            - **`$match` first:** only stages at the start of the pipeline can use indexes. Filtering early also reduces the data every later stage has to process.
            - **Memory:** `$group` and `$sort` are blocking stages with a 100 MB per-stage memory limit (they can spill to disk). With very many customers, consider pre-aggregated summary collections for dashboards.
            - **Money:** integers are fine for this example; in real apps store `Decimal128` or integer poisha, and `$multiply`/`$sum` work with `Decimal128` too.
        """,
        ex_bn=r"""
            - **`$unwind` কেন না?** `$unwind: "$items"` + `$group`-ও কাজ করে, কিন্তু এতে document সংখ্যা বেড়ে যায় (প্রতি item-এ একটা), আর order গুনতে তখন `_id`-এর `$addToSet` + `$size` লাগে। `$map` দিয়ে document-এর ভেতরেই order total হিসাব করলে প্রতি order-এ একটাই document থাকে — এটা সস্তা, আর `{ $sum: 1 }` সঠিকভাবে order গোনে।
            - **আগে `$match`:** শুধু pipeline-এর শুরুর stage-গুলো index ব্যবহার করতে পারে। আগে filter করলে পরের সব stage-এ কম data process করতে হয়।
            - **Memory:** `$group` আর `$sort` হলো blocking stage, প্রতিটি stage-এর 100 MB memory limit আছে (disk-এ spill করতে পারে)। অনেক বেশি customer থাকলে dashboard-এর জন্য pre-aggregated summary collection ভাবো।
            - **টাকা:** এই উদাহরণে integer ঠিক আছে; আসল app-এ `Decimal128` বা integer পয়সা রাখো — `$multiply`/`$sum` `Decimal128`-এর সাথেও কাজ করে।
        """,
        tip_en=r"""Talk through the pipeline stage by stage with the intermediate numbers — interviewers check whether you can "run" a pipeline in your head, not just write it.""",
        tip_bn=r"""Pipeline-এর প্রতিটি stage মাঝের সংখ্যাগুলো সহ ব্যাখ্যা করো — interviewer দেখতে চায় তুমি মাথার ভেতরে pipeline "run" করতে পারো কি না, শুধু লিখতে পারো কি না সেটা না।""",
        mist_en=r"""Using `$unwind` and then `{ $sum: 1 }` (counts items, not orders); forgetting `$sort` after `$group`; putting `$match` after `$group` so it can't use an index.""",
        mist_bn=r"""`$unwind`-এর পর `{ $sum: 1 }` ব্যবহার করা (এতে item গোনা হয়, order না); `$group`-এর পর `$sort` ভুলে যাওয়া; `$match`-কে `$group`-এর পরে রাখা, ফলে index ব্যবহার হয় না।""",
        follow=[
            ("How would you also return the top-selling SKU per customer?", "প্রতিটি customer-এর সবচেয়ে বেশি বিক্রি হওয়া SKU-ও কীভাবে return করবে?"),
            ("How would you build this report for 50 million orders without slowing the primary?", "50 million order-এর জন্য primary-কে slow না করে এই report কীভাবে বানাবে?"),
        ],
        related=["mongo-004"],
        refs=[AGG, GROUP],
    ),
    # ------------------------------------------------------------------ mongo-023
    Q(
        id="mongo-023", sub="Performance & Explain", diff="hard", type="debugging",
        prio="high", market="both", mins=7,
        tags=["explain", "collscan", "ixscan", "expr", "dates", "indexes"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""A monthly sales report became very slow after `orders` grew to ~5 million documents, even though there is an index on `{ createdAt: 1 }`. Here is the query and part of its `explain("executionStats")` output. What's wrong, and how would you fix it? (The business runs on Bangladesh time, UTC+6.)""",
        q_bn=r"""`orders` collection প্রায় 5 million document-এ পৌঁছানোর পর একটা monthly sales report খুব slow হয়ে গেছে, যদিও `{ createdAt: 1 }`-এ index আছে। নিচে query আর তার `explain("executionStats")` output-এর একটা অংশ দেওয়া আছে। সমস্যা কী, আর কীভাবে fix করবে? (Business-টা বাংলাদেশ সময়ে, অর্থাৎ UTC+6-এ চলে।)""",
        code=r"""
            // Index: { createdAt: 1 }
            db.orders.find({
              $expr: {
                $and: [
                  { $eq: [{ $year: "$createdAt" }, 2026] },
                  { $eq: [{ $month: "$createdAt" }, 9] }
                ]
              }
            }).explain("executionStats")

            // Part of the output:
            {
              queryPlanner: {
                winningPlan: { stage: "COLLSCAN", filter: { $expr: { /* ... */ } } }
              },
              executionStats: {
                nReturned: 41250,
                executionTimeMillis: 6840,
                totalKeysExamined: 0,
                totalDocsExamined: 5000000
              }
            }
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed: half-open date range on the raw field (Dhaka month boundaries)",
                    label_bn="Fix: raw field-এর ওপর half-open date range (ঢাকার সময় অনুযায়ী মাসের সীমা)", src=r"""
            // September 2026 in Asia/Dhaka (UTC+6) = [2026-08-31T18:00Z, 2026-09-30T18:00Z)
            db.orders.find({
              createdAt: {
                $gte: ISODate("2026-08-31T18:00:00Z"),
                $lt:  ISODate("2026-09-30T18:00:00Z")
              }
            }).explain("executionStats")

            // Expected plan shape now:
            //   winningPlan: FETCH <- IXSCAN { createdAt: 1 }
            //   totalKeysExamined ≈ totalDocsExamined ≈ nReturned
        """)],
        a_en=r"""
            The explain output says it all: `COLLSCAN`, `totalKeysExamined: 0` and `totalDocsExamined: 5,000,000` to return ~41k documents. The index on `createdAt` is ignored because the query **wraps the field in functions** (`$year`, `$month` inside `$expr`). The index stores raw `createdAt` values, not "year of createdAt", so MongoDB must compute the expression for every document.

            The fix is to make the predicate index-friendly: a **half-open range** on the raw field — `$gte` start of month, `$lt` start of next month. Then the plan becomes `IXSCAN` + `FETCH`, and keys examined ≈ docs examined ≈ nReturned.

            There's also a hidden correctness bug: `$year`/`$month` use **UTC** by default, so the old query covered 1 September 06:00 → 1 October 06:00 Dhaka time: it missed the first six hours of the month and included the first six hours of the next one. The fixed range uses Dhaka month boundaries.
        """,
        a_bn=r"""
            Explain output-ই সব বলে দিচ্ছে: `COLLSCAN`, `totalKeysExamined: 0` আর ~41 হাজার document return করতে `totalDocsExamined: 5,000,000`। `createdAt`-এর index ignore হচ্ছে কারণ query-তে **field-টাকে function-এর ভেতরে মোড়ানো হয়েছে** (`$expr`-এর ভেতরে `$year`, `$month`)। Index-এ raw `createdAt` value store থাকে, "createdAt-এর year" না — তাই MongoDB-কে প্রতিটি document-এর জন্য expression হিসাব করতে হচ্ছে।

            Fix হলো predicate-টাকে index-friendly করা: raw field-এর ওপর একটা **half-open range** — মাসের শুরু থেকে `$gte`, পরের মাসের শুরুর আগ পর্যন্ত `$lt`। তখন plan হয় `IXSCAN` + `FETCH`, আর keys examined ≈ docs examined ≈ nReturned।

            এখানে একটা লুকানো correctness bug-ও আছে: `$year`/`$month` default-ভাবে **UTC** ব্যবহার করে, তাই পুরনো query ঢাকার সময় 1 September সকাল 6টা থেকে 1 October সকাল 6টা পর্যন্ত order গুনছিল: মাসের প্রথম ছয় ঘণ্টা বাদ পড়ছিল, আর পরের মাসের প্রথম ছয় ঘণ্টা ঢুকে যাচ্ছিল। Fix করা range-এ ঢাকার মাসের সীমা ব্যবহার করা হয়েছে।
        """,
        ex_en=r"""
            **How to read `executionStats`:**
            - `stage`: `COLLSCAN` = full collection scan; `IXSCAN` = index scan; `FETCH` = loading documents after the index; a `SORT` stage means an in-memory sort.
            - The ideal ratio is `totalKeysExamined : totalDocsExamined : nReturned ≈ 1 : 1 : 1`. Here it's 0 : 5,000,000 : 41,250 — about 121 documents read for each one returned.
            - `executionTimeMillis` is useful, but compare plans by work done, not just time (cache warmth changes timings).

            **General rule:** keep the indexed field "bare" on one side of the comparison. Expressions like `$toLower: "$email"`, `$year: "$createdAt"` or arithmetic on the field can't use a normal index. If you really need such a filter, store a computed field (e.g. `emailLower`, or a `yearMonth` string) and index that, or use a collation-based index for case-insensitive matching.

            **For reports at scale:** run them on a secondary or analytics node, or keep a pre-aggregated daily summary collection (computed pattern) so the dashboard doesn't scan raw orders at all.
        """,
        ex_bn=r"""
            **`executionStats` কীভাবে পড়বে:**
            - `stage`: `COLLSCAN` = পুরো collection scan; `IXSCAN` = index scan; `FETCH` = index থেকে পাওয়ার পর document load করা; `SORT` stage মানে in-memory sort।
            - আদর্শ অনুপাত হলো `totalKeysExamined : totalDocsExamined : nReturned ≈ 1 : 1 : 1`। এখানে সেটা 0 : 5,000,000 : 41,250 — প্রতিটি result-এর জন্য প্রায় 121টা document পড়া হচ্ছে।
            - `executionTimeMillis` কাজের, কিন্তু plan compare করো কতটা কাজ হচ্ছে তা দিয়ে, শুধু সময় দিয়ে না (cache warm থাকলে সময় বদলে যায়)।

            **সাধারণ নিয়ম:** indexed field-কে comparison-এর এক পাশে "খালি" রাখো। `$toLower: "$email"`, `$year: "$createdAt"` বা field-এর ওপর arithmetic থাকলে সাধারণ index ব্যবহার হয় না। এমন filter সত্যিই দরকার হলে একটা computed field (যেমন `emailLower`, বা `yearMonth` string) store করে সেটায় index দাও, অথবা case-insensitive matching-এর জন্য collation-based index ব্যবহার করো।

            **বড় scale-এ report:** report secondary বা analytics node-এ চালাও, অথবা একটা pre-aggregated daily summary collection রাখো (computed pattern), যাতে dashboard raw order scan-ই না করে।
        """,
        tip_en=r"""Quote the three numbers (keys examined, docs examined, nReturned) and the stage name before proposing a fix — then mention the timezone bug. Spotting a correctness issue while fixing performance impresses interviewers.""",
        tip_bn=r"""Fix বলার আগে তিনটা সংখ্যা (keys examined, docs examined, nReturned) আর stage-এর নাম উল্লেখ করো — তারপর timezone bug-এর কথা বলো। Performance fix করতে গিয়ে correctness-এর সমস্যা ধরতে পারলে interviewer বেশ impressed হয়।""",
        mist_en=r"""Adding `.hint({ createdAt: 1 })` (it would scan the whole index and still evaluate the expression per document), or creating more indexes without changing the query shape.""",
        mist_bn=r"""`.hint({ createdAt: 1 })` যোগ করা (তাতে পুরো index scan হবে আর প্রতিটি document-এ expression তবুও evaluate হবে), অথবা query-র shape না বদলে শুধু আরও index বানানো।""",
        follow=[
            ("How would you make a case-insensitive email lookup use an index?", "Case-insensitive email lookup-এ কীভাবে index ব্যবহার করাবে?"),
            ("What does a `SORT` stage in the winning plan tell you?", "Winning plan-এ `SORT` stage থাকলে সেটা কী বোঝায়?"),
        ],
        related=["mongo-012"],
        refs=[EXPLAIN, EXPR],
    ),
    # ------------------------------------------------------------------ mongo-030
    Q(
        id="mongo-030", sub="Real-World Data Modeling", diff="extreme", type="system-design",
        prio="medium", market="international", mins=20,
        tags=["system-design", "chat", "sharding", "schema-design", "pagination", "unbounded-arrays"],
        ver="Version-independent concept (current: MongoDB 9.0, sharded cluster)", vs=False, status="stable",
        q_en=r"""Design the MongoDB data model, indexes and sharding strategy for a chat feature in a large super-app: ~5 million daily active users, 1:1 and group chats (groups up to 5,000 members), ~300 million messages per day, infinite-scroll message history, a conversation list with unread counts, and safe client retries.""",
        q_bn=r"""একটা বড় super-app-এর chat feature-এর জন্য MongoDB data model, index আর sharding strategy design করো: দিনে ~5 million active user, 1:1 ও group chat (group-এ সর্বোচ্চ 5,000 member), দিনে ~300 million message, infinite-scroll message history, unread count সহ conversation list, আর client-এর retry যেন নিরাপদ হয়।""",
        a_en=r"""
            *(Advanced, senior-level design question.)*

            **Access patterns first:** (1) send a message — ~3,500 writes/s on average with large peaks; (2) load the latest 50 messages of a conversation and scroll back; (3) show a user's conversations sorted by last activity with unread counts.

            **Collections:**
            - `messages` — **one document per message** (`conversationId`, `senderId`, `body`, `attachments`, `createdAt`). Never an array of messages inside the conversation: that's an unbounded array that hits the 16 MB limit and rewrites a huge document on every send.
            - `conversations` — members (bounded), type, and a small `lastMessage` snapshot (extended reference) for list previews.
            - `inbox` — one document per (user, conversation): `lastReadMessageId`, `unreadCount`, `lastActivityAt`, `muted`. Index `{ userId: 1, lastActivityAt: -1 }`.

            **Indexes & pagination:** `{ conversationId: 1, _id: -1 }` on `messages`, and **keyset pagination** (`_id < lastSeenId`, sort `_id: -1`, limit 50) — never `skip()`.

            **Sharding:** shard `messages` on `{ conversationId: "hashed", _id: 1 }`. The hashed prefix spreads conversations evenly (no hot shard from monotonically increasing IDs), queries with a `conversationId` are **targeted** to one shard, and the `_id` suffix lets one huge group's chunk still split. Shard `inbox` on `{ userId: "hashed" }`.

            **Writes & retries:** the API generates the message `_id` once per send and reuses it on retry, so a duplicate fails with E11000 instead of creating a second message (same shard key → same shard, where `_id` is unique). Use `w: "majority"`. Updating `conversations.lastMessage` and members' `inbox` is done asynchronously (queue or change stream) — eventual consistency is fine for previews. For big groups, avoid `$inc` on 5,000 inbox docs per message: compute unread count from `lastReadMessageId` on read (fan-out on read).

            **Beyond MongoDB:** real-time delivery via WebSocket gateways + Redis pub/sub; search via Atlas Search or a separate search engine; archive old messages to cheaper storage.
        """,
        a_bn=r"""
            *(Advanced, senior-level design প্রশ্ন।)*

            **আগে access pattern:** (1) message পাঠানো — গড়ে ~3,500 write/s, peak-এ আরও অনেক বেশি; (2) একটা conversation-এর সর্বশেষ 50টা message load করা আর পেছনে scroll করা; (3) user-এর conversation list, last activity অনুযায়ী sorted, unread count সহ।

            **Collection:**
            - `messages` — **প্রতিটি message-এর জন্য একটা document** (`conversationId`, `senderId`, `body`, `attachments`, `createdAt`)। Conversation-এর ভেতরে message-এর array কখনো না: সেটা unbounded array, 16 MB limit-এ পৌঁছে যায় আর প্রতিবার message পাঠালে একটা বিশাল document rewrite হয়।
            - `conversations` — member (bounded), type, আর list preview-র জন্য ছোট একটা `lastMessage` snapshot (extended reference)।
            - `inbox` — প্রতি (user, conversation)-এর জন্য একটা document: `lastReadMessageId`, `unreadCount`, `lastActivityAt`, `muted`। Index `{ userId: 1, lastActivityAt: -1 }`।

            **Index ও pagination:** `messages`-এ `{ conversationId: 1, _id: -1 }`, আর **keyset pagination** (`_id < lastSeenId`, sort `_id: -1`, limit 50) — কখনো `skip()` না।

            **Sharding:** `messages`-কে `{ conversationId: "hashed", _id: 1 }` দিয়ে shard করো। Hashed prefix conversation-গুলোকে সমানভাবে ছড়িয়ে দেয় (monotonically বাড়তে থাকা ID-র কারণে hot shard হয় না), `conversationId` সহ query একটা shard-এই **targeted** হয়, আর `_id` suffix থাকায় একটা বিশাল group-এর chunk-ও split হতে পারে। `inbox`-কে `{ userId: "hashed" }` দিয়ে shard করো।

            **Write ও retry:** API প্রতিটি send-এর জন্য একবার message-এর `_id` generate করে আর retry-তে সেটাই আবার ব্যবহার করে, ফলে duplicate হলে দ্বিতীয় message তৈরি না হয়ে E11000 আসে (একই shard key → একই shard, যেখানে `_id` unique)। `w: "majority"` ব্যবহার করো। `conversations.lastMessage` আর member-দের `inbox` update asynchronously হয় (queue বা change stream দিয়ে) — preview-র জন্য eventual consistency যথেষ্ট। বড় group-এ প্রতি message-এ 5,000টা inbox doc-এ `$inc` করা এড়াও: read-এর সময় `lastReadMessageId` থেকে unread count হিসাব করো (fan-out on read)।

            **MongoDB-র বাইরে:** real-time delivery-র জন্য WebSocket gateway + Redis pub/sub; search-এর জন্য Atlas Search বা আলাদা search engine; পুরনো message সস্তা storage-এ archive করা।
        """,
        ex_en=r"""
            **Why not shard on `_id` or `createdAt` alone?** Both are monotonically increasing, so with ranged sharding every insert lands in the chunk holding the maximum value → one hot shard takes all writes. Hashing `_id` alone fixes write distribution but makes "latest 50 messages of conversation X" a scatter-gather query across all shards.

            **Why not `{ conversationId: "hashed" }` alone?** All messages of one conversation would share one shard key value, so a very active group creates a chunk that can never split (jumbo chunk). The `_id` suffix gives the balancer split points.

            **Trade-offs to discuss:**
            - Fan-out on write (`$inc` unread for each member) gives cheap reads but explodes for big groups; fan-out on read is the opposite. Many systems use a hybrid by group size.
            - Storage: 300M messages × ~0.5 KB ≈ 150 GB/day before indexes — plan retention, archival (cold tier/online archive) and index size in RAM.
            - Consistency: read history from the primary (or with causal consistency) so a sender always sees their own message.
            - Failure scenarios: a shard primary failover pauses writes for that shard's conversations for seconds — retryable writes and the idempotent `_id` make client retries safe; WebSocket delivery should not depend on the DB write being instantly readable everywhere.
            - Privacy: with end-to-end encryption the server can't do content search; decide that early.
        """,
        ex_bn=r"""
            **শুধু `_id` বা `createdAt` দিয়ে shard কেন না?** দুটোই monotonically বাড়ে, তাই ranged sharding-এ প্রতিটি insert সর্বোচ্চ value-ওয়ালা chunk-এ যায় → একটা hot shard সব write নেয়। শুধু `_id` hash করলে write distribution ঠিক হয়, কিন্তু "conversation X-এর সর্বশেষ 50 message" তখন সব shard-এ scatter-gather query হয়ে যায়।

            **শুধু `{ conversationId: "hashed" }` কেন না?** তখন একটা conversation-এর সব message-এর shard key value একই হবে, ফলে খুব active group-এর chunk কখনো split হতে পারবে না (jumbo chunk)। `_id` suffix balancer-কে split point দেয়।

            **যে trade-off নিয়ে আলোচনা করবে:**
            - Fan-out on write (প্রতিটি member-এর unread-এ `$inc`) read সস্তা করে, কিন্তু বড় group-এ বিস্ফোরিত হয়; fan-out on read ঠিক উল্টো। অনেক system group size অনুযায়ী hybrid ব্যবহার করে।
            - Storage: 300M message × ~0.5 KB ≈ index ছাড়াই দিনে 150 GB — retention, archival (cold tier/online archive) আর RAM-এ index size-এর plan করতে হবে।
            - Consistency: history primary থেকে (বা causal consistency দিয়ে) পড়ো, যাতে sender সবসময় নিজের message দেখতে পায়।
            - Failure scenario: কোনো shard-এর primary failover হলে সেই shard-এর conversation-গুলোর write কয়েক second থেমে থাকে — retryable write আর idempotent `_id` থাকায় client retry নিরাপদ; WebSocket delivery যেন DB write সব জায়গায় সাথে সাথে readable হওয়ার ওপর নির্ভর না করে।
            - Privacy: end-to-end encryption থাকলে server content search করতে পারবে না — এটা শুরুতেই ঠিক করো।
        """,
        tip_en=r"""Start from access patterns and numbers, then justify the shard key against the three criteria (cardinality, frequency, monotonic growth) and query targeting. Explicitly naming what you rejected and why is what distinguishes a senior answer.""",
        tip_bn=r"""Access pattern আর সংখ্যা দিয়ে শুরু করো, তারপর shard key-কে তিনটা criteria (cardinality, frequency, monotonic growth) আর query targeting দিয়ে justify করো। কোন option বাদ দিলে আর কেন — সেটা স্পষ্ট করে বলাই senior-level উত্তরকে আলাদা করে।""",
        mist_en=r"""Embedding messages in the conversation document; offset pagination with `skip()`; sharding on `createdAt`/`_id` ranges; updating thousands of inbox documents synchronously inside a transaction for every message.""",
        mist_bn=r"""Conversation document-এর ভেতরে message embed করা; `skip()` দিয়ে offset pagination; `createdAt`/`_id`-এর range দিয়ে shard করা; প্রতিটি message-এর জন্য একটা transaction-এর ভেতরে হাজার হাজার inbox document synchronously update করা।""",
        code=r"""
            // messages: one document per message
            {
              _id: ObjectId("6709f1c2a1b2c3d4e5f60718"), // generated once per send, reused on retry
              conversationId: ObjectId("66f0a1b2c3d4e5f607182930"),
              senderId: ObjectId("65aa0b1c2d3e4f5061728394"),
              body: "On my way, 10 minutes",
              attachments: [],
              createdAt: ISODate("2026-10-12T09:15:00Z")
            }

            sh.shardCollection("chat.messages", { conversationId: "hashed", _id: 1 })
            db.messages.createIndex({ conversationId: 1, _id: -1 })

            // Infinite scroll: keyset pagination (no skip)
            db.messages.find({ conversationId: convId, _id: { $lt: lastSeenId } })
              .sort({ _id: -1 })
              .limit(50)

            // inbox: one document per (user, conversation)
            sh.shardCollection("chat.inbox", { userId: "hashed" })
            db.inbox.createIndex({ userId: 1, lastActivityAt: -1 })
        """,
        lang="javascript",
        follow=[
            ("How would you show 'seen by' receipts in a 5,000-member group without huge write amplification?", "5,000 member-এর group-এ বিশাল write amplification ছাড়া 'seen by' receipt কীভাবে দেখাবে?"),
            ("A celebrity broadcast channel gets 50x normal traffic. What breaks first and how do you handle it?", "একটা celebrity broadcast channel-এ স্বাভাবিকের 50 গুণ traffic এলে আগে কী ভাঙবে, আর কীভাবে সামলাবে?"),
            ("How would you delete a user's messages for a data-deletion request?", "Data-deletion request এলে একজন user-এর message কীভাবে delete করবে?"),
        ],
        related=["mongo-001", "mongo-003", "mongo-023"],
        refs=[SHARD_KEY, UNBOUNDED, SHARDING],
    ),
]

if __name__ == "__main__":
    save("mongodb", "b1", QUESTIONS)
