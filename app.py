"""
==============================================================
Tamil Nadu Private Omni Bus AI Chatbot

Professional Gradio Application

Version : 2.0
Part : 1 / 3

Author : Sugumar R

==============================================================
"""

import gradio as gr

from chatbot import chatbot_response

from config import (
    APP_NAME,
    APP_VERSION,
    CHATBOT_HEIGHT,
    QUICK_QUESTIONS
)

# ==========================================================
# Custom CSS
# ==========================================================

CUSTOM_CSS = """

.gradio-container{
    max-width:1450px !important;
    margin:auto;
}

footer{
    visibility:hidden;
}

#header{
    text-align:center;
    padding:20px;
}

#header h1{
    font-size:34px;
    margin-bottom:5px;
}

#header p{
    font-size:18px;
    color:#777;
}

.sidebar-title{
    font-size:20px;
    font-weight:bold;
    margin-bottom:10px;
}

.feature-box{

    padding:12px;

    border-radius:12px;

    background:#f7f7f7;

    margin-top:20px;

}

.quick-btn{

    width:100%;

}

"""

# ==========================================================
# UI
# ==========================================================

with gr.Blocks(

    title=APP_NAME,

    css=CUSTOM_CSS,

    theme=gr.themes.Soft(

        primary_hue="blue",

        secondary_hue="slate"

    )

) as demo:

    # ======================================================
    # Header
    # ======================================================

    gr.HTML(

f"""

<div id="header">

<h1>🚌 {APP_NAME}</h1>

<p>

Find the Best Tamil Nadu Private Omni Bus using AI

</p>

</div>

"""

)

    # ======================================================
    # Main Layout
    # ======================================================

    with gr.Row():

        # ==================================================
        # Sidebar
        # ==================================================

        with gr.Column(scale=1):

            gr.Markdown("## 💡 Quick Questions")

            quick_buttons = []

            for question in QUICK_QUESTIONS:

                button = gr.Button(

                    value=question,

                    elem_classes="quick-btn",

                    variant="secondary"

                )

                quick_buttons.append(button)

            gr.Markdown("---")

            gr.Markdown("""

### Supported Features

✅ Route Search

✅ Cheapest Bus

✅ Luxury Bus

✅ AC Sleeper

✅ Volvo

✅ Amenities

✅ Timings

✅ Operators

✅ Ratings

✅ Available Seats

""")

        # ==================================================
        # Chat Section
        # ==================================================

        with gr.Column(scale=4):

            chatbot = gr.Chatbot(

                label="AI Bus Assistant",

                height=CHATBOT_HEIGHT,

                bubble_full_width=False,

                show_copy_button=True,

                type="messages"

            )

            history = gr.State([])

            user_input = gr.Textbox(

                placeholder="Ask your question here...",

                lines=2,

                show_label=False,

                autofocus=True

            )

            with gr.Row():

                send_btn = gr.Button(

                    "📨 Send",

                    variant="primary"

                )

                clear_btn = gr.Button(

                    "🗑 Clear",

                    variant="secondary"

                )

                retry_btn = gr.Button(

                    "🔄 Retry",

                    variant="secondary"

                )

# ==========================================================
# Chat Functions
# ==========================================================

def send_message(message, history):
    """
    Send a message to the chatbot.
    """

    if history is None:
        history = []

    if message is None:
        return "", history

    message = message.strip()

    if message == "":
        return "", history

    try:

        response = chatbot_response(message)

    except Exception as e:

        response = f"❌ Error\n\n{str(e)}"

    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    return "", history


# ==========================================================
# Quick Question Handler
# ==========================================================

def quick_question(question, history):
    """
    Handle quick question buttons.
    """

    return send_message(question, history)


# ==========================================================
# Retry
# ==========================================================

def retry(history):

    if history is None:
        return history

    if len(history) < 2:
        return history

    last_question = None

    for item in reversed(history):

        if item["role"] == "user":

            last_question = item["content"]

            break

    if last_question is None:
        return history

    # Remove last assistant reply
    if history[-1]["role"] == "assistant":
        history.pop()

    try:

        answer = chatbot_response(last_question)

    except Exception as e:

        answer = str(e)

    history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return history


# ==========================================================
# Clear Chat
# ==========================================================

def clear_chat():

    return [], []


# ==========================================================
# Send Button
# ==========================================================

send_btn.click(

    fn=send_message,

    inputs=[
        user_input,
        history
    ],

    outputs=[
        user_input,
        chatbot
    ]

)

# ==========================================================
# Press Enter
# ==========================================================

user_input.submit(

    fn=send_message,

    inputs=[
        user_input,
        history
    ],

    outputs=[
        user_input,
        chatbot
    ]

)

# ==========================================================
# Clear Button
# ==========================================================

clear_btn.click(

    fn=clear_chat,

    outputs=[
        chatbot,
        history
    ]

)

# ==========================================================
# Retry Button
# ==========================================================

retry_btn.click(

    fn=retry,

    inputs=history,

    outputs=chatbot

)

# ==========================================================
# Quick Question Buttons
# ==========================================================

for button, question in zip(
    quick_buttons,
    QUICK_QUESTIONS
):

    button.click(

        fn=lambda h, q=question: quick_question(q, h),

        inputs=[
            history
        ],

        outputs=[
            user_input,
            chatbot
        ]

    )



