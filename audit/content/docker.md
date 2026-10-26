# Docker content audit
Coverage: 32 of 32 questions reviewed. IDs: docker-001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 025, 026, 027, 028, 029, 030, 031, 032.

## Category summary
The Docker set is strong: technically precise, built around production scenarios, and nearly every answer explains the mechanism (namespaces/cgroups, copy-on-write, cache invalidation, PID 1 signal semantics, interpolation vs container env, cache mounts vs layer cache). Debugging questions (005, 010, 012, 014, 020, 024, 027) are realistic and symptom-driven, and the code (Dockerfiles, compose files, scripts) is idiomatic and current (no `version:`, `condition: service_healthy`, secret mounts, PG18 volume path, `HOSTNAME=0.0.0.0` for Next standalone). The MCQs each have exactly one defensible key, plausible distractors, and explanations that refer to options by content rather than letter, so they survive shuffling. I found no P0/P1 errors. The issues are a misleading restart-policy detail (019), a broken rollback step in the blue/green design (031), one display leak (027), small internal inconsistencies (028), and recurring filler in the tips ("interviewers love…"). The Bangla is natural, contemporary developer Bangla with tech terms in Latin script, and it matches the EN closely. Versions are internally consistent with FACTS (Engine 29, Compose v5, NGINX 1.30, PG18, Redis 8). The one currency note is that `node:24-*` and "Node.js 24 LTS" appear everywhere, and Node 24 is now in Maintenance LTS, with Node 26 becoming Active LTS on 2026-10-28. Coverage of COVERAGE.md subtopics is complete, and the difficulty progression is sensible: 11 easy, 11 medium, 7 hard, 3 extreme. Some themes overlap (localhost-in-container, 137/OOM, hardening), but each angle is distinct.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 8 | English quality 9 | Examples & code 9 | Originality/information value 8 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| DOCKER-C01 | docker-031 | both | P2 | Technical correctness | The rollback step is inconsistent with the deploy flow. The script `docker stop`s the old slot, but rollback is described as only switching the NGINX include back. That would point NGINX at a stopped container and cause 502s. | "`docker stop -t 30` the old slot so it drains → keep its image for instant rollback" … "**Rollback:** switch the include back and reload. That takes seconds and needs no rebuild." | Either keep the old slot running (idle) for a soak period and then stop it, or say that rollback = `docker start api_<old>` → wait for healthy → switch include → reload. | High | The rollback text names a step that (re)starts and health-gates the old container, or the script delays `docker stop` of the old slot. |
| DOCKER-C02 | docker-031 | both | P3 | Code consistency | The deploy script's health check uses `wget`, but docker-018 explains that slim/distroless Node images have no curl/wget. | `--health-cmd "wget -qO- http://127.0.0.1:3000/ready \|\| exit 1"` vs docker-018 "`node:24-slim` has neither `curl` nor `wget`" | Use the `node -e "fetch(...)"` probe from docker-018, or note that the image must include wget (alpine). | High | The script's health command works on the image types the set recommends. |
| DOCKER-C03 | docker-019 | both | P2 | Misleading detail | The 10-second rule is misexplained. Containers that exit immediately are still restarted. The 10 s marks a "successful start" (it resets the back-off delay). Tight loops are prevented by the exponential back-off (100 ms doubling), not by the 10 s rule. | "A restart policy only takes effect after the container has stayed up for at least 10 seconds, which prevents tight restart loops on boot failures." | Rephrase: "Docker restarts with an increasing delay (starting at 100 ms, doubling); the delay resets once the container has run ~10 s. A container failing at boot shows `Restarting (1)` with growing gaps." Mirror in BN. | Medium | The text no longer implies that fast-failing containers aren't restarted. Check against the docs page "Start containers automatically". |
| DOCKER-C04 | docker-027 | both | P3 | Display leak | The shown code includes the daemon warning that names both platforms, which gives away the "hard" debugging answer before the learner reasons about it. | "# WARNING: The requested image's platform (linux/arm64/v8) does not match the detected host platform (linux/amd64/v3)" | Keep only `exec format error` in the shown code, and move the platform warning into the answer as confirming evidence. | High | The shown code no longer contains "arm64"/"amd64" text. |
| DOCKER-C05 | docker-028 | both | P3 | Internal inconsistency | The answer says every service gets a healthcheck and that Redis gets an eviction policy, but the code gives worker/redis no healthcheck and sets `noeviction` (i.e. no eviction). | "a `healthcheck` for each service" … "Redis gets `maxmemory` plus an eviction policy" vs code `--maxmemory-policy noeviction` | Add healthchecks to worker/redis (e.g. `redis-cli ping`), and say "a `maxmemory` limit and an explicit policy (`noeviction` for a queue: writes fail instead of losing jobs)". | High | Code and prose agree. |
| DOCKER-C06 | docker-014 | both | P3 | Nuance / accuracy | The explanation is sound for `sh` as PID 1, but it doesn't mention that recent npm forwards SIGTERM/SIGINT to its child. If the shell `exec`s npm (dash/BusyBox can), the handler may run. The robust reason to avoid npm remains the extra process layer and its signal/exit-code handling. | "The shell doesn't forward it, so Node never receives it" ; "Some shells happen to `exec` a single simple command" | Add one line: "Even when npm ends up as PID 1, behaviour depends on npm version; run Node directly so signal delivery is deterministic." | Low–Medium | The explanation doesn't assert npm never forwards signals. |
| DOCKER-C07 | docker-002, 005, 012, 013, 014, 015, 017, 018, 022, 023, 024, 027, 030 | both | P3 | Version currency | "Node.js 24 LTS" and `node:24-*` are used throughout. Per FACTS, Node 24 entered Maintenance on 2026-10-20 and Node 26 becomes LTS on 2026-10-28. This isn't wrong (24 is still supported), but it will read as dated. | ver fields e.g. "Node.js 24 LTS"; code `FROM node:24-alpine` | After 2026-10-28, switch examples to `node:26-*` (or note "current LTS, e.g. 26") and update ver labels to "Node 24 (Maintenance LTS)" where kept. | High (per FACTS) | No ver label calls 24 "Active LTS"; examples use the current Active LTS. |
| DOCKER-C08 | docker-032 | EN/BN | P3 | Mis-categorised | The docker.sock/TCP 2375 question sits under subtopic "Secrets"; it's host/daemon security. | `docker-032 \| Secrets \| extreme` | Recategorise as "Production Deployment" or a security subtopic. | High | Subtopic label matches content. |
| DOCKER-C09 | docker-029 | both | P3 | Unsupported market claim | Generalisation about local vs international teams without a source. | "local teams often run Compose on VMs or a managed service, while many international roles expect Kubernetes fluency" / BN "দেশের team-গুলো প্রায়ই…" | Soften to "smaller teams often…; larger/remote roles more often expect Kubernetes", without a geography claim. | Medium | No unsourced BD-market assertion. |
| DOCKER-C10 | docker-004, 009, 014, 020, 022, 028 (pattern) | both | P3 | Filler | Tips often end with generic claims about what impresses interviewers, which adds no information. | "That small detail sounds like production experience." ; "a quick credibility win in DevOps interviews" ; "Showing you can read symptoms like that is what impresses." | Trim the trailing praise sentences, or replace them with a concrete phrase to say. | High | Tips contain actionable content only. |
| DOCKER-C11 | docker-031 | both | P3 | Ambiguity | The question says "two VMs behind NGINX" (suggesting one NGINX in front), but the design puts NGINX on each VM, with an optional cloud LB. | "runs its Node.js API with Docker on two VMs behind NGINX" vs "Per VM: two slots … NGINX's upstream points at the active slot" | State the topology explicitly in the question (NGINX on each VM behind a cloud LB), or adapt the design to a single front NGINX. | Medium | Question and design describe the same topology. |
| DOCKER-C12 | docker-005/010, 014/024, 017/028, 018/019; cross-tech docker-025↔nginx-024, docker-031↔nginx-031 | both | P3 | Redundancy | Some themes repeat (localhost inside a container; 137 = SIGKILL; hardening list; "restart ignores unhealthy"). Each has a distinct angle, but learners will see the same points several times. | — | Keep, but cross-link with RELATED and trim duplicated paragraphs (e.g. 019's unhealthy explanation can point to 018). | Medium | RELATED fields link the overlapping items. |

## Per-question notes
- docker-001 — OK
- docker-002 — OK (C07 version note only)
- docker-003 — OK
- docker-004 — issues: C10; acc 10 / depth 8 / BN 9 / EN 9
- docker-005 — OK (C07)
- docker-006 — OK
- docker-007 — OK
- docker-008 — OK
- docker-009 — issues: C10; acc 10 / depth 9 / BN 9 / EN 9
- docker-010 — OK
- docker-011 — OK
- docker-012 — OK (C07)
- docker-013 — OK (C07)
- docker-014 — issues: C06, C07, C10; acc 9 / depth 9 / BN 9 / EN 9
- docker-015 — OK (C07)
- docker-016 — OK (minor: `--profile tools` is unnecessary with `run migrate` since targeting a service enables its profile, but it's harmless)
- docker-017 — OK (C07)
- docker-018 — OK (C07)
- docker-019 — issues: C03, C12; acc 7 / depth 8 / BN 8 / EN 9
- docker-020 — issues: C10; acc 9 / depth 9 / BN 9 / EN 9
- docker-021 — OK
- docker-022 — issues: C07, C10; acc 9 / depth 9 / BN 9 / EN 9 (see Needs verification)
- docker-023 — OK (C07)
- docker-024 — OK (C07)
- docker-025 — OK
- docker-026 — OK
- docker-027 — issues: C04, C07; acc 9 / depth 9 / BN 9 / EN 9
- docker-028 — issues: C05, C10; acc 8 / depth 9 / BN 9 / EN 9
- docker-029 — issues: C09; acc 9 / depth 9 / BN 8 / EN 9
- docker-030 — OK (C07)
- docker-031 — issues: C01, C02, C11; acc 7 / depth 9 / BN 9 / EN 9
- docker-032 — issues: C08; acc 9 / depth 10 / BN 9 / EN 9

## Coverage & gaps
- Every COVERAGE.md subtopic is covered: containers vs VMs, images/containers, Dockerfiles, layers/caching, build context, volumes/bind mounts, networks/DNS, port mapping, env vars, Compose, multi-stage, non-root, health checks, logs, image optimization, secrets, production deployment, debugging (inspect/logs/137/OOM), Docker vs Kubernetes.
- Small real gaps for juniors: no dedicated "basic container debugging toolkit" question (`docker exec -it … sh`, `docker inspect`, `docker cp`, `docker compose logs`). It's spread across 005/010/024 but never asked directly. A short easy item on Compose Watch / local dev workflow (`docker compose up --watch`) would also help, since today it appears only as extra code in docker-020. `docker init` (in FACTS) is not mentioned anywhere.
- Difficulty labels look appropriate. docker-019 (restart policies MCQ) could be easy rather than medium.
- Redundancy: see C12.

## Needs verification
- docker-022: distroless tag `gcr.io/distroless/nodejs24-debian13:nonroot` exists (Debian 13 based Node 24 variant).
- docker-022: `docker debug` availability (Docker Desktop; earlier releases needed a paid subscription). Confirm current licensing before implying it's universally available.
- docker-018: `start-interval` "needs Engine 25+" (ver field).
- docker-030: `docker scout cves --only-severity critical,high --only-fixed --exit-code` flag set and `--metadata-file` key `containerimage.digest` (believed correct).
- docker-021: `docker compose config --environment` flag (believed to be Compose ≥ 2.24).
- docker-019 (C03): wording of Docker's "10 seconds" rule against the current docs page.
- FACTS: Engine 29.9.0 / Compose v5.6.0. Not contradicted anywhere in the content.

## Verified
- No docker binary available locally (`which docker` → not found), so nothing was executed. The judgements above come from reasoning and established Docker behaviour.
- Cross-checked NGINX-related claims used in docker-031 (graceful reload, `http2 on;`) against https://nginx.org/en/CHANGES (see nginx findings). Consistent.
