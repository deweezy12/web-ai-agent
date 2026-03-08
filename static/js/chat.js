(function () {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const log = document.getElementById("chat-log");
  const send = document.getElementById("chat-send");
  const history = [];

  function append(text, role) {
    const p = document.createElement("p");
    p.className = "msg " + (role === "user" ? "msg-user" : "msg-bot");
    p.textContent = text;
    log.appendChild(p);
    log.scrollTop = log.scrollHeight;
  }

  async function ask(message) {
    send.disabled = true;
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history }),
      });

      const contentType = response.headers.get("content-type") || "";
      const raw = await response.text();
      let data = {};

      if (contentType.includes("application/json")) {
        try {
          data = JSON.parse(raw);
        } catch (_error) {
          throw new Error("Ungültige JSON-Antwort vom Server.");
        }
      } else {
        throw new Error("Server lieferte kein JSON (Status " + response.status + ").");
      }

      if (!response.ok) {
        throw new Error(data.error || "Unbekannter Fehler");
      }

      const reply = String(data.reply || "").trim() || "Keine Antwort erhalten.";
      append(reply, "bot");
      history.push([message, reply]);
    } catch (error) {
      append("Fehler: " + error.message, "bot");
    } finally {
      send.disabled = false;
      input.focus();
    }
  }

  append("Willkommen im Live-Chat. Wie kann ich helfen?", "bot");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    append(message, "user");
    input.value = "";
    ask(message);
  });
})();
