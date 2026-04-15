import json
from openai import OpenAI
from prompt_template import VALIDATION_PROMPT

class ValidationModule:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def validate(self, reasoned_data: dict, max_retries=1) -> tuple[bool, str]:
        """
        Validates the reasoned output to check for hallucinations, missing sections, and logic.
        Returns a tuple of (is_valid, feedback_message).
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": VALIDATION_PROMPT},
                    {"role": "user", "content": f"Please validate the following generated DDR data against the strict rules:\n{json.dumps(reasoned_data, indent=2)}"}
                ],
                temperature=0.0
            )
            
            result_str = response.choices[0].message.content
            result = json.loads(result_str)
            
            is_valid = result.get("is_valid", False)
            feedback = result.get("feedback", "No feedback provided.")
            return is_valid, feedback
            
        except Exception as e:
            print(f"Error during validation: {e}")
            return False, f"Validation failed due to error: {str(e)}"
