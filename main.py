from urllib import parse
import requests
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


class VideoCard:
    def __init__(self, model: str):
        self.model: str = model
        self.url: str = str()
        self.price: float = float()
        self.shop: str = str()
        self.title: str = str()

    def search(self):
        card_counter = 0
        for e_shop in E_SHOPS:
            parsed_model = parse.quote(self.model)
            if "morele.net" in e_shop:
                print("Scanning morele.net")
                url = e_shop.replace("__PLACEHOLDER__", parsed_model)
                html = requests.get(url, headers=HEADERS).text
                soup = BeautifulSoup(html, "html.parser")
                cards = soup.find_all('a', class_="productLink")
                card_set = set()
                for card in cards:
                    card_set.add(card)
                for card in card_set:
                    card_counter += 1
                    self.url = f"https://www.morele.net{card.get('href')}"
                    html = requests.get(self.url, headers=HEADERS).text
                    soup = BeautifulSoup(html, "html.parser")
                    self.title = soup.find("h1", class_="prod-name").text.strip()
                    self.price = float(
                        soup.find("div", class_="product-price").text.strip().replace(" ", "").removesuffix(
                            "zł").replace(",", "."))
                    self.shop = "Morele.net"
                    target = VideoCard(self.model)
                    target.price = self.price
                    target.shop = self.shop
                    target.title = self.title
                    target.url = self.url

                    TARGETS.append(target)
                    print(f"Found: {card_counter} cards")


TARGETS: list[VideoCard] = []

if __name__ == '__main__':
    vc = VideoCard("RTX 3050")
    vc.search()
    targets_sorted = sorted(TARGETS, key=lambda x: x.price)
    for index, t in enumerate(targets_sorted):
        print(f"[{index + 1}] {t.price} zł {t.title}")
    error_counter = 0
    while error_counter != 3:
        try:
            number = int(input(">>")) - 1
            chosen_card = targets_sorted[number]
            print("Your card:")
            print(chosen_card.url)
        except ValueError:
            print("This is not a number")
            error_counter += 1
