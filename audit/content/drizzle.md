# Drizzle content audit

Coverage: 32 of 32 questions reviewed: drizzle-001, drizzle-002, drizzle-003, drizzle-004, drizzle-005, drizzle-006, drizzle-007, drizzle-008, drizzle-009, drizzle-010, drizzle-011, drizzle-012, drizzle-013, drizzle-014, drizzle-015, drizzle-016, drizzle-017, drizzle-018, drizzle-019, drizzle-020, drizzle-021, drizzle-022, drizzle-023, drizzle-024, drizzle-025, drizzle-026, drizzle-027, drizzle-028, drizzle-029, drizzle-030, drizzle-031, drizzle-032.

## Category summary
This is an excellent, version-accurate category. It consistently teaches 0.45.x as stable, labels the v1 RC as preview (drizzle-027 has `status=preview`, and other mentions say "v1 RC (preview)"), and uses current 0.45 APIs:
- `drizzle({ client, schema })`
- identity columns
- the array-form third argument of `pgTable`
- `$count`
- `DrizzleQueryError` (since 0.44)
- `withReplicas`
- `.for('update', { skipLocked })`
- `$dynamic`

The expected outputs (drizzle-kit SQL, query results) are internally consistent and match drizzle-kit's naming conventions. I found no wrong MCQ keys or wrong outputs. The PostgreSQL depth is unusually strong for an ORM section: ON vs WHERE in outer joins, conditional UPDATE re-check semantics, the arbiter-index requirement for ON CONFLICT, NOT VALID + VALIDATE, CONCURRENTLY inside the single-transaction migrator, and PgBouncer with prepared statements.

The weaknesses are minor:
- one confusing MCQ where the code lines and the answer options are both labelled A–D (drizzle-008)
- several small technical over-simplifications (lower-case index for suffix search, stacked-query injection example, "planned once" for prepared statements, "cross-database" relations)
- "Verified …" authoring notes leaking into learner text in about 9 questions
- empty follow-ups on all 7 MCQs
- the same three themes repeated across many questions: the conditional UPDATE, the single-transaction migrator, and PgBouncer with prepared statements

The Bangla is natural and technically faithful, with consistent terminology; I found no meaning drift. Coverage of COVERAGE.md is complete. The difficulty spread (11/11/7/3) and MCQ count (7) are on target.

