"""Shared Pygame UI rendering helpers (non-OOP)."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import pygame
from src.config import (
    COLOR_BORDE_CONTENEDOR,
    COLOR_BTN_VERDE_CLARO,
    COLOR_CHARCOAL,
    COLOR_MINT,
    COLOR_MOSS,
    COLOR_PINE,
    COLOR_RED_ALERT,
    COLOR_SAGE_LIGHT,
    COLOR_WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.ods.data import get_sdg_color, get_sdg_messages, get_sdg_name, list_sdg_ids

FONT_SIZE_SCALE = 1.2
FONT_DIR = Path(__file__).resolve().parents[2] / "assets" / "images" / "font"
FONT_CANDIDATES = (
    "PatrickHand-Regular.ttf",
    "ChildosFREEPERSONALUSE-Regular.otf",
    "ChildosFREEPERSONALUSE-Medium.otf",
    "ChildosFREEPERSONALUSE-SemiBold.otf",
    "ChildosFREEPERSONALUSE-Light.otf",
    "ChildosFREEPERSONALUSE-Bold.otf",
    "Childo.otf",
    "ChildosDEMO-Regular.otf",
)
FONT_PATH = None
for candidate in FONT_CANDIDATES:
    candidate_path = FONT_DIR / candidate
    if candidate_path.exists():
        FONT_PATH = candidate_path
        break
if FONT_PATH is None:
    FONT_PATH = FONT_DIR / FONT_CANDIDATES[0]


def _font_renders_sample(font: pygame.font.Font, sample: str) -> bool:
    """Return True when the font can render a representative sample without collapsing."""
    try:
        rendered = font.render(sample, True, (255, 255, 255))
        rect = rendered.get_rect()
        return rect.width > 0 and rect.height > 0
    except Exception:
        return False


def _font_has_lowercase_and_digits(font: pygame.font.Font) -> bool:
    """Return True when the font can render lowercase letters and digits."""
    sample = "0123456789abcdefghijklmnopqrstuvwxyz"
    return _font_renders_sample(font, sample)


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    """Return a Pygame font for the given size, preferring the bundled font when it renders digits properly."""
    if not pygame.font.get_init():
        pygame.font.init()

    scaled_size = max(1, int(size * FONT_SIZE_SCALE))
    try:
        font = pygame.font.Font(str(FONT_PATH), scaled_size)
        if font is not None and _font_has_lowercase_and_digits(font):
            if bold:
                font.set_bold(True)
            return font
    except Exception:
        pass

    for family in ("Arial", "Segoe UI", "Liberation Sans", "DejaVu Sans"):
        try:
            font = pygame.font.SysFont(family, scaled_size)
            if _font_has_lowercase_and_digits(font):
                if bold:
                    font.set_bold(True)
                return font
        except Exception:
            continue

    font = pygame.font.SysFont("Arial", scaled_size)
    if bold:
        font.set_bold(True)
    return font


def _blend_color(
    color_a: Tuple[int, int, int], color_b: Tuple[int, int, int], ratio: float
) -> Tuple[int, int, int]:
    """Combinar dos colores RGB por una proporción.

    ratio=0.0 -> color_a, ratio=1.0 -> color_b
    """
    r = int(color_a[0] + (color_b[0] - color_a[0]) * ratio)
    g = int(color_a[1] + (color_b[1] - color_a[1]) * ratio)
    b = int(color_a[2] + (color_b[2] - color_a[2]) * ratio)
    return (r, g, b)


def draw_text(
    surface,
    text,
    position,
    font_size=20,
    color=(0, 0, 0),
    center=False,
    font_name: Optional[str] = None,
    italic=False,
):
    font_size = int(round(font_size))
    font = None
    if font_name:
        try:
            font = pygame.font.Font(font_name, font_size)
        except Exception:
            font = None
    if font is None:
        font = get_font(font_size)
    if italic:
        font.set_italic(True)

    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    surface.blit(text_surface, rect)


def draw_button(
    surface: pygame.Surface,
    text: str,
    rect: pygame.Rect,
    font_size: int = 24,
    hovered: bool = False,
    active: bool = True,
    focused: bool = False,
    bg_color: Optional[Tuple[int, int, int]] = None,
    text_color: Optional[Tuple[int, int, int]] = None,
) -> pygame.Rect:
    """Dibujar un botón con feedback visual (hover, focus y pressed).

    Args:
        surface: Superficie donde dibujar.
        text: Texto del botón.
        rect: Rectángulo que define la posición y tamaño.
        hovered: Indica si el mouse está sobre el botón.
        active: Si False, el botón aparece deshabilitado.
        focused: Indica foco por teclado.

    Devuelve:
        pygame.Rect: El rectángulo del botón (idéntico al pasado como `rect`).
    """
    pressed = hovered and pygame.mouse.get_pressed()[0] and active
    if bg_color is None:
        bg_color = COLOR_BTN_VERDE_CLARO if active else COLOR_SAGE_LIGHT
    if (hovered or focused) and active:
        bg_color = COLOR_BORDE_CONTENEDOR
    if pressed:
        bg_color = COLOR_BORDE_CONTENEDOR
    pygame.draw.rect(surface, bg_color, rect, border_radius=8)
    border_width = 4 if focused else 2
    pygame.draw.rect(surface, COLOR_BORDE_CONTENEDOR, rect, width=border_width, border_radius=8)
    if text_color is None:
        if bg_color == COLOR_BORDE_CONTENEDOR:
            text_color = COLOR_WHITE
        else:
            text_color = COLOR_CHARCOAL
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
    """Dibujar un campo de texto simple y devolver su rectángulo.

    Si `focused` se muestra un cursor; si `mask` es True se enmascara el texto.

    Devuelve:
        pygame.Rect: El rectángulo donde se dibujó el campo.
    """
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
    surface: pygame.Surface, rect: pygame.Rect, title: Optional[str] = None
) -> None:
    """Dibujar un panel simple con título opcional.

    Devuelve: None (operación de dibujo sobre `surface`).
    """
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
    """Dibujar un mensaje de error con color de alerta.

    Devuelve: None (operación de dibujo sobre `surface`).
    """
    draw_text(surface, message, position, font_size=font_size, color=COLOR_RED_ALERT)


def wrap_text(text: str, max_width: int, font_size: int = 20) -> List[str]:
    """Ajustar texto en varias líneas usando la fuente correcta de Canva."""
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


def draw_message_panel(
    surface: pygame.Surface,
    state: Dict[str, Any],
    sdg_id: Optional[int] = None,
    panel_height: int = 55,
) -> None:
    """Dibujar un panel inferior con mensajes rotativos relacionados al ODS.

    Si `sdg_id` no se pasa, se intenta recuperar uno almacenado en la sesión
    o se elige uno aleatoriamente.
    """
    import random

    panel_rect = pygame.Rect(
        0, WINDOW_HEIGHT - panel_height, WINDOW_WIDTH, panel_height
    )
    session = state.get("session", {})
    if sdg_id is None:
        sdg_id = session.get("bottom_sdg_id")
        if sdg_id is None:
            sdg_id = random.choice(list_sdg_ids())
            session["bottom_sdg_id"] = sdg_id
    sdg_color = get_sdg_color(sdg_id)
    soft_bg = _blend_color(COLOR_WHITE, sdg_color, 0.12)
    pygame.draw.rect(surface, soft_bg, panel_rect)
    messages = get_sdg_messages(sdg_id)
    if not messages:
        return
    message_index = pygame.time.get_ticks() // 5000 % len(messages)
    message = messages[message_index]
    sdg_name = get_sdg_name(sdg_id)
    badge_radius = 16
    badge_center = (panel_rect.x + 35, panel_rect.centery)
    pygame.draw.circle(surface, sdg_color, badge_center, badge_radius)
    pygame.draw.circle(surface, COLOR_WHITE, badge_center, badge_radius, width=2)
    draw_text(
        surface, str(sdg_id), badge_center, font_size=15, color=COLOR_WHITE, center=True
    )
    title_x = badge_center[0] + badge_radius + 12
    title_y = panel_rect.y + 8
    draw_text(
        surface,
        f"ODS {sdg_id}: {sdg_name}",
        (title_x, title_y),
        font_size=12,
        color=sdg_color,
        center=False,
    )
    quote_font = get_font(22, bold=True)
    quote_surface = quote_font.render(
        '"', True, _blend_color(sdg_color, COLOR_WHITE, 0.6)
    )
    surface.blit(quote_surface, (title_x + 360, title_y - 6))
    max_width = WINDOW_WIDTH - title_x - 90
    message_font = get_font(14, bold=True)
    lines = wrap_text(message, max_width, font_size=14)
    line_height = 18
    for index, line in enumerate(lines[:2]):
        rendered = message_font.render(line, True, COLOR_CHARCOAL)
        surface.blit(rendered, (title_x, title_y + 18 + index * line_height))
