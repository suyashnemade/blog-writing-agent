from blogwriter.workflow import app



def main(topic: str):
    out = app.invoke(
        {
            "topic": topic,
            "mode": "",
            "needs_research": False,
            "queries": [],
            "evidence": [],
            "plan": None,
            "sections": [],
            "final": "",
        }
    )

    return out


if __name__ == "__main__":
    result = main("State of Multimodal LLMs in 2026")
    print(result)
