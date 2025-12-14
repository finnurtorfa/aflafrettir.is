import React from 'react';
import type { ReactNode } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Layout.css';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="navbar-brand">
          <Link to="/dashboard">Aflafréttir Stjórnborð</Link>
        </div>
        <div className="navbar-menu">
          <Link to="/dashboard">Yfirlit</Link>
          <Link to="/articles">Fréttir</Link>
          <Link to="/categories">Flokkar</Link>
          <Link to="/ads">Auglýsingar</Link>
          <Link to="/reports">Skýrslur</Link>
        </div>
        <div className="navbar-user">
          <span>{user?.name}</span>
          <button onClick={handleLogout} className="btn-logout">Útskrá</button>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
