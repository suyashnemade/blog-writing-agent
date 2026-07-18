from blogwriter.tools.search import _tavily_search
from blogwriter.states import State
from blogwriter.schemas import RouterDecision
# from blogwriter.config import llm
from blogwriter.config import  llmresearcher
from langchain_core.messages import SystemMessage, HumanMessage
from typing import List, Dict
from blogwriter.schemas import EvidencePack

RESEARCH_SYSTEM = """You are a research synthesizer for technical writing.

Given raw web search results, produce a deduplicated list of EvidenceItem objects.

Rules:
- Only include items with a non-empty url.
- Prefer relevant + authoritative sources (company blogs, docs, reputable outlets).
- If a published date is explicitly present in the result payload, keep it as YYYY-MM-DD.
  If missing or unclear, set published_at=null. Do NOT guess.
- Keep snippets short.
- Deduplicate by URL.
"""

def research_node(state: State) -> dict:

    # take the first 10 queries from state
    queries = (state.get("queries", []) or [])
    max_results = 5

    raw_results: List[dict] = []

    for q in queries:
        raw_results.extend(_tavily_search(q, max_results=max_results))

    print("Queries:", len(queries))
    print("Results:", len(raw_results))

    if not raw_results:
        return {"evidence": []}

    # extractor = llm.with_structured_output(EvidencePack)
    # pack = extractor.invoke(
    #     [
    #         SystemMessage(content=RESEARCH_SYSTEM),
    #         HumanMessage(content=f"Raw results:\n{raw_results}"),
    #     ]
    # )
    formatted = []

    for result in raw_results:
        formatted.append(
            f"""Title: {result['title']}
            URL: {result['url']}
            Published: {result['published_at']}
            Snippet: {result['snippet']}"""
        )

    prompt = "\n\n".join(formatted)
    print("Prompt chars:", len(prompt))

    extractor = llmresearcher.with_structured_output(EvidencePack)

    pack = extractor.invoke(
        [
            SystemMessage(content=RESEARCH_SYSTEM),
            HumanMessage(content=prompt),
        ]
    )
    

    # Deduplicate by URL
    dedup = {}
    for e in pack.evidence:
        if e.url:
            dedup[e.url] = e

    return {"evidence": list(dedup.values())}
