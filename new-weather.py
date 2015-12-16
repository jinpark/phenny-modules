# -*- coding: utf8 -*-
"""
weather.py - Willie Yahoo! Weather Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright 2012, Edward Powell, embolalia.net
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""

from sopel import web
from sopel.module import commands, example

import feedparser
from lxml import etree
import requests

degc = "\xb0C"
degf = "\xb0F"
bold = "\x02"
forc = ['f','F','c','C']

def degreeToDirection(deg):
  if (337.5 <= deg <= 360) or (0 <= deg < 22.5):
    return "N"
  elif 22.5 <= deg < 67.5:
    return "NE"
  elif 67.5 <= deg < 112.6:
    return "E"
  elif 112.6 <= deg < 157.5:
    return "SE"
  elif 157.5 <= deg < 202.5:
    return "S"
  elif 202.5 <= deg < 247.5:
    return "SW"
  elif 247.5 <= deg < 292.5:
    return "W"
  elif 292.5 <= deg < 337.5:
    return "NW"


def setup(bot):
    pass

def woeid_search(query):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    # query = urllib.urlencode({'q': 'select * from geo.placefinder where text="%s"' % query})
    # body = web.get('http://query.yahooapis.com/v1/public/yql?' + query)
    payload = {'q': 'select * from geo.placefinder where text="%s"' % query}
    body = requests.get('http://query.yahooapis.com/v1/public/yql?', params=payload).content
    parsed = etree.fromstring(body)
    first_result = parsed.find('results/Result')
    if first_result is None or len(first_result) == 0:
        return None
    return first_result


def get_cover(parsed):
    try:
        condition = parsed.entries[0]['yweather_condition']
    except KeyError:
        return 'unknown'
    text = condition['text']
    # code = int(condition['code'])
    # TODO parse code to get those little icon thingies.
    return text


def get_temp(parsed):
    try:
        condition = parsed.entries[0]['yweather_condition']
    except KeyError:
        return 'unknown'
    temp = int(condition['temp'])
    f = round((temp * 1.8) + 32, 2)
    return ('%d\u00B0C (%d\u00B0F)' % (temp, f))


def get_pressure(parsed):
    try:
        pressure = parsed['feed']['yweather_atmosphere']['pressure']
    except KeyError:
        return 'unknown'
    millibar = float(pressure)
    inches = int(millibar / 33.7685)
    return ('%din (%dmb)' % (inches, int(millibar)))


def get_wind(parsed):
    try:
        wind_data = parsed['feed']['yweather_wind']
    except KeyError:
        return 'unknown'
    try:
        kph = float(wind_data['speed'])
    except ValueError:
        kph = -1
        # Incoming data isn't a number, default to zero.
        # This is a dirty fix for issue #218
    speed = int(round(kph / 1.852, 0))
    degrees = int(wind_data['direction'])
    if speed < 1:
        description = 'Calm'
    elif speed < 4:
        description = 'Light air'
    elif speed < 7:
        description = 'Light breeze'
    elif speed < 11:
        description = 'Gentle breeze'
    elif speed < 16:
        description = 'Moderate breeze'
    elif speed < 22:
        description = 'Fresh breeze'
    elif speed < 28:
        description = 'Strong breeze'
    elif speed < 34:
        description = 'Near gale'
    elif speed < 41:
        description = 'Gale'
    elif speed < 48:
        description = 'Strong gale'
    elif speed < 56:
        description = 'Storm'
    elif speed < 64:
        description = 'Violent storm'
    else:
        description = 'Hurricane'

    if (degrees <= 22.5) or (degrees > 337.5):
        degrees = '\u2191'
    elif (degrees > 22.5) and (degrees <= 67.5):
        degrees = '\u2197'
    elif (degrees > 67.5) and (degrees <= 112.5):
        degrees = '\u2192'
    elif (degrees > 112.5) and (degrees <= 157.5):
        degrees = '\u2198'
    elif (degrees > 157.5) and (degrees <= 202.5):
        degrees = '\u2193'
    elif (degrees > 202.5) and (degrees <= 247.5):
        degrees = '\u2199'
    elif (degrees > 247.5) and (degrees <= 292.5):
        degrees = '\u2190'
    elif (degrees > 292.5) and (degrees <= 337.5):
        degrees = '\u2196'

    return description + ' ' + str(speed) + 'kt (' + degrees + ')'


@commands('weather', 'wea')
@example('.weather London')
def weather(bot, trigger):
    """.weather location - Show the weather at the given location."""
    location = trigger.group(2)
    try:
        location = trigger.group(2).lower()
    except:
        location = ''
    woeid = ''
    nick = trigger.nick.lower()
    if not location:
        woeid = bot.db.get_nick_value(nick, 'woeid')
        latitude = bot.db.get_nick_value(nick, 'latitude')
        longitude = bot.db.get_nick_value(nick, 'longitude')
        location = bot.db.get_nick_value(nick, 'location')
        if not woeid:
            return bot.msg(trigger.sender, "I don't know where you live. " +
                           'Give me a location, like .weather London, or tell me where you live by saying .setlocation London, for example.')
    else:
        location = location.strip()
        if bot.db.get_nick_value(location, 'woeid'):
            nick = location
            woeid = bot.db.get_nick_value(nick, 'woeid')
            latitude = bot.db.get_nick_value(nick, 'latitude')
            longitude = bot.db.get_nick_value(nick, 'longitude')
            location = bot.db.get_nick_value(nick, 'location')
            if not woeid:
                return bot.msg(trigger.sender, "I don't know who this is or they don't have their location set.")
        else: 
            first_result = woeid_search(location)
            if first_result is not None:
                woeid = first_result.find('woeid').text
                latitude = first_result.find('latitude').text
                longitude = first_result.find('longitude').text
                location = first_result.find('line2').text
                if not location:
                    location = first_result.find('line1').text
                if not location:
                    location = first_result.find('line4').text

    if not woeid:
        return bot.reply("I don't know where that is.")
    wea_text = weabase(bot, latitude, longitude, location)
    bot.say(wea_text)

    # query = web.urlencode({'w': woeid, 'u': 'c'})
    # url = 'http://weather.yahooapis.com/forecastrss?' + query
    # parsed = feedparser.parse(url)
    # location = parsed['feed']['title']

    # cover = get_cover(parsed)
    # temp = get_temp(parsed)
    # pressure = get_pressure(parsed)
    # wind = get_wind(parsed)
    # bot.say(u'%s: %s, %s, %s, %s' % (location, cover, temp, pressure, wind))


@commands('wf', 'forecast')
@example('.wf London')
def weather_forecast(bot, trigger):
    """.weather location - Show the weather at the given location."""

    location = trigger.group(2)
    try:
        location = trigger.group(2).lower()
    except:
        location = ''
    woeid = ''
    units = 'si'
    nick = trigger.nick.lower()
    if not location:
        woeid = bot.db.get_nick_value(nick, 'woeid')
        latitude = bot.db.get_nick_value(nick, 'latitude')
        longitude = bot.db.get_nick_value(nick, 'longitude')
        location = bot.db.get_nick_value(nick, 'location')
        if not woeid:
            return bot.msg(trigger.sender, "I don't know where you live. " +
                           'Give me a location, like .weather London, or tell me where you live by saying .setlocation London, for example.')
    else:
        location = location.strip()
        if bot.db.get_nick_value(location, 'woeid'):
            nick = location
            woeid = bot.db.get_nick_value(nick, 'woeid')
            latitude = bot.db.get_nick_value(nick, 'latitude')
            longitude = bot.db.get_nick_value(nick, 'longitude')
            location = bot.db.get_nick_value(nick, 'location')
            if not woeid:
                return bot.msg(trigger.sender, "I don't know who this is or they don't have their location set.")
        else: 
            first_result = woeid_search(location)
            if first_result is not None:
                woeid = first_result.find('woeid').text
                latitude = first_result.find('latitude').text
                longitude = first_result.find('longitude').text
                location = first_result.find('line2').text
                if not location:
                    location = first_result.find('line1').text
                if not location:
                    location = first_result.find('line4').text
                units = 'si'

    if not woeid:
        return bot.reply("I don't know where that is.")

    wf_text = wfbase(bot, latitude, longitude, location, units)
    bot.say(wf_text)

@commands('setlocation', 'setloc')
@example('.setlocation Columbus, OH')
def update_woeid(bot, trigger):
    """Set your default weather location."""
    if bot.db:
        nick = trigger.nick.lower()
        first_result = woeid_search(trigger.group(2))
        if first_result is None:
            return bot.reply("I don't know where that is.")

        woeid = first_result.find('woeid').text
        latitude = first_result.find('latitude').text
        longitude = first_result.find('longitude').text
        location = first_result.find('line2').text
        if not location:
            location = first_result.find('line1').text
        if not location:
            location = first_result.find('line4').text
        timezone = get_timezone(bot, latitude, longitude)

        bot.db.set_nick_value(nick, 'woeid', woeid)
        bot.db.set_nick_value(nick, 'latitude', latitude)
        bot.db.set_nick_value(nick, 'longitude', longitude)
        bot.db.set_nick_value(nick, 'location', location)
        bot.db.set_nick_value(nick, 'tz', timezone)

        neighborhood = first_result.find('neighborhood').text or ''
        if neighborhood:
            neighborhood += ','
        city = first_result.find('city').text or ''
        state = first_result.find('state').text or ''
        country = first_result.find('country').text or ''
        try:
            uzip = first_result.find('uzip').text
        except:
            uzip = ''
        bot.reply('I now have you at WOEID %s (%s %s, %s, %s %s.) and at timezone %s' %
                  (woeid, neighborhood, city, state, country, uzip, timezone))
    else:
        bot.reply("I can't remember that; I don't have a database.")

def weabase(bot, latitude, longitude, location, units='si'):
    forecast_url = 'https://api.forecast.io/forecast/' + bot.config.apikeys.darksky_key + '/' + str(latitude) + ',' + str(longitude) + '?units=' + units
    json_forecast = requests.get(forecast_url).json()
    nowwea = json_forecast['currently']
    units = json_forecast['flags']['units']
    if units == 'us':
        deg = degf
        opp_deg = defc
        windspeedunits = "mph"
        opp_windspeedunits = "m/s"
    else:
        deg = degc
        opp_deg = degf
        windspeedunits = "m/s"
        opp_windspeedunits = "mph"
    return "{}: {}{} ({}{}) {}. Wind {} {} {} ({} {}). Feels like {} ({})".format(location, str(int(nowwea["temperature"])), deg, str(c_to_f(int(nowwea["temperature"]))), opp_deg, nowwea["summary"], degreeToDirection(nowwea["windBearing"]), str(round(nowwea["windSpeed"],1)), windspeedunits, str(round(ms_to_mph(nowwea["windSpeed"]),1)), opp_windspeedunits, str(round(nowwea["apparentTemperature"],1)), str(round(c_to_f(nowwea["apparentTemperature"]),1)) )

def wfbase(bot, latitude, longitude, location, units='si'):
    forecast_url = 'https://api.forecast.io/forecast/' + bot.config.apikeys.darksky_key + '/' + str(latitude) + ',' + str(longitude) + '?units=' + units
    weajson = requests.get(forecast_url).json()
    currentwea = weajson['daily']['data'][0]
    tomwea = weajson['daily']['data'][1]
    units = weajson['flags']['units']
    if units == 'us':
        deg = degf
    else:
        deg = degc
    return '{location} - Today: {min_temp}-{max_temp}{deg} {summary} Tomorrow: {tom_min}-{tom_max}{deg} {tom_summary} This Week: {week_summary}'.format(location=location, min_temp=str(int(round(currentwea["temperatureMin"]))), max_temp=str(int(round(currentwea["temperatureMax"]))), deg=deg, summary=currentwea["summary"],
                                                                                                                                                                                                        tom_min=str(int(round(tomwea["temperatureMin"]))), tom_max=str(int(round(tomwea["temperatureMax"]))), tom_summary=tomwea["summary"],
                                                                                                                                                                                                        week_summary=weajson['daily']['summary'])

def old_wea(woeid):
    query = web.urlencode({'w': woeid, 'u': 'c'})
    url = 'http://weather.yahooapis.com/forecastrss?' + query
    parsed = feedparser.parse(url)
    location = parsed['feed']['title']

    cover = get_cover(parsed)
    temp = get_temp(parsed)
    pressure = get_pressure(parsed)
    wind = get_wind(parsed)
    bot.say('%s: %s, %s, %s, %s' % (location, cover, temp, pressure, wind))

def c_to_f(temp):
    return temp * 1.8 + 32

def ms_to_mph(speed):
    return speed * 2.23694

def get_timezone(bot, lat, lon):
    timezonedb_url = "http://ws.geonames.org/timezoneJSON?lat={}&lng={}&username={}".format(lat, lon, bot.config.apikeys.geonames_username)
    tz_json = requests.get(timezonedb_url).json()
    return tz_json['timezoneId']

@commands('weac', 'weaf')
def weather_deprecated_message(bot, trigger):
	bot.say("weac and weaf are deprecated. Please use .wea instead")
	weather(bot, trigger)
