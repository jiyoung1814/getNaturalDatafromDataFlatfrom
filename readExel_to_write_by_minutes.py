import openpyxl
import pandas as pd
from datetime import datetime, timedelta
from openpyxl import Workbook


def HMS_to_HM(hms):
    return datetime.strftime(datetime.strptime(hms, '%H:%M:%S'), '%H:%M')


def add_a_minute_HM(hms):
    return datetime.strftime(datetime.strptime(hms, '%H:%M') + timedelta(minutes=1), '%H:%M')


class readExel_to_write_by_minutes:

    def __init__(self, file_name):
        read_file_name = file_name

        write_tile_name = read_file_name+'_by_minute.xlsx'
        write_wb = Workbook()
        # sheet = write_wb.active

        # df = pd.read_excel(read_file_name)
        df_sheet_all = pd.read_excel(read_file_name+'.xlsx',
                                     sheet_name=None,
                                     engine='openpyxl')
        # print(df_sheet_all.keys())

        cnt = -1
        # print(df_sheet_all.keys())

        for s in df_sheet_all.keys():
            cnt += 1
            if cnt == 0:
                continue

            print(s)
            sheet = write_wb.create_sheet(title=s)

            df = df_sheet_all[s]

            if len(df.keys()) == 0:
                continue

            colNames = df.keys()
            sheet.append(list(colNames)) #열 이름 시트에 추가
            # print(s)
            # print(df['datetime'])

            start = HMS_to_HM(df['datetime'][0].split()[1])
            end = HMS_to_HM(df['datetime'][len(df['datetime']) - 1].split()[1])

            cnt = 0
            time = start
            while True:
                measurement_time = HMS_to_HM(df['datetime'][cnt].split()[1])

                rows = []
                if measurement_time == time:
                    for c in colNames:
                        rows.append(df[c][cnt])

                    cnt += 1
                else:
                    rows.append(df['datetime'][cnt])

                sheet.append(rows)

                if end == measurement_time:
                    break

                time = add_a_minute_HM(time)

        print(write_tile_name)
        write_wb.save(write_tile_name)
