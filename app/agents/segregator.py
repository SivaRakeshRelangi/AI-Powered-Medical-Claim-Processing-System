from app.services.llm import get_llm

llm = get_llm()

LABELS = [
    "claim_forms",
    "cheque_or_bank_details",
    "identity_document",
    "itemized_bill",
    "discharge_summary",
    "prescription",
    "investigation_report",
    "cash_receipt",
    "other"
]


def normalize_label(raw_label: str) -> str:
    """
    Clean and map LLM output to a valid label.
    """

    if not raw_label:
        return "other"

    raw_label = raw_label.lower().strip()

    # Remove unwanted characters/newlines
    raw_label = raw_label.replace("\n", "").replace("`", "").strip()

    # Try exact match first
    if raw_label in LABELS:
        return raw_label

    # Try fuzzy match (very important)
    for label in LABELS:
        if label in raw_label:
            return label

    return "other"


def segregator_agent(state):
    pages = state["pages"]
    classified = {}

    for page in pages:
        prompt = f"""
You are a strict document classifier.

Classify the document into EXACTLY one label from this list:
{LABELS}

Rules:
- Return ONLY the label
- No explanation
- No extra words
- No punctuation
- Output must exactly match one label

Page:
{page['text']}
"""

        result = llm.invoke(prompt)

        # ✅ Always extract content properly
        raw_label = result.content if hasattr(result, "content") else str(result)

        # ✅ Normalize label (CRITICAL FIX)
        label = normalize_label(raw_label)

        # ✅ Debug (very important for you now)
        print(f"\n--- PAGE {page['page_num']} ---")
        print("RAW LABEL:", raw_label)
        print("FINAL LABEL:", label)

        classified.setdefault(label, []).append(page)

    # ✅ Final debug
    print("\n✅ CLASSIFIED KEYS:", classified.keys())

    return {"classified_pages": classified}