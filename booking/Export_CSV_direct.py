import os
import os

import MySQLdb
import pandas as pd
import datetime

Current_Directory = os.path.dirname(os.path.abspath(__file__))


def Export_csv(HtmlDirectory):
    Current_Directory = os.path.dirname(os.path.abspath(__file__))

    DB_IP = "localhost"
    DB_user = "root"
    DB_password = "root"
    DB_name = "Booking_data"
    db = MySQLdb.connect(DB_IP, DB_user, DB_password, DB_name)
    cursor = db.cursor()

    HTML_Path_1 = 'Booking_data_Temp.csv'
    HTML_Path_2 = 'Booking_data.csv'
    sql = "Select Hotel_name,Hotel_address,Hotel_stars,Hotel_image,Hotel_desciption,Hotel_facility,Hotel_review_No,Hotel_review_Score,Ingestion_timestamp from Booking_data"
    cursor.execute(sql)
    results = cursor.fetchall()
    df = pd.read_sql(sql, db)
    df.to_csv(HTML_Path_1, index=False, sep=',', quoting=0)

    with open(HTML_Path_1, 'r') as f:
        with open(HTML_Path_2, 'w') as f1:
            f.next()  # skip header line
            f1.write(
                'Hotel_name,Hotel_address,Hotel_stars,Hotel_image,Hotel_desciption,Hotel_facility,Hotel_review_No,Hotel_review_Score,Download_Time')
            f1.write("\n")
            for line in f:
                f1.write(line)

    os.remove(HTML_Path_1)
