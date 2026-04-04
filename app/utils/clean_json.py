import re

def clean_json(text: str) -> str:
    # Remove markdown ```json ``` wrappers
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # Remove leading/trailing whitespace
    return text.strip()