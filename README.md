# 🕉️ Sutra HRMS Lite

A modern, lightweight Human Resource Management System built with cutting-edge technologies.

**Sutra** (Sanskrit: सूत्र) means "thread" or "formula" - symbolizing the interconnected nature of organizational management.

## ✨ Features

- **Employee Management**: Add, view, update, and delete employee records
- **Attendance Tracking**: Mark and monitor daily attendance with comprehensive reporting
- **Dashboard Analytics**: Real-time insights into workforce metrics
- **Dual Authentication**: Email/password login + Google OAuth integration
- **Real-time Caching**: Redis-powered performance optimization
- **Professional UI**: Modern interface built with shadcn/ui and Tailwind CSS
- **Smooth Animations**: Framer Motion-powered page transitions
- **API Documentation**: Interactive Swagger UI for backend exploration
- **Containerized Deployment**: Full Docker Compose orchestration

## 🏗️ Architecture

```
┌─────────────────┐
│  Frontend (SPA) │  Vite + React + TypeScript
│  Port: 3000     │  Tailwind CSS + shadcn/ui
└────────┬────────┘
         │ HTTP/JSON
         ↓
┌─────────────────┐
│   Nginx Proxy   │  Static files + API reverse proxy
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ FastAPI Backend │  Python 3.12
│  Port: 8000     │  JWT + OAuth + Rate Limiting
└────┬──────┬─────┘
     │      │
     ↓      ↓
┌────────┐ ┌────────┐
│MongoDB │ │ Redis  │
│Port:   │ │Port:   │
│27017   │ │6379    │
└────────┘ └────────┘
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: React Context API
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **OAuth**: @react-oauth/google

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Database**: MongoDB (Motor async driver)
- **Cache**: Redis (async client)
- **Authentication**: JWT + Google OAuth
- **Validation**: Pydantic v2
- **Security**: slowapi (rate limiting), custom middleware
- **API Docs**: OpenAPI (Swagger UI + ReDoc)

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (production)
- **Databases**: MongoDB 7, Redis 7

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- (Optional) Node.js 20+ and Python 3.12+ for local development

### 1. Clone and Setup

```bash
cd etharaai-assessment
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and update:
- `JWT_SECRET_KEY`: Generate with `openssl rand -hex 32`
- `ADMIN_EMAIL` & `ADMIN_PASSWORD`: Your admin credentials
- (Optional) Google OAuth credentials if enabling social login

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

This will start all services:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

### 4. Login

Navigate to http://localhost:3000 and login with:
- Email: `admin@sutra.com` (or your configured admin email)
- Password: `admin123` (or your configured password)

## 📁 Project Structure

```
sutra-hrms/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app initialization
│   │   ├── config.py            # Environment configuration
│   │   ├── database.py          # MongoDB connection
│   │   ├── cache.py             # Redis client
│   │   ├── middleware.py        # Security headers, rate limiting
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic schemas (API contracts)
│   │   ├── routers/             # API endpoints
│   │   └── services/            # Business logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                 # API service layer
│   │   ├── components/          # React components
│   │   ├── context/             # Context providers
│   │   ├── hooks/               # Custom hooks
│   │   ├── pages/               # Route pages
│   │   ├── utils/               # Utilities
│   │   └── App.tsx              # Root component
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based auth with configurable expiration
- **Google OAuth**: Optional social login integration
- **Rate Limiting**: Redis-backed rate limiting (100 req/min global, 10 req/min for auth)
- **Security Headers**: X-Frame-Options, CSP, HSTS, X-Content-Type-Options
- **Input Validation**: Pydantic-powered request validation
- **CORS Protection**: Configurable allowed origins
- **Password Hashing**: bcrypt-based secure password storage
- **MongoDB Injection Prevention**: Parameterized queries via Motor

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Email/password login
- `POST /api/v1/auth/google` - Google OAuth login
- `GET /api/v1/auth/me` - Get current user info

### Employees
- `POST /api/v1/employees` - Create employee
- `GET /api/v1/employees` - List all employees (with filters)
- `GET /api/v1/employees/{id}` - Get single employee
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Attendance
- `POST /api/v1/attendance` - Mark attendance
- `GET /api/v1/attendance` - Get all attendance records (with filters)
- `GET /api/v1/attendance/{employee_id}` - Get employee attendance
- `PUT /api/v1/attendance/{id}` - Update attendance
- `DELETE /api/v1/attendance/{id}` - Delete attendance record

### Dashboard
- `GET /api/v1/dashboard/summary` - Dashboard statistics
- `GET /api/v1/dashboard/attendance-summary` - Per-employee attendance summary

Visit `/docs` for interactive API documentation.

## 🧪 Local Development

### Backend Only

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

## 📝 Environment Variables Reference

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URL` | MongoDB connection string | `mongodb://admin:password@localhost:27017` |
| `MONGO_DB_NAME` | MongoDB database name | `hrms` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `JWT_SECRET_KEY` | Secret key for JWT signing | *(generate with `openssl rand -hex 32`)* |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time | `1440` (24 hours) |
| `ADMIN_EMAIL` | Default admin email | `admin@sutra.com` |
| `ADMIN_PASSWORD` | Default admin password | `admin123` |
| `ADMIN_FULL_NAME` | Admin display name | `System Administrator` |
| `GOOGLE_OAUTH_ENABLED` | Enable Google login | `false` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | *(optional)* |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:5173` |
| `RATE_LIMIT_PER_MINUTE` | Global rate limit | `100` |

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` |
| `VITE_GOOGLE_CLIENT_ID` | Google OAuth Client ID (optional) | *(empty)* |

