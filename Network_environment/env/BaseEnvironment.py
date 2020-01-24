import gym
import numpy as np
from Architecture import Network, Node, Link, RoutingAlgorithm
from SimComponents import Packet
import simpy
from numpy.random import RandomState
import random

class BaseEnv(gym.env):

    def __init__(self):
        self.env = simpy.Environment()
        self.gen = RandomState(2)

    def step(self, action):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def get_reward(self, action, state):
        raise NotImplementedError()

    def create_network(self, nodes, edges):

        myNetwork = Network(env=self.env, gen=self.gen)
        myNetwork.add_nodes(nodes=nodes)
        myNetwork.set_routing_algorithm(controller="random")
        myNetwork.add_links(edges)

        return myNetwork

    def render(self):
        pass


class MultiplePacketRoutingEnv(BaseEnv):

    def __init__(self):
        super(MultiplePacketRoutingEnv, self).__init__()
        pass

    def step(self,action):
        pass

    def reset(self):
        pass

    def get_reward(self, action, state):
        pass

    def initial_state(self):
        pass