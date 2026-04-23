from src.graph.graph import build_graph


def print_trace(result: dict) -> None:
    print("\n=== FLOW TRACE ===")

    for i, step in enumerate(result.get("trace", []), start=1):
        print(f"\nStep {i}: {step.get('step', 'unknown')}")

        for key, value in step.items():
            if key == "step":
                continue

            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")

    print("\n=== END TRACE ===\n")


def main() -> None:
    graph = build_graph()

    print("Agentic RAG System")
    print("Type 'exit' to quit.\n")

    history = []

    while True:
        query = input("Enter your question: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        if not query:
            print("Please enter a question.\n")
            continue

        history = history[-10:]

        result = graph.invoke(
            {
                "query": query,
                "history": history,
                "trace": [],
            }
        )

        answer = result.get("final_answer", "No answer produced.")

        print_trace(result)

        print("Answer:")
        print(answer)
        print()

        history.append(f"User: {query}")
        history.append(f"Assistant: {answer}")


if __name__ == "__main__":
    main()