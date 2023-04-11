// Auto-generated. Do not edit!

// (in-package ros_carla_sumo_integration.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class NpcState {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.loc = null;
      this.rot = null;
      this.vel = null;
      this.ang_vel = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('loc')) {
        this.loc = initObj.loc
      }
      else {
        this.loc = new geometry_msgs.msg.Vector3();
      }
      if (initObj.hasOwnProperty('rot')) {
        this.rot = initObj.rot
      }
      else {
        this.rot = new geometry_msgs.msg.Vector3();
      }
      if (initObj.hasOwnProperty('vel')) {
        this.vel = initObj.vel
      }
      else {
        this.vel = new geometry_msgs.msg.Vector3();
      }
      if (initObj.hasOwnProperty('ang_vel')) {
        this.ang_vel = initObj.ang_vel
      }
      else {
        this.ang_vel = new geometry_msgs.msg.Vector3();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type NpcState
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [loc]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.loc, buffer, bufferOffset);
    // Serialize message field [rot]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.rot, buffer, bufferOffset);
    // Serialize message field [vel]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.vel, buffer, bufferOffset);
    // Serialize message field [ang_vel]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.ang_vel, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type NpcState
    let len;
    let data = new NpcState(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [loc]
    data.loc = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    // Deserialize message field [rot]
    data.rot = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    // Deserialize message field [vel]
    data.vel = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    // Deserialize message field [ang_vel]
    data.ang_vel = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 96;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_carla_sumo_integration/NpcState';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '19ecffc728299f14548932a1c167576b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header header
    
    geometry_msgs/Vector3 loc   # loc.x (m)
    geometry_msgs/Vector3 rot   # rot.x = rotation.roll (deg)
    geometry_msgs/Vector3 vel   # vel.x (m/s)
    geometry_msgs/Vector3 ang_vel   # ang_vel.x (deg/s)
    
    
    
    
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
    const resolved = new NpcState(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.loc !== undefined) {
      resolved.loc = geometry_msgs.msg.Vector3.Resolve(msg.loc)
    }
    else {
      resolved.loc = new geometry_msgs.msg.Vector3()
    }

    if (msg.rot !== undefined) {
      resolved.rot = geometry_msgs.msg.Vector3.Resolve(msg.rot)
    }
    else {
      resolved.rot = new geometry_msgs.msg.Vector3()
    }

    if (msg.vel !== undefined) {
      resolved.vel = geometry_msgs.msg.Vector3.Resolve(msg.vel)
    }
    else {
      resolved.vel = new geometry_msgs.msg.Vector3()
    }

    if (msg.ang_vel !== undefined) {
      resolved.ang_vel = geometry_msgs.msg.Vector3.Resolve(msg.ang_vel)
    }
    else {
      resolved.ang_vel = new geometry_msgs.msg.Vector3()
    }

    return resolved;
    }
};

module.exports = NpcState;
