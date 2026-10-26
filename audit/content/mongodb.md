# MongoDB content audit

Coverage: all 32 questions in dumps/mongodb.md reviewed — mongo-001, mongo-002, mongo-003, mongo-004, mongo-005, mongo-006, mongo-007, mongo-008, mongo-009, mongo-010, mongo-011, mongo-012, mongo-013, mongo-014, mongo-015, mongo-016, mongo-017, mongo-018, mongo-019, mongo-020, mongo-021, mongo-022, mongo-023, mongo-024, mongo-025, mongo-026, mongo-027, mongo-028, mongo-029, mongo-030, mongo-031, mongo-032 (count: 32).

## Category summary
This is a strong set. The technical accuracy is high. I re-derived every computed output: the aggregation totals, the window-function ranks and running totals, the projection and `$lookup` outputs, the timezone boundaries and the oplog timestamps. All of them are correct. I found no wrong MCQ keys. The option letters in the explanations match the order shown, and the code in output, MCQ and debugging questions does not leak the answer. The answers explain the mechanism, not just the definition: why ESR avoids an in-memory SORT, why `$unwind` drops unmatched rows, why `w:1` writes get rolled back, and why TTL is not a security check. Most answers also cover trade-offs and verification with `explain`. Difficulty rises sensibly from easy to extreme. The extreme questions (chat sharding, the replica-set incident, oplog PITR recovery) are genuinely senior-level.

The Bangla is natural, contemporary Banglish with tech terms in Latin script. It keeps the same caveats as the English. I found only a few literal renderings and one real meaning drift (mongo-014).

Version claims about MongoDB 9.0 match FACTS.md, and I checked the highest-risk ones against the official docs. The 1 GB / 20% memory limit, the `constraint` validation level, the transaction cap of 10,000, the `ppc64le` note, the Mongoose `syncIndexes` known issue, the 9.0.1 CVE fix, the Atlas-only minors with an annual X.5 release, and Community Search GA in June 2026 are all confirmed.

There are two small factual imprecisions in mongo-022: the definition of the `moderate` validation level, and the scope of "Atlas-only" minor releases.

