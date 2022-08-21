from gc import callbacks
from urllib.parse import urljoin
import scrapy

class Spiderx(scrapy.Spider):
    name = 'spiderx'
    start_urls = ['https://1337x.to/sort-search/yts/seeders/desc/1/']
    
    

    def parse(self, response):
        page = response.css('div.pagination')
        link = response.css('td.coll-1.name')
        collected_link = link.xpath('.//a[2]/@href').getall()
        for productlink in collected_link:
            url = urljoin('https://1337x.to/', productlink)
            yield response.follow(url,callback = self.parse_magnet)
        next_page = page.css('a::attr(href)').extract()[-2]
        next_page_url = urljoin('https://1337x.to/', next_page)
        if next_page is not None:
            yield response.follow(next_page_url, callback=self.parse)

                  
    def parse_magnet(self, response):
        details =response.css('ul.list')
        detail_info = response.css('div.torrent-detail-info')
        list_all = details.css('span::text').getall()
        genres = detail_info.css('span::text').getall()
        try:
            yield{
            
            'Name' :  response.css('h1::text').get().strip(),
            'genres' : genres,
            'Quality_type' : list_all[1],
            'Language'  : list_all[2],
            'Total Size' : list_all[3],
            'last_checked': list_all[6],
            'Seeders' : list_all[8],
            'Leechers': list_all[9],
            'Magnet_Link': response.css('a.l1762ea73eada99a88a62eb77db4f230464fc359d.l7a197fd7320cb21edb9b6018d783c3f6c8a52777.l7ac02d78cc3bbc918b19a6ff6e0b6dae9997a697').attrib['href']
             }
        except:
            yield{
            
            'Name' :  response.css('h1::text').get().strip(),
            'genres' : 'No info available',
            'Quality_type' : list_all[1],
            'Language'  : list_all[2],
            'Total Size' : list_all[3],
            'last_checked': list_all[6],
            'Seeders' : list_all[8],
            'Leechers': list_all[9],
        ## the following magnet_link class is keep on changing every 5 min so you have to change it to avoid keyerror ['href']
            'Magnet_Link': response.css('a.l62ab48c479083af9dc91f0cdf366a6e98c26f864').attrib['href']
             }
    

    

     
    