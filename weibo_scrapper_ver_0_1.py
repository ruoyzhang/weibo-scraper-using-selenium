import time
import re
import os
import sys
import codecs
import shutil
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from tqdm import tqdm
import pickle
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from math import floor

#-------------------------------------------------------------------------------------
# ||||||||||||||||||||||||||||||||||||||||||||||||
# ||||||                                    |||||| 
# ||||||    Weibo Scrapper with Selenium    ||||||
# ||||||                                    ||||||
# ||||||||||||||||||||||||||||||||||||||||||||||||
#
# 		* This scrapper is designed to scrape search results for a particular keyword
# 		* It requires a defined period in which the research results are limited to
# 		* It is suitable for very small volume of data acquisition
# 		* It will need a graphic use interface unix sys ready
# 		* It uses firefox as the browser
#-------------------------------------------------------------------------------------

class weibo_scraper():

	def __init__(self, username, password):
		"""
		username & password: user authentication
		"""

		# storing vars as class vars
		self.username = username
		self.password = password

		# variables for temporarily stocking single-page tweets and dates
		# initiated to be empty lists
		self.current_tweets = []
		self.current_dates = []

		# variables for temporarily stocking tweets for multi-page tweets and dates
		self.tweets_so_far = []
		self.dates_so_far = []

		# setting up the driver as a class method I guess?
		self.driver = webdriver.Firefox()

#-------------------------------------------------------------------------------------
	
	def clear_tweets_dates_so_far(self):
		"""
		method to reset current tweets and dates
		"""
		self.tweets_so_far = []
		self.dates_so_far = []

#-------------------------------------------------------------------------------------

	def clear_current_tweets_dates(self):
		"""
		method to reset cumulative tweets and dates
		"""
		self.current_tweets = []
		self.current_dates = []

#-------------------------------------------------------------------------------------

	def save_so_far(self, save_dir, name):
		"""
		method to save the below class variables at the specified location:
			tweets_so_far & dates_so_far

		save_dir: save directory
		name: name of the file, the files will have the '.pickle' extension
		"""

		# save the results as pickles
		with open(os.path.join(save_dir, '_'.join([name, 'texts.pickle'])), 'wb') as handle:
			pickle.dump(self.tweets_so_far, handle)
		with open(os.path.join(save_dir, '_'.join([name, 'dates.pickle'])), 'wb') as handle:
			pickle.dump(self.dates_so_far, handle)

#-------------------------------------------------------------------------------------

	def login_sina(self):
		"""
		function used to log into Sina
		"""
		try:
			# inputting username and password
			print("Loading 'login.sina.com.cn' now")
			self.driver.get("http://login.sina.com.cn/")
			elem_user = self.driver.find_element_by_name("username")
			elem_user.send_keys(self.username)
			elem_pwd = self.driver.find_element_by_name("password")
			elem_pwd.send_keys(self.password)

			# IMPORTANT: a temporary pause of 10s to bypass graphic verification
			time.sleep(10)

			# now login via the enter key
			elem_pwd.send_keys(Keys.RETURN)
			# and then wait for 2s
			time.sleep(2)

			# getting the cookie used for login in later
			#print(self.driver.current_url)
			#print(self.driver.get_cookies())
			#print('Outputting the cookie info')
			#for cookie in self.driver.get_cookies():
			#	for key in cookie:
			#		print(key, cookie[key])

			print('login successful')

		# handle exceptions and printing out error in case
		except Exception as e:
			print("Error: ", e)
		finally:
			print('End of login')

#-------------------------------------------------------------------------------------

	def login_weibo(self):
		"""
		function used to log into Weibo
		"""

		try:

			print("loading 'https://www.weibo.com/login.php'")

			# gavigate to the appropriate page
			self.driver.get("https://www.weibo.com/login.php")

			#change window size so that the login button can be scrolled into view
			self.driver.set_window_size(1404,1404)

			print('inputting username and password')

			# inputting username
			self.driver.find_element_by_xpath("//*[@id='loginname']").send_keys(self.username)

			# inputting password
			self.driver.find_element_by_xpath("//input[@type='password']").send_keys(self.password)

			# click on the login button
			self.driver.find_element_by_xpath("//a[@node-type='submitBtn']").click()

			# set the delay variable
			delay = 20

			# we instruct the web driver to wait until the desired element in the next page is successfully loaded before moving on
			try:
				WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//a[@node-type='account']")))
				print('login successful')
			except TimeoutException:
				print('login not yet successful after 20s, now executing an implicit {}s wait'.format(delay))
				self.driver.implicitly_wait(10)

		# handle exceptions and printing out error in case
		except Exception as e:
			print("Error: ", e)
		finally:
			print('End of login')

