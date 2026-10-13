# Vector Databases — batch 2 (vec-005, 006, 007, 014, 015, 016, 024, 025)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PGV = ("pgvector — README (GitHub)", "https://github.com/pgvector/pgvector")
PG_FTS = ("PostgreSQL docs — Full Text Search", "https://www.postgresql.org/docs/current/textsearch.html")
WIKI_BM25 = ("Wikipedia — Okapi BM25", "https://en.wikipedia.org/wiki/Okapi_BM25")
WIKI_NNS = ("Wikipedia — Nearest neighbor search", "https://en.wikipedia.org/wiki/Nearest_neighbor_search")
HNSW_PAPER = ("Malkov & Yashunin — HNSW paper (arXiv)", "https://arxiv.org/abs/1603.09320")
PINECONE_VDB = ("Pinecone — What is a vector database?", "https://www.pinecone.io/learn/vector-database/")
PINECONE_CHUNK = ("Pinecone — Chunking strategies for LLM applications", "https://www.pinecone.io/learn/chunking-strategies/")
QDRANT_HYBRID = ("Qdrant docs — Hybrid and multi-stage queries", "https://qdrant.tech/documentation/concepts/hybrid-queries/")
E5 = ("Hugging Face — multilingual-e5-base model card", "https://huggingface.co/intfloat/multilingual-e5-base")
MATRYOSHKA = ("Kusupati et al. — Matryoshka Representation Learning (arXiv)", "https://arxiv.org/abs/2205.13147")

