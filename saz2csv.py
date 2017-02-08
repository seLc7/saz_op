# coding=utf-8
# import os
# import sys
# import os.path
import zipfile
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
    content_dict = dict()
    row_dict = dict()
    name_num = '0001'
    # print zfobj.namelist()
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/'):
            # os.mkdir(os.path.join(unziptodir, name))
            continue
        else:
            content = zfobj.read(name)  # 获取文件内容

            name_num = name.split('_')[0]
            if name_num not in content_dict.keys():
                row_dict = {}
                # print "if" + name
                if 'c' in name:
                    row_dict = get_c_content(content)
                if 'm' in name:
                    row_dict = get_m_content(content)
                if 's' in name:
                    row_dict = get_s_content(content)
                content_dict[name_num] = row_dict
                # print "if" + str(row_dict)
            else:
                # print "if" + name
                if 'c' in name:
                    row_dict = get_c_content(content)
                if 'm' in name:
                    row_dict = get_m_content(content)
                    # print "m!!!!!!!!!!"
                    # print row_dict
                if 's' in name:
                    row_dict = get_s_content(content)
                content_dict[name_num].update(row_dict)
                # print "else" + str(row_dict)

    # print sorted(content_dict.iteritems())
    for key, value in sorted(content_dict.iteritems()):
        print key
        print value
    # print content_dict


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
    print host_ip
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
