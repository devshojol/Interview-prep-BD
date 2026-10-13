---
title: "SQL JOIN and GROUP BY traps: WHERE vs HAVING, LEFT JOIN filters and NULL"
description: Four SQL mistakes that quietly return wrong numbers, shown on one small dataset with the exact result of each query and the fix.
publishedAt: 2026-10-13
category: Databases and SQL
tags: [sql, joins, group by, having, null, postgresql]
practice: [sql, postgresql]
---

Most SQL interview questions are not about syntax. They are about queries that run without errors and return the wrong numbers. This article covers four of those traps: filtering a `LEFT JOIN` in the wrong place, `COUNT(*)` versus `COUNT(column)`, `WHERE` versus `HAVING`, and `NOT IN` with a `NULL`. Each one uses the same tiny dataset, so you can check every result by hand.

It is written for developers who can write joins and aggregates but want to reason about them precisely. Every query below was run on PostgreSQL, and the results shown are the actual output. The behaviour is standard SQL, so other databases agree on these examples.

## The dataset

```sql
CREATE TABLE customers (id INT PRIMARY KEY, name TEXT NOT NULL, city TEXT);
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT,               -- NULL for a guest checkout
  status TEXT NOT NULL,
  amount NUMERIC(10,2) NOT NULL
);

INSERT INTO customers VALUES
  (1, 'Rahim', 'Dhaka'), (2, 'Karim', 'Chattogram'), (3, 'Nadia', 'Dhaka'), (4, 'Sumi', NULL);

INSERT INTO orders VALUES
  (10, 1, 'delivered', 1200), (11, 1, 'cancelled', 300),
  (12, 2, 'delivered', 800),  (13, 2, 'delivered', 450),
  (14, NULL, 'delivered', 999);
```

Rahim has one delivered and one cancelled order. Karim has two delivered orders. Nadia and Sumi have no orders. Order 14 is a guest checkout with no customer.

## Trap 1: a WHERE clause that turns a LEFT JOIN into an inner join

The task: list **every** customer with their number of delivered orders, including customers with zero. A `LEFT JOIN` keeps customers without orders, so this looks right:

```sql
SELECT c.name, COUNT(o.id) AS delivered_orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.status = 'delivered'
GROUP BY c.name
ORDER BY c.name;
```

| name | delivered_orders |
|---|---:|
| Karim | 2 |
| Rahim | 1 |

Nadia and Sumi have disappeared. For customers without orders, the `LEFT JOIN` produces a row whose `o.*` columns are all `NULL`. Then `WHERE o.status = 'delivered'` compares `NULL` to a string, which is not true, so those rows are removed. The join is still written as `LEFT`, but the filter has made it behave like an `INNER JOIN`.

The fix is to move the condition on the right-hand table into the `ON` clause. It then decides *which orders match*, not *which result rows survive*:

```sql
SELECT c.name, COUNT(o.id) AS delivered_orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'
GROUP BY c.name
ORDER BY c.name;
```

| name | delivered_orders |
|---|---:|
| Karim | 2 |
| Nadia | 0 |
| Rahim | 1 |
| Sumi | 0 |

