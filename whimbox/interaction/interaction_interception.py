import time
import string
import ctypes
import win32gui

from whimbox.common.cvars import *
from whimbox.interaction.interaction_template import InteractionTemplate

WHIMBOX_TO_INTERCEPTION = {
    # 直接映射
    **{k: k for k in (
        'backspace', 'tab', 'clear', 'enter', 'shift', 'ctrl', 'alt',
        'pause', 'esc', 'space', 'end', 'home', 'select', 'print',
        'delete', 'help',
    )},
    **{str(i): str(i) for i in range(10)},
    **{c: c for c in string.ascii_lowercase},
    **{f'f{i}': f'f{i}' for i in range(1, 13)},
    # 差异映射
    'caps_lock': 'capslock',
    'num_lock': 'numlock',
    'scroll_lock': 'scrolllock',
    'left_arrow': 'left',
    'up_arrow': 'up',
    'right_arrow': 'right',
    'down_arrow': 'down',
    'page_up': 'pageup',
    'page_down': 'pagedown',
    'print_screen': 'prtsc',
    'ins': 'insert',
    'del': 'delete',
    **{f'numpad_{i}': f'num{i}' for i in range(10)},
    'multiply_key': 'multiply',
    'add_key': 'add',
    'separator_key': 'separator',
    'subtract_key': 'subtract',
    'decimal_key': 'decimal',
    'divide_key': 'divide',
    'left_shift': 'shiftleft',
    'right_shift': 'shiftright',
    'right_shift ': 'shiftright',
    'left_control': 'ctrlleft',
    'right_control': 'ctrlright',
    'left_menu': 'altleft',
    'right_menu': 'altright',
    'browser_back': 'browserback',
    'browser_forward': 'browserforward',
    'browser_refresh': 'browserrefresh',
    'browser_stop': 'browserstop',
    'browser_search': 'browsersearch',
    'browser_favorites': 'browserfavorites',
    'browser_start_and_home': 'browserhome',
    'volume_mute': 'volumemute',
    'volume_down': 'volumedown',
    'volume_up': 'volumeup',
    'next_track': 'nexttrack',
    'previous_track': 'prevtrack',
    'stop_media': 'stop',
    'play/pause_media': 'playpause',
    'start_mail': 'launchmail',
    'select_media': 'lauchmediaselect',
    'start_application_1': 'launchapp1',
    'start_application_2': 'launchapp2',
    # 标点符号直接映射
    **{k: k for k in ('+', ',', '-', '.', '/', ';', '[', '\\', ']', "'")},
}

MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW


class InteractionInterception(InteractionTemplate):

    def __init__(self, hwnd_handler):
        import interception
        self._icp = interception
        self.hwnd_handler = hwnd_handler
        self._icp.auto_capture_devices(keyboard=True, mouse=True)
        self.WHEEL_DELTA = 120

    def _resolve_key(self, key: str):
        if len(key) == 1 and key in string.printable:
            return key.lower() if key.isalpha() else key
        mapped = WHIMBOX_TO_INTERCEPTION.get(key.lower())
        if mapped is not None:
            return mapped
        return key

    def _key_via_scancode(self, key: str, up: bool = False):
        vk_code = self.get_virtual_keycode(key)
        sc = MapVirtualKeyW(vk_code, 0)
        if sc == 0:
            raise KeyError(f"Cannot resolve scan code for key: {key}")
        from interception import KeyStroke
        flags = 0x01 if up else 0x00  # KEY_UP=1, KEY_DOWN=0
        stroke = KeyStroke(int(sc), flags)
        from interception.inputs import _g_context
        _g_context.send(_g_context.keyboard, stroke)

    # ── 键盘 ──

    def key_down(self, key):
        resolved = self._resolve_key(key)
        try:
            self._icp.key_down(resolved)
        except Exception:
            self._key_via_scancode(key, up=False)

    def key_up(self, key):
        resolved = self._resolve_key(key)
        try:
            self._icp.key_up(resolved)
        except Exception:
            self._key_via_scancode(key, up=True)

    def key_press(self, key):
        self.key_down(key)
        time.sleep(0.1)
        self.key_up(key)

    # ── 鼠标点击 ──

    def left_click(self):
        self._icp.mouse_down("left")
        time.sleep(0.1)
        self._icp.mouse_up("left")

    def left_down(self):
        self._icp.mouse_down("left")

    def left_up(self):
        self._icp.mouse_up("left")

    def left_double_click(self):
        self.left_click()
        time.sleep(0.05)
        self.left_click()

    def right_click(self):
        self._icp.mouse_down("right")
        time.sleep(0.1)
        self._icp.mouse_up("right")

    def right_down(self):
        self._icp.mouse_down("right")

    def right_up(self):
        self._icp.mouse_up("right")

    def middle_click(self):
        self._icp.mouse_down("middle")
        time.sleep(0.1)
        self._icp.mouse_up("middle")

    def middle_down(self):
        self._icp.mouse_down("middle")

    def middle_up(self):
        self._icp.mouse_up("middle")

    def middle_scroll(self, distance):
        distance = int(distance)
        if distance == 0:
            return
        direction = "up" if distance > 0 else "down"
        for _ in range(abs(distance)):
            self._icp.scroll(direction)

    # ── 鼠标移动 ──

    def move_to(self, x: int, y: int, resolution=None, anchor=ANCHOR_TOP_LEFT, relative=False, smooth=True):
        x = int(x)
        y = int(y)
        standard_w = 1920
        standard_h = 1080

        if resolution is not None:
            scale = resolution[1] / standard_w
        else:
            scale = 1

        if relative:
            x = int(x * scale)
            y = int(y * scale)
            if smooth:
                self.smooth_move_relative(x, y, duration=0.2)
            else:
                self._icp.move_relative(x, y)
        else:
            if resolution is not None:
                actual_h = int(resolution[0] / scale)
            else:
                actual_h = standard_h
            if "TOP" in anchor:
                pass
            elif "BOTTOM" in anchor:
                y += actual_h - standard_h
            elif "CENTER" in anchor:
                y += (actual_h - standard_h) / 2
            else:
                pass

            x = int(x * scale)
            y = int(y * scale)
            screen_x, screen_y = win32gui.ClientToScreen(self.hwnd_handler.get_handle(), (x, y))

            if smooth:
                self.smooth_move_absolute(screen_x, screen_y, duration=0.2)
            else:
                self._icp.move_to(screen_x, screen_y)

    def smooth_move_absolute(self, target_x: int, target_y: int, duration=0.2):
        from interception.beziercurve import BezierCurveParams
        self._icp.move_to(target_x, target_y, curve_params=BezierCurveParams())

    def smooth_move_relative(self, dx: int, dy: int, duration=0.2):
        distance = (dx**2 + dy**2) ** 0.5
        steps = max(10, int(distance / 20))
        delay = duration / steps
        moved_x = 0
        moved_y = 0

        for i in range(1, steps + 1):
            if i == steps:
                step_x = dx - moved_x
                step_y = dy - moved_y
            else:
                step_x = int(dx * i / steps) - moved_x
                step_y = int(dy * i / steps) - moved_y
            self._icp.move_relative(step_x, step_y)
            moved_x += step_x
            moved_y += step_y
            time.sleep(delay)

    def drag(self, origin_xy: list, target_xy: list):
        self.move_to(origin_xy[0], origin_xy[1])
        self._icp.mouse_down("left")
        self.move_to(target_xy[0], target_xy[1], smooth=True)
        self._icp.mouse_up("left")
