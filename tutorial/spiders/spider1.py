import scrapy
import csv
import json

class FundsSpider(scrapy.Spider):
    name='funds'

    def start_requests(self):
        funds = {
            'reliance-pharma-fund':'/MRC059',
            'sbi-healthcare-opportunities-fund':'/MSB008',
            'tata-india-pharma-healthcare-fund-direct-plan-dividend-payout':'/MTA1156',
            'uti-healthcare-fund':'/MUT089',
            'aditya-birla-sun-life-digital-india-fund':'/MAC024',
            'icici-prudential-technology-fund':'/MPI014',
            'hdfc-growth-opportunities-fund':'/MMS004',

        }
        
        for key in funds:
            #url = 'http://www.moneycontrol.com/mutual-funds/'+ key +'/investment-info'+ funds[key]
            #yield scrapy.Request(url=url, callback=self.parse)
            url = 'https://www.moneycontrol.com/mutual-funds/nav/'+ key + funds[key]
            yield scrapy.Request(url=url, callback=self.parse2)

    def parse(self, response):
        title = response.css('title::text').extract_first()
        data = {}
        data['NAV']=response.css('div.toplft_cl1 div span.bd30tp::text').extract_first()
        data['NAV Growth']=response.css('div.toplft_cl1 div span.gL_13 span::text').extract_first()
        for quote in response.css('div.brdb.PT3.PB5.b13.PL10'):
            typ = quote.css('div.FL.w150 strong::text').extract_first()
            value = quote.css('div.FL.w250::text').extract_first()
            if typ is not None or value is not None:
                data[typ]=  value

        yield { 
            title:data
            }
    
    def parse2(self, response):
        title = response.css('title::text').extract_first()
        data = {}
        data['NAV']=response.css('div.mufndBx div.pcnsb span.stprh ::text').extract_first()
        data['NAV Growth']=response.css('div.mufndBx div.pcnsb span.grnpc1::text').extract_first() or response.css('div.mufndBx div.pcnsb span.redpc1::text').extract_first()
        for quote in response.css('ul.investr_info'):
            for item in quote.css('li'):
                typ = item.css('span::text').extract_first()
                value = item.css('p::text').extract_first() or item.css('p a::text').extract_first()
                if typ is not None or value is not None:
                    data[typ]=  value

        file_data = { 
            'fund': title,
            "data": data
            }
        
        yield file_data
        with open('chinmay_17ME10018.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            #row = []
            val = []
            for key, value in file_data.items():
                if type(value) is not dict:
                    #row.append(key)
                    val.append(value)            
                else:
                    for key, value in value.items():
                        #row.append(key)
                        val.append(value)
            #writer.writerow(row)
            writer.writerow(val)