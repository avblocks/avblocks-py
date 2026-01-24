"""
MetaPictureList collection for AVBlocks Python bindings.
"""

import ctypes

from .native import get_native
from .object_collection import ObjectCollection
from .meta_picture import MetaPicture


class MetaPictureList(ObjectCollection[MetaPicture]):
    """Collection of MetaPicture objects."""

    # pylint: disable=protected-access
    def to_native(self, native_pics: ctypes.c_void_p):
        """
        Add all pictures from this Python list to the provided native MetaPictureList pointer.
        The native_pics should be obtained via lib.Metadata_pictures(native_metadata).
        """
        if not native_pics:
            return

        lib = get_native().lib
        for pic in self:
            native_pic = pic._to_native()
            lib.MetaPictureList_add(native_pics, native_pic)
            lib.Reference_release(native_pic)

    # pylint: disable=protected-access
    @staticmethod
    def from_native(native_pics: ctypes.c_void_p) -> 'MetaPictureList':
        """
        Create a Python MetaPictureList from a native MetaPictureList pointer.
        """
        pics = MetaPictureList()
        if not native_pics:
            return pics

        lib = get_native().lib
        count = lib.MetaPictureList_count(native_pics)
        for i in range(count):
            native_pic = lib.MetaPictureList_at(native_pics, i)
            pic = MetaPicture._from_native(native_pic)
            if pic is not None:
                pics.add(pic)

        return pics
