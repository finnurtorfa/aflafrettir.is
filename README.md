# Aflafréttir Admin Interface

A modern admin interface for a news website focused on the Icelandic fishing industry, built with **Material UI** and **React 19**.

## Features

- 🎨 **Material UI Design System** - Modern, responsive UI with Google's Material Design
- 🔐 **Login Interface** - Secure authentication for admin users
- 📰 **News Article Management** - Full CRUD operations for news articles
- 📋 **Article Metadata** - Professional content management
  - 📝 **Article Name** - Display name for readers
  - 📅 **Publish Date/Time** - Schedule article publishing (default: now)
  - 🏷️ **Categories** - Dynamic category system (managed centrally)
- 🗂️ **Category Management** - Complete category administration
  - ✏️ **Full CRUD** - Create, read, update, delete categories
  - 🌐 **API Integration** - Fetch categories from external APIs
  - ✅ **Active/Inactive Toggle** - Control which categories appear in dropdowns
  - 🔢 **Reordering** - Move categories up/down to set priority
  - 📊 **Live Preview** - See active categories as they appear to users
- ✍️ **Enhanced Rich Text Editor** - Professional Slate.js editor with:
  - Text formatting (bold, italic, underline, strikethrough, code)
  - Multiple heading levels (H1, H2, H3)
  - Lists (numbered & bulleted)
  - Blockquotes
  - Links
  - 📤 **Image Upload** - Upload images directly from your computer
  - 🖼️ **Image URL** - Insert images from web addresses
  - 📊 **Tables** - Create and edit data tables
- 📢 **Advertisement Management** - Create and manage website ads
  - 📤 **Image Upload** - Upload ad images directly from your computer
  - 🖼️ **Image URL** - Insert images from web addresses
  - 🔗 **Clickable Ads** - Link ads to external websites
  - 👁️ **Image Preview** - See ads before publishing
- 📊 **Fishing Industry Reports** - Fetch and display reports from external APIs
- 📱 **Fully Responsive** - Optimized for desktop, tablet, and mobile devices
- 🎯 **Centered Layout** - Content automatically centers and scales with browser width

## Tech Stack

- **React 19** with TypeScript
- **Material UI v7** (MUI) - Complete UI component library
- **Emotion** - CSS-in-JS styling (MUI requirement)
- **Vite** for fast development
- **React Router** for navigation
- **Slate.js** - Professional rich text editor framework
  - Enhanced with tables, image upload, and advanced formatting
- **Axios** for API calls
- **LocalStorage** for data persistence (replace with backend API)
- **Nginx** for production deployment
- **Docker/Podman** for containerization

## Getting Started

### Prerequisites

- **Node.js 22+** (for local development)
- **Podman** or **Docker** (for containerized deployment)

### Option 1: Local Development

#### Installation

```bash
cd aflafrettir.is
npm install
```

#### Development Server

```bash
npm run dev
```

Visit **http://localhost:3000**

#### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Option 2: Run with Podman (Recommended for Production)

#### Using Podman Compose

```bash
podman-compose up -d --build
```

Visit **http://localhost:3000**

#### Manual Podman Commands

```bash
# Build the container image
podman build -t aflafrettir-admin:latest .

# Run the container
podman run -d \
  --name aflafrettir-admin \
  -p 3000:80 \
  aflafrettir-admin:latest
```

#### Stop the Container

```bash
podman stop aflafrettir-admin
podman rm aflafrettir-admin
```

### Option 3: Development Container (with Hot Reload)

For development with hot reload and volume mounts:

```bash
podman-compose -f docker-compose.dev.yml up -d --build
```

This will:
- Mount source files for live editing
- Enable hot module replacement
- Run Vite dev server in container

### Option 4: Run with Docker

#### Using Docker Compose

```bash
docker-compose up -d --build
```

#### Manual Docker Commands

```bash
# Build the container image
docker build -t aflafrettir-admin:latest .

# Run the container
docker run -d \
  --name aflafrettir-admin \
  -p 3000:80 \
  aflafrettir-admin:latest
```

Visit **http://localhost:3000**

#### Stop the Services

```bash
# Docker Compose
docker-compose down

# Podman Compose
podman-compose down
```

## Login Credentials

For development, any email/password combination will work (mock authentication).

**Example:**
- Email: `admin@aflafrettir.is`
- Password: `anything`

## Project Structure

```
aflafrettir.is/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Layout.tsx       # MUI AppBar navigation
│   │   ├── PlateEditor.tsx  # Rich text editor
│   │   └── ProtectedRoute.tsx
│   ├── context/            # React context providers
│   │   └── AuthContext.tsx
│   ├── pages/             # Page components (all using MUI)
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Articles.tsx
│   │   ├── ArticleEditor.tsx
│   │   ├── Categories.tsx
│   │   ├── Ads.tsx
│   │   └── Reports.tsx
│   ├── types/             # TypeScript type definitions
│   │   └── index.ts
│   ├── theme.ts           # MUI theme configuration
│   ├── App.tsx            # Main app with ThemeProvider
│   └── main.tsx
├── Dockerfile             # Production container (nginx)
├── Dockerfile.dev         # Development container (vite dev server)
├── docker-compose.yml     # Production compose file
├── docker-compose.dev.yml # Development compose file
├── nginx.conf            # Nginx server configuration
├── vite.config.ts        # Vite configuration (container-ready)
└── package.json          # Node.js dependencies
```

## Material UI Implementation

All pages use Material UI components for a consistent, modern design:

