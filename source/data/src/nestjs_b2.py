# NestJS — batch 2 (nest-009 … nest-016): v12 changes, config, Nest vs Express, lifecycle, interceptors,
# custom decorators, JWT/RBAC, nested validation
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NEST_RELEASES = ("NestJS releases (GitHub)", "https://github.com/nestjs/nest/releases")
NEST_MIGRATION = ("NestJS docs — Migration guide", "https://docs.nestjs.com/migration-guide")
NEST_FIRST_STEPS = ("NestJS docs — First steps", "https://docs.nestjs.com/first-steps")
NEST_CONFIG = ("NestJS docs — Configuration", "https://docs.nestjs.com/application/configuration")
NEST_LIFECYCLE = ("NestJS docs — Request lifecycle", "https://docs.nestjs.com/faq/request-lifecycle")
NEST_INTERCEPTORS = ("NestJS docs — Interceptors", "https://docs.nestjs.com/interceptors")
NEST_DECORATORS = ("NestJS docs — Custom decorators", "https://docs.nestjs.com/custom-decorators")
NEST_AUTH = ("NestJS docs — Authentication", "https://docs.nestjs.com/security/authentication")
NEST_AUTHZ = ("NestJS docs — Authorization", "https://docs.nestjs.com/security/authorization")
NEST_VALIDATION = ("NestJS docs — Validation", "https://docs.nestjs.com/application/validation")
EXPRESS_5 = ("Express — Migrating to Express 5", "https://expressjs.com/en/guide/migrating-5.html")
OWASP_JWT = ("OWASP — JSON Web Token Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ nest-009
    Q(
        id="nest-009", sub="NestJS 12 Changes", diff="easy", type="mcq",
        prio="medium", market="both", mins=1,
        tags=["nestjs-12", "esm", "nodejs", "upgrade"],
        ver="NestJS 12.1 (v11 = legacy line)", vs=True, status="stable",
        q_en=r"""Which statement about NestJS 12 is correct?""",
        q_bn=r"""NestJS 12 সম্পর্কে কোন কথাটি সঠিক?""",
        options=[
            ("Core packages ship as ES modules and require Node.js 20.19+ or 22.12+; existing CommonJS apps can still load them through `require(esm)`", "Core package গুলো ES module হিসেবে আসে এবং Node.js 20.19+ বা 22.12+ লাগে; পুরোনো CommonJS app-ও `require(esm)`-এর মাধ্যমে এগুলো load করতে পারে"),
            ("It drops the Express adapter and makes Fastify the default HTTP platform", "এটা Express adapter বাদ দিয়ে Fastify-কে default HTTP platform বানিয়েছে"),
            ("It removes `class-validator` and `ValidationPipe` in favour of Standard Schema validation", "Standard Schema validation-এর জন্য `class-validator` আর `ValidationPipe` সরিয়ে দিয়েছে"),
            ("It runs on Node.js 18 or newer, the same baseline as Express 5", "এটা Node.js 18 বা নতুন version-এ চলে, Express 5-এর মতোই baseline"),
        ],
        correct=0,
        a_en=r"""The first one. In v12 all core packages are published as ESM, and the minimum runtime is Node.js 20.19+ or 22.12+ — the versions where `require(esm)` works by default, which is how most CommonJS apps keep working.""",
        a_bn=r"""প্রথমটা। v12-এ সব core package ESM হিসেবে publish হয়, আর minimum runtime হলো Node.js 20.19+ বা 22.12+ — এই version গুলোতেই `require(esm)` default-এ কাজ করে, আর এভাবেই বেশিরভাগ CommonJS app চলতে থাকে।""",
        quick_en=r"""In NestJS 12 the core packages ship as ES modules and need Node.js 20.19+ or 22.12+, the versions where `require(esm)` works by default, so existing CommonJS apps can still load them.""",
        quick_bn=r"""NestJS 12-এ core package-গুলো ES module হিসেবে আসে আর Node.js 20.19+ বা 22.12+ লাগে — এই version-গুলোতে `require(esm)` default-এ চলে, তাই পুরোনো CommonJS app-ও এগুলো load করতে পারে।""",
        ex_en=r"""
            Other v12 points worth knowing:
            - **Express stays the default** adapter (`@nestjs/platform-express` 12 uses Express 5.x); Fastify remains an optional adapter. Express 5 already became the default in Nest 11, so route wildcards follow the newer path syntax.
            - **Standard Schema validation is added, not a replacement.** `StandardSchemaValidationPipe` and the `schema` option on `@Body()`/`@Query()`/`@Param()` let you use zod, Valibot or ArkType. `ValidationPipe` with class-validator still works, and both pipes can run side by side.
            - New projects from the CLI default to ESM with Vitest (a CommonJS + Jest option is still offered), and `@nestjs/config` validation accepts Standard Schema schemas (Joi needs v18+).
            - Option 4 is tempting because Express 5 itself supports Node 18, but Nest 12 needs the newer Node lines because of the ESM packaging.

            Practical upgrade check: confirm your Node version in Docker images and CI first — Node 18, or any version below 20.19 (20.x) / 22.12 (22.x), isn't supported.
        """,
        ex_bn=r"""
            v12-এর আরও কিছু জানার মতো point:
            - **Express-ই default** adapter থাকছে (`@nestjs/platform-express` 12, Express 5.x ব্যবহার করে); Fastify optional adapter হিসেবেই আছে। Express 5 আসলে Nest 11-এই default হয়েছিল, তাই route wildcard নতুন path syntax মেনে চলে।
            - **Standard Schema validation যোগ হয়েছে, replace করেনি।** `StandardSchemaValidationPipe` আর `@Body()`/`@Query()`/`@Param()`-এর `schema` option দিয়ে zod, Valibot বা ArkType ব্যবহার করা যায়। class-validator সহ `ValidationPipe` এখনো কাজ করে, দুটো pipe পাশাপাশি চলতে পারে।
            - CLI দিয়ে নতুন project default-এ ESM আর Vitest দিয়ে তৈরি হয় (CommonJS + Jest option এখনো আছে), আর `@nestjs/config`-এর validation Standard Schema schema নেয় (Joi হলে v18+ লাগবে)।
            - Option 4 লোভনীয় কারণ Express 5 নিজে Node 18 support করে, কিন্তু ESM packaging-এর কারণে Nest 12-এর নতুন Node line লাগে।

            Practical upgrade check: আগে Docker image আর CI-তে Node version নিশ্চিত করো — Node 18, বা 20.19 (20.x) / 22.12 (22.x)-এর নিচের কোনো version support করা হয় না।
        """,
        tip_en=r"""If asked about upgrades, connect the dots: "ESM packages → needs `require(esm)` → Node 20.19+/22.12+ → check Docker base images and CI." That reasoning impresses more than the version number alone.""",
        tip_bn=r"""Upgrade নিয়ে প্রশ্ন এলে বিষয়গুলো জোড়া লাগাও: "ESM package → `require(esm)` লাগে → Node 20.19+/22.12+ → Docker base image আর CI check করো।" শুধু version number বলার চেয়ে এই যুক্তি বেশি impress করে।""",
        related=["nest-017", "nest-026"],
        refs=[NEST_RELEASES, NEST_MIGRATION],
    ),
    # ------------------------------------------------------------------ nest-010
    Q(
        id="nest-010", sub="Configuration", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["config", "environment-variables", "validation", "zod"],
        ver="NestJS 12.1 / @nestjs/config 12", vs=True, status="stable",
        q_en=r"""The app module uses the configuration below. `DATABASE_URL` is **not** set when the app boots. What happens?""",
        q_bn=r"""App module-এ নিচের configuration আছে। App boot হওয়ার সময় `DATABASE_URL` set **করা নেই**। কী হবে?""",
        code=r"""
            import { Module } from '@nestjs/common';
            import { ConfigModule } from '@nestjs/config';
            import { z } from 'zod';

            @Module({
              imports: [
                ConfigModule.forRoot({
                  isGlobal: true,
                  validationSchema: z.object({
                    DATABASE_URL: z.url(),
                    PORT: z.coerce.number().default(3000),
                  }),
                }),
              ],
            })
            export class AppModule {}
        """,
        lang="typescript",
        options=[
            ("The app starts; `configService.get('DATABASE_URL')` simply returns `undefined`", "App চালু হয়; `configService.get('DATABASE_URL')` শুধু `undefined` return করে"),
            ("The app starts and logs a warning; the first database query fails later", "App চালু হয় আর একটা warning log করে; পরে প্রথম database query fail করে"),
            ("Bootstrap fails with a config validation error, so the app never starts listening", "Bootstrap-এর সময়েই config validation error হয়, তাই app কখনো listen করা শুরু করে না"),
            ("`PORT` gets its default and `DATABASE_URL` falls back to an empty string", "`PORT` default value পায় আর `DATABASE_URL` empty string হয়ে যায়"),
        ],
        correct=2,
        a_en=r"""Bootstrap fails. `ConfigModule.forRoot()` validates `process.env` against the schema while the module is initialised; a required variable without a default is missing, so it throws "Config validation error: DATABASE_URL: ..." and the app never starts.""",
        a_bn=r"""Bootstrap fail করে। Module initialise হওয়ার সময় `ConfigModule.forRoot()` schema দিয়ে `process.env` validate করে; default ছাড়া একটা required variable নেই, তাই "Config validation error: DATABASE_URL: ..." throw করে আর app কখনো চালু হয় না।""",
        quick_en=r"""Bootstrap fails: `ConfigModule.forRoot()` validates `process.env` against the schema while the module initialises, finds the required `DATABASE_URL` missing and throws a config validation error, so the app never starts listening.""",
        quick_bn=r"""Bootstrap fail করে: module initialise হওয়ার সময় `ConfigModule.forRoot()` schema দিয়ে `process.env` validate করে, required `DATABASE_URL` না পেয়ে config validation error throw করে, তাই app কখনো listen শুরুই করে না।""",
        ex_en=r"""
            This is the **fail-fast** behaviour you want: a misconfigured deployment crashes immediately (and the orchestrator shows it) instead of serving traffic and failing on the first query. Option one is what happens **without** a schema — the tempting answer if you've only used plain `process.env`.

            Notes for NestJS 12:
            - `validationSchema` accepts any Standard Schema (zod, Valibot, ArkType); Joi still works from v18. `z.coerce.number()` turns the string `"3000"` into a number, and variables with defaults are optional.
            - A custom synchronous `validate(config)` function is the alternative (e.g. with class-validator).
            - `isGlobal: true` avoids importing `ConfigModule` everywhere; `configService.getOrThrow('KEY')` throws instead of returning `undefined`; `registerAs('database', () => ({...}))` gives namespaced config.
            - Never commit `.env` files with real secrets; in production, inject env vars from the platform or a secrets manager.
        """,
        ex_bn=r"""
            এটাই কাঙ্ক্ষিত **fail-fast** behaviour: ভুল config-এর deployment সাথে সাথে crash করে (আর orchestrator সেটা দেখায়), traffic serve করে প্রথম query-তে গিয়ে fail করে না। Schema **ছাড়া** যা হয় সেটা option এক — শুধু plain `process.env` ব্যবহার করা থাকলে এটাই লোভনীয় উত্তর।

            NestJS 12-এর নোট:
            - `validationSchema` যেকোনো Standard Schema নেয় (zod, Valibot, ArkType); Joi এখনো চলে v18 থেকে। `z.coerce.number()` string `"3000"`-কে number বানায়, আর default থাকা variable optional।
            - বিকল্প হলো একটা custom synchronous `validate(config)` function (যেমন class-validator দিয়ে)।
            - `isGlobal: true` দিলে সব জায়গায় `ConfigModule` import করতে হয় না; `configService.getOrThrow('KEY')` `undefined` না দিয়ে throw করে; `registerAs('database', () => ({...}))` দিয়ে namespaced config পাওয়া যায়।
            - আসল secret সহ `.env` file কখনো commit করো না; production-এ env var platform বা secrets manager থেকে inject করো।
        """,
        tip_en=r"""Say "fail fast at startup" and connect it to deployments: a pod that crashes on boot is caught by health checks before it receives traffic.""",
        tip_bn=r""""Startup-এই fail fast" কথাটা বলো আর deployment-এর সাথে মেলাও: boot-এর সময় crash করা pod traffic পাওয়ার আগেই health check-এ ধরা পড়ে।""",
        related=["nest-019", "nest-022"],
        refs=[NEST_CONFIG],
    ),
    # ------------------------------------------------------------------ nest-011
    Q(
        id="nest-011", sub="NestJS vs Express", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["nestjs", "express", "architecture", "trade-offs"],
        ver="NestJS 12.1 / Express 5.x", vs=False, status="stable",
        q_en=r"""NestJS vs plain Express: what are the main differences, and when would you choose each?""",
        q_bn=r"""NestJS আর plain Express-এর মূল পার্থক্য কী, আর কখন কোনটা বেছে নেবে?""",
        a_en=r"""
            Express is a minimal, unopinionated HTTP library: routing plus middleware, and you decide the structure. NestJS is an opinionated framework that runs **on top of** Express by default (or Fastify) and adds an architecture: modules, dependency injection, decorators, and building blocks like pipes, guards, interceptors and exception filters, plus testing utilities and first-class TypeScript.

            - **Choose Express** for small services, prototypes, simple webhooks or serverless functions, or when the team wants full control and minimal abstraction.
            - **Choose NestJS** for larger or long-lived codebases and bigger teams, where consistent structure, DI-based testing and built-in patterns (validation, auth guards, microservices, WebSockets) save time.

            NestJS doesn't replace Express — it organises it.
        """,
        a_bn=r"""
            Express হলো minimal, unopinionated HTTP library: routing আর middleware, structure তুমি নিজে ঠিক করো। NestJS হলো একটা opinionated framework, যেটা default-এ Express-এর **উপরে** চলে (অথবা Fastify) এবং একটা architecture যোগ করে: module, dependency injection, decorator, আর pipe, guard, interceptor, exception filter-এর মতো building block, সাথে testing utility আর first-class TypeScript।

            - **Express নাও** ছোট service, prototype, simple webhook বা serverless function-এর জন্য, অথবা team যখন পুরো control আর কম abstraction চায়।
            - **NestJS নাও** বড় বা দীর্ঘমেয়াদি codebase আর বড় team-এর জন্য, যেখানে consistent structure, DI-based testing আর built-in pattern (validation, auth guard, microservice, WebSocket) সময় বাঁচায়।

            NestJS, Express-কে replace করে না — বরং গুছিয়ে দেয়।
        """,
        quick_en=r"""Express is a minimal, unopinionated HTTP library; NestJS is an opinionated framework that runs on top of Express (or Fastify) and adds modules, DI, decorators, pipes, guards and testing tools. Pick Express for small services and prototypes, NestJS for large, long-lived codebases and bigger teams.""",
        quick_bn=r"""Express একটা minimal, unopinionated HTTP library; NestJS একটা opinionated framework যেটা Express (বা Fastify)-এর উপরেই চলে এবং module, DI, decorator, pipe, guard আর testing tool যোগ করে। ছোট service বা prototype-এর জন্য Express, বড় ও দীর্ঘমেয়াদি codebase আর বড় team-এর জন্য NestJS।""",
        ex_en=r"""
            - **Structure:** Express — you design it; NestJS — modules, controllers, providers.
            - **Validation / auth:** Express — pick libraries and wire them manually; NestJS — pipes, guards, decorators.
            - **Testing:** Express — manual mocking; NestJS — `Test.createTestingModule()` with provider overrides.
            - **Learning curve:** Express — low; NestJS — higher (DI, decorators, RxJS in interceptors).
            - **Overhead:** Express — minimal; NestJS — small runtime cost and more boilerplate.

            Trade-offs to mention honestly: more files and abstraction, decorator/reflection "magic" that confuses juniors, and slightly slower cold starts (relevant for serverless). On the plus side, a new developer can open any Nest project and find things in predictable places.

            You can still use Express middleware (`helmet`, `cors`, `cookie-parser`) inside Nest, and drop down to the raw request/response when needed. In Bangladesh many MERN/NestJS job posts list both — knowing that Nest uses Express 5 underneath is a good bridge.
        """,
        ex_bn=r"""
            - **Structure:** Express — নিজে design করো; NestJS — module, controller, provider।
            - **Validation / auth:** Express — library বেছে নিজে জোড়া লাগাও; NestJS — pipe, guard, decorator।
            - **Testing:** Express — manual mocking; NestJS — provider override সহ `Test.createTestingModule()`।
            - **Learning curve:** Express — কম; NestJS — বেশি (DI, decorator, interceptor-এ RxJS)।
            - **Overhead:** Express — খুব কম; NestJS — সামান্য runtime cost আর বেশি boilerplate।

            সৎভাবে trade-off গুলো বলো: বেশি file আর abstraction, decorator/reflection-এর "magic" যা junior-দের বিভ্রান্ত করে, আর একটু ধীর cold start (serverless-এ প্রাসঙ্গিক)। সুবিধার দিকে, নতুন developer যেকোনো Nest project খুললেই জিনিস predictable জায়গায় পায়।

            Nest-এর ভেতরেও Express middleware (`helmet`, `cors`, `cookie-parser`) ব্যবহার করা যায়, আর দরকার হলে raw request/response-এ নামা যায়। বাংলাদেশে অনেক MERN/NestJS job post-এ দুটোই থাকে — Nest যে ভেতরে Express 5 ব্যবহার করে, এটা জানা ভালো একটা bridge।
        """,
        tip_en=r"""Avoid "Nest is better". Frame it as "structure vs freedom" and give one concrete scenario for each. Interviewers want to see that you pick tools based on team size and project lifetime.""",
        tip_bn=r""""Nest ভালো" বলা এড়িয়ে চলো। "structure বনাম স্বাধীনতা" হিসেবে বলো আর প্রতিটার জন্য একটা করে বাস্তব scenario দাও। Interviewer দেখতে চায় তুমি team size আর project-এর আয়ু দেখে tool বেছে নাও।""",
        mist_en=r"""Saying NestJS "replaces" Express or is "faster"; claiming Express can't scale to large apps (it can, with discipline); ignoring the learning-curve and boilerplate cost.""",
        mist_bn=r"""বলা যে NestJS, Express-কে "replace" করে বা "দ্রুত"; দাবি করা যে Express বড় app-এ scale করে না (discipline থাকলে করে); learning curve আর boilerplate-এর খরচ উপেক্ষা করা।""",
        code=r"""
            // Express 5: you wire everything yourself
            app.get('/users/:id', async (req, res) => {
              const id = Number(req.params.id);
              if (!Number.isInteger(id)) return res.status(400).json({ message: 'Invalid id' });
              res.json(await usersService.findOne(id)); // rejected promises reach the error handler in Express 5
            });

            // NestJS: the same route, with conversion/validation and DI built in
            @Controller('users')
            export class UsersController {
              constructor(private readonly usersService: UsersService) {}

              @Get(':id')
              findOne(@Param('id', ParseIntPipe) id: number) {
                return this.usersService.findOne(id);
              }
            }
        """,
        lang="typescript",
        follow=[
            ("Can you use existing Express middleware in a NestJS app?", "NestJS app-এ existing Express middleware ব্যবহার করা যায়?"),
            ("Would you use NestJS for an AWS Lambda function? Why or why not?", "AWS Lambda function-এর জন্য NestJS ব্যবহার করবে? কেন বা কেন না?"),
        ],
        related=["nest-001", "nest-026"],
        refs=[NEST_FIRST_STEPS, EXPRESS_5],
    ),
    # ------------------------------------------------------------------ nest-012
    Q(
        id="nest-012", sub="Request Lifecycle", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["request-lifecycle", "middleware", "guards", "interceptors", "pipes"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""In what order does NestJS process an incoming HTTP request when middleware, a guard, an interceptor, a pipe and an exception filter are all bound to the route?""",
        q_bn=r"""একটা route-এ middleware, guard, interceptor, pipe আর exception filter সব bind করা থাকলে NestJS কোন ক্রমে incoming HTTP request process করে?""",
        options=[
            ("Guards → Middleware → Pipes → Interceptors → Handler → Exception filters", "Guards → Middleware → Pipes → Interceptors → Handler → Exception filters"),
            ("Middleware → Pipes → Guards → Interceptors → Handler → Exception filters", "Middleware → Pipes → Guards → Interceptors → Handler → Exception filters"),
            ("Middleware → Interceptors (before) → Guards → Pipes → Handler → Interceptors (after)", "Middleware → Interceptors (before) → Guards → Pipes → Handler → Interceptors (after)"),
            ("Middleware → Guards → Interceptors (before) → Pipes → Handler → Interceptors (after) → Exception filters (when something throws)", "Middleware → Guards → Interceptors (before) → Pipes → Handler → Interceptors (after) → Exception filters (কিছু throw হলে)"),
        ],
        correct=3,
        a_en=r"""Middleware → guards → interceptors (before the handler) → pipes → route handler → interceptors (after, on the way out) → exception filters, which only run if something throws.""",
        a_bn=r"""Middleware → guard → interceptor (handler-এর আগে) → pipe → route handler → interceptor (পরে, ফেরার পথে) → exception filter, যেটা শুধু কিছু throw হলে চলে।""",
        quick_en=r"""Middleware → guards → interceptors (before) → pipes → route handler → interceptors (after) → exception filters, and the filters run only when something throws.""",
        quick_bn=r"""ক্রমটা হলো: প্রথমে middleware, তারপর guard, তারপর interceptor-এর আগের অংশ, তারপর pipe, তারপর route handler, ফেরার পথে interceptor-এর পরের অংশ; আর কিছু throw হলে শুধু তখনই exception filter চলে।""",
        ex_en=r"""
            The order follows responsibility: middleware does generic request work (logging, request ids, body parsing); guards decide **whether** the request may continue (so no time is wasted validating a body for an unauthenticated user); interceptors wrap the handler call; pipes transform and validate the handler's arguments right before it runs.

            Within each stage: global → controller → route (pipes also run per parameter). On the way out, interceptors unwind in reverse order. Exception filters are resolved from the most specific (route) to global.

            Option C is the most tempting — interceptors feel like "outer" wrappers. But guards run **before** interceptors, which has a practical effect: an exception thrown by a guard is never seen by an interceptor's `catchError`. Pipe and handler errors are.
        """,
        ex_bn=r"""
            এই ক্রম দায়িত্ব অনুযায়ী: middleware generic request-এর কাজ করে (logging, request id, body parsing); guard ঠিক করে request এগোবে **কি না** (তাই unauthenticated user-এর body validate করে সময় নষ্ট হয় না); interceptor handler call-কে wrap করে; pipe handler চলার ঠিক আগে argument transform ও validate করে।

            প্রতিটা stage-এর ভেতরে: global → controller → route (pipe আবার প্রতিটা parameter-এর জন্যও চলে)। ফেরার পথে interceptor উল্টো ক্রমে unwind হয়। Exception filter সবচেয়ে specific (route) থেকে global-এর দিকে resolve হয়।

            Option C সবচেয়ে লোভনীয় — interceptor-কে "বাইরের" wrapper মনে হয়। কিন্তু guard চলে interceptor-এর **আগে**, আর এর practical প্রভাব আছে: guard-এ throw হওয়া exception কখনো interceptor-এর `catchError` দেখতে পায় না। Pipe আর handler-এর error দেখতে পায়।
        """,
        tip_en=r"""Don't just recite the order — justify it ("authorize before validating"). Then add the practical consequence about interceptors not seeing guard errors; that's a senior-level detail.""",
        tip_bn=r"""শুধু ক্রম মুখস্থ বোলো না — কারণ বলো ("validate করার আগে authorize")। তারপর interceptor যে guard-এর error দেখে না, সেই practical ফলাফল যোগ করো; এটা senior-level detail।""",
        related=["nest-021", "nest-029"],
        refs=[NEST_LIFECYCLE],
    ),
    # ------------------------------------------------------------------ nest-013
    Q(
        id="nest-013", sub="Interceptors", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["interceptors", "rxjs", "logging", "response-mapping"],
        ver="NestJS 12.1 / RxJS 7", vs=False, status="stable",
        q_en=r"""
            Write two global interceptors:

            1. `LoggingInterceptor` — logs method, URL and duration for every request, **including failed ones**.
            2. `EnvelopeInterceptor` — wraps every successful response as `{ data, meta: { requestId } }` and returns the id in an `x-request-id` header (reuse the incoming header if present).

            Example: a handler returning `{ "id": 1 }` should produce `{ "data": { "id": 1 }, "meta": { "requestId": "..." } }`. Register both so they can use dependency injection.
        """,
        q_bn=r"""
            দুটো global interceptor লেখো:

            1. `LoggingInterceptor` — প্রতিটা request-এর method, URL আর duration log করবে, **fail হওয়া request-ও**।
            2. `EnvelopeInterceptor` — প্রতিটা successful response-কে `{ data, meta: { requestId } }` আকারে wrap করবে আর `x-request-id` header-এ id ফেরত দেবে (incoming header থাকলে সেটাই reuse করবে)।

            উদাহরণ: handler `{ "id": 1 }` return করলে response হবে `{ "data": { "id": 1 }, "meta": { "requestId": "..." } }`। দুটোই এমনভাবে register করো যাতে dependency injection ব্যবহার করা যায়।
        """,
        a_en=r"""
            An interceptor implements `intercept(context, next)`. Code before `next.handle()` runs before the handler; `next.handle()` returns an RxJS `Observable` of the handler's result, so I use operators for the "after" part:

            - `tap({ next, error })` for side effects — logging on success **and** on error without changing the stream.
            - `map()` to transform the response into the envelope.

            I register them with `{ provide: APP_INTERCEPTOR, useClass: ... }` in a module (instead of `app.useGlobalInterceptors(new ...)`) so Nest can inject dependencies such as a logger or `ConfigService`. Interceptors registered this way run in registration order before the handler and in reverse order after it.
        """,
        a_bn=r"""
            Interceptor `intercept(context, next)` implement করে। `next.handle()`-এর আগের code handler-এর আগে চলে; `next.handle()` handler-এর result-এর একটা RxJS `Observable` return করে, তাই "পরের" অংশের জন্য operator ব্যবহার করি:

            - `tap({ next, error })` side effect-এর জন্য — stream না বদলে success **এবং** error দুই ক্ষেত্রেই log করা।
            - `map()` দিয়ে response-কে envelope-এ transform করা।

            Module-এ `{ provide: APP_INTERCEPTOR, useClass: ... }` দিয়ে register করি (`app.useGlobalInterceptors(new ...)` না দিয়ে), যাতে Nest logger বা `ConfigService`-এর মতো dependency inject করতে পারে। এভাবে register করা interceptor handler-এর আগে registration-এর ক্রমে আর পরে উল্টো ক্রমে চলে।
        """,
        quick_en=r"""Implement `intercept(context, next)` and use RxJS on `next.handle()`: `tap({ next, error })` logs the duration for successful and failed requests, and `map()` wraps the result in `{ data, meta }` after setting `x-request-id`. Register both with `APP_INTERCEPTOR` so Nest can inject their dependencies.""",
        quick_bn=r"""`intercept(context, next)` লিখে `next.handle()`-এর উপর RxJS operator লাগাই: `tap({ next, error })` success আর failed দুই request-এরই duration log করে, আর `map()` `x-request-id` set করে result-কে `{ data, meta }`-এ wrap করে। দুটোকেই `APP_INTERCEPTOR` দিয়ে register করি, যাতে Nest এদের dependency inject করতে পারে।""",
        ex_en=r"""
            - **Error path:** `tap`'s `error` callback sees errors thrown by pipes, the handler and services — but not by guards or middleware, which run before interceptors.
            - **Don't swallow errors:** if you use `catchError`, rethrow with `throwError(() => err)` so exception filters still produce the right status.
            - **Edge cases for the envelope:** file downloads (`StreamableFile`), Server-Sent Events and routes using `@Res()` shouldn't be wrapped. A common pattern is a `@SkipEnvelope()` metadata decorator checked with `Reflector` inside the interceptor.
            - **Other typical interceptors:** timeouts (`timeout(5000)` + map `TimeoutError` to `RequestTimeoutException`), caching (`CacheInterceptor` from `@nestjs/cache-manager`), and serialization (`ClassSerializerInterceptor`).
            - Use `performance.now()` for durations; `Date.now()` can jump if the system clock changes.
        """,
        ex_bn=r"""
            - **Error path:** `tap`-এর `error` callback pipe, handler আর service-এর error দেখে — কিন্তু guard বা middleware-এর না, কারণ ওরা interceptor-এর আগে চলে।
            - **Error গিলে ফেলো না:** `catchError` ব্যবহার করলে `throwError(() => err)` দিয়ে আবার throw করো, যাতে exception filter ঠিক status দিতে পারে।
            - **Envelope-এর edge case:** file download (`StreamableFile`), Server-Sent Events আর `@Res()` ব্যবহার করা route wrap করা উচিত না। Common pattern হলো একটা `@SkipEnvelope()` metadata decorator, যেটা interceptor-এর ভেতরে `Reflector` দিয়ে check করা হয়।
            - **আরও typical interceptor:** timeout (`timeout(5000)` + `TimeoutError`-কে `RequestTimeoutException`-এ map), caching (`@nestjs/cache-manager`-এর `CacheInterceptor`), আর serialization (`ClassSerializerInterceptor`)।
            - Duration মাপতে `performance.now()` ব্যবহার করো; system clock বদলালে `Date.now()` লাফ দিতে পারে।
        """,
        tip_en=r"""Explain the Observable model in one line: "before `next.handle()` = pre-processing, operators on the returned stream = post-processing". Then mention the guard-error blind spot — few candidates know it.""",
        tip_bn=r"""এক লাইনে Observable model বোঝাও: "`next.handle()`-এর আগে = pre-processing, ফেরত stream-এর operator = post-processing"। তারপর guard-error-এর blind spot-এর কথা বলো — খুব কম candidate এটা জানে।""",
        mist_en=r"""Using `map` for logging (it changes the value if you forget to return it); catching errors without rethrowing (turns failures into 200 responses); wrapping file streams in JSON; `new`-ing interceptors that need DI.""",
        mist_bn=r"""Logging-এর জন্য `map` ব্যবহার করা (return করতে ভুলে গেলে value বদলে যায়); error ধরে আবার throw না করা (failure 200 response হয়ে যায়); file stream-কে JSON-এ wrap করা; DI লাগে এমন interceptor `new` করে বানানো।""",
        code=r"""
            import { CallHandler, ExecutionContext, Injectable, Logger, NestInterceptor } from '@nestjs/common';
            import { Observable, map, tap } from 'rxjs';
            import { randomUUID } from 'node:crypto';
            import type { Request, Response } from 'express';

            @Injectable()
            export class LoggingInterceptor implements NestInterceptor {
              private readonly logger = new Logger('HTTP');

              intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
                const req = context.switchToHttp().getRequest<Request>();
                const started = performance.now();
                const elapsed = () => `${Math.round(performance.now() - started)}ms`;

                return next.handle().pipe(
                  tap({
                    next: () => this.logger.log(`${req.method} ${req.originalUrl} ${elapsed()}`),
                    error: (err: unknown) =>
                      this.logger.warn(`${req.method} ${req.originalUrl} failed after ${elapsed()}: ${String(err)}`),
                  }),
                );
              }
            }

            export interface Envelope<T> {
              data: T;
              meta: { requestId: string };
            }

            @Injectable()
            export class EnvelopeInterceptor<T> implements NestInterceptor<T, Envelope<T>> {
              intercept(context: ExecutionContext, next: CallHandler<T>): Observable<Envelope<T>> {
                const http = context.switchToHttp();
                const req = http.getRequest<Request>();
                const res = http.getResponse<Response>();
                const requestId = req.header('x-request-id') ?? randomUUID();
                res.setHeader('x-request-id', requestId);

                return next.handle().pipe(map((data) => ({ data, meta: { requestId } })));
              }
            }

            // app.module.ts — global registration with DI support
            import { Module } from '@nestjs/common';
            import { APP_INTERCEPTOR } from '@nestjs/core';

            @Module({
              providers: [
                { provide: APP_INTERCEPTOR, useClass: LoggingInterceptor },
                { provide: APP_INTERCEPTOR, useClass: EnvelopeInterceptor },
              ],
            })
            export class AppModule {}
        """,
        lang="typescript",
        time="O(1) extra work per request",
        space="O(1) per request",
        follow=[
            ("How would you add a 5-second timeout to every request with an interceptor?", "Interceptor দিয়ে প্রতিটা request-এ ৫ সেকেন্ডের timeout কীভাবে যোগ করবে?"),
            ("How do you skip the envelope for file downloads?", "File download-এর জন্য envelope কীভাবে skip করবে?"),
        ],
        related=["nest-012", "nest-029"],
        refs=[NEST_INTERCEPTORS],
    ),
    # ------------------------------------------------------------------ nest-014
    Q(
        id="nest-014", sub="Custom Decorators", diff="medium", type="coding",
        prio="medium", market="both", mins=7,
        tags=["decorators", "createparamdecorator", "applydecorators", "setmetadata", "reflector"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""
            Create two custom decorators:

            1. `@CurrentUser()` — a parameter decorator that returns `request.user` (set by an auth guard), or one field of it, e.g. `@CurrentUser('sub') userId: number`.
            2. `@Auth(...roles)` — one decorator that attaches role metadata **and** applies `JwtAuthGuard` + `RolesGuard`, so a route can be protected with `@Auth('admin')`.

            Show how both are used on a controller.
        """,
        q_bn=r"""
            দুটো custom decorator বানাও:

            1. `@CurrentUser()` — একটা parameter decorator যেটা `request.user` (auth guard set করে) return করবে, অথবা তার একটা field, যেমন `@CurrentUser('sub') userId: number`।
            2. `@Auth(...roles)` — একটাই decorator যেটা role metadata লাগাবে **এবং** `JwtAuthGuard` + `RolesGuard` apply করবে, যাতে `@Auth('admin')` দিয়ে route protect করা যায়।

            একটা controller-এ দুটো কীভাবে ব্যবহার হবে দেখাও।
        """,
        a_en=r"""
            - `createParamDecorator((data, ctx) => ...)` builds a parameter decorator. `data` is whatever is passed in the parentheses (here a field name), and `ctx` is the `ExecutionContext`, so I read `request.user` from it.
            - `SetMetadata(ROLES_KEY, roles)` attaches metadata to the handler or class; a guard reads it with `Reflector`.
            - `applyDecorators(...)` composes several decorators into one, so `@Auth('admin')` = `@Roles('admin')` + `@UseGuards(JwtAuthGuard, RolesGuard)`.

            This removes repeated boilerplate from controllers and keeps the "how" of auth in one place.
        """,
        a_bn=r"""
            - `createParamDecorator((data, ctx) => ...)` দিয়ে parameter decorator বানানো হয়। `data` হলো bracket-এর ভেতরে যা pass করা হয় (এখানে field-এর নাম), আর `ctx` হলো `ExecutionContext`, সেখান থেকে `request.user` পড়ি।
            - `SetMetadata(ROLES_KEY, roles)` handler বা class-এ metadata লাগায়; guard সেটা `Reflector` দিয়ে পড়ে।
            - `applyDecorators(...)` কয়েকটা decorator-কে একটায় জোড়া দেয়, তাই `@Auth('admin')` = `@Roles('admin')` + `@UseGuards(JwtAuthGuard, RolesGuard)`।

            এতে controller-এর repeated boilerplate কমে আর auth-এর "কীভাবে" অংশ এক জায়গায় থাকে।
        """,
        quick_en=r"""`@CurrentUser()` is built with `createParamDecorator`, reading `request.user` (or one field of it) from the `ExecutionContext`. `@Auth(...roles)` uses `applyDecorators` to combine `SetMetadata` for the roles with `@UseGuards(JwtAuthGuard, RolesGuard)`, and the roles guard reads that metadata with `Reflector`.""",
        quick_bn=r"""`@CurrentUser()` বানাই `createParamDecorator` দিয়ে, যেটা `ExecutionContext` থেকে `request.user` (বা তার একটা field) পড়ে। `@Auth(...roles)` বানাই `applyDecorators` দিয়ে — role-এর জন্য `SetMetadata` আর `@UseGuards(JwtAuthGuard, RolesGuard)` একসাথে, আর roles guard সেই metadata `Reflector` দিয়ে পড়ে।""",
        ex_en=r"""
            - **Metadata lookup:** in the guard, `reflector.getAllAndOverride(ROLES_KEY, [context.getHandler(), context.getClass()])` lets a method-level `@Roles()` override a class-level one; `getAllAndMerge` combines them.
            - **Type-safe alternative:** `export const Roles = Reflector.createDecorator<Role[]>()` creates a decorator and its metadata key in one go; read it with `reflector.get(Roles, context.getHandler())`.
            - **Validation gotcha:** `ValidationPipe` skips custom parameter decorators unless you set `validateCustomDecorators: true`.
            - **Design choice:** if guards are already global (`APP_GUARD`), `@Auth()` only needs the role metadata — applying guards again would run them twice.
            - Decorators are evaluated once at class definition time; the function passed to `createParamDecorator` runs on every request.
        """,
        ex_bn=r"""
            - **Metadata lookup:** guard-এ `reflector.getAllAndOverride(ROLES_KEY, [context.getHandler(), context.getClass()])` দিলে method-level `@Roles()` class-level-টাকে override করে; `getAllAndMerge` দুটো মিলিয়ে দেয়।
            - **Type-safe বিকল্প:** `export const Roles = Reflector.createDecorator<Role[]>()` একবারে decorator আর তার metadata key দুটোই বানায়; `reflector.get(Roles, context.getHandler())` দিয়ে পড়া যায়।
            - **Validation-এর ফাঁদ:** `validateCustomDecorators: true` না দিলে `ValidationPipe` custom parameter decorator skip করে।
            - **Design choice:** guard যদি আগেই global থাকে (`APP_GUARD`), তাহলে `@Auth()`-এ শুধু role metadata লাগবে — আবার guard লাগালে দুবার চলবে।
            - Decorator class define হওয়ার সময় একবার evaluate হয়; কিন্তু `createParamDecorator`-এ দেওয়া function প্রতিটা request-এ চলে।
        """,
        tip_en=r"""Show the usage first (`@Auth('admin')`, `@CurrentUser('sub')`) and then the implementation. Interviewers care that you can design a clean developer-facing API, not just call `createParamDecorator`.""",
        tip_bn=r"""আগে usage দেখাও (`@Auth('admin')`, `@CurrentUser('sub')`), তারপর implementation। Interviewer দেখতে চায় তুমি developer-দের জন্য একটা পরিষ্কার API design করতে পারো, শুধু `createParamDecorator` call করতে পারো তা না।""",
        mist_en=r"""Reading metadata only from the handler and ignoring class-level decorators; expecting custom param decorators to be validated automatically; using raw string keys scattered across files instead of exported constants.""",
        mist_bn=r"""শুধু handler থেকে metadata পড়া আর class-level decorator উপেক্ষা করা; ধরে নেওয়া যে custom param decorator নিজে থেকেই validate হবে; exported constant না রেখে বিভিন্ন file-এ raw string key ছড়িয়ে রাখা।""",
        code=r"""
            import {
              ExecutionContext, SetMetadata, UseGuards, applyDecorators, createParamDecorator,
            } from '@nestjs/common';
            import { JwtAuthGuard, RolesGuard } from './guards.js';

            export type Role = 'user' | 'admin';
            export interface AuthUser { sub: number; email: string; roles: Role[] }

            // 1) parameter decorator
            export const CurrentUser = createParamDecorator(
              (field: keyof AuthUser | undefined, ctx: ExecutionContext) => {
                const request = ctx.switchToHttp().getRequest<{ user?: AuthUser }>();
                const user = request.user;
                return field ? user?.[field] : user;
              },
            );

            // 2) metadata + composed decorator
            export const ROLES_KEY = 'roles';
            export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);

            export function Auth(...roles: Role[]) {
              return applyDecorators(Roles(...roles), UseGuards(JwtAuthGuard, RolesGuard));
            }

            // usage (controller imports omitted)
            @Controller('users')
            export class UsersController {
              constructor(private readonly usersService: UsersService) {}

              @Get('me')
              @Auth()
              me(@CurrentUser() user: AuthUser) {
                return user;
              }

              @Delete(':id')
              @Auth('admin')
              remove(@Param('id', ParseIntPipe) id: number, @CurrentUser('sub') actorId: number) {
                return this.usersService.remove(id, actorId);
              }
            }
        """,
        lang="typescript",
        time="O(1) per request",
        space="O(1)",
        follow=[
            ("What's the difference between `getAllAndOverride` and `getAllAndMerge`?", "`getAllAndOverride` আর `getAllAndMerge`-এর পার্থক্য কী?"),
            ("How would you validate a value returned by a custom parameter decorator?", "Custom parameter decorator যে value return করে সেটা কীভাবে validate করবে?"),
        ],
        related=["nest-015", "nest-007"],
        refs=[NEST_DECORATORS, NEST_AUTHZ],
    ),
    # ------------------------------------------------------------------ nest-015
    Q(
        id="nest-015", sub="Authentication & Authorization", diff="medium", type="scenario",
        prio="high", market="both", mins=10,
        tags=["jwt", "rbac", "guards", "authentication", "authorization"],
        ver="NestJS 12.1 / @nestjs/jwt 12", vs=False, status="stable",
        q_en=r"""You're building an API where most routes need a logged-in user, a few are public (login, health check), and some are admin-only. How would you implement JWT authentication and role-based authorization in NestJS?""",
        q_bn=r"""তুমি এমন একটা API বানাচ্ছ যেখানে বেশিরভাগ route-এ logged-in user লাগবে, কয়েকটা public (login, health check), আর কিছু শুধু admin-এর জন্য। NestJS-এ JWT authentication আর role-based authorization কীভাবে implement করবে?""",
        a_en=r"""
            **Clarify first:** token lifetime, whether there are refresh tokens, browser vs mobile clients (cookie vs `Authorization` header), and where roles come from.

            **My design — secure by default:**
            1. `JwtModule.registerAsync()` with the secret from `ConfigService` and a short access-token expiry (e.g. 15 minutes).
            2. A **global** `JwtAuthGuard` (`APP_GUARD`) that verifies `Bearer` tokens with `jwtService.verifyAsync()` and sets `request.user`. A `@Public()` decorator marks the few open routes, so a forgotten decorator means "protected", not "open".
            3. A global `RolesGuard`, registered after the auth guard, reads `@Roles('admin')` via `Reflector` and returns 403 if the user lacks the role.
            4. Ownership checks ("can edit only their own order") live in the service or a policy layer, because they need data, not just roles.

            **Options:** Passport (`@nestjs/passport` + `passport-jwt` strategy) is fine if you need many strategies (Google, local, SAML). For JWT alone, a small custom guard with `@nestjs/jwt` is simpler and easier to debug.
        """,
        a_bn=r"""
            **আগে clarify করি:** token কতক্ষণ valid, refresh token আছে কি না, browser নাকি mobile client (cookie নাকি `Authorization` header), আর role কোথা থেকে আসে।

            **আমার design — default-এ secure:**
            1. `JwtModule.registerAsync()`, secret আসবে `ConfigService` থেকে, access token-এর expiry ছোট (যেমন ১৫ মিনিট)।
            2. একটা **global** `JwtAuthGuard` (`APP_GUARD`), যেটা `jwtService.verifyAsync()` দিয়ে `Bearer` token verify করে `request.user` set করে। অল্প কয়েকটা খোলা route-কে `@Public()` decorator দিয়ে mark করি, তাই decorator দিতে ভুলে গেলে route "protected" থাকে, "open" হয় না।
            3. একটা global `RolesGuard`, auth guard-এর পরে register করা, `Reflector` দিয়ে `@Roles('admin')` পড়ে আর role না থাকলে 403 দেয়।
            4. Ownership check ("শুধু নিজের order edit করতে পারবে") service বা policy layer-এ থাকে, কারণ এর জন্য শুধু role না, data লাগে।

            **Option:** অনেক strategy (Google, local, SAML) লাগলে Passport (`@nestjs/passport` + `passport-jwt` strategy) ঠিক আছে। শুধু JWT-র জন্য `@nestjs/jwt` দিয়ে ছোট একটা custom guard সহজ আর debug করাও সহজ।
        """,
        quick_en=r"""Make it secure by default: a global `JwtAuthGuard` (`APP_GUARD`) verifies Bearer tokens with `@nestjs/jwt`, a `@Public()` decorator opens the few public routes, and a global `RolesGuard` reads `@Roles('admin')` via `Reflector` and returns 403. Ownership checks stay in the service because they need data.""",
        quick_bn=r"""Secure by default রাখি: global `JwtAuthGuard` (`APP_GUARD`) `@nestjs/jwt` দিয়ে Bearer token verify করে, `@Public()` decorator দিয়ে অল্প কয়েকটা public route খোলা রাখি, আর global `RolesGuard` `Reflector` দিয়ে `@Roles('admin')` পড়ে দরকার হলে 403 দেয়। Ownership check service-এ থাকে, কারণ তার জন্য data লাগে।""",
        ex_en=r"""
            - **Why global + `@Public()`:** opt-out security is safer than opt-in. One missing `@UseGuards()` in an opt-in design exposes data.
            - **401 vs 403:** missing/invalid token → `UnauthorizedException` (401); valid user without the role → `false` from the guard (403).
            - **Token hygiene:** pin the algorithm, keep secrets out of code, use short expiry; store refresh tokens hashed in the DB and rotate them so a stolen one can be revoked. For browsers, prefer `httpOnly`, `Secure`, `SameSite` cookies over `localStorage`.
            - **Don't trust the token forever:** roles inside a JWT are a snapshot. For sensitive actions or instant revocation, re-check the user in the DB or keep tokens very short-lived.
            - **Beyond RBAC:** attribute/policy-based checks (e.g. CASL) when rules depend on resource fields.
        """,
        ex_bn=r"""
            - **কেন global + `@Public()`:** opt-out security, opt-in-এর চেয়ে নিরাপদ। Opt-in design-এ একটা `@UseGuards()` বাদ পড়লেই data expose হয়ে যায়।
            - **401 বনাম 403:** token নেই/invalid → `UnauthorizedException` (401); valid user কিন্তু role নেই → guard থেকে `false` (403)।
            - **Token hygiene:** algorithm pin করো, secret code-এর বাইরে রাখো, expiry ছোট রাখো; refresh token DB-তে hash করে রাখো আর rotate করো, যাতে চুরি হলে revoke করা যায়। Browser-এর জন্য `localStorage`-এর বদলে `httpOnly`, `Secure`, `SameSite` cookie ভালো।
            - **Token-কে চিরকাল বিশ্বাস কোরো না:** JWT-র ভেতরের role একটা snapshot। Sensitive action বা সাথে সাথে revoke করার দরকার হলে DB-তে user আবার check করো, অথবা token খুব অল্প সময়ের জন্য রাখো।
            - **RBAC-এর বাইরে:** rule যখন resource-এর field-এর উপর নির্ভর করে, তখন attribute/policy-based check (যেমন CASL)।
        """,
        tip_en=r"""Lead with "secure by default: global guard plus `@Public()` opt-out". Then cover 401 vs 403 and refresh-token rotation. Mention Passport as an option rather than a requirement — it shows you understand what it actually does.""",
        tip_bn=r""""Default-এ secure: global guard আর `@Public()` opt-out" দিয়ে শুরু করো। তারপর 401 বনাম 403 আর refresh-token rotation বলো। Passport-কে বাধ্যতামূলক না বলে একটা option হিসেবে বলো — এতে বোঝা যায় এটা আসলে কী করে তুমি জানো।""",
        mist_en=r"""Putting auth in middleware (no access to route metadata); storing access tokens in `localStorage` without considering XSS; long-lived access tokens with no revocation; checking roles but not resource ownership.""",
        mist_bn=r"""Auth middleware-এ রাখা (route metadata পাওয়া যায় না); XSS না ভেবে `localStorage`-এ access token রাখা; revoke করার উপায় ছাড়া দীর্ঘমেয়াদি access token; role check করা কিন্তু resource ownership check না করা।""",
        code=r"""
            import {
              CanActivate, ExecutionContext, Injectable, Module, SetMetadata, UnauthorizedException,
            } from '@nestjs/common';
            import { APP_GUARD, Reflector } from '@nestjs/core';
            import { JwtModule, JwtService } from '@nestjs/jwt';
            import { ConfigService } from '@nestjs/config';
            import type { Request } from 'express';
            import { ROLES_KEY, type AuthUser, type Role } from './auth.decorators.js';

            export const IS_PUBLIC_KEY = 'isPublic';
            export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);

            @Injectable()
            export class JwtAuthGuard implements CanActivate {
              constructor(private readonly jwt: JwtService, private readonly reflector: Reflector) {}

              async canActivate(context: ExecutionContext): Promise<boolean> {
                const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
                  context.getHandler(),
                  context.getClass(),
                ]);
                if (isPublic) return true;

                const req = context.switchToHttp().getRequest<Request & { user?: AuthUser }>();
                const [type, token] = req.headers.authorization?.split(' ') ?? [];
                if (type !== 'Bearer' || !token) throw new UnauthorizedException();

                try {
                  req.user = await this.jwt.verifyAsync<AuthUser>(token);
                } catch {
                  throw new UnauthorizedException('Invalid or expired token');
                }
                return true;
              }
            }

            @Injectable()
            export class RolesGuard implements CanActivate {
              constructor(private readonly reflector: Reflector) {}

              canActivate(context: ExecutionContext): boolean {
                const required = this.reflector.getAllAndOverride<Role[] | undefined>(ROLES_KEY, [
                  context.getHandler(),
                  context.getClass(),
                ]);
                if (!required?.length) return true;

                const { user } = context.switchToHttp().getRequest<{ user?: AuthUser }>();
                return !!user && required.some((role) => user.roles.includes(role)); // false -> 403
              }
            }

            @Module({
              imports: [
                JwtModule.registerAsync({
                  global: true,
                  inject: [ConfigService],
                  useFactory: (config: ConfigService) => ({
                    secret: config.getOrThrow<string>('JWT_SECRET'),
                    signOptions: { expiresIn: '15m' },
                  }),
                }),
              ],
              providers: [
                { provide: APP_GUARD, useClass: JwtAuthGuard }, // runs first: sets request.user
                { provide: APP_GUARD, useClass: RolesGuard },   // then checks @Roles()
              ],
            })
            export class AuthModule {}
        """,
        lang="typescript",
        follow=[
            ("How would you implement refresh-token rotation and logout?", "Refresh-token rotation আর logout কীভাবে implement করবে?"),
            ("How would you authenticate WebSocket connections with the same JWT?", "একই JWT দিয়ে WebSocket connection কীভাবে authenticate করবে?"),
            ("When would you choose Passport over a custom guard?", "কখন custom guard-এর বদলে Passport বেছে নেবে?"),
        ],
        related=["nest-007", "nest-014", "nest-028"],
        refs=[NEST_AUTH, NEST_AUTHZ, OWASP_JWT],
    ),
    # ------------------------------------------------------------------ nest-016
    Q(
        id="nest-016", sub="Validation (class-validator)", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["validation", "class-validator", "class-transformer", "nested-dto"],
        ver="NestJS 12.1 (class-validator ValidationPipe)", vs=False, status="stable",
        q_en=r"""`POST /orders` with `{ "customerId": "c1", "items": [{ "productId": "abc", "quantity": -5, "hack": 1 }] }` passes validation and reaches the service unchanged — even the unknown `hack` field. The app uses `new ValidationPipe({ whitelist: true })`. Find the bug and fix it.""",
        q_bn=r"""`POST /orders`-এ `{ "customerId": "c1", "items": [{ "productId": "abc", "quantity": -5, "hack": 1 }] }` পাঠালে validation pass করে আর data অপরিবর্তিত অবস্থায় service-এ পৌঁছে যায় — অজানা `hack` field-ও। App-এ `new ValidationPipe({ whitelist: true })` আছে। Bug খুঁজে fix করো।""",
        code=r"""
            import { ArrayMinSize, IsArray, IsInt, IsNotEmpty, IsString, Max, Min } from 'class-validator';

            export class OrderItemDto {
              @IsInt() @Min(1) productId: number;
              @IsInt() @Min(1) @Max(100) quantity: number;
            }

            export class CreateOrderDto {
              @IsString() @IsNotEmpty() customerId: string;

              @IsArray()
              @ArrayMinSize(1)
              items: OrderItemDto[];
            }

            // main.ts
            app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", label_en="Fixed DTO", label_bn="সংশোধিত DTO", src=r"""
                import { Type } from 'class-transformer';
                import {
                  ArrayMinSize, IsArray, IsInt, IsNotEmpty, IsString, Max, Min, ValidateNested,
                } from 'class-validator';

                export class OrderItemDto {
                  @IsInt() @Min(1) productId: number;
                  @IsInt() @Min(1) @Max(100) quantity: number;
                }

                export class CreateOrderDto {
                  @IsString() @IsNotEmpty() customerId: string;

                  @IsArray()
                  @ArrayMinSize(1)
                  @ValidateNested({ each: true }) // validate every element
                  @Type(() => OrderItemDto)       // turn plain objects into OrderItemDto instances
                  items: OrderItemDto[];
                }

                // Response now: 400
                // ["items.0.productId must not be less than 1",
                //  "items.0.productId must be an integer number",
                //  "items.0.quantity must not be less than 1"]
            """),
        ],
        a_en=r"""
            The nested objects are never validated. `@IsArray()` only checks that `items` is an array. class-validator validates nested objects only when the property has `@ValidateNested()`, and class-transformer only turns the plain JSON elements into `OrderItemDto` instances when it knows the type via `@Type(() => OrderItemDto)` — TypeScript's `OrderItemDto[]` annotation is not available at runtime for array elements.

            Because the elements stay plain objects, their decorators are never looked at, and `whitelist` can't strip `hack` either. Adding `@ValidateNested({ each: true })` and `@Type(() => OrderItemDto)` fixes both.
        """,
        a_bn=r"""
            Nested object গুলো কখনো validate হচ্ছে না। `@IsArray()` শুধু check করে `items` একটা array কি না। class-validator nested object validate করে কেবল তখনই যখন property-তে `@ValidateNested()` থাকে, আর class-transformer plain JSON element-কে `OrderItemDto` instance বানায় কেবল তখন যখন `@Type(() => OrderItemDto)` দিয়ে type জানানো থাকে — array element-এর জন্য TypeScript-এর `OrderItemDto[]` annotation runtime-এ পাওয়া যায় না।

            Element গুলো plain object থেকে যায় বলে তাদের decorator কখনো দেখা হয় না, আর `whitelist`-ও `hack` সরাতে পারে না। `@ValidateNested({ each: true })` আর `@Type(() => OrderItemDto)` যোগ করলে দুটো সমস্যাই মিটে যায়।
        """,
        quick_en=r"""The nested items are never validated: `@IsArray()` only checks the array, and without `@ValidateNested({ each: true })` and `@Type(() => OrderItemDto)` the elements stay plain objects, so their decorators and `whitelist` are ignored. Adding those two decorators fixes it.""",
        quick_bn=r"""Nested item-গুলো কখনো validate-ই হয় না: `@IsArray()` শুধু array কি না দেখে, আর `@ValidateNested({ each: true })` ও `@Type(() => OrderItemDto)` ছাড়া element-গুলো plain object থেকে যায়, তাই তাদের decorator বা `whitelist` কাজ করে না। ওই দুটো decorator যোগ করলেই ঠিক হয়।""",
        ex_en=r"""
            - **Root cause:** decorator metadata stores `Array` as the design type of `items`, not `OrderItemDto[]`. Without `@Type`, class-transformer has no idea what to instantiate.
            - **Security impact:** with `whitelist` silently not applying to nested data, extra fields (`isAdmin`, `price`) can reach the service — a mass-assignment risk if you spread the DTO into a DB insert.
            - **Recommended global setup:** `new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true })`. `forbidNonWhitelisted` returns 400 for unknown fields instead of stripping silently, which helps API clients notice mistakes.
            - The same applies to single nested objects (`@ValidateNested() @Type(() => AddressDto) address: AddressDto`).
            - Write an e2e test with an invalid nested payload so this can't regress.
        """,
        ex_bn=r"""
            - **Root cause:** decorator metadata `items`-এর design type হিসেবে `OrderItemDto[]` না, `Array` রাখে। `@Type` ছাড়া class-transformer জানে না কোন class-এর instance বানাতে হবে।
            - **Security প্রভাব:** nested data-তে `whitelist` চুপচাপ কাজ না করলে বাড়তি field (`isAdmin`, `price`) service পর্যন্ত পৌঁছাতে পারে — DTO spread করে DB-তে insert করলে এটা mass-assignment ঝুঁকি।
            - **Recommended global setup:** `new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true })`। `forbidNonWhitelisted` অজানা field চুপচাপ না সরিয়ে 400 দেয়, ফলে API client ভুল ধরতে পারে।
            - একক nested object-এর ক্ষেত্রেও একই নিয়ম (`@ValidateNested() @Type(() => AddressDto) address: AddressDto`)।
            - Invalid nested payload দিয়ে একটা e2e test লেখো, যাতে এই bug আবার ফিরে না আসে।
        """,
        tip_en=r"""Explain *why* both decorators are needed — one for class-transformer (instantiation), one for class-validator (recursion). Mentioning the mass-assignment risk turns a bug fix into a security discussion.""",
        tip_bn=r"""দুটো decorator *কেন* লাগে বোঝাও — একটা class-transformer-এর জন্য (instance বানানো), একটা class-validator-এর জন্য (ভেতরে ঢুকে validate)। Mass-assignment ঝুঁকির কথা বললে bug fix-টা security আলোচনায় পরিণত হয়।""",
        mist_en=r"""Adding only `@ValidateNested()` (elements still plain objects, so nothing is validated); adding only `@Type()`; assuming `whitelist` protects nested objects automatically.""",
        mist_bn=r"""শুধু `@ValidateNested()` দেওয়া (element তখনও plain object, তাই কিছুই validate হয় না); শুধু `@Type()` দেওয়া; ধরে নেওয়া যে `whitelist` নিজে থেকেই nested object রক্ষা করে।""",
        follow=[
            ("What do `whitelist`, `forbidNonWhitelisted` and `transform` each do?", "`whitelist`, `forbidNonWhitelisted` আর `transform` আলাদাভাবে কী করে?"),
            ("How would the same validation look with a zod schema in NestJS 12?", "NestJS 12-এ zod schema দিয়ে একই validation কেমন হবে?"),
        ],
        related=["nest-005", "nest-006", "nest-017"],
        refs=[NEST_VALIDATION],
    ),
]

if __name__ == "__main__":
    save("nestjs", "b2", QUESTIONS)
