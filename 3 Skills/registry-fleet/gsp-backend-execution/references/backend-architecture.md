# Backend Architecture Patterns

## Layered Architecture

```
┌─────────────────────────────────────┐
│         Controllers/Routes          │  ← HTTP handling
├─────────────────────────────────────┤
│            Services                 │  ← Business logic
├─────────────────────────────────────┤
│          Repositories               │  ← Data access
├─────────────────────────────────────┤
│          Data Sources               │  ← Database, External APIs
└─────────────────────────────────────┘
```

## Domain-Driven Design (DDD)

```
src/
├── domains/
│   ├── users/
│   │   ├── entities/
│   │   │   └── User.ts
│   │   ├── repositories/
│   │   │   └── IUserRepository.ts
│   │   ├── services/
│   │   │   └── UserService.ts
│   │   └── events/
│   │       └── UserEvents.ts
│   └── orders/
│       └── ...
├── shared/
│   ├── errors/
│   ├── events/
│   └── types/
└── infrastructure/
    ├── database/
    ├── cache/
    └── external/
```

## Event-Driven Architecture

```typescript
// Event definition
interface DomainEvent {
  eventId: string;
  occurredAt: Date;
  aggregateId: string;
}

class UserCreatedEvent implements DomainEvent {
  constructor(
    public readonly eventId: string,
    public readonly occurredAt: Date,
    public readonly aggregateId: string,
    public readonly email: string,
  ) {}
}

// Event bus
class EventBus {
  private handlers = new Map<string, EventHandler[]>();

  subscribe(eventType: string, handler: EventHandler) {
    this.handlers.get(eventType)?.push(handler) ||
      this.handlers.set(eventType, [handler]);
  }

  async publish(event: DomainEvent) {
    const handlers = this.handlers.get(event.constructor.name) || [];
    await Promise.all(handlers.map(h => h.handle(event)));
  }
}

// Usage in service
class UserService {
  constructor(private eventBus: EventBus) {}

  async createUser(data: CreateUserDTO) {
    const user = await this.userRepo.create(data);

    this.eventBus.publish(new UserCreatedEvent(
      randomUUID(),
      new Date(),
      user.id,
      user.email,
    ));

    return user;
  }
}
```

## CQRS (Command Query Responsibility Segregation)

```typescript
// Command side (write)
class OrderCommandService {
  async createOrder(data: CreateOrderDTO): Promise<Order> {
    // Validate, apply business rules
    return this.orderRepository.create(data);
  }

  async cancelOrder(orderId: string): Promise<void> {
    const order = await this.orderRepository.findById(orderId);
    if (!order.canCancel()) {
      throw new BusinessError('ORDER_CANNOT_BE_CANCELLED');
    }
    await this.orderRepository.updateStatus(orderId, 'CANCELLED');
  }
}

// Query side (read)
class OrderQueryService {
  async getOrderSummary(orderId: string): Promise<OrderSummary> {
    // Optimized read model, possibly from a different store
    return this.readDb.query(`
      SELECT o.id, o.status, u.name as customer
      FROM orders o
      JOIN users u ON o.user_id = u.id
      WHERE o.id = $1
    `, [orderId]);
  }

  async getOrderList(filter: OrderFilter): Promise<OrderListItem[]> {
    return this.readDb.query('...');
  }
}
```

## Saga Pattern (Distributed Transactions)

```typescript
// Saga step
interface SagaStep {
  execute(data: any): Promise<void>;
  compensate(data: any): Promise<void>;
}

// Order saga
class CreateOrderSaga implements SagaStep {
  async execute(ctx: OrderContext): Promise<void> {
    // Step 1: Reserve inventory
    ctx.inventoryReservation = await this.inventory.reserve(ctx.orderItems);

    // Step 2: Process payment
    ctx.payment = await this.payment.charge(ctx.userId, ctx.orderTotal);

    // Step 3: Create order
    ctx.order = await this.orderRepo.create({
      userId: ctx.userId,
      items: ctx.orderItems,
      total: ctx.orderTotal,
    });
  }

  async compensate(ctx: OrderContext): Promise<void> {
    // Undo in reverse order
    if (ctx.order) {
      await this.orderRepo.cancel(ctx.order.id);
    }
    if (ctx.payment) {
      await this.payment.refund(ctx.payment.id);
    }
    if (ctx.inventoryReservation) {
      await this.inventory.release(ctx.inventoryReservation.id);
    }
  }
}

// Saga orchestrator
class OrderSagaOrchestrator {
  async execute(data: CreateOrderDTO): Promise<Order> {
    const ctx = new OrderContext(data);
    const steps = [
      new ReserveInventoryStep(),
      new ProcessPaymentStep(),
      new CreateOrderStep(),
    ];

    const completedSteps: SagaStep[] = [];

    try {
      for (const step of steps) {
        await step.execute(ctx);
        completedSteps.push(step);
      }
      return ctx.order;
    } catch (error) {
      // Compensate completed steps
      for (const step of completedSteps.reverse()) {
        await step.compensate(ctx);
      }
      throw error;
    }
  }
}
```

## Microservices Communication

### Synchronous (HTTP/gRPC)
```typescript
// Service A calls Service B
class UserService {
  constructor(private httpClient: HttpClient) {}

  async getUserWithDepartment(userId: string) {
    const user = await this.userRepo.findById(userId);

    // Sync call to Department service
    const department = await this.httpClient.get(
      `${DEPARTMENT_SERVICE_URL}/departments/${user.departmentId}`
    );

    return { ...user, department };
  }
}
```

### Asynchronous (Message Queue)
```typescript
// Publish event
class OrderService {
  async createOrder(data: CreateOrderDTO) {
    const order = await this.orderRepo.create(data);

    // Publish to message queue
    await this.messageQueue.publish('order.created', {
      orderId: order.id,
      userId: order.userId,
      total: order.total,
    });

    return order;
  }
}

// Subscribe and handle
class NotificationService {
  @Subscribe('order.created')
  async handleOrderCreated(event: OrderCreatedEvent) {
    await this.emailService.sendOrderConfirmation(event.userId, event.orderId);
  }
}
```

## Repository Pattern

```typescript
// Interface
interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
  update(id: string, data: UpdateUserDTO): Promise<User>;
  delete(id: string): Promise<void>;
}

// Prisma implementation
class PrismaUserRepository implements IUserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }

  async create(data: CreateUserDTO): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserDTO): Promise<User> {
    return this.prisma.user.update({ where: { id }, data });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }
}
```

## Dependency Injection

```typescript
// In NestJS
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User) private userRepo: IUserRepository,
    private eventEmitter: EventEmitter,
    private cache: CacheService,
  ) {}

  async getUser(id: string) {
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return cached;

    const user = await this.userRepo.findById(id);
    if (user) {
      await this.cache.set(`user:${id}`, user, 300);
    }
    return user;
  }
}

// Manual DI
const userRepository = new PrismaUserRepository(prisma);
const cacheService = new CacheService(redis);
const eventEmitter = new EventEmitter();
const userService = new UserService(userRepository, eventEmitter, cacheService);
```