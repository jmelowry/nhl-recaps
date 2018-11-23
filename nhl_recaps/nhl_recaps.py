#!/usr/bin/env python

""""Gets a list of recent game recaps"""

import os
import sys
import logging
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

        # use premade_soup function for testing. (does not make api call)
        soup = self.make_soup()
        #soup = self.premade_soup()

        self.video_descriptions = self.get_video_descriptions(soup)
        self.video_urls = self.get_video_urls(soup)
        self.game_recaps = self.combine_data(self.video_descriptions,self.video_urls)
        self.page_results = self.get_page_results(soup)
        self.total_results = self.get_total_results(soup)


    def make_soup(self):
        """loads the recaps page, and creates bs4 soup"""
        def scroll(direction):
            """does some scrolling to get the full page. directions can be up/down"""
            if direction.upper() == 'UP':
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            elif direction.upper() == 'DOWN':
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.END)
            else:
                logging.error('unrecognized scroll direction entered')

        service = webdriver.chrome.service.Service(
            '/usr/local/bin/chromedriver')
        service.start()
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        driver = webdriver.Remote(
            service.service_url, desired_capabilities=chrome_options.to_capabilities())

        recap_url = 'https://www.nhl.com/video/search/content/gameRecap'

        driver.get(recap_url)



        inner_html = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(inner_html, 'html.parser')

        page_results = self.get_page_results(soup)
        print(page_results)
        total_results = self.get_total_results(soup)
        print(total_results)

        # while True:
        #     print(len(page_results))
        #     len(page_results) >= 30
        #     time.sleep(5)
        #     scroll('down')
        #     time.sleep(5)
        #     scroll('up')


        # f = open('output.html','w')
        # f.write(inner_html)
        # f.close()



        return soup

    def premade_soup(self):
        """used for testing. Grabs soup.html from local path"""

        inner_html = open('soup.html', 'r')

        soup = BeautifulSoup(inner_html, 'html.parser')

        return soup


    def get_total_results(self,soup):
        """gets total results"""

        return soup.find('span', {'class': 'video-search__results__total'}).text

    def get_page_results(self,soup):
        """gets the number of results on page"""

        return soup.find('span', {'class': 'video-search__results__from'}).text

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
            combined_data.append([game_date,
                                  home_team,
                                  away_team,
                                  game_description,
                                  game_score,
                                  url])


        return combined_data

    # def write_soup_file(self, soup):
    #     f = open('output.html','wb')
    #     f.write(soup.prettify("utf-8"))
    #     f.close()
    #     print('soup saved as output.html')


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    games = NhlRecaps()
    pp.pprint(games.game_recaps)
    #print(len(games.game_recaps))
    pp.pprint(games.page_results)
    pp.pprint(games.total_results)
