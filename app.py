import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

app = Flask(__name__)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


def get_allowed_origins():
    raw_origins = os.environ.get("ALLOWED_ORIGINS", "").strip()
    default_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://deweezy12.github.io",
    ]

    if not raw_origins:
        return default_origins

    if raw_origins == "*":
        return "*"

    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


CORS(
    app,
    resources={
        r"/api/*": {
            "origins": get_allowed_origins(),
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)

with (BASE_DIR / "prompt.txt").open("r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

search = DuckDuckGoSearchRun(name="web_search")
tools = [search]

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
).bind_tools(tools)


BUSINESS = {
    "name": "Notfall Elektriker Wuppertal",
    "owner": "Elektriker Notdienst",
    "phone": "+49 202 12345680",
    "address_line_1": "Varresbecker Str. 193",
    "address_line_2": "42115 Wuppertal",
    "service_area": "Wuppertal und Umgebung",
    "hours": "24/7 erreichbar",
    "maps_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2497.14880073439!2d7.101293577003866!3d51.2531695717566!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47b8d6e0b7a63ed9%3A0x8aea528dc914d126!2sVarresbecker%20Str.%20193%2C%2042115%20Wuppertal!5e0!3m2!1sde!2sde!4v1773623012764!5m2!1sde!2sde",
    "maps_link_url": "https://www.google.com/maps/search/?api=1&query=Varresbecker+Str.+193,+42115+Wuppertal",
}

SERVICES = [
    {
        "title": "Stromausfall und Sicherungen",
        "description": "Erste Einordnung bei komplettem oder teilweisem Stromausfall, ausgeloesten Sicherungen und wiederkehrenden Abschaltungen.",
    },
    {
        "title": "FI-Fehler und Steckdosen",
        "description": "Orientierung bei ausloesendem FI, spannungslosen Steckdosen, Schaltern ohne Funktion oder auffaelligen Geraeten.",
    },
    {
        "title": "Gefahrensignale richtig einschaetzen",
        "description": "Hinweise zu Rauch, Brandgeruch, Funken, Hitze oder sichtbaren Schaeden und wann sofortiger Einsatz noetig ist.",
    },
    {
        "title": "Elektriker-Notdienst",
        "description": "Klare Weiterleitung zum direkten Kontakt, wenn der Defekt nicht sicher von aussen eingegrenzt werden kann.",
    },
    {
        "title": "Kurze telefonische Vorbereitung",
        "description": "Welche Infos, Bilder oder Beobachtungen vor dem Anruf hilfreich sind, damit der Einsatz schneller eingeordnet werden kann.",
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


@app.get("/api/health")
def api_health():
    return jsonify({"ok": True})


@app.post("/api/chat")
def api_chat():
    try:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return jsonify({"error": "ANTHROPIC_API_KEY is not set"}), 500

        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()
        history = (data.get("history") or [])[-12:]

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
                result = search.invoke(query) if query else ""
                messages.append(
                    ToolMessage(content=result, tool_call_id=tool_call["id"])
                )
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
