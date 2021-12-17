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
            r"\mathbb{P}(v \in \mathcal{N}(u) | u) = \frac{w(u,v)}{\sum_{v' \in \mathcal{N}(u)}w(u, v')}",
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


class TransitionProbabilitySecondOrder(RandomWalk):
    def construct(self):
        title_font_size = 24
        txt_font_size = 21
        eqn_font_size = 26
        title_pos = RIGHT + 2.5 * UP

        # Setup title: 2nd order transition illustration
        title = Text(
            r"Second order transition ",
            font_size=title_font_size,
        ).shift(title_pos)
        title_note = Text(
            r"(depends on the previous node)",
            font_size=title_font_size,
        ).next_to(title, RIGHT)
        box_take_home = SurroundingRectangle(title_note)

        self.setup_scene_single()
        nodes_to_remove = [4, 5, 6, 7, 8, 9]
        self.g.remove_vertices(*nodes_to_remove)
        self.add(title, title_note)
        self.wait(5)

        # Key idea of three different types of edges
        txt_idea = Text(
            r"Key idea: flexibly reweight 3 different types of edges",
            font_size=txt_font_size,
        ).next_to(title, DOWN).align_to(title, LEFT).shift(0.2 * RIGHT)

        txt_in = Text(
            "in",
            font_size=txt_font_size,
        ).next_to(txt_idea, DOWN).align_to(txt_idea, LEFT)
        box_in = SurroundingRectangle(txt_in, color=WHITE)

        txt_out = Text(
            "out",
            font_size=txt_font_size,
            color=YELLOW,
        ).next_to(txt_in, RIGHT)
        box_out = SurroundingRectangle(txt_out, color=YELLOW)

        txt_return = Text(
            "return",
            font_size=txt_font_size,
            color=RED,
        ).next_to(txt_out, RIGHT)
        box_return = SurroundingRectangle(txt_return, color=RED)

        # Setup example with current node = n1, and previous node = n3
        txt_ex = MathTex(
            r"Example: ",
            font_size=eqn_font_size,
        ).next_to(txt_in, DOWN).align_to(title, LEFT).shift(0.2 * DOWN)

        txt_cur = MathTex(
            r"\text{current node } (u) = n_1,\ ",
            font_size=eqn_font_size,
        ).next_to(txt_ex, RIGHT)
        box_cur = SurroundingRectangle(self.g[1])

        txt_prev = MathTex(
            r"\text{previous node } (x) = n_3",
            font_size=eqn_font_size,
        ).next_to(txt_cur, RIGHT)
        box_prev = SurroundingRectangle(self.g[3])

        prev_to_cur = CurvedArrow(
            start_point=self.g[3].get_center(),
            end_point=self.g[1].get_center(),
            angle=-PI/4,
            stroke_width=2,
        )

        self.play(FadeIn(txt_idea))
        self.wait(6)

        self.play(
            AnimationGroup(
                Write(txt_in),
                Write(txt_out),
                Write(txt_return),
                run_time=4,
                lag_ratio=1,
            )
        )
        self.wait(2)

        self.play(FadeIn(txt_ex))
        self.wait(2)

        self.play(AnimationGroup(FadeIn(txt_cur), Create(box_cur), run_time=1))
        self.wait(3)

        self.play(
            AnimationGroup(
                FadeIn(txt_prev),
                ReplacementTransform(box_cur, box_prev),
                run_time=1,
            )
        )
        self.wait(5)

        self.play(AnimationGroup(Uncreate(box_prev), Create(prev_to_cur)))
        self.wait(4)

        # Show example of second order edges
        cur_to_n2 = Arrow(start=self.g[1].get_center(), end=self.g[2].get_center())
        self.play(
            AnimationGroup(
                Create(box_in),
                Create(cur_to_n2),
                lag_ratio=2,
                run_time=4,
            )
        )
        self.wait(9)

        cur_to_n0 = Arrow(start=self.g[1].get_center(), end=self.g[0].get_center(), color=YELLOW)
        self.play(
            AnimationGroup(
                ReplacementTransform(box_in, box_out),
                Create(cur_to_n0),
                lag_ratio=2,
                run_time=4,
            )
        )
        self.wait(6)

        cur_to_n3 = Arrow(start=self.g[1].get_center(), end=self.g[3].get_center(), color=RED)
        self.play(
            AnimationGroup(
                ReplacementTransform(box_out, box_return),
                Create(cur_to_n3),
                lag_ratio=2,
                run_time=4,
            )
        )
        self.play(Uncreate(box_return))
        self.wait(4)

        # Dsiplay biased transition probability equation
        txt_apply = MathTex(
            r"\text{Apply bias factor }\alpha_{p,q}(x,v) ",
            r"&=1 &\text{if } d_G(x,v) = 1\\",
            r"&=1/q &\text{if } d_G(x,v) = 2\\",
            r"&=1/p &\text{if } d_G(x,v) = 0",
            font_size=eqn_font_size,
        ).next_to(txt_ex, 1.8 * DOWN).align_to(txt_ex, LEFT)

        self.play(FadeIn(txt_apply))
        self.wait(5)

        # Formula for 2nd order transition probability
        eqn_tran_prob = MathTex(
            r"\mathbb{P}(v | u, x) = "
            r"\frac{\alpha_{p,q}(x,v)w(u,v)}"
            r"{\sum_{v' \in \mathcal{N}(u)}\alpha_{p,q}(x,v')w(u, v')}",
            font_size=1.3*eqn_font_size,
        ).next_to(txt_apply, DOWN).align_to(txt_apply, LEFT).shift(0.5*DOWN)
        self.play(Write(eqn_tran_prob))
        self.wait(10)

        # Take home: 2nd order random walk also depends on the previous node
        self.play(Create(box_take_home))
        self.wait(2)


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
