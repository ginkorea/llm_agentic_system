from workbench.geotext import GeoText
from workbench.location import Location
from workbench.dataloader import DataLoader
from workbench.countryinfo import CountryInfo
from workbench.city import City

if __name__ == "__main__":
    # Example usage of the GeoText library
    geo_text = GeoText()
    locations = geo_text.extractCitiesAndCountries("Sample text with city and country names")
    filtered_locations = geo_text.filterByCountryCode(locations, "US")
    country_count = geo_text.countCountryMentions("Sample text with country mentions")