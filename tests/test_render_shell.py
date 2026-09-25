import unittest
from pathlib import Path

from web import render_shell


TEMPLATE = (Path(__file__).parents[1] / "web" / "shell.html").read_text(encoding="utf-8")
ENV = {"TITLE": "Tappy Plane", "SOURCE_URL": "https://github.com/doriaxengine/tappyplane"}


class RenderShellTests(unittest.TestCase):
    def test_controls(self):
        self.assertEqual(render_shell.render_controls("Flap [Space] [↑] or tap\nPause [P]"), "\n".join([
            '<span class="controls-copy">Flap</span>',
            "<kbd>Space</kbd>",
            "<kbd>↑</kbd>",
            '<span class="controls-copy">or tap</span>',
            '<span class="controls-copy">Pause</span>',
            "<kbd>P</kbd>",
        ]))

    def test_controls_are_escaped(self):
        self.assertEqual(
            render_shell.render_controls("<b> [<]"),
            '<span class="controls-copy">&lt;b&gt;</span>\n<kbd>&lt;</kbd>',
        )

    def test_canvas_size(self):
        self.assertEqual(render_shell.canvas_size("canvasWidth: 720\r\ncanvasHeight: 1280\r\n"), ("720", "1280"))
        self.assertEqual(render_shell.canvas_size("canvasWidth: 720\n"), ("1280", "720"))

    def test_render(self):
        page = render_shell.render(TEMPLATE, {**ENV, "SUBTITLE": "Fly & flap", "CONTROLS": "Flap [Space]"}, "")
        self.assertNotRegex(page, r"\{\{\w+\}\}")
        self.assertIn("{{{ SCRIPT }}}", page)
        self.assertIn("<title>Tappy Plane — Doriax Engine</title>", page)
        self.assertIn('<meta name="description" content="Fly &amp; flap">', page)
        self.assertIn("<kbd>Space</kbd>", page)
        self.assertIn('width="1280" height="720"', page)

    def test_description(self):
        page = render_shell.render(TEMPLATE, {**ENV, "SUBTITLE": "Short", "DESCRIPTION": "Long"}, "")
        self.assertIn('<meta name="description" content="Long">', page)


if __name__ == "__main__":
    unittest.main()
