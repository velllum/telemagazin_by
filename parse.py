import csv
import os
import sys

import requests
from bs4 import BeautifulSoup

base_path = os.path.abspath(os.path.dirname(__file__))

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}

session = requests.Session()


def get_response(url, stream=False):
    response = session.get(url, headers=headers, stream=stream)
    return response


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


def save_data_csv_files(list_dicts):
    """Сохранение данных в файл CSV"""
    with open('products_data.csv', 'a', encoding='utf-8', newline='') as csv_file:
        list_key = list_dicts[0].keys()
        print(list_key)
        dict_writer = csv.DictWriter(csv_file, list_key)
        dict_writer.writeheader()
        dict_writer.writerows(list_dicts)


def save_images(urls_images):
    """сохранение файла, по пути указанной в ссылке"""
    list_images = [im for _, images in urls_images for im in images]
    for image in list_images:
        list_element = str(image).rsplit("/", 1)

        file_name = list_element[-1]
        path_files = list_element[0].split("/", 4)[-1]

        full_path_files = os.path.join(base_path, path_files)

        try:
            os.makedirs(full_path_files)
        except OSError:
            pass

        print(list_element, path_files, file_name)

        response = get_response(image, stream=True)
        with open(os.path.join(full_path_files, file_name), 'wb') as fd:
            for chunk in response.iter_content(chunk_size=1024):
                fd.write(chunk)


def collect_page_data(urls_images):
    """Собрать данные с страницы"""
    list_dicts = []
    for enum, url_image in enumerate(urls_images):
        response = get_response(url_image[0])
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
            if content:
                content = str(content).encode('l1').decode()
            else:
                content = ""
        except:
            content = ""

        try:
            title = soup.find("h1")
            title = str(title.text).encode('l1').decode()
        except:
            title = ""

        try:
            category = soup.find("div", {"class": "crumb-flex"}).find_all("a")
            links = [crumb.get("href") for crumb in category]
            list_breadcrumbs = []

            for link in links:
                response = get_response(link)
                soup = BeautifulSoup(response.text, "lxml")
                breadcrumbs = soup.find("nav", {"class": "breadcrumbs"}).find_all("span", {"itemprop": "title"})
                list_breadcrumbs.append(
                    " > ".join([str(breadcrumb.text).encode('l1').decode() for breadcrumb in breadcrumbs]))
            categories = ", ".join(list_breadcrumbs)
        except:
            categories = ""

        data_dict = dict(
            price=price,
            crossed_price=crossed_price,
            stock=stock,
            description=description,
            content=content,
            title=title,
            categories=categories,
            image=", ".join(url_image[1]),
        )

        print(enum, url_image[0], data_dict)

        list_dicts.append(data_dict)

    return list_dicts



def main():
    url = "https://www.telemagazin.by/"
    sitemap_links = [f"{url}product-sitemap1.xml", f"{url}product-sitemap2.xml"]

    for link in sitemap_links:
        collection_urls_and_images = collect_data(link)
        save_images(collection_urls_and_images)
        list_dicts = collect_page_data(collection_urls_and_images)
        save_data_csv_files(list_dicts)


if __name__ == '__main__':
    main()
