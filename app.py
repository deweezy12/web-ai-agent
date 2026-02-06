import os
import gradio as gr
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

# Load system prompt from file
with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Tools
search = DuckDuckGoSearchRun(name="web_search")
tools = [search]

# Initialize the model with tools bound
llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
).bind_tools(tools)

def chat(message, history):
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for human, ai in history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))

    messages.append(HumanMessage(content=message))

    # Let the model decide if it needs to search
    response = llm.invoke(messages)

    # If the model wants to use a tool, execute it
    if response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            result = search.invoke(tool_call["args"]["query"])
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        # Get final response after tool use
        response = llm.invoke(messages)

    return response.content

demo = gr.ChatInterface(
    fn=chat,
    title="Reddsoligarch Labs"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
