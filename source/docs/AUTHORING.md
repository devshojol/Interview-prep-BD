# Authoring Guide — Bilingual Technical Interview Question Bank

You are writing part of a question bank for an offline HTML/JS interview-prep app for software developers in
**Bangladesh** who also target **international / remote** roles. The app shows every question in English,
Bangla (বাংলা), or both side by side. Quality and technical accuracy matter more than anything else.

Read these first:
- `docs/FACTS.md` — verified versions (2026-10-12) and version-sensitive facts. **Source of truth.**
- `docs/COVERAGE.md` — the subtopics each category must cover.
- `docs/example_batch.py` — the exact file format (copy its pattern).

## 1. Workflow

1. Plan your category: list ~32 questions (JavaScript: 40) mapped to the subtopics in COVERAGE.md before writing.
   Spread difficulty and types (targets below). No two questions should test the same thing.
2. Write questions in batch files of **6–8 questions each**: `data/src/<tech>_b1.py`, `<tech>_b2.py`, …
   Each file ends with `save("<tech>", "b1", QUESTIONS)`.
3. After every batch: `python3 data/src/<tech>_bN.py && python3 tools/check.py <tech>` — fix every ERROR.
   WARNINGs about totals/distribution are expected until all batches exist; fix the rest.
4. At the end, `python3 tools/check.py <tech>` must print `OK — no errors.` and the distribution must be on target.
5. Only touch files for your own technologies. Never edit tools/ or docs/.

Tech ids: html, css, javascript, react, nextjs, nodejs, express, nestjs, mongodb, mongoose, postgresql, sql,
drizzle, redis, vectordb, docker, nginx, aws. Question id prefixes: `html-`, `css-`, `js-`, `react-`, `next-`,
`node-`, `express-`, `nest-`, `mongo-`, `mongoose-`, `pg-`, `sql-`, `drizzle-`, `redis-`, `vec-`, `docker-`,
`nginx-`, `aws-` followed by a 3-digit number (e.g. `js-017`). IDs must be unique.

## 2. Python string rules (important)

- Use raw triple-quoted strings `r"""..."""` for **every** text and code field. Then you never need to escape
  backticks, quotes, `${}`, or backslashes. Don't put `"""` inside a field, and don't end a raw string with `\`.
- Indentation inside the triple quotes is removed automatically (dedent), so indent naturally.

## 3. Fields (see `Q()` in tools/qb.py)

| kwarg | meaning |
|---|---|
| `id` | e.g. `"react-012"` |
| `sub` | subtopic (from COVERAGE.md, Title Case) |
| `diff` | `easy` / `medium` / `hard` / `extreme` |
| `type` | `conceptual`, `output` (code output prediction), `coding`, `debugging`, `scenario`, `comparison`, `system-design`, `query` (DB query), `architecture`, `security-performance`, `mcq` |
| `prio` | `high` / `medium` / `low` — importance for the target role (judgement, not statistics) |
| `market` | `both` (default), `bangladesh`, `international` — see FACTS.md research notes; justify non-`both` |
| `mins` | estimated minutes to answer aloud (1–15 typical; extreme up to 25) |
| `tags` | 2–6 lowercase tags |
| `ver` | e.g. `"React 19.3"`, `"Next.js 16.4 (App Router)"`, `"Node.js 24 LTS / 26"`, `"Express 5.x"`, or `"Version-independent concept"` |
| `vs` | `True` if the answer depends on a version (then `ver` must contain a number) |
| `status` | `stable` (default), `legacy`, `deprecated`, `experimental`, `preview`, `version-specific` — status of the *feature being taught* |
| `q_en`, `q_bn` | the question |
| `a_en`, `a_bn` | the interview-ready answer (what a strong candidate would say) |
| `ex_en`, `ex_bn` | deeper explanation: why it works, caveats, trade-offs, edge cases |
| `tip_en`, `tip_bn` | interview tip: how to structure/deliver the answer, what impresses |
| `mist_en`, `mist_bn` | optional: common mistakes/misconceptions (recommended for most questions) |
| `code`, `lang`, `output` | main code block (`lang`: javascript, typescript, jsx, tsx, html, css, sql, json, bash, dockerfile, yaml, nginx, python, text); `output` = expected output |
| `setup`, `setup_lang` | for SQL/DB questions: schema + sample data shown before the query |
| `extra` | list of extra code blocks: `[dict(lang="jsx", src=r"""...""", label_en="Fixed version", label_bn="সংশোধিত version")]` |
| `follow` | 1–3 follow-up questions an interviewer might ask: `[(en, bn), ...]` |
| `related` | optional list of other question ids **that exist** (usually in your own category) |
| `options`, `correct` | MCQ only: exactly 4 `(en, bn)` options and the 0-based index of the single correct one |
| `time`, `space` | for coding questions: complexity like `"O(n)"` |
| `refs` | 1–3 `(title, url)` official documentation links (see §8) |

### How the app displays code (write accordingly!)
- `type="output"`, `type="debugging"`, and any `mcq` that has `code`: the `code.source` is shown **together with
  the question** (the learner must see it to answer). `output` (expected output) and `extra` blocks (e.g. the
  fixed version) are hidden until the answer is revealed. So never put the answer inside `code.source` comments
  for these types (e.g. no `// prints 3` hints in an output question).
