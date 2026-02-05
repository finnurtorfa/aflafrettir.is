# Excel Download Feature - Reports Page

## Overview

The Reports page includes functionality to download Excel files from an external API endpoint with date range filtering. This feature allows users to retrieve fishing industry reports in Excel format for a specific time period.

## Features

### 1. **Date Range Selection**
- "Frá dagsetningu" (From date) picker
- "Til dagsetningar" (To date) picker
- Default range: Last 30 days
- Validation: From date cannot be after To date
- Max date: Today (cannot select future dates)

### 2. **Download Excel Button**
- Green "Hlaða niður Excel" (Download Excel) button
- Shows loading state with spinner while downloading
- Downloads file directly to browser
- Located in the date range section

### 3. **Date Validation**
- Prevents selecting invalid date ranges
- Shows error message in Icelandic if dates are invalid
- Ensures from date ≤ to date

### 4. **Error Handling**
- Displays detailed error messages for:
  - Invalid date ranges
  - HTTP errors (with status codes)
  - Network connection issues
  - General download errors

### 5. **Automatic Filename Generation**
- Downloads as: `afla-skyrsla-YYYY-MM-DD-til-YYYY-MM-DD.xlsx`
- Includes the date range in the filename
- Example: `afla-skyrsla-2026-01-01-til-2026-01-31.xlsx`

## Technical Implementation

### Date Format

All dates are in **YYYY-MM-DD** format (ISO 8601):
- Example: `2026-02-04`
- Sent as URL query parameters to the API

### API Configuration

The API host is configured in `settings.json` at the project root:

```json
{
  "api": {
    "host": "https://api.example.com"
  }
}
```

**Important:** Only the host (protocol + domain) is configured, not the full endpoint path.

The application imports this file and constructs the full URL:

```typescript
import settings from '../../settings.json';

const apiHost = settings.api.host;
const url = `${apiHost}/fishing-reports/export?from=${fromDate}&to=${toDate}`;

const response = await axios.get(url, {
  responseType: 'blob', // Important: tells axios to expect binary data
  headers: {
    'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  }
});
```

### Example API Requests

```
GET https://api.example.com/fishing-reports/export?from=2026-01-01&to=2026-01-31
GET https://api.example.com/fishing-reports/export?from=2025-12-01&to=2025-12-31
```

### File Download Process

1. **Validate date range** (from ≤ to)
2. **Build API URL** with date query parameters
3. **Fetch Excel file** from API as blob
4. **Create download link** using `window.URL.createObjectURL()`
5. **Trigger download** programmatically
6. **Cleanup** temporary URLs and DOM elements

### MIME Type

The application expects Excel files with MIME type:
```
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
```

This supports modern `.xlsx` format (Excel 2007+).

## API Requirements

### Endpoint Configuration

Configure your API endpoint at the top of `Reports.tsx`:

```typescript
const API_ENDPOINT = 'https://api.example.com/fishing-reports/export';
```

Your API endpoint should:

1. **Accept date parameters** as query strings:
   - `from` - Start date in YYYY-MM-DD format
   - `to` - End date in YYYY-MM-DD format

2. **Return Excel file** as binary data (blob)

3. **Set proper headers**:
   ```
   Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
   Content-Disposition: attachment; filename="report.xlsx"
   ```

4. **Support CORS** if the API is on a different domain

### Example Backend (Node.js/Express)

```javascript
app.get('/fishing-reports/export', async (req, res) => {
  try {
    const { from, to } = req.query;
    
    // Validate dates
    if (!from || !to) {
      return res.status(400).json({ error: 'Missing date parameters' });
    }
    
    const fromDate = new Date(from);
    const toDate = new Date(to);
    
    if (fromDate > toDate) {
      return res.status(400).json({ error: 'Invalid date range' });
    }
    
    // Generate or fetch Excel file for date range
    const excelBuffer = await generateExcelReport(fromDate, toDate);
    
    // Set headers
    res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    res.setHeader('Content-Disposition', `attachment; filename="fishing-report-${from}-to-${to}.xlsx"`);
    
    // Send file
    res.send(excelBuffer);
  } catch (error) {
    console.error('Excel generation error:', error);
    res.status(500).json({ error: 'Failed to generate report' });
  }
});
```

### Example with ExcelJS (Node.js)

