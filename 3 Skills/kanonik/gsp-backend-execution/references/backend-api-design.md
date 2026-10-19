# Backend API Design

## RESTful Best Practices

### Resource Naming

| Pattern | Good | Bad |
|---------|------|-----|
| Collections | `/users` | `/getUsers` |
| Single resource | `/users/:id` | `/user/:id` |
| Nested resource | `/users/:id/orders` | `/getUserOrders` |
| Filtering | `/orders?status=pending` | `/getPendingOrders` |
| Pagination | `/orders?page=2&limit=20` | `/orders/page/2` |
| Search | `/products?search=laptop` | `/searchProducts` |

### HTTP Methods

| Method | Usage | Idempotent | Safe |
|--------|-------|------------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource (full) | Yes | No |
| PATCH | Update resource (partial) | No | No |
| DELETE | Remove resource | Yes | No |

### Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation failed |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Authenticated but not allowed |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable Entity | Semantically invalid |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server Error | Unexpected error |

### Response Format

```typescript
// Success response
{
  "data": { /* resource */ },
  "meta": { /* pagination, etc */ }
}

// Error response
{
  "error": "ERROR_CODE",
  "message": "Human-readable message",
  "correlationId": "uuid"
}
```

### Versioning

```typescript
// URL path (most common)
GET /api/v1/users

// Header (GitHub style)
// GET /users
// Accept: application/vnd.api+json; version=1

// Query parameter
// GET /users?version=1
```

## GraphQL

### Schema Design

```typescript
const typeDefs = gql`
  type User {
    id: ID!
    email: String!
    name: String!
    orders: [Order!]!
  }

  type Order {
    id: ID!
    status: OrderStatus!
    total: Float!
    items: [OrderItem!]!
    user: User!
  }

  enum OrderStatus {
    PENDING
    PROCESSING
    SHIPPED
    DELIVERED
    CANCELLED
  }

  type Query {
    user(id: ID!): User
    users(limit: Int, offset: Int): [User!]!
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
    updateOrderStatus(id: ID!, status: OrderStatus!): Order!
  }

  input CreateUserInput {
    email: String!
    name: String!
  }
`;
```

### Resolver Pattern

```typescript
const resolvers = {
  Query: {
    user: (_, { id }, ctx) => ctx.users.findById(id),
    users: (_, args, ctx) => ctx.users.findAll(args),
  },
  User: {
    orders: (parent, _, ctx) => ctx.orders.findByUserId(parent.id),
  },
  Mutation: {
    createUser: (_, { input }, ctx) => ctx.users.create(input),
  },
};
```

## gRPC

### Proto Definition

```protobuf
syntax = "proto3";

package users;

service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (ListUsersResponse);
  rpc CreateUser (CreateUserRequest) returns (User);
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
}

message GetUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 limit = 1;
  int32 offset = 2;
}

message ListUsersResponse {
  repeated User users = 1;
  int32 total = 2;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}
```

### When to Use What

| API Style | Best For | Pros | Cons |
|-----------|----------|------|------|
| REST | Public APIs, simple CRUD | Simple, cacheable, widely understood | Over-fetching, multiple roundtrips |
| GraphQL | Complex data requirements | Flexible queries, single endpoint | Complexity, caching challenges |
| gRPC | Internal microservices | Fast, strongly typed, bidirectional streaming | Not human-readable, requires tooling |

## Pagination Patterns

### Offset-Based
```typescript
GET /users?page=2&limit=20
// Returns: { data: [...], total: 100, page: 2, limit: 20 }
```

### Cursor-Based (Keyset)
```typescript
GET /orders?cursor=eyJpZCI6MTAsImNyZWF0ZWRBdCI6IjIwMjQtMDEtMDEifQ&limit=20
// Returns: { data: [...], nextCursor: "..." }
// More efficient for large datasets, real-time data
```

### Seek Method
```typescript
// For exactly-once pagination
GET /products?seekAfter=1234&limit=20
```

## Filtering & Sorting

```typescript
// Filtering
GET /products?category=electronics&price_gte=100&price_lte=500

// Sorting
GET /products?sort=price:asc,createdAt:desc

// Search
GET /products?search=laptop+pro&fields=name,description
```

## Error Handling

```typescript
// Standardized error response
interface ApiError {
  error: string;        // Machine-readable code
  message: string;      // Human-readable
  details?: any;        // Validation details, etc.
  correlationId: string;
}

// Error codes
enum ErrorCode {
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  NOT_FOUND = 'NOT_FOUND',
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  CONFLICT = 'CONFLICT',
  RATE_LIMITED = 'RATE_LIMITED',
  INTERNAL_ERROR = 'INTERNAL_ERROR',
}
```