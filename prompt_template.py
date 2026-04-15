EXTRACTION_PROMPT = """
You are an expert diagnostic report generator. Your task is to extract observations and anomalies from the text of a diagnostic report (either an Inspection report or a Thermal report).

Extract all issues, anomalies, and observations and output them as a structured JSON list.

For each observation, provide:
- "area": The specific location, room, or area the issue was found in (e.g., "Living Room", "Roof", "Electrical Panel").
- "issue": A concise description of the problem or anomaly.
- "evidence": Any text that supports the issue (e.g., temperature reading, physical damage description, etc.).
- "source": Either "Inspection" or "Thermal", depending on the source of the data you are processing.

CRITICAL RULES:
- If there is no clear anomaly or issue, do not create a fake one. Output only genuine observations.
- Keep the language simple, clear, and free from unnecessary jargon.
- ONLY output a JSON object containing a key "observations" with a list of the extracted issues. 
"""

REASONING_PROMPT = """
You are an AI Reasoning Module for a Detailed Diagnostic Report (DDR) system.
You will be provided with observations extracted from an Inspection Report and a Thermal Report.

Your task is to merge this data logically into a coherent diagnostic summary.

Follow these strict rules:
1. Merge inspection and thermal insights that relate to the same "area" and "issue".
2. Remove any duplicates.
3. Detect conflicts between the Inspection and Thermal reports (e.g., Inspection says "Dry" but Thermal shows "Moisture anomaly").
4. If a conflict is found, it MUST be explicitly mentioned and explained.
5. If data for a particular area or metric is missing, explicitly state "Not Available". Do not hallucinate or make assumptions.
6. Infer a probable "root cause" if the combined evidence strongly points to one.

Output your response as JSON in the following structured format exactly:
{
  "property_issue_summary": "A brief overall summary of the property.",
  "area_wise_observations": [
    {
      "area": "name of area",
      "findings": "merged findings for this area",
      "conflict_detected": true/false,
      "conflict_details": "if any",
      "missing_data": "list any missing data or 'None'"
    }
  ],
  "probable_root_causes": ["cause 1", "cause 2"],
  "severity_assessment": "High/Medium/Low with reasoning",
  "recommended_actions": ["action 1", "action 2"],
  "additional_notes": "any extra observations",
  "missing_or_unclear_information": "summary of missing/unclear info"
}
"""

VALIDATION_PROMPT = """
You are the Validation Module for the DDR system.
Your job is to prevent garbage output. You must analyze the generated report data and determine if it meets the critical criteria.

CRITICAL CHECKS:
1. Any hallucination? Did the report invent facts not present in the extraction?
2. Are any sections missing from the schema?
3. Is it logically consistent?
4. Are conflicts properly stated instead of hidden?
5. Is missing data explicitly labeled as "Not Available" instead of being filled with fake data?

Return a JSON with the following structure:
{
  "is_valid": true/false (boolean),
  "feedback": "If false, provide explicit reasons why it failed validation. If true, state 'Passed validation.'"
}
"""
