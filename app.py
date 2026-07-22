
"""
app.py
=========================================
Tamil Nadu Private OmniBus AI Chatbot
Gradio Application (Version 4.0)
Compatible with Gradio 5.38.2
=========================================
"""

import gradio as gr

from chatbot import BusChatbot
from config import (
    APP_NAME,
    APP_VERSION,
    CHAT_HEIGHT,
    EXAMPLE_QUERIES,
    STYLE_FILE,
)

bot = BusChatbot()


def respond(message, history):
    reply = bot.reply(message)
    history = history or []
    history.append((message, reply))
    return "", history


css = ""
try:
    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        css = f.read()
except FileNotFoundError:
    css = ""


with gr.Blocks(
    title=f"{APP_NAME} v{APP_VERSION}",
    css=css,
) as demo:

    gr.Markdown(
        f"""
# 🚌 {APP_NAME}

Search Tamil Nadu private OmniBus services using natural language.

### Example:
- Show buses from Chennai to Madurai
- Cheapest bus under 1000
- Luxury Sleeper with WiFi
- Night Volvo bus
"""
    )

    chatbot = gr.Chatbot(
        height=CHAT_HEIGHT,
        type="tuples",
        label="Bus Assistant",
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask about buses...",
            scale=8,
            lines=1,
        )

        send = gr.Button("Send", scale=1)

    clear = gr.ClearButton([msg, chatbot])

    gr.Examples(
        examples=[[q] for q in EXAMPLE_QUERIES],
        inputs=msg,
    )

    send.click(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
    )

    msg.submit(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
    )


if __name__ == "__main__":
    demo.launch()
