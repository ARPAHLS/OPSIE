"""
Terminal color management for OPSIIE.
Supports pastel (default) and vibrant palettes.
Switch palettes at runtime using set_palette().
All color functions use the active palette.
"""

import os
import msvcrt  # For Windows keyboard input

# --- Palette Definitions ---

PASTEL = {
    'lilac':   (200, 160, 255),
    'pink':    (255, 200, 200),
    'green':   (180, 255, 210),
    'yellow':  (255, 245, 180),
    'blue':    (180, 220, 255),
    'red':     (255, 180, 180),
    'cyan':    (180, 255, 255),
    'magenta': (240, 180, 255),
    'white':   (245, 245, 255),
    'gray':    (220, 210, 230),
    'light_white': (245, 245, 255),
}

VIBRANT = {
    'lilac':   (140,  60, 255),   # deeper purple
    'pink':    (255,  80, 120),   # hot pink
    'green':   ( 60, 255,  80),   # neon green
    'yellow':  (255, 220,  40),   # bright yellow
    'blue':    ( 60, 120, 255),   # electric blue
    'red':     (255,  60,  60),   # vivid red
    'cyan':    ( 60, 255, 255),   # bright cyan
    'magenta': (255,  60, 255),   # magenta
    'white':   (255, 255, 255),   # pure white
    'gray':    (180, 180, 200),   # steel gray
    'light_white': (255, 255, 255),
}

# --- Palette State ---

_active_palette = PASTEL

def set_palette(palette_name):
    """Switch the active color palette. Accepts 'pastel' or 'vibrant'."""
    global _active_palette
    if palette_name == 'vibrant':
        _active_palette = VIBRANT
    else:
        _active_palette = PASTEL

def _color(rgb, text):
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

# --- Color Functions (names unchanged) ---
def pastel_lilac(text):
    return _color(_active_palette['lilac'], text)
def pastel_pink(text):
    return _color(_active_palette['pink'], text)
def pastel_green(text):
    return _color(_active_palette['green'], text)
def pastel_yellow(text):
    return _color(_active_palette['yellow'], text)
def pastel_blue(text):
    return _color(_active_palette['blue'], text)
def pastel_red(text):
    return _color(_active_palette['red'], text)
def pastel_cyan(text):
    return _color(_active_palette['cyan'], text)
def pastel_magenta(text):
    return _color(_active_palette['magenta'], text)
def pastel_white(text):
    return _color(_active_palette['white'], text)
def pastel_gray(text):
    return _color(_active_palette['gray'], text)
def pastel_light_white(text):
    return _color(_active_palette['light_white'], text)

def pastel_color(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def pastel_gradient_bar(progress, total, length=40):
    # Use lilac to pink for gradient
    start_color = _active_palette['lilac']
    end_color = _active_palette['pink']
    bar = ''
    for i in range(length):
        ratio = i / (length - 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        if i < int(length * progress / total):
            bar += f'\033[38;2;{r};{g};{b}m█\033[0m'
        else:
            bar += f'\033[38;2;{r};{g};{b}m░\033[0m'
    return bar

def select_theme():
    """Minimal single-line theme selector. Palette is set after selection. Confirmation replaces selector line."""
    themes = [
        {"name": "Pastel", "palette": "pastel", "colors": PASTEL},
        {"name": "Vibrant", "palette": "vibrant", "colors": VIBRANT}
    ]
    selected = 0
    n_themes = len(themes)
    bar_colors = ['lilac', 'pink', 'green', 'blue', 'red']

    def color_bar(colors):
        bar = ''
        for cname in colors:
            r, g, b = colors[cname]
            bar += f'\033[48;2;{r};{g};{b}m \033[0m'
        return bar

    def vibrant_green(text):
        r, g, b = VIBRANT['green']
        return f'\033[38;2;{r};{g};{b}m{text}\033[0m'
    def vibrant_cyan(text):
        r, g, b = VIBRANT['cyan']
        return f'\033[38;2;{r};{g};{b}m{text}\033[0m'
    def vibrant_white(text):
        r, g, b = VIBRANT['white']
        return f'\033[38;2;{r};{g};{b}m{text}\033[0m'

    def print_selector():
        if selected == 0:
            label = pastel_green('[Select theme:]')
            sel_cyan = pastel_cyan
            sel_white = pastel_white
        else:
            label = vibrant_green('[Select theme:]')
            sel_cyan = vibrant_cyan
            sel_white = vibrant_white
        line = f'{label} '
        for i, theme in enumerate(themes):
            if i == selected:
                line += f"[ {sel_cyan(theme['name'])} ] "
            else:
                line += f"[ {sel_white(theme['name'])} ] "
        line += '  ' + color_bar(themes[selected]['colors'])
        print(line, end='\r', flush=True)

    print()
    print_selector()
    while True:
        key = msvcrt.getch()
        if key in (b'K', b'M', b'\xe0K', b'\xe0M'):  # Left/Right arrow (Windows)
            if key in (b'K', b'\xe0K'):
                selected = (selected - 1) % n_themes
            else:
                selected = (selected + 1) % n_themes
            print('\r' + ' '*80 + '\r', end='')  # Clear line
            print_selector()
        elif key == b'\r':  # Enter
            break
        elif key == b'\x1b':  # Escape sequence (ANSI)
            next_key = msvcrt.getch()
            if next_key == b'[':
                arrow_key = msvcrt.getch()
                if arrow_key == b'D':  # Left
                    selected = (selected - 1) % n_themes
                elif arrow_key == b'C':  # Right
                    selected = (selected + 1) % n_themes
                print('\r' + ' '*80 + '\r', end='')
                print_selector()
    set_palette(themes[selected]['palette'])
    # Erase selector line and print confirmation in its place
    print('\r' + ' '*80 + '\r', end='')
    if selected == 0:
        confirm = pastel_green('Theme selected: Pastel (Soft, Calm, Default)')
    else:
        confirm = vibrant_green('Theme selected: Vibrant (High-Contrast, Energetic)')
    print(confirm)
    print() 