import gradio as gr

from src.graph.graph import build_graph


graph = build_graph()


def format_trace(trace):
    lines = []

    for i, step in enumerate(trace or [], start=1):
        lines.append(f"Step {i}: {step.get('step', 'unknown')}")
        for key, value in step.items():
            if key == "step":
                continue
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: {value}")
        lines.append("")

    return "\n".join(lines).strip()


def chat_fn(message, history):
    if not message.strip():
        return history, "", "", ""

    # Convert chat history into your graph history format
    graph_history = []
    for msg in history:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            graph_history.append(f"User: {content}")
        elif role == "assistant":
            graph_history.append(f"Assistant: {content}")

    result = graph.invoke(
        {
            "query": message,
            "history": graph_history[-10:],
            "trace": [],
        }
    )

    answer = result.get("final_answer", "No answer produced.")
    sources = result.get("retrieved_sources", [])
    trace = result.get("trace", [])

    unique_sources = []
    seen = set()
    for src in sources:
        if src not in seen:
            unique_sources.append(src)
            seen.add(src)

    source_text = "\n".join(f"- {s}" for s in unique_sources) if unique_sources else "No sources."
    trace_text = format_trace(trace)

    # Append messages in Gradio's expected format
    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer},
    ]

    return history, "", source_text, trace_text


with gr.Blocks(title="LangGraph RAG Chat") as demo:
    gr.Markdown("# LangGraph RAG Chat")
    gr.Markdown("Ask questions about your knowledge base.")

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="Chat", height=500)
            msg = gr.Textbox(
                label="Your question",
                placeholder="Ask something...",
            )

            with gr.Row():
                send = gr.Button("Send")
                clear = gr.Button("Clear")

        with gr.Column(scale=1):
            sources_box = gr.Textbox(label="Retrieved Sources", lines=12)
            trace_box = gr.Textbox(label="Flow Trace", lines=18)

    send.click(
        chat_fn,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, sources_box, trace_box],
    )

    msg.submit(
        chat_fn,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, sources_box, trace_box],
    )

    clear.click(
        lambda: ([], "", "", ""),
        outputs=[chatbot, msg, sources_box, trace_box],
    )

if __name__ == "__main__":
    demo.launch()