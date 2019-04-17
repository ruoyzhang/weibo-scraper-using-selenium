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
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from tqdm import tqdm
import pickle

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

class weibo_scrapper():

	def __init__(self, username, password, save_dir):
		"""
		username & password: user authentication
		save_dir: directory for where we want to save the srapped data
		"""

		# storing vars as class vars
		self.username = username
		self.password = password
		self.save_dir = save_dir

		# setting up the driver as a class method I guess?
		self.driver = webdriver.Firefox()

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
			time.sleep(5)

			# click on the login button
			self.driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/ul/li/a[@node-type='loginBtn']").send_keys(Keys.RETURN)
			time.sleep(5)

			print('inputting username and password')

			# inputting username
			elem_user = self.driver.find_element_by_xpath("/html/body/div/div/div/div/div/input[@node-type='username']")
			elem_user.clear()
			elem_user.send_keys(self.username)

			# inputting password
			elem_pwd = self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[3]/div[3]/div[2]/input")
			elem_pwd.clear()
			elem_pwd.send_keys(self.password)

			# click on the login button
			self.driver.find_element_by_xpath("/html/body/div/div/div/div/div/a[@node-type='submitBtn']").click()

			print('login successful')

		# handle exceptions and printing out error in case
		except Exception as e:
			print("Error: ", e)
		finally:
			print('End of login')

#-------------------------------------------------------------------------------------

	def scrape(self, begin_date, end_date, search_keyword):
		"""
		The scrapping method

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

		print('navigating to Weibo adv search page')

		# navigate to the search interface
		self.driver.get("http://s.weibo.com/")

		print('waiting for page to load ...')

		# need to wait for the page to load else it won't work
		time.sleep(10)

		print('specifying search criterion')

		# input the search key and hit enter in order to advance to the advanced search interface
		item_inp = self.driver.find_element_by_xpath("//input[@type='text']")
		item_inp.send_keys(search_keyword)
		item_inp.send_keys(Keys.RETURN)

		# waiting
		time.sleep(5)

		# now we try to instruct selenium to click on the 'advacned search' bottom
		self.driver.find_element_by_xpath("//a[@node-type='advsearch']").click()

		# below for instructing selenium to click on the 'time' input field
		self.driver.find_element_by_xpath("//dd/input[@value='请选择日期'][1]").click()

		# below for instructing selenium to select the right **YEAR** value
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='year']").click()
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='year']/option[@value={}]".format(begin_year)).click()

		# below for instructing selenium to select the right **MONTH** value
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='month']").click()
		self.driver.find_element_by_xpath("//div[@class='selector']/select[@class='month']/option[@value={}]".format(begin_month)).click()

		# below for instructing selenium to select the right **DAY** value
		self.driver.find_element_by_xpath("//ul[@class='days']/li/a[@title='{}']".format(begin_date)).click()

		# the below section is for selecting the right end date
		self.driver.find_element_by_xpath("//dd/input[@value='请选择日期'][2]").click()

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

		# need to wait again
		time.sleep(5)

		print('waiting for results to load ...')

		# a loop for all the result pages
		# first determine the total number of pages (usually 50 but just in case)
		dropdown_page = self.driver.find_elements_by_xpath("/html/body/div/div/div/div/div/div/span/ul[@node-type='feed_list_page_morelist']/li")
		num_pg = len(dropdown_page)

		print('there are ', str(num_pg), ' of results')

		# storage variables for the tweets and dates
		all_tweets = []
		all_dates = []

		print('now scrapping ...')

		# now loop
		for i in range(num_pg - 1):

			# now get the tweets
			tweets = self.driver.find_elements_by_xpath("/html/body/div/div/div/div/div/div/div/div/div/p[@class='txt' and @node-type='feed_list_content']")

			# retrieve only the text
			tweets = [tweet.text for tweet in tweets]

			# # the below extracts date
			dates = self.driver.find_elements_by_xpath("/html/body/div/div/div/div/div/div/div/div/div/p[@class='from']")

			# trying to convert string to datetime format
			# first, replace the chinese characters
			dates = [date.text.split(' ')[0].replace('年', ' ').replace('月', ' ').replace('日', '') for date in dates]

			# then add year if necessary
			dates = ['2019 ' + date if len(date) == 5 else date for date in dates]

			# then we convert it to datetime format
			dates = [datetime.strptime(date, '%Y %m %d') for date in dates]

			# append res to the storage variables
			all_tweets += tweets
			all_dates += dates

			print('page ', str(i+1), ' complete')

			# go to the next page
			self.driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/a[@class='next']").click()

			# wait again
			time.sleep(1)

		print('all pages scrapped, now saving ...')

		# save the results as pickles
		with open(os.path.join(self.save_dir, '_'.join([end_day, end_month, end_year, 'text.pickle'])), 'wb') as handle:
			pickle.dump(all_tweets, handle)
		with open(os.path.join(self.save_dir, '_'.join([end_day, end_month, end_year, 'date.pickle'])), 'wb') as handle:
			pickle.dump(all_dates, handle)

		print('save complete, files can be found at: ', self.save_dir)

