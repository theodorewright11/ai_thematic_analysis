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

### Version 2

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
Follow these guidelines when **completing your task**:
- Think carefully about each pattern before committing to it as a theme. Not every observable pattern is a theme - it must capture something meaningful in relation to the research question.
- Support each theme with multiple verbatim quotes from different data items where possible to ensure the theme is adequately justified.
- Themes can range from surface-level patterns in what the data explicitly state to deeper more interpretive patterns that require drawing on broader knowledge to identify. Both levels are valid. What matters is that themes are meaningful to the research question.
- Identify as many themes as the data supports. Do not force themes where the pattern is weak, and do not combine distinct patterns into a single theme. **When in doubt, it is better to identify a theme you are less certain about than to omit a pattern that may be meaningful.**
- **Theme names and definitions should be plain and descriptive rather than polished or metaphorical. Definitions specifically should be information-dense - explain what the theme captures concretely rather than abstractly.**
- **Each theme should capture a distinct pattern. If two potential themes substantially overlap, either combine them or sharpen their boundaries until each captures something the other does not.**
- Some data items may support multiple themes.
- Remember that if data items express conflicting perspectives, that itself may be part of a theme. 
- Give equal attention to all data. Do not let more vivid or lengthy data items dominate the analysis.
- A theme's importance is not determined by how many data items mention it. A pattern appearing in a few data items can be a meaningful theme if it captures something meaningful for the research question.
- The research question guides what to look for - the themes should be specific patterns you find in the data, not categories of what the research question asks about.
- **When selecting supporting quotes, both short and long passages are acceptable to show as support. Be sure each quote segment contains sufficient surrounding context to fully demonstrate its support of the theme.**
</guidelines>


<output>
Report your full analysis as a SINGLE JSON object - and nothing else outside it - matching the schema below.

For each theme, use the reasoning field to think through what you observe. It is your space to show and work through what you noticed and why it matters before committing to a theme name and definition. **It also serves as your justification for why the theme you present is acceptable.**


Schema:

{
  "themes": [
    {
      "reasoning": "The pattern you observed across the data that led to this theme: what you noticed, which data items exemplify it, and why it constitutes a meaningful pattern.",
      "name": "**Plain, concrete, descriptive theme name that captures what the theme is about.**",
      "definition": "**Plain, concrete, information dense definition that explains what the theme captures, where its boundaries are, and how it connects to the research question - enough that someone unfamiliar with the data could understand what this theme is about.**",
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

> **Schema change:** Version 1's `"justification"` field has been **removed** from each theme object.

Field rules:

- "role" is exactly one of "core" or "supporting". Use "core" when the quote directly demonstrates the theme; use "supporting" when it illustrates or reinforces it more adjacently.
- "quotes" must be verbatim - character-for-character copies of text in the data item, so each can be located back in the source. Do not normalize spelling, punctuation, or capitalization. If a point spans two separate places in a data item, list them as two separate quote objects, not one stitched-together string.

Output ONLY the JSON object and its fields - include nothing else. 
</output>


<data>
{data}
</data>

**Rationale for Version 2:**
_From v1 · 2026-06-12_

1. Conducting your analysis changed to **completing your task.** Made the prompt agnostic to be used more generally.
2. **"When in doubt, include rather than omit" appended to the themes line.** Single-pass design means the model has one chance to identify all themes. Bias toward inclusion — weak themes can be discarded during evaluation, but themes that are never generated can't be recovered.
3. **Plain-names / dense-definitions guideline added.** v1 output produced polished, metaphorical names (e.g. "Time Is the Scarce Resource," "Hope Amid Uncertainty") that prioritized catchiness over information content; we want names that convey the theme's core claim directly, even if longer. v1 definitions also lacked some informational substance that would have been useful. Also motivated by downstream embedding comparison — plain descriptive text embeds more predictably than metaphorical language. Informed by comparison to human-generated theme names, which are fuller descriptive statements.
4. **Independence guideline added ("if two themes overlap, combine or sharpen").** We originally wanted to see whether the independence criterion needed to be specified explicitly; v1 output showed overlap between themes (e.g. urgency vs. frustration with pace covered similar ground), so we include it going forward.
5. **Quote-context guideline added (permit longer passages, ensure surrounding context).** v1 output quotes were often short fragments that lost the context needed to evaluate whether the quote actually supports the claimed theme. Longer excerpts let evaluators assess the theme–data link without returning to the original comments.
6. **`reasoning` description noted to also serve as justification.** Part of merging the justification field — same rationale as change 8.
7. **`name` schema description rewritten (→ plain, concrete, descriptive).** Same rationale as change 2, applied to the schema field.
8. **`definition` schema description rewritten (→ plain, concrete, information-dense).** Same rationale as change 2.
9. **`justification` field removed from each theme object.** In v1 output, `reasoning` and `justification` contained largely redundant content. Merging reduces output bloat and simplifies the schema to four fields per theme (`reasoning`, `name`, `definition`, `quotes`) without losing function.

---

## Loweffort Variant

(To be added)

---

## Nodata Variant

(To be added)

---

## Template for New Version

Copy this template when adding a new version to PROMPTS_LOG.md:

```markdown
### Version X

[Full prompt text here with **changed sections bolded**]

**Rationale for Version X:**
- [Reason 1]
- [Reason 2]
- [Reason 3]
```
