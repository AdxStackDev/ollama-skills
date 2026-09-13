# Example: Weak bullets rewritten as ATS-friendly, impact-led bullets

Each pair shows the same underlying work described two ways. The "Weak" version is
common, generic, and low-signal. The "Strong" version follows the skill's rule:
lead with an action verb, name the specific technology from the job posting,
and quantify the result wherever a real number exists.

## Backend / API example

Weak:
"Responsible for backend development and API maintenance."

Strong:
"Built and maintained 15+ REST API endpoints in Laravel, reducing average response
time by 35% after introducing Redis caching on high-traffic order-lookup routes."

Why it's stronger: "Responsible for" describes a duty, not an outcome. The strong
version names the framework (Laravel), the caching tool (Redis) — both likely
keywords from a job posting — and a measured result (35%, 15+ endpoints).

## Frontend example

Weak:
"Worked on the company's React dashboard."

Strong:
"Rebuilt the analytics dashboard in React, cutting initial page load from 4.2s to
1.1s by lazy-loading chart components and memoizing expensive re-renders."

Why it's stronger: "Worked on" is invisible to both ATS ranking and a human
reviewer skimming for impact. The strong version shows a before/after number and
names the specific technique (lazy-loading, memoization) a reviewer would recognize.

## Fullstack / project example

Weak:
"Developed a web application for tracking inventory."

Strong:
"Designed and shipped a fullstack inventory-tracking app (Laravel + MySQL backend,
React frontend) used daily by a 12-person warehouse team, replacing a manual
spreadsheet process."

Why it's stronger: names both layers of the stack (a fullstack role should show
both), and quantifies the audience/impact (12-person team, replaced a manual
process) instead of just naming the deliverable.

## No real number available

Weak:
"Helped improve database performance."

Strong (still no fabricated number, but scoped concretely):
"Diagnosed and fixed N+1 query issues across the order-management module by adding
eager loading in Eloquent, resolving the slowest reported page-load complaints."

Why it's stronger: never invent a metric you don't have. Instead, make the scope
and outcome concrete ("order-management module," "eager loading in Eloquent,"
"slowest reported complaints") rather than leaving it vague ("helped improve").

## Junior-developer mentoring example (from the skill's collaboration section)

Weak:
"Assisted with onboarding new team members."

Strong:
"Onboarded 2 junior developers onto the Laravel codebase, writing setup docs and
pairing on their first 3 feature tickets each, cutting their ramp-up time from an
estimated 3 weeks to under 1."
