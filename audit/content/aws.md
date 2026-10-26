# AWS content audit

Coverage: I reviewed all 32 question IDs in `dumps/aws.md`: aws-001, aws-002, aws-003, aws-004, aws-005, aws-006, aws-007, aws-008, aws-009, aws-010, aws-011, aws-012, aws-013, aws-014, aws-015, aws-016, aws-017, aws-018, aws-019, aws-020, aws-021, aws-022, aws-023, aws-024, aws-025, aws-026, aws-027, aws-028, aws-029, aws-030, aws-031, aws-032 (**32/32**).

## Category summary
The AWS category is very strong. Answers are technically precise, current for 2025–2026 (S3 2023 defaults, OAC over OAI, IMDSv2, `nodejs24.x` without callback handlers, ECS built-in blue/green, regional NAT Gateway, RCPs and declarative policies, DynamoDB MRSC), and full of production gotchas: the ALB/Node keep-alive 502, the 403-vs-404 behaviour behind OAC, `StringNotEquals` with a missing key, NAT cost traps, static stability, and fencing during DR failover. I found no wrong MCQ key and no materially false teaching claim.

The main weaknesses are structural:
- All 7 MCQs refer to options by number ("Option 2", "Option 4 is the tempting trap"), while the app labels them A–D and shows "Correct answer: B".
- The MCQs have no follow-ups.
- Several easy answers run well past the 60–120-word target.
- A few small internal inconsistencies: an RDS-managed secret described as containing host/port, a lifecycle rule on a `pending/` prefix the code never uses, and a fix script that doesn't close port 3000.

Bangla is excellent. It reads as natural Bangladeshi developer speech, keeps tech terms in Latin script, and preserves caveats, with only minor digit-script inconsistency.

