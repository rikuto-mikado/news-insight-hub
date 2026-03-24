# Frontend Coding Notes

## TypeScript Interface vs Type

- `interface` — defines the shape of an object. Can be extended with `extends`. Commonly used for props and API response types in React.
- `type` — more general purpose. Better suited for union types and primitive aliases.

```ts
// usage in this project
interface Article {
  id: number;
  title: string;
  content: string;
  url: string;
  source_name: string;
  published_date: string;
}
```

Using `interface` for object shapes is the common React convention.

---

## useState

A Hook that adds state (data that changes over time) to a component.

```tsx
const [articles, setArticles] = useState<Article[]>([]);
const [query, setQuery] = useState('');
```

- First value: the current state
- Second value: the setter function — calling it triggers a re-render
- `useState<Article[]>([])` — TypeScript generic explicitly sets the type; `[]` is the initial value

---

## useEffect

A Hook for side effects (API fetches, timers, etc.) — anything that should run separately from rendering.

```tsx
useEffect(() => {
  fetch(`http://localhost:8000/api/articles/?search=${query}`)
    .then(res => res.json())
    .then(data => setArticles(data))
    .catch(err => console.error("Error fetching data:", err));
}, [query]);
```

- The second argument is the **dependency array** — the effect re-runs whenever a listed value changes
- `[query]` — re-fetches from the API every time `query` changes
- `[]` — runs only once on mount
- No array — runs after every render (almost never what you want)

---

## Fetch API

The browser's built-in HTTP client. No external library needed to communicate with an API.

```tsx
fetch(`http://localhost:8000/api/articles/?search=${query}`)
  .then(res => res.json())   // parse the response body as JSON
  .then(data => setArticles(data))
  .catch(err => console.error("Error fetching data:", err));
```

- `fetch()` returns a Promise
- `.then(res => res.json())` — converts the response body into a JavaScript object
- `.catch()` — handles network errors

---

## JSX: `className` vs `class`

JSX is a JavaScript extension, so `class` conflicts with the JavaScript reserved word. The HTML `class` attribute is written as `className` in JSX.

```tsx
// HTML
<div class="bg-white p-6">

// JSX
<div className="bg-white p-6">
```

---

## `key` prop

When rendering a list, each element must have a unique `key`. React uses it to track which DOM elements changed.

```tsx
{articles.map(article => (
  <div key={article.id}>
    ...
  </div>
))}
```

- `key` only needs to be unique within the list, not globally
- Using a database ID is more stable than using the array index

---

## `target="_blank"` and `rel="noopener noreferrer"`

When opening an external link in a new tab, always include the `rel` attribute for security.

```tsx
<a
  href={article.url}
  target="_blank"
  rel="noopener noreferrer"
>
  Read More
</a>
```

- `noopener` — prevents the opened page from accessing the original page via `window.opener`
- `noreferrer` — does not send referrer information (also implies `noopener`)

---

## `new Date().toLocaleDateString()`

Converts an ISO date string (e.g. `"2024-01-15T00:00:00Z"`) into a locale-formatted display string.

```tsx
{new Date(article.published_date).toLocaleDateString()}
// renders as "1/15/2024" in an English locale browser
```
