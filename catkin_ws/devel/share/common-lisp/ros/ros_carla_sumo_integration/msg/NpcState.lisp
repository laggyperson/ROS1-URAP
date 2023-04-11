; Auto-generated. Do not edit!


(cl:in-package ros_carla_sumo_integration-msg)


;//! \htmlinclude NpcState.msg.html

(cl:defclass <NpcState> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (loc
    :reader loc
    :initarg :loc
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (rot
    :reader rot
    :initarg :rot
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (vel
    :reader vel
    :initarg :vel
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (ang_vel
    :reader ang_vel
    :initarg :ang_vel
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3)))
)

(cl:defclass NpcState (<NpcState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <NpcState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'NpcState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_carla_sumo_integration-msg:<NpcState> is deprecated: use ros_carla_sumo_integration-msg:NpcState instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <NpcState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:header-val is deprecated.  Use ros_carla_sumo_integration-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'loc-val :lambda-list '(m))
(cl:defmethod loc-val ((m <NpcState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:loc-val is deprecated.  Use ros_carla_sumo_integration-msg:loc instead.")
  (loc m))

(cl:ensure-generic-function 'rot-val :lambda-list '(m))
(cl:defmethod rot-val ((m <NpcState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:rot-val is deprecated.  Use ros_carla_sumo_integration-msg:rot instead.")
  (rot m))

(cl:ensure-generic-function 'vel-val :lambda-list '(m))
(cl:defmethod vel-val ((m <NpcState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:vel-val is deprecated.  Use ros_carla_sumo_integration-msg:vel instead.")
  (vel m))

(cl:ensure-generic-function 'ang_vel-val :lambda-list '(m))
(cl:defmethod ang_vel-val ((m <NpcState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:ang_vel-val is deprecated.  Use ros_carla_sumo_integration-msg:ang_vel instead.")
  (ang_vel m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <NpcState>) ostream)
  "Serializes a message object of type '<NpcState>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'loc) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'rot) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'vel) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'ang_vel) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <NpcState>) istream)
  "Deserializes a message object of type '<NpcState>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'loc) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'rot) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'vel) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'ang_vel) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<NpcState>)))
  "Returns string type for a message object of type '<NpcState>"
  "ros_carla_sumo_integration/NpcState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'NpcState)))
  "Returns string type for a message object of type 'NpcState"
  "ros_carla_sumo_integration/NpcState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<NpcState>)))
  "Returns md5sum for a message object of type '<NpcState>"
  "19ecffc728299f14548932a1c167576b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'NpcState)))
  "Returns md5sum for a message object of type 'NpcState"
  "19ecffc728299f14548932a1c167576b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<NpcState>)))
  "Returns full string definition for message of type '<NpcState>"
  (cl:format cl:nil "std_msgs/Header header~%~%geometry_msgs/Vector3 loc   # loc.x (m)~%geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)~%geometry_msgs/Vector3 vel   # vel.x (m/s)~%geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)~%~%~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'NpcState)))
  "Returns full string definition for message of type 'NpcState"
  (cl:format cl:nil "std_msgs/Header header~%~%geometry_msgs/Vector3 loc   # loc.x (m)~%geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)~%geometry_msgs/Vector3 vel   # vel.x (m/s)~%geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)~%~%~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <NpcState>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'loc))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'rot))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'vel))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'ang_vel))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <NpcState>))
  "Converts a ROS message object to a list"
  (cl:list 'NpcState
    (cl:cons ':header (header msg))
    (cl:cons ':loc (loc msg))
    (cl:cons ':rot (rot msg))
    (cl:cons ':vel (vel msg))
    (cl:cons ':ang_vel (ang_vel msg))
))
