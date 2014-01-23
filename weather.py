"""
new-wea.py - Phenny Weather Module using Dark Sky API
Copyright 2013, Jin Park - jinpark.net
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import urllib, simplejson, apikey, csv
from tools import deprecated

degc = "\xc2\xb0C "
degf = "\xc2\xb0F "
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

# def wf(phenny, input):
#   """Displays weather using Dark Sky API"""
#   userinput = str(input.group(2))
#   #create dict to search for nick/location
#   with open('nickloc.csv', 'rU') as f:
#     z = csv.reader(f)
#     nickdict = {}
#     for key, val in z:
#       nickdict[key] = val
#   nickname1 = input.nick
#   nickname2 = nickname1.strip().lower()
#   if nickname2 in nickdict:
#     if userinput in forc:
#       loc = nickdict[nickname2][0] + " " + userinput
#     elif userinput == 'None':
#       loc = nickdict[nickname2][0]
#     else:
#       loc = userinput
#   else:
#     loc = userinput
#   if loc == 'None':
#     urlunits = 'ca' 
#   elif loc[-2:] == " C" or loc[-2:] == " c":
#     urlunits = 'ca'
#     loc = loc[:-2]
#   elif loc[-2:] == " F" or loc[-2:] == " f":
#     urlunits = 'us'
#     loc = loc[:-2]
#   else:
#     urlunits = 'ca'
#   locinput1 = loc.strip().lower().encode('utf8')
#   htmlinput = urllib.quote(locinput1)
#   # url2 = 'http://nominatim.openstreetmap.org/search?q=' + htmlinput + '&format=json'
#   # jsonResponse = simplejson.load(urllib.urlopen(url2))
#   # lati = jsonResponse[0]['lat']
#   # longi = jsonResponse[0]['lon']
#   # loca = jsonResponse[0]['display_name']
#   url4 = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + htmlinput + '&sensor=true'
#   jsonResponse1 = simplejson.load(urllib.urlopen(url4))
#   longi = jsonResponse1['results'][0]['geometry']['location']['lng']
#   lati = jsonResponse1['results'][0]['geometry']['location']['lat']
#   loca = jsonResponse1['results'][0]['formatted_address']
#   url3 = 'https://api.forecast.io/forecast/' + apikey.darksky + '/' + str(lati) + ',' + str(longi) + '?units=' + urlunits
#   weajson = simplejson.load(urllib.urlopen(url3))
#   currentwea = weajson['daily']['data'][0]
#   tomwea = weajson['daily']['data'][1]
#   units = weajson['flags']['units']
#   if units == 'us':
#     deg = degf
#   else:
#     deg = degc
#   phennyout = loca.encode('utf8') + "\x02" + " Today: " + "\x02" + str(int(round(currentwea["temperatureMin"]))) + "\xc2\xb0/" + str(int(round(currentwea["temperatureMax"]))) + deg + currentwea["summary"].encode('utf8') + "\x02" + " Tomorrow: " + "\x02" + str(int(round(tomwea["temperatureMin"]))) + "\xc2\xb0/" + str(int(round(tomwea["temperatureMax"]))) + deg + tomwea["summary"].encode('utf8') + "\x02" + " This Week: " + "\x02" + weajson['daily']['summary'].encode('utf8')
#   phenny.say(phennyout)
# 
# wf.commands = ['wf']
# wf.priority = 'low'
# wf.example = '.wf 11361'

# @deprecated
# def wea(phenny, input):
#   """Displays weather using Dark Sky API"""
#   userinput = str(input.group(2))
#   #create dict to search for nick/location
#   with open('nickloc.csv', 'rU') as f:
#     z = csv.reader(f)
#     nickdict = {}
#     for key, val in z:
#       nickdict[key] = val
#   nickname1 = input.nick
#   nickname2 = nickname1.strip().lower()
#   if nickname2 in nickdict:
#     if userinput in forc:
#       loc = nickdict[nickname2] + " " + userinput
#     elif userinput == 'None':
#       loc = nickdict[nickname2]
#     else:
#       loc = userinput
#   else:
#     loc = userinput
#   if loc == 'None':
#     urlunits = 'ca' 
#   elif loc[-2:] == " C" or loc[-2:] == " c":
#     urlunits = 'ca'
#     loc = loc[:-2]
#   elif loc[-2:] == " F" or loc[-2:] == " f":
#     urlunits = 'us'
#     loc = loc[:-2]
#   else:
#     urlunits = 'ca'
#   locinput1 = loc.strip().lower().encode('utf8')
#   htmlinput = urllib.quote(locinput1)
#   url4 = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + htmlinput + '&sensor=true'
#   jsonResponse1 = simplejson.load(urllib.urlopen(url4))
#   longi = jsonResponse1['results'][0]['geometry']['location']['lng']
#   lati = jsonResponse1['results'][0]['geometry']['location']['lat']
#   loca = jsonResponse1['results'][0]['formatted_address']
#   url3 = 'https://api.forecast.io/forecast/' + apikey.darksky + '/' + str(lati) + ',' + str(longi) + '?units=' + urlunits
#   weajson = simplejson.load(urllib.urlopen(url3))
#   nowwea = weajson['currently']
#   units = weajson['flags']['units']
#   if units == 'us':
#     deg = degf
#     windspeedunits = "mph"
#   else:
#     deg = degc
#     windspeedunits = "km/h"
#   #phennyout = loca.encode('utf8') + ": " + str(int(round(nowwea["temperature"]))) + deg + nowwea["summary"] + ". Wind " + degreeToDirection(nowwea["windBearing"]) + " " + str(nowwea["windSpeed"]) + " " + windspeedunits
#   phennyout = str(int(round(nowwea["temperature"]))) + deg + nowwea["summary"] + ", Wind " + degreeToDirection(nowwea["windBearing"]) + " " + str(round(nowwea["windSpeed"],1)) + " " + windspeedunits + " in " + loca.encode('utf8') + "."
#   phenny.say(phennyout)
# 
# wea.commands = ['wea', 'weather']
# wea.priority = 'low'
# wea.example = '.wea 11361'

def weabase(loc, urlunits):
  locinput1 = loc.strip().lower().encode('utf8')
  htmlinput = urllib.quote(locinput1)
  url4 = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + htmlinput + '&sensor=true'
  jsonResponse1 = simplejson.load(urllib.urlopen(url4))
  longi = jsonResponse1['results'][0]['geometry']['location']['lng']
  lati = jsonResponse1['results'][0]['geometry']['location']['lat']
  loca = jsonResponse1['results'][0]['formatted_address']
  url3 = 'https://api.forecast.io/forecast/' + apikey.darksky + '/' + str(lati) + ',' + str(longi) + '?units=' + urlunits
  weajson = simplejson.load(urllib.urlopen(url3))
  nowwea = weajson['currently']
  units = weajson['flags']['units']
  if units == 'us':
    deg = degf
    windspeedunits = "mph"
  else:
    deg = degc
    windspeedunits = "km/h"
  return loca.encode('utf8') + ": " + str(int(round(nowwea["temperature"]))) + deg + nowwea["summary"] + ". Wind " + degreeToDirection(nowwea["windBearing"]) + " " + str(round(nowwea["windSpeed"],1)) + " " + windspeedunits + ". " + "Feels like " + str(round(nowwea["apparentTemperature"],1))

def weac(phenny, input):
  """Displays weather using Dark Sky API"""
  userinput = str(input.group(2)).strip()
  #create dict to search for nick/location
  with open('nickloc.csv', 'rU') as f:
    z = csv.reader(f)
    nickdict = {}
    for key, val in z:
      nickdict[key] = val
  nickname1 = input.nick
  nickname2 = nickname1.strip().lower()
  if nickname2 in nickdict:
    if userinput != "None":
      loc = userinput
    elif userinput == 'None':
      loc = nickdict[nickname2]
    else:
      loc = userinput
  else:
    loc = userinput
  urlunits = 'ca' 
  phennyout = weabase(loc, urlunits)
  phenny.say(phennyout)

weac.commands = ['weac']
weac.priority = 'low'
weac.example = '.weac 11361'

def weaf(phenny, input):
  """Displays weather using Dark Sky API"""
  userinput = str(input.group(2)).strip()
  #create dict to search for nick/location
  with open('nickloc.csv', 'rU') as f:
    z = csv.reader(f)
    nickdict = {}
    for key, val in z:
      nickdict[key] = val
  nickname1 = input.nick
  nickname2 = nickname1.strip().lower()
  if nickname2 in nickdict:
    if userinput != "None":
      loc = userinput
    elif userinput == 'None':
      loc = nickdict[nickname2]
    else:
      loc = userinput
  else:
    loc = userinput
  urlunits = 'us' 
  phennyout = weabase(loc, urlunits)
  phenny.say(phennyout)

weaf.commands = ['weaf']
weaf.priority = 'low'
weaf.example = '.weaf 11361'

def wfbase(urlunits, loc):
  locinput1 = loc.strip().lower().encode('utf8')
  htmlinput = urllib.quote(locinput1)
  url4 = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + htmlinput + '&sensor=true'
  jsonResponse1 = simplejson.load(urllib.urlopen(url4))
  longi = jsonResponse1['results'][0]['geometry']['location']['lng']
  lati = jsonResponse1['results'][0]['geometry']['location']['lat']
  loca = jsonResponse1['results'][0]['formatted_address']
  url3 = 'https://api.forecast.io/forecast/' + apikey.darksky + '/' + str(lati) + ',' + str(longi) + '?units=' + urlunits
  weajson = simplejson.load(urllib.urlopen(url3))
  currentwea = weajson['daily']['data'][0]
  tomwea = weajson['daily']['data'][1]
  units = weajson['flags']['units']
  if units == 'us':
    deg = degf
  else:
    deg = degc
  return loca.encode('utf8') + "\x02" + " Today: " + "\x02" + str(int(round(currentwea["temperatureMin"]))) + "\xc2\xb0/" + str(int(round(currentwea["temperatureMax"]))) + deg + currentwea["summary"].encode('utf8') + "\x02" + " Tomorrow: " + "\x02" + str(int(round(tomwea["temperatureMin"]))) + "\xc2\xb0/" + str(int(round(tomwea["temperatureMax"]))) + deg + tomwea["summary"].encode('utf8') + "\x02" + " This Week: " + "\x02" + weajson['daily']['summary'].encode('utf8')

def wfc(phenny, input):
  """Displays weather using Dark Sky API"""
  userinput = str(input.group(2)).strip()
  #create dict to search for nick/location
  with open('nickloc.csv', 'rU') as f:
    z = csv.reader(f)
    nickdict = {}
    for key, val in z:
      nickdict[key] = val
  nickname1 = input.nick
  nickname2 = nickname1.strip().lower()
  if nickname2 in nickdict:
    if userinput != "None":
      loc = userinput
    elif userinput == 'None':
      loc = nickdict[nickname2]
    else:
      loc = userinput
  else:
    loc = userinput
  urlunits = 'ca'
  phennyout = wfbase(urlunits, loc)
  phenny.say(phennyout)

wfc.commands = ['wfc']
wfc.priority = 'low'
wfc.example = '.wfc 11361'

def wff(phenny, input):
  """Displays weather using Dark Sky API"""
  userinput = str(input.group(2)).strip()
  #create dict to search for nick/location
  with open('nickloc.csv', 'rU') as f:
    z = csv.reader(f)
    nickdict = {}
    for key, val in z:
      nickdict[key] = val
  nickname1 = input.nick
  nickname2 = nickname1.strip().lower()
  if nickname2 in nickdict:
    if userinput != "None":
      loc = userinput
    elif userinput == 'None':
      loc = nickdict[nickname2]
    else:
      loc = userinput
  else:
    loc = userinput
  
  urlunits = 'us'
  phennyout = wfbase(urlunits, loc)
  phenny.say(phennyout)

wff.commands = ['wff']
wff.priority = 'low'
wff.example = '.wff 11361'

