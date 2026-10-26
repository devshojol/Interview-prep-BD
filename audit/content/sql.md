# SQL content audit
Coverage: 32 of 32 questions reviewed — sql-001, sql-002, sql-003, sql-004, sql-005, sql-006, sql-007, sql-008, sql-009, sql-010, sql-011, sql-012, sql-013, sql-014, sql-015, sql-016, sql-017, sql-018, sql-019, sql-020, sql-021, sql-022, sql-023, sql-024, sql-025, sql-026, sql-027, sql-028, sql-029, sql-030, sql-031, sql-032.

## Category summary
This is an excellent practical SQL category. Every query and output question was executed in sqlite3 (3.51.0), adapted only where the dialect required it (to_char→strftime, date−int→date()). All expected outputs matched, apart from PostgreSQL-specific numeric formatting such as `3000.00` vs `3000`, which the content itself discloses. All MCQ keys are correct, with plausible distractors, and the explanations name the tempting wrong option correctly.

Strengths:
- It covers the classic interview set: second-highest salary with tie semantics, top-N per group, running totals with the RANGE/ROWS trap, the NOT IN + NULL trap, duplicates, gaps-and-islands, and keyset pagination.
- Portability is labelled consistently and accurately (MySQL/SQL Server/SQLite/Oracle differences).
- The answers carry production habits: preview DELETEs, transactions, and unique indexes to fix root causes.

The Bangla is natural and faithful, with only a few literal choices ("লোভনীয়", "অনাথ order").

