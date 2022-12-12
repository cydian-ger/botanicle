import sys
from typing import List

Env = sys.modules[__name__]


if "args" not in Env.__dict__:
    Env.args = list()  # Only use after use
    env_args: List = Env.args
