import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import type { Category } from '../types';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import Alert from '@mui/material/Alert';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import SaveIcon from '@mui/icons-material/Save';
import AddIcon from '@mui/icons-material/Add';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';

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
      <Container maxWidth="xl" sx={{ py: 4, width: '100%' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h3" component="h1">
            Flokkar
          </Typography>
          <Chip 
            label={`${activeCategories.length} virkir flokkar`}
            color="primary"
            size="medium"
          />
        </Box>

        {/* API Fetch Section */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Sækja flokka frá API
          </Typography>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} sx={{ mb: 2 }}>
            <TextField
              fullWidth
              type="url"
              placeholder="https://api.example.com/categories"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              size="small"
            />
            <Button
              variant="contained"
              onClick={fetchFromApi}
              disabled={isFetching}
              startIcon={<CloudDownloadIcon />}
              sx={{ minWidth: 180 }}
            >
              {isFetching ? 'Sæki...' : 'Sækja frá API'}
            </Button>
          </Stack>
          <Typography variant="body2" color="text.secondary">
            API þarf að skila fylki af flokkum með <code>name</code> eða <code>title</code> svæði
          </Typography>
        </Paper>

        {/* Create/Edit Form */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            {isEditing ? 'Breyta flokki' : 'Nýr flokkur'}
          </Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Grid container spacing={2}>
            <Grid size={{ xs: 12, md: 8 }}>
              <TextField
                fullWidth
                label="Nafn flokks"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                size="small"
              />
            </Grid>
            <Grid size={{ xs: 12, md: 4 }}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.isActive}
                    onChange={(e) => setFormData({ ...formData, isActive: e.target.checked })}
                  />
                }
                label="Virkur í valmynd"
              />
            </Grid>
          </Grid>
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            {isEditing ? (
              <>
                <Button 
                  variant="contained" 
                  onClick={handleUpdate}
                  startIcon={<SaveIcon />}
                >
                  Uppfæra
                </Button>
                <Button 
                  variant="outlined" 
                  onClick={resetForm}
                >
                  Hætta við
                </Button>
              </>
            ) : (
              <Button 
                variant="contained" 
                onClick={handleCreate}
                startIcon={<AddIcon />}
              >
                Stofna flokk
              </Button>
            )}
          </Box>
        </Paper>

        {/* Categories List */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom>
            Allir flokkar
          </Typography>
          {categories.length === 0 ? (
            <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', py: 6 }}>
              Engir flokkar ennþá
            </Typography>
          ) : (
            <Stack spacing={1}>
              {categories.map((category, index) => (
                <Card 
                  key={category.id} 
                  sx={{ 
                    opacity: category.isActive ? 1 : 0.6,
                    bgcolor: category.isActive ? 'background.paper' : 'action.hover'
                  }}
                >
                  <CardContent>
                    <Grid container spacing={2} alignItems="center">
                      <Grid size={{ xs: 12, sm: 2, md: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                          <IconButton
                            size="small"
                            onClick={() => moveUp(index)}
                            disabled={index === 0}
                            color="primary"
                          >
                            <ArrowUpwardIcon fontSize="small" />
                          </IconButton>
                          <Typography variant="body2" sx={{ fontWeight: 'bold', minWidth: 24, textAlign: 'center' }}>
                            {index + 1}
                          </Typography>
                          <IconButton
                            size="small"
                            onClick={() => moveDown(index)}
                            disabled={index === categories.length - 1}
                            color="primary"
                          >
                            <ArrowDownwardIcon fontSize="small" />
                          </IconButton>
                        </Box>
                      </Grid>
                      <Grid size={{ xs: 12, sm: 4, md: 3 }}>
                        <Typography variant="h6">
                          {category.name}
                        </Typography>
                      </Grid>
                      <Grid size={{ xs: 6, sm: 3, md: 2 }}>
                        <Chip
                          icon={category.isActive ? <CheckCircleIcon /> : <CancelIcon />}
                          label={category.isActive ? 'Virkur' : 'Óvirkur'}
                          color={category.isActive ? 'success' : 'default'}
                          onClick={() => toggleActive(category.id)}
                          size="small"
                        />
                      </Grid>
                      <Grid size={{ xs: 6, sm: 3, md: 3 }}>
                        <Typography variant="body2" color="text.secondary">
                          {new Date(category.updatedAt).toLocaleDateString('is-IS', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                          })}
                        </Typography>
                      </Grid>
                      <Grid size={{ xs: 12, md: 3 }}>
                        <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
                          <Button
                            variant="outlined"
                            color="secondary"
                            size="small"
                            onClick={() => handleEdit(category)}
                            startIcon={<EditIcon />}
                          >
                            Breyta
                          </Button>
                          <Button
                            variant="outlined"
                            color="error"
                            size="small"
                            onClick={() => handleDelete(category.id)}
                            startIcon={<DeleteIcon />}
                          >
                            Eyða
                          </Button>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              ))}
            </Stack>
          )}
        </Paper>

        {/* Active Categories Preview */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Virkir flokkar í valmynd
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Þessir flokkar birtast í fellivalmyndinni þegar ný frétt er búin til:
          </Typography>
          {activeCategories.length === 0 ? (
            <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', py: 6 }}>
              Engir virkir flokkar
            </Typography>
          ) : (
            <Grid container spacing={1}>
              {activeCategories.map((category, index) => (
                <Grid size={{ xs: 6, sm: 4, md: 3 }} key={category.id}>
                  <Chip
                    label={`${index + 1}. ${category.name}`}
                    color="primary"
                    variant="outlined"
                    sx={{ width: '100%' }}
                  />
                </Grid>
              ))}
            </Grid>
          )}
        </Paper>
      </Container>
    </Layout>
  );
};

export default Categories;
