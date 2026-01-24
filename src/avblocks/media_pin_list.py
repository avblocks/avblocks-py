"""
MediaPinList collection for AVBlocks Python bindings.
"""

import ctypes

from .native import get_native
from .object_collection import ObjectCollection
from .media_pin import MediaPin

class MediaPinList(ObjectCollection[MediaPin]):
    """Collection of MediaPin objects."""

    # pylint: disable=protected-access
    def to_native(self, native_pins: ctypes.c_void_p):
        """
        Add all pins from this Python list to the provided native MediaPinList pointer.
        The native_pins should be obtained via lib.MediaSocket_pins(native_socket).
        """
        if not native_pins:
            return

        lib = get_native().lib
        for pin in self:
            native_pin = pin._to_native()
            lib.MediaPinList_add(native_pins, native_pin)
            lib.Reference_release(native_pin)

    # pylint: disable=protected-access
    @staticmethod
    def from_native(native_pins: ctypes.c_void_p) -> 'MediaPinList':
        """
        Create a Python MediaPinList from a native MediaPinList pointer.
        """
        pins = MediaPinList()
        if not native_pins:
            return pins

        lib = get_native().lib
        count = lib.MediaPinList_count(native_pins)
        for i in range(count):
            native_pin = lib.MediaPinList_at(native_pins, i)
            pin = MediaPin._from_native(native_pin)
            if pin is not None:
                pins.add(pin)

        return pins
