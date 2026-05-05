---
name: fact-checking
description: Verify facts from a journalistic dossier with exhaustive critical analysis, cross-referencing sources, resolving contradictions, filling gaps, and classifying each fact by confidence level. Use when you need to fact-check, verify facts, resolve contradictions between sources, or classify information reliability.
metadata:
  version: "1.0.0"
  tags: ["journalism", "fact-check", "verification"]
---

# Fact-Checking

Exhaustive critical analysis of a journalistic evidence dossier.

## Expected Input

- Evidence dossier (produced by the source-verification skill)

## Process

Execute ALL steps in sequence, without asking for permission:

### Step 1 - Initial Cross-referencing
Compare each fact across all sources. Classify as:
- **CONFIRMED**: 2+ sources agree
- **DISPUTED**: sources diverge
- **UNVERIFIED**: only 1 source

### Step 2 - Resolving Contradictions
For each DISPUTED fact:
1. Search for an official/primary source (government, official statement, Reuters/AP/AFP)
2. Search for raw data (reports, documents, balance sheets)
3. If new information is found, re-evaluate
4. If it persists, search with different terms or international sources
5. After 3+ attempts without resolution → classify as "unresolved" with the probable reason

### Step 3 - Filling Gaps
For each gap:
1. Conduct a specific search on the open point
2. Try alternative sources (official sites, international agencies)
3. Reformulate the search with different terms
4. After 2+ attempts → mark as "pending - available sources exhausted"

### Step 4 - Verification of Single Facts
For each fact from a single source:
1. Search in at least 2 additional sources
2. If confirmed → promote to CONFIRMED
3. If contradicted → move to DISPUTED and repeat Step 2
4. If not found → keep as UNVERIFIED with an alert

### Step 5 - Final Consistency
Review dates, names, values, and quotes throughout the report.

## Output Format

```
## CONFIRMED FACTS
Facts with a high degree of confidence + sources that confirm them.

## RESOLVED DISPUTED FACTS
Original version from sources → what was found → final verdict.

## UNRESOLVED DISPUTED FACTS
What each source says, searches performed, probable reason, recommendation to the writer.

## UNVERIFIED FACTS
Information from a single source not corroborated + searches attempted.

## RESOLVED GAPS
Gaps filled + source used.

## PENDING GAPS
What remains unanswered + searches attempted.

## WRITER'S ALERT
- What can be AFFIRMED safely
- What MUST have a caveat (and which one)
- What SHOULD NOT be published without additional confirmation
- General confidence level (high/medium/low)
```

## Rules

- Execute IMMEDIATELY, without asking for permission or asking questions
- Perform all necessary searches before classifying as "unresolved"
- Explain the probable reason for each unresolved contradiction
- Be specific: cite exact values, names, and dates