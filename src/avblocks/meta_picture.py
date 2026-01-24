"""
MetaPicture class for AVBlocks Python bindings.
"""

from typing import Optional
import ctypes

from .native import get_native
from .immutable import IImmutable
from .constants import MetaPictureType
from .string_util import decode_utf16le_string, encode_utf16le_string


class MetaPicture(IImmutable):
    """
    MetaPicture describes a meta image that is part of an audio or video file.
    """
    
    def __init__(self):
        """Creates a MetaPicture object."""
        self._mime_type: Optional[str] = None
        self._picture_type: int = MetaPictureType.Other
        self._description: Optional[str] = None
        self._bytes: Optional[bytes] = None
        self._immutable: bool = False
    
    @property
    def immutable(self) -> bool:
        """
        Returns whether the object is immutable.
        An immutable object cannot be modified and all modifying methods fail to produce a result.
        
        An immutable object can be modified by the AVBlocks library.
        Object immutability spreads to all nested objects.
        Therefore it is not possible to add/set an immutable object to a mutable object.
        When cloned an immutable object becomes mutable.
        """
        return self._immutable
    
    @immutable.setter
    def immutable(self, value: bool):
        """Set the immutable state."""
        self._immutable = value
    
    @property
    def mime_type(self) -> Optional[str]:
        """
        Picture mime type.
        """
        return self._mime_type
    
    @mime_type.setter
    def mime_type(self, value: Optional[str]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._mime_type = value
    
    @property
    def picture_type(self) -> int:
        """
        Picture type such as front cover, back cover, artist, etc.
        """
        return self._picture_type
    
    @picture_type.setter
    def picture_type(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._picture_type = value
    
    @property
    def description(self) -> Optional[str]:
        """
        Picture description as a free text.
        """
        return self._description
    
    @description.setter
    def description(self, value: Optional[str]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._description = value
    
    @property
    def bytes(self) -> Optional[bytes]:
        """
        Image bytes.
        
        The image is a jpeg, png or another image type.
        """
        return self._bytes
    
    @bytes.setter
    def bytes(self, value: Optional[bytes]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._bytes = value
    
    # pylint: disable=[protected-access]
    def clone(self) -> 'MetaPicture':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new MetaPicture object
        """
        picture = MetaPicture()
        picture._mime_type = self._mime_type
        picture._picture_type = self._picture_type
        picture._description = self._description
        picture._immutable = False
        
        # Deep copy bytes - ensure we create a new bytes object
        if self._bytes is not None:
            picture._bytes = bytes(bytearray(self._bytes))
        
        return picture
    
    def _to_native(self) -> ctypes.c_void_p:
        """Create a native MetaPicture object from this instance."""
        
        lib = get_native().lib
        native_pic = lib.avb_create_meta_picture()
        
        if self._mime_type:
            lib.MetaPicture_setMimeType(native_pic, self._mime_type.encode('utf-8'))
        
        lib.MetaPicture_setPictureType(native_pic, self._picture_type)
        
        if self._description:
            # Use the existing string utility for UTF-16-LE encoding
            desc_ptr = encode_utf16le_string(self._description)
            lib.MetaPicture_setDescription(native_pic, desc_ptr)
        
        if self._bytes and len(self._bytes) > 0:
            data_ptr = (ctypes.c_uint8 * len(self._bytes)).from_buffer_copy(self._bytes)
            lib.MetaPicture_setData(native_pic, ctypes.cast(data_ptr, ctypes.c_void_p), len(self._bytes))
        
        return native_pic
    
    def _copy_from_native(self, native_pic: ctypes.c_void_p):
        """Copy properties from a native MetaPicture object."""
        if not native_pic:
            return
        
        lib = get_native().lib
        
        # Get mime type
        mime_ptr = lib.MetaPicture_mimeType(native_pic)
        if mime_ptr:
            self._mime_type = ctypes.string_at(mime_ptr).decode('utf-8')
        
        # Get description (UTF-16-LE) - use existing string utility
        desc_ptr = lib.MetaPicture_description(native_pic)
        if desc_ptr:
            self._description = decode_utf16le_string(desc_ptr)
        
        # Get picture type
        self._picture_type = lib.MetaPicture_pictureType(native_pic)
        
        # Get data
        data_size = lib.MetaPicture_dataSize(native_pic)
        if data_size > 0:
            data_ptr = lib.MetaPicture_data(native_pic)
            self._bytes = bytes(ctypes.string_at(data_ptr, data_size))
    
    @staticmethod
    def _from_native(native: ctypes.c_void_p) -> Optional['MetaPicture']:
        """Create a MetaPicture object from a native MetaPicture pointer."""
        if not native:
            return None
        
        picture = MetaPicture()
        picture._copy_from_native(native)
        return picture
