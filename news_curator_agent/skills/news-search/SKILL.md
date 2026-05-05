---
name: news-search
description: Search for and identify the most relevant and current news story about a topic, returning the title, summary, source, and keywords. Use when you need to search for recent news, identify the main story of the day, or start a journalistic investigation.
metadata:
  version: "1.0.0"
  tags: ["journalism", "search", "news"]
---

# News Search

Search for the most recent news on a topic and identify the main story.

## Expected Input

- Search topic (e.g., "Brazilian politics", "economy", "technology")

## Process

1. Search for the **most recent** news about the topic
2. Identify the main news story (the most relevant and current)
3. Extract keywords for deeper investigation

## Output Format

Return exactly:

1. **Title**: the exact title of the main news story
2. **Summary**: 2-3 sentences of what happened
3. **Source**: the outlet where it was found
4. **Keywords**: terms to search for more sources about this same story

## Rules

- Prioritize news from the current day
- Choose the news with the greatest impact and repercussions
- Keywords must be specific enough to find the same story in other outlets