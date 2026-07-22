import gradio as gr

# ==========================================
# Theme Colors
# ==========================================

PRIMARY = "#2563EB"
BACKGROUND = "#0F172A"
CARD = "#1E293B"

# ==========================================
# Dummy Chat Function
# (We'll replace this later)
# ==========================================

def chatbot(message, history):
    reply = f"""### 🤖 Tamil Nadu Private Omni Bus AI

You asked:

**{message}**

✅ Search engine is loading...

In the next step this will search your:

- bus_services.csv
- documents.pkl
- bus_index.faiss
"""

    history.append(
        {"role": "user", "content": message}
    )

    history.append(
        {"role": "assistant", "content": reply}
    )

    return history, ""

# ==========================================
# Custom CSS
# ==========================================

css = """

.gradio-container{
    max-width:1500px !important;
    margin:auto;
}

#header{
    text-align:center;
    padding:20px;
}

#title{
    font-size:36px;
    font-weight:bold;
}

#subtitle{
    color:gray;
    font-size:18px;
}

footer{
    display:none;
}

"""

# ==========================================
# UI
# ==========================================

with gr.Blocks(
    title="Tamil Nadu Private Omni Bus AI Chatbot",
    css=css,
    theme=gr.themes.Soft()
) as demo:

    gr.HTML("""

    <div id="header">

    <div id="title">

    🚌 Tamil Nadu Private Omni Bus AI Chatbot

    </div>

    <div id="subtitle">

    Find the Best Private Omni Buses Using AI

    </div>

    </div>

    """)

    with gr.Row():

        # ===========================
        # Sidebar
        # ===========================

        with gr.Column(scale=1):

            gr.Markdown("## 🚍 Quick Questions")

            examples = [

                "Show buses from Chennai to Madurai",

                "Cheapest bus",

                "Luxury Sleeper bus",

                "Night bus",

                "Bus with WiFi",

                "Bus with Charging",

                "Bus under ₹1000",

                "Best rated bus",

                "AC Sleeper",

                "Volvo bus"

            ]

            for ex in examples:
                gr.Button(ex, size="sm")

        # ===========================
        # Chat Area
        # ===========================

        with gr.Column(scale=4):

            chatbot_ui = gr.Chatbot(
                type="messages",
                height=600,
                show_copy_button=True,
                avatar_images=(None, None)
            )

            with gr.Row():

                textbox = gr.Textbox(
                    placeholder="Ask anything about buses...",
                    show_label=False,
                    scale=8
                )

                send = gr.Button(
                    "➤",
                    variant="primary",
                    scale=1
                )

    # ===========================
    # Events
    # ===========================

    send.click(
        chatbot,
        inputs=[textbox, chatbot_ui],
        outputs=[chatbot_ui, textbox]
    )

    textbox.submit(
        chatbot,
        inputs=[textbox, chatbot_ui],
        outputs=[chatbot_ui, textbox]
    )

demo.launch()
