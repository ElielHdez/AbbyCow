#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script acts as backend for a DialogFLow Chatbot. It receives the Facebook Messenger user's location and looks up vegan restaurants around using Yelp and Google Maps, then returns a series of cards to the user, including, for each restaurant: Name, Distance from User, Picture, A button to call the business and A button to open a Google Map from the user's location to the chosen restaurant's location. For a working example, hit up Abby the Cow on Facebook.
# You can find more information about Yelp Fusion API on yelp.com/developers/v3
import json
from flask import Flask
from flask import request
import requests
from dotmap import DotMap
app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
# The access token of your Facebook Messenger App
access_token='EAACBDZCzUi38BALbxAuboeAWuRO8gxfzXaLnmD0J9EZB9FJxMiAyac1iUkrP5EZBNE0ZBKdtecZB0MLlvFB7KGjZCdyweIHjeU0SnfXa7u8FIbVfHVamjlUFjJwSNp96ZCd8Xj1VqiloMZArpmjvxwPLbIT4S4xFZCbfae9pr233ZABAZDZD'

@app.route('/abby/', methods=['POST'])
def recomendaciones():
    # The request context is parsed to access user's data
    r=request.get_json()
    user_id=r['originalRequest']['data']['sender']['id']
    coords=r['result']['contexts'][0]['parameters']
    longitude=str(coords['long'])
    latitude=str(coords['lat'])
    origins=latitude+','+longitude
    # Your Yelp Fusion API key goes here
    headers = {
        'Authorization': 'Bearer AIt4dAlCkBnYXTNPeeilwiKv-0xXdmaTlntfMMBm-bCoUlfdlFlbNS5HklSq3oqUcoAuq9ajXDssSp2qFhnoVf5dqsemwlyQpUlqzGEPTsCHOXChkITj64S4__6hWnYx',
    }
    # Include here whatever Yelp search filters you wish to apply
    payload = {
            #'term': 'vegan',
            #'categories': 'Vegan,Vegetarian',
            'latitude': latitude,
            'longitude': longitude,
    }
    # A request is made to Yelp, passing in the payload. Dotmap is used for easier parsing of the result
    response = DotMap(requests.get('https://api.yelp.com/v3/businesses/search', params=payload, headers=headers).json())
    # data and data2 are the data structures which will hold the restaurant's info
    # Each will hold 4 elements tops
    data={
      'messaging_type':'RESPONSE',
      'recipient':{
        'id':user_id
      }, 'message': {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'elements': []
            }
        }
    }
    }
    data2={
      'messaging_type':'RESPONSE',
      'recipient':{
        'id':user_id
      }, 'message': {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'elements': []
            }
        }
    }
    }
    # Counter goes up to 8 tops, one for each business
    counter=0
    for index, business in enumerate(response.businesses):
        # Only open businesses with a picture are used
        if business.image_url and business.is_closed==False:
            if counter<8:
                image=business.image_url
                destination_latitude = str(business.coordinates.latitude)
                destination_longitude = str(business.coordinates.longitude)
                destination_coordinates=destination_latitude+','+destination_longitude
                # A request is made to Google Maps API to get the distance from the business to the user
                a=requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&key=AIzaSyBfI7bob5KZFrPC4kQ-tzZzE63airiYsqU', params={'origins':origins, 'destinations': destination_coordinates}).json()
                distance=a['rows'][0]['elements'][0]['distance']['text']
                address=''
                for x in business.location.display_address[:2]: address+=x+' '
                # A condition to account for which variable will a particular business will be fit into
                if counter<4: message = data
                else: message = data2
                # The business data is appended onto the message
                message['message']['attachment']['payload']['elements'].append({
                                        'title': business.name,
                                        'image_url': image,
                                        'subtitle': address+' aprox. '+distance,
                                        'buttons': [
                                            {
                                                'title': 'Get Directions',
                                                'type': 'web_url',
                                                'url': 'https://maps.google.com/?saddr='+latitude+','+longitude+'&daddr='+destination_latitude+','+destination_longitude,
                                                'messenger_extensions': 'true',
                                                'webview_height_ratio': 'tall',
                                                'fallback_url': 'https://maps.google.com/?saddr='+latitude+','+longitude+'&daddr='+destination_latitude+','+destination_longitude
                                            },
                                            {
                                                'title': 'Call',
                                                'type': 'phone_number',
                                                'payload': business.display_phone
                                            }
                                        ]
                                    })
                counter+=1
    # Now completely populated, the food recommendations are sent
    headers= {'content-type': 'application/json'}
    r = requests.post('https://graph.facebook.com/me/messages?access_token='+access_token, data = json.dumps(data), headers=headers)
    r = requests.post('https://graph.facebook.com/me/messages?access_token='+access_token, data = json.dumps(data2), headers=headers)
    # Afterwards, a message is sent with an embedded button to allow the user to begin again
    quick_reply={
  'messaging_type':'RESPONSE',
  'recipient':{
    'id':user_id
  },
  'message':{
    'text':'Anything else? Just ask.',
    'quick_replies':[
      {
        'content_type':'text',
        'title':'Veggie Places Nearby',
        'payload':'Veggie Places Nearby'
      }
    ]
  }
  }

    r = requests.post('https://graph.facebook.com/me/messages?access_token='+access_token, data = json.dumps(quick_reply), headers=headers)
    print(r.text)
    return 'Hello, World!'
