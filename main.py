#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Flask
from flask import request
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import requests
app = Flask(__name__)

auth = Oauth1Authenticator(
    consumer_key="_3rqquCuNvP2w9-FQAlAzw",
    consumer_secret="SUWrRmcZa847aQlYZeFE4xAyrt0",
    token="PDXeNGjGDwnlL-ElIaN0vd4esr-uHCyM",
    token_secret="LWaCyn41FUmXac1OZ7Av6aYRVHg"
)

client = Client(auth)

@app.route('/', methods=['GET'])
def prueba():
    return "HOLI"

@app.route('/abby/', methods=['POST'])
def recomendaciones():
    r=request.get_json()
    user_id=r["originalRequest"]["data"]["sender"]["id"]
    coords=r["result"]["contexts"][0]["parameters"]
    longitude=str(coords["long"])
    latitude=str(coords["lat"])

    params = {
    'term': 'vegan',
    'lang': 'es',
    "sort": "1"
}
    response=client.search_by_coordinates(latitude, longitude, **params)

    data={
      "recipient":{
        "id":"1061938300592052"
      }, "message": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": []
            }
        }
    }
    }
    data2={
      "recipient":{
        "id":"1061938300592052"
      }, "message": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": []
            }
        }
    }
    }


    counter=0
    for index, business in enumerate(response.businesses):
        if business.image_url and business.is_closed==False:
            if counter<4:
                image=business.image_url
                image=image[:-6]+"l"+image[-4:]

                destinations=str(business.location.coordinate.latitude)+","+str(business.location.coordinate.longitude)
                origins=latitude+","+longitude
                a=requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&key=AIzaSyBfI7bob5KZFrPC4kQ-tzZzE63airiYsqU", params={"origins":origins, "destinations": destinations}).json()
                distance=a["rows"][0]["elements"][0]["distance"]["text"]

                address=""
                for x in business.location.address:
                    address+=x+" "
                data["message"]["attachment"]["payload"]["elements"].append({
                                        "title": business.name,
                                        "image_url": image,
                                        "subtitle": address+" aprox. "+distance,
                                        "buttons": [
                                            {
                                                "title": "Get Directions",
                                                "type": "web_url",
                                                "url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+str(business.location.coordinate.latitude)+","+str(business.location.coordinate.longitude),
                                                "messenger_extensions": "true",
                                                "webview_height_ratio": "tall",
                                                "fallback_url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+str(business.location.coordinate.latitude)+","+str(business.location.coordinate.longitude)
                                            },
                                            {
                                                "title": "Call",
                                                "type": "phone_number",
                                                "payload": business.display_phone
                                            }
                                        ]
                                    })

                counter+=1
            elif counter >=4 and counter <8:
                image=business.image_url
                image=image[:-6]+"l"+image[-4:]

                destinations=str(business.location.coordinate.latitude)+","+str(business.location.coordinate.longitude)
                origins=latitude+","+longitude
                a=requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&key=AIzaSyBfI7bob5KZFrPC4kQ-tzZzE63airiYsqU", params={"origins":origins, "destinations": destinations}).json()
                distance=a["rows"][0]["elements"][0]["distance"]["text"]

                address=""
                for x in business.location.address:
                    address+=x+" "
                data2["message"]["attachment"]["payload"]["elements"].append({
                                        "title": business.name,
                                        "image_url": image,
                                        "subtitle": address+" aprox. "+distance,
                                        "buttons": [
                                            {
                                                "title": "Get Directions",
                                                "type": "web_url",
                                                "url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+str(business.location.coordinate.latitude)+","+str(business.location.coordinate.longitude),
                                                "messenger_extensions": "true",
                                                "webview_height_ratio": "tall",
                                                "fallback_url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+str(business.location.coordinate.latitude)+","+str(business.location.coordinate.longitude)
                                            },
                                            {
                                                "title": "Call",
                                                "type": "phone_number",
                                                "payload": business.display_phone
                                            }
                                        ]
                                    })

                counter+=1

    access_token="EAACBDZCzUi38BAEUPyZCT57l739Jqgk2ElWtsZBcsqBKOde8zaa9V45Ss14bv7ouQlMm0NhPpTZBFEPziZBOMWtPeAzHw70uMDJlJqArELtnHPsjaHQDmBalnGx2ilXAyBzZAjQqzHNz35958p97JhnYfP2HeHkM2ZCYfMxLQWYWAZDZD"
    headers= {"content-type": "application/json"}
    r = requests.post("https://graph.facebook.com/me/messages?access_token="+access_token, data = json.dumps(data), headers=headers)
    r = requests.post("https://graph.facebook.com/me/messages?access_token="+access_token, data = json.dumps(data2), headers=headers)

    quick_reply={
  "recipient":{
    "id":"1061938300592052"
  },
  "message":{
    "text":"Anything else? Just ask.",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Veggie Places Nearby",
        "payload":"Veggie Places Nearby"
      }
    ]
  }
  }

    r = requests.post("https://graph.facebook.com/me/messages?access_token="+access_token, data = json.dumps(quick_reply), headers=headers)
    print(r.text)
    return 'Hello, World!'
