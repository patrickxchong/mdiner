#import the library used to query a website
import urllib.request

#import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup

import datetime


# from:2018-12-31&to:2018-01-01
def ribscraper(start,numdays):
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

    output += "Checking " + str(datelist[0].strftime("%Y-%m-%d")) + " to " + str(datelist[-1].strftime("%Y-%m-%d")) + "<br>"

    for i in datelist:
        for hall in dining:
            date = i.strftime("%Y-%m-%d")
            dining_day = hall+"?menuDate=" + date
            #Query the website and return the html to the variable 'page'
            page = urllib.request.urlopen(dining_day)
            #Parse the html in the 'page' variable, and store it in Beautiful Soup format
            soup = BeautifulSoup(page, "html.parser")

            #big_table=soup.find(id = 'mdining-menu-main')
            #print (big_table)

            food_table=soup.find_all('div', {"class" : 'item-name'})

            for row in food_table:
                food = row.find(text=True)

                if(food.find("Rib") != -1):
                    output += date + ": " + location[hall] + "<br>"
                    output += row.find(text=True) + ": Ribs Today! <br>"
                    output += "================================== <br><br>"
                    
    output += "C'est tout! <br>"
    return output