# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookingItem(scrapy.Item):

    Hotel_name = scrapy.Field()
    Hotel_address = scrapy.Field()
    Hotel_stars = scrapy.Field()
    Hotel_image = scrapy.Field()
    Hotel_desciption = scrapy.Field()
    Hotel_facility = scrapy.Field()
    Hotel_review_No = scrapy.Field()
    Hotel_review_Score = scrapy.Field()

    pass
