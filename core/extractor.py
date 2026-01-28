# core/extractor.py

import json
from typing import List, Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from .rag import retriever, llm


# ------------------ PROMPT ------------------ #

EXTRACT_PROMPT = ChatPromptTemplate.from_template(
    """
You are a Government Compliance Extraction AI **ONLY for construction projects in Mumbai**.

User Project Description:
{description}

Using ONLY the provided PDF context from:
- Mumbai DCPR 2034
- Maharashtra Fire Prevention & Life Safety Act
- NBC 2016 Part 4
- BMC circulars (air pollution, parking, etc.)
- Any other Mumbai-specific rules

extract ALL **mandatory** rules and compliances that the project must follow.

For EACH compliance, output a JSON object with:

- "name": short official name of the compliance
- "description": simple explanation in 2–3 lines (why needed, what it covers)
- "stage": one of:
    - "pre_construction"
    - "during_construction"
    - "post_construction"
- "time_bound": one of:
    - "before_start"
    - "during_construction"
    - "monthly"
    - "before_occupancy"
    - "as_applicable"
- "document_required": short text about the required NOC/document
- "source_hint": which main rule/PDF it came from

Return ONLY a JSON array.

Context from PDFs:
{context}
"""
)

# ------------------ JSON CLEANER ------------------ #

def _clean_json(text: str) -> str:
    """Extract JSON array from messy LLM output."""
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text


# ------------------ MAIN FUNCTION ------------------ #

def extract_compliances(description: str) -> List[Dict[str, Any]]:
    """Extract compliances using RAG + LLM."""

    query = f"Mumbai construction compliances for: {description}"

    # 🚀 Updated for new LangChain retriever API
    docs = retriever.invoke(query)

    # Join PDF chunks into context
    context = "\n\n".join(d.page_content for d in docs)

    # Run LLM
    chain = EXTRACT_PROMPT | llm
    res = chain.invoke({"description": description, "context": context})

    # Extract raw content
    raw_text = res.content if hasattr(res, "content") else str(res)
    json_text = _clean_json(raw_text)

    # Parse JSON output safely
    try:
        data = json.loads(json_text)
        return data if isinstance(data, list) else []
    except Exception:
        return []
