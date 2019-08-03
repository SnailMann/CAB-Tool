from src.login import Login
from src.article_id_spider import ArticleIdSpider
from src.article_content_spider import ArticleContentSpider

"""
Auther : SnailMann
"""

HOME_URL = 'https://blog.csdn.net/'
PAGE_URL = '/article/list/'
MARKDOWN_URL = 'https://mp.csdn.net/mdeditor/getArticle?id='

"""User Settings"""
GLO_CONFIG = {
    'download_path': r"D:\csdn-blog-backup",  # Default path
    'download_img': False,  # Default not to download pictures
    'sleep_time': 1,
    'username': 'username',
    'password': 'password'
}


def _main():
    """
    Main Logic
    :return:
    """
    # Initialization
    login = Login()
    article_id_spider = ArticleIdSpider()
    article_content_spider = ArticleContentSpider()
    print("==================================================begin====================================================")
    print("Backup Path : %s" % GLO_CONFIG['download_path'])
    print("Download Picture Or Not ?  %s" % GLO_CONFIG['download_img'])
    print("Crawl article interval : %s seconds" % GLO_CONFIG['sleep_time'])
    print("===========================================================================================================")

    # login in csdn and get user data
    user = login.dologin(GLO_CONFIG['username'], GLO_CONFIG['password'])

    # backup article
    global HOME_URL
    article_ids = article_id_spider.getArticleId(HOME_URL + user['username'],
                                                 HOME_URL + user['username'] + PAGE_URL)
    article_content_spider.getArticle(GLO_CONFIG['sleep_time'],
                                      GLO_CONFIG['download_path'], GLO_CONFIG['download_img'],
                                      MARKDOWN_URL, article_ids, user['cookies'])

    # end
    print('')
    print("===========================================================================================================")
    print("User %s have a total of %s articles, It's all finished. Please check it." % (
        user['username'], str(len(article_ids))))

    input("====================================================end====================================================")


def _read_config():
    """
    Input
    :return:
    """
    username = input('please input CSDN username : \n')
    password = input('please input CSDN password : \n')
    download_img = input('please input backup picture or not(False/True) ? \n')
    download_path = input(
        'please input download path : \n(if path is blank, we will give it default value "d:\csdn-blog-backup")\n')

    GLO_CONFIG['username'] = username
    GLO_CONFIG['password'] = password

    # backup picture or not ?
    if download_img:
        if isinstance(download_img, bool):
            GLO_CONFIG['download_img'] = download_img
        elif isinstance(download_img, str):
            if 'true' == download_img:
                GLO_CONFIG['download_img'] = True
            if 'false' == download_img:
                GLO_CONFIG['download_img'] = False
        elif isinstance(download_img, int):
            if 1 <= download_img:
                GLO_CONFIG['download_img'] = True
            if 0 >= download_img:
                GLO_CONFIG['download_img'] = False

    # if the download path is blank, it'll get the default.
    if download_path:
        GLO_CONFIG['download_path'] = download_path


if __name__ == '__main__':
    _read_config()
    _main()
