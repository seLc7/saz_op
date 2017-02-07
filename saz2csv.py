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
    row_dict = dict()
    name_num = '0001'
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
        if name.endswith('/'):
            # os.mkdir(os.path.join(unziptodir, name))
            continue
        else:
            content = zfobj.read(name)  # 获取文件内容
            if name_num != name.split('_')[0]:
                name_num = name.split('_')[0]
                row_dict.clear()
            if 'c' in name:
                print "Filename contains 'c'!!"

                # content = content.decode('gbk', 'ignore')
                # content_list = content.split('\r\n')
                # content_list = content_list[:len(content_list) - 2]
                row_dict.update(get_c_content(content))
                # print content_list
                # print(type(content))
            if 'm' in name:
                # zfobj.
                print "Filename contains 'm'!!"
                # dom = xml.dom.minidom.psarseString(content)
                # print dom
                row_dict.update(get_m_content(content))
            if 's' in name:
                print "Filename contains 's'!!"
                get_s_content(content)

    print row_dict


def get_c_content(content):
    """获取包含‘c’字符文件的内容"""
    content_dict = dict()
    content_list = content.split('\r\n')
    # content_list = content_list[:len(content_list) - 2]
    for item in content_list:
        if 'POST' in item:
            post = item.split(' ')[1]
        if 'User-Agent' in item:
            user_agent = item.split(':')[1]
        if 'Host' in item:
            host = item.split(':')[1]
        if 'Content-Length' in item:
            content_length = item.split(':')[1]
    # host = content_list[3].split(':')[1]
    # content_length = content_list[6].split(':')[1]
    content_dict['c_post'] = post
    content_dict['c_user_agent'] = user_agent
    content_dict['c_host'] = host
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

    temp = content_list[len(content_list) - 3].strip().split(' ')
    egress_port = temp[2].strip('\"').split('=\"')[1]
    # print egress_port
    content_dict['egress_port'] = egress_port

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
            print content_length
            break
    content_dict['s_content_lenght'] = content_length
    print content_list


def unzip_file(zipfilename, unziptodir):
    # if not os.path.exists(unziptodir):
    #     os.mkdir(unziptodir)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():

        name = name.replace('\\', '/')
        print(name)
        if name.endswith('/'):
            # os.mkdir(os.path.join(unziptodir, name))
            continue
        else:
            file = zfobj.read(name)
            # file = str(file)
            # file = bytes.decode(file)
            # file = file.split(b'\r\n')
            # file += 'aaaaaaaaaaa'
            newstr = file.decode()
            print(newstr)
            print(type(file))

            # ext_filename = os.path.join(unziptodir, name)
            # ext_filename = ext_filename.replace('\\', '/')
            # print(ext_filename)
            # ext_dir = os.path.dirname(ext_filename)
            # if not os.path.exists(ext_dir):
            #     os.mkdir(ext_dir)

            # outfile = open(ext_filename, 'wb')
            # outfile.write(zfobj.read(name))
            # outfile.close()

            # read(ext_filename)

if __name__ == '__main__':
    # unzip_file('0001_c.zip', '/raw_test')
    get_content('0001_c.zip')