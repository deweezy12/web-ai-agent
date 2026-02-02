import os
import gradio as gr
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# System prompt - EDIT THIS
SYSTEM_PROMPT = """Du bist ein hilfreicher Assistent für die Website hautliebeundlaser.de.
Beantworte Fragen freundlich und professionell auf Deutsch.

[Hier kannst du weitere Informationen über die Website hinzufügen]"""

# Initialize the model
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def chat(message, history):
    # Build message list
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for human, ai in history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))

    messages.append(HumanMessage(content=message))

    # Get response
    response = llm.invoke(messages)
    return response.content

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat,
    title="AI Chat",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
