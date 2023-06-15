import hashlib

import requests
import hmac
# import secrets
from datetime import datetime, timedelta
import uuid
import base64
import json
from openpyxl import Workbook
import time

import NaturalLight
import readExel_to_write_by_minutes
import save_MongoDB

import NaturlaLight_IRD

ADMIN_KEY_SECRETE = '*****'
ADMIN_KEY_ACCESS = '*****'
url = '*******/'

# 데이터 저장할 엑셀 파일 이름
file_name = 'solar term_test'


def setDuration(start_day, end_day):
    start = datetime.strptime(start_day, "%Y-%m-%d")
    end = datetime.strptime(end_day, "%Y-%m-%d")
    diff = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return diff


def DatetimeToTimestamp(dt):  # datetime -> timestapm
    # 서버와 현재 시간과 맞추기 위햐 9시간 더함
    float_ts = datetime.timestamp((dt + timedelta(hours=9)))
    long_ts = int(float_ts * 1000)
    # print('timestamp: ' + str(long_ts))

    return long_ts


def TimestampToDatetime(ts):  # timestapm -> datetime
    # 서버와 현재 시간과 맞추기 위햐 9시간 뺀다
    dt = datetime.fromtimestamp(ts / 1000) - timedelta(hours=9)
    return dt


def getSignature(timestamp, nonce):
    # hash_string = ''
    payload = str(timestamp) + '&' + nonce

    payload_bytes = payload.encode('utf-8')
    hash_byte = hmac.new(ADMIN_KEY_SECRETE.encode('ascii'), payload_bytes, hashlib.sha256).digest()
    hash_string = base64.b64encode(hash_byte)

    return hash_string


def setHeaders():
    # timestamp 생성 - 현재 시간 기준
    now = datetime.now()
    timestamp = DatetimeToTimestamp(now)

    # nonce 생성
    # nonce = secrets.token_hex(16)  # (16바이트) 16진수 secure random number 생성
    nonce = str(uuid.uuid4())
    print("nonce: " + nonce)

    # signature 생성
    signature = getSignature(timestamp, nonce)
    print("signature: " + signature.decode('ascii'))

    headers = {
        'timestamp': str(timestamp),
        'nonce': nonce,
        'accessKey': ADMIN_KEY_ACCESS,
        'signature': signature
    }

    return headers


def toExcel_by_solar_term(res):
    # file_name 엑셀
    #   info 시트 에는
    #       열: ['date','sunrise','sunset','nearSeasonName', 'startLwstCct', 'endLwstCct']
    #       행: 조회한 날짜별 데이터
    #
    #   조회한 날짜의 시트
    #       열: ['datetime', 'lux', 'cct', 'cri', 'tirX', 'triY', 'triZ','uvi', 'uva', 'uvb', 'swr', 'mwr']
    #       행: 일출 시간 부터 일몰 시간 까지 측정된 시간의 데이터
    #
    # file_name + _by_minute
    #   조회한 날짜의 시트
    #       열: ['datetime', 'lux', 'cct', 'cri', 'tirX', 'triY', 'triZ','uvi', 'uva', 'uvb', 'swr', 'mwr']
    #       행: 일출 시간 부터 일몰 시간 까지 1분 마다의 측정 데이터(if 해당 시간에 데이터가 없다면 빈 셀)

    write_wb = Workbook()

    # info sheet 지정
    sheet_info = write_wb["Sheet"]
    # info sheet 열 이름 저장
    sheet_info.append(['date', 'sunrise', 'sunset', 'nearSeasonName', 'startLwstCct', 'endLwstCct'])

    for d in res.keys():  # 날짜 별 반복

        # info sheet 지정 날짜 마다의 데이터 저장
        sheet_info.append([res[d].date, TimestampToDatetime(res[d].sunrise), TimestampToDatetime(res[d].sunset),
                           res[d].nearSeasonName, TimestampToDatetime(res[d].startLwstCct),
                           TimestampToDatetime(res[d].endLwstCct)])

        # cols = ['datetime', 'lux', 'cct', 'cri', 'tirX', 'triY', 'triZ','uvi', 'uva', 'uvb', 'swr', 'mwr']
        cols = []

        # 저정 날짜 시트 생성
        sheet = write_wb.create_sheet(title=d)

        for t in res[d].timeData.keys():
            if len(cols) == 0:
                for k in res[d].timeData[t].keys():
                    cols.append(k)
                colName = ['datetime']
                colName.extend(cols)
                sheet.append(colName)
            data = [d + " " + t]
            for c in cols:
                data.append(res[d].timeData[t][c])
            sheet.append(data)

    # write_wb.remove_sheet(write_wb['Sheet']) #시트 제거[시트 이름]
    write_wb.save(file_name + '.xlsx')

    # 일출 시감부터 일몰시간 까지 분단위로 데이터 정리(해당 분에 데이터가 없다면 빈 셀로 처리)
    readExel_to_write_by_minutes.readExel_to_write_by_minutes(file_name)


