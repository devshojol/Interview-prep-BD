---
title: "React useEffect explained: dependencies, stale closures and cleanup"
description: Why effects run when they do, why an interval keeps reading an old value, why StrictMode runs effects twice, and when you should not use an effect at all.
publishedAt: 2026-10-13
category: React
tags: [react, useEffect, hooks, stale closures, useEffectEvent]
practice: [react, nextjs]
---

`useEffect` questions show up in React interviews in a few predictable shapes: "what does this timer log?", "why does this component fetch in an infinite loop?", "why does my effect run twice in development?". All of them come from the same three ideas: an effect is a function created during a render, the dependency array decides when React re-runs it, and cleanup undoes the previous run.

This article explains those ideas and walks through the common bugs. It assumes you have used hooks before. Every example was run on React 19.3, and the logs and screen values shown are the real output.

## An effect belongs to a render

Each render of a component is a separate call of your function, with its own props, state and local variables. An effect created during a render **captures that render's values**, exactly like any other closure in JavaScript.

React runs the effect after the render has been committed to the screen. On later renders, it compares each value in the dependency array with its value from the previous render using `Object.is`. If any value changed, React runs the previous effect's cleanup and then the new effect. If none changed, it keeps the old effect, including the old values that effect captured.

- No array: the effect runs after every render.
- `[]`: the effect runs after the first render only, and its cleanup runs on unmount.
- `[a, b]`: the effect runs after the first render and whenever `a` or `b` changes.

The dependency array is not a list of "when to run" triggers you pick freely. It should list every reactive value the effect reads. The React lint rule `react-hooks/exhaustive-deps` checks this, and the rest of this article shows what happens when the array lies.

## The stale closure

This timer is meant to count up once per second (100 ms here, to make it quick to test):

```jsx
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      console.log('tick', count);
      setCount(count + 1);
    }, 100);
    return () => clearInterval(id);
  }, []);

  return <p>{count}</p>;
}
```

After 350 ms it has logged `tick 0` three times, and the screen shows **1** and never changes.

The empty array means the effect runs once, after the first render, where `count` is `0`. The interval callback closes over that `count`, so every tick computes `0 + 1` and sets `1` again. The component does re-render with `count` equal to `1`, but that render's values never reach the interval, because the effect was not re-run.

There are two honest fixes:

- **Do not read the state at all.** A functional update receives the current value from React: `setCount((c) => c + 1)`. With that change, the same component shows `3` after 350 ms, and the empty dependency array is now truthful because the effect no longer reads `count`.
- **Declare the dependency.** `[count]` makes React clear and recreate the interval on every change. It is correct but does more work, and for timers it can drift.

