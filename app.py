import requests
from flask import request, json, Flask, jsonify
from utils import vpn, just
from gevent.pywsgi import WSGIServer
from utils.tool import parse_score, parse_score2, parse_course
from utils.exception import *

app = Flask(__name__)


class MyEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, AccountError):
            return o.__str__()
        else:
            return super().default(self, o)


@app.route('/')
def hello_world():
    return jsonify({'status': 'ok', 'message': '繁星flask后台'})


@app.route('/vpn/score')
def get_score_by_vpn():
    username = request.args['username']
    password = request.args['password']
    vpn_username = request.args['vpn_username']
    vpn_password = request.args['vpn_password']
    kksj = request.args['kksj']
    xsfs = request.args['xsfs']
    print('{} {} {} {} {} {}'.format(username, password, vpn_username, vpn_password, kksj, xsfs))
    session = requests.Session()
    session.verify = False
    try:
        # vpn.vpn_login(session, vpn_username, vpn_password)
        just.jw_login(session, username, password)
        result = just.get_score(session, kksj, xsfs)
        return jsonify({'code': 200, 'message': None, 'data': parse_score(result)})
    except BaseException as e:
        return jsonify({'code': 400, 'message': e.__str__(), 'data': None})
    finally:
        just.jw_logout(session)


@app.route('/vpn/score2')
def get_score2_by_vpn():
    username = request.args['username']
    password = request.args['password']
    vpn_username = request.args['vpn_username']
    vpn_password = request.args['vpn_password']
    kksj = request.args['kksj']
    session = requests.Session()
    session.verify = False
    try:
        # vpn.vpn_login(session, vpn_username, vpn_password)
        just.jw_login(session, username, password)
        result = just.get_score2(session, kksj)
        return jsonify({'code': 200, 'message': None, 'data': parse_score2(result)})
    except BaseException as e:
        return jsonify({'code': 400, 'message': e.__str__(), 'data': None})
    finally:
        just.jw_logout(session)


@app.route('/vpn/course')
def get_course_by_vpn():
    username = request.args['username']
    password = request.args['password']
    vpn_username = request.args['vpn_username']
    vpn_password = request.args['vpn_password']
    kksj = request.args['kksj']
    session = requests.Session()
    session.verify = False
    try:
        # vpn.vpn_login(session, vpn_username, vpn_password)
        just.jw_login(session, username, password)
        result = just.get_course(session, kksj)
        return jsonify({'code': 200, 'message': None, 'data': parse_course(result)})
    except BaseException as e:
        return jsonify({'code': 400, 'message': e.__str__(), 'data': None})
    finally:
        just.jw_logout(session)


@app.route('/just/score')
def get_score_by_just():
    username = request.args['username']
    password = request.args['password']
    xsfs = request.args['xsfs']
    kksj = request.args['kksj']
    session = requests.Session()
    session.verify = False
    try:
        just.jw_login(session, username, password)
        result = just.get_score(session, kksj, xsfs)
        return jsonify({'code': 200, 'message': None, 'data': parse_score(result)})
    except BaseException as e:
        return jsonify({'code': 400, 'message': e.__str__(), 'data': None})
    finally:
        just.jw_logout(session)


@app.route('/just/score2')
def get_score2_by_just():
    username = request.args['username']
    password = request.args['password']
    kksj = request.args['kksj']
    session = requests.Session()
    session.verify = False
    try:
        just.jw_login(session, username, password)
        result = just.get_score2(session, kksj)
        return jsonify({'code': 200, 'message': None, 'data': parse_score2(result)})
    except BaseException as e:
        return jsonify({'code': 400, 'message': e.__str__(), 'data': None})
    finally:
        just.jw_logout(session)


@app.route('/just/course')
def get_course_by_just():
    username = request.args['username']
    password = request.args['password']
    kksj = request.args['kksj']
    session = requests.Session()
    session.verify = False
    try:
        just.jw_login(session, username, password)
        result = just.get_course(session, kksj)
        return jsonify({'code': 200, 'message': None, 'data': parse_course(result)})
    except BaseException as e:
        return jsonify({'code': 400, 'message': e.__str__(), 'data': None})
    finally:
        just.jw_logout(session)


@app.route('/vpn2/score')
def get_score_by_vpn2():
    username = request.args['username']
    password = request.args['password']


@app.route('/vpn2/score2')
def get_score2_by_vpn2():
    username = request.args['username']
    password = request.args['password']


@app.route('/vpn2/course')
def get_course_by_vpn2():
    username = request.args['username']
    password = request.args['password']


if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 9008), app, keyfile='5070554_mdreamfever.com.key',
                        certfile='5070554_mdreamfever.com.pem')
    server.serve_forever()
