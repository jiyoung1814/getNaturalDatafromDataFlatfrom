class NaturalLight_IRD:
    def __init__(self, datetime, startWavelength, endWavelength, intervalWavelength , wavelength):
        self.datetime = datetime
        self.startWavelength = startWavelength
        self.endWavelength = endWavelength
        self.intervalWavelength = intervalWavelength
        self.wavelengthList = wavelength

        self.sortWavelength()

    def sortWavelength(self):
        wavelength = self.startWavelength
        IRD = {}

        for intensity in self.wavelengthList:
            IRD[wavelength] = intensity

            wavelength = wavelength + self.intervalWavelength

        print(IRD)