Adding `count` to the array while silencing the lint warning, or keeping `[]` and reading `count`, are the two ways of getting this wrong. [Question react-012](app:#/q/react-012) is this exact bug.

## Infinite loops from object dependencies

```jsx
function Products({ category }) {
  const [products, setProducts] = useState([]);
  const filters = { category, sort: 'newest' };

  useEffect(() => {
    fetchProducts(filters).then(setProducts);
  }, [filters]);
  // ...
}
```

`filters` is a **new object on every render**, and `Object.is` compares objects by identity, so the dependency always "changes". The effect runs after every render. Each fetch calls `setProducts` with a new array, which causes another render, which creates another `filters` object, and the cycle continues. In testing, an effect depending on an inline object ran on every one of three renders even though nothing meaningful changed.

Depend on the primitive values instead, and build the object inside the effect:

```jsx
useEffect(() => {
  fetchProducts({ category, sort: 'newest' }).then(setProducts);
}, [category]);
```

If an object or function genuinely has to be shared, `useMemo` or `useCallback` can keep its identity stable. Moving it inside the effect is usually simpler. [Question react-018](app:#/q/react-018) shows the production symptoms of this bug: hundreds of requests per second and a sluggish tab.

## Cleanup and race conditions

Cleanup runs before the effect re-runs and when the component unmounts. Its job is to undo whatever the effect started: clear timers, remove listeners, close connections, and ignore responses that are no longer wanted.

Data fetching needs that last one. If the user types `re` and then `react`, two requests are in flight, and the slower one can arrive last:

```jsx
function Search({ query }) {
  const [results, setResults] = useState(null);

  useEffect(() => {
    let ignore = false;
    searchApi(query).then((data) => {
      if (!ignore) setResults(data);
    });
    return () => {
      ignore = true;
    };
  }, [query]);
  // ...
}
```

When `query` changes, the cleanup of the previous run sets its `ignore` flag, so a late response for `re` is dropped. In a test where the `re` request took 200 ms and the `react` request 50 ms, the screen correctly ended on the results for `react`. Passing an `AbortController` signal to `fetch` and calling `abort()` in the cleanup also cancels the network request itself.

In real applications, a data-fetching library or your framework's data APIs usually handle caching and races for you. Knowing this pattern still matters, because it is what those tools do underneath.

## Why effects run twice in development

With `<StrictMode>`, React runs an extra **setup, cleanup, setup** cycle when a component first mounts in development. For this component:

```jsx
function ChatRoom({ roomId }) {
  useEffect(() => {
    console.log('connect', roomId);
    return () => console.log('disconnect', roomId);
  }, [roomId]);
  return null;
}
```

the first mount logs `connect general`, `disconnect general`, `connect general`. Changing the room afterwards logs only `disconnect general`, `connect jobs`. In a production build, the first mount logs `connect general` once.

This is deliberate. It simulates the component being unmounted and remounted, so an effect with a missing or broken cleanup shows its bug immediately instead of in production. The fix is never to "prevent" the second run with a ref. It is to make the cleanup undo the setup, so that running setup, cleanup, setup behaves like setup once. [Question react-013](app:#/q/react-013) asks for these exact logs.

## Reading the latest value without re-running: useEffectEvent

Sometimes an effect needs a value it should **not** react to. For example, you want to reconnect when the room changes, but showing a notification in the current theme should not cause a reconnect when the theme changes. React 19.2 added `useEffectEvent` for this:

```jsx
function ChatRoom({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    showNotification(`Connected to ${roomId}`, theme);
  });

  useEffect(() => {
    const connection = connect(roomId);
    connection.on('connected', () => onConnected());
    return () => connection.disconnect();
  }, [roomId]);
  // ...
}
```

The function returned by `useEffectEvent` always sees the latest props and state, and it is not a dependency. In testing, changing only `theme` did not re-run the effect, and the next time the room changed, the event read the new theme. Effect Events are meant to be called from inside effects only. They are not a general way to silence the dependency linter. [Question react-027](app:#/q/react-027) covers `useEffectEvent` together with `<Activity>`.

## When you do not need an effect

Many effects in interview code should not exist. An effect synchronises a component with something **outside React**: a network request, a subscription, a timer, a browser API. If you are only computing a value from props or state, compute it during render:

```jsx
// Unnecessary: an extra render, and a moment where fullName is stale
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// Better: derived during render
const fullName = `${firstName} ${lastName}`;
```

Likewise, code that responds to a specific user action (submitting a form, clicking "buy") belongs in the event handler, not in an effect that watches state. React's guide [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) has many more cases.

## What to say in an interview

When you are asked to explain or fix an effect, these points cover most questions:

1. Each render has its own values, and an effect captures the values of the render that created it.
2. The dependency array must list every reactive value the effect reads. React compares them with `Object.is`.
3. Stale values come from dependencies that are missing. The fix is a functional update, a correct dependency, or `useEffectEvent`, not a disabled lint rule.
4. New objects and functions created during render change on every render, so depending on them re-runs the effect every time.
5. Cleanup undoes the setup. StrictMode's extra mount cycle in development exists to prove that it does.
6. If nothing outside React is involved, you probably do not need an effect.

The React reference for [useEffect](https://react.dev/reference/react/useEffect) and the guides on [synchronizing with effects](https://react.dev/learn/synchronizing-with-effects) and [separating events from effects](https://react.dev/learn/separating-events-from-effects) go deeper. To practise, the [React question set](app:#/questions?tech=react) includes graded output, debugging and design questions on hooks, and the [Next.js set](app:#/questions?tech=nextjs) covers how these rules interact with Server and Client Components.
