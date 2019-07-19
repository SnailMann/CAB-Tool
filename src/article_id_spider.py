import requests
import re
from bs4 import BeautifulSoup
import math
import urllib3

"""
Auther : SnailMann
"""


class ArticleIdSpider:

    def getArticleId(self, home_url, page_url):
        """
        Public method
        Get id of all article in blog
        :param home_url:
        :param page_url:
        :return:
        """
        pagesize = self._fetch_pagesize(home_url)
        all_ids = []
        if not pagesize:  # That means there are no articles.
            print('No blog articles, pagesize : ' + str(pagesize))
            return

        for i in range(1, pagesize + 1):
            html = self._fetch_content(page_url + str(i))
            article_ids = self._analysis(html)
            article_ids = article_ids[1:]
            all_ids += article_ids

        return all_ids

    def _fetch_content(self, url):
        """
        Get website response
        :param url:
        :return:
        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        res = requests.get(url, verify=False)
        html = res.text
        return html

    def _analysis(self, html):
        """
        Parsing HTML and return article ids
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, "html.parser")  # get html
        soup.find_all('div', 'article-list')
        article_list = soup.find_all('div', 'article-item-box csdn-tracking-statistics')
        article_nums = [re.findall(r'data-articleid="(\d*)"', repr(article))[0] for article in article_list]
        return article_nums

    def _fetch_pagesize(self, url):
        """
        Get the total page number of  user's blog
        :param url:
        :return:
        """
        pagesize = 0  # total page size

        # crawl all script scripts
        homepage_html = self._fetch_content(url)
        soup = BeautifulSoup(homepage_html, 'html.parser')
        scripts = soup.find_all('script')

        for script_content in scripts:
            # size of per page
            pre_pagesize = re.findall(r'pageSize = (\d*)', repr(script_content))
            # total number of articles
            total_size = re.findall(r'listTotal = (\d*)', repr(script_content))
            if pre_pagesize and total_size:
                # math.ceil
                pagesize = math.ceil(int(total_size[0]) / int(pre_pagesize[0]))
                break
        return pagesize
