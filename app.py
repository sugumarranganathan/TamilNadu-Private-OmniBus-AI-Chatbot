"""
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
app.py
Version 8.0
Part 1 / 4
=========================================================
"""

import gradio as gr

from chatbot import BusChatbot
from config import (
    EXAMPLE_QUERIES,
    STYLE_FILE,
)

# -------------------------------------------------------
# Load Chatbot
# -------------------------------------------------------

bot = BusChatbot()

# -------------------------------------------------------
# Load Custom CSS
# -------------------------------------------------------

css = ""

try:
    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        css = f.read()
except:
    css = ""

# -------------------------------------------------------
# Callback Functions
# -------------------------------------------------------

def chat(message, history):

    if history is None:
        history = []

    message = (message or "").strip()

    if not message:
        return "", history

    try:

        response = bot.chat(message)

    except Exception as e:

        response = f"❌ Error\n\n{str(e)}"

def chat(message, history):

    if history is None:
        history = []

    message = (message or "").strip()

    if not message:
        return "", history

    try:
        response = bot.chat(message)

    except Exception as e:
        response = f"❌ Error\n\n{e}"

    history.append(
        {
            "role": "user",
            "content": message,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    return "", history

    message = (message or "").strip()

    if not message:
        return "", history

    try:
        response = bot.chat(message)
    except Exception as e:
        response = f"❌ Error\n\n{e}"

    history.append(
        {
            "role": "user",
            "content": message,
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    return "", history


def clear_chat():

    return []


def show_analytics():

    try:

        info = bot.engine.dataset_info()

        analytics = bot.engine.analytics()

        text = f"""
# Dataset Information

**Embedding Model**
{info['model']}

**Bus Records**
{info['bus_records']}

**Semantic Documents**
{info['documents']}

**FAISS Vectors**
{info['vectors']}

---

# Analytics

{analytics}
"""

    except Exception as e:

        text = f"Unable to load analytics.\n\n{e}"

    return text

# -------------------------------------------------------
# UI
# -------------------------------------------------------

with gr.Blocks(

    title="Tamil Nadu Private OmniBus AI Chatbot",

    css=css,

) as demo:

    gr.Markdown(
        """
# 🚌 Tamil Nadu Private OmniBus AI Chatbot

Search buses using natural language.

### Examples

- Chennai to Madurai
- Cheapest bus
- Luxury Sleeper
- Volvo AC
- Bus with WiFi
- Night Bus
- Bus under ₹1000
"""
    )

    with gr.Row():

        with gr.Column(scale=4):

        chatbot = gr.Chatbot(
            type="messages",
            height=520,
            label="Conversation",
            show_copy_button=True,
    )
            message = gr.Textbox(

                label="Ask about buses",

                placeholder="Example: Chennai to Madurai AC Sleeper under ₹1000",

                lines=2,

            )

            with gr.Row():

                send_btn = gr.Button(

                    "Send",

                    variant="primary",

                )

                clear_btn = gr.Button(

                    "Clear Chat"

                )

        with gr.Column(scale=1):

            analytics_btn = gr.Button(

                "Dataset Analytics"

            )

            analytics_output = gr.Markdown()

            gr.Markdown(
                """
### Quick Tips

✔ Search by city

✔ Search by operator

✔ Search by fare

✔ Search by amenities

✔ Search by timing

✔ Search by rating
"""
            )

    gr.Examples(

        examples=[[q] for q in EXAMPLE_QUERIES],

        inputs=message,

    )

    # -------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------

    send_btn.click(
        fn=chat,
        inputs=[
            message,
            chatbot,
        ],
        outputs=[
            message,
            chatbot,
        ],
    )

    message.submit(
        fn=chat,
        inputs=[
            message,
            chatbot,
        ],
        outputs=[
            message,
            chatbot,
        ],
    )

    clear_btn.click(
        fn=clear_chat,
        outputs=chatbot,
    )

    analytics_btn.click(
        fn=show_analytics,
        outputs=analytics_output,
    )

    # -------------------------------------------------------
    # Quick Examples
    # -------------------------------------------------------

    for query in EXAMPLE_QUERIES:

        gr.Button(
            query,
            size="sm",
        ).click(
            fn=lambda q=query: q,
            outputs=message,
        )


    # -------------------------------------------------------
    # Footer
    # -------------------------------------------------------

    gr.Markdown(
        """
---

### 🚀 Tamil Nadu Private OmniBus AI Chatbot

Built with

- Python
- Gradio
- FAISS
- Sentence Transformers
- Hugging Face Spaces

Natural Language Bus Search using Semantic Search.
"""
    )

# =========================================================
# Launch Application
# =========================================================

if __name__ == "__main__":

    demo.queue()

    demo.launch(
        share=False,
        debug=True,
    )

