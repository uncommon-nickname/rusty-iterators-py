from __future__ import annotations

import sys

# NOTE: 02.02.2025 <@uncommon-nickname>
# We support Python >= 3.10, so we version the type features only to
# this release. All of the versioned types should be put in this file,
# to avoid putting those ifs in every file.

if sys.version_info < (3, 13):
    from typing_extensions import TypeVar
else:
    from typing import TypeVar

if sys.version_info < (3, 12):
    from typing_extensions import override
else:
    from typing import override

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self


__all__ = ("Self", "TypeVar", "override")
