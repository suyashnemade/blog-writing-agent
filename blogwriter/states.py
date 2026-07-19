from __future__ import annotations

import operator
from typing import TypedDict, List, Annotated, Literal, Optional

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


from blogwriter.schemas import Task, Plan, EvidenceItem, RouterDecision, EvidencePack


class State(TypedDict):
    topic: str

    # routing / research
    mode: str
    needs_research: bool
    queries: List[str]
    evidence: List[EvidenceItem]
    plan: Optional[Plan]

    # NEW: recency control
    as_of: str         
    recency_days: int    

    # workers
    sections: Annotated[List[tuple[int, str]], operator.add]  # (task_id, section_md)
    final: str

    #image
    merged_md: str
    md_with_placeholders: str
    image_specs: List[dict]

    final: str