#!/usr/bin/env python2

#2021 Hotae Lee <hotae.lee@berkeley.edu>

# ======================================================= Imports =======================================================
import glob
import os
import sys
from math import cos, sin, tan, sqrt
try:
    # CHECK : Need to change the path according to the location of carla_client egg
    sys.path.append(glob.glob('/home/arpae/RFS_SMPC/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
# CARLA
import carla

# Tools
import random
import time
import csv
import numpy as np
import cv2
import logging

# NPC vehicles
from carla import VehicleLightState as vls

# ROS 
# import rosbag
import rospy
from ros_carla_sumo_integration.msg import StateEst, NpcState, NpcStateArray, SPaT, SPaTArray
from tf.transformations import euler_from_quaternion
import math as m
from std_msgs.msg import Float32
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from scipy import io
# ======================================================= End Imports =======================================================


# Loading Map matrix
map_id = 2 # 1:rfs, 2:gomentum
gomentum_mat = io.loadmat('/home/arpae/Documents/pure_sim_URAP/pure_sim_ws/src/mpclab_controllers_arpae/nodes/Gomentum_rt3003_ver1.mat')
# gomentum_mat = io.loadmat('/home/arpae/RFS_SMPC/catkin_ws/src/mpc_carla/scripts/Road_test_Both_120821.mat')
# gomentum_mat = io.loadmat('/home/arpae/RFS_SMPC/catkin_ws/src/carla_ros_connect/scripts/Gomentum_rt3003_ver1.mat')
# gomentum_mat = io.loadmat('/home/arpae-msi/catkin_ws/src/carla_ros_connect/scripts/Gomentum_long_route.mat')
# dgps_mat = io.loadmat('/home/arpae-msi/catkin_ws/src/carla_ros_connect/scripts/dgps_signal.mat')

# ============================================= Translating Coordinate Functions =============================================
def xy2z(mat, x_cur, y_cur):
    s = mat['road_s']
    z = mat['road_z']
    x = mat['road_x']
    y = mat['road_y']

    norm_array = (x - x_cur)**2 + (y - y_cur)**2
    idx_min = np.argmin(norm_array)

    z_cur = z.item(idx_min)
    z_list = [z.item(idx_min - 2), z.item(idx_min - 1), z.item(idx_min)]
    return z_cur, z_list

def xy2s(mat, x_cur, y_cur):
    s = mat['road_s']
    # z = mat['road_z']
    x = mat['road_x']
    y = mat['road_y']

    norm_array = (x - x_cur)**2 + (y - y_cur)**2
    idx_min = np.argmin(norm_array)

    s_cur = s.item(idx_min)
    return s_cur

def latlon_to_XY(lat0, lon0, lat1, lon1):
    ''' 
    Convert latitude and longitude to global X, Y coordinates,
    using an equirectangular projection.
    X = meters east of lon0
    Y = meters north of lat0
    Sources: http://www.movable-type.co.uk/scripts/latlong.html
             https://github.com/MPC-Car/StochasticLC/blob/master/controller.py
    '''
    R_earth = 6371000 # meters
    delta_lat = m.radians(lat1 - lat0)
    delta_lon = m.radians(lon1 - lon0)

    lat_avg = 0.5 * ( m.radians(lat1) + m.radians(lat0) )
    X = R_earth * delta_lon * m.cos(lat_avg)
    Y = R_earth * delta_lat

    return X,Y
# ============================================= End Translating Coordinate Functions =============================================


# ======================================== Carla Camera Sensor Functions ========================================
"""
Processes the data a camera object collects when attached to Carla Actor
"""
def process_img(image, x_size, y_size, num):
    i = np.array(image.raw_data)
    # print(i.shape)
    i2 = i.reshape((y_size,x_size,4))
    i3 = i2[:,:,:3] # except for alpha transparency
    i_resize = cv2.resize(i3, (900,500))
    winname = "First-Person-View"
    cv2.namedWindow(winname)        # Create a named window
    # cv2.moveWindow(winname, 400,30) 
    cv2.moveWindow(winname, 93,0)
    cv2.imshow(winname,i_resize)
    # cv2.imshow("{}".format(num),i_resize)
    cv2.waitKey(1)
    return i3/255.0
# ======================================== End Carla Camera Sensor Functions ========================================


def detect_handler(event):
    actor_we_collide_against = event.other_actor
    print("actor {} is collideded".format(actor_we_collide_against))
    # impulse = event.normal_impulse
    # intensity = math.sqrt(impulse.x**2 + impulse.y**2 + impulse.z**2)


# ============================================ Receive Vehicle State ============================================
# Class to recieve the vehicle's actual state
class VehicleState():
    def __init__(self):        
        # 1) For experiment        
        # rospy.Subscriber("/gps/fix", NavSatFix, self.gps2state)
        # rospy.Subscriber("/imu/data", Imu, self.imu2state)
        
        

        # 2) For simulation / recording
        # rospy.Subscriber("/vehicle/state_est", state_est, self.callback) 
        # rospy.Subscriber("/imu/data", Float32, self.heading2state)

        # 3) For pure-simulation
        rospy.Subscriber("est_state_ros1", StateEst, self.state2carla) 

        self.current_state = {'t':0, 'x':0, 'y':0, 'psi':12,'lat':0, 'lon':0, 'alt':-30, 'v_lon': 10}
        self.state_traj = []
        self.check = 0
        # rospy.spin()

    def callback(self, msg): 
        rospy.loginfo(rospy.get_caller_id() + "x and time are %s %s", msg.x, msg.header.stamp.secs + 1e-9 * msg.header.stamp.nsecs)   
        self.current_state['t'] = msg.header.stamp.secs + 1e-9 * msg.header.stamp.nsecs
        self.current_state['x'] = msg.x
        self.current_state['y'] = msg.y
        self.current_state['psi'] = msg.psi
        self.current_state['lat'] = msg.lat
        self.current_state['lon'] = msg.lon
        self.state_traj.append(self.current_state)
        # to specify when subscriber starts (need offset depending on the map)
        if self.check == 0:
            self.check = 1

    def gps2state(self, msg):
        # rospy.loginfo(rospy.get_caller_id() + "x and time are %s %s", msg.x, msg.header.stamp.secs + 1e-9 * msg.header.stamp.nsecs)   
        self.current_state['t'] = msg.header.stamp.secs + 1e-9 * msg.header.stamp.nsecs
        self.current_state['lat'] = msg.latitude
        self.current_state['lon'] = msg.longitude
        self.current_state['alt'] = msg.altitude
        self.state_traj.append(self.current_state)
        if map_id == 1:
            # REF point at RFS
            LAT0 = 37.917929
            LON0 = -122.331798   
            Psi0 = -1.5         
        elif map_id == 2:
            # Gomentum ref points
            LAT0 = 38.0143934
            LON0 = -122.0135798
            Psi0 = -1.5

        self.current_state['x'], self.current_state['y'] = latlon_to_XY(LAT0, LON0, msg.latitude, msg.longitude)
        # print('lat,lon {},{}'.format(msg.latitude, msg.longitude))
        # print('x,y {} {}'.format(self.current_state['x'], self.current_state['y']))
        if self.check == 0:
            self.check = 1

    def imu2state(self,msg):
        # Get yaw angle from quaternion representation.
        ori = msg.orientation
        quat = (ori.x, ori.y, ori.z, ori.w)
        _, _, yaw = euler_from_quaternion(quat)
        # The yaw/heading given directly by the OxTS is measured counterclockwise from N.
        # That's why we offset by 0.5 * pi and don't need to change the sign.
        psi = yaw + 0.5 * m.pi
        psi = (psi + np.pi) % (2. * np.pi) - np.pi # wrap within [-pi, pi]
        self.current_state['psi'] = psi # yaw (rad), measured counterclockwise from E (global x-axis).

    def heading2state(self, msg):
        self.current_state['psi'] = -msg.data+0.5*m.pi 

    def state2carla(self, msg):
        self.current_state['x'] = msg.x
        self.current_state['y'] = msg.y
        psi = -msg.psi + 0.5 * m.pi
        psi = (psi + np.pi) % (2. * np.pi) - np.pi # wrap within [-pi, pi]
        self.current_state['psi'] = psi
        self.current_state['v_lon'] = msg.v_long
    
# ================================================ End Vehicle State ================================================


# ================================================ Get Traffic State ================================================
class TrafficStates():
    def __init__(self):
        # From actual traffic light (throught cohda)
        rospy.Subscriber("cohda/spat2carla", SPaT, self.cohda2spat)
        self.cohda_state = {'intersection_id':0, 'obstacle_free':True, 'signal_phase':0, 'signal_timing':0.0, 'stop_bar_distance':0.0, 'time_r':0.5, 'tl_state':0 }
    def spat(self, msg):
        self.spats = msg.spats 
    def cohda2spat(self, msg):
        self.cohda_state['intersection_id'] = msg.intersection_id
        self.cohda_state['obstacle_free'] = msg.obstacle_free
        self.cohda_state['signal_phase'] = msg.signal_phase
        self.cohda_state['signal_timing'] = msg.signal_timing
        self.cohda_state['stop_bar_distance'] = msg.stop_bar_distance
        self.cohda_state['time_r'] = msg.time_r
        self.cohda_state['tl_state'] = msg.tl_state
# ================================================ End Traffic State ================================================


# ================================================ Main ================================================
def main():
    # num_loc1 = 0   # Delta street
    # num_loc2 = 0  # Fire House
    # num_loc3 = 0   # before hard curve
    # num_loc4 = 0   # Pearl ave
    num_loc1 = 3   # Delta street
    num_loc2 = 7  # Fire House
    num_loc3 = 7   # before hard curve
    num_loc4 = 10   # Pearl ave
    # num_npcs = num_loc1 + num_loc2 + num_loc3 + num_loc4 
    num_npcs = 200

    npc_status = True # if False, we don't use NPC
    car_lights_on = False
    rospy.init_node('carla_client', anonymous = True)
    state = VehicleState()
    real_traffic = TrafficStates()
    synchronous_master = False
    npc_map_offset_x = 0
    npc_map_offset_y = 0
    # carla agents' list
    actor_list = []
    npc_list = []
    npc_state_list = []

    elapsed_time_py = []
    elapsed_time_carla = []
    # We are going to add an ego vehicle to the simulation
    # We can also create a camera attached to that vehicle
    # and save images generated by the camera

    tl_frozen = True
    try:
        # First of all, we create the client
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)

        # We retrieve the world
        world = client.get_world()

        # Traffic Manager is created
        traffic_manager = client.get_trafficmanager(8000)
        traffic_manager.set_global_distance_to_leading_vehicle(1.5)
        traffic_manager.global_percentage_speed_difference(10.0) # speed limit can be exceeded by -xx% (percent is applied in a negative way)
        # traffic_manager.set_synchronous_mode(False)

        # Get blueprints for adding new actors into the simulation.
        blueprint_library = world.get_blueprint_library()
        blueprint_library_npc = world.get_blueprint_library()

        # Traffic lights
        # tls = world.get_actors().filter('traffic.traffic_light*')
        # grp = tls[0].get_group_traffic_lights()
        # print("grp, tls: {}, {}".format(grp, tls))

        # Spawn NPC vehicles
        if npc_status:
            '''
            ----------------
            NPC vehicles
            ----------------
            '''
            # spawn_points = world.get_map().get_spawn_points()

            # # force to increase the number of spawn points
            # for k in range(num_npcs-len(spawn_points)):
            #     tf = random.choice(world.get_map().get_spawn_points())        
            #     # Fix the x,y,z position to check where it spawns
            #     tf.location.x += 2*k
            #     tf.location.y += 4*k         
            #     spawn_points.append(tf)

            # force to fix spawn points around the origin(parking lot)
            spawn_points = []
            for k in range(num_npcs):
                tf = random.choice(world.get_map().get_spawn_points())  
                # For RFS map
                if map_id == 1:
                    # at the parking lot
                    # tf.location.x = 144-5*k
                    # tf.location.y = -290+11*k
                    # tf.location.z = 1.5
                    # tf.rotation.yaw = 90
                    spec=client.get_world().get_spectator()
                    tf.location.x = 134-25*k
                    tf.location.y = -269+56*k
                    tf.location.z = 1.5
                    tf.rotation.yaw = 108
                    # import pdb; pdb.set_trace()
                    # on the lane 
                    # tf.location.x = 169-5*k
                    # tf.location.y = -272+11*k
                    # tf.location.z = 1.
                    # tf.rotation.yaw = 37+180                  
                elif map_id == 2:
                # delta street
                    if k < num_loc1:
                        # tf.location.x = -350+3*k
                        # tf.location.y = -80+1*k
                        tf.location.x = 130-6*k
                        tf.location.y = 97+9*k
                        tf.location.z = 32
                        tf.rotation.yaw = 130         
                # around traffic light (fire house)
                    elif k >= num_loc1 and k < num_loc1+num_loc2:
                        tf.location.x = -193+5*(k-num_loc1)
                        tf.location.y = 45+4*(k-num_loc1)
                        tf.location.z = 20
                        tf.rotation.yaw = -145      
                # Hard curve (after traffic light)
                    elif k >= num_loc1+num_loc2 and k < num_loc1+num_loc2+num_loc3:
                        tf.location.x = -198+7.2*(k-num_loc1-num_loc2) 
                        tf.location.y = -128+4*(k-num_loc1-num_loc2)
                        # tf.location.x = -215+7.2*k
                        # tf.location.y = -134+4*k
                        tf.location.z = 24
                        tf.rotation.yaw = -145
                    elif k >= num_loc1+num_loc2+num_loc3 and k < num_npcs:
                # Pearl Ave before traffic light 
                        tf.location.x = 118+7*(k-num_loc1-num_loc2-num_loc3)
                        tf.location.y = -89+3.6*(k-num_loc1-num_loc2-num_loc3)
                        tf.location.z = 30
                        tf.rotation.yaw = 35    

                spawn_points.append(tf)
                print("try: {}, pos: {},{},{}".format(k,tf.location.x, tf.location.y, tf.location.z))

            number_of_spawn_points = len(spawn_points)

            if num_npcs <= number_of_spawn_points:
                random.shuffle(spawn_points)
            # elif num_npcs > number_of_spawn_points:
            #     num_npcs = number_of_spawn_points

            # @todo cannot import these directly.
            SpawnActor = carla.command.SpawnActor
            SetAutopilot = carla.command.SetAutopilot
            SetVehicleLightState = carla.command.SetVehicleLightState
            FutureActor = carla.command.FutureActor

            # ------------------------
            # Spawn vehicles
            # ------------------------
            batch = []
            # print("spawn_points {}".format(spawn_points))
            print("spawn_points length: {}".format(len(spawn_points)))
            # blueprint_npc = random.choice(blueprint_library_npc.filter('vehicle'))
            for n, transform_npc in enumerate(spawn_points):                
                if n >= num_npcs:
                    break
                blueprint_npc = random.choice(blueprint_library_npc.filter('vehicle'))
                while blueprint_npc.id in ["vehicle.bh.crossbike", "vehicle.harley-davidson.low_rider", "vehicle.yamaha.yzf", "vehicle.kawasaki.ninja"]:
                    blueprint_npc = random.choice(blueprint_library_npc.filter('vehicle'))
                if blueprint_npc.has_attribute('color'):
                    color = random.choice(blueprint_npc.get_attribute('color').recommended_values)
                    blueprint_npc.set_attribute('color', color)
                if blueprint_npc.has_attribute('driver_id'):
                    driver_id = random.choice(blueprint_npc.get_attribute('driver_id').recommended_values)
                    blueprint_npc.set_attribute('driver_id', driver_id)
                blueprint_npc.set_attribute('role_name', 'autopilot')
                print("blueprint: {}".format(blueprint_npc.id))
                print("trans x:{}, y:{}".format(transform_npc.location.x, transform_npc.location.y))
                # prepare the light state of the cars to spawn
                light_state = vls.NONE
                if car_lights_on:
                    light_state = vls.Position | vls.LowBeam | vls.LowBeam

                # spawn the cars and set their autopilot and light state all together
                batch.append(SpawnActor(blueprint_npc, transform_npc)
                    .then(SetAutopilot(FutureActor, True, traffic_manager.get_port()))
                    .then(SetVehicleLightState(FutureActor, light_state)))

                # npc = world.spawn_actor(blueprint_npc, transform_npc)
                # npc.set_autopilot(True)
                # npc_list.append(npc)
                # print('created {} at {}'.format(npc.type_id, transform_npc))
            # client.apply_batch(batch)
            
            for response in client.apply_batch_sync(batch, synchronous_master):
                if response.error:
                    logging.error(response.error)
                else:
                    npc_list.append(response.actor_id)


        """Publish NPC info and traffic light info"""
        pub = rospy.Publisher('carla/npc_state_array', NpcStateArray, queue_size = 10)        
        pub_traffic = rospy.Publisher('carla/spats', SPaTArray, queue_size = 10)
        rate = rospy.Rate(50)


        # --------------------
        # Ego vehicle
        #---------------------
        # Pick a blueprint 
        bp = random.choice(blueprint_library.filter('vehicle.bmw.grandtourer'))
        # bp = random.choice(blueprint_library.filter('vehicle'))

        # Test an ego vehicle's blueprint attribute (e.g. color)
        if bp.has_attribute('color'):
            # color = random.choice(bp.get_attribute('color').recommended_values)
            color ='255,0,0'
            bp.set_attribute('color', color)

        # Obtain the Carla.transform for random spawn_points
        transform = random.choice(world.get_map().get_spawn_points())
        
        # Fix the x,y,z position to check where it spawns

        if map_id == 1:            
            # transform.location.x = 138
            # transform.location.y =-50
            # transform.location.z = 3
            # transform.rotation.yaw = 0
            # transform.rotation.pitch = 0
            # transform.rotation.roll = 0
            transform.location.x = 118
            transform.location.y =-240
            transform.location.z = 1.5
            transform.rotation.yaw = 109
            transform.rotation.pitch = 0
            transform.rotation.roll = 0
        elif map_id == 2:
            transform.location.x = 136.468244438
            transform.location.y = -118.663684215
            transform.location.z = 17.75
            transform.rotation.yaw = 40
            transform.rotation.pitch = 0
            transform.rotation.roll = 0

        # Tell the world to spawn the vehicle.
        print(transform.location.x,transform.location.y,transform.location.z)
        vehicle = world.spawn_actor(bp, transform)
        # import pdb;pdb.set_trace()        

        # To destory the vehicles afterwards, we are storing all the actors we create 
        actor_list.append(vehicle)
        print('created %s' % vehicle.type_id)

        # Can set autopilot
        # vehicle.set_autopilot(True)

        # ===== Carla Camera on Ego Vehicle ===== 
        """
        # We can add a camera attached to the vehicle.
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(x=1.6, z=1.1))
        camera_bp.set_attribute('fov','60')
        camera_bp.set_attribute('image_size_x', '900')
        camera_bp.set_attribute('image_size_y', '500')
        camera_bp.set_attribute('iso', '100')
        camera_bp.set_attribute('shutter_speed', '200')
        camera_bp.set_attribute('exposure_mode', 'histogram')
        camera_bp.set_attribute('exposure_compensation', '-1.5')
        camera_bp.set_attribute('exposure_min_bright', '1')
        camera_bp.set_attribute('exposure_max_bright', '2')
        # camera_bp.set_attribute('exposure_min_bright', '20')
        # camera_bp.set_attribute('exposure_max_bright', '30')
        camera_bp.set_attribute('exposure_speed_up', '3')
        camera_bp.set_attribute('exposure_speed_down', '1.0')
        # camera_bp.set_attribute('shutter_speed', '50')
        # camera_bp.set_attribute('lens_circle_multiplier','1.0')
        # camera_bp.set_attribute('lens_y_size','0.8')
        # camera_bp.set_attribute('lens_k','1000000')
        # camera_bp.set_attribute('lens_kcube','-0.1')
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actor_list.append(camera)
        # print('created %s' % camera.type_id)

        # camera_bp1 = blueprint_library.find('sensor.camera.rgb')
        # camera_transform1 = carla.Transform(carla.Location(x=1.6, z=2.4))
        # camera_bp1.set_attribute('fov','120')
        # camera_bp1.set_attribute('image_size_x', '1000')
        # camera_bp1.set_attribute('image_size_y', '400')
        # # camera_bp1.set_attribute('lens_kcube','100000')
        # camera1 = world.spawn_actor(camera_bp1, camera_transform1, attach_to=vehicle)
        # actor_list.append(camera1)
        # print('created %s' % camera1.type_id)

        # # Now we register the function that will be called each time the sensor
        # # receives an image. In this example we are saving the image to disk
        # # converting the pixels to gray-scale.
        # cc = carla.ColorConverter.LogarithmicDepth
        # cc = carla.ColorConverter.Raw
        # camera.listen(lambda image: image.save_to_disk('FPS_out/%06d.png' % image.frame, cc))
        camera.listen(lambda image: process_img(image, camera_bp.get_attribute('image_size_x').as_int(), camera_bp.get_attribute('image_size_y').as_int(),1))
        # camera1.listen(lambda image: process_img(image, camera_bp1.get_attribute('image_size_x').as_int(), camera_bp1.get_attribute('image_size_y').as_int(),2))
        """
        # ===== End Carla Camera =====
        # import pdb; pdb.set_trace()

        """
        # Collision detector
        detector_bp = blueprint_library.find('sensor.other.collision')
        detector = world.spawn_actor(detector_bp, carla.Transform(), attach_to=vehicle)
        detector.listen(lambda event: detect_handler(event))
        """

        # Get a map to check geolocation
        cur_map = world.get_map()
        loc = vehicle.get_location()
        
        # Check the origin's gps coordinate
        check_loc = vehicle.get_location()
        check_loc.x = 0
        check_loc.y = 0
        check_loc.z = 0
        origin_gps = cur_map.transform_to_geolocation(check_loc)
        # print('origin... lat, long, alt : {}, {}, {}'.format(origin_gps.latitude, origin_gps.longitude, origin_gps.altitude))
        # print("\n")
        lat_o = origin_gps.latitude
        lon_o = origin_gps.longitude
        if map_id == 1:
            # RFS ref points
            LAT0 = 37.917929
            LON0 = -122.331798
        elif map_id == 2:
            # Gomentum ref points
            LAT0 = 38.0143934
            LON0 = -122.0135798
        offset_x, offset_y = latlon_to_XY(LAT0, LON0, lat_o, lon_o)

        # we will use offset like this : state - offset
        # print('offset x, y : {}, {}'.format(offset_x, offset_y))
        # print("\n")
        # pdb.set_trace()

        world.set_weather(carla.WeatherParameters.ClearSunset)
        # Run the client to communicate with servers
        i = 0
        j_record = 0
        tl_enforce = 0
        setup_flag = 0
        while not rospy.is_shutdown():
            print(3*"\n")
            start = time.time()
            # print(world.get_weather())
            '''
            Obtain ego's CARLA Coordinates (xego_cur, yego_cur)
            '''            
            # current_state : coordinate of real GPS referred to REF GPS / offset : RFS GPS's coordinate from carla origin
            xego_cur = state.current_state['x'] - offset_x 
            yego_cur = state.current_state['y'] - offset_y
            yego_cur = -yego_cur 
            npc_state_list = []

            # Obtain NPC vehicle's information (take only portion of surrouding vehicles)
            for actor_id in npc_list:                  
                actor_temp = world.get_actor(actor_id)
                # Force NPCs not to do lane change
                traffic_manager.auto_lane_change(actor_temp,False)  

                # print("speed limit is {}".format(actor_temp.get_speed_limit()))
                transform_temp = actor_temp.get_transform() # tr.location (x,y,z), tr.rotation(roll,pitch,yaw)
                velocity_temp = actor_temp.get_velocity() # vel.x, vel.y, vel.z
                ang_velocity_temp = actor_temp.get_angular_velocity()
                # TODO: Pick the portion of surrouding vehicles
                DIST_MEASURE = 500
                if (transform_temp.location.x - xego_cur)**2 + (transform_temp.location.y - yego_cur)**2 >= DIST_MEASURE**2:                        
                    pass
                else:
                    # print(transform_temp, velocity_temp)
                    # print("gap current 150: {}".format(np.sqrt((transform_temp.location.x - xego_cur)**2 + (transform_temp.location.y - yego_cur)**2 )))
                    
                    # Populate msg for npc state
                    npc_state_msg = NpcState()
                    # Send location without carla's offset to NUVO 

                    npc_state_msg.loc.x = transform_temp.location.x + offset_x 
                    npc_state_msg.loc.y = -(transform_temp.location.y - offset_y) 
                    npc_state_msg.rot.z = transform_temp.rotation.yaw 

                    # if we are at gomentum, compensate the offset
                    if map_id == 2: 
                        # pass
                        s_cur_npc = xy2s(gomentum_mat, npc_state_msg.loc.x, npc_state_msg.loc.y)
                        # small loop
                        if s_cur_npc >= 500 and s_cur_npc<=630:
                            npc_map_offset_x = -1*sin(npc_state_msg.rot.z /180*3.1415)
                            npc_map_offset_y = 1*cos(npc_state_msg.rot.z /180*3.1415)
                        elif s_cur_npc >630 and s_cur_npc <= 850:
                            npc_map_offset_x = -(2.3/260)*(s_cur_npc-500)*sin(npc_state_msg.rot.z/180*3.1415)
                            npc_map_offset_y = (2.3/260)*(s_cur_npc-500)*cos(npc_state_msg.rot.z/180*3.1415)
                        npc_state_msg.loc.x -= npc_map_offset_x
                        npc_state_msg.loc.y -= npc_map_offset_y

                        # large loop for baseline

                        s_cur_npc = xy2s(gomentum_mat, npc_state_msg.loc.x, npc_state_msg.loc.y)
                        if s_cur_npc >= 0 and s_cur_npc < 140:
                            npc_map_offset_x = -1.1*sin(npc_state_msg.rot.z/180*3.1415)
                            npc_map_offset_y = 1.1*cos(npc_state_msg.rot.z/180*3.1415)
                        elif s_cur_npc >= 140 and s_cur_npc < 250:
                            npc_map_offset_x = -1.2*sin(npc_state_msg.rot.z/180*3.1415)
                            npc_map_offset_y = 1.2*cos(npc_state_msg.rot.z/180*3.1415)
                        elif s_cur_npc >= 250 and s_cur_npc < 370:
                            npc_map_offset_x = -1.2*sin(npc_state_msg.rot.z/180*3.1415)
                            npc_map_offset_y = 1.2*cos(npc_state_msg.rot.z/180*3.1415)
                        elif s_cur_npc >= 370 and s_cur_npc < 500:
                            npc_map_offset_x = -1.5*sin(npc_state_msg.rot.z/180*3.1415)
                            npc_map_offset_y = 1.5*cos(npc_state_msg.rot.z/180*3.1415)
                        elif s_cur_npc >= 500 and s_cur_npc < 800:
                            npc_map_offset_x = -1.3*sin(npc_state_msg.rot.z/180*3.1415)
                            npc_map_offset_y = 1.3*cos(npc_state_msg.rot.z/180*3.1415)
                        elif s_cur_npc >= 800:
                            npc_map_offset_x = -1.1*sin(npc_state_msg.rot.z/180*3.1415)
                            npc_map_offset_y = 1.1*cos(npc_state_msg.rot.z/180*3.1415)
                        npc_state_msg.loc.x -= npc_map_offset_x
                        npc_state_msg.loc.y += npc_map_offset_y


                        s_cur = xy2s(gomentum_mat, state.current_state['x'], state.current_state['y'])
                        if s_cur >= 430 and s_cur <470:
                            dgps_comp_offset_x = -1*sin(trans.rotation.yaw/180*3.1415)
                            dgps_comp_offset_y = 1*cos(trans.rotation.yaw/180*3.1415)
                    elif map_id == 1:
                        # manula tuning for fitting to carla map
                        npc_map_offset_x = 1.2*sin(npc_state_msg.rot.z/180*3.1415)
                        npc_map_offset_y =  -1.2*cos(npc_state_msg.rot.z/180*3.1415)
                        # npc_state_msg.loc.x -= npc_map_offset_x
                        # npc_state_msg.loc.y += npc_map_offset_y

                    
                    npc_state_msg.loc.z = transform_temp.location.z
                    npc_state_msg.rot.x = transform_temp.rotation.roll
                    npc_state_msg.rot.y = transform_temp.rotation.pitch
                    npc_state_msg.vel.x = velocity_temp.x
                    npc_state_msg.vel.y = velocity_temp.y
                    npc_state_msg.vel.z = velocity_temp.z
                    npc_state_msg.ang_vel.x = ang_velocity_temp.x
                    npc_state_msg.ang_vel.y = ang_velocity_temp.y
                    npc_state_msg.ang_vel.z = ang_velocity_temp.z
                    # compensate the OxTS location in the trunk
                    npc_state_msg.loc.x  += -0.4*sin(npc_state_msg.rot.z/180*3.1415) +1.7*cos(npc_state_msg.rot.z/180*3.1415)
                    npc_state_msg.loc.y -= 0.4*cos(npc_state_msg.rot.z/180*3.1415) +1.7*sin(npc_state_msg.rot.z/180*3.1415) 
                    # print("offset : {},{}".format())
                    npc_state_msg.rot.z = -1*transform_temp.rotation.yaw
                    npc_state_list.append(npc_state_msg)
                    # mpc map offset compensation

                print("npc number / current location: {} / {},{},{}".format(actor_id, transform_temp.location.x+offset_x, -transform_temp.location.y+offset_y, transform_temp.location.z))
                print('npc vel {}'.format(sqrt(velocity_temp.x**2+velocity_temp.y**2)))                
                # Waypoints
                # waypt = world.get_map().get_waypoint(transform_temp.location)
                # print("{}-th waypt,lane_id: {},{}".format(actor_id, waypt, waypt.lane_id))

            # Assign npc_state into npc_state.msg
            npc_states_msg = NpcStateArray()  
            # npc_states_msg = NpcState() 
            # npc_states_msg.loc.x = 1 
            # npc_states_msg.npc_states = [npc_state_list[0], npc_state_list[1]]  
            npc_states_msg.npc_states = npc_state_list 
            # TODO : sort out this surrounding npc list
            # e.g. front, rear, next front, next rear


            """
            Traffic light controller
                0: Need to find what traffic light is the closest one (also sort out them in order)
                1: Get the carla type data
                2: Sync with cohda
            """

            # 0. Sort out traffic lights in order (MAYBE USE s coordinate, assign a traffic light to each s)
            # If ego vehicle is at traffic light or not
            if vehicle.is_at_traffic_light():
                print("ego is affected by a traffic light")
                tl_cur = vehicle.get_traffic_light()
            else:
                print("A traffic light is far away from ego")

            # Get all traffic lights    
            tl_list = world.get_actors().filter('traffic.traffic_light*')
            ego_s = xy2s(gomentum_mat, state.current_state['x'], state.current_state['y'])
            tl_info_list = []
            tl_ours_list = []
            # print("tl_list, num: {}, {}".format(tl_list, len(tl_list)))
            for tl in tl_list:
                tl_loc = tl.get_location()
                tl_s = xy2s(gomentum_mat, tl_loc.x + offset_x, -(tl_loc.y - offset_y))
                # tl_s -= 26
                if int(tl_loc.x) == -113:
                    tl_s -= 20
                elif int(tl_loc.x) == -240:
                    tl_s -= 19
                elif int(tl_loc.x) == -155:
                    tl_s -= 16
                elif int(tl_loc.x) == 19:
                    tl_s -= 28
                elif int(tl_loc.x) == 209:
                    tl_s -= 21
                elif int(tl_loc.x) == 140:
                    tl_s -= 25

                tl_info = {'s': tl_s, 'id':tl.id, 'tl':tl, 'x': tl_loc.x}
                tl_info_list.append(tl_info)
                # print("tl:{}, tl loc:{}, tl_loc_s:{}".format(tl, tl_loc, tl_s))

                # Pick traffic lights along our path
                if int(tl_loc.x) in [-113,-240,-155,19,209,140]:
                    tl_ours_list.append(tl_info)
                    

            spat_list = [] 
            dd = False
            # If tl_ours_list is not empty (traffic lights we want)
            if tl_ours_list and dd == False:                
                # Sort traffic lights from least to greatest
                tl_ours_sorted = sorted(tl_ours_list, key=lambda d: d['s'])      
                # print("tl_list, tl_sorted : {}, {}".format(tl_ours_list, tl_ours_sorted))

                """Set the initial cycle for traffic lights"""
                g_time_init = 30
                y_time_init = 2
                g_time_p = 10
                r_time_init = 15
                r_time_init_p  = r_time_init - g_time_p
                if setup_flag == 0:                
                    for tl_info in tl_ours_sorted:                
                        tl = tl_info['tl']
                        if int(tl_info['x']) == -113:
                            # Entrance
                            tl_p_info = [ele for ele in tl_info_list if int(ele['x']) == -97]
                            tl_p = tl_p_info[0]['tl']
                            tl_p.set_green_time(1)
                            tl_p.set_yellow_time(0)
                            tl_p.set_red_time(30)
                            tl.set_green_time(g_time_init)
                            tl.set_yellow_time(y_time_init)
                            tl.set_red_time(r_time_init)
                        elif int(tl_info['x']) == -155:
                            # 1ST Intersection
                            g_time_init1 = 20
                            y_time_init1 = 2
                            g_time_p1 = 15
                            r_time_init1 = 20
                            r_time_init_p1 = r_time_init1 - g_time_p1
                            tl_p_info = [ele for ele in tl_info_list if int(ele['x']) == -170]
                            tl_p = tl_p_info[0]['tl']
                            tl_p.set_green_time(g_time_p1)
                            tl_p.set_yellow_time(0)
                            tl_p.set_red_time(0.1)
                            tl.set_green_time(g_time_init1)
                            tl.set_yellow_time(y_time_init1)
                            tl.set_red_time(r_time_init_p1)
                        elif int(tl_info['x']) == 140:
                            tl_p_info = [ele for ele in tl_info_list if int(ele['x']) == 146]
                            tl_p = tl_p_info[0]['tl']
                            tl_p.set_green_time(0.1)
                            tl_p.set_yellow_time(0)
                            tl_p.set_red_time(0.1)
                            tl.set_green_time(g_time_init)
                            tl.set_yellow_time(y_time_init)
                            tl.set_red_time(r_time_init)
                        else:
                            # single 
                            tl.set_green_time(g_time_init)
                            tl.set_yellow_time(y_time_init)
                            tl.set_red_time(r_time_init)
                    setup_flag = 1
                else:
                    pass
                    print("setup done")
                    print("\n")
                    
                # Find a next traffic light by comparing 's'
                tl_next_idx = 0
                # print("tl_ours_sorted {}".format(tl_ours_sorted))
                for tl_info in tl_ours_sorted:
                    # print("tl_next{}, len{}".format(tl_next_idx,len(tl_ours_sorted)))
                    # print("egos, tl s: {},{}".format(ego_s, tl_info['s']))
                    if ego_s > 1100:
                        ego_s =- 1316.4

                    if ego_s >= tl_info['s'] + 5 and  tl_next_idx < len(tl_ours_sorted):
                        tl_next_idx += 1
                    else:
                        break
                    if tl_next_idx >=len(tl_ours_sorted):
                        # last traffic lgiht
                        tl_next_idx = 0

                tl_next_info = tl_ours_sorted[tl_next_idx]

                # Check corresponding pairs
                tl = tl_next_info['tl']
                pair_bool = True
                if int(tl_next_info['x']) == -113:
                    tl_p_info = [ele for ele in tl_info_list if int(ele['x']) == -97]
                    tl_p = tl_p_info[0]['tl']
                elif int(tl_next_info['x']) == -155:
                    tl_p_info = [ele for ele in tl_info_list if int(ele['x']) == -170]
                    tl_p = tl_p_info[0]['tl']
                elif int(tl_next_info['x']) == 140:
                    tl_p_info = [ele for ele in tl_info_list if int(ele['x']) == 146]
                    tl_p = tl_p_info[0]['tl']
                else:
                    pair_bool = False
                    tl_p = None
                # print("tl_p, type {}, {}".format(tl_p, type(tl_p)))
                # 1. Get the carla type data 
                """Traffic Lights
                    i) If there is no pair of traffic light (only 1 tl)
                    ii) 2 tls : tl, tl_p
                """
                # i)
                if pair_bool == False:
                    # tl.set_state(carla.TrafficLightState.Green)
                    # tl.set_green_time(3)
                    # tl.set_yellow_time(3)
                    # tl.set_red_time(30)
                    time_g = tl.get_green_time()
                    time_y = tl.get_yellow_time()
                    time_r = tl.get_red_time()
                    signal_timing = tl.get_green_time() - tl.get_elapsed_time()
                    signal_phase =  tl.get_state() 
                    # print("single tl {}'s state:{}, remaining time: {}".format(tl.get_location(),signal_phase,signal_timing))
                else:
                    # ii)
                    # tl.set_state(carla.TrafficLightState.Green)
                    # if tl_enforce == 0:
                    #     tl.set_green_time(3)
                    #     tl.set_yellow_time(3)
                    #     tl.set_red_time(30)
                    # tl_p.set_green_time(0.5)
                    # tl_p.set_yellow_time(0.1)
                    # tl_p.set_red_time(0.5)

                    # get time period
                    time_g = tl.get_green_time()
                    time_y = tl.get_yellow_time()
                    time_r = tl.get_red_time()
                    time_g_p = tl_p.get_green_time()
                    time_y_p = tl_p.get_yellow_time()
                    time_r_p = tl_p.get_red_time()
                    if int(tl_next_info['x']) == -113: 
                        # first tl, it accidently loses binding
                        signal_phase =  tl.get_state()
                        signal_timing = tl.get_green_time() - tl.get_elapsed_time()
                    else:
                        signal_phase =  tl.get_state()
                        signal_timing = tl.get_green_time() - tl.get_elapsed_time()
                        # other tls, it accidently loses binding
                        if signal_phase in [carla.TrafficLightState.Green, carla.TrafficLightState.Yellow]:
                            # tl is Green or Yellow
                            signal_timing = tl.get_green_time() - tl.get_elapsed_time()
                            tl_frozen = False
                        else:
                            # tl is Red
                            if tl_p.get_state() in [carla.TrafficLightState.Green, carla.TrafficLightState.Yellow]:
                                # tl_p: Green or Yellow, tl Red & Frozen
                                tl_frozen = True
                                if tl_p.get_state() == carla.TrafficLightState.Green:
                                    # p : Green
                                    signal_timing = tl_p.get_green_time() - tl_p.get_elapsed_time() + time_y_p + time_r_p 
                                else:
                                    # p : Yellow+ time_r_p
                                    pass
                            elif tl_p.get_state() == carla.TrafficLightState.Red and tl_frozen == False:
                                # tl_p : Red, tl : Red & Active                             
                                signal_timing = tl.get_green_time() - tl.get_elapsed_time() + time_g_p + time_y_p + time_r_p 
                            elif tl_p.get_state() == carla.TrafficLightState.Red and tl_frozen == True:
                                # tl: Red & Frozen (p:Red)
                                signal_timing = tl_p.get_green_time() - tl_p.get_elapsed_time() 

                    # print("pair1 tl {}'s state:{}, remaining time: {}".format(tl.get_location(),signal_phase,signal_timing))
                    # print("pair2 tl_p {}'s state:{}, elapsed_sec, p elapsed_sec: {},{}".format(tl_p.get_location(),tl_p.get_state(), tl.get_elapsed_time(), tl_p.get_elapsed_time()))
                    
                    # CARLA SPaT's list (hope spats of traffic light from closest to farthest)
                    # for tl in world.get_actors().filter('traffic.traffic_light*'):
                    #     # tl_list = tl.get_group_traffic_lights()   #takes time
                    #     # print('tl list : {}'.format(tl_list))
                    #     print("\n")
                    #     print("pole index {}".format(tl.get_pole_index()))
                    #     print("elapsed_sec in traffic light group: {}".format(tl.get_elapsed_time()))
                    #     tl_elapse = tl.get_elapsed_time()
                    #     if tl.get_state() == carla.TrafficLightState.Green:
                    #         print('green')
                    #         time_g = tl.get_green_time() - tl_elapse
                    #         time_y = tl.get_yellow_time()
                    #         time_r = tl.get_red_time()
                    #     elif tl.get_state() == carla.TrafficLightState.Yellow:
                    #         print('yellow')
                    #         time_y = tl.get_green_time() - tl_elapse
                    #         time_g = tl.get_green_time()
                    #         time_r = tl.get_red_time()
                    #     else:
                    #         tl_list = [tl]
                    #         time_r = 0
                    #         for tl_temp in tl_list:
                    #             if tl_temp != tl:
                    #                 if tl_temp.get_state() ==carla.TrafficLightState.Green:
                    #                     time_r = tl_temp.get_green_time()+tl_temp.get_yellow_time()+tl_temp.get_red_time()-tl_elapse
                    #                 elif tl_temp.get_state() ==carla.TrafficLightState.Yellow:
                    #                     time_r = tl_temp.get_green_time()+tl_temp.get_red_time()-tl_elapse
                    #                 else:
                    #                     time_r = tl_temp.get_green_time()-tl_elapse
                    #         time_y = tl.get_yellow_time()
                    #         time_g = tl.get_green_time()
                    #     print("tl {}'s state:{}, period time g, y, r: {},{},{}".format(tl,tl.get_state(),tl.get_green_time(), tl.get_yellow_time(), tl.get_red_time()))
                    #     print("tl {}'s state:{}, remaining time g, y, r: {},{},{}".format(tl,tl.get_state(),time_g, time_y, time_r))
                    #     # print("tl's frozen: {}".format(tl.is_frozen()))

                    #     tl_loc = tl.get_location()
                    #     print("tl's location {}".format(tl_loc))



                        
                    # Populate msg for traffic light
                    # spat_msg = SPaT()
                    # # Send all data
                    # spat_msg.time_r = tl.get_red_time()
                    # spat_msg.time_y = tl.get_yellow_time()
                    # spat_msg.time_g = tl.get_green_time()
                    # spat_msg.s = xy2s(gomentum_mat, tl_loc.x + offset_x, -(tl_loc.y - offset_y))
                    # if tl.get_state() == carla.TrafficLightState.Green:
                    #     spat_msg.tl_state = 2
                    # elif tl.get_state() == carla.TrafficLightState.Yellow:
                    #     spat_msg.tl_state = 1
                    # else:
                    #     spat_msg.tl_state = 0
                    # spat_list.append(spat_msg)

                # 2. Sync with cohda
                if pair_bool == False:
                    # SINGLE TL
                    if real_traffic.cohda_state['signal_phase'] == 3:
                        # RED
                        tl.set_state(carla.TrafficLightState.Red)
                        # tl.set_red_time(real_traffic.cohda_state['signal_timing'])
                        signal_timing = real_traffic.cohda_state['signal_timing']
                    elif real_traffic.cohda_state['signal_phase'] == 6:
                        # Green
                        tl.set_state(carla.TrafficLightState.Green)
                        # tl.set_green_time(real_traffic.cohda_state['signal_timing'])
                        signal_timing = real_traffic.cohda_state['signal_timing']
                    elif real_traffic.cohda_state['signal_phase'] == 8:
                        # Yellow
                        tl.set_state(carla.TrafficLightState.Yellow)
                        # tl.set_yellow_time(real_traffic.cohda_state['signal_timing'])
                        signal_timing = real_traffic.cohda_state['signal_timing']
                    else:
                        print("single & no cohda yet single")
                else:
                    # DOUBLE TLs
                    # time_gap = real_traffic.cohda_state['signal_timing'] - signal_timing # real - virtual
                    # if signal_timing + time_gap < 0.1:
                    #     # time to change
                    #     if real_traffic.cohda_state['signal_phase'] == 3:
                    #         #RED TO GREEN
                    #         tl.set_state(carla.TrafficLightState.Green)
                    #     elif real_traffic.cohda_state['signal_phase'] == 6:
                    #         #GREEN TO YELLOW
                    #         tl.set_state(carla.TrafficLightState.Yellow)
                    #     elif real_traffic.cohda_state['signal_phase'] == 8:
                    #         tl.set_state(carla.TrafficLightState.Red)

                    if real_traffic.cohda_state['signal_phase'] == 3 or real_traffic.cohda_state['tl_state'] == 3:
                        # REDz
                        tl.set_state(carla.TrafficLightState.Red)
                        # tl.set_red_time(self.cohda_state['signal_timing'])
                        signal_timing = real_traffic.cohda_state['signal_timing']
                        # tl.set_red_time(real_traffic.cohda_state['time_r'])
                        # tl_p.set_red_time(0)
                        # tl_p.set_green_time(0)
                        # tl_p.set_yellow_time(0)

                    elif real_traffic.cohda_state['signal_phase'] == 6 or real_traffic.cohda_state['tl_state'] == 6:
                        # Green
                        tl.set_state(carla.TrafficLightState.Green)
                        # tl.set_green_time(self.cohda_state['signal_timing'])
                        signal_timing = real_traffic.cohda_state['signal_timing']
                        # tl.set_green_time(real_traffic.cohda_state['time_r'])
                        # tl_p.set_red_time(0)
                        # tl_p.set_green_time(0)
                        # tl_p.set_yellow_time(0)
                    elif real_traffic.cohda_state['signal_phase'] == 8 or real_traffic.cohda_state['tl_state'] == 8:
                        # Yellow
                        tl.set_state(carla.TrafficLightState.Yellow)
                        # tl.set_yellow_time(self.cohda_state['signal_timing'])
                        signal_timing = real_traffic.cohda_state['signal_timing']
                        # tl.set_yellow_time(real_traffic.cohda_state['time_r'])
                        # tl_p.set_red_time(0)
                        # tl_p.set_green_time(0)
                        # tl_p.set_yellow_time(0)
                    else:
                        print("pair & no cohda yet double")
                        # print("tl_enforce:{}".format(tl_enforce))
                        # if (tl.get_state() == carla.TrafficLightState.Red) and signal_timing <=3:
                        #     tl.set_state(carla.TrafficLightState.Green)
                        #     tl.set_green_time(10)
                            #     tl_enforce = 100
                    #         # YELLOW TO RED
          
                    # TODO: Need to find what traffic light is the closest one to ego vehicle

                # Populate msg for traffic light
                spat_msg = SPaT()
                # Send all data
                # spat_msg.time_r = tl.get_red_time()
                # spat_msg.time_y = tl.get_yellow_time()
                # spat_msg.time_g = tl.get_green_time()
                tl_loc = tl.get_location()

                tl_s = xy2s(gomentum_mat, tl_loc.x + offset_x, -(tl_loc.y - offset_y))
                if int(tl_loc.x) == -113:
                    tl_s -= 20
                elif int(tl_loc.x) == -240:
                    tl_s -= 19
                elif int(tl_loc.x) == -155:
                    tl_s -= 16
                elif int(tl_loc.x) == 19:
                    tl_s -= 28
                elif int(tl_loc.x) == 209:
                    tl_s -= 21
                elif int(tl_loc.x) == 140:
                    tl_s -= 25
                spat_msg.s = tl_s

                if tl.get_state() == carla.TrafficLightState.Green:
                    spat_msg.signal_phase = 6
                    spat_msg.tl_state = 6
                elif tl.get_state() == carla.TrafficLightState.Yellow:
                    spat_msg.signal_phase = 8
                    spat_msg.tl_state = 8
                else:
                    spat_msg.signal_phase = 3
                    spat_msg.tl_state = 3
                spat_msg.signal_timing = signal_timing
                spat_msg.time_r = signal_timing

            else:
                # no spat list (empty list we want)
                spat_msg = SPaT()
                pass
             
            spat_list.append(spat_msg)



            # TODO: Obtain traffic light information
            traffic_msg = SPaTArray()
            traffic_msg.spats = spat_list

  
            rospy.loginfo(rospy.get_time())
            # Publish npc_states msg
            pub.publish(npc_states_msg)
            pub_traffic.publish(traffic_msg)
            rate.sleep()
            j_record += 1

            if synchronous_master:
                world.tick() # sync mode
            else:
                # current time
                snap = world.wait_for_tick() #async mode : wait for a server tick                
                
                # Before recieving the vehicle's state
                if state.check == 0:
                    offset = [loc.x-state.current_state['x'],loc.y-state.current_state['y']] 
                    # print("offset {}".format(offset))
                    # print("state check {}".format(state.check))
                # At the point when recieving the vehicle's state
                elif state.check == 1:
                    offset = [loc.x-state.current_state['x'],loc.y-state.current_state['y']] # to adjust the origin
                    # print("offset {}".format(offset))
                    # print("state check {}".format(state.check))
                    state.check = 2

                # Specify simulation time (world time)
                ts = snap.timestamp
                print("elapsed_sec, delta_sec in simulation: {},{}".format(ts.elapsed_seconds, ts.delta_seconds)) 
                i += 1                 
                if i%1 == 0:                  
                    # CASE: Stored data   
                    # location = vehicle.get_location()
                    # location.x += float(state[i+10][0])-float(state[i][0])
                    # location.y += float(state[i+10][1])-float(state[i][1])

                    # # CASE : Real-time ROS communication
                    # trans = vehicle.get_transform()
                    # # location = vehicle.get_location()
                    # trans.location.x = state.current_state['x'] + offset[0]
                    # trans.location.y = state.current_state['y'] + offset[1]
                    # trans.location.y = -trans.location.y 
                    # trans.rotation.yaw = state.current_state['psi']*180/3.1415
                    # trans.rotation.yaw *= -1


                    # CASE : Display with only GPS directly
                    trans = vehicle.get_transform()
                    # location = vehicle.get_location()
                    # In CARLA Coordinate
                    trans.location.x = state.current_state['x']-offset_x 
                    trans.location.y = state.current_state['y']-offset_y
                    trans.location.y = -trans.location.y 
                    trans.rotation.yaw = state.current_state['psi']*180/3.1415
                    trans.rotation.yaw *= -1
                    speed=state.current_state['v_lon']
                    # import pdb; pdb.set_trace()
                    if map_id == 1:
                        trans.rotation.yaw -= 0
                    ego_vel=carla.Vector3D(x=speed*np.cos(np.radians(trans.rotation.yaw)) ,
                                               y=speed*np.sin(np.radians(trans.rotation.yaw)) ,
                                               z=0.01)

                    # trans.location.z = trans.location.z
                    # trans.location.z = (1*state.current_state['alt'] + 2*trans.location.z)/3 + 0.2

                    # trans.location.x += -0.4*sin(trans.rotation.yaw/180*3.1415) 
                    # trans.location.y += 0.4*cos(trans.rotation.yaw/180*3.1415)  

                    # 1) Compensate dGPS ostx's location
                    # dgps_comp_offset_x = -0.4*sin(trans.rotation.yaw/180*3.1415) +1.7*cos(trans.rotation.yaw/180*3.1415)
                    # dgps_comp_offset_y = 0.4*cos(trans.rotation.yaw/180*3.1415) +1.7*sin(trans.rotation.yaw/180*3.1415) 
                    # trans.location.x += -0.4*sin(trans.rotation.yaw/180*3.1415) +1.7*cos(trans.rotation.yaw/180*3.1415)
                    # trans.location.y += 0.4*cos(trans.rotation.yaw/180*3.1415) +1.7*sin(trans.rotation.yaw/180*3.1415) 


                    """Gomentum: offset compensation 
                        1) z offset
                        2) x,y offset
                    """
                    z_offset_on = 1        # 1: map, 2: cur gps, 3: no offset (keep tran.z)
                    xy_offset_on = 2   # 1: on, 2: off   
                    if map_id == 2:
                        # 1) Gomentum z coordinate offset compensation
                        if z_offset_on == 1:
                            # From recorded map
                            z_cur, z_list = xy2z(gomentum_mat, trans.location.x+offset_x, -trans.location.y+offset_y)
                            trans.location.z = z_cur+1.25
                            s_cur = xy2s(gomentum_mat, trans.location.x+offset_x, -trans.location.y+offset_y)
                            # print("s_cur : {}".format(s_cur))
                        elif z_offset_on == 2:
                            # From current state['alt']
                            trans.location.z = state.current_state['alt']+1.0

                        # 2)-1 Gomentum X, Y Coordinate offset compensation (small loop)
                        # if s_cur >=300 and s_cur <= 500:                        
                        #     trans.location.z += (s_cur-300)/180+0.05
                        # elif s_cur >500 and s_cur <= 555: 
                        #     trans.location.z += 10/9+0.05-(s_cur-500)/50
                        # # trans.location.z -= 0.6*(trans.location.z-state.current_state['alt'])
                        # print("z_estiamted from recorded map: {}".format(z_cur))
                        # print("z_altitude from dgps: {}".format(state.current_state['alt']))
                        # print('yaw: {}'.format(trans.rotation.yaw))
                        # print('s_cur"{}'.format(s_cur))
                        # # 2) Gps offest compensation (new map offset)
                        # if s_cur >= 500 and s_cur<=630:
                        #     trans.location.x += 1*sin(trans.rotation.yaw/180*3.1415)
                        #     trans.location.y += -1*cos(trans.rotation.yaw/180*3.1415) 
                        #     # npc_map_offset_x = -1*sin(trans.rotation.yaw/180*3.1415)
                        #     # npc_map_offset_y = 1*cos(trans.rotation.yaw/180*3.1415)
                        # elif s_cur >630 and s_cur <= 850:
                        #     trans.location.x += (2.3/260)*(s_cur-500)*sin(trans.rotation.yaw/180*3.1415)
                        #     trans.location.y += -(2.3/260)*(s_cur-500)*cos(trans.rotation.yaw/180*3.1415)
                        #     # npc_map_offset_x = -(2.3/260)*(s_cur-500)*sin(trans.rotation.yaw/180*3.1415)
                        #     # npc_map_offset_y = (2.3/260)*(s_cur-500)*cos(trans.rotation.yaw/180*3.1415)


                        # 2)-2 Gomentum X, Y Coordinate offset compensation (large loop)  
                        if xy_offset_on == 1:                 
                            if s_cur >= 0 and s_cur < 140:
                                npc_map_offset_x = -1.1*sin(trans.rotation.yaw/180*3.1415)
                                npc_map_offset_y = 1.1*cos(trans.rotation.yaw/180*3.1415)
                                trans.location.x += npc_map_offset_x
                                trans.location.y += npc_map_offset_y
                            elif s_cur >= 140 and s_cur < 250:
                                npc_map_offset_x = -1.2*sin(trans.rotation.yaw/180*3.1415)
                                npc_map_offset_y = 1.2*cos(trans.rotation.yaw/180*3.1415)
                                trans.location.x += npc_map_offset_x
                                trans.location.y += npc_map_offset_y
                            elif s_cur >= 250 and s_cur < 370:
                                npc_map_offset_x = -1.2*sin(trans.rotation.yaw/180*3.1415)
                                npc_map_offset_y = 1.2*cos(trans.rotation.yaw/180*3.1415)
                                trans.location.x += npc_map_offset_x
                                trans.location.y += npc_map_offset_y
                            elif s_cur >= 370 and s_cur < 500:
                                npc_map_offset_x = -1.5*sin(trans.rotation.yaw/180*3.1415)
                                npc_map_offset_y = 1.5*cos(trans.rotation.yaw/180*3.1415)
                                trans.location.x += npc_map_offset_x
                                trans.location.y += npc_map_offset_y
                            elif s_cur >= 500 and s_cur < 800:
                                npc_map_offset_x = -1.3*sin(trans.rotation.yaw/180*3.1415)
                                npc_map_offset_y = 1.3*cos(trans.rotation.yaw/180*3.1415)
                                trans.location.x += npc_map_offset_x
                                trans.location.y += npc_map_offset_y
                            elif s_cur >= 800:
                                npc_map_offset_x = -1.1*sin(trans.rotation.yaw/180*3.1415)
                                npc_map_offset_y = 1.1*cos(trans.rotation.yaw/180*3.1415)
                                trans.location.x += npc_map_offset_x
                                trans.location.y += npc_map_offset_y
                            dgps_comp_offset_x = -0.4*sin(trans.rotation.yaw/180*3.1415) +1.7*cos(trans.rotation.yaw/180*3.1415)
                            dgps_comp_offset_y = 0.4*cos(trans.rotation.yaw/180*3.1415) +1.7*sin(trans.rotation.yaw/180*3.1415) 
                        else:
                            s_cur = xy2s(gomentum_mat, state.current_state['x'], state.current_state['y'])
                            if s_cur >= 430 and s_cur <470:
                                # push the vehicle in the right direction
                                npc_map_offset_x = -1*sin(trans.rotation.yaw/180*3.1415)
                                npc_map_offset_y = 1*cos(trans.rotation.yaw/180*3.1415)
                                # trans.location.x += npc_map_offset_x
                                # trans.location.y += npc_map_offset_y
                            else:
                                dgps_comp_offset_x = 0
                                dgps_comp_offset_y = 0
                        # Without physics at GOMENTUM
                        # vehicle.set_enable_gravity(enabled=False)
                        vehicle.set_simulate_physics(enabled=False)

                    # RFS Offset Compensation
                    elif map_id == 1:
                        if xy_offset_on == 1:
                            dgps_comp_offset_x = -0.4*sin(trans.rotation.yaw/180*3.1415) +1.7*cos(trans.rotation.yaw/180*3.1415)
                            dgps_comp_offset_y = 0.4*cos(trans.rotation.yaw/180*3.1415) +1.7*sin(trans.rotation.yaw/180*3.1415) 
                            # npc_map_offset_x = 1.2*sin(trans.rotation.yaw/180*3.1415) 
                            # npc_map_offset_y =  -1.2*cos(trans.rotation.yaw/180*3.1415) 
                            trans.location.x += npc_map_offset_x
                            trans.location.y += npc_map_offset_y
                        else:
                            dgps_comp_offset_x = 0
                            dgps_comp_offset_y = 0
                            
                    trans.rotation.pitch = 0
                    trans.rotation.roll = 0

                    # Teleport the vehicle in CARLA,
                    # import pdb; pdb.set_trace()
                    vehicle.set_transform(trans)
                    vehicle.set_velocity(ego_vel)
                    # import pdb; pdb.set_trace()

                    # vehicle.set_location(location)  
                    # npc_state_list's elements are based on the nuvo cooridnate
                    if len(npc_state_list) >=1:                  
                        gap1 = np.sqrt((npc_state_list[0].loc.x-offset_x-trans.location.x)**2+(-npc_state_list[0].loc.y+offset_y-trans.location.y)**2)
                        gap1_ = np.sqrt((npc_state_list[0].loc.x-state.current_state['x'])**2+(npc_state_list[0].loc.y-state.current_state['y'])**2)
                        print("npc1 state :{}, {}".format(npc_state_list[0].loc.x-offset_x,-npc_state_list[0].loc.y+offset_y))
                        print("npc1 state in nuvo:{}, {}".format(npc_state_list[0].loc.x,npc_state_list[0].loc.y))
                        # print("current ego vehicle in carla : {},{},{}".format(trans.location.x, trans.location.y, trans.rotation.yaw))
                        print("gap : {}, {}".format(gap1, gap1_))
                        print("length of npcs: {}".format(len(npc_state_list)))
                    print("current ego vehicle in carla : {},{},{}".format(trans.location.x, trans.location.y, trans.rotation.yaw))
                    print('move an ego vehicle to %s in carla' % vehicle.get_location())
                    carla_cur_ego_loc = vehicle.get_location()
                    print('move an ego to x={}, y={}, yaw={} in nuvo & autobox by carla'.format(carla_cur_ego_loc.x+offset_x-npc_map_offset_x+dgps_comp_offset_x, -carla_cur_ego_loc.y+offset_y+npc_map_offset_y-dgps_comp_offset_y,trans.rotation.yaw))
                    print('move an ego to x={}, y={}, yaw={} in nuvo & autobox'.format(state.current_state['x'], state.current_state['y'], state.current_state['psi']*180/3.1415))
                    # print('move an ego to x={}, y={} in nuvo & autobox'.format(trans.location.x+offset_x, -trans.location.y+offset_y))
                    geoloc = cur_map.transform_to_geolocation(vehicle.get_location())
                    # print('lat, long, alt : {}, {}, {}'.format(geoloc.latitude, geoloc.longitude, geoloc.altitude))
                    # print("\n")
                end = time.time()
                print("elapsed_time_ros:{}".format(end-start))
                print("frequency_ros:{}".format(1/(end-start)))
            if j_record % 10 == 0:
                j_record = 0
                elapsed_time_py.append(end-start)
                elapsed_time_carla.append(ts.delta_seconds)

    finally:
        print('destroying actors')
        # camera.destroy()
        len_npcs = len(npc_list)
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        client.apply_batch([carla.command.DestroyActor(x) for x in npc_list])
        print('done.')
        # filename = 'computation_time_{}.csv'.format(len_npcs)

        # # write to csv file
        # with open(filename, 'w') as csvfile:
        #     csvwriter = csv.writer(csvfile)
        #     csvwriter.writerow(elapsed_time_py)
        #     csvwriter.writerow(elapsed_time_carla)



if __name__ == '__main__':
    ## CASE : Stored data
    # state = []
    # with open('state.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         state.append(row)
    #     print(state)

    # CASE : ros coomunication
    main()
