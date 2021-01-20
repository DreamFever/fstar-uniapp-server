import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from utils.exception import *
from utils.tool import *

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def vpn_login(session: requests.Session, username, password):
    submit_data = {'tz_offset': 400, 'username': username, 'password': password, 'realm': 'LDAP-Sudi', 'btnSubmit': '登录'}
    result = session.post('https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi', data=submit_data)
    if result.url == 'https://vpn.just.edu.cn/dana-na/auth/url_default/welcome.cgi?p=failed':
        raise AccountError('VPN密码不正确')
    if 'p=user-confirm&id=state' in result.url:
        result = session.get(result.url)
        soup = BeautifulSoup(result.text, 'html.parser')
        value = soup.find(id='DSIDFormDataStr')['value']
        session.post('https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi',
                     data={'btnContinue': '继续会话', 'FormDataStr': value})
        session.get('https://vpn.just.edu.cn/dana/home/starter0.cgi?check=yes')


def vpn_logout(session: requests.Session):
    session.get('https://vpn.just.edu.cn/dana-na/auth/logout.cgi')


def jw_login(session: requests.Session, username, password):
    session.get('https://vpn.just.edu.cn/jsxsd/,DanaInfo=jwgl.just.edu.cn,Port=8080+')
    result = session.post('https://vpn.just.edu.cn/jsxsd/xk/,DanaInfo=jwgl.just.edu.cn,Port=8080+LoginToXk',
                          data={'USERNAME': username, 'PASSWORD': password})
    if result.url != 'https://vpn.just.edu.cn/jsxsd/framework/,DanaInfo=jwgl.just.edu.cn,Port=8080+xsMain.jsp' and \
            result.url != 'https://vpn.just.edu.cn/jsxsd/grsz/,DanaInfo=jwgl.just.edu.cn,Port=8080+grsz_xgmm_beg.do':
        raise AccountError('教务系统账号或密码不正确')


def get_score(session: requests.Session, kksj='', xsfs='MAX'):
    """
    :param kksj: 开课时间
    :param xsfs: 成绩显示方式
    :return:
    """
    result = session.post('https://vpn.just.edu.cn/jsxsd/kscj/,DanaInfo=jwgl.just.edu.cn,Port=8080+cjcx_list',
                          data={'kksj': kksj, 'kcxz': '', 'kcmc': '', 'xsfs': xsfs})
    # print(result.text)
    return result.text


def get_score2(session: requests.Session, kksj=''):
    """
    :param kksj: 开课时间
    :return:
    """
    result = session.post('https://vpn.just.edu.cn/jsxsd/kscj/,DanaInfo=jwgl.just.edu.cn,Port=8080+cjtd_add_left',
                          data={'kch': '', 'xnxq01id': kksj})
    # print(result.text)
    return result.text


def get_course(session: requests.Session, kksj):
    """
    :param kksj: 开课时间
    :return:
    """
    result = session.post('https://vpn.just.edu.cn/jsxsd/xskb/,DanaInfo=jwgl.just.edu.cn,Port=8080+xskb_list.do',
                          data={'xnxq01id': kksj})
    return result.text
