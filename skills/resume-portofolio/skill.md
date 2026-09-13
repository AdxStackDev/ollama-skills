---
name: resume-portfolio
description: Guidance for writing ATS-friendly resumes and building developer portfolios that pass automated screening and read well to a human reviewer afterward. Use whenever the task is writing, reviewing, or restructuring a resume, cover letter, or portfolio site/page, or tailoring one of these to a specific job posting.
license: Complete terms in LICENSE.txt
---

# Resume and Portfolio

Approach this as a resume writer who has also built the applicant-tracking systems (ATS) that will parse the document first. Two audiences read this document in sequence — a parser, then a person — and both have to be satisfied, in that order. A resume that's beautiful to a human but unparseable to a machine never reaches the human; a resume a machine parses cleanly but that reads as generic keyword-stuffing loses the person in the first ten seconds. Optimize for both, without letting either compromise the other.

## How ATS parsing actually works (and what it means for format)

An ATS extracts plain text from the document and maps it to fields (name, contact, work history, skills, education) using structural cues — not visual layout. Anything that depends on visual layout to convey meaning is invisible to the parser.

- **File format**: prefer a .docx or a text-based (not scanned/image) PDF. If given a choice, .docx often parses more reliably across ATS platforms than PDF, since some ATS PDF parsers still mis-handle multi-column layouts or embedded fonts — but a clean, text-based single-column PDF is safe with almost any modern ATS. Never submit a resume as a scanned image or a design tool's flattened export (e.g. an image-based Canva export) — there is no text for the parser to read at all.
- **Layout**: single column, top to bottom, standard reading order. Multi-column layouts, text boxes, tables, and headers/footers are the most common cause of scrambled or dropped content — many parsers read left-to-right across the whole page width and will interleave a two-column resume's left and right content into nonsense, or skip header/footer text entirely (don't put contact info only in a header). If a template uses columns or a sidebar for skills, either avoid it or verify by copy-pasting the whole document into a plain text editor and checking the result is still coherent — that's the actual parser's-eye view.
- **Fonts and characters**: standard, embedded system fonts (Arial, Calibri, Georgia, Helvetica) — not a decorative or custom font that might not embed correctly. Avoid special characters, icons, or symbols in place of text (a phone icon instead of the word "Phone", a star rating for skill level) — parsers often drop these, and human reviewers scanning quickly don't need iconography to understand a phone number.
- **Section headers**: use conventional, exact labels the parser is trained to recognize — "Work Experience" or "Professional Experience," not "Where I've Made an Impact"; "Education," not "Learning Journey." Creative header names are a common way otherwise-strong resumes get misfiled by an ATS.
- **Dates and structure**: consistent, unambiguous date format throughout (e.g. "Jan 2022 – Aug 2026," not a mix of formats across entries). List experience in reverse-chronological order within each section — the format ATS platforms and recruiters both expect by default; deviate only with a strong specific reason.
- **No graphics for content**: a skills chart, a proficiency bar, or a logo used to convey a company/technology name carries no extractable text. If you want a visual skills representation, it belongs on the portfolio site, not the ATS-facing resume — put the equivalent as plain text on the resume.

## Content and keyword strategy

Passing the parse is necessary but not sufficient — most ATS platforms also rank or filter candidates by keyword match against the job posting, and a human reviewer (recruiter or hiring manager) reads whatever clears that bar next.

- **Mirror the job posting's language, precisely.** If the posting says "React Native," use "React Native," not just "React" or "mobile development" — an ATS keyword match is often literal string matching, not semantic. Pull the specific technologies, tools, and role titles from the posting itself and confirm each one you genuinely have appears verbatim somewhere on the resume (skills section and/or in the relevant bullet). Never claim a technology you don't have — the interview will surface the gap immediately, and misrepresenting skills undermines trust.
- **Include both the acronym and the spelled-out form** the first time a term appears where it's ambiguous (e.g. "Application Programming Interface (API)" is rarely necessary for a technical audience, but "Search Engine Optimization (SEO)" might matter for a role spanning technical and marketing audiences) — this covers ATS platforms that match on one form but not the other.
- **Every bullet leads with what changed, using an action verb, and quantifies the result wherever the number exists**: "Reduced API response time by 40% by adding Redis caching to the order-lookup endpoint," not "Responsible for backend performance." A reviewer skimming for 6–10 seconds needs the impact visible without parsing a sentence about responsibilities. Where a real number doesn't exist, use a concrete scope instead of a vague one ("Migrated a 40-table legacy MySQL schema to..." beats "Worked on database migration").
- **Tailor per application, not once.** A resume optimized for one specific posting's language will consistently outrank a generic all-purpose version against that posting's ATS ranking, even with identical underlying experience — the same work history described in the posting's vocabulary scores differently than the same work described in your own habitual vocabulary. This means the "master resume" is a working document you trim and reword per application, not a single static file.
- **Skills section**: a plain-text list (comma or line separated), grouped by category if it aids scanning (Languages / Frameworks / Databases / Cloud & DevOps) — grouping is for the human reader; the parser just needs the terms present as text. Don't pad with skills irrelevant to the target role just to lengthen the list; irrelevant keywords can dilute relevance scoring on some platforms rather than help it.
- **Length**: one page for most individual-contributor roles under ~10 years of experience; two pages is acceptable once experience genuinely doesn't fit, never as padding. Cut the oldest/least relevant roles before letting length creep.

