# Weibo Scraper

## A Selenium based scraper for the Chinese social media site Weibo
### The scraper utilises the advance search function of Weibo to acquire tweets and their respective dates:
#### 1. returned from search queries of a particular keyword of interest
#### 2. limited to a user-specified time window (date A to date B)

This scraper is designed for single account use on multiple simultaneous sessions although multiple account use is possible.
It is designed for small volume scraping, depending on specification and internet/Weibo server conditions, the scraper can acquire up to 150K tweets per session per day, with a 7-session set up, the scraper can gather roughly 1 million tweets per day.

Selenium and firefox (and its geckodriver) are required, although other browsers can also be easily made compatible with a slight modification to the code

To see how the scraper can be executed, see 'sample_execution.py'



Please note that the scraper can run into internet connection / weibo server response related issues, especially during long scraping sessions. The scraping speed largely depends on your location internet connection conditions and where you are in the World, for example, scraping this with a Chinese internet connection will most likely lead to faster scraping speed and experience fewer errors than someone executing this with an European connection

*** please note that the program runs by default in firefox headless mode, the option to run it with the head is provided by the variable 'headless' when initiating the class. ***
