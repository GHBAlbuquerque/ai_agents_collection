---
name: source-verification
description: Verify and cross-reference multiple journalistic sources regarding a news story, compiling a structured dossier with evidence, timeline, consensus, contradictions, and gaps. Use this when you need to investigate sources, cross-reference information from different outlets, or build an evidence dossier about a news story.
metadata:
  version: "1.0.0"
  tags: ["journalism", "verification", "sources", "dossier"]
---

# Source Verification

Workflow to investigate a news story across multiple sources and produce a structured evidence dossier.

## When to use

- You received a news story and need to verify it against other sources.
- You need to build an evidence dossier on a specific subject.
- You want to cross-reference information from different media outlets.

## Expected Input

- Title or summary of the news story to be verified.
- Search keywords (optional — if not provided, extract them from the title).

## Process

1.  **Search for sources**: Use the keywords to find the same news story in different outlets (minimum 3, ideally 5).
2.  **Extract facts**: For each source, record data, numbers, names, and direct quotes.
3.  **Cross-reference information**: Identify points of consensus, contradictions, and exclusive details.
4.  **Assemble dossier**: Produce the structured document using the format below.

## Output Format

Produce the dossier exactly in this structure:

```
## COLLECTED SOURCES

For each source found:
- **Outlet** | URL | Publication date/time
- Reported facts (data, numbers, names, direct quotes)
- Exclusive information from this source (what only this source provides)

## TIMELINE

Events in chronological order with the source in brackets.
Ex: "10:00 AM - Government announces measure X [Folha] [Reuters]"

## POINTS OF CONSENSUS

Facts that ALL or most sources confirm.

## CONTRADICTIONS AND DIVERGENCES

Data that differs between sources. Be specific:
- Ex: "Folha says R$ 2.5 billion; Estadão says R$ 2.8 billion; Reuters says USD 500 million"
- Ex: "G1 claims the decision was unanimous; Valor says there were 2 opposing votes"

## GAPS

What no source has clarified or what still needs confirmation.
```

## Rules

- Minimum of **3 sources**, ideally **5 or more**.
- Prioritize outlets with recognized credibility (Reuters, AP, AFP, major newspapers).
- Never invent data - record only what the sources actually published.
- Be specific about contradictions: cite exact values, names, and dates from each source.
- Always include the URL for each source whenever available.