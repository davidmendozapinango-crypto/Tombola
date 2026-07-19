import importlib

import pygame

from src.ui.common import get_font


class DummyFont:
    def __init__(self, *args, **kwargs):
        self.bold = False

    def set_bold(self, bold: bool) -> None:
        self.bold = bold

    def render(self, text: str, antialias: bool, color):
        if text:
            return pygame.Surface((0, 0))
        return pygame.Surface((10, 10))


class DummySystemFont(DummyFont):
    pass


def test_get_font_falls_back_when_custom_font_cannot_render_digits(monkeypatch):
    monkeypatch.setattr(pygame.font, "Font", lambda *args, **kwargs: DummyFont())

    def fake_sys_font(*args, **kwargs):
        return DummySystemFont()

    monkeypatch.setattr(pygame.font, "SysFont", fake_sys_font)

    font = get_font(24)

    assert isinstance(font, DummySystemFont)


def test_reload_uses_bundled_font_candidate():
    import src.ui.common as common

    reloaded = importlib.reload(common)

    assert reloaded.FONT_PATH.name == "PatrickHand-Regular.ttf"
