import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import type { Ad } from '../types';
import './Ads.css';

const Ads: React.FC = () => {
  const [ads, setAds] = useState<Ad[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingAd, setEditingAd] = useState<Ad | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [formData, setFormData] = useState({
    title: '',
    imageUrl: '',
    linkUrl: '',
    position: 'sidebar',
    active: true,
  });

  useEffect(() => {
    const saved = localStorage.getItem('ads');
    if (saved) {
      setAds(JSON.parse(saved));
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    let updated;
    if (editingAd) {
      updated = ads.map(ad => ad.id === editingAd.id 
        ? { ...formData, id: editingAd.id } 
        : ad
      );
    } else {
      const newAd: Ad = {
        ...formData,
        id: Date.now().toString(),
      };
      updated = [...ads, newAd];
    }
    
    setAds(updated);
    localStorage.setItem('ads', JSON.stringify(updated));
    resetForm();
  };

  const deleteAd = (id: string) => {
    if (confirm('Ertu viss um að þú viljir eyða þessari auglýsingu?')) {
      const updated = ads.filter(a => a.id !== id);
      setAds(updated);
      localStorage.setItem('ads', JSON.stringify(updated));
    }
  };

  const editAd = (ad: Ad) => {
    setEditingAd(ad);
    setFormData({
      title: ad.title,
      imageUrl: ad.imageUrl,
      linkUrl: ad.linkUrl,
      position: ad.position,
      active: ad.active,
    });
    setImagePreview(ad.imageUrl);
    setShowForm(true);
  };

  const resetForm = () => {
    setShowForm(false);
    setEditingAd(null);
    setImagePreview('');
    setFormData({
      title: '',
      imageUrl: '',
      linkUrl: '',
      position: 'sidebar',
      active: true,
    });
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const dataUrl = e.target?.result as string;
        setFormData({...formData, imageUrl: dataUrl});
        setImagePreview(dataUrl);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <Layout>
      <div className="ads-page">
        <div className="ads-header">
          <h1>Auglýsingar</h1>
          <button onClick={() => setShowForm(true)} className="btn-primary">+ Ný auglýsing</button>
        </div>

        {showForm && (
          <div className="ad-form-container">
            <form onSubmit={handleSubmit} className="ad-form">
              <h2>{editingAd ? 'Breyta auglýsingu' : 'Ný auglýsing'}</h2>
              <div className="form-group">
                <label>Titill</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Mynd</label>
                <div className="image-upload-group">
                  <div className="upload-buttons">
                    <button 
                      type="button"
                      onClick={() => document.getElementById('ad-image-upload')?.click()}
                      className="btn-secondary"
                    >
                      📤 Hlaða upp mynd
                    </button>
                    <span className="upload-or">eða</span>
                    <input
                      type="url"
                      placeholder="Sláðu inn vefslóð myndar"
                      value={formData.imageUrl}
                      onChange={(e) => {
                        setFormData({...formData, imageUrl: e.target.value});
                        setImagePreview(e.target.value);
                      }}
                    />
                  </div>
                  <input
                    id="ad-image-upload"
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    style={{ display: 'none' }}
                  />
                  {imagePreview && (
                    <div className="image-preview">
                      <img src={imagePreview} alt="Preview" />
                    </div>
                  )}
                </div>
              </div>
              <div className="form-group">
                <label>Vefslóð tengils (þar sem notendur fara þegar þeir smella á auglýsinguna)</label>
                <input
                  type="url"
                  placeholder="https://example.com"
                  value={formData.linkUrl}
                  onChange={(e) => setFormData({...formData, linkUrl: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Staðsetning</label>
                <select value={formData.position} onChange={(e) => setFormData({...formData, position: e.target.value})}>
                  <option value="sidebar">Hliðarslá</option>
                  <option value="header">Haus</option>
                  <option value="footer">Fótur</option>
                </select>
              </div>
              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={formData.active}
                    onChange={(e) => setFormData({...formData, active: e.target.checked})}
                  />
                  Virk
                </label>
              </div>
              <div className="form-actions">
                <button type="button" onClick={resetForm} className="btn-secondary">Hætta við</button>
                <button type="submit" className="btn-primary">Vista</button>
              </div>
            </form>
          </div>
        )}

        <div className="ads-grid">
          {ads.map(ad => (
            <div key={ad.id} className="ad-card">
              <a href={ad.linkUrl} target="_blank" rel="noopener noreferrer" className="ad-image-link">
                <img src={ad.imageUrl} alt={ad.title} />
              </a>
              <div className="ad-info">
                <h3>{ad.title}</h3>
                <p><strong>Tengill:</strong> <a href={ad.linkUrl} target="_blank" rel="noopener noreferrer">{ad.linkUrl}</a></p>
                <p><strong>Staðsetning:</strong> {ad.position}</p>
                <p>{ad.active ? '✅ Virk' : '❌ Óvirk'}</p>
              </div>
              <div className="ad-actions">
                <button onClick={() => editAd(ad)} className="btn-secondary">Breyta</button>
                <button onClick={() => deleteAd(ad.id)} className="btn-danger">Eyða</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
};

export default Ads;
