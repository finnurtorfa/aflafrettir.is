# Configuration Guide

## Overview

The application uses a private `settings.json` file for configuration. This file is located at the project root and imported directly into the code at build time.

**Important:** Unlike `public/settings.json`, this configuration file is:
- ✅ **Private** - Not accessible via HTTP
- ✅ **Build-time only** - Embedded into the JavaScript bundle
- ✅ **Git-ignored** - Never committed to version control

## Configuration File

### Location

```
/settings.json  (project root, NOT in public/)
```

### Structure

```json
{
  "api": {
    "host": "https://api.example.com"
  }
}
```

### Configuration Options

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `api.host` | string | Yes | API host URL (without paths) | `"https://api.aflafrettir.is"` |

**Important:** Only specify the host (protocol + domain), not the full endpoint path.

✅ Correct: `"https://api.aflafrettir.is"`  
❌ Incorrect: `"https://api.aflafrettir.is/reports/export"`

## How It Works

### Build Time Import

The settings file is imported as a module and bundled at build time:

```typescript
// In Reports.tsx
import settings from '../../settings.json';

const apiHost = settings.api.host;
const url = `${apiHost}/fishing-reports/export?from=${fromDate}&to=${toDate}`;
```

### Endpoint Construction

The application constructs full API URLs from the configured host:

```typescript
// Host from settings.json
const apiHost = "https://api.aflafrettir.is"

// Constructs full URLs
GET https://api.aflafrettir.is/fishing-reports/export?from=2026-01-01&to=2026-01-31
```

## Quick Start

1. Copy the example file:
   ```bash
   cp settings.example.json settings.json
   ```

2. Edit with your API host:
   ```bash
   nano settings.json
   ```

3. Build:
   ```bash
   npm run build
   ```

## Environment-Specific Configuration

### Development
```json
{
  "api": {
    "host": "http://localhost:8080"
  }
}
```

### Production
Create `settings.production.json`:
```json
{
  "api": {
    "host": "https://api.aflafrettir.is"
  }
}
```

Build with production config:
```bash
cp settings.production.json settings.json
npm run build
```

## Docker Deployment

Copy settings before building:

```bash
# Create production settings
cp settings.production.json settings.json

# Build container
podman build -t aflafrettir-admin:latest .
```

The Dockerfile already copies all files including settings.json.

## Security

- ✅ File is **git-ignored** (see `.gitignore`)
- ✅ File is **private** (not in public/ folder)
- ✅ Never accessible via HTTP
- ✅ Embedded at build time only

## Troubleshooting

### Cannot find module '../../settings.json'

```bash
cp settings.example.json settings.json
```

### Settings not applied

Rebuild required after changes:
```bash
npm run build
```

### TypeScript errors

Ensure `tsconfig.app.json` has:
```json
{
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

## Further Details

See `EXCEL_DOWNLOAD.md` for information about the Reports API endpoint.
