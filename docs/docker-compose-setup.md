# Docker Compose Setup Guide

Template for Django (Celery) + React (Vite) + PostgreSQL + Redis.

## Project Structure

```
project/
├── backend/      # Django
│   └── Dockerfile
├── frontend/     # React + Vite
│   └── Dockerfile
├── docker-compose.yml
└── .env
```

## Services

| Service      | Image/Build     | Port | Role                     |
|-------------|----------------|------|--------------------------|
| db          | postgres       | 5432 | PostgreSQL               |
| backend     | ./backend      | 8000 | Django + Gunicorn        |
| redis       | redis:alpine   | 6379 | Celery broker            |
| celery      | ./backend      | -    | Celery worker            |
| celery-beat | ./backend      | -    | Periodic task scheduler  |
| frontend    | ./frontend     | 5173 | Vite dev server          |

## .env

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
DATABASE_URL=postgres://your_user:your_password@db:5432/your_db
```

The host in `DATABASE_URL` is the service name `db` (resolved via Docker's internal network).

## docker-compose.yml

```yaml
services:
  db:
    image: postgres:<version>
    volumes:
      - db_data:/var/lib/postgresql/data
    env_file:
      - .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    command: sh -c "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      DATABASE_URL: ${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy  # wait until DB is ready

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  celery:
    build: ./backend
    command: sh -c "celery -A config worker -l info"
    volumes:
      - ./backend:/app
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery-beat:
    build: ./backend
    command: sh -c "celery -A config beat -l info"
    volumes:
      - ./backend:/app
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    volumes:
      - ./frontend:/app
      - /app/node_modules  # prevent host node_modules from overwriting container's
    ports:
      - "5173:5173"

volumes:
  db_data:
```

## Dockerfiles

### backend (Python)

```dockerfile
FROM python:<version>-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
```

### frontend (Node)

```dockerfile
FROM node:<version>-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173
```

## Common Commands

```bash
# First run or after Dockerfile changes
docker compose up -d --build

# Start without rebuilding
docker compose up -d

# Follow logs
docker compose logs -f backend
docker compose logs -f celery

# Open a shell inside a container
docker compose exec backend bash
docker compose exec db psql -U your_user -d your_db

# Stop all services
docker compose down

# Stop and remove volumes (full reset including DB data)
docker compose down -v
```

## Notes & Gotchas

### Ensure startup order with healthchecks
`depends_on` alone only guarantees container start order, not readiness. Without healthchecks, the backend may try to connect before PostgreSQL or Redis is actually ready.
Use `condition: service_healthy` so dependent services wait until the healthcheck passes.

### Protect node_modules with an anonymous volume
```yaml
volumes:
  - ./frontend:/app
  - /app/node_modules  # without this, the host's node_modules would overwrite the container's
```
The host (Mac) and container (Linux) have incompatible binaries, so the container's `node_modules` must be isolated.

### Use the service name as the database host
In local development, use the Docker service name (`db`) instead of `localhost`.
```
DATABASE_URL=postgres://user:password@db:5432/dbname
                                       ^^
                                       service name, not localhost
```

### Vite requires `--host` to be accessible from the host machine
By default, Vite inside a container only listens on `localhost`.
Adding `--host` binds it to `0.0.0.0`, making it reachable from outside the container.
