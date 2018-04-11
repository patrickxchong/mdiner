## proj_nps.py
## Skeleton for Project 2, Winter 2018
## ~~~ modify this file, but don't rename it ~~~
import requests
import json
from bs4 import BeautifulSoup
import secrets
from requests_oauthlib import OAuth1
import codecs
import sys

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
CACHE_FNAME = 'national_sites.json'
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

consumer_key = secrets.twitter_api_key
consumer_secret = secrets.twitter_api_secret
access_token = secrets.twitter_access_token
access_secret = secrets.twitter_access_token_secret

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)

CACHE_FNAME2 = 'twitter_cache.json'
try:
    cache_file2 = open(CACHE_FNAME2, 'r')
    cache_contents2 = cache_file2.read()
    CACHE_DICTION2 = json.loads(cache_contents2)
    cache_file2.close()

except:
    CACHE_DICTION2 = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_twitter_request_using_cache(baseurl, params):
    unique_ident2 = params_unique_combination(baseurl,params)

    if unique_ident2 in CACHE_DICTION2:
        print("Getting cached data...")
        return CACHE_DICTION2[unique_ident2]

    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params, auth=auth)
        CACHE_DICTION2[unique_ident2] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION2)
        fw = open(CACHE_FNAME2,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION2[unique_ident2]

class NationalSite:
    def __init__(self, type1=None, name=None, desc=None, url=None, street='123 Main St.', city='Smallville', state='KS', zipcode='11111'):
        self.type = type1
        self.name = name
        self.description = desc
        self.url = url
        self.address_street = street
        self.address_city = city
        self.address_state = state
        self.address_zip = zipcode

    def __str__(self):
        return str(self.name) + ' (' + str(self.type) + '): ' + str(self.address_street) + ', ' + str(self.address_city) + ', ' + str(self.address_state) + ' ' + str(self.address_zip)

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class Tweet:
    def __init__(self, text, user, date, retweets, favorites, popscore, id_):
        self.text = text
        self.username = user
        self.creation_date = date
        self.num_retweets = retweets
        self.num_favorites = favorites
        self.popularity_score = popscore
        self.id = id_

    def __str__(self):
        return '@' + str(self.username) +': ' + str(self.text) + '\n[retweeted ' + str(self.num_retweets) + ' times]\n' + '[favorited ' + str(self.num_favorites) + ' times]\n' + '[popularity ' + str(self.popularity_score) +']\n[tweeted on ' + str(self.creation_date) + '] | [id: ' + str(self.id) + ' ]'


## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov

def get_sites_for_state(state_abbr):
    baseurl = 'https://www.nps.gov'
    catalog_url = baseurl + '/state/'+ state_abbr
    page_text = make_request_using_cache(catalog_url)
    page_soup = BeautifulSoup(page_text,'html.parser')

    content_div = page_soup.find(id='list_parks')
    site_type = content_div.find_all('h2')
    sites_name_list = []
    sites_type_list = []
    sites_street_list = []
    sites_city_list = []
    sites_state_list = []
    sites_zip_list = []
    site_name = content_div.find_all('h3')
    length = 0
    for v in site_name:
        length += 1
        name = v.text
        sites_name_list.append(name)
    for x in site_type:
        t = x.text
        sites_type_list.append(t)



    site_address = []
    for link in content_div.find_all('a'):
        if 'www' not in link.get('href'):
            page_url = link.get('href')
            # print(NationalSite.url)
            url_address = baseurl + page_url + 'planyourvisit/basicinfo.htm'
            pg_txt = make_request_using_cache(url_address)
            pg_soup = BeautifulSoup(pg_txt,'html.parser')

            try:
                address_div = pg_soup.find(class_="physical-address")
                street = address_div.find(itemprop='streetAddress').text.strip()
                sites_street_list.append(street)
                city = address_div.find(itemprop='addressLocality').text.strip()
                sites_city_list.append(city)
                state = address_div.find(itemprop='addressRegion').text.strip()
                sites_state_list.append(state)
                zipcode = zipcode=address_div.find(itemprop='postalCode').text.strip()
                sites_zip_list.append(zipcode)
            except:
                address_span = pg_soup.find(class_='mailing-address')
                try:
                    street = address_span.find(itemprop='streetAddress').text.strip()
                    sites_street_list.append(street)
                    city = address_span.find(itemprop='addressLocality').text.strip()
                    sites_city_list.append(city)
                    state = address_span.find(itemprop='addressRegion').text.strip()
                    sites_state_list.append(state)
                    zipcode = address_span.find(itemprop='postalCode').text.strip()
                    sites_zip_list.append(zipcode)

                except:
                    street = address_span.find(itemprop='postOfficeBoxNumber').text.strip()
                    sites_street_list.append(street)
                    city = address_span.find(itemprop='addressLocality').text.strip()
                    sites_city_list.append(city)
                    state = address_span.find(itemprop='addressRegion').text.strip()
                    sites_state_list.append(state)
                    zipcode = address_span.find(itemprop='postalCode').text.strip()
                    sites_zip_list.append(zipcode)

    lst = []
    for i in range(length):
        obj = NationalSite(name=sites_name_list[i], type1=sites_type_list[i], street=sites_street_list[i], city=sites_city_list[i], state=sites_state_list[i], zipcode=sites_zip_list[i])
        lst.append(obj)
        # print(i+1, obj)
    return lst

## Must return the list of NearbyPlaces for the specified NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list

def get_nearby_places_for_site(site_object):
    google_api = secrets.google_places_key
    name = site_object.name
    type_= site_object.type
    query = name + " "+ type_
    text_baseurl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}'.format(query, google_api)
    data = json.loads(make_request_using_cache(text_baseurl))
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    location = str(lat) + ',' + str(lng)
    places_baseurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={}&radius=10000'.format(google_api, location)
    results = json.loads(make_request_using_cache(places_baseurl))
    nearbyplaces_list = []
    for n in results['results']:
        objects = NearbyPlace(name=n['name'])
        nearbyplaces_list.append(objects)
    return nearbyplaces_list

