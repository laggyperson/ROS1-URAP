; Auto-generated. Do not edit!


(cl:in-package ros_carla_sumo_integration-msg)


;//! \htmlinclude sim_state.msg.html

(cl:defclass <sim_state> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (npc_states
    :reader npc_states
    :initarg :npc_states
    :type (cl:vector ros_carla_sumo_integration-msg:StateEst)
   :initform (cl:make-array 0 :element-type 'ros_carla_sumo_integration-msg:StateEst :initial-element (cl:make-instance 'ros_carla_sumo_integration-msg:StateEst)))
   (ids
    :reader ids
    :initarg :ids
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass sim_state (<sim_state>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <sim_state>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'sim_state)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_carla_sumo_integration-msg:<sim_state> is deprecated: use ros_carla_sumo_integration-msg:sim_state instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <sim_state>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:header-val is deprecated.  Use ros_carla_sumo_integration-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'npc_states-val :lambda-list '(m))
(cl:defmethod npc_states-val ((m <sim_state>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:npc_states-val is deprecated.  Use ros_carla_sumo_integration-msg:npc_states instead.")
  (npc_states m))

(cl:ensure-generic-function 'ids-val :lambda-list '(m))
(cl:defmethod ids-val ((m <sim_state>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:ids-val is deprecated.  Use ros_carla_sumo_integration-msg:ids instead.")
  (ids m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <sim_state>) ostream)
  "Serializes a message object of type '<sim_state>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'npc_states))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'npc_states))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'ids))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'ids))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <sim_state>) istream)
  "Deserializes a message object of type '<sim_state>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'npc_states) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'npc_states)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'ros_carla_sumo_integration-msg:StateEst))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'ids) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'ids)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296)))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<sim_state>)))
  "Returns string type for a message object of type '<sim_state>"
  "ros_carla_sumo_integration/sim_state")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'sim_state)))
  "Returns string type for a message object of type 'sim_state"
  "ros_carla_sumo_integration/sim_state")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<sim_state>)))
  "Returns md5sum for a message object of type '<sim_state>"
  "185341581fb7d3ee8a79a208168cad63")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'sim_state)))
  "Returns md5sum for a message object of type 'sim_state"
  "185341581fb7d3ee8a79a208168cad63")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<sim_state>)))
  "Returns full string definition for message of type '<sim_state>"
  (cl:format cl:nil "Header header~%StateEst[] npc_states			# Array of state_est for all NPCs in the simulation~%int32[] ids						# Array of ids for all NPCs in the simulation, each index corresponding with an element in state_est~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_carla_sumo_integration/StateEst~%std_msgs/Header header~%~%float64 lat      # latitude (deg)~%float64 lon      # longitude (deg)~%~%float64 x        # x coordinate (m)~%float64 y        # y coordinate (m)~%float64 psi      # yaw angle (rad)~%float64 v        # speed (m/s)~%~%float64 v_long   # longitidunal velocity (m/s)~%float64 v_lat    # lateral velocity (m/s)~%float64 yaw_rate # w_z, yaw rate (rad/s)~%~%float64 a_long   # longitudinal acceleration (m/s^2)~%float64 a_lat    # lateral acceleration (m/s^2)~%float64 df       # front steering angle (rad)~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'sim_state)))
  "Returns full string definition for message of type 'sim_state"
  (cl:format cl:nil "Header header~%StateEst[] npc_states			# Array of state_est for all NPCs in the simulation~%int32[] ids						# Array of ids for all NPCs in the simulation, each index corresponding with an element in state_est~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_carla_sumo_integration/StateEst~%std_msgs/Header header~%~%float64 lat      # latitude (deg)~%float64 lon      # longitude (deg)~%~%float64 x        # x coordinate (m)~%float64 y        # y coordinate (m)~%float64 psi      # yaw angle (rad)~%float64 v        # speed (m/s)~%~%float64 v_long   # longitidunal velocity (m/s)~%float64 v_lat    # lateral velocity (m/s)~%float64 yaw_rate # w_z, yaw rate (rad/s)~%~%float64 a_long   # longitudinal acceleration (m/s^2)~%float64 a_lat    # lateral acceleration (m/s^2)~%float64 df       # front steering angle (rad)~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <sim_state>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'npc_states) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'ids) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <sim_state>))
  "Converts a ROS message object to a list"
  (cl:list 'sim_state
    (cl:cons ':header (header msg))
    (cl:cons ':npc_states (npc_states msg))
    (cl:cons ':ids (ids msg))
))
