# 📋 Product Requirements Prompt (PRP) - Base Template

## 🏷️ PRP Metadata
- **PRP ID**: {{prp_id}}
- **Version**: 1.0.0
- **Creation Date**: {{creation_date}}
- **Author**: {{author}}
- **Status**: {{status}} (draft/review/approved/executed)
- **Complexity**: {{complexity}} (low/medium/high)
- **Estimated Effort**: {{estimated_effort}}

## 🎯 Business Context Layer
*Translates business requirements into technical context*

### Business Problem Statement
```
{{business_problem}}
# Example:
# "Users need to manage their profile autonomously, but the current 
# implementation requires technical support intervention for simple updates"
```

### Business Objectives
- **Primary Objective**: {{primary_objective}}
- **Secondary Objectives**: {{secondary_objectives}}
- **Expected Outcomes**: {{expected_outcomes}}
- **Success Metrics**: {{success_metrics}}

### Value Proposition
```
{{value_proposition}}
# Example:
# "Reduce resolution time from 48h to 2h, decreasing support costs 
# by 40% and increasing user satisfaction"
```

## 👥 Stakeholder Analysis
*Identifies all stakeholders and their needs*

### Key Stakeholders
```
{{stakeholders}}
# Example:
# - End Users: Need self-service for profile management
# - Support Team: Want to reduce support tickets
# - Product Owners: Seek to improve satisfaction metrics
# - Developers: Need clear and technical requirements
```

### Stakeholder Requirements
- **Functional Requirements**: {{functional_requirements}}
- **Non-Functional Requirements**: {{non_functional_requirements}}
- **Business Constraints**: {{business_constraints}}
- **UX Expectations**: {{ux_expectations}}

### Priority Matrix
```
{{priority_matrix}}
# Example:
# | Requirement | Priority | Impact | Effort |
# |------------|----------|--------|--------|
# | Profile CRUD | High | High | Medium |
# | Email Validation | Medium | Medium | Low |
```

## 📋 Requirement Extraction
*Extracts and structures executable requirements*

### User Stories
```
{{user_stories}}
# Example:
# As a [user], I want to [edit my profile] to [update personal information]
# Acceptance Criteria:
# - Must validate properly formatted email
# - Must persist changes in the database
# - Must return visual feedback for success/error
```

### Technical Requirements
- **Frontend Requirements**: {{frontend_requirements}}
- **Backend Requirements**: {{backend_requirements}}
- **Database Requirements**: {{database_requirements}}
- **Infrastructure Requirements**: {{infrastructure_requirements}}

### Edge Cases & Error Conditions
```
{{edge_cases}}
# Example:
# - User tries to save profile with duplicate email
# - Database connection fails during update
# - User attempts to access another user's profile
```

## 🔧 Technical Translation
*Translates requirements into executable technical specifications*

### Architecture Decisions
```
{{architecture_decisions}}
# Example:
# - Pattern: Controller-Service-Repository
# - API: RESTful with JSON
# - Authentication: JWT tokens
# - Database: PostgreSQL with SQLAlchemy ORM
```

### Technology Stack
- **Languages**: {{languages}}
- **Frameworks**: {{frameworks}}
- **Libraries**: {{libraries}}
- **Tools**: {{tools}}

### Data Models & Schema
```
{{data_models}}
# Example:
# User:
# - id: UUID (primary key)
# - email: String (unique, not null)
# - name: String (not null)
# - created_at: DateTime
# - updated_at: DateTime
```

### API Specifications
```
{{api_specs}}
# Example:
# GET /api/users/{id}
# PUT /api/users/{id}
# Request/Response examples with status codes
```

## 📝 Specification Output
*Defines the expected output format and structure*

### Expected Deliverables
- **Source Code**: {{source_code_requirements}}
- **Documentation**: {{documentation_requirements}}
- **Tests**: {{testing_requirements}}
- **Configurations**: {{configuration_requirements}}

### Output Structure
```
{{output_structure}}
# Example:
# 1. Complete endpoint implementation
# 2. Unit and integration tests
# 3. API documentation (OpenAPI)
# 4. Database migration scripts
# 5. Usage examples
```

### Code Standards & Conventions
```
{{code_standards}}
# Example:
# - Follow PEP8 for Python
# - Use type hints consistently
# - Write docstrings for all functions
# - Include error handling
```

## ✅ Validation Framework
*Establishes validation and testing criteria*

### Testing Strategy
- **Unit Tests**: {{unit_testing_requirements}}
- **Integration Tests**: {{integration_testing_requirements}}
- **End-to-End Tests**: {{e2e_testing_requirements}}
- **Performance Tests**: {{performance_testing_requirements}}

### Quality Gates
```
{{quality_gates}}
# Example:
# - 100% passing tests
# - Test coverage > 80%
# - Zero critical security vulnerabilities
# - Linting score 10/10
```

### Validation Checklist
- [ ] **Functionality**: All requirements implemented
- [ ] **Quality**: Code follows established standards
- [ ] **Performance**: Meets non-functional requirements
- [ ] **Security**: No known vulnerabilities
- [ ] **Usability**: User experience validated

### Automated Validation
```
{{automated_validation}}
# Example:
# - Run pytest with coverage
# - Execute security scan (bandit/safety)
# - Run linter (flake8/black)
# - Performance testing (locust)
```

## ⚠️ Known Pitfalls
*Identifies potential issues and mitigation strategies*

### Common Challenges
```
{{common_challenges}}
# Example:
# - Complex state management in UI
# - Race conditions in concurrent updates
# - Performance bottlenecks in queries
# - Security vulnerabilities in input validation
```

### Risk Mitigation
```
{{risk_mitigation}}
# Example:
# - Implement proper state management library
# - Use database transactions and locks
# - Optimize queries and add caching
# - Validate all inputs server-side
```

## 🔄 Execution Context
*Defines the implementation environment and constraints*

### Pre-requisites
```
{{prerequisites}}
# Example:
# - Development environment setup
# - Database server running
# - Required dependencies installed
# - Access to necessary APIs
```

### Development Setup
```
{{development_setup}}
# Example:
# - Clone repository
# - Install dependencies
# - Configure environment variables
# - Run database migrations
```

### Deployment Considerations
```
{{deployment_considerations}}
# Example:
# - CI/CD pipeline configuration
# - Environment-specific settings
# - Monitoring and logging setup
# - Backup and recovery procedures
```

## 📊 Success Metrics
*Defines how success will be measured*

### Performance Metrics
```
{{performance_metrics}}
# Example:
# - Response time < 200ms
# - Error rate < 0.1%
# - CPU usage < 70%
# - Memory usage < 80%
```

### Business Metrics
```
{{business_metrics}}
# Example:
# - Support ticket reduction
# - User satisfaction increase
# - Time to resolution decrease
# - Cost savings achieved
```

---
*Base PRP Template - Provides a comprehensive framework for technical requirement specification*