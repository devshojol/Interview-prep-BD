# Vector Databases content audit

Coverage: 32/32 questions reviewed — vec-001, vec-002, vec-003, vec-004, vec-005, vec-006, vec-007, vec-008, vec-009, vec-010, vec-011, vec-012, vec-013, vec-014, vec-015, vec-016, vec-017, vec-018, vec-019, vec-020, vec-021, vec-022, vec-023, vec-024, vec-025, vec-026, vec-027, vec-028, vec-029, vec-030, vec-031, vec-032.

Distribution: easy 11 (001–011), medium 11 (012–022), hard 7 (023–029), extreme 3 (030–032). MCQs 8 (002, 006, 009, 010, 011, 012, 020, 025).

## Category summary
Excellent, technically careful category. I recomputed every piece of similarity, distance and storage arithmetic with Python, and re-ran both JavaScript examples with Node. Everything is correct, including:
- cosine/L2/dot rankings (vec-004, vec-012);
- the pgvector query outputs (vec-013);
- RRF scores (vec-016) and recall/MRR (vec-017);
- storage sizing (vec-011, vec-027, vec-030);
- the chunker count (vec-007).

pgvector facts match the README: `4×dims+8` bytes, HNSW defaults 16/64/40, the IVFFlat lists/probes guidance, the 2,000/4,000-dimension index limits, iterative scans with `max_scan_tuples` 20,000, and the halfvec/binary_quantize syntax. The content is product-neutral and practical, with strong Bangla-market specifics (dari "।" sentence splitting, Banglish, bKash tickets) that are useful rather than filler.

Main weaknesses are minor:
- The easy metadata-filter MCQ presents "filter + vector in one query" as a full fix without noting that pgvector HNSW still post-filters (the category itself explains this in 013/025).
- "Recall@k" is defined as hit rate.
- One small arithmetic inconsistency in vec-025.
- References lean on non-official sources (Wikipedia, Pinecone learn pages, HF blog, arXiv), contrary to AUTHORING §8; acceptable for concepts, but the Pinecone pages are vendor content in a product-neutral category.
- Two code blocks mix SQL and JS under `javascript`.

Bangla is natural and complete, with a handful of literal phrasings. Coverage of COVERAGE.md is complete. There is some intended repetition of the post-filtering / operator-class rules across 010/013/018/025/026.

