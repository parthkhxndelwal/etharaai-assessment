# Sutra

A lightweight Human Resource Management System built for the Ethara.AI assessment.

**Sutra** (Sanskrit: सूत्र) means "thread", symbolizing the interconnected nature of organizational management.

View here:

| Service | URL |
|---------|-----|
| Frontend | https://sutra.parth.engineer |
| Backend API | https://sutra-8bv8.onrender.com |
| Swagger Docs | https://sutra-8bv8.onrender.com/docs |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui |
| Backend | FastAPI (Python 3.12) |
| Database | MongoDB 7 (Motor async driver) |
| Cache | Redis 7 |
| Auth | JWT (python-jose + bcrypt) |
| Deployment | Docker Compose / Vercel + Render |

## Features

- **Employee Management** - Add, view, update, and delete employee records
- **Attendance Tracking** - Mark daily attendance (Present / Absent / Half Day / Leave) and filter by date/status
- **Dashboard** - Summary cards, department distribution, per-employee attendance stats
- **UI States** - Loading spinners, empty states, error states with retry
- **Validation** - Client-side and server-side (email format, required fields, duplicate handling)
- **Caching** - Redis-backed response caching for performance
- **Rate Limiting** - Configurable per-endpoint rate limits
- **Security** - CORS, security headers, bcrypt password hashing

## Running Locally with Docker
 
The application is containerised. So you can simply run it with docker. If docker isn't installed, you can choose to proceed without it.

### Prerequisites

- Docker & Docker Compose (Open Docker Desktop app after installation, to run the docker daemon)

### Steps

```bash
git clone <repo-url>
cd etharaai-assessment
cp .env.example .env
docker-compose up --build
```

Once running:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

### Login (configurable through .env)

```
Email:    admin@sutra.com
Password: admin123
```

## Running Without Docker

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Requires MongoDB and Redis running locally.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── backend/
│   └── app/
│       ├── main.py          # App entry point, middleware, routes
│       ├── config.py         # Env-based configuration
│       ├── database.py       # MongoDB connection
│       ├── cache.py          # Redis client
│       ├── models/           # Pydantic DB models
│       ├── schemas/          # Request/response schemas
│       ├── routers/          # API endpoints
│       └── services/         # Business logic
├── frontend/
│   └── src/
│       ├── api/              # Axios API layer
│       ├── components/       # Reusable UI components
│       ├── context/          # React context providers
│       ├── pages/            # Route pages
│       └── utils/            # Helpers, validators, formatters
├── docker-compose.yml
└── .env.example
```

## API Endpoints

### Auth
- `POST /api/v1/auth/login` - Login with email/password
- `GET  /api/v1/auth/me` - Get current user

### Employees
- `POST   /api/v1/employees` - Create employee
- `GET    /api/v1/employees` - List employees (with search/filter)
- `GET    /api/v1/employees/{id}` - Get employee
- `PUT    /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Attendance
- `POST   /api/v1/attendance` - Mark attendance
- `GET    /api/v1/attendance` - List records (with date/status filters)
- `GET    /api/v1/attendance/{employee_id}` - Get employee attendance
- `PUT    /api/v1/attendance/{id}` - Update record
- `DELETE /api/v1/attendance/{id}` - Delete record

### Dashboard
- `GET /api/v1/dashboard/summary` - Overview stats
- `GET /api/v1/dashboard/attendance-summary` - Per-employee breakdown

## Assumptions & Limitations

- Single admin user (no multi-role system)
- One attendance record per employee per day (enforced by DB unique index)
- All timestamps stored in UTC
- Authentication is a bonus feature - the spec says "no authentication required" but JWT is implemented for production readiness
- Cache TTL: Dashboard 30s, employee lists 60s, individual records 300s

## Deployment

- **Frontend**: Vercel
- **Backend**: Render
- **Database**: MongoDB Atlas
- **Cache**: Upstash Redis