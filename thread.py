import time

#import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup

import datetime
import threading
import queue

import requests
import json
import datetime
import codecs
import sys

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

CACHE_FNAME = 'dining_sites.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

def getUrl(q, url):
    #print('getUrl('+url+') called from a thread.')
    q.put(BeautifulSoup(make_request_using_cache(url), "html.parser"))


def ribscraper(food_,start,numdays):
    # starting = time.time()
    #food_ = "Ribs"
    #start = "2017-01-04"
    #numdays = 2
    output = ""
    date = start.split("-")

    base = datetime.datetime(int(date[0]),int(date[1]),int(date[2]))
    #base = datetime.date(2018, 1, 2)
    datelist = [base + datetime.timedelta(days=x) for x in range(0, int(numdays))]

    output += "You're looking for <b>" + food_ + "</b><br>"
    output += "Checking " + str(datelist[0].strftime("%Y-%m-%d")) + " to " + str(datelist[-1].strftime("%Y-%m-%d")) + "<br><br>"
    
    #specify the url
    mj = "mosher-jordan"
    burs = "bursley"
    eq = "east-quad"
    nq = "north-quad"
    sq = "south-quad"
    mark = "markley"

    dining = [mj, burs, eq, nq, sq, mark]

    location = {mj : "Mosher Jordan", burs : "Bursley", eq : "East Quad", nq : "North Quad", sq : "South Quad", mark : "Markley"}

    theurls = []


    for i in datelist:
        date = i.strftime("%Y-%m-%d")
        for hall in dining:
            dining_day = "https://dining.umich.edu/menus-locations/dining-halls/" + hall+"?menuDate=" + date
            theurls.append(dining_day)
            #Query the website and return the html to the variable 'page'

    threadQueue = queue.Queue()
    for u in theurls:
        t = threading.Thread(target=getUrl, args = (threadQueue,u))
        t.daemon = True
        t.start()
    
    output += "<div class='food-wrapper'>"

    for i in datelist:
        date = i.strftime("%Y-%m-%d")
        for hall in dining:
            url = "https://dining.umich.edu/menus-locations/dining-halls/" + hall+"/?menuDate=" + date
            soup = threadQueue.get()
            food_table=soup.find_all('div', {"class" : 'item-name'})
            for row in food_table:
                food = row.find(text=True)
                if(food.find(food_) != -1):
                    output += "<a href="+url+" class='food'>"
                    output += "<p>" + location[hall] + "</p>"
                    output += "<p>" + date + "</p>"
                    output += "<p>" + row.find(text=True) + "</p>"
                    output += "</a>"

    output += "</div>"

    if (len(output) < (65 + len(food_))):
        output += "<p>Oh noooo what you want isn't on the menu! :(</p>"

    output += "<p>Voila!</p>"
    #output += "Runtime : " + str(time.time()-starting)
    return output