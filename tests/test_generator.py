import unittest

from generator.engine import Engine, cjk_len, load_chapters, render_novel
from generator.main import ngrams
from generator.voices import wrap_line


class TestChapters(unittest.TestCase):
    def test_fifty_numbered_chapters(self):
        chapters = load_chapters()
        self.assertEqual(len(chapters), 50)
        self.assertEqual([c["num"] for c in chapters], list(range(1, 51)))
        self.assertEqual(chapters[-1]["title"], "其余势力")
        titles = [c["title"] for c in chapters]
        self.assertNotIn("田园立项", titles)
        self.assertNotIn("第一滴小宇宙", titles)

    def test_scope_stops_at_discovery(self):
        text = "\n".join(c["title"] + c["doc"][1] for c in load_chapters()[-3:])
        self.assertIn("不是联盟", text)


class TestVoices(unittest.TestCase):
    def test_tony_not_uniform_tag(self):
        line = wrap_line("托尼", "红线很好。", 0)
        self.assertIn("红线很好", line)
        self.assertNotEqual(line, "「红线很好。」托尼说。")

    def test_luo_and_sophon_differ(self):
        a = wrap_line("罗辑", "别打。", 0)
        b = wrap_line("智子", "不要回答。", 0)
        self.assertIn("轻得像在抱怨旅馆空调", a)
        self.assertIn("没有停顿", b)
        self.assertNotEqual(a, b)


class TestEngine(unittest.TestCase):
    def test_sides_are_selective(self):
        eng = Engine()
        kinds = [tuple(eng.sides_for({"num": i})) for i in range(1, 51)]
        self.assertGreater(len(set(kinds)), 3)
        self.assertIn((), kinds)

    def test_ngram_includes_last_window(self):
        text = "甲" * 20
        c = ngrams(text, 20)
        self.assertEqual(c["甲" * 20], 1)

    def test_no_padding_loop_in_source(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[1] / "generator"
        engine = (root / "engine.py").read_text(encoding="utf-8")
        main = (root / "main.py").read_text(encoding="utf-8")
        self.assertNotIn("while cjk_len(text) < 200000", engine + main)
        self.assertNotIn("text += (", main)

    def test_render_skips_padding_and_old_street(self):
        text = render_novel()
        self.assertNotIn("值班补记", text)
        self.assertNotIn("相关新闻当成一种更硬的天气", text)
        self.assertGreater(cjk_len(text), 80000)
        self.assertIn("其余势力已被点名", text)
        self.assertIn("嘲讽在前", text)
        hot = [(g, n) for g, n in ngrams(text, 20).most_common(5) if n >= 40]
        self.assertEqual(hot, [])


if __name__ == "__main__":
    unittest.main()
