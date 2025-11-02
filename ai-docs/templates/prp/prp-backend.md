# 🚀 PRP - Desenvolvimento Backend

## 🏷️ Metadados do PRP Backend
- **PRP ID**: {{prp_id}}
- **Tipo**: Backend Development
- **Domínio**: {{domain}} (ex: API, Microservice, Database)
- **Tecnologia**: {{technology}} (ex: Python/FastAPI, Node.js/Express)
- **Complexidade**: {{complexity}}

## 🎯 Business Context Layer

### Backend Business Objectives
```
{{backend_objectives}}
# Exemplo:
# "Desenvolver API RESTful para gestão de usuários que reduza tempo de resposta 
# em 50% e suporte 1000 req/segundo com 99.9% disponibilidade"
```

### SLAs & Performance Requirements
- **Disponibilidade**: {{availability}} (ex: 99.9%)
- **Latência**: {{latency}} (ex: < 200ms p95)
- **Throughput**: {{throughput}} (ex: 1000 req/seg)
- **Escalabilidade**: {{scalability}} (ex: horizontal scaling)

## 👥 Stakeholder Analysis

### Backend Stakeholders
```
{{backend_stakeholders}}
# - Mobile Developers: Consomem APIs RESTful
# - Web Frontend: Utiliza endpoints JSON
# - DevOps: Precisam de health checks e métricas
# - Database Admins: Concerned with query performance
```

## 📋 Backend Requirement Extraction

### API Endpoints Specification
```
{{api_endpoints}}
# GET /api/users - List users with pagination
# POST /api/users - Create new user
# GET /api/users/{id} - Get user by ID
# PUT /api/users/{id} - Update user
# DELETE /api/users/{id} - Delete user
```

### Data Models & Entities
```
{{data_models}}
# User:
# - id: UUID (primary key)
# - email: str (unique, indexed)
# - name: str
# - created_at: datetime
# - updated_at: datetime
# - is_active: bool
```

### Database Requirements
- **SGBD**: {{database}} (ex: PostgreSQL, MySQL, MongoDB)
- **Migrations**: {{migrations}} (ex: Alembic, Flyway)
- **Indexes**: {{indexes}} (ex: email unique index)
- **Constraints**: {{constraints}} (ex: foreign keys, not null)

## 🔧 Backend Technical Translation

### Architecture Pattern
```
{{architecture_pattern}}
# Exemplo para Python/FastAPI:
# - Pattern: Controller-Service-Repository
# - Controllers: FastAPI routers with dependency injection
# - Services: Business logic with unit tests
# - Repositories: Database operations with SQLAlchemy
# - Models: Pydantic schemas for validation
```

### Technology Stack Specifics
- **Framework**: {{framework}} (ex: FastAPI, Express.js, Spring Boot)
- **ORM/ODM**: {{orm}} (ex: SQLAlchemy, Mongoose, TypeORM)
- **Validation**: {{validation}} (ex: Pydantic, Joi, class-validator)
- **Authentication**: {{auth}} (ex: JWT, OAuth2, API keys)

### API Design Specifications
```
{{api_design}}
# - RESTful conventions with proper HTTP verbs
# - JSON responses with consistent structure
# - Error handling with standard HTTP codes
# - Pagination using limit/offset or cursor-based
# - Filtering, sorting, searching parameters
```

### Performance Considerations
```
{{performance_considerations}}
# - Database query optimization
# - Caching strategy (Redis, Memcached)
# - Connection pooling settings
# - Background job processing
# - Rate limiting and throttling
```

## 📝 Backend Specification Output

### Expected Backend Deliverables
```
{{backend_deliverables}}
# 1. Complete API implementation with all endpoints
# 2. Database models and migrations
# 3. Service layer with business logic
# 4. Repository pattern for data access
# 5. Pydantic schemas for request/response validation
# 6. Dependency injection setup
# 7. Error handling middleware
# 8. Logging configuration
```

### Code Structure
```
{{code_structure}}
# src/
# ├── main.py              # FastAPI app initialization
# ├── api/                 # API routers
# │   ├── users.py         # User endpoints
# │   └── __init__.py
# ├── services/            # Business logic
# │   ├── user_service.py
# │   └── __init__.py
# ├── repositories/       # Data access
# │   ├── user_repository.py
# │   └── __init__.py
# ├── models/              # Database models
# │   ├── user_model.py
# │   └── __init__.py
# ├── schemas/             # Pydantic schemas
# │   ├── user_schema.py
# │   └── __init__.py
# └── config.py            # Configuration
```

### Environment Configuration
```
{{environment_config}}
# .env.example:
# DATABASE_URL=postgresql://user:pass@localhost:5432/db
# JWT_SECRET=your-secret-key
# DEBUG=False
# CORS_ORIGINS=http://localhost:3000
```

## ✅ Backend Validation Framework

### Backend Testing Strategy
```
{{backend_testing}}
# - Unit tests for services and utilities
# - Integration tests for API endpoints
# - Database transaction rollback in tests
# - Test factories for model creation
# - Mock external dependencies
```

### Backend Quality Gates
```
{{backend_quality_gates}}
# - 100% test coverage on business logic
# - All endpoints have integration tests
# - No SQL injection vulnerabilities
# - Proper error handling and logging
# - Security headers implemented
# - API documentation generated
```

### Security Requirements
```
{{security_requirements}}
# - Input validation on all endpoints
# - SQL injection prevention
# - XSS protection
# - CORS properly configured
# - Rate limiting on public endpoints
# - Authentication/authorization
```

### Performance Testing
```
{{performance_testing}}
# - Load testing with Locust or k6
# - Database query performance analysis
# - Memory usage profiling
# - Response time metrics collection
```

## ⚠️ Backend Known Gotchas

### Common Backend Pitfalls
```
{{backend_pitfalls}}
# - N+1 query problems
# - Race conditions in concurrent updates
# - Database connection leaks
# - Improper error handling leading to information disclosure
# - Missing input validation
# - Inadequate logging for debugging
```

### Database Specific Considerations
```
{{database_considerations}}
# - Transaction management
# - Migration rollback safety
# - Index optimization
# - Connection pool sizing
# - Database-level constraints vs application-level
```

## 🔄 Backend Execution Context

### Backend Dependencies
```
{{backend_dependencies}}
# - Database server running
# - Redis for caching (if used)
# - Message broker for async tasks
# - External API integrations
```

### Development Setup
```
{{development_setup}}
# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# alembic upgrade head
# uvicorn src.main:app --reload
```

### Deployment Considerations
```
{{deployment_considerations}}
# - Docker containerization
# - Kubernetes deployment manifests
# - Health check endpoints
# - Environment-specific configuration
# - Secret management
```

## 📊 Backend Metrics

### Backend Success Metrics
```
{{backend_metrics}}
# - API response time p95 < 200ms
# - Error rate < 0.1%
# - Database query performance
# - Memory and CPU usage
# - Request throughput capacity
```

### Monitoring & Logging
```
{{monitoring_logging}}
# - Structured JSON logging
# - Request/response logging
# - Error tracking integration
# - Performance metrics collection
# - Health check endpoints
```

---
*PRP Backend Template - Especializado em desenvolvimento de APIs e serviços backend*