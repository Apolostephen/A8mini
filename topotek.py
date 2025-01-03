import socket
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
from std_msgs.msg import Empty
from tf.transformations import euler_from_quaternion
import math
import requests
import json
# 创建UDP套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p_result = 0
# 绑定本地地址和端口
ip = "192.168.144.8"
port = 12345
udp_socket.bind((ip,port))

def Add_TPCmd_Crc(cmd,len): #len为cmd的总长度，cmd此时为缺少crc，需要补充上
    crc = 0
    for i in range(len):
        crc = crc + ord(cmd[i])
    crc = crc % 256
    formatted_crc = "{:02X}".format(crc)
    print(formatted_crc)
    cmd += formatted_crc
    print(cmd)
    return cmd

def poseCallback(msg):
    quaternion = msg.orientation
    quaternion = msg.orientation
    x = quaternion.x
    y = quaternion.y
    z = quaternion.z
    w = quaternion.w
    roll,pitch,yaw = euler_from_quaternion([x, y, z, w])
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)
    pitch = pitch*100
    yaw = yaw*100
    #data = '#tpPG6wGAP 0xFFFF 0xFF crc'
    data = '#tpPG6w'
    if pitch != 0:
        data += 'GAP'
        if pitch < 0:
            pitch = ~pitch
            pitch += 1
            hex_pitch = "{:04X}".format(pitch)
        else:
            hex_pitch = "{:04X}".format(pitch)
    data += hex_pitch
    data += "32"
    cmd = Add_TPCmd_Crc(data,len(data))
    cmd_bytes = cmd.encode('utf-8')
    # 发送数据
    addr = ("192.168.144.25",37260) #发送消息至目标的地址
    udp_socket.sendto(cmd_bytes, addr)

def captureImageCallback(msg):
    data = [0x55,0x66,0x01,0x01,0x00,0x00,0x00,0x0c,0x00,0x34,0xce] #
    # crc_check_16bites(data, len(data))
    # high = (p_result & 0xff00) >> 8
    # low = p_result & 0x00FF
    # data.append(low)
    # data.append(high)
    # 发送数据
    addr = ("192.168.144.25",37260) #发送消息至目标的地址
    data_bytes = bytes([x & 0xFF for x in data])
    udp_socket.sendto(data_bytes,addr)
    data.clear()
    look_for_photo()
def fetch_data_from_url(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 假设返回的是 JSON 数据
        print("请求成功！！")
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        print(json_data)
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
def look_for_photo():
    url_getdirectories = "http://192.168.144.25:82//cgi-bin/media.cgi/api/v1/getdirectories"#获取文件夹目录列表
    url_getmediacount = "http://192.168.144.25:82//cgi-bin/media.cgi/api/v1/getmediacount" #获取文件数量
    url_getmedialist = "http://192.168.144.25:82//cgi-bin/media.cgi/api/v1/getmedialist" #获取文件列表
    params_getdirectories = {
        "media_type": 0
    }
    params_getmediacount = {
        "media_type": 0,
        "path": "A"
    }
    params_getmedialist = {
        "media_type": 0,
        "path": "A",
        "start": 0,
        "count": 10
    }
    fetch_data_from_url(url_getmedialist,params_getmedialist)
if __name__ == '__main__':

    rospy.init_node('A8mini')
    # data = '#TPUD2wAWB01'
    # '#tpPG6wGAP 0xFFFF 0xFF crc'#GAP为云台 角度 pitch 控制 还有GAY GAR,前四个十六进制代表转动角度，后两个十六进制代表速度，精度为0.01
    # Add_TPCmd_Crc(data,len(data))
    rospy.Subscriber("/A8mini", Pose, poseCallback)
    rospy.Subscriber("/A8mini/captureImage", Empty, captureImageCallback)
    #data = [0x55,0x66,0x01,0x09,0x00,0x00,0x00,0x21,0x00,0x02,0x00,0x0f,0x70,0x08,0x98,0x3a,0x00,0x70,0xbe]
    rospy.spin()

        
