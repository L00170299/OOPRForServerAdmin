"""
#
# File          : main.py
# Created       : 30/11/2021 21:54
# Author        : Luis Gonzalez (L00170299)
# Version       : v1.0.0
# Licencing     : (C) 2021 Luis Gonzalez
                  Available under GNU Public License (GPL)
# Description   : This script request content from a website and uses BeautifulSoup to scrape data from it
# 
"""

from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    """
        Main method of application      
        Parameters:
            none      
        Returns:
            none
    """

    url_path = "http://192.168.0.222/"              # variable with webpage to scrape
    page = requests.get(url_path)                   # it has the raw content of webpage
    soup_page = BeautifulSoup(page.content, "html.parser")

    print(soup_page.find_all('a').get('href'))
    # print(soup_page.prettify(formatter="minimal").a)
