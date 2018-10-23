#!/usr/bin/env python

""""Gets a list of recent game recaps"""

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import dateparser
import abbreviations

def make_soup():
    """loads the recaps page, and creates bs4 soup"""
    service = webdriver.chrome.service.Service('/usr/local/bin/chromedriver')
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


def get_video_descriptions(soup):
    """get descriptions"""
    descriptions = []
    for meta in soup.find_all('div', {'class': 'video-preview__meta-info'}):
        descriptions.append(meta)
        print(meta.text)

    return descriptions


def get_video_urls(soup):
    """get video urls"""
    urls = []
    base_url = 'https://www.nhl.com'
    for link in soup.find_all('a'):
        content = link.get('href')
        if '/video/recap-' in content:
            full_url = base_url + content
            urls.append(full_url)
            #urls.append(analyze_url(base_url + content))
            print(base_url + content)

    return urls


def analyze_url(url):
    """gets some data based on a video url"""
    split = url.split('-')
    home_team = abbreviations.translate_code(split[1])
    away_team = abbreviations.translate_code(split[3])
    score = split[2] + '-' + split[4].split('/')[0]

    return home_team, away_team, score

def analyze_date(video_description):
    """returns date, based on video description"""
    raw_date = video_description.strip().split('•')[-1].lstrip()

    return dateparser.parse(raw_date)

def analyze_description(video_description):
    """returns video description + video length"""
    return video_description.strip().split('•')[0].lstrip()


if __name__ == '__main__':
    #SOUP = make_soup()
    #print(len(get_video_descriptions(SOUP)))
    #print(len(get_video_urls(SOUP)))
    print(analyze_url('https://www.nhl.com/video/recap-stl-4-tor-1/c-62039403?tag=content&tagValue=gameRecap'))
    print(analyze_date('Ovechkin powers Caps past Canucks with four points  03:43 • Oct 22, 2018'))
    print(analyze_description('Ovechkin powers Caps past Canucks with four points  03:43 • Oct 22, 2018'))