#-------------------------------------------------------------------------------------

	def advanced_search(self):
		"""
		a very simple wrapper for getting to the search page
		"""

		# navigating to the search interface
		print('navigating to Weibo search page')
		self.driver.get("http://s.weibo.com/")

		# input the search key and hit enter in order to advance to the advanced search interface
		print('inputing random search term to be redirected to the adv search page')
		item_inp = self.driver.find_element_by_xpath("//input[@type='text']")
		item_inp.send_keys('search_keyword')
		item_inp.send_keys(Keys.RETURN)

		delay = 10
		try:
			WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//a[@node-type='advsearch']")))
			print('successfully loaded the advanced search page')
		except TimeoutException:
			print('advanved search page not yet loaded after 10s, now executing an implicit {}s wait'.format(delay))
			self.driver.implicitly_wait(10)


#-------------------------------------------------------------------------------------

	def search_criterion(self, begin_date, end_date, search_keyword):
		"""
		inputting the search criterion once we're on the adv search page

		begin_date & end_date: date limits for the research results,
								they have to be in the format of "YYYY-MM-DD"
								as is conventional in the Chinese writting sys
		search_keyword: the keyword used for Weibo advanced search
		"""

		# parsing year, month and day for the 2 date variables
		# begin date
		begin_year = str(int(begin_date.split('-')[0]))
		begin_month = str(int(begin_date.split('-')[1])-1)
		begin_day = str(int(begin_date.split('-')[2]))

		# end date
		end_year = str(int(end_date.split('-')[0]))
		end_month = str(int(end_date.split('-')[1])-1)
		end_day = str(int(end_date.split('-')[2]))

		print('inputting search criterion')

		# now we try to instruct selenium to click on the 'advacned search' bottom
		self.driver.find_element_by_xpath("//a[@node-type='advsearch']").click()

		# below for instructing selenium to input the correct search keyword
		kw = self.driver.find_element_by_xpath("/html/body/div/div/div/div/dl/dd/input[@name='keyword']")
		kw.clear()
		kw.send_keys(search_keyword)

		# below for instructing selenium to click on the 'time' input field
		self.driver.find_element_by_xpath("//dd/input[@name='stime']").click()

		# below for instructing selenium to select the right **YEAR** value
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='year']").click()
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='year']/option[@value={}]".format(begin_year)).click()

		# below for instructing selenium to select the right **MONTH** value
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='month']").click()
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='month']/option[@value={}]".format(begin_month)).click()

		# below for instructing selenium to select the right **DAY** value
		self.driver.find_element_by_xpath("//ul[@class='days']/li/a[@title='{}']".format(begin_date)).click()

		# the below section is for selecting the right end date
		self.driver.find_element_by_xpath("//dd/input[@name='etime']").click()

		# end **YEAR**
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='year']").click()
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='year']/option[@value={}]".format(end_year)).click()

		# end **MONTH**
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='month']").click()
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='month']/option[@value={}]".format(end_month)).click()

		# end **DAY**
		self.driver.find_element_by_xpath("//ul[@class='days']/li/a[@title='{}']".format(end_date)).click()

		# click on the 'search' button
		self.driver.find_element_by_xpath("//div[@class='m-adv-search']/div[@class='btn-box']/a[@class='s-btn-a']").click()

		# we instruct the function to wait until the tweets are loaded properly
		delay = 10
		try:
			WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//p[@class='txt' and @node-type='feed_list_content']")))
			#print('successfully loaded the search result page')
		except TimeoutException:
			print('search result page not yet loaded after {}s, now executing an implicit 10s wait'.format(delay))
			self.driver.implicitly_wait(10)

#-------------------------------------------------------------------------------------

	def scrape_this_page(self):
		"""
		Scrape all the tweets and their respective dates on the page
		The page *** HAS TO *** be a result page of the advance search function
		"""

		# now get the tweets
		tweets = self.driver.find_elements_by_xpath("/html/body/div/div/div/div/div/div/div/div/div/p[@class='txt' and @node-type='feed_list_content']")

		# retrieve only the text
		tweets = [tweet.text for tweet in tweets]

		# the below extracts date
		dates = self.driver.find_elements_by_xpath("/html/body/div/div/div/div/div/div/div/div/div/p[@class='from']")

		# trying to convert string to datetime format
		# first, replace the chinese characters
		dates = [date.text.split(' ')[0].replace('年', ' ').replace('月', ' ').replace('日', '') for date in dates]

		# then add year if necessary
		dates = ['2019 ' + date if len(date) == 5 else date for date in dates]

		# then we convert it to datetime format
		dates = [datetime.datetime.strptime(date, '%Y %m %d') for date in dates]

		# storing them in class variables
		self.current_tweets = tweets
		self.current_dates = dates

#-------------------------------------------------------------------------------------
	
	def next_page(self):
		"""
		a simple wrapper for commading selenium to go to the next page by clicking on the current button
		"""
		self.driver.find_element_by_xpath("//a[@class='next']").click()

		# we instruct the function to wait until the tweets are loaded properly
		delay = 10
		try:
			WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//p[@class='txt' and @node-type='feed_list_content']")))
			#print('successfully loaded the search result page')
		except TimeoutException:
			print('page not yet loaded after {}s, now executing an implicit 10s wait'.format(delay))

