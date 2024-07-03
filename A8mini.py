import socket
import sys
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
from tf.transformations import euler_from_quaternion
import math
# 创建UDP套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p_result = 0
# 绑定本地地址和端口
ip = "192.168.144.8"
port = 12345
udp_socket.bind((ip,port))
crc16_tab=[
    0x0,0x1021,0x2042,0x3063,0x4084,0x50a5,0x60c6,0x70e7,
    0x8108,0x9129,0xa14a,0xb16b,0xc18c,0xd1ad,0xe1ce,0xf1ef,
    0x1231,0x210,0x3273,0x2252,0x52b5,0x4294,0x72f7,0x62d6,
    0x9339,0x8318,0xb37b,0xa35a,0xd3bd,0xc39c,0xf3ff,0xe3de,
    0x2462,0x3443,0x420,0x1401,0x64e6,0x74c7,0x44a4,0x5485,
    0xa56a,0xb54b,0x8528,0x9509,0xe5ee,0xf5cf,0xc5ac,0xd58d,
    0x3653,0x2672,0x1611,0x630,0x76d7,0x66f6,0x5695,0x46b4,
    0xb75b,0xa77a,0x9719,0x8738,0xf7df,0xe7fe,0xd79d,0xc7bc,
    0x48c4,0x58e5,0x6886,0x78a7,0x840,0x1861,0x2802,0x3823,
    0xc9cc,0xd9ed,0xe98e,0xf9af,0x8948,0x9969,0xa90a,0xb92b,
    0x5af5,0x4ad4,0x7ab7,0x6a96,0x1a71,0xa50,0x3a33,0x2a12,
    0xdbfd,0xcbdc,0xfbbf,0xeb9e,0x9b79,0x8b58,0xbb3b,0xab1a,
    0x6ca6,0x7c87,0x4ce4,0x5cc5,0x2c22,0x3c03,0xc60,0x1c41,
    0xedae,0xfd8f,0xcdec,0xddcd,0xad2a,0xbd0b,0x8d68,0x9d49,
    0x7e97,0x6eb6,0x5ed5,0x4ef4,0x3e13,0x2e32,0x1e51,0xe70,
    0xff9f,0xefbe,0xdfdd,0xcffc,0xbf1b,0xaf3a,0x9f59,0x8f78,
    0x9188,0x81a9,0xb1ca,0xa1eb,0xd10c,0xc12d,0xf14e,0xe16f,
    0x1080,0xa1,0x30c2,0x20e3,0x5004,0x4025,0x7046,0x6067,
    0x83b9,0x9398,0xa3fb,0xb3da,0xc33d,0xd31c,0xe37f,0xf35e,
    0x2b1,0x1290,0x22f3,0x32d2,0x4235,0x5214,0x6277,0x7256,
    0xb5ea,0xa5cb,0x95a8,0x8589,0xf56e,0xe54f,0xd52c,0xc50d,
    0x34e2,0x24c3,0x14a0,0x481,0x7466,0x6447,0x5424,0x4405,
    0xa7db,0xb7fa,0x8799,0x97b8,0xe75f,0xf77e,0xc71d,0xd73c,
    0x26d3,0x36f2,0x691,0x16b0,0x6657,0x7676,0x4615,0x5634,
    0xd94c,0xc96d,0xf90e,0xe92f,0x99c8,0x89e9,0xb98a,0xa9ab,
    0x5844,0x4865,0x7806,0x6827,0x18c0,0x8e1,0x3882,0x28a3,
    0xcb7d,0xdb5c,0xeb3f,0xfb1e,0x8bf9,0x9bd8,0xabbb,0xbb9a,
    0x4a75,0x5a54,0x6a37,0x7a16,0xaf1,0x1ad0,0x2ab3,0x3a92,
    0xfd2e,0xed0f,0xdd6c,0xcd4d,0xbdaa,0xad8b,0x9de8,0x8dc9,
    0x7c26,0x6c07,0x5c64,0x4c45,0x3ca2,0x2c83,0x1ce0,0xcc1,
    0xef1f,0xff3e,0xcf5d,0xdf7c,0xaf9b,0xbfba,0x8fd9,0x9ff8,
    0x6e17,0x7e36,0x4e55,0x5e74,0x2e93,0x3eb2,0xed1,0x1ef0
]
def crc_check_16bites(data, len):
    global p_result
    #crc_result = 0
    #crc_result= CRC16_cal(pbuf,len, 0)
    crc:hex = 0x00
    num:int = 0
    while len != 0:
        len -= 1
        temp=(crc>>8)&0xff
        oldcrc16=crc16_tab[data[num]^temp]
        crc=(crc<<8)^oldcrc16
        num+=1
    p_result = crc
    return 2

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
    pitch = pitch*10
    yaw = yaw*10
    
    hex_pitch = int(pitch)
    hex_yaw = int(yaw)
    hex_pitch_high = (hex_pitch & 0xff00) >>8
    hex_pitch_low = (hex_pitch & 0x00ff)
    hex_yaw_high = (hex_yaw & 0xff00) >>8
    hex_yaw_low = (hex_yaw & 0x00ff)
    data = [0x55,0x66,0x01,0x04,0x00,0x00,0x00,0x0e] #
    data.append(hex_yaw_low)
    data.append(hex_yaw_high)
    data.append(hex_pitch_low)
    data.append(hex_pitch_high)
    crc_check_16bites(data, len(data))
    high = (p_result & 0xff00) >> 8
    low = p_result & 0x00FF
    data.append(low)
    data.append(high)
    #while True:
    # 发送数据
    addr = ("192.168.144.25",37260) #发送消息至目标的地址
    data_bytes = bytes([x & 0xFF for x in data])
    #data_bytes = bytes(data)
    udp_socket.sendto(data_bytes, addr)
    data.clear()


