import time

from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from pywebcopy import save_webpage

def get_all_links(url, deph, deph_counter=0):
    all_links = {url}

    if deph_counter < deph:
        try:
            req = get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
        except:
            print(f"С сайтом ({url}) какие-то проблемы. Ухожу в сон на 5 секунд...")
            time.sleep(5)
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
                        all_links = all_links.union(get_all_links(link, deph, deph_counter+1))
                    elif link == "/":
                        continue
                    else:
                        url = urlparse(url).scheme + "://" + urlparse(url).netloc
                        all_links = all_links.union(get_all_links(url+link, deph, deph_counter+1))
            except:
                print(link)

    return all_links

def save_page(url):
    dir_name = unquote(urlparse(url).netloc + urlparse(url).path)
    for char in ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]:
        dir_name = dir_name.replace(char, "!")

    try:
        save_webpage(
            url=url,
            project_folder="sites/",
            project_name=str(dir_name),
            open_in_browser=False,
            threaded=True
        )
    except:
        print(" ! Не удалось скачать:", dir_name, url)
        return

if __name__ == '__main__':
    start_url = "https://habr.com/ru/articles/669766/"

    links = get_all_links(start_url, 0)

    print(len(links))
    for link in links:
        save_page(link)
