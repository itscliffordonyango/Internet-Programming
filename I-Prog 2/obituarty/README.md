# Obituary Management Platform

A compassionate, production-quality web application for submitting, managing, and sharing obituaries. Built with Flask and SQLAlchemy, this platform provides a dignified space for remembering and honoring loved ones.

## Features

- **Obituary Submission**: Easy-to-use form for submitting obituary records with validation on both frontend and backend.
- **Database Storage**: All obituaries stored securely in a SQLite database using SQLAlchemy ORM.
- **View All Obituaries**: Browse all submitted obituaries with a clean, card-based layout.
- **Search Functionality**: Search obituaries by name, author, or content.
- **Pagination**: Browse through obituaries with page navigation (6 per page).
- **Individual Obituary Pages**: Each obituary gets its own dedicated page with an SEO-friendly URL.
- **SEO Optimization**:
  - Dynamic page titles and meta descriptions
  - Canonical URLs
  - Open Graph tags (Facebook, LinkedIn)
  - Twitter Card metadata
  - Schema.org JSON-LD structured data
- **Social Media Sharing**: Share obituaries on Facebook, X (Twitter), and WhatsApp with one click.
- **Copy Link**: Copy the obituary URL to clipboard with visual feedback.
- **XML Sitemap**: Auto-generated sitemap for search engine indexing.
- **Responsive Design**: Modern, accessible UI that works on all devices.
- **Custom Error Pages**: Friendly 404 and 500 error pages.
- **Automated Testing**: Comprehensive test suite using pytest.

## Technology Stack

### Backend
- **Python 3** - Core programming language
- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **SQLite** - Development database
- **Jinja2** - Template engine
- **python-slugify** - URL slug generation
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Flexbox and Grid
- **Vanilla JavaScript** - Client-side validation and interactivity
- **Responsive Design** - Mobile-first approach

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd obituary-platform
```

2. **Create a virtual environment**
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables (optional)**
```bash
cp .env.example .env
# Edit .env with your settings if needed
```

## Running the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`.

The database is created automatically on first run.

## Project Structure

```
obituary-platform/
├── app.py                  # Application entry point and factory
├── config.py               # Configuration classes
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── database/              # SQLite database storage
│   └── obituary_platform.db
│
├── models/                # Database models
│   ├── __init__.py
│   └── obituary.py        # Obituary model
│
├── routes/                # Route blueprints
│   ├── __init__.py
│   ├── obituary_routes.py # Obituary CRUD routes
│   └── seo_routes.py      # SEO routes (sitemap)
│
├── templates/             # Jinja2 templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page
│   ├── obituary_form.html # Submission form
│   ├── view_obituaries.html # Listing page
│   ├── obituary_detail.html # Individual obituary
│   ├── success.html       # Success page
│   ├── 404.html           # Not found page
│   ├── 500.html           # Server error page
│   └── sitemap.xml        # Sitemap template
│
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Application styles
│   ├── js/
│   │   └── validation.js  # Client-side validation
│   └── images/
│       └── default-obituary-image.svg
│
├── tests/                 # Automated tests
│   ├── __init__.py
│   ├── conftest.py        # Test fixtures
│   ├── test_obituaries.py # Route tests
│   └── test_validation.py # Validation tests
│
└── seo/
    └── sitemap.xml        # Generated sitemap output
```

## Routes

| Route | Methods | Description |
|-------|---------|-------------|
| `/` | GET | Home page with hero section |
| `/submit-obituary` | GET, POST | Obituary submission form |
| `/obituaries` | GET | View all obituaries with search & pagination |
| `/obituary/<slug>` | GET | Individual obituary detail page |
| `/sitemap.xml` | GET | XML sitemap for search engines |

### Query Parameters

**Search & Pagination** (`/obituaries`):
- `?page=1` - Page number
- `?search=john` - Search term (matches name, author, content)

## Database

The application uses SQLite during development. The database file is created at:
```
database/obituary_platform.db
```

### Obituaries Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| name | String(100) | Full name of the deceased |
| date_of_birth | Date | Date of birth |
| date_of_death | Date | Date of death |
| content | Text | Obituary text |
| author | String(100) | Name of the person submitting |
| submission_date | DateTime | Auto-generated timestamp |
| slug | String(255) | Unique SEO-friendly URL |

The slug is automatically generated from the person's name. If duplicates exist, a number is appended (e.g., `john-kamau-2`).

## Testing

Run the test suite with pytest:

```bash
pytest
```

Or with verbose output:

```bash
pytest -v
```

### Tests included

- **Route tests**: Home page, form submission, listing, detail pages, search, pagination, sitemap
- **Validation tests**: Empty fields, invalid dates, date logic, length limits, duplicate slugs
- **Error tests**: 404 handling, database rollback behaviour

## SEO Features

### Meta Tags
Each obituary page dynamically generates:
- Title: `Remembering [Name] | Obituary Platform`
- Meta description based on obituary content
- Keywords based on name, author, and memorial terms

### Canonical URLs
Each page includes a `<link rel="canonical">` tag pointing to the correct URL.

### Open Graph Tags
```
og:title
og:description
og:type (article)
og:url
og:image
```

### Twitter Cards
```
twitter:card (summary_large_image)
twitter:title
twitter:description
twitter:image
```

### Structured Data
Schema.org JSON-LD (Article type) with:
- Name and headline
- Description
- Date published
- Author information
- Page URL

### XML Sitemap
Available at `/sitemap.xml`, includes:
- Home page
- Obituary listing page
- Every individual obituary URL

## GitHub Submission

```bash
# Initialize Git
git init
git add .
git commit -m "Initial commit: Obituary Management Platform"

# Create main branch
git branch -M main

# Add remote repository
git remote add origin <repository-url>

# Push to GitHub
git push -u origin main
```

## Security

- Parameterized SQLAlchemy queries prevent SQL injection
- All user input is validated server-side
- User content is escaped in templates (Jinja2 auto-escaping)
- Environment variables for sensitive configuration
- `.env` and `venv/` excluded from version control
- No raw database errors exposed to users

## License

This project is developed for academic assessment purposes.
