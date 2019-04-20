# Weibo Scraper

## A Selenium based scraper for the Chinese social media site Weibo
### The scraper utilises the advance search function of Weibo to acquire tweets and their respective dates:
#### 1. returned from search queries of a particular keyword of interest
#### 2. limited to a user-specified time window (date A to date B)

This scraper is designed for single account use although multiple account use is possible.
It is designed for small volume scraping, depending on specification and internet/Weibo server conditions, the scraper can acquire up to 150K tweets per day

Selenium and firefox (and its geckodriver) are required, although other browsers can also be easily made compatible with a slight modification to the code

To see how the scraper can be executed, see 'sample_execution.py'



Please note that the scraper can run into internet connection / weibo server response related issues, especially during long scraping sessions.
