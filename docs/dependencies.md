# Backend Dependencies

A detailed guide to every package installed for this Django backend.

---

## Overview

| Package | Category | Purpose |
|---|---|---|
| `django` | Framework | Core web framework |
| `djangorestframework` | Framework | REST API layer |
| `psycopg2-binary` | Database | PostgreSQL driver |
| `python-dotenv` | Config | Load `.env` files |
| `django-environ` | Config | Parse env vars into Django settings |
| `django-cors-headers` | Security | Allow cross-origin requests from frontend |
| `drf-spectacular` | Docs | Generate OpenAPI schema + Swagger UI |
| `gunicorn` | Server | Production WSGI server |

---

## Django & Django REST Framework

```
pip install django djangorestframework
```

**Django** is the core web framework. It handles routing, ORM, migrations, authentication, admin, and more.

**Django REST Framework (DRF)** sits on top of Django and provides everything needed to build Web APIs:

- `ModelSerializer` — turns Django models into JSON automatically
- `ViewSet` + `Router` — maps CRUD operations to HTTP methods with minimal boilerplate
- Authentication classes — Token, Session, JWT (via third-party)
- Permission classes — `IsAuthenticated`, `IsAdminUser`, custom rules
- Browsable API — a built-in HTML interface for testing endpoints in the browser

```python
# settings.py
INSTALLED_APPS = [
    ...
    "rest_framework",
]
```

---

## psycopg2-binary

```
pip install psycopg2-binary
```

The adapter that lets Python talk to PostgreSQL. Without it, Django's PostgreSQL backend (`django.db.backends.postgresql`) cannot connect to the database.

> **Why `-binary`?**
> The binary variant ships with precompiled C extensions, so no local `libpq` or compiler setup is needed. Ideal for development and Docker-based deployments. For production on bare metal, `psycopg2` (without `-binary`) compiled against the system's `libpq` is often preferred for performance.

```python
# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5432"),
    }
}
```

---

## python-dotenv & django-environ

```
pip install python-dotenv django-environ
```

These two packages work together to keep secrets and environment-specific config out of source code.

### How they complement each other

| | `python-dotenv` | `django-environ` |
|---|---|---|
| Reads `.env` file | Yes | Yes (via `env.read_env()`) |
| Parses typed values | No | **Yes** — int, bool, list, URL, etc. |
| Django-specific helpers | No | **Yes** — `db_url()`, `cache_url()` |

### Typical usage

```python
# settings.py
import environ

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])
```

```bash
# .env  (never commit this file)
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=newsdb
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

## django-cors-headers

```
pip install django-cors-headers
```

Browsers block cross-origin HTTP requests by default (CORS policy). Since the React frontend runs on `http://localhost:5173` and the Django API runs on `http://localhost:8000`, every API call would be rejected without this package.

`django-cors-headers` injects the appropriate `Access-Control-Allow-*` headers into Django's responses.

```python
# settings.py
INSTALLED_APPS = [
    ...
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be as high as possible
    "django.middleware.common.CommonMiddleware",
    ...
]

# Development: allow the Vite dev server
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

# Production: lock down to the actual domain
# CORS_ALLOWED_ORIGINS = ["https://yourdomain.com"]
```

---

## drf-spectacular

```
pip install drf-spectacular
```

Automatically generates an **OpenAPI 3.0 schema** from your DRF views, and serves interactive documentation via **Swagger UI** and **ReDoc** — no manual YAML/JSON writing required.

### Benefits beyond documentation

- **Frontend type generation** — feed the schema into tools like `openapi-typescript` or `orval` to auto-generate TypeScript types and API client hooks for React
- **Contract testing** — validate that your API matches the schema in CI
- **Team communication** — share the Swagger UI URL with frontend developers

```python
# settings.py
INSTALLED_APPS = [
    ...
    "drf_spectacular",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "News Insight Hub API",
    "VERSION": "1.0.0",
}
```

```python
# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
```

After running the server, visit `http://localhost:8000/api/docs/` to see the interactive API explorer.

---

## gunicorn

```
pip install gunicorn
```

Django's built-in development server (`manage.py runserver`) is **not safe for production** — it is single-threaded and not designed to handle real traffic.

**Gunicorn** (Green Unicorn) is a production-grade WSGI server that:

- Spawns multiple **worker processes** to handle concurrent requests
- Sits behind a reverse proxy (Nginx, Caddy, etc.)
- Is the industry standard for deploying Django applications

### Common startup command

```bash
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120
```

| Flag | Description |
|---|---|
| `--bind` | Address and port to listen on |
| `--workers` | Number of worker processes (rule of thumb: `2 × CPU cores + 1`) |
| `--timeout` | Kill workers that take longer than N seconds |

> In development, keep using `manage.py runserver`. Switch to gunicorn only in staging/production.
