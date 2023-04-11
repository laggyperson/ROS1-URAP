; Auto-generated. Do not edit!


(cl:in-package ros_carla_sumo_integration-msg)


;//! \htmlinclude SPaT.msg.html

(cl:defclass <SPaT> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (tl_state
    :reader tl_state
    :initarg :tl_state
    :type cl:fixnum
    :initform 0)
   (s
    :reader s
    :initarg :s
    :type cl:float
    :initform 0.0)
   (time_r
    :reader time_r
    :initarg :time_r
    :type cl:float
    :initform 0.0)
   (time_y
    :reader time_y
    :initarg :time_y
    :type cl:float
    :initform 0.0)
   (time_g
    :reader time_g
    :initarg :time_g
    :type cl:float
    :initform 0.0)
   (intersection_id
    :reader intersection_id
    :initarg :intersection_id
    :type cl:integer
    :initform 0)
   (obstacle_free
    :reader obstacle_free
    :initarg :obstacle_free
    :type cl:boolean
    :initform cl:nil)
   (signal_phase
    :reader signal_phase
    :initarg :signal_phase
    :type cl:integer
    :initform 0)
   (signal_timing
    :reader signal_timing
    :initarg :signal_timing
    :type cl:float
    :initform 0.0)
   (stop_bar_distance
    :reader stop_bar_distance
    :initarg :stop_bar_distance
    :type cl:float
    :initform 0.0))
)

(cl:defclass SPaT (<SPaT>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SPaT>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SPaT)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_carla_sumo_integration-msg:<SPaT> is deprecated: use ros_carla_sumo_integration-msg:SPaT instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:header-val is deprecated.  Use ros_carla_sumo_integration-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'tl_state-val :lambda-list '(m))
(cl:defmethod tl_state-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:tl_state-val is deprecated.  Use ros_carla_sumo_integration-msg:tl_state instead.")
  (tl_state m))

(cl:ensure-generic-function 's-val :lambda-list '(m))
(cl:defmethod s-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:s-val is deprecated.  Use ros_carla_sumo_integration-msg:s instead.")
  (s m))

(cl:ensure-generic-function 'time_r-val :lambda-list '(m))
(cl:defmethod time_r-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:time_r-val is deprecated.  Use ros_carla_sumo_integration-msg:time_r instead.")
  (time_r m))

(cl:ensure-generic-function 'time_y-val :lambda-list '(m))
(cl:defmethod time_y-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:time_y-val is deprecated.  Use ros_carla_sumo_integration-msg:time_y instead.")
  (time_y m))

(cl:ensure-generic-function 'time_g-val :lambda-list '(m))
(cl:defmethod time_g-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:time_g-val is deprecated.  Use ros_carla_sumo_integration-msg:time_g instead.")
  (time_g m))

(cl:ensure-generic-function 'intersection_id-val :lambda-list '(m))
(cl:defmethod intersection_id-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:intersection_id-val is deprecated.  Use ros_carla_sumo_integration-msg:intersection_id instead.")
  (intersection_id m))

(cl:ensure-generic-function 'obstacle_free-val :lambda-list '(m))
(cl:defmethod obstacle_free-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:obstacle_free-val is deprecated.  Use ros_carla_sumo_integration-msg:obstacle_free instead.")
  (obstacle_free m))

(cl:ensure-generic-function 'signal_phase-val :lambda-list '(m))
(cl:defmethod signal_phase-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:signal_phase-val is deprecated.  Use ros_carla_sumo_integration-msg:signal_phase instead.")
  (signal_phase m))

(cl:ensure-generic-function 'signal_timing-val :lambda-list '(m))
(cl:defmethod signal_timing-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:signal_timing-val is deprecated.  Use ros_carla_sumo_integration-msg:signal_timing instead.")
  (signal_timing m))

(cl:ensure-generic-function 'stop_bar_distance-val :lambda-list '(m))
(cl:defmethod stop_bar_distance-val ((m <SPaT>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_carla_sumo_integration-msg:stop_bar_distance-val is deprecated.  Use ros_carla_sumo_integration-msg:stop_bar_distance instead.")
  (stop_bar_distance m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SPaT>) ostream)
  "Serializes a message object of type '<SPaT>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let* ((signed (cl:slot-value msg 'tl_state)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 's))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'time_r))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'time_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'time_g))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let* ((signed (cl:slot-value msg 'intersection_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'obstacle_free) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'signal_phase)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'signal_timing))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'stop_bar_distance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SPaT>) istream)
  "Deserializes a message object of type '<SPaT>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'tl_state) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 's) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'time_r) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'time_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'time_g) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'intersection_id) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
    (cl:setf (cl:slot-value msg 'obstacle_free) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'signal_phase) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'signal_timing) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'stop_bar_distance) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SPaT>)))
  "Returns string type for a message object of type '<SPaT>"
  "ros_carla_sumo_integration/SPaT")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SPaT)))
  "Returns string type for a message object of type 'SPaT"
  "ros_carla_sumo_integration/SPaT")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SPaT>)))
  "Returns md5sum for a message object of type '<SPaT>"
  "4a13bd7f4a042e03e0c090f45d0c6c44")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SPaT)))
  "Returns md5sum for a message object of type 'SPaT"
  "4a13bd7f4a042e03e0c090f45d0c6c44")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SPaT>)))
  "Returns full string definition for message of type '<SPaT>"
  (cl:format cl:nil "Header header~%~%int16 tl_state        # green:2, yellow:1, red:0 ~%float32 s             # location s (m)~%~%float32 time_r        # period of red (s)~%float32 time_y        # period of red (s)~%float32 time_g        # period of red (s)~%~%# Jacopo's cohda msg~%int64 intersection_id~%bool obstacle_free~%int64 signal_phase~%float64 signal_timing~%float64 stop_bar_distance~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SPaT)))
  "Returns full string definition for message of type 'SPaT"
  (cl:format cl:nil "Header header~%~%int16 tl_state        # green:2, yellow:1, red:0 ~%float32 s             # location s (m)~%~%float32 time_r        # period of red (s)~%float32 time_y        # period of red (s)~%float32 time_g        # period of red (s)~%~%# Jacopo's cohda msg~%int64 intersection_id~%bool obstacle_free~%int64 signal_phase~%float64 signal_timing~%float64 stop_bar_distance~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SPaT>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     2
     4
     4
     4
     4
     8
     1
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SPaT>))
  "Converts a ROS message object to a list"
  (cl:list 'SPaT
    (cl:cons ':header (header msg))
    (cl:cons ':tl_state (tl_state msg))
    (cl:cons ':s (s msg))
    (cl:cons ':time_r (time_r msg))
    (cl:cons ':time_y (time_y msg))
    (cl:cons ':time_g (time_g msg))
    (cl:cons ':intersection_id (intersection_id msg))
    (cl:cons ':obstacle_free (obstacle_free msg))
    (cl:cons ':signal_phase (signal_phase msg))
    (cl:cons ':signal_timing (signal_timing msg))
    (cl:cons ':stop_bar_distance (stop_bar_distance msg))
))
