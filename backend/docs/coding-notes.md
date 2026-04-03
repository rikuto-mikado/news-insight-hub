# Backend Coding Notes

## String Prefixes: `r""` vs `f""`

- `r"..."` — raw string. Backslashes are not treated as escape sequences. Used for regex patterns and URL paths.
- `f"..."` — format string. Allows variable interpolation via `{}`. Used for dynamic strings.

```python
r"articles"   # raw string, same as "articles" here — just a convention for URL patterns
f"hello {name}"  # becomes "hello John" if name = "John"
```

---

## ViewSet: `ModelViewSet` vs `ReadOnlyModelViewSet`

- `ModelViewSet` — provides full CRUD (list, retrieve, create, update, destroy).
- `ReadOnlyModelViewSet` — provides only read operations (list, retrieve). No POST/PUT/DELETE.

Use `ReadOnlyModelViewSet` when clients should not be able to modify data directly — e.g., news articles fetched from external sources.

---

## Serializer `fields`: `"__all__"` vs explicit list

- `"__all__"` — includes every model field automatically. Convenient but risky if sensitive fields are added later.
- Explicit list — safer, exposes only what is intentionally defined.

```python
fields = "__all__"  # all fields
fields = ["id", "title", "url", "published_date"]  # explicit
```

---

## `os.environ.get(key, default)`

Reads an environment variable. If the variable is not set, falls back to the default value.

```python
os.environ.get("DB_HOST", "localhost")
# uses DB_HOST if set, otherwise "localhost"
```

Useful for running the same code in Docker (where DB_HOST=db) and locally (where DB_HOST=localhost).

---

## Django Migrations

When you change a model (add/remove/modify a field), the database table does NOT update automatically. You must run migrations to sync the model with the database.

```bash
# Step 1: Generate a migration file from model changes
docker compose exec backend python manage.py makemigrations

# Step 2: Apply the migration to the database
docker compose exec backend python manage.py migrate
```

- Skipping this will cause errors when Django tries to access a column that doesn't exist in the DB.
- Always run both commands after editing `models.py`.
