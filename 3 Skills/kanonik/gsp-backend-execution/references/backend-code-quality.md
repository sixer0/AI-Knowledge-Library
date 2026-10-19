# Backend Code Quality

## SOLID Principles

### Single Responsibility Principle (SRP)
```typescript
// ❌ Violation: UserService handles too much
class UserService {
  async createUser(data) { /* ... */ }
  async sendWelcomeEmail(user) { /* ... */ } // Should be separate
  async createAuditLog(action) { /* ... */ } // Should be separate
}

// ✅ Correct: Each class has one responsibility
class UserService {
  constructor(
    private userRepo: IUserRepository,
    private eventBus: EventBus,
  ) {}
  async createUser(data) {
    const user = await this.userRepo.create(data);
    this.eventBus.publish(new UserCreatedEvent(user));
    return user;
  }
}

class EmailService {
  async sendWelcomeEmail(user: User) { /* ... */ }
}
```

### Open/Closed Principle (OCP)
```typescript
// ❌ Violation: Must modify to add new validation
class CreateUserRequest {
  validate() {
    if (!this.email) throw new Error('Email required');
    // Adding new validation means modifying this class
  }
}

// ✅ Correct: Open for extension, closed for modification
interface Validator {
  validate(data: unknown): void;
}

class EmailValidator implements Validator {
  validate(data: unknown) {
    if (!isValidEmail(data)) throw new Error('Invalid email');
  }
}

class PasswordValidator implements Validator {
  validate(data: unknown) {
    if (!isStrongPassword(data)) throw new Error('Weak password');
  }
}

// Add new validators without modifying existing code
```

### Liskov Substitution Principle (LSP)
```typescript
// ❌ Violation: Subclass can't fulfill contract
class UserRepository {
  async findAll(): Promise<User[]> { return []; }
}

class CachedUserRepository extends UserRepository {
  async findAll(): Promise<User[]> {
    // Can't return from cache if empty - violates contract
    const cached = await this.cache.get('users');
    if (!cached) throw new Error('Cache miss');
    return cached;
  }
}

// ✅ Correct: Respect parent contract
class UserRepository {
  async findAll(): Promise<User[]> { return []; }
  async findAllFromCache(): Promise<User[] | null> { return null; } // Separate method
}
```

### Interface Segregation Principle (ISP)
```typescript
// ❌ Violation: Fat interface
interface UserManager {
  createUser(data: CreateUserDTO): Promise<User>;
  deleteUser(id: string): Promise<void>;
  getUser(id: string): Promise<User>;
  updatePermissions(userId: string, perms: Permission[]): Promise<void>;
  banUser(userId: string): Promise<void>;
}

// Admin needs ban/update perms, but service layer shouldn't know
// ✅ Correct: Segregated interfaces
interface UserReader {
  getUser(id: string): Promise<User>;
}

interface UserWriter {
  createUser(data: CreateUserDTO): Promise<User>;
}

interface UserAdmin {
  updatePermissions(userId: string, perms: Permission[]): Promise<void>;
  banUser(userId: string): Promise<void>;
}
```

### Dependency Inversion Principle (DIP)
```typescript
// ❌ Violation: Depend on concrete implementation
class UserService {
  constructor(private db: PrismaClient) {} // Tightly coupled
}

// ✅ Correct: Depend on abstractions
class UserService {
  constructor(
    private userRepo: IUserRepository, // Abstraction
    private eventBus: EventBus,        // Abstraction
  ) {}
}
```

## Design Patterns

### Factory Pattern
```typescript
class UserFactory {
  static createAdmin(data: CreateUserDTO): User {
    return new User({ ...data, role: 'admin', permissions: ALL_PERMISSIONS });
  }

  static createCustomer(data: CreateUserDTO): User {
    return new User({ ...data, role: 'customer', permissions: BASIC_PERMISSIONS });
  }
}
```

