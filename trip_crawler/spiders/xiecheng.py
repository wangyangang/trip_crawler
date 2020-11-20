import scrapy
from urllib.parse import quote
from functools import reduce
from trip_crawler.items import TripCrawlerItem


class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['ctrip.com']
    # start_urls = ['http://ctrip.com/']
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': '_RF1=221.218.211.105; _RSG=A3qHdWLUHH00jJ.lh_SgzA; _RDG=286b11cc8dd3822aef3f16934df61ef567; _RGUID=04517958-2747-40ca-af6a-73faeff93b40; MKT_CKID=1605696346040.f1xv0.tqjf; _ga=GA1.2.597831558.1605696346; MKT_Pagesource=PC; _abtest_userid=27c7600a-d42c-4f06-b6ee-fbb386807954; ASP.NET_SessionSvc=MTAuNjAuNDkuNzh8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTU4OTAwMzM0Njc4NQ; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&createtime=1605864496&Expires=1606469295693; _jzqco=%7C%7C%7C%7C%7C1.1364881985.1605696346037.1605697980276.1605864495711.1605697980276.1605864495711.0.0.0.10.10; MKT_CKID_LMT=1605864495714; __zpspc=9.2.1605864495.1605864495.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _gid=GA1.2.1701149798.1605864496; _gat=1; _bfa=1.1605696343553.3rqekn.1.1605696343553.1605864493277.2.29; _bfs=1.3; _bfi=p1%3D290057%26p2%3D290049%26v1%3D29%26v2%3D28; appFloatCnt=25',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def start_requests(self):
        base_url = 'https://you.ctrip.com/searchsite/travels/?query=%e5%8f%88%e8%a7%81%e5%b9%b3%e9%81%a5&isAnswered=&isRecommended=&publishDate=&PageNo={}'
        for page in range(1, 32):
            url = base_url.format(page)
            yield scrapy.Request(url, headers=self.headers, dont_filter=True, cb_kwargs={'page': page},
                                 callback=self.parse_list)

    def parse_list(self, response, **kwargs):
        page = kwargs.get('page')
        articles = response.xpath('//ul[@class="youji-ul cf"]/li')
        for index, article in enumerate(articles):
            href = article.xpath('./dl/dt/a/@href').get()
            title = article.xpath('./dl/dt/a/text()').get()
            detail_url = 'https://you.ctrip.com' + href
            yield scrapy.Request(detail_url, headers=self.headers.update(referer=response.url),
                                 callback=self.parse_detail,
                                 cb_kwargs={'page': page, 'index': index + 1, 'title': title})

    def parse_detail(self, response, **kwargs):
        page = kwargs.get('page')
        index = kwargs.get('index')
        title = kwargs.get('title')
        content = response.xpath('//div[@class="ctd_content"]//text()').getall()
        content = reduce(lambda x, y: x.strip() + y.strip(), content) if content else ''
        item = TripCrawlerItem()
        item['page'] = page
        item['index'] = index
        item['title'] = title
        item['content'] = content
        yield item

