# NestJS content audit

Coverage: 32 of 32 questions reviewed: nest-001, nest-002, nest-003, nest-004, nest-005, nest-006, nest-007, nest-008, nest-009, nest-010, nest-011, nest-012, nest-013, nest-014, nest-015, nest-016, nest-017, nest-018, nest-019, nest-020, nest-021, nest-022, nest-023, nest-024, nest-025, nest-026, nest-027, nest-028, nest-029, nest-030, nest-031, nest-032.

## Category summary
This is a strong category. The technical content is accurate almost throughout. I found no wrong MCQ keys and no wrong expected outputs. Option letters in the explanations match the A–D order. Answers are framed the way an interviewer wants: direct answer, then the mechanism, then the practical consequence. They also include real production details: scope bubbling, the guard-error blind spot for interceptors, `DrizzleQueryError.cause`, transaction-local `set_config` behind PgBouncer, and `FORCE ROW LEVEL SECURITY`. Code is idiomatic and current: ESM `.js` imports, Express 5, Throttler v6 millisecond `ttl`, and zod 4 `z.email()`/`z.url()`. I spot-checked the riskiest v12 claims against docs.nestjs.com and npm and they hold up: `StandardSchemaValidationPipe`, the `schema` option, Standard Schema support in `@nestjs/config` with Joi v18+, `@nestjs/drizzle` and `@nestjs/idempotency` at 0.0.x from Sept 2026, and the 12.x versions of `@nestjs/config`, `@nestjs/jwt` and `@nestjs/cqrs`. The weaknesses are all minor:
- code excerpts with missing imports
- small internal naming inconsistencies
- empty follow-ups on every MCQ
- "Verified …" authoring notes leaking into learner text
- "NestJS 12.1" labels now one minor behind (12.2.0 shipped 2026-10-19)
- one real coverage gap: TypeORM, Prisma and Mongoose integration, which Bangladeshi job posts list often, is only mentioned in passing

The Bangla is excellent: natural Bangladeshi developer register, tech terms in Latin script, consistent terminology, and no meaning drift found. Two areas repeat across several questions: the guard-error blind spot (4 questions) and guards vs middleware (2 questions). The difficulty spread (11/11/7/3) and the MCQ count (8) are on target.

Scores: Technical accuracy 9 | Explanation depth 9 | Interview usefulness 9 | Bangla quality 9 | English quality 9 | Examples & code 8 | Originality/information value 9 | Structural clarity 9

