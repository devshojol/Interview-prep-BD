# PostgreSQL content audit
Coverage: 32 of 32 questions reviewed — pg-001, pg-002, pg-003, pg-004, pg-005, pg-006, pg-007, pg-008, pg-009, pg-010, pg-011, pg-012, pg-013, pg-014, pg-015, pg-016, pg-017, pg-018, pg-019, pg-020, pg-021, pg-022, pg-023, pg-024, pg-025, pg-026, pg-027, pg-028, pg-029, pg-030, pg-031, pg-032.

## Category summary
This is a very strong category. The technical accuracy is high throughout. I found no wrong MCQ keys, no wrong expected outputs and no materially incorrect teaching. The answers show real operational experience: lock-queue outages from `ALTER TABLE`, the `pg.Pool` BEGIN/COMMIT trap, EvalPlanQual re-checks under Read Committed, `NOT VALID` + `VALIDATE` migrations, xmin-horizon blockers, the RLS fail-closed behaviour of `current_setting`, and PITR to a separate instance followed by copying the rows back.

PostgreSQL 18 claims match FACTS.md and what I know of the release: `uuidv7()`, virtual generated columns as the default, skip scan, `OLD`/`NEW` in `RETURNING`, BUFFERS on by default in EXPLAIN ANALYZE, fractional actual rows, `Index Searches`, MD5 deprecation, `idle_replication_slot_timeout`, `autovacuum_vacuum_max_threshold`, stats kept across `pg_upgrade`, and `NOT NULL ... NOT VALID`.

The difficulty spread is exactly on target (11/11/7/3), with 7 MCQs. The Bangla is natural, contemporary and technically faithful, keeps the tech terms in Latin script, and carries the same caveats as the English. Only a few word choices are slightly literal.

