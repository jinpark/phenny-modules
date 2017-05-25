# -*- coding: utf8 -*-

from sopel import web
from sopel.module import commands, example

import requests

BASE_URL = "http://api.waqi.info/"
SEARCH_URL = "http://api.waqi.info/search/?token={}&keyword={}"
FEED_URL = "http://api.waqi.info/feed/{}/?token={}"
LAT_LNG_FEED_URL = "http://api.waqi.info/feed/geo:{};{}/?token={}"

def search_keyword(bot, location):
    key = bot.config.apikeys.aqicn_key
    search = requests.get(SEARCH_URL.format(key, location)).json()
    uid = search["data"][0]["station"]["uid"]
    feed = requests.get(FEED_URL.format(uid)).json()
    return feed["data"]

def get_feed(bot, uid):
    key = bot.config.apikeys.aqicn_key
    print(['getfeed', uid])
    r = requests.get(FEED_URL.format(uid, key)).json()
    return r

def aqicn_uid_lat_lng_search(bot, lat, lng):
    key = bot.config.apikeys.aqicn_key
    search = requests.get(LAT_LNG_FEED_URL.format(lat, lng, key)).json()
    # if search["status"] == 'OK'
    uid = search["data"]["idx"]
    return uid

def search_keyword_uid(bot, location):
    key = bot.config.apikeys.aqicn_key
    search = requests.get(SEARCH_URL.format(key, location)).json()
    uid = search["data"][0]["station"]["uid"]
    return uid

def aqi_status(aqi):
    if aqi < 50:
        return "Good"
    elif 50 <= aqi < 100:
        return "Moderate"
    elif 100 <= aqi < 150:
        return "Unhealthy for Sensitive Groups"
    elif 150 <= aqi < 200:
        return "Unhealthy"
    elif 250 <= aqi < 300:
        return "Very Unhealthy"
    elif aqi > 300:
        return "Hazardous"

def construct_airq_string(bot, uid):
    data = get_feed(bot, uid)
    print(['construct', data])
    if data["status"] == "ok":
        data = data["data"]
        aqi = data["aqi"]
        city = data["city"]["name"]
        dominant_pollution = data["dominentpol"]
        pm25 = data["iaqi"]["pm25"]["v"]
        pm10 = data["iaqi"]["pm10"]["v"]
        status = aqi_status(aqi)

        return "Current Air Quality in {} is {}. AQI is {}. Dominant pollution is {}. pm25: {} pm10: {}" \
                .format(city, status, aqi, dominant_pollution, pm25, pm10)
    return "stupid bob"

@commands('air', 'aq', 'airq')
@example('.air seoul')
def air_quality(bot, trigger):
    """.air location - Show the air quality at the given location."""
    # If no input, check current user. If input, check if input is a user or search location instead

    location_or_nick = trigger.group(2)
    try:
        location_or_nick = trigger.group(2).lower()
    except:
        location_or_nick = ''

    nick = trigger.nick.lower()

    if not location_or_nick:
        # looking for self
        uid = bot.db.get_nick_value(nick, 'uid')
        if not uid:
            latitude = bot.db.get_nick_value(nick, 'latitude')
            longitude = bot.db.get_nick_value(nick, 'longitude')
            if latitude:
                uid = aqicn_uid_lat_lng_search(bot, latitude, longitude)
            else: 
                return bot.msg(trigger.sender, "I don't know where you live. " +
                           'Give me a location, like .air London, or tell me where you live by saying .setlocation London, for example.')
    else:
        location_or_nick = location_or_nick.strip()
        if bot.db.get_nick_value(location_or_nick, 'uid'):
            nick = location_or_nick
            uid = bot.db.get_nick_value(nick, 'uid')
            if not uid:
                latitude = bot.db.get_nick_value(nick, 'latitude')
                longitude = bot.db.get_nick_value(nick, 'longitude')
                if latitude:
                    uid = aqicn_uid_lat_lng_search(bot, latitude, longitude)
                else: 
                    return bot.msg(trigger.sender, "I don't know who this is or they don't have their location set.")
        else: 
            uid = search_keyword_uid(bot, location_or_nick)

    if not uid:
        return bot.reply("I don't know where that is.")

    airquality_text = construct_airq_string(bot, uid)
    bot.say(airquality_text)
