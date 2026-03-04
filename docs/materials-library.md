# Materials Library

## Overview
The Materials Library provides a comprehensive interface for browsing and filtering materials from manufacturing partners. It features server-side pagination, multiple filtering options, and real-time search capabilities.

## Features

### Filtering Options
- **Manufacturer**: Filter materials by specific manufacturer
- **Category**: Filter by material type (leather, suede, mesh, synthetic, canvas, knit, other)
- **Printable Status**: Filter by printable vs non-printable materials
- **Search**: Real-time search by material name or code (300ms debounced)

### UI Components
- **Material Cards**: Display name, code, category, manufacturer, texture, and color
- **Color Chips**: Visual representation of material colors using hex values
- **Printable Badges**: Green "Printable" badge for printable materials, gray "Standard" for others
- **Pagination**: Server-side pagination with 12 materials per page

### Technical Implementation
- **Backend**: Laravel MaterialController with Inertia.js integration
- **Frontend**: Vue 3 with Tailwind CSS styling
- **Database**: Materials table with manufacturer relationships and proper indexing
- **Testing**: Comprehensive feature tests covering all filtering and pagination scenarios

## Routes

### Web Routes
- `GET /materials` - Materials Library index page

### API Routes (for future use)
- `GET /api/v1/materials` - List materials with filtering
- `GET /api/v1/materials/{material}` - Show specific material

## Database Schema

### Materials Table
- `id` - Primary key
- `manufacturer_id` - Foreign key to manufacturers
- `code` - Unique per manufacturer
- `name` - Material name
- `category` - Material category (enum)
- `color_hex` - Color representation (#RRGGBB)
- `texture_ref` - Texture description
- `printable` - Boolean for printable capability
- `constraints` - JSON field for material properties
- `active` - Boolean for active status
- `timestamps`

### Indexes
- Unique: `(manufacturer_id, code)`
- Index: `(manufacturer_id, category, active)`
- Index: `(printable, active)`

## Screenshots
The implementation includes:
1. Filter toolbar with all controls
2. Responsive material cards grid
3. Working pagination controls
4. Color chips and printable badges
5. Empty state handling
