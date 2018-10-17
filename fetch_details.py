import requests
import json
from bs4 import BeautifulSoup
import datetime


# Get IMDB id for the show
def getImdbID(show_name):
	url = "http://www.omdbapi.com/"
	querystring = {"t":"\"%s\"" %(show_name),"apikey":"12fa2ce0"}
	response = requests.request("GET", url, params=querystring)
	return json.loads(response.text)["imdbID"]


# Get url for page displaying the list of episodes for the latest season
def getSeasonLink(show_name):
	imdb_id = getImdbID(show_name)
	show_url = "https://www.imdb.com/title/%s/" %(imdb_id)
	response = requests.request("GET", show_url)
	bs4_obj = BeautifulSoup(response.text, 'html.parser')
	episode_tab = bs4_obj.find_all('div', class_ = 'seasons-and-year-nav')
	return "https://www.imdb.com" + episode_tab[0].a["href"]

# Get status of the show
def getShowStatus(show_name):
	url = getSeasonLink(show_name)
	response = requests.request("GET", url)
	bs4_obj = BeautifulSoup(response.text, 'html.parser')
	episode_dates = bs4_obj.find_all('div', class_ = 'airdate')

	future = False

	count = 0
	for i in episode_dates:
		air_date = i.contents[0].strip()
		
		try:
			air_date = datetime.datetime.strptime(air_date, '%d %b. %Y')
			count +=1
			if air_date > datetime.datetime.now():
				status = "The next episode airs on %s." %(air_date.strftime("%d %m %Y"))
				future = True
				break
			
			continue
		except ValueError:
			pass

		try:
			air_date = datetime.datetime.strptime(air_date, '%Y')
			count +=1
			if air_date > datetime.datetime.now():
				status = "The next season begins in %s" %(air_date.strftime("%Y"))
				future = True
				break
			
			continue
		except ValueError:
			pass
	
	

	if future == False:
		status = "The show has finished streaming all its episodes or no future information is available on IMDb."

	return status

