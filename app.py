"""
app.py
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
Gemini + FAISS + Gradio
Version 10.0
=========================================================
"""

import os
import spaces
import gradio as gr

from chatbot import BusChatbot
from config import STYLE_FILE, EXAMPLE_QUERIES

# ==========================================================
# Initialize Chatbot
# ==========================================================

bot = BusChatbot()

# ==========================================================
# Load CSS
# ==========================================================

css = ""

if os.path.exists(STYLE_FILE):
    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        css = f.read()

# ==========================================================
# Chat Function
# ==========================================================

@spaces.GPU
def respond(message, history):

    history = history or []

    if not message.strip():
        return "", history

    try:
        answer = bot.reply(message)
    except Exception as e:
        answer = f"❌ {e}"

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


# ==========================================================
# Clear Chat
# ==========================================================

def clear_chat():
    return []


# ==========================================================
# Analytics
# ==========================================================

def show_analytics():

    try:

        info = bot.engine.dataset_info()
        stats = bot.engine.analytics()

        return f"""
# 📊 Dataset Analytics

### Embedding Model
{info["model"]}

### Bus Records
{info["bus_records"]}

### Semantic Documents
{info["documents"]}

### FAISS Vectors
{info["vectors"]}

---

{stats}
"""

    except Exception as e:

        return f"❌ {e}"


# ==========================================================
# Gradio UI
# ==========================================================

with gr.Blocks(
    title="Tamil Nadu Private OmniBus AI",
    css=css,
    theme=gr.themes.Soft(),
) as demo:

    gr.Markdown(
        """
# 🚌 Tamil Nadu Private OmniBus AI Assistant

Search buses intelligently using AI.
"""
    )

    with gr.Row():

        with gr.Column(scale=4):

            chatbot = gr.Chatbot(
                type="messages",
                label="AI Bus Assistant",
                height=600,
            )

            msg = gr.Textbox(
                placeholder="Example: Cheapest AC Sleeper bus from Chennai to Madurai",
                lines=2,
            )

            with gr.Row():

                send = gr.Button(
                    "🔍 Search",
                    variant="primary",
                )

                clear = gr.Button("🧹 Clear")

            gr.Examples(
                examples=[[x] for x in EXAMPLE_QUERIES],
                inputs=msg,
            )

        with gr.Column(scale=1):

            analytics_btn = gr.Button("📊 Analytics")

            analytics_md = gr.Markdown()

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

    clear.click(
        clear_chat,
        outputs=chatbot,
    )

    analytics_btn.click(
        show_analytics,
        outputs=analytics_md,
    )

# ==========================================================
# Launch
# ==========================================================

if __name__ == "__main__":

    demo.queue()

    demo.launch()
