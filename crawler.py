import os
import re
import time
import random
import logging

import requests
from bs4 import BeautifulSoup

from constants import month_dict
from path_setting import log_dir, keyword_dir
from logging_setting import Log
from db_controller import DB_Controller
from linebot_api import LineBot

Log(log_dir).create_logger('main.log')
logger = logging.getLogger('main.log')

class Crawler:
    def __init__(self, board):
        self.board = board
        self.url = f'https://www.ptt.cc/bbs/{board}/index.html'
        self.headers = {
            'cookie': 'over18=1;',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        self.soup = None
        self.db_controller = DB_Controller()
        self.linebot = LineBot()

        with open(os.path.join(keyword_dir, f'{self.board}_keyword.txt'), 'r', encoding='utf-8') as f:
            self.keyword = f.readline().lower()

    def crawl_page(self):
        try:
            res = requests.get(self.url, headers=self.headers)
            self.soup = BeautifulSoup(res.text, 'html.parser')
        except:
            logger.exception(f'While crawling the {self.url}')
            raise
    
    # get the title and insert into the db
    def fetch_title(self):
        rows = self.soup.find_all('div', class_='r-ent')

        for row in rows:
            try:
                title_tag = row.find('div', class_='title')
                title = title_tag.text.strip()
                author = row.find('div', class_='author').text.strip()
                a_tag = title_tag.select_one('a')
                if a_tag is not None:
                    href = a_tag['href']
                    tmp = href.split('/')[-1].split('.')
                    id = (''.join(tmp[:-1])).lower()
                    
                    result = self.db_controller.search_by_id(id)
                    if result.first() is not None:
                        time.sleep(2)
                        continue

                    content_res = requests.get(f'https://www.ptt.cc{href}', headers=self.headers)
                    content_soup = BeautifulSoup(content_res.text, 'html.parser')
                    article = content_soup.find_all('div', class_='article-metaline')
                    post_time_article = article[2]
                    post_time_str = post_time_article.select('span')[1].text
                    post_time_str = post_time_str.split()
                    if len(post_time_str[2]) == 1:
                        post_time_str[2] = f'0{post_time_str[2]}'
                    post_time = f'{post_time_str[4]}{month_dict[post_time_str[1]]}{post_time_str[2]} {post_time_str[3]}'

                    url = f'https://www.ptt.cc{href}'
                    self.db_controller.save_record(id=id, title=title, author=author, url=url, post_time=post_time)

                    if self.keyword in title.lower():
                        self.linebot.push_message((title, url))
                    
                    sec = random.uniform(1.0, 3.0)
                    time.sleep(sec)   
            except:
                logger.exception(f'While fetching the titles')
                continue

    def crawl_pages(self):
        self.crawl_page()
        if self.soup is not None:
            self.fetch_title()

        # Read the page number which the crawler will start to crawl from
        # with open(os.path.join(page_dir, f'{self.board}_page_num.txt'), 'r', encoding='utf-8') as f:
        #     page_num = int(f.readline())
        
        # status_code = self.crawl_page(page_num)
        # while status_code == 200:
        #     self.fetch_title()
        #     page_num += 1
        #     status_code = self.crawl_page(page_num)
        
        # with open(os.path.join(page_dir, f'{self.board}_page_num.txt'), 'w', encoding='utf-8') as f:
        #     f.write(str(page_num))

        # btn_group = self.soup.find('div', class_='btn-group btn-group-paging')
        # prev_page_href = btn_group.select('a')[1]['href']
        # prev_page = prev_page_href.split('/')[-1]
        # prev_page = re.findall('\d+', prev_page)
        # # get previous page number
        # prev_page = int(prev_page[0])

        # crawl the previous pages
        # for i in range(page_count-1):
        #     url = f'{self.url[:-5]}{prev_page-i}.html'
        #     self.crawl_page(url=url)
        #     self.fetch_title()
            

