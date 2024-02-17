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
    def __init__(self, car_make: str) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        self.car_make = car_make
        self.website = "https://www.otomoto.pl/osobowe"

    def scrape_pages(self, number_of_pages: int) -> List[Car]:
        cars = []
        for i in range(1, number_of_pages + 1):
            current_website = f"{self.website}/{self.car_make}/?page={i}"
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
        offers_table = soup.find("div", class_="ooa-r53y0q ezh3mkl11")
        cars = offers_table.find_all("article")
        links = []
        for car in cars:
            link = (car.find("h1", class_="e1oqyyyi9 ooa-1ed90th er34gjf0").find("a", href=True).get("href"))
            links.append(link)
        for link in links:
            offer_details = scrap_single_offer(link)

        return offer_details

    def scrap_single_offer(self, link):
        response = requests.get(link, headers=self.headers).text
        soup = BeautifulSoup(response, "html.parser")
        table_details = soup.find('div', class_='ooa-1gtr7l5 e18eslyg2')

        brand = table_details.find('a', class_='ooa-162vy3d e18eslyg3').text
        full_name = table_details.find('a', class_='ooa-162vy3d e18eslyg3').text


