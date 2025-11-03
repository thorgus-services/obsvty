# 🚀 PRP - Backend Development

## 🏷️ Backend PRP Metadata
- **PRP ID**: {{prp_id}}
- **Type**: Backend Development
- **Domain**: {{domain}} (e.g.: API, Microservice, Database)
- **Technology**: {{technology}} (e.g.: Python/FastAPI, Node.js/Express)
- **Complexity**: {{complexity}}

## 🎯 Business Context Layer

### Backend Business Objectives
```
{{backend_objectives}}
# Example:
# "Develop RESTful API for user management that reduces response time 
# by 50% and supports 1000 req/second with 99.9% availability"
```

### SLAs & Performance Requirements
- **Availability**: {{availability}} (e.g.: 99.9%)
- **Latency**: {{latency}} (e.g.: < 200ms p95)
- **Throughput**: {{throughput}} (e.g.: 1000 req/sec)
- **Scalability**: {{scalability}} (e.g.: horizontal scaling)

## 👥 Stakeholder Analysis

### Backend Stakeholders
```
{{backend_stakeholders}}
# - Mobile Developers: Consume RESTful APIs
# - Web Frontend: Uses JSON endpoints
# - DevOps: Need health checks and metrics
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
- **DBMS**: {{database}} (e.g.: PostgreSQL, MySQL, MongoDB)
- **Migrations**: {{migrations}} (e.g.: Alembic, Flyway)
- **Indexes**: {{indexes}} (e.g.: email unique index)
- **Constraints**: {{constraints}} (e.g.: foreign keys, not null)

## 🔧 Backend Technical Translation

### Architecture Pattern
```
{{architecture_pattern}}
# Example for Python/FastAPI:
# - Pattern: Controller-Service-Repository
# - Controllers: FastAPI routers with dependency injection
# - Services: Business logic with unit tests
# - Repositories: Database operations with SQLAlchemy
# - Models: Pydantic schemas for validation
```

### Technology Stack Specifics
- **Framework**: {{framework}} (e.g.: FastAPI, Express.js, Spring Boot)
- **ORM/ODM**: {{orm}} (e.g.: SQLAlchemy, Mongoose, TypeORM)
- **Validation**: {{validation}} (e.g.: Pydantic, Joi, class-validator)
- **Authentication**: {{auth}} (e.g.: JWT, OAuth2, API keys)

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
# ├── repositories/        # Data access
# │   ├── user_repository.py
# │   └── __init__.py
# ├── models/             # Database models
# │   ├── user_model.py
# │   └── __init__.py
# ├── schemas/            # Pydantic schemas
# │   ├── user_schema.py
# │   └── __init__.py
# └── config.py           # Configuration
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
# - Memory leaks in long-running processes
# - Connection pool exhaustion
# - Improper error handling
# - Missing database indexes
# - Inadequate input validation
```

### Risk Areas
```
{{risk_areas}}
# - High-traffic endpoints
# - Complex database queries
# - Authentication flows
# - File upload handling
# - External service integration
# - Concurrent operations
```

## 🔄 Execution Context

### Backend Pre-requisites
```
{{backend_prerequisites}}
# - Development environment setup
# - Database server running
# - Required dependencies installed
# - Environment variables configured
# - Access to external services
```

### Development Tools Setup
```
{{development_tools}}
# - IDE with Python/FastAPI support
# - Database management tool
# - API testing tool (Postman, Insomnia)
# - Git for version control
# - Docker for containerization
```

### Iterative Development Process
```
{{iterative_process}}
# 1. Implement API endpoint
# 2. Write tests
# 3. Add validation
# 4. Implement business logic
# 5. Test performance
# 6. Document changes
# 7. Code review
```

## 📊 Success Metrics

### Backend Performance Metrics
```
{{performance_metrics}}
# - Response time < 200ms (p95)
# - Error rate < 0.1%
# - CPU usage < 70%
# - Memory usage < 80%
# - Database query time < 100ms
```

### Quality & Reliability Metrics
```
{{quality_metrics}}
# - Test coverage > 80%
# - Zero critical security issues
# - Documentation coverage 100%
# - API versioning maintained
# - Successful CI/CD builds
```

---
*Backend PRP Template - Specialized in backend development with focus on performance, scalability, and maintainability*