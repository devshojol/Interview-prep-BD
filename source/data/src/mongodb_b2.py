# MongoDB — batch 2 (mongo-006, 007, 013, 014, 015, 024, 025, 031)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

QUERY_OPS = ("MongoDB Manual — Query and Projection Operators", "https://www.mongodb.com/docs/manual/reference/operator/query/")
PROJECTION = ("MongoDB Manual — Project Fields to Return from Query", "https://www.mongodb.com/docs/manual/tutorial/project-fields-from-query-results/")
NULL_FIELDS = ("MongoDB Manual — Query for Null or Missing Fields", "https://www.mongodb.com/docs/manual/tutorial/query-for-null-fields/")
LOOKUP = ("MongoDB Manual — $lookup (aggregation)", "https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/")
UNWIND = ("MongoDB Manual — $unwind (aggregation)", "https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/")
ELEMMATCH = ("MongoDB Manual — $elemMatch (query)", "https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/")
ESR = ("MongoDB Manual — The ESR (Equality, Sort, Range) Guideline", "https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-guideline/")
QUERY_OPT = ("MongoDB Manual — Query Optimization (covered queries)", "https://www.mongodb.com/docs/manual/core/query-optimization/")
PIPE_OPT = ("MongoDB Manual — Aggregation Pipeline Optimization", "https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/")
PIPE_LIMITS = ("MongoDB Manual — Aggregation Pipeline Limits", "https://www.mongodb.com/docs/manual/core/aggregation-pipeline-limits/")
FACET = ("MongoDB Manual — $facet (aggregation)", "https://www.mongodb.com/docs/manual/reference/operator/aggregation/facet/")
SHARD_KEY = ("MongoDB Manual — Choose a Shard Key", "https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/")
HASHED = ("MongoDB Manual — Hashed Sharding", "https://www.mongodb.com/docs/manual/core/hashed-sharding/")
RESHARD = ("MongoDB Manual — Reshard a Collection", "https://www.mongodb.com/docs/manual/core/sharding-reshard-a-collection/")
WRITE_CONCERN = ("MongoDB Manual — Write Concern", "https://www.mongodb.com/docs/manual/reference/write-concern/")
ROLLBACK = ("MongoDB Manual — Rollbacks During Replica Set Failover", "https://www.mongodb.com/docs/manual/core/replica-set-rollbacks/")
CAUSAL = ("MongoDB Manual — Read Isolation, Consistency, and Recency", "https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/")