Weaknesses are minor:
- All 7 MCQs have no follow-ups.
- Three advanced questions are labelled `market=international` without justification.
- A few small imprecisions: DELETE "updates" indexes, the fillfactor caveat, and the FK unique-index wording.
- PG18 asynchronous I/O (listed in COVERAGE.md) is not covered at all.
- There is some overlap between the two wallet/concurrency questions (pg-019, pg-023).

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| PG-C01 | pg-005 | both | P3 | Technical precision | The write-cost sentence says every DELETE updates the index. A DELETE only sets xmax in the heap, and dead index entries are removed later by VACUUM. A non-HOT UPDATE of a *non-indexed* column also adds entries to every index, so the sentence is imprecise both ways. | "every `INSERT`, `DELETE`, and `UPDATE` of an indexed column must also update the index" | "every INSERT, and every UPDATE that can't be done as a HOT update, must add index entries; dead entries are cleaned up later by VACUUM" | High | Text no longer claims DELETE writes index entries synchronously |
| PG-C02 | pg-002 | both | P3 | Technical precision | Option B and the answer say the referenced columns must be a PK or unique *constraint*. PostgreSQL also accepts a non-partial unique *index*. This doesn't change the key. | "must have a primary key or unique constraint (so it is indexed)" | Add "(or a non-partial unique index)" in the explanation | High | Matches the docs wording in ddl-constraints (Foreign Keys) |
| PG-C03 | pg-029 | both | P3 | Missing caveat | Recommends lowering `fillfactor` as a fix for an already-bloated table. The new fillfactor only applies to pages written afterwards; existing pages change only after a rewrite (`pg_repack` / `VACUUM FULL`). | "Lower `fillfactor` so more updates are HOT." | Add: "takes effect for new pages, or after the pg_repack/VACUUM FULL rewrite" | High | Caveat present in EN and BN |
| PG-C04 | pg-024 | both | P3 | Clarity | "~550k rows" appears without saying what it refers to. It is the join-row estimate (it matches `rows=554310` in the extra code), but the sentence reads as if it were the payments estimate, which should be ~200k. | "With correct estimates (~550k rows), the planner picks a hash join instead." | "With correct estimates (~200k payments, ~550k joined rows) …" | Medium | Numbers are consistent with the plan shown |
| PG-C05 | pg-002, pg-003, pg-008, pg-009, pg-015, pg-020, pg-028 | both | P3 | Question quality | All MCQs have empty follow-ups (`FOLLOW-UPS: []`). The authoring guide asks for 1–3, and natural follow-ups exist (e.g. pg-020 "how do you recover jobs from crashed workers?", pg-028 "how would you see skip scan in EXPLAIN?"). | "FOLLOW-UPS: []" | Add 1–2 follow-ups per MCQ | High | Every MCQ has ≥1 follow-up |
| PG-C06 | pg-030, pg-031, pg-032 | — | P3 | market label | `market=international`. This is consistent with the FACTS.md policy ("Use `international` for deeper system-design / large-scale … questions"), so it is not an error. However, if the app filters by market, BD learners targeting senior roles at local product companies would not see these three. The label also differs from the PG MCQs, which are `both`, while the equivalent SQL fundamentals MCQs are tagged `bangladesh`. | "market=international prio=medium" (pg-030) | Optional: use `both` for these three, since incident response and multi-tenancy are not international-only | Low | Product decision; check the filter UX |
| PG-C07 | (category) | — | P2 | Coverage gap | COVERAGE.md lists "PostgreSQL 18 features (… AIO)". No question or explanation mentions the asynchronous I/O subsystem (`io_method`); a grep for `io_method`/`AIO` finds nothing. | COVERAGE: "PostgreSQL 18 features (uuidv7, virtual generated columns, skip scan, OLD/NEW RETURNING, AIO)" | Add a short mention, e.g. in pg-029/pg-031 explanation or a "what's new in PG18" MCQ: `io_method` (`worker` default, `io_uring` on Linux, `sync`) speeds up seq scans, bitmap heap scans and vacuum reads | High | AIO mentioned with correct GUC name and status |
| PG-C08 | pg-019, pg-023 | both | P3 | Redundancy | Both are wallet/withdrawal concurrency scenarios. They share the conditional `UPDATE ... WHERE balance >= amount`, `CHECK (balance >= 0)`, the idempotency key and `40001` retries. pg-023 extends pg-019 (deadlock ordering, hot rows, write skew), so this is acceptable, but the overlap is noticeable. | pg-019 "`UPDATE ... SET balance = balance - $1 WHERE user_id = $2 AND balance >= $1`"; pg-023 "`UPDATE accounts SET balance = balance - 500.00 WHERE id = 42 AND balance >= 500.00`" | Optionally change the pg-019 domain (e.g. inventory/stock decrement or seat booking) | Medium | Scenarios differ in domain |
| PG-C09 | pg-012 | BN | P3 | BN meaning drift | "লুকানো" means "hidden". The point is that the timestamp is *readable* and therefore leaks the creation time, so "hidden" contradicts the privacy warning that follows. | "UUIDv7-এর ভেতরে তৈরির সময় লুকানো থাকে" | "UUIDv7-এর ভেতরে তৈরির সময় encode করা থাকে (বাইরে থেকে পড়া যায়)" | High | BN conveys "embedded and readable" |
| PG-C10 | pg-002, pg-003, pg-008, pg-009, pg-015, pg-020 | BN | P3 | BN phrasing | "লোভনীয় ভুল উত্তর" is a literal rendering of "tempting wrong answer". লোভনীয় usually means appetising or greedy-tempting, which reads oddly here. | "লোভনীয় ভুল উত্তর হলো `money`" (pg-003); "`NOWAIT` হলো লোভনীয় ভুল উত্তর" (pg-020) | "সবচেয়ে বিভ্রান্তিকর ভুল option" / "যে ভুল উত্তরটায় সবাই আটকে যায়" | Medium | Consistent natural phrase across MCQs |
| PG-C11 | pg-024, pg-021, others | BN | P3 | BN consistency | Bangla and Latin numerals are mixed inconsistently, sometimes within one question. | pg-021 "30 pod × 20 = সর্বোচ্চ 600 connection"; pg-024 "**২,০০,০০০**" alongside "`rows=1`", "cost 13" | Pick one convention (e.g. Latin digits next to code/metrics, Bangla digits in prose) and apply it consistently | Medium | Style check |
| PG-C12 | pg-022 | both | P3 | Precision | Says `ON CONFLICT`/`EXCLUDED`/`RETURNING` are "PostgreSQL syntax". SQLite supports the same `ON CONFLICT ... DO UPDATE` + `excluded` + `RETURNING`, and MariaDB has `RETURNING`. "PostgreSQL-specific" slightly overstates it. | "`ON CONFLICT`, `EXCLUDED`, and `RETURNING` are PostgreSQL syntax (MySQL uses `ON DUPLICATE KEY UPDATE`)." | "non-standard (PostgreSQL syntax, also adopted by SQLite); MySQL uses ON DUPLICATE KEY UPDATE; the standard is MERGE" | High | Ran the same statement in sqlite3 3.51 and it works |
| PG-C13 | pg-014 | both | P3 | Missing caveat | Recommends `CREATE UNIQUE INDEX CONCURRENTLY ... (lower(email))` without warning that it fails, leaving an INVALID index, if existing emails already collide case-insensitively. | "If emails must be unique case-insensitively, make it a `UNIQUE` expression index" | Add: "first check `GROUP BY lower(email) HAVING count(*) > 1` and resolve duplicates" | High | Caveat present |

