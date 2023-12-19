import sys

from .core.core import OpenCodeInterpreter

sys.modules["opencodeinterpreter"] = OpenCodeInterpreter()

"""
这样做的目的是当用户 `import opencodeinterpreter` 时，他们可以获得一个实例。
这是一个有争议的做法，因为也许模块应该表现得像模块。
但我认为这节省了一步，减少了摩擦，看起来很棒。
"""
