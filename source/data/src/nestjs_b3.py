# NestJS — batch 3 (nest-017 … nest-024): Standard Schema, custom providers, dynamic modules, testing,
# guards vs middleware, DB integration, request scope, circular dependencies
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NEST_VALIDATION = ("NestJS docs — Validation", "https://docs.nestjs.com/application/validation")
NEST_PIPES = ("NestJS docs — Pipes", "https://docs.nestjs.com/pipes")
NEST_CUSTOM_PROVIDERS = ("NestJS docs — Custom providers", "https://docs.nestjs.com/fundamentals/custom-providers")
NEST_DYNAMIC = ("NestJS docs — Dynamic modules", "https://docs.nestjs.com/fundamentals/dynamic-modules")
NEST_TESTING = ("NestJS docs — Testing", "https://docs.nestjs.com/fundamentals/testing")
NEST_MIDDLEWARE = ("NestJS docs — Middleware", "https://docs.nestjs.com/middleware")
NEST_GUARDS = ("NestJS docs — Guards", "https://docs.nestjs.com/guards")
NEST_DRIZZLE = ("NestJS docs — Drizzle", "https://docs.nestjs.com/data/drizzle")
NEST_LIFECYCLE_EVENTS = ("NestJS docs — Lifecycle events", "https://docs.nestjs.com/fundamentals/lifecycle-events")
NEST_SCOPES = ("NestJS docs — Injection scopes", "https://docs.nestjs.com/fundamentals/injection-scopes")
NEST_ALS = ("NestJS docs — Async Local Storage", "https://docs.nestjs.com/recipes/async-local-storage")
NEST_CIRCULAR = ("NestJS docs — Circular dependency", "https://docs.nestjs.com/fundamentals/circular-dependency")
NEST_COMMON_ERRORS = ("NestJS docs — Common errors", "https://docs.nestjs.com/faq/common-errors")
DRIZZLE_PG = ("Drizzle ORM — PostgreSQL", "https://orm.drizzle.team/docs/get-started-postgresql")
STANDARD_SCHEMA = ("Standard Schema specification", "https://github.com/standard-schema/standard-schema")

