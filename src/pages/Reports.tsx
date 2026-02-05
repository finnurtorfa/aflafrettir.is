import React, { useState } from 'react';
import axios from 'axios';
import Layout from '../components/Layout';
import settings from '../../settings.json';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import AssessmentIcon from '@mui/icons-material/Assessment';
import DownloadIcon from '@mui/icons-material/Download';

const Reports: React.FC = () => {
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState('');
  
  // API host from settings.json (private config file, not in public/)
  const apiHost = settings.api.host;
  
  // Date range state - default to last 30 days
  const today = new Date();
  const thirtyDaysAgo = new Date(today);
  thirtyDaysAgo.setDate(today.getDate() - 30);
  
  const [fromDate, setFromDate] = useState(thirtyDaysAgo.toISOString().split('T')[0]);
  const [toDate, setToDate] = useState(today.toISOString().split('T')[0]);

  const downloadExcel = async () => {
    if (!fromDate || !toDate) {
      setError('Vinsamlegast veldu dagsetningar');
      return;
    }

    if (new Date(fromDate) > new Date(toDate)) {
      setError('Frá dagsetning getur ekki verið síðar en til dagsetning');
      return;
    }

    setDownloading(true);
    setError('');
    
    try {
      // Build URL with date parameters
      // apiHost comes from settings.json (e.g., https://api.example.com)
      // Full endpoint: https://api.example.com/fishing-reports/export
      const url = `${apiHost}/fishing-reports/export?from=${fromDate}&to=${toDate}`;
      
      // Call external API to download Excel file
      const response = await axios.get(url, {
        responseType: 'blob', // Important: tells axios to expect binary data
        headers: {
          'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
      });

      // Create a blob from the response
      const blob = new Blob([response.data], { 
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
      });

      // Create a download link and trigger it
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      
      // Generate filename with date range
      const fileName = `afla-skyrsla-${fromDate}-til-${toDate}.xlsx`;
      link.setAttribute('download', fileName);
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);
      
    } catch (err: any) {
      console.error('Download error:', err);
      if (err.response) {
        setError(`Villa við niðurhal: ${err.response.status} - ${err.response.statusText}`);
      } else if (err.request) {
        setError('Ekki tókst að hafa samband við API. Athugaðu netsamband.');
      } else {
        setError(`Villa við niðurhal: ${err.message}`);
      }
    } finally {
      setDownloading(false);
    }
  };

  return (
    <Layout>
      <Container maxWidth="xl" sx={{ py: 4, width: '100%' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
          <AssessmentIcon color="primary" sx={{ fontSize: 40 }} />
          <Typography variant="h3" component="h1">
            Afla skýrslur
          </Typography>
        </Box>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Hlaða niður Excel skýrslu
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Veldu tímabil til að sækja afla skýrslu
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid size={{ xs: 12, sm: 4 }}>
              <TextField
                fullWidth
                label="Frá dagsetningu"
                type="date"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                InputLabelProps={{ shrink: true }}
                inputProps={{
                  max: toDate,
                }}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <TextField
                fullWidth
                label="Til dagsetningar"
                type="date"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                InputLabelProps={{ shrink: true }}
                inputProps={{
                  min: fromDate,
                  max: today.toISOString().split('T')[0],
                }}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 4 }}>
              <Button
                fullWidth
                variant="contained"
                onClick={downloadExcel}
                disabled={downloading}
                startIcon={downloading ? <CircularProgress size={20} color="inherit" /> : <DownloadIcon />}
                size="large"
                color="success"
              >
                {downloading ? 'Hleð niður...' : 'Hlaða niður Excel'}
              </Button>
            </Grid>
          </Grid>
        </Paper>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
      </Container>
    </Layout>
  );
};

export default Reports;
