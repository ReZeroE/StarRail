# SPDX-License-Identifier: MIT
# MIT License
#
# Copyright (c) 2023 Kevin L.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import psutil
import pytest
import time
import os
import time
import pyautogui
from elevate import elevate


import ctypes
import os

try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

print(is_admin)

# from typing import Optional
# from ctypes import wintypes, windll, create_unicode_buffer

# def getForegroundWindowTitle() -> Optional[str]:
#     hWnd = windll.user32.GetForegroundWindow()
#     length = windll.user32.GetWindowTextLengthW(hWnd)
#     buf = create_unicode_buffer(length + 1)
#     windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
#     # 1-liner alternative: return buf.value if buf.value else None
#     if buf.value:
#         return buf.value
#     else:
#         return None
    
# print(getForegroundWindowTitle())