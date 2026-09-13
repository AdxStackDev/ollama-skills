# Example: portfolio project case study (not ATS-facing — for the human-read portfolio site)

This is the kind of depth the skill recommends for 2–3 flagship projects on a
portfolio, contrasted with the shallow version most portfolios default to.

## Shallow version (avoid — this is the generic default)

"Inventory Tracker
Tech: React, Laravel, MySQL
A web app for tracking inventory.
[View on GitHub]"

Problem: this tells a reviewer what was built but nothing about the reasoning,
the role, or the difficulty — it reads the same for a weekend project and a
production system.

## Case-study version (what the skill recommends)

### Inventory Tracker

**The problem:** A 12-person warehouse team was tracking stock levels in a
shared spreadsheet that regularly went out of sync between shifts, causing
overselling on two occasions in one month.

**What I built:** A fullstack inventory app — Laravel + MySQL on the backend,
React on the frontend — with real-time-enough stock counts (polled every 30s,
not full websockets, since the team's usage didn't justify that complexity),
role-based logins so warehouse staff could update counts but only managers
could adjust reorder thresholds, and automated low-stock email alerts.

**A decision worth explaining:** I chose polling over websockets deliberately.
The team checks the dashboard a few times per shift, not continuously, so the
added infrastructure complexity of websockets wasn't justified by the actual
usage pattern — a good example of matching the technical solution to the real
problem rather than the more impressive-sounding one.

**Outcome:** Replaced the spreadsheet entirely within the first week of
rollout; no overselling incidents in the 4 months since launch.

**Stack:** Laravel, MySQL, React, deployed on AWS EC2.

[Live demo] [View on GitHub]

---

Why this version is stronger: it shows the problem (not just the solution),
names one specific technical decision and the reasoning behind it (per the
skill's guidance that a portfolio should show "your specific role and
decisions, not just 'I used React'"), and gives a concrete outcome instead of
letting the project speak for itself with no framing.
