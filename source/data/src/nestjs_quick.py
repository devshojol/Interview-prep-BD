# NestJS — quick-recall questions (nest-q01 … nest-q10): short viva-style fundamentals
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NEST_VER = "NestJS 12.x"

QUESTIONS = [
    # ------------------------------------------------------------------ nest-q01
    Q(
        id="nest-q01", sub="NestJS vs Express", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["nestjs", "framework", "basics"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""What is NestJS, and why would you use it?""",
        q_bn=r"""NestJS কী, আর এটা কেন ব্যবহার করবে?""",
        a_en=r"""NestJS is a TypeScript-first framework for building server-side Node.js applications. It runs on top of an HTTP library (Express by default, or Fastify) and adds a fixed structure: modules, controllers, providers with dependency injection, and building blocks like pipes, guards and interceptors. Teams use it so large codebases stay consistent and easy to test.""",
        a_bn=r"""NestJS হলো server-side Node.js application বানানোর জন্য একটা TypeScript-first framework। এটা একটা HTTP library-র উপর চলে (default-এ Express, চাইলে Fastify) আর একটা নির্দিষ্ট structure যোগ করে: module, controller, dependency injection-সহ provider, আর pipe, guard, interceptor-এর মতো building block। বড় codebase consistent আর সহজে test করার মতো রাখতে team-গুলো এটা ব্যবহার করে।""",
        ex_en=r"""NestJS is not a replacement for Node.js or Express: Node.js is the runtime, Express or Fastify handles HTTP, and Nest organises your code on top of them.""",
        ex_bn=r"""NestJS, Node.js বা Express-এর বিকল্প নয়: Node.js হলো runtime, HTTP সামলায় Express বা Fastify, আর Nest তাদের উপরে তোমার code সাজিয়ে রাখে।""",
        tip_en=r"""Say "framework on top of Express or Fastify, with modules and DI", then name one benefit such as testability.""",
        tip_bn=r"""বলো "Express বা Fastify-এর উপর module আর DI-সহ framework", তারপর testability-র মতো একটা সুবিধা বলো।""",
        follow=[("When would plain Express be the better choice?", "কখন plain Express ভালো choice?")],
        related=["nest-011", "nest-001"],
        refs=[("NestJS docs — First steps", "https://docs.nestjs.com/first-steps")],
    ),
    # ------------------------------------------------------------------ nest-q02
    Q(
        id="nest-q02", sub="Controllers & REST APIs", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["controllers", "routing", "decorators"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""What is a controller in NestJS, and how do `@Param()`, `@Query()` and `@Body()` differ?""",
        q_bn=r"""NestJS-এ controller কী, আর `@Param()`, `@Query()` ও `@Body()`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""A controller is a class marked `@Controller('path')` whose methods handle routes declared with `@Get()`, `@Post()` and so on. `@Param()` reads route parameters (`/users/:id`), `@Query()` reads the query string (`?page=2`), and `@Body()` reads the parsed request body.""",
        a_bn=r"""Controller হলো `@Controller('path')` দেওয়া একটা class, যার method-গুলো `@Get()`, `@Post()` ইত্যাদি দিয়ে declare করা route handle করে। `@Param()` route parameter পড়ে (`/users/:id`), `@Query()` query string পড়ে (`?page=2`), আর `@Body()` parse করা request body পড়ে।""",
        code=r"""
            @Controller('users')
            export class UsersController {
              @Get(':id')   // GET /users/7?fields=name → id = 7, fields = 'name'
              findOne(@Param('id', ParseIntPipe) id: number, @Query('fields') fields?: string) {}

              @Post()       // POST /users with a JSON body → dto = parsed body
              create(@Body() dto: CreateUserDto) {}
            }
        """, lang="typescript",
        ex_en=r"""Params and query values always arrive as strings, so use a pipe like `ParseIntPipe` (or `transform: true`) when you need a number.""",
        ex_bn=r"""Param আর query value সবসময় string হয়ে আসে, তাই number লাগলে `ParseIntPipe`-এর মতো pipe (বা `transform: true`) ব্যবহার করো।""",
        tip_en=r"""Point at one URL and say which decorator reads which part of it.""",
        tip_bn=r"""একটা URL দেখিয়ে বলো কোন decorator তার কোন অংশ পড়ে।""",
        follow=[("How do you return a 204 status instead of 200?", "200-এর বদলে 204 status কীভাবে return করবে?")],
        related=["nest-002", "nest-005"],
        refs=[("NestJS docs — Controllers", "https://docs.nestjs.com/controllers")],
    ),
    # ------------------------------------------------------------------ nest-q03
    Q(
        id="nest-q03", sub="DTOs", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["dto", "validation", "class-validator"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""What is a DTO in NestJS?""",
        q_bn=r"""NestJS-এ DTO কী?""",
        a_en=r"""A DTO (Data Transfer Object) is a class that describes the shape of data coming into or going out of the API, usually the request body. With `class-validator` decorators on its fields and a global `ValidationPipe`, Nest rejects invalid input with a 400 before your handler runs.""",
        a_bn=r"""DTO (Data Transfer Object) হলো একটা class, যেটা API-তে আসা বা API থেকে যাওয়া data-র shape বর্ণনা করে, সাধারণত request body-র। এর field-এ `class-validator` decorator আর global `ValidationPipe` থাকলে handler চলার আগেই Nest ভুল input-কে 400 দিয়ে reject করে।""",
        code=r"""
            export class CreateUserDto {
              @IsEmail() email: string;
              @IsString() @Length(2, 50) name: string;
            }
            // POST /users { "email": "nope" } → 400, message includes "email must be an email"
        """, lang="typescript",
        ex_en=r"""Write DTOs as classes, not interfaces: interfaces disappear at runtime, so the pipe would have nothing to validate against.""",
        ex_bn=r"""DTO class হিসেবে লেখো, interface নয়: interface runtime-এ থাকে না, তাই pipe-এর validate করার কিছু থাকে না।""",
        tip_en=r"""Define it in one line, then mention "class, not interface" as the classic follow-up.""",
        tip_bn=r"""এক line-এ সংজ্ঞা দাও, তারপর "class, interface নয়" কথাটা বলো — এটাই সাধারণ follow-up।""",
        follow=[("What does `whitelist: true` do?", "`whitelist: true` কী করে?")],
        related=["nest-006", "nest-016"],
        refs=[("NestJS docs — Validation", "https://docs.nestjs.com/application/validation")],
    ),
    # ------------------------------------------------------------------ nest-q04
    Q(
        id="nest-q04", sub="Pipes & Validation", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["pipes", "validation", "transformation"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""What is a pipe in NestJS? Name a few built-in pipes.""",
        q_bn=r"""NestJS-এ pipe কী? কয়েকটা built-in pipe-এর নাম বলো।""",
        a_en=r"""A pipe runs just before the route handler and works on its arguments: it either transforms a value (string `"7"` → number `7`) or validates it and throws a 400 if it's wrong. Built-in examples are `ValidationPipe`, `ParseIntPipe`, `ParseUUIDPipe`, `ParseBoolPipe` and `DefaultValuePipe`.""",
        a_bn=r"""Pipe route handler-এর ঠিক আগে চলে আর তার argument নিয়ে কাজ করে: হয় value বদলায় (string `"7"` → number `7`), নয়তো validate করে আর ভুল হলে 400 throw করে। Built-in উদাহরণ: `ValidationPipe`, `ParseIntPipe`, `ParseUUIDPipe`, `ParseBoolPipe` আর `DefaultValuePipe`।""",
        code=r"""
            @Get(':id')
            findOne(@Param('id', ParseIntPipe) id: number) {
              return typeof id; // GET /users/7 → "number";  GET /users/abc → 400 Bad Request
            }
        """, lang="typescript",
        ex_en=r"""Pipes run after guards and interceptors (before part), so a request that fails auth never reaches validation.""",
        ex_bn=r"""Pipe চলে guard আর interceptor-এর (before অংশের) পরে, তাই auth-এ fail করা request validation পর্যন্ত পৌঁছায়ই না।""",
        tip_en=r"""Say "transform or validate" and give `ParseIntPipe` as the one-line example.""",
        tip_bn=r"""বলো "transform অথবা validate", আর এক line-এর উদাহরণ হিসেবে `ParseIntPipe` দেখাও।""",
        follow=[("How do you apply a pipe globally?", "Pipe global-ভাবে কীভাবে লাগাবে?")],
        related=["nest-005", "nest-016", "nest-012"],
        refs=[("NestJS docs — Pipes", "https://docs.nestjs.com/pipes")],
    ),
    # ------------------------------------------------------------------ nest-q05
    Q(
        id="nest-q05", sub="Interceptors", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["interceptors", "rxjs", "aop"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""What is an interceptor in NestJS, and what is it used for?""",
        q_bn=r"""NestJS-এ interceptor কী, আর এটা কী কাজে লাগে?""",
        a_en=r"""An interceptor wraps the route handler, so it can run code both before and after it. Through `next.handle()`, which returns an RxJS Observable, it can transform the response, measure timing, add caching, or map errors. Typical uses are logging, response envelopes and timeouts.""",
        a_bn=r"""Interceptor route handler-কে wrap করে, তাই handler-এর আগে আর পরে দুই জায়গাতেই code চালাতে পারে। `next.handle()` একটা RxJS Observable দেয়, তার মাধ্যমে response বদলানো, সময় মাপা, caching বা error map করা যায়। সাধারণ ব্যবহার: logging, response envelope আর timeout।""",
        code=r"""
            @Injectable()
            export class WrapInterceptor implements NestInterceptor {
              intercept(ctx: ExecutionContext, next: CallHandler) {
                return next.handle().pipe(map((data) => ({ data }))); // { id: 1 } → { data: { id: 1 } }
              }
            }
        """, lang="typescript",
        ex_en=r"""Interceptors run after guards, so they never see an error thrown by a guard.""",
        ex_bn=r"""Interceptor guard-এর পরে চলে, তাই guard-এর throw করা error সে কখনো দেখে না।""",
        tip_en=r"""Say "wraps the handler, before and after", then give response transformation as the example.""",
        tip_bn=r"""বলো "handler-কে আগে-পরে wrap করে", তারপর response transformation-এর উদাহরণ দাও।""",
        follow=[("How is an interceptor different from middleware?", "Interceptor আর middleware-এর পার্থক্য কী?")],
        related=["nest-013", "nest-029", "nest-021"],
        refs=[("NestJS docs — Interceptors", "https://docs.nestjs.com/interceptors")],
    ),
    # ------------------------------------------------------------------ nest-q06
    Q(
        id="nest-q06", sub="Exception Filters", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["exceptions", "filters", "http-errors"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""How do you return HTTP errors in NestJS, and what is an exception filter?""",
        q_bn=r"""NestJS-এ HTTP error কীভাবে return করো, আর exception filter কী?""",
        a_en=r"""You throw a built-in `HttpException` subclass such as `NotFoundException`, `BadRequestException` or `UnauthorizedException`, and Nest's global exception filter turns it into the right status and JSON body. An exception filter is the layer that catches thrown errors and builds the response; you write a custom one with `@Catch()` to change the error format.""",
        a_bn=r"""`NotFoundException`, `BadRequestException` বা `UnauthorizedException`-এর মতো built-in `HttpException` subclass throw করি, আর Nest-এর global exception filter সেটাকে ঠিক status আর JSON body-তে বদলে দেয়। Exception filter হলো সেই layer যেটা throw হওয়া error ধরে response বানায়; error format বদলাতে `@Catch()` দিয়ে নিজের filter লেখা যায়।""",
        code=r"""
            throw new NotFoundException('User 42 not found');
            // → 404 {"message":"User 42 not found","error":"Not Found","statusCode":404}
        """, lang="typescript",
        ex_en=r"""Any error that is not an `HttpException` becomes a generic 500 "Internal server error", so internal messages don't leak to the client.""",
        ex_bn=r"""`HttpException` নয় এমন যেকোনো error generic 500 "Internal server error" হয়ে যায়, তাই ভেতরের message client-এর কাছে leak হয় না।""",
        tip_en=r"""Show the one-line `throw` and the JSON it produces, then mention custom filters.""",
        tip_bn=r"""এক line-এর `throw` আর তার JSON দেখাও, তারপর custom filter-এর কথা বলো।""",
        follow=[("What happens if a handler throws a plain `Error`?", "Handler সাধারণ `Error` throw করলে কী হয়?")],
        related=["nest-008", "nest-025"],
        refs=[("NestJS docs — Exception filters", "https://docs.nestjs.com/exception-filters")],
    ),
    # ------------------------------------------------------------------ nest-q07
    Q(
        id="nest-q07", sub="Custom Decorators", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["decorators", "metadata", "typescript"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""What are decorators, and why does NestJS use them so much?""",
        q_bn=r"""Decorator কী, আর NestJS এত বেশি decorator কেন ব্যবহার করে?""",
        a_en=r"""A decorator is a function written as `@Name()` above a class, method, property or parameter that attaches behaviour or metadata to it. Nest reads that metadata at startup to know what is a module, controller or route, what to inject, and which pipes or guards apply, so you declare intent instead of wiring everything by hand.""",
        a_bn=r"""Decorator হলো একটা function, যেটা class, method, property বা parameter-এর উপরে `@Name()` আকারে লেখা হয় আর তাতে behaviour বা metadata যোগ করে। Startup-এর সময় Nest সেই metadata পড়ে বোঝে কোনটা module, controller বা route, কী inject করতে হবে, আর কোন pipe বা guard লাগবে — তাই সবকিছু হাতে wire না করে শুধু উদ্দেশ্যটা declare করো।""",
        ex_en=r"""You can build your own with `createParamDecorator()` (for example `@CurrentUser()`) or combine several with `applyDecorators()`.""",
        ex_bn=r"""`createParamDecorator()` দিয়ে নিজের decorator বানানো যায় (যেমন `@CurrentUser()`), আর `applyDecorators()` দিয়ে কয়েকটা একসাথে জোড়া যায়।""",
        tip_en=r"""Give the definition, then three examples from different levels: `@Module()`, `@Get()`, `@Body()`.""",
        tip_bn=r"""সংজ্ঞা দাও, তারপর আলাদা level-এর তিনটা উদাহরণ: `@Module()`, `@Get()`, `@Body()`।""",
        follow=[("How would you write a `@CurrentUser()` decorator?", "`@CurrentUser()` decorator কীভাবে লিখবে?")],
        related=["nest-014", "nest-003"],
        refs=[("NestJS docs — Custom decorators", "https://docs.nestjs.com/custom-decorators")],
    ),
    # ------------------------------------------------------------------ nest-q08
    Q(
        id="nest-q08", sub="Lifecycle Hooks", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["lifecycle-hooks", "onmoduleinit", "shutdown"],
        ver=NEST_VER, vs=False, status="stable",
        q_en=r"""What are NestJS lifecycle hooks such as `onModuleInit` and `onApplicationShutdown`?""",
        q_bn=r"""`onModuleInit` আর `onApplicationShutdown`-এর মতো NestJS lifecycle hook কী?""",
        a_en=r"""They are methods Nest calls on providers, controllers and modules at fixed moments. `onModuleInit` runs once the module's dependencies are resolved and `onApplicationBootstrap` once all modules are ready, which suits connecting or warming caches. `onModuleDestroy`, `beforeApplicationShutdown` and `onApplicationShutdown` run on shutdown to close connections, but only after you call `app.enableShutdownHooks()`.""",
        a_bn=r"""এগুলো এমন method, যেগুলো Nest নির্দিষ্ট মুহূর্তে provider, controller আর module-এ call করে। Module-এর dependency resolve হলে `onModuleInit`, আর সব module ready হলে `onApplicationBootstrap` চলে — connect করা বা cache গরম করার জন্য ভালো। Shutdown-এ connection বন্ধ করতে `onModuleDestroy`, `beforeApplicationShutdown` আর `onApplicationShutdown` চলে, তবে শুধু `app.enableShutdownHooks()` call করলে।""",
        code=r"""
            @Injectable()
            export class DbService implements OnModuleInit, OnApplicationShutdown {
              async onModuleInit() { await this.pool.query('select 1'); } // fail fast at startup
              async onApplicationShutdown(signal?: string) { await this.pool.end(); } // e.g. 'SIGTERM'
            }
        """, lang="typescript",
        ex_en=r"""Forgetting `enableShutdownHooks()` is the usual bug: on SIGTERM from Docker or Kubernetes the shutdown hooks never run and connections are cut instead of closed.""",
        ex_bn=r"""সাধারণ bug হলো `enableShutdownHooks()` ভুলে যাওয়া: Docker বা Kubernetes-এর SIGTERM-এ shutdown hook চলে না, connection ঠিকভাবে বন্ধ না হয়ে কেটে যায়।""",
        tip_en=r"""Name one startup hook and one shutdown hook, then mention `enableShutdownHooks()`.""",
        tip_bn=r"""একটা startup hook আর একটা shutdown hook-এর নাম বলো, তারপর `enableShutdownHooks()`-এর কথা বলো।""",
        follow=[("Why not do async setup in the constructor?", "Constructor-এ async setup কেন করবে না?")],
        related=["nest-022", "nest-023"],
        refs=[("NestJS docs — Lifecycle events", "https://docs.nestjs.com/fundamentals/lifecycle-events")],
    ),
    # ------------------------------------------------------------------ nest-q09
    Q(
        id="nest-q09", sub="Database Integration", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["typeorm", "prisma", "mongoose", "orm"],
        ver=NEST_VER + " (@nestjs/typeorm, @nestjs/mongoose, Prisma ORM 7)", vs=True, status="stable",
        q_en=r"""How do you connect an ORM such as TypeORM, Prisma or Mongoose to a NestJS app?""",
        q_bn=r"""TypeORM, Prisma বা Mongoose-এর মতো ORM NestJS app-এ কীভাবে যুক্ত করো?""",
        a_en=r"""TypeORM and Mongoose have official modules: configure the connection once with `TypeOrmModule.forRootAsync()` or `MongooseModule.forRoot()`, register entities or schemas per feature with `forFeature()`, and inject them with `@InjectRepository(User)` or `@InjectModel(Cat.name)`. Prisma has no Nest package, so you wrap the generated client in a `PrismaService` provider and inject that.""",
        a_bn=r"""TypeORM আর Mongoose-এর official module আছে: `TypeOrmModule.forRootAsync()` বা `MongooseModule.forRoot()` দিয়ে connection একবার configure করো, প্রতিটা feature-এ `forFeature()` দিয়ে entity বা schema register করো, তারপর `@InjectRepository(User)` বা `@InjectModel(Cat.name)` দিয়ে inject করো। Prisma-র কোনো Nest package নেই, তাই generate করা client-কে একটা `PrismaService` provider-এ wrap করে সেটাই inject করো।""",
        code=r"""
            // users.module.ts
            @Module({ imports: [TypeOrmModule.forFeature([User])], providers: [UsersService] })
            export class UsersModule {}

            // users.service.ts
            constructor(@InjectRepository(User) private readonly users: Repository<User>) {}
            // this.users.findOneBy({ id: 1 }) → User | null
        """, lang="typescript",
        ex_en=r"""Read the connection settings from `ConfigService` in `forRootAsync()`, and never use TypeORM's `synchronize: true` in production: it can drop data; use migrations instead.""",
        ex_bn=r"""`forRootAsync()`-এ connection setting `ConfigService` থেকে পড়ো, আর production-এ TypeORM-এর `synchronize: true` কখনো ব্যবহার করো না: এতে data হারাতে পারে; তার বদলে migration ব্যবহার করো।""",
        tip_en=r"""Describe the pattern "root connection, per-feature registration, injection", then say how Prisma differs.""",
        tip_bn=r"""এই pattern বলো: "root connection, feature-ভিত্তিক registration, injection", তারপর Prisma কোথায় আলাদা সেটা বলো।""",
        follow=[("How would you integrate Drizzle instead?", "এর বদলে Drizzle কীভাবে integrate করবে?"),
                ("Why use `forRootAsync()` instead of `forRoot()`?", "`forRoot()`-এর বদলে `forRootAsync()` কেন?")],
        related=["nest-022", "nest-019"],
        refs=[("NestJS docs — TypeORM", "https://docs.nestjs.com/data/typeorm"),
              ("NestJS docs — Prisma", "https://docs.nestjs.com/data/prisma"),
              ("NestJS docs — MongoDB", "https://docs.nestjs.com/data/mongodb")],
    ),
    # ------------------------------------------------------------------ nest-q10
    Q(
        id="nest-q10", sub="Configuration", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["config", "env", "configservice"],
        ver=NEST_VER + " (@nestjs/config)", vs=False, status="stable",
        q_en=r"""How do you read environment variables in NestJS?""",
        q_bn=r"""NestJS-এ environment variable কীভাবে পড়ো?""",
        a_en=r"""Import `ConfigModule.forRoot()` from `@nestjs/config`, which loads `.env` into the environment, and inject `ConfigService` wherever you need a value: `config.get('PORT')`, or `config.getOrThrow('DATABASE_URL')` for required ones. Add a validation schema so the app refuses to start when a required variable is missing.""",
        a_bn=r"""`@nestjs/config` থেকে `ConfigModule.forRoot()` import করো, যেটা `.env` load করে, তারপর যেখানে value লাগে সেখানে `ConfigService` inject করো: `config.get('PORT')`, আর required হলে `config.getOrThrow('DATABASE_URL')`। একটা validation schema দাও, যাতে required variable না থাকলে app start-ই না হয়।""",
        code=r"""
            @Module({ imports: [ConfigModule.forRoot({ isGlobal: true })] })
            export class AppModule {}

            constructor(private readonly config: ConfigService) {}
            // this.config.get<number>('PORT', 3000) → 3000 when PORT is not set
        """, lang="typescript",
        ex_en=r"""Use `ConfigService` instead of reading `process.env` everywhere: it is injectable, so tests can replace it, and `isGlobal: true` saves importing the module in every feature.""",
        ex_bn=r"""সব জায়গায় `process.env` না পড়ে `ConfigService` ব্যবহার করো: এটা injectable, তাই test-এ বদলানো যায়, আর `isGlobal: true` দিলে প্রতিটা feature-এ module import করতে হয় না।""",
        tip_en=r"""Mention fail-fast validation at startup; it shows production thinking.""",
        tip_bn=r"""Startup-এ fail-fast validation-এর কথা বলো; এতে production-এর চিন্তা বোঝা যায়।""",
        follow=[("How do you pass config into `JwtModule` or a database module?", "`JwtModule` বা database module-এ config কীভাবে দেবে?")],
        related=["nest-010", "nest-019"],
        refs=[("NestJS docs — Configuration", "https://docs.nestjs.com/application/configuration")],
    ),
]

if __name__ == "__main__":
    save("nestjs", "quick", QUESTIONS)