Weaknesses are small:
- One misleading claim about `USING` joins.
- A few dialect over-generalisations ("works everywhere" next to `FETCH FIRST`, SQL Server MAXRECURSION "stops").
- A naming inconsistency (colour/color) and a NULL-uniqueness gap in the marketplace schema.
- Empty follow-ups on all 7 MCQs.
- Non-official references in sql-011 (Wikipedia).
- One unsupported Bangladesh-market claim (sql-028).
- A stale "Node.js 24 LTS" label (sql-021).
- Set operations (UNION/INTERSECT/EXCEPT) have no question.
- There is noticeable cross-category overlap with PostgreSQL (transactions/transfer, isolation, sargability).

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 10 | Bangla quality 8 | English quality 9 | Examples & code 10 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| SQL-C01 | sql-002 | both | P2 | Technical accuracy | The claim is wrong for `USING`. `USING (col)` names its join columns explicitly, so adding a same-named column elsewhere does not change it. Only `NATURAL JOIN` (which joins on *all* common column names) silently changes. The real `USING` caveats are different: the merged output column, and needing to qualify it. | "Avoid `NATURAL JOIN` / `USING` on wide schemas: adding a column with the same name can silently change the join." / BN "`NATURAL JOIN` / `USING` এড়িয়ে চলো: একই নামের নতুন column যোগ হলে join নীরবে বদলে যেতে পারে।" | "Avoid `NATURAL JOIN`: it joins on every same-named column, so adding e.g. `created_at` to both tables silently changes the join. `USING (id)` is explicit and safe, but merges the join column into one." | High | Text distinguishes NATURAL from USING in EN and BN |
| SQL-C02 | sql-002 | both | P3 | Technical precision | The MySQL FULL OUTER JOIN emulation uses `UNION`, which removes legitimate duplicate result rows. The robust form is `LEFT JOIN … UNION ALL … RIGHT JOIN … WHERE left.key IS NULL`. | "emulate it with a `LEFT JOIN ... UNION ... RIGHT JOIN`" | Mention the `UNION ALL` + anti-join form (or the caveat) | High | Explanation notes the duplicate-removal caveat |
| SQL-C03 | sql-026 | both | P3 | Dialect accuracy | The "works everywhere" fallback uses `FETCH FIRST 3 ROWS ONLY`, which MySQL and SQLite do not support (SQL Server also needs `OFFSET 0 ROWS`, which is noted). The WHERE expansion is portable; the paging clause is not. | "-- equivalent without row values (works everywhere, e.g. SQL Server) ... FETCH FIRST 3 ROWS ONLY;" | "the WHERE form works everywhere; use LIMIT 3 in MySQL/SQLite, OFFSET 0 ROWS FETCH NEXT 3 ROWS ONLY in SQL Server" | High | Comment no longer implies FETCH FIRST works in MySQL/SQLite |
| SQL-C04 | sql-023 | both | P3 | Technical precision | SQL Server does not gracefully "stop" at MAXRECURSION. The statement is aborted with an error (Msg 530) once the limit is exceeded, so it isn't a cycle *guard* that returns partial results. | "SQL Server stops at `MAXRECURSION` (default 100)" / BN "SQL Server `MAXRECURSION`-এ (default 100) থেমে যায়" | "SQL Server aborts the query with an error after `MAXRECURSION` levels (default 100)" | High | Wording says "fails/aborts" |
| SQL-C05 | sql-032 | both | P3 | Design gap / consistency | (a) `UNIQUE (product_id, size, color)` with nullable `size`/`color`: NULLs are distinct, so a product without sizes/colours can get duplicate variant rows. Mention `NULLS NOT DISTINCT` (PG15+), or make the columns NOT NULL with a default such as `''`/'one-size'. (b) The text says `colour` but the code column is `color`. | code: "`size VARCHAR(10), color VARCHAR(30) ... UNIQUE (product_id, size, color)`"; answer: "`UNIQUE (product_id, size, colour)`" | Fix the spelling to match the code, and add the NULL caveat | High | Text and code identifiers match; caveat present |
| SQL-C06 | sql-001, sql-005, sql-006, sql-009, sql-011, sql-019, sql-025 | both | P3 | Question quality | All MCQs have `FOLLOW-UPS: []`. Good follow-ups already appear in the explanations (e.g. sql-025 LAST_VALUE trap, sql-009 TRUNCATE rollback per DB). | "FOLLOW-UPS: []" | Add 1–2 follow-ups each | High | Every MCQ has ≥1 follow-up |
| SQL-C07 | sql-011 | — | P3 | References | The references are Wikipedia and a Microsoft Office/Access troubleshooting article. Neither is on the AUTHORING §8 official list, and the Access KB is an odd source for SQL normalization. | REFS: "Wikipedia — Database normalization", "Microsoft Learn — Database normalization description (office/troubleshoot/access)" | Replace with PostgreSQL docs (ddl-constraints / tutorial) or keep only one vendor doc; Wikipedia is not official | High | Refs from the allowed list |
| SQL-C08 | sql-028 | both | P3 | Unsupported BD-market claim | A generalisation about Bangladeshi banking/ERP stacks without a source (brief item 9/10). It is plausible, but not supported by FACTS.md research notes. | "In the Bangladesh market, legacy banking/ERP systems often keep heavy logic in Oracle/SQL Server procedures" / BN "বাংলাদেশের বাজারে legacy banking/ERP system প্রায়ই ভারী logic Oracle/SQL Server procedure-এ রাখে" | Rephrase neutrally: "Many legacy banking/ERP systems keep heavy logic in Oracle/SQL Server procedures; reading and migrating them is a valuable skill." | Medium | No unsourced market claim |
| SQL-C09 | sql-007 | both | P3 | Frequency claim | "a common viva definition" / "viva-তে প্রায়ই জিজ্ঞেস করা" asserts frequency. AUTHORING §7 says not to claim how often a question is asked. | "— a common viva definition." | "— a definition worth knowing for written/viva rounds." | Medium | No frequency wording |
| SQL-C10 | sql-021 | — | P3 | Version currency | The version label says "Node.js 24 LTS". Per FACTS.md, Node 24 entered Maintenance on 2026-10-20 and Node 26 becomes Active LTS on 2026-10-28, so this is stale or about to be. The content itself is version-independent. | "ver=node-postgres 8.x on Node.js 24 LTS; Express 5.x" | "node-postgres 8.x; Node.js 24/26 LTS; Express 5.x" | High | Label updated |
| SQL-C11 | sql-005 | both | P3 | Technical precision | Overgeneralisation: `ARRAY_AGG` (SQL:2008) keeps NULLs, and `JSON_ARRAYAGG` can (`NULL ON NULL`). The statement is true for the numeric aggregates the question is about. | "All standard aggregates except `COUNT(*)` ignore NULLs." | "All the common numeric aggregates (SUM, AVG, MIN, MAX, COUNT(col)) ignore NULLs; COUNT(*) counts rows" | High | Wording scoped |
| SQL-C12 | sql-002, sql-001, sql-005, sql-006, sql-009, sql-011, sql-019, sql-025 | BN | P3 | BN phrasing | Same literal "tempting" rendering as in PostgreSQL. "লোভনীয়" (appetising/greedy-tempting) sounds odd for a distractor. | sql-006 "লোভনীয় উত্তর 3"; sql-009 "Option D হলো লোভনীয় ফাঁদ" | "সবচেয়ে বিভ্রান্তিকর option" / "যেটায় অনেকে ভুল করে" | Medium | Consistent natural phrase |
| SQL-C13 | sql-019 | BN | P3 | BN phrasing | "অনাথ" means an orphaned *child*. For data, Bangladeshi devs say "orphan" or describe it. | "অনাথ order 13 NULL নাম-সহ যোগ হয়" | "কোনো customer-এর সাথে না-মেলা (orphan) order 13" | High | Natural wording |
| SQL-C14 | sql-030 | BN | P3 | BN — code translated | A Bangla word appears inside a code-like expression, against the rule "Never translate code". | "`login_date <> LAG(login_date) + 1 দিন` হলে নতুন island-এর flag দাও" | "`login_date <> LAG(login_date) + 1` (PostgreSQL-এ date + integer = পরের দিন) হলে…" | High | Code token not translated |
| SQL-C15 | sql-024 | — | P3 | Difficulty label | Monthly aggregation + LAG + NULLIF is a standard mid-level reporting query. "hard" overstates it compared with sql-013/sql-014 (medium). The missing-month insight is good but doesn't make it hard. | "sql-024 \| LAG & Month-over-Month Growth \| hard \| query" | Relabel `medium`, or add a harder requirement (fill missing months with generate_series/recursive calendar in the reference solution) | Medium | Difficulty consistent with peers |
| SQL-C16 | (category) | — | P3 | Coverage gap | No question covers set operations (`UNION` vs `UNION ALL`, `INTERSECT`, `EXCEPT`). This is a frequent fundamentals topic (dedup cost, column compatibility), and it only appears as a follow-up in sql-016 and a comment in sql-023. Basic filtering operators (`IN`, `BETWEEN`, `LIKE`, `CASE`) appear only incidentally. | sql-016 follow-up "Is `EXCEPT` another way to do this?" | Add an easy MCQ/query on UNION vs UNION ALL (and EXCEPT for anti-joins) | Medium | Question exists |
| SQL-C17 | sql-010 ↔ pg-006/pg-019/pg-023; sql-029 ↔ pg-008/pg-023; sql-020 ↔ pg-014; sql-017 ↔ pg-014 | both | P3 | Cross-category redundancy | Several pairs repeat the same teaching points across SQL and PostgreSQL: the money-transfer with `AND balance >= amount` guard (sql-010, pg-019, pg-023, sql-032), isolation defaults and write skew (sql-029, pg-008, pg-023), function-on-column sargability plus a `LOWER(email)` unique index (sql-020, sql-017, pg-014). Each is individually fine, but a learner doing both categories sees heavy repetition. | sql-010 "`WHERE id = 1 AND balance >= 500`"; pg-019 "`WHERE user_id = $2 AND balance >= $1`" | Keep SQL portable and conceptual and PostgreSQL engine-specific. Swap one of the transfer scenarios for another domain (seat booking, coupon redemption limit) | Medium | Distinct scenarios per category |
| SQL-C18 | sql-021 | — | P3 | References | The node-postgres link points to the GitHub repo. The official docs site is node-postgres.com (queries/parameterized queries page), which better supports the simple vs extended protocol claim. | REFS: "node-postgres (pg) — GitHub" https://github.com/brianc/node-postgres | Use https://node-postgres.com/features/queries | Medium | Ref points to docs page |