QUESTIONS = [
    # ------------------------------------------------------------------ vec-005
    Q(
        id="vec-005", sub="Vector DBs vs Full-Text Search", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["semantic-search", "full-text-search", "bm25", "keyword-search"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""What's the difference between semantic (vector) search and keyword/full-text search like BM25? When does each one win?""",
        q_bn=r"""Semantic (vector) search আর BM25-এর মতো keyword/full-text search-এর পার্থক্য কী? কখন কোনটা ভালো কাজ করে?""",
        a_en=r"""
            **Keyword / full-text search (BM25):** builds an inverted index of words and scores documents by how often the query terms appear, how rare those terms are across the collection, and document length.
            - Wins at **exact matches**: product codes, model numbers, names, error messages ("Redmi Note 13", "ERR_CONNECTION_RESET").
            - Cheap, fast, explainable ("matched these words").
            - Misses synonyms and paraphrases: "phone case" won't match "mobile cover".

            **Semantic search:** compares embeddings, so it matches **meaning**.
            - Wins on synonyms, paraphrases, natural-language questions and even cross-language matches with a multilingual model ("cheap phone" ↔ "সস্তা মোবাইল").
            - Weaker on exact identifiers, numbers, rare jargon and negation, and its results are harder to explain.

            In production I usually combine them — **hybrid search** — so exact matches and meaning both count.
        """,
        a_bn=r"""
            **Keyword / full-text search (BM25):** শব্দের একটা inverted index তৈরি করে, আর document-কে score দেয় query-র শব্দ কতবার আছে, সেই শব্দ পুরো collection-এ কতটা বিরল, আর document-এর দৈর্ঘ্য দেখে।
            - **Exact match**-এ জেতে: product code, model number, নাম, error message ("Redmi Note 13", "ERR_CONNECTION_RESET")।
            - সস্তা, দ্রুত, ব্যাখ্যা করা যায় ("এই শব্দগুলো মিলেছে")।
            - Synonym আর ভিন্নভাবে বলা কথা ধরতে পারে না: "phone case" দিয়ে "mobile cover" পাওয়া যায় না।

            **Semantic search:** embedding তুলনা করে, তাই **অর্থ** মেলায়।
            - Synonym, ভিন্নভাবে বলা কথা, স্বাভাবিক ভাষার প্রশ্ন, এমনকি multilingual model দিয়ে ভাষা পেরিয়েও মেলাতে পারে ("cheap phone" ↔ "সস্তা মোবাইল")।
            - Exact identifier, সংখ্যা, বিরল jargon আর negation-এ দুর্বল, আর result ব্যাখ্যা করা কঠিন।

            Production-এ আমি সাধারণত দুটো মেলাই — **hybrid search** — যাতে exact match আর অর্থ দুটোই গুরুত্ব পায়।
        """,
        ex_en=r"""
            - **Negation example:** "laptop without touchscreen" embeds very close to "touchscreen laptop"; keyword search with a filter or query parsing handles it better.
            - **Language tooling:** full-text search depends on tokenisers and stemmers per language. Check whether your engine has a proper analyser for Bangla; if not, a simple (no-stemming) configuration or n-gram matching is the fallback, and a multilingual embedding model can cover the gap.
            - **Cost:** semantic search needs an embedding call per query and more memory for vectors; keyword search runs on modest hardware.
            - **In PostgreSQL** you can do both in one database: `tsvector`/`tsquery` full-text search plus pgvector.
        """,
        ex_bn=r"""
            - **Negation-এর উদাহরণ:** "laptop without touchscreen"-এর embedding "touchscreen laptop"-এর খুব কাছে পড়ে; filter বা query parsing সহ keyword search এটা ভালো সামলায়।
            - **ভাষার tooling:** full-text search প্রতিটা ভাষার tokeniser আর stemmer-এর ওপর নির্ভর করে। তোমার engine-এ Bangla-র জন্য ঠিকঠাক analyser আছে কিনা দেখো; না থাকলে simple (stemming ছাড়া) configuration বা n-gram matching হলো বিকল্প, আর multilingual embedding model সেই ঘাটতি পূরণ করতে পারে।
            - **খরচ:** semantic search-এ প্রতি query-তে একটা embedding call আর vector-এর জন্য বেশি memory লাগে; keyword search সাধারণ hardware-এই চলে।
            - **PostgreSQL-এ** এক database-এই দুটো করা যায়: `tsvector`/`tsquery` full-text search আর pgvector।
        """,
        tip_en=r"""Give one query where keyword search wins (a model number) and one where semantic wins (a paraphrase), then conclude with hybrid. Concrete examples beat abstract definitions.""",
        tip_bn=r"""একটা query দাও যেখানে keyword search জেতে (একটা model number) আর একটা যেখানে semantic জেতে (ভিন্নভাবে বলা কথা), তারপর hybrid দিয়ে শেষ করো। বিমূর্ত definition-এর চেয়ে concrete উদাহরণ বেশি কাজ করে।""",
        mist_en=r"""Claiming semantic search makes keyword search obsolete, or that BM25 "understands" synonyms.""",
        mist_bn=r"""দাবি করা যে semantic search keyword search-কে অপ্রয়োজনীয় করে দিয়েছে, অথবা BM25 synonym "বোঝে"।""",
        follow=[
            ("How would you combine BM25 and vector scores that are on completely different scales?", "সম্পূর্ণ আলাদা scale-এর BM25 আর vector score কীভাবে মেলাবে?"),
            ("Why is negation hard for embedding-based search?", "Embedding-ভিত্তিক search-এর জন্য negation কেন কঠিন?"),
        ],
        related=["vec-016", "vec-001"],
        refs=[WIKI_BM25, PG_FTS, PGV],
    ),
    # ------------------------------------------------------------------ vec-006
    Q(
        id="vec-006", sub="Approximate Nearest Neighbour (ANN) Search", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["ann", "knn", "recall", "performance"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""Why do most vector databases use approximate nearest neighbour (ANN) indexes instead of exact k-NN search?""",
        q_bn=r"""বেশিরভাগ vector database কেন exact k-NN search-এর বদলে approximate nearest neighbour (ANN) index ব্যবহার করে?""",
        options=[
            ("Exact search compares the query with every vector, which is too slow at millions of vectors; ANN returns nearly the same top results far faster by trading a little recall", "Exact search query-কে প্রতিটা vector-এর সাথে তুলনা করে, যেটা লাখো vector-এ খুব ধীর; ANN সামান্য recall ছেড়ে দিয়ে প্রায় একই top result অনেক দ্রুত দেয়"),
            ("Exact k-NN gives wrong answers for high-dimensional vectors", "High-dimensional vector-এ exact k-NN ভুল উত্তর দেয়"),
            ("ANN is more accurate than exact search because it uses a graph", "Graph ব্যবহার করে বলে ANN exact search-এর চেয়েও বেশি accurate"),
            ("ANN is required because SQL databases cannot sort by distance", "SQL database distance দিয়ে sort করতে পারে না বলে ANN দরকার"),
        ],
        correct=0,
        a_en=r"""Exact k-NN is a brute-force scan — cost grows linearly with the number of vectors and their dimension. ANN indexes such as HNSW or IVF only examine a small, promising part of the data, so queries stay fast at millions of vectors, at the price of occasionally missing a true neighbour.""",
        a_bn=r"""Exact k-NN হলো brute-force scan — খরচ vector-এর সংখ্যা আর dimension-এর সাথে সরলরৈখিকভাবে বাড়ে। HNSW বা IVF-এর মতো ANN index data-র শুধু ছোট, সম্ভাবনাময় একটা অংশ দেখে, তাই লাখো vector-এও query দ্রুত থাকে — বিনিময়ে মাঝে মাঝে একটা আসল neighbour বাদ পড়তে পারে।""",
        ex_en=r"""
            Exact search is *always* correct, so option B is wrong, and option C reverses the trade-off — ANN can only match exact search's accuracy, never beat it. Option D is false: pgvector, for example, does exact search with `ORDER BY embedding <=> $1 LIMIT k` when no index exists.

            The quality of ANN is measured as **recall@k**: of the true top-k neighbours, how many did the index return? You tune it with parameters like `hnsw.ef_search` or `ivfflat.probes` — higher means better recall but slower queries. For small collections (tens of thousands of vectors), exact search is often fast enough and gives perfect recall, so an index isn't always needed.
        """,
        ex_bn=r"""
            Exact search *সবসময়* সঠিক, তাই option B ভুল; আর option C trade-off-টা উল্টে দেয় — ANN বড়জোর exact search-এর সমান accurate হতে পারে, বেশি কখনো নয়। Option D মিথ্যা: যেমন pgvector index না থাকলে `ORDER BY embedding <=> $1 LIMIT k` দিয়ে exact search করে।

            ANN-এর মান মাপা হয় **recall@k** দিয়ে: আসল top-k neighbour-এর মধ্যে index কয়টা ফেরত দিল? এটা tune করা হয় `hnsw.ef_search` বা `ivfflat.probes`-এর মতো parameter দিয়ে — বেশি দিলে recall ভালো, কিন্তু query ধীর। ছোট collection-এ (কয়েক দশ হাজার vector পর্যন্ত) exact search প্রায়ই যথেষ্ট দ্রুত আর perfect recall দেয়, তাই সবসময় index লাগে না।
        """,
        tip_en=r"""Use the phrase "speed–recall trade-off" and name the knob (`ef_search`, `probes`). It shows you know ANN is tunable, not magic.""",
        tip_bn=r""""Speed–recall trade-off" কথাটা ব্যবহার করো আর knob-এর নাম বলো (`ef_search`, `probes`)। এতে বোঝা যায় তুমি জানো ANN tune করা যায়, এটা জাদু নয়।""",
        refs=[WIKI_NNS, PGV],
        related=["vec-003", "vec-014"],
    ),
    # ------------------------------------------------------------------ vec-007
    Q(
        id="vec-007", sub="Chunking", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["chunking", "overlap", "rag", "embeddings"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""Why do we split documents into chunks before embedding them, and how do you choose the chunk size and overlap?""",
        q_bn=r"""Embed করার আগে document-কে chunk-এ ভাগ করি কেন, আর chunk size ও overlap কীভাবে ঠিক করো?""",
        a_en=r"""
            We chunk for three reasons:
            - **Model limits:** embedding models accept a limited number of tokens; longer text gets truncated.
            - **Precise retrieval:** one vector for a 40-page PDF averages everything into a blurry meaning. Smaller chunks let a query match the exact section that answers it.
            - **LLM context budget:** in RAG we can only send a few passages to the LLM, so they should be focused.

            **Choosing size:** too large → diluted embeddings and wasted context; too small → chunks lose the context needed to make sense ("it", "this policy"). A common starting point is a few hundred tokens, then measure.

            **Overlap** (e.g. 10–20%) repeats a little text between neighbouring chunks so a sentence or idea split at a boundary still appears whole in at least one chunk.

            Better than fixed sizes: **split by structure** — headings, paragraphs, list items — and prepend the document title and section heading to each chunk.
        """,
        a_bn=r"""
            Chunk করার তিনটা কারণ:
            - **Model-এর সীমা:** embedding model সীমিত সংখ্যক token নেয়; লম্বা text কেটে ফেলা হয়।
            - **নিখুঁত retrieval:** 40 পাতার PDF-এর জন্য একটা vector সবকিছু গড় করে একটা ঝাপসা অর্থ তৈরি করে। ছোট chunk থাকলে query ঠিক সেই অংশের সাথে মেলে যেখানে উত্তর আছে।
            - **LLM context budget:** RAG-এ LLM-কে অল্প কয়েকটা passage-ই পাঠানো যায়, তাই সেগুলো focused হওয়া দরকার।

            **Size ঠিক করা:** খুব বড় → embedding ঝাপসা আর context-এর অপচয়; খুব ছোট → chunk অর্থ বোঝার মতো context হারায় ("এটা", "এই policy")। সাধারণ শুরু কয়েকশো token, তারপর মেপে দেখো।

            **Overlap** (যেমন 10–20%) পাশাপাশি chunk-এর মধ্যে সামান্য text পুনরাবৃত্তি করে, যাতে boundary-তে ভাগ হয়ে যাওয়া বাক্য বা ধারণা অন্তত একটা chunk-এ পুরোটা থাকে।

            Fixed size-এর চেয়ে ভালো: **কাঠামো অনুযায়ী ভাগ করা** — heading, paragraph, list item — আর প্রতিটা chunk-এর শুরুতে document-এর title ও section heading জুড়ে দেওয়া।
        """,
        ex_en=r"""
            - **Words aren't tokens:** models count tokens, and Bangla text often uses more tokens per word than English with many tokenisers — size chunks by the model's tokeniser, not by characters.
            - **Keep units intact:** don't cut tables, code blocks or numbered steps in half; convert tables to text rows that each make sense alone.
            - **Metadata travels with the chunk:** store doc id, title, section and position so you can cite sources and fetch neighbouring chunks.
            - **No universal best size:** the right size depends on your documents and questions — evaluate with a small golden set of real queries.
        """,
        ex_bn=r"""
            - **শব্দ মানে token নয়:** model token গোনে, আর অনেক tokeniser-এ Bangla text-এ প্রতি শব্দে English-এর চেয়ে বেশি token লাগে — character নয়, model-এর tokeniser দিয়ে chunk-এর আকার ঠিক করো।
            - **একক অংশ অক্ষত রাখো:** table, code block বা নম্বরযুক্ত ধাপ মাঝখান দিয়ে কেটো না; table-কে এমন text row-তে বদলাও যেগুলো আলাদাভাবেও অর্থবহ।
            - **Metadata chunk-এর সাথে যায়:** doc id, title, section আর অবস্থান store করো, যাতে source cite করা আর পাশের chunk আনা যায়।
            - **সবার জন্য একটা সেরা size নেই:** সঠিক size তোমার document আর প্রশ্নের ওপর নির্ভর করে — আসল query-র ছোট একটা golden set দিয়ে মূল্যায়ন করো।
        """,
        tip_en=r"""Explain the trade-off (too big vs too small) with a concrete example, then say you'd validate the choice with retrieval metrics. "It depends — and here's how I'd measure it" is the strong answer.""",
        tip_bn=r"""একটা concrete উদাহরণ দিয়ে trade-off (খুব বড় বনাম খুব ছোট) ব্যাখ্যা করো, তারপর বলো retrieval metric দিয়ে সিদ্ধান্তটা যাচাই করবে। "নির্ভর করে — আর এভাবে আমি মাপব" — এটাই শক্তিশালী উত্তর।""",
        mist_en=r"""Embedding whole documents as one vector, cutting chunks by raw character count through the middle of tables, or never revisiting chunk size after launch.""",
        mist_bn=r"""পুরো document একটা vector হিসেবে embed করা, raw character গুনে table-এর মাঝখান দিয়ে chunk কাটা, অথবা launch-এর পর আর কখনো chunk size নিয়ে ভাবা না।""",
        code=r"""
            // Naive word-based chunker with overlap.
            // Real pipelines split on headings/paragraphs first and measure size in model tokens.
            function chunkText(text, { size = 300, overlap = 50 } = {}) {
              if (overlap >= size) throw new Error('overlap must be smaller than size');
              const words = text.split(/\s+/).filter(Boolean);
              const chunks = [];
              for (let start = 0; start < words.length; start += size - overlap) {
                chunks.push(words.slice(start, start + size).join(' '));
                if (start + size >= words.length) break;
              }
              return chunks;
            }

            // 700 words -> chunks covering words 1-300, 251-550, 501-700
            const longText = Array.from({ length: 700 }, (_, i) => `w${i + 1}`).join(' ');
            console.log(chunkText(longText, { size: 300, overlap: 50 }).length);
        """,
        lang="javascript", output=r"""3""",
        follow=[
            ("How would you chunk a document that contains large tables?", "বড় table থাকা document কীভাবে chunk করবে?"),
            ("What is 'parent-child' (small-to-big) retrieval?", "'Parent-child' (small-to-big) retrieval কী?"),
        ],
        related=["vec-015", "vec-008"],
        refs=[PINECONE_CHUNK, E5],
    ),
    # ------------------------------------------------------------------ vec-014
    Q(
        id="vec-014", sub="Vector Indexing Fundamentals", diff="medium", type="comparison",
        prio="high", market="both", mins=8,
        tags=["hnsw", "ivfflat", "ann-index", "pgvector", "tuning"],
        ver="pgvector 0.8.7 (PostgreSQL 18)", vs=True, status="stable",
        q_en=r"""Compare HNSW and IVFFlat indexes (as in pgvector) with a flat/brute-force search. How does each work at a high level, what are the tuning knobs, and when would you pick each?""",
        q_bn=r"""HNSW আর IVFFlat index (pgvector-এ যেমন) flat/brute-force search-এর সাথে তুলনা করো। প্রতিটা মোটা দাগে কীভাবে কাজ করে, tuning-এর knob কী, আর কখন কোনটা বেছে নেবে?""",
        a_en=r"""
            **Flat (no index):** compare the query with every vector. Perfect recall, simple, no build time — fine up to tens of thousands of vectors or when filters already shrink the set.

            **HNSW (Hierarchical Navigable Small World):** a multi-layer graph where each vector links to its near neighbours. A search starts at a sparse top layer, greedily hops towards the query, and refines in denser layers below — like taking a highway, then main roads, then side streets.
            - Knobs: `m` (links per node, pgvector default 16) and `ef_construction` (build-time candidate list, default 64) affect quality, memory and build time; `hnsw.ef_search` (default 40) trades query speed for recall.
            - Pros: excellent speed/recall, can be created on an empty table and handles inserts well. Cons: slower to build, more memory.

            **IVFFlat (inverted file):** k-means splits vectors into `lists` clusters; a query only scans the `probes` closest clusters.
            - Knobs: `lists` (pgvector suggests rows/1000 up to 1M rows, √rows above) and `ivfflat.probes` (default 1; start around √lists).
            - Pros: faster build, less memory. Cons: generally a worse speed/recall trade-off than HNSW, must be built **after** data is loaded, and recall drifts as new data changes the distribution — rebuild periodically.

            My default is HNSW; IVFFlat when build time or memory is the constraint; flat for small or heavily filtered sets.
        """,
        a_bn=r"""
            **Flat (index নেই):** query-কে প্রতিটা vector-এর সাথে তুলনা করো। Perfect recall, সহজ, build time নেই — কয়েক দশ হাজার vector পর্যন্ত বা filter আগেই set ছোট করে দিলে যথেষ্ট।

            **HNSW (Hierarchical Navigable Small World):** একটা multi-layer graph, যেখানে প্রতিটা vector তার কাছের neighbour-দের সাথে যুক্ত। Search শুরু হয় হালকা উপরের layer থেকে, লোভীভাবে query-র দিকে লাফিয়ে এগোয়, তারপর নিচের ঘন layer-এ সূক্ষ্মভাবে খোঁজে — অনেকটা আগে highway, তারপর বড় রাস্তা, শেষে গলিপথ ধরার মতো।
            - Knob: `m` (প্রতি node-এ link, pgvector default 16) আর `ef_construction` (build-এর সময় candidate list, default 64) quality, memory আর build time-এ প্রভাব ফেলে; `hnsw.ef_search` (default 40) query speed-এর বিনিময়ে recall বাড়ায়।
            - সুবিধা: চমৎকার speed/recall, খালি table-এও তৈরি করা যায় আর insert ভালো সামলায়। অসুবিধা: build ধীর, memory বেশি।

            **IVFFlat (inverted file):** k-means vector-গুলোকে `lists`-সংখ্যক cluster-এ ভাগ করে; query শুধু সবচেয়ে কাছের `probes`-সংখ্যক cluster scan করে।
            - Knob: `lists` (pgvector-এর পরামর্শ 1M row পর্যন্ত rows/1000, তার ওপরে √rows) আর `ivfflat.probes` (default 1; শুরু করো √lists-এর কাছাকাছি)।
            - সুবিধা: দ্রুত build, কম memory। অসুবিধা: সাধারণত HNSW-এর চেয়ে খারাপ speed/recall, data load করার **পরে** build করতে হয়, আর নতুন data distribution বদলালে recall কমে যায় — নিয়মিত rebuild করো।

            আমার default HNSW; build time বা memory সীমাবদ্ধতা হলে IVFFlat; ছোট বা অনেক বেশি filter করা set-এর জন্য flat।
        """,
        ex_en=r"""
            - **Why IVFFlat needs data first:** its cluster centroids are learned from the rows present at build time; built on an empty or tiny table, the lists are poor and queries return fewer results.
            - **Memory matters:** HNSW performs best when the index fits in RAM (`shared_buffers` + OS cache). Index builds also benefit from a larger `maintenance_work_mem` — pgvector logs a notice when the graph no longer fits.
            - **Operator class must match the query:** an index built with `vector_cosine_ops` only serves `<=>` queries.
            - **Measure recall:** compare ANN results against an exact query (e.g. with the index disabled) on a sample of queries before choosing parameters.
            - **Other engines:** dedicated vector DBs offer the same ideas plus extras (product/binary quantisation, disk-based indexes, filter-aware graphs).
        """,
        ex_bn=r"""
            - **IVFFlat-এ আগে data কেন লাগে:** এর cluster centroid build-এর সময় থাকা row থেকে শেখা হয়; খালি বা খুব ছোট table-এ build করলে list খারাপ হয় আর query কম result দেয়।
            - **Memory গুরুত্বপূর্ণ:** index RAM-এ (`shared_buffers` + OS cache) আঁটলে HNSW সবচেয়ে ভালো চলে। বড় `maintenance_work_mem` index build-এও সাহায্য করে — graph আর না আঁটলে pgvector একটা notice log করে।
            - **Operator class query-র সাথে মিলতে হবে:** `vector_cosine_ops` দিয়ে তৈরি index শুধু `<=>` query serve করে।
            - **Recall মাপো:** parameter বেছে নেওয়ার আগে কিছু query-তে ANN result-কে exact query-র (যেমন index বন্ধ রেখে) সাথে তুলনা করো।
            - **অন্য engine:** dedicated vector DB একই ধারণার সাথে বাড়তি সুবিধা দেয় (product/binary quantisation, disk-based index, filter-aware graph)।
        """,
        tip_en=r"""Give the intuition (graph of neighbours vs clusters) before the parameters. An analogy like "highway → main road → side street" for HNSW makes the answer memorable without heavy math.""",
        tip_bn=r"""Parameter-এর আগে intuition দাও (neighbour-এর graph বনাম cluster)। HNSW-এর জন্য "highway → বড় রাস্তা → গলি"-র মতো উপমা ভারী math ছাড়াই উত্তরটা মনে রাখার মতো করে।""",
        mist_en=r"""Creating an IVFFlat index on an empty table, expecting `ef_search` changes to need a reindex (it's a query-time setting), or comparing indexes without measuring recall.""",
        mist_bn=r"""খালি table-এ IVFFlat index তৈরি করা, ভাবা যে `ef_search` বদলাতে reindex লাগে (এটা query-time setting), অথবা recall না মেপেই index তুলনা করা।""",
        code=r"""
            -- HNSW: good default; can be created before data arrives
            CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops)
              WITH (m = 16, ef_construction = 64);
            SET hnsw.ef_search = 100;            -- per session/transaction: higher = better recall, slower

            -- IVFFlat: build AFTER loading data
            CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops)
              WITH (lists = 1000);               -- ~rows/1000 for up to 1M rows
            SET ivfflat.probes = 32;             -- start near sqrt(lists)
        """,
        lang="sql",
        follow=[
            ("How would you measure the recall of your HNSW index in production?", "Production-এ তোমার HNSW index-এর recall কীভাবে মাপবে?"),
            ("What happens to an HNSW index when you delete many rows?", "অনেক row delete করলে HNSW index-এর কী হয়?"),
        ],
        related=["vec-006", "vec-027", "vec-025"],
        refs=[PGV, HNSW_PAPER, PINECONE_VDB],
    ),
    # ------------------------------------------------------------------ vec-015
    Q(
        id="vec-015", sub="Chunking", diff="medium", type="scenario",
        prio="medium", market="both", mins=8,
        tags=["chunking", "rag", "bangla", "tables", "evaluation"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""Your RAG assistant answers questions from company HR policy PDFs written in Bangla and English. Users report that it misses details, and answers about leave rules quote half a table. The current pipeline splits text every 1,000 characters with no overlap. How do you fix the chunking?""",
        q_bn=r"""তোমার RAG assistant Bangla আর English-এ লেখা company-র HR policy PDF থেকে প্রশ্নের উত্তর দেয়। User-রা বলছে এটা খুঁটিনাটি বাদ দেয়, আর ছুটির নিয়ম নিয়ে উত্তরে একটা table-এর অর্ধেক quote করে। বর্তমান pipeline প্রতি 1,000 character-এ text কাটে, কোনো overlap ছাড়া। Chunking কীভাবে ঠিক করবে?""",
        a_en=r"""
            **1. Diagnose first.** Collect 20–30 failing questions and look at what was retrieved. Is the right content split across chunks, missing (bad PDF extraction), or present but ranked low? That decides the fix.

            **2. Fix extraction.** Make sure tables come out as structured rows and scanned pages are OCR'd; garbage in, garbage out.

            **3. Chunk by structure, not by characters.**
            - Split on headings and sections ("ছুটি নীতি / Leave Policy"), then paragraphs; use the embedding model's token count for size (a few hundred tokens) with ~10–20% overlap.
            - Use a sentence splitter that understands Bangla — Bangla sentences end with "।" (dari), so a splitter that only looks for "." produces huge, broken chunks.
            - **Keep tables whole**, or turn each row into a self-contained sentence: "Annual leave — permanent staff — 20 days per year".

            **4. Add context to every chunk.** Prepend document title and section path ("HR Policy 2026 › Leave › Annual leave") before embedding, and store it as metadata for citations.

            **5. Consider small-to-big retrieval.** Retrieve small precise chunks, but send the LLM the parent section so it sees the whole table.

            **6. Re-evaluate** on the failing set plus a broader golden set; compare recall@k before and after.
        """,
        a_bn=r"""
            **1. আগে diagnose করো।** 20–30টা fail হওয়া প্রশ্ন জোগাড় করে দেখো কী retrieve হয়েছে। সঠিক content কি কয়েকটা chunk-এ ভাগ হয়ে গেছে, একেবারে নেই (PDF extraction খারাপ), নাকি আছে কিন্তু নিচে rank হয়েছে? এটাই ঠিক করবে সমাধান কী।

            **2. Extraction ঠিক করো।** Table যেন structured row হিসেবে বের হয় আর scan করা পাতায় OCR হয়, নিশ্চিত করো; ভুল input মানেই ভুল output।

            **3. Character নয়, কাঠামো অনুযায়ী chunk করো।**
            - Heading আর section ("ছুটি নীতি / Leave Policy") ধরে ভাগ করো, তারপর paragraph; size ঠিক করো embedding model-এর token গুনে (কয়েকশো token), ~10–20% overlap সহ।
            - এমন sentence splitter ব্যবহার করো যেটা Bangla বোঝে — Bangla বাক্য শেষ হয় "।" (দাঁড়ি) দিয়ে, তাই শুধু "." খোঁজা splitter বিশাল, ভাঙা chunk তৈরি করে।
            - **Table অক্ষত রাখো**, অথবা প্রতিটা row-কে স্বয়ংসম্পূর্ণ বাক্যে বদলাও: "Annual leave — permanent staff — বছরে 20 দিন"।

            **4. প্রতিটা chunk-এ context যোগ করো।** Embed করার আগে document title আর section path ("HR Policy 2026 › Leave › Annual leave") জুড়ে দাও, আর citation-এর জন্য metadata হিসেবেও রাখো।

            **5. Small-to-big retrieval বিবেচনা করো।** ছোট নিখুঁত chunk দিয়ে retrieve করো, কিন্তু LLM-কে পাঠাও parent section, যাতে পুরো table দেখতে পায়।

            **6. আবার মূল্যায়ন করো** fail হওয়া set আর বড় একটা golden set দিয়ে; আগে-পরে recall@k তুলনা করো।
        """,
        ex_en=r"""
            - **Why fixed 1,000-character splits hurt:** they cut mid-sentence and mid-table, and in Bangla a fixed character count means very different token counts than in English.
            - **Mixed-language documents:** detect language per chunk and store it as metadata; it helps filtering and evaluation, and confirms your embedding model handles both.
            - **Re-ingestion:** changing the chunker changes chunk ids — plan a full re-index and keep the old index until the new one is evaluated.
            - **Watch duplicates:** with overlap and near-identical policy versions, the top results can all be the same paragraph; de-duplicate or diversify results before sending them to the LLM.
        """,
        ex_bn=r"""
            - **নির্দিষ্ট 1,000-character ভাগ কেন ক্ষতিকর:** বাক্য আর table-এর মাঝখান দিয়ে কাটে, আর Bangla-য় নির্দিষ্ট character সংখ্যা মানে English-এর তুলনায় অনেক আলাদা token সংখ্যা।
            - **মিশ্র ভাষার document:** প্রতিটা chunk-এর ভাষা শনাক্ত করে metadata হিসেবে রাখো; filtering আর evaluation-এ কাজে লাগে, আর নিশ্চিত হওয়া যায় embedding model দুটো ভাষাই সামলাচ্ছে।
            - **আবার ingest:** chunker বদলালে chunk id বদলায় — পুরো re-index plan করো, আর নতুনটা মূল্যায়ন না হওয়া পর্যন্ত পুরনো index রেখে দাও।
            - **Duplicate খেয়াল রাখো:** overlap আর প্রায়-একই policy version থাকলে top result-গুলো সব একই paragraph হতে পারে; LLM-এ পাঠানোর আগে de-duplicate বা diversify করো।
        """,
        tip_en=r"""Start with "I'd look at the retrieved chunks for failing questions" — diagnosis before solutions. Mentioning the Bangla "।" sentence boundary shows real local experience.""",
        tip_bn=r""""Fail হওয়া প্রশ্নের retrieve হওয়া chunk-গুলো আগে দেখব" দিয়ে শুরু করো — সমাধানের আগে diagnosis। Bangla-র "।" দিয়ে বাক্য শেষ হওয়ার কথা বললে বাস্তব local অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Jumping straight to "use a bigger LLM" or "increase top-k" without checking whether the right text was ever in a single chunk.""",
        mist_bn=r"""সঠিক text কখনো একটা chunk-এ ছিল কিনা না দেখে সরাসরি "বড় LLM ব্যবহার করো" বা "top-k বাড়াও"-তে চলে যাওয়া।""",
        follow=[
            ("How would you measure whether the new chunking is actually better?", "নতুন chunking আসলেই ভালো কিনা কীভাবে মাপবে?"),
            ("When does semantic chunking (splitting where the topic changes) help?", "Semantic chunking (যেখানে topic বদলায় সেখানে ভাগ করা) কখন সাহায্য করে?"),
        ],
        related=["vec-007", "vec-017", "vec-032"],
        refs=[PINECONE_CHUNK, E5],
    ),
    # ------------------------------------------------------------------ vec-016
    Q(
        id="vec-016", sub="Hybrid Search", diff="medium", type="coding",
        prio="high", market="both", mins=10,
        tags=["hybrid-search", "rrf", "bm25", "ranking", "javascript"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""
            Implement **Reciprocal Rank Fusion (RRF)** in JavaScript to merge the results of a keyword (BM25) search and a vector search into one ranking.

            - Input: an array of ranked lists of document ids (best first), plus `k` (default 60) and `limit`.
            - Each document's score is the sum over lists of `1 / (k + rank)`, with rank starting at 1.
            - Return the top `limit` documents as `{ id, score }`, highest score first.

            Example: keyword = `['p7', 'p2', 'p9']`, semantic = `['p2', 'p4', 'p7']`, `k = 60`, `limit = 3` → `p2`, `p7`, `p4`.
        """,
        q_bn=r"""
            একটা keyword (BM25) search আর একটা vector search-এর result একটা ranking-এ মেলাতে JavaScript-এ **Reciprocal Rank Fusion (RRF)** implement করো।

            - Input: document id-এর ranked list-এর একটা array (সেরাটা আগে), সাথে `k` (default 60) আর `limit`।
            - প্রতিটা document-এর score হলো সব list মিলিয়ে `1 / (k + rank)`-এর যোগফল, rank শুরু 1 থেকে।
            - সবচেয়ে বেশি score আগে রেখে top `limit`টা document `{ id, score }` হিসেবে return করো।

            উদাহরণ: keyword = `['p7', 'p2', 'p9']`, semantic = `['p2', 'p4', 'p7']`, `k = 60`, `limit = 3` → `p2`, `p7`, `p4`।
        """,
        a_en=r"""
            RRF ignores the raw scores and uses only **positions**, which is exactly why it's popular for hybrid search: BM25 scores and cosine similarities live on completely different scales, but ranks are comparable.

            For each list I walk the ids with their 1-based rank and add `1 / (k + rank)` to a running total in a `Map`. A document ranked well in *both* lists accumulates two contributions and rises to the top; a document found by only one retriever still gets credit. Then I sort by score and take the top `limit`.

            In the example, `p2` gets 1/62 + 1/61 ≈ 0.03252 and `p7` gets 1/61 + 1/63 ≈ 0.03227, so `p2` edges out `p7`; `p4` (only in the vector list, rank 2) beats `p9` (only in the keyword list, rank 3).
        """,
        a_bn=r"""
            RRF raw score উপেক্ষা করে শুধু **অবস্থান** ব্যবহার করে — hybrid search-এ এটা জনপ্রিয় ঠিক এই কারণেই: BM25 score আর cosine similarity সম্পূর্ণ আলাদা scale-এ থাকে, কিন্তু rank তুলনা করা যায়।

            প্রতিটা list-এর id-গুলো তাদের 1-based rank সহ ঘুরে দেখি আর একটা `Map`-এ চলমান যোগফলে `1 / (k + rank)` যোগ করি। *দুই* list-এই ভালো rank পাওয়া document দুইবার অবদান জমিয়ে উপরে ওঠে; শুধু একটা retriever-এ পাওয়া document-ও কিছু credit পায়। তারপর score অনুযায়ী sort করে top `limit`টা নিই।

            উদাহরণে `p2` পায় 1/62 + 1/61 ≈ 0.03252 আর `p7` পায় 1/61 + 1/63 ≈ 0.03227, তাই `p2` সামান্য ব্যবধানে `p7`-এর আগে; `p4` (শুধু vector list-এ, rank 2) `p9`-কে (শুধু keyword list-এ, rank 3) হারায়।
        """,
        ex_en=r"""
            - **Why `k`?** It dampens the advantage of the very top ranks so one list can't dominate. 60 comes from the original RRF paper and is a common default; some engines use other defaults (Qdrant's documentation, for example, uses a smaller constant), so treat it as tunable.
            - **Edge cases:** duplicate ids inside one list (count only the first occurrence), empty lists, ties (break them deterministically, e.g. by id), and `limit` larger than the number of unique ids.
            - **Alternatives:** a weighted sum of *normalised* scores (convex combination) can beat RRF when tuned on labelled data, but it's sensitive to score distributions. RRF is a robust, tuning-free start.
            - **Pipeline:** retrieve ~50–100 from each retriever, fuse with RRF, then rerank the top few dozen with a cross-encoder if you need higher precision.
        """,
        ex_bn=r"""
            - **`k` কেন?** এটা একেবারে উপরের rank-গুলোর সুবিধা কিছুটা কমায়, যাতে একটা list একাই প্রাধান্য না পায়। 60 এসেছে মূল RRF paper থেকে আর এটা প্রচলিত default; কিছু engine অন্য default ব্যবহার করে (যেমন Qdrant-এর documentation ছোট একটা constant ব্যবহার করে), তাই এটাকে tune করার মতো ধরো।
            - **Edge case:** একই list-এ duplicate id (শুধু প্রথমটা গোনো), খালি list, tie (নির্দিষ্টভাবে ভাঙো, যেমন id দিয়ে), আর unique id-এর চেয়ে বড় `limit`।
            - **বিকল্প:** *normalised* score-এর weighted যোগফল (convex combination) labelled data-য় tune করলে RRF-কে ছাড়িয়ে যেতে পারে, কিন্তু score distribution-এর প্রতি সংবেদনশীল। RRF tuning ছাড়াই নির্ভরযোগ্য শুরু।
            - **Pipeline:** প্রতিটা retriever থেকে ~50–100টা আনো, RRF দিয়ে মেলাও, তারপর আরও precision লাগলে top কয়েক ডজন cross-encoder দিয়ে rerank করো।
        """,
        tip_en=r"""Before coding, explain *why* ranks instead of scores (incomparable scales). Then walk through the example numbers — it proves your implementation is right.""",
        tip_bn=r"""Code লেখার আগে ব্যাখ্যা করো score-এর বদলে rank *কেন* (scale তুলনীয় নয়)। তারপর উদাহরণের সংখ্যাগুলো হিসাব করে দেখাও — এতেই প্রমাণ হয় তোমার implementation ঠিক।""",
        mist_en=r"""Adding raw BM25 and cosine scores directly, using 0-based ranks (changes the scores), or counting a duplicate id twice within the same list.""",
        mist_bn=r"""Raw BM25 আর cosine score সরাসরি যোগ করা, 0-based rank ব্যবহার করা (score বদলে যায়), অথবা একই list-এ duplicate id দুইবার গোনা।""",
        code=r"""
            function reciprocalRankFusion(rankedLists, { k = 60, limit = 10 } = {}) {
              const scores = new Map();

              for (const list of rankedLists) {
                const seen = new Set();
                list.forEach((id, index) => {
                  if (seen.has(id)) return;            // ignore duplicates inside one list
                  seen.add(id);
                  const rank = index + 1;              // ranks start at 1
                  scores.set(id, (scores.get(id) ?? 0) + 1 / (k + rank));
                });
              }

              return [...scores.entries()]
                .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])))
                .slice(0, limit)
                .map(([id, score]) => ({ id, score: Number(score.toFixed(5)) }));
            }

            const keyword  = ['p7', 'p2', 'p9'];   // full-text / BM25 order
            const semantic = ['p2', 'p4', 'p7'];   // vector search order
            console.log(reciprocalRankFusion([keyword, semantic], { k: 60, limit: 3 }));
        """,
        lang="javascript",
        output=r"""
            [
              { id: 'p2', score: 0.03252 },
              { id: 'p7', score: 0.03227 },
              { id: 'p4', score: 0.01613 }
            ]
        """,
        time="O(N log N) where N = total ids across lists", space="O(U) for U unique ids",
        follow=[
            ("How would you give the vector results more weight than the keyword results in RRF?", "RRF-এ keyword result-এর চেয়ে vector result-কে বেশি গুরুত্ব কীভাবে দেবে?"),
            ("When might a weighted sum of normalised scores beat RRF?", "কখন normalised score-এর weighted যোগফল RRF-কে ছাড়িয়ে যেতে পারে?"),
        ],
        related=["vec-005", "vec-023", "vec-030"],
        refs=[QDRANT_HYBRID, PGV, WIKI_BM25],
    ),
    # ------------------------------------------------------------------ vec-024
    Q(
        id="vec-024", sub="Embedding Model Changes", diff="hard", type="scenario",
        prio="high", market="both", mins=12,
        tags=["re-embedding", "migration", "versioning", "zero-downtime", "pgvector"],
        ver="pgvector 0.8.7 (PostgreSQL 18)", vs=True, status="stable",
        q_en=r"""You have 5 million chunks embedded with model A (1536 dimensions) in pgvector. A new model B (1024 dimensions) scores better on your Bangla queries. How do you migrate to model B with zero downtime and a safe rollback?""",
        q_bn=r"""pgvector-এ model A (1536 dimension) দিয়ে embed করা 50 লাখ chunk আছে। নতুন model B (1024 dimension) তোমার Bangla query-তে ভালো score করছে। Zero downtime আর নিরাপদ rollback সহ কীভাবে model B-তে migrate করবে?""",
        a_en=r"""
            **Golden rule:** vectors from different models are not comparable — a model-B query must only ever be compared with model-B documents. So this is a parallel build and a cutover, not an in-place update.

            1. **Prove it first:** evaluate model B offline on a golden set (recall@k, MRR) per language, and estimate cost/time for 5M chunks (tokens × price or GPU throughput).
            2. **Add, don't replace:** a new column `embedding_v2 vector(1024)` (or a new table), plus an `embedding_model` version field.
            3. **Dual-write:** from now on, new and updated chunks are embedded with **both** models, so the backfill doesn't chase a moving target.
            4. **Backfill in batches:** an idempotent, resumable job (checkpoint by id), respecting API rate limits; log failures for retry.
            5. **Build the index after the backfill:** `CREATE INDEX CONCURRENTLY ... USING hnsw (embedding_v2 vector_cosine_ops)` with enough `maintenance_work_mem`, so writes aren't blocked.
            6. **Shadow and compare:** run both pipelines for a sample of real traffic, compare overlap and quality metrics; re-tune similarity thresholds, because score distributions change between models.
            7. **Cut over behind a feature flag** (by percentage or tenant) — query embedding and document column switch together.
            8. **Rollback window:** keep model A's column and index for a while; once stable, stop dual-writing and drop them.
        """,
        a_bn=r"""
            **মূল নিয়ম:** আলাদা model-এর vector তুলনীয় নয় — model-B-এর query শুধু model-B-এর document-এর সাথেই তুলনা হবে। তাই এটা জায়গায় বসে update নয়, পাশাপাশি নতুন build আর তারপর cutover।

            1. **আগে প্রমাণ করো:** ভাষাভিত্তিক golden set-এ (recall@k, MRR) model B offline মূল্যায়ন করো, আর 50 লাখ chunk-এর খরচ/সময় হিসাব করো (token × দাম বা GPU throughput)।
            2. **Replace নয়, add করো:** নতুন column `embedding_v2 vector(1024)` (বা নতুন table), সাথে একটা `embedding_model` version field।
            3. **Dual-write:** এখন থেকে নতুন আর update হওয়া chunk **দুটো** model দিয়েই embed হবে, যাতে backfill একটা চলমান লক্ষ্যের পেছনে না ছোটে।
            4. **Batch-এ backfill:** idempotent, আবার শুরু করা যায় এমন job (id দিয়ে checkpoint), API rate limit মেনে; fail হওয়াগুলো retry-এর জন্য log করো।
            5. **Backfill-এর পরে index build:** যথেষ্ট `maintenance_work_mem` সহ `CREATE INDEX CONCURRENTLY ... USING hnsw (embedding_v2 vector_cosine_ops)`, যাতে write block না হয়।
            6. **Shadow চালিয়ে তুলনা:** আসল traffic-এর একটা sample-এ দুটো pipeline চালাও, overlap আর quality metric তুলনা করো; similarity threshold আবার tune করো, কারণ model বদলালে score distribution বদলায়।
            7. **Feature flag-এর পেছনে cutover** (percentage বা tenant অনুযায়ী) — query embedding আর document column একসাথে বদলাবে।
            8. **Rollback window:** model A-এর column আর index কিছুদিন রেখে দাও; স্থিতিশীল হলে dual-write বন্ধ করে সেগুলো drop করো।
        """,
        ex_en=r"""
            - **Cache keys must include the model version** — a cached query embedding from model A must never be used against model B's column.
            - **Storage during migration roughly doubles** (two vectors per row plus two indexes) — check disk and RAM headroom first, or migrate per partition/tenant.
            - **Dimension limits:** pgvector indexes `vector` up to 2,000 dimensions and `halfvec` up to 4,000, so a 3,072-dimension model would need half-precision indexing.
            - **Shorter vectors:** some models can output fewer dimensions (Matryoshka-style training / a `dimensions` option) — a cheaper alternative to a full model switch, but still a re-embedding.
            - **Communicate:** search results *will* change; tell support and product teams before the cutover.
        """,
        ex_bn=r"""
            - **Cache key-এ model version থাকতে হবে** — model A থেকে cache করা query embedding কখনো model B-এর column-এর বিপরীতে ব্যবহার করা যাবে না।
            - **Migration চলাকালীন storage প্রায় দ্বিগুণ হয়** (প্রতি row-এ দুইটা vector আর দুইটা index) — আগে disk আর RAM-এর জায়গা দেখে নাও, অথবা partition/tenant ধরে ধরে migrate করো।
            - **Dimension-এর সীমা:** pgvector `vector` index করে 2,000 dimension পর্যন্ত আর `halfvec` 4,000 পর্যন্ত, তাই 3,072-dimension-এর model-এ half-precision indexing লাগবে।
            - **ছোট vector:** কিছু model কম dimension output দিতে পারে (Matryoshka-ধরনের training / `dimensions` option) — পুরো model বদলের চেয়ে সস্তা বিকল্প, তবুও আবার embed করতে হয়।
            - **জানিয়ে দাও:** search result *বদলাবেই*; cutover-এর আগে support আর product team-কে জানাও।
        """,
        tip_en=r"""Lead with the invariant ("never compare across models"), then present the steps as a classic expand → migrate → contract plan. Interviewers recognise that pattern from database migrations.""",
        tip_bn=r"""শুরু করো অপরিবর্তনীয় নিয়মটা দিয়ে ("model পেরিয়ে কখনো তুলনা নয়"), তারপর ধাপগুলো classic expand → migrate → contract plan হিসেবে দেখাও। Database migration থেকে interviewer-রা এই pattern চেনে।""",
        mist_en=r"""Re-embedding in place (mixing models in one column during the backfill), switching query embeddings before documents are done, or forgetting to re-tune thresholds.""",
        mist_bn=r"""জায়গায় বসে আবার embed করা (backfill-এর সময় এক column-এ model মিশিয়ে ফেলা), document শেষ হওয়ার আগেই query embedding বদলে ফেলা, অথবা threshold আবার tune করতে ভুলে যাওয়া।""",
        code=r"""
            -- 1. Expand
            ALTER TABLE chunks ADD COLUMN embedding_v2 vector(1024);

            -- 2. Backfill in batches from a worker (idempotent, resumable)
            UPDATE chunks SET embedding_v2 = $2 WHERE id = $1 AND embedding_v2 IS NULL;

            -- 3. Build the new index without blocking writes
            SET maintenance_work_mem = '8GB';
            CREATE INDEX CONCURRENTLY chunks_embedding_v2_idx
              ON chunks USING hnsw (embedding_v2 vector_cosine_ops);

            -- 4. After cutover and a rollback window: contract
            DROP INDEX CONCURRENTLY chunks_embedding_idx;
            ALTER TABLE chunks DROP COLUMN embedding;
        """,
        lang="sql",
        follow=[
            ("How would you estimate the cost and duration of re-embedding 5 million chunks?", "50 লাখ chunk আবার embed করার খরচ আর সময় কীভাবে হিসাব করবে?"),
            ("What would you monitor during the gradual cutover?", "ধীরে ধীরে cutover চলাকালীন কী কী monitor করবে?"),
        ],
        related=["vec-002", "vec-011", "vec-028"],
        refs=[PGV, MATRYOSHKA],
    ),
    # ------------------------------------------------------------------ vec-025
    Q(
        id="vec-025", sub="Metadata Filtering", diff="hard", type="mcq",
        prio="high", market="both", mins=4,
        tags=["metadata-filtering", "pgvector", "hnsw", "iterative-scan", "post-filtering"],
        ver="pgvector 0.8.7 (iterative index scans since 0.8.0)", vs=True, status="version-specific",
        q_en=r"""A table holds 20,000 documents with an HNSW index on `embedding`. Tenant 7 owns about 4% of them. This query should return 10 rows, but it returns only 5. What is the most likely cause and fix?""",
        q_bn=r"""একটা table-এ 20,000 document, `embedding`-এ HNSW index আছে। Tenant 7-এর আছে প্রায় 4%। এই query-র 10টা row return করার কথা, কিন্তু দিচ্ছে মাত্র 5টা। সবচেয়ে সম্ভাব্য কারণ আর সমাধান কী?""",
        options=[
            ("The filter is applied after the index scan: HNSW returns about `hnsw.ef_search` (default 40) candidates and only a few belong to tenant 7. Enable iterative index scans (`SET hnsw.iterative_scan = relaxed_order`), raise `ef_search`, or use a partial index/partitioning per tenant", "Filter প্রয়োগ হয় index scan-এর পরে: HNSW প্রায় `hnsw.ef_search` (default 40)-টা candidate দেয়, যার অল্প কয়েকটা tenant 7-এর। Iterative index scan চালু করো (`SET hnsw.iterative_scan = relaxed_order`), `ef_search` বাড়াও, অথবা tenant-ভিত্তিক partial index/partitioning ব্যবহার করো"),
            ("The HNSW index is corrupted; run `REINDEX`", "HNSW index corrupt হয়ে গেছে; `REINDEX` চালাও"),
            ("`LIMIT` is ignored when an HNSW index is used; add `OFFSET 0`", "HNSW index ব্যবহার হলে `LIMIT` উপেক্ষা করা হয়; `OFFSET 0` যোগ করো"),
            ("Cosine distance can't be combined with `WHERE`; filter in application code instead", "Cosine distance `WHERE`-এর সাথে মেলানো যায় না; বদলে application code-এ filter করো"),
        ],
        correct=0,
        a_en=r"""With approximate indexes, pgvector applies the `WHERE` filter **after** the index scan. HNSW hands back roughly `ef_search` nearest candidates, most belonging to other tenants, so only a handful survive the filter. Iterative index scans (pgvector 0.8+) keep scanning until enough rows pass the filter.""",
        a_bn=r"""Approximate index-এ pgvector `WHERE` filter প্রয়োগ করে index scan-এর **পরে**। HNSW মোটামুটি `ef_search`-সংখ্যক কাছের candidate ফেরত দেয়, যার বেশিরভাগ অন্য tenant-এর, তাই filter পেরিয়ে টেকে মাত্র কয়েকটা। Iterative index scan (pgvector 0.8+) যথেষ্ট row filter পার না হওয়া পর্যন্ত scan চালিয়ে যায়।""",
        ex_en=r"""
            This is the classic **post-filtering** pitfall of filtered ANN search. The pgvector docs give the same arithmetic: with the default `ef_search` of 40 and a filter matching 10% of rows, you get about 4 matches on average.

            Fixes, from simplest:
            - `SET hnsw.iterative_scan = relaxed_order;` (or `strict_order`) — pgvector 0.8.0+ automatically scans more of the index, bounded by `hnsw.max_scan_tuples` (default 20,000). With `relaxed_order`, results can be slightly out of order; re-sort in an outer query if exact order matters.
            - Raise `hnsw.ef_search` — helps, but costs latency for every query.
            - **Partial indexes** per large tenant/category, or **partitioning** by tenant, so the filter is "built in".
            - For very selective filters, an exact scan over a B-tree-filtered subset may be faster and gives perfect recall.

            Option D is the tempting wrong answer: filtering in app code after `LIMIT` makes the problem worse, and can leak data if you forget it.
        """,
        ex_bn=r"""
            এটা filtered ANN search-এর classic **post-filtering** ফাঁদ। pgvector docs-এ একই হিসাব দেওয়া আছে: default `ef_search` 40 আর 10% row match করা filter থাকলে গড়ে প্রায় 4টা match পাওয়া যায়।

            সমাধান, সহজ থেকে শুরু:
            - `SET hnsw.iterative_scan = relaxed_order;` (বা `strict_order`) — pgvector 0.8.0+ নিজে থেকেই index-এর আরও বেশি অংশ scan করে, `hnsw.max_scan_tuples` (default 20,000) পর্যন্ত। `relaxed_order`-এ result-এর ক্রম সামান্য এলোমেলো হতে পারে; সঠিক ক্রম জরুরি হলে বাইরের query-তে আবার sort করো।
            - `hnsw.ef_search` বাড়াও — সাহায্য করে, কিন্তু প্রতিটা query-র latency বাড়ায়।
            - বড় tenant/category-র জন্য **partial index**, বা tenant অনুযায়ী **partitioning**, যাতে filter "ভেতরেই" থাকে।
            - খুব selective filter-এ B-tree দিয়ে filter করা subset-এ exact scan বেশি দ্রুত হতে পারে আর perfect recall দেয়।

            Option D হলো লোভনীয় ভুল উত্তর: `LIMIT`-এর পরে app code-এ filter করলে সমস্যা আরও বাড়ে, আর ভুলে গেলে data ফাঁসও হতে পারে।
        """,
        tip_en=r"""Name the concept — "post-filtering in approximate search" — before the fix. Then mention that other vector databases solve it with filter-aware indexes, which shows breadth beyond one tool.""",
        tip_bn=r"""সমাধানের আগে ধারণাটার নাম বলো — "approximate search-এ post-filtering"। তারপর উল্লেখ করো যে অন্য vector database filter-aware index দিয়ে এটা সমাধান করে — এতে এক tool-এর বাইরেও তোমার জ্ঞানের পরিধি দেখা যায়।""",
        code=r"""
            SELECT id
            FROM docs
            WHERE tenant_id = 7
            ORDER BY embedding <=> $1
            LIMIT 10;
        """,
        lang="sql",
        refs=[PGV],
        related=["vec-013", "vec-026", "vec-010"],
    ),
]

if __name__ == "__main__":
    save("vectordb", "b2", QUESTIONS)