## Structure and sections

Standard order, present the ones that apply:

1. **Header** — name, phone, email, location (city/region is enough; full address isn't expected), LinkedIn URL, portfolio/GitHub URL. All as plain text in the body, not only in a header/footer region.
2. **Summary** (optional, 2–3 lines) — only include if it adds specific signal ("Backend-leaning fullstack developer, 7 years, fintech and healthcare" is useful; "Hardworking team player seeking growth opportunities" is not — it's true of every candidate and wastes the reviewer's first reading seconds).
3. **Work Experience** — reverse chronological. Company, title, dates, location. 3–6 bullets per role, weighted toward the most recent/relevant roles; older roles can compress to 1–2 bullets.
4. **Skills** — grouped plain-text list as above.
5. **Projects** (especially valuable for developers — a strong project section can carry a resume when work history is thinner or is changing domains). Name, one-line description of what it does and for whom, the stack, and a link. Treat each like a mini work-experience bullet: what it does and what's notable about building it, not just a tech list.
6. **Education** — degree, institution, graduation year (omit year if it's a source of unwanted age signal and the role doesn't require verifying recency). Certifications can live here or in their own section if there are several relevant ones.

Omit an "Objective" section (superseded by Summary), an unlabeled photo (unusual and sometimes disqualifying depending on region/company EEO policy), and a References section (the phrase "references available on request" is a known filler that both ATS and human reviewers ignore).

## Portfolio (the human-facing counterpart)

The resume gets through the door; the portfolio is where a reviewer who's already interested goes deeper — so it can and should do everything an ATS-safe resume can't: visual hierarchy, live demos, written narrative, personality. It is not itself parsed by an ATS, so the constraints above don't apply here — this is where you can be as visually considered as the frontend-design skill describes.

- **Above the fold**: who you are and what you build, in concrete terms — "Fullstack developer building fintech and healthcare products with Laravel and React" tells a visitor more in one line than a generic "Welcome to my portfolio."
- **Project pages, not just a grid of thumbnails**: for each real project, show what problem it solved, your specific role and decisions (not just "I used React"), a real screenshot or working demo, and a link to the repo where relevant. A reviewer evaluating a fullstack candidate wants to see the reasoning behind a choice (why this database, why this architecture) as much as the finished screen.
- **Case-study depth on 2–3 projects beats shallow coverage of ten.** Pick the projects that best demonstrate the kind of work you want to be hired to do next, not just the most recent or most technically impressive in isolation.
- **Keep the code and the writing both current.** A portfolio linking to a project last touched three years ago, or a live demo that 404s, actively undercuts credibility more than having fewer projects would.
- **Make contact and resume access trivial**: a visible link to download the actual ATS-formatted resume, and a direct way to reach you — don't make a reviewer hunt for either.
- For the portfolio's own visual design and implementation choices (palette, typography, layout, avoiding templated defaults; HTML/CSS/Bootstrap/Tailwind/JS implementation), use the frontend-design skill together with this one — this skill covers what content belongs and why; frontend-design covers how to make it look distinctive rather than templated.

## Process: tailor, verify, review

1. **Start from a master resume** that has every role, bullet, and project you might ever use, written fully. Tailoring per application is then a subtraction-and-reword exercise, not a from-scratch rewrite each time.
2. **Read the target job posting closely** and extract its specific vocabulary (tech names, methodologies, role title) before touching the resume — tailor bullets and the skills section to mirror that language wherever it's honestly true of the candidate's experience.
3. **Verify parseability** by copy-pasting the final document into a plain text editor (or an ATS-checker tool if available) and confirming the extracted text is complete, correctly ordered, and free of scrambled columns or missing header/footer content.
4. **Proofread for the human pass**: no typos, consistent tense (past tense for past roles, present for current), consistent date/formatting style throughout, and every bullet passes the "so what" test — does this line tell a reviewer something that would make them want to talk to this candidate.
5. **Cross-check the portfolio and resume tell the same story** — the same project names, the same framing of your role, the same current focus — since a reviewer who visits both expects them to reinforce, not contradict, each other.