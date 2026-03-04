# ADR-0001: Domain Foundation Architecture

**Status:** Accepted  
**Date:** 2025-08-19  
**Deciders:** Development Team  

## Context

We are building a Custom Sneaker Platform MVP that connects customers, creators, and manufacturers in a design-to-production workflow. The platform needs to handle complex business logic including design management, order processing, quality gates, and multi-actor authorization while maintaining data integrity and auditability.

## Decision

We have implemented a comprehensive domain foundation with the following architectural decisions:

### 1. Domain Model Structure

#### Core Entities
- **Users**: Multi-role actors (customer, creator, admin) with OAuth support
- **Profiles**: Extended user information with preferences and localization
- **Manufacturers**: Regional production partners with capabilities and constraints
- **Silhouettes**: Base sneaker models with customizable panel specifications
- **Materials**: Manufacturer-specific materials with printability and constraints
- **Designs**: User-created customizations with versioning and IP tracking
- **Orders**: Purchase requests with quality gates and pricing breakdown
- **Issues**: Quality problem tracking with evidence and resolution

#### Supporting Entities
- **DesignRevisions**: Version control with manufacturability and IP risk scoring
- **Artworks**: User-uploaded content with similarity detection and IP checking
- **OrderEvents**: Audit trail for order lifecycle tracking
- **ProductionPackages**: Manufacturing kits with approval workflow
- **Remixes**: Design attribution and derivative tracking

### 2. Type Safety with PHP Enums

We chose PHP 8.1+ backed enums for all enumerated fields to ensure type safety and prevent invalid state transitions:

```php
enum UserRole: string {
    case CUSTOMER = 'customer';
    case CREATOR = 'creator';
    case ADMIN = 'admin';
}

enum OrderStatus: string {
    case CREATED = 'created';
    case AWAITING_VALIDATION = 'awaiting_validation';
    // ... 11 total states
}
```

**Benefits:**
- Compile-time type checking
- IDE autocomplete support
- Prevents invalid enum values
- Clear business logic representation

### 3. Quality Gates System

We implemented a JSON-based quality gate system in the orders table:

```json
{
  "A": false,  // IP compliance check
  "B": false,  // Manufacturability check  
  "C": false,  // Production package validation
  "D": false   // Manufacturer acceptance
}
```

**Rationale:**
- Flexible gate definitions without schema changes
- Easy to query and update individual gates
- Supports complex business rules
- Audit trail through OrderEvents

### 4. Database Design Decisions

#### Indexing Strategy
- **Composite indexes** for frequent query patterns (user_id + status)
- **Unique constraints** on business keys (manufacturer_id + code)
- **Foreign key constraints** with appropriate cascade rules
- **Soft deletes** for designs to preserve order history

#### JSON Columns
We use JSON columns for flexible, evolving data structures:
- `metadata` fields for extensible properties
- `specs` for silhouette panel definitions
- `constraints` for material properties
- `price_breakdown` for detailed order pricing
- `gate_state` for quality gate tracking

### 5. Authorization Architecture (RBAC)

#### Three-Tier Role System
1. **Customer**: Can create orders, view public designs, report issues
2. **Creator**: Can create/manage designs, view orders for their designs
3. **Admin**: Full access to all resources with override capabilities

#### Policy-Based Authorization
- **DesignPolicy**: Ownership-based access with public visibility support
- **OrderPolicy**: Customer ownership + creator read access for their designs
- **IssuePolicy**: Reporter ownership + admin resolution capabilities

#### Middleware Integration
- Route-level protection with `role:creator,admin` syntax
- Gateway pattern for programmatic access control
- Future-ready for manufacturer portal integration

### 6. Event-Driven Architecture

#### Domain Events
- **DesignRevisionCreated**: Triggers quality checks and notifications
- **OrderStatusChanged**: Maintains audit trail and triggers workflows
- **IssueOpened**: Enables immediate escalation and notifications

#### Event Integration
- Automatic OrderEvent creation for audit compliance
- Broadcasting channels for real-time updates
- Extensible for future workflow automation

