# 保存udp套接字
udp_socket = None

# 用户相关信息
feiQ_port = 2425
feiQ_version = 1
feiQ_user_name = "罗斯柴尔德-james"
feiQ_host_name = '罗斯柴尔德家族'
broadcast_ip = '192.168.35.34' # 广播ip

# 飞秋command
IPMSG_BR_ENTRY = 0x00000001
IPMSG_BR_EXIT = 0x00000002
IPMSG_SENDMSG = 0x00000020  # 表示 发送消息
IPMSG_ANSENTRY = 0x00000003
IPMSG_RECVMSG = 0x00000021  # 当告知对方 已收到消息

# optin for all command
IPMSG_FILEATTACHOPT = 0x00200000  # 文件消息

# file_types for fileattach command
IPMSG_FILE_REGULAR = 0x00000001  # 普通文件
# 下载文件 tcp发送
IPMSG_GETFILEDATA = 0x00000060

# 用户列表
user_list = list() # 保存在线用户列表
# 保存文件包编号
packet_id = 0

# 一个队列来进程间通信
file_info_queue = None
# 保存文件
file_list = list()
# 保存下载文件按
download_file_list = list()
