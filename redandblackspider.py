import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import csv
from bs4 import BeautifulSoup

class redandblackspiderSpider(CrawlSpider): #this is just the default scrapy stuff
    name = 'redandblackspider'
    allowed_domains = ['redandblack.com']
    start_urls = ['http://www.redandblack.com/athensnews']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )
   
       
    def parse_item(self, response):

        category = response.url #since the website has no category displayed, I got it from the URL
        category = category[category.index('/')+1:]
        category = category[category.index('/')+1:]
        category = category[category.index('/')+1:]
        category = category[:category.index('/')]

        try: #these all extract elements from the page. All news story should have all these elements.
            soup = BeautifulSoup(response.text, 'html.parser')
            headline = soup.find(class_='headline').get_text()
            body = soup.find(itemprop='articleBody').getText()
            date = soup.find(class_='asset-date').get_text()
            author = soup.find(itemprop='author').get_text()
        except: #this just makes sure that if the above values aren't found, they are still assigned something.
            headline = ""
            date = ""
            author = ""
            body = ""
            print("Some value was not found")
        csvfile = open("redandblackarticles.csv", 'a', newline='') #opened with the 'a' setting so it will re-open the same file, rather than make a new one.
        writer = csv.writer(csvfile)
        if category == "search" or category == "users":
            print("This page was useless")#these pages are useless, and are never news stories.
        else:
            writer.writerow([date.strip(), headline.strip(), body.strip(), author.strip(), category, response.url])
