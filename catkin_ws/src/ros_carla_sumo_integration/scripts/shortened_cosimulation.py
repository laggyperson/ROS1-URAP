#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# Credits also to Hotae Lee <hotae.lee@berkeley.edu>

""" 
    Allows us to run Carla and Sumo co-simulation in ROS enviornment.
    Subscribes information about the ego vehicle
    Publishes information about all the NPCs

    Default parameters are going to be default of original 'run_synchronization' script.
    Running the G16_trafficsim.confg simulation by default
    Can change by writing _<param name>=<value> on command line.

    WORK IN PROGRESS - Haven't connected to corresponding Arpa-E Vehicle node
    Have connected to a dummy node: seems to be working!

    Date: November, 2022
    Author: Phillip Chen 
"""

# ==================================================================================================
# -- ROS imports -----------------------------------------------------------------------------------
# ==================================================================================================
import rospy
from ros_carla_sumo_integration.msg import StateEst
from ros_carla_sumo_integration.msg import NpcState
from ros_carla_sumo_integration.msg import NpcStateArray

# ==================================================================================================
# -- General Python imports ------------------------------------------------------------------------
# ==================================================================================================
import argparse
import logging
import time
import glob
import os
import sys
import math
import random
from scipy import io
import numpy as np

# ==================================================================================================
# -- Carla import ----------------------------------------------------------------------------------
# ==================================================================================================
try:
    sys.path.append(glob.glob('/home/arpae/Documents/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name =='nt' else 'linux-x86_64'))[0])
except IndexError:
    print("Couldn't find Carla")
    pass

import carla

# ==================================================================================================
# -- TraCI import ----------------------------------------------------------------------------------
# ==================================================================================================
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import sumolib

# ==================================================================================================
# -- sumo integration imports ----------------------------------------------------------------------
# ==================================================================================================

from sumo_integration.bridge_helper import BridgeHelper  # pylint: disable=wrong-import-position
from sumo_integration.carla_simulation import CarlaSimulation  # pylint: disable=wrong-import-position
from sumo_integration.constants import INVALID_ACTOR_ID  # pylint: disable=wrong-import-position
from sumo_integration.sumo_simulation import SumoSimulation  # pylint: disable=wrong-import-position

# Helper Function
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
    delta_lat = math.radians(lat1 - lat0)
    delta_lon = math.radians(lon1 - lon0)

    lat_avg = 0.5 * ( math.radians(lat1) + math.radians(lat0) )
    X = R_earth * delta_lon * math.cos(lat_avg)
    Y = R_earth * delta_lat

    return X,Y

# Uses the mat file for Gomentum to get the z changes
def xy2z(mat, x_cur, y_cur):
    z = mat['road_z']
    x = mat['road_x']
    y = mat['road_y']

    norm_array = (x - x_cur)**2 + (y - y_cur)**2
    idx_min = np.argmin(norm_array)

    z_cur = z.item(idx_min)
    return z_cur

# The mat file for the Gomentum planner route
gomentum_mat = io.loadmat('/home/arpae/Documents/pure_sim_URAP/pure_sim_ws/src/mpclab_controllers_arpae/nodes/Gomentum_rt3003_ver1.mat')

# ==================================================================================================
# --------------------------------------------------------------------------------------------------
# -- run_synchronization.py ------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# ==================================================================================================

# ==================================================================================================
# -- synchronization_loop --------------------------------------------------------------------------
# ==================================================================================================


class SimulationSynchronization(object):
    """
    SimulationSynchronization class is responsible for the synchronization of sumo and carla
    simulations.
    """
    def __init__(self,
                 sumo_simulation,
                 carla_simulation,
                 tls_manager='none',
                 sync_vehicle_color=False,
                 sync_vehicle_lights=False,
                 freq_reduction=10.0):

        self.sumo = sumo_simulation
        self.carla = carla_simulation

        self.tls_manager = tls_manager
        self.sync_vehicle_color = sync_vehicle_color
        self.sync_vehicle_lights = sync_vehicle_lights

        if tls_manager == 'carla':
            self.sumo.switch_off_traffic_lights()
        elif tls_manager == 'sumo':
            self.carla.switch_off_traffic_lights()

        # Mapped actor ids.
        self.sumo2carla_ids = {}  # Contains only actors controlled by sumo.
        self.carla2sumo_ids = {}  # Contains only actors controlled by carla.

        BridgeHelper.blueprint_library = self.carla.world.get_blueprint_library()
        BridgeHelper.offset = self.sumo.get_net_offset()

        # Configuring carla simulation in sync mode.
        settings = self.carla.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = self.carla.step_length
        self.carla.world.apply_settings(settings)

        # ================================================ ROS ================================================
        # ROS Node Object
        # ================================================ ROS ================================================
        self.ego_vehicle = rosNode(self.carla, self.sumo, self.carla.world.get_map())
        self.sumo_ego = [] # List of ID's for ego sumo actor
        self.carla_ego = [] # same as above

        self.tick_count = 0 # To keep track of when to update Carla with Sumo data
        self.freq_reduction = freq_reduction

    def tick(self):
        """
        Tick to simulation synchronization
        Going to change the frequency of ticks for performance
        """
        # -----------------
        # sumo-->carla sync
        # -----------------
        self.sumo.tick()

        # Spawning new sumo actors in carla (i.e, not controlled by carla).
        sumo_spawned_actors = self.sumo.spawned_actors - set(self.carla2sumo_ids.values()) - set(self.sumo_ego)
        for sumo_actor_id in sumo_spawned_actors:
            self.sumo.subscribe(sumo_actor_id)
            sumo_actor = self.sumo.get_actor(sumo_actor_id)

            carla_blueprint = BridgeHelper.get_carla_blueprint(sumo_actor, self.sync_vehicle_color)
            if carla_blueprint is not None:
                carla_transform = BridgeHelper.get_carla_transform(sumo_actor.transform,
                                                                   sumo_actor.extent)

                carla_actor_id = self.carla.spawn_actor(carla_blueprint, carla_transform)
                if carla_actor_id != INVALID_ACTOR_ID:
                    self.sumo2carla_ids[sumo_actor_id] = carla_actor_id
            else:
                self.sumo.unsubscribe(sumo_actor_id)

        # Destroying sumo arrived actors in carla.
        for sumo_actor_id in self.sumo.destroyed_actors:
            if sumo_actor_id in self.sumo2carla_ids:
                self.carla.destroy_actor(self.sumo2carla_ids.pop(sumo_actor_id))
        
        if self.tick_count == 0:
            # Updating sumo actors in carla.
            for sumo_actor_id in self.sumo2carla_ids:
                carla_actor_id = self.sumo2carla_ids[sumo_actor_id]

                sumo_actor = self.sumo.get_actor(sumo_actor_id)
                carla_actor = self.carla.get_actor(carla_actor_id)

                carla_transform = BridgeHelper.get_carla_transform(sumo_actor.transform,
                                                                   sumo_actor.extent)
                if self.sync_vehicle_lights:
                    carla_lights = BridgeHelper.get_carla_lights_state(carla_actor.get_light_state(),
                                                                       sumo_actor.signals)
                else:
                    carla_lights = None

                self.carla.synchronize_vehicle(carla_actor_id, carla_transform, carla_lights)

                # ================================================ ROS ================================================
                # Adds Sumo actor state to ego vehicle's curr_sim array
                # ================================================ ROS ================================================
                if self.ego_vehicle.ego_check > 1:
                    self.ego_vehicle.add_state(carla_actor, 1)
                # ============================================== End ROS ==============================================

        self.tick_count = (self.tick_count + 1) % self.freq_reduction # Every fre_reduction ticks we will sync the Sumo cars with the Carla world

        # Updates traffic lights in carla based on sumo information. Will do every tick
        if self.tls_manager == 'sumo':
            common_landmarks = self.sumo.traffic_light_ids & self.carla.traffic_light_ids
            for landmark_id in common_landmarks:
                sumo_tl_state = self.sumo.get_traffic_light_state(landmark_id)
                carla_tl_state = BridgeHelper.get_carla_traffic_light_state(sumo_tl_state)

                self.carla.synchronize_traffic_light(landmark_id, carla_tl_state)

        # -----------------
        # carla-->sumo sync
        # -----------------
        self.carla.tick()

        # Spawning new carla actors (not controlled by sumo)
        carla_spawned_actors = self.carla.spawned_actors - set(self.sumo2carla_ids.values()) - set(self.carla_ego)
        for carla_actor_id in carla_spawned_actors:
            carla_actor = self.carla.get_actor(carla_actor_id)

            type_id = BridgeHelper.get_sumo_vtype(carla_actor)
            color = carla_actor.attributes.get('color', None) if self.sync_vehicle_color else None
            if type_id is not None:
                sumo_actor_id = self.sumo.spawn_actor(type_id, color)
                if sumo_actor_id != INVALID_ACTOR_ID:
                    self.carla2sumo_ids[carla_actor_id] = sumo_actor_id
                    self.sumo.subscribe(sumo_actor_id)

        # Destroying required carla actors in sumo.
        for carla_actor_id in self.carla.destroyed_actors:
            if carla_actor_id in self.carla2sumo_ids:
                self.sumo.destroy_actor(self.carla2sumo_ids.pop(carla_actor_id))

        # Updating carla actors in sumo.
        for carla_actor_id in self.carla2sumo_ids:
            sumo_actor_id = self.carla2sumo_ids[carla_actor_id]

            carla_actor = self.carla.get_actor(carla_actor_id)
            sumo_actor = self.sumo.get_actor(sumo_actor_id)

            sumo_transform = BridgeHelper.get_sumo_transform(carla_actor.get_transform(),
                                                             carla_actor.bounding_box.extent)
            if self.sync_vehicle_lights:
                carla_lights = self.carla.get_actor_light_state(carla_actor_id)
                if carla_lights is not None:
                    sumo_lights = BridgeHelper.get_sumo_lights_state(sumo_actor.signals,
                                                                     carla_lights)
                else:
                    sumo_lights = None
            else:
                sumo_lights = None
            
            self.sumo.synchronize_vehicle(sumo_actor_id, sumo_transform, sumo_lights)

            # ================================================ ROS ================================================
            # Adds Carla actor state to ego vehicle's curr_sim array
            # ================================================ ROS ================================================
            if self.ego_vehicle.ego_check > 1:
                self.ego_vehicle.add_state(carla_actor, 0)
            # ============================================== End ROS ==============================================

        # Updates traffic lights in sumo based on carla information.
        if self.tls_manager == 'carla':
            common_landmarks = self.sumo.traffic_light_ids & self.carla.traffic_light_ids
            for landmark_id in common_landmarks:
                carla_tl_state = self.carla.get_traffic_light_state(landmark_id)
                sumo_tl_state = BridgeHelper.get_sumo_traffic_light_state(carla_tl_state)

                # Updates all the sumo links related to this landmark.
                self.sumo.synchronize_traffic_light(landmark_id, sumo_tl_state)

        # ================================================ ROS ================================================
        # Check if Ego vehicle has spawned, and does so if not
        # Updating Ego Vehicle Position in Carla and Sumo
        # Publishes at the very end
        # ================================================ ROS ================================================
        
        # Checking spawn
        if self.ego_vehicle.ego_check == 1:
            self.ego_vehicle.spawn()
            self.sumo_ego.append(self.ego_vehicle.sumo_actor)
            self.carla_ego.append(self.ego_vehicle.carla_actor.id)

        # Updating Vehicle
        if self.ego_vehicle.ego_check == 2:
            ego_transform = self.ego_vehicle.update_carla_state()
            carla_lights = None # Not syncing lights for now

            self.carla.synchronize_vehicle(self.ego_vehicle.carla_actor.id, ego_transform, carla_lights)

            sumo_transform = BridgeHelper.get_sumo_transform(ego_transform, self.ego_vehicle.carla_actor.bounding_box.extent)
            sumo_lights = None # Not syncing lights for now

            self.sumo.synchronize_vehicle(self.ego_vehicle.sumo_actor, sumo_transform, sumo_lights)

        # # Temporary npc for Ego Vehicle
        # if self.ego_vehicle.ego_check == 3:
        #     ego_transform = self.ego_vehicle.carla_actor.get_transform()

        #     sumo_transform = BridgeHelper.get_sumo_transform(ego_transform, self.ego_vehicle.carla_actor.bounding_box.extent)
        #     sumo_lights = None # Not syncing lights for now

        #     self.sumo.synchronize_vehicle(self.ego_vehicle.sumo_actor, sumo_transform, sumo_lights)

        # Publishing, also with specified tick frequency
        if self.tick_count == 0:
            self.ego_vehicle.publish()
        
        # ============================================== End ROS ==============================================

    def close(self):
        """
        Cleans synchronization.
        """
        # Configuring carla simulation in async mode.
        settings = self.carla.world.get_settings()
        settings.synchronous_mode = False
        settings.fixed_delta_seconds = None
        self.carla.world.apply_settings(settings)

        # ================================================ ROS ================================================
        # Destroying ego vehicle
        # ================================================ ROS ================================================
        if self.ego_vehicle.carla_actor is not None:
            self.carla.destroy_actor(self.ego_vehicle.carla_actor.id)
            print("Destroyed Ego Actors in Carla")
        # ============================================== End ROS ==============================================

        # Destroying synchronized actors.
        for carla_actor_id in self.sumo2carla_ids.values():
            self.carla.destroy_actor(carla_actor_id)

        for sumo_actor_id in self.carla2sumo_ids.values():
            self.sumo.destroy_actor(sumo_actor_id)
        
        if self.ego_vehicle.sumo_actor is not None:
            self.sumo.destroy_actor(self.ego_vehicle.sumo_actor)
            print("Destroyed Ego Actors in Sumo")

        # Closing sumo and carla client.
        self.carla.close()
        self.sumo.close()


def synchronization_loop(args):
    """
    Entry point for sumo-carla co-simulation.
    """
    sumo_simulation = SumoSimulation(args.sumo_cfg_file, args.step_length, args.sumo_host,
                                     args.sumo_port, args.sumo_gui, args.client_order)
    carla_simulation = CarlaSimulation(args.carla_host, args.carla_port, args.step_length)

    synchronization = SimulationSynchronization(sumo_simulation, carla_simulation, args.tls_manager,
                                                args.sync_vehicle_color, args.sync_vehicle_lights, args.freq_reduction)
    try:
        while True:
            start = time.time()

            synchronization.tick()

            end = time.time()
            elapsed = end - start
            if elapsed < args.step_length:
                time.sleep(args.step_length - elapsed)

    except KeyboardInterrupt:
        logging.info('Cancelled by user.')

    finally:
        logging.info('Cleaning synchronization')

        synchronization.close()

# ==================================================================================================
# -- ROS Node Class --------------------------------------------------------------------------------
# ==================================================================================================

class rosNode:
    def __init__(self, carla_sim, sumo_sim, carla_map):
        rospy.init_node("cosimulation_client", anonymous=True)
        pub_topic_name = "/NpcStateArray"
        sub_topic_name = "/est_state_ros1"

        self.pub = rospy.Publisher(pub_topic_name, NpcStateArray, queue_size=5)
        self.sub = rospy.Subscriber(sub_topic_name, StateEst, self.callback)
        
        self.current_ego_state = {'t':0, 'x':0, 'y':0, 'psi':0,'lat':0, 'lon':0}
        self.state_traj = []
        self.ego_color = (255, 0, 0)
        self.ego_check = 0      # 0 means not yet spawned, 1 means ready to spawn, 2 means spawned, 3 means Carla Autopilot

        self.carla_actor = None
        self.sumo_actor = None

        self.carla_sim = carla_sim
        self.sumo_sim = sumo_sim

        self.carla_map = carla_map
        self.carla_offset = [0, 0]

        # Array to be published
        self.curr_sim = NpcStateArray()

    """
    Spawns the ego vehicle at the subscribed location.
    """
    def spawn(self):
        # Spawning in Carla
        ego_carla_blueprint = random.choice(self.carla_sim.blueprint_library.filter('vehicle'))
        if ego_carla_blueprint.has_attribute('color'):
            color ='255, 0, 0'
            ego_carla_blueprint.set_attribute('color', color)

        # Obtain the Carla.transform for random spawn_points
        transform = random.choice(self.carla_map.get_spawn_points())

        # Tell the Carla world to spawn the vehicle
        self.carla_actor = self.carla_sim.world.spawn_actor(ego_carla_blueprint, transform)
        self.carla_sim.tick()
        transform = self.carla_actor.get_transform()
    
        # Fix the x,y,z spawn point
        transform.location.x = self.current_ego_state['x']
        transform.location.y = self.current_ego_state['y']
        transform.location.z = 17
        transform.rotation.yaw = self.current_ego_state['psi']
        self.carla_sim.synchronize_vehicle(self.carla_actor.id, transform, None)
        self.carla_sim.tick()

        transform = self.carla_actor.get_transform()
        print("Spawned Ego Vehicle at: {},{},{}".format(transform.location.x, transform.location.y, transform.location.z))

        # Getting offset by getting the origin
        location = self.carla_actor.get_location()
        location.x, location.y, location.z = 0, 0, 0
        origin_gps = self.carla_map.transform_to_geolocation(location)
        lat_o, lon_o = origin_gps.latitude, origin_gps.longitude
        LAT0, LON0 = 38.0143934, -122.0135798
        offset_x, offset_y = latlon_to_XY(LAT0, LON0, lat_o, lon_o)
        self.carla_offset = [offset_x, offset_y]

        # Spawning in Sumo based on Carla object. POTENTIAL ISSUE: Cannot create sumo object because blueprints can't translate
        sumo_type_id = BridgeHelper.get_sumo_vtype(self.carla_actor)
        color = self.carla_actor.attributes.get('color', None)
        if sumo_type_id is not None:
            self.sumo_actor = self.sumo_sim.spawn_actor(sumo_type_id, color)
            if self.sumo_actor != INVALID_ACTOR_ID:
                self.sumo_sim.subscribe(self.sumo_actor)

        self.ego_check = 2

    """
    Subscribes to the current state of the vehicle
    """
    def callback(self, msg):
        rospy.loginfo(rospy.get_caller_id() + "x and time are %s %s", msg.x, msg.header.stamp.secs + 1e-9 * msg.header.stamp.nsecs)   
        self.current_ego_state['t'] = msg.header.stamp.secs + 1e-9 * msg.header.stamp.nsecs
        self.current_ego_state['x'] = msg.x
        self.current_ego_state['y'] = msg.y
        self.current_ego_state['psi'] = msg.psi
        self.current_ego_state['lat'] = msg.lat
        self.current_ego_state['lon'] = msg.lon
        self.state_traj.append(self.current_ego_state)
        
        if not self.ego_check:
            self.ego_check = 1

    """
    Publishes the attribute curr_sim and resets it to get ready for next timestep
    """
    def publish(self):
        self.pub.publish(self.curr_sim)

    """
    Adds the actor and its state to curr_sim as a state_est type
    Params:
        actor - the actor object to get attributes from Carla sim; will always be a Carla actor object
        sim - integer describing what simulation actor is from, 0=Carla, 1=Sumo, anything else errors
    Result (no return):
        Appends state to curr_sim of type NpcState()
    """
    def add_state(self, actor, sim):
        if not (sim == 0 or sim == 1):
            raise Exception("Cannot add state for actor that isn't in Sumo or Carla. Please specify with parameter sim=0 or 1 for Carla or Sumo respectively")
            exit()

        state = NpcState()
        transform = actor.get_transform()

        state.loc = transform.location
        rotation = transform.rotation 
        state.rot = carla.Vector3D(rotation.roll, rotation.yaw, rotation.pitch)
        state.vel = actor.get_velocity()
        state.ang_vel = actor.get_angular_velocity()

        self.curr_sim.npc_states.append(state)

    """
    Updates the current carla actor transform with the current_ego_state
    Returns the new transform
    """
    def update_carla_state(self):
        transform = self.carla_actor.get_transform()

        # Updating with current_state
        transform.location.x = self.current_ego_state['x'] - self.carla_offset[0]
        transform.location.y = self.current_ego_state['y'] - self.carla_offset[1]
        transform.location.y = -transform.location.y 
        transform.rotation.yaw = self.current_ego_state['psi']*180/3.1415 - 90
        # transform.rotation.yaw *= -1

        # Z offset
        transform.location.z = xy2z(gomentum_mat, self.current_ego_state['x'], self.current_ego_state['y']) + 0.9

        print("Moving the ego vehicle to %s in Carla" % self.carla_actor.get_location())

        return transform

# ==================================================================================================
# -- main --------------------------------------------------------------------------------
# ==================================================================================================

def main():

    # Creating argparser:
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('sumo_cfg_file', type=str, help='sumo configuration file')
    argparser.add_argument('--carla-host',
                           metavar='H',
                           default='127.0.0.1',
                           help='IP of the carla host server (default: 127.0.0.1)')
    argparser.add_argument('--carla-port',
                           metavar='P',
                           default=2000,
                           type=int,
                           help='TCP port to listen to (default: 2000)')
    argparser.add_argument('--freq-reduction',
                           metavar='F',
                           default=10.0,
                           type=float,
                           help='The frequency of updating Sumo NPCs in Carla')
    argparser.add_argument('--sumo-host',
                           metavar='H',
                           default=None,
                           help='IP of the sumo host server (default: 127.0.0.1)')
    argparser.add_argument('--sumo-port',
                           metavar='P',
                           default=None,
                           type=int,
                           help='TCP port to liston to (default: 8813)')
    argparser.add_argument('--sumo-gui', action='store_true', help='run the gui version of sumo')
    argparser.add_argument('--step-length',
                           default=0.05,
                           type=float,
                           help='set fixed delta seconds (default: 0.05s)')
    argparser.add_argument('--client-order',
                           metavar='TRACI_CLIENT_ORDER',
                           default=1,
                           type=int,
                           help='client order number for the co-simulation TraCI connection (default: 1)')
    argparser.add_argument('--sync-vehicle-lights',
                           action='store_true',
                           help='synchronize vehicle lights state (default: False)')
    argparser.add_argument('--sync-vehicle-color',
                           action='store_true',
                           help='synchronize vehicle color (default: False)')
    argparser.add_argument('--sync-vehicle-all',
                           action='store_true',
                           help='synchronize all vehicle properties (default: False)')
    argparser.add_argument('--tls-manager',
                           type=str,
                           choices=['none', 'sumo', 'carla'],
                           help="select traffic light manager (default: none)",
                           default='none')
    argparser.add_argument('--debug', action='store_true', help='enable debug messages')

    arguments = argparser.parse_args()

    if arguments.sync_vehicle_all:
        arguments.sync_vehicle_lights = True
        arguments.sync_vehicle_color = True
    if arguments.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    synchronization_loop(arguments)

if __name__ == "__main__":
    main()
