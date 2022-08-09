import io
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import hashlib
from urllib.parse import unquote

from PIL import Image
naver_css=[
'img_attachedfile', 'se_mediaImage'
]

def fetch_image_urls(wd: webdriver,site: str, q: str, m: str = '', sleep_between_interactions: float = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        # build the google query
    if site == 'sbs':
        search_url = f"https://programs.sbs.co.kr/enter/gayo/visualboard/{m}?cmd=view&board_no={q}"
        css_class = 'aba_img'
    elif site == 'naver':
        search_url = f"https://m.post.naver.com/viewer/postView.naver?volumeNo={q}&memberNo={m}"
        css_class = naver_css
    elif site == 'gfycat':
        search_url = q
        css_class = 'image media'


    # load the page
    wd.get(search_url)
    time.sleep(sleep_between_interactions)
    image_urls = set()

    scroll_to_end(wd)
    page = wd.page_source
    soup = BeautifulSoup(page, 'html.parser')
    for item in soup.findAll(attrs={'class': css_class}):
        if site == 'naver':
            image_urls.add(item.get('src')[:-11])
        else:
            image_urls.add(item.get('src'))
    return image_urls


def persist_image(folder_path: str, url: str, q: str, type: str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        url = unquote(url)
        file_path = os.path.join(folder_path, q + '_' + url.split('/')[-1][:-4] + type)
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=100)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(site: str, q: str, m: str, driver_path: str, target_path='E:/images', number_images=5,
                        type: str = '.jpg'):
    target_folder = target_path

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(wd=wd, site=site, q=q, m=m, sleep_between_interactions=20)

    for elem in res:
        persist_image(target_folder, elem, q, type)

site = 'sbs'

if site == 'sbs':
    for n in range(439773, 439779):
        if n not in [439737]:
            search_and_download(site, str(n), '54795', 'chromedriver.exe', number_images=100)
else:
    search_and_download(site, '34098471', '16220685', 'chromedriver.exe', number_images=100)