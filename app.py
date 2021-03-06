# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/
# IMPORTS
import os
import re
import random
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import requests
import time

app = Flask(__name__)
bot_id = os.getenv('BOT_ID')

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group test

@app.route('/', methods=['POST'])

def webhook():
    # 'message' is an object that represents a single GroupMe message.
    message = request.get_json()
    speaker = message['name']

    # nudes
    #if 'hairy bush' in message['text'].lower() and not sender_is_bot(message):
        #imgURL = 'https://lh3.googleusercontent.com/-KcACUCow5eM/AAAAAAAAAAI/AAAAAAAAApU/Chy90UyVVAk/photo.jpg'
        #reply_with_image(speaker + ' here you go',imgURL)

    #susan
    #if 'hi susan' in message['text'].lower() and not sender_is_bot(message):
        #imgURL = 'https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/31587889_10101675251344908_7201868137652813824_n.jpg?_nc_cat=0&oh=b8465166e2482892684f910c0ff28d19&oe=5B91DE9D'
        #reply_with_image(speaker + ' - Susan says hi',imgURL)

    #testing the @ feature
    #if 'repeattest!' in message['text'].lower() and not sender_is_bot(message):
        #reply('@'+speaker + ' - you just spoke to me: ')

    # sacraments
    if 'sacraments' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' - The Knights of Omega Delta Phi live the sacraments of Unity, Honesty, Integrity, and Leadership!')

    # If hypefact! is spoken, return random fact
    if 'hypefact!' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' - Here is your Hype Fact: ')
        reply(fact_delivery())

    # If hypefact! is spoken, return random fact
    if '8ball!' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' - Hypebot is generating predictions and performing machine learning: ')
        time.sleep(3)
        reply(eight_ball())

    # hypebot pledge questions
    if 'what is the greek alphabet hypebot' in message['text'].lower() or 'hypebot what is the greek alphabet' in message['text'].lower() and not sender_is_bot(message):
        reply('Sir ' + speaker + ' ,the Greek Alphabet is Alpha, Beta , Gamma, Delta, Epsilon, Zeta, Eta, Theta, Iota, Kappa, Lambda, Mu, Nu, Xi, Omnicron, Pi, Rho, Sigma, Tau, Upsilon, Phi, Chi, Psi, and Omega....Sir')

    # hypebot pledge questions
    if 'what is the national founding date hypebot' in message['text'].lower() or 'hypebot what is the national founding date' in message['text'].lower() and not sender_is_bot(message):
        reply('Sir ' + speaker + '...the Brotherhood of Omega Delta Phi Fraternity, Inc was founded on November 25, 1987..Sir')


    if 'what is the mission statement hypebot' in message['text'].lower() or 'hypebot what is the mission statement' in message['text'].lower and not sender_is_bot(message):
        reply('Sir, The purpose of this Brotherhood, a Service/Social fraternity dedicated to the needs and concerns of the community, is and shall be to promote and maintain the traditional values of Unity, Honesty, Integrity, and Leadership. This Brotherhood was founded in order to provide, to ANY man, a diverse fraternal experience which coincides with a higher education.')


    if 'what is the mission statement hypebot' in message['text'].lower() or 'hypebot what is the mission statement' in message['text'].lower() and not sender_is_bot(message):
        reply('Sir, The purpose of this Brotherhood, a Service/Social fraternity dedicated to the needs and concerns of the community, is and shall be to promote and maintain the traditional values of Unity, Honesty, Integrity, and Leadership.')
        reply('This Brotherhood was founded in order to provide, to ANY man, a diverse fraternal experience which coincides with a higher education.')
        


    # cedrick reference
    #if 'cedrick' in message['text'].lower() and not sender_is_bot(message):
        #reply(speaker + ' -- shhhhhhh dont let Ryan see us talking about Cedrick')

    # luis reference
    if 'luis' in message['text'].lower() and not sender_is_bot(message):
        reply('WITCHOOOOOO87LOVIINNNNNNNASSSSSSSSSSSS')

    # help hypebot! reference
    if 'help hypebot!' in message['text'].lower() and not sender_is_bot(message):
        reply('you can ask a question and then type 8ball! , you can type hypefact! for a fact, you can ask me PM questions, and other phrases will trigger me as well')

    # delta or chevon reference
    if 'delta or chevon' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker +' it is always a Delta')

    # nli promo ad
    if 'nli' in message['text'].lower() and not sender_is_bot(message):
        reply(speaker + ' just go to nlichicgo2018.com for info on NLI')
        #reply('Right now in Chicago the weather report is: ')
        #get_weather('Chicago')

    # clint dig
    #if 'clint' in message['text'].lower() and not sender_is_bot(message):
        #reply('I have more personality than Clints videos')

    # president reference
    if 'president' in message['text'].lower() and not sender_is_bot(message):
        reply('Someone say President? Check out www.tony2018.com')

    # corpus reference
    #if 'corpus' in message['text'].lower() and not sender_is_bot(message):
        #reply('Corpus - smh.')

    # help reference
    if 'help me hypebot' in message['text'].lower() and not sender_is_bot(message):
        reply('I am HypeBot version 1987.  Certain phrases will trigger me, you can also type hypefact! and I will shit out a random fact about ODPhi')

    # weather reference
    if 'weather in' in message['text'].lower() and not sender_is_bot(message):
        #reply('Currently at Alpha Chapter, it is ')
        #get_weather('Lubbock')
        match = re.search('[Ww]eather in (?P<city>\w+)', message['text'])
        #need to fix this double reg ex search so it can do two cities instead of just one
        #match = re.search('[Ww]eather in (?P<city>([A-Z]\w+\W+)+)', message['text'])
        if match:
            reply(speaker + ' The current weather in ' + match.group('city') + ' is as follows:')
            get_weather(match.group('city'))
        else:
            pass
            # maybe add text for i cant find the scenarios
            # the text does not contain "weather in {CITY}" pattern

    return "ok", 200


