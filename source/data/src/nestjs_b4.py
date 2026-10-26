# NestJS — batch 4 (nest-025 … nest-032): exception filter, Fastify adapter, microservices/WebSockets, security,
# lifecycle MCQ, modular monolith, multi-tenancy, idempotent webhooks
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NEST_FILTERS = ("NestJS docs — Exception filters", "https://docs.nestjs.com/exception-filters")
NEST_PERFORMANCE = ("NestJS docs — Performance (Fastify)", "https://docs.nestjs.com/http/performance")
NEST_MICRO = ("NestJS docs — Microservices", "https://docs.nestjs.com/microservices/basics")
NEST_GATEWAYS = ("NestJS docs — WebSocket gateways", "https://docs.nestjs.com/websockets/gateways")
NEST_WS_ADAPTER = ("NestJS docs — WebSocket adapters", "https://docs.nestjs.com/websockets/adapter")
NEST_HELMET = ("NestJS docs — Helmet", "https://docs.nestjs.com/security/helmet")
NEST_RATE = ("NestJS docs — Rate limiting", "https://docs.nestjs.com/security/rate-limiting")
NEST_SERIALIZATION = ("NestJS docs — Serialization", "https://docs.nestjs.com/application/serialization")
NEST_LIFECYCLE = ("NestJS docs — Request lifecycle", "https://docs.nestjs.com/faq/request-lifecycle")
NEST_INTERCEPTORS = ("NestJS docs — Interceptors", "https://docs.nestjs.com/interceptors")
NEST_CQRS = ("NestJS docs — CQRS", "https://docs.nestjs.com/recipes/cqrs")
NEST_MODULES = ("NestJS docs — Modules", "https://docs.nestjs.com/modules")
NEST_SCOPES = ("NestJS docs — Injection scopes (durable providers)", "https://docs.nestjs.com/fundamentals/injection-scopes")
NEST_IDEMPOTENCY = ("NestJS docs — Idempotency", "https://docs.nestjs.com/reliability/idempotency")
NEST_RAW_BODY = ("NestJS docs — Raw body", "https://docs.nestjs.com/faq/raw-body")
PG_RLS = ("PostgreSQL docs — Row Security Policies", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html")
PG_ERRCODES = ("PostgreSQL docs — Error codes", "https://www.postgresql.org/docs/current/errcodes-appendix.html")
OWASP_MULTI_TENANT = ("OWASP — Multi-Tenant Security Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ nest-025
    Q(
        id="nest-025", sub="Exception Filters", diff="hard", type="coding",
        prio="high", market="both", mins=10,
        tags=["exception-filters", "error-handling", "postgresql", "drizzle", "platform-agnostic"],
        ver="NestJS 12.1 / Drizzle ORM 0.45 (DrizzleQueryError since 0.44)", vs=True, status="stable",
        q_en=r"""
            Write a global exception filter that:

            - returns one consistent JSON shape for every error: `statusCode`, `message`, `path`, `timestamp`;
            - keeps `HttpException` responses (404, validation 400s) as they are;
            - maps PostgreSQL unique violations (SQLSTATE `23505`) to **409 Conflict** — note that Drizzle 0.44+ wraps driver errors in `DrizzleQueryError`;
            - never leaks internal error messages, and logs 5xx errors with stack traces;
            - works with both the Express and the Fastify adapter.

            Example: inserting a duplicate email returns `409 {"statusCode":409,"error":"Conflict","message":"Resource already exists","path":"/users","timestamp":"..."}`.
        """,
        q_bn=r"""
            একটা global exception filter লেখো যেটা:

            - প্রতিটা error-এর জন্য একই JSON shape দেবে: `statusCode`, `message`, `path`, `timestamp`;
            - `HttpException`-এর response (404, validation 400) যেমন আছে তেমন রাখবে;
            - PostgreSQL unique violation (SQLSTATE `23505`)-কে **409 Conflict**-এ map করবে — খেয়াল রাখো, Drizzle 0.44+ driver error-কে `DrizzleQueryError`-এ wrap করে;
            - internal error message কখনো leak করবে না, আর 5xx error stack trace সহ log করবে;
            - Express আর Fastify দুই adapter-এই কাজ করবে।

            উদাহরণ: duplicate email insert করলে আসবে `409 {"statusCode":409,"error":"Conflict","message":"Resource already exists","path":"/users","timestamp":"..."}`।
        """,
        a_en=r"""
            - `@Catch()` with no arguments catches everything. I register it with `{ provide: APP_FILTER, useClass: AllExceptionsFilter }` so it can inject dependencies.
            - To stay platform-agnostic I inject `HttpAdapterHost` and use `httpAdapter.reply()`, `getRequestUrl()` and `getRequestMethod()` instead of Express's `res.status().json()`.
            - A small `toResponse()` method classifies the error: `HttpException` → its own status and body; a database error whose code is `23505` → 409; anything else → generic 500.
            - Because Drizzle 0.44+ throws `DrizzleQueryError` with the original `pg` error in `.cause`, the helper unwraps `cause` before reading `code`. Checking `err.code` directly would silently stop matching after a Drizzle upgrade.
            - Only 5xx errors are logged with stack traces; 4xx are expected client errors and would just add noise.
        """,
        a_bn=r"""
            - Argument ছাড়া `@Catch()` সব কিছু ধরে। `{ provide: APP_FILTER, useClass: AllExceptionsFilter }` দিয়ে register করি, যাতে dependency inject করা যায়।
            - Platform-agnostic থাকতে `HttpAdapterHost` inject করি আর Express-এর `res.status().json()`-এর বদলে `httpAdapter.reply()`, `getRequestUrl()` আর `getRequestMethod()` ব্যবহার করি।
            - ছোট একটা `toResponse()` method error-কে ভাগ করে: `HttpException` → তার নিজের status আর body; database error যার code `23505` → 409; বাকি সব → generic 500।
            - Drizzle 0.44+ যেহেতু original `pg` error `.cause`-এ রেখে `DrizzleQueryError` throw করে, helper আগে `cause` খুলে তারপর `code` পড়ে। সরাসরি `err.code` check করলে Drizzle upgrade-এর পর চুপচাপ match করা বন্ধ হয়ে যেত।
            - শুধু 5xx error stack trace সহ log হয়; 4xx হলো প্রত্যাশিত client error, log করলে শুধু noise বাড়ে।
        """,
        quick_en=r"""Use a `@Catch()` filter registered via `APP_FILTER` that replies through `HttpAdapterHost`, so it works on Express and Fastify. `HttpException` keeps its status and body, a `23505` code found after unwrapping `DrizzleQueryError.cause` becomes 409, and anything else becomes a generic 500 logged with its stack.""",
        quick_bn=r"""`APP_FILTER` দিয়ে register করা একটা `@Catch()` filter ব্যবহার করি, যেটা `HttpAdapterHost` দিয়ে reply দেয়, তাই Express আর Fastify দুটোতেই চলে। `HttpException` নিজের status আর body রাখে, `DrizzleQueryError.cause` unwrap করে `23505` পেলে 409, আর বাকি সব generic 500 যেটা stack-সহ log হয়।""",
        ex_en=r"""
            - **Why 409 instead of checking first:** "SELECT then INSERT" has a race between two requests; letting the unique constraint decide and mapping the error is both correct under concurrency and cheaper.
            - **Other useful SQLSTATEs:** `23503` (foreign key violation) and `23502` (not-null violation) usually mean bad input → 409/422; `40001` (serialization failure) and `40P01` (deadlock) are retryable.
            - **Don't over-centralise:** mapping in the filter is a safety net. When the business meaning matters ("email already registered"), catch the error in the service and throw a specific `ConflictException` with a clear message.
            - **Correlation:** add a request id to the body and logs so support can find the log line from a user's screenshot.
            - Filters also receive errors from guards and pipes, so 401/403/400 get the same `path` and `timestamp` fields.
        """,
        ex_bn=r"""
            - **আগে check না করে 409 কেন:** "SELECT তারপর INSERT"-এ দুই request-এর মধ্যে race থাকে; unique constraint-কে সিদ্ধান্ত নিতে দিয়ে error map করা concurrency-তেও সঠিক, আর সস্তাও।
            - **আরও কাজের SQLSTATE:** `23503` (foreign key violation) আর `23502` (not-null violation) সাধারণত খারাপ input বোঝায় → 409/422; `40001` (serialization failure) আর `40P01` (deadlock) retry করা যায়।
            - **সব কিছু কেন্দ্রে এনো না:** filter-এ mapping একটা safety net। Business অর্থ যখন গুরুত্বপূর্ণ ("email আগেই registered"), service-এ error ধরে পরিষ্কার message সহ নির্দিষ্ট `ConflictException` throw করো।
            - **Correlation:** body আর log-এ একটা request id যোগ করো, যাতে user-এর screenshot থেকে support টিম log line খুঁজে পায়।
            - Guard আর pipe-এর error-ও filter-এ আসে, তাই 401/403/400-ও একই `path` আর `timestamp` field পায়।
        """,
        tip_en=r"""Highlight two senior details: `HttpAdapterHost` for platform independence, and unwrapping `DrizzleQueryError.cause`. Then explain why mapping the constraint error beats a pre-check (race conditions).""",
        tip_bn=r"""দুটো senior detail তুলে ধরো: platform independence-এর জন্য `HttpAdapterHost`, আর `DrizzleQueryError.cause` খোলা। তারপর বলো কেন pre-check-এর চেয়ে constraint error map করা ভালো (race condition)।""",
        mist_en=r"""Returning `exception.message` for unknown errors (leaks internals); using Express-only `response.status().json()` in a shared filter; logging every 4xx as an error; checking `err.code` on the Drizzle wrapper instead of `err.cause.code`.""",
        mist_bn=r"""Unknown error-এর জন্য `exception.message` return করা (internal জিনিস leak হয়); shared filter-এ শুধু Express-এর `response.status().json()` ব্যবহার করা; প্রতিটা 4xx-কে error হিসেবে log করা; `err.cause.code`-এর বদলে Drizzle wrapper-এর `err.code` check করা।""",
        code=r"""
            import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Logger } from '@nestjs/common';
            import { HttpAdapterHost } from '@nestjs/core';
            import { DrizzleQueryError } from 'drizzle-orm';

            function pgErrorCode(err: unknown): string | undefined {
              const cause = err instanceof DrizzleQueryError ? err.cause : err;
              const code = (cause as { code?: unknown } | undefined)?.code;
              return typeof code === 'string' ? code : undefined;
            }

            @Catch()
            export class AllExceptionsFilter implements ExceptionFilter {
              private readonly logger = new Logger(AllExceptionsFilter.name);

              constructor(private readonly adapterHost: HttpAdapterHost) {}

              catch(exception: unknown, host: ArgumentsHost): void {
                const { httpAdapter } = this.adapterHost;
                const ctx = host.switchToHttp();
                const req = ctx.getRequest();
                const { status, body } = this.toResponse(exception);

                if (status >= 500) {
                  const method = httpAdapter.getRequestMethod(req);
                  const url = httpAdapter.getRequestUrl(req);
                  this.logger.error(`${method} ${url}`, exception instanceof Error ? exception.stack : String(exception));
                }

                httpAdapter.reply(
                  ctx.getResponse(),
                  { ...body, path: httpAdapter.getRequestUrl(req), timestamp: new Date().toISOString() },
                  status,
                );
              }

              private toResponse(exception: unknown): { status: number; body: Record<string, unknown> } {
                if (exception instanceof HttpException) {
                  const status = exception.getStatus();
                  const res = exception.getResponse();
                  return {
                    status,
                    body: typeof res === 'string' ? { statusCode: status, message: res } : (res as Record<string, unknown>),
                  };
                }
                if (pgErrorCode(exception) === '23505') {
                  return {
                    status: HttpStatus.CONFLICT,
                    body: { statusCode: 409, error: 'Conflict', message: 'Resource already exists' },
                  };
                }
                return { status: 500, body: { statusCode: 500, message: 'Internal server error' } };
              }
            }

            // app.module.ts
            // providers: [{ provide: APP_FILTER, useClass: AllExceptionsFilter }]
        """,
        lang="typescript",
        output=r"""
            POST /users {"email":"a@b.co"}   (second time)
            409 {"statusCode":409,"error":"Conflict","message":"Resource already exists","path":"/users","timestamp":"2026-10-12T12:33:42.562Z"}

            GET /users/boom   (handler throws new Error('secret internals'))
            500 {"statusCode":500,"message":"Internal server error","path":"/users/boom","timestamp":"2026-10-12T12:33:42.568Z"}
        """,
        time="O(1) per error",
        space="O(1)",
        follow=[
            ("When would you catch the error in the service instead of the filter?", "কখন filter-এর বদলে service-এ error ধরবে?"),
            ("How would you adapt the filter for WebSocket or microservice contexts?", "WebSocket বা microservice context-এর জন্য filter কীভাবে বদলাবে?"),
        ],
        related=["nest-008", "drizzle-019"],
        refs=[NEST_FILTERS, PG_ERRCODES],
    ),
    # ------------------------------------------------------------------ nest-026
    Q(
        id="nest-026", sub="Express vs Fastify Adapter", diff="hard", type="scenario",
        prio="medium", market="both", mins=10,
        tags=["fastify", "express", "http-adapter", "performance", "migration"],
        ver="NestJS 12.1 (@nestjs/platform-express on Express 5.x; @nestjs/platform-fastify on Fastify 5.x)", vs=True, status="stable",
        q_en=r"""Your team lead suggests switching a production NestJS API from the default Express adapter to Fastify "for performance". How would you evaluate this, what would break, and how would you migrate safely?""",
        q_bn=r"""তোমার team lead একটা production NestJS API-কে default Express adapter থেকে Fastify-তে নিতে চান "performance-এর জন্য"। তুমি এটা কীভাবে evaluate করবে, কী কী ভাঙতে পারে, আর কীভাবে নিরাপদে migrate করবে?""",
        a_en=r"""
            **1. Check the premise.** Fastify has lower framework overhead per request, but most APIs spend their time in the database, external calls or serialisation. I'd profile first (p95/p99 latency, CPU per request). The switch pays off for high-RPS, small-payload endpoints where the framework itself is a measurable share of CPU.

            **2. What changes / breaks:**
            - Bootstrap: `NestFactory.create<NestFastifyApplication>(AppModule, new FastifyAdapter())`, and `app.listen(port, '0.0.0.0')` — Fastify binds to localhost by default, which breaks inside Docker.
            - Express middleware (`helmet`, `multer`, `express-session`, `compression`) must be replaced with Fastify plugins (`@fastify/helmet`, `@fastify/multipart`, `@fastify/cookie`, `@fastify/compress`) registered via `app.register()`.
            - Any code that uses `@Req()`/`@Res()` with Express APIs (`res.status().json()`, `req.header()`) breaks; Fastify uses `FastifyRequest`/`FastifyReply` (`reply.code().send()`). Nest middleware receives the raw Node request/response objects under Fastify.
            - E2E tests need the Fastify instance to be ready (`await app.getHttpAdapter().getInstance().ready()`) before sending requests.

            **3. Migrate safely:** first make the code platform-agnostic (no `@Res()`, filters using `HttpAdapterHost`), switch on a branch, run the full e2e suite and a load test comparing both adapters, then canary-release.

            **Recommendation:** Express 5 is the default in Nest 12 and is fine for most teams; switch only with measured evidence.
        """,
        a_bn=r"""
            **১. আগে ধারণাটা যাচাই করি।** Fastify-র per-request framework overhead কম, কিন্তু বেশিরভাগ API-র সময় যায় database, external call বা serialisation-এ। আমি আগে profile করব (p95/p99 latency, per request CPU)। High-RPS, ছোট payload-এর endpoint-এ, যেখানে framework নিজেই CPU-র উল্লেখযোগ্য অংশ নেয়, সেখানেই switch করে লাভ হয়।

            **২. কী বদলায় / ভাঙে:**
            - Bootstrap: `NestFactory.create<NestFastifyApplication>(AppModule, new FastifyAdapter())`, আর `app.listen(port, '0.0.0.0')` — Fastify default-এ localhost-এ bind করে, Docker-এর ভেতরে এটা কাজ করে না।
            - Express middleware (`helmet`, `multer`, `express-session`, `compression`) Fastify plugin (`@fastify/helmet`, `@fastify/multipart`, `@fastify/cookie`, `@fastify/compress`) দিয়ে বদলাতে হবে, `app.register()` দিয়ে register করে।
            - যেসব code `@Req()`/`@Res()` দিয়ে Express API (`res.status().json()`, `req.header()`) ব্যবহার করে সেগুলো ভাঙবে; Fastify-তে `FastifyRequest`/`FastifyReply` (`reply.code().send()`)। Fastify-তে Nest middleware raw Node request/response object পায়।
            - E2E test-এ request পাঠানোর আগে Fastify instance ready হতে হয় (`await app.getHttpAdapter().getInstance().ready()`)।

            **৩. নিরাপদ migration:** আগে code platform-agnostic করো (`@Res()` বাদ, filter-এ `HttpAdapterHost`), একটা branch-এ switch করো, পুরো e2e suite আর দুই adapter-এর তুলনামূলক load test চালাও, তারপর canary release।

            **সুপারিশ:** Nest 12-এ Express 5-ই default আর বেশিরভাগ team-এর জন্য যথেষ্ট; মাপা প্রমাণ থাকলে তবেই switch করো।
        """,
        quick_en=r"""Profile first: Fastify cuts framework overhead, but most APIs spend their time in the database, so switch only with measured evidence. Express middleware, `@Res()` code and bootstrap (`listen(port, '0.0.0.0')`) must change, so make the code platform-agnostic, run e2e and load tests, then canary-release.""",
        quick_bn=r"""আগে profile করি: Fastify framework-এর overhead কমায়, কিন্তু বেশিরভাগ API-র সময় যায় database-এ, তাই মাপা প্রমাণ ছাড়া switch করি না। Express middleware, `@Res()`-নির্ভর code আর bootstrap (`listen(port, '0.0.0.0')`) বদলাতে হয়, তাই আগে code platform-agnostic করি, e2e আর load test চালাই, তারপর canary release দিই।""",
        ex_en=r"""
            - **Hidden coupling:** Passport strategies usually work, but libraries that monkey-patch Express (`req.flash`, some session stores, older upload middleware) don't. Grep for `express` imports and `@Res()` first — that's your migration list.
            - **Schema-based serialisation** is a Fastify strength, but Nest's interceptors/`ClassSerializerInterceptor` still run on the Nest side, so don't expect Fastify's full benefits automatically.
            - **Behaviour differences:** body size limits, query-string parsing and error messages for malformed JSON differ; check them in e2e tests.
            - **Measure the right thing:** compare CPU per request and tail latency at the same load, not only "requests per second" on a hello-world route.
            - Rollback is cheap if the code is platform-agnostic — that's the real value of the preparation step.
        """,
        ex_bn=r"""
            - **লুকানো coupling:** Passport strategy সাধারণত চলে, কিন্তু যেসব library Express-কে monkey-patch করে (`req.flash`, কিছু session store, পুরোনো upload middleware) সেগুলো চলে না। আগে `express` import আর `@Res()` grep করো — এটাই তোমার migration list।
            - **Schema-based serialisation** Fastify-র শক্তি, কিন্তু Nest-এর interceptor/`ClassSerializerInterceptor` তখনো Nest-এর দিকে চলে, তাই Fastify-র পুরো সুবিধা নিজে থেকে আশা কোরো না।
            - **আচরণগত পার্থক্য:** body size limit, query-string parsing আর ভুল JSON-এর error message আলাদা; e2e test-এ এগুলো check করো।
            - **ঠিক জিনিস মাপো:** একই load-এ per request CPU আর tail latency তুলনা করো, শুধু hello-world route-এ "requests per second" না।
            - Code platform-agnostic হলে rollback সস্তা — preparation step-এর আসল মূল্য এটাই।
        """,
        tip_en=r"""Start with "measure first" — interviewers test whether you chase benchmarks or solve real bottlenecks. Then list concrete breakages (`0.0.0.0`, middleware → plugins, `@Res()` code) to show hands-on knowledge.""",
        tip_bn=r""""আগে মাপো" দিয়ে শুরু করো — interviewer দেখতে চায় তুমি benchmark-এর পেছনে ছোটো নাকি আসল bottleneck সমাধান করো। তারপর নির্দিষ্ট কী ভাঙে বলো (`0.0.0.0`, middleware → plugin, `@Res()` code) — এতে hands-on জ্ঞান বোঝা যায়।""",
        mist_en=r"""Switching without profiling; forgetting `'0.0.0.0'` in containers; keeping Express middleware with `app.use()`; assuming Fastify fixes slow database queries.""",
        mist_bn=r"""Profile না করে switch করা; container-এ `'0.0.0.0'` ভুলে যাওয়া; `app.use()` দিয়ে Express middleware রেখে দেওয়া; ভাবা যে Fastify ধীর database query ঠিক করে দেবে।""",
        code=r"""
            // main.ts — Fastify adapter
            import { NestFactory } from '@nestjs/core';
            import { FastifyAdapter, type NestFastifyApplication } from '@nestjs/platform-fastify';
            import helmet from '@fastify/helmet';
            import { AppModule } from './app.module.js';

            const app = await NestFactory.create<NestFastifyApplication>(
              AppModule,
              new FastifyAdapter({ logger: false }),
            );
            await app.register(helmet); // Fastify plugin instead of Express helmet middleware
            app.enableShutdownHooks();
            await app.listen(Number(process.env.PORT ?? 3000), '0.0.0.0'); // Fastify defaults to localhost
        """,
        lang="typescript",
        follow=[
            ("How would you write a controller that works unchanged on both adapters?", "এমন controller কীভাবে লিখবে যা দুই adapter-এ কোনো পরিবর্তন ছাড়াই কাজ করে?"),
            ("Where does the time actually go in a typical NestJS request?", "একটা সাধারণ NestJS request-এ সময় আসলে কোথায় খরচ হয়?"),
        ],
        related=["nest-011", "nest-025", "nest-028"],
        refs=[NEST_PERFORMANCE],
    ),
    # ------------------------------------------------------------------ nest-027
    Q(
        id="nest-027", sub="WebSockets & Microservices", diff="hard", type="conceptual",
        prio="medium", market="both", mins=10,
        tags=["microservices", "websockets", "message-pattern", "event-pattern", "socket.io"],
        ver="NestJS 12.1 (@nestjs/microservices, @nestjs/websockets)", vs=False, status="stable",
        q_en=r"""Explain NestJS microservices fundamentals — transports, `@MessagePattern` vs `@EventPattern`, and hybrid apps — and WebSocket gateways. How would you scale a Socket.IO gateway across several instances?""",
        q_bn=r"""NestJS microservices-এর মূল বিষয় — transport, `@MessagePattern` বনাম `@EventPattern`, আর hybrid app — এবং WebSocket gateway ব্যাখ্যা করো। কয়েকটা instance জুড়ে একটা Socket.IO gateway কীভাবে scale করবে?""",
        a_en=r"""
            **Microservices:** `@nestjs/microservices` lets the same controllers/providers model talk over a transport instead of HTTP: TCP, Redis, NATS, MQTT, RabbitMQ, Kafka, gRPC or a custom one.
            - `@MessagePattern('orders.get')` = **request-response**. The caller uses `client.send()`, which returns a *cold* Observable — nothing is sent until you subscribe (e.g. `firstValueFrom()`).
            - `@EventPattern('payment.succeeded')` = **fire-and-forget event**. The caller uses `client.emit()`, which dispatches immediately; no response is expected.
            - A **hybrid app** serves HTTP and listens on a transport: `app.connectMicroservice(...)` + `app.startAllMicroservices()`.

            **WebSockets:** a `@WebSocketGateway()` class handles real-time messages with `@SubscribeMessage()`, `@MessageBody()` and `@ConnectedSocket()`; guards, pipes, interceptors and filters work there too (`WsException`). The default platform is Socket.IO; a `ws` adapter is available.

            **Scaling Socket.IO:** each instance only knows its own sockets. To broadcast to a room across instances, use the Socket.IO **Redis adapter** via a custom `IoAdapter` (pub/sub between instances), and enable **sticky sessions** at the load balancer if clients may fall back to HTTP long-polling. Authenticate during the handshake (`client.handshake.auth.token`), not on every message.

            This is advanced material for most backend roles; the interview focus is usually request-response vs events and the scaling problem.
        """,
        a_bn=r"""
            **Microservices:** `@nestjs/microservices` দিয়ে একই controller/provider model HTTP-র বদলে একটা transport-এর উপর কথা বলতে পারে: TCP, Redis, NATS, MQTT, RabbitMQ, Kafka, gRPC বা custom।
            - `@MessagePattern('orders.get')` = **request-response**। Caller `client.send()` ব্যবহার করে, যেটা একটা *cold* Observable return করে — subscribe না করা পর্যন্ত কিছুই পাঠানো হয় না (যেমন `firstValueFrom()`)।
            - `@EventPattern('payment.succeeded')` = **fire-and-forget event**। Caller `client.emit()` ব্যবহার করে, যেটা সাথে সাথে dispatch করে; কোনো response আশা করা হয় না।
            - **Hybrid app** HTTP-ও serve করে আবার transport-এও listen করে: `app.connectMicroservice(...)` + `app.startAllMicroservices()`।

            **WebSockets:** একটা `@WebSocketGateway()` class `@SubscribeMessage()`, `@MessageBody()` আর `@ConnectedSocket()` দিয়ে real-time message handle করে; guard, pipe, interceptor আর filter সেখানেও কাজ করে (`WsException`)। Default platform Socket.IO; একটা `ws` adapter-ও আছে।

            **Socket.IO scale করা:** প্রতিটা instance শুধু নিজের socket চেনে। Instance জুড়ে একটা room-এ broadcast করতে custom `IoAdapter`-এর মাধ্যমে Socket.IO **Redis adapter** ব্যবহার করো (instance-এর মধ্যে pub/sub), আর client HTTP long-polling-এ fallback করতে পারলে load balancer-এ **sticky session** চালু করো। প্রতিটা message-এ না, handshake-এর সময় authenticate করো (`client.handshake.auth.token`)।

            বেশিরভাগ backend role-এর জন্য এটা advanced বিষয়; interview-এ সাধারণত focus থাকে request-response বনাম event আর scaling-এর সমস্যায়।
        """,
        quick_en=r"""`@nestjs/microservices` runs handlers over transports like TCP, Redis, NATS or Kafka: `@MessagePattern` is request-response via `send()`, `@EventPattern` is fire-and-forget via `emit()`, and a hybrid app serves HTTP plus a transport. To scale a Socket.IO gateway, add the Redis adapter and sticky sessions.""",
        quick_bn=r"""`@nestjs/microservices` দিয়ে handler-গুলো TCP, Redis, NATS বা Kafka-র মতো transport-এ চলে: `@MessagePattern` হলো `send()` দিয়ে request-response, `@EventPattern` হলো `emit()` দিয়ে fire-and-forget, আর hybrid app HTTP-র পাশাপাশি transport-এও listen করে। Socket.IO gateway scale করতে Redis adapter আর sticky session লাগে।""",
        ex_en=r"""
            - **Delivery guarantees depend on the transport.** Redis pub/sub is at-most-once — if the consumer is down, the event is lost. For business-critical events (payments, orders) use a broker with acknowledgements and persistence (RabbitMQ, Kafka, NATS JetStream) and make consumers idempotent.
            - **v12 note:** the NATS transport moved to the `@nats-io/transport-node` (NATS v3) client package.
            - **Don't build a distributed monolith:** chains of synchronous `send()` calls between services multiply latency and failure points. Prefer events for side effects and keep request-response for real queries, with timeouts.
            - **Gateways are singletons** — don't inject request-scoped providers into them.
            - **Rooms per user** (`user:42`) make "notify this user on all their devices" a single `server.to(room).emit()`.
        """,
        ex_bn=r"""
            - **Delivery guarantee transport-এর উপর নির্ভর করে।** Redis pub/sub at-most-once — consumer বন্ধ থাকলে event হারিয়ে যায়। Business-critical event-এর (payment, order) জন্য acknowledgement আর persistence সহ broker ব্যবহার করো (RabbitMQ, Kafka, NATS JetStream), আর consumer-কে idempotent বানাও।
            - **v12 নোট:** NATS transport এখন `@nats-io/transport-node` (NATS v3) client package ব্যবহার করে।
            - **Distributed monolith বানিও না:** service-এর মধ্যে synchronous `send()` call-এর chain latency আর failure point বাড়িয়ে দেয়। Side effect-এর জন্য event, আর আসল query-র জন্য timeout সহ request-response রাখো।
            - **Gateway singleton** — এতে request-scoped provider inject কোরো না।
            - **প্রতি user-এর room** (`user:42`) থাকলে "এই user-এর সব device-এ notify করো" একটাই `server.to(room).emit()`।
        """,
        tip_en=r"""Contrast `send` vs `emit` with one real example each (get order details vs payment succeeded). Then raise delivery guarantees unprompted — that's the senior signal.""",
        tip_bn=r"""`send` আর `emit`-এর পার্থক্য একটা করে বাস্তব example দিয়ে বলো (order details আনা বনাম payment succeeded)। তারপর কেউ জিজ্ঞেস করার আগেই delivery guarantee-র কথা তোলো — এটাই senior signal।""",
        mist_en=r"""Calling `client.send()` without subscribing and wondering why nothing happens; using Redis pub/sub for events that must not be lost; scaling Socket.IO horizontally without an adapter (broadcasts reach only some users).""",
        mist_bn=r"""Subscribe না করে `client.send()` call করে ভাবা কেন কিছু হচ্ছে না; যে event হারানো চলবে না তার জন্য Redis pub/sub ব্যবহার করা; adapter ছাড়া Socket.IO horizontally scale করা (broadcast শুধু কিছু user-এর কাছে পৌঁছায়)।""",
        code=r"""
            // orders microservice — message and event handlers
            @Controller()
            export class OrdersMessagesController {
              constructor(private readonly orders: OrdersService) {}

              @MessagePattern('orders.get') // request-response
              getOrder(@Payload() id: number) {
                return this.orders.findOne(id);
              }

              @EventPattern('payment.succeeded') // fire-and-forget
              async onPaymentSucceeded(@Payload() evt: { orderId: number }) {
                await this.orders.markPaid(evt.orderId);
              }
            }

            // main.ts — hybrid app: HTTP + Redis transport
            const app = await NestFactory.create(AppModule);
            app.connectMicroservice<MicroserviceOptions>({
              transport: Transport.REDIS,
              options: { host: 'redis', port: 6379 },
            });
            await app.startAllMicroservices();
            await app.listen(3000);

            // caller side
            const order = await firstValueFrom(this.client.send('orders.get', 42)); // cold: needs subscription
            this.client.emit('payment.succeeded', { orderId: 42 });                  // hot: sent immediately

            // real-time notifications gateway
            @WebSocketGateway({ namespace: '/notifications', cors: { origin: ['https://app.example.com'] } })
            export class NotificationsGateway implements OnGatewayConnection {
              @WebSocketServer() server: Server;

              handleConnection(client: Socket) {
                const token = client.handshake.auth?.token as string | undefined;
                if (!token) client.disconnect(true); // verify the JWT here in real code
              }

              notifyOrderPaid(userId: number, orderId: number) {
                this.server.to(`user:${userId}`).emit('order.paid', { orderId });
              }
            }
        """,
        lang="typescript",
        follow=[
            ("How would you guarantee an `order.paid` event is processed exactly once?", "একটা `order.paid` event ঠিক একবারই process হবে এটা কীভাবে নিশ্চিত করবে?"),
            ("When would you choose gRPC over a message broker?", "কখন message broker-এর বদলে gRPC বেছে নেবে?"),
        ],
        related=["nest-030", "nest-032"],
        refs=[NEST_MICRO, NEST_GATEWAYS, NEST_WS_ADAPTER],
    ),
    # ------------------------------------------------------------------ nest-028
    Q(
        id="nest-028", sub="Security & Performance", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["security", "helmet", "rate-limiting", "serialization", "performance"],
        ver="NestJS 12.1 / @nestjs/throttler 6", vs=True, status="stable",
        q_en=r"""You're preparing a NestJS API for production. Which security and performance measures would you put in place, and what common traps would you check for?""",
        q_bn=r"""তুমি একটা NestJS API production-এর জন্য প্রস্তুত করছ। কোন কোন security আর performance ব্যবস্থা নেবে, আর কোন common ফাঁদগুলো check করবে?""",
        a_en=r"""
            **Security**
            - **Input:** global `ValidationPipe({ whitelist, forbidNonWhitelisted, transform })` (or Standard Schema with strict objects) to block mass assignment; body size limits (`app.useBodyParser('json', { limit: '1mb' })`).
            - **Headers & CORS:** `helmet()`; CORS with an explicit origin allow-list, never `origin: true` together with credentials.
            - **Rate limiting:** `@nestjs/throttler` as a global guard, stricter limits on login/OTP routes; a shared store (e.g. Redis) when running several instances, and `trust proxy` behind a load balancer so limits apply per client IP.
            - **Output:** never return entities blindly. `ClassSerializerInterceptor` + `@Exclude()` only works on **class instances** — a plain object from a query builder leaks `passwordHash`. Prefer selecting only the needed columns or mapping to response DTOs.
            - **Auth & secrets:** short-lived JWTs, secrets from the environment/secret manager, async password hashing (argon2/bcrypt), generic 500 errors via a global filter.

            **Performance**
            - Avoid request-scoped providers on hot paths; size DB pools for (pool × instances); add indexes for real query patterns; cache read-heavy data (Redis).
            - Keep the event loop free: no sync crypto or huge JSON work in handlers — move CPU-heavy jobs to queues (`@nestjs/bullmq`) or worker threads.
            - Graceful shutdown with `app.enableShutdownHooks()`; compression and TLS usually at the reverse proxy (NGINX/ALB).
        """,
        a_bn=r"""
            **Security**
            - **Input:** mass assignment আটকাতে global `ValidationPipe({ whitelist, forbidNonWhitelisted, transform })` (বা strict object সহ Standard Schema); body size limit (`app.useBodyParser('json', { limit: '1mb' })`)।
            - **Header ও CORS:** `helmet()`; নির্দিষ্ট origin allow-list সহ CORS, credentials-এর সাথে কখনো `origin: true` না।
            - **Rate limiting:** global guard হিসেবে `@nestjs/throttler`, login/OTP route-এ আরও কড়া limit; একাধিক instance চললে shared store (যেমন Redis), আর load balancer-এর পেছনে `trust proxy`, যাতে limit প্রতিটা client IP অনুযায়ী হয়।
            - **Output:** entity অন্ধভাবে return কোরো না। `ClassSerializerInterceptor` + `@Exclude()` শুধু **class instance**-এ কাজ করে — query builder থেকে আসা plain object `passwordHash` leak করে। দরকারি column-ই select করা বা response DTO-তে map করা ভালো।
            - **Auth ও secret:** ছোট মেয়াদের JWT, environment/secret manager থেকে secret, async password hashing (argon2/bcrypt), global filter দিয়ে generic 500 error।

            **Performance**
            - Hot path-এ request-scoped provider এড়াও; DB pool-এর size ঠিক করো (pool × instance); আসল query pattern অনুযায়ী index দাও; read-heavy data cache করো (Redis)।
            - Event loop ফাঁকা রাখো: handler-এ sync crypto বা বিশাল JSON-এর কাজ না — CPU-heavy job queue (`@nestjs/bullmq`) বা worker thread-এ পাঠাও।
            - `app.enableShutdownHooks()` দিয়ে graceful shutdown; compression আর TLS সাধারণত reverse proxy-তে (NGINX/ALB)।
        """,
        quick_en=r"""Security: strict global validation with `whitelist`, body size limits, `helmet()`, an explicit CORS allow-list, `@nestjs/throttler`, response DTOs instead of raw entities, and a generic error filter. Performance: no request-scoped providers on hot paths, sized DB pools, caching, queued CPU work and shutdown hooks.""",
        quick_bn=r"""Security-র দিকে: `whitelist`-সহ কড়া global validation, body-র আকারের সীমা, `helmet()`, নির্দিষ্ট origin-এর তালিকা দিয়ে CORS, `@nestjs/throttler`, সরাসরি entity না পাঠিয়ে response DTO, আর সাধারণ error filter। Performance-এর দিকে: ব্যস্ত পথে request-scoped provider নয়, মাপমতো DB pool, caching, CPU-ভারী কাজ queue-তে পাঠানো, আর shutdown hook চালু রাখা।""",
        ex_en=r"""
            - **Verified trap:** with `ClassSerializerInterceptor` enabled, returning `new UserEntity(row)` hides `passwordHash`, but returning the raw `row` object includes it. Many teams switch ORMs (e.g. to Drizzle, which returns plain objects) and silently lose this protection.
            - **Throttler details (v6):** `ttl` is in milliseconds, configs are named (`default`), and `@SkipThrottle()` / `@Throttle({ default: { limit, ttl } })` override per route.
            - **Logging:** use a structured async logger (e.g. pino), and redact `authorization`, cookies, passwords and OTPs.
            - **Dependencies:** keep Nest, Express and `multer` patched; run `npm audit` / Dependabot in CI.
            - **Measure:** load-test with realistic data, watch event-loop lag and p99 latency, and profile before micro-optimising (or switching adapters).
        """,
        ex_bn=r"""
            - **যাচাই করা ফাঁদ:** `ClassSerializerInterceptor` চালু থাকলে `new UserEntity(row)` return করলে `passwordHash` লুকায়, কিন্তু raw `row` object return করলে সেটা থেকে যায়। অনেক team ORM বদলায় (যেমন Drizzle-এ, যেটা plain object দেয়) আর চুপচাপ এই সুরক্ষা হারায়।
            - **Throttler detail (v6):** `ttl` millisecond-এ, config-এর নাম থাকে (`default`), আর route অনুযায়ী override করা যায় `@SkipThrottle()` / `@Throttle({ default: { limit, ttl } })` দিয়ে।
            - **Logging:** structured async logger ব্যবহার করো (যেমন pino), আর `authorization`, cookie, password, OTP redact করো।
            - **Dependency:** Nest, Express আর `multer` patched রাখো; CI-তে `npm audit` / Dependabot চালাও।
            - **মাপো:** বাস্তব data দিয়ে load-test করো, event-loop lag আর p99 latency দেখো, আর micro-optimise (বা adapter বদলানোর) আগে profile করো।
        """,
        tip_en=r"""Group your answer (input, output, identity, infrastructure, performance) instead of listing random tips. The `@Exclude()`-on-plain-objects trap is a strong, specific example to mention.""",
        tip_bn=r"""এলোমেলো tip না বলে উত্তর ভাগ করে বলো (input, output, identity, infrastructure, performance)। Plain object-এ `@Exclude()` কাজ না করার ফাঁদটা উল্লেখ করার মতো একটা শক্তিশালী, নির্দিষ্ট example।""",
        mist_en=r"""Relying on `@Exclude()` with plain objects; in-memory rate limits with several replicas; IP-based throttling without `trust proxy` (everyone shares the load balancer's IP); `bcrypt.hashSync` in request handlers.""",
        mist_bn=r"""Plain object-এ `@Exclude()`-এর উপর ভরসা করা; একাধিক replica থাকতেও in-memory rate limit; `trust proxy` ছাড়া IP-based throttling (সবাই load balancer-এর IP share করে); request handler-এ `bcrypt.hashSync`।""",
        code=r"""
            // main.ts (Express adapter)
            import { NestFactory, Reflector } from '@nestjs/core';
            import { ClassSerializerInterceptor, ValidationPipe } from '@nestjs/common';
            import type { NestExpressApplication } from '@nestjs/platform-express';
            import helmet from 'helmet';
            import { AppModule } from './app.module.js';

            const app = await NestFactory.create<NestExpressApplication>(AppModule);
            app.set('trust proxy', 1); // real client IP behind one proxy/LB
            app.use(helmet());
            app.enableCors({ origin: ['https://app.example.com'], credentials: true });
            app.useBodyParser('json', { limit: '1mb' });
            app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }));
            app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));
            app.enableShutdownHooks();
            await app.listen(process.env.PORT ?? 3000);

            // app.module.ts — global rate limit, stricter on login
            @Module({
              imports: [ThrottlerModule.forRoot([{ ttl: 60_000, limit: 100 }])],
              providers: [{ provide: APP_GUARD, useClass: ThrottlerGuard }],
            })
            export class AppModule {}

            @Controller('auth')
            export class AuthController {
              @Throttle({ default: { limit: 5, ttl: 60_000 } })
              @Post('login')
              login(@Body() dto: LoginDto) { /* ... */ }
            }
        """,
        lang="typescript",
        follow=[
            ("How would you rate-limit per user or per tenant instead of per IP?", "IP-র বদলে per user বা per tenant কীভাবে rate-limit করবে?"),
            ("How do you detect that the event loop is blocked in production?", "Production-এ event loop block হচ্ছে কি না কীভাবে ধরবে?"),
        ],
        related=["nest-015", "nest-016", "nest-023"],
        refs=[NEST_HELMET, NEST_RATE, NEST_SERIALIZATION],
    ),
    # ------------------------------------------------------------------ nest-029
    Q(
        id="nest-029", sub="Interceptors & Request Lifecycle", diff="hard", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["interceptors", "guards", "pipes", "error-handling", "rxjs"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""The interceptor below is bound globally to log every error. Which of these errors will it **NOT** see?""",
        q_bn=r"""নিচের interceptor-টা প্রতিটা error log করার জন্য globally bind করা আছে। নিচের কোন error-টা এটা **দেখতে পাবে না**?""",
        code=r"""
            @Injectable()
            export class ErrorLoggingInterceptor implements NestInterceptor {
              private readonly logger = new Logger('Errors');

              intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
                return next.handle().pipe(
                  catchError((err) => {
                    this.logger.error(err);
                    return throwError(() => err);
                  }),
                );
              }
            }
        """,
        lang="typescript",
        options=[
            ("A `BadRequestException` thrown by the global `ValidationPipe`", "Global `ValidationPipe` থেকে throw হওয়া `BadRequestException`"),
            ("An error thrown inside a service method called by the handler", "Handler যে service method call করে তার ভেতরে throw হওয়া error"),
            ("A rejected promise returned by an `async` route handler", "একটা `async` route handler-এর return করা rejected promise"),
            ("A `ForbiddenException` thrown by a guard", "একটা guard থেকে throw হওয়া `ForbiddenException`"),
        ],
        correct=3,
        a_en=r"""The guard's `ForbiddenException`. Guards run **before** interceptors, so when a guard throws, `intercept()` is never called. Pipes, the handler and services all run inside `next.handle()`, so their errors flow through the interceptor's `catchError`.""",
        a_bn=r"""Guard-এর `ForbiddenException`। Guard interceptor-এর **আগে** চলে, তাই guard throw করলে `intercept()` কখনো call-ই হয় না। Pipe, handler আর service সবই `next.handle()`-এর ভেতরে চলে, তাই তাদের error interceptor-এর `catchError` দিয়ে যায়।""",
        quick_en=r"""The `ForbiddenException` thrown by a guard. Guards run before interceptors, so `intercept()` is never called, while errors from pipes, the handler and services all flow through `next.handle()`.""",
        quick_bn=r"""Guard-এর throw করা `ForbiddenException`। Guard interceptor-এর আগে চলে, তাই `intercept()` call-ই হয় না; অথচ pipe, handler আর service-এর error সব `next.handle()`-এর ভেতর দিয়ে interceptor-এ পৌঁছায়।""",
        ex_en=r"""
            The tempting wrong answer is the pipe error: pipes feel "earlier" than interceptors. But in Nest's execution order, the interceptor chain wraps a function that first applies pipes and then calls the handler — so a validation failure surfaces as an error on the `next.handle()` stream. (Verified on NestJS 12.1: a guard's 403 never reached the interceptor, while `ParseIntPipe` and `ValidationPipe` errors did.)

            Practical consequence: if you rely on an interceptor for error logging or metrics, auth failures (401/403) and middleware errors are invisible to it. Use a global exception filter (or middleware/`res.on('finish')` logging) when you need every error and status code.
        """,
        ex_bn=r"""
            লোভনীয় ভুল উত্তর হলো pipe-এর error: মনে হয় pipe interceptor-এর "আগে" চলে। কিন্তু Nest-এর execution order-এ interceptor chain এমন একটা function-কে wrap করে যেটা আগে pipe apply করে তারপর handler call করে — তাই validation fail হলে সেটা `next.handle()` stream-এ error হিসেবে আসে। (NestJS 12.1-এ যাচাই করা: guard-এর 403 কখনো interceptor-এ পৌঁছায়নি, কিন্তু `ParseIntPipe` আর `ValidationPipe`-এর error পৌঁছেছে।)

            Practical ফলাফল: error logging বা metrics-এর জন্য interceptor-এর উপর নির্ভর করলে auth failure (401/403) আর middleware error তার কাছে অদৃশ্য। প্রতিটা error আর status code দরকার হলে global exception filter (বা middleware/`res.on('finish')` logging) ব্যবহার করো।
        """,
        tip_en=r"""Explain the mechanism in one sentence — "pipes run inside `next.handle()`, guards run before `intercept()`" — then give the logging consequence. That's what makes it a senior answer.""",
        tip_bn=r"""এক বাক্যে mechanism বোঝাও — "pipe চলে `next.handle()`-এর ভেতরে, guard চলে `intercept()`-এর আগে" — তারপর logging-এর ফলাফলটা বলো। এটাই উত্তরটাকে senior-level বানায়।""",
        related=["nest-012", "nest-013"],
        refs=[NEST_LIFECYCLE, NEST_INTERCEPTORS],
    ),
    # ------------------------------------------------------------------ nest-030
    Q(
        id="nest-030", sub="Application Architecture", diff="extreme", type="architecture",
        prio="medium", market="international", mins=20,
        tags=["modular-monolith", "cqrs", "domain-events", "outbox", "microservices"],
        ver="NestJS 12.1 (@nestjs/cqrs 12, @nestjs/microservices 12)", vs=False, status="stable",
        q_en=r"""Your NestJS e-commerce backend (catalog, orders, payments, inventory, notifications) has grown to ~40 modules and 8 developers. Modules import each other freely, changes break unrelated features, and management asks about "moving to microservices". How would you restructure it, and how would you decide what (if anything) to extract?""",
        q_bn=r"""তোমার NestJS e-commerce backend (catalog, orders, payments, inventory, notifications) এখন প্রায় ৪০টা module আর ৮ জন developer-এ বড় হয়েছে। Module গুলো যথেচ্ছ একে অপরকে import করে, একটা পরিবর্তনে সম্পর্কহীন feature ভেঙে যায়, আর management "microservices-এ যাওয়া" নিয়ে জানতে চায়। তুমি কীভাবে এটা পুনর্গঠন করবে, আর কী (যদি কিছু থাকে) আলাদা করবে সেটা কীভাবে ঠিক করবে?""",
        a_en=r"""
            This is advanced material. My recommendation: first turn it into a **modular monolith**, then extract services only where there's a concrete reason.

            **1. Boundaries:** group the 40 modules into a few bounded contexts — Catalog, Orders, Payments, Inventory, Notifications, Identity. Each context is a top-level Nest module whose `exports` is a small **facade** (e.g. `OrdersFacade`); repositories and entities stay private. Each context owns its tables (ideally its own PostgreSQL schema); no cross-context joins or writes.

            **2. Communication:**
            - Queries across contexts go through exported facades (synchronous, in-process).
            - Side effects use **domain events** (`OrderPlaced` → reserve stock, send SMS), via `@nestjs/event-emitter` or the `@nestjs/cqrs` `EventBus`.
            - For reliability, write events to an **outbox table in the same transaction** as the state change; a relay publishes them to a queue/broker. In-process events alone are lost if the process crashes mid-way.

            **3. Enforce it:** lint rules for allowed imports (dependency-cruiser / ESLint boundaries), CODEOWNERS per context, contract tests for facades, and dependencies pointing one way.

            **4. Extract only when justified:** a different scaling profile (notifications spikes), independent deploy cadence, separate team ownership, or isolation needs (payments/PCI). Because events already flow through the outbox, extraction means swapping an in-process consumer for a microservice consuming from the broker — a strangler-style step, not a rewrite.

            **Trade-off:** microservices add network failures, sagas instead of DB transactions, distributed tracing and on-call load. For 8 developers, a well-structured monolith plus one or two extracted services is usually the sweet spot.
        """,
        a_bn=r"""
            এটা advanced বিষয়। আমার সুপারিশ: আগে এটাকে একটা **modular monolith** বানাও, তারপর শুধু নির্দিষ্ট কারণ থাকলে service আলাদা করো।

            **১. Boundary:** ৪০টা module-কে কয়েকটা bounded context-এ ভাগ করো — Catalog, Orders, Payments, Inventory, Notifications, Identity। প্রতিটা context একটা top-level Nest module, যার `exports` হলো ছোট একটা **facade** (যেমন `OrdersFacade`); repository আর entity private থাকে। প্রতিটা context নিজের table-এর মালিক (আদর্শভাবে নিজের PostgreSQL schema); context-এর বাইরে join বা write নেই।

            **২. যোগাযোগ:**
            - Context-এর বাইরে query যায় exported facade দিয়ে (synchronous, in-process)।
            - Side effect-এর জন্য **domain event** (`OrderPlaced` → stock reserve, SMS পাঠানো), `@nestjs/event-emitter` বা `@nestjs/cqrs`-এর `EventBus` দিয়ে।
            - নির্ভরযোগ্যতার জন্য state change-এর **একই transaction-এ outbox table-এ** event লেখো; একটা relay সেটা queue/broker-এ publish করে। শুধু in-process event হলে process মাঝপথে crash করলে event হারিয়ে যায়।

            **৩. Enforce করো:** অনুমোদিত import-এর জন্য lint rule (dependency-cruiser / ESLint boundaries), প্রতিটা context-এর CODEOWNERS, facade-এর contract test, আর dependency এক দিকে।

            **৪. যুক্তি থাকলে তবেই আলাদা করো:** আলাদা scaling profile (notification-এ হঠাৎ spike), স্বাধীন deploy cadence, আলাদা team ownership, বা isolation-এর প্রয়োজন (payments/PCI)। Event যেহেতু আগেই outbox দিয়ে যাচ্ছে, আলাদা করা মানে in-process consumer-কে broker থেকে consume করা একটা microservice দিয়ে বদলানো — strangler-ধরনের একটা ধাপ, rewrite না।

            **Trade-off:** microservices network failure, DB transaction-এর বদলে saga, distributed tracing আর on-call-এর চাপ যোগ করে। ৮ জন developer-এর জন্য সাধারণত একটা ভালোভাবে গোছানো monolith আর এক-দুটো আলাদা service-ই সবচেয়ে ভালো।
        """,
        quick_en=r"""First make it a modular monolith: bounded contexts that export only small facades, own their tables and talk through domain events written to an outbox, with import rules enforced by lint. Extract a service only for a concrete reason such as a different scaling profile, team ownership or isolation needs.""",
        quick_bn=r"""আগে modular monolith বানাই: bounded context-গুলো শুধু ছোট facade export করে, নিজের table নিজে রাখে, আর outbox-এ লেখা domain event দিয়ে কথা বলে; import rule lint দিয়ে enforce করি। আলাদা service তখনই বের করি যখন আলাদা scaling, team ownership বা isolation-এর মতো স্পষ্ট কারণ থাকে।""",
        ex_en=r"""
            **Components:** API layer (controllers per context) → facades → domain services → repositories (Drizzle/TypeORM) → PostgreSQL schemas per context; outbox relay → broker (RabbitMQ/Kafka/NATS JetStream or BullMQ for simpler cases) → consumers.

            **CQRS:** use `@nestjs/cqrs` (CommandBus/QueryBus/EventBus, sagas) where reads and writes really diverge — e.g. an order-reporting read model fed by events. Applying CQRS everywhere adds ceremony without benefit.

            **Failure scenarios to discuss:**
            - Event consumer fails → retries with backoff, dead-letter queue, idempotent handlers (dedupe by event id).
            - Outbox relay down → events accumulate safely; alert on outbox lag.
            - Schema migrations: each context migrates only its own tables; expand–contract for shared contracts.

            **Monorepo:** Nest CLI monorepo mode or Nx keeps contexts as libraries with enforced boundaries; NestJS 12 uses Rspack by default for monorepo builds.
        """,
        ex_bn=r"""
            **Component:** API layer (প্রতিটা context-এর controller) → facade → domain service → repository (Drizzle/TypeORM) → প্রতিটা context-এর PostgreSQL schema; outbox relay → broker (RabbitMQ/Kafka/NATS JetStream, বা সহজ ক্ষেত্রে BullMQ) → consumer।

            **CQRS:** যেখানে read আর write সত্যিই আলাদা, সেখানে `@nestjs/cqrs` (CommandBus/QueryBus/EventBus, saga) ব্যবহার করো — যেমন event থেকে তৈরি একটা order-reporting read model। সব জায়গায় CQRS দিলে লাভ ছাড়াই আনুষ্ঠানিকতা বাড়ে।

            **যে failure scenario গুলো আলোচনা করবে:**
            - Event consumer fail → backoff সহ retry, dead-letter queue, idempotent handler (event id দিয়ে dedupe)।
            - Outbox relay বন্ধ → event নিরাপদে জমা থাকে; outbox lag-এ alert।
            - Schema migration: প্রতিটা context শুধু নিজের table migrate করে; shared contract-এর জন্য expand–contract।

            **Monorepo:** Nest CLI monorepo mode বা Nx context গুলোকে enforced boundary সহ library হিসেবে রাখে; NestJS 12 monorepo build-এ default-এ Rspack ব্যবহার করে।
        """,
        tip_en=r"""Push back gently on "microservices" as a goal — talk about the actual pain (coupling) and fix that first. Interviewers for senior roles want to hear criteria for extraction, the outbox pattern, and honest trade-offs.""",
        tip_bn=r"""লক্ষ্য হিসেবে "microservices"-এর বিরুদ্ধে নম্রভাবে যুক্তি দাও — আসল সমস্যা (coupling) নিয়ে কথা বলো আর আগে সেটা ঠিক করো। Senior role-এর interviewer আলাদা করার criteria, outbox pattern আর সৎ trade-off শুনতে চায়।""",
        mist_en=r"""Splitting into microservices along technical layers (an "auth service", a "database service"); sharing one database between services; relying on in-process events for critical side effects; extracting before boundaries are clean (creates a distributed monolith).""",
        mist_bn=r"""Technical layer ধরে microservice ভাগ করা (একটা "auth service", একটা "database service"); service-এর মধ্যে একই database share করা; গুরুত্বপূর্ণ side effect-এর জন্য in-process event-এর উপর ভরসা; boundary পরিষ্কার হওয়ার আগেই আলাদা করা (distributed monolith তৈরি হয়)।""",
        code=r"""
            // orders/orders.module.ts — the context's public API is only the facade
            @Module({
              imports: [CatalogModule], // uses CatalogFacade, never Catalog's repositories
              providers: [OrdersFacade, PlaceOrderService, OrdersRepository],
              exports: [OrdersFacade],
            })
            export class OrdersModule {}

            // orders/place-order.service.ts — state change + event in ONE transaction (outbox)
            @Injectable()
            export class PlaceOrderService {
              constructor(@Inject(DRIZZLE) private readonly db: Database, private readonly catalog: CatalogFacade) {}

              async placeOrder(cmd: PlaceOrderCommand) {
                const prices = await this.catalog.getPrices(cmd.items.map((i) => i.productId));
                return this.db.transaction(async (tx) => {
                  const [order] = await tx.insert(orders).values(toOrderRow(cmd, prices)).returning();
                  await tx.insert(outbox).values({ type: 'order.placed', payload: { orderId: order.id } });
                  return order;
                });
              }
            }
            // A relay polls `outbox` and publishes to the broker; Inventory and Notifications consume
            // 'order.placed' idempotently — in-process today, as separate services later if needed.
        """,
        lang="typescript",
        follow=[
            ("How would you implement the outbox relay, and how do you avoid publishing an event twice?", "Outbox relay কীভাবে implement করবে, আর একটা event দুবার publish হওয়া কীভাবে এড়াবে?"),
            ("How do you handle a multi-step checkout across services without a distributed transaction?", "Distributed transaction ছাড়া একাধিক service জুড়ে multi-step checkout কীভাবে handle করবে?"),
        ],
        related=["nest-001", "nest-024", "nest-027"],
        refs=[NEST_MODULES, NEST_CQRS, NEST_MICRO],
    ),
    # ------------------------------------------------------------------ nest-031
    Q(
        id="nest-031", sub="Application Architecture", diff="extreme", type="system-design",
        prio="medium", market="international", mins=25,
        tags=["multi-tenancy", "row-level-security", "durable-providers", "asynclocalstorage", "saas"],
        ver="NestJS 12.1 / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""Design the backend of a multi-tenant SaaS (e.g. inventory/POS software used by thousands of shops) on NestJS and PostgreSQL. Cover tenant resolution, data isolation, how tenant context flows through the app, background jobs, and the main failure risks.""",
        q_bn=r"""NestJS আর PostgreSQL দিয়ে একটা multi-tenant SaaS-এর backend design করো (যেমন হাজার হাজার দোকান যে inventory/POS software ব্যবহার করে)। Tenant resolution, data isolation, app-এর ভেতর দিয়ে tenant context কীভাবে যায়, background job, আর প্রধান failure ঝুঁকিগুলো আলোচনা করো।""",
        a_en=r"""
            This is advanced, senior-level material.

            **Requirements to clarify:** number and size of tenants, isolation/compliance needs (do some customers demand a dedicated DB?), per-tenant customisation, expected noisy neighbours.

            **1. Tenant resolution:** derive the tenant from a trusted source — a verified JWT claim (`tenantId`) and/or a subdomain mapped in the DB — and check the user's membership in a guard. Never trust a raw `x-tenant-id` header on its own.

            **2. Tenant context:** middleware/guard stores `{ tenantId, userId, requestId }` in **AsyncLocalStorage** (e.g. `nestjs-cls`), so singleton services and repositories can read it without request-scoped DI.

            **3. Data isolation — pick per tier:**
            - **Shared tables + `tenant_id` + PostgreSQL Row-Level Security** (default for most shops): every transaction runs `set_config('app.tenant_id', $1, true)` and RLS policies filter rows. Cheap, scales to thousands of tenants; RLS is defence in depth against a forgotten `WHERE`.
            - **Schema per tenant:** stronger separation, but migrations run N times.
            - **Database per tenant** for large/enterprise customers: strongest isolation; requires per-tenant connection management — Nest **durable providers** (`durable: true` + `ContextIdStrategy`) can keep one DI sub-tree (and pool) per tenant, with a bounded cache.
            A hybrid (shared by default, dedicated for enterprise) is common.

            **4. Everything else is tenant-aware:** cache keys (`t:{tenantId}:...`), rate limits per tenant (custom throttler tracker), file storage prefixes, logs/traces tagged with the tenant id, and **background jobs carry `tenantId` explicitly in the payload** (there's no request context in a worker).

            **5. Failure risks:** cross-tenant leaks (missing filter, cache-key collision, wrong context in async callbacks), connection exhaustion with DB-per-tenant, a migration that succeeds for some tenant schemas but not others, and one big tenant starving others.
        """,
        a_bn=r"""
            এটা advanced, senior-level বিষয়।

            **যে requirement গুলো clarify করব:** tenant-এর সংখ্যা ও আকার, isolation/compliance-এর প্রয়োজন (কোনো customer কি dedicated DB চায়?), per-tenant customisation, noisy neighbour-এর সম্ভাবনা।

            **১. Tenant resolution:** বিশ্বস্ত source থেকে tenant বের করো — verified JWT claim (`tenantId`) আর/বা DB-তে map করা subdomain — আর একটা guard-এ user-এর membership check করো। শুধু raw `x-tenant-id` header-কে কখনো বিশ্বাস কোরো না।

            **২. Tenant context:** middleware/guard `{ tenantId, userId, requestId }` **AsyncLocalStorage**-এ রাখে (যেমন `nestjs-cls`), ফলে singleton service আর repository request-scoped DI ছাড়াই সেটা পড়তে পারে।

            **৩. Data isolation — tier অনুযায়ী বাছাই:**
            - **Shared table + `tenant_id` + PostgreSQL Row-Level Security** (বেশিরভাগ দোকানের জন্য default): প্রতিটা transaction-এ `set_config('app.tenant_id', $1, true)` চলে আর RLS policy row filter করে। সস্তা, হাজার হাজার tenant-এ scale করে; ভুলে যাওয়া `WHERE`-এর বিরুদ্ধে RLS হলো defence in depth।
            - **Tenant প্রতি schema:** বেশি আলাদা, কিন্তু migration N বার চলে।
            - **Tenant প্রতি database** বড়/enterprise customer-এর জন্য: সবচেয়ে শক্ত isolation; per-tenant connection management লাগে — Nest-এর **durable provider** (`durable: true` + `ContextIdStrategy`) প্রতি tenant-এ একটা DI sub-tree (আর pool) রাখতে পারে, সীমিত cache সহ।
            Hybrid (default-এ shared, enterprise-এর জন্য dedicated) খুবই common।

            **৪. বাকি সবকিছুও tenant-aware:** cache key (`t:{tenantId}:...`), tenant অনুযায়ী rate limit (custom throttler tracker), file storage prefix, tenant id সহ log/trace, আর **background job payload-এ `tenantId` explicitly থাকে** (worker-এ কোনো request context নেই)।

            **৫. Failure ঝুঁকি:** tenant-এর মধ্যে data leak (filter বাদ পড়া, cache-key collision, async callback-এ ভুল context), DB-per-tenant-এ connection শেষ হয়ে যাওয়া, এমন migration যা কিছু tenant schema-য় সফল কিন্তু বাকিগুলোতে না, আর একটা বড় tenant অন্যদের resource খেয়ে ফেলা।
        """,
        quick_en=r"""Resolve the tenant from a verified JWT claim or subdomain, keep it in AsyncLocalStorage, and default to shared tables with `tenant_id` plus PostgreSQL Row-Level Security, with dedicated databases for big tenants. Make caches, rate limits and jobs tenant-aware; the main risk is cross-tenant data leaks.""",
        quick_bn=r"""Tenant বের করি verified JWT claim বা subdomain থেকে, AsyncLocalStorage-এ রাখি, আর default হিসেবে `tenant_id`-সহ shared table আর PostgreSQL Row-Level Security; বড় tenant-এর জন্য আলাদা database। Cache, rate limit আর job-ও tenant-aware করি; সবচেয়ে বড় risk হলো এক tenant-এর data আরেক tenant-এর কাছে leak হওয়া।""",
        ex_en=r"""
            **RLS details that matter:**
            - `ALTER TABLE orders ENABLE ROW LEVEL SECURITY; ALTER TABLE orders FORCE ROW LEVEL SECURITY;` — without `FORCE`, the table owner bypasses policies.
            - The application role must not be a superuser or have `BYPASSRLS`.
            - Use `set_config(..., true)` (transaction-local) inside the same transaction as the queries; with PgBouncer in transaction mode, a session-level `SET` would leak to the next client.
            - Policy example: `CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::uuid);`

            **Testing isolation:** automated tests that log in as tenant A and try to read tenant B's ids on every endpoint; alert on any cross-tenant access in audit logs.

            **Scaling:** shard large tenants to separate databases later via a tenant → database routing table; the ALS context makes the routing decision in one place.

            **Durable-provider gotcha:** `ContextIdStrategy.attach()` runs when Nest resolves the request-scoped handler — *before* guards. If authentication happens in a guard, `request.user` is still empty there, so verify the JWT (or resolve the tenant) in middleware for this path.
        """,
        ex_bn=r"""
            **RLS-এর গুরুত্বপূর্ণ detail:**
            - `ALTER TABLE orders ENABLE ROW LEVEL SECURITY; ALTER TABLE orders FORCE ROW LEVEL SECURITY;` — `FORCE` না দিলে table owner policy bypass করে।
            - Application role superuser হবে না, বা `BYPASSRLS` থাকবে না।
            - Query-র একই transaction-এর ভেতরে `set_config(..., true)` (transaction-local) ব্যবহার করো; transaction mode-এ PgBouncer থাকলে session-level `SET` পরের client-এর কাছে leak করবে।
            - Policy-র উদাহরণ: `CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::uuid);`

            **Isolation test:** automated test যেটা tenant A হিসেবে login করে প্রতিটা endpoint-এ tenant B-র id পড়ার চেষ্টা করে; audit log-এ যেকোনো cross-tenant access-এ alert।

            **Scaling:** পরে tenant → database routing table দিয়ে বড় tenant-কে আলাদা database-এ shard করো; ALS context routing-এর সিদ্ধান্ত এক জায়গায় নিতে দেয়।

            **Durable provider-এর ফাঁদ:** Nest যখন request-scoped handler resolve করে তখন `ContextIdStrategy.attach()` চলে — guard-এর *আগে*। Authentication যদি guard-এ হয়, তাহলে সেখানে `request.user` তখনও খালি থাকে; তাই এই path-এর জন্য JWT verify (বা tenant resolve) middleware-এ করো।
        """,
        tip_en=r"""Present the three isolation models as a spectrum with costs, then pick a default and justify it. Bringing up `FORCE ROW LEVEL SECURITY`, transaction-local settings with PgBouncer, and tenant ids in job payloads shows real production depth.""",
        tip_bn=r"""তিনটা isolation model-কে খরচ সহ একটা spectrum হিসেবে দেখাও, তারপর একটা default বেছে যুক্তি দাও। `FORCE ROW LEVEL SECURITY`, PgBouncer-এর সাথে transaction-local setting, আর job payload-এ tenant id-এর কথা তুললে আসল production গভীরতা বোঝা যায়।""",
        mist_en=r"""Trusting a client-supplied tenant header; relying only on developers remembering `WHERE tenant_id = ?`; session-level `SET` behind a transaction-mode pooler; unbounded per-tenant connection pools; cache keys without the tenant id.""",
        mist_bn=r"""Client-এর পাঠানো tenant header বিশ্বাস করা; শুধু developer-রা `WHERE tenant_id = ?` মনে রাখবে এই ভরসায় থাকা; transaction-mode pooler-এর পেছনে session-level `SET`; সীমাহীন per-tenant connection pool; tenant id ছাড়া cache key।""",
        code=r"""
            // 1) Shared-schema isolation with RLS: set the tenant per transaction (Drizzle)
            type Tx = Parameters<Parameters<Database['transaction']>[0]>[0];

            export async function withTenant<T>(db: Database, tenantId: string, fn: (tx: Tx) => Promise<T>) {
              return db.transaction(async (tx) => {
                await tx.execute(sql`select set_config('app.tenant_id', ${tenantId}, true)`); // transaction-local
                return fn(tx); // RLS policies now filter every query in this transaction
              });
            }

            // 2) Dedicated-DB tenants: durable providers keep one DI sub-tree per tenant
            const tenantTrees = new Map<string, ContextId>(); // bound this (LRU) in production

            export class TenantContextIdStrategy implements ContextIdStrategy {
              attach(contextId: ContextId, request: Request & { user?: { tenantId?: string } }) {
                // attach() runs BEFORE guards, so request.user must be set by JWT-verifying middleware
                const tenantId = request.user?.tenantId; // from the verified JWT, not a raw header
                if (!tenantId) return () => contextId;

                let tenantSubTreeId = tenantTrees.get(tenantId);
                if (!tenantSubTreeId) {
                  tenantSubTreeId = ContextIdFactory.create();
                  tenantTrees.set(tenantId, tenantSubTreeId);
                }
                return {
                  resolve: (info: HostComponentInfo) => (info.isTreeDurable ? tenantSubTreeId : contextId),
                  payload: { tenantId },
                };
              }
            }

            // main.ts
            ContextIdFactory.apply(new TenantContextIdStrategy());

            @Injectable({ scope: Scope.REQUEST, durable: true })
            export class TenantDatabase {
              // for durable providers, REQUEST holds the payload ({ tenantId }), not the request
              constructor(@Inject(REQUEST) private readonly ctx: { tenantId: string }) {}
            }
        """,
        lang="typescript",
        follow=[
            ("How would you run migrations safely across 500 tenant schemas?", "৫০০টা tenant schema-জুড়ে নিরাপদে migration কীভাবে চালাবে?"),
            ("How do you stop one large tenant from degrading everyone else?", "একটা বড় tenant যাতে বাকিদের performance খারাপ না করে, সেটা কীভাবে আটকাবে?"),
        ],
        related=["nest-023", "drizzle-030"],
        refs=[NEST_SCOPES, PG_RLS, OWASP_MULTI_TENANT],
    ),
    # ------------------------------------------------------------------ nest-032
    Q(
        id="nest-032", sub="Reliability & Idempotency", diff="extreme", type="scenario",
        prio="high", market="both", mins=20,
        tags=["idempotency", "webhooks", "concurrency", "outbox", "payments"],
        ver="NestJS 12.1 / Drizzle ORM 0.45 / PostgreSQL 18", vs=False, status="stable",
        q_en=r"""Incident: your NestJS API runs on 3 instances. The payment gateway (e.g. bKash or SSLCommerz) retries webhooks when it doesn't get a fast 200. Some orders are marked paid twice and customers receive two confirmation SMS; once, two orders were created from one double-clicked "Place order". How do you diagnose and fix this properly?""",
        q_bn=r"""Incident: তোমার NestJS API ৩টা instance-এ চলে। Payment gateway (যেমন bKash বা SSLCommerz) দ্রুত 200 না পেলে webhook আবার পাঠায়। কিছু order দুবার paid mark হচ্ছে আর customer দুটো confirmation SMS পাচ্ছে; একবার, double-click করা একটা "Place order" থেকে দুটো order তৈরি হয়েছে। কীভাবে diagnose করবে আর ঠিকভাবে সমাধান করবে?""",
        a_en=r"""
            This is an advanced production scenario.

            **Diagnose:** correlate logs across instances by the gateway's event id — you'll see the same event handled twice, often concurrently on different pods (the retry arrives while the first attempt is still running). The root cause is a **check-then-act** handler ("if not processed → process") with no atomic guard, plus side effects (SMS) executed inline.

            **Fix — make every step idempotent, with the database as the source of truth:**
            1. **Verify the signature** on the raw body (`NestFactory.create(AppModule, { rawBody: true })`, `RawBodyRequest`) and reject unsigned calls.
            2. **Dedupe atomically:** a `processed_events` table with a unique constraint on `(provider, event_id)`. Inside one transaction: `INSERT ... ON CONFLICT DO NOTHING RETURNING id`; if no row comes back, it's a duplicate → return 200 and stop. A concurrent duplicate blocks on the unique index until the first commits, then sees the conflict.
            3. **Conditional state transition:** `UPDATE orders SET status = 'paid' WHERE id = $1 AND status = 'pending'` — repeated calls change nothing.
            4. **Side effects via an outbox** row in the same transaction; a worker sends the SMS and records the message id, so retries don't double-send.
            5. **Respond fast** (acknowledge within the gateway's timeout) and do slow work asynchronously, which also reduces retries.
            6. **Client-side double submits:** require an `Idempotency-Key` header on `POST /orders`, stored with a unique constraint and the saved response. NestJS also recently published an official `@nestjs/idempotency` package (`@Idempotent()`), but it's very new (0.0.x) — evaluate it, or implement the same pattern with an interceptor + DB store.

            Redis locks alone are not enough (TTL expiry, failover); the unique constraint is what guarantees correctness.
        """,
        a_bn=r"""
            এটা একটা advanced production scenario।

            **Diagnose:** gateway-র event id দিয়ে সব instance-এর log মেলাও — দেখবে একই event দুবার handle হয়েছে, প্রায়ই আলাদা pod-এ একই সময়ে (প্রথম চেষ্টা চলার মধ্যেই retry এসে গেছে)। Root cause হলো atomic guard ছাড়া একটা **check-then-act** handler ("process না হয়ে থাকলে → process করো"), আর inline চালানো side effect (SMS)।

            **সমাধান — প্রতিটা ধাপ idempotent করো, আর database-কে source of truth রাখো:**
            1. Raw body-র উপর **signature verify করো** (`NestFactory.create(AppModule, { rawBody: true })`, `RawBodyRequest`), unsigned call reject করো।
            2. **Atomically dedupe:** `(provider, event_id)`-এর উপর unique constraint সহ একটা `processed_events` table। একটা transaction-এর ভেতরে: `INSERT ... ON CONFLICT DO NOTHING RETURNING id`; কোনো row ফেরত না এলে এটা duplicate → 200 দিয়ে থেমে যাও। একই সময়ের duplicate প্রথমটা commit না হওয়া পর্যন্ত unique index-এ আটকে থাকে, তারপর conflict দেখে।
            3. **শর্তসাপেক্ষ state transition:** `UPDATE orders SET status = 'paid' WHERE id = $1 AND status = 'pending'` — বারবার call করলেও কিছু বদলায় না।
            4. **Side effect outbox দিয়ে**, একই transaction-এ একটা row; একটা worker SMS পাঠায় আর message id record করে, তাই retry হলেও দুবার যায় না।
            5. **দ্রুত response দাও** (gateway-র timeout-এর মধ্যে acknowledge), ধীর কাজ asynchronously করো — এতে retry-ও কমে।
            6. **Client-এর double submit:** `POST /orders`-এ `Idempotency-Key` header বাধ্যতামূলক করো, unique constraint আর saved response সহ store করো। NestJS সম্প্রতি একটা official `@nestjs/idempotency` package-ও (`@Idempotent()`) publish করেছে, কিন্তু এটা একদম নতুন (0.0.x) — evaluate করো, নয়তো interceptor + DB store দিয়ে একই pattern implement করো।

            শুধু Redis lock যথেষ্ট না (TTL শেষ হওয়া, failover); correctness নিশ্চিত করে unique constraint।
        """,
        quick_en=r"""The root cause is a non-atomic check-then-act handler running concurrently on several instances. Verify the signature, dedupe with a unique `(provider, event_id)` row via `ON CONFLICT DO NOTHING`, use a conditional `UPDATE`, send SMS through an outbox, and require an `Idempotency-Key` on `POST /orders`.""",
        quick_bn=r"""মূল কারণ একটা non-atomic check-then-act handler, যেটা কয়েকটা instance-এ একসাথে চলে। Signature verify করি, `ON CONFLICT DO NOTHING` দিয়ে unique `(provider, event_id)` row রেখে dedupe করি, status বদলানো conditional `UPDATE` দিয়ে করি, SMS outbox দিয়ে পাঠাই, আর `POST /orders`-এ `Idempotency-Key` বাধ্যতামূলক করি।""",
        ex_en=r"""
            - **Why the unique constraint works under concurrency:** PostgreSQL's unique index makes the second inserter wait for the first transaction; on commit it gets a conflict (`DO NOTHING` → zero rows), on rollback it proceeds. No race window, no distributed lock.
            - **Keep the dedupe insert and the state change in the same transaction** — otherwise a crash between them marks the event processed without updating the order.
            - **Idempotency-Key semantics (for client requests):** same key + same body → replay the stored response; same key while the first request is still running → 409 with `Retry-After`; same key + different body → 422.
            - **Verification:** a test that fires the same webhook 10 times concurrently and asserts one status change and one outbox row; a metric on duplicate deliveries (useful to tune timeouts).
            - **Ordering:** gateways may deliver events out of order (refund before success). The state machine must reject invalid transitions rather than blindly applying the latest event.
        """,
        ex_bn=r"""
            - **Concurrency-তে unique constraint কেন কাজ করে:** PostgreSQL-এর unique index দ্বিতীয় inserter-কে প্রথম transaction-এর জন্য অপেক্ষা করায়; commit হলে conflict পায় (`DO NOTHING` → শূন্য row), rollback হলে এগিয়ে যায়। কোনো race window নেই, distributed lock লাগে না।
            - **Dedupe insert আর state change একই transaction-এ রাখো** — নাহলে মাঝখানে crash হলে event processed mark হয়ে যাবে অথচ order update হবে না।
            - **Idempotency-Key-এর নিয়ম (client request-এর জন্য):** একই key + একই body → stored response replay; প্রথম request চলার সময় একই key → `Retry-After` সহ 409; একই key + আলাদা body → 422।
            - **যাচাই:** একটা test যেটা একই webhook একসাথে ১০ বার পাঠায় আর assert করে একটাই status change আর একটাই outbox row; duplicate delivery-র একটা metric (timeout tune করতে কাজে লাগে)।
            - **ক্রম:** gateway event উল্টো ক্রমে পাঠাতে পারে (success-এর আগে refund)। State machine অবৈধ transition reject করবে, অন্ধভাবে শেষ event apply করবে না।
        """,
        tip_en=r"""Use the incident structure: impact → timeline/evidence → root cause → fix → prevention. Saying "at-least-once delivery means handlers must be idempotent, and the DB constraint is the real guard" is the key senior insight.""",
        tip_bn=r"""Incident-এর কাঠামো ব্যবহার করো: impact → timeline/প্রমাণ → root cause → fix → prevention। "At-least-once delivery মানে handler-কে idempotent হতেই হবে, আর আসল পাহারাদার DB constraint" — এই কথাটাই মূল senior insight।""",
        mist_en=r"""Checking "already processed?" with a SELECT before processing (race); deduplicating in memory per instance; sending SMS inside the request transaction; trusting webhooks without signature verification; using only a Redis lock with a TTL.""",
        mist_bn=r"""Process করার আগে SELECT দিয়ে "আগে process হয়েছে?" check করা (race); প্রতিটা instance-এ memory-তে dedupe করা; request transaction-এর ভেতরে SMS পাঠানো; signature verify না করে webhook বিশ্বাস করা; শুধু TTL সহ Redis lock-এর উপর নির্ভর করা।""",
        code=r"""
            // main.ts: const app = await NestFactory.create(AppModule, { rawBody: true });

            @Controller('webhooks')
            export class PaymentWebhooksController {
              constructor(@Inject(DRIZZLE) private readonly db: Database, private readonly config: ConfigService) {}

              @Post('payments')
              @HttpCode(200)
              async handle(
                @Req() req: RawBodyRequest<Request>,
                @Headers('x-signature') signature: string | undefined,
                @Body() event: PaymentEvent,
              ) {
                const expected = createHmac('sha256', this.config.getOrThrow<string>('GATEWAY_WEBHOOK_SECRET'))
                  .update(req.rawBody ?? Buffer.alloc(0))
                  .digest('hex');
                if (!signature || signature.length !== expected.length ||
                    !timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) {
                  throw new UnauthorizedException('Bad signature');
                }

                return this.db.transaction(async (tx) => {
                  const inserted = await tx
                    .insert(processedEvents) // UNIQUE (provider, event_id)
                    .values({ provider: 'gateway', eventId: event.id })
                    .onConflictDoNothing({ target: [processedEvents.provider, processedEvents.eventId] })
                    .returning({ id: processedEvents.id });
                  if (inserted.length === 0) return { duplicate: true }; // already handled

                  const updated = await tx
                    .update(orders)
                    .set({ status: 'paid' })
                    .where(and(eq(orders.id, event.orderId), eq(orders.status, 'pending')))
                    .returning({ id: orders.id });

                  if (updated.length === 1) {
                    await tx.insert(outbox).values({ type: 'order.paid', payload: { orderId: event.orderId } });
                  }
                  return { duplicate: false };
                });
              }
            }
        """,
        lang="typescript",
        follow=[
            ("How would you design the `Idempotency-Key` store for `POST /orders`?", "`POST /orders`-এর জন্য `Idempotency-Key` store কীভাবে design করবে?"),
            ("What if the gateway delivers a refund event before the success event?", "Gateway যদি success event-এর আগে refund event পাঠায় তাহলে কী করবে?"),
        ],
        related=["nest-027", "nest-030", "drizzle-016"],
        refs=[NEST_IDEMPOTENCY, NEST_RAW_BODY, PG_ERRCODES],
    ),
]

if __name__ == "__main__":
    save("nestjs", "b4", QUESTIONS)
