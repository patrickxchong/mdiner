import time
starting = time.time()
#import the library used to query a website
import urllib.request

#import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup

import datetime
import threading
import queue


def getUrl(q, url):
    print('getUrl('+url+') called from a thread.')
    q.put(BeautifulSoup(urllib.request.urlopen(url), "html.parser"))

def getFood(output_str, soup, food, datelist, dining):
    print('ok')

def ribscraper(food_,start,numdays):
    #start = "2017-12-31"
    #food_ = "Ribs"
    #numdays = 10
    output = ""
    date = start.split("-")

    base = datetime.datetime(int(date[0]),int(date[1]),int(date[2]))
    #base = datetime.date(2018, 1, 2)
    datelist = [base + datetime.timedelta(days=x) for x in range(0, int(numdays))]


    #specify the url
    mj = "https://dining.umich.edu/menus-locations/dining-halls/mosher-jordan/"
    burs = "https://dining.umich.edu/menus-locations/dining-halls/bursley/"
    eq = "https://dining.umich.edu/menus-locations/dining-halls/east-quad/"
    nq = "https://dining.umich.edu/menus-locations/dining-halls/north-quad/"
    sq = "https://dining.umich.edu/menus-locations/dining-halls/south-quad/"
    mark = "https://dining.umich.edu/menus-locations/dining-halls/markley/"

    dining = [mj, burs, eq, nq, sq, mark]

    location = {mj : "Mosher Jordan", burs : "Bursley", eq : "East Quad", nq : "North Quad", sq : "South Quad", mark : "Markley"}

    theurls = []


    for i in datelist:
        for hall in dining:
            date = i.strftime("%Y-%m-%d")
            dining_day = hall+"?menuDate=" + date
            theurls.append(dining_day)
            #Query the website and return the html to the variable 'page'



    threadQueue = queue.Queue()
    for u in theurls:
        t = threading.Thread(target=getUrl, args = (threadQueue,u))
        t.daemon = True
        t.start()


    for i in datelist:
        for hall in dining:
            date = i.strftime("%Y-%m-%d")
            soup = threadQueue.get()
            food_table=soup.find_all('div', {"class" : 'item-name'})
            for row in food_table:
                food = row.find(text=True)
                if(food.find(food_) != -1):
                    output += date + ": " + location[hall] + "<br>"
                    output += row.find(text=True) + ": Looks like we have this today! <br>"
                    output += "================================== <br><br>"

    if (len(output) == 0):
        output += "Oh noooo what you want isn't on the menu! :("

    output += "C'est tout! <br>"
    output += "Runtime : " + str(time.time()-starting)
    return output