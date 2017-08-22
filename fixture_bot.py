import datetime
import requests
from auth import HEADERS
# TBD: To deal with incomplete/wrong strings
import re

# We get the current year and convert it to a string so we can append it to URLs easily
season = str(datetime.datetime.now().year)

# Find the competition to access the table details in the method
url_season = "http://api.football-data.org/v1/competitions/?season="+season

headers = HEADERS

def get_comp(comp):
	
	# Convert the year to a format like '2016/17' or 'yyyy/next yy'
	year = str(season) + '/' + str(int(season[2:]) + 1)

	# Append the year to the competition name
	req_comp = comp + ' ' + year

	# Use requests to get list of competitions
	competitions = requests.get(url_season, headers = headers)

	# .json() method converts it into a iterable list of json objects
	for competition in competitions.json():
		# If competition is in the list
		if competition["caption"] == req_comp:
			# Return the competition details
			return competition
	# Competition was not found in list
	return -1
	
def get_comp_fixtures(comp):
	
	# If competition does not exist
	if comp == -1:
		return "Invalid competition ID or name."
	
	# API serving point for fixtures data
	url_fixtures = "http://api.football-data.org/v1/competitions/" + str(comp["id"]) +"/fixtures"

	# Get the fixtures and iterate through them, printing completed fixtures
	r = requests.get(url_fixtures, headers = HEADERS)
	for fixture in r.json()["fixtures"]:
		if fixture["status"] == "FINISHED":
			
			# Assign home team, away team, result and print

			home = fixture["homeTeamName"]
			away = fixture["awayTeamName"]
			h_goals = str(fixture["result"]["goalsHomeTeam"])
			a_goals = str(fixture["result"]["goalsAwayTeam"])
			print("{}  {} - {}  {}".format(home.rjust(30), h_goals, a_goals, away.ljust(30)))
	
# Tests
#print(get_comp("Premier League")) # Should return PL data
#print(get_comp("Ligue")) # Should return -1
#print(get_comp("Ligue 1")) # Should return Ligue 1 data
#print(get_comp("")) # Should return -1 (duh..)

print(get_comp_fixtures(get_comp("Premier League")))
print(get_comp_fixtures(get_comp("Ligue")))
print(get_comp_fixtures(get_comp("Ligue 1")))
