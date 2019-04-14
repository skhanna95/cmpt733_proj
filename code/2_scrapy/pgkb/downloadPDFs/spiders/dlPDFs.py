import scrapy
import urllib
import os
import re
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
import scrapy.signals

class downloadPDFs(scrapy.Spider):
    name = "downloadPDFs"

    #allowed_domains = ["bccancer.bc.ca"]
    #start_urls = [
    #    "http://www.bccancer.bc.ca/health-professionals",
    #    #"http://www.bccancer.bc.ca/health-professionals/clinical-resources/chemotherapy-protocols/genitourinary",
    #]
    allowed_domains = ["pharmgkb.org"]
    start_urls = [
        "https://www.pharmgkb.org",
    ]
    #allowed_domains = ["hhwangs27.com"]
    #start_urls = [
    #    "http://hhwangs27.com",
    #]

    rr_doi = re.compile(r'https?://.*doi.org/(.+)$')
    rr_pmcid = re.compile(r'https?://www.ncbi.nlm.nih.gov/pmc/.*PMC(\d+)$')
    rr_pmid = re.compile(r'https?://www.ncbi.nlm.nih.gov/pubmed/(\?term=)?(\d+)')

    def __init__(self):
        # makes brower do not load imgs
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_experimental_option(
            "prefs",
            {"profile.managed_default_content_settings.images":2})

        self.browser = webdriver.Chrome(
            executable_path="/usr/local/bin/chromedriver",
            options=chrome_opt)

        super(downloadPDFs, self).__init__()

        # when spider close we call this function
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)

    def spider_closed(self, spider):
        # close the browser when spider is closed
        self.browser.quit()






    def parse(self, response):
        for href in response.css('a::attr(href)').extract():

            hrefparsed = urllib.parse.unquote_plus(href)

            if href.endswith('.pdf'):
                yield response.follow(href, self.pdf_save)

            elif self.rr_doi.match(hrefparsed):
                res = self.rr_doi.match(hrefparsed)
                with open('dois.txt', 'a') as f:
                    f.write(f'{res.group(1)}\n')

            elif self.rr_pmcid.match(hrefparsed):
                res = self.rr_pmcid.match(hrefparsed)
                with open('pmcids.txt', 'a') as f:
                    f.write(f'{res.group(1)}\n')

            elif self.rr_pmid.match(hrefparsed):
                res = self.rr_pmid.match(hrefparsed)
                with open('pmids.txt', 'a') as f:
                    f.write(f'{res.group(2)}\n')

            else:
                yield response.follow(href, self.parse)
            # for *test* yield response.follow(href, self.test)

    #def test(self, response):
    #    print("Harry Wang"+response.url)

    def pdf_save(self, response):
        path = 'pdfs' + urllib.parse.urlparse(response.url).path
        self.logger.info(f'Saving PDF {path}')
        dirnm = os.path.dirname(path)
        if not os.path.exists(dirnm):
            os.makedirs(dirnm)
        with open(path, 'wb') as f:
            f.write(response.body)
