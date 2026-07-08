# Basic SQL Injection 

This project display a basic SQL Injection vulnerability in a Flask application using SQLite.

## Vulnerability

The application connects user input directly into the SQL query.

```python
query = f"SELECT name FROM products WHERE category = '{category}' AND released = 0"
```

## Project Structure

```
app.py
products.db
requirements.txt
```

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Example

Normal request

```
/search?category=clothing
```
![Normal Request](screenshots/normal-request.png)

Injection request

```
/search?category=clothing' OR 1=1--
```
![SQL Injection](screenshots/sqli-request.png)

## Secure Version
```python
query = "SELECT name FROM products WHERE category = ? AND released = 0"
cursor.execute(query, (category,))
```