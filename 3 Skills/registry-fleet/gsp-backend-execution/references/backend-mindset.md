# Backend Mindset

## Problem-Solving Framework

### 1. Understand Before Solving
```typescript
// ❌ Jump to solution
function getUser(id) {
  return db.query(`SELECT * FROM users WHERE id = ${id}`); // SQL injection!
}

// ✅ Understand the problem first
// Q: What should happen if user doesn't exist?
// Q: What data should be returned?
// Q: Who can access this endpoint?
// Q: What are the performance requirements?

async function getUser(id: string): Promise<UserDTO> {
  // Validate input
  if (!isValidUUID(id)) {
    throw new AppError('INVALID_USER_ID', 'Invalid user ID format', 400);
  }

  const user = await userRepo.findById(id);
  if (!user) {
    throw new AppError('USER_NOT_FOUND', 'User not found', 404);
  }

  return toUserDTO(user);
}
```

### 2. Consider Edge Cases
```typescript
// Happy path first, then edge cases
async function calculateOrderTotal(items: OrderItem[]): Promise<number> {
  // ✅ Empty cart
  if (!items || items.length === 0) {
    return 0;
  }

  // ✅ Single item
  // ✅ Large orders
  // ✅ Items with quantity 0 (should be filtered out?)
  // ✅ Negative quantities (invalid)

  return items.reduce((total, item) => {
    if (item.quantity <= 0) {
      throw new AppError('INVALID_QUANTITY', 'Quantity must be positive', 400);
    }
    return total + (item.price * item.quantity);
  }, 0);
}
```

### 3. Design for Failure
```typescript
// Assume external services WILL fail
async function getUserWithExternalData(userId: string) {
  try {
    const user = await userRepo.findById(userId);

    // External service might be down - handle gracefully
    let preferences;
    try {
      preferences = await externalApi.getPreferences(userId);
    } catch (error) {
      logger.warn({ event: 'preferences_fetch_failed', userId, error: error.message });
      preferences = null; // Use defaults
    }

    return { ...user, preferences };
  } catch (error) {
    // Database might be down
    logger.error({ event: 'user_fetch_failed', userId, error: error.message });
    throw new AppError('SERVICE_UNAVAILABLE', 'Unable to fetch user data', 503);
  }
}
```

## Architectural Thinking

### 1. Start with Requirements
```typescript
// Document before coding
interface Requirement {
  id: string;
  title: string;
  description: string;
  acceptanceCriteria: string[];
  priority: 'must' | 'should' | 'could';
}

// Example
const requirement: Requirement = {
  id: 'AUTH-001',
  title: 'User Authentication',
  description: 'Users should be able to log in with email/password',
  acceptanceCriteria: [
    'Valid credentials return JWT token',
    'Invalid credentials return 401',
    'Token expires after 15 minutes',
    'Refresh token valid for 7 days',
  ],
  priority: 'must',
};
```

### 2. Trade-off Analysis
```typescript
// Every decision has trade-offs - document them

// Decision: Use PostgreSQL vs MongoDB
const tradeOffAnalysis = {
  postgres: {
    pros: ['ACID transactions', 'Mature ecosystem', 'Complex queries'],
    cons: ['Schema migrations needed', 'Less flexible'],
    bestFor: 'User data, orders, transactions',
  },
  mongo: {
    pros: ['Flexible schema', 'Easy horizontal scaling'],
    cons: ['No transactions across collections', 'Less mature tooling'],
    bestFor: 'Logging, real-time data, flexible documents',
  },
};

// Decision: Monolith vs Microservices
const architectureDecision = {
  monolith: {
    pros: ['Simple deployment', 'Easy debugging', 'Lower latency'],
    cons: ['Tight coupling', 'Scale entire app'],
    recommendedWhen: ['Small team', 'Rapid prototyping', '< 10 services'],
  },
  microservices: {
    pros: ['Independent scaling', 'Technology flexibility', 'Team autonomy'],
    cons: ['Complexity', 'Network latency', 'Debugging difficulty'],
    recommendedWhen: ['Large team', 'Multiple domains', 'High scale'],
  },
};
```

### 3. YAGNI (You Aren't Gonna Need It)
```typescript
// ❌ Over-engineering
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date | null; // Why? Not required yet
  preferences: {           // Not required
    theme: 'light' | 'dark';
    language: string;
    notifications: boolean;
  };
}

// ✅ Start simple, add when needed
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}
```

