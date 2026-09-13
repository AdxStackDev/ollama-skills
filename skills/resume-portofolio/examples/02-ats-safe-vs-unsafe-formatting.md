# Example: ATS-unsafe formatting choices vs. their safe equivalents

Each row shows a formatting choice that risks breaking or confusing ATS parsing,
and the safe replacement described in the skill.

## Layout

Unsafe: Two-column layout — skills sidebar on the left, experience on the right.
Safe: Single column, top to bottom. Skills section as its own full-width block,
placed after Experience.
Why: many parsers read left-to-right across the full page width and will
interleave the two columns' text out of order.

## Contact info placement

Unsafe: Name, phone, and email placed inside the document's header/footer region.
Safe: Name, phone, email, location, LinkedIn/portfolio links placed as normal
body text at the top of the first page.
Why: some ATS parsers skip header/footer regions entirely, so contact info placed
there may never be extracted.

## Section headers

Unsafe: "Where I've Made an Impact" (as a stand-in for a work history section).
Safe: "Work Experience" or "Professional Experience."
Why: ATS platforms are trained to recognize conventional section labels; creative
labels risk the section not being mapped to the right field at all.

## Skill representation

Unsafe: A visual proficiency bar (e.g. a 4-out-of-5-filled graphic next to "React").
Safe: Plain text list — "React, React Native, JavaScript (ES6+)."
Why: graphics carry no extractable text; the parser sees nothing where the bar is.

## Dates

Unsafe: Mixed formats across entries — "Jan 2022 - Present" in one role,
"2021–2022" in another, "March '20 to Feb '21" in a third.
Safe: One consistent format throughout — "Jan 2022 – Present," "Mar 2021 – Feb 2022."
Why: consistency helps both the parser's date-field extraction and a human
reviewer scanning quickly for recency and tenure.

## File type

Unsafe: A Canva-exported flattened image, or a scanned/photographed resume.
Safe: A text-based .docx, or a text-based (not scanned) single-column PDF.
Why: an image has no underlying text at all — the parser extracts nothing.

## Verification step

After formatting, copy the entire resume's text and paste it into a plain text
editor (Notepad, TextEdit, a markdown file). If the pasted result reads in the
correct order with nothing missing or scrambled, the layout is ATS-safe. If
sentences from two different sections are interleaved, or the contact info is
missing, the layout needs to be simplified.
