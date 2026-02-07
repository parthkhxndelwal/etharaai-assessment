# Sutra HRMS - Contributing Guide

Thank you for your interest in contributing to Sutra HRMS!

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js 20+
- MongoDB 7+
- Redis 7+
- Docker & Docker Compose (optional)

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export MONGO_URL="mongodb://localhost:27017"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET_KEY="your-test-secret-key"

# Run the server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for function parameters and returns
- Write docstrings for all public functions
- Use Pydantic models for validation
- Keep functions small and focused

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Keep components small and reusable
- Use proper typing for props and state

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated for changes
- [ ] Documentation updated if needed
- [ ] No console.log or debugging code
- [ ] Environment variables documented
- [ ] Security considerations addressed
- [ ] Performance impact considered

## Project Structure Best Practices

### Backend
- **Models**: Pure data models (database schema)
- **Schemas**: API contracts (request/response)
- **Services**: Business logic
- **Routers**: API endpoints (thin layer)
- **Middleware**: Cross-cutting concerns

### Frontend
- **api/**: API service layer
- **components/**: Reusable UI components
- **context/**: Global state management
- **pages/**: Route components
- **utils/**: Pure utility functions

## Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

Examples:
```
feat(auth): add Google OAuth login
fix(attendance): resolve duplicate record error
docs(readme): update deployment instructions
```

## Questions?

Open an issue for discussion or reach out to the maintainers.

Thank you for contributing! 🙏
