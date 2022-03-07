from manim import *
import numpy as np

class BinaryCase(Scene):
    @staticmethod
    def matrix(*args, **kwargs):
        return Matrix(*args, h_buff=1.8, v_buff=1).scale(0.8)

    def construct(self):
        rng = np.random.default_rng(0)
        y = np.expand_dims(rng.random(5), 1)
        y_true = np.expand_dims(np.array([1, 0, 0, 1, 0], dtype=int), 1)

        m = self.matrix(y.round(2)).shift(RIGHT * 3)
        y_text = MathTex(r"\hat{y} =").next_to(m, direction=LEFT)

        g1 = Group(m, y_text)
        self.play(FadeIn(g1))
        self.wait(2)

        m2 = self.matrix((1 - y).round(2)).shift(LEFT * 2)
        y2_text = MathTex(r"(1 - \hat{y}) =").next_to(m2, direction=LEFT)

        g2 = Group(m2, y2_text)
        self.play(FadeIn(g2))
        self.wait(3)

        logm = self.matrix(np.log(y).round(2)).shift(RIGHT * 3)
        logy_text = MathTex(r"\log{\hat{y}} =").next_to(logm, direction=LEFT)

        logm2 = self.matrix(np.log(1 - y).round(2)).shift(LEFT * 2)
        logy2_text = MathTex(r"\log{(1 - \hat{y})} =").next_to(logm2, direction=LEFT)

        log_g1 = Group(logm, logy_text)
        log_g2 = Group(logm2, logy2_text)

        self.play(Transform(g1, log_g1), Transform(g2, log_g2))
        self.wait(3)

        gg = Group(g1, g2)
        mat = self.matrix(
            np.hstack(
                (
                    np.log(1 - y).round(2),
                    np.log(y).round(2),
                ),
            ),
        ).shift(LEFT)
        mat_annot1 = MathTex(r"\log(1 - \hat{y})").next_to(mat.get_columns()[0], direction=UP).scale(0.6).shift(0.1 * LEFT + 0.1 * UP)
        mat_annot2 = MathTex(r"\log(\hat{y})").next_to(mat.get_columns()[1], direction=UP).scale(0.6).shift(0.1 * RIGHT + 0.1 * UP)
        nlll_eqn = MathTex(r"y \log{\hat{y}} + (1 - y) \log{(1 - \hat{y})}")\
            .next_to(mat.get_columns()[1], direction=UP).scale(0.6).shift(3.1 * RIGHT + 0.1 * UP)
        mat_brace = Brace(mat, direction=DOWN)
        mat_brace_text = Text("Log predicted probabilities", font_size=24).next_to(mat_brace, direction=DOWN)

        self.play(
            Transform(gg, mat),
            Create(mat_annot1),
            Create(mat_annot2),
            Create(nlll_eqn),
            FadeIn(mat_brace),
            FadeIn(mat_brace_text),
        )
        self.wait(3)

        m_true = self.matrix(y_true.round(0)).shift(LEFT * 4)
        y_true_text = MathTex(r"y =").next_to(m_true, direction=LEFT)
        g_true = Group(m_true, y_true_text)
        m_true_brace = Brace(m_true, direction=DOWN)
        m_true_brace_text = Text("True labels", font_size=24).next_to(m_true_brace, direction=DOWN)
        self.play(FadeIn(g_true), FadeIn(m_true_brace), FadeIn(m_true_brace_text))
        self.wait(3)

        # Masking desired negative log values
        arrows = []
        r_boxes = []
        nllls = []
        nlll_sum = 0
        for i in range(5):
            l_entry = m_true.get_entries()[i]
            r_entry = mat.get_columns()[y_true[i, 0]][i]
            arrows.append(
                Arrow(
                    start=l_entry.get_center(),
                    end=r_entry.get_center() + 0.3 * LEFT,
                )
            )
            r_boxes.append(SurroundingRectangle(r_entry))
            nlll = np.log(y[i, 0]).round(2) if y_true[i, 0] == 1 else np.log(1 - y[i, 0]).round(2)
            nllls.append(
                MathTex(nlll).next_to(
                    mat.get_columns()[1][i],
                    direction=RIGHT,
                ).shift(RIGHT * 1.4).scale(0.8)
            )
            nlll_sum += nlll

        for i in range(len(arrows)):
            if i == 0:
                self.play(
                    Create(arrows[i]),
                    Create(r_boxes[i]),
                    Write(nllls[i]),
                )
            else:
                self.play(
                    ReplacementTransform(arrows[i-1], arrows[i]),
                    Create(r_boxes[i]),
                    Write(nllls[i]),
                )
        self.play(FadeOut(arrows[i]))

        # Summing up the log likelihoods
        brace = Brace(mat, direction=RIGHT).shift(RIGHT * 3)
        nlll_text = MathTex(round(nlll_sum, 2)).next_to(brace, direction=RIGHT)
        self.play(Write(brace), Write(nlll_text))

        self.wait(5)


