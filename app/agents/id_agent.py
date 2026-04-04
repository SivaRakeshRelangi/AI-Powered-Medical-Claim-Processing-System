from app.services.llm import get_llm
from app.utils.clean_json import clean_json
import json

llm = get_llm()

def id_agent(state):
    pages = state["classified_pages"].get("identity_document", [])
    text = "\n".join([p["text"] for p in pages])

    if not text:
        return {"id_data": {}}

    prompt = f"""
Extract in JSON:
{{
 "name": "",
 "dob": "",
 "id_number": "",
 "policy_number": ""
}}

Return ONLY JSON.

{text}
"""

    # ✅ Use invoke() for ChatGroq
    result = llm.invoke(prompt)

    # The response is usually under result["output_text"]
    # response_text = result.get("output_text", "") if isinstance(result, dict) else str(result)
    response_text = clean_json(result.content)
    print(response_text)
    try:
        return {"id_data": json.loads(response_text)}
    except json.JSONDecodeError:
        # fallback if LLM didn't return valid JSON
        return {"id_data": {"raw": response_text}}