## Per-question notes
- pg-001 — OK (accurate 1NF/junction table answer, with the array + GIN alternative). Scores: acc 10, depth 9, BN 9, EN 9.
- pg-002 — issues: PG-C02, PG-C05, PG-C10. Scores: acc 9, depth 9, BN 8, EN 9.
- pg-003 — issues: PG-C05, PG-C10. Scores: acc 10, depth 9, BN 8, EN 9. The `money`/`lc_monetary` explanation and float output are correct.
- pg-004 — OK (NULLS NOT DISTINCT PG15, EXCLUDE + btree_gist, deferrable list, PG18 WITHOUT OVERLAPS all correct).
- pg-005 — issues: PG-C01. Scores: acc 8, depth 8, BN 9, EN 9.
- pg-006 — OK (the aborted-transaction state, COMMIT acting as rollback, and the pool gotcha are all correct).
- pg-007 — OK.
- pg-008 — issues: PG-C05, PG-C10. Scores: acc 10, depth 8, BN 8, EN 9.
- pg-009 — issues: PG-C05, PG-C10. Scores: acc 10, depth 9, BN 8, EN 9. PG18 BUFFERS default and fractional rows are correct.
- pg-010 — OK (expected output `{"a": 3, "b": 1}` is correct: jsonb dedups with last-wins and sorts keys).
- pg-011 — OK.
- pg-012 — issues: PG-C09. Scores: acc 10, depth 10, BN 8, EN 9.
- pg-013 — OK.
- pg-014 — issues: PG-C13. Scores: acc 9, depth 10, BN 9, EN 9. The expression-index index-only-scan nuance is correct.
- pg-015 — issues: PG-C05, PG-C10. Scores: acc 10, depth 9, BN 8, EN 9.
- pg-016 — OK (expected output verified by reasoning: ordering, NULL for has_5g, NULLS LAST).
- pg-017 — OK (output reproduced in sqlite with the ROW_NUMBER equivalent; coalesce → `0` matches PG numeric display).
- pg-018 — OK (MD5 deprecation PG18, SCRAM default PG14, PG15 public schema, and FORCE RLS are all correct).
- pg-019 — issues: PG-C08. Scores: acc 10, depth 10, BN 9, EN 9.
- pg-020 — issues: PG-C05, PG-C10. Scores: acc 10, depth 9, BN 8, EN 9. The no-lock double-processing explanation is correct.
- pg-021 — OK.
- pg-022 — issues: PG-C12. Scores: acc 9, depth 10, BN 9, EN 9. Output verified in sqlite.
- pg-023 — issues: PG-C08. Scores: acc 10, depth 10, BN 9, EN 9.
- pg-024 — issues: PG-C04, PG-C11. Scores: acc 9, depth 10, BN 8, EN 9.
- pg-025 — OK (lock queue, NOT VALID/VALIDATE, CHECK→SET NOT NULL, PG18 NOT NULL NOT VALID all correct).
- pg-026 — OK.
- pg-027 — OK.
- pg-028 — issues: PG-C05. Scores: acc 10, depth 9, BN 9, EN 9.
- pg-029 — issues: PG-C03. Scores: acc 9, depth 10, BN 9, EN 9.
- pg-030 — issues: PG-C06. Scores: acc 10, depth 10, BN 9, EN 9. DEFAULT partition blocking DETACH CONCURRENTLY and PG17 identity on partitioned tables are correct.
- pg-031 — issues: PG-C06. Scores: acc 10, depth 10, BN 9, EN 9.
- pg-032 — issues: PG-C06. Scores: acc 10, depth 10, BN 9, EN 9. The fail-closed `current_setting` behaviour is described accurately.

