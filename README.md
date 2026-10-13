# Interview Prep BD — Bilingual Technical Interview Platform (English + বাংলা)

An offline, browser-only interview-preparation app for developers in Bangladesh who also target international and remote roles. It has **584 bilingual questions across 18 technologies**, practice sessions with weighted scoring, auto-graded MCQs, mock interviews, flashcards, spaced review and progress tracking. It's built with HTML5, CSS3 and vanilla JavaScript, with no backend, build step or login.

## Run it

1. Keep the four files together in one folder: `index.html`, `styles.css`, `app.js`, `questions.js`.
2. Double-click `index.html`, or open it from any modern browser (Chrome/Edge/Firefox/Safari, 2023+). It works from `file://`, so no server is needed.
3. Optional: `interview-prep-bd-standalone.html` is the same app in a single file.

Fonts (Inter, Hind Siliguri, JetBrains Mono) load from Google Fonts when you're online. Offline, the app falls back to system fonts, including any installed Bangla font. Nothing else is fetched.

## What's implemented

- **Dashboard.** Shows real stats calculated from your data:
  - total, answered, correct/partial/incorrect, accuracy, weighted score, completion, bookmarks, needs-review and streak
  - today's goal, recent sessions, per-technology progress, difficulty distribution, weak topics and the daily challenge
  - a getting-started panel for new users
- **Technologies.** 18 cards with real counts per difficulty, completion, Start learning and Practice, plus search, sort and area filter.
- **All Questions.** Search in English or বাংলা, including tags and subtopics. Filter by technology, difficulty, type and market, and show only bookmarked, incorrect, unanswered, learned or needs-review questions. Sort by relevance, difficulty, priority or recently practised. Includes a live count, pagination, clear-all and an empty state.
- **Question detail.**
  - Metadata, version box, Learning mode (answer shown) and Interview mode (hidden until you reveal it, with no forced delay)
  - Code blocks with copy, expected output, explanation, common mistakes, interview tip, follow-ups and official docs
  - Bookmark, learned and review flags, which are independent of each other
  - Self-assessment, previous/next and related questions
- **Practice.**
  - Presets (Quick 10, Focus 20, Deep 30, Custom) or filters for technologies, difficulties, types and market. Choose random or priority-based order, pick a question pool (all, unanswered, answered or mistakes) and an optional timer.
  - Validates the setup. If fewer questions match, it offers the available number and never duplicates questions.
  - Reveal, self-assess (Correct/Partial/Incorrect/Skip), flag, bookmark and keyboard shortcuts.
  - The session survives reloads and language switches.
- **MCQs.** Graded automatically, with the correct answer and an explanation. An attempt is locked once scored, so it can't be scored twice.
- **Scoring.**
  - Points: Easy 1, Medium 2, Hard 3, Extreme 4. Correct earns 100%, partial 50%, incorrect 0%. Skipped earns 0% and is counted separately.
  - **Weighted score** = earned ÷ available × 100.
  - **Accuracy** = correct ÷ answered, excluding skips; shown as "—" when nothing is answered.
  - Revealing an answer is never penalised.
- **Results.** Score ring, points, accuracy, time, all four counts, per-technology and per-difficulty tables, questions to review, plus Review mistakes, Practice again and Dashboard. Every result is saved to history.
- **Interview simulation.** Choose the number of questions, technologies, difficulties, market, time limit and whether to include MCQs. Questions are ordered easy to hard and answers stay hidden. It auto-submits when time runs out.
- **Daily challenge.** Three questions picked deterministically from your local date (no server).
- **Flashcards.** Flip cards with bilingual answers, decks (all, not learned, bookmarked, due, mistakes), shuffle and keyboard control.
- **Bookmarks, Incorrect Answers, Review Questions.** Review Questions shows due spaced reviews, flagged items, the next 7 days and recently studied.
- **Spaced review.** A simple, transparent schedule, not an adaptive algorithm. Incorrect → tomorrow, partial → 3 days. Each later correct answer moves it to 7 → 14 → 30 days, after which it leaves the queue.
- **Weak-topic detection.** Miss rate = (incorrect + ½ partial) ÷ attempts, per subtopic and per difficulty, from your recorded answers only.
- **Study planner.** Daily target, a 7-day chart, an optional interview date with a suggested daily pace, and recommendations.
- **Study history.** A 16-week activity heatmap and a table of every session.
- **Settings.**
  - Language (English / বাংলা / Both), theme (dark/light), default question mode, motion (system/reduced/full), text size and sidebar.
  - **Export JSON** backup and **Import JSON**. Imports are validated and sanitised, and nothing is replaced until you confirm.
  - **Reset progress**, which requires typing `RESET`.
  - A data-health report.
- **Versions & Sources.** The verified version table, research sources and real counts.

### Storage

