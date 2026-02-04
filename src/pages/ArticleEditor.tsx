import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import type { Descendant } from 'slate';
import Layout from '../components/Layout';
import { EnhancedEditor as PlateEditor } from '../components/PlateEditor';
import type { NewsArticle, Category } from '../types';
import { useAuth } from '../context/AuthContext';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';

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
    const savedCategories = JSON.parse(localStorage.getItem('categories') || '[]') as Category[];
    const activeCategories = savedCategories.filter(cat => cat.isActive);
    setCategories(activeCategories);
    
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
      <Container maxWidth="xl" sx={{ py: 4, width: '100%' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h3" component="h1">
            {id ? 'Breyta frétt' : 'Ný frétt'}
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={() => navigate('/articles')}
              startIcon={<CancelIcon />}
            >
              Hætta við
            </Button>
            <Button
              variant="contained"
              onClick={handleSave}
              startIcon={<SaveIcon />}
            >
              Vista
            </Button>
          </Box>
        </Box>
        <Paper sx={{ p: 3 }}>
          <Box sx={{ mb: 3 }}>
            <TextField
              fullWidth
              label="Titill"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Sláðu inn titil fréttarinnar..."
              variant="outlined"
            />
          </Box>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField
                fullWidth
                label="Nafn fréttarinnar"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Nafn til birtingar..."
                required
              />
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <TextField
                fullWidth
                label="Birtingartími"
                type="datetime-local"
                value={publishDate}
                onChange={(e) => setPublishDate(e.target.value)}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <FormControl fullWidth>
                <InputLabel>Flokkur</InputLabel>
                <Select
                  value={category}
                  label="Flokkur"
                  onChange={(e) => setCategory(e.target.value)}
                >
                  {categories.length === 0 ? (
                    <MenuItem value="">Engir flokkar í boði</MenuItem>
                  ) : (
                    categories.map((cat) => (
                      <MenuItem key={cat.id} value={cat.name}>
                        {cat.name}
                      </MenuItem>
                    ))
                  )}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Efni
            </Typography>
            <PlateEditor value={editorValue} onChange={setEditorValue} />
          </Box>
          <FormControlLabel
            control={
              <Checkbox
                checked={published}
                onChange={(e) => setPublished(e.target.checked)}
              />
            }
            label="Birta strax"
          />
        </Paper>
      </Container>
    </Layout>
  );
};

export default ArticleEditor;
