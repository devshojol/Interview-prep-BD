# Mongoose — batch 4 (mongoose-010, 011, 019, 020, 021, 022, 028, 029)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

MIGRATE7 = ("Mongoose — Migrating to 7 (callbacks removed)", "https://mongoosejs.com/docs/migrating_to_7.html")
MIGRATE9 = ("Mongoose — Migrating to 9", "https://mongoosejs.com/docs/migrating_to_9.html")
QUERIES = ("Mongoose — Queries", "https://mongoosejs.com/docs/queries.html")
MONGOOSE_API = ("Mongoose API — Mongoose (isValidObjectId, isObjectIdOrHexString)", "https://mongoosejs.com/docs/api/mongoose.html")
VALIDATION = ("Mongoose — Validation", "https://mongoosejs.com/docs/validation.html")
GUIDE_INDEXES = ("Mongoose — Schemas guide (indexes, autoIndex)", "https://mongoosejs.com/docs/guide.html")
MODEL_API = ("Mongoose API — Model", "https://mongoosejs.com/docs/api/model.html")
NODE_DRIVER = ("MongoDB Node.js Driver documentation", "https://www.mongodb.com/docs/drivers/node/current/")
MONGOOSE_INDEX = ("Mongoose — Getting Started", "https://mongoosejs.com/docs/index.html")
SCHEMA_VALIDATION = ("MongoDB Manual — Schema Validation", "https://www.mongodb.com/docs/manual/core/schema-validation/")
DISCRIMINATORS = ("Mongoose — Discriminators", "https://mongoosejs.com/docs/discriminators.html")
POPULATE = ("Mongoose — Populate (virtual populate, perDocumentLimit)", "https://mongoosejs.com/docs/populate.html")
VIRTUALS = ("Mongoose — Mongoose Virtuals", "https://mongoosejs.com/docs/tutorials/virtuals.html")
CONNECTIONS = ("Mongoose — Connections", "https://mongoosejs.com/docs/connections.html")
NEXTJS = ("Mongoose — Using Mongoose With Next.js", "https://mongoosejs.com/docs/nextjs.html")