################################################################################
# Get weather

def get_weather(city):
    GOOGLEAPIKEY = 'AIzaSyCCnY8x4sSLo3JwfHJn1oj3w5qFGsHNwXI'  # your key for Google's geocoding API
    DARKSKYAPIKEY = '797fa78aa87c345ba6cccccbb189bccb'  # your key for Dark Sky's weather data API
    city = city.replace(' ', '+')  # replaces the space if state is also given e.g. 'gainesville, fl'
    googlebaseURL = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (
    city, GOOGLEAPIKEY)  # URL for googles geocoding api
    res = requests.get(googlebaseURL)
    res.raise_for_status()
    geocodeData = json.loads(res.text)
    geocode = geocodeData['results'][0]['geometry']['location']
    latitude = geocode['lat']
    longitude = geocode['lng']
    darkskybaseURL = 'https://api.darksky.net/forecast/%s/%s,%s' % (DARKSKYAPIKEY, latitude, longitude)
    res = requests.get(darkskybaseURL)
    res.raise_for_status()
    weatherData = json.loads(res.text)
    degree_sign = u'\N{DEGREE SIGN}'  # degree unicode character
    reply(weatherData['currently']['summary'] + ', ' + str(
        weatherData['currently']['apparentTemperature']) + degree_sign + 'F. ' + weatherData['hourly'][
              'summary'] + '\n\n' + weatherData['daily']['summary'])


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



# random fact generator
def fact_delivery():
    knightFacts = [
        'Epsilon Chapter was started by Robbie Aguilar, a Gamma Chapter Brother who had transferred to ASU.',
        'The Oh So Dangerous Epsilon Chapter of Omega Delta Phi was founded on September 22, 1992.',
        'Beta Chapters expansion was conceived at a Juarez, Mexico bar called Spankys',
        'Tony Pagliocco created me'
        'Lambda chapter (University of Washington) does an annual canned food drive with KDChi where we table outside of a local grocery store for 1987 minutes',
        'Jorge Rodriguez’s senior architecture project was designing the Omega Delta Phi headquarters. A model exists of it.',
        'West Texas State University Colony was granted Theta Chapter on April 16, 1994 and we still Theta. The 8th Wonder of the World. 16 Founders, 8 Charter Members.',
        'Xi Chapter is the first multicultural Greek organization established in the State of Oklahoma.',
        'Lateef Ipaye has 1987 KDX Littles',
        'University of Houston Downtown Colony was founded on January 14th, 2014.',
        'Although Delta Chapter says November 23, 1991 is their founding date, it really became an official Colony on November 17, 1990 at national conference.',
        'Mo Geb, a Xi Brother by the name of Joseph Reyes, Bouba, and Peter Jaravata are the Founders of the CaliKnights!!',
        'The 8th ODPhi founder of Omega Delta Phi on the 1987 student org application is John Enriquez.',
        'Beta Chapter was started by Oscar Leroy, an Alpha Chapter Brother who shared his first year odphi experience with his high school buddies who were attending UTEP in 1988.',
        'Gamma Chapter was also started by Oscar Leroy with his relationship to his high school buddy Jeff Martin.',
        'Zeta Chapter was Founded on April 25, 1991. Their founders were: Billy Ray Thompson, Rafael Rivers, Ruben Franco, Juan Dominguez, Hector Lopez, Victor Tarin, Ruben Sanchez, Jesus Sifuentes, & Daniel Gonzales'
    ]
    fact = random.choice(knightFacts)
    return fact

def eight_ball():

    responses = [
        'Yes that will happen...1987% chance',
        'No, Im sorry',
        'Maybe - but i really got nfc',
        'Future looks cloudy',
        'Im leaning towards saying yes'
    ]
    answer = random.choice(responses)
    return answer
