import gym
import numpy as np
from Architecture import Network, Node, Link, RoutingAlgorithm
from SimComponents import Packet
import simpy
from numpy.random import RandomState
import random
from BaseEnvironment import BaseEnv


class SinglePacketRoutingEnv(BaseEnv):

    def __init__(self, nodes, edges, packet=None):
        self.__version__ = "1.0.0"
        self.name = "Simple Packet Routing Environment"
        super(SinglePacketRoutingEnv, self).__init__()

        self.graph = self.create_network(nodes=nodes, edges=edges)

        self.finished = False
        self.step_number = -1
        self.episode_number = -1
        self.num_nodes = len(self.graph.nodes.values())

        # State = [current node, source node, next node]
        self.state = self.initial_state(packet=packet)
        self.past_state = None

    def initial_state(self, packet=None):
        if packet is None:
            src = random.choice(list(self.graph.nodes.keys()))
            dst = random.choice(list(self.graph.nodes.keys()))
            while not dst == src:
                dst = random.choice(list(self.graph.nodes.keys()))

            pkt = Packet(time=self.graph.env.now, size=1, id=1, src=src, dst=dst)
            self.graph.add_packet(pkt=pkt)
        else:
            src = packet[0]
            dst = packet[1]

        pkt = Packet(time=self.graph.env.now, size=1, id=1, src=src, dst=dst)
        self.graph.add_packet(pkt=pkt)

        return (
            self.graph.nodes[src],
            self.graph.nodes[src],
            self.graph.nodes[dst],
        )

    def reset(self):
        self.graph.clear_packets()
        self.episode_number += 1
        self.step_number = -1
        self.finished = False
        self.state = self.initial_state()

    def step(self, action):
        self.step_number += 1

    def get_reward(self, action, state):
        pass
