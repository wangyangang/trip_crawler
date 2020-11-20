import scrapy
from functools import reduce
from trip_crawler.items import MafengwoItem


class MafengwoSpider(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['mafengwo.cn']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '__jsluid_h=e165e099d46584c2d3a91a49b606f01b; PHPSESSID=lv3t66t4qn1tds6r8kmc6k3er0; __jsl_clearance=1605894047.248|0|nTsfTCF1HnvYFfePlx3APXx5D2c%3D; mfw_uuid=5fb7ffa0-fff2-b74d-6f2d-d7e019e01f4d; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-11-21+01%3A40%3A48%22%3B%7D; __mfwc=direct; __mfwa=1605894049196.39978.1.1605894049196.1605894049196; __mfwlv=1605894049; __mfwvn=1; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1605894049; UM_distinctid=175e6be91c5325-0dc3359465d036-326d7907-13c680-175e6be91c6af6; CNZZDATA30065558=cnzz_eid%3D603827338-1605891217-http%253A%252F%252Fwww.mafengwo.cn%252F%26ntime%3D1605891217; bottom_ad_status=0; __omc_chl=; __omc_r=; __mfwb=16cff532002d.3.direct; __mfwlt=1605894074; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1605894074',
        'DNT': '1',
        'Host': 'www.mafengwo.cn',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def start_requests(self):
        url1 = 'http://www.mafengwo.cn/search/q.php?q=%E5%8F%88%E8%A7%81%E5%B9%B3%E9%81%A5%E5%89%A7%E5%9C%BA&p=1&t=notes&kt=1'
        url2 = 'http://www.mafengwo.cn/search/q.php?q=%E5%8F%88%E8%A7%81%E5%B9%B3%E9%81%A5%E5%89%A7%E5%9C%BA&p=2&t=notes&kt=1'

        yield scrapy.Request(url1, headers=self.headers, callback=self.parse, cb_kwargs={'page': 1}, dont_filter=True)
        yield scrapy.Request(url2, headers=self.headers, callback=self.parse, cb_kwargs={'page': 2}, dont_filter=True)

    def parse(self, response, **kwargs):
        # with open('detail1.html', 'w') as f:
        #     f.write(response.body.decode())
        page = kwargs.get('page')
        articles = response.xpath('//div[@class="att-list"]/ul/li')
        for index, article in enumerate(articles):
            title = article.xpath('./div/div[2]/h3/a/text()').get()
            href = article.xpath('./div/div[2]/h3/a/@href').get()
            yield scrapy.Request(href,
                                 callback=self.parse_detail,
                                 headers=self.headers,
                                 cb_kwargs={'page': page, 'index': index + 1, 'title': title})

    def parse_detail(self, response, **kwargs):
        page = kwargs.get('page')
        index = kwargs.get('index')
        title = kwargs.get('title')
        content = response.xpath('//div[@class="_j_content_box"]//text()').getall()
        content = reduce(lambda x, y: x.strip() + y.strip(), content) if content else ''
        item = MafengwoItem()
        item['page'] = page
        item['index'] = index
        item['title'] = title
        item['content'] = content
        yield item
