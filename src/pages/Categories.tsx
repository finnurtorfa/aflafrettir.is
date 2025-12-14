import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import type { Category } from '../types';
import './Categories.css';

const Categories: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    isActive: true,
  });
  const [apiUrl, setApiUrl] = useState('');
  const [isFetching, setIsFetching] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = () => {
    const saved = localStorage.getItem('categories');
    if (saved) {
      setCategories(JSON.parse(saved));
    } else {
      // Initialize with default categories
      const defaultCategories: Category[] = [
        { id: '1', name: 'Veiðifréttir', isActive: true, order: 1, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '2', name: 'Markaðsfréttir', isActive: true, order: 2, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '3', name: 'Útflutningur', isActive: true, order: 3, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '4', name: 'Vinnsla', isActive: true, order: 4, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '5', name: 'Sjávarútvegur', isActive: true, order: 5, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '6', name: 'Stjórnmál', isActive: true, order: 6, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '7', name: 'Umhverfi', isActive: true, order: 7, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '8', name: 'Tækni', isActive: true, order: 8, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
        { id: '9', name: 'Annað', isActive: true, order: 9, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
      ];
      setCategories(defaultCategories);
      localStorage.setItem('categories', JSON.stringify(defaultCategories));
    }
  };

  const saveCategories = (cats: Category[]) => {
    localStorage.setItem('categories', JSON.stringify(cats));
    setCategories(cats);
  };

  const handleCreate = () => {
    if (!formData.name.trim()) {
      setError('Nafn flokks er nauðsynlegt');
      return;
    }

    const newCategory: Category = {
      id: Date.now().toString(),
      name: formData.name.trim(),
      isActive: formData.isActive,
      order: categories.length + 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    const updated = [...categories, newCategory];
    saveCategories(updated);
    resetForm();
    setError('');
  };

  const handleUpdate = () => {
    if (!editingCategory || !formData.name.trim()) {
      setError('Nafn flokks er nauðsynlegt');
      return;
    }

    const updated = categories.map(cat =>
      cat.id === editingCategory.id
        ? { ...cat, name: formData.name.trim(), isActive: formData.isActive, updatedAt: new Date().toISOString() }
        : cat
    );

    saveCategories(updated);
    resetForm();
    setError('');
  };

  const handleDelete = (id: string) => {
    if (confirm('Ertu viss um að þú viljir eyða þessum flokki?')) {
      const updated = categories.filter(cat => cat.id !== id);
      saveCategories(updated);
    }
  };

  const handleEdit = (category: Category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      isActive: category.isActive,
    });
    setIsEditing(true);
  };

  const toggleActive = (id: string) => {
    const updated = categories.map(cat =>
      cat.id === id
        ? { ...cat, isActive: !cat.isActive, updatedAt: new Date().toISOString() }
        : cat
    );
    saveCategories(updated);
  };

  const moveUp = (index: number) => {
    if (index === 0) return;
    const updated = [...categories];
    [updated[index - 1], updated[index]] = [updated[index], updated[index - 1]];
    // Update order numbers
    updated.forEach((cat, idx) => {
      cat.order = idx + 1;
      cat.updatedAt = new Date().toISOString();
    });
    saveCategories(updated);
  };

  const moveDown = (index: number) => {
    if (index === categories.length - 1) return;
    const updated = [...categories];
    [updated[index], updated[index + 1]] = [updated[index + 1], updated[index]];
    // Update order numbers
    updated.forEach((cat, idx) => {
      cat.order = idx + 1;
      cat.updatedAt = new Date().toISOString();
    });
    saveCategories(updated);
  };

  const fetchFromApi = async () => {
    if (!apiUrl.trim()) {
      setError('Vinsamlegast sláðu inn API slóð');
      return;
    }

    setIsFetching(true);
    setError('');

    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP villa: ${response.status}`);
      }

      const data = await response.json();
      
      // Assuming API returns array of categories with at least a 'name' field
      // Adjust this based on your actual API response format
      let fetchedCategories: Category[];
      
      if (Array.isArray(data)) {
        fetchedCategories = data.map((item: any, index: number) => ({
          id: item.id?.toString() || Date.now().toString() + index,
          name: item.name || item.title || item.label || 'Ónefndur flokkur',
          isActive: item.isActive !== undefined ? item.isActive : true,
          order: item.order || index + 1,
          createdAt: item.createdAt || new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }));
      } else if (data.categories && Array.isArray(data.categories)) {
        // Handle nested response like { categories: [...] }
        fetchedCategories = data.categories.map((item: any, index: number) => ({
          id: item.id?.toString() || Date.now().toString() + index,
          name: item.name || item.title || item.label || 'Ónefndur flokkur',
          isActive: item.isActive !== undefined ? item.isActive : true,
          order: item.order || index + 1,
          createdAt: item.createdAt || new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        }));
      } else {
        throw new Error('Ógild svarsnið frá API');
      }

      if (fetchedCategories.length === 0) {
        setError('Engir flokkar fundust í API svari');
        return;
      }

      saveCategories(fetchedCategories);
      setApiUrl('');
      alert(`${fetchedCategories.length} flokkar sóttir frá API!`);
    } catch (err) {
      setError(`Villa við að sækja frá API: ${err instanceof Error ? err.message : 'Óþekkt villa'}`);
    } finally {
      setIsFetching(false);
    }
  };

  const resetForm = () => {
    setFormData({ name: '', isActive: true });
    setEditingCategory(null);
    setIsEditing(false);
  };

  const activeCategories = categories.filter(cat => cat.isActive);

  return (
    <Layout>
      <div className="categories-page">
        <div className="categories-header">
          <h1>Flokkar</h1>
          <div className="active-count">
            {activeCategories.length} virkir flokkar
          </div>
        </div>

        {/* API Fetch Section */}
        <div className="api-section">
          <h2>Sækja flokka frá API</h2>
          <div className="api-form">
            <input
              type="url"
              placeholder="https://api.example.com/categories"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              className="api-input"
            />
            <button
              onClick={fetchFromApi}
              disabled={isFetching}
              className="btn-primary"
            >
              {isFetching ? 'Sæki...' : 'Sækja frá API'}
            </button>
          </div>
          <p className="api-hint">
            API þarf að skila fylki af flokkum með <code>name</code> eða <code>title</code> svæði
          </p>
        </div>

        {/* Create/Edit Form */}
        <div className="category-form">
          <h2>{isEditing ? 'Breyta flokki' : 'Nýr flokkur'}</h2>
          {error && <div className="error-message">{error}</div>}
          <div className="form-row">
            <input
              type="text"
              placeholder="Nafn flokks"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="form-input"
            />
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={formData.isActive}
                onChange={(e) => setFormData({ ...formData, isActive: e.target.checked })}
              />
              Virkur í valmynd
            </label>
          </div>
          <div className="form-actions">
            {isEditing ? (
              <>
                <button onClick={handleUpdate} className="btn-primary">
                  Uppfæra
                </button>
                <button onClick={resetForm} className="btn-secondary">
                  Hætta við
                </button>
              </>
            ) : (
              <button onClick={handleCreate} className="btn-primary">
                Stofna flokk
              </button>
            )}
          </div>
        </div>

        {/* Categories List */}
        <div className="categories-list">
          <h2>Allir flokkar</h2>
          {categories.length === 0 ? (
            <p className="empty-state">Engir flokkar ennþá</p>
          ) : (
            <div className="category-table">
              <div className="table-header">
                <div className="col-order">Röð</div>
                <div className="col-name">Nafn</div>
                <div className="col-status">Staða</div>
                <div className="col-updated">Síðast uppfært</div>
                <div className="col-actions">Aðgerðir</div>
              </div>
              {categories.map((category, index) => (
                <div key={category.id} className={`table-row ${!category.isActive ? 'inactive' : ''}`}>
                  <div className="col-order">
                    <div className="order-controls">
                      <button
                        onClick={() => moveUp(index)}
                        disabled={index === 0}
                        className="order-btn"
                        title="Færa upp"
                      >
                        ▲
                      </button>
                      <span className="order-number">{index + 1}</span>
                      <button
                        onClick={() => moveDown(index)}
                        disabled={index === categories.length - 1}
                        className="order-btn"
                        title="Færa niður"
                      >
                        ▼
                      </button>
                    </div>
                  </div>
                  <div className="col-name">
                    <strong>{category.name}</strong>
                  </div>
                  <div className="col-status">
                    <button
                      onClick={() => toggleActive(category.id)}
                      className={`status-badge ${category.isActive ? 'active' : 'inactive-badge'}`}
                    >
                      {category.isActive ? '✓ Virkur' : '✗ Óvirkur'}
                    </button>
                  </div>
                  <div className="col-updated">
                    {new Date(category.updatedAt).toLocaleDateString('is-IS', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </div>
                  <div className="col-actions">
                    <button
                      onClick={() => handleEdit(category)}
                      className="btn-edit"
                    >
                      Breyta
                    </button>
                    <button
                      onClick={() => handleDelete(category.id)}
                      className="btn-delete"
                    >
                      Eyða
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Active Categories Preview */}
        <div className="active-preview">
          <h2>Virkir flokkar í valmynd</h2>
          <p className="preview-description">
            Þessir flokkar birtast í fellivalmyndinni þegar ný frétt er búin til:
          </p>
          {activeCategories.length === 0 ? (
            <p className="empty-state">Engir virkir flokkar</p>
          ) : (
            <div className="preview-list">
              {activeCategories.map((category, index) => (
                <div key={category.id} className="preview-item">
                  <span className="preview-number">{index + 1}.</span>
                  <span className="preview-name">{category.name}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Categories;
