# Debugging Notes

## 1. Category filter not working

**Problem:** Selecting a category in the frontend returned no results.

**Root cause:** `fetch_news` command accepted `--category` argument but never passed it to the NewsAPI URL or saved it to the DB.

**Fix:** Updated `fetch_news.py` to append `&category={category}` to the API request URL and include `category` in `get_or_create` defaults.

---

## 2. `StringDataRightTruncation` error on article save

**Problem:** `fetch_news --category health/science` crashed with `value too long for type character varying(200)`.

**Root cause:** `URLField` defaults to `max_length=200`, but some NewsAPI article URLs exceed that length.

**Fix:** Set `max_length=500` on the `url` field in `NewsArticle` model and generated a new migration (`0003_alter_newsarticle_url.py`).

---

## 3. `django_filters` not registered

**Problem:** Category filtering via `?category=` query param had no effect.

**Root cause:** `django_filters` was used in `views.py` but not added to `INSTALLED_APPS` in `settings.py`.

**Fix:** Added `"django_filters"` to `INSTALLED_APPS`.

---

## 4. No category data in DB on first run

**Problem:** All articles had an empty `category` field after initial setup.

**Root cause:** Celery beat runs every hour, so no data was fetched yet at startup.

**Fix:** Manually ran `fetch_news --category <category>` for each category to populate the DB immediately.
