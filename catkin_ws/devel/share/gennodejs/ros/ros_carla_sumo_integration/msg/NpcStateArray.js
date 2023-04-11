// Auto-generated. Do not edit!

// (in-package ros_carla_sumo_integration.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let NpcState = require('./NpcState.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class NpcStateArray {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.npc_states = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('npc_states')) {
        this.npc_states = initObj.npc_states
      }
      else {
        this.npc_states = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type NpcStateArray
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [npc_states]
    // Serialize the length for message field [npc_states]
    bufferOffset = _serializer.uint32(obj.npc_states.length, buffer, bufferOffset);
    obj.npc_states.forEach((val) => {
      bufferOffset = NpcState.serialize(val, buffer, bufferOffset);
    });
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type NpcStateArray
    let len;
    let data = new NpcStateArray(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [npc_states]
    // Deserialize array length for message field [npc_states]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.npc_states = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.npc_states[i] = NpcState.deserialize(buffer, bufferOffset)
    }
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    object.npc_states.forEach((val) => {
      length += NpcState.getMessageSize(val);
    });
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_carla_sumo_integration/NpcStateArray';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '753f31c416b6057fc1aecabd83a43635';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
    
    ros_carla_sumo_integration/NpcState[] npc_states
    
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
    MSG: ros_carla_sumo_integration/NpcState
    std_msgs/Header header
    
    geometry_msgs/Vector3 loc   # loc.x (m)
    geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)
    geometry_msgs/Vector3 vel   # vel.x (m/s)
    geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)
    
    
    
    
    ================================================================================
    MSG: geometry_msgs/Vector3
    # This represents a vector in free space. 
    # It is only meant to represent a direction. Therefore, it does not
    # make sense to apply a translation to it (e.g., when applying a 
    # generic rigid transformation to a Vector3, tf2 will only apply the
    # rotation). If you want your data to be translatable too, use the
    # geometry_msgs/Point message instead.
    
    float64 x
    float64 y
    float64 z
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new NpcStateArray(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.npc_states !== undefined) {
      resolved.npc_states = new Array(msg.npc_states.length);
      for (let i = 0; i < resolved.npc_states.length; ++i) {
        resolved.npc_states[i] = NpcState.Resolve(msg.npc_states[i]);
      }
    }
    else {
      resolved.npc_states = []
    }

    return resolved;
    }
};

module.exports = NpcStateArray;
