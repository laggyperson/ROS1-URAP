;; Auto-generated. Do not edit!


(when (boundp 'ros_carla_sumo_integration::sim_state)
  (if (not (find-package "ROS_CARLA_SUMO_INTEGRATION"))
    (make-package "ROS_CARLA_SUMO_INTEGRATION"))
  (shadow 'sim_state (find-package "ROS_CARLA_SUMO_INTEGRATION")))
(unless (find-package "ROS_CARLA_SUMO_INTEGRATION::SIM_STATE")
  (make-package "ROS_CARLA_SUMO_INTEGRATION::SIM_STATE"))

(in-package "ROS")
;;//! \htmlinclude sim_state.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_carla_sumo_integration::sim_state
  :super ros::object
  :slots (_header _npc_states _ids ))

(defmethod ros_carla_sumo_integration::sim_state
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:npc_states __npc_states) (let (r) (dotimes (i 0) (push (instance ros_carla_sumo_integration::StateEst :init) r)) r))
    ((:ids __ids) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _header __header)
   (setq _npc_states __npc_states)
   (setq _ids __ids)
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
  (:ids
   (&optional __ids)
   (if __ids (setq _ids __ids)) _ids)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; ros_carla_sumo_integration/StateEst[] _npc_states
    (apply #'+ (send-all _npc_states :serialization-length)) 4
    ;; int32[] _ids
    (* 4    (length _ids)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; ros_carla_sumo_integration/StateEst[] _npc_states
     (write-long (length _npc_states) s)
     (dolist (elem _npc_states)
       (send elem :serialize s)
       )
     ;; int32[] _ids
     (write-long (length _ids) s)
     (dotimes (i (length _ids))
       (write-long (elt _ids i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; ros_carla_sumo_integration/StateEst[] _npc_states
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _npc_states (let (r) (dotimes (i n) (push (instance ros_carla_sumo_integration::StateEst :init) r)) r))
     (dolist (elem- _npc_states)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; int32[] _ids
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _ids (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _ids i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get ros_carla_sumo_integration::sim_state :md5sum-) "185341581fb7d3ee8a79a208168cad63")
(setf (get ros_carla_sumo_integration::sim_state :datatype-) "ros_carla_sumo_integration/sim_state")
(setf (get ros_carla_sumo_integration::sim_state :definition-)
      "Header header
StateEst[] npc_states			# Array of state_est for all NPCs in the simulation
int32[] ids						# Array of ids for all NPCs in the simulation, each index corresponding with an element in state_est
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
MSG: ros_carla_sumo_integration/StateEst
std_msgs/Header header

float64 lat      # latitude (deg)
float64 lon      # longitude (deg)

float64 x        # x coordinate (m)
float64 y        # y coordinate (m)
float64 psi      # yaw angle (rad)
float64 v        # speed (m/s)

float64 v_long   # longitidunal velocity (m/s)
float64 v_lat    # lateral velocity (m/s)
float64 yaw_rate # w_z, yaw rate (rad/s)

float64 a_long   # longitudinal acceleration (m/s^2)
float64 a_lat    # lateral acceleration (m/s^2)
float64 df       # front steering angle (rad)
")



(provide :ros_carla_sumo_integration/sim_state "185341581fb7d3ee8a79a208168cad63")


