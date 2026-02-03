import os
import gradio as gr
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load system prompt from file
with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Initialize the model
llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def chat(message, history):
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for human, ai in history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))

    messages.append(HumanMessage(content=message))

    response = llm.invoke(messages)
    return response.content

demo = gr.ChatInterface(
    fn=chat,
    title="Hautliebe & Laser - Beautyberater"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
