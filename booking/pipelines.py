# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from booking.items import BookingItem

class BookingPipeline(object):
    host = 'localhost'
    user = 'root'
    password = 'root'
    DB_name = "Booking_data"

    def __init__(self):
        try:
            self.connection = MySQLdb.connect(self.host, self.user, self.password, charset='utf8')
            self.cursor = self.connection.cursor()
            self.cursor.execute('CREATE DATABASE ' + self.DB_name)
            self.connection = MySQLdb.connect(self.host, self.user, self.password, self.DB_name, charset='utf8')
            self.cursor = self.connection.cursor()
            strquery2 = "CREATE TABLE Booking_data""""(Id INT NOT NULL AUTO_INCREMENT,
                                                                Hotel_name longtext DEFAULT NULL,
                                                                Hotel_address longtext DEFAULT NULL,
                                                                Hotel_stars longtext DEFAULT NULL,
                                                                Hotel_image longtext DEFAULT NULL,
                                                                Hotel_desciption longtext DEFAULT NULL,
                                                                Hotel_facility longtext DEFAULT NULL,
                                                                Hotel_review_No longtext DEFAULT NULL, 
                                                                Hotel_review_Score longtext DEFAULT NULL,                                                                        
                                                                Ingestion_timestamp timestamp,
                                                                PRIMARY KEY (`Id`))"""

            self.cursor.execute(strquery2)

        except Exception as e:
            print(str(e))

    def process_item(self, item, spider):

        if isinstance(item, BookingItem):

            try:
                self.connection = MySQLdb.connect(self.host, self.user, self.password, self.DB_name, charset='utf8')
                self.cursor = self.connection.cursor()
                self.cursor.execute(
                    """INSERT INTO Booking_data (Hotel_name,Hotel_address,Hotel_stars,Hotel_image,Hotel_desciption,Hotel_facility,Hotel_review_No,Hotel_review_Score)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (item['Hotel_name'], item['Hotel_address'], item['Hotel_stars'], item['Hotel_image'], item['Hotel_desciption'],
                     item['Hotel_facility'], item['Hotel_review_No'], item['Hotel_review_Score']))
                self.connection.commit()
            except Exception as e:
                print(e)
