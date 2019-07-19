from src.login import Login
from src.article_id_spider import ArticleIdSpider
from src.article_content_spider import ArticleContentSpider
import os
import yaml

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
    print("Backup Path : %s" % GLO_CONFIG['download_path'])
    print("Download Picture Or Not ?  %s" % GLO_CONFIG['download_img'])

    # login in csdn and get user data
    user = login.dologin(GLO_CONFIG['username'], GLO_CONFIG['password'])

    # backup article
    global HOME_URL
    article_ids = article_id_spider.getArticleId(HOME_URL + user['username'],
                                                 HOME_URL + user['username'] + PAGE_URL)
    article_content_spider.getArticle(GLO_CONFIG['download_path'], GLO_CONFIG['download_img'],
                                      MARKDOWN_URL, article_ids, user['cookies'])

    # end
    print('')
    print("User %s have a total of %s articles, It's all finished. Please check it." % (
        user['username'], str(len(article_ids))))


def _read_config():
    """
    Load setting.yaml
    :return:
    """
    # get the current directory
    cur_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.join(cur_path, "settings.yaml")
    file = open(yaml_path, 'r', encoding='utf-8')

    # load setting.yaml , config is a dict
    config = yaml.safe_load(file)
    GLO_CONFIG['username'] = config['user']['username']
    GLO_CONFIG['password'] = config['user']['password']

    # if the download path is blank, it'll get the default.
    if config['backup']['download-path']:
        GLO_CONFIG['download_path'] = config['backup']['download-path']
    # download img or not ?
    if config['backup']['download-img']:
        GLO_CONFIG['download_img'] = config['backup']['download-img']


if __name__ == '__main__':
    _read_config()
    _main()
