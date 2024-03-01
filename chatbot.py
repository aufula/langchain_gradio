import gradio as gr
import openai
import os
from functools import partial

import chat_agent
from langchain.schema import (
    HumanMessage
)

def set_api_key(api_key):
    openai.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    return "API Key set successfully."

def get_response(chatbot, api_key, selected_model, user_input, conversation_history=""):
    set_api_key(api_key)

    # Preserve the memory of the current chatbot
    preserved_memory = chatbot.memory

    # Create a new chat agent based on the selected model and seed the memory
    chatbot = chat_agent.create_chatbot(model_name=selected_model, seed_memory=preserved_memory)

    # Get raw chat response
    response = chatbot.agent.run(user_input).strip()

    # Iterate through messages in ChatMessageHistory and format the output
    updated_conversation = '<div style="background-color: hsl(30, 100%, 30%); color: white; padding: 5px; margin-bottom: 10px; text-align: center; font-size: 1.5em;">Chat History</div>'
    for i, message in enumerate(chatbot.memory.chat_memory.messages):
        if isinstance(message, HumanMessage):
            prefix = "User: "
            background_color = "hsl(0, 0%, 40%)"  # Dark grey background
            text_color = "hsl(0, 0%, 100%)"  # White text
        else:
            prefix = "Chatbot: "
            background_color = "hsl(0, 0%, 95%)"  # White background
            text_color = "hsl(0, 0%, 0%)"  # Black text
        updated_conversation += f'<div style="color: {text_color}; background-color: {background_color}; margin: 5px; padding: 5px;">{prefix}{message.content}</div>'
    return updated_conversation


def main():
    api_key = os.environ.get("OPENAI_API_KEY")

    api_key_input = gr.components.Textbox(
        lines=1,
        label="Enter OpenAI API Key",
        value=api_key,
        type="password",
    )

    model_selection = gr.components.Dropdown(
        choices=["gpt-4", "gpt-3.5-turbo"],
        label="Select a GPT Model",
        value="gpt-3.5-turbo",
    )

    user_input = gr.components.Textbox(
        lines=3,
        label="Enter your message",
    )

    output_history = gr.outputs.HTML(
        label="Updated Conversation",
    )

    chatbot = chat_agent.create_chatbot(model_name=model_selection.value)

    inputs = [
        api_key_input,
        model_selection,
        user_input,
    ]

    iface = gr.Interface(
        fn=partial(get_response, chatbot),
        inputs=inputs,
        outputs=[output_history],
        title="LiveQuery GPT-4",
        description="A simple chatbot using GPT-4 and Gradio with conversation history",
        allow_flagging="never",
    )

    iface.launch(server_name="0.0.0.0", server_port=7861)


if __name__ == "__main__":
    main()