On versions, the only staleness is "Node.js 24 LTS" in EC2/Express contexts. Per FACTS, Node 24 entered Maintenance on 2026-10-20 and Node 26 becomes LTS on 2026-10-28. Coverage matches COVERAGE.md well, and difficulty (11/11/7/3) and type mix are on target. The one real gap is Auto Scaling, which appears only inside aws-023 and has no dedicated question. Redundancy is intentional progression (003→004, 015→024, 012→020) and acceptable.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 9 | English quality 9 | Examples & code 9 | Originality/information value 9 | Structural clarity 8

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| AWS-C01 | aws-002, aws-004, aws-007, aws-011, aws-018, aws-019, aws-029 | both | P2 | MCQ structure | Answers and explanations name options by number, but the app renders options as an `<ol type="A">` and shows the key as "Correct answer: B — …". Learners see A–D, so "Option 4" has to be mentally translated, and aws-002 even says "The second option". | aws-002: "**Option 4 is the tempting trap.**", "Option 1 is wrong twice"; aws-029: "Option 2. Only **REST APIs**…"; BN "Option 4 হলো আকর্ষণীয় ফাঁদ" (app.js:3100 `h('ol', { type: 'A' …`, 3104 `'ABCD'[q.correctIndex]`) | Replace Option 1/2/3/4 with A/B/C/D in a_en/a_bn/ex_en/ex_bn for all 7 MCQs. | High | grep `Option [1-4]` in aws dump returns 0 hits; each explanation's letters match the rendered list. |
| AWS-C02 | aws-002, aws-004, aws-007, aws-011, aws-018, aws-019, aws-029 | both | P3 | Follow-ups | Every MCQ has an empty follow-up list, but AUTHORING §3 asks for 1–3 per question. aws-002 also has no related questions. | `FOLLOW-UPS: []`; aws-002 `RELATED: []` | Add 1–2 follow-ups each, e.g. aws-019 "When would you put an NLB in front of an ALB?", aws-029 "Why aren't API keys authentication?". Add related ['aws-023','aws-030'] to aws-002. | High | Dump shows non-empty FOLLOW-UPS for all 32. |
| AWS-C03 | aws-016 | both | P2 | Technical accuracy (code comment) | The code comment says an RDS-managed secret contains host/port. A secret created by RDS master-password management (`ManageMasterUserPassword`, `rds!db-…`) stores only `username` and `password`. Host/port only appear in secrets created through the Secrets Manager "credentials for RDS" flow. The destructuring `{ username, password, host, port }` would give `host`/`port` = undefined for an RDS-managed secret. | `// RDS-managed secret: JSON with username/password/host/port` … `const { username, password, host, port } = JSON.parse(db.SecretString);` | Change the comment to "Secrets Manager database secret (username/password/host/port)", or keep the RDS-managed secret and read host/port from config. Optionally note that RDS-managed secrets rotate every 7 days by default. | Medium (RDS doc fetched; it doesn't list the JSON fields, but from knowledge an `rds!` secret holds username/password only) | Run `aws secretsmanager get-secret-value` on an `rds!db-…` secret and check the keys. |
| AWS-C04 | aws-014 | both | P3 | Internal consistency | The cleanup advice targets a `pending/` prefix, but the code writes to `uploads/<userId>/` and never uses `pending/`. | "a lifecycle rule can expire objects under a `pending/` prefix" vs ``const key = `uploads/${req.user.id}/…` `` | Either upload to `pending/<userId>/…` and move/copy on confirm, or say "tag unconfirmed objects and expire by tag". | High | Prefixes in code and text agree. |
| AWS-C05 | aws-009 | both | P3 | Debugging fix incomplete | The answer says to close or restrict port 3000, and assumes an IGW is attached. The fix script only adds the route and port 22. It never revokes the `3000 0.0.0.0/0` rule or creates/attaches the IGW. | Answer: "close 3000 or restrict it to the load balancer"; "attach an IGW to the VPC"; Extra code has only `create-route` and `authorize-security-group-ingress … --port 22` | Add `aws ec2 create-internet-gateway` / `attach-internet-gateway` and `aws ec2 revoke-security-group-ingress … --port 3000 --cidr 0.0.0.0/0`. | High | Fix block contains IGW attach and revoke steps. |
| AWS-C06 | aws-012, aws-014, aws-022 | both | P3 | Version currency | "Node.js 24 LTS" is recommended for new EC2/Express deployments. Per FACTS, Node 24 entered Maintenance on 2026-10-20 and Node 26 becomes Active LTS on 2026-10-28, so this is about to be stale. Lambda `nodejs24.x` is a separate case and still correct. | aws-012: "Install: Node.js 24 LTS (NodeSource, nvm or official binaries)"; ver "Node.js 24 LTS"; aws-014 "// server.js — Express 5, Node.js 24" | Use "current Active LTS (Node.js 26 from 2026-10-28; 24 is Maintenance LTS)" or make it version-neutral ("the current LTS"). | High (per FACTS) | ver strings and text don't recommend 24 as the newest LTS after 2026-10-28. |
| AWS-C07 | aws-023 | both | P2 | Depth gap (security of design) | CloudFront + WAF fronts a *public* ALB, but nothing stops clients from hitting the ALB directly and bypassing WAF and caching. Restricting the origin is a standard senior-level point. | "`/api/*` behaviour forwards to the ALB with caching disabled"; "an **ALB** in public subnets" | Add: restrict the ALB SG to the CloudFront managed prefix list (`com.amazonaws.global.cloudfront.origin-facing`) plus a secret custom origin header checked by a listener rule, or use CloudFront VPC origins with an internal ALB. | Medium-High | Explanation mentions origin protection for the ALB. |
| AWS-C08 | aws-013 | both | P3 | Missing caveat | CloudFront custom error responses (403/404 → `/index.html` 200) apply to the whole distribution. If an API behaviour shares the distribution (as in aws-023), real API 404/403s get masked as HTML 200s. | "For an **SPA**, map 403 and 404 errors to `/index.html` with status 200 (or rewrite with a CloudFront Function)" | Add one line: the error mapping is distribution-wide, so prefer a CloudFront Function on the S3 behaviour when APIs share the distribution. | High | Caveat present. |
| AWS-C09 | aws-020 | both | P3 | Overstatement | "Always" is too strong. Negative caching (NXDOMAIN cached up to the SOA minimum TTL), DNSSEC mismatch after a nameserver change, or split-horizon resolvers can produce the same symptom. | "When the direct query works but the public one doesn't, it's always a delegation problem." / BN "সমস্যা সবসময় delegation-এ" | Replace with "almost always…; otherwise check negative caching/DNSSEC". | High | Wording softened. |
| AWS-C10 | aws-024 | both | P3 | Clue/consistency | The explanation says modern errors tell you which policy type denied the request, but the error shown is the bare form. AWS now usually appends e.g. "because no identity-based policy allows…" or "with an explicit deny in a resource-based policy", which is a key debugging clue. | Code: "is not authorized to perform: s3:PutObject on resource: …"; Answer: "many services now say which policy type denied the request" | Optionally append "because no identity-based policy allows the s3:PutObject action" to the shown error, and mention that fixing it would reveal the explicit-deny message next. | Medium | Error text and explanation agree. |
| AWS-C11 | aws-025 | both | P3 | Imprecision | The leak is per invocation, not one connection per environment: each warm environment accumulates a new unclosed client on every call. The explanation understates how fast connections pile up. | "Lambda scales out *environments*, and each one holds its own connection." | "…and each one accumulates a new unclosed connection on every invocation". | High | Wording fixed. |
| AWS-C12 | aws-001, aws-005, aws-006, aws-008, aws-010 | EN | P3 | Length vs difficulty | Easy answers are roughly 180–260 words against the ~60–120 guideline. They're excellent content but heavy to say aloud for an easy question. aws-010 packs limits, runtimes, the Node 24 handler change, cold starts and two concurrency types into an "easy" answer. | aws-010 answer has 4 dense bullets plus an intro; aws-006 lists 5 storage-class bullets plus versioning and lifecycle | Trim the answer to the core ~120 words and move details (payload limits, Express One Zone, API class names) to the explanation. Alternatively relabel aws-010 as medium. | Medium | Word counts within ~150 for easy answers. |
| AWS-C13 | aws-012, aws-020 (labels); aws-002 (text) | both | P3 | Market label / unsupported claim | `market=bangladesh` for generic "deploy Node on EC2" / DNS debugging has no FACTS justification (FACTS only says Docker/AWS appear as nice-to-have in BD job posts). aws-002 states a BD-team habit as fact. | `market=bangladesh` (aws-012, aws-020); aws-002: "Teams in Bangladesh often pick a nearby Region such as Mumbai or Singapore." | Use `market=both`, or justify the label (junior deployment tasks emphasised in BD full-stack roles). Rephrase aws-002 to "For users in Bangladesh, nearby Regions such as Mumbai or Singapore usually give the lowest latency; measure it." | Medium | Label justified or changed; claim reworded. |
| AWS-C14 | aws-027 | both | P3 | Minor currency | `rds.force_ssl` is presented as something to turn on, but on RDS for PostgreSQL 15+ it already defaults to 1. | "and `rds.force_ssl` on PostgreSQL" | "(default on for RDS PostgreSQL 15+; verify it on older versions)". | Medium | Note added. |
| AWS-C15 | aws-006, aws-010, aws-014, aws-025 (and others) | BN | P3 | BN consistency | Bangla and ASCII digits are mixed for the same kind of quantity, sometimes inside one passage. | aws-006 BN "IA class-এ ৩০ দিন" vs aws-025 BN "পুরো 30 second"; aws-014 BN "URL ৫ মিনিট valid" vs "5 MB"; aws-010 "সর্বোচ্চ timeout ১৫ মিনিট। Memory 128 MB" | Pick one convention (e.g. ASCII digits next to units and code, Bangla digits in prose) and apply it consistently. | High | Spot-check consistent. |
| AWS-C16 | — (category) | — | P3 | Coverage gap | Auto Scaling (launch templates, target tracking vs step scaling, warm-up, lifecycle hooks, instance refresh, health-check grace) is only mentioned inside aws-023/aws-028. COVERAGE lists "Auto Scaling" as a subtopic. | COVERAGE: "load balancers (ALB/NLB); Auto Scaling; Route 53" | Add or retarget one medium question on EC2 Auto Scaling groups (scaling policies, ELB health checks, launch template versions, cooldown/warm-up). | High | A question with sub="Auto Scaling" exists. |

## Per-question notes
- aws-001 — issues: AWS-C12; scores acc 9 / depth 9 / BN 9 / EN 9
- aws-002 — issues: AWS-C01, AWS-C02, AWS-C13; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-003 — OK
- aws-004 — issues: AWS-C01, AWS-C02; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-005 — issues: AWS-C12; scores acc 9 / depth 9 / BN 9 / EN 9
- aws-006 — issues: AWS-C12, AWS-C15; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-007 — issues: AWS-C01, AWS-C02; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-008 — issues: AWS-C12; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-009 — issues: AWS-C05; scores acc 9 / depth 9 / BN 9 / EN 9
- aws-010 — issues: AWS-C12, AWS-C15; scores acc 9 / depth 9 / BN 9 / EN 9 (I verified the Node 24 callback-handler claim)
- aws-011 — issues: AWS-C01, AWS-C02; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-012 — issues: AWS-C06, AWS-C13; scores acc 9 / depth 9 / BN 9 / EN 9
- aws-013 — issues: AWS-C08; scores acc 9 / depth 10 / BN 9 / EN 9
- aws-014 — issues: AWS-C04, AWS-C06, AWS-C15; scores acc 9 / depth 10 / BN 9 / EN 9
- aws-015 — OK
- aws-016 — issues: AWS-C03; scores acc 8 / depth 9 / BN 9 / EN 9
- aws-017 — OK (I verified the regional NAT Gateway claims)
- aws-018 — issues: AWS-C01, AWS-C02; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-019 — issues: AWS-C01, AWS-C02; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-020 — issues: AWS-C09, AWS-C13; scores acc 9 / depth 9 / BN 9 / EN 9
- aws-021 — OK
- aws-022 — issues: AWS-C06; scores acc 9 / depth 9 / BN 9 / EN 9
- aws-023 — issues: AWS-C07; scores acc 9 / depth 8 / BN 9 / EN 9
- aws-024 — issues: AWS-C10; scores acc 10 / depth 10 / BN 9 / EN 9
- aws-025 — issues: AWS-C11, AWS-C15; scores acc 9 / depth 10 / BN 9 / EN 9
- aws-026 — OK
- aws-027 — issues: AWS-C14; scores acc 9 / depth 9 / BN 9 / EN 9
- aws-028 — OK (see Needs verification on ECS native canary/linear)
- aws-029 — issues: AWS-C01, AWS-C02; scores acc 10 / depth 9 / BN 9 / EN 9
- aws-030 — OK (I verified the MRSC claims)
- aws-031 — OK
- aws-032 — OK

## Coverage & gaps
- All COVERAGE.md subtopics are covered except a dedicated **Auto Scaling** question (AWS-C16).
- Difficulty is 11 easy / 11 medium / 7 hard / 3 extreme, which is on target. MCQs: 7 (target 7–9).
- Type minimums are met: 7 conceptual, 4 scenario, 4 debugging + 2 coding, 3 comparison, 1 security-performance, 2 architecture + 2 system-design.
- Junior deployment questions (aws-012 EC2+NGINX+PM2, aws-013 S3+CloudFront) are clearly separated from architecture questions, as COVERAGE asks.
- These overlaps are intentional and acceptable: aws-003↔aws-004 (instance profile), aws-015↔aws-024 (bucket vs object ARN), aws-012↔aws-020 (EC2 + DNS + certbot), aws-017↔aws-026 (NAT cost trap repeated almost verbatim). Consider trimming the repeated NAT story in one of them.
- Possible additions for this audience, not mandatory: a CI/CD question on deploying to ECS/EC2 from GitHub Actions with OIDC (currently only follow-ups mention it), and an ElastiCache basics question.
- No mis-categorised questions found. aws-010 is arguably medium given its density (AWS-C12).

## Needs verification
- aws-022: "Node's `server.keepAliveTimeout` defaults to 5 s". This is true on v22 (verified locally). I could not confirm whether Node 24/26 changed the default; a web search found no evidence of a change. Low risk.
- aws-028: canary is shown only through CodeDeploy (`CodeDeployDefault.ECSCanary10Percent5Minutes`) plus ECS built-in blue/green. I believe Amazon ECS also added built-in linear and canary deployment strategies (late 2025). If so, mention it as the simpler native option. Not verified.
- aws-004 / FACTS: "Amazon Linux 2023 AMIs require IMDSv2, and you can set an account-level default". This is consistent with my knowledge; not fetched.
- aws-030: `rds.global_db_rpo` blocks commits when lag exceeds the limit (Aurora PostgreSQL). Consistent with my knowledge; not fetched.
- aws-016: RDS-managed secret JSON fields (see AWS-C03); the RDS doc page doesn't list the fields explicitly.

## Verified
- WebFetch https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html: "Callback-based function handlers are only supported up to Node.js 22. Starting from Node.js 24, asynchronous tasks should be implemented using async function handlers." Synchronous `(event)`/`(event, context)` handlers are listed as valid. This confirms the aws-010 and aws-025 claims.
- WebFetch https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html: the regional NAT Gateway exists, "you don't need to create a public subnet to host it", `--availability-mode regional`, and it expands across AZs. This confirms aws-017 and aws-023.
- WebFetch https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/multi-region-strong-consistency-gt.html: MRSC needs "exactly three Regions … three replicas, or with two replicas and one witness", and "TTL is not supported" and transactions are not supported for MRSC. Mumbai and Singapore are in the supported list. This confirms aws-030.
- WebFetch https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html: RDS-managed secrets exist (`rds!db-…`) and rotate every 7 days by default. The page doesn't list the JSON fields (relevant to AWS-C03).
- `/usr/local/bin/node -e` (v22.18.0): `http.createServer().keepAliveTimeout` = 5000 and `headersTimeout` = 60000. This confirms the aws-022 statement for v22.
- WebSearch on the Node keepAliveTimeout default change in v24/v25: no evidence of a change.
- app.js lines 3100/3104: MCQ options are rendered as `<ol type="A">` and the key as `'ABCD'[q.correctIndex]`, and options are not shuffled. This is the basis for AWS-C01.
