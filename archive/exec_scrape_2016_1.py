from weibo_scrapper_ver_0_1 import weibo_scraper


username = 'ruoyzhang@outlook.com'
password = 'Cyfloel1.1.'

begin_date = '2017-08-15'
end_date = '2017-08-20'

search_keyword = '人工智能'
window_size = 1

num_pg = 50

save = True
save_dir = '../master_thesis_data/weibo_raw'



# initiation
scrape_this = weibo_scraper(username=username, password=password)

# login
scrape_this.login_weibo()

# advance search queries
scrape_this.scrape_over_period(begin_date = begin_date, end_date = end_date,
	search_keyword = search_keyword, window_size = window_size, num_pg = num_pg,
	save = save, save_dir = save_dir)


# done done done