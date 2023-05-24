dataCol = ['datetime', 'lux', 'cct', 'cri', 'triX', 'triY', 'triZ', 'uvi', 'uva', 'uvb', 'swr', 'mwr', 'narr']


class NaturalLight:
    def __init__(self, date, sunrise, sunset, nearSeasonName, startLwstCct, endLwstCct,dataList, diffRateCCT50_All):
        self.date = date
        self.sunrise = sunrise
        self.sunset = sunset
        self.nearSeasonName = nearSeasonName
        self.dataList = dataList
        self.startLwstCct = startLwstCct
        self.endLwstCct = endLwstCct
        self.diffRateCCT50_All = diffRateCCT50_All

        # time이 키인 딕셔너리
        self.timeData = {}
        self.sortDataList()

    def sortDataList(self):
        for l in self.dataList:
            element = []
            for c in dataCol:
                element.append(l[c])
            day = NaturalLightTime(element)
            self.timeData[day.datetime] = day.getElementsByDic()
            # self.timeData.append(day.getAll())


class NaturalLightTime:
    def __init__(self, day):
        self.datetime = str(day[0]).split()[1]
        self.lux = day[1]
        self.cct = day[2]
        self.cri = day[3]
        self.triX = day[4]
        self.triY = day[5]
        self.triZ = day[6]
        self.uvi = day[7]
        self.uva = day[8]
        self.uvb = day[9]
        self.swr = day[10]
        self.mwr = day[11]
        self.narr = day[12]

    def getAll(self):
        return [self.datetime, self.lux, self.cct, self.cri, self.triX, self.triY, self.triZ, self.uvi, self.uva,
                self.uvb, self.swr, self.mwr]

    def getElements(self):
        return [self.lux, self.cct, self.cri, self.triX, self.triY, self.triZ, self.uvi, self.uva, self.uvb, self.swr,
                self.mwr]

    def getElementsByDic(self):
        elements = {
            'lux': self.lux,
            'cct': self.cct,
            'cri': self.cri,
            'triX': self.triX,
            'triY': self.triY,
            'triZ': self.triZ,
            'uvi': self.uvi,
            'uva': self.uva,
            'uvb': self.uvb,
            'swr': self.swr,
            'mwr': self.mwr,
            'narr': self.narr
        }
        return elements
