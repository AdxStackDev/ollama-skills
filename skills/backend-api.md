---
name: backend-api
description: Guidance for designing and implementing RESTful APIs and backend services with best practices for security, performance, and maintainability
license: Complete terms in LICENSE.txt
---

# Backend API Design

Build APIs that are secure, performant, and developer-friendly. Think like a platform engineer designing an API that thousands of developers will integrate with — every decision about endpoints, auth, error handling, and data formats affects their experience.

## Core Principles

**Design for the client, not the database**. API endpoints should reflect the client's mental model and use cases, not your internal database schema. A mobile app listing products doesn't need 47 fields per item; it needs exactly what fits on screen.

**Be consistent everywhere**. Use the same patterns for authentication, pagination, filtering, error responses, and naming across all endpoints. Developers should be able to predict how a new endpoint works based on the ones they already know.

**Fail gracefully and informatively**. Every error response should tell the client exactly what went wrong and how to fix it. A 400 with `{"error": "invalid request"}` is useless. A 400 with `{"error": "missing_field", "field": "email", "message": "Email address is required"}` is actionable.

## REST Endpoint Design

**Use HTTP methods correctly:**
- GET: Retrieve resources (idempotent, no side effects)
- POST: Create new resources
- PUT: Replace entire resource
- PATCH: Partial update
- DELETE: Remove resource

**Structure URLs hierarchically:**
```
GET    /api/v1/users              # List users
GET    /api/v1/users/123          # Get specific user
POST   /api/v1/users              # Create user
PATCH  /api/v1/users/123          # Update user
DELETE /api/v1/users/123          # Delete user
GET    /api/v1/users/123/posts    # User's posts (nested resource)
```

**URL naming conventions:**
- Use nouns, not verbs (`/users` not `/getUsers`)
- Plural for collections (`/users` not `/user`)
- Lowercase with hyphens for multi-word (`/user-profiles`)
- Keep nesting to 2 levels maximum
- Use query params for filtering, sorting, pagination

**Version your API** from day one. Use URL versioning (`/v1/`) or header versioning. Never break existing clients without a deprecation window.

## Request & Response Patterns

**Standard response envelope:**
```json
{
  "data": { },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "abc-123"
  }
}
```

**Pagination (cursor-based preferred):**
```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIzfQ",
    "prev_cursor": "eyJpZCI6OTh9",
    "has_more": true
  }
}
```

**Error responses:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "issue": "invalid_format",
        "message": "Email must be a valid email address"
      }
    ],
    "request_id": "abc-123"
  }
}
```

**Use appropriate status codes:**
- 200: Success
- 201: Created
- 204: Success with no content
- 400: Client error (bad request)
- 401: Unauthenticated
- 403: Unauthorized (authenticated but insufficient permissions)
- 404: Not found
- 409: Conflict (duplicate resource)
- 422: Unprocessable (validation failed)
- 429: Rate limited
- 500: Server error
- 503: Service unavailable

## Security First

**Authentication & Authorization:**
- Use OAuth 2.0 or JWT for token-based auth
- Never pass tokens in URL params (use Authorization header)
- Implement token refresh flows
- Validate permissions on every request
- Rate limit by user/IP

**Input validation:**
- Validate all inputs server-side (never trust client validation)
- Use allowlists, not denylists
- Sanitize inputs to prevent injection attacks
- Validate content types and file uploads
- Set maximum request sizes

**Sensitive data:**
- Never log passwords, tokens, or PII
- Use HTTPS everywhere (no HTTP fallback)
- Hash passwords with bcrypt/argon2
- Encrypt sensitive fields at rest
- Implement proper CORS policies

## Performance & Scalability

**Query optimization:**
- Implement pagination on all list endpoints
- Use database indexes on frequently queried fields
- Avoid N+1 queries (use joins or batch loading)
- Cache frequently accessed data (Redis, CDN)
- Support field selection (`?fields=id,name,email`)

**Rate limiting:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1634567890
```

**Async operations:**
- Use webhooks or polling for long-running tasks
- Return 202 Accepted with status endpoint
- Provide job ID for status checking

## Data Validation

**Validation rules should be:**
- Specific: "Email must contain @" not "Invalid email"
- Consistent: Same field validated same way everywhere
- Client-friendly: Return all errors at once, not one at a time
- Type-safe: Validate types, formats, ranges, patterns

**Example validation:**
```python
{
  "email": {
    "required": true,
    "type": "email",
    "max_length": 255
  },
  "age": {
    "required": false,
    "type": "integer",
    "min": 0,
    "max": 150
  },
  "role": {
    "required": true,
    "type": "string",
    "enum": ["admin", "user", "guest"]
  }
}
```

## Documentation

**Every endpoint needs:**
- Purpose and use case
- Full URL path
- HTTP method
- Authentication requirements
- Request body schema (with examples)
- Response schema (with examples)
- Error codes and meanings
- Rate limits

**Use OpenAPI/Swagger** for interactive documentation. Developers should be able to test endpoints directly from docs.

## Testing Strategy

**Test coverage must include:**
- Happy path (valid inputs, expected outputs)
- Authentication/authorization (valid/invalid tokens, permissions)
- Validation errors (missing fields, wrong types, out of range)
- Edge cases (empty lists, null values, max sizes)
- Error handling (database down, external service timeout)
- Performance (concurrent requests, large payloads)

## Monitoring & Observability

**Log these for every request:**
- Request ID (generated per request)
- Endpoint and method
- Response status and time
- User/client identifier
- Error stack traces

**Track these metrics:**
- Request rate (per endpoint)
- Response times (p50, p95, p99)
- Error rates by status code
- Rate limit hits
- Database query times

## Code Structure

**Organize by domain, not by type:**
```
/api
  /users
    routes.py
    models.py
    schemas.py
    service.py
  /posts
    routes.py
    models.py
    schemas.py
    service.py
  /common
    auth.py
    errors.py
    validators.py
```

**Separate concerns:**
- Routes: HTTP handling only (parse request, call service, format response)
- Services: Business logic
- Models: Database interactions
- Schemas: Validation and serialization
- Middleware: Cross-cutting concerns (auth, logging, error handling)

## Common Anti-Patterns to Avoid

❌ Exposing internal IDs (use UUIDs or opaque tokens)
❌ Accepting SQL/NoSQL queries directly
❌ Returning different structures for same endpoint
❌ Using GET requests for state-changing operations
❌ Ignoring idempotency for POST/PUT/PATCH
❌ Returning 200 for errors
❌ Over-fetching (sending unnecessary data)
❌ Under-fetching (requiring multiple requests for related data)
❌ No pagination on list endpoints
❌ Inconsistent date formats (always use ISO 8601)

## Idempotency

**For POST/PATCH/DELETE:**
- Accept Idempotency-Key header
- Store request signature with result
- Return same result for duplicate keys
- Expire keys after 24 hours

## Backwards Compatibility

**Safe changes:**
- Adding new optional fields to requests
- Adding new fields to responses
- Adding new endpoints
- Making required fields optional

**Breaking changes (need new version):**
- Removing fields
- Renaming fields
- Changing field types
- Making optional fields required
- Changing response structure

When introducing breaking changes, deprecate the old version with:
- Warning headers in responses
- Documentation of migration path
- Sunset date announcement
- Sufficient transition period (3-6 months minimum)
