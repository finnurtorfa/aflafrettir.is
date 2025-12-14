import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  return (
    <Layout>
      <div className="dashboard">
        <h1>Stjórnborð</h1>
        <div className="dashboard-grid">
          <Link to="/articles" className="dashboard-card">
            <h2>📰 Fréttir</h2>
            <p>Búa til, skoða, breyta og eyða fréttum</p>
          </Link>
          <Link to="/ads" className="dashboard-card">
            <h2>📢 Auglýsingar</h2>
            <p>Stjórna auglýsingum á vefsíðu</p>
          </Link>
          <Link to="/reports" className="dashboard-card">
            <h2>📊 Afla skýrslur</h2>
            <p>Skoða skýrslur um fiskveiðiiðnaðinn á Íslandi</p>
          </Link>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
