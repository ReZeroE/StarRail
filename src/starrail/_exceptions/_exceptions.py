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

class StarRailBaseException(Exception):
    __module__ = 'builtins'
    def __init__(self, message):
        super().__init__(message)

class StarRailModuleException(Exception):
    __module__ = 'builtins'
    def __init__(self, err_code):
        self.message = f"\nAn unexpected exception has occurred ({err_code}). Please seek help at https://github.com/ReZeroE/StarRail/issues."
        super().__init__(self.message)
        
class StarRailOSNoteSupported(Exception):
    __module__ = 'builtins'
    def __init__(self):
        super().__init__(f"\nThe starrail package only supports Windows installations of Honkai Star Rail.")

class StarRailGameNotFoundException(Exception):
    __module__ = 'builtins'
    def __init__(self, err_code):
        if err_code == "A0":
            self.message = f"\nHonkai Star Rail cannot be found on the local machine."
        elif err_code == "M0":
            self.message = f"\nThe provided absolute path to Honkai Star Rail does not exist."
        elif err_code == "M1":
            self.message = f"\nThe provided path does not correspond to the Honkai Star Rail executable (StarRail.exe)."
        else:
            raise StarRailBaseException("\nStarRailGameNotFoundException raised with no error code.")
        super().__init__(self.message)