### Builder Pattern
```typescript
class OrderBuilder {
  private order: Partial<Order> = {};

  setUser(userId: string): this {
    this.order.userId = userId;
    return this;
  }

  addItem(productId: string, quantity: number): this {
    this.order.items ||= [];
    this.order.items.push({ productId, quantity });
    return this;
  }

  setShippingAddress(address: Address): this {
    this.order.shippingAddress = address;
    return this;
  }

  build(): Order {
    if (!this.order.userId || !this.order.items?.length) {
      throw new Error('Invalid order: missing required fields');
    }
    return new Order(this.order);
  }
}

// Usage
const order = new OrderBuilder()
  .setUser('user-123')
  .addItem('product-1', 2)
  .addItem('product-2', 1)
  .setShippingAddress(address)
  .build();
```

### Observer Pattern
```typescript
interface Observer {
  update(event: DomainEvent): void;
}

class OrderObserver implements Observer {
  update(event: DomainEvent) {
    if (event instanceof OrderCreatedEvent) {
      this.inventoryService.reserve(event.items);
      this.paymentService.process(event.userId, event.total);
    }
  }
}

class Subject {
  private observers: Observer[] = [];

  attach(observer: Observer) {
    this.observers.push(observer);
  }

  notify(event: DomainEvent) {
    this.observers.forEach(o => o.update(event));
  }
}
```

### Strategy Pattern
```typescript
interface PaymentStrategy {
  process(amount: number): Promise<PaymentResult>;
}

class CreditCardStrategy implements PaymentStrategy {
  async process(amount: number) { /* Stripe logic */ }
}

class PayPalStrategy implements PaymentStrategy {
  async process(amount: number) { /* PayPal logic */ }
}

class PaymentService {
  constructor(private strategies: Map<string, PaymentStrategy>) {}

  async pay(userId: string, amount: number, method: string) {
    const strategy = this.strategies.get(method);
    if (!strategy) throw new Error('Unknown payment method');
    return strategy.process(amount);
  }
}
```

## Clean Code Guidelines

### Naming
```typescript
// ❌ Bad names
const d = new Date();
const fn = (x) => x * 2;
const data = fetchData();
const temp = calculate();

// ✅ Good names
const currentDate = new Date();
const doubleValue = (value: number) => value * 2;
const userData = fetchUserData();
const temporaryDiscount = calculateDiscount();
```

### Functions
```typescript
// ❌ Too many responsibilities
function createUserAndSendEmailAndLogAndValidate(data) { /* ... */ }

// ✅ Single responsibility, composable
async function createUser(data: CreateUserDTO) {
  validateUserData(data);
  const user = await userRepository.create(data);
  return user;
}

async function sendWelcomeEmail(user: User) {
  await emailService.send(user.email, 'welcome');
}

async function createUserPipeline(data: CreateUserDTO) {
  const user = await createUser(data);
  await sendWelcomeEmail(user);
  logger.info('User created', { userId: user.id });
}
```

### Error Handling
```typescript
// ❌ Swallowing errors
try {
  await doSomething();
} catch (e) {}

// ✅ Proper error handling
try {
  await doSomething();
} catch (error) {
  logger.error('Failed to do something', { error, context });
  throw new AppError('ACTION_FAILED', 'Failed to perform action', 500);
}
```

### TypeScript Best Practices
```typescript
// ❌ Using 'any'
function processData(data: any) { /* ... */ }

// ✅ Explicit types
function processData(data: UserDTO): Promise<Result> { /* ... */ }

// ❌ Type assertions
const user = data as User;

// ✅ Type guards
function isUser(data: unknown): data is User {
  return typeof data === 'object' && data !== null && 'email' in data;
}

if (isUser(data)) {
  // data is typed as User here
}
```

## Code Review Checklist

- [ ] No commented-out code
- [ ] No TODO comments without issue references
- [ ] Functions are small and single-purpose
- [ ] Variable names are descriptive
- [ ] Error handling is consistent
- [ ] No hardcoded values (use constants/env)
- [ ] No security vulnerabilities
- [ ] Tests cover happy path and edge cases
- [ ] No unnecessary dependencies
- [ ] API responses are consistent