Progress lives in this browser's `localStorage` under the key `ipbd:state`. The data is versioned and has a migration path for older formats. Corrupted or incompatible data never crashes the app: it's backed up under a separate key and you're notified.

Progress doesn't sync between devices or browsers. Use Export/Import to move it. No account and no personal data are involved.

### Accessibility and responsiveness

- Semantic landmarks, a skip link and visible focus rings.
- ARIA on custom controls, a native `<dialog>` for modals and screen-reader live regions.
- Colour is never the only signal: difficulty has text plus pips, and results have text plus icons.
- Charts have text alternatives, `prefers-reduced-motion` is honoured, and there's a dark and a light theme.
- Layouts adapt to desktop, tablet and mobile (with a navigation drawer). Code blocks scroll horizontally.

## Question bank (counted from the actual records)

| Technology | Easy | Medium | Hard | Extreme | Total | MCQs |
|---|---:|---:|---:|---:|---:|---:|
| HTML | 11 | 11 | 7 | 3 | 32 | 8 |
| CSS | 11 | 11 | 7 | 3 | 32 | 7 |
| JavaScript | 14 | 14 | 8 | 4 | 40 | 10 |
| React | 11 | 11 | 7 | 3 | 32 | 8 |
| Next.js | 11 | 11 | 7 | 3 | 32 | 8 |
| Node.js | 11 | 11 | 7 | 3 | 32 | 7 |
| Express.js | 11 | 11 | 7 | 3 | 32 | 7 |
| NestJS | 11 | 11 | 7 | 3 | 32 | 8 |
| MongoDB | 11 | 11 | 7 | 3 | 32 | 8 |
| Mongoose | 11 | 11 | 7 | 3 | 32 | 8 |
| PostgreSQL | 11 | 11 | 7 | 3 | 32 | 7 |
| SQL | 11 | 11 | 7 | 3 | 32 | 7 |
| Drizzle ORM | 11 | 11 | 7 | 3 | 32 | 7 |
| Redis | 11 | 11 | 7 | 3 | 32 | 8 |
| Vector Databases | 11 | 11 | 7 | 3 | 32 | 8 |
| Docker | 11 | 11 | 7 | 3 | 32 | 8 |
| NGINX | 11 | 11 | 7 | 3 | 32 | 9 |
| AWS | 11 | 11 | 7 | 3 | 32 | 7 |
| **Total** | **201** | **201** | **127** | **55** | **584** | **140** |

The overall split is 34% easy, 34% medium, 22% hard and 9% extreme.

**By question type:** MCQ 140, conceptual 115, scenario 67, debugging 57, coding 46, comparison 44, security/performance 27, database query 25, architecture 23, output prediction 23, system design 17.

**By market:** both 457, Bangladesh 72, international 55.

**Other counts:**
- 201 questions are marked version-sensitive.
- 490 include code.
- There are 1,387 official-documentation references (853 unique URLs).

Every record has English and Bangla text for the question, answer, explanation, interview tip, follow-ups and MCQ options. Every record also carries `technologyVersion`, `verifiedAt`, `versionSensitive`, `status` and `documentationUrl`.

## Verified versions (checked 2026-10-12)

| Technology | Current stable used for content |
|---|---|
| HTML / CSS | HTML Living Standard; CSS Baseline status from web-features 3.42.0 (e.g. anchor positioning is **not** Baseline yet) |
| JavaScript | ECMAScript 2026 (approved 2026-06-30) |
| React | 19.3.0 (React Compiler 1.0) |
| Next.js | 16.4.0 (Cache Components recommended; `proxy.ts` replaces deprecated `middleware.ts`) |
| Node.js | 24.21.0 Active LTS · 26.11.1 Current (26 becomes LTS on 2026-10-28; annual releases from v27) |
| Express | 5.3.0 |
| NestJS | 12.1.3 |
| MongoDB | 9.0 (Node driver 7.7) |
| Mongoose | 9.11.1 |
| PostgreSQL | 18 (18.6); 19 is still in beta |
| Drizzle ORM | 0.45.4 stable (v1.0 is a release candidate → labelled *preview*) |
| Redis | Redis Open Source 8.10; node-redis 6.3, ioredis 6.0 |
| pgvector | 0.8.7 |
| Docker | Engine 29.9.0 · Compose v5.6.0 |
| NGINX | 1.30.5 stable · 1.31.6 mainline |
| AWS | Current services (Lambda `nodejs24.x` GA; Amazon Linux 2 end of support 2026-06-30) |

Versions came from the npm registry, nodejs.org, official release notes and docs. The full list of sources is on the in-app **Versions & Sources** page.

## How the content was produced and checked