## Issue register
| ID | Question id(s) | Lang | Severity | Category | Issue | Evidence (quote) | Recommended correction | Confidence | Verification / acceptance test |
|---|---|---|---|---|---|---|---|---|---|
| NEST-C01 | all (ver labels), esp. nest-009 | both | P3 | Version currency | Every question is labelled "NestJS 12.1", and FACTS says 12.1.3 (2026-10-12). npm shows `@nestjs/core` **12.2.0** was published 2026-10-19 as `latest`. Nothing taught is wrong, but the label is already one minor behind. | "ver=NestJS 12.1 …" | Update FACTS/labels to "NestJS 12.x (12.2 current)" or use "NestJS 12" where the minor doesn't matter. Check the 12.2 release notes for anything that affects nest-009/017. | High | `npm view @nestjs/core dist-tags.latest` → 12.2.0 |
| NEST-C02 | nest-017 | both | P3 | API accuracy | The code uses a property key plus an options object: `@Query('page', { schema })`. The docs only show the whole-object form `@Query({ schema: listUsersQuerySchema })`. The property-key overload is unverified. | "`list(@Query('page', { schema: pageSchema }) page: number)`" | Verify the overload. If it isn't supported, use a query schema object `@Query({ schema: z.object({ page: ... }) })`. | Medium | Run the snippet on NestJS 12.1: `GET /users?page=3` returns `page === 3` (number), and a missing page returns 1 |
| NEST-C04 | nest-002, nest-014, nest-022, nest-024 (extra), nest-030 | code | P3 | Code completeness | Code that is presented as a solution is missing imports. nest-002 is a `coding` reference solution, yet the service file uses `CreateUserDto`/`UpdateUserDto` and the controller uses `UsersService`/`CreateUserDto` without importing them. nest-022's repository uses `Injectable` and `eq` without imports. | nest-002: "`export interface User extends CreateUserDto { id: number }`" (no import in that file); nest-022: "`@Injectable() export class UsersRepository`… `eq(schema.users.email, email)`" | Add the missing import lines, or add a single comment such as "// imports omitted". nest-014 already does this. | High | Paste nest-002 into a fresh Nest 12 project and run `tsc --noEmit` with no errors |
| NEST-C05 | nest-003 | both | P3 | Internal consistency | The answer text names `UsersService`/`UsersController`, but the code example defines `GreetingService`/`GreetingController`. | "When I list `UsersService` in a module's `providers`…" vs code "`export class GreetingService`" | Use the same names in the code and the prose. | High | Read-through: the names match |
| NEST-C06 | nest-015 | both | P3 | Code/text mismatch; reference | The explanation advises pinning the algorithm, but the code doesn't do it. The OWASP reference is the Java-specific JWT cheat sheet. | "pin the algorithm" vs `JwtModule.registerAsync({ … secret, signOptions: { expiresIn: '15m' } })`; ref ".../JSON_Web_Token_for_Java_Cheat_Sheet.html" | Add `verifyOptions: { algorithms: ['HS256'] }` and `signOptions.algorithm`. Swap the reference for a language-neutral OWASP page (e.g. REST Security or Authentication cheat sheet), or keep it but label it "Java examples, concepts apply". | High | The code contains `algorithms: ['HS256']` |
| NEST-C07 | nest-024 | both | P3 | Exact error text | The quoted Nest error message is shortened. The real message reads "...Please make sure that the argument dependency at index [0] is available in the OrdersModule context." | "Please make sure that the argument at index [0] is available" | Quote the full real message, or mark it with "…". | Medium | Reproduce the cycle in a CJS build and copy the message |
| NEST-C08 | nest-026 | both | P3 | Accuracy (minor) | `@fastify/cookie` is listed as part of the replacement set for `express-session`. Sessions need `@fastify/secure-session` or `@fastify/session`; `@fastify/cookie` replaces `cookie-parser`. | "`express-session`, `compression`) must be replaced with Fastify plugins (`@fastify/helmet`, `@fastify/multipart`, `@fastify/cookie`, `@fastify/compress`)" | List the pairs explicitly: helmet→@fastify/helmet, multer→@fastify/multipart, cookie-parser→@fastify/cookie, express-session→@fastify/secure-session, compression→@fastify/compress. | High | Each Express middleware maps to the right plugin |
| NEST-C09 | nest-004, 005, 006, 009, 010, 012, 018, 029 | both | P3 | Structure | All 8 MCQs have empty follow-ups. AUTHORING §3 asks for 1–3 per question. | "FOLLOW-UPS: []" | Add 1–2 follow-ups each (e.g. nest-004: "When is `Scope.TRANSIENT` useful?"; nest-029: "How would you log 401/403s then?"). | High | `follow` is non-empty for every MCQ |
| NEST-C10 | nest-028, nest-029 | both | P3 | Authoring artifact | Learner-facing text claims verification by the author. The reader can't act on this and it reads oddly. | nest-029: "(Verified on NestJS 12.1: a guard's 403 never reached the interceptor…)"; nest-028: "**Verified trap:**" | Rephrase as fact ("A guard's 403 never reaches the interceptor…") and drop "Verified". | High | No "Verified" wording remains in the learner text |
| NEST-C11 | nest-032 | code | P3 | Security edge case | The signature check compares string lengths and then compares byte buffers. A non-ASCII header can have equal string length but different byte length, so `timingSafeEqual` throws `RangeError` and the request returns 500 instead of 401. nest-007 does it correctly by comparing Buffer lengths. | "`signature.length !== expected.length || !timingSafeEqual(Buffer.from(signature), Buffer.from(expected))`" | Build both Buffers first and compare `.length` on the Buffers. Or decode the hex: `Buffer.from(signature, 'hex')`. | High | Sending header `x-signature` with multibyte characters of equal length returns 401, not 500 |
| NEST-C12 | nest-013, nest-021, nest-023 (extra) | both | P3 | Security nuance | A client-supplied `x-request-id` is reused without validation and echoed back into logs and headers. That allows log forging and unbounded values. | "`const requestId = req.header('x-request-id') ?? randomUUID();`" | Accept the incoming id only if it matches a UUID/short safe pattern (e.g. `/^[\w-]{1,64}$/`), otherwise generate a new one. Mention this in the explanation. | Medium | Unit test: a malicious header gets replaced |
| NEST-C13 | nest-012, nest-013, nest-021, nest-029 | both | P3 | Redundancy | The "guard errors are invisible to interceptors" insight appears as a key point in 4 questions. "Guards vs middleware for auth" is repeated in nest-007, nest-015 and nest-021. | nest-012: "an exception thrown by a guard is never seen by an interceptor's `catchError`"; nest-013 tip: "mention the guard-error blind spot"; nest-029 is entirely about it | Keep nest-029 as the dedicated item. In nest-012 and nest-013, reduce the point to a one-line cross-reference. | High | Each insight is primary in only one question |
| NEST-C14 | nest-004, nest-006 vs nest-005 | meta | P3 | Market label | Labels are inconsistent: two fundamentals MCQs are `bangladesh`, while a very similar fundamentals MCQ (nest-005) is `both`. FACTS allows `bangladesh` for written-MCQ style, so this isn't wrong, just inconsistent. | "nest-004 … market=bangladesh"; "nest-005 … market=both" | Use `both` for all three, or apply `bangladesh` consistently to fundamentals MCQs. | Medium | Consistent labels |
| NEST-C15 | (category) | both | P2 | Coverage gap | COVERAGE asks for "database integration (TypeORM/Prisma/Drizzle/Mongoose)". Only Drizzle has a worked question (nest-022). TypeORM, Prisma and `@nestjs/mongoose` get one sentence each, even though FACTS notes BD job posts list Mongoose/Prisma/TypeORM. | nest-022: "TypeORM has `@nestjs/typeorm` (`forRootAsync` + `forFeature` + `@InjectRepository`), Mongoose has `@nestjs/mongoose`, and Prisma is usually a `PrismaService` provider" | Add one medium question, e.g. "`@nestjs/mongoose` `MongooseModule.forFeature` + `@InjectModel` vs a `PrismaService` with `onModuleInit`/shutdown". Or extend nest-022 with a short example. | High | The bank has at least one question with a Mongoose or Prisma/TypeORM Nest code sample |

