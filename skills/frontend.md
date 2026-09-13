---
name: frontend-design
description: Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one, implemented in HTML, CSS, Bootstrap, Tailwind CSS, and JavaScript. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults.
license: Complete terms in LICENSE.txt
---

# Frontend Design

Approach this as the design lead at a design studio known for giving every client a distinct visual identity that is not mistaken for anyone else's. This client has already rejected proposals that felt cliché or templated, and is paying for a distinctive point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take aesthetic risk if justified.

All builds under this skill are implemented as plain HTML, CSS, Bootstrap CSS, Tailwind CSS, and vanilla JavaScript — no React or other component frameworks. See the "Implementation stack" section below for how to choose and combine these tools for a given brief.

## Ground your designs in the subject matter

If the brief does not identify what the product or subject matter is, identify it yourself before designing, and confirm with the client. You can come up with one concrete subject, the design's audience, and the design's primary job, as a proposal. If there's any information in your memory about the client's preferences or context about what they're building, use that as a hint. The subject's industry, subject matter, materials, and vernacular are where distinctive visual choices come from — a design for a toy for girls aged 8–11 will be very aesthetically different from a dashboard for financial analysts. Build with the brief's real content and subject matter throughout.

## Design principles

For web designs, the hero is the first thing viewers will see. Open with the most characteristic thing in the subject's world, in the form that is most appropriate: a headline, an image, an animation, a live demo, an interactive moment, or other treatments. Be deliberate with your choice: a big number with a small label, supporting stats, and a gradient accent is the default treatment, so only use it if that's truly the best option.

Typography carries the personality of the page. You don't need a different typeface for display or headline text and body content: use one family or two, and if two, make them clearly distinct.

Choose your typefaces deliberately, not the default families you would reach for on any other project, and set a clear type scale following the default guidance of The Elements of Typographic Style with intentional weights, widths, and spacing. When type is used as a headline or visual element, use the type treatment itself as an active part of the design, not a neutral delivery vehicle for the content.

Default to line lengths of less than 80 characters. Serif typefaces can have slightly longer line lengths; give serif body text slightly more line-height than a sans-serif.

Avoid these default typographic treatments; they are the commonest tells of a generated page:
- Accenting just a single word or phrase in a headline, like putting one word in italic/bold or a different color.
- Using all caps for labels.
- Adding unnecessary typographic labels above content.

Visual structure is information. Structural devices like outlines, borders, numbering, eyebrows, dividers, labels, etc., encode useful information about the content rather than decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence — like a stepped process or a timeline. Before adding numbered markers, check the content really is a sequence.

Use non-user-triggered motion sparingly and deliberately, only to draw attention. A single orchestrated moment — one page-load sequence or one reveal — lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed. In this stack, implement such motion with CSS transitions/animations first, and vanilla JavaScript (IntersectionObserver, event listeners) only where CSS alone can't express the behavior.

Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy and placeholder content. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.

## Implementation stack

Every build uses some combination of plain HTML, plain CSS, Bootstrap CSS, Tailwind CSS, and vanilla JavaScript. Pick deliberately per brief rather than defaulting to the same combination every time.

