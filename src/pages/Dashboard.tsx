import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

const Dashboard: React.FC = () => {
  const cards = [
    {
      to: '/articles',
      icon: '📰',
      title: 'Fréttir',
      description: 'Búa til, skoða, breyta og eyða fréttum',
    },
    {
      to: '/ads',
      icon: '📢',
      title: 'Auglýsingar',
      description: 'Stjórna auglýsingum á vefsíðu',
    },
    {
      to: '/reports',
      icon: '📊',
      title: 'Afla skýrslur',
      description: 'Skoða skýrslur um fiskveiðiiðnaðinn á Íslandi',
    },
  ];

  return (
    <Layout>
      <Container maxWidth="xl" sx={{ py: 4, width: '100%' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Stjórnborð
        </Typography>
        <Grid container spacing={3}>
          {cards.map((card) => (
            <Grid size={{ xs: 12, md: 6, lg: 4 }} key={card.to}>
              <Card
                component={Link}
                to={card.to}
                sx={{
                  textDecoration: 'none',
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4,
                  },
                }}
              >
                <CardContent>
                  <Typography variant="h4" component="h2" gutterBottom color="primary">
                    {card.icon} {card.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {card.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Layout>
  );
};

export default Dashboard;