- `type="coding"`: `code` is the **reference solution**, hidden until reveal. Put the problem statement, input
  and expected output examples in `q_en`/`q_bn`.
- `type="query"`: `setup` (schema + sample rows) is shown with the question; `code` (the query) and `output`
  (expected result) are hidden until reveal.
- All other types: `code` is an illustrative example shown inside the revealed answer.

### Text formatting (the app renders this safely; no HTML allowed)
- Blank line = new paragraph. Lines starting with `- ` = bullet list; `1. ` = numbered list.
- Inline code with backticks: `` `useEffect` ``. Bold with `**text**`.
- Avoid fenced code blocks inside prose; put code in `code` / `extra` (shown once for both languages).
- Never translate code, identifiers, API names, CLI commands, SQL keywords or product names.

## 4. Difficulty targets per category (32 questions; JavaScript 40)

| level | share | 32-question category | JavaScript (40) | audience / focus |
|---|---|---|---|---|
| easy | ~35% | 11 | 14 | juniors: definitions, fundamentals, syntax, basic debugging |
| medium | ~35% | 11 | 14 | junior→mid: practical implementation, real-world use, trade-offs, combining concepts |
| hard | ~20% | 7 | 8 | mid→senior: internals, complex debugging, architecture, performance, security |
| extreme | ~10% | 3 | 4 | senior: hard architecture decisions, concurrency, distributed systems, incidents, scale |

Extreme questions must be genuinely relevant (real production/architecture problems), not trivia. Write the
English answer for extreme questions so it notes it's advanced material where appropriate.

## 5. Question type mix per category (guideline)

- **7–9 MCQs** (JavaScript 10) spread across difficulties, each with 4 plausible options (no silly distractors,
  exactly one correct answer). The MCQ `ex_*` must explain why the correct option is right AND why the most
  tempting wrong option is wrong.
- The rest: conceptual, comparison, scenario, debugging, coding/query, output (JS/React/Node especially),
  security-performance, architecture/system-design (mostly hard/extreme). Every category needs at least:
  3 conceptual, 2 scenario, 2 debugging *or* coding/query, 1 comparison, 1 security-performance,
  1 architecture or system-design.
- **Output questions:** code + exact expected output + step-by-step reasoning in `ex_*`.
- **Coding questions:** problem statement in `q_*` (with expected behaviour & example), reference solution in
  `code`, explanation + edge cases + common mistakes, `time`/`space` complexity.
- **SQL / DB query questions:** schema & sample rows in `setup`, query in `code`, expected result table in
  `output` (plain text table), explain joins/grouping/window logic.
- **Scenario questions:** structured approach: clarify assumptions → options → trade-offs → recommendation.
- **System design / architecture:** requirements, constraints, components, data flow, trade-offs, failure
  scenarios, security & scaling (bullets keep it readable).
- **Debugging:** buggy code in `code`, fixed code in `extra`, explain root cause.

## 6. Writing style

**English:** natural, conversational technical English — like an experienced developer answering an
interviewer. Direct answer first, then explanation, example, caveats, real-world relevance. No robotic
textbook tone. Length scales with difficulty: easy answers ~60–120 words; medium ~100–180; hard/extreme
~150–300 (bullets welcome). Explanation adds depth; don't just repeat the answer.

