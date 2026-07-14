"""Shared Pygame UI rendering helpers (non-OOP)."""

from typing import Any, Dict, List, Optional, Tuple

import pygame

from src.config import (
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_MOSS,
    COLOR_PINE,
    COLOR_RED_ALERT,
    COLOR_SAGE_LIGHT,
    COLOR_WHITE,
)


def get_font(size: int) -> pygame.font.Font:
    """Return a Pygame font for the given size."""
    return pygame.font.SysFont("Arial", size)


def draw_text(
    surface: pygame.Surface,
    text: str,
    position: Tuple[int, int],
    font_size: int = 24,
    color: Tuple[int, int, int] = COLOR_CHARCOAL,
    center: bool = False,
) -> pygame.Rect:
    """Draw text on a surface and return its bounding rectangle."""
    font = get_font(font_size)
    rendered = font.render(str(text), True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    surface.blit(rendered, rect)
    return rect


def draw_button(
    surface: pygame.Surface,
    text: str,
    rect: pygame.Rect,
    font_size: int = 24,
    hovered: bool = False,
    active: bool = True,
    focused: bool = False,
) -> pygame.Rect:
    """Draw a button with hover, focus and click feedback."""
    pressed = hovered and pygame.mouse.get_pressed()[0] and active
    bg_color = COLOR_MOSS if active else COLOR_SAGE_LIGHT
    if (hovered or focused) and active:
        bg_color = COLOR_PINE
    if pressed:
        bg_color = (46, 82, 45)
    pygame.draw.rect(surface, bg_color, rect, border_radius=6)
    border_width = 4 if focused else 2
    pygame.draw.rect(surface, COLOR_CHARCOAL, rect, width=border_width, border_radius=6)
    text_color = (
        COLOR_WHITE if (hovered or focused or pressed) and active else COLOR_CHARCOAL
    )
    offset = 2 if pressed else 0
    draw_text(
        surface,
        text,
        (rect.centerx + offset, rect.centery + offset),
        font_size=font_size,
        color=text_color,
        center=True,
    )
    return rect


def draw_input(
    surface: pygame.Surface,
    value: str,
    rect: pygame.Rect,
    focused: bool = False,
    mask: bool = False,
    placeholder: str = "",
) -> pygame.Rect:
    """Draw a text input field and return its rectangle."""
    bg_color = COLOR_WHITE if focused else COLOR_MINT
    pygame.draw.rect(surface, bg_color, rect)
    border_color = COLOR_PINE if focused else COLOR_SAGE_LIGHT
    pygame.draw.rect(surface, border_color, rect, width=2)

    text_color = COLOR_CHARCOAL
    display_text = ""
    if value:
        display_text = "*" * len(value) if mask else value
    elif not focused:
        display_text = placeholder
        text_color = COLOR_SAGE_LIGHT

    text_surface = get_font(22).render(display_text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.midleft = (rect.x + 10, rect.centery)
    surface.blit(text_surface, text_rect)

    if focused:
        cursor_x = text_rect.right + 2
        cursor_top = rect.y + 8
        cursor_bottom = rect.bottom - 8
        pygame.draw.line(
            surface,
            COLOR_CHARCOAL,
            (cursor_x, cursor_top),
            (cursor_x, cursor_bottom),
            2,
        )
    return rect


def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    title: Optional[str] = None,
) -> None:
    """Draw a simple panel with an optional title."""
    pygame.draw.rect(surface, COLOR_WHITE, rect, border_radius=8)
    pygame.draw.rect(surface, COLOR_SAGE_LIGHT, rect, width=2, border_radius=8)
    if title:
        draw_text(
            surface, title, (rect.x + 15, rect.y + 10), font_size=22, color=COLOR_PINE
        )


def draw_error_message(
    surface: pygame.Surface,
    message: str,
    position: Tuple[int, int],
    font_size: int = 20,
) -> None:
    """Draw an error message in alert color."""
    draw_text(surface, message, position, font_size=font_size, color=COLOR_RED_ALERT)


def wrap_text(text: str, max_width: int, font_size: int = 20) -> List[str]:
    """Wrap text into lines that fit within max_width pixels."""
    font = get_font(font_size)
    words = str(text).split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines
