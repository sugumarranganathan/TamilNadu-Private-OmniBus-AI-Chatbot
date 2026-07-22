
"""
app_v6.py
=================================================
Tamil Nadu Private OmniBus AI Chatbot
Professional UI (Version 6.0)
Compatible with Gradio 5.38.2
=================================================
"""

import os
import gradio as gr

from chatbot.py import BusChatbot
from config import (
    APP_NAME,
    APP_VERSION,
    EXAMPLE_QUERIES,
    STYLE_FILE,
)

bot = BusChatbot()

# ---------------------------------------------------
# Load CSS (optional)
# ---------------------------------------------------
css = ""
if os.path.exists(STYLE_FILE):
    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        css = f.read()


def chat(message, history):
    history = history or []

    if not message.strip():
        return "", history

    answer = bot.reply(message)

    history.append(
        {"role": "user", "content": message}
    )

    history.append(
        {"role": "assistant", "content": answer}
    )

    return "", history


def quick_query(query, history):
    return chat(query, history)


with gr.Blocks(
    title=f"{APP_NAME} {APP_VERSION}",
    css=css,
    fill_height=True,
) as demo:

    gr.Markdown(f"""
# 🚌 {APP_NAME}

### AI-powered semantic search for Tamil Nadu Private OmniBus services

Search using natural language.

Examples:

- Chennai to Madurai
- Cheapest bus under 1000
- Luxury Sleeper to Bangalore
- Night bus with WiFi
- Best rated Volvo bus
""")

    chatbot = gr.Chatbot(
        type="messages",
        height=560,
        label="AI Bus Assistant",
    )

    with gr.Row():
        textbox = gr.Textbox(
            placeholder="Ask about buses...",
            scale=8,
            lines=1,
        )

        send = gr.Button(
            "🚀 Send",
            variant="primary",
            scale=1,
        )

    gr.Markdown("## 🚀 Quick Search")

    with gr.Row():
        cheapest = gr.Button("💰 Cheapest")
        luxury = gr.Button("🛏 Luxury Sleeper")
        wifi = gr.Button("📶 WiFi")
        night = gr.Button("🌙 Night Bus")

    with gr.Row():
        volvo = gr.Button("🚌 Volvo")
        best = gr.Button("⭐ Best Rated")
        chennai = gr.Button("📍 Chennai → Madurai")
        bangalore = gr.Button("🏙 Chennai → Bengaluru")

    clear = gr.Button("🧹 Clear Chat")

    gr.Examples(
        examples=[[x] for x in EXAMPLE_QUERIES],
        inputs=textbox,
    )

    send.click(
        chat,
        [textbox, chatbot],
        [textbox, chatbot],
        show_progress="full",
    )

    textbox.submit(
        chat,
        [textbox, chatbot],
        [textbox, chatbot],
        show_progress="full",
    )

    cheapest.click(
        quick_query,
        inputs=[
            gr.State("Cheapest bus"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    luxury.click(
        quick_query,
        inputs=[
            gr.State("Luxury Sleeper bus"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    wifi.click(
        quick_query,
        inputs=[
            gr.State("Bus with WiFi"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    night.click(
        quick_query,
        inputs=[
            gr.State("Night bus"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    volvo.click(
        quick_query,
        inputs=[
            gr.State("Volvo bus"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    best.click(
        quick_query,
        inputs=[
            gr.State("Best rated bus"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    chennai.click(
        quick_query,
        inputs=[
            gr.State("Show buses from Chennai to Madurai"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    bangalore.click(
        quick_query,
        inputs=[
            gr.State("Luxury Sleeper bus to Bangalore"),
            chatbot,
        ],
        outputs=[textbox, chatbot],
    )

    clear.click(
        lambda: ("", []),
        outputs=[textbox, chatbot],
    )

    gr.Markdown(
        """
---
### ℹ️ About

**Version:** 6.0

**Backend**
- FAISS Semantic Search
- Sentence Transformers
- Intent Detection
- Natural Language Search

Built using **Python**, **FAISS**, **Sentence Transformers**, and **Gradio**.
"""
    )

if __name__ == "__main__":
    demo.launch(share=True)
