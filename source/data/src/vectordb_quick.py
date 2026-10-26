# Vector Databases — quick-recall questions (vec-q01..vec-q10)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PGVECTOR = ("pgvector — README (GitHub)", "https://github.com/pgvector/pgvector")
QD_VECTORS = ("Qdrant docs — Vectors", "https://qdrant.tech/documentation/concepts/vectors/")
QD_SEARCH = ("Qdrant docs — Search", "https://qdrant.tech/documentation/concepts/search/")
QD_INDEXING = ("Qdrant docs — Indexing", "https://qdrant.tech/documentation/concepts/indexing/")
QD_HYBRID = ("Qdrant docs — Hybrid and multi-stage queries", "https://qdrant.tech/documentation/concepts/hybrid-queries/")
R_VECTORS = ("Redis docs — Vector search concepts", "https://redis.io/docs/latest/develop/ai/search-and-query/vectors/")
PG_FTS = ("PostgreSQL docs — Full Text Search: Introduction", "https://www.postgresql.org/docs/current/textsearch-intro.html")
RAG_PAPER = ("Lewis et al. — Retrieval-Augmented Generation (arXiv)", "https://arxiv.org/abs/2005.11401")

VER = "Version-independent concept"

QUESTIONS = [
    # ------------------------------------------------------------------ vec-q01
    Q(
        id="vec-q01", sub="Vectors & Dimensions", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["vector", "dimensions", "basics"],
        ver=VER, vs=False, status="stable",
        q_en=r"""In a vector database, what is a vector, and what is its "dimension"?""",
        q_bn=r"""Vector database-এ vector কী, আর তার "dimension" মানে কী?""",
        a_en=r"""A vector is just an ordered list of numbers, like `[0.12, -0.48, 0.91]`. Its dimension is how many numbers it has, so that one has 3. Real embedding models produce a fixed size such as 384, 768 or 1536, and every vector in one column or collection must have the same dimension.""",
        a_bn=r"""Vector হলো সংখ্যার একটা ordered list, যেমন `[0.12, -0.48, 0.91]`। এতে কয়টা সংখ্যা আছে সেটাই dimension, তাই এটার dimension 3। আসল embedding model নির্দিষ্ট size-এর vector দেয়, যেমন 384, 768 বা 1536, আর একটা column বা collection-এর সব vector-এর dimension একই হতে হয়।""",
        code=r"""
            const v = [0.12, -0.48, 0.91];
            console.log(v.length); // 3 → the dimension
        """, lang="javascript",
        ex_en=r"""You can't compare vectors of different dimensions. Switching to a model with a different size means re-embedding everything; pgvector rejects an insert with the wrong size.""",
        ex_bn=r"""আলাদা dimension-এর vector তুলনা করা যায় না। ভিন্ন size-এর model-এ গেলে সবকিছু আবার embed করতে হয়; ভুল size-এর insert pgvector reject করে।""",
        tip_en=r"""Keep it simple: "a list of numbers; dimension = its length", then give a real model size.""",
        tip_bn=r"""সহজ রাখো: "সংখ্যার list; dimension = তার length", তারপর একটা আসল model-এর size বলো।""",
        follow=[("What happens if you insert a 1536-dim vector into a `vector(768)` column?", "`vector(768)` column-এ 1536-dim vector insert করলে কী হয়?")],
        related=["vec-002", "vec-011"],
        refs=[QD_VECTORS],
    ),
    # ------------------------------------------------------------------ vec-q02
    Q(
        id="vec-q02", sub="Embeddings", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["embeddings", "embedding-model", "same-model"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What does an embedding model do, and why must documents and queries use the same model?""",
        q_bn=r"""Embedding model কী করে, আর document ও query কেন একই model দিয়ে embed করতে হয়?""",
        a_en=r"""An embedding model turns text (or an image) into a vector so that similar meanings get nearby vectors. Each model builds its own "map" of meaning, so vectors from two different models aren't comparable: a query embedded with model B against documents from model A gives meaningless results.""",
        a_bn=r"""Embedding model text (বা image)-কে vector-এ পরিণত করে, যাতে একই রকম অর্থের vector কাছাকাছি থাকে। প্রতিটা model অর্থের নিজস্ব একটা "map" বানায়, তাই দুই model-এর vector তুলনা করা যায় না: model A-এর document-এর সাথে model B দিয়ে embed করা query মেলালে result অর্থহীন হয়।""",
        ex_en=r"""The trap: two models can have the same dimension, so nothing errors, yet results are random. Store the model name with each vector to catch this.""",
        ex_bn=r"""ফাঁদটা হলো: দুই model-এর dimension একই হতে পারে, তাই কোনো error হয় না, অথচ result এলোমেলো। এটা ধরতে প্রতিটা vector-এর সাথে model-এর নাম রাখো।""",
        tip_en=r"""Say "same model, same space", and mention that changing models means re-embedding.""",
        tip_bn=r"""বলো "same model, same space", আর উল্লেখ করো যে model বদলালে আবার embed করতে হয়।""",
        follow=[("How would you switch embedding models without downtime?", "Downtime ছাড়া embedding model কীভাবে বদলাবে?")],
        related=["vec-001", "vec-018", "vec-024"],
        refs=[QD_VECTORS],
    ),
    # ------------------------------------------------------------------ vec-q03
    Q(
        id="vec-q03", sub="Similarity Search", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["vector-database", "similarity-search", "basics"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is a vector database?""",
        q_bn=r"""Vector database কী?""",
        a_en=r"""A vector database stores vectors (usually embeddings) along with an id and metadata, and is built to answer one question fast: "which stored vectors are closest to this query vector?" It uses special indexes for this nearest-neighbour search and lets you combine it with metadata filters.""",
        a_bn=r"""Vector database vector (সাধারণত embedding) id আর metadata-সহ রাখে, আর একটা প্রশ্নের উত্তর দ্রুত দেওয়ার জন্য বানানো: "এই query vector-এর সবচেয়ে কাছের stored vector কোনগুলো?" এই nearest-neighbour search-এর জন্য বিশেষ index ব্যবহার করে, আর metadata filter-এর সাথেও মেলানো যায়।""",
        ex_en=r"""It can be a dedicated product (Qdrant, Weaviate, Milvus, Pinecone) or an extension of a database you already run, like pgvector for PostgreSQL or vector search in Redis.""",
        ex_bn=r"""এটা আলাদা product হতে পারে (Qdrant, Weaviate, Milvus, Pinecone), অথবা আগে থেকে চালানো database-এর extension, যেমন PostgreSQL-এর pgvector বা Redis-এর vector search।""",
        tip_en=r"""Define it by the query it answers ("nearest vectors"), not by a product name.""",
        tip_bn=r"""Product-এর নাম দিয়ে না, এটা কোন query-র উত্তর দেয় ("সবচেয়ে কাছের vector") সেটা দিয়ে define করো।""",
        follow=[("Do you always need a dedicated vector database?", "সবসময় কি আলাদা vector database লাগে?")],
        related=["vec-003", "vec-021"],
        refs=[R_VECTORS],
    ),
    # ------------------------------------------------------------------ vec-q04
    Q(
        id="vec-q04", sub="Cosine Similarity", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["cosine-similarity", "similarity", "basics"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What do cosine similarity values of 1, 0 and −1 mean?""",
        q_bn=r"""Cosine similarity-র মান 1, 0 আর −1 মানে কী?""",
        a_en=r"""Cosine similarity compares the direction of two vectors, not their length. 1 means they point the same way (very similar), 0 means they're at a right angle (unrelated), and −1 means they point in opposite directions.""",
        a_bn=r"""Cosine similarity দুটো vector-এর দিক তুলনা করে, length না। 1 মানে একই দিকে (খুব মিল), 0 মানে সমকোণে (সম্পর্কহীন), আর −1 মানে উল্টো দিকে।""",
        code=r"""
            const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
            const cos = (a, b) => dot(a, b) / Math.sqrt(dot(a, a) * dot(b, b));
            console.log(cos([3, 4], [6, 8]).toFixed(2));   // same direction
            console.log(cos([3, 4], [-4, 3]).toFixed(2));  // right angle
            console.log(cos([3, 4], [-3, -4]).toFixed(2)); // opposite
        """, lang="javascript",
        output=r"""
            1.00
            0.00
            -1.00
        """,
        ex_en=r"""Databases often sort by cosine **distance** = 1 − similarity, so smaller means closer. With text embeddings, scores are usually positive, so don't expect to see −1 in practice.""",
        ex_bn=r"""Database প্রায়ই cosine **distance** = 1 − similarity দিয়ে sort করে, তাই ছোট মানে বেশি কাছে। Text embedding-এ score সাধারণত positive থাকে, তাই বাস্তবে −1 দেখার আশা কোরো না।""",
        tip_en=r"""Say "angle, not length", then mention similarity vs distance so the sort order doesn't trip you up.""",
        tip_bn=r"""বলো "angle, length না", তারপর similarity বনাম distance বলো, যাতে sort order নিয়ে গুলিয়ে না যায়।""",
        follow=[("In pgvector, which operator gives cosine distance?", "pgvector-এ কোন operator cosine distance দেয়?")],
        related=["vec-004", "vec-012"],
        refs=[PGVECTOR],
    ),
    # ------------------------------------------------------------------ vec-q05
    Q(
        id="vec-q05", sub="Approximate Nearest Neighbour (ANN) Search", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["ann", "knn", "hnsw", "recall"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is ANN search, and what does "approximate" give up?""",
        q_bn=r"""ANN search কী, আর "approximate" হওয়ায় কী ছাড় দিতে হয়?""",
        a_en=r"""ANN (approximate nearest neighbour) search finds vectors that are almost certainly among the closest, using an index like HNSW instead of comparing the query with every vector. It's far faster at millions of vectors, but it may occasionally miss a true nearest neighbour, so recall is slightly below 100%.""",
        a_bn=r"""ANN (approximate nearest neighbour) search প্রতিটা vector-এর সাথে query তুলনা না করে HNSW-এর মতো index দিয়ে এমন vector খোঁজে যেগুলো প্রায় নিশ্চিতভাবে সবচেয়ে কাছেরগুলোর মধ্যে আছে। লাখ লাখ vector-এ এটা অনেক দ্রুত, কিন্তু মাঝে মাঝে আসল কোনো nearest neighbour বাদ পড়তে পারে, তাই recall 100%-এর একটু নিচে থাকে।""",
        ex_en=r"""Exact k-NN (compare everything) is fine for small sets. Index settings like HNSW `ef_search` trade speed for recall.""",
        ex_bn=r"""ছোট set-এ exact k-NN (সবকিছুর সাথে তুলনা) ঠিক আছে। HNSW-এর `ef_search`-এর মতো index setting speed আর recall-এর মধ্যে trade-off করে।""",
        tip_en=r"""Say the trade-off in one phrase: "much faster, slightly lower recall".""",
        tip_bn=r"""Trade-off-টা এক কথায় বলো: "অনেক দ্রুত, recall সামান্য কম"।""",
        follow=[("When is exact search good enough?", "কখন exact search-ই যথেষ্ট?")],
        related=["vec-006", "vec-014"],
        refs=[QD_INDEXING],
    ),
    # ------------------------------------------------------------------ vec-q06
    Q(
        id="vec-q06", sub="Vector DBs vs Full-Text Search", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["semantic-search", "keyword-search", "bm25"],
        ver=VER, vs=False, status="stable",
        q_en=r"""Give one search where keyword search beats semantic search, and one where semantic search wins.""",
        q_bn=r"""এমন একটা search বলো যেখানে keyword search semantic search-কে হারায়, আর একটা যেখানে semantic search জেতে।""",
        a_en=r"""Keyword search wins on exact strings: a model number like "Redmi Note 13" or an error code, because it matches the exact words. Semantic search wins when the words differ but the meaning is the same: "phone case" should find "mobile cover", which shares no words with it.""",
        a_bn=r"""Exact string-এ keyword search জেতে: "Redmi Note 13"-এর মতো model number বা error code, কারণ এটা হুবহু শব্দ মেলায়। শব্দ আলাদা কিন্তু অর্থ একই হলে semantic search জেতে: "phone case" দিয়ে "mobile cover" পাওয়া উচিত, যদিও দুটোতে কোনো শব্দ মিল নেই।""",
        ex_en=r"""That's why production search often combines both (hybrid search).""",
        ex_bn=r"""এজন্যই production search-এ প্রায়ই দুটো মিলিয়ে ব্যবহার হয় (hybrid search)।""",
        tip_en=r"""Concrete examples beat definitions here; give one of each.""",
        tip_bn=r"""এখানে definition-এর চেয়ে বাস্তব example বেশি কাজে দেয়; প্রতিটার একটা করে বলো।""",
        follow=[("What is hybrid search?", "Hybrid search কী?")],
        related=["vec-005"],
        refs=[PG_FTS],
    ),
    # ------------------------------------------------------------------ vec-q07
    Q(
        id="vec-q07", sub="Chunking", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["chunking", "overlap", "rag"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is a chunk, and why add overlap between chunks?""",
        q_bn=r"""Chunk কী, আর chunk-গুলোর মধ্যে overlap কেন রাখা হয়?""",
        a_en=r"""A chunk is a small piece of a document (often a few hundred tokens) that gets its own embedding, so a search can find the exact section that answers a question. Overlap repeats a little text between neighbouring chunks, so an idea split at a boundary still appears whole in at least one chunk.""",
        a_bn=r"""Chunk হলো document-এর একটা ছোট অংশ (প্রায়ই কয়েকশো token), যার নিজের embedding থাকে, যাতে search প্রশ্নের উত্তর থাকা ঠিক অংশটা খুঁজে পায়। Overlap পাশাপাশি chunk-এর মধ্যে একটু text পুনরাবৃত্তি করে, যাতে boundary-তে কাটা পড়া কোনো idea অন্তত একটা chunk-এ পুরোটা থাকে।""",
        ex_en=r"""Too big and the embedding becomes a blurry average; too small and chunks lose context. Splitting on headings and paragraphs usually beats fixed character counts.""",
        ex_bn=r"""খুব বড় হলে embedding ঝাপসা গড় হয়ে যায়; খুব ছোট হলে chunk context হারায়। নির্দিষ্ট character গুনে কাটার চেয়ে heading আর paragraph ধরে ভাগ করা সাধারণত ভালো।""",
        tip_en=r"""Mention a typical overlap (10–20%) and that you'd measure retrieval quality before and after changing chunk size.""",
        tip_bn=r"""একটা সাধারণ overlap (10–20%) বলো, আর বলো chunk size বদলানোর আগে-পরে retrieval quality মেপে দেখবে।""",
        follow=[("How would you chunk Bangla documents?", "Bangla document কীভাবে chunk করবে?")],
        related=["vec-007", "vec-015"],
        refs=[QD_SEARCH],
    ),
    # ------------------------------------------------------------------ vec-q08
    Q(
        id="vec-q08", sub="RAG Architecture", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["rag", "llm", "retrieval"],
        ver=VER, vs=False, status="stable",
        q_en=r"""Explain RAG in one breath.""",
        q_bn=r"""এক নিঃশ্বাসে RAG ব্যাখ্যা করো।""",
        a_en=r"""RAG (Retrieval-Augmented Generation) means: embed the user's question, retrieve the most relevant chunks from your own data, put them into the LLM's prompt, and let the LLM answer from that context, ideally with citations. It lets the LLM use private or fresh data it was never trained on.""",
        a_bn=r"""RAG (Retrieval-Augmented Generation) মানে: user-এর প্রশ্ন embed করো, নিজের data থেকে সবচেয়ে relevant chunk retrieve করো, সেগুলো LLM-এর prompt-এ দাও, আর LLM সেই context থেকে উত্তর দিক, পারলে citation-সহ। এতে LLM এমন private বা নতুন data ব্যবহার করতে পারে, যেটা দিয়ে সে কখনো train হয়নি।""",
        ex_en=r"""If retrieval brings back the wrong chunks, the LLM answers confidently from the wrong context, so retrieval quality decides answer quality.""",
        ex_bn=r"""Retrieval ভুল chunk আনলে LLM ভুল context থেকেই আত্মবিশ্বাসের সাথে উত্তর দেয়, তাই retrieval quality-ই answer quality ঠিক করে।""",
        tip_en=r"""Say the four verbs in order: embed, retrieve, augment the prompt, generate.""",
        tip_bn=r"""চারটা verb ক্রম অনুযায়ী বলো: embed, retrieve, prompt augment, generate।""",
        follow=[("Why use RAG instead of fine-tuning for company documents?", "Company document-এর জন্য fine-tuning-এর বদলে RAG কেন?")],
        related=["vec-008", "vec-023"],
        refs=[RAG_PAPER],
    ),
    # ------------------------------------------------------------------ vec-q09
    Q(
        id="vec-q09", sub="Vector DBs vs Relational DBs (pgvector)", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["pgvector", "postgresql", "sql"],
        ver="pgvector 0.8.7 (PostgreSQL 18)", vs=True, status="stable",
        q_en=r"""What is pgvector, and what does a basic similarity query look like?""",
        q_bn=r"""pgvector কী, আর একটা সাধারণ similarity query দেখতে কেমন?""",
        a_en=r"""pgvector is a PostgreSQL extension that adds a `vector` column type, distance operators (`<->` L2, `<=>` cosine, `<#>` negative inner product) and ANN indexes (HNSW, IVFFlat). You find the nearest rows with `ORDER BY embedding <operator> query LIMIT k`, right next to your normal tables.""",
        a_bn=r"""pgvector হলো একটা PostgreSQL extension, যেটা `vector` column type, distance operator (`<->` L2, `<=>` cosine, `<#>` negative inner product) আর ANN index (HNSW, IVFFlat) যোগ করে। সবচেয়ে কাছের row পেতে লেখো `ORDER BY embedding <operator> query LIMIT k`, তোমার সাধারণ table-এর পাশেই।""",
        code=r"""
            CREATE EXTENSION IF NOT EXISTS vector;
            CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
            INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
            SELECT id FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 1;  -- id 1 (L2 distance 2.449 vs 5.745)
        """, lang="sql",
        ex_en=r"""Order by the distance operator ascending; ordering by a computed similarity `DESC` can't use the index. The index's operator class must match the operator (`vector_cosine_ops` for `<=>`).""",
        ex_bn=r"""Distance operator দিয়ে ascending order দাও; হিসাব করা similarity দিয়ে `DESC` দিলে index ব্যবহার হয় না। Index-এর operator class operator-এর সাথে মিলতে হবে (`<=>`-এর জন্য `vector_cosine_ops`)।""",
        tip_en=r"""If the team already uses PostgreSQL, say pgvector is the sensible first step before adding a separate vector database.""",
        tip_bn=r"""Team আগে থেকেই PostgreSQL ব্যবহার করলে বলো, আলাদা vector database যোগ করার আগে pgvector-ই যুক্তিসঙ্গত প্রথম ধাপ।""",
        follow=[("Why might an HNSW query with a `WHERE` filter return fewer rows than `LIMIT`?", "`WHERE` filter-সহ HNSW query কেন `LIMIT`-এর চেয়ে কম row দিতে পারে?")],
        related=["vec-009", "vec-013", "vec-021"],
        refs=[PGVECTOR],
    ),
    # ------------------------------------------------------------------ vec-q10
    Q(
        id="vec-q10", sub="Hybrid Search", diff="medium", type="quick",
        prio="medium", market="both", mins=1,
        tags=["hybrid-search", "bm25", "rrf"],
        ver=VER, vs=False, status="stable",
        q_en=r"""What is hybrid search?""",
        q_bn=r"""Hybrid search কী?""",
        a_en=r"""Hybrid search runs a keyword search (like BM25) and a vector search for the same query, then merges the two result lists, often with Reciprocal Rank Fusion, which combines ranks instead of raw scores. You get exact-word matches and meaning-based matches in one ranking.""",
        a_bn=r"""Hybrid search একই query-র জন্য keyword search (যেমন BM25) আর vector search দুটোই চালায়, তারপর দুই result list মিলিয়ে দেয়, প্রায়ই Reciprocal Rank Fusion দিয়ে, যেটা raw score-এর বদলে rank মেলায়। এতে হুবহু শব্দের match আর অর্থভিত্তিক match একটা ranking-এ পাওয়া যায়।""",
        ex_en=r"""Ranks are used because BM25 scores and cosine similarities are on completely different scales, so adding them directly makes no sense.""",
        ex_bn=r"""Rank ব্যবহার করা হয় কারণ BM25 score আর cosine similarity সম্পূর্ণ আলাদা scale-এ থাকে, তাই সরাসরি যোগ করার মানে হয় না।""",
        tip_en=r"""Name RRF and give the one-line reason it uses ranks.""",
        tip_bn=r"""RRF-এর নাম বলো, আর কেন rank ব্যবহার করে সেটা এক line-এ বলো।""",
        follow=[("How does Reciprocal Rank Fusion score a document?", "Reciprocal Rank Fusion একটা document-কে কীভাবে score দেয়?")],
        related=["vec-016", "vec-005"],
        refs=[QD_HYBRID],
    ),
]

save("vectordb", "quick", QUESTIONS)
