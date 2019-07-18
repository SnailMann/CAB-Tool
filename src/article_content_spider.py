import os
import re
import uuid
import requests
import urllib3


class ArticleContentSpider:
    count = 0

    def getArticle(self, download_path, article_url, article_ids, cookies):
        """
        Get article content
        :param url:
        :param article_ids:
        :param cookies:
        :return:
        """
        self._mkdir(download_path)  # mkdir backup directory
        for id in article_ids:
            # time.sleep(1)
            article = self._get_markdown(article_url, id, cookies)
            self._download(download_path, article)

    def _get_markdown(self, article_url, id, cookies):
        """
        Get article data from markdown editor
        https://mp.csdn.net/mdeditor/getArticle?id=

        :param article_url:
        :param id:
        :param cookies:
        :return:
        """
        login_url = article_url + id  # assembling
        headers = {  # request headers
            'Host': 'mp.csdn.net',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        res = requests.get(login_url, headers=headers, verify=False, cookies=cookies)
        res.raise_for_status()
        res.encoding = 'utf-8'
        article = res.json()
        return article['data']

    def _download(self, download_path, article):
        """
        Download article to local storeage
        :param download_path:
        :param article:
        :return:
        """
        if os.path.exists(download_path):
            # get article title and content
            title = article['title']
            markdown = article['markdowncontent']
            html = article['content']

            # check the title
            if not title:
                title = "DEFAULT_TITLE_" + str(uuid.uuid1())[1:8]
            title = self._validate_title(title)

            # download
            self._download_markdown(download_path, title, markdown)
            self._download_html(download_path, title, html)

            ArticleContentSpider.count += 1
            print("[%s] :%s        is Done!!" % (ArticleContentSpider.count, title))

        else:
            print('The path is not exists')

    def _download_markdown(self, path, title, markdown):
        """
        Download the markdown content
        :param path:
        :param title:
        :param markdown:
        :return:
        """
        # check article content
        if not (title and markdown):  # Exclude articles written in HTML
            print('------------------------------------------------------------------------------')
            print('Title:' + title)
            print('No MarkDown Content!!!')
            print('------------------------------------------------------------------------------')
            return

        # write
        path = path + "\\markdown" + "\\" + title + '.md'
        f = open(path, 'w+', encoding="utf8")
        f.write(markdown)
        f.seek(0)
        f.close()

    def _download_html(self, path, title, html):
        """
        Download the html content
        :param path:
        :param title:
        :param html:
        :return:
        """
        # check the content
        if not (title and html):
            print('------------------------------------------------------------------------------')
            print('Title:' + title)
            print('No HTML Content!!!')
            print('------------------------------------------------------------------------------')
            return

        # write
        path = path + "\\html" + "\\" + title + '.html'
        f = open(path, 'w+', encoding="utf8")
        f.write(html)
        f.seek(0)
        f.close()

    def _mkdir(self, download_path):
        """
        mkdir directory
        :param download_path:
        :return:
        """
        html_path = download_path + '\\' + 'html'
        markdown_path = download_path + '\\' + 'markdown'

        # create father directory
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            print('The directory has been created :' + download_path)

        # create son directory (html, markdown)
        if not os.path.exists(html_path):
            os.makedirs(html_path)
            print('The directory has been created :' + html_path)
        if not os.path.exists(markdown_path):
            os.makedirs(markdown_path)
            print('The directory has been created :' + markdown_path)

    def _validate_title(self, title):
        """
        Replace windows illegal characters from file names
        '/ \ : * ? " < > |'
        :return:
        """

        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)
        return new_title
