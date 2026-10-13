---
title: How to predict JavaScript output with promises, timers and async/await
description: A step-by-step method for "what does this code log?" questions: the call stack, the microtask queue, task queues, and where await actually pauses.
publishedAt: 2026-10-13
category: JavaScript
tags: [event loop, promises, async/await, microtasks, output prediction]
practice: [javascript, nodejs]
featured: true
---

Output-prediction questions give you a few lines of code that mix `console.log`, `setTimeout`, promises and `async` functions, and ask for the exact order of the logs. They are short, but they test whether you have an accurate model of how JavaScript schedules work. This article gives you that model as a procedure you can apply line by line, then works through the cases that catch people out.

It is written for developers who already use promises and `async/await` day to day but tend to guess when the order matters. Every output shown here was run on Node.js, and the browser behaves the same way for these examples unless a section says otherwise.

## The model: one stack, one microtask queue, task queues

JavaScript runs your code on a single thread with a **call stack**. Asynchronous work does not interrupt the stack. Instead, callbacks wait in queues until the stack is empty:

- **Microtasks** come from promise reactions (`.then`, `.catch`, `.finally`), the continuation after an `await`, and `queueMicrotask()`.
- **Tasks** (also called macrotasks) come from timers (`setTimeout`, `setInterval`), I/O, UI events and similar sources.

The rule that answers most questions is this: **when the call stack empties, the engine runs every queued microtask, including microtasks queued by other microtasks, before it takes the next task.** One task, then all microtasks, then the next task, and so on.

So the procedure is:

1. Run the synchronous code top to bottom. Log anything it logs immediately.
2. While doing that, note where each callback is queued: the microtask queue or a task queue.
3. When the synchronous code finishes, drain the microtask queue in order. New microtasks join the end of the same queue and run in this same drain.
4. Take the oldest ready task (for timers with the same delay, that is the order they were scheduled), run it, then drain microtasks again.

## A first example

```js
console.log('A');
setTimeout(() => console.log('B'), 0);
Promise.resolve().then(() => console.log('C'));
queueMicrotask(() => console.log('D'));
console.log('E');
```

Apply the procedure. The synchronous pass logs `A` and `E`. Along the way it queues a timer task (`B`) and two microtasks (`C`, then `D`). When the stack empties, the microtasks run in order, and only then the timer:

```text
A
E
C
D
B
```

A delay of `0` does not mean "now". It means "as a task, no earlier than 0 ms from now", which always puts it behind every microtask that is already queued.

## Where `await` actually pauses

An `async` function runs **synchronously until its first `await`**. Everything after the `await` becomes a microtask continuation. People often get this wrong in both directions: they assume the whole function is deferred, or they assume nothing is.

```js
async function load() {
  console.log('1: load starts');
  await null;
  console.log('4: after await');
}
console.log('0: script start');
load();
Promise.resolve().then(() => console.log('5: then callback'));
console.log('2: script continues');
setTimeout(() => console.log('6: timeout'), 0);
console.log('3: script end');
```

```text
0: script start
1: load starts
2: script continues
3: script end
4: after await
5: then callback
6: timeout
```

`load()` logs line 1 immediately, because no `await` has happened yet. The `await null` queues the rest of `load` as a microtask *before* the `.then` callback is queued, so line 4 comes before line 5. The timeout is a task, so it is last.

Awaiting a value that is not a promise still yields. `await null` and `await 42` both suspend the function and resume it from the microtask queue.

## Microtasks queued by microtasks

Because the queue is drained completely, a microtask that schedules another microtask still runs before any timer, but it joins the *end* of the queue:

```js
setTimeout(() => console.log('timeout 1'), 0);
setTimeout(() => console.log('timeout 2'), 0);
Promise.resolve().then(() => {
  console.log('micro 1');
  Promise.resolve().then(() => console.log('micro 1.1'));
});
Promise.resolve().then(() => console.log('micro 2'));
```

```text
micro 1
micro 2
micro 1.1
timeout 1
timeout 2
```

`micro 1.1` is queued while `micro 1` runs, so it waits behind `micro 2`, which was already queued. Both timers wait until the queue is empty.

This is also why a loop that keeps queueing microtasks can freeze a page: the browser never gets back to tasks such as rendering or input, because the microtask queue never empties. Splitting long work into tasks (or using a worker) is the fix, and it comes up in [question js-034](app:#/q/js-034).

## Microtasks run between tasks too

The drain does not only happen after the main script. It happens after **every** task:

```js
setTimeout(() => {
  console.log('timeout 1');
  Promise.resolve().then(() => console.log('micro inside timeout 1'));
}, 0);
setTimeout(() => console.log('timeout 2'), 0);
```

```text
timeout 1
micro inside timeout 1
timeout 2
```

The promise callback queued inside the first timer runs before the second timer, even though both timers were ready at the same moment.

## Node.js: `process.nextTick` and module type

Node adds `process.nextTick()`, which has its own queue. In a CommonJS script, the next-tick queue is processed before promise microtasks:

```js
Promise.resolve().then(() => console.log('promise'));
process.nextTick(() => console.log('nextTick'));
console.log('sync');
```

Run as a CommonJS file (`.cjs`), this prints `sync`, `nextTick`, `promise`. Run the same lines as an ES module (`.mjs`) and it prints `sync`, `promise`, `nextTick`, because an ES module's top-level code is itself evaluated asynchronously and the promise queue is drained first. If an interview question uses `nextTick`, it is worth saying which module system you are assuming. The Node.js guide to [the event loop, timers and nextTick](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) describes the phases in detail.

## Sequential versus parallel `await`

Ordering questions often turn into performance questions. These two functions wait for the same two 100 ms timers:

```js
function wait(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function sequential() {
  await wait(100);
  await wait(100); // starts only after the first finishes: about 200 ms in total
}

async function parallel() {
  await Promise.all([wait(100), wait(100)]); // both timers run together: about 100 ms
}
```

`sequential` takes about 200 ms because the second timer is not even created until the first `await` resumes. `parallel` starts both before awaiting, so it takes about 100 ms. When the operations are independent, start them first and await them together. When one needs the result of the other, sequential is correct and the extra time is the cost of the dependency.

## Mistakes that lose marks

- **Treating `setTimeout(fn, 0)` as immediate.** It is a task, so every microtask queued before it runs first.
- **Assuming an `async` function is deferred as a whole.** The code before the first `await` runs synchronously, inside the caller's turn.
- **Forgetting that new microtasks go to the end of the queue.** They run in the same drain, but after microtasks that were already waiting.
- **Explaining with "promises are faster than timers".** The real answer is about queues: microtasks are drained before the next task is taken. Interviewers usually want the mechanism, not a rule of thumb.
- **Mixing up `try/catch` and un-awaited promises.** A `try` block only catches a rejection if the promise is awaited inside it. [Question js-023](app:#/q/js-023) is a compact example.

## Practise the procedure

The fastest way to make this automatic is to write the order down before you run anything, then check. The practice bank has graded versions of exactly these patterns:

- [js-016](app:#/q/js-016): the call stack, microtask queue and task queue in one small program.
- [js-017](app:#/q/js-017): log order with `async` functions and `await`.
- [js-029](app:#/q/js-029): a harder mix of timers, promise chains and nested microtasks.
- [js-024](app:#/q/js-024): a debugging question where `forEach` with an `async` callback does not wait.

For the specification-level view, MDN's [guide to microtasks](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide) and the HTML Standard's [event loop processing model](https://html.spec.whatwg.org/multipage/webappapis.html#event-loops) are the primary references.
