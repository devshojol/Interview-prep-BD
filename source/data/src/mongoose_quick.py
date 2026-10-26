# Mongoose — quick-recall questions (mongoose-q01..mongoose-q10)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

GUIDE = ("Mongoose — Getting Started", "https://mongoosejs.com/docs/index.html")
CONNECTIONS = ("Mongoose — Connections", "https://mongoosejs.com/docs/connections.html")
QUERIES = ("Mongoose — Queries", "https://mongoosejs.com/docs/queries.html")
TIMESTAMPS = ("Mongoose — Timestamps", "https://mongoosejs.com/docs/timestamps.html")
VIRTUALS = ("Mongoose — Virtuals", "https://mongoosejs.com/docs/tutorials/virtuals.html")
MIDDLEWARE = ("Mongoose — Middleware", "https://mongoosejs.com/docs/middleware.html")
QUERY_API = ("Mongoose API — Query", "https://mongoosejs.com/docs/api/query.html")
FOAU = ("Mongoose — How to Use findOneAndUpdate()", "https://mongoosejs.com/docs/tutorials/findoneandupdate.html")
SUBDOCS = ("Mongoose — Subdocuments", "https://mongoosejs.com/docs/subdocs.html")
TS_SCHEMAS = ("Mongoose — Schemas in TypeScript", "https://mongoosejs.com/docs/typescript/schemas.html")

