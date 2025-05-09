
from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
import asyncio

app = Flask(__name__)

# Ersetze durch deine Azure App-ID und dein Passwort (aus App-Registrierung)
APP_ID = ""
APP_PASSWORD = ""

# Adapter konfigurieren
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Beispielantworten – später ersetzbar durch DB-Zugriffe
antworten = {
    "passwort vergessen": "Kein Problem! Du kannst dein Passwort über den folgenden Link zurücksetzen: [Passwort-Link]",
    "terminbuchung nicht möglich": "Bitte prüfe, ob du eingeloggt bist. Falls das Problem weiterhin besteht, kontaktiere den Support.",
    "teilnehmer-id & problem eingeben": "Bitte gib deine Teilnehmer-ID sowie eine kurze Beschreibung des Problems ein, damit wir dir weiterhelfen können."
}

# Logik bei eingehender Nachricht
async def on_message(context: TurnContext):
    user_message = context.activity.text.lower()
    antwort = antworten.get(user_message, f"Ich habe deine Nachricht erhalten: '{context.activity.text}'. Ein Mitarbeiter wird sich bald melden.")
    await context.send_activity(antwort)

# Bot-Endpunkt
@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(adapter.process_activity(activity, auth_header, on_message))
    loop.run_until_complete(task)
    return Response(status=201)
