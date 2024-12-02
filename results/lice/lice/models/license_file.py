class LicenseFile:
    def __init__(self, type, year, org, content):
        self.type = type
        self.year = year
        self.organization = org
        self.content = content

    def saveToFile(self, fileName):
        with open(fileName, 'w') as f:
            f.write(self.content)
        return True