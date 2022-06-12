# from src.common import vkeys

# vkeys.press('c', 1)

import os
import ctypes
import win32api
import re
from pynput.keyboard import Key, Controller
import win32gui

keyboard = Controller()

window = None


def _window_enum_callback(hwnd, wildcard):
    """Pass to win32gui.EnumWindows() to check all the opened windows"""
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        win32gui.SetForegroundWindow(hwnd)


def set_foreground(wildcard):
    """put the window in the foreground"""
    win32gui.EnumWindows(_window_enum_callback, wildcard)


PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def press_key(key):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    flags = 0x0008

    ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    flags = 0x0008 | 0x0002

    ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def get_game_window():
    # Game window is named 'Minecraft 1.13.1' for example.
    set_foreground('MapleStory*')


get_game_window()
keyboard.press('c')
press_key(0x2E)
release_key(0x2E)  # h
press_key(0x12)
release_key(0x12)  # e
press_key(0x26)
release_key(0x26)  # l
press_key(0x26)
release_key(0x26)  # l
press_key(0x18)
release_key(0x18)  # o
