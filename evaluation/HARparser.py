#! /usr/bin/python

from __future__ import division



import matplotlib as mtp

import matplotlib.pyplot as plt

import matplotlib.patches as mpatches

import json

from matplotlib import font_manager as fm

#from matplotlib.patches import FancyArrowPatch

import math

import sys



from datetime import datetime

import time

import os

from urlparse import urlparse

import csv

import numpy as np



tBlocked = []

tDNS = []

tConnect = []

tSend = []

tWait = []

tReceive = []

totalDNS = []






def simplify_cdf(data):

    '''Return the cdf and data to plot

        Remove unnecessary points in the CDF in case of repeated data

        '''

    data_len = len(data)

    assert data_len != 0

    cdf = np.arange(data_len) / data_len

    simple_cdf = [0]

    simple_data = [data[0]]



    if data_len > 1:

        simple_cdf.append(1.0 / data_len)

        simple_data.append(data[1])

        for cdf_value, data_value in zip(cdf, data):

            if data_value == simple_data[-1]:

                simple_cdf[-1] = cdf_value

            else:

                simple_cdf.append(cdf_value)

                simple_data.append(data_value)

    assert len(simple_cdf) == len(simple_data)

    # to have cdf up to 1

    simple_cdf.append(1)

    simple_data.append(data[-1])



    return simple_cdf, simple_data



def cdfplot(data_in):

    """Plot the cdf of a data array

        Wrapper to call the plot method of axes

        """

    # cannot shortcut lambda, otherwise it will drop values at 0

    data = sorted(filter(lambda x: (x is not None and ~np.isnan(x)

                                    and ~np.isinf(x)),

                         data_in))



    data_len = len(data)

    if data_len == 0:

#        LOG.info("no data to plot")

        return

    simple_cdf, simple_data = simplify_cdf(data)



    #label = name

    #line = _axis.plot(simple_data, simple_cdf, drawstyle='steps', label=label)

    return simple_data, simple_cdf

    #adjust_plot()



def calculate_cp(arg1, arg2, arg3):

   # Add both the parameters and return them."

    index = sorted(range(len(arg1.sTime)),key=lambda x:arg1.sTime[x])



    sTime = [0]*len(arg1.sTime)

    eTime = [0]*len(arg1.sTime)

    Time = [0]*len(arg1.sTime)



    for i in range (0,len (arg1.sTime)):

        Time [i] = arg1.time[index[i]]

        sTime [i] = arg1.sTime[index[i]]

        eTime [i] = arg1.eTime[index[i]]



        tmptime = Time[0];

        endtime = eTime[0];



    for i in range (1, len (sTime)):

        if sTime [i] < endtime:

            if eTime [i] > endtime:

                tmptime = tmptime + eTime[i] - endtime

                endtime = eTime[i]

        else:

            tmptime = tmptime + Time[i]

            endtime = eTime[i]

    ##print arg2 + " time is " + str(tmptime) +" ms" + " and percetage of page load time is " + str(round(tmptime/x_lim/10.0, 2)) + "%"

    #return round(tmptime/x_lim/10.0, 2);

    return tmptime;



relevant_path = "./baseCase/"

included_extenstions = ['har'] ;

file_names = [fn for fn in os.listdir(relevant_path) if any([fn.endswith(ext) for ext in included_extenstions])];



class Data:

    time = None

    sTime = None

    eTime  = None



file_names.sort()


