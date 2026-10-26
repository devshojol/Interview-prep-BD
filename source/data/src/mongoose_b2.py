# Mongoose — batch 2 (mongoose-006, 007, 013, 014, 015, 024, 025, 031)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

POPULATE = ("Mongoose — Populate", "https://mongoosejs.com/docs/populate.html")
SCHEMATYPES = ("Mongoose — SchemaTypes", "https://mongoosejs.com/docs/schematypes.html")
VIRTUALS = ("Mongoose — Mongoose Virtuals", "https://mongoosejs.com/docs/tutorials/virtuals.html")
GUIDE = ("Mongoose — Schemas guide", "https://mongoosejs.com/docs/guide.html")
MIDDLEWARE = ("Mongoose — Middleware", "https://mongoosejs.com/docs/middleware.html")
MIGRATE9 = ("Mongoose — Migrating to 9", "https://mongoosejs.com/docs/migrating_to_9.html")
LOOKUP = ("MongoDB Manual — $lookup (aggregation)", "https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/")
AGGREGATE_API = ("Mongoose API — Aggregate", "https://mongoosejs.com/docs/api/aggregate.html")
LEAN = ("Mongoose — Faster Mongoose Queries With Lean", "https://mongoosejs.com/docs/tutorials/lean.html")
QUERIES = ("Mongoose — Queries", "https://mongoosejs.com/docs/queries.html")
ESR = ("MongoDB Manual — The ESR (Equality, Sort, Range) Guideline", "https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-guideline/")
ATOMICITY = ("MongoDB Manual — Atomicity and Transactions", "https://www.mongodb.com/docs/manual/core/write-operations-atomicity/")
TRANSACTIONS = ("Mongoose — Transactions", "https://mongoosejs.com/docs/transactions.html")

