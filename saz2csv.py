# coding=utf-8
# import os
# import sys
# import os.path
import zipfile
from collections import OrderedDict, defaultdict

# from read_c import read_c as read
# zfile = zipfile.ZipFile('test.saz', 'r')
# for filename in zfile.namelist():
#     data = zfile.read(filename)
#     file = open(filename, 'w+b')
#     file.write(data)
#     file.close()


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

    # for key, value in sorted(content_dict.iteritems()):
    #     print key
    #     print value
    out_file = open('data.txt', 'w')

    for line in get_line_from_contentdict(content_dict):
        print line
        out_file.write(line + '\r\n')

    out_file.close()


def get_line_from_contentdict(content_dict):
    """从contentdict中获取行信息，输出字符串"""
    # print content_dict
    for name_key in content_dict:
        # print name_key
        # print content_dict[name_key]
        d = content_dict[name_key]
        key_list = ['c_post', 'c_user_agent', 'c_host', 'c_content_length',
                    'client_connected_time', 'client_done_request_time',
                    'server_connected_time', 'client_done_response_time',
                    's_content_lenght']
        line = name_key + ':'
        # line = ''
        for key in key_list:
            v = d.get(key, "N/A")  # 获取key键的值，若没有该key，则赋值为N/A
            # line += '\t' + v
            line += v + ','
        yield line
        # for content_key in content_dict[name_key]:
        #     # print content_key
        #     if content_key == 'c_post':
        #         c_post = content_dict[name_key][content_key]
        #     if content_key == 'c_user_agent':
        #         c_user_agent = content_dict[name_key][content_key]
        #     if content_key == 'c_host':
        #         c_host = content_dict[name_key][content_key]
        #     if content_key == 'c_content_length':
        #         c_content_length = content_dict[name_key][content_key]

        #     if content_key == 'client_connected_time':
        #         client_connected_time = content_dict[name_key][content_key]
        #     if content_key == 'client_done_request_time':
        #         client_done_request_time = content_dict[name_key][content_key]
        #     if content_key == 'server_connected_time':
        #         server_connected_time = content_dict[name_key][content_key]
        #     if content_key == 'client_done_response_time':
        # client_done_response_time = content_dict[name_key][content_key]

        #     if content_key == 's_content_lenght':
        #         s_content_lenght = content_dict[name_key][content_key]

        # y


def get_c_content(content):
    """获取包含‘c’字符文件的内容"""
    content_dict = dict()
    content_list = content.split('\r\n')
    # content_list = content_list[:len(content_list) - 2]
    for item in content_list:
        if 'POST' in item:
            post = item.split(' ')[1]
            content_dict['c_post'] = post
        if 'User-Agent' in item:
            user_agent = item.split(':')[1]
            content_dict['c_user_agent'] = user_agent
        if 'Host' in item:
            host = item.split(':')[1]
            content_dict['c_host'] = host
        if 'Content-Length' in item:
            content_length = item.split(':')[1]
            content_dict['c_content_length'] = content_length

    # print post, user_agent, host, content_length

    return content_dict


def get_m_content(content):
    """获取包含‘m’字符文件的内容"""
    content_dict = dict()
    time_list = []
    content_list = content.split('\r\n')
    content_list = content_list[2:len(content_list) - 2]
    # print content_list
    # 获取时间
    temp = content_list[0].strip().split(' ')

    for i in temp[1:5]:
        time = i.strip('\"').strip('+08:00').split('T')[1]
        # if time not in time_list:
        time_list.append(time)
    for i in temp[9:len(temp) - 1]:
        time = i.strip('\"').strip('+08:00').split('T')[1]
        time_list.append(time)
    # print time_list

    content_dict['client_connected_time'] = time_list[0]
    content_dict['client_done_request_time'] = time_list[3]
    content_dict['server_connected_time'] = time_list[4]
    content_dict['client_done_response_time'] = time_list[9]

    # temp = content_list[len(content_list) - 3].strip().split(' ')
    # egress_port = temp[2].strip('\"').split('=\"')[1]
    # # print egress_port
    # content_dict['egress_port'] = egress_port

    temp = content_list[len(content_list) - 1].strip().split(' ')
    host_ip = temp[2].strip('\"').split('=\"')[1]
    content_dict['host_ip'] = host_ip
    # print temp

    return content_dict


def get_s_content(content):
    """获取带‘s’字符的文件内容"""
    content_dict = dict()
    content_list = content.split('\r\n')
    for item in content_list:
        if 'Content-Length' in item:
            content_length = item.split(':')[1]
            content_dict['s_content_lenght'] = content_length
            # print content_length
            break

    # print content_list
    return content_dict


if __name__ == '__main__':
    # unzip_file('0001_c.zip', '/raw_test')
    get_content('0001_c.zip')
