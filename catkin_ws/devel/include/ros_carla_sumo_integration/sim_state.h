// Generated by gencpp from file ros_carla_sumo_integration/sim_state.msg
// DO NOT EDIT!


#ifndef ROS_CARLA_SUMO_INTEGRATION_MESSAGE_SIM_STATE_H
#define ROS_CARLA_SUMO_INTEGRATION_MESSAGE_SIM_STATE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <ros_carla_sumo_integration/StateEst.h>

namespace ros_carla_sumo_integration
{
template <class ContainerAllocator>
struct sim_state_
{
  typedef sim_state_<ContainerAllocator> Type;

  sim_state_()
    : header()
    , npc_states()
    , ids()  {
    }
  sim_state_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , npc_states(_alloc)
    , ids(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef std::vector< ::ros_carla_sumo_integration::StateEst_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::ros_carla_sumo_integration::StateEst_<ContainerAllocator> >::other >  _npc_states_type;
  _npc_states_type npc_states;

   typedef std::vector<int32_t, typename ContainerAllocator::template rebind<int32_t>::other >  _ids_type;
  _ids_type ids;





  typedef boost::shared_ptr< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> const> ConstPtr;

}; // struct sim_state_

typedef ::ros_carla_sumo_integration::sim_state_<std::allocator<void> > sim_state;

typedef boost::shared_ptr< ::ros_carla_sumo_integration::sim_state > sim_statePtr;
typedef boost::shared_ptr< ::ros_carla_sumo_integration::sim_state const> sim_stateConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator1> & lhs, const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator2> & rhs)
{
  return lhs.header == rhs.header &&
    lhs.npc_states == rhs.npc_states &&
    lhs.ids == rhs.ids;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator1> & lhs, const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace ros_carla_sumo_integration

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
{
  static const char* value()
  {
    return "185341581fb7d3ee8a79a208168cad63";
  }

  static const char* value(const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x185341581fb7d3eeULL;
  static const uint64_t static_value2 = 0x8a79a208168cad63ULL;
};

template<class ContainerAllocator>
struct DataType< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ros_carla_sumo_integration/sim_state";
  }

  static const char* value(const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
{
  static const char* value()
  {
    return "Header header\n"
"StateEst[] npc_states			# Array of state_est for all NPCs in the simulation\n"
"int32[] ids						# Array of ids for all NPCs in the simulation, each index corresponding with an element in state_est\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: ros_carla_sumo_integration/StateEst\n"
"std_msgs/Header header\n"
"\n"
"float64 lat      # latitude (deg)\n"
"float64 lon      # longitude (deg)\n"
"\n"
"float64 x        # x coordinate (m)\n"
"float64 y        # y coordinate (m)\n"
"float64 psi      # yaw angle (rad)\n"
"float64 v        # speed (m/s)\n"
"\n"
"float64 v_long   # longitidunal velocity (m/s)\n"
"float64 v_lat    # lateral velocity (m/s)\n"
"float64 yaw_rate # w_z, yaw rate (rad/s)\n"
"\n"
"float64 a_long   # longitudinal acceleration (m/s^2)\n"
"float64 a_lat    # lateral acceleration (m/s^2)\n"
"float64 df       # front steering angle (rad)\n"
;
  }

  static const char* value(const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.npc_states);
      stream.next(m.ids);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct sim_state_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ros_carla_sumo_integration::sim_state_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ros_carla_sumo_integration::sim_state_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "npc_states[]" << std::endl;
    for (size_t i = 0; i < v.npc_states.size(); ++i)
    {
      s << indent << "  npc_states[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::ros_carla_sumo_integration::StateEst_<ContainerAllocator> >::stream(s, indent + "    ", v.npc_states[i]);
    }
    s << indent << "ids[]" << std::endl;
    for (size_t i = 0; i < v.ids.size(); ++i)
    {
      s << indent << "  ids[" << i << "]: ";
      Printer<int32_t>::stream(s, indent + "  ", v.ids[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROS_CARLA_SUMO_INTEGRATION_MESSAGE_SIM_STATE_H
