You are converting a thematic analysis output from prose format into a JSON schema. Do NOT change, edit, rephrase, or improve any of the text except for the additional_text field. Your only job is to restructure existing text into the JSON format below.

Rules:
- Preserve all text exactly as written. Do not rephrase theme names, descriptions, or quotes.
- Map the original theme title/heading → "name"
- Map the original theme description/explanation → "definition" (combine the descriptive paragraphs and text if needed, but do not rewrite them)
- If there is reasoning provided past the definition, set the "reasoning" field to the exact text provided. If there is not, set it to "N/A - low-effort condition",
- Map any quoted or paraphrased text → "quotes" array entries. Copy quotes/paraphrases character-for-character. Set the "source" field to the identifier if given for a quote (e.g. "D1", "D3"), but if no identifier for that specific quote put "source" as "N/A - low-effort condition". Set "role" to "N/A - low-effort condition" for all quotes
- Make sure to include ALL of the themes and relevant text
- If the original output contains text that does not belong to any specific theme (introductory paragraphs, meta-themes, summary sections, frequency tables, concluding statements, etc.), summarize it concisely in the top-level "additional_text" field. This will be done only once. Capture the key points but do not reproduce the full text. This is only time you will deviate from copying text over verbatim into fields.

Output schema:

{
  "themes": [
    {
      "reasoning": "exact reasoning text", or "N/A - low-effort condition",
      "name": "the theme title",
      "definition": "the descriptive text, preserved as-is",
      "quotes": [
        {
          "text": "exact quote/paraphrase",
          "source": "identifier",
          "role": "N/A - low-effort condition"
        }
      ]
    }
  ],
  "additional_text": "A summary of any text from the original output that does not fit into any of the other fields"
}

Here is the prose output to convert:

[PASTE OUTPUT HERE]