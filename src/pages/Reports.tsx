import React, { useState } from 'react';
import axios from 'axios';
import Layout from '../components/Layout';
import type { FishingReport } from '../types';
import './Reports.css';

const Reports: React.FC = () => {
  const [reports, setReports] = useState<FishingReport[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchReports = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Example API call - replace with actual Icelandic fishing industry API
      const response = await axios.get('https://api.example.com/fishing-reports');
      setReports(response.data);
    } catch (err) {
      // For demo purposes, using mock data
      setError('Nota prufugögn (skipta út fyrir raunverulegt API)');
      const mockData: FishingReport[] = [
        { species: 'Þorskur', quantity: 1250, date: '2025-12-10', location: 'Reykjavík' },
        { species: 'Ýsa', quantity: 850, date: '2025-12-10', location: 'Akureyri' },
        { species: 'Síld', quantity: 2300, date: '2025-12-09', location: 'Ísafjörður' },
        { species: 'Makríll', quantity: 1100, date: '2025-12-09', location: 'Vestmannaeyjar' },
      ];
      setReports(mockData);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="reports-page">
        <div className="reports-header">
          <h1>Afla skýrslur</h1>
          <button onClick={fetchReports} className="btn-primary" disabled={loading}>
            {loading ? 'Hleð...' : 'Sækja skýrslur'}
          </button>
        </div>

        {error && <div className="info-message">{error}</div>}

        {reports.length > 0 && (
          <div className="reports-container">
            <table className="reports-table">
              <thead>
                <tr>
                  <th>Tegund</th>
                  <th>Magn (tonn)</th>
                  <th>Dagsetning</th>
                  <th>Staðsetning</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((report, index) => (
                  <tr key={index}>
                    <td>{report.species}</td>
                    <td>{report.quantity.toLocaleString('is-IS')}</td>
                    <td>{new Date(report.date).toLocaleDateString('is-IS')}</td>
                    <td>{report.location}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            
            <div className="reports-summary">
              <h3>Samantekt</h3>
              <p>Heildarafli: {reports.reduce((sum, r) => sum + r.quantity, 0).toLocaleString('is-IS')} tonn</p>
              <p>Tegundir: {new Set(reports.map(r => r.species)).size}</p>
            </div>
          </div>
        )}

        {reports.length === 0 && !loading && (
          <div className="empty-state">
            <p>Engar skýrslur tiltækar. Smelltu á "Sækja skýrslur" til að hlaða gögnum.</p>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Reports;
