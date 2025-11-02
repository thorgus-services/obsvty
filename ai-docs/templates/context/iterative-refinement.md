# 🔄 Template de Refinamento Iterativo

## 🏷️ Metadados do Processo Iterativo
- **Process ID**: {{process_id}}
- **Tipo**: Context Refinement
- **Contexto Alvo**: {{target_context}} (ex: PRP específico, documentação)
- **Número de Iterações Planejadas**: {{planned_iterations}}
- **Duração Estimada**: {{estimated_duration}} (ex: 2 horas, 1 sprint)

## 🎯 Objetivo do Refinamento

### Meta Principal
```
{{main_goal}}
# Exemplo:
# "Refinar o PRP de autenticação para garantir especificação completa e sem ambiguidades,
# reduzindo necessidade de retrabalho durante implementação"
```

### Critérios de Sucesso
```
{{success_criteria}}
# - Claridade: Especificação compreensível por todos os stakeholders
# - Completeza: Todos os requisitos funcionais e não-funcionais cobertos
# - Consistência: Sem contradições entre diferentes partes do contexto
# - Mensurável: Critérios de aceitação quantificáveis
# - Testável: Possibilidade de verificação automática
```

## 🔍 Fase 1: Análise Inicial

### Contexto Atual
```
{{current_context}}
# Estado atual do contexto/PRP/documentação
# Pontos fortes identificados
# Lacunas e ambiguidades detectadas
# Áreas que necessitam clarificação
```

### Identificação de Problemas
```
{{problem_identification}}
# 1. Requisitos ambíguos ou subjetivos
# 2. Informações técnicas missing
# 3. Dependências não mapeadas
# 4. Casos de borda não considerados
# 5. Conflitos entre diferentes partes do contexto
```

### Stakeholders para Consulta
```
{{consultation_stakeholders}}
# - Product Owner: Para clarificar requisitos de negócio
# - Tech Lead: Para validar viabilidade técnica
# - QA Team: Para definir critérios de aceitação
# - UX Designer: Para especificações de interface
# - DevOps: Para requisitos de infraestrutura
```

## 🛠️ Fase 2: Estratégia de Refinamento

### Técnicas de Refinamento
```
{{refinement_techniques}}
# - 5 Whys: Para chegar à raiz dos problemas
# - Example Mapping: Para clarificar requisitos com exemplos
# - Behavior Driven Development: Para especificação por comportamento
# - Decision Records: Para documentar escolhas técnicas
# - Peer Review: Para validação cruzada
```

### Ferramentas de Apoio
```
{{support_tools}}
# - Miro/FigJam: Para sessões colaborativas
# - Confluence/Notion: Para documentação
# - JIRA/Trello: Para tracking de tasks
# - Slack/Teams: Para comunicação
# - Version Control: Para histórico de mudanças
```

### Plano de Iterações
```
{{iteration_plan}}
# Iteração 1: Foco em requisitos funcionais principais
# Iteração 2: Adicionar requisitos não-funcionais
# Iteração 3: Especificar casos de borda e exceções
# Iteração 4: Validação final com todos stakeholders
# Iteração 5: Ajustes finais e aprovação
```

## 📝 Fase 3: Execução Iterativa

### Template de Sessão de Refinamento
```
{{refinement_session}}
# Data: {{date}}
# Participantes: {{participants}}
# Objetivo da Sessão: {{session_goal}}
#
# Discussões:
# - Tópico 1: {{discussion_1}}
# - Decisão: {{decision_1}}
# - Ações: {{action_1}}
#
# - Tópico 2: {{discussion_2}}
# - Decisão: {{decision_2}}
# - Ações: {{action_2}}
```

### Registro de Mudanças
```
{{change_log}}
# Iteração {{iteration_number}} - {{date}}
# - Adicionado: {{added_items}}
# - Removido: {{removed_items}}
# - Modificado: {{modified_items}}
# - Clarificado: {{clarified_items}}
# - Validado: {{validated_items}}
```

### Checklist de Validação por Iteração
```
{{validation_checklist}}
# [ ] Todos os requisitos estão claros e não-ambíguos?
# [ ] Casos de uso principais estão cobertos?
# [ ] Requisitos não-funcionais estão especificados?
# [ ] Dependências estão mapeadas?
# [ ] Critérios de aceitação são mensuráveis?
# [ ] Documentação está consistente?
```

