# SQL Injection - Blind 

This project demonstrates a Boolean-based Blind SQL Injection vulnerability using Flask and SQLite. The application takes the TrackingId cookie from the request and directly adds it into the SQL query. Because of this, the SQL query can be modified with an injection payload. Instead of displaying database results, the application returns different responses based on whether the query is true or false. This behavior can be used to extract sensitive information one character at a time.

# Vulnerability

The application directly adds the TrackingId cookie value into the SQL query without using parameterized queries. This allows user input to modify the SQL query and makes the application vulnerable to SQL Injection.

```python
query = "SELECT id FROM analytics WHERE tracking_id = '" + tracking + "';"
```

A custom TrackingId cookie is created to test the application.

![Image](screenshots/image%20(1).png)

A single quote (') is added to the TrackingId cookie. An SQL error is returned, confirming that the application is vulnerable to SQL Injection.

![Image](screenshots/image%20(2).png)

A condition that is always true is added to the TrackingId cookie. The application returns Welcome back, confirming that the injected condition is evaluated as true.

```python
SELECT id FROM analytics WHERE tracking_id = 'abc123' OR '1'='1';
```

![Image](screenshots/image%20(3).png)

A condition that is always false is added to the TrackingId cookie. The application returns Hello visitor, confirming that the injected condition is evaluated as false.

![Image](screenshots/image%20(4).png)

A Boolean condition is used to check the first character of the administrator's password. When the condition is true, the application returns Welcome back.

![Image](screenshots/image%20(5).png)


## Secure Version

The secure version uses a parameterized query, so the TrackingId value is treated as data instead of SQL code.

```python
cur.execute("SELECT id FROM analytics WHERE tracking_id = ?", (tracking,))
```