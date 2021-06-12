import requests
from utils.exception import *
import datetime
import time


def jw_login(session: requests.Session, username, password):
    result = session.post('http://202.195.206.35:8080/jsxsd/xk/LoginToXk',
                          data={'USERNAME': username, 'PASSWORD': password})
    if result.url != 'http://202.195.206.35:8080/jsxsd/framework/xsMain.jsp' and result.url != 'http://202.195.206.35:8080/jsxsd/grsz/grsz_xgmm_beg.do':
        raise AccountError('教务系统账号或密码不正确')


def jw_logout(session: requests.Session):
    session.get('http://202.195.206.35:8080/jsxsd/xk/LoginToXk', params={'method': 'exit',
                                                                           'tktime': time.mktime(
                                                                               datetime.datetime.now().timetuple())})


def get_course(session: requests.Session, kksj):
    result = session.post('http://202.195.206.35:8080/jsxsd/xskb/xskb_list.do', data={'xnxq01id': kksj})
    return result.text


def get_score(session: requests.Session, kksj, xsfs):
    result = session.post('http://202.195.206.35:8080/jsxsd/kscj/cjcx_list',
                          data={'kksj': kksj, 'kcxz': '', 'kcmc': '', 'xsfs': xsfs})
    return result.text


def get_score2(session: requests.Session, kksj):
    result = session.post('http://202.195.206.35:8080/jsxsd/kscj/cjtd_add_left', data={'kch': '', 'xnxq01id': kksj})
    return result.text