### UI Components Used
- **Layout**: AppBar, Toolbar, Container, Box
- **Forms**: TextField, Select, Checkbox, FormControl, Button
- **Data Display**: Card, CardContent, Typography, Chip, Table
- **Feedback**: Alert, CircularProgress
- **Navigation**: Button with Link integration
- **Layout**: Grid system with responsive breakpoints
- **Icons**: MUI Icons throughout

### Theme Customization

The application uses a custom theme (`src/theme.ts`) with brand colors:
- Primary: `#77ccdd` (Aflafréttir brand color)
- Secondary: `#3498db`
- Error: `#e74c3c`
- Background: `#f5f5f5`

### Responsive Design

All layouts use MUI Grid with responsive breakpoints:
- `xs`: Mobile (< 600px)
- `sm`: Small tablet (≥ 600px)
- `md`: Medium screens (≥ 900px)
- `lg`: Large desktop (≥ 1200px)
- `xl`: Extra large (≥ 1536px)

Content is centered with `Container maxWidth="xl"` and scales dynamically.

## Container Details

### Production Container (Dockerfile)

The containerized version uses a **multi-stage build**:

1. **Build stage**: Compiles the React app using Node.js 22
2. **Production stage**: Serves static files using Nginx Alpine

**Image size**: ~50MB (optimized with Alpine Linux)

**Port mapping**: Container port 80 → Host port 3000

### Development Container (Dockerfile.dev)

For development with hot reload:
- Uses Node.js 22 Alpine
- Runs Vite dev server
- Volume mounts for live editing
- Port 3000 exposed

## Environment Variables

Currently using localStorage for demo. To connect to a backend API:

1. Create a `.env` file:
```bash
VITE_API_URL=https://api.aflafrettir.is
```

2. Update API calls in the code to use `import.meta.env.VITE_API_URL`

## Development Commands

```bash
# Install dependencies
npm install

# Start dev server (localhost:3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Container Commands

### Production

```bash
# Build and start with compose
podman-compose up -d --build

# Or manually
podman build -t aflafrettir-admin .
podman run -d -p 3000:80 --name aflafrettir-admin aflafrettir-admin

# View logs
podman logs -f aflafrettir-admin

# Stop and remove
podman stop aflafrettir-admin
podman rm aflafrettir-admin

# Rebuild after code changes
podman-compose down
podman-compose up -d --build
```

### Development

```bash
# Start dev container with hot reload
podman-compose -f docker-compose.dev.yml up -d --build

# View logs
podman logs -f aflafrettir-admin-dev

# Stop
podman-compose -f docker-compose.dev.yml down
```

## Editor Features

See `ENHANCED_EDITOR.md` and `TABLE_AND_UPLOAD_FEATURES.md` for detailed editor documentation.

### Quick Overview
- ✅ Rich text formatting (bold, italic, underline, strikethrough, code)
- ✅ Headings (H1, H2, H3)
- ✅ Lists (numbered and bulleted)
- ✅ Links with URL prompts
- ✅ **Image upload from computer**
- ✅ **Image insert from URL** 
- ✅ **Tables with custom rows/columns**
- ✅ Blockquotes
- ✅ Keyboard shortcuts (Ctrl/Cmd + B/I/U)
- ✅ Active state toolbar buttons

## Recent Updates

### Version 2.0 - Material UI Migration (February 2026)
- ✨ Complete UI overhaul with Material UI v7
- 🎨 Modern, consistent design system
- 📱 Enhanced responsive design with MUI Grid
- 🎯 Centered, scalable layouts
- 🔧 Container configuration for development and production
- ⚡ Vite configured for container networking

## Next Steps

1. **Backend Integration** - Replace localStorage with actual API calls
2. **Authentication** - Implement proper JWT-based authentication
3. **API Integration** - Connect to Icelandic fishing industry APIs (e.g., Fiskistofa API)
4. **Image Storage** - Move from base64 to cloud storage (S3, Cloudinary)
5. **Database** - Set up PostgreSQL or MongoDB for persistent storage
6. **Deployment** - Deploy to production (Kubernetes, OpenShift, or cloud platform)
7. **Testing** - Add unit and integration tests
8. **Accessibility** - Enhance ARIA labels and keyboard navigation

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, change the port mapping:

```bash
podman run -d -p 8080:80 --name aflafrettir-admin aflafrettir-admin
# Access via http://localhost:8080
```

### Can't Access localhost:3000 in Container

Make sure:
1. Container is running: `podman ps | grep aflafrettir`
2. Port is mapped correctly: Should show `0.0.0.0:3000->80/tcp`
3. Rebuild container after code changes: `podman-compose up -d --build`

### Container Exits Immediately

Check logs:
```bash
podman logs aflafrettir-admin
```

Common issues:
- Build failed - Check build logs
- Port conflict - Change port mapping
- Nginx configuration error - Verify nginx.conf

### Permission Denied (Podman)

Run Podman in rootless mode or add your user to the appropriate group:
```bash
sudo usermod -aG podman $USER
```

### Build Fails

Ensure you have:
- Enough disk space (>2GB free)
- Docker/Podman is running properly
- Internet connection for npm dependencies
- Node.js 22+ installed (for local builds)

### Material UI Components Not Rendering

Make sure:
1. All dependencies are installed: `npm install`
2. Theme is properly configured in `App.tsx`
3. No CSS conflicts with old styles
4. Browser cache is cleared

## License

MIT

## Support

For issues or questions, please contact the development team.
