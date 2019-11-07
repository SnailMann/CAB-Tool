from src.article_content_spider import ArticleContentSpider
from src.article_id_spider import ArticleIdSpider

"""
Auther : SnailMann
temporary cookies version
"""

HOME_URL = 'https://blog.csdn.net/'
PAGE_URL = '/article/list/'
MARKDOWN_URL = 'https://mp.csdn.net/mdeditor/getArticle?id='

"""User Settings"""
GLO_CONFIG = {
    'download_path': r"D:\csdn-blog-backup",  # Default path
    'download_img': False,  # Default not to download pictures
    'sleep_time': 1,
    'name': 'yourname',  # https://blog.csdn.net/yourname <- yourname
    'cookies': 'yourcookies'
}


def _main():
    """
    Main Logic
    :return:
    """
    # Initialization
    article_id_spider = ArticleIdSpider()
    article_content_spider = ArticleContentSpider()
    print("==================================================begin====================================================")
    print("Backup Path : %s" % GLO_CONFIG['download_path'])
    print("Download Picture Or Not ?  %s" % GLO_CONFIG['download_img'])
    print("Crawl article interval : %s seconds" % GLO_CONFIG['sleep_time'])
    print("===========================================================================================================")

    # backup article
    global HOME_URL
    article_ids = article_id_spider.getArticleId(HOME_URL + GLO_CONFIG['name'],
                                                 HOME_URL + GLO_CONFIG['name'] + PAGE_URL)
    article_content_spider.getArticle(GLO_CONFIG['sleep_time'],
                                      GLO_CONFIG['download_path'], GLO_CONFIG['download_img'],
                                      MARKDOWN_URL, article_ids, convert_cookies_to_dict(GLO_CONFIG['cookies']))

    # end
    print('')
    print("===========================================================================================================")
    print("User %s have a total of %s articles, It's all finished. Please check it." % (
        GLO_CONFIG['name'], str(len(article_ids))))
    input("====================================================end====================================================")


def convert_cookies_to_dict(cookies):
    '''
    convert cookies to dict
    :param cookies:
    :return:
    '''
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    return cookies


if __name__ == '__main__':
    _main()
