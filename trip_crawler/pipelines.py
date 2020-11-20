# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import pandas as pd
from trip_crawler.items import TripCrawlerItem, MafengwoItem


class TripCrawlerFilePipeline:
    def __init__(self):
        self.datas1 = list()
        self.datas2 = list()

    def process_item(self, item, spider):
        if isinstance(item, TripCrawlerItem):
            self.datas1.append(item)
        elif isinstance(item, MafengwoItem):
            self.datas2.append(item)
        return item

    def close_spider(self, spider):
        self.datas1.sort(key=lambda x: (x['page'], x['index']))
        df1 = pd.DataFrame(self.datas1)
        df1.to_excel('xiecheng.xlsx')

        self.datas2.sort(key=lambda x: (x['page'], x['index']))
        df2 = pd.DataFrame(self.datas2)
        df2.to_excel('mafengwo.xlsx')


class TripCrawlerMysqlPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.num = 0

    def open_spider(self, spider):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                                    password='456wyg31', db='trip', charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print('*' * 20)
        page = item['page']
        index = item['index']
        title = item['title']
        content = item['content']
        try:
            self.cursor.execute('INSERT INTO articles values(NULL, %s, %s, %s, %s)', (page, index, title, content))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        print('end')
        self.cursor.close()
        self.conn.close()
