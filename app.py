import os
from flask import Flask, render_template, request, jsonify
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Load system prompt from file
with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Tools
search = DuckDuckGoSearchRun(name="web_search")
tools = [search]

# Initialize the model with a fixed model ID requested by the user.
llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
).bind_tools(tools)


BUSINESS = {
    "name": "Valerio Giuseppe Scaglione Fliesenlegerei",
    "owner": "Valerio Scaglione",
    "phone": "+49 202 478880",
    "address_line_1": "Varresbecker Str. 193",
    "address_line_2": "42115 Wuppertal",
    "service_area": "Wuppertal und Umgebung",
    "hours": "Termine nach Vereinbarung",
    "maps_embed_url": "https://www.google.com/maps?q=Varresbecker+Str.+193,+42115+Wuppertal&output=embed",
}

SERVICES = [
    {
        "title": "Fliesenverlegung",
        "description": "Präzise Verlegung für Boden- und Wandflächen mit sauberem Fugenbild und klarer Ausrichtung.",
    },
    {
        "title": "Badsanierung",
        "description": "Begleitung vom ersten Aufmaß bis zur fertigen Oberfläche für moderne, belastbare Badbereiche.",
    },
    {
        "title": "Naturstein und Mosaik",
        "description": "Sorgfältige Verarbeitung hochwertiger Materialien für detailreiche Flächen und besondere Akzente.",
    },
    {
        "title": "Reparaturarbeiten",
        "description": "Ausbesserungen, Teilflächen und Instandsetzungen bei Schäden, Hohllagen oder gealterten Belägen.",
    },
    {
        "title": "Beratung und Aufmaß",
        "description": "Klare Einschätzung zu Material, Untergrund, Abdichtung und sinnvoller Umsetzung vor Ort.",
    },
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
    try:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return jsonify({"error": "ANTHROPIC_API_KEY is not set"}), 500

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

        content = response.content
        if isinstance(content, list):
            reply = " ".join(
                str(part.get("text", part)) if isinstance(part, dict) else str(part)
                for part in content
            ).strip()
        else:
            reply = str(content).strip()

        return jsonify({"reply": reply or "Keine Antwort erhalten."})
    except Exception as exc:
        return jsonify({"error": f"Serverfehler: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