### 7. API Design Decisions

#### RESTful Structure
- **Versioned APIs** (`/api/v1/`) for future compatibility
- **Resource-based endpoints** with proper HTTP methods
- **Filtering support** via query parameters
- **Pagination** for large datasets

#### Authentication
- **Laravel Sanctum** for API token authentication
- **Role-based middleware** for endpoint protection
- **Policy enforcement** at the controller level

#### Response Format
- **JSON API Resources** with relationship data
- **Permission flags** for frontend authorization
- **Consistent error responses** with proper HTTP status codes

### 8. Testing Strategy

#### Comprehensive Test Coverage
- **Policy tests**: 9 tests covering all authorization scenarios
- **Integration tests**: Quality gates and event firing verification
- **Factory-driven tests**: Realistic data relationships
- **Database tests**: Migration and seeding validation

#### Test Data Management
- **Seeded test accounts** with known credentials
- **Realistic demo data** (3 manufacturers, 18 users, 36 materials)
- **Relationship integrity** across all entities

## Consequences

### Positive
- **Type-safe domain model** prevents runtime errors
- **Flexible quality gate system** supports complex business rules
- **Comprehensive authorization** with fine-grained permissions
- **Event-driven architecture** enables workflow automation
- **Rich demo environment** for development and testing
- **Production-ready CI/CD** with multiple quality checks

### Negative
- **Complex relationship graph** requires careful query optimization
- **JSON column queries** may need special indexing strategies
- **Event system** adds complexity for simple CRUD operations
- **Enum casting** requires careful handling in API responses

### Risks
- **Database performance** with complex joins across 12+ tables
- **Event ordering** in high-concurrency scenarios
- **JSON schema evolution** without proper versioning
- **Authorization complexity** may impact performance

## Alternatives Considered

### 1. Simple String Enums vs PHP Enums
**Rejected:** String constants lack type safety and IDE support

### 2. Separate Quality Tables vs JSON Gates
**Rejected:** Separate tables would require complex joins for gate status queries

### 3. Single User Table vs User+Profile Split
**Rejected:** Single table would mix authentication and profile concerns

### 4. Event Sourcing vs Simple Events
**Rejected:** Full event sourcing too complex for MVP, simple events provide sufficient auditability

## Implementation Details

### Database Schema
- **12 core tables** with proper relationships
- **15 migrations** with idempotent design
- **36 indexes** for query optimization
- **Foreign key constraints** with cascade rules

### Code Organization
- **9 PHP enums** for type safety
- **12 Eloquent models** with relationships and casting
- **3 authorization policies** with role-based logic
- **4 API controllers** with filtering and validation
- **4 API resources** with permission metadata

### Quality Assurance
- **Laravel Pint** formatting with strict rules
- **PHPStan level 6** static analysis
- **Pest testing framework** with 11+ passing tests
- **GitHub Actions CI/CD** with multi-PHP version testing

## Future Considerations

### Scalability
- Consider **read replicas** for manufacturer/material queries
- Implement **caching layers** for frequently accessed silhouettes
- **Queue-based processing** for IP checking and manufacturability scoring

### Feature Extensions
- **Manufacturer portal** with dedicated roles and permissions
- **Advanced quality gates** with custom business rules
- **Workflow automation** based on domain events
- **Real-time collaboration** using broadcasting channels

### Technical Debt
- **Relationship eager loading** optimization
- **JSON column indexing** for complex queries
- **Event replay mechanisms** for debugging
- **API rate limiting** and throttling

## Monitoring and Metrics

### Key Performance Indicators
- **API response times** for public endpoints
- **Database query performance** for complex joins
- **Event processing latency** for real-time features
- **Authorization decision times** for policy enforcement

### Business Metrics
- **Design creation rate** by creators
- **Order conversion rate** through quality gates
- **Issue resolution time** for quality problems
- **Manufacturer utilization** across regions

---

**This ADR documents the foundational architecture decisions for the Custom Sneaker Platform MVP. All implementation details are production-ready and support the planned feature roadmap while maintaining flexibility for future enhancements.**
