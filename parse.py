import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}

session = requests.Session()


def get_response(url):
    response = session.get(url, headers=headers)
    return response


def recursion(lis, breadcrumb):
    # submenu = li.find_all("li")

    lis = []

    # print("ppp", (lis.a.get("href"), breadcrumb))

    for li in lis:

        print("*" * 100)

        breadcrumbs = f"{breadcrumb} > {str(li.text).encode('l1').decode()}"
        link = li.find("a").get("href")

        print(link, breadcrumbs)

        # lis.append((link, breadcrumbs))

        print("*" * 100)

        if "dropdown" in li.get("class"):
            list_data = recursion(li, breadcrumbs)
            # lis.extend(list_data)

    # return lis


def obtain_nesting(response):
    soup = BeautifulSoup(response.text, "lxml")
    menu = soup.find("ul", {"id": "menu-katalog"}).find_all("li", {"class": "menu-item"})

    lis = []

    for li in menu:

        if "dropdown" in li.get("class"):

            print("_" * 100)

            breadcrumbs = "Главная"

            breadcrumbs += f" > {str(li.text).encode('l1').decode()}"
            link = li.a.get("href")

            lis.append((link, breadcrumbs))

            # print(link, breadcrumbs)

            recursion(li, breadcrumbs)

            print("_" * 100)

        else:

            breadcrumbs = "Главная"

            breadcrumbs += f" > {str(li.text).encode('l1').decode()}"
            link = li.a.get("href")

            print(link, breadcrumbs)

            print("=" * 100)

    #         list_links.append((link, breadcrumbs))
    #
    # print(list_links)


def get_links(response):
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find("ul", {"id": "menu-katalog"}).find_all("a")
    list_links = []
    for e, link in enumerate(links, 1):
        print(e, link.get("href"), str(link.text).encode('l1').decode())
        list_links.append((link.get("href"), str(link.text).encode('l1').decode()))

    return list_links


def collect_data(link):
    """Собрать данные с карты сайта о товаре"""
    response = get_response(link)

    soup = BeautifulSoup(response.text, "lxml")
    urls_and_images = []

    for url in soup.find_all("url"):

        if not url.find("image:loc"):
            continue

        links_images = [image.text for image in url.find_all("image:loc")]
        url_and_image = url.loc.text, links_images
        urls_and_images.append(url_and_image)

    return urls_and_images


def collect_page_data(urls_images):
    """Собрать данные с страницы str(link.text).encode('l1').decode()"""
    # for url_image in urls_images:
    response = get_response("https://www.telemagazin.by/product/urna-s-ershikom/")
    # response = get_response(url_image[0])
    soup = BeautifulSoup(response.text, "lxml")


    try:
        number = soup.find("div", {"itemprop": "offers"}).find("p", {"class": "price"})

        if number.ins:
            number = number.ins.text.split()[0]
        else:
            number = number.text.split()[0]

        price = number
    except:
        price = ""


    try:
        number = soup.find("div", {"itemprop": "offers"}).find("p", {"class": "price"})

        crossed_price = number.find("del").text.split()[0]
    except:
        crossed_price = ""


    try:
        stock = soup.find("p", {"class": "stock out-of-stock"})
        stock = str(stock.span.text).encode('l1').decode()
    except:
        stock = ""


    try:
        description = soup.find("div", {"class": "woo-short-description"})
        description = str(description).encode('l1').decode()
    except:
        description = ""


    try:
        content = soup.find("div", {"id": "tab-description"})
        content = str(content).encode('l1').decode()
    except:
        content = ""


    try:
        title = soup.find("h1")
        title = str(title.text).encode('l1').decode()
    except:
        title = ""


    try:
        crumb = soup.find("div", {"class": "crumb-flex"}).find_all("a")
        print(crumb)
    except:
        title = ""


    # print(url_image[0], url_image[1], price, stock, description, content, title)
    # print(price, crossed_price, stock, description, content, title)




def main():
    url = "https://www.telemagazin.by/"
    sitemap_links = [f"{url}product-sitemap1.xml", f"{url}product-sitemap2.xml"]

    for link in sitemap_links:
        collection_urls_and_images = collect_data(link)
        collect_page_data(collection_urls_and_images)
        break


if __name__ == '__main__':
    main()
