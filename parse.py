import requests
from bs4 import BeautifulSoup

url = "https://www.telemagazin.by/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

links = soup.find("ul", {"id": "menu-katalog"}).find_all("a")

for link in links:
    print(str(link.text).encode('l1').decode())
    print(link.get("href"))


