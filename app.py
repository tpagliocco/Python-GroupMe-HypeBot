# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import random
import urllib.request
import json
import urllib.parse
#from urllib.parse import urlencode
#from urllib.request import Request, urlopen
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
        'Lateef Ipaye has 1987 KDX Littles',
        'University of Houston Downtown Colony was founded on January 14th, 2014.',
        'Although Delta Chapter says November 23, 1991 is their founding date, it really became an official Colony on November 17, 1990 at national conference.',
        'Mo Geb, a Xi Brother by the name of Joseph Reyes, Bouba, and Peter Jaravata are the Founders of the CaliKnights!!',
        'The 8th ODPhi founder of omega delta phi on the 1987 student org application is John Enriquez.',
        'Beta Chapter was started by Oscar Leroy, an Alpha Chapter Brother who shared his first year odphi experience with his high school buddies who were attending UTEP in 1988.',
        'Gamma Chapter was also started by Oscar Leroy with his relationship to his high school buddy Jeff Martin.',
        'Zeta Chapter was Founded on April 25, 1991. Their founders were: Billy Ray Thompson, Rafael Rivers, Ruben Franco, Juan Dominguez, Hector Lopez, Victor Tarin, Ruben Sanchez, Jesus Sifuentes, & Daniel Gonzales'
    ]
    fact = random.choice(knightFacts)
    return fact


# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
    # 'message' is an object that represents a single GroupMe message.
    message = request.get_json()
    speaker = message['name']


    # TODO: Your bot's logic here
    # nudes
    if 'hairy bush' in message['text'].lower() and not sender_is_bot(message):
        imgURL = 'https://lh3.googleusercontent.com/-KcACUCow5eM/AAAAAAAAAAI/AAAAAAAAApU/Chy90UyVVAk/photo.jpg'
        reply_with_image(speaker + ' here you go',imgURL)

    # sacraments
    if 'sacraments' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' - The Knights of Omega Delta Phi live the sacraments of Unity, Honesty, Integrity, and Leadership!')

    # If hypefact! is spoken, return random fact
    if 'hypefact!' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' - Here is your Hype Fact: ')
        reply(fact_delivery())

    # hypebot pledge questions
    if 'what is the greek alphabet hypebot' in message['text'].lower() or 'hypebot what is the greek alphabet' in message['text'].lower() and not sender_is_bot(message):
        reply('Sir ' + speaker + ' ,the greek alphabet is Alpha, Beta , Gamma, Delta, Epsilon, Zeta, Eta, Theta, Iota, Kappa, Lambda, Mu, Nu, Xi, Omnicron, Pi, Rho, Sigma, Tau, Upsilon, Phi, Chi, Psi, and Omega....Sir')

    # cedrick reference
    if 'cedrick' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' -- shhhhhhh dont let Ryan see us talking about Cedrick')

    # delta or chevon reference
    if 'delta or chevon' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker +' it is always a Delta')

    # nli promo ad
    if 'nli' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' just go to nlichicgo2018.com for info on NLI')

    # clint dig
    if 'clint' in message['text'].lower() and not sender_is_bot(message):
        reply('I have more personality than Clints videos')

    # president reference
    if 'president' in message['text'].lower() and not sender_is_bot(message):
        reply('Someone say President? Check out www.tony2018.com')

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
