# Vector Databases — batch 4 (vec-010, 011, 020, 021, 022, 028, 029, 032)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PGV = ("pgvector — README (GitHub)", "https://github.com/pgvector/pgvector")
PINECONE_VDB = ("Pinecone — What is a vector database?", "https://www.pinecone.io/learn/vector-database/")
QDRANT_FILTER = ("Qdrant docs — Filtering", "https://qdrant.tech/documentation/concepts/filtering/")
RERANK_PAPER = ("Nogueira & Cho — Passage Re-ranking with BERT (arXiv)", "https://arxiv.org/abs/1901.04085")
SBERT = ("Reimers & Gurevych — Sentence-BERT (arXiv)", "https://arxiv.org/abs/1908.10084")
R_VECTORS = ("Redis docs — Vector search concepts", "https://redis.io/docs/latest/develop/ai/search-and-query/vectors/")
OWASP_LLM08 = ("OWASP GenAI — LLM08:2025 Vector and Embedding Weaknesses", "https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/")
PG_RLS = ("PostgreSQL docs — Row Security Policies", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html")
WIKI_IREVAL = ("Wikipedia — Evaluation measures (information retrieval)", "https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)")
RAG_PAPER = ("Lewis et al. — Retrieval-Augmented Generation (arXiv)", "https://arxiv.org/abs/2005.11401")

QUESTIONS = [
    # ------------------------------------------------------------------ vec-010
    Q(
        id="vec-010", sub="Metadata Filtering", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["metadata-filtering", "pre-filtering", "post-filtering", "e-commerce"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""A shopper searches for "red saree under 2000 taka". Which approach gives the most reliable results?""",
        q_bn=r"""একজন ক্রেতা খুঁজলেন "red saree under 2000 taka"। কোন পদ্ধতিতে সবচেয়ে নির্ভরযোগ্য result পাওয়া যাবে?""",
        options=[
            ("Embed the whole query and rely on vector similarity alone — the model understands prices", "পুরো query embed করে শুধু vector similarity-র ওপর ভরসা করা — model দাম বোঝে"),
            ("Turn the price limit into a structured filter (`price < 2000`) and use \"red saree\" for semantic search, applying both in the same query", "দামের সীমাকে একটা structured filter (`price < 2000`) বানানো আর \"red saree\" দিয়ে semantic search করা, দুটো একই query-তে প্রয়োগ করে"),
            ("Run semantic search for \"red saree\", take the top 10, then drop items costing 2000 or more in application code", "\"red saree\" দিয়ে semantic search চালিয়ে top 10 নেওয়া, তারপর application code-এ 2000 বা বেশি দামের item বাদ দেওয়া"),
            ("Use only keyword search, because numbers can't be embedded", "শুধু keyword search ব্যবহার করা, কারণ সংখ্যা embed করা যায় না"),
        ],
        correct=1,
        a_en=r"""Use a metadata filter for the hard constraint and vector search for the meaning. Embeddings capture "red saree" well but are unreliable for numeric conditions like "under 2000"; a structured `price < 2000` filter is exact.""",
        a_bn=r"""কঠোর শর্তের জন্য metadata filter আর অর্থের জন্য vector search ব্যবহার করো। Embedding "red saree" ভালোভাবে ধরে, কিন্তু "under 2000"-এর মতো সংখ্যাভিত্তিক শর্তে নির্ভরযোগ্য নয়; structured `price < 2000` filter নিখুঁত।""",
        quick_en=r"""Turn "under 2000 taka" into a structured filter (`price < 2000`) and use "red saree" for the vector search, applied in the same query. Embeddings capture meaning well but are unreliable for numeric conditions, while a structured filter is exact.""",
        quick_bn=r""""Under 2000 taka"-কে structured filter (`price < 2000`) বানাও আর "red saree" দিয়ে vector search করো, দুটোই একই query-তে। Embedding অর্থ ভালো ধরে, কিন্তু সংখ্যার শর্তে নির্ভরযোগ্য না; structured filter একদম exact।""",
        ex_en=r"""
            - **Option A** may rank a 5,000-taka saree first — embeddings don't do arithmetic.
            - **Option C** is **post-filtering** done badly: if 8 of the top 10 cost more than 2000, the shopper sees 2 results even though hundreds of matching sarees exist.
            - **Option D** loses semantic matching ("লাল শাড়ি", "maroon saree").

            **Pre-filtering** restricts the candidate set first, then searches by similarity — accurate but can be slower with approximate indexes. **Post-filtering** searches first and filters afterwards — fast but may return too few results. Good engines combine them (filter-aware indexes, or pgvector 0.8+ iterative index scans). Getting "under 2000 taka" out of free text needs a small query-parsing step (rules or an LLM) that maps it to fields you stored as metadata.
        """,
        ex_bn=r"""
            - **Option A** 5,000 টাকার একটা শাড়িকে প্রথমে দেখাতে পারে — embedding পাটিগণিত করে না।
            - **Option C** হলো খারাপভাবে করা **post-filtering**: top 10-এর 8টার দাম 2000-এর বেশি হলে ক্রেতা মাত্র 2টা result দেখবে, অথচ শত শত মানানসই শাড়ি আছে।
            - **Option D** semantic matching হারায় ("লাল শাড়ি", "maroon saree")।

            **Pre-filtering** আগে candidate set সীমিত করে, তারপর similarity দিয়ে খোঁজে — নিখুঁত, কিন্তু approximate index-এ ধীর হতে পারে। **Post-filtering** আগে খোঁজে, পরে filter করে — দ্রুত, কিন্তু খুব কম result দিতে পারে। ভালো engine দুটো মেলায় (filter-aware index, বা pgvector 0.8+-এর iterative index scan)। Free text থেকে "under 2000 taka" বের করতে একটা ছোট query-parsing ধাপ লাগে (rule বা LLM), যেটা এটাকে metadata হিসেবে রাখা field-এর সাথে মেলায়।
        """,
        tip_en=r"""Define pre- vs post-filtering in one line each — interviewers often follow up on exactly that distinction.""",
        tip_bn=r"""Pre- বনাম post-filtering এক লাইনে করে define করো — interviewer-রা প্রায়ই ঠিক এই পার্থক্য নিয়েই follow-up করে।""",
        extra=[dict(lang="sql", label_en="Filter + semantic search in one query (pgvector)", label_bn="এক query-তে filter + semantic search (pgvector)", src=r"""
            SELECT id, name, price
            FROM products
            WHERE price < 2000 AND in_stock          -- structured metadata filter
            ORDER BY embedding <=> $1                -- $1 = embedding of "red saree"
            LIMIT 10;
        """)],
        refs=[PGV, PINECONE_VDB, QDRANT_FILTER],
        related=["vec-025", "vec-030"],
    ),
    # ------------------------------------------------------------------ vec-011
    Q(
        id="vec-011", sub="Vectors & Dimensions", diff="easy", type="mcq",
        prio="medium", market="bangladesh", mins=2,
        tags=["dimensions", "storage", "capacity-planning", "float32"],
        ver="pgvector 0.8.7 (storage formula from the pgvector docs)", vs=False, status="stable",
        q_en=r"""Roughly how much raw storage does **one** 1536-dimensional embedding take when stored as 32-bit floats (as pgvector's `vector` type does)?""",
        q_bn=r"""32-bit float হিসেবে রাখলে (pgvector-এর `vector` type যেভাবে রাখে) **একটা** 1536-dimensional embedding মোটামুটি কতটা raw storage নেয়?""",
        options=[
            ("About 1.5 KB", "প্রায় 1.5 KB"),
            ("About 6 KB", "প্রায় 6 KB"),
            ("About 12 KB", "প্রায় 12 KB"),
            ("About 48 KB", "প্রায় 48 KB"),
        ],
        correct=1,
        a_en=r"""About 6 KB: 1536 dimensions × 4 bytes = 6,144 bytes. pgvector documents `4 × dimensions + 8` bytes per vector, so 6,152 bytes.""",
        a_bn=r"""প্রায় 6 KB: 1536 dimension × 4 byte = 6,144 byte। pgvector-এর docs অনুযায়ী প্রতি vector-এ `4 × dimensions + 8` byte, অর্থাৎ 6,152 byte।""",
        quick_en=r"""About 6 KB: 1536 dimensions × 4 bytes = 6,144 bytes, and pgvector stores `4 × dimensions + 8` bytes, so 6,152 bytes per vector.""",
        quick_bn=r"""প্রায় 6 KB: 1536 dimension × 4 byte = 6,144 byte, আর pgvector প্রতি vector-এ `4 × dimensions + 8` byte রাখে, তাই 6,152 byte।""",
        ex_en=r"""
            Option A forgets that each dimension is a 4-byte float, not 1 byte; option C would be 64-bit doubles. This tiny calculation drives capacity planning:
            - **1 million** such vectors ≈ 6 GB for the vectors alone — and an HNSW index stores the vectors again plus graph links, ideally in RAM.
            - **Half precision** (`halfvec`, 2 bytes per dimension) halves it; **binary quantisation** (1 bit per dimension) shrinks it 32×, usually with re-ranking to recover accuracy.
            - **Fewer dimensions** (384 or 768 instead of 1536) cut storage proportionally — another reason not to pick the biggest model by default.
        """,
        ex_bn=r"""
            Option A ভুলে যায় যে প্রতিটা dimension 1 byte নয়, 4 byte-এর float; option C হতো 64-bit double হলে। এই ছোট হিসাবটাই capacity planning চালায়:
            - এমন **10 লাখ** vector ≈ শুধু vector-এর জন্যই 6 GB — আর HNSW index vector-গুলো আবার রাখে সাথে graph link, আদর্শভাবে RAM-এ।
            - **Half precision** (`halfvec`, প্রতি dimension-এ 2 byte) এটা অর্ধেক করে; **binary quantisation** (প্রতি dimension-এ 1 bit) 32 গুণ ছোট করে, সাধারণত accuracy ফেরাতে re-ranking সহ।
            - **কম dimension** (1536-এর বদলে 384 বা 768) অনুপাতে storage কমায় — default হিসেবে সবচেয়ে বড় model না বেছে নেওয়ার আরেক কারণ।
        """,
        tip_en=r"""Show the multiplication, then immediately scale it to a million vectors. Turning a trivia number into a capacity-planning insight is what makes the answer stand out.""",
        tip_bn=r"""গুণটা দেখাও, তারপর সাথে সাথে 10 লাখ vector-এ scale করো। একটা সাধারণ সংখ্যাকে capacity-planning insight-এ বদলে দেওয়াই উত্তরকে আলাদা করে।""",
        refs=[PGV],
        related=["vec-002", "vec-027"],
    ),
    # ------------------------------------------------------------------ vec-020
    Q(
        id="vec-020", sub="Retrieval Quality", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["reranking", "cross-encoder", "rag", "top-k"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""Your RAG assistant gives confident wrong answers. Logs show the correct chunk exists but is ranked **14th** by vector search, while you pass only the top 5 chunks to the LLM. What is the best first fix?""",
        q_bn=r"""তোমার RAG assistant আত্মবিশ্বাসের সাথে ভুল উত্তর দিচ্ছে। Log দেখাচ্ছে সঠিক chunk আছে, কিন্তু vector search-এ তার rank **14তম**, অথচ তুমি LLM-কে পাঠাও শুধু top 5 chunk। সবচেয়ে ভালো প্রথম সমাধান কী?""",
        options=[
            ("Fine-tune the LLM on all the company documents", "সব company document দিয়ে LLM fine-tune করা"),
            ("Raise the LLM temperature so it explores more possible answers", "LLM-এর temperature বাড়ানো, যাতে সে আরও সম্ভাব্য উত্তর খুঁজে দেখে"),
            ("Retrieve a larger candidate set (e.g. top 50, ideally hybrid) and rerank it with a cross-encoder, then pass the best 5 to the LLM", "বড় একটা candidate set retrieve করা (যেমন top 50, সম্ভব হলে hybrid) আর cross-encoder দিয়ে rerank করে সেরা 5টা LLM-কে পাঠানো"),
            ("Put all 50 candidates directly into the prompt and let the LLM sort it out", "50টা candidate সরাসরি prompt-এ দিয়ে LLM-কে বাছাই করতে দেওয়া"),
        ],
        correct=2,
        a_en=r"""Retrieve more, then rerank. The first-stage retriever (a bi-encoder plus ANN) is fast but coarse; a cross-encoder reads the query and each candidate **together** and scores relevance much more accurately, so the correct chunk can move from rank 14 into the top 5.""",
        a_bn=r"""বেশি retrieve করো, তারপর rerank করো। প্রথম ধাপের retriever (bi-encoder আর ANN) দ্রুত কিন্তু মোটা দাগের; cross-encoder query আর প্রতিটা candidate **একসাথে** পড়ে অনেক নিখুঁতভাবে relevance score দেয়, ফলে সঠিক chunk rank 14 থেকে top 5-এ উঠে আসতে পারে।""",
        quick_en=r"""Retrieve a bigger candidate set (say the top 50, ideally hybrid) and rerank it with a cross-encoder, then pass the best 5 to the LLM. A cross-encoder reads the query and each chunk together, so it scores relevance far more accurately than the fast first-stage vector search.""",
        quick_bn=r"""বড় candidate set আনো (ধরো top 50, পারলে hybrid), cross-encoder দিয়ে rerank করো, তারপর সেরা 5টা LLM-কে দাও। Cross-encoder query আর প্রতিটা chunk একসাথে পড়ে, তাই দ্রুত কিন্তু মোটা দাগের প্রথম ধাপের vector search-এর চেয়ে অনেক নিখুঁতভাবে relevance score করে।""",
        ex_en=r"""
            - **Why not D?** It's the tempting one and sometimes works, but it multiplies token cost and latency, adds noise, and LLMs tend to use information in the middle of long contexts less reliably. Reranking keeps the context small and relevant.
            - **Why not A?** Fine-tuning doesn't fix a ranking problem and makes facts harder to update and cite. **B** just makes answers more random.
            - **Bi-encoder vs cross-encoder:** a bi-encoder embeds query and document separately (so documents can be pre-computed and indexed); a cross-encoder must run per query–document pair, so it's only affordable on a few dozen candidates.
            - **Also check:** is hybrid search on (an exact term may be the key)? Is chunking hiding the answer? Measure recall@50 vs recall@5 to see whether the problem is retrieval or ranking.
        """,
        ex_bn=r"""
            - **D কেন নয়?** এটাই লোভনীয়, আর মাঝে মাঝে কাজও করে, কিন্তু token খরচ আর latency কয়েক গুণ বাড়ায়, noise যোগ করে, আর লম্বা context-এর মাঝখানের তথ্য LLM তুলনামূলক কম নির্ভরযোগ্যভাবে ব্যবহার করে। Reranking context ছোট আর প্রাসঙ্গিক রাখে।
            - **A কেন নয়?** Fine-tuning ranking-এর সমস্যা ঠিক করে না, আর তথ্য update ও cite করা কঠিন করে তোলে। **B** শুধু উত্তরকে আরও এলোমেলো করে।
            - **Bi-encoder বনাম cross-encoder:** bi-encoder query আর document আলাদাভাবে embed করে (তাই document আগে থেকে হিসাব করে index করা যায়); cross-encoder প্রতিটা query–document জোড়ার জন্য চালাতে হয়, তাই শুধু কয়েক ডজন candidate-এর ওপরই সাশ্রয়ী।
            - **আরও দেখো:** hybrid search চালু আছে কি (একটা নির্দিষ্ট শব্দই হয়তো আসল চাবি)? Chunking কি উত্তর লুকিয়ে ফেলছে? সমস্যা retrieval নাকি ranking, বুঝতে recall@50 আর recall@5 তুলনা করো।
        """,
        tip_en=r"""Explain the two-stage idea — cheap recall first, expensive precision second. It's a pattern from search engineering that interviewers love to hear named.""",
        tip_bn=r"""দুই ধাপের ধারণাটা ব্যাখ্যা করো — আগে সস্তায় recall, পরে দামি precision। Search engineering-এর এই pattern-এর নাম শুনতে interviewer-রা পছন্দ করে।""",
        refs=[RERANK_PAPER, SBERT],
        related=["vec-017", "vec-008", "vec-016"],
    ),
    # ------------------------------------------------------------------ vec-021
    Q(
        id="vec-021", sub="Vector DBs vs Relational DBs (pgvector)", diff="medium", type="comparison",
        prio="high", market="both", mins=8,
        tags=["pgvector", "vector-database", "pinecone", "qdrant", "architecture"],
        ver="pgvector 0.8.7 (PostgreSQL 18); product-neutral", vs=False, status="stable",
        q_en=r"""Compare using PostgreSQL with pgvector against a dedicated vector database (for example Pinecone, Qdrant, Weaviate or Milvus). What are the trade-offs, and how would you decide?""",
        q_bn=r"""pgvector সহ PostgreSQL ব্যবহার করা আর একটা dedicated vector database (যেমন Pinecone, Qdrant, Weaviate বা Milvus)-এর তুলনা করো। Trade-off কী কী, আর কীভাবে সিদ্ধান্ত নেবে?""",
        a_en=r"""
            **PostgreSQL + pgvector**
            - One system: vectors live next to users, products and permissions — SQL joins, `WHERE` filters, transactions, row-level security, and the backups/replication you already run (pgvector data goes through the WAL).
            - No sync problem: when a product is updated or deleted, its vector changes in the same transaction.
            - Limits: you scale it like PostgreSQL — mostly vertically plus read replicas and partitioning; very large indexes need lots of RAM and long builds; fewer vector-specific features.

            **Dedicated vector database**
            - Built for vector workloads: horizontal scaling, quantisation and disk-based index options, filter-aware search, sparse/hybrid vectors, multi-tenancy features, and managed/serverless offerings.
            - Costs: another system to operate or pay for, and you must **keep it in sync** with your primary database (dual writes or change-data-capture), handle eventual consistency, and duplicate access-control logic.

            **How I decide:** if the data already lives in PostgreSQL and the scale is moderate (up to millions or low tens of millions of vectors with reasonable QPS), start with pgvector. Move to a dedicated engine when measurements show you've outgrown it — memory/latency at your scale, heavy filtered search, very high QPS, or features you genuinely need.
        """,
        a_bn=r"""
            **PostgreSQL + pgvector**
            - একটাই system: vector থাকে user, product আর permission-এর পাশে — SQL join, `WHERE` filter, transaction, row-level security, আর যে backup/replication তুমি ইতিমধ্যে চালাও (pgvector-এর data WAL দিয়েই যায়)।
            - Sync-এর ঝামেলা নেই: product update বা delete হলে একই transaction-এ তার vector-ও বদলায়।
            - সীমা: PostgreSQL-এর মতোই scale করতে হয় — মূলত vertically, সাথে read replica আর partitioning; খুব বড় index-এ অনেক RAM আর লম্বা build time লাগে; vector-নির্দিষ্ট feature কম।

            **Dedicated vector database**
            - Vector workload-এর জন্যই তৈরি: horizontal scaling, quantisation আর disk-based index option, filter-aware search, sparse/hybrid vector, multi-tenancy feature, আর managed/serverless সুবিধা।
            - খরচ: চালানোর বা টাকা দেওয়ার মতো আরেকটা system, আর primary database-এর সাথে **sync রাখতে হয়** (dual write বা change-data-capture), eventual consistency সামলাতে হয়, আর access-control logic দুই জায়গায় রাখতে হয়।

            **কীভাবে সিদ্ধান্ত নিই:** data আগে থেকেই PostgreSQL-এ থাকলে আর scale মাঝারি হলে (লাখ থেকে কয়েক কোটি vector, যুক্তিসঙ্গত QPS) pgvector দিয়ে শুরু করি। মেপে যখন দেখা যায় এটা ছাড়িয়ে গেছি — আমার scale-এ memory/latency, ভারী filtered search, খুব বেশি QPS, বা সত্যিই দরকারি feature — তখন dedicated engine-এ যাই।
        """,
        quick_en=r"""pgvector keeps vectors next to your relational data, with joins, filters, transactions, existing backups and no sync problem, but it scales like PostgreSQL. A dedicated vector DB scales out and has more vector features, but it's another system to run and keep in sync. Start with pgvector; switch when measurements say so.""",
        quick_bn=r"""pgvector vector-কে relational data-র পাশেই রাখে: join, filter, transaction, আগের backup, আর sync-এর ঝামেলা নেই; তবে scale হয় PostgreSQL-এর মতো। Dedicated vector DB horizontally scale করে আর vector feature বেশি দেয়, কিন্তু আরেকটা system চালাতে আর sync রাখতে হয়। শুরু pgvector দিয়ে; মেপে দরকার দেখলে বদলাও।""",
        ex_en=r"""
            - **The sync problem is the hidden cost:** with a separate vector store, a deleted product can still appear in search until the deletion propagates — and for privacy deletions that delay matters.
            - **Hybrid search:** PostgreSQL gives you full-text (`tsvector`) next to pgvector; many dedicated engines provide built-in sparse+dense hybrid search and fusion.
            - **Other options:** Redis (Query Engine vector indexes, Vector Sets) for low-latency, in-memory use cases; search engines like OpenSearch/Elasticsearch when you already run them for keyword search.
            - **Avoid premature migration:** many teams adopt a dedicated vector DB on day one for a few hundred thousand vectors, adding operational cost without benefit. Benchmark with your own data and filters first.
        """,
        ex_bn=r"""
            - **Sync-সমস্যাই লুকানো খরচ:** আলাদা vector store থাকলে delete করা product deletion পৌঁছানো পর্যন্ত search-এ দেখা যেতে পারে — আর privacy-সংক্রান্ত deletion-এ এই দেরি গুরুত্বপূর্ণ।
            - **Hybrid search:** PostgreSQL pgvector-এর পাশেই full-text (`tsvector`) দেয়; অনেক dedicated engine built-in sparse+dense hybrid search আর fusion দেয়।
            - **অন্য option:** কম latency-র in-memory use case-এর জন্য Redis (Query Engine vector index, Vector Sets); keyword search-এর জন্য আগে থেকেই চালালে OpenSearch/Elasticsearch-এর মতো search engine।
            - **অকাল migration এড়াও:** অনেক team কয়েক লাখ vector-এর জন্য প্রথম দিনেই dedicated vector DB নেয়, কোনো লাভ ছাড়াই operational খরচ বাড়ায়। আগে নিজের data আর filter দিয়ে benchmark করো।
        """,
        tip_en=r"""Stay product-neutral and decision-oriented: "start simple, measure, migrate on evidence". Naming the sync/consistency cost of a second datastore is the detail that impresses.""",
        tip_bn=r"""Product-neutral থাকো আর সিদ্ধান্তমুখী হও: "সহজ দিয়ে শুরু, মাপো, প্রমাণ পেলে migrate করো"। দ্বিতীয় datastore-এর sync/consistency খরচের কথা বলাই মুগ্ধ করার মতো detail।""",
        mist_en=r"""Claiming PostgreSQL "can't do vectors", or picking a vector DB by hype without considering how it stays in sync with the source of truth.""",
        mist_bn=r"""দাবি করা যে PostgreSQL "vector সামলাতে পারে না", অথবা source of truth-এর সাথে কীভাবে sync থাকবে না ভেবেই hype দেখে vector DB বেছে নেওয়া।""",
        follow=[
            ("How would you keep a dedicated vector DB in sync with PostgreSQL?", "একটা dedicated vector DB-কে PostgreSQL-এর সাথে কীভাবে sync রাখবে?"),
            ("Which metrics would tell you that pgvector is no longer enough?", "কোন metric দেখে বুঝবে যে pgvector আর যথেষ্ট নয়?"),
        ],
        related=["vec-009", "vec-027"],
        refs=[PGV, PINECONE_VDB, R_VECTORS],
    ),
    # ------------------------------------------------------------------ vec-022
    Q(
        id="vec-022", sub="Data Privacy", diff="medium", type="security-performance",
        prio="high", market="both", mins=8,
        tags=["privacy", "pii", "access-control", "embedding-inversion", "deletion"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""What privacy and security risks do embeddings and vector databases introduce in a RAG or semantic-search system, and how do you mitigate them?""",
        q_bn=r"""RAG বা semantic-search system-এ embedding আর vector database কী কী privacy ও security ঝুঁকি তৈরি করে, আর সেগুলো কীভাবে কমাও?""",
        a_en=r"""
            - **PII inside chunks:** documents and tickets contain names, phone numbers, NID numbers, addresses. Classify and **mask or remove PII before embedding** where it isn't needed for search, and before sending context to an LLM.
            - **Sending data to external APIs:** a hosted embedding or LLM API receives your raw text. Check the provider's data-retention and processing terms, region and contract; use self-hosted models for highly sensitive data.
            - **Embeddings are not anonymous:** research shows embeddings can be partially inverted to recover the original text. Treat vectors as sensitive as the source — encryption at rest, network isolation, least-privilege access.
            - **Access control at retrieval time:** store tenant and ACL metadata on every chunk and filter in the query (plus row-level security). A prompt instruction is not access control.
            - **Deletion:** a "delete my data" request must remove the source document, its chunks and vectors, cached answers and logs that contain the text — and backups must age out on a documented schedule.
            - **Poisoning and injection:** only ingest from trusted sources; scan for hidden text; treat retrieved content as untrusted input to the LLM.
        """,
        a_bn=r"""
            - **Chunk-এর ভেতরে PII:** document আর ticket-এ নাম, phone number, NID number, ঠিকানা থাকে। Search-এর জন্য দরকার না হলে **embed করার আগেই PII শ্রেণিবদ্ধ করে mask বা মুছে ফেলো**, আর LLM-কে context পাঠানোর আগেও।
            - **External API-তে data পাঠানো:** hosted embedding বা LLM API তোমার raw text পায়। Provider-এর data-retention আর processing শর্ত, region আর চুক্তি দেখে নাও; খুব sensitive data-র জন্য self-hosted model ব্যবহার করো।
            - **Embedding নামহীন (anonymous) নয়:** গবেষণা দেখায় embedding আংশিকভাবে উল্টে মূল text উদ্ধার করা যায়। Vector-কে source-এর মতোই sensitive ধরো — encryption at rest, network isolation, least-privilege access।
            - **Retrieval-এর সময় access control:** প্রতিটা chunk-এ tenant আর ACL metadata রাখো, query-তেই filter করো (সাথে row-level security)। Prompt-এর নির্দেশনা access control নয়।
            - **Deletion:** "আমার data মুছে দাও" request-এ source document, তার chunk আর vector, cached answer, আর text থাকা log — সব মুছতে হবে, আর backup একটা documented সময়সূচিতে মেয়াদোত্তীর্ণ হতে হবে।
            - **Poisoning আর injection:** শুধু বিশ্বস্ত source থেকে ingest করো; লুকানো text scan করো; retrieve হওয়া content-কে LLM-এর জন্য untrusted input হিসেবে দেখো।
        """,
        quick_en=r"""Chunks can contain PII, hosted embedding/LLM APIs see your raw text, embeddings can be partly inverted back to text, and missing filters leak data across users. Mask PII before embedding, vet the provider or self-host, protect vectors like the source, filter by ACL in the query, and treat retrieved text as untrusted.""",
        quick_bn=r"""Chunk-এ PII থাকতে পারে, hosted embedding/LLM API তোমার raw text দেখে, embedding থেকে আংশিকভাবে আসল text ফেরত বের করা যায়, আর filter না থাকলে এক user-এর data অন্যজনের কাছে যায়। Embed করার আগে PII mask করো, provider যাচাই করো বা self-host করো, vector-কে source-এর মতোই সুরক্ষিত রাখো, query-তে ACL filter দাও, আর retrieve করা text-কে untrusted ধরো।""",
        ex_en=r"""
            - **Performance side of security:** filtering by tenant/ACL inside ANN search can reduce recall or speed; plan for it (iterative scans, partitions per large tenant) instead of dropping the filter.
            - **Logging:** prompts and retrieved chunks in logs are a common leak path — redact them or restrict log access, and set retention.
            - **Regulations:** follow the data-protection rules that apply to your users (Bangladesh's own rules for local users, GDPR if you serve EU residents, and sector rules like banking). Involve legal early for cross-border data transfers to embedding providers.
            - **OWASP** lists "Vector and Embedding Weaknesses" as one of the top LLM application risks — a good checklist to cite.
        """,
        ex_bn=r"""
            - **Security-র performance দিক:** ANN search-এর ভেতরে tenant/ACL দিয়ে filter করলে recall বা speed কমতে পারে; filter বাদ না দিয়ে এর জন্য পরিকল্পনা করো (iterative scan, বড় tenant-এর জন্য partition)।
            - **Logging:** log-এ prompt আর retrieve হওয়া chunk থাকা ফাঁসের একটা সাধারণ পথ — redact করো বা log access সীমিত করো, আর retention ঠিক করো।
            - **আইন-কানুন:** তোমার user-দের ক্ষেত্রে প্রযোজ্য data-protection নিয়ম মেনে চলো (local user-দের জন্য বাংলাদেশের নিজস্ব নিয়ম, EU-র বাসিন্দাদের serve করলে GDPR, আর banking-এর মতো খাতভিত্তিক নিয়ম)। Embedding provider-এর কাছে দেশের বাইরে data পাঠানোর ক্ষেত্রে শুরুতেই legal team-কে যুক্ত করো।
            - **OWASP** "Vector and Embedding Weaknesses"-কে LLM application-এর শীর্ষ ঝুঁকিগুলোর একটা হিসেবে তালিকাভুক্ত করেছে — উল্লেখ করার মতো ভালো checklist।
        """,
        tip_en=r"""Organise the answer along the data's journey: ingest (PII), embed (external API), store (vectors are sensitive), retrieve (access control), delete (right to be forgotten). A lifecycle structure is easy to follow and complete.""",
        tip_bn=r"""উত্তরটা data-র যাত্রাপথ ধরে সাজাও: ingest (PII), embed (external API), store (vector-ও sensitive), retrieve (access control), delete (মুছে ফেলার অধিকার)। Lifecycle-ভিত্তিক কাঠামো অনুসরণ করা সহজ আর সম্পূর্ণ।""",
        mist_en=r"""Calling embeddings "anonymised data", relying on the LLM prompt to hide restricted content, or deleting the source document but leaving its vectors searchable.""",
        mist_bn=r"""Embedding-কে "anonymised data" বলা, restricted content লুকাতে LLM prompt-এর ওপর ভরসা করা, অথবা source document মুছে ফেলে তার vector search-যোগ্য রেখে দেওয়া।""",
        code=r"""
            -- Deleting a customer's data must reach every derived copy
            BEGIN;
            DELETE FROM chunks        WHERE doc_id IN (SELECT id FROM documents WHERE customer_id = $1);
            DELETE FROM answer_cache  WHERE customer_id = $1;
            DELETE FROM documents     WHERE customer_id = $1;
            COMMIT;
            -- then: purge object storage files, external vector stores, logs; backups expire per policy
        """,
        lang="sql",
        follow=[
            ("Should you embed text before or after removing PII? What do you lose either way?", "PII মুছে ফেলার আগে না পরে text embed করবে? দুই ক্ষেত্রেই কী হারাও?"),
            ("How would you prove to an auditor that a user's data was fully deleted?", "একজন auditor-কে কীভাবে প্রমাণ করবে যে একজন user-এর data পুরোপুরি মুছে ফেলা হয়েছে?"),
        ],
        related=["vec-026", "vec-031", "vec-019"],
        refs=[OWASP_LLM08, PG_RLS],
    ),
    # ------------------------------------------------------------------ vec-028
    Q(
        id="vec-028", sub="Retrieval Quality", diff="hard", type="conceptual",
        prio="medium", market="international", mins=12,
        tags=["evaluation", "golden-set", "llm-as-judge", "ci", "regression-testing"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""How would you set up continuous evaluation for a RAG system so that changes to chunking, embedding models, index parameters or prompts never silently make it worse?""",
        q_bn=r"""একটা RAG system-এর জন্য continuous evaluation কীভাবে সাজাবে, যাতে chunking, embedding model, index parameter বা prompt-এর পরিবর্তন কখনো চুপচাপ system-কে খারাপ করে দিতে না পারে?""",
        a_en=r"""
            **1. A versioned golden dataset.**
            - 100–500 real questions sampled from logs and support channels, stratified by language (Bangla/English/Banglish), topic and difficulty, including "no answer exists" cases.
            - Each labelled with the relevant documents/chunks and a reference answer, reviewed by subject-matter experts. LLM-generated questions can bootstrap coverage, but humans must check them.

            **2. Measure retrieval and generation separately.**
            - Retrieval: recall@k, MRR, nDCG against the labels — plus ANN recall against exact search for index changes.
            - Generation: faithfulness (is every claim supported by the retrieved context?), answer correctness, citation accuracy, and refusal when the answer isn't in the sources. An LLM-as-judge can score these at scale, but calibrate it against human ratings first.

            **3. Gate changes in CI/CD.** Every pull request that touches the pipeline runs the evaluation; a drop beyond a tolerance on any key metric (overall *or* per language segment) blocks the merge. Store results so you can see trends.

            **4. Roll out safely.** Shadow traffic or a canary with online metrics — thumbs up/down, "no answer" rate, reformulation rate, latency and cost — before full rollout.

            **5. Keep it alive.** Add every production failure to the golden set, and refresh it as documents and user behaviour drift.
        """,
        a_bn=r"""
            **1. Version করা golden dataset।**
            - Log আর support channel থেকে 100–500টা আসল প্রশ্ন, ভাষা (Bangla/English/Banglish), topic আর কাঠিন্য অনুযায়ী ভাগ করে নেওয়া, "উত্তর নেই" ধরনের case সহ।
            - প্রতিটার সাথে relevant document/chunk আর একটা reference answer-এর label, বিষয়-বিশেষজ্ঞদের review করা। LLM দিয়ে তৈরি প্রশ্ন coverage বাড়াতে শুরুতে সাহায্য করে, কিন্তু মানুষকে সেগুলো যাচাই করতে হবে।

            **2. Retrieval আর generation আলাদা করে মাপো।**
            - Retrieval: label-এর বিপরীতে recall@k, MRR, nDCG — সাথে index পরিবর্তনের জন্য exact search-এর বিপরীতে ANN recall।
            - Generation: faithfulness (প্রতিটা দাবি কি retrieve হওয়া context দিয়ে সমর্থিত?), answer correctness, citation accuracy, আর source-এ উত্তর না থাকলে অস্বীকার করা। LLM-as-judge বড় পরিসরে এগুলো score করতে পারে, কিন্তু আগে মানুষের rating-এর সাথে calibrate করে নাও।

            **3. CI/CD-তে পরিবর্তন আটকাও।** Pipeline ছোঁয়া প্রতিটা pull request evaluation চালায়; কোনো মূল metric-এ (সামগ্রিক *বা* কোনো ভাষার segment-এ) সহনসীমার বেশি পতন হলে merge আটকে যায়। Result সংরক্ষণ করো যাতে প্রবণতা দেখা যায়।

            **4. নিরাপদে rollout।** পুরো rollout-এর আগে shadow traffic বা canary, online metric সহ — thumbs up/down, "উত্তর নেই" rate, প্রশ্ন বদলে লেখার rate, latency আর খরচ।

            **5. সজীব রাখো।** Production-এর প্রতিটা ব্যর্থতা golden set-এ যোগ করো, আর document ও user-এর আচরণ বদলালে set-টা হালনাগাদ করো।
        """,
        quick_en=r"""Keep a versioned golden set of real questions (per language, including no-answer cases), measure retrieval (recall@k, MRR, nDCG) and generation (faithfulness, correctness) separately, block merges in CI when a metric drops beyond a tolerance, roll out via canary, and add every production failure to the set.""",
        quick_bn=r"""আসল প্রশ্নের একটা versioned golden set রাখো (ভাষা অনুযায়ী, উত্তর নেই এমন case-সহ), retrieval (recall@k, MRR, nDCG) আর generation (faithfulness, correctness) আলাদা করে মাপো, কোনো metric tolerance-এর বেশি কমলে CI-তে merge আটকাও, canary দিয়ে rollout করো, আর production-এর প্রতিটা failure set-এ যোগ করো।""",
        ex_en=r"""
            - **Why per-segment gates:** a new model can raise the English average while quietly breaking Bangla queries. Averages hide regressions in minority segments.
            - **LLM-as-judge pitfalls:** judges can prefer longer answers or their own style, and can be inconsistent. Use clear rubrics, fixed judge models/prompts, and periodic human spot checks.
            - **Cost control:** run a small fast subset on every PR and the full suite nightly or before releases.
            - **Reproducibility:** pin the embedding model version, index parameters and prompt versions in the evaluation report so you can explain any change in numbers.
        """,
        ex_bn=r"""
            - **Segment-ভিত্তিক gate কেন:** নতুন model English-এর গড় বাড়িয়ে দিয়েও চুপচাপ Bangla query ভেঙে ফেলতে পারে। গড় হিসাব ছোট segment-এর regression লুকিয়ে ফেলে।
            - **LLM-as-judge-এর ফাঁদ:** judge লম্বা উত্তর বা নিজের ধাঁচ পছন্দ করতে পারে, আর অসামঞ্জস্যপূর্ণও হতে পারে। স্পষ্ট rubric, নির্দিষ্ট judge model/prompt, আর মাঝে মাঝে মানুষের spot check ব্যবহার করো।
            - **খরচ নিয়ন্ত্রণ:** প্রতিটা PR-এ ছোট দ্রুত একটা subset, আর পুরো suite রাতে বা release-এর আগে চালাও।
            - **Reproducibility:** evaluation report-এ embedding model version, index parameter আর prompt version pin করে রাখো, যাতে সংখ্যার যেকোনো পরিবর্তন ব্যাখ্যা করা যায়।
        """,
        tip_en=r"""Frame it as "unit tests for search quality". Mentioning per-language regression gates and LLM-as-judge calibration shows you've thought about how evaluation itself can fail.""",
        tip_bn=r"""এটাকে "search quality-র unit test" হিসেবে উপস্থাপন করো। ভাষাভিত্তিক regression gate আর LLM-as-judge calibration-এর কথা বললে বোঝা যায় তুমি ভেবেছ evaluation নিজেও কীভাবে ব্যর্থ হতে পারে।""",
        mist_en=r"""Evaluating only end-to-end answers (you can't tell whether retrieval or generation broke), trusting an uncalibrated LLM judge, or letting the golden set go stale.""",
        mist_bn=r"""শুধু end-to-end উত্তর মূল্যায়ন করা (retrieval না generation ভাঙল বোঝা যায় না), calibrate না করা LLM judge-কে বিশ্বাস করা, অথবা golden set-কে পুরনো হতে দেওয়া।""",
        code=r"""
            # ci/eval_gate.py — fail the build on retrieval regressions (per language)
            import sys

            TOLERANCE = 0.02
            baseline = {"bn": {"recall@5": 0.81, "mrr@5": 0.58},
                        "en": {"recall@5": 0.86, "mrr@5": 0.64}}

            current = run_retrieval_eval("golden_set_v7.jsonl")   # returns the same shape

            failures = [
                f"{lang} {metric}: {current[lang][metric]:.2f} < {value:.2f}"
                for lang, metrics in baseline.items()
                for metric, value in metrics.items()
                if current[lang][metric] < value - TOLERANCE
            ]
            if failures:
                sys.exit("Retrieval regression:\n" + "\n".join(failures))
        """,
        lang="python",
        follow=[
            ("How do you evaluate answers when there is no single correct wording?", "যখন একটাই সঠিক শব্দচয়ন নেই, তখন উত্তর কীভাবে মূল্যায়ন করবে?"),
            ("How would you detect that the golden set no longer represents real traffic?", "Golden set আর আসল traffic-এর প্রতিনিধিত্ব করছে না — এটা কীভাবে ধরবে?"),
        ],
        related=["vec-017", "vec-032", "vec-024"],
        refs=[WIKI_IREVAL, RAG_PAPER],
    ),
    # ------------------------------------------------------------------ vec-029
    Q(
        id="vec-029", sub="Production Use Cases", diff="hard", type="scenario",
        prio="medium", market="both", mins=10,
        tags=["semantic-cache", "llm-cost", "threshold", "invalidation", "multi-tenant"],
        ver="Version-independent concept (example: pgvector 0.8.7)", vs=False, status="stable",
        q_en=r"""To cut LLM costs, a teammate proposes a **semantic cache**: if a new question's embedding has cosine similarity ≥ 0.92 with a previously answered question, return the cached answer. What can go wrong, and how would you design it safely?""",
        q_bn=r"""LLM-এর খরচ কমাতে একজন teammate একটা **semantic cache** প্রস্তাব করেছে: নতুন প্রশ্নের embedding আগে উত্তর দেওয়া কোনো প্রশ্নের সাথে cosine similarity ≥ 0.92 হলে cached উত্তর ফেরত দেওয়া হবে। কী কী ভুল হতে পারে, আর নিরাপদভাবে কীভাবে design করবে?""",
        a_en=r"""
            **What can go wrong:**
            - **False hits:** "How do I cancel my order?" vs "How do I cancel my subscription?" — very similar embeddings, different answers. Negation ("can I" vs "can't I"), numbers and ids ("refund for order 1234" vs "5678") are classic traps.
            - **Data leaks:** a cached answer generated for one user or tenant ("your balance is…") served to another.
            - **Stale answers:** the policy document changed yesterday, but the cache keeps serving last month's answer.
            - **Wrong language or channel:** a Bangla question gets an English cached answer.

            **Safer design:**
            1. **Scope the cache key:** tenant, language, user role/permissions and product area are hard filters — similarity is only compared within the same scope. Never cache personalised answers.
            2. **Exact cache first:** a hash of the normalised question catches repeats safely; semantic matching is the second layer.
            3. **Tune the threshold on labelled pairs** (same answer / different answer), optimising for precision — a false hit is worse than a miss.
            4. **Invalidate on source changes:** store the ids and versions of the documents behind each answer; when a document changes, drop dependent entries. Add a TTL as a backstop.
            5. **Guard sensitive patterns:** skip the cache when the question contains ids, amounts or dates, or let a cheap check confirm the entities match.
            6. **Monitor:** hit rate, user feedback on cached answers versus fresh ones, and sampled audits.
        """,
        a_bn=r"""
            **কী কী ভুল হতে পারে:**
            - **ভুল hit:** "How do I cancel my order?" বনাম "How do I cancel my subscription?" — embedding খুব কাছাকাছি, উত্তর আলাদা। Negation ("পারি" বনাম "পারি না"), সংখ্যা আর id ("order 1234-এর refund" বনাম "5678") হলো classic ফাঁদ।
            - **Data ফাঁস:** একজন user বা tenant-এর জন্য তৈরি cached উত্তর ("তোমার balance হলো…") অন্য কাউকে দেওয়া।
            - **পুরনো উত্তর:** policy document গতকাল বদলেছে, কিন্তু cache গত মাসের উত্তরই দিয়ে যাচ্ছে।
            - **ভুল ভাষা বা channel:** Bangla প্রশ্নের জবাবে English cached উত্তর।

            **নিরাপদ design:**
            1. **Cache key-এর পরিধি ঠিক করো:** tenant, language, user role/permission আর product area হলো কঠোর filter — similarity তুলনা হবে শুধু একই পরিধির ভেতরে। Personalised উত্তর কখনো cache কোরো না।
            2. **আগে exact cache:** normalised প্রশ্নের hash নিরাপদে পুনরাবৃত্তি ধরে; semantic matching দ্বিতীয় স্তর।
            3. **Labelled জোড়া দিয়ে threshold tune করো** (একই উত্তর / আলাদা উত্তর), precision-কে অগ্রাধিকার দিয়ে — miss-এর চেয়ে ভুল hit খারাপ।
            4. **Source বদলালে invalidate করো:** প্রতিটা উত্তরের পেছনের document-এর id আর version রাখো; document বদলালে নির্ভরশীল entry মুছে দাও। Backstop হিসেবে TTL দাও।
            5. **Sensitive pattern থেকে সাবধান:** প্রশ্নে id, টাকার অঙ্ক বা তারিখ থাকলে cache এড়িয়ে যাও, অথবা একটা সস্তা check দিয়ে নিশ্চিত হও যে entity-গুলো মিলছে।
            6. **Monitor করো:** hit rate, cached বনাম নতুন উত্তরে user feedback, আর sample করে audit।
        """,
        quick_en=r"""Similar questions can need different answers ("cancel my order" vs "cancel my subscription"), cached answers can leak across users or tenants, and they go stale. Scope it by tenant, language and permissions, try an exact-hash cache first, tune the threshold for precision, and invalidate on document changes.""",
        quick_bn=r"""কাছাকাছি প্রশ্নের উত্তর আলাদা হতে পারে ("cancel my order" বনাম "cancel my subscription"), cached উত্তর এক user বা tenant থেকে অন্যের কাছে leak হতে পারে, আর পুরনো হয়ে যায়। Cache-কে tenant, language আর permission দিয়ে scope করো, আগে exact-hash cache দেখো, precision-এর জন্য threshold tune করো, আর document বদলালে invalidate করো।""",
        ex_en=r"""
            - **0.92 means nothing universal:** similarity scales differ between models; a threshold copied from a blog post can be far too loose or too strict for your model and languages.
            - **Where to store it:** a small table in pgvector, or Redis (its Query Engine vector indexes or Vector Sets) for very low latency — both work; what matters is the scoping and invalidation logic.
            - **Expected savings:** semantic caches pay off for FAQ-like traffic with many repeated intents; for long-tail, personalised questions the hit rate will be low and the risk higher.
            - **Compliance:** cached answers are stored data — include them in deletion requests and retention policies.
        """,
        ex_bn=r"""
            - **0.92-এর কোনো সর্বজনীন অর্থ নেই:** model ভেদে similarity-র scale আলাদা; কোনো blog post থেকে নেওয়া threshold তোমার model আর ভাষার জন্য অনেক বেশি ঢিলা বা কড়া হতে পারে।
            - **কোথায় রাখবে:** pgvector-এ একটা ছোট table, অথবা খুব কম latency-র জন্য Redis (তার Query Engine vector index বা Vector Sets) — দুটোই চলে; আসল বিষয় হলো পরিধি আর invalidation-এর logic।
            - **প্রত্যাশিত সাশ্রয়:** একই intent বারবার আসে এমন FAQ-ধরনের traffic-এ semantic cache লাভজনক; long-tail, personalised প্রশ্নে hit rate কম আর ঝুঁকি বেশি।
            - **Compliance:** cached উত্তরও store করা data — deletion request আর retention policy-তে এগুলোও অন্তর্ভুক্ত করো।
        """,
        tip_en=r"""Lead with a concrete false-hit pair — it instantly shows you understand the risk. Then present scoping, threshold tuning and invalidation as the three pillars.""",
        tip_bn=r"""একটা concrete ভুল-hit জোড়া দিয়ে শুরু করো — সাথে সাথে বোঝা যায় তুমি ঝুঁকিটা বোঝো। তারপর পরিধি নির্ধারণ, threshold tuning আর invalidation-কে তিনটা স্তম্ভ হিসেবে উপস্থাপন করো।""",
        mist_en=r"""Using a single global cache across tenants, picking the threshold by intuition, or caching answers without tracking which documents they came from.""",
        mist_bn=r"""সব tenant-এর জন্য একটাই global cache ব্যবহার করা, অনুমানে threshold বেছে নেওয়া, অথবা কোন document থেকে উত্তর এসেছে সেটা track না করেই cache করা।""",
        code=r"""
            -- Semantic cache lookup, scoped by tenant and language ($1 = question embedding)
            SELECT answer, source_versions, 1 - (question_embedding <=> $1) AS similarity
            FROM answer_cache
            WHERE tenant_id = $2
              AND language = $3
              AND expires_at > now()
            ORDER BY question_embedding <=> $1
            LIMIT 1;
            -- App: use it only if similarity >= tuned threshold AND all source_versions are still current
        """,
        lang="sql",
        follow=[
            ("How would you measure whether the semantic cache is causing wrong answers?", "Semantic cache ভুল উত্তর দিচ্ছে কিনা কীভাবে মাপবে?"),
            ("How do you invalidate cached answers when a source document changes?", "Source document বদলালে cached উত্তর কীভাবে invalidate করবে?"),
        ],
        related=["vec-017", "vec-031"],
        refs=[PGV, R_VECTORS],
    ),
    # ------------------------------------------------------------------ vec-032
    Q(
        id="vec-032", sub="RAG Architecture", diff="extreme", type="scenario",
        prio="medium", market="international", mins=20,
        tags=["incident", "rag", "regression", "re-ingestion", "debugging", "observability"],
        ver="Version-independent (pgvector 0.8.7 used in diagnostics)", vs=False, status="stable",
        q_en=r"""After last week's deploy, your RAG assistant's thumbs-down rate doubled and answers now cite irrelevant or outdated documents. The deploy included a new chunker, an upgrade of the embedding client library, and a full re-ingestion of the knowledge base. Nothing throws errors. How do you investigate and fix this?""",
        q_bn=r"""গত সপ্তাহের deploy-এর পর তোমার RAG assistant-এর thumbs-down rate দ্বিগুণ হয়েছে, আর উত্তরে অপ্রাসঙ্গিক বা পুরনো document cite হচ্ছে। Deploy-এ ছিল একটা নতুন chunker, embedding client library-র upgrade, আর পুরো knowledge base আবার ingest করা। কোনো error throw হচ্ছে না। কীভাবে investigate আর fix করবে?""",
        a_en=r"""
            *(Advanced incident question.)*

            **1. Contain.** If the previous index still exists (blue/green), switch reads back to it behind a flag while you investigate. If it doesn't, that's the first lesson for the postmortem.

            **2. Reproduce with numbers.** Run the golden set against the old and new pipelines; break results down by language and document type. Determine whether **retrieval** broke (the right chunks aren't in the top k) or **generation** broke (right chunks, bad answers).

            **3. Check the data, not just the code:**
            - **Mixed or wrong models:** count rows per `embedding_model`; a partially failed re-ingestion can leave old and new vectors mixed in one index.
            - **Library defaults changed:** normalisation, pooling, truncation length or required prefixes (`query:`/`passage:`) may differ after the upgrade — so queries and documents are no longer embedded the same way.
            - **Stale and duplicate chunks:** old versions not deleted during re-ingestion explain "outdated documents cited". Check for duplicate content hashes and chunks whose document version is behind.
            - **Chunker output:** compare chunk-length distributions; look for empty chunks, chunks that cut tables, or Bangla text that never got split because the splitter ignores "।".
            - **Lost metadata/filters:** missing language or ACL fields can silently widen searches.
            - **Index built too early:** an IVFFlat index built before the data finished loading has poor clusters and low recall.

            **4. Bisect.** Re-run evaluation with each change isolated (old chunker + new library, and so on) to pin the cause.

            **5. Fix and prevent:** rebuild cleanly into a new index, verify metrics, cut over; then add an evaluation gate in CI, ingestion data-quality checks (model consistency, duplicates, chunk stats), canary rollouts watching feedback rate, and keep the previous index for quick rollback.
        """,
        a_bn=r"""
            *(Advanced incident প্রশ্ন।)*

            **1. সীমাবদ্ধ করো।** আগের index এখনো থাকলে (blue/green), investigate করার সময় একটা flag-এর পেছনে read সেখানে ফিরিয়ে দাও। না থাকলে, সেটাই postmortem-এর প্রথম শিক্ষা।

            **2. সংখ্যা দিয়ে পুনরুৎপাদন করো।** পুরনো আর নতুন pipeline-এর বিপরীতে golden set চালাও; ভাষা আর document-এর ধরন অনুযায়ী ফল ভাগ করে দেখো। নির্ধারণ করো **retrieval** ভেঙেছে (সঠিক chunk top k-তে নেই) নাকি **generation** ভেঙেছে (chunk ঠিক, উত্তর খারাপ)।

            **3. শুধু code নয়, data দেখো:**
            - **মিশ্র বা ভুল model:** `embedding_model` অনুযায়ী row গোনো; আংশিক fail করা re-ingestion এক index-এ পুরনো আর নতুন vector মিশিয়ে রাখতে পারে।
            - **Library-র default বদলেছে:** upgrade-এর পর normalisation, pooling, truncation length বা প্রয়োজনীয় prefix (`query:`/`passage:`) আলাদা হতে পারে — ফলে query আর document আর একইভাবে embed হচ্ছে না।
            - **পুরনো আর duplicate chunk:** re-ingestion-এর সময় পুরনো version না মুছলে "পুরনো document cite হওয়া"-র ব্যাখ্যা মেলে। Duplicate content hash আর পিছিয়ে থাকা document version-এর chunk খোঁজো।
            - **Chunker-এর output:** chunk-length distribution তুলনা করো; খালি chunk, table কেটে ফেলা chunk, বা "।" উপেক্ষা করে এমন splitter-এর কারণে কখনো ভাগ না হওয়া Bangla text খোঁজো।
            - **হারানো metadata/filter:** language বা ACL field না থাকলে search চুপচাপ বিস্তৃত হয়ে যায়।
            - **খুব আগে index build:** data load শেষ হওয়ার আগে বানানো IVFFlat index-এর cluster খারাপ হয় আর recall কম থাকে।

            **4. Bisect করো।** প্রতিটা পরিবর্তন আলাদা করে (পুরনো chunker + নতুন library, ইত্যাদি) আবার evaluation চালাও, কারণটা নির্দিষ্ট করতে।

            **5. ঠিক করো আর প্রতিরোধ করো:** একটা নতুন index-এ পরিষ্কারভাবে rebuild করো, metric যাচাই করো, cut over করো; তারপর CI-তে evaluation gate, ingestion-এ data-quality check (model consistency, duplicate, chunk stats), feedback rate দেখে canary rollout যোগ করো, আর দ্রুত rollback-এর জন্য আগের index রেখে দাও।
        """,
        quick_en=r"""Switch back to the previous index if it still exists, then run the golden set on old and new pipelines to see whether retrieval or generation broke. Check the data (mixed embedding models, changed library defaults, stale or duplicate chunks, bad chunker output), bisect each change, then rebuild cleanly and add evaluation gates.""",
        quick_bn=r"""আগের index থাকলে আগে সেটায় ফিরে যাও, তারপর পুরনো আর নতুন pipeline-এ golden set চালিয়ে দেখো retrieval ভেঙেছে নাকি generation। Data দেখো (মিশে যাওয়া embedding model, library-র বদলানো default, পুরনো বা duplicate chunk, খারাপ chunker output), প্রতিটা change আলাদা করে bisect করো, তারপর পরিষ্কারভাবে rebuild করে evaluation gate যোগ করো।""",
        ex_en=r"""
            - **"No errors" is the norm for ML regressions:** dimension checks pass, queries return rows — quality silently drops. That's why data-quality assertions and evaluation gates matter as much as unit tests.
            - **Three changes in one deploy** made attribution hard. Ship pipeline changes separately, each behind its own evaluation.
            - **Re-ingestion should be idempotent:** deterministic chunk ids plus "delete chunks not seen in this run" (or a fresh index swapped in atomically) prevent orphans and duplicates.
            - **Observability to add:** per-query logs of retrieved chunk ids, scores and model version; dashboards for feedback rate, "no answer" rate and score distributions per language.
        """,
        ex_bn=r"""
            - **ML regression-এ "কোনো error নেই" স্বাভাবিক:** dimension check পার হয়, query row ফেরত দেয় — quality চুপচাপ পড়ে যায়। এজন্যই data-quality assertion আর evaluation gate unit test-এর মতোই জরুরি।
            - **এক deploy-এ তিনটা পরিবর্তন** কারণ খুঁজে বের করা কঠিন করেছে। Pipeline-এর পরিবর্তন আলাদা আলাদা ship করো, প্রতিটা নিজস্ব evaluation-এর পেছনে।
            - **Re-ingestion idempotent হওয়া উচিত:** নির্দিষ্ট chunk id আর "এই run-এ দেখা যায়নি এমন chunk মুছে ফেলো" (বা atomically বদলে দেওয়া নতুন index) অনাথ আর duplicate chunk ঠেকায়।
            - **যে observability যোগ করবে:** প্রতি query-তে retrieve হওয়া chunk id, score আর model version-এর log; ভাষা অনুযায়ী feedback rate, "উত্তর নেই" rate আর score distribution-এর dashboard।
        """,
        tip_en=r"""Structure it like a real incident: contain → measure → form hypotheses → verify with data → bisect → fix → prevent. Naming the "mixed embeddings after partial re-ingestion" failure shows hands-on experience.""",
        tip_bn=r"""এটাকে বাস্তব incident-এর মতো সাজাও: সীমাবদ্ধ করো → মাপো → hypothesis তৈরি করো → data দিয়ে যাচাই করো → bisect করো → ঠিক করো → প্রতিরোধ করো। "আংশিক re-ingestion-এর পর মিশ্র embedding" ব্যর্থতার নাম বললে হাতে-কলমে অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Blaming the LLM and tweaking prompts first, rolling forward with more changes before measuring, or re-ingesting into the same live index without a rollback path.""",
        mist_bn=r"""আগে LLM-কে দোষ দিয়ে prompt নিয়ে টানাটানি করা, না মেপেই আরও পরিবর্তন নিয়ে এগিয়ে যাওয়া, অথবা rollback-এর পথ না রেখে একই live index-এ আবার ingest করা।""",
        code=r"""
            -- Mixed embedding models after re-ingestion?
            SELECT embedding_model, count(*) FROM chunks GROUP BY 1 ORDER BY 1;

            -- Duplicate chunks (old versions not deleted)?
            SELECT content_hash, count(*) FROM chunks
            GROUP BY 1 HAVING count(*) > 1 ORDER BY 2 DESC LIMIT 10;

            -- Did chunk sizes change dramatically? (p50, p95 in characters)
            SELECT percentile_cont(ARRAY[0.5, 0.95]) WITHIN GROUP (ORDER BY length(content)) FROM chunks;

            -- Chunks from deleted documents or outdated document versions
            SELECT count(*) FROM chunks c
            LEFT JOIN documents d ON d.id = c.doc_id
            WHERE d.id IS NULL OR c.doc_version < d.version;
        """,
        lang="sql",
        follow=[
            ("How would you design re-ingestion so it can never leave a half-updated index live?", "Re-ingestion কীভাবে design করবে যাতে কখনো অর্ধেক-update হওয়া index live না থাকে?"),
            ("Which signals would have alerted you before users noticed?", "User-রা টের পাওয়ার আগেই কোন signal তোমাকে সতর্ক করত?"),
            ("How do you tell a retrieval regression from a generation regression?", "Retrieval regression আর generation regression কীভাবে আলাদা করবে?"),
        ],
        related=["vec-028", "vec-024", "vec-015", "vec-018"],
        refs=[PGV, WIKI_IREVAL, OWASP_LLM08],
    ),
]

if __name__ == "__main__":
    save("vectordb", "b4", QUESTIONS)