**Bangla:** natural, technically accurate Bangla for Bangladeshi developers — NOT word-for-word translation.
Keep technical terms in English (Latin script) with Bangla suffixes joined by a hyphen, e.g. `component-এর`,
`API-তে`, `JavaScript-এ`, `cache করা`, `request পাঠানো`. Do not transliterate tech terms into Bangla script
(write "component", not "কম্পোনেন্ট"). Use তুমি-form in tips ("ব্যাখ্যা করো", "উল্লেখ করো"). Answers can be
first-person ("আমি সাধারণত ... ব্যবহার করি"). Keep the same technical content as the English version.

Benchmark (match this quality, don't copy the template rigidly) — see `docs/example_batch.py`.

## 7. Accuracy & version rules (mandatory)

- Everything must match the **current stable** versions in FACTS.md (React 19.3, Next.js 16.4, Node 24 LTS /
  26 Current, Express 5.3, NestJS 12.1, MongoDB 9.0, Mongoose 9.11, PostgreSQL 18, Drizzle 0.45 stable,
  Redis 8.10, Docker Engine 29 / Compose v5, NGINX 1.30 stable / 1.31 mainline, ECMAScript 2026...).
- Never present deprecated/removed APIs as current. When an older approach matters (maintaining legacy apps or
  common interview questions — e.g. class lifecycle methods, Pages Router, `middleware.ts`, Express 4 wildcard
  syntax, Mongoose callbacks, `docker-compose` v1), label it clearly (status `legacy`/`version-specific` or say
  "legacy" in the text) and give the current approach.
- Don't mix incompatible APIs from different versions in one example.
- Mark experimental/preview features (e.g. Drizzle v1 RC, Temporal, CSS anchor positioning not Baseline,
  `node:sqlite` unless verified) as such.
- If you're not sure a claim is true for the current version, check the official docs with WebFetch (keep it to
  a handful of targeted checks), or rephrase so it's version-independent. Never invent API behaviour.
- Don't claim statistics about how often a question is asked.

## 8. References

1–3 per question, official documentation only (MDN, react.dev, nextjs.org/docs, nodejs.org/api,
expressjs.com, docs.nestjs.com, mongodb.com/docs, mongoosejs.com/docs, postgresql.org/docs/current,
orm.drizzle.team/docs, redis.io/docs, github.com/pgvector/pgvector, docs.docker.com, nginx.org/en/docs,
docs.aws.amazon.com, owasp.org / cheatsheetseries.owasp.org, tc39.es, html.spec.whatwg.org, web.dev).
Use URLs you are confident exist (prefer stable, top-level API/guide pages over deep anchors). If unsure,
verify with WebFetch or use the parent docs page. Never fabricate a URL.

Useful known-good roots: `https://react.dev/reference/react/useEffect`, `https://nextjs.org/docs/app`,
`https://nodejs.org/api/events.html`, `https://expressjs.com/en/guide/error-handling.html`,
`https://expressjs.com/en/guide/migrating-5.html`, `https://docs.nestjs.com/guards`,
`https://www.mongodb.com/docs/manual/aggregation/`, `https://mongoosejs.com/docs/middleware.html`,
`https://www.postgresql.org/docs/current/mvcc.html`, `https://orm.drizzle.team/docs/overview`,
`https://redis.io/docs/latest/develop/data-types/`, `https://docs.docker.com/build/building/multi-stage/`,
`https://nginx.org/en/docs/http/ngx_http_proxy_module.html`,
`https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html`.

## 9. Final self-review before you finish

- [ ] `python3 tools/check.py <tech>` → `OK — no errors.`; difficulty distribution on target.
- [ ] All COVERAGE.md subtopics for the category addressed (several may be combined in one question).
- [ ] No duplicated knowledge; varied types; 7–9 MCQs with a single correct answer each.
- [ ] Version-sensitive answers match FACTS.md; legacy approaches labelled.
- [ ] Bangla reads naturally and matches the English content.
- [ ] Code examples are correct and runnable for the stated version; outputs are exact.

Report back: per-category counts (by difficulty and type), the subtopics covered, any claims you verified
online (URL), and anything you were unsure about.