## Collaboration

### Code Review Culture
```typescript
// As a reviewer, focus on:
const reviewFocus = {
  correctness: [
    'Does the code do what the ticket asks?',
    'Are edge cases handled?',
    'Are there potential bugs?',
  ],
  security: [
    'Any SQL injection risks?',
    'Is input validated?',
    'Are secrets properly handled?',
  ],
  design: [
    'Is the code testable?',
    'Does it follow existing patterns?',
    'Is it simple enough?',
  ],
  maintainability: [
    'Is the code readable?',
    'Are functions small and focused?',
    'Are variable names descriptive?',
  ],
};

// As an author:
const prDescription = `
## What
User authentication endpoint with JWT tokens

## Why
Users need to log in to access protected resources

## How
- Validates email/password against database
- Returns access token (15 min) and refresh token (7 days)
- Refresh tokens are rotated on use

## Testing
- [x] Valid credentials → 200 + tokens
- [x] Invalid password → 401
- [x] Invalid email → 401
- [x] Missing fields → 400

## Screenshots
N/A (API-only change)
`;
```

### Documentation as Communication
```typescript
// Every non-obvious decision deserves a comment
async function calculateShippingCost(order: Order): Promise<number> {
  // Use weight-based calculation for orders > 5kg
  // Flat rate for lighter orders (simpler, good UX)
  if (order.totalWeight <= 5000) { // grams
    return FLAT_RATE;
  }

  // Exponential pricing for heavy items
  // Reason: Carriers charge more for weight > 5kg
  const baseWeight = 5000;
  const extraWeight = order.totalWeight - baseWeight;
  return FLAT_RATE + (extraWeight * RATE_PER_GRAM);
}
```

## Technical Debt

### When to Accept Debt
```typescript
// Accept debt when:
// 1. Time pressure is real
// 2. Debt is isolated (doesn't spread)
// 3. You have a plan to pay it back

// Document it!
const technicalDebt = {
  id: 'DEBT-001',
  title: 'No rate limiting on search endpoint',
  incurredDate: '2024-01-15',
  impact: 'Potential DoS via expensive queries',
  mitigation: 'IP-based limiting at load balancer',
  fixEstimate: '4 hours',
  priority: 'medium',
};
```

### When to Pay It Back
```typescript
// Pay back when:
// 1. It's causing bugs or slowdowns
// 2. You're touching that code anyway
// 3. The cost of not fixing exceeds the cost of fixing

// "Boy scout rule" - leave code cleaner than you found it
// When editing a file with tech debt, fix it if:
// - It's in the same area you're working on
// - Fix is simple (a few minutes)
// - You won't exceed PR size limits
```

## Continuous Learning

### Stay Current
```typescript
const learningResources = {
  fundamentals: [
    'MDN Web Docs (HTTP, Web APIs)',
    'PostgreSQL documentation',
    'Node.js documentation',
  ],
  security: [
    'OWASP Top 10',
    'NIST guidelines',
    'Security newsletters',
  ],
  architecture: [
    'Martin Fowler\'s blog',
    'AWS Well-Architected Framework',
    'Google Cloud Architecture Center',
  ],
  performance: [
    'Web.dev',
    'Node.js performance tips',
    'Database indexing strategies',
  ],
};
```

### Reflect and Improve
```typescript
// Post-mortem template for incidents
const incidentReview = {
  summary: 'What happened?',
  timeline: 'When did what occur?',
  impact: 'Who/what was affected?',
  rootCause: 'Why did it happen?',
  whatWentWell: 'What helped mitigate?',
  whatCouldBeBetter: 'What was slow/difficult?',
  actionItems: [
    'Prevent recurrence',
    'Improve detection',
    'Improve response',
  ],
};
```

## Key Principles Summary

| Principle | Meaning |
|-----------|---------|
| **KISS** | Keep it simple, stupid |
| **YAGNI** | You aren't gonna need it |
| **DRY** | Don't repeat yourself |
| **SOLID** | Single responsibility, open/closed, liskov substitution, interface segregation, dependency inversion |
| **Fail Fast** | Validate early, crash early |
| **Design for Failure** | Expect and handle errors gracefully |
| **Measure Twice, Cut Once** | Plan before coding |
| **Boy Scout Rule** | Leave code cleaner than you found it |
| **Rubber Duck** | Explain the problem to understand it |
| **First Do No Harm** | When in doubt, don't break existing functionality |