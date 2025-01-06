import socket
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
from std_msgs.msg import Empty
from tf.transformations import euler_from_quaternion
import math
import requests
import json
from enum import Enum
# 创建UDP套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定本地地址和端口
ip = "192.168.144.92"
port = 12345
udp_socket.bind((ip,port))

#发送消息至目标的地址
addr = ("192.168.144.108",9003) 

#创建命令类型枚举
class CmdType(Enum):
    rotation_pitch = 0
    rotation_yaw = 1
    rotation_roll = 2

def Add_TPCmd_Crc(cmd,len): #len为cmd的总长度，cmd此时为缺少crc，需要补充上
    crc = 0
    for i in range(len):
        crc = crc + ord(cmd[i])
    crc = crc % 256
    formatted_crc = "{:02X}".format(crc)
    #print(formatted_crc)
    cmd += formatted_crc
    #print(cmd)
    return cmd

def data_append_cmd(data,Cmdtype):
    if Cmdtype == CmdType.rotation_pitch:
        data += 'GAP'
    elif Cmdtype == CmdType.rotation_yaw:
        data += 'GAY'
    elif Cmdtype == CmdType.rotation_roll:
        data += 'GAR'
    return data
def data_send(data):
    cmd = Add_TPCmd_Crc(data,len(data))
    cmd_bytes = cmd.encode('utf-8')
    # 发送数据
    udp_socket.sendto(cmd_bytes, addr)
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
    roll = math.degrees(roll)
    pitch = pitch*100
    yaw = yaw*100
    roll = roll*100
    #data = '#tpPG6wGAP 0xFFFF 0xFF crc'
    
    if pitch != 0:
        data = '#tpPG6w'                                        #数据头 tp--变长命令 P--udp G--云台 6--命令长度为6 w--控制命令
        data = data_append_cmd(data,CmdType.rotation_pitch)     #添加命令类型，如pitch转动
                                                                
        if pitch < 0:           
            hex_pitch = "{:04X}".format((int(pitch) & 0xffff))
        else:
            hex_pitch = "{:04X}".format(int(pitch))
        data += hex_pitch                                       #添加pitch角度
        data += "32"#速度,32代表速度为50,即5度每秒                 #添加转动速度
        data_send(data)                                         #经crc校验后发送数据
    if yaw != 0:
        data = '#tpPG6w'
        data = data_append_cmd(data,CmdType.rotation_yaw)

        if yaw < 0:
            hex_yaw = "{:04X}".format(int(yaw) & 0xffff)
        else:
            hex_yaw = "{:04X}".format(int(yaw))
        data += hex_yaw
        data += '32'
        data_send(data)
    if roll != 0:
        data = '#tpPG6w'                                      
        data = data_append_cmd(data,CmdType.rotation_roll)

        if roll < 0:
            hex_roll = "{:04X}".format(int(roll) & 0xffff)
        else:
            hex_roll = "{:04X}".format(int(roll))
        data += hex_roll
        data += '32'
        data_send(data)

if __name__ == '__main__':
    rospy.init_node('A8mini')
    rospy.Subscriber("/A8mini", Pose, poseCallback)
    rospy.spin()

        
