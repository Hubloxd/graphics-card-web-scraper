from os import system
from dataclasses import dataclass
from urllib import parse
from requests import get
from bs4 import BeautifulSoup

E_SHOPS = [
    "https://www.morele.net/kategoria/karty-graficzne-12/?q=__PLACEHOLDER__",  # MORELE.NET
    "https://www.x-kom.pl/szukaj?q=__PLACEHOLDER__&f%5Bgroups%5D%5B5%5D=1",  # X-KOM

]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/102.0.5005.72 Safari/537.36 ",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9 "
}


@dataclass()
class VideoCard:
    title: str
    url: str
    price: float
    shop: str


TARGETS: list[VideoCard] = list()

if __name__ == '__main__':
    searched_model = input("Model: ")
    parsed_model = parse.quote(searched_model)
    for e_shop in E_SHOPS:
        cards_counter = 0
        url = e_shop.replace("__PLACEHOLDER__", parsed_model)
        html = get(url, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        if "morele.net" in e_shop:
            try:
                shop = "MORELE.NET"
                links = set()
                for card in soup.find_all('a', class_="productLink"):
                    links.add(f"https://www.morele.net{card.get('href')}")
                for link in links:
                    html = get(link, headers=HEADERS).text
                    soup = BeautifulSoup(html, 'html.parser')
                    try:
                        title = soup.find("h1", "prod-name").text.strip()
                        if "Karta graficzna " in title:
                            title = title.removeprefix("Karta graficzna ")
                    except AttributeError:
                        break
                    price_text = soup.find("div", class_="product-price").text.strip()
                    try:
                        price = float(price_text.removesuffix("zł").replace(' ', '').replace(',', '.'))
                    except ValueError:
                        price = 0.0

                    TARGETS.append(VideoCard(title, link, price, shop))
                    cards_counter += 1
                    print(f"FOUND: {cards_counter} cards at {shop}")
            except KeyboardInterrupt:
                print("Skipping morele")
                break
        elif "x-kom.pl" in e_shop:
            pass

    TARGETS = sorted(TARGETS, key=lambda x: x.price)
    for card in TARGETS:
        print(card.title, card.price, card.shop)