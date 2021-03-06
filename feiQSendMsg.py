import feiQCoreData
import time
import os


def build_msg(command_num, option=''):
    """组装需要发送的消息"""
    feiQCoreData.packet_id = int(time.time())
    msg = "%d:%d:%s:%s:%d:%s" % (feiQCoreData.feiQ_version, feiQCoreData.packet_id, feiQCoreData.feiQ_user_name, feiQCoreData.feiQ_host_name, command_num, option)
    
    return msg


def build_file_msg(file_name):
    """组装需要发送的文件消息"""
    try:
        file_size = os.path.getsize(file_name)
        file_ctime = os.path.getctime(file_name)
    except:
        print('%s >>文件不存在，请重新输入' % file_name)
    else:
        # 文件序号：文件名：文件大小：文件修改时间：文件类型
        # 0:test.doc:05600:5983d77e:1:
        option_str = "%d:%s:%x:%x:%x" % (0, file_name, file_size, int(file_ctime), feiQCoreData.IPMSG_FILE_REGULAR)
        command_num = feiQCoreData.IPMSG_SENDMSG | feiQCoreData.IPMSG_FILEATTACHOPT
        file_str = '\0' + option_str
        return build_msg(command_num, file_str)


def send_msg(send_data, dest_ip):
    """发送飞秋数据"""
    feiQCoreData.udp_socket.sendto(send_data.encode('gbk'), (dest_ip, feiQCoreData.feiQ_port))


def send_broadcast_online_msg():
    """发送上线提醒"""
    online_msg = build_msg(feiQCoreData.IPMSG_BR_ENTRY, feiQCoreData.feiQ_user_name)
    send_msg(online_msg, feiQCoreData.broadcast_ip)


def send_broadcast_offline_msg():
    """发送下线提醒"""
    offline_msg = build_msg(feiQCoreData.IPMSG_BR_EXIT, feiQCoreData.feiQ_user_name)
    send_msg(offline_msg, feiQCoreData.broadcast_ip)


def send_msg_2_ip():
    """向指定的ip发送飞秋消息"""
    # 获取对方的ip
    dest_ip = input("请输入对方的ip(s输入0显示用户列表)")
    if dest_ip == '0':
        # 显示在线用户列表，选取其中一个
        for i, user_info in enumerate(feiQCoreData.user_list):
            print(i, user_info)
        try:
            num = int(input("请输入用户所对应的序号："))
        except:
            print("输入有误")
        else:
            dest_ip = feiQCoreData.user_list[num]["ip"]

    send_data = input('请输入你要发送的消息详情：')

    if dest_ip and send_data:
        chat_msg = build_msg(feiQCoreData.IPMSG_SENDMSG, send_data)
        send_msg(chat_msg, dest_ip)


def send_file_2_ip():
    """向指定的ip发送飞秋文件"""
    # 获取对方的ip
    dest_ip = input("请输入对方的ip(s输入0显示用户列表)")
    if dest_ip == '0':
        # 显示在线用户列表，选取其中一个
        for i, user_info in enumerate(feiQCoreData.user_list):
            print(i, user_info)
        try:
            num = int(input("请输入用户所对应的序号："))
        except:
            print("输入有误")
        else:
            dest_ip = feiQCoreData.user_list[num]["ip"]

    send_data = input('请输入你要发送的文件名：')

    if dest_ip and send_data:
        file_msg = build_file_msg(send_data)
        send_msg(file_msg, dest_ip)

        # 组织数据将其发送给子进程，告知器文件名，包编号，文件序号
        send_file_info = dict()
        send_file_info['packet_id'] = feiQCoreData.packet_id
        send_file_info['file_name'] = send_data
        send_file_info['file_id'] = 0

        send_info = dict()
        send_info["type"] = 'send_file'
        send_info['data'] = send_file_info

        feiQCoreData.file_info_queue.put(send_info)
