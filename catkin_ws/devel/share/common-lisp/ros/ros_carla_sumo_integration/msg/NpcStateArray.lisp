; Auto-generated. Do not edit!


(cl:in-package ros_carla_sumo_integration-msg)


;//! \htmlinclude NpcStateArray.msg.html

(cl:defclass <NpcStateArray> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (npc_states
    :reader npc_states
    :initarg :npc_states
    :type (cl:vector ros_carla_sumo_integration-msg:NpcState)
   :initform (cl:make-array 0 :element-type 'ros_carla_sumo_integration-msg:NpcState :initial-element (cl:make-instance 'ros_carla_sumo_integration-msg:NpcState))))
)

(cl:defclass NpcStateArray (<NpcStateArray>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <NpcStateArray>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'NpcStateArray)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_carla_sumo_integration-msg:<NpcStateArray> is deprecated: use ros_carla_sumo_integration-msg:NpcStateArray instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <NpcStateArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:header-val is deprecated.  Use ros_carla_sumo_integration-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'npc_states-val :lambda-list '(m))
(cl:defmethod npc_states-val ((m <NpcStateArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:npc_states-val is deprecated.  Use ros_carla_sumo_integration-msg:npc_states instead.")
  (npc_states m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <NpcStateArray>) ostream)
  "Serializes a message object of type '<NpcStateArray>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'npc_states))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'npc_states))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <NpcStateArray>) istream)
  "Deserializes a message object of type '<NpcStateArray>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'npc_states) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'npc_states)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'ros_carla_sumo_integration-msg:NpcState))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<NpcStateArray>)))
  "Returns string type for a message object of type '<NpcStateArray>"
  "ros_carla_sumo_integration/NpcStateArray")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'NpcStateArray)))
  "Returns string type for a message object of type 'NpcStateArray"
  "ros_carla_sumo_integration/NpcStateArray")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<NpcStateArray>)))
  "Returns md5sum for a message object of type '<NpcStateArray>"
  "753f31c416b6057fc1aecabd83a43635")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'NpcStateArray)))
  "Returns md5sum for a message object of type 'NpcStateArray"
  "753f31c416b6057fc1aecabd83a43635")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<NpcStateArray>)))
  "Returns full string definition for message of type '<NpcStateArray>"
  (cl:format cl:nil "std_msgs/Header header~%~%ros_carla_sumo_integration/NpcState[] npc_states~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_carla_sumo_integration/NpcState~%std_msgs/Header header~%~%geometry_msgs/Vector3 loc   # loc.x (m)~%geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)~%geometry_msgs/Vector3 vel   # vel.x (m/s)~%geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)~%~%~%~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'NpcStateArray)))
  "Returns full string definition for message of type 'NpcStateArray"
  (cl:format cl:nil "std_msgs/Header header~%~%ros_carla_sumo_integration/NpcState[] npc_states~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_carla_sumo_integration/NpcState~%std_msgs/Header header~%~%geometry_msgs/Vector3 loc   # loc.x (m)~%geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)~%geometry_msgs/Vector3 vel   # vel.x (m/s)~%geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)~%~%~%~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <NpcStateArray>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'npc_states) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <NpcStateArray>))
  "Converts a ROS message object to a list"
  (cl:list 'NpcStateArray
    (cl:cons ':header (header msg))
    (cl:cons ':npc_states (npc_states msg))
))
