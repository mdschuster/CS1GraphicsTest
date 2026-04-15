from graphics import *
import time
import __main__

# ------------------------
# Internal State (hidden)
# ------------------------

_win = None
_width = 400
_height = 400
_bg = "white"
_fps = 60
_running = True
_dt = 0
_time = 0
_last_frame = None
__main__.dt = _dt
__main__.time = _time

_shapes = {}          # id -> object
_shape_meta = {}      # id -> (type, params)

_last_key = None
_mouse_pos = None

# ------------------------
# Keyboard Constants
# ------------------------

LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = "Down"

SPACE = "space"
ENTER = "Return"
ESCAPE = "Escape"

A = "a"
D = "d"
W = "w"
S = "s"


# ------------------------
# Color Constants
# ------------------------
RED = "red"
GREEN = "green"
BLUE = "blue"
WHITE = "white"
BLACK = "black"



# ------------------------
# Setup / Window
# ------------------------

def create_canvas(width=400, height=400, title="CS1 Graphics"):
    global _win, _width, _height
    _width = width
    _height = height
    _win = GraphWin(title, width, height, autoflush=False)
    set_background(_bg)

def set_fps(fps):
    global _fps
    _fps = fps

def set_background(color):
    global _bg
    _bg = color
    if _win:
        _win.setBackground(color)

def quit():
    global _running
    _running = False

    try:
        if _win:
            _win.close()
    except:
        pass

# ------------------------
# Input
# ------------------------

def _update_input():
    global _last_key, _mouse_pos, _running

    if not _win:
        return

    try:
        key = _win.checkKey()
        if key:
            _last_key = key

            # ESC exits program cleanly
            if key == ESCAPE:
                quit()

        mouse = _win.checkMouse()
        if mouse:
            _mouse_pos = (mouse.getX(), mouse.getY())

    except Exception:
        # Window was closed via X button
        quit()

def get_key():
    global _last_key
    key = _last_key
    _last_key = None
    return key

def get_mouse():
    return _mouse_pos

# ------------------------
# Time
# ------------------------

def get_dt():
    return _dt

def get_time():
    return _time

# ------------------------
# Color Utilities
# ------------------------

def rgb(r, g, b):
    """Convert (r,g,b) in 0–255 to a Tk color string"""
    return f"#{r:02x}{g:02x}{b:02x}"

def _normalize_color(color):
    if isinstance(color, tuple):
        return rgb(*color)
    return color

# ------------------------
# Shape Helpers
# ------------------------

def _create_circle(x, y, r, color):
    c = Circle(Point(x, y), r)
    c.setFill(_normalize_color(color))
    c.draw(_win)
    return c

def _create_rectangle(x, y, w, h, color):
    r = Rectangle(Point(x, y), Point(x + w, y + h))
    r.setFill(_normalize_color(color))
    r.draw(_win)
    return r

def _create_text(x, y, msg, size):
    t = Text(Point(x, y), msg)
    t.setSize(size)
    t.draw(_win)
    return t

# ------------------------
# Public Drawing API
# ------------------------

def circle(id, x, y, r, color="black"):
    _update_shape(id, "circle", (x, y, r, color))

def rectangle(id, x, y, w, h, color="black"):
    _update_shape(id, "rect", (x, y, w, h, color))

def text(id, x, y, msg, size=12):
    _update_shape(id, "text", (x, y, msg, size))

def remove(id):
    if id in _shapes:
        _shapes[id].undraw()
        del _shapes[id]
        del _shape_meta[id]

# ------------------------
# Update Logic
# Because of the way that Tkinter does things,
# we don't have access to the low level double buffer
# so there is flicker if we don't update the shapes
# instead of redraw them (it's a pita)
# ------------------------

def _update_shape(id, shape_type, params):
    if id not in _shapes:
        obj = _create(shape_type, params)
        _shapes[id] = obj
        _shape_meta[id] = (shape_type, params)
        return

    old_type, old_params = _shape_meta[id]

    # If type changed, recreate
    if old_type != shape_type:
        _shapes[id].undraw()
        obj = _create(shape_type, params)
        _shapes[id] = obj
        _shape_meta[id] = (shape_type, params)
        return

    obj = _shapes[id]

    # --- Circle ---
    if shape_type == "circle":
        x, y, r, color = params
        ox, oy, or_, oc = old_params

        # Move
        dx = x - ox
        dy = y - oy
        obj.move(dx, dy)

        # Resize or recolor → recreate
        if r != or_ or _normalize_color(color) != _normalize_color(oc):
            obj.undraw()
            obj = _create_circle(x, y, r, color)
            _shapes[id] = obj

    # --- Rectangle ---
    elif shape_type == "rect":
        x, y, w, h, color = params
        ox, oy, ow, oh, oc = old_params

        dx = x - ox
        dy = y - oy
        obj.move(dx, dy)

        if w != ow or h != oh or color != oc:
            obj.undraw()
            obj = _create_rectangle(x, y, w, h, color)
            _shapes[id] = obj

    # --- Text ---
    elif shape_type == "text":
        x, y, msg, size = params
        ox, oy, om, os = old_params

        dx = x - ox
        dy = y - oy
        obj.move(dx, dy)

        if msg != om or size != os:
            obj.undraw()
            obj = _create_text(x, y, msg, size)
            _shapes[id] = obj

    _shape_meta[id] = (shape_type, params)

def _create(shape_type, params):
    if shape_type == "circle":
        return _create_circle(*params)
    elif shape_type == "rect":
        return _create_rectangle(*params)
    elif shape_type == "text":
        return _create_text(*params)

# ------------------------
# Main Loop
# ------------------------

def run():
    global _dt, _time, _last_frame

    if hasattr(__main__, "setup"):
        __main__.setup()

    _last_frame = time.time()

    while _running:
        now = time.time()

        # --- dt calculation ---
        _dt = now - _last_frame
        _last_frame = now

        _time += _dt
        __main__.dt = _dt
        __main__.time = _time

        #--- input ---
        _update_input()

        #--- Student Draw ---
        try:
            if hasattr(__main__, "draw"):
                __main__.draw()
        except Exception:
            # If draw crashes, fail gracefully instead of killing students
            quit()

        try:
            if _win:
                _win.update()
        except Exception:
            quit()

        time.sleep(1 / _fps)
# final cleanup safety
    try:
        if _win:
            _win.close()
    except:
        pass