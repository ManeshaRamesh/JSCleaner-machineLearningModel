
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from browsermobproxy import Server
# import json

# # from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.options import Options as FirefoxOptions


# server = Server("/Users/manesha/Desktop/University/Capstone/JSCleaner-machineLearningModel/evaluation/browsermob-proxy/bin/browsermob-proxy")
# server.start()
# proxy = server.create_proxy()

# d = DesiredCapabilities.FIREFOX
# d['loggingPrefs'] = {'browser': 'ALL'}

# firefox_binary = '/usr/local/bin/firefox-developer'  # Must be the developer edition!!!
# # driver = webdriver.Firefox(firefox_binary=firefox_binary)
# fp = webdriver.FirefoxProfile('/Users/manesha/Library/Application Support/Firefox/Profiles/et1zmgvb.Capstone')

# fp.set_proxy(proxy.selenium_proxy())
# driver = webdriver.Firefox(fp,  capabilities=d)


#  get websites from txt files


# driver.get(websites[0])


# proxy.new_har(websites[0], options={'captureHeaders': True})

# result = json.dumps(proxy.har, ensure_ascii=False)
# print result
# server.stop()    
# driver.quit()

# # a = input("go")
import csv


import os
header = ['url', 'Time to interactivity', 'Time to DOM completion', 'Page Load Time', 'Total Number requests', 'Total Number JS requests', 'Total Transfer Size', 'Transfer size of JS elements' ]


f_websites = open("websites2.txt", "r")
websites = []
# store websites in an array
for i in range(22):
    websites.append(f_websites.readline().rstrip())
with open('BaseCase/Fixes/BaseCaseFixes.csv', 'a') as csvfile3:
    writer3 = csv.writer(csvfile3, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer3.writerow(header)

with open('FirstPageLoadBatch/Fixes/FirstPageLoadBatchFixes.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
with open('SecondPageLoadBatch/Fixes/SecondPageLoadBatchFixes.csv', 'a') as csvfile2:
    writer2 = csv.writer(csvfile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer2.writerow(header)

for url in websites:
    command = "python harRecorder/harRecorder3.py " + url
    print command
    os.system(command)
    command2 = "python harRecorder/harRecorder2.py " + url
    os.system(command2)
    command3 = "python harRecorder/harRecorder4.py " + url
    os.system(command2)
    break

