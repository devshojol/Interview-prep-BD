"""
check.py — validate question JSON produced by qb.save().

    python3 tools/check.py javascript          # one technology
    python3 tools/check.py javascript react    # several
    python3 tools/check.py --all               # everything (global ID / related checks)

Exit code 1 if any ERROR is found. WARNINGS should be reviewed and fixed where reasonable.
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qb import TECHS, DIFFS, TYPES, MARKETS, PRIORITIES, STATUSES, JSON_DIR, SHORT_TYPES  # noqa: E402

BN_RE = re.compile(r"[ঀ-৿]")
LATIN_RE = re.compile(r"[A-Za-z]")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
FENCE_RE = re.compile(r"```.*?```", re.S)
ID_RE = re.compile(r"^[a-z0-9]+-[a-z0-9-]+$")

TARGET = {"javascript": 40, "reactnative": 40}
DEFAULT_TARGET = 32
QUICK_TARGET = 10          # quick-recall questions per technology
NON_TECH = {"behavioral"}  # categories without the technical difficulty/type targets
SENTENCE_RE = re.compile(r"[.!?।](?:\s|$)")
OFFICIAL_HINTS = [
    "developer.mozilla.org", "html.spec.whatwg.org", "w3.org", "web.dev", "tc39.es", "ecma-international.org",
    "react.dev", "nextjs.org", "nodejs.org", "expressjs.com", "docs.nestjs.com", "nestjs.com",
    "mongodb.com", "mongoosejs.com", "postgresql.org", "orm.drizzle.team", "redis.io", "github.com/pgvector",
    "docs.docker.com", "nginx.org", "docs.nginx.com", "aws.amazon.com", "docs.aws.amazon.com",
    "typescriptlang.org", "owasp.org", "cheatsheetseries.owasp.org", "datatracker.ietf.org", "rfc-editor.org",
    "v8.dev", "libuv.org", "github.com", "npmjs.com", "kubernetes.io", "wikipedia.org", "sqlite.org",
    "learn.microsoft.com", "iso.org", "valkey.io", "huggingface.co", "platform.openai.com", "pinecone.io",
    "qdrant.tech", "weaviate.io", "milvus.io", "faiss.ai", "arxiv.org", "martin.kleppmann.com",
    "fastify.dev", "jwt.io", "jestjs.io", "vitest.dev", "zod.dev", "socket.io", "webassembly.org",
    "reactnative.dev", "expo.dev", "reactnavigation.org", "swmansion.com", "callstack.github.io", "callstack.com",
    "developer.android.com", "developer.apple.com", "firebase.google.com", "tanstack.com", "maestro.dev",
    "mobile.dev", "wix.github.io", "shopify.github.io", "zustand.docs.pmnd.rs", "redux-toolkit.js.org",
]


def strip_code(s):
    return INLINE_CODE_RE.sub(" ", FENCE_RE.sub(" ", s or ""))


def bn_ratio(s):
    t = strip_code(s)
    b = len(BN_RE.findall(t))
    l = len(LATIN_RE.findall(t))
    return b / max(1, (b + l)), b


def load(techs):
    data = {}
    for t in techs:
        qs = []
        for path in sorted(glob.glob(os.path.join(JSON_DIR, f"{t}.*.json"))):
            with open(path, encoding="utf-8") as f:
                try:
                    arr = json.load(f)
                except Exception as e:  # pragma: no cover
                    print(f"ERROR {path}: invalid JSON: {e}")
                    continue
            for q in arr:
                q["_file"] = os.path.basename(path)
            qs.extend(arr)
        data[t] = qs
    return data


def words(s):
    return set(re.findall(r"[a-z0-9]+", (s or "").lower())) - {"the", "a", "an", "of", "in", "and", "to", "is", "what", "how", "you", "would", "your", "for", "with", "on", "does", "do", "it", "are", "why", "between", "difference"}


def check_question(q, errors, warns):
    qid = q.get("id", "<no id>")
    E = lambda m: errors.append(f"{qid}: {m}")  # noqa: E731
    W = lambda m: warns.append(f"{qid}: {m}")  # noqa: E731

    if not ID_RE.match(str(q.get("id", ""))):
        E("id must match ^[a-z0-9]+-[a-z0-9-]+$")
    for k, allowed in [("difficulty", DIFFS), ("type", TYPES), ("market", MARKETS), ("priority", PRIORITIES), ("status", STATUSES)]:
        if q.get(k) not in allowed:
            E(f"{k}='{q.get(k)}' not in {allowed}")
    if not q.get("subtopic"):
        E("missing subtopic")
    m = q.get("estimatedMinutes")
    if not isinstance(m, int) or not (1 <= m <= 60):
        E("estimatedMinutes must be int 1..60")
    if not q.get("tags"):
        E("tags required")
    if not q.get("technologyVersion"):
        E("technologyVersion required")
    if not isinstance(q.get("versionSensitive"), bool):
        E("versionSensitive must be bool")
    if q.get("versionSensitive") and not re.search(r"\d", q.get("technologyVersion", "")):
        E("versionSensitive=True but technologyVersion has no version number")

    for field in ["question", "answer", "explanation", "interviewTip"]:
        obj = q.get(field) or {}
        en, bn = obj.get("en"), obj.get("bn")
        if not en:
            E(f"{field}.en missing")
        if not bn:
            E(f"{field}.bn missing")
            continue
        r, b = bn_ratio(bn)
        if field == "question":
            if b < 2:
                E(f"{field}.bn has no Bangla text")
        elif r < 0.2:
            E(f"{field}.bn looks untranslated (Bangla ratio {r:.2f})")
        if en:
            r2, _ = bn_ratio(en)
            if r2 > 0.05:
                E(f"{field}.en contains Bangla text")
    t = q.get("type")
    qa = q.get("quickAnswer")
    if t in SHORT_TYPES:
        if qa:
            E(f"type '{t}' must not have quickAnswer (its answer is already the short answer)")
        a_en = (q.get("answer") or {}).get("en") or ""
        if len(strip_code(a_en)) > 450:
            W(f"type '{t}' answer.en is long ({len(a_en)} chars); keep it to 1-3 plain sentences")
        if t == "quick" and q.get("difficulty") not in ("easy", "medium"):
            E("quick-recall questions must be easy or medium")
    else:
        if not qa:
            E("quickAnswer (quick_en/quick_bn) required")
        else:
            qen, qbn = qa.get("en") or "", qa.get("bn") or ""
            if not qen or not qbn:
                E("quickAnswer needs en+bn")
            else:
                if bn_ratio(qen)[0] > 0.05:
                    E("quickAnswer.en contains Bangla text")
                if bn_ratio(qbn)[0] < 0.2:
                    E("quickAnswer.bn looks untranslated")
                if "\n" in qen.strip():
                    E("quickAnswer must be a single paragraph")
                if len(qen) > 340:
                    W(f"quickAnswer.en is long ({len(qen)} chars); aim for 1-3 sentences under ~300 chars")
                if len(SENTENCE_RE.findall(strip_code(qen) + " ")) > 3:
                    W("quickAnswer.en has more than 3 sentences")
    if q.get("commonMistakes"):
        cm = q["commonMistakes"]
        if not cm.get("en") or not cm.get("bn"):
            E("commonMistakes needs en+bn")
        elif bn_ratio(cm["bn"])[0] < 0.2:
            E("commonMistakes.bn looks untranslated")

    ans_len = len((q.get("answer") or {}).get("en") or "")
    if ans_len < 60:
        W(f"answer.en very short ({ans_len} chars)")

    refs = q.get("references") or []
    if not refs:
        (W if q.get("technology") in NON_TECH else E)("at least one reference required")
    for r in refs:
        u = r.get("url", "")
        if not u.startswith("https://"):
            E(f"reference url must be https: {u}")
        if not r.get("title"):
            E("reference title missing")
        if not any(h in u for h in OFFICIAL_HINTS):
            W(f"reference not on a known official domain: {u}")

    for i, f in enumerate(q.get("followUps") or []):
        if not f.get("en") or not f.get("bn") or not BN_RE.search(f.get("bn", "")):
            E(f"followUps[{i}] needs en + Bangla bn")
    if q.get("type") != "mcq" and not q.get("followUps"):
        W("no followUps")

    if t == "mcq":
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) != 4:
            E("mcq needs exactly 4 options")
        else:
            for i, o in enumerate(opts):
                if not o.get("en") or not o.get("bn"):
                    E(f"option {i} needs en+bn")
            ens = [o.get("en", "").strip().lower() for o in opts]
            if len(set(ens)) != 4:
                E("mcq options must be distinct")
        ci = q.get("correctIndex")
        if not isinstance(ci, int) or not (0 <= ci <= 3):
            E("mcq correctIndex must be int 0..3")
    else:
        if "options" in q:
            E("options only allowed on type='mcq'")
    code = q.get("code")
    if code is not None:
        if not isinstance(code, dict) or "source" not in code:
            E("code must be {language, source, output?}")
    if t == "output":
        if not code or not code.get("source") or not code.get("output"):
            E("type 'output' requires code.source and code.output")
    if t == "coding":
        if not code or not code.get("source"):
            E("type 'coding' requires a reference solution in code")
        if not q.get("complexity"):
            W("coding question without time/space complexity")
    if t == "query" and not code:
        W("query question without code (query)")
    if t == "debugging" and not code:
        W("debugging question without code")


def main(argv):
    techs = TECHS if (not argv or argv == ["--all"]) else argv
    for t in techs:
        if t not in TECHS:
            sys.exit(f"unknown technology {t}")
    data = load(techs)
    errors, warns = [], []
    all_ids = Counter()
    for t, qs in data.items():
        for q in qs:
            all_ids[q.get("id")] += 1
    # include ids from other techs for related checks
    every = load(TECHS) if techs != TECHS else data
    known = {q.get("id") for qs in every.values() for q in qs}

    for t, qs in data.items():
        print(f"\n=== {t}: {len(qs)} questions ===")
        if not qs:
            continue
        for q in qs:
            if q.get("technology") != t:
                errors.append(f"{q.get('id')}: technology field '{q.get('technology')}' != {t}")
            check_question(q, errors, warns)
            for rid in q.get("related") or []:
                if rid not in known:
                    errors.append(f"{q.get('id')}: related id '{rid}' does not exist")
        for qid, n in all_ids.items():
            if n > 1 and any(q.get("id") == qid for q in qs):
                errors.append(f"{qid}: duplicate id ({n} times)")
        # near-duplicate questions
        seen = []
        for q in qs:
            w = words((q.get("question") or {}).get("en"))
            for (oid, ow) in seen:
                if w and ow:
                    j = len(w & ow) / len(w | ow)
                    if j >= 0.85:
                        warns.append(f"{q.get('id')}: question very similar to {oid} (jaccard {j:.2f})")
            seen.append((q.get("id"), w))
        main = [q for q in qs if q.get("type") not in SHORT_TYPES]
        quick = [q for q in qs if q.get("type") == "quick"]
        ty = Counter(q.get("type") for q in qs)
        mk = Counter(q.get("market") for q in qs)
        print("types     :", dict(ty))
        print("market    :", dict(mk))
        if t in NON_TECH:
            print(f"{len(qs)} questions (no difficulty/type targets for this category)")
            continue
        print(f"quick-recall: {len(quick)} (target {QUICK_TARGET})")
        if len(quick) < QUICK_TARGET:
            warns.append(f"[{t}] only {len(quick)} quick-recall questions (target {QUICK_TARGET})")
        d = Counter(q.get("difficulty") for q in main)
        n = len(main)
        target = TARGET.get(t, DEFAULT_TARGET)
        print("difficulty:", {k: d.get(k, 0) for k in DIFFS}, f"(main bank; target total >= {target})")
        subs = Counter(q.get("subtopic") for q in qs)
        print("subtopics :", len(subs), "distinct")
        if n < target:
            warns.append(f"[{t}] only {n} questions (target {target})")
        for k, pct in [("easy", .35), ("medium", .35), ("hard", .20), ("extreme", .10)]:
            share = d.get(k, 0) / n
            if abs(share - pct) > 0.10:
                warns.append(f"[{t}] {k} share {share:.0%} far from target {pct:.0%}")
            if d.get(k, 0) == 0:
                errors.append(f"[{t}] no '{k}' questions")
        if ty.get("mcq", 0) < 6 and n >= 24:
            warns.append(f"[{t}] only {ty.get('mcq', 0)} MCQs (aim for 7-10)")

    print("\n--- WARNINGS ({}) ---".format(len(warns)))
    for w in warns:
        print("WARN ", w)
    print("\n--- ERRORS ({}) ---".format(len(errors)))
    for e in errors:
        print("ERROR", e)
    if errors:
        sys.exit(1)
    print("\nOK — no errors.")


if __name__ == "__main__":
    main(sys.argv[1:])
