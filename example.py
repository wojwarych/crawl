from wrap_crawl import SiteInfo, TheCrawl


if __name__ == "__main__":

	#Set the crawler - starting point, robots.txt
	#file to write down to it, headers
	data = SiteInfo("robot_parser.txt")
	data.create_table("dane")

	url = data.data_from_txt.readline()
	headers = data.data_from_txt.readline()
	robots_info = data.data_from_txt.readline()

	data.write_table(headers)
	data.check_robots(robots_info)
	data.check_url(url)

	iter_page = int(input("Set the starting page: "))
	num_pages = int(input("Set the number of pages: "))
	url = url[:-1]

	while iter_page <= num_pages:
		
		urliter = (url + str(iter_page))

		#Get the url and its content
		crawler = TheCrawl(urliter)
		#Get the specific content of a page - another links
		crawler.get_link('href', 'a', class_ = 'product')
		crawler.get_content(data)
		crawler.get_details('table', class_ = 'productSpecification')
		crawler.reformat("Dowiedz się więcej więcej ", "")
		crawler.insert_to_reformat(" zł", "", 1, 'div', class_ = 'newPrice')

		for number, _ in enumerate(crawler.reformatted):
			
			crawler.add_by_regex("Producent: (.+?) Kod", number, ";")
			crawler.add_by_regex("Długość \(cm\): (.+?) Waga", number, ";")
			crawler.add_by_regex(
				"Waga \(g\): (.+?) Powierzchnia", number, ";")
			crawler.add_by_regex(
				"Powierzchnia główki \(cm2\): (.+?) Balans", number, ";")
			crawler.add_by_regex(
				"Balans \(mm\): (.+?) Sztywność", number, ";")
			crawler.add_by_regex("Sztywność \(RA\): (.+?) Układ", number, ";")
			crawler.add_by_regex("Układ strun: (.+?) Profil", number, ";")
			crawler.add_by_regex("Profil ramy \(mm\): (.+?) ", number, ";")
			crawler.add_by_regex("([0-9]{3,4}?,[0-9]{2})", number, "\n")

			crawler.product_spec.append(crawler.text)

			crawler.clear_text()

		for index, _ in enumerate(crawler.product_spec):

			data.write_table(crawler.product_spec[index])
		
		print(crawler.product_spec)

		iter_page +=1

	#Close csv file
	data.close_file()