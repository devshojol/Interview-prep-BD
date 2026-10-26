# Mongoose content audit

Coverage: all 32 questions in dumps/mongoose.md reviewed — mongoose-001, mongoose-002, mongoose-003, mongoose-004, mongoose-005, mongoose-006, mongoose-007, mongoose-008, mongoose-009, mongoose-010, mongoose-011, mongoose-012, mongoose-013, mongoose-014, mongoose-015, mongoose-016, mongoose-017, mongoose-018, mongoose-019, mongoose-020, mongoose-021, mongoose-022, mongoose-023, mongoose-024, mongoose-025, mongoose-026, mongoose-027, mongoose-028, mongoose-029, mongoose-030, mongoose-031, mongoose-032 (count: 32).

## Category summary
This is a high-quality, practical set. It targets the bugs Mongoose users actually hit:
- update validators being opt-in, and which operators they cover
- `pre('save')` not running on `findByIdAndUpdate`
- missing `{ session }` and `Promise.all` inside transactions
- `strictQuery` semantics
- `__v` not protecting plain fields
- `perDocumentLimit` vs `limit`
- connection-scoped models causing buffering timeouts
- the Mongoose 9 / MongoDB 9.0 `syncIndexes` incident

The Mongoose 9 content (no `next()` in pre hooks, `updatePipeline`, `returnDocument`, `isValidObjectId(6)`, `QueryFilter`) matches FACTS.md. I checked the key points against the official migration guide and the API docs. MCQ keys are all correct, and debugging questions don't leak answers.

There is one material error. In mongoose-026 the "fixed" code enables `sanitizeFilter` globally and then uses its own `$regex` operator without `mongoose.trusted()`. That turns the search into a literal `$eq` match that returns nothing. The answer text even mentions `trusted()`, but the code doesn't use it.

Smaller issues: a discriminator-key inconsistency (022), an imprecise parenthetical about deprecation (021), an unexplained "no error surfaced" with an awaited `syncIndexes()` (032), the exact error type for a leftover `next()` call, and one unsupported Bangladesh-market claim.

The Bangla is natural and keeps the technical caveats; terminology is consistent. All COVERAGE.md subtopics are covered. There is heavy repetition of the "conditional `$inc` for stock" and "hook doesn't run on updates" points across questions. Gaps: TypeScript typing (`InferSchemaType`, `HydratedDocument`), subdocument arrays and positional updates, and change-stream/`watch()` usage.

