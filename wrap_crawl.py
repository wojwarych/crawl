import csv
from datetime import datetime as count
import re
import urllib.robotparser as robotparser
import pdb


import requests as rs
from bs4 import BeautifulSoup as bsoup


# TODO: refactor SiteInfo class -> move robot methods to TheCrawl object
# Make methods which specify usage of csv module
class SiteInfo:


    the_date = count.now()


    def __init__(self, filename):
        
        self.txt_file = filename
        self.data_from_txt = open(self.txt_file, mode = 'r')

    def create_table(self, name):
        
        self.table_name = (
            name
            + '{}'.format(self.the_date.strftime("%Y-%m"))
            + ".csv")
        self.data_table = open(self.table_name, mode = 'w')


    def write_table(self, found_data):
        
        self.data_table.write(found_data)


    @staticmethod
    def check_url(url):
        
        print("The page where crawler starts is: \n" + url + "\n")


    def check_robots(self, robots_txt):
        
        self.check_robots = robotparser.RobotFileParser()
        self.check_robots.set_url(robots_txt)
        self.check_robots.read()

    
    def close_file(self):
        
        self.data_table.close()


    def fetch_robot(self, robot_name, url):
        
        if self.check_robots.can_fetch(robot_name, url) == True:
            
            return True
        else:
            
            return False



class TheCrawl(object):


    the_agent = {
        "User-Agent" : "My_Crawler/0.1 (Windows NT 6.1)",
        "Contact" : "woj.warych@gmail.com",
        "Connection": "keep-alive"}
    the_parser = 'lxml'


    def __init__(self, url, specs):
        

        self.link_pages = []
        self.link_pages.append(url)
        self.racquet_links = []
        self.requested_data = {spec: None for spec in specs}
        self.gathered_data = []
        self.get_tree(url)


    def show_tree(self):


        '''Shows whole HTML tree of link'''
        print(self.page_tree.prettify())


    def get_tree(self, url):


        '''Create tree to parse through it''' 
        url_content = (
            rs.request('GET', url=url, headers=self.the_agent).content)
        self.page_tree = bsoup(url_content, self.the_parser)


    def get_links(self, link, *args, **kwargs):


        '''Get all links of all raquets on the page'''
        return link.find_all(*args, **kwargs)


    def is_next_page(self):


        '''Check if current self.page_tree has its successor'''
        link = self.page_tree.find(class_="pagination").li
        if link.a.get('title') == "Następna Strona":
            return True

        else:
            for l in link.next_siblings:
                if l.__class__.__name__ == "NavigableString" or l.a.get('title') == "Poprzednia Strona":
                    pass
                else:
                    if l.a.get('title') == "Następna Strona":
                        return True
                    return False


    def get_link_next(self):


        '''Catches link for page which is next after current self.page_tree'''
        if self.is_next_page():
            link = self.page_tree.find(class_='pagination').li

            if link.a.get('href') not in self.link_pages:
                self.link_pages.append(link.a.get('href'))
            else:
                iter_link_sibs = link.next_siblings
                for l in iter_link_sibs:
                    if l.__class__.__name__ == 'NavigableString' or l.a.get('href') in self.link_pages:
                        pass
                    else:
                        self.link_pages.append(l.a.get('href'))

            return self.link_pages
        
        else:
            return self.is_next_page()
        

    def set_link_next(self):


        '''Sets new self.page_tree which is latest catched url from get_link_next method'''
        self.get_tree(self.link_pages[-1])


    def get_racquet_hrefs(self, racquets_tags):


        '''Get proper urls from html tags from list w tags'''
        racqs_hrefs = self.flat_list(racquets_tags)
        self.racquet_links = [tag.get('href') for tag in racqs_hrefs]


    def flat_list(self, racquets_tags):


        '''Collected anchor tags from pages are list of lists (1 list - one page)
        Flatten list for further ease of use'''
        racquets_tags = [tag for page_tag in racquets_tags for tag in page_tag]
        return racquets_tags


    def get_price(self, *args, **kwargs):


        return self.page_tree.find(*args, **kwargs).get_text().strip()


    def get_content(self, properties):


        '''Gets the content from the table specs in the racquet link'''
        table_tag_list = self.get_table_tags()

        for tag in table_tag_list:
            stripped_tag = tag.get_text().strip()
            if stripped_tag in properties.keys():
                properties[stripped_tag] = (
                    tag.next_sibling.get_text().strip())

        self._check_for_nas(properties)


    def _check_for_nas(self, data):


        for key in data.keys():
            if data[key] is None:
                data[key] = 'NA'


    def set_gathered_data(self, data, price):


        data = list(data.values())
        data.append(price)
        self.gathered_data.append(data)


    def get_table_tags(self):


        return self.page_tree.table.find_all('td')