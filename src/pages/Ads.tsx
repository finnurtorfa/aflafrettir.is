import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import type { Ad } from '../types';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CardActions from '@mui/material/CardActions';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Cancel';
import UploadIcon from '@mui/icons-material/Upload';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelOutlinedIcon from '@mui/icons-material/CancelOutlined';

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
      <Container maxWidth="xl" sx={{ py: 4, width: '100%' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h3" component="h1">
            Auglýsingar
          </Typography>
          <Button
            variant="contained"
            onClick={() => setShowForm(true)}
            startIcon={<AddIcon />}
            size="large"
          >
            Ný auglýsing
          </Button>
        </Box>

        {showForm && (
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              {editingAd ? 'Breyta auglýsingu' : 'Ný auglýsing'}
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid size={12}>
                  <TextField
                    fullWidth
                    label="Titill"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    required
                    size="small"
                  />
                </Grid>
                <Grid size={12}>
                  <Typography variant="body2" gutterBottom>
                    Mynd
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
                    <Button
                      variant="outlined"
                      component="label"
                      startIcon={<UploadIcon />}
                    >
                      Hlaða upp mynd
                      <input
                        type="file"
                        accept="image/*"
                        hidden
                        onChange={handleImageUpload}
                      />
                    </Button>
                    <Typography variant="body2" color="text.secondary">
                      eða
                    </Typography>
                    <TextField
                      fullWidth
                      type="url"
                      placeholder="Sláðu inn vefslóð myndar"
                      value={formData.imageUrl}
                      onChange={(e) => {
                        setFormData({...formData, imageUrl: e.target.value});
                        setImagePreview(e.target.value);
                      }}
                      size="small"
                    />
                  </Box>
                  {imagePreview && (
                    <Box 
                      sx={{ 
                        border: 1, 
                        borderColor: 'divider', 
                        borderRadius: 1, 
                        p: 1,
                        maxWidth: 400 
                      }}
                    >
                      <img 
                        src={imagePreview} 
                        alt="Preview" 
                        style={{ 
                          width: '100%', 
                          height: 'auto',
                          display: 'block'
                        }} 
                      />
                    </Box>
                  )}
                </Grid>
                <Grid size={12}>
                  <TextField
                    fullWidth
                    type="url"
                    label="Vefslóð tengils"
                    placeholder="https://example.com"
                    value={formData.linkUrl}
                    onChange={(e) => setFormData({...formData, linkUrl: e.target.value})}
                    required
                    size="small"
                    helperText="Þar sem notendur fara þegar þeir smella á auglýsinguna"
                  />
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Staðsetning</InputLabel>
                    <Select
                      value={formData.position}
                      label="Staðsetning"
                      onChange={(e) => setFormData({...formData, position: e.target.value})}
                    >
                      <MenuItem value="sidebar">Hliðarslá</MenuItem>
                      <MenuItem value="header">Haus</MenuItem>
                      <MenuItem value="footer">Fótur</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={formData.active}
                        onChange={(e) => setFormData({...formData, active: e.target.checked})}
                      />
                    }
                    label="Virk"
                  />
                </Grid>
              </Grid>
              <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  type="submit"
                  startIcon={<SaveIcon />}
                >
                  Vista
                </Button>
                <Button
                  variant="outlined"
                  onClick={resetForm}
                  startIcon={<CancelIcon />}
                >
                  Hætta við
                </Button>
              </Box>
            </Box>
          </Paper>
        )}

        <Grid container spacing={3}>
          {ads.length === 0 ? (
            <Grid size={12}>
              <Typography variant="body1" color="text.secondary" sx={{ textAlign: 'center', py: 6 }}>
                Engar auglýsingar ennþá. Búðu til þína fyrstu auglýsingu!
              </Typography>
            </Grid>
          ) : (
            ads.map(ad => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={ad.id}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardMedia
                    component="a"
                    href={ad.linkUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{ 
                      display: 'block',
                      textDecoration: 'none',
                      '&:hover': {
                        opacity: 0.9
                      }
                    }}
                  >
                    <Box
                      component="img"
                      src={ad.imageUrl}
                      alt={ad.title}
                      sx={{
                        width: '100%',
                        height: 200,
                        objectFit: 'cover'
                      }}
                    />
                  </CardMedia>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" gutterBottom>
                      {ad.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      <strong>Tengill:</strong>{' '}
                      <Box
                        component="a"
                        href={ad.linkUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        sx={{ 
                          color: 'primary.main',
                          textDecoration: 'none',
                          '&:hover': {
                            textDecoration: 'underline'
                          },
                          display: 'block',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        {ad.linkUrl}
                      </Box>
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      <strong>Staðsetning:</strong> {ad.position}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      {ad.active ? (
                        <>
                          <CheckCircleIcon color="success" fontSize="small" />
                          <Typography variant="body2" color="success.main">
                            Virk
                          </Typography>
                        </>
                      ) : (
                        <>
                          <CancelOutlinedIcon color="disabled" fontSize="small" />
                          <Typography variant="body2" color="text.disabled">
                            Óvirk
                          </Typography>
                        </>
                      )}
                    </Box>
                  </CardContent>
                  <CardActions sx={{ justifyContent: 'flex-end', px: 2, pb: 2 }}>
                    <Button
                      variant="outlined"
                      color="secondary"
                      size="small"
                      onClick={() => editAd(ad)}
                      startIcon={<EditIcon />}
                    >
                      Breyta
                    </Button>
                    <Button
                      variant="outlined"
                      color="error"
                      size="small"
                      onClick={() => deleteAd(ad.id)}
                      startIcon={<DeleteIcon />}
                    >
                      Eyða
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))
          )}
        </Grid>
      </Container>
    </Layout>
  );
};

export default Ads;
