from datetime import datetime as count
import re
import urllib.robotparser as robotparser

import requests as rs
from bs4 import BeautifulSoup as bsoup



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

class TheCrawl(object):


	the_agent = {
		"User-Agent" : "My_Crawler/0.1 (Windows NT 6.1)",
		"Contact" : "woj.warych@gmail.com",
		"Connection": "keep-alive"}
	the_parser = 'xml'


	def __init__(self, url):
		
		self.paginated_items = []
		self.paginated_items.append(url)

		self.get_tree(url)


	def show_tree(self):

		'''Shows tree of the link'''
		print(self.page_tree.prettify())


	def get_tree(self, url):


		print(url)
		url_content = (
			rs.request('GET', url=url, headers=self.the_agent).content)
		self.page_tree = bsoup(url_content, self.the_parser)


	def get_links(self, *args, **kwargs):

		'''Get all links of all raquets on the page'''

		requested_links = self.page_tree.find_all(*args, **kwargs)
		return requested_links


	def is_next_page(self):

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
					
					else:
						return False

		
		'''for l in link.next_siblings:
			
			print(l)
			if l.__class__.__name__ == "NavigableString" or l.a.get('title') == "Poprzednia Strona":
				pass
			
			else:
				if l.a.get('title') == "Następna Strona":
					print(l.a.get('href'))
					return True
				
				else:
					return False'''

		#if link.get('title') == "Następna Strona":
		#	return True
		#else:
		#	return False


	def get_link_next(self):

		if self.is_next_page():

			link = self.page_tree.find(class_='pagination').li

			if link.a.get('href'):

				self.paginated_items.append(link.a.get('href'))

			else:

				for l in link.next_siblings:

					if l.__class__.__name__ == 'NavigableString' or l.a.get('href') in self.paginated_items:
						pass
					else:
						self.paginated_items.append(l.a.get('href'))

			return self.paginated_items
		
		else:
			return self.is_next_page()
		

	def set_link_next(self):

		self.get_tree(self.paginated_items[-1])

	"""def get_content(self, SiteInfo):

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
			self.reformatted.append(string)"""


if __name__ == "__main__":


	start_url = 'https://strefatenisa.com.pl/rakiety-tenisowe/rakiety-seniorskie/page=1'
	tennis_data = TheCrawl(start_url)

	links = tennis_data.get_link_next()

	tennis_data.set_link_next()

	tennis_data.get_link_next()