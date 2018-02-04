"""
Core code for Pytecode.

.. currentmodule:: pytecode._core
"""

# Re-export tokens first
# This means `from pytecode._core import tokens` will always acces the right tokens.
import sys

vertuple = sys.version_info[0:2]
if vertuple == (3, 6):
    from pytecode._core._tokens import tokens_36 as tokens
elif vertuple == (3, 7):
    from pytecode._core._tokens import tokens_37 as tokens
elif vertuple == (3, 8):
    from pytecode._core._tokens import tokens_38 as tokens
else:
    raise SystemError("Pytecode does not support this version of Python yet")

if tokens._pytecode_PY_VERSION != vertuple:
    raise SystemError("Token version marker does not match our version")