Scores: Technical accuracy 9.5 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8.5 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| VEC-C01 | vec-010 | both | P2 | Misleading simplification | The keyed answer and its extra SQL imply that putting `WHERE price < 2000` in the same pgvector query avoids the "too few results" problem of option C. With an HNSW index, pgvector applies the WHERE after the index scan (as vec-013/025 explain), so the query can still return fewer than 10 rows unless iterative scans are on or the planner picks a B-tree path. | Option B "applying both in the same query"; extra code `WHERE price < 2000 AND in_stock ... ORDER BY embedding <=> $1 LIMIT 10` with no `hnsw.iterative_scan` | Add one line under the extra code: "with an HNSW index, also `SET hnsw.iterative_scan = relaxed_order` (pgvector 0.8+) or raise `ef_search`; see vec-025". Optionally add that line to the SQL. | High | The extra code/explanation mentions iterative scan, consistent with vec-013/025. |
| VEC-C02 | vec-017 (also used in 015, 020, 023, 028) | both | P3 | Definition precision | "Recall@k" is defined as the share of queries with any relevant doc in the top k. That is hit rate / success@k. Standard recall@k is the fraction of a query's relevant docs found in the top k, averaged. They coincide only with one relevant doc per query (true in the example). | "**Recall@k:** the share of queries where a relevant document appears in the top k." | "Recall@k = relevant docs retrieved in top k ÷ all relevant docs for that query, averaged; with one relevant doc per query this equals hit rate@k." | High | Definition matches IR textbooks; the example values remain 0.67/0.44. |
| VEC-C03 | vec-025 | both | P3 | Internal arithmetic | Using the explanation's own rule (ef_search 40 × filter selectivity), a 4% tenant yields about 1.6 expected matches, yet the question says it returns 5. That's not impossible (tenant docs may cluster near the query) but it's inconsistent with the cited arithmetic. | "Tenant 7 owns about 4%... returns only 5"; "with the default `ef_search` of 40 and a filter matching 10% of rows, you get about 4 matches" | Change to "about 10%" or "returns only 2". | High | 40 × selectivity ≈ the stated returned count. |
| VEC-C04 | vec-001, 003, 004, 005, 006, 007, 008, 009, 010, 012, 014, 015, 017, 020, 021, 028, 032 | both | P3 | References | AUTHORING §8 requires official docs only. Many refs are Wikipedia, vendor learning pages (Pinecone "What is a vector database?", "Chunking strategies") or a Hugging Face blog. Papers (arXiv) are defensible. Pinecone pages in a product-neutral category look like vendor endorsement. | e.g. `https://www.pinecone.io/learn/vector-database/`; `https://en.wikipedia.org/wiki/Cosine_similarity` | Prefer the pgvector README, PostgreSQL docs, Redis/Qdrant/Weaviate official docs, model cards and original papers. Keep at most one vendor page, or balance them. | Medium (policy interpretation) | Refs comply with the AUTHORING §8 domain list or are primary papers. |
| VEC-C05 | vec-018 (code + extra), vec-026 (extra) | both | P3 | Code presentation | SQL (`-- migration.sql`, `CREATE INDEX`, `ALTER TABLE`, `CREATE POLICY`) and JS are in one block labelled `javascript`. Highlighting is wrong, and `--` lines are invalid JS if copied. | `### CODE (javascript)` starting with `-- migration.sql` | Split into a `sql` block plus a `javascript` block (use `extra` for the second). | High | Each block parses in its declared language. |
| VEC-C06 | vec-018 (fixed version) | both | P3 | Code correctness | `ADD COLUMN embedding_model text NOT NULL DEFAULT 'kb-embed-v2'` stamps every existing row as v2. That includes any rows embedded with v1 before the refactor, which hides exactly the mismatch the column is meant to catch. | `ALTER TABLE kb_chunks ADD COLUMN embedding_model text NOT NULL DEFAULT 'kb-embed-v2';` | Add the column nullable (or `'unknown'`), set it explicitly at ingestion, and backfill/re-embed rows of unknown provenance. | Medium | Rows' model label reflects how they were actually embedded. |
| VEC-C07 | vec-011 | EN | P3 | Market label | `market=bangladesh` on a storage-arithmetic MCQ has no support in the FACTS research notes. | `vec-011 | ... | market=bangladesh` | Use `both`. | Medium | Label justified. |
| VEC-C08 | vec-014, vec-032, vec-031 | BN | P3 | Bangla phrasing / style rule | Literal or awkward choices, and one tech term in Bangla script (AUTHORING says Latin). | 014: "লোভীভাবে query-র দিকে লাফিয়ে এগোয়"; 032: "অনাথ আর duplicate chunk", "সংখ্যা দিয়ে পুনরুৎপাদন করো"; 031: "তিনটা মডেল", "একটাই মডেল" | 014: "greedy-ভাবে query-র সবচেয়ে কাছের দিকে এগোয়"; 032: "orphan আর duplicate chunk", "সংখ্যা দিয়ে reproduce করো"; 031: "তিনটা isolation model". | Medium | Native BN reviewer reads them as natural; no Bangla-script tech terms. |
| VEC-C09 | vec-030 | EN/BN | P3 | Realism | The latency budget assumes "rerank the top ~200" in ~50 ms at 2,000 QPS. That's realistic for a lightweight learning-to-rank/GBDT model, not for a cross-encoder (which is what "rerank" means elsewhere in this bank). | "rerank the top ~200 with a model that also uses business signals"; "rerank ~50 ms" | Say "a lightweight learning-to-rank model (e.g. GBDT on features) on ~200, optionally a cross-encoder on the top ~20". | Medium | Budget states which reranker type it assumes. |
| VEC-C10 | vec-002, 006, 009, 010, 011, 012, 020, 025 | both | P3 | Weak follow-ups | All MCQs have `FOLLOW-UPS: []`, though AUTHORING asks for 1–3. | `FOLLOW-UPS: []` | Add 1–2 each (e.g. 012: "Which pgvector operator class matches a model trained for dot product?"). | High | Every question has ≥1 follow-up. |