The rule of thumb: in a `LEFT JOIN`, conditions on the **left** table can go in `WHERE`. Conditions on the **right** table belong in `ON`, unless you deliberately want to drop the unmatched rows. [Question sql-019](app:#/q/sql-019) tests how many rows a `LEFT JOIN` returns, and [sql-003](app:#/q/sql-003) is this exact task with a twist.

## Trap 2: COUNT(*) counts the empty row

In the fixed query we used `COUNT(o.id)`. Here is what `COUNT(*)` would have given:

```sql
SELECT c.name, COUNT(*) AS count_star, COUNT(o.id) AS count_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'
GROUP BY c.name
ORDER BY c.name;
```

| name | count_star | count_id |
|---|---:|---:|
| Karim | 2 | 2 |
| Nadia | 1 | 0 |
| Rahim | 1 | 1 |
| Sumi | 1 | 0 |

`COUNT(*)` counts rows, and Nadia and Sumi each still have one row: the unmatched row the `LEFT JOIN` keeps for them. `COUNT(o.id)` counts non-null values, so the all-`NULL` row counts as zero. After an outer join, count a column from the optional side, ideally its primary key.

The same `NULL` behaviour affects other aggregates. `SUM`, `AVG`, `MIN` and `MAX` ignore `NULL`s, and over a group with no non-null values they return `NULL`, not `0`:

```sql
SELECT c.name, SUM(o.amount) AS total, COALESCE(SUM(o.amount), 0) AS total_or_zero
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'delivered'
GROUP BY c.name
ORDER BY c.name;
```

| name | total | total_or_zero |
|---|---:|---:|
| Karim | 1250.00 | 1250.00 |
| Nadia | NULL | 0 |
| Rahim | 1200.00 | 1200.00 |
| Sumi | NULL | 0 |

If the application expects a number, wrap the aggregate in `COALESCE`. [Question sql-005](app:#/q/sql-005) checks aggregates over `NULL`s.

## Trap 3: WHERE filters rows, HAVING filters groups

`WHERE` runs before grouping and sees individual rows. `HAVING` runs after grouping and sees groups, so it is where aggregate conditions go. Compare two questions that sound similar.

"Customers with a delivered order **over 1,000**", a condition on single rows:

```sql
SELECT c.name, SUM(o.amount) AS delivered_total
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.status = 'delivered' AND o.amount > 1000
GROUP BY c.name;
```

This returns only Rahim (1200.00). None of Karim's orders is over 1,000 on its own.

"Customers whose delivered orders **total** over 1,000", a condition on the group:

```sql
SELECT c.name, SUM(o.amount) AS delivered_total
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.status = 'delivered'
GROUP BY c.name
HAVING SUM(o.amount) > 1000;
```

This returns Karim (1250.00) and Rahim (1200.00). Karim qualifies because his two orders add up to 1,250.

Putting an aggregate in `WHERE` is not just wrong, it is an error. PostgreSQL reports `aggregate functions are not allowed in WHERE`. The underlying idea is the **logical processing order**: `FROM` and joins, then `WHERE`, then `GROUP BY`, then `HAVING`, then `SELECT`, then `ORDER BY`. That order also explains why a column alias defined in `SELECT` cannot be used in `WHERE`. [Question sql-001](app:#/q/sql-001) asks for that order directly, and [sql-004](app:#/q/sql-004) needs both clauses in one query.

Use `WHERE` for anything that does not need an aggregate, even when you also have a `HAVING`. Filtering early means fewer rows to group.

## Trap 4: NOT IN with a NULL returns nothing

The task: find customers who have never placed an order. This version looks natural:

```sql
SELECT name FROM customers
WHERE id NOT IN (SELECT customer_id FROM orders);
```

It returns **zero rows**, even though Nadia and Sumi have no orders. The subquery's results include the guest checkout's `NULL`. For Nadia, `3 NOT IN (1, 1, 2, 2, NULL)` means `3 <> 1 AND 3 <> 2 AND 3 <> NULL`. The last comparison is `UNKNOWN`, so the whole condition is `UNKNOWN`, and `WHERE` keeps only rows where the condition is `TRUE`.

`NOT EXISTS` does not have this problem, because it asks whether a matching row exists rather than comparing against a list:

```sql
SELECT c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

This returns Nadia and Sumi. A `LEFT JOIN ... WHERE o.id IS NULL` anti-join gives the same result. Prefer one of those two whenever the subquery column can contain `NULL`, which is the case for any nullable foreign key. [Question sql-016](app:#/q/sql-016) is built around this guest-checkout scenario.

The same three-valued logic catches simpler filters too. `WHERE city <> 'Dhaka'` on our customers returns only Karim. Sumi's `NULL` city is not "not Dhaka", it is unknown. If you mean "anything except Dhaka, including unknown", write `city IS DISTINCT FROM 'Dhaka'` in PostgreSQL, or `city <> 'Dhaka' OR city IS NULL`. See [sql-006](app:#/q/sql-006).

## How to talk through these in an interview

When you are given a query to fix or predict, say the steps out loud:

1. **Which rows does the join produce?** Write a few of them down, including the `NULL`-filled rows from outer joins.
2. **Which rows does `WHERE` keep?** Remember that a comparison with `NULL` is never true.
3. **How are the rows grouped, and what does each aggregate see?** `COUNT(*)` counts rows, `COUNT(column)` and `SUM(column)` skip `NULL`s.
4. **Which groups does `HAVING` keep?**

That is the logical processing order, and following it is how you avoid all four traps. The PostgreSQL documentation on [joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN), [aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html) and [subquery expressions](https://www.postgresql.org/docs/current/functions-subquery.html) covers each rule in detail. For practice, the [SQL question set](app:#/questions?tech=sql) has graded join, aggregate and `NULL` questions, and the [PostgreSQL set](app:#/questions?tech=postgresql) goes further into indexes and query plans.
