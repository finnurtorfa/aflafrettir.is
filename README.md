# Aflafréttir Admin Interface

A modern admin interface for a news website focused on the Icelandic fishing industry.

## Features

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

## Tech Stack

- **React 19** with TypeScript
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

- **Node.js 20+** (for local development)
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

Visit **http://localhost:5173**

#### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Option 2: Run with Podman (Recommended)

#### Build the Container Image

```bash
podman build -t aflafrettir-admin:latest .
```

#### Run the Container

```bash
podman run -d \
  --name aflafrettir-admin \
  -p 3000:80 \
  aflafrettir-admin:latest
```

Visit **http://localhost:3000**

#### Stop the Container

```bash
podman stop aflafrettir-admin
podman rm aflafrettir-admin
```

### Option 3: Run with Docker Compose / Podman Compose

#### Using Docker Compose

```bash
docker-compose up -d
```

#### Using Podman Compose

```bash
podman-compose up -d
```

Visit **http://localhost:3000**

#### Stop the Services

```bash
# Docker
docker-compose down

# Podman
podman-compose down
```

### Option 4: Run with Docker

#### Build the Container Image

```bash
docker build -t aflafrettir-admin:latest .
```

#### Run the Container

```bash
docker run -d \
  --name aflafrettir-admin \
  -p 3000:80 \
  aflafrettir-admin:latest
```

Visit **http://localhost:3000**

## Login Credentials

For development, any email/password combination will work (mock authentication).

**Example:**
- Email: `admin@aflafrettir.is`
- Password: `anything`

## Project Structure

```
aflafrettir.is/
├── src/
│   ├── components/       # Reusable components
│   │   ├── Layout.tsx
│   │   └── ProtectedRoute.tsx
│   ├── context/         # React context providers
│   │   └── AuthContext.tsx
│   ├── pages/          # Page components
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Articles.tsx
│   │   ├── ArticleEditor.tsx
│   │   ├── Ads.tsx
│   │   └── Reports.tsx
│   ├── types/          # TypeScript type definitions
│   │   └── index.ts
│   └── App.tsx         # Main app component
├── Dockerfile          # Container build configuration
├── docker-compose.yml  # Container orchestration
├── nginx.conf         # Nginx server configuration
└── package.json       # Node.js dependencies
```

## Container Details

The containerized version uses a **multi-stage build**:

1. **Build stage**: Compiles the React app using Node.js 20
2. **Production stage**: Serves static files using Nginx Alpine

**Image size**: ~50MB (optimized with Alpine Linux)

**Port mapping**: Container port 80 → Host port 3000

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

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Container Commands

```bash
# Build image
podman build -t aflafrettir-admin .

# Run container
podman run -d -p 3000:80 --name aflafrettir-admin aflafrettir-admin

# View logs
podman logs -f aflafrettir-admin

# Stop container
podman stop aflafrettir-admin

# Remove container
podman rm aflafrettir-admin

# Remove image
podman rmi aflafrettir-admin
```

## Editor Features

See `ENHANCED_EDITOR.md` and `TABLE_AND_UPLOAD_FEATURES.md` for detailed editor documentation.

### Quick Overview
- ✅ Rich text formatting (bold, italic, underline, strikethrough, code)
- ✅ Headings (H1, H2, H3)
- ✅ Lists (numbered and bulleted)
- ✅ Links with URL prompts
- ✅ **Image upload from computer** (NEW!)
- ✅ **Image insert from URL** 
- ✅ **Tables with custom rows/columns** (NEW!)
- ✅ Blockquotes
- ✅ Keyboard shortcuts (Ctrl/Cmd + B/I/U)
- ✅ Active state toolbar buttons

## Next Steps

1. **Backend Integration** - Replace localStorage with actual API calls
2. **Authentication** - Implement proper JWT-based authentication
3. **API Integration** - Connect to Icelandic fishing industry APIs (e.g., Fiskistofa API)
4. **Image Storage** - Move from base64 to cloud storage (S3, Cloudinary)
5. **Database** - Set up PostgreSQL or MongoDB for persistent storage
6. **Deployment** - Deploy to production (Kubernetes, OpenShift, or cloud platform)

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, change the port mapping:

```bash
podman run -d -p 8080:80 --name aflafrettir-admin aflafrettir-admin
```

### Permission Denied (Podman)

Run Podman in rootless mode or add your user to the appropriate group.

### Build Fails

Ensure you have enough disk space and Docker/Podman is running properly.

## License

MIT

## Support

For issues or questions, please contact the development team.
