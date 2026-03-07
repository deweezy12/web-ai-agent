import os
from flask import Flask, render_template, request, jsonify
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

app = Flask(__name__)

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


BUSINESS = {
    "name": "Valerio Giuseppe Scaglione Fliesenlegerei",
    "owner": "Valerio Scaglione",
    "phone": "+49 202 478880",
    "address_line_1": "Varresbecker Str. 193",
    "address_line_2": "42115 Wuppertal",
}

SERVICES = [
    "Fliesenverlegung",
    "Badsanierung",
    "Naturstein- und Mosaikarbeiten",
    "Reparatur- und Ausbesserungsarbeiten",
    "Beratung und Aufmaß",
]


@app.context_processor
def inject_globals():
    return {
        "business": BUSINESS,
    }


@app.route("/")
def startseite():
    return render_template("startseite.html", services=SERVICES)


@app.route("/ueber-uns")
def ueber_uns():
    return render_template("ueber_uns.html")


@app.route("/anfrage-stellen")
def anfrage_stellen():
    return render_template("anfrage_stellen.html")


@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")


@app.route("/live-chat")
def live_chat():
    return render_template("live_chat.html")


@app.route("/impressum")
def impressum():
    return render_template("impressum.html")


@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not message:
        return jsonify({"error": "message is required"}), 400

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for turn in history:
        if isinstance(turn, list) and len(turn) == 2:
            human, ai = turn
            if human:
                messages.append(HumanMessage(content=str(human)))
            if ai:
                messages.append(AIMessage(content=str(ai)))

    messages.append(HumanMessage(content=message))

    response = llm.invoke(messages)

    if response.tool_calls:
        messages.append(response)
        for tool_call in response.tool_calls:
            args = tool_call.get("args", {})
            query = args.get("query", "")
            result = search.invoke(query)
            messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
        response = llm.invoke(messages)

    return jsonify({"reply": response.content})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
