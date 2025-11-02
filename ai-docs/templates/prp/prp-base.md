# 📋 Product Requirements Prompt (PRP) - Template Base

## 🏷️ Metadados do PRP
- **PRP ID**: {{prp_id}}
- **Versão**: 1.0.0
- **Data de Criação**: {{creation_date}}
- **Autor**: {{author}}
- **Status**: {{status}} (draft/review/approved/executed)
- **Complexidade**: {{complexity}} (baixa/média/alta)
- **Esforço Estimado**: {{estimated_effort}}

## 🎯 Business Context Layer
*Traduz requisitos de negócio para contexto técnico*

### Business Problem Statement
```
{{business_problem}}
# Exemplo:
# "Usuários precisam gerenciar seu perfil de forma autônoma, mas a atual 
# implementação requer intervenção do suporte técnico para atualizações simples"
```

### Business Objectives
- **Objetivo Primário**: {{primary_objective}}
- **Objetivos Secundários**: {{secondary_objectives}}
- **Resultados Esperados**: {{expected_outcomes}}
- **Métricas de Sucesso**: {{success_metrics}}

### Value Proposition
```
{{value_proposition}}
# Exemplo:
# "Reduzir tempo de resolução de 48h para 2h, diminuindo custos de suporte 
# em 40% e aumentando satisfação do usuário"
```

## 👥 Stakeholder Analysis
*Identifica todas as partes interessadas e suas necessidades*

### Key Stakeholders
```
{{stakeholders}}
# Exemplo:
# - Usuários Finais: Necessitam de self-service para gestão de perfil
# - Equipe de Suporte: Quer reduzir tickets de suporte
# - Product Owners: Buscam melhorar métricas de satisfação
# - Desenvolvedores: Precisam de requisitos claros e técnicos
```

### Stakeholder Requirements
- **Requisitos Funcionais**: {{functional_requirements}}
- **Requisitos Não-Funcionais**: {{non_functional_requirements}}
- **Restrições de Negócio**: {{business_constraints}}
- **Expectativas de UX**: {{ux_expectations}}

### Priority Matrix
```
{{priority_matrix}}
# Exemplo:
# | Requisito | Prioridade | Impacto | Esforço |
# |----------|------------|---------|---------|
# | CRUD Perfil | Alta | Alto | Médio |
# | Validação Email | Média | Médio | Baixo |
```

## 📋 Requirement Extraction
*Extrai e estrutura requisitos executáveis*

### User Stories
```
{{user_stories}}
# Exemplo:
# Como [usuário], quero [editar meu perfil] para [atualizar informações pessoais]
# Critérios de Aceitação:
# - Deve validar email formatado corretamente
# - Deve persistir alterações no banco de dados
# - Deve retornar feedback visual de sucesso/erro
```

### Technical Requirements
- **Requisitos de Frontend**: {{frontend_requirements}}
- **Requisitos de Backend**: {{backend_requirements}}
- **Requisitos de Banco de Dados**: {{database_requirements}}
- **Requisitos de Infraestrutura**: {{infrastructure_requirements}}

### Edge Cases & Error Conditions
```
{{edge_cases}}
# Exemplo:
# - Usuário tenta salvar perfil com email duplicado
# - Conexão com banco de dados falha durante atualização
# - Usuário tenta acessar perfil de outro usuário
```

## 🔧 Technical Translation
*Traduz requisitos para especificações técnicas executáveis*

### Architecture Decisions
```
{{architecture_decisions}}
# Exemplo:
# - Pattern: Controller-Service-Repository
# - API: RESTful com JSON
# - Autenticação: JWT tokens
# - Banco: PostgreSQL com SQLAlchemy ORM
```

### Technology Stack
- **Linguagens**: {{languages}}
- **Frameworks**: {{frameworks}}
- **Bibliotecas**: {{libraries}}
- **Ferramentas**: {{tools}}

### Data Models & Schema
```
{{data_models}}
# Exemplo:
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
# Exemplo:
# GET /api/users/{id}
# PUT /api/users/{id}
# Request/Response examples with status codes
```

## 📝 Specification Output
*Define o formato e estrutura da saída esperada*

### Expected Deliverables
- **Código Fonte**: {{source_code_requirements}}
- **Documentação**: {{documentation_requirements}}
- **Testes**: {{testing_requirements}}
- **Configurações**: {{configuration_requirements}}

