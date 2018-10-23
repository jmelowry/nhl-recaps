#!/usr/bin/env python

""""Gets a list of recent game recaps"""

import os
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pprint
from bs4 import BeautifulSoup
import dateparser
import abbreviations

class NhlRecaps:
    """gets a list of games, and recaps the game"""

    def __init__(self):
        pp = pprint.PrettyPrinter(indent=4)
        soup = self.make_soup()
        self.video_descriptions = self.get_video_descriptions(soup)
        self.video_urls = self.get_video_urls(soup)
        self.game_recaps = self.combine_data(self.video_descriptions,self.video_urls)
        self.total_results = self.get_total_results(soup).text
        

    def make_soup(self):
        """loads the recaps page, and creates bs4 soup"""
        service = webdriver.chrome.service.Service(
            '/usr/local/bin/chromedriver')
        service.start()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        driver = webdriver.Remote(
            service.service_url, desired_capabilities=chrome_options.to_capabilities())

        recap_url = 'https://www.nhl.com/video/search/content/gameRecap'

        driver.get(recap_url)
        inner_html = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(inner_html, 'html.parser')

        return soup

    def get_total_results(self,soup):

        return soup.find('span', {'class': 'video-search__results__total'})

    def get_video_descriptions(self, soup):
        """get descriptions"""
        descriptions = []
        for meta in soup.find_all('div', {'class': 'video-preview__meta-info'}):
            descriptions.append(meta.text.strip().lstrip())

        return descriptions

    def get_video_urls(self, soup):
        """get video urls"""
        urls = []
        base_url = 'https://www.nhl.com'
        for link in soup.find_all('a'):
            content = link.get('href')
            if '/video/recap-' in content:
                full_url = base_url + content
                urls.append(full_url)

        return urls

    def analyze_url(self, url):
        """gets some data based on a video url"""
        split = url.split('-')

        # in case the team isn't found in translate function
        try:
            home_team = abbreviations.translate_code(split[1])
        except:
            home_team = split[1]
        try:
            away_team = abbreviations.translate_code(split[3])
        except:
            away_team = split[3]
        score = split[2] + '-' + split[4].split('/')[0]

        return home_team, away_team, score

    def analyze_date(self, video_description):
        """returns date, based on video description"""
        raw_date = video_description.strip().split('•')[-1].lstrip()

        return dateparser.parse(raw_date)

    def analyze_description(self, video_description):
        """returns video description + video length"""
        return video_description.strip().split('•')[0].lstrip()

    def combine_data(self, video_descriptions, video_urls):
        """creates dictionary of game, teams, score, url"""
        combined_data = []
        for item in video_descriptions:
            game_date = self.analyze_date(item).strftime("%m/%d/%Y")
            game_description = self.analyze_description(item).replace('\"', '').strip()
            url = video_urls[video_descriptions.index(item)]
            home_team = self.analyze_url(url)[0]
            away_team = self.analyze_url(url)[1]
            game_score = self.analyze_url(url)[2]
            combined_data.append([game_date, home_team, away_team, game_description, game_score, url])

        return combined_data


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    games = NhlRecaps()
    pp.pprint(games.game_recaps)
    pp.pprint(games.total_results)
