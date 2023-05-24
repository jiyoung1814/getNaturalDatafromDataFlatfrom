import pymongo
import pandas as pd
import time
from datetime import datetime

import crawling_Az_El

db_name = 'naturalLight'
collection_name = ['date','datetime']
mongo_host = "mongodb://localhost:27017/"

dataCol = ['datetime', 'timestamp', 'lux', 'cct', 'cri', 'triX', 'triY', 'triZ', 'uvi', 'uva', 'uvb', 'swr', 'mwr',
           'Az', 'El']

class save_MongoDB:
    def __init__(self, natural):
        self.natural = natural

        # 천정각 고도각 데이터 가져오기
        self.AZ_EL = self.get_AZ_EL_from_excel()

        # DB 연결
        self.db = None
        self.collection_d = None
        self.collection_dt = None
        self.connectMongoDB()

        self.saveData()


    def get_AZ_EL_from_excel(self):
        year = ['2020']
        AZ_EL = {}

        df_AZ_EL = pd.read_excel('2021_2023_04_Az_El.xlsx', sheet_name=None, engine='openpyxl')

        for y in year:
            for i in range(len(df_AZ_EL[y]) - 1):

                date = str(df_AZ_EL[y]['date'][i]).split()[0]
                time = str(df_AZ_EL[y]['time'][i])
                dt = date + " " + time

                az = float(df_AZ_EL[y]['Az'][i])
                el = float(df_AZ_EL[y]['El'][i])
                AZ_EL[dt] = {'Az': az, 'El': el}

        # print(AZ_EL)
        return AZ_EL

    def connectMongoDB(self):
        client = pymongo.MongoClient(mongo_host)
        # print(client.list_database_names())
        self.db = client[db_name] # naturalLight라는 DB가 없으면 생성, 있으면 지정
        self.collection_d = self.db[collection_name[0]] # [] 라는 이름의 collection 에 접속 if 없다면 생성
        self.collection_dt = self.db[collection_name[1]]
        print('connect with mongoDB \'' + db_name+'\'['+collection_name[0] + ', ' + collection_name[1]+']')

    def saveData(self):
        # print(self.AZ_EL.keys())

        for d in self.natural.keys():
            #일별 데이터
            day_data = {
                "date": d,
                'sunrise': self.natural[d].sunrise,
                'sunset': self.natural[d].sunset,
                'nearSeasonName': self.natural[d].nearSeasonName,
                'startLwstCct': self.natural[d].startLwstCct,
                'endLwstCct': self.natural[d].endLwstCct,
                'diffRateCCT50_All': self.natural[d].diffRateCCT50_All,
            }
            self.collection_d.insert_one(day_data)

            #시간별 데이터
            for t in self.natural[d].timeData.keys():
                dt = d+" "+t

                dt_ignore_second = dt[0:len(dt)-2]+"00" #엑셀에 저장된 시간의 초단위는 다 00 임
                if dt_ignore_second in self.AZ_EL.keys(): #엑셀에 해당 시간에 대한 방위각 고도각이 있는 경우
                    az = self.AZ_EL[dt[0:len(dt) - 2] + "00"]['Az']
                    el = self.AZ_EL[dt[0:len(dt)-2] + "00"]['El']
                else: #없는 경우 크롤링
                    az_el = crawling_Az_El.crawling_Az_El(d, t)
                    az = az_el.az
                    el = az_el.el

                data = {
                    'datetime': dt,
                    'timestamp': time.mktime(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timetuple()),
                    'lux': self.natural[d].timeData[t]['lux'],
                    'cct': self.natural[d].timeData[t]['cct'],
                    'triX': self.natural[d].timeData[t]['triX'],
                    'triY': self.natural[d].timeData[t]['triY'],
                    'triZ': self.natural[d].timeData[t]['triZ'],
                    'uvi': self.natural[d].timeData[t]['uvi'],
                    'uva': self.natural[d].timeData[t]['uva'],
                    'uvb': self.natural[d].timeData[t]['uvb'],
                    'swr': self.natural[d].timeData[t]['swr'],
                    'mwr': self.natural[d].timeData[t]['mwr'],
                    'Az': az,
                    'El': el
                }

                print(data)
                self.collection_dt.insert_one(data)

