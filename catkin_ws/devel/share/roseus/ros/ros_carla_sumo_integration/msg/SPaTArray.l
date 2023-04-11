;; Auto-generated. Do not edit!


(when (boundp 'ros_carla_sumo_integration::SPaTArray)
  (if (not (find-package "ROS_CARLA_SUMO_INTEGRATION"))
    (make-package "ROS_CARLA_SUMO_INTEGRATION"))
  (shadow 'SPaTArray (find-package "ROS_CARLA_SUMO_INTEGRATION")))
(unless (find-package "ROS_CARLA_SUMO_INTEGRATION::SPATARRAY")
  (make-package "ROS_CARLA_SUMO_INTEGRATION::SPATARRAY"))

(in-package "ROS")
;;//! \htmlinclude SPaTArray.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_carla_sumo_integration::SPaTArray
  :super ros::object
  :slots (_header _spats ))

(defmethod ros_carla_sumo_integration::SPaTArray
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:spats __spats) (let (r) (dotimes (i 0) (push (instance ros_carla_sumo_integration::SPaT :init) r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _spats __spats)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:spats
   (&rest __spats)
   (if (keywordp (car __spats))
       (send* _spats __spats)
     (progn
       (if __spats (setq _spats (car __spats)))
       _spats)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; ros_carla_sumo_integration/SPaT[] _spats
    (apply #'+ (send-all _spats :serialization-length)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; ros_carla_sumo_integration/SPaT[] _spats
     (write-long (length _spats) s)
     (dolist (elem _spats)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; ros_carla_sumo_integration/SPaT[] _spats
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _spats (let (r) (dotimes (i n) (push (instance ros_carla_sumo_integration::SPaT :init) r)) r))
     (dolist (elem- _spats)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;;
   self)
  )

(setf (get ros_carla_sumo_integration::SPaTArray :md5sum-) "c20326c1787561babdd88b0bf497cc65")
(setf (get ros_carla_sumo_integration::SPaTArray :datatype-) "ros_carla_sumo_integration/SPaTArray")
(setf (get ros_carla_sumo_integration::SPaTArray :definition-)
      "std_msgs/Header header

ros_carla_sumo_integration/SPaT[] spats






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
MSG: ros_carla_sumo_integration/SPaT
Header header

int16 tl_state        # green:2, yellow:1, red:0 
float32 s             # location s (m)

float32 time_r        # period of red (s)
float32 time_y        # period of red (s)
float32 time_g        # period of red (s)

# Jacopo's cohda msg
int64 intersection_id
bool obstacle_free
int64 signal_phase
float64 signal_timing
float64 stop_bar_distance

")



(provide :ros_carla_sumo_integration/SPaTArray "c20326c1787561babdd88b0bf497cc65")