#-------------------------------------------------------------------------------------

	def scrape_first_x_pages(self, num_pg):
		"""
		a method to scrape the first user-defined number of pages for a particular query
		please note that the results will be accumulated at the class vars: tweets_so_far & dates_so_far

		num_pg: the max number of pages to scrape
		"""

		# first navigate to the search page and initiate search
		#elf.advanced_search()

		# specify the search criterion
		#self.search_criterion(begin_date, end_date, search_keyword)

		# now loop through the user defined number of pages
		for i in range(num_pg):
			# scrape the current page with exception handler
			try:
				self.scrape_this_page()
			except ValueError:
				print('currently at the final page, we have obtained tweets from', str(i), 'pages')
				break

			# update the stored tweets and dates
			self.tweets_so_far += self.current_tweets
			self.dates_so_far += self.current_dates

			print('page', str(i+1), 'complete')

			# turn the next page with the exception handler
			if i < num_pg - 1:
				try:
					self.next_page()
				except NoSuchElementException:
					print('currently at the final page, we have obtained tweets from', str(i), 'pages')
					break

#-------------------------------------------------------------------------------------


	def scrape_over_period(self, begin_date, end_date, search_keyword, window_size, num_pg, save = False, save_dir = '/data'):
		"""
		The scrapping method for one single search keyword divided into multiple queries, each covering the same window size in terms of time (usually number of days)
		this method will allow the user to scrape results organised in the following form:
		*************************
		
		begin_date --------------------------------------------------------------> end_date

		   period 0	  	      period 1	  		 period 2 	  	   ...    period n
		|<---------------->|<---------------->|<---------------->| ... |<---------------->|
		| multi-pg scrape 0|multi-pg scrape 1 |multi-pg scrape 2 | ... |multi-pg scrape n |

		*************************

		where each multi-pg scrape contains tweets from a subperiod of the predefined window size

		begin_date & end_date: date limits for the research results,
								they have to be in the format of "YYYY-MM-DD"
								as is conventional in the Chinese writting sys
		search_keyword: the keyword used for Weibo advanced search, also used in this function to name the results
		window_size: the number of consecutive days covered in one single query
		num_pg: the max number of pages from which we srape data off, must be greater than 1
		save: boolean, optional, indicates to the function whether the results are saved per query or not
		save_dir: directory to store the data, optional and by default '/data'
		"""

		# converting dates to datetime format
		begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
		end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

		# calculating the total number of days and how many iterations we need
		num_days = (end_date - begin_date).days + 1
		if num_days % window_size > 0:
			num_periods = floor(num_days / window_size) + 1
		else:
			num_periods = int(num_days / window_size)

		# routine search query launch
		self.advanced_search()


		begin_time = time.time()
		tweet_count = 0
		date_count = 0

		# now loop through all the periods
		for i in range(num_periods):

			# determining the begin and end dates for the period
			date_0 = begin_date + datetime.timedelta(days = i * window_size)
			# specify for the final period
			if i != num_periods - 1:
				date_1 = date_0 + datetime.timedelta(window_size - 1)
			else:
				date_1 = end_date

			# converting the dates into the right str format
			date_0 = "-".join([str(int(elem)) for elem in str(date_0.date()).split('-')])
			date_1 = "-".join([str(int(elem)) for elem in str(date_1.date()).split('-')])

			# update the search criterion
			self.search_criterion(begin_date = date_0, end_date = date_1, search_keyword = search_keyword)

			print('now starting scrapping')

			# multi-page scrape
			self.scrape_first_x_pages(num_pg)

			print('scraping complete for period', i)

			# saving the results if required
			if save:
				self.save_so_far(save_dir, '_'.join([search_keyword, date_0, date_1]))
				print('saving the data for period', i)
				
				# update the tweet count
				tweet_count += len(self.tweets_so_far)
				date_count += len(self.dates_so_far)

				# clear the storage variables
				self.clear_tweets_dates_so_far()
			else:
				tweet_count = len(self.tweets_so_far)
				date_count = len(self.dates_so_far)

			print('so far we have scraped a total of', tweet_count, 'tweets')

			if tweet_count != date_count:
				print('!!!!!!!!!!!!!!!!!!!!!!!!!! number of tweets and number of dates not equal')
				break

			# time consumption information and remaining time estimation
			avg_time_so_far = (time.time() - begin_time)/(i+1)
			print('time lapsed for', str(i+1), 'iterations is', str(time.time()-begin_time), 'seconds')
			print('average time per iteration is:', avg_time_so_far,'seconds')
			print('total time to lapse predicted to be', str((avg_time_so_far * (num_periods))/60), 'minutes')
			print('time remaining estimated to be', str((avg_time_so_far * (num_periods-i-1))/60), 'minutes')
			print(' ')
			print(' ')





