## Per-question notes
- sql-001 — issues: SQL-C06, SQL-C12. Scores: acc 10, depth 9, BN 8, EN 9.
- sql-002 — issues: SQL-C01, SQL-C02. Scores: acc 7, depth 9, BN 9, EN 9.
- sql-003 — OK (output verified in sqlite; formatting caveat disclosed).
- sql-004 — OK (output verified).
- sql-005 — issues: SQL-C06, SQL-C11, SQL-C12. Scores: acc 9, depth 9, BN 8, EN 9. Output verified (5|3|2|433.33); the SQL Server integer AVG note is correct.
- sql-006 — issues: SQL-C06, SQL-C12. Scores: acc 10, depth 9, BN 8, EN 9. Verified 1, and 3 with IS DISTINCT FROM.
- sql-007 — issues: SQL-C09. Scores: acc 10, depth 9, BN 9, EN 9.
- sql-008 — OK (verified).
- sql-009 — issues: SQL-C06, SQL-C12. Scores: acc 10, depth 9, BN 8, EN 9.
- sql-010 — issues: SQL-C17. Scores: acc 10, depth 9, BN 9, EN 9. Crash-recovery description per engine is accurate.
- sql-011 — issues: SQL-C06, SQL-C07, SQL-C12. Scores: acc 10, depth 9, BN 8, EN 9.
- sql-012 — OK (verified; RANK/DENSE_RANK table correct).
- sql-013 — OK (verified both ROW_NUMBER and DENSE_RANK outputs).
- sql-014 — OK (verified).
- sql-015 — OK (verified).
- sql-016 — OK (verified; NOT IN returns 0 rows).
- sql-017 — issues: SQL-C17. Scores: acc 10, depth 10, BN 9, EN 9. Find + delete verified.
- sql-018 — OK (verified CASE and FILTER NULL behaviour).
- sql-019 — issues: SQL-C06, SQL-C12, SQL-C13. Scores: acc 10, depth 9, BN 7, EN 9. Verified LEFT=4, FULL=5.
- sql-020 — issues: SQL-C17. Scores: acc 10, depth 10, BN 9, EN 9.
- sql-021 — issues: SQL-C10, SQL-C18. Scores: acc 10, depth 10, BN 9, EN 9. The simple-protocol multi-statement point, the identifier allowlist and LIKE escaping are correct.
- sql-022 — OK (verified).
- sql-023 — issues: SQL-C04. Scores: acc 9, depth 10, BN 9, EN 9. Output verified.
- sql-024 — issues: SQL-C15. Scores: acc 10, depth 9, BN 9, EN 9. Output verified with strftime.
- sql-025 — issues: SQL-C06, SQL-C12. Scores: acc 10, depth 10, BN 8, EN 9. Verified 100/180/180/200.
- sql-026 — issues: SQL-C03. Scores: acc 9, depth 10, BN 9, EN 9. Output verified (row-value comparison works in sqlite).
- sql-027 — OK.
- sql-028 — issues: SQL-C08. Scores: acc 10, depth 10, BN 9, EN 9.
- sql-029 — issues: SQL-C17. Scores: acc 10, depth 10, BN 9, EN 9.
- sql-030 — issues: SQL-C14. Scores: acc 10, depth 10, BN 8, EN 9. Output verified; the CAST of row_number to INT for `date - int` is correctly handled for PostgreSQL.
- sql-031 — OK (sound plan; `market=international` is consistent with the FACTS.md policy).
- sql-032 — issues: SQL-C05. Scores: acc 9, depth 10, BN 9, EN 9.