QUESTIONS = [
    # ------------------------------------------------------------------ mongoose-q01
    Q(
        id="mongoose-q01", sub="Mongoose vs Native Driver", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["odm", "basics", "schema", "validation"],
        ver="Mongoose 9.x", vs=False, status="stable",
        q_en=r"""What is Mongoose, and why do people use it with MongoDB?""",
        q_bn=r"""Mongoose কী, আর MongoDB-র সাথে মানুষ এটা কেন ব্যবহার করে?""",
        a_en=r"""Mongoose is an ODM (Object Data Modeling) library for MongoDB in Node.js, built on top of the official driver. It adds schemas with types, casting, validation and defaults, plus middleware, `populate()` and a model-based API, so your data keeps a consistent shape even though MongoDB itself doesn't force one.""",
        a_bn=r"""Mongoose হলো Node.js-এ MongoDB-র জন্য একটা ODM (Object Data Modeling) library, যেটা official driver-এর ওপর তৈরি। এটা type, casting, validation আর default-সহ schema দেয়, সাথে middleware, `populate()` আর model-ভিত্তিক API; তাই MongoDB নিজে কোনো shape force না করলেও তোমার data-র shape consistent থাকে।""",
        code=r"""
            const User = mongoose.model("User", new mongoose.Schema({
              name: { type: String, required: true }, age: Number,
            }));
            const u = await User.create({ name: "Rafi", age: "25" });
            console.log(u.age, typeof u.age);  // → 25 'number' (cast from "25")
            await User.create({ age: 30 });     // → ValidationError: ... Path `name` is required.
        """,
        lang="javascript",
        ex_en=r"""The schema lives only in your app: writes made by other tools or by the native driver skip Mongoose's validation.""",
        ex_bn=r"""Schema শুধু তোমার app-এই থাকে: অন্য tool বা native driver দিয়ে করা write Mongoose-এর validation এড়িয়ে যায়।""",
        tip_en=r"""Say "ODM on top of the driver" and name two things it adds, such as validation and `populate()`.""",
        tip_bn=r"""বলো "driver-এর ওপর একটা ODM", আর এটা যোগ করে এমন দুইটা জিনিসের নাম বলো, যেমন validation আর `populate()`।""",
        follow=[("When would you use the native driver instead?", "কখন এর বদলে native driver ব্যবহার করবে?")],
        related=["mongoose-020", "mongoose-001"],
        refs=[GUIDE],
    ),
    # ------------------------------------------------------------------ mongoose-q02
    Q(
        id="mongoose-q02", sub="Connections", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["connect", "connection-pool", "startup"],
        ver="Mongoose 9.x", vs=False, status="stable",
        q_en=r"""How do you connect to MongoDB with Mongoose, and where should you do it?""",
        q_bn=r"""Mongoose দিয়ে MongoDB-তে কীভাবে connect করবে, আর সেটা কোথায় করা উচিত?""",
        a_en=r"""Call `await mongoose.connect(uri)` once when the app starts, before it accepts requests. Models created with `mongoose.model()` use this default connection, and Mongoose keeps a connection pool, so you never connect per request. Use `mongoose.createConnection()` only when you need several databases.""",
        a_bn=r"""App start হওয়ার সময় একবার, request নেওয়ার আগেই, `await mongoose.connect(uri)` call করো। `mongoose.model()` দিয়ে বানানো model এই default connection ব্যবহার করে, আর Mongoose একটা connection pool রাখে, তাই প্রতি request-এ connect করতে হয় না। একাধিক database লাগলে তবেই `mongoose.createConnection()` ব্যবহার করো।""",
        code=r"""
            import mongoose from "mongoose";

            await mongoose.connect(process.env.MONGODB_URI);  // e.g. mongodb://127.0.0.1:27017/shop
            console.log(mongoose.connection.readyState);       // → 1 (connected)
            mongoose.connection.on("error", (err) => console.error(err));
            app.listen(3000);
        """,
        lang="javascript",
        ex_en=r"""Keep the URI in an environment variable, never in the code. A model registered on a connection that never opens doesn't fail at once: its operations buffer and then time out.""",
        ex_bn=r"""URI environment variable-এ রাখো, code-এ কখনো না। যে connection কখনো খোলে না, তাতে register করা model সাথে সাথে fail করে না: operation-গুলো buffer হয়ে থাকে, তারপর timeout হয়।""",
        tip_en=r"""Mention "connect once at startup, reuse the pool": that's the point most juniors miss.""",
        tip_bn=r"""বলো "startup-এ একবার connect, তারপর pool reuse": বেশিরভাগ junior এই কথাটাই বাদ দেয়।""",
        follow=[("What happens to queries sent before the connection is open?", "Connection খোলার আগেই query পাঠালে কী হয়?")],
        related=["mongoose-029"],
        refs=[CONNECTIONS],
    ),
    # ------------------------------------------------------------------ mongoose-q03
    Q(
        id="mongoose-q03", sub="Documents & Queries", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["find", "findone", "findbyid", "queries"],
        ver="Mongoose 9.x", vs=False, status="stable",
        q_en=r"""What is the difference between `find()`, `findOne()` and `findById()` in Mongoose?""",
        q_bn=r"""Mongoose-এ `find()`, `findOne()` আর `findById()`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""`find(filter)` returns an array of all matching documents, or an empty array. `findOne(filter)` returns the first match or `null`. `findById(id)` is a shortcut for `findOne({ _id: id })` that also casts a string id to an `ObjectId`.""",
        a_bn=r"""`find(filter)` match করা সব document-এর একটা array দেয়, কিছু না পেলে empty array। `findOne(filter)` প্রথম match-টা দেয়, না পেলে `null`। `findById(id)` হলো `findOne({ _id: id })`-এর shortcut, যেটা string id-কে `ObjectId`-তে cast-ও করে।""",
        code=r"""
            await User.find({ age: { $gte: 18 } });   // → [doc, doc, ...] or []
            await User.findOne({ email: "a@x.com" }); // → doc or null
            await User.findById("6709a1f2c3d4e5f601234567"); // → doc or null
        """,
        lang="javascript",
        ex_en=r"""Without a `sort()`, "first" in `findOne` just means the first one MongoDB finds. An invalid id string like `"abc"` makes `findById` throw a `CastError`.""",
        ex_bn=r"""`sort()` না দিলে `findOne`-এর "প্রথম" মানে শুধু MongoDB যেটা আগে পায়। `"abc"`-এর মতো ভুল id string দিলে `findById` একটা `CastError` throw করে।""",
        tip_en=r"""Give the return value of each one, including the empty case (`[]` or `null`).""",
        tip_bn=r"""প্রতিটার return value বলো, কিছু না পাওয়ার case-সহ (`[]` বা `null`)।""",
        follow=[("How do you return a 404 neatly when `findById` finds nothing?", "`findById` কিছু না পেলে সুন্দরভাবে 404 কীভাবে দেবে?")],
        related=["mongoose-005", "mongoose-011"],
        refs=[QUERIES],
    ),
    # ------------------------------------------------------------------ mongoose-q04
    Q(
        id="mongoose-q04", sub="Schemas & Models", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["timestamps", "createdat", "updatedat", "schema-options"],
        ver="Mongoose 9.x", vs=False, status="stable",
        q_en=r"""What does the `timestamps` schema option do in Mongoose?""",
        q_bn=r"""Mongoose-এ `timestamps` schema option কী করে?""",
        a_en=r"""`{ timestamps: true }` makes Mongoose add `createdAt` and `updatedAt` `Date` fields. Both are set when the document is created, and `updatedAt` is refreshed on `save()` and on update queries such as `updateOne()` and `findOneAndUpdate()`.""",
        a_bn=r"""`{ timestamps: true }` দিলে Mongoose `createdAt` আর `updatedAt` নামে দুইটা `Date` field যোগ করে। Document তৈরির সময় দুটোই set হয়, আর `save()` এবং `updateOne()`, `findOneAndUpdate()`-এর মতো update query-তে `updatedAt` নতুন করে set হয়।""",
        code=r"""
            const Post = mongoose.model("Post", new mongoose.Schema({ title: String }, { timestamps: true }));
            const p = await Post.create({ title: "Hi" });  // createdAt === updatedAt
            await Post.updateOne({ _id: p._id }, { title: "Hello" });
            // → updatedAt moves forward, createdAt stays the same
        """,
        lang="javascript",
        ex_en=r"""Writes through the native driver (`Post.collection.updateOne(...)`) bypass Mongoose, so `updatedAt` isn't touched. You can rename the fields: `timestamps: { createdAt: "created_at" }`.""",
        ex_bn=r"""Native driver দিয়ে write করলে (`Post.collection.updateOne(...)`) Mongoose বাদ পড়ে, তাই `updatedAt` বদলায় না। Field-এর নামও বদলানো যায়: `timestamps: { createdAt: "created_at" }`।""",
        tip_en=r"""Say which operations update `updatedAt`, and name the native-driver exception.""",
        tip_bn=r"""কোন কোন operation-এ `updatedAt` update হয় সেটা বলো, আর native driver-এর ব্যতিক্রমটা উল্লেখ করো।""",
        follow=[("How would you add a timestamp only when a status changes?", "শুধু status বদলালে একটা timestamp কীভাবে যোগ করবে?")],
        related=["mongoose-002"],
        refs=[TIMESTAMPS],
    ),
    # ------------------------------------------------------------------ mongoose-q05
    Q(
        id="mongoose-q05", sub="Virtuals", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["virtuals", "computed-fields", "tojson"],
        ver="Mongoose 9.x", vs=False, status="stable",
        q_en=r"""What is a virtual in Mongoose?""",
        q_bn=r"""Mongoose-এ virtual কী?""",
        a_en=r"""A virtual is a computed property defined on the schema that is not stored in MongoDB, like `fullName` built from `firstName` and `lastName`. You can read it on documents, but you can't query or sort by it, and it isn't in JSON output unless you set `toJSON: { virtuals: true }`.""",
        a_bn=r"""Virtual হলো schema-তে define করা একটা computed property, যেটা MongoDB-তে store হয় না, যেমন `firstName` আর `lastName` থেকে বানানো `fullName`। Document-এ এটা পড়া যায়, কিন্তু এটা দিয়ে query বা sort করা যায় না, আর `toJSON: { virtuals: true }` না দিলে JSON output-এ আসে না।""",
        code=r"""
            const personSchema = new mongoose.Schema({ firstName: String, lastName: String });
            personSchema.virtual("fullName").get(function () {
              return `${this.firstName} ${this.lastName}`;
            });
            const p = await Person.create({ firstName: "Nusrat", lastName: "Jahan" });
            console.log(p.fullName);  // → Nusrat Jahan (stored fields: _id, firstName, lastName, __v)
        """,
        lang="javascript",
        ex_en=r"""Use a regular function for the getter so `this` is the document. Virtuals are also missing from `.lean()` results, because those are plain objects.""",
        ex_bn=r"""Getter-এ সাধারণ function ব্যবহার করো, যাতে `this` document হয়। `.lean()` result-এও virtual থাকে না, কারণ সেগুলো plain object।""",
        tip_en=r"""Say "computed, not stored, not queryable" and mention the `toJSON` option.""",
        tip_bn=r"""বলো "computed, store হয় না, query করা যায় না", আর `toJSON` option-টা উল্লেখ করো।""",
        follow=[("What is virtual populate?", "Virtual populate কী?")],
        related=["mongoose-007", "mongoose-028"],
        refs=[VIRTUALS],
    ),
    # ------------------------------------------------------------------ mongoose-q06
    Q(
        id="mongoose-q06", sub="Middleware & Hooks", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["middleware", "pre-save", "post-save", "hooks", "mongoose-9"],
        ver="Mongoose 9.x (pre hooks get no next())", vs=True, status="stable",
        q_en=r"""What are `pre` and `post` middleware (hooks) in Mongoose, and how do you write one in Mongoose 9?""",
        q_bn=r"""Mongoose-এ `pre` আর `post` middleware (hook) কী, আর Mongoose 9-এ কীভাবে লিখবে?""",
        a_en=r"""Middleware are functions that run before (`pre`) or after (`post`) an operation such as `save`, `validate`, `deleteOne`, `find` or `aggregate`. In Mongoose 9 pre hooks no longer receive `next()`: write an `async function` and `throw` to stop the operation. Use a regular function so `this` is the document (or the query, in query middleware).""",
        a_bn=r"""Middleware হলো এমন function, যেটা `save`, `validate`, `deleteOne`, `find` বা `aggregate`-এর মতো কোনো operation-এর আগে (`pre`) বা পরে (`post`) চলে। Mongoose 9-এ pre hook আর `next()` পায় না: একটা `async function` লেখো, আর operation থামাতে `throw` করো। সাধারণ function ব্যবহার করো, যাতে `this` হয় document (query middleware-এ query)।""",
        code=r"""
            userSchema.pre("save", async function () {
              if (!this.isModified("password")) return;
              this.password = await bcrypt.hash(this.password, 10);
            });
            userSchema.post("save", function (doc) {
              console.log("saved", doc.email);
            });
        """,
        lang="javascript",
        ex_en=r"""`save` hooks don't run for `updateOne()` or `findByIdAndUpdate()`: those trigger query middleware instead. That's why a password-hashing hook can be skipped by an update query.""",
        ex_bn=r"""`updateOne()` বা `findByIdAndUpdate()`-এ `save` hook চলে না: এগুলো query middleware trigger করে। এজন্যই update query দিয়ে password-hashing hook এড়িয়ে যাওয়া সম্ভব।""",
        tip_en=r"""Mention the Mongoose 9 change (no `next()`) and the document vs query middleware split.""",
        tip_bn=r"""Mongoose 9-এর পরিবর্তনটা (`next()` নেই) আর document বনাম query middleware-এর ভাগটা উল্লেখ করো।""",
        follow=[("Which hook runs for `findOneAndUpdate()`?", "`findOneAndUpdate()`-এ কোন hook চলে?")],
        related=["mongoose-013", "mongoose-014"],
        refs=[MIDDLEWARE],
    ),
    # ------------------------------------------------------------------ mongoose-q07
    Q(
        id="mongoose-q07", sub="Documents & Queries", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["select", "projection", "select-false", "security"],
        ver="Mongoose 9.x", vs=False, status="stable",
        q_en=r"""How do you hide a field like `password` from query results in Mongoose?""",
        q_bn=r"""Mongoose-এ query result থেকে `password`-এর মতো একটা field কীভাবে লুকাবে?""",
        a_en=r"""Set `select: false` on the schema path, so every query leaves that field out by default. When you really need it, such as at login, opt back in with `.select("+password")`. For one-off projections, `.select("name email")` includes fields and `.select("-field")` excludes them.""",
        a_bn=r"""Schema path-এ `select: false` দাও, তাহলে default-ভাবে কোনো query সেই field আনবে না। সত্যিই দরকার হলে, যেমন login-এর সময়, `.select("+password")` দিয়ে আবার আনো। এক-আধবারের projection-এর জন্য `.select("name email")` field include করে আর `.select("-field")` বাদ দেয়।""",
        code=r"""
            const userSchema = new mongoose.Schema({
              name: String, email: String, password: { type: String, select: false },
            });
            await User.findOne({ email }).lean();                    // → { _id, name, email, __v }
            await User.findOne({ email }).select("+password").lean(); // → also has password
            await User.findOne({ email }).select("name -_id").lean(); // → { name: 'Rafi' }
        """,
        lang="javascript",
        ex_en=r"""`select: false` protects every route at once; remembering `.select("-password")` in each route is easy to forget. For API responses, a `toJSON` transform or an explicit response object adds another layer.""",
        ex_bn=r"""`select: false` একসাথে সব route-কে রক্ষা করে; প্রতিটি route-এ `.select("-password")` মনে রাখা সহজেই ভুলে যাওয়া যায়। API response-এর জন্য `toJSON` transform বা আলাদা response object আরেকটা স্তর যোগ করে।""",
        tip_en=r"""Show `select: false` plus `+password` at login: it shows you think about security by default.""",
        tip_bn=r"""`select: false` আর login-এ `+password` দেখাও: এতে বোঝা যায় তুমি শুরু থেকেই security নিয়ে ভাবো।""",
        follow=[("How would you hide fields from populated documents?", "Populate করা document থেকে field কীভাবে লুকাবে?")],
        related=["mongoose-026", "mongoose-002"],
        refs=[QUERY_API],
    ),
    # ------------------------------------------------------------------ mongoose-q08
    Q(
        id="mongoose-q08", sub="CRUD", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["findoneandupdate", "findbyidandupdate", "returndocument", "mongoose-9"],
        ver="Mongoose 9.x (`new` deprecated since 9.2)", vs=True, status="stable",
        q_en=r"""Why does `findByIdAndUpdate()` return the old document, and how do you get the updated one?""",
        q_bn=r"""`findByIdAndUpdate()` কেন পুরনো document return করে, আর update হওয়া document কীভাবে পাবে?""",
        a_en=r"""By default `findOneAndUpdate()` and `findByIdAndUpdate()` return the document as it was **before** the update. Pass `{ returnDocument: "after" }` to get the updated one; the older `new: true` option does the same but is deprecated since Mongoose 9.2. Add `runValidators: true` if the update should be validated.""",
        a_bn=r"""Default-ভাবে `findOneAndUpdate()` আর `findByIdAndUpdate()` update-এর **আগের** document return করে। Update হওয়া document পেতে `{ returnDocument: "after" }` দাও; পুরনো `new: true` option-ও একই কাজ করে, কিন্তু Mongoose 9.2 থেকে deprecated। Update validate করাতে চাইলে `runValidators: true` যোগ করো।""",
        code=r"""
            // { name: "Pen", price: 10 }
            (await Product.findByIdAndUpdate(id, { price: 15 })).price;  // → 10 (before)
            (await Product.findByIdAndUpdate(id, { price: 20 },
              { returnDocument: "after", runValidators: true })).price;  // → 20 (after)
        """,
        lang="javascript",
        ex_en=r"""If no document matches, both forms return `null`, so the route should still answer 404.""",
        ex_bn=r"""কোনো document match না করলে দুই ক্ষেত্রেই `null` আসে, তাই route-কে তখনও 404 দিতে হবে।""",
        tip_en=r"""Name the current option (`returnDocument: "after"`) and say that `new: true` is the legacy spelling.""",
        tip_bn=r"""এখনকার option-টা (`returnDocument: "after"`) বলো, আর বলো যে `new: true` পুরনো লেখা।""",
        follow=[("Does `findByIdAndUpdate()` run `pre('save')` hooks?", "`findByIdAndUpdate()` কি `pre('save')` hook চালায়?")],
        related=["mongoose-012", "mongo-021"],
        refs=[FOAU],
    ),
    # ------------------------------------------------------------------ mongoose-q09
    Q(
        id="mongoose-q09", sub="Documents & Queries", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["subdocuments", "arrays", "positional-operator", "save"],
        ver="Mongoose 9.x", vs=False, status="stable",
        q_en=r"""How do you add, change and remove items in an array of subdocuments in Mongoose?""",
        q_bn=r"""Mongoose-এ subdocument-এর array-তে item কীভাবে যোগ, পরিবর্তন আর মুছবে?""",
        a_en=r"""Define the array with a child schema (`items: [itemSchema]`), so each item gets its own `_id`, casting and validation. On a loaded document, `push()` a new item, find one with `doc.items.id(itemId)`, change it or call `deleteOne()` on it, then `save()`. For one atomic change without loading, use `updateOne` with the positional `$` operator.""",
        a_bn=r"""Array-টা একটা child schema দিয়ে define করো (`items: [itemSchema]`), তাহলে প্রতিটি item নিজের `_id`, casting আর validation পায়। Load করা document-এ নতুন item `push()` করো, `doc.items.id(itemId)` দিয়ে একটা item খুঁজে বদলাও বা তার ওপর `deleteOne()` call করো, তারপর `save()`। Load না করে একটা atomic পরিবর্তনের জন্য positional `$` operator-সহ `updateOne` ব্যবহার করো।""",
        code=r"""
            const order = await Order.findById(orderId);
            order.items.push({ sku: "C", qty: 1 });
            order.items.id(itemId).qty = 5;
            await order.save();
            // atomic, without loading the order:
            await Order.updateOne({ _id: orderId, "items._id": itemId }, { $inc: { "items.$.qty": 1 } });
        """,
        lang="javascript",
        ex_en=r"""The load-modify-`save()` path runs subdocument validation and hooks but is read-modify-write, so concurrent edits can overwrite each other; the `$inc` path is atomic but skips `save` hooks.""",
        ex_bn=r"""Load করে বদলে `save()` করলে subdocument validation আর hook চলে, কিন্তু এটা read-modify-write, তাই একসাথে কয়েকজন edit করলে একে অপরের লেখা overwrite হতে পারে; `$inc`-এর পথ atomic, কিন্তু `save` hook চলে না।""",
        tip_en=r"""Show both paths and say when you'd pick each one: rich edits vs a hot counter.""",
        tip_bn=r"""দুইটা পথই দেখাও, আর কখন কোনটা নেবে সেটা বলো: বিস্তারিত edit বনাম ঘনঘন বদলানো counter।""",
        follow=[("When would you move the array into its own collection instead?", "কখন array-টা আলাদা collection-এ সরিয়ে নেবে?")],
        related=["mongoose-004", "mongoose-025"],
        refs=[SUBDOCS],
    ),
    # ------------------------------------------------------------------ mongoose-q10
    Q(
        id="mongoose-q10", sub="Schemas & Models", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["typescript", "inferschematype", "hydrateddocument", "types"],
        ver="Mongoose 9.x with TypeScript", vs=False, status="stable",
        q_en=r"""How do you type a Mongoose model in TypeScript without writing the interface twice?""",
        q_bn=r"""Interface দুইবার না লিখে TypeScript-এ একটা Mongoose model-এর type কীভাবে দেবে?""",
        a_en=r"""Let Mongoose infer the type from the schema: `InferSchemaType<typeof userSchema>` gives the plain data shape, and `model("User", userSchema)` is typed automatically. `HydratedDocument<User>` is the type of a loaded document with `save()` and other document methods. A hand-written interface also works, but it can drift from the schema.""",
        a_bn=r"""Schema থেকেই Mongoose-কে type বের করতে দাও: `InferSchemaType<typeof userSchema>` plain data-র shape দেয়, আর `model("User", userSchema)` নিজে থেকেই typed হয়। `HydratedDocument<User>` হলো load করা document-এর type, যেখানে `save()` আর অন্য document method থাকে। হাতে লেখা interface-ও চলে, কিন্তু সেটা schema থেকে আলাদা হয়ে যেতে পারে।""",
        code=r"""
            import { Schema, model, InferSchemaType, HydratedDocument } from "mongoose";

            const userSchema = new Schema({ name: { type: String, required: true }, age: Number });
            type User = InferSchemaType<typeof userSchema>;   // name: string, age optional
            const UserModel = model("User", userSchema);
            const u: HydratedDocument<User> | null = await UserModel.findById(id);
        """,
        lang="typescript",
        ex_en=r"""A required field becomes a non-optional type; fields without `required` become optional and may be `null`. Instance methods and statics need extra generic parameters on `Schema`/`model`.""",
        ex_bn=r"""Required field non-optional type হয়; `required` ছাড়া field optional হয় আর `null`-ও হতে পারে। Instance method আর static-এর জন্য `Schema`/`model`-এ বাড়তি generic parameter দিতে হয়।""",
        tip_en=r"""Say "single source of truth: the schema" and name `InferSchemaType` and `HydratedDocument`.""",
        tip_bn=r"""বলো "একটাই source of truth: schema", আর `InferSchemaType` ও `HydratedDocument`-এর নাম বলো।""",
        follow=[("How would you type an instance method like `comparePassword`?", "`comparePassword`-এর মতো একটা instance method-এর type কীভাবে দেবে?")],
        related=["mongoose-001", "mongoose-008"],
        refs=[TS_SCHEMAS],
    ),
]

save("mongoose", "quick", QUESTIONS)
