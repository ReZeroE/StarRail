"""
StarRail
=====
Provides Honkai Star Rail Gameplay Automation
"""

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

__author__  = "Kevin L."
__version__ = "0.0.3"
__support__ = "Honkai Star Rail"
__all__     = ["starrail"]


from ._utils._utils import *
from ._exceptions._exceptions import *
from .honkai_star_rail import HonkaiStarRail
from .logic.grind_logic.grind_controller import StarRailGrindController
from .logic.login_logic.login_controller import StarRailLoginController # LOG-IN Controller, NOT Logic Controller
from .logic.rewards_logic.rewards_controller import StarRailRewardsController

if check_platform() == False:
    raise StarRailOSNotSupported()