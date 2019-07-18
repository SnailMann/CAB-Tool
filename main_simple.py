from src.login import Login
from src.article_id_spider import ArticleIdSpider
from src.article_content_spider import ArticleContentSpider

HOME_URL = 'https://blog.csdn.net/'
PAGE_URL = '/article/list/'
MARKDOWN_URL = 'https://mp.csdn.net/mdeditor/getArticle?id='

"""User Settings"""
GLO_CONFIG = {
    'download_path': r"D:\csdn-blog-backup",  # default
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

    # login in csdn and get user data
    user = login.dologin(GLO_CONFIG['username'], GLO_CONFIG['password'])

    # backup article
    global HOME_URL
    article_ids = article_id_spider.getArticleId(HOME_URL + user['username'],
                                                 HOME_URL + user['username'] + PAGE_URL)
    article_content_spider.getArticle(GLO_CONFIG['download_path'],
                                      MARKDOWN_URL, article_ids, user['cookies'])

    # end
    print('')
    print("User %s have a total of %s articles, It's all finished. Please check it." % (
        user['username'], str(len(article_ids))))


def _read_config():
    """
    Input
    :return:
    """
    username = input('please input CSDN username : \n')
    password = input('please input CSDN password : \n')
    download_path = input(
        'please input download path : \n(if path is blank, we will give it default value "d:\csdn-blog-backup")\n')

    GLO_CONFIG['username'] = username
    GLO_CONFIG['password'] = password

    # if the download path is blank, it'll get the default.
    if not download_path:
        return
    GLO_CONFIG['download_path'] = download_path


if __name__ == '__main__':
    _read_config()
    _main()
