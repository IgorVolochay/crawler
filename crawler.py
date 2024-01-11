from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_all_links(url, deph, deph_counter=0):
    all_links = {url}

    if deph_counter < deph:
        try:
            req = get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
        except:
            return

        for link in soup.find_all('a'):
            link = link.get('href')
            try:
                if link:
                    if "http" in link:
                        all_links = all_links.union(get_all_links(link, deph, deph_counter + 1))
                    elif link == "/":
                        continue
                    else:
                        url = urlparse(url).scheme + "://" + urlparse(url).netloc
                        all_links = all_links.union(get_all_links(url + link, deph, deph_counter + 1))
            except:
                print(link)

    return all_links

 
if __name__ == '__main__':
    start_url = "https://habr.com/ru/articles/669766/"

    links = get_all_links(start_url, 1)
    print(len(links))
    print(*list(links)[-5:], sep="\n")