class MultiCase(Scene):
    @staticmethod
    def matrix(*args, **kwargs):
        return Matrix(*args, h_buff=1.8, v_buff=1).scale(0.8)

    def construct(self):
        rng = np.random.default_rng(0)
        z = rng.normal(0, 1, (5, 3))
        y = (np.exp(z).T / np.exp(z).sum(1)).T
        y_true = np.expand_dims(np.array([0, 2, 2, 0, 1], dtype=int), 1)

        # Raw prediction socres (z)
        m = self.matrix(z.round(2))
        z_text = MathTex(r"z =").next_to(m, direction=LEFT)
        self.play(FadeIn(m), FadeIn(z_text))
        self.wait(3)

        # Softmax transform (y_hat)
        m2 = self.matrix(y.round(2))
        y_text = MathTex(r"\hat{y} = \text{softmax}(z) = ").next_to(m2, direction=LEFT)
        self.play(ReplacementTransform(m, m2), ReplacementTransform(z_text, y_text))
        self.wait(3)

        y_text_brief = MathTex(r"\hat{y}=").next_to(m2, direction=LEFT)
        self.play(ReplacementTransform(y_text, y_text_brief))
        self.wait(1)

        # Log y_hat
        logm = self.matrix(np.log(y).round(2))
        logy_text = MathTex(r"\log{\hat{y}} =").next_to(logm, direction=LEFT)
        self.play(
            ReplacementTransform(m2, logm),
            ReplacementTransform(y_text_brief, logy_text),
        )
        self.wait(3)

        mat_annot1 = MathTex(r"\log\hat{y}^{(0)}").next_to(logm.get_columns()[0], direction=UP).scale(0.6).shift(0.2 * RIGHT + 0.1 * UP)
        mat_annot2 = MathTex(r"\log\hat{y}^{(1)}").next_to(logm.get_columns()[1], direction=UP).scale(0.6).shift(0.2 * RIGHT + 0.1 * UP)
        mat_annot3 = MathTex(r"\log\hat{y}^{(2)}").next_to(logm.get_columns()[2], direction=UP).scale(0.6).shift(0.2 * RIGHT + 0.1 * UP)
        nlll_eqn = MathTex(r"\log{\hat{y}^{(y_i)}}").next_to(logm.get_columns()[2], direction=UP).scale(0.6).shift(2.1 * RIGHT + 0.1 * UP)
        mat_brace = Brace(logm, direction=DOWN)
        mat_brace_text = Text("Log predicted probabilities", font_size=24).next_to(mat_brace, direction=DOWN)

        self.play(
            Create(mat_annot1),
            Create(mat_annot2),
            Create(mat_annot3),
            Create(nlll_eqn),
            FadeIn(mat_brace),
            FadeIn(mat_brace_text),
        )

        m_true = self.matrix(y_true.round(0)).shift(LEFT * 5)
        y_true_text = MathTex(r"y =").next_to(m_true, direction=LEFT)
        g_true = Group(m_true, y_true_text)
        m_true_brace = Brace(m_true, direction=DOWN)
        m_true_brace_text = Text("True labels", font_size=24).next_to(m_true_brace, direction=DOWN)
        self.play(FadeIn(g_true), FadeIn(m_true_brace), FadeIn(m_true_brace_text))
        self.wait(3)

        # Masking desired negative log values
        arrows = []
        r_boxes = []
        nllls = []
        nlll_sum = 0
        for i in range(5):
            l_entry = m_true.get_entries()[i]
            r_entry = logm.get_columns()[y_true[i, 0]][i]
            arrows.append(
                Arrow(
                    start=l_entry.get_center(),
                    end=r_entry.get_center() + 0.3 * LEFT,
                )
            )
            r_boxes.append(SurroundingRectangle(r_entry))
            nlll = np.log(y[i, y_true[i,0]]).round(2)
            nllls.append(
                MathTex(nlll).next_to(
                    logm.get_columns()[2][i],
                    direction=RIGHT,
                ).shift(RIGHT * 0.7).scale(0.8)
            )
            nlll_sum += nlll

        for i in range(len(arrows)):
            if i == 0:
                self.play(
                    Create(arrows[i]),
                    Create(r_boxes[i]),
                    Write(nllls[i]),
                )
            else:
                self.play(
                    ReplacementTransform(arrows[i-1], arrows[i]),
                    Create(r_boxes[i]),
                    Write(nllls[i]),
                )
        self.play(FadeOut(arrows[i]))

        # Summing up the log likelihoods
        brace = Brace(logm, direction=RIGHT).shift(RIGHT * 2)
        nlll_text = MathTex(round(nlll_sum, 2)).next_to(brace, direction=RIGHT)
        self.play(Write(brace), Write(nlll_text))

        self.wait(5)
