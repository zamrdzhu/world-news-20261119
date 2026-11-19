#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026.

Reads stories.json and paints THE WORLD TODAY, a 1024x1024 newspaper
front page, to entry.png. Pillow is the only dependency. No network,
no clock, no randomness: the same stories.json always paints the
same bytes."""

import json
from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
SIDE = 34
WIDTH = CANVAS - 2 * SIDE
INK = (20, 20, 20)
PAPER = (253, 252, 246)
RED = (158, 24, 24)
GREY = (98, 94, 86)
PALE = (205, 201, 191)
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class Types:
    """A small cache so each face/size pair is loaded once."""

    def __init__(self):
        self._seen = {}

    def get(self, path, size):
        key = (path, size)
        if key not in self._seen:
            self._seen[key] = ImageFont.truetype(path, size)
        return self._seen[key]


def wrap_text(text, font, pixels, lines=None):
    """Greedy wrap measured with the real font, trimming with an ellipsis."""
    words = text.split()
    out = []
    while words:
        line = words.pop(0)
        while words and font.getlength(line + " " + words[0]) <= pixels:
            line += " " + words.pop(0)
        out.append(line)
    if lines is not None and len(out) > lines:
        out = out[:lines]
        tail = out[-1]
        while tail and font.getlength(tail + "…") > pixels:
            tail = tail[:-1].rstrip()
        out[-1] = tail + "…"
    return out


class FrontPage:
    def __init__(self, data):
        self.data = data
        self.image = Image.new("RGB", (CANVAS, CANVAS), PAPER)
        self.pen = ImageDraw.Draw(self.image)
        self.types = Types()

    def rule(self, y, weight, colour=INK):
        self.pen.rectangle([SIDE, y, CANVAS - SIDE, y + weight - 1], fill=colour)

    def centred(self, text, y, font, colour=INK):
        self.pen.text((CANVAS // 2, y), text, font=font, fill=colour, anchor="ma")

    def paragraph(self, lines, x, y, font, colour=INK, leading=None):
        step = leading if leading is not None else int(font.size * 1.2)
        for line in lines:
            self.pen.text((x, y), line, font=font, fill=colour)
            y += step
        return y

    def emblem(self, cx, cy, radius):
        """A small globe: outline, meridian, equator, one parallel."""
        pen = self.pen
        pen.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                    outline=INK, width=2)
        pen.ellipse([cx - radius * 0.38, cy - radius, cx + radius * 0.38,
                     cy + radius], outline=INK, width=1)
        pen.line([cx - radius, cy, cx + radius, cy], fill=INK, width=1)
        pen.arc([cx - radius, cy - radius * 0.6, cx + radius,
                 cy + radius * 0.6], start=205, end=335, fill=INK, width=1)

    def masthead(self):
        self.rule(28, 4)
        self.rule(35, 1)
        self.emblem(SIDE + 17, 72, 14)
        self.emblem(CANVAS - SIDE - 17, 72, 14)
        self.centred(self.data["paper"], 42, self.types.get(SERIF_BOLD, 56))
        self.centred(self.data["date"], 102, self.types.get(SANS_BOLD, 27), RED)
        self.centred(self.data["tagline"], 132,
                     self.types.get(SERIF_ITALIC, 20))
        self.rule(158, 3)
        return 170

    def lead_story(self, y):
        lead = self.data["lead"]
        kick = self.types.get(SANS_BOLD, 20)
        self.pen.text((SIDE, y), lead["kicker"], font=kick, fill=RED)
        head = self.types.get(SERIF_BOLD, 43)
        y = self.paragraph(wrap_text(lead["headline"], head, WIDTH, lines=2),
                           SIDE, y + 26, head, leading=48)
        deck = self.types.get(SANS, 21)
        y = self.paragraph(wrap_text(lead["deck"], deck, WIDTH, lines=2),
                           SIDE, y + 8, deck, leading=26)
        self.rule(y + 12, 2)
        return y + 24

    def story_cell(self, story, x, y, col_w):
        kick = self.types.get(SANS_BOLD, 20)
        self.pen.text((x, y), story["section"], font=kick, fill=RED)
        head = self.types.get(SERIF_BOLD, 22)
        y = self.paragraph(wrap_text(story["headline"], head, col_w, lines=2),
                           x, y + 24, head, leading=25)
        body = self.types.get(SANS, 20)
        self.paragraph(wrap_text(story["body"], body, col_w, lines=2),
                       x, y + 4, body, leading=22)

    def grid(self, y):
        row_h, gutter = 130, 18
        col_w = (WIDTH - 2 * gutter) // 3
        xs = [SIDE, SIDE + col_w + gutter, SIDE + 2 * (col_w + gutter)]
        tops = [y, y, y]
        for i, story in enumerate(self.data["stories"][:12]):
            col = i % 3
            x, top = xs[col], tops[col]
            self.story_cell(story, x, top, col_w)
            if col < 2:
                mid = x + col_w + gutter // 2
                self.pen.line([mid, top + 2, mid, top + row_h - 12],
                              fill=PALE, width=1)
            if i // 3 < 3:
                self.pen.line([x, top + row_h - 4, x + col_w, top + row_h - 4],
                              fill=PALE, width=1)
            tops[col] += row_h
        return y + 4 * row_h

    def briefs(self, y):
        self.rule(y + 6, 2)
        kick = self.types.get(SANS_BOLD, 20)
        body = self.types.get(SANS, 20)
        col_w = (WIDTH - 36) // 3
        xs = [SIDE, SIDE + col_w + 18, SIDE + 2 * (col_w + 18)]
        base = y + 16
        for i, story in enumerate(self.data["stories"][12:15]):
            x = xs[i]
            self.pen.text((x, base), story["section"], font=kick, fill=RED)
            self.paragraph(wrap_text(story["headline"], body, col_w, lines=2),
                           x, base + 24, body, leading=22)
        return base + 72

    def footer(self, y):
        self.rule(y + 8, 1)
        self.centred(self.data["footer"], y + 16, self.types.get(SANS, 20), GREY)

    def paint(self):
        y = self.masthead()
        y = self.lead_story(y)
        y = self.grid(y)
        y = self.briefs(y)
        self.footer(y)
        return self.image


def main():
    with open("stories.json", encoding="utf-8") as handle:
        data = json.load(handle)
    page = FrontPage(data).paint()
    page.save("entry.png", optimize=True)
    print("saved entry.png", page.size)


if __name__ == "__main__":
    main()
