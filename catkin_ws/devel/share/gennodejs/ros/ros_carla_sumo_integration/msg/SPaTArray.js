// Auto-generated. Do not edit!

// (in-package ros_carla_sumo_integration.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let SPaT = require('./SPaT.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class SPaTArray {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.spats = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('spats')) {
        this.spats = initObj.spats
      }
      else {
        this.spats = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SPaTArray
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [spats]
    // Serialize the length for message field [spats]
    bufferOffset = _serializer.uint32(obj.spats.length, buffer, bufferOffset);
    obj.spats.forEach((val) => {
      bufferOffset = SPaT.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SPaTArray
    let len;
    let data = new SPaTArray(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [spats]
    // Deserialize array length for message field [spats]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.spats = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.spats[i] = SPaT.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    object.spats.forEach((val) => {
      length += SPaT.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_carla_sumo_integration/SPaTArray';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c20326c1787561babdd88b0bf497cc65';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
    
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SPaTArray(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.spats !== undefined) {
      resolved.spats = new Array(msg.spats.length);
      for (let i = 0; i < resolved.spats.length; ++i) {
        resolved.spats[i] = SPaT.Resolve(msg.spats[i]);
      }
    }
    else {
      resolved.spats = []
    }

    return resolved;
    }
};

module.exports = SPaTArray;
