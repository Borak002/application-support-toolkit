# SQL Support Toolkit

Practical SQL queries and investigation patterns for Application Support, Production Support, transaction validation, reconciliation, and data troubleshooting.

## Purpose

This toolkit focuses on using SQL to investigate application and transaction issues without modifying production data unnecessarily.

> **Important:** Always confirm the database, environment, and intended scope before executing queries. Use `SELECT` queries for investigation unless a controlled change has been explicitly authorized.

---

## 1. Inspect Recent Records

Retrieve the latest transactions:

```sql
SELECT *
FROM transactions
ORDER BY created_at DESC
LIMIT 20;
```

Retrieve transactions within a specific period:

```sql
SELECT *
FROM transactions
WHERE created_at >= '2026-10-01'
  AND created_at < '2026-10-02'
ORDER BY created_at;
```

---

## 2. Find Failed Transactions

```sql
SELECT
    id,
    reference,
    status,
    amount,
    created_at
FROM transactions
WHERE status = 'FAILED'
ORDER BY created_at DESC;
```

Search for multiple failure states:

```sql
SELECT
    id,
    reference,
    status,
    amount
FROM transactions
WHERE status IN ('FAILED', 'REVERSED', 'TIMEOUT')
ORDER BY created_at DESC;
```

---

## 3. Investigate Error Messages

```sql
SELECT
    id,
    reference,
    status,
    error_message,
    created_at
FROM transactions
WHERE error_message IS NOT NULL
ORDER BY created_at DESC;
```

Search for a specific error:

```sql
SELECT *
FROM transactions
WHERE error_message ILIKE '%timeout%';
```

---

## 4. Identify Duplicate References

Duplicate transaction references can indicate retry, processing, or integration issues.

```sql
SELECT
    reference,
    COUNT(*) AS occurrence_count
FROM transactions
GROUP BY reference
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;
```

---

## 5. Transaction Reconciliation

Compare transaction counts by status:

```sql
SELECT
    status,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY status
ORDER BY transaction_count DESC;
```

Compare transaction values by status:

```sql
SELECT
    status,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY status
ORDER BY total_amount DESC;
```

---

## 6. Identify Transactions With Missing Data

Find records with missing references:

```sql
SELECT *
FROM transactions
WHERE reference IS NULL
   OR reference = '';
```

Find records with missing status:

```sql
SELECT *
FROM transactions
WHERE status IS NULL;
```

---

## 7. Investigate a Specific Transaction

When a customer or operations team provides a transaction reference:

```sql
SELECT *
FROM transactions
WHERE reference = 'TRANSACTION_REFERENCE';
```

For a specific transaction ID:

```sql
SELECT *
FROM transactions
WHERE id = 12345;
```

---

## 8. Check Processing Duration

If the database contains both creation and completion timestamps:

```sql
SELECT
    id,
    reference,
    created_at,
    completed_at,
    completed_at - created_at AS processing_time
FROM transactions
WHERE completed_at IS NOT NULL
ORDER BY processing_time DESC;
```

This can help identify unusually slow transactions.

---

## 9. Daily Transaction Summary

```sql
SELECT
    DATE(created_at) AS transaction_date,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY DATE(created_at)
ORDER BY transaction_date DESC;
```

---

## 10. Support Investigation Workflow

A basic SQL investigation can follow this sequence:

1. Identify the transaction reference or customer identifier.
2. Confirm the transaction exists.
3. Check the transaction status.
4. Review timestamps.
5. Check error messages or failure reasons.
6. Check for duplicate records.
7. Compare related transactions.
8. Validate the transaction against the expected business state.
9. Document findings.
10. Escalate with evidence when a deeper investigation is required.

---

## Application Support Principle

SQL should be used to **understand what happened before attempting to change anything**.

For production incidents:

* Prefer read-only investigation.
* Never run an `UPDATE` or `DELETE` without authorization.
* Confirm the environment before executing queries.
* Record relevant transaction IDs and timestamps.
* Protect customer and financial data.
* Avoid exposing sensitive information in tickets, screenshots, or public repositories.

---

## Disclaimer

The table and column names used in these examples are generic and are intended for demonstration and learning purposes. They should be adapted to the actual database schema in a controlled environment.
