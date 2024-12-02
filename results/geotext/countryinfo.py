class CountryInfo:
    def __init__(self, iso: str, name: str, capital: str, area: int, population: int, languages: list):
        self.iso = iso
        self.name = name
        self.capital = capital
        self.area = area
        self.population = population
        self.languages = languages