// Auto-generated. Do not edit!

// (in-package ros_carla_sumo_integration.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class SPaT {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.tl_state = null;
      this.s = null;
      this.time_r = null;
      this.time_y = null;
      this.time_g = null;
      this.intersection_id = null;
      this.obstacle_free = null;
      this.signal_phase = null;
      this.signal_timing = null;
      this.stop_bar_distance = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('tl_state')) {
        this.tl_state = initObj.tl_state
      }
      else {
        this.tl_state = 0;
      }
      if (initObj.hasOwnProperty('s')) {
        this.s = initObj.s
      }
      else {
        this.s = 0.0;
      }
      if (initObj.hasOwnProperty('time_r')) {
        this.time_r = initObj.time_r
      }
      else {
        this.time_r = 0.0;
      }
      if (initObj.hasOwnProperty('time_y')) {
        this.time_y = initObj.time_y
      }
      else {
        this.time_y = 0.0;
      }
      if (initObj.hasOwnProperty('time_g')) {
        this.time_g = initObj.time_g
      }
      else {
        this.time_g = 0.0;
      }
      if (initObj.hasOwnProperty('intersection_id')) {
        this.intersection_id = initObj.intersection_id
      }
      else {
        this.intersection_id = 0;
      }
      if (initObj.hasOwnProperty('obstacle_free')) {
        this.obstacle_free = initObj.obstacle_free
      }
      else {
        this.obstacle_free = false;
      }
      if (initObj.hasOwnProperty('signal_phase')) {
        this.signal_phase = initObj.signal_phase
      }
      else {
        this.signal_phase = 0;
      }
      if (initObj.hasOwnProperty('signal_timing')) {
        this.signal_timing = initObj.signal_timing
      }
      else {
        this.signal_timing = 0.0;
      }
      if (initObj.hasOwnProperty('stop_bar_distance')) {
        this.stop_bar_distance = initObj.stop_bar_distance
      }
      else {
        this.stop_bar_distance = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SPaT
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [tl_state]
    bufferOffset = _serializer.int16(obj.tl_state, buffer, bufferOffset);
    // Serialize message field [s]
    bufferOffset = _serializer.float32(obj.s, buffer, bufferOffset);
    // Serialize message field [time_r]
    bufferOffset = _serializer.float32(obj.time_r, buffer, bufferOffset);
    // Serialize message field [time_y]
    bufferOffset = _serializer.float32(obj.time_y, buffer, bufferOffset);
    // Serialize message field [time_g]
    bufferOffset = _serializer.float32(obj.time_g, buffer, bufferOffset);
    // Serialize message field [intersection_id]
    bufferOffset = _serializer.int64(obj.intersection_id, buffer, bufferOffset);
    // Serialize message field [obstacle_free]
    bufferOffset = _serializer.bool(obj.obstacle_free, buffer, bufferOffset);
    // Serialize message field [signal_phase]
    bufferOffset = _serializer.int64(obj.signal_phase, buffer, bufferOffset);
    // Serialize message field [signal_timing]
    bufferOffset = _serializer.float64(obj.signal_timing, buffer, bufferOffset);
    // Serialize message field [stop_bar_distance]
    bufferOffset = _serializer.float64(obj.stop_bar_distance, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SPaT
    let len;
    let data = new SPaT(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [tl_state]
    data.tl_state = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [s]
    data.s = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [time_r]
    data.time_r = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [time_y]
    data.time_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [time_g]
    data.time_g = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [intersection_id]
    data.intersection_id = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [obstacle_free]
    data.obstacle_free = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [signal_phase]
    data.signal_phase = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [signal_timing]
    data.signal_timing = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [stop_bar_distance]
    data.stop_bar_distance = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 51;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_carla_sumo_integration/SPaT';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4a13bd7f4a042e03e0c090f45d0c6c44';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SPaT(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.tl_state !== undefined) {
      resolved.tl_state = msg.tl_state;
    }
    else {
      resolved.tl_state = 0
    }

    if (msg.s !== undefined) {
      resolved.s = msg.s;
    }
    else {
      resolved.s = 0.0
    }

    if (msg.time_r !== undefined) {
      resolved.time_r = msg.time_r;
    }
    else {
      resolved.time_r = 0.0
    }

    if (msg.time_y !== undefined) {
      resolved.time_y = msg.time_y;
    }
    else {
      resolved.time_y = 0.0
    }

    if (msg.time_g !== undefined) {
      resolved.time_g = msg.time_g;
    }
    else {
      resolved.time_g = 0.0
    }

    if (msg.intersection_id !== undefined) {
      resolved.intersection_id = msg.intersection_id;
    }
    else {
      resolved.intersection_id = 0
    }

    if (msg.obstacle_free !== undefined) {
      resolved.obstacle_free = msg.obstacle_free;
    }
    else {
      resolved.obstacle_free = false
    }

    if (msg.signal_phase !== undefined) {
      resolved.signal_phase = msg.signal_phase;
    }
    else {
      resolved.signal_phase = 0
    }

    if (msg.signal_timing !== undefined) {
      resolved.signal_timing = msg.signal_timing;
    }
    else {
      resolved.signal_timing = 0.0
    }

    if (msg.stop_bar_distance !== undefined) {
      resolved.stop_bar_distance = msg.stop_bar_distance;
    }
    else {
      resolved.stop_bar_distance = 0.0
    }

    return resolved;
    }
};

module.exports = SPaT;
