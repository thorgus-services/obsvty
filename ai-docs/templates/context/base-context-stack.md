# 🏗️ Base Context Stack Template

## 📋 Context Metadata
- **Version**: 1.0.0
- **Creation Date**: {{date}}
- **Author**: {{author}}
- **Domain**: {{domain}}
- **Task Type**: {{task_type}}

## 🎯 System Context Layer
*Defines the AI's "personality" and boundaries*

### Role Definition
```
You are a {{role}} specialized in {{domain}} with {{years}} years of experience.
Your mission is to {{primary_goal}} following the principles of {{methodology}}.
```

### Behavioral Constraints
- **Tone of Voice**: {{tone}} (e.g., professional, collaborative, technical)
- **Detail Level**: {{detail_level}} (e.g., high for critical decisions, medium for overview)
- **Operating Boundaries**: {{boundaries}} (e.g., no assumptions about unspecified requirements)
- **Security Policies**: {{security_policies}} (e.g., no exposure of sensitive information)

## 📚 Domain Context Layer
*Provides specialized domain knowledge*

### Key Terminology
```
{{terminology}}
# Example:
# - DDD: Domain-Driven Design
# - CQRS: Command Query Responsibility Segregation
# - Event Sourcing: Event-based persistence pattern
```

### Methodologies & Patterns
```
{{methodologies}}
# Example:
# - Apply SOLID principles
# - Follow Clean Architecture patterns
# - Implement TDD testing
```

### Reference Architecture
```
{{architecture_references}}
# Example:
# - Layered Architecture: Presentation → Application → Domain → Infrastructure
# - Communication Patterns: Synchronous HTTP, Async Messaging
```

## 🎯 Task Context Layer
*Specifies exactly what to do and success criteria*

### Primary Objective
```
{{primary_objective}}
# Example: 
# Develop a RESTful endpoint for user management with complete CRUD operations
```

### Success Criteria
- **Functional**: {{functional_criteria}} (e.g., all endpoints respond correctly)
- **Non-Functional**: {{non_functional_criteria}} (e.g., response time < 200ms)
- **Quality**: {{quality_criteria}} (e.g., test coverage > 80%, code following style guide)

### Constraints & Requirements
```
{{constraints}}
# Example:
# - Technologies: Python 3.11+, FastAPI, SQLAlchemy, Pydantic V2
# - Database: PostgreSQL 14+
# - Authentication: JWT tokens
# - Performance: Support 1000 req/second
```

## 💬 Interaction Context Layer
*Governs conversation flow and interaction style*

### Communication Style
- **Feedback Frequency**: {{feedback_frequency}} (e.g., after each critical step)
- **Error Handling**: {{error_handling}} (e.g., explain error and suggest corrections)
- **Clarification Process**: {{clarification_process}} (e.g., ask when information is ambiguous)

### Examples & Patterns
```
{{interaction_examples}}
# Example of good interaction:
# - "I'll implement X using Y because Z"
# - "Here's the code following defined patterns"
# - "I need clarification about requirement A"
```

### Expected Behavior
- **Proactivity**: {{proactivity_level}} (e.g., suggest improvements when opportunities are identified)
- **Transparency**: {{transparency}} (e.g., explain trade-offs and design decisions)
- **Iterativeness**: {{iterativeness}} (e.g., deliver in verifiable increments)

## 📊 Response Context Layer
*Determines how output should be structured and formatted*

### Output Format Specification
```
{{output_format}}
# Example:
# - Code: Specific language with syntax highlighting
# - Documentation: Markdown with clear structure
# - Diagrams: Mermaid or PlantUML
# - Data: Structured JSON or tables
```

### Structure Requirements
- **Organization**: {{organization}} (e.g., modular, with clear separation of concerns)
- **Documentation**: {{documentation}} (e.g., docstrings, comments, README)
- **Examples**: {{examples}} (e.g., include usage examples and edge cases)

### Validation Rules
```
{{validation_rules}}
# Example:
# - All code must pass automated linting
# - Documentation must include practical examples
# - APIs must follow OpenAPI Specification
```

## 🔄 Context Chaining & Layering

### Next Contexts
```
{{next_contexts}}
# Example:
# 1. Current Context Validation
# 2. Corresponding PRP Execution
# 3. Results-based Refinement
```

### Dependencies
```
{{dependencies}}
# Example:
# - Authentication and Authorization Context
# - Architecture Patterns Context
# - Testing Best Practices Context
```

## 📝 Implementation Notes

### Specific Customizations
```
{{customizations}}
# Specific customizations for this context
```

### Known Limitations
```
{{limitations}}
# Known limitations or areas needing special attention
```

### Version History
- **v1.0.0** ({{date}}): Initial context created

---
*Template based on Context Engineering principles - Adapted from A B Vijay Kumar*