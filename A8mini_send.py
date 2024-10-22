import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler
import math
def euler_to_quaternion(roll, pitch, yaw):
    quaternion = quaternion_from_euler(roll, pitch, yaw)
    return Quaternion(*quaternion)

def send_pose():
    

    roll = 0
    pitch = float(input("请输入Pitch角度："))
    yaw = float(input("请输入Yaw角度："))
    pitch = math.radians(pitch)
    yaw = math.radians(yaw)
    pose_msg = Pose()
    pose_msg.orientation = euler_to_quaternion(roll, pitch, yaw)
    pub.publish(pose_msg)
      # 发送频率为10Hz

if __name__ == '__main__':
    rospy.init_node('pose_sender', anonymous=True)
    pub = rospy.Publisher('/A8mini', Pose, queue_size=10)
    while True:
        try:
            send_pose()
            rate = rospy.Rate(10)
            rate.sleep()
        except rospy.ROSInterruptException:
            pass