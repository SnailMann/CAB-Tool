import json
import urllib3
import requests


class Login:

    def dologin(self, username='', password=''):
        """
        Simulated login CSDN account
        :param username:
        :param password:
        :return:
        """
        url = 'https://passport.csdn.net/v1/register/pc/login/doLogin'
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'referer': 'https://passport.csdn.net/login',
            'origin': 'https://passport.csdn.net',
            'content-Type': 'application/json;charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'connection': 'keep-alive',
            'Host': 'passport.csdn.net'
        }

        data = {
            'loginType': '1',
            'pwdOrVerifyCode': str(password),
            'userIdentification': str(username),
            'uaToken': '',
            'webUmidToken': ''
        }

        # login in csdn and get response
        res = requests.post(url, data=json.dumps(data), headers=header, verify=False)

        # login error
        if not res.status_code == 200:
            raise Exception(res.text)

        # assemble user data (username and cookies)
        body = res.json()
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        user = {
            'username': body['username'],
            'cookies': cookies
        }

        return user
