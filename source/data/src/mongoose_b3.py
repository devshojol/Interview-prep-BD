# Mongoose — batch 3 (mongoose-008, 009, 016, 017, 018, 026, 027, 032)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

GUIDE = ("Mongoose — Schemas guide", "https://mongoosejs.com/docs/guide.html")
QUERIES = ("Mongoose — Queries", "https://mongoosejs.com/docs/queries.html")
VALIDATION = ("Mongoose — Validation", "https://mongoosejs.com/docs/validation.html")
SCHEMATYPES = ("Mongoose — SchemaTypes", "https://mongoosejs.com/docs/schematypes.html")
LEAN = ("Mongoose — Faster Mongoose Queries With Lean", "https://mongoosejs.com/docs/tutorials/lean.html")
EXPRESS_ERRORS = ("Express — Error handling", "https://expressjs.com/en/guide/error-handling.html")
MONGOOSE_API = ("Mongoose API — Mongoose (set options)", "https://mongoosejs.com/docs/api/mongoose.html")
MIGRATE7 = ("Mongoose — Migrating to 7 (strictQuery default)", "https://mongoosejs.com/docs/migrating_to_7.html")
QUERY_CASTING = ("Mongoose — Query Casting", "https://mongoosejs.com/docs/tutorials/query_casting.html")
OWASP_NOSQL = ("OWASP — NoSQL Security Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/NoSQL_Security_Cheat_Sheet.html")
MIDDLEWARE = ("Mongoose — Middleware", "https://mongoosejs.com/docs/middleware.html")
PLUGINS = ("Mongoose — Plugins", "https://mongoosejs.com/docs/plugins.html")
MODEL_API = ("Mongoose API — Model (createIndexes, diffIndexes, syncIndexes)", "https://mongoosejs.com/docs/api/model.html")
RN_90 = ("MongoDB 9.0 Release Notes (known issues)", "https://www.mongodb.com/docs/manual/release-notes/9.0/")
INDEX_BUILDS = ("MongoDB Manual — Index Builds on Populated Collections", "https://www.mongodb.com/docs/manual/core/index-creation/")

