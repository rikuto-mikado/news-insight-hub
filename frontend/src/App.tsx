import { useEffect, useState } from 'react';

interface Article {
  id: number;
  title: string;
  content: string;
  url: string;
  source_name: string;
  published_date: string;
}

function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [query, setQuery] = useState(''); 

  useEffect(() => {
    fetch(`http://localhost:8000/api/articles/?search=${query}`)
    .then(res => res.json())
    .then(data => setArticles(data))
    .catch(err => console.error("Error fetching data:", err));
  }, [query]);

  return(
    <>
      <div className="min-h-screen bg-gray-100 p-8">
        <header className="mb-12">
          <h1 className="text-4xl font-bold text-state-900">News DashBoard</h1>
        </header>

        <input
          type="text"
          placeholder="Search articles..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          className="w-full max-w-md px-4 py-2 border border-slate-500 rounded-lg mb-8"
        />

        <div className="grid grid-col-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map(article => (
            <div key={article.id} className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-6 border border-slate-200">
              <h2 className="text-xs font-semibold text-orange-500 uppercase tracking-wider">
                {article.source_name}
              </h2>
              <h3 className="text-base font-semibold text-slate-800 mb-2">{article.title}</h3>
              <p className="text-state-600 text-sm mb-4 line-clamp-3">
                {article.content}
              </p>
              <div className="flex justify-between items-center mt-auto">
                <span className="text-xs text-slate-400">
                  {new Date(article.published_date).toLocaleDateString()}
                </span>
                <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm font-medium text-orange-600 hover:text-orange-600">
                  Read More
                </a>
            </div>
          </div>
          ))}
        </div>
      </div>
    </>
  )
}

export default App