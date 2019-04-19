from weibo_scrapper_ver_0_1 import weibo_scraper
import datetime
import time

# specifying the variables used for testing
begin_date = datetime.datetime.strptime('12-01-2016', '%d-%m-%Y')
end_date = datetime.datetime.strptime('12-01-2016', '%d-%m-%Y')
date = begin_date
date = "-".join([str(int(elem)) for elem in str(date.date()).split('-')])
username = 'ruoyzhang@outlook.com'
password = 'Cyfloel1.1.'
search_keyword = '人工智能'
save_dir = '../master_thesis_data/weibo/test'
max_page = 50
num_days = (end_date - begin_date).days

# initiation
scrape_this = weibo_scraper(username=username, password=password)

# login
scrape_this.login_weibo()

# advance search queries
scrape_this.advanced_search()
scrape_this.search_criterion(begin_date = date, end_date = date, search_keyword = search_keyword)

# scrape 30 pages
scrape_this.scrape_first_x_pages(num_pg = 50)

# save
scrape_this.save_so_far(save_dir = save_dir, name = 'test')

