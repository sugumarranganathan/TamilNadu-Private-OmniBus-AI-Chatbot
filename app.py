"""
app.py
=========================================================
Tamil Nadu Private OmniBus AI Chatbot
Professional Gradio Interface
Version 7.0
Part 1 / 3
=========================================================
"""

import os
import gradio as gr

from chatbot import BusChatbot

from config import (
    APP_NAME,
    APP_VERSION,
    EXAMPLE_QUERIES,
    STYLE_FILE,
)

# =========================================================
# Initialize Chatbot
# =========================================================

bot = BusChatbot()

# =========================================================
# Load Optional CSS
# =========================================================

css = ""

if os.path.exists(STYLE_FILE):
    with open(STYLE_FILE, "r", encoding="utf-8") as f:
        css = f.read()

# =========================================================
# Chat Function
# =========================================================

def chat(message, history):

    history = history or []

    message = (message or "").strip()

    if not message:
        return "", history

    try:

        answer = bot.reply(message)

    except Exception as e:

        answer = (
            "❌ An unexpected error occurred.\n\n"
            f"{str(e)}"
        )

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

# =========================================================
# Quick Search
# =========================================================

def quick_search(query, history):

    return chat(query, history)

# =========================================================
# Analytics Button
# =========================================================

def show_analytics(history):

    history = history or []

    try:

        answer = bot.reply("dataset statistics")

    except Exception as e:

        answer = str(e)

    history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    return history

# =========================================================
# Welcome Message
# =========================================================

def welcome():

    return [
        {
            "role": "assistant",
            "content": bot.greeting(),
        }
    ]

# =========================================================
# Clear Chat
# =========================================================

def clear_chat():

    return "", welcome()

# =========================================================
# About Information
# =========================================================

ABOUT_TEXT = f"""
## ℹ️ About

**{APP_NAME}**

Version: **{APP_VERSION}**

### Features

✅ Semantic Search (FAISS)

✅ Natural Language Queries

✅ Intent Detection

✅ Conversation Memory

✅ Route Search

✅ Fare Filtering

✅ Bus Type Filtering

✅ Amenity Filtering

✅ Time-based Search

✅ Dataset Analytics

### Built With

- Python
- FAISS
- Sentence Transformers
- Gradio
"""

# =========================================================
# Gradio Interface
# =========================================================

with gr.Blocks(
    title=f"{APP_NAME} {APP_VERSION}",
    css=css,
    fill_height=True,
) as demo:

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------

    gr.Markdown(f"""
# 🚌 {APP_NAME}

### AI-Powered Semantic Search for Tamil Nadu Private OmniBus Services

Search buses using natural language.

Examples:

- Chennai to Madurai
- Cheapest bus under ₹1000
- Luxury Sleeper Bus
- Bus with WiFi
- Night Bus
- Best Rated Bus
""")

    # -----------------------------------------------------
    # Main Layout
    # -----------------------------------------------------

    with gr.Row():

        # ==========================================
        # Sidebar
        # ==========================================

        with gr.Column(scale=1, min_width=280):

            gr.Markdown("## 🚀 Quick Actions")

            analytics_btn = gr.Button(
                "📊 Dataset Analytics",
                variant="secondary",
            )

            clear_btn = gr.Button(
                "🧹 Clear Chat",
                variant="stop",
            )

            gr.Markdown("---")

            gr.Markdown("""
### 💡 Popular Searches

Click any button below.
""")

        # ==========================================
        # Chat Area
        # ==========================================

        with gr.Column(scale=4):

            chatbot = gr.Chatbot(
                label="AI Bus Assistant",
                type="messages",
                height=600,
                value=welcome(),
            )

            with gr.Row():

                textbox = gr.Textbox(
                    placeholder="Ask anything about Tamil Nadu buses...",
                    lines=1,
                    scale=8,
                )

                send_btn = gr.Button(
                    "🚀 Send",
                    variant="primary",
                    scale=1,
                )

    # -----------------------------------------------------
    # Quick Search Buttons
    # -----------------------------------------------------

    gr.Markdown("## ⚡ Quick Search")

    with gr.Row():

        btn1 = gr.Button("📍 Chennai → Madurai")
        btn2 = gr.Button("📍 Chennai → Bengaluru")
        btn3 = gr.Button("📍 Coimbatore → Chennai")
        btn4 = gr.Button("📍 Madurai → Trichy")

    with gr.Row():

        btn5 = gr.Button("💰 Cheapest Bus")
        btn6 = gr.Button("🛏 Luxury Sleeper")
        btn7 = gr.Button("⭐ Best Rated")
        btn8 = gr.Button("🚌 Volvo Bus")

    with gr.Row():

        btn9 = gr.Button("🌙 Night Bus")
        btn10 = gr.Button("📶 Bus with WiFi")
        btn11 = gr.Button("❄️ AC Sleeper")
        btn12 = gr.Button("💺 Seats Available")

    # -----------------------------------------------------
    # Examples
    # -----------------------------------------------------

    gr.Markdown("## 📚 Example Queries")

    gr.Examples(
        examples=[[x] for x in EXAMPLE_QUERIES],
        inputs=textbox,
        label="Try these example searches",
    )

    # -----------------------------------------------------
    # About Section
    # -----------------------------------------------------

    gr.Markdown("---")

    with gr.Accordion(
        "ℹ️ About This Project",
        open=False,
    ):

        gr.Markdown(ABOUT_TEXT)

# =========================================================
# Event Handlers
# =========================================================

# -----------------------------
# Send Button
# -----------------------------

send_btn.click(
    fn=chat,
    inputs=[textbox, chatbot],
    outputs=[textbox, chatbot],
    show_progress="full",
)

# -----------------------------
# Press Enter
# -----------------------------

textbox.submit(
    fn=chat,
    inputs=[textbox, chatbot],
    outputs=[textbox, chatbot],
    show_progress="full",
)

# -----------------------------
# Analytics Button
# -----------------------------

analytics_btn.click(
    fn=show_analytics,
    inputs=[chatbot],
    outputs=[chatbot],
)

# -----------------------------
# Clear Chat
# -----------------------------

clear_btn.click(
    fn=clear_chat,
    outputs=[textbox, chatbot],
)

# =========================================================
# Quick Search Buttons
# =========================================================

QUICK_SEARCHES = {
    btn1: "Show buses from Chennai to Madurai",
    btn2: "Show buses from Chennai to Bengaluru",
    btn3: "Show buses from Coimbatore to Chennai",
    btn4: "Show buses from Madurai to Trichy",
    btn5: "Cheapest bus",
    btn6: "Luxury Sleeper bus",
    btn7: "Best rated bus",
    btn8: "Volvo bus",
    btn9: "Night bus",
    btn10: "Bus with WiFi",
    btn11: "AC Sleeper bus",
    btn12: "Seats available",
}

for button, query in QUICK_SEARCHES.items():

    button.click(
        fn=quick_search,
        inputs=[
            gr.State(query),
            chatbot,
        ],
        outputs=[
            textbox,
            chatbot,
        ],
        show_progress="hidden",
    )

# =========================================================
# Footer
# =========================================================

gr.Markdown(
    f"""
---

<center>

### 🚌 {APP_NAME}

**Version:** {APP_VERSION}

Built using:

🐍 Python • 🤖 Sentence Transformers • ⚡ FAISS • 🎨 Gradio

© 2026 Tamil Nadu Private OmniBus AI Chatbot

</center>
"""
)

# =========================================================
# Launch
# =========================================================

if __name__ == "__main__":

    demo.launch(
        share=True,
        show_error=True,
    )