# print(get_nearby_places_for_site(get_sites_for_state('ca')[6]))

## Must return the list of Tweets that mention the specified NationalSite
## param: a NationalSite object
## returns: a list of up to 10 Tweets, in descending order of "popularity"



def get_tweets_for_site(site_object):
    name = site_object.name
    type_= site_object.type
    query = name + ' ' + type_
    baseurl = 'https://api.twitter.com/1.1/search/tweets.json'
    params = {'q':query,'count':'50'}
    r = make_twitter_request_using_cache(baseurl, params)
    tweets = r['statuses']
    tweets_list = []
    for t in tweets:
        if 'RT @' not in t['text']:
            text = t['text']
            username = t['user']['screen_name']
            creation_date = t['created_at']
            num_retweets = t['retweet_count']
            num_favorites = t['favorite_count']
            id_ = t['id_str']
            popularity_score = int(num_retweets)*2 + int(num_favorites)*3
            tweetobj = Tweet(text,username,creation_date,num_retweets,num_favorites, popularity_score, id_)
            tweets_list.append(tweetobj)

    newlist = sorted(tweets_list, key=lambda k: k.popularity_score, reverse=True)
    return newlist[0:10]


state_abbr_dict = {
        'ak': 'Alaska',
        'al': 'Alabama',
        'ar': 'Arkansas',
        'as': 'American Samoa',
        'az': 'Arizona',
        'ca': 'California',
        'co': 'Colorado',
        'ct': 'Connecticut',
        'dc': 'District of Columbia',
        'de': 'Delaware',
        'fl': 'Florida',
        'ga': 'Georgia',
        'gu': 'Guam',
        'hi': 'Hawaii',
        'ia': 'Iowa',
        'id': 'Idaho',
        'il': 'Illinois',
        'in': 'Indiana',
        'ks': 'Kansas',
        'ky': 'Kentucky',
        'la': 'Louisiana',
        'ma': 'Massachusetts',
        'md': 'Maryland',
        'me': 'Maine',
        'mi': 'Michigan',
        'mn': 'Minnesota',
        'mo': 'Missouri',
        'mp': 'Northern Mariana Islands',
        'ms': 'Mississippi',
        'mt': 'Montana',
        'na': 'National',
        'nc': 'North Carolina',
        'nd': 'North Dakota',
        'ne': 'Nebraska',
        'nh': 'New Hampshire',
        'nj': 'New Jersey',
        'nm': 'New Mexico',
        'nv': 'Nevada',
        'ny': 'New York',
        'oh': 'Ohio',
        'ok': 'Oklahoma',
        'or': 'Oregon',
        'pa': 'Pennsylvania',
        'pr': 'Puerto Rico',
        'ri': 'Rhode Island',
        'sc': 'South Carolina',
        'sd': 'South Dakota',
        'tn': 'Tennessee',
        'tx': 'Texas',
        'ut': 'Utah',
        'va': 'Virginia',
        'vi': 'Virgin Islands',
        'vt': 'Vermont',
        'wa': 'Washington',
        'wi': 'Wisconsin',
        'wv': 'West Virginia',
        'wy': 'Wyoming'
}

if __name__ == '__main__':
    input_ = input('Enter command (or "help" for options): ')
    while True:
        if input_ == 'help':
            print('list <stateabbr>\n'
               '\tavailable anytime\n'
               '\tlists all National Sites in a state\n'
               '\tvalid inputs: a two-letter state abbreviation\n'
           'nearby <result_number>\n'
              '\tavailable only if there is an active result set\n'
              '\tlists all Places nearby a given result\n'
               '\tvalid inputs: an integer 1-len(result_set_size)\n'
           'tweets <result_number>\n'
                '\tavailable only if there is an active results set\n'
                '\nlists up to 10 most "popular" tweets that mention the selected Site\n'
      'exit\n'
               '\texits the program\n'
      'help\n'
               '\tlists available commands (these instructions)')
            input_ = input('Enter command (or "help" for options): ')

        if input_ == 'exit':
            print('Bye!')
            break

        if 'list' in input_:
            state_abbr = input_[-2:]
            global sites
            sites = get_sites_for_state(state_abbr)
            num = 0
            print('National Sites in ' + str(state_abbr_dict[state_abbr]) +'\n')
            for x in sites:
                num += 1
                print (str(num) + ' ' + str(x))
            input_ = input('Enter command (or "help" for options): ')

        if 'nearby' in input_:
            index = int(input_.split(' ')[1])
            place = sites[index-1]
            nearbysites = get_nearby_places_for_site(place)
            no = 0
            print('Places near ' + str(place.name) +' ' + str(place.type) +'\n')
            for n in nearbysites:
                no += 1
                print(str(no) + ' ' + str(n))
            input_ = input('Enter command (or "help" for options): ')

        if 'tweets' in input_:
            ind = int(input_.split(' ')[1])
            plc = sites[ind-1]
            tweet = get_tweets_for_site(plc)
            for t in tweet:
                print(t)
                print('-------------------------------------------')
            input_ = input('Enter command (or "help" for options): ')

        else:
            input_ = input('Sorry, please insert a valid input, or key in "help" for options: ')
