from weibo_scrapper import weibo_scrapper
import datetime
import time

# specifying the variables used for testing
starting_date = datetime.datetime.strptime('01-02-2017', '%d-%m-%Y')
end_date = datetime.datetime.strptime('17-04-2017', '%d-%m-%Y')
username = 'ruoyzhang@outlook.com'
password = 'Cyfloel1.1.'
search_keyword = '人工智能'
save_dir = '../master_thesis_data/weibo'
max_page = 50
num_days = (end_date - starting_date).days

# initiation
scrape_this = weibo_scrapper(username=username, password=password, save_dir=save_dir)

# log in
scrape_this.login_weibo()
time.sleep(20)

# looping through the days
total_time = 0
begin = time.time()
for i in range(num_days):
	date = starting_date + datetime.timedelta(days = i)
	date = "-".join([str(int(elem)) for elem in str(date.date()).split('-')])
	scrape_this.scrape(begin_date=date, end_date=date, search_keyword=search_keyword, max_page=max_page)
	avg_time_so_far = (time.time() - begin)/(i+1)
	print('time lapsed for', str(i+1), 'iterations is', str(time.time()-begin), 'seconds')
	print('average time per iteration is:', avg_time_so_far,'seconds')
	print('total time to lapse predicted to be', str((avg_time_so_far * (num_days))/60), 'minutes')
	print('time remaining estimated to be', str((avg_time_so_far * (num_days-i-1))/60), 'minutes')