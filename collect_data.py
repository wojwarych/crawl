if __name__ == "__main__":

    import wrap_crawl


    start_url = 'https://strefatenisa.com.pl/rakiety-tenisowe/rakiety-seniorskie/page=1'
    tennis_data = wrap_crawl.TheCrawl(
        start_url,
        [
            'Producent:',
            'Waga (g):',
            'Długość (cm):',
            'Powierzchnia główki (cm2):',
            'Balans (mm):',
            'Sztywność (RA):',
            'Układ strun:',
            'Profil ramy (mm):'
        ]
    )

    #pdb.set_trace()
    while tennis_data.is_next_page():
        urls = tennis_data.get_link_next()
        tennis_data.set_link_next()

    for item in tennis_data.link_pages:
        #pdb.set_trace()
        tennis_data.get_tree(item)
        tennis_data.racquet_links.append(tennis_data.get_links(tennis_data.page_tree, "a", class_="product"))

    tennis_data.get_racquet_hrefs(tennis_data.racquet_links)


    for href in tennis_data.racquet_links:

        tennis_data.get_tree(href)
        price = tennis_data.get_price('div', class_='newPrice')
        tennis_data.get_content(tennis_data.requested_data)
        tennis_data.set_gathered_data(tennis_data.requested_data, price)


    with open('racquets_data.csv', 'w', newline='') as csvfile:
        linewriter = csv.writer(
            csvfile,
            delimiter=';',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL,)

        for item in tennis_data.gathered_data:
            linewriter.writerow(item)