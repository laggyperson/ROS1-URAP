;; Auto-generated. Do not edit!


(when (boundp 'ros_carla_sumo_integration::SPaT)
  (if (not (find-package "ROS_CARLA_SUMO_INTEGRATION"))
    (make-package "ROS_CARLA_SUMO_INTEGRATION"))
  (shadow 'SPaT (find-package "ROS_CARLA_SUMO_INTEGRATION")))
(unless (find-package "ROS_CARLA_SUMO_INTEGRATION::SPAT")
  (make-package "ROS_CARLA_SUMO_INTEGRATION::SPAT"))

(in-package "ROS")
;;//! \htmlinclude SPaT.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_carla_sumo_integration::SPaT
  :super ros::object
  :slots (_header _tl_state _s _time_r _time_y _time_g _intersection_id _obstacle_free _signal_phase _signal_timing _stop_bar_distance ))

(defmethod ros_carla_sumo_integration::SPaT
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:tl_state __tl_state) 0)
    ((:s __s) 0.0)
    ((:time_r __time_r) 0.0)
    ((:time_y __time_y) 0.0)
    ((:time_g __time_g) 0.0)
    ((:intersection_id __intersection_id) 0)
    ((:obstacle_free __obstacle_free) nil)
    ((:signal_phase __signal_phase) 0)
    ((:signal_timing __signal_timing) 0.0)
    ((:stop_bar_distance __stop_bar_distance) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _tl_state (round __tl_state))
   (setq _s (float __s))
   (setq _time_r (float __time_r))
   (setq _time_y (float __time_y))
   (setq _time_g (float __time_g))
   (setq _intersection_id (round __intersection_id))
   (setq _obstacle_free __obstacle_free)
   (setq _signal_phase (round __signal_phase))
   (setq _signal_timing (float __signal_timing))
   (setq _stop_bar_distance (float __stop_bar_distance))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:tl_state
   (&optional __tl_state)
   (if __tl_state (setq _tl_state __tl_state)) _tl_state)
  (:s
   (&optional __s)
   (if __s (setq _s __s)) _s)
  (:time_r
   (&optional __time_r)
   (if __time_r (setq _time_r __time_r)) _time_r)
  (:time_y
   (&optional __time_y)
   (if __time_y (setq _time_y __time_y)) _time_y)
  (:time_g
   (&optional __time_g)
   (if __time_g (setq _time_g __time_g)) _time_g)
  (:intersection_id
   (&optional __intersection_id)
   (if __intersection_id (setq _intersection_id __intersection_id)) _intersection_id)
  (:obstacle_free
   (&optional __obstacle_free)
   (if __obstacle_free (setq _obstacle_free __obstacle_free)) _obstacle_free)
  (:signal_phase
   (&optional __signal_phase)
   (if __signal_phase (setq _signal_phase __signal_phase)) _signal_phase)
  (:signal_timing
   (&optional __signal_timing)
   (if __signal_timing (setq _signal_timing __signal_timing)) _signal_timing)
  (:stop_bar_distance
   (&optional __stop_bar_distance)
   (if __stop_bar_distance (setq _stop_bar_distance __stop_bar_distance)) _stop_bar_distance)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; int16 _tl_state
    2
    ;; float32 _s
    4
    ;; float32 _time_r
    4
    ;; float32 _time_y
    4
    ;; float32 _time_g
    4
    ;; int64 _intersection_id
    8
    ;; bool _obstacle_free
    1
    ;; int64 _signal_phase
    8
    ;; float64 _signal_timing
    8
    ;; float64 _stop_bar_distance
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int16 _tl_state
       (write-word _tl_state s)
     ;; float32 _s
       (sys::poke _s (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _time_r
       (sys::poke _time_r (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _time_y
       (sys::poke _time_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _time_g
       (sys::poke _time_g (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; int64 _intersection_id
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _intersection_id (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _intersection_id) (= (length (_intersection_id . bv)) 2)) ;; bignum
              (write-long (ash (elt (_intersection_id . bv) 0) 0) s)
              (write-long (ash (elt (_intersection_id . bv) 1) -1) s))
             ((and (class _intersection_id) (= (length (_intersection_id . bv)) 1)) ;; big1
              (write-long (elt (_intersection_id . bv) 0) s)
              (write-long (if (>= _intersection_id 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _intersection_id s)(write-long (if (>= _intersection_id 0) 0 #xffffffff) s)))
     ;; bool _obstacle_free
       (if _obstacle_free (write-byte -1 s) (write-byte 0 s))
     ;; int64 _signal_phase
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _signal_phase (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _signal_phase) (= (length (_signal_phase . bv)) 2)) ;; bignum
              (write-long (ash (elt (_signal_phase . bv) 0) 0) s)
              (write-long (ash (elt (_signal_phase . bv) 1) -1) s))
             ((and (class _signal_phase) (= (length (_signal_phase . bv)) 1)) ;; big1
              (write-long (elt (_signal_phase . bv) 0) s)
              (write-long (if (>= _signal_phase 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _signal_phase s)(write-long (if (>= _signal_phase 0) 0 #xffffffff) s)))
     ;; float64 _signal_timing
       (sys::poke _signal_timing (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _stop_bar_distance
       (sys::poke _stop_bar_distance (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int16 _tl_state
     (setq _tl_state (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; float32 _s
     (setq _s (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _time_r
     (setq _time_r (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _time_y
     (setq _time_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _time_g
     (setq _time_g (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; int64 _intersection_id
#+(or :alpha :irix6 :x86_64)
      (setf _intersection_id (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _intersection_id (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; bool _obstacle_free
     (setq _obstacle_free (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int64 _signal_phase
#+(or :alpha :irix6 :x86_64)
      (setf _signal_phase (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _signal_phase (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float64 _signal_timing
     (setq _signal_timing (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _stop_bar_distance
     (setq _stop_bar_distance (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get ros_carla_sumo_integration::SPaT :md5sum-) "4a13bd7f4a042e03e0c090f45d0c6c44")
(setf (get ros_carla_sumo_integration::SPaT :datatype-) "ros_carla_sumo_integration/SPaT")
(setf (get ros_carla_sumo_integration::SPaT :definition-)
      "Header header

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

")



(provide :ros_carla_sumo_integration/SPaT "4a13bd7f4a042e03e0c090f45d0c6c44")


