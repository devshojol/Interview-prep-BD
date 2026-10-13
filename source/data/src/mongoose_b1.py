# Mongoose — batch 1 (mongoose-001..005, mongoose-012, mongoose-023, mongoose-030)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

GUIDE = ("Mongoose — Schemas guide", "https://mongoosejs.com/docs/guide.html")
MODELS = ("Mongoose — Models", "https://mongoosejs.com/docs/models.html")
DOCUMENTS = ("Mongoose — Documents", "https://mongoosejs.com/docs/documents.html")
SCHEMATYPES = ("Mongoose — SchemaTypes", "https://mongoosejs.com/docs/schematypes.html")
VALIDATION = ("Mongoose — Validation", "https://mongoosejs.com/docs/validation.html")
FAQ = ("Mongoose — FAQ", "https://mongoosejs.com/docs/faq.html")
QUERIES = ("Mongoose — Queries", "https://mongoosejs.com/docs/queries.html")
MODEL_API = ("Mongoose API — Model", "https://mongoosejs.com/docs/api/model.html")
QUERY_API = ("Mongoose API — Query", "https://mongoosejs.com/docs/api/query.html")
FOAU = ("Mongoose — How to Use findOneAndUpdate()", "https://mongoosejs.com/docs/tutorials/findoneandupdate.html")
MIGRATE9 = ("Mongoose — Migrating to 9", "https://mongoosejs.com/docs/migrating_to_9.html")
TRANSACTIONS = ("Mongoose — Transactions", "https://mongoosejs.com/docs/transactions.html")
DISCRIMINATORS = ("Mongoose — Discriminators", "https://mongoosejs.com/docs/discriminators.html")
MONGO_TXN = ("MongoDB Manual — Transactions", "https://www.mongodb.com/docs/manual/core/transactions/")

