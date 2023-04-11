;; Auto-generated. Do not edit!


(when (boundp 'ros_carla_sumo_integration::NpcState)
  (if (not (find-package "ROS_CARLA_SUMO_INTEGRATION"))
    (make-package "ROS_CARLA_SUMO_INTEGRATION"))
  (shadow 'NpcState (find-package "ROS_CARLA_SUMO_INTEGRATION")))
(unless (find-package "ROS_CARLA_SUMO_INTEGRATION::NPCSTATE")
  (make-package "ROS_CARLA_SUMO_INTEGRATION::NPCSTATE"))

(in-package "ROS")
;;//! \htmlinclude NpcState.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_carla_sumo_integration::NpcState
  :super ros::object
  :slots (_header _loc _rot _vel _ang_vel ))

(defmethod ros_carla_sumo_integration::NpcState
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:loc __loc) (instance geometry_msgs::Vector3 :init))
    ((:rot __rot) (instance geometry_msgs::Vector3 :init))
    ((:vel __vel) (instance geometry_msgs::Vector3 :init))
    ((:ang_vel __ang_vel) (instance geometry_msgs::Vector3 :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _loc __loc)
   (setq _rot __rot)
   (setq _vel __vel)
   (setq _ang_vel __ang_vel)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:loc
   (&rest __loc)
   (if (keywordp (car __loc))
       (send* _loc __loc)
     (progn
       (if __loc (setq _loc (car __loc)))
       _loc)))
  (:rot
   (&rest __rot)
   (if (keywordp (car __rot))
       (send* _rot __rot)
     (progn
       (if __rot (setq _rot (car __rot)))
       _rot)))
  (:vel
   (&rest __vel)
   (if (keywordp (car __vel))
       (send* _vel __vel)
     (progn
       (if __vel (setq _vel (car __vel)))
       _vel)))
  (:ang_vel
   (&rest __ang_vel)
   (if (keywordp (car __ang_vel))
       (send* _ang_vel __ang_vel)
     (progn
       (if __ang_vel (setq _ang_vel (car __ang_vel)))
       _ang_vel)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; geometry_msgs/Vector3 _loc
    (send _loc :serialization-length)
    ;; geometry_msgs/Vector3 _rot
    (send _rot :serialization-length)
    ;; geometry_msgs/Vector3 _vel
    (send _vel :serialization-length)
    ;; geometry_msgs/Vector3 _ang_vel
    (send _ang_vel :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; geometry_msgs/Vector3 _loc
       (send _loc :serialize s)
     ;; geometry_msgs/Vector3 _rot
       (send _rot :serialize s)
     ;; geometry_msgs/Vector3 _vel
       (send _vel :serialize s)
     ;; geometry_msgs/Vector3 _ang_vel
       (send _ang_vel :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; geometry_msgs/Vector3 _loc
     (send _loc :deserialize buf ptr-) (incf ptr- (send _loc :serialization-length))
   ;; geometry_msgs/Vector3 _rot
     (send _rot :deserialize buf ptr-) (incf ptr- (send _rot :serialization-length))
   ;; geometry_msgs/Vector3 _vel
     (send _vel :deserialize buf ptr-) (incf ptr- (send _vel :serialization-length))
   ;; geometry_msgs/Vector3 _ang_vel
     (send _ang_vel :deserialize buf ptr-) (incf ptr- (send _ang_vel :serialization-length))
   ;;
   self)
  )

(setf (get ros_carla_sumo_integration::NpcState :md5sum-) "19ecffc728299f14548932a1c167576b")
(setf (get ros_carla_sumo_integration::NpcState :datatype-) "ros_carla_sumo_integration/NpcState")
(setf (get ros_carla_sumo_integration::NpcState :definition-)
      "std_msgs/Header header

geometry_msgs/Vector3 loc   # loc.x (m)
geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)
geometry_msgs/Vector3 vel   # vel.x (m/s)
geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)




================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space. 
# It is only meant to represent a direction. Therefore, it does not
# make sense to apply a translation to it (e.g., when applying a 
# generic rigid transformation to a Vector3, tf2 will only apply the
# rotation). If you want your data to be translatable too, use the
# geometry_msgs/Point message instead.

float64 x
float64 y
float64 z
")



(provide :ros_carla_sumo_integration/NpcState "19ecffc728299f14548932a1c167576b")


