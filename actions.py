# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World my first action!")

        return []

class ActionRestaurantSearch(Action):

    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        for e in entities:
            if e['entity'] == 'hotel':
                name=e['value']
            if name == 'indian':
                message =  "Indian1, Indian2, Indian3, Indian4, Indian5"
            if name == 'chinese':
                message =  "chinese1, chinese2, chinese3, chinese4, chinese5"
            
            if name == 'thai':
                message =  "thai1, thai2, thai3, thai4, thai5"
            if name == 'italian':
                message =  "italian1, italian2, italian3, italian4, italian5"
            else:
                message = "Sorry please try something else..."
        dispatcher.utter_message(text=message)

        return []


class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = requests.get('https://api.covid19india.org/data.json').json()

        entities = tracker.latest_message['entities']
        state=None
        message = "Active cases are {0}\n, confirmed cases are {1}\n, Total deaths are {2}\n, Total patient recovered are {3}\n"
        for e in entities:
            if e['entity'] == 'state':
                state=e['value']
            for data in response["statewise"]:
                if data['state']==state.title():
                    
                    message = message.format(data['active'], data['confirmed'],data['deaths'],data['recovered'])

                
            
        dispatcher.utter_message(text=message)

        return []