Scores: Technical accuracy 9 | Explanation depth 10 | Interview usefulness 9 | Bangla quality 9 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 8

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| DRZ-C01 | drizzle-008 | both | P2 | MCQ structure / ambiguity | The code lines are labelled A–D, and the four answer options are also lettered A–D. So the correct option is "A" while its text is "Only D", and the explanation switches between line letters and option letters. A learner can easily misread which "D" or "B/C" is meant. | Code: "// A … // D"; options: "OPTION A (CORRECT): Only D"; explanation: "The tempting wrong answer is B/C" (lines) … "Option D in the list ('Drizzle escapes everything')" (option) | Label the code lines 1–4 (or i–iv) and rewrite the options as "Only line 4", "Lines 2 and 3", and so on. Update the explanation to match. | High | Learner text never uses the same letter for both a line and an option |
| DRZ-C02 | drizzle-005 | both | P3 | Technical accuracy | The performance note suggests a lower-case email column with an index as a remedy for a suffix search (`'%@gmail.com'`). A normal B-tree index on `lower(email)` still can't serve a leading-wildcard pattern; it only removes the need for `ilike`. | "or store a normalised lower-case email with an index on it." | Say: "a `pg_trgm` GIN index, or store the domain in its own (lower-cased) column / index `reverse(lower(email))` and search by prefix." | High | `EXPLAIN` on `lower(email) LIKE '%@gmail.com'` with a B-tree index on `lower(email)` shows a Seq Scan |
| DRZ-C03 | drizzle-028 | both | P3 | Technical accuracy | The injection example `?sort=1; DROP TABLE …` doesn't work through node-postgres here. The query has bound params (customer id, limit, offset), so it uses the extended protocol, which rejects multiple statements. The real risks are subqueries, boolean/time-based blind extraction, and error-based leaks. | "`sql.raw(req.query.sort)` puts user input straight into the SQL text (`?sort=1; DROP TABLE ...` or data-exfiltrating subqueries)" | Lead with a realistic payload, e.g. `?sort=(case when (select substr(password_hash,1,1) from users where id=1)='a' then id else created_at end)`. Say that stacked statements usually fail with parameterised queries, but extraction via subqueries still works. | High | With pg, `query('select 1 order by 1; drop table x', [])`-style text plus params fails with "cannot insert multiple commands into a prepared statement" |
| DRZ-C04 | drizzle-021 | both | P3 | Technical nuance | The text says a named statement is "parsed and planned once per connection". PostgreSQL parses and analyses once, but by default it builds a **custom plan** on each of the first 5 executions, then may switch to a cached generic plan. The explanation's "generic plans" bullet partly covers this, but the answer contradicts it. | "with node-postgres, a named statement is parsed and planned once per connection; later executions only bind parameters" | "…parsed once per connection; planning may be reused via a generic plan after a few executions (see `plan_cache_mode`)." | High | PostgreSQL docs, PREPARE: "the first five executions are done with custom plans" |
| DRZ-C05 | drizzle-010 | both | P3 | Accuracy (minor) | "Cross-database links" is given as a valid use of relations without FKs. Drizzle's relational query compiles to one SQL statement on one connection, so it can't join across databases. Relations without FKs make sense for legacy tables, FK-less engines (e.g. PlanetScale/Vitess) or views. | "relations without FKs (legacy tables, cross-database links)" | Replace with "legacy tables, views, or databases where FKs are disabled (e.g. Vitess/PlanetScale)". | High | Read-through |
| DRZ-C06 | drizzle-008, 009, 013, 015, 016, 018, 022, 025, 032 | both | P3 | Authoring artifact | Learner-facing text repeatedly says "Verified …", "(verified)" or "(verified with a one-connection PGlite setup)". These are the author's test notes. They are unverifiable for the learner and odd in an interview answer. Some are also cryptic, e.g. "returned `[1, 0, null]`" with no explanation of what the values are. | drizzle-025: "Verified: three concurrent reservations of 1 unit with stock 2 returned `[1, 0, null]`"; drizzle-009: "is **not** reported (verified)"; drizzle-032: "**Verified behaviour:**" | Rephrase as plain facts or as a suggested experiment ("Try it: run three concurrent reservations… two succeed (remaining stock 1 then 0), the third gets no row"). | High | No "verified" wording remains in learner text |
| DRZ-C07 | drizzle-005, 006, 007, 008, 015, 018, 024 | both | P3 | Structure | All 7 MCQs have empty follow-ups. AUTHORING §3 asks for 1–3. | "FOLLOW-UPS: []" | Add 1–2 each, e.g. drizzle-018: "How would you read the attempted insert value in `set`?"; drizzle-024: "What else breaks behind a transaction-mode pooler?". | High | `follow` is non-empty for every MCQ |
| DRZ-C08 | drizzle-014 | code/output | P3 | Output determinism | The top-level query has no `orderBy`, but the expected output lists Rahim then Karim as if the order were guaranteed. Also, `publishedAt` is shown as an ISO string, but Drizzle returns a `Date` (JSON-serialised it becomes a string). | `db.query.users.findMany({ columns…, where…, with… })` with no top-level `orderBy`; output `"publishedAt": "2026-10-01T00:00:00.000Z"` | Add `orderBy: (u, { asc }) => [asc(u.id)]`. Note "(shown as JSON)" above the output. | High | Read-through |
| DRZ-C09 | drizzle-030 | both | P3 | Design detail | The unique constraint `(user_id, product_id, sale_id)` on reservations would stop a user from reserving again after their reservation **expired**, because the expired row still exists. `sale_id` is also not among the listed reservation columns. The sweeper updates `products` in reservation-id order, so two sweepers locking several products in different orders can deadlock. | "with a unique `(user_id, product_id, sale_id)` to stop one user grabbing everything"; listed columns "reservations(id, product_id, user_id, qty, status, expires_at)" | Use a partial unique index `WHERE status IN ('pending','paid')` and add `sale_id` to the column list. In the sweeper, aggregate qty per product and update products in `product_id` order. | Medium | Read-through; a concurrent sweeper test shows no `40P01` |
| DRZ-C10 | drizzle-026 | both | P3 | Completeness | The custom migrations for the NOT NULL steps aren't tied back to `schema.ts`. Custom migrations don't update the drizzle-kit snapshot, so the author must also add `.notNull()` to `phone` (and the next `generate` may emit a redundant `SET NOT NULL`). Release 3 also runs VALIDATE and SET NOT NULL in the same migrator transaction, while the answer text says "in a **separate** run, `VALIDATE`" (relative to ADD). That's acceptable, but it isn't explained. | "Release 3 — custom: validate … then flip to NOT NULL"; answer step 3 "in a **separate** run, `VALIDATE CONSTRAINT`" | Add one line: "Then add `.notNull()` to `phone` in `schema.ts` and run `generate`. Review that it produces either nothing or a harmless `SET NOT NULL`." | Medium | Run `generate` after the custom migrations and check for snapshot drift |
| DRZ-C11 | drizzle-022 | both | P3 | Edge case | The user-supplied `search` term is interpolated into an `ilike` pattern unescaped. That isn't SQL injection, but `%` and `_` from users act as wildcards (e.g. `search=%` matches everything, and long patterns can be costly). | "`filters.push(ilike(posts.title, `%${f.search}%`))`" | Escape `%`, `_` and `\` in `search` (e.g. `f.search.replace(/[\\%_]/g, '\\$&')`) and cap its length. Mention this in the explanation. | High | Searching `"_"` returns only titles containing an underscore |
| DRZ-C12 | drizzle-016, 025, 030 (+ nest-032); 017, 026, 032; 021, 023, 024 | both | P3 | Redundancy | Three themes are each a major point in 3–4 questions: (a) the conditional `UPDATE … WHERE stock/balance >= x RETURNING` pattern; (b) "the migrator runs all pending migrations in one transaction"; (c) "PgBouncer transaction mode breaks named prepared statements". Each is correct, but the repetition lowers the bank's information density. | drizzle-016: "Debit atomically with a guard"; drizzle-025: "make the check and the write one atomic statement"; drizzle-030: "Reserve atomically" | Keep each theme primary in one question (016, 032, 024) and cross-reference it elsewhere in one line. Use the freed space for gaps (see Coverage). | High | Each theme is primary in only one question |
| DRZ-C13 | drizzle-005 | meta | P3 | Market label | An MCQ is labelled `bangladesh`, while comparable easy MCQs (006, 007, 008) are `both`. FACTS allows `bangladesh` for MCQ fundamentals, so this isn't wrong, just inconsistent. | "drizzle-005 … market=bangladesh" | Use `both`, or apply the label consistently. | Medium | Consistent labels |

