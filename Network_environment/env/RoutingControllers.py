import sys
import random
from abc import ABCMeta, abstractmethod


class RoutingAlgorithm(object):

    def __init__(self, node, graph):
        self.node = node
        self.graph = graph

    @abstractmethod
    def route_packet(self, packet):
        raise NotImplementedError()


class RandomRouting(RoutingAlgorithm):

    def __init__(self, node, graph, gen):
        super().__init__(node=node, graph=graph)
        self.gen = gen

    def route_packet(self, packet):
        if not self.node.routes:
            return None

        for link in self.node.routes.values():
            if link.dst.id == packet.dst:
                return link
        link = random.choice(list(self.node.routes.values()))
        while not link.state:
            link = random.choice(list(self.node.routes.values()))
        return link


class Dijkstra(RoutingAlgorithm):

    def __init__(self, node, graph):
        super().__init__(node=node, graph=graph)

    def route_packet(self, packet):

        def min_distance(distance, spt_set, self_nodes):
            minimum = sys.maxsize
            minimum_node = None
            for curr_node in self_nodes.values():
                if distance[curr_node.id] < minimum and not spt_set[curr_node.id]:
                    minimum = distance[curr_node.id]
                    minimum_node = curr_node
            return minimum_node

        if self.graph.contains_node(self.node.id) and self.graph.contains_node(packet.dst):
            src = self.graph.nodes[self.node.id]
            dst = self.graph.nodes[packet.dst]

            dist = self.graph.nodes.copy()
            for node in dist.keys():
                dist[node] = sys.maxsize
            dist[src.id] = 0

            sptSet = self.graph.nodes.copy()
            for node in sptSet.keys():
                sptSet[node] = False

            path = self.graph.nodes.copy()
            for node in path.keys():
                path[node] = []

            for count in range(len(self.graph.nodes)):
                current = min_distance(distance=dist, spt_set=sptSet, self_nodes=self.graph.nodes)
                sptSet[current.id] = True
                if current == dst:
                    break

                for v in self.graph.nodes.values():
                    if current.is_neighbour(v) and not sptSet[v.id] and dist[v.id] > dist[current.id] + current.routes["{}_{}".format(current.id, v.id)].cost:
                        if current.routes["{}_{}".format(current.id, v.id)].state:
                            dist[v.id] = dist[current.id] + current.routes["{}_{}".format(current.id, v.id)].cost
                            path[v.id] = path[current.id].copy()
                            path[v.id].append(v)

            #print("The distance between node " + str(src.id) + " and node " + str(dst.id) + " is " + str(dist[dst.id]))
            #print("The path towards destination is " + str(i for i in path[dst.id]))
            #print(path[dst.id][0].id)
            return self.node.routes["{}_{}".format(self.node.id, path[dst.id][0].id)]
        else:
            print("Either destination or source not in the graph")
            return None
