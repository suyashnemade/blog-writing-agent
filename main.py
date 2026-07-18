from blogwriter.workflow import app


def main():
    topic = "Write a blog on Self Attention"
    result = app.invoke(
        {
            "topic": topic,
            "sections": [],
        }
    )

    print(result)


if __name__ == "__main__":
    main()