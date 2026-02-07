@echo off
REM Sutra HRMS - Quick Setup Script for Windows
REM This script helps you get started with the application

echo.
echo 🕉️  Sutra HRMS - Setup Script
echo ==============================
echo.

REM Check for Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed
echo.

REM Check for .env file
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please update .env with your configurations before continuing
    echo    Important: Change JWT_SECRET_KEY and ADMIN_PASSWORD
    pause
)

echo ✅ .env file exists
echo.

REM Build and start services
echo 🏗️  Building Docker images...
docker-compose build

echo.
echo 🚀 Starting services...
docker-compose up -d

echo.
echo ⏳ Waiting for services to be healthy...
timeout /t 15 /nobreak >nul

echo ✅ Services should be running now!
echo.
echo 🎉 Sutra HRMS is ready!
echo.
echo Access the application:
echo   🌐 Frontend:     http://localhost:3000
echo   📡 Backend API:  http://localhost:8000
echo   📚 Swagger Docs: http://localhost:8000/docs
echo   📖 ReDoc:        http://localhost:8000/redoc
echo.
echo Default login credentials (change in .env):
echo   Email:    admin@sutra.com
echo   Password: admin123
echo.
echo Useful commands:
echo   View logs:       docker-compose logs -f
echo   Stop services:   docker-compose down
echo   Restart:         docker-compose restart
echo.
echo 🙏 Om Namah Shivaya ^| Jai Shree Ram! 🚩
echo.
pause