### Docker Compose Variables

See `.env.example` for configuration used in Docker Compose deployments.

## 🎯 Assumptions & Limitations

- **Single Admin User**: No multi-user role management (admin only)
- **Employee ID Format**: User-entered, must be unique (validated at DB level)
- **Attendance Records**: One record per employee per day (enforced by compound unique index)
- **No Authentication Required**: As per assignment spec, but JWT security implemented for production readiness
- **Time Zone**: All timestamps in UTC
- **Cache TTL**: Dashboard (30s), Employee lists (60s), Individual employees (300s)

## 🚢 Deployment

The application is production-ready and can be deployed to:

### Frontend
- Vercel
- Netlify
- AWS Amplify
- Azure Static Web Apps

### Backend
- Render
- Railway
- Fly.io
- AWS ECS/Fargate
- Google Cloud Run

### Full Stack (Docker)
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

**Production Checklist**:
- ✅ Change `JWT_SECRET_KEY` to a strong random value
- ✅ Update `ADMIN_PASSWORD` to a secure password
- ✅ Configure `CORS_ORIGINS` to your production domain
- ✅ Enable HTTPS (configure reverse proxy/load balancer)
- ✅ Set up MongoDB backups
- ✅ Configure Redis persistence (RDB/AOF)
- ✅ Use secrets management (AWS Secrets Manager, Azure Key Vault, etc.)
- ✅ Enable monitoring and logging

## 🐛 Troubleshooting

### Backend won't start
- **Check MongoDB connection**: Ensure MongoDB is running and accessible
- **Check Redis connection**: Verify Redis is running on the correct port
- **Environment variables**: Validate all required env vars are set
- **Port conflicts**: Ensure port 8000 is not in use

### Frontend won't connect to backend
- **CORS errors**: Check `CORS_ORIGINS` includes your frontend URL
- **API URL**: Verify `VITE_API_URL` in `.env` points to correct backend
- **Network**: Ensure frontend can reach backend (check Docker network in containerized setup)

### Authentication issues
- **JWT errors**: Regenerate `JWT_SECRET_KEY` and restart backend
- **Google OAuth fails**: Verify `GOOGLE_CLIENT_ID` matches Google Cloud Console configuration
- **Token expired**: Default token lifetime is 24 hours, check `ACCESS_TOKEN_EXPIRE_MINUTES`

### Database issues
- **Duplicate key errors**: Employee ID or email already exists, use unique values
- **Connection timeout**: Check MongoDB connection string and network access
- **Indexes not created**: Restart backend to trigger index creation on startup

### Performance issues
- **Slow queries**: Check MongoDB indexes are created properly
- **Cache misses**: Verify Redis is running and configured correctly
- **High memory usage**: Adjust Redis `maxmemory` policy in production

### Docker Compose issues
- **Containers won't start**: Run `docker-compose logs <service>` to see error logs
- **Permission denied**: On Linux, may need to run with `sudo` or configure Docker permissions
- **Build failures**: Clear Docker cache with `docker-compose build --no-cache`

## 🧪 Testing the Application

### Quick Verification

1. **Health Checks**:
   - Frontend: http://localhost:3000/health
   - Backend: http://localhost:8000/health

2. **Create Sample Employee**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/employees \
     -H "Authorization: Bearer <your-jwt-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "employee_id": "EMP-001",
       "full_name": "John Doe",
       "email": "john@example.com",
       "department": "Engineering",
       "position": "Software Engineer"
     }'
   ```

3. **Mark Attendance**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/attendance \
     -H "Authorization: Bearer <your-jwt-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "employee_id": "EMP-001",
       "date": "2024-01-15",
       "status": "present",
       "notes": "On time"
     }'
   ```

4. **View Dashboard**: Navigate to http://localhost:3000/dashboard

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [MongoDB Manual](https://docs.mongodb.com/)
- [Redis Documentation](https://redis.io/documentation)

## 🙏 Om Namah Shivaya

Built with devotion and precision.

**Jai Shree Ram!** 🚩

---

**License**: MIT  
**Version**: 1.0.0  
**Author**: Built for Etharaai Assessment
