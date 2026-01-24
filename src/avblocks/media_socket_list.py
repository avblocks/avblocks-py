"""
MediaSocketList collection for AVBlocks Python bindings.
"""

import ctypes

from .native import get_native
from .object_collection import ObjectCollection
from .media_socket import MediaSocket


class MediaSocketList(ObjectCollection[MediaSocket]):
    """Collection of MediaSocket objects."""

    # pylint: disable=protected-access
    def to_native(self, native_sockets: ctypes.c_void_p):
        """
        Add all sockets from this Python list to the provided native MediaSocketList pointer.
        The native_sockets should be obtained via lib.Transcoder_inputs(native_transcoder) or
        lib.Transcoder_outputs(native_transcoder).
        """
        if not native_sockets:
            return

        lib = get_native().lib
        for socket in self:
            native_socket = socket._to_native()
            lib.MediaSocketList_add(native_sockets, native_socket)
            lib.Reference_release(native_socket)

    # pylint: disable=protected-access
    @staticmethod
    def from_native(native_sockets: ctypes.c_void_p) -> 'MediaSocketList':
        """
        Create a Python MediaSocketList from a native MediaSocketList pointer.
        """
        sockets = MediaSocketList()
        if not native_sockets:
            return sockets

        lib = get_native().lib
        count = lib.MediaSocketList_count(native_sockets)
        for i in range(count):
            native_socket = lib.MediaSocketList_at(native_sockets, i)
            socket = MediaSocket._from_native(native_socket)
            if socket is not None:
                sockets.add(socket)

        return sockets
