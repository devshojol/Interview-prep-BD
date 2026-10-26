"""
qb.py — helper for authoring bilingual interview questions.

Usage inside a batch file (e.g. data/src/javascript_b1.py):

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
    from qb import Q, save

    QUESTIONS = [
        Q(id="js-001", sub="Scope", diff="easy", type="conceptual", ...),
        ...
    ]
    save("javascript", "b1", QUESTIONS)

Run it with:  python3 data/src/javascript_b1.py
Then validate: python3 tools/check.py javascript
"""
import json
import os
import re
import sys
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "data", "json")
VERIFIED_AT = "2026-10-12"

TECHS = [
    "html", "css", "javascript", "react", "nextjs", "reactnative", "nodejs", "express", "nestjs",
    "mongodb", "mongoose", "postgresql", "sql", "drizzle", "redis", "vectordb",
    "docker", "nginx", "aws", "behavioral",
]
DIFFS = ["easy", "medium", "hard", "extreme"]
TYPES = [
    "conceptual", "output", "coding", "debugging", "scenario", "comparison",
    "system-design", "query", "architecture", "security-performance", "mcq",
    "quick", "behavioral",
]
# Types that are short-format by design: they are left out of the per-category difficulty and
# type-mix targets, and their `answer` is already the short answer (no separate quickAnswer).
SHORT_TYPES = ["quick", "behavioral"]
MARKETS = ["both", "bangladesh", "international"]
PRIORITIES = ["high", "medium", "low"]
STATUSES = ["stable", "legacy", "deprecated", "experimental", "preview", "version-specific"]


def _text(s):
    """Normalise prose: dedent, strip outer blank lines, collapse trailing spaces."""
    if s is None:
        return None
    s = textwrap.dedent(s).strip("\n")
    lines = [ln.rstrip() for ln in s.split("\n")]
    # dedent again in case first line had no indent but others did
    s = "\n".join(lines).strip()
    return s


def _code(s):
    """Normalise a code block: dedent, strip leading/trailing blank lines, keep inner indentation."""
    if s is None:
        return None
    s = textwrap.dedent(s)
    lines = s.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(ln.rstrip() for ln in lines)


def _bi(en, bn):
    return {"en": _text(en), "bn": _text(bn)}


def Q(
    id, sub, diff, type,
    q_en, q_bn, a_en, a_bn, ex_en, ex_bn, tip_en, tip_bn,
    refs, tags, ver,
    prio="medium", market="both", mins=3, vs=False, status="stable",
    code=None, lang=None, output=None,
    setup=None, setup_lang="sql",
    extra=None,
    mist_en=None, mist_bn=None,
    follow=None, related=None,
    options=None, correct=None,
    time=None, space=None,
    quick_en=None, quick_bn=None,
):
    """Build one question record.

    refs:    list of (title, url)
    follow:  list of (en, bn) follow-up questions an interviewer may ask
    options: list of 4 (en, bn) tuples (MCQ only); correct = index 0..3
    extra:   list of dicts {lang, src, label_en, label_bn} for additional code blocks
    quick_*: the 1-3 sentence "quick answer" shown above the full answer (not used for
             type="quick" / "behavioral", whose `a_*` is already short)
    """
    rec = {
        "id": id,
        "subtopic": sub,
        "difficulty": diff,
        "type": type,
        "market": market,
        "priority": prio,
        "estimatedMinutes": mins,
        "tags": list(tags or []),
        "technologyVersion": ver,
        "verifiedAt": VERIFIED_AT,
        "versionSensitive": bool(vs),
        "status": status,
        "question": _bi(q_en, q_bn),
        "answer": _bi(a_en, a_bn),
        "explanation": _bi(ex_en, ex_bn),
        "interviewTip": _bi(tip_en, tip_bn),
        "references": [{"title": t, "url": u} for (t, u) in (refs or [])],
        "followUps": [_bi(e, b) for (e, b) in (follow or [])],
        "related": list(related or []),
    }
    if quick_en or quick_bn:
        rec["quickAnswer"] = _bi(quick_en, quick_bn)
    if mist_en or mist_bn:
        rec["commonMistakes"] = _bi(mist_en, mist_bn)
    if code is not None:
        rec["code"] = {"language": lang or "text", "source": _code(code)}
        if output is not None:
            rec["code"]["output"] = _code(output)
    elif output is not None:
        rec["code"] = {"language": "text", "source": "", "output": _code(output)}
    if setup is not None:
        rec["setup"] = {"language": setup_lang or "sql", "source": _code(setup)}
    if extra:
        rec["extraCode"] = [
            {
                "language": x.get("lang", "text"),
                "source": _code(x.get("src", "")),
                "label": _bi(x.get("label_en", ""), x.get("label_bn", "")),
            }
            for x in extra
        ]
    if options is not None:
        rec["options"] = [_bi(e, b) for (e, b) in options]
        rec["correctIndex"] = correct
    if time or space:
        rec["complexity"] = {"time": time or "", "space": space or ""}
    return rec


def save(tech, batch, questions):
    if tech not in TECHS:
        sys.exit(f"Unknown technology '{tech}'. Use one of: {TECHS}")
    os.makedirs(JSON_DIR, exist_ok=True)
    for q in questions:
        q["technology"] = tech
    path = os.path.join(JSON_DIR, f"{tech}.{batch}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=1)
    print(f"Saved {len(questions)} questions -> {os.path.relpath(path, ROOT)}")
