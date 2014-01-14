
# kdheepak89@gmail.com

# Pulls data from google calender feed, uses current location read from file and calculates and writes transit details into file

import sys
import types
import urllib2
import time
# from bs4 import BeautifulSoup
# from datetime import datetime

# Function definition is here
def findvalinxml( list,tag ):
	# Add both the parameters and return them."
	# stringtag = 'hello world'
	for item in list.split('<'+tag+'>'):
		if((item.find('</'+tag+'>'))!=-1):
			stringtag = item.split('</'+tag+'>')[0]
			break
	return stringtag;


gcalURL = 'https://www.google.com/calendar/feeds/PRIVATEKEYHERE/basic?orderby=starttime&sortorder=ascending&futureevents=true&singleevents=true&max-results=1'

url = urllib2.urlopen(gcalURL)
content = url.read()

list = content.split("&lt;br /&gt;Where: ")
eventLoc = []
for item in list[1:]:
	eventLoc.append(item.split("&lt;br /&gt;")[0].strip().replace(" ","+"))

list = content.split("<content type='html'>When: ")
eventTime = []
for item in list[1:]:
	eventTime.append(item.split("CDT&lt;br /&gt;")[0].strip().replace("\xc2\xa0","").split(' to')[0])

list = content.split("<title type='html'>")
eventName = []
for item in list[1:]:
	eventName.append(item.split("</title>")[0].replace("\xc2\xa0",""))

new_eventTime = [item+' CDT' for item in eventTime]
eventTime=new_eventTime

eventStartTimeSecs=[]
for item in eventTime:
	try:
		eventStartTime = (time.strptime(item, "%a %b %d, %Y %I:%M%p %Z"))
	except ValueError:
		eventStartTime = (time.strptime(item, "%a %b %d, %Y %I%p %Z"))
	eventStartTimeSecs.append(time.mktime(eventStartTime))

# print eventLoc,'\n',eventTime,'\n',eventName, '\n', eventStartTimeSecs

# f = open('events','w')
# f.write(eventName[0]+';'+eventLoc[0]+';'+str(eventStartTimeSecs[0]))

f = open('location','r')
loc = f.read()

gdirURL = 'http://maps.googleapis.com/maps/api/directions/xml?&origin='+loc+'&destination='+eventLoc[0]+'&sensor=false&mode=transit&arrival_time='+str(int(eventStartTimeSecs[0]))

# print eventLoc[0]
# print time.strftime("%b %d %Y %H:%M:%S",time.localtime(eventStartTimeSecs[0]))

#print gdirURL

#print time.strftime("%b %d %Y %H:%M:%S",time.localtime(eventStartTimeSecs[0]))
#print time.strftime("%b %d %Y %H:%M:%S",time.localtime(1369643157))
#print time.strftime("%b %d %Y %H:%M:%S",time.localtime(time.time()))

#print 'google data ', time.strftime("%b %d %Y %H:%M:%S",time.localtime(1369972200))

gdirURL = 'http://maps.googleapis.com/maps/api/directions/xml?&origin='+loc+'&destination='+eventLoc[0]+'&sensor=false&mode=transit&arrival_time='+str(int(eventStartTimeSecs[0]))
url = urllib2.urlopen(gdirURL)
content = url.read()

list = content.split("<travel_mode>")

for item in list:
	if((item.find('TRANSIT'))!=-1):
		xmlcontent = item

try:
	list = xmlcontent
except NameError:
	departName = '0'
	departLineName = '0'
	departLineShortName = '0'
	departTime = '0'
	departTimeSecs = 0
	arrivalTime = '0'
	arrivalTimeSecs = 0
else:
	for item in list.split('<transit_details>'):
		if((item.find('</transit_details>'))!=-1):
			xmlcontent = item
		
	list = xmlcontent

	departName = findvalinxml(findvalinxml(list,'departure_stop'),'name')
	departLineName = findvalinxml(findvalinxml(list,'line'),'name')
	departLineShortName = findvalinxml(findvalinxml(list,'line'),'short_name')
	departTime = findvalinxml(findvalinxml(list,'departure_time'),'text')
	departTimeSecs = findvalinxml(findvalinxml(list,'departure_time'),'value')
	arrivalTime = findvalinxml(findvalinxml(list,'arrival_time'),'text')
	arrivalTimeSecs = findvalinxml(findvalinxml(list,'arrival_time'),'value')

f = open('journeydetails','w')
f.write(departName+';'+departLineName+' ('+departLineShortName+');'+departTime+';'+arrivalTime)

# print 'Starting location - '+departName
# print 'Bus - '+departLineName+'('+departLineShortName+')'
# print 'Start time - '+time.strftime("%b %d %Y %H:%M:%S",time.localtime(float(departTimeSecs)))
# for item in list.split('<departure_stop>'):
#	if((item.find('</departure_stop>'))!=-1):
#		print item.split('</departure_stop>')[0]
				