## Coverage & gaps
- All COVERAGE.md subtopics are present: SELECT/WHERE/ORDER/GROUP/HAVING, joins, subqueries, CTEs incl. recursive, aggregates, windows, DML, constraints/keys, normalization, transactions/ACID, NULL logic, indexes, views, procedures/triggers, optimization, injection, and the classic practical queries.
- **Gap:** set operations (SQL-C16).
- **Redundancy:**
  - Inside SQL: sql-012 and sql-013 both teach ROW_NUMBER/RANK/DENSE_RANK tie semantics. They are complementary (global vs per-group), so this is acceptable.
  - sql-014 and sql-025 both teach the RANGE vs ROWS default. This is intentional reinforcement, but the second could use a different frame topic (e.g. a moving average with `RANGE BETWEEN INTERVAL '6 days' PRECEDING`).
  - Across categories: SQL-C17.
- **Difficulty:** distribution on target (11/11/7/3); sql-024 is arguably medium (SQL-C15).
- **market labels:** the SQL MCQs are `bangladesh` and the extreme questions `international`, both consistent with the FACTS.md policy. The equivalent PostgreSQL MCQs use `both`, so the labelling is inconsistent across categories (see PG-C06).

## Needs verification
- sql-029: "`READ_COMMITTED_SNAPSHOT` … is on by default in Azure SQL Database". I believe this is correct; confirm in the Microsoft docs.
- sql-006: "`IS DISTINCT FROM` … SQL Server 2022+". Correct per my knowledge (SQL Server 2022 added IS [NOT] DISTINCT FROM).
- sql-017: the MySQL error-1093 derived-table workaround relies on the derived table being materialized. With GROUP BY it is not merged, so it should work; confirm on MySQL 8.4.

## Verified
sqlite3 3.51.0 script at SCRATCH/run/sql_checks.sql. Results:

**Matched exactly, or differed only by numeric formatting:**
- sql-003: Karim 3000 / Rahim 2200 / Nadia 1200.
- sql-004: Engineering 2/83500, HR 2/56000.
- sql-005: 5|3|2|433.33.
- sql-006: 1, and 3 via IS DISTINCT FROM.
- sql-008: Joy/Mitu, Omar/Rafi.
- sql-012: Ayesha, Esha; rank table matches.
- sql-013: ROW_NUMBER and DENSE_RANK tables match.
- sql-014: running totals match.
- sql-015: Bilal, Esha, Dipu.
- sql-016: Karim, Sumi; NOT IN → 0 rows.
- sql-017: groups and post-delete table match.
- sql-018: CASE pivot and FILTER NULL match.
- sql-019: LEFT 4, FULL 5.
- sql-022: 3850/3080.
- sql-023: tree and order match.
- sql-025: 100/180/180/200.
- sql-026: 4, 3, 2.

**Dialect-adapted** (logic identical):
- sql-024: strftime instead of to_char. Output 20.0/-25.0/50.0/0.0 matches.
- sql-030: date(…, '-N days') instead of date − int. Output 3/4/1 streaks match.

**Not run** (PostgreSQL-only syntax or not a query): sql-027 (materialized views), sql-028 (PL/pgSQL), sql-031/sql-032 (DDL plus reasoning). These were reviewed by reasoning instead.

No web fetches used.
