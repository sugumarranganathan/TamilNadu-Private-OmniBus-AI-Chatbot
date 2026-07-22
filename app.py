
"""
app.py
Version 3.0
Gradio 6.x compatible UI
"""

from pathlib import Path
import gradio as gr

from chatbot import chatbot_response, WELCOME_MESSAGE

TITLE = "🚌 Tamil Nadu Private OmniBus AI Chatbot"

EXAMPLES = [
    "Show buses from Chennai to Madurai",
    "Luxury Sleeper bus from Bengaluru to Chennai",
    "Bus under 1000",
    "Bus with WiFi",
    "Night bus to Salem",
    "Best rated bus",
]

CSS = ""
css_file = Path("style.css")
if css_file.exists():
    CSS = css_file.read_text(encoding="utf-8")


def chat(message, history):
    history = history or []
    if not message.strip():
        return "", history

    try:
        reply = chatbot_response(message)
    except Exception as e:
        reply = f"❌ Error\n\n{e}"

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})

    return "", history


with gr.Blocks(
    title=TITLE,
    css=CSS,
    fill_height=True,
) as demo:

    gr.Markdown(f"# {TITLE}")
    gr.Markdown(WELCOME_MESSAGE)

    chatbot = gr.Chatbot(
        label="Bus Assistant",
        height=520,
        show_copy_button=True,
    )

    with gr.Row():
        textbox = gr.Textbox(
            placeholder="Ask about buses...",
            lines=1,
            scale=8,
        )
        send = gr.Button("Send", variant="primary", scale=1)

    clear = gr.Button("🧹 Clear Chat")

    gr.Examples(
        examples=[[q] for q in EXAMPLES],
        inputs=textbox,
    )

    send.click(
        chat,
        inputs=[textbox, chatbot],
        outputs=[textbox, chatbot],
    )

    textbox.submit(
        chat,
        inputs=[textbox, chatbot],
        outputs=[textbox, chatbot],
    )

    clear.click(
        lambda: ("", []),
        outputs=[textbox, chatbot],
    )

if __name__ == "__main__":
    demo.launch(
        share=True,
        debug=True,
    )
