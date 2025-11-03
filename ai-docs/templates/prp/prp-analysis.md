# 🔍 PRP - Analysis and Refactoring

## 🏷️ Analysis PRP Metadata
- **PRP ID**: {{prp_id}}
- **Type**: Code Analysis & Refactoring
- **Scope**: {{scope}} (e.g.: architectural, performance, security)
- **Target Code**: {{target_code}} (e.g.: specific module, legacy code)
- **Complexity**: {{complexity}}

## 🎯 Business Context Layer

### Analysis Objectives
```
{{analysis_objectives}}
# Example:
# "Analyze and refactor authentication module to improve performance by 40%, 
# reduce cyclomatic complexity and eliminate security vulnerabilities"
```

### Business Impact
- **Current Risk**: {{current_risk}} (e.g.: high maintenance cost, poor performance)
- **Expected Benefits**: {{expected_benefits}} (e.g.: bug reduction, better performance)
- **Estimated ROI**: {{estimated_roi}} (e.g.: 3 months payback)
- **Priority**: {{priority}} (e.g.: high - blocks new features)

## 👥 Stakeholder Analysis

### Analysis Stakeholders
```
{{analysis_stakeholders}}
# - Development Team: Need maintainable code
# - Product Owners: Want reduced development time
# - QA Team: Need testable code
# - Security Team: Concerned with vulnerabilities
# - End Users: Affected by performance issues
```

## 📋 Analysis Requirement Extraction

### Current State Analysis
```
{{current_state}}
# - High cyclomatic complexity (>25)
# - Strong coupling between modules
# - Significant code duplication
# - Fragile or missing tests
# - Identified performance bottlenecks
# - Security vulnerabilities
```

### Problem Areas Identification
```
{{problem_areas}}
# 1. God classes with many responsibilities
# 2. Very long and complex methods
# 3. Business logic duplication
# 4. SOLID principles violations
# 5. Circular dependencies
# 6. Poor testability
```

### Desired Future State
```
{{future_state}}
# - Cyclomatic complexity < 15 per method
# - High cohesion within modules
# - Low coupling between modules
# - Test coverage > 80%
# - Performance improved by 40%
# - Zero critical vulnerabilities
```

## 🔧 Technical Translation

### Analysis Methodology
```
{{analysis_methodology}}
# 1. Static Code Analysis (SonarQube, ESLint, Pylint)
# 2. Complexity Metrics (cyclomatic, cognitive)
# 3. Dependency Graph Analysis
# 4. Performance Profiling
# 5. Security Vulnerability Scan
# 6. Test Coverage Analysis
```

### Refactoring Patterns
```
{{refactoring_patterns}}
# - Extract Method
# - Extract Class
# - Introduce Parameter Object
# - Replace Conditional with Polymorphism
# - Introduce Strategy Pattern
# - Apply Dependency Injection
# - Implement Repository Pattern
```

### Technical Debt Assessment
```
{{technical_debt}}
# - Principal: {{principal}} (e.g.: 40 hours of refactoring)
# - Interest: {{interest}} (e.g.: 2 extra hours per week of maintenance)
# - Deadline: {{deadline}} (e.g.: must be paid in 2 sprints)
```

## 📝 Analysis Specification Output

### Expected Analysis Deliverables
```
{{analysis_deliverables}}
# 1. Detailed static analysis report
# 2. Before/after complexity metrics
# 3. Dependency and coupling graphs
# 4. Specific code smells identification
# 5. Prioritized refactoring plan
# 6. Effort estimation for each refactoring
```

### Refactoring Plan
```
{{refactoring_plan}}
# Phase 1: Low-risk refactorings (1-2 days)
# - Extract short methods
# - Rename variables for clarity
# - Remove duplicate code
#
# Phase 2: Structural refactorings (3-5 days)
# - Introduce design patterns
# - Improve package structure
# - Implement dependency injection
#
# Phase 3: Optimizations (2-3 days)
# - Performance tuning
# - Memory optimization
# - Cache implementation
```

### Risk Mitigation Strategy
```
{{risk_mitigation}}
# - Refactor in small increments
# - Keep tests passing continuously
# - Pair programming for complex changes
# - Feature flags for gradual transitions
# - Rollback plan for each refactoring
```

## ✅ Validation Framework

### Analysis Validation Criteria
```
{{validation_criteria}}
# - Cyclomatic complexity reduced by 50%
# - Test coverage increased to > 80%
# - Performance improved by 40%
# - Zero functional regressions
# - More readable and maintainable code
# - Clean security scan
```

### Testing Strategy for Refactoring
```
{{testing_strategy}}
# - Comprehensive regression testing
# - Comparative performance testing
# - Security penetration testing
# - User acceptance testing
# - Canary deployment to production
```

### Quality Metrics Tracking
```
{{quality_metrics}}
# - Maintainability Index
# - Code Coverage Percentage
# - Bug Count Reduction
# - Cycle Time Improvement
# - Team Velocity Impact
```

## ⚠️ Known Analysis Challenges

### Common Refactoring Pitfalls
```
{{refactoring_pitfalls}}
# - Refactoring too much at once (big bang)
# - Not having adequate tests before refactoring
# - Introducing unnecessary new dependencies
# - Not measuring before/after impact
# - Neglecting non-functional aspects
```

### Risk Areas
```
{{risk_areas}}
# - Complex business logic with subtle edge cases
# - Poorly documented external dependencies
# - Legacy code with missing tests
# - Performance-critical sections
# - Security-sensitive functionality
```