Scores: Technical accuracy 8.5 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 9 | English quality 9 | Examples & code 8 | Originality/information value 9 | Structural clarity 9.

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| MGS-C01 | mongoose-026 | both (code) | P1 | Wrong code / misleading fix | The fixed version turns on `sanitizeFilter` globally and then builds a filter with its own `$regex` operator. `sanitizeFilter` wraps any nested object with a `$`-prefixed key in `$eq`. So `{ nameLower: { $regex: "^abc" } }` becomes `{ nameLower: { $eq: { $regex: "^abc" } } }` and the search returns nothing. The answer text mentions `mongoose.trusted()`, but the code doesn't apply it. | Code: `mongoose.set("sanitizeFilter", true);` … `Product.find({ nameLower: { $regex: \`^${safe}\` } })` | Use `Product.find({ nameLower: mongoose.trusted({ $regex: \`^${safe}\` }) })` (or a `RegExp` object: `{ nameLower: new RegExp(\`^${safe}\`) }`, which isn't a `$`-key object). Add a sentence saying operators you add yourself must be wrapped in `trusted()` once `sanitizeFilter` is on. | High | Mongoose API docs: sanitizeFilter "wrap[s] any nested objects that have a property whose name starts with `$` in a `$eq`"; `trusted()` opts out. Acceptance test: with `sanitizeFilter: true`, the fixed search returns the matching products. |
| MGS-C02 | mongoose-013, mongoose-021 | both | P3 | Unverified specific | Says calling `next()` in a v9 pre hook "throws a `TypeError`". The migration guide only says pre middleware "no longer receives a `next()` parameter". The exact failure depends on what is passed as the first argument (probably "next is not a function", but this is unconfirmed). | 013 EN: "pre middleware no longer receives `next`. Calling it throws a `TypeError`."; 021 EN: "will throw a `TypeError` at runtime" | Say "calling `next()` fails at runtime (`next` is no longer a function you receive)" unless verified on 9.11. | Medium | Run a 9.11 repro; if the error is TypeError, keep the text. |
| MGS-C03 | mongoose-021 | both | P3 | Clarity | The parenthetical sits after `returnDocument`, so it reads as if `returnDocument` were the deprecated option. | "replace `new: true` / `returnOriginal: false` with `returnDocument: \"after\"` (deprecated since 9.2, warnings in logs)"; BN same placement | "…replace `new: true` / `returnOriginal: false` (both deprecated since 9.2) with `returnDocument: \"after\"`." | High | Read-through. |
| MGS-C04 | mongoose-022 | both | P3 | Internal inconsistency | The code sets `discriminatorKey: "kind"`, and the code comment says the filter includes `{ kind: "sms" }`. The answer then says the child query adds `{ __t: "sms" }`. | Answer: "automatically adds `{ __t: \"sms\" }` to the filter"; code comment: "filter automatically includes { kind: \"sms\" }" | Use `{ kind: "sms" }` in the answer, or add "(`__t` by default; `kind` in this example)". | High | Text and code agree. |
| MGS-C05 | mongoose-032 | both | P2 | Scenario/answer gap | The scenario says the app "calls `syncIndexes()` at startup" and "no error surfaced". An awaited `syncIndexes()` rejects when the unique build fails on duplicates. The answer explains the silence only through the `autoIndex` `'index'` event and never says why the `syncIndexes()` rejection went unnoticed. | Q: "the app calls `syncIndexes()` at startup … no error surfaced"; A: "Mongoose reports that only as an `'index'` error event / log line" | Add: "the startup `syncIndexes()` call was fire-and-forget / caught-and-logged (or ran in only one pod and failed there), so its rejection was swallowed", or change the scenario. | Medium | The explanation covers both index paths. |
| MGS-C06 | mongoose-020 | both | P3 | Unsupported market claim | Claims frequency in BD teams. FACTS only says BD job posts list Mongoose/Prisma/TypeORM. | EN: "in many Bangladeshi MERN teams Mongoose is the common default"; BN: "বাংলাদেশের অনেক MERN team-এ Mongoose-ই common default" | "If your existing services and team already use Mongoose, consistency is a legitimate reason to choose it." | High | No frequency claim remains. |
| MGS-C07 | mongoose-018 | both | P3 | Unverified TS claim | States that unknown keys still compile under Mongoose 9's `QueryFilter`. The migration guide only says it "enforces stronger types for top-level keys" and doesn't say how unknown keys are handled. | "an unknown key like `emial` still compiles" | Verify with `tsc` on Mongoose 9.11, or soften to "may still compile depending on your schema typing". | Low | `tsc` repro. |
| MGS-C08 | mongoose-017 | — | P3 | Filler metadata | A complexity field on an Express error middleware adds nothing. | `COMPLEXITY: {'time': 'O(k) where k = number of invalid fields', 'space': 'O(k)'}` | Drop `time`/`space` for this non-algorithmic coding question. | High | — |
| MGS-C09 | mongoose-004, 012, 013, 014, 023, 030, 031 (+ mongo-017/018/027) | both | P3 | Redundancy | The "conditional `$inc` guard for stock" and "`pre('save')` doesn't run on `findOneAndUpdate`" points are each re-taught in 4–7 questions. 013 and 014 overlap substantially (014's key point is the "Explanation" bullet of 013). | 013 EXPL: "This hook only covers `save()` … `findOneAndUpdate`/`updateOne` bypasses it"; 014 key: "`findByIdAndUpdate` … hash hook never runs" | Keep 014 as the MCQ and, in 013, link to 014 instead of repeating the point. Vary the scenarios in 023/030/031 (e.g. 030 could focus on the read model and seller split rather than the stock guard). | High | Each question has a distinct primary learning point. |
| MGS-C10 | mongoose-026 ↔ mongo-028 | both | P3 | Cross-tech duplicate | Same login operator-injection payload and same fix in both categories. | "`{ \"email\": \"admin@shop.com\", \"password\": { \"$ne\": null } }`" (both) | See MONGO-C07: split the focus (Mongoose features vs deployment hardening). | High | — |
| MGS-C11 | (category) | — | P2 | Coverage gap | No question on TypeScript with Mongoose (`InferSchemaType`, `HydratedDocument`, typing methods and statics). It's only a follow-up in 008 and a passing mention in 021. Nothing on subdocument arrays (`doc.items.id()`, positional `$` / `arrayFilters` via Mongoose), and nothing on `Model.watch()` change streams. TS + Mongoose is very common in NestJS/MERN roles. | mongoose-008 follow-up: "How would you type instance methods and statics in TypeScript?" | Add a medium TS-typing question and an easy/medium subdocument-array update question. | Medium | COVERAGE review. |

## Per-question notes
- mongoose-001 — OK (the console output `rafi@example.com customer` is correct via the lowercase setter + default)
- mongoose-002 — OK
- mongoose-003 — OK (unique is not a validator; the race-condition note is good)
- mongoose-004 — OK (update validators skip `$inc` — confirmed in the docs)
- mongoose-005 — OK
- mongoose-006 — OK
- mongoose-007 — OK
- mongoose-008 — OK
- mongoose-009 — OK (the BD mobile regex is correct; `errors` keys name/phone/age are plausible — category isn't validated when undefined)
- mongoose-010 — OK
- mongoose-011 — OK (`isObjectIdOrHexString` recommendation correct; v9 `isValidObjectId(6)` change confirmed)
- mongoose-012 — OK (operator list and `this` = query confirmed in the docs; global `runValidators` option exists)
- mongoose-013 — issues: MGS-C02, MGS-C09; scores 9/9/9/9
- mongoose-014 — issues: MGS-C09; scores 10/8/9/9
- mongoose-015 — OK
- mongoose-016 — OK
- mongoose-017 — issues: MGS-C08; scores 9/9/9/9
- mongoose-018 — issues: MGS-C07; scores 9/9/9/9
- mongoose-019 — OK
- mongoose-020 — issues: MGS-C06; scores 9/9/9/9
- mongoose-021 — issues: MGS-C02, MGS-C03; scores 9/9/9/8 (the claim that hooks on custom methods/statics require async/promise is confirmed in the migration guide)
- mongoose-022 — issues: MGS-C04; scores 9/9/9/9
- mongoose-023 — OK (all four bugs are real; symptom→cause mapping is excellent; `transactionAsyncLocalStorage` mention correct)
- mongoose-024 — OK (skip count (500−1)×20 = 9,980 verified; keyset handler correct)
- mongoose-025 — OK (key C correct; `optimisticConcurrency` explained well)
- mongoose-026 — issues: MGS-C01, MGS-C10; scores 7/9/9/9
- mongoose-027 — OK (good pitfalls: `$geoNear`/`$search` first stage, TTL bypassing hooks, partial unique index)
- mongoose-028 — OK
- mongoose-029 — OK
- mongoose-030 — issues: MGS-C09; scores 9/10/9/9
- mongoose-031 — issues: MGS-C09; scores 10/10/9/9
- mongoose-032 — issues: MGS-C05; scores 9/10/9/9 (the SERVER-89953 known issue and its workaround match the 9.0 release notes exactly)

## Coverage & gaps
- Every COVERAGE.md subtopic has at least one question: schemas/models, documents, CRUD, validation, middleware (v9 no-`next`), populate, references, virtuals, methods/statics, lean, indexes (autoIndex, syncIndexes), query performance, transactions, error handling (ValidationError/CastError/E11000), schema design, pitfalls, driver vs Mongoose, Mongoose 9 changes.
- Gaps: see MGS-C11 (TypeScript typing; subdocument arrays and positional updates; `watch()`).
- Redundancy: MGS-C09 and MGS-C10.
- Difficulty: labels are appropriate. 005 (findOne → null) is very basic but fine as an easy MCQ.
- Market labels: the `bangladesh` labels on 001/003/005/007/009/010/011 are viva/MCQ-style fundamentals, which FACTS allows. No change needed.

## Needs verification
- mongoose-013/021: the exact runtime error when a v9 pre hook calls `next()` (MGS-C02).
- mongoose-018: whether Mongoose 9 `QueryFilter` lets unknown top-level keys compile (MGS-C07).
- mongoose-011: "older releases accepted any 12-character string such as `\"hello-world!\"`" for `isValidObjectId` — true historically for Mongoose 6. Which version stopped accepting it isn't stated; the hedged wording is fine.
- mongoose-029: "calling `mongoose.connect()` when already connected is a no-op" (Medium; true for the same URI in recent versions as far as I know).

## Verified
- WebFetch https://mongoosejs.com/docs/api/mongoose.html — `sanitizeFilter` wraps `$`-key nested objects in `$eq`; `trusted()` opts out; a global `runValidators` option exists (default false). Basis for MGS-C01.
- WebFetch https://mongoosejs.com/docs/migrating_to_9.html — pre middleware no longer receives `next()` (the error type isn't stated); hooks on custom methods/statics need async/promise; `updatePipeline: true` / `mongoose.set('updatePipeline', true)`; `isValidObjectId()` returns false for numbers and `new ObjectId(6)` throws; QueryFilter "enforces stronger types for top-level keys" (unknown keys not discussed).
- WebFetch https://mongoosejs.com/docs/validation.html — update validators run only on `$set`, `$unset`, `$push`, `$addToSet`, `$pull`, `$pullAll`; in update validators `this` is the query.
- WebFetch https://www.mongodb.com/docs/manual/release-notes/9.0/ — the Mongoose `syncIndexes()` known issue at FCV 9.0 (`collation: { locale: "simple" }`), with the fix in Mongoose 9.10.4 / 8.24.5 and the advice to stop calling syncIndexes at startup. This confirms mongoose-021/032.
- Mongoose is not installed locally, so I could not execute a code repro.
