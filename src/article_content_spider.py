import os
import re
import time
import uuid
import requests
import urllib3

"""
Auther : SnailMann
"""


class ArticleContentSpider:
    count = 0
    sleep_time = 1  # crawl article interval, the unit is seconds.
    download_img_flag = False  # download img or not?
    download_path = ''  # backup path
    article_url = ''  # url of get article data
    html_path = ''  # backup html path
    markdown_path = ''  # backup markdown path
    img_path = ''  # backup img path

    def getArticle(self, sleep_time, download_path, download_img, article_url, article_ids, cookies):
        """
        Get article content
        :param url:
        :param article_ids:
        :param cookies:
        :return:
        """

        # init
        ArticleContentSpider.sleep_time = sleep_time
        ArticleContentSpider.download_path = download_path
        ArticleContentSpider.article_url = article_url
        ArticleContentSpider.download_img_flag = download_img
        ArticleContentSpider.html_path = download_path + '\\' + 'html'
        ArticleContentSpider.markdown_path = download_path + '\\' + 'markdown'
        ArticleContentSpider.img_path = download_path + '\\' + 'img'

        # mkdir backup directory
        self._mkdir()

        # get article content
        for id in article_ids:
            time.sleep(ArticleContentSpider.sleep_time)  # prevent crawling too fast,you can customize this variable
            article = self._get_markdown(id, cookies)
            self._download(article)

    def _get_markdown(self, id, cookies):
        """
        Get article data from markdown editor
        https://mp.csdn.net/mdeditor/getArticle?id=

        :param article_url:
        :param id:
        :param cookies:
        :return:
        """
        login_url = self.__class__.article_url + id  # assembling
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

    def _download(self, article):
        """
        Download article to local storeage
        :param download_path:
        :param article:
        :return:
        """
        if os.path.exists(self.__class__.download_path):
            # get article title and content
            title = article['title']
            markdown = article['markdowncontent']
            html = article['content']

            # check the title
            if not title:
                title = "DEFAULT_TITLE_" + str(uuid.uuid1())[1:8]
            title = self._validate_title(title)

            # download
            self._download_markdown(title, markdown)
            self._download_html(title, html)
            if self.__class__.download_img_flag:
                self._download_img(title, markdown)
            ArticleContentSpider.count += 1
            print("[%s] :%s        is Done!!" % (ArticleContentSpider.count, title))

        else:
            print('The path is not exists')

    def _download_markdown(self, title, markdown):
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
            print('No MarkDown Content !?')
            print('------------------------------------------------------------------------------')
            return

        # write
        path = self.__class__.download_path + "\\markdown" + "\\" + title + '.md'
        f = open(path, 'w+', encoding="utf8")
        f.write(markdown)
        f.seek(0)
        f.close()

    def _download_html(self, title, html):
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
        path = self.__class__.download_path + "\\html" + "\\" + title + '.html'
        f = open(path, 'w+', encoding="utf8")
        f.write(html)
        f.seek(0)
        f.close()

    def _download_img(self, title, markdown):
        """
        Download the images
        :param download_path:
        :param title:
        :param markdown:
        :return:
        """
        # check article content
        if not (title and markdown):
            print("Because there is no Markdown content, you can't download pictures.")
            return

        # regular expression matching
        # picture URLs have two formats as follows :
        #   (1) html
        #   <center>
        #       <img src = "url">
        #   </center>
        #
        #   (2) markdown
        #   ![picture](url)
        pic_urls = re.findall(r"!\[[\s\S]*?\]\((.+?)\)", markdown)  # one
        pic_urls += re.findall(r'.*?img src.*?"(http.+?)">', markdown)  # two

        # remove csdn 'watermarking'
        pics = []
        for pic in pic_urls:
            pic = re.findall('.*(http.*(.png|.jpg|.gif|))[?]?.*', pic)  # support .png .jpg .gif and ''(blank)
            if pic and pic[0]:
                pics.append(pic[0])

        # if there is no picture URL that meets the requirements, return
        if (not pics) or (not pics[0]):
            return

        # create directory
        article_img_path = self.__class__.img_path + '\\' + title
        if not os.path.exists(article_img_path):
            os.makedirs(article_img_path)

        # save the images
        count = 1
        for pic in pics:
            url = pic[0]  # pic url
            suffix = '.png' if not pic[1] else pic[1]  # if pic[1] is black , default .png
            try:
                html = requests.get(url, verify=False)
                with open(article_img_path + '\\' + str(count) + suffix, "wb")as f:
                    f.write(html.content)
                    f.seek(0)
                    f.close()
                    count += 1
            except requests.exceptions.ConnectionError:
                print("Cannot download pic, skip this time:", pic[0])

    def _mkdir(self):
        """
        mkdir directory
        :param download_path:
        :return:
        """

        # create father directory
        if not os.path.exists(self.__class__.download_path):
            os.makedirs(self.__class__.download_path)
            print('The directory has been created :' + self.__class__.download_path)

        # create son directory (html, markdown,img)
        if not os.path.exists(self.__class__.html_path):
            os.makedirs(self.__class__.html_path)
            print('The directory has been created :' + self.__class__.html_path)
        if not os.path.exists(self.__class__.markdown_path):
            os.makedirs(self.__class__.markdown_path)
            print('The directory has been created :' + self.__class__.markdown_path)
        if self.__class__.download_img_flag:
            if not os.path.exists(self.__class__.img_path):
                os.makedirs(self.__class__.img_path)
                print('The directory has been created :' + self.__class__.img_path)

    def _validate_title(self, title):
        """
        Replace windows illegal characters from file names
        '/ \ : * ? " < > |'
        :return:
        """

        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        new_title = re.sub(rstr, "_", title)
        return new_title
