
"""
app.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Version 5.0
Gradio 5.38.2 Compatible
=========================================
"""

import os
import gradio as gr

from chatbot import BusChatbot
from config import APP_NAME, APP_VERSION, EXAMPLE_QUERIES, STYLE_FILE

bot = BusChatbot()

# -------------------------------------------------
# Load CSS (optional)
# -------------------------------------------------
css = ""
if os.path.exists(STYLE_FILE):
    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        css = f.read()


def chat(message, history):
    """
    Gradio Chatbot(type='messages') callback.
    history is a list of:
    {"role":"user","content":"..."}
    {"role":"assistant","content":"..."}
    """
    history = history or []

    if not message.strip():
        return "", history

    answer = bot.reply(message)

    history.append(
        {
            "role": "user",
            "content": message,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return "", history


with gr.Blocks(
    title=f"{APP_NAME} {APP_VERSION}",
    css=css,
    fill_height=True,
) as demo:

    gr.Markdown(f"""
# 🚌 {APP_NAME}

Search private OmniBus services using natural language.

### Try asking:
- Show buses from Chennai to Madurai
- Cheapest bus under 1000
- Luxury Sleeper with WiFi
- Night Volvo bus
""")

    chatbot = gr.Chatbot(
        type="messages",
        height=560,
        label="AI Bus Assistant",
        bubble_full_width=False,
    )

    with gr.Row():
        textbox = gr.Textbox(
            placeholder="Type your bus query here...",
            lines=1,
            scale=8,
        )

        send = gr.Button(
            "🚀 Send",
            variant="primary",
            scale=1,
        )

    clear = gr.Button("🧹 Clear Chat")

    gr.Examples(
        examples=[[q] for q in EXAMPLE_QUERIES],
        inputs=textbox,
    )

    send.click(
        fn=chat,
        inputs=[textbox, chatbot],
        outputs=[textbox, chatbot],
        show_progress="full",
    )

    textbox.submit(
        fn=chat,
        inputs=[textbox, chatbot],
        outputs=[textbox, chatbot],
        show_progress="full",
    )

    clear.click(
        lambda: ("", []),
        outputs=[textbox, chatbot],
    )

if __name__ == "__main__":
    demo.launch(share=True)