## Per-question notes
- drizzle-001 — OK (acc 10 / depth 9 / BN 9 / EN 9)
- drizzle-002 — OK (acc 10 / depth 9 / BN 9 / EN 9; generated SQL matches drizzle-kit conventions: `users_email_unique`, identity sequence clause)
- drizzle-003 — OK (acc 10 / depth 9 / BN 9 / EN 9)
- drizzle-004 — OK (acc 10 / depth 9 / BN 9 / EN 9; expected output is consistent: total 3 after +1 insert −1 delete)
- drizzle-005 — issues: DRZ-C02, DRZ-C07, DRZ-C13; scores acc 9 / depth 8 / BN 9 / EN 9
- drizzle-006 — issues: DRZ-C07; scores acc 10 / depth 9 / BN 9 / EN 9
- drizzle-007 — issues: DRZ-C07; scores acc 10 / depth 9 / BN 9 / EN 9
- drizzle-008 — issues: DRZ-C01, DRZ-C06, DRZ-C07; scores acc 10 / depth 9 / BN 9 / EN 8
- drizzle-009 — issues: DRZ-C06; scores acc 10 / depth 10 / BN 9 / EN 9 (lazy thenable; `checkThenables` defaults to false in typescript-eslint v8, correct)
- drizzle-010 — issues: DRZ-C05; scores acc 9 / depth 9 / BN 9 / EN 9
- drizzle-011 — OK (acc 9 / depth 9 / BN 9 / EN 9)
- drizzle-012 — OK (acc 10 / depth 10 / BN 9 / EN 9)
- drizzle-013 — issues: DRZ-C06; scores acc 10 / depth 10 / BN 9 / EN 9 (ON vs WHERE and `count(col)` logic correct; output correct for the data)
- drizzle-014 — issues: DRZ-C08; scores acc 9 / depth 9 / BN 9 / EN 9
- drizzle-015 — issues: DRZ-C06, DRZ-C07; scores acc 10 / depth 9 / BN 9 / EN 9
- drizzle-016 — issues: DRZ-C06, DRZ-C12; scores acc 10 / depth 10 / BN 9 / EN 9
- drizzle-017 — issues: DRZ-C12; scores acc 10 / depth 10 / BN 9 / EN 9
- drizzle-018 — issues: DRZ-C06, DRZ-C07; scores acc 10 / depth 9 / BN 9 / EN 9 (42P10 correct)
- drizzle-019 — OK (acc 10 / depth 10 / BN 9 / EN 9)
- drizzle-020 — OK (acc 9 / depth 9 / BN 9 / EN 9; balanced, not tribal)
- drizzle-021 — issues: DRZ-C04, DRZ-C12; scores acc 8 / depth 9 / BN 9 / EN 9
- drizzle-022 — issues: DRZ-C06, DRZ-C11; scores acc 9 / depth 9 / BN 9 / EN 9
- drizzle-023 — issues: DRZ-C12; scores acc 10 / depth 10 / BN 9 / EN 9 (pg default pool max 10 correct)
- drizzle-024 — issues: DRZ-C07, DRZ-C12; scores acc 10 / depth 9 / BN 9 / EN 9
- drizzle-025 — issues: DRZ-C06, DRZ-C12; scores acc 10 / depth 10 / BN 9 / EN 9
- drizzle-026 — issues: DRZ-C10, DRZ-C12; scores acc 9 / depth 10 / BN 9 / EN 9
- drizzle-027 — OK (acc 9 / depth 9 / BN 9 / EN 9; correctly `status=preview`; some RC details are in Needs verification)
- drizzle-028 — issues: DRZ-C03; scores acc 9 / depth 10 / BN 9 / EN 9
- drizzle-029 — OK (acc 9 / depth 10 / BN 9 / EN 9; the statement-breakpoint-in-comment gotcha is a strong practical detail)
- drizzle-030 — issues: DRZ-C09, DRZ-C12; scores acc 9 / depth 10 / BN 9 / EN 9 (`international` label justified)
- drizzle-031 — OK (acc 10 / depth 10 / BN 9 / EN 9)
- drizzle-032 — issues: DRZ-C06, DRZ-C12; scores acc 10 / depth 10 / BN 9 / EN 9

