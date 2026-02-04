import React, { useState } from 'react';
import axios from 'axios';
import Layout from '../components/Layout';
import type { FishingReport } from '../types';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import RefreshIcon from '@mui/icons-material/Refresh';
import AssessmentIcon from '@mui/icons-material/Assessment';

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
      <Container maxWidth="xl" sx={{ py: 4, width: '100%' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <AssessmentIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h3" component="h1">
              Afla skýrslur
            </Typography>
          </Box>
          <Button
            variant="contained"
            onClick={fetchReports}
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <RefreshIcon />}
            size="large"
          >
            {loading ? 'Hleð...' : 'Sækja skýrslur'}
          </Button>
        </Box>

        {error && (
          <Alert severity="info" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {reports.length > 0 ? (
          <>
            <TableContainer component={Paper} sx={{ mb: 3 }}>
              <Table>
                <TableHead>
                  <TableRow sx={{ bgcolor: 'primary.main' }}>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Tegund</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }} align="right">Magn (tonn)</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Dagsetning</TableCell>
                    <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Staðsetning</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {reports.map((report, index) => (
                    <TableRow
                      key={index}
                      sx={{ 
                        '&:nth-of-type(odd)': { bgcolor: 'action.hover' },
                        '&:hover': { bgcolor: 'action.selected' }
                      }}
                    >
                      <TableCell>
                        <Typography variant="body1" fontWeight="medium">
                          {report.species}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body1">
                          {report.quantity.toLocaleString('is-IS')}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        {new Date(report.date).toLocaleDateString('is-IS', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </TableCell>
                      <TableCell>{report.location}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <AssessmentIcon color="primary" />
                Samantekt
              </Typography>
              <Grid container spacing={3}>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Card variant="outlined" sx={{ bgcolor: 'primary.light', color: 'primary.contrastText' }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Heildarafli
                      </Typography>
                      <Typography variant="h4">
                        {reports.reduce((sum, r) => sum + r.quantity, 0).toLocaleString('is-IS')} tonn
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 12, sm: 6 }}>
                  <Card variant="outlined" sx={{ bgcolor: 'secondary.light', color: 'secondary.contrastText' }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Fjöldi tegunda
                      </Typography>
                      <Typography variant="h4">
                        {new Set(reports.map(r => r.species)).size}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Paper>
          </>
        ) : (
          !loading && (
            <Paper sx={{ p: 6 }}>
              <Box sx={{ textAlign: 'center' }}>
                <AssessmentIcon sx={{ fontSize: 60, color: 'text.disabled', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  Engar skýrslur tiltækar
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Smelltu á "Sækja skýrslur" til að hlaða gögnum.
                </Typography>
              </Box>
            </Paper>
          )
        )}
      </Container>
    </Layout>
  );
};

export default Reports;
