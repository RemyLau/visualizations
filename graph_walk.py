import random

import networkx as nx
from manim import *


class RandomWalkOnGraph(Scene):
    def construct(self):
        random.seed(0)
        init_node = 0
        walk_length = 50
        init_pos = 2 * RIGHT  # initial current position of the star

        # Create graph
        nodes = list(range(10))
        edges = [
            (0, 1),
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 4),
            (4, 5),
            (4, 6),
            (2, 7),
            (7, 8),
            (8, 9),
        ]
        nxg = nx.Graph()
        nxg.add_nodes_from(nodes)
        nxg.add_edges_from(edges)
        g = Graph.from_networkx(
            nxg,
            layout="kamada_kawai",
            labels=True,
            layout_scale=3.4,
        )
        self.play(Create(g))

        # Create star walker
        star = Star(n=5, outer_radius=0.5, inner_radius=0.3, density=2)
        star.shift(init_pos)
        star.set_fill(BLUE, opacity=0.8)
        self.play(Create(star))
        self.wait(0.1)

        # Move walker to node 0
        relative_shift = g[init_node].get_center() - star.get_center()
        self.play(star.animate.shift(relative_shift))
        self.wait(1)

        # Generate random walk starting from init node
        cur_node = init_node
        for _ in range(walk_length):
            cur_node = random.choice(list(nxg[cur_node]))

            relative_shift = g[cur_node].get_center() - star.get_center()
            self.play(star.animate.shift(relative_shift), run_time=0.5)
            self.wait(0.1)

        self.wait(1)
