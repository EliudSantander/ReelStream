# ReelStream

ReelStream is a Django REST Framework backend API built on top of the Pagila PostgreSQL
database. The goal of this project is to simulate a real-world movie rental service backend,
focusing on API design, SOLID principles and database integration.

## Features
- RESTful film catalog endpoint
- JWT authentication
- Basic filtering support and pagination
- PostgreSQL (Pagila dataset) integration
- Browsable API interface
- Swagger/ReDoc API documentation

## Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Postman (API testing)

## Setup Instructions
### 1. Clone Repository
```bash
git clone
cd ReelStream
```

### 2.Backend setup
```bash
cd backend
```

Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3.Database setup
Inside the db folder:
```bash
docker compose up -d
```

This initializes PostgreSQL with the Pagila dataset.

### 4.Configure environment
Create `.env` based on `.env.example` and configure credentials.

### 5.Run migrations
```bash
python manage.py migrate
```

### 6.Start server
```bash
python manage.py runserver
```

## Authentication
JWT authentication is enabled.

Obtain a token:

```bash
POST /api/token/
```

Use token:
*Authorization: Bearer*

## Future Improvements
- Advanced filtering and pagination
- USer workflows
- CRUD expansion
- API testing automation