## Per-question notes
- vec-001 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9 (dims 384/768/1536 and output (3, 384) correct)
- vec-002 — issues: VEC-C10; acc 10 / depth 9 / BN 9 / EN 9 (pgvector error strings correct)
- vec-003 — issues: VEC-C04; acc 10 / depth 8 / BN 9 / EN 9
- vec-004 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9 (output 1.0 / 0.0 / 0.707 verified)
- vec-005 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9
- vec-006 — issues: VEC-C04, VEC-C10; acc 10 / depth 9 / BN 9 / EN 9
- vec-007 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9 (Node: 3 chunks w1-w300, w251-w550, w501-w700)
- vec-008 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9
- vec-009 — issues: VEC-C04, VEC-C10; acc 10 / depth 8 / BN 9 / EN 9
- vec-010 — issues: VEC-C01, VEC-C04, VEC-C10; acc 8 / depth 8 / BN 9 / EN 9
- vec-011 — issues: VEC-C07, VEC-C10; acc 10 / depth 9 / BN 9 / EN 9 (6,144 / 6,152 B verified)
- vec-012 — issues: VEC-C04, VEC-C10; acc 10 / depth 10 / BN 9 / EN 9 (1.0 vs 0.707; L2 4.243 vs 1; dot 8 vs 1; unit-vector identity verified)
- vec-013 — OK (0.994 / 0.963 / 0.768; Jamdani 0.983; panjabi 0.216 — verified in float64 and float32)
- vec-014 — issues: VEC-C04, VEC-C08; acc 10 / depth 9 / BN 8 / EN 9
- vec-015 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9
- vec-016 — OK (Node output matches exactly: 0.03252 / 0.03227 / 0.01613)
- vec-017 — issues: VEC-C02, VEC-C04; acc 9 / depth 9 / BN 9 / EN 9 (0.67 / 0.44 verified)
- vec-018 — issues: VEC-C05, VEC-C06; acc 9 / depth 9 / BN 9 / EN 9
- vec-019 — OK
- vec-020 — issues: VEC-C04, VEC-C10; acc 10 / depth 9 / BN 9 / EN 9
- vec-021 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9
- vec-022 — OK (OWASP LLM08:2025 correct)
- vec-023 — OK
- vec-024 — OK (2,000 / 4,000 dimension limits and CONCURRENTLY correct)
- vec-025 — issues: VEC-C03, VEC-C10; acc 9 / depth 9 / BN 9 / EN 9
- vec-026 — issues: VEC-C05; acc 10 / depth 10 / BN 9 / EN 9 (RLS/FORCE/BYPASSRLS caveats correct)
- vec-027 — OK (61.5 / 30.8 / 20.6 / 1.9 GB and ~3× verified; halfvec/binary_quantize SQL matches README)
- vec-028 — issues: VEC-C04; acc 10 / depth 9 / BN 9 / EN 9
- vec-029 — OK
- vec-030 — issues: VEC-C09; acc 9 / depth 10 / BN 9 / EN 9 (15.4 / 7.72 GB verified)
- vec-031 — issues: VEC-C08; acc 10 / depth 10 / BN 8 / EN 9 (partition DDL valid on PG 17+, identity on partitioned table)
- vec-032 — issues: VEC-C04, VEC-C08; acc 10 / depth 10 / BN 8 / EN 9

## Coverage & gaps
- All COVERAGE.md subtopics are covered: embeddings, dimensions, similarity search, cosine, L2/dot, ANN (HNSW/IVF), semantic search, metadata filtering (pre/post), chunking, indexing, vs relational (pgvector), vs full-text, hybrid/RRF, RAG, retrieval quality/reranking, model changes, privacy, production use cases.
- Easy questions have no heavy math, as required.
- Redundancy: the post-filtering and operator-class rules recur in 010/013/018/025/026/030. That's fine pedagogically, but 025 and 013 overlap noticeably.
- Optional gaps: sparse vectors / learned sparse (SPLADE) appear only in passing; there is nothing on upsert/delete behaviour of HNSW (index bloat, VACUUM), which is only a follow-up in vec-014.
- Cross-category: redis-010 (Vector Sets) and vec-021/029 (Redis as a vector option) are consistent with each other.

## Needs verification
- vec-016: "Qdrant's documentation ... uses a smaller constant" for RRF k. Not checked.
- vec-022: "Bangladesh's own rules for local users" is vague. If a specific BD data-protection law is now in force, name it; otherwise keep it generic.
- pgvector 0.8.7 version label (FACTS) — not re-checked; all syntax used exists in 0.8.x.

## Verified
- python3 -I SCRATCH/run/vec_math.py:
  - cosine examples (vec-004): 1.0, 0.0, 0.707
  - vec-012 rankings and the unit-vector identity |a−b|² = 2−2a·b
  - vec-013 similarities in float64 and float32: 0.994, 0.963, 0.983, 0.216, 0.768
  - vec-011: 6144 / 6152
  - vec-027: 61.52 / 30.8 / 20.56 / 1.92 GB, ratio 2.99
  - vec-030: 15.4 / 7.72 GB
  - vec-016 RRF: 0.03252 / 0.03227 / 0.01613 / 0.01587
  - vec-017: 0.67 / 0.44
  - vec-025: 40 × 0.04 = 1.6
- node SCRATCH/run/node_checks.mjs:
  - vec-007 → `3` chunks [w1-w300, w251-w550, w501-w700]
  - vec-016 console.log output identical to the expected output, including the multi-line formatting