```javascript
const ExcelJS = require('exceljs');

async function generateExcelReport(fromDate, toDate) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Afla skýrsla');
  
  // Add metadata
  worksheet.getCell('A1').value = `Tímabil: ${fromDate.toISOString().split('T')[0]} til ${toDate.toISOString().split('T')[0]}`;
  worksheet.getCell('A1').font = { bold: true, size: 14 };
  worksheet.addRow([]); // Empty row
  
  // Add headers
  worksheet.columns = [
    { header: 'Tegund', key: 'species', width: 20 },
    { header: 'Magn (tonn)', key: 'quantity', width: 15 },
    { header: 'Dagsetning', key: 'date', width: 15 },
    { header: 'Staðsetning', key: 'location', width: 20 }
  ];
  
  // Fetch data for date range from database
  const data = await fetchFishingData(fromDate, toDate);
  
  // Add data
  worksheet.addRows(data);
  
  // Style headers
  worksheet.getRow(3).font = { bold: true };
  worksheet.getRow(3).fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: 'FF77CCDD' }
  };
  
  // Generate buffer
  const buffer = await workbook.xlsx.writeBuffer();
  return buffer;
}
```

## Usage

### For End Users

1. Navigate to the **Reports** page (`/reports`)
2. Select date range:
   - **Frá dagsetningu** (From date) - Start of period
   - **Til dagsetningar** (To date) - End of period
3. Click **"Hlaða niður Excel"** button
4. File will download automatically to your browser's download folder
5. Filename format: `afla-skyrsla-2026-01-01-til-2026-01-31.xlsx`

### For Developers

To integrate with your API:

1. Update the API endpoint constant in `Reports.tsx`:
   ```typescript
   const API_ENDPOINT = 'https://your-api.com/fishing-reports/export';
   ```

2. Ensure your API:
   - Accepts `from` and `to` query parameters
   - Returns Excel file with proper MIME type
   - Handles date validation server-side

3. Handle CORS if API is on different domain:
   ```javascript
   // Backend CORS configuration
   app.use(cors({
     origin: 'https://aflafrettir.is',
     credentials: true
   }));
   ```

## Error Messages (Icelandic)

| Error | Message |
|-------|---------|
| Missing dates | `Vinsamlegast veldu dagsetningar` |
| Invalid range | `Frá dagsetning getur ekki verið síðar en til dagsetning` |
| HTTP Error | `Villa við niðurhal: 404 - Not Found` |
| Network Error | `Ekki tókst að hafa samband við API. Athugaðu netsamband.` |
| General Error | `Villa við niðurhal: [error message]` |

## Date Range Features

### Default Range
- Automatically set to last 30 days
- From: 30 days ago
- To: Today

### Date Constraints
- From date cannot be after To date (enforced by input validation)
- To date cannot be in the future (max: today)
- Both dates are required before download

### UI Components
- Material UI `TextField` with `type="date"`
- Native browser date picker
- Full localization support (Icelandic labels)

## Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+

All modern browsers support:
- Date input type
- Blob API
- Download attributes

## Testing

### Test Scenarios

1. **Valid Date Range**
   ```
   From: 2026-01-01
   To: 2026-01-31
   Expected: Download successful
   ```

2. **Invalid Range (From > To)**
   ```
   From: 2026-02-01
   To: 2026-01-01
   Expected: Error message displayed
   ```

3. **Future Date**
   ```
   To: 2027-01-01
   Expected: Date picker prevents selection
   ```

4. **Missing Dates**
   ```
   From: (empty)
   To: (empty)
   Expected: Error message displayed
   ```

### Testing Checklist

- [ ] Date pickers appear and work correctly
- [ ] Default date range is set to last 30 days
- [ ] Cannot select From date after To date
- [ ] Cannot select future dates for To date
- [ ] Error displays for invalid ranges
- [ ] Download button shows loading state
- [ ] File downloads with correct filename including date range
- [ ] API receives correct date parameters in URL
- [ ] Error messages display properly in Icelandic
- [ ] Works on mobile devices

## Future Enhancements

- [ ] Preset date ranges (Last 7 days, Last month, Last year)
- [ ] Date range validation on server side
- [ ] Maximum range limit (e.g., max 1 year)
- [ ] Multiple format support (CSV, PDF)
- [ ] Progress bar for large files
- [ ] Download history/cache
- [ ] Email report functionality
- [ ] Scheduled automatic downloads

## Support

For issues or questions about the Excel download feature, check:

1. Browser console for detailed error messages
2. Network tab to see API request with date parameters
3. Verify date format in URL (should be YYYY-MM-DD)
4. Backend logs for server-side issues

Common issues:
- **CORS errors**: Configure CORS on backend
- **File not downloading**: Check MIME type
- **Wrong date range**: Verify query parameters in URL
- **Invalid dates**: Check date format (must be YYYY-MM-DD)
- **Empty file**: Verify backend filters data by date range correctly
