import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import type { NewsArticle } from '../types';
import './Articles.css';

const Articles: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem('articles');
    if (saved) {
      setArticles(JSON.parse(saved));
    }
  }, []);

  const deleteArticle = (id: string) => {
    if (confirm('Ertu viss um að þú viljir eyða þessari frétt?')) {
      const updated = articles.filter(a => a.id !== id);
      setArticles(updated);
      localStorage.setItem('articles', JSON.stringify(updated));
    }
  };

  return (
    <Layout>
      <div className="articles-page">
        <div className="articles-header">
          <h1>Fréttir</h1>
          <Link to="/articles/new" className="btn-primary">+ Ný frétt</Link>
        </div>
        <div className="articles-list">
          {articles.length === 0 ? (
            <p className="empty-state">Engar fréttir ennþá. Búðu til þína fyrstu frétt!</p>
          ) : (
            articles.map(article => (
              <div key={article.id} className="article-card">
                <div className="article-info">
                  <h3>{article.name || article.title}</h3>
                  <p className="article-meta">
                    <span className="category-badge">{article.category || 'Annað'}</span>
                    Eftir {article.author} • Birtist: {new Date(article.publishDate || article.createdAt).toLocaleString('is-IS', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                    {article.published ? <span className="badge published">Birt</span> : <span className="badge draft">Drög</span>}
                  </p>
                </div>
                <div className="article-actions">
                  <Link to={`/articles/edit/${article.id}`} className="btn-secondary">Breyta</Link>
                  <button onClick={() => deleteArticle(article.id)} className="btn-danger">Eyða</button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Articles;
