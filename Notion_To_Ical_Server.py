from flask import Flask, Response, jsonify
from notion_client import Client
from ics import Calendar, Event
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz
import os

app = Flask(__name__)

load_dotenv()

# Put your Notion API key and database ID here
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

notion = Client(auth=NOTION_API_KEY)

def fetch_notion_data(database_id):
    response = notion.databases.query(database_id=database_id)
    return response["results"]

def create_ical(events):
    calendar = Calendar()
    tz = pytz.timezone("Europe/Paris")  # CHoose your timezone here

    for item in events:
        event = Event()

        # CHange the property name to match your database
        if 'Project' in item['properties']:
            event.name = item['properties']['Project']['title'][0]['text']['content']
        
        if 'Timeline' in item['properties']:
            start_date = item['properties']['Timeline']['date']['start']
            end_date = item['properties']['Timeline']['date'].get('end')
            
            # Convertir les dates au fuseau horaire spécifié
            event.begin = datetime.fromisoformat(start_date).astimezone(tz)
            if end_date:
                event.end = datetime.fromisoformat(end_date).astimezone(tz)
            else:
                event.end = event.begin.replace(hour=18, minute=0)
        
        calendar.events.add(event)
    return calendar

@app.route("/calendar.ics")
def calendar():
    notion_data = fetch_notion_data(DATABASE_ID)
    ical_calendar = create_ical(notion_data)
    
    response = Response(str(ical_calendar), mimetype="text/calendar")
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
    return response

@app.route("/properties")
def properties():
    notion_data = fetch_notion_data(DATABASE_ID)
    
    # Créer une liste de dictionnaires pour stocker les propriétés de chaque élément
    properties_list = []
    for item in notion_data:
        item_properties = {}
        for prop_name, prop_value in item['properties'].items():
            # Ajouter le nom et la valeur de la propriété dans le dictionnaire
            item_properties[prop_name] = prop_value
        properties_list.append(item_properties)

    return jsonify(properties_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
