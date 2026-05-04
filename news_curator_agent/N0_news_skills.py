NEWS_AGENT_SKILLS = {
"NEWS_SEARCH": """
    ## SKILL: NEWS SEARCH
    Search for the latest news on a topic and identify the lead story.

    ### Expected Input
    - Search topic (e.g., "Brazilian politics," "economy," "technology")

    ### Process
    1. Search for the most recent news on the topic.
    2. Identify the lead story (the most relevant and current).
    3. Extract keywords for deeper investigation.

    ### Output Format
    Return exactly:
    1. **Title**: the exact title of the lead story.
    2. **Summary**: 2-3 sentences explaining what happened.
    3. **Source**: the outlet where it was found.
    4. **Keywords**: terms to search for more sources on this same story.

    ### Rules
    - Prioritize news from the current day.
    - Choose the story with the greatest impact and repercussion.
    - Keywords must be specific enough to find the same story in other outlets.
    """,

"SOURCE_INVESTIGATION": """
    ## SKILL: JOURNALISTIC SOURCE INVESTIGATION
    Workflow to investigate a news story across multiple sources and produce a structured dossier of evidence.

    ### Expected Input
    - Title or summary of the news to be investigated.
    - Keywords for search (optional).

    ### Output Format
    Produce the dossier exactly in this structure:
    ## COLLECTED SOURCES
    - **Outlet** | URL | Date/time of publication
    - Reported facts (data, numbers, names, direct quotes)
    - Exclusive information from this source

    ## TIMELINE
    Events in chronological order with the source in brackets.

    ## POINTS OF CONSENSUS
    Facts that ALL or most sources confirm.

    ## CONTRADICTIONS AND DIVERGENCES
    Be specific about differences in values, names, and dates.

    ## GAPS
    What no source clarified or what still needs to be confirmed.

    ### Rules
    - Minimum of 3 sources, ideally 5 or more.
    - Prioritize credible outlets (Reuters, AP, AFP, major newspapers).
    - Never invent data.
    """,

"FACTUAL_VERIFICATION": """
    ## SKILL: FACTUAL VERIFICATION
    Exhaustive critical analysis of a journalistic evidence dossier.

    ### Process
    1. **Initial Cross-referencing**: Classify as CONFIRMED, DISPUTED, or NOT VERIFIED.
    2. **Resolving Contradictions**: Search for official primary sources or raw data.
    3. **Filling Gaps**: Conduct specific searches on open points.
    4. **Verifying Unique Facts**: Seek at least 2 additional sources for single-source info.
    5. **Final Consistency**: Review dates, names, and values.

    ### Output Format
    - ## CONFIRMED FACTS
    - ## RESOLVED DISPUTED FACTS
    - ## UNRESOLVED DISPUTED FACTS
    - ## NOT VERIFIED FACTS
    - ## RESOLVED GAPS
    - ## PENDING GAPS
    - ## WRITER'S ALERT (Caveats and overall confidence level)

    ### Rules
    - Execute IMMEDIATELY without asking for permission.
    - Explain the probable reason for unresolved contradictions.
    """,

"NEWS_WRITING": """
    ## SKILL: JOURNALISTIC NEWS WRITING
    Write the news as if it were being published now in a real press outlet.

    ### Structure
    - **Headline**: New, strong, factual headline.
    - **Lead**: Answer What, Who, When, Where, and Why.
    - **Body**: Inverted pyramid. Use numerical citations [1], [2] for every piece of data.
    - **Context**: Broader scenario and why it matters.
    - **References**: Numbered list at the end with full URLs.

    ### Non-negotiable Rules
    - Fluent English, professional and impartial tone.
    - ALWAYS use numerical citations [1], [2], [3] in the body.
    - ALWAYS include the "References" section with full URLs.
    - NEVER use bullet points in the body - use running PARAGRAPHS.
    - Length: 400-600 words.
    """
}