QUESTIONS = [
    # ------------------------------------------------------------------ mongoose-001
    Q(
        id="mongoose-001", sub="Schemas & Models", diff="easy", type="conceptual",
        prio="high", market="bangladesh", mins=2,
        tags=["schema", "model", "document", "basics"],
        ver="Mongoose 9.11 (concept unchanged since early versions)", vs=False, status="stable",
        q_en=r"""In Mongoose, what is the difference between a schema, a model and a document?""",
        q_bn=r"""Mongoose-এ schema, model আর document-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""
            - A **schema** describes the shape of your data: fields and their types, validators, defaults, indexes, plus middleware, virtuals and methods. It lives only in your Node.js app — MongoDB itself doesn't know about it.
            - A **model** is compiled from a schema with `mongoose.model("User", userSchema)`. It's a class bound to a collection (by default the lowercased plural, `users`) and gives you the query API: `find`, `create`, `updateOne`, and so on.
            - A **document** is an instance of a model — one record. It knows which fields changed, can validate itself, has `save()`, and exposes your virtuals and instance methods.

            In short: schema = blueprint, model = the class/collection API, document = one object built from it.
        """,
        a_bn=r"""
            - **Schema** data-র shape বর্ণনা করে: field আর তাদের type, validator, default, index — সাথে middleware, virtual আর method। এটা শুধু তোমার Node.js app-এ থাকে — MongoDB নিজে এ সম্পর্কে কিছু জানে না।
            - **Model** তৈরি হয় schema থেকে compile করে, `mongoose.model("User", userSchema)` দিয়ে। এটা একটা class যেটা একটা collection-এর সাথে যুক্ত (default-ভাবে lowercase plural নাম, `users`), আর query API দেয়: `find`, `create`, `updateOne` ইত্যাদি।
            - **Document** হলো model-এর একটা instance — একটা record। কোন field বদলেছে তা জানে, নিজেকে validate করতে পারে, এর `save()` আছে, আর তোমার virtual ও instance method ব্যবহার করা যায়।

            সংক্ষেপে: schema = নকশা, model = class/collection API, document = সেখান থেকে তৈরি একটা object।
        """,
        ex_en=r"""
            - **Compile once:** call `mongoose.model()` once per name. Re-compiling in hot-reload environments (e.g. Next.js dev) throws `OverwriteModelError`, which is why you often see `mongoose.models.User || mongoose.model("User", userSchema)`.
            - **Collection name:** override pluralisation with the third argument or the `collection` schema option.
            - **Schema is app-level:** another service writing to the same collection with the native driver bypasses your Mongoose validation — add MongoDB `$jsonSchema` validation if several apps write.
            - **Change tracking:** documents remember modified paths, so `save()` sends only `$set` for what changed (`doc.isModified("email")`).
        """,
        ex_bn=r"""
            - **একবারই compile করো:** প্রতিটি নামের জন্য একবারই `mongoose.model()` call করো। Hot-reload environment-এ (যেমন Next.js dev) আবার compile করলে `OverwriteModelError` হয় — এজন্যই প্রায়ই `mongoose.models.User || mongoose.model("User", userSchema)` দেখা যায়।
            - **Collection-এর নাম:** তৃতীয় argument বা `collection` schema option দিয়ে pluralisation override করা যায়।
            - **Schema app-level:** অন্য কোনো service native driver দিয়ে একই collection-এ লিখলে তোমার Mongoose validation bypass হয়ে যায় — একাধিক app লিখলে MongoDB-র `$jsonSchema` validation যোগ করো।
            - **Change tracking:** document মনে রাখে কোন path বদলেছে, তাই `save()` শুধু বদলানো অংশের জন্য `$set` পাঠায় (`doc.isModified("email")`)।
        """,
        tip_en=r"""Point out that the schema is enforced by Mongoose, not MongoDB — it shows you understand where validation actually happens.""",
        tip_bn=r"""বলো যে schema Mongoose enforce করে, MongoDB না — এতে বোঝা যায় validation আসলে কোথায় হয় সেটা তুমি জানো।""",
        mist_en=r"""Saying MongoDB "stores the schema", or calling `mongoose.model()` inside a request handler on every request.""",
        mist_bn=r"""MongoDB "schema store করে" বলা, অথবা প্রতিটি request-এ request handler-এর ভেতরে `mongoose.model()` call করা।""",
        code=r"""
            import mongoose from "mongoose";

            const userSchema = new mongoose.Schema(
              {
                name: { type: String, required: true, trim: true },
                email: { type: String, required: true, lowercase: true },
                role: { type: String, enum: ["customer", "admin"], default: "customer" },
              },
              { timestamps: true }
            );

            const User = mongoose.model("User", userSchema);   // model → "users" collection

            const user = new User({ name: "Rafi", email: "RAFI@EXAMPLE.COM" }); // document
            console.log(user.email, user.role);   // rafi@example.com customer
            await user.save();
        """,
        lang="javascript",
        follow=[
            ("Why do Next.js projects use `mongoose.models.User || mongoose.model(...)`?", "Next.js project-এ কেন `mongoose.models.User || mongoose.model(...)` ব্যবহার করা হয়?"),
            ("How would you enforce a schema if another service writes to the same collection?", "অন্য একটা service একই collection-এ লিখলে schema কীভাবে enforce করবে?"),
        ],
        refs=[GUIDE, MODELS, DOCUMENTS],
    ),
    # ------------------------------------------------------------------ mongoose-002
    Q(
        id="mongoose-002", sub="Schemas & Models", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["schematypes", "schema-options", "validation", "defaults"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""What are the common SchemaTypes and field options in Mongoose? Show them with a product schema.""",
        q_bn=r"""Mongoose-এ common SchemaType আর field option কী কী? একটা product schema দিয়ে দেখাও।""",
        a_en=r"""
            **SchemaTypes:** `String`, `Number`, `Boolean`, `Date`, `ObjectId` (`Schema.Types.ObjectId`, used for references), arrays like `[String]` or arrays of subdocuments, `Decimal128`, `Map`, `Buffer`, `UUID`, `BigInt` and `Mixed` (anything, no casting — use sparingly).

            **Options for all types:** `required`, `default`, `validate`, `select` (e.g. `select: false` to hide a field), `immutable`, `get`/`set`, and index helpers `index`, `unique`, `sparse`.

            **Type-specific options:** strings have `trim`, `lowercase`, `uppercase`, `match`, `enum`, `minLength`, `maxLength`; numbers have `min`, `max`; dates have `min`, `max` and `expires` (a TTL index).

            **Schema options** apply to the whole schema — `timestamps: true` adds `createdAt`/`updatedAt`, and `toJSON` controls serialisation.
        """,
        a_bn=r"""
            **SchemaType:** `String`, `Number`, `Boolean`, `Date`, `ObjectId` (`Schema.Types.ObjectId`, reference-এর জন্য), `[String]`-এর মতো array বা subdocument-এর array, `Decimal128`, `Map`, `Buffer`, `UUID`, `BigInt` আর `Mixed` (যেকোনো কিছু, casting ছাড়া — কম ব্যবহার করো)।

            **সব type-এর option:** `required`, `default`, `validate`, `select` (যেমন field লুকাতে `select: false`), `immutable`, `get`/`set`, আর index helper `index`, `unique`, `sparse`।

            **Type-specific option:** string-এ `trim`, `lowercase`, `uppercase`, `match`, `enum`, `minLength`, `maxLength`; number-এ `min`, `max`; date-এ `min`, `max` আর `expires` (একটা TTL index)।

            **Schema option** পুরো schema-তে apply হয় — `timestamps: true` দিলে `createdAt`/`updatedAt` যোগ হয়, আর `toJSON` serialisation নিয়ন্ত্রণ করে।
        """,
        ex_en=r"""
            - **Casting:** Mongoose converts values to the declared type — `"42"` becomes `42` for a Number path; a value that can't be cast (e.g. `"abc"` for a Number) produces a `CastError`.
            - **`lowercase`/`trim` are setters**, not validators: they transform the value before saving (and when casting query filters for those paths).
            - **`unique` and `index` are not validators** — they only ask Mongoose to create indexes.
            - **`select: false`** is the standard way to keep `passwordHash` out of normal queries; include it explicitly with `.select("+passwordHash")` in the login flow.
            - **`Mixed`** loses change tracking for nested edits — you must call `doc.markModified("path")`.
            - **Money:** store integer poisha in a `Number` (or use `Decimal128`) instead of floating-point taka.
        """,
        ex_bn=r"""
            - **Casting:** Mongoose value-কে declared type-এ রূপান্তর করে — Number path-এ `"42"` হয়ে যায় `42`; cast করা না গেলে (যেমন Number-এ `"abc"`) `CastError` হয়।
            - **`lowercase`/`trim` হলো setter**, validator না: save-এর আগে value বদলে দেয় (আর ওই path-এর query filter cast করার সময়ও)।
            - **`unique` আর `index` validator না** — এরা শুধু Mongoose-কে index বানাতে বলে।
            - **`select: false`** দিয়েই সাধারণত `passwordHash`-কে normal query থেকে দূরে রাখা হয়; login flow-তে `.select("+passwordHash")` দিয়ে explicitly আনো।
            - **`Mixed`**-এ nested পরিবর্তনের change tracking থাকে না — `doc.markModified("path")` call করতে হয়।
            - **টাকা:** floating-point টাকার বদলে `Number`-এ integer পয়সা রাখো (অথবা `Decimal128` ব্যবহার করো)।
        """,
        tip_en=r"""Group your answer (types → common options → type-specific options → schema options) instead of listing randomly — structure makes even a basic answer sound senior.""",
        tip_bn=r"""এলোমেলো তালিকা না দিয়ে উত্তরটা ভাগ করে বলো (type → common option → type-specific option → schema option) — গোছানো উত্তর একটা basic প্রশ্নকেও senior-level শোনায়।""",
        mist_en=r"""Treating `unique` as validation; using `Mixed` everywhere to "avoid schema problems"; storing prices as floating-point taka.""",
        mist_bn=r"""`unique`-কে validation মনে করা; "schema-র ঝামেলা এড়াতে" সব জায়গায় `Mixed` ব্যবহার করা; দাম floating-point টাকা হিসেবে রাখা।""",
        code=r"""
            import mongoose, { Schema } from "mongoose";

            const productSchema = new Schema(
              {
                name: { type: String, required: [true, "Name is required"], trim: true, maxLength: 120 },
                slug: { type: String, required: true, unique: true, lowercase: true, match: /^[a-z0-9-]+$/ },
                price: { type: Number, required: true, min: 0 },          // integer poisha
                stock: { type: Number, min: 0, default: 0 },
                category: { type: String, enum: ["grocery", "electronics", "fashion"], index: true },
                tags: [String],
                sku: { type: String, immutable: true },
                seller: { type: Schema.Types.ObjectId, ref: "Seller", required: true },
                attributes: { type: Map, of: String },                    // { color: "black", size: "M" }
                costPrice: { type: Number, select: false },               // hidden by default
              },
              { timestamps: true }
            );

            export const Product = mongoose.model("Product", productSchema);
        """,
        lang="javascript",
        follow=[
            ("When would you use a `Map` instead of a nested object?", "কখন nested object-এর বদলে `Map` ব্যবহার করবে?"),
            ("How do you return a field marked `select: false` when you need it?", "`select: false` দেওয়া field দরকার হলে কীভাবে return করবে?"),
        ],
        related=["mongoose-001"],
        refs=[SCHEMATYPES, GUIDE],
    ),
    # ------------------------------------------------------------------ mongoose-003
    Q(
        id="mongoose-003", sub="Validation", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=1,
        tags=["unique", "indexes", "validation", "e11000"],
        ver="Mongoose 9.11 (behaviour unchanged across versions)", vs=False, status="stable",
        q_en=r"""A schema defines `email: { type: String, unique: true }`. Which statement is correct?""",
        q_bn=r"""একটা schema-তে `email: { type: String, unique: true }` define করা আছে। কোন statement-টি সঠিক?""",
        options=[
            ("`unique` is a built-in validator, so `doc.validate()` rejects a duplicate email before any database write",
             "`unique` একটা built-in validator, তাই database write-এর আগেই `doc.validate()` duplicate email reject করে"),
            ("`unique` only tells Mongoose to build a unique index; MongoDB rejects duplicates with an E11000 error — and only if that index actually exists",
             "`unique` শুধু Mongoose-কে একটা unique index বানাতে বলে; MongoDB E11000 error দিয়ে duplicate reject করে — তাও শুধু যদি index-টা আসলেই থাকে"),
            ("`unique` makes Mongoose run a `findOne` before every save to check for duplicates",
             "`unique` দিলে Mongoose প্রতিটি save-এর আগে duplicate check করতে একটা `findOne` চালায়"),
            ("`unique` has no effect unless the field is also `required: true`",
             "Field-টা `required: true` না হলে `unique`-এর কোনো প্রভাব নেই"),
        ],
        correct=1,
        a_en=r"""`unique: true` is an **index helper, not a validator**. Mongoose asks MongoDB to create a unique index (via `autoIndex` or `syncIndexes()`), and it's the **server** that rejects a duplicate with an E11000 duplicate key error. If the index was never built — or failed to build because duplicates already existed — nothing stops duplicates.""",
        a_bn=r"""`unique: true` হলো একটা **index helper, validator না**। Mongoose MongoDB-কে একটা unique index বানাতে বলে (`autoIndex` বা `syncIndexes()` দিয়ে), আর duplicate reject করে **server** — E11000 duplicate key error দিয়ে। Index কখনো build না হলে — বা আগে থেকেই duplicate থাকায় build fail করলে — duplicate আটকানোর কিছুই থাকে না।""",
        ex_en=r"""
            The tempting answer is A, because `unique` sits next to `required` and `min` in the schema. The Mongoose docs explicitly call this a common beginner gotcha.

            Option C describes what the third-party `mongoose-unique-validator` plugin does — and that approach has a race condition (two requests can both pass the `findOne` check). The index is the only reliable guarantee. In practice: make sure the index exists in production (see `syncIndexes()`), normalise values (e.g. `lowercase: true` for emails), and translate `err.code === 11000` into a friendly 409 "email already registered" response.
        """,
        ex_bn=r"""
            সবচেয়ে বিভ্রান্তিকর উত্তর A, কারণ schema-তে `unique` থাকে `required` আর `min`-এর পাশেই। Mongoose docs নিজেই এটাকে beginner-দের common gotcha বলেছে।

            Option C হলো third-party `mongoose-unique-validator` plugin যা করে — আর সেই পদ্ধতিতে race condition আছে (দুইটা request একসাথে `findOne` check পার হয়ে যেতে পারে)। Index-ই একমাত্র নির্ভরযোগ্য guarantee। বাস্তবে: production-এ index আছে কি না নিশ্চিত করো (`syncIndexes()` দেখো), value normalise করো (যেমন email-এ `lowercase: true`), আর `err.code === 11000`-কে একটা friendly 409 "email already registered" response-এ রূপান্তর করো।
        """,
        tip_en=r"""Mention the race condition of "check then insert" — it shows you understand why the database constraint, not application code, must enforce uniqueness.""",
        tip_bn=r""""আগে check, পরে insert"-এর race condition-এর কথা বলো — এতে বোঝা যায় কেন uniqueness application code না, database constraint দিয়েই enforce করতে হয়।""",
        follow=[
            ("How would you turn an E11000 error into a helpful API response?", "E11000 error-কে কীভাবে একটা কাজের API response-এ রূপান্তর করবে?"),
        ],
        related=["mongoose-002"],
        refs=[VALIDATION, FAQ],
    ),
    # ------------------------------------------------------------------ mongoose-004
    Q(
        id="mongoose-004", sub="CRUD", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["crud", "create", "find", "save", "updateone", "async-await"],
        ver="Mongoose 9.11 (`returnDocument` replaces deprecated `new` since 9.2)", vs=True, status="stable",
        q_en=r"""How do you do basic CRUD with Mongoose using async/await? For updates, what's the difference between changing a document and calling `save()` versus calling `Model.updateOne()`?""",
        q_bn=r"""Mongoose-এ async/await দিয়ে basic CRUD কীভাবে করো? Update-এর ক্ষেত্রে document বদলে `save()` call করা আর `Model.updateOne()` call করার মধ্যে পার্থক্য কী?""",
        a_en=r"""
            - **Create:** `Model.create(data)` (or `new Model(data).save()`); `insertMany` for bulk.
            - **Read:** `find(filter)`, `findOne(filter)`, `findById(id)`, chained with `.select()`, `.sort()`, `.limit()`, and `.lean()` for read-only results.
            - **Update:** either load → modify → `save()`, or a direct update command: `updateOne`, `updateMany`, `findOneAndUpdate` / `findByIdAndUpdate`.
            - **Delete:** `deleteOne`, `deleteMany`, `findByIdAndDelete`.

            **`save()` vs `updateOne()`:** `save()` works on a loaded document — it runs full schema validation and `save` middleware, then sends only the changed paths. But it's read-modify-write, so two concurrent requests can overwrite each other. `updateOne()` sends one atomic command (e.g. `$inc`) without loading the document — faster and safe for counters — but `save` hooks don't run and validators run only if you pass `runValidators: true` (and even then only for operators like `$set`/`$push`, not `$inc`).
        """,
        a_bn=r"""
            - **Create:** `Model.create(data)` (অথবা `new Model(data).save()`); bulk-এর জন্য `insertMany`।
            - **Read:** `find(filter)`, `findOne(filter)`, `findById(id)`, সাথে chain করে `.select()`, `.sort()`, `.limit()`, আর read-only result-এর জন্য `.lean()`।
            - **Update:** হয় load → modify → `save()`, নয়তো সরাসরি update command: `updateOne`, `updateMany`, `findOneAndUpdate` / `findByIdAndUpdate`।
            - **Delete:** `deleteOne`, `deleteMany`, `findByIdAndDelete`।

            **`save()` বনাম `updateOne()`:** `save()` load করা document-এর ওপর কাজ করে — পুরো schema validation আর `save` middleware চালায়, তারপর শুধু বদলানো path পাঠায়। কিন্তু এটা read-modify-write, তাই দুইটা concurrent request একে অপরের পরিবর্তন overwrite করতে পারে। `updateOne()` document load না করেই একটা atomic command (যেমন `$inc`) পাঠায় — দ্রুত আর counter-এর জন্য নিরাপদ — কিন্তু `save` hook চলে না, আর `runValidators: true` না দিলে validator-ও চলে না (দিলেও শুধু `$set`/`$push`-এর মতো operator-এ চলে, `$inc`-এ না)।
        """,
        ex_en=r"""
            - **Return values:** `find()` → array (empty if nothing matches); `findOne()`/`findById()` → document or `null`; `updateOne()` → `{ acknowledged, matchedCount, modifiedCount, ... }`; `deleteOne()` → `{ deletedCount }`.
            - **Returning the updated document:** `findOneAndUpdate(filter, update, { returnDocument: "after" })`. The old `{ new: true }` option still works but has been deprecated since Mongoose 9.2.
            - **Queries are thenables:** `await Model.find()` executes it; `.exec()` gives a real Promise and better stack traces. Callbacks were removed in Mongoose 7.
            - **Counters, stock, balances:** prefer atomic operators (`$inc`, `$push`) over load-modify-save.
        """,
        ex_bn=r"""
            - **Return value:** `find()` → array (কিছু match না করলে খালি); `findOne()`/`findById()` → document বা `null`; `updateOne()` → `{ acknowledged, matchedCount, modifiedCount, ... }`; `deleteOne()` → `{ deletedCount }`।
            - **Update হওয়া document ফেরত পেতে:** `findOneAndUpdate(filter, update, { returnDocument: "after" })`। পুরনো `{ new: true }` option এখনো কাজ করে, কিন্তু Mongoose 9.2 থেকে deprecated।
            - **Query হলো thenable:** `await Model.find()` দিলেই execute হয়; `.exec()` আসল Promise আর ভালো stack trace দেয়। Mongoose 7-এ callback সরিয়ে দেওয়া হয়েছে।
            - **Counter, stock, balance:** load-modify-save-এর বদলে atomic operator (`$inc`, `$push`) ব্যবহার করো।
        """,
        tip_en=r"""When comparing `save()` and `updateOne()`, mention concurrency ("lost updates") — that's the detail most juniors miss and interviewers listen for.""",
        tip_bn=r"""`save()` আর `updateOne()` তুলনা করার সময় concurrency ("lost update")-এর কথা বলো — বেশিরভাগ junior এটাই মিস করে, আর interviewer ঠিক এটাই শুনতে চায়।""",
        mist_en=r"""Expecting `updateOne()` to trigger `pre('save')` hooks; using `{ new: true }` in new Mongoose 9 code; decrementing stock with `doc.stock -= 1; await doc.save()` under concurrency.""",
        mist_bn=r"""`updateOne()`-এ `pre('save')` hook চলবে আশা করা; নতুন Mongoose 9 code-এ `{ new: true }` ব্যবহার করা; concurrency থাকা অবস্থায় `doc.stock -= 1; await doc.save()` দিয়ে stock কমানো।""",
        code=r"""
            // Create
            const product = await Product.create({ name: "Earbuds", slug: "earbuds", price: 189900, stock: 10, seller });

            // Read
            const one = await Product.findById(product._id);
            const cheap = await Product.find({ price: { $lte: 200000 } }).sort({ price: 1 }).limit(20).lean();

            // Update (a): load → change → save  (full validation + save hooks)
            one.name = "QCY Earbuds";
            await one.save();

            // Update (b): one atomic command (no save hooks). Guard stock in the filter:
            // update validators (runValidators) don't check $inc, so min: 0 won't stop it
            await Product.updateOne({ _id: product._id, stock: { $gte: 1 } }, { $inc: { stock: -1 } });

            // Update and get the new version back
            const updated = await Product.findOneAndUpdate(
              { _id: product._id },
              { $set: { price: 179900 } },
              { returnDocument: "after", runValidators: true }
            );

            // Delete
            await Product.deleteOne({ _id: product._id });
        """,
        lang="javascript",
        follow=[
            ("Two requests decrement stock at the same time using `save()`. What can go wrong?", "দুইটা request একই সময়ে `save()` দিয়ে stock কমালে কী সমস্যা হতে পারে?"),
            ("When would you choose `insertMany` over `create` with an array?", "কখন array সহ `create`-এর বদলে `insertMany` বেছে নেবে?"),
        ],
        related=["mongoose-001", "mongoose-002"],
        refs=[MODELS, QUERIES, FOAU],
    ),
    # ------------------------------------------------------------------ mongoose-005
    Q(
        id="mongoose-005", sub="Documents & Queries", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=1,
        tags=["findone", "null", "orfail", "queries"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""What does `await User.findOne({ email: "nobody@example.com" })` return when no document matches?""",
        q_bn=r"""কোনো document match না করলে `await User.findOne({ email: "nobody@example.com" })` কী return করে?""",
        options=[
            (r"""An empty array `[]`""",
             r"""একটা খালি array `[]`"""),
            (r"""It throws a `DocumentNotFoundError`""",
             r"""একটা `DocumentNotFoundError` throw করে"""),
            (r"""An empty document `{}`""",
             r"""একটা খালি document `{}`"""),
            (r"""`null`""",
             r"""`null`"""),
        ],
        correct=3,
        a_en=r"""`findOne()` and `findById()` resolve to `null` when nothing matches; `find()` resolves to an empty array. Your code has to check for `null` — usually by returning a 404.""",
        a_bn=r"""কিছু match না করলে `findOne()` আর `findById()` `null` দেয়; `find()` দেয় একটা খালি array। তাই code-এ `null` check করতে হয় — সাধারণত 404 return করে।""",
        ex_en=r"""
            Option B is tempting because `DocumentNotFoundError` does exist — but it's only thrown when you opt in with `.orFail()` (or when `save()` can't find the document it's updating). `.orFail()` is handy in Express 5, where a thrown error in an async handler goes straight to your error middleware:

            `const user = await User.findById(id).orFail();`

            Option A is the `find()` behaviour. Forgetting the `null` check leads to the classic `TypeError: Cannot read properties of null` in production logs.
        """,
        ex_bn=r"""
            Option B বিভ্রান্তিকর, কারণ `DocumentNotFoundError` আসলেই আছে — কিন্তু এটা throw হয় শুধু তখনই যখন তুমি `.orFail()` দিয়ে opt in করো (অথবা `save()` যে document update করছে সেটা খুঁজে না পেলে)। Express 5-এ `.orFail()` কাজের, কারণ async handler-এ throw হওয়া error সরাসরি error middleware-এ চলে যায়:

            `const user = await User.findById(id).orFail();`

            Option A হলো `find()`-এর আচরণ। `null` check ভুলে গেলে production log-এ classic `TypeError: Cannot read properties of null` দেখা যায়।
        """,
        tip_en=r"""Contrast all three — `find` → `[]`, `findOne` → `null`, `.orFail()` → throws — it shows you know the API surface, not just one method.""",
        tip_bn=r"""তিনটাই তুলনা করে বলো — `find` → `[]`, `findOne` → `null`, `.orFail()` → throw — এতে বোঝা যায় তুমি শুধু একটা method না, পুরো API জানো।""",
        follow=[
            ("How would you map `DocumentNotFoundError` to a 404 in Express?", "Express-এ `DocumentNotFoundError`-কে কীভাবে 404-এ map করবে?"),
        ],
        related=["mongoose-004"],
        refs=[QUERY_API, MODEL_API],
    ),
    # ------------------------------------------------------------------ mongoose-012
    Q(
        id="mongoose-012", sub="Validation", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["update-validators", "runvalidators", "findbyidandupdate", "returndocument", "mass-assignment"],
        ver="Mongoose 9.11 (`new` deprecated since 9.2), Express 5, zod 4", vs=True, status="stable",
        q_en=r"""This PATCH endpoint accepts `{ "price": -500, "status": "deleted" }` and saves it without any error, even though the schema has `min: 0` and an `enum`. Why, and what else is wrong with it?""",
        q_bn=r"""এই PATCH endpoint `{ "price": -500, "status": "deleted" }` নিয়ে কোনো error ছাড়াই save করে ফেলে, যদিও schema-তে `min: 0` আর `enum` আছে। কেন? আর এতে আর কী কী সমস্যা আছে?""",
        code=r"""
            const productSchema = new mongoose.Schema({
              name: { type: String, required: true },
              price: { type: Number, required: true, min: 0 },
              status: { type: String, enum: ["draft", "active", "archived"], default: "draft" },
            });
            const Product = mongoose.model("Product", productSchema);

            app.patch("/products/:id", async (req, res) => {
              const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
              res.json(product);
            });
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            import { z } from "zod";

            const PatchProduct = z.strictObject({
              name: z.string().min(1).max(120).optional(),
              price: z.number().int().nonnegative().optional(),
              status: z.enum(["draft", "active", "archived"]).optional(),
            });

            app.patch("/products/:id", async (req, res) => {
              const changes = PatchProduct.parse(req.body);   // ZodError → 400 in error middleware

              const product = await Product.findByIdAndUpdate(
                req.params.id,
                { $set: changes },
                { returnDocument: "after", runValidators: true }
              );
              if (!product) return res.status(404).json({ error: "Product not found" });
              res.json(product);
            });
        """)],
        a_en=r"""
            **Root cause:** schema validators run on `save()`/`create()`, but **update validators are off by default** for `updateOne`, `updateMany` and `findOneAndUpdate` (which `findByIdAndUpdate` uses). The update goes straight to MongoDB, so `min` and `enum` are never checked. Fix: pass `runValidators: true`.

            **Other problems:**
            1. `{ new: true }` is deprecated since Mongoose 9.2 — use `returnDocument: "after"`.
            2. **Mass assignment:** passing `req.body` as the update lets a client change any schema field, and even send operators like `$unset`. Validate and whitelist fields (zod), then wrap them in `$set`.
            3. **Missing document:** `findByIdAndUpdate` returns `null` if the ID doesn't exist, so the API answers `200 null` instead of 404.
            4. An invalid ID like `"abc"` throws a `CastError` — handle it as a 400 in error middleware (Express 5 forwards rejected promises automatically).
        """,
        a_bn=r"""
            **Root cause:** schema validator চলে `save()`/`create()`-এ, কিন্তু `updateOne`, `updateMany` আর `findOneAndUpdate`-এ (`findByIdAndUpdate` এটাই ব্যবহার করে) **update validator default-ভাবে বন্ধ থাকে**। Update সরাসরি MongoDB-তে চলে যায়, তাই `min` আর `enum` কখনো check হয় না। Fix: `runValidators: true` দাও।

            **আরও সমস্যা:**
            1. `{ new: true }` Mongoose 9.2 থেকে deprecated — `returnDocument: "after"` ব্যবহার করো।
            2. **Mass assignment:** `req.body`-কে সরাসরি update হিসেবে দিলে client যেকোনো schema field বদলাতে পারে, এমনকি `$unset`-এর মতো operator-ও পাঠাতে পারে। Field validate আর whitelist করো (zod), তারপর `$set`-এ মুড়ে দাও।
            3. **Document না থাকা:** ID না থাকলে `findByIdAndUpdate` `null` return করে, তাই API 404-এর বদলে `200 null` দেয়।
            4. `"abc"`-এর মতো invalid ID দিলে `CastError` throw হয় — error middleware-এ এটাকে 400 হিসেবে handle করো (Express 5 rejected promise automatically forward করে)।
        """,
        ex_en=r"""
            **How update validators differ from document validation:**
            - They only run on these operators: `$set`, `$unset`, `$push`, `$addToSet`, `$pull`, `$pullAll` — so a `$inc` that makes stock negative isn't caught by `min: 0`. Guard such cases in the filter instead (`{ stock: { $gte: qty } }`).
            - They only validate the **paths in the update**, not the whole document.
            - `required` validators only fail when you explicitly `$unset` the field.
            - Inside a custom validator, `this` is the **query**, not the document — validators that read other fields via `this.otherField` break in updates.

            **Alternative:** load the document, assign the allowed fields, and call `save()` — you get full validation and `save` hooks, at the cost of an extra read and read-modify-write semantics. Many teams also set `runValidators` globally with a plugin or `mongoose.set('runValidators', true)`.
        """,
        ex_bn=r"""
            **Update validator আর document validation-এর পার্থক্য:**
            - এরা শুধু এই operator-গুলোতে চলে: `$set`, `$unset`, `$push`, `$addToSet`, `$pull`, `$pullAll` — তাই stock negative করে ফেলা `$inc` `min: 0` দিয়ে ধরা পড়ে না। এমন ক্ষেত্রে filter-এই guard দাও (`{ stock: { $gte: qty } }`)।
            - এরা শুধু **update-এ থাকা path** validate করে, পুরো document না।
            - `required` validator শুধু তখনই fail করে যখন তুমি explicitly field-টা `$unset` করো।
            - Custom validator-এর ভেতরে `this` হলো **query**, document না — যেসব validator `this.otherField` দিয়ে অন্য field পড়ে, সেগুলো update-এ ভেঙে যায়।

            **বিকল্প:** document load করে allowed field assign করো, তারপর `save()` call করো — পুরো validation আর `save` hook পাবে, তবে একটা বাড়তি read আর read-modify-write-এর ঝুঁকি থাকবে। অনেক team plugin বা `mongoose.set('runValidators', true)` দিয়ে globally `runValidators` চালু করে।
        """,
        tip_en=r"""Lead with the root cause in one sentence ("update validators are opt-in"), then list the secondary issues by severity. Spotting the mass-assignment risk unprompted is a strong signal.""",
        tip_bn=r"""এক বাক্যে root cause দিয়ে শুরু করো ("update validator opt-in"), তারপর গুরুত্ব অনুযায়ী বাকি সমস্যাগুলো বলো। নিজে থেকে mass-assignment-এর ঝুঁকি ধরতে পারলে খুব ভালো signal যায়।""",
        mist_en=r"""Assuming schema validation always runs; relying on `runValidators` to catch `$inc` going negative; trusting `req.body` as an update document.""",
        mist_bn=r"""ধরে নেওয়া যে schema validation সবসময় চলে; `$inc` দিয়ে negative হওয়া ধরতে `runValidators`-এর ওপর ভরসা করা; `req.body`-কে update document হিসেবে বিশ্বাস করা।""",
        follow=[
            ("How would you validate a rule that compares two fields (e.g. `salePrice < price`) in both save and update paths?", "দুইটা field তুলনা করে এমন rule (যেমন `salePrice < price`) save আর update — দুই পথেই কীভাবে validate করবে?"),
            ("Why might a team prefer load-and-save over `findByIdAndUpdate` for admin edits?", "Admin edit-এর জন্য একটা team কেন `findByIdAndUpdate`-এর বদলে load-and-save পছন্দ করতে পারে?"),
        ],
        related=["mongoose-003", "mongoose-004"],
        refs=[VALIDATION, FOAU, MIGRATE9],
    ),
    # ------------------------------------------------------------------ mongoose-023
    Q(
        id="mongoose-023", sub="Transactions", diff="hard", type="debugging",
        prio="high", market="both", mins=10,
        tags=["transactions", "session", "connection-transaction", "promise-all", "side-effects", "inventory"],
        ver="Mongoose 9.11 (Connection#transaction), MongoDB 9.0 replica set", vs=False, status="stable",
        q_en=r"""This checkout function uses a Mongoose transaction, but in production the team sees stock decreasing for orders that were never created, occasional overselling, and customers receiving the "order placed" SMS two or three times. Find the bugs.""",
        q_bn=r"""এই checkout function একটা Mongoose transaction ব্যবহার করে, কিন্তু production-এ team দেখছে যে কখনো তৈরিই হয়নি এমন order-এর জন্য stock কমে যাচ্ছে, মাঝে মাঝে overselling হচ্ছে, আর customer-রা "order placed" SMS দুই-তিনবার পাচ্ছে। Bug-গুলো খুঁজে বের করো।""",
        code=r"""
            async function placeOrder(user, items) {
              return mongoose.connection.transaction(async (session) => {
                const [order] = await Order.create(
                  [{ user: user._id, items, status: "pending" }],
                  { session }
                );

                await Promise.all(items.map((item) =>
                  Product.updateOne(
                    { _id: item.productId, stock: { $gte: item.qty } },
                    { $inc: { stock: -item.qty } }
                  )
                ));

                await User.updateOne({ _id: user._id }, { $inc: { orderCount: 1 } }, { session });
                await sms.send(user.phone, `Order ${order._id} placed`);
                return order;
              });
            }
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            async function placeOrder(user, items) {
              let order;
              await mongoose.connection.transaction(async (session) => {
                for (const item of items) {                      // sequential — never Promise.all
                  const res = await Product.updateOne(
                    { _id: item.productId, stock: { $gte: item.qty } },
                    { $inc: { stock: -item.qty } },
                    { session }                                   // part of the transaction
                  );
                  if (res.matchedCount === 0) {
                    throw new OutOfStockError(item.productId);    // aborts everything
                  }
                }

                [order] = await Order.create(
                  [{ user: user._id, items, status: "pending" }],
                  { session }
                );
                await User.updateOne({ _id: user._id }, { $inc: { orderCount: 1 } }, { session });
              });

              // Side effects only after a successful commit (or via an outbox + worker)
              await sms.send(user.phone, `Order ${order._id} placed`);
              return order;
            }
        """)],
        a_en=r"""
            1. **Missing `{ session }` on `Product.updateOne`.** Without the session the stock update runs **outside** the transaction and commits immediately. If the transaction later aborts (or is retried), the order disappears but the stock stays decremented — that's the "stock gone, no order" symptom. Every operation inside must receive the session.
            2. **`Promise.all` inside a transaction.** Running operations in parallel on one transaction/session isn't supported — Mongoose's docs call it undefined behaviour. Use a sequential `for...of`.
            3. **Ignoring `matchedCount`.** When stock is insufficient, the conditional update matches nothing — no error — and the order is still created. That's the overselling. Check `matchedCount` and throw to abort.
            4. **SMS inside the callback.** `connection.transaction()` wraps `withTransaction()`, which **re-runs the whole callback** on transient errors (write conflicts are common during a sale). Each attempt sends another SMS, and if the commit ultimately fails the customer was told about an order that doesn't exist. Do side effects after commit, or write an "outbox" document in the transaction and let a worker send it exactly once.

            `Order.create([doc], { session })` itself is correct — passing options to `create()` requires the array form.
        """,
        a_bn=r"""
            1. **`Product.updateOne`-এ `{ session }` নেই।** Session ছাড়া stock update transaction-এর **বাইরে** চলে আর সাথে সাথে commit হয়ে যায়। পরে transaction abort (বা retry) হলে order মুছে যায় কিন্তু stock কমেই থাকে — এটাই "stock নেই, order নেই" লক্ষণ। ভেতরের প্রতিটি operation-এ session দিতে হবে।
            2. **Transaction-এর ভেতরে `Promise.all`।** একটা transaction/session-এ parallel-ভাবে operation চালানো support করে না — Mongoose docs এটাকে undefined behaviour বলে। Sequential `for...of` ব্যবহার করো।
            3. **`matchedCount` উপেক্ষা করা।** Stock কম থাকলে conditional update কিছুই match করে না — কোনো error হয় না — তবুও order তৈরি হয়ে যায়। এটাই overselling। `matchedCount` check করে throw করো, যাতে abort হয়।
            4. **Callback-এর ভেতরে SMS।** `connection.transaction()` আসলে `withTransaction()`-কে wrap করে, যেটা transient error-এ **পুরো callback আবার চালায়** (sale-এর সময় write conflict খুব common)। প্রতিটি চেষ্টায় আরেকটা SMS যায়, আর শেষে commit fail করলে customer এমন order-এর খবর পায় যেটা আসলে নেই। Side effect commit-এর পরে করো, অথবা transaction-এর ভেতরে একটা "outbox" document লিখে worker দিয়ে ঠিক একবার পাঠাও।

            `Order.create([doc], { session })` নিজে ঠিক আছে — `create()`-এ option দিতে হলে array form-ই লাগে।
        """,
        ex_en=r"""
            - **Why not rely on the return value?** The fixed version assigns `order` from inside the callback, so it doesn't depend on what `transaction()` resolves to, and each retry simply overwrites it.
            - **Document state on abort:** `connection.transaction()` also resets Mongoose's change tracking for documents saved in an aborted attempt, so a retry re-sends their changes — one advantage over calling `session.withTransaction()` directly.
            - **Forgetting sessions is easy:** `mongoose.set('transactionAsyncLocalStorage', true)` makes Mongoose pass the session automatically to operations inside `connection.transaction()`.
            - **Keep it short:** the transaction should contain only database writes. No HTTP calls (payment gateway, SMS) inside — they're slow, can't be rolled back, and may run multiple times.
            - **Testing:** run integration tests against a replica set (e.g. `mongodb-memory-server`'s replica set mode) and simulate concurrent checkouts for the last unit.
        """,
        ex_bn=r"""
            - **Return value-এর ওপর কেন নির্ভর না?** Fixed version-এ `order` callback-এর ভেতর থেকেই assign হয়, তাই `transaction()` কী resolve করে তার ওপর নির্ভর করে না, আর প্রতিটি retry শুধু value-টা overwrite করে।
            - **Abort-এ document-এর state:** `connection.transaction()` abort হওয়া চেষ্টায় save করা document-এর change tracking-ও reset করে, ফলে retry-তে সেই পরিবর্তন আবার পাঠানো হয় — সরাসরি `session.withTransaction()` call করার চেয়ে এটা একটা সুবিধা।
            - **Session ভুলে যাওয়া সহজ:** `mongoose.set('transactionAsyncLocalStorage', true)` দিলে `connection.transaction()`-এর ভেতরের operation-এ Mongoose নিজেই session পাঠিয়ে দেয়।
            - **ছোট রাখো:** transaction-এ শুধু database write থাকবে। ভেতরে কোনো HTTP call (payment gateway, SMS) না — এগুলো slow, rollback করা যায় না, আর একাধিকবার চলতে পারে।
            - **Testing:** replica set-এর বিরুদ্ধে integration test চালাও (যেমন `mongodb-memory-server`-এর replica set mode) আর শেষ unit-এর জন্য concurrent checkout simulate করো।
        """,
        tip_en=r"""Map each symptom to its bug ("stock gone, no order" → missing session; "duplicate SMS" → retried callback). Symptom-to-cause reasoning is exactly what production debugging interviews test.""",
        tip_bn=r"""প্রতিটি লক্ষণকে তার bug-এর সাথে মেলাও ("stock নেই, order নেই" → session নেই; "duplicate SMS" → retry হওয়া callback)। লক্ষণ থেকে কারণ বের করার যুক্তিই production debugging interview-তে যাচাই করা হয়।""",
        mist_en=r"""Thinking that code inside the callback is automatically transactional; using `Promise.all` for speed; assuming the callback runs exactly once.""",
        mist_bn=r"""ভাবা যে callback-এর ভেতরের সব code automatically transactional; speed-এর জন্য `Promise.all` ব্যবহার করা; ধরে নেওয়া যে callback ঠিক একবারই চলে।""",
        follow=[
            ("How would you implement the outbox pattern for the SMS?", "SMS-এর জন্য outbox pattern কীভাবে implement করবে?"),
            ("What happens to the stock if the payment fails after the order is created?", "Order তৈরির পর payment fail করলে stock-এর কী হবে?"),
        ],
        related=["mongoose-004"],
        refs=[TRANSACTIONS, MONGO_TXN],
    ),
    # ------------------------------------------------------------------ mongoose-030
    Q(
        id="mongoose-030", sub="Schema Design", diff="extreme", type="system-design",
        prio="medium", market="both", mins=20,
        tags=["system-design", "e-commerce", "marketplace", "discriminators", "transactions", "inventory"],
        ver="Mongoose 9.11, MongoDB 9.0 replica set", vs=False, status="stable",
        q_en=r"""Design the Mongoose models and data-access approach for a multi-vendor marketplace: one customer checkout can contain items from several sellers, each seller ships their part separately, stock must not oversell during 11.11-style campaigns (≈20× normal traffic), and payments come via bKash, card or cash on delivery.""",
        q_bn=r"""একটা multi-vendor marketplace-এর জন্য Mongoose model আর data-access পদ্ধতি design করো: একজন customer-এর এক checkout-এ কয়েকজন seller-এর item থাকতে পারে, প্রতিটি seller নিজের অংশ আলাদাভাবে ship করে, 11.11-এর মতো campaign-এ (স্বাভাবিকের ≈20 গুণ traffic) stock oversell হওয়া চলবে না, আর payment আসে bKash, card বা cash on delivery-তে।""",
        a_en=r"""
            *(Advanced, senior-level design question.)*

            **Models:**
            - `Product` with a bounded array of embedded variants; **`Inventory`** as a separate small document per SKU (`available`, `reserved`). Keeping hot stock counters out of the big product document reduces write contention and document rewrites.
            - `Order` — the customer-level record: `checkoutId` (unique idempotency key), customer, shipping-address snapshot, totals, payment status. `optimisticConcurrency: true` so concurrent admin edits fail loudly instead of overwriting.
            - `SellerOrder` — one per seller per order, with item snapshots (name, SKU, unit price in poisha, qty) and its own status/tracking. Sellers update and query only their own part: index `{ sellerId: 1, status: 1, createdAt: -1 }`.
            - `Payment` — one collection with **discriminators** per method (`bkash`, `card`, `cod`) because each has different fields; a unique partial index on the gateway transaction ID makes webhook handling idempotent.

            **Checkout (one short transaction):** for each SKU, a conditional `$inc` on `Inventory` (`available ≥ qty`), checking `matchedCount`; then create `Order`, `SellerOrder`s and a pending `Payment` — all with the session, sequentially. Side effects (SMS, seller notifications) go through an outbox after commit.

            **Payment confirmation:** the bKash/card webhook updates `Payment` + `Order` in a transaction, guarded by the unique transaction ID so duplicate callbacks are harmless. Unpaid reservations are released by a worker after a timeout (re-increment `available`).

            **Read paths:** "My orders" `{ customerId: 1, createdAt: -1 }` with `.lean()` and projections; seller dashboards on `SellerOrder`; admin analytics from pre-aggregated stats or an analytics node, never by populating millions of documents.

            **Campaign scale:** cache product pages (Redis/CDN), size `maxPoolSize` per instance against the cluster's connection limit, rate-limit checkout, and consider a queue/waiting room for flash deals so the database sees a controlled write rate.
        """,
        a_bn=r"""
            *(Advanced, senior-level design প্রশ্ন।)*

            **Model:**
            - `Product`-এ embedded variant-এর bounded array; আর প্রতিটি SKU-র জন্য আলাদা ছোট document হিসেবে **`Inventory`** (`available`, `reserved`)। Hot stock counter বড় product document-এর বাইরে রাখলে write contention আর document rewrite কমে।
            - `Order` — customer-level record: `checkoutId` (unique idempotency key), customer, shipping address-এর snapshot, total, payment status। `optimisticConcurrency: true`, যাতে concurrent admin edit চুপচাপ overwrite না করে স্পষ্টভাবে fail করে।
            - `SellerOrder` — প্রতি order-এ প্রতিটি seller-এর জন্য একটা, item snapshot (name, SKU, পয়সায় unit price, qty) আর নিজস্ব status/tracking সহ। Seller শুধু নিজের অংশ update আর query করে: index `{ sellerId: 1, status: 1, createdAt: -1 }`।
            - `Payment` — একটা collection, প্রতিটি method-এর জন্য **discriminator** (`bkash`, `card`, `cod`), কারণ প্রত্যেকের field আলাদা; gateway transaction ID-তে unique partial index থাকলে webhook handling idempotent হয়।

            **Checkout (একটা ছোট transaction):** প্রতিটি SKU-র জন্য `Inventory`-তে conditional `$inc` (`available ≥ qty`), `matchedCount` check সহ; তারপর `Order`, `SellerOrder` আর pending `Payment` তৈরি — সবগুলো session সহ, একটার পর একটা। Side effect (SMS, seller notification) commit-এর পরে outbox দিয়ে যায়।

            **Payment confirmation:** bKash/card webhook একটা transaction-এ `Payment` + `Order` update করে, unique transaction ID দিয়ে সুরক্ষিত, তাই duplicate callback ক্ষতি করে না। Pay না করা reservation একটা worker timeout-এর পর ছেড়ে দেয় (`available` আবার বাড়ায়)।

            **Read path:** "My orders"-এর জন্য `{ customerId: 1, createdAt: -1 }`, `.lean()` আর projection সহ; seller dashboard `SellerOrder`-এর ওপর; admin analytics pre-aggregated stats বা analytics node থেকে — লক্ষ লক্ষ document populate করে কখনো না।

            **Campaign-এর scale:** product page cache করো (Redis/CDN), cluster-এর connection limit অনুযায়ী প্রতিটি instance-এর `maxPoolSize` ঠিক করো, checkout rate-limit করো, আর flash deal-এর জন্য queue/waiting room ভাবো, যাতে database একটা নিয়ন্ত্রিত write rate দেখে।
        """,
        ex_en=r"""
            **Trade-offs and failure scenarios:**
            - **Embedding vs separate `SellerOrder`:** embedding seller groups inside `Order` gives one-read order pages, but every seller update rewrites the shared document and seller dashboards need multikey queries. A separate collection isolates writes and indexes per seller.
            - **Hot SKUs:** a flash-deal SKU can get thousands of decrements per second on one document. Options: pre-split stock into N inventory shards (`sku#1..N`) and pick one randomly, or queue purchase requests and process them sequentially.
            - **Payment succeeded, order transaction failed:** run a reconciliation job against gateway records; never trust only the redirect URL — rely on the server-to-server callback or a status query.
            - **COD:** stock is reserved at checkout but cash is collected later; returns and failed deliveries must re-increment stock through the same idempotent path.
            - **Mongoose specifics:** `.lean()` for list endpoints, `select: false` for sensitive fields, `autoIndex: false` in production with indexes managed by migrations, and `discriminatorKey` chosen explicitly (`method`) instead of the default `__t`.
        """,
        ex_bn=r"""
            **Trade-off আর failure scenario:**
            - **Embed বনাম আলাদা `SellerOrder`:** seller group `Order`-এর ভেতরে embed করলে এক read-এ order page হয়, কিন্তু প্রতিটি seller update shared document rewrite করে, আর seller dashboard-এ multikey query লাগে। আলাদা collection প্রতিটি seller-এর write আর index আলাদা রাখে।
            - **Hot SKU:** flash-deal-এর একটা SKU-তে এক document-এ প্রতি second হাজার হাজার decrement আসতে পারে। উপায়: stock আগে থেকেই Nটা inventory shard-এ ভাগ করা (`sku#1..N`) আর random-ভাবে একটা বেছে নেওয়া, অথবা purchase request queue করে একটার পর একটা process করা।
            - **Payment সফল, order transaction fail:** gateway-র record-এর সাথে reconciliation job চালাও; শুধু redirect URL-এর ওপর ভরসা কোরো না — server-to-server callback বা status query-র ওপর নির্ভর করো।
            - **COD:** checkout-এ stock reserve হয় কিন্তু টাকা পরে আসে; return আর failed delivery-তে একই idempotent পথে stock আবার বাড়াতে হয়।
            - **Mongoose-এর দিক:** list endpoint-এ `.lean()`, sensitive field-এ `select: false`, production-এ `autoIndex: false` আর migration দিয়ে index management, আর default `__t`-এর বদলে explicitly বেছে নেওয়া `discriminatorKey` (`method`)।
        """,
        tip_en=r"""Anchor the design on two invariants — "never oversell" and "never charge without an order" — and show how each model and transaction protects them. Naming failure scenarios unprompted is what makes it an extreme-level answer.""",
        tip_bn=r"""Design-টা দুইটা invariant-এর ওপর দাঁড় করাও — "কখনো oversell না" আর "order ছাড়া কখনো charge না" — আর দেখাও প্রতিটি model আর transaction কীভাবে এগুলো রক্ষা করে। নিজে থেকে failure scenario বলাই এটাকে extreme-level উত্তর বানায়।""",
        mist_en=r"""One giant `Order` document that every seller edits; stock checked with `findOne` then decremented with `save()`; calling the payment gateway inside the transaction; populating everything for admin reports.""",
        mist_bn=r"""এমন একটা বিশাল `Order` document, যেটা সব seller edit করে; `findOne` দিয়ে stock check করে `save()` দিয়ে কমানো; transaction-এর ভেতরে payment gateway call করা; admin report-এর জন্য সবকিছু populate করা।""",
        code=r"""
            import mongoose, { Schema, model } from "mongoose";

            const itemSnapshot = new Schema({
              productId: { type: Schema.Types.ObjectId, ref: "Product", required: true },
              sku: { type: String, required: true },
              name: String,
              unitPrice: { type: Number, required: true },   // poisha, frozen at checkout
              qty: { type: Number, required: true, min: 1 },
            }, { _id: false });

            const Inventory = model("Inventory", new Schema({
              sku: { type: String, required: true, unique: true },
              available: { type: Number, required: true, min: 0 },
              reserved: { type: Number, default: 0 },
            }));

            const orderSchema = new Schema({
              checkoutId: { type: String, required: true, unique: true },   // idempotency key
              customerId: { type: Schema.Types.ObjectId, ref: "User", required: true },
              shipping: { name: String, phone: String, city: String, area: String },
              totals: { subtotal: Number, delivery: Number, discount: Number, grandTotal: Number },
              paymentStatus: { type: String, enum: ["pending", "paid", "failed", "refunded"], default: "pending" },
            }, { timestamps: true, optimisticConcurrency: true });
            orderSchema.index({ customerId: 1, createdAt: -1 });
            const Order = model("Order", orderSchema);

            const sellerOrderSchema = new Schema({
              orderId: { type: Schema.Types.ObjectId, ref: "Order", required: true },
              sellerId: { type: Schema.Types.ObjectId, ref: "Seller", required: true },
              items: [itemSnapshot],
              status: { type: String, enum: ["pending", "packed", "shipped", "delivered", "cancelled"], default: "pending" },
            }, { timestamps: true });
            sellerOrderSchema.index({ sellerId: 1, status: 1, createdAt: -1 });
            const SellerOrder = model("SellerOrder", sellerOrderSchema);

            const paymentOpts = { timestamps: true, discriminatorKey: "method" };
            const paymentSchema = new Schema({
              orderId: { type: Schema.Types.ObjectId, ref: "Order", required: true },
              amount: { type: Number, required: true },
              status: { type: String, enum: ["pending", "paid", "failed"], default: "pending" },
              gatewayTrxId: String,
            }, paymentOpts);
            paymentSchema.index(
              { gatewayTrxId: 1 },
              { unique: true, partialFilterExpression: { gatewayTrxId: { $type: "string" } } }
            );
            const Payment = model("Payment", paymentSchema);
            Payment.discriminator("bkash", new Schema({ payerMsisdn: String }, paymentOpts));
            Payment.discriminator("card", new Schema({ cardBrand: String, last4: String }, paymentOpts));
            Payment.discriminator("cod", new Schema({ collectedBy: String }, paymentOpts));

            // Inside the checkout transaction, per SKU (sequentially, with the session):
            async function reserve(item, session) {
              const res = await Inventory.updateOne(
                { sku: item.sku, available: { $gte: item.qty } },
                { $inc: { available: -item.qty, reserved: item.qty } },
                { session }
              );
              if (res.matchedCount === 0) throw new OutOfStockError(item.sku);
            }
        """,
        lang="javascript",
        follow=[
            ("A seller cancels one item from a three-seller order. Walk me through the data changes.", "তিন seller-এর একটা order থেকে একজন seller একটা item cancel করল। Data-তে কী কী পরিবর্তন হবে, ধাপে ধাপে বলো।"),
            ("How would you make the bKash webhook handler idempotent and safe against forged callbacks?", "bKash webhook handler-কে কীভাবে idempotent আর জাল callback থেকে নিরাপদ করবে?"),
            ("Where would you draw the line between Mongoose models and raw driver/aggregation code here?", "এখানে Mongoose model আর raw driver/aggregation code-এর মধ্যে সীমারেখা কোথায় টানবে?"),
        ],
        related=["mongoose-023", "mongoose-002"],
        refs=[DISCRIMINATORS, TRANSACTIONS, GUIDE],
    ),
]

if __name__ == "__main__":
    save("mongoose", "b1", QUESTIONS)
