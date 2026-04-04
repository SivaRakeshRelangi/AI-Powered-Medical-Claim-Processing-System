from app.services.llm import get_llm
from app.utils.clean_json import clean_json
import json

llm = get_llm()

def bill_agent(state):
    pages = state["classified_pages"].get("itemized_bill", [])
    text = "\n".join([p["text"] for p in pages])

    if not text:
        return {"billing_data": {}}

    prompt = f"""
Extract in JSON:
{{
 "items": [],
 "total_amount": ""
}}

Return ONLY JSON.

{text}
"""

    # ✅ Use invoke() for ChatGroq
    result = llm.invoke(prompt)

    # Extract response text safely
    # response_text = result.get("output_text", "") if isinstance(result, dict) else str(result)
    response_text = clean_json(result.content)
    print(response_text)
    try:
        return {"billing_data": json.loads(response_text)}
    except json.JSONDecodeError:
        # fallback if JSON parsing fails
        return {"billing_data": {"raw": response_text}}