**Choosing your CSS approach:**
- **Plain CSS** — use for anything that carries the design's distinctive identity: custom type scale, the token system's colors, bespoke layout, the one bold signature element. Hand-rolled CSS is where aesthetic risk and specificity live; don't outsource it to a utility framework.
- **Tailwind CSS** — use for rapid utility-driven layout and spacing (flex/grid scaffolding, responsive breakpoints, spacing scales) once the token system is decided. Configure Tailwind's theme (colors, fontFamily, spacing) to match your token system rather than reaching for default Tailwind values (default blue-500, default gray scale, default font stack) — using Tailwind's un-configured defaults is itself a templated tell.
- **Bootstrap CSS** — use selectively for structural/component scaffolding (grid system, modals, nav, forms) when the brief calls for a conventional, componentized UI (e.g. an admin panel, a form-heavy dashboard) and speed matters more than a fully bespoke look. Always override Bootstrap's default theme variables (`--bs-primary`, `--bs-font-sans-serif`, `--bs-border-radius`, etc.) to match your token system — shipping Bootstrap's default blue (#0d6efd) and default component shapes unmodified is a strong templated tell and should be avoided per the calibration list below.
- Don't combine Bootstrap and Tailwind on the same page unless the brief specifically requires it (e.g. migrating one section at a time) — their utility classes and resets can conflict. Prefer plain CSS + Tailwind, or plain CSS + Bootstrap, as your default pairing.

**Structuring markup and files:**
- Semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`) over generic `<div>` soup — this also gives you real hooks for CSS specificity and JS selectors.
- Keep CSS in a dedicated stylesheet (or a clearly separated `<style>` block), not inlined on elements, except for one-off dynamic values JavaScript sets at runtime.
- Vanilla JavaScript only: no framework runtime. Use `document.querySelector`/`addEventListener`, small pure functions, and `IntersectionObserver`/`requestAnimationFrame` for scroll- or load-triggered moments. Keep JS focused on behavior (interaction, state, animation triggers) — not layout, which belongs in CSS.

**Avoiding CSS specificity collisions (stack-specific):**
This stack multiplies the classic specificity trap the base skill warns about, because you now have three sources of rules — plain CSS, Bootstrap's own classes, and Tailwind's utility classes — all potentially targeting the same element.
- When plain CSS and Bootstrap disagree on the same element, prefer overriding via a custom class with equal or higher specificity rather than `!important`; reserve `!important` for narrow, documented overrides of a Bootstrap utility you can't otherwise reach.
- When plain CSS and Tailwind utility classes disagree, remember Tailwind utilities are single-property and high-specificity by convention — don't fight them with a broad type/class selector in plain CSS; instead scope your custom CSS to a wrapper class and let Tailwind own the utility-level properties inside it.
- Avoid mixing a type-based selector (e.g. `.card`) with an element-based one (e.g. `.card h3`) targeting the same property from two different files — this is the exact cancel-out trap the base skill flags, and it's easier to hit accidentally when Bootstrap/Tailwind resets are also in play. Grep for the property across all three sources before assuming a style isn't applying.

## Process: plan, review against the brief, build, critique

For calibration, AI-generated design right now clusters around some traits:
1. a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta or warm-clay accent (often near #D97757 — Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell);
2. a near-black background with a single bright acid-green or vermilion accent;
3. a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns;
4. the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration;
5. template chrome that appears whatever the subject: a tracked-out ALL-CAPS eyebrow label above every heading; meta strings joined with middle dots ('A · B · C'); labels built as 'WORD — fragment' with a spaced em dash; tinted near-black (#0B0B0B, #111) standing in for black; a monospace face for small data labels; a '→' appended to link and button text.
6. (stack-specific) shipping Bootstrap's default theme (default blue #0d6efd, default border-radius, default font stack) or Tailwind's un-configured default palette and type scale unmodified — this reads as "didn't bother to theme it" as clearly as any of the above.

All traits are legitimate for some briefs, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly — the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults. As with a hired human designer, there's often a careful balance between doing what you're good at and taking each project as a chance to experiment and learn.

Work in two passes. First, brainstorm a short design plan based on the client's design brief: create a compact token system with color, type, layout, and principles.
- Color: describe the core base palette as 4–6 named hex values.
- Type: the typefaces and their roles.
- Layout: a layout concept, using one-sentence prose descriptions and ASCII wireframes to ideate and compare. Include alignment guidance; should the content be left aligned, center aligned, justified?
- Principles: the high-level guidance for what makes this page unique.
- Stack: which of plain CSS, Bootstrap, and Tailwind you'll use for which parts, and why (see Implementation stack above).

Then review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page (work through a similar prompt to see if you arrive somewhere similar) rather than a choice made for this specific brief — revise that part, say what you changed and why. Only after you've confirmed the relative uniqueness of your design plan should you start to write the code, following the revised plan.

When writing the code, be careful of structuring your CSS selector specificities. It's easy to generate CSS classes that cancel each other out (especially with a type-based selector like .section and an element-based selector like .cta). This can happen often with padding/margin between sections. In this stack, this applies equally to interactions between your plain CSS and any Bootstrap or Tailwind classes on the same element — see "Avoiding CSS specificity collisions" above.

## Restraint and self-critique

Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Build to a quality floor without announcing it: responsive down to mobile (test Bootstrap's/Tailwind's breakpoint behavior explicitly, don't just assume the framework handles it), visible keyboard focus, reduced motion respected (`prefers-reduced-motion` in your CSS transitions and in any JS-driven animation), visually accessible, harmonious color palettes. Critique your own work as you build, taking screenshots to review if your environment supports it — a picture is worth 1000 tokens. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. Human creatives have memory and always try to do something new, so if you have a space to quickly jot down notes about what you've tried, it can help you in future passes.

## More on writing in design

Words appear in a design for one reason: to make it easier to understand and use. They are design content, not decoration. Bring the same intentionality and minimalism to copywriting that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.

Write from the end user's perspective. Name things by what users will understand in simple language, not by how the system is built. A user manages notifications, not webhook config. Describe what something is or does in plain terms rather than selling it. Being specific and legible to new users is always better than being clever.

Use active voice as default. A CTA says exactly what happens when it is used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.

Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act.

Keep the tone conversational: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each written element do exactly one job.