# Refactoring Practices Rule

**Based on:** Martin Fowler's Refactoring, Code Smells, Continuous Improvement
**Scope:** Refactoring techniques, code smell detection, and improvement practices

## Code Smells Detection

### Duplication (Priority #1)
- **Rule:** Zero tolerance for code duplication
- **Rule of Three:** Refactor at third occurrence of similar logic
- **Detection:** Structural and semantic duplication analysis
- **Examples:**
  - Repeated validation logic
  - Similar calculation patterns
  - Copy-pasted business rules

### Long Methods
- **Rule:** Methods > 5 lines need evaluation
- **Rule:** Methods > 10 lines require refactoring
- **Extraction Patterns:**
  - Extract validation logic
  - Extract calculation functions
  - Extract notification logic
- **Example:**
  ```python
  # ❌ Long method
  def process_order(order):
      # Validation (5 lines)
      # Calculation (8 lines) 
      # Notification (4 lines)
      # Total: 17 lines
  
  # ✅ Refactored
  def process_order(order):
      validate_order(order)     # 5 lines
      calculate_totals(order)   # 8 lines
      notify_parties(order)     # 4 lines
  ```

### Large Classes (God Classes)
- **Rule:** Classes with > 3 responsibilities need splitting
- **Detection:** Cohesion metrics and responsibility analysis
- **Refactoring:** Extract Class, Move Method
- **Example:**
  ```python
  # ❌ God class
  class UserManager:
      def validate_user()
      def save_user()
      def send_email()
      def generate_report()
      # Too many responsibilities
  
  # ✅ Split responsibilities
  class UserValidator:   # Validation
  class UserRepository:  # Persistence  
  class EmailService:    # Notification
  class ReportGenerator: # Reporting
  ```

### Complex Conditionals
- **Rule:** Conditionals with > 2 branches need evaluation
- **Pattern:** Replace Conditional with Polymorphism
- **Detection:** Nested if/else, complex switch statements
- **Example:**
  ```python
  # ❌ Complex conditional
  def calculate_shipping(country):
      if country == "US":
          return 5.00
      elif country == "CA":
          return 7.00
      elif country == "UK":
          return 8.00
      # ... 10 more countries
  
  # ✅ Strategy pattern
  class ShippingStrategy(ABC):
      @abstractmethod
      def calculate(self) -> float:
  
  class USShipping(ShippingStrategy):
      def calculate(self) -> float: return 5.00
  
  # Factory creates appropriate strategy
  ```

## Fundamental Refactoring Techniques

### Extract Function/Method
- **When:** Logic can be named and reused
- **Benefit:** Improved readability and reusability
- **Example:**
  ```python
  # Before
  def process_data(data):
      # ... complex validation logic
      # ... complex calculation logic
  
  # After  
  def process_data(data):
      validate_data(data)
      calculate_results(data)
  
  def validate_data(data):
      # extracted validation
  
  def calculate_results(data):
      # extracted calculation
  ```

### Rename
- **When:** Names don't reveal intention
- **Benefit:** Living documentation
- **Importance:** One of most powerful refactorings
- **Example:**
  ```python
  # ❌ Unclear
  def proc(d):
      # what does this do?
  
  # ✅ Clear intention
  def process_user_registration(user_data):
      # clearly processes user registration
  ```

### Move Function/Field
- **When:** Logic belongs in different context
- **Benefit:** Improved cohesion and organization
- **Example:**
  ```python
  # ❌ Feature envy
  class OrderProcessor:
      def calculate_tax(self, order):
          # uses mostly TaxCalculator methods
  
  # ✅ Move to proper class
  class TaxCalculator:
      def calculate_tax(self, order):
          # natural home for tax logic
  ```

### Introduce Parameter Object
- **When:** Multiple related parameters
- **Benefit:** Simplified method signatures
- **Example:**
  ```python
  # ❌ Many parameters
  def create_user(name, email, phone, address, city, zip_code):
  
  # ✅ Parameter object
  class UserData:
      def __init__(self, name, email, phone, address):
          self.name = name
          self.email = email
          self.phone = phone
          self.address = address
  
  def create_user(user_data: UserData):
  ```

## Refactoring Process Rules

### When to Refactor
1. **Adding Feature:** Preparatory refactoring
2. **Fixing Bug:** Comprehension refactoring  
3. **Code Review:** Collaborative refactoring
4. **Reading Code:** Light cleanup refactoring

### When NOT to Refactor
- **Stable Code:** If it works and won't be modified
- **Without Tests:** Too risky without safety net
- **Mass Rewrites:** Prefer incremental improvements

### Test Requirements
- **Rule:** No refactoring without tests
- **Rule:** Tests must pass before and after
- **Rule:** Small, safe steps with continuous testing

## Automated Refactoring Support

### IDE Integration
- **AST-based Refactoring:** Not text-based search/replace
- **Supported Operations:**
  - Rename with dependency tracking
  - Extract method/function
  - Move class/function
  - Inline function/variable
  - Change function signature

### Language Server Protocol (LSP)
- **Rule:** Use LSP-enabled editors for refactoring
- **Benefits:** Cross-editor compatibility
- **Supported:** Python, TypeScript, Java, etc.

### Limitations Awareness
- **Dynamic Languages:** Python refactoring more challenging
- **Metaprogramming:** Decorators, metaclasses complicate refactoring
- **Document:** Known limitations for each language

## Continuous Improvement Practices

### Campground Rule
- **Principle:** "Leave the campground cleaner than you found it"
- **Practice:** Small improvements during feature work
- **Benefit:** Prevents technical debt accumulation

### YAGNI + Refactoring
- **Strategy:** Build minimal needed today
- **Evolution:** Refactor when real needs emerge
- **Balance:** Avoid over-engineering, enable future change

### Code Review Refactoring
- **Practice:** Turn abstract suggestions into concrete improvements
- **Benefit:** Learning and alignment opportunity
- **Example:** "Let's extract this validation logic together"

## Validation Rules for Trae IDE

1. **Duplication Detection:** Structural and semantic analysis
2. **Method Length:** Flag methods > 5 lines for evaluation
3. **Class Responsibility:** Detect classes with > 3 responsibilities
4. **Conditional Complexity:** Identify complex conditionals for polymorphism
5. **Test Coverage:** Ensure tests exist before suggesting refactoring
6. **Safe Refactoring:** AST-based operations with dependency tracking

## Examples from Study Materials

### Good Refactoring (From Refactoring Book)
```python
# Before: Complex method
def print_owing(amount):
    print_banner()
    
    # Print details
    print("name:", name)
    print("amount:", amount)

# After: Extracted methods
def print_owing(amount):
    print_banner()
    print_details(amount)

def print_details(amount):
    print("name:", name)
    print("amount:", amount)
```

### Code Smell Examples
```python
# ❌ Data clump (multiple related parameters)
def create_order(customer_name, customer_email, customer_phone):
    # parameters always used together

# ✅ Parameter object
class CustomerInfo:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

def create_order(customer: CustomerInfo):
```

## References

- Martin Fowler: Refactoring Book
- Code Smells Catalog
- Continuous Improvement Practices
- Study files: `/refactoring-improving-the-design-of-existing-code-book/README.md`