QUESTIONS = [
    # ------------------------------------------------------------------ mongoose-006
    Q(
        id="mongoose-006", sub="References & Populate", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["populate", "references", "objectid", "ref"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""How do you model a relationship between `Post` and `User` using references in Mongoose, and what does `populate()` actually do?""",
        q_bn=r"""Mongoose-এ reference ব্যবহার করে `Post` আর `User`-এর মধ্যে relationship কীভাবে model করবে, আর `populate()` আসলে কী করে?""",
        a_en=r"""
            In the post schema I store the author's ID with `type: Schema.Types.ObjectId, ref: "User"`. The `ref` tells Mongoose which model the ID belongs to.

            `populate("author")` replaces that ID with the actual user document. Under the hood it's **not a database join**: Mongoose runs the post query, collects all author IDs, then runs **one more query** like `User.find({ _id: { $in: ids } })` and stitches the results into the posts. I usually limit the fields — `.populate("author", "name avatarUrl")` — so I don't send emails or password hashes to the client.

            If a referenced user has been deleted, the populated field becomes `null`, so the code must handle that.
        """,
        a_bn=r"""
            Post schema-তে আমি author-এর ID রাখি `type: Schema.Types.ObjectId, ref: "User"` দিয়ে। `ref` Mongoose-কে জানায় ID-টা কোন model-এর।

            `populate("author")` ওই ID-কে আসল user document দিয়ে replace করে। ভেতরে ভেতরে এটা **database join না**: Mongoose আগে post query চালায়, সব author ID জড়ো করে, তারপর `User.find({ _id: { $in: ids } })`-এর মতো **আরেকটা query** চালিয়ে result-গুলো post-এর সাথে জুড়ে দেয়। আমি সাধারণত field সীমিত রাখি — `.populate("author", "name avatarUrl")` — যাতে client-এ email বা password hash না যায়।

            Referenced user delete হয়ে গেলে populated field `null` হয়ে যায়, তাই code-এ সেটা handle করতে হয়।
        """,
        quick_en=r"""Store the author's ID with `type: Schema.Types.ObjectId, ref: "User"`. `populate("author")` is not a database join: Mongoose runs one more query (`User.find({ _id: { $in: ids } })`) and swaps the IDs for documents; limit fields with `.populate("author", "name avatarUrl")` and handle `null` for deleted users.""",
        quick_bn=r"""Post-এ author-এর ID রাখো `type: Schema.Types.ObjectId, ref: "User"` দিয়ে। `populate("author")` database join না: Mongoose আরেকটা query চালায় (`User.find({ _id: { $in: ids } })`) আর ID-র জায়গায় document বসিয়ে দেয়; `.populate("author", "name avatarUrl")` দিয়ে field সীমিত করো, আর user delete হয়ে গেলে `null` handle করো।""",
        ex_en=r"""
            - **Reference vs embed:** reference when the related data is shared, large or updated independently (a user's profile is used across posts, comments, orders). Embed subdocuments when the data belongs only to the parent and stays bounded (an order's items).
            - **Cost:** each populated path is an extra round trip. Populating inside a loop (one post at a time) recreates the N+1 problem — populate the whole result set at once.
            - **Arrays of refs** (`followers: [{ type: ObjectId, ref: "User" }]`) can grow unbounded; for one-to-many relationships prefer storing the parent ID on the child and using virtual populate.
            - **Works with `lean()`:** populated data is attached to the plain objects too.
        """,
        ex_bn=r"""
            - **Reference বনাম embed:** related data shared, বড় বা আলাদাভাবে update হলে reference করো (user-এর profile post, comment, order — সব জায়গায় ব্যবহার হয়)। Data শুধু parent-এর এবং bounded থাকলে subdocument embed করো (order-এর item)।
            - **খরচ:** প্রতিটি populated path মানে একটা বাড়তি round trip। Loop-এর ভেতরে (এক এক করে post) populate করলে N+1 সমস্যা ফিরে আসে — পুরো result set একবারে populate করো।
            - **Ref-এর array** (`followers: [{ type: ObjectId, ref: "User" }]`) সীমাহীনভাবে বাড়তে পারে; one-to-many relationship-এ child-এ parent ID রেখে virtual populate ব্যবহার করা ভালো।
            - **`lean()`-এর সাথেও কাজ করে:** populated data plain object-এও যুক্ত হয়।
        """,
        tip_en=r"""Say explicitly "populate is a second query, not a join" — it's the one sentence that shows you understand its performance profile.""",
        tip_bn=r"""স্পষ্ট করে বলো "populate হলো দ্বিতীয় একটা query, join না" — এই এক বাক্যেই বোঝা যায় তুমি এর performance-এর ধরন বোঝো।""",
        mist_en=r"""Thinking populate performs a server-side JOIN; populating full user documents (including sensitive fields); forgetting that deleted references populate as `null`.""",
        mist_bn=r"""ভাবা যে populate server-side JOIN করে; পুরো user document populate করা (sensitive field সহ); ভুলে যাওয়া যে delete হওয়া reference populate হলে `null` আসে।""",
        code=r"""
            import mongoose, { Schema } from "mongoose";

            const postSchema = new Schema({
              title: { type: String, required: true },
              body: String,
              author: { type: Schema.Types.ObjectId, ref: "User", required: true },
            }, { timestamps: true });
            const Post = mongoose.model("Post", postSchema);

            const posts = await Post.find()
              .sort({ createdAt: -1 })
              .limit(20)
              .populate("author", "name avatarUrl")   // 2 queries total: posts + users ($in)
              .lean();

            posts[0].author;   // { _id: ..., name: "Nusrat", avatarUrl: "..." }  (or null if deleted)
        """,
        lang="javascript",
        follow=[
            ("How would you populate the author of each comment inside a post?", "একটা post-এর ভেতরের প্রতিটি comment-এর author কীভাবে populate করবে?"),
            ("When would you embed an author snapshot instead of populating?", "কখন populate না করে author-এর একটা snapshot embed করবে?"),
        ],
        refs=[POPULATE, SCHEMATYPES],
    ),
    # ------------------------------------------------------------------ mongoose-007
    Q(
        id="mongoose-007", sub="Virtuals", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=1,
        tags=["virtuals", "tojson", "serialization"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""You define the virtual below and return the user from an Express route with `res.json(user)`. Why is `fullName` missing from the JSON response?""",
        q_bn=r"""নিচের virtual define করে Express route থেকে `res.json(user)` দিয়ে user return করছ। JSON response-এ `fullName` নেই কেন?""",
        code=r"""
            userSchema.virtual("fullName").get(function () {
              return `${this.firstName} ${this.lastName}`;
            });

            app.get("/me", async (req, res) => {
              const user = await User.findById(req.userId);
              res.json(user);
            });
        """,
        lang="javascript",
        options=[
            ("Virtuals aren't included in `toJSON()` / `toObject()` output by default — enable `toJSON: { virtuals: true }` on the schema",
             "Default-ভাবে `toJSON()` / `toObject()` output-এ virtual থাকে না — schema-তে `toJSON: { virtuals: true }` চালু করতে হবে"),
            ("Virtuals only work after the document has been saved at least once",
             "Document অন্তত একবার save হওয়ার পরেই virtual কাজ করে"),
            ("The getter must be an arrow function so it can access the document",
             "Document access করতে getter-কে arrow function হতে হবে"),
            ("Virtuals are stored in MongoDB, but `res.json()` strips fields not defined in the schema",
             "Virtual MongoDB-তে store হয়, কিন্তু `res.json()` schema-তে না থাকা field বাদ দিয়ে দেয়"),
        ],
        correct=0,
        a_en=r"""`res.json()` calls `JSON.stringify`, which calls the document's `toJSON()`. Mongoose does **not** include virtuals in `toJSON()`/`toObject()` unless you set `{ toJSON: { virtuals: true } }` (and `toObject` if needed) in the schema options.""",
        a_bn=r"""`res.json()` `JSON.stringify` call করে, যেটা document-এর `toJSON()` call করে। Schema option-এ `{ toJSON: { virtuals: true } }` (দরকার হলে `toObject`-ও) না দিলে Mongoose `toJSON()`/`toObject()`-এ virtual **রাখে না**।""",
        quick_en=r"""Virtuals are not included in `toJSON()`/`toObject()` output by default, and `res.json()` serialises the document through `toJSON()`. Set `toJSON: { virtuals: true }` in the schema options so `fullName` appears.""",
        quick_bn=r"""Default-ভাবে virtual `toJSON()`/`toObject()`-এর output-এ থাকে না, আর `res.json()` document-কে `toJSON()` দিয়েই serialise করে। `fullName` দেখাতে schema option-এ `toJSON: { virtuals: true }` দাও।""",
        ex_en=r"""
            Virtuals are computed properties — they're **never stored in MongoDB** (so D is wrong) and you can't query by them. Option C is backwards: arrow functions don't get their own `this`, so a getter written as an arrow function can't see the document at all.

            Two related gotchas:
            - With `virtuals: true`, the built-in `id` virtual (string version of `_id`) also appears in the output.
            - `.lean()` returns plain objects, so virtuals don't exist on them at all — either skip `lean()` for that query or compute the field yourself (or use a plugin such as `mongoose-lean-virtuals`).
        """,
        ex_bn=r"""
            Virtual হলো computed property — এগুলো **কখনো MongoDB-তে store হয় না** (তাই D ভুল), আর এগুলো দিয়ে query করা যায় না। Option C উল্টো: arrow function-এর নিজস্ব `this` থাকে না, তাই arrow function দিয়ে লেখা getter document-টাই দেখতে পায় না।

            সম্পর্কিত দুইটা gotcha:
            - `virtuals: true` দিলে built-in `id` virtual-ও (`_id`-এর string রূপ) output-এ চলে আসে।
            - `.lean()` plain object return করে, তাই সেগুলোতে virtual থাকেই না — হয় ওই query-তে `lean()` বাদ দাও, নয়তো field-টা নিজে হিসাব করো (অথবা `mongoose-lean-virtuals`-এর মতো plugin ব্যবহার করো)।
        """,
        tip_en=r"""Explain the chain `res.json → JSON.stringify → doc.toJSON()` — understanding *why* it's missing is more impressive than knowing the flag.""",
        tip_bn=r"""`res.json → JSON.stringify → doc.toJSON()` — এই chain-টা ব্যাখ্যা করো। শুধু flag-টা জানার চেয়ে *কেন* field-টা নেই তা বোঝা বেশি impressive।""",
        follow=[
            ("Why don't virtuals appear on documents returned by `.lean()`?", "`.lean()`-এর document-এ virtual কেন থাকে না?"),
        ],
        related=["mongoose-002"],
        refs=[VIRTUALS, GUIDE],
    ),
    # ------------------------------------------------------------------ mongoose-013
    Q(
        id="mongoose-013", sub="Middleware & Hooks", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["middleware", "pre-save", "bcrypt", "mongoose-9", "next", "ismodified"],
        ver="Mongoose 9.11 (pre hooks receive no next() since 9.0)", vs=True, status="stable",
        q_en=r"""This password-hashing hook comes from an older project that was just upgraded to Mongoose 9. Saving a user now throws, and even before the upgrade some users couldn't log in after editing their profile. Find all the problems and fix the hook.""",
        q_bn=r"""এই password-hashing hook একটা পুরনো project থেকে এসেছে, যেটা সদ্য Mongoose 9-এ upgrade করা হয়েছে। এখন user save করলেই error throw হয়, আর upgrade-এর আগেও কিছু user profile edit করার পর login করতে পারত না। সব সমস্যা খুঁজে বের করো আর hook-টা ঠিক করো।""",
        code=r"""
            import bcrypt from "bcrypt";

            userSchema.pre("save", (next) => {
              this.password = bcrypt.hashSync(this.password, 10);
              next();
            });
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Fixed (Mongoose 9: async hook, no next)", label_bn="সংশোধিত (Mongoose 9: async hook, next ছাড়া)", src=r"""
                import bcrypt from "bcrypt";

                userSchema.pre("save", async function () {
                  if (!this.isModified("password")) return;      // only when it actually changed
                  this.password = await bcrypt.hash(this.password, 12);
                });
            """),
            dict(lang="javascript", label_en="Legacy (Mongoose 8 and earlier) — callback style, not supported in Mongoose 9", label_bn="Legacy (Mongoose 8 ও তার আগের) — callback style, Mongoose 9-এ support নেই", src=r"""
                userSchema.pre("save", function (next) {
                  if (!this.isModified("password")) return next();
                  bcrypt.hash(this.password, 12)
                    .then((hash) => { this.password = hash; next(); })
                    .catch(next);
                });
            """),
        ],
        a_en=r"""
            1. **Arrow function:** an arrow function doesn't get its own `this`, so `this` is not the document (in an ES module it's `undefined`) → `TypeError`. Document middleware must be a regular `function`.
            2. **`next()` in Mongoose 9:** pre middleware no longer receives `next`. Calling it throws a `TypeError`. Use an `async function` (or return a promise); to fail the save, just `throw`.
            3. **Re-hashing on every save:** without `if (!this.isModified("password")) return;`, editing a user's name re-hashes the *already hashed* password, so the real password no longer matches — that's the "can't log in after editing the profile" bug.
            4. **`hashSync` blocks the event loop:** bcrypt is deliberately slow (tens of milliseconds or more per hash); doing it synchronously stalls every other request. Use the async `bcrypt.hash`.
        """,
        a_bn=r"""
            1. **Arrow function:** arrow function-এর নিজস্ব `this` থাকে না, তাই `this` document না (ES module-এ এটা `undefined`) → `TypeError`। Document middleware অবশ্যই সাধারণ `function` হতে হবে।
            2. **Mongoose 9-এ `next()`:** pre middleware আর `next` পায় না। এটা call করলে `TypeError` throw হয়। `async function` ব্যবহার করো (বা promise return করো); save fail করাতে চাইলে শুধু `throw` করো।
            3. **প্রতিবার save-এ আবার hash:** `if (!this.isModified("password")) return;` না থাকলে user-এর নাম edit করলেও *আগে থেকে hash করা* password আবার hash হয়, ফলে আসল password আর মেলে না — এটাই "profile edit করার পর login করা যায় না" bug।
            4. **`hashSync` event loop block করে:** bcrypt ইচ্ছাকৃতভাবে ধীর (প্রতিটি hash-এ কয়েক দশ millisecond বা তার বেশি); synchronously করলে বাকি সব request আটকে যায়। Async `bcrypt.hash` ব্যবহার করো।
        """,
        quick_en=r"""Three bugs: the arrow function has no document `this`, Mongoose 9 pre hooks no longer receive `next`, and with no `isModified("password")` check every save re-hashes the hash. Use an `async function` that returns early if the password is unchanged and awaits `bcrypt.hash` instead of the blocking `hashSync`.""",
        quick_bn=r"""তিনটা bug: arrow function-এ `this` document না, Mongoose 9-এর pre hook আর `next` পায় না, আর `isModified("password")` check না থাকায় প্রতিটি save-এ আগের hash-কেই আবার hash করা হয়। একটা `async function` লেখো, password না বদলালে আগেই return করো, আর blocking `hashSync`-এর বদলে `await bcrypt.hash` ব্যবহার করো।""",
        ex_en=r"""
            - **This hook only covers `save()`** (and `create()`, which calls `save()`). A password reset done with `findOneAndUpdate`/`updateOne` bypasses it and stores plain text — route password changes through `save()`, or hash in the service layer.
            - **Error handling:** in an async pre hook, a thrown error or rejected promise aborts the save and rejects `doc.save()` — no `next(err)` needed.
            - **Storage hygiene:** store the hash in a field like `passwordHash` with `select: false`, and never return it from the API.
            - **Migration tip:** search the codebase for `pre(` hooks that take a parameter or call `next` — they all need converting when moving to Mongoose 9.
        """,
        ex_bn=r"""
            - **এই hook শুধু `save()` cover করে** (আর `create()`, কারণ সেটা `save()` call করে)। `findOneAndUpdate`/`updateOne` দিয়ে password reset করলে hook bypass হয়ে plain text store হয় — password পরিবর্তন `save()` দিয়ে করো, অথবা service layer-এ hash করো।
            - **Error handling:** async pre hook-এ error throw হলে বা promise reject হলে save abort হয় আর `doc.save()` reject করে — `next(err)` লাগে না।
            - **Storage-এর নিয়ম:** hash রাখো `passwordHash`-এর মতো field-এ, `select: false` সহ, আর API থেকে কখনো return কোরো না।
            - **Migration tip:** codebase-এ সেই সব `pre(` hook খোঁজো যেগুলো parameter নেয় বা `next` call করে — Mongoose 9-এ যাওয়ার সময় সবগুলো বদলাতে হবে।
        """,
        tip_en=r"""Separate the version-specific bug (`next` removed in v9) from the timeless bugs (arrow function, missing `isModified`, sync hashing). Interviewers like hearing that you'd grep for every legacy hook during an upgrade.""",
        tip_bn=r"""Version-specific bug (v9-এ `next` সরানো) আর চিরকালীন bug (arrow function, `isModified` না থাকা, sync hashing) আলাদা করে বলো। Upgrade-এর সময় সব legacy hook grep করে খুঁজবে — এটা শুনতে interviewer পছন্দ করে।""",
        mist_en=r"""Keeping `next` "just in case"; using arrow functions for hooks, methods or virtual getters; assuming `pre('save')` also runs on `findByIdAndUpdate`.""",
        mist_bn=r""""যদি লাগে" ভেবে `next` রেখে দেওয়া; hook, method বা virtual getter-এ arrow function ব্যবহার করা; ধরে নেওয়া `pre('save')` `findByIdAndUpdate`-এও চলে।""",
        follow=[
            ("How would you make sure a password reset via `findOneAndUpdate` is also hashed?", "`findOneAndUpdate` দিয়ে password reset করলে সেটাও যেন hash হয়, কীভাবে নিশ্চিত করবে?"),
            ("What does `this` refer to in `pre('findOneAndUpdate')` middleware?", "`pre('findOneAndUpdate')` middleware-এ `this` কী বোঝায়?"),
        ],
        refs=[MIDDLEWARE, MIGRATE9],
    ),
    # ------------------------------------------------------------------ mongoose-014
    Q(
        id="mongoose-014", sub="Middleware & Hooks", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["middleware", "pre-save", "query-middleware", "findbyidandupdate"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""`userSchema.pre("save", ...)` hashes passwords. Which of these calls will **not** run that hook — and therefore store the new password in plain text?""",
        q_bn=r"""`userSchema.pre("save", ...)` password hash করে। নিচের কোন call ওই hook **চালাবে না** — ফলে নতুন password plain text হিসেবে store হবে?""",
        options=[
            ("`await User.create({ email, password })`", "`await User.create({ email, password })`"),
            ("`const u = new User({ email, password }); await u.save();`", "`const u = new User({ email, password }); await u.save();`"),
            ("`await User.findByIdAndUpdate(id, { password: newPassword })`", "`await User.findByIdAndUpdate(id, { password: newPassword })`"),
            ("`const u = await User.findById(id); u.password = newPassword; await u.save();`", "`const u = await User.findById(id); u.password = newPassword; await u.save();`"),
        ],
        correct=2,
        a_en=r"""`findByIdAndUpdate()` sends an update command directly to MongoDB. It triggers **query middleware** (`findOneAndUpdate`), not document `save` middleware, so the hash hook never runs. `create()` calls `save()` internally, and the other two options call `save()` explicitly.""",
        a_bn=r"""`findByIdAndUpdate()` সরাসরি MongoDB-তে একটা update command পাঠায়। এটা **query middleware** (`findOneAndUpdate`) চালায়, document-এর `save` middleware না — তাই hash hook কখনো চলে না। `create()` ভেতরে `save()` call করে, আর বাকি দুইটা option explicitly `save()` call করে।""",
        quick_en=r"""`User.findByIdAndUpdate(id, { password })` doesn't run the hook: it sends an update straight to MongoDB and triggers query middleware (`findOneAndUpdate`), not `save` middleware. `create()` and the other two options all call `save()`.""",
        quick_bn=r"""`User.findByIdAndUpdate(id, { password })` hook চালায় না: এটা সরাসরি MongoDB-তে update পাঠায় আর query middleware (`findOneAndUpdate`) trigger করে, `save` middleware না। `create()` আর বাকি দুইটা option সবাই `save()` call করে।""",
        ex_en=r"""
            The tempting wrong answer is A — many developers don't realise `create()` is just a convenience wrapper around `new Model(doc).save()`, so it *does* run save hooks.

            In query middleware, `this` is the **Query**, not a document, so you'd have to read and rewrite the update (`this.getUpdate()` / `this.setUpdate()`) to hash there. The cleaner fix is a rule: password changes always go through load → set → `save()` (or a dedicated service function). Also note `insertMany()` triggers `insertMany` middleware, not `save` hooks.
        """,
        ex_bn=r"""
            সবচেয়ে বিভ্রান্তিকর ভুল উত্তর A — অনেক developer জানে না যে `create()` আসলে `new Model(doc).save()`-এর একটা সুবিধাজনক wrapper, তাই এটা save hook *চালায়*।

            Query middleware-এ `this` হলো **Query**, document না — তাই সেখানে hash করতে হলে update পড়ে আবার লিখতে হয় (`this.getUpdate()` / `this.setUpdate()`)। পরিষ্কার সমাধান হলো একটা নিয়ম: password পরিবর্তন সবসময় load → set → `save()` দিয়ে (বা একটা dedicated service function দিয়ে) হবে। আরও মনে রেখো, `insertMany()` `insertMany` middleware চালায়, `save` hook না।
        """,
        tip_en=r"""Name the two middleware families (document vs query) and what `this` is in each — that's the mental model behind every "why didn't my hook run?" bug.""",
        tip_bn=r"""দুই ধরনের middleware (document বনাম query) আর প্রতিটিতে `this` কী — সেটা বলো। "আমার hook কেন চলল না?" ধরনের প্রতিটি bug-এর পেছনে এই mental model-টাই কাজ করে।""",
        follow=[
            ("How would you implement an audit log that records every update, including `updateMany`?", "`updateMany` সহ প্রতিটি update record করে এমন audit log কীভাবে implement করবে?"),
        ],
        related=["mongoose-013", "mongoose-004"],
        refs=[MIDDLEWARE],
    ),
    # ------------------------------------------------------------------ mongoose-015
    Q(
        id="mongoose-015", sub="References & Populate", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["populate", "lookup", "n-plus-one", "aggregation", "performance"],
        ver="Mongoose 9.11, MongoDB 9.0", vs=False, status="stable",
        q_en=r"""Compare Mongoose `populate()` with an aggregation `$lookup`. What is the N+1 problem here, and when would you use each approach?""",
        q_bn=r"""Mongoose-এর `populate()` আর aggregation `$lookup`-এর তুলনা করো। এখানে N+1 সমস্যা কী, আর কখন কোন পদ্ধতি ব্যবহার করবে?""",
        a_en=r"""
            **N+1:** load 20 posts, then call `User.findById()` for each author in a loop → 1 + 20 queries. `populate()` fixes this by batching: one query for posts plus **one `$in` query per populated path** — 2 queries total.

            **`populate()`** is an application-side join:
            - Pros: very convenient, returns Mongoose documents (or works with `lean()`), applies schema casting, `select` limits fields, nested populate is easy.
            - Cons: an extra round trip per path (more for nested populate); you can't filter, sort or paginate the parents by populated fields — `match` in populate only nulls out non-matching children, it doesn't remove the parent.

            **`$lookup`** is a server-side join inside an aggregation pipeline:
            - Pros: one round trip; you can `$match`, `$sort`, `$group` on joined fields.
            - Cons: returns plain objects, no casting (you must convert string IDs to `ObjectId` yourself), no virtuals/getters/document middleware, more verbose.

            **My rule:** populate for normal CRUD pages ("post with its author"); `$lookup` for reports and for filtering or sorting by related data ("posts by verified authors, newest first"); and denormalise a small snapshot when a field is needed on every read.
        """,
        a_bn=r"""
            **N+1:** 20টা post load করে loop-এ প্রতিটি author-এর জন্য `User.findById()` call করা → 1 + 20টা query। `populate()` এটা batch করে ঠিক করে: post-এর জন্য একটা query আর **প্রতিটি populated path-এর জন্য একটা `$in` query** — মোট 2টা query।

            **`populate()`** হলো application-side join:
            - সুবিধা: খুব সুবিধাজনক, Mongoose document return করে (বা `lean()`-এর সাথে কাজ করে), schema casting apply হয়, `select` দিয়ে field সীমিত করা যায়, nested populate সহজ।
            - অসুবিধা: প্রতিটি path-এ একটা বাড়তি round trip (nested populate-এ আরও বেশি); populated field দিয়ে parent-কে filter, sort বা paginate করা যায় না — populate-এর `match` শুধু না-মেলা child-কে null করে, parent বাদ দেয় না।

            **`$lookup`** হলো aggregation pipeline-এর ভেতরে server-side join:
            - সুবিধা: একটাই round trip; join করা field-এ `$match`, `$sort`, `$group` করা যায়।
            - অসুবিধা: plain object return করে, casting নেই (string ID নিজেকেই `ObjectId`-এ রূপান্তর করতে হয়), virtual/getter/document middleware নেই, code বেশি লম্বা।

            **আমার নিয়ম:** সাধারণ CRUD page-এ ("author সহ post") populate; report আর related data দিয়ে filter বা sort করতে ("verified author-দের post, নতুনগুলো আগে") `$lookup`; আর কোনো field প্রতিটি read-এ লাগলে ছোট একটা snapshot denormalise করা।
        """,
        quick_en=r"""N+1 is one query for the list plus one per item; `populate()` batches it into one extra `$in` query per path, but can't filter or sort parents by populated fields. `$lookup` joins on the server and can `$match`/`$sort` on joined data: populate for CRUD pages, `$lookup` for reports.""",
        quick_bn=r"""N+1 মানে list-এর জন্য একটা query আর প্রতিটি item-এর জন্য আরেকটা; `populate()` প্রতি path-এ একটা অতিরিক্ত `$in` query দিয়ে এটা ঠিক করে, কিন্তু populated field দিয়ে parent filter বা sort করতে পারে না। `$lookup` server-এ join করে আর joined data-তে `$match`/`$sort` করা যায়: CRUD page-এ populate, report-এ `$lookup`।""",
        ex_en=r"""
            - **Aggregation casting gotcha:** `Post.aggregate([{ $match: { author: req.params.id } }])` matches nothing, because the string isn't cast to `ObjectId` in pipelines. Use `new mongoose.Types.ObjectId(id)`.
            - **Order of stages matters:** in the `$lookup` example, filtering on `author.verified` after the join means joining every post first. On a big collection, denormalise `authorVerified` onto posts or `$match` on post fields before the join.
            - **Populate performance:** keep `select` tight, avoid populating unbounded arrays, and use `perDocumentLimit` (not `limit`) when you want "N children per parent".
            - **Measure:** enable `mongoose.set("debug", true)` in development to see every query a request triggers — N+1 problems become obvious.
        """,
        ex_bn=r"""
            - **Aggregation casting-এর gotcha:** `Post.aggregate([{ $match: { author: req.params.id } }])` কিছুই match করে না, কারণ pipeline-এ string `ObjectId`-এ cast হয় না। `new mongoose.Types.ObjectId(id)` ব্যবহার করো।
            - **Stage-এর ক্রম গুরুত্বপূর্ণ:** `$lookup` উদাহরণে join-এর পরে `author.verified` দিয়ে filter করা মানে আগে প্রতিটি post join করা। বড় collection-এ post-এ `authorVerified` denormalise করো, অথবা join-এর আগে post-এর field দিয়ে `$match` করো।
            - **Populate performance:** `select` সংক্ষিপ্ত রাখো, unbounded array populate এড়াও, আর "প্রতি parent-এ Nটা child" চাইলে `limit` না, `perDocumentLimit` ব্যবহার করো।
            - **মেপে দেখো:** development-এ `mongoose.set("debug", true)` চালু করলে একটা request কতগুলো query চালায় সব দেখা যায় — N+1 সমস্যা সাথে সাথে চোখে পড়ে।
        """,
        tip_en=r"""Give your decision rule in one line at the end — interviewers want to hear judgement ("it depends on whether I filter by the related data"), not just two feature lists.""",
        tip_bn=r"""শেষে এক লাইনে তোমার সিদ্ধান্তের নিয়মটা বলো — interviewer শুধু দুইটা feature-এর তালিকা না, বিচারবুদ্ধি শুনতে চায় ("related data দিয়ে filter করব কি না তার ওপর নির্ভর করে")।""",
        mist_en=r"""Believing `populate()` is a JOIN; using populate's `match` expecting parents to be filtered; passing string IDs into aggregation `$match`.""",
        mist_bn=r"""`populate()`-কে JOIN মনে করা; parent filter হবে ভেবে populate-এর `match` ব্যবহার করা; aggregation-এর `$match`-এ string ID দেওয়া।""",
        code=r"""
            // N+1 — avoid: 1 query for posts + 1 per post
            const slow = await Post.find().sort({ createdAt: -1 }).limit(20).lean();
            for (const p of slow) p.author = await User.findById(p.author).select("name").lean();

            // populate — 2 queries in total (posts + one $in query for authors)
            const populated = await Post.find().sort({ createdAt: -1 }).limit(20)
              .populate("author", "name avatarUrl")
              .lean();

            // $lookup — filter on joined data inside MongoDB (plain objects, no casting)
            const verifiedOnly = await Post.aggregate([
              { $sort: { createdAt: -1 } },
              { $lookup: {
                  from: "users", localField: "author", foreignField: "_id",
                  pipeline: [{ $project: { name: 1, avatarUrl: 1, verified: 1 } }],
                  as: "author"
              } },
              { $unwind: "$author" },
              { $match: { "author.verified": true } },
              { $limit: 20 },
            ]);
        """,
        lang="javascript",
        follow=[
            ("How would you get each user's latest 3 posts efficiently?", "প্রতিটি user-এর সর্বশেষ 3টা post দক্ষভাবে কীভাবে আনবে?"),
            ("How do you spot N+1 queries in an existing Express + Mongoose app?", "একটা existing Express + Mongoose app-এ N+1 query কীভাবে ধরবে?"),
        ],
        related=["mongoose-006"],
        refs=[POPULATE, AGGREGATE_API, LOOKUP],
    ),
    # ------------------------------------------------------------------ mongoose-024
    Q(
        id="mongoose-024", sub="Query Performance", diff="hard", type="security-performance",
        prio="high", market="both", mins=12,
        tags=["performance", "lean", "pagination", "indexes", "populate", "validation"],
        ver="Mongoose 9.11, Express 5, zod 4", vs=False, status="stable",
        q_en=r"""
            `GET /api/products?category=electronics&page=500` takes 3–4 seconds and the Node.js process uses a lot of memory. On every request the handler does:

            - `const page = Number(req.query.page) || 1;`
            - `Product.find({ category: req.query.category }).populate("seller").populate("reviews").sort({ createdAt: -1 }).skip((page - 1) * 20).limit(20)`
            - `Product.countDocuments({ category: req.query.category })` for the total

            How would you make it fast and safe?
        """,
        q_bn=r"""
            `GET /api/products?category=electronics&page=500`-এ 3–4 second লাগে, আর Node.js process অনেক memory ব্যবহার করে। প্রতিটি request-এ handler এগুলো করে:

            - `const page = Number(req.query.page) || 1;`
            - `Product.find({ category: req.query.category }).populate("seller").populate("reviews").sort({ createdAt: -1 }).skip((page - 1) * 20).limit(20)`
            - total-এর জন্য `Product.countDocuments({ category: req.query.category })`

            এটাকে দ্রুত আর নিরাপদ কীভাবে করবে?
        """,
        code=r"""
            app.get("/api/products", async (req, res) => {
              const page = Number(req.query.page) || 1;
              const products = await Product.find({ category: req.query.category })
                .populate("seller")
                .populate("reviews")
                .sort({ createdAt: -1 })
                .skip((page - 1) * 20)
                .limit(20);
              const total = await Product.countDocuments({ category: req.query.category });
              res.json({ products, total });
            });
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Optimised handler (keyset pagination)", label_bn="Optimise করা handler (keyset pagination)", src=r"""
            import { z } from "zod";

            productSchema.index({ category: 1, createdAt: -1, _id: -1 });

            const ListQuery = z.object({
              category: z.enum(["electronics", "fashion", "grocery"]),
              cursor: z.string().regex(/^\d{4}-\d{2}-\d{2}T[\d:.]+Z_[a-f0-9]{24}$/).optional(),
              limit: z.coerce.number().int().min(1).max(50).default(20),
            });

            app.get("/api/products", async (req, res) => {
              const { category, cursor, limit } = ListQuery.parse(req.query);   // ZodError → 400

              const filter = { category };
              if (cursor) {
                const [iso, id] = cursor.split("_");
                const createdAt = new Date(iso);
                filter.$or = [
                  { createdAt: { $lt: createdAt } },
                  { createdAt, _id: { $lt: id } },          // tie-breaker for equal timestamps
                ];
              }

              const rows = await Product.find(filter)
                .select("name slug price thumbnail avgRating reviewCount seller createdAt")
                .populate("seller", "shopName rating")
                .sort({ createdAt: -1, _id: -1 })
                .limit(limit + 1)
                .lean();

              const hasMore = rows.length > limit;
              const items = rows.slice(0, limit);
              const last = items.at(-1);
              res.json({
                items,
                nextCursor: hasMore ? `${last.createdAt.toISOString()}_${last._id}` : null,
              });
            });
        """)],
        a_en=r"""
            **Performance problems:**
            1. **No suitable index** for "filter by category, sort by newest" → collection scan plus an in-memory sort. Add `{ category: 1, createdAt: -1, _id: -1 }` (equality → sort).
            2. **Deep `skip()`**: page 500 makes MongoDB walk and discard 9,980 entries before returning 20. Use **keyset (cursor) pagination**: "items older than the last one I saw", with `_id` as a tie-breaker.
            3. **Hydrated documents:** each result becomes a full Mongoose document with change tracking. For read-only lists, `.lean()` returns plain objects — much less memory and CPU.
            4. **Over-fetching:** no projection, the whole `seller` document, and **all reviews** of every product (an unbounded array of refs). Select only list fields, populate the seller with a few fields, and show computed `reviewCount`/`avgRating` instead of reviews.
            5. **`countDocuments` on every request** for a large category is expensive — drop the exact total (infinite scroll), cache it briefly, or show "1,000+".

            **Security problems:** `req.query.category` is used unvalidated — if a nested query parser is enabled it could be an object (`category[$ne]=x` → operator injection), and `page`/`limit` are unbounded, so a client can request huge pages. Validate with a schema (enum category, bounded limit).
        """,
        a_bn=r"""
            **Performance-এর সমস্যা:**
            1. "category দিয়ে filter, নতুন অনুযায়ী sort"-এর জন্য **উপযুক্ত index নেই** → collection scan আর in-memory sort। `{ category: 1, createdAt: -1, _id: -1 }` যোগ করো (equality → sort)।
            2. **গভীর `skip()`:** page 500-এ 20টা return করার আগে MongoDB-কে 9,980টা entry পার হয়ে ফেলে দিতে হয়। **Keyset (cursor) pagination** ব্যবহার করো: "শেষ যেটা দেখেছি তার চেয়ে পুরনো item", tie-breaker হিসেবে `_id` সহ।
            3. **Hydrated document:** প্রতিটি result change tracking সহ পূর্ণ Mongoose document হয়। Read-only list-এর জন্য `.lean()` plain object দেয় — অনেক কম memory আর CPU।
            4. **প্রয়োজনের বেশি data আনা:** কোনো projection নেই, পুরো `seller` document, আর প্রতিটি product-এর **সব review** (ref-এর unbounded array)। শুধু list-এর field select করো, seller-কে কয়েকটা field সহ populate করো, আর review-এর বদলে computed `reviewCount`/`avgRating` দেখাও।
            5. বড় category-তে **প্রতিটি request-এ `countDocuments`** ব্যয়বহুল — exact total বাদ দাও (infinite scroll), অল্প সময়ের জন্য cache করো, অথবা "1,000+" দেখাও।

            **Security-র সমস্যা:** `req.query.category` validation ছাড়াই ব্যবহার হচ্ছে — nested query parser চালু থাকলে এটা object হতে পারে (`category[$ne]=x` → operator injection), আর `page`/`limit`-এর কোনো সীমা নেই, তাই client বিশাল page চাইতে পারে। Schema দিয়ে validate করো (enum category, সীমিত limit)।
        """,
        quick_en=r"""Add a `{ category: 1, createdAt: -1, _id: -1 }` index, replace deep `skip()` with keyset pagination, use `.lean()` with projections, populate only a few seller fields instead of all reviews, and cache or drop the exact count. Also validate `category` and bound `page`/`limit` to block operator injection and huge pages.""",
        quick_bn=r"""`{ category: 1, createdAt: -1, _id: -1 }` index দাও, গভীর `skip()`-এর বদলে keyset pagination করো, projection সহ `.lean()` ব্যবহার করো, সব review না এনে seller-এর অল্প কয়েকটা field populate করো, আর exact count cache করো বা বাদ দাও। সাথে `category` validate করো আর `page`/`limit` সীমিত রাখো, যাতে operator injection আর বিশাল page আটকানো যায়।""",
        ex_en=r"""
            - **Why keyset works:** with the index, MongoDB seeks directly to the cursor position and reads exactly `limit + 1` keys, so page 500 costs the same as page 1. The trade-off: no "jump to page 37" — fine for feeds and infinite scroll, while admin tables with page numbers can keep `skip` for shallow pages.
            - **Mongoose casting:** the `_id: { $lt: id }` string is cast to `ObjectId` by Mongoose because `_id` is in the schema — this does *not* happen inside `aggregate()`.
            - **`lean()` caveats:** no virtuals, getters, defaults applied on read, or `save()`; `_id` values are still `ObjectId` instances (they serialise to strings in JSON).
            - **Verify:** `Product.find(filter).sort(...).explain("executionStats")` — expect `IXSCAN`, no `SORT` stage, keys examined ≈ `limit + 1`.
            - **Bigger lists or exports:** stream with `Product.find().lean().cursor()` instead of loading everything into memory.
        """,
        ex_bn=r"""
            - **Keyset কেন কাজ করে:** index থাকায় MongoDB সরাসরি cursor-এর অবস্থানে চলে যায় আর ঠিক `limit + 1`টা key পড়ে, তাই page 500-এর খরচ page 1-এর সমান। Trade-off: "page 37-এ লাফ দাও" করা যায় না — feed আর infinite scroll-এর জন্য ঠিক আছে, আর page number-ওয়ালা admin table অগভীর page-এর জন্য `skip` রাখতে পারে।
            - **Mongoose casting:** `_id` schema-তে আছে বলে `_id: { $lt: id }`-এর string Mongoose `ObjectId`-এ cast করে — `aggregate()`-এর ভেতরে এটা হয় *না*।
            - **`lean()`-এর সতর্কতা:** read-এ virtual, getter, default apply হয় না, `save()` নেই; `_id` value তখনও `ObjectId` instance (JSON-এ string হয়ে যায়)।
            - **Verify করো:** `Product.find(filter).sort(...).explain("executionStats")` — `IXSCAN` আশা করো, কোনো `SORT` stage না, আর keys examined ≈ `limit + 1`।
            - **বড় list বা export:** সব memory-তে load না করে `Product.find().lean().cursor()` দিয়ে stream করো।
        """,
        tip_en=r"""Rank the fixes by impact (index → pagination → lean/projection → populate → count) and add the validation point at the end. Treating performance and security together is what this question type rewards.""",
        tip_bn=r"""প্রভাব অনুযায়ী fix-গুলো সাজাও (index → pagination → lean/projection → populate → count), আর শেষে validation-এর কথা যোগ করো। এই ধরনের প্রশ্নে performance আর security একসাথে ভাবাকেই পুরস্কৃত করা হয়।""",
        mist_en=r"""Adding `.lean()` and calling it done; adding an index on `category` alone (still sorts in memory); trusting `req.query` values as filter objects.""",
        mist_bn=r"""শুধু `.lean()` যোগ করে কাজ শেষ মনে করা; শুধু `category`-তে index দেওয়া (তবুও memory-তে sort হয়); `req.query`-র value-কে filter object হিসেবে বিশ্বাস করা।""",
        follow=[
            ("How would you support 'sort by price' as well as 'newest first' with keyset pagination?", "Keyset pagination দিয়ে 'newest first'-এর পাশাপাশি 'price অনুযায়ী sort' কীভাবে support করবে?"),
            ("When is `skip()` still acceptable?", "কখন `skip()` এখনো গ্রহণযোগ্য?"),
        ],
        related=["mongoose-015", "mongoose-006"],
        refs=[LEAN, QUERIES, ESR],
    ),
    # ------------------------------------------------------------------ mongoose-025
    Q(
        id="mongoose-025", sub="Common Pitfalls", diff="hard", type="mcq",
        prio="medium", market="international", mins=2,
        tags=["versioning", "optimistic-concurrency", "versionkey", "lost-update", "save"],
        ver="Mongoose 9.11", vs=False, status="stable",
        q_en=r"""Two admins open the same product (price 1,200) at the same time. Admin A sets the price to 1,500 and calls `save()`. A second later, Admin B — still looking at 1,200 — sets it to 1,250 and calls `save()`. The schema uses Mongoose's default options. What happens?""",
        q_bn=r"""দুইজন admin একই সময়ে একই product খুলেছে (price 1,200)। Admin A price 1,500 করে `save()` call করল। এক second পরে Admin B — যে এখনো 1,200 দেখছে — price 1,250 করে `save()` call করল। Schema-তে Mongoose-এর default option। কী হবে?""",
        options=[
            (r"""Mongoose merges both changes and keeps 1,500 because it was saved first""",
             r"""Mongoose দুইটা পরিবর্তন merge করে 1,500 রাখে, কারণ সেটা আগে save হয়েছে"""),
            (r"""B's save throws a `VersionError`, because `__v` is checked on every `save()` by default""",
             r"""B-এর save একটা `VersionError` throw করে, কারণ default-ভাবে প্রতিটি `save()`-এ `__v` check হয়"""),
            (r"""Both saves succeed and the final price is 1,250 — A's change is silently lost, because default versioning only guards certain array changes""",
             r"""দুইটা save-ই সফল হয় আর শেষ price হয় 1,250 — A-এর পরিবর্তন চুপচাপ হারিয়ে যায়, কারণ default versioning শুধু কিছু array পরিবর্তন রক্ষা করে"""),
            (r"""B's `findById` blocked until A saved, because Mongoose locks documents while they are loaded""",
             r"""A save না করা পর্যন্ত B-এর `findById` আটকে ছিল, কারণ load থাকা অবস্থায় Mongoose document lock করে"""),
        ],
        correct=2,
        a_en=r"""By default Mongoose's `__v` versioning only protects **array** operations that could shift element positions. A plain field change is saved as `$set: { price }` filtered by `_id` only, so the last `save()` wins and A's update is lost without any error.""",
        a_bn=r"""Default-ভাবে Mongoose-এর `__v` versioning শুধু সেই **array** operation রক্ষা করে, যেগুলো element-এর অবস্থান সরিয়ে দিতে পারে। সাধারণ field-এর পরিবর্তন শুধু `_id` filter দিয়ে `$set: { price }` হিসেবে save হয়, তাই শেষ `save()`-টাই জেতে আর কোনো error ছাড়াই A-এর update হারিয়ে যায়।""",
        quick_en=r"""Both saves succeed and the final price is 1,250, so A's change is silently lost. Default `__v` versioning only guards certain array changes; a plain field update is sent as `$set` filtered by `_id` only, so the last save wins.""",
        quick_bn=r"""দুইটা save-ই সফল হয় আর শেষ price হয় 1,250, তাই A-র পরিবর্তন চুপচাপ হারিয়ে যায়। Default `__v` versioning শুধু কিছু array পরিবর্তন রক্ষা করে; সাধারণ field update শুধু `_id` filter দিয়ে `$set` হিসেবে যায়, তাই শেষ save-ই জেতে।""",
        ex_en=r"""
            Option B is what many people assume because they see `__v` on every document. It becomes true only if you enable **`optimisticConcurrency: true`** on the schema: then every `save()` includes the current `__v` in its filter and increments it, so B's stale save matches nothing and throws a `VersionError` — your API can return 409 and ask B to reload.

            Notes: `updateOne()`/`findOneAndUpdate()` never use or bump `__v`, so optimistic concurrency only protects `save()`-based flows. For counters like stock, atomic operators (`$inc` with a conditional filter) are better than version checks. MongoDB doesn't lock documents between a read and a later write (option D).
        """,
        ex_bn=r"""
            Option B অনেকেই ধরে নেয়, কারণ প্রতিটি document-এ `__v` দেখা যায়। এটা সত্য হয় শুধু schema-তে **`optimisticConcurrency: true`** চালু করলে: তখন প্রতিটি `save()` filter-এ বর্তমান `__v` রাখে আর সেটা বাড়ায়, ফলে B-এর পুরনো save কিছুই match করে না আর `VersionError` throw করে — তোমার API তখন 409 return করে B-কে reload করতে বলতে পারে।

            খেয়াল রাখো: `updateOne()`/`findOneAndUpdate()` কখনো `__v` ব্যবহার করে না বা বাড়ায় না, তাই optimistic concurrency শুধু `save()`-ভিত্তিক flow রক্ষা করে। Stock-এর মতো counter-এর জন্য version check-এর চেয়ে atomic operator (conditional filter সহ `$inc`) ভালো। আর MongoDB read আর পরের write-এর মাঝে document lock করে না (option D)।
        """,
        tip_en=r"""Name both mechanisms — optimistic concurrency for "edit forms" and atomic operators for "counters" — and when each fits. That distinction is a senior-level signal.""",
        tip_bn=r"""দুইটা পদ্ধতিরই নাম বলো — "edit form"-এর জন্য optimistic concurrency আর "counter"-এর জন্য atomic operator — আর কোনটা কখন মানানসই। এই পার্থক্যটা senior-level signal।""",
        follow=[
            ("How would you surface a `VersionError` to the user in a REST API?", "REST API-তে একটা `VersionError` user-কে কীভাবে জানাবে?"),
        ],
        related=["mongoose-004"],
        refs=[GUIDE, ATOMICITY],
    ),
    # ------------------------------------------------------------------ mongoose-031
    Q(
        id="mongoose-031", sub="Concurrency & Atomic Updates", diff="extreme", type="scenario",
        prio="high", market="both", mins=18,
        tags=["concurrency", "flash-sale", "overselling", "atomic-updates", "idempotency", "contention"],
        ver="Mongoose 9.11, MongoDB 9.0", vs=False, status="stable",
        q_en=r"""During a flash sale, about 5,000 users try to buy the last 100 units of a phone within a few seconds. The checkout does: `findById` → check `product.stock >= qty` → `product.stock -= qty` → `await product.save()` → create the order. Afterwards there are 340 orders for 100 units. Explain why, and design a correct and scalable solution with Mongoose.""",
        q_bn=r"""একটা flash sale-এ প্রায় 5,000 user কয়েক second-এর মধ্যে একটা phone-এর শেষ 100টা unit কিনতে চেষ্টা করে। Checkout-এর ধাপ: `findById` → `product.stock >= qty` check → `product.stock -= qty` → `await product.save()` → order তৈরি। শেষে দেখা গেল 100টা unit-এর জন্য 340টা order। কেন এমন হলো ব্যাখ্যা করো, আর Mongoose দিয়ে একটা সঠিক ও scalable সমাধান design করো।""",
        a_en=r"""
            *(Advanced: concurrency under contention.)*

            **Why:** it's a classic **read-modify-write race**. Hundreds of requests read `stock: 100` at nearly the same moment, all pass the check in Node.js, and each `save()` sends `$set: { stock: <its own computed value> }`. The writes overwrite each other (last write wins), so the counter never reflects all purchases. Mongoose's default `__v` versioning doesn't protect plain fields, so nothing fails.

            **Correctness — let the database decide:**
            1. **Atomic conditional decrement:** `Product.updateOne({ _id, stock: { $gte: qty } }, { $inc: { stock: -qty } })`. MongoDB applies writes to a single document atomically, so exactly 100 units can be sold; the rest get `modifiedCount: 0` → "sold out".
            2. **Order + stock together:** either a short transaction (decrement + create order), or decrement first and **compensate** (`$inc: +qty`) if order creation fails, with a reconciliation job for crashes in between.
            3. **Idempotency:** a unique `checkoutId` per attempt so client retries don't create extra orders, and a unique `{ saleId, userId }` index to enforce "one per customer".

            **Scale — one hot document:** 5,000 concurrent writes on one document serialise on the server; inside transactions they also cause `WriteConflict` retries that multiply load. Options:
            - Keep the hot path a **single-document atomic update without a transaction**, and do the rest asynchronously.
            - **Queue** purchase requests (e.g. Redis-backed queue) and process them at a controlled rate, or put a waiting room in front.
            - Pre-split stock into N buckets (`sku#1..N`) to spread contention, or gate with an atomic Redis `DECR` counter while MongoDB stays the source of truth.
            - Reserve with an expiry: unpaid orders release units after ~10 minutes via a worker.

            **Observe:** watch write-conflict counts, p99 latency and connection-pool saturation during the sale, and load-test the checkout before the campaign.
        """,
        a_bn=r"""
            *(Advanced: contention-এর মধ্যে concurrency।)*

            **কেন:** এটা classic **read-modify-write race**। শত শত request প্রায় একই মুহূর্তে `stock: 100` পড়ে, Node.js-এ সবাই check পার হয়ে যায়, আর প্রতিটি `save()` পাঠায় `$set: { stock: <নিজের হিসাব করা value> }`। Write-গুলো একে অপরকে overwrite করে (last write wins), তাই counter কখনো সব কেনাকাটা প্রতিফলিত করে না। Mongoose-এর default `__v` versioning সাধারণ field রক্ষা করে না, তাই কিছুই fail করে না।

            **সঠিকতা — সিদ্ধান্ত database-কে নিতে দাও:**
            1. **Atomic conditional decrement:** `Product.updateOne({ _id, stock: { $gte: qty } }, { $inc: { stock: -qty } })`। MongoDB একটা document-এ write atomically apply করে, তাই ঠিক 100টা unit-ই বিক্রি হতে পারে; বাকিরা `modifiedCount: 0` পায় → "sold out"।
            2. **Order আর stock একসাথে:** হয় একটা ছোট transaction (decrement + order তৈরি), নয়তো আগে decrement করে order তৈরি fail করলে **compensate** (`$inc: +qty`), আর মাঝখানে crash হলে একটা reconciliation job।
            3. **Idempotency:** প্রতিটি চেষ্টার জন্য unique `checkoutId`, যাতে client retry করলে বাড়তি order না হয়; আর "প্রতি customer একটা" enforce করতে unique `{ saleId, userId }` index।

            **Scale — একটা hot document:** একটা document-এ 5,000 concurrent write server-এ একটার পর একটা হয়; transaction-এর ভেতরে হলে `WriteConflict` retry-ও হয়, যা load বহুগুণ বাড়ায়। উপায়:
            - Hot path-কে **transaction ছাড়া single-document atomic update** রাখো, বাকিটা asynchronously করো।
            - Purchase request **queue** করো (যেমন Redis-backed queue) আর নিয়ন্ত্রিত হারে process করো, অথবা সামনে একটা waiting room রাখো।
            - Contention ছড়াতে stock আগে থেকেই Nটা bucket-এ ভাগ করো (`sku#1..N`), অথবা atomic Redis `DECR` counter দিয়ে gate করো, আর MongoDB-ই থাকুক source of truth।
            - Expiry সহ reserve করো: pay না করা order ~10 minute পর একটা worker দিয়ে unit ছেড়ে দেয়।

            **পর্যবেক্ষণ:** sale চলাকালীন write-conflict সংখ্যা, p99 latency আর connection-pool saturation দেখো, আর campaign-এর আগে checkout load-test করো।
        """,
        quick_en=r"""It's a read-modify-write race: hundreds of requests read `stock: 100`, all pass the check, and each `save()` overwrites the others. Let the database decide with an atomic `updateOne({ _id, stock: { $gte: qty } }, { $inc: { stock: -qty } })`, add idempotency keys, and queue or throttle requests for the hot document.""",
        quick_bn=r"""এটা read-modify-write race: শত শত request একসাথে `stock: 100` পড়ে, সবাই check পার হয়, আর প্রতিটি `save()` অন্যদের লেখা overwrite করে। সিদ্ধান্ত database-কে নিতে দাও atomic `updateOne({ _id, stock: { $gte: qty } }, { $inc: { stock: -qty } })` দিয়ে, idempotency key যোগ করো, আর hot document-এর জন্য request queue বা throttle করো।""",
        ex_en=r"""
            - **Why not `optimisticConcurrency` here?** It would turn lost updates into `VersionError`s, but under 5,000 concurrent buyers almost every save fails and retries — a retry storm. Version checks suit low-contention edit forms; hot counters need atomic operators.
            - **Transaction or compensation?** Transactions give clean atomicity and are fine at normal traffic. At flash-sale contention, a single-document conditional `$inc` plus compensation is cheaper; the price is a reconciliation job to repair rare crashes between the two steps.
            - **Fairness:** first-come-first-served at the database isn't the same as fair for users on slow mobile networks; a queue or lottery may be a product decision.
            - **Don't forget the read side:** product pages showing "only 3 left" should be cached and allowed to be slightly stale — they shouldn't hammer the same hot document.
            - **Payment timeouts:** with bKash/card redirects taking minutes, reserved-but-unpaid units must return to stock reliably, or the sale "sells out" with unpaid orders.
        """,
        ex_bn=r"""
            - **এখানে `optimisticConcurrency` কেন না?** এটা lost update-কে `VersionError`-এ পরিণত করত, কিন্তু 5,000 concurrent buyer-এর মধ্যে প্রায় প্রতিটি save fail করে retry করবে — একটা retry storm। Version check কম contention-এর edit form-এর জন্য মানানসই; hot counter-এর জন্য atomic operator লাগে।
            - **Transaction নাকি compensation?** Transaction পরিষ্কার atomicity দেয় আর স্বাভাবিক traffic-এ ঠিক আছে। Flash-sale-এর contention-এ single-document conditional `$inc` আর compensation সস্তা; বিনিময়ে দুই ধাপের মাঝে বিরল crash ঠিক করতে একটা reconciliation job লাগে।
            - **ন্যায্যতা:** database-এ first-come-first-served মানেই ধীর mobile network-এর user-দের জন্য ন্যায্য না; queue বা lottery একটা product সিদ্ধান্তও হতে পারে।
            - **Read দিকটাও ভুলো না:** "মাত্র 3টা বাকি" দেখানো product page cache করা উচিত এবং একটু পুরনো হলেও চলে — এগুলো যেন একই hot document-এ চাপ না দেয়।
            - **Payment timeout:** bKash/card redirect-এ কয়েক মিনিট লাগলে, reserve করা কিন্তু pay না করা unit নির্ভরযোগ্যভাবে stock-এ ফিরতে হবে, নইলে unpaid order দিয়েই sale "sold out" হয়ে যাবে।
        """,
        tip_en=r"""Separate correctness (atomic conditional update, idempotency) from scalability (contention, queueing). Explaining why `optimisticConcurrency` is the wrong tool here shows real depth.""",
        tip_bn=r"""Correctness (atomic conditional update, idempotency) আর scalability (contention, queueing) আলাদা করে বলো। এখানে `optimisticConcurrency` কেন ভুল tool — সেটা ব্যাখ্যা করতে পারলে আসল গভীরতা বোঝা যায়।""",
        mist_en=r"""Adding a mutex in Node.js (doesn't work across multiple instances); checking stock with `findOne` before `updateOne`; wrapping everything in a long transaction that calls the payment gateway.""",
        mist_bn=r"""Node.js-এ একটা mutex যোগ করা (একাধিক instance-এ কাজ করে না); `updateOne`-এর আগে `findOne` দিয়ে stock check করা; payment gateway call সহ সবকিছু একটা লম্বা transaction-এ মুড়ে দেওয়া।""",
        code=r"""
            // 1) Hot path: one atomic, conditional decrement (no read-modify-write)
            async function reserveUnits(productId, qty) {
              const res = await Product.updateOne(
                { _id: productId, stock: { $gte: qty } },
                { $inc: { stock: -qty } }
              );
              return res.modifiedCount === 1;          // false → sold out
            }

            // 2) Create the order; give the units back if that fails (incl. duplicate retries)
            async function checkout({ saleId, userId, productId, qty, checkoutId }) {
              if (!(await reserveUnits(productId, qty))) throw new SoldOutError(productId);
              try {
                return await Order.create({ saleId, checkoutId, userId, productId, qty, status: "awaiting_payment" });
              } catch (err) {
                await Product.updateOne({ _id: productId }, { $inc: { stock: qty } });   // compensate
                throw err;                              // E11000 → "already ordered" for the client
              }
            }

            // 3) Database-enforced rules
            orderSchema.index({ checkoutId: 1 }, { unique: true });          // idempotent retries
            orderSchema.index({ saleId: 1, userId: 1 }, { unique: true });   // one per customer per sale
        """,
        lang="javascript",
        follow=[
            ("How would you release units for orders that are never paid?", "যে order কখনো pay হয় না, সেগুলোর unit কীভাবে ছেড়ে দেবে?"),
            ("Your load test shows p99 checkout latency of 4 seconds at 2,000 RPS. Where do you look first?", "Load test-এ 2,000 RPS-এ checkout-এর p99 latency 4 second দেখাচ্ছে। প্রথমে কোথায় খুঁজবে?"),
        ],
        related=["mongoose-025", "mongoose-023", "mongoose-030"],
        refs=[ATOMICITY, TRANSACTIONS, GUIDE],
    ),
]

if __name__ == "__main__":
    save("mongoose", "b2", QUESTIONS)