All COVERAGE.md subtopics are covered. The main redundancy is with the Mongoose set: the `$ne` login injection and the conditional `$inc` stock pattern each appear several times across the two categories. Real gaps: change streams (mentioned often, never asked), array update operators (positional `$`, `$[]`, `arrayFilters`), and geospatial queries.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 9.

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| MONGO-C01 | mongo-022 | both | P2 | Technical accuracy | The definition of the `moderate` validation level leaves out inserts. In `moderate` mode, inserts are validated, and so are updates to documents that were already valid. | EN: "`moderate` only checks updates to documents that were already valid"; BN: "`moderate` শুধু আগে থেকে valid document-এর update check করে" | "`moderate` validates all inserts, and updates only to documents that were already valid (existing invalid documents can still be updated freely)." | High | Matches the MongoDB Schema Validation docs ("validationLevel: moderate"). |
| MONGO-C02 | mongo-022 | both | P3 | Version accuracy | The release model is slightly oversimplified. From 9.0, minor releases go only to **Atlas Core Auto Upgrade**. Atlas Core Manual Upgrade clusters behave like self-managed ones (they get the X.5 Feature Update). | "minor releases (9.1, 9.2…) ship only on Atlas … Atlas clusters get features continuously" | Write "only on Atlas clusters using Auto Upgrade; self-managed and Atlas Manual Upgrade get the major + annual X.5 Feature Update". | High | The mongodb.com/docs/mongodb-versions/ page says minors are "available only through Atlas Core Auto Upgrade and are unavailable to Atlas Core Manual Upgrade and self-managed deployments". |
| MONGO-C03 | mongo-014 | BN | P2 | BN meaning drift | "একটাই item" means "only one item". That suggests an order with exactly one item, not "one and the same element satisfies both conditions", which is what the question tests. | BN Q: "যেখানে **একটাই item**-এর SKU \"A\" এবং `qty ≥ 5`" | Use "যেখানে **একই item**-এর SKU \"A\" আর `qty ≥ 5`" (or "একটা item-ই দুইটা শর্ত পূরণ করে"). | High | A BN reader understands the question as "the same element matches both conditions". |
| MONGO-C04 | mongo-027 | both | P3 | Edge case | A missing sender wallet is reported as "Insufficient balance", because the conditional filter can't tell the two cases apart. The explanation lists "missing receiver" as an edge case but not a missing sender. | `if (debit.matchedCount === 0) throw new Error("Insufficient balance");` | Add a sentence (or a `findOne` inside the transaction on failure) that tells "wallet not found" apart from "insufficient balance". | High | The code review comment is addressed. |
| MONGO-C05 | mongo-020 | both | P3 | Metadata | Time-sensitive claims ("since mid-2026 … GA for self-managed Community Edition", "now branded MongoDB Search") but the question is marked `vs=False`. | ver "Version-independent concept…" vs=False | Set `vs=True` and keep the date. The claim itself is verified (GA announced 2026-06-30). | High | The metadata check passes. |
| MONGO-C06 | mongo-011, mongo-017 | both | P3 | market label | `market=bangladesh` on a generic OTP/TTL scenario and an e-commerce modelling design question. Per FACTS, the BD label is for written MCQ/output-tracing/viva styles, and these are neither. | "market=bangladesh" (mongo-011 scenario, mongo-017 scenario) | Change to `market=both`. Local flavour (bKash, +880) can stay in the text. | Medium | The labels follow the FACTS research note. |
| MONGO-C07 | mongo-028 ↔ mongoose-026; mongo-017/018/027 ↔ mongoose-023/030/031; mongo-013 ↔ mongoose-015; mongo-029 ↔ mongoose-028 | both | P3 | Redundancy | Cross-category overlap. The `{ "password": { "$ne": null } }` login bypass, with the same fix (zod + bcrypt + `sanitizeFilter`), is the centrepiece of both mongo-028 and mongoose-026. The conditional-`$inc` stock/balance guard is taught in at least 6 questions. | mongo-028: "`{ \"email\": \"admin@shop.com\", \"password\": { \"$ne\": null } }`"; mongoose-026 item 1: same payload | Keep mongo-028 focused on deployment/RBAC/network hardening and refer to mongoose-026 for code-level injection (or the reverse). Vary the stock examples. | High | No two questions test the same primary point. |
| MONGO-C08 | mongo-027 (TIP BN), mongo-029/mongo-030 (BN) | BN | P3 | BN phrasing | Literal renderings: "জোরে বলো" (literally "say it loudly") for "Say out loud", and "বিস্ফোরিত হয়" (literally "explodes", as a bomb does) for "explodes" (load blow-up). | "জোরে বলো কেন callback side-effect-free হতে হবে"; "celebrity-র জন্য বিস্ফোরিত হয়"; "বড় group-এ বিস্ফোরিত হয়" | Use "স্পষ্ট করে বলো"; "celebrity-র ক্ষেত্রে write অনেক গুণ বেড়ে যায়". | High | A native-speaker read-through sounds natural. |
| MONGO-C09 | mongo-028 | both | P3 | Question quality | The question text repeats the code and the deployment notes as bullets, and the code block repeats them again. This is redundant on screen. | Q bullets + CODE comments "// - mongod runs on a VPS with net.bindIp 0.0.0.0…" | Keep either the bullets or the code comments. | High | Nothing appears twice when rendered. |
| MONGO-C10 | (category) | — | P2 | Coverage gap | Change streams appear in answers (mongo-020, mongo-029, mongo-030) but are never asked about. There is no question on array update operators (`$`, `$[]`, `$[<id>]` with `arrayFilters`) or on geospatial `2dsphere` / `$near`. These are common in MERN interviews (e.g. "update one item's qty inside an order"). | — | Add 1–2 medium questions: change streams (resume tokens, need for a replica set), and an `arrayFilters` update query. Optionally, a geo "nearby shops" query. | Medium | COVERAGE review. |