gdirURL = 'http://maps.googleapis.com/maps/api/directions/xml?&origin='+loc+'&destination='+eventLoc[0]+'&sensor=false&mode=transit&arrival_time='+str(int(eventStartTimeSecs[0]))
url = urllib2.urlopen(gdirURL)
content = url.read()

xmlout = open('output','w')
xmlout.write(content)

list = content.split("<travel_mode>")

for item in list:
	if((item.find('TRANSIT'))!=-1):
		xmlcontent = item

try:
	list = xmlcontent
except NameError:
	departName = '0'
	departLineName = '0'
	departLineShortName = '0'
	departTime = '0'
	departTimeSecs = 0
	arrivalTime = '0'
	arrivalTimeSecs = 0
else:
	for item in list.split('<transit_details>'):
		if((item.find('</transit_details>'))!=-1):
			xmlcontent = item
		
	list = xmlcontent

	departName = findvalinxml(findvalinxml(list,'departure_stop'),'name')
	departLineName = findvalinxml(findvalinxml(list,'line'),'name')
	departLineShortName = findvalinxml(findvalinxml(list,'line'),'short_name')
	departTime = findvalinxml(findvalinxml(list,'departure_time'),'text')
	departTimeSecs = findvalinxml(findvalinxml(list,'departure_time'),'value')
	arrivalTime = findvalinxml(findvalinxml(list,'arrival_time'),'text')
	arrivalTimeSecs = findvalinxml(findvalinxml(list,'arrival_time'),'value')

f = open('journeydetails','w')
f.write(departName+';'+departLineName+' ('+departLineShortName+');'+departTime+';'+arrivalTime)

#####

eventStartTimeSecs[0]=eventStartTimeSecs[0] - 600
time.sleep(5)
gdirURL = 'http://maps.googleapis.com/maps/api/directions/xml?&origin='+loc+'&destination='+eventLoc[0]+'&sensor=false&mode=transit&arrival_time='+str(int(eventStartTimeSecs[0]))

url = urllib2.urlopen(gdirURL)
content = url.read()
list = content.split("<travel_mode>")

xmlout.write(content)

del xmlcontent

for item in list:
	if((item.find('TRANSIT'))!=-1):
		xmlcontent = item

print xmlcontent

try:
	list = xmlcontent
except NameError:
	departName = '0'
	departLineName = '0'
	departLineShortName = '0'
	departTime = '0'
	departTimeSecs = 0
	arrivalTime = '0'
	arrivalTimeSecs = 0
else:
	for item in list.split('<transit_details>'):
		if((item.find('</transit_details>'))!=-1):
			xmlcontent = item
		
	list = xmlcontent

	departName = findvalinxml(findvalinxml(list,'departure_stop'),'name')
	departLineName = findvalinxml(findvalinxml(list,'line'),'name')
	departLineShortName = findvalinxml(findvalinxml(list,'line'),'short_name')
	departTime = findvalinxml(findvalinxml(list,'departure_time'),'text')
	departTimeSecs = findvalinxml(findvalinxml(list,'departure_time'),'value')
	arrivalTime = findvalinxml(findvalinxml(list,'arrival_time'),'text')
	arrivalTimeSecs = findvalinxml(findvalinxml(list,'arrival_time'),'value')

f = open('journeydetails1','w')
f.write(departName+';'+departLineName+' ('+departLineShortName+');'+departTime+';'+arrivalTime)

#####

time.sleep(5)
eventStartTimeSecs[0]=eventStartTimeSecs[0] - 600

gdirURL = 'http://maps.googleapis.com/maps/api/directions/xml?&origin='+loc+'&destination='+eventLoc[0]+'&sensor=false&mode=transit&arrival_time='+str(int(eventStartTimeSecs[0]))

url = urllib2.urlopen(gdirURL)
content = url.read()
list = content.split("<travel_mode>")

xmlout.write(content)

try: 
	del xmlcontent
except NameError:
	temp = 0

for item in list:
	if((item.find('TRANSIT'))!=-1):
		xmlcontent = item

print xmlcontent

try:
	list = xmlcontent
except NameError:
	departName = '0'
	departLineName = '0'
	departLineShortName = '0'
	departTime = '0'
	departTimeSecs = 0
	arrivalTime = '0'
	arrivalTimeSecs = 0
else:
	for item in list.split('<transit_details>'):
		if((item.find('</transit_details>'))!=-1):
			xmlcontent = item
		
	list = xmlcontent

	departName = findvalinxml(findvalinxml(list,'departure_stop'),'name')
	departLineName = findvalinxml(findvalinxml(list,'line'),'name')
	departLineShortName = findvalinxml(findvalinxml(list,'line'),'short_name')
	departTime = findvalinxml(findvalinxml(list,'departure_time'),'text')
	departTimeSecs = findvalinxml(findvalinxml(list,'departure_time'),'value')
	arrivalTime = findvalinxml(findvalinxml(list,'arrival_time'),'text')
	arrivalTimeSecs = findvalinxml(findvalinxml(list,'arrival_time'),'value')

f = open('journeydetails2','w')
f.write(departName+';'+departLineName+' ('+departLineShortName+');'+departTime+';'+arrivalTime)