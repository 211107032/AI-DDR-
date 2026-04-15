import json
from openai import OpenAI
from prompt_template import REASONING_PROMPT

class ReasoningModule:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def process(self, inspection_data: list, thermal_data: list) -> dict:
        """
        Merges inspection and thermal data, handles conflicts, and structures the final output.
        """
        combined_data = {
            "inspection_observations": inspection_data,
            "thermal_observations": thermal_data
        }
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": REASONING_PROMPT},
                    {"role": "user", "content": f"Combine and analyze the following extracted data:\n{json.dumps(combined_data, indent=2)}"}
                ],
                temperature=0.2
            )
            
            result_str = response.choices[0].message.content
            return json.loads(result_str)
            
        except Exception as e:
            print(f"Error during reasoning: {e}")
            return {}
