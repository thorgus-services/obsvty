# 🔍 PRP - Análise e Refatoração

## 🏷️ Metadados do PRP de Análise
- **PRP ID**: {{prp_id}}
- **Tipo**: Code Analysis & Refactoring
- **Âmbito**: {{scope}} (ex: arquitetural, performance, segurança)
- **Código Alvo**: {{target_code}} (ex: módulo específico, código legado)
- **Complexidade**: {{complexity}}

## 🎯 Business Context Layer

### Analysis Objectives
```
{{analysis_objectives}}
# Exemplo:
# "Analisar e refatorar módulo de autenticação para melhorar performance em 40%, 
# reduzir complexidade ciclomática e eliminar vulnerabilidades de segurança"
```

### Business Impact
- **Risco Atual**: {{current_risk}} (ex: alto custo de manutenção, performance ruim)
- **Benefícios Esperados**: {{expected_benefits}} (ex: redução de bugs, melhor performance)
- **ROI Estimado**: {{estimated_roi}} (ex: 3 meses payback)
- **Prioridade**: {{priority}} (ex: alta - bloqueia novas features)

## 👥 Stakeholder Analysis

### Analysis Stakeholders
```
{{analysis_stakeholders}}
# - Development Team: Precisam de código maintainable
# - Product Owners: Querem reduzir tempo de desenvolvimento
# - QA Team: Precisam de código testável
# - Security Team: Preocupados com vulnerabilidades
# - End Users: Afetados por performance issues
```

## 📋 Analysis Requirement Extraction

### Current State Analysis
```
{{current_state}}
# - Complexidade ciclomática alta (>25)
# - Acoplamento forte entre módulos
# - Duplicação de código significativa
# - Testes frágeis ou ausentes
# - Performance bottlenecks identificados
# - Vulnerabilidades de segurança
```

### Problem Areas Identification
```
{{problem_areas}}
# 1. God classes com muitas responsabilidades
# 2. Métodos muito longos e complexos
# 3. Duplicação de lógica de negócio
# 4. Violações de princípios SOLID
# 5. Dependências circulares
# 6. Testabilidade pobre
```

### Desired Future State
```
{{future_state}}
# - Complexidade ciclomática < 15 por método
# - Coesão alta dentro de módulos
# - Acoplamento baixo entre módulos
# - Cobertura de testes > 80%
# - Performance melhorada em 40%
# - Zero vulnerabilidades críticas
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
# - Principal: {{principal}} (ex: 40 horas de refatoração)
# - Juros: {{interest}} (ex: 2 horas extra por semana de manutenção)
# - Prazo: {{deadline}} (ex: deve ser pago em 2 sprints)
```

## 📝 Analysis Specification Output

### Expected Analysis Deliverables
```
{{analysis_deliverables}}
# 1. Relatório detalhado de análise estática
# 2. Métricas de complexidade antes/depois
# 3. Gráficos de dependência e acoplamento
# 4. Identificação de code smells específicos
# 5. Plano de refatoração priorizado
# 6. Estimativa de esforço para cada refatoração
```

### Refactoring Plan
```
{{refactoring_plan}}
# Fase 1: Refatorações de baixo risco (1-2 dias)
# - Extrair métodos curtos
# - Renomear variáveis para clareza
# - Remover código duplicado
#
# Fase 2: Refatorações estruturais (3-5 dias)
# - Introduzir padrões de design
# - Melhorar estrutura de packages
# - Implementar injeção de dependência
#
# Fase 3: Otimizações (2-3 dias)
# - Performance tuning
# - Memory optimization
# - Cache implementation
```

### Risk Mitigation Strategy
```
{{risk_mitigation}}
# - Refatorar em pequenos incrementos
# - Manter testes passando continuamente
# - Pair programming para mudanças complexas
# - Feature flags para transições graduais
# - Rollback plan para cada refatoração
```

## ✅ Validation Framework

### Analysis Validation Criteria
```
{{validation_criteria}}
# - Complexidade ciclomática reduzida em 50%
# - Cobertura de testes aumentada para > 80%
# - Performance melhorada em 40%
# - Zero regressões funcionais
# - Código mais legível e maintainable
# - Security scan limpo
```

### Testing Strategy for Refactoring
```
{{testing_strategy}}
# - Testes de regressão abrangentes
# - Performance testing comparativo
# - Security penetration testing
# - User acceptance testing
# - Canary deployment para produção
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
# - Refatorar muito de uma vez (big bang)
# - Não ter testes adequados antes de refatorar
# - Introduzir novas dependências desnecessárias
# - Não medir impacto antes/depois
# - Negligenciar aspectos não-funcionais
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

## 🔄 Execution Context

### Pre-requisites for Analysis
```
{{prerequisites}}
# - Codebase checkout and setup
# - Development environment configured
# - Access to monitoring and logging tools
# - Understanding of business domain
# - Knowledge of current pain points
```

### Analysis Tools Setup
```
{{analysis_tools}}
# - SonarQube for static analysis
# - JMeter for performance testing
# - OWASP ZAP for security scanning
# - Code climate for quality metrics
# - Git for version control and blame
```

### Iterative Process
```
{{iterative_process}}
# 1. Analyze small section
# 2. Propose refactoring plan
# 3. Get team review and approval
# 4. Implement refactoring
# 5. Validate with tests
# 6. Measure improvements
# 7. Repeat for next section
```

## 📊 Success Metrics

### Quantitative Improvement Metrics
```
{{improvement_metrics}}
# - Code Complexity: {{complexity_before}} → {{complexity_after}}
# - Test Coverage: {{coverage_before}}% → {{coverage_after}}%
# - Performance: {{perf_before}}ms → {{perf_after}}ms
# - Bug Rate: {{bug_rate_before}} → {{bug_rate_after}}
# - Build Time: {{build_time_before}} → {{build_time_after}}
```

### Qualitative Improvement Assessment
```
{{qualitative_assessment}}
# - Developer happiness survey results
# - Code review feedback improvements
# - Onboarding time for new developers
# - Frequency of production incidents
# - Team confidence in codebase
```

---
*PRP Analysis Template - Especializado em análise de código, identificação de technical debt e planejamento de refatoração*