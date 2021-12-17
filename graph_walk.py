import random

import networkx as nx
from manim import *

GRAPH_POS = 2.8 * LEFT + 0.3 * UP
WALKER_POS = RIGHT
WALK_LENGTH = 24
TEST = False
WALK_HIST_RECORD_LENGTH = 8
WALK_HIST_POS = 1.2 * RIGHT + 2.5 * UP
WALK_HIST_FONT_SIZE = 30


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

        txt1 = Text(r"Real random walker", font_size=font_size).shift(txt_pos)
        txt2 = Text(r"Not an actor", font_size=font_size).shift(txt_pos + 0.6 * DOWN)

        # Generate random walk starting from init node
        cur_node = init_node
        for i in range(WALK_LENGTH if not TEST else 8):
            cur_node = random.choice(list(nxg[cur_node]))

            relative_shift = g[cur_node].get_center() - walker.get_center()
            self.play(walker.animate.shift(relative_shift), run_time=0.8)

            if i == 6:
                self.add(txt1)

            if i == 10:
                self.add(txt2)

        self.wait(1)


class RandomWalk(Scene):
    def setup_scene_single(self, init_node=1, walker_color=BLUE):
        self.nxg, self.g = get_graph()
        self.walker = get_walker(pos=init_node, color=walker_color)
        self.walker.shift(
            self.g[init_node].get_center() - self.walker.get_center()
        )
        self.add(self.g, self.walker)

    def setup_scene_multi(self, init_nodes=(1,), walker_colors=(BLUE,)):
        self.nxg, self.g = get_graph()
        self.walkers = []
        for init_node, walker_color in zip(init_nodes, walker_colors):
            self.walkers.append(get_walker(pos=init_node, color=walker_color))
            self.walkers[-1].shift(
                self.g[init_node].get_center() - self.walkers[-1].get_center()
            )
        self.add(self.g, *self.walkers)


class TransitionProbability(RandomWalk):
    def construct(self):
        eqn_font_size = 32
        eqn_pos = 2.4 * RIGHT + 2 * UP

        self.setup_scene_single()
        self.wait(1 if not TEST else 0.1)

        nodes_to_remove = [4, 5, 6, 7, 8, 9]
        edges_to_remove = [
            (u, v) for u, v in self.g.edges
            if u in nodes_to_remove or v in nodes_to_remove
        ]
        to_remove = [self.g[v] for v in nodes_to_remove] \
            + [self.g.edges[e] for e in edges_to_remove]

        self.play(
            AnimationGroup(
                *map(Uncreate, to_remove),
                lag_ratio=0.2,
                run_time=1,
            )
        )
        self.wait(5)

        eqn1 = MathTex(
            r"\mathbb{P}(v \in \mathcal{N}(u) | u) = \frac1{|\mathcal{N}(u)|}",
            font_size=eqn_font_size
        ).shift(eqn_pos)

        eqn2 = MathTex(
            r"\Rightarrow \mathbb{P}(n_3 | n_1) = \mathbb{P}(n_2 | n_1) = \mathbb{P}(n_0 | n_1) = \frac13",
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

        self.play(Write(eqn1))
        self.wait(4 if not TEST else 0.1)

        self.play(Write(eqn2))
        self.wait(5 if not TEST else 0.1)

        self.play(Write(txt3))
        self.play(FadeIn(eqn4, shift=DOWN))
        self.wait(5 if not TEST else 0.1)

        self.play(
            AnimationGroup(
                FadeOut(txt3, shift=DOWN),
                FadeOut(eqn4, shift=DOWN),
                lag_ratio=0.2,
                run_time=0.4,
            )
        )
        self.wait(1)


class RecordSingleRandomWalk(RandomWalk):
    def construct(self):
        random.seed(0)
        font_size = 36
        walker_color = BLUE
        init_node = 1

        self.setup_scene_single(init_node=init_node, walker_color=walker_color)

        # Generate random walk starting from init node
        cur_node = init_node
        self.add(
            Tex(
                str(init_node),
                font_size=WALK_HIST_FONT_SIZE,
                color=walker_color,
            ).shift(WALK_HIST_POS + 0.2 * RIGHT)
        )
        self.wait(1 if not TEST else 0.1)

        for i in range(WALK_LENGTH if not TEST else 12):
            cur_node = random.choice(list(self.nxg[cur_node]))

            relative_shift = self.g[cur_node].get_center() - self.walker.get_center()
            self.play(self.walker.animate.shift(relative_shift), run_time=0.8)
            self.wait(0.1)

            if i < WALK_HIST_RECORD_LENGTH:
                # Record walk history
                head = MathTex(
                    f"\\rightarrow {cur_node}",
                    font_size=WALK_HIST_FONT_SIZE,
                    color=walker_color,
                ).shift(WALK_HIST_POS + (i + 1) * 0.6 * RIGHT)
                self.add(head)
            elif i == WALK_HIST_RECORD_LENGTH:
                head = Tex(
                    r"\dots",
                    font_size=WALK_HIST_FONT_SIZE,
                    color=walker_color,
                ).shift(WALK_HIST_POS + (i + 1) * 0.6 * RIGHT)
                self.add(head)


class RecordMultiRandomWalk(RandomWalk):
    def construct(self):
        random.seed(0)
        font_size = 36

        init_nodes = (1, 5, 6, 7, 9)
        walker_colors = (BLUE, YELLOW, RED, PURPLE, ORANGE)

        self.setup_scene_multi(init_nodes=init_nodes, walker_colors=walker_colors)

        # Generate random walk starting from init node
        cur_nodes = list(init_nodes)
        for i, (init_node, walker_color) in enumerate(zip(init_nodes, walker_colors)):
            self.add(
                Tex(
                    str(init_node),
                    font_size=WALK_HIST_FONT_SIZE,
                    color=walker_color,
                ).shift(WALK_HIST_POS + i * 1.1 * DOWN + 0.2 * RIGHT)
            )
        self.add(
            Tex(
                r"\vdots",
                font_size=WALK_HIST_FONT_SIZE,
                color=WHITE
            ).shift(WALK_HIST_POS + len(self.walkers) * 1.1 * DOWN + 0.2 * RIGHT)
        )
        self.wait(1 if not TEST else 0.1)

        for i in range(WALK_LENGTH if not TEST else 12):
            group = []
            for j, walker in enumerate(self.walkers):
                cur_nodes[j] = random.choice(list(self.nxg[cur_nodes[j]]))
                relative_shift = self.g[cur_nodes[j]].get_center() - walker.get_center()
                group.append(walker.animate.shift(relative_shift))

                if i <= WALK_HIST_RECORD_LENGTH:
                    head = MathTex(
                        r"\dots" if i == WALK_HIST_RECORD_LENGTH else f"\\rightarrow {cur_nodes[j]}",
                        font_size=WALK_HIST_FONT_SIZE,
                        color=walker_colors[j],
                    ).shift(WALK_HIST_POS + (i + 1) * 0.6 * RIGHT + j * 1.1 * DOWN)
                    group.append(FadeIn(head))

                    if i < WALK_HIST_RECORD_LENGTH and j == len(self.walkers) - 1:
                        head = Tex(r"\vdots", font_size=WALK_HIST_FONT_SIZE, color=WHITE)
                        head.shift(WALK_HIST_POS + (i + 1) * 0.6 * RIGHT + (j + 1) * 1.1 * DOWN + 0.2 * RIGHT)
                        group.append(FadeIn(head))

            self.play(
                AnimationGroup(
                    *group,
                    lag_ratio=0.1 if i == WALK_HIST_RECORD_LENGTH else 0.2,
                    run_time=0.7,
                )
            )
