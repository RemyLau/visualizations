from manim import *
import networkx as nx


class SampleGraph(Scene):
    def construct(self):
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
        g = Graph(
            nodes,
            edges,
            layout='kamada_kawai',
            labels=True,
            layout_scale=3.4,
        )
        self.play(Create(g))

        # Create star walker
        star = Star(n=5, outer_radius=0.5, inner_radius=0.3, density=2)
        init_pos = 2 * RIGHT  # initial position of the star
        star.shift(init_pos)
        star.set_fill(BLUE, opacity=0.8)
        self.play(Create(star))

        # Move walker to node 0
        self.play(star.animate.shift(g[0].get_center() - init_pos))
        self.wait(1)
