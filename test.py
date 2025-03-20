import rospy 
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
import math
import numpy as np
from tf.transformations import euler_from_quaternion,quaternion_from_euler
from geometry_msgs.msg import Pose, Point, Quaternion
global global_yaw
global_yaw = 0
global odom
odom = Point(0,0,0)

def calculate_yaw(target_p,current_p):
    x = current_p.x
    y = current_p.y
    z = current_p.z
    diff = np.array(target_p)-np.array([x,y,z])
    #diff = np.array([0.2,0.7,0.3])
    cos_theta = np.dot((diff/np.linalg.norm(diff)),np.array([1,0,0]))
    if target_p[1]>0:
        ptz_yaw = math.acos(cos_theta)
    else:
        ptz_yaw = -math.acos(cos_theta)
    return ptz_yaw
def odom_callback(msg):
    orientation = msg.pose.pose.orientation
    roll,pitch,yaw = euler_from_quaternion([orientation.x, orientation.y, 
                                            orientation.z, orientation.w])
    global global_yaw,odom
    global_yaw = yaw
    odom = msg.pose.pose.position
if __name__ == '__main__':
    rospy.init_node('pose_publisher')
    pub = rospy.Publisher('/A8mini', Pose, queue_size=10)
    rate = rospy.Rate(10)  # 初始化频率控制器
    x = float(input("x: "))
    y = float(input("y: "))
    z = float(input("z: "))
    while not rospy.is_shutdown():
        try:
            # 获取带校验的输入
            
            
            # 同步获取最新odom和yaw（需在回调中实现锁机制）
            current_odom = odom  # 需实现同步方法
            current_yaw = global_yaw
            
            # 计算目标角度
            np_target = np.array([x, y, z])
            ptz_yaw = calculate_yaw(np_target, current_odom)
            total_yaw = ptz_yaw - current_yaw
            
            # 生成四元数
            q = quaternion_from_euler(0, 0, total_yaw)
            
            # 发布消息
            pose_msg = Pose()
            pose_msg.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])
            pub.publish(pose_msg)
            
            rate.sleep()

        except KeyboardInterrupt:
            rospy.loginfo("用户终止操作")
            break
        except Exception as e:
            rospy.logerr(f"错误: {str(e)}")
            continue