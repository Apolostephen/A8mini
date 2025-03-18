import rospy 
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
import math
import numpy as np
from tf.transformations import euler_from_quaternion,quaternion_from_euler

global_yaw
odom

def calculate_yaw(target_p,current_p):
    diff = np.array(target_p)-np.array(current_p)
    cos_theta = np.dot((diff/np.linalg.norm(target_p-current_p)),np.array([1,0,0]))
    if target_p[1]>0:
        ptz_yaw = math.acos(cos_theta)
    else:
        ptz_yaw = -math.acos(cos_theta)
    return ptz_yaw
def odom_callback(msg):
    roll,pitch,yaw = euler_from_quaternion(msg.pose.pose.orientation)
    global global_yaw,odom
    global_yaw = yaw
    odom = msg.pose.pose.position
if __name__ == '__main__':
    rospy.init_node('pose_sender', anonymous=True)
    pub = rospy.Publisher('/A8mini', Pose, queue_size=10)
    sub = rospy.Subscriber('ekf_fuser/odom',Odometry,)
    while True:
        try:
            print("请输入目标点坐标")
            x = float(input("x:"))
            y = float(input("y:"))
            z = float(input("z:"))
            np_target = np.array([x,y,z])
            ptz_yaw = calculate_yaw(np_target,odom)
            total_yaw = ptz_yaw - global_yaw
           
            pose_msg = Pose()
            pose_msg.orientation = quaternion_from_euler(0, 0, total_yaw)
            pub.publish(pose_msg)
            rate = rospy.Rate(10)
            rate.sleep()
        except rospy.ROSInterruptException:
            pass