## 🔄 Fase 4: Processo de Feedback

### Mecanismos de Coleta de Feedback
```
{{feedback_mechanisms}}
# - Revisões formais com stakeholders
# - Sessões de pairing para validação técnica
# - Prototipagem rápida para feedback de UX
# - Spike técnico para validação de viabilidade
# - Documentos compartilhados para comentários assíncronos
```

### Template de Solicitação de Feedback
```
{{feedback_request}}
# Contexto: {{context_description}}
# Área Específica: {{specific_area}}
# Tipo de Feedback Necessário: {{feedback_type}} (ex: técnico, negócio, UX)
# Prazo para Feedback: {{feedback_deadline}}
# Formato Preferido: {{feedback_format}} (ex: comentários no doc, reunião)
```

### Processamento de Feedback
```
{{feedback_processing}}
# 1. Coletar todo feedback recebido
# 2. Categorizar por tipo e urgência
# 3. Priorizar based on impact
# 4. Incorporar changes no contexto
# 5. Documentar decisões tomadas
# 6. Comunicar mudanças aos stakeholders
```

## 📊 Fase 5: Métricas de Progresso

### Indicadores de Qualidade do Contexto
```
{{quality_indicators}}
# - Completeness Score: {{completeness}}%
# - Clarity Index: {{clarity_score}}
# - Consistency Metric: {{consistency}}
# - Stakeholder Confidence: {{confidence}}%
# - Ambiguity Count: {{ambiguity_count}}
```

### Velocidade de Refinamento
```
{{refinement_velocity}}
# - Iterações Completadas: {{completed_iterations}}
# - Tempo Médio por Iteração: {{avg_time_per_iteration}}
# - Issues Resolvidas por Iteração: {{issues_resolved}}
# - Feedback Incorporação Rate: {{feedback_incorporation}}%
```

### ROI do Processo Iterativo
```
{{roi_calculation}}
# - Tempo Investido: {{time_invested}} horas
# - Retrabalho Evitado: {{rework_avoided}} horas
# - Bugs Prevenidos: {{bugs_prevented}}
# - ROI: {{roi}} (ex: 3:1 - para cada hora investida, 3 horas economizadas)
```

## 🚨 Fase 6: Gestão de Riscos

### Riscos do Processo Iterativo
```
{{process_risks}}
# - Analysis Paralysis: Refinar demais sem progresso
# - Scope Creep: Adicionar requisitos não essenciais
# - Stakeholder Disengagement: Perda de interesse
# - Inconsistências: Introduzir contradições
# - Time Sink: Gastar tempo desproporcional
```

### Mitigation Strategies
```
{{mitigation_strategies}}
# - Timeboxing: Limitar tempo por iteração
# - Minimum Viable Context: Focar no essencial primeiro
# - Regular Check-ins: Manter stakeholders engajados
# - Decision Log: Documentar para evitar revisitação
# - Exit Criteria: Definir quando parar de refinar
```

### Critérios de Saída
```
{{exit_criteria}}
# [ ] Todos os stakeholders aprovaram?
# [ ] Critérios de aceitação estão definidos?
# [ ] Requisitos não-funcionais estão cobertos?
# [ ] Dependências estão mapeadas?
# [ ] Riscos técnicos estão identificados?
# [ ] Plano de implementação está claro?
```

## 📋 Fase 7: Documentação Final

### Template de Relatório de Refinamento
```
{{refinement_report}}
# Resumo do Processo:
# - Iterações Realizadas: {{iterations_done}}
# - Tempo Total: {{total_time}} horas
# - Principais Melhorias: {{key_improvements}}
# - ROI Estimado: {{estimated_roi}}
#
# Estado Final do Contexto:
# - Completeness: {{final_completeness}}%
# - Clarity: {{final_clarity_score}}
# - Stakeholder Satisfaction: {{satisfaction}}%
#
# Lições Aprendidas: {{lessons_learned}}
```

### Checklist de Finalização
```
{{completion_checklist}}
# [ ] Contexto versionado e armazenado
# [ ] Histórico de mudanças documentado
# [ ] Approvals coletados de todos stakeholders
# [ ] Plano de comunicação das mudanças
# [ ] Setup para monitoramento contínuo
# [ ] Processo definido para futuros refinamentos
```

---
*Template de Refinamento Iterativo - Para evolução contínua e melhoria de contextos através de ciclos estruturados de feedback*