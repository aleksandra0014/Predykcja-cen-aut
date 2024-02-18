from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from typing import List


@dataclass
class Car:
    brand: str
    full_name: str
    year: int
    mileage_km: str
    engine_capacity: str
    fuel_type: str
    price_pln: int
    colour: str
    type: str
    gear_box: str
    num_place: int
    num_doors: int
    condition: str


class Scraper:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        self.website = "https://www.otomoto.pl/osobowe"

    def scrape_pages(self, number_of_pages: int) -> List[Car]:
        cars = []
        for i in range(1, number_of_pages + 1):
            current_website = f"{self.website}?page={i}"
            new_cars = self.scrape_cars_from_current_page(current_website)
            if new_cars:
                cars.extend(new_cars)
        return cars

    def scrape_cars_from_current_page(self, current_website: str) -> List[Car]:
        try:
            response = requests.get(current_website, headers=self.headers).text
            soup = BeautifulSoup(response, "html.parser")
            cars = self.extract_cars_from_page(soup)
            return cars
        except Exception as e:
            print(f"Problem with scraping website: {current_website}, reason: {e}")
            return []

    def extract_cars_from_page(self, soup: BeautifulSoup):
        try:
            offers_table = soup.find("div", class_="ooa-r53y0q ezh3mkl11")
            cars = offers_table.find_all("article", class_="ooa-yca59n")
            links = []
            list_of_cars = []
            for car in cars:
                link = car.find("h1", class_="e1oqyyyi9 ooa-1ed90th er34gjf0").find('a').get('href')
                links.append(link)
            for link in links:
                offer_details = self.scrap_single_offer(link)
                list_of_cars.append(offer_details)
            return list_of_cars
        except Exception as e:
            print(f"Problem with scraping cars, reason: {e}")
            return []

    def scrap_single_offer(self, link):
        try:
            response = requests.get(link, headers=self.headers).text
            soup = BeautifulSoup(response, "html.parser")
            divs = soup.findAll('div',  {"data-testid": "advert-details-item"})
            one_car_details = []
            for div in divs:
                dic = {}
                item = div.find('p', class_='e18eslyg4').get_text(strip=True)
                if div.find('a') is not None:
                    link = div.find('a').get_text(strip=True)
                    dic[item] = link
                if div.find('p', class_='e16lfxpc0') is not None:
                    paragraph = div.find('p', class_='e16lfxpc0').get_text(strip=True)
                    dic[item] = paragraph
                one_car_details.append(dic)
            return one_car_details
        except Exception as e:
            print(f"Problem with scraping website, reason: {e}")
            return []


sc = Scraper()
lista = sc.scrape_pages(1)
for i in lista[:3]:
    print(i)