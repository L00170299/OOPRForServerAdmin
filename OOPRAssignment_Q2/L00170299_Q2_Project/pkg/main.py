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


def get_soup_response(url):
    """
        This function gets a url and returns html parsed response using requests & BeautifulSoup4 modules
        Parameters:
            url        Web page link to get content
        Returns:
            String     HTML parsed contend of requested website
    """
    raw_page = requests.get(url)
    soup_page = BeautifulSoup(raw_page.content, "html.parser")

    return soup_page


def get_pretty_response(soup_page, formatter="minimal"):
    """
        This function gets a parsed content of a website and it returns formatted string
        Parameters:
            soup_page   HTML parsed content
            formatter   Formatter type to prettify response. Available: minimal, html, html5, None. Default: minimal
        Returns:
            String     Prettified response from requested url
    """
    pretty_page = soup_page.prettify(formatter=formatter)

    return pretty_page


def get_entities(soup_page, entity_type):
    """
        This function returns values or text from html objects depending of entity type requested
        Parameters:
            soup_page       HTML parsed content
        Returns:
            String/List     Depends what is asked to get it could be a single text value or a list
    """
    # Options available could be amended according to needs
    if entity_type == "link":
        # if links requested, we build list and append them in a list
        link_list = []
        for link in soup_page.find_all('a'):
            link_list.append(link.get("href"))
        return link_list
    elif entity_type == "title":
        # if title requested but page doesn't have one, then return empty
        if soup_page.title:
            return soup_page.title.string

    # If not in available options then returns empty rather than fail
    return


def contains_text(soup_page, text):
    """
        This function returns true of false depending if it find text into page content
        Parameters:
            soup_page       HTML parsed content
            text            text to search
        Returns:
            Bool            true or false
    """
    pretty_page = get_pretty_response(soup_page)
    return text in pretty_page


if __name__ == '__main__':
    """
        Main method of application      
        Parameters:
            none      
        Returns:
            none
    """

    # List with webpages to scrape
    url_list = ["http://192.168.0.222/", "http://192.168.0.222:8080/login",
                "https://lyitbb.blackboard.com/"]
    text_list = ["Fedora Webserver Test Page", "Welcome to Jenkins!", "contact the helpdesk on 0749186050"]

    # we will scrape each page and store some info from each to use it after
    for url_path in url_list:
        # get content of website
        soup_page = get_soup_response(url_path)

        print(f"Link: {url_path}")

        # from here we can do whatever we want with it
        # For example find title
        print(f"Title: {get_entities(soup_page, 'title')}")

        # Or get list of links that appear in website
        links = get_entities(soup_page, "link")
        if len(links) > 0:
            print(f"Links: {links}")
        else:
            print("Links: None")

        # Or find out if it contains some text
        for text in text_list:
            print(f"Contains '{text}': {contains_text(soup_page, text)}")

        # This is just to have some separation in the output
        print("=" * 50)



