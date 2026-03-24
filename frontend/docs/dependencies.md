# Frontend Dependencies

A detailed guide to every package installed for this React frontend.

---

## Overview

| Package | Category | Purpose |
|---|---|---|
| `react` | Framework | Core UI library |
| `react-dom` | Framework | Renders React into the browser DOM |
| `typescript` | Language | Static type checking for JavaScript |
| `vite` | Build | Dev server and bundler |
| `@vitejs/plugin-react` | Build | React support for Vite |
| `tailwindcss` | Styling | Utility-first CSS framework |
| `@tailwindcss/vite` | Styling | Tailwind integration for Vite |
| `eslint` | Quality | JavaScript/TypeScript linter |
| `typescript-eslint` | Quality | TypeScript support for ESLint |
| `eslint-plugin-react-hooks` | Quality | Enforces Rules of Hooks |
| `eslint-plugin-react-refresh` | Quality | HMR compatibility checks |

---

## React & React DOM

```
npm install react react-dom
```

**React** is the core UI library. It lets you build UIs out of reusable components and manages how the UI updates when data changes.

**React DOM** is the package that actually renders React components into the browser. `react` contains the core logic; `react-dom` handles the browser-specific rendering.

```tsx
// src/main.tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

> **StrictMode** runs extra checks during development (double-invoking renders and effects) to help catch bugs early. It has no effect in production builds.

---

## TypeScript

```
npm install -D typescript
```

TypeScript adds static types to JavaScript. The compiler (`tsc`) checks your code for type errors before it runs.

This project uses three config files:

| File | Purpose |
|---|---|
| `tsconfig.json` | Root config — references the others |
| `tsconfig.app.json` | Config for `src/` (targets ES2022, enables strict mode) |
| `tsconfig.node.json` | Config for build tool files like `vite.config.ts` |

Key settings in `tsconfig.app.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

- `strict: true` — enables a bundle of safety checks (null checks, implicit any, etc.)
- `react-jsx` — uses the modern JSX transform (no need to `import React` in every file)

---

## Vite & @vitejs/plugin-react

```
npm install -D vite @vitejs/plugin-react
```

**Vite** is the build tool and dev server. It serves files over native ES modules during development (near-instant startup) and bundles with Rollup for production.

**@vitejs/plugin-react** adds React support: JSX transformation and Fast Refresh (HMR that preserves component state on file save).

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

### Common npm scripts

| Script | Command | Description |
|---|---|---|
| `dev` | `vite` | Start dev server at `http://localhost:5173` |
| `build` | `tsc -b && vite build` | Type-check, then bundle for production |
| `preview` | `vite preview` | Preview the production build locally |
| `lint` | `eslint .` | Run the linter across all files |

---

## Tailwind CSS & @tailwindcss/vite

```
npm install -D tailwindcss @tailwindcss/vite
```

**Tailwind CSS** is a utility-first CSS framework. Instead of writing custom CSS, you apply pre-built utility classes directly in JSX.

**@tailwindcss/vite** integrates Tailwind into the Vite build pipeline — no PostCSS config required.

```css
/* src/index.css */
@import "tailwindcss";
```

That single import is all that is needed. Tailwind scans your source files and generates only the CSS classes you actually use.

### Example usage in this project

```tsx
<div className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-6 border border-slate-200">
```

| Class | Effect |
|---|---|
| `bg-white` | White background |
| `rounded-xl` | Large border radius |
| `shadow-sm` | Subtle drop shadow |
| `hover:shadow-md` | Larger shadow on hover |
| `transition-shadow` | Animate the shadow change |
| `p-6` | 1.5rem padding on all sides |

---

## ESLint, typescript-eslint & plugins

```
npm install -D eslint typescript-eslint eslint-plugin-react-hooks eslint-plugin-react-refresh
```

**ESLint** statically analyzes your code to catch bugs and enforce code style.

**typescript-eslint** gives ESLint the ability to parse TypeScript and adds TypeScript-specific lint rules.

**eslint-plugin-react-hooks** enforces the [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks):
- Hooks must be called at the top level (not inside conditions or loops)
- Hooks must only be called from React functions

**eslint-plugin-react-refresh** warns when a file's exports are not compatible with Vite's Fast Refresh (HMR), which would cause a full page reload instead of a partial update.

```js
// eslint.config.js (flat config format)
export default tseslint.config(
  { ignores: ['dist'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },
)
```
