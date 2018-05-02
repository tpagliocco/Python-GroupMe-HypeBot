# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import random
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
bot_id = "d83162a10aef6bcaf531d322d1"

# random fact generator
def fact_delivery():
    knightFacts = [
        'Epsilon Chapter was started by Robbie Aguilar, a Gamma Chapter Brother who had transferred to ASU.',
        'The Oh So Dangerous Epsilon Chapter of Omega Delta Phi was founded on September 22, 1992.',
        'Beta Chapters expansion was conceived at a Juarez, Mexico bar called Spankys',
        'Lambda chapter (University of Washington) does an annual canned food drive with KDChi where we table outside of a local grocery store for 1987 minutes',
        'Jorge Rodriguez’s senior architecture project was designing the Omega Delta Phi headquarters. A model exists of it.',
        'West Texas State University Colony was granted Theta Chapter on April 16, 1994 and we still Theta. The 8th Wonder of the World. 16 Founders, 8 Charter Members.',
        'Xi Chapter is the first multicultural Greek organization established in the State of Oklahoma.',
        'University of Houston Downtown Colony was founded on January 14th, 2014.',
        'Although Delta Chapter says November 23, 1991 is their founding date, it really became an official Colony on November 17, 1990 at national conference.'
    ]
    fact = random.choice(knightFacts)
    return fact


# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
    # 'message' is an object that represents a single GroupMe message.
    message = request.get_json()

    # TODO: Your bot's logic here
    if 'hypefact!' in message['text'].lower() and not sender_is_bot(message):
        reply(fact_delivery())

    if 'cedrick' in message['text'].lower() and not sender_is_bot(messages):
        reply('Shhhhh dont let Ryan see us talking about Cedrick')

    return "ok", 200


################################################################################

# Send a message in the groupchat
def reply(msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id': bot_id,
        'text': msg
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()


# Send a message with an image attached in the groupchat
def reply_with_image(msg, imgURL):
    url = 'https://api.groupme.com/v3/bots/post'
    urlOnGroupMeService = upload_image_to_groupme(imgURL)
    data = {
        'bot_id': bot_id,
        'text': msg,
        'picture_url': urlOnGroupMeService
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()


# Uploads image to GroupMe's services and returns the new URL
def upload_image_to_groupme(imgURL):
    imgRequest = requests.get(imgURL, stream=True)
    filename = 'temp.png'
    postImage = None
    if imgRequest.status_code == 200:
        # Save Image
        with open(filename, 'wb') as image:
            for chunk in imgRequest:
                image.write(chunk)
        # Send Image
        headers = {'content-type': 'application/json'}
        url = 'https://image.groupme.com/pictures'
        files = {'file': open(filename, 'rb')}
        payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
        r = requests.post(url, files=files, params=payload)
        imageurl = r.json()['payload']['url']
        os.remove(filename)
        return imageurl


# Checks whether the message sender is a bot
def sender_is_bot(message):
    return message['sender_type'] == "bot"