## Coverage & gaps
- Required subtopics are covered except **PG18 AIO** (PG-C07).
- **Joins** have no dedicated PostgreSQL question. They are covered thoroughly in the SQL category (sql-002, sql-019), so this is acceptable.
- **Normalization** beyond 1NF only appears as a pg-001 follow-up. It is covered in sql-011.
- **Locks & deadlocks** are covered inside pg-023/pg-025. A short question on the lock-mode matrix or `pg_locks` could help mid-level candidates, but this is optional.
- **Recursive CTEs** are in SQL (sql-023), not in PostgreSQL. That is fine.
- **Redundancy:** pg-019 vs pg-023 (PG-C08). pg-011 vs pg-026 are complementary (logical vs PITR), so that pair is fine.
- **Difficulty:** labels are appropriate. pg-009 (EXPLAIN ANALYZE executes) and pg-007 (MVCC) as easy is reasonable.

## Needs verification
- pg-009 / pg-024: "In PostgreSQL 18 … actual row counts are shown with decimals (e.g. `rows=1.00`)" and the `Index Searches:` line in EXPLAIN ANALYZE. I believe both are PG18 changes; confirm against the release-18 notes.
- pg-025: "PG18 can also add a `NOT NULL` constraint directly as `NOT VALID`". I believe this is correct (PG18); confirm the syntax `ALTER TABLE ... ADD CONSTRAINT ... NOT NULL col NOT VALID`.
- pg-029: `autovacuum_vacuum_max_threshold` is new in PG18 (consistent with my knowledge; default 100,000,000).
- pg-027: `idle_replication_slot_timeout` is PG18; "sequence values aren't replicated as of PG18" is correct for PG18. PG19 (beta) may add sequence sync, so re-check when 19 is GA.
- pg-018: "it warns when you set MD5 passwords" (`md5_password_warnings`, PG18).
- pg-021: PgBouncer `max_prepared_statements` (since 1.21). This is correct, but "current releases" is unpinned.

## Verified
- `sqlite3` 3.51.0 (SCRATCH/run): reproduced the pg-017 result with a portable ROW_NUMBER() rewrite. Rahim 104/2026-10-02/2500/3/4500, Karim 107/950/2/1400, Nadia 106/700/2/1000, Sumi -/0/0 all match. (DISTINCT ON is PG-only, so the window logic was checked instead.)
- `sqlite3`: ran the pg-022 `INSERT ... ON CONFLICT (sku) DO UPDATE SET qty = inventory.qty + excluded.qty RETURNING sku, qty`. Output TSHIRT-M 30, JEANS-32 5, CAP-RED 12 matches the expected output. It also shows the syntax is not PostgreSQL-only (PG-C12).
- Checked by reasoning (no PG installed): pg-010 jsonb output, pg-016 output, pg-014 plan estimate (rows=500 = 0.5% default selectivity of 100k), pg-030 arithmetic (20M/86400 ≈ 231/s).
- No web fetches used.
