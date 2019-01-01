# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import urlparse
from urlparse import urljoin
from law.items import LawItem

class NewSpider(scrapy.Spider):
    name = 'new'
    allowed_domains = ['www.avvo.com']
    start_urls = ['https://www.avvo.com/all-lawyers/ny/new_york.html']
   
   #Extracting all practice areas   
    def parse(self, response):
        next_url=response.css('.row.text-center.strong a::attr("href")').extract()
        for url in next_url:
            urls=response.urljoin(url)
            print(urls)
            yield scrapy.Request(urls, callback=self.parse_new)
            
    def parse_new(self, response):
        areas= response.css('.row ul.link-list.u-vertical-padding-half li a::attr("href")').extract()
        for area in areas:
            areau=response.urljoin(area)
            print(areau)
            yield scrapy.Request(areau, callback=self.parse_lawyers)

    def parse_lawyers(self,response):
        news=response.css('div.row a.v-serp-block-link::attr("href")').extract()
        for new in news:
            newu =response.urljoin(new)
            print(newu)
            yield scrapy.Request(newu, callback=self.parse_details)

       #Follow the paginatin link
        next_page_url = response.css('nav.pagination span a::attr("href")').extract_first()
        if next_page_url is not None:
            next_page_url=response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_lawyers)

    def parse_details(self, response):
        
            yield{
                'name':response.css('title::text').extract_first(),
                'about':response.css('div.card p::text').extract(),
                'license':response.css('li time::text').extract(),
                'avvo_rating':response.css('.row span.h3::text').extract(),
                'client_rating':response.css('.row span.small::text').extract(),
                'image':response.css('.row img::attr(src)').extract_first(),
                'phone':response.css('.row span.js-v-phone-replace a::attr("href")').extract_first(),
                'address':response.css('.row .v-lawyer-address span::text').extract(),
                'payment_types':response.css('.row .col-xs-12 .card h2.u-margin-top-0::text')[-1].extract(),
                'practice area':response.css('.row li.js-specialty a::attr("href")').extract(),
                'geo_details_link': response.css('.row a.js-v-google-map-link::attr("href")').extract(),

                
              
         }
           

           
            
           
    