### Output Structure
```
{{output_structure}}
# Exemplo:
# 1. Implementação completa do endpoint
# 2. Testes unitários e de integração
# 3. Documentação da API (OpenAPI)
# 4. Scripts de migração de banco
# 5. Exemplos de uso
```

### Code Standards & Conventions
```
{{code_standards}}
# Exemplo:
# - Follow PEP8 for Python
# - Use type hints consistently
# - Write docstrings for all functions
# - Include error handling
```

## ✅ Validation Framework
*Estabelece critérios de validação e teste*

### Testing Strategy
- **Testes Unitários**: {{unit_testing_requirements}}
- **Testes de Integração**: {{integration_testing_requirements}}
- **Testes End-to-End**: {{e2e_testing_requirements}}
- **Testes de Performance**: {{performance_testing_requirements}}

### Quality Gates
```
{{quality_gates}}
# Exemplo:
# - 100% dos testes passando
# - Cobertura de testes > 80%
# - Zero vulnerabilidades de segurança críticas
# - Linting score 10/10
```

### Validation Checklist
- [ ] **Funcionalidade**: Todos os requisitos implementados
- [ ] **Qualidade**: Código segue padrões estabelecidos
- [ ] **Performance**: Atende requisitos não-funcionais
- [ ] **Segurança**: Sem vulnerabilidades conhecidas
- [ ] **Usabilidade**: Experiência do usuário validada

### Automated Validation
```
{{automated_validation}}
# Exemplo:
# - Run pytest with coverage
# - Execute security scan (bandit/safety)
# - Run linter (flake8/black)
# - Performance testing (locust)
```

## ⚠️ Known Gotchas & Risks
*Identifica armadilhas conhecidas e riscos potenciais*

### Technical Risks
```
{{technical_risks}}
# Exemplo:
# - Complexidade de validação de email único
# - Performance em atualizações concorrentes
# - Migração de dados existentes
```

### Mitigation Strategies
```
{{mitigation_strategies}}
# Exemplo:
# - Implementar locking otimista para concorrência
# - Criar índices adequados no banco
# - Testar com carga simulada
```

### Dependencies & Assumptions
```
{{dependencies}}
# Exemplo:
# - Assume serviço de email configurado
# - Dependente de módulo de autenticação
# - Requer PostgreSQL 14+
```

## 🔄 Execution Context
*Contexto adicional para execução do PRP*

### Related Contexts
```
{{related_contexts}}
# Exemplo:
# - Contexto de Autenticação JWT
# - Contexto de Padrões de API RESTful
# - Contexto de Boas Práticas Python
```

### Environment Setup
```
{{environment_setup}}
# Exemplo:
# - Python 3.11+
# - PostgreSQL running locally
# - Environment variables for configuration
```

### References & Documentation
```
{{references}}
# Exemplo:
# - Link para documentação do FastAPI
# - Exemplos de implementações similares
# - Guia de estilo da equipe
```

## 📊 Metrics & Monitoring
*Métricas para medir sucesso do PRP*

### Success Metrics
- **Taxa de Sucesso**: {{success_rate}}
- **Tempo de Desenvolvimento**: {{development_time}}
- **Qualidade do Código**: {{code_quality}}
- **Satisfação do Usuário**: {{user_satisfaction}}

### Monitoring Requirements
```
{{monitoring_requirements}}
# Exemplo:
# - Log de execuções bem-sucedidas
# - Métricas de performance da API
# - Monitoring de errors/exceptions
```

## 📋 Approval & Sign-off

### PRP Reviewers
- **Product Owner**: {{product_owner}}
- **Tech Lead**: {{tech_lead}}
- **QA Engineer**: {{qa_engineer}}

### Approval Status
- [ ] **✅ Product Owner Approval**
- [ ] **✅ Technical Review**
- [ ] **✅ QA Review**
- [ ] **✅ Ready for Execution**

### Execution History
| Data Execução | Versão | Executor | Resultado | Métricas |
|---------------|--------|----------|-----------|----------|
| {{exec_date}} | {{version}} | {{executor}} | {{result}} | {{metrics}} |

---
*PRP Base Template - Garantindo sucesso em uma única passagem através de contexto comprehensive*