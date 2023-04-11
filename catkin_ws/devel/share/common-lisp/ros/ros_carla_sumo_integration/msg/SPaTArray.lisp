; Auto-generated. Do not edit!


(cl:in-package ros_carla_sumo_integration-msg)


;//! \htmlinclude SPaTArray.msg.html

(cl:defclass <SPaTArray> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (spats
    :reader spats
    :initarg :spats
    :type (cl:vector ros_carla_sumo_integration-msg:SPaT)
   :initform (cl:make-array 0 :element-type 'ros_carla_sumo_integration-msg:SPaT :initial-element (cl:make-instance 'ros_carla_sumo_integration-msg:SPaT))))
)

(cl:defclass SPaTArray (<SPaTArray>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SPaTArray>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SPaTArray)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_carla_sumo_integration-msg:<SPaTArray> is deprecated: use ros_carla_sumo_integration-msg:SPaTArray instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <SPaTArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:header-val is deprecated.  Use ros_carla_sumo_integration-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'spats-val :lambda-list '(m))
(cl:defmethod spats-val ((m <SPaTArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:spats-val is deprecated.  Use ros_carla_sumo_integration-msg:spats instead.")
  (spats m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SPaTArray>) ostream)
  "Serializes a message object of type '<SPaTArray>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'spats))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'spats))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SPaTArray>) istream)
  "Deserializes a message object of type '<SPaTArray>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'spats) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'spats)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'ros_carla_sumo_integration-msg:SPaT))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SPaTArray>)))
  "Returns string type for a message object of type '<SPaTArray>"
  "ros_carla_sumo_integration/SPaTArray")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SPaTArray)))
  "Returns string type for a message object of type 'SPaTArray"
  "ros_carla_sumo_integration/SPaTArray")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SPaTArray>)))
  "Returns md5sum for a message object of type '<SPaTArray>"
  "c20326c1787561babdd88b0bf497cc65")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SPaTArray)))
  "Returns md5sum for a message object of type 'SPaTArray"
  "c20326c1787561babdd88b0bf497cc65")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SPaTArray>)))
  "Returns full string definition for message of type '<SPaTArray>"
  (cl:format cl:nil "std_msgs/Header header~%~%ros_carla_sumo_integration/SPaT[] spats~%~%~%~%~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_carla_sumo_integration/SPaT~%Header header~%~%int16 tl_state        # green:2, yellow:1, red:0 ~%float32 s             # location s (m)~%~%float32 time_r        # period of red (s)~%float32 time_y        # period of red (s)~%float32 time_g        # period of red (s)~%~%# Jacopo's cohda msg~%int64 intersection_id~%bool obstacle_free~%int64 signal_phase~%float64 signal_timing~%float64 stop_bar_distance~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SPaTArray)))
  "Returns full string definition for message of type 'SPaTArray"
  (cl:format cl:nil "std_msgs/Header header~%~%ros_carla_sumo_integration/SPaT[] spats~%~%~%~%~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: ros_carla_sumo_integration/SPaT~%Header header~%~%int16 tl_state        # green:2, yellow:1, red:0 ~%float32 s             # location s (m)~%~%float32 time_r        # period of red (s)~%float32 time_y        # period of red (s)~%float32 time_g        # period of red (s)~%~%# Jacopo's cohda msg~%int64 intersection_id~%bool obstacle_free~%int64 signal_phase~%float64 signal_timing~%float64 stop_bar_distance~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SPaTArray>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'spats) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SPaTArray>))
  "Converts a ROS message object to a list"
  (cl:list 'SPaTArray
    (cl:cons ':header (header msg))
    (cl:cons ':spats (spats msg))
))
