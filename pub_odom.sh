#!/bin/bash

# 设置默认参数值
TOPIC="/ekf_fuser/odom"
FRAME_ID="odom"
CHILD_FRAME="base_link"
POSITION="0.0,0.0,0.0"
ORIENTATION="0.0,0.0,0.0,1.0"  # 单位四元数
LINEAR_VEL="0.0,0.0,0.0"
ANGULAR_VEL="0.0,0.0,0.0"
RATE=10  # 发布频率(Hz)
ONCE=false  # 是否单次发布

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--topic)
            TOPIC="$2"
            shift 2
            ;;
        -f|--frame)
            FRAME_ID="$2"
            shift 2
            ;;
        -c|--child-frame)
            CHILD_FRAME="$2"
            shift 2
            ;;
        -p|--position)
            POSITION="$2"
            shift 2
            ;;
        -o|--orientation)
            ORIENTATION="$2"
            shift 2
            ;;
        -lv|--linear-velocity)
            LINEAR_VEL="$2"
            shift 2
            ;;
        -av|--angular-velocity)
            ANGULAR_VEL="$2"
            shift 2
            ;;
        -r|--rate)
            RATE="$2"
            shift 2
            ;;
        --once)
            ONCE=true
            shift
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 构造消息内容
MSG_TEMPLATE="
header: 
  seq: 0
  stamp: { secs: 0, nsecs: 0 }
  frame_id: '$FRAME_ID'
child_frame_id: '$CHILD_FRAME'
pose:
  pose:
    position: { x: ${POSITION%,*,*}, y: ${POSITION#*,}, z: ${POSITION##*,} }
    orientation: { x: ${ORIENTATION%,*,*,*}, y: ${ORIENTATION#*,}, z: ${ORIENTATION%,*}, w: ${ORIENTATION##*,} }
twist:
  twist:
    linear: { x: ${LINEAR_VEL%,*,*}, y: ${LINEAR_VEL#*,}, z: ${LINEAR_VEL##*,} }
    angular: { x: ${ANGULAR_VEL%,*,*}, y: ${ANGULAR_VEL#*,}, z: ${ANGULAR_VEL##*,} }
"

# 生成发布命令
PUB_CMD="rostopic pub $TOPIC nav_msgs/Odometry"
if $ONCE; then
    PUB_CMD+=" -1"
else
    PUB_CMD+=" -r $RATE"
fi

# 执行发布命令
echo "发布消息到: $TOPIC"
echo "使用参数:"
echo " - 坐标系: [$FRAME_ID] -> [$CHILD_FRAME]"
echo " - 位置: ($POSITION)"
echo " - 方向: ($ORIENTATION)"
echo " - 线速度: ($LINEAR_VEL)"
echo " - 角速度: ($ANGULAR_VEL)"
echo " - 频率: ${RATE}Hz" 

eval "$PUB_CMD" "$MSG_TEMPLATE"
