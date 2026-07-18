import pytest

from src.core.calculation_engine import make_engine_context
from src.core.calculation_rules import build_default_registry
from src.core.dependencies import make_dependency_checker
from src.ui.screens import calculation_demo_screen
from src.ui.screens.calculation_screen import (focus_next, focus_previous,
                                               make_screen)
from src.ui.state.calculation_state import make_state


@pytest.fixture
def screen():
    engine_context = make_engine_context(build_default_registry(), [], make_dependency_checker())
    return make_screen(engine_context, make_state())

@pytest.fixture
def demo_state():
    state = {'current_screen': 'calculator', 'session': {}}
    calculation_demo_screen.init_calculation_demo(state)
    return state

def test_screen_supports_focus_navigation(screen):
    assert 'focus_next' not in screen
    assert 'focus_previous' not in screen
    assert 'focused_control' in screen

def test_focus_next_cycles_through_controls(screen):
    assert screen['focused_control'] == 'calculate_button'
    focus_next(screen)
    assert screen['focused_control'] == 'cancel_button'
    focus_next(screen)
    assert screen['focused_control'] == 'calculate_button'

def test_focus_previous_cycles(screen):
    focus_next(screen)
    focus_previous(screen)
    assert screen['focused_control'] == 'calculate_button'

def test_demo_screen_uses_calculation_screen_focus_on_tab(demo_state):
    import pygame
    demo_screen = demo_state['calculation_demo_screen']
    assert demo_screen['focused_control'] == 'calculate_button'
    tab_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_TAB, mod=0)
    calculation_demo_screen.handle_event(demo_state, tab_event)
    assert demo_screen['focused_control'] == 'cancel_button'

def test_demo_screen_shift_tab_moves_focus_back(demo_state):
    import pygame
    demo_screen = demo_state['calculation_demo_screen']
    focus_next(demo_screen)
    assert demo_screen['focused_control'] == 'cancel_button'
    shift_tab_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_TAB, mod=pygame.KMOD_SHIFT)
    calculation_demo_screen.handle_event(demo_state, shift_tab_event)
    assert demo_screen['focused_control'] == 'calculate_button'