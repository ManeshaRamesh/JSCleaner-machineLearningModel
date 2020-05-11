from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import sys, time
import threading
import unicodedata
from browsermobproxy import Server
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import codecs
import csv

# git clone git://github.com/AutomatedTester/browsermob-proxy-py.git
# python setup.py install

# url = sys.argv[1]

# server = Server("./harRecorder/browsermob-proxy-2.1.4/bin/browsermob-proxy")
# server.start()
# proxy = server.create_proxy({'captureHeaders': True, 'captureContent': True, 'captureBinaryContent': True})

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False) 
# selenium_proxy = proxy.selenium_proxy()
# profile.set_proxy(selenium_proxy)
driver = webdriver.Firefox(firefox_profile=profile)

f_websites = open("websites.txt", "r")
# f_FirstPageLoadSingleLoadTimes = open("./data/websites.txt", "w")
header = ['url', 'Time to interactivity', 'Time to DOM completion', 'Page Load Time', 'Total Number requests', 'Total Number JS requests', 'Total Transfer Size', 'Transfer size of JS elements' ]

websites = []
# store websites in an array
for i in range(100):
	websites.append(f_websites.readline().rstrip())

a = raw_input("go")

with open('FirstPageLoadSingle/FirstPageLoadSingleFinal.csv', 'a') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(header)
	for i in range(50):
		try:
			stats= []
			jssize = []
			size = []
			# proxy.new_har(websites[i])
			# go to the google home page
			driver.get(websites[i])
			navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
			responseStart = driver.execute_script("return window.performance.timing.responseStart")
			domComplete = driver.execute_script("return window.performance.timing.domComplete")
			domInteractive = driver.execute_script("return window.performance.timing.domInteractive")
			LoadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")
			Network =  driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

			print "1. Scrolling throught the page to make sure everything is loaded"
			scheight = 0
			while scheight < 15.0:
			    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
			    time.sleep(0.001)
			    scheight += .01  
			for entry in Network:
				if entry.get('transferSize'):
					size.append(entry['transferSize'])
				else:
					print entry
				if entry.get('initiatorType'):
					if entry['initiatorType'] == "script":
						if entry.get('transferSize'):
							jssize.append(entry['transferSize'])
						else:
							print entry
			print "	2. Recording page load time, page size, number fo requests as"
			print "	Time to Interactivity: " + str(domInteractive - navigationStart)
			print "	Time to DOM completion: " + str(domComplete - navigationStart)
			print "	Page Load Time: " + str(LoadEventEnd - navigationStart)
			print "	Total Number requests: " + str(len(size))
			print "	Total Number JS requests: " + str(len(jssize))
			print "	Total Transfer Size: " + str(sum(size))
			print "	Transfer size of JS elements: " + str(sum(jssize))



			stats.append(websites[i])
			stats.append((domInteractive - navigationStart)/1000.0)
			stats.append((domComplete - navigationStart)/1000.0)
			stats.append((LoadEventEnd - navigationStart)/1000.0)
			stats.append(len(size))
			stats.append(len(jssize))
			stats.append(sum(size))
			stats.append(sum(jssize))

			writer.writerow(stats)
		except:
			print "	 First Page Load  - Skipped: " + websites[i]
		

		# print "3. Saving the har file"
		# result = json.dumps(proxy.har, ensure_ascii=False)
		# filename = "./FirstPageLoadSingle/" + websites[i].replace("http://","").replace("https://","").strip('/').split('/')[0]+".har"
		# print "Filename: " + filename
		# f = codecs.open (filename ,"w", encoding='utf-8')
		# f.write(result)
		# f.close()
		# driver.close()
with open('SecondPageLoadSingle/SecondPageLoadSingleFinal.csv', 'a') as csvfile2:
	writer2 = csv.writer(csvfile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer2.writerow(header)
	for i in range(50):
		try:
			stats= []
			jssize = []
			size = []
			jsEntries = []
			# proxy.new_har(websites[i])
			# go to the google home page
			driver.get(websites[i])
			navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
			responseStart = driver.execute_script("return window.performance.timing.responseStart")
			domComplete = driver.execute_script("return window.performance.timing.domComplete")
			domInteractive = driver.execute_script("return window.performance.timing.domInteractive")
			LoadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")
			Network =  driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

			print "1. Scrolling throught the page to make sure everything is loaded"
			scheight = 0
			while scheight < 15.0:
			    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
			    time.sleep(0.001)
			    scheight += .01  
			for entry in Network:
				if entry.get('transferSize'):
					size.append(entry['transferSize'])
				else:
					print entry
				if entry.get('initiatorType'):
					if entry['initiatorType'] == "script":
						if entry.get('transferSize'):
							jssize.append(entry['transferSize'])
							jsEntries.append(entry)
						else:
							print entry
			print "	2. Recording page load time, page size, number fo requests as"
			print "	Time to Interactivity: " + str(domInteractive - navigationStart)
			print "	Time to DOM completion: " + str(domComplete - navigationStart)
			print "	Page Load Time: " + str(LoadEventEnd - navigationStart)
			print "	Total Number requests: " + str(len(size))
			print "	Total Number JS requests: " + str(len(jssize))
			print "	Total Transfer Size: " + str(sum(size))
			print "	Transfer size of JS elements: " + str(sum(jssize))




			stats.append(websites[i])
			stats.append((domInteractive - navigationStart)/1000.0)
			stats.append((domComplete - navigationStart)/1000.0)
			stats.append((LoadEventEnd - navigationStart)/1000.0)
			stats.append(len(size))
			stats.append(len(jssize))
			stats.append(sum(size))
			stats.append(sum(jssize))

			writer2.writerow(stats)
		except:
			print "	 Second Page Load - Skipped: " + websites[i]


driver.quit()


