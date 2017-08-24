import datetime
import requests
from auth import HEADERS
# TBD: To deal with incomplete/wrong strings
import re
import unicodedata # to deal with diacritics

# We get the current year and convert it to a string so we can append it to URLs easily
season = str(datetime.datetime.now().year)

headers = HEADERS

# Key-value pairs to convert numeric dates to shortened months

MONTHS = {
1: 'Jan',
2: 'Feb',
3: 'Mar',
4: 'Apr',
5: 'May',
6: 'Jun',
7: 'Jul',
8: 'Aug', # Insert deus ex reference here
9: 'Sep',
10: 'Oct',
11: 'Nov',
12: 'Dec'
}


def get_comp(comp):

	# Find the competition to access the table details in the method
	url_season = "http://api.football-data.org/v1/competitions/?season="+season
	
	# Convert the year to a format like '2016/17' or 'yyyy/next yy'
	year = str(season) + '/' + str(int(season[2:]) + 1)

	# Append the year to the competition name
	req_comp = comp + ' ' + year

	# Use requests to get list of competitions
	try:
		competitions = requests.get(url_season, headers = headers)
	
	except requests.exceptions.RequestException as ex:
		print(ex)
		sys.exit(1)

	# .json() method converts it into a iterable list of json objects
	for competition in competitions.json():
		# If competition is in the list
		if competition["caption"] == req_comp:
			# Return the competition details		
			return competition
	# Competition was not found in list
	return -1

def get_team_comps(team):

	# Key value pairs of competitions and team ids
	comp_ids = {}
	# Find the competition to access the table details in the method
	url_season = "http://api.football-data.org/v1/competitions/?season="+season
        # Use requests to get list of competitions
	try:
		competitions = requests.get(url_season, headers = headers)
	except requests.exceptions.RequestException as ex:
		print(ex)
		sys.exit(1)
	
	for competition in competitions.json():
		comp_id = str(competition["id"])
		team_url = "http://api.football-data.org/v1/competitions/" + comp_id + "/teams/"
		try:
			team_data = requests.get(team_url, headers = headers)
		except requests.exceptions.RequestException as ex:
			print(ex)
			sys.exit(1)
		for _team in team_data.json()["teams"]:
			name = unicodedata.normalize('NFKD', _team["name"]).encode('ascii', 'ignore')
			name = str(name, 'utf-8')
			if name == team:
				comp_ids[comp_id] = _team["name"]
				comp_ids[_team["name"]] = _team["_links"]["fixtures"]["href"]

	return comp_ids

def get_comp_fixtures(comp):
	
	# If competition does not exist
	if comp == -1:
		return "Invalid competition ID or name."
	
	# API serving point for fixtures data
	url_fixtures = "http://api.football-data.org/v1/competitions/" + str(comp["id"]) +"/fixtures"

	# Get the fixtures and iterate through them, printing completed fixtures
	try:
		r = requests.get(url_fixtures, headers = HEADERS)
	
	except requests.exceptions.RequestException as ex:
		print(ex)
		sys.exit(1)

	for fixture in r.json()["fixtures"]:
		if fixture["status"] == "FINISHED":
			
			# Assign home team, away team, result and print

			home = fixture["homeTeamName"]
			away = fixture["awayTeamName"]
			h_goals = str(fixture["result"]["goalsHomeTeam"])
			a_goals = str(fixture["result"]["goalsAwayTeam"])
			print("{}  {} - {}  {}".format(home.rjust(30), h_goals.rjust(5), a_goals.ljust(5), away.ljust(30)))

		elif fixture["status"] == "SCHEDULED":

			# Assign home team, away team, date and print
			"""
			In the following lines of code starting from date = ... , what I'm doing is spliting a date string like '2018-05-02T18:45:00Z' into a list consisting of 2018-05-02 and 18:45:00Z. Then, I'm splitting the date component into 2018, 05, 02, replacing the 05 with the corresponding month abbreviation, reversing the list so that it's now 02, May, 2018, joining it as a string into '02 May 2018'. Then, in the second component, which is 18:45:00Z, I just replace the 'Z' with '' i.e nothing, then join the list when I'm printing so it's '02 May 2018 | 18:45:00'.
			"""
			home = fixture["homeTeamName"]
			away = fixture["awayTeamName"]
			date = fixture["date"].split('T')
			date[0] = date[0].split('-')
			date[0] = date[0][::-1]
			date[0][1] = MONTHS[int(date[0][1])]
			date[0] = ' '.join(date[0])
			date[1] = date[1].replace('Z','')
			date[1] = date[1][:5]
			print("{} ({}) {}".format(home.rjust(25), ' | '.join(date), away.ljust(25)))

def get_team_fixtures(team):
	pass

	
# Tests
#print(get_comp("Premier League")) # Should return PL data
#print(get_comp("Ligue")) # Should return -1
#print(get_comp("Ligue 1")) # Should return Ligue 1 data
#print(get_comp("")) # Should return -1 (duh..)

#print(get_comp_fixtures(get_comp("Premier League")))
#print(get_comp_fixtures(get_comp("Ligue#")))
#print(get_comp_fixtures(get_comp("Ligue 1")))
print(get_team_comps("Chelsea FC"))
