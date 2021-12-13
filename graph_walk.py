import random

import networkx as nx
from manim import *

GRAPH_POS = 2.8 * LEFT + 0.3 * UP
WALKER_POS = RIGHT
WALK_LENGTH = 24
TEST = False


def get_walker(pos=WALKER_POS, color=BLUE):
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
        txt_pos = 2.4 * RIGHT + 0.6 * UP

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

        txt1 = Text(r"Real random walker", font_size=font_size)
        txt2 = Text(r"Not an actor", font_size=font_size)

        # Generate random walk starting from init node
        cur_node = init_node
        for i in range(WALK_LENGTH if not TEST else 8):
            cur_node = random.choice(list(nxg[cur_node]))

            relative_shift = g[cur_node].get_center() - walker.get_center()
            self.play(walker.animate.shift(relative_shift), run_time=0.8)
            self.wait(0.1)

            if i == 1:
                self.add(txt1.shift(txt_pos))
                self.wait(0.1)

            if i == 5:
                self.add(txt2.shift(txt_pos + 0.6 * DOWN))
                self.wait(0.1)

        self.wait(1)


class RandomWalk(Scene):
    def setup_scene(self, init_node=1, walker_color=BLUE):
        self.nxg, self.g = get_graph()
        self.walker = get_walker(pos=init_node, color=walker_color)
        self.walker.shift(
            self.g[init_node].get_center() - self.walker.get_center()
        )
        self.add(self.g, self.walker)


class TransitionProbability(RandomWalk):
    def construct(self):
        eqn_font_size = 32
        eqn_pos = 2.4 * RIGHT + 2.5 * UP

        self.setup_scene()
        self.wait(1 if not TEST else 0.1)

        nodes_to_remove = [4, 5, 6, 7, 8, 9]
        #self.play(self.g.animate.remove_vertices(*nodes_to_remove))
        self.g.remove_vertices(*nodes_to_remove)
        self.g.remove_edges((2, 3))
        self.wait(5 if not TEST else 0.1)

        eqn1 = MathTex(
            r"\mathbb{P}(v \in \mathcal{N}(u) | u) = \frac1{|\mathcal{N}(u)|}",
            font_size=eqn_font_size
        ).shift(eqn_pos)

        eqn2 = MathTex(
            r"\mathbb{P}(n_3 | n_1) = \mathbb{P}(n_2 | n_1) = \mathbb{P}(n_0 | n_1) = \frac13",
            font_size=eqn_font_size
        ).shift(eqn_pos + DOWN)

        txt3= Text(
            "Could also work with weighted graphs:",
            font_size=eqn_font_size
        ).shift(eqn_pos + 2.5 * DOWN)

        eqn4 = MathTex(
            r"\mathbb{P}(v \in \mathcal{N}(u) | v) = \frac{w(u,v)}{\sum_{v' \in \mathcal{N}(u)}w(u, v')}",
            font_size=eqn_font_size
        ).shift(eqn_pos + 3.5 * DOWN)

        self.add(eqn1)
        self.wait(4 if not TEST else 0.1)

        self.add(eqn2)
        self.wait(5 if not TEST else 0.1)

        self.add(txt3)
        self.wait(1 if not TEST else 0.1)

        self.add(eqn4)
        self.wait(1 if not TEST else 0.1)


class RecordSingleRandomWalk(RandomWalk):
    def construct(self):
        random.seed(0)
        font_size = 36
        txt_pos = 2.4 * RIGHT + 0.6 * UP
        walk_hist_pos = 1.2 * RIGHT + 2.5 * UP
        walk_hist_font_size = 29
        walk_hist_record_length = 9
        walker_color = BLUE
        init_node = 1

        txt1 = Text(r"Real random walker", font_size=font_size)
        txt2 = Text(r"Not an actor", font_size=font_size)

        self.setup_scene(init_node=init_node, walker_color=walker_color)

        # Generate random walk starting from init node
        cur_node = init_node
        self.add(
            Text(
                str(init_node),
                font_size=walk_hist_font_size,
                color=walker_color,
            ).shift(walk_hist_pos)
        )
        self.wait(1 if not TEST else 0.1)

        for i in range(WALK_LENGTH if not TEST else 12):
            cur_node = random.choice(list(self.nxg[cur_node]))

            relative_shift = self.g[cur_node].get_center() - self.walker.get_center()
            self.play(self.walker.animate.shift(relative_shift), run_time=0.8)
            self.wait(0.1)

            if i < walk_hist_record_length:
                # Record walk history
                head = Text(
                    str(cur_node),
                    font_size=walk_hist_font_size,
                    color=walker_color,
                ).shift(walk_hist_pos + (i + 1) * 0.4 * RIGHT)
                self.add(head)
                self.wait(0.1)
            elif i == walk_hist_record_length:
                head = Tex(
                    r"\dots",
                    font_size=walk_hist_font_size,
                    color=walker_color,
                ).shift(walk_hist_pos + (i + 1) * 0.4 * RIGHT)
                self.add(head)
                self.wait(0.1)

            if i == 5:
                self.add(txt1.shift(txt_pos))
                self.wait(0.1)

            if i == 9:
                self.add(txt2.shift(txt_pos + 0.6 * DOWN))
                self.wait(0.1)
