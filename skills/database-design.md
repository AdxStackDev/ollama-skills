---
name: database-design
description: Best practices for database schema design, optimization, and data modeling for both SQL and NoSQL databases
license: Complete terms in LICENSE.txt
---

# Database Design

Design databases that scale, perform well, and maintain data integrity. Think like a database architect building a foundation that will support years of feature growth without requiring painful migrations.

## Core Principles

**Normalize to reduce redundancy, denormalize for performance**. Start with a normalized schema (3NF) to avoid data anomalies, then selectively denormalize based on actual query patterns and performance requirements. Never denormalize prematurely.

**Design for your queries, not your entities**. How you'll read the data is more important than how it's stored. A schema that perfectly models your domain but makes every query slow is a failed design.

**Enforce constraints in the database**. Your application might have bugs, but your database shouldn't lie. Use foreign keys, unique constraints, check constraints, and not-null constraints to maintain data integrity at the lowest level.

**Plan for data growth**. A schema that works with 1,000 rows might fail catastrophically at 1,000,000. Consider indexing strategy, partitioning, and archival from the beginning.

## SQL Schema Design

### Table Structure

**Naming conventions:**
- Tables: plural, lowercase, underscores (`users`, `blog_posts`, `order_items`)
- Columns: singular, lowercase, underscores (`user_id`, `created_at`, `is_active`)
- Primary keys: `id` or `{table_name}_id`
- Foreign keys: `{referenced_table}_id` (e.g., `user_id`)
- Boolean columns: prefix with `is_`, `has_`, `can_` (`is_active`, `has_discount`)
- Timestamps: `created_at`, `updated_at`, `deleted_at`

**Every table should have:**
- Primary key (prefer BIGINT/UUID over INT)
- Created timestamp (`created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP`)
- Updated timestamp (`updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`)
- Soft delete if applicable (`deleted_at TIMESTAMP NULL`)

**Example well-structured table:**
```sql
CREATE TABLE users (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT true,
    email_verified_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_created_at (created_at),
    INDEX idx_active_users (is_active, deleted_at)
);
```

### Relationships

**One-to-Many:**
```sql
CREATE TABLE posts (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_posts (user_id, created_at)
);
```

**Many-to-Many (use junction table):**
```sql
CREATE TABLE users_roles (
    user_id BIGINT UNSIGNED NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    INDEX idx_role_users (role_id, user_id)
);
```

**Self-referencing (hierarchical data):**
```sql
CREATE TABLE categories (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    parent_id BIGINT UNSIGNED NULL,
    name VARCHAR(100) NOT NULL,
    path VARCHAR(500), -- Materialized path for faster queries
    
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_parent (parent_id),
    INDEX idx_path (path)
);
```

### Data Types

**Choose the right type:**
- IDs: `BIGINT UNSIGNED` or `UUID` (never use `INT` for user-facing tables)
- Money: `DECIMAL(19,4)` (never use FLOAT/DOUBLE for currency)
- Booleans: `BOOLEAN` (stored as TINYINT(1))
- Dates: `DATE` for dates, `TIMESTAMP` for datetime with timezone awareness
- Text: `VARCHAR(n)` for bounded strings, `TEXT` for unbounded
- JSON: `JSON` type for structured data (MySQL 5.7+, PostgreSQL 9.4+)
- Enums: Use `ENUM` carefully (hard to modify) or separate lookup table

**String lengths:**
- Email: `VARCHAR(255)`
- Username: `VARCHAR(50)`
- Name: `VARCHAR(100)`
- Short description: `VARCHAR(500)`
- Long text: `TEXT` or `MEDIUMTEXT`
- URL: `VARCHAR(2048)`

### Indexes

**Index strategy:**
- Primary keys are automatically indexed
- Foreign keys should always be indexed
- Columns in WHERE clauses need indexes
- Columns in JOIN conditions need indexes
- Columns in ORDER BY need indexes
- Composite indexes for multi-column queries

**Composite index order matters:**
```sql
-- Good for: WHERE user_id = X AND status = Y
-- Good for: WHERE user_id = X
-- Bad for: WHERE status = Y (can't use index)
INDEX idx_user_status (user_id, status)

-- Order by selectivity (most selective first)
-- High selectivity: user_id (many unique values)
-- Low selectivity: status (few unique values)
```

**Don't over-index:**
- Each index slows down INSERT/UPDATE/DELETE
- Indexes take storage space
- Database can only use one index per table per query (usually)
- Profile queries first, then add indexes that help

### Constraints

**Use database constraints for data integrity:**

```sql
CREATE TABLE orders (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    total_amount DECIMAL(19,4) NOT NULL,
    status ENUM('pending', 'paid', 'shipped', 'delivered', 'cancelled') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    CHECK (total_amount >= 0),
    INDEX idx_user_orders (user_id, status)
);
```

**Constraint types:**
- `NOT NULL`: Prevent null values
- `UNIQUE`: Ensure uniqueness
- `PRIMARY KEY`: Unique identifier
- `FOREIGN KEY`: Referential integrity
- `CHECK`: Value validation
- `DEFAULT`: Default values

### Normalization vs Denormalization

