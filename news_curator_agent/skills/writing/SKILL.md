---
name: writing
description: Write a professional journalistic article based on a fact-checking report, featuring an original headline, lead, inverted pyramid body, and context. Use when you need to write a news story, draft an article, produce journalistic text, or transform a dossier into a publishable news piece.
metadata:
  version: "1.0.0"
  tags: ["journalism", "writing", "article"]
---

# Journalistic Writing

Write the news story as if it were being published right now by a real media outlet.

## Expected Input

- Factual verification report (produced by the fact-checking skill)

## Article Structure

### Headline
Create a NEW journalistic headline-do not copy from the sources. Factual, strong, and informative.

Examples of good headlines:
- "Federal government announces R$ 15 billion cut in 2026 Budget"
- "Supreme Court reaches majority to validate 'marco temporal' for indigenous lands"
- "Dollar drops to R$ 5.12 following Fed's signaling on interest rates"

### Lead (1st paragraph)
Answer: WHAT, WHO, WHEN, WHERE, and WHY. It must be able to stand alone.

### Body (3-5 paragraphs)
- Inverted pyramid (most important facts first)
- Natural attribution: "According to the Ministry...", "Per data from the IBGE..."
- Handling divergences naturally: "While Outlet A points to R$ 2.5 billion [1], Outlet B estimates R$ 2.8 billion [2]"
- Unverified facts with caveats: "this information has not yet been officially confirmed"
- Concrete numbers, dates, names, and data
- Direct quotes in quotation marks when available
- **MANDATORY CITATIONS**: Whenever mentioning a data point, fact, or quote from a source, insert the corresponding numerical reference in brackets-e.g., [1], [2], [3]. Each number must correspond to an entry in the "References" section at the end of the text.

### Context (1 paragraph)
The broader scenario: what happened previously and why this matters.

### References
At the end of the article, include a `## References` section with a numbered list of ALL sources cited in the text, in the following format:

```
## References

[1] Media Outlet Name - Article Title. URL
[2] Media Outlet Name - Article Title. URL
[3] Media Outlet Name - Article Title. URL
```

- Use the same numbering as the citations [1], [2], etc., in the body text.
- Include the full URL for each source (extracted from the investigation/verification dossier).
- If the exact title is unavailable, use a brief description of the content.
- ALL sources mentioned in the body MUST appear in the reference list.
- ALL entries in the reference list MUST be cited at least once in the body.

## Non-negotiable Rules

- Fluent English, professional journalistic tone.
- Serious, direct, impartial-no opinions, no unnecessary adjectives.
- ALWAYS use numerical citations [1], [2], [3] in the body to indicate the source of each piece of information.
- ALWAYS include the "References" section at the end with full URLs.
- NEVER use bullet points in the body-write in continuous PARAGRAPHS.
- NEVER invent data, names, or quotes.
- Length: 400-600 words (excluding the references section).
- Must look like it came from a real newsroom, NOT an AI.