QUESTIONS = [
    # ------------------------------------------------------------------ nest-017
    Q(
        id="nest-017", sub="Validation (Standard Schema, v12)", diff="medium", type="comparison",
        prio="medium", market="both", mins=6,
        tags=["standard-schema", "zod", "validation", "class-validator", "nestjs-12"],
        ver="NestJS 12.1 (Standard Schema validation added in v12)", vs=True, status="stable",
        q_en=r"""NestJS 12 adds Standard Schema validation (e.g. zod schemas). How does it compare with the classic `ValidationPipe` + class-validator approach, and how would you adopt it in an existing app?""",
        q_bn=r"""NestJS 12-এ Standard Schema validation (যেমন zod schema) যোগ হয়েছে। এটা classic `ValidationPipe` + class-validator approach-এর সাথে তুলনায় কেমন, আর একটা existing app-এ কীভাবে চালু করবে?""",
        a_en=r"""
            - **class-validator:** the DTO is a class with decorators (`@IsEmail()`); `ValidationPipe` uses class-transformer to build an instance and validates it. Unknown fields are handled with `whitelist` / `forbidNonWhitelisted`.
            - **Standard Schema (v12):** the DTO is a schema object (zod, Valibot, ArkType) and the TypeScript type is inferred (`z.infer`). You attach it with the `schema` option — `@Body({ schema: createUserSchema })`, also on `@Query()` and `@Param()` — and `StandardSchemaValidationPipe` validates it. The schema decides unknown keys: `z.object` strips, `z.strictObject` rejects, `z.looseObject` keeps. By default the handler receives the schema's **output**, so coercion, defaults and `.trim()` apply.

            Adoption: register **both** pipes globally. `ValidationPipe` only validates class-typed parameters and `StandardSchemaValidationPipe` only validates parameters that declare a schema, so old and new endpoints coexist and you migrate module by module.
        """,
        a_bn=r"""
            - **class-validator:** DTO হলো decorator (`@IsEmail()`) সহ একটা class; `ValidationPipe`, class-transformer দিয়ে instance বানিয়ে validate করে। অজানা field সামলানো হয় `whitelist` / `forbidNonWhitelisted` দিয়ে।
            - **Standard Schema (v12):** DTO হলো একটা schema object (zod, Valibot, ArkType), আর TypeScript type infer হয় (`z.infer`)। `schema` option দিয়ে লাগানো হয় — `@Body({ schema: createUserSchema })`, `@Query()` আর `@Param()`-এও — আর `StandardSchemaValidationPipe` সেটা validate করে। অজানা key-র ব্যাপারে schema-ই সিদ্ধান্ত নেয়: `z.object` বাদ দেয়, `z.strictObject` reject করে, `z.looseObject` রেখে দেয়। Default-এ handler schema-র **output** পায়, তাই coercion, default আর `.trim()` apply হয়।

            চালু করার উপায়: **দুটো** pipe-ই globally register করো। `ValidationPipe` শুধু class-typed parameter validate করে আর `StandardSchemaValidationPipe` শুধু যেসব parameter-এ schema আছে সেগুলো, তাই পুরোনো আর নতুন endpoint পাশাপাশি চলে, আর module ধরে ধরে migrate করা যায়।
        """,
        quick_en=r"""class-validator uses decorated DTO classes checked by `ValidationPipe`; NestJS 12's Standard Schema takes a zod or Valibot schema via the `schema` option on `@Body()`, `@Query()` or `@Param()`, validated by `StandardSchemaValidationPipe`. Register both pipes globally and migrate module by module.""",
        quick_bn=r"""class-validator-এ decorator দেওয়া DTO class থাকে, যেটা `ValidationPipe` check করে; NestJS 12-এর Standard Schema-তে `@Body()`, `@Query()` বা `@Param()`-এর `schema` option-এ zod বা Valibot schema দিই, আর `StandardSchemaValidationPipe` validate করে। দুটো pipe-ই global রেখে module ধরে ধরে migrate করি।""",
        ex_en=r"""
            **Trade-offs:**
            - Schemas can be **shared with the frontend** (React Hook Form + zod) — one source of truth for validation rules. That's the strongest argument.
            - No `reflect-metadata` tricks for validation, nested objects and arrays work naturally (`z.array(itemSchema)`), and the type is inferred, so DTO and type never drift.
            - class-validator DTOs integrate deeply with existing tooling (e.g. the `@nestjs/swagger` CLI plugin reads classes). Check how your OpenAPI setup handles schema-based DTOs before migrating public APIs.

            **Gotcha (easy to miss):** the `schema` option does nothing by itself. If `StandardSchemaValidationPipe` isn't bound — globally or via `@Body({ schema, pipes: [StandardSchemaValidationPipe] })` — the body passes through unvalidated.

            Errors are 400 with messages prefixed by the property path, e.g. `"email: Invalid email address"`.
        """,
        ex_bn=r"""
            **Trade-off:**
            - Schema **frontend-এর সাথে share** করা যায় (React Hook Form + zod) — validation rule-এর একটাই source of truth। এটাই সবচেয়ে বড় যুক্তি।
            - Validation-এর জন্য `reflect-metadata`-এর কৌশল লাগে না, nested object আর array স্বাভাবিকভাবে কাজ করে (`z.array(itemSchema)`), আর type infer হয় বলে DTO আর type কখনো আলাদা হয়ে যায় না।
            - class-validator DTO existing tooling-এর সাথে গভীরভাবে যুক্ত (যেমন `@nestjs/swagger` CLI plugin class পড়ে)। Public API migrate করার আগে দেখো তোমার OpenAPI setup schema-based DTO কীভাবে handle করে।

            **সহজে চোখ এড়ানো ফাঁদ:** `schema` option নিজে কিছুই করে না। `StandardSchemaValidationPipe` যদি bind করা না থাকে — globally বা `@Body({ schema, pipes: [StandardSchemaValidationPipe] })` দিয়ে — তাহলে body validate না হয়েই চলে যায়।

            Error হলে 400 আসে, message-এর শুরুতে property path থাকে, যেমন `"email: Invalid email address"`।
        """,
        tip_en=r"""Frame it as "two valid tools, incremental migration". Mention sharing schemas with the frontend and the "schema option needs the pipe" gotcha — that shows you've actually used v12, not just read the release notes.""",
        tip_bn=r""""দুটোই valid tool, ধাপে ধাপে migration" — এভাবে বলো। Frontend-এর সাথে schema share করা আর "schema option-এর জন্য pipe লাগে" ফাঁদটার কথা বলো — এতে বোঝা যায় তুমি শুধু release note পড়োনি, v12 আসলে ব্যবহার করেছ।""",
        mist_en=r"""Assuming v12 removed class-validator; adding `schema` to `@Body()` without registering `StandardSchemaValidationPipe`; using `z.object` and expecting unknown keys to be rejected (it strips them).""",
        mist_bn=r"""ধরে নেওয়া যে v12 class-validator সরিয়ে দিয়েছে; `StandardSchemaValidationPipe` register না করে `@Body()`-এ `schema` দেওয়া; `z.object` ব্যবহার করে আশা করা যে অজানা key reject হবে (আসলে বাদ দিয়ে দেয়)।""",
        code=r"""
            // main.ts — both pipes side by side during migration
            app.useGlobalPipes(
              new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }),
              new StandardSchemaValidationPipe(),
            );

            // users/users.schemas.ts
            import { z } from 'zod';

            export const createUserSchema = z.strictObject({
              email: z.email(),
              password: z.string().min(12),
              displayName: z.string().trim().max(50).optional(),
            });
            export type CreateUserDto = z.infer<typeof createUserSchema>;

            const pageSchema = z.coerce.number().int().min(1).default(1);

            // users/users.controller.ts
            @Controller('users')
            export class UsersController {
              @Post()
              create(@Body({ schema: createUserSchema }) dto: CreateUserDto) {
                return this.usersService.create(dto); // displayName already trimmed
              }

              @Get()
              list(@Query('page', { schema: pageSchema }) page: number) {
                return this.usersService.list(page); // "3" -> 3, missing -> 1
              }
            }
        """,
        lang="typescript",
        follow=[
            ("How would you return a custom error shape for schema validation failures?", "Schema validation fail হলে custom error shape কীভাবে return করবে?"),
            ("Would you share zod schemas between a Next.js frontend and a NestJS backend? How?", "Next.js frontend আর NestJS backend-এর মধ্যে zod schema share করবে? কীভাবে?"),
        ],
        related=["nest-006", "nest-016", "nest-009"],
        refs=[NEST_VALIDATION, STANDARD_SCHEMA],
    ),
    # ------------------------------------------------------------------ nest-018
    Q(
        id="nest-018", sub="Custom Providers", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["custom-providers", "usefactory", "useexisting", "injection-tokens"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""Given these providers in one module, `OrdersService` injects `CacheService` and `ReportsService` injects `@Inject('LegacyCache')`. How many times does the factory run, and how many `CacheService` instances exist?""",
        q_bn=r"""একটা module-এ নিচের provider গুলো আছে। `OrdersService`, `CacheService` inject করে আর `ReportsService`, `@Inject('LegacyCache')` inject করে। Factory কতবার চলবে, আর কয়টা `CacheService` instance থাকবে?""",
        code=r"""
            providers: [
              { provide: 'CACHE_TTL', useValue: 60 },
              {
                provide: CacheService,
                useFactory: (ttl: number) => new CacheService(ttl),
                inject: ['CACHE_TTL'],
              },
              { provide: 'LegacyCache', useExisting: CacheService },
              OrdersService,
              ReportsService,
            ]
        """,
        lang="typescript",
        options=[
            ("Twice — `useExisting` re-runs the factory to build a second instance", "দুইবার — `useExisting` factory আবার চালিয়ে দ্বিতীয় instance বানায়"),
            ("Once — there is a single instance; `'LegacyCache'` is just an alias for the `CacheService` provider", "একবার — একটাই instance; `'LegacyCache'` শুধু `CacheService` provider-এর একটা alias"),
            ("Once, but `'LegacyCache'` receives a fresh `new CacheService()` without the TTL", "একবার, কিন্তু `'LegacyCache'` TTL ছাড়া একটা নতুন `new CacheService()` পায়"),
            ("Zero until the first HTTP request, because factory providers are created lazily", "প্রথম HTTP request পর্যন্ত শূন্য, কারণ factory provider lazy ভাবে তৈরি হয়"),
        ],
        correct=1,
        a_en=r"""Once, with one instance. `useExisting` creates an alias: the token `'LegacyCache'` resolves to whatever the `CacheService` token resolves to. The factory runs once at bootstrap because the provider is a default-scoped singleton.""",
        a_bn=r"""একবার, আর একটাই instance। `useExisting` একটা alias তৈরি করে: `'LegacyCache'` token resolve হয় `CacheService` token যা resolve করে ঠিক সেটাতেই। Provider default-scope singleton বলে factory bootstrap-এর সময় একবারই চলে।""",
        quick_en=r"""The factory runs once and there is one `CacheService` instance: `useExisting` makes `'LegacyCache'` an alias that resolves to the same singleton as the `CacheService` token.""",
        quick_bn=r"""Factory একবারই চলে, আর `CacheService`-এর instance একটাই: `useExisting` দিয়ে `'LegacyCache'` শুধু একটা alias, যেটা `CacheService` token-এর একই singleton-এ resolve হয়।""",
        ex_en=r"""
            The four custom provider forms:
            - `useValue` — a constant or a mock object (great for tests and config).
            - `useClass` — choose an implementation class, e.g. `{ provide: PaymentGateway, useClass: process.env.NODE_ENV === 'test' ? FakeGateway : BkashGateway }`.
            - `useFactory` + `inject` — build the instance from other providers; can be `async` (e.g. open a DB connection before the app starts).
            - `useExisting` — alias one token to another provider, sharing the same instance.

            Option A is the tempting mistake: people assume each token means a new object. If you **wanted** two instances, you'd use two `useFactory` providers. Option D is wrong because singletons are instantiated at bootstrap (an async factory even delays startup until it resolves).

            Non-class tokens (strings or, better, exported `Symbol`s / `InjectionToken`s) require `@Inject(TOKEN)` at the injection site.
        """,
        ex_bn=r"""
            Custom provider-এর চার ধরন:
            - `useValue` — একটা constant বা mock object (test আর config-এর জন্য দারুণ)।
            - `useClass` — implementation class বেছে নেওয়া, যেমন `{ provide: PaymentGateway, useClass: process.env.NODE_ENV === 'test' ? FakeGateway : BkashGateway }`।
            - `useFactory` + `inject` — অন্য provider থেকে instance বানানো; `async` হতে পারে (যেমন app চালুর আগে DB connection খোলা)।
            - `useExisting` — একটা token-কে অন্য provider-এর alias বানানো, একই instance share হয়।

            Option A হলো লোভনীয় ভুল: অনেকে ভাবে প্রতিটা token মানে নতুন object। যদি সত্যিই দুটো instance **চাইতে**, তাহলে দুটো `useFactory` provider লাগত। Option D ভুল, কারণ singleton bootstrap-এর সময়ই তৈরি হয় (async factory হলে তো startup-ই অপেক্ষা করে)।

            Class নয় এমন token (string, বা আরও ভালো exported `Symbol` / `InjectionToken`) হলে inject করার জায়গায় `@Inject(TOKEN)` লাগে।
        """,
        tip_en=r"""Name all four forms quickly and give one real use for each — `useClass` for swapping a payment gateway in tests is a nice concrete example.""",
        tip_bn=r"""চারটা ধরনই দ্রুত বলো আর প্রতিটার একটা বাস্তব ব্যবহার দাও — test-এ payment gateway বদলাতে `useClass` একটা ভালো concrete example।""",
        related=["nest-003", "nest-019"],
        refs=[NEST_CUSTOM_PROVIDERS],
    ),
    # ------------------------------------------------------------------ nest-019
    Q(
        id="nest-019", sub="Dynamic Modules", diff="medium", type="conceptual",
        prio="medium", market="both", mins=5,
        tags=["dynamic-modules", "forroot", "forrootasync", "global-modules"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""What is a dynamic module in NestJS? Explain `forRoot()`, `forRootAsync()` and `forFeature()`, and when you'd make a module global.""",
        q_bn=r"""NestJS-এ dynamic module কী? `forRoot()`, `forRootAsync()` আর `forFeature()` ব্যাখ্যা করো, আর কখন একটা module-কে global করবে?""",
        a_en=r"""
            A normal module has fixed metadata. A **dynamic module** is returned by a static method, so its providers can depend on options passed by the importer — that's how reusable modules like `ConfigModule`, `JwtModule` or `TypeOrmModule` are configured.

            - `forRoot(options)` — configure once for the whole app (connection string, API key).
            - `forRootAsync({ imports, inject, useFactory })` — same, but the options come from other providers, typically `ConfigService`, so secrets aren't hard-coded and are read after config is validated.
            - `forFeature(...)` — per-feature configuration of an already-configured module, e.g. `TypeOrmModule.forFeature([User])` registers repositories for one feature module.

            Setting `global: true` on the returned module (or `@Global()`) makes its exports available everywhere. I reserve that for true infrastructure: config, database, logger, mail.
        """,
        a_bn=r"""
            সাধারণ module-এর metadata স্থির থাকে। **Dynamic module** একটা static method থেকে return হয়, তাই এর provider গুলো importer-এর দেওয়া option-এর উপর নির্ভর করতে পারে — `ConfigModule`, `JwtModule` বা `TypeOrmModule`-এর মতো reusable module এভাবেই configure হয়।

            - `forRoot(options)` — পুরো app-এর জন্য একবার configure করা (connection string, API key)।
            - `forRootAsync({ imports, inject, useFactory })` — একই কাজ, কিন্তু option আসে অন্য provider থেকে, সাধারণত `ConfigService`; তাই secret hard-code হয় না, আর config validate হওয়ার পরে পড়া হয়।
            - `forFeature(...)` — আগেই configure করা module-এর per-feature configuration, যেমন `TypeOrmModule.forFeature([User])` একটা feature module-এর জন্য repository register করে।

            Return করা module-এ `global: true` (বা `@Global()`) দিলে এর export সব জায়গায় পাওয়া যায়। আমি এটা শুধু আসল infrastructure-এর জন্য রাখি: config, database, logger, mail।
        """,
        quick_en=r"""A dynamic module is returned by a static method, so its providers can depend on options from the importer: `forRoot()` configures it once, `forRootAsync()` takes options from providers like `ConfigService`, and `forFeature()` adds per-feature setup. Make only real infrastructure, like config, global.""",
        quick_bn=r"""Dynamic module একটা static method থেকে return হয়, তাই এর provider import করা module-এর দেওয়া option-এর উপর নির্ভর করতে পারে: `forRoot()` একবার configure করে, `forRootAsync()` `ConfigService`-এর মতো provider থেকে option নেয়, আর `forFeature()` প্রতিটা feature-এর আলাদা setup দেয়। Global করি শুধু config-এর মতো আসল infrastructure-কে।""",
        ex_en=r"""
            - Under the hood, a dynamic module is just `{ module, providers, exports, imports, global }`. Options are usually exposed as a provider under a token (`MAIL_OPTIONS`) that the module's services inject.
            - `forRootAsync` supports `useFactory`, `useClass` and `useExisting`; the factory can be `async`.
            - `ConfigurableModuleBuilder` generates `forRoot`/`forRootAsync` (or `register`/`registerAsync`) boilerplate for you, including the options token and types.
            - Naming convention: `forRoot` = configure once, `register` = a configured instance per importer, `forFeature` = extra config for a feature.
            - Too many global modules hide dependencies and make modules hard to extract later (e.g. into a microservice).
        """,
        ex_bn=r"""
            - ভেতরে ভেতরে dynamic module শুধু একটা `{ module, providers, exports, imports, global }` object। Option গুলো সাধারণত একটা token-এর (`MAIL_OPTIONS`) অধীনে provider হিসেবে থাকে, module-এর service গুলো সেটা inject করে।
            - `forRootAsync`, `useFactory`, `useClass` আর `useExisting` support করে; factory `async` হতে পারে।
            - `ConfigurableModuleBuilder` তোমার জন্য `forRoot`/`forRootAsync` (বা `register`/`registerAsync`)-এর boilerplate, options token আর type সহ generate করে দেয়।
            - নামকরণের রীতি: `forRoot` = একবার configure, `register` = প্রতিটা importer-এর জন্য configured instance, `forFeature` = feature-এর জন্য বাড়তি config।
            - বেশি global module dependency লুকিয়ে ফেলে, আর পরে module আলাদা করা (যেমন microservice-এ) কঠিন হয়।
        """,
        tip_en=r"""Use a familiar example: "`TypeOrmModule.forRootAsync()` once in `AppModule`, `forFeature([User])` in `UsersModule`". Then show you could write your own — that's what separates users from builders.""",
        tip_bn=r"""পরিচিত example দাও: "`AppModule`-এ একবার `TypeOrmModule.forRootAsync()`, আর `UsersModule`-এ `forFeature([User])`"। তারপর দেখাও তুমি নিজেও লিখতে পারো — এটাই user আর builder-এর পার্থক্য।""",
        mist_en=r"""Reading `process.env` directly inside `forRoot()` instead of using `forRootAsync` with `ConfigService`; marking every shared module global; forgetting to export the service from the dynamic module.""",
        mist_bn=r"""`ConfigService` সহ `forRootAsync` ব্যবহার না করে `forRoot()`-এর ভেতরে সরাসরি `process.env` পড়া; প্রতিটা shared module global করে দেওয়া; dynamic module থেকে service export করতে ভুলে যাওয়া।""",
        code=r"""
            import { DynamicModule, Inject, Injectable, InjectionToken, Module, ModuleMetadata, OptionalFactoryDependency } from '@nestjs/common';

            export interface MailOptions { apiKey: string; from: string }
            export const MAIL_OPTIONS = Symbol('MAIL_OPTIONS');

            @Injectable()
            export class MailService {
              constructor(@Inject(MAIL_OPTIONS) private readonly options: MailOptions) {}
            }

            @Module({})
            export class MailModule {
              static forRootAsync(options: {
                imports?: ModuleMetadata['imports'];
                inject?: (InjectionToken | OptionalFactoryDependency)[];
                useFactory: (...args: any[]) => MailOptions | Promise<MailOptions>;
              }): DynamicModule {
                return {
                  module: MailModule,
                  global: true,
                  imports: options.imports ?? [],
                  providers: [
                    { provide: MAIL_OPTIONS, useFactory: options.useFactory, inject: options.inject ?? [] },
                    MailService,
                  ],
                  exports: [MailService],
                };
              }
            }

            // app.module.ts
            MailModule.forRootAsync({
              inject: [ConfigService],
              useFactory: (config: ConfigService) => ({
                apiKey: config.getOrThrow<string>('MAIL_API_KEY'),
                from: 'no-reply@shop.example',
              }),
            });
        """,
        lang="typescript",
        follow=[
            ("What does `ConfigurableModuleBuilder` generate for you?", "`ConfigurableModuleBuilder` তোমার জন্য কী generate করে?"),
            ("How would you register the same module twice with different options (two databases)?", "একই module ভিন্ন option দিয়ে দুবার (দুটো database) কীভাবে register করবে?"),
        ],
        related=["nest-001", "nest-018", "nest-022"],
        refs=[NEST_DYNAMIC],
    ),
    # ------------------------------------------------------------------ nest-020
    Q(
        id="nest-020", sub="Testing", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["testing", "unit-tests", "e2e", "mocking", "supertest"],
        ver="NestJS 12.1 (@nestjs/testing; new ESM projects use Vitest, CJS projects Jest)", vs=True, status="stable",
        q_en=r"""
            `UsersService.findOne(id)` calls an injected repository (token `USERS_REPOSITORY`) and throws `NotFoundException` when the user doesn't exist.

            1. Write unit tests for both cases using `Test.createTestingModule()` and a mocked repository.
            2. Show how an e2e test boots the full `AppModule` but replaces the real `MailService`, then checks that `POST /users` with an invalid email returns 400.
        """,
        q_bn=r"""
            `UsersService.findOne(id)` একটা inject করা repository (token `USERS_REPOSITORY`) call করে, আর user না থাকলে `NotFoundException` throw করে।

            1. `Test.createTestingModule()` আর একটা mock repository দিয়ে দুটো case-এর unit test লেখো।
            2. দেখাও একটা e2e test কীভাবে পুরো `AppModule` চালু করে কিন্তু আসল `MailService` বদলে দেয়, তারপর check করে যে invalid email দিয়ে `POST /users` করলে 400 আসে।
        """,
        a_en=r"""
            - **Unit test:** build a small testing module with only `UsersService` plus `{ provide: USERS_REPOSITORY, useValue: repoMock }`. Nest's real DI wires it, but nothing touches a database. Then assert both the happy path and that `findOne(42)` rejects with `NotFoundException`.
            - **E2E test:** `Test.createTestingModule({ imports: [AppModule] })`, then `.overrideProvider(MailService).useValue(mailMock)` before `.compile()`. Create the app with `createNestApplication()`, apply the same global setup as `main.ts` (pipes, prefix), `await app.init()`, and drive it with `supertest` via `app.getHttpServer()`. Close the app in `afterAll`.

            In NestJS 12, new ESM projects come with Vitest (`vi.fn()`, globals enabled); CommonJS projects use Jest (`jest.fn()`). The Nest testing API is the same in both.
        """,
        a_bn=r"""
            - **Unit test:** শুধু `UsersService` আর `{ provide: USERS_REPOSITORY, useValue: repoMock }` দিয়ে একটা ছোট testing module বানাও। Nest-এর আসল DI জোড়া লাগায়, কিন্তু database-এ কিছুই যায় না। তারপর happy path আর `findOne(42)` যে `NotFoundException` দিয়ে reject করে — দুটোই assert করো।
            - **E2E test:** `Test.createTestingModule({ imports: [AppModule] })`, তারপর `.compile()`-এর আগে `.overrideProvider(MailService).useValue(mailMock)`। `createNestApplication()` দিয়ে app বানাও, `main.ts`-এর মতো একই global setup দাও (pipe, prefix), `await app.init()` করো, আর `app.getHttpServer()` দিয়ে `supertest` চালাও। `afterAll`-এ app close করো।

            NestJS 12-এ নতুন ESM project Vitest দিয়ে আসে (`vi.fn()`, globals চালু); CommonJS project Jest ব্যবহার করে (`jest.fn()`)। দুটোতেই Nest-এর testing API একই।
        """,
        quick_en=r"""Unit test: `Test.createTestingModule()` with `UsersService` and `{ provide: USERS_REPOSITORY, useValue: mock }`, asserting the found user and the `NotFoundException`. E2E: import `AppModule`, `.overrideProvider(MailService).useValue(mock)`, apply the `main.ts` pipes, and expect 400 from `POST /users` via supertest.""",
        quick_bn=r"""Unit test-এ `Test.createTestingModule()`-এ `UsersService` আর `{ provide: USERS_REPOSITORY, useValue: mock }` দিয়ে found user আর `NotFoundException` দুটোই check করি। E2E-তে `AppModule` import করে `.overrideProvider(MailService).useValue(mock)` দিই, `main.ts`-এর মতো pipe লাগাই, তারপর supertest দিয়ে `POST /users` পাঠিয়ে 400 আশা করি।""",
        ex_en=r"""
            - **Biggest e2e gotcha:** anything configured in `main.ts` (`app.useGlobalPipes(...)`, `setGlobalPrefix`, `enableVersioning`) does **not** exist in the test app unless you repeat it. Registering pipes/guards via `APP_PIPE`/`APP_GUARD` providers avoids the duplication, because they live inside the module graph.
            - Reset mocks between tests (`vi.resetAllMocks()` / `jest.resetAllMocks()`) so state doesn't leak.
            - Mock at the boundary you own (repository, mail, payment gateway) — not `UsersService` internals.
            - For DB-heavy logic, add integration tests against a real PostgreSQL (e.g. a disposable Docker container) — mocks can't catch wrong SQL or constraint errors.
            - Use `moduleRef.resolve()` instead of `get()` for request-scoped or transient providers.
        """,
        ex_bn=r"""
            - **E2E-র সবচেয়ে বড় ফাঁদ:** `main.ts`-এ যা configure করা (`app.useGlobalPipes(...)`, `setGlobalPrefix`, `enableVersioning`) সেটা test app-এ **থাকে না**, যদি না আবার লেখো। `APP_PIPE`/`APP_GUARD` provider দিয়ে pipe/guard register করলে এই duplication লাগে না, কারণ সেগুলো module graph-এর ভেতরে থাকে।
            - Test-এর মাঝে mock reset করো (`vi.resetAllMocks()` / `jest.resetAllMocks()`), যাতে state এক test থেকে আরেকটায় না যায়।
            - নিজের boundary-তে mock করো (repository, mail, payment gateway) — `UsersService`-এর ভেতরের জিনিস না।
            - DB-heavy logic-এর জন্য আসল PostgreSQL-এর বিরুদ্ধে integration test যোগ করো (যেমন disposable Docker container) — mock ভুল SQL বা constraint error ধরতে পারে না।
            - Request-scoped বা transient provider-এর জন্য `get()`-এর বদলে `moduleRef.resolve()` ব্যবহার করো।
        """,
        tip_en=r"""Separate the two levels clearly: unit = one class, mocked dependencies; e2e = whole app over HTTP with only external services replaced. Then mention the `main.ts` setup gotcha — it's a classic "my e2e test passes but prod fails" story.""",
        tip_bn=r"""দুই level পরিষ্কার আলাদা করো: unit = একটা class, dependency mock; e2e = HTTP দিয়ে পুরো app, শুধু external service বদলানো। তারপর `main.ts` setup-এর ফাঁদটা বলো — "e2e test pass করে কিন্তু prod-এ fail" ধরনের classic গল্প এটা।""",
        mist_en=r"""Forgetting `await app.close()` (open handles, hanging test runs); not re-applying global pipes in e2e tests; mocking so much that the test only checks the mocks.""",
        mist_bn=r"""`await app.close()` ভুলে যাওয়া (open handle, test run আটকে থাকে); e2e test-এ global pipe আবার না দেওয়া; এত বেশি mock করা যে test শুধু mock-কেই check করে।""",
        code=r"""
            // users.service.ts
            export const USERS_REPOSITORY = Symbol('USERS_REPOSITORY');
            export interface UsersRepository {
              findById(id: number): Promise<{ id: number; email: string } | undefined>;
            }

            @Injectable()
            export class UsersService {
              constructor(@Inject(USERS_REPOSITORY) private readonly repo: UsersRepository) {}

              async findOne(id: number) {
                const user = await this.repo.findById(id);
                if (!user) throw new NotFoundException(`User ${id} not found`);
                return user;
              }
            }

            // users.service.spec.ts — Vitest with globals (Jest: replace vi.fn with jest.fn)
            import { Test } from '@nestjs/testing';
            import { NotFoundException } from '@nestjs/common';
            import { UsersService, USERS_REPOSITORY, type UsersRepository } from './users.service.js';

            describe('UsersService', () => {
              let service: UsersService;
              const repo = { findById: vi.fn<UsersRepository['findById']>() };

              beforeEach(async () => {
                vi.resetAllMocks();
                const moduleRef = await Test.createTestingModule({
                  providers: [UsersService, { provide: USERS_REPOSITORY, useValue: repo }],
                }).compile();
                service = moduleRef.get(UsersService);
              });

              it('returns the user when it exists', async () => {
                repo.findById.mockResolvedValue({ id: 1, email: 'a@b.co' });
                await expect(service.findOne(1)).resolves.toEqual({ id: 1, email: 'a@b.co' });
                expect(repo.findById).toHaveBeenCalledWith(1);
              });

              it('throws NotFoundException when the user is missing', async () => {
                repo.findById.mockResolvedValue(undefined);
                await expect(service.findOne(42)).rejects.toBeInstanceOf(NotFoundException);
              });
            });
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="E2E test with a replaced provider", label_bn="Provider বদলে e2e test", src=r"""
                // test/users.e2e-spec.ts
                import { Test } from '@nestjs/testing';
                import { INestApplication, ValidationPipe } from '@nestjs/common';
                import request from 'supertest';
                import { AppModule } from '../src/app.module.js';
                import { MailService } from '../src/mail/mail.service.js';

                describe('Users (e2e)', () => {
                  let app: INestApplication;
                  const mail = { send: vi.fn() };

                  beforeAll(async () => {
                    const moduleRef = await Test.createTestingModule({ imports: [AppModule] })
                      .overrideProvider(MailService)
                      .useValue(mail)
                      .compile();

                    app = moduleRef.createNestApplication();
                    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true })); // same as main.ts
                    await app.init();
                  });

                  afterAll(async () => {
                    await app.close();
                  });

                  it('POST /users rejects an invalid email', () =>
                    request(app.getHttpServer()).post('/users').send({ email: 'nope' }).expect(400));
                });
            """),
        ],
        time="O(1) per test case",
        space="O(1)",
        follow=[
            ("How would you test a guard or an interceptor in isolation?", "একটা guard বা interceptor আলাদাভাবে কীভাবে test করবে?"),
            ("How do you run integration tests against a real PostgreSQL in CI?", "CI-তে আসল PostgreSQL-এর বিরুদ্ধে integration test কীভাবে চালাবে?"),
        ],
        related=["nest-003", "nest-018"],
        refs=[NEST_TESTING],
    ),
    # ------------------------------------------------------------------ nest-021
    Q(
        id="nest-021", sub="Guards vs Middleware", diff="medium", type="comparison",
        prio="high", market="both", mins=5,
        tags=["middleware", "guards", "interceptors", "nestmodule"],
        ver="NestJS 12.1 (Express 5 adapter)", vs=False, status="stable",
        q_en=r"""What's the difference between middleware, guards and interceptors in NestJS? Which would you use for request-id logging, JWT/role checks, and response transformation — and how do you register middleware?""",
        q_bn=r"""NestJS-এ middleware, guard আর interceptor-এর পার্থক্য কী? Request-id logging, JWT/role check আর response transformation-এর জন্য কোনটা ব্যবহার করবে — আর middleware কীভাবে register করো?""",
        a_en=r"""
            - **Middleware** runs first, Express-style `(req, res, next)`. It doesn't know which controller or handler will run, so it's for generic HTTP concerns: request ids, request logging, CORS, cookie parsing, raw body for webhooks. → **request-id logging**.
            - **Guards** run after middleware with an `ExecutionContext`, so they know the target handler and can read metadata such as `@Roles('admin')` or `@Public()`. They only answer yes/no. → **JWT and role checks**.
            - **Interceptors** wrap the handler call (before and after) and can transform the result or errors with RxJS. → **response transformation**, timing, caching.

            Middleware is registered in a module that implements `NestModule`: `configure(consumer)` with `consumer.apply(...).forRoutes(...)`, optionally `.exclude(...)`. Global Express middleware like `helmet()` can also go in `main.ts` via `app.use()`.
        """,
        a_bn=r"""
            - **Middleware** সবার আগে চলে, Express-এর মতো `(req, res, next)`। কোন controller বা handler চলবে এটা জানে না, তাই এটা generic HTTP কাজের জন্য: request id, request logging, CORS, cookie parsing, webhook-এর জন্য raw body। → **Request-id logging**।
            - **Guard** middleware-এর পরে `ExecutionContext` নিয়ে চলে, তাই target handler জানে আর `@Roles('admin')` বা `@Public()`-এর মতো metadata পড়তে পারে। এটা শুধু হ্যাঁ/না উত্তর দেয়। → **JWT আর role check**।
            - **Interceptor** handler call-কে আগে-পরে wrap করে, আর RxJS দিয়ে result বা error transform করতে পারে। → **Response transformation**, timing, caching।

            Middleware register করা হয় `NestModule` implement করা module-এ: `configure(consumer)`-এর ভেতরে `consumer.apply(...).forRoutes(...)`, দরকার হলে `.exclude(...)`। `helmet()`-এর মতো global Express middleware `main.ts`-এ `app.use()` দিয়েও দেওয়া যায়।
        """,
        quick_en=r"""Middleware runs first and doesn't know the handler, so it suits request-id logging; guards know the handler and its metadata and answer yes/no, so they do JWT and role checks; interceptors wrap the handler to transform responses. Register middleware in `configure(consumer)` with `apply().forRoutes()`.""",
        quick_bn=r"""Middleware সবার আগে চলে আর কোন handler চলবে জানে না, তাই request-id logging-এর জন্য ঠিক; guard handler আর তার metadata জানে এবং শুধু হ্যাঁ/না বলে, তাই JWT আর role check; interceptor handler-কে wrap করে response বদলায়। Middleware register হয় `NestModule`-এর `configure(consumer)`-এ `apply().forRoutes()` দিয়ে।""",
        ex_en=r"""
            - **Why not auth in middleware?** You can verify a token there, but you can't cleanly read per-route metadata, you lose `@Public()`-style opt-outs, and it only works for HTTP. Guards also work for WebSockets and microservices.
            - **DI:** class middleware registered through `configure()` supports constructor injection. Middleware added with `app.use()` in `main.ts` is outside the DI container.
            - **Error handling:** guards throw HTTP exceptions that exception filters format; middleware errors are also caught, but middleware has no access to the handler context.
            - **Pipes** are the fourth piece — they validate/transform handler arguments right before the handler runs.
            - A good rule: "Is it about the raw HTTP request? Middleware. Is it a permission decision for a route? Guard. Is it about the handler's input? Pipe. Its output? Interceptor."
        """,
        ex_bn=r"""
            - **Auth middleware-এ কেন না?** Token সেখানে verify করা যায়, কিন্তু per-route metadata পরিষ্কারভাবে পড়া যায় না, `@Public()`-ধরনের opt-out হারাতে হয়, আর শুধু HTTP-তে কাজ করে। Guard WebSocket আর microservice-এও কাজ করে।
            - **DI:** `configure()` দিয়ে register করা class middleware constructor injection support করে। `main.ts`-এ `app.use()` দিয়ে দেওয়া middleware DI container-এর বাইরে থাকে।
            - **Error handling:** guard HTTP exception throw করে যেটা exception filter format করে; middleware-এর error-ও ধরা হয়, কিন্তু middleware handler context পায় না।
            - **Pipe** হলো চতুর্থ অংশ — handler চলার ঠিক আগে argument validate/transform করে।
            - ভালো একটা নিয়ম: "Raw HTTP request নিয়ে? Middleware। Route-এর permission-এর সিদ্ধান্ত? Guard। Handler-এর input? Pipe। Output? Interceptor।"
        """,
        tip_en=r"""Give the one-line rule at the end ("raw request → middleware, permission → guard, input → pipe, output → interceptor"). It shows you have a mental model, not a memorised list.""",
        tip_bn=r"""শেষে এক লাইনের নিয়মটা বলো ("raw request → middleware, permission → guard, input → pipe, output → interceptor")। এতে বোঝা যায় তোমার একটা mental model আছে, শুধু মুখস্থ list না।""",
        mist_en=r"""Doing authorization in middleware; trying to read `@Roles()` metadata in middleware; expecting `app.use()` middleware to receive injected services.""",
        mist_bn=r"""Middleware-এ authorization করা; middleware-এ `@Roles()` metadata পড়ার চেষ্টা করা; আশা করা যে `app.use()` middleware inject করা service পাবে।""",
        code=r"""
            import { Injectable, MiddlewareConsumer, Module, NestMiddleware, NestModule, RequestMethod } from '@nestjs/common';
            import { randomUUID } from 'node:crypto';
            import type { NextFunction, Request, Response } from 'express';

            @Injectable()
            export class RequestIdMiddleware implements NestMiddleware {
              use(req: Request, res: Response, next: NextFunction) {
                const id = req.header('x-request-id') ?? randomUUID();
                res.setHeader('x-request-id', id);
                next();
              }
            }

            @Module({ /* imports, controllers, providers */ })
            export class AppModule implements NestModule {
              configure(consumer: MiddlewareConsumer) {
                consumer
                  .apply(RequestIdMiddleware)
                  .exclude({ path: 'health', method: RequestMethod.GET })
                  .forRoutes('*');
              }
            }
        """,
        lang="typescript",
        follow=[
            ("Why can't a guard read the validated DTO?", "Guard কেন validated DTO পড়তে পারে না?"),
            ("How would you capture the raw request body for webhook signature verification?", "Webhook signature verify করার জন্য raw request body কীভাবে পাবে?"),
        ],
        related=["nest-007", "nest-012", "nest-013"],
        refs=[NEST_MIDDLEWARE, NEST_GUARDS],
    ),
    # ------------------------------------------------------------------ nest-022
    Q(
        id="nest-022", sub="Database Integration", diff="medium", type="scenario",
        prio="high", market="both", mins=8,
        tags=["database", "drizzle", "custom-providers", "connection-pool", "shutdown"],
        ver="NestJS 12.1 / Drizzle ORM 0.45 / pg 8", vs=True, status="stable",
        q_en=r"""Your team chose Drizzle ORM with PostgreSQL for a NestJS 12 API. How would you integrate it so repositories can inject the database, the connection pool is configured from environment variables, and connections close cleanly on shutdown? How does this compare with TypeORM or Prisma integration?""",
        q_bn=r"""তোমার team একটা NestJS 12 API-র জন্য PostgreSQL সহ Drizzle ORM বেছে নিয়েছে। কীভাবে integrate করবে যাতে repository database inject করতে পারে, connection pool environment variable থেকে configure হয়, আর shutdown-এর সময় connection ঠিকভাবে বন্ধ হয়? TypeORM বা Prisma integration-এর সাথে এটা কেমন?""",
        a_en=r"""
            **Approach:** a global `DatabaseModule` with custom providers.
            1. A `PG_POOL` provider built with `useFactory` from `ConfigService` (`DATABASE_URL`, pool `max`).
            2. A `DRIZZLE` provider that wraps the pool: `drizzle({ client: pool, schema })` — passing `schema` enables `db.query.*` relational queries.
            3. Export only the `DRIZZLE` token; repositories inject it with `@Inject(DRIZZLE)`.
            4. Implement `OnApplicationShutdown` to call `pool.end()`, and call `app.enableShutdownHooks()` in `main.ts` so SIGTERM from Docker/Kubernetes triggers it.

            Services depend on small repositories, not on Drizzle directly, so they're easy to mock.

            **Alternatives:** NestJS recently published an official `@nestjs/drizzle` package (`DrizzleModule.forRoot({ drizzle, connection })`, `@InjectDrizzle()`), but it's very new (0.0.x, Sept 2026) and its docs target the Drizzle v1 RC — fine to evaluate, while the custom provider above works with stable Drizzle 0.45 today. TypeORM has `@nestjs/typeorm` (`forRootAsync` + `forFeature` + `@InjectRepository`), Mongoose has `@nestjs/mongoose`, and Prisma is usually a `PrismaService` provider wrapping the generated client.
        """,
        a_bn=r"""
            **Approach:** custom provider সহ একটা global `DatabaseModule`।
            1. `ConfigService` থেকে (`DATABASE_URL`, pool `max`) `useFactory` দিয়ে বানানো একটা `PG_POOL` provider।
            2. Pool-কে wrap করা একটা `DRIZZLE` provider: `drizzle({ client: pool, schema })` — `schema` দিলে `db.query.*` relational query চালু হয়।
            3. শুধু `DRIZZLE` token export করি; repository গুলো `@Inject(DRIZZLE)` দিয়ে inject করে।
            4. `OnApplicationShutdown` implement করে `pool.end()` call করি, আর `main.ts`-এ `app.enableShutdownHooks()` দিই যাতে Docker/Kubernetes-এর SIGTERM-এ এটা চলে।

            Service গুলো সরাসরি Drizzle-এর উপর না, ছোট repository-র উপর নির্ভর করে, তাই mock করা সহজ।

            **বিকল্প:** NestJS সম্প্রতি একটা official `@nestjs/drizzle` package publish করেছে (`DrizzleModule.forRoot({ drizzle, connection })`, `@InjectDrizzle()`), কিন্তু এটা একদম নতুন (0.0.x, Sept 2026) আর এর docs Drizzle v1 RC লক্ষ্য করে — evaluate করা যায়, তবে উপরের custom provider আজকের stable Drizzle 0.45-এর সাথে কাজ করে। TypeORM-এর আছে `@nestjs/typeorm` (`forRootAsync` + `forFeature` + `@InjectRepository`), Mongoose-এর `@nestjs/mongoose`, আর Prisma সাধারণত generated client wrap করা একটা `PrismaService` provider।
        """,
        quick_en=r"""A global `DatabaseModule` with a `useFactory` pool provider from `ConfigService`, a `DRIZZLE` provider wrapping it for repositories to inject, and `pool.end()` in `OnApplicationShutdown` with `enableShutdownHooks()`. TypeORM and Mongoose have official Nest modules; Prisma is usually a `PrismaService`.""",
        quick_bn=r"""একটা global `DatabaseModule` বানাই: `ConfigService` থেকে `useFactory` দিয়ে pool provider, তার উপর `DRIZZLE` provider (`drizzle({ client: pool, schema })`) যেটা repository inject করে, আর `enableShutdownHooks()`-সহ `OnApplicationShutdown`-এ `pool.end()`। TypeORM আর Mongoose-এর official Nest module আছে; Prisma সাধারণত একটা `PrismaService` provider।""",
        ex_en=r"""
            - **Pool sizing:** total connections = pool `max` × number of app instances. Ten pods with `max: 20` = 200 connections, which can exceed PostgreSQL's `max_connections`. Use PgBouncer or a managed pooler when you scale out.
            - **Pool errors:** node-postgres emits `error` on the pool when an idle connection drops (DB restart, failover). Attach a listener (`pool.on('error', ...)`) so it's logged instead of crashing the process.
            - **Transactions across services:** either pass the `tx` object explicitly to repository methods, or use a request-context library (e.g. `nestjs-cls` with a transactional plugin) so nested calls share one transaction.
            - **Migrations** run as a separate deployment step (`drizzle-kit migrate`), not on every app start in a multi-instance deployment.
            - Exporting a typed `Database` alias (`NodePgDatabase<typeof schema>`) keeps `db.query.users` fully typed in every repository.
        """,
        ex_bn=r"""
            - **Pool sizing:** মোট connection = pool `max` × app instance সংখ্যা। ১০টা pod আর `max: 20` = ২০০ connection, যা PostgreSQL-এর `max_connections` ছাড়িয়ে যেতে পারে। Scale out করলে PgBouncer বা managed pooler ব্যবহার করো।
            - **Pool error:** idle connection কেটে গেলে (DB restart, failover) node-postgres pool-এ `error` emit করে। একটা listener লাগাও (`pool.on('error', ...)`), যাতে process crash না করে log হয়।
            - **একাধিক service জুড়ে transaction:** হয় repository method-এ `tx` object explicitly pass করো, নয়তো request-context library (যেমন transactional plugin সহ `nestjs-cls`) ব্যবহার করো, যাতে nested call একই transaction share করে।
            - **Migration** আলাদা deployment step হিসেবে চলে (`drizzle-kit migrate`), multi-instance deployment-এ প্রতিবার app start-এ না।
            - একটা typed `Database` alias (`NodePgDatabase<typeof schema>`) export করলে প্রতিটা repository-তে `db.query.users` পুরোপুরি typed থাকে।
        """,
        tip_en=r"""Structure it as: provider design → injection → lifecycle (shutdown hooks) → scaling (pool × instances). Mentioning `enableShutdownHooks()` and connection math shows production experience.""",
        tip_bn=r"""এভাবে সাজাও: provider design → injection → lifecycle (shutdown hook) → scaling (pool × instance)। `enableShutdownHooks()` আর connection-এর হিসাব বললে production অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Creating a new `Pool` inside every repository; forgetting `enableShutdownHooks()` so `pool.end()` never runs; running migrations on startup from every replica; injecting the raw pool everywhere instead of a typed Drizzle instance.""",
        mist_bn=r"""প্রতিটা repository-র ভেতরে নতুন `Pool` বানানো; `enableShutdownHooks()` ভুলে যাওয়া, ফলে `pool.end()` কখনো চলে না; প্রতিটা replica থেকে startup-এ migration চালানো; typed Drizzle instance-এর বদলে সব জায়গায় raw pool inject করা।""",
        code=r"""
            // database/database.module.ts
            import { Global, Inject, Module, OnApplicationShutdown } from '@nestjs/common';
            import { ConfigService } from '@nestjs/config';
            import { drizzle, type NodePgDatabase } from 'drizzle-orm/node-postgres';
            import { Pool } from 'pg';
            import * as schema from './schema.js';

            export const PG_POOL = Symbol('PG_POOL');
            export const DRIZZLE = Symbol('DRIZZLE');
            export type Database = NodePgDatabase<typeof schema>;

            @Global()
            @Module({
              providers: [
                {
                  provide: PG_POOL,
                  inject: [ConfigService],
                  useFactory: (config: ConfigService) =>
                    new Pool({ connectionString: config.getOrThrow<string>('DATABASE_URL'), max: 10 }),
                },
                {
                  provide: DRIZZLE,
                  inject: [PG_POOL],
                  useFactory: (pool: Pool): Database => drizzle({ client: pool, schema }),
                },
              ],
              exports: [DRIZZLE],
            })
            export class DatabaseModule implements OnApplicationShutdown {
              constructor(@Inject(PG_POOL) private readonly pool: Pool) {}

              async onApplicationShutdown() {
                await this.pool.end();
              }
            }

            // users/users.repository.ts
            @Injectable()
            export class UsersRepository {
              constructor(@Inject(DRIZZLE) private readonly db: Database) {}

              findByEmail(email: string) {
                return this.db.query.users.findFirst({ where: eq(schema.users.email, email) });
              }
            }

            // main.ts
            app.enableShutdownHooks(); // SIGTERM -> onApplicationShutdown -> pool.end()
        """,
        lang="typescript",
        follow=[
            ("How would you run a transaction that spans two repositories?", "দুটো repository জুড়ে একটা transaction কীভাবে চালাবে?"),
            ("What changes if the app runs on serverless (e.g. AWS Lambda)?", "App serverless-এ (যেমন AWS Lambda) চললে কী বদলাবে?"),
        ],
        related=["nest-019", "drizzle-003", "drizzle-023"],
        refs=[NEST_DRIZZLE, NEST_LIFECYCLE_EVENTS, DRIZZLE_PG],
    ),
    # ------------------------------------------------------------------ nest-023
    Q(
        id="nest-023", sub="Dependency Injection Scopes", diff="hard", type="conceptual",
        prio="medium", market="both", mins=8,
        tags=["request-scope", "scope-bubbling", "asynclocalstorage", "durable-providers", "performance"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""A teammate makes a `RequestContext` provider `Scope.REQUEST` so services can read the current tenant and request id. What happens to the classes that depend on it, what does it cost, and what alternatives would you consider?""",
        q_bn=r"""একজন teammate একটা `RequestContext` provider-কে `Scope.REQUEST` করেছে যাতে service গুলো current tenant আর request id পড়তে পারে। এর উপর নির্ভরশীল class গুলোর কী হয়, খরচ কী, আর কী কী বিকল্প ভাববে?""",
        a_en=r"""
            **Scope bubbles up.** Any provider that injects a request-scoped provider becomes request-scoped too, and so does every controller above it. In the example, `InvoicesService` and `InvoicesController` are declared as singletons but are now re-created on **every request** — their whole dependency subtree is instantiated per request.

            **Cost:** extra allocations and GC pressure on hot paths, slower requests, and surprises: request-scoped providers can't be used in places with no request (cron jobs, queue consumers, `onModuleInit`), and WebSocket gateways must stay singletons.

            **Alternatives:**
            - **AsyncLocalStorage** (Node's `node:async_hooks`, or `nestjs-cls`): middleware starts a context per request, singletons read it anywhere. No DI scope change, very low overhead. My default for request ids, tenant ids and the current user.
            - **Pass data explicitly** as method arguments — simplest and most testable when only a few calls need it.
            - **Durable providers** (`durable: true` + a `ContextIdStrategy`) when you truly need per-tenant instances (e.g. a tenant-specific DB connection): Nest creates one sub-tree per tenant and reuses it instead of per request.

            This is advanced material: in interviews, the key point is "scope bubbling" and its performance impact.
        """,
        a_bn=r"""
            **Scope উপরের দিকে bubble করে।** যে provider একটা request-scoped provider inject করে, সেটাও request-scoped হয়ে যায়, আর তার উপরের প্রতিটা controller-ও। Example-এ `InvoicesService` আর `InvoicesController` singleton হিসেবে declare করা, কিন্তু এখন **প্রতিটা request-এ** আবার তৈরি হয় — পুরো dependency subtree per request instantiate হয়।

            **খরচ:** hot path-এ বাড়তি allocation আর GC pressure, ধীর request, আর কিছু অবাক করা ব্যাপার: যেখানে request নেই (cron job, queue consumer, `onModuleInit`) সেখানে request-scoped provider ব্যবহার করা যায় না, আর WebSocket gateway-কে singleton-ই থাকতে হয়।

            **বিকল্প:**
            - **AsyncLocalStorage** (Node-এর `node:async_hooks`, বা `nestjs-cls`): middleware প্রতিটা request-এর জন্য একটা context শুরু করে, singleton যেকোনো জায়গা থেকে পড়তে পারে। DI scope বদলায় না, overhead খুব কম। Request id, tenant id আর current user-এর জন্য এটাই আমার default।
            - **Data explicitly pass করা** method argument হিসেবে — অল্প কয়েকটা call-এ দরকার হলে সবচেয়ে সহজ আর testable।
            - **Durable provider** (`durable: true` + একটা `ContextIdStrategy`) যখন সত্যিই per-tenant instance দরকার (যেমন tenant-specific DB connection): Nest প্রতি tenant-এ একটা sub-tree বানিয়ে reuse করে, প্রতি request-এ না।

            এটা advanced বিষয়: interview-এ মূল কথা হলো "scope bubbling" আর এর performance প্রভাব।
        """,
        quick_en=r"""Request scope bubbles up: every provider and controller that depends on it also becomes request-scoped and is re-created per request, costing latency and breaking use in cron jobs or queue workers. Prefer AsyncLocalStorage (`nestjs-cls`), explicit arguments, or durable providers for per-tenant instances.""",
        quick_bn=r"""Request scope উপরের দিকে ছড়িয়ে পড়ে: যারা এর উপর নির্ভর করে সেই সব provider আর controller-ও request-scoped হয়ে প্রতি request-এ নতুন করে তৈরি হয় — বাড়তি allocation আর latency, আর cron job বা queue worker-এ ব্যবহারই করা যায় না। এর বদলে AsyncLocalStorage (`nestjs-cls`), explicit argument, বা per-tenant instance-এর জন্য durable provider ভালো।""",
        ex_en=r"""
            - **Transient is different:** a singleton that injects a `TRANSIENT` provider gets its own fresh instance but **stays** a singleton — transient scope does not bubble the same way.
            - **How to verify:** add a counter in a controller constructor; with a request-scoped dependency it increments on every request.
            - **ALS correctness:** call `als.run(store, () => next())` in middleware so the whole async chain (awaits, promises) sees the same store. Don't mutate a shared object across requests.
            - **Durable providers caveat:** they're powerful for multi-tenancy, but the tenant id must come from a trusted source (verified JWT claim or a validated subdomain), not a raw header, and you must bound the number of cached sub-trees.
            - `moduleRef.resolve()` (not `get()`) is required to obtain request-scoped/transient instances manually.
        """,
        ex_bn=r"""
            - **Transient আলাদা:** একটা singleton যদি `TRANSIENT` provider inject করে, সে নিজের নতুন instance পায়, কিন্তু নিজে singleton-ই **থাকে** — transient scope একইভাবে bubble করে না।
            - **কীভাবে যাচাই করবে:** controller-এর constructor-এ একটা counter রাখো; request-scoped dependency থাকলে প্রতিটা request-এ সেটা বাড়বে।
            - **ALS-এর সঠিকতা:** middleware-এ `als.run(store, () => next())` call করো, যাতে পুরো async chain (await, promise) একই store দেখে। Request-এর মধ্যে shared object mutate কোরো না।
            - **Durable provider-এর সতর্কতা:** multi-tenancy-র জন্য শক্তিশালী, কিন্তু tenant id অবশ্যই বিশ্বস্ত source থেকে আসতে হবে (verified JWT claim বা validated subdomain), raw header থেকে না; আর cache করা sub-tree-র সংখ্যা সীমিত রাখতে হবে।
            - Request-scoped/transient instance নিজে নিতে হলে `get()` না, `moduleRef.resolve()` লাগে।
        """,
        tip_en=r"""Say "scope bubbling" explicitly and quantify the effect ("the controller and every service in between are now built per request"). Offering AsyncLocalStorage as the fix shows you've hit this in production.""",
        tip_bn=r""""Scope bubbling" কথাটা স্পষ্ট করে বলো আর প্রভাবটা বোঝাও ("controller আর মাঝখানের সব service এখন per request তৈরি হয়")। সমাধান হিসেবে AsyncLocalStorage বললে বোঝা যায় তুমি production-এ এই সমস্যায় পড়েছ।""",
        mist_en=r"""Believing only the request-scoped provider itself is re-created; storing per-request data in a singleton field; using request scope just to read the current user; injecting request-scoped providers into gateways or cron jobs.""",
        mist_bn=r"""ভাবা যে শুধু request-scoped provider-টাই আবার তৈরি হয়; singleton-এর field-এ per-request data রাখা; শুধু current user পড়ার জন্য request scope ব্যবহার করা; gateway বা cron job-এ request-scoped provider inject করা।""",
        code=r"""
            import { Controller, Inject, Injectable, Scope } from '@nestjs/common';
            import { REQUEST } from '@nestjs/core';
            import type { Request } from 'express';

            @Injectable({ scope: Scope.REQUEST })
            export class RequestContext {
              constructor(@Inject(REQUEST) private readonly req: Request) {}
              get tenantId() {
                return this.req.header('x-tenant-id');
              }
            }

            @Injectable() // declared singleton...
            export class InvoicesService {
              constructor(private readonly ctx: RequestContext) {} // ...but now request-scoped
            }

            @Controller('invoices') // also re-created for every request
            export class InvoicesController {
              constructor(private readonly invoices: InvoicesService) {}
            }
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="Alternative: AsyncLocalStorage (singletons stay singletons)", label_bn="বিকল্প: AsyncLocalStorage (singleton singleton-ই থাকে)", src=r"""
                import { Injectable, NestMiddleware } from '@nestjs/common';
                import { AsyncLocalStorage } from 'node:async_hooks';
                import { randomUUID } from 'node:crypto';
                import type { NextFunction, Request, Response } from 'express';

                export interface RequestStore { requestId: string; tenantId?: string }
                export const requestContext = new AsyncLocalStorage<RequestStore>();

                @Injectable()
                export class RequestContextMiddleware implements NestMiddleware {
                  use(req: Request, _res: Response, next: NextFunction) {
                    // in real code, take tenantId from the verified JWT, not a raw header
                    requestContext.run({ requestId: randomUUID(), tenantId: req.header('x-tenant-id') }, () => next());
                  }
                }

                @Injectable() // singleton
                export class AuditService {
                  record(action: string) {
                    const store = requestContext.getStore(); // works after any number of awaits
                    return { action, requestId: store?.requestId, tenantId: store?.tenantId };
                  }
                }
            """),
        ],
        follow=[
            ("How do durable providers and `ContextIdStrategy` work for multi-tenancy?", "Multi-tenancy-র জন্য durable provider আর `ContextIdStrategy` কীভাবে কাজ করে?"),
            ("How does AsyncLocalStorage keep context across `await`?", "AsyncLocalStorage কীভাবে `await` পার হয়েও context ধরে রাখে?"),
        ],
        related=["nest-004", "nest-031"],
        refs=[NEST_SCOPES, NEST_ALS],
    ),
    # ------------------------------------------------------------------ nest-024
    Q(
        id="nest-024", sub="Circular Dependencies", diff="hard", type="debugging",
        prio="medium", market="both", mins=8,
        tags=["circular-dependency", "forwardref", "esm", "dependency-injection"],
        ver="NestJS 12.1 (CommonJS and ESM builds)", vs=True, status="stable",
        q_en=r"""After adding `UsersService` to `OrdersService` (orders need the customer) and `OrdersService` to `UsersService` (a user's order history), the app fails at startup. In a CommonJS build the error is "Nest can't resolve dependencies of the OrdersService (?). Please make sure that the argument at index [0] is available". In the ESM build it crashes with `ReferenceError: Cannot access 'UsersService' before initialization`. Explain both errors and fix the problem.""",
        q_bn=r"""`OrdersService`-এ `UsersService` (order-এর customer লাগে) আর `UsersService`-এ `OrdersService` (user-এর order history) যোগ করার পর app startup-এ fail করছে। CommonJS build-এ error: "Nest can't resolve dependencies of the OrdersService (?). Please make sure that the argument at index [0] is available"। ESM build-এ crash করে `ReferenceError: Cannot access 'UsersService' before initialization` দিয়ে। দুটো error ব্যাখ্যা করো আর সমস্যার সমাধান করো।""",
        code=r"""
            // users.service.ts
            import { Injectable } from '@nestjs/common';
            import { OrdersService } from './orders.service.js';

            @Injectable()
            export class UsersService {
              constructor(private readonly orders: OrdersService) {}
            }

            // orders.service.ts
            import { Injectable } from '@nestjs/common';
            import { UsersService } from './users.service.js';

            @Injectable()
            export class OrdersService {
              constructor(private readonly users: UsersService) {}
            }
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="Preferred fix: break the cycle", label_bn="পছন্দের সমাধান: cycle ভেঙে দেওয়া", src=r"""
                // customers.service.ts — shared read logic both sides need
                @Injectable()
                export class CustomersService {
                  constructor(@Inject(DRIZZLE) private readonly db: Database) {}
                  findCustomer(id: number) { /* ... */ }
                }

                // orders.service.ts — depends on CustomersService, not UsersService
                @Injectable()
                export class OrdersService {
                  constructor(private readonly customers: CustomersService) {}
                  findByUser(userId: number) { /* ... */ }
                }

                // users.service.ts — one-way dependency: Users -> Orders
                @Injectable()
                export class UsersService {
                  constructor(private readonly orders: OrdersService) {}
                }
            """),
            dict(lang="typescript", label_en="Last resort: forwardRef on both sides (ESM-safe)", label_bn="শেষ উপায়: দুই পাশে forwardRef (ESM-safe)", src=r"""
                import { Inject, Injectable, forwardRef } from '@nestjs/common';
                import { OrdersService } from './orders.service.js';

                // In ESM, the parameter type must not reference the class eagerly in decorator metadata
                type WrapperType<T> = T;

                @Injectable()
                export class UsersService {
                  constructor(
                    @Inject(forwardRef(() => OrdersService))
                    private readonly orders: WrapperType<OrdersService>,
                  ) {}
                }
                // OrdersService mirrors this with forwardRef(() => UsersService).
                // Module-level cycles need imports: [forwardRef(() => OrdersModule)] on both modules.
            """),
        ],
        a_en=r"""
            Both errors come from the **circular import** between the two files.

            - **CommonJS:** when `orders.service.ts` is evaluated, `users.service.ts` is still half-loaded, so `UsersService` is `undefined` when TypeScript writes the constructor's `design:paramtypes` metadata. Nest sees `[undefined]` and reports "can't resolve dependencies ... index [0]".
            - **ESM:** imports are live bindings in the temporal dead zone, so reading `UsersService` for the metadata before its module finishes throws `ReferenceError` at load time — before Nest even starts.

            **Fix:** first, break the cycle. Usually the two services share a concern (customer lookup) that belongs in a third provider, or one direction can become an event (`OrderPlaced`) instead of a direct call. If the cycle is truly needed, use `@Inject(forwardRef(() => OtherService))` on **both** sides. In ESM builds also wrap the parameter type (`WrapperType<OrdersService>`) so the metadata becomes `Object` and doesn't touch the class too early.
        """,
        a_bn=r"""
            দুটো error-ই আসছে দুই file-এর মধ্যে **circular import** থেকে।

            - **CommonJS:** `orders.service.ts` evaluate হওয়ার সময় `users.service.ts` অর্ধেক load হয়ে থাকে, তাই TypeScript যখন constructor-এর `design:paramtypes` metadata লেখে, তখন `UsersService` হয় `undefined`। Nest দেখে `[undefined]` আর report করে "can't resolve dependencies ... index [0]"।
            - **ESM:** import হলো live binding, temporal dead zone-এ থাকে; তাই module শেষ হওয়ার আগে metadata-র জন্য `UsersService` পড়লে load-এর সময়েই `ReferenceError` throw হয় — Nest শুরু হওয়ার আগেই।

            **সমাধান:** প্রথমে cycle ভাঙো। সাধারণত দুটো service একটা common concern share করে (customer lookup), যেটা তৃতীয় একটা provider-এ যাওয়া উচিত; অথবা এক দিক direct call-এর বদলে event (`OrderPlaced`) হতে পারে। Cycle সত্যিই দরকার হলে **দুই পাশেই** `@Inject(forwardRef(() => OtherService))` দাও। ESM build-এ parameter type-ও wrap করো (`WrapperType<OrdersService>`), যাতে metadata `Object` হয় আর class-কে আগেভাগে ছুঁতে না হয়।
        """,
        quick_en=r"""Both come from the circular import: in CommonJS `UsersService` is still `undefined` when the decorator metadata is written, and in ESM reading it early throws a TDZ `ReferenceError`. Break the cycle with a third provider or an event; if it must stay, use `forwardRef()` on both sides (plus `WrapperType` in ESM).""",
        quick_bn=r"""দুটো error-ই circular import থেকে আসে: CommonJS-এ decorator metadata লেখার সময় `UsersService` তখনো `undefined`, আর ESM-এ আগেভাগে পড়তে গেলে TDZ-এর `ReferenceError`। Shared কাজটা তৃতীয় provider-এ সরিয়ে বা event দিয়ে cycle ভাঙি; একান্তই রাখতে হলে দুই পাশে `forwardRef()` (ESM-এ সাথে `WrapperType`)।""",
        ex_en=r"""
            - `forwardRef` delays resolving the token until both classes exist; Nest then creates them in some order — don't rely on the other instance inside the constructor (use it in methods or `onModuleInit`).
            - Circular dependencies usually signal unclear module boundaries. In a modular monolith, dependencies should point one way (e.g. `Orders → Customers`), with events for the reverse direction.
            - The NestJS 12 CLI generates ESM projects by default, so the TDZ variant of this bug is more common in new projects than in older CommonJS ones.
            - Barrel files (`index.ts` re-exporting everything) often create accidental cycles — import from the concrete file instead.
            - Tools like `madge --circular` can detect import cycles in CI.
        """,
        ex_bn=r"""
            - `forwardRef` token resolve করা পিছিয়ে দেয় যতক্ষণ না দুটো class-ই তৈরি হয়; তারপর Nest যেকোনো একটা ক্রমে এদের বানায় — তাই constructor-এর ভেতরে অন্য instance-এর উপর ভরসা কোরো না (method-এ বা `onModuleInit`-এ ব্যবহার করো)।
            - Circular dependency সাধারণত অস্পষ্ট module boundary-র লক্ষণ। Modular monolith-এ dependency এক দিকে যাওয়া উচিত (যেমন `Orders → Customers`), উল্টো দিকের জন্য event।
            - NestJS 12 CLI default-এ ESM project বানায়, তাই এই bug-এর TDZ রূপটা পুরোনো CommonJS project-এর চেয়ে নতুন project-এ বেশি দেখা যায়।
            - Barrel file (`index.ts` যেটা সব re-export করে) প্রায়ই অনিচ্ছাকৃত cycle তৈরি করে — concrete file থেকে import করো।
            - `madge --circular`-এর মতো tool CI-তে import cycle ধরতে পারে।
        """,
        tip_en=r"""Say "forwardRef is a workaround, not a design" before showing it. Explaining *why* the class is `undefined` (module evaluation order + decorator metadata) is what makes this a hard-level answer.""",
        tip_bn=r"""`forwardRef` দেখানোর আগে বলো "এটা workaround, design না"। Class কেন `undefined` হয় (module evaluation order + decorator metadata) সেটা ব্যাখ্যা করলেই উত্তরটা hard-level হয়।""",
        mist_en=r"""Adding `forwardRef` on only one side; using `forwardRef` in an ESM build without changing the parameter type; reaching for `forwardRef` instead of fixing the boundary; confusing provider cycles with module import cycles.""",
        mist_bn=r"""শুধু এক পাশে `forwardRef` দেওয়া; ESM build-এ parameter type না বদলে `forwardRef` ব্যবহার করা; boundary ঠিক না করে সরাসরি `forwardRef`-এ চলে যাওয়া; provider cycle আর module import cycle গুলিয়ে ফেলা।""",
        follow=[
            ("How would you replace the reverse dependency with domain events?", "উল্টো dependency-টা domain event দিয়ে কীভাবে replace করবে?"),
            ("How do you detect circular imports automatically in CI?", "CI-তে circular import কীভাবে automatically ধরবে?"),
        ],
        related=["nest-003", "nest-030"],
        refs=[NEST_CIRCULAR, NEST_COMMON_ERRORS],
    ),
]

if __name__ == "__main__":
    save("nestjs", "b3", QUESTIONS)
