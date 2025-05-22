# PyHeart 🐍💜

<div align="center">
<img height="300" width="700" alt="PyHeart Demo" align="center" src="https://github.com/GowtherHeart/PyHeart/blob/main/_assets/1.gif">

**A modern, async Python web application built with FastAPI, PostgreSQL, and Redis**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7+-red.svg)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

</div>

## 🚀 Overview

PyHeart is a comprehensive REST API application that demonstrates modern Python web development practices. It features a clean architecture with separation of concerns, async/await patterns, database transactions, and comprehensive API documentation.

### ✨ Key Features

- **🎯 RESTful API** - Complete CRUD operations for Notes and Tasks entities
- **⚡ Async Architecture** - Built with FastAPI and async/await patterns
- **🛡️ Type Safety** - Full type annotations with Pydantic models
- **🔄 Transaction Management** - ACID transactions for data consistency
- **📖 Auto Documentation** - Interactive OpenAPI/Swagger documentation
- **🏗️ Clean Architecture** - Repository pattern, Use Cases, and Controllers
- **🔍 Advanced Filtering** - Search and pagination support
- **🧪 Testing Ready** - Comprehensive test structure
- **🐳 Docker Support** - Containerized development and deployment

## 🏛️ Architecture

PyHeart follows a **Clean Architecture** pattern with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Controllers   │────│   Use Cases     │────│  Repositories   │
│   (HTTP/CLI)    │    │ (Business Logic)│    │ (Data Access)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Models      │    │    Entities     │    │    Drivers      │
│ (Request/Resp)  │    │ (Domain Objects)│    │ (PostgreSQL)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Project Structure

```
PyHeart/
├── src/
│   ├── cmd/                    # Application entry points
│   │   ├── cli/               # CLI commands
│   │   └── http/              # HTTP server command
│   ├── config/                # Configuration management
│   ├── controllers/           # HTTP request handlers
│   │   ├── notes/            # Notes API endpoints
│   │   ├── tasks/            # Tasks API endpoints
│   │   └── internal/         # Internal/Admin endpoints
│   ├── entity/               # Domain entities
│   │   └── db/               # Database entities & types
│   ├── models/               # Data models
│   │   ├── db/               # Database models
│   │   ├── request/          # Request models
│   │   └── response/         # Response models
│   ├── pkg/                  # Shared packages
│   │   ├── abc/              # Abstract base classes
│   │   ├── driver/           # Database drivers
│   │   └── core/             # Core utilities
│   ├── repository/           # Data access layer
│   ├── usecase/              # Business logic
│   └── internal/             # Internal utilities
├── contrib/                  # External contributions
│   ├── migrations/           # Database migrations
│   ├── docker/              # Docker configurations
│   └── scripts/             # Utility scripts
├── tests/                    # Test suite
└── main.py                   # Application entry point
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | FastAPI | High-performance async web framework |
| **Database** | PostgreSQL | Primary data storage |
| **Cache** | Redis | Caching and session storage |
| **ORM/Query** | Raw SQL + asyncpg | Direct database queries |
| **Validation** | Pydantic | Data validation and serialization |
| **Containerization** | Docker | Development and deployment |
| **Testing** | pytest | Test framework |
| **Linting** | mypy, ruff | Code quality and type checking |

## 🏃‍♂️ Quick Start

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GowtherHeart/PyHeart.git
   cd PyHeart
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   ./contrib/scripts/migration.sh up
   ```

5. **Start the application**
   ```bash
   poetry run python main.py --cmd Http
   ```

### Using Docker

```bash
# Start all services (PostgreSQL, Redis, and PyHeart)
docker-compose up -d

# Run migrations
docker-compose exec app ./contrib/scripts/migration.sh up

# View logs
docker-compose logs -f app
```

## 📖 API Documentation

### 🗒️ Notes API (`/v1/notes/`)

