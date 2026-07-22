"""
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
app.py
Version 9.0
Part 1
=========================================================
"""

import os
import gradio as gr

from chatbot import BusChatbot
from config import (
    STYLE_FILE,
    EXAMPLE_QUERIES,
)

# =========================================================
# Initialize Chatbot
# =========================================================

bot = BusChatbot()

# =========================================================
# Load CSS
# =========================================================

css = ""

if os.path.exists(STYLE_FILE):

    try:

        with open(STYLE_FILE, "r", encoding="utf-8") as f:
            css = f.read()

    except Exception:
        css = ""

# =========================================================
# Chat Function
# =========================================================

def chat(message, history):

    if history is None:
        history = []

    message = str(message).strip()

    if message == "":
        return "", history

    try:

        response = bot.chat(message)

    except Exception as e:

        response = f"❌ {e}"

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


# =========================================================
# Clear Chat
# =========================================================

def clear_chat():

    return []


# =========================================================
# Analytics
# =========================================================

def show_analytics():

    try:

        info = bot.engine.dataset_info()

        analytics = bot.engine.analytics()

        return f"""
# Dataset Information

**Embedding Model**
{info["model"]}

**Bus Records**
{info["bus_records"]}

**Semantic Documents**
{info["documents"]}

**FAISS Vectors**
{info["vectors"]}

---

# Analytics

{analytics}
"""

    except Exception as e:

        return f"❌ {e}"

# =========================================================
# User Interface
# =========================================================

with gr.Blocks(

    title="Tamil Nadu Private OmniBus AI Chatbot",

    css=css,

) as demo:

    gr.Markdown(
        """
# 🚌 Tamil Nadu Private OmniBus AI Chatbot

Search Tamil Nadu private buses using natural language.

### Try asking

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

        # ==========================================
        # Left Panel
        # ==========================================

        with gr.Column(scale=4):

            chatbot = gr.Chatbot(

                type="messages",

                label="Conversation",

                height=520,

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

            gr.Examples(

                examples=[[q] for q in EXAMPLE_QUERIES],

                inputs=message,

            )

        # ==========================================
        # Right Panel
        # ==========================================

        with gr.Column(scale=1):

            analytics_btn = gr.Button(

                "📊 Dataset Analytics",

                variant="secondary",

            )

            analytics_output = gr.Markdown()

            gr.Markdown(
                """
### Search Tips

✅ Search by route

✅ Search by operator

✅ Search by bus type

✅ Search by amenities

✅ Search by timing

✅ Search by fare

✅ Search by rating

---

### Example Queries

- Chennai to Salem

- Chennai to Madurai

- AC Sleeper

- Volvo

- Cheapest Bus

- Bus under ₹800

- Bus with WiFi

- Best Rated Bus
"""
            )

    # =========================================================
    # Event Handlers
    # =========================================================

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
        inputs=[],
        outputs=chatbot,
    )

    analytics_btn.click(
        fn=show_analytics,
        inputs=[],
        outputs=analytics_output,
    )

    # =========================================================
    # Footer
    # =========================================================

    gr.Markdown(
        """
---

### 🚀 Tamil Nadu Private OmniBus AI Chatbot

Built with:

- Python
- Gradio
- FAISS
- Sentence Transformers

AI-powered semantic search for Tamil Nadu private bus services.
"""
    )

# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    demo.queue()

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True,
        share=True,
    )