if __name__ == '__main__':

    # #기간 설정
    # start_day = '2020-01-01'
    # end_day = '2020-12-31'
    # dates = setDuration(start_day, end_day)

    # 원하는 날짜만
    # dates = ['2022-02-10', '2021-02-21', '2022-02-27', '2020-03-20', '2022-04-04', '2021-04-19', '2021-05-09', '2022-05-28', '2019-06-03', '2019-06-24', '2018-07-15','2021-07-21', '2018-08-01', '2018-08-17','2021-09-11', '2019-09-18', '2020-10-08', '2021-10-17', '2020-11-12', '2021-11-27','2021-12-05', '2021-12-22', '2021-01-08', '2022-01-20']
    # dates = ['2022-02-10', '2022-02-23', '2022-03-03', '2022-03-22', '2022-04-04', '2021-04-19']
    dates = ['2022-04-04']

    data = {'dateList': dates}
    data_json = json.dumps(data).encode('utf-8')

    headers = setHeaders()
    response = requests.get(url + 'find/daily', headers=headers, data=data_json)

    natural = {}
    for res in response.json():
        natural[res['date']] = NaturalLight.NaturalLight(res['date'], res['sunrise'], res['sunset'],
                                                         res['nearSeasonName'], res['startLwstCct'], res['endLwstCct'],
                                                         res['dataList'], res['diffRateCCT50_All'])


    # print(natural['YYYY-mm-dd'].timeData['HH:MM:SS']['lux'])
    # print(natural['YYYY-mm-dd'].sunset)

    # #절기별 데이터 엑셀 정리
    # toExcel_by_solar_term(natural)

    # # 몽고 DB에 저장
    # save_MongoDB.save_MongoDB(natural)

    # # #ird 받기
    # # datatimeList = ['2022-02-10 08:04:18', '2022-02-10 17:34:33']
    # datatimeList = ['2022-01-20 17:17:02']
    # startWavelength = 380
    # endWavelength = 780
    # intervalWavelength = 1
    #
    # natural_ird = {}
    #
    # for dt_str in datatimeList:
    #     headers = setHeaders()
    #
    #     dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    #     ts = DatetimeToTimestamp(dt)
    #     data = {
    #         'timestamp': ts,
    #         'datetime': dt_str,
    #         'startWavelength': startWavelength,
    #         'endWavelength': endWavelength
    #     }
    #     data_json = json.dumps(data).encode('utf-8')
    #     response = requests.get(url + 'find/wavelength', headers=headers, data=data_json)
    #     res = response.json()
    #
    #     print(res['datetime'])
    #     natural_ird[dt_str] = NaturlaLight_IRD.NaturalLight_IRD(res['datetime'], res['startWavelength'], res['endWavelength'], intervalWavelength, res['wavelength'])
