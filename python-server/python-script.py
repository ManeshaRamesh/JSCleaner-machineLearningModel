
import requests
from collections import OrderedDict
import pandas
import numpy as np
import pickle
import json


PROXY_IP = "127.0.0.1"
PROXY_PORT = 8080

HTTP_PROXY = "http://" + PROXY_IP + ":" + str(PROXY_PORT)
HTTPS_PROXY = "https://" + PROXY_IP + ":" + str(PROXY_PORT)
PROXYDICT = {"http": HTTP_PROXY, "https": HTTPS_PROXY}
PROXY = PROXY_IP + ":" + str(PROXY_PORT)
ENCODING = "utf-8"


filename = "ml_model.sav"

input = ["https://apis.google.com/_/scs/abc-static/_/js/k=gapi.gapi.en.jw7XZHvcak8.O/m=gapi_iframes,googleapis_client,plusone/rt=j/sv=1/d=1/ed=1/rs=AHpOoo-L1iz4xVj0PCdm2On38RCj6aYemA/cb=gapi.loaded_0"]


# PROXY_IP = "10.224.41.171"

loaded_model = pickle.load(open(filename, 'rb'),  encoding='latin-1')
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
    req = requests.get(url)
    try:
        return req.text
    except KeyError:
        return None

#once you recieve teh c


def extract_features(content_text):
    """Return vectorization of features in content_text."""
    if not content_text:
        return None
    tmp = OrderedDict()
    for feature in FEATURES:
        tmp[feature] = None
        if '|' not in feature:
            tmp[feature] = (content_text.count("."+feature+"(") +
                            content_text.count("."+feature+" ("))
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


def main():
    json_object = "{";
    for url in input:
        content = get_resource(url);
        vector = extract_features(content);
        new_output = loaded_model.predict([vector]) #this is your label to be displayed (ex: Ads...) c
        confidence = np.amax(loaded_model.predict_proba([vector])) #this is the confidence of prediction
        # print (new_output , confidence)
        json_object =  json_object + "{ 'name': '"+url +"', 'label': '" + new_output[0] + "',  'accuracy': '"+  str(confidence) +"'} ,"
    json_object = json_object[0:-1]; # remove the last comma
    json_object += "}"


    print(json.dumps(json_object))


    # the json object will be returned

                   

main()









