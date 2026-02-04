import React from 'react';
import type { ReactNode } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

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
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography
            variant="h6"
            component={Link}
            to="/dashboard"
            sx={{
              flexGrow: 0,
              textDecoration: 'none',
              color: 'inherit',
              marginRight: 4,
              fontWeight: 'bold',
            }}
          >
            Aflafréttir Stjórnborð
          </Typography>
          <Box sx={{ flexGrow: 1, display: 'flex', gap: 3 }}>
            <Button color="inherit" component={Link} to="/dashboard">
              Yfirlit
            </Button>
            <Button color="inherit" component={Link} to="/articles">
              Fréttir
            </Button>
            <Button color="inherit" component={Link} to="/categories">
              Flokkar
            </Button>
            <Button color="inherit" component={Link} to="/ads">
              Auglýsingar
            </Button>
            <Button color="inherit" component={Link} to="/reports">
              Skýrslur
            </Button>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="body1">{user?.name}</Typography>
            <Button
              variant="outlined"
              color="inherit"
              onClick={handleLogout}
              sx={{
                borderColor: 'white',
                '&:hover': {
                  borderColor: 'white',
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                },
              }}
            >
              Útskrá
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: 'background.default',
          width: '100%',
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
