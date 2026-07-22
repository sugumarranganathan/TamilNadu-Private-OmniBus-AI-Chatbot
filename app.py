"""
app.py
-------

Gradio interface for TamilNadu-Private-OmniBus-AI-Chatbot
"""

import gradio as gr

from chatbot import chatbot_response, WELCOME_MESSAGE


EXAMPLES = [
    "Show buses from Chennai to Madurai",
    "Luxury Sleeper buses",
    "Bus under 1000",
    "Night bus to Salem",
    "Bus with WiFi",
    "Cheapest bus to Coimbatore",
    "AC Sleeper bus",
    "Best rated bus",
]


def respond(message, history):
    history = history or []

    answer = chatbot_response(message)

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
    title="Tamil Nadu Private OmniBus AI Chatbot",
    theme=gr.themes.Soft(),
) as demo:

    gr.Markdown(
        "# 🚌 Tamil Nadu Private OmniBus AI Chatbot"
    )

    gr.Markdown(WELCOME_MESSAGE)

    chatbot = gr.Chatbot(
        type="messages",
        height=550,
        show_copy_button=True,
    )

    msg = gr.Textbox(
        placeholder="Ask about buses...",
        lines=1,
        scale=8,
    )

    send = gr.Button("Send", variant="primary")
    clear = gr.Button("Clear Chat")

    gr.Examples(
        examples=[[e] for e in EXAMPLES],
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

    clear.click(
        lambda: ("", []),
        outputs=[msg, chatbot],
    )

if __name__ == "__main__":
    demo.launch()
