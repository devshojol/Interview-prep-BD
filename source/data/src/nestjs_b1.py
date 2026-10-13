# NestJS — batch 1 (nest-001 … nest-008): modules, controllers, providers/DI, scopes, pipes, DTOs, guards, exceptions
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

NEST_MODULES = ("NestJS docs — Modules", "https://docs.nestjs.com/modules")
NEST_CONTROLLERS = ("NestJS docs — Controllers", "https://docs.nestjs.com/controllers")
NEST_PROVIDERS = ("NestJS docs — Providers", "https://docs.nestjs.com/providers")
NEST_SCOPES = ("NestJS docs — Injection scopes", "https://docs.nestjs.com/fundamentals/injection-scopes")
NEST_PIPES = ("NestJS docs — Pipes", "https://docs.nestjs.com/pipes")
NEST_VALIDATION = ("NestJS docs — Validation", "https://docs.nestjs.com/application/validation")
NEST_GUARDS = ("NestJS docs — Guards", "https://docs.nestjs.com/guards")
NEST_FILTERS = ("NestJS docs — Exception filters", "https://docs.nestjs.com/exception-filters")
NEST_COMMON_ERRORS = ("NestJS docs — Common errors", "https://docs.nestjs.com/faq/common-errors")

QUESTIONS = [
    # ------------------------------------------------------------------ nest-001
    Q(
        id="nest-001", sub="Modules", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["modules", "imports", "exports", "encapsulation"],
        ver="NestJS 12.1 (concept unchanged since early versions)", vs=False, status="stable",
        q_en=r"""What is a module in NestJS, and what do the `imports`, `controllers`, `providers` and `exports` arrays in `@Module()` do?""",
        q_bn=r"""NestJS-এ module কী? `@Module()`-এর `imports`, `controllers`, `providers` আর `exports` array গুলো কী কাজ করে?""",
        a_en=r"""
            A module is a class decorated with `@Module()` that groups the controllers and providers of one feature — `UsersModule`, `OrdersModule` and so on. Every app has a root `AppModule`, and Nest builds its dependency graph starting from there.

            - `controllers` — the classes that handle incoming requests for this feature.
            - `providers` — services, repositories and factories that Nest creates and can inject **inside** this module.
            - `exports` — the providers other modules are allowed to use. Providers are private by default, which gives you encapsulation.
            - `imports` — other modules whose exported providers this module needs.

            So if `OrdersService` needs `UsersService`, `UsersModule` exports it and `OrdersModule` imports `UsersModule`.
        """,
        a_bn=r"""
            Module হলো `@Module()` decorator দেওয়া একটা class, যেটা একটা feature-এর controller আর provider গুলোকে একসাথে রাখে — যেমন `UsersModule`, `OrdersModule`। প্রতিটা app-এ একটা root `AppModule` থাকে, আর Nest সেখান থেকে শুরু করে পুরো dependency graph তৈরি করে।

            - `controllers` — এই feature-এর incoming request handle করে যে class গুলো।
            - `providers` — service, repository, factory ইত্যাদি, যেগুলো Nest তৈরি করে এবং এই module-এর **ভেতরে** inject করতে পারে।
            - `exports` — কোন provider গুলো অন্য module ব্যবহার করতে পারবে। Default-এ provider private থাকে, এটাই encapsulation।
            - `imports` — অন্য যেসব module-এর exported provider এই module-এর দরকার।

            তাই `OrdersService`-এর যদি `UsersService` লাগে, তাহলে `UsersModule` সেটা export করবে আর `OrdersModule`, `UsersModule`-কে import করবে।
        """,
        ex_en=r"""
            - **Encapsulation is enforced.** If `UsersModule` forgets `exports: [UsersService]`, injecting it in `OrdersService` fails at startup with "Nest can't resolve dependencies of the OrdersService (?)".
            - **Modules are singletons.** Importing `UsersModule` in five modules still gives one shared `UsersService` instance. But if you also list `UsersService` directly in `OrdersModule.providers`, you get a *second* instance — a common source of "my cache/state is not shared" bugs.
            - **Re-exporting:** a module can export a module it imports (`exports: [UsersModule]`) to build a shared "core" module.
            - **Global modules:** `@Global()` (or `isGlobal: true` on modules like `ConfigModule`) removes the need to import everywhere. Use it sparingly — config, database, logger — otherwise dependencies become invisible.
            - In NestJS 12, new projects are generated as ES modules, which is why relative imports in the example end with `.js`.
        """,
        ex_bn=r"""
            - **Encapsulation সত্যিই enforce হয়।** `UsersModule` যদি `exports: [UsersService]` দিতে ভুলে যায়, তাহলে `OrdersService`-এ inject করতে গেলে startup-এই "Nest can't resolve dependencies of the OrdersService (?)" error আসবে।
            - **Module singleton।** পাঁচটা module-এ `UsersModule` import করলেও একটাই shared `UsersService` instance থাকে। কিন্তু যদি `OrdersModule.providers`-এ সরাসরি `UsersService` আবার লিখে দাও, তাহলে *দ্বিতীয়* একটা instance তৈরি হয় — "আমার cache/state share হচ্ছে না" ধরনের bug-এর common কারণ এটা।
            - **Re-export:** একটা module তার import করা module-কে export করতে পারে (`exports: [UsersModule]`), এভাবে shared "core" module বানানো যায়।
            - **Global module:** `@Global()` (বা `ConfigModule`-এর মতো module-এ `isGlobal: true`) দিলে সব জায়গায় import করতে হয় না। তবে কম ব্যবহার করা উচিত — config, database, logger-এর মতো জিনিসে — নাহলে dependency গুলো চোখের আড়ালে চলে যায়।
            - NestJS 12-এ নতুন project ES module হিসেবে generate হয়, তাই example-এর relative import-এ `.js` extension আছে।
        """,
        tip_en=r"""Explain modules as "feature boundaries with a public API (exports)". Then give the Users/Orders example — interviewers like hearing the word encapsulation and the "can't resolve dependencies" error.""",
        tip_bn=r"""Module-কে "public API (exports) সহ একটা feature boundary" হিসেবে ব্যাখ্যা করো। তারপর Users/Orders example দাও — interviewer encapsulation শব্দটা আর "can't resolve dependencies" error-এর কথা শুনতে পছন্দ করে।""",
        mist_en=r"""Re-declaring another module's service in your own `providers` instead of importing the module; marking every module `@Global()`; thinking `imports` takes classes like services.""",
        mist_bn=r"""Module import না করে অন্য module-এর service নিজের `providers`-এ আবার declare করা; সব module-কে `@Global()` করে ফেলা; ভাবা যে `imports`-এ service-এর মতো class দেওয়া যায়।""",
        code=r"""
            // users/users.module.ts
            import { Module } from '@nestjs/common';
            import { UsersController } from './users.controller.js';
            import { UsersService } from './users.service.js';

            @Module({
              controllers: [UsersController],
              providers: [UsersService],
              exports: [UsersService], // the module's public API
            })
            export class UsersModule {}

            // orders/orders.module.ts
            import { Module } from '@nestjs/common';
            import { UsersModule } from '../users/users.module.js';
            import { OrdersController } from './orders.controller.js';
            import { OrdersService } from './orders.service.js';

            @Module({
              imports: [UsersModule], // OrdersService can now inject UsersService
              controllers: [OrdersController],
              providers: [OrdersService],
            })
            export class OrdersModule {}
        """,
        lang="typescript",
        follow=[
            ("When would you use `@Global()`, and what is the downside?", "কখন `@Global()` ব্যবহার করবে, আর এর অসুবিধা কী?"),
            ("What is a dynamic module (e.g. `forRoot()`)?", "Dynamic module (যেমন `forRoot()`) কী?"),
        ],
        related=["nest-003", "nest-019"],
        refs=[NEST_MODULES],
    ),
    # ------------------------------------------------------------------ nest-002
    Q(
        id="nest-002", sub="Controllers & REST APIs", diff="easy", type="coding",
        prio="high", market="both", mins=8,
        tags=["controllers", "rest", "parseintpipe", "httpcode", "crud"],
        ver="NestJS 12.1 (Express 5 adapter)", vs=False, status="stable",
        q_en=r"""
            Write a `UsersController` for a REST resource at `/users`:

            - `GET /users` — list users, with an optional `?role=` filter
            - `GET /users/:id` — the id must be numeric (`/users/abc` → 400); unknown id → 404
            - `POST /users` — create a user from a validated body, respond with 201
            - `PATCH /users/:id` — partial update
            - `DELETE /users/:id` — respond with 204 and no body

            Keep the business logic in a `UsersService` (an in-memory store is fine).
        """,
        q_bn=r"""
            `/users` resource-এর জন্য একটা REST `UsersController` লেখো:

            - `GET /users` — user list, optional `?role=` filter সহ
            - `GET /users/:id` — id অবশ্যই numeric হবে (`/users/abc` → 400); না পাওয়া গেলে → 404
            - `POST /users` — validated body থেকে user তৈরি করবে, response 201
            - `PATCH /users/:id` — partial update
            - `DELETE /users/:id` — 204, কোনো body ছাড়া

            Business logic `UsersService`-এ রাখো (in-memory store হলেই চলবে)।
        """,
        a_en=r"""
            The controller only maps HTTP to service calls; the service owns the data and throws HTTP exceptions.

            - `@Controller('users')` sets the route prefix; `@Get()`, `@Post()`, `@Patch(':id')`, `@Delete(':id')` define the routes.
            - `@Param('id', ParseIntPipe)` converts the id to a number and returns 400 for non-numeric input before my code runs.
            - `@Query('role')` reads the optional filter; `@Body()` gets the DTO, which a global `ValidationPipe` validates.
            - `POST` returns 201 by default; for `DELETE` I add `@HttpCode(HttpStatus.NO_CONTENT)` and return nothing.
            - The service throws `NotFoundException`, which Nest turns into a 404 JSON response.
            - `UpdateUserDto extends PartialType(CreateUserDto)` reuses the same validation rules with every field optional.
        """,
        a_bn=r"""
            Controller শুধু HTTP-কে service call-এ map করে; data-র দায়িত্ব service-এর, আর HTTP exception-ও service throw করে।

            - `@Controller('users')` route prefix ঠিক করে; `@Get()`, `@Post()`, `@Patch(':id')`, `@Delete(':id')` দিয়ে route define হয়।
            - `@Param('id', ParseIntPipe)` id-কে number-এ convert করে, আর non-numeric হলে আমার code চলার আগেই 400 দেয়।
            - `@Query('role')` optional filter পড়ে; `@Body()` DTO নেয়, যেটা global `ValidationPipe` validate করে।
            - `POST` default-এ 201 দেয়; `DELETE`-এর জন্য `@HttpCode(HttpStatus.NO_CONTENT)` দিই আর কিছু return করি না।
            - Service `NotFoundException` throw করে, Nest সেটাকে 404 JSON response বানায়।
            - `UpdateUserDto extends PartialType(CreateUserDto)` একই validation rule reuse করে, শুধু সব field optional হয়ে যায়।
        """,
        ex_en=r"""
            - **Thin controllers:** keeping logic in the service makes it reusable (from a queue consumer or CLI) and easy to unit-test without HTTP.
            - **Status codes:** Nest defaults to 200 for everything except `POST` (201). Use `@HttpCode()` for 204/202. Avoid injecting `@Res()` just to set a status — it switches the route to manual response mode and you lose interceptors' response mapping unless you pass `{ passthrough: true }`.
            - **Validation:** the DTO classes use `class-validator`; the example assumes `app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }))` in `main.ts`.
            - **Edge cases:** `PATCH` merges only provided fields; `DELETE` of an already-deleted id returns 404 (a valid design; some teams prefer idempotent 204).
            - `PartialType` comes from `@nestjs/mapped-types` (or `@nestjs/swagger` if you use OpenAPI, so the docs stay in sync).
        """,
        ex_bn=r"""
            - **Thin controller:** logic service-এ রাখলে সেটা reuse করা যায় (queue consumer বা CLI থেকেও), আর HTTP ছাড়াই unit test করা সহজ হয়।
            - **Status code:** `POST` (201) ছাড়া বাকি সব কিছুর default 200। 204/202-এর জন্য `@HttpCode()` ব্যবহার করো। শুধু status set করতে `@Res()` inject করো না — এতে route manual response mode-এ চলে যায়, `{ passthrough: true }` না দিলে interceptor-এর response mapping আর কাজ করে না।
            - **Validation:** DTO class গুলো `class-validator` ব্যবহার করে; example ধরে নিচ্ছে `main.ts`-এ `app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }))` আছে।
            - **Edge case:** `PATCH` শুধু দেওয়া field গুলো merge করে; already-deleted id `DELETE` করলে 404 আসে (এটা valid design; কিছু team idempotent 204 পছন্দ করে)।
            - `PartialType` আসে `@nestjs/mapped-types` থেকে (OpenAPI ব্যবহার করলে `@nestjs/swagger` থেকে, যাতে docs sync থাকে)।
        """,
        tip_en=r"""Talk through the route table first (method, path, status code), then write code. Mentioning `ParseIntPipe`, `@HttpCode(204)` and "thin controller, fat service" signals real project experience.""",
        tip_bn=r"""আগে route table মুখে বলো (method, path, status code), তারপর code লেখো। `ParseIntPipe`, `@HttpCode(204)` আর "thin controller, fat service"-এর কথা বললে বোঝা যায় তোমার real project অভিজ্ঞতা আছে।""",
        mist_en=r"""Using `@Param('id') id: number` and assuming it's a number (it's a string); putting database logic in the controller; using `@Res()` and forgetting to send a response, which hangs the request.""",
        mist_bn=r"""`@Param('id') id: number` লিখে ধরে নেওয়া যে এটা number (আসলে string); controller-এ database logic রাখা; `@Res()` ব্যবহার করে response পাঠাতে ভুলে যাওয়া, ফলে request hang হয়ে থাকে।""",
        code=r"""
            // users/dto/create-user.dto.ts
            import { IsEmail, IsIn, IsString, Length } from 'class-validator';
            import { PartialType } from '@nestjs/mapped-types';

            export class CreateUserDto {
              @IsEmail() email: string;
              @IsString() @Length(2, 50) name: string;
              @IsIn(['user', 'admin']) role: 'user' | 'admin';
            }
            export class UpdateUserDto extends PartialType(CreateUserDto) {}

            // users/users.service.ts
            import { Injectable, NotFoundException } from '@nestjs/common';

            export interface User extends CreateUserDto { id: number }

            @Injectable()
            export class UsersService {
              private readonly users = new Map<number, User>();
              private nextId = 1;

              findAll(role?: string): User[] {
                const all = [...this.users.values()];
                return role ? all.filter((u) => u.role === role) : all;
              }

              findOne(id: number): User {
                const user = this.users.get(id);
                if (!user) throw new NotFoundException(`User ${id} not found`);
                return user;
              }

              create(dto: CreateUserDto): User {
                const user: User = { id: this.nextId++, ...dto };
                this.users.set(user.id, user);
                return user;
              }

              update(id: number, dto: UpdateUserDto): User {
                const user: User = { ...this.findOne(id), ...dto };
                this.users.set(id, user);
                return user;
              }

              remove(id: number): void {
                this.findOne(id); // throws 404 if missing
                this.users.delete(id);
              }
            }

            // users/users.controller.ts
            import {
              Body, Controller, Delete, Get, HttpCode, HttpStatus,
              Param, ParseIntPipe, Patch, Post, Query,
            } from '@nestjs/common';

            @Controller('users')
            export class UsersController {
              constructor(private readonly usersService: UsersService) {}

              @Get()
              findAll(@Query('role') role?: string) {
                return this.usersService.findAll(role);
              }

              @Get(':id')
              findOne(@Param('id', ParseIntPipe) id: number) {
                return this.usersService.findOne(id);
              }

              @Post()
              create(@Body() dto: CreateUserDto) {
                return this.usersService.create(dto); // 201 by default
              }

              @Patch(':id')
              update(@Param('id', ParseIntPipe) id: number, @Body() dto: UpdateUserDto) {
                return this.usersService.update(id, dto);
              }

              @Delete(':id')
              @HttpCode(HttpStatus.NO_CONTENT)
              remove(@Param('id', ParseIntPipe) id: number): void {
                this.usersService.remove(id);
              }
            }
        """,
        lang="typescript",
        time="O(1) per lookup/insert/delete (Map); O(n) for the filtered list",
        space="O(n) for n stored users",
        follow=[
            ("How would you add pagination and sorting to `GET /users`?", "`GET /users`-এ pagination আর sorting কীভাবে যোগ করবে?"),
            ("When would you use `@Res({ passthrough: true })`?", "কখন `@Res({ passthrough: true })` ব্যবহার করবে?"),
        ],
        related=["nest-003", "nest-006", "nest-008"],
        refs=[NEST_CONTROLLERS, NEST_PIPES],
    ),
    # ------------------------------------------------------------------ nest-003
    Q(
        id="nest-003", sub="Providers & Dependency Injection", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["providers", "dependency-injection", "services", "ioc"],
        ver="NestJS 12.1 (concept unchanged since early versions)", vs=False, status="stable",
        q_en=r"""What is a provider in NestJS, and how does dependency injection work when a controller needs a service?""",
        q_bn=r"""NestJS-এ provider কী? একটা controller-এর যখন একটা service দরকার হয়, তখন dependency injection কীভাবে কাজ করে?""",
        a_en=r"""
            A provider is anything Nest's IoC container can create and inject. Most often it's a class marked `@Injectable()` — a service, repository or helper — but it can also be a plain value or a factory.

            When I list `UsersService` in a module's `providers`, Nest registers it under a token (the class itself). When Nest creates `UsersController`, it reads the constructor parameter types from TypeScript's decorator metadata, finds the matching providers, creates them (once, by default) and passes them in. So I just write `constructor(private readonly usersService: UsersService) {}` and never call `new` myself.

            Services are simply providers that hold business logic, so controllers stay thin.
        """,
        a_bn=r"""
            Provider হলো এমন যেকোনো কিছু যেটা Nest-এর IoC container তৈরি করে inject করতে পারে। সাধারণত এটা `@Injectable()` দেওয়া একটা class — service, repository বা helper — তবে plain value বা factory-ও হতে পারে।

            Module-এর `providers`-এ `UsersService` লিখলে Nest সেটাকে একটা token (class-টাই token) দিয়ে register করে। `UsersController` তৈরির সময় Nest TypeScript-এর decorator metadata থেকে constructor parameter-এর type পড়ে, matching provider খুঁজে বের করে, সেগুলো তৈরি করে (default-এ একবারই) এবং pass করে দেয়। তাই আমি শুধু `constructor(private readonly usersService: UsersService) {}` লিখি, নিজে কখনো `new` call করি না।

            Service আসলে business logic রাখার provider, যাতে controller হালকা থাকে।
        """,
        ex_en=r"""
            - **Why it matters:** loose coupling (the controller depends on an injected instance, not a concrete construction), lifecycle management by the framework, and easy testing — you swap a provider for a mock in `Test.createTestingModule()`.
            - **How Nest knows the types:** `emitDecoratorMetadata` stores `design:paramtypes`. That's why `import type { UsersService }` breaks injection — the type is erased and Nest sees `undefined`. The NestJS 12 error message even suggests checking for `import type`.
            - **Interfaces can't be tokens** because they don't exist at runtime. For "inject an implementation of an interface", use a custom token (string/symbol) with `@Inject(TOKEN)`.
            - `@Injectable()` is what makes Nest emit metadata for a class's own dependencies; add it to every provider class.
        """,
        ex_bn=r"""
            - **কেন গুরুত্বপূর্ণ:** loose coupling (controller একটা inject করা instance-এর উপর নির্ভর করে, নিজে বানায় না), lifecycle framework manage করে, আর test সহজ — `Test.createTestingModule()`-এ provider-কে mock দিয়ে বদলে দেওয়া যায়।
            - **Nest type কীভাবে জানে:** `emitDecoratorMetadata`, `design:paramtypes` save করে রাখে। এজন্যই `import type { UsersService }` লিখলে injection ভেঙে যায় — type erase হয়ে যায়, Nest পায় `undefined`। NestJS 12-এর error message-ও `import type` check করতে বলে।
            - **Interface token হতে পারে না**, কারণ runtime-এ interface থাকে না। "Interface-এর একটা implementation inject করতে" custom token (string/symbol) আর `@Inject(TOKEN)` ব্যবহার করো।
            - `@Injectable()` দিলেই Nest ওই class-এর নিজের dependency-র metadata emit করে; তাই প্রতিটা provider class-এ এটা দাও।
        """,
        tip_en=r"""Use the phrase "inversion of control": the framework creates and wires objects; my classes just declare what they need. Then mention testing with mocks as the practical benefit.""",
        tip_bn=r""""Inversion of control" কথাটা ব্যবহার করো: framework object তৈরি করে জোড়া লাগায়, আমার class শুধু বলে তার কী লাগবে। তারপর practical সুবিধা হিসেবে mock দিয়ে testing-এর কথা বলো।""",
        mist_en=r"""Creating services manually with `new`; using `import type` for injected classes; trying to inject a TypeScript interface without a token.""",
        mist_bn=r"""`new` দিয়ে নিজে service তৈরি করা; inject করা class-এর জন্য `import type` ব্যবহার করা; token ছাড়া TypeScript interface inject করার চেষ্টা করা।""",
        code=r"""
            import { Controller, Get, Injectable, Module } from '@nestjs/common';

            @Injectable()
            export class GreetingService {
              greet(name: string) {
                return `Hello, ${name}`;
              }
            }

            @Controller('greet')
            export class GreetingController {
              // Nest resolves GreetingService from the module's providers
              constructor(private readonly greeting: GreetingService) {}

              @Get()
              hello() {
                return this.greeting.greet('Dhaka');
              }
            }

            @Module({
              controllers: [GreetingController],
              providers: [GreetingService],
            })
            export class GreetingModule {}
        """,
        lang="typescript",
        follow=[
            ("How do you inject something that isn't a class, like a config object?", "Class নয় এমন কিছু (যেমন config object) কীভাবে inject করবে?"),
            ("What are provider scopes?", "Provider scope কী?"),
        ],
        related=["nest-001", "nest-004", "nest-018"],
        refs=[NEST_PROVIDERS, NEST_COMMON_ERRORS],
    ),
    # ------------------------------------------------------------------ nest-004
    Q(
        id="nest-004", sub="Dependency Injection Scopes", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=1,
        tags=["scopes", "singleton", "providers"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""A class is decorated with plain `@Injectable()` and listed in one module's `providers`. What is its lifetime by default?""",
        q_bn=r"""একটা class-এ শুধু `@Injectable()` দেওয়া আছে আর একটা module-এর `providers`-এ রাখা আছে। Default-এ এর lifetime কী?""",
        options=[
            ("A new instance is created for every incoming request (`Scope.REQUEST`)", "প্রতিটা incoming request-এর জন্য নতুন instance তৈরি হয় (`Scope.REQUEST`)"),
            ("Every class that injects it receives its own private instance (`Scope.TRANSIENT`)", "যে class-ই inject করুক, প্রত্যেকে নিজের আলাদা instance পায় (`Scope.TRANSIENT`)"),
            ("One shared instance for the whole application, created at bootstrap (`Scope.DEFAULT`, singleton)", "পুরো application-এ একটাই shared instance, bootstrap-এর সময় তৈরি হয় (`Scope.DEFAULT`, singleton)"),
            ("One instance per module that imports the provider's module", "Provider-এর module যতগুলো module import করে, প্রত্যেকটার জন্য একটা করে instance"),
        ],
        correct=2,
        a_en=r"""Singleton (`Scope.DEFAULT`): Nest creates one instance when the app bootstraps and shares it with every consumer, across all modules that import the provider's module.""",
        a_bn=r"""Singleton (`Scope.DEFAULT`): app bootstrap-এর সময় Nest একটা instance তৈরি করে এবং provider-এর module যারা import করে, সব module-এর সব consumer-এর সাথে সেটাই share করে।""",
        ex_en=r"""
            Singleton is the default because it's the cheapest: no per-request allocation, and Node's single-threaded model makes sharing safe as long as you don't store request-specific data in fields.

            The tempting wrong answer is the last one. Importing a module many times does **not** duplicate its providers — modules are singletons too. You only get a second instance if the same class is declared in the `providers` array of **another** module as well.

            `REQUEST` and `TRANSIENT` must be opted into with `@Injectable({ scope: Scope.REQUEST })` / `Scope.TRANSIENT`, and request scope has a performance cost because it "bubbles up" to every consumer.
        """,
        ex_bn=r"""
            Singleton default কারণ এটাই সবচেয়ে সস্তা: per-request allocation নেই, আর Node-এর single-threaded model-এ share করা নিরাপদ — যতক্ষণ না field-এ request-specific data রাখছ।

            লোভনীয় ভুল উত্তর হলো শেষেরটা। একটা module অনেকবার import করলে তার provider duplicate **হয় না** — module-ও singleton। দ্বিতীয় instance তখনই হয় যখন একই class **অন্য** module-এর `providers` array-তেও declare করা হয়।

            `REQUEST` আর `TRANSIENT` আলাদা করে `@Injectable({ scope: Scope.REQUEST })` / `Scope.TRANSIENT` দিয়ে চালু করতে হয়, আর request scope-এর performance cost আছে কারণ এটা সব consumer পর্যন্ত "bubble up" করে।
        """,
        tip_en=r"""After answering "singleton", add one sentence on why you must not keep per-request state (like the current user) in a singleton's fields. That shows you understand the consequence, not just the default.""",
        tip_bn=r""""Singleton" বলার পর এক লাইনে যোগ করো কেন singleton-এর field-এ per-request state (যেমন current user) রাখা যাবে না। এতে বোঝা যায় তুমি শুধু default না, তার ফলাফলও বোঝো।""",
        related=["nest-003", "nest-023"],
        refs=[NEST_SCOPES, NEST_PROVIDERS],
    ),
    # ------------------------------------------------------------------ nest-005
    Q(
        id="nest-005", sub="Pipes & Validation", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["validationpipe", "transform", "query-params", "pipes"],
        ver="NestJS 12.1 (class-validator ValidationPipe)", vs=False, status="stable",
        q_en=r"""`main.ts` registers `app.useGlobalPipes(new ValidationPipe())` with default options. What does `GET /products?page=2` return for the handler shown?""",
        q_bn=r"""`main.ts`-এ default option সহ `app.useGlobalPipes(new ValidationPipe())` register করা আছে। দেখানো handler-এ `GET /products?page=2` call করলে কী return করবে?""",
        code=r"""
            @Controller('products')
            export class ProductsController {
              @Get()
              list(@Query('page') page: number) {
                return { type: typeof page, next: page + 1 };
              }
            }
        """,
        lang="typescript",
        options=[
            ("`{\"type\":\"number\",\"next\":3}`", "`{\"type\":\"number\",\"next\":3}`"),
            ("`{\"type\":\"string\",\"next\":\"21\"}`", "`{\"type\":\"string\",\"next\":\"21\"}`"),
            ("`400 Bad Request`, because `page` is not a number", "`400 Bad Request`, কারণ `page` number নয়"),
            ("`{\"type\":\"number\",\"next\":null}`", "`{\"type\":\"number\",\"next\":null}`"),
        ],
        correct=1,
        a_en=r"""`{"type":"string","next":"21"}`. Query values always arrive as strings, the `: number` annotation is compile-time only, and `ValidationPipe` without `transform: true` returns the original value — so `"2" + 1` is string concatenation.""",
        a_bn=r"""`{"type":"string","next":"21"}`। Query value সবসময় string হিসেবে আসে, `: number` annotation শুধু compile-time-এর জিনিস, আর `transform: true` ছাড়া `ValidationPipe` original value-ই ফেরত দেয় — তাই `"2" + 1` string concatenation হয়ে যায়।""",
        ex_en=r"""
            The tempting answer is the first one, because TypeScript "says" `page` is a number. But types are erased; at runtime Nest only has the metadata type `Number`. `ValidationPipe` validates **class** metatypes (DTOs) and skips primitives, so nothing is checked or converted.

            Fixes:
            - `new ValidationPipe({ transform: true })` → primitives are converted using the metadata, so `page` becomes `2` and the response is `{"type":"number","next":3}`. Careful: `?page=abc` then becomes `NaN` (serialised as `null`) **without** an error.
            - `@Query('page', ParseIntPipe) page: number` → converts and returns 400 for `abc`. Use `new DefaultValuePipe(1)` before it for an optional param.
            - For query DTOs: `@Type(() => Number) @IsInt() @Min(1) page: number` plus `transform: true`.
        """,
        ex_bn=r"""
            লোভনীয় উত্তর হলো প্রথমটা, কারণ TypeScript "বলছে" `page` একটা number। কিন্তু type erase হয়ে যায়; runtime-এ Nest-এর কাছে শুধু metadata type `Number` থাকে। `ValidationPipe` শুধু **class** metatype (DTO) validate করে, primitive skip করে — তাই কিছুই check বা convert হয় না।

            সমাধান:
            - `new ValidationPipe({ transform: true })` → metadata দেখে primitive convert হয়, `page` হয়ে যায় `2`, response `{"type":"number","next":3}`। সাবধান: তখন `?page=abc` কোনো error **ছাড়াই** `NaN` হয়ে যায় (JSON-এ `null`)।
            - `@Query('page', ParseIntPipe) page: number` → convert করে, আর `abc` হলে 400 দেয়। Optional param হলে আগে `new DefaultValuePipe(1)` দাও।
            - Query DTO-র জন্য: `@Type(() => Number) @IsInt() @Min(1) page: number` আর সাথে `transform: true`।
        """,
        tip_en=r"""Say the key sentence: "TypeScript types don't exist at runtime; HTTP gives strings." Then mention `ParseIntPipe` as the strict option — that's what interviewers want to hear.""",
        tip_bn=r"""মূল কথাটা বলো: "TypeScript type runtime-এ থাকে না; HTTP সবসময় string দেয়।" তারপর strict option হিসেবে `ParseIntPipe`-এর কথা বলো — interviewer এটাই শুনতে চায়।""",
        related=["nest-002", "nest-016"],
        refs=[NEST_VALIDATION, NEST_PIPES],
    ),
    # ------------------------------------------------------------------ nest-006
    Q(
        id="nest-006", sub="DTOs", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=1,
        tags=["dto", "class-validator", "metadata", "typescript"],
        ver="NestJS 12.1 (class-validator ValidationPipe)", vs=False, status="stable",
        q_en=r"""Why do NestJS developers usually write DTOs as **classes** rather than TypeScript interfaces when using `ValidationPipe`?""",
        q_bn=r"""`ValidationPipe` ব্যবহার করার সময় NestJS developer-রা সাধারণত DTO কেন TypeScript interface না লিখে **class** হিসেবে লেখে?""",
        options=[
            ("Classes are serialised to JSON faster than interfaces", "Interface-এর চেয়ে class দ্রুত JSON-এ serialise হয়"),
            ("NestJS refuses to compile a handler whose parameter is typed with an interface", "Handler-এর parameter interface দিয়ে type করলে NestJS compile হতে দেয় না"),
            ("Interfaces cannot describe optional properties or nested objects", "Interface দিয়ে optional property বা nested object বোঝানো যায় না"),
            ("Interfaces are erased at compile time, so the pipe has no runtime class to read `class-validator` decorators from; classes exist at runtime and carry that metadata", "Interface compile-এর সময় মুছে যায়, তাই pipe runtime-এ কোনো class পায় না যেখান থেকে `class-validator` decorator পড়বে; class runtime-এ থাকে এবং সেই metadata বহন করে"),
        ],
        correct=3,
        a_en=r"""Because interfaces disappear after compilation. `ValidationPipe` needs a real class at runtime: it uses `class-transformer` to turn the plain body into an instance and `class-validator` to read the decorators (`@IsEmail()`, `@Length()`) attached to that class.""",
        a_bn=r"""কারণ compile-এর পরে interface আর থাকে না। `ValidationPipe`-এর runtime-এ একটা আসল class দরকার: `class-transformer` দিয়ে plain body-কে instance বানায়, আর `class-validator` দিয়ে ওই class-এ লাগানো decorator (`@IsEmail()`, `@Length()`) পড়ে।""",
        ex_en=r"""
            A DTO (Data Transfer Object) defines the shape of data crossing a boundary — usually the request body. With an interface, the handler parameter's metadata type becomes `Object`, so the pipe silently skips validation and any payload gets through. That's the dangerous part: no error, just no validation.

            The second option is tempting because some people remember "Nest needs classes", but nothing fails at compile time — it just doesn't validate. Interfaces can describe optional and nested properties perfectly well, so option three is wrong too.

            Note: in NestJS 12 you can also validate with a Standard Schema (e.g. a zod schema) via the `schema` option on `@Body()`. Then the DTO type can be inferred from the schema (`z.infer`) and doesn't need to be a class.
        """,
        ex_bn=r"""
            DTO (Data Transfer Object) একটা boundary পার হওয়া data-র shape ঠিক করে — সাধারণত request body। Interface দিলে handler parameter-এর metadata type হয় `Object`, ফলে pipe চুপচাপ validation skip করে আর যেকোনো payload ঢুকে যায়। বিপদটা এখানেই: কোনো error নেই, শুধু validation নেই।

            দ্বিতীয় option-টা লোভনীয়, কারণ অনেকের মনে থাকে "Nest-এর class লাগে" — কিন্তু compile-এ কিছু fail করে না, শুধু validate হয় না। Interface দিয়ে optional আর nested property ভালোভাবেই বোঝানো যায়, তাই তৃতীয় option-ও ভুল।

            নোট: NestJS 12-এ `@Body()`-এর `schema` option দিয়ে Standard Schema (যেমন zod schema) দিয়েও validate করা যায়। তখন DTO type schema থেকে infer করা যায় (`z.infer`), class হওয়ার দরকার নেই।
        """,
        tip_en=r"""Mention the silent failure: "with an interface, validation is skipped without any error". That's the practical risk interviewers care about.""",
        tip_bn=r"""চুপচাপ fail হওয়ার কথাটা বলো: "interface দিলে কোনো error ছাড়াই validation skip হয়ে যায়"। Interviewer এই practical ঝুঁকিটাই জানতে চায়।""",
        related=["nest-005", "nest-016", "nest-017"],
        refs=[NEST_VALIDATION, NEST_PIPES],
    ),
    # ------------------------------------------------------------------ nest-007
    Q(
        id="nest-007", sub="Guards", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["guards", "canactivate", "executioncontext", "authorization"],
        ver="NestJS 12.1", vs=False, status="stable",
        q_en=r"""What is a guard in NestJS, and what happens when `canActivate()` returns `false`?""",
        q_bn=r"""NestJS-এ guard কী? `canActivate()` যদি `false` return করে তাহলে কী হয়?""",
        a_en=r"""
            A guard is a class implementing `CanActivate` that decides whether the current request may reach the route handler. It's the standard place for authentication and authorization checks.

            `canActivate(context)` receives an `ExecutionContext` (request, handler, controller class) and returns a `boolean`, `Promise<boolean>` or `Observable<boolean>`. If it returns `false`, Nest throws a `ForbiddenException`, so the client gets **403** with `{"message":"Forbidden resource","error":"Forbidden","statusCode":403}`. If I want 401 instead, I throw `UnauthorizedException` myself.

            I bind guards with `@UseGuards()` on a controller or method, or globally with the `APP_GUARD` provider.
        """,
        a_bn=r"""
            Guard হলো `CanActivate` implement করা একটা class, যেটা ঠিক করে current request route handler পর্যন্ত যেতে পারবে কি না। Authentication আর authorization check-এর standard জায়গা এটাই।

            `canActivate(context)` একটা `ExecutionContext` পায় (request, handler, controller class) এবং `boolean`, `Promise<boolean>` বা `Observable<boolean>` return করে। `false` return করলে Nest একটা `ForbiddenException` throw করে, তাই client পায় **403** — `{"message":"Forbidden resource","error":"Forbidden","statusCode":403}`। 401 দিতে চাইলে আমি নিজেই `UnauthorizedException` throw করি।

            Guard bind করি controller বা method-এ `@UseGuards()` দিয়ে, অথবা globally `APP_GUARD` provider দিয়ে।
        """,
        ex_en=r"""
            - **Why guards and not middleware for auth?** A guard has the `ExecutionContext`, so it knows *which handler* will run and can read metadata like `@Roles('admin')` via `Reflector`. Middleware runs before routing decisions and doesn't know that.
            - **Order:** guards run after middleware and before interceptors and pipes. So the body hasn't been validated yet when a guard runs.
            - **DI:** guards are injectable. `app.useGlobalGuards(new MyGuard())` creates the instance yourself (no injection); `{ provide: APP_GUARD, useClass: MyGuard }` lets Nest inject `ConfigService`, `Reflector`, etc.
            - **Transport-agnostic:** the same guard can work for HTTP, WebSockets (`context.switchToWs()`) and microservices (`switchToRpc()`).
            - In the example I compare secrets with `timingSafeEqual` to avoid timing attacks.
        """,
        ex_bn=r"""
            - **Auth-এর জন্য middleware না দিয়ে guard কেন?** Guard-এর কাছে `ExecutionContext` থাকে, তাই সে জানে *কোন handler* চলবে, এবং `Reflector` দিয়ে `@Roles('admin')`-এর মতো metadata পড়তে পারে। Middleware routing-এর আগে চলে, এটা জানে না।
            - **Order:** guard চলে middleware-এর পরে, interceptor আর pipe-এর আগে। তাই guard চলার সময় body এখনো validate হয়নি।
            - **DI:** guard injectable। `app.useGlobalGuards(new MyGuard())` দিলে instance তুমি নিজে বানাচ্ছ (injection নেই); `{ provide: APP_GUARD, useClass: MyGuard }` দিলে Nest `ConfigService`, `Reflector` ইত্যাদি inject করতে পারে।
            - **Transport-agnostic:** একই guard HTTP, WebSocket (`context.switchToWs()`) আর microservice (`switchToRpc()`)-এ কাজ করতে পারে।
            - Example-এ timing attack এড়াতে secret compare করেছি `timingSafeEqual` দিয়ে।
        """,
        tip_en=r"""Give the 403 vs 401 detail — returning `false` gives 403, throwing `UnauthorizedException` gives 401. It's a small detail that shows hands-on experience.""",
        tip_bn=r"""403 আর 401-এর পার্থক্যটা বলো — `false` return করলে 403, `UnauthorizedException` throw করলে 401। ছোট detail, কিন্তু hands-on অভিজ্ঞতা বোঝায়।""",
        mist_en=r"""Expecting `false` to produce 401; registering a guard that needs dependencies with `useGlobalGuards(new Guard())`; reading the validated DTO inside a guard (pipes haven't run yet).""",
        mist_bn=r"""ভাবা যে `false` দিলে 401 আসবে; dependency লাগে এমন guard `useGlobalGuards(new Guard())` দিয়ে register করা; guard-এর ভেতরে validated DTO পড়ার চেষ্টা করা (pipe তখনো চলেনি)।""",
        code=r"""
            import {
              CanActivate, Controller, ExecutionContext, Injectable, UnauthorizedException, UseGuards,
            } from '@nestjs/common';
            import { ConfigService } from '@nestjs/config';
            import { timingSafeEqual } from 'node:crypto';
            import type { Request } from 'express';

            @Injectable()
            export class ApiKeyGuard implements CanActivate {
              constructor(private readonly config: ConfigService) {}

              canActivate(context: ExecutionContext): boolean {
                const req = context.switchToHttp().getRequest<Request>();
                const provided = Buffer.from(req.header('x-api-key') ?? '');
                const expected = Buffer.from(this.config.getOrThrow<string>('INTERNAL_API_KEY'));
                if (provided.length !== expected.length || !timingSafeEqual(provided, expected)) {
                  throw new UnauthorizedException('Invalid API key'); // 401 instead of default 403
                }
                return true;
              }
            }

            @UseGuards(ApiKeyGuard)
            @Controller('internal/reports')
            export class InternalReportsController {}
        """,
        lang="typescript",
        follow=[
            ("How would you build a role-based guard with a `@Roles()` decorator?", "`@Roles()` decorator দিয়ে role-based guard কীভাবে বানাবে?"),
            ("How do you make a guard global but still skip it for public routes?", "Guard global করেও public route-এর জন্য কীভাবে skip করবে?"),
        ],
        related=["nest-015", "nest-021"],
        refs=[NEST_GUARDS],
    ),
    # ------------------------------------------------------------------ nest-008
    Q(
        id="nest-008", sub="Exception Filters", diff="easy", type="output",
        prio="high", market="both", mins=2,
        tags=["exceptions", "httpexception", "exception-filters", "error-response"],
        ver="NestJS 12.1 (built-in global exception filter)", vs=False, status="stable",
        q_en=r"""No custom exception filters are registered. What status code and JSON body does the client receive for `GET /users/missing` and for `GET /users/crash`?""",
        q_bn=r"""কোনো custom exception filter register করা নেই। `GET /users/missing` আর `GET /users/crash` call করলে client কোন status code আর কোন JSON body পাবে?""",
        code=r"""
            import { Controller, Get, NotFoundException } from '@nestjs/common';

            @Controller('users')
            export class UsersController {
              @Get('missing')
              missing() {
                throw new NotFoundException('User 42 not found');
              }

              @Get('crash')
              crash() {
                throw new Error('connect ECONNREFUSED 10.0.0.5:5432');
              }
            }
        """,
        lang="typescript",
        output=r"""
            GET /users/missing -> 404
            {"message":"User 42 not found","error":"Not Found","statusCode":404}

            GET /users/crash -> 500
            {"statusCode":500,"message":"Internal server error"}
        """,
        a_en=r"""
            `/users/missing` returns **404** with `{"message":"User 42 not found","error":"Not Found","statusCode":404}`. `/users/crash` returns **500** with `{"statusCode":500,"message":"Internal server error"}` — the original error message is not sent to the client.

            Nest's built-in global exception filter handles every unhandled exception. `HttpException` subclasses are serialised from their response; anything else is treated as an unknown error, logged on the server and replaced by a generic 500 body.
        """,
        a_bn=r"""
            `/users/missing` দেয় **404**, body `{"message":"User 42 not found","error":"Not Found","statusCode":404}`। `/users/crash` দেয় **500**, body `{"statusCode":500,"message":"Internal server error"}` — আসল error message client-এর কাছে যায় না।

            Nest-এর built-in global exception filter সব unhandled exception handle করে। `HttpException`-এর subclass হলে তার response serialise করে; অন্য যেকোনো কিছু unknown error ধরা হয় — server-এ log হয় আর generic 500 body দিয়ে replace হয়।
        """,
        ex_en=r"""
            Step by step:
            1. `NotFoundException` extends `HttpException` with status 404. Passing a string sets `message`; Nest adds the standard `error` text (`"Not Found"`) and `statusCode`.
            2. The plain `Error` is not an `HttpException`, so the base filter can't know a safe status or message. It logs the stack trace and sends the generic 500 body.

            Why this matters: internal details like `ECONNREFUSED 10.0.0.5:5432` (an internal IP and port) never leak to clients. That's good default security behaviour.

            You can customise the body by passing an object: `new BadRequestException({ code: 'EMAIL_TAKEN', message: '...' })`, or attach a cause: `new NotFoundException('User 42 not found', { cause: err })`. For a consistent error format across the API, write a global exception filter.
        """,
        ex_bn=r"""
            ধাপে ধাপে:
            1. `NotFoundException`, `HttpException`-কে extend করে, status 404। String দিলে সেটা `message` হয়; Nest standard `error` text (`"Not Found"`) আর `statusCode` যোগ করে।
            2. Plain `Error` কোনো `HttpException` নয়, তাই base filter জানে না কোন status বা message দেওয়া নিরাপদ। সে stack trace log করে আর generic 500 body পাঠায়।

            কেন গুরুত্বপূর্ণ: `ECONNREFUSED 10.0.0.5:5432`-এর মতো internal detail (internal IP আর port) কখনো client-এর কাছে leak হয় না। এটা ভালো default security behaviour।

            Object pass করে body customise করা যায়: `new BadRequestException({ code: 'EMAIL_TAKEN', message: '...' })`, অথবা cause যোগ করা যায়: `new NotFoundException('User 42 not found', { cause: err })`। পুরো API-তে একই error format চাইলে একটা global exception filter লেখো।
        """,
        tip_en=r"""Point out the security angle: unknown errors become a generic 500 so stack traces and connection strings don't leak. That turns a trivia answer into a design answer.""",
        tip_bn=r"""Security দিকটা বলো: unknown error generic 500 হয়ে যায়, তাই stack trace বা connection string leak হয় না। এতে একটা মুখস্থ উত্তর design-এর উত্তরে পরিণত হয়।""",
        mist_en=r"""Expecting the raw `Error` message in the response; returning error objects with status 200 instead of throwing; catching errors in every controller with try/catch instead of using filters.""",
        mist_bn=r"""ভাবা যে raw `Error`-এর message response-এ যাবে; throw না করে status 200 দিয়ে error object return করা; filter ব্যবহার না করে প্রতিটা controller-এ try/catch দিয়ে error ধরা।""",
        follow=[
            ("How would you write a global filter that maps a database unique-violation to 409?", "Database unique-violation-কে 409-এ map করতে global filter কীভাবে লিখবে?"),
            ("Where in the request lifecycle do exception filters run?", "Request lifecycle-এর কোথায় exception filter চলে?"),
        ],
        related=["nest-002", "nest-025"],
        refs=[NEST_FILTERS],
    ),
]

if __name__ == "__main__":
    save("nestjs", "b1", QUESTIONS)
