# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from taonan.items import TaonanItem


# class TnanSpider(CrawlSpider):
#使用分布式的方法
class TnanSpider(RedisCrawlSpider):
    name = 'tnan'
    allowed_domains = ['taonanw.com']
    # 使用scrpay_redis时 修改
    # start_urls = [
        # 'http://www.taonanw.com/page/search_result_v2/p/1/search_type/search_quick/page_key/93e0a62a085397e93da5ed4bb727e0be/match_gender/1/match_r_city_id/330100/match_age_min/18/match_age_max/25/items_file/search_result_v2/total/1160/match_r_state_id/6941/n/20/list_style/2']
    #分布式爬取的入口
    redis_key = 'tnanspider:start_urls'

    # 使用动态域范围获取（可以使用也可以不使用）
    # def __init__(self,*args,**kwargs):
    #     domain = kwargs.pop('domain','')
    #     self.allowed_domains = filter(None,domain.split(','))
    #     super(TnanSpider,self).__init__(*args,**kwargs)


    # 杭州18-25岁列表页
    page_link = LinkExtractor(allow=(
        r'taonanw.com/page/search_result_v2/p/\d+/search_type/search_quick/page_key/93e0a62a085397e93da5ed4bb727e0be/match_gender/1/match_r_city_id/330100/match_age_min/18/match_age_max/25/items_file/search_result_v2/total/1160/match_r_state_id/6941/n/20/list_style/2'))
    # 个人主页的连接
    profile_link = LinkExtractor(allow=(r'taonanw.com/u_\d+'))

    rules = (
        Rule(page_link,follow=True),
        Rule(profile_link, callback='parse_item',follow=False),
    )
    def parse_item(self, response):

        # 创建Items字段
        item = TaonanItem()
        # 用户名
        item['username'] = self.get_username(response)

        # 年龄
        item['age'] = self.get_age(response)

        # 出生地
        item['address'] = self.get_address(response)

        # 学历
        item['education'] = self.get_education(response)

        # 头像url
        item['headerurl'] = self.get_headerurl(response)

        # 相册图片url
        item['images_url'] = self.get_images_url(response)

        # 交友宣言
        item['content'] = self.get_content(response)

        # 择友地址
        item['fage'] = self.get_fage(response)

        # 个人主页
        item['source_url'] = response.url

        # 数据来源网站
        item['source'] = 'taonan'
        yield item

    # 解析各个字段
    def get_username(self, response):
        username = response.xpath("//div[@id='p1_act']//a//h1/text()").extract()
        if len(username):
            username = username[0]
        else:
            username = 'Null'
        return username

    def get_age(self, response):
        age = response.xpath("//div[@class='userinfo-item']//span[@id = 'profile_age']//text()").extract()
        if len(age):
            age = age[0]
        else:
            age = 'Null'
        return age

    def get_address(self, response):
        address = response.xpath("//div[@class='userinfo-item']//span[@id = 'profile_n_state_id']//text()").extract()
        if len(address):
            address = address[0]
        else:
            address = 'Null'
        return address

    def get_education(self, response):
        education = response.xpath("//div[@class='userinfo-item']//span[@id = 'profile_education']//text()").extract()
        if len(education):
            education = education[0]
        else:
            education = 'Null'
        return education

    def get_headerurl(self, response):
        headerurl = response.xpath("//div[@class='profile-user-img-box']//a//img/@src").extract()
        if len(headerurl):
            headerurl = headerurl[0]
        else:
            headerurl = 'Null'
        return headerurl

    def get_images_url(self, response):
        images_url = response.xpath("//div[@class='profile-photo-ul']//a//img/@src").extract()
        if len(images_url):
            images_url = images_url
        else:
            images_url = 'Null'
        return images_url

    def get_content(self, response):
        content = response.xpath("//div[@id='default_profile_inner_init']//span[@id='profile_about']//text()").extract()
        if len(content):
            content = content[0]
        else:
            content = 'Null'
        return content

    def get_fage(self, response):
        fage = response.xpath(
            "//div[@class='profile-box-item']//span[@id = 'profile_match_r_state_id']//text()").extract()
        if len(fage):
            fage = fage[0]
        else:
            fage = 'Null'
        return fage