1. **Research.** Versions came from official release notes, docs and the npm registry. Market context came from the Stack Overflow Developer Survey 2025, public Bangladesh interview reviews, a Bangladesh-focused JS interview article and a Bangladesh MERN/NestJS job post. Priority and market labels are editorial judgements, **not** frequency statistics.
2. **Writing.** Each category was written by a dedicated specialist pass with an automated validator. Code was executed wherever possible:
   - JS and Node outputs on Node 22, plus Node 24/26 binaries for ES2026 features
   - SQL on PostgreSQL 16 and SQLite, with PostgreSQL 18-only syntax checked against the PG18 docs and source
   - pgvector 0.8.x
   - Redis with node-redis 6.3
   - Express 5.3, NestJS 12.1 and Drizzle 0.45 packages
   - HTML/CSS behaviour in headless Chromium
3. **Independent review.** A second, independent technical review covered all 584 questions and made about 80 accuracy fixes. These included MCQ edge cases, CSS behaviour verified in Chromium, Node graceful-shutdown code, Next.js caching nuances, Mongoose 9 validator behaviour, Redis eviction advice, pgvector and EXPLAIN details, Compose v5 validation and AWS regional NAT gateways.

## Tests performed

An automated Playwright suite ran in Chromium against the real files over `file://`. **102 of 102 checks passed.** It covered:

- **Loading and navigation:** the app opens with no build step, the runtime validator reports 0 errors and 0 warnings, all 14 navigation links work, and there are no JS errors on any screen.
- **Search and filters:** English and Bangla search; combined filters match counts computed independently from the data; clear-all, sort, pagination and the empty state.
- **Question detail:** Learning vs Interview mode, reveal, independent bookmark/learned/review flags, and re-assessment that doesn't double count.
- **Persistence and language:** everything persists after reload; English, Bangla and Both modes; the language switch preserves an in-progress session.
- **Scoring:** a scripted session (correct, partial, incorrect, skip) gives exactly 1.5/4 points, 38% weighted and 33% accuracy.
- **Session behaviour:**
  - skips are recorded
  - ending early counts unanswered questions as skipped
  - MCQs can't be scored twice (re-click, keyboard, language switch, navigating back)
  - no-match and fewer-than-requested configurations are handled
  - timed sessions auto-submit
  - interview ordering and MCQ exclusion
  - the daily challenge, flashcards and keyboard shortcuts
- **Storage robustness:** corrupted JSON, an incompatible version and an unversioned legacy format are all handled without crashing; export downloads valid JSON; malformed and foreign imports are rejected with data unchanged; HTML in imported data is never rendered; reset needs typed confirmation and cancel keeps the data.
- **Planner, weak topics and theme:** the planner validates its input, weak topics are detected, and the theme persists.
- **Responsive layout:** no horizontal overflow at 390px and 768px across 16 routes in all three language modes; the mobile drawer opens and closes with Esc; touch targets are at least 30px.
- **Accessibility:** an axe-core WCAG 2 A/AA audit of 8 key screens in both the dark and light themes found no critical or serious violations, and reduced motion is honoured.

All 584 question pages were also rendered once each with zero errors.

## Limitations

- **Self-assessment.** Apart from MCQs, answers are self-assessed against the reference answer. The app doesn't (and can't reliably) grade free-form spoken or written answers.
- **Local-only storage.** Progress is per-browser and per-device, and clearing site data erases it, so export backups regularly.
- **Links.** 13 reference URLs across 13 documentation sites were re-checked at the end, and the writers and reviewers spot-checked many more. Not every one of the 853 unique URLs was individually fetched.
- **Language review.** The Bangla was written and reviewed for technical fidelity, but not proofread by a native-speaker editor.
- **Things that will date:** the content reflects versions as of **12 Oct 2026**. Known upcoming changes:
  - Node 26 becomes LTS on 2026-10-28.
  - Next.js 17 will make Cache Components the default.
  - Drizzle v1 will become stable.
  - Node's main branch has an unreleased change to the `keepAliveTimeout` default.

  Re-verify version-specific details before relying on them.
- **Optional fonts.** Google Fonts is the only network request, and it's optional.

## Extending the question bank

The `source/` folder in the zip contains the authoring pipeline:

- `data/src/<tech>_bN.py`: question sources, written as raw strings, with one `Q(...)` per question.
- `tools/qb.py` (helpers), `tools/check.py` (validator), `tools/build_bank.py` (writes `questions.js`), `tools/build_app.sh` (concatenates `app/src/*.js` into `app/app.js`).
- `docs/AUTHORING.md`, `docs/FACTS.md`, `docs/COVERAGE.md`, `docs/REVIEW.md`: the writing rules, the verified facts, the coverage plan and the review checklist.
- `tests/e2e.mjs`: the Playwright suite. It needs `playwright` and `axe-core`; adjust the `APP` path at the top of the file.

To add a question, add a `Q(...)` entry, then run `python3 data/src/<file>.py`, `python3 tools/check.py <tech>` and `python3 tools/build_bank.py` (it writes `app/questions.js`; copy it next to `index.html`).