QUESTIONS = [
    # ------------------------------------------------------------------ mongoose-008
    Q(
        id="mongoose-008", sub="Instance & Static Methods", diff="easy", type="conceptual",
        prio="medium", market="both", mins=3,
        tags=["methods", "statics", "query-helpers", "schema"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""What's the difference between instance methods, static methods and query helpers in Mongoose? When would you use each?""",
        q_bn=r"""Mongoose-এ instance method, static method আর query helper-এর মধ্যে পার্থক্য কী? কোনটা কখন ব্যবহার করবে?""",
        a_en=r"""
            - **Instance methods** (`schema.methods`) are available on **documents**; `this` is the document. Use them for behaviour of one record: `user.comparePassword(plain)`, `order.canBeCancelled()`.
            - **Static methods** (`schema.statics`) are available on the **model**; `this` is the model. Use them for reusable queries or domain operations that aren't about one loaded document: `User.findByEmail(email)`, `Order.markExpiredAsCancelled()`.
            - **Query helpers** (`schema.query`) are chainable methods on **queries**; `this` is the query. Use them for reusable filters: `Product.find().inStock().sort({ price: 1 })`.

            In all three, use regular `function`s, not arrow functions, so `this` is bound correctly.
        """,
        a_bn=r"""
            - **Instance method** (`schema.methods`) **document**-এ পাওয়া যায়; `this` হলো document। একটা record-এর আচরণের জন্য ব্যবহার করো: `user.comparePassword(plain)`, `order.canBeCancelled()`।
            - **Static method** (`schema.statics`) **model**-এ পাওয়া যায়; `this` হলো model। Reusable query বা এমন domain operation-এর জন্য, যেটা একটা load করা document নিয়ে না: `User.findByEmail(email)`, `Order.markExpiredAsCancelled()`।
            - **Query helper** (`schema.query`) হলো **query**-র ওপর chain করা যায় এমন method; `this` হলো query। Reusable filter-এর জন্য: `Product.find().inStock().sort({ price: 1 })`।

            তিনটাতেই arrow function না, সাধারণ `function` ব্যবহার করো, যাতে `this` ঠিকভাবে bind হয়।
        """,
        ex_en=r"""
            - **Where logic belongs:** methods keep data rules close to the data (e.g. normalising an email in one place), but don't move everything into models — HTTP concerns, emails and payment calls belong in services.
            - **Alternative syntax:** you can pass `methods`, `statics` and `query` in the schema options object, or use `schema.loadClass(SomeClass)` with ES6 classes. The options style gives better TypeScript inference.
            - **Query helpers compose:** because they return the query, you can chain them with `.lean()`, `.select()` and pagination.
            - **Static vs plain function:** a static is just a function attached to the model; its value is discoverability (`User.` autocompletes it) and access to `this` (the model) for inheritance with discriminators.
        """,
        ex_bn=r"""
            - **Logic কোথায় থাকবে:** method data-র নিয়ম data-র কাছাকাছি রাখে (যেমন email normalise করা এক জায়গায়), কিন্তু সবকিছু model-এ ঢুকিয়ে দিও না — HTTP-সংক্রান্ত কাজ, email আর payment call service-এ থাকবে।
            - **বিকল্প syntax:** schema-র options object-এ `methods`, `statics` আর `query` দেওয়া যায়, অথবা ES6 class সহ `schema.loadClass(SomeClass)` ব্যবহার করা যায়। Options style-এ TypeScript inference ভালো হয়।
            - **Query helper মিলিয়ে ব্যবহার করা যায়:** এগুলো query return করে বলে `.lean()`, `.select()` আর pagination-এর সাথে chain করা যায়।
            - **Static বনাম সাধারণ function:** static হলো model-এর সাথে জুড়ে দেওয়া একটা function; এর সুবিধা হলো সহজে খুঁজে পাওয়া (`User.` লিখলে autocomplete হয়) আর `this` (model) access, যা discriminator-এর inheritance-এ কাজে লাগে।
        """,
        tip_en=r"""Give one realistic example of each and say what `this` is in each case — that's the whole answer in a form interviewers can check quickly.""",
        tip_bn=r"""প্রতিটির একটা বাস্তব উদাহরণ দাও আর প্রতিটিতে `this` কী সেটা বলো — interviewer দ্রুত যাচাই করতে পারে এমনভাবে পুরো উত্তরটাই এতে চলে আসে।""",
        mist_en=r"""Using arrow functions (then `this` is undefined); putting a static on `schema.methods` and wondering why `User.findByEmail` is undefined.""",
        mist_bn=r"""Arrow function ব্যবহার করা (তখন `this` undefined); static-কে `schema.methods`-এ রেখে অবাক হওয়া যে `User.findByEmail` কেন undefined।""",
        code=r"""
            import bcrypt from "bcrypt";

            // Instance method: this = document
            userSchema.methods.comparePassword = function (plain) {
              return bcrypt.compare(plain, this.passwordHash);
            };

            // Static: this = model
            userSchema.statics.findByEmail = function (email) {
              return this.findOne({ email: email.trim().toLowerCase() });
            };

            // Query helper: this = query
            productSchema.query.inStock = function () {
              return this.where({ stock: { $gt: 0 } });
            };

            const user = await User.findByEmail("Rafi@Example.com").select("+passwordHash");
            const ok = user && (await user.comparePassword("secret123"));
            const items = await Product.find({ category: "electronics" }).inStock().lean();
        """,
        lang="javascript",
        follow=[
            ("How would you type instance methods and statics in TypeScript?", "TypeScript-এ instance method আর static-এর type কীভাবে দেবে?"),
        ],
        related=["mongoose-001"],
        refs=[GUIDE, QUERIES],
    ),
    # ------------------------------------------------------------------ mongoose-009
    Q(
        id="mongoose-009", sub="Validation", diff="easy", type="conceptual",
        prio="high", market="bangladesh", mins=3,
        tags=["validation", "validators", "custom-validator", "async-validator"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""How does validation work in Mongoose? Explain built-in validators, custom validators, and when validation runs.""",
        q_bn=r"""Mongoose-এ validation কীভাবে কাজ করে? Built-in validator, custom validator, আর validation কখন চলে — ব্যাখ্যা করো।""",
        a_en=r"""
            Validation rules live on the schema paths and run in the app before data is written.

            - **Built-in validators:** `required` for any type; `min`/`max` for numbers and dates; `enum`, `match`, `minLength`, `maxLength` for strings. Each accepts a custom message, e.g. `required: [true, "Phone is required"]`.
            - **Custom validators:** `validate: { validator: fn, message }`. The function returns `true`/`false`; an **async** validator returns a promise, and a rejection or `false` means invalid.
            - **When it runs:** automatically on `save()` and `create()` (validation is a pre-save step), or manually with `doc.validate()`. It does **not** run on `updateOne`/`findOneAndUpdate` unless you pass `runValidators: true`.

            On failure Mongoose throws a `ValidationError` whose `errors` object has one entry per invalid path.
        """,
        a_bn=r"""
            Validation-এর নিয়ম schema-র path-এ থাকে, আর data লেখার আগে app-এর ভেতরেই চলে।

            - **Built-in validator:** যেকোনো type-এ `required`; number আর date-এ `min`/`max`; string-এ `enum`, `match`, `minLength`, `maxLength`। প্রতিটিতে custom message দেওয়া যায়, যেমন `required: [true, "Phone is required"]`।
            - **Custom validator:** `validate: { validator: fn, message }`। Function `true`/`false` return করে; **async** validator একটা promise return করে, আর reject হলে বা `false` দিলে invalid ধরা হয়।
            - **কখন চলে:** `save()` আর `create()`-এ automatically (validation হলো একটা pre-save ধাপ), অথবা `doc.validate()` দিয়ে manually। `runValidators: true` না দিলে `updateOne`/`findOneAndUpdate`-এ **চলে না**।

            Fail করলে Mongoose একটা `ValidationError` throw করে, যার `errors` object-এ প্রতিটি invalid path-এর জন্য একটা করে entry থাকে।
        """,
        ex_en=r"""
            - **Casting comes first:** if a value can't be cast (e.g. `"abc"` for a Number), you get a `CastError` inside `err.errors` and the other validators for that path don't run.
            - **Not validators:** `unique` (an index) and setters like `trim`/`lowercase` (transformations).
            - **Async validators** (e.g. "the referenced category exists") add a database query per save — fine for admin forms, costly in bulk imports.
            - **Message templates:** `{VALUE}` and `{PATH}` in messages are replaced with the actual value and path name.
            - **API boundary:** many teams validate request bodies with zod at the edge *and* keep Mongoose validation as the last line of defence for data integrity.
        """,
        ex_bn=r"""
            - **আগে casting:** value cast করা না গেলে (যেমন Number-এ `"abc"`) `err.errors`-এর ভেতরে একটা `CastError` আসে, আর ওই path-এর অন্য validator চলে না।
            - **Validator না:** `unique` (একটা index) আর `trim`/`lowercase`-এর মতো setter (রূপান্তর)।
            - **Async validator** (যেমন "referenced category আছে কি না") প্রতিটি save-এ একটা database query যোগ করে — admin form-এ ঠিক আছে, bulk import-এ ব্যয়বহুল।
            - **Message template:** message-এ `{VALUE}` আর `{PATH}` আসল value আর path name দিয়ে replace হয়।
            - **API boundary:** অনেক team request body-কে edge-এ zod দিয়ে validate করে, *আর* data integrity-র শেষ প্রতিরক্ষা হিসেবে Mongoose validation-ও রাখে।
        """,
        tip_en=r"""Mention the "doesn't run on updates by default" rule even though it wasn't asked — it's the most common real-world validation bug and shows experience.""",
        tip_bn=r"""জিজ্ঞেস না করলেও "default-ভাবে update-এ চলে না" নিয়মটা উল্লেখ করো — বাস্তবে validation-এর সবচেয়ে common bug এটাই, আর এতে অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Assuming validation runs on every write; treating `unique` as a validator; writing validators as arrow functions that need `this`.""",
        mist_bn=r"""ধরে নেওয়া প্রতিটি write-এ validation চলে; `unique`-কে validator মনে করা; `this` লাগে এমন validator arrow function দিয়ে লেখা।""",
        code=r"""
            const customerSchema = new Schema({
              name: { type: String, required: [true, "Name is required"], minLength: 2, maxLength: 80 },
              phone: {
                type: String,
                required: true,
                validate: {
                  validator: (v) => /^(?:\+?88)?01[3-9]\d{8}$/.test(v),   // Bangladeshi mobile
                  message: "{VALUE} is not a valid Bangladeshi mobile number",
                },
              },
              age: { type: Number, min: [18, "Must be at least 18"] },
              category: {
                type: Schema.Types.ObjectId,
                ref: "Category",
                validate: {
                  // async validator: resolve false (or reject) = invalid
                  validator: async (id) => !!(await Category.exists({ _id: id })),
                  message: "Category does not exist",
                },
              },
            });

            try {
              await Customer.create({ name: "R", phone: "12345", age: 16 });
            } catch (err) {
              console.log(Object.keys(err.errors));   // [ 'name', 'phone', 'age' ]
            }
        """,
        lang="javascript",
        follow=[
            ("How would you validate that `endDate` is after `startDate`?", "`endDate` যে `startDate`-এর পরে, সেটা কীভাবে validate করবে?"),
            ("Why might you validate with zod and also keep Mongoose validators?", "zod দিয়ে validate করার পরেও কেন Mongoose validator রাখবে?"),
        ],
        related=["mongoose-003", "mongoose-012"],
        refs=[VALIDATION, SCHEMATYPES],
    ),
    # ------------------------------------------------------------------ mongoose-016
    Q(
        id="mongoose-016", sub="Lean Queries", diff="medium", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["lean", "performance", "hydration", "pojo", "nextjs"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""What does `.lean()` do in Mongoose, why is it faster, and what do you lose by using it?""",
        q_bn=r"""Mongoose-এ `.lean()` কী করে, এটা কেন দ্রুত, আর ব্যবহার করলে কী কী হারাও?""",
        a_en=r"""
            Normally Mongoose **hydrates** every result: it wraps the raw object from the driver in a full Mongoose document with change tracking, getters/setters, virtuals and methods. `.lean()` skips that step and returns **plain JavaScript objects**.

            That's faster and uses much less memory, which matters for list endpoints returning hundreds of rows.

            What you lose on lean results:
            - `save()`, change tracking and `isModified()`
            - instance methods
            - virtuals and getters (and schema `toJSON` transforms)
            - defaults for fields missing in the stored document

            I use `.lean()` for **read-only** paths — API lists, reports, server-side rendering — and keep normal documents when I'm going to modify and `save()`, or need virtuals/methods.
        """,
        a_bn=r"""
            সাধারণভাবে Mongoose প্রতিটি result **hydrate** করে: driver থেকে আসা raw object-কে change tracking, getter/setter, virtual আর method সহ পূর্ণ Mongoose document-এ মুড়ে দেয়। `.lean()` এই ধাপটা বাদ দিয়ে **plain JavaScript object** return করে।

            এটা দ্রুত আর অনেক কম memory ব্যবহার করে — শত শত row return করা list endpoint-এ এটা গুরুত্বপূর্ণ।

            Lean result-এ যা হারাও:
            - `save()`, change tracking আর `isModified()`
            - instance method
            - virtual আর getter (আর schema-র `toJSON` transform)
            - stored document-এ না থাকা field-এর default

            আমি **read-only** পথে `.lean()` ব্যবহার করি — API list, report, server-side rendering — আর modify করে `save()` করব বা virtual/method লাগবে এমন জায়গায় সাধারণ document রাখি।
        """,
        ex_en=r"""
            - **What still works:** the query filter is still cast by the schema (lean only affects the *result*), and `populate()` still works.
            - **Types are BSON types:** `_id` is still an `ObjectId` instance and dates are `Date` objects. When passing lean results from a Next.js Server Component to a Client Component, convert `_id` to a string — class instances like `ObjectId` aren't allowed across that boundary.
            - **Virtuals on lean results:** compute them yourself or use a plugin (e.g. `mongoose-lean-virtuals`).
            - **Hidden fields still hidden:** `select: false` applies to lean queries too.
            - **Rule of thumb:** if the handler ends with `res.json(result)` and never calls `save()`, it's a good candidate for `.lean()`.
        """,
        ex_bn=r"""
            - **যা এখনো কাজ করে:** query filter তখনও schema অনুযায়ী cast হয় (lean শুধু *result*-কে প্রভাবিত করে), আর `populate()`-ও কাজ করে।
            - **Type-গুলো BSON type:** `_id` তখনও `ObjectId` instance, আর date হলো `Date` object। Next.js Server Component থেকে Client Component-এ lean result পাঠালে `_id`-কে string-এ রূপান্তর করো — `ObjectId`-এর মতো class instance ওই boundary পার হতে পারে না।
            - **Lean result-এ virtual:** নিজে হিসাব করো, অথবা plugin ব্যবহার করো (যেমন `mongoose-lean-virtuals`)।
            - **লুকানো field লুকানোই থাকে:** `select: false` lean query-তেও apply হয়।
            - **মূল নিয়ম:** handler যদি `res.json(result)` দিয়ে শেষ হয় আর কখনো `save()` call না করে, তাহলে সেটা `.lean()`-এর ভালো প্রার্থী।
        """,
        tip_en=r"""Frame lean as "skip hydration" and list what hydration gives you — then the trade-off explains itself. Mentioning the Next.js serialisation gotcha shows real-world use.""",
        tip_bn=r"""Lean-কে "hydration বাদ দেওয়া" হিসেবে ব্যাখ্যা করো আর hydration কী কী দেয় তার তালিকা বলো — তাহলে trade-off নিজেই বোঝা যায়। Next.js-এর serialisation gotcha উল্লেখ করলে বাস্তব ব্যবহারের অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Calling `.save()` on a lean result; expecting virtuals in lean output; assuming lean turns `ObjectId`s into strings.""",
        mist_bn=r"""Lean result-এ `.save()` call করা; lean output-এ virtual আশা করা; ধরে নেওয়া যে lean `ObjectId`-কে string বানিয়ে দেয়।""",
        code=r"""
            // Hydrated documents: needed when you modify and save
            const order = await Order.findById(id);
            order.status = "shipped";
            await order.save();

            // Lean: read-only list for an API response
            const recent = await Order.find({ customerId })
              .select("status totals.grandTotal createdAt")
              .sort({ createdAt: -1 })
              .limit(20)
              .lean();

            recent[0] instanceof mongoose.Document;   // false — plain object
            typeof recent[0].save;                    // "undefined"
            recent[0]._id instanceof mongoose.Types.ObjectId;   // true
        """,
        lang="javascript",
        follow=[
            ("How would you safely pass lean documents to a Next.js Client Component?", "Lean document নিরাপদে Next.js Client Component-এ কীভাবে পাঠাবে?"),
            ("Would you use `.lean()` in a query that is later passed to `save()`? Why not?", "যে query-র result পরে `save()`-এ যাবে, সেখানে কি `.lean()` ব্যবহার করবে? কেন না?"),
        ],
        related=["mongoose-007", "mongoose-024"],
        refs=[LEAN, QUERIES],
    ),
    # ------------------------------------------------------------------ mongoose-017
    Q(
        id="mongoose-017", sub="Error Handling", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["error-handling", "validationerror", "casterror", "e11000", "express-5"],
        ver="Mongoose 9.11, Express 5.x", vs=False, status="stable",
        q_en=r"""Write Express 5 error-handling middleware that turns Mongoose/MongoDB errors into clean API responses:

- `ValidationError` → 400 with a message per field
- `CastError` (e.g. an invalid ObjectId) → 400
- duplicate key (E11000) → 409 naming the field
- `DocumentNotFoundError` (from `.orFail()`) → 404
- anything else → 500 without leaking internals

Example: creating a user with an existing email returns `409 { "error": "email already exists" }`.""",
        q_bn=r"""এমন একটা Express 5 error-handling middleware লেখো, যেটা Mongoose/MongoDB error-কে পরিষ্কার API response-এ রূপান্তর করবে:

- `ValidationError` → 400, প্রতিটি field-এর message সহ
- `CastError` (যেমন invalid ObjectId) → 400
- duplicate key (E11000) → 409, field-এর নাম সহ
- `DocumentNotFoundError` (`.orFail()` থেকে) → 404
- বাকি সব → 500, ভেতরের কোনো তথ্য ফাঁস না করে

উদাহরণ: আগে থেকে থাকা email দিয়ে user তৈরি করলে `409 { "error": "email already exists" }` return হবে।""",
        code=r"""
            import mongoose from "mongoose";

            export function mongooseErrorHandler(err, req, res, next) {
              if (res.headersSent) return next(err);

              if (err instanceof mongoose.Error.ValidationError) {
                const fields = Object.fromEntries(
                  Object.entries(err.errors).map(([path, e]) => [path, e.message])
                );
                return res.status(400).json({ error: "Validation failed", fields });
              }

              if (err instanceof mongoose.Error.CastError) {
                return res.status(400).json({ error: `Invalid value for '${err.path}'` });
              }

              if (err instanceof mongoose.Error.DocumentNotFoundError) {
                return res.status(404).json({ error: "Not found" });
              }

              // Duplicate key comes from the MongoDB driver (MongoServerError), not Mongoose
              if (err?.code === 11000) {
                const field = Object.keys(err.keyValue ?? err.keyPattern ?? {})[0] ?? "value";
                return res.status(409).json({ error: `${field} already exists` });
              }

              console.error(err);          // use your logger (pino, winston) in real apps
              return res.status(500).json({ error: "Internal server error" });
            }

            // Register after all routes. In Express 5, errors thrown in async handlers
            // are forwarded here automatically — no try/catch needed in routes.
            app.post("/users", async (req, res) => {
              const user = await User.create(pickSignupFields(req.body));
              res.status(201).json(user);
            });
            app.use(mongooseErrorHandler);
        """,
        lang="javascript",
        time="O(k) where k = number of invalid fields",
        space="O(k)",
        a_en=r"""
            The middleware checks error types from most to least specific:

            - `mongoose.Error.ValidationError`: `err.errors` maps each path to a `ValidatorError` (or a `CastError` if casting failed during validation), so I turn it into `{ field: message }`.
            - `mongoose.Error.CastError`: thrown when a **query** value can't be cast, e.g. `findById("abc")`. I report the path but don't echo internal details.
            - `DocumentNotFoundError` → 404, so routes can use `.orFail()` instead of manual `null` checks.
            - **E11000** isn't a Mongoose error class — it's a `MongoServerError` from the driver with `code: 11000` and `keyValue` (e.g. `{ email: "a@x.com" }`), so I check `err.code`.
            - Everything else is logged server-side and returned as a generic 500.

            It has four parameters, which is how Express recognises error middleware, and it's registered after the routes.
        """,
        a_bn=r"""
            Middleware-টা error type-গুলো সবচেয়ে নির্দিষ্ট থেকে কম নির্দিষ্ট ক্রমে check করে:

            - `mongoose.Error.ValidationError`: `err.errors` প্রতিটি path-কে একটা `ValidatorError`-এর সাথে map করে (validation-এর সময় casting fail করলে `CastError`), তাই আমি এটাকে `{ field: message }`-এ রূপান্তর করি।
            - `mongoose.Error.CastError`: কোনো **query** value cast করা না গেলে throw হয়, যেমন `findById("abc")`। আমি path জানাই, কিন্তু ভেতরের বিস্তারিত echo করি না।
            - `DocumentNotFoundError` → 404, যাতে route-গুলো হাতে `null` check না করে `.orFail()` ব্যবহার করতে পারে।
            - **E11000** কোনো Mongoose error class না — এটা driver-এর `MongoServerError`, যেখানে `code: 11000` আর `keyValue` (যেমন `{ email: "a@x.com" }`) থাকে, তাই আমি `err.code` check করি।
            - বাকি সব server-side-এ log হয় আর generic 500 হিসেবে return হয়।

            এতে চারটা parameter আছে — Express এভাবেই error middleware চিনতে পারে — আর এটা route-গুলোর পরে register করা হয়।
        """,
        ex_en=r"""
            - **Edge cases:** an error after headers were sent (streaming) must be delegated with `next(err)`; bulk inserts with duplicates throw a `MongoBulkWriteError` with per-document `writeErrors`; a `ValidationError` can contain several fields at once — return them all so the form can show every problem.
            - **Don't leak:** echoing `err.message` for unknown errors can reveal collection names, query shapes or stack traces.
            - **Consistency:** use one error shape for the whole API (e.g. `{ error, fields? }`), and consider mapping zod errors in the same middleware.
            - **Duplicate key in practice:** keep values normalised (`lowercase`, `trim`) so "Rafi@x.com" and "rafi@x.com" are caught as duplicates.
            - **Express 4 (legacy):** async errors were not forwarded automatically, so routes needed `try/catch` + `next(err)` or a wrapper; Express 5 handles rejected promises for you.
        """,
        ex_bn=r"""
            - **Edge case:** header পাঠানোর পরে error হলে (streaming) `next(err)` দিয়ে পাঠিয়ে দিতে হয়; duplicate সহ bulk insert একটা `MongoBulkWriteError` throw করে, যেখানে প্রতিটি document-এর `writeErrors` থাকে; একটা `ValidationError`-এ একসাথে কয়েকটা field থাকতে পারে — সবগুলোই return করো, যাতে form প্রতিটি সমস্যা দেখাতে পারে।
            - **তথ্য ফাঁস কোরো না:** অজানা error-এর `err.message` echo করলে collection-এর নাম, query-র shape বা stack trace বেরিয়ে যেতে পারে।
            - **Consistency:** পুরো API-তে একটাই error shape রাখো (যেমন `{ error, fields? }`), আর একই middleware-এ zod error map করার কথা ভাবো।
            - **বাস্তবে duplicate key:** value normalise করে রাখো (`lowercase`, `trim`), যাতে "Rafi@x.com" আর "rafi@x.com" duplicate হিসেবে ধরা পড়ে।
            - **Express 4 (legacy):** async error automatically forward হতো না, তাই route-এ `try/catch` + `next(err)` বা wrapper লাগত; Express 5 rejected promise নিজেই সামলায়।
        """,
        tip_en=r"""Point out that E11000 comes from the driver, not Mongoose — it's a detail that shows you've actually debugged these errors rather than guessed at them.""",
        tip_bn=r"""উল্লেখ করো যে E11000 আসে driver থেকে, Mongoose থেকে না — এই detail-টাই দেখায় যে তুমি আসলে এই error-গুলো debug করেছ, আন্দাজে বলছ না।""",
        mist_en=r"""Checking `err.name === "MongoError"` (old class name); returning `err.message` to clients; defining the handler with three parameters so Express treats it as normal middleware.""",
        mist_bn=r"""`err.name === "MongoError"` check করা (পুরনো class name); client-কে `err.message` return করা; তিনটা parameter দিয়ে handler define করা, ফলে Express এটাকে সাধারণ middleware মনে করে।""",
        follow=[
            ("How would you return field-level errors for an `insertMany` import?", "`insertMany` import-এর জন্য field-level error কীভাবে return করবে?"),
            ("Where would you log the request ID so errors can be traced across services?", "Service জুড়ে error trace করতে request ID কোথায় log করবে?"),
        ],
        related=["mongoose-003", "mongoose-005", "mongoose-012"],
        refs=[VALIDATION, EXPRESS_ERRORS, MONGOOSE_API],
    ),
    # ------------------------------------------------------------------ mongoose-018
    Q(
        id="mongoose-018", sub="Common Pitfalls", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["strictquery", "filters", "typos", "pitfalls"],
        ver="Mongoose 9.11 (`strictQuery` default false since Mongoose 7)", vs=True, status="stable",
        q_en=r"""With Mongoose 9 default settings, a developer runs `await User.deleteMany({ emial: "spam@example.com" })` — note the typo: `emial` is not a path in the schema. What happens?""",
        q_bn=r"""Mongoose 9-এর default setting-এ একজন developer চালাল `await User.deleteMany({ emial: "spam@example.com" })` — খেয়াল করো typo: `emial` schema-র কোনো path না। কী হবে?""",
        options=[
            (r"""Mongoose maps the typo to the closest schema path, `email`, and deletes that user""",
             r"""Mongoose typo-টাকে সবচেয়ে কাছের schema path `email`-এ map করে সেই user delete করে"""),
            (r"""Every user is deleted, because Mongoose strips unknown filter fields and the filter becomes `{}`""",
             r"""সব user delete হয়ে যায়, কারণ Mongoose অজানা filter field বাদ দেয় আর filter হয়ে যায় `{}`"""),
            (r"""Mongoose throws a `StrictModeError` because `emial` isn't in the schema""",
             r"""`emial` schema-তে না থাকায় Mongoose একটা `StrictModeError` throw করে"""),
            (r"""Nothing is deleted: with the default `strictQuery: false` the unknown field is sent to MongoDB as-is, and no document has an `emial` field""",
             r"""কিছুই delete হয় না: default `strictQuery: false`-এ অজানা field যেমন আছে তেমনই MongoDB-তে যায়, আর কোনো document-এ `emial` field নেই"""),
        ],
        correct=3,
        a_en=r"""Since Mongoose 7, `strictQuery` defaults to `false`, so filter properties that aren't in the schema are **kept** and passed to MongoDB. `{ emial: "spam@example.com" }` matches no documents, so `deletedCount` is 0.""",
        a_bn=r"""Mongoose 7 থেকে `strictQuery`-এর default `false`, তাই schema-তে না থাকা filter property **রেখে দেওয়া হয়** আর MongoDB-তে পাঠানো হয়। `{ emial: "spam@example.com" }` কোনো document match করে না, তাই `deletedCount` 0।""",
        ex_en=r"""
            Option B is exactly what happens with `strictQuery: true` (the Mongoose 6 default): unknown paths are stripped, the filter becomes `{}`, and `deleteMany({})` wipes the collection. That danger is one reason the default changed. Option C happens if you set `strictQuery: "throw"` — a good choice in development and tests to catch typos early.

            The flip side of `false`: filter keys coming from user input aren't restricted to schema paths, so always validate request data before using it in a filter. Don't count on TypeScript here: Mongoose 9's stricter `QueryFilter` type checks value types for known paths, but an unknown key like `emial` still compiles — `strictQuery: "throw"` in tests is the reliable safety net.
        """,
        ex_bn=r"""
            Option B ঠিক সেটাই, যা `strictQuery: true` (Mongoose 6-এর default) থাকলে হয়: অজানা path বাদ পড়ে, filter হয়ে যায় `{}`, আর `deleteMany({})` পুরো collection মুছে দেয়। এই বিপদই default বদলানোর একটা কারণ। `strictQuery: "throw"` set করলে option C হয় — development আর test-এ আগেভাগে typo ধরার জন্য এটা ভালো পছন্দ।

            `false`-এর উল্টো দিক: user input থেকে আসা filter key schema path-এ সীমাবদ্ধ থাকে না, তাই filter-এ ব্যবহারের আগে সবসময় request data validate করো। এখানে TypeScript-এর ওপর ভরসা কোরো না: Mongoose 9-এর আরও কঠোর `QueryFilter` type জানা path-এর value type check করে, কিন্তু `emial`-এর মতো অজানা key তবুও compile হয়ে যায় — test-এ `strictQuery: "throw"`-ই নির্ভরযোগ্য safety net।
        """,
        tip_en=r"""Explain all three settings (`false`, `true`, `"throw"`) and which one you'd use where — knowing *why* the default changed is the impressive part.""",
        tip_bn=r"""তিনটা setting-ই (`false`, `true`, `"throw"`) ব্যাখ্যা করো আর কোনটা কোথায় ব্যবহার করবে বলো — default *কেন* বদলেছে সেটা জানাটাই impressive অংশ।""",
        follow=[
            ("Why is `strictQuery: \"throw\"` useful in tests but risky as a production default for some teams?", "Test-এ `strictQuery: \"throw\"` কেন কাজের, কিন্তু কিছু team-এর জন্য production default হিসেবে কেন ঝুঁকিপূর্ণ?"),
        ],
        related=["mongoose-012"],
        refs=[MIGRATE7, MONGOOSE_API, QUERY_CASTING],
    ),
    # ------------------------------------------------------------------ mongoose-026
    Q(
        id="mongoose-026", sub="Security", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["security", "nosql-injection", "sanitizefilter", "mass-assignment", "redos", "select-false"],
        ver="Mongoose 9.11, Express 5, zod 4", vs=False, status="stable",
        q_en=r"""
            Review these four lines from an Express + Mongoose API for security problems:

            1. Login: `User.findOne({ email: req.body.email, password: req.body.password })`
            2. Signup: `User.create(req.body)`
            3. Search: `Product.find({ name: { $regex: req.query.q, $options: "i" } })`
            4. Profile: `res.json(await User.findById(req.userId))`

            How would you fix each one, and which Mongoose features help?
        """,
        q_bn=r"""
            একটা Express + Mongoose API-র এই চারটা line security-র দৃষ্টিতে review করো:

            1. Login: `User.findOne({ email: req.body.email, password: req.body.password })`
            2. Signup: `User.create(req.body)`
            3. Search: `Product.find({ name: { $regex: req.query.q, $options: "i" } })`
            4. Profile: `res.json(await User.findById(req.userId))`

            প্রতিটি কীভাবে ঠিক করবে, আর কোন Mongoose feature সাহায্য করে?
        """,
        code=r"""
            // 1) Login
            const user = await User.findOne({ email: req.body.email, password: req.body.password });

            // 2) Signup
            const created = await User.create(req.body);

            // 3) Product search
            const products = await Product.find({ name: { $regex: req.query.q, $options: "i" } });

            // 4) Profile
            res.json(await User.findById(req.userId));
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                mongoose.set("sanitizeFilter", true);   // defence in depth against query selector injection

                // 1) Login: strings only, look up by email, compare the hash in the app
                const { email, password } = LoginBody.parse(req.body);          // zod schema
                const user = await User.findOne({ email }).select("+passwordHash");
                const ok = user && (await bcrypt.compare(password, user.passwordHash));

                // 2) Signup: whitelist fields; role/flags are never taken from the client
                const { name, email: newEmail, password: pw } = SignupBody.parse(req.body);
                const created = await User.create({ name, email: newEmail, passwordHash: await bcrypt.hash(pw, 12) });

                // 3) Search: validated, length-limited, escaped, bounded result; a case-sensitive
                //    prefix on a lowercase copy (nameLower) can use an index, unlike $options: "i"
                const { q } = SearchQuery.parse(req.query);                      // z.string().min(1).max(50)
                const safe = q.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
                const products = await Product.find({ nameLower: { $regex: `^${safe}` } })
                  .limit(20).lean();

                // 4) Profile: sensitive fields hidden by the schema
                res.json(await User.findById(req.userId));
            """),
            dict(lang="javascript", label_en="Schema-level protections", label_bn="Schema-level সুরক্ষা", src=r"""
                const userSchema = new Schema({
                  name: { type: String, required: true, trim: true },
                  email: { type: String, required: true, unique: true, lowercase: true, trim: true },
                  passwordHash: { type: String, required: true, select: false },
                  role: { type: String, enum: ["customer", "admin"], default: "customer" },
                  resetToken: { type: String, select: false },
                }, {
                  toJSON: {
                    transform(doc, ret) {
                      delete ret.passwordHash;
                      delete ret.resetToken;
                      delete ret.__v;
                      return ret;
                    },
                  },
                });
            """),
        ],
        a_en=r"""
            1. **Query selector injection + plain-text passwords.** Sending `{ "email": "admin@shop.com", "password": { "$ne": null } }` logs in as admin. Fix: validate that both values are strings (zod), query **only by email**, compare a bcrypt/argon2 hash in the app. Mongoose's **`sanitizeFilter`** option adds a second layer: it wraps nested objects that contain `$` keys in `$eq`, so `{ $ne: null }` becomes a literal value that matches nothing (use `mongoose.trusted()` for operators you add intentionally).
            2. **Mass assignment.** `User.create(req.body)` accepts any schema field, so a client can send `role: "admin"` or `isVerified: true`. `strict` mode only drops fields that aren't in the schema — `role` is. Fix: pick allowed fields explicitly; set privileged fields server-side.
            3. **Regex injection / ReDoS.** Raw user input becomes a regular expression: `.*` dumps everything, and patterns with catastrophic backtracking burn database CPU. A case-insensitive regex also can't use an index efficiently, even when anchored. Fix: validate type and length, escape special characters, limit results; for an index-backed prefix search, match a case-sensitive `^prefix` against a normalised lowercase field — or use a text index / Atlas Search.
            4. **Sensitive data exposure.** Returning the whole document leaks `passwordHash`, reset tokens and internal fields. Fix: `select: false` on sensitive paths plus a `toJSON` transform (or an explicit response DTO).
        """,
        a_bn=r"""
            1. **Query selector injection + plain-text password।** `{ "email": "admin@shop.com", "password": { "$ne": null } }` পাঠালেই admin হিসেবে login হয়ে যায়। Fix: দুইটা value-ই string কি না validate করো (zod), **শুধু email দিয়ে** query করো, app-এ bcrypt/argon2 hash compare করো। Mongoose-এর **`sanitizeFilter`** option আরেকটা স্তর যোগ করে: `$` key থাকা nested object-কে `$eq`-এ মুড়ে দেয়, ফলে `{ $ne: null }` একটা literal value হয়ে যায় যা কিছুই match করে না (ইচ্ছাকৃতভাবে যোগ করা operator-এর জন্য `mongoose.trusted()` ব্যবহার করো)।
            2. **Mass assignment।** `User.create(req.body)` যেকোনো schema field নেয়, তাই client `role: "admin"` বা `isVerified: true` পাঠাতে পারে। `strict` mode শুধু schema-তে না থাকা field বাদ দেয় — `role` তো schema-তেই আছে। Fix: অনুমোদিত field explicitly বেছে নাও; privileged field server-side-এ set করো।
            3. **Regex injection / ReDoS।** Raw user input regular expression হয়ে যায়: `.*` দিলে সব বেরিয়ে আসে, আর catastrophic backtracking-ওয়ালা pattern database-এর CPU পুড়িয়ে দেয়। Case-insensitive regex anchor করা থাকলেও দক্ষভাবে index ব্যবহার করতে পারে না। Fix: type আর length validate করো, special character escape করো, result সীমিত করো; index-backed prefix search চাইলে একটা normalised lowercase field-এর ওপর case-sensitive `^prefix` match করো — অথবা text index / Atlas Search ব্যবহার করো।
            4. **Sensitive data ফাঁস।** পুরো document return করলে `passwordHash`, reset token আর internal field বেরিয়ে যায়। Fix: sensitive path-এ `select: false` আর একটা `toJSON` transform (অথবা explicit response DTO)।
        """,
        ex_en=r"""
            - **`sanitizeFilter` is not a substitute for validation:** it protects filters, not updates, and it doesn't stop `$where`/`$function` code you build yourself. Validation at the edge remains the primary control.
            - **`strictQuery: false` (default since Mongoose 7)** means unknown filter keys pass through to MongoDB — another reason to validate the shape of any user-controlled filter (e.g. API "filter" query params).
            - **Express 5 helps a little:** its default `'simple'` query parser doesn't build nested objects from `?q[$ne]=x`, but JSON bodies can still contain objects.
            - **Performance angle:** bounded `limit`, `.lean()` and indexed, case-sensitive prefix queries also prevent a single request from exhausting database CPU — security and performance overlap here.
            - **Logging:** never log full request bodies on auth routes (passwords) and redact tokens.
        """,
        ex_bn=r"""
            - **`sanitizeFilter` validation-এর বিকল্প না:** এটা filter রক্ষা করে, update না, আর তুমি নিজে যে `$where`/`$function` code বানাও সেটাও আটকায় না। Edge-এ validation-ই মূল নিয়ন্ত্রণ।
            - **`strictQuery: false` (Mongoose 7 থেকে default)** মানে অজানা filter key MongoDB পর্যন্ত চলে যায় — user-controlled যেকোনো filter-এর (যেমন API-র "filter" query param) shape validate করার আরেকটা কারণ।
            - **Express 5 একটু সাহায্য করে:** এর default `'simple'` query parser `?q[$ne]=x` থেকে nested object বানায় না, কিন্তু JSON body-তে তবুও object থাকতে পারে।
            - **Performance-এর দিক:** সীমিত `limit`, `.lean()` আর indexed, case-sensitive prefix query একটা request-কে database-এর CPU শেষ করে ফেলা থেকেও আটকায় — এখানে security আর performance মিলে যায়।
            - **Logging:** auth route-এ কখনো পুরো request body log কোরো না (password থাকে), আর token redact করো।
        """,
        tip_en=r"""For each snippet, state the attack first (payload or scenario), then the fix, then the Mongoose feature that adds depth. Concrete payloads make the answer far more convincing than "sanitise inputs".""",
        tip_bn=r"""প্রতিটি snippet-এর জন্য আগে attack-টা বলো (payload বা scenario), তারপর fix, তারপর যে Mongoose feature বাড়তি সুরক্ষা দেয়। "Input sanitise করো" বলার চেয়ে concrete payload উত্তরকে অনেক বেশি বিশ্বাসযোগ্য করে।""",
        mist_en=r"""Believing Mongoose schemas make injection impossible; relying on `strict` mode to block privileged fields; escaping regex input but still allowing unlimited length and unbounded results.""",
        mist_bn=r"""Mongoose schema থাকলে injection অসম্ভব মনে করা; privileged field আটকাতে `strict` mode-এর ওপর ভরসা করা; regex input escape করলেও সীমাহীন length আর unbounded result রেখে দেওয়া।""",
        follow=[
            ("How would you let admins build flexible filters from the UI without opening an injection hole?", "Injection-এর ফাঁক না রেখে admin-দের UI থেকে flexible filter বানাতে দেবে কীভাবে?"),
            ("Where do `select: false` fields still leak (e.g. aggregation)?", "`select: false` field কোথায় এখনো ফাঁস হতে পারে (যেমন aggregation-এ)?"),
        ],
        related=["mongoose-018", "mongoose-024"],
        refs=[MONGOOSE_API, QUERY_CASTING, OWASP_NOSQL],
    ),
    # ------------------------------------------------------------------ mongoose-027
    Q(
        id="mongoose-027", sub="Middleware & Hooks", diff="hard", type="scenario",
        prio="medium", market="both", mins=10,
        tags=["soft-delete", "query-middleware", "plugins", "ttl", "partial-index", "aggregate-middleware"],
        ver="Mongoose 9.11 (sync/async hooks without next), MongoDB 9.0", vs=False, status="stable",
        q_en=r"""Product wants "soft delete" for users and posts: deleted items must disappear from every query in the app but stay in the database for 30 days for recovery and audits. How would you implement this with Mongoose, and what pitfalls would you watch for?""",
        q_bn=r"""Product team user আর post-এর জন্য "soft delete" চায়: delete করা item app-এর সব query থেকে অদৃশ্য হবে, কিন্তু recovery আর audit-এর জন্য 30 দিন database-এ থাকবে। Mongoose দিয়ে এটা কীভাবে implement করবে, আর কোন কোন pitfall-এর দিকে নজর রাখবে?""",
        a_en=r"""
            **Clarify:** should related data (a deleted user's posts) also hide? Can a deleted user's email be reused? Who can see or restore deleted items?

            **Implementation — a reusable plugin:**
            - Add `isDeleted: Boolean` (default `false`, backfilled on existing documents) and `deletedAt: Date`.
            - **Query middleware** on `/^find/` (covers `find`, `findOne`, `findById`, `findOneAndUpdate`…) plus `countDocuments`, `updateOne`, `updateMany`: if the filter doesn't already mention `isDeleted`, add `{ isDeleted: false }`. In query middleware `this` is the Query, so `this.getFilter()` / `this.where()` do the job.
            - **Aggregate middleware:** `pre("aggregate")` prepends `{ $match: { isDeleted: false } }` — aggregations don't trigger find hooks.
            - A `softDelete()` method that sets both fields, used instead of `deleteOne()`.
            - **Purge:** a TTL index on `deletedAt` with `expireAfterSeconds` = 30 days. Documents with no `deletedAt` never expire.
            - **Uniqueness:** make `email` unique only among live users with a partial index (`partialFilterExpression: { isDeleted: false }`) so a deleted account doesn't block re-registration.

            **Pitfalls:** hooks don't cover `Model.collection.*`, the native driver, or `bulkWrite`; `$geoNear`/`$search` must be the first pipeline stage, so prepending `$match` breaks them; `populate()` runs find middleware on the referenced model, so deleted references become `null`; TTL deletion bypasses Mongoose entirely (no cascade, no hooks); every query now has an extra condition, so check that hot indexes still fit (add `isDeleted` to compound indexes where needed).
        """,
        a_bn=r"""
            **আগে প্রশ্ন পরিষ্কার করো:** related data-ও (delete হওয়া user-এর post) কি লুকাবে? Delete হওয়া user-এর email কি আবার ব্যবহার করা যাবে? কে delete হওয়া item দেখতে বা restore করতে পারবে?

            **Implementation — একটা reusable plugin:**
            - `isDeleted: Boolean` (default `false`, আগের document-এ backfill করা) আর `deletedAt: Date` যোগ করো।
            - `/^find/`-এ **query middleware** (`find`, `findOne`, `findById`, `findOneAndUpdate`… cover করে), সাথে `countDocuments`, `updateOne`, `updateMany`: filter-এ আগে থেকে `isDeleted` না থাকলে `{ isDeleted: false }` যোগ করো। Query middleware-এ `this` হলো Query, তাই `this.getFilter()` / `this.where()` দিয়েই কাজ হয়।
            - **Aggregate middleware:** `pre("aggregate")` শুরুতে `{ $match: { isDeleted: false } }` বসিয়ে দেয় — aggregation find hook চালায় না।
            - একটা `softDelete()` method, যেটা দুইটা field-ই set করে আর `deleteOne()`-এর বদলে ব্যবহার হয়।
            - **Purge:** `deletedAt`-এ 30 দিনের `expireAfterSeconds` সহ TTL index। যাদের `deletedAt` নেই, তারা কখনো expire হয় না।
            - **Uniqueness:** partial index দিয়ে (`partialFilterExpression: { isDeleted: false }`) `email` শুধু live user-দের মধ্যে unique রাখো, যাতে delete হওয়া account আবার registration আটকে না দেয়।

            **Pitfall:** hook `Model.collection.*`, native driver বা `bulkWrite` cover করে না; `$geoNear`/`$search` pipeline-এর প্রথম stage হতে হয়, তাই আগে `$match` বসালে এগুলো ভেঙে যায়; `populate()` referenced model-এ find middleware চালায়, তাই delete হওয়া reference `null` হয়ে যায়; TTL deletion পুরোপুরি Mongoose bypass করে (কোনো cascade বা hook নেই); প্রতিটি query-তে এখন একটা বাড়তি condition, তাই hot index এখনো মানানসই কি না দেখো (দরকার হলে compound index-এ `isDeleted` যোগ করো)।
        """,
        ex_en=r"""
            - **Why a boolean plus a date?** Filtering on `isDeleted: false` is simple equality (index- and partial-index-friendly), while `deletedAt` drives the TTL purge. Backfill `isDeleted: false` before enabling the hook, or old documents (missing the field) vanish from queries.
            - **Escape hatch:** admins can query deleted items explicitly (`{ isDeleted: true }`) because the hook leaves filters that already mention `isDeleted` alone.
            - **Alternative design:** move deleted documents into an archive collection (`users_deleted`) inside a transaction. Live queries need no middleware at all; restoring is a move back. It's often simpler when deletes are rare.
            - **Compliance:** if a user requests permanent erasure, soft delete isn't enough — you need a real purge path, including backups policy.
            - **Testing:** write tests that assert deleted documents don't appear via `find`, `findById`, `countDocuments`, `aggregate` and `populate` — that's where regressions hide.
        """,
        ex_bn=r"""
            - **Boolean আর date দুটোই কেন?** `isDeleted: false` দিয়ে filter করা সহজ equality (index আর partial index-এর জন্য সুবিধাজনক), আর `deletedAt` TTL purge চালায়। Hook চালু করার আগে `isDeleted: false` backfill করো, নইলে পুরনো document (যেগুলোতে field নেই) query থেকে উধাও হয়ে যাবে।
            - **Escape hatch:** admin explicitly delete হওয়া item query করতে পারে (`{ isDeleted: true }`), কারণ filter-এ আগে থেকে `isDeleted` থাকলে hook সেটা ছুঁয়ে দেখে না।
            - **বিকল্প design:** delete হওয়া document একটা transaction-এর ভেতরে archive collection-এ (`users_deleted`) সরিয়ে নাও। তখন live query-তে কোনো middleware-ই লাগে না; restore মানে আবার ফিরিয়ে আনা। Delete কম হলে এটা প্রায়ই সহজ।
            - **Compliance:** কোনো user স্থায়ীভাবে মুছে ফেলার অনুরোধ করলে soft delete যথেষ্ট না — backup policy সহ একটা আসল purge পথ লাগবে।
            - **Testing:** এমন test লেখো যেগুলো নিশ্চিত করে delete হওয়া document `find`, `findById`, `countDocuments`, `aggregate` আর `populate`-এ আসে না — regression এখানেই লুকিয়ে থাকে।
        """,
        tip_en=r"""Spend most of the answer on the pitfalls — anyone can write a `pre(/^find/)` hook; knowing where it silently doesn't apply (aggregate, populate, TTL, unique indexes) is what the interviewer is testing.""",
        tip_bn=r"""উত্তরের বেশিরভাগ সময় pitfall-এ দাও — `pre(/^find/)` hook যে কেউ লিখতে পারে; কোথায় এটা চুপচাপ apply হয় না (aggregate, populate, TTL, unique index) সেটা জানাই interviewer যাচাই করছে।""",
        mist_en=r"""Adding only a `find` hook (missing `findOne`, counts and aggregations); forgetting to backfill the flag; keeping a plain unique index on email so deleted users block sign-ups.""",
        mist_bn=r"""শুধু `find` hook যোগ করা (`findOne`, count আর aggregation বাদ পড়ে); flag backfill করতে ভুলে যাওয়া; email-এ সাধারণ unique index রেখে দেওয়া, ফলে delete হওয়া user sign-up আটকে দেয়।""",
        code=r"""
            export function softDeletePlugin(schema) {
              schema.add({
                isDeleted: { type: Boolean, default: false },
                deletedAt: { type: Date },
              });

              // Purge 30 days after soft delete (TTL ignores documents without a Date)
              schema.index({ deletedAt: 1 }, { expireAfterSeconds: 60 * 60 * 24 * 30 });

              function hideDeleted() {                     // Mongoose 9: no next()
                if (!("isDeleted" in this.getFilter())) this.where({ isDeleted: false });
              }
              schema.pre(/^find/, hideDeleted);
              schema.pre(["countDocuments", "updateOne", "updateMany"], hideDeleted);

              schema.pre("aggregate", function () {
                this.pipeline().unshift({ $match: { isDeleted: false } });
              });

              schema.methods.softDelete = function () {
                this.isDeleted = true;
                this.deletedAt = new Date();
                return this.save();
              };
            }

            userSchema.plugin(softDeletePlugin);
            userSchema.index(
              { email: 1 },
              { unique: true, partialFilterExpression: { isDeleted: false } }
            );
        """,
        lang="javascript",
        follow=[
            ("How would you restore a soft-deleted user together with their posts?", "একজন soft-deleted user-কে তার post সহ কীভাবে restore করবে?"),
            ("Would you choose the archive-collection approach instead? When?", "এর বদলে কি archive-collection পদ্ধতি বেছে নেবে? কখন?"),
        ],
        related=["mongoose-014", "mongoose-008"],
        refs=[MIDDLEWARE, PLUGINS],
    ),
    # ------------------------------------------------------------------ mongoose-032
    Q(
        id="mongoose-032", sub="Indexes", diff="extreme", type="architecture",
        prio="high", market="international", mins=18,
        tags=["indexes", "autoindex", "syncindexes", "migrations", "mongodb-9", "production"],
        ver="Mongoose 9.11 (syncIndexes fix for MongoDB 9.0 in 9.10.4 / 8.24.5), MongoDB 9.0", vs=True, status="stable",
        q_en=r"""Your Express + Mongoose API runs as 12 Kubernetes pods against a MongoDB 9.0 replica set (~200 GB). Indexes are declared in schemas, `autoIndex` is on, and the app calls `syncIndexes()` at startup. Last week a deploy added `unique: true` on `users.phone`: no error surfaced, yet duplicates keep appearing. Since the MongoDB 9.0 upgrade, every pod restart also seems to rebuild indexes and spike CPU/IO. Explain what's happening and design a production index-management strategy.""",
        q_bn=r"""তোমার Express + Mongoose API 12টা Kubernetes pod হিসেবে একটা MongoDB 9.0 replica set-এর (~200 GB) বিরুদ্ধে চলে। Index schema-তে declare করা, `autoIndex` চালু, আর app startup-এ `syncIndexes()` call করে। গত সপ্তাহে একটা deploy-এ `users.phone`-এ `unique: true` যোগ হয়েছে: কোনো error দেখা যায়নি, তবুও duplicate আসতেই থাকছে। MongoDB 9.0 upgrade-এর পর থেকে প্রতিবার pod restart-এ index rebuild হচ্ছে বলে মনে হয়, CPU/IO বেড়ে যাচ্ছে। কী ঘটছে ব্যাখ্যা করো, আর production-এর জন্য একটা index-management strategy design করো।""",
        a_en=r"""
            *(Advanced: production operations and data integrity.)*

            **What's happening:**
            - With `autoIndex`, each model calls `createIndexes()` when the app connects — 12 pods race to build the same indexes on every deploy. The new unique index **failed to build** because duplicate phones already existed; Mongoose reports that only as an `'index'` error event / log line, the app keeps running, and the uniqueness you think you have doesn't exist.
            - Known MongoDB 9.0 issue: at FCV 9.0, `listIndexes` reports `collation: { locale: "simple" }`, and Mongoose versions before **9.10.4 / 8.24.5** see that as a difference — so `syncIndexes()` **drops and rebuilds unchanged indexes at each startup**. That's the CPU/IO spike, and while a unique index is being rebuilt it isn't enforcing anything.

            **Strategy — treat indexes like schema migrations:**
            1. **Upgrade Mongoose** to ≥ 9.10.4 and **stop calling `syncIndexes()` at startup**.
            2. **`autoIndex: false` in production.** Schema index definitions stay the source of truth, but nothing builds or drops automatically.
            3. **A migration job, run once per deploy by the pipeline** (not per pod): review `Model.diffIndexes()`, create new indexes explicitly with `createIndexes()` (create-only), and drop only after review.
            4. **Before adding a unique index:** find and resolve duplicates with an aggregation, normalise the data (e.g. phone numbers to `+8801…` format), use a partial index if the field is optional, then build — and **verify the index exists** afterwards.
            5. **Large builds:** run off-peak and monitor progress (`$currentOp`). Index builds hold exclusive locks only briefly but consume CPU/IO and cache on every data-bearing member.
            6. **Safe drops:** **hide** the index first (`collMod` with `hidden: true`), watch latency for a few days, then drop. Unhiding is instant; rebuilding isn't.
            7. **Observability & CI:** alert on model `'index'` errors, compare `diffIndexes()` against staging in CI to detect drift, and review `$indexStats` for unused indexes.
        """,
        a_bn=r"""
            *(Advanced: production operations আর data integrity।)*

            **কী ঘটছে:**
            - `autoIndex` চালু থাকলে app connect হওয়ার সময় প্রতিটি model `createIndexes()` call করে — প্রতিটি deploy-এ 12টা pod একই index বানানোর প্রতিযোগিতায় নামে। নতুন unique index **build হতে fail করেছে**, কারণ আগে থেকেই duplicate phone ছিল; Mongoose এটা শুধু একটা `'index'` error event / log line হিসেবে জানায়, app চলতেই থাকে, আর তুমি যে uniqueness আছে বলে ভাবছ সেটা আসলে নেই।
            - MongoDB 9.0-এর known issue: FCV 9.0-তে `listIndexes` `collation: { locale: "simple" }` report করে, আর **9.10.4 / 8.24.5**-এর আগের Mongoose version এটাকে পার্থক্য হিসেবে দেখে — তাই `syncIndexes()` **প্রতিটি startup-এ অপরিবর্তিত index drop করে আবার build করে**। এটাই CPU/IO spike, আর unique index rebuild হওয়ার সময় সেটা কিছুই enforce করে না।

            **Strategy — index-কে schema migration-এর মতো সামলাও:**
            1. Mongoose **9.10.4 বা তার ওপরে upgrade করো** আর **startup-এ `syncIndexes()` call করা বন্ধ করো**।
            2. **Production-এ `autoIndex: false`।** Schema-র index definition-ই source of truth থাকবে, কিন্তু automatically কিছু build বা drop হবে না।
            3. **একটা migration job, pipeline প্রতি deploy-এ একবার চালাবে** (প্রতি pod-এ না): `Model.diffIndexes()` review করো, নতুন index explicitly `createIndexes()` দিয়ে বানাও (শুধু create করে), আর review-এর পরেই কেবল drop করো।
            4. **Unique index যোগ করার আগে:** aggregation দিয়ে duplicate খুঁজে সমাধান করো, data normalise করো (যেমন phone number `+8801…` format-এ), field optional হলে partial index ব্যবহার করো, তারপর build করো — আর পরে **index আসলেই আছে কি না verify করো**।
            5. **বড় build:** কম traffic-এর সময় চালাও আর progress দেখো (`$currentOp`)। Index build অল্প সময়ের জন্য exclusive lock নেয়, কিন্তু প্রতিটি data-bearing member-এ CPU/IO আর cache খরচ করে।
            6. **নিরাপদ drop:** আগে index **hide** করো (`hidden: true` সহ `collMod`), কয়েক দিন latency দেখো, তারপর drop করো। Unhide সাথে সাথে হয়; rebuild হয় না।
            7. **Observability ও CI:** model-এর `'index'` error-এ alert দাও, drift ধরতে CI-তে staging-এর বিরুদ্ধে `diffIndexes()` compare করো, আর অব্যবহৃত index-এর জন্য `$indexStats` review করো।
        """,
        ex_en=r"""
            - **`createIndexes()` vs `syncIndexes()`:** `createIndexes()` only builds what's missing; `syncIndexes()` also **drops** indexes that aren't in the schema — including ones a DBA added by hand for a hot query. Dropping should always be a reviewed, deliberate step.
            - **Why not per pod?** Index management is a cluster-level operation; doing it from every replica of the app multiplies load, creates races and hides failures in individual pod logs.
            - **Rolling index builds** (one member at a time) exist for the rare cases where a simultaneous replica-set build is too disruptive; they're operationally heavier.
            - **Atlas:** the same principles apply; Atlas also surfaces index suggestions (Performance Advisor) — treat them as input for a migration, not auto-apply.
            - **Version awareness:** this incident combines a MongoDB server change and an ODM bug fix; reading both release notes before upgrading is part of the job.
        """,
        ex_bn=r"""
            - **`createIndexes()` বনাম `syncIndexes()`:** `createIndexes()` শুধু যেটা নেই সেটা build করে; `syncIndexes()` schema-তে না থাকা index **drop-ও করে** — এমনকি কোনো DBA hot query-র জন্য হাতে বানানো index-ও। Drop করা সবসময় review করা, সচেতন একটা ধাপ হওয়া উচিত।
            - **প্রতি pod-এ কেন না?** Index management একটা cluster-level কাজ; app-এর প্রতিটি replica থেকে করলে load বহুগুণ বাড়ে, race তৈরি হয়, আর failure আলাদা আলাদা pod log-এ লুকিয়ে থাকে।
            - **Rolling index build** (একবারে একটা member) আছে সেই বিরল ক্ষেত্রের জন্য, যখন পুরো replica set-এ একসাথে build খুব বিঘ্ন ঘটায়; এটা operationally ভারী।
            - **Atlas:** একই নীতি খাটে; Atlas index-এর পরামর্শও দেখায় (Performance Advisor) — এগুলো auto-apply না করে migration-এর input হিসেবে নাও।
            - **Version সচেতনতা:** এই incident-এ একটা MongoDB server পরিবর্তন আর একটা ODM bug fix মিলে গেছে; upgrade-এর আগে দুটোর release note পড়াও কাজের অংশ।
        """,
        tip_en=r"""Name the integrity risk first ("we believe phone is unique, but it isn't") — it's more serious than the CPU spike. Then present the migration-based workflow with hide-before-drop; that's what operators of large systems recognise as experience.""",
        tip_bn=r"""আগে integrity-র ঝুঁকিটা বলো ("আমরা ভাবছি phone unique, কিন্তু আসলে না") — এটা CPU spike-এর চেয়ে গুরুতর। তারপর hide-before-drop সহ migration-ভিত্তিক workflow দেখাও; বড় system চালানো লোকেরা এটাকেই অভিজ্ঞতা হিসেবে চেনে।""",
        mist_en=r"""Leaving `autoIndex` on in production "because it's convenient"; running `syncIndexes()` on every boot; assuming a unique index exists because it's in the schema; dropping an index without hiding it first.""",
        mist_bn=r""""সুবিধাজনক" বলে production-এ `autoIndex` চালু রাখা; প্রতিটি boot-এ `syncIndexes()` চালানো; schema-তে আছে বলেই unique index আছে ধরে নেওয়া; আগে hide না করে index drop করা।""",
        code=r"""
            // App startup (production): never build or drop indexes here
            await mongoose.connect(process.env.MONGODB_URI, { autoIndex: false });

            // migrations/2026-10-12-users-phone-unique.js — run once by the deploy pipeline
            const dups = await User.aggregate([
              { $match: { phone: { $type: "string" } } },
              { $group: { _id: "$phone", ids: { $push: "$_id" }, n: { $sum: 1 } } },
              { $match: { n: { $gt: 1 } } },
            ]);
            if (dups.length) throw new Error(`Resolve ${dups.length} duplicate phone numbers first`);

            console.log(await User.diffIndexes());   // { toDrop: [...], toCreate: [...] } — review
            await User.createIndexes();               // builds missing indexes only; never drops

            // Later, to retire an index safely: hide → observe → drop
            await mongoose.connection.db.command({
              collMod: "users",
              index: { name: "status_1_createdAt_-1", hidden: true },
            });
        """,
        lang="javascript",
        follow=[
            ("How would you add a unique index on 50 million documents with minimal impact?", "50 million document-এ সবচেয়ে কম প্রভাব ফেলে কীভাবে unique index যোগ করবে?"),
            ("A DBA added an index manually for a hot query. How do you keep it from being dropped by tooling?", "একজন DBA একটা hot query-র জন্য হাতে একটা index বানিয়েছে। Tooling যেন সেটা drop না করে, কীভাবে নিশ্চিত করবে?"),
        ],
        related=["mongoose-003", "mongoose-030"],
        refs=[MODEL_API, RN_90, INDEX_BUILDS],
    ),
]

if __name__ == "__main__":
    save("mongoose", "b3", QUESTIONS)
