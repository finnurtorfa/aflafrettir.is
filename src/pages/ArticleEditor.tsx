import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import type { Descendant } from 'slate';
import Layout from '../components/Layout';
import { EnhancedEditor as PlateEditor } from '../components/PlateEditor';
import type { NewsArticle, Category } from '../types';
import { useAuth } from '../context/AuthContext';
import './ArticleEditor.css';

const ArticleEditor: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [title, setTitle] = useState('');
  const [name, setName] = useState('');
  const [publishDate, setPublishDate] = useState(new Date().toISOString().slice(0, 16));
  const [category, setCategory] = useState('');
  const [categories, setCategories] = useState<Category[]>([]);
  const [published, setPublished] = useState(false);
  const [editorValue, setEditorValue] = useState<Descendant[]>([
    {
      type: 'paragraph',
      children: [{ text: '' }],
    } as any,
  ]);

  useEffect(() => {
    // Load categories from localStorage
    const savedCategories = JSON.parse(localStorage.getItem('categories') || '[]') as Category[];
    const activeCategories = savedCategories.filter(cat => cat.isActive);
    setCategories(activeCategories);
    
    // Set default category if we have categories
    if (activeCategories.length > 0 && !category) {
      setCategory(activeCategories[0].name);
    }

    if (id) {
      const articles = JSON.parse(localStorage.getItem('articles') || '[]');
      const article = articles.find((a: NewsArticle) => a.id === id);
      if (article) {
        setTitle(article.title);
        setName(article.name || article.title);
        setPublishDate(article.publishDate || article.createdAt);
        setCategory(article.category || (activeCategories.length > 0 ? activeCategories[0].name : ''));
        try {
          const parsedContent = JSON.parse(article.content);
          setEditorValue(parsedContent);
        } catch {
          // If content is not JSON (legacy HTML), create a simple text node
          setEditorValue([
            {
              type: 'paragraph',
              children: [{ text: article.content }],
            } as any,
          ]);
        }
        setPublished(article.published);
      }
    }
  }, [id]);

  const handleSave = () => {
    const content = JSON.stringify(editorValue);
    const articles = JSON.parse(localStorage.getItem('articles') || '[]');
    
    if (id) {
      const index = articles.findIndex((a: NewsArticle) => a.id === id);
      if (index !== -1) {
        articles[index] = {
          ...articles[index],
          title,
          name,
          content,
          publishDate,
          category,
          published,
          updatedAt: new Date().toISOString(),
        };
      }
    } else {
      const newArticle: NewsArticle = {
        id: Date.now().toString(),
        title,
        name,
        content,
        author: user?.name || 'Admin',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        publishDate,
        category,
        published,
      };
      articles.push(newArticle);
    }
    
    localStorage.setItem('articles', JSON.stringify(articles));
    navigate('/articles');
  };

  return (
    <Layout>
      <div className="editor-page">
        <div className="editor-header">
          <h1>{id ? 'Breyta frétt' : 'Ný frétt'}</h1>
          <div className="editor-actions">
            <button onClick={() => navigate('/articles')} className="btn-secondary">Hætta við</button>
            <button onClick={handleSave} className="btn-primary">Vista</button>
          </div>
        </div>
        <div className="editor-form">
          <div className="form-group">
            <label htmlFor="title">Titill</label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Sláðu inn titil fréttarinnar..."
            />
          </div>
          <div className="article-metadata">
            <div className="form-group">
              <label htmlFor="name">Nafn fréttarinnar</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Nafn til birtingar..."
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="publishDate">Birtingartími</label>
              <input
                type="datetime-local"
                id="publishDate"
                value={publishDate}
                onChange={(e) => setPublishDate(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="category">Flokkur</label>
              <select
                id="category"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                {categories.length === 0 ? (
                  <option value="">Engir flokkar í boði</option>
                ) : (
                  categories.map((cat) => (
                    <option key={cat.id} value={cat.name}>
                      {cat.name}
                    </option>
                  ))
                )}
              </select>
            </div>
          </div>
          <div className="form-group">
            <label>Efni</label>
            <PlateEditor value={editorValue} onChange={setEditorValue} />
          </div>
          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={published}
                onChange={(e) => setPublished(e.target.checked)}
              />
              Birta strax
            </label>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ArticleEditor;
