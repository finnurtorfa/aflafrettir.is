import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout';
import type { NewsArticle } from '../types';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';

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
      <Container maxWidth="xl" sx={{ py: 4, width: '100%' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h3" component="h1">
            Fréttir
          </Typography>
          <Button
            variant="contained"
            component={Link}
            to="/articles/new"
            startIcon={<AddIcon />}
            size="large"
          >
            Ný frétt
          </Button>
        </Box>
        <Stack spacing={2}>
          {articles.length === 0 ? (
            <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', py: 6 }}>
              Engar fréttir ennþá. Búðu til þína fyrstu frétt!
            </Typography>
          ) : (
            articles.map(article => (
              <Card key={article.id}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="h5" component="h3" gutterBottom>
                        {article.name || article.title}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                        <Chip 
                          label={article.category || 'Annað'} 
                          color="primary" 
                          size="small" 
                        />
                        <Typography variant="body2" color="text.secondary">
                          Eftir {article.author}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          • Birtist: {new Date(article.publishDate || article.createdAt).toLocaleString('is-IS', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </Typography>
                        <Chip 
                          label={article.published ? 'Birt' : 'Drög'}
                          color={article.published ? 'success' : 'default'}
                          size="small"
                        />
                      </Box>
                    </Box>
                    <CardActions>
                      <Button
                        component={Link}
                        to={`/articles/edit/${article.id}`}
                        variant="outlined"
                        color="secondary"
                        startIcon={<EditIcon />}
                      >
                        Breyta
                      </Button>
                      <Button
                        onClick={() => deleteArticle(article.id)}
                        variant="outlined"
                        color="error"
                        startIcon={<DeleteIcon />}
                      >
                        Eyða
                      </Button>
                    </CardActions>
                  </Box>
                </CardContent>
              </Card>
            ))
          )}
        </Stack>
      </Container>
    </Layout>
  );
};

export default Articles;
