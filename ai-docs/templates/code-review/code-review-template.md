# 📋 Code Review Template - Context Engineering

## 🏷️ Review Metadata
- **PRP ID**: {{prp_id}}
- **Context**: {{context_name}}
- **Author**: {{author}}
- **Reviewer**: {{reviewer}}
- **Date**: {{review_date}}
- **Status**: {{status}}

## 🎯 SOLID-Based Review Criteria
- [ ] **Single Responsibility**: Does each class/function have a single responsibility?
- [ ] **Open/Closed**: Is the code open for extension, closed for modification?
- [ ] **Liskov Substitution**: Do subtypes substitute their base types?
- [ ] **Interface Segregation**: Are interfaces specific rather than general?
- [ ] **Dependency Inversion**: Does it depend on abstractions, not implementations?

## 🏗️ Architecture (Hexagonal/Clean)
- [ ] **Separation of Concerns**: Are layers well defined?
- [ ] **Ports & Adapters**: Are interfaces clear for integrations?
- [ ] **Dependency Direction**: Do dependencies point towards the center?
- [ ] **Testability**: Is it easy to mock and test?

## 🧪 Testing & Quality
- [ ] **Coverage**: >90% coverage for critical code?
- [ ] **Unit Tests**: Is business logic tested in isolation?
- [ ] **Integration Tests**: Are integrations adequately tested?
- [ ] **Edge Cases**: Are edge cases covered?
- [ ] **Performance**: Are load tests performed for critical endpoints?

## 🔒 Security
- [ ] **Input Validation**: Are all inputs validated?
- [ ] **Authentication**: Is JWT validation implemented?
- [ ] **Authorization**: Is access control adequate?
- [ ] **Data Sanitization**: Are data sanitized before processing?

## 📊 Performance
- [ ] **Response Time**: Within established limits?
- [ ] **Database Queries**: Are queries optimized and indexed?
- [ ] **Caching**: Is caching implemented where appropriate?
- [ ] **Concurrency**: Is concurrency handled properly?

## 📝 Documentation
- [ ] **OpenAPI Spec**: Complete API documentation?
- [ ] **Code Comments**: Are comments clear and useful?
- [ ] **README**: Setup and usage guide?
- [ ] **Examples**: Are usage examples included?

## 💡 Suggestions for Improvement
**Strengths:**
{{strengths}}

**Areas for Improvement:**
{{improvements}}

**Recommended Actions:**
{{actions}}

## ✅ Final Result
- [ ] **✅ APPROVED** - Ready to merge
- [ ] **✅ APPROVED WITH COMMENTS** - Merge after minor adjustments
- [ ] **🔄 NEEDS WORK** - Significant revision required
- [ ] **❌ REJECTED** - Does not meet minimum criteria

**Final Comments:**
{{final_comments}}