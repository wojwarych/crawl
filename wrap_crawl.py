import requests as rs
from bs4 import BeautifulSoup as bsoup
import re
from datetime import datetime as count
import urllib.robotparser as robotparser



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

#######################################################################################################################

class TheCrawl:


	the_agent = {
		"User-Agent" : "My_Crawler/0.1 (Windows NT 6.1)",
		"Contact" : "woj.warych@gmail.com"}
	the_parser = 'html.parser'


	def __init__(self, url):
		

		self.links = []
		self.detail_soup = []
		self.container = []
		self.reformatted = []
		self.text = ""
		self.text_insert = []
		self.product_spec = []
		self.url = url
		crawl = rs.request('GET', url = self.url, headers = self.the_agent)
		self.soup = bsoup(crawl.content, self.the_parser)


	def show_tree(self):

		
		'''Shows tree of the link'''

		print(self.soup.prettify())


	def get_link(self, key, *args, **kwargs):


		'''Gets the data from selected link'''

		for link in self.soup.find_all(*args, **kwargs):
			
			link = link.get(key)
			self.links.append(link)

	def get_content(self, SiteInfo):


		'''Gets the soup from selected link'''

		for cont, _ in enumerate(self.links):
			
			next_link = self.links[cont]

			if SiteInfo.check_robots.can_fetch('*', next_link) == True:

				new_link = rs.get(url = next_link)
				self.detail_soup.append(bsoup(new_link.content,
											  self.the_parser))
			else:
				pass


	def get_details(self, *args, **kwargs):


		'''Gets detailed content from the link'''

		for det, _ in enumerate(self.detail_soup):

			parse_text = self.detail_soup[det]

			for cont in parse_text.find_all(*args, **kwargs):
				self.container.append(cont)
				

	def insert_to_reformat(self, clean, replacer, position, *args, **kwargs):


		'''Insert the data to self.container if forgotten'''

		for det, _ in enumerate(self.detail_soup):

			parse_text = self.detail_soup[det]

			for cont in parse_text.find_all(*args, **kwargs):

				cont = cont.get_text(" ", strip = True)
				cont = cont.replace(clean, replacer)
				self.text_insert.append(cont)

		for iteration, _ in enumerate(self.text_insert):

			self.reformatted.insert(position, self.text_insert[iteration])
			self.reformatted[position - 1:position + 1] = (
				[' '.join(self.reformatted[position - 1:position + 1])])
			position += 1


	def add_by_regex(self, expression, num, delimiter):

		'''Put to string text from self.reformatted list or NAs if not found'''

		if re.search(expression, self.reformatted[num]):
			
			self.text += (
				(re.search(expression, self.reformatted[num]).group(1))
				+ delimiter)
		else:
			
			self.text += ("NA" + delimiter)


	def clear_text(self):

		self.text = ""
	

	def reformat(self, clean, replacer):


		'''Reformats html body to text'''

		for body, _ in enumerate(self.container):
			string = self.container[body]
			string = string.get_text(" ", strip = True)
			string = string.replace(clean, replacer)
			self.reformatted.append(string)