#!/usr/bin/env python2

"""
Temporary node to feed co-simulation node an ego vehicle.

Author: Phillip
"""

# All necessary imports here
import glob
import os
import sys

try:
    sys.path.append(
        glob.glob('/home/arpae/Documents/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' %
                  (sys.version_info.major, sys.version_info.minor,
                   'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

import random
import time
import logging
import rospy
import math

from ros_carla_sumo_integration.msg import state_est 

class dummyNode:
    def __init__(self):
        rospy.init_node("dummy_node", anonymous=True)
        pub_topic_name = "/vehicle/state_est"

        self.pub = rospy.Publisher(pub_topic_name, state_est, queue_size=10)

        self.actor = None
    
    def set_carla_world(self, world):
        self.world = world
        self.map = world.get_map()

    def spawn(self):
        print("Spawning actor")
        bp = random.choice(self.world.get_blueprint_library().filter('vehicle'))
        transform = random.choice(self.map.get_spawn_points())

        self.actor = self.world.spawn_actor(bp, transform)
        self.actor.set_autopilot(True)
        print("Spawn Successful")

    def destroy(self):
        print("Destroying Actor")
        self.actor.destroy()
        print("Successfully destroyed actor")

    def publish(self):
        state = state_est()
        actor_transform = self.actor.get_transform()
        velocity = self.actor.get_velocity()
        angular_velocity = self.actor.get_angular_velocity()
        accel = self.actor.get_acceleration()
        geo_loc = self.map.transform_to_geolocation(actor_transform.location)

        state.x = actor_transform.location.x
        state.y = actor_transform.location.y
        state.psi = actor_transform.rotation.yaw * math.pi/180

        state.v = math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)

        state.lon = geo_loc.longitude
        state.lat = geo_loc.latitude
        state.v_long = velocity.y
        state.v_lat = velocity.x

        state.yaw_rate = angular_velocity.z

        state.a_long = accel.y
        state.a_lat = accel.x

        print("Location: " + str(state.x) + ", " + str(state.y))

        self.pub.publish(state)

def main():
    ego = dummyNode()
    try:
        # Find Carla Client
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        # Add world to dummy node
        ego.set_carla_world(client.get_world())

        # Spawn dummyNode vehicle
        ego.spawn()
        # Loop - maybe go in ticks
        #   Publish dummyNode state
        while True:
            ego.publish()
            time.sleep(0.05) # The tick steps
            
    except KeyboardInterrupt:
        logging.info('Cancelled by user.')

    finally:
        print("Cleaning up")
        ego.destroy()
        self.carla.close()


if __name__ == "__main__":
    main()