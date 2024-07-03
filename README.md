# A8mini角度控制ros包(目前仅支持roll,pitch控制)
1. 准备工作
   
    1. 将电脑设备的网口设置为144网段（192.168.144.xxx）后面的xxx不可设置为25
    2. 将A8mini.py的11行设为第一步设置的ip
    3. A8mini的rtsp流为192.168.144.25:8554/main.264
    4. 目标角度需要是四元数的形式

2. A8mini角度控制
   
   1. ros话题为'/A8mini'
   2. 消息类型为geometry_msgs/Pose
   3. 只需要配置Pose类型下的四元数（x,y,z,w）

3. 启动脚本
   
   ```python
   
    python3 A8mini.py

   ```
    

   