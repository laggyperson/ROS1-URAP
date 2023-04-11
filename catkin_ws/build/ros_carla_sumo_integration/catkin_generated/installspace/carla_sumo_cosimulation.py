#!/usr/bin/env python2

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
from ros_carla_sumo_integration.msg import state_est
from ros_carla_sumo_integration.msg import sim_state

# ==================================================================================================
# -- General Python imports ------------------------------------------------------------------------
# ==================================================================================================
import argparse
import logging
import time
import glob
import os
import sys
import json
import math
import random
import collections
import enum
import lxml.etree as ET

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
# -- constants.py ----------------------------------------------------------------------------------
# ==================================================================================================
INVALID_ACTOR_ID = -1
SPAWN_OFFSET_Z = 25.0  # meters

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
                 sync_vehicle_lights=False):

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

    def tick(self):
        """
        Tick to simulation synchronization
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

        # Updates traffic lights in carla based on sumo information.
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

        """# Temporary npc for Ego Vehicle
        if self.ego_vehicle.ego_check == 3:
            ego_transform = self.ego_vehicle.carla_actor.get_transform()

            sumo_transform = BridgeHelper.get_sumo_transform(ego_transform, self.ego_vehicle.carla_actor.bounding_box.extent)
            sumo_lights = None # Not syncing lights for now

            self.sumo.synchronize_vehicle(self.ego_vehicle.sumo_actor, sumo_transform, sumo_lights)"""

        # Publishing
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
            print("Destroyed Ego Actors")
        # ============================================== End ROS ==============================================

        # Destroying synchronized actors.
        for carla_actor_id in self.sumo2carla_ids.values():
            self.carla.destroy_actor(carla_actor_id)

        for sumo_actor_id in self.carla2sumo_ids.values():
            self.sumo.destroy_actor(sumo_actor_id)
        
        if self.ego_vehicle.sumo_actor is not None:
            self.sumo.destroy_actor(self.ego_vehicle.sumo_actor)

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
                                                args.sync_vehicle_color, args.sync_vehicle_lights)
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
# --------------------------------------------------------------------------------------------------
# -- bridge_helper.py ------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# ==================================================================================================

# ==================================================================================================
# -- Bridge helper (SUMO <=> CARLA) ----------------------------------------------------------------
# ==================================================================================================


class BridgeHelper(object):
    """
    BridgeHelper provides methos to ease the co-simulation between sumo and carla.
    """

    blueprint_library = []
    offset = (0, 0)
    vtypes_path = "/home/arpae/Documents/carla/Co-Simulation/Sumo/data/vtypes.json"

    with open(vtypes_path) as f:
        _VTYPES = json.load(f)['carla_blueprints']

    @staticmethod
    def get_carla_transform(in_sumo_transform, extent):
        """
        Returns carla transform based on sumo transform.
        """
        offset = BridgeHelper.offset
        in_location = in_sumo_transform.location
        in_rotation = in_sumo_transform.rotation

        # From front-center-bumper to center (sumo reference system).
        # (http://sumo.sourceforge.net/userdoc/Purgatory/Vehicle_Values.html#angle)
        yaw = -1 * in_rotation.yaw + 90
        pitch = in_rotation.pitch
        out_location = (in_location.x - math.cos(math.radians(yaw)) * extent.x,
                        in_location.y - math.sin(math.radians(yaw)) * extent.x,
                        in_location.z - math.sin(math.radians(pitch)) * extent.x)
        out_rotation = (in_rotation.pitch, in_rotation.yaw, in_rotation.roll)

        # Applying offset sumo-carla net.
        out_location = (out_location[0] - offset[0], out_location[1] - offset[1], out_location[2])

        # Transform to carla reference system (left-handed system).
        out_transform = carla.Transform(
            carla.Location(out_location[0], -out_location[1], out_location[2]),
            carla.Rotation(out_rotation[0], out_rotation[1] - 90, out_rotation[2]))

        return out_transform

    @staticmethod
    def get_sumo_transform(in_carla_transform, extent):
        """
        Returns sumo transform based on carla transform.
        """
        offset = BridgeHelper.offset
        in_location = in_carla_transform.location
        in_rotation = in_carla_transform.rotation

        # From center to front-center-bumper (carla reference system).
        yaw = -1 * in_rotation.yaw
        pitch = in_rotation.pitch
        out_location = (in_location.x + math.cos(math.radians(yaw)) * extent.x,
                        in_location.y - math.sin(math.radians(yaw)) * extent.x,
                        in_location.z - math.sin(math.radians(pitch)) * extent.x)
        out_rotation = (in_rotation.pitch, in_rotation.yaw, in_rotation.roll)

        # Applying offset carla-sumo net
        out_location = (out_location[0] + offset[0], out_location[1] - offset[1], out_location[2])

        # Transform to sumo reference system.
        out_transform = carla.Transform(
            carla.Location(out_location[0], -out_location[1], out_location[2]),
            carla.Rotation(out_rotation[0], out_rotation[1] + 90, out_rotation[2]))

        return out_transform

    @staticmethod
    def _get_recommended_carla_blueprint(sumo_actor):
        """
        Returns an appropriate blueprint based on the given sumo actor.
        """
        vclass = sumo_actor.vclass.value

        blueprints = []
        for blueprint in BridgeHelper.blueprint_library:
            if blueprint.id in BridgeHelper._VTYPES and \
               BridgeHelper._VTYPES[blueprint.id]['vClass'] == vclass:
                blueprints.append(blueprint)

        if not blueprints:
            return None

        return random.choice(blueprints)

    @staticmethod
    def get_carla_blueprint(sumo_actor, sync_color=False):
        """
        Returns an appropriate blueprint based on the received sumo actor.
        """
        blueprint_library = BridgeHelper.blueprint_library
        type_id = sumo_actor.type_id

        if type_id in [bp.id for bp in blueprint_library]:
            blueprint = blueprint_library.filter(type_id)[0]
            logging.debug('[BridgeHelper] sumo vtype %s found in carla blueprints', type_id)
        else:
            blueprint = BridgeHelper._get_recommended_carla_blueprint(sumo_actor)
            if blueprint is not None:
                logging.warning(
                    'sumo vtype %s not found in carla. The following blueprint will be used: %s',
                    type_id, blueprint.id)
            else:
                logging.error('sumo vtype %s not supported. No vehicle will be spawned in carla',
                              type_id)
                return None

        if blueprint.has_attribute('color'):
            if sync_color:
                color = "{},{},{}".format(sumo_actor.color[0], sumo_actor.color[1],
                                          sumo_actor.color[2])
            else:
                color = random.choice(blueprint.get_attribute('color').recommended_values)
            blueprint.set_attribute('color', color)

        if blueprint.has_attribute('driver_id'):
            driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
            blueprint.set_attribute('driver_id', driver_id)

        blueprint.set_attribute('role_name', 'sumo_driver')

        logging.debug(
            '''[BridgeHelper] sumo vtype %s will be spawned in carla with the following attributes:
            \tblueprint: %s
            \tcolor: %s''', type_id, blueprint.id,
            sumo_actor.color if blueprint.has_attribute('color') else (-1, -1, -1))

        return blueprint

    @staticmethod
    def _create_sumo_vtype(carla_actor):
        """
        Creates an appropriate vtype based on the given carla_actor.
        """
        type_id = carla_actor.type_id
        attrs = carla_actor.attributes
        extent = carla_actor.bounding_box.extent

        if int(attrs['number_of_wheels']) == 2:
            traci.vehicletype.copy('DEFAULT_BIKETYPE', type_id)
        else:
            traci.vehicletype.copy('DEFAULT_VEHTYPE', type_id)

        if type_id in BridgeHelper._VTYPES:
            if 'vClass' in BridgeHelper._VTYPES[type_id]:
                _class = BridgeHelper._VTYPES[type_id]['vClass']
                traci.vehicletype.setVehicleClass(type_id, _class)

            if 'guiShape' in BridgeHelper._VTYPES[type_id]:
                shape = BridgeHelper._VTYPES[type_id]['guiShape']
                traci.vehicletype.setShapeClass(type_id, shape)

        if 'color' in attrs:
            color = attrs['color'].split(',')
            traci.vehicletype.setColor(type_id, color)

        traci.vehicletype.setLength(type_id, 2.0 * extent.x)
        traci.vehicletype.setWidth(type_id, 2.0 * extent.y)
        traci.vehicletype.setHeight(type_id, 2.0 * extent.z)

        logging.debug(
            '''[BridgeHelper] blueprint %s not found in sumo vtypes
            \tdefault vtype: %s
            \tvtype: %s
            \tclass: %s
            \tshape: %s
            \tcolor: %s
            \tlenght: %s
            \twidth: %s
            \theight: %s''', type_id,
            'DEFAULT_BIKETYPE' if int(attrs['number_of_wheels']) == 2 else 'DEFAULT_VEHTYPE',
            type_id, traci.vehicletype.getVehicleClass(type_id),
            traci.vehicletype.getShapeClass(type_id), traci.vehicletype.getColor(type_id),
            traci.vehicletype.getLength(type_id), traci.vehicletype.getWidth(type_id),
            traci.vehicletype.getHeight(type_id))

        return type_id

    @staticmethod
    def get_sumo_vtype(carla_actor):
        """
        Returns an appropriate vtype based on the type id and attributes.
        """
        type_id = carla_actor.type_id

        if not type_id.startswith('vehicle'):
            logging.error(
                '[BridgeHelper] Blueprint %s not supported. No vehicle will be spawned in sumo',
                type_id)
            return None

        if type_id in traci.vehicletype.getIDList():
            logging.debug('[BridgeHelper] blueprint %s found in sumo vtypes', type_id)
            return type_id
        return BridgeHelper._create_sumo_vtype(carla_actor)

    @staticmethod
    def get_carla_lights_state(current_carla_lights, sumo_lights):
        """
        Returns carla vehicle light state based on sumo signals.
        """
        current_lights = current_carla_lights

        # Blinker right / emergency.
        if (any([
                bool(sumo_lights & SumoVehSignal.BLINKER_RIGHT),
                bool(sumo_lights & SumoVehSignal.BLINKER_EMERGENCY)
        ]) != bool(current_lights & carla.VehicleLightState.RightBlinker)):
            current_lights ^= carla.VehicleLightState.RightBlinker

        # Blinker left / emergency.
        if (any([
                bool(sumo_lights & SumoVehSignal.BLINKER_LEFT),
                bool(sumo_lights & SumoVehSignal.BLINKER_EMERGENCY)
        ]) != bool(current_lights & carla.VehicleLightState.LeftBlinker)):
            current_lights ^= carla.VehicleLightState.LeftBlinker

        # Break.
        if (bool(sumo_lights & SumoVehSignal.BRAKELIGHT) !=
                bool(current_lights & carla.VehicleLightState.Brake)):
            current_lights ^= carla.VehicleLightState.Brake

        # Front (low beam).
        if (bool(sumo_lights & SumoVehSignal.FRONTLIGHT) !=
                bool(current_lights & carla.VehicleLightState.LowBeam)):
            current_lights ^= carla.VehicleLightState.LowBeam

        # Fog.
        if (bool(sumo_lights & SumoVehSignal.FOGLIGHT) !=
                bool(current_lights & carla.VehicleLightState.Fog)):
            current_lights ^= carla.VehicleLightState.Fog

        # High beam.
        if (bool(sumo_lights & SumoVehSignal.HIGHBEAM) !=
                bool(current_lights & carla.VehicleLightState.HighBeam)):
            current_lights ^= carla.VehicleLightState.HighBeam

        # Backdrive (reverse).
        if (bool(sumo_lights & SumoVehSignal.BACKDRIVE) !=
                bool(current_lights & carla.VehicleLightState.Reverse)):
            current_lights ^= carla.VehicleLightState.Reverse

        # Door open left/right.
        if (any([
                bool(sumo_lights & SumoVehSignal.DOOR_OPEN_LEFT),
                bool(sumo_lights & SumoVehSignal.DOOR_OPEN_RIGHT)
        ]) != bool(current_lights & carla.VehicleLightState.Position)):
            current_lights ^= carla.VehicleLightState.Position

        return current_lights

    @staticmethod
    def get_sumo_lights_state(current_sumo_lights, carla_lights):
        """
        Returns sumo signals based on carla vehicle light state.
        """
        current_lights = current_sumo_lights

        # Blinker right.
        if (bool(carla_lights & carla.VehicleLightState.RightBlinker) !=
                bool(current_lights & SumoVehSignal.BLINKER_RIGHT)):
            current_lights ^= SumoVehSignal.BLINKER_RIGHT

        # Blinker left.
        if (bool(carla_lights & carla.VehicleLightState.LeftBlinker) !=
                bool(current_lights & SumoVehSignal.BLINKER_LEFT)):
            current_lights ^= SumoVehSignal.BLINKER_LEFT

        # Emergency.
        if (all([
                bool(carla_lights & carla.VehicleLightState.RightBlinker),
                bool(carla_lights & carla.VehicleLightState.LeftBlinker)
        ]) != (current_lights & SumoVehSignal.BLINKER_EMERGENCY)):
            current_lights ^= SumoVehSignal.BLINKER_EMERGENCY

        # Break.
        if (bool(carla_lights & carla.VehicleLightState.Brake) !=
                bool(current_lights & SumoVehSignal.BRAKELIGHT)):
            current_lights ^= SumoVehSignal.BRAKELIGHT

        # Front (low beam)
        if (bool(carla_lights & carla.VehicleLightState.LowBeam) !=
                bool(current_lights & SumoVehSignal.FRONTLIGHT)):
            current_lights ^= SumoVehSignal.FRONTLIGHT

        # Fog light.
        if (bool(carla_lights & carla.VehicleLightState.Fog) !=
                bool(current_lights & SumoVehSignal.FOGLIGHT)):
            current_lights ^= SumoVehSignal.FOGLIGHT

        # High beam ligth.
        if (bool(carla_lights & carla.VehicleLightState.HighBeam) !=
                bool(current_lights & SumoVehSignal.HIGHBEAM)):
            current_lights ^= SumoVehSignal.HIGHBEAM

        # Backdrive (reverse)
        if (bool(carla_lights & carla.VehicleLightState.Reverse) !=
                bool(current_lights & SumoVehSignal.BACKDRIVE)):
            current_lights ^= SumoVehSignal.BACKDRIVE

        return current_lights

    @staticmethod
    def get_carla_traffic_light_state(sumo_tl_state):
        """
        Returns carla traffic light state based on sumo traffic light state.
        """
        if sumo_tl_state == SumoSignalState.RED or sumo_tl_state == SumoSignalState.RED_YELLOW:
            return carla.TrafficLightState.Red

        elif sumo_tl_state == SumoSignalState.YELLOW:
            return carla.TrafficLightState.Yellow

        elif sumo_tl_state == SumoSignalState.GREEN or \
             sumo_tl_state == SumoSignalState.GREEN_WITHOUT_PRIORITY:
            return carla.TrafficLightState.Green

        elif sumo_tl_state == SumoSignalState.OFF:
            return carla.TrafficLightState.Off

        else:  # SumoSignalState.GREEN_RIGHT_TURN and SumoSignalState.OFF_BLINKING
            return carla.TrafficLightState.Unknown

    @staticmethod
    def get_sumo_traffic_light_state(carla_tl_state):
        """
        Returns sumo traffic light state based on carla traffic light state.
        """
        if carla_tl_state == carla.TrafficLightState.Red:
            return SumoSignalState.RED

        elif carla_tl_state == carla.TrafficLightState.Yellow:
            return SumoSignalState.YELLOW

        elif carla_tl_state == carla.TrafficLightState.Green:
            return SumoSignalState.GREEN

        else:  # carla.TrafficLightState.Off and carla.TrafficLightState.Unknown
            return SumoSignalState.OFF


# ==================================================================================================
# --------------------------------------------------------------------------------------------------
# -- sumo_simulation.py ----------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# ==================================================================================================

# ==================================================================================================
# -- sumo definitions ------------------------------------------------------------------------------
# ==================================================================================================

# https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#signal_state_definitions
class SumoSignalState(object):
    """
    SumoSignalState contains the different traffic light states.
    """
    RED = 'r'
    YELLOW = 'y'
    GREEN = 'G'
    GREEN_WITHOUT_PRIORITY = 'g'
    GREEN_RIGHT_TURN = 's'
    RED_YELLOW = 'u'
    OFF_BLINKING = 'o'
    OFF = 'O'


# https://sumo.dlr.de/docs/TraCI/Vehicle_Signalling.html
class SumoVehSignal(object):
    """
    SumoVehSignal contains the different sumo vehicle signals.
    """
    BLINKER_RIGHT = 1 << 0
    BLINKER_LEFT = 1 << 1
    BLINKER_EMERGENCY = 1 << 2
    BRAKELIGHT = 1 << 3
    FRONTLIGHT = 1 << 4
    FOGLIGHT = 1 << 5
    HIGHBEAM = 1 << 6
    BACKDRIVE = 1 << 7
    WIPER = 1 << 8
    DOOR_OPEN_LEFT = 1 << 9
    DOOR_OPEN_RIGHT = 1 << 10
    EMERGENCY_BLUE = 1 << 11
    EMERGENCY_RED = 1 << 12
    EMERGENCY_YELLOW = 1 << 13


# https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html#abstract_vehicle_class
class SumoActorClass(enum.Enum):
    """
    SumoActorClass enumerates the different sumo actor classes.
    """
    IGNORING = "ignoring"
    PRIVATE = "private"
    EMERGENCY = "emergency"
    AUTHORITY = "authority"
    ARMY = "army"
    VIP = "vip"
    PEDESTRIAN = "pedestrian"
    PASSENGER = "passenger"
    HOV = "hov"
    TAXI = "taxi"
    BUS = "bus"
    COACH = "coach"
    DELIVERY = "delivery"
    TRUCK = "truck"
    TRAILER = "trailer"
    MOTORCYCLE = "motorcycle"
    MOPED = "moped"
    BICYCLE = "bicycle"
    EVEHICLE = "evehicle"
    TRAM = "tram"
    RAIL_URBAN = "rail_urban"
    RAIL = "rail"
    RAIL_ELECTRIC = "rail_electric"
    RAIL_FAST = "rail_fast"
    SHIP = "ship"
    CUSTOM1 = "custom1"
    CUSTOM2 = "custom2"


SumoActor = collections.namedtuple('SumoActor', 'type_id vclass transform signals extent color')

# ==================================================================================================
# -- sumo traffic lights ---------------------------------------------------------------------------
# ==================================================================================================


class SumoTLLogic(object):
    """
    SumoTLLogic holds the data relative to a traffic light in sumo.
    """
    def __init__(self, tlid, states, parameters):
        self.tlid = tlid
        self.states = states

        self._landmark2link = {}
        self._link2landmark = {}
        for link_index, landmark_id in parameters.items():
            # Link index information is added in the parameter as 'linkSignalID:x'
            link_index = int(link_index.split(':')[1])

            if landmark_id not in self._landmark2link:
                self._landmark2link[landmark_id] = []
            self._landmark2link[landmark_id].append((tlid, link_index))
            self._link2landmark[(tlid, link_index)] = landmark_id

    def get_number_signals(self):
        """
        Returns number of internal signals of the traffic light.
        """
        if len(self.states) > 0:
            return len(self.states[0])
        return 0

    def get_all_signals(self):
        """
        Returns all the signals of the traffic light.
            :returns list: [(tlid, link_index), (tlid, link_index), ...]
        """
        return [(self.tlid, i) for i in range(self.get_number_signals())]

    def get_all_landmarks(self):
        """
        Returns all the landmarks associated with this traffic light.
        """
        return self._landmark2link.keys()

    def get_associated_signals(self, landmark_id):
        """
        Returns all the signals associated with the given landmark.
            :returns list: [(tlid, link_index), (tlid, link_index), ...]
        """
        return self._landmark2link.get(landmark_id, [])


class SumoTLManager(object):
    """
    SumoTLManager is responsible for the management of the sumo traffic lights (i.e., keeps control
    of the current program, phase, ...)
    """
    def __init__(self):
        self._tls = {}  # {tlid: {program_id: SumoTLLogic}
        self._current_program = {}  # {tlid: program_id}
        self._current_phase = {}  # {tlid: index_phase}

        for tlid in traci.trafficlight.getIDList():
            self.subscribe(tlid)

            self._tls[tlid] = {}
            for tllogic in traci.trafficlight.getAllProgramLogics(tlid):
                states = [phase.state for phase in tllogic.getPhases()]
                parameters = tllogic.getParameters()
                tl = SumoTLLogic(tlid, states, parameters)
                self._tls[tlid][tllogic.programID] = tl

            # Get current status of the traffic lights.
            self._current_program[tlid] = traci.trafficlight.getProgram(tlid)
            self._current_phase[tlid] = traci.trafficlight.getPhase(tlid)

        self._off = False

    @staticmethod
    def subscribe(tlid):
        """
        Subscribe the given traffic ligth to the following variables:

            * Current program.
            * Current phase.
        """
        traci.trafficlight.subscribe(tlid, [
            traci.constants.TL_CURRENT_PROGRAM,
            traci.constants.TL_CURRENT_PHASE,
        ])

    @staticmethod
    def unsubscribe(tlid):
        """
        Unsubscribe the given traffic ligth from receiving updated information each step.
        """
        traci.trafficlight.unsubscribe(tlid)

    def get_all_signals(self):
        """
        Returns all the traffic light signals.
        """
        signals = set()
        for tlid, program_id in self._current_program.items():
            signals.update(self._tls[tlid][program_id].get_all_signals())
        return signals

    def get_all_landmarks(self):
        """
        Returns all the landmarks associated with a traffic light in the simulation.
        """
        landmarks = set()
        for tlid, program_id in self._current_program.items():
            landmarks.update(self._tls[tlid][program_id].get_all_landmarks())
        return landmarks

    def get_all_associated_signals(self, landmark_id):
        """
        Returns all the signals associated with the given landmark.
            :returns list: [(tlid, link_index), (tlid, link_index), ...]
        """
        signals = set()
        for tlid, program_id in self._current_program.items():
            signals.update(self._tls[tlid][program_id].get_associated_signals(landmark_id))
        return signals

    def get_state(self, landmark_id):
        """
        Returns the traffic light state of the signals associated with the given landmark.
        """
        states = set()
        for tlid, link_index in self.get_all_associated_signals(landmark_id):
            current_program = self._current_program[tlid]
            current_phase = self._current_phase[tlid]

            tl = self._tls[tlid][current_program]
            states.update(tl.states[current_phase][link_index])

        if len(states) == 1:
            return states.pop()
        elif len(states) > 1:
            logging.warning('Landmark %s is associated with signals with different states',
                            landmark_id)
            return SumoSignalState.RED
        else:
            return None

    def set_state(self, landmark_id, state):
        """
        Updates the state of all the signals associated with the given landmark.
        """
        for tlid, link_index in self.get_all_associated_signals(landmark_id):
            traci.trafficlight.setLinkState(tlid, link_index, state)
        return True

    def switch_off(self):
        """
        Switch off all traffic lights.
        """
        for tlid, link_index in self.get_all_signals():
            traci.trafficlight.setLinkState(tlid, link_index, SumoSignalState.OFF)
        self._off = True

    def tick(self):
        """
        Tick to traffic light manager
        """
        if self._off is False:
            for tl_id in traci.trafficlight.getIDList():
                results = traci.trafficlight.getSubscriptionResults(tl_id)
                current_program = results[traci.constants.TL_CURRENT_PROGRAM]
                current_phase = results[traci.constants.TL_CURRENT_PHASE]

                if current_program != 'online':
                    self._current_program[tl_id] = current_program
                    self._current_phase[tl_id] = current_phase


# ==================================================================================================
# -- sumo simulation -------------------------------------------------------------------------------
# ==================================================================================================

def _get_sumo_net(cfg_file):
    """
    Returns sumo net.

    This method reads the sumo configuration file and retrieve the sumo net filename to create the
    net.
    """
    cfg_file = os.path.join(os.getcwd(), cfg_file)

    tree = ET.parse(cfg_file)
    tag = tree.find('//net-file')
    if tag is None:
        return None

    net_file = os.path.join(os.path.dirname(cfg_file), tag.get('value'))
    logging.debug('Reading net file: %s', net_file)

    sumo_net = sumolib.net.readNet(net_file)
    return sumo_net

class SumoSimulation(object):
    """
    SumoSimulation is responsible for the management of the sumo simulation.
    """
    def __init__(self, cfg_file, step_length, host=None, port=None, sumo_gui=False, client_order=1):
        if sumo_gui is True:
            sumo_binary = sumolib.checkBinary('sumo-gui')
        else:
            sumo_binary = sumolib.checkBinary('sumo')

        if host is None or port is None:
            logging.info('Starting new sumo server...')
            if sumo_gui is True:
                logging.info('Remember to press the play button to start the simulation')

            traci.start([sumo_binary,
                '--configuration-file', cfg_file,
                '--step-length', str(step_length),
                '--lateral-resolution', '0.25',
                '--collision.check-junctions'
            ])

        else:
            logging.info('Connection to sumo server. Host: %s Port: %s', host, port)
            traci.init(host=host, port=port)

        traci.setOrder(client_order)

        # Retrieving net from configuration file.
        self.net = _get_sumo_net(cfg_file)

        # Creating a random route to be able to spawn carla actors.
        traci.route.add("carla_route", [traci.edge.getIDList()[0]])

        # Variable to asign an id to new added actors.
        self._sequential_id = 0

        # Structures to keep track of the spawned and destroyed vehicles at each time step.
        self.spawned_actors = set()
        self.destroyed_actors = set()

        # Traffic light manager.
        self.traffic_light_manager = SumoTLManager()

    @property
    def traffic_light_ids(self):
        return self.traffic_light_manager.get_all_landmarks()

    @staticmethod
    def subscribe(actor_id):
        """
        Subscribe the given actor to the following variables:

            * Type.
            * Vehicle class.
            * Color.
            * Length, Width, Height.
            * Position3D (i.e., x, y, z).
            * Angle, Slope.
            * Speed.
            * Lateral speed.
            * Signals.
        """
        traci.vehicle.subscribe(actor_id, [
            traci.constants.VAR_TYPE, traci.constants.VAR_VEHICLECLASS, traci.constants.VAR_COLOR,
            traci.constants.VAR_LENGTH, traci.constants.VAR_WIDTH, traci.constants.VAR_HEIGHT,
            traci.constants.VAR_POSITION3D, traci.constants.VAR_ANGLE, traci.constants.VAR_SLOPE,
            traci.constants.VAR_SPEED, traci.constants.VAR_SPEED_LAT, traci.constants.VAR_SIGNALS
        ])

    @staticmethod
    def unsubscribe(actor_id):
        """
        Unsubscribe the given actor from receiving updated information each step.
        """
        traci.vehicle.unsubscribe(actor_id)

    def get_net_offset(self):
        """
        Accessor for sumo net offset.
        """
        if self.net is None:
            return (0, 0)
        return self.net.getLocationOffset()

    @staticmethod
    def get_actor(actor_id):
        """
        Accessor for sumo actor.
        """
        results = traci.vehicle.getSubscriptionResults(actor_id)

        type_id = results[traci.constants.VAR_TYPE]
        vclass = SumoActorClass(results[traci.constants.VAR_VEHICLECLASS])
        color = results[traci.constants.VAR_COLOR]

        length = results[traci.constants.VAR_LENGTH]
        width = results[traci.constants.VAR_WIDTH]
        height = results[traci.constants.VAR_HEIGHT]

        location = list(results[traci.constants.VAR_POSITION3D])
        rotation = [results[traci.constants.VAR_SLOPE], results[traci.constants.VAR_ANGLE], 0.0]
        transform = carla.Transform(carla.Location(location[0], location[1], location[2]),
                                    carla.Rotation(rotation[0], rotation[1], rotation[2]))

        signals = results[traci.constants.VAR_SIGNALS]
        extent = carla.Vector3D(length / 2.0, width / 2.0, height / 2.0)

        return SumoActor(type_id, vclass, transform, signals, extent, color)

    def spawn_actor(self, type_id, color=None):
        """
        Spawns a new actor.

            :param type_id: vtype to be spawned.
            :param color: color attribute for this specific actor.
            :return: actor id if the actor is successfully spawned. Otherwise, INVALID_ACTOR_ID.
        """
        actor_id = 'carla' + str(self._sequential_id)
        try:
            traci.vehicle.add(actor_id, 'carla_route', typeID=type_id)
        except traci.exceptions.TraCIException as error:
            logging.error('Spawn sumo actor failed: %s', error)
            return INVALID_ACTOR_ID

        if color is not None:
            color = color.split(',')
            traci.vehicle.setColor(actor_id, color)

        self._sequential_id += 1

        return actor_id

    @staticmethod
    def destroy_actor(actor_id):
        """
        Destroys the given actor.
        """
        traci.vehicle.remove(actor_id)

    def get_traffic_light_state(self, landmark_id):
        """
        Accessor for traffic light state.

        If the traffic ligth does not exist, returns None.
        """
        return self.traffic_light_manager.get_state(landmark_id)

    def switch_off_traffic_lights(self):
        """
        Switch off all traffic lights.
        """
        self.traffic_light_manager.switch_off()

    def synchronize_vehicle(self, vehicle_id, transform, signals=None):
        """
        Updates vehicle state.

            :param vehicle_id: id of the actor to be updated.
            :param transform: new vehicle transform (i.e., position and rotation).
            :param signals: new vehicle signals.
            :return: True if successfully updated. Otherwise, False.
        """
        loc_x, loc_y = transform.location.x, transform.location.y
        yaw = transform.rotation.yaw

        traci.vehicle.moveToXY(vehicle_id, "", 0, loc_x, loc_y, angle=yaw, keepRoute=2)
        if signals is not None:
            traci.vehicle.setSignals(vehicle_id, signals)
        return True

    def synchronize_traffic_light(self, landmark_id, state):
        """
        Updates traffic light state.

            :param tl_id: id of the traffic light to be updated (logic id, link index).
            :param state: new traffic light state.
            :return: True if successfully updated. Otherwise, False.
        """
        self.traffic_light_manager.set_state(landmark_id, state)

    def tick(self):
        """
        Tick to sumo simulation.
        """
        traci.simulationStep()

        self.traffic_light_manager.tick()

        # Update data structures for the current frame.
        self.spawned_actors = set(traci.simulation.getDepartedIDList())
        self.destroyed_actors = set(traci.simulation.getArrivedIDList())

    @staticmethod
    def close():
        """
        Closes traci client.
        """
        traci.close()


# ==================================================================================================
# --------------------------------------------------------------------------------------------------
# -- carla_simulation.py ---------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# ==================================================================================================

# ==================================================================================================
# -- carla simulation ------------------------------------------------------------------------------
# ==================================================================================================

class CarlaSimulation(object):
    """
    CarlaSimulation is responsible for the management of the carla simulation.
    """
    def __init__(self, host, port, step_length):
        self.client = carla.Client(host, port)
        self.client.set_timeout(2.0)

        self.world = self.client.get_world()
        self.blueprint_library = self.world.get_blueprint_library()
        self.step_length = step_length

        # The following sets contain updated information for the current frame.
        self._active_actors = set()
        self.spawned_actors = set()
        self.destroyed_actors = set()

        # Set traffic lights.
        self._tls = {}  # {landmark_id: traffic_ligth_actor}

        tmp_map = self.world.get_map()
        for landmark in tmp_map.get_all_landmarks_of_type('1000001'):
            if landmark.id != '':
                traffic_ligth = self.world.get_traffic_light(landmark)
                if traffic_ligth is not None:
                    self._tls[landmark.id] = traffic_ligth
                else:
                    logging.warning('Landmark %s is not linked to any traffic light', landmark.id)

    def get_actor(self, actor_id):
        """
        Accessor for carla actor.
        """
        return self.world.get_actor(actor_id)

    # This is a workaround to fix synchronization issues when other carla clients remove an actor in
    # carla without waiting for tick (e.g., running sumo co-simulation and manual control at the
    # same time)
    def get_actor_light_state(self, actor_id):
        """
        Accessor for carla actor light state.

        If the actor is not alive, returns None.
        """
        try:
            actor = self.get_actor(actor_id)
            return actor.get_light_state()
        except RuntimeError:
            return None

    @property
    def traffic_light_ids(self):
        return set(self._tls.keys())

    def get_traffic_light_state(self, landmark_id):
        """
        Accessor for traffic light state.

        If the traffic ligth does not exist, returns None.
        """
        if landmark_id not in self._tls:
            return None
        return self._tls[landmark_id].state

    def switch_off_traffic_lights(self):
        """
        Switch off all traffic lights.
        """
        for actor in self.world.get_actors():
            if actor.type_id == 'traffic.traffic_light':
                actor.freeze(True)
                # We set the traffic light to 'green' because 'off' state sets the traffic light to
                # 'red'.
                actor.set_state(carla.TrafficLightState.Green)

    def spawn_actor(self, blueprint, transform):
        """
        Spawns a new actor.

            :param blueprint: blueprint of the actor to be spawned.
            :param transform: transform where the actor will be spawned.
            :return: actor id if the actor is successfully spawned. Otherwise, INVALID_ACTOR_ID.
        """
        transform = carla.Transform(transform.location + carla.Location(0, 0, SPAWN_OFFSET_Z),
                                    transform.rotation)

        batch = [
            carla.command.SpawnActor(blueprint, transform).then(
                carla.command.SetSimulatePhysics(carla.command.FutureActor, False))
        ]
        response = self.client.apply_batch_sync(batch, False)[0]
        if response.error:
            logging.error('Spawn carla actor failed. %s', response.error)
            return INVALID_ACTOR_ID

        return response.actor_id

    def destroy_actor(self, actor_id):
        """
        Destroys the given actor.
        """
        actor = self.world.get_actor(actor_id)
        if actor is not None:
            return actor.destroy()
        return False

    def synchronize_vehicle(self, vehicle_id, transform, lights=None):
        """
        Updates vehicle state.

            :param vehicle_id: id of the actor to be updated.
            :param transform: new vehicle transform (i.e., position and rotation).
            :param lights: new vehicle light state.
            :return: True if successfully updated. Otherwise, False.
        """
        vehicle = self.world.get_actor(vehicle_id)
        if vehicle is None:
            return False

        vehicle.set_transform(transform)
        if lights is not None:
            vehicle.set_light_state(carla.VehicleLightState(lights))
        return True

    def synchronize_traffic_light(self, landmark_id, state):
        """
        Updates traffic light state.

            :param landmark_id: id of the landmark to be updated.
            :param state: new traffic light state.
            :return: True if successfully updated. Otherwise, False.
        """
        if not landmark_id in self._tls:
            logging.warning('Landmark %s not found in carla', landmark_id)
            return False

        traffic_light = self._tls[landmark_id]
        traffic_light.set_state(state)
        return True

    def tick(self):
        """
        Tick to carla simulation.
        """
        self.world.tick()

        # Update data structures for the current frame.
        current_actors = set(
            [vehicle.id for vehicle in self.world.get_actors().filter('vehicle.*')])
        self.spawned_actors = current_actors.difference(self._active_actors)
        self.destroyed_actors = self._active_actors.difference(current_actors)
        self._active_actors = current_actors

    def close(self):
        """
        Closes carla client.
        """
        for actor in self.world.get_actors():
            if actor.type_id == 'traffic.traffic_light':
                actor.freeze(False)

# ==================================================================================================
# -- ROS Node Class --------------------------------------------------------------------------------
# ==================================================================================================

class rosNode:
    def __init__(self, carla_sim, sumo_sim, carla_map):
        rospy.init_node("cosimulation_client", anonymous=True)
        pub_topic_name = "/vehicle/sim_state" # Will have to create new message type for this
        sub_topic_name = "/vehicle/state_est"

        self.pub = rospy.Publisher(pub_topic_name, sim_state, queue_size=5)
        self.sub = rospy.Subscriber(sub_topic_name, state_est, self.callback)
        
        self.current_ego_state = {'t':0, 'x':0, 'y':0, 'psi':0,'lat':0, 'lon':0}
        self.state_traj = []
        self.ego_color = (255, 0, 0)
        self.ego_check = 0      # 0 means not yet spawned, 1 means ready to spawn, 2 means spawned, 3 means Carla Autopilot

        self.carla_actor = None
        self.sumo_actor = None

        self.carla_sim = carla_sim
        self.sumo_sim = sumo_sim

        self.carla_map = carla_map
        self.carla_offset = []

        # Array to be published
        self.curr_sim = []

    """
    Spawns the ego vehicle. Currently spawning in a random location
    """
    def spawn(self):
        # Spawning in Carla
        ego_carla_blueprint = random.choice(self.carla_sim.blueprint_library.filter('vehicle'))
        #if ego_carla_blueprint.has_attribute('color'):
        #    ego_carla_blueprint.set_attribute('color', self.ego_vehicle.ego_color)

        # Obtain the Carla.transform for random spawn_points
        transform = random.choice(self.carla_map.get_spawn_points())
    
        """
        # Fix the x,y,z position to check where it spawns. Not working right now, will comment out
        transform.location.x = 390
        transform.location.y = 331
        transform.location.z = 1.5
        transform.rotation.yaw = 0"""

        # Tell the Carla world to spawn the vehicle
        self.carla_actor = self.carla_sim.world.spawn_actor(ego_carla_blueprint, transform)


        # Setting offset
        location = self.carla_actor.get_location()
        self.carla_offset = [location.x - self.current_ego_state['x'], location.y - self.current_ego_state['y']]

        # Spawning in Sumo based on Carla object. POTENTIAL ISSUE: Cannot create sumo object because blueprints can't translate
        sumo_type_id = BridgeHelper.get_sumo_vtype(self.carla_actor)
        color = self.carla_actor.attributes.get('color', None)
        if sumo_type_id is not None:
            self.sumo_actor = self.sumo_sim.spawn_actor(sumo_type_id, color)
            if self.sumo_actor != INVALID_ACTOR_ID:
                self.sumo_sim.subscribe(self.sumo_actor)

        self.ego_check = 2

    """
    Gets the current state of the vehicle
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
        data = sim_state()
        for veh in self.curr_sim:
            data.npc_states.append(veh[1])
            data.ids.append(veh[0])

        self.pub.publish(data)

    """
    Adds the actor and its state to curr_sim as a state_est type
    Params:
        actor - the actor object to get attributes from Carla sim; will always be a Carla actor object
        sim - integer describing what simulation actor is from, 0=Carla, 1=Sumo, anything else errors
    Result (no return):
        Appends data[] to curr_sim where:
        data[0] - String identifier starting with simulation name followed by the ID of the actor in that simulation
        data[1] - state_est of actor
    """
    def add_state(self, actor, sim):
        if not (sim == 0 or sim == 1):
            raise Exception("Cannot add state for actor that isn't in Sumo or Carla. Please specify with parameter sim=0 or 1 for Carla or Sumo respectively")
            exit()

        data = []
        name = ""
        state = state_est()
        state.df = 0
        if sim == 1:
            name = "sumo_" + str(actor.id)
        else:
            name = "carla_" + str(actor.id)

        actor_transform = actor.get_transform()
        velocity = actor.get_velocity()
        angular_velocity = actor.get_angular_velocity()
        accel = actor.get_acceleration()
        geo_loc = self.carla_map.transform_to_geolocation(actor_transform.location)

        state.x = actor_transform.location.x - self.carla_offset[0]
        state.y = actor_transform.location.y - self.carla_offset[1]
        state.psi = actor_transform.rotation.yaw * math.pi/180

        state.v = math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)

        state.lon = geo_loc.longitude
        state.lat = geo_loc.latitude
        state.v_long = velocity.y
        state.v_lat = velocity.x

        state.yaw_rate = angular_velocity.z

        state.a_long = accel.y
        state.a_lat = accel.x

        data += [name, state]

        self.curr_sim.append(data)

    """
    Updates the current carla actor transform with the current_ego_state
    Returns the new transform
    """
    def update_carla_state(self):
        transform = self.carla_actor.get_transform()

        # Updating with current_state
        transform.location.x = self.current_ego_state['x'] + self.carla_offset[0]
        transform.location.y = self.current_ego_state['y'] + self.carla_offset[1]
        transform.location.y = -transform.location.y 
        transform.rotation.yaw = self.current_ego_state['psi']*180/3.1415
        transform.rotation.yaw *= -1

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
