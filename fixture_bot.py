import datetime
import requests

# TBD: To deal with incomplete/wrong strings
import re

# We get the current year and convert it to a string so we can append it to URLs easily
season = str(datetime.datetime.now().year)

# Find the competition to access the table details in the method
url_season = "http://api.football-data.org/v1/competitions/?season="+season

# headers = { 'X-Auth-Token': ADD YOUR KEY ENCLOSED WITH QUOTES HERE }

def get_comp(comp):
	
	# Convert the year to a format like '2016/17' or 'yyyy/next yy'
	year = str(season) + '/' + str(int(season[2:]) + 1)

	# Append the year to the competition name
	req_comp = comp + ' ' + year

	# Use requests to get list of competitions
	# competitions = requests.get(url_season, headers = headers)
	competitions = requests.get(url_season)
	# .json() method converts it into a iterable list of json objects
	for competition in competitions.json():
		# If competition is in the list
		if competition["caption"] == req_comp:
			# Return the competition details
			return competition
	# Competition was not found in list
	return -1
	

# Tests
print(get_comp("Premier League")) # Should return PL data
print(get_comp("Ligue")) # Should return -1
print(get_comp("Ligue 1")) # Should return Ligue 1 data
print(get_comp("")) # Should return -1 (duh..)
