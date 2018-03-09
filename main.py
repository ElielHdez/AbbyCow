#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Flask
from flask import request
import requests
from dotmap import DotMap
app = Flask(__name__)

if __name__ == "__main__":
    app.run()

access_token="EAACBDZCzUi38BALbxAuboeAWuRO8gxfzXaLnmD0J9EZB9FJxMiAyac1iUkrP5EZBNE0ZBKdtecZB0MLlvFB7KGjZCdyweIHjeU0SnfXa7u8FIbVfHVamjlUFjJwSNp96ZCd8Xj1VqiloMZArpmjvxwPLbIT4S4xFZCbfae9pr233ZABAZDZD"

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
    origins=latitude+","+longitude

    headers = {
        'Authorization': 'Bearer AIt4dAlCkBnYXTNPeeilwiKv-0xXdmaTlntfMMBm-bCoUlfdlFlbNS5HklSq3oqUcoAuq9ajXDssSp2qFhnoVf5dqsemwlyQpUlqzGEPTsCHOXChkITj64S4__6hWnYx',
    }

    payload = {
            'term': 'vegan',
            #'categories': 'Vegan,Vegetarian',
            'latitude': latitude,
            'longitude': longitude,
    }
        
    response = DotMap(requests.get('https://api.yelp.com/v3/businesses/search', params=payload, headers=headers).json())
    print (response)
    data={
      "messaging_type":"RESPONSE",
      "recipient":{
        "id":user_id
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
      "messaging_type":"RESPONSE",
      "recipient":{
        "id":user_id
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
                #image=image[:-6]+"l"+image[-4:]
                destination_latitude = str(business.coordinates.latitude)
                destination_longitude = str(business.coordinates.longitude)
                destination_coordinates=destination_latitude+","+destination_longitude

                a=requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&key=AIzaSyBfI7bob5KZFrPC4kQ-tzZzE63airiYsqU", params={"origins":origins, "destinations": destination_coordinates}).json()
                distance=a["rows"][0]["elements"][0]["distance"]["text"]

                address=""
                for x in business.location.display_address[:2]: address+=x+" "
                
                data["message"]["attachment"]["payload"]["elements"].append({
                                        "title": business.name,
                                        "image_url": image,
                                        "subtitle": address+" aprox. "+distance,
                                        "buttons": [
                                            {
                                                "title": "Get Directions",
                                                "type": "web_url",
                                                "url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+destination_latitude+","+destination_longitude,
                                                "messenger_extensions": "true",
                                                "webview_height_ratio": "tall",
                                                "fallback_url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+destination_latitude+","+destination_longitude
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
                #image=image[:-6]+"l"+image[-4:]
                destination_latitude = str(business.coordinates.latitude)
                destination_longitude = str(business.coordinates.longitude)
                destination_coordinates=destination_latitude+","+destination_longitude

                a=requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&key=AIzaSyBfI7bob5KZFrPC4kQ-tzZzE63airiYsqU", params={"origins":origins, "destinations": destination_coordinates}).json()
                distance=a["rows"][0]["elements"][0]["distance"]["text"]

                address=""
                for x in business.location.display_address[:2]: address+=x+" "
                
                data2["message"]["attachment"]["payload"]["elements"].append({
                                        "title": business.name,
                                        "image_url": image,
                                        "subtitle": address+" aprox. "+distance,
                                        "buttons": [
                                            {
                                                "title": "Get Directions",
                                                "type": "web_url",
                                                "url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+destination_latitude+","+destination_longitude,
                                                "messenger_extensions": "true",
                                                "webview_height_ratio": "tall",
                                                "fallback_url": "https://maps.google.com/?saddr="+latitude+","+longitude+"&daddr="+destination_latitude+","+destination_longitude
                                            },
                                            {
                                                "title": "Call",
                                                "type": "phone_number",
                                                "payload": business.display_phone
                                            }
                                        ]
                                    })

                counter+=1
            
            
    headers= {"content-type": "application/json"}
    r = requests.post("https://graph.facebook.com/me/messages?access_token="+access_token, data = json.dumps(data), headers=headers)
    r = requests.post("https://graph.facebook.com/me/messages?access_token="+access_token, data = json.dumps(data2), headers=headers)
    
    quick_reply={
  "messaging_type":"RESPONSE",
  "recipient":{
    "id":user_id
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
