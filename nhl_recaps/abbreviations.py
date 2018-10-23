#!/usr/bin/env python

"""parses team codes and names from list"""

# source: https://en.wikipedia.org/wiki/Template:NHL_team_abbreviations

TEAM_CODES = """AFM – Atlanta Flames
ANA – Anaheim Ducks
ARI – Arizona Coyotes
ATL – Atlanta Thrashers
BOS – Boston Bruins
BRK – Brooklyn Americans
BUF – Buffalo Sabres
CAR – Carolina Hurricanes
CGS – California Golden Seals
CGY – Calgary Flames
CHI – Chicago Blackhawks
CBJ – Columbus Blue Jackets
CLE – Cleveland Barons
CLR – Colorado Rockies
COL – Colorado Avalanche
DAL – Dallas Stars
DFL – Detroit Falcons
DCG – Detroit Cougars
DET – Detroit Red Wings
EDM – Edmonton Oilers
FLA – Florida Panthers
HAM – Hamilton Tigers
HFD – Hartford Whalers
KCS – Kansas City Scouts
LAK – Los Angeles Kings
MIN – Minnesota Wild
MMR – Montreal Maroons
MNS – Minnesota North Stars
MTL – Montreal Canadiens
MWN – Montreal Wanderers
NSH – Nashville Predators
NJD – New Jersey Devils
NYA – New York Americans
NYI – New York Islanders
NYR – New York Rangers
OAK – Oakland Seals
OTT – Ottawa Senators
PHI – Philadelphia Flyers
PHX – Phoenix Coyotes
PIR – Pittsburgh Pirates
PIT – Pittsburgh Penguins
QUA – Philadelphia Quakers
QUE – Quebec Nordiques
QBD – Quebec Bulldogs
SEN – Ottawa Senators (original)
SJS – San Jose Sharks
SLE – St. Louis Eagles
STL – St. Louis Blues
TAN – Toronto Arenas
TBL – Tampa Bay Lightning
TOR – Toronto Maple Leafs
TSP – Toronto St. Patricks
VAN – Vancouver Canucks
VGK – Vegas Golden Knights
WIN – Winnipeg Jets (original)
WPG – Winnipeg Jets
WSH – Washington Capitals"""

def team_codes():
    teams = {}
    for item in TEAM_CODES.split('\n'):
        team_code = item.split('–')[0].strip()
        team_name = item.split('–')[1].lstrip()

        teams.update({team_code: team_name})

    return teams

def translate_code(team_code):
    all_teams = team_codes()

    return all_teams[team_code.upper()]



if __name__ == '__main__':
    #team_codes()
    print(translate_code('ana'))
