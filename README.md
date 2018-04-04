# AbbyCow

Server-side for a FB Chatbot using DialogFlow, Yelp and Google Maps APIs. Mine gives vegan restaurant recommendations but the code is general enough to be adapted to other use cases. I'm working on a full tutorial on to be posted on Medium, with links to the DialogFlow agent .json file and everything you need to get this bad boy up and running.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

Clone the repo and install the dependencies

```
pip install requirements.txt
```

That's pretty much it. Now open that flask and take a big sip.

```
export FLASK_APP=main.py
flask run
```

## Deployment

For free deployment, check out the tutorial referenced at the top. You will find instructions for serverless deployment on AWS Lamda via [Zappa](github.com/Miserlou/Zappa/)

## Built With

* [DialogFlow](http://www.dropwizard.io/1.0.2/docs/) - Dope Chatbot framework
* [Flask](https://maven.apache.org/) - Python web microframework
