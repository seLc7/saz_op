# coding=utf-8
# import os
# import sys
# import os.path
import zipfile
from collections import OrderedDict
from datetime import datetime


def get_content(zipfilename):
    """获取文件内容"""
    zfobj = zipfile.ZipFile(zipfilename)
    content_dict = OrderedDict()
    row_dict = {}
    name_num = '0001'
    # print zfobj.namelist()
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/') or name == '[Content_Types].xml' \
                or name.endswith('.htm'):
            # os.mkdir(os.path.join(unziptodir, name))
            continue
        else:
            content = zfobj.read(name)  # 获取文件内容

            name_num = name.split('_')[0]
            if name_num not in content_dict.keys():  # 判断是否在字典中已存在条目
                row_dict = {}
                if 'c' in name:
                    row_dict = get_c_content(content)
                if 'm' in name:
                    row_dict = get_m_content(content)
                if 's' in name:
                    row_dict = get_s_content(content)
                # 若不存在就第一次获取内容后，添加第一次的条目（初始化）
                content_dict[name_num] = row_dict
            else:
                if 'c' in name:
                    row_dict = get_c_content(content)
                if 'm' in name:
                    row_dict = get_m_content(content)
                if 's' in name:
                    row_dict = get_s_content(content)
                content_dict[name_num].update(row_dict)  # 若存在就对相应条目进行内容更新

    # 写文件
    out_file = open('data.txt', 'w')
    out_file.write('c_POST, c_User-Agent, c_Host, c_Content-Length, ' +
                   'c_Connected-Time, c_Done-Request-Time, s_Connected-Time, ' +
                   'c_Done-Response-Time, s_Content-Lenght, Time-Flow-Length' +
                   '\r\n')
    for line in get_line_from_contentdict(content_dict):
        print line
        out_file.write(line + '\r\n')

    out_file.close()


def get_line_from_contentdict(content_dict):
    """从contentdict中获取行信息，输出字符串"""
    for name_key in content_dict:
        d = content_dict[name_key]
        key_list = ['c_post', 'c_user_agent', 'c_host', 'c_content_length',
                    'client_connected_time', 'client_done_request_time',
                    'server_connected_time', 'client_done_response_time',
                    's_content_lenght']
        line = name_key + ':'
        # line = ''
        for key in key_list:
            v = d.get(key, "N/A")  # 获取key键的值，若没有该key，则赋值为N/A

            if key == 'client_connected_time':
                first_time = time_format(v[:-1])  # 小数点后只有6位有效可运算
            if key == 'client_done_response_time':
                last_time = time_format(v[:-1])
            line += v + ','
        time_flow_length = (last_time - first_time).total_seconds()  # 获取秒级通信时长
        # print last_time - first_time
        yield line + str(time_flow_length)


def get_c_content(content):
    """获取包含‘c’字符文件的内容"""
    content_dict = dict()
    content_list = content.split('\r\n')
    for item in content_list:
        if 'POST' in item:
            post = item.split(' ')[1]
            content_dict['c_post'] = post
            continue
        if 'User-Agent' in item:
            user_agent = item.split(':')[1].replace(',', '')
            # 某些字符串中包含“，”，替换成空
            content_dict['c_user_agent'] = user_agent
            continue
        if 'Host' in item:
            host = item.split(':')[1]
            content_dict['c_host'] = host
            continue
        if 'Content-Length' in item:
            content_length = item.split(':')[1]
            content_dict['c_content_length'] = content_length
            continue

    return content_dict


def get_m_content(content):
    """获取包含‘m’字符文件的内容"""
    content_dict = dict()
    content_list = content.split('\r\n')

    for item in content_list:
        if 'SessionTimers' in item:
            # 获取时间
            temp = item.strip().split(' ')
            for element in temp:
                if 'ClientConnected' in element:
                    content_dict['client_connected_time'] = \
                        element.strip('\"').strip('+08:00').split('T')[1]
                    continue
                if 'ClientDoneRequest' in element:
                    content_dict['client_done_request_time'] = \
                        element.strip('\"').strip('+08:00').split('T')[1]
                    continue
                if 'ServerConnected' in element:
                    content_dict['server_connected_time'] = \
                        element.strip('\"').strip('+08:00').split('T')[1]
                    continue
                if 'ClientDoneResponse' in element:
                    content_dict['client_done_response_time'] = \
                        element.strip('\"').strip('+08:00').split('T')[1]
                    continue

            continue

        if 'x-hostip' in item:
            temp = item.strip().split(' ')
            content_dict['host_ip'] = temp[2].strip('\"').split('=\"')[1]
            continue

    return content_dict


def time_format(time):
    """字符串转换格式为时间"""
    date_time = datetime.strptime(
        time, '%H:%M:%S.%f') - datetime(1900, 1, 1)  # 不减会自动生成年月日为1900-01-01
    return date_time


def get_s_content(content):
    """获取带‘s’字符的文件内容"""
    content_dict = dict()
    content_list = content.split('\r\n')
    for item in content_list:
        if 'Content-Length' in item:
            content_length = item.split(':')[1]
            content_dict['s_content_lenght'] = content_length
            break

    return content_dict


if __name__ == '__main__':
    get_content('test.saz')