Manage text notes with full CRUD operations and soft delete.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/notes/` | Retrieve notes with filtering and pagination |
| `POST` | `/v1/notes/` | Create a new note |
| `PATCH` | `/v1/notes/` | Update an existing note |
| `DELETE` | `/v1/notes/` | Soft delete a note |

### ✅ Tasks API (`/v1/tasks/`)

Manage tasks with completion tracking and soft delete.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/tasks/` | Retrieve tasks with filtering and pagination |
| `POST` | `/v1/tasks/` | Create a new task |
| `PATCH` | `/v1/tasks/` | Update task content and completion status |
| `DELETE` | `/v1/tasks/` | Soft delete a task |

### 🔧 Internal API (`/_internal/`)

Administrative endpoints for direct database operations.

⚠️ **Warning**: These endpoints bypass business logic and should not be exposed to end users.

- **Simple Operations** (`/_internal/v1/postgres/simple/`) - Direct DB operations without transactions
- **Transaction Operations** (`/_internal/v1/postgres/transaction/`) - Operations with transaction guarantees
- **Exception Testing** (`/_internal/v1/postgres/transaction_exception/`) - For testing rollback scenarios

## 📋 Configuration

### Environment Variables

```bash
# HTTP Server
HTTP__HOST=0.0.0.0
HTTP__PORT=8000
HTTP__WORKER=1
HTTP__RELOAD=true

# PostgreSQL Database
PG__HOST=localhost
PG__PORT=5432
PG__USERNAME=postgres
PG__PASSWORD=password
PG__DB=pyheart

# Redis Cache
REDIS__HOST=localhost
REDIS__PORT=6379
REDIS__USERNAME=
REDIS__PASSWORD=
REDIS__DB=0

# Logging
LOGGING__LVL=INFO

# CLI
CLI__DEBUG=false
```

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test category
poetry run pytest tests/endpoint/
```

## 🔍 Code Quality

```bash
# Type checking
poetry run mypy src tests main.py

# Linting
poetry run ruff check src tests

# Format code
poetry run ruff format src tests

# Run all quality checks
make lint
```

## 🗃️ Database Management

### Migrations

PyHeart uses SQL migrations with Goose format:

```bash
# Run all migrations
./contrib/scripts/migration.sh up

# Rollback one migration
./contrib/scripts/migration.sh down

# Check migration status
./contrib/scripts/migration.sh status
```

### Database Schema

- **notes** - Text notes with soft delete
- **tasks** - Tasks with completion tracking
- **internal** - Internal configuration storage

## 🚀 Deployment

### Docker Production

```bash
# Build production image
docker build -f contrib/docker/app.Dockerfile -t pyheart:latest .

# Run with production settings
docker run -p 8000:8000 --env-file .env.prod pyheart:latest
```

### Development Commands

```bash
# Start HTTP server
python main.py --cmd Http

# Run CLI commands
python main.py --cmd CreateNoteCli --name "Example" --content "Content"

# Development server with auto-reload
HTTP__RELOAD=true python main.py --cmd Http
```

## 🏗️ Development Guide

### Adding New Entities

1. Create database migration in `contrib/migrations/`
2. Define entity types in `src/entity/db/types/`
3. Create entity classes in `src/entity/db/`
4. Build database models in `src/models/db/`
5. Create request/response models in `src/models/`
6. Implement repository queries in `src/repository/`
7. Add business logic in `src/usecase/`
8. Create HTTP controller in `src/controllers/`
9. Register controller in `src/cmd/http/_main.py`

### Code Patterns

- **Entities** - Domain objects with field validation
- **Models** - Pydantic models for serialization
- **Repositories** - Data access with SQL queries
- **Use Cases** - Business logic with transaction management
- **Controllers** - HTTP request/response handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make lint`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - For the excellent async web framework
- **Pydantic** - For powerful data validation
- **asyncpg** - For high-performance PostgreSQL driver
- **Docker** - For containerization support

## 📞 Support

If you have any questions or need help:

- 📧 Create an issue on [GitHub Issues](https://github.com/GowtherHeart/PyHeart/issues)
- 📖 Check the [API Documentation](http://localhost:8000/docs) when running locally
- 💬 Join our discussions on GitHub

---

<div align="center">

**Made with 💜 by GowtherHeart**

⭐ Star this repository if you found it helpful!

</div>
