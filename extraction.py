import json
from openai import OpenAI
from prompt_template import EXTRACTION_PROMPT

class ExtractionModule:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def extract_data(self, ingestion_data: dict) -> list:
        """
        Converts messy text from ingestion into structured extraction data.
        """
        # Combine all text from the PDF into a single string to feed to LLM
        # For very large PDFs, chunking might be needed, but we keep it simple for now as requested
        combined_text = "\n".join([f"Page {t['page']}: {t['text']}" for t in ingestion_data["text"]])
        source = ingestion_data["source"]
        
        if not combined_text.strip():
            print(f"No text found for {source}.")
            return []

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": EXTRACTION_PROMPT},
                    {"role": "user", "content": f"Source Type: {source}\n\nReport Text:\n{combined_text}"}
                ],
                temperature=0.2
            )
            
            result_str = response.choices[0].message.content
            result_json = json.loads(result_str)
            observations = result_json.get("observations", [])
            
            # Ensure the source is tagged properly as per blueprint
            for obs in observations:
                obs["source"] = source
                if "area" not in obs: obs["area"] = "Unknown"
                if "issue" not in obs: obs["issue"] = "Not Available"
                if "evidence" not in obs: obs["evidence"] = "Not Available"
                
            return observations
            
        except Exception as e:
            print(f"Error during extraction for {source}: {e}")
            return []
