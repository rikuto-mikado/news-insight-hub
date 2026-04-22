# Category Setup

## Overview

Categories are fetched from the [NewsAPI](https://newsapi.org/) `top-headlines` endpoint, which supports the following categories:

`technology` / `business` / `sports` / `entertainment` / `health` / `science`

---

## How it works

### 1. Fetch command — `fetch_news.py`

Accepts an optional `--category` argument.

- If provided, appends `&category={category}` to the NewsAPI request URL.
- Saves the category value to the `NewsArticle.category` field in the DB.
- If omitted, fetches general top headlines with no category.

```bash
# Fetch with category
python manage.py fetch_news --category technology

# Fetch without category (general)
python manage.py fetch_news
```

### 2. Celery task — `tasks.py`

`fetch_news_task` runs all categories automatically every hour (configured in `settings.py`).

```python
CATEGORIES = ["technology", "business", "sports", "entertainment", "health", "science"]

@shared_task
def fetch_news_task():
    call_command("fetch_news")           # general
    for category in CATEGORIES:
        call_command("fetch_news", category=category)
```

### 3. Frontend — `App.tsx`

Select box options must match exactly the category strings stored in the DB.

```tsx
<option value="technology">Technology</option>
<option value="business">Business</option>
...
```

---

## Adding a new category

1. Add the category string to `CATEGORIES` in `tasks.py`.
2. Add a corresponding `<option>` in `App.tsx`.
3. Manually run `python manage.py fetch_news --category <new_category>` once to populate the DB immediately.

---

## Notes

- Duplicate articles are prevented by the unique constraint on `NewsArticle.url`.
- Once an article is saved, its category is not updated even if re-fetched.

---

### Note in japanese

`python manage.py fetch_news --category technology` のようにカテゴリを指定して叩くと、NewsAPIに`&category=technology`付きでリクエストを送り、返ってきた記事をすべて`category="technology"`としてDBに保存する。カテゴリなしで叩いた場合は`category=""`（空）で保存される。

### 自動化（Celery）

`@shared_task`はCeleryに「このタスクを定期実行してね」と登録するデコレータ。`settings.py`の`CELERY_BEAT_SCHEDULE`で「1時間ごとに`fetch_news_task`を実行」と設定しているので、celery-beatが1時間ごとに自動で全カテゴリ分の`fetch_news`コマンドを叩いてDBを更新し続ける。検索をしているわけではなく、あくまでデータ収集の定期実行の仕組み。

### フロントへの反映

DBにカテゴリ付きで記事が入ったあとは、フロントのセレクトボックスで選んだカテゴリを`?category=technology`というクエリパラメータとしてバックエンドに送るだけ。バックエンドの`DjangoFilterBackend`がそのパラメータでDBをフィルタリングして記事一覧を返し、フロントに表示される。

```
Celery Beat（1時間ごと）
  → fetch_news（カテゴリ別）
  → NewsAPI からデータ取得
  → DB に保存

フロント操作
  → ?category=technology をバックエンドに送信
  → DB からフィルタして返す
  → 表示
```
