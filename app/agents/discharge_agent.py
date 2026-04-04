from app.services.llm import get_llm
from app.utils.clean_json import clean_json
import json

llm = get_llm()


def discharge_agent(state):
    pages = state["classified_pages"].get("discharge_summary", [])
    text = "\n".join([p["text"] for p in pages])

    if not text:
        return {"discharge_data": {}}

    prompt = f"""
Extract in JSON:
{{
 "diagnosis": "",
 "admission_date": "",
 "discharge_date": "",
 "doctor": ""
}}

Return ONLY JSON.

{text}
"""

    # Use invoke() for ChatGroq
    result = llm.invoke(prompt)

    # Extract text safely
    #response_text = result.get("output_text", "") if isinstance(result, dict) else str(result)
    response_text = clean_json(result.content)
    print(response_text)
    try:
        return {"discharge_data": json.loads(response_text)}
    except json.JSONDecodeError:
        return {"discharge_data": {"raw": response_text}}