QUESTIONS = [
    # ------------------------------------------------------------------ mongo-006
    Q(
        id="mongo-006", sub="Query Operators & Projection", diff="easy", type="query",
        prio="high", market="bangladesh", mins=3,
        tags=["find", "in", "comparison-operators", "projection", "sort"],
        ver="Version-independent concept (current: MongoDB 9.0, mongosh)", vs=False, status="stable",
        q_en=r"""From the `products` collection below, find products in the "bags" or "electronics" category that are in stock and priced between 1,000 and 4,000 taka (inclusive). Return only `name` and `price` (no `_id`), cheapest first.""",
        q_bn=r"""নিচের `products` collection থেকে "bags" বা "electronics" category-র সেই product-গুলো বের করো যেগুলো stock-এ আছে এবং দাম 1,000 থেকে 4,000 টাকার মধ্যে (দুই প্রান্তসহ)। শুধু `name` আর `price` return করো (`_id` ছাড়া), সবচেয়ে কম দামেরটা আগে।""",
        setup=r"""
            db.products.insertMany([
              { _id: 1, name: "Laptop Bag",  category: "bags",        price: 1800, stock: 12 },
              { _id: 2, name: "Power Bank",  category: "electronics", price: 2200, stock: 0 },
              { _id: 3, name: "Earbuds",     category: "electronics", price: 3500, stock: 25 },
              { _id: 4, name: "Backpack",    category: "bags",        price: 950,  stock: 40 },
              { _id: 5, name: "Smart Watch", category: "wearables",   price: 4200, stock: 8 }
            ])
        """,
        setup_lang="javascript",
        code=r"""
            db.products.find(
              {
                category: { $in: ["bags", "electronics"] },
                stock: { $gt: 0 },
                price: { $gte: 1000, $lte: 4000 }
              },
              { _id: 0, name: 1, price: 1 }
            ).sort({ price: 1 })
        """,
        lang="javascript",
        output=r"""
            [
              { name: 'Laptop Bag', price: 1800 },
              { name: 'Earbuds', price: 3500 }
            ]
        """,
        a_en=r"""
            Fields listed in one filter object are combined with an implicit **AND**. `$in` matches any of the listed categories, `$gt: 0` keeps in-stock items, and `$gte`/`$lte` on the same field form an inclusive range. The second argument is the **projection**: `name: 1, price: 1` includes those fields and `_id: 0` removes `_id`, which is returned by default.

            Walking the data: Power Bank is out of stock, Backpack is below 1,000 and Smart Watch is in another category, so only Laptop Bag (1800) and Earbuds (3500) remain.
        """,
        a_bn=r"""
            একটা filter object-এ যতগুলো field দেওয়া হয়, সেগুলো implicit **AND** দিয়ে যুক্ত হয়। `$in` তালিকার যেকোনো category match করে, `$gt: 0` stock-এ থাকা item রাখে, আর একই field-এ `$gte`/`$lte` মিলে inclusive range তৈরি করে। দ্বিতীয় argument হলো **projection**: `name: 1, price: 1` ওই field-গুলো include করে, আর `_id: 0` `_id` বাদ দেয় — যেটা default-ভাবে আসে।

            Data মিলিয়ে দেখলে: Power Bank stock-এ নেই, Backpack 1,000-এর কম, আর Smart Watch অন্য category-র — তাই শুধু Laptop Bag (1800) আর Earbuds (3500) থাকে।
        """,
        ex_en=r"""
            - **Projection rule:** you can't mix inclusion (`1`) and exclusion (`0`) in one projection — the only exception is `_id`. `{ name: 1, stock: 0 }` throws an error.
            - **`$in` vs `$or`:** for several values of the *same* field, `$in` is simpler and optimises better than `$or`.
            - **Projection saves bandwidth**, not query work: the server still finds the same documents unless the query is fully covered by an index.
            - In the Node.js driver the projection goes in options: `find(filter, { projection: { _id: 0, name: 1, price: 1 } })` or `.project(...)`.
        """,
        ex_bn=r"""
            - **Projection-এর নিয়ম:** একই projection-এ inclusion (`1`) আর exclusion (`0`) মেশানো যায় না — একমাত্র ব্যতিক্রম `_id`। `{ name: 1, stock: 0 }` দিলে error হয়।
            - **`$in` বনাম `$or`:** *একই* field-এর কয়েকটা value-র জন্য `$in` সহজ এবং `$or`-এর চেয়ে ভালো optimise হয়।
            - **Projection bandwidth বাঁচায়**, query-র কাজ না: query পুরোপুরি index দিয়ে covered না হলে server-কে একই document-গুলোই খুঁজতে হয়।
            - Node.js driver-এ projection options-এ যায়: `find(filter, { projection: { _id: 0, name: 1, price: 1 } })` অথবা `.project(...)`।
        """,
        tip_en=r"""Walk through why each excluded document fails a condition — it shows you can verify a query against data, which is exactly what a written test checks.""",
        tip_bn=r"""বাদ পড়া প্রতিটি document কোন condition-এ fail করছে সেটা ব্যাখ্যা করো — এতে বোঝা যায় তুমি data দেখে query verify করতে পারো, written test-এ ঠিক এটাই যাচাই করা হয়।""",
        mist_en=r"""Writing `price: { $gte: 1000 }, price: { $lte: 4000 }` as two keys (the second silently overwrites the first in a JS object), or forgetting that `_id` is returned unless excluded.""",
        mist_bn=r"""`price: { $gte: 1000 }, price: { $lte: 4000 }` দুইটা আলাদা key হিসেবে লেখা (JS object-এ দ্বিতীয়টা চুপচাপ প্রথমটাকে overwrite করে), অথবা ভুলে যাওয়া যে exclude না করলে `_id` সবসময় আসে।""",
        follow=[
            ("How would you find products whose name contains 'bag', case-insensitively? Can it use an index?", "যেসব product-এর name-এ 'bag' আছে (case-insensitive), সেগুলো কীভাবে খুঁজবে? এতে কি index ব্যবহার হবে?"),
            ("How do you paginate this result efficiently?", "এই result দক্ষভাবে paginate করবে কীভাবে?"),
        ],
        related=["mongo-004"],
        refs=[QUERY_OPS, PROJECTION],
    ),
    # ------------------------------------------------------------------ mongo-007
    Q(
        id="mongo-007", sub="Query Operators & Projection", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=1,
        tags=["null", "exists", "type", "query-operators"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""The `users` collection contains the three documents below. How many documents does `db.users.find({ phone: null })` return?""",
        q_bn=r"""`users` collection-এ নিচের তিনটা document আছে। `db.users.find({ phone: null })` কয়টা document return করবে?""",
        code=r"""
            { _id: 1, name: "Rafi",   phone: "01711000000" }
            { _id: 2, name: "Mitu",   phone: null }
            { _id: 3, name: "Tanvir" }
        """,
        lang="javascript",
        options=[
            ("1 — only Mitu, because only her `phone` is explicitly null", "1 — শুধু Mitu, কারণ শুধু তার `phone` explicitly null"),
            ("2 — Mitu and Tanvir, because `null` matches both null values and missing fields", "2 — Mitu আর Tanvir, কারণ `null` null value আর missing field দুটোই match করে"),
            ("0 — you must use `$exists` to query null values", "0 — null value query করতে `$exists` ব্যবহার করতেই হবে"),
            ("3 — a null condition is ignored, so every document matches", "3 — null condition ignore হয়, তাই সব document match করে"),
        ],
        correct=1,
        a_en=r"""`{ phone: null }` matches documents where `phone` is **null or does not exist**, so it returns Mitu and Tanvir (2 documents).""",
        a_bn=r"""`{ phone: null }` সেই document-গুলো match করে যেখানে `phone` **null অথবা field-টাই নেই** — তাই Mitu আর Tanvir, মোট 2টা document আসে।""",
        ex_en=r"""
            The tempting answer is "1 — only Mitu", which is what SQL's `IS NULL` intuition suggests. To be precise in MongoDB:

            - Only explicit null: `{ phone: { $type: "null" } }`
            - Only missing field: `{ phone: { $exists: false } }`
            - Field present (even if null): `{ phone: { $exists: true } }`

            This matters for data clean-up scripts and for sparse/partial indexes, where "missing" and "null" are treated differently.
        """,
        ex_bn=r"""
            সবচেয়ে বিভ্রান্তিকর উত্তর হলো "1 — শুধু Mitu" — SQL-এর `IS NULL`-এর অভ্যাস থেকে এটাই মনে হয়। MongoDB-তে নির্দিষ্টভাবে চাইলে:

            - শুধু explicit null: `{ phone: { $type: "null" } }`
            - শুধু missing field: `{ phone: { $exists: false } }`
            - Field আছে (null হলেও): `{ phone: { $exists: true } }`

            Data clean-up script আর sparse/partial index-এ এটা গুরুত্বপূর্ণ, কারণ সেখানে "missing" আর "null" আলাদাভাবে ধরা হয়।
        """,
        tip_en=r"""After answering, give the `$type: "null"` and `$exists: false` alternatives — it turns a trivia answer into a practical one.""",
        tip_bn=r"""উত্তর দেওয়ার পর `$type: "null"` আর `$exists: false`-এর বিকল্পগুলোও বলো — এতে একটা trivia উত্তর practical উত্তরে পরিণত হয়।""",
        follow=[
            ("How does a unique index treat documents that are missing the indexed field?", "Unique index সেই document-গুলোকে কীভাবে treat করে, যেগুলোতে indexed field-টাই নেই?"),
        ],
        related=["mongo-006"],
        refs=[NULL_FIELDS, QUERY_OPS],
    ),
    # ------------------------------------------------------------------ mongo-013
    Q(
        id="mongo-013", sub="Aggregation Pipelines", diff="medium", type="query",
        prio="high", market="both", mins=5,
        tags=["lookup", "unwind", "join", "aggregation", "ifnull"],
        ver="Version-independent (MongoDB 3.6+; current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""Return every **delivered** order together with the customer's name and city as flat documents `{ orderId, total, customer, city }`, sorted by `orderId`. Note that order 104 points to a customer that no longer exists — it must still appear, with "Unknown" for name and city.""",
        q_bn=r"""প্রতিটি **delivered** order-কে customer-এর name আর city সহ flat document `{ orderId, total, customer, city }` আকারে return করো, `orderId` অনুযায়ী sort করে। খেয়াল করো, order 104 এমন একজন customer-কে point করছে যে আর নেই — তবুও সেটা result-এ আসতে হবে, name আর city হিসেবে "Unknown" দিয়ে।""",
        setup=r"""
            db.customers.insertMany([
              { _id: "c1", name: "Rahim", city: "Dhaka" },
              { _id: "c2", name: "Karim", city: "Sylhet" },
              { _id: "c3", name: "Sumi",  city: "Khulna" }
            ])

            db.orders.insertMany([
              { _id: 101, customerId: "c1", total: 450, status: "delivered" },
              { _id: 102, customerId: "c2", total: 100, status: "delivered" },
              { _id: 103, customerId: "c1", total: 400, status: "cancelled" },
              { _id: 104, customerId: "c9", total: 700, status: "delivered" }
            ])
        """,
        setup_lang="javascript",
        code=r"""
            db.orders.aggregate([
              { $match: { status: "delivered" } },
              { $lookup: {
                  from: "customers",
                  localField: "customerId",
                  foreignField: "_id",
                  as: "customer"
              } },
              { $unwind: { path: "$customer", preserveNullAndEmptyArrays: true } },
              { $project: {
                  _id: 0,
                  orderId: "$_id",
                  total: "$total",
                  customer: { $ifNull: ["$customer.name", "Unknown"] },
                  city: { $ifNull: ["$customer.city", "Unknown"] }
              } },
              { $sort: { orderId: 1 } }
            ])
        """,
        lang="javascript",
        output=r"""
            [
              { orderId: 101, total: 450, customer: 'Rahim', city: 'Dhaka' },
              { orderId: 102, total: 100, customer: 'Karim', city: 'Sylhet' },
              { orderId: 104, total: 700, customer: 'Unknown', city: 'Unknown' }
            ]
        """,
        a_en=r"""
            `$lookup` performs a **left outer join**: for each order it adds a `customer` **array** with the matching customer documents (empty if none). `$unwind` turns that one-element array into an embedded object so we can read `customer.name`.

            The key detail is `preserveNullAndEmptyArrays: true`. A plain `$unwind: "$customer"` **drops** documents whose array is empty, so order 104 would silently disappear. With the option, 104 is kept without a `customer` field, and `$ifNull` fills in "Unknown". Order 103 is removed by the initial `$match` because it's cancelled.
        """,
        a_bn=r"""
            `$lookup` একটা **left outer join** করে: প্রতিটি order-এ matching customer document-গুলো নিয়ে একটা `customer` **array** যোগ করে (match না থাকলে খালি array)। `$unwind` সেই এক-element-এর array-কে embedded object বানায়, যাতে `customer.name` পড়া যায়।

            আসল বিষয় হলো `preserveNullAndEmptyArrays: true`। সাধারণ `$unwind: "$customer"` খালি array-ওয়ালা document **বাদ দিয়ে দেয়**, ফলে order 104 চুপচাপ হারিয়ে যেত। এই option দিলে 104 থাকে (`customer` field ছাড়া), আর `$ifNull` সেখানে "Unknown" বসায়। Order 103 cancelled হওয়ায় শুরুর `$match`-এই বাদ পড়ে।
        """,
        ex_en=r"""
            - **Performance:** `$lookup` runs a query on `customers` for each input document, so filter first (`$match`) and make sure `foreignField` is indexed (`_id` always is). For large reports, join after `$sort` + `$limit` whenever possible.
            - **Pipeline form:** when you need extra join conditions or want to fetch only some fields, use `$lookup` with `pipeline` (since MongoDB 5.0 it can be combined with `localField`/`foreignField`), e.g. `pipeline: [{ $project: { name: 1, city: 1 } }]`.
            - **Data modelling alternative:** if every order screen needs the customer name, store a small snapshot (`customer: { _id, name }`) in the order — the extended reference pattern — and avoid the join entirely.
            - **Orphans:** order 104 shows a referential-integrity gap; MongoDB has no foreign keys, so the application (or a periodic check) must handle deletes.
        """,
        ex_bn=r"""
            - **Performance:** `$lookup` প্রতিটি input document-এর জন্য `customers`-এ একটা query চালায়, তাই আগে `$match` দিয়ে filter করো আর নিশ্চিত করো `foreignField`-এ index আছে (`_id`-এ সবসময় থাকে)। বড় report-এ সম্ভব হলে `$sort` + `$limit`-এর পরে join করো।
            - **Pipeline form:** বাড়তি join condition লাগলে বা কিছু field শুধু আনতে চাইলে `pipeline` সহ `$lookup` ব্যবহার করো (MongoDB 5.0 থেকে এটা `localField`/`foreignField`-এর সাথেও মেলানো যায়), যেমন `pipeline: [{ $project: { name: 1, city: 1 } }]`।
            - **Data modelling-এর বিকল্প:** প্রতিটি order screen-এ যদি customer-এর নাম লাগে, তাহলে order-এর ভেতরেই ছোট একটা snapshot (`customer: { _id, name }`) রাখো — extended reference pattern — তাহলে join-ই লাগবে না।
            - **Orphan data:** order 104 referential integrity-র একটা ফাঁক দেখায়; MongoDB-তে foreign key নেই, তাই delete-এর ব্যাপারটা application (বা periodic check) সামলাতে হয়।
        """,
        tip_en=r"""Call out the `$unwind` data-loss trap before the interviewer asks — it's the most common real bug with `$lookup` reports ("why are some orders missing from the export?").""",
        tip_bn=r"""Interviewer জিজ্ঞেস করার আগেই `$unwind`-এর data হারানোর ফাঁদটা উল্লেখ করো — `$lookup` report-এ এটাই সবচেয়ে common বাস্তব bug ("export-এ কিছু order নেই কেন?")।""",
        mist_en=r"""Expecting `$lookup` to return a single object instead of an array; using plain `$unwind` and losing unmatched rows; running `$lookup` on the whole collection before `$match`.""",
        mist_bn=r"""`$lookup` থেকে array-র বদলে single object আশা করা; সাধারণ `$unwind` ব্যবহার করে match-না-হওয়া row হারানো; `$match`-এর আগেই পুরো collection-এ `$lookup` চালানো।""",
        follow=[
            ("How would you return each customer with an array of only their last 3 orders?", "প্রতিটি customer-এর সাথে শুধু তার শেষ 3টা order-এর array কীভাবে return করবে?"),
            ("When would you embed the customer data in the order instead of using `$lookup`?", "কখন `$lookup` ব্যবহার না করে order-এর ভেতরে customer data embed করবে?"),
        ],
        related=["mongo-012"],
        refs=[LOOKUP, UNWIND],
    ),
    # ------------------------------------------------------------------ mongo-014
    Q(
        id="mongo-014", sub="Query Operators & Projection", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["elemmatch", "arrays", "embedded-documents", "query-operators"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""Given these `orders`, which documents does the first query return — and which query returns only orders where **a single item** has SKU "A" with `qty ≥ 5`?""",
        q_bn=r"""নিচের `orders` থেকে প্রথম query কোন document-গুলো return করবে — আর কোন query শুধু সেই order-গুলো return করবে যেখানে **একটাই item**-এর SKU "A" এবং `qty ≥ 5`?""",
        code=r"""
            // Data
            { _id: 1, items: [ { sku: "A", qty: 1 }, { sku: "B", qty: 10 } ] }
            { _id: 2, items: [ { sku: "A", qty: 7 } ] }
            { _id: 3, items: [ { sku: "B", qty: 2 } ] }

            // Query 1
            db.orders.find({ "items.sku": "A", "items.qty": { $gte: 5 } })
        """,
        lang="javascript",
        options=[
            (r"""Only `_id: 2` — dotted conditions on the same array already apply to the same element""",
             r"""শুধু `_id: 2` — একই array-তে dotted condition দিলে সেগুলো এমনিতেই একই element-এ apply হয়"""),
            (r"""`_id: 1` and `_id: 2`; use `{ items: { sku: "A", qty: { $gte: 5 } } }` to get only `_id: 2`""",
             r"""`_id: 1` আর `_id: 2`; শুধু `_id: 2` পেতে `{ items: { sku: "A", qty: { $gte: 5 } } }` ব্যবহার করতে হবে"""),
            (r"""`_id: 1`, `2` and `3`; use `$all` to force both conditions onto one element""",
             r"""`_id: 1`, `2` আর `3`; দুইটা condition একই element-এ আনতে `$all` ব্যবহার করতে হবে"""),
            (r"""`_id: 1` and `_id: 2`; use `{ items: { $elemMatch: { sku: "A", qty: { $gte: 5 } } } }` to get only `_id: 2`""",
             r"""`_id: 1` আর `_id: 2`; শুধু `_id: 2` পেতে `{ items: { $elemMatch: { sku: "A", qty: { $gte: 5 } } } }` ব্যবহার করতে হবে"""),
        ],
        correct=3,
        a_en=r"""Query 1 returns `_id: 1` and `_id: 2`. Separate dotted conditions on an array can be satisfied by **different elements**: in order 1, item A satisfies the SKU condition and item B satisfies `qty ≥ 5`. `$elemMatch` requires one element to satisfy all conditions, so it returns only `_id: 2`.""",
        a_bn=r"""Query 1 `_id: 1` আর `_id: 2` return করে। Array-র ওপর আলাদা dotted condition **ভিন্ন ভিন্ন element** দিয়ে পূরণ হতে পারে: order 1-এ item A SKU condition পূরণ করে আর item B `qty ≥ 5` পূরণ করে। `$elemMatch` চায় একটাই element সব condition পূরণ করুক, তাই সেটা শুধু `_id: 2` return করে।""",
        ex_en=r"""
            Option B is the subtle trap: `{ items: { sku: "A", qty: { $gte: 5 } } }` is an **exact embedded-document match**. MongoDB looks for an array element exactly equal to `{ sku: "A", qty: { $gte: 5 } }` (same fields, same order, and `$gte` treated as a literal field name), so it matches nothing.

            Option A is the common misconception; it's only true with `$elemMatch`. `$all` matches arrays that contain all listed values, which doesn't solve the per-element problem. Indexes on `items.sku` / `items.qty` are **multikey** indexes and work with `$elemMatch`.
        """,
        ex_bn=r"""
            Option B হলো সূক্ষ্ম ফাঁদ: `{ items: { sku: "A", qty: { $gte: 5 } } }` হলো একটা **exact embedded-document match**। MongoDB এমন array element খোঁজে যেটা হুবহু `{ sku: "A", qty: { $gte: 5 } }`-এর সমান (একই field, একই order, আর `$gte` তখন literal field name হিসেবে ধরা হয়) — তাই কিছুই match করে না।

            Option A হলো common ভুল ধারণা; এটা শুধু `$elemMatch` দিলেই সত্য। `$all` সেই array match করে যেখানে তালিকার সব value আছে — এতে per-element সমস্যার সমাধান হয় না। `items.sku` / `items.qty`-এর index হলো **multikey** index, আর এগুলো `$elemMatch`-এর সাথে কাজ করে।
        """,
        tip_en=r"""Explain with the concrete document `_id: 1` — showing which element satisfies which condition is the clearest proof that you understand array matching.""",
        tip_bn=r"""`_id: 1` document দিয়ে ব্যাখ্যা করো — কোন element কোন condition পূরণ করছে সেটা দেখালেই সবচেয়ে স্পষ্টভাবে প্রমাণ হয় তুমি array matching বোঝো।""",
        follow=[
            ("How do you return only the matching array element in the projection?", "Projection-এ শুধু matching array element-টা কীভাবে return করবে?"),
        ],
        related=["mongo-006"],
        refs=[ELEMMATCH, QUERY_OPS],
    ),
    # ------------------------------------------------------------------ mongo-015
    Q(
        id="mongo-015", sub="Compound Indexes (ESR)", diff="medium", type="scenario",
        prio="high", market="both", mins=6,
        tags=["compound-index", "esr", "sort", "covered-query", "indexes"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""A marketplace seller dashboard lists a shop's **paid** orders worth at least 1,000 taka, newest first, 20 per page. A teammate created `{ shopId: 1, status: 1, total: 1, createdAt: -1 }` but the page is still slow for big shops. Which compound index would you create, and why?""",
        q_bn=r"""একটা marketplace-এর seller dashboard একটা shop-এর **paid** order দেখায়, যেগুলোর মূল্য কমপক্ষে 1,000 টাকা — নতুনগুলো আগে, প্রতি page-এ 20টা। একজন teammate `{ shopId: 1, status: 1, total: 1, createdAt: -1 }` index বানিয়েছে, কিন্তু বড় shop-এর জন্য page এখনো slow। তুমি কোন compound index বানাবে, আর কেন?""",
        a_en=r"""
            I'd follow the **ESR guideline — Equality, Sort, Range**: `{ shopId: 1, status: 1, createdAt: -1, total: 1 }`.

            - **Equality** fields (`shopId`, `status`) go first; they narrow the index to one contiguous section.
            - **Sort** field (`createdAt`) comes next, so within that section the keys are already in the order we want. MongoDB walks the index newest-first, checks `total` on the index key, and **stops after 20 matches** — no in-memory sort.
            - **Range** field (`total`) goes last.

            With the teammate's index (E-R-S), the range on `total` splits the section into many `total` values, each with its own `createdAt` ordering. The keys are no longer in global `createdAt` order, so MongoDB must read **all** matching keys and do a blocking in-memory `SORT` before it can apply `limit(20)`. That's what's slow for big shops.

            I'd confirm with `explain("executionStats")`: no `SORT` stage, and `totalKeysExamined` close to 20 (a bit more if many recent orders are under 1,000 — their keys are examined and skipped).
        """,
        a_bn=r"""
            আমি **ESR guideline — Equality, Sort, Range** মেনে চলব: `{ shopId: 1, status: 1, createdAt: -1, total: 1 }`।

            - **Equality** field (`shopId`, `status`) প্রথমে; এগুলো index-কে একটা ধারাবাহিক অংশে সীমিত করে।
            - এরপর **Sort** field (`createdAt`), যাতে ওই অংশের ভেতরে key-গুলো আগে থেকেই আমাদের চাওয়া order-এ থাকে। MongoDB index-টা newest-first ধরে হাঁটে, index key থেকেই `total` check করে, আর **20টা match পেলেই থেমে যায়** — in-memory sort লাগে না।
            - **Range** field (`total`) সবার শেষে।

            Teammate-এর index (E-R-S)-এ `total`-এর range অংশটাকে অনেকগুলো `total` value-তে ভাগ করে ফেলে, প্রতিটির নিজস্ব `createdAt` ordering থাকে। তখন key-গুলো সামগ্রিকভাবে `createdAt` order-এ থাকে না, ফলে `limit(20)` apply করার আগে MongoDB-কে matching **সব** key পড়ে একটা blocking in-memory `SORT` করতে হয়। বড় shop-এ এটাই slow।

            আমি `explain("executionStats")` দিয়ে নিশ্চিত হব: কোনো `SORT` stage নেই, আর `totalKeysExamined` 20-এর কাছাকাছি (সাম্প্রতিক অনেক order 1,000-এর কম হলে একটু বেশি — সেগুলোর key examine হয়ে skip হয়)।
        """,
        ex_en=r"""
            - **Exception:** if the range is extremely selective (e.g. only a handful of orders above the threshold), E-R-S can examine fewer keys than E-S-R even with an in-memory sort of a tiny result. Measure with `explain` on realistic data.
            - **Prefixes:** the same index also serves queries on `{ shopId }` and `{ shopId, status }`, so you may be able to drop older single-field indexes. Every extra index costs RAM and slows writes.
            - **Sort direction:** for a single sort field the direction doesn't matter (indexes can be walked backwards); for multi-field sorts the relative directions must match the index or its exact reverse.
            - **Covered query:** if the page only needs indexed fields, project them and exclude `_id` — e.g. `{ _id: 0, createdAt: 1, total: 1 }`. Then the plan shows `PROJECTION_COVERED` and `totalDocsExamined: 0`. Multikey (array) fields can't be covered.
        """,
        ex_bn=r"""
            - **ব্যতিক্রম:** range যদি অত্যন্ত selective হয় (যেমন threshold-এর ওপরে মাত্র কয়েকটা order), তাহলে ছোট result-এর in-memory sort থাকলেও E-R-S, E-S-R-এর চেয়ে কম key examine করতে পারে। বাস্তব data-তে `explain` দিয়ে মেপে দেখো।
            - **Prefix:** একই index `{ shopId }` আর `{ shopId, status }` query-ও serve করে, তাই পুরনো single-field index হয়তো drop করা যাবে। প্রতিটি বাড়তি index RAM খায় আর write slow করে।
            - **Sort direction:** একটা sort field হলে direction কোনো ব্যাপার না (index উল্টো দিকেও হাঁটা যায়); কয়েকটা field-এ sort হলে আপেক্ষিক direction index-এর সাথে বা তার ঠিক উল্টোটার সাথে মিলতে হবে।
            - **Covered query:** page-এ যদি শুধু indexed field লাগে, সেগুলো project করো আর `_id` বাদ দাও — যেমন `{ _id: 0, createdAt: 1, total: 1 }`। তখন plan-এ `PROJECTION_COVERED` আর `totalDocsExamined: 0` দেখাবে। Multikey (array) field cover করা যায় না।
        """,
        tip_en=r"""Name the guideline (ESR), then explain *why* sort-before-range avoids the in-memory sort. Ending with "and I'd verify with explain" signals production habits.""",
        tip_bn=r"""Guideline-এর নাম (ESR) বলো, তারপর ব্যাখ্যা করো *কেন* range-এর আগে sort রাখলে in-memory sort এড়ানো যায়। শেষে "আর আমি explain দিয়ে verify করব" বললে production-এর অভ্যাস বোঝা যায়।""",
        mist_en=r"""Ordering index fields the same way as they appear in the query; creating one single-field index per field and expecting MongoDB to combine them efficiently.""",
        mist_bn=r"""Query-তে field যে ক্রমে লেখা আছে index-এও সেই ক্রমে রাখা; প্রতিটি field-এর জন্য আলাদা single-field index বানিয়ে আশা করা যে MongoDB সেগুলো দক্ষভাবে মিলিয়ে নেবে।""",
        code=r"""
            // Query
            db.orders.find({ shopId: shopId, status: "paid", total: { $gte: 1000 } })
              .sort({ createdAt: -1 })
              .limit(20)

            // Equality → Sort → Range
            db.orders.createIndex({ shopId: 1, status: 1, createdAt: -1, total: 1 })

            // Verify: no SORT stage, totalKeysExamined close to nReturned
            db.orders.find({ shopId: shopId, status: "paid", total: { $gte: 1000 } })
              .sort({ createdAt: -1 })
              .limit(20)
              .explain("executionStats")
        """,
        lang="javascript",
        follow=[
            ("How would you make this query covered, and how do you see that in explain?", "এই query-কে কীভাবে covered করবে, আর explain-এ সেটা কীভাবে বুঝবে?"),
            ("How many indexes are too many on a write-heavy collection?", "Write-heavy collection-এ কতগুলো index হলে বেশি হয়ে যায়?"),
        ],
        related=["mongo-023", "mongo-006"],
        refs=[ESR, QUERY_OPT],
    ),
    # ------------------------------------------------------------------ mongo-024
    Q(
        id="mongo-024", sub="Aggregation Performance", diff="hard", type="debugging",
        prio="high", market="both", mins=10,
        tags=["aggregation", "performance", "facet", "lookup", "memory-limit", "pagination"],
        ver="MongoDB 9.0 (per-operation memory limit); concepts apply to 5.0+", vs=True, status="stable",
        q_en=r"""An admin dashboard runs the pipeline below on ~8 million orders to show "the 20 most recent delivered orders of 5,000+ taka from Dhaka customers, plus a total count". It takes 15+ seconds, and after upgrading to MongoDB 9.0 it sometimes fails with a memory-limit error. How would you optimise it?""",
        q_bn=r"""একটা admin dashboard প্রায় 8 million order-এর ওপর নিচের pipeline চালায়, "ঢাকার customer-দের 5,000+ টাকার সর্বশেষ 20টা delivered order, সাথে total count" দেখানোর জন্য। এতে 15+ second লাগে, আর MongoDB 9.0-তে upgrade করার পর মাঝে মাঝে memory-limit error দিয়ে fail করে। তুমি এটা কীভাবে optimise করবে?""",
        code=r"""
            db.orders.aggregate([
              { $lookup: { from: "customers", localField: "customerId",
                           foreignField: "_id", as: "customer" } },
              { $unwind: "$customer" },
              { $match: { status: "delivered", total: { $gte: 5000 },
                          "customer.city": "Dhaka" } },
              { $sort: { createdAt: -1 } },
              { $facet: {
                  data: [ { $skip: 0 }, { $limit: 20 } ],
                  totalCount: [ { $count: "n" } ]
              } }
            ])
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Optimised version", label_bn="Optimise করা version", src=r"""
            // Assumption confirmed with the product team: "Dhaka" = delivery city,
            // which is stored on the order at checkout (extended reference).
            db.orders.createIndex({ status: 1, "shipping.city": 1, createdAt: -1, total: 1 })

            const filter = { status: "delivered", "shipping.city": "Dhaka", total: { $gte: 5000 } };

            // Page: filter + sort + limit first, then join only 20 documents
            db.orders.aggregate([
              { $match: filter },
              { $sort: { createdAt: -1 } },
              { $limit: 20 },
              { $lookup: {
                  from: "customers",
                  localField: "customerId",
                  foreignField: "_id",
                  pipeline: [ { $project: { name: 1, phone: 1 } } ],
                  as: "customer"
              } },
              { $unwind: { path: "$customer", preserveNullAndEmptyArrays: true } }
            ])

            // Count separately (index-backed); cache it for a minute or show "50,000+"
            db.orders.countDocuments(filter)
        """)],
        a_en=r"""
            **Clarify first:** does "Dhaka customers" mean the customer's current city or the order's delivery city? For an orders dashboard it's usually the delivery city, which belongs on the order anyway.

            **What's wrong:**
            1. `$lookup` + `$unwind` run for **all 8M orders** before any filtering. Only stages at the start of a pipeline can use indexes, and the city filter depends on joined data.
            2. `$sort` on millions of joined documents is a blocking in-memory sort (100 MB per stage, then spilling to disk).
            3. `$facet` receives the entire sorted set; its sub-pipelines **can't use indexes**, and `$count` walks every document just to show a number.
            4. On MongoDB 9.0 the whole operation is also subject to the new **per-operation memory limit** (by default the greater of 1 GB or 20% of the server's memory), so this pipeline can now fail outright.

            **Fix:**
            - Store `shipping.city` on the order (extended reference) so the filter needs no join.
            - Create an ESR index `{ status: 1, "shipping.city": 1, createdAt: -1, total: 1 }`.
            - Put `$match` → `$sort` → `$limit` first; `$sort` + `$limit` coalesce into a top-20 sort, and with the index there's no in-memory sort at all.
            - `$lookup` **after** the limit — 20 lookups instead of 8 million — using the pipeline form to fetch only needed fields.
            - Get the count with a separate `countDocuments(filter)` that uses the index, and cache it (or show "50,000+").
        """,
        a_bn=r"""
            **আগে প্রশ্ন পরিষ্কার করো:** "ঢাকার customer" মানে কি customer-এর বর্তমান city, নাকি order-এর delivery city? Order dashboard-এ সাধারণত delivery city বোঝায়, আর সেটা এমনিতেই order-এ থাকা উচিত।

            **সমস্যা কোথায়:**
            1. কোনো filter-এর আগেই **8M order-এর সবগুলোর** জন্য `$lookup` + `$unwind` চলছে। শুধু pipeline-এর শুরুর stage index ব্যবহার করতে পারে, আর city filter join করা data-র ওপর নির্ভরশীল।
            2. লক্ষ লক্ষ join করা document-এ `$sort` একটা blocking in-memory sort (প্রতি stage-এ 100 MB, তারপর disk-এ spill)।
            3. `$facet` পুরো sorted set পায়; এর sub-pipeline **index ব্যবহার করতে পারে না**, আর শুধু একটা সংখ্যা দেখাতে `$count` প্রতিটি document পার হয়।
            4. MongoDB 9.0-তে পুরো operation-টা নতুন **per-operation memory limit**-এর অধীনেও পড়ে (default-ভাবে 1 GB বা server memory-র 20% — যেটা বড়), তাই এই pipeline এখন সরাসরি fail করতে পারে।

            **Fix:**
            - Order-এ `shipping.city` store করো (extended reference), যাতে filter-এর জন্য join না লাগে।
            - ESR index বানাও: `{ status: 1, "shipping.city": 1, createdAt: -1, total: 1 }`।
            - শুরুতে `$match` → `$sort` → `$limit`; `$sort` + `$limit` মিলে top-20 sort হয়, আর index থাকায় in-memory sort-ই লাগে না।
            - Limit-এর **পরে** `$lookup` — 8 million-এর বদলে 20টা lookup — pipeline form দিয়ে শুধু দরকারি field আনো।
            - Count আলাদা `countDocuments(filter)` দিয়ে নাও, যেটা index ব্যবহার করে, আর সেটা cache করো (অথবা "50,000+" দেখাও)।
        """,
        ex_en=r"""
            - **Optimizer vs you:** the aggregation optimizer can reorder some stages (e.g. move parts of a `$match` earlier, coalesce `$sort` + `$limit`), but it can't move a filter on joined fields before the join. Write the efficient order explicitly and confirm with `explain()`.
            - **`$facet` pagination** is popular in MERN tutorials because it returns data + count in one call, but it's only fine for small filtered sets. Its single output document is also capped at 16 MB.
            - **Deep pages:** `$skip` gets slower the deeper you go; for "next page" use keyset pagination (`createdAt`/`_id` of the last row).
            - **`allowDiskUse`** lets blocking stages spill, but it treats the symptom; reducing the data early fixes the cause and keeps the operation under the 9.0 per-operation limit.
            - **Isolation:** heavy analytics can run on a secondary or an analytics node so they don't compete with checkout traffic on the primary.
        """,
        ex_bn=r"""
            - **Optimizer বনাম তুমি:** aggregation optimizer কিছু stage-এর order বদলাতে পারে (যেমন `$match`-এর অংশ আগে আনা, `$sort` + `$limit` coalesce করা), কিন্তু join করা field-এর filter join-এর আগে আনতে পারে না। দক্ষ order-টা নিজে লেখো আর `explain()` দিয়ে নিশ্চিত হও।
            - **`$facet` দিয়ে pagination** MERN tutorial-এ জনপ্রিয়, কারণ এক call-এ data + count দুটোই আসে — কিন্তু এটা শুধু ছোট filtered set-এর জন্য ঠিক আছে। এর single output document-ও 16 MB-তে সীমাবদ্ধ।
            - **Deep page:** যত গভীর page, `$skip` তত slow; "next page"-এর জন্য keyset pagination ব্যবহার করো (শেষ row-এর `createdAt`/`_id`)।
            - **`allowDiskUse`** blocking stage-কে spill করতে দেয়, কিন্তু এটা শুধু লক্ষণের চিকিৎসা; শুরুতেই data কমানোই আসল সমাধান, আর এতে operation 9.0-এর per-operation limit-এর মধ্যে থাকে।
            - **Isolation:** ভারী analytics secondary বা analytics node-এ চালাও, যাতে primary-তে checkout traffic-এর সাথে প্রতিযোগিতা না করে।
        """,
        tip_en=r"""Structure it as: clarify the requirement → list the bottlenecks in pipeline order → fix → how you'd verify (explain, timings). Mentioning the 9.0 per-operation memory limit shows you track current releases.""",
        tip_bn=r"""এভাবে সাজাও: requirement পরিষ্কার করা → pipeline-এর ক্রম ধরে bottleneck-গুলো বলা → fix → কীভাবে verify করবে (explain, timing)। 9.0-এর per-operation memory limit-এর কথা বললে বোঝা যায় তুমি current release-এর খোঁজ রাখো।""",
        mist_en=r"""Just adding `allowDiskUse: true` or more RAM; adding an index on `customer.city` (a field that only exists after the join, so no index can help).""",
        mist_bn=r"""শুধু `allowDiskUse: true` বা বেশি RAM যোগ করা; `customer.city`-তে index বানানো (এই field শুধু join-এর পরেই তৈরি হয়, তাই কোনো index কাজে আসে না)।""",
        follow=[
            ("The customer's city can change — what are the trade-offs of storing it on the order?", "Customer-এর city বদলাতে পারে — order-এ সেটা store করার trade-off কী?"),
            ("How would you build an 'orders per day for the last 90 days' chart without scanning raw orders on every page load?", "প্রতিবার page load-এ raw order scan না করে 'গত 90 দিনের প্রতিদিনের order' chart কীভাবে বানাবে?"),
        ],
        related=["mongo-013", "mongo-015", "mongo-023"],
        refs=[PIPE_OPT, PIPE_LIMITS, FACET],
    ),
    # ------------------------------------------------------------------ mongo-025
    Q(
        id="mongo-025", sub="Sharding & Shard Keys", diff="hard", type="mcq",
        prio="medium", market="international", mins=2,
        tags=["sharding", "shard-key", "hot-shard", "monotonic", "hashed"],
        ver="Version-independent concept (current: MongoDB 9.0)", vs=False, status="stable",
        q_en=r"""An `events` collection is sharded with a **ranged** shard key `{ createdAt: 1 }`, and the app inserts about 20,000 events per second. What is the most likely problem?""",
        q_bn=r"""একটা `events` collection **ranged** shard key `{ createdAt: 1 }` দিয়ে shard করা, আর app প্রতি second-এ প্রায় 20,000 event insert করে। সবচেয়ে সম্ভাব্য সমস্যা কী?""",
        options=[
            ("New inserts all go to the chunk holding the highest `createdAt` values, so one shard takes almost all writes",
             "সব নতুন insert সর্বোচ্চ `createdAt` value-ওয়ালা chunk-এ যায়, তাই প্রায় সব write একটা shard-এই পড়ে"),
            ("Inserts spread evenly, but every `createdAt` range query becomes scatter-gather across all shards",
             "Insert সমানভাবে ছড়ায়, কিন্তু প্রতিটি `createdAt` range query সব shard-এ scatter-gather হয়ে যায়"),
            ("MongoDB rejects the shard key, because Date fields can't be used in shard keys",
             "MongoDB shard key-টা reject করে, কারণ Date field shard key-তে ব্যবহার করা যায় না"),
            ("Writes are balanced, but the key's low cardinality causes jumbo chunks",
             "Write balanced থাকে, কিন্তু key-এর low cardinality-র কারণে jumbo chunk তৈরি হয়"),
        ],
        correct=0,
        a_en=r"""A monotonically increasing key (timestamps, ObjectIds, auto-increment numbers) with ranged sharding sends every new document to the chunk with the **maximum key range**, which lives on one shard. That shard becomes a write hotspot while the others sit idle, and the balancer keeps migrating older chunks away.""",
        a_bn=r"""Monotonically বাড়তে থাকা key (timestamp, ObjectId, auto-increment number) ranged sharding-এ থাকলে প্রতিটি নতুন document **সর্বোচ্চ key range**-এর chunk-এ যায়, যেটা একটা shard-এই থাকে। সেই shard write hotspot হয়ে যায়, বাকিগুলো অলস বসে থাকে, আর balancer বারবার পুরনো chunk সরাতে থাকে।""",
        ex_en=r"""
            Option B describes the opposite trade-off — that's what happens with a **hashed** key on `createdAt`: writes spread evenly, but range queries on time can no longer be targeted. Option D is wrong because timestamps have very high cardinality; low cardinality (e.g. `status`) is a different problem.

            A good shard key balances **cardinality**, **frequency** (no single hot value) and **non-monotonic growth**, and also matches your main queries so they're targeted. For events, `{ deviceId: 1, createdAt: 1 }` (or a hashed `deviceId` prefix) spreads writes across devices and keeps per-device time-range queries on one shard. If you chose badly, `reshardCollection` (MongoDB 5.0+) can change the key online, and `refineCollectionShardKey` can add suffix fields.
        """,
        ex_bn=r"""
            Option B উল্টো trade-off বর্ণনা করে — `createdAt`-এ **hashed** key দিলে এমন হয়: write সমানভাবে ছড়ায়, কিন্তু সময়ের range query আর targeted থাকে না। Option D ভুল, কারণ timestamp-এর cardinality খুব বেশি; low cardinality (যেমন `status`) আলাদা সমস্যা।

            ভালো shard key-তে **cardinality**, **frequency** (কোনো একক hot value না থাকা) আর **non-monotonic growth**-এর ভারসাম্য থাকে, এবং main query-গুলোর সাথে মেলে যাতে সেগুলো targeted হয়। Event-এর জন্য `{ deviceId: 1, createdAt: 1 }` (বা hashed `deviceId` prefix) device-গুলোর মধ্যে write ছড়িয়ে দেয় আর per-device time-range query একটা shard-এই রাখে। ভুল key বেছে ফেললে `reshardCollection` (MongoDB 5.0+) দিয়ে online-এ key বদলানো যায়, আর `refineCollectionShardKey` দিয়ে suffix field যোগ করা যায়।
        """,
        tip_en=r"""Name the three shard-key criteria (cardinality, frequency, monotonicity) and then the query-targeting angle — that's the full mental model interviewers look for.""",
        tip_bn=r"""Shard key-এর তিনটা criteria (cardinality, frequency, monotonicity) বলো, তারপর query targeting-এর দিকটা — interviewer ঠিক এই পূর্ণ mental model-টাই খোঁজে।""",
        follow=[
            ("When would you choose a hashed shard key over a ranged one?", "কখন ranged-এর বদলে hashed shard key বেছে নেবে?"),
        ],
        related=["mongo-030"],
        refs=[SHARD_KEY, HASHED, RESHARD],
    ),
    # ------------------------------------------------------------------ mongo-031
    Q(
        id="mongo-031", sub="Replication & Consistency", diff="extreme", type="scenario",
        prio="high", market="international", mins=15,
        tags=["write-concern", "rollback", "read-preference", "causal-consistency", "retryable-writes", "incident"],
        ver="Version-independent concept (default w:majority since MongoDB 5.0; current: MongoDB 9.0, Node.js driver 7.7)", vs=False, status="stable",
        q_en=r"""Incident: after the primary of your 3-node replica set crashed, some customers say orders they got a "success" message for are gone. Others complain they can't see an order right after placing it. The API uses the Node.js driver with `w: 1` and reads order history with `readPreference: "secondaryPreferred"`. Explain what happened and how you'd fix and recover.""",
        q_bn=r"""Incident: তোমার 3-node replica set-এর primary crash করার পর কিছু customer বলছে, যেসব order-এর জন্য তারা "success" message পেয়েছিল সেগুলো উধাও। আরও কিছু customer অভিযোগ করছে, order দেওয়ার সাথে সাথে তারা সেটা দেখতে পাচ্ছে না। API Node.js driver দিয়ে `w: 1` ব্যবহার করে, আর order history পড়ে `readPreference: "secondaryPreferred"` দিয়ে। কী ঘটেছে ব্যাখ্যা করো, আর কীভাবে fix ও recover করবে?""",
        a_en=r"""
            *(Advanced: distributed-systems incident.)*

            **Lost orders → rollback.** With `w: 1` the primary acknowledges a write as soon as it's applied **locally**. Some orders were acknowledged but not yet replicated when the primary crashed. A secondary was elected without them; when the old primary rejoined, it found writes the new primary never had and **rolled them back** (MongoDB saves rolled-back documents as BSON files under the `rollback/` directory in the data path). So "success" was returned for data that wasn't durable.

            **Missing right after placing → stale secondary reads.** `secondaryPreferred` reads can lag the primary, so a user may not see their own write.

            **Fix:**
            1. Use `w: "majority"` — the default since MongoDB 5.0, which this app overrode. Majority-acknowledged writes survive elections and are never rolled back.
            2. Keep **retryable writes** on (default in modern drivers) and make order creation **idempotent** (client `requestId` + unique index), so retries after a failover don't create duplicates or double charges.
            3. Read-your-writes: read a user's own recent data from the **primary**, or use a **causally consistent session** with majority read/write concern so a secondary read waits until it has caught up. Keep secondary reads for analytics.
            4. Topology: three data-bearing members across AZs (avoid an arbiter with majority writes), alerts on replication lag and elections.

            **Recover:** extract the rollback files with `bsondump`, reconcile them against payment-gateway records, and re-insert verified orders. Communicate with affected customers.
        """,
        a_bn=r"""
            *(Advanced: distributed-systems incident।)*

            **হারানো order → rollback।** `w: 1`-এ primary শুধু **নিজের কাছে** write apply হলেই acknowledge করে দেয়। কিছু order acknowledge হয়েছিল কিন্তু primary crash করার আগে replicate হয়নি। একটা secondary সেগুলো ছাড়াই elect হয়েছে; পুরনো primary ফিরে এসে দেখে তার কাছে এমন write আছে যা নতুন primary-র কাছে নেই, তাই সেগুলো **rollback** করে (MongoDB rolled-back document-গুলো data path-এর `rollback/` directory-তে BSON file হিসেবে রেখে দেয়)। অর্থাৎ durable না হওয়া data-র জন্য "success" দেওয়া হয়েছিল।

            **Order দেওয়ার পরপরই দেখা যাচ্ছে না → stale secondary read।** `secondaryPreferred` read primary-র চেয়ে পিছিয়ে থাকতে পারে, তাই user নিজের write দেখতে পায় না।

            **Fix:**
            1. `w: "majority"` ব্যবহার করো — MongoDB 5.0 থেকে এটাই default, এই app সেটা override করেছিল। Majority-acknowledged write election-এর পরও টিকে থাকে, কখনো rollback হয় না।
            2. **Retryable write** চালু রাখো (modern driver-এ default) আর order তৈরি **idempotent** করো (client `requestId` + unique index), যাতে failover-এর পর retry হলে duplicate বা double charge না হয়।
            3. Read-your-writes: user-এর নিজের সাম্প্রতিক data **primary** থেকে পড়ো, অথবা majority read/write concern সহ **causally consistent session** ব্যবহার করো, যাতে secondary read catch up না করা পর্যন্ত অপেক্ষা করে। Secondary read analytics-এর জন্য রাখো।
            4. Topology: বিভিন্ন AZ-তে তিনটা data-bearing member (majority write-এর সাথে arbiter এড়াও), replication lag আর election-এ alert।

            **Recover:** `bsondump` দিয়ে rollback file থেকে data বের করো, payment gateway-র record-এর সাথে মিলিয়ে দেখো, verify করা order আবার insert করো। ক্ষতিগ্রস্ত customer-দের সাথে যোগাযোগ করো।
        """,
        ex_en=r"""
            - **Cost of majority:** each write waits for one secondary in a 3-node set — typically a millisecond or two within a region, more across regions. For orders and payments that's the right trade; for click-tracking logs `w: 1` may be acceptable.
            - **Arbiters (PSA):** with one secondary down, a PSA set can't reach a data-bearing majority, so majority writes stall. That's why three data-bearing nodes are preferred.
            - **Read concern:** `readConcern: "majority"` returns only data that can't be rolled back; `"local"` (default for most reads) may return data that is later rolled back. `"linearizable"` is the strongest but slow and primary-only.
            - **Causal consistency** guarantees (read-your-writes, monotonic reads) need majority read and write concern within the same session.
            - **Retryable writes** retry once on transient network/election errors; they don't replace application-level idempotency for the client's own retries.
        """,
        ex_bn=r"""
            - **Majority-র খরচ:** 3-node set-এ প্রতিটি write একটা secondary-র জন্য অপেক্ষা করে — একই region-এ সাধারণত এক-দুই millisecond, region পার হলে বেশি। Order আর payment-এর জন্য এটা সঠিক trade-off; click-tracking log-এর জন্য হয়তো `w: 1` চলতে পারে।
            - **Arbiter (PSA):** একটা secondary down থাকলে PSA set data-bearing majority পায় না, ফলে majority write আটকে যায়। এজন্যই তিনটা data-bearing node পছন্দনীয়।
            - **Read concern:** `readConcern: "majority"` শুধু সেই data দেয় যা rollback হতে পারে না; `"local"` (বেশিরভাগ read-এর default) এমন data দিতে পারে যা পরে rollback হয়। `"linearizable"` সবচেয়ে শক্তিশালী, কিন্তু slow আর শুধু primary-তে চলে।
            - **Causal consistency**-র guarantee (read-your-writes, monotonic reads) পেতে একই session-এ majority read ও write concern লাগে।
            - **Retryable write** transient network/election error-এ একবার retry করে; client-এর নিজের retry-র জন্য application-level idempotency-র বিকল্প এটা না।
        """,
        tip_en=r"""Separate the two symptoms (durability vs. staleness) — they have different root causes. Then cover prevent → recover → monitor. Interviewers love hearing you'd reconcile with the payment gateway, not just "restore the data".""",
        tip_bn=r"""দুইটা লক্ষণ আলাদা করো (durability বনাম staleness) — এদের root cause ভিন্ন। তারপর prevent → recover → monitor ধরে বলো। Interviewer শুনতে পছন্দ করে যে তুমি শুধু "data restore করব" না বলে payment gateway-র সাথে reconcile করবে।""",
        mist_en=r"""Blaming "MongoDB lost data" without mentioning write concern; assuming secondaries are always up to date; thinking retryable writes alone prevent duplicate orders.""",
        mist_bn=r"""Write concern-এর কথা না বলে "MongoDB data হারিয়েছে" বলে দোষ দেওয়া; ধরে নেওয়া secondary সবসময় up to date থাকে; ভাবা যে শুধু retryable write-ই duplicate order আটকাবে।""",
        code=r"""
            import { MongoClient } from "mongodb";

            const client = new MongoClient(process.env.MONGODB_URI, {
              w: "majority",               // durable across elections
              readConcernLevel: "majority",
              retryWrites: true,           // default in modern drivers
            });
            const orders = client.db("shop").collection("orders");

            // Idempotent create: unique index on requestId (created once at deploy)
            await orders.createIndex({ requestId: 1 }, { unique: true });

            // Read-your-writes even when reading from a secondary
            const session = client.startSession({ causalConsistency: true });
            try {
              await orders.insertOne({ requestId, customerId, items, total, createdAt: new Date() }, { session });
              const history = await orders
                .find({ customerId }, { session, readPreference: "secondaryPreferred" })
                .sort({ createdAt: -1 })
                .limit(20)
                .toArray();
            } finally {
              await session.endSession();
            }
        """,
        lang="javascript",
        follow=[
            ("How large should the oplog window be, and why does it matter for a secondary that was down for hours?", "Oplog window কত বড় হওয়া উচিত, আর কয়েক ঘণ্টা down থাকা secondary-র জন্য এটা কেন গুরুত্বপূর্ণ?"),
            ("Would you ever use `w: 1` in production? For which data?", "Production-এ কি কখনো `w: 1` ব্যবহার করবে? কোন data-র জন্য?"),
        ],
        related=["mongo-030", "mongo-025"],
        refs=[WRITE_CONCERN, ROLLBACK, CAUSAL],
    ),
]

if __name__ == "__main__":
    save("mongodb", "b2", QUESTIONS)
