import re

from bs4 import BeautifulSoup


def parse_course(html):
    soup = BeautifulSoup(html, 'html.parser')
    course_list = []
    years = []
    r = soup.find(id='xnxq01id').find_all('option')
    for item in r:
        years.append(item['value'])
    weeks = []
    r = soup.find(id='zc').find_all('option')
    for item in r:
        weeks.append(item['value'])
    student_info = soup.find(id='Top1_divLoginName').text
    user_match = re.match(r'(.*)\((.*)\)', student_info)
    student_name = user_match.group(1)
    student_number = user_match.group(2)
    r = soup.find(id='kbtable').find_all('tr')
    remark = r[-1].text.strip().replace('\n', '').replace('\t', '')
    for row in range(1, len(r) - 1):
        contents = r[row].find_all('div', attrs={'class': 'kbcontent'})
        for column in range(len(contents)):
            kbcontent = contents[column]
            raw_info = kbcontent.decode_contents()
            if raw_info[0] == '\xa0':
                continue
            one_raw_info = re.split('-{5,}<br/?>', raw_info)
            pattern = re.compile(
                r'(.*?)<br/?>(.*?)<br/?><.*?>(.*?)</font>.*?">(.*?)\(周\)')
            for info in one_raw_info:
                match = pattern.match(info)
                if match is not None:
                    id = match.group(1)
                    name = match.group(2)
                    teacher = match.group(3)
                    week: str = match.group(4)
                    room_pattern = re.compile(r'<font title="教室">(.*?)</font>')
                    room_match_result = room_pattern.search(info)
                    class_room = room_match_result.group(1) if room_match_result is not None else ''
                    string_weeks = week.split(',')
                    week_list = []
                    for sw in string_weeks:
                        if '-' in sw:
                            num = sw.split('-')
                            for w in range(int(num[0]), int(num[1]) + 1):
                                week_list.append(w)
                        else:
                            week_list.append(int(sw))
                    course_list.append(
                        {'name': name, 'id': id,
                         'classroom': class_room,
                         'week': week_list,
                         'row': row * 2 - 1,
                         'column': column + 1, 'teacher': teacher,
                         'rowSpan': 2})
    return {'course': course_list, 'remark': remark, 'week': int(weeks[-1]), 'years': years,
            'studentInfo': {'name': student_name, 'number': student_number}}


def parse_score(html):
    score_list = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find(id='dataList').find_all('tr')
        if len(trs) > 0:
            trs = trs[1:]
        for score in trs:
            one_score_prop = []
            one = score.find_all('td')
            for prop in one:
                one_score_prop.append(prop.text)
            score_list.append({'no': one_score_prop[0], 'semester': one_score_prop[1], 'scoreNo': one_score_prop[2],
                               'name': one_score_prop[3], 'score': one_score_prop[4], 'credit': one_score_prop[5],
                               'period': one_score_prop[6], 'evaluationMode': one_score_prop[7],
                               'courseProperty': one_score_prop[8], 'courseNature': one_score_prop[9],
                               'alternativeCourseNumber': one_score_prop[10],
                               'alternativeCourseName': one_score_prop[11],
                               'scoreFlag': one_score_prop[12]})
    except BaseException as e:
        print(e)
        raise Exception('没有解析到成绩或者未评教，可以使用成绩替代入口尝试查询')
    return score_list


def parse_score2(html):
    score_list = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find(id='dataList').find_all('tr')
        if len(trs) > 0:
            trs = trs[1:]
        for score in trs:
            one_score_prop = []
            one = score.find_all('td')[1:]
            for prop in one:
                one_score_prop.append(prop.text)
            score_list.append({'no': one_score_prop[0], 'semester': one_score_prop[1], 'scoreNo': one_score_prop[2],
                               'name': one_score_prop[3], 'score': one_score_prop[4], 'credit': one_score_prop[5],
                               'period': None, 'evaluationMode': one_score_prop[6],
                               'courseProperty': one_score_prop[7], 'courseNature': None,
                               'alternativeCourseNumber': None,
                               'alternativeCourseName': None,
                               'scoreFlag': None})
    except BaseException as e:
        print(e)
        raise Exception('没有解析到成绩')
    return score_list