QUESTIONS = [
    # ------------------------------------------------------------------ mongoose-010
    Q(
        id="mongoose-010", sub="Mongoose 9 Changes", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=1,
        tags=["callbacks", "async-await", "mongoose-9", "migration"],
        ver="Mongoose 9.11 (callbacks removed since 7.0; remaining ones removed in 9.0)", vs=True, status="version-specific",
        q_en=r"""An older tutorial uses the code below. What happens when you run it with Mongoose 9?""",
        q_bn=r"""একটা পুরনো tutorial-এ নিচের code ব্যবহার করা হয়েছে। Mongoose 9-এ এটা run করলে কী হবে?""",
        code=r"""
            User.find({ role: "admin" }, function (err, users) {
              if (err) return console.error(err);
              console.log(users.length);
            });
        """,
        lang="javascript",
        options=[
            ("It works — callbacks are still supported for backwards compatibility",
             "চলবে — backwards compatibility-র জন্য callback এখনো support করে"),
            ("It throws a `MongooseError` saying `Model.find()` no longer accepts a callback",
             "একটা `MongooseError` throw করবে, যেখানে বলা থাকবে `Model.find()` আর callback নেয় না"),
            ("The callback is silently ignored and the query never runs",
             "Callback চুপচাপ ignore হবে, আর query কখনো চলবে না"),
            ("It works but prints a deprecation warning",
             "চলবে, তবে একটা deprecation warning print করবে"),
        ],
        correct=1,
        a_en=r"""Mongoose removed callback support from model and query APIs in **Mongoose 7**, and Mongoose 9 removed the last remaining callback-style APIs. Passing a callback throws an error such as "Model.find() no longer accepts a callback". The modern form is `const users = await User.find({ role: "admin" });`.""",
        a_bn=r"""**Mongoose 7**-এ model আর query API থেকে callback support সরিয়ে দেওয়া হয়েছে, আর Mongoose 9 বাকি থাকা শেষ callback-style API-গুলোও সরিয়েছে। Callback দিলে "Model.find() no longer accepts a callback"-এর মতো error throw হয়। আধুনিক রূপ হলো `const users = await User.find({ role: "admin" });`।""",
        ex_en=r"""
            Option D is the tempting one — many libraries deprecate before removing — but in Mongoose 7+ it's a hard error, not a warning. Option C would be worse (a silent failure); Mongoose fails loudly on purpose.

            The same applies to `mongoose.connect(uri, cb)`, `doc.save(cb)`, `Model.create(doc, cb)` and `query.exec(cb)`. In Mongoose 9, `doValidate()` returns a promise and `Document.prototype.updateOne()` no longer takes a callback either. When upgrading legacy Express code, convert to `async/await` and let Express 5 forward rejected promises to your error middleware.
        """,
        ex_bn=r"""
            Option D বিভ্রান্তিকর — অনেক library সরানোর আগে deprecate করে — কিন্তু Mongoose 7+-এ এটা warning না, সরাসরি error। Option C আরও খারাপ হতো (চুপচাপ fail); Mongoose ইচ্ছাকৃতভাবে জোরে fail করে।

            একই কথা `mongoose.connect(uri, cb)`, `doc.save(cb)`, `Model.create(doc, cb)` আর `query.exec(cb)`-এর ক্ষেত্রেও। Mongoose 9-এ `doValidate()` promise return করে, আর `Document.prototype.updateOne()`-ও আর callback নেয় না। Legacy Express code upgrade করার সময় `async/await`-এ রূপান্তর করো, আর Express 5-কে rejected promise error middleware-এ পাঠাতে দাও।
        """,
        tip_en=r"""Say which version removed callbacks (7) and show the async/await rewrite in one line — it proves you can maintain older codebases, which is common in real jobs.""",
        tip_bn=r"""কোন version-এ callback সরানো হয়েছে (7) সেটা বলো আর এক লাইনে async/await-এ রূপান্তর দেখাও — এতে প্রমাণ হয় তুমি পুরনো codebase maintain করতে পারো, যা বাস্তব চাকরিতে খুবই common।""",
        follow=[
            ("How would you convert a callback-based Mongoose 5 codebase to async/await safely?", "Callback-ভিত্তিক একটা Mongoose 5 codebase নিরাপদে async/await-এ কীভাবে রূপান্তর করবে?"),
        ],
        related=["mongoose-004"],
        refs=[MIGRATE7, MIGRATE9],
    ),
    # ------------------------------------------------------------------ mongoose-011
    Q(
        id="mongoose-011", sub="Error Handling", diff="easy", type="debugging",
        prio="high", market="bangladesh", mins=3,
        tags=["casterror", "objectid", "isobjectidorhexstring", "404", "express"],
        ver="Mongoose 9.11 (`isValidObjectId(number)` returns false since 9.0), Express 5", vs=True, status="stable",
        q_en=r"""This endpoint returns **500 Internal Server Error** for `GET /api/products/abc` and **200 `null`** for a valid ID of a deleted product. What's wrong, and how would you fix it?""",
        q_bn=r"""এই endpoint `GET /api/products/abc`-এর জন্য **500 Internal Server Error** দেয়, আর delete হয়ে যাওয়া product-এর valid ID-র জন্য **200 `null`** দেয়। সমস্যা কী, আর কীভাবে ঠিক করবে?""",
        code=r"""
            app.get("/api/products/:id", async (req, res) => {
              const product = await Product.findById(req.params.id);
              res.json(product);
            });

            // Log for /api/products/abc:
            // CastError: Cast to ObjectId failed for value "abc" (type string)
            //   at path "_id" for model "Product"
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            import mongoose from "mongoose";

            app.get("/api/products/:id", async (req, res) => {
              const { id } = req.params;
              if (!mongoose.isObjectIdOrHexString(id)) {
                return res.status(400).json({ error: "Invalid product id" });
              }

              const product = await Product.findById(id).lean();
              if (!product) return res.status(404).json({ error: "Product not found" });

              res.json(product);
            });
        """)],
        a_en=r"""
            Two bugs:

            1. **`CastError` → 500.** Mongoose casts query values to the schema type before querying. `"abc"` can't become an `ObjectId`, so `findById` throws a `CastError`, and with no handling it becomes a 500. That's a client mistake and should be a **400**.
            2. **`null` → 200.** `findById` returns `null` when nothing matches; the code sends it as a successful response instead of a **404**.

            Fix: validate the ID first with `mongoose.isObjectIdOrHexString(id)` (true only for `ObjectId` instances and 24-character hex strings), and check for `null`. Alternatively, map `CastError` to 400 in central error middleware and use `.orFail()` for 404s.
        """,
        a_bn=r"""
            দুইটা bug:

            1. **`CastError` → 500।** Query চালানোর আগে Mongoose query value-কে schema type-এ cast করে। `"abc"` `ObjectId` হতে পারে না, তাই `findById` একটা `CastError` throw করে, আর কোনো handling না থাকায় সেটা 500 হয়ে যায়। এটা client-এর ভুল, তাই **400** হওয়া উচিত।
            2. **`null` → 200।** কিছু match না করলে `findById` `null` return করে; code সেটাকে **404**-এর বদলে সফল response হিসেবে পাঠাচ্ছে।

            Fix: আগে `mongoose.isObjectIdOrHexString(id)` দিয়ে ID validate করো (শুধু `ObjectId` instance আর 24-character hex string-এর জন্য true), আর `null` check করো। বিকল্পভাবে, central error middleware-এ `CastError`-কে 400-এ map করো আর 404-এর জন্য `.orFail()` ব্যবহার করো।
        """,
        ex_en=r"""
            - **Why not `isValidObjectId()`?** It answers a broader question — "can Mongoose cast this to an ObjectId?" — so it also returns `true` for things like a Mongoose document, and its rules have changed between versions (older releases accepted any 12-character string such as `"hello-world!"`; until Mongoose 8 it returned `true` for numbers, while Mongoose 9 returns `false` and `new mongoose.Types.ObjectId(6)` throws). For a URL param, `isObjectIdOrHexString()` states the intent exactly: an `ObjectId` instance or a 24-character hex string.
            - **Express 5:** a thrown `CastError` in an async route reaches your error middleware automatically; in Express 4 an unhandled rejection could leave the request hanging.
            - **Security:** don't echo the raw error message to clients; it reveals model and path names.
            - `.lean()` is fine here because the handler only reads and returns data.
        """,
        ex_bn=r"""
            - **`isValidObjectId()` কেন না?** এটা আরও বড় প্রশ্নের উত্তর দেয় — "Mongoose কি এটাকে ObjectId-এ cast করতে পারবে?" — তাই Mongoose document-এর মতো জিনিসের জন্যও `true` দেয়, আর version ভেদে এর নিয়ম বদলেছে (পুরনো release যেকোনো 12-character string, যেমন `"hello-world!"`, মেনে নিত; Mongoose 8 পর্যন্ত number-এর জন্য `true` দিত, আর Mongoose 9 `false` দেয় এবং `new mongoose.Types.ObjectId(6)` throw করে)। URL param-এর জন্য `isObjectIdOrHexString()` উদ্দেশ্যটা ঠিকঠাক বলে: একটা `ObjectId` instance বা 24-character hex string।
            - **Express 5:** async route-এ throw হওয়া `CastError` automatically error middleware-এ পৌঁছায়; Express 4-এ unhandled rejection-এ request ঝুলে থাকতে পারত।
            - **Security:** raw error message client-কে echo কোরো না; এতে model আর path-এর নাম বেরিয়ে যায়।
            - Handler শুধু data পড়ে return করছে, তাই এখানে `.lean()` ঠিক আছে।
        """,
        tip_en=r"""Name the HTTP status each case deserves (400 vs 404 vs 500) — API-design awareness is part of what this question checks, not just Mongoose knowledge.""",
        tip_bn=r"""প্রতিটি ক্ষেত্রে কোন HTTP status হওয়া উচিত (400 বনাম 404 বনাম 500) সেটা বলো — এই প্রশ্নে শুধু Mongoose না, API design-এর সচেতনতাও যাচাই করা হয়।""",
        mist_en=r"""Wrapping everything in `try/catch` and returning 500 for all errors; relying on `isValidObjectId()` semantics that differ between Mongoose versions; forgetting the `null` check.""",
        mist_bn=r"""সবকিছু `try/catch`-এ মুড়ে সব error-এর জন্য 500 return করা; Mongoose version ভেদে বদলে যাওয়া `isValidObjectId()`-এর আচরণের ওপর ভরসা করা; `null` check ভুলে যাওয়া।""",
        follow=[
            ("How would you handle invalid IDs for every route at once instead of in each handler?", "প্রতিটি handler-এ আলাদা করে না করে সব route-এর invalid ID একসাথে কীভাবে handle করবে?"),
        ],
        related=["mongoose-005", "mongoose-017"],
        refs=[MONGOOSE_API, VALIDATION, MIGRATE9],
    ),
    # ------------------------------------------------------------------ mongoose-019
    Q(
        id="mongoose-019", sub="Indexes", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["indexes", "autoindex", "createindexes", "deployment"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""Production runs with `autoIndex: false`. A new release adds `orderSchema.index({ customerId: 1, createdAt: -1 })` for the "My orders" page. What happens after the deploy?""",
        q_bn=r"""Production `autoIndex: false` দিয়ে চলে। নতুন একটা release-এ "My orders" page-এর জন্য `orderSchema.index({ customerId: 1, createdAt: -1 })` যোগ করা হয়েছে। Deploy-এর পর কী হবে?""",
        options=[
            ("Mongoose builds the index lazily the first time a query needs it",
             "প্রথমবার কোনো query-র দরকার হলে Mongoose lazily index build করে"),
            ("Nothing is built automatically: the index exists only after you run `Order.createIndexes()` (or a migration), so the page keeps scanning until then",
             "Automatically কিছুই build হয় না: `Order.createIndexes()` (বা একটা migration) চালানোর পরেই index তৈরি হয়, তার আগ পর্যন্ত page scan করতেই থাকে"),
            ("The app refuses to start because the schema declares an index that doesn't exist in MongoDB",
             "App start হতে অস্বীকার করে, কারণ schema-তে এমন index declare করা যেটা MongoDB-তে নেই"),
            ("MongoDB notices the repeated query pattern and creates the index automatically",
             "MongoDB বারবার আসা query pattern লক্ষ করে automatically index বানিয়ে ফেলে"),
        ],
        correct=1,
        a_en=r"""`schema.index()` only **declares** an index. With `autoIndex: true` (the default), Mongoose calls `createIndexes()` when the model initialises; with `autoIndex: false` nothing happens until you build it yourself — `Model.createIndexes()`, `syncIndexes()`, or a migration script/pipeline step.""",
        a_bn=r"""`schema.index()` শুধু একটা index **declare** করে। `autoIndex: true` (default) থাকলে model initialise হওয়ার সময় Mongoose `createIndexes()` call করে; `autoIndex: false` হলে তুমি নিজে build না করা পর্যন্ত কিছুই হয় না — `Model.createIndexes()`, `syncIndexes()`, বা একটা migration script/pipeline ধাপ দিয়ে।""",
        ex_en=r"""
            Turning `autoIndex` off in production is what the Mongoose docs suggest when you want to manage indexes carefully: an index build on a large collection consumes CPU, I/O and cache on every replica-set member, and you don't want every app restart to trigger one. The cost is that you need a deployment step — otherwise you ship code that depends on an index that doesn't exist (option B's "keeps scanning").

            Option C is wrong — Mongoose doesn't verify indexes at startup. Option D is wrong — MongoDB never creates secondary indexes on its own. A good pipeline runs the index migration *before* deploying the code that relies on it.
        """,
        ex_bn=r"""
            Index সাবধানে manage করতে চাইলে Mongoose docs production-এ `autoIndex` বন্ধ রাখার পরামর্শ দেয়: বড় collection-এ index build প্রতিটি replica-set member-এ CPU, I/O আর cache খরচ করে, আর তুমি চাও না প্রতিবার app restart-এ সেটা শুরু হোক। খরচ হলো একটা deployment ধাপ লাগে — না হলে এমন code ship হয় যেটা একটা অনুপস্থিত index-এর ওপর নির্ভর করে (option B-এর "scan করতেই থাকে")।

            Option C ভুল — Mongoose startup-এ index যাচাই করে না। Option D ভুল — MongoDB কখনো নিজে থেকে secondary index বানায় না। একটা ভালো pipeline index migration চালায় সেই code deploy করার *আগে*, যেটা ওই index-এর ওপর নির্ভর করে।
        """,
        tip_en=r"""Add the ordering point — "build the index before deploying the code that needs it" — it shows you think about deployments, not just APIs.""",
        tip_bn=r"""ক্রমের কথাটা যোগ করো — "যে code-এর index লাগবে, সেটা deploy করার আগে index build করো" — এতে বোঝা যায় তুমি শুধু API না, deployment নিয়েও ভাবো।""",
        follow=[
            ("What's the difference between `createIndexes()` and `syncIndexes()`?", "`createIndexes()` আর `syncIndexes()`-এর পার্থক্য কী?"),
        ],
        related=["mongoose-032", "mongoose-003"],
        refs=[GUIDE_INDEXES, MODEL_API],
    ),
    # ------------------------------------------------------------------ mongoose-020
    Q(
        id="mongoose-020", sub="Mongoose vs Native Driver", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["odm", "native-driver", "trade-offs", "validation", "performance"],
        ver="Mongoose 9.11 (built on MongoDB Node.js driver 7.x)", vs=False, status="stable",
        q_en=r"""Mongoose or the native MongoDB Node.js driver: how do they compare, and how would you choose for a new service?""",
        q_bn=r"""Mongoose নাকি native MongoDB Node.js driver: এদের তুলনা কেমন, আর নতুন একটা service-এর জন্য কীভাবে বেছে নেবে?""",
        a_en=r"""
            Mongoose is an ODM built **on top of** the official driver.

            **Mongoose gives you:** schemas with casting, defaults and validation; middleware (hooks); `populate()`; virtuals, methods and plugins; discriminators; and TypeScript types inferred from schemas. It's productive for CRUD-heavy apps and keeps a team consistent.

            **Its costs:** an abstraction layer with its own rules to learn (update validators off by default, `strictQuery`, hook types), hydration overhead (mitigated with `.lean()`), and occasional lag behind brand-new server features.

            **The native driver gives you:** a thin, fast, explicit API with every server feature available immediately (new aggregation stages, encryption options, bulk and streaming APIs). But there's no schema — you bring validation yourself (zod at the API edge, `$jsonSchema` validators in MongoDB).

            **How I choose:** a typical business app with many related models and a mixed-experience team → Mongoose. A high-throughput ingestion/analytics service, a shared library, or a database written to by several services/languages → native driver plus database-level validation. They also mix well: inside a Mongoose app you can drop to the driver via `Model.collection` for bulk or streaming jobs.
        """,
        a_bn=r"""
            Mongoose হলো official driver-এর **ওপর** তৈরি একটা ODM।

            **Mongoose যা দেয়:** casting, default আর validation সহ schema; middleware (hook); `populate()`; virtual, method আর plugin; discriminator; আর schema থেকে inferred TypeScript type। CRUD-heavy app-এ এটা productive, আর team-কে consistent রাখে।

            **এর খরচ:** নিজস্ব নিয়মসহ একটা abstraction layer, যেটা শিখতে হয় (update validator default-ভাবে বন্ধ, `strictQuery`, hook-এর ধরন), hydration overhead (`.lean()` দিয়ে কমানো যায়), আর একদম নতুন server feature-এ মাঝে মাঝে পিছিয়ে থাকা।

            **Native driver যা দেয়:** পাতলা, দ্রুত, explicit API, যেখানে প্রতিটি server feature সাথে সাথে পাওয়া যায় (নতুন aggregation stage, encryption option, bulk আর streaming API)। কিন্তু কোনো schema নেই — validation নিজেকেই আনতে হয় (API edge-এ zod, MongoDB-তে `$jsonSchema` validator)।

            **আমি যেভাবে বেছে নিই:** অনেক related model আর মিশ্র অভিজ্ঞতার team সহ সাধারণ business app → Mongoose। High-throughput ingestion/analytics service, shared library, বা যে database-এ কয়েকটা service/language লেখে → native driver আর database-level validation। দুটো মিলিয়েও চলে: Mongoose app-এর ভেতরেই bulk বা streaming job-এর জন্য `Model.collection` দিয়ে driver-এ নেমে যাওয়া যায়।
        """,
        ex_en=r"""
            - **Validation location matters:** Mongoose validation lives in one Node.js codebase. If a Python job or another service writes to the same collection, only MongoDB `$jsonSchema` validation protects you — so for shared data, put rules in the database too.
            - **Performance reality:** for reads, `.lean()` brings Mongoose close to the driver; the bigger wins usually come from indexes, projections and query shape, not from dropping the ODM.
            - **TypeScript:** the driver supports typed collections (`db.collection<User>("users")`), but types aren't runtime validation; Mongoose schemas give both runtime casting and inferred types.
            - **Team factor:** in many Bangladeshi MERN teams Mongoose is the common default — consistency with existing services and hiring is a legitimate reason to choose it.
            - **Bypass caution:** anything done through `Model.collection` skips Mongoose casting, validation and middleware.
        """,
        ex_bn=r"""
            - **Validation কোথায় থাকে, সেটা গুরুত্বপূর্ণ:** Mongoose validation একটা Node.js codebase-এই থাকে। কোনো Python job বা অন্য service একই collection-এ লিখলে শুধু MongoDB-র `$jsonSchema` validation-ই রক্ষা করে — তাই shared data-র নিয়ম database-এও রাখো।
            - **Performance-এর বাস্তবতা:** read-এ `.lean()` Mongoose-কে driver-এর কাছাকাছি নিয়ে আসে; বড় উন্নতি সাধারণত index, projection আর query-র shape থেকে আসে, ODM বাদ দিয়ে না।
            - **TypeScript:** driver typed collection support করে (`db.collection<User>("users")`), কিন্তু type মানেই runtime validation না; Mongoose schema runtime casting আর inferred type দুটোই দেয়।
            - **Team-এর বিষয়:** বাংলাদেশের অনেক MERN team-এ Mongoose-ই common default — existing service আর hiring-এর সাথে consistency রাখাও এটা বেছে নেওয়ার একটা যৌক্তিক কারণ।
            - **Bypass-এ সাবধান:** `Model.collection` দিয়ে করা যেকোনো কাজ Mongoose-এর casting, validation আর middleware এড়িয়ে যায়।
        """,
        tip_en=r"""Avoid "Mongoose is slow" or "the driver is too low-level" clichés. Tie the choice to who writes the data, how many models there are and the team — that's how senior engineers argue tooling.""",
        tip_bn=r""""Mongoose slow" বা "driver খুব low-level" — এমন বাঁধাধরা কথা এড়াও। পছন্দটাকে যুক্ত করো কে data লেখে, কতগুলো model আছে আর team কেমন — senior engineer-রা এভাবেই tooling নিয়ে যুক্তি দেয়।""",
        mist_en=r"""Claiming the driver can't do relationships (it has `$lookup`); assuming Mongoose validation protects data written by other services; picking the driver "for speed" without measuring.""",
        mist_bn=r"""Driver relationship সামলাতে পারে না বলা (এতে `$lookup` আছে); ধরে নেওয়া Mongoose validation অন্য service-এর লেখা data-ও রক্ষা করে; না মেপেই "speed-এর জন্য" driver বেছে নেওয়া।""",
        code=r"""
            // Mongoose: casting, setters and validation happen in the app
            const user = await User.create({ email: "Rafi@Example.com", age: "27" });
            // stored as { email: "rafi@example.com", age: 27 } — lowercase setter + Number cast

            // Native driver: stored exactly as given — validation is your job
            const { insertedId } = await db.collection("users").insertOne({ email: "Rafi@Example.com", age: "27" });
            // stored as { email: "Rafi@Example.com", age: "27" } (age is a string!)

            // Dropping to the driver from a Mongoose app (skips Mongoose validation/middleware)
            const cursor = User.collection.find({}, { projection: { email: 1 } }).batchSize(1000);
        """,
        lang="javascript",
        follow=[
            ("How would you enforce a schema if a Python job also writes to the `users` collection?", "একটা Python job-ও `users` collection-এ লিখলে schema কীভাবে enforce করবে?"),
            ("Would you use Mongoose in a high-volume event-ingestion service? Why or why not?", "High-volume event-ingestion service-এ কি Mongoose ব্যবহার করবে? কেন বা কেন না?"),
        ],
        related=["mongoose-016", "mongoose-001"],
        refs=[MONGOOSE_INDEX, NODE_DRIVER, SCHEMA_VALIDATION],
    ),
    # ------------------------------------------------------------------ mongoose-021
    Q(
        id="mongoose-021", sub="Mongoose 9 Changes", diff="medium", type="scenario",
        prio="high", market="both", mins=8,
        tags=["mongoose-9", "migration", "upgrade", "breaking-changes", "update-pipeline"],
        ver="Mongoose 9.11 (upgrade from 8.x)", vs=True, status="version-specific",
        q_en=r"""You need to upgrade a large Express + Mongoose 8 codebase to Mongoose 9.11. What would you check and change, and how would you roll it out safely?""",
        q_bn=r"""একটা বড় Express + Mongoose 8 codebase Mongoose 9.11-এ upgrade করতে হবে। কী কী check আর পরিবর্তন করবে, আর কীভাবে নিরাপদে roll out করবে?""",
        a_en=r"""
            **Prerequisites:** Node.js **≥ 20.19**, and awareness that Mongoose 9 uses the MongoDB Node.js driver 7.x — check any direct driver usage. If the cluster runs MongoDB 9.0, target Mongoose ≥ 9.10.4 because of the `syncIndexes()` collation issue.

            **Code changes from the migration guide:**
            1. **Pre hooks:** no more `next()` — convert to `async function () {}` and `throw` to fail. `isAsync`-style `(next, done)` hooks are gone.
            2. **Update pipelines:** `updateOne(filter, [ { $set: ... } ])` now throws unless you pass `{ updatePipeline: true }` (or enable it globally after review).
            3. **`findOneAndUpdate`:** replace `new: true` / `returnOriginal: false` with `returnDocument: "after"` (deprecated since 9.2, warnings in logs).
            4. **ObjectId:** `isValidObjectId(6)` is now `false` and `new ObjectId(6)` throws — check numeric-ID code paths.
            5. **UUID paths** now return `bson.UUID` instances instead of strings — `===` comparisons with strings break.
            6. Remove the `background` index option; remaining callbacks (`doValidate`, `Document#updateOne`) are gone.
            7. **TypeScript:** `FilterQuery` → `QueryFilter`, with stricter filter typing that will surface real bugs.

            **Rollout:** upgrade on a branch, grep for the patterns above, run the type checker and full test suite (including hooks and transactions), soak in staging with production-like data while watching logs for deprecation warnings, then deploy gradually with the 8.x line as a rollback option.
        """,
        a_bn=r"""
            **পূর্বশর্ত:** Node.js **≥ 20.19**, আর মনে রাখা যে Mongoose 9 MongoDB Node.js driver 7.x ব্যবহার করে — সরাসরি driver ব্যবহারের জায়গাগুলো check করো। Cluster MongoDB 9.0-এ চললে `syncIndexes()`-এর collation সমস্যার জন্য Mongoose ≥ 9.10.4 target করো।

            **Migration guide অনুযায়ী code-এর পরিবর্তন:**
            1. **Pre hook:** আর `next()` নেই — `async function () {}`-এ রূপান্তর করো আর fail করাতে `throw` করো। `isAsync`-style `(next, done)` hook আর নেই।
            2. **Update pipeline:** `updateOne(filter, [ { $set: ... } ])` এখন throw করে, যদি না `{ updatePipeline: true }` দাও (বা review করে globally চালু করো)।
            3. **`findOneAndUpdate`:** `new: true` / `returnOriginal: false`-এর বদলে `returnDocument: "after"` (9.2 থেকে deprecated, log-এ warning আসে)।
            4. **ObjectId:** `isValidObjectId(6)` এখন `false` আর `new ObjectId(6)` throw করে — numeric-ID-র code path check করো।
            5. **UUID path** এখন string-এর বদলে `bson.UUID` instance return করে — string-এর সাথে `===` তুলনা ভেঙে যায়।
            6. `background` index option সরিয়ে দাও; বাকি callback (`doValidate`, `Document#updateOne`) আর নেই।
            7. **TypeScript:** `FilterQuery` → `QueryFilter`, আরও কঠোর filter typing সহ — এতে আসল bug ধরা পড়বে।

            **Rollout:** একটা branch-এ upgrade করো, উপরের pattern-গুলো grep করো, type checker আর পুরো test suite চালাও (hook আর transaction সহ), production-এর মতো data নিয়ে staging-এ কিছুদিন চালিয়ে log-এ deprecation warning দেখো, তারপর ধীরে ধীরে deploy করো, rollback option হিসেবে 8.x line রেখে।
        """,
        ex_en=r"""
            - **Why update pipelines became opt-in:** a pipeline update (`[ { $set: ... } ]`) is evaluated by the server with aggregation semantics; accidentally passing an array where an update object was expected — e.g. from user input — could do unexpected things. Opt-in makes the intent explicit.
            - **Hidden hook breakage:** a pre hook that still declares `next` and calls it will throw a `TypeError` at runtime, so only tests that exercise `save()` paths will catch it — make sure they exist before upgrading.
            - **Hooks on custom methods/statics** now only run when those functions are async or return a promise.
            - **Order of operations:** upgrade Node.js first, then Mongoose, then the MongoDB server (or vice versa with compatibility checks) — never everything in one deploy.
        """,
        ex_bn=r"""
            - **Update pipeline কেন opt-in হলো:** pipeline update (`[ { $set: ... } ]`) server aggregation-এর নিয়মে evaluate করে; update object-এর জায়গায় ভুল করে array চলে গেলে — যেমন user input থেকে — অপ্রত্যাশিত কিছু ঘটতে পারে। Opt-in হওয়ায় উদ্দেশ্যটা স্পষ্ট করতে হয়।
            - **লুকানো hook ভাঙন:** যে pre hook এখনো `next` declare করে call করে, সেটা runtime-এ `TypeError` throw করবে — তাই শুধু `save()` পথ চালানো test-ই এটা ধরবে; upgrade-এর আগে নিশ্চিত হও এমন test আছে।
            - **Custom method/static-এর hook** এখন শুধু তখনই চলে, যখন ওই function async বা promise return করে।
            - **কাজের ক্রম:** আগে Node.js, তারপর Mongoose, তারপর MongoDB server upgrade করো (অথবা compatibility check করে উল্টো ক্রমে) — কখনো সবকিছু এক deploy-এ না।
        """,
        tip_en=r"""Show a process, not just a list: prerequisites → code changes → verification → gradual rollout with rollback. Mentioning the MongoDB 9.0 + `syncIndexes()` interaction shows you read both release notes.""",
        tip_bn=r"""শুধু তালিকা না, একটা process দেখাও: পূর্বশর্ত → code পরিবর্তন → যাচাই → rollback সহ ধীরে ধীরে rollout। MongoDB 9.0 + `syncIndexes()`-এর সম্পর্ক উল্লেখ করলে বোঝা যায় তুমি দুটোর release note-ই পড়েছ।""",
        mist_en=r"""Bumping the version and relying on "it compiles"; enabling `updatePipeline` globally without reviewing call sites; ignoring deprecation warnings for `new: true`.""",
        mist_bn=r"""শুধু version বাড়িয়ে "compile তো হচ্ছে" ভেবে নিশ্চিন্ত থাকা; call site review না করেই globally `updatePipeline` চালু করা; `new: true`-এর deprecation warning উপেক্ষা করা।""",
        code=r"""
            // Before (Mongoose 8)
            schema.pre("save", function (next) { this.slug = slugify(this.title); next(); });
            await Post.findOneAndUpdate({ _id }, { $inc: { views: 1 } }, { new: true });
            await Post.updateOne({ _id }, [{ $set: { score: { $add: ["$likes", "$shares"] } } }]);

            // After (Mongoose 9.11)
            schema.pre("save", async function () { this.slug = slugify(this.title); });
            await Post.findOneAndUpdate({ _id }, { $inc: { views: 1 } }, { returnDocument: "after" });
            await Post.updateOne(
              { _id },
              [{ $set: { score: { $add: ["$likes", "$shares"] } } }],
              { updatePipeline: true }          // pipelines are opt-in in v9
            );
        """,
        lang="javascript",
        extra=[dict(lang="bash", label_en="Quick audit before upgrading", label_bn="Upgrade-এর আগে দ্রুত audit", src=r"""
            grep -rnE "pre\(.*function *\( *next" src/        # hooks that still take next
            grep -rnE "new: *true|returnOriginal" src/        # deprecated findOneAndUpdate options
            grep -rnE "update(One|Many)\([^)]*\[" src/        # possible update pipelines
            grep -rn  "FilterQuery\|background:" src/          # TS rename, removed index option
        """)],
        follow=[
            ("Which tests would you write first to make this upgrade safe?", "এই upgrade নিরাপদ করতে প্রথমে কোন test-গুলো লিখবে?"),
            ("How would you roll back if production errors spike after deploying Mongoose 9?", "Mongoose 9 deploy-এর পর production-এ error বেড়ে গেলে কীভাবে rollback করবে?"),
        ],
        related=["mongoose-013", "mongoose-010", "mongoose-032"],
        refs=[MIGRATE9],
    ),
    # ------------------------------------------------------------------ mongoose-022
    Q(
        id="mongoose-022", sub="Schema Design", diff="medium", type="conceptual",
        prio="medium", market="both", mins=5,
        tags=["discriminators", "inheritance", "polymorphism", "schema-design"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""What are discriminators in Mongoose, when would you use them, and what pitfalls should you know about?""",
        q_bn=r"""Mongoose-এ discriminator কী, কখন ব্যবহার করবে, আর কোন pitfall-গুলো জানা দরকার?""",
        a_en=r"""
            Discriminators are Mongoose's way of doing **schema inheritance in a single collection**. You define a base model with shared fields, then create child models with `Base.discriminator("name", childSchema)`. All documents live in the same collection, and a **discriminator key** (default `__t`, configurable with `discriminatorKey`) records each document's type.

            - Querying a child model (`SmsNotification.find()`) automatically adds `{ __t: "sms" }` to the filter.
            - Querying the base model returns all types, each hydrated as the right child model with its own validation, methods and hooks.

            Good uses: notifications (SMS / email / push), payment methods (bKash / card / COD), activity-feed events, polymorphic content — "same kind of thing, a few different fields, usually listed together".
        """,
        a_bn=r"""
            Discriminator হলো **একটা collection-এর ভেতরে schema inheritance** করার Mongoose-এর উপায়। Shared field সহ একটা base model define করো, তারপর `Base.discriminator("name", childSchema)` দিয়ে child model বানাও। সব document একই collection-এ থাকে, আর একটা **discriminator key** (default `__t`, `discriminatorKey` দিয়ে বদলানো যায়) প্রতিটি document-এর type লিখে রাখে।

            - Child model দিয়ে query করলে (`SmsNotification.find()`) filter-এ automatically `{ __t: "sms" }` যোগ হয়।
            - Base model দিয়ে query করলে সব type আসে, প্রতিটি নিজের child model হিসেবে hydrate হয়ে — নিজস্ব validation, method আর hook সহ।

            ভালো ব্যবহারের জায়গা: notification (SMS / email / push), payment method (bKash / card / COD), activity-feed event, polymorphic content — "একই ধরনের জিনিস, কয়েকটা field আলাদা, সাধারণত একসাথে list হয়"।
        """,
        ex_en=r"""
            **Pitfalls:**
            - **One collection, shared indexes:** an index declared for a child-only field is still built on the whole collection. Use partial indexes (e.g. on the discriminator key) for child-specific uniqueness.
            - **Inheritance timing:** hooks and methods on the base schema are inherited only if they're added **before** calling `discriminator()`.
            - **Changing type:** switching a document from one discriminator to another isn't a normal update — treat it as a delete + create, or a deliberate migration.
            - **Where the type filter is (and isn't) added:** queries *and* `aggregate()` on a child model get the discriminator filter automatically, but the base model returns every type, and `$lookup` from another collection or native-driver queries (`Model.collection`) don't filter at all — include `{ kind: ... }` yourself there.
            - **When not to use:** if the types are very different, grow at very different rates, or need different retention, separate collections are simpler.
            - **Embedded discriminators** also exist for arrays of subdocuments (e.g. an order's `events` array with different event shapes).
        """,
        ex_bn=r"""
            **Pitfall:**
            - **একটা collection, shared index:** শুধু child-এর field-এর জন্য declare করা index-ও পুরো collection-এ build হয়। Child-specific uniqueness-এর জন্য partial index ব্যবহার করো (যেমন discriminator key-এর ওপর)।
            - **Inheritance-এর সময়:** base schema-র hook আর method তখনই inherit হয়, যদি `discriminator()` call করার **আগে** যোগ করা হয়।
            - **Type বদলানো:** একটা document-কে এক discriminator থেকে আরেকটায় বদলানো সাধারণ update না — এটাকে delete + create বা সচেতন migration হিসেবে দেখো।
            - **Type filter কোথায় যোগ হয় (আর কোথায় হয় না):** child model-এর query *আর* `aggregate()`-এ discriminator filter automatically যোগ হয়, কিন্তু base model সব type return করে, আর অন্য collection থেকে `$lookup` বা native-driver query (`Model.collection`) কোনো filter-ই করে না — সেখানে `{ kind: ... }` নিজেই দিতে হয়।
            - **কখন ব্যবহার করবে না:** type-গুলো খুব আলাদা হলে, খুব ভিন্ন হারে বাড়লে, বা আলাদা retention লাগলে আলাদা collection সহজ।
            - **Embedded discriminator**-ও আছে subdocument-এর array-র জন্য (যেমন order-এর `events` array, যেখানে event-এর shape আলাদা)।
        """,
        tip_en=r"""Explain the storage model in one sentence ("one collection, a type field, automatic filtering"), then give a concrete domain example. Mentioning the shared-index pitfall and where the type filter isn't applied shows you've used it in production.""",
        tip_bn=r"""এক বাক্যে storage model ব্যাখ্যা করো ("একটা collection, একটা type field, automatic filtering"), তারপর একটা concrete domain-এর উদাহরণ দাও। Shared index-এর pitfall আর কোথায় type filter apply হয় না সেটা উল্লেখ করলে বোঝা যায় তুমি production-এ এটা ব্যবহার করেছ।""",
        mist_en=r"""Thinking each discriminator gets its own collection; expecting base-model queries, `$lookup` or `Model.collection` calls to filter by type automatically; adding base hooks after creating discriminators.""",
        mist_bn=r"""ভাবা যে প্রতিটি discriminator-এর আলাদা collection থাকে; base model-এর query, `$lookup` বা `Model.collection` call automatically type অনুযায়ী filter করবে আশা করা; discriminator তৈরির পরে base hook যোগ করা।""",
        code=r"""
            import { Schema, model } from "mongoose";

            const options = { discriminatorKey: "kind", timestamps: true };

            const notificationSchema = new Schema({
              userId: { type: Schema.Types.ObjectId, ref: "User", required: true, index: true },
              status: { type: String, enum: ["queued", "sent", "failed"], default: "queued" },
            }, options);
            const Notification = model("Notification", notificationSchema);

            const SmsNotification = Notification.discriminator("sms",
              new Schema({ phone: { type: String, required: true }, text: String }, options));
            const EmailNotification = Notification.discriminator("email",
              new Schema({ to: { type: String, required: true }, subject: String, html: String }, options));

            await SmsNotification.create({ userId, phone: "+8801711000000", text: "Your OTP is 4821" });

            await Notification.find({ userId });      // both kinds, each hydrated as its own model
            await SmsNotification.find({ userId });   // filter automatically includes { kind: "sms" }
        """,
        lang="javascript",
        follow=[
            ("How would you enforce a unique `phone` only for SMS notifications in a shared collection?", "Shared collection-এ শুধু SMS notification-এর জন্য unique `phone` কীভাবে enforce করবে?"),
        ],
        related=["mongoose-030", "mongoose-002"],
        refs=[DISCRIMINATORS],
    ),
    # ------------------------------------------------------------------ mongoose-028
    Q(
        id="mongoose-028", sub="Virtuals", diff="hard", type="conceptual",
        prio="medium", market="both", mins=8,
        tags=["virtual-populate", "populate", "unbounded-arrays", "perdocumentlimit", "schema-design"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""An `Author` schema stores `posts: [ObjectId]`, and every new post pushes its ID into that array. As some authors reach thousands of posts, this becomes a problem. Why, and how would you redesign it with **virtual populate**? Which populate options keep it efficient?""",
        q_bn=r"""একটা `Author` schema `posts: [ObjectId]` রাখে, আর প্রতিটি নতুন post নিজের ID ওই array-তে push করে। কিছু author-এর post হাজার ছাড়ালে এটা সমস্যা হয়ে দাঁড়ায়। কেন? আর **virtual populate** দিয়ে কীভাবে redesign করবে? কোন populate option এটাকে দক্ষ রাখে?""",
        a_en=r"""
            **Why the array is a problem:** it's an unbounded array — the author document grows forever (toward the 16 MB limit), every new post rewrites a bigger document, and it's a **dual write**: if the post is created but the `$push` fails (or vice versa) the two collections disagree.

            **Redesign:** keep the relationship in **one place** — the child. Each post stores `author`. On the author schema, define a **virtual** that tells Mongoose how to find the posts:
            `authorSchema.virtual("posts", { ref: "Post", localField: "_id", foreignField: "author" })`.

            Nothing is stored on the author; `populate("posts")` runs `Post.find({ author: { $in: authorIds } })` on demand. Index `{ author: 1, createdAt: -1 }` on posts.

            **Options that keep it efficient:**
            - `select` to fetch only list fields, `match` to filter (e.g. only published), `options: { sort: { createdAt: -1 } }`.
            - **`perDocumentLimit: 5`** for "latest 5 posts per author". Plain `limit` is applied to the *single* populate query for all authors (Mongoose uses roughly `limit × number of authors`), so prolific authors can crowd out others — some get fewer or none.
            - **`count: true`** on a virtual returns just the number of posts.

            Remember virtuals appear in JSON only with `toJSON: { virtuals: true }`, and for paginating one author's thousands of posts, query `Post` directly with keyset pagination — populate isn't a pagination tool.
        """,
        a_bn=r"""
            **Array কেন সমস্যা:** এটা unbounded array — author document চিরকাল বাড়তে থাকে (16 MB limit-এর দিকে), প্রতিটি নতুন post একটা আরও বড় document rewrite করায়, আর এটা একটা **dual write**: post তৈরি হলো কিন্তু `$push` fail করল (বা উল্টোটা) — তখন দুই collection-এর তথ্য মেলে না।

            **Redesign:** relationship-টা **এক জায়গায়** রাখো — child-এ। প্রতিটি post `author` রাখে। Author schema-তে একটা **virtual** define করো, যেটা Mongoose-কে বলে post কীভাবে খুঁজতে হবে:
            `authorSchema.virtual("posts", { ref: "Post", localField: "_id", foreignField: "author" })`।

            Author-এ কিছুই store হয় না; `populate("posts")` দরকারমতো `Post.find({ author: { $in: authorIds } })` চালায়। Post-এ `{ author: 1, createdAt: -1 }` index দাও।

            **যে option এটাকে দক্ষ রাখে:**
            - শুধু list-এর field আনতে `select`, filter করতে `match` (যেমন শুধু published), আর `options: { sort: { createdAt: -1 } }`।
            - "প্রতি author-এর সর্বশেষ 5টা post"-এর জন্য **`perDocumentLimit: 5`**। সাধারণ `limit` সব author-এর জন্য চালানো *একটাই* populate query-তে apply হয় (Mongoose মোটামুটি `limit × author সংখ্যা` ব্যবহার করে), ফলে বেশি post-ওয়ালা author-রা বাকিদের জায়গা নিয়ে নিতে পারে — কেউ কেউ কম বা কিছুই পায় না।
            - Virtual-এ **`count: true`** দিলে শুধু post-এর সংখ্যা return করে।

            মনে রেখো, `toJSON: { virtuals: true }` ছাড়া virtual JSON-এ আসে না, আর একজন author-এর হাজার হাজার post paginate করতে সরাসরি `Post` query করো keyset pagination দিয়ে — populate pagination-এর tool না।
        """,
        ex_en=r"""
            - **Cost of `perDocumentLimit`:** to guarantee N per parent, Mongoose runs **one query per parent document**. For a page of 20 authors that's 20 small indexed queries — acceptable, but don't do it for 1,000 authors.
            - **Counts at scale:** `count: true` runs a count per populate; for list pages showing "1,240 posts" for many authors, a stored `postCount` (computed pattern, updated with `$inc`) is cheaper.
            - **Migration path:** backfill `post.author` (usually already there), stop writing to `author.posts`, switch reads to the virtual, then `$unset` the old array.
            - **justOne:** for one-to-one virtuals (e.g. `profile`), set `justOne: true` so the result is a document instead of an array.
            - **Lean:** virtual populate works with `.lean()` too — the populated array is attached to the plain object.
        """,
        ex_bn=r"""
            - **`perDocumentLimit`-এর খরচ:** প্রতি parent-এ N নিশ্চিত করতে Mongoose **প্রতিটি parent document-এর জন্য একটা query** চালায়। 20 জন author-এর একটা page-এ সেটা 20টা ছোট indexed query — গ্রহণযোগ্য, কিন্তু 1,000 author-এর জন্য এটা কোরো না।
            - **বড় scale-এ count:** `count: true` প্রতিটি populate-এ একটা count চালায়; অনেক author-এর জন্য "1,240 posts" দেখানো list page-এ store করা `postCount` (computed pattern, `$inc` দিয়ে update) সস্তা।
            - **Migration-এর পথ:** `post.author` backfill করো (সাধারণত আগে থেকেই থাকে), `author.posts`-এ লেখা বন্ধ করো, read virtual-এ switch করো, তারপর পুরনো array `$unset` করো।
            - **justOne:** one-to-one virtual-এ (যেমন `profile`) `justOne: true` দাও, যাতে result array না হয়ে একটা document হয়।
            - **Lean:** virtual populate `.lean()`-এর সাথেও কাজ করে — populated array plain object-এ যুক্ত হয়।
        """,
        tip_en=r"""Lead with "store the relationship on the child only" and explain the dual-write risk — then show `perDocumentLimit` vs `limit`. That one distinction is something most candidates miss.""",
        tip_bn=r""""Relationship শুধু child-এ রাখো" দিয়ে শুরু করো আর dual-write-এর ঝুঁকি ব্যাখ্যা করো — তারপর `perDocumentLimit` বনাম `limit` দেখাও। এই একটা পার্থক্যই বেশিরভাগ candidate মিস করে।""",
        mist_en=r"""Keeping both `author.posts` and `post.author` "for convenience"; using `limit` and expecting it per author; forgetting `toJSON: { virtuals: true }` and thinking populate failed.""",
        mist_bn=r""""সুবিধার জন্য" `author.posts` আর `post.author` দুটোই রাখা; `limit` দিয়ে প্রতি author-এ আলাদা limit আশা করা; `toJSON: { virtuals: true }` ভুলে গিয়ে ভাবা populate fail করেছে।""",
        code=r"""
            const authorSchema = new Schema(
              { name: String, bio: String },
              { toJSON: { virtuals: true }, toObject: { virtuals: true } }
            );

            authorSchema.virtual("posts", {
              ref: "Post",
              localField: "_id",
              foreignField: "author",
            });

            authorSchema.virtual("postCount", {
              ref: "Post",
              localField: "_id",
              foreignField: "author",
              count: true,
            });

            postSchema.index({ author: 1, createdAt: -1 });

            // Latest 5 published posts for each author on the page
            const authors = await Author.find().limit(20).populate({
              path: "posts",
              select: "title slug createdAt",
              match: { status: "published" },
              options: { sort: { createdAt: -1 } },
              perDocumentLimit: 5,
            });
        """,
        lang="javascript",
        follow=[
            ("How many queries does the example above run, and how would you reduce them?", "উপরের উদাহরণে কয়টা query চলে, আর কীভাবে কমাবে?"),
            ("When would you still keep a bounded array of references on the parent?", "কখন তবুও parent-এ reference-এর একটা bounded array রাখবে?"),
        ],
        related=["mongoose-006", "mongoose-007", "mongoose-015"],
        refs=[POPULATE, VIRTUALS],
    ),
    # ------------------------------------------------------------------ mongoose-029
    Q(
        id="mongoose-029", sub="Connections", diff="hard", type="debugging",
        prio="high", market="both", mins=8,
        tags=["connections", "buffering", "createconnection", "timeouts", "debugging"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""Every request to this endpoint hangs for 10 seconds and then fails with `MongooseError: Operation users.findOne() buffering timed out after 10000ms`. The database is up and reachable from the server. What's the bug, and how would you fix and prevent this class of problem?""",
        q_bn=r"""এই endpoint-এ প্রতিটি request 10 second ঝুলে থাকে, তারপর `MongooseError: Operation users.findOne() buffering timed out after 10000ms` দিয়ে fail করে। Database চালু আছে আর server থেকে reachable। Bug-টা কী, আর কীভাবে fix করবে ও এই ধরনের সমস্যা আটকাবে?""",
        code=r"""
            // db.js
            import mongoose from "mongoose";
            export const conn = mongoose.createConnection(process.env.MONGODB_URI);

            // models/User.js
            import mongoose from "mongoose";
            const userSchema = new mongoose.Schema({ email: String, name: String });
            export const User = mongoose.model("User", userSchema);

            // routes/users.js
            app.get("/users/:id", async (req, res) => {
              res.json(await User.findById(req.params.id));
            });
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            // db.js
            import mongoose from "mongoose";
            export const conn = mongoose.createConnection(process.env.MONGODB_URI, {
              serverSelectionTimeoutMS: 5000,      // fail fast instead of the 30 s default
            });
            conn.on("error", (err) => console.error("MongoDB connection error", err));

            // models/User.js — register the model on the SAME connection
            import { Schema } from "mongoose";
            import { conn } from "../db.js";
            const userSchema = new Schema({ email: String, name: String });
            export const User = conn.model("User", userSchema);

            // server.js — accept traffic only once the database is reachable
            await conn.asPromise();
            app.listen(3000);
        """)],
        a_en=r"""
            **Root cause:** models are always scoped to **one connection**. `mongoose.model()` registers `User` on Mongoose's **default** connection, but the app opened a *separate* connection with `createConnection()` and never called `mongoose.connect()`. So the default connection never opens. Mongoose **buffers** model operations until their connection is ready; after `bufferTimeoutMS` (10 seconds by default) it gives up with this error.

            **Fix:** register the model on the connection you actually opened — `conn.model("User", userSchema)` — or use `mongoose.connect()` + `mongoose.model()` consistently. Then await the connection (`conn.asPromise()`) before the server starts accepting requests.

            **Same symptom, other causes worth checking:** `mongoose.connect()` failing silently (wrong URI, auth failure, Atlas IP access list not including the server's IP, DNS/SRV problems) because nobody listened for `'error'`; or two copies of the `mongoose` package in `node_modules` (common in monorepos), so the models and the connection belong to different Mongoose instances.
        """,
        a_bn=r"""
            **Root cause:** model সবসময় **একটা connection**-এর সাথে যুক্ত থাকে। `mongoose.model()` `User`-কে Mongoose-এর **default** connection-এ register করে, কিন্তু app `createConnection()` দিয়ে একটা *আলাদা* connection খুলেছে আর কখনো `mongoose.connect()` call করেনি। তাই default connection কখনো খোলে না। Connection ready না হওয়া পর্যন্ত Mongoose model operation **buffer** করে রাখে; `bufferTimeoutMS` (default 10 second) পার হলে এই error দিয়ে হাল ছেড়ে দেয়।

            **Fix:** যে connection আসলে খুলেছ, model সেটাতেই register করো — `conn.model("User", userSchema)` — অথবা consistently `mongoose.connect()` + `mongoose.model()` ব্যবহার করো। তারপর server request নেওয়া শুরু করার আগে connection await করো (`conn.asPromise()`)।

            **একই লক্ষণ, অন্য যে কারণগুলো check করা উচিত:** `mongoose.connect()` চুপচাপ fail করা (ভুল URI, auth failure, Atlas IP access list-এ server-এর IP নেই, DNS/SRV সমস্যা), কারণ কেউ `'error'` শোনেনি; অথবা `node_modules`-এ `mongoose` package-এর দুইটা copy (monorepo-তে common), ফলে model আর connection আলাদা Mongoose instance-এর।
        """,
        ex_en=r"""
            - **Why buffering exists:** it lets you define models and even start queries before the connection finishes, which is convenient at startup — but it turns configuration mistakes into mysterious timeouts.
            - **Fail fast:** `mongoose.set("bufferCommands", false)` (or per schema) makes operations error immediately when not connected; a shorter `serverSelectionTimeoutMS` (default 30 s) surfaces unreachable clusters sooner.
            - **Observability:** log connection events (`connected`, `disconnected`, `error`) and expose a health check that verifies the DB (`db.admin().ping()`), so Kubernetes or a load balancer doesn't send traffic to a pod that can't reach MongoDB.
            - **Serverless / Next.js:** create the connection once per process and reuse it — the Mongoose docs suggest a `dbConnect()` helper (calling `mongoose.connect()` when already connected is a no-op) and `mongoose.models.User || mongoose.model(...)` to survive hot reloads.
            - **Multiple databases:** `createConnection()` is the right tool for multi-tenant or read/analytics connections — just keep each model registered on the intended connection.
        """,
        ex_bn=r"""
            - **Buffering কেন আছে:** connection শেষ হওয়ার আগেই model define করা, এমনকি query শুরু করাও যায় — startup-এ এটা সুবিধাজনক — কিন্তু configuration-এর ভুলকে রহস্যময় timeout-এ পরিণত করে।
            - **দ্রুত fail করো:** `mongoose.set("bufferCommands", false)` (বা schema অনুযায়ী) দিলে connected না থাকলে operation সাথে সাথে error দেয়; ছোট `serverSelectionTimeoutMS` (default 30 s) unreachable cluster আরও আগে ধরিয়ে দেয়।
            - **Observability:** connection event (`connected`, `disconnected`, `error`) log করো আর DB যাচাই করে এমন health check দাও (`db.admin().ping()`), যাতে Kubernetes বা load balancer এমন pod-এ traffic না পাঠায় যেটা MongoDB-তে পৌঁছাতে পারে না।
            - **Serverless / Next.js:** প্রতি process-এ একবার connection তৈরি করে আবার ব্যবহার করো — Mongoose docs একটা `dbConnect()` helper (আগে থেকে connected থাকলে `mongoose.connect()` call করা no-op) আর hot reload সামলাতে `mongoose.models.User || mongoose.model(...)`-এর পরামর্শ দেয়।
            - **একাধিক database:** multi-tenant বা read/analytics connection-এর জন্য `createConnection()`-ই সঠিক tool — শুধু প্রতিটি model যেন সঠিক connection-এ register থাকে।
        """,
        tip_en=r"""Explain *why* the error says "buffering" — once you connect it to "models are scoped to a connection", the bug is obvious. Listing other causes with the same symptom shows real debugging experience.""",
        tip_bn=r"""Error-এ কেন "buffering" লেখা, সেটা ব্যাখ্যা করো — "model একটা connection-এর সাথে যুক্ত" কথাটার সাথে মেলালেই bug স্পষ্ট হয়ে যায়। একই লক্ষণের অন্য কারণগুলো বললে আসল debugging অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Increasing `bufferTimeoutMS` to "fix" it; assuming the database is down; mixing `mongoose.model()` with `createConnection()` connections.""",
        mist_bn=r""""Fix" করতে `bufferTimeoutMS` বাড়িয়ে দেওয়া; ধরে নেওয়া database down; `createConnection()`-এর connection-এর সাথে `mongoose.model()` মিশিয়ে ফেলা।""",
        follow=[
            ("How would you connect one app to two databases (main and analytics) with Mongoose?", "Mongoose দিয়ে একটা app-কে দুইটা database-এ (main আর analytics) কীভাবে connect করবে?"),
            ("What should a readiness probe check for a Node.js service that depends on MongoDB?", "MongoDB-নির্ভর একটা Node.js service-এর readiness probe কী check করা উচিত?"),
        ],
        related=["mongoose-001"],
        refs=[CONNECTIONS, NEXTJS],
    ),
]

if __name__ == "__main__":
    save("mongoose", "b4", QUESTIONS)
