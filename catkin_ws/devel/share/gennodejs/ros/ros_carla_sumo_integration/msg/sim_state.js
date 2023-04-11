// Auto-generated. Do not edit!

// (in-package ros_carla_sumo_integration.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let StateEst = require('./StateEst.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class sim_state {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.npc_states = null;
      this.ids = null;
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
      if (initObj.hasOwnProperty('ids')) {
        this.ids = initObj.ids
      }
      else {
        this.ids = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type sim_state
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [npc_states]
    // Serialize the length for message field [npc_states]
    bufferOffset = _serializer.uint32(obj.npc_states.length, buffer, bufferOffset);
    obj.npc_states.forEach((val) => {
      bufferOffset = StateEst.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [ids]
    bufferOffset = _arraySerializer.int32(obj.ids, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type sim_state
    let len;
    let data = new sim_state(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [npc_states]
    // Deserialize array length for message field [npc_states]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.npc_states = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.npc_states[i] = StateEst.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [ids]
    data.ids = _arrayDeserializer.int32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    object.npc_states.forEach((val) => {
      length += StateEst.getMessageSize(val);
    });
    length += 4 * object.ids.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_carla_sumo_integration/sim_state';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '185341581fb7d3ee8a79a208168cad63';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    StateEst[] npc_states			# Array of state_est for all NPCs in the simulation
    int32[] ids						# Array of ids for all NPCs in the simulation, each index corresponding with an element in state_est
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
    MSG: ros_carla_sumo_integration/StateEst
    std_msgs/Header header
    
    float64 lat      # latitude (deg)
    float64 lon      # longitude (deg)
    
    float64 x        # x coordinate (m)
    float64 y        # y coordinate (m)
    float64 psi      # yaw angle (rad)
    float64 v        # speed (m/s)
    
    float64 v_long   # longitidunal velocity (m/s)
    float64 v_lat    # lateral velocity (m/s)
    float64 yaw_rate # w_z, yaw rate (rad/s)
    
    float64 a_long   # longitudinal acceleration (m/s^2)
    float64 a_lat    # lateral acceleration (m/s^2)
    float64 df       # front steering angle (rad)
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new sim_state(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.npc_states !== undefined) {
      resolved.npc_states = new Array(msg.npc_states.length);
      for (let i = 0; i < resolved.npc_states.length; ++i) {
        resolved.npc_states[i] = StateEst.Resolve(msg.npc_states[i]);
      }
    }
    else {
      resolved.npc_states = []
    }

    if (msg.ids !== undefined) {
      resolved.ids = msg.ids;
    }
    else {
      resolved.ids = []
    }

    return resolved;
    }
};

module.exports = sim_state;