**Third Normal Form (3NF) - start here:**
- No repeating groups
- All attributes depend on the key
- No transitive dependencies

**When to denormalize:**
- Query performance is critical and proven slow
- Read-heavy workload (10:1 or higher read:write ratio)
- Data rarely changes
- Complex joins are killing performance

**Denormalization techniques:**
- Add redundant columns (e.g., `user_post_count` in `users` table)
- Materialized views
- Pre-aggregated data
- JSON columns for nested data

## NoSQL Data Modeling

### Document Stores (MongoDB, Firestore)

**Embed vs Reference:**

**Embed when:**
- Data is accessed together
- One-to-few relationships
- Data doesn't change often
- Data is owned by parent

```javascript
// Embedded comments in blog post
{
  "_id": "post123",
  "title": "Database Design",
  "content": "...",
  "comments": [
    {
      "user": "john_doe",
      "text": "Great post!",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Reference when:**
- Data is accessed separately
- One-to-many or many-to-many
- Data changes frequently
- Data is shared across documents

```javascript
// Referenced author
{
  "_id": "post123",
  "title": "Database Design",
  "author_id": "user456",
  "content": "..."
}

{
  "_id": "user456",
  "username": "john_doe",
  "email": "john@example.com"
}
```

**Design for your queries:**
```javascript
// If you always query posts by author, denormalize author name
{
  "_id": "post123",
  "author_id": "user456",
  "author_name": "John Doe", // Denormalized
  "title": "Database Design"
}
```

### Key-Value Stores (Redis, DynamoDB)

**Key naming conventions:**
```
user:123:profile
user:123:sessions
post:456:comments
cache:api:users:list:page1
```

**Access patterns determine schema:**
- Single-table design in DynamoDB
- Use composite keys for sorting
- Denormalize aggressively
- Duplicate data for different access patterns

## Performance Optimization

### Query Optimization

**Use EXPLAIN to analyze queries:**
```sql
EXPLAIN SELECT * FROM posts 
WHERE user_id = 123 
ORDER BY created_at DESC 
LIMIT 10;
```

**Look for:**
- Type: Should be `ref` or `range`, avoid `ALL` (full table scan)
- Possible_keys: Available indexes
- Key: Index actually used
- Rows: Fewer is better

**Common optimizations:**
- Add missing indexes
- Rewrite subqueries as JOINs
- Use LIMIT for large result sets
- Avoid SELECT *, specify needed columns
- Use covering indexes (index contains all queried columns)

### Pagination

**Offset-based (simple but slow for large offsets):**
```sql
SELECT * FROM posts 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 1000; -- Slow: skips first 1000 rows
```

**Cursor-based (fast for any page):**
```sql
SELECT * FROM posts 
WHERE created_at < '2024-01-15T10:30:00Z' 
ORDER BY created_at DESC 
LIMIT 20; -- Fast: uses index directly
```

### Connection Pooling

**Always use connection pools:**
- Reuse database connections
- Set max connections based on database limits
- Set timeout values appropriately
- Monitor active connections

```python
# Example: SQLAlchemy pool
engine = create_engine(
    'mysql://user:pass@host/db',
    pool_size=10,
    max_overflow=20,
    pool_timeout=30
)
```

## Migrations

**Migration best practices:**
- Never edit old migrations
- Every migration must be reversible (rollback)
- Test migrations on copy of production data
- Run in transaction if possible
- Add indexes concurrently (non-blocking)
- For large tables, batch operations

**Schema change strategy:**
```sql
-- Bad: ALTER blocks entire table
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Good: Non-blocking in PostgreSQL
ALTER TABLE users ADD COLUMN phone VARCHAR(20) DEFAULT NULL;
-- Later, populate in batches:
UPDATE users SET phone = ... WHERE id BETWEEN 1 AND 1000;
```

## Data Integrity

**ACID properties:**
- Atomicity: All or nothing
- Consistency: Valid state always
- Isolation: Concurrent transactions don't interfere
- Durability: Committed data survives crashes

**Use transactions for multi-step operations:**
```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

**Handle concurrent updates:**
```sql
-- Optimistic locking with version
UPDATE posts 
SET content = 'new content', version = version + 1
WHERE id = 123 AND version = 5;

-- Pessimistic locking
SELECT * FROM posts WHERE id = 123 FOR UPDATE;
```

## Backup & Recovery

**Backup strategy:**
- Automated daily backups
- Point-in-time recovery enabled
- Test restore procedure regularly
- Store backups off-site
- Document recovery procedures

**Data retention:**
- Keep audit logs
- Soft delete for important data
- Archive old data to separate storage
- Implement data purging for GDPR compliance

## Common Anti-Patterns

❌ Using ORM without understanding SQL
❌ No indexes on foreign keys
❌ Too many indexes (slows writes)
❌ Using TEXT for everything
❌ No database constraints (relying only on app logic)
❌ FLOAT/DOUBLE for money
❌ Storing dates as strings
❌ No created_at/updated_at timestamps
❌ Inconsistent naming conventions
❌ Missing ON DELETE/ON UPDATE clauses
❌ Premature optimization without profiling
❌ No backup strategy