## Coverage & gaps
- Every COVERAGE.md subtopic is covered: type-safe queries, schema/column types/identity, relations, CRUD, joins, RQB, migrations (generate/migrate/push/pull, config), introspection, transactions, prepared statements, drivers (pg/postgres.js/neon), `$inferSelect`/`$inferInsert`, relations vs FKs, Drizzle Kit, error handling, connection management/serverless, vs Prisma, vs raw SQL, when an ORM fits, and v1 RC as preview.
- Optional additions, if the redundant space (DRZ-C12) is reclaimed:
  - batch/bulk insert (`values([...])` limits, `COPY`), which only appears as a follow-up
  - validation integration (`drizzle-zod` / `createInsertSchema` with 0.45), which is only mentioned
  - `jsonb` columns with `$type<T>()`, plus array/enum handling
  - views (`pgView`), mentioned only
  - testing patterns (transaction-rollback per test, PGlite), only in passing
- Difficulty: easy 11 / medium 11 / hard 7 / extreme 3, on target. Types are well mixed (7 MCQ, 4 coding, 1 query, 3 debugging, 3 scenario, etc.). The labels look appropriate.
- Cross-tech redundancy: nest-022 and drizzle-003/023 overlap on pool setup and shutdown; nest-025 and drizzle-019 overlap on `DrizzleQueryError.cause`; nest-032 and drizzle-016/025 overlap on the conditional UPDATE/outbox. Each is acceptable, since the framing differs, but consider cross-linking instead of re-explaining.

## Needs verification
- drizzle-027: v1 RC details. "`check` gains commutativity checks for migrations from different branches; `drop` is removed"; "one folder per migration (SQL + snapshot), no `_journal.json`"; "a relation can carry its own `where`"; `RAW` filter escape hatch. (npm shows rc.5 is now the `rc` tag; FACTS says rc.4. The content doesn't cite an rc number, so this is fine.)
- drizzle-029: "`drizzle-kit pull --init`" (v1 RC); `tablesFilter: ['!legacy_*']` negation glob support in drizzle-kit 0.31; the exact 0.31 pull output layout (`drizzle/0000_*.sql` with commented body).
- drizzle-023: the exact error text "No transactions support in neon-http driver".
- drizzle-001/027: validators moving to `drizzle-orm/zod` in v1 RC.
- drizzle-020: "Prisma ORM 7.x" architecture claims (stated generically; low risk).

## Verified
- `npm view` (2026-10-26): `drizzle-orm` latest **0.45.4**, rc **1.0.0-rc.5**; `drizzle-kit` latest **0.31.11**, rc 1.0.0-rc.5; `pg` 8.23.1; `postgres` 3.4.9. This matches the content's "0.45.x stable / drizzle-kit 0.31 / v1 RC" framing and the `pg 8` / `postgres.js 3` labels.
- Reasoned and not executed (no PostgreSQL or Drizzle install; I did not download packages):
  - drizzle-004 output arithmetic
  - drizzle-013 LEFT JOIN + `count(posts.id)` result for the sample data (Nadia 2, Rahim 1, Karim 0)
  - drizzle-018 42P10 on ON CONFLICT without an arbiter
  - drizzle-016/025 conditional-UPDATE re-check under READ COMMITTED (EvalPlanQual)
  - drizzle-032 SQLSTATE 25001 for CONCURRENTLY inside a transaction, and that a plain CREATE INDEX takes a SHARE lock
  - drizzle-026: SET NOT NULL skips the scan with a validated CHECK (PG12+)
  - drizzle-024: node-postgres uses unnamed statements unless named
