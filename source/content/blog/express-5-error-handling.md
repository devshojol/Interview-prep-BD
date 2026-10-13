---
title: "Error handling in Express 5: async routes, error middleware and 404s"
description: How Express 5 forwards errors from async route handlers, how to write one error handler for a REST API, and the gaps Express still cannot catch for you.
publishedAt: 2026-10-13
category: Backend Development
tags: [express, node.js, error handling, rest api, middleware]
practice: [express, nodejs]
---

Error handling is one of the most practical backend interview topics because it shows whether you have run an API in production. Typical questions sound like: what happens when an `async` route handler throws, where do 404s come from, and why do the logs say "Cannot set headers after they are sent"?

Express 5 changed the answer to the first of those. This article explains what Express 5 does with errors, builds a small centralised error handler you can reuse, and lists the cases Express still cannot catch. It assumes you have written Express routes before. The code was run on Express 5.1, and the behaviour described applies to the whole 5.x line. The Express 4 behaviour shown for comparison was run on Express 4.21.

## What changed in Express 5

In Express 5, if a route handler or middleware **returns a rejected promise**, Express catches the rejection and calls `next(err)` for you. An `async` function that throws, or that awaits something that rejects, returns a rejected promise, so this now reaches your error handler:

```js
app.get('/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id); // if this rejects...
  res.json(user);                                       // ...Express 5 calls next(err)
});
```

Express 4 did not look at the return value of handlers. The same route on Express 4 produces an `unhandledRejection` event, and the request never gets a response: the client waits until something times out. That is why Express 4 codebases are full of `try/catch` blocks that call `next(err)`, or wrapper helpers such as `asyncHandler(fn)`. On Express 5 you can delete those wrappers. [Question express-005](app:#/q/express-005) asks exactly what happens in this situation.

Synchronous throws were already handled in both versions: if a handler throws before returning, Express catches it and forwards it.

## One error handler for the whole API

Express recognises error-handling middleware by its **four parameters**, `(err, req, res, next)`. Register it after all routes. Together with a model for expected errors, it gives every endpoint the same response shape:

```js
import express from 'express';

class AppError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

const app = express();
app.use(express.json());

app.get('/users/:id', async (req, res) => {
  const user = await findUser(req.params.id);
  if (!user) throw new AppError(404, 'USER_NOT_FOUND', `User ${req.params.id} not found`);
  res.json(user);
});

// 404: runs only when no route matched
app.use((req, res) => {
  res.status(404).json({ error: { code: 'ROUTE_NOT_FOUND', message: `No route for ${req.method} ${req.path}` } });
});

// Error handler: four parameters, registered last
app.use((err, req, res, next) => {
  if (res.headersSent) return next(err);

  if (err instanceof AppError) {
    return res.status(err.status).json({ error: { code: err.code, message: err.message } });
  }
  if (err.type === 'entity.parse.failed') {
    return res.status(400).json({ error: { code: 'INVALID_JSON', message: 'Request body is not valid JSON' } });
  }
  console.error(err); // unexpected: log the details, hide them from the client
  res.status(500).json({ error: { code: 'INTERNAL', message: 'Something went wrong' } });
});
```

Running requests against it gives:

| Request | Status | Error code |
|---|---:|---|
| `GET /users/7` (exists) | 200 | none |
| `GET /users/9` (missing) | 404 | `USER_NOT_FOUND` |
| `GET /nope` | 404 | `ROUTE_NOT_FOUND` |
| `POST /users` with a malformed JSON body | 400 | `INVALID_JSON` |

A few decisions in that code are worth being able to explain.

### Expected errors versus bugs

`AppError` represents **operational** errors: things that are part of normal use, such as "not found", "validation failed" or "conflict". They carry a status and a stable, machine-readable `code` that clients can branch on. Anything else is treated as a bug or an outage. It gets logged in full, and the client gets a generic 500 so stack traces, SQL and internal messages never leak. [Question express-006](app:#/q/express-006) asks you to design this split and map library errors to HTTP statuses.

### 404 is not an error in Express

When no route matches, Express does not call your error handler. The request falls through to the end of the stack, and Express sends its default "Cannot GET /path" page. To control the response, add an ordinary middleware with **two or three parameters** after all your routes, as above. Its order relative to the error handler does not change behaviour: Express skips error handlers while there is no error and skips ordinary middleware once there is one. Placing it just before the error handler simply keeps the end of the file readable.

### The `res.headersSent` check

If an error happens after the response has started (for example while streaming), you cannot send a new status or JSON body. Delegating to `next(err)` lets Express's built-in handler close the connection properly. It is a cheap guard that turns a confusing secondary crash into a clean failure.

### Errors from body parsing

`express.json()` raises an error with `type: 'entity.parse.failed'` and `status: 400` for malformed JSON. Without a specific branch, that would surface as a 500, which tells the client the server is broken when in fact the request is.

## What Express still does not catch

Express 5 sees errors that happen *in* a handler's promise chain. It cannot see errors in code that runs later, outside that chain:

- **Callbacks scheduled from a handler.** A throw inside `setTimeout`, an event-emitter listener or a callback-style API happens on a later turn of the event loop, with no request context. Convert callbacks to promises and `await` them inside the handler.
- **Promises you start but do not return or await.** A "fire-and-forget" call such as `sendEmail(user)` without `await` rejects on its own. Await it, or attach a `.catch()` that logs the failure.
- **Stream errors.** Pipe with `stream.pipeline()` (or `await pipeline(...)` from `node:stream/promises`) so errors are propagated and the streams are cleaned up.

For truly unexpected failures, log `unhandledRejection` and `uncaughtException` at the process level. After an uncaught exception the process may be in an unknown state, so the safe response is to log, stop accepting traffic and exit, and let your process manager start a fresh instance.

## A classic bug: responding twice

This handler "rejects" invalid input, but the logs fill up with `ERR_HTTP_HEADERS_SENT`:

```js
app.post('/orders', async (req, res) => {
  if (req.body.quantity < 1) {
    res.status(400).json({ error: { code: 'INVALID_QUANTITY' } });
  }
  const order = await createOrder(req.body);
  res.status(201).json(order);
});
```

`res.json()` sends a response but does not stop the function. Execution continues, creates the order anyway and then tries to send a second response. The fix is `return res.status(400).json(...)`, or throwing an `AppError` so the error handler responds. Note that the bug is worse than the log noise suggests: the invalid order was saved. [Question express-011](app:#/q/express-011) is this scenario.

## Interview checklist

If you are asked to review an Express API's error handling, these are the points to cover:

1. Which Express version? On 4.x, every `async` handler needs a wrapper or `try/catch` with `next(err)`. On 5.x, rejected promises are forwarded.
2. Is there exactly one error handler, with four parameters, registered last?
3. Is there a 404 handler before it?
4. Are expected errors distinguished from bugs, with stable error codes and no leaked internals?
5. Are fire-and-forget promises, callbacks and streams handled?
6. Is every early `res.send()` or `res.json()` followed by a `return`?

The Express guides on [error handling](https://expressjs.com/en/guide/error-handling.html) and [migrating to Express 5](https://expressjs.com/en/guide/migrating-5.html) are the primary references. To practise, the [Express question set](app:#/questions?tech=express) covers middleware, validation and authentication, and the [Node.js set](app:#/questions?tech=nodejs) covers the event loop and process-level failures behind several of these bugs.
