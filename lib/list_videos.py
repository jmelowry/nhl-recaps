#!/usr/bin/env python

""""Gets a list of recent game recaps"""

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


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


def get_descriptions(soup):
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
            urls.append(base_url + content)
            print(base_url + content)

    return urls


def analyze_url(url):
    """gets some data based on a video url"""
    split = url.split('-')
    home_team = split[1]
    away_team = split[3]
    score = split[2] + '-' + split[4].split('/')[0]

    return home_team, away_team, score


if __name__ == '__main__':
    SOUP = make_soup()
    print(len(get_descriptions(SOUP)))
    print(len(get_video_urls(SOUP)))
