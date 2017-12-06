# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class JsonWithEncodingTutorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('tutorial.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MySQLStoreTutorialPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        if len(item) > 0:
            app_name = item['app_name']
            # print app_name
            conn.execute("""
                insert into apple_store(app_name, app_category, app_rank, app_content, app_url, app_developer)
                values(%s, %s, %s, %s, %s, %s)
            """, (app_name, item['app_category'], item['app_rank'], item['app_content'], item['app_url'],
                  item['app_developer']))


    # 异常处理
    def _handle_error(self, failue, item, spider):
        print str(failue)
