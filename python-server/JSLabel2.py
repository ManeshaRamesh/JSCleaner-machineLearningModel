#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
import random
import pymysql.cursors
from os import path, listdir
from tempfile import gettempdir
import os
import binascii
import time



import requests
from collections import OrderedDict
import pandas
import numpy as np
import sklearn
import pickle

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

print "Status: 200 Ok"
print "Content-Type: application/json;charset=utf-8"
print ""


connection = pymysql.connect(host='86.97.179.52',
                             user='jscleaner_remote',
                             port=8306,
                             password='comnets@2019',
                             db='mydb_mitmjscleaner',
                             autocommit=True)


filename = "ml_model.sav"

featuresListFile = open("featuresList.json", "r")

featuresList = json.load(featuresListFile)

loaded_model = pickle.load(open(filename, 'rb'))
# feature store (50 features)
FEATURES = ['replace',
            'createElement',
            'javaEnabled',
            'get',
            'getElementById',
            'appendChild',
            'toString',
            'takeRecords',
            'getElementsByTagName',
            'addEventListener',
            'getAttribute',
            'append|replace',
            'open',
            'forEach',
            'preventDefault',
            'keys',
            'setAttribute',
            'setTimeout',
            'querySelector',
            'insertBefore',
            'add',
            'appendChild|createElement|open|setAttribute|write',
            'addEventListener|postMessage',
            'closest',
            'focus',
            'write',
            'min',
            'removeAttribute',
            'error',
            'animate',
            'removeChild',
            'postMessage',
            'remove',
            'contains',
            'addEventListener|createElement|querySelectorAll|replace',
            'sendBeacon',
            'max',
            'replaceState',
            'defaultValue',
            'attachEvent|createElement|getElementById|open',
            'removeEventListener',
            'search',
            'filter',
            'appendChild|querySelector',
            'createTextNode',
            'values',
            'add|appendChild|remove',
            # pylint: disable=line-too-long
            'appendChild|createElement|getElementById|getElementsByTagName|open|removeChild|setAttribute',
            'start',
            'appendChild|getAttribute|removeEventListener|replace']



#make request 

#get script content and store in a variable

def get_resource(url):
	req = requests.get(url, verify=False)
	try:
		#print req.text.encode('utf-8')
		return req.text
	except KeyError:
		return None

#once you recieve teh c


def extract_features(content_text):
	if not content_text:
		return None
	tmp = OrderedDict()
	for feature in FEATURES:
		tmp[feature] = None
		if '|' not in feature:
			tmp[feature] = (content_text.count("."+feature+"(") + content_text.count("."+feature+" ("))
	for feature in FEATURES:
		if '|' in feature:
			feats = feature.split('|')
			res = 1
			for feat in feats:
				try:
					if tmp[feat] == 0:
						res = 0
						break
				except KeyError:
					if ("."+feat+"(") not in content_text and ("."+feat+" (") not in content_text:
						res = 0
						break
			tmp[feature] = res
	vector = pandas.Series(tmp)
	return vector


cgitb.enable()
form = cgi.FieldStorage()

url = form["url"].value
details = []
data = []


f1 = open("JSplugin.log","a")
log = url +","
sTime = time.time()

if (len(url) > 760):
	hashed_url = str(hash(url))
else:
	hashed_url = url
# check if label is in database
with connection.cursor(pymysql.cursors.DictCursor) as cursor:
	# print str(item)
	query = "SELECT * FROM pluginLabels where requestUrl = '"+ hashed_url + "'"
	cursor.execute(query)
	result = cursor.fetchone()
	# print result
	# will be labelled using the ML model
	cursor.close()
	# print str(result) + " "+hashed_url + " " + url
	if result is None:
		# print "not in database"
		try: 
			content = get_resource(url);
			if len(content):
				vector = extract_features(content);
				new_output = loaded_model.predict([vector]) #this is your label to be displayed (ex: Ads...) c
				confidence = np.amax(loaded_model.predict_proba([vector])) #this is the confidence of prediction
			    # print (new_output , confidence)
			    # json_object =  json_object + "{ 'name': '"+url +"', 'label': '" + new_output[0] + "',  'accuracy': '"+  str(confidence) +"'} ,"
				confidence = confidence.item()
				# details.append(url)
				# details.append(new_output[0])
				# details.append(confidence)
			# else:
			# 	continue # if there is not content
				if (confidence  < 0.60):
					confidence = -2.0 # non-critical
					new_output[0] = 'others' 
					for i in featuresList:
						if featuresList[i] == "RW" or featuresList[i] == "W":
							if (content.find(i + "(") != -1):
								confidence = 2.0 # critical
								# print(i)
								break

				log += "Not in DB, label=" + str(new_output)+","

				# labelledscripts.append(entry)
				if new_output[0] == 'cdn':
					label = 'CDN'
				elif new_output[0] == 'ads':
					label = 'Advertising'
				elif new_output[0] == 'tag-manager':
					label = 'Tag Manager'
				elif new_output[0] == 'customer-success':
					label = 'Customer Success'
				else:
					label = new_output[0].capitalize()
				data.append({"name":url, "label":label, "accuracy": str(round(confidence, 2))})
				if (len(url) > 760):
					url = hash(url)
				try: 
					# for item in labelledscripts:
					with connection.cursor() as cursor:
						# print str(item)
						query = "INSERT INTO pluginLabels (requestUrl, label, accuracy) VALUES (%s, %s, %s)"
						cursor.execute(query, (url, new_output[0], str(round(confidence, 5))))
				finally: 
					cursor.close()
		except: 
			print "Error in labelling"
			# new_output = []
			# new_output.append("error")
			# new_output[0] = "error"
			# confidence = 0
			# data.append({"name":url, "label":new_output[0], "accuracy":str(round(confidence, 2))})
	

	# if is is in the database add to data 
	else:
		# get_resource(result["requestUrl"])
		# print "is in database"
		# json_string = "{" + "name: '"+ result["requestUrl"] + "', label: '" + result["label"] + "', accuracy: '" + result["accuracy"] + "'}"
		# if result != None:
		# toBeLabelled.remove(url)
		try: 
			# details.append(result["requestUrl"])
			# details.append(result["label"])
			# details.append(str(round(result["accuracy"])))

			if result["label"] == 'cdn':
				result["label"] = 'CDN'
			elif result["label"] == 'ads':
				result["label"] = 'Advertising'
			elif result["label"] == 'tag-manager':
				result["label"] = 'Tag Manager'
			elif result["label"] == 'customer-success':
				result["label"] = 'Customer Success'
			else:
				result["label"] = result["label"].capitalize()

			log += "Labeled, label="+result["label"]+","

			data.append({"name": url, "label": result["label"], "accuracy": str(round(float(result["accuracy"]), 2))})
		except:
			print "Error in getting from database"
			# new_output = []
			# new_output[0] = "error"
			# confidence = 0
			# data.append({"name":url, "label":new_output[0], "accuracy":str(round(confidence, 2))})

log += "total time=" + str(time.time()-sTime)+"\n"
f1.write(log)
f1.close()

# print ">>>>>>>>>>>>>>>>>>>> JSCLEANER <<<<<<<<<<<<<<<<<<<<"
print json.dumps(data, indent=4)


# # except:
# # print "Error - error sending request"

