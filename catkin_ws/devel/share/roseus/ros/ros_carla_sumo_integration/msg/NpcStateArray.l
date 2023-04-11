;; Auto-generated. Do not edit!


(when (boundp 'ros_carla_sumo_integration::NpcStateArray)
  (if (not (find-package "ROS_CARLA_SUMO_INTEGRATION"))
    (make-package "ROS_CARLA_SUMO_INTEGRATION"))
  (shadow 'NpcStateArray (find-package "ROS_CARLA_SUMO_INTEGRATION")))
(unless (find-package "ROS_CARLA_SUMO_INTEGRATION::NPCSTATEARRAY")
  (make-package "ROS_CARLA_SUMO_INTEGRATION::NPCSTATEARRAY"))

(in-package "ROS")
;;//! \htmlinclude NpcStateArray.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_carla_sumo_integration::NpcStateArray
  :super ros::object
  :slots (_header _npc_states ))

(defmethod ros_carla_sumo_integration::NpcStateArray
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:npc_states __npc_states) (let (r) (dotimes (i 0) (push (instance ros_carla_sumo_integration::NpcState :init) r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _npc_states __npc_states)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:npc_states
   (&rest __npc_states)
   (if (keywordp (car __npc_states))
       (send* _npc_states __npc_states)
     (progn
       (if __npc_states (setq _npc_states (car __npc_states)))
       _npc_states)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; ros_carla_sumo_integration/NpcState[] _npc_states
    (apply #'+ (send-all _npc_states :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; ros_carla_sumo_integration/NpcState[] _npc_states
     (write-long (length _npc_states) s)
     (dolist (elem _npc_states)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; ros_carla_sumo_integration/NpcState[] _npc_states
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _npc_states (let (r) (dotimes (i n) (push (instance ros_carla_sumo_integration::NpcState :init) r)) r))
     (dolist (elem- _npc_states)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get ros_carla_sumo_integration::NpcStateArray :md5sum-) "753f31c416b6057fc1aecabd83a43635")
(setf (get ros_carla_sumo_integration::NpcStateArray :datatype-) "ros_carla_sumo_integration/NpcStateArray")
(setf (get ros_carla_sumo_integration::NpcStateArray :definition-)
      "std_msgs/Header header

ros_carla_sumo_integration/NpcState[] npc_states

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
MSG: ros_carla_sumo_integration/NpcState
std_msgs/Header header

geometry_msgs/Vector3 loc   # loc.x (m)
geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)
geometry_msgs/Vector3 vel   # vel.x (m/s)
geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)




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



(provide :ros_carla_sumo_integration/NpcStateArray "753f31c416b6057fc1aecabd83a43635")