with open('baseCase/parsed/total/stats.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['url', 'size', 'js size', 'js requests', 'requests', 'load time'])

	for file in range (1, len(file_names)):

	    # print "------------" + str(file_names[file]) + "------------"  

	    print file_names[file], 



	    with open(relevant_path+str(file_names[file])) as json_file:
	    	# initializing variables for a cpecific page

	        data = json.load(json_file)

	        json_file.close()



	        log = data['log']

	        #  all teh entries of the page
	        entries = log ['entries'] 
	        jsentries = []
	        # page level time stats
	        pageTimings = log["pages"][0]["pageTimings"]


	        pagestarttime = -100

	        starttime = []

	        endtime = []

	        url = []

	        size = []
	        jssize = []



	        blocked = Data ()

	        blocked.time = []

	        blocked.sTime = []

	        blocked.eTime = []



	        dns = Data ()

	        dns.time = []

	        dns.sTime = []

	        dns.eTime = []



	        connect = Data ()

	        connect.time = []

	        connect.sTime = []

	        connect.eTime = []



	        send = Data ()

	        send.time = []

	        send.sTime = []

	        send.eTime = []



	        wait = Data ()

	        wait.time = []

	        wait.sTime = []

	        wait.eTime = []



	        receive = Data ()

	        receive.time = []

	        receive.sTime = []

	        receive.eTime = []



	        x_lim = 0

	        y_lim = (len (entries)+1)*1.2

	        pageloadtime=0



	        #fig =plt.figure(figsize=(20,y_lim/10))

	        #fig = plt.figure(figsize=(4, 30))

	        fig = plt.figure()



	        y = y_lim-1.2



	        # print "Stime" + "\t" + "Block" + "\t" + "DNS" + "\t" + "connect" + "\t" + "send" + "\t" + "wait" + "\t" + "receive" + "\t" + "url"



	        for entry in entries:
	        	#  for eachr equest
	            if entry["response"]["content"]["mimeType"] == "application/x-javascript" or entry["response"]["content"]["mimeType"] == "application/javascript" or entry["response"]["content"]["mimeType"] == "application/ecmascript" or entry["response"]["content"]["mimeType"] == "text/javascript" or entry["response"]["content"]["mimeType"] == "text/ecmascript":
	            	jsentries.append(entry)
	            	tmp = 0
	            	if 'headersSize' in entry['response']:
	            		tmp += entry['response']['headersSize']
	            	if 'bodySize' in entry['response']:
	            		tmp += entry['response']['bodySize']
	            	jssize.append(int(tmp/1000))

	            if  pagestarttime < 0:

	                pagestarttime = entry['startedDateTime']

	                pagestarttime = datetime.strptime(pagestarttime[:-6], '%Y-%m-%dT%H:%M:%S.%f')

	                pagestarttime = long(time.mktime(pagestarttime.timetuple())*1e3 + pagestarttime.microsecond/1e3)

	                starttime.append(0)

	                endtime.append(starttime[-1]+entry['time'])

	                pageloadtime = pageloadtime + entry['time']

	            else:

	                objectstarttime = entry['startedDateTime']

	                objectstarttime = datetime.strptime(objectstarttime[:-6], '%Y-%m-%dT%H:%M:%S.%f')

	                objectstarttime = long(time.mktime(objectstarttime.timetuple())*1e3 + objectstarttime.microsecond/1e3)

	                objectstarttime = objectstarttime - pagestarttime

	                starttime.append(objectstarttime)

	                endtime.append(starttime[-1]+entry['time'])

	                pageloadtime = pageloadtime + entry['time']



	            try:

	                blocked.time.append(entry['timings']['blocked'])

	                dns.time.append(entry['timings']['dns'])

	            except:

	                continue



	            if entry['timings']['dns'] != 0:

	                totalDNS.append(long(entry['timings']['dns']))



	            # if entry['timings']['dns'] > 15000:

	            #     print str(entry['timings']['dns']) + " " + str(file_names[file])



	            connect.time.append(entry['timings']['connect'])

	            send.time.append(entry['timings']['send'])

	            wait.time.append(entry['timings']['wait'])

	            receive.time.append(entry['timings']['receive'])

	            url.append(entry['request']['url'])



	            tmp = 0

	            if 'headersSize' in entry['response']:

	                tmp += entry['response']['headersSize']



	            if 'bodySize' in entry['response']:

	                tmp += entry['response']['bodySize']



	            size.append(int(tmp/1000))



	            if x_lim < endtime[-1]:

	                x_lim = endtime[-1]/1000.0



	            xy = starttime[-1]/1000.0, y,

	            width, height = entry['time']/1000.0, 1

	            color="black"



	            nameurl = urlparse(url[-1])

	            if nameurl.path != '/':

	                name=nameurl.path[-40:]

	            else:

	                name=nameurl.netloc

	            #if len (url[-1]) > 40:

	            #    name=url[-1][7:20]+"..."+url[-1][-20:len(url[-1])]

	            #else:

	            #    name=url[-1][7:len(url[-1])]



	            p = mpatches.Rectangle(xy, width, height, facecolor=color)

	            plt.gca().add_patch(p)



	            if entry['time'] >= 1000:

	                plt.annotate(str(entry['time']/1000.0)+'s', ([xy[0]+width+0.5, xy[1]+0.25]), size=16)

	            else:

	                plt.annotate(str(entry['time'])+'ms', ([xy[0]+width+0.5, xy[1]+0.25]), size=16)

	            plt.annotate(name, ([-4, xy[1]+0.25]), size=16)



	            # Blocking

	            blocked.sTime.append(starttime[-1])

	            blocked.eTime.append(starttime[-1]+blocked.time[-1])

	            xy = starttime[-1]/1000.0, y,

	            width, height = blocked.time[-1]/1000.0, 1

	            color="#E2C7AE"

	            p = mpatches.Rectangle(xy, width, height, facecolor=color, edgecolor=color)

	            plt.gca().add_patch(p)



	            # DNS

	            dns.sTime.append(blocked.eTime[-1])

	            dns.eTime.append(blocked.eTime[-1]+dns.time[-1])

	            xy = (starttime[-1]+blocked.time[-1])/1000.0, y,

	            width, height = dns.time[-1]/1000.0, 1

	            color="#66ccff"

	            p = mpatches.Rectangle(xy, width, height, facecolor=color, edgecolor=color)

	            plt.gca().add_patch(p)



	            # CONNECT

	            connect.sTime.append(dns.eTime[-1])

	            connect.eTime.append(dns.eTime[-1]+connect.time[-1])

	            xy = (starttime[-1]+blocked.time[-1]+dns.time[-1])/1000.0, y,

	            width, height = connect.time[-1]/1000.0, 1

	            color="#a5d842"

	            p = mpatches.Rectangle(xy, width, height, facecolor=color, edgecolor=color)

	            plt.gca().add_patch(p)



	            # SEND

	            send.sTime.append(connect.eTime[-1])

	            send.eTime.append(connect.eTime[-1]+send.time[-1])

	            xy = (starttime[-1]+blocked.time[-1]+dns.time[-1]+connect.time[-1])/1000.0, y,

	            width, height = send.time[-1]/1000.0, 1

	            color="#d99989"

	            p = mpatches.Rectangle(xy, width, height, facecolor=color, edgecolor=color)

	            plt.gca().add_patch(p)



	            # WAIT

	            wait.sTime.append(send.eTime[-1])

	            wait.eTime.append(send.eTime[-1]+wait.time[-1])

	            xy = (starttime[-1]+blocked.time[-1]+dns.time[-1]+connect.time[-1]+send.time[-1])/1000.0, y,

	            width, height = wait.time[-1]/1000.0, 1

	            color="#8c7caf"

	            p = mpatches.Rectangle(xy, width, height, facecolor=color, edgecolor=color)

	            plt.gca().add_patch(p)



	            # RECEIVE

	            receive.sTime.append(wait.eTime[-1])

	            receive.eTime.append(wait.eTime[-1]+receive.time[-1])

	            xy = (starttime[-1]+blocked.time[-1]+dns.time[-1]+connect.time[-1]+send.time[-1]+wait.time[-1])/1000.0, y,

	            width, height = receive.time[-1]/1000.0, 1

	            color="#A8A8A8"

	            p = mpatches.Rectangle(xy, width, height, facecolor=color, edgecolor=color)

	            plt.gca().add_patch(p)



	            y = y -1.2



	            # print str(starttime[-1]) + "\t" + str(blocked.time[-1]) + "\t" + str(dns.time[-1]) + "\t" + str(connect.time[-1]) + "\t" + str(send.time[-1]) + "\t" + str(wait.time[-1]) + "\t" + str(receive.time[-1]) + "\t" + str(url[-1])



	    xy = -4, y-0.5,

	    width, height = x_lim+6, 1.3

	    color="#A8A8A8"

	    p = mpatches.Rectangle(xy, width, height, facecolor=color)

	    plt.gca().add_patch(p)

	    plt.annotate(str(len(entries))+' requests', ([-3.5, xy[1]+0.4]), size=16)

	    plt.annotate('page load time: '+ str(x_lim)+"s", ([x_lim-3, xy[1]+0.4]), size=16)
	    # plt.annotate('Load Time: '+ LoadTime, size=16)
	    # plt.annotate('DOMContentLoadTime: '+ DOMContentLoadTime, size=16)



	    print ",", sum(size), ",", str(len(entries)), ",", str(x_lim)



	    plt.draw()

	    plt.xlim([-4,x_lim*1.2])

	    plt.ylim([-1.3,y_lim])



	    fig.set_size_inches(15,(4.5*y_lim)/x_lim)

	    plt.axis('off')

	    fig.savefig( "baseCase/parsed/"+ file_names[file][:-3]+".pdf", dpi=200)

	    plt.close(fig)



	    tBlocked.append(calculate_cp (blocked, "blocking", x_lim))

	    tDNS.append(calculate_cp (dns, "dns", x_lim))

	    tConnect.append(calculate_cp (connect, "connecting", x_lim))

	    tSend.append(calculate_cp (send, "sending", x_lim))

	    tWait.append(calculate_cp (wait, "waiting", x_lim))

	    tReceive.append(calculate_cp (receive, "receiving", x_lim))

	    # print "\n"
	    stats = []
	    stats.append(file_names[file].rstrip(".har"))
	    stats.append(sum(size))
	    stats.append(sum(jssize))
	    stats.append(len(jsentries))
	    stats.append(len(entries))
	    stats.append(str(x_lim))
	    writer.writerow(stats)
	    


	    




fracs = []

# print tBlocked

fracs.append(sum(tBlocked))

# print "\n"

# print tDNS

fracs.append(sum(tDNS))

# print "\n"

# print tConnect

fracs.append(sum(tConnect))

# print "\n"

# print tSend

fracs.append(sum(tSend))

# print "\n"

# print tWait

fracs.append(sum(tWait))

# print "\n"

# print tReceive

fracs.append(sum(tReceive))



#ls_output = os.system("ls *.har")



# print "DNS average " + str( sum(tDNS) / float(len(tDNS)))



fig1 = plt.figure()

num_bins = 50

counts, bins = np.histogram(tDNS, bins=num_bins)

bins = bins[:-1] + (bins[1] - bins[0])/2

probs = counts/float(counts.sum())

# print probs.sum() # 1.0

plt.bar(bins, probs, 1.0/num_bins)

fig1.savefig('baseCase/parsed/total/dnsdist.pdf')



fig1 = plt.figure()

simple_data, simple_cdf = cdfplot(totalDNS)

plt.plot(simple_data, simple_cdf, drawstyle='steps')

plt.xlim([0,8000])

fig1.savefig('baseCase/parsed/total/DNStotal.pdf', dpi=200)



#for x in range(0, len(simple_data)):

#    print simple_data[x], simple_cdf[x]



fig2 = plt.figure(figsize=(6,6))

colors= "#E2C7AE", "#66ccff", "#a5d842", "#d99989", "#8c7caf", "#A8A8A8"

labels = 'Blocked', 'DNS', 'Connect', 'Send', 'Wait', 'Receive'

# labels = '', '', '', '', '', ''

explode=(0, 0.05, 0, 0, 0, 0)

patches, texts, autotexts = plt.pie(fracs, colors=colors, explode=explode, labels=labels,

                                    autopct='%1.1f%%', shadow=True)

plt.axis(aspect=5/3)

params = {'legend.fontsize': 20,

         'legend.linewidth': 2,

         'font.size': 20

         }

plt.rcParams.update(params)

proptease = fm.FontProperties()

proptease.set_size('xx-large')

plt.setp(autotexts, fontproperties=proptease)

plt.setp(texts, fontproperties=proptease)



fig2.savefig('baseCase/parsed/total/piechart.pdf', dpi=200)



print fracs





