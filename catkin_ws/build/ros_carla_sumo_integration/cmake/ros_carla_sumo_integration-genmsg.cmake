# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "ros_carla_sumo_integration: 6 messages, 0 services")

set(MSG_I_FLAGS "-Iros_carla_sumo_integration:/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(ros_carla_sumo_integration_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg" NAME_WE)
add_custom_target(_ros_carla_sumo_integration_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_carla_sumo_integration" "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg" "ros_carla_sumo_integration/StateEst:std_msgs/Header"
)

get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg" NAME_WE)
add_custom_target(_ros_carla_sumo_integration_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_carla_sumo_integration" "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg" NAME_WE)
add_custom_target(_ros_carla_sumo_integration_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_carla_sumo_integration" "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg" NAME_WE)
add_custom_target(_ros_carla_sumo_integration_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_carla_sumo_integration" "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg" "ros_carla_sumo_integration/NpcState:geometry_msgs/Vector3:std_msgs/Header"
)

get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg" NAME_WE)
add_custom_target(_ros_carla_sumo_integration_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_carla_sumo_integration" "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg" "ros_carla_sumo_integration/SPaT:std_msgs/Header"
)

get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg" NAME_WE)
add_custom_target(_ros_carla_sumo_integration_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ros_carla_sumo_integration" "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg" "geometry_msgs/Vector3:std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_cpp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_cpp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_cpp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_cpp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_cpp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
)

### Generating Services

### Generating Module File
_generate_module_cpp(ros_carla_sumo_integration
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(ros_carla_sumo_integration_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(ros_carla_sumo_integration_generate_messages ros_carla_sumo_integration_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_cpp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_cpp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_cpp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_cpp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_cpp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_cpp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_carla_sumo_integration_gencpp)
add_dependencies(ros_carla_sumo_integration_gencpp ros_carla_sumo_integration_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_carla_sumo_integration_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_eus(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_eus(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_eus(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_eus(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_eus(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
)

### Generating Services

### Generating Module File
_generate_module_eus(ros_carla_sumo_integration
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(ros_carla_sumo_integration_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(ros_carla_sumo_integration_generate_messages ros_carla_sumo_integration_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_eus _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_eus _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_eus _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_eus _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_eus _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_eus _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_carla_sumo_integration_geneus)
add_dependencies(ros_carla_sumo_integration_geneus ros_carla_sumo_integration_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_carla_sumo_integration_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_lisp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_lisp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_lisp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_lisp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_lisp(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
)

### Generating Services

### Generating Module File
_generate_module_lisp(ros_carla_sumo_integration
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(ros_carla_sumo_integration_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(ros_carla_sumo_integration_generate_messages ros_carla_sumo_integration_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_lisp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_lisp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_lisp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_lisp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_lisp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_lisp _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_carla_sumo_integration_genlisp)
add_dependencies(ros_carla_sumo_integration_genlisp ros_carla_sumo_integration_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_carla_sumo_integration_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_nodejs(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_nodejs(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_nodejs(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_nodejs(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_nodejs(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
)

### Generating Services

### Generating Module File
_generate_module_nodejs(ros_carla_sumo_integration
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(ros_carla_sumo_integration_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(ros_carla_sumo_integration_generate_messages ros_carla_sumo_integration_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_carla_sumo_integration_gennodejs)
add_dependencies(ros_carla_sumo_integration_gennodejs ros_carla_sumo_integration_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_carla_sumo_integration_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_py(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_py(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_py(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg;/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_py(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg"
  "${MSG_I_FLAGS}"
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
)
_generate_msg_py(ros_carla_sumo_integration
  "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
)

### Generating Services

### Generating Module File
_generate_module_py(ros_carla_sumo_integration
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(ros_carla_sumo_integration_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(ros_carla_sumo_integration_generate_messages ros_carla_sumo_integration_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/sim_state.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_py _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/StateEst.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_py _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaT.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_py _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcStateArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_py _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/SPaTArray.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_py _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/arpae/Documents/ROS1-URAP/catkin_ws/src/ros_carla_sumo_integration/msg/NpcState.msg" NAME_WE)
add_dependencies(ros_carla_sumo_integration_generate_messages_py _ros_carla_sumo_integration_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ros_carla_sumo_integration_genpy)
add_dependencies(ros_carla_sumo_integration_genpy ros_carla_sumo_integration_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ros_carla_sumo_integration_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ros_carla_sumo_integration
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(ros_carla_sumo_integration_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(ros_carla_sumo_integration_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/ros_carla_sumo_integration
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(ros_carla_sumo_integration_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(ros_carla_sumo_integration_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ros_carla_sumo_integration
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(ros_carla_sumo_integration_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(ros_carla_sumo_integration_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/ros_carla_sumo_integration
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(ros_carla_sumo_integration_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ros_carla_sumo_integration
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(ros_carla_sumo_integration_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(ros_carla_sumo_integration_generate_messages_py geometry_msgs_generate_messages_py)
endif()
