#!/usr/bin/env python3

import html
import os
import re
import sys
from pathlib import Path


def render_controls(controls):
    parts = []
    for line in controls.splitlines():
        # split() alternates between label text and [key] contents
        for i, text in enumerate(re.split(r"\[([^\]]+)\]", line)):
            text = html.escape(text.strip())
            if i % 2:
                parts.append(f"<kbd>{text}</kbd>")
            elif text:
                parts.append(f'<span class="controls-copy">{text}</span>')
    return "\n".join(parts)


def canvas_size(project):
    width = re.search(r"^canvasWidth: *(\d+)", project, re.M)
    height = re.search(r"^canvasHeight: *(\d+)", project, re.M)
    if width and height:
        return width[1], height[1]
    return "1280", "720"


def render(template, env, project):
    width, height = canvas_size(project)
    subtitle = env.get("SUBTITLE", "")
    values = {
        "TITLE": html.escape(env["TITLE"]),
        "SUBTITLE": html.escape(subtitle),
        "DESCRIPTION": html.escape(env.get("DESCRIPTION") or subtitle),
        "SOURCE_URL": html.escape(env["SOURCE_URL"]),
        "CONTROLS": render_controls(env.get("CONTROLS", "")),
        "WIDTH": width,
        "HEIGHT": height,
    }
    return re.sub(r"\{\{(\w+)\}\}", lambda match: values[match[1]], template)


def main():
    project_file, output_file = sys.argv[1:]
    template = Path(__file__).with_name("shell.html").read_text(encoding="utf-8")
    project = Path(project_file).read_text(encoding="utf-8")
    Path(output_file).write_text(render(template, os.environ, project), encoding="utf-8")


if __name__ == "__main__":
    main()
