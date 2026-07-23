"""
Tamil Nadu Private OmniBus AI Chatbot
Improved app.py (Gradio 5.x)
"""

import os
import gradio as gr

from chatbot import BusChatbot
from config import STYLE_FILE, EXAMPLE_QUERIES

bot = BusChatbot()

css = ""
if os.path.exists(STYLE_FILE):
    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        css = f.read()


def chat(message, history):
    """Gradio 5.x tuple-compatible callback."""
    history = history or []

    if not str(message).strip():
        return "", history

    try:
        response = bot.reply(message)   # <-- use reply(), not chat()
    except Exception as e:
        response = f"❌ {e}"

    # Tuple format expected by Chatbot(type="tuples")
    history.append((message, response))
    return "", history


def clear_chat():
    return []


def show_analytics():
    try:
        info = bot.engine.dataset_info()
        analytics = bot.engine.analytics()

        return f"""
# Dataset Information

**Embedding Model:** {info["model"]}

**Bus Records:** {info["bus_records"]}

**Semantic Documents:** {info["documents"]}

**FAISS Vectors:** {info["vectors"]}

---

# Analytics

{analytics}
"""
    except Exception as e:
        return f"❌ {e}"


with gr.Blocks(
    title="Tamil Nadu Private OmniBus AI Chatbot",
    css=css,
) as demo:

    gr.Markdown("# 🚌 Tamil Nadu Private OmniBus AI Chatbot")

    with gr.Row():

        with gr.Column(scale=4):

            chatbot = gr.Chatbot(
                type="tuples",
                label="Bus Assistant",
                height=520,
                
            )

            message = gr.Textbox(
                placeholder="Example: Chennai to Madurai AC Sleeper under ₹1000",
                lines=2,
            )

            with gr.Row():
                send_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("🧹 Clear Chat")

            gr.Examples(
                examples=[[q] for q in EXAMPLE_QUERIES],
                inputs=message,
            )

        with gr.Column(scale=1):
            analytics_btn = gr.Button("📊 Dataset Analytics")
            analytics_output = gr.Markdown()

    send_btn.click(
        fn=chat,
        inputs=[message, chatbot],
        outputs=[message, chatbot],
    )

    message.submit(
        fn=chat,
        inputs=[message, chatbot],
        outputs=[message, chatbot],
    )

    clear_btn.click(
        fn=clear_chat,
        outputs=chatbot,
    )

    analytics_btn.click(
        fn=show_analytics,
        outputs=analytics_output,
    )

if __name__ == "__main__":

    demo.queue()

    
