from manim import *
import networkx as nx
from manimnx import ManimGraph


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

class RandomGraph(Scene):
    def construct(self):
        g = ManimGraph(nx.erdos_renyi_graph(10, 0.5))

        self.play(*[Create(m) for m in g])  # show random graph creation
        self.wait(1)