## Per-question notes
- mongo-001 — OK (rules on `_id` types, the 16 MB limit and flexible-vs-no schema are all correct)
- mongo-002 — OK
- mongo-003 — OK (12-byte layout 4/5/3 correct; key A correct; BD label acceptable for MCQ)
- mongo-004 — OK (output verified by reasoning: `updateOne` result shape matches mongosh. With 5.0+ lexicographic field processing, new fields `badges`, `verified` are appended in that order. Medium confidence on field order; the explanation correctly says not to rely on it)
- mongo-005 — OK (ordered insert semantics and `MongoBulkWriteError` correct)
- mongo-006 — OK (expected output verified)
- mongo-007 — OK
- mongo-008 — OK
- mongo-009 — OK
- mongo-010 — OK (10 s election timeout, 50 members / 7 voting, w:majority default since 5.0 — all correct)
- mongo-011 — issues: MONGO-C06; scores acc/depth/BN/EN 9/9/9/9
- mongo-012 — OK (revenue 580/450/340 recomputed)
- mongo-013 — OK (left-outer-join + `preserveNullAndEmptyArrays` output verified)
- mongo-014 — issues: MONGO-C03; scores 10/8/7/9
- mongo-015 — OK (ESR reasoning and covered-query notes correct)
- mongo-016 — OK (missing field is indexed as null → E11000; the partial index with `$type:"string"` is the right fix)
- mongo-017 — issues: MONGO-C06; scores 9/9/9/9 (totals 3798−200+60=3658 verified)
- mongo-018 — OK (60 s lifetime, ~1,000 docs guidance, 9.0 cap of 10,000 verified)
- mongo-019 — OK
- mongo-020 — issues: MONGO-C05; scores 9/9/9/9 (Community GA claim verified)
- mongo-021 — OK (driver v6+ return shape, `includeResultMetadata` correct)
- mongo-022 — issues: MONGO-C01, MONGO-C02; scores 8/9/8/9
- mongo-023 — OK (UTC vs Asia/Dhaka month boundaries and the 121:1 ratio verified)
- mongo-024 — OK (9.0 per-operation limit default verified; `$facet` sub-pipelines can't use indexes)
- mongo-025 — OK
- mongo-026 — OK (running totals 500/800/1500, 200/1100 and ranks verified)
- mongo-027 — issues: MONGO-C04, MONGO-C08; scores 9/9/8/9
- mongo-028 — issues: MONGO-C07, MONGO-C09; scores 10/9/9/9 (9.0.1 security fix verified: CVE-2026-89099)
- mongo-029 — issues: MONGO-C08; scores 9/9/8/9
- mongo-030 — issues: MONGO-C08; scores 9/10/8/9 (3,472 writes/s and 150 GB/day verified; the compound hashed shard key and `_id` uniqueness reasoning are correct)
- mongo-031 — OK
- mongo-032 — OK (timestamps 1791748800 = 2026-10-11T20:00Z = 02:00 Dhaka, and 1791792303 = 08:05:03Z, verified; `mongorestore` insert-only merge semantics correct)

## Coverage & gaps
- All COVERAGE.md subtopics are present: documents/collections, BSON, CRUD, operators/projection, aggregation (`$match`/`$group`/`$lookup`/`$unwind`/`$facet` — `$facet` only appears as an anti-pattern in mongo-024, which is fine), indexes, ESR, unique/partial, text + Atlas Search, schema design, embed vs reference, transactions, replication/write+read concern, sharding, atomicity, consistency, explain, security, backup/recovery, real-world modelling, MongoDB 9.0.
- Gaps (MONGO-C10): change streams; array update operators with `arrayFilters`; geospatial. `$jsonSchema` validation is only covered inside the 9.0 question (mongo-022) and mentioned in mongo-001. A short question on DB-level schema validation would help.
- Redundancy: see MONGO-C07 (overlap with Mongoose on injection, the stock `$inc` guard and `$lookup` vs populate).
- Difficulty labels look right. The easy MCQs (003/005/007) are trivia-plus-explanation, which suits written tests.

## Needs verification
- mongo-004: exact field order of `{ ..., badges, verified }` after a multi-operator update on 5.0+ (Medium confidence that `badges` precedes `verified`). Run against mongosh to confirm.
- mongo-011: "TTL works only on single-field indexes (compound indexes ignore the option)". This was true through 8.x as far as I know; I did not check it against the 9.0 docs.
- mongo-032: "since MongoDB 6.1 multi-deletes are batched into applyOps entries" (Medium confidence. Batched deletes landed in the 6.x line; the exact first version should be checked).

## Verified
- WebFetch https://www.mongodb.com/docs/manual/release-notes/9.0/ — confirmed: the per-operation limit is "1 gigabyte or 20% of the memory available … whichever is greater"; per-stage 100 MB unchanged; `$where`/`$function`/`$accumulator` un-deprecated on WASM, not on `ppc64le`; `constraint` level wording; `maxConcurrentMultiDocumentTransactions` 10000 / `TooManyOpenTransactions`; known issue SERVER-89953 (`collation: { locale: "simple" }` → Mongoose `syncIndexes()` rebuilds; fixed in Mongoose 9.10.4 / 8.24.5); 9.0.1 fixes CVE-2026-89099.
- WebFetch https://www.mongodb.com/docs/mongodb-versions/ — from 9.0, minors only via Atlas Core Auto Upgrade; annual X.5 Feature Update for Atlas + self-managed; majors supported 5 years (+2 ELS). Basis for MONGO-C02.
- WebSearch "MongoDB Search Vector Search Community Edition … GA" — the MongoDB product-updates page "Now GA: MongoDB Search and Vector Search for Community Edition" (announced 2026-06-30; public preview 2025-09-17). This supports mongo-020's "mid-2026" claim. https://www.mongodb.com/products/updates/now-ga-mongodb-search-and-vector-search-for-community-edition/
- node (SCRATCH/run, inline `-e`): `Date.UTC(2026,9,11,20)/1000 = 1791748800`; `1791792303` → `2026-10-12T08:05:03Z`; `300e6/86400 = 3472`.
- Manual recomputation of the expected outputs for mongo-006, 012, 013, 017, 023 and 026.
