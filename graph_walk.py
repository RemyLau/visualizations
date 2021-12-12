import random

import networkx as nx
from manim import *


class RandomWalkOnGraph(Scene):
    def construct(self):
        random.seed(0)
        init_node = 1
        walk_length = 20
        font_size = 36
        star_pos = RIGHT
        text_pos = 2.4 * RIGHT + 0.6 * UP
        graph_pos = 2.8 * LEFT + 0.3 * UP

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
        ).shift(graph_pos)
        self.play(Create(g))
        self.wait(2)

        # Create star walker
        star = Star(n=5, outer_radius=0.5, inner_radius=0.3, density=2)
        star.shift(star_pos)
        star.set_fill(BLUE, opacity=0.8)
        self.play(Create(star))
        self.wait(2)

        # Move walker to node 0
        relative_shift = g[init_node].get_center() - star.get_center()
        self.play(star.animate.shift(relative_shift))
        self.wait(2)

        text1 = Text(r"Real random walker", font_size=font_size)
        text2 = Text(r"Not an actor", font_size=font_size)

        # Generate random walk starting from init node
        cur_node = init_node
        for i in range(walk_length):
            cur_node = random.choice(list(nxg[cur_node]))

            relative_shift = g[cur_node].get_center() - star.get_center()
            self.play(star.animate.shift(relative_shift), run_time=0.8)
            self.wait(0.1)


            if i == 1:
                self.add(text1.shift(text_pos))
                self.wait(0.1)

            if i == 5:
                self.add(text2.shift(text_pos + 0.6 * DOWN))
                self.wait(0.1)

        self.wait(1)
