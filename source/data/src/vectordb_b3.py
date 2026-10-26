# Vector Databases — batch 3 (vec-008, 009, 017, 018, 019, 026, 027, 031)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

PGV = ("pgvector — README (GitHub)", "https://github.com/pgvector/pgvector")
RAG_PAPER = ("Lewis et al. — Retrieval-Augmented Generation (arXiv)", "https://arxiv.org/abs/2005.11401")
PINECONE_VDB = ("Pinecone — What is a vector database?", "https://www.pinecone.io/learn/vector-database/")
WIKI_IREVAL = ("Wikipedia — Evaluation measures (information retrieval)", "https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)")
WIKI_MRR = ("Wikipedia — Mean reciprocal rank", "https://en.wikipedia.org/wiki/Mean_reciprocal_rank")
OWASP_LLM08 = ("OWASP GenAI — LLM08:2025 Vector and Embedding Weaknesses", "https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/")
PG_RLS = ("PostgreSQL docs — Row Security Policies", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html")
E5 = ("Hugging Face — multilingual-e5-base model card", "https://huggingface.co/intfloat/multilingual-e5-base")
MATRYOSHKA = ("Kusupati et al. — Matryoshka Representation Learning (arXiv)", "https://arxiv.org/abs/2205.13147")

QUESTIONS = [
    # ------------------------------------------------------------------ vec-008
    Q(
        id="vec-008", sub="RAG Architecture", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["rag", "llm", "retrieval", "citations"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""What is Retrieval-Augmented Generation (RAG)? Describe the basic flow, and explain why teams use it instead of only prompting an LLM or fine-tuning it.""",
        q_bn=r"""Retrieval-Augmented Generation (RAG) কী? মূল flow-টা বর্ণনা করো, আর team-গুলো কেন শুধু LLM-কে prompt করা বা fine-tune করার বদলে এটা ব্যবহার করে, ব্যাখ্যা করো।""",
        a_en=r"""
            RAG means: **retrieve relevant information first, then let the LLM generate an answer using it.**

            **Indexing (offline):** collect documents → split into chunks → embed each chunk → store vectors plus metadata in a vector store.

            **Answering (online):**
            1. Embed the user's question.
            2. Retrieve the most similar chunks (often with keyword search too, and a reranker).
            3. Put those chunks into the prompt as context, with instructions like "answer only from these sources and cite them".
            4. The LLM writes the answer, ideally with citations back to the source documents.

            **Why not just prompt the LLM?** It doesn't know your private or recent data, and it may confidently make things up. **Why not fine-tune?** Fine-tuning is good for style, format or behaviour, but it's a poor way to store facts that change — every policy update would need retraining, and you can't easily cite or permission-check what the model "remembers". RAG keeps knowledge in a database you can update, filter by user permissions and cite.
        """,
        a_bn=r"""
            RAG মানে: **আগে প্রাসঙ্গিক তথ্য retrieve করো, তারপর সেটা ব্যবহার করে LLM-কে উত্তর generate করতে দাও।**

            **Indexing (offline):** document জোগাড় করো → chunk-এ ভাগ করো → প্রতিটা chunk embed করো → vector আর metadata একটা vector store-এ রাখো।

            **উত্তর দেওয়া (online):**
            1. User-এর প্রশ্ন embed করো।
            2. সবচেয়ে কাছাকাছি chunk-গুলো retrieve করো (প্রায়ই keyword search আর reranker সহ)।
            3. সেই chunk-গুলো context হিসেবে prompt-এ দাও, সাথে নির্দেশনা — "শুধু এই source থেকে উত্তর দাও আর cite করো"।
            4. LLM উত্তর লেখে, আদর্শভাবে source document-এর citation সহ।

            **শুধু LLM-কে prompt করা নয় কেন?** এটা তোমার private বা সাম্প্রতিক data জানে না, আর আত্মবিশ্বাসের সাথে বানিয়ে বলতে পারে। **Fine-tune নয় কেন?** Fine-tuning style, format বা আচরণ শেখাতে ভালো, কিন্তু বদলাতে থাকা তথ্য রাখার জন্য দুর্বল উপায় — প্রতিটা policy update-এ আবার train করতে হবে, আর model যা "মনে রাখে" তা সহজে cite বা permission-check করা যায় না। RAG জ্ঞানকে এমন database-এ রাখে যেটা update করা যায়, user permission দিয়ে filter করা যায় আর cite করা যায়।
        """,
        quick_en=r"""RAG retrieves the most relevant chunks from your own data and puts them into the LLM's prompt, so it answers from them, ideally with citations. It beats plain prompting because the LLM doesn't know your private or recent data, and beats fine-tuning for facts because you can update, permission-filter and cite the data.""",
        quick_bn=r"""RAG তোমার নিজের data থেকে সবচেয়ে relevant chunk খুঁজে LLM-এর prompt-এ দেয়, যাতে LLM সেগুলো থেকে উত্তর দেয়, পারলে citation-সহ। শুধু prompt করার চেয়ে ভালো, কারণ LLM তোমার private বা সাম্প্রতিক data জানে না; আর fact রাখার জন্য fine-tuning-এর চেয়ে ভালো, কারণ data update, permission filter আর cite করা যায়।""",
        ex_en=r"""
            - **RAG reduces hallucination but doesn't eliminate it:** if retrieval returns the wrong chunks, the LLM answers confidently from the wrong context. Retrieval quality is usually the bottleneck.
            - **Context window ≠ solution:** stuffing everything into a huge context is slow, expensive and often less accurate than good retrieval.
            - **Security:** filter by the user's permissions during retrieval; retrieved text can also contain prompt-injection attempts, so treat it as untrusted data.
            - **The term** comes from a 2020 research paper (Lewis et al.); today it describes a broad family of retrieve-then-generate architectures.
        """,
        ex_bn=r"""
            - **RAG hallucination কমায়, পুরোপুরি দূর করে না:** retrieval ভুল chunk দিলে LLM ভুল context থেকেই আত্মবিশ্বাসের সাথে উত্তর দেয়। সাধারণত retrieval quality-ই আসল bottleneck।
            - **Context window মানেই সমাধান নয়:** সবকিছু বিশাল context-এ ঠেসে দেওয়া ধীর, ব্যয়বহুল, আর প্রায়ই ভালো retrieval-এর চেয়ে কম নির্ভুল।
            - **Security:** retrieval-এর সময়ই user-এর permission দিয়ে filter করো; retrieve হওয়া text-এ prompt-injection-এর চেষ্টাও থাকতে পারে, তাই এটাকে untrusted data হিসেবে দেখো।
            - **নামটা** এসেছে 2020 সালের একটা research paper থেকে (Lewis et al.); আজ এটা retrieve-then-generate ধরনের নানা architecture-এর সাধারণ নাম।
        """,
        tip_en=r"""Describe RAG as two pipelines (indexing and answering), then answer "why not fine-tuning?" with "facts change; RAG keeps knowledge updatable, citable and permission-aware". That's the line interviewers want.""",
        tip_bn=r"""RAG-কে দুইটা pipeline (indexing আর answering) হিসেবে বর্ণনা করো, তারপর "fine-tuning নয় কেন?"-এর উত্তর দাও "তথ্য বদলায়; RAG জ্ঞানকে update করা যায়, cite করা যায় আর permission-aware রাখে" বলে। Interviewer এই কথাটাই চায়।""",
        mist_en=r"""Saying RAG "trains the model on your documents", or that it guarantees correct answers.""",
        mist_bn=r"""বলা যে RAG "তোমার document দিয়ে model-কে train করে", অথবা এটা সঠিক উত্তরের নিশ্চয়তা দেয়।""",
        code=r"""
            // Minimal RAG answer flow (illustrative)
            async function answer(question, user) {
              const queryVector = await embed(question);
              const chunks = await searchChunks(queryVector, { groups: user.groups, limit: 5 });

              const context = chunks
                .map((c, i) => `[${i + 1}] ${c.title}\n${c.content}`)
                .join('\n\n');

              const prompt = `Answer using ONLY the sources below and cite them like [1].
            If the answer is not in the sources, say you don't know.

            ${context}

            Question: ${question}`;

              return llm.generate(prompt);
            }
        """,
        lang="javascript",
        follow=[
            ("What would you do if the right document exists but isn't retrieved?", "সঠিক document আছে কিন্তু retrieve হচ্ছে না — এমন হলে কী করবে?"),
            ("When would fine-tuning still make sense alongside RAG?", "RAG-এর পাশাপাশি কখন fine-tuning-ও যুক্তিসঙ্গত?"),
        ],
        related=["vec-023", "vec-020", "vec-007"],
        refs=[RAG_PAPER, PINECONE_VDB],
    ),
    # ------------------------------------------------------------------ vec-009
    Q(
        id="vec-009", sub="Vector DBs vs Relational DBs (pgvector)", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["pgvector", "postgresql", "architecture", "vector-database"],
        ver="pgvector 0.8.7 (PostgreSQL 18)", vs=False, status="stable",
        q_en=r"""Your Node.js app already uses PostgreSQL. You need semantic search over about 200,000 product descriptions. What is the most sensible first choice?""",
        q_bn=r"""তোমার Node.js app আগে থেকেই PostgreSQL ব্যবহার করে। প্রায় 200,000 product description-এর ওপর semantic search লাগবে। সবচেয়ে যুক্তিসঙ্গত প্রথম পছন্দ কী?""",
        options=[
            ("Store embeddings as JSON arrays and compute cosine similarity in Node.js for every query", "Embedding JSON array হিসেবে রেখে প্রতিটা query-তে Node.js-এ cosine similarity হিসাব করা"),
            ("Deploy a dedicated vector database, because relational databases cannot store vectors", "একটা dedicated vector database deploy করা, কারণ relational database vector রাখতে পারে না"),
            ("Create a full-text index on the descriptions — that is semantic search", "Description-এ একটা full-text index তৈরি করা — ওটাই semantic search"),
            ("Enable the pgvector extension, add a `vector` column with an HNSW index, and query it with SQL", "pgvector extension চালু করে একটা `vector` column আর HNSW index যোগ করা, তারপর SQL দিয়ে query করা"),
        ],
        correct=3,
        a_en=r"""Use pgvector. It adds a `vector` type, distance operators and ANN indexes to PostgreSQL, so embeddings live next to your products — with joins, filters, transactions and your existing backups. 200,000 vectors is well within its comfort zone.""",
        a_bn=r"""pgvector ব্যবহার করো। এটা PostgreSQL-এ একটা `vector` type, distance operator আর ANN index যোগ করে, ফলে embedding তোমার product-এর পাশেই থাকে — join, filter, transaction আর বিদ্যমান backup সহ। 200,000 vector এর জন্য একেবারেই স্বচ্ছন্দ পরিসর।""",
        quick_en=r"""Enable pgvector, add a `vector` column with an HNSW index and query it with SQL. The embeddings then live next to your products with joins, filters, transactions and your existing backups, and 200,000 vectors is well within its comfort zone.""",
        quick_bn=r"""pgvector চালু করো, HNSW index-সহ একটা `vector` column যোগ করো, আর SQL দিয়ে query করো। তাতে embedding product-এর পাশেই থাকে, join, filter, transaction আর আগের backup-সহ, আর 200,000 vector এর জন্য একদম সহজ কাজ।""",
        ex_en=r"""
            - **Option A** works for a demo but every query loads and scans all vectors in Node — slow, memory-hungry and impossible to filter efficiently.
            - **Option B** is false: with pgvector, PostgreSQL stores and indexes vectors well. A dedicated vector database (Pinecone, Qdrant, Weaviate, Milvus…) becomes attractive at much larger scale, with heavy filtered-search needs, or when you want managed vector-specific features — not as a default.
            - **Option C** is keyword search; it won't match "budget phone" with "সস্তা মোবাইল".

            Setup is small: `CREATE EXTENSION vector;`, a `vector(768)` column, an HNSW index with the right operator class, and `ORDER BY embedding <=> $1 LIMIT k`.
        """,
        ex_bn=r"""
            - **Option A** demo-র জন্য চলে, কিন্তু প্রতিটা query-তে Node-এ সব vector load করে scan করতে হয় — ধীর, memory-খেকো, আর দক্ষভাবে filter করা অসম্ভব।
            - **Option B** মিথ্যা: pgvector সহ PostgreSQL ভালোভাবেই vector রাখে আর index করে। Dedicated vector database (Pinecone, Qdrant, Weaviate, Milvus…) আকর্ষণীয় হয় অনেক বড় scale-এ, ভারী filtered-search-এর প্রয়োজনে, বা managed vector-specific feature চাইলে — default হিসেবে নয়।
            - **Option C** হলো keyword search; এটা "budget phone"-এর সাথে "সস্তা মোবাইল" মেলাবে না।

            Setup ছোট: `CREATE EXTENSION vector;`, একটা `vector(768)` column, সঠিক operator class সহ HNSW index, আর `ORDER BY embedding <=> $1 LIMIT k`।
        """,
        tip_en=r"""Mention "use the database you already operate until it hurts" — interviewers appreciate pragmatic, low-ops choices, followed by the signals that would make you switch.""",
        tip_bn=r""""যে database ইতিমধ্যে চালাও, সমস্যা না হওয়া পর্যন্ত সেটাই ব্যবহার করো" — এই কথাটা বলো; interviewer-রা বাস্তবসম্মত, কম-ops সিদ্ধান্ত পছন্দ করে, তারপর বলো কোন লক্ষণ দেখলে বদলাবে।""",
        refs=[PGV, PINECONE_VDB],
        related=["vec-013", "vec-021"],
    ),
    # ------------------------------------------------------------------ vec-017
    Q(
        id="vec-017", sub="Retrieval Quality", diff="medium", type="conceptual",
        prio="high", market="both", mins=7,
        tags=["recall-at-k", "mrr", "evaluation", "golden-set", "metrics"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""How do you measure retrieval quality in a semantic search or RAG system? Explain recall@k and MRR with a small worked example.""",
        q_bn=r"""Semantic search বা RAG system-এ retrieval quality কীভাবে মাপো? একটা ছোট হিসাবসহ উদাহরণ দিয়ে recall@k আর MRR ব্যাখ্যা করো।""",
        a_en=r"""
            First build a **golden test set**: real user questions, each labelled with the document(s) that should be retrieved. Then run retrieval and score it.

            - **Recall@k:** the share of queries where a relevant document appears in the top k. It answers "did we find it at all?" — critical for RAG, because the LLM can't use what wasn't retrieved.
            - **MRR (Mean Reciprocal Rank):** for each query take `1 / rank` of the first relevant result (0 if it's missing), then average. It rewards putting the right document near the top.

            **Example (k = 5), one relevant doc per query:**
            - q1: relevant doc at rank 1 → hit, reciprocal rank 1
            - q2: relevant doc at rank 3 → hit, reciprocal rank 1/3
            - q3: relevant doc at rank 8 → miss in the top 5, reciprocal rank 0

            Recall@5 = 2/3 ≈ **0.67**; MRR@5 = (1 + 1/3 + 0) / 3 ≈ **0.44**.

            I track these before and after every change — chunk size, embedding model, `ef_search`, hybrid weights — so improvements are measured, not guessed.
        """,
        a_bn=r"""
            প্রথমে একটা **golden test set** তৈরি করো: আসল user-এর প্রশ্ন, প্রতিটার সাথে কোন document(গুলো) retrieve হওয়া উচিত তার label। তারপর retrieval চালিয়ে score দাও।

            - **Recall@k:** কত শতাংশ query-তে top k-এর মধ্যে একটা relevant document এসেছে। এটা উত্তর দেয় "আদৌ খুঁজে পেয়েছি কি?" — RAG-এর জন্য অত্যন্ত জরুরি, কারণ যা retrieve হয়নি LLM তা ব্যবহার করতে পারে না।
            - **MRR (Mean Reciprocal Rank):** প্রতিটা query-র প্রথম relevant result-এর `1 / rank` নাও (না থাকলে 0), তারপর গড় করো। সঠিক document উপরের দিকে রাখলে এটা পুরস্কার দেয়।

            **উদাহরণ (k = 5), প্রতি query-তে একটা relevant doc:**
            - q1: relevant doc rank 1-এ → hit, reciprocal rank 1
            - q2: relevant doc rank 3-এ → hit, reciprocal rank 1/3
            - q3: relevant doc rank 8-এ → top 5-এ নেই, reciprocal rank 0

            Recall@5 = 2/3 ≈ **0.67**; MRR@5 = (1 + 1/3 + 0) / 3 ≈ **0.44**।

            প্রতিটা পরিবর্তনের আগে-পরে — chunk size, embedding model, `ef_search`, hybrid weight — আমি এগুলো track করি, যাতে উন্নতি অনুমান নয়, মাপা হয়।
        """,
        quick_en=r"""Build a golden set of real questions labelled with the right documents. Recall@k checks whether the relevant documents appear in the top k (here, with one relevant doc per query, 2/3 ≈ 0.67); MRR averages 1/rank of the first relevant result (≈ 0.44). Track both before and after every change.""",
        quick_bn=r"""আসল প্রশ্ন আর তাদের সঠিক document দিয়ে label করা একটা golden set বানাও। Recall@k দেখে relevant document top k-তে আসছে কিনা (এখানে প্রতি query-তে একটা relevant doc, তাই 2/3 ≈ 0.67); MRR প্রথম relevant result-এর 1/rank-এর গড় (≈ 0.44)। প্রতিটা change-এর আগে-পরে দুটোই মাপো।""",
        ex_en=r"""
            - **Building the golden set:** start with 50–200 real queries from logs or support tickets, include both Bangla and English (and Banglish if users type it), and include hard cases. Label which chunks or documents answer each one.
            - **Other metrics:** precision@k (how much of the top k is relevant — matters for LLM context budget), nDCG (handles graded relevance and multiple relevant docs).
            - **ANN recall vs retrieval recall:** "index recall" compares ANN results with exact search; "retrieval recall" compares results with human labels. Both matter, and they fail differently.
            - **Separate retrieval from generation:** if answers are wrong, check whether the right chunk was retrieved before blaming the LLM.
            - **Online signals:** clicks, "was this helpful?", reformulated queries and zero-result rates complement offline metrics.
        """,
        ex_bn=r"""
            - **Golden set তৈরি:** log বা support ticket থেকে 50–200টা আসল query দিয়ে শুরু করো, Bangla আর English (user লিখলে Banglish-ও) দুটোই রাখো, আর কঠিন case-ও রাখো। প্রতিটার উত্তর কোন chunk বা document-এ আছে label করো।
            - **অন্যান্য metric:** precision@k (top k-এর কতটা relevant — LLM context budget-এর জন্য গুরুত্বপূর্ণ), nDCG (relevance-এর মাত্রা আর একাধিক relevant doc সামলায়)।
            - **ANN recall বনাম retrieval recall:** "index recall" ANN result-কে exact search-এর সাথে তুলনা করে; "retrieval recall" result-কে মানুষের দেওয়া label-এর সাথে তুলনা করে। দুটোই জরুরি, আর এরা আলাদা কারণে fail করে।
            - **Retrieval আর generation আলাদা করো:** উত্তর ভুল হলে LLM-কে দোষ দেওয়ার আগে দেখো সঠিক chunk retrieve হয়েছিল কিনা।
            - **Online signal:** click, "এটা কি সাহায্য করেছে?", বারবার বদলে লেখা query আর zero-result rate offline metric-এর পরিপূরক।
        """,
        tip_en=r"""Do the arithmetic out loud — it's quick and shows you truly understand the metrics. Then say "I'd run this on every change", which signals an engineering mindset.""",
        tip_bn=r"""হিসাবটা জোরে জোরে করো — দ্রুত হয়, আর বোঝা যায় তুমি metric-গুলো সত্যিই বোঝো। তারপর বলো "প্রতিটা পরিবর্তনে আমি এটা চালাব" — এতে engineering মানসিকতা বোঝা যায়।""",
        mist_en=r"""Judging quality by eyeballing a few queries, confusing recall with precision, or evaluating only English queries for a bilingual product.""",
        mist_bn=r"""কয়েকটা query চোখে দেখে quality বিচার করা, recall আর precision গুলিয়ে ফেলা, অথবা দ্বিভাষিক product-এ শুধু English query দিয়ে মূল্যায়ন করা।""",
        code=r"""
            def recall_at_k(results, relevant, k):
                hits = sum(1 for q, ranked in results.items() if relevant[q] in ranked[:k])
                return hits / len(results)

            def mrr_at_k(results, relevant, k):
                total = 0.0
                for q, ranked in results.items():
                    top = ranked[:k]
                    if relevant[q] in top:
                        total += 1 / (top.index(relevant[q]) + 1)
                return total / len(results)

            results = {
                "q1": ["d3", "d8", "d1", "d4", "d9"],
                "q2": ["d7", "d2", "d5", "d6", "d0"],
                "q3": ["d4", "d6", "d2", "d1", "d3", "d5", "d9", "d8"],
            }
            relevant = {"q1": "d3", "q2": "d5", "q3": "d8"}

            print(round(recall_at_k(results, relevant, 5), 2))
            print(round(mrr_at_k(results, relevant, 5), 2))
        """,
        lang="python",
        output=r"""
            0.67
            0.44
        """,
        follow=[
            ("How would you build a golden test set if you have no labelled data yet?", "এখনো কোনো labelled data না থাকলে golden test set কীভাবে তৈরি করবে?"),
            ("When is nDCG a better choice than MRR?", "কখন MRR-এর চেয়ে nDCG ভালো পছন্দ?"),
        ],
        related=["vec-028", "vec-020"],
        refs=[WIKI_IREVAL, WIKI_MRR],
    ),
    # ------------------------------------------------------------------ vec-018
    Q(
        id="vec-018", sub="Embedding Model Changes", diff="medium", type="debugging",
        prio="high", market="both", mins=8,
        tags=["debugging", "pgvector", "operator-class", "embedding-model", "index"],
        ver="pgvector 0.8.7 (PostgreSQL 18); postgres.js", vs=True, status="stable",
        q_en=r"""After a refactor, the knowledge-base search returns strange, irrelevant results and has become slow as the table grew to 2 million rows. No errors are thrown. Both embedding models output 768 dimensions. Find the bugs.""",
        q_bn=r"""একটা refactor-এর পর knowledge-base search অদ্ভুত, অপ্রাসঙ্গিক result দিচ্ছে, আর table 20 লাখ row-এ পৌঁছানোয় ধীরও হয়ে গেছে। কোনো error throw হচ্ছে না। দুটো embedding model-ই 768 dimension output দেয়। Bug-গুলো খুঁজে বের করো।""",
        a_en=r"""
            1. **Different models for documents and queries.** Ingestion uses `kb-embed-v2`, search uses `kb-embed-v1`. Because both output 768 dimensions, nothing errors — but vectors from different models live in different spaces, so distances are meaningless. That's the "strange results".
            2. **Operator class doesn't match the query operator.** The index is built with `vector_l2_ops` (for `<->`), but the query uses `<=>` (cosine). PostgreSQL can't use the index for that operator, so it scans and sorts all 2 million rows.
            3. **Ordering by an expression, descending.** `ORDER BY similarity DESC` sorts on `1 - distance`; pgvector can only use an index for `ORDER BY <distance operator> ASC LIMIT k`. Even with the right index, this query can't use it.

            Fix: one shared model constant (and an `embedding_model` column to enforce it), an HNSW index with `vector_cosine_ops`, and `ORDER BY embedding <=> $1 LIMIT 5`, computing similarity only in the `SELECT` list.
        """,
        a_bn=r"""
            1. **Document আর query-তে আলাদা model।** Ingestion ব্যবহার করছে `kb-embed-v2`, search ব্যবহার করছে `kb-embed-v1`। দুটোই 768 dimension দেয় বলে কোনো error হয় না — কিন্তু আলাদা model-এর vector আলাদা space-এ থাকে, তাই distance অর্থহীন। এটাই "অদ্ভুত result"।
            2. **Operator class query-র operator-এর সাথে মেলে না।** Index বানানো হয়েছে `vector_l2_ops` দিয়ে (`<->`-এর জন্য), কিন্তু query ব্যবহার করছে `<=>` (cosine)। PostgreSQL ওই operator-এর জন্য index ব্যবহার করতে পারে না, তাই 20 লাখ row-ই scan করে sort করে।
            3. **Expression দিয়ে, descending order-এ sort।** `ORDER BY similarity DESC` sort করে `1 - distance` দিয়ে; pgvector index ব্যবহার করতে পারে শুধু `ORDER BY <distance operator> ASC LIMIT k`-এর জন্য। সঠিক index থাকলেও এই query সেটা ব্যবহার করতে পারবে না।

            সমাধান: একটাই shared model constant (আর এটা নিশ্চিত করতে একটা `embedding_model` column), `vector_cosine_ops` সহ HNSW index, আর `ORDER BY embedding <=> $1 LIMIT 5` — similarity শুধু `SELECT` list-এ হিসাব করা।
        """,
        quick_en=r"""Documents are embedded with `kb-embed-v2` but queries with `kb-embed-v1`, so distances are meaningless even though nothing errors. The index uses `vector_l2_ops` while the query uses `<=>`, and `ORDER BY similarity DESC` can't use an index anyway. Fix: one model, `vector_cosine_ops`, and `ORDER BY embedding <=> $1 LIMIT k`.""",
        quick_bn=r"""Document embed হচ্ছে `kb-embed-v2` দিয়ে কিন্তু query `kb-embed-v1` দিয়ে, তাই কোনো error না হলেও distance অর্থহীন। Index `vector_l2_ops`-এ, অথচ query `<=>` ব্যবহার করে, আর `ORDER BY similarity DESC` এমনিতেও index ব্যবহার করতে পারে না। Fix: একটাই model, `vector_cosine_ops`, আর `ORDER BY embedding <=> $1 LIMIT k`।""",
        ex_en=r"""
            - **Why no error for bug 1:** pgvector only checks dimensions. Two models with equal dimensions are a silent failure — that's why storing the model name/version per row and checking it in queries is valuable.
            - **Verify with `EXPLAIN`:** a healthy query plan shows `Index Scan using ..._embedding_idx` with `Order By: (embedding <=> ...)`; the buggy one shows `Sort` over a sequential scan.
            - **Model-specific input rules:** some models require prefixes (the e5 family uses `query: ` / `passage: `) or normalisation. Put embedding logic in one shared module used by both ingestion and search.
            - **Regression test:** keep a handful of "known answer" queries in CI; a model mismatch drops their scores immediately.
        """,
        ex_bn=r"""
            - **Bug 1-এ error কেন হয় না:** pgvector শুধু dimension check করে। সমান dimension-এর দুইটা model চুপচাপ ব্যর্থতা তৈরি করে — এজন্যই প্রতিটা row-এ model-এর নাম/version রেখে query-তে check করা মূল্যবান।
            - **`EXPLAIN` দিয়ে যাচাই:** সুস্থ query plan-এ দেখা যায় `Index Scan using ..._embedding_idx` সাথে `Order By: (embedding <=> ...)`; bug-ওয়ালা plan-এ sequential scan-এর ওপর `Sort`।
            - **Model-নির্দিষ্ট input নিয়ম:** কিছু model-এ prefix লাগে (e5 family `query: ` / `passage: ` ব্যবহার করে) বা normalisation লাগে। Embedding-এর logic একটা shared module-এ রাখো, যেটা ingestion আর search দুটোই ব্যবহার করবে।
            - **Regression test:** CI-তে কয়েকটা "জানা উত্তর"-এর query রাখো; model mismatch হলে তাদের score সাথে সাথে পড়ে যায়।
        """,
        tip_en=r"""Separate correctness bugs (wrong model) from performance bugs (index unusable), and mention `EXPLAIN` as your verification tool. Structured debugging beats spotting one issue.""",
        tip_bn=r"""Correctness bug (ভুল model) আর performance bug (index ব্যবহার অযোগ্য) আলাদা করো, আর যাচাইয়ের tool হিসেবে `EXPLAIN` উল্লেখ করো। একটা সমস্যা ধরার চেয়ে কাঠামোবদ্ধ debugging বেশি প্রভাব ফেলে।""",
        mist_en=r"""Fixing only the slowness by adding more indexes, or assuming equal dimensions mean the models are compatible.""",
        mist_bn=r"""আরও index যোগ করে শুধু ধীরগতি ঠিক করা, অথবা ধরে নেওয়া যে সমান dimension মানে model দুটো compatible।""",
        code=r"""
            -- migration.sql
            CREATE INDEX kb_chunks_embedding_idx ON kb_chunks USING hnsw (embedding vector_l2_ops);

            // ingest.js
            const vector = await embed(chunk.text, { model: 'kb-embed-v2' });   // 768 dims
            await sql`INSERT INTO kb_chunks (id, content, embedding)
                      VALUES (${chunk.id}, ${chunk.text}, ${JSON.stringify(vector)}::vector)`;

            // search.js
            export async function search(query) {
              const q = await embed(query, { model: 'kb-embed-v1' });             // 768 dims
              return sql`
                SELECT id, content, 1 - (embedding <=> ${JSON.stringify(q)}::vector) AS similarity
                FROM kb_chunks
                ORDER BY similarity DESC
                LIMIT 5`;
            }
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            -- migration.sql
            DROP INDEX IF EXISTS kb_chunks_embedding_idx;
            CREATE INDEX kb_chunks_embedding_idx ON kb_chunks USING hnsw (embedding vector_cosine_ops);
            ALTER TABLE kb_chunks ADD COLUMN embedding_model text NOT NULL DEFAULT 'kb-embed-v2';

            // embedding.js — single source of truth for ingestion AND search
            export const EMBED_MODEL = 'kb-embed-v2';
            export const embedText = (text) => embed(text, { model: EMBED_MODEL });

            // search.js
            export async function search(query) {
              const q = JSON.stringify(await embedText(query));
              return sql`
                SELECT id, content, 1 - (embedding <=> ${q}::vector) AS similarity
                FROM kb_chunks
                WHERE embedding_model = ${EMBED_MODEL}
                ORDER BY embedding <=> ${q}::vector      -- ascending distance -> index usable
                LIMIT 5`;
            }
        """)],
        follow=[
            ("How would `EXPLAIN` output differ before and after the fix?", "Fix-এর আগে আর পরে `EXPLAIN` output কীভাবে আলাদা হবে?"),
            ("How would you catch a model mismatch automatically before it reaches production?", "Production-এ পৌঁছানোর আগেই model mismatch কীভাবে automatically ধরবে?"),
        ],
        related=["vec-013", "vec-012", "vec-024"],
        refs=[PGV, E5],
    ),
    # ------------------------------------------------------------------ vec-019
    Q(
        id="vec-019", sub="Production Use Cases", diff="medium", type="scenario",
        prio="medium", market="both", mins=8,
        tags=["deduplication", "support-tickets", "similarity-threshold", "multilingual"],
        ver="Version-independent concept (example: pgvector 0.8.7)", vs=False, status="stable",
        q_en=r"""Your support team receives tickets in Bangla and English, and many are duplicates of the same issue — for example "bKash payment failed" in English and the same complaint written in Bangla. How would you use embeddings to detect duplicate tickets?""",
        q_bn=r"""তোমার support team Bangla আর English-এ ticket পায়, আর অনেকগুলোই একই সমস্যার duplicate ("bKash payment failed", "পেমেন্ট হচ্ছে না")। Duplicate ticket শনাক্ত করতে embedding কীভাবে ব্যবহার করবে?""",
        a_en=r"""
            **1. Clarify the goal:** suggest possible duplicates to agents, auto-merge, or detect incidents (a spike of similar tickets)? Wrongly merging two different problems is worse than missing a duplicate, so I'd start with **suggestions**.

            **2. Pipeline:**
            - Clean the text (strip signatures, quoted replies, phone numbers/PII), combine subject + first message.
            - Embed with a **multilingual** model so Bangla and English descriptions of the same problem land close together.
            - On each new ticket, search the nearest open tickets from the last ~14 days, filtered by product/channel, and show those above a similarity threshold as "possible duplicates".

            **3. Choose the threshold with data:** label a few hundred ticket pairs as duplicate / not duplicate, compute precision and recall at different thresholds, and pick the trade-off the support team prefers.

            **4. Bonus — incident detection:** if many new tickets cluster around one centroid within an hour, alert on-call; it's often an outage (e.g. a payment gateway down).
        """,
        a_bn=r"""
            **1. লক্ষ্য পরিষ্কার করো:** agent-কে সম্ভাব্য duplicate suggest করা, automatically merge করা, নাকি incident শনাক্ত করা (একই রকম ticket-এর হঠাৎ বৃদ্ধি)? দুইটা আলাদা সমস্যা ভুল করে merge করা একটা duplicate miss করার চেয়ে খারাপ, তাই আমি শুরু করব **suggestion** দিয়ে।

            **2. Pipeline:**
            - Text পরিষ্কার করো (signature, quoted reply, phone number/PII বাদ দাও), subject + প্রথম message একসাথে করো।
            - **Multilingual** model দিয়ে embed করো, যাতে একই সমস্যার Bangla আর English বর্ণনা কাছাকাছি পড়ে।
            - প্রতিটা নতুন ticket-এ গত ~14 দিনের সবচেয়ে কাছের open ticket খোঁজো, product/channel দিয়ে filter করে, আর একটা similarity threshold-এর ওপরে থাকাগুলো "সম্ভাব্য duplicate" হিসেবে দেখাও।

            **3. Data দিয়ে threshold ঠিক করো:** কয়েকশো ticket জোড়াকে duplicate / duplicate নয় হিসেবে label করো, বিভিন্ন threshold-এ precision আর recall হিসাব করো, আর support team যে trade-off পছন্দ করে সেটা বেছে নাও।

            **4. বাড়তি — incident শনাক্তকরণ:** এক ঘণ্টার মধ্যে অনেক নতুন ticket একটা centroid-এর চারপাশে জড়ো হলে on-call-কে alert দাও; প্রায়ই এটা একটা outage (যেমন payment gateway down)।
        """,
        quick_en=r"""Embed each cleaned ticket (subject plus first message) with a multilingual model, search the nearest recent open tickets filtered by product or channel, and show those above a similarity threshold as possible duplicates. Tune the threshold on labelled pairs, and start with suggestions rather than auto-merging.""",
        quick_bn=r"""প্রতিটা পরিষ্কার করা ticket (subject আর প্রথম message) multilingual model দিয়ে embed করো, product বা channel দিয়ে filter করে সাম্প্রতিক open ticket-এর মধ্যে সবচেয়ে কাছেরগুলো খোঁজো, আর similarity threshold-এর ওপরে থাকলে possible duplicate হিসেবে দেখাও। Label করা pair দিয়ে threshold ঠিক করো, আর auto-merge না করে suggestion দিয়ে শুরু করো।""",
        ex_en=r"""
            - **Short tickets are hard:** "not working" is similar to everything. Combine similarity with metadata (same product, same error code) or require a minimum text length.
            - **Banglish:** many users write romanised Bangla ("payment hocche na"); test the model on it and consider adding keyword features.
            - **Thresholds are model-specific** and drift when you change the model — re-tune after any model change.
            - **Privacy:** tickets contain phone numbers, transaction ids and addresses. Mask PII before sending text to an external embedding API, and respect retention rules.
            - **Feedback loop:** when agents accept or reject a suggestion, log it — it becomes labelled data for re-tuning.
        """,
        ex_bn=r"""
            - **ছোট ticket কঠিন:** "not working" সবকিছুর সাথেই মেলে। Similarity-র সাথে metadata (একই product, একই error code) মেলাও, বা ন্যূনতম text length রাখো।
            - **Banglish:** অনেক user romanised Bangla-য় লেখে ("payment hocche na"); model-কে এটা দিয়ে test করো আর keyword feature যোগ করার কথা ভাবো।
            - **Threshold model-নির্ভর**, আর model বদলালে সরে যায় — যেকোনো model পরিবর্তনের পর আবার tune করো।
            - **Privacy:** ticket-এ phone number, transaction id আর ঠিকানা থাকে। External embedding API-তে পাঠানোর আগে PII mask করো, আর retention নিয়ম মেনে চলো।
            - **Feedback loop:** agent suggestion গ্রহণ বা বাতিল করলে log করো — এটাই re-tuning-এর labelled data হয়ে যায়।
        """,
        tip_en=r"""Emphasise "suggest, don't auto-merge" and "tune the threshold on labelled pairs". Those two decisions show product sense plus engineering rigour.""",
        tip_bn=r""""Suggest করো, auto-merge নয়" আর "labelled জোড়া দিয়ে threshold tune করো" — এই দুইটা সিদ্ধান্তে জোর দাও। এতে product sense আর engineering-এর কঠোরতা দুটোই দেখা যায়।""",
        mist_en=r"""Picking a threshold like 0.8 by gut feeling, auto-merging without human review, or comparing new tickets against years of closed tickets with no time or product filter.""",
        mist_bn=r"""অনুমানে 0.8-এর মতো একটা threshold বেছে নেওয়া, মানুষের review ছাড়া auto-merge করা, অথবা কোনো সময় বা product filter ছাড়াই নতুন ticket-কে বছরের পর বছরের বন্ধ ticket-এর সাথে তুলনা করা।""",
        code=r"""
            -- Candidate duplicates for a new ticket ($1 = its embedding)
            SELECT id, subject, 1 - (embedding <=> $1) AS similarity
            FROM tickets
            WHERE status = 'open'
              AND product_id = $2
              AND created_at > now() - interval '14 days'
            ORDER BY embedding <=> $1
            LIMIT 5;
            -- App: show as "possible duplicate" only if similarity >= threshold tuned on labelled pairs
        """,
        lang="sql",
        follow=[
            ("How would you evaluate precision and recall for different thresholds?", "বিভিন্ন threshold-এ precision আর recall কীভাবে মূল্যায়ন করবে?"),
            ("How could you detect a sudden spike of similar tickets in near real time?", "একই রকম ticket-এর হঠাৎ বৃদ্ধি প্রায় real time-এ কীভাবে ধরবে?"),
        ],
        related=["vec-017", "vec-022"],
        refs=[PGV, E5],
    ),
    # ------------------------------------------------------------------ vec-026
    Q(
        id="vec-026", sub="Data Privacy", diff="hard", type="debugging",
        prio="high", market="both", mins=12,
        tags=["multi-tenant", "access-control", "rls", "sql-injection", "rag-security"],
        ver="pgvector 0.8.7 (PostgreSQL 18); node-postgres 8.x; Express 5", vs=True, status="stable",
        q_en=r"""This endpoint powers a multi-tenant RAG assistant. A security review says tenant data can leak and the endpoint is injectable. Find every problem and fix it.""",
        q_bn=r"""এই endpoint একটা multi-tenant RAG assistant চালায়। Security review বলছে tenant-এর data ফাঁস হতে পারে আর endpoint-টা injectable। প্রতিটা সমস্যা খুঁজে বের করে ঠিক করো।""",
        a_en=r"""
            1. **Tenant id comes from the request body.** Any user can send another company's `tenantId`. The tenant must come from the authenticated session/token (`req.user.tenantId`).
            2. **Retrieval isn't filtered by tenant at all.** The SQL searches every tenant's chunks; the "only use tenant X's documents" line in the prompt is **not** a security boundary — the LLM can still quote other tenants' text, and prompt injection can make it do so deliberately.
            3. **SQL injection.** `category` from the request body is interpolated straight into the SQL string (`'${category}'`). A value like `x' OR '1'='1` breaks out of the string and rewrites the query.
            4. **No defence in depth.** One forgotten `WHERE` in a future query would leak again.
            5. **Recall side effect:** once you add `WHERE tenant_id = $2` on an HNSW search, small tenants can get too few results (post-filtering).

            **Fix:** take the tenant from auth; parameterise everything; filter by tenant **inside** the SQL; add PostgreSQL **row-level security** keyed on a per-transaction setting so the database itself refuses cross-tenant rows; enable iterative index scans (or per-tenant partitions) so filtered searches still return enough rows; log retrievals for audit.
        """,
        a_bn=r"""
            1. **Tenant id আসছে request body থেকে।** যেকোনো user অন্য company-র `tenantId` পাঠাতে পারে। Tenant আসতে হবে authenticated session/token থেকে (`req.user.tenantId`)।
            2. **Retrieval tenant দিয়ে filter-ই করা হয় না।** SQL সব tenant-এর chunk-এ খোঁজে; prompt-এর "শুধু tenant X-এর document ব্যবহার করো" লাইনটা **কোনো** security boundary নয় — LLM তবুও অন্য tenant-এর text quote করতে পারে, আর prompt injection দিয়ে ইচ্ছাকৃতভাবে করানোও যায়।
            3. **SQL injection।** Request body-র `category` সরাসরি SQL string-এ বসানো হয়েছে (`'${category}'`)। `x' OR '1'='1`-এর মতো একটা value string ভেঙে বেরিয়ে query-টাই বদলে দিতে পারে।
            4. **Defence in depth নেই।** ভবিষ্যতের কোনো query-তে একটা `WHERE` ভুলে গেলেই আবার ফাঁস হবে।
            5. **Recall-এর পার্শ্বপ্রতিক্রিয়া:** HNSW search-এ `WHERE tenant_id = $2` যোগ করলে ছোট tenant খুব কম result পেতে পারে (post-filtering)।

            **সমাধান:** tenant নাও auth থেকে; সবকিছু parameterise করো; tenant দিয়ে filter করো SQL-এর **ভেতরেই**; per-transaction setting-ভিত্তিক PostgreSQL **row-level security** যোগ করো, যাতে database নিজেই অন্য tenant-এর row দিতে অস্বীকার করে; iterative index scan (বা tenant-ভিত্তিক partition) চালু করো যাতে filter করা search-ও যথেষ্ট row দেয়; audit-এর জন্য retrieval log করো।
        """,
        quick_en=r"""The tenant id comes from the request body, retrieval isn't filtered by tenant (a prompt instruction isn't a security boundary), and `category` is interpolated into the SQL. Fix: tenant from auth, parameterised SQL, a tenant filter inside the query, row-level security, and iterative scans so filtered searches still return enough rows.""",
        quick_bn=r"""Tenant id request body থেকে আসছে, retrieval-এ tenant filter নেই (prompt-এর নির্দেশ security boundary না), আর `category` সরাসরি SQL-এ বসানো হচ্ছে। Fix: auth থেকে tenant, parameterised SQL, query-র ভেতরেই tenant filter, row-level security, আর iterative scan যাতে filter-সহ search-ও যথেষ্ট row দেয়।""",
        ex_en=r"""
            - **RLS caveats:** superusers and roles with `BYPASSRLS` always bypass RLS, and the table owner bypasses it unless you use `FORCE ROW LEVEL SECURITY` — so the app should connect as a dedicated, unprivileged non-owner role. Use `set_config(..., true)` inside a transaction so the tenant setting can't leak to the next request on a pooled connection.
            - **Document-level permissions:** within a tenant, HR or finance documents may be restricted to some groups — store ACLs on chunks and filter on them too.
            - **Vectors are sensitive data:** embeddings can leak information about the source text (OWASP lists embedding inversion as a risk), so protect them like the text itself.
            - **Test it:** an automated test that queries as tenant A and asserts no tenant-B ids appear should run in CI.
        """,
        ex_bn=r"""
            - **RLS-এর সতর্কতা:** superuser আর `BYPASSRLS`-ওয়ালা role সবসময় RLS এড়িয়ে যায়, আর `FORCE ROW LEVEL SECURITY` না দিলে table owner-ও এড়িয়ে যায় — তাই app-কে একটা আলাদা, কম-ক্ষমতার non-owner role দিয়ে connect করা উচিত। Transaction-এর ভেতরে `set_config(..., true)` ব্যবহার করো, যাতে pooled connection-এ tenant setting পরের request-এ চলে না যায়।
            - **Document-level permission:** একই tenant-এর ভেতরেও HR বা finance document কিছু group-এর জন্য সীমিত থাকতে পারে — chunk-এ ACL রেখে সেটা দিয়েও filter করো।
            - **Vector-ও sensitive data:** embedding থেকে মূল text সম্পর্কে তথ্য ফাঁস হতে পারে (OWASP embedding inversion-কে ঝুঁকি হিসেবে তালিকাভুক্ত করেছে), তাই text-এর মতোই এগুলো সুরক্ষিত রাখো।
            - **Test করো:** tenant A হিসেবে query করে tenant B-র কোনো id আসছে না — এটা assert করা একটা automated test CI-তে চালাও।
        """,
        tip_en=r"""Say clearly: "the prompt is not an access-control layer." Then fix at three levels — auth (where the tenant comes from), query (filter + parameters) and database (RLS). Layered answers impress security-minded interviewers.""",
        tip_bn=r"""স্পষ্ট করে বলো: "prompt কোনো access-control layer নয়।" তারপর তিন স্তরে ঠিক করো — auth (tenant কোথা থেকে আসে), query (filter + parameter) আর database (RLS)। স্তরে স্তরে সাজানো উত্তর security-সচেতন interviewer-কে মুগ্ধ করে।""",
        mist_en=r"""Filtering results by tenant in JavaScript after the `LIMIT` (low recall and easy to forget), or trusting the LLM to ignore other tenants' context.""",
        mist_bn=r"""`LIMIT`-এর পরে JavaScript-এ tenant দিয়ে result filter করা (recall কম আর ভুলে যাওয়া সহজ), অথবা LLM অন্য tenant-এর context উপেক্ষা করবে বলে বিশ্বাস করা।""",
        code=r"""
            app.post('/api/ask', async (req, res) => {
              const { question, tenantId, category } = req.body;
              const qVec = await embed(question);

              const { rows } = await pool.query(`
                SELECT content FROM chunks
                WHERE category = '${category}'
                ORDER BY embedding <=> '${JSON.stringify(qVec)}'
                LIMIT 5`);

              const prompt = `You are the assistant for tenant ${tenantId}.
            Only use documents that belong to tenant ${tenantId}.
            Context:
            ${rows.map((r) => r.content).join('\n---\n')}
            Question: ${question}`;

              res.json({ answer: await llm(prompt) });
            });
        """,
        lang="javascript",
        extra=[dict(lang="javascript", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
            -- One-time setup (defence in depth). The app connects as a non-owner role.
            ALTER TABLE chunks ENABLE ROW LEVEL SECURITY;
            CREATE POLICY tenant_isolation ON chunks
              USING (tenant_id = current_setting('app.tenant_id')::bigint);

            // Express 5 route — tenant comes from auth, never from the body
            app.post('/api/ask', requireAuth, async (req, res) => {
              const tenantId = req.user.tenantId;
              const { question, category } = req.body;
              const qVec = JSON.stringify(await embed(question));

              const client = await pool.connect();
              let rows;
              try {
                await client.query('BEGIN');
                await client.query(`SELECT set_config('app.tenant_id', $1, true)`, [String(tenantId)]);
                await client.query('SET LOCAL hnsw.iterative_scan = relaxed_order');
                ({ rows } = await client.query(
                  `SELECT id, content
                   FROM chunks
                   WHERE tenant_id = $2                -- explicit filter (RLS is the backstop)
                     AND category = $3                 -- parameterised, never interpolated
                   ORDER BY embedding <=> $1::vector
                   LIMIT 5`,
                  [qVec, tenantId, category],
                ));
                await client.query('COMMIT');
              } catch (err) {
                await client.query('ROLLBACK');
                throw err;                            // Express 5 forwards it to the error handler
              } finally {
                client.release();
              }

              const context = rows.map((r) => r.content).join('\n---\n');
              res.json({ answer: await llm(buildPrompt(context, question)) });
            });
        """)],
        follow=[
            ("Would you choose one shared index with a tenant filter, or a partition per tenant? Why?", "Tenant filter সহ একটা shared index, নাকি প্রতি tenant-এ একটা partition — কোনটা বেছে নেবে, কেন?"),
            ("How can a malicious document inside one tenant still attack that tenant's users?", "একটা tenant-এর ভেতরের কোনো malicious document কীভাবে সেই tenant-এর user-দেরই আক্রমণ করতে পারে?"),
        ],
        related=["vec-025", "vec-031", "vec-022"],
        refs=[OWASP_LLM08, PG_RLS, PGV],
    ),
    # ------------------------------------------------------------------ vec-027
    Q(
        id="vec-027", sub="Vector Indexing Fundamentals", diff="hard", type="scenario",
        prio="medium", market="both", mins=12,
        tags=["scaling", "memory", "halfvec", "binary-quantization", "pgvector", "partitioning"],
        ver="pgvector 0.8.7 (halfvec/bit since 0.7.0; PostgreSQL 18)", vs=True, status="stable",
        q_en=r"""Your pgvector table has grown to 10 million chunks with 1536-dimensional embeddings. The HNSW index no longer fits in RAM, p95 query latency jumped, and index builds take hours. What are your options, roughly how much do they save, and what would you try first?""",
        q_bn=r"""তোমার pgvector table-এ এখন 1536-dimensional embedding সহ 1 কোটি chunk। HNSW index আর RAM-এ আঁটে না, p95 query latency লাফিয়ে বেড়েছে, আর index build-এ কয়েক ঘণ্টা লাগে। তোমার হাতে কী কী option আছে, মোটামুটি কতটা সাশ্রয় হয়, আর প্রথমে কোনটা চেষ্টা করবে?""",
        a_en=r"""
            **Size it first.** pgvector stores a `vector` in `4 × dims + 8` bytes: 10M × 6,152 B ≈ **61.5 GB** for the vectors alone. The HNSW index keeps its own copy of each vector plus neighbour links, so the total working set is well over 100 GB — far beyond RAM on a typical instance, which is why latency jumped.

            **Options:**
            1. **Half precision** — index `embedding::halfvec(1536)` (2 bytes per dimension): ≈ **30.8 GB** of vectors, usually with very little recall loss. Lowest effort: an expression index plus a query rewrite.
            2. **Fewer dimensions** — models trained Matryoshka-style (or with a `dimensions` option) can produce 512-dim vectors: ≈ 20.6 GB as float32, ~3× smaller, but requires re-embedding and re-evaluation.
            3. **Binary quantisation + re-ranking** — index `binary_quantize(embedding)::bit(1536)` (192 bytes per vector ≈ **1.9 GB**), fetch ~100 candidates by Hamming distance, then re-rank them with full vectors. Huge savings; validate recall.
            4. **Partitioning** by tenant, category or time — smaller per-partition indexes, and filters prune partitions.
            5. **Clean up** duplicate and stale chunks; `REINDEX CONCURRENTLY` + `VACUUM` after large deletes.
            6. **Bigger memory-optimised instances / read replicas**, or a dedicated vector DB with disk-based indexes if growth continues.

            **What I'd try first:** a half-precision HNSW index (cheap, reversible), measure recall@10 against exact search on a sample; if still too big, binary quantisation with re-ranking; plan dimension reduction as a longer-term re-embedding project.
        """,
        a_bn=r"""
            **আগে আকার হিসাব করো।** pgvector একটা `vector` রাখে `4 × dims + 8` byte-এ: 1 কোটি × 6,152 B ≈ শুধু vector-এর জন্যই **61.5 GB**। HNSW index প্রতিটা vector-এর নিজস্ব কপি আর neighbour link রাখে, তাই মোট working set 100 GB-এর অনেক বেশি — সাধারণ instance-এর RAM-এর অনেক বাইরে, latency বাড়ার কারণ এটাই।

            **Option-গুলো:**
            1. **Half precision** — `embedding::halfvec(1536)` index করো (প্রতি dimension-এ 2 byte): vector ≈ **30.8 GB**, সাধারণত recall-এর খুব সামান্য ক্ষতিতে। সবচেয়ে কম পরিশ্রম: একটা expression index আর query-র ছোট পরিবর্তন।
            2. **কম dimension** — Matryoshka-ধরনে (বা `dimensions` option সহ) train করা model 512-dim vector দিতে পারে: float32-এ ≈ 20.6 GB, ~3 গুণ ছোট, কিন্তু আবার embed আর মূল্যায়ন করতে হবে।
            3. **Binary quantisation + re-ranking** — `binary_quantize(embedding)::bit(1536)` index করো (প্রতি vector-এ 192 byte ≈ **1.9 GB**), Hamming distance দিয়ে ~100টা candidate আনো, তারপর পূর্ণ vector দিয়ে re-rank করো। বিশাল সাশ্রয়; recall যাচাই করো।
            4. Tenant, category বা সময় অনুযায়ী **partitioning** — প্রতি partition-এ ছোট index, আর filter partition বাদ দিতে পারে।
            5. Duplicate আর পুরনো chunk **পরিষ্কার করো**; বড় delete-এর পর `REINDEX CONCURRENTLY` + `VACUUM`।
            6. **বড় memory-optimised instance / read replica**, অথবা বৃদ্ধি চলতে থাকলে disk-based index সহ dedicated vector DB।

            **প্রথমে যা চেষ্টা করব:** half-precision HNSW index (সস্তা, ফেরত নেওয়া যায়), একটা sample-এ exact search-এর বিপরীতে recall@10 মাপব; তবুও বড় হলে re-ranking সহ binary quantisation; আর dimension কমানোকে দীর্ঘমেয়াদি re-embedding project হিসেবে plan করব।
        """,
        quick_en=r"""10M × 1536-dim float32 vectors is ≈ 61.5 GB before the HNSW graph, so the index no longer fits in RAM. Try a `halfvec` index first (about half the size, little recall loss), then binary quantisation with re-ranking, fewer dimensions, partitioning and cleanup, measuring recall against exact search each time.""",
        quick_bn=r"""10M × 1536-dim float32 vector মানে HNSW graph ছাড়াই ≈ 61.5 GB, তাই index আর RAM-এ ধরে না। আগে `halfvec` index চেষ্টা করো (প্রায় অর্ধেক size, recall সামান্য কমে), তারপর re-ranking-সহ binary quantisation, কম dimension, partitioning আর cleanup; প্রতিবার exact search-এর সাথে recall মেপে দেখো।""",
        ex_en=r"""
            - **Index limits:** pgvector can index `vector` up to 2,000 dimensions and `halfvec` up to 4,000 — another reason half precision matters for large models (e.g. 3,072 dims).
            - **Build speed:** raise `maintenance_work_mem` (pgvector logs a notice when the graph no longer fits) and `max_parallel_maintenance_workers`; build on a quiet primary, and use `CREATE INDEX CONCURRENTLY` to avoid blocking writes.
            - **Why re-ranking works:** binary codes are a coarse filter; the exact distances on a small candidate set restore most of the precision.
            - **Measure, don't assume:** compare each option's recall@k and p95 latency against an exact-search baseline on a fixed query sample before switching production traffic.
        """,
        ex_bn=r"""
            - **Index-এর সীমা:** pgvector `vector` index করতে পারে 2,000 dimension পর্যন্ত আর `halfvec` 4,000 পর্যন্ত — বড় model-এর (যেমন 3,072 dim) জন্য half precision জরুরি হওয়ার আরেক কারণ।
            - **Build-এর গতি:** `maintenance_work_mem` বাড়াও (graph আর না আঁটলে pgvector একটা notice log করে) আর `max_parallel_maintenance_workers`; চাপ কম থাকা primary-তে build করো, আর write block এড়াতে `CREATE INDEX CONCURRENTLY` ব্যবহার করো।
            - **Re-ranking কেন কাজ করে:** binary code একটা মোটা দাগের filter; ছোট candidate set-এ exact distance বেশিরভাগ precision ফিরিয়ে আনে।
            - **ধরে নিও না, মাপো:** production traffic বদলানোর আগে একটা নির্দিষ্ট query sample-এ প্রতিটা option-এর recall@k আর p95 latency exact-search baseline-এর সাথে তুলনা করো।
        """,
        tip_en=r"""Open with the back-of-the-envelope calculation — numbers make the problem concrete and show seniority. Then order options by effort vs savings and pick one, with a measurement plan.""",
        tip_bn=r"""শুরু করো মোটা দাগের হিসাব দিয়ে — সংখ্যা সমস্যাটাকে concrete করে আর seniority দেখায়। তারপর option-গুলো পরিশ্রম বনাম সাশ্রয় অনুযায়ী সাজিয়ে একটা বেছে নাও, মাপার পরিকল্পনা সহ।""",
        mist_en=r"""Only "adding more RAM", lowering `ef_search` until recall collapses without measuring it, or truncating vectors from a model that wasn't trained for shorter dimensions.""",
        mist_bn=r"""শুধু "আরও RAM যোগ করো" বলা, না মেপেই `ef_search` এতটা কমানো যে recall ভেঙে পড়ে, অথবা ছোট dimension-এর জন্য train করা হয়নি এমন model-এর vector কেটে ছোট করা।""",
        code=r"""
            -- 1. Half-precision index (2 bytes/dimension)
            CREATE INDEX CONCURRENTLY chunks_embedding_half_idx
              ON chunks USING hnsw ((embedding::halfvec(1536)) halfvec_cosine_ops);

            SELECT id FROM chunks
            ORDER BY embedding::halfvec(1536) <=> $1::halfvec(1536)
            LIMIT 10;

            -- 2. Binary quantisation + re-rank with full vectors
            CREATE INDEX CONCURRENTLY chunks_embedding_bin_idx
              ON chunks USING hnsw ((binary_quantize(embedding)::bit(1536)) bit_hamming_ops);

            SELECT id FROM (
              SELECT id, embedding FROM chunks
              ORDER BY binary_quantize(embedding)::bit(1536) <~> binary_quantize($1::vector)
              LIMIT 100
            ) candidates
            ORDER BY embedding <=> $1::vector
            LIMIT 10;
        """,
        lang="sql",
        follow=[
            ("How would you measure the recall cost of half precision or binary quantisation?", "Half precision বা binary quantisation-এ recall-এর ক্ষতি কীভাবে মাপবে?"),
            ("At what point would you move from pgvector to a dedicated vector database?", "কোন পর্যায়ে pgvector থেকে dedicated vector database-এ যাবে?"),
        ],
        related=["vec-014", "vec-024", "vec-021"],
        refs=[PGV, MATRYOSHKA],
    ),
    # ------------------------------------------------------------------ vec-031
    Q(
        id="vec-031", sub="Data Privacy", diff="extreme", type="architecture",
        prio="medium", market="international", mins=20,
        tags=["multi-tenancy", "architecture", "isolation", "saas", "data-residency"],
        ver="Version-independent architecture (pgvector 0.8.7 / dedicated vector DBs as examples)", vs=False, status="stable",
        q_en=r"""You're building a B2B "AI support assistant" SaaS. Each customer company uploads its own documents. How would you isolate tenants in the vector layer, and how does the design change as you grow from 50 tenants to 5,000 — including a few very large, regulated customers?""",
        q_bn=r"""তুমি একটা B2B "AI support assistant" SaaS বানাচ্ছ। প্রতিটা customer company নিজের document upload করে। Vector layer-এ tenant-দের কীভাবে আলাদা রাখবে, আর 50 tenant থেকে 5,000-এ বাড়ার সাথে — কয়েকটা খুব বড়, regulated customer সহ — design কীভাবে বদলাবে?""",
        a_en=r"""
            *(Advanced architecture question.)* There are three isolation models:

            **1. Shared index + tenant filter (pooled).** One table/collection with `tenant_id` on every row, filtered in every query, with row-level security as a backstop.
            - Cheapest and simplest to operate; works well for many small tenants.
            - Risks: one missing filter leaks data; filtered ANN can return too few results for small tenants (use iterative scans or tenant-aware indexing); a huge tenant becomes a noisy neighbour.

            **2. Partition / namespace per tenant.** PostgreSQL list partitioning by tenant (each partition has its own index) or the namespace/collection features of dedicated vector DBs.
            - Searches never see other tenants' vectors, recall is good, and deleting a tenant is a cheap `DROP`.
            - Overhead grows with thousands of partitions (planning time, many small indexes, migrations).

            **3. Dedicated database/cluster per tenant (silo).** Strongest isolation, per-tenant encryption keys and region (data residency), independent scaling and maintenance windows — at the highest cost and operational effort.

            **My design — tiered:** small tenants in a pooled index; mid-size tenants in their own partitions; large or regulated tenants in silos. A **tenant directory** maps each tenant to its tier and location, so moving a tenant between tiers is a background migration, not a rewrite.

            **Cross-cutting rules:** tenant id derived only from authentication; per-tenant quotas and rate limits; embedding model version tracked per tenant; complete deletion (source files, chunks, vectors, caches, and backup-retention policy); per-tenant audit logs; automated cross-tenant leakage tests in CI.
        """,
        a_bn=r"""
            *(Advanced architecture প্রশ্ন।)* Isolation-এর তিনটা মডেল আছে:

            **1. Shared index + tenant filter (pooled)।** একটা table/collection, প্রতিটা row-এ `tenant_id`, প্রতিটা query-তে filter, আর backstop হিসেবে row-level security।
            - সবচেয়ে সস্তা আর চালানো সহজ; অনেক ছোট tenant-এর জন্য ভালো কাজ করে।
            - ঝুঁকি: একটা filter বাদ পড়লেই data ফাঁস; filter করা ANN ছোট tenant-কে খুব কম result দিতে পারে (iterative scan বা tenant-aware indexing ব্যবহার করো); বিশাল একটা tenant noisy neighbour হয়ে যায়।

            **2. প্রতি tenant-এ partition / namespace।** Tenant অনুযায়ী PostgreSQL list partitioning (প্রতিটা partition-এর নিজস্ব index) বা dedicated vector DB-র namespace/collection feature।
            - Search কখনো অন্য tenant-এর vector দেখে না, recall ভালো, আর tenant মুছতে শুধু একটা সস্তা `DROP`।
            - হাজারো partition হলে overhead বাড়ে (planning time, অনেক ছোট index, migration)।

            **3. প্রতি tenant-এ আলাদা database/cluster (silo)।** সবচেয়ে শক্ত isolation, tenant-ভিত্তিক encryption key আর region (data residency), স্বাধীন scaling আর maintenance window — কিন্তু খরচ আর operational পরিশ্রম সবচেয়ে বেশি।

            **আমার design — স্তরভিত্তিক:** ছোট tenant pooled index-এ; মাঝারি tenant নিজস্ব partition-এ; বড় বা regulated tenant silo-তে। একটা **tenant directory** প্রতিটা tenant-কে তার স্তর আর অবস্থানের সাথে map করে, তাই এক স্তর থেকে আরেক স্তরে tenant সরানো একটা background migration, পুনর্লিখন নয়।

            **সব স্তরের জন্য নিয়ম:** tenant id শুধু authentication থেকে আসবে; tenant-ভিত্তিক quota আর rate limit; প্রতি tenant-এ embedding model version track করা; সম্পূর্ণ deletion (source file, chunk, vector, cache, আর backup-retention policy); tenant-ভিত্তিক audit log; CI-তে automated cross-tenant leakage test।
        """,
        quick_en=r"""There are three isolation models: a shared index filtered by `tenant_id` with row-level security (cheap, but leak and recall risks), a partition or namespace per tenant, or a dedicated database per tenant (strongest, costliest). Tier them: pooled for small tenants, partitions for mid-size, silos for large or regulated ones.""",
        quick_bn=r"""Isolation-এর তিনটা model: `tenant_id` দিয়ে filter করা shared index আর row-level security (সস্তা, কিন্তু leak আর recall-এর ঝুঁকি), প্রতি tenant-এ আলাদা partition বা namespace, অথবা প্রতি tenant-এ আলাদা database (সবচেয়ে শক্ত, সবচেয়ে দামি)। Tier করো: ছোট tenant pooled, মাঝারি tenant partition-এ, বড় বা regulated tenant silo-তে।""",
        ex_en=r"""
            - **Why tiers:** 5,000 silos is an operations nightmare; one pooled index with a 2-million-document tenant next to 4,000 tiny ones gives poor filtered recall and noisy-neighbour latency. Tiering matches cost to customer value and risk.
            - **Data residency & compliance:** regulated customers may require data to stay in a specific region or under their own encryption keys — only silos (or region-specific pools) satisfy that cleanly.
            - **Right to deletion:** vectors are derived personal data. Deleting a tenant or a user's documents must remove embeddings too, and backups must expire on a known schedule.
            - **External embedding APIs:** decide per tier whether text may leave your infrastructure; some customers will require self-hosted models.
            - **Observability per tenant:** latency, cost, token usage and retrieval quality per tenant help you spot who should move tiers.
        """,
        ex_bn=r"""
            - **স্তর কেন:** 5,000টা silo চালানো operations-এর দুঃস্বপ্ন; আবার 4,000টা ছোট tenant-এর পাশে 20 লাখ document-এর একটা tenant নিয়ে একটা pooled index filter করা recall খারাপ করে আর noisy-neighbour latency তৈরি করে। স্তরভিত্তিক design খরচকে customer-এর মূল্য আর ঝুঁকির সাথে মেলায়।
            - **Data residency ও compliance:** regulated customer চাইতে পারে data নির্দিষ্ট region-এ বা তাদের নিজস্ব encryption key-এর অধীনে থাকুক — শুধু silo (বা region-নির্দিষ্ট pool) এটা পরিষ্কারভাবে পূরণ করে।
            - **মুছে ফেলার অধিকার:** vector হলো personal data থেকে তৈরি data। Tenant বা কোনো user-এর document মুছলে embedding-ও মুছতে হবে, আর backup একটা জানা সময়সূচিতে expire হতে হবে।
            - **External embedding API:** প্রতিটা স্তরে ঠিক করো text তোমার infrastructure-এর বাইরে যেতে পারবে কিনা; কিছু customer self-hosted model দাবি করবে।
            - **Tenant-ভিত্তিক observability:** tenant অনুযায়ী latency, খরচ, token ব্যবহার আর retrieval quality দেখলে বোঝা যায় কাকে অন্য স্তরে সরানো উচিত।
        """,
        tip_en=r"""Present the three models as a spectrum (pool → partition → silo) with cost vs isolation trade-offs, then propose a tiered mix and how tenants migrate between tiers. That's the classic SaaS architecture answer interviewers look for.""",
        tip_bn=r"""তিনটা মডেলকে একটা পরিসর হিসেবে দেখাও (pool → partition → silo), খরচ বনাম isolation-এর trade-off সহ, তারপর একটা স্তরভিত্তিক মিশ্রণ আর tenant কীভাবে এক স্তর থেকে আরেক স্তরে সরে সেটা প্রস্তাব করো। Interviewer-রা ঠিক এই classic SaaS architecture উত্তরটাই খোঁজে।""",
        mist_en=r"""Choosing one model for everyone, relying on application filters without a database-level backstop, or forgetting that deleting documents must also delete their vectors and cached answers.""",
        mist_bn=r"""সবার জন্য একটাই মডেল বেছে নেওয়া, database-level backstop ছাড়া শুধু application filter-এর ওপর ভরসা করা, অথবা ভুলে যাওয়া যে document মুছলে তার vector আর cached answer-ও মুছতে হবে।""",
        code=r"""
            -- Partition per mid-size tenant (each partition gets its own HNSW index)
            CREATE TABLE chunks (
              id        bigint GENERATED ALWAYS AS IDENTITY,
              tenant_id bigint NOT NULL,
              content   text   NOT NULL,
              embedding vector(768) NOT NULL,
              PRIMARY KEY (tenant_id, id)
            ) PARTITION BY LIST (tenant_id);

            CREATE TABLE chunks_t42 PARTITION OF chunks FOR VALUES IN (42);
            CREATE TABLE chunks_pool PARTITION OF chunks DEFAULT;   -- small tenants share this one

            CREATE INDEX ON chunks_t42  USING hnsw (embedding vector_cosine_ops);
            CREATE INDEX ON chunks_pool USING hnsw (embedding vector_cosine_ops);

            -- Offboarding tenant 42 is a cheap, complete delete
            DROP TABLE chunks_t42;
        """,
        lang="sql",
        follow=[
            ("How would you move a tenant from the shared pool to its own partition without downtime?", "Downtime ছাড়া একটা tenant-কে shared pool থেকে নিজস্ব partition-এ কীভাবে সরাবে?"),
            ("How do you prove to an enterprise customer that their data is isolated?", "একজন enterprise customer-কে কীভাবে প্রমাণ করবে যে তাদের data আলাদা রাখা আছে?"),
        ],
        related=["vec-026", "vec-022", "vec-023"],
        refs=[OWASP_LLM08, PG_RLS, PGV],
    ),
]

if __name__ == "__main__":
    save("vectordb", "b3", QUESTIONS)
