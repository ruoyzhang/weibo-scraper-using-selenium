from weibo_scrapper_ver_0_1 import weibo_scraper
import datetime
import time


username = 'insert_username'
password = 'insert_password'
headless = True

begin_date = '2016-01-12'
end_date = '2016-01-18'

search_keyword = '人工智能'
window_size = 1

num_pg = 15

save = True
save_dir = 'insert_dir'



# initiation
scrape_this = weibo_scraper(username=username, password=password, headless = headless)

# login
scrape_this.login_weibo()

# advance search queries
scrape_this.scrape_over_period(begin_date = begin_date, end_date = end_date,
	search_keyword = search_keyword, window_size = window_size, num_pg = num_pg,
	save = save, save_dir = save_dir)