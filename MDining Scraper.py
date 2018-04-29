#import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
import time

import requests
import json
import re

CACHE_FNAME = 'dining_sites.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_menu(url):
    if url in CACHE_DICTION:
        return CACHE_DICTION[url]

    else:
        DAY = {}
        
        page = requests.get(url)

        #Parse the html in the 'page' variable, and store it in Beautiful Soup format
        soup = BeautifulSoup(page.text, "html5lib")

        for ul in soup.find_all('ul', {"class": 'traits'}):
            ul.decompose()

        for div in soup.find_all('div', {"class": 'nutrition'}):
            div.decompose()

        for i in soup.find_all('i', {"class": 'fa-minus'}):
            i.decompose()
        
        counter = 0;
        menu=soup.find('div', {"id": 'mdining-items'})
        meals=menu.select("h3 a")
        courses = menu.find_all('ul', {"class" : 'courses_wrapper'})
        for meal in meals:
            DAY[meal.text[1:]] = [food.string for food in courses[counter].find_all('div', {"class" : 'item-name'})]
            counter += 1
        
        CACHE_DICTION[url] = DAY
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[url]


# In[10]:


search = "Chocolate Glazed Donuts"
start_str = "2018-04-13"
end_str = "2018-04-24"

print ("You're looking for " + search)
print ("Checking " + start_str + " to " + end_str)

# url keys
mj = "mosher-jordan"
burs = "bursley"
eq = "east-quad"
nq = "north-quad"
sq = "south-quad"
mark = "markley"

dining = [mj, burs, eq, nq, sq, mark]
location = {mj : "Mosher Jordan", burs : "Bursley", eq : "East Quad", nq : "North Quad", sq : "South Quad", mark : "Markley"}

start = datetime.strptime(start_str, "%Y-%m-%d")
end = datetime.strptime(end_str, "%Y-%m-%d")

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)
 


# In[11]:


for dt in daterange(start, end):
    for hall in dining:
        url =  "https://dining.umich.edu/menus-locations/dining-halls/" + hall + "/?menuDate=" + dt.strftime("%Y-%m-%d")
        print (url)
        menu = get_menu(url)
        for meal, dishes in menu.items():
             for dish in dishes:
                    if re.search(search, dish, re.IGNORECASE):
                        print(meal)
                        print(dish)
                        print("\n")