# def poseCallback(msg):
#     roll,pitch,yaw = quaternion_to_euler(msg)
#     pitch = pitch*10
#     yaw = yaw*10
    
#     hex_pitch = int(pitch)
#     hex_yaw = int(yaw)
#     import ipdb;ipdb.set_trace()
#     hex_pitch_high = (hex_pitch & 0xff00) >>8
#     hex_pitch_low = (hex_pitch & 0x00ff)
#     hex_yaw_high = (hex_yaw & 0xff00) >>8
#     hex_yaw_low = (hex_yaw & 0x00ff)
#     import ipdb;ipdb.set_trace()
#     data.append(hex_yaw_low)
#     data.append(hex_yaw_high)
#     data.append(hex_pitch_low)
#     data.append(hex_pitch_high)
#     crc_check_16bites(data, len(data))
#     high = (p_result & 0xff00) >> 8
#     low = p_result & 0x00FF
#     data.append(low)
#     data.append(high)
#     #while True:
#     # 发送数据
#     addr = ("192.168.144.25",37260) #发送消息至目标的地址
#     data_bytes = bytes([x & 0xFF for x in data])
#     #data_bytes = bytes(data)
#     udp_socket.sendto(data_bytes, addr)


# def quaternion_to_euler(quaternion):
#     x = quaternion.orientation.x
#     y = quaternion.orientation.y
#     z = quaternion.orientation.z
#     w = quaternion.orientation.w

#     # roll (x-axis rotation)
#     sinr_cosp = 2 * (w * x + y * z)
#     cosr_cosp = 1 - 2 * (x * x + y * y)
#     roll = math.atan2(sinr_cosp, cosr_cosp)

#     # pitch (y-axis rotation)
#     sinp = 2 * (w * y - z * x)
#     if abs(sinp) >= 1:
#         pitch = math.copysign(math.pi / 2, sinp)  # use 90 degrees if out of range
#     else:
#         pitch = math.asin(sinp)

#     # yaw (z-axis rotation)
#     siny_cosp = 2 * (w * z + x * y)
#     cosy_cosp = 1 - 2 * (y * y + z * z)
#     yaw = math.atan2(siny_cosp, cosy_cosp)

#     return roll, pitch, yaw

if __name__ == '__main__':

    rospy.init_node('A8mini')
    rospy.Subscriber("/A8mini", Pose, poseCallback)
    rospy.spin()
    # while True:
    #     user_input = input("1.云台转向 2.回中 3.回传云台姿态 4.朝下90度 5.单轴姿态控制\n")
    #     if user_input == '1':
    #         data = [0x55, 0x66, 0x01, 0x02, 0x00, 0x00, 0x00, 0x07, 0x10, 0x20]
    #     elif user_input == '2':
    #         data = [0x55, 0x66, 0x01, 0x01, 0x00, 0x00, 0x00, 0x08, 0x01]
    #     elif user_input == '3':
    #         data = [0x55,0x66,0x01,0x00,0x00,0x00,0x00,0x0d,0xe8,0x05]
    #     elif user_input == '4':
    #         data = [0x55,0x66,0x01,0x04,0x00,0x00,0x00,0x0e,0x80,-0x05,0xff,-0x10]
    #     elif user_input == "5":
    #         data = [0x55,0x66,0x01,0x03,0x00,0x00,0x00,0x41,0x36,0x10,0x00]
    #     crc_check_16bites(data, len(data))
    #     high = (p_result & 0xff00) >> 8
    #     print(f'高位: {high:x}')
    #     low = p_result & 0x00FF
    #     print(f'低位: {low:x}')
    #     data.append(low)
    #     data.append(high)
    #     #while True:
    #     # 发送数据
    #     addr = ("192.168.144.25",37260) #发送消息至目标的地址
    #     data_bytes = bytes([x & 0xFF for x in data])
    #     #data_bytes = bytes(data)
    #     udp_socket.sendto(data_bytes, addr)
    #     print("发送成功")
    #     # if user_input == '3':
    #     recv_data, recv_addr = udp_socket.recvfrom(1024)
    #     # if recv_data != b'':
    #     #     print(f"接收到的数据为: {recv_data.decode()}")
    #     user_input = '0'

        
