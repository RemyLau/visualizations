import random

import networkx as nx
from manim import *

GRAPH_POS = 2.8 * LEFT + 0.3 * UP
WALKER_POS = RIGHT
WALK_LENGTH = 15
TEST = False


def get_walker(color=BLUE, pos=WALKER_POS):
    walker = Star(n=5, outer_radius=0.4, inner_radius=0.2, density=2, color=color)
    walker.set_fill(color, opacity=0.7)
    walker.shift(pos)
    return walker


def get_graph():
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
    ).shift(GRAPH_POS)

    return nxg, g


class RandomWalkOnGraph(Scene):
    def construct(self):
        random.seed(0)
        init_node = 1
        font_size = 36
        text_pos = 2.4 * RIGHT + 0.6 * UP

        nxg, g = get_graph()
        self.play(Create(g))
        self.wait(2 if not TEST else 0.1)

        # Create walker
        walker = get_walker()
        self.play(Create(walker))
        self.wait(2 if not TEST else 0.1)

        # Move walker to node 0
        relative_shift = g[init_node].get_center() - walker.get_center()
        self.play(walker.animate.shift(relative_shift))
        self.wait(2 if not TEST else 0.1)

        text1 = Text(r"Real random walker", font_size=font_size)
        text2 = Text(r"Not an actor", font_size=font_size)

        # Generate random walk starting from init node
        cur_node = init_node
        for i in range(WALK_LENGTH if not TEST else 8):
            cur_node = random.choice(list(nxg[cur_node]))

            relative_shift = g[cur_node].get_center() - walker.get_center()
            self.play(walker.animate.shift(relative_shift), run_time=0.8)
            self.wait(0.1)

            if i == 1:
                self.add(text1.shift(text_pos))
                self.wait(0.1)

            if i == 5:
                self.add(text2.shift(text_pos + 0.6 * DOWN))
                self.wait(0.1)

        self.wait(1)
