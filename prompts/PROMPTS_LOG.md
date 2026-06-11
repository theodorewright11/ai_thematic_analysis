# Prompt Development Log

This file documents the evolution of each prompt variant, showing full text and rationale for changes. For exact diffs, see git history.

---

## Engineered Variant

### Version 1

You are predicting what a trained, expert qualitative researcher would identify when conducting a thematic analysis of public comments.


<background>
The data at the bottom of this prompt are comments submitted by members of the public - primarily ALS patients, their families, and caregivers - in response to an FDA guidance document on drug development for Amyotrophic Lateral Sclerosis (ALS). Each public comment is referred to as a data item. ALS is a terminal neurodegenerative disease with no cure and limited treatments, with a typical life expectancy of 2-5 years after diagnosis. The FDA opened a public commenting period on its draft guidance and received these responses.
</background>


<research_question>
What are the experiences and perspectives of the ALS community as expressed in their public comments to the FDA regarding ALS drug development policy?
</research_question>


<task>
Conduct a thematic analysis of the data. Identify the themes that capture meaningful patterns across the data in relation to the research question.
</task>


<guidelines>
Follow these guidelines when conducting your analysis:
- Think carefully about each pattern before committing to it as a theme. Not every observable pattern is a theme - it must capture something meaningful in relation to the research question.
- Support each theme with multiple verbatim quotes from different data items where possible to ensure the theme is adequately justified.
- Themes can range from surface-level patterns in what the data explicitly state to deeper more interpretive patterns that require drawing on broader knowledge to identify. Both levels are valid. What matters is that themes are meaningful to the research question.
- Identify as many themes as the data supports. Do not force themes where the pattern is weak, and do not combine distinct patterns into a single theme.
- Some data items may support multiple themes.
- Remember that if data items express conflicting perspectives, that itself may be part of a theme. 
- Give equal attention to all data. Do not let more vivid or lengthy data items dominate the analysis.
- A theme's importance is not determined by how many data items mention it. A pattern appearing in a few data items can be a meaningful theme if it captures something meaningful for the research question.
- The research question guides what to look for - the themes should be specific patterns you find in the data, not categories of what the research question asks about.
</guidelines>


<output>
Report your full analysis as a SINGLE JSON object - and nothing else outside it - matching the schema below.

For each theme, use the reasoning field to think through what you observe. It is your space to show and work through what you noticed and why it matters before committing to a theme name and definition.


Schema:

{
  "themes": [
    {
      "reasoning": "The pattern you observed across the data that led to this theme: what you noticed, which data items exemplify it, and why it constitutes a meaningful pattern."
      "name": "Short, specific theme label (a phrase, not a sentence).",
      "definition": "What the theme captures, where its boundaries are, and how it connects to the research question - enough that someone unfamiliar with the data could understand what this theme is about",
      "justification": "Why this pattern qualifies as a theme: how it recurs across multiple data items, and what it captures about the ALS community's experience in relation to the research question.",
      "quotes": [
        {
          "text": "An EXACT, verbatim quote copied from a data item (no paraphrasing, no edits, no ellipses-joining of separate spans).",
          "source": "An identifier for the data item the quote came from (e.g. the data item identifier as it appears in the input).",
          "role": "core" or "supporting"
        },
        {
          "text": "Second verbatim quote from a different data item.",
          "source": "data item identifier.",
          "role": "core" or "supporting"
        }
      ]
    }
  ]
}

Field rules:

- "role" is exactly one of "core" or "supporting". Use "core" when the quote directly demonstrates the theme; use "supporting" when it illustrates or reinforces it more adjacently.
- "quotes" must be verbatim - character-for-character copies of text in the data item, so each can be located back in the source. Do not normalize spelling, punctuation, or capitalization. If a point spans two separate places in a data item, list them as two separate quote objects, not one stitched-together string.

Output ONLY the JSON object and its fields - include nothing else. 
</output>


<data>
{data}
</data>

**Rationale for Version 1:**
(Initial version — no prior changes to document)

---

## Loweffort Variant

(To be added)

---

## Nodata Variant

(To be added)
