import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
}


def get_response(url):
    response = requests.get(url, headers=headers)
    return response


def recursion(li):
    submenu = li.find("ul", {"class": "dropdown-submenu"}).find_all("li", {"class": "menu-item"})

    breadcrumbs = []

    for li in submenu:

        if not li.ul:
            breadcrumb = str(li.text).encode('l1').decode()

            breadcrumbs.append(breadcrumb)

            return li.a.get("href"), " > ".join(breadcrumbs)

        else:
            # breadcrumbs.append(recursion(li))
            recursion(li)

    # print(breadcrumbs)
    # return link, breadcrumbs


def obtain_nesting(response):
    soup = BeautifulSoup(response.text, "lxml")
    menu = soup.find("ul", {"id": "menu-katalog"}).find_all("li", {"class": "menu-item"})

    list_links = []

    breadcrumbs = "Главная"

    for li in menu:

        if li.ul:
            # link, breadcrumb = recursion(li)
            # breadcrumbs.append(breadcrumb)
            #
            # list_links.append((link, " > ".join(breadcrumbs)))
            # list_links.append((li.a.get("href"), " > ".join(breadcrumbs)))

            # print({str(li.ul.text).encode('l1').decode()})
            print("_"*100)
            #
            # text = f"{text} > {str(li.text).encode('l1').decode()}"
            # obtain_nesting(response, text)

        else:

            breadcrumbs = "Главная"

            # breadcrumb = str(li.text).encode('l1').decode()
            #
            # breadcrumbs.append(breadcrumb)

            breadcrumbs += f" > {str(li.text).encode('l1').decode()}"
            link = li.a.get("href")

            print(link, breadcrumbs)

            list_links.append((link, breadcrumbs))

    print(list_links)


def get_links(response):
    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find("ul", {"id": "menu-katalog"}).find_all("a")
    list_links = []
    for e, link in enumerate(links, 1):
        print(e, link.get("href"), str(link.text).encode('l1').decode())
        list_links.append((link.get("href"), str(link.text).encode('l1').decode()))

    return list_links


def main():
    url = "https://www.telemagazin.by/"

    response = get_response(url)

    # list_links = get_links(response)

    # print(list_links)

    obtain_nesting(response)


if __name__ == '__main__':
    main()
