# -*- coding: utf-8 -*-
import os
import scrapy
import logging

from booking.items import BookingItem
from booking.Export_CSV_direct import Export_csv


class BkSpider(scrapy.Spider):
    name = 'booking_spider'
    Current_Directory = os.path.dirname(os.path.abspath(__file__))
    allowed_domains = ['booking.com']

    def start_requests(self):
        lines = [line.rstrip('\n') for line in open('Input.txt', 'r')]
        urls = lines
        for url in urls:
            self.Current_page = 1
            yield scrapy.FormRequest(url, callback=self.main_page)

    def main_page(self, response):
        try:
            Total_page_list = response.xpath(
                '//li[@class="bui-pagination__item sr_pagination_item"]/a/text()').extract()
            Total_page = Total_page_list[-1]
            div = response.xpath('//div[@id="hotellist_inner"]/div/table')
            for data1 in div:
                link = 'https://www.booking.com' + str(data1.xpath('.//tbody/tr/td/h3/a/@href').extract_first().strip())
                link = link.replace('\n', '')
                # print link
                hotel_name = response.xpath('.//tbody/tr/td/h3/a/span/text()').extract_first()
                if hotel_name != None:
                    hotel_name = hotel_name.strip()
                yield scrapy.FormRequest(link, callback=self.data_page, meta={'hotel_name': hotel_name, 'link': link})

            last_page = True
            if self.Current_page == Total_page:
                last_page = False
            if last_page == True:
                next_page_id = ''
                li = response.xpath('//li[@class="bui-pagination__pages"]/ul/li/@class').extract()
                for data in range(len(li)):
                    if li[data] == 'bui-pagination__item bui-pagination__item--active sr_pagination_item current':
                        next_page_id = data + 1

                li1 = response.xpath('//li[@class="bui-pagination__pages"]/ul/li' + '[' + str(
                    next_page_id + 1) + ']/a/@href').extract_first()
                next_page_link = li1
                self.Current_page = self.Current_page + 1
                yield scrapy.FormRequest(next_page_link, callback=self.parse)
        except Exception as e:
            logging.log(logging.ERROR, e)

    def data_page(self, response):
        item = BookingItem()
        try:
            try:
                Hotel_name = ''
                Hotel_name = response.xpath('//h2[@id="hp_hotel_name"]/text()').extract_first()
                if Hotel_name != None:
                    Hotel_name = Hotel_name.strip()
            except Exception as e:
                logging.log(logging.ERROR, e)
            Hotel_address = response.xpath('//span[@data-node_tt_id="location_score_tooltip"]/text()').extract_first()
            if Hotel_address != None:
                Hotel_address = Hotel_address.strip()
            Hotel_stars = response.xpath(
                '//span[@class="hp__hotel_ratings__stars nowrap"]/i/span/text()').extract_first()
            if Hotel_stars != None:
                Hotel_stars = Hotel_stars.strip()
            Hotel_image = response.xpath('//img[@alt="Gallery image of this property"]/@src').extract_first()
            Hotel_desciption_bunch = response.xpath('//div[@id="summary"]/p/text()').extract()
            Hotel_desciption = ''.join(Hotel_desciption_bunch)
            Hotel_desciption = Hotel_desciption.replace('\n', '')
            Hotel_facility_bunch1 = []

            Hotel_f_bunch = response.xpath('//div[@class="hotel_description_wrapper_exp hp-description"]')
            Hotel_facility_bunch = Hotel_f_bunch.xpath(
                './/div[@class="hp_desc_important_facilities clearfix "]/div/text()').extract()
            for i in Hotel_facility_bunch:
                hh = i.strip()
                if hh != '':
                    Hotel_facility_bunch1.append(hh)
            Hotel_facility = ' | '.join(Hotel_facility_bunch1)

            try:
                Hotel_review_No = ''
                Hotel_review_No_bunch = response.xpath(
                    '//a[@class="hp_nav_reviews_link toggle_review track_review_link_zh"]/span').re(r'</strong>(.+?)\n')
                Hotel_review_No = Hotel_review_No_bunch[0].strip()

            except Exception as e:
                logging.log(logging.ERROR, e)
            Hotel_review_Score = response.xpath('//div[@class="bui-review-score__badge"]/text()').extract_first()
            if Hotel_review_Score != None:
                Hotel_review_Score = Hotel_review_Score.strip()

            item['Hotel_name'] = Hotel_name
            item['Hotel_address'] = Hotel_address
            item['Hotel_stars'] = Hotel_stars
            item['Hotel_image'] = Hotel_image
            item['Hotel_desciption'] = Hotel_desciption
            item['Hotel_facility'] = Hotel_facility
            item['Hotel_review_No'] = Hotel_review_No
            item['Hotel_review_Score'] = Hotel_review_Score
            yield item
            Export_csv(self.Current_Directory)

        except Exception as e:
            logging.log(logging.ERROR, e)
