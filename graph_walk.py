from manim import *
import networkx as nx


def get_sample_graph():
    nodes = list(range(9))
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
    ]
    return Graph(nodes, edges, layout='spring')


class LineExample(Scene):
    def construct(self):
        d = VGroup()
        for i in range(10):
            d.add(Dot())
        #d.arrange_in_grid(buff=1)
        d.arrange()
        self.add(d)

        l = Line(d[0], d[1])
        self.add(l)
        self.wait()

        l.put_start_and_end_on(d[1].get_center(), d[2].get_center())
        self.wait()

        l.put_start_and_end_on(d[4].get_center(), d[7].get_center())
        self.wait()


class SampleGraph(Scene):
    def construct(self):
        g = get_sample_graph()
        self.play(Create(g))

        star = Star(5, outer_radius=0.4, density=2, color=BLUE)
        self.play(Create(star))
        self.wait(1)
