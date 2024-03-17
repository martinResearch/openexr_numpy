"""openexr_numpy.

Martin de La Gorce. 2024.
"""

__version__ = "0.0.6"

__all__ = [
    "read",
    "write",
    "imread",
    "imwrite",
    "read_dict",
    "write_dict",
    "set_default_channel_names",
    "get_default_channel_names",
    "write_structured_array",
    "read_structured_array",
]

from .openexr_numpy import (get_default_channel_names, imread, imwrite, read,
                            read_structured_array, set_default_channel_names,
                            write, write_dict, write_structured_array)
