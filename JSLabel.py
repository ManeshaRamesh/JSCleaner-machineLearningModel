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
from urllib import unquote



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





#if True:

# PROXY_IP = "127.0.0.1"
# PROXY_PORT = 8080

# HTTP_PROXY = "http://" + PROXY_IP + ":" + str(PROXY_PORT)
# HTTPS_PROXY = "https://" + PROXY_IP + ":" + str(PROXY_PORT)
# PROXYDICT = {"http": HTTP_PROXY, "https": HTTPS_PROXY}
# PROXY = PROXY_IP + ":" + str(PROXY_PORT)
# ENCODING = "utf-8"
connection = pymysql.connect(host='86.97.179.52',
   user='jscleaner_remote',
   port=8306,
   password='comnets@2019',
   db='mydb_mitmjscleaner',
   autocommit=True)


filename = "ml_model.sav"

featuresListFile = open("featuresList.json", "r")

featuresList = json.load(featuresListFile)

# inputs = ["https://apis.google.com/_/scs/abc-static/_/js/k=gapi.gapi.en.jw7XZHvcak8.O/m=gapi_iframes,googleapis_client,plusone/rt=j/sv=1/d=1/ed=1/rs=AHpOoo-L1iz4xVj0PCdm2On38RCj6aYemA/cb=gapi.loaded_0"]

# PROXY_IP = "10.224.41.171"

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
    """Request resource from proxy and return response."""
    req = requests.get(url, verify=False)
    try:
        return req.text
    except KeyError:
        return None

# #once you recieve teh c


def extract_features(content_text):
    """Return vectorization of features in content_text."""
    if not content_text:
        return None
    tmp = OrderedDict()
    for feature in FEATURES:
        tmp[feature] = None
        if '|' not in feature:
            tmp[feature] = (content_text.count("."+feature+"(") +content_text.count("."+feature+" ("))
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
data = []
entry = []
f1 = open("JSplugin.log","a")

sTime = time.time()


# toBeLabelled = [] #scripts not in teh database
# labelledscripts = []

# try:
urls = form["url"].value.split("*****") 
# print form["url"].value
# print urls
# urls = inputs

# # find already labelled scripts add to data list
for url in urls:
    log = url +","
    if (len(url) > 760):
        hashed_url = str(hash(url))
    else:
        hashed_url = url
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        query = "SELECT * FROM pluginLabels where requestUrl = '"+hashed_url + "'"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        # print "Result: " + str(result)
# will be labelled using the ML loaded_model
        if result is None:
            print "not in database"

            try:        
                content = get_resource(url);
                print "content" +  content
                if (len(content)):
                    vector = extract_features(content);
                    new_output = loaded_model.predict([vector]) #this is your label to be displayed (ex: Ads...) c
                    confidence = np.amax(loaded_model.predict_proba([vector])) #this is the confidence of prediction
                else:
                    # if there is no content - ignore and move onto the next script
                    continue
                # if the confidence is less than 0.60 set the label to Others and use the rule based model
                if (confidence  < 0.60):
                    confidence = -2.0 # non-critical
                    new_output[0] = 'others' 
                    for i in featuresList:
                        if featuresList[i] == "RW" or featuresList[i] == "W":
                            if (content.find(i + "(") != -1):
                                confidence = 2.0 # critical
                                print(i)
                                break

                if new_output[0] == 'cdn':
                    new_output[0] = 'CDN'
                elif new_output[0] == 'ads':
                    new_output[0] = 'Advertising'
                elif new_output[0] == 'tag-manager':
                    new_output[0] = 'Tag Manager'
                elif new_output[0] == 'customer-success':
                    new_output[0] = 'Customer Success'
                else:
                    new_output[0] = new_output[0].capitalize()
                print "pass"
                data.append({"name":url, "label":new_output[0], "accuracy":str(round(confidence, 2))})
                log += "Not in DB, label=" + str(data)+","
                with connection.cursor() as cursor:
                    query = "INSERT INTO pluginLabels (requestUrl, label, accuracy) VALUES (%s, %s, %s)"
                    cursor.execute(query, (url,new_output[0] , str(round(confidence, 5))))
            except: 
                # dont add it to database if there is an error
                print "Error - error in labelling"
                new_output = []
                new_output[0] = "error"
                confidence = 0
                data.append({"name":url, "label":new_output[0], "accuracy":str(round(confidence, 2))})



            # try:
            
            # finally: 
            cursor.close()
# if is is in the database add to data 
        else:
            print "is in database"
# json_string = "{" + "name: '"+ result["requestUrl"] + "', label: '" + result["label"] + "', accuracy: '" + result["accuracy"] + "'}"
# if result != None:
# toBeLabelled.remove(url)
            try:
                # if the confidence is less than 0.60 set the label to Others and use the rule based model

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
                data.append({"name": url, "label": "error", "accuracy": 1.0})

    cursor.close()





print json.dumps(data, indent=4)

# # label unlabelled scripts and add to data list

# # # try:
# # for url in toBeLabelled:
# # 	content = get_resource(url);
# # 	vector = extract_features(content);
# # 	new_output = loaded_model.predict([vector]) #this is your label to be displayed (ex: Ads...) c
# # 	confidence = np.amax(loaded_model.predict_proba([vector])) #this is the confidence of prediction
# #     # print (new_output , confidence)
# #     # json_object =  json_object + "{ 'name': '"+url +"', 'label': '" + new_output[0] + "',  'accuracy': '"+  str(confidence) +"'} ,"
# # 	entry.append(url)
# # 	entry.append(new_output[0])
# # 	entry.append(confidence)
# # 	labelledscripts.append(entry)
# # 	if new_output[0] == 'cdn':
# # 		new_output[0] = 'CDN'
# # 	elif new_output[0] == 'ads':
# # 		new_output[0] = 'Advertising'
# # 	elif new_output[0] == 'tag-manager':
# # 		new_output[0] = 'Tag Manager'
# # 	elif new_output[0] == 'customer-success':
# # 		new_output[0] = 'Customer Success'
# # 	else:
# # 		new_output[0] = new_output[0].capitalize()

# # 	data.append({"name":url, "label":new_output[0], "accuracy":confidence})

# print json.dumps(data, indent=4)
# except:
# print "Error - error sending request"






# except:
# 	print "Error: "