(NEST-C03 was withdrawn: npm confirms that `@nestjs/config` 12.0.1 exists, so the "@nestjs/config 12" label is correct.)

## Per-question notes
- nest-001 — OK (acc 10 / depth 9 / BN 9 / EN 9)
- nest-002 — issues: NEST-C04; scores acc 9 / depth 9 / BN 9 / EN 9
- nest-003 — issues: NEST-C05; scores acc 9 / depth 9 / BN 9 / EN 9 (the v12 "import type" error-hint claim is in Needs verification)
- nest-004 — issues: NEST-C09, NEST-C14; scores acc 10 / depth 9 / BN 9 / EN 9
- nest-005 — issues: NEST-C09; scores acc 10 / depth 9 / BN 9 / EN 9 (output `"21"` correct; `abc` → NaN → `null` correct)
- nest-006 — issues: NEST-C09, NEST-C14; scores acc 10 / depth 9 / BN 9 / EN 9
- nest-007 — OK (acc 10 / depth 9 / BN 9 / EN 9; 403 body text correct)
- nest-008 — OK (acc 10 / depth 9 / BN 9 / EN 9; both JSON bodies match Nest's built-in filter)
- nest-009 — issues: NEST-C09; scores acc 9 / depth 9 / BN 9 / EN 9 (CLI Vitest default is in Needs verification)
- nest-010 — issues: NEST-C09; scores acc 9 / depth 9 / BN 9 / EN 9 (Standard Schema `validationSchema` and Joi v18 verified)
- nest-011 — OK (acc 9 / depth 8 / BN 9 / EN 9; the BD job-post remark is consistent with FACTS research notes)
- nest-012 — issues: NEST-C09, NEST-C13; scores acc 10 / depth 9 / BN 9 / EN 9
- nest-013 — issues: NEST-C12, NEST-C13; scores acc 9 / depth 9 / BN 9 / EN 9
- nest-014 — issues: NEST-C04 (minor; it has an "imports omitted" note); scores acc 10 / depth 9 / BN 9 / EN 9
- nest-015 — issues: NEST-C06, NEST-C13; scores acc 9 / depth 9 / BN 9 / EN 9
- nest-016 — OK (acc 9 / depth 10 / BN 9 / EN 9; the exact order of the three messages in the fixed-DTO comment is not executed, Low risk)
- nest-017 — issues: NEST-C02; scores acc 9 / depth 9 / BN 9 / EN 9 (pipe, `schema` option and error prefix verified in docs)
- nest-018 — issues: NEST-C09; scores acc 10 / depth 9 / BN 9 / EN 9
- nest-019 — OK (acc 10 / depth 9 / BN 9 / EN 9)
- nest-020 — OK (acc 9 / depth 9 / BN 9 / EN 9; the e2e test is in extra code)
- nest-021 — issues: NEST-C12, NEST-C13; scores acc 9 / depth 9 / BN 9 / EN 9 (`forRoutes('*')` still shown in current docs, so not flagged)
- nest-022 — issues: NEST-C04, NEST-C15; scores acc 9 / depth 9 / BN 9 / EN 9
- nest-023 — issues: NEST-C12 (extra code); scores acc 10 / depth 10 / BN 9 / EN 9
- nest-024 — issues: NEST-C07; scores acc 9 / depth 10 / BN 9 / EN 9 (CJS `undefined` vs ESM TDZ explanation correct)
- nest-025 — OK (acc 10 / depth 10 / BN 9 / EN 9; `DrizzleQueryError` since 0.44 is consistent with the Drizzle 0.44 release)
- nest-026 — issues: NEST-C08; scores acc 9 / depth 9 / BN 9 / EN 9
- nest-027 — OK (acc 9 / depth 9 / BN 9 / EN 9; the NATS v3 claim is in Needs verification)
- nest-028 — issues: NEST-C10; scores acc 10 / depth 10 / BN 9 / EN 9
- nest-029 — issues: NEST-C09, NEST-C10, NEST-C13; scores acc 10 / depth 9 / BN 9 / EN 9
- nest-030 — OK (acc 9 / depth 10 / BN 9 / EN 9; `international` label justified)
- nest-031 — OK (acc 10 / depth 10 / BN 9 / EN 9)
- nest-032 — issues: NEST-C11; scores acc 9 / depth 10 / BN 9 / EN 9

## Coverage & gaps
- Covered: modules, controllers/REST, providers/DI, scopes (incl. durable), custom providers, dynamic modules, custom decorators, pipes, guards, interceptors, filters, DTOs, both validation styles, middleware, JWT/RBAC, guards vs middleware, lifecycle order, config, Drizzle integration, testing, WebSockets and microservices, architecture, Express vs Fastify, Nest vs Express, v12 changes, circular deps, idempotency, multi-tenancy.
- Gap (P2, NEST-C15): there is no worked TypeORM, Prisma or Mongoose integration question. This matters for the stated BD MERN/NestJS market.
- Minor gaps worth considering: lifecycle hooks (`onModuleInit` / `onApplicationBootstrap` / `beforeApplicationShutdown`) only appear incidentally; queues with `@nestjs/bullmq` and Swagger/OpenAPI with `@nestjs/swagger` are only mentioned. Neither is required by COVERAGE.
- Redundancy: see NEST-C13.
- Difficulty: easy 11 / medium 11 / hard 7 / extreme 3, on target. The labels look right. nest-004 (scopes, easy) and nest-023 (scopes, hard) progress well.

## Needs verification
- nest-003: "The NestJS 12 error message even suggests checking for `import type`."
- nest-009 / nest-020 / nest-024: "New projects from the CLI default to ESM with Vitest (a CommonJS + Jest option is still offered)", and "Vitest (`vi.fn()`, globals enabled)".
- nest-027: "the NATS transport moved to the `@nats-io/transport-node` (NATS v3) client package" in v12.
- nest-030: "NestJS 12 uses Rspack by default for monorepo builds" (matches FACTS; not independently checked).
- nest-017: `@Query('page', { schema })` property-key overload (see NEST-C02).

## Verified
- `npm view` (2026-10-26): `@nestjs/core` latest 12.2.0 (12.1.3 published 2026-10-12, 12.2.0 on 2026-10-19); `@nestjs/config` 12.0.1; `@nestjs/jwt` 12.0.3; `@nestjs/cqrs` 12.1.1; `@nestjs/drizzle` 0.0.2, created 2026-09-23; `@nestjs/idempotency` 0.0.2, created 2026-09-25. So the version labels in nest-010/015/030 and the "0.0.x, Sept 2026" claims in nest-022/032 are **correct**. The only finding is NEST-C01 (12.2 is out).
- WebFetch https://docs.nestjs.com/data/drizzle: the page exists. It documents `@nestjs/drizzle`, `DrizzleModule.forRoot({ drizzle, connection, … })`, `forRootAsync`, `@InjectDrizzle()`, targets Drizzle v1 (rc) and supports 0.35+. No version number. This matches nest-022 apart from the version/date.
- WebFetch https://docs.nestjs.com/reliability/idempotency: the page exists. It documents `@nestjs/idempotency` and `@Idempotent()` with no version label. This matches nest-032.
- WebFetch https://docs.nestjs.com/techniques/validation (canonical /application/validation): confirms `StandardSchemaValidationPipe`; the `schema` option on `@Body()`, `@Query()` and `@Param()`; and messages "prefixed with the path of the invalid property", e.g. "email: Invalid email address". This matches nest-017. The docs example uses the whole-object `@Query({ schema })`.
- WebFetch https://docs.nestjs.com/techniques/configuration: `validationSchema` accepts Standard Schema (zod); "Joi … requires Joi v18 or later"; a missing required variable throws during bootstrap. This matches nest-009 and nest-010.
- WebFetch https://docs.nestjs.com/middleware: the docs still show `.forRoutes('*')` for global class middleware, so nest-021 is not flagged.
- Reasoned and not executed (no Nest install): nest-005 output (`ValidationPipe` skips primitive metatypes and returns the original value without `transform`); nest-008 bodies; nest-024 TS metadata emit (CJS gives `undefined`, ESM throws a TDZ `ReferenceError`, since `typeof` on a TDZ binding throws); nest-032 `INSERT … ON CONFLICT DO NOTHING` blocking semantics under READ COMMITTED.
