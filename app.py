import os
import gradio as gr
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Load system prompt from file
with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Initialize the model
llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Tools
search = DuckDuckGoSearchRun(name="web_search")
tools = [search]

# Agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

# Create agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

def chat(message, history):
    chat_history = []
    for human, ai in history:
        chat_history.append(HumanMessage(content=human))
        chat_history.append(AIMessage(content=ai))

    response = agent_executor.invoke({
        "input": message,
        "chat_history": chat_history
    })
    return response["output"]

demo = gr.ChatInterface(
    fn=chat,
    title="Reddsoligarch Labs"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
